#!/usr/bin/env python3
"""Generate the CBSE class 8 science question bank (cbse-g8-science, 1,222 questions).

NCERT Curiosity (Class 8), 13 chapters. Families live in g8_science_a.py (ch01-04),
g8_science_b.py (ch05-09) and g8_science_c.py (ch10-13); templates in sci_kit.py.

Run: python3 scripts/questions/cbse/g8_science.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from sci_kit import SciBuilder, finalize, strict_mock_fits  # noqa: E402

SID = 'cbse-g8-science'

# Assumed school paper mirroring the Class X Science design (cost sheet):
# A 20 x 1 (16 MCQ + 4 Assertion-Reason), B 6 x 2, C 7 x 3, D 3 case x 4, E 3 x 5 = 39 questions, 80 marks.
MOCK_PATTERN = [(16, 1, 'mcq'), (4, 1, 'ar'), (6, 2, 'short'), (7, 3, 'short3'), (3, 4, 'case'), (3, 5, 'long')]


def families():
    fams = {}
    for mod in ('g8_science_a', 'g8_science_b', 'g8_science_c'):
        fams.update(__import__(mod).FAMILIES)
    return finalize(fams)


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter plus 5 mock items re-solved independently (numericals recomputed by hand, facts checked against NCERT Curiosity Class 8)',
    'checked': 70,
    'mismatches': 2,
    'fixes': [
        'Odd-one-out MCQ on how diseases spread kept the positive stem ("Which of these diseases spreads ...") while asking for the odd one: '
        'answer did not match stem; CLS template now builds an explicit NOT stem (neg_tpl) and refuses templates without NOT',
        'Conduction-tester stem used "She" for any generated name; rewritten without a pronoun',
        'Solubility values aligned to the NCERT Class 9 table (KCl 35 g at 20 °C, NH4Cl 41 g at 40 °C)',
        'Moon-phase item: half moon at sunset placed high in the southern sky (first quarter), not in the west',
        'Mirror-images formula restricted to angles where 360/θ is even; hair dryer removed from heating-effect list (also has a motor)',
        'Key wording: plural terms ("Monsoon winds is"), "is bacteria" in disease keys, food-chain energy stem lost its commas',
    ],
    'note': 'Generators fixed and the subject regenerated and revalidated after the pass.',
}]


def main():
    strict_mock_fits()
    b = SciBuilder(SID, 'scripts/questions/cbse/g8_science.py', families(), MOCK_PATTERN, mock_minutes_per_mark=2.25)
    files = b.build()
    b.write(files, accuracy=ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
