---
type: scenario
title: "23. Skills: built by interview, proven by evals, offered by policy"
tags: ["scenario-23"]
level: standard
---
**Level:** Standard (the skill builder needs a Standard-class model; on a 9B it drafts slowly and
unreliably).


*How a procedure gets into the platform: the person who does the work is interviewed, the draft is
checked, its evals decide whether it may be offered widely, and an admin decides where.*

**You are** Sam (builder), then Dana.

1. As Sam, Skills tab → **New skill**. The skill builder asks about the work one question at a time.
   Answer as a service coordinator: **"I handle warranty claims for the service desk. A customer
   reports a fault on a pump under warranty. I check the serial number and the purchase date, check
   the fault is covered (seals, bearings and the controller are; damage and misuse are not), and if
   it is, book a field engineer. Claims over 2,000 pounds need sign-off from the service manager.
   It is done when the claim is approved with a booking, or refused with the reason."** Then give
   two real examples and a near miss when it asks: **"Claim for MW-300 serial 0412, seal leak,
   bought March 2025"**, **"Is this pump covered? It is a controller fault"**, and the near miss
   **"How many warranty claims did we have last quarter?"**.
2. The builder says which form fits (a skill, a workflow, or a skill that starts one) and why, then
   drafts. Under the conversation: the draft file by file, `SKILL.md` with its inputs (serial
   number, purchase date, fault), the steps, a *Done when* list, and `evals/evals.yaml` built from
   the examples, the near miss marked *should not trigger*. Read the warnings: if the draft puts
   the manager's sign-off under approvals against a tool this workspace does not have, the check
   says it would pause nothing, and the builder asks which system books the engineer. Say: an
   approval is only real if it pauses a real tool; the checks will not let a draft pretend.
   **Save skill**: Sam owns it; its evals start.
3. Open the new skill: **Evals** shows the trigger cases (was the skill picked for the requests and
   left alone for the near miss) and the answers with the skill against without it, on the host's
   model. *Versions*: this one, with its fingerprint.
4. As Dana, Skills → `customer-notice` (the playbook from scenario 9) → **Where it is offered** →
   *Every agent* → Save. Refused while its evals have not passed on this version: *Run evals*
   (a few minutes), then save again. Say: a skill reaches every agent only when a person other
   than its author has reviewed it (a signed pack counts) and its evals pass, including a check
   that it does not take the requests of the skills already offered.
5. Admin → Audit: `skills.draft.save`, `skills.evals.run`, `skills.scope.set` with before and
   after.

**Land:** procedures come from the people who do the work, are tested before they spread, and reach
every agent only when an admin puts them there, with every step recorded.

---
