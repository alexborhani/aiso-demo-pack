---
type: scenario
title: "26. Columns: withheld one by one, the untagged ones classified, the conflicts reported"
tags: ["scenario-26"]
level: full
---
**Level:** Full (the demo-data server is a Full resource). Steps 1–2, 6 and 8–9 need no model. Steps
3–5 need the music librarian's model (the cloud entry). Step 7 needs the local classifier model; a
9B-class model carries it. Measured: every step but one passed on Gemini 3.7 Flash; the 9B classifier
 decided all 46 untagged columns (in Monitor).


*A database answer is filtered column by column: the customer's city comes through, the email
address does not. The tags come from the data team's catalog; where they are missing, the local
classifier proposes one; where tags and the policy disagree, the compliance report says so.*

**You are** Dana in one window, Priya in the other. Server: `demo-data` (the music store), its tags
read through `demo-catalog`, the data team's catalog (a stand-in for BigQuery's policy tags, served
from a file in the pack). Agent: `music-librarian`.

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
7. Policy → Classification → *Background classifier*: the model is the local chat entry (set in
   scenario 1); **Columns nobody tagged** → *Monitor: record the classifier's view only*; *Save
   taxonomy*. Back in Columns: *Only columns without a tag*, *Classify now*. Refresh until *waiting*
   reaches zero (46 columns; time not measured). *Set by* shows the classifier's level and its
   one-line reason for each; nothing changes for readers.
8. The data team now tags Customer.Address `contact=address`, which the policy maps to internal. In a
   terminal on the Mac, change the catalog in place (never replace the file while `demo-catalog`
   runs):

   ```
   sqlite3 "<workspace>/bundles/aiso-demo-pack/column-catalog/catalog.sqlite" "DELETE FROM column_tags WHERE \"table\"='Customer' AND \"column\"='Address' AND tag IS NULL; INSERT INTO column_tags VALUES ('musicstore','','Customer','Address','NVARCHAR(70)','column','contact','address',0);"
   ```

   Then *Read tags now*. Address reads internal, set by the BigQuery tag, with *Classifier:
   confidential* under it if the classifier put it there in step 7. Compliance → *Check now*:
   `column-classifier-higher`: "Tagged internal; the classifier reads it as confidential. The tag
   stands."
9. Columns → *Download tag statements*. For BigQuery each line is a note naming the policy tag to
   attach in Dataplex; AI Stackops writes no tags to the source.

**Land:** column-level control works with the tags the data team already keeps. Where the tags are
missing or weaker than the policy, the platform says so; the data team decides what to change.

---
