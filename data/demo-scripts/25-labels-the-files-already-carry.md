---
type: scenario
title: "25. Labels the files already carry"
tags: ["scenario-25"]
level: essentials
---
**Level:** Essentials for steps 1–6 (no chat model; step 5 needs only the embedding model):
measured end to end on Qwen 3.5 9B, 3 of 3 runs. Step 7 (Chat finding the board pack for Lena) did
not work on the 9B in any run: treat it as Standard, or skip it.


*Most organisations have already labelled their documents in Microsoft 365. The platform reads
those labels from inside the file and files each document at the level the policy gives that label.*

**You are** Dana in one window, Sam in the other. Store: `labelled-files`, nine Word, Excel,
PowerPoint and PDF files, seven carrying a Purview sensitivity label, two that cannot be opened. No
Microsoft 365 tenant is involved: the labels were written into the files for the pack.

1. As Dana, Admin → Policy → Classification → **External labels** → Purview. Five rows map label names
   to levels, and two rows match by label id: *General* and *Confidential - Finance*. Say why: Office
   files saved since 2022 carry only the label's id, not its name, so a mapping by name alone
   misses them. *Partner Shared* has no row.
2. Knowledge → `labelled-files` → *Sources*. Seven files with a level, *Set by* **Purview label**: the
   town hall agenda public, the shift handover and the safety bulletin internal, the Q3 board pack
   confidential Finance, the grievance notes confidential HR, the Northfield memo restricted Legal.
   The shift handover is the Word file with only the id; the grievance notes are a PDF whose label
   sits only in its compressed XMP metadata. No one typed any of these levels.
3. The price list reads at the store default, internal. Its label, *Partner Shared*, has no mapping
   (the server log names it; the Sources panel does not). Press *Classify* on it, set confidential,
   give a reason, *Save*: applied at once. Say: until the policy knows a label, a person or the
   classifier decides.
4. Two files are missing from the list. Admin → Policy → Classification → **Compliance** → *Check now*:
   two `unreadable` findings. `audit-committee-minutes.pdf`: "Not indexed: Encrypted by the
   sensitivity label Highly Confidential; the content could not be read." `salary-review-2027.pdf`:
   "Encrypted with a password". The platform says what it could not read instead of indexing an
   empty page.
5. Enforcement → **Enforce** (skip if scenario 4 left it there). As Sam (builder, cleared internal and
   confidential Security), Knowledge → `labelled-files` → *Search*: **"liability cap Northfield"**, then
   **"Q3 revenue against plan"**. Neither the memo nor the board pack comes back; the agenda and the
   bulletin do when asked about them. As Dana, the same two searches return both files.
6. Admin → Audit, filter `classification.refused`: one row per search Sam made, naming the store and
   the levels withheld.
7. Optional, with the chat model: as Priya, Chat: **"What did the Q3 board pack say about revenue
   against plan?"** She is told nothing she is not cleared for; as Lena (Finance) the answer gives
   41.8 million against a plan of 44.5 million, with the board pack as its source.

**Land:** the labels people already put on files are the classification. Nobody re-tags anything, and
a file the platform cannot open is reported, not guessed at.

---
