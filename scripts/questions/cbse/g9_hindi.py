#!/usr/bin/env python3
"""Generate the CBSE class 9 Hindi (NCERT Ganga) question bank (cbse-g9-hindi, 765 questions).

Chapter data: g9_hindi_a.py (1-6), g9_hindi_b.py (7-12); shared kit g9_g11_hindi_kit.py (reuses g8_hindi_lib.py),
grammar g9_hindi_gram.py (extends g8_hindi_gram.py), रचना tables g9_g11_hindi_rachna.py, original अपठित texts in
g9_hindi_passages.py. No copyrighted textbook passage is reproduced.

Run: python3 scripts/questions/cbse/g9_hindi.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import F  # noqa: E402
from eng_kit_g8_g9_g12 import EngBuilder  # noqa: E402  (Builder with mock-only families)
from g9_g11_hindi_kit import build_families, mcq_set, short_set  # noqa: E402
import g9_hindi_a as A  # noqa: E402
import g9_hindi_b as B  # noqa: E402

SID = 'cbse-g9-hindi'

# CBSE class 9 Hindi design: अपठित 14, व्याकरण 16, पाठ्यपुस्तक 30, लेखन 20 = 80 marks, 15 questions.
MOCK_PATTERN = [
    (2, 7, 'apathit'),    # अपठित गद्यांश / काव्यांश
    (4, 4, 'vyak'),       # व्याकरण, 4 parts × 1
    (2, 5, 'path_ext'),   # पाठ-आधारित बहुविकल्पी (5 × 1)
    (2, 6, 'path6'),      # पाठ्यपुस्तक: 3 × 2 अंक
    (2, 4, 'path4'),      # पाठ्यपुस्तक: 2 × 2 अंक
    (1, 7, 'patra'),      # पत्र
    (1, 7, 'anuch'),      # अनुच्छेद
    (1, 6, 'lekh6'),      # संवाद / सूचना
]


def mock_families(chapters):
    out = {}
    for n, ch in chapters.items():
        facts, ex = [], []
        first = None
        for k, st in ch['sts'].items():
            if st['kind'] != 'lit':
                continue
            first = first or k
            facts += st.get('facts', []) + st.get('infer', [])
            ex += st.get('explain', [])
        if not first:
            continue
        fl = []
        if len(facts) >= 5:
            fl.append(F('C2', 'D2', 'case', mcq_set(ch, facts, 5), kinds=('path_ext',), marks=5, minutes=6))
        if len(ex) >= 3:
            fl.append(F('C2', 'D3', 'explain', short_set(ch, ex, 3, 2), kinds=('path6',), marks=6, minutes=8))
            fl.append(F('C2', 'D3', 'explain', short_set(ch, ex, 2, 2), kinds=('path4',), marks=4, minutes=5))
        out[f'{SID}-ch{n:02d}-st{first}'] = fl
    return out


def main():
    chapters = {**A.CH, **B.CH}
    fams = build_families(chapters, SID, 9)
    b = EngBuilder(SID, 'scripts/questions/cbse/g9_hindi.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.25,
                   mock_families=mock_families(chapters))
    files = b.build()
    acc_path = os.path.join(HERE, 'g9_hindi_accuracy.json')
    acc = json.load(open(acc_path, encoding='utf-8')) if os.path.exists(acc_path) else None
    b.write(files, acc)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
