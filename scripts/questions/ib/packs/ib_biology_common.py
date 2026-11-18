"""Shared helpers for the IB DP Biology packs (ib-g11-biology, ib-g12-biology; first assessment 2025).

Exam model mirrored in the mocks (HL, data/questions/targets.json examPattern):
  Paper 1A  40 multiple-choice questions                                   40 marks
  Paper 1B  4 data-based questions on experimental work                    35 marks (3 x 9 + 1 x 8)
  Paper 2A  1 data-based question + 6 short-answer structured questions    48 marks (12 + 6 x 6)
  Paper 2B  2 extended-response questions (of 3)                           32 marks (2 x 16)
                                                                            -> 53 items, 155 marks
Data-based items are parametric: each generator returns an introduction (data table / scenario) and a list
of parts (question, answer, markscheme, marks) with computed answers; the wrapper picks a subset of parts whose
marks add up exactly to the mark value the paper section needs.
"""
from __future__ import annotations

import itertools
import math
import random
import re

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
from engine import Slot

CONFIG = {'minutesPerMark': 1.6, 'mcqMinutes': 1.5}

MOCK = [
    dict(section='Paper 1A – multiple-choice questions', count=40, c=['C1', 'C2', 'C1', 'C3', 'C2'], d=[2, 3, 2, 3, 2], type='mcq', marks=1),
    dict(section='Paper 1B – data-based questions on experimental work (questions 1–3)', count=3, c=['C3', 'C4'], d=[3, 4], type='case', marks=9, style='p1b'),
    dict(section='Paper 1B – data-based questions on experimental work (question 4)', count=1, c=['C3'], d=[3], type='case', marks=8, style='p1b'),
    dict(section='Paper 2 Section A – data-based question', count=1, c=['C4'], d=[4], type='case', marks=12, style='p1b'),
    dict(section='Paper 2 Section A – short-answer and structured questions', count=6, c=['C3', 'C4'], d=[3, 4, 3], type='multi_step', marks=6, style='p2'),
    dict(section='Paper 2 Section B – extended-response questions', count=2, c=['C4'], d=[4, 5], type='long', marks=16, style='p2x'),
]

MARKBAND = ('Markscheme points: award 1 mark for each valid, relevant point up to the maximum; points must be linked and '
            'explained, not listed. A clear, well-structured response with correct biological terminology and a conclusion '
            'that follows from the argument is required for full marks.')
STYLE = {'eval_marks': 7, 'essay_marks': 8, 'markband': MARKBAND}

CHI_CRIT = {1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07, 6: 12.59}
T_CRIT = {4: 2.78, 5: 2.57, 6: 2.45, 7: 2.36, 8: 2.31, 9: 2.26, 10: 2.23, 11: 2.20, 12: 2.18, 13: 2.16, 14: 2.14,
          15: 2.13, 16: 2.12, 17: 2.11, 18: 2.10, 19: 2.09, 20: 2.09, 22: 2.07, 24: 2.06, 26: 2.06, 28: 2.05, 30: 2.04}


def pick(rng, seq):
    return seq[rng.randrange(len(seq))]


def sf(x, n=3):
    """x to n significant figures; scientific notation with superscripts outside 10^-3 .. 10^5."""
    if x == 0:
        return '0'
    mag = math.floor(math.log10(abs(x)))
    xr = round(x, -mag + n - 1)
    if xr == 0:
        return '0'
    mag = math.floor(math.log10(abs(xr)))
    if -3 <= mag < 5:
        dec = max(0, n - 1 - mag)
        return f'{xr:.{dec}f}'
    m_ = xr / 10 ** mag
    return f'{m_:.{n - 1}f} × 10{sup(mag)}'


def dp(x, k=1):
    return f'{x:.{k}f}'


def mean(xs):
    return sum(xs) / len(xs)


