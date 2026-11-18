#!/usr/bin/env python3
"""Authoring aid: show which subtopic every slot of a design resolves to, per board.
  python3 scripts/onboarding/refs.py content.g11_science
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import runpy  # noqa: E402
ns = runpy.run_path(os.path.join(HERE, 'build-forms.py'), run_name='refs')
mod = importlib.import_module(sys.argv[1])
d = mod.DESIGN
for board in d['boards']:
    groups = d['groups'](board) if callable(d['groups']) else d['groups']
    for g in groups:
        for n, slot in enumerate(g['slots'], 1):
            if 'ref' not in slot:
                slot = slot[board]
            hint = slot['hint'][board] if isinstance(slot['hint'], dict) else slot['hint']
            try:
                sid = ns['resolve_ref'](slot['ref'], board)[2]
                name = ns['_curriculum'](sid.rsplit('-ch', 1)[0])
                nm = {s['id']: s['name'] for s in name['subtopics']}.get(sid, '?')
            except AssertionError as e:
                sid, nm = 'ERROR', str(e)
            print(f"{board:9} {g['group']:18} {n} {hint[:40]:40} -> {sid}  {nm[:60]}")
