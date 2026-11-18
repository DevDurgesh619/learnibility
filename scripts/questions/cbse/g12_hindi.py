#!/usr/bin/env python3
"""Generate the CBSE class 12 Hindi Core (302) question bank (cbse-g12-hindi, 1152 questions).

Chapter data: g12_hindi_a.py (आरोह-2 काव्य खंड ch 1-6), g12_hindi_b.py (काव्य ch 7-9, गद्य ch 10-12), g12_hindi_c.py
(गद्य ch 13-15, वितान-2 ch 16-18). अभिव्यक्ति और माध्यम subtopics sit in ch 4, 10, 11, 12, 15, 16, 17; अपठित in ch 18.
Engine: g10_hindi_kit.py (shared with cbse-g10-hindi); original अपठित passages in g12_hindi_passages.py.

Mock design (assumption from the CBSE SQP structure, 80 marks, 12 questions):
 क अपठित 18: Q1 गद्यांश 10 (3 MCQ + शीर्षक + 3 × 2), Q2 काव्यांश 8 (3 MCQ + शीर्षक + 2 × 2)
 ख अभिव्यक्ति और माध्यम 22: Q3 रचनात्मक लेखन / संस्मरण 6, Q4 नाट्य-रूपांतरण, कविता-कहानी, जनसंचार 2 × 4,
   Q5 विशेष लेखन / पत्रकारीय लेखन 2 × 4
 ग आरोह/वितान 40: Q6 काव्यांश 5 MCQ, Q7 गद्यांश 5 MCQ, Q8 काव्य 2 × 3, Q9 काव्य 2 × 2, Q10 गद्य 2 × 3, Q11 गद्य 2 × 2,
   Q12 वितान 2 × 5

Run: python3 scripts/questions/cbse/g12_hindi.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import F  # noqa: E402
from g8_hindi_lib import ROMAN  # noqa: E402
from g10_hindi_kit import (run, extract_set, wr_set, all_wr, all_long, first_lit, gadyansh, kavya_gen)  # noqa: E402
from g12_hindi_passages import THEMES, POEMS  # noqa: E402
import g12_hindi_a  # noqa: E402
import g12_hindi_b  # noqa: E402
import g12_hindi_c  # noqa: E402

SID = 'cbse-g12-hindi'
CFG = {'w2': '30-40', 'w3': '50-60', 'wl': '80-100', 'ml': 5}

PATTERN = [(1, 10, 'gad10'), (1, 8, 'kav8'),
           (1, 6, 'rachna6'), (1, 8, 'abhi8'), (1, 8, 'patrakar8'),
           (1, 5, 'kavya_mcq5'), (1, 5, 'gadya_mcq5'), (1, 6, 'kavya6'), (1, 4, 'kavya4'), (1, 6, 'gadya6'), (1, 4, 'gadya4'),
           (1, 10, 'vitan10')]

def rachna_choice(topics, form):
    """Board-style internal choice: three topics, write on any one (6 marks)."""
    def g(r):
        pick = r.sample(topics, 3)
        if form == 'rachna':
            head = 'निम्नलिखित दिए गए तीन अप्रत्याशित विषयों में से किसी एक विषय पर लगभग 120 शब्दों में रचनात्मक लेख लिखिए।'
            lines = [f'({ROMAN[i]}) {t}' for i, t in enumerate(pick)]
            ans = 'आकर्षक आरंभ, विषय के विविध पक्षों पर मौलिक विचार, अनुभव या उदाहरण, सुसंगत क्रम और प्रभावी निष्कर्ष।'
        else:
            head = 'निम्नलिखित में से किसी एक विषय पर लगभग 120 शब्दों में संस्मरण या रेखाचित्र (जैसा निर्दिष्ट है) लिखिए।'
            lines = [f'({ROMAN[i]}) {f}: {t}' for i, (f, t) in enumerate(pick)]
            ans = 'संस्मरण—स्मृति-आधारित, आत्मीय "मैं" शैली, प्रसंग और अनुभूतियाँ; रेखाचित्र—व्यक्ति/दृश्य का शब्द-चित्र, रूप, स्वभाव और आदतों की रेखाएँ।'
        return {'stem': '\n'.join([head] + lines), 'answer': ans,
                'key': 'अंक-विभाजन (6): आरंभ और प्रस्तुति 1, विषय-वस्तु और मौलिकता 3, भाषा-शुद्धता 1, निष्कर्ष 1।', 'marks': 6, 'minutes': 12, 'gap': 'G5'}
    return g


THEORY_KIND = {4: 'abhi8', 16: 'abhi8', 17: 'abhi8', 11: 'patrakar8', 12: 'patrakar8', 10: 'abhi8', 15: 'abhi8'}


def mock_extra(chapters, fams):
    out = {}

    def add(st, f):
        out.setdefault(st, []).append(f)

    for n, ch in chapters.items():
        cid = f'{SID}-ch{n:02d}'
        lst = first_lit(ch, cid)
        poetry, prose, vitan = n <= 9, 10 <= n <= 15, n >= 16
        exs = [e for e in ch.get('extracts', []) if sum(1 for q in e[2] if len(q) > 2 and q[2]) >= 5]
        exs = [e for e in exs if ('\n' in e[1]) == poetry]
        if exs and (poetry or prose):
            kind = 'kavya_mcq5' if poetry else 'gadya_mcq5'
            add(f'{cid}-st{exs[0][0]}', F('C3', 'D3', 'case', (lambda c, e: lambda r: extract_set(r, c, e, 5, only_mcq=True))(ch, exs),
                                          kinds=(kind,), gap='G7'))
        if poetry or prose:
            pre = 'kavya' if poetry else 'gadya'
            add(lst, F('C3', 'D3', 'explain', wr_set(all_wr(ch, True), 2, 3, '50-60'), kinds=(f'{pre}6',)))
            add(lst, F('C2', 'D2', 'explain', wr_set(all_wr(ch, False), 2, 2, '30-40'), kinds=(f'{pre}4',)))
        if vitan:
            pool = all_long(ch) + [x for st in ch['sts'].values() if st['kind'] == 'lit' for x in st.get('think', [])]
            add(lst, F('C4', 'D4', 'long', wr_set(pool, 2, 5, '80-100'), kinds=('vitan10',), gap='G5'))
        for k, st in ch['sts'].items():
            sid = f'{cid}-st{k}'
            if st['kind'] == 'write':
                if st.get('theory'):
                    add(sid, F('C3', 'D3', 'explain', wr_set(st['theory'], 2, 4, '60'), kinds=(THEORY_KIND[n],)))
                for form, topics, kw in st.get('tasks', []):
                    if form in ('rachna', 'sansmaran'):
                        add(sid, F('C4', 'D4', 'long', rachna_choice(topics, form), kinds=('rachna6',), gap='G5'))
            elif st['kind'] == 'apathit':
                add(sid, F('C3', 'D3', 'case', gadyansh(THEMES, 4, 3, 2), kinds=('gad10',), gap='G7'))
                add(sid, F('C3', 'D3', 'case', kavya_gen(POEMS, 3, 2, True), kinds=('kav8',), gap='G7'))
    return out


def main():
    chapters = {**g12_hindi_a.CH, **g12_hindi_b.CH, **g12_hindi_c.CH}
    acc = None
    p = os.path.join(HERE, 'g12_hindi_accuracy.json')
    if os.path.exists(p):
        acc = json.load(open(p, encoding='utf-8'))
    run(SID, 'scripts/questions/cbse/g12_hindi.py', chapters, 12, CFG, PATTERN, {}, mock_extra, acc)


if __name__ == '__main__':
    main()
