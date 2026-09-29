/**
 * The column stand-in end to end with the product's own code and the real MCP Toolbox server
 * (@toolbox-sdk/server@1.13.1 over stdio, as the pack pins it). No AI Stackops server, no model.
 *
 *  1. The pack's mcp fragment and taxonomy parse (MCPServerConfigSchema, TaxonomySchema).
 *  2. toolboxReader.read → classifyCatalog('bigquery') over the catalog server's aiso_column_tags.
 *  3. columnFindings on the result (the compliance kinds a sync would produce).
 *  4. The data team re-tags Customer.Address after the classifier recorded an opinion on it
 *     (the opinion is SET BY HAND here: the classifier needs a model) → the findings again.
 *  5. The pack's named queries (scenario 22's included) on a copy of the demo-data server, each result through filterOutcome with
 *     a ReadFilter for Priya, Lena and Dana, with and without the internal model ceiling (enforce).
 *
 *   AISO_SRC=~/Dev/aiso-wt-skills node drafts/classification/probes/probe-columns.ts
 */
import { readFileSync, mkdtempSync, cpSync, mkdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir, homedir } from 'node:os';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const pack = path.resolve(here, '..', '..', '..');
const src = process.env.AISO_SRC ?? path.join(homedir(), 'Dev', 'aiso-wt-skills');
const load = (rel: string) => import(pathToFileURL(path.join(src, rel)).href);
const mod = (rel: string) => import(pathToFileURL(path.join(src, 'node_modules', rel)).href);

const YAML = (await mod('yaml/dist/index.js')).default;
const { Client } = await mod('@modelcontextprotocol/sdk/dist/esm/client/index.js');
const { StdioClientTransport } = await mod('@modelcontextprotocol/sdk/dist/esm/client/stdio.js');
const { TaxonomySchema, setTaxonomy } = await load('lib/auth/classification.ts');
const { MCPServerConfigSchema, ColumnSyncSchema } = await load('lib/mcp/types.ts');
const { toolboxReader, classifyCatalog } = await load('lib/mcp/columns/catalog.ts');
const { buildIndex, filterOutcome } = await load('lib/mcp/columns/column-filter.ts');
const { readCallResult } = await load('lib/mcp/call-result.ts');
const { toolboxStatement } = await load('lib/mcp/toolbox-statements.ts');
const { ReadFilter } = await load('lib/knowledge/read-filter.ts');
const { columnFindings } = await load('lib/auth/compliance.ts');

const TOOLBOX = ['-y', '@toolbox-sdk/server@1.13.1', '--stdio', '--config', 'tools.yaml'];
const work = mkdtempSync(path.join(tmpdir(), 'aiso-columns-'));

// ---- 1. the pack's config parses
const fragment = JSON.parse(readFileSync(path.join(pack, 'mcp', 'demo-data.mcp.json'), 'utf8'));
for (const [name, cfg] of Object.entries(fragment.servers)) MCPServerConfigSchema.parse(cfg), console.log(`mcp fragment: ${name} parses`);
const base = YAML.parse(readFileSync(path.join(pack, 'classification.yaml'), 'utf8'));
const taxonomy = TaxonomySchema.parse({ ...base, enforcement: 'enforce' });
setTaxonomy(taxonomy);
console.log('taxonomy parses (enforcement set to enforce for this probe)\n');

async function server(cwd: string) {
  const client = new Client({ name: 'probe', version: '0' });
  await client.connect(new StdioClientTransport({ command: 'npx', args: TOOLBOX, cwd, stderr: 'ignore' }));
  const tools = (await client.listTools()).tools;
  return { client, tools, call: async (tool: string, args: Record<string, unknown>) => readCallResult(await client.callTool({ name: tool, arguments: args })) };
}

// ---- 2. the catalog through the product's reader
const catalogDir = path.join(work, 'column-catalog');
cpSync(path.join(pack, 'data', 'column-catalog'), catalogDir, { recursive: true });
const catalog = await server(catalogDir);
console.log(`== 2. catalog server: tools ${catalog.tools.map((t: { name: string }) => t.name).join(', ')}`);
const sync = ColumnSyncSchema.parse(fragment.servers['demo-data'].columns);
async function readCatalog() {
  const snap = await toolboxReader.read({ tools: catalog.tools, sync, call: catalog.call });
  return { snap, rows: classifyCatalog(snap, sync.vocabulary ?? toolboxReader.vocabulary, taxonomy) };
}
let { snap, rows } = await readCatalog();
console.log(`snapshot: ${snap.columns.length} columns, ${snap.tags.length} tags, ${snap.masked.length} masked`);
console.log(`classified rows: ${rows.length} total, ${rows.filter((r: { level?: string }) => r.level).length} with a level`);
for (const r of rows.filter((r: { level?: string; unmapped: unknown[] }) => r.level || r.unmapped.length)) {
  console.log(`  ${r.objectRef}.${r.columnName}: ${r.level ?? '-'}${r.categories.length ? ` [${r.categories.join(', ')}]` : ''}${r.masked ? ' masked' : ''} by ${r.classifiedBy || '-'}${r.tags.length ? `; tags ${r.tags.map((t: { name: string; value?: string }) => `${t.name}=${t.value}`).join(', ')}` : ''}${r.unmapped.length ? `; UNMAPPED ${r.unmapped.map((t: { name: string; value?: string }) => `${t.name}=${t.value}`).join(', ')}` : ''}`);
}

