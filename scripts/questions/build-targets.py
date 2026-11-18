#!/usr/bin/env python3
"""Build data/questions/targets.json from the assessment cost sheet.

One record per counted subject (rows marked Y on the sheet): how many mastery-bank
questions per chapter, how many questions per practice form, how many mocks and how
many questions per mock, plus the subject total. The shared validator
(scripts/questions/validate.ts) checks every subject's files against these numbers.

Run: python3 scripts/questions/build-targets.py
"""
import json
import os
import re
import sys

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEET = os.path.join(ROOT, 'reference', 'assessment-cost-gr8-12.xlsx')
OUT = os.path.join(ROOT, 'data', 'questions', 'targets.json')

TABS = {
    'CBSE 8th  to 10th': 'cbse',
    'Cbse 11th -12th ': 'cbse',
    'IGCSE 8th-10th ': 'cambridge',
    'IGCSE 11th and 12th ': 'cambridge',
    'IB - 8th to 10th ': 'ib',
    'IB 11th and 12th ': 'ib',
}

# Sheet subject name (lowercased, trimmed) -> W2 subject slug.
SLUGS = [
    (r'^maths - stats', 'applied-maths'),
    (r'^maths – advanced', 'maths-advanced'),
    (r'^science – advanced', 'science-advanced'),
    (r'^maths', 'maths'),
    (r'^social science – history', 'history'),
    (r'^social science – geography', 'geography'),
    (r'^social science', 'social-science'),
    (r'^science', 'science'),
    (r'^english', 'english'),
    (r'^hindi \(course b\)', 'hindi-b'),
    (r'^hindi', 'hindi'),
    (r'^physics', 'physics'),
    (r'^chemistry', 'chemistry'),
    (r'^bio', 'biology'),
    (r'^eco', 'economics'),
    (r'^comp science', 'computer-science'),
    (r'^psychology', 'psychology'),
    (r'^envio?rmental', 'environmental'),
    (r'^accounts', 'accountancy'),
    (r'^bussiness|^business', 'business'),
    (r'^ip and', 'informatics'),
    (r'^legal', 'legal-studies'),
    (r'^enterpre', 'entrepreneurship'),
    (r'^history', 'history'),
    (r'^pol science', 'political-science'),
    (r'^geography', 'geography'),
    (r'^sociology', 'sociology'),
    (r'^management behav', 'management-behaviour'),
]

EXPECTED = {'cbse': 63582, 'cambridge': 62540, 'ib': 53893}


def slug_for(name: str) -> str:
    n = name.strip().lower()
    for pat, slug in SLUGS:
        if re.search(pat, n):
            return slug
    raise SystemExit(f'No slug for sheet subject "{name}"')


def main() -> None:
    wb = openpyxl.load_workbook(SHEET, data_only=True)
    items = []
    seen = set()
    for tab, board in TABS.items():
        ws = wb[tab]
        for r in ws.iter_rows(min_row=2, values_only=True):
            if not isinstance(r[0], int):
                continue
            if str(r[16]).strip().upper() != 'Y':
                continue
            grade = int(re.match(r'\d+', str(r[1])).group())
            stream = (r[2] or 'none').strip().lower() if grade >= 11 else 'none'
            slug = slug_for(str(r[3]))
            sid = f'{board}-g{grade}-{slug}'
            if sid in seen:
                raise SystemExit(f'Duplicate counted subject {sid}')
            seen.add(sid)
            chapters, per_ch, forms, per_form, mocks, per_mock, total = (
                int(r[5]), int(r[7]), int(r[9]), int(r[10]), int(r[12]), int(r[13]), int(r[15]))
            if chapters * per_ch + forms * per_form + mocks * per_mock != total:
                raise SystemExit(f'{sid}: sheet arithmetic does not add up')
            if forms != 2 * chapters:
                raise SystemExit(f'{sid}: expected 2 practice forms per chapter')
            items.append({
                'subjectId': sid,
                'board': board,
                'grade': grade,
                'stream': stream,
                'sheetName': str(r[3]).strip(),
                'programme': str(r[4]).strip(),
                'chapters': chapters,
                'bankPerChapter': per_ch,
                'questionsPerForm': per_form,
                'mocks': mocks,
                'questionsPerMock': per_mock,
                'total': total,
                'examPattern': str(r[19] or '').strip(),
                'chapterMix': str(r[20] or '').strip(),
            })
    for board, want in EXPECTED.items():
        got = sum(i['total'] for i in items if i['board'] == board)
        if got != want:
            raise SystemExit(f'{board}: totals {got} != cost sheet {want}')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({'schemaVersion': 1, 'generatedBy': 'scripts/questions/build-targets.py', 'items': items},
                  f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'{len(items)} subjects, {sum(i["total"] for i in items)} questions -> {os.path.relpath(OUT, ROOT)}')


if __name__ == '__main__':
    sys.exit(main())
