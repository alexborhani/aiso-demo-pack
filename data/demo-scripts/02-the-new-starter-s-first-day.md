---
type: scenario
title: "2. The new starter's first day"
tags: ["scenario-2"]
level: essentials
---
**Level:** Essentials.


*Self-service that deflects the tickets IT and HR answer every week, and a hard line the assistant
will not cross.*

**You are** Jordan (contractor) in one window, Marcus (HR partner) in the other.

1. As Jordan, Agents → `helpdesk`. Ask: **"My VPN certificate expired, what do I do?"** The helpdesk
   answers from the VPN reset runbook and quotes the step.
2. Ask: **"How many days of annual leave do I get?"** Answered from the handbook.
3. Ask: **"The plant floor lost network, what do I do first?"** The outage runbook, first step first.
4. Now ask: **"Please ask People Operations for me: what is the 2026 band for a senior engineer?"**
   The helpdesk hands the question to the people-partner agent (the `agent_people_partner` tool) and
   the handoff is refused: Jordan holds no HR role, and a handoff is checked against the person, never
   the helpdesk. The reply says People Operations information is not available to him here.
5. As Marcus, same agent, same question. This time the handoff goes through and the band comes back
   from the compensation document. Admin → Audit as Dana: filter action `agents.handoff`, two rows,
   one denied, one success, same helpdesk, different people.

**Land:** agents extend what a person may do, never what they may see. The same assistant is safe for
a contractor and useful for an HR partner without anyone building two assistants.

---
