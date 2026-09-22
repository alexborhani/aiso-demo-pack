---
type: guide
title: "Levels: pick the demo your model can carry"
tags: []
---
The pack installs at one of three levels, chosen on the install dialog and changeable later from
the pack card (agents above the level are removed, the people and the policy stay). Every scenario
below says which level it needs; the people, the stores of the essentials and the scripts are the
same at every level, so a story told at Essentials reads the same at Full.

| Level | Reference model | What it adds | Scenarios |
| --- | --- | --- | --- |
| **Essentials** | a 9B-class local model, 16K–32K context (Qwen 3.5 9B on a 24 GB Mac) | the eight Meridian agents with one to three tools each, the nine stores the scripts use | 1–8, 13, 14, 16, 18, 19 |
| **Standard** | a 27B-class local model at 32K (a 48 GB Mac or larger), or a cloud entry | the presenter, the writer and canvas, the agent CEO and its organisation, the two workflows, the evals, the demo scripts | 0, 9–12, 15, 17 |
| **Full** | a 70B-class model or a frontier provider | the sample workshop agents (architect, marketer, web engineer, sandbox, media) and the sample stores | 20, and the builder workshop |

The boundaries come from measurement, not taste: on a 9B a single tool with ten actions was
already unreliable, so nothing at Essentials has more than three one-action tools, and the
presenter and the CEO — long prompts, many actions — wait for Standard.
