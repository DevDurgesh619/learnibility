#!/usr/bin/env python3
"""Generate the CBSE class 12 Informatics Practices (065) question bank (cbse-g12-informatics, 762 questions).

Families: g12_informatics_a.py (ch 1 SQL functions, aggregates, operations on relations), _b.py (ch 2-3 pandas),
_c.py (ch 4 Matplotlib, ch 5 networks and web, ch 6 societal impacts); shared helpers and the SQL engine come from
g12_computer_science_kit.py, and some SQL and network generators from the Computer Science bank. Fact tables are
turned into families by g12_hum_engine.py. SQL outputs are computed on sqlite3 with MySQL-style functions, pandas
outputs by running the code; never typed by hand.

Paper (SQP 2026-27, 70 marks, 37 questions): A 21 × 1 (19 MCQ + 2 Assertion-Reason), B 7 × 2, C 4 × 3, D 2 × 4
(case based), E 3 × 5.

Run: python3 scripts/questions/cbse/g12_informatics.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
import g12_computer_science_kit as K  # noqa: E402

SID = 'cbse-g12-informatics'
MOCK_PATTERN = [(19, 1, 'mcq'), (2, 1, 'ar'), (7, 2, 'k2'), (4, 3, 'k3'), (2, 4, 'k4'), (3, 5, 'k5')]
CODE_SUBTOPICS = [f'{SID}-ch0{c}-st{s}' for c, n in ((1, 5), (2, 5), (3, 5), (4, 3)) for s in range(1, n + 1)]
ACC = os.path.join(HERE, 'g12_informatics_accuracy.json')


def families():
    chapters, extra = [], {}
    for mod, fn in (('g12_informatics_a', 'fams_ch01'), ('g12_informatics_b', 'fams_ch02_03'), ('g12_informatics_c', 'fams_ch04_06')):
        chs, E = getattr(__import__(mod), fn)()
        chapters += chs
        extra.update(E)
    fams = K.fact_families(chapters, extra, drop_case=CODE_SUBTOPICS, code=CODE_SUBTOPICS)
    return K.assign_kinds(fams)


def main():
    b = Builder(SID, 'scripts/questions/cbse/g12_informatics.py', families(), MOCK_PATTERN, mock_minutes_per_mark=2.5)
    files = b.build()
    acc = json.load(open(ACC)) if os.path.exists(ACC) else None
    b.write(files, accuracy=acc)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
