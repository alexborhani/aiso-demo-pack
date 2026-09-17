---
type: scenario
title: "3. Who can see what"
tags: ["scenario-3"]
---
*RBAC, custom roles and clearances applied to real questions by four people.*

**You are** each of Jordan, Marcus, Lena, Dana in turn (two windows, swap the second).

1. As Jordan, Agents tab: count the agents. `people-partner`, `finance-analyst`, `counsel` and
   `security-lead` are not listed at all. Knowledge tab: `people-files` and `finance-close` are listed,
   but *Search* inside them answers `knowledge_access_denied`.
2. As Marcus, `people-partner`: **"What is the 2026 band for a senior engineer?"** and
   **"Summarise Priya Nair's last review."** Both answered. Then `finance-analyst`: not listed.
3. As Lena, `finance-analyst`: **"What was Q2 2026 revenue against the forecast?"** Answered.
   `people-partner`: not listed.
4. As Dana, Admin → People → Roles: open `hr-partners` and `finance-analysts`. Each is a handful of
   permissions plus a clearance (confidential, one category). Open the audit log, filter
   `knowledge.access.denied`: Jordan's attempts, with the reason.

**Land:** one platform, one set of stores, and each person sees exactly their slice, enforced at
retrieval on every chunk, not by which assistant they were given.

---
