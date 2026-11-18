#!/usr/bin/env python3
"""Generate the CBSE class 11 biology question bank (cbse-g11-biology, 1809 questions).

Fact tables per subtopic live in g11_biology_a.py (chapters 1-5), _b.py (6-10), _c.py (11-15) and _d.py (16-19);
they are turned into families by the shared science kit g11_chemistry_kit.py (as in g12_biology*.py).
This script adds two 3-mark families per subtopic (hand-written 'q3' items and a generated "three differences"
item from the feature table) so that the 3-mark mock section only takes items written for 3 marks.

Mocks: school annual exam on the Class XII theory design: 33 questions, 70 marks:
A 16 × 1 (12 MCQ + 4 Assertion-Reason), B 5 × 2, C 7 × 3, D 2 case-based × 4, E 3 × 5.

Run: python3 scripts/questions/cbse/g11_biology.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import qbank  # noqa: E402
from qbank import Builder, F  # noqa: E402
from g11_chemistry_kit import build_all, cap, LONG  # noqa: E402

SID = 'cbse-g11-biology'
MODS = ('g11_biology_a', 'g11_biology_b', 'g11_biology_c', 'g11_biology_d')
PATTERN = [(12, 1, 'mcq'), (4, 1, 'ar'), (5, 2, 'short'), (7, 3, 'k3'), (2, 4, 'case'), (3, 5, LONG)]
ACC = os.path.join(HERE, 'g11_biology_accuracy.json')

_orig_fits = qbank._fits


def fits(f, kind):
    if kind == 'k3':
        return 'k3' in f.kinds
    if kind == 'short' and (f.marks or 2) > 2:
        return False
    return _orig_fits(f, kind)


def _deck(items):
    state = {'left': []}

    def take(r):
        if not state['left']:
            state['left'] = list(items)
            r.shuffle(state['left'])
        return state['left'].pop()
    return take


def q3_family(items):
    d = _deck(items)

    def gen(r):
        stem, ans, key = d(r)
        return {'stem': stem, 'answer': ans, 'key': key, 'marks': 3, 'minutes': 5}
    return F('C3', 'D3', 'explain', gen, marks=3, minutes=5, kinds=('k3',))


def compare3_family(ft):
    items = [x for x in ft['items'] if len(x[1]) >= 3]
    if len(items) < 2 or not ft.get('compare', True):
        return None
    what = ft.get('what', 'structure')

    def gen(r):
        (l1, f1), (l2, f2) = r.sample(items, 2)
        a, b = r.sample(f1, 3), r.sample(f2, 3)
        lead = r.choice(['Give three differences between', 'Distinguish between', 'Compare'])
        tail = '' if lead == 'Give three differences between' else ' on any three points'
        return {'stem': f'{lead} {l1} and {l2}{tail}.',
                'answer': f'{cap(l1)}: {"; ".join(a)}. {cap(l2)}: {"; ".join(b)}.',
                'key': f'1 mark for each of three correct, paired points of difference, e.g. {l1} – {"; ".join(a)}; '
                       f'{l2} – {"; ".join(b)}.', 'marks': 3, 'minutes': 5}
    return F('C3', 'D3', 'explain', gen, marks=3, minutes=5, kinds=('k3',))


def families():
    fams = {}
    for mod in MODS:
        try:
            m = __import__(mod)
        except ModuleNotFoundError as e:
            if e.name != mod:
                raise
            continue
        built = build_all(m.P, m.SPECS)
        for k, spec in m.SPECS.items():
            sid = f'{m.P}-{k}'
            extra = []
            if spec.get('q3'):
                extra.append(q3_family(spec['q3']))
            for fk in ('features', 'features2'):
                if fk in spec:
                    c3 = compare3_family(spec[fk])
                    if c3:
                        extra.append(c3)
            built[sid] += extra
        fams.update(built)
    return fams


def main():
    qbank._fits = fits
    fams = families()
    b = Builder(SID, 'scripts/questions/cbse/g11_biology.py', fams, PATTERN)
    lim = int(os.environ.get('QB_LIMIT', '0'))
    if lim:
        b.cur['chapters'] = b.cur['chapters'][:lim]
        b.t = dict(b.t, chapters=lim)
    else:
        need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
        if set(fams) != need:
            raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = b.build()
    acc = json.load(open(ACC, encoding='utf-8')) if os.path.exists(ACC) else None
    b.write(files, acc)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files


if __name__ == '__main__':
    main()
