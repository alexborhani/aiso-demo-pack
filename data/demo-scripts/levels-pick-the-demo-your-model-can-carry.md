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
| **Essentials** | Qwen 3.5 9B (4-bit) on MLX Serve, 32K context, on a 24 GB Mac | the eight Meridian agents with one to three tools each, the nine stores the scripts use | 1–8, 13, 14, 16, 18, 19, 21, 22 |
| **Standard** | Claude Haiku 4.5 through OpenRouter, standing in for a 27B-class local model | the presenter, the writer with its customer-notice playbook, canvas, the agent CEO and its organisation, the two workflows, the evals, the demo scripts | 0, 9–12, 15, 17, 23 |
| **Full** | Claude Haiku 4.5 through OpenRouter, standing in for a 70B-class model or a frontier provider | the sample workshop agents, the sample stores, the demo-data MCP server, the firmware docs and the safety review skill | 20, 22 (part two), 24, and the builder workshop |

The boundaries come from measurement, not taste: on a 9B a single tool with ten actions was
already unreliable, so nothing at Essentials has more than three one-action tools, and the
presenter and the CEO — long prompts, many actions — wait for Standard. Standard and Full were
measured on a small cloud model; no 27B or 70B local model was measured for this release, so treat
those rows as the size the scenarios need, not a promise about a particular local model.
`scripts/bench.py` runs every scripted call of a level against the model your host serves and
says, check by check, whether that level operates on it.
