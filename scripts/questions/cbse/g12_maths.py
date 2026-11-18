#!/usr/bin/env python3
"""Generate the CBSE class 12 mathematics (041) question bank (cbse-g12-maths).

Families for every subtopic of NCERT Mathematics XII Parts I and II (rationalised syllabus) live in
g12_maths_a.py (ch 1-4: relations and functions, inverse trigonometric functions, matrices, determinants),
g12_maths_b.py (ch 5-9: continuity and differentiability, applications of derivatives, integrals,
applications of integrals, differential equations) and g12_maths_c.py (ch 10-13: vectors, 3D geometry,
linear programming, probability); shared helpers are in g12_maths_h.py. Each chapter gets a mastery bank
and two parallel practice forms; mocks follow the CBSE class XII pattern (38 questions, 80 marks).

Run: python3 scripts/questions/cbse/g12_maths.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
from g9_maths_h import polish  # noqa: E402
from g12_maths_h import tidy  # noqa: E402

SID = 'cbse-g12-maths'

# A 20×1 (18 MCQ + 2 A-R), B 5×2, C 6×3, D 4×5, E 3 case-based×4 = 80 marks, 38 questions.
# Custom kinds keep each section to families written for its marks (see SLOT_KINDS).
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'sa2'), (6, 3, 'sa3'), (4, 5, 'la5'), (3, 4, 'case')]
SLOT_KINDS = {'explain': 'sa2', 'numerical': 'sa2', 'multi_step': 'sa3', 'long': 'la5'}

ACCURACY = [
    {
        'date': '2026-11-18',
        'method': 'one generated variant of every family (about 480 generators) read and checked; 5 random items per chapter from the built files re-solved by hand (65 items); '
                  'calculus generators verified numerically from private check data (3,881 derivative/integral/ODE checks) and by parsing the answer text back into a function and differentiating it (1,018 answers)',
        'checked': 65,
        'mismatches': 1,
        'mismatchDetail': ['ch07 power-rule integral gave ∫ (2x + 1/x²) dx = x² + 1/x + C (sign of the 1/x term reversed for negative powers)'],
        'fixes': ['sign of reciprocal-power antiderivatives corrected and the whole family re-verified from the answer text',
                  'ambiguous fraction coefficients bracketed: (6/7)î, (39/5)e⁻⁵ˣ, (1/5)P, e^(x²/4), 1/(81π), 1/(6√134), 9t/8',
                  'unit coefficients and double signs removed (1x, −1k, + −, x − −4, 1 cos 4x); hyphen-minus replaced by true minus',
                  'partial-fraction stems and keys written as (px + q)/((x − a)(x − b)) with signed terms',
                  'maximum-profit item restricted to a positive maximum profit; area key ½|−50| shows a true minus',
                  'grammar: singular "1 hour/unit/ball/sq unit", "each souvenir of type A", defective/good bulbs',
                  'redundant "= 3/7 = 3/7" style steps removed from conditional-probability and direction-cosine keys'],
    },
    {
        'date': '2026-11-18',
        'method': 'second pass after regeneration: 5 new random items per chapter (65 items) plus 14 random mock items re-solved by hand',
        'checked': 79,
        'mismatches': 0,
        'fixes': ['presentation only: A² − tA + dI = O keys written with signed terms; unreduced (3/6)√ ellipse factor reduced'],
        'note': 'Bank regenerated and revalidated after each pass.',
    },
    {
        'date': '2026-11-18',
        'method': 'shared clean-up rules re-run while the applied-mathematics bank was checked; affected items re-read',
        'checked': 12,
        'mismatches': 0,
        'fixes': ['LPP corner-point MCQ key names both optimal corners (tie at (3, 4) and (0, 6))', '(1/−6) written −(1/6) in matrix-method keys; singular nouns after 1'],
    },
]


def families():
    fams = {}
    for mod in ('g12_maths_a', 'g12_maths_b', 'g12_maths_c'):
        fams.update(__import__(mod).FAMILIES)
    for lst in fams.values():
        for f in lst:
            k = SLOT_KINDS.get(f.type)
            if k and k not in f.kinds:
                f.kinds = tuple(f.kinds) + (k,)
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g12_maths.py', families(), MOCK_PATTERN)
    files = b.build()
    polish(files)
    tidy(files)
    b.write(files, accuracy=ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
