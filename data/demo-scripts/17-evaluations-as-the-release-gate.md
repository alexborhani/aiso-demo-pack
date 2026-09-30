---
type: scenario
title: "17. Evaluations as the release gate"
tags: ["scenario-17"]
level: standard
---
**Level:** Standard.


*Change an agent's knowledge and know, before anyone notices, whether it still answers correctly.*

**You are** Sam for the change, Dana for the run.

1. Admin → Setup → *Evaluations*: `helpdesk.eval.yaml`, three cases, threshold 50 percent. *Run*.
   Each case shows pass or fail with its checks: a phrase that must appear, a phrase that must not,
   a judgement by the local model. Expect a pass.
2. As Sam, IDE tab → `bundles/aiso-demo-pack/it-runbooks/vpn-reset.md`: change the new certificate's
   validity from 12 months to 6 months. Save. Knowledge → `it-runbooks` → *Re-index* (a few seconds;
   only the changed file is embedded).
3. As Dana, *Run* the helpdesk evals again: the VPN case fails. Its pattern check expects the
   12-month validity the runbook used to give, and the agent now answers 6 months from the runbook.
   Point at the check detail: this is the eval catching a change in what the agent says.
4. Undo the change, re-index, run once more: green.
5. Skills carry their own evals, beside the skill (Skills tab → a skill → *Evals*): whether agents
   pick it for the requests it is for and leave it alone for near misses, and whether answers are
   better with it. Scenario 23 runs one.

**Land:** knowledge and prompts change every week; evals turn "we think it still works" into a
number on a page, and the run is audited.

---
