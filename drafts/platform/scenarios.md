# Platform scenarios: drafts for DEMOS.md

**Merged into DEMOS.md on 2026-09-29** as scenarios 28–36 (25–33 in the first draft; renumbered here too),
with the additions applied to 15, 18, 20, 22 and 24. What changed on the way in: the Models tab now
names entries (**Name**, a list of each provider's entries, **New entry**), so DEMOS.md creates and
edits named entries there instead of in the IDE tab; `gemini-flash` became the existing `claude-haiku`
entry and `claude-gemini-flash` became `claude-haiku-4-5`; `deepseek-flash` is a second entry in
*Before the day* for scenario 28; scenario 20's additions use the spoke's own `chatbot` (a fresh spoke
has no `simple-toolbox`); scenario 35 says that only hooks run isolated. DEMOS.md is the text to
edit from now on; this file is kept for its reasoning.

New scenarios 28–36 and additions to scenarios 15, 18, 20, 22 and 24, written in the style of
DEMOS.md. Nothing here has been run yet. Each block says its level and, where it cannot run on the
demo Mac alone, **Needs:** the system it needs. NOTES.md has the code paths, the exact config and
a test harness for each; coverage.md maps the Why AISO headings to scenarios.

**The cloud entries for this round.** DEMOS.md names one cloud entry, `claude-haiku`. This round
uses two OpenRouter entries instead, written into `models.yaml` from the IDE tab (NOTES.md §0).
They have to be: the Models tab has one tab per provider, no name field, and saves what its
OpenRouter tab shows under the key `openrouter` (NOTES.md §9, item 1), so it cannot make two
OpenRouter entries or name one.

| Entry | Model on OpenRouter | Stands in for | Used by |
| --- | --- | --- | --- |
| `deepseek-flash` | `deepseek/deepseek-v4.1-flash` | a Standard-class (27B) local model | Standard agents on a 9B Mac |
| `gemini-flash` | `google/gemini-3.7-flash` | a Full-class (70B) local model or a frontier provider | `music-librarian`, the workshop agents, scenario 24's project |

Both: key `${OPENROUTER_API_KEY}`, access minimum role **member**, classification ceiling
**internal**, Max Tokens 2048, pricing from each model's OpenRouter page on the day (type the
figures; do not copy them from here), USD / day **1**. Where DEMOS.md says `claude-haiku`, read the
entry the level names. Change their budgets in the IDE tab too, not on the Models tab.

---

## 28. The model stays put until you move it
**Level:** Full (the kept answers come from the music librarian, which needs the demo-data server).
Needs the `ai-stackops` command on the Mac (as for scenario 24) and both cloud entries.


*A model that changes under an organisation changes its answers. Here the model is pinned, a
change is refused, and the switch is tested on the answers people kept before anyone makes it.*

**You are** Dana. **Windows:** the Studio and a terminal. Best after scenario 22 part two, whose
kept answer is reused here.

1. IDE tab → `models.yaml` → the `mlx-serve` entry under `llm`: replace `model: mlx-serve` with the
   model's own name, `mlx-community/Qwen3.5-9B-MLX-4bit`, and add `pinned: true`. Save. Models tab →
   MLX Serve: the chat entry carries a lock and **pinned**. Say: this is the model every agent
   without a model of its own answers with, and from now on nothing moves it by accident. (The name
   matters: the `mlx-serve` alias follows whatever the engine serves, which no pin can hold.)
2. Models tab → the OpenRouter tab → **Make default**. Refused: *llm.mlx-serve is pinned: "default"
   currently resolves to it; re-pointing to "openrouter" would replace the pinned model. Unpin it
   first (pinned: false) to make this change.* Admin → Audit, action `models.pin.bypass`: one row,
   outcome denied, reason *config-write: …*, Dana as the actor. Say: the same refusal meets a
   federation setting that would send the work to another node, and a router that would escalate.
