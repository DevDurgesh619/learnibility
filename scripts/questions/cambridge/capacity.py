#!/usr/bin/env python3
"""Estimate, per chapter and concept group, how many distinct stems the content can produce
versus how many the cost sheet needs (bank + forms + mock share). Development aid.

  python3 scripts/questions/cambridge/capacity.py cambridge-g10-physics
"""
import importlib
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import core  # noqa: E402


def main(sid):
    plan = json.load(open(os.path.join(os.path.dirname(__file__), 'plan.json')))[sid]
    mod = importlib.import_module('content.' + sid.replace('cambridge-', '').replace('-', '_'))
    core.augment(mod)
    chapters, subs = core.load_curriculum(sid)
    mock_share = plan['nmock'] * plan['qpm'] / max(1, len(chapters))
    bad = 0
    for ch in chapters:
        topics = mod.CHAPTERS[ch['order']]
        need = {}
        for s, C, D, _, _ in core.allocate_chapter(subs[ch['id']], plan['perch']):
            need[C] = need.get(C, 0) + 1
        for s, C, D in core.form_blueprint(subs[ch['id']], plan['qpt']):
            need[C] = need.get(C, 0) + 2
        for C, f in (('C1', .15), ('C2', .3), ('C3', .3), ('C4', .25)):
            need[C] = need.get(C, 0) + round(mock_share * f)
        cap = {}
        seen = []
        exact = set()
        for t in [t for tp in topics for t in tp.templates]:
            for i in range(150 if t.name not in ('fixed',) else 1):
                q = t.fn(random.Random(i), max(t.D))
                if not q:
                    continue
                n = core.norm(q['stem'])
                if n in exact:
                    continue
                sh = core.shingles(n)
                if core.near_dup(sh, len(n), seen):
                    continue
                exact.add(n); seen.append((sh, len(n)))
                cap[t.C] = cap.get(t.C, 0) + 1
        flag = [f'{C} {cap.get(C, 0)}/{need.get(C, 0)}' for C in ('C1', 'C2', 'C3', 'C4') if cap.get(C, 0) < 1.3 * need.get(C, 0)]
        if flag:
            bad += 1
        print(f"{ch['id']} {ch['name'][:40]:40s} " + ('OK' if not flag else 'SHORT ' + ', '.join(flag)))
    print('chapters short:', bad)


if __name__ == '__main__':
    main(sys.argv[1])
