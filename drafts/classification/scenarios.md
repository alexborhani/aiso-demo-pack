# Draft scenarios 25–27 (classification with local stand-ins)

Draft for DEMOS.md. Nothing here is in the pack until the config changes in NOTES.md are made.
Nothing in these scenarios uses a real Purview tenant or a real warehouse: the labels are written
into the files by `drafts/classification/generate_labelled_files.py`, and the column tags come from a
catalog file served by a second MCP Toolbox server (`generate_column_catalog.py`).

---

## 25. Labels the files already carry
**Level:** Essentials. Steps 1–6 need no model (step 5 needs only the embedding model); step 7 needs
the chat model. Not yet measured on Qwen 3.5 9B.

*Most organisations have already labelled their documents in Microsoft 365. The platform reads
those labels from inside the file and files each document at the level the policy gives that label.*

**You are** Dana in one window, Sam in the other. Store: `labelled-files`, nine Word, Excel,
PowerPoint and PDF files, seven carrying a Purview sensitivity label, two that cannot be opened.

1. As Dana, Admin → Policy → Classification → **External labels** → Purview. Six rows map label names
   to levels, and two rows match by label id: *General* and *Confidential - Finance*. Say why: Office
   files saved since 2022 carry only the label's id, not its name, so a mapping by name alone
   misses them. *Partner Shared* has no row.
2. Knowledge → `labelled-files` → *Sources*. Seven files with a level, *Set by* **Purview label**: the
   town hall agenda public, the shift handover and the safety bulletin internal, the Q3 board pack
   confidential Finance, the grievance notes confidential HR, the Northfield memo restricted Legal.
   The shift handover is the Word file with only the id; the grievance notes are a PDF whose label
   sits only in its compressed XMP metadata. No one typed any of these levels.
3. The price list reads at the store default, internal. Its label, *Partner Shared*, has no mapping
   (the server log names it). Press *Classify* on it, set confidential, give a reason, *Save*:
   applied at once. Say: until the policy knows a label, a person or the classifier decides.
4. Two files are missing from the list. Admin → Policy → Classification → **Compliance** → *Check now*:
   two `unreadable` findings. `audit-committee-minutes.pdf`: "Not indexed: Encrypted by the
   sensitivity label Highly Confidential; the content could not be read." `salary-review-2027.pdf`:
   "Encrypted with a password". The platform says what it could not read instead of indexing an
   empty page.
5. Enforcement → **Enforce** (skip if scenario 4 left it there). As Sam (builder, cleared internal and
   confidential Security), Knowledge → `labelled-files` → *Search*: **"liability cap Northfield"**, then
   **"Q3 revenue against plan"**. Neither the memo nor the board pack comes back; the agenda and the
   bulletin do when asked about them. As Dana, the same two searches return both files.
6. Admin → Audit, filter `classification.refused`: one row per search Sam made, naming the store and
   the levels withheld.
7. Optional, with the chat model: as Priya, Chat: **"What did the Q3 board pack say about revenue
   against plan?"** She is told nothing she is not cleared for; as Lena (Finance) the answer gives
   41.8 million against a plan of 44.5 million, with the board pack as its source.

**Land:** the labels people already put on files are the classification. Nobody re-tags anything, and
a file the platform cannot open is reported, not guessed at.

---

## 26. Columns: withheld one by one, the untagged ones classified, the conflicts reported
**Level:** Full (the demo-data server is a Full resource). Steps 1–2, 6 and 8–9 need no model. Steps
3–5 need the music librarian's model (the cloud entry in the measured setup). Step 7 needs the local
classifier model; a 9B-class model carries it. None of it is measured yet.

*A database answer is filtered column by column: the customer's city comes through, the email
address does not. The tags come from the data team's catalog; where they are missing, the local
classifier proposes one; where tags and the policy disagree, the compliance report says so.*

**You are** Dana in one window, Priya in the other. Server: `demo-data` (the music store), its tags
read through `demo-catalog`, the data team's catalog. Agent: `music-librarian`.

1. As Dana, Tools → MCP → `demo-data` → **Columns**. *Read tags now*: "Read 64 columns in 11 tables …
   through demo-catalog. 18 classified, 1 masked." Filter `Customer`: Email and Phone confidential,
   tags `pii=email` and `pii=phone`. Filter `Employee`: every column confidential HR from one table
   tag, BirthDate restricted. The Invoice columns carry `retention=7y` in a dashed box; the line
   above the table says 9 columns carry a tag with no mapping.
