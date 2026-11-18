#!/usr/bin/env python3
"""Generate the CBSE class 12 accountancy question bank (cbse-g12-accountancy, 1004 questions).

NCERT Accountancy XII Part I and II (055), Part B option: Financial Statement Analysis.
Families per subtopic: g12_accountancy_a.py (ch01-04 partnership), g12_accountancy_b.py (ch05-06 shares and
debentures), g12_accountancy_c.py (ch07-10 company statements, analysis, ratios, cash flow). Theory fact tables use
g11_accountancy_kit.facts(); problems are computed with exact fractions.

Mocks follow the CBSE paper: Part A (ch01-06) Q1-16 1 mark (14 MCQ + 2 Assertion-Reason), 4 x 3, 2 x 4, 4 x 6;
Part B (ch07-10) 4 x 1 (3 MCQ + 1 A-R), 2 x 3, 1 x 4, 1 x 6 = 34 questions, 80 marks.
4- and 6-mark slots take only computed practical problems (theory lists and case items stay in the bank and forms).

Run: python3 scripts/questions/cbse/g12_accountancy.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g12-accountancy'
PART_A = {f'{SID}-ch0{i}' for i in range(1, 7)}

MOCK_PATTERN = [(14, 1, 'A1'), (2, 1, 'Aar'), (4, 3, 'A3'), (2, 4, 'A4'), (4, 6, 'A6'),
                (3, 1, 'B1'), (1, 1, 'Bar'), (2, 3, 'B3'), (1, 4, 'B4'), (1, 6, 'B6')]


def families():
    fams = {}
    for mod in ('g12_accountancy_a', 'g12_accountancy_b', 'g12_accountancy_c'):
        fams.update(__import__(mod).FAMILIES)
    for st, fl in fams.items():
        part = 'A' if st.rsplit('-st', 1)[0] in PART_A else 'B'
        for f in fl:
            theory = f.gen.__qualname__.startswith('facts.')
            k = set(f.kinds)
            add = set()
            if f.type == 'mcq' and 'ar' not in k:
                add.add(part + '1')
            if 'ar' in k:
                add.add(part + 'ar')
            if 'm3' in k:
                add.add(part + '3')
            if 'm4' in k and not theory:
                add.add(part + '4')
            if 'm6' in k and not theory:
                add.add(part + '6')
            f.kinds = tuple(sorted(k | add))
    return fams


def main(accuracy=None):
    b = Builder(SID, 'scripts/questions/cbse/g12_accountancy.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, accuracy)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return files


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random items per chapter re-solved by hand (50 mixed items), then 2 numerical/journal/long items per chapter (20 items: '
              'appropriation with insufficient profit, revaluation, retirement dues, dissolution with realisation and bank, pro-rata allotment, '
              'debenture issue and write-off, ratios, full cash flow statement)',
    'checked': 70,
    'mismatches': 0,
    'fixes': [
        'cash flow statement problem could list profit on sale of investments without the matching investing inflow; the full statement now derives profit or loss on machinery and interest from the investing and financing data only',
        'share capital note answer reworded into subscribed-and-fully-paid and subscribed-but-not-fully-paid lines (NCERT format)',
        'reserves-and-surplus key mentioned a debit balance even when the balance was a credit; note now only when it applies',
        'interest-on-drawings key showed the period as 13/2 months; now 6.5 months',
        'share counts used western grouping (121,000); now Indian grouping (1,21,000)',
        'case pronoun did not always agree with the partner named; reworded',
        'paid-up capital and vendor/debenture MCQs could fail to find three distinct distractors; distractor sets rebuilt',
        '4- and 6-mark mock slots restricted to computed practical problems; Part A (ch01-06) and Part B (ch07-10) sections kept separate'],
}]

if __name__ == '__main__':
    main(ACCURACY)
