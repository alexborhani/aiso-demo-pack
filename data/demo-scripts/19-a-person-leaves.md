---
type: scenario
title: "19. A person leaves"
tags: ["scenario-19"]
level: essentials
---
**Level:** Essentials, no chat model. Measured (2026-10-01): end to end three times in a row, every step
passing, after scenario 39 each time.


*Subject access, a legal hold that stops every deletion, erasure and the grace period, with the audit
log kept intact.*

**You are** Dana; Lena in the second window for step 3. Best after scenario 39, which leaves Lena her
`Board prep` space; without it, have Lena make any space and upload a file from `space-files`.

1. Admin → People → Users → Jordan → the download icon (*Export their data first* on the delete
   dialog does the same): one JSON with the account, the roles, the
   documents Jordan added, the memories, the usage rows and the audit rows Jordan is the actor of.
   Say: this is the subject-access request, answered in one click.
2. Admin → Data → *Legal hold*: set it, with a reason (*Northfield dispute*). The Setup checklist shows
   it; every prune stops.
3. As Lena, Spaces → `Board prep` → **Delete**. It leaves her list with a note: kept under a legal hold,
   deleted when the hold is cleared. As Dana, the *Legal hold* panel counts one kept item. Say: under a
   hold a person's own delete hides; it does not destroy.
4. *Export held content* → person **lena** → *Export*: one JSON file signed with the workspace key, holding
   the deleted space and the text of its documents, who deleted it and when. Admin → Audit, `hold.export`:
   the filters and the counts, never the content.
5. People → Users → *Delete disabled accounts* → **After 30 days**. Disable Jordan (his contract ended):
   his row reads *disabled*, *deleted on* a date 30 days out. Say: a deactivation, which is what a SCIM
   delete does, keeps the account and everything in it for the grace period so a returning person finds
   it all; after that the account goes with its content.
6. Now **Erase** Jordan, with a reason. Under the hold it waits: the row reads *deletion waits for the
   legal hold*, and the erasure is recorded.
7. Admin → Data → clear the hold. The toast: one kept item deleted, one deferred deletion done. Lena's
   space is gone for good; Jordan is erased: keys revoked, memories and added documents removed, usage
   rows pseudonymised, the account deleted. Admin → Audit: `users.erase` by *legal-hold* lists the
   steps; the rows that name Jordan as the actor are untouched. Set *Delete disabled accounts* back to
   *Never*.
8. Say: reinstalling the pack brings Jordan back for the next demo.

**Land:** the data-protection lifecycle is built in, per person: a hold stops every deletion, people's
own included, everything it held back runs when it lifts, and the audit trail is the one thing never
edited.

---
