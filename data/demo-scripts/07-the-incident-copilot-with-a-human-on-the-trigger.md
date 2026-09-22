---
type: scenario
title: "7. The incident copilot, with a human on the trigger"
tags: ["scenario-7"]
level: essentials
---
**Level:** Essentials.


*An agent that can act, and the approval that stands between it and the action.*

**You are** Dana. Two windows help: one for the chat, one for Approvals. *Needs room:* the incident
record, the access review and the revoke call together exceed 4096 tokens.

1. `security-lead`: **"What is still outstanding on INC-2026-021, and who is responsible?"** The
   agent reads the incident record and the access review and lists the open actions.
2. **"Revoke the access of the contractor holding badge 4471, reason INC-2026-021."** The agent calls
   `revoke_access`. The run pauses and an approval card appears in the chat: the tool, the arguments
   as the agent proposed them, a hash of them.
3. In the other window, Approvals (or the card itself): *Approve*, with a note. The run resumes, the
   function records what it would have done, the agent confirms.
4. Admin → Audit, filter `tools.approval`: requested, granted, with the approver as actor and the
   arguments hash. Point out `tools.fragment.yaml` in the pack: three lines made this tool
   approval-gated for every agent that has it.

**Land:** agents can be given real actions because the action waits for a person, the arguments cannot
change between approval and execution, and both halves are on the record.

---
