#!/usr/bin/env python3
"""Generate the CBSE class 11 History question bank (cbse-g11-history, 627 questions).

Fact tables per subtopic live in g11_history_a.py (chapters 1-4) and g11_history_b.py (chapters 5-7)
of NCERT Themes in World History; g12_hum_engine.py turns them into question families.

Paper pattern (school annual exam on the XI-XII design, 80 marks, 34 questions): Section A 21 × 1
(19 MCQ + 2 Assertion-Reason), Section B 6 × 3 short answers, Section C 3 × 8 long answers,
Section D 3 source-based × 4, Section E 1 map × 5.

Run: python3 scripts/questions/cbse/g11_history.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import g12_hum_engine as E  # noqa: E402

SID = 'cbse-g11-history'
MOCK_PATTERN = [(19, 1, 'mcq'), (2, 1, 'ar'), (6, 3, 'short3'), (3, 8, 'long'), (3, 4, 'case'), (1, 5, 'map')]


def chapters():
    out = []
    for mod in ('g11_history_a', 'g11_history_b'):
        out += __import__(mod).CHAPTERS
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5-6 random generated items per chapter (40 items) plus one full mock (34 items) re-solved by hand against '
              'NCERT Themes in World History (class XI); dates, chronology orders and map places checked',
    'checked': 74,
    'mismatches': 0,
    'fixes': [
        'Khwarazm campaign cause reworded to the killing of Mongol envoys and merchants at Otrar, as in NCERT',
        'Mabo judgement reason reworded to say Australia was not empty land before the British arrived (terra nullius rejected)',
    ],
}]

if __name__ == '__main__':
    E.run(SID, 'scripts/questions/cbse/g11_history.py', chapters(), MOCK_PATTERN, accuracy=ACCURACY or None)
