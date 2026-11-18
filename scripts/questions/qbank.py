"""Question-bank builder shared by the subject generators (QB-CBSE; other boards may reuse it).

A subject generator describes, for every subtopic, a list of *families*. A family is one
question design with fixed tags (concept group C, difficulty D, type, gap) and a generator
function that returns a fresh variant (new numbers, names, contexts) each call. The builder:

1. builds each subtopic's student-check path (L 5, S 6, H 8 items, C1 -> C4, starting at D2),
   or takes seeded items (the class 8 maths workbook) as the check path;
2. tops each chapter up to the cost-sheet bank size, always picking the family whose C and D
   tags are furthest below the subject's target mix (C1 15, C2 30, C3 35, C4 20;
   D1 10, D2 40, D3 35, D4 12, D5 3);
3. builds practice Form A and Form B per chapter from the same blueprint: position i of
   both forms uses the same family (same subtopic, C, D) with different numbers and contexts;
4. builds the mocks from the official paper pattern (sections, marks, question kinds);
5. rejects duplicate and near-duplicate stems exactly as scripts/questions/validate.ts does;
6. writes data/questions/{subjectId}/{chapterId}.json, mocks.json and _status.json.

Variant functions take a random.Random and return a dict:
    stem, answer, key                    required (key = marking key)
    options                              optional, for a ready-made MCQ (answer must be one of them)
    distractors                          optional, wrong answers so the item can be asked as an MCQ
"""
from __future__ import annotations

import datetime as _dt
import json
import math
import os
import random
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable, Iterable

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q_DIR = os.environ.get('QB_QUESTIONS_DIR', os.path.join(ROOT, 'data', 'questions'))
CUR_DIR = os.environ.get('QB_CURRICULUM_DIR', os.path.join(ROOT, 'data', 'curriculum'))
TARGETS = os.path.join(ROOT, 'data', 'questions', 'targets.json')

C_TARGET = {'C1': .15, 'C2': .30, 'C3': .35, 'C4': .20}
D_TARGET = {'D1': .10, 'D2': .40, 'D3': .35, 'D4': .12, 'D5': .03}
DNUM = {'D1': 1, 'D2': 2, 'D3': 3, 'D4': 4, 'D5': 5}
NEAR_DUP = 0.85

# Student-check path per subtopic weight: (C, D, ALR role). Mirrors the class 8 maths workbook.
CHECK_PATH = {
    'L': [('C1', 'D2', 'retention_probe'), ('C2', 'D2', 'practised'), ('C3', 'D2', 'retention_probe'),
          ('C3', 'D3', 'practised'), ('C4', 'D3', 'transfer_probe')],
    'S': [('C1', 'D2', 'retention_probe'), ('C2', 'D2', 'practised'), ('C2', 'D3', 'practised'),
          ('C3', 'D2', 'retention_probe'), ('C3', 'D3', 'practised'), ('C4', 'D3', 'transfer_probe')],
    'H': [('C1', 'D2', 'retention_probe'), ('C2', 'D2', 'practised'), ('C2', 'D3', 'practised'),
          ('C3', 'D2', 'retention_probe'), ('C3', 'D3', 'practised'), ('C3', 'D4', 'transfer_probe'),
          ('C4', 'D3', 'transfer_probe'), ('C4', 'D4', 'transfer_probe')],
}

# Default marks and minutes by type (bank and practice forms; mocks use section marks).
TYPE_MARKS = {'mcq': (1, 1), 'short': (1, 1.5), 'explain': (2, 2), 'numerical': (2, 3),
              'multi_step': (3, 4), 'case': (4, 6), 'long': (5, 7)}


# ---------------------------------------------------------------- text utilities

def norm(s: str) -> str:
    """Same normalisation as validate.ts normaliseStem (digits kept)."""
    import re
    s = unicodedata.normalize('NFKC', s).lower()
    s = re.sub(r'\([a-d]\)', ' ', s)
    out = []
    for ch in s:
        cat = unicodedata.category(ch)
        out.append(ch if cat[0] in 'LNM' else ' ')
    return ' '.join(''.join(out).split())


