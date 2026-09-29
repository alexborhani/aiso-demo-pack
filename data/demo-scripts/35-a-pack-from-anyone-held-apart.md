---
type: scenario
title: "35. A pack from anyone, held apart"
tags: ["scenario-35"]
level: essentials
---
**Level:** Essentials. **Needs:** a small unsigned pack in a git repository of its own; not built
(`drafts/platform/NOTES.md` §7 lists what it holds), so not tested.


*Capability can come from any git repository, not only from signed publishers. What the platform
lets an unknown publisher's pack do is the point.*

**You are** Dana.

1. Packs → *Install* → the unsigned pack's git URL → *Inspect*. The card: **community**, unsigned,
   publisher unknown. Say: anyone can publish a pack; nobody vouched for this one.
2. Install it. Admin → Policy → **Packs**: its hook is listed with **runs isolated**: its code runs
   in a separate process with no network, no files and no modules, and is stopped after 30 seconds.
   Say the limit out loud: only hooks run this way; a function a pack offers agents as a tool loads
   in the server like any other, which is one more reason to install community packs with care.
3. What it may not do, and the install dialog would refuse if it tried: seed accounts or roles,
   read the audit log or usage, or decide anything in a person's place (decisions are for certified
   packs only).
4. Packs → *Trusted publishers* → *Minimum tier to install*: **pack — signed by a trusted
   publisher** (it saves when chosen). Inspect it again: *Install* is off, and the reason says the
   host no longer accepts community packs. Set it back to **community**.
5. Uninstall it. Admin → Audit: `packs.install` (its metadata: tier *community*, verification
   *unsigned*), `packs.trust` twice, `packs.uninstall`.

**Land:** packs install from any git repository; the hooks of one whose publisher nobody trusts run
held apart and reach no people, no records and no decisions, and an admin can refuse unsigned packs
estate-wide in one setting.

---
