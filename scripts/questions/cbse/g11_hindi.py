#!/usr/bin/env python3
"""Generate the CBSE class 11 Hindi Core (NCERT आरोह भाग-1 + वितान भाग-1) question bank (cbse-g11-hindi, 1176 questions).

Chapter data: g11_hindi_a.py (गद्य 1-6), g11_hindi_b.py (7-13), g11_hindi_c.py (14-19, incl. वितान and अपठित);
shared kit g9_g11_hindi_kit.py (reuses g8_hindi_lib.py), रचना tables g9_g11_hindi_rachna.py, original अपठित texts
in g11_hindi_passages.py. No copyrighted textbook passage is reproduced: prose extracts are original retellings,
modern poems are paraphrased, only public-domain verse (कबीर, मीरा) is quoted.

Run: python3 scripts/questions/cbse/g11_hindi.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import F  # noqa: E402
from eng_kit_g8_g9_g12 import EngBuilder  # noqa: E402  (Builder with mock-only families)
from g8_hindi_lib import ROMAN  # noqa: E402
from g9_g11_hindi_kit import build_families, mcq_set, short_set, extract_set, need, passage, kavya  # noqa: E402
import g9_g11_hindi_rachna as rc  # noqa: E402
from g11_hindi_passages import THEMES, KAVYA  # noqa: E402
import g11_hindi_a as A  # noqa: E402
import g11_hindi_b as B  # noqa: E402
import g11_hindi_c as C  # noqa: E402

SID = 'cbse-g11-hindi'

# CBSE class 11 Hindi Core design: अपठित 18, अभिव्यक्ति और माध्यम + रचनात्मक लेखन 22, आरोह 30, वितान 10 = 80 marks.
MOCK_PATTERN = [
    (1, 10, 'gad10'),     # अपठित गद्यांश
    (1, 8, 'kav8'),       # अपठित काव्यांश
    (1, 6, 'rach6'),      # रचनात्मक लेखन (निबंध/अनुच्छेद)
    (1, 5, 'patra5'),     # औपचारिक पत्र
    (1, 6, 'media6'),     # जनसंचार/समाचार: 3 × 2 अंक
    (1, 5, 'lekh5'),      # समाचार/भाषण/पटकथा/फ़ीचर लेखन
    (1, 5, 'kext5'),      # काव्य-खंड: पठित काव्यांश, 5 बहुविकल्पी
    (1, 5, 'gext5'),      # गद्य-खंड: पठित गद्यांश, 5 बहुविकल्पी
    (1, 6, 'kav6s'),      # काव्य-खंड: 3 × 2 अंक
    (1, 6, 'gad6s'),      # गद्य-खंड: 3 × 2 अंक
    (1, 10, 'vitan10'),   # वितान: 2 × 5 अंक
    (1, 8, 'long8'),      # आरोह: 2 × 4 अंक
]

PROSE = range(1, 9)
POEMS = range(9, 17)
VITAN = range(17, 20)


def table_set(tab, k, each, words='25-30'):
    """k written parts from a non-literature table (explain + think)."""
    pairs = tab['explain'] + tab.get('think', [])

    def g(r):
        need(len(pairs) >= k)
        pick = r.sample(pairs, k)
        lines, ans = [f'"{tab["ref"]}" से संबंधित निम्नलिखित प्रश्नों के उत्तर लगभग {words} शब्दों में लिखिए।'], []
        for i, (q, a) in enumerate(pick):
            lines.append(f'({ROMAN[i]}) {q}')
            ans.append(f'({ROMAN[i]}) {a}')
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans),
                'key': f'प्रत्येक भाग {each} अंक (कुल {k * each} अंक): विषय-वस्तु {each - 1}, भाषा 1। ' + ' '.join(ans),
                'marks': k * each}
    return g


def mock_families(chapters):
    out = {}
    for n, ch in chapters.items():
        facts, ex, deep = [], [], []
        first = None
        for k, st in ch['sts'].items():
            if st['kind'] != 'lit':
                continue
            first = first or k
            facts += st.get('facts', []) + st.get('infer', [])
            ex += st.get('explain', [])
            deep += st.get('long', []) + st.get('think', [])
        if not first:
            continue
        fl = []
        exs5 = [e for e in ch.get('extracts', []) if sum(1 for q in e[2] if len(q) > 2 and q[2]) >= 5]
        if n in PROSE or n in POEMS:
            kind = 'gext5' if n in PROSE else 'kext5'
            if exs5:
                fl.append(F('C3', 'D3', 'case', extract_set(ch, exs5, 5, True), kinds=(kind,), marks=5, minutes=7))
            elif len(facts) >= 5:
                fl.append(F('C2', 'D2', 'case', mcq_set(ch, facts, 5), kinds=(kind,), marks=5, minutes=6))
            if len(ex) >= 3:
                fl.append(F('C2', 'D3', 'explain', short_set(ch, ex, 3, 2),
                            kinds=('gad6s' if n in PROSE else 'kav6s',), marks=6, minutes=8))
            if len(deep) >= 2:
                fl.append(F('C4', 'D4', 'long', short_set(ch, deep, 2, 4, '60-70'), kinds=('long8',), marks=8, minutes=12))
        else:
            pool = deep + ex
            if len(pool) >= 2:
                fl.append(F('C4', 'D4', 'long', short_set(ch, pool, 2, 5, '60-70'), kinds=('vitan10',), marks=10, minutes=14))
        out[f'{SID}-ch{n:02d}-st{first}'] = fl
    # जनसंचार/समाचार 3 × 2 sets on the media subtopics
    out.setdefault(f'{SID}-ch01-st4', []).append(
        F('C2', 'D3', 'explain', table_set(rc.MEDIA, 3, 2), kinds=('media6',), marks=6, minutes=8))
    out.setdefault(f'{SID}-ch02-st3', []).append(
        F('C2', 'D3', 'explain', table_set(rc.SAMACHAR, 3, 2), kinds=('media6',), marks=6, minutes=8))
    # further अपठित gad10/kav8 variants on the अपठित subtopic
    out.setdefault(f'{SID}-ch19-st4', []).extend([
        F('C3', 'D3', 'case', passage(THEMES[2], 4, (2, 3)), kinds=('gad10',), marks=10, minutes=13),
        F('C3', 'D4', 'case', passage(THEMES[3], 4, (2, 3)), kinds=('gad10',), marks=10, minutes=13),
        F('C3', 'D3', 'case', kavya(KAVYA[1:], 3, (2, 2)), kinds=('kav8',), marks=8, minutes=11),
    ])
    return out


def main():
    chapters = {**A.CH, **B.CH, **C.CH}
    assert sorted(chapters) == list(range(1, 20)), sorted(chapters)
    fams = build_families(chapters, SID, 11)
    b = EngBuilder(SID, 'scripts/questions/cbse/g11_hindi.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.25,
                   mock_families=mock_families(chapters))
    files = b.build()
    acc_path = os.path.join(HERE, 'g11_hindi_accuracy.json')
    acc = json.load(open(acc_path, encoding='utf-8')) if os.path.exists(acc_path) else None
    b.write(files, acc)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
