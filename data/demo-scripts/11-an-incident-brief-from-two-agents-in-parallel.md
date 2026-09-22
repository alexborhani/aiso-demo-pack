---
type: scenario
title: "11. An incident brief from two agents in parallel"
tags: ["scenario-11"]
level: standard
---
**Level:** Standard.


*Fan-out and merge: two specialists work at once, and the workflow refuses to pretend a missing half
arrived.*

**You are** Dana. Workflow: `incident-brief`. Two to three minutes end to end at 4096; faster at 16K.

1. Workflows → `incident-brief` → *Run* with incident **"INC-2026-021"**. Two agents research in
   parallel: the security lead reads the incident and access review; the helpdesk reads the runbook
   side. A merge step joins them into one brief.
2. Open the run: the parallel block, each branch's output, the merge record showing what was expected
   and what arrived. Say: if one branch fails, the merge guard marks the run failed rather than
   shipping half a brief as if it were whole.
3. Read the brief aloud: what happened, what was done, what is open.

**Land:** this is how the platform composes specialists into a process with a deterministic spine.
The agents are the same ones people chat with; the workflow is the management layer.

---
