#!/usr/bin/env python3
"""Build the onboarding test forms (QB-ONB).

15 form designs -> one JSON file per board/grade/stream a student can be in:
  grades 8-10: 3 boards x 3 grades            = 9 files  (onb-{board}-g{grade}-none)
  grades 11-12: 3 streams x 2 grades x 3 boards = 18 files (onb-{board}-g{grade}-{stream})
The 6 senior designs share most content across boards and swap in board-specific items.

Usage:  python3 scripts/onboarding/build-forms.py
Writes: data/questions/onboarding/{formId}.json, index.json, _status.json (validation is separate:
        node scripts/onboarding/validate.ts).
"""
import hashlib
import importlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from dsl import LEVELS_BY_SLOT  # noqa: E402

OUT = os.path.join(ROOT, 'data', 'questions', 'onboarding')
GENERATED_BY = 'scripts/onboarding/build-forms.py'
BOARDS = ['cbse', 'cambridge', 'ib']

CONCEPT_BY_D = {'D1': 'C1', 'D2': 'C2', 'D3': 'C3'}
MARKS_BY_D = {'D1': 1, 'D2': 2, 'D3': 3}
MINUTES_BY_D = {'D1': 0.5, 'D2': 1.0, 'D3': 1.5}

# Gap on a wrong answer, from the workbook's Gap Diagnosis decision rule:
# prerequisite items -> G1; this grade's items: C1 (D1) miss -> G1 (no recall / prerequisite),
# C2 (D2) miss -> G2 conceptual, C3 (D3) miss -> G3 procedural.
def default_gap(half, d):
    if half == 'prerequisite':
        return 'G1'
    return {'D1': 'G1', 'D2': 'G2', 'D3': 'G3'}[d]


LADDER = {
    'start': 'D2', 'floor': 'D1', 'ceiling': 'D3', 'hitsToStepUp': 2,
    'weights': {'D1': 1, 'D2': 2, 'D3': 3},
}
BANDS = [
    {'band': 'excellent', 'minPercent': 80},
    {'band': 'above_avg', 'minPercent': 65},
    {'band': 'average', 'minPercent': 45},
    {'band': 'below_avg', 'minPercent': 0},
]

DESIGN_MODULES = [
    'content.g8_cbse', 'content.g8_cambridge', 'content.g8_ib',
    'content.g9_cbse', 'content.g9_cambridge', 'content.g9_ib',
    'content.g10_cbse', 'content.g10_cambridge', 'content.g10_ib',
    'content.g11_science', 'content.g11_commerce', 'content.g11_humanities',
    'content.g12_science', 'content.g12_commerce', 'content.g12_humanities',
]


def seeded_shuffle(options, key):
    rnd = random.Random(int(hashlib.sha1(key.encode()).hexdigest()[:12], 16))
    out = list(options)
    rnd.shuffle(out)
    return out


_CURRICULA = {}


def _curriculum(subject_id):
    if subject_id not in _CURRICULA:
        f = os.path.join(ROOT, 'data', 'curriculum', f'{subject_id}.json')
        _CURRICULA[subject_id] = json.load(open(f)) if os.path.exists(f) else None
    return _CURRICULA[subject_id]


def find_subtopic(subject_id, keywords):
    """'subject~kw1|kw2': first subtopic (in chapter order) whose name, or failing that whose chapter
    name, contains a keyword. Fails loudly so a bad keyword never ships an unlinked item."""
    d = _curriculum(subject_id)
    assert d, f'no curriculum for {subject_id}'
    names = {s['id']: s['name'].lower() for s in d.get('subtopics', [])}
    chapters = sorted(d['items'], key=lambda c: c['id'])
    for kw in keywords.lower().split('|'):
        for ch in chapters:
            for sid in ch['subtopicIds']:
                if kw in names.get(sid, ''):
                    return sid
        for ch in chapters:
            if kw in ch['name'].lower() and ch['subtopicIds']:
                return ch['subtopicIds'][0]
    raise AssertionError(f'{subject_id}: no subtopic matches {keywords!r}')


def resolve_ref(ref, board):
    if isinstance(ref, dict):
        ref = ref[board]
    if '~' in ref:
        subject_id, kw = ref.split('~', 1)
        sid = find_subtopic(subject_id, kw)
        return subject_id, sid.rsplit('-st', 1)[0], sid
    subject_id, ch, st = ref.split(':')
    chapter_id = f'{subject_id}-ch{int(ch):02d}'
    return subject_id, chapter_id, f'{chapter_id}-st{int(st)}'


def curriculum_index():
    """subtopicIds present in data/curriculum (empty until W2 lands)."""
    ids = set()
    d = os.path.join(ROOT, 'data', 'curriculum')
    if not os.path.isdir(d):
        return ids
    for f in os.listdir(d):
        if not f.endswith('.json') or f == 'subjects.json':
            continue
        try:
            data = json.load(open(os.path.join(d, f)))
        except Exception:
            continue
        for st in data.get('subtopics', []) or []:
            if isinstance(st, dict) and 'id' in st:
                ids.add(st['id'])
        for it in data.get('items', []):
            for st in it.get('subtopics', []) or []:
                if isinstance(st, dict) and 'id' in st:
                    ids.add(st['id'])
            if isinstance(it, dict) and '-st' in str(it.get('id', '')):
                ids.add(it['id'])
    return ids


