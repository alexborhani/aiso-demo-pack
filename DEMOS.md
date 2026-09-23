# Twenty demonstrations of AI Stackops, on one Mac, as Meridian Works

Scripts for a presenter showing AI Stackops to senior business and technology leaders. Every
scenario runs on a single Mac with the demo pack installed and the local model; nothing in the
product or the pack is scripted to produce a particular answer. What the audience sees is what the
platform does with the data in the pack. Each scenario takes five to eight minutes; a 60-minute tour
that chains eight of them is at the end, with a reset checklist.

Meridian Works is fictional: an industrial pump and controls company with a plant at Halden, a
service centre at Riverside and an office at Crestview, about 400 people. Nothing in the pack is real.

## Levels: pick the demo your model can carry

The pack installs at one of three levels, chosen on the install dialog and changeable later from
the pack card (agents above the level are removed, the people and the policy stay). Every scenario
below says which level it needs; the people, the stores of the essentials and the scripts are the
same at every level, so a story told at Essentials reads the same at Full.

| Level | Reference model | What it adds | Scenarios |
| --- | --- | --- | --- |
| **Essentials** | a 9B-class local model, 16K–32K context (Qwen 3.5 9B on a 24 GB Mac) | the eight Meridian agents with one to three tools each, the nine stores the scripts use | 1–8, 13, 14, 16, 18, 19 |
| **Standard** | a 27B-class local model at 32K (a 48 GB Mac or larger), or a cloud entry | the presenter, the writer and canvas, the agent CEO and its organisation, the two workflows, the evals, the demo scripts | 0, 9–12, 15, 17 |
| **Full** | a 70B-class model or a frontier provider | the sample workshop agents (architect, marketer, web engineer, sandbox, media) and the sample stores | 20, and the builder workshop |

The boundaries come from measurement, not taste: on a 9B a single tool with ten actions was
already unreliable, so nothing at Essentials has more than three one-action tools, and the
presenter and the CEO — long prompts, many actions — wait for Standard.

## Before the day

**Install and prepare (once, about 20 minutes)**

1. Install or update AI Stackops on the Mac and give the engine a 16K context. With the macOS deploy
   kit that is `sudo ./install.sh --orcha <binary> --ctx-size 16384` (32768 is fine on 24 GB or more);
   otherwise pass `--ctx-size 16384` to `mlx-serve`. This is not optional for the full set: the
   engine's own default of 4096 tokens is enough for a chat, not for an agent with tools and
   retrieved documents. Every scenario below was exercised against the real engine; the ones marked
   *needs room* fail with "prompt exceeds maximum context length" or take minutes at 4096 and are
   written for 16K.
2. Sign in as the first admin, then Packs → *Install* → `https://github.com/alexborhani/aiso-demo-pack`,
   and pick the level your model carries (above).
   Copy the six passwords from the dialog into a password manager: Dana (admin), Sam (builder),
   Priya, Marcus, Lena (members with roles), Jordan (contractor, public only). *Reset passwords* on
   the pack card mints new ones at any time.
3. Knowledge tab: index `handbook`, `it-runbooks`, `people-files`, `finance-close`,
   `security-incidents`, `legal-matters`, `all-hands`, `site-notes`, `product-faq`, `scratchpad`.
   Ten stores, a few minutes in total on the local embedding model.
4. Models tab: confirm the default chat entry is the engine's Gemma and the embedding entry is
   `bge-small`. Nothing else is required. Scenario 15 adds a cloud entry live.
5. Open the Studio in two browser profiles (or one normal and one private window) so you can be Dana
   in one and another person in the other without signing out. Scenario 14 needs a third window with
   no session at all.

**The people you will be**

| Sign in as | Tier and roles | Clears | Use them for |
| --- | --- | --- | --- |
| Dana | admin | restricted, every category | policy, approvals, audit, the CEO |
| Sam | builder | internal | building: agents, workflows, the IDE |
| Priya | member, staff | internal | the everyday employee |
| Marcus | member, staff, hr-partners | confidential within HR | people questions |
| Lena | member, staff, finance-analysts | confidential within Finance | finance questions |
| Jordan | member, contractors | public | the outsider inside the building |

**Reset between runs** is at the end of this document. The whole pack can be uninstalled and
reinstalled in under five minutes, which returns every account, store and policy to the starting state.

---

