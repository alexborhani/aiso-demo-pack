---
type: scenario
title: "41. Plan first, then the change"
tags: ["scenario-41"]
level: standard
---
**Level:** Standard: the `runbook-editor` agent, five tools (the runbook search, three sandbox file
tools and a to-do list). Measured: pending (new in 1.16.0); its bench check is `plan-first`.


*An agent that can change files shows its plan first, works through a to-do list once the plan is
approved, and its changes can be taken back by rewinding the conversation.*

**You are** Sam. The sandbox file tools work only under `/tmp` on the host; this scenario writes
`/tmp/meridian/halden-outage-checklist.md`.

1. Agents → `runbook-editor`. The header says **Plans first**: its definition has `planMode: required`.
   Ask: **"Turn the plant network outage runbook into a checklist for the Halden night shift, saved as
   /tmp/meridian/halden-outage-checklist.md."** The agent searches the runbooks and replies with a plan:
   numbered steps, which tool each uses, what could go wrong. Nothing is written yet: during the planning
   turn the tools that change things (`sandbox_file_write`, `sandbox_file_patch`) are withheld. The card
   under the reply reads *A plan, not yet carried out*.
2. **Approve and run.** The next turn runs with every tool and the plan in the agent's instructions. Its
   to-do list shows in the reply and ticks off as it goes; it writes the file: call the plant
   supervisor first, check the fibre link and the floor cabinet UPS. Admin → Audit, `plan.approved`.
3. **"Add a step before calling the supervisor: write the time of the outage in the shift log."** It plans
   again (this agent plans every request); approve. It reads the file and changes it with
   `sandbox_file_patch`, a list of exact edits that is applied whole or not at all.
4. Rewind the conversation to before step 3. The Studio has no Rewind control yet (measured: pending);
   the route is `POST /api/transcripts/<conversation id>/rewind` with `{"at": <seq>}`, the last message to
   keep. The conversation loses step 3's turns, the model forgets them, and the file is put back as step
   2 left it: before the patch, AI Stackops had kept what the file held. Admin → Audit, `transcript.rewind`
   and `sandbox.restore`: the paths and counts, never the content.

**Land:** an agent that changes things can be made to show its working first, and what it changed can be
undone with the conversation. It edits only inside the sandbox, never the host's own files.

---
