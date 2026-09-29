---
name: customer-notice
description: Draft a notice to Meridian customers about a change (prices, service intervals, parts, contacts), get it signed off, and file it on the record. Use when someone asks for a customer notice, a letter to customers or a customer announcement about a change.
inputs:
  subject:
    type: string
    required: true
    description: what changes, in a few words, e.g. "2027 price list"
  effective_date:
    type: string
    required: true
    description: the date the change takes effect, e.g. 1 November 2026
  audience:
    type: string
    default: all customers
    description: which customers it goes to, e.g. MW-300 owners
approvals:
  - before: knowledge_add
    approvers: { minRole: admin }
    separate: true
    reason: A filed customer notice is what the service desk quotes to customers; an administrator signs it off first.
done:
  - The notice says what changes, from which date and which customers it affects, in its first three lines
  - It gives the service desk as the contact (service@meridianworks.example, +44 1632 960 411)
  - A price change gives at least 30 days' notice before the effective date, or says why it cannot
  - It is filed in the scratchpad store with a title, or the person decided not to file it
---
# Customer notice

1. Load the house-style skill and follow it.
2. Read references/notice-rules.md before drafting. It holds the notice periods and the contract clause to cite.
3. Draft the notice on the canvas with canvas_write. Name the change, the effective date and the audience in the first three lines.
4. If a price change gives less than 30 days' notice, say so to the person and ask whether to go on.
5. Ask the person whether to file it. Only on a yes, file it in the scratchpad store with knowledge_add, titled "Customer notice: <subject>", with the request as the source. Filing waits for an administrator's approval; tell the person that.
