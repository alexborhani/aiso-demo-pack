# AI Stackops demo pack — Meridian Works

A pack that turns a vanilla AI Stackops install into a fictional company, **Meridian Works**, so the whole platform can be evaluated as different people. Nothing in it is real: the people, documents, figures and matters are invented.

**Presenting to leaders?** [DEMOS.md](DEMOS.md) has twenty scripted scenarios, a 60-minute tour and the reset list.

## What it installs

- **Six accounts** with generated passwords, shown once at install (Packs → *Reset passwords* mints new ones):

  | Person | Tier | Role → clearance | Sees |
  | --- | --- | --- | --- |
  | Dana Okafor, IT director | admin | — | every level and category by clearance, the Admin pages — but not the HR or Finance stores, which require those roles even of an admin |
  | Sam Reyes, automation engineer | builder | — | builds agents; internal stores |
  | Priya Nair, operations coordinator | member | staff → internal | the helpdesk, the handbook and the IT runbooks |
  | Marcus Bell, HR partner | member | staff + hr-partners → confidential · HR | people files, the people-partner agent |
  | Lena Fischer, finance analyst | member | staff + finance-analysts → confidential · Finance | finance close, the finance-analyst agent |
  | Jordan Lee, contractor | member | contractors → public only | the handbook; every other store is refused, visibly |

- **A classification policy** (`policy.md`, `classification.yaml`): four levels, four categories, handling rules. Adopted on install, restored on uninstall.
- **Knowledge stores** at every level: `handbook` (public), `it-runbooks` (internal), `people-files` (confidential · HR), `finance-close` (confidential · Finance), `legal-matters` and `security-incidents` (restricted), `scratchpad` (write-back target), plus the former samples (`music-store`, `pet-store`, `org-chart`, `patient-records`, `transcripts`, `web-docs`).
- **Agents** scoped to them: `helpdesk` (everyone), `people-partner`, `finance-analyst`, `counsel`, `security-lead` (with the approval-gated `revoke_access` action), `writer` (canvas + knowledge write-back), `meridian-ceo`, plus the former sample agents.
- **Workflows**: an evaluator loop (`customer-notice`), a parallel research-and-merge (`incident-brief`), and the former examples.
- **An organisation**, Meridian Works, with an agent CEO, members and eight tickets.
- **A data source** (full level): `demo-data`, MCP Toolbox for Databases over the music-store and pet-store SQLite files, with five named queries in `data/toolbox/tools.yaml` and no free SQL. The music librarian answers purchases and track lengths from it, so its replies carry a Sources line with the statement that ran. It needs Node's `npx` on the server's path; the first call downloads the pinned `@toolbox-sdk/server@1.13.1`.
- **Routing objectives** per role and agent, **budgets** on two roles, a **tool-approval** entry, an **eval** file for the helpdesk, a **skill** (house style) and functions.

## Levels

The pack installs at one of three levels — pick the one your default chat model carries on the install dialog, and change it later from the pack card (raising installs more; lowering removes the agents and stores above the level and keeps the people and the policy):

| Level | For | Adds |
| --- | --- | --- |
| Essentials | a 9B-class local model, 16K+ context | the eight Meridian agents (one to three tools each), the nine stores the scripts use, the people, roles and policy; the Chat scenario (21) |
| Standard | a 27B-class local model at 32K, or a cloud entry | the presenter, the writer and canvas, the agent CEO and its organisation, the workflows, the evals, the demo scripts |
| Full | a 70B-class model or a frontier provider | the sample workshop agents and the sample stores, and the `demo-data` MCP server |

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

## Uninstall

Removes everything it created: the accounts and everything they did, the roles and key, the organisation, the stores and their indexed data, the files, the fragments, and restores the previous taxonomy. Audit rows stay.

## Evaluation walk-through

1. As **Jordan** (contractor): ask the helpdesk about leave; then try the people-partner agent — it is not listed, and a knowledge search of `people-files` is refused with `knowledge_access_denied`.
2. Run the classification demo below, then as **Marcus**: ask the people-partner for the senior engineer band. As **Lena**: ask the finance-analyst for Q2 revenue.
3. As **Dana**: ask the security-lead to revoke the contractor from INC-2026-021 — an approval card appears; approve it under Approvals.
4. As **Dana**: Admin → Policy → Classification shows the adopted policy and a compliance check; Admin → Usage shows each person's calls.
5. Run the `customer-notice` workflow, open Organisations → Meridian Works, and `ai-stackops eval helpdesk`.
