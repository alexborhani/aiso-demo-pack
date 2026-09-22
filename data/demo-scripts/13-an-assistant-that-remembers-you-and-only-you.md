---
type: scenario
title: "13. An assistant that remembers you, and only you"
tags: ["scenario-13"]
level: essentials
---
**Level:** Essentials.


*Personal memory with a boundary the audience can see, and a person's right to see and delete it.*

**You are** Priya in one window, Marcus in the other.

1. As Priya, `assistant`: **"I'm Priya, a team lead at the Halden plant. I start at 6 and prefer
   bullet points."** The assistant keeps a short note (the `save_memory` tool) and says what it kept.
2. Start a new chat as Priya: **"What do you remember about me?"** It recites the note.
3. As Marcus, `assistant`: **"What do you remember about me?"** Nothing. Memory is per person by
   default; the file for Priya is hers alone.
4. As Priya, Account → *Your data*: the memory is listed by agent with a *Forget* button. Press it;
   ask the assistant again; it has forgotten. Admin → Audit as Dana: `memory.forget`.
5. Optional: **"Plan my first hour tomorrow."** The assistant uses what it knows (start time, format).

**Land:** personalisation without a data-protection problem: memory is scoped to the person, visible to
them, deletable by them, and never shared between people or nodes.

---