def sd(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def pct_change(a, b):
    return 100 * (b - a) / a


def signed(x, k=1):
    return f'+{x:.{k}f}' if x > 0 else f'{x:.{k}f}'


def num(stem, ans, key, marks=2, type='numerical', gap=None):
    d = dict(stem=stem, answer=ans, markingKey=key, marks=marks, type=type)
    if gap:
        d['gap'] = gap
    return d


def nmcq(rng, stem, correct, wrongs, key):
    """MCQ with already-formatted options; drops duplicates of the correct answer."""
    ws = []
    for w in wrongs:
        if w != correct and w not in ws:
            ws.append(w)
    if len(ws) < 3:
        return None
    return mcq(rng, stem, correct, ws[:3], key)


def table(headers, rows):
    head = ' | '.join(headers)
    return head + '\n' + '\n'.join(' | '.join(str(c) for c in r) for r in rows)


# ---------------------------------------------------------------------------------------------
# Subtopic registration
# ---------------------------------------------------------------------------------------------
def topic(R, key, mc2=(), mc3=(), **kw):
    """Register a fact pack for a subtopic plus C2 / C3 multiple-choice lists (stem, correct, [3 wrong], why)."""
    R.facts(key, F(**kw))
    if mc2:
        R.mcqs(key, 'C2', (1, 4), list(mc2))
    if mc3:
        R.mcqs(key, 'C3', (2, 5), list(mc3))


def data_q(R, key, gen, c=('C3', 'C4'), d=(2, 5), name_=None):
    """Data-based question (Paper 1B / Paper 2 Section A). gen(rng, slot) -> (intro, parts) or None,
    parts = [(question, answer, markscheme, marks)]. Part 1 (reading the data) is always kept."""
    def fn(rng, slot):
        r = gen(rng, slot)
        if r is None:
            return None
        intro, parts = r
        target = slot.marks if (slot.marks and slot.set == 'mock') else None
        if target:
            idx = list(range(1, len(parts)))
            combos = []
            for k in range(len(idx), -1, -1):
                for comb in itertools.combinations(idx, k):
                    if parts[0][3] + sum(parts[i][3] for i in comb) == target:
                        combos.append((0,) + comb)
                if combos:
                    break
            if not combos:
                return None
            chosen = [parts[i] for i in pick(rng, combos)]
        else:
            n = {1: 2, 2: 2, 3: 3, 4: 4, 5: len(parts)}[slot.d]
            chosen = parts[:max(2, min(n, len(parts)))]
        letters = 'abcdefghij'
        stem = intro.strip() + '\n\n' + '\n'.join(f'({letters[i]}) {q} [{m}]' for i, (q, a, k, m) in enumerate(chosen))
        ans = ' '.join(f'({letters[i]}) {a}' for i, (q, a, k, m) in enumerate(chosen))
        key_ = ' '.join(f'({letters[i]}) [{m}] {k}' for i, (q, a, k, m) in enumerate(chosen))
        return dict(stem=stem, answer=ans, markingKey=key_, type='case', marks=sum(p[3] for p in chosen), gap='G7')
    R.t.setdefault(key, []).append(T(c, d, fn, 'case', 'p1b', name_ or gen.__name__))
    return gen


# ---------------------------------------------------------------------------------------------
# Paper 2 composites (only used to fill mock sections)
# ---------------------------------------------------------------------------------------------
def _part(rng, tpls, c, d, used, slot):
    pool = [t for t in tpls if (c in (t.c if isinstance(t.c, tuple) else (t.c,))) and t.type != 'mcq'
            and t.style is None and t.name not in used and t.d[0] <= d <= t.d[1] + 1]
    rng.shuffle(pool)
    for t in pool[:8]:
        try:
            out = t.fn(rng, Slot(slot.subtopic, slot.chapter, c, d, set='part'))
        except IndexError:
            out = None
        if out and out.get('type') != 'mcq' and not out.get('options') and len(out['stem']) < 900:
            used.add(t.name)
            return out
    return None


GENERIC = [r'\s*1 mark for identifying the error, 1-2 marks for the correct explanation\.',
           r'\s*One mark for a correct account of each side; further marks for making the difference explicit \(not two separate definitions\)\.',
           r'\s*Award full marks only if the defining feature is clear; a vague example alone scores 0\.',
           r'\s*\(\d+ marks?: one for each linked point in the chain of reasoning; no marks for assertion without explanation\.\)']


def _fix_marks(key, m_):
    for g in GENERIC:
        key = re.sub(g, '', key)
    key = re.sub(r'^1 mark for the core idea: ', '', key)
    return key.strip() + f' Award up to {m_} mark{"s" if m_ > 1 else ""} for valid, linked points.'


def composite(st, tpls, spec, style):
    def fn(rng, slot):
        if slot.set != 'mock':
            return None
        used = set()
        parts = []
        for c, d, m_ in spec:
            p = _part(rng, tpls, c, d, used, slot)
            if p is None:
                return None
            parts.append((p, m_))
        stems = [p['stem'] for p, _ in parts]
        if len(set(stems)) < len(stems):
            return None
        intro = f'This question is about {topic_name(st)}.'
        letters = 'abcdef'
        stem = intro + '\n\n' + '\n\n'.join(f'({letters[i]}) {p["stem"]} [{m_}]' for i, (p, m_) in enumerate(parts))
        ans = ' '.join(f'({letters[i]}) {p["answer"]}' for i, (p, m_) in enumerate(parts))
        key = ' '.join(f'({letters[i]}) [{m_}] {_fix_marks(p["markingKey"], m_)}' for i, (p, m_) in enumerate(parts))
        return dict(stem=stem, answer=ans, markingKey=key, type='multi_step' if style == 'p2' else 'long',
                    marks=sum(m_ for _, m_ in parts), gap='G5')
    return fn


P2_SPECS = [
    [('C1', 2, 1), ('C2', 2, 2), ('C3', 3, 3)],
    [('C2', 2, 2), ('C3', 3, 4)],
    [('C1', 2, 2), ('C2', 3, 4)],
    [('C2', 2, 3), ('C3', 3, 3)],
]
P2X_SPECS = [
    [('C2', 3, 4), ('C3', 3, 5), ('C4', 4, 7)],
    [('C2', 3, 4), ('C2', 4, 5), ('C4', 4, 7)],
    [('C1', 2, 3), ('C3', 4, 6), ('C4', 4, 7)],
]


MISC_STEMS = ['Which statement about {t} is not correct?', 'Which of the following statements about {t} is false?',
              'Which of these statements about {t} contains a misconception?',
              'Three of these statements about {t} are correct. Which one is incorrect?',
              'A student’s revision notes on {t} contain four statements. Which statement is wrong?']


def _clause(s):
    s = s.split(';')[0].strip().rstrip('.')
    return s[0].upper() + s[1:] + '.'


def topic_name(st):
    t = re.sub(r'^[A-D]\d(\.\d)?(-[A-D]\d\.\d)?\s+', '', st['name'])
    t = re.sub(r'\s*\((HL|HL-relevant)\)', '', t)
    return t[0].lower() + t[1:]


def auto_mcqs(R, st):
    """C2 'which statement is incorrect' items from misconceptions, C3 'which concept does this example illustrate' items from cases."""
    key = st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]
    ch = key.split('-')[0]
    f = R.f.get(key)
    out = []
    if f is None:
        return out
    t = topic_name(st)
    if f.misc:
        trues = ([_clause(fix) for _, fix in f.misc] + [_clause(d) for _, _, d in f.contrast]
                 + [f'{tt[0].upper() + tt[1:]} is {dd}.' for tt, dd in f.terms])

        def misc_mcq(rng, slot):
            if slot.set != 'mock':  # reserved for Paper 1A in the mocks
                return None
            i = rng.randrange(len(f.misc))
            if i >= len(MISC_STEMS):
                return None
            claim, fix = f.misc[i]
            pool = [x for j, x in enumerate(trues) if j != i and len(x) < 260]
            if len(pool) < 3:
                return None
            return mcq(rng, MISC_STEMS[i].format(t=t), claim, rng.sample(pool, 3), f'The incorrect statement is “{claim}” – {fix}')
        out.append(T('C2', (1, 4), misc_mcq, 'mcq', None, 'misc_mcq'))
    others = [c for k, ff in R.f.items() if k.startswith(ch + '-') and k != key for c in ff.cases]
    if f.cases and len({c[2] for c in others}) >= 3:
        def case_mcq(rng, slot):
            if slot.set != 'mock':
                return None
            case, what, concept, how = pick(rng, f.cases)
            wr = rng.sample(sorted({c[2] for c in others if c[2] != concept}), 3)
            stem = f'{what} Which concept is best illustrated by this example ({case})?'
            return mcq(rng, stem, concept[0].upper() + concept[1:], [w[0].upper() + w[1:] for w in wr], how)
        out.append(T('C3', (1, 5), case_mcq, 'mcq', None, 'case_mcq'))
    return out


