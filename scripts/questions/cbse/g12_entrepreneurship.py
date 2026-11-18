#!/usr/bin/env python3
"""Generate the CBSE class 12 entrepreneurship question bank (cbse-g12-entrepreneurship, 684 questions).

CBSE Entrepreneurship XII (066), 6 units. Theory fact tables (units 1-4, unit 6 st2-st4) are in
g12_entrepreneurship_a.py; Business Arithmetic (unit 5) and capital requirement (unit 6 st1) are computed in
g12_entrepreneurship_b.py. `efacts()` adapts g11_accountancy_kit.facts() to the 1/2/3/5-mark paper.

Mock pattern (CBSE SQP, theory 70 marks, 34 questions): 18 x 1 (14 MCQ + 4 Assertion-Reason), 6 x 2, 5 x 3, 5 x 5.

Run: python3 scripts/questions/cbse/g12_entrepreneurship.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g12-entrepreneurship'

# Each written section mixes explain/list items (m2, m3, m5) with scenario, case and computed items (m2c, m3c, m5c).
MOCK_PATTERN = [(14, 1, 'mcq'), (4, 1, 'ar'), (3, 2, 'm2'), (3, 2, 'm2c'), (2, 3, 'm3'), (3, 3, 'm3c'),
                (2, 5, 'm5'), (3, 5, 'm5c')]


def families():
    fams = {}
    for mod in ('g12_entrepreneurship_a', 'g12_entrepreneurship_b'):
        fams.update(__import__(mod).FAMILIES)
    for fl in fams.values():
        for f in fl:
            if f.gen.__name__ == 'tf_true':
                f.D = 'D1'
    return dict(sorted(fams.items()))


def main(accuracy=None):
    b = Builder(SID, 'scripts/questions/cbse/g12_entrepreneurship.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, accuracy)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return files


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random items per chapter re-answered by hand (30 items), one output of each of the 20 computed generators re-solved '
              'independently (unit cost and margin, BEP, margin of safety, target-profit units, EOQ, FIFO closing stock, stock turnover, '
              'current and debt-equity ratios, ROE/ROI, income statement, three-month cash projection, project cost and means of finance), '
              'then 12 more case, assertion-reason and statement items',
    'checked': 62,
    'mismatches': 0,
    'fixes': [
        'fact-table cases were written with all sub-questions in one segment; split into question/answer pairs so each part is marked',
        'franchising-type scenarios had only three options and could not form an MCQ; a fourth plausible option (joint venture) added',
        'an assertion-reason item on raising unit price had a debatable code; rewritten as a clear (d) item',
        'SWOT scenario question and the 2-mark "explain one point" stem reworded to read as questions',
        'bakery comparison (5 marks) asked an opinion question; now asks which product earns more per unit and in total, and why',
        'break-even problem raised fixed costs by odd amounts; the rise is now a round multiple of the contribution',
        'ratio answers shown as x:1 with decimals (1.25:1), as in CBSE marking schemes',
        'mock sections split so each written section mixes explain/list items with scenario, case and computed items'],
}]

if __name__ == '__main__':
    main(ACCURACY)
