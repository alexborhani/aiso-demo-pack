# Classification stand-ins: notes

Drafted 2026-09-29 against the product at `~/Dev/aiso-wt-skills` (branch `skills-engine` checkout).
The data and drafts are under `drafts/classification/`, `data/labelled-files/` and
`data/column-catalog/`. **Merged into the pack on 2026-09-29** (uncommitted, unsigned, version not
bumped): the store, the mappings, the MCP fragment, the two named queries and the manifest entries
listed under *Config changes the pack needs*. Scenarios 25–27 are still only in `scenarios.md`, and
the onboarding agent (section 5, option 1) is not shipped. The probes now read the pack's own files
(`classification.yaml`, `knowledge/`, `mcp/`, `data/toolbox/tools.yaml`), not the drafts.

## Files

| Path | What it is |
| --- | --- |
| `drafts/classification/generate_labelled_files.py` | Builds `data/labelled-files/` (9 files). Needs `python-docx openpyxl python-pptx pypdf reportlab` in a venv. |
| `drafts/classification/generate_column_catalog.py` | Builds `data/column-catalog/catalog.sqlite` + `tools.yaml` from the music store's schema. Standard library only. `--variant retagged` changes the catalog in place. |
| `drafts/classification/labelled-files.knowledge.yaml` | Draft store: `loader: office`, pattern `*.{docx,xlsx,pptx,pdf}`, default internal, `auto: false`. |
| `drafts/classification/classification-mappings.yaml` | Draft `mappings:` block for `classification.yaml` (Purview + BigQuery vocabularies). |
| `drafts/classification/toolbox-tools.addition.yaml` | Two named queries to append to `data/toolbox/tools.yaml`; option B for the tag query. |
| `drafts/classification/demo-data.mcp.draft.json` | Draft replacement for `mcp/demo-data.mcp.json` (adds `classification`, `columns`, and the `demo-catalog` server). |
| `drafts/classification/probes/probe-labels.ts` | Runs the product's loaders and label mapping over the files. |
| `drafts/classification/probes/probe-columns.ts` | Runs the product's Toolbox reader, `classifyCatalog`, `columnFindings` and `filterOutcome` against two real Toolbox servers. |
| `drafts/classification/scenarios.md` | Scenarios 25–27 in DEMOS.md style. |
| `data/labelled-files/*` | The generated Office and PDF files. |
| `data/column-catalog/catalog.sqlite`, `tools.yaml` | The generated tag catalog and its Toolbox config. |

Run the probes with `node drafts/classification/probes/probe-labels.ts` and
`node drafts/classification/probes/probe-columns.ts` from the pack root (Node 22+, `AISO_SRC` defaults
to `~/Dev/aiso-wt-skills`). The column probe starts `npx -y @toolbox-sdk/server@1.13.1` twice over
stdio; it copies the pack's data into a temp folder and changes nothing in the pack.

## 1. Purview labels inside files

### The labels (fictional tenant, fixed)

Site (tenant) id `0f5e3d2c-1b4a-4968-8776-5a4b3c2d1e0f`.

| Label name | Label id | Mapped to |
| --- | --- | --- |
| Public | `3a1c0f4e-6b2d-4c8e-9f10-2a5b7c9d1e01` | public (by name) |
| General | `5d8e2b1a-7c4f-4e9a-8b3d-6f1a2c4e8b02` | internal (by id) |
| Confidential | `8f2a6c3d-1e5b-4a7c-9d0e-3b6f8a1c5d03` | confidential (by name; no file uses it) |
| Confidential - Finance | `9a4d7e2f-3c6b-4d8a-8e1f-5c2b9d4a7e04` | confidential + Finance (by id) |
| Confidential - HR | `b1e5c8a2-4f7d-4b9c-9a2e-7d3c1f6b8a05` | confidential + HR (by name) |
| Highly Confidential | `c7f3a9d1-5e2b-4c6d-8f4a-9e1b3d7c2f06` | restricted (by name) |
| Highly Confidential - Legal | `d2a8f4c6-6b1e-4e3a-9c5d-1f7e4b9a3c07` | restricted + Legal (by name) |
| Partner Shared | `e6c1b7d3-8a4f-4f2b-8d6c-2a9f5e1b4d08` | not mapped, on purpose |

