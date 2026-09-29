# Notes for the platform scenarios

What each draft scenario rests on in the product (`~/Dev/aiso-wt-skills`, read 2026-09-29), the pack
or host config it needs, what a test harness can check locally and how, and what it cannot.
Nothing here was run: no server was started and no model was called.

The harness calls follow `scripts/bench.py` (cookie login through `POST /api/auth/login`, agents
through `POST /api/agents/<agent>/invoke` with `{input: {query}, sessionId}`, the provenance in
`response.metadata.provenance`). Paths below are relative to the product repository.

---

## §0 The cloud entries for this round

*Merged 2026-09-29:* DEMOS.md keeps its `claude-haiku` entry where these drafts say `gemini-flash`
(and `claude-haiku-4-5` for `claude-gemini-flash`), and adds `deepseek-flash` in *Before the day* as
scenario 28's candidate. Both are made on the Models tab, which now names entries (§9, item 1).

`models.yaml` (or the Models tab → OpenRouter, which writes the same and moves a typed key to the
secret store):

```yaml
llm:
  deepseek-flash:
    provider: openrouter
    model: deepseek/deepseek-v4.1-flash
    apiKey: ${OPENROUTER_API_KEY}
    maxTokens: 2048
    access: { minRole: member }
    maxClassification: internal
    budget: { usdPerDay: 1 }
    pricing: { inputPerMillion: <from OpenRouter>, outputPerMillion: <from OpenRouter> }
    active: true
  gemini-flash:
    provider: openrouter
    model: google/gemini-3.7-flash
    apiKey: ${OPENROUTER_API_KEY}
    maxTokens: 2048
    access: { minRole: member }
    maxClassification: internal
    budget: { usdPerDay: 1 }
    pricing: { inputPerMillion: <from OpenRouter>, outputPerMillion: <from OpenRouter> }
    active: true
```

`maxClassification` is the field behind the form's *Highest classification this model may be
shown* (`lib/llm/llm-config.ts:198`). Prices are left blank on purpose: I found no
source for these two models' prices in either repository.

Consequences of OpenRouter for this round, found while reading:
- The provider bill check (§6) reads Anthropic and OpenAI usage reports only
  (`lib/orchestrator.ts:2308` logs and skips anything else). With OpenRouter entries, scenario 33
  step 3 cannot run.
- Decisions (judge, clarify, classifier confidence) on OpenRouter models use the written-JSON path
  or `decideRouted`; Before the day step 6 already puts *Model for decisions* on the local entry,
  which keeps the judge on token probabilities.
- Claude Code through the gateway to an OpenRouter entry goes through `lib/gateway/translate.ts`
  (Anthropic Messages → Chat Completions), because `upstreamFor` gives OpenRouter only `chat`.
  CLAUDE.md records translation verified live against Qwen 9B on MLX Serve only.

---

## §1 Pinning and replaying kept answers (scenario 28; addition to 20)

**Code read.** `lib/llm/model-pinning.ts` (`enforcePinnedLeverage`, `checkPinnedWrite`,
`recordPinBypass`); `src/routes/llm.route.ts:172-186` (`pinRefusal`) and its callers at 250, 311,
435, 468 (409 `{ error }`); `src/routes/local-llm.route.ts:459` (engine activate); `docs/help/models.md`
→ *Pinned models*; `ui/src/pages/LocalLlmPage.svelte:1058` (the **pinned** badge). Replay:
`src/cli/commands/eval.ts:23-45,117-160` (`replayKept`), `lib/answers/regression.ts`
(`loadReplayCase`, `replayMessages`, `assessAnswer`, `replayCase`, `summarise`).

**Config.** `pinned: true` on the entry, set in `models.yaml` (there is no Studio switch; the IDE
tab is the documented way). Scenario 28 pins the default local entry, because the Models tab's
own controls then meet the pin: **Make default** on a cloud tab re-points `default` and is refused.
A named cloud entry could not be edited from the Models tab when this was written (§9, item 1);
it can now, so a refused *model change* can also be shown in the Studio: pin an entry, pick it on
its provider's tab, change the model, Save. Pin an entry that names its model: `loadModelsConfig` warns when a
pinned entry's model is the `mlx-serve` alias, because the engine can change what the alias
serves without any write AI Stackops sees. For a local pin, name the model:
`model: mlx-community/Qwen3.5-9B-MLX-4bit` on a `provider: local, engine: mlx-serve` entry.

**What refuses.** `PUT|DELETE /api/llm/config/models/:name` changing `model` without `pinned: false`
in the same body; re-pointing `default` off a pinned entry; `POST /api/local-llm/engines/activate`
onto a pinned slot; a UFP `remote-first`/`remote-only` run (downgraded to local, audited); a router
escalation off a pinned candidate; a video tool's per-call model override. Each writes
`models.pin.bypass` (outcome `denied`, reason `<attempt>: <detail>`; attempts `config-write`,
`engine-activate`, `ufp-remote-first`, `ufp-remote-only`, `router`, `request-override`,
`embedding-model-change`). The 409 text: `llm.<name> is pinned: model change <old> → <new>. Unpin
it first (pinned: false) to make this change.`

