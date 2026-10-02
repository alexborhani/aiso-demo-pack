---
type: scenario
title: "38. Instructions of your own"
tags: ["scenario-38"]
level: essentials
---
**Level:** Essentials. Measured on Qwen 3.5 9B (2026-10-01): end to end three times in a row, every step passing; its bench check (`instructions`) 10 of 10.


*Each person tells the assistant once how they want their answers. The same question then comes back
shaped for each of them, and nobody else reads what they wrote.*

**You are** Lena in one window, Priya in the other; Dana for the last step.

1. As Lena, Account → **Personal instructions**: **"Answer in German. I work in Finance at Crestview."**
   Save. As Priya: **"I am an operations coordinator at the Halden plant and I read answers on my phone.
   Keep answers short and use bullet points."** Save.
2. As Lena, Chat: **"How do I reset my VPN certificate?"** The steps from the VPN runbook, in German.
3. As Priya, the same question: the same steps as short bullet points, in English. Chat's own
   instructions say plain sentences and no lists; Priya's changed the form of the answer. Say: the
   person's instructions come after the agent's and the admin's, marked as the person's preferences, and
   access is enforced in code, so no instruction widens what anyone may see or use.
4. As Dana, Admin → Data → **Personal instructions**: on or off, the length limit, and how many people
   have written some. No text. Admin → Audit, `instructions.set`: who, and how many characters.

**Land:** personalisation that costs nothing in control: one sentence per person, applied everywhere
they chat, and read by nobody else.

---
