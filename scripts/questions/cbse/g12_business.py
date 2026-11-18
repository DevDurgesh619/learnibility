#!/usr/bin/env python3
"""Generate the CBSE class 12 business studies question bank (cbse-g12-business).

NCERT Business Studies XII Parts I and II (054). Families per subtopic are fact tables in g12_business_a.py
(ch01-04), g12_business_b.py (ch05-08) and g12_business_c.py (ch09-12, plus computed trading-on-equity problems),
written with g12_business_a.spec() and turned into families by g11_accountancy_kit.facts().

Run: python3 scripts/questions/cbse/g12_business.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g12-business'

# CBSE Business Studies paper: 34 questions, 80 marks, 3 h.
# 20 x 1 (16 MCQ + 4 Assertion-Reason), 4 x 3, 6 x 4, 4 x 6.
MOCK_PATTERN = [(16, 1, 'mcq'), (4, 1, 'ar'), (4, 3, 'm3'), (6, 4, 'm4'), (4, 6, 'm6')]


def families():
    fams = {}
    for mod in ('g12_business_a', 'g12_business_b', 'g12_business_c'):
        fams.update(__import__(mod).FAMILIES)
    # "Which statement is correct?" items are direct recall of a textbook line.
    for fl in fams.values():
        for f in fl:
            if f.gen.__name__ == 'tf_true':
                f.D = 'D1'
    return fams


def main(accuracy=None):
    b = Builder(SID, 'scripts/questions/cbse/g12_business.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, accuracy)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return files


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random items per chapter re-answered from NCERT Business Studies XII (60 mixed items), then 4 more per chapter for '
              'ch09-12 (16 items: scenario, case, assertion-reason), plus 3 trading-on-equity EPS problems re-computed by hand',
    'checked': 79,
    'mismatches': 0,
    'fixes': [
        'contrast between factors of fixed and working capital removed: both lists share points (nature of business, scale, growth), which gave repeated MCQ options',
        'scenario and case stems that put a random product where it did not fit (a "low-sugar" or "cures all diseases" random product, a pack of bicycles) now name a fitting product',
        'trading-on-equity MCQ key lower-cased EPS and ROI; fixed',
        'consumer commission pecuniary limits stated as in the Act as enacted (NCERT), and labelled so'],
}]

if __name__ == '__main__':
    main(ACCURACY)
