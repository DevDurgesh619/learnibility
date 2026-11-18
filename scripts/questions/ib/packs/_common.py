"""Shared helpers for IB content packs.

A pack module exposes:
    CONFIG = {'minutesPerMark': 1.2, 'mcqMinutes': 1.5}
    MOCK = [ {section, count, c, d, type?, marks?, style?}, ... ]   # one paper; counts sum to questionsPerMock
    def init(subject_id): ...                                        # optional set-up
    def templates(subtopic) -> list[T]

Most packs describe each subtopic with a fact pack `F(...)` (authored content) and let
`fact_templates()` turn it into IB-style items across C1-C4 using the IB command terms
(define, state, identify, outline, describe, explain, distinguish, analyse, compare,
evaluate, discuss, to what extent). Quantitative packs add parametric templates (`T`) that
compute their own answers, so numbers vary between items and every answer is checked.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from fractions import Fraction

from engine import T  # noqa: F401  (re-exported for packs)

NAMES = ['Amara', 'Lukas', 'Sofia', 'Kenji', 'Priya', 'Mateo', 'Chloé', 'Omar', 'Ingrid', 'Tomás', 'Aiko',
         'Nia', 'Yusuf', 'Elena', 'Kwame', 'Mei', 'Lars', 'Zara', 'Diego', 'Hana', 'Felix', 'Leila', 'Arjun',
         'Freya', 'Mohammed', 'Isabel', 'Jonas', 'Ana', 'Rafael', 'Sana', 'Noah', 'Alessia', 'Tariq', 'Maya']
CITIES = ['Geneva', 'Singapore', 'Nairobi', 'Lima', 'Oslo', 'Toronto', 'Kuala Lumpur', 'Lisbon', 'Dubai',
          'Melbourne', 'Accra', 'Hanoi', 'Bogotá', 'Vienna', 'Mumbai', 'Cape Town', 'Seoul', 'Mexico City']


def name(rng):
    return rng.choice(NAMES)


def two_names(rng):
    a, b = rng.sample(NAMES, 2)
    return a, b


def fmt(x, sf=3):
    """Format a number to sf significant figures, without trailing noise."""
    if x == 0:
        return '0'
    if isinstance(x, int) or (isinstance(x, float) and x.is_integer() and abs(x) < 1e6):
        return str(int(x))
    mag = math.floor(math.log10(abs(x)))
    if -3 <= mag < 6:
        dec = max(0, sf - 1 - mag)
        s = f'{x:.{dec}f}'
        return s
    m = x / 10 ** mag
    return f'{m:.{sf - 1}f} × 10^{mag}'


def sci(x, sf=3):
    if x == 0:
        return '0'
    mag = math.floor(math.log10(abs(x)))
    m = x / 10 ** mag
    if round(m, sf - 1) >= 10:
        m /= 10
        mag += 1
    return f'{m:.{sf - 1}f} × 10^{mag}'


def frac(fr: Fraction) -> str:
    fr = Fraction(fr)
    return str(fr.numerator) if fr.denominator == 1 else f'{fr.numerator}/{fr.denominator}'


def shuffle_opts(rng, correct, wrongs):
    """Return (options, answer) with 4 unique options."""
    seen, opts = set(), []
    for o in [correct] + list(wrongs):
        o = str(o)
        if o not in seen:
            seen.add(o)
            opts.append(o)
        if len(opts) == 4:
            break
    if len(opts) < 4:
        return None
    rng.shuffle(opts)
    return opts, str(correct)


def mcq(rng, stem, correct, wrongs, key, **kw):
    r = shuffle_opts(rng, correct, wrongs)
    if r is None:
        return None
    opts, ans = r
    letter = 'ABCD'[opts.index(ans)]
    return dict(stem=stem, options=opts, answer=ans, markingKey=f'{letter}. {key}', type='mcq', **kw)


def num_distractors(rng, v, n=3, sf=3, kinds=None):
    """Plausible wrong numeric answers around v (factor-of-2, ×10, sign, off-by-one-ish)."""
    cands = kinds or [v * 2, v / 2, v * 10, v / 10, -v, v * 1.5, v + 1, v - 1, v * 4, v / 4]
    out = []
    for c in cands:
        s = fmt(c, sf)
        if s != fmt(v, sf) and s not in out:
            out.append(s)
    rng.shuffle(out)
    return out[:n]


# --------------------------------------------------------------------------------------------
# Fact packs
# --------------------------------------------------------------------------------------------
@dataclass
class F:
    """Authored content for one subtopic. All fields optional; the richer, the more variety."""
    terms: list = field(default_factory=list)      # (term, definition)
    facts: list = field(default_factory=list)      # (question, correct, [3 distractors], why)
    why: list = field(default_factory=list)        # (explain-stem, answer)            C2
    contrast: list = field(default_factory=list)   # (a, b, difference)                C2
    misc: list = field(default_factory=list)       # (wrong claim, correction)         C2/C3
    apply: list = field(default_factory=list)      # (stem, answer[, marks, type])     C3 authored
    cases: list = field(default_factory=list)      # (case, what happened, concept, how it illustrates)  C3
    sources: list = field(default_factory=list)    # (source text, attribution, question, answer)  C3 (source/data)
    evaluate: list = field(default_factory=list)   # (claim, [for], [against], judgement)  C4
    extended: list = field(default_factory=list)   # (stem, answer[, marks, type])      C4 authored
    gens: list = field(default_factory=list)       # extra T templates (parametric)


def _pick(rng, seq, slot, salt=''):
    if not seq:
        raise IndexError('empty')
    return rng.choice(seq)


def fact_templates(f: F, style: dict | None = None, pool_terms: list | None = None) -> list:
    """Turn a fact pack into templates. style tweaks wording per subject:
       style = {'subject': 'economics', 'essay_marks': 15, 'eval_marks': 10, 'mcq': True,
                'context_word': 'the period', 'markband': '...'}"""
    style = style or {}
    st_marks_eval = style.get('eval_marks', 10)
    st_marks_essay = style.get('essay_marks', 15)
    markband = style.get('markband', 'Top band: focused, balanced argument, well-chosen specific evidence, and a reasoned judgement that follows from the analysis.')
    out = []
    pool_terms = pool_terms or []

    if f.terms:
        def define(rng, slot):
            t, d = _pick(rng, f.terms, slot)
            verb = rng.choice(['Define', 'State what is meant by', 'Outline the meaning of'])
            return dict(stem=f'{verb} the term "{t}".', answer=d[0].upper() + d[1:],
                        markingKey=f'1 mark for the core idea: {d}. Award full marks only if the defining feature is clear; a vague example alone scores 0.',
                        type='short', marks=2 if slot.d >= 2 else 1)
        out.append(T('C1', (1, 2), define, 'short', name='define'))

        def term_mcq(rng, slot):
            t, d = _pick(rng, f.terms, slot)
            others = [dd for tt, dd in (f.terms + pool_terms) if tt != t and dd != d]
            if len(others) < 3:
                return None
            wrong = rng.sample(others, 3)
            return mcq(rng, f'Which of the following best describes "{t}"?', d[0].upper() + d[1:],
                       [w[0].upper() + w[1:] for w in wrong], f'"{t}" is {d}.')
        out.append(T('C1', (1, 3), term_mcq, 'mcq', name='term_mcq'))

        def term_rev(rng, slot):
            t, d = _pick(rng, f.terms, slot)
            others = [tt for tt, dd in (f.terms + pool_terms) if tt != t]
            if len(others) < 3:
                return None
            return mcq(rng, f'Which term matches this description: "{d[0].upper() + d[1:]}"?', t,
                       rng.sample(others, 3), f'This is the definition of {t}.')
        out.append(T('C1', (1, 2), term_rev, 'mcq', name='term_rev'))

    if f.facts:
        def fact_mcq(rng, slot):
            q, a, wrong, why = _pick(rng, f.facts, slot)
            return mcq(rng, q, a, wrong, why)
        out.append(T('C1', (1, 3), fact_mcq, 'mcq', name='fact_mcq'))

        def fact_short(rng, slot):
            q, a, wrong, why = _pick(rng, f.facts, slot)
            q2 = q.replace('Which of the following', 'What').replace('which of the following', 'what')
            return dict(stem=q2, answer=a, markingKey=f'{a}. {why}', type='short', marks=1)
        out.append(T('C1', (2, 3), fact_short, 'short', name='fact_short'))

    if f.why:
        def why(rng, slot):
            q, a = _pick(rng, f.why, slot)
            m = 2 if slot.d <= 2 else 3 if slot.d == 3 else 4
            v = rng.random()
            if slot.d >= 3 and v < 0.5 and q.startswith('Explain'):
                q = 'With the help of a specific example, e' + q[1:]
                a = a + ' (A specific, correct example that illustrates this is required for full marks.)'
            elif slot.d <= 2 and v < 0.4 and q.startswith('Explain why'):
                q = 'Briefly explain why' + q[len('Explain why'):]
            return dict(stem=q, answer=a, type='explain', marks=m,
                        markingKey=f'Award marks for: {a} ({m} marks: one for each linked point in the chain of reasoning; no marks for assertion without explanation.)')
        out.append(T(('C2',), (1, 4), why, 'explain', name='why'))

    if f.contrast:
        def contrast(rng, slot):
            a, b, diff = _pick(rng, f.contrast, slot)
            if rng.random() < 0.5:
                a, b = b, a
            verb = rng.choice(['Distinguish between', 'Explain the difference between'])
            return dict(stem=f'{verb} {a} and {b}.', answer=diff, type='explain', marks=2 if slot.d <= 2 else 4,
                        markingKey=f'{diff} One mark for a correct account of each side; further marks for making the difference explicit (not two separate definitions).')
        out.append(T('C2', (2, 4), contrast, 'explain', name='contrast'))

    if f.misc:
        def misc(rng, slot):
            claim, fix = _pick(rng, f.misc, slot)
            who = name(rng)
            frame = rng.choice([f'{who} writes: "{claim}" Explain why this is inaccurate.',
                                f'A student claims that {claim[0].lower() + claim[1:]} Identify the error in this claim and correct it.',
                                f'"{claim}" Explain the flaw in this statement.'])
            return dict(stem=frame, answer=fix, type='explain', marks=3 if slot.d >= 3 else 2,
                        markingKey=f'{fix} 1 mark for identifying the error, 1-2 marks for the correct explanation.', gap='G2')
        out.append(T(('C2', 'C3'), (2, 4), misc, 'explain', name='misc'))

    if f.apply:
        def apply(rng, slot):
            it = _pick(rng, f.apply, slot)
            stem, ans = it[0], it[1]
            m = it[2] if len(it) > 2 else (2 if slot.d <= 2 else 3 if slot.d == 3 else 4)
            ty = it[3] if len(it) > 3 else 'short'
            return dict(stem=stem, answer=ans, markingKey=f'{ans}', type=ty, marks=m)
        out.append(T('C3', (1, 5), apply, 'short', name='apply'))

    if f.cases:
        def case_explain(rng, slot):
            case, what, concept, how = _pick(rng, f.cases, slot)
            frames = [
                (f'With reference to {case}, explain how it illustrates {concept}.', 2),
                (f'Outline one way in which {case} shows {concept}.', 1),
                (f'Using {case} as an example, explain {concept}.', 2),
                (f'Briefly describe {case} and explain what it reveals about {concept}.', 3),
            ]
            stem, base = rng.choice(frames)
            m = base + (1 if slot.d >= 3 else 0) + (1 if slot.d >= 4 else 0)
            return dict(stem=stem, answer=f'{what} {how}', type='short', marks=m,
                        markingKey=f'Context ({what}) – 1 mark for accurate, specific detail. Link: {how} – remaining marks for explicitly connecting the example to {concept}.')
        out.append(T('C3', (1, 4), case_explain, 'short', name='case'))

    if f.sources:
        def source(rng, slot):
            src, attr, q, a = _pick(rng, f.sources, slot)
            m = 2 if slot.d <= 2 else 3 if slot.d == 3 else 4
            return dict(stem=f'Read the source below.\n\n{src}\n— {attr}\n\n{q}', answer=a, type='case', marks=m,
                        markingKey=f'{a} Award marks for points drawn explicitly from the source; own knowledge alone is not credited in this part.', gap='G7')
        out.append(T(('C3', 'C4'), (2, 4), source, 'case', name='source'))

    if f.evaluate:
        def evaluate(rng, slot):
            claim, pro, con, judge = _pick(rng, f.evaluate, slot)
            if slot.d >= 5:
                stem = f'"{claim}" To what extent do you agree with this statement?'
                m = st_marks_essay
                ty = 'long'
            elif slot.d == 4:
                stem = rng.choice([f'Evaluate the claim that {claim[0].lower() + claim[1:]}',
                                   f'"{claim}" Discuss.',
                                   f'To what extent is it true that {claim[0].lower() + claim[1:].rstrip(".")}?'])
                m = st_marks_eval
                ty = 'long'
            else:
                stem = rng.choice([f'Give one argument for and one argument against the view that {claim[0].lower() + claim[1:]}',
                                   f'Outline two points that could be used to evaluate the claim: "{claim}"',
                                   f'Analyse one strength and one limitation of the view that {claim[0].lower() + claim[1:]}'])
                m = 4
                ty = 'case'
            key = ('Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) +
                   f'. Supported judgement: {judge}')
            if ty == 'long':
                key += f' Markbands: {markband}'
            return dict(stem=stem, answer=judge, markingKey=key, type=ty, marks=m)
        out.append(T('C4', (2, 5), evaluate, 'long', name='evaluate'))

    if f.extended:
        def extended(rng, slot):
            it = _pick(rng, f.extended, slot)
            stem, ans = it[0], it[1]
            m = it[2] if len(it) > 2 else (4 if slot.d <= 3 else 6)
            ty = it[3] if len(it) > 3 else 'multi_step'
            return dict(stem=stem, answer=ans, markingKey=ans, type=ty, marks=m)
        out.append(T('C4', (2, 5), extended, 'multi_step', name='extended'))

    out.extend(f.gens)
    return out


# --------------------------------------------------------------------------------------------
# Registry helpers for packs keyed by 'chNN-stN'
# --------------------------------------------------------------------------------------------
SUP = str.maketrans('0123456789-+', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺')


def sup(n) -> str:
    return str(n).translate(SUP)


def pe(expr) -> str:
    """Pretty-print a sympy expression: x**2 -> x², 3*x -> 3x, sqrt(2) -> √2."""
    import re as _re
    s = str(expr)
    s = _re.sub(r'sqrt\(([^()]+)\)', r'√\1', s)
    s = _re.sub(r'\*\*\((-?\d+)\)', lambda m: sup(m.group(1)), s)
    s = _re.sub(r'\*\*(\d+)', lambda m: sup(m.group(1)), s)
    s = s.replace('*', '')
    return s


class Registry:
    def __init__(self):
        self.t: dict[str, list] = {}
        self.f: dict[str, F] = {}

    def add(self, key, c, d, type='short', style=None):
        def deco(fn):
            self.t.setdefault(key, []).append(T(c, d, fn, type, style, fn.__name__))
            return fn
        return deco

    def static(self, key, c, d, items, type='short', marks=None, style=None, gap=None):
        """items: (stem, answer, markingKey) tuples."""
        def fn(rng, slot):
            it = rng.choice(items)
            out = dict(stem=it[0], answer=it[1], markingKey=it[2] if len(it) > 2 else it[1], type=type)
            if marks:
                out['marks'] = marks
            if gap:
                out['gap'] = gap
            return out
        self.t.setdefault(key, []).append(T(c, d, fn, type, style, 'static'))

    def mcqs(self, key, c, d, items, style=None):
        """items: (stem, correct, [3 wrong], explanation)."""
        def fn(rng, slot):
            q, a, w, why = rng.choice(items)
            return mcq(rng, q, a, w, why)
        self.t.setdefault(key, []).append(T(c, d, fn, 'mcq', style, 'mcqs'))

    def facts(self, key, f: F):
        self.f[key] = f

    def build(self, st, style=None):
        key = st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]
        ch = key.split('-')[0]
        pool = [t for k, ff in self.f.items() if k.startswith(ch + '-') and k != key for t in ff.terms]
        out = list(self.t.get(key, []))
        if key in self.f:
            out += fact_templates(self.f[key], style, pool)
        if not out:
            raise RuntimeError(f'no content for {st["id"]} ({st["name"]})')
        return out
