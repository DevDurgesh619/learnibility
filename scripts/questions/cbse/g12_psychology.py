#!/usr/bin/env python3
"""Generate the CBSE class 12 Psychology (037) question bank (cbse-g12-psychology, 758 questions).

Fact tables per subtopic live in g12_psychology_a.py (chapters 1-4) and g12_psychology_b.py (chapters 5-7);
g12_hum_engine.py turns them into question families. Case vignettes (original, short) and curated
'distinguish between' pairs live in g12_psychology_c.py. No textbook passage is reproduced.

Paper pattern (SQP 2026-27, theory 70 marks, 33 questions): Section A 14 × 1 (12 MCQ + 2 Assertion-Reason),
Section B 5 × 2, Section C 4 × 3, Section D 4 × 4, Section E 2 × 6, Section F 4 case-based questions on
two vignettes (2 × 1 + 2 × 2).

Run: python3 scripts/questions/cbse/g12_psychology.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import qbank  # noqa: E402
import g12_hum_engine as E  # noqa: E402

SID = 'cbse-g12-psychology'
MOCK_PATTERN = [(12, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'short'), (4, 3, 'q3'), (4, 4, 'q4'), (2, 6, 'long6'),
                (2, 1, 'case1'), (2, 2, 'case2')]
DEFAULTS = {'long_marks': 6, 'case_marks': (1, 1, 2)}
CUSTOM = {'q3', 'q4', 'long6', 'case1', 'case2'}


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
    for fs in fams.values():
        for f in fs:
            if f.type == 'long' and f.marks == 6:
                f.kinds = tuple(f.kinds) + ('long6',)
            elif f.type == 'explain' and 'case' not in f.kinds and f.marks in (3, 4):
                f.kinds = tuple(f.kinds) + (f'q{f.marks}',)
    return fams


def chapters():
    out = []
    for mod in ('g12_psychology_a', 'g12_psychology_b'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (35 items) plus all written items of mock 2 (19 items) re-solved by hand against '
              'NCERT Psychology class 12; every fact line, vignette and distinguish pair re-checked against the chapters',
    'checked': 54,
    'mismatches': 0,
    'fixes': [
        "source-based items: a variant whose part (ii) asks to explain the same term that answers part (i) is now rejected and regenerated (no_echo guard)",
        "dropped the 'placebo effect' item from healing factors (NCERT frames them as techniques, alliance, catharsis and non-specific patient/therapist factors)",
        "renamed duplicate key terms ('modelling' in ch05 and ch06, 'social identity' in ch02 and ch07) so subject-wide term stems stay distinct",
        "curated 'distinguish between' pairs exclude pairs already written as hand items, avoiding near-duplicate stems",
        'Section F case items use original one-paragraph vignettes (case1: identify, 1 mark; case2: identify and explain, 2 marks) from one shared deck per subtopic so a vignette is never reused',
    ],
}]


def main():
    import g12_psychology_c as X
    qbank._fits = fits
    chs = chapters()
    fams = no_echo(tag(E.families([c for c, _ in chs], [cfg for _, cfg in chs], X.extra(chs))))
    b = qbank.Builder(SID, 'scripts/questions/cbse/g12_psychology.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.5)
    need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
    if set(fams) != need:
        raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = b.build()
    b.write(files, accuracy=ACCURACY or None)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files


if __name__ == '__main__':
    main()
