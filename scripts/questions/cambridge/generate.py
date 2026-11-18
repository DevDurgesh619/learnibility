#!/usr/bin/env python3
"""
Generate the Cambridge question bank, one subject at a time.

  python3 scripts/questions/cambridge/generate.py cambridge-g10-physics [more ids] [--all] [--curriculum DIR] [--out DIR]

Counts come from plan.json (derived from the assessment cost sheet, tabs "IGCSE 8th-10th" and
"IGCSE 11th and 12th"). Subtopics come from data/curriculum/{subjectId}.json (W2).
Content (templates per chapter) comes from content/{module}.py, module name = subject id with
'cambridge-' removed and '-' -> '_' (e.g. g10_physics).
"""
import argparse
import importlib
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import core  # noqa: E402

HERE = os.path.dirname(__file__)


def module_for(sid):
    name = sid.replace('cambridge-', '').replace('-', '_')
    return importlib.import_module(f'content.{name}')


def run(sid, plan, out_root):
    row = plan[sid]
    content = module_for(sid)
    chapters, subs = core.load_curriculum(sid)
    subject = {'id': sid}
    try:
        subject = core.load_subjects().get(sid, subject)
    except FileNotFoundError:
        pass
    assert len(chapters) == row['nch'], f'{sid}: curriculum has {len(chapters)} chapters, cost sheet {row["nch"]}'
    g = core.Generator(subject, chapters, subs, content, row)
    out_dir = os.path.join(out_root, sid)
    status_path = os.path.join(out_dir, '_status.json')
    status = {'subjectId': sid, 'board': 'cambridge', 'generatedBy': core.GENERATED_BY,
              'target': row['total'], 'chapters': {}, 'mocks': None, 'validated': False,
              'accuracyLog': []}
    allq = []
    for ch in chapters:
        items = g.chapter(ch)
        core.write_json(os.path.join(out_dir, f"{ch['id']}.json"), core.envelope(items))
        allq += items
        bank = [q for q in items if q['set'] == 'mastery_bank']
        status['chapters'][ch['id']] = {
            'name': ch['name'], 'mastery': len(bank),
            'formA': sum(q['set'] == 'practice_form_a' for q in items),
            'formB': sum(q['set'] == 'practice_form_b' for q in items),
            'done': True,
        }
        core.write_json(status_path, status)
    mocks, papers = g.mocks()
    core.write_json(os.path.join(out_dir, 'mocks.json'), core.envelope(mocks, papers=papers))
    allq += mocks
    status['mocks'] = {'count': row['nmock'], 'perMock': row['qpm'], 'questions': len(mocks)}
    bank = [q for q in allq if q['set'] == 'mastery_bank']
    c, d = core.mix(bank)
    status['total'] = len(allq)
    status['masteryMix'] = {'C': c, 'D': d}
    status['topicMap'] = {k: v for k, v in g.topic_map.items() if v}
    core.write_json(status_path, status)
    return allq, status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--curriculum')
    ap.add_argument('--out')
    a = ap.parse_args()
    if a.curriculum:
        core.CURRICULUM = a.curriculum
    out = a.out or core.OUT
    with open(os.path.join(HERE, 'plan.json')) as f:
        plan = json.load(f)
    ids = list(plan) if a.all else a.ids
    for sid in ids:
        qs, st = run(sid, plan, out)
        print(f"{sid}: {len(qs)} questions (target {plan[sid]['total']}); mastery mix C {st['masteryMix']['C']} D {st['masteryMix']['D']}")


if __name__ == '__main__':
    main()
