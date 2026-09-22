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
2. As Sam, IDE tab → `bundles/aiso-demo-pack/it-runbooks/vpn-reset.md`: change the first step so it no
   longer says to revoke the old certificate. Save. Knowledge → `it-runbooks` → *Re-index* (a few
   seconds; only the changed file is embedded).
3. As Dana, *Run* the helpdesk evals again: the VPN case fails on the missing phrase. Point at the
   check detail.
4. Undo the change, re-index, run once more: green.

**Land:** knowledge and prompts change every week; evals turn "we think it still works" into a
number on a page, and the run is audited.

---
