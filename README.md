# AI Stackops demo pack — Meridian Works

A pack that turns a vanilla AI Stackops install into a fictional company, **Meridian Works**, so the whole platform can be evaluated as different people. Nothing in it is real: the people, documents, figures and matters are invented.

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
- **Routing objectives** per role and agent, **budgets** on two roles, a **tool-approval** entry, an **eval** file for the helpdesk, a **skill** (house style) and functions.

## Install

Packs tab → Install → source `https://github.com/alexborhani/aiso-demo-pack`. The pack is signed by AI Stack Ops (certified tier); seeding accounts requires that signature. Install is refused while SCIM provisioning is on or when a classification policy is already adopted.

Then sign out and back in as each person to see what changes. The Setup checklist notes the demo accounts until the pack is uninstalled.

## Uninstall

Removes everything it created: the accounts and everything they did, the roles and key, the organisation, the stores and their indexed data, the files, the fragments, and restores the previous taxonomy. Audit rows stay.

## Evaluation walk-through

1. As **Jordan** (contractor): ask the helpdesk about leave; then try the people-partner agent — it is not listed, and a knowledge search of `people-files` is refused with `knowledge_access_denied`.
2. As **Marcus**: ask the people-partner for the senior engineer band. As **Lena**: ask the finance-analyst for Q2 revenue.
3. As **Dana**: ask the security-lead to revoke the contractor from INC-2026-021 — an approval card appears; approve it under Approvals.
4. As **Dana**: Admin → Policy → Classification shows the adopted policy and a compliance check; Admin → Usage shows each person's calls.
5. Run the `customer-notice` workflow, open Organisations → Meridian Works, and `ai-stackops eval helpdesk`.