## 0. Meet the presenter
**Level:** Standard.


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
LLM tab (it stays resident; both fit beside Gemma). The presenter's presets name the model as the
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
3. Scroll to *Written policy*. This is the organisation's own document, stored beside the taxonomy,
   hashed and versioned. Press *Extract criteria*: the local model reads the policy and proposes
   levels with criteria, categories, clearances and handling rules. Compare the proposal with the
   editor above it. Nothing applies until an admin copies it in. *Needs room:* the policy is about
   1,500 tokens; at 4K the proposal may come back short.
4. Scroll to *Compliance* → *Check now*. Every finding is a gap between what the policy requires of a
   level and the actual configuration, with the change that fixes it. The first finding is the
   enforcement mode itself.
5. Packs tab. Open the pack card (*Details*): signed by AI Stack Ops, certified tier, publisher key id,
   what it seeded. Below the cards, the trusted publishers panel: the minimum tier the host accepts. Say: capability arrives as
   signed packs, installs in one line, uninstalls completely, and unsigned packs can be refused
   estate-wide.

6. Still on the pack card: *Update* and the *auto* switch. Say: a pack is kept current from the same
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
2. Ask: **"How many days of annual leave do I get?"** Answered from the handbook.
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
4. Admin → Policy → Classification → classifier settings: set the model to the local chat entry, save.
   Back on *Sources*, *Send undecided to the classifier*: four notes go *pending*. Refresh every ten
   seconds. Within a minute each carries a level, categories and the classifier's confidence:
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

## 9. Drafting on the canvas, in house style, filed on the record
**Level:** Standard.


*Knowledge work with an output you can see, and an agent writing back into the estate under audit.*

**You are** Sam (builder).

1. `writer`: **"Draft the customer notice about the 2027 price change, effective 1 November, on the
   canvas in house style."** The canvas pane opens beside the chat with the rendered notice. The
   `house-style` skill shaped it: tone, structure, the sign-off.
2. **"Shorten it to three paragraphs and add the service-desk contact."** The canvas updates in place.
3. **"File it in the scratchpad store as '2027 price change notice'."** The agent calls
   `knowledge_add`. Knowledge → `scratchpad` → *Sources*: the new document, decided by a person,
   with who added it and when. Admin → Audit: `knowledge.add` names the title and the sources, never
   the text.
4. Knowledge → `scratchpad` → *Search* for "price change": the notice is retrievable by every agent
   that has the store.

**Land:** the canvas is where a leader sees the work; the audit is where the organisation keeps it.
An agent that writes into the estate does so with a name attached.

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

## 12. An organisation run by an agent CEO
**Level:** Standard.


*Tickets, a team of agents, and a CEO that triages and delegates on a heartbeat.*

**You are** Dana. Organisations → Meridian Works. *Needs room:* the CEO's prompt carries the whole
organisation (chart, open tickets, ten organisation tools), about 4,000 tokens before it says a word,
so this scenario needs the 16K engine; at 4096 the heartbeat fails with a context-length error, which
the CEO runs list shows as a failed run.

1. Open the board: eight tickets across backlog, to do, in progress, in review, blocked, done, each
   assigned to an agent: the helpdesk, the writer, the security lead.
2. Open a ticket: description, priority, activity. Create a new one: **"Riverside test rig guard
   interlock trips twice a shift"**, priority high, unassigned.
