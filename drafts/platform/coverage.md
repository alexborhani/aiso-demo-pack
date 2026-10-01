# Why AISO, heading by heading: which demo shows it

Scenarios 0–36 are in DEMOS.md. 25–27 came from `drafts/classification/scenarios.md`; 28–36 and
the additions to 15, 18, 20, 22 and 24 came from `drafts/platform/scenarios.md` (its 25–33, renumbered)
and were merged on 2026-09-29. None of 25–36 or the additions has been run yet. Status:

- **covered-local**: runs on the demo Mac with the pack (and, where named, the cloud entry or
  Claude Code). Drafts marked *draft* have not been run yet.
- **needs-system**: written, but needs a system the Mac does not have; not claimed as tested.
- **not covered**: no scenario, with the reason.

| Why AISO heading | Scenarios | Status |
| --- | --- | --- |
| Your models don't change until you do | 28 (pin, refused change, replay of kept answers on a candidate); 20 step 5 (a pinned entry does not fail over) | covered-local (draft; 28 needs Full and the `ai-stackops` command; 20 step 5 needs the spoke) |
| Open-weight models cut risk and bill | 1–8 on the local 9B; 15 step 7 (router: local first, cloud only when it does not fit); 16 without a key; 28 step 5 (replay on `mlx-serve`); 31 (background calls on the local model) | covered-local |
| Sensitive data reaches only models cleared for it | 8 (counsel local-only); 15 (ceiling *internal*, `allowFrontier: false`); 24 step 6 (classified code refused for the cloud model) | covered-local |
| Every figure checked before anyone reads it | 22 (parts one and two) | covered-local |
| Data stays in its source, read as the person asking | 22 part two (data read through MCP, never copied in); 34 (per-person sign-in, *as you*) | covered-local for "stays in its source"; needs-system (Snowflake or Databricks) for "as the person asking" |
| Developers keep their coding tools | 24 (Claude Code; the login also sets up Codex and OpenCode, not shown) | covered-local (needs Claude Code) |
| Skills written once with approvals | 9, 23 | covered-local (Standard) |
| Automation has no meter | 5 (classifier on the local model), 10–11 (workflows), 12 (an agent on a schedule, on the 9B), 16 without a key (priced, not billed) | covered-local, with a caveat: on a 9B Mac the Standard workflows run on the cloud entry, so the "no meter" point holds for them only on a Standard-class local model. |
| One rulebook and self-proving audit log | 1, 4, 18 (**Verify chain**, signed evidence bundle) | covered-local |
| A proven setup spreads as one pack | 1 (signed pack, update, auto), 20 (hub floors), 35 (any git repo, unknown publisher held apart) | covered-local for 1 and 20; 35 needs-system (a small unsigned pack repo, not built) |
| A policy drafted with you | 1 step 3 (*Extract criteria*); 27 (the onboarding agent) | covered-local (draft; 27 needs the onboarding agent added, which the pack does not ship) |
| Classified on your own machines | 5 (the classifier on the local model); 26 step 7 (columns) | covered-local |
| A person approves anything lowered | 5 step 3 (lowering goes to *Reviews*) | covered-local |
| Watch before you enforce | 4 (Monitor, then Enforce) | covered-local |
| Handling rules checked | 1 step 4, 8 step 5 (*Compliance*) | covered-local |
| Purview labels read from files | 25 | covered-local (draft; labels written into the files, no tenant) |
| Withheld column by column | 26 steps 3–5 | covered-local (draft; Full) |
| Where tags and policy disagree | 26 steps 6 and 8 | covered-local (draft; the catalog is a stand-in for BigQuery policy tags) |
| Columns nobody tagged | 26 step 7 | covered-local (draft) |
| Data read as the person asking | 34 | needs-system (Snowflake; Databricks variant noted) |
| Metric definitions before SQL | 22 part two (named queries, *Governed*); 30 (free SQL only for builders, labelled *Ad hoc*, graded lower) | covered-local with a stand-in: Toolbox named queries stand in for a semantic layer (dbt, Cortex Analyst, Power BI); a real semantic layer is needs-system. 30 needs the proposed `demo-sql` server (draft). |
| Sources under every reply | 22 | covered-local |
| Figures traced not trusted | 22 (*Figures found in sources*, step 8's miss) | covered-local |
| Charts from the query result | 29 | covered-local (draft; Full; model fit unmeasured) |
| Keep, verify, re-run | 22 steps 6 and 7 (re-run on SQLite: time travel reported as not applied); 34 step 5 (time travel) | covered-local for keep, verify, export, re-run; needs-system (Snowflake or Databricks) for reading the data as it was |
| Checked before it is shown | 22 step 4 (*Checking the answer against the results…*) | covered-local |
| Figures filled in from the result | 22 step 3 (the setting); 22 step 4 (the grade reason) | covered-local, conditional: the reason appears only when the model used result references; check on the day |
| A second model reads the answer | 22 step 3 (the setting); 22 step 4 (the grade reason) | covered-local; a judge catching a wrong answer is not scripted (not reproducible on demand) |
| A grade, and SQL read before it runs | 22 (grade); 30 (SQL check, warn and refuse) | covered-local (30 is a draft needing the proposed `demo-sql` server) |
| Marked by the people who asked | 22 step 2; calibration panel *How the checks have done* | covered-local |
| One gateway for every tool | 24 | covered-local (Claude Code only; Codex and OpenCode not shown) |
| Projects, budgets and a second admin | 24 (project); 31 (pool budget, downgrade, a weakening change approved by a second admin); 33 (chargeback by project) | covered-local (draft; needs Claude Code and the host's first admin) |
| Local models where they fit | 15 step 7 (router by context fit); 24 (`claude-local-qwen`); 31 (background calls routed and downgraded to local) | covered-local |
| Context the checkout doesn't have | 24 steps 3–5 (docs, code map, owners, skill) | covered-local |
| Classified code stays put | 24 step 6 | covered-local |
| Which lines a model wrote | 24 step 7 (`code attest`), step 8 (*AI provenance*) | covered-local |
| A check before code leaves | 24 step 6 (classified code refused before it leaves); 32 (pack pre-send check) | covered-local for 24; 32 needs-system: a certified pack with a `gateway.before_call` decide hook (none exists outside the product's tests; `drafts/platform/NOTES.md` §5c drafts one) |
| Microsoft 365 search (aso-o365 pack) | 36 | needs-system (Microsoft 365 tenant, Entra app with admin consent) |

**Also covered, beyond the headings:** usage checked against the provider's bill (33 step 3;
needs-system: an Anthropic or OpenAI admin key, so not with OpenRouter entries); the operator switch
forbidding cloud models, done live (15 step 8; needs a restart); Azure entries (15 step 1, *With
Azure*; needs Azure); answers across nodes (20 step 7; not yet run).
