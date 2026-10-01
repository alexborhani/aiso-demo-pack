# Demonstrations of AI Stackops, on one Mac, as Meridian Works

Scripts for a presenter showing AI Stackops to senior business and technology leaders. Every
scenario runs on a single Mac with the demo pack installed and the local model; nothing in the
product or the pack is scripted to produce a particular answer. What the audience sees is what the
platform does with the data in the pack. Each scenario takes five to eight minutes; a 60-minute tour
that chains nine of them is at the end, with a reset checklist. Scenarios 34–36 need a system the
Mac does not have (a warehouse, an unsigned pack's repository, a Microsoft 365 tenant) and say so.

Meridian Works is fictional: an industrial pump and controls company with a plant at Halden, a
service centre at Riverside and an office at Crestview, about 400 people. Nothing in the pack is real.

## Levels: pick the demo your model can carry

The pack installs at one of three levels, chosen on the install dialog and changeable later from
the pack card (agents above the level are removed, the people and the policy stay). Every scenario
below says which level it needs; the people, the stores of the essentials and the scripts are the
same at every level, so a story told at Essentials reads the same at Full.

| Level | Model it was measured on | What it adds | Scenarios |
| --- | --- | --- | --- |
| **Essentials** | Qwen 3.5 9B (4-bit) on MLX Serve, 32K context, on a 24 GB Mac | the nine Meridian agents with one to three tools each, the nine stores the scripts use, the labelled files, the files for a person's own space | 1–8, 12, 13, 14, 16, 18, 19, 21, 22 (part one), 25 (steps 1–6), 37–39; 35 (needs an unsigned pack repository, not built; not tested) |
| **Standard** | DeepSeek V4.1 Flash through OpenRouter for the writer, canvas and helpdesk, standing in for a 27B-class local model | the presenter, the writer with its customer-notice playbook, canvas, the two workflows, the evals, the demo scripts | 0, 9–11, 15, 17, 23, 27; 34 (needs Snowflake or Databricks, not tested); 36 (needs a Microsoft 365 tenant, not tested) |
| **Full** | Gemini 3.7 Flash through OpenRouter for the librarian, the data analyst and Claude Code, standing in for a 70B-class model or a frontier provider | the sample workshop agents, the sample stores, the demo-data and demo-sql MCP servers and the column catalog, the firmware docs and the safety review skill | 20, 22 (part two), 24, 26, 28–30, 31–33 (with Claude Code, continuing from 24; 32 also needs a pack with a pre-send hook, not tested), and the builder workshop |

**Measured on 2026-09-29/30.** Essentials: every scenario in the row ran end to end three times
in a row on the 9B with every step passing, and `scripts/bench.py --level essentials` passed all 18
checks 10 of 10. Scenario 25's step 7 did not work on the 9B. Standard, with the agents above on
DeepSeek: 0, 9, 10, 11, 15, 17 and 27 passed end to end; 23 built, drafted and saved the skill,
and its eval gate held because the evals ran on the host's 9B default (see the note in 23). On the
9B alone, 0, 10 and 11 also passed; the rest of Standard did not. Full, on Gemini: 20, 24, 28, 30,
31 and 33 passed end to end; 22 part two passed but for the clarifying question, which the local
decision model did not ask; 26 passed but for one column left over from an earlier run; 29 passed
once its label was read as *Governed or Mixed*. Steps that need Claude Code's spend (31), seven
days (29), a provider admin key (33) or a live tenant (34, 36) were not run.

**Measured on 2026-10-01 (1.14.0).** Scenarios 37–39 and the extended 19 ran end to end three times in a
row on the 9B with every step passing (the pack reinstalled before each pass), and the three new bench
checks (`space-answer`, `instructions`, `save-to-space`) passed 10 of 10 each. The other checks and
scenarios were not re-run for 1.14.0. Spaces at Standard and Full: measured: pending.

**Measured on 2026-10-01 (1.15.0).** Scenario 12 (*Work on a schedule*) ran end to end three times in a
row on the 9B with every step passing (one install, the schedule deleted at the end of each pass), and
the new bench check `schedule-run` passed 10 of 10. Nothing else was re-run for 1.15.0: the release
removes the organisation and its two CEO agents and adds no other agent, store or step.

The boundaries come from measurement, not taste: on a 9B a single tool with ten actions was
already unreliable, so nothing at Essentials has more than three one-action tools, and the
presenter — a long prompt, many actions — waits for Standard. Standard and Full were
measured on small cloud models; no 27B or 70B local model was measured for this release, so treat
those rows as the size the scenarios need, not a promise about a particular local model.
`scripts/bench.py` runs every scripted call of a level against the model your host serves and
says, check by check, whether that level operates on it.

## Before the day

**Install and prepare (once, about 30 minutes)**

1. Install or update AI Stackops on the Mac (the deploy kit installs AI Stackops only; the engine is
   MLX Core, run separately). Give the engine at least a 16K context, 32K on 24 GB or more: in MLX
   Core's settings, or `--ctx-size 32768` if you start `mlx-serve` yourself. This is not optional:
   the engine's own default of 4096 tokens is enough for a chat, not for an agent with tools and
   retrieved documents. The scenarios marked *needs room* fail with "prompt exceeds maximum context
   length" or take minutes at 4096. Load Qwen 3.5 9B (`mlx-community/Qwen3.5-9B-MLX-4bit`) and an
   embedding model (`bge-small` or `Qwen3-Embedding-0.6B`).
2. Sign in as the first admin. Admin → Estate → **Licence**: paste the demo Enterprise key (issued
   by AI Stack Ops for the demo). The Licence panel shows the edition, the people and nodes used and
   the date it ends. On the Free edition the pack still installs, but the chargeback export and the
   evidence bundle's projects section (scenarios 18, 24 and 33) say *edition required*.
3. Packs → *Install* → `https://github.com/alexborhani/aiso-demo-pack`, and pick the level your
   model carries (above). Copy the six passwords from the dialog into a password manager: Dana
   (admin), Sam (builder), Priya, Marcus, Lena (members with roles), Jordan (contractor, public
   only). *Reset passwords* on the pack card mints new ones at any time.
4. Knowledge tab: the pack's stores index on install. Check each shows *indexed* (a few minutes in
   total on the local embedding model). The HR and finance stores are listed only to the people
   whose roles open them, so sign in as Marcus and Lena to see those two.
