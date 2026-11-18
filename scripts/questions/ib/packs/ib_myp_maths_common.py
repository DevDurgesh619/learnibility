"""Shared helpers for the IB MYP Mathematics packs (ib-g8-maths, ib-g10-maths).

Formatting helpers (minus signs, linear/polynomial text, surds), international contexts with
currencies, and a few small number utilities. Answers are always computed (sympy / fractions).
"""
from __future__ import annotations

import math
from fractions import Fraction as Fr

import sympy as sp

from _common import pe, frac

x, y = sp.symbols('x y')

# (city, country, currency prefix, currency name) – international real-life frames
PLACES = [
    ('Geneva', 'Switzerland', 'CHF ', 'Swiss francs'), ('Singapore', 'Singapore', 'S$', 'Singapore dollars'),
    ('Nairobi', 'Kenya', 'KSh ', 'Kenyan shillings'), ('Lima', 'Peru', 'S/ ', 'soles'),
    ('Oslo', 'Norway', 'NOK ', 'Norwegian kroner'), ('Toronto', 'Canada', 'C$', 'Canadian dollars'),
    ('Kuala Lumpur', 'Malaysia', 'RM', 'ringgit'), ('Lisbon', 'Portugal', '€', 'euros'),
    ('Dubai', 'the UAE', 'AED ', 'dirhams'), ('Melbourne', 'Australia', 'A$', 'Australian dollars'),
    ('Accra', 'Ghana', 'GH₵', 'cedis'), ('Hanoi', 'Vietnam', '₫', 'dong'), ('Bogotá', 'Colombia', 'COP ', 'pesos'),
    ('Vienna', 'Austria', '€', 'euros'), ('Mumbai', 'India', '₹', 'rupees'), ('Cape Town', 'South Africa', 'R', 'rand'),
    ('Seoul', 'South Korea', '₩', 'won'), ('Mexico City', 'Mexico', 'MX$', 'pesos'), ('Tokyo', 'Japan', '¥', 'yen'),
    ('London', 'the UK', '£', 'pounds'), ('Buenos Aires', 'Argentina', 'ARS ', 'pesos'), ('Cairo', 'Egypt', 'E£', 'Egyptian pounds'),
]
# Places whose currency amounts look natural with 2 dp
DP2 = [p for p in PLACES if p[2] in ('CHF ', 'S$', 'C$', 'RM', '€', 'A$', '£', 'AED ', 'GH₵', 'E£')]


def place(rng, dp2=True):
    return rng.choice(DP2 if dp2 else PLACES)


def money(cur, v, dp=2):
    s = f'{v:,.{dp}f}'
    return f'{cur}{s}'


def m(s) -> str:
    """Typographic minus."""
    return str(s).replace('-', '−')


def lin(a, b, v='x') -> str:
    """a·v + b as text with typographic minus."""
    if a == 0:
        return m(b)
    s = ('' if a == 1 else '−' if a == -1 else m(a)) + v
    if b > 0:
        s += f' + {b}'
    elif b < 0:
        s += f' − {-b}'
    return s


def poly(e) -> str:
    return pe(sp.expand(e)).replace('-', '−')


def sgn(v) -> str:
    """' + 3' or ' − 3' for building expressions."""
    return f' + {v}' if v >= 0 else f' − {-v}'


def fr(v) -> str:
    return m(frac(Fr(v)))


def surd_parts(n: int):
    a = 1
    for k in range(int(math.isqrt(n)), 1, -1):
        if n % (k * k) == 0:
            a = k
            break
    return a, n // (a * a)


def surd(a, b) -> str:
    if b == 1:
        return str(a)
    return f'{"" if a == 1 else a}√{b}'


def g(v, sf=3) -> str:
    """Round to sf significant figures and print without trailing zeros; integers stay integers."""
    v = float(v)
    if v == 0:
        return '0'
    if abs(v - round(v)) < 1e-9 and abs(v) < 1e12:
        return m(int(round(v)))
    mag = math.floor(math.log10(abs(v)))
    dec = sf - 1 - mag
    r = round(v, dec)
    if dec <= 0:
        return m(int(r))
    s = f'{r:.{dec}f}'.rstrip('0').rstrip('.')
    return m(s)


def dp(v, k=2) -> str:
    return m(f'{v:.{k}f}')


def ordinal(n: int) -> str:
    return f'{n}{"th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")}'


def explain(stem, ans, key=None, marks=2, gap=None):
    d = dict(stem=stem, answer=ans, markingKey=key or f'{ans} (R1 A1; reasoning communicated clearly – criterion C)', type='explain', marks=marks)
    if gap:
        d['gap'] = gap
    return d


def short(stem, ans, key, marks=2, type='short', gap=None):
    d = dict(stem=stem, answer=ans, markingKey=key, type=type, marks=marks)
    if gap:
        d['gap'] = gap
    return d
