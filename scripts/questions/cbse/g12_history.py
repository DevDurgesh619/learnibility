#!/usr/bin/env python3
"""Generate the CBSE class 12 History question bank (cbse-g12-history, 1,104 questions).

Fact tables per subtopic live in g12_history_a.py (chapters 1-4), g12_history_b.py (5-8) and
g12_history_c.py (9-12); g12_hum_engine.py turns them into question families.

Paper pattern (SQP 2026-27, 80 marks, 34 questions): Section A 21 × 1 (19 MCQ + 2 Assertion-Reason),
Section B 6 × 3 short answers, Section C 3 × 8 long answers, Section D 3 source-based × 4,
Section E 1 map × 5.

Run: python3 scripts/questions/cbse/g12_history.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import g12_hum_engine as E  # noqa: E402

SID = 'cbse-g12-history'
MOCK_PATTERN = [(19, 1, 'mcq'), (2, 1, 'ar'), (6, 3, 'short3'), (3, 8, 'long'), (3, 4, 'case'), (1, 5, 'map')]


def chapters():
    out = []
    for mod in ('g12_history_a', 'g12_history_b', 'g12_history_c'):
        try:
            m = __import__(mod)
        except ModuleNotFoundError:
            continue
        out += m.CHAPTERS
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (60 items) plus one full mock re-solved by hand against NCERT '
              'Themes in Indian History I-III; every fact line in the tables re-checked against the NCERT chapters',
    'checked': 94,
    'mismatches': 0,
    'fixes': [
        'removed unverified claims (drain inspection holes, iron ploughshare in Punjab/Rajasthan, Mahanavami deity, Multan clue)',
        'corrected Asokan script/language statement and the Piyadassi identification wording',
        'Ibn Battuta postal-system reason restated (Sind news in five days vs fifty-day journey)',
        "Match-List header no longer prints '(List I)'; A-R statements capitalised",
        'source items no longer ask to identify a term that is absent from the extract',
        'map items use an outline map of the Indian subcontinent (sites in Pakistan and Afghanistan)',
        'mock 3-mark section only draws 3-4 mark answers; 2-mark reason items excluded',
    ],
}]

if __name__ == '__main__':
    E.run(SID, 'scripts/questions/cbse/g12_history.py', chapters(), MOCK_PATTERN, accuracy=ACCURACY)
