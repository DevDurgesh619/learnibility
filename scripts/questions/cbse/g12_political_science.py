#!/usr/bin/env python3
"""Generate the CBSE class 12 Political Science question bank (cbse-g12-political-science).

Fact tables per subtopic live in g12_political_science_a.py (Contemporary World Politics, chapters 1-7)
and g12_political_science_b.py (Politics in India since Independence, chapters 8-15);
g12_hum_engine.py turns them into question families.

Paper pattern (SQP 2026-27, 80 marks, 30 questions): Section A 12 × 1 (10 MCQ + 2 Assertion-Reason),
Section B 6 × 2, Section C 5 × 4, Section D 2 source/cartoon-based × 4 and 1 map × 4, Section E 4 × 6
long answers.

Run: python3 scripts/questions/cbse/g12_political_science.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import g12_hum_engine as E  # noqa: E402

SID = 'cbse-g12-political-science'
MOCK_PATTERN = [(10, 1, 'mcq'), (2, 1, 'ar'), (6, 2, 'short'), (5, 4, 'short3'), (2, 4, 'case'), (1, 4, 'map'),
                (4, 6, 'long')]
DEFAULTS = {'long_marks': 6, 'map_n': 4}


def chapters():
    out = []
    for mod in ('g12_political_science_a', 'g12_political_science_b'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (75 items) plus one full mock (30 items) re-solved by hand against '
              'NCERT Contemporary World Politics and Politics in India since Independence',
    'checked': 105,
    'mismatches': 0,
    'fixes': [
        'Kerala 1959 dismissal reason restated as NCERT does (cited as the first misuse of Article 356), not a "first use" claim',
        'Assertion-Reason items no longer use a pronoun-led statement (e.g. "Local communities protect them...") as an unrelated Reason',
        'hand-written long/short items can be redrawn after a rejected draw, so all 6 mocks get 4 distinct 6-mark answers',
    ],
}]

if __name__ == '__main__':
    E.run(SID, 'scripts/questions/cbse/g12_political_science.py', chapters(), MOCK_PATTERN, accuracy=ACCURACY)
