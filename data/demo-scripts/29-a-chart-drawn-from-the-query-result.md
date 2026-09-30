---
type: scenario
title: "29. A chart drawn from the query result"
tags: ["scenario-29"]
level: full
---
**Level:** Full (the demo-data server). Measured on Gemini 3.7 Flash: every step but the seven-day expiry.
`builtin:chart` needs the model to name the result and write a small Vega-Lite spec; start on the
cloud entry.


*A chart the model cannot fake: it names which result to draw and how, and the platform draws it
from the rows the query returned.*

**You are** Dana; Jordan in the second window for the last step.

1. `music-librarian` (on the cloud entry): **"Chart the 10 longest tracks."** The librarian calls
   `longest_tracks` with 10, then `chart` naming that result, and the reply shows a bar chart: one
   bar per track, its length in seconds. The chart appears once the reply is finished (where the
   model placed it, or under the reply when it did not).
2. Open the tool trace: the `chart` call's arguments are a step number (`S1`) and a mark and
   encoding over the result's columns (`track`, `seconds`), and nothing else. Say: there is no
   field for data. The model cannot pass numbers to the chart; a spec that tries (`data`, `url`,
   `transform`, an expression) is refused before anything is drawn.
3. The Sources line under it: *Governed*, the named query `longest_tracks`, 10 rows, *Figures found
   in sources*, the grade. Open it: the step's statement and **Show result** — the ten rows the
   bars are drawn from.
4. **Keep** it (*Longest tracks, charted*). **Export** → HTML: open the file. The chart is in it,
   drawn as a picture from the kept rows, under the answer, with the statement and the checks. It
   loads nothing from the internet. Admin → Audit, `answer.exported`: `charts: 1`.
5. Say what happens later: the rows behind an unkept chart are kept for seven days, after which
   the chart reads *Data expired: keep the answer to preserve its charts.* A kept answer keeps them.

**Land:** a chart in a reply is a view of a recorded result, not a picture the model made, and it
travels with the signed answer.

---
