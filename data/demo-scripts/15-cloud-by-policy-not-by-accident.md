---
type: scenario
title: "15. Cloud by policy, not by accident"
tags: ["scenario-15"]
---
*Where a cloud model fits: as a governed entry with access, a ceiling and a budget, never as the
default.* Stronger with a cloud key on the host (Anthropic, or OpenRouter — `provider: openrouter`, model
`<vendor>/<model>`, key `${OPENROUTER_API_KEY}`; the steps read the same); complete without one.

**You are** Dana; Jordan in the second window.

1. Models tab → *Frontier providers* → add one: provider Anthropic, name `claude`, model `claude-sonnet-4-5`,
   key `${ANTHROPIC_API_KEY}`, access minimum role admin, budget 5 USD a day, pricing 3/15 per
   million, maximum classification internal. Save. Say: four decisions were just made about a cloud
   model before anyone could use it: who, how much, what data, at what price.
2. Agents → *New agent* `board-analyst`: model `claude`, tool `knowledge:handbook`, prompt "You are a
   concise business analyst." Save.
3. As Jordan, `board-analyst`: **"Summarise our values in one line."** Refused before anything is
   dialled: access to model `claude` needs role admin. Admin → Audit: `model.access.denied`.
4. As Dana, same question. With a key on the host, the answer comes from Claude and the usage row
   carries the cost at the pricing you set. Without one, the attempt reaches Anthropic and is refused
   by them; the point stands: the only person who could reach the cloud was the one the policy allows.
5. Try `counsel` with the cloud entry (edit its model to `claude`): refused for everyone, because the
   agent and the legal store both say `allowFrontier: false`. Then Admin → Setup: the checklist
   shows the cloud entry needs a budget and access (it has both), and the compliance report says
   whether any restricted store could reach it (it cannot, ceiling internal).
6. Mention the operator lock: `EGRESS_ALLOW_FRONTIER=false` in the host's environment refuses every
   cloud call for everyone, and no setting in the Studio can override it.
7. The router, local first and cloud only when the local model cannot: IDE tab → `models.yaml`, add an
   entry `frontline` with `provider: router` and `candidates: [mlx-serve, claude]`, and set `helpdesk`'s
   model to `frontline`. As Dana, `helpdesk`: **"How do I reset my VPN certificate?"** — answered by
   the local model; Admin → Audit, `models.route`: candidate `mlx-serve`, reason *first candidate*.
   Then open `bundles/aiso-demo-pack/long-reads/riverside-commissioning-report.md` in the IDE tab
   (320 test records, about 19,000 tokens — more than the local engine's window), copy all of it into
   the chat and ask: **"How many of these tests failed, and which fault was most common?"** The router
   skips the local model before dialling — the audit row's reason says *fit: mlx-serve (context …)* —
   and the cloud entry answers; the answer key is beside the report. As Jordan, the same paste is
   refused: the local model does not fit and the cloud entry is not his to use.

**Land:** cloud models are welcome where the policy says so, with a person, a data class and a budget
attached, and the answer to "did anything leave the building" is in the audit log.

---
