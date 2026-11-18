#!/usr/bin/env python3
"""Generate the CBSE class 11 entrepreneurship question bank (cbse-g11-entrepreneurship, 662 questions).

CBSE Entrepreneurship XI (066), 7 chapters. Theory fact tables: g11_entrepreneurship_a.py (chapters 1, 2, 3 st1, 4),
g11_entrepreneurship_b.py (chapters 3 st2-st4, 5, 7) with tables shared with the class 12 syllabus copied into
g11_entrepreneurship_c.py; chapter 6 (Business Finance and Arithmetic) uses computed families copied into
g11_entrepreneurship_num.py. `efacts()` adapts g11_accountancy_kit.facts() to the 1/2/3/5-mark paper.

Mock pattern (CBSE theory paper, 70 marks, 34 questions): 18 x 1 (14 MCQ + 4 Assertion-Reason), 6 x 2, 5 x 3, 5 x 5.
Each written section mixes explain/list items (m2, m3, m5) with scenario, case and computed items (m2c, m3c, m5c).

Run: python3 scripts/questions/cbse/g11_entrepreneurship.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g11-entrepreneurship'
MOCK_PATTERN = [(14, 1, 'mcq'), (4, 1, 'ar'), (3, 2, 'm2'), (3, 2, 'm2c'), (2, 3, 'm3'), (3, 3, 'm3c'),
                (2, 5, 'm5'), (3, 5, 'm5c')]


def families():
    fams = {}
    for mod in ('g11_entrepreneurship_a', 'g11_entrepreneurship_b'):
        fams.update(__import__(mod).FAMILIES)
    for fl in fams.values():
        for f in fl:
            if f.gen.__name__ == 'tf_true':
                f.D = 'D1'
    return dict(sorted(fams.items()))


def main(accuracy=None):
    b = Builder(SID, 'scripts/questions/cbse/g11_entrepreneurship.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, accuracy)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return files


ACCURACY = [{
    'date': '2026-11-18',
    'method': '8 random items per chapter (56 items) and one full mock (34 items) re-answered by hand; every computed item in '
              'the sample (EOQ, stock turnover, break-even point, unit cost and margin) re-solved independently; scheme '
              'facts checked against the Startup India, PMMY (MUDRA) and Stand-Up India scheme rules, and IPR terms against '
              'the Patents Act 1970, Copyright Act 1957 and Trade Marks Act 1999',
    'checked': 90,
    'mismatches': 0,
    'fixes': [
        'intrapreneur/entrepreneur/manager scenario pool had three answers and could not form an MCQ; "Investor" added',
        'an Assertion-Reason item (manager is an employee / receives a salary) had a debatable (b) code; replaced by a clear one',
        'case texts no longer use a pronoun bound to the first name for the second person, or {himself}, which ctx() does not fill',
        'a 5-mark case no longer calls a firm named "... Traders" a large food company',
        'tables shared with the class 12 syllabus and the Business Arithmetic generators are copied (not imported) from the '
        'validated class 12 entrepreneurship modules',
    ],
}]

if __name__ == '__main__':
    main(ACCURACY)
