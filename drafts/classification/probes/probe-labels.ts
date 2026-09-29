/**
 * Reads data/labelled-files with the product's own code, no server and no model:
 *  1. OfficeLoader / PDFLoader on each file (labels, protection, first words of text);
 *  2. KnowledgeStore.loadDocuments with the pack's store YAML (so loader routing for an `office`
 *     store is the product's: PDFs to the PDF loader), from a temporary workspace;
 *  3. KnowledgeStore.applyDocumentLabels against a recording backend, with the pack's
 *     classification.yaml (TaxonomySchema.parse) — what each file is filed at.
 *
 *   AISO_SRC=~/Dev/aiso-wt-skills node drafts/classification/probes/probe-labels.ts
 */
import { readFileSync, readdirSync, mkdtempSync, cpSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir, homedir } from 'node:os';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const pack = path.resolve(here, '..', '..', '..');
const src = process.env.AISO_SRC ?? path.join(homedir(), 'Dev', 'aiso-wt-skills');
const load = (rel: string) => import(pathToFileURL(path.join(src, rel)).href);

const YAML = (await import(pathToFileURL(path.join(src, 'node_modules', 'yaml', 'dist', 'index.js')).href)).default;
const { OfficeLoader, PDFLoader } = await load('lib/knowledge/loaders/file-loaders.ts');
const { KnowledgeStore } = await load('lib/knowledge/knowledge-store.ts');
const { KnowledgeConfigSchema } = await load('lib/knowledge/types.ts');
const { TaxonomySchema, setTaxonomy, mapExternalLabel } = await load('lib/auth/classification.ts');

const dir = path.join(pack, 'data', 'labelled-files');
const files = readdirSync(dir).filter((f) => /\.(docx|xlsx|pptx|pdf)$/.test(f)).sort();

// ---- the taxonomy: the pack's classification.yaml (the draft mappings were merged into it)
const taxonomy = TaxonomySchema.parse(YAML.parse(readFileSync(path.join(pack, 'classification.yaml'), 'utf8')));
setTaxonomy(taxonomy);
console.log(`taxonomy parsed: levels ${taxonomy.levels.join(' < ')}; vocabularies ${Object.keys(taxonomy.mappings.external).join(', ')}\n`);

// ---- 1. each file through its loader
console.log('== 1. loaders ==');
for (const f of files) {
  const p = path.join(dir, f);
  const loader = f.endsWith('.pdf') ? new PDFLoader(p) : new OfficeLoader(p);
  const [doc] = await loader.load();
  const labels = (doc.metadata.externalLabels ?? []) as Array<{ id?: string; name?: string; siteId?: string; method?: string }>;
  console.log(`${f}`);
  console.log(`  labels: ${labels.length ? labels.map((l) => `${l.name ?? '(no name)'} ${l.id}${l.method ? ` ${l.method}` : ''}${l.siteId ? ` site ${l.siteId}` : ''}`).join('; ') : 'none'}`);
  if (doc.metadata.protected) console.log(`  protected: ${(doc.metadata.protected as { reason: string }).reason}`);
  else console.log(`  text: ${JSON.stringify(doc.pageContent.replace(/\s+/g, ' ').slice(0, 90))}…`);
  for (const l of labels) {
    const m = mapExternalLabel('purview', { id: l.id, name: l.name }, taxonomy);
    console.log(`  maps to: ${m ? `${m.level ?? '-'}${m.categories.length ? ` [${m.categories.join(', ')}]` : ''} (rows: ${m.matched.map((r: { match: string; key: string }) => `${r.match} ${r.key}`).join(', ')})` : 'NOTHING (unmapped)'}`);
  }
}

// ---- 2. the pack's store YAML, loaded as the product loads a directory store
console.log('\n== 2. the pack store (KnowledgeStore.loadDocuments) ==');
const cfg = KnowledgeConfigSchema.parse(YAML.parse(readFileSync(path.join(pack, 'knowledge', 'labelled-files.knowledge.yaml'), 'utf8')));
const ws = mkdtempSync(path.join(tmpdir(), 'aiso-labels-'));
mkdirSync(path.join(ws, 'bundles', 'aiso-demo-pack'), { recursive: true });
cpSync(dir, path.join(ws, 'bundles', 'aiso-demo-pack', 'labelled-files'), { recursive: true });
let loaded: Array<{ pageContent: string; metadata: Record<string, unknown> }>;
try {
  loaded = await KnowledgeStore.loadDocuments(cfg, ws);
} finally {
  // keep the temp workspace until the end: applyDocumentLabels only needs the metadata
}
console.log(`loader type ${cfg.loader.type}, pattern ${cfg.source.pattern}: ${loaded.length} document(s)`);
for (const d of loaded) console.log(`  ${path.basename(String(d.metadata.source))}: ${d.metadata.protected ? 'protected' : `${d.metadata.office ?? (d.metadata.pdf_pages !== undefined ? 'pdf' : '?')}, ${d.pageContent.length} chars`}`);

// ---- 3. what the index path files each document at
console.log('\n== 3. applyDocumentLabels (the index path) ==');
const calls: string[] = [];
const backend = {
  async setSourceUnreadable(i: { source: string; reason: string }) { calls.push(`${path.basename(i.source)}: UNREADABLE — ${i.reason}`); },
  async setSourceClassification(i: { source: string; level?: string; categories?: string[]; classifiedBy: string; reason: string }) {
    calls.push(`${path.basename(i.source)}: ${i.level}${i.categories?.length ? ` [${i.categories.join(', ')}]` : ''} by ${i.classifiedBy} (${i.reason})`);
  },
};
const labelled = await KnowledgeStore.applyDocumentLabels(backend, loaded, {}, 'labelled-files');
for (const c of calls) console.log(`  ${c}`);
const untouched = loaded.map((d) => path.basename(String(d.metadata.source))).filter((n) => !calls.some((c) => c.startsWith(`${n}:`)));
for (const n of untouched) console.log(`  ${n}: no row — reads at the store default (${cfg.classification?.level})`);
console.log(`\n${labelled.length} classified from labels, ${calls.filter((c) => c.includes('UNREADABLE')).length} unreadable, ${untouched.length} at the default`);
rmSync(ws, { recursive: true, force: true });
