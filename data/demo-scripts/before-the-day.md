---
type: guide
title: "Before the day"
tags: []
---
**Install and prepare (once, about 30 minutes)**

1. Install or update AI Stackops on the Mac (the deploy kit installs AI Stackops only; the engine is
   MLX Core, run separately). Give the engine at least a 16K context, 32K on 24 GB or more: in MLX
   Core's settings, or `--ctx-size 32768` if you start `mlx-serve` yourself. This is not optional:
   the engine's own default of 4096 tokens is enough for a chat, not for an agent with tools and
   retrieved documents. The scenarios marked *needs room* fail with "prompt exceeds maximum context
   length" or take minutes at 4096. Load Qwen 3.5 9B (`mlx-community/Qwen3.5-9B-MLX-4bit`) and an
   embedding model (`bge-small` or `Qwen3-Embedding-0.6B`).
2. Sign in as the first admin. Admin → Estate → **Licence**: paste the demo Enterprise key (issued
   by AI Stack Ops for the demo). The Licence panel shows the edition, the people and nodes used and
   the date it ends. On the Free edition the pack still installs, but the chargeback export and the
   evidence bundle's projects section (scenarios 18, 24 and 33) say *edition required*.
3. Packs → *Install* → `https://github.com/alexborhani/aiso-demo-pack`, and pick the level your
   model carries (above). Copy the six passwords from the dialog into a password manager: Dana
   (admin), Sam (builder), Priya, Marcus, Lena (members with roles), Jordan (contractor, public
   only). *Reset passwords* on the pack card mints new ones at any time.
4. Knowledge tab: the pack's stores index on install. Check each shows *indexed* (a few minutes in
   total on the local embedding model). The HR and finance stores are listed only to the people
   whose roles open them, so sign in as Marcus and Lena to see those two.
5. Models tab: the default chat entry is the engine's Qwen 3.5 9B and the embedding entry is the
   engine's embedding model. Nothing else is required. Scenario 15 adds a cloud entry live.
   Scenarios 16, 22 and 24, and Standard and Full on a small Mac, are stronger with the cloud entry
   below, added once; without it they run on the local model.

   *The cloud entries.* Two, one per level, the ones this release was measured on. Models tab → the
   OpenRouter tab → **New entry**. **Name** `deepseek-flash` (the scenarios and agents refer to the
   entries by these names; a new entry is named after its model until you type one), model
   `deepseek/deepseek-v4.1-flash`, key `${OPENROUTER_API_KEY}` (the key in the host's environment or
   the secret store, never in the file), Max Tokens 4096, Thinking budget 0, access minimum role
   **member** (Priya asks the questions; a new cloud entry starts admin-only), classification
   ceiling **internal** (the runbooks are internal; the firmware safety code, confidential, stays
   off it), pricing from the model's OpenRouter page on the day (0.30 / 1.20 per million when
   measured), and USD / day **1**. Save. Then **New entry** again: name `gemini-flash`, model
   `google/gemini-3.7-flash`, the same key, access and ceiling, its own pricing (0.75 / 3.75 when
   measured) and USD / day **1**. That dollar a day per entry is the demo's own fence: a rehearsal
   and a run share it, because the window is a rolling 24 hours. Make neither the default; the
   scenarios switch agents to them live. From then on the provider's tab lists each entry by name
   above the form: pick one there to edit it (scenario 16 changes `deepseek-flash`'s budget).
   *Standard and Full on a 9B-class Mac.* Keep the local model as the default and give the cloud
   entries only to the agents those levels add: for Standard, Agents → `writer`, `canvas`
   and `skill-builder` (added the first time Skills → *New skill* is opened) → Model
   → `deepseek-flash`; for Full, `music-librarian`, `data-analyst` and the workshop agents → Model →
   `gemini-flash`. The finance, HR, legal and security agents and the presenter refuse cloud models
   by policy (their `egress` says so), so they stay on the local model whatever the default is; a
   cloud default would stop them, and the eval judge too.
6. Admin → Policy → **Answer checks**: leave the checks on, and set *Model for decisions* to the
   local chat entry. The second-model judge and the grades (scenario 22) then run on the local model,
   where the engine returns token probabilities; nothing about an answer leaves the Mac to be judged.
7. On a 24 GB Mac, load only what the day needs: the chat model and the embedding model, and the
   voices only for scenario 0. The models, the engine's prompt cache and a browser fill 24 GB;
   once the Mac swaps, a reply that takes seconds takes minutes. Close other large apps, and start
   a scenario only when the Knowledge tab shows every store *indexed*: the engine serves requests
   side by side, and a chat slows while a store is still embedding.
8. Open the Studio in two browser profiles (or one normal and one private window) so you can be Dana
   in one and another person in the other without signing out. Scenario 14 needs a third window with
   no session at all.
9. For scenario 24 and the ones that continue from it (31, 32, 33; all Full): Claude Code on the
   Mac, the `ai-stackops` command on the PATH (the same binary the host runs), and a clone of
   `https://github.com/alexborhani/meridian-pump-controller` in a folder of its own. Scenario 28 needs
   the `ai-stackops` command too.

**The people you will be**

| Sign in as | Tier and roles | Clears | Use them for |
| --- | --- | --- | --- |
| Dana | admin | restricted, every category | policy, approvals, audit |
| Sam | builder, firmware-engineers | internal, and confidential Security | building: agents, workflows, skills, schedules, the IDE, the firmware repository |
| Priya | member, staff | internal | the everyday employee |
| Marcus | member, staff, hr-partners | confidential within HR | people questions |
| Lena | member, staff, finance-analysts | confidential within Finance | finance questions |
| Jordan | member, contractors | public | the outsider inside the building |

**Reset between runs** is at the end of this document. The whole pack can be uninstalled and
reinstalled in under five minutes, which returns every account, store and policy to the starting state.

---
