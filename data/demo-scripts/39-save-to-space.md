---
type: scenario
title: "39. Save to space"
tags: ["scenario-39"]
level: essentials
---
**Level:** Essentials: the `board-brief` agent, two tools (the close package and the canvas).
Measured on Qwen 3.5 9B (2026-10-01): end to end three times in a row, every step passing; its bench check (`save-to-space`) 10 of 10.


*A draft an assistant made becomes a document the person keeps: versioned, linked to the conversation and
the sources it came from, and never less sensitive than what it was made from.*

**You are** Lena; Dana in the second window for the last step.

1. As Lena, **Spaces** → *New space* `Board prep`.
2. Agents → `board-brief`: **"Draft a one-page board brief on Q2 2026 revenue against the forecast."** It
   searches the close package, and the canvas opens with the brief: 41.2 million against a forecast of
   40.5 million, with the document named.
3. Above the canvas, **Save to space** (the folder with a plus) → `Board prep`, level *The conversation's
   level* → Save. The brief reads **confidential**, *Set by* **conversation**: the conversation read the
   confidential close package. The space is now confidential too. Save it once more choosing *internal*:
   refused, *This came from a conversation at confidential, so it is kept at confidential or higher.*
4. Spaces → `Board prep` → the brief → **Text**: the conversation it came from, with a link back, and the
   answer's sources: the close package.
5. Back in the chat: **"Rewrite the brief on the canvas as three bullet points."** Save to space → *New
   version of* the brief. The space lists it once, at version 2, still confidential; the first version
   is kept and no longer counts toward the limits. Its **Text** now names the revision's answer, in the
   same conversation.
6. As Dana: nothing of it under her Spaces. Admin → Audit, `space.save`: the file id, the level, the
   source level, the conversation and answer ids; never the title or a word of the brief.

**Land:** what an assistant drafts can be kept without leaking down a level on the way out of the chat,
and every document knows where it came from.

---
