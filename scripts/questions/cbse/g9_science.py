#!/usr/bin/env python3
"""Generate the CBSE class 9 science question bank (cbse-g9-science, 1,197 questions).

NCERT Exploration (Class 9), 12 chapters. Families live in g9_science_a.py (ch01-04),
g9_science_b.py (ch05-08) and g9_science_c.py (ch09-12); templates in sci_kit.py.

Run: python3 scripts/questions/cbse/g9_science.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from sci_kit import SciBuilder, finalize, strict_mock_fits  # noqa: E402

SID = 'cbse-g9-science'

# School annual exam, assumed to mirror the Class X Science design (cost sheet):
# A 20 x 1 (16 MCQ + 4 Assertion-Reason), B 6 x 2, C 7 x 3, D 3 case x 4, E 3 x 5 = 39 questions, 80 marks.
MOCK_PATTERN = [(16, 1, 'mcq'), (4, 1, 'ar'), (6, 2, 'short'), (7, 3, 'short3'), (3, 4, 'case'), (3, 5, 'long')]


def families():
    fams = {}
    for mod in ('g9_science_a', 'g9_science_b', 'g9_science_c'):
        fams.update(__import__(mod).FAMILIES)
    return finalize(fams)


ACCURACY = {
    'date': '2026-11-18',
    'method': 'Random sample of 5 items per chapter file and 5 from mocks.json (seed 909, 65 items), plus a second sample of 5 each from ch09-ch12 and mocks (seed 31, 25 items); each re-solved by hand against NCERT class 9 values.',
    'checked': 90,
    'mismatches': 2,
    'fixes': [
        'ch09 wave-speed generators produced physically impossible speeds of sound (50 m/s, 200 m/s): now built from real media speeds (v = f lambda pairs and lambda = vT).',
        'ch09 vibration-source key read "A shehnai is an air column": key verb changed.',
        'ch06 energy categories reworded to "an object possessing kinetic/potential energy".',
        'ch04 colloid list: blood replaced by cheese (NCERT example).',
        'ch12 tree count now says "at least" for a rounded-up value.',
    ],
}


def main():
    strict_mock_fits()
    b = SciBuilder(SID, 'scripts/questions/cbse/g9_science.py', families(), MOCK_PATTERN, mock_minutes_per_mark=2.25)
    files = b.build()
    b.write(files, accuracy=ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
