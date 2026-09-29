---
type: guide
title: "Reset between runs"
tags: []
---
- Scenario 1: the classifier model stays set; later scenarios (5, 26) use it. While it is set, a
  document indexed or re-indexed waits for it (pending) before anyone below the top level sees it.
- Scenario 4: set enforcement back to *Off* (Admin → Policy → Classification).
- Scenario 5: the classified notes stay classified; to repeat, uninstall and reinstall the pack, or
  reindex `site-notes` after deleting its rows under Sources (classify each back to internal, then
  approve the lowerings).
- Scenario 9: delete the filed notice from `scratchpad` (Sources) or leave it as a talking point.
- Scenario 12: the CEO's ticket changes stay; add a fresh ticket next time.
- Scenario 13: Priya → Account → *Forget*.
- Scenario 15: leave the entry; delete `board-analyst` if you prefer a clean agent list. After
  step 8, restart the host without `EGRESS_ALLOW_FRONTIER=false`.
- Scenario 16: member Requests / min back to empty; `helpdesk`'s model back to `default`;
  `claude-haiku` USD / day back to 1 (or, without a key, the pricing removed from `mlx-serve`).
  Leave the entry: the next run needs it.
- Scenario 17: restore the runbook and reindex.
- Scenario 19: reinstall the pack to bring Jordan back (Packs → uninstall → install).
- Scenario 20: revoke the enrollment on the hub and stop the spoke process.
- Scenario 21: Marcus → Account → *Access you granted* → *Revoke*, if the scenario did not end there.
- Scenario 22: Answer checks → *Clarifying questions* back to Off; kept answers stay (Account →
  *Kept answers*). Enforcement back to where you found it.
- Scenario 23: the skill Sam built stays (delete its folder in the IDE tab if you want it gone);
  Skills → `customer-notice` → *Where it is offered* → untick *Every agent*.
- Scenario 24: Projects → pump-controller → *Archive*; Account → *Signed-in machines* → sign the
  terminal out; delete the demo branch in the clone. Archive it only after 31–33, which use it.
- Scenario 25: enforcement back to *Off*. The price list's hand classification stays until the
  store is rebuilt or the pack reinstalled.
- Scenario 26: enforcement back to *Off*; *Columns nobody tagged* back to *Off*; `music-librarian`'s
  model back to the cloud entry if you changed it; undo the Address tag:
  `sqlite3 "<workspace>/bundles/aiso-demo-pack/column-catalog/catalog.sqlite" "DELETE FROM column_tags WHERE \"table\"='Customer' AND \"column\"='Address'; INSERT INTO column_tags VALUES ('musicstore','','Customer','Address','NVARCHAR(70)','column',NULL,NULL,0);"`
- Scenario 27: reject any open proposal (Admin → Policy → Classification → *Proposals*). Never adopt
  one in the demo workspace: it replaces the Meridian taxonomy and the Purview mapping.
- Scenario 28: IDE tab → `models.yaml` → the `mlx-serve` entry: `pinned: false` and `model:
  mlx-serve` in one edit, then remove the `pinned` line. Kept answers stay.
- Scenario 30: *When a query has a known mistake* back to **Run it and note the problem**.
- Scenario 31: restore the daily caps (tightening applies at once), *When the budget runs out* back to
  *Refuse paid calls*, the *By kind* routes back to *same as the id*.
- Scenario 32: Admin → Policy → Packs → switch the hook off.
- Scenario 34: Lena and Marcus → Account → *Connected services* → **Disconnect**.
- Scenario 35: uninstall the community pack; *Minimum tier to install* back to what it was.

A full reset is Packs → uninstall → install: accounts, stores, policy and the organisation return to
the starting state, with new passwords.
