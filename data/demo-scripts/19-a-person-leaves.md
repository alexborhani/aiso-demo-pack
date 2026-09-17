---
type: scenario
title: "19. A person leaves"
tags: ["scenario-19"]
---
*Subject access, erasure and legal hold, with the audit log kept intact.*

**You are** Dana.

1. Admin → People → Users → Jordan → the download icon (*Export their data first* on the delete
   dialog does the same): one JSON with the account, the roles, the
   documents Jordan added, the memories, the usage rows and the audit rows Jordan is the actor of.
   Say: this is the subject-access request, answered in one click.
2. Admin → Data → *Legal hold*: set it, with a reason. The Setup checklist shows it; every prune
   stops. Say: retention is suspended estate-wide for litigation without touching the data.
3. Clear the hold. Back on Users → Jordan → *Erase*: keys revoked, memories and added documents
   removed, usage rows pseudonymised, the account deleted. The audit rows are untouched: they name
   the actor as they did. Admin → Audit: `users.erase` lists the steps.
4. Say: reinstalling the pack brings Jordan back for the next demo.

**Land:** the data-protection lifecycle is built in, per person, with the audit trail as the one
thing that is never edited.

---
