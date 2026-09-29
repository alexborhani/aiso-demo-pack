---
type: scenario
title: "21. One chat for everyone"
tags: ["scenario-21"]
level: essentials
---
**Level:** Essentials.


*A member never picks an agent. Chat answers from what they may use, refuses the rest
by name, and asks the people who own it on their behalf.*

**You are** Jordan, then Marcus, then Dana (two windows).

1. As Jordan, the Chat tab (it is the only chat a member has; the workshop tabs are gone). Ask
   **"How do I reset my VPN certificate?"** Chat hands the question to the helpdesk and answers
   from the runbook, naming it.
2. Still as Jordan: **"How much holiday do I carry over at year end?"** Chat says the people
   partner owns that and it is outside Jordan's access, and offers to ask. Say **"Yes, please ask
   the people who decide access for me."** Chat confirms the request was sent; a card under the
   reply shows it waiting.
3. As Marcus, Approvals → *Access requests*: Jordan's request is here because Marcus owns the
   people partner (its *Owners* list names him), not because he is an admin. An owner has one
   choice: *Grant access to "people-partner"*, that agent and nothing else, never a role. Grant it
   with a note.
4. As Jordan, without signing out (the card under the reply turns *granted*): **"How many days of
   annual leave do I get?"** It now reaches the people partner, which answers from the handbook:
   25 days, 28 after five years. The HR files stay closed: the grant opened the agent, and Jordan's
   clearance is still public.
5. As Dana, Approvals shows the same request, answered by Marcus as owner; an admin could have
   assigned a role instead. Admin → Audit: `access.request`, `access.grant` with *as: owner*, and
   *Chat routing* lists Jordan's refused route and his successful one.
6. As Marcus, Account → *Access you granted*: Jordan and the people partner. *Revoke*. Jordan's
   next question is refused again.

**Land:** one chat for members, resolved per person on every request; access is asked of the
people who own the thing, granted for that one thing, and taken back in one click, all on the
record.

---
