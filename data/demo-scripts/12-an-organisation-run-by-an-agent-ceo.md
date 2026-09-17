---
type: scenario
title: "12. An organisation run by an agent CEO"
tags: ["scenario-12"]
---
*Tickets, a team of agents, and a CEO that triages and delegates on a heartbeat.*

**You are** Dana. Organisations → Meridian Works. *Needs room:* the CEO's prompt carries the whole
organisation (chart, open tickets, ten organisation tools), about 4,000 tokens before it says a word,
so this scenario needs the 16K engine; at 4096 the heartbeat fails with a context-length error, which
the CEO runs list shows as a failed run.

1. Open the board: eight tickets across backlog, to do, in progress, in review, blocked, done, each
   assigned to an agent: the helpdesk, the writer, the security lead.
2. Open a ticket: description, priority, activity. Create a new one: **"Riverside test rig guard
   interlock trips twice a shift"**, priority high, unassigned.
3. Press *Wake CEO* (the CEO's manual heartbeat). Watch Activity: the `meridian-ceo` agent reads
   the org context, the open tickets and the team, decides who should own the new ticket, updates
   statuses, and writes its reasoning as comments. The CEO run appears under CEO runs with its
   token count and cost.
4. Show the heartbeat schedule (every 30 minutes by default, off until an admin enables it) and the
   `org-ceo` skill that shapes how the CEO triages.

**Land:** the organisation object is where agents stop being chat windows and become a team with a
backlog, an owner and a cadence, with every decision written down.

---