5. Models tab: the default chat entry is the engine's Qwen 3.5 9B and the embedding entry is the
   engine's embedding model. Nothing else is required. Scenario 15 adds a cloud entry live.
   Scenarios 16, 22 and 24, and Standard and Full on a small Mac, are stronger with the cloud entry
   below, added once; without it they run on the local model.

   *The cloud entries.* Two, one per level, the ones this release was measured on. Models tab → the
   OpenRouter tab → **New entry**. **Name** `deepseek-flash` (the scenarios and agents refer to the
   entries by these names; a new entry is named after its model until you type one), model
   `deepseek/deepseek-v4.1-flash`, key `${OPENROUTER_API_KEY}` (the key in the host's environment or
   the secret store, never in the file), Max Tokens 4096, Thinking budget 0, access minimum role
   **member** (Priya asks the questions; a new cloud entry starts admin-only), classification
   ceiling **internal** (the runbooks are internal; the firmware safety code, confidential, stays
   off it), pricing from the model's OpenRouter page on the day (0.30 / 1.20 per million when
   measured), and USD / day **1**. Save. Then **New entry** again: name `gemini-flash`, model
   `google/gemini-3.7-flash`, the same key, access and ceiling, its own pricing (0.75 / 3.75 when
   measured) and USD / day **1**. That dollar a day per entry is the demo's own fence: a rehearsal
   and a run share it, because the window is a rolling 24 hours. Make neither the default; the
   scenarios switch agents to them live. From then on the provider's tab lists each entry by name
   above the form: pick one there to edit it (scenario 16 changes `deepseek-flash`'s budget).
   *Standard and Full on a 9B-class Mac.* Keep the local model as the default and give the cloud
   entries only to the agents those levels add: for Standard, Agents → `writer`, `canvas`
   and `skill-builder` (added the first time Skills → *New skill* is opened) → Model
   → `deepseek-flash`; for Full, `music-librarian`, `data-analyst` and the workshop agents → Model →
   `gemini-flash`. The finance, HR, legal and security agents and the presenter refuse cloud models
   by policy (their `egress` says so), so they stay on the local model whatever the default is; a
   cloud default would stop them, and the eval judge too.
6. Admin → Policy → **Answer checks**: leave the checks on, and set *Model for decisions* to the
   local chat entry. The second-model judge and the grades (scenario 22) then run on the local model,
   where the engine returns token probabilities; nothing about an answer leaves the Mac to be judged.
7. On a 24 GB Mac, load only what the day needs: the chat model and the embedding model, and the
   voices only for scenario 0. The models, the engine's prompt cache and a browser fill 24 GB;
   once the Mac swaps, a reply that takes seconds takes minutes. Close other large apps, and start
   a scenario only when the Knowledge tab shows every store *indexed*: the engine serves requests
   side by side, and a chat slows while a store is still embedding.
8. Open the Studio in two browser profiles (or one normal and one private window) so you can be Dana
   in one and another person in the other without signing out. Scenario 14 needs a third window with
   no session at all.
9. For scenario 24 and the ones that continue from it (31, 32, 33; all Full): Claude Code on the
   Mac, the `ai-stackops` command on the PATH (the same binary the host runs), and a clone of
   `https://github.com/alexborhani/meridian-pump-controller` in a folder of its own. Scenario 28 needs
   the `ai-stackops` command too.

**The people you will be**

| Sign in as | Tier and roles | Clears | Use them for |
| --- | --- | --- | --- |
| Dana | admin | restricted, every category | policy, approvals, audit |
| Sam | builder, firmware-engineers | internal, and confidential Security | building: agents, workflows, skills, schedules, the IDE, the firmware repository |
| Priya | member, staff | internal | the everyday employee |
| Marcus | member, staff, hr-partners | confidential within HR | people questions |
| Lena | member, staff, finance-analysts | confidential within Finance | finance questions |
| Jordan | member, contractors | public | the outsider inside the building |

**Reset between runs** is at the end of this document. The whole pack can be uninstalled and
reinstalled in under five minutes, which returns every account, store and policy to the starting state.

---

## 0. Meet the presenter
**Level:** Standard, on a Standard-class local model: the presenter refuses cloud models (its
`egress` says so), and a 9B does not drive it reliably (measured: Qwen 3.5 9B started a scenario in
0 of 3 runs).


*Optional opener: the platform introduces itself, in a voice the room chooses, and can present the
rest of the day on request.*

**You are** Dana. Agents → `presenter`. The engine needs the Kokoro voices and the cloning TTS model
(see *Voices on the engine* below).

1. Above the chat, the voice bar: press *Voice* and let the audience pick **Emma** or **Michael**. The
   presenter introduces itself in that voice under that name, and *Read replies aloud* is on: every
   reply from here is spoken, one paragraph at a time.
2. Ask: **"What is the enforcement mode right now?"** The presenter checks the platform and answers in
   a sentence or two, spoken.
3. Ask: **"Run scenario 4."** It reads the script from the `demo-scripts` store and gives you the first
   step only: who must be signed in and in which window, what to do there, and what the room should
   see. Do it in that window, then say **"next"**; it never moves on by itself. Where a step is a
   switch it holds (enforcement, the classifier, evaluations, the member cap) it flips it in that
   same turn and says so. A question in the middle gets a spoken paragraph and "say next when you
   are ready"; the last step ends with the scenario's closing point.
4. *Lend your voice*: an audience member types their first name, agrees on screen, reads the passage,
   ten seconds record with a meter, and the presenter carries on in their voice under their name —
   "I'm Alex, or at least I sound like him today." *Forget this voice* deletes the clip, audited; the
   presenter falls back to the preset the room chose. Say: nothing was trained and nothing left the Mac.

**Land:** the product can explain itself, run its own demonstration, and prove the data-lifecycle
promise on a volunteer's own voice in under a minute.

**Voices on the engine.** The presets are Kokoro voices; the lent voice uses the cloning TTS model.
Both models are pulled once. MLX Serve's pull skips a repository's subdirectories, so two files must
be fetched by hand after the pull, and the engine lists a pulled model by its bare name:

```
# in the engine's models directory (MLX Core: ~/.mlx-serve/models of the account running it)
curl -X POST localhost:11234/api/pull -d '{"model":"ddalcu/Kokoro-82M-MLX-Serve"}'
mkdir -p ddalcu/Kokoro-82M-MLX-Serve/g2p && for f in gb_gold us_gold us_silver; do
  curl -sL https://huggingface.co/ddalcu/Kokoro-82M-MLX-Serve/resolve/main/g2p/$f.json -o ddalcu/Kokoro-82M-MLX-Serve/g2p/$f.json; done
ln -sfn "$PWD/ddalcu/Kokoro-82M-MLX-Serve" Kokoro-82M-MLX-Serve
curl -X POST localhost:11234/api/pull -d '{"model":"mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit"}'
mkdir -p mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit/speech_tokenizer && curl -sL \
  https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit/resolve/main/speech_tokenizer/config.json \
  -o mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit/speech_tokenizer/config.json
# then restart the engine (quit and reopen MLX Core): it discovers the files at start-up
```

Then Models tab → activate the Qwen3-TTS entry for the *tts* role, and load Kokoro once from the Local
LLM tab (it stays resident; both fit beside Qwen 3.5 9B). The presenter's presets name the model as the
engine lists it, `Kokoro-82M-MLX-Serve`.

---

## 1. Day one: a governed estate before lunch
**Level:** Essentials.


*For the audience: what "governed" looks like on the first morning, without a services engagement.*

**You are** Dana. **Windows:** one.

1. Admin → Setup. Point at the *Setup health* button and its percentage. Open it: every line is a
   control with its status, the fix, and the tab that fixes it. Green groups are collapsed; only what
   needs a decision is open. Say: the platform never blocks on a missing control, it reports it.
2. Admin → Policy → Classification. Show the four levels and the categories the pack adopted from the
   written policy, the tier clearances, and the *Enforcement* panel showing **Off** in red. Say: the
   policy is loaded and idle; scenario 4 turns it on in front of them.
3. First give the classifier its model: a pack does not set the host's classifier, and *Extract
   criteria* needs one. Under *Background classifier*, *Model (a local chat entry under Models)*:
   type the local chat entry's name, `mlx-serve`, and press *Save taxonomy*. The status line under
   it reads *classifier ready on mlx-serve*. Then scroll to *Written policy*. This is the
   organisation's own document, stored beside the taxonomy, hashed and versioned. Press *Extract
   criteria*: the local model reads the policy and proposes
   levels with criteria, categories, clearances and handling rules. Compare the proposal with the
   editor above it. Nothing applies until an admin copies it in. *Needs room:* the policy is about
   1,500 tokens; at 4K the proposal may come back short.
4. Scroll to *Compliance* → *Check now*. Every finding is a gap between what the policy requires of a
   level and the actual configuration, with the change that fixes it. The first finding is the
   enforcement mode itself.
5. Admin → Estate → **Licence**: the edition, the people and nodes in use against its limits, and
   the date it ends; renewal is a new key pasted here, never a reinstall. Admin → Policy →
   **Answer checks**: the rules every answer meets before anyone sees it (scenario 22).
6. Packs tab. Open the pack card (*Details*): signed by AI Stack Ops, certified tier, publisher key id,
   what it seeded. Below the cards, the trusted publishers panel: the minimum tier the host accepts. Say: capability arrives as
   signed packs, installs in one line, uninstalls completely, and unsigned packs can be refused
   estate-wide.

7. Still on the pack card: *Update* and the *auto* switch. Say: a pack is kept current from the same
   publisher without reinstalling — accounts keep their passwords, unchanged stores keep their index,
   an edited policy is kept — and a pack you trust can take its updates from the daily check on its
   own, every one of them audited. *Check for updates* asks every source now.

**Land:** the controls a security review asks for exist on day one, are visible on one page, and every
one names its fix. Nothing here required a consultant.

---

## 2. The new starter's first day
**Level:** Essentials.


*Self-service that deflects the tickets IT and HR answer every week, and a hard line the assistant
will not cross.*

**You are** Jordan (contractor) in one window, Marcus (HR partner) in the other.

1. As Jordan, Agents → `helpdesk`. Ask: **"My VPN certificate expired, what do I do?"** The helpdesk
   answers from the VPN reset runbook and quotes the step.
2. Ask: **"What are the core working hours?"** Answered from the handbook: 10:00 to 15:00. (Leave and
   pay questions are different: the helpdesk hands those to People Operations, as step 4 shows.)
3. Ask: **"The plant floor lost network, what do I do first?"** The outage runbook, first step first.
4. Now ask: **"Please ask People Operations for me: what is the 2026 band for a senior engineer?"**
   The helpdesk hands the question to the people-partner agent (the `agent_people_partner` tool) and
   the handoff is refused: Jordan holds no HR role, and a handoff is checked against the person, never
   the helpdesk. The reply says People Operations information is not available to him here.
5. As Marcus, same agent, same question. This time the handoff goes through and the band comes back
   from the compensation document. Admin → Audit as Dana: filter action `agents.handoff`, two rows,
   one denied, one success, same helpdesk, different people.

**Land:** agents extend what a person may do, never what they may see. The same assistant is safe for
a contractor and useful for an HR partner without anyone building two assistants.

---

## 3. Who can see what
**Level:** Essentials.


*RBAC, custom roles and clearances applied to real questions by four people.*

**You are** each of Jordan, Marcus, Lena, Dana in turn (two windows, swap the second).

1. As Jordan, Agents tab: count the agents. `people-partner`, `finance-analyst`, `counsel` and
   `security-lead` are not listed at all. Knowledge tab: `people-files` and `finance-close` are listed,
   but *Search* inside them answers `knowledge_access_denied`.
2. As Marcus, `people-partner`: **"What is the 2026 band for a senior engineer?"** and
   **"Summarise Priya Nair's last review."** Both answered. Then `finance-analyst`: not listed.
3. As Lena, `finance-analyst`: **"What was Q2 2026 revenue against the forecast?"** Answered.
   `people-partner`: not listed.
4. As Dana, Admin → People → Roles: open `hr-partners` and `finance-analysts`. Each is a handful of
   permissions plus a clearance (confidential, one category). Open the audit log, filter
   `knowledge.access.denied`: Jordan's attempts, with the reason.
5. Say who decides a request for more: each restricted agent and store names its owners (Marcus
   for the people partner and the HR files, Lena for the finance analyst and the close package).
   A request goes to them, not to a queue in IT; scenario 21 shows it.

**Land:** one platform, one set of stores, and each person sees exactly their slice, enforced at
retrieval on every chunk, not by which assistant they were given.

---

## 4. Classification, switched on in front of them
**Level:** Essentials.


*The difference a policy makes, shown as before and after with the same questions.*

**You are** Dana in one window, Jordan in the other. Store: `all-hands`, eight notices at every level in
one public store; agent: `announcements`.

1. As Dana, Admin → Policy → Classification: enforcement is **Off**. Say what that means: the policy
   is loaded, the levels are on every document, and nothing checks them.
2. As Jordan, `announcements`: ask the four sample questions in turn: the town hall (public), the
   Riverside restructuring (confidential HR), the Q3 results (confidential Finance), the plant USB
   incident (restricted). Every answer comes back in full, severance terms and revenue figures
   included. Nothing is recorded.
3. As Dana, set **Monitor**. As Jordan, ask the same four again: identical answers. As Dana, refresh
   the panel: it now counts the reads the policy would have refused. Admin → Audit, filter
   `classification.monitor`: one row per search, naming Jordan, the store, the levels and why.
4. As Dana, set **Enforce**. As Jordan, ask again: the town hall answers; the other three come back as
   "nothing has been announced". Same store, same agent, same person.
5. Optional: as Marcus ask about the restructuring (answered, HR) and the Q3 results (not); as Lena
   the reverse.

**Land:** the policy can be measured before it is enforced, then enforced without touching a single
document, agent or store. Monitor mode is how you take a sceptical organisation from chaos to control
with evidence at each step.

---

## 5. Classify what nobody labelled
**Level:** Essentials.


*The unglamorous truth of every estate: most content carries no label. Here it gets one.*

**You are** Dana. Store: `site-notes`, six Riverside notes as staff wrote them, none labelled.

1. Knowledge → `site-notes` → *Sources*. Every note reads at the store default, decider *store default*.
2. Press *Classify* on the workshop incident note (the injury): set confidential, tick HR, give a
   reason, *Save*. Applied at once; Audit shows `knowledge.classify` with the reason.
3. Press *Classify* on the parking note and set it public: it goes to the review queue instead,
   because that would lower it. Admin → Policy → Classification → *Reviews*: approve it there. Say:
   raising is a person's call, lowering is a second person's.
4. Admin → Policy → Classification → *Background classifier*: the model is the local chat entry,
   `mlx-serve`, if scenario 1 set it; if not, type it and press *Save taxonomy*. Back on *Sources*,
   *Send undecided to the classifier*: four notes go *pending*. Refresh every ten seconds. Within a minute each carries a level, categories and the classifier's confidence:
   the customer visit confidential Finance, the badge follow-up restricted Security, the checklist
   internal, the volunteers note public or internal. The note a person decided is untouched.
5. Admin → Policy → Classification: the classifier status and the backlog count, now zero.

**Land:** classification is not a project. It is a background service driven by the organisation's own
criteria, with a person in the loop only where the policy says so.

---

## 6. The finance close in a conversation
**Level:** Essentials.


*Numbers from the close package, with arithmetic done by a tool rather than the model.*

**You are** Lena; Jordan in the second window for the last step. *Needs room:* the close package
chunks plus the calculator exceed 4096 tokens; at 16K the question is one round.

1. As Lena, `finance-analyst`: **"What was Q2 2026 revenue against forecast, and by what percentage
   did we miss or beat?"** The agent reads the close package and the forecast, then calls the
   `calculator` function for the percentage. Open the tool trace under the reply: the search calls,
   the calculator call with its inputs.
2. **"Which items on the month-end close checklist are still open for September?"**
3. **"What changes in the 2027 pricing, and which customers are affected first?"**
4. As Jordan, `finance-analyst` is not listed; open the URL of the agent directly if you like: refused.

**Land:** the analyst's question is answered from the controlled close package in seconds, the maths
is deterministic, and the answer never reaches anyone outside the finance role.

---

## 7. The incident copilot, with a human on the trigger
**Level:** Essentials.


*An agent that can act, and the approval that stands between it and the action.*

**You are** Dana. Two windows help: one for the chat, one for Approvals. *Needs room:* the incident
record, the access review and the revoke call together exceed 4096 tokens.

1. `security-lead`: **"What is still outstanding on INC-2026-021, and who is responsible?"** The
   agent reads the incident record and the access review and lists the open actions.
2. **"Revoke the access of the contractor holding badge 4471, reason INC-2026-021."** The agent calls
   `revoke_access`. The run pauses and an approval card appears in the chat: the tool, the arguments
   as the agent proposed them, a hash of them.
3. In the other window, Approvals (or the card itself): *Approve*, with a note. The run resumes, the
   function records what it would have done, the agent confirms.
4. Admin → Audit, filter `tools.approval`: requested, granted, with the approver as actor and the
   arguments hash. Point out `tools.fragment.yaml` in the pack: three lines made this tool
   approval-gated for every agent that has it.

**Land:** agents can be given real actions because the action waits for a person, the arguments cannot
change between approval and execution, and both halves are on the record.

---

## 8. Counsel on a restricted matter
**Level:** Essentials.


*The most sensitive store on the estate, in use, and invisible to everyone else.*

**You are** Dana; Jordan in the second window.

1. As Dana, `counsel`: **"Where do we stand with the regulator this year, and what is due next?"**
   Answered from the regulator correspondence record.
2. **"Summarise the Crestview lease dispute and our exposure."**
3. Show the agent's definition (Agents → counsel → edit, read-only glance): `access: minRole: admin`,
   `egress: allowFrontier: false`. The store `legal-matters` is restricted, Legal, admin-only,
   local-only.
4. As Jordan: no `counsel` in the list; Knowledge → `legal-matters` search: refused.
5. As Dana, Admin → Policy → Classification → *Compliance*: the handling rule for restricted requires
   access restriction and local-only processing, and the store meets both.

**Land:** the same platform that answers a contractor's VPN question holds counsel's files, and the
policy's handling rules are checked against the configuration, not promised.

---

## 9. A customer notice by the playbook: drafted, signed off, filed
**Level:** Standard.


*A procedure the organisation wrote down once, followed by an agent every time: it asks for what
it needs, drafts in house style, and waits for a person before anything goes on the record.*

**You are** Sam (builder) in one window, Dana in the other for the sign-off.

1. As Sam, `writer`: **"Draft a customer notice about the 2027 price list."** It asks for the
   effective date before drafting anything: the playbook declares it as a required input, and a
   required input is asked for, never guessed.
2. **"1 November 2026, for all customers."** Open the tool trace under the reply: the writer loaded
   two skills by itself, `house-style` and `customer-notice` (`load_skill`), because the request
   matched their descriptions, and read the playbook's `references/notice-rules.md`. The canvas
   opens with the notice: what changes, from when and for whom in the first three lines, clause 7.2
   and the 30 days' notice, the service desk as the contact.
3. **"File it."** The writer calls `knowledge_add`, and the run pauses: an approval card, because
   the playbook says filing a customer notice needs an administrator, and a different person from
   the one who asked. Sam cannot approve it.
4. As Dana, Approvals: the card names the tool, the title and the store. *Approve*, with a note.
   The run resumes; Knowledge → `scratchpad` → *Sources*: the notice, added by Sam. Admin → Audit:
   `skills.loaded` (which skills, which version), `tools.approval.requested` and `.granted`, and
   `knowledge.add` with the title and never the text.
5. Skills tab → `customer-notice`: the playbook as the organisation wrote it: the inputs, the
   approval and who gives it, the *Done when* list, the reference file.

**Land:** a procedure the organisation wrote down once, not a prompt someone remembered: the agent
asks for what it needs, follows the house rules, and the step that matters waits for a person.

---

## 10. A notice that improves itself
**Level:** Standard.


*A workflow where one agent drafts and another judges, until the reviewer is satisfied.*

**You are** Sam. Workflow: `customer-notice` (an evaluator loop). *Needs room:* three rounds of draft
and review; at 4096 the run completes but each round crawls.

1. Workflows → `customer-notice` → *Run* with subject **"the 2027 price change effective
   1 November"**. Watch the run: round one, the writer drafts; the helpdesk, acting as reviewer,
   scores it with feedback; round two addresses the feedback; the loop stops when the score clears
   the threshold or after three rounds, keeping the best.
2. Open the run's step metadata: rounds, the score per round, the final feedback. Open the workflow
   definition: eleven lines describe the loop, the threshold and what happens when rounds run out.
3. Say: the reviewer here is a local model; in production it can be a stricter agent, a function, or a
   different model entirely. *Needs room:* three rounds of draft plus review fit comfortably at 16K.

**Land:** quality is a loop, not a prompt. The organisation decides the bar and the platform iterates
to it, with every round recorded.

---

## 11. An incident brief from two agents in parallel
**Level:** Standard.


*Fan-out and merge: two specialists work at once, and the workflow refuses to pretend a missing half
arrived.*

**You are** Dana. Workflow: `incident-brief`. Two to three minutes end to end at 4096; faster at 16K.

1. Workflows → `incident-brief` → *Run* with incident **"INC-2026-021"**. Two agents research in
   parallel: the security lead reads the incident and access review; the helpdesk reads the runbook
   side. A merge step joins them into one brief.
2. Open the run: the parallel block, each branch's output, the merge record showing what was expected
   and what arrived. Say: if one branch fails, the merge guard marks the run failed rather than
   shipping half a brief as if it were whole.
3. Read the brief aloud: what happened, what was done, what is open.

**Land:** this is how the platform composes specialists into a process with a deterministic spine.
The agents are the same ones people chat with; the workflow is the management layer.

---

## 12. Work on a schedule
**Level:** Essentials.


*An agent that runs on its own, as the person who set it up, and stops when that person goes.*

**You are** Sam in one window, Dana in the other.

1. As Sam, Agents → `helpdesk` → *Schedule…* in the chat header (or Activity → Schedules → *New
   schedule*). Name **"Weekly VPN digest"**; *What to ask it*: **"Write this week's helpdesk digest:
   how to reset a VPN certificate, in three bullet points from the IT runbooks."**; *Every week*,
   Monday, 09:00, your time zone. *Create schedule*. Activity → Schedules lists it: *Mondays at
   09:00*, when it runs next, *Active*.
2. *Run now* (the bolt). Activity → Runs shows a `helpdesk` run under Sam. When it ends the row says
   *Last: Completed*; open the row for its run history, and *Open in Activity* for the digest, built
   from the VPN runbook.
3. As Dana, Admin → People → Users → Sam → disable. Activity → Schedules → *Everyone's* → Sam's
   schedule → *Run now*. The run is *Skipped*: its owner is disabled. It never runs as Dana, and
   never as the system. Enable Sam again.
4. As Dana, Admin → Audit, filter `schedules.`: `schedules.create` and `schedules.run_now` by Sam,
   `schedules.run_now` by Dana, and `schedules.run` as Sam twice: the run that completed, then the
   skip with its reason.
5. As Sam, delete the schedule (it asks first); its run history goes with it.

**Land:** a timer here is not a service account. A schedule acts as the person who saved it, with
their access, limits and approvals, checked again every time it fires, and every change and every
firing is in the audit log.

---

## 13. An assistant that remembers you, and only you
**Level:** Essentials.


*Personal memory with a boundary the audience can see, and a person's right to see and delete it.*

**You are** Priya in one window, Marcus in the other.

1. As Priya, `assistant`: **"I'm Priya, a team lead at the Halden plant. I start at 6 and prefer
   bullet points."** The assistant keeps a short note (the `save_memory` tool) and says what it kept.
2. Start a new chat as Priya: **"What do you remember about me?"** It recites the note.
3. As Marcus, `assistant`: **"What do you remember about me?"** Nothing. Memory is per person by
   default; the file for Priya is hers alone.
4. As Priya, Account → *Your data*: the memory is listed by agent with a *Forget* button. Press it;
   ask the assistant again; it has forgotten. Admin → Audit as Dana: `memory.forget`.
5. Optional: **"Plan my first hour tomorrow."** The assistant uses what it knows (start time, format).

**Land:** personalisation without a data-protection problem: memory is scoped to the person, visible to
them, deletable by them, and never shared between people or nodes.

---

## 14. A support page for people outside the building
**Level:** Essentials.


*The same governed platform, published to customers, with limits and without any of the internal data.*

**You are** nobody: a third window with no Studio session. Agent: `support` over `product-faq`.

1. Open `/chat/support`. It asks for the page password (`meridian-customer`, standing in for a
   customer-portal login). Say: published pages have their own authentication, separate from staff
   accounts.
2. Ask: **"How often should an MW-300 be serviced?"** Answered from the product FAQ with the
   intervals. **"My pump is two years old and leaking at the seal, is that under warranty?"** The
   warranty terms, and the service desk contact.
3. Ask something internal: **"What happened with the USB incident at the Halden plant?"** The page
   has one store, the FAQ; it says it cannot help and gives the service desk.
4. As Dana, Admin → Policy → Limits: the *Anonymous* row caps published pages per IP address. Set
   requests per minute to 2, then ask three questions quickly from the customer window: the third is
   refused with a retry time. Admin → Audit: `limits.exceeded` for the anonymous scope. Set it back.

**Land:** one platform serves customers and staff with the same controls: a published page can only
reach the store it was given, and it is rate-limited like any other caller.

---

## 15. Cloud by policy, not by accident
**Level:** Standard.


*Where a cloud model fits: as a governed entry with access, a ceiling and a budget, never as the
default.* Stronger with a cloud key on the host (Anthropic, or OpenRouter — `provider: openrouter`, model
`<vendor>/<model>`, key `${OPENROUTER_API_KEY}`; the steps read the same); complete without one.

**You are** Dana; Jordan in the second window.

1. Models tab → the OpenRouter tab (or Anthropic, or Azure for Claude and OpenAI models in the
   organisation's own Azure tenant) → **New entry**: name `cloud`, model
   `deepseek/deepseek-v4.1-flash` (the model this was measured on; on Anthropic `claude-sonnet-4-6`
   reads the same), key `${OPENROUTER_API_KEY}`, access minimum role admin, budget 1 USD a day,
   pricing 0.30 / 1.20 per million, maximum classification internal. Save. Say: four decisions were just made about a cloud
   model before anyone could use it: who, how much, what data, at what price.

   *With Azure* (**Needs:** an Azure subscription with an Azure OpenAI or Foundry resource and a
   deployment; not tested). The Azure tab → **New entry**: *Resource endpoint*
   (`https://<resource>.openai.azure.com`), *API* **Azure OpenAI** (or **Claude on Foundry**), *Sign
   in with* **API key** or **Managed identity (Microsoft Entra)**, *Chat deployment*, *Data zone*
   (EU, US or global: recorded, so the evidence bundle says where the model ran). Access, ceiling,
   budget and pricing as for any cloud entry. Say: the model runs in the organisation's own tenant
   under its own agreement; with managed identity there is no key to leak. The steps that follow
   read the same with the Azure entry.
2. Agents → *New agent* `board-analyst`: model `cloud`, tool `knowledge:handbook`, prompt "You are a
   concise business analyst." Save.
3. As Jordan, `board-analyst`: **"Summarise our values in one line."** Refused before anything is
   dialled: access to model `cloud` needs role admin. Admin → Audit: `model.access.denied`.
4. As Dana, same question. With a key on the host, the answer comes from Claude and the usage row
   carries the cost at the pricing you set. Without one, the attempt reaches the provider and is refused
   by them; the point stands: the only person who could reach the cloud was the one the policy allows.
5. Try `counsel` with the cloud entry (edit its model to `cloud`): refused for everyone, because the
   agent and the legal store both say `allowFrontier: false`. Then Admin → Setup: the checklist
   shows the cloud entry needs a budget and access (it has both), and the compliance report says
   whether any restricted store could reach it (it cannot, ceiling internal).
6. Mention the operator lock: `EGRESS_ALLOW_FRONTIER=false` in the host's environment refuses every
   cloud call for everyone, and no setting in the Studio can override it. Step 8 shows it live.
7. The router, local first and cloud only when the local model cannot: IDE tab → `models.yaml`, add an
   entry `frontline` with `provider: router` and `candidates: [mlx-serve, cloud]`, and set `helpdesk`'s
   model to `frontline`. As Dana, `helpdesk`: **"How do I reset my VPN certificate?"** — answered by
   the local model; Admin → Audit, `models.route`: candidate `mlx-serve`, reason *first candidate*.
   Then open `bundles/aiso-demo-pack/long-reads/riverside-commissioning-report.md` in the IDE tab
   (320 test records, about 19,000 tokens — more than the local engine's window), copy all of it into
   the chat and ask: **"How many of these tests failed, and which fault was most common?"** The router
   skips the local model before dialling — the audit row's reason says *fit: mlx-serve (context …)* —
   and the cloud entry answers; the answer key is beside the report. As Jordan, the same paste is
   refused: the local model does not fit and the cloud entry is not his to use.
8. Optional, the operator lock live (it needs a restart of the host, so do it last; not yet run,
   measured: pending). Quit AI Stackops and start it again with `EGRESS_ALLOW_FRONTIER=false` in its
   environment (the deploy kit's service environment, or `EGRESS_ALLOW_FRONTIER=false ai-stackops
   start`). Models tab: *Frontier providers* **locked by operator**: *Cloud models are off for
   everyone on this node.* As Dana, `board-analyst` (on `cloud`): refused before anything is
   dialled, for the admin too. Admin → Audit: `egress.denied`, reason *EGRESS_ALLOW_FRONTIER=false
   locks this host to local models*. No Studio setting turns it back on; restart without it.

**Land:** cloud models are welcome where the policy says so, with a person, a data class and a budget
attached, and the answer to "did anything leave the building" is in the audit log.

---

## 16. The runaway agent
**Level:** Essentials.


*Budgets and rate limits as circuit breakers, per person, per agent, per model, on real answers
and real dollars.* Stronger with the `deepseek-flash` entry from *Before the day*; complete without
one (see the end).

**You are** Dana; Priya in the second window. A run is about ten helpdesk answers, a cent or two on
DeepSeek V4.1 Flash; the entry's 1 USD a day stops anything beyond that.

1. As Dana, Agents → `helpdesk` → edit its model to `deepseek-flash`. Save. Say: the most-used
   assistant in the building now runs on a paid cloud model, and three fences sit around it.
2. As Priya, `helpdesk`: **"How do I reset my VPN certificate?"** The cloud model answers from the VPN
   reset runbook and quotes the step. As Dana, Usage tab → the *Model entries* table → `deepseek-flash`:
   one row, its tokens and its cost at the pricing on the entry, a fraction of a cent. Note that per-answer cost; step 4
   uses it.
3. **The person fence, by rate.** Admin → Policy → Limits: member tier, Requests / min **2**. Save.
   As Priya, ask three in a row without waiting: **"The plant floor lost network, what do I do
   first?"**, **"A print job is stuck in the queue, how do I clear it?"**, **"What does IT set up
   for a new starter on day one?"** Two answers; the third is refused with *Limit reached: 2
   requests per minute for priya — retry in …s*. Wait it out, ask the third again: answered.
   The count is questions, not model calls. Set Requests / min back to empty.
4. **The model fence, by spend.** As Dana, Usage shows what `deepseek-flash` has spent in the last 24
   hours. Models tab → the OpenRouter tab → pick
   `deepseek-flash` in the list of entries above the form → USD / day: type that figure plus about
   three answers' worth (spent $0.008 and about $0.001 an answer: **0.011**). Type it; the arrows step
   by 0.50. Save. As Priya,
   keep asking runbook questions (**"How do I rebuild my laptop?"**, the VPN question again). A few
   are answered, then: *Limit reached: $… per day for model entry "deepseek-flash" (used $…).
   It frees up as the rolling 24 hours pass; an admin can raise it in the model entry's budget on
   the Models tab.* The check runs before each call, so the answer that crosses the line still
   arrives and the next one is refused. Usage: Priya's rows add up to it, at the price you set,
   and the same calls are on the OpenRouter bill.
5. Admin → Audit, action `limits.exceeded`: the rate refusal (scope principal) and the spend
   refusal (scope model), each throttled to one row per five minutes so a loop cannot flood the
   log.
6. Show the third scope without running it: an agent's own `limits` (runs per minute, spend per
   month) in its definition. Say: a runaway loop, a leaked API key, or an over-enthusiastic pilot
   all hit the same three fences.
7. Reset now (the list at the end): `helpdesk` back to `default`, `deepseek-flash` back to 1 USD a day.

*Without a cloud key:* skip step 1 and give the `mlx-serve` entry pricing 0.30 / 1.20 per million on the
Models tab. The local model answers, Usage prices each call as if it were DeepSeek V4.1 Flash, nothing is billed,
and steps 3–5 run the same with `mlx-serve` in place of `deepseek-flash`. A 9B answer may use more
tokens than the cloud model's, so read the per-answer cost from Usage before setting the cap. Remove the
pricing afterwards.

**Land:** spend and load are bounded by policy before they become an invoice, and every refusal is
recorded with who, what and how much.

---

## 17. Evaluations as the release gate
**Level:** Standard.


*Change an agent's knowledge and know, before anyone notices, whether it still answers correctly.*

**You are** Sam for the change, Dana for the run.

1. Admin → Setup → *Evaluations*: `helpdesk.eval.yaml`, three cases, threshold 50 percent. *Run*.
   Each case shows pass or fail with its checks: a phrase that must appear, a phrase that must not,
   a judgement by the local model. Expect a pass.
2. As Sam, IDE tab → `bundles/aiso-demo-pack/it-runbooks/vpn-reset.md`: change the new certificate's
   validity from 12 months to 6 months. Save. Knowledge → `it-runbooks` → *Re-index* (a few seconds;
   only the changed file is embedded).
3. As Dana, *Run* the helpdesk evals again: the VPN case fails. Its pattern check expects the
   12-month validity the runbook used to give, and the agent now answers 6 months from the runbook.
   Point at the check detail: this is the eval catching a change in what the agent says.
4. Undo the change, re-index, run once more: green.
5. Skills carry their own evals, beside the skill (Skills tab → a skill → *Evals*): whether agents
   pick it for the requests it is for and leave it alone for near misses, and whether answers are
   better with it. Scenario 23 runs one.

**Land:** knowledge and prompts change every week; evals turn "we think it still works" into a
number on a page, and the run is audited.

---

## 18. On the record
**Level:** Essentials.


*The audit trail, the usage ledger, chargeback and a signed evidence bundle: the paperwork a
security review or an auditor asks for, produced by the platform.*

**You are** Dana. Best after a few of the earlier scenarios have run.

1. Admin → Audit. Filter by action: `knowledge.access.denied`, `classification.monitor`,
   `tools.approval.granted`, `models.route`. Every row has the actor, the target, the outcome, the
   reason and a request id that matches the engine call. Say: the log is hash-chained; a removed or
   altered row breaks the chain. Press **Verify chain**: every link checked, and where the check
   starts. Filter `answer.recorded`: one row per answer, with its record hash.
2. Admin → Audit → **Look up an answer**: paste a run id from any Sources line. The answer's record
   opens: who asked, each step with its statement and row count, the figures checked, the grade.
   Which skills shaped it, and which version, is in the audit rows `skills.loaded` for the same
   run. Scenario 22 keeps and verifies one.
3. Usage tab: calls, tokens and cost by person, by agent, by model entry, by kind, by day, and by
   development project. Click a person to drill. **Export 30 days (CSV)**: one row per month, person,
   agent, model entry and project, ready for chargeback: a Claude Code project's spend is its own
   line. Scenario 33 walks it.
4. Admin → Data → *Evidence bundle*: choose the last 30 days, download. One JSON file, signed with the
   workspace key, containing the setup checklist, the compliance report, the taxonomy version, the
   packs, the limits, the usage totals, the development projects and the audit rows. Open it and
   show the signature block.
5. Admin → Estate → *Estate report*: nodes and active people, signed the same way.

**Land:** nothing here was assembled by hand for the meeting. The evidence a control framework asks
for is a download, and it is tamper-evident.

---

## 19. A person leaves
**Level:** Essentials, no chat model. Measured (2026-10-01): end to end three times in a row, every step
passing, after scenario 39 each time.


*Subject access, a legal hold that stops every deletion, erasure and the grace period, with the audit
log kept intact.*

**You are** Dana; Lena in the second window for step 3. Best after scenario 39, which leaves Lena her
`Board prep` space; without it, have Lena make any space and upload a file from `space-files`.

1. Admin → People → Users → Jordan → the download icon (*Export their data first* on the delete
   dialog does the same): one JSON with the account, the roles, the
   documents Jordan added, the memories, the usage rows and the audit rows Jordan is the actor of.
   Say: this is the subject-access request, answered in one click.
2. Admin → Data → *Legal hold*: set it, with a reason (*Northfield dispute*). The Setup checklist shows
   it; every prune stops.
3. As Lena, Spaces → `Board prep` → **Delete**. It leaves her list with a note: kept under a legal hold,
   deleted when the hold is cleared. As Dana, the *Legal hold* panel counts one kept item. Say: under a
   hold a person's own delete hides; it does not destroy.
4. *Export held content* → person **lena** → *Export*: one JSON file signed with the workspace key, holding
   the deleted space and the text of its documents, who deleted it and when. Admin → Audit, `hold.export`:
   the filters and the counts, never the content.
5. People → Users → *Delete disabled accounts* → **After 30 days**. Disable Jordan (his contract ended):
   his row reads *disabled*, *deleted on* a date 30 days out. Say: a deactivation, which is what a SCIM
   delete does, keeps the account and everything in it for the grace period so a returning person finds
   it all; after that the account goes with its content.
6. Now **Erase** Jordan, with a reason. Under the hold it waits: the row reads *deletion waits for the
   legal hold*, and the erasure is recorded.
7. Admin → Data → clear the hold. The toast: one kept item deleted, one deferred deletion done. Lena's
   space is gone for good; Jordan is erased: keys revoked, memories and added documents removed, usage
   rows pseudonymised, the account deleted. Admin → Audit: `users.erase` by *legal-hold* lists the
   steps; the rows that name Jordan as the actor are untouched. Set *Delete disabled accounts* back to
   *Never*.
8. Say: reinstalling the pack brings Jordan back for the next demo.

**Land:** the data-protection lifecycle is built in, per person: a hold stops every deletion, people's
own included, everything it held back runs when it lifts, and the audit trail is the one thing never
edited.

---

## 20. Two nodes, one policy
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

## 21. One chat for everyone
**Level:** Essentials.


*A member never picks an agent. Chat answers from what they may use, refuses the rest
by name, and asks the people who own it on their behalf.*

**You are** Jordan, then Marcus, then Dana (two windows).

1. As Jordan, the Chat tab (it is the only chat a member has; the workshop tabs are gone). Ask
   **"How do I reset my VPN certificate?"** Chat hands the question to the helpdesk and answers
   from the runbook, naming it.
2. Still as Jordan: **"How much holiday do I carry over at year end?"** Chat says the people
   partner owns that and it is outside Jordan's access, and offers to ask. Say **"Yes, please ask
   the people who decide access for me."** Chat confirms the request was sent; a card under the
   reply shows it waiting.
3. As Marcus, Approvals → *Access requests*: Jordan's request is here because Marcus owns the
   people partner (its *Owners* list names him), not because he is an admin. An owner has one
   choice: *Grant access to "people-partner"*, that agent and nothing else, never a role. Grant it
   with a note.
4. As Jordan, without signing out (the card under the reply turns *granted*): **"How many days of
   annual leave do I get?"** It now reaches the people partner, which answers from the handbook:
   25 days, 28 after five years. The HR files stay closed: the grant opened the agent, and Jordan's
   clearance is still public.
5. As Dana, Approvals shows the same request, answered by Marcus as owner; an admin could have
   assigned a role instead. Admin → Audit: `access.request`, `access.grant` with *as: owner*, and
   *Chat routing* lists Jordan's refused route and his successful one.
6. As Marcus, Account → *Access you granted*: Jordan and the people partner. *Revoke*. Jordan's
   next question is refused again.

**Land:** one chat for members, resolved per person on every request; access is asked of the
people who own the thing, granted for that one thing, and taken back in one click, all on the
record.

---

## 22. Numbers you can check
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
   appears. Sources: *Governed* (or *Mixed*, if the librarian also searched the catalogue), the named
   query `customer_purchases`, 38 rows, *Figures found in
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

## 23. Skills: built by interview, proven by evals, offered by policy
**Level:** Standard (the skill builder needs a Standard-class model; on a 9B it drafts slowly and
unreliably).


*How a procedure gets into the platform: the person who does the work is interviewed, the draft is
checked, its evals decide whether it may be offered widely, and an admin decides where.*

**You are** Sam (builder), then Dana.

1. As Sam, Skills tab → **New skill**. The skill builder asks about the work one question at a time.
   Answer as a service coordinator: **"I handle warranty claims for the service desk. A customer
   reports a fault on a pump under warranty. I check the serial number and the purchase date, check
   the fault is covered (seals, bearings and the controller are; damage and misuse are not), and if
   it is, book a field engineer. Claims over 2,000 pounds need sign-off from the service manager.
   It is done when the claim is approved with a booking, or refused with the reason."** Then give
   two real examples and a near miss when it asks: **"Claim for MW-300 serial 0412, seal leak,
   bought March 2025"**, **"Is this pump covered? It is a controller fault"**, and the near miss
   **"How many warranty claims did we have last quarter?"**.
2. The builder says which form fits (a skill, a workflow, or a skill that starts one) and why, then
   drafts. Under the conversation: the draft file by file, `SKILL.md` with its inputs (serial
   number, purchase date, fault), the steps, a *Done when* list, and `evals/evals.yaml` built from
   the examples, the near miss marked *should not trigger*. Read the warnings: if the draft puts
   the manager's sign-off under approvals against a tool this workspace does not have, the check
   says it would pause nothing, and the builder asks which system books the engineer. Say: an
   approval is only real if it pauses a real tool; the checks will not let a draft pretend.
   **Save skill**: Sam owns it; its evals start.
3. Open the new skill: **Evals** shows the trigger cases (was the skill picked for the requests and
   left alone for the near miss) and the answers with the skill against without it, on the host's
   model. *Versions*: this one, with its fingerprint.
4. As Dana, Skills → `customer-notice` (the playbook from scenario 9) → **Where it is offered** →
   *Every agent* → Save. Refused while its evals have not passed on this version: *Run evals*
   (a few minutes), then save again. Say: a skill reaches every agent only when a person other
   than its author has reviewed it (a signed pack counts) and its evals pass, including a check
   that it does not take the requests of the skills already offered. The evals run on the model
   the eval file names (`model:` in `evals/evals.yaml`), else the host's default. On a Qwen 3.5 9B
   default the near-miss trigger checks failed in our runs, so the save stayed refused: on such a
   host, name the cloud entry in the eval file first, or show the refusal as the point.
5. Admin → Audit: `skills.draft.save`, `skills.evals.run`, `skills.scope.set` with before and
   after.

**Land:** procedures come from the people who do the work, are tested before they spread, and reach
every agent only when an admin puts them there, with every step recorded.

---

## 24. Coding agents inside the policy
**Level:** Full. Needs Claude Code, the `ai-stackops` command, a clone of
`meridian-pump-controller`, and the cloud entry (see *Before the day*).


*Claude Code works through AI Stackops: the project decides which models it may use, what it may
read, which code may never go to a cloud model, and every line an AI wrote is on the record.*

**You are** Dana in the Studio, Sam in a terminal in the clone.

1. As Dana, **Projects** → *New project* `pump-controller`: repository
   `alexborhani/meridian-pump-controller`, level internal. Models: `claude-gemini-flash` routed to the
   `gemini-flash` entry, and `claude-local-qwen` routed to the local chat entry. Members: Sam.
   A cloud id must contain `claude` for Claude Code's model picker to keep it; to route it to a model
   that is not Claude, set its *Claude Code picker behaves as* to `claude-haiku-4-5` (as `claude-gemini-flash` does).
   With the `gemini-flash` entry on OpenRouter the gateway translates Claude Code's Anthropic calls
   for OpenRouter's Chat Completions API; measured live with Gemini 3.7 Flash.
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
4. `claude`, then `/model claude-gemini-flash`, then: **"What does the service API expose, and who
   owns firmware/safety?"** Claude Code answers through AI Stackops with the project's code map
   (the OpenAPI contract), `code_owners` (`@meridian/safety-engineering`) and `search_docs` (the
   service API guide): one read-only endpoint, owned by the service platform team.
5. **/mcp__aiso-pump-controller__safety-change-review feature/raise-trip** (the project's skill,
   served to Claude Code as a command): it loads the safety checklist from AI Stackops and asks for
   the change's files.
6. **"Show me what firmware/safety/interlock.c does."** Claude Code reads the file on the Mac and
   sends it to the model, and the call is refused before it leaves: *This conversation carries
   classified code from firmware/safety/interlock.c (confidential, 27 lines), which
   claude-gemini-flash may not receive: the model is cleared for internal at most. Switch to
   claude-local-qwen for this work, or remove that code from the conversation (for example
   /clear).* Nothing reached the cloud provider. `/clear` to go on. A careful model may stop one step
   earlier: it calls `code_classification` for the path first, is told the cloud model may not receive
   it, and says so without reading the file. Either way the file stays on the Mac; show whichever
   happened (the refusal, or the `code_classification` call in the transcript).
7. **"Add a bar-to-psi conversion function to src/controller/units.c, next to bar_to_kpa."** Claude
   Code writes it. Commit it on a branch, then `ai-stackops code attest --base main` (with the same
   `AISO_URL`, `AISO_CI_KEY` and `AISO_PROJECT`): *4 lines added (2 long enough to tell), written
   by a model through AI Stackops: 2 (100%), from cloud models: 2 — claude-gemini-flash*, and a signed
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

## 25. Labels the files already carry
**Level:** Essentials for steps 1–6 (no chat model; step 5 needs only the embedding model):
measured end to end on Qwen 3.5 9B, 3 of 3 runs. Step 7 (Chat finding the board pack for Lena) did
not work on the 9B in any run: treat it as Standard, or skip it.


*Most organisations have already labelled their documents in Microsoft 365. The platform reads
those labels from inside the file and files each document at the level the policy gives that label.*

**You are** Dana in one window, Sam in the other. Store: `labelled-files`, nine Word, Excel,
PowerPoint and PDF files, seven carrying a Purview sensitivity label, two that cannot be opened. No
Microsoft 365 tenant is involved: the labels were written into the files for the pack.

1. As Dana, Admin → Policy → Classification → **External labels** → Purview. Five rows map label names
   to levels, and two rows match by label id: *General* and *Confidential - Finance*. Say why: Office
   files saved since 2022 carry only the label's id, not its name, so a mapping by name alone
   misses them. *Partner Shared* has no row.
2. Knowledge → `labelled-files` → *Sources*. Seven files with a level, *Set by* **Purview label**: the
   town hall agenda public, the shift handover and the safety bulletin internal, the Q3 board pack
   confidential Finance, the grievance notes confidential HR, the Northfield memo restricted Legal.
   The shift handover is the Word file with only the id; the grievance notes are a PDF whose label
   sits only in its compressed XMP metadata. No one typed any of these levels.
3. The price list reads at the store default, internal. Its label, *Partner Shared*, has no mapping
   (the server log names it; the Sources panel does not). Press *Classify* on it, set confidential,
   give a reason, *Save*: applied at once. Say: until the policy knows a label, a person or the
   classifier decides.
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

## 27. A policy drafted with you
**Level:** Standard. Every step after the first needs a model: a long interview, a nine-section policy
in Markdown and one tool call with a nested schema. Measured: passed end to end on DeepSeek V4.1 Flash; on Qwen 3.5 9B it ran the interview and filed
a proposal but missed two of eight checks.


*An organisation with no written classification policy gets one by answering eight questions. The
agent proposes; an admin decides.*

**You are** Dana. Agent: `classification-onboarding`. The pack does not ship it yet, and the Studio
offers it only while no policy is adopted (the banner's *Draft one with the onboarding agent*). Before
the day, add it as Dana with `POST /api/admin/classification/onboarding/install`, or run this
scenario on a second install without the pack, where the banner shows. The Meridian policy stays in
force throughout.

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

---

## 28. The model stays put until you move it
**Level:** Full (the kept answers come from the music librarian, which needs the demo-data server).
Needs the `ai-stackops` command on the Mac (as for scenario 24) and both cloud entries from *Before
the day* (`gemini-flash` and `deepseek-flash`). Measured: passed on Gemini 3.7 Flash, with the two
    replay steps (the `ai-stackops` command) not run in the automated pass.


*A model that changes under an organisation changes its answers. Here the model is pinned, a
change is refused, and the switch is tested on the answers people kept before anyone makes it.*

**You are** Dana. **Windows:** the Studio and a terminal. Best after scenario 22 part two, whose
kept answer is replayed here too. Enforcement on Monitor or Off, as for scenario 22 part two.

1. IDE tab → `models.yaml` → the `mlx-serve` entry under `llm`: replace `model: mlx-serve` with the
   model's own name, `mlx-community/Qwen3.5-9B-MLX-4bit`, and add `pinned: true`. Save. Models tab →
   MLX Serve: the chat entry carries a lock and **pinned**. Say: this is the model every agent
   without a model of its own answers with, and from now on nothing moves it by accident. (The name
   matters: the `mlx-serve` alias follows whatever the engine serves, which no pin can hold.)
2. Models tab → the OpenRouter tab → pick `gemini-flash` → **Make default**. Refused: *llm.mlx-serve
   is pinned: "default" currently resolves to it; re-pointing to "gemini-flash" would replace the
   pinned model. Unpin it first (pinned: false) to make this change.* Admin → Audit, action
   `models.pin.bypass`: one row, outcome denied, reason *config-write: …*, Dana as the actor. Say:
   the same refusal meets an edit of `models.yaml` that changes the pinned model, a federation
   setting that would send the work to another node, and a router that would escalate.
3. As Dana, `music-librarian`: ask three questions and **Keep** each answer with a title (the
   reply's Sources line → **Keep** → title → **Keep and sign**):
   **"Find the 5 longest tracks in the catalog"** (title *Longest tracks*),
   **"Which artists have tracks in both Rock and Jazz?"** (*Rock and Jazz*),
   **"What has customer Heather Leacock purchased, and how much did she spend in total?"**
   (*Heather Leacock*). Account → *Kept answers* lists them, with scenario 22's if it ran.
4. In the terminal, with the host's workspace, ask whether the librarian could move from
   `gemini-flash` to the cheaper `deepseek-flash`:
   `WORKSPACE=<the host's workspace> ai-stackops eval --from-kept --model deepseek-flash --agent music-librarian`
   Each kept answer is given to `deepseek-flash` with the librarian's instructions, the question
   and the results it was built from (no query runs again), and checked and graded like a live
   answer. One line per answer: `SAME`, `BETTER` or `WORSE`, its title, the grade before and
   after, and under a worse one the figure the candidate gave that the results do not hold
   (*not in the results: …*) or a figure the kept answer gave and the candidate dropped (*no
   longer given: …*). The last line counts them.
5. Read out the answers that came back worse, by title. Say: this is the release test for a model
   change. It exits non-zero when anything got worse, so it can gate a change the same way the
   evals in scenario 17 do. Run it again with `--model mlx-serve`: the same question of the pinned
   local model. This is how you find out which work can move to open weights, before moving it.
6. To make a switch for real: point the librarian at the model that passed (Agents →
   `music-librarian` → Model), or, for the default, set `pinned: false` and the new model in one
   edit of `models.yaml`. Neither happens by itself.

**Land:** the model under an agent changes only when an admin changes it, and the change is tested
against the answers people kept before it is made, with the ones that got worse named.

*Reset:* IDE tab → `models.yaml` → the `mlx-serve` entry: `pinned: false` and `model: mlx-serve` in
one edit (an edit that drops `pinned` and changes the model together is refused), then remove the
`pinned` line. Kept answers stay.

---

## 29. A chart drawn from the query result
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

## 30. SQL read before it runs
**Level:** Full: the `demo-sql` server (one free-SQL tool, `run_sql`, over a copy of the music
store) and the `data-analyst` agent come with that level. Standard-class model or better: writing SQL over an
unfamiliar schema is beyond what a 9B does reliably. Start on the cloud entry. Measured: passed on Gemini 3.7 Flash (it wrote a LIMIT
itself, so step 3's *Low* grade did not show; the refusal in step 4 did).


*Named queries are governed; free SQL is not. Here free SQL is offered only to builders, read
before it runs, refused when it is plainly wrong, and graded lower than a governed answer.*

**You are** Dana; Priya in the second window.

1. Tools → MCP: two servers over the same database. `demo-data`: every tool chipped **Governed**.
   `demo-sql`: one tool, `run_sql`, chipped **SQL · builders**. Say: the question is not whether a
   model can write SQL but who may ask it to, and what reads it first.
2. As Priya, `data-analyst` is not in her list (the agent is for builders). Open the agent's
   definition as Dana: `access: minRole: builder`, and even without that the SQL tool itself is
   withheld below builder. Members get named queries; builders get SQL.
3. As Dana, Admin → Policy → **Answer checks** → *When a query has a known mistake*: it is on
   **Run it and note the problem** (the default). `data-analyst`: **"Show me everything in the
   Track table."** A model asked that writes `SELECT * FROM Track` with no limit. It runs; under the
   reply, open the step: the statement, and under it a warning *SELECT * from Track with no LIMIT
   returns every row and column…*. The grade is **Low**, and its reasons name the query.
4. Switch it to **Refuse it**. Save. Ask the same question in a new chat. The query is refused
   before it runs, the model reads why (*this query was refused by the SQL check before it ran …
   Fix the query and run it again*), rewrites it with named columns and a LIMIT, and the second
   statement runs. Open the steps: the refused one, with the finding, marked failed; the one that
   ran, clean.
5. **"How much has each customer spent in total?"** The model joins invoices to invoice lines and
   sums. That is allowed, and the step carries a note: *The query sums or counts across a join …*.
   The Sources line says **Ad hoc**, not Governed, and the grade is **Medium** at best: *Figures
   come from SQL written for this answer, not a governed metric.* Compare scenario 22's Heather
   Leacock answer from a named query: Governed, High.
6. Set *When a query has a known mistake* back to **Run it and note the problem**.

**Land:** free SQL is a builder's tool, read before it runs; the plainly wrong shapes are sent back
to be fixed, and an answer built on SQL written on the spot says so in its label and its grade.

---

## 31. A project's budget, its background calls, and a second admin
**Level:** Full, with Claude Code. Needs what scenario 24 needs (Claude Code, `ai-stackops`, the
clone, the project `pump-controller` from scenario 24 step 1), and the host's first admin account
(the one made at install) as the second admin. Measured: the API steps passed; the Claude Code spend
    steps (2–3) were not run.


*A development project has its own money: a pool, a share per person, and a rule for what happens
when it runs out. Loosening any of that takes a second admin.*

**You are** Dana and the first admin in the Studio (two browser profiles), Sam in the terminal.

1. As Dana, **Projects** → `pump-controller` → **Overview** → *Budget*: *Project, USD per day*
   **0.03**, *When the budget runs out*: **Move background calls to a local model**. Save.
   Tightening applies at once. Point at *Each member, USD per day*: the same cap per person inside
   the pool (left empty here, so the pool is what runs out). (The stand-in is the project's local id,
   `claude-local-qwen`; the `mlx-serve` entry must carry no pricing, or it spends the same budget.)
2. As Sam, in the clone: `claude`, `/model claude-gemini-flash`, and ask for a few small changes
   until the spend passes three cents. From then on Claude Code's background calls (conversation
   titles, summaries, compaction) are moved to the local model instead of failing, and his next
   main call is refused: *Limit reached: $0.03 per day for project pump-controller (used
   $0.03). It frees up as the rolling 24 hours pass; an admin can raise it in the project's budget.
   Local models do not count against it: switch to claude-local-qwen.* `/model claude-local-qwen`
   and carry on. Nothing about the project stopped.
3. As Dana, Admin → Audit: `gateway.downgraded` (from the cloud id to `claude-local-qwen`, request
   class *auxiliary* or *compaction*, the budget as the reason; one row per person every five
   minutes, repeats counted) and `gateway.refused` for the main call. Admin → Setup → *Since your
   last visit*: *Project pump-controller has spent 8x % of its daily budget*, then *… has spent its
   daily budget ($0.03 of $0.03)* (the project's name as created in scenario 24).
4. Make it permanent for background work: Projects → `pump-controller` → **Models** →
   `claude-gemini-flash` → **By kind** → *auxiliary*: `mlx-serve`, *compaction*: `mlx-serve` → **Save
   models**. Now background calls run locally whatever the budget; only the work itself goes to the
   cloud model. The project's **Usage** → *By: Kind of request* shows the split after a few turns.
5. Now loosen it. **Overview** → clear *Project, USD per day* (no daily cap). Save. The toast: *This
   change weakens the project, so it waits for a second admin. It is listed under Changes waiting.*
   The project still has its cap. The box *Changes waiting for a second admin* lists it with the
   reason, in words: *the project's daily dollar cap removed*. Dana's own **Approve** is refused:
   *A change that weakens a project needs a second admin: someone other than the person who asked
   must decide it.*
6. As the first admin, **Projects** → `pump-controller`: the same change, asked by Dana. **Approve**:
   *Approved and applied.* Admin → Audit: `project.change.request` by Dana, `project.change.approve`
   by the first admin. Say what else waits for a second admin: a lower level, a cloud route added, a
   30-day cap above $1,000, a restored project, a later end date, wider networks, more docs for the
   agents, looser code rules. (Raising a daily dollar cap does not.)

**Land:** a project spends what it was given, its background work falls back to the local model
instead of stopping, and nobody loosens its rules alone.

*Reset:* restore the daily caps (tightening applies at once), *When the budget runs out* back to
*Refuse paid calls*, the *By kind* routes back to *same as the id*.

---

## 32. A check before code leaves
**Level:** Full, with Claude Code, continuing from scenario 24. **Needs:** a certified pack that
carries a `gateway.before_call` decide hook; not tested. The demo pack carries no hook (by decision;
`drafts/platform/NOTES.md` §5c drafts the one it could ship), and the product's own test pack for
this lives only in its test suite.


*A pack the organisation trusts reads what a coding tool is about to send to a cloud model, and
can stop it.*

**You are** Dana in the Studio, Sam in the terminal.

1. As Dana, Admin → Policy → **Packs**: the pack's `presend-secrets` hook on `gateway.before_call`,
   mode decide, **off: not consulted**. Switch it on. The confirmation says what it reads: *the new
   text of every developer call to a cloud model (prompts and code) and may stop it.* Switch on.
2. As Sam, in the clone, on the cloud id: **"Why does this fail? AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
   is set in the build."** Refused before it leaves, with the pack's reason: a cloud call carrying
   what looks like a cloud access key. Nothing reached the provider.
3. The same question without the key goes through. Admin → Audit: `gateway.refused` names the pack,
   its version and the hook, never the text; the `gateway.call` row of the call that went out
   carries *allowed by* the hook.
4. Say what a stricter organisation does (shown, not run: the Studio's handling-rules table has
   no column for it yet): IDE tab → `classification.yaml` → `handling: internal: preSend: required`.
   Calls at that level then leave only when a pack said yes; with no hook switched on, every cloud
   call at that level is refused, and Admin → Setup fails the *pre-send check* line.
   `PACK_DECIDE=false` on the host stops every pack deciding.

**Land:** what leaves for a cloud model can be read first by a pack the organisation certified,
and stopped, with the refusal on the record and the text nowhere in it.

---

## 33. The bill, checked; the cost, charged back
**Level:** Full, with Claude Code: the project's spend comes from scenarios 24 and 31. The
chargeback export itself works at any level with the Enterprise licence (*Before the day*, step 2).
The bill check **Needs:** an Anthropic or OpenAI organisation admin key (OpenRouter and Azure
publish no usage report the check reads); not tested. The rest (usage by project, the chargeback CSV) passed in the measured run.


*What the platform metered, compared with what the provider billed, and the spend split by
project for the people who pay it.*

**You are** Dana. Best after scenarios 16, 24 and 31 have run, so there is usage to split.

1. Usage tab → *By development project*: `pump-controller` and *(no project)*. Click the project:
   calls, tokens and cost for the Claude Code work alone.
2. **Export 30 days (CSV)**. Open it: one row per month, person, agent, model entry, node and
   **project**, with calls, tokens and cost. Filter `project = pump-controller`: the engineering
   chargeback. Admin → Audit: `usage.export`.
3. *Needs an Anthropic or OpenAI admin key.* The cloud entry carries a `usageReport` block in
   `models.yaml` (IDE tab): `usageReport: { apiKey: ${secret:anthropic-admin-key}, apiKeyId: <the
   call key's id> }`, the organisation's admin key, never the call key, and the call key's id so other
   apps on the account are not counted. Usage tab → *Checked against the provider's bill*: for each
   such entry, yesterday's metered tokens beside the provider's own report for the same key, and a
   verdict: *matches*, *billed more than metered* or *metered more than billed*. **Compare yesterday
   now** runs it at once. Admin → Audit: `usage.reconcile`, per provider and key, never the admin key.
4. Say what *billed more than metered* means: calls reached the provider with this organisation's
   key without passing through AI Stackops. The key has been copied somewhere. Rotate it.

**Land:** the ledger is checked against the provider's own bill daily, and the same ledger splits
the cost by project for chargeback.

---

## 34. Data read as the person asking
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

## 35. A pack from anyone, held apart
**Level:** Essentials. **Needs:** a small unsigned pack in a git repository of its own; not built
(`drafts/platform/NOTES.md` §7 lists what it holds), so not tested.


*Capability can come from any git repository, not only from signed publishers. What the platform
lets an unknown publisher's pack do is the point.*

**You are** Dana.

1. Packs → *Install* → the unsigned pack's git URL → *Inspect*. The card: **community**, unsigned,
   publisher unknown. Say: anyone can publish a pack; nobody vouched for this one.
2. Install it. Admin → Policy → **Packs**: its hook is listed with **runs isolated**: its code runs
   in a separate process with no network, no files and no modules, and is stopped after 30 seconds.
   Say the limit out loud: only hooks run this way; a function a pack offers agents as a tool loads
   in the server like any other, which is one more reason to install community packs with care.
3. What it may not do, and the install dialog would refuse if it tried: seed accounts or roles,
   read the audit log or usage, or decide anything in a person's place (decisions are for certified
   packs only).
4. Packs → *Trusted publishers* → *Minimum tier to install*: **pack — signed by a trusted
   publisher** (it saves when chosen). Inspect it again: *Install* is off, and the reason says the
   host no longer accepts community packs. Set it back to **community**.
5. Uninstall it. Admin → Audit: `packs.install` (its metadata: tier *community*, verification
   *unsigned*), `packs.trust` twice, `packs.uninstall`.

**Land:** packs install from any git repository; the hooks of one whose publisher nobody trusts run
held apart and reach no people, no records and no decisions, and an admin can refuse unsigned packs
estate-wide in one setting.

---

## 36. Microsoft 365, searched as you
**Level:** Standard. **Needs:** a Microsoft 365 tenant, an Entra app registration with admin
consent (the `aso-o365` pack's SETUP.md), and the `aso-o365` pack; not tested. Written from the
pack.


*Mail, calendar, files and Teams searched by a local model, as the signed-in person, read-only.*

**You are** Dana to install, then Priya.

1. As Dana, Packs → *Install* → `https://github.com/alexborhani/aso-o365`: signed by AI Stack Ops,
   certified. The dialog asks for the tenant's client and tenant ids and the local folders. Its
   declared egress: `login.microsoftonline.com`, `graph.microsoft.com`, nothing else.
2. As Priya, Packs → the pack → *Your setup* → **Connect your Microsoft account**: a device code,
   signed in once with her Microsoft account. Admin → Audit: `identity.connect`.
3. `o365-assistant`: **"What did Marcus send me about the Riverside open day?"** One search across
   her mail, files and calendar, answered with each item's title and link, on the local model. It
   is her mailbox, read with her delegated token; nobody else's mail is reachable.
4. **"Reply to him and say yes."** It says it is read-only and offers a draft for her to send.

**Land:** a Copilot-style search over Microsoft 365 that runs on the organisation's own model, as
the person asking, and cannot send or change anything.

---

## 37. A space of your own
**Level:** Essentials. Step 5 needs the `deepseek-flash` entry from *Before the day*; it needs no working
key, because the refusal comes before anything is dialled. Measured on Qwen 3.5 9B (2026-10-01): end to end three times in a row, every step passing; its bench check (`space-answer`) 10 of 10.


*A person keeps their own documents in one place and chats with them. The platform decides which models
may read them, how much the space may hold, and that nobody else sees any of it.*

**You are** Sam in one window, Dana in the other. Sam uploads three files from the pack's `space-files`
folder (`<workspace>/bundles/aiso-demo-pack/space-files/`): a Word file carrying the Purview label
*Confidential*, his own notes, and a sensor log.

1. As Sam, **Spaces** → *New space* `Riverside rig trips`. Upload `riverside-interlock-trips.docx` and
   `rig-trip-working-notes.md`. The Word file reads **confidential**, *Set by* **label**; the notes read
   internal, *Set by* **default**. The space takes the highest level of its documents: confidential.
2. Under the space, its limit: about 22,600 tokens, set by `mlx-serve`, the local model, whose window is
   32,768 tokens (the rest is kept for instructions, the conversation and the reply; the figure assumes the
   entry's Max Tokens at 4,096). Upload `halden-rig-sensor-log-2026.csv`, about 44,000 tokens: refused.
   Every document goes into the chat whole, the model allowed to read this space cannot take it, and
   *larger sets of documents belong in a knowledge store*. Say: the line between a personal space and a
   governed knowledge store is set by the models the organisation runs.
3. **Chat in this space**. Ask: **"Which sensor caused most of the rig trips, and what does the analysis
   recommend doing about it?"** The local model answers from the Word file: sensor GS-2, 29 of the 41 trips,
   a cracked bracket, a coded safety sensor in its place. With the reply, a note lists what a space chat
   does not have: nothing in it is handed to another agent or saved where other people can read it.
4. **"What do my working notes say I should check on Tuesday?"** The torque on the bracket bolts. Account
   → the usage line: *(… from a prompt cache)*. Every turn sends the documents again; the engine kept
   them from the first turn and read them back instead of working through them again. Say: that is what
   keeps a space affordable, on the Mac and on a cloud provider.
5. A new chat in the space, **With** `deepseek-flash`, the same question. Refused before anything is
   sent: *The model "deepseek-flash" may only see internal data, and this space holds confidential
   documents.* As Dana, Admin → Audit, `space.chat.refused`: the space id, the model and the levels,
   never a name or a word of the space.
6. As Dana, **Spaces** lists only her own. Admin → Data → **Spaces**: how many spaces, people,
   documents and megabytes, nothing more. Admin → Audit, `space.upload`: ids, levels and sizes, and the
   refused upload with its reason. Say: the one route by which an admin reaches a space is the
   subject-access export of the whole account (scenario 19), and that export is on the record.

**Land:** people get a private place to work with their own documents, and the organisation still
decides which models read them, how much goes in, and that none of it reaches anyone else.

---

## 38. Instructions of your own
**Level:** Essentials. Measured on Qwen 3.5 9B (2026-10-01): end to end three times in a row, every step passing; its bench check (`instructions`) 10 of 10.


*Each person tells the assistant once how they want their answers. The same question then comes back
shaped for each of them, and nobody else reads what they wrote.*

**You are** Lena in one window, Priya in the other; Dana for the last step.

1. As Lena, Account → **Personal instructions**: **"Answer in German. I work in Finance at Crestview."**
   Save. As Priya: **"I am an operations coordinator at the Halden plant and I read answers on my phone.
   Keep answers short and use bullet points."** Save.
2. As Lena, Chat: **"How do I reset my VPN certificate?"** The steps from the VPN runbook, in German.
3. As Priya, the same question: the same steps as short bullet points, in English. Chat's own
   instructions say plain sentences and no lists; Priya's changed the form of the answer. Say: the
   person's instructions come after the agent's and the admin's, marked as the person's preferences, and
   access is enforced in code, so no instruction widens what anyone may see or use.
4. As Dana, Admin → Data → **Personal instructions**: on or off, the length limit, and how many people
   have written some. No text. Admin → Audit, `instructions.set`: who, and how many characters.

**Land:** personalisation that costs nothing in control: one sentence per person, applied everywhere
they chat, and read by nobody else.

---

## 39. Save to space
**Level:** Essentials: the `board-brief` agent, two tools (the close package and the canvas).
Measured on Qwen 3.5 9B (2026-10-01): end to end three times in a row, every step passing; its bench check (`save-to-space`) 10 of 10.


*A draft an assistant made becomes a document the person keeps: versioned, linked to the conversation and
the sources it came from, and never less sensitive than what it was made from.*

**You are** Lena; Dana in the second window for the last step.

1. As Lena, **Spaces** → *New space* `Board prep`.
2. Agents → `board-brief`: **"Draft a one-page board brief on Q2 2026 revenue against the forecast."** It
   searches the close package, and the canvas opens with the brief: 41.2 million against a forecast of
   40.5 million, with the document named.
3. Above the canvas, **Save to space** (the folder with a plus) → `Board prep`, level *The conversation's
   level* → Save. The brief reads **confidential**, *Set by* **conversation**: the conversation read the
   confidential close package. The space is now confidential too. Save it once more choosing *internal*:
   refused, *This came from a conversation at confidential, so it is kept at confidential or higher.*
4. Spaces → `Board prep` → the brief → **Text**: the conversation it came from, with a link back, and the
   answer's sources: the close package.
5. Back in the chat: **"Rewrite the brief on the canvas as three bullet points."** Save to space → *New
   version of* the brief. The space lists it once, at version 2, still confidential; the first version
   is kept and no longer counts toward the limits. Its **Text** now names the revision's answer, in the
   same conversation.
6. As Dana: nothing of it under her Spaces. Admin → Audit, `space.save`: the file id, the level, the
   source level, the conversation and answer ids; never the title or a word of the brief.

**Land:** what an assistant drafts can be kept without leaking down a level on the way out of the chat,
and every document knows where it came from.

---

## The 60-minute tour

| Minute | Scenario | Why here |
| --- | --- | --- |
| 0 | 1. Day one | the estate as it is on the first morning |
| 6 | 2. New starter | value in the first minute, and the first hard line |
| 13 | 3. Who can see what | the model of control, on real questions |
| 20 | 4. Classification switched on | the before and after |
| 28 | 22. Numbers you can check (part one) | an answer is a record, with its figures checked |
| 35 | 21. One chat for everyone | access asked of the owner, granted for one thing |
| 42 | 15. Cloud by policy | the cloud question, answered |
| 49 | 18. On the record | the evidence |
| 55 | 37. A space of your own | personal AI use, inside the policy |

On Standard or Full, swap scenario 21 for 9 (the playbook with its sign-off). Keep 5, 10, 12 and 23
ready as follow-ups for the technical people in the room, 24 and 31–33 for engineering leaders, 25–27
for whoever owns data classification, 26, 29 and 30 for the data team, 28 for whoever signs off a
model change, 14 for a commercial audience, 20 for whoever runs more than one site, 38 and 39 after 37
for anyone asking what people do with it day to day, and 19 for anyone with a privacy remit.

## Reset between runs

- Scenario 1: the classifier model stays set; later scenarios (5, 26) use it. While it is set, a
  document indexed or re-indexed waits for it (pending) before anyone below the top level sees it.
- Scenario 4: set enforcement back to *Off* (Admin → Policy → Classification).
- Scenario 5: the classified notes stay classified; to repeat, uninstall and reinstall the pack, or
  reindex `site-notes` after deleting its rows under Sources (classify each back to internal, then
  approve the lowerings).
- Scenario 9: delete the filed notice from `scratchpad` (Sources) or leave it as a talking point.
- Scenario 12: as Sam, delete *Weekly VPN digest* if a run stopped before step 5, and enable Sam if
  step 3 left him disabled.
- Scenario 13: Priya → Account → *Forget*.
- Scenario 15: leave the entry; delete `board-analyst` if you prefer a clean agent list. After
  step 8, restart the host without `EGRESS_ALLOW_FRONTIER=false`.
- Scenario 16: member Requests / min back to empty; `helpdesk`'s model back to `default`;
  `deepseek-flash` USD / day back to 1 (or, without a key, the pricing removed from `mlx-serve`).
  Leave the entry: the next run needs it.
- Scenario 17: restore the runbook and reindex.
- Scenario 19: *Delete disabled accounts* back to *Never* (People → Users) if the scenario did not end
  there; the legal hold cleared; reinstall the pack to bring Jordan back (Packs → uninstall → install).
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
- Scenario 37: as Sam, Spaces → `Riverside rig trips` → *Delete* (its documents and conversations go with
  it). Spaces are personal: only the person who made one can delete it, and uninstalling the pack
  deletes the accounts and their spaces with them.
- Scenario 38: Lena and Priya → Account → *Personal instructions* → *Delete* (or save an empty text).
- Scenario 39: Lena → Spaces → `Board prep` → *Delete*, unless scenario 19 comes next (it deletes it
  under the hold). Delete it while no hold is active, or it is only hidden until the hold is cleared.

A full reset is Packs → uninstall → install: accounts (with their spaces, instructions and schedules), stores and policy
return to the starting state, with new passwords.
