#!/usr/bin/env python3
"""Generate the CBSE class 11 Economics (030) question bank (cbse-g11-economics, 1207 questions).

Families live in g11_economics_a.py (Statistics ch 1-4), g11_economics_b.py (Statistics ch 5-8) and
g11_economics_c.py (Introductory Microeconomics ch 9-13); shared helpers in g11_economics_lib.py.
All numerical answers are computed in code. No textbook passage is reproduced.

Run: python3 scripts/questions/cbse/g11_economics.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g11-economics'

# Class XII design used for Class XI (cost sheet): 20 × 1 (18 MCQ + 2 A-R), 4 × 3, 6 × 4 (4 short + 2 case), 4 × 6 = 80 marks, 34 questions.
MOCK_PATTERN = [
    (18, 1, 'mcq'),
    (2, 1, 'ar'),
    (4, 3, 'q3'),
    (4, 4, 'q4'),
    (2, 4, 'case'),
    (4, 6, 'long6'),     # only true 6-mark families (marks=6) are tagged long6 below
]


def families():
    fams = {}
    for mod in ('g11_economics_a', 'g11_economics_b', 'g11_economics_c'):
        fams.update(__import__(mod).FAMILIES)
    for fs in fams.values():
        for f in fs:
            if f.marks == 6 and 'long6' not in f.kinds:
                f.kinds = tuple(f.kinds) + ('long6',)
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g11_economics.py', families(), MOCK_PATTERN, mock_minutes_per_mark=2.25)
    files = b.build()
    b.write(files)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
