---
type: scenario
title: "21. One chat for everyone"
tags: ["scenario-21"]
level: essentials
---
**Level:** Essentials.


*A member never picks an agent. Chat answers from what they may use, refuses the rest
by name, and asks the admins on their behalf.*

**You are** Jordan, then Marcus, then Dana (two windows).

1. As Jordan, the Chat tab (it is the only chat a member has; the workshop tabs are gone). Ask
   **"How do I reset my VPN certificate?"** Chat hands the question to the helpdesk and answers
   from the runbook, naming it.
2. Still as Jordan: **"How much holiday do I carry over at year end?"** Chat says the people
   partner owns that and it is outside Jordan's access, and offers to ask the administrators. Say
   **"Yes, please ask."** Chat confirms the request was sent.
3. As Marcus, Chat: the same holiday question. This time it reaches the people partner and answers.
   Say: same chat, same question, different person, different destinations.
4. As Dana, Approvals: Jordan's request is waiting, with `hr-partners` pre-selected because that is
   the role `people-partner` names. *Grant*. Admin → Audit → *Chat routing* lists Jordan's refused
   route and Marcus's successful one.
5. As Jordan again (sign out and in — the role is read at sign-in): the holiday question now
   reaches the people partner.

**Land:** one chat for members, resolved per person on every request; nothing is granted by
Chat, and every route and every request is on the record.

---
