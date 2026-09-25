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
    return st == 200 and (bool(denied) and denied[0]['outcome'] == 'denied') and hasnt(out, r'\b\d+ days\b'), (f'handoff denied={bool(denied)} ' + out[:70])
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
    ('presenter-start', 'standard', 4, 'the presenter starts a scenario through its tool', c_presenter),
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