3. Press *Wake CEO* (the CEO's manual heartbeat). Watch Activity: the `meridian-ceo` agent reads
   the org context, the open tickets and the team, decides who should own the new ticket, updates
   statuses, and writes its reasoning as comments. The CEO run appears under CEO runs with its
   token count and cost.
4. Show the heartbeat schedule (every 30 minutes by default, off until an admin enables it) and the
   `org-ceo` skill that shapes how the CEO triages.

**Land:** the organisation object is where agents stop being chat windows and become a team with a
backlog, an owner and a cadence, with every decision written down.

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

1. Models tab → *Frontier providers* → add one: provider Anthropic, name `claude`, model `claude-sonnet-4-5`,
   key `${ANTHROPIC_API_KEY}`, access minimum role admin, budget 5 USD a day, pricing 3/15 per
   million, maximum classification internal. Save. Say: four decisions were just made about a cloud
   model before anyone could use it: who, how much, what data, at what price.
2. Agents → *New agent* `board-analyst`: model `claude`, tool `knowledge:handbook`, prompt "You are a
   concise business analyst." Save.
3. As Jordan, `board-analyst`: **"Summarise our values in one line."** Refused before anything is
   dialled: access to model `claude` needs role admin. Admin → Audit: `model.access.denied`.
4. As Dana, same question. With a key on the host, the answer comes from Claude and the usage row
   carries the cost at the pricing you set. Without one, the attempt reaches Anthropic and is refused
   by them; the point stands: the only person who could reach the cloud was the one the policy allows.
5. Try `counsel` with the cloud entry (edit its model to `claude`): refused for everyone, because the
   agent and the legal store both say `allowFrontier: false`. Then Admin → Setup: the checklist
   shows the cloud entry needs a budget and access (it has both), and the compliance report says
   whether any restricted store could reach it (it cannot, ceiling internal).
6. Mention the operator lock: `EGRESS_ALLOW_FRONTIER=false` in the host's environment refuses every
   cloud call for everyone, and no setting in the Studio can override it.
7. The router, local first and cloud only when the local model cannot: IDE tab → `models.yaml`, add an
   entry `frontline` with `provider: router` and `candidates: [mlx-serve, claude]`, and set `helpdesk`'s
   model to `frontline`. As Dana, `helpdesk`: **"How do I reset my VPN certificate?"** — answered by
   the local model; Admin → Audit, `models.route`: candidate `mlx-serve`, reason *first candidate*.
   Then open `bundles/aiso-demo-pack/long-reads/riverside-commissioning-report.md` in the IDE tab
   (320 test records, about 19,000 tokens — more than the local engine's window), copy all of it into
   the chat and ask: **"How many of these tests failed, and which fault was most common?"** The router
   skips the local model before dialling — the audit row's reason says *fit: mlx-serve (context …)* —
   and the cloud entry answers; the answer key is beside the report. As Jordan, the same paste is
   refused: the local model does not fit and the cloud entry is not his to use.

**Land:** cloud models are welcome where the policy says so, with a person, a data class and a budget
attached, and the answer to "did anything leave the building" is in the audit log.

---

## 16. The runaway agent
**Level:** Essentials.


*Budgets and rate limits as circuit breakers, per person, per agent, per model.*

**You are** Dana; Priya in the second window.

1. Admin → Policy → Limits: set the member tier to 1,500 tokens a day. Save.
2. As Priya, `helpdesk`: **"How do I reset my VPN certificate?"** Answered. Ask again with another
   runbook question. On the second or third call the reply is refused: budget exceeded, with what was
   used and the limit. The Usage tab as Dana shows Priya's rows adding up to it.
3. Admin → Audit: `limits.exceeded`, scope principal, throttled to one row per five minutes so a
   loop cannot flood the log.
4. Show the other two scopes without running them: an agent's own `limits` (runs per minute, spend
   per month) in its definition, and a model entry's `budget` on the Models tab. Say: a runaway loop,
   a leaked API key, or an over-enthusiastic pilot all hit the same three fences.
5. Set the member cap back.

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
2. As Sam, IDE tab → `bundles/aiso-demo-pack/it-runbooks/vpn-reset.md`: change the first step so it no
   longer says to revoke the old certificate. Save. Knowledge → `it-runbooks` → *Re-index* (a few
   seconds; only the changed file is embedded).
3. As Dana, *Run* the helpdesk evals again: the VPN case fails on the missing phrase. Point at the
   check detail.
4. Undo the change, re-index, run once more: green.

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
   altered row breaks the chain, and the chain is verified.
2. Usage tab: calls, tokens and cost by person, by agent, by model entry, by kind, by day. Click a
   person to drill. *Export CSV*: one row per month, person, agent and model, ready for chargeback.
3. Admin → Data → *Evidence bundle*: choose the last 30 days, download. One JSON file, signed with the
   workspace key, containing the setup checklist, the compliance report, the taxonomy version, the
   packs, the limits, the usage totals and the audit rows. Open it and show the signature block.
4. Admin → Estate → *Estate report*: nodes and active people, signed the same way.

**Land:** nothing here was assembled by hand for the meeting. The evidence a control framework asks
for is a download, and it is tamper-evident.

---

## 19. A person leaves
**Level:** Essentials.


*Subject access, erasure and legal hold, with the audit log kept intact.*

**You are** Dana.

1. Admin → People → Users → Jordan → the download icon (*Export their data first* on the delete
   dialog does the same): one JSON with the account, the roles, the
   documents Jordan added, the memories, the usage rows and the audit rows Jordan is the actor of.
   Say: this is the subject-access request, answered in one click.
2. Admin → Data → *Legal hold*: set it, with a reason. The Setup checklist shows it; every prune
   stops. Say: retention is suspended estate-wide for litigation without touching the data.
3. Clear the hold. Back on Users → Jordan → *Erase*: keys revoked, memories and added documents
   removed, usage rows pseudonymised, the account deleted. The audit rows are untouched: they name
   the actor as they did. Admin → Audit: `users.erase` lists the steps.
4. Say: reinstalling the pack brings Jordan back for the next demo.

**Land:** the data-protection lifecycle is built in, per person, with the audit trail as the one
thing that is never edited.

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
WORKSPACE=~/aiso-spoke PORT=3460 P2P_ENABLED=true P2P_PEER_NAME=riverside-laptop \
  P2P_ENDPOINT=http://127.0.0.1:3460 HEADLESS=true ./dist/sea/ai-stackops start
```

Open `http://localhost:3460`, create its admin, and continue from step 2. The spoke uses the same
engine as the hub, which is fine for a demo; in production each node has its own. The hub must not
have been started with `P2P_ENABLED=false` in its environment: that locks federation off.

---

## 21. One door for everyone
**Level:** Essentials.


*A member never picks an agent. The front door answers from what they may use, refuses the rest
by name, and asks the admins on their behalf.*

**You are** Jordan, then Marcus, then Dana (two windows).

1. As Jordan, the Chat tab (it is the only chat a member has; the workshop tabs are gone). Ask
   **"How do I reset my VPN certificate?"** The door hands the question to the helpdesk and answers
   from the runbook, naming it.
2. Still as Jordan: **"How much holiday do I carry over at year end?"** The door says the people
   partner owns that and it is outside Jordan's access, and offers to ask the administrators. Say
   **"Yes, please ask."** The door confirms the request was sent.
3. As Marcus, Chat: the same holiday question. The door reaches the people partner and answers.
   Say: same door, same question, different person, different destinations.
4. As Dana, Approvals: Jordan's request is waiting, with `hr-partners` pre-selected because that is
   the role `people-partner` names, and a *Hygiene* score beside the reason — put there by this
   pack's own hook, not by the product (Packs → the pack's card → *Reacts to*). *Grant*. Admin →
   Audit → *Door routing* lists Jordan's refused route and Marcus's successful one.
