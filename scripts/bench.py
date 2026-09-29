#!/usr/bin/env python3
"""Does a level of the pack operate on the model a host runs?  Every scripted call of the level's
scenarios, N runs each, through a running AI Stackops — the product's own API, the pack's own
people, whatever model the host's default entry names.  A check passes when at least `--gate`
of its runs pass (default 9 of 10).  Nothing here is scripted to produce a particular answer.

  python3 scripts/bench.py --url http://127.0.0.1:3459 --admin root:secret --level essentials
                           [--install .] [--creds creds.json] [--runs 10] [--gate 9] [--json out.json]

--install <pack dir or git url> installs the pack at the level first (an existing install is
replaced) and saves the one-time passwords to --creds; without it the people's passwords are read
from --creds (the file the previous install wrote).  Runs as the pack's people, so it needs the
Studio's admin credentials only to install and to read the audit log.
"""
import argparse, json, re, sys, time, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument('--url', default='http://127.0.0.1:3333'); ap.add_argument('--admin', required=True, help='username:password of an admin')
ap.add_argument('--level', default='essentials', choices=['essentials', 'standard', 'full'])
ap.add_argument('--install', help='pack source to install at --level first (replaces an existing install)')
ap.add_argument('--creds', default='bench-creds.json'); ap.add_argument('--runs', type=int, default=10); ap.add_argument('--gate', type=int, default=9)
ap.add_argument('--only', help='comma list of check ids'); ap.add_argument('--json', help='write results here')
A = ap.parse_args()
B = A.url.rstrip('/')