def dup_text(v: dict) -> str:
    """Same as validate.ts dupText: stem plus options for MCQs, stem only for Assertion-Reason."""
    opts = v.get('options')
    if opts and not v['stem'].startswith('Assertion (A)'):
        return v['stem'] + ' ' + ' '.join(sorted(map(str, opts)))
    return v['stem']


def onorm(s: str) -> str:
    """Light normalisation for comparing MCQ options (keeps symbols such as + and −)."""
    return ' '.join(unicodedata.normalize('NFKC', str(s)).lower().split())


def shingles(n: str) -> frozenset:
    w = n.split(' ')
    if len(w) < 3:
        return frozenset([n])
    return frozenset(' '.join(w[i:i + 3]) for i in range(len(w) - 2))


def jaccard(a: frozenset, b: frozenset) -> float:
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter or 1)


def inr(n: float) -> str:
    """Indian digit grouping: 1234567 -> ₹12,34,567."""
    neg = n < 0
    n = abs(n)
    whole = int(round(n)) if float(n).is_integer() or abs(n - round(n)) < 1e-9 else None
    if whole is None:
        s = f'{n:.2f}'
        ip, dp = s.split('.')
    else:
        ip, dp = str(whole), ''
    if len(ip) > 3:
        head, tail = ip[:-3], ip[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        ip = ','.join(parts + [tail])
    return ('−' if neg else '') + '₹' + ip + ('.' + dp if dp else '')


def num(x: float, dp: int = 2) -> str:
    """Pretty number: drop trailing zeros, use the true minus sign."""
    if isinstance(x, int) or float(x).is_integer():
        s = str(int(round(x)))
    else:
        s = f'{x:.{dp}f}'.rstrip('0').rstrip('.')
    return s.replace('-', '−')


SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')


def sup(n: int) -> str:
    return str(n).translate(SUP)


# Indian names and contexts for CBSE stems.
GIRLS = ['Ananya', 'Ishita', 'Meera', 'Diya', 'Kavya', 'Saanvi', 'Riya', 'Aditi', 'Pooja', 'Sneha', 'Tanvi',
         'Nandini', 'Zoya', 'Fatima', 'Harleen', 'Lakshmi', 'Priya', 'Shreya', 'Aisha', 'Gauri', 'Mehak', 'Tara']
BOYS = ['Aarav', 'Kabir', 'Rohan', 'Vihaan', 'Arjun', 'Nikhil', 'Kunal', 'Aditya', 'Ishaan', 'Rahul', 'Siddharth',
        'Imran', 'Harpreet', 'Karthik', 'Manish', 'Dev', 'Yash', 'Farhan', 'Aryan', 'Varun', 'Sahil', 'Om']
CITIES = ['Delhi', 'Mumbai', 'Pune', 'Jaipur', 'Lucknow', 'Kochi', 'Bhopal', 'Chandigarh', 'Indore', 'Patna',
          'Nagpur', 'Surat', 'Guwahati', 'Mysuru', 'Dehradun', 'Varanasi', 'Coimbatore', 'Ranchi', 'Shimla', 'Agra']


def name(r: random.Random) -> str:
    return r.choice(GIRLS + BOYS)


def two_names(r: random.Random) -> tuple[str, str]:
    a, b = r.sample(GIRLS + BOYS, 2)
    return a, b


# ---------------------------------------------------------------- families

@dataclass
class Family:
    C: str
    D: str
    type: str
    gen: Callable[[random.Random], dict]
    gap: str | None = None
    marks: float | None = None
    minutes: float | None = None
    kinds: tuple = ()          # extra mock kinds this family serves, e.g. ('ar',) or ('case',)
    used: int = 0
    exhausted: bool = False
    st: str = ''               # subtopic id, set by the builder

    def default_gap(self) -> str:
        if self.gap:
            return self.gap
        d = DNUM[self.D]
        if self.C == 'C1':
            return 'G4' if d == 1 else 'G1'
        if self.C == 'C2':
            return 'G2'
        if self.C == 'C3':
            return 'G3' if d <= 3 else 'G5'
        return 'G5'

    def can_mcq(self) -> bool:
        return self.type == 'mcq'


def F(C, D, type_, gen, **kw) -> Family:
    return Family(C=C, D=D, type=type_, gen=gen, **kw)


# ---------------------------------------------------------------- builder

@dataclass
class Seed:
    """A ready-made item (e.g. imported from the workbook) used as part of a check path."""
    st: str
    C: str
    D: str
    type: str
    stem: str
    answer: str
    key: str
    marks: float
    minutes: float
    alr: str
    gap: str
    legacy: str | None = None
    options: list | None = None


def load_targets(subject_id: str) -> dict:
    for t in json.load(open(TARGETS, encoding='utf-8'))['items']:
        if t['subjectId'] == subject_id:
            return t
    raise SystemExit(f'No target for {subject_id}')


def load_curriculum(subject_id: str, fallback: dict | None = None) -> dict:
    """Return {'chapters': [ {id, name, subtopics:[{id,name,weight}]} ], 'source': str}."""
    path = os.path.join(CUR_DIR, f'{subject_id}.json')
    if os.path.exists(path):
        data = json.load(open(path, encoding='utf-8'))
        chapters, subtopics = {}, {}

        def walk(v):
            if isinstance(v, list):
                for x in v:
                    walk(x)
            elif isinstance(v, dict):
                i = v.get('id')
                if isinstance(i, str) and i.startswith(subject_id + '-ch'):
                    if re.search(r'-st\d+$', i):
                        subtopics[i] = v
                    else:
                        chapters[i] = v
                for x in v.values():
                    if isinstance(x, (list, dict)):
                        walk(x)
        walk(data)
        out = []
        for cid in sorted(chapters):
            ch = chapters[cid]
            st_ids = ch.get('subtopicIds') or sorted(s for s in subtopics if s.startswith(cid + '-st'))
            out.append({'id': cid, 'name': ch.get('name', ''),
                        'subtopics': [{'id': s, 'name': subtopics[s].get('name', ''), 'weight': subtopics[s].get('weight', 'S')}
                                      for s in st_ids if s in subtopics]})
        return {'chapters': out, 'source': os.path.relpath(path, ROOT)}
    if fallback is None:
        raise SystemExit(f'Curriculum file data/curriculum/{subject_id}.json not found and no fallback given')
    return {'chapters': fallback['chapters'], 'source': 'fallback (generator)'}


class Builder:
    def __init__(self, subject_id: str, generated_by: str, families: dict[str, list[Family]],
                 mock_pattern: list[tuple], seeds: dict[str, list[Seed]] | None = None,
                 fallback_curriculum: dict | None = None, seed: int | None = None,
                 mock_minutes_per_mark: float = 2.25):
        self.sid = subject_id
        self.generated_by = generated_by
        self.t = load_targets(subject_id)
        self.cur = load_curriculum(subject_id, fallback_curriculum)
        self.families = families
        self.seeds = seeds or {}
        self.mock_pattern = mock_pattern
        self.mpm = mock_minutes_per_mark
        self.r = random.Random(seed if seed is not None else subject_id)
        self.stems: dict[str, str] = {}          # normalised stem -> id
        self.ch_shingles: dict[str, list] = {}   # chapter -> [(shingles, len)]
        self.bank_c = {c: 0 for c in C_TARGET}
        self.bank_d = {d: 0 for d in D_TARGET}
        self.bank_n = 0
        self.log: list[str] = []
        for st, fams in families.items():
            for f in fams:
                f.st = st

    # ---- uniqueness

    def _fresh(self, fam: Family, ch_id: str, tries: int = 40) -> dict | None:
        lst = self.ch_shingles.setdefault(ch_id, [])
        for _ in range(tries):
            try:
                v = fam.gen(self.r)
            except (ValueError, ZeroDivisionError, IndexError):
                continue
            n = norm(dup_text(v))
            if n in self.stems:
                continue
            sh = shingles(n)
            ln = len(n)
            clash = False
            for (osh, oln) in lst:
                if min(ln, oln) / max(ln, oln) < 0.7:
                    continue
                if jaccard(sh, osh) >= NEAR_DUP:
                    clash = True
                    break
            if clash:
                continue
            v['_norm'] = n
            v['_sh'] = (sh, ln)
            return v
        fam.exhausted = True
        return None

    def _commit(self, v: dict, qid: str, ch_id: str) -> None:
        self.stems[v['_norm']] = qid
        self.ch_shingles.setdefault(ch_id, []).append(v['_sh'])

    def _item(self, fam: Family, v: dict, qid: str, ch_id: str, set_: str, alr: str,
              marks=None, minutes=None, as_mcq=False) -> dict:
        typ = fam.type
        options = v.get('options')
        answer = v['answer']
        key = v['key']
        if as_mcq and typ != 'mcq':
            options = self._mcq_options(v)
            v = dict(v, stem=_mcq_stem(v['stem']))
            typ = 'mcq'
            letter = 'abcd'[options.index(answer)]
            key = f'({letter}) {answer}. {key}' if key != answer else f'({letter}) {answer}.'
        elif typ == 'mcq':
            if not options:
                options = self._mcq_options(v)
            if not key.startswith('('):
                letter = 'abcd'[options.index(answer)]
                key = f'({letter}) {key}'
        dm, dt = TYPE_MARKS[fam.type]
        q = {
            'id': qid,
            'subtopicId': fam.st,
            'chapterId': ch_id,
            'subjectId': self.sid,
            'conceptGroup': fam.C,
            'difficulty': fam.D,
            'type': typ,
            'stem': v['stem'],
            'answer': answer,
            'markingKey': key,
            'marks': marks if marks is not None else (v.get('marks') or fam.marks or dm),
            'minutes': minutes if minutes is not None else (v.get('minutes') or fam.minutes or dt),
            'alrRole': alr,
            'likelyGapOnWrong': v.get('gap') or fam.default_gap(),
            'set': set_,
        }
        if options:
            q['options'] = options
        fam.used += 1
        return q

    def _mcq_options(self, v: dict) -> list:
        ans = v['answer']
        ds = []
        seen = {onorm(ans)}
        for d in v.get('distractors', []):
            nd = onorm(str(d))
            if nd and nd not in seen:
                ds.append(str(d))
                seen.add(nd)
            if len(ds) == 3:
                break
        if len(ds) < 3:
            raise ValueError(f'not enough distractors for MCQ: {v["stem"][:60]}')
        opts = ds + [ans]
        self.r.shuffle(opts)
        return opts

    # ---- tag balancing

    def _score(self, fam: Family, c_cnt, d_cnt, n) -> float:
        n1 = n + 1
        return (C_TARGET[fam.C] * n1 - c_cnt[fam.C]) + (D_TARGET[fam.D] * n1 - d_cnt[fam.D])

    def _pick(self, fams: list[Family], c_cnt, d_cnt, n, st_use: dict, weights: dict) -> Family | None:
        live = [f for f in fams if not f.exhausted]
        if not live:
            return None
        best, best_s = None, -1e9
        for f in live:
            s = self._score(f, c_cnt, d_cnt, n)
            s -= 0.35 * st_use.get(f.st, 0) / weights.get(f.st, 1)   # spread across subtopics
            s -= 0.15 * f.used                                         # spread across families
            s += self.r.random() * 0.05
            if s > best_s:
                best, best_s = f, s
        return best

    def _closest(self, fams: list[Family], C: str, D: str) -> Family | None:
        live = [f for f in fams if not f.exhausted]
        same_c = [f for f in live if f.C == C]
        pool = same_c or live
        if not pool:
            return None
        return min(pool, key=lambda f: (abs(DNUM[f.D] - DNUM[D]) + (0 if f.C == C else 3), f.used, self.r.random()))

    # ---- build

    def build(self) -> dict:
        t = self.t
        chapters = self.cur['chapters']
        if len(chapters) != t['chapters']:
            raise SystemExit(f'{self.sid}: curriculum has {len(chapters)} chapters, cost sheet {t["chapters"]}')
        files = {}
        practice_c = {c: 0 for c in C_TARGET}
        practice_d = {d: 0 for d in D_TARGET}
        practice_n = 0
        for ch in chapters:
            cid = ch['id']
            bank: list[dict] = []
            per_st: dict[str, list[dict]] = {s['id']: [] for s in ch['subtopics']}
            weights = {s['id']: {'L': 5, 'S': 6, 'H': 8}[s['weight']] for s in ch['subtopics']}
            ch_fams = [f for s in ch['subtopics'] for f in self.families.get(s['id'], [])]
            for s in ch['subtopics']:
                if not self.families.get(s['id']):
                    raise SystemExit(f'{s["id"]}: no families defined')
            # 1. check path
            for s in ch['subtopics']:
                sid = s['id']
                if sid in self.seeds:
                    for sd in self.seeds[sid]:
                        qid = f'{sid}-q{len(per_st[sid]) + 1:02d}'
                        n = norm(dup_text({'stem': sd.stem, 'options': sd.options}))
                        if n in self.stems:
                            raise SystemExit(f'duplicate seeded stem {qid}')
                        self.stems[n] = qid
                        self.ch_shingles.setdefault(cid, []).append((shingles(n), len(n)))
                        q = {'id': qid, 'subtopicId': sid, 'chapterId': cid, 'subjectId': self.sid,
                             'conceptGroup': sd.C, 'difficulty': sd.D, 'type': sd.type, 'stem': sd.stem,
                             'answer': sd.answer, 'markingKey': sd.key, 'marks': sd.marks, 'minutes': sd.minutes,
                             'alrRole': sd.alr, 'likelyGapOnWrong': sd.gap, 'set': 'mastery_bank'}
                        if sd.legacy:
                            q = {'id': qid, 'legacyId': sd.legacy, **{k: v for k, v in q.items() if k != 'id'}}
                        if sd.options:
                            q['options'] = sd.options
                        per_st[sid].append(q)
                        self._count_bank(sd.C, sd.D)
                    continue
                fams = self.families[sid]
                for (C, D, alr) in CHECK_PATH[s['weight']]:
                    v, fam = None, None
                    for _ in range(len(fams)):
                        fam = self._closest(fams, C, D)
                        if fam is None:
                            break
                        v = self._fresh(fam, cid)
                        if v:
                            break
                    if not v:
                        raise SystemExit(f'{sid}: families exhausted on check path')
                    qid = f'{sid}-q{len(per_st[sid]) + 1:02d}'
                    role = alr
                    if role == 'transfer_probe' and not _transfer_ok(fam.C, fam.D):
                        role = 'practised'
                    if role == 'practised' and _transfer_ok(fam.C, fam.D):
                        role = 'transfer_probe'
                    q = self._item(fam, v, qid, cid, 'mastery_bank', role)
                    self._commit(v, qid, cid)
                    per_st[sid].append(q)
                    self._count_bank(fam.C, fam.D)
            # 2. wider bank
            have = sum(len(x) for x in per_st.values())
            st_use = {k: len(v) for k, v in per_st.items()}
            while have < t['bankPerChapter']:
                fam = self._pick(ch_fams, self.bank_c, self.bank_d, self.bank_n, st_use, weights)
                if fam is None:
                    raise SystemExit(f'{cid}: all families exhausted at {have} bank items')
                v = self._fresh(fam, cid)
                if not v:
                    continue
                sid = fam.st
                qid = f'{sid}-q{len(per_st[sid]) + 1:02d}'
                role = 'transfer_probe' if _transfer_ok(fam.C, fam.D) else 'practised'
                q = self._item(fam, v, qid, cid, 'mastery_bank', role)
                self._commit(v, qid, cid)
                per_st[sid].append(q)
                st_use[sid] = st_use.get(sid, 0) + 1
                self._count_bank(fam.C, fam.D)
                have += 1
            for s in ch['subtopics']:
                bank.extend(per_st[s['id']])
            # 3. practice forms (parallel)
            n_form = t['questionsPerForm']
            forms_a, forms_b = [], []
            st_use_p: dict[str, int] = {}
            for fam in ch_fams:
                fam.exhausted = False
            pos = 0
            guard = 0
            while pos < n_form:
                guard += 1
                if guard > 50 * n_form:
                    raise SystemExit(f'{cid}: could not build parallel practice forms')
                fam = self._pick(ch_fams, practice_c, practice_d, practice_n, st_use_p, weights)
                if fam is None:
                    raise SystemExit(f'{cid}: families exhausted building forms')
                va = self._fresh(fam, cid)
                if not va:
                    continue
                qa = f'{cid}-pfa-q{pos + 1:02d}'
                self._commit(va, qa, cid)
                vb = self._fresh(fam, cid)
                if not vb:
                    # roll back A
                    del self.stems[va['_norm']]
                    self.ch_shingles[cid].remove(va['_sh'])
                    fam.exhausted = True
                    continue
                qb = f'{cid}-pfb-q{pos + 1:02d}'
                self._commit(vb, qb, cid)
                forms_a.append(self._item(fam, va, qa, cid, 'practice_form_a', 'practised'))
                forms_b.append(self._item(fam, vb, qb, cid, 'practice_form_b', 'practised'))
                practice_c[fam.C] += 1
                practice_d[fam.D] += 1
                practice_n += 1
                st_use_p[fam.st] = st_use_p.get(fam.st, 0) + 1
                pos += 1
            for fam in ch_fams:
                fam.exhausted = False
            files[cid] = bank + forms_a + forms_b
        files['mocks'] = self._mocks(chapters)
        return files

    def _count_bank(self, C, D):
        self.bank_c[C] += 1
        self.bank_d[D] += 1
        self.bank_n += 1

    def _mocks(self, chapters) -> list[dict]:
        """mock_pattern: list of (count, marks, kind) where kind is mcq | ar | short | long | case | any type name."""
        items = []
        total_q = sum(c for c, _, _ in self.mock_pattern)
        if total_q != self.t['questionsPerMock']:
            raise SystemExit(f'mock pattern has {total_q} questions, cost sheet {self.t["questionsPerMock"]}')
        ch_ids = [c['id'] for c in chapters]
        fams_by_ch = {c['id']: [f for s in c['subtopics'] for f in self.families.get(s['id'], [])] for c in chapters}
        for m in range(1, self.t['mocks'] + 1):
            order = ch_ids[:]
            self.r.shuffle(order)
            k = 0
            n = 0
            for (count, marks, kind) in self.mock_pattern:
                for _ in range(count):
                    n += 1
                    qid = f'{self.sid}-mock{m}-q{n:02d}'
                    done = False
                    for attempt in range(len(order) * 2):
                        cid = order[(k + attempt) % len(order)]
                        cands = [f for f in fams_by_ch[cid] if _fits(f, kind)]
                        self.r.shuffle(cands)
                        cands.sort(key=lambda f: f.used)
                        for fam in cands[:6]:
                            v = self._fresh(fam, cid, tries=15)
                            fam.exhausted = False
                            if not v:
                                continue
                            as_mcq = kind in ('mcq',) and fam.type != 'mcq'
                            if as_mcq and not v.get('distractors'):
                                continue
                            try:
                                q = self._item(fam, v, qid, cid, 'mock', 'practised', marks=marks,
                                               minutes=round(marks * self.mpm, 1), as_mcq=as_mcq)
                            except ValueError:
                                continue
                            self._commit(v, qid, cid)
                            items.append(q)
                            done = True
                            break
                        if done:
                            k = (k + attempt + 1) % len(order)
                            break
                    if not done:
                        raise SystemExit(f'mock{m} q{n}: no family fits kind {kind}')
        return items

    # ---- output

    def write(self, files: dict, accuracy: list | None = None) -> None:
        out_dir = os.path.join(Q_DIR, self.sid)
        os.makedirs(out_dir, exist_ok=True)
        for name, items in files.items():
            items = [{k: v for k, v in q.items() if not k.startswith('_')} for q in items]
            with open(os.path.join(out_dir, f'{name if name == "mocks" else name}.json'), 'w', encoding='utf-8') as fh:
                json.dump({'schemaVersion': 1, 'generatedBy': self.generated_by, 'items': items}, fh,
                          ensure_ascii=False, indent=1)
                fh.write('\n')
        st_path = os.path.join(out_dir, '_status.json')
        prev = json.load(open(st_path, encoding='utf-8')) if os.path.exists(st_path) else {}
        prev.update({
            'subjectId': self.sid,
            'generatedBy': self.generated_by,
            'curriculumSource': self.cur['source'],
            'generatedAt': _dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'chaptersDone': [k for k in files if k != 'mocks'],
            'mocksDone': 'mocks' in files,
            'target': self.t['total'],
            'generated': sum(len(v) for v in files.values()),
        })
        if accuracy is not None:
            prev['accuracyChecks'] = accuracy
        prev.setdefault('validated', False)
        with open(st_path, 'w', encoding='utf-8') as fh:
            json.dump(prev, fh, ensure_ascii=False, indent=2)
            fh.write('\n')


_INSTR = re.compile(r'\s*(Justify( your answer)?|Explain( why)?|Show (your|the) (method|working|test you use)|Give a reason|Show how you narrowed the search)\.?\s*$', re.I)


def _mcq_stem(stem: str) -> str:
    """Drop a trailing 'Justify.' / 'Explain.' when a written item is asked as an MCQ."""
    return _INSTR.sub('', stem).strip()


def _transfer_ok(C: str, D: str) -> bool:
    d = DNUM[D]
    return (C == 'C3' and d >= 4) or (C == 'C4' and d >= 3)


def _fits(f: Family, kind: str) -> bool:
    if kind in f.kinds:
        return True
    if kind == 'mcq':
        if 'ar' in f.kinds:
            return False
        return f.type == 'mcq' or (f.type in ('short', 'numerical') and DNUM[f.D] <= 3 and f.C in ('C1', 'C2', 'C3'))
    if kind == 'ar':
        return 'ar' in f.kinds
    if kind == 'short':
        return f.type in ('short', 'explain', 'numerical') and f.C in ('C2', 'C3')
    if kind == 'short3':
        return f.type in ('explain', 'numerical', 'multi_step') and DNUM[f.D] >= 2
    if kind == 'long':
        return f.type in ('multi_step', 'long') or (f.C == 'C4' and f.type != 'mcq')
    if kind == 'case':
        return f.type == 'case' or 'case' in f.kinds
    return f.type == kind


# ---------------------------------------------------------------- distractor helpers

def num_distractors(ans: float, *cands, dp: int = 2) -> list[str]:
    """Format candidate wrong answers, dropping any equal to the answer; pad with nearby values."""
    out = []
    seen = {num(ans, dp)}
    for c in list(cands) + [ans + 1, ans - 1, ans * 2, ans + 10, ans / 2 if ans else 3, ans + 2]:
        s = num(c, dp)
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out


def pick_others(r: random.Random, pool: Iterable, exclude, k: int = 3) -> list:
    pool = [p for p in pool if p != exclude]
    return r.sample(pool, k)


# ---------------------------------------------------------------- common item shapes

AR_OPTIONS = [
    'Both A and R are true, and R is the correct explanation of A.',
    'Both A and R are true, but R is not the correct explanation of A.',
    'A is true, but R is false.',
    'A is false, but R is true.',
]


def ar(assertion: str, reason: str, code: str, why: str) -> dict:
    """Assertion-Reason item in the CBSE format. code is 'a', 'b', 'c' or 'd'."""
    i = 'abcd'.index(code)
    return {
        'stem': f'Assertion (A): {assertion}\nReason (R): {reason}\nChoose the correct option.',
        'options': AR_OPTIONS[:],
        'answer': AR_OPTIONS[i],
        'key': f'({code}) {why}',
    }


def mcq(stem: str, correct: str, wrong: list, key: str, r: random.Random) -> dict:
    opts = [correct] + list(wrong)[:3]
    if len({onorm(o) for o in opts}) != 4:
        raise ValueError(f'MCQ options not distinct: {opts}')
    r.shuffle(opts)
    return {'stem': stem, 'options': opts, 'answer': correct, 'key': key}


def frac(n: int, d: int) -> str:
    from math import gcd
    if d < 0:
        n, d = -n, -d
    g = gcd(abs(n), abs(d)) or 1
    n //= g
    d //= g
    s = f'{abs(n)}' if d == 1 else f'{abs(n)}/{d}'
    return ('−' if n < 0 else '') + s


def factorise(n: int) -> dict:
    out, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def fstr(f: dict) -> str:
    return ' × '.join(f'{p}{sup(e)}' if e > 1 else f'{p}' for p, e in sorted(f.items()))