def make_templates(R):
    cache: dict = {}

    def templates(st):
        if st['id'] in cache:
            return cache[st['id']]
        base = R.build(st, STYLE) + auto_mcqs(R, st)
        out = list(base)
        if not any(t.style == 'p1b' for t in base):
            ch = st['id'].rsplit('-', 2)[-2]
            for k2, ts in R.t.items():
                if k2.startswith(ch + '-'):
                    out += [t for t in ts if t.style == 'p1b']
        for i, spec in enumerate(P2_SPECS):
            out.append(T(('C3', 'C4'), (3, 5), composite(st, base, spec, 'p2'), 'multi_step', 'p2', f'p2_{i}'))
        for i, spec in enumerate(P2X_SPECS):
            out.append(T('C4', (3, 5), composite(st, base, spec, 'p2x'), 'long', 'p2x', f'p2x_{i}'))
        cache[st['id']] = out
        return out
    return templates


# ---------------------------------------------------------------------------------------------
# Generic quantitative factories
# ---------------------------------------------------------------------------------------------
def pct_items(R, key, ctxs, c='C3', d=(1, 4)):
    """Percentage change. ctxs: (sentence with {a} and {b}, unit, lo, hi, rel_lo, rel_hi, dp, meaning)."""
    def fn(rng, slot):
        s, unit, lo, hi, rlo, rhi, k, meaning = pick(rng, ctxs)
        a = round(rng.uniform(lo, hi), k)
        b = round(a * (1 + rng.uniform(rlo, rhi)), k)
        if a == b or a == 0:
            return None
        p = pct_change(a, b)
        text = s.format(a=f'{a:.{k}f}', b=f'{b:.{k}f}', u=unit)
        if slot.d <= 2 or slot.type == 'mcq':
            stem = f'{text} Calculate the percentage change.'
            ans = f'{signed(p)} %'
            if slot.type == 'mcq' or rng.random() < 0.3:
                wr = [f'{signed(-p)} %', f'{signed(100 * (b - a) / b)} %', f'{signed(p / 10)} %', f'{signed(p * 10)} %']
                return nmcq(rng, f'{text} What is the percentage change?', ans, wr,
                            f'% change = (final − initial)/initial × 100 = ({b:.{k}f} − {a:.{k}f})/{a:.{k}f} × 100 = {signed(p)} %.')
            return num(stem, ans, f'(final − initial)/initial × 100 = ({b:.{k}f} − {a:.{k}f})/{a:.{k}f} × 100 (M1) = {signed(p)} % (A1); sign/direction required.', 2)
        stem = f'{text} Calculate the percentage change and suggest a biological explanation for it.'
        return num(stem, f'{signed(p)} %; {meaning}',
                   f'% change = ({b:.{k}f} − {a:.{k}f})/{a:.{k}f} × 100 (M1) = {signed(p)} % (A1). Explanation (R1): {meaning}', 3)
    R.t.setdefault(key, []).append(T(c, d, fn, 'numerical', None, 'pct_items'))


