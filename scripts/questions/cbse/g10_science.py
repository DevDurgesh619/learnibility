#!/usr/bin/env python3
"""Generate the CBSE class 10 science question bank (cbse-g10-science, 1,404 questions).

NCERT Science X (086), 13 chapters. Families live in g10_science_a.py (ch01-04 chemistry),
g10_science_b.py (ch05-08 biology) and g10_science_c.py (ch09-13 physics and environment);
templates in sci_kit.py.

Run: python3 scripts/questions/cbse/g10_science.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from sci_kit import SciBuilder, finalize, strict_mock_fits  # noqa: E402
import sci_kit  # noqa: E402

sci_kit.DEF_MCQ_MIN = 99  # definition items stay written (1-mark short); their MCQ form repeats option sets across mocks

SID = 'cbse-g10-science'

# CBSE Board paper (cost sheet): 39 questions, 80 marks, 3 h.
# A 20 x 1 (16 MCQ + 4 Assertion-Reason), B 6 x 2, C 7 x 3, D 3 case x 4, E 3 x 5.
# The board paper also groups questions by subject (Biology Q1-16, Chemistry Q17-29, Physics Q30-39);
# the shared Builder orders mock items by section type, not by subject, so that grouping is not reproduced.
MOCK_PATTERN = [(16, 1, 'mcq'), (4, 1, 'ar'), (6, 2, 'short'), (7, 3, 'short3'), (3, 4, 'case'), (3, 5, 'long')]


def families():
    fams = {}
    for mod in ('g10_science_a', 'g10_science_b', 'g10_science_c'):
        fams.update(__import__(mod).FAMILIES)
    return finalize(fams)


ACCURACY = {
    'date': '2026-11-18',
    'method': 'Random sample of 5 items per chapter file and 5 from mocks.json (seed 1010, 70 items), plus a second full sample on the final build (seed 77, 70 items); each re-solved by hand (balanced equations, mirror/lens formula with NCERT sign convention, Ohm/series-parallel/energy arithmetic, Mendel ratios) against NCERT class 10 values.',
    'checked': 140,
    'mismatches': 1,
    'fixes': [
        'ch07 response-type classification: ambiguous involuntary vs reflex category removed (one item keyed involuntary was arguably reflex).',
        'ch03 double-negative electrolyte NOT-question removed.',
        'ch04 saturated/unsaturated stem now says open-chain hydrocarbon.',
        'Definition MCQ form disabled (kept as 1-mark written) after two mocks drew near-identical option sets.',
    ],
}


def main():
    strict_mock_fits()
    b = SciBuilder(SID, 'scripts/questions/cbse/g10_science.py', families(), MOCK_PATTERN, mock_minutes_per_mark=2.25)
    files = b.build()
    b.write(files, accuracy=ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
