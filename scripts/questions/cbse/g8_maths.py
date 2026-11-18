#!/usr/bin/env python3
"""Generate the CBSE class 8 maths question bank (cbse-g8-maths, 1,514 questions).

The class 8 maths workbook's 294 questions (M8-001 ... M8-294) are imported unchanged as each
subtopic's student-check path (legacyId kept). The bank is then topped up to 60 per chapter,
and the practice forms and mocks are generated, from the families in g8_maths_*.py.

Run: python3 scripts/questions/cbse/g8_maths.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import openpyxl  # noqa: E402

from qbank import Builder, Seed, ROOT  # noqa: E402

SID = 'cbse-g8-maths'
WORKBOOK = os.path.join(ROOT, 'reference', 'cbse-class8-maths-assessment-v4.xlsx')

TYPE_MAP = {'Worked numerical': 'numerical', 'Explain / reason (1-3 lines)': 'explain',
            'Multi-step problem': 'multi_step', 'Short answer / MCQ': 'short'}
ALR_MAP = {'Practised item (dK)': 'practised', 'Retention probe (R)': 'retention_probe',
           'Transfer probe (TQ)': 'transfer_probe'}

# CBSE paper design used for class 8 (cost sheet): A 20×1 (18 MCQ + 2 A-R), B 5×2, C 6×3, D 4×5, E 3 case×4 = 80 marks.
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (5, 2, 'short'), (6, 3, 'short3'), (4, 5, 'long'), (3, 4, 'case')]


def gap_for(c, d, typ, stem):
    dn = int(d[1])
    if c == 'C1':
        return 'G4' if dn == 1 else 'G1'
    if c == 'C2':
        return 'G2'
    if c == 'C3':
        if dn >= 4:
            return 'G5'
        if typ == 'multi_step' and len(stem.split()) > 25:
            return 'G7'
        return 'G3'
    return 'G5'


def workbook_seeds():
    wb = openpyxl.load_workbook(WORKBOOK, data_only=True)
    plan = wb['Teaching Plan']
    order = {}
    for r in plan.iter_rows(min_row=2, values_only=True):
        if isinstance(r[0], (int, float)) and r[2]:
            order[(int(r[0]), r[2].strip())] = int(r[3])
    seeds = {}
    for r in wb['Assessment'].iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        ch = int(r[1])
        st = order[(ch, r[3].strip())]
        sid = f'{SID}-ch{ch:02d}-st{st}'
        stem, ans = str(r[11]).strip(), str(r[12]).strip()
        typ = TYPE_MAP[r[10]]
        options = None
        m = re.search(r'\s*\(a\)\s*(.+?)\s*\(b\)\s*(.+?)\s*\(c\)\s*(.+?)\s*\(d\)\s*(.+)$', stem)
        key = ans
        if m:
            options = [x.strip() for x in m.groups()]
            stem = stem[:m.start()].strip()
            letter = re.match(r'\(([a-d])\)', ans).group(1)
            answer = options['abcd'.index(letter)]
            typ = 'mcq'
        else:
            answer = ans
        seeds.setdefault(sid, []).append(Seed(
            st=sid, C=r[6], D=r[8], type=typ, stem=stem, answer=answer, key=key,
            marks=float(r[13]) if float(r[13]) % 1 else int(r[13]),
            minutes=float(r[14]) if float(r[14]) % 1 else int(r[14]),
            alr=ALR_MAP[r[15]], gap=gap_for(r[6], r[8], typ, stem), legacy=r[0], options=options))
    return seeds


def families():
    fams = {}
    for mod in ('g8_maths_a', 'g8_maths_b', 'g8_maths_c'):
        try:
            m = __import__(mod)
        except ModuleNotFoundError:
            continue
        fams.update(m.FAMILIES)
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g8_maths.py', families(), MOCK_PATTERN, seeds=workbook_seeds())
    files = b.build()
    b.write(files)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
