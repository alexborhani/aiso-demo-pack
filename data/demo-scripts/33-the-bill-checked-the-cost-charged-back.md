---
type: scenario
title: "33. The bill, checked; the cost, charged back"
tags: ["scenario-33"]
level: full
---
**Level:** Full, with Claude Code: the project's spend comes from scenarios 24 and 31. The
chargeback export itself works at any level with the Enterprise licence (*Before the day*, step 2).
The bill check **Needs:** an Anthropic or OpenAI organisation admin key (OpenRouter and Azure
publish no usage report the check reads); not tested. The rest (usage by project, the chargeback CSV) passed in the measured run.


*What the platform metered, compared with what the provider billed, and the spend split by
project for the people who pay it.*

**You are** Dana. Best after scenarios 16, 24 and 31 have run, so there is usage to split.

1. Usage tab → *By development project*: `pump-controller` and *(no project)*. Click the project:
   calls, tokens and cost for the Claude Code work alone.
2. **Export 30 days (CSV)**. Open it: one row per month, person, agent, model entry, node and
   **project**, with calls, tokens and cost. Filter `project = pump-controller`: the engineering
   chargeback. Admin → Audit: `usage.export`.
3. *Needs an Anthropic or OpenAI admin key.* The cloud entry carries a `usageReport` block in
   `models.yaml` (IDE tab): `usageReport: { apiKey: ${secret:anthropic-admin-key}, apiKeyId: <the
   call key's id> }`, the organisation's admin key, never the call key, and the call key's id so other
   apps on the account are not counted. Usage tab → *Checked against the provider's bill*: for each
   such entry, yesterday's metered tokens beside the provider's own report for the same key, and a
   verdict: *matches*, *billed more than metered* or *metered more than billed*. **Compare yesterday
   now** runs it at once. Admin → Audit: `usage.reconcile`, per provider and key, never the admin key.
4. Say what *billed more than metered* means: calls reached the provider with this organisation's
   key without passing through AI Stackops. The key has been copied somewhere. Rotate it.

**Land:** the ledger is checked against the provider's own bill daily, and the same ledger splits
the cost by project for chargeback.

---
