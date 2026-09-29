---
type: scenario
title: "28. The model stays put until you move it"
tags: ["scenario-28"]
level: full
---
**Level:** Full (the kept answers come from the music librarian, which needs the demo-data server).
Needs the `ai-stackops` command on the Mac (as for scenario 24) and both cloud entries from *Before
the day* (`claude-haiku` and `deepseek-flash`). Not yet run (measured: pending).


*A model that changes under an organisation changes its answers. Here the model is pinned, a
change is refused, and the switch is tested on the answers people kept before anyone makes it.*

**You are** Dana. **Windows:** the Studio and a terminal. Best after scenario 22 part two, whose
kept answer is replayed here too. Enforcement on Monitor or Off, as for scenario 22 part two.

1. IDE tab → `models.yaml` → the `mlx-serve` entry under `llm`: replace `model: mlx-serve` with the
   model's own name, `mlx-community/Qwen3.5-9B-MLX-4bit`, and add `pinned: true`. Save. Models tab →
   MLX Serve: the chat entry carries a lock and **pinned**. Say: this is the model every agent
   without a model of its own answers with, and from now on nothing moves it by accident. (The name
   matters: the `mlx-serve` alias follows whatever the engine serves, which no pin can hold.)
2. Models tab → the OpenRouter tab → pick `claude-haiku` → **Make default**. Refused: *llm.mlx-serve
   is pinned: "default" currently resolves to it; re-pointing to "claude-haiku" would replace the
   pinned model. Unpin it first (pinned: false) to make this change.* Admin → Audit, action
   `models.pin.bypass`: one row, outcome denied, reason *config-write: …*, Dana as the actor. Say:
   the same refusal meets an edit of `models.yaml` that changes the pinned model, a federation
   setting that would send the work to another node, and a router that would escalate.
3. As Dana, `music-librarian`: ask three questions and **Keep** each answer with a title (the
   reply's Sources line → **Keep** → title → **Keep and sign**):
   **"Find the 5 longest tracks in the catalog"** (title *Longest tracks*),
   **"Which artists have tracks in both Rock and Jazz?"** (*Rock and Jazz*),
   **"What has customer Heather Leacock purchased, and how much did she spend in total?"**
   (*Heather Leacock*). Account → *Kept answers* lists them, with scenario 22's if it ran.
4. In the terminal, with the host's workspace, ask whether the librarian could move from
   `claude-haiku` to the cheaper `deepseek-flash`:
   `WORKSPACE=<the host's workspace> ai-stackops eval --from-kept --model deepseek-flash --agent music-librarian`
   Each kept answer is given to `deepseek-flash` with the librarian's instructions, the question
   and the results it was built from (no query runs again), and checked and graded like a live
   answer. One line per answer: `SAME`, `BETTER` or `WORSE`, its title, the grade before and
   after, and under a worse one the figure the candidate gave that the results do not hold
   (*not in the results: …*) or a figure the kept answer gave and the candidate dropped (*no
   longer given: …*). The last line counts them.
5. Read out the answers that came back worse, by title. Say: this is the release test for a model
   change. It exits non-zero when anything got worse, so it can gate a change the same way the
   evals in scenario 17 do. Run it again with `--model mlx-serve`: the same question of the pinned
   local model. This is how you find out which work can move to open weights, before moving it.
6. To make a switch for real: point the librarian at the model that passed (Agents →
   `music-librarian` → Model), or, for the default, set `pinned: false` and the new model in one
   edit of `models.yaml`. Neither happens by itself.

**Land:** the model under an agent changes only when an admin changes it, and the change is tested
against the answers people kept before it is made, with the ones that got worse named.

*Reset:* IDE tab → `models.yaml` → the `mlx-serve` entry: `pinned: false` and `model: mlx-serve` in
one edit (an edit that drops `pinned` and changes the model together is refused), then remove the
`pinned` line. Kept answers stay.

---
