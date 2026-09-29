---
type: scenario
title: "20. Two nodes, one policy"
tags: ["scenario-20"]
level: full
---
**Level:** Full.


*Hub and spoke on one Mac: a second AI Stackops process enrolls, receives the hub's floors, and sends
its usage and audit home.*

**You are** Dana on the hub (the main install). The spoke is a second process started from the same
binary with its own workspace, standing in for a laptop at Riverside.

1. Start the spoke (see *Running a spoke on the same Mac* below). In a second browser profile, sign
   in to it on its own port and complete its first-run admin. It is a plain, empty AI Stackops.
2. On the hub, Admin → Estate: *Enable federation*, set the endpoint to the hub's own URL, and set
   the floors it pushes: tier caps, the taxonomy, roles, pack trust, cloud off, the chat model pinned.
3. Under *Hub and spoke*, mint a token for `riverside-laptop` with ceiling internal and role member (*Mint token*). Copy the join
   command. On the spoke, Admin → Estate → *Join a hub*: paste the hub URL and token. Within seconds
   the spoke banner shows the hub, the policy version and the floors applied.
4. On the spoke: Admin → Policy → Limits shows the hub floor badge; the Models tab shows the chat
   entry pinned and cloud locked; Classification shows the hub's taxonomy. Say: a laptop cannot
   loosen what the hub set, only tighten it.
5. A pinned model does not fail over. The spoke has none of the pack's agents, so use its own
   `chatbot`: on the spoke, Agents → `chatbot` → *Use models on other nodes* **Remote-first**, and
   tick *Share this agent with other nodes* (step 7 uses it). Save. Ask it **"What is 1234 * 5678?"**:
   answered on the spoke's own model, because the hub pinned the chat entry (step 2's floor). Admin
   → Audit on the spoke: `models.pin.bypass`, reason *ufp-remote-first: …*. Say: a pinned model is
   never swapped for another node's, even when an agent asks. Set it back to *Node default*.
   (Not yet run; measured: pending.)
6. On the hub: Admin → Estate → enrollments: the spoke with its policy version and last rollup.
   Network → Capacity: two nodes. On the spoke, *Send usage and audit now*; on the hub, Usage → *By
   node* and Audit → node selector: the spoke's rows, under its own name.
7. Optional, an answer from another node. On the hub, **Network** → the spoke → `chatbot` (shared in
   step 5) → ask **"What is 1234 * 5678?"**. Under the reply, the Sources line names the step *on
   riverside-laptop*; open it: *Answered on riverside-laptop, which keeps the record of what it ran*,
   the spoke's run id, and *signature verified*. Not yet run on the demo (measured: pending): check
   before the day that the Network tab's reply shows the Sources line as the Agents tab does.
8. Optional: revoke the enrollment on the hub; the spoke's next sync is refused and it purges the
   hub's snapshots.

**Land:** an estate of Macs is governed from one place: floors go down, evidence comes up, and a
lost or leaving laptop is cut off with one click.

**Running a spoke on the same Mac.** From the repository, with the same binary the host runs:

```
mkdir -p ~/aiso-spoke && cp templates/models.yaml ~/aiso-spoke/
WORKSPACE=~/aiso-spoke PORT=3460 UFP_ENABLED=true UFP_PEER_NAME=riverside-laptop \
  UFP_ENDPOINT=http://127.0.0.1:3460 HEADLESS=true ./dist/sea/ai-stackops start
```

Open `http://localhost:3460`, create its admin, and continue from step 2. The spoke uses the same
engine as the hub, which is fine for a demo; in production each node has its own. The hub must not
have been started with `UFP_ENABLED=false` in its environment: that locks federation off.

---
