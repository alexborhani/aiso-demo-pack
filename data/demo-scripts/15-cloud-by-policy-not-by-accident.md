---
type: scenario
title: "15. Cloud by policy, not by accident"
tags: ["scenario-15"]
level: standard
---
**Level:** Standard.


*Where a cloud model fits: as a governed entry with access, a ceiling and a budget, never as the
default.* Stronger with a cloud key on the host (Anthropic, or OpenRouter — `provider: openrouter`, model
`<vendor>/<model>`, key `${OPENROUTER_API_KEY}`; the steps read the same); complete without one.

**You are** Dana; Jordan in the second window.

1. Models tab → the OpenRouter tab (or Anthropic, or Azure for Claude and OpenAI models in the
   organisation's own Azure tenant) → **New entry**: name `cloud`, model
   `deepseek/deepseek-v4.1-flash` (the model this was measured on; on Anthropic `claude-sonnet-4-6`
   reads the same), key `${OPENROUTER_API_KEY}`, access minimum role admin, budget 1 USD a day,
   pricing 0.30 / 1.20 per million, maximum classification internal. Save. Say: four decisions were just made about a cloud
   model before anyone could use it: who, how much, what data, at what price.

   *With Azure* (**Needs:** an Azure subscription with an Azure OpenAI or Foundry resource and a
   deployment; not tested). The Azure tab → **New entry**: *Resource endpoint*
   (`https://<resource>.openai.azure.com`), *API* **Azure OpenAI** (or **Claude on Foundry**), *Sign
   in with* **API key** or **Managed identity (Microsoft Entra)**, *Chat deployment*, *Data zone*
   (EU, US or global: recorded, so the evidence bundle says where the model ran). Access, ceiling,
   budget and pricing as for any cloud entry. Say: the model runs in the organisation's own tenant
   under its own agreement; with managed identity there is no key to leak. The steps that follow
   read the same with the Azure entry.

   *Also possible, not tested here* (no account on the demo Mac): an entry on **Amazon Bedrock**
   (`provider: bedrock`, a `region`; a Bedrock API key or the host's AWS credentials), on **Google
   Vertex AI** (`provider: vertex`, `project` and `region`; a service-account key held in the secret
   store), or on OpenAI's **Responses API** (`api: responses` on an OpenAI or Azure entry). Each takes
   the same access, ceiling, budget and pricing as the entry above.
2. Agents → *New agent* `board-analyst`: model `cloud`, tool `knowledge:handbook`, prompt "You are a
   concise business analyst." Save.
3. As Jordan, `board-analyst`: **"Summarise our values in one line."** Refused before anything is
   dialled: access to model `cloud` needs role admin. Admin → Audit: `model.access.denied`.
4. As Dana, same question. With a key on the host, the answer comes from Claude and the usage row
   carries the cost at the pricing you set. Without one, the attempt reaches the provider and is refused
   by them; the point stands: the only person who could reach the cloud was the one the policy allows.
5. Try `counsel` with the cloud entry (edit its model to `cloud`): refused for everyone, because the
   agent and the legal store both say `allowFrontier: false`. Then Admin → Setup: the checklist
   shows the cloud entry needs a budget and access (it has both), and the compliance report says
   whether any restricted store could reach it (it cannot, ceiling internal).
6. Mention the operator lock: `EGRESS_ALLOW_FRONTIER=false` in the host's environment refuses every
   cloud call for everyone, and no setting in the Studio can override it. Step 8 shows it live.
7. The router, local first and cloud only when the local model cannot: IDE tab → `models.yaml`, add an
   entry `frontline` with `provider: router` and `candidates: [mlx-serve, cloud]`, and set `helpdesk`'s
   model to `frontline`. As Dana, `helpdesk`: **"How do I reset my VPN certificate?"** — answered by
   the local model; Admin → Audit, `models.route`: candidate `mlx-serve`, reason *first candidate*.
   Then open `bundles/aiso-demo-pack/long-reads/riverside-commissioning-report.md` in the IDE tab
   (320 test records, about 19,000 tokens — more than the local engine's window), copy all of it into
   the chat and ask: **"How many of these tests failed, and which fault was most common?"** The router
   skips the local model before dialling — the audit row's reason says *fit: mlx-serve (context …)* —
   and the cloud entry answers; the answer key is beside the report. As Jordan, the same paste is
   refused: the local model does not fit and the cloud entry is not his to use.
8. Optional, the operator lock live (it needs a restart of the host, so do it last; not yet run,
   measured: pending). Quit AI Stackops and start it again with `EGRESS_ALLOW_FRONTIER=false` in its
   environment (the deploy kit's service environment, or `EGRESS_ALLOW_FRONTIER=false ai-stackops
   start`). Models tab: *Frontier providers* **locked by operator**: *Cloud models are off for
   everyone on this node.* As Dana, `board-analyst` (on `cloud`): refused before anything is
   dialled, for the admin too. Admin → Audit: `egress.denied`, reason *EGRESS_ALLOW_FRONTIER=false
   locks this host to local models*. No Studio setting turns it back on; restart without it.

**Land:** cloud models are welcome where the policy says so, with a person, a data class and a budget
attached, and the answer to "did anything leave the building" is in the audit log.

---
