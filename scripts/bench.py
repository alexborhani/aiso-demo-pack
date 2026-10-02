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
    return ok, f"label={prov.get('label')} grade={grade} figures={figs.get('matched')}+{figs.get('derived')}/{figs.get('total')} unsupported={[u.get('text') for u in (figs.get('unsupported') or [])]}"
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
    for _ in range(150):
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

# ── Spaces (scenarios 37-39): a person's own space, personal instructions, Save to space ──────────
import os, uuid
SPACE_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'space-files')
def stream_full(path, body, who, timeout=900):
    """A Studio chat stream (an agent's or a model's, in a space or not): the text, the tool calls, the answer record."""
    req = urllib.request.Request(B + path, method='POST', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'Cookie': people[who], 'Origin': B})
    res = {'out': '', 'tools': [], 'prov': None, 'error': None, 'plan': None}
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            for line in r:
                line = line.decode(errors='replace').strip()
                if not line.startswith('data: '): continue
                try: e = json.loads(line[6:])
                except Exception: continue
                t = e.get('type')
                if t == 'content': res['out'] += e.get('content') or ''
                elif t == 'tool_start': res['tools'].append((e.get('tool'), e.get('input') or e.get('args')))
                elif t == 'provenance': res['prov'] = e
                elif t == 'plan': res['plan'] = e
                elif t == 'error' or ('error' in e and not t): res['error'] = e.get('error') or e.get('message')
    except urllib.error.HTTPError as e:
        res['error'] = f'HTTP {e.code} {e.read().decode(errors="replace")[:120]}'
    return res
def upload_space_file(who, space_id, name):
    bnd = uuid.uuid4().hex
    with open(os.path.join(SPACE_FILES, name), 'rb') as f: data = f.read()
    body = f'--{bnd}\r\nContent-Disposition: form-data; name="file"; filename="{name}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode() + data + f'\r\n--{bnd}--\r\n'.encode()
    req = urllib.request.Request(B + f'/api/spaces/{space_id}/files', method='POST', data=body, headers={'Content-Type': f'multipart/form-data; boundary={bnd}', 'Cookie': people[who], 'Origin': B})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return r.status
    except urllib.error.HTTPError as e: return e.code
_SPACES = {}
def bench_space(who, name, files):
    """One space per person for the whole bench, made on first use and deleted at the end."""
    if who not in _SPACES:
        st, sp = call('POST', '/api/spaces', {'name': name}, people[who])
        if st != 201: raise RuntimeError(f'space not created: HTTP {st} {sp}')
        for f in files: upload_space_file(who, sp['id'], f)
        _SPACES[who] = sp['id']
    return _SPACES[who]
def c_space_answer(i):
    sid = bench_space('sam', 'Riverside rig trips (bench)', ['riverside-interlock-trips.docx', 'rig-trip-working-notes.md'])
    r = stream_full('/api/agents/chat/stream', {'input': {'query': 'Which sensor caused most of the rig trips, and what does the analysis recommend doing about it?'}, 'sessionId': f'b-sp-{i}-{STAMP}', 'spaceId': sid}, 'sam')
    figs = (((r['prov'] or {}).get('checks') or {}).get('figures') or {})
    return not r['error'] and has(r['out'], r'GS-2') and has(r['out'], r'\b29\b|twenty-nine') and not figs.get('unsupported'), (r['error'] or '') + r['out'][:80]
def c_instructions(i):
    st, before = call('GET', '/api/auth/me/instructions', cookie=people['lena'])
    call('PUT', '/api/auth/me/instructions', {'text': 'Answer in German. I work in Finance at Crestview.'}, people['lena'])
    try:
        r = stream_full('/api/agents/' + chat_name() + '/stream', {'input': {'query': 'How do I reset my VPN certificate?'}, 'sessionId': f'b-pi-{i}-{STAMP}'}, 'lena')
    finally:
        call('PUT', '/api/auth/me/instructions', {'text': (before or {}).get('text', '') if isinstance(before, dict) else ''}, people['lena'])
    german = len(re.findall(r'\b(Sie|und|die|der|das|Zertifikat|Konsole|neues?)\b', r['out']))
    return not r['error'] and german >= 4 and has(r['out'], r'VPN'), f'german words={german} ' + (r['error'] or '') + r['out'][:70]
