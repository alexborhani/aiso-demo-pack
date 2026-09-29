---
type: scenario
title: "22. Numbers you can check"
tags: ["scenario-22"]
level: essentials
---
**Level:** Essentials for part one; part two needs Full (the demo-data server).


*Every answer carries where its figures came from, whether each figure was found there, and a
grade, before anyone acts on it. The platform checks the answer; it does not ask the audience to
trust the model.*

**You are** Lena for part one, Dana for part two and the settings.

*Part one: documents (Essentials).*

1. As Lena, `finance-analyst`: **"What was Q2 2026 revenue, and how does the full-year forecast
   compare with the plan?"** Under the reply, the Sources line: *Documents*, the close package
   passages it read, *Figures found in sources*, and a *Grade* badge. Open it: each figure is
   matched to a passage; the difference and the percentage are marked as worked out from them, by
   the calculator, not by the model in its head. The grade's reasons say why it is High or Medium.
2. Mark the answer: thumbs down, *What was wrong?* → a figure, a short note. Every mark is kept with
   the answer and counts towards tuning the checks (Admin → Policy → Answer checks → *How the checks
   have done*).
3. As Dana, Admin → Policy → **Answer checks**: the policy in one place. Answers built on data are
   held and checked before they are shown; one repair turn is allowed; figures from query results
   are filled in by the platform, not typed by the model; the second-model judge; clarifying
   questions; the minimum grade and what happens below it. *Model for decisions* is the local
   model: nothing about an answer leaves the Mac to be judged.

*Part two: data (Full).*

First, as Dana, Admin → Policy → Classification → Enforcement → **Monitor** (or Off) if an earlier
scenario left it on Enforce. Under Enforce the column filter withholds the purchases query's
renamed columns from the cloud librarian: that is scenario 26, not this one.

4. As Dana, `music-librarian` (answers from the demo-data MCP server: named, parameterised queries
   over the store's database; there is no free SQL tool). **"What has customer Heather Leacock
   purchased, and how much did she spend in total?"** While it is held the reply says *Checking the answer against the results…*, then the table
   appears. Sources: *Governed*, the named query `customer_purchases`, 38 rows, *Figures found in
   sources*, Grade High. Open the step: the statement
   that ran and its row count. Press *Show result*: the rows themselves. Open the grade. When the
   model used references to the result (it is told to while *Fill in figures from the results* is
   on), one reason reads *N figures were filled in from the results*: the model wrote a reference to
   a column and row, and the platform put the number in. Not every answer uses them; a total the
   model worked out with `calculate` is checked instead (*worked out from them*). Check on the day
   which reason appears before saying it. With *Model for decisions* on the local entry (*Before the
   day*, step 6) the second-model judge is on: a High grade's reasons include *A second model found
   it answers the question*; where it doubts, the grade is Low and the reason names what it doubted.
5. Answer checks → *Clarifying questions* → On. Ask **"Which artists play in two genres?"** The
   librarian asks which genres before running anything. **"Rock and Metal."** The named query
   `artists_in_both_genres` runs with those two, four artists come back, graded High. Set it back.
6. Under that answer, **Keep** with a title. **Verify**: the signature, the record, the results,
   the audit row, the checks and the grade are each checked again and pass. **Export** → HTML: one
   file a reviewer can open without the Studio. Account → *Kept answers* lists it; Admin → Audit →
   *Look up an answer* finds it by its run id.
7. Under the kept answer, **Re-run** against **data as it was**. The report: *Re-run against the data
   as it was: 1 same, 0 changed, … not re-run, 0 failed*, and on the `artists_in_both_genres` line *time
   travel not applied: the question is asked again, and the source may answer from newer data* (a
   calculation is never re-run; it counts as not re-run). Say: the demo store is SQLite, which cannot
   read the past; against Snowflake or Databricks the statement is rewritten to read the table as of
   the answer's time (scenario 34). Against **current data**: the same, and the line under it says
   how many of the answer's figures are still found. Admin → Audit: `answer.rerun`. (Not yet run;
   measured: pending.)
8. Optional, to show a check catching something: ask the librarian how long the longest track is in
   hours and minutes. If the model does the arithmetic in its head, the Sources line says *1 figure
   not found in sources* and the grade drops to Low.

**Land:** an answer is not a paragraph to be trusted; it is a record: what was asked, what ran, what
came back, which figures were found where, and a grade, signed and verifiable after the fact.

---
