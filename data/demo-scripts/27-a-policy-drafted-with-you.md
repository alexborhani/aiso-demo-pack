---
type: scenario
title: "27. A policy drafted with you"
tags: ["scenario-27"]
level: standard
---
**Level:** Standard. Every step after the first needs a model: a long interview, a nine-section policy
in Markdown and one tool call with a nested schema. Measured: passed end to end on DeepSeek V4.1 Flash; on Qwen 3.5 9B it ran the interview and filed
a proposal but missed two of eight checks.


*An organisation with no written classification policy gets one by answering eight questions. The
agent proposes; an admin decides.*

**You are** Dana. Agent: `classification-onboarding`. The pack does not ship it yet, and the Studio
offers it only while no policy is adopted (the banner's *Draft one with the onboarding agent*). Before
the day, add it as Dana with `POST /api/admin/classification/onboarding/install`, or run this
scenario on a second install without the pack, where the banner shows. The Meridian policy stays in
force throughout.

1. Admin → Policy → Classification: the Meridian policy is adopted (*Adopted … by pack:aiso-demo-pack*).
   Say: this scenario plays a different company, a 60-person pump distributor in Aarhus with no
   written policy, and nothing it proposes is adopted here.
2. Agents → `classification-onboarding`: **"We have no written classification policy."** Answer its
   questions one at a time. Suggested answers: GDPR, no other regulator; customer contacts, employee
   records, prices and margins, service reports; no labels today; three levels, *public*, *internal*,
   *confidential*; members see internal, admins see everything; confidential never goes to a cloud
   model; categories *Customer* and *HR*; untagged means internal, reviewed every year.
3. It shows the full draft: purpose, roles, the three levels with examples, categories, labelling,
   handling rules per level, the default, review, audit. Ask for one change, for example "service
   reports are internal, not confidential". Then **"Submit it."**
4. It says where the proposal waits and that nothing is in force. Admin → Policy → Classification →
   **Proposals**: the summary, levels *public < internal < confidential*, the handling rules. *Read
   policy* opens the Markdown. The Approvals tab lists it too.
5. **Reject.** Say what *Adopt* would do: write the policy, replace the taxonomy, re-check documents
   against the new criteria, and replace the Purview mapping with what the proposal names. In this
   workspace that would drop the Meridian levels and the id rows scenario 25 relies on.

**Land:** a policy nobody had written becomes one draft and one decision. The agent cannot put
anything in force.

---
