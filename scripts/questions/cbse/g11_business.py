#!/usr/bin/env python3
"""Generate the CBSE class 11 business studies question bank (cbse-g11-business).

NCERT Business Studies XI (054). Families per subtopic are fact tables in g11_business_a.py
(ch01-03), g11_business_b.py (ch04-06) and g11_business_c.py (ch07-10), turned into families by
the shared helper g11_accountancy_kit.facts().

Run: python3 scripts/questions/cbse/g11_business.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g11-business'

# CBSE Business Studies design: 34 questions, 80 marks, 3 h.
# 20 x 1 (16 MCQ + 4 Assertion-Reason), 4 x 3, 6 x 4, 4 x 6.
MOCK_PATTERN = [(16, 1, 'mcq'), (4, 1, 'ar'), (4, 3, 'm3'), (6, 4, 'm4'), (4, 6, 'm6')]


def families():
    fams = {}
    for mod in ('g11_business_a', 'g11_business_b', 'g11_business_c'):
        fams.update(__import__(mod).FAMILIES)
    # "Which statement is correct?" items in business studies are direct recall of a textbook line.
    for fl in fams.values():
        for f in fl:
            if f.gen.__name__ == 'tf_true':
                f.D = 'D1'
    return fams


def main(accuracy=None):
    b = Builder(SID, 'scripts/questions/cbse/g11_business.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, accuracy)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return files


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random items per chapter re-answered from NCERT Business Studies XI (two rounds: 50 mixed items, then 50 '
              'explain/case/assertion-reason items), plus a read-through of every assertion-reason item in the fact tables',
    'checked': 100,
    'mismatches': 0,
    'fixes': [
        'three assertion-reason items whose intended code could be argued (risk/profit, insurance disclosure, resources of business) rewritten so the code is unambiguous',
        'justification for the policy on sick public enterprises was circular; now names referral to the BIFR',
        'four case stems put a random product where it did not fit (a "textbooks plant", a patented-technology handicrafts maker, etc.); products fixed in those cases',
        'two scenario families had fewer than four options and could not generate; pools widened',
        '"Which statement is correct?" recall items retagged D1'],
}]

if __name__ == '__main__':
    main(ACCURACY)