def c_save_to_space(i):
    sid = bench_space('lena', 'Board prep (bench)', [])
    sess = f'b-sv-{i}-{STAMP}'
    r = stream_full('/api/agents/board-brief/stream', {'input': {'query': 'Draft a one-page board brief on Q2 2026 revenue against the forecast.'}, 'sessionId': sess}, 'lena')
    cw = [x for t, x in r['tools'] if t == 'canvas_write' and isinstance(x, dict)]
    if not cw: return False, 'no canvas: ' + (r['error'] or '') + r['out'][:60]
    content = cw[-1].get('content', '')
    st, saved = call('POST', f'/api/spaces/{sid}/canvas', {'content': content, 'format': cw[-1].get('format') or 'markdown', 'name': f'brief-{i}.md', 'sessionId': sess, 'runId': (r['prov'] or {}).get('runId')}, people['lena'])
    doc = (saved or {}).get('document', {}) if isinstance(saved, dict) else {}
    return has(content, r'41\.2') and st == 201 and doc.get('level') == 'confidential' and doc.get('classifiedBy') == 'source', f"save={st} level={doc.get('level')}/{doc.get('classifiedBy')} " + content[:50].replace('\n', ' ')

def c_schedule_run(i):
    body = {'name': f'Weekly VPN digest (bench {i})', 'agentName': 'helpdesk', 'cron': '0 9 * * 1', 'timezone': 'Europe/London',
            'prompt': "Write this week's helpdesk digest: how to reset a VPN certificate, in three bullet points from the IT runbooks."}
    st, s = call('POST', '/api/schedules', body, people['sam'])
    if st != 201: return False, f'create HTTP {st} {s}'
    try:
        st, r = call('POST', f"/api/schedules/{s['id']}/run-now", {}, people['sam'])
        run = (r or {}).get('run', {}) if isinstance(r, dict) else {}
        for _ in range(200):
            st, rs = call('GET', f"/api/schedules/{s['id']}/runs", cookie=people['sam'])
            run = next((x for x in (rs.get('runs', []) if isinstance(rs, dict) else []) if x['id'] == run.get('id')), run)
            if run.get('status') not in ('queued', 'running'): break
            time.sleep(3)
        out = ''
        if run.get('taskId'):
            st, task = call('GET', f"/api/tasks/{run['taskId']}", cookie=people['sam'])
            res = task.get('result') if isinstance(task, dict) else None
            out = str(res.get('output', '') if isinstance(res, dict) else res or '')
        rows = audit_since('schedules.run', 'sam', run.get('startedAt', '9'))
        return run.get('status') == 'completed' and has(out, r'vpn', r'certificat') and any(x.get('targetId') == s['id'] and x['outcome'] == 'success' for x in rows), f"run={run.get('status')} {run.get('reason') or ''} " + out[:70].replace('\n', ' ')
    finally:
        call('DELETE', f"/api/schedules/{s['id']}", cookie=people['sam'])

# ── Harness depth (1.16.0): a shared space (40), plan mode (41), sub-agents (42), a tool that asks first (43) ──
def c_space_shared(i):
    sid = bench_space('sam', 'Riverside rig trips (bench)', ['riverside-interlock-trips.docx', 'rig-trip-working-notes.md'])
    call('POST', f'/api/spaces/{sid}/members', {'user': 'dana', 'role': 'member'}, people['sam'])
    call('POST', f'/api/spaces/{sid}/members', {'user': 'priya', 'role': 'member'}, people['sam'])
    enforce('enforce')
    st, _ = call('GET', f'/api/spaces/{sid}', cookie=people['priya'])
    r = stream_full('/api/agents/chat/stream', {'input': {'query': 'Which sensor caused most of the rig trips, and what does the analysis recommend doing about it?'}, 'sessionId': f'b-ss-{i}-{STAMP}', 'spaceId': sid}, 'dana')
    return st == 403 and not r['error'] and has(r['out'], r'GS-2') and has(r['out'], r'\b29\b|twenty-nine'), f'priya HTTP {st} ' + (r['error'] or '') + r['out'][:70]
