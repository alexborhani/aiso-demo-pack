---
type: scenario
title: "16. The runaway agent"
tags: ["scenario-16"]
level: essentials
---
**Level:** Essentials.


*Budgets and rate limits as circuit breakers, per person, per agent, per model.*

**You are** Dana; Priya in the second window.

1. Admin → Policy → Limits: set the member tier to 1,500 tokens a day. Save.
2. As Priya, `helpdesk`: **"How do I reset my VPN certificate?"** Answered. Ask again with another
   runbook question. On the second or third call the reply is refused: budget exceeded, with what was
   used and the limit. The Usage tab as Dana shows Priya's rows adding up to it.
3. Admin → Audit: `limits.exceeded`, scope principal, throttled to one row per five minutes so a
   loop cannot flood the log.
4. Show the other two scopes without running them: an agent's own `limits` (runs per minute, spend
   per month) in its definition, and a model entry's `budget` on the Models tab. Say: a runaway loop,
   a leaked API key, or an over-enthusiastic pilot all hit the same three fences.
5. Set the member cap back.

**Land:** spend and load are bounded by policy before they become an invoice, and every refusal is
recorded with who, what and how much.

---