def call(method, path, body=None, cookie='', timeout=900):
    req = urllib.request.Request(B + path, method=method, data=json.dumps(body).encode() if body is not None else None, headers={'Content-Type': 'application/json', **({'Cookie': cookie} if cookie else {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode(); return r.status, (json.loads(raw) if raw.startswith(('{', '[')) else raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode(); return e.code, (json.loads(raw) if raw.startswith(('{', '[')) else raw)

def login(user, pw):
    req = urllib.request.Request(B + '/api/auth/login', method='POST', data=json.dumps({'username': user, 'password': pw}).encode(), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r: return r.headers.get('set-cookie').split(';')[0]

u, pw = A.admin.split(':', 1); ADMIN = login(u, pw)
if A.install:
    st, packs = call('GET', '/api/packs', cookie=ADMIN)
    have = next((p for p in (packs if isinstance(packs, list) else packs.get('packs', [])) if p.get('id') == 'aiso-demo-pack'), None)
    st, r = call('POST', '/api/packs/install', {'source': A.install, 'level': A.level, 'reinstall': bool(have)}, ADMIN)
    if st != 201: sys.exit(f'install failed: {st} {r}')
    creds = {x['username']: x['password'] for x in r.get('credentials', {}).get('users', [])}
    json.dump(creds, open(A.creds, 'w')); print(f'installed at level {A.level}; {len(creds)} passwords saved to {A.creds}')
    # index every store the level installed (the scripts assume indexed stores)
    for f in r['pack'].get('knowledge', []):
        name = f.replace('.knowledge.yaml', ''); call('POST', f'/api/knowledge/{name}/index', {}, ADMIN)
    for _ in range(120):
        st, kn = call('GET', '/api/knowledge', cookie=ADMIN); rows = kn if isinstance(kn, list) else kn.get('stores', [])
        mine = [k for k in rows if k['name'] + '.knowledge.yaml' in r['pack'].get('knowledge', [])]
        if mine and all(k.get('status') == 'indexed' for k in mine): break
        time.sleep(3)
    print('stores indexed:', [k['name'] for k in mine if k.get('status') == 'indexed'])
else:
    creds = json.load(open(A.creds))
people = {n: login(n, p) for n, p in creds.items()}

# Session ids carry a per-invocation stamp: a reused id (the server keeps conversation history in
# memory between passes) makes the model answer from history without a tool call.
STAMP = time.strftime('%H%M%S')
def ask(agent, who, q, session, extra=None):
    inp = {'query': q}; inp.update(extra or {})
    st, r = call('POST', f'/api/agents/{agent}/invoke', {'input': inp, 'sessionId': f'{session}-{STAMP}'}, people[who])
    return st, (r.get('output', '') if isinstance(r, dict) else str(r))

def ask_full(agent, who, q, session, extra=None, timeout=900):
    inp = {'query': q}; inp.update(extra or {})
    st, r = call('POST', f'/api/agents/{agent}/invoke', {'input': inp, 'sessionId': f'{session}-{STAMP}'}, people[who], timeout=timeout)
    return st, (r if isinstance(r, dict) else {'output': str(r)})

def audit_since(action, actor, t0):
    st, r = call('GET', f'/api/admin/audit?action={action}&limit=50', cookie=ADMIN)
    return [e for e in (r.get('entries', []) if isinstance(r, dict) else []) if e.get('actorName') == actor and e['ts'] >= t0]

def enforce(mode): call('PUT', '/api/admin/classification/enforcement', {'mode': mode}, ADMIN)

# ── the checks: (id, level, scenario, description, fn(run) -> (ok, detail)) ─────────────────
def has(text, *pats): return all(re.search(p, text, re.I) for p in pats)
def hasnt(text, *pats): return not any(re.search(p, text, re.I) for p in pats)

def c_runbook(i):
    st, out = ask('helpdesk', 'priya', 'How do I reset my VPN certificate?', f'b-vpn-{i}')
    return st == 200 and has(out, r'vpn|certificat'), out[:90]
def c_handoff_refused(i):
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    st, out = ask('helpdesk', 'jordan', 'How much holiday do I carry over at year end?', f'b-ho-j-{i}')
    denied = audit_since('agents.handoff', 'jordan', t0)
    # The handbook's public leave allowance may still be quoted; what must not happen is the handoff.
    return st == 200 and (bool(denied) and denied[0]['outcome'] == 'denied') and hasnt(out, r'people (operations|partner) (says|said|told)'), (f'handoff denied={bool(denied)} ' + out[:70])
def c_handoff_works(i):
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    st, out = ask('helpdesk', 'marcus', 'How much holiday do I carry over at year end?', f'b-ho-m-{i}')
    rows = audit_since('agents.handoff', 'marcus', t0)
    return st == 200 and bool(rows) and rows[0]['outcome'] == 'success' and has(out, r'holiday|leave|carry|days'), (f'handoff={rows[0]["outcome"] if rows else "none"} ' + out[:70])
def c_town_hall(i):
    enforce('enforce'); st, out = ask('announcements', 'jordan', 'When is the town hall?', f'b-th-{i}')
    return st == 200 and has(out, r'town hall') and has(out, r'october|\b16\b|thursday'), out[:90]
def c_severance_refused(i):
    enforce('enforce'); st, out = ask('announcements', 'jordan', 'What are the severance terms in the Riverside restructuring?', f'b-sv-j-{i}')
    return st == 200 and hasnt(out, r'four weeks|26 weeks|per year of service'), out[:90]
def c_severance_hr(i):
    enforce('enforce'); st, out = ask('announcements', 'marcus', 'What are the severance terms in the Riverside restructuring?', f'b-sv-m-{i}')
    return st == 200 and has(out, r'four weeks|26 weeks|severance'), out[:90]
def c_store_refused(i):
    st, r = call('POST', '/api/knowledge/legal-matters/search', {'query': 'litigation'}, people['jordan'])
    return st == 403, f'HTTP {st}'
def c_memory(i):
    ask('assistant', 'priya', f'Remember that my desk is at Halden, second floor, bay {i + 1}.', f'b-mem-{i}')
    st, out = ask('assistant', 'priya', 'Where is my desk?', f'b-mem-{i}')
    return st == 200 and has(out, r'halden'), out[:80]
def c_counsel(i):
    st, out = ask('counsel', 'dana', 'In two sentences, what is the Riverside matter about?', f'b-co-{i}')
    return st == 200 and has(out, r'riverside'), out[:80]
def c_finance(i):
    st, out = ask('finance-analyst', 'lena', 'What is the Q3 close status? One sentence.', f'b-fin-{i}')
    return st == 200 and len(out.strip()) > 20 and hasnt(out, r'cannot|not able|no access'), out[:80]
def chat_name():
    # The Chat agent: rows carry `chat` (older hosts `door` only); it is named `chat`, or `front-door` on older workspaces.
    st, r = call('GET', '/api/agents', cookie=ADMIN)
    rows = r if isinstance(r, list) else []
    return (next((a['name'] for a in rows if a.get('chat')), None) or next((a['name'] for a in rows if a.get('door')), None)
            or ('chat' if any(a.get('name') == 'chat' for a in rows) else 'front-door'))
def c_chat_refused(i):
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    st, out = ask(chat_name(), 'jordan', 'How much holiday do I carry over at year end?', f'b-dr-j-{i}')
    ok = st == 200 and hasnt(out, r'\b\d+ days\b') and has(out, r'people|access|administrator|request')
    return ok, out[:90]
def c_chat_works(i):
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    st, out = ask(chat_name(), 'marcus', 'How much holiday do I carry over at year end?', f'b-dr-m-{i}')
    rows = audit_since('agents.handoff', 'marcus', t0)
    return st == 200 and bool(rows) and rows[0]['outcome'] == 'success' and has(out, r'holiday|leave|carry|days'), (f'handoff={rows[0]["outcome"] if rows else "none"} ' + out[:70])
def c_chat_request(i):
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    ask(chat_name(), 'jordan', 'How much holiday do I carry over at year end?', f'b-dq-{i}')
    st, out = ask(chat_name(), 'jordan', 'Yes, please ask the administrators for me.', f'b-dq-{i}')
    rows = audit_since('access.request', 'jordan', t0)
    st2, q = call('GET', '/api/admin/access-requests?status=all', cookie=ADMIN)
    mine = [x for x in (q.get('requests', []) if isinstance(q, dict) else []) if x.get('principalName') == 'jordan' and x.get('requestedAt', '') >= t0]
    for x in mine: call('POST', f"/api/admin/access-requests/{x['id']}/decline", {'note': 'bench'}, ADMIN)
    return st == 200 and bool(rows) and rows[0]['outcome'] == 'success' and bool(mine), (f'request rows={len(rows)} queued={len(mine)} ' + out[:60])
def c_presenter(i):
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    ask('presenter', 'dana', 'Run scenario 4.', f'b-pr-{i}', {'presenter_name': 'Emma', 'presenter_voice': 'Emma'})
    ask('presenter', 'dana', 'next', f'b-pr-{i}', {'presenter_name': 'Emma', 'presenter_voice': 'Emma'})
    st, r = call('GET', '/api/admin/audit?action=demo.scenario.start&limit=20', cookie=ADMIN)
    started = [e for e in r.get('entries', []) if e['ts'] >= t0]
    return bool(started), f'start rows={len(started)}'

def c_answer_grade(i):
    st, r = ask_full('finance-analyst', 'lena', 'What was Q2 2026 revenue, and how does the full-year forecast compare with the plan?', f'b-gr-{i}')
    prov = (r.get('metadata') or {}).get('provenance') or {}
    grade = (prov.get('grade') or {}).get('level'); figs = ((prov.get('checks') or {}).get('figures') or {})
    ok = st == 200 and prov.get('label') == 'documents' and grade in ('high', 'medium') and not figs.get('unsupported')
    return ok, f"label={prov.get('label')} grade={grade} figures={figs.get('matched')}+{figs.get('derived')}/{figs.get('total')} unsupported={len(figs.get('unsupported') or [])}"
def c_answer_mark(i):
    st, r = ask_full('helpdesk', 'priya', 'How do I reset my VPN certificate?', f'b-mk-{i}')
    run = ((r.get('metadata') or {}).get('provenance') or {}).get('runId')
    if not run: return False, 'no answer record'
    st1, _ = call('POST', f'/api/answers/{run}/outcome', {'verdict': 'wrong', 'reason': 'other', 'note': 'bench'}, people['priya'])
    st2, _ = call('POST', f'/api/answers/{run}/outcome', {'verdict': None}, people['priya'])
    return st1 == 200 and st2 == 200, f'mark {st1}, clear {st2}'
def c_owner_grant(i):
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    ask(chat_name(), 'jordan', 'How much holiday do I carry over at year end?', f'b-og-{i}')
    ask(chat_name(), 'jordan', 'Yes, please ask the people who decide access for me.', f'b-og-{i}')
    st, q = call('GET', '/api/access-requests', cookie=people['marcus'])
    mine = [x for x in (q.get('requests', []) if isinstance(q, dict) else []) if x.get('principalName') == 'jordan' and x.get('status') == 'pending' and x.get('requestedAt', '') >= t0]
    if not mine: return False, 'no request reached the owner'
    cap = mine[0].get('capacity')
    st, g = call('POST', f"/api/access-requests/{mine[0]['id']}/grant", {'note': 'bench'}, people['marcus'])
    t1 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    st2, out = ask(chat_name(), 'jordan', 'How many days of annual leave do I get?', f'b-og2-{i}')
    rows = audit_since('agents.handoff', 'jordan', t1)
    reached = any(r_['outcome'] == 'success' for r_ in rows)
    st3, gr = call('GET', '/api/access-requests/grants?kind=agent&name=people-partner', cookie=people['marcus'])
    for x in (gr.get('grants', []) if isinstance(gr, dict) else []):
        if x.get('userName') == 'jordan' and not x.get('revokedAt'): call('POST', f"/api/access-requests/grants/{x['id']}/revoke", {}, people['marcus'])
    return cap == 'owner' and st == 200 and reached, f'capacity={cap} grant={st} handoff after grant={reached} ' + out[:50]
def c_playbook_asks(i):
    # The playbook's required input is asked for, never guessed; nothing is filed on a draft request.
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    st, out = ask('writer', 'sam', 'Draft a customer notice about the 2027 price list.', f'b-pa-{i}')
    filed = [e for e in audit_since('knowledge.add', 'sam', t0)]
    return st == 200 and has(out, r'effective|date|when') and not filed, f'filed={bool(filed)} ' + out[:70]
def c_playbook_signoff(i):
    import threading
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()); seen = {}; done = threading.Event()
    def approve():
        while not done.is_set():
            st, a = call('GET', '/api/approvals', cookie=people['dana'])
            for x in (a.get('pending', []) if isinstance(a, dict) else []):
                if x.get('tool') == 'knowledge_add' and x.get('requestedByName') == 'sam' and x.get('createdAt', '') >= t0:
                    seen['id'] = x['id']; st2, _ = call('POST', f"/api/approvals/{x['id']}/decide", {'decision': 'approve', 'argsHash': x['argsHash'], 'note': 'bench'}, people['dana']); seen['decided'] = st2; return
            done.wait(3)
    th = threading.Thread(target=approve, daemon=True); th.start()
    st, out = ask('writer', 'sam', 'Draft a customer notice about the 2027 price list, effective 1 November 2026, for all customers.', f'b-ps-{i}')
    if not seen.get('decided'): st, out = ask('writer', 'sam', 'File it.', f'b-ps-{i}')
    done.set(); th.join(timeout=10)
    added = [e for e in audit_since('knowledge.add', 'sam', t0) if e.get('outcome') == 'success']
    return st == 200 and seen.get('decided') == 200 and bool(added), f"approval={'decided' if seen.get('decided') == 200 else 'none'} filed={bool(added)} " + out[:50]
def c_revoke(i):
    # The security lead calls revoke_access at once; the run waits on Dana's approval, then runs it.
    import threading
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()); seen = {}; done = threading.Event()
    def approve():
        while not done.is_set():
            st, a = call('GET', '/api/approvals', cookie=people['dana'])
            for x in (a.get('pending', []) if isinstance(a, dict) else []):
                if x.get('tool') == 'revoke_access' and x.get('createdAt', '') >= t0:
                    st2, _ = call('POST', f"/api/approvals/{x['id']}/decide", {'decision': 'approve', 'argsHash': x['argsHash'], 'note': 'bench'}, people['dana']); seen['decided'] = st2; return
            done.wait(2)
    th = threading.Thread(target=approve, daemon=True); th.start()
    st, out = ask('security-lead', 'dana', 'Revoke the access of the contractor holding badge 4471, reason INC-2026-021.', f'b-rv-{i}')
    done.set(); th.join(timeout=10)
    granted = audit_since('tools.approval.granted', 'dana', t0)
    return st == 200 and seen.get('decided') == 200 and bool(granted), f"approval={'decided' if seen.get('decided') == 200 else 'none'} " + out[-60:]
def c_classify_note(i):
    # The local classifier decides one unlabelled note: the customer visit's price proposal is confidential Finance.
    view = call('GET', '/api/knowledge/site-notes/sources', cookie=ADMIN)[1]
    if not (view.get('classifier') or {}).get('model'):
        # Scenario 1 step 3: an admin names the classifier's model (a pack never sets the host's).
        st, c = call('GET', '/api/admin/classification', cookie=ADMIN)
        t = {k: v for k, v in (c.get('taxonomy', c) if isinstance(c, dict) else {}).items() if k not in ('enforcement', 'pending', 'classifier_status')}
        t['classifier'] = {**(t.get('classifier') or {}), 'model': 'mlx-serve'}
        call('PUT', '/api/admin/classification', t, ADMIN)
    src = next((x['source'] for x in (view.get('sources') or []) if 'nordvik' in x['source'].lower()), None)
    if not src: return False, 'note not found'
    st, r = call('POST', '/api/knowledge/site-notes/sources/queue', {'sources': [src]}, ADMIN)
    if st != 200: return False, f'queue HTTP {st} {r}'
    for _ in range(90):
        time.sleep(4)
        row = next((x for x in call('GET', '/api/knowledge/site-notes/sources', cookie=ADMIN)[1].get('sources') or [] if x['source'] == src), {})
        if row.get('status') != 'pending': break
    return row.get('level') == 'confidential' and 'Finance' in (row.get('categories') or []), f"{row.get('status')} {row.get('level')} {row.get('categories')}"
_SKILL_EVALS = {}
def c_skill_evals(i):
    if 'r' not in _SKILL_EVALS:
        _SKILL_EVALS['r'] = call('POST', '/api/skills/customer-notice/evals/run', {}, people['dana'], timeout=3600)
    st, r = _SKILL_EVALS['r']
    t = (r.get('triggers') or {}) if isinstance(r, dict) else {}
    return st == 200 and bool(t.get('ok')), f"triggers {t.get('passed')}/{t.get('total')} ok={r.get('ok') if isinstance(r, dict) else r}"
def c_data_answer(i):
    st, r = ask_full('music-librarian', 'dana', 'What has customer Heather Leacock purchased, and how much did she spend in total?', f'b-da-{i}')
    prov = (r.get('metadata') or {}).get('provenance') or {}
    grade = (prov.get('grade') or {}).get('level')
    figs = ((prov.get('checks') or {}).get('figures') or {})
    return st == 200 and prov.get('label') == 'governed' and grade in ('high', 'medium') and not figs.get('unsupported'), f"label={prov.get('label')} grade={grade} figures={figs.get('matched')}/{figs.get('total')} " + (r.get('output') or '')[-60:]

CHECKS = [
    ('runbook', 'essentials', 2, 'helpdesk answers Priya from the IT runbooks', c_runbook),
    ('handoff-refused', 'essentials', 2, 'a contractor\'s pay question is not handed to the people partner', c_handoff_refused),
    ('handoff-works', 'essentials', 2, 'an HR partner\'s pay question reaches the people partner', c_handoff_works),
    ('town-hall', 'essentials', 4, 'a contractor gets the public town-hall notice under enforcement', c_town_hall),
    ('severance-refused', 'essentials', 4, 'a contractor does not get the confidential severance terms', c_severance_refused),
    ('severance-hr', 'essentials', 4, 'an HR partner does get them', c_severance_hr),
    ('store-refused', 'essentials', 3, 'the legal store refuses a contractor at the API', c_store_refused),
    ('memory', 'essentials', 13, 'the assistant remembers within a session', c_memory),
    ('chat-refused', 'essentials', 21, 'Chat refuses a contractor\'s holiday question by name and offers to ask', c_chat_refused),
    ('chat-works', 'essentials', 21, 'Chat hands an HR partner\'s holiday question to the people partner', c_chat_works),
    ('chat-request', 'essentials', 21, 'a yes in Chat files an access request the admins see', c_chat_request),
    ('counsel', 'essentials', 8, 'counsel answers the admin on a restricted matter', c_counsel),
    ('finance', 'essentials', 6, 'the finance analyst answers a finance analyst', c_finance),
    ('answer-grade', 'essentials', 22, 'a finance answer is labelled documents, its figures found in sources, graded high or medium', c_answer_grade),
    ('answer-mark', 'essentials', 22, 'a person marks an answer wrong and clears the mark', c_answer_mark),
    ('revoke', 'essentials', 7, 'the security lead calls revoke_access and it runs once Dana approves', c_revoke),
    ('classify-note', 'essentials', 5, 'the local classifier files the Nordvik price proposal as confidential Finance', c_classify_note),
    ('owner-grant', 'essentials', 21, 'a contractor\'s request reaches the agent\'s owner, whose grant opens the agent', c_owner_grant),
    ('presenter-start', 'standard', 4, 'the presenter starts a scenario through its tool', c_presenter),
    ('playbook-asks', 'standard', 9, 'the writer asks for the playbook\'s missing date and files nothing', c_playbook_asks),
    ('playbook-signoff', 'standard', 9, 'filing the notice waits for an admin\'s approval, then files', c_playbook_signoff),
    ('skill-evals', 'standard', 23, 'the playbook\'s own evals pass on the host\'s model', c_skill_evals),
    ('data-answer', 'full', 22, 'a data answer through the demo-data MCP server carries a label and a grade', c_data_answer),
]
RANK = {'essentials': 0, 'standard': 1, 'full': 2}
todo = [c for c in CHECKS if RANK[c[1]] <= RANK[A.level] and (not A.only or c[0] in A.only.split(','))]
results = []; t_all = time.time()
print(f'level {A.level}: {len(todo)} checks × {A.runs} runs, gate {A.gate}/{A.runs}\n')
for cid, lvl, sc, desc, fn in todo:
    passed = 0; details = []; t0 = time.time()
    for i in range(A.runs):
        try: ok, d = fn(i)
        except Exception as e: ok, d = False, f'error: {e}'
        passed += bool(ok); details.append((bool(ok), d))
    dt = (time.time() - t0) / A.runs
    verdict = 'PASS' if passed >= A.gate else 'FAIL'
    print(f'  {verdict}  {cid:18} {passed:2}/{A.runs}  {dt:5.1f}s/run  scenario {sc}: {desc}')
    for ok, d in details:
        if not ok: print(f'            ✗ {d}')
    results.append({'id': cid, 'level': lvl, 'scenario': sc, 'passed': passed, 'runs': A.runs, 'gate': A.gate, 'verdict': verdict, 'avgSeconds': round(dt, 1), 'failures': [d for ok, d in details if not ok]})
enforce('off')
fails = [r for r in results if r['verdict'] == 'FAIL']
print(f'\n{len(results) - len(fails)}/{len(results)} checks passed at level {A.level} in {round((time.time() - t_all) / 60, 1)} min')
if A.json: json.dump({'level': A.level, 'runs': A.runs, 'gate': A.gate, 'results': results, 'ranAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, open(A.json, 'w'), indent=1)
sys.exit(1 if fails else 0)