5. As Jordan again (sign out and in — the role is read at sign-in): the holiday question now
   reaches the people partner.

**Land:** one chat for members, resolved per person on every request; nothing is granted by the
door, and every route and every request is on the record.

---

## The 60-minute tour

| Minute | Scenario | Why here |
| --- | --- | --- |
| 0 | 1. Day one | the estate as it is on the first morning |
| 6 | 2. New starter | value in the first minute, and the first hard line |
| 13 | 3. Who can see what | the model of control, on real questions |
| 20 | 4. Classification switched on | the before and after |
| 28 | 7. Incident copilot with approval | an agent that acts, safely |
| 35 | 13. An assistant that remembers you | personal, and provably private |
| 41 | 15. Cloud by policy | the cloud question, answered |
| 48 | 18. On the record | the evidence |
| 55 | 20. Two nodes | the estate |

Keep 5, 10 and 12 ready as follow-ups for the technical people in the room; 14 for a commercial
audience; 19 for anyone with a privacy remit.

## Reset between runs

- Scenario 4: set enforcement back to *Off* (Admin → Policy → Classification).
- Scenario 5: the classified notes stay classified; to repeat, uninstall and reinstall the pack, or
  reindex `site-notes` after deleting its rows under Sources (classify each back to internal, then
  approve the lowerings).
- Scenario 9: delete the filed notice from `scratchpad` (Sources) or leave it as a talking point.
- Scenario 12: the CEO's ticket changes stay; add a fresh ticket next time.
- Scenario 13: Priya → Account → *Forget*.
- Scenario 15: leave the entry; delete `board-analyst` if you prefer a clean agent list.
- Scenario 16: member cap back to unlimited.
- Scenario 17: restore the runbook and reindex.
- Scenario 19: reinstall the pack to bring Jordan back (Packs → uninstall → install).
- Scenario 20: revoke the enrollment on the hub and stop the spoke process.

A full reset is Packs → uninstall → install: accounts, stores, policy and the organisation return to
the starting state, with new passwords.
