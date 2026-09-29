---
type: scenario
title: "32. A check before code leaves"
tags: ["scenario-32"]
level: full
---
**Level:** Full, with Claude Code, continuing from scenario 24. **Needs:** a certified pack that
carries a `gateway.before_call` decide hook; not tested. The demo pack carries no hook (by decision;
`drafts/platform/NOTES.md` §5c drafts the one it could ship), and the product's own test pack for
this lives only in its test suite.


*A pack the organisation trusts reads what a coding tool is about to send to a cloud model, and
can stop it.*

**You are** Dana in the Studio, Sam in the terminal.

1. As Dana, Admin → Policy → **Packs**: the pack's `presend-secrets` hook on `gateway.before_call`,
   mode decide, **off: not consulted**. Switch it on. The confirmation says what it reads: *the new
   text of every developer call to a cloud model (prompts and code) and may stop it.* Switch on.
2. As Sam, in the clone, on the cloud id: **"Why does this fail? AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
   is set in the build."** Refused before it leaves, with the pack's reason: a cloud call carrying
   what looks like a cloud access key. Nothing reached the provider.
3. The same question without the key goes through. Admin → Audit: `gateway.refused` names the pack,
   its version and the hook, never the text; the `gateway.call` row of the call that went out
   carries *allowed by* the hook.
4. Say what a stricter organisation does (shown, not run: the Studio's handling-rules table has
   no column for it yet): IDE tab → `classification.yaml` → `handling: internal: preSend: required`.
   Calls at that level then leave only when a pack said yes; with no hook switched on, every cloud
   call at that level is refused, and Admin → Setup fails the *pre-send check* line.
   `PACK_DECIDE=false` on the host stops every pack deciding.

**Land:** what leaves for a cloud model can be read first by a pack the organisation certified,
and stopped, with the refusal on the record and the text nowhere in it.

---