def build_part_a(groups, board, form_id, counter, linked_ids):
    items = []
    for g in groups:
        for slot_no, slot in enumerate(g['slots'], start=1):
            if 'ref' not in slot:          # board swap: {board: S(...)}
                slot = slot[board]
            hint = slot['hint'][board] if isinstance(slot['hint'], dict) else slot['hint']
            levels = LEVELS_BY_SLOT[slot_no]
            assert len(slot['items']) == len(levels), \
                f"{form_id} {g['group']} slot {slot_no}: need {levels}, got {len(slot['items'])}"
            half = 'prerequisite' if slot_no <= 4 else 'current'
            subject_id, chapter_id, subtopic_id = resolve_ref(slot['ref'], board)
            for i, (d, it) in enumerate(zip(levels, slot['items'])):
                stem, correct, wrong, why = it
                counter[0] += 1
                qid = f'{form_id}-q{counter[0]:02d}'
                content_key = hashlib.sha1(f"A|{g['group']}|{stem}".encode()).hexdigest()[:12]
                q = {
                    'id': qid,
                    'subtopicId': subtopic_id,
                    'chapterId': chapter_id,
                    'subjectId': subject_id,
                    'conceptGroup': CONCEPT_BY_D[d],
                    'difficulty': d,
                    'type': 'mcq' if wrong else 'numerical',
                    'stem': stem,
                    'answer': str(correct),
                    'marks': MARKS_BY_D[d],
                    'minutes': MINUTES_BY_D[d],
                    'alrRole': 'practised',
                    'likelyGapOnWrong': (slot.get('gaps') or [None] * 3)[i] or default_gap(half, d),
                    'set': 'onboarding',
                    'part': 'A',
                    'group': g['group'],
                    'slot': slot_no,
                    'half': half,
                    'subtopicHint': hint,
                    'subtopicLinked': subtopic_id in linked_ids,
                    'contentKey': content_key,
                }
                if wrong:
                    assert len(wrong) == 3, f'{qid}: need 3 wrong options'
                    q['options'] = seeded_shuffle([str(correct)] + [str(w) for w in wrong], content_key)
                    letter = 'ABCD'[q['options'].index(str(correct))]
                    q['markingKey'] = f'{letter}. {correct}. {why}'
                else:
                    q['markingKey'] = f'{correct}. {why}'
                if slot.get('note'):
                    q['prerequisiteNote'] = slot['note']
                items.append(q)
    return items


def build_part_b(grade, form_id, counter):
    mod = importlib.import_module('content.part_b')
    out = []
    for it in mod.items_for(grade):
        counter[0] += 1
        x = dict(it)
        x['id'] = f'{form_id}-q{counter[0]:02d}'
        x['part'] = 'B'
        x['contentKey'] = hashlib.sha1(f"B|{it['stem']}".encode()).hexdigest()[:12]
        x['options'] = seeded_shuffle(it['options'], x['contentKey'])
        out.append(x)
    return out


def build_survey(mod_name, board, grade, stream, form_id, counter, params):
    mod = importlib.import_module(mod_name)
    out = []
    for it in mod.items_for(board, grade, stream):
        counter[0] += 1
        x = dict(it)
        x['id'] = f'{form_id}-q{counter[0]:02d}'
        p = params[x['paramId']]
        x['tier'] = p['tier']
        x['screened'] = p['tier'] == 'T3'
        x.setdefault('optional', x['screened'] or p['tier'] == 'T2' and x['part'] == 'C')
        x['contentKey'] = hashlib.sha1(f"{x['part']}|{it['prompt']}".encode()).hexdigest()[:12]
        out.append(x)
    return out


