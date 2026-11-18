#!/usr/bin/env python3
"""Generate the CBSE class 12 Geography question bank (cbse-g12-geography).

Fact tables per subtopic live in g12_geography_a.py (Fundamentals of Human Geography, chapters 1-8),
g12_geography_b.py (India: People and Economy, chapters 9-17) and g12_geography_c.py (Practical Work
Part II, chapters 18-21); numeric families (density, growth, sex ratio, balance of trade, frequency
distribution, mean/median/mode, dispersion, rank correlation, pie angles, GIS) are in g12_geography_num.py.
g12_hum_engine.py turns the tables into question families.

Paper pattern (SQP 2026-27, theory 70 marks, 30 questions): Section A 17 × 1 (15 MCQ + 2 Assertion-Reason),
Section B 2 source-based × 3, Section C 4 × 3, Section D 5 × 5 long answers, Section E 2 map items × 5.

Run: python3 scripts/questions/cbse/g12_geography.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import g12_hum_engine as E  # noqa: E402
from g12_geography_num import EXTRA  # noqa: E402

SID = 'cbse-g12-geography'
MOCK_PATTERN = [(15, 1, 'mcq'), (2, 1, 'ar'), (2, 3, 'case'), (4, 3, 'short3'), (5, 5, 'long'), (2, 5, 'map')]
DEFAULTS = {'long_marks': 5, 'map_n': 5, 'case_marks': (1, 1, 1)}


def chapters():
    out = []
    for mod in ('g12_geography_a', 'g12_geography_b', 'g12_geography_c'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (105 items) plus one full mock (30 items) re-solved by hand against '
              'NCERT Fundamentals of Human Geography, India: People and Economy and Practical Work in Geography Part II; '
              'numeric items (frequency, standard deviation, rank correlation, choropleth classes, growth rate) recomputed',
    'checked': 135,
    'mismatches': 0,
    'fixes': [
        'match categories whose right-hand items repeated (push/pull, factor types) removed so no Match-List has two equal answers',
        'correlation match set no longer mixes a diagram name with coefficient values',
        'two Give-a-reason answers reworded to stand as full sentences (sex ratio, urban noise)',
        'NCERT sub-field list used for social geography; Kolkhoz item no longer names a leader not given in NCERT',
    ],
}]

if __name__ == '__main__':
    E.run(SID, 'scripts/questions/cbse/g12_geography.py', chapters(), MOCK_PATTERN, extra=EXTRA, accuracy=ACCURACY)