def mean_sd_items(R, key, ctxs, c='C3', d=(2, 5)):
    """Mean and sample standard deviation of replicate measurements.
    ctxs: (setup sentence, quantity, unit, lo, hi, rel_spread, dp)"""
    def fn(rng, slot):
        s, qty, unit, lo, hi, spread, k = pick(rng, ctxs)
        n = 5 if slot.d <= 3 else 6
        mu = rng.uniform(lo, hi)
        xs = [round(rng.gauss(mu, mu * spread), k) for _ in range(n)]
        if len(set(xs)) < n - 1 or min(xs) <= 0:
            return None
        m, s_ = mean(xs), sd(xs)
        vals = ', '.join(f'{x:.{k}f}' for x in xs)
        who = name(rng)
        if slot.d <= 3:
            stem = f'{who} {s} The values of {qty} ({unit}) were: {vals}. Calculate the mean and the standard deviation.'
            return num(stem, f'mean = {m:.{k + 1}f} {unit}; SD = {s_:.{k + 1}f} {unit}',
                       f'Mean = Σx/n = {sum(xs):.{k}f}/{n} = {m:.{k + 1}f} {unit} (A1); SD (sample, n − 1) = {s_:.{k + 1}f} {unit} (A1). Accept population SD {math.sqrt(sum((x - m) ** 2 for x in xs) / n):.{k + 1}f}.', 2)
        cv = 100 * s_ / m
        stem = (f'{who} {s} The values of {qty} ({unit}) were: {vals}. (a) Calculate the mean and standard deviation. '
                f'(b) Express the standard deviation as a percentage of the mean and comment on the reliability of the data.')
        return num(stem, f'(a) mean = {m:.{k + 1}f} {unit}, SD = {s_:.{k + 1}f} {unit}; (b) {cv:.1f} % – ' + ('low variability, the mean is reliable.' if cv < 10 else 'considerable variability; more repeats are needed for a reliable mean.'),
                   f'(a) mean {m:.{k + 1}f} (A1), SD {s_:.{k + 1}f} (A1); (b) SD/mean × 100 = {cv:.1f} % (A1); comment: small SD relative to mean = data clustered/reliable; large = spread/less reliable (R1).', 4)
    R.t.setdefault(key, []).append(T(c, d, fn, 'numerical', None, 'mean_sd'))


