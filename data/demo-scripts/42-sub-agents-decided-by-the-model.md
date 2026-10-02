---
type: scenario
title: "42. Sub-agents, decided by the model"
tags: ["scenario-42"]
level: standard
---
**Level:** Standard: the `incident-coordinator` agent, administrators only, with `security-lead` and
`helpdesk` as its sub-agents. Measured: pending (new in 1.16.0); its bench check is `subagents`.


*The same two specialists as scenario 11, but an agent decides whom to ask, and each one works with a
fresh context of its own.*

**You are** Dana; Sam in the second window.

1. Agents → `incident-coordinator` → its definition: no stores of its own, and `subagents: { enabled:
   true, agents: [security-lead, helpdesk], maxParallel: 2 }`. That gives it one tool, `task`.
2. Ask: **"Brief me on INC-2026-021: what happened, what is still open, and what the runbooks say about
   the plant network side."** Two `task` calls in the reply, one to each specialist, running at once. Each
   child starts with only its question, uses its own tools, and has its own answer checked. The
   coordinator writes one brief and names where each part came from.
3. Admin → Audit, `agents.task`: one row per child, with Dana as the actor, the child agent as the
   target, the parent, the depth and how long it took. A child is checked against Dana's access as if
   she had asked it herself, and never gets more than she has.
4. As Sam (a builder): `incident-coordinator` is not in his list; through the API it answers *open to
   the admin tier and above*.
5. Put it beside scenario 11. The workflow always runs both branches and its merge guard fails the run if
   one is missing. The coordinator decides for itself whom to ask, and says so when a specialist can't
   answer. Say: a workflow when the steps are known, sub-agents when the question decides them.

**Land:** an agent can split a question among specialists the way a person would, while every child run
stays inside the asker's access and is on the record.

---
