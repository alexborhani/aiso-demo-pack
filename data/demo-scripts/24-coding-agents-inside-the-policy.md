---
type: scenario
title: "24. Coding agents inside the policy"
tags: ["scenario-24"]
level: full
---
**Level:** Full. Needs Claude Code, the `ai-stackops` command, a clone of
`meridian-pump-controller`, and the cloud entry (see *Before the day*).


*Claude Code works through AI Stackops: the project decides which models it may use, what it may
read, which code may never go to a cloud model, and every line an AI wrote is on the record.*

**You are** Dana in the Studio, Sam in a terminal in the clone.

1. As Dana, **Projects** → *New project* `pump-controller`: repository
   `alexborhani/meridian-pump-controller`, level internal. Models: `claude-haiku-4-5` routed to the
   `claude-haiku` entry, and `claude-local-qwen` routed to the local chat entry. Members: Sam.
   A cloud id must contain `claude` for Claude Code's model picker to keep it; to route it to a model
   that is not Claude, set its *Claude Code picker behaves as* to `claude-haiku-4-5`. With the
   `claude-haiku` entry on OpenRouter the gateway translates Claude Code's Anthropic calls for
   OpenRouter's Chat Completions API; that path was verified live with a local model only.
   *Docs for agents*: `firmware-docs`. **Code** → *Path rules*: `firmware/safety/**` confidential,
   Security. *Classified code*: **Enforce**. Mint a CI key and copy it.
2. Skills → `safety-change-review` → *Where it is offered* → *Development projects*:
   `pump-controller` → Save. If it is refused, run its evals first (*Evals* → *Run evals*);
   scenario 23 shows why.
3. As Sam, in the terminal, in the clone: `ai-stackops dev login --hub <the Studio's URL>`. It
   prints a code; approve it in the Studio as Sam under Account → *Sign in a terminal*. The login
   points Claude Code (and Codex and OpenCode) at the project through AI Stackops by itself. Then
   Projects → pump-controller → *Setup files* → `.mcp.json`: save it in the clone's root; it gives
   Claude Code the project's docs, code map and skills. Index the code as CI would:
   `AISO_URL=<the Studio's URL> AISO_CI_KEY=<the key> AISO_PROJECT=pump-controller ai-stackops code index`
   It reports the files, the contract, the owners, and *Classified above internal: 1 files*: the
   server keeps fingerprints of those lines, never the lines.
4. `claude`, then `/model claude-haiku-4-5`, then: **"What does the service API expose, and who
   owns firmware/safety?"** Claude Code answers through AI Stackops with the project's code map
   (the OpenAPI contract), `code_owners` (`@meridian/safety-engineering`) and `search_docs` (the
   service API guide): one read-only endpoint, owned by the service platform team.
5. **/mcp__aiso-pump-controller__safety-change-review feature/raise-trip** (the project's skill,
   served to Claude Code as a command): it loads the safety checklist from AI Stackops and asks for
   the change's files.
6. **"Show me what firmware/safety/interlock.c does."** Claude Code reads the file on the Mac and
   sends it to the model, and the call is refused before it leaves: *This conversation carries
   classified code from firmware/safety/interlock.c (confidential, 27 lines), which
   claude-haiku-4-5 may not receive: the model is cleared for internal at most. Switch to
   claude-local-qwen for this work, or remove that code from the conversation (for example
   /clear).* Nothing reached the cloud provider. `/clear` to go on. A careful model may stop one step
   earlier: it calls `code_classification` for the path first, is told the cloud model may not receive
   it, and says so without reading the file. Either way the file stays on the Mac; show whichever
   happened (the refusal, or the `code_classification` call in the transcript).
7. **"Add a bar-to-psi conversion function to src/controller/units.c, next to bar_to_kpa."** Claude
   Code writes it. Commit it on a branch, then `ai-stackops code attest --base main` (with the same
   `AISO_URL`, `AISO_CI_KEY` and `AISO_PROJECT`): *4 lines added (2 long enough to tell), written
   by a model through AI Stackops: 2 (100%), from cloud models: 2 — claude-haiku-4-5*, and a signed
   attestation with the `cosign` command that checks it.
8. As Dana, Projects → pump-controller → **Code**: *What the code rules did* (the refusal, the file,
   the person) and **AI provenance** (the change and its AI lines); **Usage** (tokens and cost by
   model and person). Admin → Audit: `gateway.call` rows carry the model, the tokens and the cost,
   never the prompt; `code.attest` names the change.

Optional, for engineering leaders: *Classified code* also offers a guard that stops Claude Code
reading the file at all, before anything is sent. It is a managed setting installed on the Mac
(Projects → *Setup files* → managed settings, which needs an administrator on the Mac), so it is
left out of the live run.

**Land:** coding agents are governed like every other agent: the project picks the models, the policy
keeps classified code on the models allowed to carry it, and what the AI wrote is attested.

Scenarios 31 and 32 continue from this project; scenario 33 charges back its spend.

---
