---
type: scenario
title: "37. A space of your own"
tags: ["scenario-37"]
level: essentials
---
**Level:** Essentials. Step 5 needs the `deepseek-flash` entry from *Before the day*; it needs no working
key, because the refusal comes before anything is dialled. Measured on Qwen 3.5 9B (2026-10-01): end to end three times in a row, every step passing; its bench check (`space-answer`) 10 of 10.


*A person keeps their own documents in one place and chats with them. The platform decides which models
may read them and how much the space may hold. Nobody else sees any of it unless its owner shares it
(scenario 40).*

**You are** Sam in one window, Dana in the other. Sam uploads three files from the pack's `space-files`
folder (`<workspace>/bundles/aiso-demo-pack/space-files/`): a Word file carrying the Purview label
*Confidential*, his own notes, and a sensor log.

1. As Sam, **Spaces** → *New space* `Riverside rig trips`. Upload `riverside-interlock-trips.docx` and
   `rig-trip-working-notes.md`. The Word file reads **confidential**, *Set by* **label**; the notes read
   internal, *Set by* **default**. The space takes the highest level of its documents: confidential.
2. Under the space, its limit: about 22,600 tokens, set by `mlx-serve`, the local model, whose window is
   32,768 tokens (the rest is kept for instructions, the conversation and the reply; the figure assumes the
   entry's Max Tokens at 4,096). Upload `halden-rig-sensor-log-2026.csv`, about 44,000 tokens: refused.
   Every document goes into the chat whole, the model allowed to read this space cannot take it, and
   *larger sets of documents belong in a knowledge store*. Say: the line between a personal space and a
   governed knowledge store is set by the models the organisation runs.
3. **Chat in this space**. Ask: **"Which sensor caused most of the rig trips, and what does the analysis
   recommend doing about it?"** The local model answers from the Word file: sensor GS-2, 29 of the 41 trips,
   a cracked bracket, a coded safety sensor in its place. With the reply, a note lists what a space chat
   does not have: nothing in it is handed to another agent or saved where other people can read it.
4. **"What do my working notes say I should check on Tuesday?"** The torque on the bracket bolts. Account
   → the usage line: *(… from a prompt cache)*. Every turn sends the documents again; the engine kept
   them from the first turn and read them back instead of working through them again. Say: that is what
   keeps a space affordable, on the Mac and on a cloud provider.
5. A new chat in the space, **With** `deepseek-flash`, the same question. Refused before anything is
   sent: *The model "deepseek-flash" may only see internal data, and this space holds confidential
   documents.* As Dana, Admin → Audit, `space.chat.refused`: the space id, the model and the levels,
   never a name or a word of the space.
6. As Dana, **Spaces** lists only her own. Admin → Data → **Spaces**: how many spaces, people,
   documents and megabytes, nothing more. Admin → Audit, `space.upload`: ids, levels and sizes, and the
   refused upload with its reason. Say: an admin reaches a space only if its owner shares it with them
   (scenario 40), or through the subject-access export of the whole account (scenario 19), and that
   export is on the record.

**Land:** people get a private place to work with their own documents, and the organisation still
decides which models read them and how much goes in. Sharing is the owner's choice, made by name: it is
on by default (Admin → Data → **Spaces**: *Allow sharing spaces*, up to 25 people per space), and
while classification is enforced a person not cleared for the space's level cannot open it.

---
