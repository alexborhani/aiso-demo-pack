---
type: scenario
title: "36. Microsoft 365, searched as you"
tags: ["scenario-36"]
level: standard
---
**Level:** Standard. **Needs:** a Microsoft 365 tenant, an Entra app registration with admin
consent (the `aso-o365` pack's SETUP.md), and the `aso-o365` pack; not tested. Written from the
pack.


*Mail, calendar, files and Teams searched by a local model, as the signed-in person, read-only.*

**You are** Dana to install, then Priya.

1. As Dana, Packs → *Install* → `https://github.com/alexborhani/aso-o365`: signed by AI Stack Ops,
   certified. The dialog asks for the tenant's client and tenant ids and the local folders. Its
   declared egress: `login.microsoftonline.com`, `graph.microsoft.com`, nothing else.
2. As Priya, Packs → the pack → *Your setup* → **Connect your Microsoft account**: a device code,
   signed in once with her Microsoft account. Admin → Audit: `identity.connect`.
3. `o365-assistant`: **"What did Marcus send me about the Riverside open day?"** One search across
   her mail, files and calendar, answered with each item's title and link, on the local model. It
   is her mailbox, read with her delegated token; nobody else's mail is reachable.
4. **"Reply to him and say yes."** It says it is read-only and offers a draft for her to send.

**Land:** a Copilot-style search over Microsoft 365 that runs on the organisation's own model, as
the person asking, and cannot send or change anything.

---
