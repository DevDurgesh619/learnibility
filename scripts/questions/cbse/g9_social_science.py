#!/usr/bin/env python3
"""Generate the CBSE class 9 social science question bank (cbse-g9-social-science, 1,314 questions).

Fact tables per subtopic live in g9_social_science_a.py (ch01-05), _b.py (ch06-10, with computed
economics items) and _c.py (ch11-15, with computed personal-finance items); the family kit is
g8_social_science_kit.py, shared with classes 8 and 10.

Run: python3 scripts/questions/cbse/g9_social_science.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
import g8_social_science as base  # noqa: E402

SID = 'cbse-g9-social-science'
GRADE = 9
MODULES = ('g9_social_science_a', 'g9_social_science_b', 'g9_social_science_c')
# Assumed school paper on the Class X SS design: 38 questions, 80 marks (see targets.json examPattern).
MOCK_PATTERN = base.MOCK_PATTERN

ACCURACY = [{
    'date': '2026-11-18',
    'method': 'random generated items re-solved independently (7 per chapter plus 7 mock items, then 3 per chapter plus 3 mock items '
              'after fixes); computed economics and finance items (opportunity cost, PPF, equilibrium, excess demand, CPI inflation, '
              'simple and compound interest, loan cost) recomputed by hand; fact tables reviewed line by line before generation',
    'checked': 160,
    'mismatches': 0,
    'fixes': [
        'review: "Kanchenjunga is the highest peak in India" reworded (claim depends on how K2 is treated); now "third highest peak in the world"',
        'review: distractors "Cherrapunji town of Assam", "Pangaea only", "cracy-tax" and "100 − inflation" replaced with plausible ones',
        'review: chronology rows with equal years (MUDRA and Digital India, both 2015) changed',
        'sample: "1 tractors" grammar in the PPF table',
        'sample: term "cVIGIL" was capitalised to "CVIGIL" in options; term renamed "the cVIGIL app"',
        'sample: revision-note case could ask two blanks with the same answer; now rejected',
        'sample: adjective definitions (sovereign, secular) rewritten as noun phrases so "Which term is used for ..." reads well',
    ],
    'note': 'Generators fixed, bank regenerated and revalidated.',
}]


def families():
    return base.families(SID, MODULES, GRADE)


def main():
    b = Builder(SID, 'scripts/questions/cbse/g9_social_science.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
