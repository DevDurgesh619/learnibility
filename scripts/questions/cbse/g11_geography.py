#!/usr/bin/env python3
"""Generate the CBSE class 11 Geography (029) question bank (cbse-g11-geography, 1930 questions).

Fact tables per subtopic live in g11_geography_a.py (Fundamentals of Physical Geography, chapters 1-6),
g11_geography_b.py (chapters 7-12), g11_geography_c.py (India: Physical Environment, chapters 13-17) and
g11_geography_d.py (Practical Work in Geography Part I, chapters 18-23). Computed items (scale conversion,
local time, projection construction, gradient, pixels, lapse rate, humidity, salinity, heat budget) are in
g11_geography_num.py. g12_hum_engine.py turns the tables into question families; g11_hum_kit adds a two-part
3-mark item (reason + correction) per subtopic. No textbook passage is reproduced.

Paper pattern (theory 70 marks, 30 questions, on the XI/XII design): Section A 17 × 1 (15 MCQ + 2 Assertion-Reason),
Section B 2 source-based × 3, Section C 4 × 3, Section D 5 × 5 long answers, Section E 2 map items × 5
(world map for the oceans chapters, political map of India for the India chapters).

Run: python3 scripts/questions/cbse/g11_geography.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import g12_hum_engine as E  # noqa: E402
import g11_hum_kit as K  # noqa: E402
from g11_geography_num import EXTRA  # noqa: E402

SID = 'cbse-g11-geography'
MOCK_PATTERN = [(15, 1, 'mcq'), (2, 1, 'ar'), (2, 3, 'case'), (4, 3, 'short3'), (5, 5, 'long'), (2, 5, 'map')]
DEFAULTS = {'long_marks': 5, 'map_n': 5, 'case_marks': (1, 1, 1)}


def chapters():
    out = []
    for mod in ('g11_geography_a', 'g11_geography_b', 'g11_geography_c', 'g11_geography_d'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


def extras(chs):
    out = dict(EXTRA)
    for subs, _ in chs:
        for sb in subs:
            out = K.merge(out, {sb.sid: K.combo(sb, marks=3, C='C3', D='D3')})
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (115 items) plus one full mock (30 items) re-solved by hand against '
              'NCERT Fundamentals of Physical Geography, India: Physical Environment and Practical Work in Geography Part I; '
              'numeric items (scale conversion, local time, gradient, R sin φ, pixels, lapse rate) recomputed',
    'checked': 145,
    'mismatches': 0,
    'fixes': [
        'salt-lake salinity figures (Lake Van, Dead Sea) removed; only qualitative statements kept',
        'thermocline described as the layer below the warm surface layer, about 500-1,000 m thick',
        'Kangchenjunga described as the third highest peak of the world rather than the highest peak in India',
        'easterly jet stream described as steering tropical depressions into India, as in NCERT',
        'non-geographical MCQ distractors (chapters 1, 3, 6, 13, 18, 22) replaced with same-topic alternatives',
    ],
}]

if __name__ == '__main__':
    chs = chapters()
    E.run(SID, 'scripts/questions/cbse/g11_geography.py', chs, MOCK_PATTERN, extra=extras(chs), accuracy=ACCURACY or None)
