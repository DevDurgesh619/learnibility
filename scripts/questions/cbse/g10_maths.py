#!/usr/bin/env python3
"""Generate the CBSE class 10 maths question bank (cbse-g10-maths, 1,628 questions).

Families for every subtopic of NCERT Mathematics X (rationalised syllabus) live in g10_maths_a.py (ch 1-5),
g10_maths_b.py (ch 6-10) and g10_maths_c.py (ch 11-14); they reuse helpers in g9_maths_h.py and a few
class 9 families (coordinate geometry, APs, probability). Each chapter gets a 60-item mastery bank and
two parallel 20-item practice forms; six mocks follow the CBSE Class X pattern (38 questions, 80 marks).

Run: python3 scripts/questions/cbse/g10_maths.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
from g9_maths_h import polish  # noqa: E402

SID = 'cbse-g10-maths'

# A 20×1 (18 MCQ + 2 A-R), B 5×2, C 6×3, D 4×5, E 3 case-based×4 = 80 marks, 38 questions.
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'short'), (6, 3, 'short3'), (4, 5, 'long'), (3, 4, 'case')]

ACCURACY = [
    {
        'date': '2026-11-18',
        'method': 'one generated variant of every family (about 420 generators) read and checked, plus 5 random items per chapter from the built files re-solved by hand (70 items)',
        'checked': 70,
        'mismatches': 1,
        'mismatchDetail': ['ch04 quadratic-formula item gave x = (6 ± 2√5)/2 instead of the simplest form 3 ± √5'],
        'fixes': ['quadratic-formula answers reduced to simplest surd form',
                  'coefficient-1 display fixed (1x, 1p, 1q, 1n) and polynomials built with the shared poly/term helpers',
                  'rationalised forms simplified (4/√2 = 2√2); redundant "= 1/52 = 1/52" style keys removed; plural "unit(s)"',
                  'surd heights shown as (p + q√3) m ≈ value, with the positive term first',
                  'generators with too few variants (ages, BPT algebra, trapezium diagonals, mensuration radii) widened',
                  'similar-triangle perimeter items give terminating answers; implausible or duplicate distractors replaced',
                  'class 9 wording "Baudhayana-Pythagoras theorem" replaced by the NCERT X "Pythagoras theorem"'],
    },
    {
        'date': '2026-11-18',
        'method': 'second pass after regeneration: 5 new random items per chapter re-solved by hand (70 items)',
        'checked': 70,
        'mismatches': 0,
        'fixes': [],
        'note': 'Bank regenerated and revalidated after each pass.',
    },
]


def families():
    fams = {}
    for mod in ('g10_maths_a', 'g10_maths_b', 'g10_maths_c'):
        fams.update(__import__(mod).FAMILIES)
    return fams


def _class10_terms(files: dict) -> None:
    """NCERT X says 'Pythagoras theorem' (the class 9 Ganita Manjari wording is Baudhayana-Pythagoras)."""
    for items in files.values():
        for q in items:
            for k in ('stem', 'answer', 'key'):
                if isinstance(q.get(k), str):
                    q[k] = q[k].replace('Baudhayana-Pythagoras theorem', 'Pythagoras theorem')
            if isinstance(q.get('options'), list):
                q['options'] = [o.replace('Baudhayana-Pythagoras theorem', 'Pythagoras theorem') if isinstance(o, str) else o for o in q['options']]


def main():
    b = Builder(SID, 'scripts/questions/cbse/g10_maths.py', families(), MOCK_PATTERN)
    files = b.build()
    polish(files)
    _class10_terms(files)
    b.write(files, accuracy=ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
