"""Shared helpers for the IB DP Computer Science packs (ib_g11_computer_science, available to g12).

Packs create their own Registry R and call the helpers with it:
    from ib_cs_common import Kit
    K = Kit(R, case_orgs=[...], style=STYLE)
    templates = K.templates
    K.ar('ch01-st1', [...]); K.scen(...); K.code_tasks(...)
"""
from __future__ import annotations

import contextlib
import io
import re

from _common import T, mcq
from engine import Slot

AR_OPTS = ['Both A and R are true, and R is the correct explanation of A.',
           'Both A and R are true, but R is not the correct explanation of A.',
           'A is true but R is false.',
           'A is false but R is true.']

GENERIC_PARTS = ('define', 'why', 'contrast', 'misc', 'evaluate')

PEOPLE = ['Amara', 'Lukas', 'Sofia', 'Kenji', 'Priya', 'Mateo', 'Chloe', 'Omar', 'Ingrid', 'Tomas', 'Aiko',
          'Nia', 'Yusuf', 'Elena', 'Kwame', 'Mei', 'Lars', 'Zara', 'Diego', 'Hana', 'Felix', 'Leila', 'Arjun',
          'Freya', 'Isabel', 'Jonas', 'Ana', 'Rafael', 'Sana', 'Noah', 'Alessia', 'Tariq', 'Maya']


def fake_open(store: dict):
    """Return an open() replacement backed by the dict `store` (filename -> text); supports r, w, a modes."""
    class _F(io.StringIO):
        def __init__(self, name, mode):
            self._name, self._mode = name, mode
            if 'r' in mode:
                if name not in store:
                    raise FileNotFoundError(name)
                super().__init__(store[name])
            elif 'a' in mode:
                super().__init__(store.get(name, ''))
                self.seek(0, 2)
            else:
                super().__init__('')

        def close(self):
            if 'r' not in self._mode and not self.closed:
                store[self._name] = self.getvalue()
            super().close()

        def __exit__(self, *a):
            self.close()

    return lambda name, mode='r', **kw: _F(name, mode)


def run_py(code: str, files: dict | None = None) -> str:
    """Execute generated Python and return what it prints. `files` gives a fake file system for open()."""
    buf = io.StringIO()
    g = {'__name__': '__qb__'}
    if files is not None:
        store = files
        g['open'] = fake_open(store)
        g['__files__'] = store
    with contextlib.redirect_stdout(buf):
        exec(code, g)
    return buf.getvalue().rstrip('\n')


def table(headers, rows) -> str:
    h = ' | '.join(str(x) for x in headers)
    body = '\n'.join(' | '.join('NULL' if v is None else str(v) for v in r) for r in rows)
    return f'{h}\n{body}'


def r2(x, nd=2):
    s = f'{x:.{nd}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


def code_q(code, lang='Python'):
    return f'Consider the following {lang} code.\n{code}\nState the exact output.'


def _clean_key(k):
    k = re.sub(r'\((\d+) marks: ', '(', k)
    k = re.sub(r'Markbands \(\d+ marks\)', 'Markbands', k)
    return k


def _split_marks(total, parts):
    raw = [max(1, int(p.get('marks') or 2)) for p in parts]
    s = sum(raw)
    floor = 2 if total >= 2 * len(parts) else 1
    ms = [max(floor, round(total * r / s)) for r in raw]
    while sum(ms) > total:
        i = ms.index(max(ms))
        if ms[i] <= floor:
            break
        ms[i] -= 1
    while sum(ms) < total:
        i = ms.index(max(ms))
        ms[i] += 1
    return ms


def compose(parts, total, intro=''):
    for p in parts:
        p['markingKey'] = _clean_key(p['markingKey'])
    ms = _split_marks(total, parts)
    letters = 'abcd'
    stem = (intro + '\n' if intro else '') + '\n'.join(f'({letters[i]}) {p["stem"]} [{ms[i]}]' for i, p in enumerate(parts))
    ans = ' '.join(f'({letters[i]}) {p["answer"]}' for i, p in enumerate(parts))
    key = ' '.join(f'({letters[i]}) [{ms[i]} marks] {p["markingKey"]}' for i, p in enumerate(parts))
    return stem, ans, key


def org_short(org):
    cuts = [org.find(x) for x in (',', ' keeps', ' logs', ' runs') if org.find(x) > 0]
    return org[:min(cuts)] if cuts else 'the organisation'


