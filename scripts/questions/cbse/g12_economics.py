#!/usr/bin/env python3
"""Generate the CBSE class 12 Economics (030) question bank (cbse-g12-economics, 1,394 questions).

Fact tables per subtopic live in g12_economics_a.py (Introductory Macroeconomics, chapters 1-6) and
g12_economics_b.py (Indian Economic Development, chapters 7-14); g12_hum_engine.py turns them into
question families. Numerical families (national income, money multiplier, consumption function and
multiplier, deficits, balance of payments, exchange rate) live in g12_economics_c.py with answers
computed in code. No textbook passage is reproduced.

Paper pattern (SQP 2026-27, 80 marks, 34 questions): Section A 20 × 1 (18 MCQ + 2 Assertion-Reason),
4 × 3, 6 × 4 (4 short answers + 2 case/data-based), 4 × 6 long answers.

Run: python3 scripts/questions/cbse/g12_economics.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import qbank  # noqa: E402
import g12_hum_engine as E  # noqa: E402

SID = 'cbse-g12-economics'
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (4, 3, 'q3'), (4, 4, 'q4'), (2, 4, 'case'), (4, 6, 'long6')]
DEFAULTS = {'long_marks': 6, 'case_marks': (1, 1, 2)}
CUSTOM = {'q3', 'q4', 'long6'}


def fits(f, kind):
    if kind in CUSTOM:
        return kind in f.kinds
    return E.strict_fits(f, kind)



def no_echo(fams):
    """Engine source items pick part (i) from a Q line and part (ii) from a T line independently; reject a
    variant whose part (ii) asks to explain the very term that is the answer to part (i), so _fresh retries."""
    for fs in fams.values():
        for f in fs:
            if f.type == 'case' and 'case' in f.kinds:
                def gen(r, g=f.gen):
                    v = g(r)
                    t = re.search(r"\(ii\) Explain the term '([^']+)'", v['stem'])
                    a = re.search(r"^\(i\) (.*?) \(ii\)", v['answer'])
                    if t and a and a.group(1).strip().rstrip('.').lower() == t.group(1).lower():
                        raise ValueError('source item asks the same term twice')
                    return v
                f.gen = gen
    return fams

def tag(fams):
    """Mock kinds by marks: 3-mark and 4-mark written answers, 6-mark long answers."""
    for fs in fams.values():
        for f in fs:
            if f.type == 'long' and f.marks == 6:
                f.kinds = tuple(f.kinds) + ('long6',)
            elif f.type in ('explain', 'numerical', 'multi_step') and 'case' not in f.kinds and DNUM(f) >= 2:
                if f.marks == 3:
                    f.kinds = tuple(f.kinds) + ('q3',)
                elif f.marks == 4:
                    f.kinds = tuple(f.kinds) + ('q4',)
    return fams


def DNUM(f):
    return qbank.DNUM[f.D]


def chapters():
    out = []
    for mod in ('g12_economics_a', 'g12_economics_b'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


def extra():
    import g12_economics_c
    return g12_economics_c.FAMILIES


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (70 items) plus one variant of every numerical family (37) and 8 extra numerical/data '
              'items from the bank, re-solved by hand against NCERT Introductory Macroeconomics and Indian Economic Development; '
              'one full mock reviewed for slot marks',
    'checked': 115,
    'mismatches': 0,
    'fixes': [
        "source-based items: a variant whose part (ii) asks to explain the same term that answers part (i) is now rejected and regenerated (no_echo guard)",
        "China sector item rewritten: services, not industry, now has the largest share of China's GDP; the item asks which sector has a much larger share than in India",
        'ASCII minus in negative data values (e.g. change in stock, NFIA) replaced by the true minus sign in stems and keys',
        'fractional MPC/MPS coefficients printed as (2/3)Y and ÷ (1/6), not 2/3Y',
        'MPS/MPC MCQ distractors rebuilt (one distractor expression could repeat the answer)',
        'exchange-rate key reworded for appreciation; inflationary-gap item now says "reduce government expenditure by ₹x crore"',
        'stock/flow options keep month names capitalised; one causal reason line corrected for grammar',
    ],
}]


def main():
    qbank._fits = fits
    chs = chapters()
    fams = no_echo(tag(E.families([c for c, _ in chs], [cfg for _, cfg in chs], extra())))
    b = qbank.Builder(SID, 'scripts/questions/cbse/g12_economics.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.25)
    have = set(fams)
    need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
    if have != need:
        raise SystemExit(f'subtopics missing: {sorted(need - have)[:5]} extra: {sorted(have - need)[:5]}')
    files = b.build()
    b.write(files, accuracy=ACCURACY or None)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files


if __name__ == '__main__':
    main()