def c_plan_first(i):
    # The file is read through the agent's own sandbox_file_read result, so the bench also works against a remote host.
    # Each run names its own file: a file left by an earlier run would be patched rather than written, as it should be.
    sess = f'b-pl-{i}-{STAMP}'
    plan_file = f'/tmp/meridian/halden-outage-checklist-{i}-{STAMP}.md'
    r = stream_full('/api/agents/runbook-editor/stream', {'input': {'query': f'Turn the plant network outage runbook into a checklist for the Halden night shift, saved as {plan_file}.'}, 'sessionId': sess}, 'sam')
    p = r['plan'] or {}
    planned = p.get('kept') is True and 'sandbox_file_write' in (p.get('withheld') or []) and not any(t in ('sandbox_file_write', 'sandbox_file_patch') for t, _ in r['tools'])
    if not planned: return False, f"plan={ {k: p.get(k) for k in ('kept', 'withheld')} } tools={[t for t, _ in r['tools']]} " + (r['error'] or '') + r['out'][:60]
    r2 = stream_full('/api/agents/runbook-editor/stream', {'input': {'query': 'Go ahead with the plan.'}, 'sessionId': sess, 'plan': 'approve'}, 'sam')
    wrote = [x for t, x in r2['tools'] if t == 'sandbox_file_write' and isinstance(x, dict)]
    body = (wrote[-1].get('content') or '') if wrote else ''
    return not r2['error'] and bool(wrote) and has(body, r'supervisor') and has(body, r'UPS'), f"tools={[t for t, _ in r2['tools']]} " + (r2['error'] or '') + body[:60].replace('\n', ' ')
def c_subagents(i):
    r = stream_full('/api/agents/incident-coordinator/stream', {'input': {'query': 'Brief me on INC-2026-021: what happened, what is still open, and what the runbooks say about the plant network side.'}, 'sessionId': f'b-sa-{i}-{STAMP}'}, 'dana')
    agents = {(x or {}).get('agent') for t, x in r['tools'] if t == 'task' and isinstance(x, dict)}
    return not r['error'] and {'security-lead', 'helpdesk'} <= agents and has(r['out'], r'INC-2026-021|USB|4471'), f'children={sorted(a for a in agents if a)} ' + (r['error'] or '') + r['out'][:60]
def c_elicitation(i):
    import threading
    seen = {}; done = threading.Event()
    def answer():
        while not done.is_set():
            st, q = call('GET', '/api/elicitations', cookie=people['sam'])
            for x in (q.get('elicitations', []) if isinstance(q, dict) else []):
                st2, _ = call('POST', f"/api/elicitations/{x['id']}", {'action': 'accept', 'content': {'confirm': True, 'window': 'Saturday 06:00'}}, people['sam']); seen['answered'] = st2; return
            done.wait(2)
    th = threading.Thread(target=answer, daemon=True); th.start()
    r = stream_full('/api/agents/change-clerk/stream', {'input': {'query': 'File a change on MW-300 Halden line 2: set the interlock timer back to 400 ms, because the 250 ms setting caused nuisance trips.'}, 'sessionId': f'b-el-{i}-{STAMP}'}, 'sam')
    done.set(); th.join(timeout=10)
    return not r['error'] and seen.get('answered') == 200 and has(r['out'], r'CHG-2026-0\d{3}'), f"card={'answered' if seen.get('answered') == 200 else 'none'} " + (r['error'] or '') + r['out'][:60]
