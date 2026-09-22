#!/usr/bin/env python3
"""Split DEMOS.md into one OKF concept per scenario under data/demo-scripts/ (what the presenter agent reads). Run after editing DEMOS.md."""
import re, json, os, glob
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
md = open(os.path.join(root, 'DEMOS.md')).read()
out = os.path.join(root, 'data', 'demo-scripts')
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, '*.md')): os.remove(f)
for part in re.split(r'^## ', md, flags=re.M)[1:]:
    title, _, body = part.partition('\n'); title = title.strip()
    m = re.match(r'(\d+)\. (.+)', title)
    if m:
        n = int(m.group(1)); slug = re.sub(r'[^a-z0-9]+', '-', m.group(2).lower()).strip('-'); fname = f'{n:02d}-{slug}.md'; ctype = 'scenario'; tags = [f'scenario-{n}']
    else:
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-'); fname = f'{slug}.md'; ctype = 'guide'; tags = []
    body = body.strip().replace('\n---\n', '\n')
    lv = re.search(r'^\*\*Level:\*\*\s*(\w+)', body, re.M)
    level = f'level: {lv.group(1).lower()}\n' if lv else ''
    front = f'---\ntype: {ctype}\ntitle: "{title.replace(chr(34), chr(39))}"\ntags: {json.dumps(tags)}\n{level}---\n'
    open(os.path.join(out, fname), 'w').write(front + body + '\n')
print('demo-scripts written:', len(os.listdir(out)))
