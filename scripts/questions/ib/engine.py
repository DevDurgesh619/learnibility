#!/usr/bin/env python3
"""IB question-bank generator (QB-IB).

Builds the mastery bank, practice Forms A/B and mocks for one IB subject from
  - data/curriculum/{subjectId}.json      (chapters + subtopics, owned by W2)
  - data/questions/targets.json           (counts from the assessment cost sheet)
  - scripts/questions/ib/packs/{slug}.py  (authored content: item templates and fact packs)

Writes data/questions/{subjectId}/{chapterId}.json, mocks.json and _status.json.

Slot planning follows the class 8 maths workbook (sheets Assessment, Difficulty Mix, ALR Method):
  * per subtopic a student-check path (L 5, S 6, H 8 items) C1 -> C2 -> C3 -> C4 starting at D2,
  * wider-bank items fill the chapter to the cost-sheet count, steering the chapter towards the
    target mix C1 15 / C2 30 / C3 35 / C4 20 and D1 10 / D2 40 / D3 35 / D4 12 / D5 3,
  * ALR roles: 2 retention probes per subtopic (C1 and C3 at the lowest difficulty on the path),
    transfer probes on C3-D4+ and C4 items, everything else practised.

Run: python3 scripts/questions/ib/engine.py ib-g12-physics [--chapters ch01,ch02]
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import importlib.util
import json
import os
import random
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Callable

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
GENERATED_BY = 'scripts/questions/ib/engine.py'

C_TARGET = {'C1': 0.15, 'C2': 0.30, 'C3': 0.35, 'C4': 0.20}
D_TARGET = {'D1': 0.10, 'D2': 0.40, 'D3': 0.35, 'D4': 0.12, 'D5': 0.03}
CS = list(C_TARGET)
DS = list(D_TARGET)
# Plausible difficulty band for each concept group.
D_RANGE = {'C1': (1, 3), 'C2': (1, 4), 'C3': (1, 5), 'C4': (2, 5)}

# Student-check path per subtopic weight (workbook "Assessment" sheet pattern).
# role: R = retention probe, T = transfer probe, P = practised.
PATH = {
    'L': [('C1', 2, 'R'), ('C2', 2, 'P'), ('C3', 2, 'R'), ('C3', 3, 'P'), ('C4', 3, 'T')],
    'S': [('C1', 2, 'R'), ('C2', 2, 'P'), ('C2', 3, 'P'), ('C3', 2, 'R'), ('C3', 3, 'P'), ('C4', 3, 'T')],
    'H': [('C1', 2, 'R'), ('C2', 2, 'P'), ('C2', 3, 'P'), ('C3', 2, 'R'), ('C3', 3, 'P'), ('C3', 4, 'T'),
          ('C4', 3, 'T'), ('C4', 4, 'T')],
}
WEIGHT_SHARE = {'L': 1.0, 'S': 1.3, 'H': 1.7}
ROLE_NAME = {'R': 'retention_probe', 'T': 'transfer_probe', 'P': 'practised'}


# --------------------------------------------------------------------------------------------
# Slots
# --------------------------------------------------------------------------------------------
@dataclass
class Slot:
    subtopic: dict
    chapter: dict
    c: str
    d: int
    role: str = 'P'
    path: bool = False
    set: str = 'mastery_bank'
    # Optional constraints from mock sections.
    type: str | None = None
    marks: int | None = None
    section: str | None = None
    style: str | None = None  # free tag a pack can use (e.g. 'paper1a', 'data_based', 'essay')

    @property
    def D(self) -> str:
        return f'D{self.d}'


def apportion(n: int, pct: dict[str, float]) -> dict[str, int]:
    raw = {k: n * v for k, v in pct.items()}
    out = {k: int(v) for k, v in raw.items()}
    rest = n - sum(out.values())
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[:rest]:
        out[k] += 1
    return out


def _count(slots, attr):
    out: dict[Any, int] = {}
    for s in slots:
        out[getattr(s, attr)] = out.get(getattr(s, attr), 0) + 1
    return out


def plan_mastery(chapter: dict, subtopics: list[dict], n: int) -> list[Slot]:
    slots: list[Slot] = []
    for st in subtopics:
        for c, d, role in PATH[st['weight']]:
            slots.append(Slot(st, chapter, c, d, role, path=True))
    # If the paths alone exceed the chapter count, shorten the heaviest paths first.
    while len(slots) > n:
        # remove a non-retention practised path item from the subtopic with the most items
        by_st: dict[str, list[Slot]] = {}
        for s in slots:
            by_st.setdefault(s.subtopic['id'], []).append(s)
        big = max(by_st.values(), key=len)
        victim = next((s for s in reversed(big) if s.role == 'P'), big[-1])
        slots.remove(victim)
    # Fill to n with wider-bank items, steering towards the targets.
    c_t = apportion(n, C_TARGET)
    d_t = apportion(n, D_TARGET)
    need = n - len(slots)
    c_have = _count(slots, 'c')
    extra_c: list[str] = []
    for _ in range(need):
        k = max(CS, key=lambda k: (c_t[k] - c_have.get(k, 0), C_TARGET[k]))
        extra_c.append(k)
        c_have[k] = c_have.get(k, 0) + 1
    d_have = _count(slots, 'd')
    extra_d: list[int] = []
    for _ in range(need):
        k = max(range(1, 6), key=lambda k: (d_t[f'D{k}'] - d_have.get(k, 0), D_TARGET[f'D{k}']))
        extra_d.append(k)
        d_have[k] = d_have.get(k, 0) + 1
    extra_c.sort()
    extra_d.sort()
    # assign to subtopics in proportion to weight
    load = {st['id']: sum(1 for s in slots if s.subtopic['id'] == st['id']) for st in subtopics}
    for c, d in zip(extra_c, extra_d):
        lo, hi = D_RANGE[c]
        d = min(max(d, lo), hi)
        st = min(subtopics, key=lambda st: (load[st['id']] / WEIGHT_SHARE[st['weight']], st['order']))
        load[st['id']] += 1
        slots.append(Slot(st, chapter, c, d, 'P'))
    rebalance(slots, n)
    assign_roles(slots)
    return slots


def rebalance(slots: list[Slot], n: int) -> None:
    """Nudge difficulties (then concept groups) so the chapter sits close to the target mix."""
    d_t = apportion(n, D_TARGET)
    for _ in range(4 * n):
        have = _count(slots, 'd')
        over = [k for k in range(1, 6) if have.get(k, 0) > d_t[f'D{k}']]
        under = [k for k in range(1, 6) if have.get(k, 0) < d_t[f'D{k}']]
        if not over or not under:
            break
        moved = False
        for u in sorted(under, key=lambda k: have.get(k, 0) - d_t[f'D{k}']):
            # move a slot from an adjacent over-full level, preferring wider-bank slots
            for o in sorted(over, key=lambda k: abs(k - u)):
                cands = [s for s in slots if s.d == o and D_RANGE[s.c][0] <= u <= D_RANGE[s.c][1]]
                cands.sort(key=lambda s: (s.path, s.role == 'R', abs(s.d - u)))
                if cands:
                    cands[0].d = u
                    moved = True
                    break
            if moved:
                break
        if not moved:
            break
    c_t = apportion(n, C_TARGET)
    for _ in range(2 * n):
        have = _count(slots, 'c')
        over = [k for k in CS if have.get(k, 0) > c_t[k] + 1]
        under = [k for k in CS if have.get(k, 0) < c_t[k] - 1]
        if not over or not under:
            break
        u, o = under[0], over[0]
        cands = [s for s in slots if s.c == o and not s.path and D_RANGE[u][0] <= s.d <= D_RANGE[u][1]]
        if not cands:
            cands = [s for s in slots if s.c == o and s.role == 'P' and D_RANGE[u][0] <= s.d <= D_RANGE[u][1]]
        if not cands:
            break
        cands[0].c = u


def is_transfer(s) -> bool:
    return (s.c == 'C3' and s.d >= 4) or (s.c == 'C4' and s.d >= 3)


def assign_roles(slots: list[Slot]) -> None:
    by_st: dict[str, list[Slot]] = {}
    for s in slots:
        by_st.setdefault(s.subtopic['id'], []).append(s)
    for group in by_st.values():
        for s in group:
            s.role = 'T' if is_transfer(s) else 'P'
        # two retention probes: lowest-difficulty C1 and C3 items on the path (fallback: any)
        for c in ('C1', 'C3'):
            pool = [s for s in group if s.c == c and s.role == 'P']
            pool.sort(key=lambda s: (not s.path, s.d))
            if pool:
                pool[0].role = 'R'
        n_r = sum(1 for s in group if s.role == 'R')
        if n_r < 2:
            pool = sorted([s for s in group if s.role == 'P'], key=lambda s: (s.c not in ('C1', 'C2'), s.d))
            for s in pool[: 2 - n_r]:
                s.role = 'R'


def plan_form(chapter: dict, subtopics: list[dict], n: int, form: str) -> list[Slot]:
    c_list = sorted(c for c, k in apportion(n, C_TARGET).items() for _ in range(k))
    d_list = sorted(int(d[1]) for d, k in apportion(n, D_TARGET).items() for _ in range(k))
    pairs = []
    for c, d in zip(c_list, d_list):
        lo, hi = D_RANGE[c]
        pairs.append((c, min(max(d, lo), hi)))
    # spread over subtopics: each subtopic gets a run of C1..C4 where possible
    order = sorted(subtopics, key=lambda st: -WEIGHT_SHARE[st['weight']])
    slots: list[Slot] = []
    # interleave: deal pairs round-robin over subtopics so each sees mixed groups
    for i, (c, d) in enumerate(pairs):
        st = order[i % len(order)]
        slots.append(Slot(st, chapter, c, d, 'P', set=f'practice_form_{form.lower()}'))
    slots.sort(key=lambda s: (CS.index(s.c), s.d))
    for s in slots:
        s.role = 'T' if is_transfer(s) else 'P'
    return slots


# --------------------------------------------------------------------------------------------
# Templates (packs build these)
# --------------------------------------------------------------------------------------------
@dataclass
class T:
    """An item template. fn(rng, slot) -> dict(stem, answer, markingKey, [options, type, marks, gap, minutes])."""
    c: str | tuple
    d: tuple[int, int]
    fn: Callable
    type: str = 'short'
    style: str | None = None
    name: str = ''
    uses: int = field(default=0, compare=False)

    def fits(self, slot: Slot, strict_style: bool = True) -> int:
        cs = self.c if isinstance(self.c, tuple) else (self.c,)
        if slot.c not in cs:
            return -1
        if slot.type == 'mcq' and self.type != 'mcq':
            return -1
        if slot.type and slot.type != 'mcq' and self.type == 'mcq':
            return -1
        if strict_style and slot.style and self.style != slot.style:
            return -1
        lo, hi = self.d
        if lo <= slot.d <= hi:
            score = 4
        else:
            score = 2 if abs(slot.d - (lo if slot.d < lo else hi)) == 1 else 0
        if slot.type and slot.type == self.type:
            score += 1
        if slot.style and self.style == slot.style:
            score += 2
        return score


DEFAULT_MARKS = {
    'C1': {1: 1, 2: 1, 3: 2},
    'C2': {1: 1, 2: 2, 3: 3, 4: 4},
    'C3': {1: 1, 2: 2, 3: 3, 4: 4, 5: 6},
    'C4': {2: 3, 3: 4, 4: 6, 5: 8},
}


def default_gap(slot: Slot, qtype: str) -> str:
    if slot.c == 'C1':
        return 'G1' if slot.d <= 2 else 'G2'
    if slot.c == 'C2':
        return 'G2'
    if slot.c == 'C3':
        return 'G3' if slot.d <= 3 else 'G5'
    return 'G5'


def norm_stem(s: str) -> str:
    # mirrors normaliseStem() in scripts/questions/validate.ts
    s = s.lower()
    s = re.sub(r'\([a-d]\)', ' ', s)
    s = re.sub(r'[\W_]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def shingles(norm: str) -> frozenset:
    w = norm.split(' ')
    if len(w) < 3:
        return frozenset([norm])
    return frozenset(' '.join(w[i:i + 3]) for i in range(len(w) - 2))


def near_dup(a, b) -> bool:
    (sa, la), (sb, lb) = a, b
    if min(la, lb) / max(la, lb, 1) < 0.7:
        return False
    inter = len(sa & sb)
    return inter / ((len(sa) + len(sb) - inter) or 1) >= 0.80


class Generator:
    def __init__(self, subject_id: str, pack):
        self.subject_id = subject_id
        self.pack = pack
        self.seen: set[str] = set()
        self.by_chapter: dict[str, list] = {}
        self.cfg = pack.CONFIG

    def templates_for(self, st: dict) -> list[T]:
        return self.pack.templates(st)

    def make(self, slot: Slot, qid: str) -> dict:
        tpls = self.templates_for(slot.subtopic)
        scored = [(t.fits(slot), t) for t in tpls]
        if max((x for x, _ in scored), default=-1) < 0:
            scored = [(t.fits(slot, strict_style=False), t) for t in tpls]
        best = max((x for x, _ in scored), default=-1)
        if best < 0:
            raise RuntimeError(f'No template fits {slot.subtopic["id"]} {slot.c}-{slot.D} type={slot.type} style={slot.style}')
        narrow = [t for x, t in scored if x == best]
        wide = [t for x, t in scored if x >= 0]
        seed = int(hashlib.md5(qid.encode()).hexdigest()[:12], 16)
        rng = random.Random(seed)
        last_err = None
        for attempt in range(120):
            pool = narrow if attempt < 40 else wide
            pool.sort(key=lambda t: (t.uses, rng.random()))
            t = pool[0] if attempt % 40 < 20 else rng.choice(pool)
            t.uses += 1
            try:
                out = t.fn(rng, slot)
            except IndexError as e:  # template exhausted its facts
                last_err = e
                continue
            if out is None:
                continue
            key = norm_stem(out['stem'])
            if key in self.seen:
                continue
            sig = (shingles(key), len(key))
            lst = self.by_chapter.setdefault(slot.chapter['id'], [])
            if any(near_dup(sig, o) for o in lst):
                continue
            lst.append(sig)
            self.seen.add(key)
            return self._finish(out, t, slot, qid)
        raise RuntimeError(f'Could not make a unique item for {qid} ({slot.subtopic["id"]} {slot.c}-{slot.D}); pack too thin. {last_err}')

    def _finish(self, out: dict, t: T, slot: Slot, qid: str) -> dict:
        qtype = out.get('type', t.type)
        marks = slot.marks or out.get('marks') or (1 if qtype == 'mcq' else DEFAULT_MARKS[slot.c].get(slot.d, 3))
        mpm = self.cfg.get('minutesPerMark', 1.2)
        if 'minutes' in out:
            minutes = out['minutes']
        elif qtype == 'mcq':
            minutes = self.cfg.get('mcqMinutes', 1.5)
        else:
            minutes = max(1.0, round(marks * mpm * 2) / 2)
        q = {
            'id': qid,
            'subtopicId': slot.subtopic['id'],
            'chapterId': slot.chapter['id'],
            'subjectId': self.subject_id,
            'conceptGroup': slot.c,
            'difficulty': slot.D,
            'type': qtype,
            'stem': out['stem'].strip(),
        }
        if out.get('options'):
            opts = out['options']
            assert len(opts) == 4, qid
            assert out['answer'] in opts, (qid, out['answer'], opts)
            assert len(set(opts)) == 4, (qid, opts)
            q['options'] = opts
        q['answer'] = str(out['answer']).strip()
        q['markingKey'] = out['markingKey'].strip()
        q['marks'] = int(marks)
        q['minutes'] = float(minutes)
        q['alrRole'] = ROLE_NAME[slot.role]
        q['likelyGapOnWrong'] = out.get('gap') or default_gap(slot, qtype)
        q['set'] = slot.set
        return q


# --------------------------------------------------------------------------------------------
# IO
# --------------------------------------------------------------------------------------------
def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def write_json(path, items):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump({'schemaVersion': 1, 'generatedBy': GENERATED_BY, 'items': items}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    os.replace(tmp, path)


def write_status(path, status):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    prev = load_json(path) if os.path.exists(path) else {}
    prev.update(status)
    prev['generatedBy'] = GENERATED_BY
    with open(path + '.tmp', 'w', encoding='utf-8') as f:
        json.dump(prev, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(path + '.tmp', path)


def load_pack(slug: str, subject_id: str):
    # Grade-specific pack wins (e.g. packs/ib_g12_physics.py), else slug pack (packs/physics.py).
    for name in (subject_id.replace('-', '_'), slug.replace('-', '_')):
        p = os.environ.get('QB_PACK') or os.path.join(HERE, 'packs', f'{name}.py')
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location(f'pack_{name}', p)
            mod = importlib.util.module_from_spec(spec)
            sys.path.insert(0, HERE)
            sys.path.insert(0, os.path.join(HERE, 'packs'))
            spec.loader.exec_module(mod)
            mod.init(subject_id)
            return mod
    raise SystemExit(f'No pack for {subject_id}')


def load_curriculum(subject_id: str):
    cdir = os.environ.get('CURRICULUM_DIR') or os.path.join(ROOT, 'data', 'curriculum')
    path = os.path.join(cdir, f'{subject_id}.json')
    data = load_json(path)
    items = data['items'] if isinstance(data, dict) and 'items' in data else data
    # Accept either a flat list of chapters + subtopics or one nested subject record.
    chapters, subtopics = [], {}
    if isinstance(data, dict) and isinstance(data.get('subtopics'), list):
        for st in data['subtopics']:
            subtopics[st['id']] = st
    if len(items) == 1 and 'chapters' in items[0]:
        rec = items[0]
        chapters = rec['chapters']
        for st in rec.get('subtopics', []):
            subtopics[st['id']] = st
        for ch in chapters:
            for st in ch.get('subtopics', []):
                if isinstance(st, dict):
                    subtopics[st['id']] = st
    else:
        for it in items:
            if re.search(r'-st\d+$', it['id']):
                subtopics[it['id']] = it
            elif re.search(r'-ch\d+$', it['id']):
                chapters.append(it)
    chapters.sort(key=lambda c: c['order'])
    out = []
    for ch in chapters:
        ids = ch.get('subtopicIds') or [s['id'] if isinstance(s, dict) else s for s in ch.get('subtopics', [])]
        sts = [subtopics[i] for i in ids]
        sts.sort(key=lambda s: s['order'])
        out.append((ch, sts))
    return out


def target_for(subject_id: str) -> dict:
    t = load_json(os.path.join(ROOT, 'data', 'questions', 'targets.json'))
    for it in t['items']:
        if it['subjectId'] == subject_id:
            return it
    raise SystemExit(f'No target for {subject_id}')


def now():
    return _dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def mix(items):
    n = len(items) or 1
    c = {k: round(100 * sum(1 for q in items if q['conceptGroup'] == k) / n, 1) for k in CS}
    d = {k: round(100 * sum(1 for q in items if q['difficulty'] == k) / n, 1) for k in DS}
    return {'conceptGroup': c, 'difficulty': d}


def run(subject_id: str, only: set[str] | None = None, mocks_only=False):
    tgt = target_for(subject_id)
    slug = subject_id.split('-', 2)[2]
    pack = load_pack(slug, subject_id)
    gen = Generator(subject_id, pack)
    curriculum = load_curriculum(subject_id)
    assert len(curriculum) == tgt['chapters'], (subject_id, len(curriculum), tgt['chapters'])
    out_dir = os.path.join(os.environ.get('QUESTIONS_DIR') or os.path.join(ROOT, 'data', 'questions'), subject_id)
    status_path = os.path.join(out_dir, '_status.json')
    status = {
        'subjectId': subject_id, 'board': 'ib', 'grade': tgt['grade'],
        'target': {'total': tgt['total'], 'bankPerChapter': tgt['bankPerChapter'],
                   'questionsPerForm': tgt['questionsPerForm'], 'mocks': tgt['mocks'],
                   'questionsPerMock': tgt['questionsPerMock']},
        'chapters': {}, 'counts': {}, 'validated': False, 'accuracyChecks': [], 'updatedUtc': now(),
    }
    if os.path.exists(status_path):
        old = load_json(status_path)
        status['chapters'] = old.get('chapters', {})
        status['accuracyChecks'] = old.get('accuracyChecks', [])
    # Seed the duplicate filter with chapters not being regenerated.
    for ch, _ in curriculum:
        p = os.path.join(out_dir, f'{ch["id"]}.json')
        regen = (only is None or ch['id'] in only) and not mocks_only
        if os.path.exists(p) and not regen:
            for q in load_json(p)['items']:
                k = norm_stem(q['stem'])
                gen.seen.add(k)
                gen.by_chapter.setdefault(q['chapterId'], []).append((shingles(k), len(k)))
    all_mastery = []
    for ch, sts in curriculum:
        p = os.path.join(out_dir, f'{ch["id"]}.json')
        if mocks_only or (only is not None and ch['id'] not in only):
            if os.path.exists(p):
                all_mastery += [q for q in load_json(p)['items'] if q['set'] == 'mastery_bank']
            continue
        items = []
        slots = plan_mastery(ch, sts, tgt['bankPerChapter'])
        per_st: dict[str, int] = {}
        # order: by subtopic, path first, then wider bank by C/D
        slots.sort(key=lambda s: (s.subtopic['order'], not s.path, CS.index(s.c), s.d))
        for s in slots:
            per_st[s.subtopic['id']] = per_st.get(s.subtopic['id'], 0) + 1
            items.append(gen.make(s, f'{s.subtopic["id"]}-q{per_st[s.subtopic["id"]]:02d}'))
        for form in ('A', 'B'):
            for i, s in enumerate(plan_form(ch, sts, tgt['questionsPerForm'], form), 1):
                items.append(gen.make(s, f'{ch["id"]}-pf{form.lower()}-q{i:02d}'))
        write_json(p, items)
        all_mastery += [q for q in items if q['set'] == 'mastery_bank']
        status['chapters'][ch['id']] = {
            'mastery': sum(1 for q in items if q['set'] == 'mastery_bank'),
            'practiceFormA': sum(1 for q in items if q['set'] == 'practice_form_a'),
            'practiceFormB': sum(1 for q in items if q['set'] == 'practice_form_b'),
            'done': True, 'updatedUtc': now(),
        }
        status['updatedUtc'] = now()
        write_status(status_path, status)
        print(f'  {ch["id"]}: {len(items)} items', flush=True)
    if only is None or mocks_only:
        mocks = []
        for m in range(1, tgt['mocks'] + 1):
            slots = plan_mock(pack, curriculum, tgt, m)
            for i, s in enumerate(slots, 1):
                mocks.append(gen.make(s, f'{subject_id}-mock{m}-q{i:02d}'))
        for q in mocks:
            q.setdefault('mock', None)
        write_json(os.path.join(out_dir, 'mocks.json'), mocks)
        status['mocks'] = {'papers': tgt['mocks'], 'questions': len(mocks)}
    # counts
    total = 0
    for ch, _ in curriculum:
        p = os.path.join(out_dir, f'{ch["id"]}.json')
        if os.path.exists(p):
            total += len(load_json(p)['items'])
    mp = os.path.join(out_dir, 'mocks.json')
    nm = len(load_json(mp)['items']) if os.path.exists(mp) else 0
    status['counts'] = {'chapterFiles': total, 'mocks': nm, 'total': total + nm, 'target': tgt['total']}
    status['mastery'] = mix(all_mastery)
    status['updatedUtc'] = now()
    write_status(status_path, status)
    print(f'{subject_id}: {total + nm} / {tgt["total"]}')


def plan_mock(pack, curriculum, tgt, m: int) -> list[Slot]:
    """Sections come from pack.MOCK: list of dicts(count, c, d, type?, marks?, style?, section)."""
    spec = pack.MOCK
    n_total = sum(sec['count'] for sec in spec)
    assert n_total == tgt['questionsPerMock'], (n_total, tgt['questionsPerMock'])
    rng = random.Random(f'{tgt["subjectId"]}-mock{m}')
    # chapters for this subject; DP year-2 mocks cover both years only in content of this subject file.
    flat = [(ch, st) for ch, sts in curriculum for st in sts]
    rng.shuffle(flat)
    slots = []
    k = (m - 1) * 7
    for sec in spec:
        cs = sec['c'] if isinstance(sec['c'], (list, tuple)) else [sec['c']]
        ds = sec['d'] if isinstance(sec['d'], (list, tuple)) else [sec['d']]
        for i in range(sec['count']):
            ch, st = flat[k % len(flat)]
            k += 1
            slots.append(Slot(st, ch, cs[i % len(cs)], ds[(i * 7 + m) % len(ds)], 'P', set='mock',
                              type=sec.get('type'), marks=sec.get('marks'), section=sec.get('section'),
                              style=sec.get('style')))
    for s in slots:
        s.role = 'T' if is_transfer(s) else 'P'
    return slots


def capacity(subject_id: str):
    """Report, per subtopic and concept group, distinct stems the pack can make vs. what the plan needs."""
    tgt = target_for(subject_id)
    slug = subject_id.split('-', 2)[2]
    pack = load_pack(slug, subject_id)
    curriculum = load_curriculum(subject_id)
    short = 0
    for ch, sts in curriculum:
        need: dict[tuple, int] = {}
        for s in plan_mastery(ch, sts, tgt['bankPerChapter']) + plan_form(ch, sts, tgt['questionsPerForm'], 'A') * 2:
            need[(s.subtopic['id'], s.c)] = need.get((s.subtopic['id'], s.c), 0) + 1
        for st in sts:
            tpls = pack.templates(st)
            line = []
            for c in CS:
                stems = set()
                sigs = []
                for t in tpls:
                    cs = t.c if isinstance(t.c, tuple) else (t.c,)
                    if c not in cs:
                        continue
                    for d in range(t.d[0], t.d[1] + 1):
                        for k in range(25):
                            rng = random.Random(k * 31 + d)
                            try:
                                o = t.fn(rng, Slot(st, ch, c, d))
                            except IndexError:
                                o = None
                            if o:
                                k2 = norm_stem(o['stem'])
                                sig = (shingles(k2), len(k2))
                                if k2 not in stems and not any(near_dup(sig, z) for z in sigs):
                                    stems.add(k2)
                                    sigs.append(sig)
                n = need.get((st['id'], c), 0) + 1  # +1 headroom for mocks
                flag = "" if len(stems) >= int(n * 1.5) + 1 else '  <-- THIN'
                if flag:
                    short += 1
                line.append(f'{c} {len(stems)}/{n}{flag}')
            print(st['id'][-9:], st['weight'], ' | '.join(line), '|', st['name'][:50])
    print('thin cells:', short)


if __name__ == '__main__':
    args = sys.argv[1:]
    if '--capacity' in args:
        for sid in [a for a in args if not a.startswith('--')]:
            capacity(sid)
        sys.exit(0)
    only = None
    mocks_only = '--mocks' in args
    if '--chapters' in args:
        i = args.index('--chapters')
        only = set(args[i + 1].split(','))
        del args[i:i + 2]
    args = [a for a in args if not a.startswith('--')]
    for sid in args:
        if only:
            only = {c if c.startswith(sid) else f'{sid}-{c}' for c in only}
        run(sid, only, mocks_only)
