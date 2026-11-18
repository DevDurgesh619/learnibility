#!/usr/bin/env python3
"""Generate the CBSE class 10 Hindi A (002) question bank (cbse-g10-hindi, 990 questions).

Chapter data: g10_hindi_a.py (क्षितिज-2 काव्य खंड, ch 1-6), g10_hindi_b.py (क्षितिज-2 गद्य खंड ch 7-12, कृतिका-2 ch 13-15).
Engines: g10_hindi_kit.py (literature, writing, अपठित, mock builder), g10_hindi_gram.py (वाक्य भेद, वाच्य, पद परिचय, अलंकार),
g10_hindi_passages.py (original अपठित गद्यांश themes and काव्यांश). Helpers imported from the validated g8_hindi_lib.py.

Mock design = CBSE Hindi A board paper (80 marks, 15 questions):
 क अपठित 14: Q1 गद्यांश 7 (3 MCQ + 2 × 2), Q2 काव्यांश 7 (3 MCQ + 2 × 2)
 ख व्याकरण 16: Q3 वाक्य भेद 4, Q4 वाच्य 4, Q5 पद परिचय 4, Q6 अलंकार 4 (4 × 1 each)
 ग पाठ्यपुस्तक 30: Q7 गद्य extract 5 MCQ, Q8 गद्य 3 × 2, Q9 काव्य extract 5 MCQ, Q10 काव्य 3 × 2, Q11 कृतिका 2 × 4
 घ लेखन 20: Q12 अनुच्छेद 6, Q13 पत्र 5, Q14 स्ववृत्त/ई-मेल 5, Q15 विज्ञापन/संदेश 4

Run: python3 scripts/questions/cbse/g10_hindi.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import F  # noqa: E402
from g10_hindi_kit import (run, extract_set, wr_set, all_wr, all_long, first_lit, gadyansh, kavya_gen, WRITERS)  # noqa: E402
from g10_hindi_gram import mock_gram  # noqa: E402
from g10_hindi_passages import THEMES, POEMS  # noqa: E402
import g10_hindi_a  # noqa: E402
import g10_hindi_b  # noqa: E402

SID = 'cbse-g10-hindi'
CFG = {'w2': '25-30', 'w3': '30-40', 'wl': '50-60', 'ml': 4}

PATTERN = [(1, 7, 'gadyansh7'), (1, 7, 'kavyansh7'),
           (1, 4, 'vakya4'), (1, 4, 'vachya4'), (1, 4, 'pad4'), (1, 4, 'alank4'),
           (1, 5, 'gadya_mcq5'), (1, 6, 'gadya6'), (1, 5, 'kavya_mcq5'), (1, 6, 'kavya6'), (1, 8, 'kritika8'),
           (1, 6, 'anuch6'), (1, 5, 'patra5'), (1, 5, 'svavritt5'), (1, 4, 'vigyapan4')]

WRITE_KIND = {'anuch': ('anuch6', 6), 'patra': ('patra5', 5), 'email': ('svavritt5', 5), 'svavritt': ('svavritt5', 5),
              'vigyapan': ('vigyapan4', 4), 'sandesh': ('vigyapan4', 4)}


def mock_extra(chapters, fams):
    out = {}

    def add(st, f):
        out.setdefault(st, []).append(f)

    for n, ch in chapters.items():
        cid = f'{SID}-ch{n:02d}'
        lst = first_lit(ch, cid)
        poetry, prose, kritika = n <= 6, 7 <= n <= 12, n >= 13
        exs = [e for e in ch.get('extracts', []) if sum(1 for q in e[2] if len(q) > 2 and q[2]) >= 5]
        if poetry:
            exs = [e for e in exs if '\n' in e[1]]
        if exs and (poetry or prose):
            kind = 'kavya_mcq5' if poetry else 'gadya_mcq5'
            add(f'{cid}-st{exs[0][0]}', F('C3', 'D3', 'case', (lambda c, e: lambda r: extract_set(r, c, e, 5, only_mcq=True))(ch, exs),
                                          kinds=(kind,), gap='G7'))
        wr = all_wr(ch, False)
        if poetry or prose:
            add(lst, F('C2', 'D3', 'explain', wr_set(wr, 3, 2, '25-30'), kinds=('kavya6' if poetry else 'gadya6',)))
        if kritika:
            add(lst, F('C4', 'D4', 'long', wr_set(all_long(ch) + [x for st in ch['sts'].values() if st['kind'] == 'lit' for x in st.get('think', [])], 2, 4, '50-60'), kinds=('kritika8',), gap='G5'))
        for k, st in ch['sts'].items():
            sid = f'{cid}-st{k}'
            if st['kind'] == 'gram':
                add(sid, mock_gram(st['engine'], f'{st["engine"]}4'))
            elif st['kind'] == 'write':
                for form, topics, kw in st.get('tasks', []):
                    kind, mk = WRITE_KIND[form]
                    add(sid, F('C4', 'D4', 'long', WRITERS[form](topics, 10, marks=mk), kinds=(kind,), gap='G5'))
            elif st['kind'] == 'apathit':
                add(sid, F('C3', 'D3', 'case', gadyansh(THEMES, 3, 2, 2), kinds=('gadyansh7',), gap='G7'))
                add(sid, F('C3', 'D3', 'case', kavya_gen(POEMS, 2, 2, True), kinds=('kavyansh7',), gap='G7'))
    return out


def main():
    chapters = {**g10_hindi_a.CH, **g10_hindi_b.CH}
    acc = None
    p = os.path.join(HERE, 'g10_hindi_accuracy.json')
    if os.path.exists(p):
        acc = json.load(open(p, encoding='utf-8'))
    run(SID, 'scripts/questions/cbse/g10_hindi.py', chapters, 10, CFG, PATTERN, {}, mock_extra, acc)


if __name__ == '__main__':
    main()
