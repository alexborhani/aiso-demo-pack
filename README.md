# AI Stackops demo pack — Meridian Works

A pack that turns a vanilla AI Stackops install into a fictional company, **Meridian Works**, so the whole platform can be evaluated as different people. Nothing in it is real: the people, documents, figures and matters are invented.

**Presenting to leaders?** [DEMOS.md](DEMOS.md) has thirty-seven scripted scenarios (0–36), a 60-minute tour and the reset list. Scenarios 25–33 were measured in this release (DEMOS.md → *Levels*); 34–36 need a system the demo Mac does not have (a warehouse, an unsigned pack's repository, a Microsoft 365 tenant) and were not run.

## What it installs

- **Six accounts** with generated passwords, shown once at install (Packs → *Reset passwords* mints new ones):

  | Person | Tier | Role → clearance | Sees |
  | --- | --- | --- | --- |
  | Dana Okafor, IT director | admin | — | every level and category by clearance, the Admin pages — but not the HR or Finance stores, which require those roles even of an admin |
  | Sam Reyes, automation engineer | builder | firmware-engineers → confidential · Security | builds agents and skills; internal stores; the firmware repository's safety code |
  | Priya Nair, operations coordinator | member | staff → internal | the helpdesk, the handbook and the IT runbooks |
  | Marcus Bell, HR partner | member | staff + hr-partners → confidential · HR | people files, the people-partner agent |
  | Lena Fischer, finance analyst | member | staff + finance-analysts → confidential · Finance | finance close, the finance-analyst agent |
  | Jordan Lee, contractor | member | contractors → public only | the handbook; every other store is refused, visibly |

- **A classification policy** (`policy.md`, `classification.yaml`): four levels, four categories, handling rules. Adopted on install, restored on uninstall.
- **Knowledge stores** at every level: `handbook` (public), `it-runbooks` (internal), `people-files` (confidential · HR), `finance-close` (confidential · Finance), `legal-matters` and `security-incidents` (restricted), `scratchpad` (write-back target), plus the former samples (`music-store`, `pet-store`, `org-chart`, `patient-records`, `transcripts`, `web-docs`).
- **Agents** scoped to them: `helpdesk` (everyone), `people-partner`, `finance-analyst`, `counsel`, `security-lead` (with the approval-gated `revoke_access` action), `writer` (canvas + knowledge write-back), `meridian-ceo`, plus the former sample agents. The restricted agents and stores name their **owners** (Marcus for HR, Lena for finance, Dana for legal and security): Chat sends a request for access to them.
- **Workflows**: an evaluator loop (`customer-notice`), a parallel research-and-merge (`incident-brief`), and the former examples.
- **An organisation**, Meridian Works, with an agent CEO, members and eight tickets.
- **A data source** (full level): `demo-data`, MCP Toolbox for Databases over the music-store and pet-store SQLite files, with five named queries in `data/toolbox/tools.yaml` and no free SQL. The music librarian answers purchases and track lengths from it, so its replies carry a Sources line with the statement that ran. It needs Node's `npx` on the server's path; the first call downloads the pinned `@toolbox-sdk/server@1.13.1`.
- **Skills**: `house-style`; `customer-notice`, a playbook (inputs, a filing that waits for an admin's sign-off, a done list, a reference file, its own evals) the writer follows; `safety-change-review` for coding agents on the firmware project; and the workshop skills.
- **Firmware docs** (full level): `firmware-docs`, the service API guide, the commissioning runbook and the controller overview, served to coding agents through a development project. The code itself is in [meridian-pump-controller](https://github.com/alexborhani/meridian-pump-controller).
- **Routing objectives** per role and agent, **budgets** on two roles, a **tool-approval** entry, an **eval** file for the helpdesk, and functions.

## Levels

The pack installs at one of three levels — pick the one your default chat model carries on the install dialog, and change it later from the pack card (raising installs more; lowering removes the agents and stores above the level and keeps the people and the policy):

| Level | For | Adds |
| --- | --- | --- |
| Essentials | a 9B-class local model, 16K+ context (measured on Qwen 3.5 9B) | the eight Meridian agents (one to three tools each), the nine stores the scripts use, the people, roles and policy; Chat (21), checked answers (22) and files that carry Purview labels (25) |
| Standard | a 27B-class local model at 32K, or a cloud entry for the agents this level adds (measured on DeepSeek V4.1 Flash) | the presenter, the writer with its playbook, canvas, the agent CEO and its organisation, the workflows, the evals, the demo scripts |
| Full | a 70B-class model or a frontier provider (measured on Gemini 3.7 Flash) | the sample workshop agents and stores, the `demo-data` MCP server and its column-tag catalog (26), the firmware docs and the safety review skill |

[DEMOS.md](DEMOS.md) says which level each scenario needs. `scripts/bench.py` checks a level against the model on a host (see *Benchmarking a level*).

## Install

Packs tab → Install → source `https://github.com/alexborhani/aiso-demo-pack`, and choose a level. The pack is signed by AI Stack Ops (certified tier); seeding accounts requires that signature. Install is refused while SCIM provisioning is on or when a classification policy is already adopted.

Then sign out and back in as each person to see what changes. The Setup checklist notes the demo accounts until the pack is uninstalled.

## Classification demo: off → monitor → enforce

The pack ships with the classification policy adopted but **enforcement off**, so the same questions can be asked three times and the answers compared. The stores for it are `all-hands` — eight notices in one public store, each labelled in its own frontmatter — two public, two internal, two confidential (one HR, one Finance) and two restricted (Security, Legal). The `announcements` agent reads it and everyone may use it. Jordan, the contractor, clears public only. The `site-notes` store, unlabelled, is for step 4.

1. **Off.** As **Dana**, open Admin → Policy → Classification: the Enforcement panel shows *Off* in red, the Setup checklist warns, and *Check now* under Compliance lists it as the first finding. Sign in as **Jordan** and ask the announcements agent its sample questions. Every answer comes back: the town hall, the Riverside restructuring memo with the severance terms, the Q3 figures, the plant USB incident, the regulator inquiry. Nothing is recorded.
2. **Monitor.** As Dana, set *Monitor*. As Jordan, ask the same questions: the answers are the same. Back as Dana, refresh the panel — it now counts the reads the policy would have refused — and open Admin → Audit filtered by action `classification.monitor`: one row per search naming Jordan, the store, the levels involved and why each would have been refused. Nothing was withheld yet.
3. **Enforce.** As Dana, set *Enforce*. As Jordan, ask again: only the town hall and the open day come back; the memo, the results, the incident and the inquiry are "not announced". As **Marcus** (HR partner, confidential within HR) the restructuring memo is readable but the Q3 figures are not; as **Lena** (finance analyst) it is the reverse; as Dana everything is.

4. **Classify what nobody labelled.** The `site-notes` store is a shared folder as staff wrote it: six notes, none labelled, all reading at the store default (internal). As Dana, open it on the Knowledge page: the *Sources* panel shows every note with *store default* as the decider. Classify one in place — the injury note as confidential HR, say — and watch it apply and land in the audit log; try lowering one and see it go to the review queue instead. Then set a local classifier model under Admin → Policy → Classification (the chat model will do), come back and press *Send undecided to the classifier*: the notes go pending, and one by one the classifier decides them from the policy's criteria — the Nordvik visit confidential Finance, the badge follow-up restricted Security, the parking note public. Anything it is unsure about waits in the review queue.

The switch changes only the clearance and model-ceiling checks. The role-locked stores (people files, finance close, legal, security) stay locked in every mode, because their access blocks are RBAC, not classification.

## Benchmarking a level

`scripts/bench.py` runs every scripted call of a level against the model a host serves, as the pack's people, through the product's own API, and passes a check when enough runs pass:

```
python3 scripts/bench.py --url http://127.0.0.1:3333 --admin <admin>:<password> --level essentials \
                         [--install <pack dir or git url>] [--runs 10] [--gate 9] [--only id,id] [--json out.json]
```

Measured for 1.13.0 on 2026-09-29/30 on a 24 GB Mac. Essentials: 10 runs per check, a check passing at 9 of 10.

| Level | Model | Result |
| --- | --- | --- |
| Essentials | Qwen 3.5 9B (4-bit) on MLX Serve, 32K context | 18 of 18 checks, each 10 of 10: the runbooks, the refused and the allowed handoff, classification under enforcement, the legal store refused, memory, Chat's refusal, handoff and request, counsel, finance, a documents answer graded with its figures found, marking an answer, the revoke waiting for Dana's approval (7), the classifier filing the Nordvik note (5), a request granted by the agent's owner. Every Essentials scenario also ran end to end three times in a row with every step passing (end-to-end harness, not shipped). |
| Standard | DeepSeek V4.1 Flash (OpenRouter) for the writer, canvas, CEO and helpdesk | scenarios 0, 9, 10, 11, 12, 15, 17 and 27 end to end; 23 up to its eval gate (the evals ran on the 9B default) |
| Full | Gemini 3.7 Flash (OpenRouter) for the librarian, the data analyst and Claude Code | scenarios 20, 24, 28, 30, 31 and 33 end to end; 22 part two, 26 and 29 all but one step each (see DEMOS.md) |

The presenter (scenario 0) stays on the local model and passed on the 9B. The Standard and Full rows are end-to-end runs, not bench runs: the bench's Standard and Full checks were not re-run for 1.13.0. On a 24 GB Mac some calls to the 9B stalled for two minutes when the machine was swapping; see *Before the day* in DEMOS.md.

## Uninstall

Removes everything it created: the accounts and everything they did, the roles and key, the organisation, the stores and their indexed data, the files, the fragments, and restores the previous taxonomy. Audit rows stay.

## Evaluation walk-through

1. As **Jordan** (contractor): ask the helpdesk about leave; then try the people-partner agent — it is not listed, and a knowledge search of `people-files` is refused with `knowledge_access_denied`.
2. Run the classification demo below, then as **Marcus**: ask the people-partner for the senior engineer band. As **Lena**: ask the finance-analyst for Q2 revenue.
3. As **Dana**: ask the security-lead to revoke the contractor from INC-2026-021 — an approval card appears; approve it under Approvals.
4. As **Dana**: Admin → Policy → Classification shows the adopted policy and a compliance check; Admin → Usage shows each person's calls.
5. Run the `customer-notice` workflow, open Organisations → Meridian Works, and `ai-stackops eval helpdesk`.