def chi_assoc(o):
    """2x2 contingency chi-squared for association. o = [[a, b], [c, d]]. Returns (expected, chi2)."""
    rows = [sum(r) for r in o]
    cols = [o[0][0] + o[1][0], o[0][1] + o[1][1]]
    n = sum(rows)
    e = [[rows[i] * cols[j] / n for j in range(2)] for i in range(2)]
    chi = sum((o[i][j] - e[i][j]) ** 2 / e[i][j] for i in range(2) for j in range(2))
    return e, chi


def chi_gof(obs, ratio):
    n = sum(obs)
    tot = sum(ratio)
    e = [n * r / tot for r in ratio]
    chi = sum((o - x) ** 2 / x for o, x in zip(obs, e))
    return e, chi


def simpson(ns):
    """IB Simpson's reciprocal index D = N(N − 1) / Σ n(n − 1)."""
    N = sum(ns)
    den = sum(n * (n - 1) for n in ns)
    return N * (N - 1) / den if den else None


def welch_t(a, b):
    ma, mb = mean(a), mean(b)
    va, vb = sd(a) ** 2, sd(b) ** 2
    return (ma - mb) / math.sqrt(va / len(a) + vb / len(b))


def pooled_t(a, b):
    na, nb = len(a), len(b)
    sp2 = ((na - 1) * sd(a) ** 2 + (nb - 1) * sd(b) ** 2) / (na + nb - 2)
    return (mean(a) - mean(b)) / math.sqrt(sp2 * (1 / na + 1 / nb))


def pearson(x, y):
    mx, my = mean(x), mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy)


def interp_zero(xs, ys):
    """x where y crosses zero by linear interpolation between the bracketing points."""
    for (x1, y1), (x2, y2) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if y1 == 0:
            return x1
        if (y1 > 0) != (y2 > 0):
            return x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
    return None
