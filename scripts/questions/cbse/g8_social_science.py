#!/usr/bin/env python3
"""Generate the CBSE class 8 social science question bank (cbse-g8-social-science, 1,314 questions).

Fact tables per subtopic live in g8_social_science_a.py (ch01-05), _b.py (ch06-10) and _c.py (ch11-15);
g8_social_science_kit.py turns them into qbank families (terms, fill-ins, true/false, assertion-reason,
chronology, matching, scenario MCQs, explain items, source/cloze cases, long answers, map items).

Run: python3 scripts/questions/cbse/g8_social_science.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder, CUR_DIR  # noqa: E402
import g8_social_science_kit as kit  # noqa: E402

SID = 'cbse-g8-social-science'
GRADE = 8
MODULES = ('g8_social_science_a', 'g8_social_science_b', 'g8_social_science_c')

# Class X SS paper design used for the school exam (cost sheet): 38 questions, 80 marks.
# A 20 x 1 (18 MCQ + 2 Assertion-Reason), B 4 x 2, C 5 x 3, D 4 x 5, E 3 case/source x 4, F map 2 + 3.
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (4, 2, 'sa2'), (5, 3, 'sa3'), (4, 5, 'la5'), (3, 4, 'case'),
                (1, 2, 'map2'), (1, 3, 'map3')]


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (75 items, seed 7) re-solved independently against NCERT facts; '
              'fact tables reviewed line by line before generation',
    'checked': 75,
    'mismatches': 0,
    'fixes': [
        'review: distractor "Vitthala" removed from Mirabai/Surdas items (Vitthala is a form of Krishna, so it was not clearly wrong)',
        'review: distractor "gold" for Chota Nagpur minerals replaced (region has minor gold deposits)',
        'review: Assertion-Reason on Babur\'s artillery vs Lodi\'s elephants replaced (code b was arguable)',
        'review: "criminal case ... sessions court" reworded to "serious criminal case is tried in the sessions court"',
        'review: chronology rows with equal years (Constitution and Election Commission, both 1950) removed',
        'sample: nested (a)/(b) labels inside a long-answer part changed to (i)-(iii)',
        'sample: category options capitalised consistently',
    ],
    'note': 'Generators fixed, bank regenerated and revalidated.',
}]


def subtopic_names(sid):
    d = json.load(open(os.path.join(CUR_DIR, f'{sid}.json'), encoding='utf-8'))
    return {s['id'][len(sid) + 3:]: s['name'] for s in d['subtopics']}


def families(sid=SID, modules=MODULES, grade=GRADE):
    data = {}
    for mod in modules:
        try:
            m = __import__(mod)
        except ModuleNotFoundError:
            continue
        data.update(m.DATA)
    fams = kit.build(f'{sid}-ch', data, subtopic_names(sid), grade=grade)
    bad = kit.check(fams)
    if bad:
        raise SystemExit('\n'.join(bad))
    return fams


def main():
    b = Builder(SID, 'scripts/questions/cbse/g8_social_science.py', families(), MOCK_PATTERN)
    files = b.build()
    b.write(files, ACCURACY)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
