---
type: scenario
title: "12. Work on a schedule"
tags: ["scenario-12"]
level: essentials
---
**Level:** Essentials.


*An agent that runs on its own, as the person who set it up, and stops when that person goes.*

**You are** Sam in one window, Dana in the other.

1. As Sam, Agents → `helpdesk` → *Schedule…* in the chat header (or Activity → Schedules → *New
   schedule*). Name **"Weekly VPN digest"**; *What to ask it*: **"Write this week's helpdesk digest:
   how to reset a VPN certificate, in three bullet points from the IT runbooks."**; *Every week*,
   Monday, 09:00, your time zone. *Create schedule*. Activity → Schedules lists it: *Mondays at
   09:00*, when it runs next, *Active*.
2. *Run now* (the bolt). Activity → Runs shows a `helpdesk` run under Sam. When it ends the row says
   *Last: Completed*; open the row for its run history, and *Open in Activity* for the digest, built
   from the VPN runbook.
3. As Dana, Admin → People → Users → Sam → disable. Activity → Schedules → *Everyone's* → Sam's
   schedule → *Run now*. The run is *Skipped*: its owner is disabled. It never runs as Dana, and
   never as the system. Enable Sam again.
4. As Dana, Admin → Audit, filter `schedules.`: `schedules.create` and `schedules.run_now` by Sam,
   `schedules.run_now` by Dana, and `schedules.run` as Sam twice: the run that completed, then the
   skip with its reason.
5. As Sam, delete the schedule (it asks first); its run history goes with it.

**Land:** a timer here is not a service account. A schedule acts as the person who saved it, with
their access, limits and approvals, checked again every time it fires, and every change and every
firing is in the audit log.

---