def scoring_map(groups_meta, part_b, survey):
    writes = [
        {'paramId': 'p1', 'rule': 'Grade of the form taken', 'source': 'M1', 'confidence': 'high'},
        {'paramId': 'p3', 'rule': 'Board of the form taken', 'source': 'M1', 'confidence': 'high'},
        {'paramId': 'p5', 'rule': 'Stream of the form taken (grades 11-12)', 'source': 'M1', 'confidence': 'high'},
        {'paramId': 'p278', 'rule': 'Per subtopic seen: pMastery 0.7 if right at D2/D3, 0.55 if right at D1, '
                                    '0.25 if wrong; level L0-L3 from the ladder step reached', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p279', 'rule': 'Prerequisite-gap index = 100 x weighted misses / weighted items seen in slots 1-4, '
                                    'averaged over groups', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p13', 'rule': 'Groups with the highest Part A percent (top 1-2, only if >= 65%)', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p14', 'rule': 'Groups with the lowest Part A percent (bottom 1-2, only if < 65%)', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p140', 'rule': 'Mean confidence (1-5) per group', 'source': 'M1', 'confidence': 'medium'},
        {'paramId': 'p141', 'rule': 'Calibration = 1 - mean |confidence/5 - correct| over Part A (feeds the first MCI reading)',
         'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p284', 'rule': 'Highest difficulty answered correctly twice in a row: D1 low, D2 medium, D3 high',
         'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p61', 'rule': 'Verbal reasoning = percent of Part B verbal items right', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p62', 'rule': 'Numerical reasoning = percent of Part B numerical items right', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p63', 'rule': 'Abstract reasoning = percent of Part B abstract items right', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p64', 'rule': 'Spatial reasoning = percent of Part B spatial items right', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p65', 'rule': 'Logical deduction = percent right on Part B items tagged p65', 'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p68', 'rule': 'Numeracy fluency = numerical percent scaled by speed (right answers under target time count 1.2x, max 100)',
         'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p69', 'rule': 'Processing speed = 100 x share of Part B items answered right within target seconds',
         'source': 'M9', 'confidence': 'low'},
        {'paramId': 'p200', 'rule': 'RIASEC profile: each career-interest item scored 1-5; letter score = mean of its 2 items; '
                                    'top 3 letters form the code (e.g. IRC)', 'source': 'M1', 'confidence': 'low'},
    ]
    seen = {w['paramId'] for w in writes}
    for s in survey:
        if s['paramId'] not in seen:
            writes.append({'paramId': s['paramId'], 'rule': f"Answer to {s['id']} ({s['responseType']})",
                           'source': 'M2' if s['respondent'] == 'parent' else 'M1',
                           'confidence': 'medium' if s['respondent'] == 'parent' else 'low'})
            seen.add(s['paramId'])
    reasoning = []
    for dom, pid in [('numerical', 'p62'), ('verbal', 'p61'), ('abstract', 'p63'), ('spatial', 'p64')]:
        reasoning.append({'domain': dom, 'paramId': pid, 'itemIds': [b['id'] for b in part_b if b['domain'] == dom]})
    riasec = {k: [] for k in 'RIASEC'}
    for s in survey:
        if s.get('riasec'):
            riasec[s['riasec']].append(s['id'])
    return {'ladder': LADDER, 'bandCutoffs': BANDS, 'groups': groups_meta, 'writes': writes,
            'reasoning': reasoning, 'riasec': riasec}


def main():
    params = {p['id']: p for p in json.load(open(os.path.join(ROOT, 'data', 'profile', 'parameters.json')))['items']}
    linked_ids = curriculum_index()
    os.makedirs(OUT, exist_ok=True)
    index = []
    total_items = 0
    for mod_name in DESIGN_MODULES:
        try:
            mod = importlib.import_module(mod_name)
        except ModuleNotFoundError as e:
            if e.name == mod_name:
                print(f'skip {mod_name} (not written yet)')
                continue
            raise
        d = mod.DESIGN
        for board in d['boards']:
            stream = d['stream']
            grade = d['grade']
            form_id = f'onb-{board}-g{grade}-{stream}'
            groups = d['groups'](board) if callable(d['groups']) else d['groups']
            counter = [0]
            part_a = build_part_a(groups, board, form_id, counter, linked_ids)
            part_b = build_part_b(grade, form_id, counter)
            part_c = build_survey('content.part_c', board, grade, stream, form_id, counter, params)
            part_p = build_survey('content.parent', board, grade, stream, form_id, counter, params)
            groups_meta = []
            for g in groups:
                sids = sorted({q['subjectId'] for q in part_a if q['group'] == g['group']})
                groups_meta.append({'group': g['group'], 'label': g['label'], 'subjectIds': sids})
            form = {
                'formId': form_id,
                'designId': d['designId'],
                'board': board, 'grade': grade, 'stream': stream,
                'title': d['title'](board) if callable(d['title']) else d['title'],
                'minutes': {'A': 8 * len(groups), 'B': 12, 'C': 8, 'P': 5},
                'partA': {'pool': len(part_a), 'delivered': 8 * len(groups)},
                'scoring': scoring_map(groups_meta, part_b, part_c + part_p),
            }
            items = part_a + part_b + part_c + part_p
            with open(os.path.join(OUT, f'{form_id}.json'), 'w') as f:
                json.dump({'schemaVersion': 1, 'generatedBy': GENERATED_BY, 'form': form, 'items': items},
                          f, ensure_ascii=False, indent=2)
                f.write('\n')
            total_items += len(items)
            index.append({'formId': form_id, 'designId': d['designId'], 'board': board, 'grade': grade,
                          'stream': stream, 'title': form['title'], 'items': len(items),
                          'partA': len(part_a), 'partB': len(part_b), 'partC': len(part_c), 'parent': len(part_p),
                          'path': f'data/questions/onboarding/{form_id}.json'})
            print(f'{form_id}: A {len(part_a)}  B {len(part_b)}  C {len(part_c)}  P {len(part_p)}')
    with open(os.path.join(OUT, 'index.json'), 'w') as f:
        json.dump({'schemaVersion': 1, 'generatedBy': GENERATED_BY, 'items': index}, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'{len(index)} forms, {total_items} items')


if __name__ == '__main__':
    main()
