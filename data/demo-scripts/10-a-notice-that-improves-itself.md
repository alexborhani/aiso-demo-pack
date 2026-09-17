---
type: scenario
title: "10. A notice that improves itself"
tags: ["scenario-10"]
---
*A workflow where one agent drafts and another judges, until the reviewer is satisfied.*

**You are** Sam. Workflow: `customer-notice` (an evaluator loop). *Needs room:* three rounds of draft
and review; at 4096 the run completes but each round crawls.

1. Workflows → `customer-notice` → *Run* with subject **"the 2027 price change effective
   1 November"**. Watch the run: round one, the writer drafts; the helpdesk, acting as reviewer,
   scores it with feedback; round two addresses the feedback; the loop stops when the score clears
   the threshold or after three rounds, keeping the best.
2. Open the run's step metadata: rounds, the score per round, the final feedback. Open the workflow
   definition: eleven lines describe the loop, the threshold and what happens when rounds run out.
3. Say: the reviewer here is a local model; in production it can be a stricter agent, a function, or a
   different model entirely. *Needs room:* three rounds of draft plus review fit comfortably at 16K.

**Land:** quality is a loop, not a prompt. The organisation decides the bar and the platform iterates
to it, with every round recorded.

---