3. As Dana, `music-librarian`: ask three questions and **Keep** each answer with a title (the
   reply's Sources line → **Keep** → title → **Keep and sign**):
   **"Find the 5 longest tracks in the catalog"** (title *Longest tracks*),
   **"Which artists have tracks in both Rock and Jazz?"** (*Rock and Jazz*),
   **"What has customer Heather Leacock purchased, and how much did she spend in total?"** (skip
   if scenario 22 already kept it). Account → *Kept answers* lists them.
4. In the terminal, with the host's workspace, ask whether the librarian could move from
   `gemini-flash` to the cheaper `deepseek-flash`:
   `WORKSPACE=<the host's workspace> ai-stackops eval --from-kept --model deepseek-flash --agent music-librarian`
   Each kept answer is given to `deepseek-flash` with the librarian's instructions, the question
   and the results it was built from (no query runs again), and checked and graded like a live
   answer. One line per answer: `SAME`, `BETTER` or `WORSE`, its title, the grade before and
   after, and under a worse one the figure the candidate gave that the results do not hold
   (*not in the results: …*) or a figure the kept answer gave and the candidate dropped (*no
   longer given: …*). The last line counts them.
5. Read out the answers that came back worse, by title. Say: this is the release test for a model
   change. It exits non-zero when anything got worse, so it can gate a change the same way the
   evals in scenario 17 do. Run it again with `--model mlx-serve`: the same question of the pinned
   local model. This is how you find out which work can move to open weights, before moving it.
6. To make a switch for real: point the librarian at the model that passed (Agents →
   `music-librarian` → Model), or, for the default, set `pinned: false` and the new model in one
   edit of `models.yaml`. Neither happens by itself.

**Land:** the model under an agent changes only when an admin changes it, and the change is tested
against the answers people kept before it is made, with the ones that got worse named.

*Reset:* IDE tab → `models.yaml` → the `mlx-serve` entry back to `model: mlx-serve`, without
`pinned`. Kept answers stay.

---

## 29. A chart drawn from the query result
**Level:** Full (the demo-data server). Measured on neither model yet: `builtin:chart` needs the
model to name the result and write a small Vega-Lite spec; start on `gemini-flash`.


*A chart the model cannot fake: it names which result to draw and how, and the platform draws it
from the rows the query returned.*

**You are** Dana; Jordan in the second window for the last step.

1. `music-librarian` (on `gemini-flash`): **"Chart the 10 longest tracks."** The librarian calls
   `longest_tracks` with 10, then `chart` naming that result, and the reply ends with a bar
   chart: one bar per track, its length in seconds. The chart appears once the reply is finished.
2. Open the tool trace: the `chart` call's arguments are a step number (`S1`) and a mark and
   encoding over the result's columns (`track`, `seconds`), and nothing else. Say: there is no
   field for data. The model cannot pass numbers to the chart; a spec that tries (`data`, `url`,
   `transform`, an expression) is refused before anything is drawn.
3. The Sources line under it: *Governed*, the named query `longest_tracks`, 10 rows, *Figures found
   in sources*, the grade. Open it: the step's statement and **Show result** — the ten rows the
   bars are drawn from.
4. **Keep** it (*Longest tracks, charted*). **Export** → HTML: open the file. The chart is in it,
   drawn as a picture from the kept rows, under the answer, with the statement and the checks. It
   loads nothing from the internet. Admin → Audit, `answer.exported`: `charts: 1`.
5. Say what happens later: the rows behind an unkept chart are kept for seven days, after which
   the chart reads *Data expired: keep the answer to preserve its charts.* A kept answer keeps them.

**Land:** a chart in a reply is a view of a recorded result, not a picture the model made, and it
travels with the signed answer.

---

## 30. SQL read before it runs
**Level:** Full, plus the `demo-sql` server and `data-analyst` agent this draft proposes (NOTES.md
§3; not in the pack yet). Standard-class model or better: writing SQL over an unfamiliar schema is
beyond what a 9B does reliably. Start on `gemini-flash`.


*Named queries are governed; free SQL is not. Here free SQL is offered only to builders, read
before it runs, refused when it is plainly wrong, and graded lower than a governed answer.*

**You are** Dana; Priya in the second window.

1. Tools → MCP: two servers over the same database. `demo-data`: every tool chipped **Governed**.
   `demo-sql`: one tool, `run_sql`, chipped **SQL · builders**. Say: the question is not whether a
   model can write SQL but who may ask it to, and what reads it first.
2. As Priya, `data-analyst` is not in her list (the agent is for builders). Open the agent's
   definition as Dana: `access: minRole: builder`, and even without that the SQL tool itself is
   withheld below builder. Members get named queries; builders get SQL.
3. As Dana, Admin → Policy → **Answer checks** → *When a query has a known mistake*: it is on
   **Run it and note the problem** (the default). `data-analyst`: **"Show me everything in the
   Track table."** A model asked that writes `SELECT * FROM Track` with no limit. It runs; under the
   reply, open the step: the statement, and under it a warning *SELECT * from Track with no LIMIT
   returns every row and column…*. The grade is **Low**, and its reasons name the query.
4. Switch it to **Refuse it**. Save. Ask the same question in a new chat. The query is refused
   before it runs, the model reads why (*this query was refused by the SQL check before it ran …
   Fix the query and run it again*), rewrites it with named columns and a LIMIT, and the second
   statement runs. Open the steps: the refused one, with the finding, marked failed; the one that
   ran, clean.
5. **"How much has each customer spent in total?"** The model joins invoices to invoice lines and
   sums. That is allowed, and the step carries a note: *The query sums or counts across a join …*.
   The Sources line says **Ad hoc**, not Governed, and the grade is **Medium** at best: *Figures
   come from SQL written for this answer, not a governed metric.* Compare scenario 22's Heather
   Leacock answer from a named query: Governed, High.
6. Set *When a query has a known mistake* back to **Run it and note the problem**.

**Land:** free SQL is a builder's tool, read before it runs; the plainly wrong shapes are sent back
to be fixed, and an answer built on SQL written on the spot says so in its label and its grade.

---

## 31. A project's budget, its background calls, and a second admin
**Level:** Full. Needs what scenario 24 needs (Claude Code, `ai-stackops`, the clone, the project
`pump-controller` from scenario 24 step 1), and the host's first admin account (the one made at
install) as the second admin.


