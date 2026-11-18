#!/usr/bin/env python3
"""Generate the CBSE class 10 social science question bank (cbse-g10-social-science, 1,988 questions).

Fact tables per subtopic live in g10_social_science_a.py (History, ch01-05), _b.py (Geography, ch06-12),
_c.py (Political Science, ch13-17) and _d.py (Economics, ch18-22, with computed items); the family kit is
g8_social_science_kit.py, shared with classes 8 and 9.

Run: python3 scripts/questions/cbse/g10_social_science.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
import g8_social_science as base  # noqa: E402

SID = 'cbse-g10-social-science'
GRADE = 10
MODULES = ('g10_social_science_a', 'g10_social_science_b', 'g10_social_science_c', 'g10_social_science_d')
# CBSE Class X SS board pattern: 38 questions, 80 marks (MCQ 20 incl. 2 A-R, SA 2/3, LA 5, case 4, map 5).
MOCK_PATTERN = base.MOCK_PATTERN

ACCURACY = [{
    'date': '2026-11-18',
    'method': 'random generated items re-solved independently (5 per chapter plus 5 mock items, then 3 per chapter plus 3 mock items with '
              'a second seed); computed economics items (per capita income, average income, literacy rate, BMI, GDP and value added, sector '
              'share, bank lending, cost of credit, consumer commission jurisdiction) and map items recomputed or checked by hand; fact tables '
              'reviewed line by line before generation',
    'checked': 197,
    'mismatches': 0,
    'fixes': [
        'review: silly distractor "1876 BCE" for Amar Jiban replaced with 1890',
        'review: chronology rows with equal years (Ford Motors in India and WTO, both 1995) removed',
        'review: assertion on the RTI Act and consumer right to information rewritten (the two are different rights)',
        'build: subtopic ch10-st1 had no C4 item; added an evaluate question on the uneven distribution of minerals',
        'build: computed MCQs (GDP, sector share, literacy rate) could repeat an option; generators now reject repeats',
    ],
    'note': 'Generators fixed, bank regenerated and revalidated.',
}]


def families():
    return base.families(SID, MODULES, GRADE)


def main():
    b = Builder(SID, 'scripts/questions/cbse/g10_social_science.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