### The files

| File | Where the label is | Result (verified) |
| --- | --- | --- |
| `town-hall-agenda.docx` | `docProps/custom.xml` (`MSIP_Label_<id>_Enabled/SetDate/Method/Name/SiteId/ActionId/ContentBits`) | public |
| `riverside-shift-handover.docx` | `docMetadata/LabelInfo.xml` only (`<clbl:label id enabled method siteId removed>`, no name) | internal via the id row |
| `q3-board-pack-summary.xlsx` | custom.xml | confidential [Finance] via the id row |
| `northfield-negotiation-memo.docx` | custom.xml, Method Privileged | restricted [Legal] |
| `distributor-price-list-2027.pptx` | custom.xml, Partner Shared | no row; store default internal; logged as unmapped |
| `plant-safety-bulletin.pdf` | information dictionary `/MSIP_Label_<id>_…` | internal (the id row also matches: the key carries the id) |
| `grievance-hearing-notes.pdf` | FlateDecode XMP stream only, `pdfx:MSIP_Label_…` elements | confidential [HR] |
| `audit-committee-minutes.pdf` | info dictionary + `/Encrypt << /Filter /MicrosoftIRMServices … >>` | unreadable: "Encrypted by the sensitivity label Highly Confidential; the content could not be read" |
| `salary-review-2027.pdf` | no label; RC4-128 password `meridian-2027` | unreadable: "Encrypted with a password; the content could not be read" |

Figures in the board pack match `data/all-hands/q3-preliminary-results.md` (41.8 m, 18.2 %, 9.4 m, Nordvik 3.1 m); the plan column (44.5 m, 21.0 %, 10.0 m) is new. The Northfield memo matches `legal-matters/supplier-contract-northfield.md` (12 / 24 / 18 months).

### How it is wired

`KnowledgeStore.loaderForFile` sends docx/xlsx/pptx to `OfficeLoader` and, because the loader type is
`office`, PDFs to `PDFLoader`. Both put `externalLabels` on the document; a protected file comes back
with `metadata.protected` and no text. `applyDocumentLabels` then writes an authoritative row
(`classifiedBy: external:purview`, reason `sensitivity label <name or id>`) for mapped labels and an
`unreadable: …` pending row for protected files, which the compliance report lists as `unreadable`
(`document:labelled-files/<file>`). Protected files never appear in the Sources panel (it lists sources
with chunks only).

### Verified (probe-labels.ts output, 2026-09-29)

- `OfficeLoader` / `PDFLoader` read every label above, including the name-less LabelInfo.xml label, the
  compressed-XMP-only label, and the label left in the clear on the IRM stand-in.
- `KnowledgeStore.loadDocuments` with the draft store YAML finds the 9 files with the brace pattern
  and routes the PDFs to the PDF loader.
- `applyDocumentLabels` with the draft mappings over the pack's `classification.yaml`
  (`TaxonomySchema.parse`): 6 classified from labels, 2 unreadable, 1 at the store default.
- Independently: python-docx, openpyxl and python-pptx reopen the Office files; pypdf decrypts the
  password PDF with `meridian-2027`.

### Not verified

- Opening the files in Word, Excel, PowerPoint or Acrobat. Office would show the labels only if the
  tenant existed; Acrobat will refuse the IRM stand-in as a damaged or unsupported file.
- A real Purview-protected file. The IRM PDF is a stand-in: a real one is a wrapper PDF with an
  encrypted payload. A label-encrypted Office file (an OLE compound file) is not built at all; making
  one needs a tenant.
- Indexing and search through a running server, and the Sources panel wording.

## 2–4. Column tags, untagged columns, findings

### Design

- `data/column-catalog/catalog.sqlite`, table `column_tags ("database", "schema", "table", "column",
  data_type, domain, tag, value, masked)`: every one of the music store's 64 columns, plus one row per
  tag. It lists untagged columns deliberately: a column the catalog does not list is unknown to the
  filter, and a query reading its table then takes the highest level of that table (fail closed), so
  untagged columns would be withheld along with the tagged ones.
