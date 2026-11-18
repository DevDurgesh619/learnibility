"""
Cambridge question-bank generator core (QB-CAM).

Builds, for one subject:
  data/questions/{subjectId}/{chapterId}.json   mastery bank + practice Forms A and B
  data/questions/{subjectId}/mocks.json         full mock papers mirroring the paper pattern
  data/questions/{subjectId}/_status.json       counts, tag mix, accuracy log, validated flag

Content lives in content/{module}.py. Each module exposes CHAPTERS: {chapterOrder: [Topic, ...]}
where a Topic is matched to the curriculum's subtopics by keywords (fallback: order).

A Topic holds templates. A template is a function (r: random.Random, D: int) -> dict with
  stem, answer, key (marking key), optional options (MCQ, 4 strings, answer is one of them),
  optional type, optional marks, optional minutes.
Templates are registered with the concept group they test and the difficulty range they support.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
from dataclasses import dataclass, field
from typing import Callable

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
CURRICULUM = os.environ.get('QB_CURRICULUM_DIR') or os.path.join(REPO, 'data', 'curriculum')
OUT = os.path.join(REPO, 'data', 'questions')
GENERATED_BY = 'scripts/questions/cambridge/generate.py'

C_TARGET = {'C1': 0.15, 'C2': 0.30, 'C3': 0.35, 'C4': 0.20}
D_TARGET = {'D1': 0.10, 'D2': 0.40, 'D3': 0.35, 'D4': 0.12, 'D5': 0.03}
ALLOWED_D = {'C1': (1, 2, 3), 'C2': (1, 2, 3, 4), 'C3': (1, 2, 3, 4, 5), 'C4': (2, 3, 4, 5)}

# Student-check path per subtopic weight (class 8 maths workbook, sheet "Assessment").
CHECK_PATH = {
    'L': [('C1', 1), ('C1', 2), ('C2', 2), ('C3', 2), ('C4', 2)],
    'S': [('C1', 2), ('C2', 2), ('C2', 3), ('C3', 2), ('C3', 3), ('C4', 3)],
    'H': [('C1', 2), ('C2', 2), ('C2', 3), ('C3', 2), ('C3', 3), ('C3', 4), ('C4', 3), ('C4', 4)],
}

# Default marks and minutes per cell (workbook pattern, extended for D1 and D5).
MARKS = {
    ('C1', 1): (1, 1), ('C1', 2): (1, 1), ('C1', 3): (2, 1.5),
    ('C2', 1): (1, 1), ('C2', 2): (1, 1.5), ('C2', 3): (2, 2), ('C2', 4): (3, 3),
    ('C3', 1): (1, 1.5), ('C3', 2): (2, 2), ('C3', 3): (3, 3), ('C3', 4): (4, 4), ('C3', 5): (5, 6),
    ('C4', 2): (3, 4), ('C4', 3): (4, 5), ('C4', 4): (5, 6), ('C4', 5): (6, 8),
}

CTX = {'want_marks': None}  # replaced by content._lib.CTX at import time

DEFAULT_TYPE = {'C1': 'mcq', 'C2': 'explain', 'C3': 'numerical', 'C4': 'multi_step'}


# ---------------------------------------------------------------- templates

@dataclass
class Tpl:
    C: str
    D: tuple
    fn: Callable
    type: str | None = None
    name: str = ''


@dataclass
class Topic:
    keys: list
    templates: list = field(default_factory=list)
    name: str = ''

    def add(self, C, D, type=None):
        D = tuple(D) if isinstance(D, (list, tuple, range)) else (D,)

        def deco(fn):
            self.templates.append(Tpl(C, D, fn, type, fn.__name__))
            return fn
        return deco


def _fixed_fn(entry, as_mcq):
    stem, answer, key = entry[0], entry[1], entry[2]
    dis = entry[3] if len(entry) > 3 else None

    def fn(r, D):
        if as_mcq and dis:
            opts, ans = mcq(r, answer, list(dis))
            return {'stem': stem, 'options': opts, 'answer': ans, 'key': key}
        return {'stem': stem, 'answer': answer, 'key': key}
    return fn


def _fixed(self, C, D, entries, type=None):
    """Register fixed items: (stem, answer, markingKey[, distractors]). With 3+ distractors -> MCQ."""
    D = tuple(D) if isinstance(D, (list, tuple, range)) else (D,)
    if not hasattr(self, 'entries'):
        self.entries = {}
    self.entries.setdefault(C, []).extend((e, D) for e in entries)
    for e in entries:
        as_mcq = len(e) > 3 and e[3] is not None and len(e[3]) >= 3
        self.templates.append(Tpl(C, D, _fixed_fn(e, as_mcq), 'mcq' if as_mcq else type, 'fixed'))
    return self


Topic.fixed = _fixed


def _pair_fn(entries, C):
    def fn(r, D):
        if len(entries) < 2:
            return None
        (a, _), (b, _) = r.sample(entries, 2)
        lead = 'Answer both parts.' if C == 'C1' else r.choice(['Answer both parts.', 'Explain your reasoning in each part.', 'Give a reason for each answer.'])
        return {'stem': f'{lead} (a) {a[0]} (b) {b[0]}',
                'answer': f'(a) {a[1]} (b) {b[1]}',
                'key': f'(a) {a[2]} (b) {b[2]}',
                'type': 'short' if C == 'C1' else 'explain',
                'marks': _km(a[2], C) + _km(b[2], C)}
    return fn


def _km(key, C):
    m = re.findall(r'\[(\d+)\]', key)
    if m:
        return int(m[-1])
    m = re.findall(r'(\d) marks?', key)
    return max(1, min(4, sum(int(x) for x in m))) if m else (1 if C == 'C1' else 2)


def augment(content):
    """Add two-part items built from each topic's fixed C1 and C2 entries."""
    for topics in content.CHAPTERS.values():
        for t in topics:
            if getattr(t, '_aug', False):
                continue
            t._aug = True
            for C, ents in getattr(t, 'entries', {}).items():
                if C in ('C1', 'C2') and len(ents) >= 3:
                    Ds = sorted({d for _, ds in ents for d in ds})
                    if C == 'C1':
                        Ds = sorted(set(Ds) | {2, 3})
                    t.templates.append(Tpl(C, tuple(Ds), _pair_fn(ents, C), 'short' if C == 'C1' else 'explain', 'pair'))