class Kit:
    def __init__(self, R, case_orgs, style, drop=('fact_short',)):
        self.R = R
        self.case_orgs = case_orgs
        self.style = style
        self.drop = set(drop)
        self._cache = {}

    # ---------- registration helpers ----------
    def ar(self, key, items, d=(2, 4)):
        """Assertion-Reason MCQs: (assertion, reason, index of correct option 0-3, explanation)."""
        def fn(rng, slot):
            a, r_, k, why = rng.choice(items)
            return dict(stem=f'Assertion (A): {a}\nReason (R): {r_}\nWhich option is correct?', options=list(AR_OPTS),
                        answer=AR_OPTS[k], markingKey=f'{"ABCD"[k]}. {why}', type='mcq')
        self.R.t.setdefault(key, []).append(T('C2', d, fn, 'mcq', None, 'ar'))

    def code_tasks(self, key, items, c='C4', d=(3, 5), lang_note='Python; an equivalent Java solution is equally acceptable'):
        """(stem, model_code, test_code, marks): the model answer is executed against the tests at import."""
        for stem, model, test, marks in items:
            exec(model + '\n' + test, {})
        def fn(rng, slot):
            stem, model, test, marks = rng.choice(items)
            return dict(stem=stem, answer=model, type='long', marks=marks,
                        markingKey=f'Model answer ({lang_note}):\n{model}\nMarks: correct headers/parameters; correct logic and boundary handling; correct return values/output. Tested with:\n{test}')
        self.R.t.setdefault(key, []).append(T(c, d, fn, 'long', None, 'code_task'))

    def specific(self, key, c, d, items, type='short'):
        """items: (context, [(question, answer, marks), ...]) – every question tied to its own context."""
        def fn(rng, slot):
            ctx, qs = rng.choice(items)
            q, a, m = rng.choice(qs)
            return dict(stem=f'{ctx} {q}', answer=a, markingKey=a + ' Marks for relevant points applied to the scenario.', type=type,
                        marks=m + (1 if slot.d >= 4 else 0))
        self.R.t.setdefault(key, []).append(T(c, d, fn, type, None, 'specific'))

    # ---------- composite templates ----------
    def _parts_for(self, base, st, slot, rng, plan, only=None):
        out, used = [], set()
        for c, d in plan:
            pool = [t for t in base if t.type != 'mcq' and t.name not in ('structured', 'case_study')
                    and c in (t.c if isinstance(t.c, tuple) else (t.c,)) and (only is None or t.name in only)]
            fresh = [t for t in pool if id(t.fn) not in used]
            pool = fresh or pool
            rng.shuffle(pool)
            for t in pool[:6]:
                try:
                    o = t.fn(rng, Slot(st, slot.chapter, c, d))
                except IndexError:
                    o = None
                if o and o.get('type') != 'mcq' and not o.get('options') and all(o['stem'] != p['stem'] for p in out):
                    out.append(o)
                    used.add(id(t.fn))
                    break
        return out

    def structured_t(self, base, st):
        def fn(rng, slot):
            if slot.c == 'C4':
                plan = [('C2', 2), ('C3', 3), ('C4', max(3, slot.d))]
            elif slot.d >= 4:
                plan = [('C1', 2), ('C3', 3), ('C3', 4)]
            else:
                plan = [('C1', 2), ('C2', 2), ('C3', 3)]
            parts = self._parts_for(base, st, slot, rng, plan)
            if len(parts) < 2:
                return None
            total = slot.marks or sum(int(p.get('marks') or 2) for p in parts)
            stem, ans, key = compose(parts, total)
            return dict(stem=stem, answer=ans, markingKey=key, type='multi_step', marks=total)
        return T(('C3', 'C4'), (3, 5), fn, 'multi_step', 'structured', 'structured')

    def case_study_t(self, base, st):
        def fn(rng, slot):
            org = rng.choice(self.case_orgs)
            short = org_short(org)
            parts = self._parts_for(base, st, slot, rng, [('C2', 3), ('C4', max(3, slot.d))], GENERIC_PARTS)
            if len(parts) < 2:
                return None
            for p in parts:
                p['stem'] = p['stem'].rstrip() + f' Refer to {short} in your answer.'
            total = slot.marks or 6
            stem, ans, key = compose(parts, total, 'Case study context: ' + org)
            return dict(stem=stem, answer=ans, markingKey=key + ' Credit is given only for points applied to the stated organisation (not generic answers).', type='long', marks=total)
        return T('C4', (3, 5), fn, 'long', 'case_study', 'case_study')

    def templates(self, st):
        if st['id'] not in self._cache:
            base = [t for t in self.R.build(st, self.style) if t.name not in self.drop]
            self._cache[st['id']] = base + [self.structured_t(base, st), self.case_study_t(base, st)]
        return self._cache[st['id']]
