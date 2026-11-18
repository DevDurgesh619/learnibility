#!/usr/bin/env python3
"""Generate the CBSE class 11 Psychology (037) question bank (cbse-g11-psychology, 739 questions).

Fact tables per subtopic live in g11_psychology_a.py (chapters 1-4) and g11_psychology_b.py (chapters 5-8),
written from NCERT Introduction to Psychology (class 11); g12_hum_engine.py turns them into question families.
Original short case vignettes and curated 'distinguish between' pairs live in g11_psychology_c.py.
No textbook passage is reproduced.

Paper pattern (no CBSE SQP for class 11; the class 12 template is assumed, theory 70 marks, 33 questions):
Section A 14 x 1 (12 MCQ + 2 Assertion-Reason), Section B 5 x 2, Section C 4 x 3, Section D 4 x 4,
Section E 2 x 6, Section F 4 case-based questions on vignettes (2 x 1 + 2 x 2).

Run: python3 scripts/questions/cbse/g11_psychology.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import qbank  # noqa: E402
import g12_hum_engine as E  # noqa: E402

SID = 'cbse-g11-psychology'
MOCK_PATTERN = [(12, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'short'), (4, 3, 'q3'), (4, 4, 'q4'), (2, 6, 'long6'),
                (2, 1, 'case1'), (2, 2, 'case2')]
DEFAULTS = {'long_marks': 6, 'case_marks': (1, 1, 2)}
CUSTOM = {'q3', 'q4', 'long6', 'case1', 'case2'}


def fits(f, kind):
    if kind in CUSTOM:
        return kind in f.kinds
    return E.strict_fits(f, kind)


def no_echo(fams):
    """Reject a source-based variant whose part (ii) asks to explain the term that answers part (i), or whose
    open part (i) is a recall line worded to pick from options the extract item does not show."""
    for fs in fams.values():
        for f in fs:
            if f.type == 'case' and 'case' in f.kinds:
                def gen(r, g=f.gen):
                    v = g(r)
                    t = re.search(r"\(ii\) Explain the term '([^']+)'", v['stem'])
                    a = re.search(r"^\(i\) (.*?) \(ii\)", v['answer'])
                    if t and a and a.group(1).strip().rstrip('.').lower() == t.group(1).lower():
                        raise ValueError('source item asks the same term twice')
                    p1 = re.search(r"\(i\) (.*?) \(1\)", v['stem'])
                    if p1 and re.search(r"Which of (these|the following)|\bNOT\b", p1.group(1)):
                        raise ValueError('open part (i) cannot ask to pick from unseen options')
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
    for mod in ('g11_psychology_a', 'g11_psychology_b'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


def accuracy():
    p = os.path.join(HERE, 'g11_psychology_accuracy.json')
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    import g11_psychology_c as X
    qbank._fits = fits
    chs = chapters()
    fams = no_echo(tag(E.families([c for c, _ in chs], [cfg for _, cfg in chs], X.extra(chs))))
    b = qbank.Builder(SID, 'scripts/questions/cbse/g11_psychology.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.5)
    lim = int(os.environ.get('QB_LIMIT', '0'))
    if lim:
        b.cur['chapters'] = b.cur['chapters'][:lim]
        b.t = dict(b.t, chapters=lim)
    else:
        need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
        if set(fams) != need:
            raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = b.build()
    b.write(files, accuracy=accuracy())
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files


if __name__ == '__main__':
    main()
