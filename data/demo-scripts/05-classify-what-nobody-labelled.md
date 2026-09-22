---
type: scenario
title: "5. Classify what nobody labelled"
tags: ["scenario-5"]
level: essentials
---
**Level:** Essentials.


*The unglamorous truth of every estate: most content carries no label. Here it gets one.*

**You are** Dana. Store: `site-notes`, six Riverside notes as staff wrote them, none labelled.

1. Knowledge → `site-notes` → *Sources*. Every note reads at the store default, decider *store default*.
2. Press *Classify* on the workshop incident note (the injury): set confidential, tick HR, give a
   reason, *Save*. Applied at once; Audit shows `knowledge.classify` with the reason.
3. Press *Classify* on the parking note and set it public: it goes to the review queue instead,
   because that would lower it. Admin → Policy → Classification → *Reviews*: approve it there. Say:
   raising is a person's call, lowering is a second person's.
4. Admin → Policy → Classification → classifier settings: set the model to the local chat entry, save.
   Back on *Sources*, *Send undecided to the classifier*: four notes go *pending*. Refresh every ten
   seconds. Within a minute each carries a level, categories and the classifier's confidence:
   the customer visit confidential Finance, the badge follow-up restricted Security, the checklist
   internal, the volunteers note public or internal. The note a person decided is untouched.
5. Admin → Policy → Classification: the classifier status and the backlog count, now zero.

**Land:** classification is not a project. It is a background service driven by the organisation's own
criteria, with a person in the loop only where the policy says so.

---
