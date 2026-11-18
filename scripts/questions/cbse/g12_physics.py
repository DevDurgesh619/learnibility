#!/usr/bin/env python3
"""Generate the CBSE class 12 physics question bank (cbse-g12-physics, NCERT Physics XII, 1,598 questions).

Families live in g12_physics_a.py (ch01-05), g12_physics_b.py (ch06-10), g12_physics_c.py (ch11-14).
Mock pattern is the CBSE class XII board paper (70 marks, 33 questions):
A 16 x 1 (12 MCQ + 4 A-R), B 5 x 2, C 7 x 3, D 2 case x 4, E 3 x 5.

Run: python3 scripts/questions/cbse/g12_physics.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g12-physics'
MOCK_PATTERN = [(12, 1, 'mcq'), (4, 1, 'ar'), (5, 2, 'short'), (7, 3, 'short3'), (2, 4, 'case'), (3, 5, 'long')]


def families():
    fams = {}
    for mod in ('g12_physics_a', 'g12_physics_b', 'g12_physics_c'):
        fams.update(__import__(mod).FAMILIES)
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g12_physics.py', families(), MOCK_PATTERN, mock_minutes_per_mark=180 / 70)
    files = b.build()
    b.write(files)  # keeps accuracyChecks already in _status.json
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
