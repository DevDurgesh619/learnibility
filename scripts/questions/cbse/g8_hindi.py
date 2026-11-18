#!/usr/bin/env python3
"""Generate the CBSE class 8 Hindi (Malhar) question bank (cbse-g8-hindi, 645 questions).

Families live in g8_hindi_a.py (chapters 1-5) and g8_hindi_b.py (chapters 6-10); shared helpers in
g8_hindi_lib.py, grammar tables in g8_hindi_gram.py, original अपठित passages in g8_hindi_passages.py.
No textbook passage is reproduced; Kabir's dohe (15th century) are public domain.

Run: python3 scripts/questions/cbse/g8_hindi.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g8-hindi'

# Class 9/10 CBSE Hindi design (cost sheet): अपठित 14, व्याकरण 16, पाठ्यपुस्तक 30, लेखन 20 = 80 marks, 15 questions.
MOCK_PATTERN = [
    (2, 7, 'apathit'),    # अपठित गद्यांश / काव्यांश, 7 each
    (4, 4, 'vyak'),       # व्याकरण, 4 parts × 1
    (2, 5, 'path_ext'),   # पाठ-आधारित बहुविकल्पी (5 × 1)
    (2, 6, 'path6'),      # पाठ्यपुस्तक: 3 × 2 अंक
    (2, 4, 'path4'),      # पाठ्यपुस्तक: 2 × 2 अंक
    (1, 7, 'patra'),      # पत्र
    (1, 7, 'anuch'),      # अनुच्छेद
    (1, 6, 'samvad'),     # संवाद
]


def families():
    fams = {}
    for mod in ('g8_hindi_a', 'g8_hindi_b'):
        fams.update(__import__(mod).FAMILIES)
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g8_hindi.py', families(), MOCK_PATTERN, mock_minutes_per_mark=2.25)
    files = b.build()
    b.write(files)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
