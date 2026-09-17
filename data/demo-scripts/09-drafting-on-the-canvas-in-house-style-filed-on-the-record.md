---
type: scenario
title: "9. Drafting on the canvas, in house style, filed on the record"
tags: ["scenario-9"]
---
*Knowledge work with an output you can see, and an agent writing back into the estate under audit.*

**You are** Sam (builder).

1. `writer`: **"Draft the customer notice about the 2027 price change, effective 1 November, on the
   canvas in house style."** The canvas pane opens beside the chat with the rendered notice. The
   `house-style` skill shaped it: tone, structure, the sign-off.
2. **"Shorten it to three paragraphs and add the service-desk contact."** The canvas updates in place.
3. **"File it in the scratchpad store as '2027 price change notice'."** The agent calls
   `knowledge_add`. Knowledge → `scratchpad` → *Sources*: the new document, decided by a person,
   with who added it and when. Admin → Audit: `knowledge.add` names the title and the sources, never
   the text.
4. Knowledge → `scratchpad` → *Search* for "price change": the notice is retrievable by every agent
   that has the store.

**Land:** the canvas is where a leader sees the work; the audit is where the organisation keeps it.
An agent that writes into the estate does so with a name attached.

---
