---
type: scenario
title: "9. A customer notice by the playbook: drafted, signed off, filed"
tags: ["scenario-9"]
level: standard
---
**Level:** Standard.


*A procedure the organisation wrote down once, followed by an agent every time: it asks for what
it needs, drafts in house style, and waits for a person before anything goes on the record.*

**You are** Sam (builder) in one window, Dana in the other for the sign-off.

1. As Sam, `writer`: **"Draft a customer notice about the 2027 price list."** It asks for the
   effective date before drafting anything: the playbook declares it as a required input, and a
   required input is asked for, never guessed.
2. **"1 November 2026, for all customers."** Open the tool trace under the reply: the writer loaded
   two skills by itself, `house-style` and `customer-notice` (`load_skill`), because the request
   matched their descriptions, and read the playbook's `references/notice-rules.md`. The canvas
   opens with the notice: what changes, from when and for whom in the first three lines, clause 7.2
   and the 30 days' notice, the service desk as the contact.
3. **"File it."** The writer calls `knowledge_add`, and the run pauses: an approval card, because
   the playbook says filing a customer notice needs an administrator, and a different person from
   the one who asked. Sam cannot approve it.
4. As Dana, Approvals: the card names the tool, the title and the store. *Approve*, with a note.
   The run resumes; Knowledge → `scratchpad` → *Sources*: the notice, added by Sam. Admin → Audit:
   `skills.loaded` (which skills, which version), `tools.approval.requested` and `.granted`, and
   `knowledge.add` with the title and never the text.
5. Skills tab → `customer-notice`: the playbook as the organisation wrote it: the inputs, the
   approval and who gives it, the *Done when* list, the reference file.

**Land:** a procedure the organisation wrote down once, not a prompt someone remembered: the agent
asks for what it needs, follows the house rules, and the step that matters waits for a person.

---