def c_sampling_off(i):
    t0 = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    r = stream_full('/api/agents/change-clerk/stream', {'input': {'query': 'Summarise the change log of MW-300 Halden line 2.'}, 'sessionId': f'b-so-{i}-{STAMP}'}, 'sam')
    st, a = call('GET', '/api/admin/audit?action=mcp.sampling&limit=20', cookie=ADMIN)
    refused = [e for e in (a.get('entries', []) if isinstance(a, dict) else []) if e['ts'] >= t0 and e.get('outcome') == 'denied']
    return not r['error'] and bool(refused) and has(r['out'], r'CHG-2026-0412|CHG-2026-0471'), f'refused rows={len(refused)} ' + (r['error'] or '') + r['out'][:60]

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
    ('schedule-run', 'essentials', 12, 'Sam\'s schedule runs the helpdesk as Sam and writes the VPN digest from the runbook', c_schedule_run),
    ('counsel', 'essentials', 8, 'counsel answers the admin on a restricted matter', c_counsel),
    ('finance', 'essentials', 6, 'the finance analyst answers a finance analyst', c_finance),
    ('answer-grade', 'essentials', 22, 'a finance answer is labelled documents, its figures found in sources, graded high or medium', c_answer_grade),
    ('answer-mark', 'essentials', 22, 'a person marks an answer wrong and clears the mark', c_answer_mark),
    ('revoke', 'essentials', 7, 'the security lead calls revoke_access and it runs once Dana approves', c_revoke),
    ('classify-note', 'essentials', 5, 'the local classifier files the Nordvik price proposal as confidential Finance', c_classify_note),
    ('owner-grant', 'essentials', 21, 'a contractor\'s request reaches the agent\'s owner, whose grant opens the agent', c_owner_grant),
    ('space-answer', 'essentials', 37, 'Chat in a person\'s own confidential space answers from its document, every figure found in it', c_space_answer),
    ('instructions', 'essentials', 38, 'a person\'s own instructions shape Chat\'s answer (German for Lena)', c_instructions),
    ('space-shared', 'essentials', 40, 'a member of Sam\'s shared space is answered from its document; Priya, below its level, is refused it', c_space_shared),
    ('save-to-space', 'essentials', 39, 'a brief drafted on the canvas from the close package is saved to a space at confidential, set by the conversation', c_save_to_space),
    ('presenter-start', 'standard', 4, 'the presenter starts a scenario through its tool', c_presenter),
    ('playbook-asks', 'standard', 9, 'the writer asks for the playbook\'s missing date and files nothing', c_playbook_asks),
    ('playbook-signoff', 'standard', 9, 'filing the notice waits for an admin\'s approval, then files', c_playbook_signoff),
    ('plan-first', 'standard', 41, 'the runbook editor plans with its write tools withheld, then writes the checklist once the plan is approved', c_plan_first),
    ('subagents', 'standard', 42, 'the incident coordinator hands the question to the security lead and the helpdesk with task', c_subagents),
    ('skill-evals', 'standard', 23, 'the playbook\'s own evals pass on the host\'s model', c_skill_evals),
    ('elicitation', 'full', 43, 'the change desk asks Sam on a card before it files; his answer files the change', c_elicitation),
    ('sampling-off', 'full', 43, 'with sampling off the desk is refused a model and returns the log as it is', c_sampling_off),
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
for who, sid in _SPACES.items(): call('DELETE', f'/api/spaces/{sid}', cookie=people[who])
fails = [r for r in results if r['verdict'] == 'FAIL']
print(f'\n{len(results) - len(fails)}/{len(results)} checks passed at level {A.level} in {round((time.time() - t_all) / 60, 1)} min')
if A.json: json.dump({'level': A.level, 'runs': A.runs, 'gate': A.gate, 'results': results, 'ranAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, open(A.json, 'w'), indent=1)
sys.exit(1 if fails else 0)
