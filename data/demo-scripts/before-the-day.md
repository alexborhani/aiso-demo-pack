---
type: guide
title: "Before the day"
tags: []
---
**Install and prepare (once, about 20 minutes)**

1. Install or update AI Stackops on the Mac and give the engine a 16K context. With the macOS deploy
   kit that is `sudo ./install.sh --orcha <binary> --ctx-size 16384` (32768 is fine on 24 GB or more);
   otherwise pass `--ctx-size 16384` to `mlx-serve`. This is not optional for the full set: the
   engine's own default of 4096 tokens is enough for a chat, not for an agent with tools and
   retrieved documents. Every scenario below was exercised against the real engine; the ones marked
   *needs room* fail with "prompt exceeds maximum context length" or take minutes at 4096 and are
   written for 16K.
2. Sign in as the first admin, then Packs → *Install* → `https://github.com/alexborhani/aiso-demo-pack`,
   and pick the level your model carries (above).
   Copy the six passwords from the dialog into a password manager: Dana (admin), Sam (builder),
   Priya, Marcus, Lena (members with roles), Jordan (contractor, public only). *Reset passwords* on
   the pack card mints new ones at any time.
3. Knowledge tab: index `handbook`, `it-runbooks`, `people-files`, `finance-close`,
   `security-incidents`, `legal-matters`, `all-hands`, `site-notes`, `product-faq`, `scratchpad`.
   Ten stores, a few minutes in total on the local embedding model.
4. Models tab: confirm the default chat entry is the engine's Gemma and the embedding entry is
   `bge-small`. Nothing else is required. Scenario 15 adds a cloud entry live. Scenario 16 is
   stronger with the cloud entry below, added once; skip it and the scenario runs on the local model.

   *Scenario 16's Claude entry.* Models tab → Anthropic, name `claude-haiku`, model
   `claude-haiku-4-5-20251001`, key `${ANTHROPIC_API_KEY}`, Max Tokens 2048, Thinking budget 0,
   access minimum role **member** (Priya asks the questions; a new cloud entry starts admin-only),
   classification ceiling internal (the runbooks are internal), pricing 1 / 5 per million, and
   USD / day **1**. Save. That dollar a day is the demo's own fence: a rehearsal and a run share it,
   because the window is a rolling 24 hours. Do not make it the default and leave `helpdesk` on
   `default`; the scenario switches it live. Keep to Haiku 4.5 or a 4.6 model here: the helpdesk
   sends a temperature, and Sonnet 5, Opus 4.7 and later refuse one.
5. Open the Studio in two browser profiles (or one normal and one private window) so you can be Dana
   in one and another person in the other without signing out. Scenario 14 needs a third window with
   no session at all.

**The people you will be**

| Sign in as | Tier and roles | Clears | Use them for |
| --- | --- | --- | --- |
| Dana | admin | restricted, every category | policy, approvals, audit, the CEO |
| Sam | builder | internal | building: agents, workflows, the IDE |
| Priya | member, staff | internal | the everyday employee |
| Marcus | member, staff, hr-partners | confidential within HR | people questions |
| Lena | member, staff, finance-analysts | confidential within Finance | finance questions |
| Jordan | member, contractors | public | the outsider inside the building |

**Reset between runs** is at the end of this document. The whole pack can be uninstalled and
reinstalled in under five minutes, which returns every account, store and policy to the starting state.

---
