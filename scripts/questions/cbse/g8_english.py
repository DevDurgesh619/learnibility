#!/usr/bin/env python3
"""Generate the CBSE class 8 English question bank (cbse-g8-english, NCERT Poorvi, 942 questions).

Chapter data: g8_english_a.py (ch 1-8), g8_english_b.py (ch 9-15 and reading passages).
Engines: eng_kit_g8_g9_g12.py (literature, vocabulary, writing, reading, mocks) and eng_kit_g8_g9_g12_grammar.py.
Mock design (school exam modelled on the Class 9 CBSE paper, 80 marks, 14 questions):
Reading 2 x 10, Grammar 2 x 5, Writing 4 x 5, Literature 2 extracts x 5 + 2 short-answer sets x 4 + 2 long answers x 6.

Run: python3 scripts/questions/cbse/g8_english.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from eng_kit_g8_g9_g12 import run, mock_extra_g8_g9, PATTERN_G8_G9  # noqa: E402
import g8_english_a  # noqa: E402
import g8_english_b  # noqa: E402

SID = 'cbse-g8-english'


def main():
    chapters = {**g8_english_a.CH, **g8_english_b.CH}
    acc = None
    p = os.path.join(HERE, 'g8_english_accuracy.json')
    if os.path.exists(p):
        acc = json.load(open(p, encoding='utf-8'))
    run(SID, 'scripts/questions/cbse/g8_english.py', 8, chapters, PATTERN_G8_G9, g8_english_b.PASSAGES, mock_extra_g8_g9(SID, 8, g8_english_b.PASSAGES), acc)


if __name__ == '__main__':
    main()
