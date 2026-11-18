#!/usr/bin/env python3
"""Generate the CBSE class 9 English question bank (cbse-g9-english, NCERT Kaveri, 1002 questions).

Chapter data: g9_english_a.py (ch 1-8 and reading passages), g9_english_b.py (ch 9-16).
Engines: eng_kit_g8_g9_g12.py (literature, vocabulary, writing, reading, mocks) and eng_kit_g8_g9_g12_grammar.py.
Mock design (school exam following the official Class 9 CBSE design, 80 marks, 14 questions):
Reading 2 x 10, Grammar 2 x 5, Writing 4 x 5, Literature 2 extracts x 5 + 2 short-answer sets x 4 + 2 long answers x 6.

Run: python3 scripts/questions/cbse/g9_english.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from eng_kit_g8_g9_g12 import run, mock_extra_g8_g9, PATTERN_G8_G9  # noqa: E402
import g9_english_a  # noqa: E402
import g9_english_b  # noqa: E402

SID = 'cbse-g9-english'


def main():
    chapters = {**g9_english_a.CH, **g9_english_b.CH}
    acc = None
    p = os.path.join(HERE, 'g9_english_accuracy.json')
    if os.path.exists(p):
        acc = json.load(open(p, encoding='utf-8'))
    run(SID, 'scripts/questions/cbse/g9_english.py', 9, chapters, PATTERN_G8_G9, g9_english_a.PASSAGES, mock_extra_g8_g9(SID, 9, g9_english_a.PASSAGES), acc)


if __name__ == '__main__':
    main()
