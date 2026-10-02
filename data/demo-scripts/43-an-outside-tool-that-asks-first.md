---
type: scenario
title: "43. An outside tool that asks first"
tags: ["scenario-43"]
level: full
---
**Level:** Full: the `change-desk` MCP server (a small Node script in the pack, no dependencies, nothing
on the network) and the `change-clerk` agent. **Needs:** Node on the server's path, as `demo-data`
needs `npx`. Measured: pending (new in 1.16.0); its bench checks are `elicitation` and `sampling-off`.


*An outside system can stop and ask the person something while it works, and can ask for a model's help,
but only if an admin allowed it.*

**You are** Sam; Dana for steps 4 and 5.

1. As Sam, `change-clerk`: **"File a change on MW-300 Halden line 2: set the interlock timer back to
   400 ms, because the 250 ms setting caused nuisance trips."** The clerk calls the desk's
   `request_change`, and the desk asks Sam directly: a card in the reply with a box to tick (*File this
   change request*) and a change window. Only Sam sees it, and it waits five minutes.
2. Tick the box, pick *Saturday 06:00*, submit. The desk files it and the clerk gives the ticket number,
   CHG-2026-0521 or the next one. Ask again and **Decline** the card: nothing is filed, and the clerk
   says so. Say: what Sam typed went to that tool only and is not kept.
3. **"Summarise the change log of MW-300 Halden line 2."** The desk asks AI Stackops for a model to write
   the summary, and is refused: the pack ships the server with `sampling: { allow: false }`. The clerk
   returns the log as it is, four tickets from CHG-2026-0412 to CHG-2026-0503.
4. As Dana, IDE tab → `mcp.json` → the `change-desk` entry: `"sampling": { "allow": true, "maxTokens": 512 }`.
   Save (it needs permission to manage MCP servers). As Sam, ask for the summary again: this time it is
   written, by the default chat model, as Sam: his access, his budget, his clearance.
5. Admin → Audit: `mcp.elicitation` (asked, with the field names), `mcp.elicitation.answered` (the answer,
   never the values), `mcp.sampling` denied with its reason, then `mcp.sampling` success with the model
   entry and the token counts, never the text. Set `allow` back to `false`.

**Land:** outside tools can hold a real conversation with the person and borrow a model, and each of those
is something the organisation switched on, answered by the right person, and recorded.

---
