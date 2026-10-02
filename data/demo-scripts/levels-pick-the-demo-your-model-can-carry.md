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
| **Essentials** | Qwen 3.5 9B (4-bit) on MLX Serve, 32K context, on a 24 GB Mac | the nine Meridian agents with one to three tools each, the nine stores the scripts use, the labelled files, the files for a person's own space | 1–8, 12, 13, 14, 16, 18, 19, 21, 22 (part one), 25 (steps 1–6), 37–40; 35 (needs an unsigned pack repository, not built; not tested) |
| **Standard** | DeepSeek V4.1 Flash through OpenRouter for the writer, canvas and helpdesk, standing in for a 27B-class local model | the presenter, the writer with its customer-notice playbook, canvas, the two workflows, the evals, the demo scripts, the runbook editor (plan mode) and the incident coordinator (sub-agents) | 0, 9–11, 15, 17, 23, 27, 41, 42; 34 (needs Snowflake or Databricks, not tested); 36 (needs a Microsoft 365 tenant, not tested) |
| **Full** | Gemini 3.7 Flash through OpenRouter for the librarian, the data analyst and Claude Code, standing in for a 70B-class model or a frontier provider | the sample workshop agents, the sample stores, the demo-data and demo-sql MCP servers and the column catalog, the change desk MCP server and its clerk, the firmware docs and the safety review skill | 20, 22 (part two), 24, 26, 28–30, 43, 31–33 (with Claude Code, continuing from 24; 32 also needs a pack with a pre-send hook, not tested), and the builder workshop |

**Measured on 2026-09-29/30.** Essentials: every scenario in the row ran end to end three times
in a row on the 9B with every step passing, and `scripts/bench.py --level essentials` passed all 18
checks 10 of 10. Scenario 25's step 7 did not work on the 9B. Standard, with the agents above on
DeepSeek: 0, 9, 10, 11, 15, 17 and 27 passed end to end; 23 built, drafted and saved the skill,
and its eval gate held because the evals ran on the host's 9B default (see the note in 23). On the
9B alone, 0, 10 and 11 also passed; the rest of Standard did not. Full, on Gemini: 20, 24, 28, 30,
31 and 33 passed end to end; 22 part two passed but for the clarifying question, which the local
decision model did not ask; 26 passed but for one column left over from an earlier run; 29 passed
once its label was read as *Governed or Mixed*. Steps that need Claude Code's spend (31), seven
days (29), a provider admin key (33) or a live tenant (34, 36) were not run.

**Measured on 2026-10-01 (1.14.0).** Scenarios 37–39 and the extended 19 ran end to end three times in a
row on the 9B with every step passing (the pack reinstalled before each pass), and the three new bench
checks (`space-answer`, `instructions`, `save-to-space`) passed 10 of 10 each. The other checks and
scenarios were not re-run for 1.14.0. Spaces at Standard and Full: measured: pending.

**Measured on 2026-10-01 (1.15.0).** Scenario 12 (*Work on a schedule*) ran end to end three times in a
row on the 9B with every step passing (one install, the schedule deleted at the end of each pass), and
the new bench check `schedule-run` passed 10 of 10. Nothing else was re-run for 1.15.0: the release
removes the organisation and its two CEO agents and adds no other agent, store or step.

**1.16.0 (2026-10-02): measured: pending.** This release adds scenarios for the harness work in AI
Stackops (main 222c921): 7's step 5 (an approval card that outlives a restart), 40 (a shared space),
41 (plan mode, a to-do list, sandbox files and a rewind), 42 (sub-agents) and 43 (an MCP server that
asks the person, and asks the host's model). None of them, and none of the earlier scenarios, has been
run on the reference models for this release. Every result above was measured before the answer
checks moved into turn hooks, before context was counted in tokens and before conversations moved into
the database; they describe the product as it was on those dates. The harness scripts and bench checks
for the new scenarios exist (`space-shared`, `plan-first`, `subagents`, `elicitation`,
`sampling-off`); their results on the Essentials, Standard and Full models are still to come.

The boundaries come from measurement, not taste: on a 9B a single tool with ten actions was
already unreliable, so nothing at Essentials has more than three one-action tools, and the
presenter — a long prompt, many actions — waits for Standard. Standard and Full were
measured on small cloud models; no 27B or 70B local model was measured for this release, so treat
those rows as the size the scenarios need, not a promise about a particular local model.
`scripts/bench.py` runs every scripted call of a level against the model your host serves and
says, check by check, whether that level operates on it.