2. Admin → Policy → Classification → External labels → **BigQuery**: `pii` → confidential, `finance` →
   confidential Finance, `hr` → confidential HR, `hr` = `date_of_birth` → restricted HR. There is no
   row for `retention`. Enforcement → **Enforce**.
3. As Priya, `music-librarian`: **"What are Heather Leacock's contact details?"** The reply gives
   Orlando, USA and her support rep's id, and says the email and phone were withheld. Under the reply:
   *2 columns withheld*. Open the step, *Show result*: `"Email":"[withheld: confidential]"`. The model
   never had the values.
4. As Dana, ask the same. Still withheld: the librarian runs on the cloud entry, whose ceiling is
   internal. Say: the email address never reaches the cloud model, whoever is asking. Admin → Audit,
   filter `classification.refused`: the row names `Customer.Email` and `Customer.Phone` and the
   ceiling.
5. As Priya: **"Which three countries have the most customer spending?"** The countries come back;
   the customer counts and the spend are withheld. They are computed from Customer and Invoice, so
   they take the highest level of the tables read. A computed column cannot be traced to one source
   column, so the filter withholds it.
6. As Dana, Admin → Policy → Classification → **Compliance** → *Check now*. Three column findings:
   `column-above-server` ("demo-data" is classified internal, but 18 of its columns are tagged
   higher), `column-unmasked` (Employee.BirthDate is restricted with no masking policy) and
   `column-tag-unmapped` (retention = 7y on 9 columns). Each fix says who acts: *AISO admin:* or
   *Data team:*.
7. Policy → Classification → background classifier: model = the local chat entry (as in scenario 5);
   **Columns nobody tagged** → *Monitor: record the classifier's view only*; *Save taxonomy*. Back in
   Columns: *Only columns without a tag*, *Classify now*. Refresh until *waiting* reaches zero (46
   columns; time not measured). *Set by* shows the classifier's level and its one-line reason for
   each; nothing changes for readers.
8. The data team now tags Customer.Address `contact=address`, which the policy maps to internal. Run
   the one-line command in NOTES.md (*The data team's change*), then *Read tags now*. Address reads
   internal, set by the BigQuery tag, with *Classifier: confidential* under it if the classifier put
   it there in step 7. Compliance → *Check now*: `column-classifier-higher`: "Tagged internal; the
   classifier reads it as confidential. The tag stands."
9. Columns → *Download tag statements*. For BigQuery each line is a note naming the policy tag to
   attach in Dataplex; AI Stackops writes no tags to the source.

**Land:** column-level control works with the tags the data team already keeps. Where the tags are
missing or weaker than the policy, the platform says so; the data team decides what to change.

---

## 27. A policy drafted with you
**Level:** Standard. Every step after the first needs a model: a long interview, a nine-section policy
in Markdown and one tool call with a nested schema. Not measured on any model yet; a 9B is not
expected to carry it.

*An organisation with no written classification policy gets one by answering eight questions. The
agent proposes; an admin decides.*

**You are** Dana. Agent: `classification-onboarding` (see NOTES.md for how it gets into the demo
workspace). The Meridian policy stays in force throughout.

1. Admin → Policy → Classification: the Meridian policy is adopted (*Adopted … by pack:aiso-demo-pack*).
   Say: this scenario plays a different company, a 60-person pump distributor in Aarhus with no
   written policy, and nothing it proposes is adopted here.
2. Agents → `classification-onboarding`: **"We have no written classification policy."** Answer its
   questions one at a time. Suggested answers: GDPR, no other regulator; customer contacts, employee
   records, prices and margins, service reports; no labels today; three levels, *public*, *internal*,
   *confidential*; members see internal, admins see everything; confidential never goes to a cloud
   model; categories *Customer* and *HR*; untagged means internal, reviewed every year.
3. It shows the full draft: purpose, roles, the three levels with examples, categories, labelling,
   handling rules per level, the default, review, audit. Ask for one change, for example "service
   reports are internal, not confidential". Then **"Submit it."**
4. It says where the proposal waits and that nothing is in force. Admin → Policy → Classification →
   **Proposals**: the summary, levels *public < internal < confidential*, the handling rules. *Read
   policy* opens the Markdown. The Approvals tab lists it too.
5. **Reject.** Say what *Adopt* would do: write the policy, replace the taxonomy, re-check documents
   against the new criteria, and replace the Purview mapping with what the proposal names. In this
   workspace that would drop the Meridian levels and the id rows scenario 25 relies on.

**Land:** a policy nobody had written becomes one draft and one decision. The agent cannot put
anything in force.
