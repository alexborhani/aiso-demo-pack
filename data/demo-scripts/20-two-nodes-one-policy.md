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
5. On the hub: Admin → Estate → enrollments: the spoke with its policy version and last rollup.
   Network → Capacity: two nodes. On the spoke, *Send usage and audit now*; on the hub, Usage → *By
   node* and Audit → node selector: the spoke's rows, under its own name.
6. Optional: revoke the enrollment on the hub; the spoke's next sync is refused and it purges the
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
