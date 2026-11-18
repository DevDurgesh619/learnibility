#!/usr/bin/env python3
"""Generate the CBSE class 9 maths question bank (cbse-g9-maths, 1,514 questions).

Families for every subtopic of NCERT Ganita Manjari (2026-27) live in g9_maths_a.py (ch 1-5),
g9_maths_b.py (ch 6-10) and g9_maths_c.py (ch 11-14); helpers in g9_maths_h.py.
Each chapter gets a 60-item mastery bank and two parallel 20-item practice forms; three mocks
follow the assumed Class X pattern (38 questions, 80 marks).

Run: python3 scripts/questions/cbse/g9_maths.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
from g9_maths_h import polish  # noqa: E402

SID = 'cbse-g9-maths'

# A 20×1 (18 MCQ + 2 A-R), B 5×2, C 6×3, D 4×5, E 3 case-based×4 = 80 marks, 38 questions.
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'short'), (6, 3, 'short3'), (4, 5, 'long'), (3, 4, 'case')]


# Accuracy pass (brief step 5), recorded in _status.json as accuracyChecks.
ACCURACY = [
    {
        'date': '2026-11-18',
        'method': '5 random items per chapter from the built files re-solved by hand (70 items), plus one generated variant of every family (about 470 generators) read and checked',
        'checked': 70,
        'mismatches': 1,
        'mismatchDetail': ['ch04 factorisation item accepted 3(2x + 2y)(2x − 2y) for 12x² − 12y² (not fully factorised)'],
        'fixes': ['factorisation family now takes out the common factor and uses coprime coefficients',
                  'ASCII minus signs replaced by the true minus sign in all text',
                  'mark totals quoted in marking keys aligned with each item\'s marks',
                  'duplicate or equivalent MCQ distractors removed (factor order, intercepts, probabilities)',
                  'converse/inverse/contrapositive statements rewritten with a subject so they read grammatically',
                  'square-root-spiral items avoid perfect squares; science-fair and quiz cases give whole-number answers',
                  'number formatting: coefficient 1, fractions shown as decimals where they terminate, plurals'],
    },
    {
        'date': '2026-11-18',
        'method': 'second pass after regeneration: 5 new random items per chapter re-solved by hand (70 items)',
        'checked': 70,
        'mismatches': 2,
        'mismatchDetail': ['ch03 decimal-expansion explain item could pick 7/14 (= 1/2, terminating) but answered non-terminating',
                           'ch03 surd Assertion-Reason could pick (√5 + √5)²'],
        'fixes': ['numerator now coprime to the denominator and free of 3 and 7', 'surd A-R uses two different non-square surds',
                  'coefficient-1 display ("1a", "1x") and plural fixes'],
        'note': 'Bank regenerated and revalidated after each pass.',
    },
]


def families():
    fams = {}
    for mod in ('g9_maths_a', 'g9_maths_b', 'g9_maths_c'):
        fams.update(__import__(mod).FAMILIES)
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g9_maths.py', families(), MOCK_PATTERN)
    files = b.build()
    polish(files)
    b.write(files, accuracy=ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