def topic(name, *keys):
    return Topic(keys=[k.lower() for k in (keys or (name,))], name=name)


# ---------------------------------------------------------------- helpers

def norm(s: str) -> str:
    """Same normalisation as scripts/questions/validate.ts."""
    s = s.lower()
    s = re.sub(r'\([a-d]\)', ' ', s)
    s = re.sub(r'[^\w\u0900-\u097F]+|_', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def shingles(n: str):
    w = n.split(' ')
    if len(w) < 3:
        return {n}
    return {f'{w[i]} {w[i + 1]} {w[i + 2]}' for i in range(len(w) - 2)}


NEAR_DUP = 0.85


def near_dup(sh, ln, lst):
    for sh2, ln2 in lst:
        if min(ln, ln2) / max(ln, ln2) < 0.7:
            continue
        inter = len(sh & sh2)
        if inter / (len(sh) + len(sh2) - inter or 1) >= NEAR_DUP - 0.01:
            return True
    return False


def seed_of(*parts) -> int:
    return int(hashlib.sha1('|'.join(map(str, parts)).encode()).hexdigest()[:12], 16)


def mcq(r: random.Random, correct: str, distractors: list, k: int = 3):
    """Return (options, answer) with 4 distinct options and the correct one shuffled in."""
    ds = []
    for d in distractors:
        if d != correct and d not in ds:
            ds.append(d)
    if len(ds) < k:
        raise ValueError(f'MCQ needs {k} distractors for {correct!r}, got {ds}')
    pick = r.sample(ds, k)
    opts = pick + [correct]
    r.shuffle(opts)
    return opts, correct


def fmt(x, dp=2):
    """Format a number without trailing zeros."""
    if isinstance(x, int):
        return f'{x:,}' if abs(x) >= 10000 else str(x)
    s = f'{x:.{dp}f}'.rstrip('0').rstrip('.')
    if s == '-0':
        s = '0'
    return s


# ---------------------------------------------------------------- curriculum loading

def load_subjects():
    p = os.path.join(CURRICULUM, 'subjects.json')
    with open(p) as f:
        return {s['id']: s for s in json.load(f)['items']}


def load_curriculum(subject_id):
    """Returns (chapters, subtopics_by_chapter). Tolerates nested or flat layouts."""
    p = os.path.join(CURRICULUM, f'{subject_id}.json')
    with open(p) as f:
        data = json.load(f)
    items = data['items'] if isinstance(data, dict) and 'items' in data else data
    chapters, subs = [], {}
    flat_subs = []

    def take(x):
        if 'subtopicIds' in x or re.search(r'-ch\d+$', x.get('id', '')):
            ch = dict(x)
            nested = ch.pop('subtopics', None)
            chapters.append(ch)
            if nested and isinstance(nested[0], dict):
                flat_subs.extend(nested)
        elif re.search(r'-st\d+$', x.get('id', '')):
            flat_subs.append(x)
        for k in ('chapters', 'subtopics'):
            if isinstance(x.get(k), list) and x[k] and isinstance(x[k][0], dict):
                for y in x[k]:
                    take(y)

    for x in items:
        take(x)
    if isinstance(data, dict) and isinstance(data.get('subtopics'), list):
        flat_subs.extend(data['subtopics'])
    chapters.sort(key=lambda c: c['order'])
    for s in flat_subs:
        subs.setdefault(s['chapterId'], {})[s['id']] = s
    out = {}
    for c in chapters:
        lst = list(subs.get(c['id'], {}).values())
        lst.sort(key=lambda s: s['order'])
        out[c['id']] = lst
    return chapters, out


# ---------------------------------------------------------------- allocation

def _allowed(C, D):
    return D in ALLOWED_D[C]


def fill_cells(n, have_c=None, have_d=None, total=None):
    """Choose n (C, D) cells that move the running mix toward the targets."""
    have_c = dict(have_c or {}); have_d = dict(have_d or {})
    total = total or n
    cells = []
    for _ in range(n):
        done = sum(have_c.values())
        # deficit relative to the size the bank will have once this cell is added
        size = done + 1
        cd = {c: C_TARGET[c] * size - have_c.get(c, 0) for c in C_TARGET}
        C = max(cd, key=lambda c: (cd[c], -int(c[1])))
        dd = {d: D_TARGET[d] * size - have_d.get(d, 0) for d in D_TARGET if _allowed(C, int(d[1]))}
        D = max(dd, key=lambda d: (dd[d], -abs(int(d[1]) - 2.5)))
        cells.append((C, int(D[1])))
        have_c[C] = have_c.get(C, 0) + 1
        have_d[D] = have_d.get(D, 0) + 1
    return cells


WEIGHT_SHARE = {'L': 0.7, 'S': 1.0, 'H': 1.4}


def allocate_chapter(subtopics, n):
    """Mastery-bank plan for one chapter: list of (subtopic, C, D, alrRole, pathIndex|None)."""
    plan = []
    paths = {s['id']: list(CHECK_PATH.get(s.get('weight', 'S'), CHECK_PATH['S'])) for s in subtopics}
    # 1) check paths, round-robin so a short chapter still covers every subtopic
    idx = 0
    while len(plan) < n and any(paths.values()):
        s = subtopics[idx % len(subtopics)]
        if paths[s['id']]:
            C, D = paths[s['id']].pop(0)
            plan.append([s, C, D, None, 'path'])
        idx += 1
    # 2) wider bank
    hc, hd = {}, {}
    for _, C, D, _, _ in plan:
        hc[C] = hc.get(C, 0) + 1; hd[f'D{D}'] = hd.get(f'D{D}', 0) + 1
    rest = fill_cells(n - len(plan), hc, hd)
    # spread wider-bank cells across subtopics by weight, cycling cell types
    rest.sort(key=lambda cd: (cd[1] not in (1, 4, 5), cd))
    load = {s['id']: sum(1 for p in plan if p[0] is s) for s in subtopics}
    for C, D in rest:
        s = min(subtopics, key=lambda s: (load[s['id']] / WEIGHT_SHARE.get(s.get('weight', 'S'), 1), s['order']))
        plan.append([s, C, D, None, 'wide'])
        load[s['id']] += 1
    rebalance_d(plan)
    # 3) ALR roles
    retained = {}
    for p in plan:
        s, C, D, _, src = p
        if is_transfer(C, D):
            p[3] = 'transfer_probe'
        elif src == 'path' and retained.get(s['id'], 0) < 2 and C in ('C1', 'C3') and D <= 2:
            p[3] = 'retention_probe'; retained[s['id']] = retained.get(s['id'], 0) + 1
        else:
            p[3] = 'practised'
    for s in subtopics:
        while retained.get(s['id'], 0) < 2:
            cand = [p for p in plan if p[0] is s and p[3] == 'practised' and p[1] in ('C1', 'C2', 'C3') and p[2] <= 3]
            if not cand:
                break
            cand.sort(key=lambda p: (p[1] == 'C2', p[2]))
            cand[0][3] = 'retention_probe'; retained[s['id']] = retained.get(s['id'], 0) + 1
    # order within chapter: subtopic order, then path first, then C, D
    plan.sort(key=lambda p: (p[0]['order'], p[4] != 'path', p[1], p[2]))
    return plan


def is_transfer(C, D):
    return (C == 'C3' and D >= 4) or (C == 'C4' and D >= 3)


def rebalance_d(plan):
    """Shift difficulty tags (keeping concept groups) so the chapter's D mix tracks the target."""
    n = len(plan)
    for _ in range(4 * n):
        cnt = {d: sum(1 for p in plan if p[2] == d) for d in range(1, 6)}
        dev = {d: cnt[d] - D_TARGET[f'D{d}'] * n for d in range(1, 6)}
        over = [d for d in dev if dev[d] > 0.75]
        under = [d for d in dev if dev[d] < -0.75]
        if not over or not under:
            return
        best = None
        for p in plan:
            if p[2] not in over:
                continue
            for d in under:
                if not _allowed(p[1], d):
                    continue
                cost = abs(d - p[2]) + (0.5 if p[4] == 'path' else 0) - 0.1 * (dev[p[2]] - dev[d])
                if best is None or cost < best[0]:
                    best = (cost, p, d)
        if best is None:
            return
        best[1][2] = best[2]


def form_blueprint(subtopics, n):
    """Parallel-form blueprint: list of (subtopic, C, D)."""
    cells = fill_cells(n)
    cells.sort(key=lambda cd: (cd[0], cd[1]))
    out = []
    load = {s['id']: 0 for s in subtopics}
    # interleave so subtopics each get a spread of C levels
    for C, D in cells:
        s = min(subtopics, key=lambda s: (load[s['id']] / WEIGHT_SHARE.get(s.get('weight', 'S'), 1), s['order']))
        out.append((s, C, D)); load[s['id']] += 1
    out.sort(key=lambda x: (x[0]['order'], x[1], x[2]))
    return out


# ---------------------------------------------------------------- gap codes

def gap_for(C, D, alr, qtype, profile):
    if alr == 'retention_probe' and C != 'C1':
        return 'G6'
    if C == 'C1':
        return 'G1'
    if C == 'C2':
        return 'G9' if (D >= 4 and profile.get('calibration')) else 'G2'
    if C == 'C3':
        if D >= 4:
            return 'G5'
        if D == 1:
            return 'G4'
        return 'G3'
    # C4
    if qtype in ('case',) and profile.get('wordy'):
        return 'G7'
    if D >= 5:
        return 'G8'
    return 'G5'


# ---------------------------------------------------------------- topic matching

STOP = set('and or of the in a an to for with on by from its their as at into is are vs'.split())


def words(s):
    return {w for w in re.findall(r'[a-z0-9]+', s.lower()) if w not in STOP and len(w) > 2}


def match_topics(subtopics, topics, chapter_name=''):
    """Map each subtopic id -> Topic, by keyword overlap; leftover by order."""
    out = {}
    used = {}
    for i, s in enumerate(subtopics):
        sw = words(s['name'])
        best, bs = None, 0.0
        for t in topics:
            score = 0.0
            for k in t.keys:
                kw = words(k)
                if not kw:
                    continue
                if k in s['name'].lower():
                    score += 3
                score += len(kw & sw) / len(kw)
            score -= 0.25 * used.get(id(t), 0)
            if score > bs:
                best, bs = t, score
        if best is None or bs <= 0.3:
            best = topics[i % len(topics)]
        out[s['id']] = best
        used[id(best)] = used.get(id(best), 0) + 1
    return out


# ---------------------------------------------------------------- generation

class Generator:
    def __init__(self, subject, chapters, subtopics, content, plan_row, profile=None):
        self.subject = subject
        self.sid = subject['id']
        self.chapters = chapters
        self.subtopics = subtopics
        self.content = content
        self.row = plan_row
        self.profile = profile or getattr(content, 'PROFILE', {})
        augment(content)
        global CTX
        try:
            from content._lib import CTX as _C
            CTX = _C
        except ImportError:
            pass
        self.seen = set()
        self.rot = {}
        self.fail = []
        self.topic_map = {}
        self.chap_sh = {}
        self.borrowed = []
        self._tmaps = {}

    # template choice ---------------------------------------------------
    def pools(self, topic, all_topics, C, D):
        allt = [t for tp in all_topics for t in tp.templates]

        def ok(t, slack):
            return t.C == C and (min(t.D) - slack) <= D <= (max(t.D) + slack)
        for pool, slack, borrowed in ((topic.templates, 0, False), (topic.templates, 1, False), (topic.templates, 9, False),
                                      (allt, 0, True), (allt, 9, True)):
            c = [t for t in pool if ok(t, slack)]
            if c:
                yield c, borrowed

    def make(self, qid, topic, all_topics, C, D, tries=40, chapter_id=None, want_marks=None, strict=False):
        lst = self.chap_sh.setdefault(chapter_id, [])
        CTX['want_marks'] = want_marks or MARKS.get((C, D), (2, 2))[0]
        for cands, borrowed in self.pools(topic, all_topics, C, D):
            key = (id(topic), C, D, len(cands))
            start = self.rot.get(key, 0)
            lim = min(tries, max(len(cands) * 3, 12))
            for attempt in range(lim):
                t = cands[(start + attempt) % len(cands)]
                r = random.Random(seed_of(self.sid, qid, attempt, len(cands)))
                try:
                    q = t.fn(r, D)
                except ValueError:
                    continue
                if q is None:
                    continue
                if strict and q.get('marks') and q['marks'] != CTX['want_marks'] and attempt < lim // 2:
                    continue
                opts = q.get('options')
                dt = q['stem'] + (' ' + ' '.join(sorted(map(str, opts))) if isinstance(opts, list) and not q['stem'].startswith('Assertion (A)') else '')
                n = norm(dt)   # same text the validator compares (stem + sorted MCQ options)
                if n in self.seen:
                    continue
                sh = shingles(n)
                if near_dup(sh, len(n), lst):
                    continue
                self.seen.add(n)
                lst.append((sh, len(n)))
                self.rot[key] = start + attempt + 1
                if borrowed:
                    self.borrowed.append((qid, C, D, topic.name))
                q['_tpl'] = t
                return q
        self.fail.append(qid)
        raise RuntimeError(f'Could not make a unique question for {qid} ({C} D{D}) in topic {topic.name}')

    def build(self, qid, s, ch, C, D, alr, set_, q):
        t = q.pop('_tpl')
        qtype = q.get('type') or t.type or DEFAULT_TYPE[C]
        if q.get('options'):
            qtype = 'mcq'
        elif qtype == 'mcq':
            qtype = 'short'
        m, mins = MARKS.get((C, D), (2, 2))
        sc = self.profile.get('mark_scale', {}).get(qtype)
        if sc:
            m, mins = max(1, round(m * sc[0])), round(mins * sc[1] * 2) / 2
        out = {
            'id': qid,
            'subtopicId': s['id'],
            'chapterId': ch['id'],
            'subjectId': self.sid,
            'conceptGroup': C,
            'difficulty': f'D{D}',
            'type': qtype,
            'stem': q['stem'],
        }
        if q.get('options'):
            out['options'] = q['options']
            assert q['answer'] in q['options'], qid
        out['answer'] = q['answer']
        out['markingKey'] = q['key']
        out['marks'] = q.get('marks', m)
        out['minutes'] = q.get('minutes', mins if 'marks' not in q else round(max(1.0, q['marks'] * 1.25) * 2) / 2)
        out['alrRole'] = alr
        out['likelyGapOnWrong'] = q.get('gap') or gap_for(C, D, alr, qtype, self.profile)
        out['set'] = set_
        return out

    def tmap(self, ch):
        if ch['id'] not in self._tmaps:
            topics = self.content.CHAPTERS[ch['order']]
            tm = match_topics(self.subtopics[ch['id']], topics, ch['name'])
            self.topic_map.update({k: v.name for k, v in tm.items()})
            self._tmaps[ch['id']] = (topics, tm)
        return self._tmaps[ch['id']]

    def chapter(self, ch):
        subs = self.subtopics[ch['id']]
        topics, tmap = self.tmap(ch)
        items = []
        # mastery bank
        nq = {}
        for s, C, D, alr, src in allocate_chapter(subs, self.row['perch']):
            nq[s['id']] = nq.get(s['id'], 0) + 1
            qid = f"{s['id']}-q{nq[s['id']]:02d}"
            q = self.make(qid, tmap[s['id']], topics, C, D, chapter_id=ch['id'])
            items.append(self.build(qid, s, ch, C, D, alr, 'mastery_bank', q))
        # practice forms
        amarks = {}
        for form in ('a', 'b'):
            for i, (s, C, D) in enumerate(form_blueprint(subs, self.row['qpt']), 1):
                qid = f"{ch['id']}-pf{form}-q{i:02d}"
                q = self.make(qid, tmap[s['id']], topics, C, D, chapter_id=ch['id'], want_marks=amarks.get(i), strict=form == 'b')
                if form == 'a':
                    amarks[i] = q.get('marks') or MARKS.get((C, D), (2, 2))[0]
                alr = 'transfer_probe' if is_transfer(C, D) else 'practised'
                items.append(self.build(qid, s, ch, C, D, alr, f'practice_form_{form}', q))
        return items

    def mocks(self):
        sections = mock_sections(self.row['pattern'], self.row['qpm'], self.profile)
        all_subs = [(ch, s) for ch in self.chapters for s in self.subtopics[ch['id']]]
        items, papers = [], []
        for m in range(1, self.row['nmock'] + 1):
            rr = random.Random(seed_of(self.sid, 'mock', m))
            order = all_subs[:]
            rr.shuffle(order)
            # spread over chapters: sort by chapter so each chapter appears, rotating offset per mock
            byc = {}
            for ch, s in order:
                byc.setdefault(ch['id'], []).append((ch, s))
            seq = []
            while any(byc.values()):
                for k in list(byc):
                    if byc[k]:
                        seq.append(byc[k].pop())
            seq = seq[(m * 3) % len(seq):] + seq[:(m * 3) % len(seq)]
            n = 0
            paper = {'mock': m, 'sections': [], 'totalMarks': 0, 'minutes': 0}
            for sec in sections:
                sec_ids = []
                for j in range(sec['count']):
                    ch, s = seq[n % len(seq)]
                    C, D = sec['cells'][j % len(sec['cells'])]
                    n += 1
                    qid = f"{self.sid}-mock{m}-q{n:02d}"
                    topics, tmap = self.tmap(ch)
                    wm, wmin = mock_marks(C, D, sec['type'], self.profile)
                    q = self.make(qid, tmap[s['id']], topics, C, D, chapter_id=ch['id'], want_marks=wm, strict=True)
                    it = self.build(qid, s, ch, C, D, 'transfer_probe' if is_transfer(C, D) else 'practised', 'mock', q)
                    if 'marks' not in q:
                        it['marks'], it['minutes'] = wm, wmin
                    items.append(it)
                    sec_ids.append(qid)
                    paper['totalMarks'] += it['marks']; paper['minutes'] += it['minutes']
                paper['sections'].append({'name': sec['name'], 'questionIds': sec_ids})
            papers.append(paper)
        equalise_mocks(items, papers)
        return items, papers


SECTION_RULES = [
    # keyword regex -> (cells, preferred type)
    (r'mcq|multiple|objective|recall|knowledge|definition|short skill|vocabulary|grammar|one-step', [('C1', 1), ('C1', 2), ('C2', 2), ('C3', 1), ('C2', 3), ('C3', 2)], 'mcq'),
    (r'short answer|short structured|short practical|structured questions|short-answer|explanation|define|listening|reading comprehension|reading items|output|language & vocabulary|textual|पाठ|व्याकरण|शब्द', [('C2', 2), ('C3', 2), ('C2', 3), ('C3', 3), ('C3', 2)], 'short'),
    (r'extended|long|essay|multi-part|composition|writing|रचना|long programs|proofs', [('C4', 3), ('C3', 4), ('C4', 4), ('C4', 3)], 'long'),
    (r'case|source|data|practical|hots|problem-solving|modelling|map|fieldwork|scenario|calculation|past-paper|directed|theory', [('C3', 3), ('C4', 3), ('C3', 4), ('C4', 4), ('C4', 5), ('C3', 3)], 'case'),
]


def equalise_mocks(items, papers):
    """Make every mock carry the same total marks by nudging simple (non-composed) items."""
    by = {p['mock']: [q for q in items if f"-mock{p['mock']}-" in q['id']] for p in papers}
    tot = {m: sum(q['marks'] for q in qs) for m, qs in by.items()}
    target = max(set(tot.values()), key=list(tot.values()).count)
    for m, qs in by.items():
        diff = target - tot[m]
        # prefer items whose key carries no part marks, then ones with a single trailing [n] (rewritten to match)
        nomark = [q for q in qs if q['type'] != 'mcq' and not re.search(r'\[\d+\]', str(q.get('markingKey', '')))]
        single = [q for q in qs if q['type'] not in ('mcq', 'long') and len(re.findall(r'\[\d+\]', str(q.get('markingKey', '')))) == 1
                  and re.search(r'\[\d+\]\s*$', str(q.get('markingKey', '')))
                  and not re.search(r'\(\d\)', str(q.get('markingKey', '')))]   # inner "(1)" points would disagree
        broad = [q for q in qs if '(a)' not in q['stem'] and q['type'] != 'mcq'] or [q for q in qs if q['type'] != 'mcq'] or qs
        for simple in (nomark + single, broad):
          i = 0
          while simple and diff != 0 and i < 10 * len(simple):
              q = simple[i % len(simple)]
              step = 1 if diff > 0 else -1
              if 1 <= q['marks'] + step <= 20:
                  q['marks'] += step
                  q['minutes'] = max(0.5, q['minutes'] + step)
                  if q in single:
                      q['markingKey'] = re.sub(r'\[\d+\]\s*$', f"[{q['marks']}]", q['markingKey'])
                  diff -= step
              i += 1
    for p in papers:
        p['totalMarks'] = sum(q['marks'] for q in by[p['mock']])
        p['minutes'] = sum(q['minutes'] for q in by[p['mock']])


def mock_marks(C, D, sec_type, profile):
    m, mins = MARKS.get((C, D), (2, 2))
    sc = profile.get('mark_scale', {}).get(sec_type)
    if sc:
        m, mins = max(1, round(m * sc[0])), round(mins * sc[1] * 2) / 2
    return m, mins


def mock_sections(pattern, qpm, profile):
    lines = [l.strip(' •\t') for l in (pattern or '').split('\n') if l.strip().startswith('•') and 'Mastery check' not in l]
    secs = []
    for l in lines:
        m = re.match(r'(\d+)\s+(.*)', l)
        if not m:
            continue
        cnt, name = int(m.group(1)), m.group(2)
        cells, typ = SECTION_RULES[2][1], 'long'
        for rx, c, t in SECTION_RULES:
            if re.search(rx, name, re.I):
                cells, typ = c, t
                break
        secs.append({'name': name, 'raw': cnt, 'cells': cells, 'type': typ})
    if not secs:
        secs = [{'name': 'Paper', 'raw': 1, 'cells': [('C2', 2), ('C3', 3), ('C4', 3)], 'type': None}]
    tot = sum(s['raw'] for s in secs)
    # largest-remainder scaling to qpm
    exact = [s['raw'] * qpm / tot for s in secs]
    base = [int(math.floor(e)) for e in exact]
    rem = qpm - sum(base)
    for i in sorted(range(len(secs)), key=lambda i: -(exact[i] - base[i]))[:rem]:
        base[i] += 1
    for s, b in zip(secs, base):
        s['count'] = b
    return [s for s in secs if s['count'] > 0]


# ---------------------------------------------------------------- writing

def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def envelope(items, **extra):
    d = {'schemaVersion': 1, 'generatedBy': GENERATED_BY, 'items': items}
    d.update(extra)
    return d


def mix(items):
    n = len(items) or 1
    c = {k: round(100 * sum(1 for q in items if q['conceptGroup'] == k) / n, 1) for k in C_TARGET}
    d = {k: round(100 * sum(1 for q in items if q['difficulty'] == k) / n, 1) for k in D_TARGET}
    return c, d