- Tags (database `musicstore`, schema empty, so the object is `musicstore.<Table>`):
  `Customer.Email pii=email` (masked), `Customer.Phone pii=phone`, `Invoice.Total finance=revenue`,
  table tag `Invoice retention=7y` (not mapped), table tag `Employee hr=personnel`,
  `Employee.BirthDate hr=date_of_birth`. Result: 18 classified columns, 9 with an unmapped tag.
- A second Toolbox server `demo-catalog` (cwd `bundles/aiso-demo-pack/column-catalog`) declares only
  `aiso_column_tags`. `demo-data` reads it with `columns.via: demo-catalog`, so no agent is ever given
  the tag query. `ColumnHost.sync` runs the reader against `via` and stores the columns under
  `demo-data`.
- How the product reads the query (`catalog.ts toolboxReader`): it requires a tool named
  `aiso_column_tags` (or `columns.tool`) on the target, calls it with `{}`, reads the rows with the
  Toolbox extractor (JSON objects run together), and takes `database|catalog|project`,
  `schema|dataset`, `table|object`, `column|field`, `tag|policy_tag|label`, `value|tag_value`,
  `domain`, `data_type`, `masked` (true/1/yes). No tag = an untagged column; a tag with no column =
  a table tag (domain from the row, else table). Vocabulary: `bigquery` unless `columns.vocabulary`.
- Two new named queries on `demo-data` return columns under their own names, so the filter resolves
  each result column through the declared statement: `customer_contact` and
  `customer_spend_by_country`.

### How a withheld value appears

The column host filters the result after the MCP call and before the model, the direct call route or
the answer record see it, and only under Monitor or Enforce (Off skips the filter). Under Enforce each
withheld value is replaced by `[withheld: <level>]`, and a note is appended to the text the model
reads: `[Values of 2 columns withheld (Email, Phone): classified above what this conversation may
show. If the answer needs them, say they were withheld.]`. The Sources line shows *N columns
withheld*; *Show result* shows the redacted rows; one `classification.refused` audit row per call
names the columns. Under Monitor the values pass and a `classification.monitor` row records what
would have been withheld. The check is the caller's clearance AND the model ceiling of the run.

### Verified (probe-columns.ts output, 2026-09-29)

- Both server entries parse with `MCPServerConfigSchema`; the taxonomy with the draft mappings parses.
- Real Toolbox 1.13.1 serves `aiso_column_tags` with no parameters; `toolboxReader.read` gets 64
  columns, 6 tags, 1 masked; `classifyCatalog('bigquery')` gives 18 classified columns (Customer.Email
  and Phone confidential, 15 Employee columns confidential [HR], BirthDate restricted [HR],
  Invoice.Total confidential [Finance]) and 9 Invoice columns with `retention=7y` unmapped.
- `columnFindings` after that sync: `column-tag-unmapped` (low), `column-above-server` (medium, 18
  columns above internal), `column-unmasked` (medium, Employee.BirthDate).
- After `generate_column_catalog.py --variant retagged` (in place, against a copy) and a second read,
  with a classifier opinion of confidential SET BY HAND on Customer.Address: `column-classifier-higher`
  "Tagged internal; the classifier reads it as confidential. The tag stands."
- `filterOutcome` on real results, enforce, ReadFilter per person (server default level internal):

| Query | Priya (internal) | Lena (confidential, Finance), local model | Dana (admin), local model | Anyone on a model ceilinged at internal |
| --- | --- | --- | --- | --- |
| `customer_contact(Leacock)` | Email, Phone withheld | nothing withheld | nothing withheld | Email, Phone withheld |
| `customer_spend_by_country(3)` | customers, spend withheld (computed) | nothing withheld | nothing withheld | customers, spend withheld |
| `customer_purchases(Heather Leacock)` (scenario 22) | 7 of 8 columns withheld | nothing | nothing | 7 of 8 columns withheld |
| `longest_tracks(2)` | nothing | nothing | nothing | nothing |

