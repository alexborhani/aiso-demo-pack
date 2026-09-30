---
type: guide
title: "Levels: pick the demo your model can carry"
tags: []
---
The pack installs at one of three levels, chosen on the install dialog and changeable later from
the pack card (agents above the level are removed, the people and the policy stay). Every scenario
below says which level it needs; the people, the stores of the essentials and the scripts are the
same at every level, so a story told at Essentials reads the same at Full.

| Level | Model it was measured on | What it adds | Scenarios |
| --- | --- | --- | --- |
| **Essentials** | Qwen 3.5 9B (4-bit) on MLX Serve, 32K context, on a 24 GB Mac | the eight Meridian agents with one to three tools each, the nine stores the scripts use, the labelled files | 1–8, 13, 14, 16, 18, 19, 21, 22 (part one), 25 (steps 1–6); 35 (needs an unsigned pack repository, not built; not tested) |
| **Standard** | DeepSeek V4.1 Flash through OpenRouter for the writer, canvas, CEO and helpdesk, standing in for a 27B-class local model | the presenter, the writer with its customer-notice playbook, canvas, the agent CEO and its organisation, the two workflows, the evals, the demo scripts | 0, 9–12, 15, 17, 23, 27; 34 (needs Snowflake or Databricks, not tested); 36 (needs a Microsoft 365 tenant, not tested) |
| **Full** | Gemini 3.7 Flash through OpenRouter for the librarian, the data analyst and Claude Code, standing in for a 70B-class model or a frontier provider | the sample workshop agents, the sample stores, the demo-data and demo-sql MCP servers and the column catalog, the firmware docs and the safety review skill | 20, 22 (part two), 24, 26, 28–30, 31–33 (with Claude Code, continuing from 24; 32 also needs a pack with a pre-send hook, not tested), and the builder workshop |

**Measured on 2026-09-29/30.** Essentials: every scenario in the row ran end to end three times
in a row on the 9B with every step passing, and `scripts/bench.py --level essentials` passed all 18
checks 10 of 10. Scenario 25's step 7 did not work on the 9B. Standard, with the agents above on
DeepSeek: 0, 9, 10, 11, 12, 15, 17 and 27 passed end to end; 23 built, drafted and saved the skill,
and its eval gate held because the evals ran on the host's 9B default (see the note in 23). On the
9B alone, 0, 10 and 11 also passed; the rest of Standard did not. Full, on Gemini: 20, 24, 28, 30,
31 and 33 passed end to end; 22 part two passed but for the clarifying question, which the local
decision model did not ask; 26 passed but for one column left over from an earlier run; 29 passed
once its label was read as *Governed or Mixed*. Steps that need Claude Code's spend (31), seven
days (29), a provider admin key (33) or a live tenant (34, 36) were not run.

The boundaries come from measurement, not taste: on a 9B a single tool with ten actions was
already unreliable, so nothing at Essentials has more than three one-action tools, and the
presenter and the CEO — long prompts, many actions — wait for Standard. Standard and Full were
measured on small cloud models; no 27B or 70B local model was measured for this release, so treat
those rows as the size the scenarios need, not a promise about a particular local model.
`scripts/bench.py` runs every scripted call of a level against the model your host serves and
says, check by check, whether that level operates on it.