*A development project has its own money: a pool, a share per person, and a rule for what happens
when it runs out. Loosening any of that takes a second admin.*

**You are** Dana and the first admin in the Studio (two browser profiles), Sam in the terminal.

1. As Dana, **Projects** → `pump-controller` → **Overview** → *Budget*: *Project, USD per day*
   **0.03**, *When the budget runs out*: **Move background calls to a local model**. Save.
   Tightening applies at once. Point at *Each member, USD per day*: the same cap per person inside
   the pool (left empty here, so the pool is what runs out). (The stand-in is the project's local id,
   `claude-local-qwen`; the `mlx-serve` entry must carry no pricing, or it spends the same budget.)
2. As Sam, in the clone: `claude`, `/model claude-gemini-flash`, and ask for a few small changes
   until the spend passes three cents. From then on Claude Code's background calls (conversation
   titles, summaries, compaction) are moved to the local model instead of failing, and his next
   main call is refused: *Limit reached: $0.03 per day for project pump-controller (used
   $0.03). It frees up as the rolling 24 hours pass; an admin can raise it in the project's budget.
   Local models do not count against it: switch to claude-local-qwen.* `/model claude-local-qwen`
   and carry on. Nothing about the project stopped.
3. As Dana, Admin → Audit: `gateway.downgraded` (from the cloud id to `claude-local-qwen`, request
   class *auxiliary* or *compaction*, the budget as the reason; one row per person every five
   minutes, repeats counted) and `gateway.refused` for the main call. Admin → Setup → *Since your
   last visit*: *Project pump-controller has spent 8x % of its daily budget*, then *… has spent its
   daily budget ($0.03 of $0.03)* (the project's name as created in scenario 24).
4. Make it permanent for background work: **Models** → `claude-gemini-flash` → **By kind** →
   *auxiliary*: `mlx-serve`, *compaction*: `mlx-serve` → Save models. Now background calls run
   locally whatever the budget; only the work itself goes to the cloud model. **Usage** → *By:
   Kind of request* shows the split after a few turns.
5. Now loosen it. **Overview** → clear *Project, USD per day* (no daily cap). Save. The toast: *This
   change weakens the project, so it waits for a second admin. It is listed under Changes waiting.*
   The project still has its cap. The box *Changes waiting for a second admin* lists it with the
   reason, in words: *the project's daily dollar cap removed*. Dana's own **Approve** is refused:
   *A change that weakens a project needs a second admin: someone other than the person who asked
   must decide it.*
6. As the first admin, **Projects** → `pump-controller`: the same change, asked by Dana. **Approve**:
   *Approved and applied.* Admin → Audit: `project.change.request` by Dana, `project.change.approve`
   by the first admin. Say what else waits for a second admin: a lower level, a cloud route added, a
   30-day cap above $1,000, a restored project, a later end date, wider networks, more docs for the
   agents, looser code rules.

**Land:** a project spends what it was given, its background work falls back to the local model
instead of stopping, and nobody loosens its rules alone.

*Reset:* restore the daily caps (tightening applies at once), *When the budget runs out* back to
*Refuse paid calls*, the *By kind* routes back to *same as the id*.

---

## 32. A check before code leaves
**Level:** Full, as scenario 24. **Needs:** a certified pack that carries a `gateway.before_call`
decide hook. The demo pack carries no hook (by decision; see NOTES.md §5c for the one it could
ship). The product's own test pack for this lives only in its test suite.


*A pack the organisation trusts reads what a coding tool is about to send to a cloud model, and
can stop it.*

**You are** Dana in the Studio, Sam in the terminal.

1. As Dana, Admin → Policy → **Packs**: the pack's `presend-secrets` hook on `gateway.before_call`,
   mode decide, **off: not consulted**. Switch it on. The confirmation says what it reads: *the new
   text of every developer call to a cloud model (prompts and code) and may stop it.* Switch on.
2. As Sam, in the clone, on the cloud id: **"Why does this fail? AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
   is set in the build."** Refused before it leaves, with the pack's reason: a cloud call carrying
   what looks like a cloud access key. Nothing reached the provider.
3. The same question without the key goes through. Admin → Audit: `gateway.refused` names the pack,
   its version and the hook, never the text; the `gateway.call` row of the call that went out
   carries *allowed by* the hook.
4. Say what a stricter organisation does (shown, not run: the Studio's handling-rules table has
   no column for it yet): IDE tab → `classification.yaml` → `handling: internal: preSend: required`.
   Calls at that level then leave only when a pack said yes; with no hook switched on, every cloud
   call at that level is refused, and Admin → Setup fails the *pre-send check* line.
   `PACK_DECIDE=false` on the host stops every pack deciding.

**Land:** what leaves for a cloud model can be read first by a pack the organisation certified,
and stopped, with the refusal on the record and the text nowhere in it.

---

## 33. The bill, checked; the cost, charged back
**Level:** Essentials for the chargeback; the bill check **Needs:** an Anthropic or OpenAI
organisation admin key (OpenRouter and Azure publish no usage report the check reads).
The chargeback needs the Enterprise licence (Before the day, step 2).


*What the platform metered, compared with what the provider billed, and the spend split by
project for the people who pay it.*

**You are** Dana. Best after scenarios 16, 24 and 31 have run, so there is usage to split.

1. Usage tab → *By development project*: `pump-controller` and *(no project)*. Click the project:
   calls, tokens and cost for the Claude Code work alone.
2. **Export 30 days (CSV)**. Open it: one row per month, person, agent, model entry, node and
   **project**, with calls, tokens and cost. Filter `project = pump-controller`: the engineering
   chargeback. Admin → Audit: `usage.export`.
3. *Needs an Anthropic or OpenAI admin key.* Usage tab → *Checked against the provider's bill*: for
   each cloud entry with a `usageReport` block (NOTES.md §6), yesterday's metered tokens beside the
   provider's own report for the same key, and a verdict: *matches*, *billed more than metered* or
   *metered more than billed*. **Compare yesterday now** runs it at once. Admin → Audit:
   `usage.reconcile`, per provider and key, never the admin key.
4. Say what *billed more than metered* means: calls reached the provider with this organisation's
   key without passing through AI Stackops. The key has been copied somewhere. Rotate it.

**Land:** the ledger is checked against the provider's own bill daily, and the same ledger splits
the cost by project for chargeback.

---

## 34. Data read as the person asking
**Level:** Standard. **Needs:** a Snowflake account with a managed MCP server (or Databricks, see
the note), an OAuth integration for AI Stackops, and two Snowflake users with different roles.
Written from the code; not run.


*The warehouse, not AI Stackops, decides what each person may see: the query runs under the
person's own sign-in. And a kept answer can be re-run against the data as it stood when it was
given.*

**You are** Lena and Marcus (two windows), then Lena again.

1. As Dana, Tools → MCP: the `snowflake` server, profile *Snowflake*, sign-in **per person**
   (config in NOTES.md §4). Agents → `finance-analyst` gains `mcp:snowflake`.
2. As Lena, Account → **Connected services**: *Snowflake* — **Not connected** → **Connect**. The
   Snowflake sign-in opens; she signs in as her Snowflake user. Back in the Studio: **Connected**.
   Marcus does the same with his.
3. As Lena, `finance-analyst`: **"What was Q2 2026 revenue by region?"** The answer comes from the
   warehouse. Open the Sources line: the statement Snowflake ran, its query id, the rows, and
   **as you**. Snowflake's query history shows the query under Lena's user and role.
4. As Marcus (whose Snowflake role cannot read the revenue table), the same question: the
   warehouse refuses it, and the reply says so. AI Stackops granted nothing; the warehouse decided.
5. As Lena, **Keep** the answer. A day later (or after changing a row in the table), **Re-run**
   against *data as it was*: the report says, per step, *identical*, and *time travel applied: read
   as of <the answer's time>*. Against *current data*: *changed*, with the row counts before and
   after, and which of the answer's figures are no longer found.
6. As Lena, Account → Connected services → **Disconnect**: the warehouse tool is withheld from her
   next question, with the reason *it acts as you through your Snowflake account, which you haven't
   connected — connect it under Account → Connections* (the page's heading is *Connected services*).

*Databricks instead:* the same steps with a Databricks SQL MCP server. Its SQL tool is chipped
**Writes** by the profile (Databricks SQL can write), and a write tool is never re-run, so re-tier
it as `sql` in `mcp.json` on a read-only warehouse (NOTES.md §4) before step 5.

**Land:** the data stays in the warehouse and answers the person, as that person; a kept answer can
be asked again of the data as it was, and says whether it still holds.

---

## 35. A pack from anyone, held apart
**Level:** Essentials. **Needs:** a small unsigned pack in a git repository of its own (not built;
NOTES.md §7 lists what it holds).


*Capability can come from any git repository, not only from signed publishers. What the platform
lets an unknown publisher's pack do is the point.*

**You are** Dana.

1. Packs → *Install* → the unsigned pack's git URL → *Inspect*. The card: **community**, unsigned,
   publisher unknown. Say: anyone can publish a pack; nobody vouched for this one.
2. Install it. Admin → Policy → **Packs**: its hook is listed with **runs isolated**: its code runs
   in a separate process with no network, no files and no modules, and is stopped after 30 seconds.
3. What it may not do, and the install dialog would refuse if it tried: seed accounts or roles,
   read the audit log or usage, or decide anything in a person's place (decisions are for certified
   packs only).
4. Packs → *Trusted publishers* → minimum tier **pack** → Save. Inspect it again: *Install* is off,
   and the reason says the host no longer accepts community packs. Set it back to **community**.
5. Uninstall it. Admin → Audit: `packs.install` (its metadata: tier *community*, verification
   *unsigned*), `packs.trust` twice, `packs.uninstall`.

**Land:** packs install from any git repository; one whose publisher nobody trusts runs its code
held apart and can reach no people, no records and no decisions, and an admin can refuse unsigned
packs estate-wide in one setting.

---

## 36. Microsoft 365, searched as you
**Level:** Standard. **Needs:** a Microsoft 365 tenant, an Entra app registration with admin
consent (the `aso-o365` pack's SETUP.md), and the `aso-o365` pack. Written from the pack; not run.


*Mail, calendar, files and Teams searched by a local model, as the signed-in person, read-only.*

**You are** Dana to install, then Priya.

1. As Dana, Packs → *Install* → `https://github.com/alexborhani/aso-o365`: signed by AI Stack Ops,
   certified. The dialog asks for the tenant's client and tenant ids and the local folders. Its
   declared egress: `login.microsoftonline.com`, `graph.microsoft.com`, nothing else.
2. As Priya, Packs → the pack → *Your setup* → **Connect your Microsoft account**: a device code,
   signed in once with her Microsoft account. Admin → Audit: `identity.connect`.
3. `o365-assistant`: **"What did Marcus send me about the Riverside open day?"** One search across
   her mail, files and calendar, answered with each item's title and link, on the local model. It
   is her mailbox, read with her delegated token; nobody else's mail is reachable.
4. **"Reply to him and say yes."** It says it is read-only and offers a draft for her to send.

**Land:** a Copilot-style search over Microsoft 365 that runs on the organisation's own model, as
the person asking, and cannot send or change anything.

---

## Correction to *Before the day*, step 5, and scenario 16

The Models tab has no *name* field: its OpenRouter tab saves the entry as `openrouter`, whatever
DEMOS.md calls it, and edits that entry even when a differently named OpenRouter entry exists
(NOTES.md §9, item 1). Either call the entry `openrouter` throughout (scenario 16: Models tab →
OpenRouter → USD / day), or write the named entries in `models.yaml` from the IDE tab, as this
round does, and change their budgets there.

---

## Additions to scenario 15 (Cloud by policy)

**Step 6, done live instead of mentioned** (optional; needs a restart of the host, so do it last).
Quit AI Stackops and start it again with `EGRESS_ALLOW_FRONTIER=false` in its environment (the
deploy kit's service environment, or `EGRESS_ALLOW_FRONTIER=false ai-stackops start`). Models tab:
*Frontier providers* **locked by operator** — *Cloud models are off for everyone on this node.* As
Dana, `board-analyst` (on `claude`/`gemini-flash`): refused before anything is dialled, for the
admin too. Admin → Audit: `egress.denied`, reason *EGRESS_ALLOW_FRONTIER=false locks this host to
local models*. No Studio setting turns it back on; restart without it.

**Step 1b, Azure** — **Needs:** an Azure subscription with an Azure OpenAI or Foundry resource and a
deployment. Models tab → **Azure**: *Resource endpoint* (`https://<resource>.openai.azure.com`),
*API* **Azure OpenAI** (or **Claude on Foundry**), *Sign in with* **API key** or **Managed identity
(Microsoft Entra)**, *Chat deployment*, *Data zone* (EU, US or global: recorded, so the evidence
bundle says where the model ran). Access, ceiling, budget and pricing as for any cloud entry. Say:
the model runs in the organisation's own tenant under its own agreement; with managed identity
there is no key to leak. The steps that follow read the same with the Azure entry.

---

## Additions to scenario 18 (On the record)

- Step 3 label: the button is **Export 30 days (CSV)** (DEMOS says *Export CSV*), and the file has
  a **project** column: a Claude Code project's spend is its own line in the chargeback.
  Scenario 33 walks it.
- DEMOS scenario 16 step 2 says *By model entry*; the Usage table is titled **Model entries**.

---

## Additions to scenario 20 (Two nodes, one policy)

**After step 4: a pinned model does not fail over.** On the spoke, Agents → `simple-toolbox` →
*Use models on other nodes* **Remote-first**. Save. Ask it **"What is 1234 * 5678?"**: answered on
the spoke's own model, because the hub pinned the chat entry (step 2's floor). Admin → Audit on the
spoke: `models.pin.bypass`, reason *ufp-remote-first: …*. Say: a pinned model is never swapped for
another node's, even when an agent asks. Set it back to *Node default*.

**After step 5, optional: an answer from another node.** On the hub, **Network** → the spoke →
`simple-toolbox` (it is shared: `ufp: share: true`) → ask **"What is 1234 * 5678?"**. Under the
reply, the Sources line names the step *on riverside-laptop*; open it: *Answered on
riverside-laptop, which keeps the record of what it ran*, the spoke's run id, and *signature
verified*. Not yet run on the demo; see NOTES.md §8.

---

## Additions to scenario 22 (Numbers you can check)

**Step 6b, re-run** (after Keep / Verify / Export). Under the kept answer, **Re-run** against **data
as it was** → the report: *Re-run against the data as it was: 1 same, 0 changed, … not re-run, 0
failed*, and on the `customer_purchases` line *time travel not applied: the question is asked
again, and the source may answer from newer data* (a calculation is never re-run; it counts as not
re-run). Say: the demo store is SQLite, which cannot read the past; against Snowflake or Databricks
the statement is rewritten to read the table as of the answer's time (scenario 34). Against
**current data**: the same, and the line under it says how many of the answer's figures are still
found. Admin → Audit: `answer.rerun`.

**Step 4b, figures filled in.** Open the grade on the Heather Leacock answer. When the model used
references to the result (it is told to, while *Fill in figures from the results* is on), one of the
reasons reads *N figures were filled in from the results*: the model wrote a reference to a column
and row, and the platform put the number in. Not every answer uses them; a total the model worked
out with `calculate` is checked instead (*worked out from them*). Check on the day which reason
appears before saying it.

**Step 4c, the second model.** With *Model for decisions* on the local entry (Before the day, step
6), the judge is on: a High grade's reasons include *A second model found it answers the
question*. Where it doubts, the grade is Low and the reason names what it doubted.

---

## Additions to scenario 24 (Coding agents inside the policy), for this round

- Step 1: the cloud model id must contain `claude` for Claude Code's picker to keep it. Use
  `claude-gemini-flash` routed to `gemini-flash`, *Claude Code picker behaves as*
  `claude-haiku-4-5` (Models → **By kind**). The gateway translates Claude Code's Anthropic calls
  for OpenRouter's Chat Completions API; that path was verified live with a local model only.
- Step 7's attestation line then reads *from cloud models: 2 — claude-gemini-flash*.
- Scenarios 31 and 32 continue from this project.
