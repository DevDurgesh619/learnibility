"""Shared helpers for the CBSE class 11 humanities banks (history, political science, geography, sociology).

Adds extra families on top of g12_hum_engine (which is imported, not edited):
- `combo(sub, marks)`: a two-part written item built from a subtopic's cause lines (C) and false statements (S-):
  (a) give a reason, (b) correct a wrong statement. Many distinct variants, so it can fill 3-, 4- or 6-mark mock slots.
- `pairs(subs, table, marks)`: 'Distinguish between' items over curated pairs of a chapter's key terms (T lines).
"""
from __future__ import annotations

import qbank
import g12_hum_engine as E


def combo(sub, marks: int = 4, C: str = 'C3', D: str = 'D3', kinds: tuple = ()):
    """(a) reason for a causal statement + (b) correction of a false statement, split marks evenly."""
    if not sub.C or not sub.Sm:
        return []
    a_m = marks // 2
    b_m = marks - a_m

    def gen(r):
        A, R = r.choice(sub.C)
        f, corr = r.choice(sub.Sm)
        stem = (f'Answer the following with reference to {sub.topic}.\n'
                f'(a) Give a reason for the following: {E.end(A)} ({a_m})\n'
                f'(b) The following statement is incorrect. Rewrite it correctly and give one supporting fact: "{E.end(f)}" ({b_m})')
        ans = f'(a) {E.end(E.cap(R))} (b) {E.end(corr)}'
        key = (f'{marks} marks: (a) {a_m} for the reason – {E.end(R)} (b) {b_m} for the corrected statement – {E.end(corr)} '
               'Credit a relevant supporting fact from the NCERT chapter.')
        return {'stem': stem, 'answer': ans, 'key': key, 'marks': marks, 'minutes': round(marks * 1.6)}
    return [qbank.F(C, D, 'explain', gen, marks=marks, minutes=round(marks * 1.6), kinds=kinds)]


def pairs(subs, table: dict, marks: int = 2, C: str = 'C2', D: str = 'D2', suffix: str = ''):
    """Distinguish-between family per subtopic. table maps 'NN-stK' -> [(term a, term b), ...]."""
    out = {}
    terms = {t: m for sb in subs for t, m in sb.T}
    for sb in subs:
        lst = table.get(sb.sid.split('-ch')[-1], [])
        for a, b in lst:
            assert a in terms and b in terms, (sb.sid, a, b)
        if not lst:
            continue
        d = E.deck([((a, terms[a]), (b, terms[b])) for a, b in lst], recycle=True)

        def gen(r, d=d):
            (a, ma), (b, mb) = d(r)
            ans = f'{E.cap(a)}: {E.end(ma)} {E.cap(b)}: {E.end(mb)}'
            half = marks / 2
            h = int(half) if half == int(half) else half
            return {'stem': f"Distinguish between '{a}' and '{b}'{suffix}.", 'answer': ans,
                    'key': f"{marks} marks: {h} for explaining '{a}' ({E.end(ma)}) and {h} for '{b}' ({E.end(mb)}), "
                           'with the contrast made clear.', 'marks': marks, 'minutes': max(2, round(marks * 1.5))}
        out[sb.sid] = [qbank.F(C, D, 'explain', gen, marks=marks, minutes=max(2, round(marks * 1.5)))]
    return out


def merge(*dicts):
    out = {}
    for d in dicts:
        for k, v in d.items():
            out.setdefault(k, []).extend(v)
    return out
