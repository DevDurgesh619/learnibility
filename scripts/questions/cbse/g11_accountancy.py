#!/usr/bin/env python3
"""Generate the CBSE class 11 accountancy question bank (cbse-g11-accountancy, 822 questions).

NCERT Financial Accounting Part I and II (055). Families per subtopic are in g11_accountancy_a.py
(ch01-02 theory), g11_accountancy_b.py (journal, ledger, cash book, special books, from a computed
transaction library), g11_accountancy_c.py (BRS, trial balance and rectification, depreciation) and
g11_accountancy_d.py (financial statements with adjustments). Shared fact-table helpers are in
g11_accountancy_kit.py (also used by cbse-g11-business).

Run: python3 scripts/questions/cbse/g11_accountancy.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder  # noqa: E402

SID = 'cbse-g11-accountancy'

# Class XI follows the Class XII accountancy design (cost sheet): 34 questions, 80 marks, 3 h.
# Section A 20 x 1 (16 MCQ + 4 Assertion-Reason), 6 x 3, 3 x 4, 5 x 6.
MOCK_PATTERN = [(16, 1, 'mcq'), (4, 1, 'ar'), (6, 3, 'm3'), (3, 4, 'm4'), (5, 6, 'm6')]


def families():
    fams = {}
    for mod in ('g11_accountancy_a', 'g11_accountancy_b', 'g11_accountancy_c', 'g11_accountancy_d'):
        fams.update(__import__(mod).FAMILIES)
    # 6-mark accountancy questions should be practical problems: theory lists and six-basis distinctions
    # stay in the bank and forms but are not used for the 6-mark mock section.
    for fl in fams.values():
        for f in fl:
            if f.gen.__name__ in ('long_', 'pair6'):
                f.kinds = tuple(k for k in f.kinds if k != 'm6')
    return fams


def main(accuracy=None):
    b = Builder(SID, 'scripts/questions/cbse/g11_accountancy.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, accuracy)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return files


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random items per chapter re-solved by hand (two rounds: 45 mixed items, then 45 numerical items incl. BRS with overdraft, '
              'rectification with suspense, WDV disposal, full final accounts with six adjustments)',
    'checked': 90,
    'mismatches': 0,
    'fixes': [
        'accounting-equation sequences could pay a creditor or debtor that did not exist (negative liabilities); now start with capital and a goods purchase and exclude settlements',
        'equation item could sell more goods than were bought; cost of goods sold now capped by purchases',
        '"true of X but not of Y" MCQs gave bare fragments as options; each option now names its basis',
        'rectification items used one amount for every error in a question; each error now has its own amount',
        'cash book and book-identification items could repeat the same transaction type; transaction types are now sampled without repeats',
        'BRS marking key wording for overdraft starts (add/less reversed relative to a favourable balance) corrected',
        'pronouns in scenarios now agree with the randomly chosen name',
        'amend-cash-book MCQ showed a truncated correct option; options rewritten as parallel short phrases',
        '6-mark mock slots restricted to practical problems (theory lists remain in bank and forms)'],
}]

if __name__ == '__main__':
    main(ACCURACY)
