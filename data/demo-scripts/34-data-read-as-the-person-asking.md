---
type: scenario
title: "34. Data read as the person asking"
tags: ["scenario-34"]
level: standard
---
**Level:** Standard. **Needs:** a Snowflake account with a managed MCP server (or Databricks, see
the note), an OAuth integration for AI Stackops, and two Snowflake users with different roles; not
tested. Written from the code (`drafts/platform/NOTES.md` §4 has the host config).


*The warehouse, not AI Stackops, decides what each person may see: the query runs under the
person's own sign-in. And a kept answer can be re-run against the data as it stood when it was
given.*

**You are** Lena and Marcus (two windows), then Lena again.

1. As Dana, Tools → MCP: the `snowflake` server, profile *Snowflake*, sign-in **per person**.
   Agents → `finance-analyst` gains `mcp:snowflake`.
2. As Lena, Account → **Connected services**: *Snowflake* — **Not connected** → **Connect**. The
   Snowflake sign-in opens; she signs in as her Snowflake user. Back in the Studio: **Connected**.
   Marcus does the same with his.
3. As Lena, `finance-analyst`: **"What was Q2 2026 revenue by region?"** The answer comes from the
   warehouse. Open the Sources line: the statement Snowflake ran, its query id, the rows, and
   **as you**. Snowflake's query history shows the query under Lena's user and role.
4. As Marcus (whose Snowflake role cannot read the revenue table), the same question: the
   warehouse refuses it, and the reply says so. AI Stackops granted nothing; the warehouse decided.
5. As Lena, **Keep** the answer. A day later (or after changing a row in the table), **Re-run**
   against *data as it was*: the report says, per step, *identical*, and *time travel applied: read
   as of <the answer's time>*. Against *current data*: *changed*, with the row counts before and
   after, and which of the answer's figures are no longer found.
6. As Lena, Account → Connected services → **Disconnect**: the warehouse tool is withheld from her
   next question, with the reason *it acts as you through your Snowflake account, which you haven't
   connected — connect it under Account → Connections* (the page's heading is *Connected services*).

*Databricks instead:* the same steps with a Databricks SQL MCP server. Its SQL tool is chipped
**Writes** by the profile (Databricks SQL can write), and a write tool is never re-run, so re-tier
it as `sql` in `mcp.json` on a read-only warehouse before step 5.

**Land:** the data stays in the warehouse and answers the person, as that person; a kept answer can
be asked again of the data as it was, and says whether it still holds.

---
