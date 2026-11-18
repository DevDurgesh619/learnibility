#!/usr/bin/env python3
"""Generate the CBSE class 12 biology question bank (cbse-g12-biology, 1368 questions).

Families per subtopic live in g12_biology_a.py (chapters 1-4), _b.py (chapters 5-8) and _c.py (chapters 9-13);
the fact-table kit shared with the class 12 science banks is g11_chemistry_kit.py.
Mocks follow the CBSE Class XII theory SQP design: 33 questions, 70 marks.

Run: python3 scripts/questions/cbse/g12_biology.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402
from g11_chemistry_kit import SCIENCE_PATTERN  # noqa: E402

SID = 'cbse-g12-biology'
MODS = ('g12_biology_a', 'g12_biology_b', 'g12_biology_c')


def families():
    fams = {}
    for mod in MODS:
        try:
            m = __import__(mod)
        except ModuleNotFoundError:
            continue
        fams.update(m.FAMILIES)
    return fams


def accuracy():
    p = os.path.join(HERE, 'g12_biology_accuracy.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def main():
    b = Builder(SID, 'scripts/questions/cbse/g12_biology.py', families(), SCIENCE_PATTERN)
    files = b.build()
    b.write(files, accuracy())
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
