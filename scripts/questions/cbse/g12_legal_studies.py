#!/usr/bin/env python3
"""Generate the CBSE class 12 Legal Studies (074) question bank (cbse-g12-legal-studies, 1215 questions).

Fact tables per subtopic live in g12_legal_studies_a.py (chapters 1-7) and g12_legal_studies_b.py (chapters 8-13);
g12_hum_engine.py turns them into question families. No textbook passage is reproduced.

Paper pattern (SQP, theory 80 marks, 40 questions): 20 MCQ × 1 (18 MCQ + 2 Assertion-Reason), 8 × 2, 8 × 3, 4 × 5.

Note: qbank.load_curriculum treats every id containing '-st' as a subtopic, and 'legal-studies' contains '-st',
so it finds no chapters for this subject. This script loads the curriculum file itself and sets Builder.cur.

Run: python3 scripts/questions/cbse/g12_legal_studies.py
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

SID = 'cbse-g12-legal-studies'
MOCK_PATTERN = [(18, 1, 'mcq'), (2, 1, 'ar'), (8, 2, 'short'), (8, 3, 'q3'), (4, 5, 'long5')]
DEFAULTS = {'long_marks': 5, 'case_marks': (1, 1, 2)}
CUSTOM = {'q3', 'long5'}


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
            if f.type == 'long' and f.marks == 5:
                f.kinds = tuple(f.kinds) + ('long5',)
            elif f.type == 'explain' and 'case' not in f.kinds and f.marks == 3:
                f.kinds = tuple(f.kinds) + ('q3',)
    return fams


def chapters():
    out = []
    for mod in ('g12_legal_studies_a', 'g12_legal_studies_b'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


def curriculum():
    path = os.path.join(qbank.CUR_DIR, f'{SID}.json')
    data = json.load(open(path, encoding='utf-8'))
    subs = {s['id']: s for s in data['subtopics']}
    chs = [{'id': c['id'], 'name': c.get('name', ''),
            'subtopics': [{'id': s, 'name': subs[s].get('name', ''), 'weight': subs[s].get('weight', 'S')}
                          for s in c['subtopicIds']]}
           for c in sorted(data['items'], key=lambda c: c['id'])]
    return {'chapters': chs, 'source': os.path.relpath(path, qbank.ROOT)}


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (65 items) plus all written items of mock 3 (20 items) re-solved by hand against '
              'the CBSE Legal Studies class 12 textbook and the bare Acts and judgments cited; every fact line re-checked',
    'checked': 85,
    'mismatches': 0,
    'fixes': [
        "engine keys cited 'NCERT'; Legal Studies uses the CBSE textbook, so keys now cite the CBSE textbook",
        "source-based items: a variant whose part (ii) asks to explain the same term that answers part (i) is now rejected and regenerated (no_echo guard); the redundant 'A natural person is' recall line was dropped",
        "arbitrator-number item reworded (Section 10: the number fixed by the parties must not be even; otherwise a sole arbitrator)",
        "dropped a 'year of M.C. Mehta absolute liability' item (judgment of December 1986 is reported as 1987, so the year is ambiguous)",
        "three vague assertion lines ('legal literacy camps are organised' etc.) rewritten as arguable statements for the 'Examine' items",
        'mock sections use custom kinds q3 and long5 so the 3-mark and 5-mark slots take only items whose keys are written for those marks',
    ],
}]


def textbook(files):
    """The engine's keys cite 'NCERT'; Legal Studies uses the CBSE textbook, so reword those keys."""
    for items in files.values():
        for q in items:
            for k, v in q.items():
                if isinstance(v, str) and 'NCERT' in v:
                    q[k] = v.replace('the NCERT chapter', 'the CBSE textbook chapter').replace(
                        'NCERT evidence', 'evidence from the CBSE textbook').replace('NCERT', 'CBSE textbook')
    return files


def main():
    qbank._fits = fits
    chs = chapters()
    fams = no_echo(tag(E.families([c for c, _ in chs], [cfg for _, cfg in chs])))
    b = qbank.Builder(SID, 'scripts/questions/cbse/g12_legal_studies.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.25)
    b.cur = curriculum()
    need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
    if set(fams) != need:
        raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = textbook(b.build())
    b.write(files, accuracy=ACCURACY or None)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files


if __name__ == '__main__':
    main()
