---
type: scenario
title: "31. A project's budget, its background calls, and a second admin"
tags: ["scenario-31"]
level: full
---
**Level:** Full, with Claude Code. Needs what scenario 24 needs (Claude Code, `ai-stackops`, the
clone, the project `pump-controller` from scenario 24 step 1), and the host's first admin account
(the one made at install) as the second admin. Measured: the API steps passed; the Claude Code spend
    steps (2–3) were not run.


*A development project has its own money: a pool, a share per person, and a rule for what happens
when it runs out. Loosening any of that takes a second admin.*

**You are** Dana and the first admin in the Studio (two browser profiles), Sam in the terminal.

1. As Dana, **Projects** → `pump-controller` → **Overview** → *Budget*: *Project, USD per day*
   **0.03**, *When the budget runs out*: **Move background calls to a local model**. Save.
   Tightening applies at once. Point at *Each member, USD per day*: the same cap per person inside
   the pool (left empty here, so the pool is what runs out). (The stand-in is the project's local id,
   `claude-local-qwen`; the `mlx-serve` entry must carry no pricing, or it spends the same budget.)
2. As Sam, in the clone: `claude`, `/model claude-haiku-4-5`, and ask for a few small changes
   until the spend passes three cents. From then on Claude Code's background calls (conversation
   titles, summaries, compaction) are moved to the local model instead of failing, and his next
   main call is refused: *Limit reached: $0.03 per day for project pump-controller (used
   $0.03). It frees up as the rolling 24 hours pass; an admin can raise it in the project's budget.
   Local models do not count against it: switch to claude-local-qwen.* `/model claude-local-qwen`
   and carry on. Nothing about the project stopped.
3. As Dana, Admin → Audit: `gateway.downgraded` (from the cloud id to `claude-local-qwen`, request
   class *auxiliary* or *compaction*, the budget as the reason; one row per person every five
   minutes, repeats counted) and `gateway.refused` for the main call. Admin → Setup → *Since your
   last visit*: *Project pump-controller has spent 8x % of its daily budget*, then *… has spent its
   daily budget ($0.03 of $0.03)* (the project's name as created in scenario 24).
4. Make it permanent for background work: Projects → `pump-controller` → **Models** →
   `claude-haiku-4-5` → **By kind** → *auxiliary*: `mlx-serve`, *compaction*: `mlx-serve` → **Save
   models**. Now background calls run locally whatever the budget; only the work itself goes to the
   cloud model. The project's **Usage** → *By: Kind of request* shows the split after a few turns.
5. Now loosen it. **Overview** → clear *Project, USD per day* (no daily cap). Save. The toast: *This
   change weakens the project, so it waits for a second admin. It is listed under Changes waiting.*
   The project still has its cap. The box *Changes waiting for a second admin* lists it with the
   reason, in words: *the project's daily dollar cap removed*. Dana's own **Approve** is refused:
   *A change that weakens a project needs a second admin: someone other than the person who asked
   must decide it.*
6. As the first admin, **Projects** → `pump-controller`: the same change, asked by Dana. **Approve**:
   *Approved and applied.* Admin → Audit: `project.change.request` by Dana, `project.change.approve`
   by the first admin. Say what else waits for a second admin: a lower level, a cloud route added, a
   30-day cap above $1,000, a restored project, a later end date, wider networks, more docs for the
   agents, looser code rules. (Raising a daily dollar cap does not.)

**Land:** a project spends what it was given, its background work falls back to the local model
instead of stopping, and nobody loosens its rules alone.

*Reset:* restore the daily caps (tightening applies at once), *When the budget runs out* back to
*Refuse paid calls*, the *By kind* routes back to *same as the id*.

---
