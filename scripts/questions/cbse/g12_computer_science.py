#!/usr/bin/env python3
"""Generate the CBSE class 12 Computer Science (083) question bank (cbse-g12-computer-science, 1,032 questions).

Families: g12_computer_science_a.py (ch 1-2 Python revision, functions, exceptions), _b.py (ch 3-4 files, stack),
_c.py (ch 5-6 networks, data communication), _d.py (ch 7-9 databases, SQL, Python-MySQL); helpers in
g12_computer_science_kit.py; fact tables are turned into families by g12_hum_engine.py.
Every code output is computed by running the code (Python in a temporary folder; SQL on sqlite3 with MySQL-style
functions), never typed by hand.

Paper (SQP 2026-27, 70 marks, 37 questions): A 21 × 1 (19 MCQ + 2 Assertion-Reason), B 7 × 2, C 3 × 3,
D 4 × 4 (case/program/SQL), E 2 × 5 (network design case, file/database program).

Run: python3 scripts/questions/cbse/g12_computer_science.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
import g12_computer_science_kit as K  # noqa: E402

SID = 'cbse-g12-computer-science'
MOCK_PATTERN = [(19, 1, 'mcq'), (2, 1, 'ar'), (7, 2, 'k2'), (3, 3, 'k3'), (4, 4, 'k4'), (2, 5, 'k5')]
CODE_SUBTOPICS = [f'{SID}-ch0{c}-st{s}' for c, n in ((1, 4), (2, 3), (3, 5), (4, 3), (9, 3)) for s in range(1, n + 1)] + \
                 [f'{SID}-ch08-st{s}' for s in range(1, 6)]
ACC = os.path.join(HERE, 'g12_computer_science_accuracy.json')


def families():
    chapters, extra = [], {}
    for mod, fn in (('g12_computer_science_a', 'fams_ch01_02'), ('g12_computer_science_b', 'fams_ch03_04'),
                    ('g12_computer_science_c', 'fams_ch05_06'), ('g12_computer_science_d', 'fams_ch07_09')):
        chs, E = getattr(__import__(mod), fn)()
        chapters += chs
        extra.update(E)
    fams = K.fact_families(chapters, extra, drop_case=CODE_SUBTOPICS, code=CODE_SUBTOPICS)
    return K.assign_kinds(fams)


def main():
    b = Builder(SID, 'scripts/questions/cbse/g12_computer_science.py', families(), MOCK_PATTERN, mock_minutes_per_mark=2.5)
    files = b.build()
    acc = json.load(open(ACC)) if os.path.exists(ACC) else None
    b.write(files, accuracy=acc)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