// ---- 3. compliance findings
const asCompliance = (rs: typeof rows, opinions: Record<string, string> = {}) => [{
  name: 'demo-data', profile: 'toolbox', level: fragment.servers['demo-data'].classification.level, sync: true, via: 'demo-catalog', perPerson: false,
  masking: toolboxReader.masking, vocabulary: 'bigquery', state: { status: 'ok', lastSyncAt: new Date().toISOString() },
  columns: rs.map((r: { objectRef: string; columnName: string; level?: string; categories: string[]; unmapped: unknown[]; masked: boolean }) => ({ objectRef: r.objectRef, columnName: r.columnName, level: r.level, categories: r.categories, unmapped: r.unmapped, masked: r.masked, ...(opinions[`${r.objectRef}.${r.columnName}`] ? { modelLevel: opinions[`${r.objectRef}.${r.columnName}`] } : {}) })),
}];
const show = (fs: Array<{ severity: string; kind: string; target: string; message: string }>) => { for (const f of fs) console.log(`  [${f.severity}] ${f.kind} ${f.target}\n      ${f.message}`); };
console.log('\n== 3. compliance findings after the first sync');
show(columnFindings(asCompliance(rows), taxonomy));

// ---- 4. retag Customer.Address in place, with a classifier opinion recorded before
execFileSync('python3', [path.join(here, '..', 'generate_column_catalog.py'), '--variant', 'retagged', '--out', catalogDir], { stdio: 'inherit' });
({ snap, rows } = await readCatalog());
const addr = rows.find((r: { columnName: string; objectRef: string }) => r.objectRef.endsWith('Customer') && r.columnName === 'Address');
console.log(`\n== 4. after the retag: ${addr.objectRef}.Address ${addr.level} by ${addr.classifiedBy}; opinion confidential set by hand (as monitor would record it)`);
show(columnFindings(asCompliance(rows, { 'musicstore.Customer.Address': 'confidential' }), taxonomy).filter((f: { kind: string }) => f.kind === 'column-classifier-higher'));
({ snap, rows } = await (async () => { cpSync(path.join(pack, 'data', 'column-catalog', 'catalog.sqlite'), path.join(catalogDir, 'catalog.sqlite')); return readCatalog(); })());
await catalog.client.close();

// ---- 5. the filter on real results
const tb = path.join(work, 'toolbox');
mkdirSync(path.join(work, 'music-store'), { recursive: true });
cpSync(path.join(pack, 'data', 'music-store', 'musicstore.sqlite'), path.join(work, 'music-store', 'musicstore.sqlite'));
mkdirSync(path.join(work, 'pet-store'), { recursive: true });
cpSync(path.join(pack, 'data', 'pet-store', 'pet-store.db'), path.join(work, 'pet-store', 'pet-store.db'));
mkdirSync(tb, { recursive: true });
cpSync(path.join(pack, 'data', 'toolbox', 'tools.yaml'), path.join(tb, 'tools.yaml'));
const data = await server(tb);
console.log(`\n== 5. demo-data (the pack's tools.yaml): ${data.tools.length} tools`);
const index = buildIndex(rows.map((r: { objectRef: string; columnName: string; level?: string; categories: string[] }) => ({ objectRef: r.objectRef, columnName: r.columnName, level: r.level, categories: r.categories })));

const people = {
  'Priya (internal)': { type: 'user', id: 'p', name: 'priya', role: 'member', clearance: { level: 'internal', categories: [] } },
  'Lena (confidential, Finance)': { type: 'user', id: 'l', name: 'lena', role: 'member', clearance: { level: 'confidential', categories: ['Finance'] } },
  'Dana (admin)': { type: 'user', id: 'd', name: 'dana', role: 'admin' },
};
const calls: Array<[string, Record<string, unknown>]> = [
  ['customer_contact', { last_name: 'Leacock' }],
  ['customer_spend_by_country', { limit: 3 }],
  ['customer_purchases', { first_name: 'Heather', last_name: 'Leacock' }],
  ['longest_tracks', { limit: 2 }],
  ['artists_in_both_genres', { genre_a: 'Rock', genre_b: 'Metal' }],
];
for (const [tool, args] of calls) {
  const outcome = await data.call(tool, args);
  const statement = toolboxStatement('demo-data', tb, TOOLBOX, tool);
  const rec = { server: 'demo-data', tool, registryName: tool, args, extractor: 'toolbox', profile: 'toolbox', text: outcome.text, content: outcome.content, isError: false, startedAt: new Date().toISOString(), durationMs: 5, outcome: 'success', identity: { mode: 'service' }, mcpCallId: 'x', ...(statement ? { declared: { statement, language: 'sql' } } : {}) };
  console.log(`\n-- ${tool}(${JSON.stringify(args)}) ${statement ? '' : '(no declared statement!)'}\n   raw: ${outcome.text.slice(0, 150).replace(/\n/g, ' ')}…`);
  for (const [who, principal] of Object.entries(people)) {
    for (const ceiling of [undefined, 'internal']) {
      const rf = new ReadFilter('mcp:demo-data', new Map(), { level: 'internal' }, principal, ceiling, taxonomy);
      const d = filterOutcome({ rec, outcome, index, allow: (key: string, cls: unknown) => rf.allow(key, cls as never), taxonomy });
      const via = [...new Set(d.resolution.columns.map((c: { via: string }) => c.via))].join('/');
      console.log(`   ${who}${ceiling ? ', model ceiling internal' : ', local model'}: withheld [${d.withheld.join(', ')}]${d.unreadable ? ' WHOLE RESULT' : ''} (resolved by ${via})`);
      if (who.startsWith('Priya') && !ceiling && d.withheld.length) console.log(`      model sees: ${d.outcome.text.slice(0, 230).replace(/\n/g, ' ')}…`);
    }
  }
}
await data.client.close();
rmSync(work, { recursive: true, force: true });