**Replay.** `ai-stackops eval --from-kept --model <entry> [--agent <name>] [--limit <n>] [--out <file>] [--json]`,
with `WORKSPACE` pointing at the host's workspace (default `~/.aistackops/workspace`). It reads
kept roots (`store.list({ frozen: true, roots: true })`), skips any answer with no MCP data step
(documents-only answers such as the finance analyst's are skipped: *no data step to replay*), any
whose results are no longer kept, and any whose agent is not loaded. `worse` = the grade fell or the
candidate gave a figure the results do not hold. Output per answer `SAME|BETTER|WORSE|FAIL <title>
(<agent>)  <grade> → <grade>  <s>`, then `not in the results: …` / `no longer given: …`, then
`<entry>: n replayed — b better, s the same, w worse, f failed; …`. Exit 1 on any worse or failed.
The judge is not run in replay (`assessAnswer`: "no judge").

**Model size.** The kept answers need the Full level (demo-data). The candidate can be any entry.

**Harness (local).**
0. `PUT /api/llm/config/models/default {"_pointer":"openrouter"}` while `default` resolves to a
   pinned `mlx-serve` → 409 *llm.mlx-serve is pinned: "default" currently resolves to it; re-pointing
   to "openrouter" would replace the pinned model. …* (what scenario 28 step 2 shows).
1. `PUT /api/llm/config/models/gemini-flash` with the entry and `pinned: true` → 200 (a write that
   pins is allowed). Then the same with `model` changed → expect 409 and the text above; `GET
   /api/admin/audit?action=models.pin.bypass&limit=5` → a row with reason starting `config-write:`.
2. The same PUT with `pinned: false` and the new model → 200 (the documented escape).
3. Replay: invoke `music-librarian` three times, `POST /api/answers/<runId>/keep {title}` each, then
   run the CLI as a subprocess with `--json --out r.json` and assert `summary.replayed == 3` and
   `skipped == []`. Use a local entry as `--model` to avoid spend; a stub OpenAI-compatible server on
   loopback (`provider: local`, `baseUrl: http://127.0.0.1:<port>/v1`, no `engine`) returning a
   fixed answer with a figure that is not in the results makes a deterministic `WORSE`.

**Cannot test locally.** The UFP no-failover path needs a second node (scenario 20's spoke).

**Watch for.** The CLI builds a whole `Orchestrator` on the live workspace
(`eval.ts:119-120`) while the server runs: MCP servers are spawned a second time and timers start.
Try it on a rehearsal before the day.

---

## §2 Charts (scenario 29)

**Code read.** `lib/answers/chart.ts` (`checkChartSpec`: top keys `mark|encoding|title|description|
width|height|config`, `FORBIDDEN_KEYS` at any depth incl. `data`, `url`, `transform`, `layer`,
`condition`, `filter`, `datum`; `datum.`/`javascript:` strings refused; 13 marks, 23 channels;
fields must be columns of the step; ≤ 8 KB spec, ≤ 5 000 rows); `lib/tools/built-in/chart.tool.ts`
(args `{ step: n | "S<n>", spec, title? }`, returns a ```` ```vega-lite {"chart":"C1"} ```` block);
`src/routes/answers.route.ts:305-319` (export draws each chart with `renderChartSvg`; audit
`answer.exported` metadata `charts: <n>`), `:328` (`GET /api/answers/:runId/charts/:chartId` →
`{spec, values, title, truncated}`, 410 when the rows expired); `lib/answers/export.ts:108-120`
(HTML `<figure><svg…><figcaption>`); `ui/src/lib/services/charts.ts` (placeholder while streaming,
drawn after `provenance`; *Data expired: keep the answer to preserve its charts.*);
`docs/help/chat.md` → *Charts*.

**Config.** None new: `agents/music-librarian.agent.yaml` already has `builtin:chart` and the
prompt paragraph telling it to chart a `[S…]` result without data; its sample questions include
"Chart the 10 longest tracks". The Sources line shows the named query and rows; the chart itself is
not listed on the line (it is in the reply and in `provenance.charts`).

**Model size.** Unmeasured. The spec is small, but the model must pass `S1` and column names it
read. Start on `gemini-flash`; add a bench check before claiming it on the 9B.

**Harness (local).** Invoke `music-librarian` with "Chart the 10 longest tracks"; assert
`provenance.charts` has one entry with `step` pointing at the `longest_tracks` step; `GET
/api/answers/<runId>/charts/C1` → 200 with 10 `values` and `spec.mark` present and no `data` key;
`POST /keep`; `GET /api/answers/<runId>/export?format=html` → body contains `<figure>` and `<svg`;
audit `answer.exported` row with `metadata.charts == 1`. A negative case needs no model: the unit
tests in `test/answers/chart-spec.test.ts` already refuse `data`/`transform`.

**Suggested bench check** (for `scripts/bench.py`, level `full`, scenario 29):
`c_chart`: invoke as dana, pass when `provenance.charts` is non-empty and the chart route returns
rows.

---

## §3 The SQL check (scenario 30)

**Code read.** `lib/answers/sql-lint.ts` (whole file: `lintSql` severe rules
`multiple-statements`, `write-statement`, `select-star-no-limit`, `join-without-condition`, note
`aggregate-over-join`; `lintResult` notes `no-rows`, `result-cut-short`, `mostly-empty-column`;
`withSqlLint` applies only when `tool.guard.tier === 'sql'`; `refuse` + severe → the tool is not
called and the model reads `lintRefusal`); `lib/mcp/tool-tiers.ts` (`tierFor` order: `tools.tiers`
patterns → profile rules → annotations → `looksLikeSql` → default); `lib/mcp/profiles/toolbox.ts`
(rule 1: a name ending `execute_sql` or an input property `sql|query|statement` → `sql`; every
other named query → `semantic`); `lib/mcp/types.ts:55-65` (`McpToolPolicySchema`, `sql.access`
default `{ minRole: builder }`); `lib/answers/grade.ts:65-76,106-137` (a severe finding on a step
that ran → Low with *A query read whole rows with no limit* etc.; `ad-hoc` label → Medium *Figures
come from SQL written for this answer, not a governed metric*); `lib/answers/recorder.ts:235`
(a tool output starting `Error` is a failed step, so a refused query does not count against the
grade); `ui/src/pages/admin/AnswerChecksTab.svelte:29-33,149` (labels); `AnswerSteps.svelte:169`
(the findings under a step).

**Why the demo cannot show it today.** Every tool on `demo-data` is a named query, so the Toolbox
profile tiers them all `semantic`, and `withSqlLint` passes them through untouched. The check has
nothing to read.

**The stand-in (honest, and small).** A second Toolbox server over a copy of the music database,
with one free-SQL tool, and an agent for builders. It uses only what the Toolbox profile already
tiers as `sql`, so no `tools.tiers` override is needed; the override is shown for clarity.

`data/toolbox/sql.yaml` (new bundle file):

```yaml
# Free SQL over a copy of the music store, for scenario 30. A copy, because in the default
# mode (warn) a statement the check flags as a write still runs.
sources:
  music-store-copy:
    kind: sqlite
    database: ../music-store/musicstore-analyst.sqlite
tools:
  run_sql:
    kind: sqlite-execute-sql        # confirm the kind name against Toolbox 1.13.1's docs
    source: music-store-copy
    description: Run one read-only SQL SELECT against the music store and return the rows.
```

`data/music-store/musicstore-analyst.sqlite`: a byte copy of `musicstore.sqlite`.

Second server in `mcp/demo-data.mcp.json` (the manifest takes one MCP file; it may hold several
servers):

```json
"demo-sql": {
  "description": "The music store through MCP Toolbox with one free-SQL tool, for builders.",
  "command": "npx",
  "args": ["-y", "@toolbox-sdk/server@1.13.1", "--stdio", "--config", "sql.yaml"],
  "cwd": "bundles/aiso-demo-pack/toolbox",
  "profile": "toolbox",
  "serviceAccount": { "name": "demo SQLite copy", "description": "A copy of the music store's SQLite file, opened by the Toolbox server." },
  "tools": { "tiers": { "run_sql": "sql" }, "sql": { "access": { "minRole": "builder" } } },
  "timeout": 120000,
  "callTimeout": 30000
}
```

A separate server, not a tool added to `demo-data`: `mcp:<server>` hands an agent every tool on the
server, and a free-SQL tool on `demo-data` would change the music librarian (scenario 22's
*Governed* label becomes *Ad hoc* or *Mixed* whenever the model picks SQL).

`agents/data-analyst.agent.yaml` (new, Full level):

```yaml
name: data-analyst
icon: fa-database
description: Answers questions about the music store by writing SQL (for builders)
version: "1.0.0"
access:
  minRole: builder
prompt:
  system: |
    You answer questions about a music store's sales database by writing one SQLite SELECT at a time
    and running it with run_sql. Tables: Customer(CustomerId, FirstName, LastName, Country),
    Invoice(InvoiceId, CustomerId, InvoiceDate, Total), InvoiceLine(InvoiceLineId, InvoiceId,
    TrackId, UnitPrice, Quantity), Track(TrackId, Name, AlbumId, GenreId, Milliseconds, UnitPrice),
    Album(AlbumId, Title, ArtistId), Artist(ArtistId, Name), Genre(GenreId, Name).
    Every figure you give must come from a result. If a query is refused, read why, fix it, and run it again.
  inputVariables: [query]
tools:
  - mcp:demo-sql
  - builtin:calculate
  - builtin:chart
sampleQuestions:
  - "Show me everything in the Track table."
  - "How much has each customer spent in total?"
```

Check the column list against `musicstore.sqlite` before shipping (I did not open the database).
Manifest (not edited): add the agent under `resources.agents`, the new bundle files ride in the
existing `data/toolbox` and `data/music-store` bundles, and add the agent to the `full` level's
`adds.agents`. The pack must be re-signed.

**Model size.** Standard-class at least; Full cloud entry for the demo.

**Harness (local).**
1. `GET /api/mcp/demo-sql/tools` → `run_sql` with `tier: "sql"`.
2. As priya (member): `GET /api/agents` → no `data-analyst` (agent access); separately, an agent
   that lists `mcp:demo-sql` for a member gets the tool withheld (`withholdTools`, reason names the
   builder rule).
3. `PUT /api/admin/answers/settings {"accuracy":{"sqlLint":"warn"}}`; invoke `data-analyst` as dana
   with "Show me everything in the Track table"; `GET /api/answers/<runId>` → a step with
   `lint[].rule == "select-star-no-limit"`, outcome success; `provenance.grade.level == "low"`.
4. `{"accuracy":{"sqlLint":"refuse"}}`; same question in a new session → the first `run_sql` step
   has outcome `failure` and the finding, a later step succeeds; label `ad-hoc`; grade not low
   unless the model gave up.
5. "How much has each customer spent in total?" → a step with `aggregate-over-join` (not severe),
   grade `medium` with the ad-hoc reason.
Steps 3–5 depend on what SQL the model writes; assert on the findings only when the statement has
the shape (`statementOf(args)` of the recorded step is readable from the tree).

**Cannot test locally.** The time-travel rewrite of a SQL step (it needs Snowflake or Databricks;
`timeTravel` refuses `toolbox`: *toolbox has no time travel AISO can use*). The Re-run itself works
on the stand-in and says so.

---

## §4 Per-person sign-in and time travel (scenario 34)

**Code read.** `lib/mcp/connections.ts` (`connectionFor`, `isPerPerson`), `lib/auth/mcp-oauth.ts`
(`McpOAuth`: discovery, DCR or `client`, PKCE, `complete`, `refresh`), `lib/mcp/session-pool.ts`
(one session per person and server, Bearer, 401 → one retry), `lib/tools/tool-guard.ts:33`
(withhold with *connect it under Account → Connections*), `src/routes/auth.route.ts`
(`GET /api/auth/connections`, `POST /:id/start`, `GET /callback`, `DELETE /:id`; audit
`identity.connect.start`, `identity.connect`), `ui/src/pages/AccountPage.svelte:66,564-653`
(*Connected services*, statuses *Connected / Through your sign-in / Reconnect needed / Consent needed
/ Not connected*, **Connect**, **Reconnect**, **Disconnect**), `AnswerSteps.svelte:74` (*as you*),
`lib/mcp/profiles/warehouses.ts` (Snowflake: identity `oauth` default, SQL-property tools → `sql`;
Databricks: identity `entra` default, DBSQL/`execute_sql` → `write`), `lib/answers/rerun.ts:95-127`,
`lib/answers/time-travel.ts` (Snowflake `AT(TIMESTAMP => '…'::TIMESTAMP_LTZ)`, Databricks `TIMESTAMP
AS OF '…'`; refuses CTEs, subqueries, set operations, comma joins, table functions, a clause already
present, non-SELECT), `docs/enterprise/mcp-connections.md`.

**Host config (Snowflake).** `mcp.json`:

```json
"snowflake": {
  "url": "https://<account>.snowflakecomputing.com/api/v2/databases/<DB>/schemas/<SCHEMA>/mcp-servers/<SERVER>",
  "profile": "snowflake",
  "identity": { "provider": "oauth", "scopes": ["session:role:ANALYST"] }
}
```

plus `AISO_PUBLIC_URL` (the OAuth callback is `<public url>/api/auth/connections/callback`; setup
health `mcp-oauth-callback` fails without it), and a Snowflake security integration for OAuth whose
redirect URI is that callback. If Snowflake refuses dynamic client registration, add
`"client": { "id": "…", "secret": "${secret:snowflake-oauth}" }` to `identity`. Agent:
`finance-analyst` gains `mcp:snowflake` (its `egress` refuses cloud models, so it stays local).

**Host config (Databricks).** The profile tiers Databricks SQL tools `write` (DBSQL can write), and
`rerun.ts:96` never re-runs a write step, and write tools are withheld unless `write.enabled`. To
re-run with time travel, serve a read-only warehouse and re-tier: `"tools": { "tiers": {
"execute_sql": "sql" } }`. Say so in the scenario; it is a real configuration choice, not a demo
trick.

**What a time-travel re-run needs.** The step's arguments hold SQL under `sql|query|statement|…`
(`sqlArgument`), the step's extractor is `snowflake` or `databricks`, and the statement is simple.
A semantic step (Cortex Analyst, Genie) is asked again without time travel, and the report says so.
The re-run writes `answer.rerun` and, when the answer had figures, a `rerun` outcome that shows in
*How the checks have done*.

**Model size.** Standard (the finance question is one tool call).

**Harness.** Needs the warehouse. A stand-in that exercises everything but the warehouse: the
product's `test/mcp/per-person.test.ts` (a real HTTP MCP server that checks bearer tokens) and
`test/auth/mcp-oauth.test.ts` (stub authorization server). For the demo pack, the local part that
can be tested is the Re-run report on the SQLite stand-in (§3), which must say *time travel not
applied*.

**Not tested, and not claimable yet:** the whole scenario. Written from code and docs.

---

## §5 The developer gateway: budgets, a second admin, background calls, pre-send (scenarios 31, 32; addition to 24)

**Code read.** `lib/projects/types.ts:9-145` (`ProjectConfigSchema`: `models[{id, displayName,
behavesAs, contextLength, route{entry,target}, byClass{main,subagent,auxiliary,compaction}}]`,
`budget`, `perPersonBudget`, `requestsPerMinute`, `onBudgetExhausted refuse|auxiliary-local`,
`frontierElsewhere`, `fallbackToFrontier`, `allowedCidrs`, `context`, `code`);
`lib/projects/project-policy.ts:109-175` (`weakeningReasons`, `relaxedCaps`, the reason strings);
`lib/projects/project-store.ts:21,160,210` (`DEFAULT_BUDGET_APPROVAL_USD` 1000; same-person 403);
`src/routes/projects.route.ts:97-98` (202 + `project.change.request`); audit actions
`project.create|update|archive|delete|change.request|change.approve|change.reject|artifact.issue`;
`lib/gateway/gateway-service.ts:80-84` (`requestClassOf(x-claude-code-request-class)`),
`:355-400` (rate, budget, `auxiliary-local` → `localStandIn`), `:402-417` (`gateway.downgraded`),
`:875-895` (ops `project.budget.80|100`); `lib/auth/budget-guard.ts:65-112` (project pool and
per-person scopes; an unpriced entry skips dollar caps); `lib/auth/limits.ts:210-220` (message
text); `ui/src/pages/ProjectsPage.svelte:305-360,380-420` (labels: *Changes waiting for a second
admin*, **Approve**/**Reject**, *Project, USD per day*, *Project, USD per 30 days*, *Each member,
USD per day*, *Each member, USD per 30 days*, *Requests per minute, each member*, *When the budget
runs out* → *Refuse paid calls* / *Move background calls to a local model*, **By kind**, *same as
the id*, **Save models**, the toast *This change weakens the project, so it waits for a second
admin. It is listed under Changes waiting.*).

**Project config for scenarios 31/32 (this round).** Created in scenario 24 step 1; the shape the
Studio writes:

```json
{
  "slug": "pump-controller", "name": "pump-controller", "repo": "alexborhani/meridian-pump-controller", "level": "internal",
  "config": {
    "models": [
      { "id": "claude-gemini-flash", "displayName": "Gemini Flash (cloud)", "behavesAs": "claude-haiku-4-5", "contextLength": 200000,
        "route": { "entry": "gemini-flash", "target": "hub" },
        "byClass": { "auxiliary": { "entry": "mlx-serve", "target": "hub" }, "compaction": { "entry": "mlx-serve", "target": "hub" } } },
      { "id": "claude-local-qwen", "displayName": "Qwen 3.5 9B (local)", "behavesAs": "claude-haiku-4-5", "contextLength": 32768,
        "route": { "entry": "mlx-serve", "target": "hub" } }
    ],
    "budget": { "usdPerDay": 0.03 },
    "perPersonBudget": {},
    "onBudgetExhausted": "auxiliary-local"
  }
}
```

(`byClass` is set in scenario 31 step 4, after the downgrade has been shown; with it set from the
start the background calls never touch the budget and nothing is downgraded.) `validateProject`
warns for ids under 64K context (`MAIN_LOOP_MIN_CONTEXT`); the local id at 32K will carry that
warning, which is true.

**Conditions the scenario depends on.**
- The stand-in is the first project model (≠ the refused id) whose route for that class is `hub`,
  non-frontier, speaking the tool's protocol (`localStandIn`). MLX Serve speaks `anthropic`.
- The stand-in entry must be **unpriced**: `BudgetGuard.check` runs again for the stand-in with the
  same project scopes, and only an entry without `pricing` skips dollar caps. Scenario 16's
  "without a cloud key" variant prices `mlx-serve`; its reset removes the pricing. A project
  `tokensPerDay` cap would also stop the stand-in.
- The pool alert (`project.budget.80|100`) reads the pooled budget only, not the per-member one.
- Only `auxiliary` and `compaction` are downgraded; `main` and `subagent` are refused.
- The second admin must hold `projects:write` and be a user (not a key). The pack seeds one admin
  (Dana); the host's first admin is the other.

**What files a change for a second admin** (`weakeningReasons`): level lowered; archived restored;
end date later or removed; a cloud route added; `frontierElsewhere` off; `fallbackToFrontier` on;
networks widened or removed; any cap removed (project or per-member: requests/min, tokens/day,
USD/day, USD/30 days); a 30-day cap raised above $1,000; `requestsPerMinute` removed; a knowledge
store or MCP server added to *Docs for agents*; code rules loosened. Not on the list: raising a
daily dollar cap, or a 30-day cap up to $1,000 (see §9).

**Harness (local, no model needed for the second-admin half).**
1. As dana: `POST /api/projects` with the JSON above (201). `PATCH /api/projects/pump-controller
   {"config":{"budget":{}}}` → 202 `{change:{id, reasons:["the project’s daily dollar cap removed"]}}`
   and an audit `project.change.request`. `GET /api/projects/pump-controller` → `budget.usdPerDay`
   still 0.03, `pendingChanges[0].id` = the change.
2. As dana: `POST /api/projects/changes/<id>/approve` → 403 `project_change_same_person`.
3. As the first admin: same → 200; project budget now `{}`; audit `project.change.approve`.
4. Tightening: `PATCH … {"config":{"budget":{"usdPerDay":0.03}}}` → 200 applied.
5. Budget and downgrade without spending money or calling the engine: add a `provider: local` entry
   with no `engine` and `baseUrl: http://127.0.0.1:<stub>/v1` (a stub that answers Anthropic
   Messages with a usage block, like `test/gateway/stub-upstream.ts`), give it `pricing: {
   inputPerMillion: 1000, outputPerMillion: 1000 }`, route the project's "cloud" id to it and a
   second id to an unpriced stub entry. `POST /api/dev/keys {"name":"harness"}` (Studio session) →
   `token`. Then `POST /gateway/anthropic/v1/messages` with `Authorization: Bearer <token>`,
   `x-aiso-project: pump-controller`, `x-claude-code-request-class: auxiliary` until the pool is
   spent; the next one answers with header `x-aiso-downgraded: <id> -> <local id> (budget spent)`
   and an audit `gateway.downgraded`; a `main` call → 429 with `code` `gateway_budget` and the
   *Local models do not count against it* sentence. Note the budget test is about pricing, not
   frontier-ness: a priced local stub stands in for the cloud entry.

**Cannot test locally.** Claude Code's own behaviour on a 429 with `Retry-After: 3600`
(`BUDGET_RETRY_AFTER`), and whether this Claude Code build sends `x-claude-code-request-class` on
its title and compaction calls (the gateway relies on it; P0 recorded 2.1.283's traffic).

### §5c The pre-send check (scenario 32)

**Code read.** `lib/packs/hooks.ts` (`gateway.before_call` in `DECIDE_EVENTS` and
`DECIDE_ONLY_EVENTS`), `PackHookBus.decideAll`, `GatewayService.screen`,
`docs/enterprise/pack-events.md:212-242` (payload), `ui/src/pages/admin/PacksPolicyTab.svelte:49,98`
(the confirmation text and the decide toggle), `test/gateway/gateway-presend.test.ts` (the
secret-scanning test pack, in the test only).

**What exists.** The event, the gateway call site, the Studio toggle, setup health `presend-check`,
the kill switch `PACK_DECIDE=false`, and a test pack inside the test file. **What does not:** any
installable pack with a `gateway.before_call` hook. The demo pack carries no hook by decision
(CLAUDE.md, pack extensions slice 1). `handling[level].preSend` has no Studio control: the
handling-rules table on Policy → Classification edits `requireAccess`, `minTier`, `localOnly`,
`retentionDays` only (`ClassificationTab.svelte:15,343-346`); a `preSend` set in
`classification.yaml` is kept by a Studio save (the editor spreads the existing rule), but cannot be
seen or changed there.

**If the demo pack is to ship one** (a manifest change, a new function and a re-sign; certified
tier is required for any decide hook — `pack_decide_tier`):

```js
// functions/presend-secrets.function.mjs
const PATTERNS = [
  [/\bAKIA[0-9A-Z]{16}\b/, 'an AWS access key id'],
  [/-----BEGIN [A-Z ]*PRIVATE KEY-----/, 'a private key'],
  [/\bghp_[A-Za-z0-9]{36}\b/, 'a GitHub token'],
  [/\bsk-[A-Za-z0-9_-]{20,}\b/, 'an API secret key'],
];
export default {
  name: 'presend-secrets',
  description: 'Refuses a developer call to a cloud model that carries a credential (a hook core calls; not a tool for agents).',
  parameters: { newText: { type: 'array', description: 'Text not checked before in this conversation', required: false } },
  execute: async ({ newText }) => {
    const text = (Array.isArray(newText) ? newText : []).join('\n');
    for (const [re, what] of PATTERNS) if (re.test(text)) return JSON.stringify({ decision: 'deny', reason: `the call carries ${what}; remove it and send again` });
    return JSON.stringify({ decision: 'allow' });
  },
};
```

Manifest additions: `resources.functions` += `functions/presend-secrets.function.mjs`; top-level
`"hooks": [{ "event": "gateway.before_call", "function": "presend-secrets", "mode": "decide" }]`;
add the function to the `full` level's `adds.functions`. Timeout: the decide timeout is 500 ms
(`DECIDE_TIMEOUT_MS`). The payload's field is `newText` (array of strings); confirm that a hook
function receives the payload's top-level fields as its arguments, as `request-hygiene` does in
`test/fixtures/packs/seed-pack`.

**Harness (local, no model).** With the pack installed and the hook switched on (`PUT
/api/packs/aiso-demo-pack/decide {"event":"gateway.before_call","function":"presend-secrets",
"enabled":true}`), a gateway call to a frontier-routed project id with `AKIAIOSFODNN7EXAMPLE` in a
user message → 403 `gateway_presend_denied`, and `gateway.refused` metadata `{pack, version,
hook}`. The screen runs only for a **frontier** upstream: a local stub will never reach the hook,
so this check needs a real cloud entry (the call is refused before it leaves, so it costs nothing;
the clean control call does cost).

---

## §6 The bill and chargeback (scenario 33; addition to 18)

**Code read.** `lib/llm/usage-reconcile.ts` (Anthropic `/v1/organizations/usage_report/messages`,
OpenAI `/v1/organization/usage/completions`; tolerance 5 % or 2 000 tokens; a day settles at 06:00
UTC next day; ≤ 7 days catch-up), `lib/orchestrator.ts:2301-2332` (targets: entries with
`usageReport`, Anthropic or OpenAI only), routes `GET|POST /api/admin/usage/reconcile` (audit
`usage.reconcile.run`, per-target `usage.reconcile`, ops `provider.usage.mismatch`),
`ui/src/pages/UsagePage.svelte:85,159-165` (*Checked against the provider's bill*, *matches /
billed more than metered / metered more than billed*, **Compare yesterday now**, table *By
development project*, button **Export 30 days (CSV)**), `src/routes/admin.route.ts:1264-1279`
(`/api/admin/usage/export.csv`, edition-gated `chargeback`, columns `month, person, personId,
agent, modelEntry, provider, model, node, kind, project, calls, inputTokens, outputTokens, units,
costUsd`; audit `usage.export`).

**Host config for the bill check.** On an Anthropic or OpenAI entry (not OpenRouter, not Azure):

```yaml
  claude:
    provider: anthropic
    model: claude-haiku-4-5-20251001
    apiKey: ${secret:anthropic-api-key}
    usageReport:
      apiKey: ${secret:anthropic-admin-key}   # the organisation's admin key, never the call key
      apiKeyId: apikey_01…                    # the call key's id, so other apps on the account are not counted
```

**Harness.** Chargeback (local): `GET /api/admin/usage/export.csv` as dana → header row contains
`project`; after a gateway call for `pump-controller`, a row with that project. Needs the
Enterprise licence (else the edition refusal). Bill check: needs a real admin key; the product
covers the parsing with `test/llm/usage-reconcile.test.ts` against a stub of both report shapes.
`POST /api/admin/usage/reconcile {"day":"YYYY-MM-DD"}` returns per-target results.

**Cannot test locally.** The comparison against a real bill (admin keys; OpenRouter entries are
out of scope for it).

---

## §7 The operator lock, Azure, packs from anyone, Microsoft 365 (additions to 15; scenarios 35, 36)

**Operator lock.** `lib/llm/egress-policy.ts:45` (`EGRESS_ALLOW_FRONTIER=false` → every policy
`allowFrontier: false`, reason *EGRESS_ALLOW_FRONTIER=false locks this host to local models*),
`lib/llm/model-gate.ts` (applies even with no agent: `opts.egress ?? resolveEgressPolicy()`),
`GET /api/llm/config` → `_frontierHardLocked`, `LocalLlmPage.svelte:1114-1123` (*Frontier providers*
**locked by operator**, *Cloud models are off for everyone on this node.*). The gateway runs
`gateModelUse` too, so Claude Code's cloud ids are refused under the lock. Harness: start a
throwaway server with the variable set; `GET /api/llm/config` → `_frontierHardLocked: true`;
invoke an agent on a cloud entry → error; audit `egress.denied`. Needs a restart, so it is a
separate run from the rest.

**Azure.** `CLAUDE.md` → *Azure*; `lib/llm/azure.ts`, `azure-auth.ts`; Models → **Azure** labels:
*Resource endpoint*, *API* (*Azure OpenAI* / *Claude on Foundry*), *Sign in with* (*API key* /
*Managed identity (Microsoft Entra)*), *Managed identity client ID (optional)*, *Chat deployment*,
*Embedding deployment*, *Data zone*. YAML:

```yaml
  azure-gpt:
    provider: azure
    baseUrl: https://<resource>.openai.azure.com
    deployment: <deployment name>
    model: gpt-5.1
    api: openai
    auth: key                 # or entra (managed identity; azureClientId for a user-assigned one)
    apiKey: ${AZURE_OPENAI_API_KEY}
    dataZone: eu
    access: { minRole: admin }
```

Needs an Azure subscription; nothing local.

**Packs from anyone (scenario 35).** `lib/packs/pack-source.ts` (any `https://`, `ssh://`,
`git://`, `git@` URL is shallow-cloned; a directory is resolved against the workspace),
`lib/packs/pack-trust.ts` (`verifyPack`: unsigned or unknown key → `community`),
`pack-seed.ts:69` (`pack_seed_tier`), `assertCapabilitiesAllowed` (`pack_capability_tier`),
`assertDecideAllowed` (`pack_decide_tier`), `lib/packs/pack-worker*.ts` (community hooks run in a
child with `--permission`, fs-read limited to the worker entry, network globals deleted, imports
refused, 30 s run timeout, 60 s idle stop), `PacksPolicyTab.svelte:86` (**runs isolated**),
`PUT /api/packs/trust {minTier}` (409 `pack_trust_env_override` while `PACKS_MIN_TIER` is set).
**Caveat to say out loud:** only hooks run isolated. A community pack's functions used as agent
**tools** still load in-process through the FunctionLoader (CLAUDE.md, pack worker slice).

The unsigned pack to build (a repo of its own, e.g. `aiso-demo-community-pack`): `manifest.json`
with `id`, `name`, `version`, `publisher: "Riverside volunteers"`, `tier: "community"`, no
`signature`, `resources.functions: ["request-hygiene.function.mjs"]`, `hooks: [{ "event":
"access.requested", "function": "request-hygiene", "mode": "annotate" }]` (copy the product's
`test/fixtures/packs/seed-pack/request-hygiene.function.mjs`, dropping its `ctx.data` write unless
the manifest declares `data`). No `seed`, no `capabilities`, no decide hooks: each of those would be
refused at install for a community pack, which can be shown by `POST /api/packs/inspect` on a
variant that adds one. Harness: `POST /api/packs/inspect {source}` → `verification.status ==
"unsigned"`, tier `community`; install → 201; `PUT /api/packs/trust {"minTier":"pack"}` then inspect
again → `installBlocked.code == "pack_tier_denied"`.

**Microsoft 365 (scenario 36).** `~/Dev/aso-o365/pack/manifest.json` (2.0.3, certified, signed;
config `MS365_MCP_CLIENT_ID`, `MS365_MCP_TENANT_ID`, `UNIFIEDSEARCH_DIR`, `LOCAL_DIRS` (user
scope) …; `userSetup` *Connect your Microsoft account* (device code); `identity` Entra with
read-only Graph scopes on `unifiedsearch`; egress `sanctioned-saas` to `login.microsoftonline.com`
and `graph.microsoft.com`), `o365-assistant.agent.yaml` (read-only; `unified_search` first),
`SETUP.md` (Entra app registration, admin consent, public client flows on). Needs a tenant.
The pack also ships a `dlp-guard` function; I did not read it, so the scenario does not claim it.

---

## §8 Federation additions (scenario 20)

**No failover on a pinned entry.** `enforcePinnedLeverage` downgrades `remote-first` to local and
audits `models.pin.bypass` with `ufp-remote-first` (silently for `local-first`). The hub's *Pin
entries* field (Admin → Estate, `EstateTab.svelte:372`) pushes pins as a floor. The agent control:
Agents → an agent → *Use models on other nodes*: *Node default / Off / Local-first / Remote-first
/ Remote-only* (`AgentComposer.svelte`). Local test: needs the spoke from scenario 20.

**Answers across nodes.** `lib/ufp/answer-proof.ts` (Ed25519 over the claims with the node key),
the Network tab's chat with a remote agent (`UFPPage.svelte`, `api.streamUFPAgent`),
`AnswerSteps.svelte:133-135` (*Answered on <node>, which keeps the record of what it ran*). I did
not trace whether the Network tab's reply renders the Sources line the way the Agents tab does;
check on the day before scripting step 5b.

---

## §9 Things that look like product bugs or gaps (not fixed)

1. **The Models tab edits one entry per provider, whatever it is called, and saves it under the
   provider's name.** The OpenRouter (Anthropic, Gemini …) tab loads the default entry if it is that
   provider's, else the first entry whose provider matches (`ui/src/pages/LocalLlmPage.svelte:434-443`,
   `cloudModelEntry`), but **Save** writes `PUT /api/llm/config/models/<provider>`
   (`LocalLlmPage.svelte:842`) and **Make default** points `default` at `<provider>`
   (`:418-423`). Editing a named entry such as `claude-haiku` or `gemini-flash` there creates or
   overwrites an entry called `openrouter` and leaves the named one as it was; its budget, pricing
   or pin is not the one changed, and a pin on the named entry is not consulted. There is no name
   field, so DEMOS.md's *Before the day* step 5 ("Models tab → OpenRouter …, name `claude-haiku`")
   produces an entry named `openrouter`, and scenario 16's "Models tab → `claude-haiku` → USD / day"
   edits that one. The drafts create named entries in the IDE tab for this reason.
   *Since fixed in the product working tree (read 2026-09-29):* each provider's tab lists its
   entries by name above the form, with **New entry** and a **Name** field (`LocalLlmPage.svelte`
   ~1295–1316, `docs/help/models.md` → *Entry names*); **Save** writes under that name and **Make
   default** points at it. DEMOS.md now uses the Models tab.
2. **A pinned model can be changed from the IDE tab without refusal or audit.** The pin guard runs
   only in `src/routes/llm.route.ts:172-186` (Models tab API) and `local-llm.route.ts:459`. The
   IDE's file write (`src/routes/files.route.ts:32-44`, `refusedWrite`) checks only the permission
   for a policy file; a `models.yaml` edit that changes a pinned entry's `model` and keeps
   `pinned: true` is saved and reloaded with no `models.pin.bypass` row. The help
   (`docs/help/models.md` → *Pinned models*) says a save naming another model is refused.
   *Since fixed:* `src/routes/files.route.ts` now runs `checkPinnedFileWrite` on a `models.yaml`
   edit. Only an explicit `pinned: false` in the same edit lets the model change, so an edit that
   drops the `pinned` line and changes the model is refused (scenario 28's reset says so).
3. *Fixed 2026-09-29 (product 89ada89): replay skips cases above the candidate's ceiling, localOnly levels on cloud candidates, and what the original egress refuses.* **Model replay ignores the agent's and the store's egress and the candidate's classification
   ceiling.** `src/cli/commands/eval.ts:131` creates the candidate with `LLMFactory.create(model,
   { agent: 'model-replay' })` under `SYSTEM_PRINCIPAL`; `lib/answers/regression.ts:56-76` loads
   every kept answer with a data step. A kept answer from an agent with `egress.allowFrontier:
   false`, or built on results above the candidate's `maxClassification`, is sent to a cloud
   candidate. (The operator lock still applies: `gateModelUse` defaults to the workspace policy.)
4. *Fixed 2026-09-29 (89ada89): any raised cap, and a 30-day dollar exposure above the approval line, needs a second admin.* **Raising a project's daily dollar cap needs no second admin.** `relaxedCaps`
   (`lib/projects/project-policy.ts:111-120`) flags a cap removed, or a 30-day cap raised above
   $1,000; `usdPerDay` raised from $1 to $900, or `tokensPerDay` raised to any number, applies at
   once. Possibly intended; the Why AISO line "a second admin" reads wider than this.
5. *Fixed 2026-09-29 (89ada89): a writing statement is a write-tier call in every mode.* **In the default SQL-check mode, a statement flagged as a write still runs.** `withSqlLint`
   (`lib/answers/sql-lint.ts:153-178`) refuses severe findings only in `refuse` mode; in `warn`
   (the default) `write-statement` is noted and executed. The design leans on the data source's
   account being read-only; consider refusing `write-statement` in every mode.
6. *Not a bug: under auxiliary-local no paid call goes through either; wording left as is.* **The budget alert says paid calls are refused when the project downgrades instead.**
   `gateway-service.ts:889`: *…paid model calls are refused until it frees up* is written for
   `onBudgetExhausted: auxiliary-local` too, where background calls move to a local model.
7. *Fixed 2026-09-29 (89ada89).* **Two names for one page.** Tool and error messages say *Account → Connections*
   (`lib/tools/tool-guard.ts:33`, `lib/mcp/mcp-client.ts:220,524`, `lib/mcp/session-pool.ts:158`,
   `lib/orchestrator.ts:1515`); the Account page's section is *Connected services*
   (`AccountPage.svelte:567`).
8. **DEMOS.md label drift** (not product bugs): scenario 18 *Export CSV* is **Export 30 days
   (CSV)**; scenario 16 *By model entry* is the table **Model entries**. Fixed in DEMOS.md.
9. **No Studio control for `preSend`** (see §5c). A level can require a pre-send check only by
   editing `classification.yaml`.
