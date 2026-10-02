---
type: scenario
title: "40. A space for the team"
tags: ["scenario-40"]
level: essentials
---
**Level:** Essentials: Chat on the local model, no new agent. Measured: pending (new in 1.16.0); its bench check is
`space-shared`.


*A person shares their space with named colleagues. Each one still has to be cleared for what is in it,
and nobody reads anyone else's conversations.*

**You are** Sam in one window, Dana in the other; Priya for step 3. Sam's `Riverside rig trips` space from
scenario 37 (the Word file and his notes; confidential), or make it again.

1. As Dana, Admin → Policy → Classification → Enforcement: **Enforce** (as in scenario 4). This step
   matters: the clearance check on a shared space is the same one every store gets, so with enforcement
   *Off*, as the pack ships, a person below the space's level is let in and reads its documents (with
   *Monitor*, let in and recorded). Sharing itself has nothing to switch on: Admin → Data → **Spaces**
   shows *Allow sharing spaces* on by default, up to 25 people per space.
2. As Sam, Spaces → `Riverside rig trips` → **Share**. Username **dana**, *As* **Member** → Share. Then
   **priya.nair@meridianworks.example**, Member → Share. The dialog takes a username or an email exactly
   (there is no directory to search) and says at once: *They are not cleared for confidential, so they
   cannot open it until their clearance changes or the level comes down.* Priya's row reads *Not cleared
   for confidential: cannot open it*. (The dialog says this whatever the enforcement mode; it holds
   only under *Enforce*, which is why step 1 comes first.)
3. As Priya, Spaces → **Shared with you**: *sam's · you can read · above your clearance*. It doesn't open,
   and a chat in it is refused: *This space holds documents at confidential, above what you are cleared
   for, so you cannot open it or chat in it.* Admin → Audit, `classification.refused`: Priya, the space
   id, the level. Say: sharing gives a person a place in the space, never a level they do not have.
4. As Dana, Spaces → Shared with you → the space: the two documents, read-only. **Chat in this space**,
   **"Which sensor caused most of the rig trips, and what does the analysis recommend doing about
   it?"** Sensor GS-2, 29 of the 41 trips, from Sam's Word file. Her conversation is hers: Sam's list of
   conversations in the space doesn't show it, and hers doesn't show his.
5. As Dana, try to write the space's instructions: refused, *This space was shared with you to read and
   chat in.* As Sam, Share → Dana's row → **Editor**. Dana writes the instructions: **"Answer for the
   Riverside maintenance team: name the sensor tag and the trip count."** An editor can also upload and
   replace documents; one that would raise the level above someone it is shared with asks first and
   says how many people would lose access. What she adds is Sam's and counts toward his limits.
6. As Sam, **Remove** Priya. As Dana, **Leave**: the space is gone from her list, and her conversation in
   it stays hers but can't go on. Admin → Audit, `space.share` and `space.unshare`: the space id, the
   member's id, the role and whether it was added, changed or left; never a name, a file name or a word
   of the space.

**Land:** a space can be a team's working set without becoming a way around the policy. The owner
chooses the people by name, the clearance check still runs for each of them, and every share and
every refusal is on the record.

---