### Not verified

- A sync through a running server (`ColumnHost.sync`, the `columns.via` lookup, the settings state,
  the Columns dialog wording and counts). The probe calls the same reader with the same inputs.
- Any model step: the librarian choosing `customer_contact`, how it words a withheld value, the
  Sources line, the audit row.
- The column classifier (step 7 of scenario 26). It needs the local model. Two facts from the code:
  for a Toolbox source it never reads sample values (`SAMPLE_QUOTE` has no toolbox entry, and the
  catalog server has no SQL tool), so it decides on name, type and sibling columns only; and it never
  looks at tagged columns. Whether it rates Customer.Address confidential, which the
  `column-classifier-higher` step depends on, is the model's call.

## 5. A policy drafted with you

The pack adopts its policy on install (`seed.taxonomy` + `seed.policy`, `adoptedBy: pack:aiso-demo-pack`),
so the Studio's *No classification policy adopted* banner and its *Draft one with the onboarding
agent* button never show in the demo workspace, and the Studio has no other button that installs the
agent. Three ways to show onboarding honestly:

1. **Ship the agent in the pack** (recommended). Copy the product template verbatim:
   `cp ~/Dev/aiso-wt-skills/templates/agents/classification-onboarding.agent.yaml agents/`, list it in
   `resources.agents` and in the `standard` level's `adds.agents`. Scenario 27 then runs in the demo
   workspace: the agent submits a proposal, Dana reads it under *Proposals* and rejects it. Recopy
   when the template changes. If the install route runs later it reports `existing: true`.
2. **Call the install route** as Dana: `POST /api/admin/classification/onboarding/install`
   (`policy:write`). Works, but it is an API call on stage.
3. **A second workspace without the pack**, where the banner and button appear. That is the real
   first-run path; it needs a second install.

Do not adopt a proposal in the demo workspace. `taxonomyFromProposal` replaces the levels and
categories, and replaces the Purview vocabulary with the proposal's name → level pairs, so the id rows
and the label categories from scenario 25 would go. Adoption also re-stamps `policy.adoptedBy`, so a
pack update no longer re-adopts the pack's policy (`updateSeed` re-adopts only while
`adoptedBy === pack:<id>`). Uninstall and reinstall restores it.

Not verified: any of it. It needs a running server and a model.

## Scenario 22 interplay

**The conflict.** Scenario 22 part two (Full, as Dana) asks `music-librarian` for Heather Leacock's
purchases (`customer_purchases`) and later runs `artists_in_both_genres` and `longest_tracks`. With
demo-data's columns synced, the column filter resolves each result column of `customer_purchases`:
all but `quantity` are renamed (`AS invoice_id`, `date(...) AS invoice_date`, `t.Name AS track` …),
so they take the highest level of every table the statement reads. Customer (Email, Phone) and
Invoice (Total) make that confidential [Finance]. Measured with `probe-columns.ts` on the merged
pack, enforcement Enforce:

| Query | Local model, Dana | Cloud entry (ceiling internal), anyone incl. Dana | Priya |
| --- | --- | --- | --- |
| `customer_purchases(Heather Leacock)` | nothing withheld | 7 of 8 withheld (all but `quantity`) | 7 of 8 withheld |
| `artists_in_both_genres(Rock, Metal)` | nothing | nothing | nothing |
| `longest_tracks(2)` | nothing | nothing | nothing |

The last two read only untagged tables (Track, Album, Artist, Genre), so they are safe. Only
`customer_purchases` is hit, and only under Enforce: Off skips the filter and Monitor lets the values
through while recording `classification.monitor`.

**Decision: keep the tags and the query; scenario 22 part two runs with enforcement Off or Monitor.**
Nothing in the pack config changes for it. Why not the alternatives:

