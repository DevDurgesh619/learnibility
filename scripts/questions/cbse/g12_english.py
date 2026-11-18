#!/usr/bin/env python3
"""Generate the CBSE class 12 English Core (301) question bank (cbse-g12-english, NCERT Flamingo + Vistas).

Chapter data: g12_english_a.py (Flamingo ch 1-10, reading passages), g12_english_b.py (Flamingo poems ch 11-13, Vistas ch 14-19).
Engines: eng_kit_g8_g9_g12.py (literature, vocabulary, writing, reading, mocks).
Mock design (CBSE board paper, 80 marks, 13 questions):
Reading 22 = passage 12 + case-based data passage 10; Writing 18 = notice 4 + invitation/reply 4 + letter 5 + article/report 5;
Literature 40 = poetry extract 6 + prose extract 4 + Vistas extract 6 + Flamingo short answers 5 x 2 + Vistas short answers 2 x 2
+ Flamingo long answer 5 + Vistas long answer 5.

Run: python3 scripts/questions/cbse/g12_english.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import F  # noqa: E402
from eng_kit_g8_g9_g12 import run, writing_item, passage_set, data_case, mock_extract, mock_short_set, mock_long, first_st  # noqa: E402
import g12_english_a  # noqa: E402
import g12_english_b  # noqa: E402

SID = 'cbse-g12-english'
GRADE = 12

PATTERN_G12 = [(1, 12, 'read12'), (1, 10, 'read10'), (1, 4, 'notice4'), (1, 4, 'invite4'), (1, 5, 'letter5'), (1, 5, 'artrep5'),
               (1, 6, 'poem6'), (1, 4, 'prose4'), (1, 6, 'vistas6'), (1, 10, 'short10'), (1, 4, 'short4'), (1, 5, 'longF'), (1, 5, 'longV')]

WRITING_KINDS = {'notice': 'notice4', 'formal_invitation': 'invite4', 'reply': 'invite4', 'letter': 'letter5', 'editor': 'letter5',
                 'job': 'letter5', 'article': 'artrep5', 'report': 'artrep5'}
MARKS = {'notice4': 4, 'invite4': 4, 'letter5': 5, 'artrep5': 5}

FLAMINGO = range(1, 14)
PROSE = range(1, 9)
POEMS = range(9, 14)
VISTAS = range(14, 20)


def mock_extra_g12(sid, grade, passages):
    def extra(chapters, fams):
        out = {}
        for n, ch in chapters.items():
            cid = f'{sid}-ch{n:02d}'
            for k, st in ch['sts'].items():
                if st['kind'] == 'read':
                    stid = f'{cid}-st{k}'
                    ps = passages.get(n, [])
                    if ps:
                        out.setdefault(stid, []).append(F('C3', 'D3', 'case', (lambda ps_: lambda r: passage_set(r, ps_, 12))(ps), kinds=('read12',), gap='G7'))
                    out.setdefault(stid, []).append(F('C3', 'D3', 'case', lambda r: data_case(r, grade, 10), kinds=('read10',), gap='G7'))
            wst = next((f'{cid}-st{k}' for k, st in ch['sts'].items() if st['kind'] == 'write'), first_st(ch, cid))
            prompts = [p[:3] for p in ch.get('writing', [])]
            for st in ch['sts'].values():
                prompts += [p[:3] for p in st.get('prompts', [])]
            groups = {}
            for p in prompts:
                kind = WRITING_KINDS.get(p[0])
                if kind:
                    groups.setdefault(kind, []).append(p)
            for kind, ps in groups.items():
                out.setdefault(wst, []).append(F('C4', 'D4', 'long', (lambda ps_, m: lambda r: writing_item(r, grade, *r.choice(ps_), marks=m))(ps, MARKS[kind]),
                                                 kinds=(kind,), gap='G5'))
            lst = first_st(ch, cid)
            exs = ch.get('extracts', [])
            if exs:
                est = f'{cid}-st{exs[0][0]}'
                if n in POEMS:
                    out.setdefault(est, []).extend(mock_extract(ch, 6, 'poem6'))
                elif n in PROSE:
                    out.setdefault(est, []).extend(mock_extract(ch, 4, 'prose4'))
                else:
                    out.setdefault(est, []).extend(mock_extract(ch, 6, 'vistas6'))
            if n in FLAMINGO:
                out.setdefault(lst, []).extend(mock_short_set(ch, grade, 5, 'short10'))
                out.setdefault(lst, []).extend(mock_long(ch, grade, 'longF', 5))
            else:
                out.setdefault(lst, []).extend(mock_short_set(ch, grade, 2, 'short4'))
                out.setdefault(lst, []).extend(mock_long(ch, grade, 'longV', 5))
        return out
    return extra


def main():
    chapters = {**g12_english_a.CH, **g12_english_b.CH}
    acc = None
    p = os.path.join(HERE, 'g12_english_accuracy.json')
    if os.path.exists(p):
        acc = json.load(open(p, encoding='utf-8'))
    run(SID, 'scripts/questions/cbse/g12_english.py', GRADE, chapters, PATTERN_G12, g12_english_a.PASSAGES,
        mock_extra_g12(SID, GRADE, g12_english_a.PASSAGES), acc)


if __name__ == '__main__':
    main()
