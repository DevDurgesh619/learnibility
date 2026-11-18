#!/usr/bin/env python3
"""Generate the CBSE class 11 mathematics question bank (cbse-g11-maths, NCERT Mathematics XI, 1,654 questions).

Families live in g11_maths_a.py (ch01-05, plus shared maths helpers), g11_maths_b.py (ch06-10) and g11_maths_c.py (ch11-14).
Mock pattern follows the class XII design assumed for the school annual exam (80 marks, 38 questions):
A 20 x 1 (18 MCQ + 2 A-R), B 5 x 2, C 6 x 3, D 4 x 5, E 3 case x 4.

Run: python3 scripts/questions/cbse/g11_maths.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g11-maths'
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'short'), (6, 3, 'short3'), (4, 5, 'long'), (3, 4, 'case')]


def families():
    fams = {}
    for mod in ('g11_maths_a', 'g11_maths_b', 'g11_maths_c'):
        fams.update(__import__(mod).FAMILIES)
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g11_maths.py', families(), MOCK_PATTERN, mock_minutes_per_mark=180 / 80)
    files = b.build()
    b.write(files)  # keeps accuracyChecks already in _status.json
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
