#!/usr/bin/env python3
"""Print a compact chapter/subtopic outline of curriculum subjects (authoring aid).

  python3 scripts/onboarding/outline.py cbse-g9-maths cbse-g8-science ...   [--chapters N]
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
limit = 99
if '--chapters' in sys.argv:
    limit = int(sys.argv[sys.argv.index('--chapters') + 1])
for sid in args:
    f = os.path.join(ROOT, 'data', 'curriculum', f'{sid}.json')
    if not os.path.exists(f):
        print(f'## {sid}: no curriculum file')
        continue
    d = json.load(open(f))
    sts = {s['id']: s for s in d.get('subtopics', [])}
    print(f"## {sid} ({d['subject'].get('name')})")
    for ch in d['items'][:limit]:
        n = int(ch['id'].rsplit('-ch', 1)[1])
        subs = '; '.join(f"{int(s.rsplit('-st', 1)[1])} {sts[s]['name']}" for s in ch['subtopicIds'] if s in sts)
        print(f"{n}. {ch['name'][:70]} | {subs}")
