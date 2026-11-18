#!/usr/bin/env python3
"""Generate the CBSE class 12 Applied Mathematics (241) question bank (cbse-g12-applied-maths).

Families live in g12_applied_maths_a.py (ch 1-3: numbers, quantification and numerical applications;
algebra/matrices; determinants and Cramer's rule), g12_applied_maths_b.py (ch 4-6 and 13: calculus and its
business applications, differential equations, linear programming) and g12_applied_maths_c.py (ch 7-12:
probability distributions, inferential statistics, index numbers and time series, financial mathematics);
shared helpers are in g12_applied_maths_h.py. Several algebra, calculus and LPP subtopics re-use the
041 (g12_maths_*) families, filtered so that no trigonometric content reaches the 241 bank. Mocks follow
the CBSE class XII pattern (38 questions, 80 marks).

Run: python3 scripts/questions/cbse/g12_applied_maths.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
from g9_maths_h import polish  # noqa: E402
from g12_maths_h import tidy  # noqa: E402

SID = 'cbse-g12-applied-maths'

# A 20×1 (18 MCQ + 2 A-R), B 5×2, C 6×3, D 4×5, E 3 case-based×4 = 80 marks, 38 questions.
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'sa2'), (6, 3, 'sa3'), (4, 5, 'la5'), (3, 4, 'case')]
SLOT_KINDS = {'explain': 'sa2', 'numerical': 'sa2', 'multi_step': 'sa3', 'long': 'la5'}

ACCURACY = [
    {
        'date': '2026-11-18',
        'method': 'one generated variant of every family read and checked; 5 random items per chapter from the built files re-solved by hand (65 items), then 4 more per '
                  'chapter for ch07-ch12 and 4 mock items (28) and a third draw of 16 items from ch07, ch08, ch10, ch11; calculus families verified numerically from '
                  'private check data (3,121 checks) and by parsing 676 answers back into functions; re-used 041 families filtered so that no trigonometric content remains',
        'checked': 109,
        'mismatches': 1,
        'mismatchDetail': ['ch11 EMI split: the stated EMI (₹1,46,626.18 for ₹16,50,000 at 1% a month, 12 months) came from the rounded factor 1.1268 and was about ₹26 above the exact EMI'],
        'fixes': ['EMI in the interest/principal split now computed from the exact (1 + i)ⁿ',
                  'perpetuity stem that asked for both the sum and the payment rewritten as a single question',
                  'z-statistic keys bracket the standard error: (130.6 − 130)/(3/4)',
                  'Poisson keys: e^(−λ)λ written without ^1/1!; "exactly 0 defective" written "no defective"; eggs replaced by pens in the machine-defect items',
                  'Poisson parameter item made parametric (kP(X = a) = P(X = a + 1)) instead of three fixed variants',
                  'singular nouns after 1 (1 year, 1 file, 1 order); (1/−6) written −(1/6); trailing "+ 0" in curve equations removed; "subtract (−6)" written "add 6"'],
        'note': 'Bank regenerated and revalidated after the fixes.',
    },
]


def families():
    fams = {}
    for mod in ('g12_applied_maths_a', 'g12_applied_maths_b', 'g12_applied_maths_c'):
        fams.update(__import__(mod).FAMILIES)
    for lst in fams.values():
        for f in lst:
            k = SLOT_KINDS.get(f.type)
            if k and k not in f.kinds:
                f.kinds = tuple(f.kinds) + (k,)
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g12_applied_maths.py', families(), MOCK_PATTERN)
    files = b.build()
    polish(files)
    tidy(files)
    b.write(files, accuracy=ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