- *Result columns that trace cleanly.* Every source column needs its own name in the result, and
  the track, the artist and the genre are all `Name` (Track.Name, Artist.Name, Genre.Name). Toolbox
  prints such a row with the key twice (`{"Name":"Balls to the Wall","Name":"Accept"}`, checked with
  1.13.1), and every JSON reader keeps only the last: AISO's row extractor, figure binding, charts
  and the redaction itself. So at most the artist or the track can trace; the other stays renamed
  and is withheld. The librarian's eval
  needs both (`contains: Metallica`, and a judge asking for an artist and an album), so a half
  rename still breaks under Enforce while changing what *Show result* shows.
- *Fewer tags.* The purchases query must read Customer (the question is by name) and Invoice (the
  date). Customer.Email and Phone are the point of scenario 26, so any renamed column of this query
  stays confidential whatever happens to Invoice.Total. Removing Invoice.Total as well and splitting
  the query in two (look the customer up, then purchases by id without Customer) would work, but it
  changes scenario 22's flow, the librarian's prompt, the catalog generator and scenario 26's counts
  (18 → 17 classified), for a scenario that is about answer checks, not columns.
- *Two servers over the same database, one filtered.* A loophole demonstrated on stage. No.

Under Enforce the result is correct policy: a renamed column cannot be traced to one source column,
so it fails closed. Scenario 26 step 5 shows exactly that with `customer_spend_by_country`.

**What to change in DEMOS.md when scenarios 25–27 are merged** (then re-run
`scripts/split-demos.py` so the `demo-scripts` store matches). Not done now, so DEMOS.md and the
scripts store stay in step with each other. In §22, before step 4:

> 3a. As Dana, Admin → Policy → Classification → Enforcement → **Monitor** (or Off) if an earlier
> scenario left it on Enforce. Under Enforce the column filter withholds the purchases query's
> renamed columns from the cloud librarian: that is scenario 26, not this one.

And in the reset list: nothing new (enforcement already goes back to Off).

**Other ways to run 22 under Enforce, if a presenter must:** the librarian on a local model with no
ceiling, as Dana (nothing withheld, row 1). Not as Priya or Lena: their clearance withholds the same
columns whatever the model.

**Watch:** if scenario 26 step 7 were run in *Apply* instead of Monitor, the classifier's levels on
untagged columns would count too; a Track or Album column rated above internal would start withholding
`artists_in_both_genres` and `longest_tracks`. The scenario uses Monitor; keep it that way.

**Product note (not acted on).** The filter trusts result names: an expression aliased to a source
column's name (`date(i.InvoiceDate) AS InvoiceDate`, or `SUM(i.Total) AS InvoiceId`) takes that
column's level. Named queries are written by whoever controls the server config, so this is by
design, but it means a query author can launder a column by naming it after an untagged one.

## Config changes the pack needs (exact)

*Applied 2026-09-29, except the onboarding agent (option 1 of section 5), the version bump and the
signature.*

### manifest.json

Add to `resources.knowledge`:

```json
"knowledge/labelled-files.knowledge.yaml"
```

Add to `resources.bundles`:

```json
"data/labelled-files",
"data/column-catalog"
```

Add to the `full` level's `adds.bundles` (the catalog goes with the demo-data server; the labelled
files stay at Essentials by not being listed in any `adds`):

```json
"data/column-catalog"
```

If option 1 above is taken, add to `resources.agents` and to the `standard` level's `adds.agents`:

```json
"agents/classification-onboarding.agent.yaml"
```

Level descriptions: Essentials "… the ten stores the scripts use … Scenarios 1–8, 13, 14, 16, 18, 19,
21, 22, 25."; Standard "… Scenarios 0, 9–12, 15, 17, 23, 27."; Full "… Scenarios 20, 22 (part two), 24,
26 and the builder workshop." Bump `version` (1.13.0), then `ai-stackops pack sign` so `integrity`
covers the changed MCP fragment; a stale `integrity` drops the pack to community.

### Files to copy

```sh
cp drafts/classification/labelled-files.knowledge.yaml knowledge/
cp drafts/classification/demo-data.mcp.draft.json mcp/demo-data.mcp.json
# append the two queries (not the commented option B) under tools: in data/toolbox/tools.yaml
sed -n '/^  customer_contact:/,/^# Option B/p' drafts/classification/toolbox-tools.addition.yaml | sed '$d' >> data/toolbox/tools.yaml
```

