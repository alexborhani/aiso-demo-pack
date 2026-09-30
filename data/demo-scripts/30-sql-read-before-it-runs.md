---
type: scenario
title: "30. SQL read before it runs"
tags: ["scenario-30"]
level: full
---
**Level:** Full: the `demo-sql` server (one free-SQL tool, `run_sql`, over a copy of the music
store) and the `data-analyst` agent come with that level. Standard-class model or better: writing SQL over an
unfamiliar schema is beyond what a 9B does reliably. Start on the cloud entry. Measured: passed on Gemini 3.7 Flash (it wrote a LIMIT
itself, so step 3's *Low* grade did not show; the refusal in step 4 did).


*Named queries are governed; free SQL is not. Here free SQL is offered only to builders, read
before it runs, refused when it is plainly wrong, and graded lower than a governed answer.*

**You are** Dana; Priya in the second window.

1. Tools → MCP: two servers over the same database. `demo-data`: every tool chipped **Governed**.
   `demo-sql`: one tool, `run_sql`, chipped **SQL · builders**. Say: the question is not whether a
   model can write SQL but who may ask it to, and what reads it first.
2. As Priya, `data-analyst` is not in her list (the agent is for builders). Open the agent's
   definition as Dana: `access: minRole: builder`, and even without that the SQL tool itself is
   withheld below builder. Members get named queries; builders get SQL.
3. As Dana, Admin → Policy → **Answer checks** → *When a query has a known mistake*: it is on
   **Run it and note the problem** (the default). `data-analyst`: **"Show me everything in the
   Track table."** A model asked that writes `SELECT * FROM Track` with no limit. It runs; under the
   reply, open the step: the statement, and under it a warning *SELECT * from Track with no LIMIT
   returns every row and column…*. The grade is **Low**, and its reasons name the query.
4. Switch it to **Refuse it**. Save. Ask the same question in a new chat. The query is refused
   before it runs, the model reads why (*this query was refused by the SQL check before it ran …
   Fix the query and run it again*), rewrites it with named columns and a LIMIT, and the second
   statement runs. Open the steps: the refused one, with the finding, marked failed; the one that
   ran, clean.
5. **"How much has each customer spent in total?"** The model joins invoices to invoice lines and
   sums. That is allowed, and the step carries a note: *The query sums or counts across a join …*.
   The Sources line says **Ad hoc**, not Governed, and the grade is **Medium** at best: *Figures
   come from SQL written for this answer, not a governed metric.* Compare scenario 22's Heather
   Leacock answer from a named query: Governed, High.
6. Set *When a query has a known mistake* back to **Run it and note the problem**.

**Land:** free SQL is a builder's tool, read before it runs; the plainly wrong shapes are sent back
to be fixed, and an answer built on SQL written on the spot says so in its label and its grade.

---
