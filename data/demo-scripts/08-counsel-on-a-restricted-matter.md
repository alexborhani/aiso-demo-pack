---
type: scenario
title: "8. Counsel on a restricted matter"
tags: ["scenario-8"]
---
*The most sensitive store on the estate, in use, and invisible to everyone else.*

**You are** Dana; Jordan in the second window.

1. As Dana, `counsel`: **"Where do we stand with the regulator this year, and what is due next?"**
   Answered from the regulator correspondence record.
2. **"Summarise the Crestview lease dispute and our exposure."**
3. Show the agent's definition (Agents → counsel → edit, read-only glance): `access: minRole: admin`,
   `egress: allowFrontier: false`. The store `legal-matters` is restricted, Legal, admin-only,
   local-only.
4. As Jordan: no `counsel` in the list; Knowledge → `legal-matters` search: refused.
5. As Dana, Admin → Policy → Classification → *Compliance*: the handling rule for restricted requires
   access restriction and local-only processing, and the store meets both.

**Land:** the same platform that answers a contractor's VPN question holds counsel's files, and the
policy's handling rules are checked against the configuration, not promised.

---