### classification.yaml

Replace the last two lines (`mappings:` / `  external: {}`) and the comment above them with the
`mappings:` block of `drafts/classification/classification-mappings.yaml`. Leave `classifier.columns`
off in the shipped file; scenario 26 switches it on in the Studio.

### mcp/demo-data.mcp.json (as drafted)

```json
"demo-data": {
  "…": "unchanged fields",
  "classification": { "level": "internal" },
  "columns": { "sync": true, "via": "demo-catalog", "vocabulary": "bigquery", "intervalHours": 24, "classify": true }
},
"demo-catalog": {
  "description": "The data team's column catalog for the music store (a stand-in for BigQuery policy tags): one named query, aiso_column_tags, read by AI Stackops to classify the demo-data columns. No agent uses it.",
  "command": "npx",
  "args": ["-y", "@toolbox-sdk/server@1.13.1", "--stdio", "--config", "tools.yaml"],
  "cwd": "bundles/aiso-demo-pack/column-catalog",
  "profile": "toolbox",
  "serviceAccount": { "name": "demo catalog file", "description": "The catalog SQLite file shipped in the pack, opened by the Toolbox server." },
  "timeout": 120000,
  "callTimeout": 30000
}
```

`classification: internal` on demo-data is what produces `column-above-server`. It also means that
under Enforce Jordan (public) is not offered any demo-data tool.

### The data team's change (scenario 26, step 8) and its undo

```sh
DB="<workspace>/bundles/aiso-demo-pack/column-catalog/catalog.sqlite"
sqlite3 "$DB" "DELETE FROM column_tags WHERE \"table\"='Customer' AND \"column\"='Address' AND tag IS NULL;
INSERT INTO column_tags VALUES ('musicstore','','Customer','Address','NVARCHAR(70)','column','contact','address',0);"
# undo
sqlite3 "$DB" "DELETE FROM column_tags WHERE \"table\"='Customer' AND \"column\"='Address';
INSERT INTO column_tags VALUES ('musicstore','','Customer','Address','NVARCHAR(70)','column',NULL,NULL,0);"
```

Change the file in place; never replace it while `demo-catalog` runs (the server keeps the old file
open). `generate_column_catalog.py --variant retagged --out <that folder>` does the same.

### Reset between runs (additions)

Enforcement back to Off; *Columns nobody tagged* back to Off; undo the Address tag; the
`music-librarian` model back to the cloud entry; reject any open proposal; the price list's hand
classification from scenario 25 stays until the store is rebuilt or the pack reinstalled.

## Open questions and findings

1. **Scenario 22 part two under Enforce.** Decided: see *Scenario 22 interplay* above (run part two
   under Monitor or Off; the tags and the query stay).
2. **A mapping added after indexing does not reach files already indexed.** `applyDocumentLabels` runs
   only on the index path, and a directory store re-indexes only files whose content changed, so a new
   *External labels* row leaves the price list at the default until the file changes or the store is
   rebuilt. Scenario 25 works around it by classifying the file by hand. Product question: should saving
   a vocabulary re-map stored `externalLabels` (they are kept on the chunks)?
3. **Wording.** For the password-protected PDF the server log says "2 file(s) are protected by a
   label", but that file carries no label. The compliance message itself is right.
4. **Unmapped labels are only in the server log.** The Sources panel shows the price list at the store
   default with no hint that it carries *Partner Shared*. The scenario relies on the presenter saying
   so.
5. **Apply mode floods the review queue.** In *Apply*, every column the classifier rates public (track
   names, genres) is a lowering against the source level internal and goes to review: expect dozens of
   rows from the music store. Scenario 26 uses Monitor for that reason.
6. **Onboarding in the demo workspace** needs the manifest change (option 1) or an API call; decide
   which. Scenario 27's model level is a guess; nothing was run.
7. **Time for the column classifier** on 46 untagged columns with a 9B at concurrency 2 is not
   measured.
