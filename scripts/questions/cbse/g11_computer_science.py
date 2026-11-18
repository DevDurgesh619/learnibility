#!/usr/bin/env python3
"""Generate the CBSE class 11 Computer Science (083) question bank (cbse-g11-computer-science, 1,101 questions).

Families: g11_computer_science_a.py (theory chapters 1-4 and 11: fact tables plus computed number-system, encoding,
Boolean-logic and algorithm-trace families), g11_computer_science_b.py (Python chapters 5-10); computed families in
g11_computer_science_kit.py, plus validated class 12 Python families from g12_computer_science_a.py. Fact tables
are turned into families by g12_hum_engine.py through g12_computer_science_kit.fact_families.
Every code output is computed by running the code, never typed by hand.

Paper (no CBSE SQP for class 11; class 12 template assumed, 70 marks, 37 questions): A 21 x 1 (19 MCQ + 2 A-R),
B 7 x 2, C 3 x 3, D 4 x 4, E 2 x 5.

Run: python3 scripts/questions/cbse/g11_computer_science.py   (QB_LIMIT=n builds the first n chapters only)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
import g12_computer_science_kit as K12  # noqa: E402

SID = 'cbse-g11-computer-science'
MOCK_PATTERN = [(19, 1, 'mcq'), (2, 1, 'ar'), (7, 2, 'k2'), (3, 3, 'k3'), (4, 4, 'k4'), (2, 5, 'k5')]
CODE_SUBTOPICS = [f'{SID}-ch{c:02d}-st{s}' for c, n in ((5, 5), (6, 4), (7, 4), (8, 4), (9, 4), (10, 3)) for s in range(1, n + 1)]
ACC = os.path.join(HERE, 'g11_computer_science_accuracy.json')


def families():
    import g11_computer_science_a as A
    import g11_computer_science_b as B
    ca, ea = A.fams_theory()
    cb, eb = B.fams_python()
    # chapter order 1-4, 5-10, 11
    chapters = ca[:4] + cb + ca[4:]
    extra = dict(ea)
    extra.update(eb)
    fams = K12.fact_families(chapters, extra, drop_case=CODE_SUBTOPICS, code=CODE_SUBTOPICS)
    import g11_computer_science_kit as K
    return K12.assign_kinds(K.no_open_pick(fams))


def main():
    fams = families()
    b = Builder(SID, 'scripts/questions/cbse/g11_computer_science.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.5)
    lim = int(os.environ.get('QB_LIMIT', '0'))
    if lim:
        b.cur['chapters'] = b.cur['chapters'][:lim]
        b.t = dict(b.t, chapters=lim)
    else:
        need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
        if set(fams) != need:
            raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = b.build()
    acc = json.load(open(ACC)) if os.path.exists(ACC) else None
    b.write(files, accuracy=acc)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
