#!/usr/bin/env python3
"""Generate the CBSE class 11 Applied Mathematics (241) question bank (cbse-g11-applied-maths, 1,514 questions).

Families live in g11_applied_maths_a.py (ch01-04, plus shared helpers and the reuse of cbse-g11-maths families for
topics common to both syllabuses), g11_applied_maths_b.py (ch05-09) and g11_applied_maths_c.py (ch10-14).
Reused cbse-g11-maths families are copies; any variant mentioning trigonometry is rejected (Applied Mathematics has none).

Mock pattern: class XII design assumed for the school annual exam (80 marks, 38 questions, 3 hours):
A 20 x 1 (18 MCQ + 2 Assertion-Reason), B 5 x 2, C 6 x 3, D 4 x 5 (long5: only genuine long-answer families), E 3 case x 4.

Run: python3 scripts/questions/cbse/g11_applied_maths.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder, DNUM  # noqa: E402
from g11_maths_a import mpolish  # noqa: E402
from g11_physics_util import polish  # noqa: E402

SID = 'cbse-g11-applied-maths'
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'short'), (6, 3, 'short3'), (4, 5, 'long5'), (3, 4, 'case')]

ACCURACY = [{
    'date': '2026-11-18',
    'method': 'Two rounds of random items from the generated files (5 per chapter, then 3 per chapter: 112 items) plus one full mock '
              '(38 items) re-solved independently by hand (arithmetic re-done, dates checked against the calendar, GST/annuity/correlation '
              'values recomputed)',
    'checked': 150,
    'mismatches': 2,
    'fixes': [
        'reused cbse-g11-maths GP family "5th and 7th terms given" dropped here: it gave only r = 2 when r = ±2 both fit',
        'reused cbse-g11-maths limit family that could produce a trivial (p(x))/(p(x)) limit dropped from Applied Mathematics',
        'reused families filtered so that no variant mentions trigonometry (not in the 241 syllabus); slope-from-angle, angle-between-lines, '
        'normal-form and trig-limit families excluded',
        'continuity key text "−1a + b" rewritten as "−a + b"; "1 units" wording fixed; f⁻¹ of (ax + b)/(cx + d) normalised to a positive leading denominator',
        'income-tax slabs, cess, GST rates and tariffs are always stated in the question, so answers do not depend on a particular year\'s rates',
    ],
}]


def families():
    fams = {}
    for mod in ('g11_applied_maths_a', 'g11_applied_maths_b', 'g11_applied_maths_c'):
        fams.update(__import__(mod).FAMILIES)
    for fs in fams.values():
        for f in fs:
            if 'long5' not in f.kinds and (f.type == 'long' or (f.type == 'multi_step' and f.C == 'C4' and DNUM[f.D] >= 4)):
                f.kinds = tuple(f.kinds) + ('long5',)
    return polish(mpolish(fams))


def main():
    b = Builder(SID, 'scripts/questions/cbse/g11_applied_maths.py', families(), MOCK_PATTERN, mock_minutes_per_mark=180 / 80)
    files = b.build()
    b.write(files, accuracy=ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
