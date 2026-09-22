---
type: scenario
title: "6. The finance close in a conversation"
tags: ["scenario-6"]
level: essentials
---
**Level:** Essentials.


*Numbers from the close package, with arithmetic done by a tool rather than the model.*

**You are** Lena; Jordan in the second window for the last step. *Needs room:* the close package
chunks plus the calculator exceed 4096 tokens; at 16K the question is one round.

1. As Lena, `finance-analyst`: **"What was Q2 2026 revenue against forecast, and by what percentage
   did we miss or beat?"** The agent reads the close package and the forecast, then calls the
   `calculator` function for the percentage. Open the tool trace under the reply: the search calls,
   the calculator call with its inputs.
2. **"Which items on the month-end close checklist are still open for September?"**
3. **"What changes in the 2027 pricing, and which customers are affected first?"**
4. As Jordan, `finance-analyst` is not listed; open the URL of the agent directly if you like: refused.

**Land:** the analyst's question is answered from the controlled close package in seconds, the maths
is deterministic, and the answer never reaches anyone outside the finance role.

---
