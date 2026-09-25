---
type: scenario
title: "16. The runaway agent"
tags: ["scenario-16"]
level: essentials
---
**Level:** Essentials.


*Budgets and rate limits as circuit breakers, per person, per agent, per model, on real answers
and real dollars.* Stronger with the `claude-haiku` entry from *Before the day*; complete without
one (see the end).

**You are** Dana; Priya in the second window. A run is about ten helpdesk answers, roughly 10–15
cents on Haiku; the entry's 1 USD a day stops anything beyond that.

1. As Dana, Agents → `helpdesk` → edit its model to `claude-haiku`. Save. Say: the most-used
   assistant in the building now runs on a paid cloud model, and three fences sit around it.
2. As Priya, `helpdesk`: **"How do I reset my VPN certificate?"** Claude answers from the VPN reset
   runbook and quotes the step. As Dana, Usage tab → *By model entry* → `claude-haiku`: one row, its
   tokens and its cost at the pricing on the entry, about a cent. Note that per-answer cost; step 4
   uses it.
3. **The person fence, by rate.** Admin → Policy → Limits: member tier, Requests / min **2**. Save.
   As Priya, ask three in a row without waiting: **"The plant floor lost network, what do I do
   first?"**, **"A print job is stuck in the queue, how do I clear it?"**, **"What does IT set up
   for a new starter on day one?"** Two answers; the third is refused with *Limit reached: 2
   requests per minute for priya — retry in …s*. Wait it out, ask the third again: answered.
   The count is questions, not model calls. Set Requests / min back to empty.
4. **The model fence, by spend.** As Dana, Usage shows what `claude-haiku` has spent in the last 24
   hours. Models tab → `claude-haiku` → USD / day: type that figure plus about three answers' worth
   (spent $0.06 and a cent an answer: **0.09**). Type it; the arrows step by 0.50. Save. As Priya,
   keep asking runbook questions (**"How do I rebuild my laptop?"**, the VPN question again). A few
   are answered, then: *Limit reached: $0.09 per day for model entry "claude-haiku" (used $0.09).
   It frees up as the rolling 24 hours pass; an admin can raise it in the model entry's budget on
   the Models tab.* The check runs before each call, so the answer that crosses the line still
   arrives and the next one is refused. Usage: Priya's rows add up to it, at the price you set,
   and the same calls are on the Anthropic bill.
5. Admin → Audit, action `limits.exceeded`: the rate refusal (scope principal) and the spend
   refusal (scope model), each throttled to one row per five minutes so a loop cannot flood the
   log.
6. Show the third scope without running it: an agent's own `limits` (runs per minute, spend per
   month) in its definition. Say: a runaway loop, a leaked API key, or an over-enthusiastic pilot
   all hit the same three fences.
7. Reset now (the list at the end): `helpdesk` back to `default`, `claude-haiku` back to 1 USD a day.

*Without a cloud key:* skip step 1 and give the `mlx-serve` entry pricing 1 / 5 per million on the
Models tab. The local model answers, Usage prices each call as if it were Haiku, nothing is billed,
and steps 3–5 run the same with `mlx-serve` in place of `claude-haiku`. A 9B answer costs more
tokens than Claude's, so read the per-answer cost from Usage before setting the cap. Remove the
pricing afterwards.

**Land:** spend and load are bounded by policy before they become an invoice, and every refusal is
recorded with who, what and how much.

---
