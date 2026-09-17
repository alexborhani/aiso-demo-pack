---
type: scenario
title: "18. On the record"
tags: ["scenario-18"]
---
*The audit trail, the usage ledger, chargeback and a signed evidence bundle: the paperwork a
security review or an auditor asks for, produced by the platform.*

**You are** Dana. Best after a few of the earlier scenarios have run.

1. Admin → Audit. Filter by action: `knowledge.access.denied`, `classification.monitor`,
   `tools.approval.granted`, `models.route`. Every row has the actor, the target, the outcome, the
   reason and a request id that matches the engine call. Say: the log is hash-chained; a removed or
   altered row breaks the chain, and the chain is verified.
2. Usage tab: calls, tokens and cost by person, by agent, by model entry, by kind, by day. Click a
   person to drill. *Export CSV*: one row per month, person, agent and model, ready for chargeback.
3. Admin → Data → *Evidence bundle*: choose the last 30 days, download. One JSON file, signed with the
   workspace key, containing the setup checklist, the compliance report, the taxonomy version, the
   packs, the limits, the usage totals and the audit rows. Open it and show the signature block.
4. Admin → Estate → *Estate report*: nodes and active people, signed the same way.

**Land:** nothing here was assembled by hand for the meeting. The evidence a control framework asks
for is a download, and it is tamper-evident.

---
