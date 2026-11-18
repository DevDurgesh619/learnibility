#!/usr/bin/env python3
"""Generate the CBSE class 10 English (Language and Literature 184) question bank (cbse-g10-english, 1746 questions).

Chapter data: g10_english_a.py (First Flight ch 1-10), g10_english_b.py (First Flight ch 11-19),
g10_english_c.py (Footprints Without Feet ch 20-28 and the original Section A reading passages).
Engines: g10_english_kit.py and g10_english_kit_grammar.py (own snapshot of the g8/g9/g12 English kit plus class 10
additions: analytical paragraph, mixed grammar set, board-paper mock families).

Mock design = CBSE board paper (80 marks, 11 questions):
 A Reading 20: Q1 discursive passage 10, Q2 case-based factual passage 10;
 B Grammar 10 + Writing 10: Q3 ten grammar items, Q4 formal letter 5, Q5 analytical paragraph 5;
 C Literature 40: Q6 prose extract 5, Q7 poetry extract 5, Q8 First Flight 4 x 3, Q9 Footprints 2 x 3,
   Q10 First Flight long answer 6, Q11 Footprints long answer 6.

Run: python3 scripts/questions/cbse/g10_english.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from g10_english_kit import run, mock_extra_g10, PATTERN_G10  # noqa: E402
import g10_english_a  # noqa: E402
import g10_english_b  # noqa: E402
import g10_english_c  # noqa: E402

SID = 'cbse-g10-english'


def main():
    chapters = {**g10_english_a.CH, **g10_english_b.CH, **g10_english_c.CH}
    acc = None
    p = os.path.join(HERE, 'g10_english_accuracy.json')
    if os.path.exists(p):
        acc = json.load(open(p, encoding='utf-8'))
    run(SID, 'scripts/questions/cbse/g10_english.py', 10, chapters, PATTERN_G10, g10_english_c.PASSAGES,
        mock_extra_g10(SID, g10_english_c.PASSAGES), acc)


if __name__ == '__main__':
    main()
