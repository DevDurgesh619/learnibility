"""CBSE class 12 maths (NCERT Mathematics XII, 041) families, chapters 1-4."""
from __future__ import annotations

import itertools
import math
from fractions import Fraction as Fr

from qbank import F, mcq, ar, num, name, two_names, inr, num_distractors, CITIES
from g12_maths_h import (Q, mcqbank, arbank, xbank, fn, fz, fpar, poly, term, pif, mstr, mmul, madd, mscale, tr, eye,
                         det, minor_m, cof, adj, inv, rand_mat, unimod, lin_eq, dist3)

S = 'cbse-g12-maths-ch'


# ======================================================================= ch01 Relations and Functions

def _props(R, A):
    ref = all((a, a) in R for a in A)
    sym = all((b, a) in R for (a, b) in R)
    trn = all((a, d) in R for (a, b) in R for (c, d) in R if b == c)
    return ref, sym, trn


def _desc(ref, sym, trn):
    if ref and sym and trn:
        return 'reflexive, symmetric and transitive (an equivalence relation)'
    names = ['reflexive', 'symmetric', 'transitive']
    t = [n for n, v in zip(names, (ref, sym, trn)) if v]
    f = [n for n, v in zip(names, (ref, sym, trn)) if not v]
    if not t:
        return 'neither reflexive nor symmetric nor transitive'
    if len(t) == 2:
        return f'{t[0]} and {t[1]} but not {f[0]}'
    return f'{t[0]} but neither {f[0]} nor {f[1]}'


ALL_DESC = [_desc(*p) for p in itertools.product([True, False], repeat=3)]


def _rset(R):
    return '{' + ', '.join(f'({a}, {b})' for a, b in sorted(R)) + '}' if R else '∅'


def _aset(A):
    return '{' + ', '.join(str(a) for a in sorted(A)) + '}'


RULES = [
    ('a − b is divisible by 2', lambda a, b: (a - b) % 2 == 0),
    ('a − b is divisible by 3', lambda a, b: (a - b) % 3 == 0),
    ('a divides b', lambda a, b: b % a == 0),
    ('a < b', lambda a, b: a < b),
    ('a ≤ b', lambda a, b: a <= b),
    ('|a − b| ≤ 1', lambda a, b: abs(a - b) <= 1),
    ('b = a + 1', lambda a, b: b == a + 1),
    ('a + b is even', lambda a, b: (a + b) % 2 == 0),
    ('a ≠ b', lambda a, b: a != b),
    ('a = b', lambda a, b: a == b),
    ('a + b ≤ 6', lambda a, b: a + b <= 6),
    ('ab is odd', lambda a, b: (a * b) % 2 == 1),
    ('b = 2a', lambda a, b: b == 2 * a),
    ('a ≥ b', lambda a, b: a >= b),
    ('|a − b| is even and a ≤ b', lambda a, b: (a - b) % 2 == 0 and a <= b),
]


def _rand_rel(r, A):
    pairs = [(a, b) for a in A for b in A]
    while True:
        R = set(p for p in pairs if r.random() < 0.38)
        if r.random() < 0.4:
            R |= {(a, a) for a in A}
        if r.random() < 0.3:
            R |= {(b, a) for (a, b) in R}
        if 2 <= len(R) <= 7:
            return R


def c1s1_def(r):
    return mcqbank([
        ('A relation R in a set A is called reflexive if …', '(a, a) ∈ R for every a ∈ A', ['(a, b) ∈ R implies (b, a) ∈ R', '(a, a) ∉ R for every a ∈ A', '(a, b) ∈ R for all a, b ∈ A'], 'Definition of a reflexive relation (NCERT 1.2).'),
        ('A relation R in a set A is called symmetric if …', '(a₁, a₂) ∈ R implies (a₂, a₁) ∈ R', ['(a₁, a₁) ∈ R for all a₁ ∈ A', '(a₁, a₂) ∈ R and (a₂, a₃) ∈ R imply (a₁, a₃) ∈ R', '(a₁, a₂) ∈ R implies (a₂, a₁) ∉ R'], 'Definition of a symmetric relation.'),
        ('A relation R in a set A is called transitive if …', '(a₁, a₂) ∈ R and (a₂, a₃) ∈ R imply (a₁, a₃) ∈ R', ['(a₁, a₂) ∈ R implies (a₂, a₁) ∈ R', '(a, a) ∈ R for all a ∈ A', '(a₁, a₂) ∈ R implies (a₁, a₁) ∈ R'], 'Definition of a transitive relation.'),
        ('The relation R = A × A in a set A is called …', 'the universal relation', ['the empty relation', 'the identity relation', 'an inverse relation'], 'Every element is related to every element.'),
        ('A relation R in A in which no element of A is related to any element of A (R = ∅) is called …', 'the empty relation', ['the universal relation', 'the identity relation', 'a reflexive relation'], 'R = φ ⊂ A × A.'),
        ('Let A = {1, 2, 3}. The relation R = {(1, 1), (2, 2), (3, 3)} in A is …', 'reflexive, symmetric and transitive', ['reflexive only', 'symmetric only', 'not transitive'], 'The identity relation is an equivalence relation.'),
        ('In the set of all lines in a plane, R = {(L₁, L₂): L₁ is perpendicular to L₂} is …', 'symmetric but neither reflexive nor transitive', ['an equivalence relation', 'reflexive and symmetric', 'transitive only'], 'L ⟂ L is false; L₁ ⟂ L₂ ⇒ L₂ ⟂ L₁; L₁ ⟂ L₂, L₂ ⟂ L₃ ⇒ L₁ ∥ L₃.'),
        ('In the set of all triangles in a plane, R = {(T₁, T₂): T₁ is similar to T₂} is …', 'an equivalence relation', ['reflexive only', 'symmetric but not transitive', 'transitive but not symmetric'], 'Similarity is reflexive, symmetric and transitive.'),
    ])(r)


def c1s1_count(r):
    n = r.choice([2, 3, 4, 5])
    names = r.choice([['a', 'b', 'c', 'd', 'e'], ['1', '2', '3', '4', '5'], ['p', 'q', 'r', 's', 't'], ['x', 'y', 'z', 'u', 'v']])
    A = '{' + ', '.join(names[:n]) + '}'
    kind = r.randint(0, 2)
    if kind == 0:
        ans = 2 ** (n * n)
        return Q(f'How many relations can be defined in the set A = {A}?', f'2{_sup(n * n)} = {ans}', f'A × A has {n}² = {n * n} elements; every subset of A × A is a relation, so 2{_sup(n * n)} = {ans}.',
                 [str(n * n), str(2 ** n), str(2 ** (n * n) - 1)])
    if kind == 1:
        ans = 2 ** (n * n - n)
        return Q(f'How many reflexive relations can be defined in the set A = {A}?', f'2{_sup(n * n - n)} = {ans}', f'All {n} pairs (a, a) must be present; each of the other {n * n - n} pairs may or may not be: 2{_sup(n * n - n)} = {ans}.',
                 [str(2 ** (n * n)), str(2 ** n), str(n * n - n)])
    ans = 2 ** (n * (n + 1) // 2)
    return Q(f'How many symmetric relations can be defined in the set A = {A}?', f'2{_sup(n * (n + 1) // 2)} = {ans}',
             f'Choose freely the {n} diagonal pairs and the {n * (n - 1) // 2} unordered pairs {{a, b}}: 2{_sup(n * (n + 1) // 2)} = {ans}.',
             [str(2 ** (n * n)), str(2 ** (n * n - n)), str(2 ** n)])


def _sup(n):
    from qbank import sup
    return sup(n)


def c1s1_props(r):
    n = r.choice([3, 3, 4])
    A = list(range(1, n + 1))
    R = _rand_rel(r, A)
    d = _desc(*_props(R, A))
    wrong = [x for x in ALL_DESC if x != d]
    r.shuffle(wrong)
    return mcq(f'Let A = {_aset(A)} and R = {_rset(R)} be a relation in A. Then R is …', d, wrong[:3],
               f'Check each property for every element/pair: R is {d}.', r)


def c1s1_rule(r):
    n = r.choice([4, 5, 6])
    A = list(range(1, n + 1))
    txt, f = r.choice(RULES)
    R = {(a, b) for a in A for b in A if f(a, b)}
    if not R or len(R) > 12:
        raise ValueError
    p = _props(R, A)
    d = _desc(*p)
    wrong = [x for x in ALL_DESC if x != d]
    r.shuffle(wrong)
    return Q(f'Let A = {_aset(A)} and R = {{(a, b): a, b ∈ A, {txt}}}. Write R in roster form and determine whether R is reflexive, symmetric or transitive.',
             f'R = {_rset(R)}; R is {d}', f'List all pairs satisfying the rule (1 mark); test each of the three properties on the list (1 mark).', wrong[:3])


def _closure_rt(R, A):
    S = set(R) | {(a, a) for a in A}
    changed = True
    while changed:
        changed = False
        for (a, b) in list(S):
            for (c, d) in list(S):
                if b == c and (a, d) not in S:
                    S.add((a, d))
                    changed = True
    return S


def _closure_rs(R, A):
    return set(R) | {(b, a) for (a, b) in R} | {(a, a) for a in A}


def c1s1_add(r):
    A = [1, 2, 3]
    while True:
        R = set(r.sample([(a, b) for a in A for b in A if a != b], r.randint(1, 3)))
        kind = r.randint(0, 1)
        S = _closure_rt(R, A) if kind == 0 else _closure_rs(R, A)
        add = sorted(S - R)
        if 3 <= len(add) <= 7 and S != {(a, b) for a in A for b in A}:
            break
    want = 'reflexive and transitive but not symmetric' if kind == 0 else 'reflexive and symmetric but not transitive'
    if _props(S, A) != ((True, False, True) if kind == 0 else (True, True, False)):
        raise ValueError
    return Q(f'Let A = {{1, 2, 3}} and R = {_rset(R)}. Find the minimum number of ordered pairs to be added to R so that the enlarged relation is {want}. List them.',
             f'{len(add)}: {", ".join(f"({a}, {b})" for a, b in add)}',
             f'Add (1, 1), (2, 2), (3, 3) for reflexivity, then the pairs forced by {"transitivity" if kind == 0 else "symmetry"} (2 marks); check the new relation is still not {"symmetric" if kind == 0 else "transitive"} (1 mark).',
             [str(len(add) + 1), str(len(add) - 1), str(len(add) + 2)])


STD_REL = [
    ('R = {(a, b): a ≤ b²} in the set R of real numbers', 'neither reflexive nor symmetric nor transitive',
     'Not reflexive: (1/2, 1/2) ∉ R as 1/2 > 1/4. Not symmetric: (1, 4) ∈ R but (4, 1) ∉ R. Not transitive: (3, 2), (2, 1.5) ∈ R but 3 > 2.25, so (3, 1.5) ∉ R.'),
    ('R = {(a, b): a ≤ b³} in the set R of real numbers', 'neither reflexive nor symmetric nor transitive',
     'Not reflexive: (1/2, 1/2) ∉ R. Not symmetric: (1, 2) ∈ R but (2, 1) ∉ R. Not transitive: (3, 3/2), (3/2, 6/5) ∈ R but 3 > (6/5)³ = 1.728.'),
    ('R = {(a, b): a ≤ b} in the set R of real numbers', 'reflexive and transitive but not symmetric',
     'a ≤ a; a ≤ b and b ≤ c ⇒ a ≤ c; but (1, 2) ∈ R and (2, 1) ∉ R.'),
    ('R = {(a, b): b = a + 1} in the set A = {1, 2, 3, 4, 5, 6}', 'neither reflexive nor symmetric nor transitive',
     '(1, 1) ∉ R; (1, 2) ∈ R but (2, 1) ∉ R; (1, 2), (2, 3) ∈ R but (1, 3) ∉ R.'),
    ('R = {(x, y): x − y is an integer} in the set R of real numbers', 'reflexive, symmetric and transitive (an equivalence relation)',
     'x − x = 0 ∈ Z; x − y ∈ Z ⇒ y − x ∈ Z; (x − y) + (y − z) = x − z ∈ Z.'),
    ('R = {(a, b): |a − b| ≤ 1} in the set R of real numbers', 'reflexive and symmetric but not transitive',
     '|a − a| = 0; |a − b| = |b − a|; (0, 1), (1, 2) ∈ R but |0 − 2| = 2 > 1.'),
    ('R = {(a, b): ab ≥ 0} in the set R of real numbers', 'reflexive and symmetric but not transitive',
     'a² ≥ 0; ab = ba; (1, 0), (0, −1) ∈ R but 1 × (−1) < 0.'),
    ('R = {(a, b): a divides b} in the set N of natural numbers', 'reflexive and transitive but not symmetric',
     'a | a; a | b, b | c ⇒ a | c; 2 | 4 but 4 ∤ 2.'),
    ('R = {(x, y): x is exactly 7 cm taller than y} in the set of people of a town', 'neither reflexive nor symmetric nor transitive',
     'No one is 7 cm taller than self; if x is 7 cm taller than y, y is shorter; x 7 cm taller than y and y than z gives 14 cm.'),
    ('R = {(x, y): x and y live in the same locality} in the set of people of a city', 'reflexive, symmetric and transitive (an equivalence relation)',
     'Same locality as oneself; symmetric by wording; same locality is passed on.'),
    ('R = {(x, y): x is the father of y} in the set of people of a town', 'neither reflexive nor symmetric nor transitive',
     'No one is their own father; if x is father of y, y is not father of x; a grandfather is not the father.'),
    ('R = {(a, b): a − b is divisible by 4} in the set Z of integers', 'reflexive, symmetric and transitive (an equivalence relation)',
     '0 divisible by 4; b − a = −(a − b); (a − b) + (b − c) = a − c.'),
    ('R = {(a, b): a < b} in the set N of natural numbers', 'transitive but neither reflexive nor symmetric',
     '1 < 1 false; 1 < 2 but 2 < 1 false; a < b < c ⇒ a < c.'),
    ('R = {(1, 2), (2, 1)} in the set A = {1, 2, 3}', 'symmetric but neither reflexive nor transitive',
     '(1, 1) ∉ R; pairs appear with their reverses; (1, 2), (2, 1) ∈ R but (1, 1) ∉ R.'),
]


def c1s1_std(r):
    s, a, k = r.choice(STD_REL)
    verb = r.choice(['Check whether the relation', 'Determine whether the relation', 'Examine whether the relation'])
    return Q(f'{verb} {s} is reflexive, symmetric or transitive. Justify your answer.', f'R is {a}', k + ' (1 mark for each property).',
             [x for x in ALL_DESC if x != a][:3])


def c1s1_std_mcq(r):
    s, a, k = r.choice(STD_REL)
    wrong = [x for x in ALL_DESC if x != a]
    r.shuffle(wrong)
    return mcq(f'The relation {s} is …', a, wrong[:3], k, r)


def c1s1_ar(r):
    A = [1, 2, 3]
    for _ in range(50):
        R = _rand_rel(r, A)
        ref, sym, trn = _props(R, A)
        kind = r.randint(0, 3)
        if kind == 0 and not trn:
            x, y, z = next((a, b, d) for (a, b) in sorted(R) for (c, d) in sorted(R) if b == c and (a, d) not in R)
            return ar(f'The relation R = {_rset(R)} in A = {{1, 2, 3}} is not transitive.', f'({x}, {y}) ∈ R and ({y}, {z}) ∈ R but ({x}, {z}) ∉ R.', 'a', 'The counterexample in R proves A.')
        if kind == 1 and sym and any(a != b for a, b in R):
            p, q = next((a, b) for a, b in sorted(R) if a != b)
            return ar(f'The relation R = {_rset(R)} in A = {{1, 2, 3}} is symmetric.', f'({p}, {q}) ∈ R and ({q}, {p}) ∈ R.', 'b', 'Both true, but one pair and its reverse do not prove symmetry for all pairs.')
        if kind == 2 and not ref and (1, 1) in R:
            return ar(f'The relation R = {_rset(R)} in A = {{1, 2, 3}} is reflexive.', '(1, 1) ∈ R.', 'd', 'A is false: reflexivity needs (2, 2) and (3, 3) as well; R is true.')
        if kind == 3 and ref:
            miss = [(a, b) for a in A for b in A if (a, b) not in R]
            if not miss:
                continue
            p, q = miss[0]
            return ar(f'The relation R = {_rset(R)} in A = {{1, 2, 3}} is reflexive.', f'({p}, {q}) ∈ R.', 'c', f'A is true since (1, 1), (2, 2), (3, 3) ∈ R; R is false since ({p}, {q}) ∉ R.')
    raise ValueError


def c1s1_people(r):
    return xbank([
        ('Give an example of a relation in the set A = {1, 2, 3} which is symmetric but neither reflexive nor transitive. Explain.', 'R = {(1, 2), (2, 1)}',
         '(1, 1) ∉ R so not reflexive; pairs occur with reverses so symmetric; (1, 2), (2, 1) ∈ R but (1, 1) ∉ R so not transitive.'),
        ('Give an example of a relation in A = {1, 2, 3} which is transitive but neither reflexive nor symmetric. Explain.', 'R = {(1, 2)}',
         '(1, 1) ∉ R; (2, 1) ∉ R; transitivity holds vacuously as there is no chain (a, b), (b, c).'),
        ('Give an example of a relation in A = {1, 2, 3} which is reflexive and symmetric but not transitive. Explain.', 'R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1), (2, 3), (3, 2)}',
         'Contains all (a, a); pairs come with reverses; (1, 2), (2, 3) ∈ R but (1, 3) ∉ R.'),
        ('Show that the relation R in the set {1, 2, 3} given by R = {(1, 2), (2, 1)} is symmetric but neither reflexive nor transitive.', 'Symmetric only',
         '(1, 1) ∉ R; reverse of each pair is in R; (1, 2), (2, 1) ∈ R but (1, 1) ∉ R.'),
        ('Explain why the empty relation in a non-empty set A is symmetric and transitive but not reflexive.', 'There is no pair to violate symmetry or transitivity, but (a, a) ∉ ∅.',
         'Conditions of symmetry and transitivity hold vacuously; reflexivity needs (a, a) ∈ R for each a ∈ A.'),
        ('Show that the universal relation in a set A is an equivalence relation.', 'R = A × A contains every pair.', 'All (a, a), all reverses and all chains are in A × A.'),
        ('Is the relation "is a brother of" in the set of all people reflexive, symmetric, transitive? Explain.', 'Not reflexive, not symmetric (a sister may be involved), and not transitive in general (x brother of y, y brother of x gives (x, x)).',
         'No one is his own brother; x brother of y does not give y brother of x if y is a girl; x brother of y and y brother of x would need x brother of x.'),
    ])(r)


def c1s1_case(r):
    n = r.choice([4, 5, 6])
    A = list(range(1, n + 1))
    for _ in range(40):
        txt, f = r.choice(RULES)
        R = {(a, b) for a in A for b in A if f(a, b)}
        if not R or all(_props(R, A)):
            continue
        S = _closure_rs(R, A)
        add = len(S - R)
        if add == 0:
            continue
        who = name(r)
        ref, sym, trn = _props(R, A)
        return Q((f'In a maths club activity, {who} writes the numbers on {n} cards, A = {_aset(A)}, and defines a relation R = {{(a, b): a, b ∈ A, {txt}}}. '
                  f'(i) How many ordered pairs are there in R? (ii) Is R symmetric? Give a reason. (iii) Find the minimum number of ordered pairs to be added to R to make it both reflexive and symmetric.'),
                 f'(i) {len(R)} (ii) {"Yes" if sym else "No"} (iii) {add}',
                 f'(i) R = {_rset(R)}, {len(R)} pairs (1 mark). (ii) {"every pair has its reverse in R" if sym else "some (a, b) ∈ R has (b, a) ∉ R"} (1 mark). (iii) add the missing (a, a) and reverse pairs: {add} (2 marks).')
    raise ValueError


# ---- st2 equivalence relations

def _classes(m, A):
    out = {}
    for a in A:
        out.setdefault(a % m, []).append(a)
    return out


def c1s2_mcq(r):
    return mcqbank([
        ('The number of equivalence relations in the set {1, 2, 3} containing (1, 2) and (2, 1) is …', '2', ['1', '3', '5'], 'The smallest one {(1,1),(2,2),(3,3),(1,2),(2,1)} and the universal relation.'),
        ('The total number of equivalence relations that can be defined on the set {1, 2, 3} is …', '5', ['3', '4', '8'], 'They correspond to the 5 partitions of a 3-element set.'),
        ('In an equivalence relation, any two equivalence classes are …', 'either identical or disjoint', ['always identical', 'always disjoint', 'always overlapping'], 'Equivalence classes partition the set.'),
        ('The union of all the equivalence classes of an equivalence relation R in a set X is …', 'the whole set X', ['the empty set', 'R itself', 'a single class'], 'The classes partition X.'),
        ('Let R be the relation in Z given by R = {(a, b): 2 divides a − b}. The equivalence class [0] is …', 'the set of all even integers', ['the set of all odd integers', '{0}', 'Z'], '[0] = {x ∈ Z : x − 0 is even}.'),
        ('The smallest equivalence relation in a set A is …', 'the identity relation {(a, a): a ∈ A}', ['the empty relation', 'A × A', 'not defined'], 'It must contain every (a, a) and nothing more is needed.'),
        ('The largest equivalence relation in a set A is …', 'the universal relation A × A', ['the identity relation', 'the empty relation', 'not defined'], 'A × A contains every pair.'),
        ('R = {(T₁, T₂): T₁ is congruent to T₂} in the set of all triangles is …', 'an equivalence relation', ['reflexive only', 'not symmetric', 'not transitive'], 'Congruence is reflexive, symmetric and transitive.'),
    ])(r)


def c1s2_modz(r):
    m = r.randint(2, 9)
    t = r.randint(0, m - 1)
    kind = r.randint(0, 1)
    if kind == 0:
        return Q(f'R is the relation in Z defined by R = {{(a, b): {m} divides a − b}}. How many distinct equivalence classes does R have?', str(m),
                 f'The classes are [0], [1], …, [{m - 1}] (the possible remainders on division by {m}).', [str(m - 1), str(m + 1), 'infinitely many'])
    cls = ', '.join(str(t + m * k) for k in range(-2, 3))
    return Q(f'R is the relation in Z defined by R = {{(a, b): a − b is divisible by {m}}}. Write the equivalence class [{t}].', f'[{t}] = {{…, {cls}, …}} = {{{m}k + {t} : k ∈ Z}}'.replace(' + 0 ', ' '),
             f'[{t}] = {{x ∈ Z : x − {t} is divisible by {m}}}.', [f'{{{t}}}', f'{{…, {", ".join(str(t + (m + 1) * k) for k in range(-1, 3))}, …}}', f'{{{m}k : k ∈ Z}}' if t else f'{{{m}k + 1 : k ∈ Z}}'])


def c1s2_class(r):
    N = r.randint(8, 14)
    lo = r.choice([0, 1])
    m = r.choice([2, 3, 4, 5])
    A = list(range(lo, N + 1))
    t = r.choice(A)
    cl = [a for a in A if (a - t) % m == 0]
    wrong1 = [a for a in A if (a - t - 1) % m == 0]
    wrong2 = [a for a in A if a % m == 0 and a != t][:len(cl)]
    form = r.choice(['|a − b| is divisible by', 'a − b is a multiple of'])
    return Q(f'Let A = {{{lo}, {lo + 1}, …, {N}}} and R = {{(a, b): a, b ∈ A, {form} {m}}}. Find the set of all elements related to {t}.',
             _aset(cl), f'b is related to {t} exactly when b − {t} is a multiple of {m}: {_aset(cl)}.', [_aset(wrong1), _aset([t]), _aset(sorted(set(wrong2) | {t}))])


def c1s2_prove(r):
    N = r.randint(9, 15)
    m = r.choice([2, 3, 4, 5])
    t = r.randint(1, N)
    A = list(range(1, N + 1))
    cl = [a for a in A if (a - t) % m == 0]
    return Q(f'Show that the relation R in the set A = {{1, 2, …, {N}}} given by R = {{(a, b): |a − b| is divisible by {m}}} is an equivalence relation. Find the set of all elements related to {t}.',
             f'R is an equivalence relation; elements related to {t}: {_aset(cl)}',
             f'Reflexive: |a − a| = 0 is divisible by {m} (1 mark). Symmetric: |a − b| = |b − a| (1 mark). Transitive: if {m} | (a − b) and {m} | (b − c) then {m} | (a − b) + (b − c) = a − c (2 marks). Related to {t}: {_aset(cl)} (1 mark).')


def c1s2_partition(r):
    n = r.randint(5, 8)
    A = list(range(1, n + 1))
    r.shuffle(A)
    k = r.randint(2, 3)
    cuts = sorted(r.sample(range(1, n), k - 1))
    parts = [sorted(A[i:j]) for i, j in zip([0] + cuts, cuts + [n])]
    cnt = sum(len(p) ** 2 for p in parts)
    ptxt = ', '.join(_aset(p) for p in parts)
    return Q(f'The set A = {{1, 2, …, {n}}} is partitioned into the subsets {ptxt}, and R is the equivalence relation whose equivalence classes are these subsets. How many ordered pairs does R contain?',
             str(cnt), f'Each class of size s gives s² ordered pairs: {" + ".join(f"{len(p)}²" for p in parts)} = {cnt}.',
             [str(sum(len(p) for p in parts)), str(sum(len(p) * (len(p) - 1) for p in parts)), str(cnt + n)])


def c1s2_closure(r):
    n = r.choice([4, 5])
    A = list(range(1, n + 1))
    pairs = r.sample([(a, b) for a in A for b in A if a < b], r.randint(1, 3))
    par = {a: a for a in A}

    def find(x):
        while par[x] != x:
            x = par[x]
        return x
    for a, b in pairs:
        par[find(a)] = find(b)
    cls = {}
    for a in A:
        cls.setdefault(find(a), []).append(a)
    parts = sorted(cls.values())
    cnt = sum(len(p) ** 2 for p in parts)
    return Q(f'Let A = {_aset(A)}. Find the smallest equivalence relation R in A containing the pairs {", ".join(f"({a}, {b})" for a, b in pairs)}. Write its equivalence classes and the number of ordered pairs in R.',
             f'Classes: {", ".join(_aset(p) for p in parts)}; R has {cnt} ordered pairs',
             f'Add all (a, a), the reverse pairs and the pairs forced by transitivity (2 marks); classes {", ".join(_aset(p) for p in parts)}, count = {" + ".join(f"{len(p)}²" for p in parts)} = {cnt} (1 mark).',
             [f'R has {cnt - n} ordered pairs', f'R has {len(pairs) * 2 + n} ordered pairs' if len(pairs) * 2 + n != cnt else f'R has {cnt + 2} ordered pairs', f'R has {n * n} ordered pairs' if n * n != cnt else f'R has {cnt + 1} ordered pairs'])


def c1s2_nn(r):
    p, q = r.sample(range(1, 9), 2)
    N = 10
    d = q - p
    cl = [(x, x + d) for x in range(1, N + 1) if 1 <= x + d <= N]
    return Q(f'Let A = {{1, 2, 3, …, {N}}} and R be the relation in A × A defined by (a, b) R (c, d) if a + d = b + c. Prove that R is an equivalence relation and obtain the equivalence class [({p}, {q})].',
             f'[({p}, {q})] = {{{", ".join(f"({x}, {y})" for x, y in cl)}}}',
             f'Reflexive: a + b = b + a (1 mark). Symmetric: a + d = b + c ⇒ c + b = d + a (1 mark). Transitive: a + d = b + c and c + f = d + e ⇒ a + f = b + e (2 marks). '
             f'Class: (x, y) R ({p}, {q}) ⇔ x + {q} = y + {p} ⇔ y − x = {d}: {{{", ".join(f"({x}, {y})" for x, y in cl)}}} (1 mark).')


def c1s2_ar(r):
    m = r.randint(3, 9)
    a, b = r.sample(range(-15, 30), 2)
    kind = r.randint(0, 3)
    if kind == 0:
        if (a - b) % m == 0:
            b += 1
        return ar(f'Under the relation "a − b is divisible by {m}" in Z, the equivalence classes [{a}] and [{b}] have no common element.', 'Two equivalence classes are either identical or disjoint.', 'a',
                  f'{a} − {b} is not divisible by {m}, so the classes differ; distinct classes are disjoint.')
    if kind == 1:
        b = a + m * r.choice([-3, -2, 2, 3, 4])
        return ar(f'Under the relation "a − b is divisible by {m}" in Z, [{a}] = [{b}].', f'{a} − ({b}) = {a - b} is divisible by {m}.', 'a', 'Related elements have the same class.')
    if kind == 2:
        if (a - b) % m == 0:
            b += 1
        return ar(f'Under the relation "a − b is divisible by {m}" in Z, [{a}] = [{b}].', 'Any two equivalence classes are either identical or disjoint.', 'd', f'{a} − {b} = {a - b} is not divisible by {m}, so A is false; R is a true property.')
    return ar(r.choice(['The relation R = {(a, b): a ≤ b} in Z is an equivalence relation.', 'The relation R = {(a, b): a divides b} in N is an equivalence relation.']),
              'The relation is reflexive and transitive.', 'd', 'It is not symmetric, so A is false; R is true.')


def c1s2_explain(r):
    m = r.randint(2, 7)
    return xbank([
        (f'Explain why the equivalence classes of the relation "a − b is divisible by {m}" in Z are exactly [0], [1], …, [{m - 1}].', f'Every integer leaves one of the remainders 0, 1, …, {m - 1} on division by {m}.',
         f'a is related to its remainder r on division by {m}; different remainders are not related, so the classes are disjoint and cover Z.'),
        ('Explain why the relation R = {(a, b): a ≤ b} in R is not an equivalence relation.', 'It is not symmetric.', '(1, 2) ∈ R but (2, 1) ∉ R; reflexive and transitive alone do not make an equivalence relation.'),
        (f'If R is an equivalence relation in A and (x, y) ∈ R, explain why [x] = [y].', 'Both classes contain the same elements.', 'If z ∈ [x] then (z, x), (x, y) ∈ R so (z, y) ∈ R and z ∈ [y]; similarly the other way.'),
        ('Show that R = {(a, b): a and b are both odd or both even} in the set {1, 2, 3, 4, 5} is an equivalence relation and name its classes.', 'Classes {1, 3, 5} and {2, 4}',
         'Same parity is reflexive, symmetric and transitive; elements of {1, 3, 5} are related only among themselves, as are {2, 4}.'),
        ('Explain why an equivalence relation in a set A divides A into mutually disjoint subsets.', 'The equivalence classes form a partition.', 'Each element lies in its own class; two classes are identical or disjoint.'),
    ])(r)


def c1s2_case(r):
    N = r.randint(30, 48)
    m = r.choice([3, 4, 5, 6])
    t = r.randint(1, N)
    A = list(range(1, N + 1))
    cl = [a for a in A if (a - t) % m == 0]
    sizes = sorted(len(v) for v in _classes(m, A).values())
    city = r.choice(CITIES)
    return Q((f'For a sports day at a school in {city}, the {N} students of Class XII are given roll numbers 1 to {N}. The teacher places two students in the same team if the difference of their roll numbers is divisible by {m}, '
              f'i.e. R = {{(a, b): a − b is divisible by {m}}} in A = {{1, 2, …, {N}}}. (i) Is R an equivalence relation? (ii) Write the team (equivalence class) of roll number {t}. '
              f'(iii) How many teams are formed and how many students are in the largest team?'),
             f'(i) Yes (ii) {_aset(cl)} (iii) {m} teams; largest has {sizes[-1]} students',
             f'(i) reflexive, symmetric, transitive (1 mark) (ii) {_aset(cl)} (1 mark) (iii) one team per remainder: {m}; sizes {", ".join(map(str, sizes))}, largest {sizes[-1]} (2 marks).')


# ---- st3 one-one and onto

FN_CLASS = [
    ('f: R → R, f(x) = 3 − 4x', 'both one-one and onto (bijective)'),
    ('f: R → R, f(x) = 1 + x²', 'neither one-one nor onto'),
    ('f: N → N, f(x) = x²', 'one-one but not onto'),
    ('f: Z → Z, f(x) = x²', 'neither one-one nor onto'),
    ('f: R → R, f(x) = x²', 'neither one-one nor onto'),
    ('f: N → N, f(x) = x³', 'one-one but not onto'),
    ('f: Z → Z, f(x) = x³', 'one-one but not onto'),
    ('f: R → R, f(x) = x³', 'both one-one and onto (bijective)'),
    ('f: R → R, f(x) = |x|', 'neither one-one nor onto'),
    ('f: R → R, f(x) = [x] (greatest integer function)', 'neither one-one nor onto'),
    ('f: N → N, f(x) = 2x', 'one-one but not onto'),
    ('f: R → R, f(x) = 2x', 'both one-one and onto (bijective)'),
    ('f: R* → R*, f(x) = 1/x (R* = non-zero reals)', 'both one-one and onto (bijective)'),
    ('f: N → N, f(n) = (n + 1)/2 if n is odd and n/2 if n is even', 'onto but not one-one'),
    ('f: N → N, f(1) = f(2) = 1 and f(x) = x − 1 for x > 2', 'onto but not one-one'),
    ('f: R → R, f(x) = 2x + 5', 'both one-one and onto (bijective)'),
    ('f: N → N, f(x) = x + 1', 'one-one but not onto'),
    ('f: Z → Z, f(x) = x + 1', 'both one-one and onto (bijective)'),
    ('f: R → R, the signum function', 'neither one-one nor onto'),
    ('f: R → [0, ∞), f(x) = x²', 'onto but not one-one'),
    ('f: [0, ∞) → [0, ∞), f(x) = x²', 'both one-one and onto (bijective)'),
]
FN_LABELS = ['one-one but not onto', 'onto but not one-one', 'both one-one and onto (bijective)', 'neither one-one nor onto']


def c1s3_mcq(r):
    s, a = r.choice(FN_CLASS)
    return mcq(f'The function {s} is …', a, [x for x in FN_LABELS if x != a], f'Test f(x₁) = f(x₂) ⇒ x₁ = x₂ and whether every element of the codomain has a pre-image: {a}.', r)


def c1s3_finite(r):
    m = r.randint(3, 4)
    n = r.choice([m - 1, m, m, m + 1])
    A = [1, 2, 3, 4][:m]
    B = r.sample([5, 6, 7, 8, 9, 10, 11], n)
    B.sort()
    f = {a: r.choice(B) for a in A}
    if r.random() < 0.5 and n >= m:
        vals = r.sample(B, m)
        f = dict(zip(A, vals))
    oo = len(set(f.values())) == m
    on = set(f.values()) == set(B)
    lab = FN_LABELS[[(True, False), (False, True), (True, True), (False, False)].index((oo, on))]
    fs = '{' + ', '.join(f'({a}, {f[a]})' for a in A) + '}'
    return mcq(f'Let A = {_aset(A)}, B = {_aset(B)} and f: A → B be f = {fs}. Then f is …', lab, [x for x in FN_LABELS if x != lab],
               f'{"Distinct images" if oo else "Two elements share an image"}; range {_aset(set(f.values()))} {"=" if on else "≠"} B.', r)


def c1s3_count(r):
    kind = r.randint(0, 3)
    m = r.randint(2, 5)
    n = r.randint(m, 6)
    if kind == 0:
        ans = n ** m
        return Q(f'Find the number of functions from a set with {m} elements to a set with {n} elements.', str(ans), f'Each of the {m} elements has {n} choices: {n}{_sup(m)} = {ans}.', [str(m ** n), str(m * n), str(math.perm(n, m))])
    if kind == 1:
        ans = math.perm(n, m)
        return Q(f'Find the number of one-one functions from a set with {m} elements to a set with {n} elements.', str(ans),
                 f'Choices {n}, {n - 1}, …, {n - m + 1}: ⁿPₘ = {ans}.', dist3(str(ans), [n ** m, math.comb(n, m), m ** n, ans + 1]))
    if kind == 2:
        k = r.randint(3, 7)
        ans = 2 ** k - 2
        return Q(f'Find the number of onto functions from the set {{1, 2, …, {k}}} to the set {{a, b}}.', str(ans), f'All 2{_sup(k)} functions except the two constant ones: 2{_sup(k)} − 2 = {ans}.', [str(2 ** k), str(2 * k), str(2 ** k - 1)])
    k = r.randint(3, 6)
    return Q(f'Find the number of bijective functions from the set A = {{1, 2, …, {k}}} to itself.', str(math.factorial(k)), f'Bijections of a {k}-element set are its arrangements: {k}! = {math.factorial(k)}.',
             [str(k ** k), str(k * k), str(2 ** k)])


def c1s3_linear(r):
    a = r.choice([-7, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
    b = r.randint(-9, 9)
    f = poly([a, b])
    pre = f'(y {"−" if b > 0 else "+"} {abs(b)})/{fpar(a)}' if b else f'y/{fpar(a)}'
    return Q(f'Show that the function f: R → R defined by f(x) = {f} is one-one and onto.', 'f is a bijection',
             f'One-one: f(x₁) = f(x₂) ⇒ {a}x₁ = {a}x₂ ⇒ x₁ = x₂ (1 mark). Onto: for any real y, x = {pre} is real and f(x) = y (2 marks).')


def c1s3_rational(r):
    while True:
        a, b, c, d = r.randint(1, 6), r.randint(-6, 6), r.randint(1, 5), r.randint(-6, 6)
        if a * d - b * c != 0 and d != 0:
            break
    fx = f'({poly([a, b])})/({poly([c, d])})'
    xm, ym = Fr(-d, c), Fr(a, c)
    pre = f'({fz(d)}y {"−" if b >= 0 else "+"} {abs(b)})/({fz(a)} − {fz(c)}y)'.replace('(1y', '(y').replace('(−1y', '(−y').replace('− 1y', '− y')
    return Q(f'Let A = R − {{{fz(xm)}}} and B = R − {{{fz(ym)}}}. Show that f: A → B defined by f(x) = {fx} is one-one and onto.', 'f is one-one and onto',
             f'One-one: f(x₁) = f(x₂) ⇒ ({poly([a, b], "x₁")})({poly([c, d], "x₂")}) = ({poly([a, b], "x₂")})({poly([c, d], "x₁")}) ⇒ ({a * d - b * c})(x₁ − x₂) = 0 ⇒ x₁ = x₂ (2 marks). '
             f'Onto: for y ∈ B, solve y = {fx}: x = {pre}, which is defined since y ≠ {fz(ym)}, and x ≠ {fz(xm)} (2 marks); hence every y has a pre-image (1 mark).')


def c1s3_square(r):
    k = r.randint(-9, 9)
    kind = r.randint(0, 1)
    f = poly([1, 0, k])
    if kind == 0:
        t = r.randint(1, 6)
        return Q(f'Show that f: R → R defined by f(x) = {f} is neither one-one nor onto.', 'Neither one-one nor onto',
                 f'f({t}) = f(−{t}) = {t * t + k}, so not one-one (1 mark); f(x) ≥ {k} for all x, so {k - 1} has no pre-image: not onto (1 mark).')
    c = r.randint(2, 6)
    return Q(f'Show that f: N → N defined by f(x) = {c}x is one-one but not onto.', 'One-one, not onto',
             f'{c}x₁ = {c}x₂ ⇒ x₁ = x₂ (1 mark); 1 (or any number not a multiple of {c}) has no pre-image in N (1 mark).')


def c1s3_ar(r):
    k = r.randint(1, 9)
    c = r.randint(2, 7)
    return arbank([
        (f'f: R → R, f(x) = x² + {k} is not one-one.', f'f(−t) = f(t) for every real number t.', 'a', 'For t ≠ 0, two different inputs give the same image.'),
        (f'f: Z → Z, f(x) = x + {k} is a bijection.', f'f is one-one and every integer y has the pre-image y − {k}.', 'a', 'One-one and onto ⇒ bijective.'),
        (f'f: N → N, f(x) = x + {k} is onto.', 'f is one-one.', 'd', f'1 has no pre-image in N, so A is false; R is true.'),
        (f'f: R → R, f(x) = |x| + {k} is not one-one.', f'f(x) ≥ {k} for every real x.', 'b', 'Both true; but A follows from f(1) = f(−1), not from the lower bound (which shows f is not onto).'),
        (f'f: N → N, f(x) = {c}x is one-one.', f'f: N → N, f(x) = {c}x is onto.', 'c', f'A is true; R is false since 1 is not a multiple of {c}.'),
        (f'f: R → R, f(x) = {c}x − {k} is onto.', f'For any real y, x = (y + {k})/{c} satisfies f(x) = y.', 'a', 'Every y has a pre-image.'),
    ])(r)


def c1s3_case(r):
    names = r.sample(['Aarav', 'Ananya', 'Kabir', 'Meera', 'Rohan', 'Diya', 'Ishaan', 'Saanvi', 'Arjun', 'Kavya'], 4)
    houses = r.sample(['Ganga', 'Yamuna', 'Kaveri', 'Narmada', 'Godavari', 'Krishna'], r.choice([3, 4]))
    f = {s: r.choice(houses) for s in names}
    oo = len(set(f.values())) == 4
    on = set(f.values()) == set(houses)
    nl = r.randint(5, 8)
    ft = ', '.join(f'{s} → {f[s]}' for s in names)
    return Q((f'In a school, four students {", ".join(names[:3])} and {names[3]} are allotted to houses {", ".join(houses)}. The allotment is a function f: S → H with {ft}. '
              f'(i) Is f one-one? (ii) Is f onto? (iii) If instead the 4 students are to be given distinct lockers from {nl} lockers, in how many ways can this one-one allotment be made?'),
             f'(i) {"Yes" if oo else "No"} (ii) {"Yes" if on else "No"} (iii) {math.perm(nl, 4)}',
             f'(i) {"all images distinct" if oo else "two students share a house"} (1 mark) (ii) {"every house is used" if on else "some house has no student"} (1 mark) (iii) {nl}P4 = {math.perm(nl, 4)} (2 marks).')


def c1s3_d5(r):
    return xbank([
        ('Let f: N → N be defined by f(n) = (n + 1)/2 if n is odd and f(n) = n/2 if n is even, for all n ∈ N. State whether f is bijective. Justify your answer.', 'Not bijective: onto but not one-one',
         'f(1) = 1 = f(2), so not one-one (2 marks). Any n ∈ N is f(2n) (and f(2n − 1)), so onto (2 marks). Conclusion (1 mark).'),
        ('Let A = R − {3} and B = R − {1}. Consider f: A → B defined by f(x) = (x − 2)/(x − 3). Is f one-one and onto? Justify.', 'Yes, f is one-one and onto',
         'f(x₁) = f(x₂) ⇒ (x₁ − 2)(x₂ − 3) = (x₂ − 2)(x₁ − 3) ⇒ x₁ = x₂ (2 marks). For y ≠ 1, x = (2 − 3y)/(1 − y) ∈ A gives f(x) = y (3 marks).'),
        ('Show that the function f: R → {x ∈ R : −1 < x < 1} defined by f(x) = x/(1 + |x|) is one-one and onto.', 'f is one-one and onto',
         'For x ≥ 0, f(x) = x/(1 + x) ∈ [0, 1); for x < 0, f(x) = x/(1 − x) ∈ (−1, 0); f(x₁) = f(x₂) forces same sign and then x₁ = x₂ (3 marks). For 0 ≤ y < 1, x = y/(1 − y); for −1 < y < 0, x = y/(1 + y) (2 marks).'),
        ('Let f: N → N be defined by f(n) = n + 1 if n is odd and f(n) = n − 1 if n is even. Show that f is a bijection.', 'f is a bijection',
         'f swaps 1↔2, 3↔4, …; f(f(n)) = n (2 marks). One-one: f(a) = f(b) ⇒ a = f(f(a)) = f(f(b)) = b (1 mark). Onto: n = f(f(n)) (2 marks).'),
        ('Show that the modulus function f: R → R, f(x) = |x|, is neither one-one nor onto.', 'Neither one-one nor onto',
         'f(−1) = f(1) = 1, so not one-one (2 marks); −1 is not the image of any real number since |x| ≥ 0 (2 marks); conclusion (1 mark).'),
    ])(r)


# ======================================================================= ch02 Inverse Trigonometric Functions

INV = {  # function: list of (argument text, principal value as fraction of π)
    'sin⁻¹': [('0', Fr(0)), ('1/2', Fr(1, 6)), ('1/√2', Fr(1, 4)), ('√3/2', Fr(1, 3)), ('1', Fr(1, 2)),
              ('−1/2', Fr(-1, 6)), ('−1/√2', Fr(-1, 4)), ('−√3/2', Fr(-1, 3)), ('−1', Fr(-1, 2))],
    'cos⁻¹': [('1', Fr(0)), ('√3/2', Fr(1, 6)), ('1/√2', Fr(1, 4)), ('1/2', Fr(1, 3)), ('0', Fr(1, 2)),
              ('−1/2', Fr(2, 3)), ('−1/√2', Fr(3, 4)), ('−√3/2', Fr(5, 6)), ('−1', Fr(1))],
    'tan⁻¹': [('0', Fr(0)), ('1/√3', Fr(1, 6)), ('1', Fr(1, 4)), ('√3', Fr(1, 3)), ('−1/√3', Fr(-1, 6)), ('−1', Fr(-1, 4)), ('−√3', Fr(-1, 3))],
    'cot⁻¹': [('√3', Fr(1, 6)), ('1', Fr(1, 4)), ('1/√3', Fr(1, 3)), ('0', Fr(1, 2)), ('−1/√3', Fr(2, 3)), ('−1', Fr(3, 4)), ('−√3', Fr(5, 6))],
    'sec⁻¹': [('1', Fr(0)), ('2/√3', Fr(1, 6)), ('√2', Fr(1, 4)), ('2', Fr(1, 3)), ('−2', Fr(2, 3)), ('−√2', Fr(3, 4)), ('−2/√3', Fr(5, 6)), ('−1', Fr(1))],
    'cosec⁻¹': [('1', Fr(1, 2)), ('2', Fr(1, 6)), ('√2', Fr(1, 4)), ('2/√3', Fr(1, 3)), ('−1', Fr(-1, 2)), ('−2', Fr(-1, 6)), ('−√2', Fr(-1, 4)), ('−2/√3', Fr(-1, 3))],
}
BRANCH = {'sin⁻¹': ('[−1, 1]', '[−π/2, π/2]'), 'cos⁻¹': ('[−1, 1]', '[0, π]'), 'tan⁻¹': ('R', '(−π/2, π/2)'),
          'cot⁻¹': ('R', '(0, π)'), 'sec⁻¹': ('R − (−1, 1)', '[0, π] − {π/2}'), 'cosec⁻¹': ('R − (−1, 1)', '[−π/2, π/2] − {0}')}
ODD = {'sin⁻¹', 'tan⁻¹', 'cosec⁻¹'}


def _wrong_pv(f, v):
    """A typical wrong principal value: sign rule applied to the wrong function, or the value outside the branch."""
    if f in ODD:
        return Fr(1) - v if v < 0 else Fr(1) + v if v == 0 else Fr(1) - v
    return -(Fr(1) - v) if v > Fr(1, 2) else -v if v else Fr(1)


def c2s1_branch(r):
    f = r.choice(list(BRANCH))
    kind = r.randint(0, 1)
    d, rg = BRANCH[f]
    if kind == 0:
        wrong = [BRANCH[g][1] for g in BRANCH if BRANCH[g][1] != rg]
        r.shuffle(wrong)
        return mcq(f'The range of the principal value branch of {f}x is …', rg, wrong[:3], f'Principal value branch of {f}: {rg}.', r)
    wrong = list(dict.fromkeys(['[−1, 1]', 'R', 'R − (−1, 1)', '(−1, 1)', '[0, ∞)']))
    wrong = [w for w in wrong if w != d]
    r.shuffle(wrong)
    return mcq(f'The domain of {f}x is …', d, wrong[:3], f'{f}x is defined for x ∈ {d}.', r)


def _interval(lo, hi):
    return f'[{fz(lo)}, {fz(hi)}]'


def c2s1_domain(r):
    f = r.choice(['sin⁻¹', 'cos⁻¹'])
    a = r.choice([2, 3, 4, 5, -2, -3, Fr(1, 2), Fr(1, 3)])
    b = r.randint(-5, 5)
    lo, hi = sorted([Fr(-1 - b) / a, Fr(1 - b) / a])
    arg = poly([a, b])
    return Q(f'Find the domain of the function {f}({arg}).', _interval(lo, hi),
             f'Need −1 ≤ {arg} ≤ 1 ⇒ {fz(lo)} ≤ x ≤ {fz(hi)}' + (' (the inequalities reverse on dividing by a negative number).' if a < 0 else '.'),
             [_interval(Fr(-1 + b) / a if a > 0 else Fr(1 + b) / a, Fr(1 + b) / a if a > 0 else Fr(-1 + b) / a) if b else _interval(0, hi), _interval(-1, 1), _interval(lo * 2, hi * 2)])


def c2s1_domain_sq(r):
    k = r.choice([2, 3, 4, 5, 8, 10, 15, 17, 24, 26])
    from g12_maths_h import surd
    lo, hi = surd(k - 1), surd(k + 1)
    ans = f'[−{hi}, −{lo}] ∪ [{lo}, {hi}]'
    return Q(f'Find the domain of the function f(x) = sin⁻¹(x² − {k}).', ans,
             f'−1 ≤ x² − {k} ≤ 1 ⇒ {k - 1} ≤ x² ≤ {k + 1} (1 mark) ⇒ {lo} ≤ |x| ≤ {hi} (1 mark).',
             [f'[{lo}, {hi}]', f'[−{hi}, {hi}]', f'[{k - 1}, {k + 1}]'])


def c2s1_ar(r):
    f = r.choice(list(INV))
    arg, v = r.choice(INV[f])
    lo, hi = BRANCH[f][1], ''
    kind = r.randint(0, 2)
    if kind == 0:
        return ar(f'The principal value of {f}({arg}) is {pif(v)}.', f'The range of the principal value branch of {f} is {BRANCH[f][1]}.', 'a', f'{pif(v)} lies in the branch and gives the correct ratio.')
    if kind == 1 and f in ('cos⁻¹', 'sec⁻¹', 'cot⁻¹') and v > Fr(1, 2):
        return ar(f'The principal value of {f}({arg}) is {pif(-(1 - v))}.', f'The range of the principal value branch of {f} is {BRANCH[f][1]}.', 'd',
                  f'{pif(-(1 - v))} is outside {BRANCH[f][1]}; the principal value is {pif(v)}. A false, R true.')
    g = r.choice(['sin⁻¹', 'cos⁻¹'])
    x = r.choice(['2', '3/2', '−2', '√3', '−5/3'])
    return ar(f'{g}({x}) is not defined.', f'The domain of {g} is [−1, 1].', 'a', f'{x} lies outside [−1, 1].')


def c2s1_explain(r):
    return xbank([
        ('Why is the domain of sin x restricted to [−π/2, π/2] to define sin⁻¹x?', 'On [−π/2, π/2], sin is one-one and onto [−1, 1].', 'A function has an inverse only if it is a bijection; sin is not one-one on R, but it is on [−π/2, π/2] with range [−1, 1].'),
        ('Why is the principal value branch of cos⁻¹x taken as [0, π] and not [−π/2, π/2]?', 'cos is not one-one on [−π/2, π/2] but is one-one on [0, π].', 'cos(−θ) = cos θ, so the interval [−π/2, π/2] gives repeated values; on [0, π] cos decreases from 1 to −1.'),
        ('Explain why tan⁻¹x is defined for every real x.', 'tan maps (−π/2, π/2) one-one onto R.', 'tan is increasing on (−π/2, π/2) and takes every real value, so its inverse has domain R.'),
        ('Explain why sec⁻¹(1/2) is not defined.', '|sec θ| ≥ 1 for all θ.', 'The domain of sec⁻¹ is R − (−1, 1); 1/2 lies in (−1, 1).'),
        ('Explain why sin⁻¹x ≠ (sin x)⁻¹.', 'sin⁻¹x is an angle whose sine is x; (sin x)⁻¹ = 1/sin x = cosec x.', 'The notation ⁻¹ denotes the inverse function, not a reciprocal.'),
    ])(r)


def c2s1_case(r):
    f = r.choice(['sin⁻¹', 'cos⁻¹'])
    a = r.choice([2, 3, 4])
    b = r.randint(-3, 3)
    lo, hi = sorted([Fr(-1 - b, a), Fr(1 - b, a)])
    arg, v = r.choice([x for x in INV[f] if x[0] not in ('0', '1')])
    who = name(r)
    return Q((f'{who} is studying the function y = {f}x for a project on ramps. (i) Write the domain and the range of the principal value branch of {f}x. '
              f'(ii) Find the principal value of {f}({arg}). (iii) Find the domain of y = {f}({poly([a, b])}).'),
             f'(i) domain {BRANCH[f][0]}, range {BRANCH[f][1]} (ii) {pif(v)} (iii) {_interval(lo, hi)}',
             f'(i) 1 mark (ii) value in the branch (1 mark) (iii) −1 ≤ {poly([a, b])} ≤ 1 ⇒ {_interval(lo, hi)} (2 marks).')


GRAPH_FACTS = [
    ('The graph of y = sin⁻¹x can be obtained from the graph of y = sin x (restricted to [−π/2, π/2]) by …', 'reflecting it in the line y = x', ['reflecting it in the x-axis', 'reflecting it in the y-axis', 'shifting it by π/2'], 'Graphs of a function and its inverse are mirror images in y = x.'),
    ('On its domain, the function y = cos⁻¹x is …', 'strictly decreasing', ['strictly increasing', 'constant', 'periodic'], 'Its graph falls from (−1, π) to (1, 0).'),
    ('On its domain, the function y = sin⁻¹x is …', 'strictly increasing', ['strictly decreasing', 'constant', 'periodic'], 'Its graph rises from (−1, −π/2) to (1, π/2).'),
    ('The graph of y = tan⁻¹x has horizontal asymptotes …', 'y = π/2 and y = −π/2', ['x = π/2 and x = −π/2', 'y = 0 and y = π', 'y = 1 and y = −1'], 'tan⁻¹x → ±π/2 as x → ±∞.'),
    ('The graph of y = cot⁻¹x lies between the lines …', 'y = 0 and y = π', ['y = −π/2 and y = π/2', 'x = 0 and x = π', 'y = −1 and y = 1'], 'Range of cot⁻¹ is (0, π).'),
    ('The graph of y = sin⁻¹x passes through the point …', '(1, π/2)', ['(π/2, 1)', '(1, 0)', '(0, π/2)'], 'sin⁻¹1 = π/2.'),
    ('The graph of y = cos⁻¹x meets the y-axis at …', '(0, π/2)', ['(0, 0)', '(0, π)', '(π/2, 0)'], 'cos⁻¹0 = π/2.'),
    ('The graph of y = sec⁻¹x has a horizontal asymptote …', 'y = π/2', ['y = 0', 'y = π', 'x = 1'], 'sec⁻¹x → π/2 as x → ±∞ and never equals π/2.'),
    ('The graph of y = sin⁻¹x is symmetric about …', 'the origin', ['the y-axis', 'the x-axis', 'the line y = x'], 'sin⁻¹(−x) = −sin⁻¹x: an odd function.'),
    ('The graph of y = tan⁻¹x crosses the x-axis at …', 'the origin only', ['x = π/4', 'x = 1', 'no point'], 'tan⁻¹x = 0 only for x = 0.'),
]


def c2s2_mcq(r):
    return mcqbank(GRAPH_FACTS)(r)


def c2s2_point(r):
    f = r.choice(['sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'cot⁻¹'])
    arg, v = r.choice(INV[f])
    wrong = []
    for g, lst in INV.items():
        for a2, v2 in lst:
            if g == f and a2 == arg:
                continue
            if g == f and v2 != v:
                wrong.append(f'({a2}, {pif(v)})')
    wrong = list(dict.fromkeys(wrong))
    r.shuffle(wrong)
    wrong = wrong[:2] + [f'({pif(v)}, {arg})' if v else f'({arg}, π)']
    return mcq(f'Which of the following points lies on the graph of y = {f}x?', f'({arg}, {pif(v)})', wrong,
               f'{f}({arg}) = {pif(v)}.', r)


def c2s2_read(r):
    f = r.choice(['sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'cot⁻¹', 'sec⁻¹', 'cosec⁻¹'])
    pts = r.sample(INV[f], 2)
    return Q(f'Find the y-coordinates of the points on the graph of y = {f}x whose x-coordinates are {pts[0][0]} and {pts[1][0]}. Mark which of the two points is higher on the graph.',
             f'{pif(pts[0][1])} and {pif(pts[1][1])}; higher: x = {max(pts, key=lambda p: p[1])[0]}',
             f'Principal values {f}({pts[0][0]}) = {pif(pts[0][1])}, {f}({pts[1][0]}) = {pif(pts[1][1])} (1 mark each).',
             [f'{pif(pts[1][1])} and {pif(pts[0][1])}; higher: x = {min(pts, key=lambda p: p[1])[0]}', f'{pif(-pts[0][1])} and {pif(-pts[1][1])}; higher: x = {min(pts, key=lambda p: p[1])[0]}',
              f'{pif(pts[0][1] / 2)} and {pif(pts[1][1] / 2)}; higher: x = {max(pts, key=lambda p: p[1])[0]}'])


def c2s2_explain(r):
    return xbank([
        ('Sketch the graph of y = sin⁻¹x and state its domain and range. Explain how it is related to the graph of y = sin x.', 'Domain [−1, 1], range [−π/2, π/2]; mirror image of y = sin x (−π/2 ≤ x ≤ π/2) in y = x.',
         'Curve through (−1, −π/2), (0, 0), (1, π/2), increasing (1 mark); relation to sin x (1 mark).'),
        ('Sketch the graph of y = cos⁻¹x and state its domain and range.', 'Domain [−1, 1], range [0, π]; decreasing from (−1, π) through (0, π/2) to (1, 0).', 'Shape and key points (1 mark); domain and range (1 mark).'),
        ('Sketch the graph of y = tan⁻¹x and write its asymptotes.', 'Increasing curve through the origin with asymptotes y = ±π/2.', 'Shape (1 mark); asymptotes (1 mark).'),
        ('Explain, using graphs, why sin⁻¹x has range [−π/2, π/2] while cos⁻¹x has range [0, π].', 'Each is the reflection in y = x of the part of the graph on which the function is one-one.', 'sin is one-one on [−π/2, π/2]; cos is one-one on [0, π] (2 marks).'),
        ('The graphs of y = sin⁻¹x and y = cos⁻¹x intersect at one point. Find it.', '(1/√2, π/4)', 'sin⁻¹x = cos⁻¹x ⇒ the angle θ has sin θ = cos θ with θ in both branches ⇒ θ = π/4, x = 1/√2 (2 marks).'),
    ])(r)


def c2s2_ar(r):
    f = r.choice(['sin⁻¹', 'tan⁻¹', 'cosec⁻¹'])
    arg, v = r.choice([x for x in INV[f] if x[1] > 0])
    g = r.choice(['cos⁻¹', 'cot⁻¹'])
    a2, v2 = r.choice([x for x in INV[g] if 0 < x[1] < Fr(1, 2)])
    return arbank([
        (f'The graph of y = {f}x is symmetric about the origin, so {f}(−{arg}) = {pif(-v)}.', f'{f}(−x) = −{f}x for x in the domain.', 'a', 'Odd function: symmetric about the origin.'),
        (f'{g}(−{a2}) = −{pif(v2)}.', f'The graph of y = {g}x lies above the x-axis.', 'd', f'Values of {g} lie in {BRANCH[g][1]}, so they are not negative: {g}(−{a2}) = π − {pif(v2)} = {pif(1 - v2)}. A false, R true.'),
        ('The graph of y = sin⁻¹x is the mirror image of y = sin x (−π/2 ≤ x ≤ π/2) in the line y = x.', 'The graphs of a bijection and its inverse are reflections of each other in y = x.', 'a', 'Interchanging x and y reflects in y = x.'),
        ('The graph of y = tan⁻¹x never meets the line y = π/2.', 'The range of tan⁻¹ is the open interval (−π/2, π/2).', 'a', 'π/2 is not attained.'),
    ])(r)


def c2s2_case(r):
    f = r.choice(['sin⁻¹', 'cos⁻¹'])
    pts = r.sample(INV[f], 3)
    arg, v = pts[0]
    who = name(r)
    return Q((f'{who} plots y = {f}x on graph paper for a mathematics exhibition. (i) Write the coordinates of the end points of the graph. '
              f'(ii) Find the y-coordinates where x = {pts[1][0]} and x = {pts[2][0]}. (iii) Is the graph rising or falling from left to right? Explain using two plotted points.'),
             f'(i) {"(−1, −π/2) and (1, π/2)" if f == "sin⁻¹" else "(−1, π) and (1, 0)"} (ii) {pif(pts[1][1])}, {pif(pts[2][1])} (iii) {"rising (strictly increasing)" if f == "sin⁻¹" else "falling (strictly decreasing)"}',
             '(i) 1 mark (ii) 1 mark (iii) reason with points (2 marks).')


def _red(f, t):
    """Principal value of f⁻¹(f(tπ)) for f in sin, cos, tan; t is a Fraction (multiple of π)."""
    if f == 'sin':
        u = (t + Fr(1, 2)) % 2 - Fr(1, 2)        # in [−1/2, 3/2)
        return u if u <= Fr(1, 2) else 1 - u
    if f == 'cos':
        u = t % 2
        return u if u <= 1 else 2 - u
    u = (t + Fr(1, 2)) % 1 - Fr(1, 2)
    if u == Fr(-1, 2):
        raise ValueError
    return u


def c2s3_eval(r):
    fs = r.sample(list(INV), r.choice([2, 3]))
    terms, tot, naive = [], Fr(0), Fr(0)
    for i, f in enumerate(fs):
        arg, v = r.choice(INV[f])
        c = r.choice([1, 1, 2, -1])
        terms.append((c, f, arg, v))
        tot += c * v
    s = ''
    for c, f, arg, v in terms:
        t = f'{f}({arg})'
        if s == '':
            s = ('−' if c < 0 else '') + ('2 ' if abs(c) == 2 else '') + t
        else:
            s += (' − ' if c < 0 else ' + ') + ('2 ' if abs(c) == 2 else '') + t
    wrong = [pif(tot + Fr(1, 6)), pif(tot - Fr(1, 3)), pif(-tot) if tot else pif(Fr(1, 2)), pif(tot + Fr(1, 2)), pif(tot + 1)]
    return Q(f'Find the value of {s}.', pif(tot), '; '.join(f'{f}({arg}) = {pif(v)}' for c, f, arg, v in terms) + f'; value = {pif(tot)}.', dist3(pif(tot), wrong))


def c2s3_pv(r):
    f = r.choice(list(INV))
    arg, v = r.choice([x for x in INV[f] if x[0].startswith('−')] or INV[f])
    wrong = dist3(pif(v), [pif(_wrong_pv(f, v)), pif(-v), pif(v + Fr(1, 2)), pif(1 - v), pif(v / 2)])
    return Q(f'Find the principal value of {f}({arg}).', pif(v), f'The principal value lies in {BRANCH[f][1]}: {f}({arg}) = {pif(v)}.', wrong)


def c2s3_reduce(r):
    f = r.choice(['sin', 'cos', 'tan'])
    while True:
        d = r.choice([3, 4, 5, 6, 7, 8])
        n = r.randint(-2 * d, 3 * d)
        t = Fr(n, d)
        try:
            v = _red(f, t)
        except ValueError:
            continue
        if v != t and t.denominator > 1:
            break
    wrong = dist3(pif(v), [pif(t), pif(-v) if v else pif(Fr(1, 2)), pif(1 - v), pif(v + Fr(1, 2))])
    branch = {'sin': '[−π/2, π/2]', 'cos': '[0, π]', 'tan': '(−π/2, π/2)'}[f]
    return Q(f'Find the value of {f}⁻¹({f} {pif(t)}).', pif(v),
             f'{pif(t)} is not in {branch}; find the angle θ in {branch} with {f} θ = {f} {pif(t)}: θ = {pif(v)} (so the answer is not {pif(t)}).', wrong)


def c2s3_mixed(r):
    kind = r.randint(0, 2)
    if kind == 0:
        f = r.choice(['sin', 'cos', 'tan'])
        g = r.choice(['sin⁻¹', 'cos⁻¹', 'tan⁻¹'])
        arg, v = r.choice([x for x in INV[g] if x[1] != 0])
        e = {'sin': {Fr(1, 6): '1/2', Fr(1, 4): '1/√2', Fr(1, 3): '√3/2', Fr(1, 2): '1', Fr(2, 3): '√3/2', Fr(3, 4): '1/√2', Fr(5, 6): '1/2', Fr(1): '0',
                     Fr(-1, 6): '−1/2', Fr(-1, 4): '−1/√2', Fr(-1, 3): '−√3/2', Fr(-1, 2): '−1'},
             'cos': {Fr(1, 6): '√3/2', Fr(1, 4): '1/√2', Fr(1, 3): '1/2', Fr(1, 2): '0', Fr(2, 3): '−1/2', Fr(3, 4): '−1/√2', Fr(5, 6): '−√3/2', Fr(1): '−1',
                     Fr(-1, 6): '√3/2', Fr(-1, 4): '1/√2', Fr(-1, 3): '1/2', Fr(-1, 2): '0'},
             'tan': {Fr(1, 6): '1/√3', Fr(1, 4): '1', Fr(1, 3): '√3', Fr(2, 3): '−√3', Fr(3, 4): '−1', Fr(5, 6): '−1/√3', Fr(1): '0',
                     Fr(-1, 6): '−1/√3', Fr(-1, 4): '−1', Fr(-1, 3): '−√3'}}[f]
        if v not in e:
            raise ValueError
        ans = e[v]
        others = [x for x in ['0', '1', '−1', '1/2', '−1/2', '√3/2', '−√3/2', '1/√2', '√3', '1/√3', '−1/√3'] if x != ans]
        r.shuffle(others)
        return Q(f'Evaluate {f}({g}({arg})).', ans, f'{g}({arg}) = {pif(v)}; {f} {pif(v)} = {ans}.', others[:3])
    if kind == 1:
        arg, v = r.choice(INV['sin⁻¹'][1:5])
        arg2, v2 = r.choice(INV['cos⁻¹'][5:9])
        tot = v + v2
        return Q(f'Find the value of tan⁻¹(1) + cos⁻¹({arg2}) + sin⁻¹({"−" + arg if not arg.startswith("−") else arg[1:]}).',
                 pif(Fr(1, 4) + v2 - v), f'= π/4 + {pif(v2)} − {pif(v)} = {pif(Fr(1, 4) + v2 - v)}.',
                 dist3(pif(Fr(1, 4) + v2 - v), [pif(Fr(1, 4) - v2 - v), pif(Fr(1, 4) + v2 + v), pif(Fr(1, 4) - (1 - v2) - v), pif(tot)]))
    arg, v = r.choice(INV['cos⁻¹'][5:9])
    arg2, v2 = r.choice(INV['sin⁻¹'][5:9])
    return Q(f'Find the value of cos⁻¹({arg}) − 2 sin⁻¹({arg2}).', pif(v - 2 * v2), f'cos⁻¹({arg}) = {pif(v)}, sin⁻¹({arg2}) = {pif(v2)}; {pif(v)} − 2({pif(v2)}) = {pif(v - 2 * v2)}.',
             dist3(pif(v - 2 * v2), [pif(v + 2 * v2), pif(-(1 - v) - 2 * v2), pif(v - v2), pif(-(1 - v) + 2 * v2)]))


def c2s3_mcq(r):
    return mcqbank([
        ('The principal value of cos⁻¹(−1/2) is …', '2π/3', ['−π/3', 'π/3', '4π/3'], 'cos⁻¹(−x) = π − cos⁻¹x = π − π/3.'),
        ('The value of sin⁻¹(sin 3π/5) is …', '2π/5', ['3π/5', '−2π/5', 'π/5'], '3π/5 ∉ [−π/2, π/2]; sin(3π/5) = sin(π − 3π/5) = sin(2π/5).'),
        ('The principal value of tan⁻¹(−√3) is …', '−π/3', ['2π/3', 'π/3', '5π/6'], 'Range (−π/2, π/2).'),
        ('The value of cos⁻¹(cos 7π/6) is …', '5π/6', ['7π/6', 'π/6', '−5π/6'], 'cos(7π/6) = cos(2π − 7π/6) = cos(5π/6), and 5π/6 ∈ [0, π].'),
        ('The principal value of sec⁻¹(−2) is …', '2π/3', ['−π/3', '4π/3', 'π/3'], 'Range [0, π] − {π/2}: sec(2π/3) = −2.'),
        ('The principal value of cot⁻¹(−1) is …', '3π/4', ['−π/4', '5π/4', 'π/4'], 'Range (0, π).'),
        ('The value of tan⁻¹(tan 3π/4) is …', '−π/4', ['3π/4', 'π/4', '−3π/4'], 'tan(3π/4) = −1 and the principal value of tan⁻¹(−1) is −π/4.'),
    ])(r)


def c2s3_ar(r):
    f = r.choice(['sin', 'cos'])
    d = r.choice([5, 6, 7, 8])
    n = r.randint(d + 1, 2 * d - 1) if f == 'cos' else r.randint(d // 2 + 1, d - 1)
    t = Fr(n, d)
    v = _red(f, t)
    if v == t:
        raise ValueError
    br = '[−π/2, π/2]' if f == 'sin' else '[0, π]'
    if r.random() < 0.5:
        return ar(f'{f}⁻¹({f} {pif(t)}) = {pif(v)}.', f'{f}⁻¹({f} x) = x only when x lies in {br}.', 'a', f'{pif(t)} ∉ {br}; the equivalent angle in the branch is {pif(v)}.')
    return ar(f'{f}⁻¹({f} {pif(t)}) = {pif(t)}.', f'{f}⁻¹({f} x) = x only when x lies in {br}.', 'd', f'A is false: the value is {pif(v)}; R is true.')


def c2s3_case(r):
    a1, v1 = r.choice(INV['sin⁻¹'][1:])
    a2, v2 = r.choice(INV['cos⁻¹'][1:8])
    f = r.choice(['sin', 'cos'])
    d = r.choice([5, 6, 7])
    t = Fr(r.randint(d + 1, 2 * d - 1), d)
    v = _red(f, t)
    who1, who2 = two_names(r)
    return Q((f'In a quiz on inverse trigonometric functions, {who1} and {who2} are given three tasks. (i) Find the principal value of sin⁻¹({a1}). (ii) Find cos⁻¹({a2}). '
              f'(iii) {who2} writes {f}⁻¹({f} {pif(t)}) = {pif(t)}. Is this correct? If not, find the correct value.'),
             f'(i) {pif(v1)} (ii) {pif(v2)} (iii) No; {pif(v)}', f'(i) 1 mark (ii) 1 mark (iii) {pif(t)} is outside the principal branch; equivalent angle {pif(v)} (2 marks).')


def c2s3_long(r):
    picks = []
    for f in r.sample(list(INV), 3):
        arg, v = r.choice([x for x in INV[f] if x[1] != 0])
        picks.append((f, arg, v))
    f, dd = r.choice(['sin', 'cos', 'tan']), r.choice([5, 6, 7, 8])
    t = Fr(r.randint(dd + 1, 3 * dd), dd)
    try:
        v = _red(f, t)
    except ValueError:
        raise
    tot = picks[0][2] + picks[1][2] - picks[2][2]
    return Q(f'Evaluate: (i) {picks[0][0]}({picks[0][1]}) + {picks[1][0]}({picks[1][1]}) − {picks[2][0]}({picks[2][1]}) (ii) {f}⁻¹({f} {pif(t)}). Show the principal branch used at each step.',
             f'(i) {pif(tot)} (ii) {pif(v)}', '(i) each principal value 1 mark, combination 1 mark (ii) reduction to the principal branch (1 mark).')


# ======================================================================= ch03 Matrices

def c3s1_mcq(r):
    k = r.randint(2, 9)
    return mcqbank([
        ('A square matrix in which every non-diagonal element is zero is called …', 'a diagonal matrix', ['a scalar matrix', 'a zero matrix', 'a row matrix'], 'Definition (NCERT 3.3).'),
        ('A diagonal matrix in which all the diagonal elements are equal is called …', 'a scalar matrix', ['an identity matrix', 'a zero matrix', 'a column matrix'], 'Definition of scalar matrix.'),
        (f'The matrix [{k}, 0; 0, {k}] is …', 'a scalar matrix', ['an identity matrix', 'a zero matrix', 'a row matrix'], f'Diagonal with equal entries {k}.'),
        ('A matrix having only one column is called …', 'a column matrix', ['a row matrix', 'a square matrix', 'a diagonal matrix'], 'Order m × 1.'),
        ('A matrix of order 1 × n is …', 'a row matrix', ['a column matrix', 'a square matrix', 'a scalar matrix'], 'One row.'),
        ('Two matrices A = [aᵢⱼ] and B = [bᵢⱼ] are equal if …', 'they have the same order and aᵢⱼ = bᵢⱼ for all i, j', ['they have the same order only', 'they have the same number of elements', 'their diagonal elements are equal'], 'Definition of equality.'),
        ('The number of all possible matrices of order 3 × 3 with each entry 0 or 1 is …', '512', ['27', '18', '81'], '2⁹ = 512.'),
        ('The number of all possible matrices of order 2 × 2 with each entry 0 or 1 is …', '16', ['4', '8', '32'], '2⁴ = 16.'),
    ])(r)


def c3s1_orders(r):
    n = r.choice([4, 6, 8, 9, 10, 12, 13, 15, 16, 18, 20, 24, 5, 7, 11, 30, 36])
    ords = [f'{d} × {n // d}' for d in range(1, n + 1) if n % d == 0]
    wrong = [f'{len(ords) + 1} orders', f'{len(ords) - 1} orders' if len(ords) > 2 else '1 order', f'{2 * len(ords)} orders']
    return Q(f'If a matrix has {n} elements, what are the possible orders it can have?', f'{len(ords)} orders: {", ".join(ords)}',
             f'Order m × n with mn = {n}: {", ".join(ords)}.', [f'{w}' for w in wrong])


FORMULAS = [
    ('(i + j)²/2', lambda i, j: Fr((i + j) ** 2, 2)),
    ('(i − j)²/2', lambda i, j: Fr((i - j) ** 2, 2)),
    ('i/j', lambda i, j: Fr(i, j)),
    ('|−3i + j|/2', lambda i, j: Fr(abs(-3 * i + j), 2)),
    ('2i − j', lambda i, j: Fr(2 * i - j)),
    ('i + 2j', lambda i, j: Fr(i + 2 * j)),
    ('ij', lambda i, j: Fr(i * j)),
    ('(2i + j)²/2', lambda i, j: Fr((2 * i + j) ** 2, 2)),
    ('i² − j', lambda i, j: Fr(i * i - j)),
    ('3i − 2j', lambda i, j: Fr(3 * i - 2 * j)),
    ('(i + 2j)²/2', lambda i, j: Fr((i + 2 * j) ** 2, 2)),
]


def c3s1_construct(r):
    txt, f = r.choice(FORMULAS)
    m, n = r.choice([(2, 2), (2, 3), (3, 2), (3, 3), (3, 4)])
    M = [[f(i, j) for j in range(1, n + 1)] for i in range(1, m + 1)]
    W = [[f(j, i) for j in range(1, n + 1)] for i in range(1, m + 1)]
    W2 = [[f(i, j) + 1 for j in range(1, n + 1)] for i in range(1, m + 1)]
    W3 = tr(M) if m != n else [[f(i, j) * 2 for j in range(1, n + 1)] for i in range(1, m + 1)]
    return Q(f'Construct a {m} × {n} matrix A = [aᵢⱼ] whose elements are given by aᵢⱼ = {txt}.', f'A = {mstr(M)}',
             f'Substitute i = 1…{m}, j = 1…{n}: A = {mstr(M)}.', dist3(f'A = {mstr(M)}', [f'A = {mstr(W)}', f'A = {mstr(W2)}', f'A = {mstr(W3)}']))


def c3s1_equal(r):
    kind = r.randint(0, 2)
    if kind == 0:
        x, y = r.randint(-6, 9), r.randint(-6, 9)
        p, q = r.randint(-9, 9), r.randint(-9, 9)
        return Q(f'Find x and y if [x + y, {p}; {q}, x − y] = [{x + y}, {p}; {q}, {x - y}].', f'x = {x}, y = {y}',
                 f'Equal matrices: x + y = {x + y}, x − y = {x - y} ⇒ x = {x}, y = {y}.', [f'x = {y}, y = {x}' if x != y else f'x = {x + 1}, y = {y - 1}', f'x = {x + y}, y = {x - y}', f'x = {-x}, y = {-y}' if x or y else 'x = 1, y = 1'])
    if kind == 1:
        a, b = r.sample(range(1, 9), 2)
        c, d = r.randint(-5, 5), r.randint(1, 6)
        return Q(f'Find a, b, c and d if [a − b, 2a + c; 2a − b, 3c + d] = [{a - b}, {2 * a + c}; {2 * a - b}, {3 * c + d}].', f'a = {a}, b = {b}, c = {c}, d = {d}',
                 f'a − b = {a - b} and 2a − b = {2 * a - b} ⇒ a = {a}, b = {b} (1 mark); 2a + c = {2 * a + c} ⇒ c = {c}; 3c + d = {3 * c + d} ⇒ d = {d} (1 mark).',
                 [f'a = {b}, b = {a}, c = {c}, d = {d}', f'a = {a}, b = {b}, c = {-c}, d = {d + 6 * c}' if c else f'a = {a}, b = {b}, c = 1, d = {d - 3}', f'a = {a + 1}, b = {b + 1}, c = {c - 2}, d = {d}'])
    a, b = r.sample(range(1, 9), 2)
    return Q(f'Find x and y if [x + y, 2; 5, xy] = [{a + b}, 2; 5, {a * b}].', f'x = {a}, y = {b} or x = {b}, y = {a}',
             f'x + y = {a + b}, xy = {a * b} ⇒ x, y are roots of t² − {a + b}t + {a * b} = 0, i.e. {a} and {b}.',
             [f'x = {a + b}, y = {a * b}', f'x = {a}, y = {a}', f'x = {-a}, y = {-b}'])


def c3s1_count(r):
    m, n = r.randint(1, 3), r.randint(2, 3)
    k = r.choice([2, 3])
    ents = '0 or 1' if k == 2 else '0, 1 or 2'
    ans = k ** (m * n)
    return Q(f'How many matrices of order {m} × {n} can be formed if each entry is {ents}?', str(ans), f'{m * n} entries, each with {k} choices: {k}{_sup(m * n)} = {ans}.',
             [str(k * m * n), str((m * n) ** k), str(ans // k)])


def c3s1_ar(r):
    k, m = r.sample(range(2, 10), 2)
    return arbank([
        (f'[{k}, 0; 0, {k}] is a scalar matrix.', 'A diagonal matrix with all diagonal elements equal is a scalar matrix.', 'a', 'Definition applies.'),
        (f'[{k}, 0; 0, {m}] is a scalar matrix.', 'A diagonal matrix with all diagonal elements equal is a scalar matrix.', 'd', f'Diagonal entries {k} ≠ {m}; A false, R true.'),
        (f'[1, 0; 0, 1] is an identity matrix.', 'Every diagonal matrix is an identity matrix.', 'c', 'A true; R false (e.g. [2, 0; 0, 3]).'),
        (f'A matrix with {k * m} elements can have order {k} × {m}.', 'A matrix of order p × q has pq elements.', 'a', f'{k} × {m} = {k * m}.'),
        (f'[{k}, {m}] and [{k}; {m}] are equal matrices.', 'Equal matrices must have the same order.', 'd', 'Orders 1 × 2 and 2 × 1 differ; A false, R true.'),
    ])(r)


def c3s1_case(r):
    shops = r.sample(['Sharma Stores', 'Gupta Traders', 'Iyer Mart', 'Khan General Store', 'Patel Provisions', 'Singh Bazaar'], 3)
    items = r.sample(['notebooks', 'pens', 'geometry boxes', 'calculators', 'files', 'water bottles'], 2)
    M = [[r.randint(10, 90) for _ in range(2)] for _ in range(3)]
    i, j = r.randint(1, 3), r.randint(1, 2)
    tot = sum(M[k][j - 1] for k in range(3))
    return Q((f'Three shops {", ".join(shops)} in {r.choice(CITIES)} sold {items[0]} and {items[1]} in a week: the sales are recorded in the matrix A = {mstr(M)} (rows: shops in the order given; columns: {items[0]}, {items[1]}). '
              f'(i) Write the order of A. (ii) What does a{_sub(i)}{_sub(j)} = {M[i - 1][j - 1]} represent? (iii) Find the total number of {items[j - 1]} sold by the three shops, and write Aᵀ\'s order.'),
             f'(i) 3 × 2 (ii) {shops[i - 1]} sold {M[i - 1][j - 1]} {items[j - 1]} (iii) {tot}; order of Aᵀ is 2 × 3',
             '(i) 1 mark (ii) 1 mark (iii) column sum 1 mark, order 1 mark.')


def _sub(n):
    return str(n).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))


def c3s1_explain(r):
    return xbank([
        ('Explain why a matrix with a prime number p of elements can have only two orders.', 'p = 1 × p = p × 1 only.', 'The only factorisations of a prime are 1 × p and p × 1.'),
        ('Explain why every identity matrix is a scalar matrix but not every scalar matrix is an identity matrix.', 'Identity has all diagonal entries 1; scalar allows any equal value.', '[2, 0; 0, 2] is scalar but not identity.'),
        ('Can a zero matrix be a square matrix? Can it be a row matrix? Explain.', 'Yes to both.', 'A zero matrix is any matrix of zeros, of any order, e.g. [0, 0; 0, 0] and [0, 0, 0].'),
        ('Explain why [2, 3] and [2; 3] are not equal matrices.', 'Their orders differ (1 × 2 and 2 × 1).', 'Equality needs the same order and equal corresponding entries.'),
    ])(r)


# ---- st2 operations

def c3s2_lin(r):
    m, n = r.choice([(2, 2), (2, 3), (3, 2)])
    A, B = rand_mat(r, m, n, -4, 6), rand_mat(r, m, n, -4, 6)
    p, q = r.choice([2, 3, 1, -1]), r.choice([-2, -3, 2, 3, -1])
    C = madd(A, B, p, q)
    expr = f'{"" if p == 1 else "−" if p == -1 else p}A {"+" if q > 0 else "−"} {"" if abs(q) == 1 else abs(q)}B'
    return Q(f'If A = {mstr(A)} and B = {mstr(B)}, find {expr}.', mstr(C), f'Multiply each entry by the scalar and add corresponding entries: {mstr(C)}.',
             dist3(mstr(C), [mstr(madd(A, B, p, -q)), mstr(madd(A, B, q, p)), mstr(madd(A, B, p, q + 1))]))


def c3s2_mul(r):
    shape = r.choice([(2, 2, 2), (2, 3, 2), (3, 2, 2), (2, 2, 3), (3, 3, 3)])
    m, k, n = shape
    A, B = rand_mat(r, m, k, -3, 5), rand_mat(r, k, n, -3, 5)
    C = mmul(A, B)
    W1 = [[Fr(A[i][j]) * B[i][j] for j in range(n)] for i in range(m)] if (m, k) == (k, n) else mmul(A, B)[::-1]
    W2 = mmul(B, A) if m == n and k == m else [row[::-1] for row in C]
    W3 = madd(C, [[1 if i == j else 0 for j in range(n)] for i in range(m)])
    return Q(f'Find AB, where A = {mstr(A)} and B = {mstr(B)}.', mstr(C), f'(AB)ᵢⱼ = Σ aᵢₖbₖⱼ (row of A times column of B): AB = {mstr(C)}.', dist3(mstr(C), [mstr(W1), mstr(W2), mstr(W3)]))


def c3s2_order(r):
    m, n, p = r.sample(range(2, 6), 3)
    kind = r.randint(0, 1)
    if kind == 0:
        return Q(f'If A is a matrix of order {m} × {n} and B is of order {n} × {p}, what is the order of AB? Is BA defined?', f'{m} × {p}; BA is not defined',
                 f'AB: ({m} × {n})({n} × {p}) = {m} × {p}; BA needs {p} = {m}, which is false.', [f'{n} × {n}; BA is defined', f'{p} × {m}; BA is not defined', f'{m} × {n}; BA is defined'])
    return Q(
        f'If A is a {m} × {n} matrix and AB and BA are both defined, what must be the order of B? Then write the orders of AB and BA.', f'B is {n} × {m}; AB is {m} × {m}, BA is {n} × {n}',
        f'AB defined ⇒ B has {n} rows; BA defined ⇒ B has {m} columns.', [f'B is {m} × {n}; AB is {m} × {n}, BA is {n} × {m}', f'B is {n} × {n}; AB is {m} × {n}, BA is not defined', f'B is {m} × {m}; AB is {n} × {n}, BA is {m} × {m}'])


def c3s2_ch(r):
    while True:
        A = rand_mat(r, 2, 2, -3, 6)
        t, d = A[0][0] + A[1][1], det(A)
        if t != 0 and d != 0:
            break
    x, y = -t, d
    return Q(f'If A = {mstr(A)}, find the values of x and y such that A² + xA + yI = O.', f'x = {fz(x)}, y = {fz(y)}',
             f'A² = {mstr(mmul(A, A))} (1 mark); compare entries of A² + xA + yI with O (1 mark): x = {fz(x)}, y = {fz(y)} (1 mark).',
             [f'x = {fz(t)}, y = {fz(d)}', f'x = {fz(x)}, y = {fz(-y)}', f'x = {fz(d)}, y = {fz(t)}'])


def c3s2_ar(r):
    while True:
        A, B = rand_mat(r, 2, 2, -2, 4), rand_mat(r, 2, 2, -2, 4)
        if mmul(A, B) != mmul(B, A):
            break
    k = r.randint(2, 6)
    return arbank([
        (f'For A = {mstr(A)} and B = {mstr(B)}, AB ≠ BA.', 'Matrix multiplication is not commutative in general.', 'a', f'AB = {mstr(mmul(A, B))}, BA = {mstr(mmul(B, A))}.'),
        (f'For A = {mstr(A)} and B = {mstr(B)}, (A + B)² = A² + 2AB + B².', 'Matrix multiplication is associative.', 'd', '(A + B)² = A² + AB + BA + B² and AB ≠ BA here, so A is false; R is true.'),
        (f'For any square matrix A, A·({k}I) = ({k}I)·A.', 'A scalar matrix commutes with every square matrix of the same order.', 'a', f'{k}I·A = {k}A = A·{k}I.'),
        ('If AB = O then A = O or B = O.', 'The product of two non-zero matrices can be a zero matrix.', 'd', 'e.g. [0, 1; 0, 0]² = O; A is false, R is true.'),
    ])(r)


def c3s2_sales(r):
    items = r.sample(['pens', 'pencils', 'erasers', 'notebooks', 'markers', 'rulers'], 3)
    shops = r.sample(['A', 'B', 'C', 'D'], 2)
    Ssold = [[r.randint(5, 40) * 10 for _ in range(3)] for _ in range(2)]
    price = [Fr(r.randint(4, 30)) for _ in range(3)]
    cost = [p - Fr(r.randint(1, 3)) for p in price]
    rev = [sum(Ssold[i][j] * price[j] for j in range(3)) for i in range(2)]
    prof = [sum(Ssold[i][j] * (price[j] - cost[j]) for j in range(3)) for i in range(2)]
    city = r.choice(CITIES)
    return Q((f'Two stationery shops {shops[0]} and {shops[1]} in {city} sold {items[0]}, {items[1]} and {items[2]} in a month as given by the matrix S = {mstr(Ssold)} '
              f'(rows: shops {shops[0]}, {shops[1]}; columns: {", ".join(items)}). The selling prices are ₹{fz(price[0])}, ₹{fz(price[1])} and ₹{fz(price[2])} and the cost prices ₹{fz(cost[0])}, ₹{fz(cost[1])} and ₹{fz(cost[2])} per item respectively. '
              f'Using matrix multiplication, find the total revenue and the total profit of each shop.'),
             f'Revenue: {shops[0]} {inr(rev[0])}, {shops[1]} {inr(rev[1])}; profit: {shops[0]} {inr(prof[0])}, {shops[1]} {inr(prof[1])}',
             f'Revenue = S × P (column of selling prices) = {mstr([[x] for x in rev])} (2 marks); profit = S × (P − C) = {mstr([[x] for x in prof])} (2 marks); statement (1 mark).')


def c3s2_power(r):
    a = r.choice([1, 2, -1, 3])
    b = r.randint(1, 4)
    n = r.choice([3, 4, 5])
    A = [[a, b], [0, a]]
    An = [[a ** n, n * a ** (n - 1) * b], [0, a ** n]]
    return Q(f'If A = {mstr(A)}, find A² and A³, and hence write A{_sup(n)} by observing the pattern. Verify your A{_sup(n)} by direct multiplication.' if n > 3 else f'If A = {mstr(A)}, find A² and A³.',
             f'A{_sup(n)} = {mstr(An)}' if n > 3 else f'A² = {mstr(mmul(A, A))}, A³ = {mstr(An)}',
             f'A² = {mstr(mmul(A, A))} (1 mark), A³ = {mstr(mmul(mmul(A, A), A))} (2 marks); pattern Aⁿ = [aⁿ, n aⁿ⁻¹b; 0, aⁿ] (2 marks).')


def _c3s2_case2(r):
    fam = r.sample(['Rao', 'Mehta', 'Das', 'Kapoor', 'Nair', 'Reddy', 'Bose', 'Joshi'], 2)
    M = [[r.randint(1, 4) for _ in range(3)] for _ in range(2)]
    cost = [r.choice([60, 70, 80, 90, 100]), r.choice([50, 60, 70, 80]), r.choice([30, 40, 45, 50])]
    tot = [sum(M[i][j] * cost[j] for j in range(3)) for i in range(2)]
    diff = tot[0] - tot[1]
    cmp_ = f'{fam[0]} by ₹{diff}' if diff > 0 else f'{fam[1]} by ₹{-diff}' if diff < 0 else 'both spend the same'
    return Q((f'For a trip to {r.choice(CITIES)}, the {fam[0]} and {fam[1]} families have members given by F = {mstr(M)} (rows: {fam[0]}, {fam[1]}; columns: men, women, children). '
              f'The daily meal cost per person is ₹{cost[0]} for a man, ₹{cost[1]} for a woman and ₹{cost[2]} for a child, written as the column matrix C. '
              f'(i) Write the orders of F and C. (ii) Find FC and interpret it. (iii) Which family spends more per day on meals, and by how much?'),
             f'(i) F: 2 × 3, C: 3 × 1 (ii) FC = [{tot[0]}; {tot[1]}]: daily meal cost of each family (iii) {cmp_}',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c3s2_explain(r):
    return xbank([
        ('Explain why (A + B)² ≠ A² + 2AB + B² in general for square matrices A and B.', '(A + B)² = A² + AB + BA + B², and AB need not equal BA.', 'Expand using distributivity (1 mark); non-commutativity (1 mark).'),
        ('Explain, with an example, that AB = O does not imply A = O or B = O.', 'A = [0, 1; 0, 0] and B = [1, 0; 0, 0] are non-zero, but AB = [0, 0; 0, 0] = O.', 'Example with non-zero A, B (2 marks).'),
        ('If A and B are matrices such that AB and BA are both defined, explain why AB and BA are square matrices.', 'If A is m × n then B is n × m; AB is m × m and BA is n × n.', 'Order argument (2 marks).'),
        ('Explain why the product of a 2 × 3 matrix and a 2 × 3 matrix is not defined.', 'Columns of the first (3) ≠ rows of the second (2).', 'Condition for multiplication (2 marks).'),
    ])(r)


# ---- st3 transpose, symmetric, skew-symmetric

def c3s3_tr(r):
    m, n = r.choice([(2, 3), (3, 2), (3, 3), (2, 2)])
    A = rand_mat(r, m, n, -5, 9)
    return Q(f'Find the transpose of A = {mstr(A)} and write its order.', f'Aᵀ = {mstr(tr(A))}, order {n} × {m}', 'Rows of A become columns of Aᵀ.',
             dist3(f'Aᵀ = {mstr(tr(A))}, order {n} × {m}', [f'Aᵀ = {mstr([row[::-1] for row in A])}, order {m} × {n}', f'Aᵀ = {mstr(A[::-1])}, order {m} × {n}', f'Aᵀ = {mstr(mscale(tr(A), -1))}, order {n} × {m}']))


def c3s3_split(r):
    n = r.choice([2, 3])
    A = rand_mat(r, n, n, -4, 7)
    P = mscale(madd(A, tr(A)), Fr(1, 2))
    Qm = mscale(madd(A, tr(A), 1, -1), Fr(1, 2))
    return Q(f'Express the matrix A = {mstr(A)} as the sum of a symmetric and a skew-symmetric matrix.', f'P = {mstr(P)} (symmetric), Q = {mstr(Qm)} (skew-symmetric)',
             f'P = ½(A + Aᵀ) = {mstr(P)} (2 marks); Q = ½(A − Aᵀ) = {mstr(Qm)} (2 marks); check Pᵀ = P, Qᵀ = −Q and P + Q = A (1 mark).')


def c3s3_find(r):
    kind = r.randint(0, 1)
    a, b, c = r.randint(-6, 6), r.randint(-6, 6), r.randint(-6, 6)
    if kind == 0:
        k1, k2 = r.randint(1, 4), r.randint(-5, 5)
        return Q(f'If A = [{r.randint(1, 5)}, {a}, x + {k1}; {a}, {r.randint(-3, 3)}, {b}; {c}, y − {abs(k2)}, {r.randint(1, 6)}] is a symmetric matrix, find x and y.'.replace('− 0', '+ 0'),
                 f'x = {c - k1}, y = {b + abs(k2)}', f'Symmetric: a₁₃ = a₃₁ ⇒ x + {k1} = {c} and a₂₃ = a₃₂ ⇒ y − {abs(k2)} = {b}.',
                 [f'x = {c + k1}, y = {b - abs(k2)}', f'x = {-c - k1}, y = {-b + abs(k2)}', f'x = {c}, y = {b}'])
    return Q(f'If A = [0, {a}, x; {-a}, 0, {b}; {c}, y, 0] is a skew-symmetric matrix, find x and y.', f'x = {-c}, y = {-b}',
             f'Skew-symmetric: aᵢⱼ = −aⱼᵢ ⇒ x = −({c}) and y = −({b}).', [f'x = {c}, y = {b}', f'x = {-b}, y = {-c}' if b != c else f'x = {c + 1}, y = {b + 1}', f'x = {c}, y = {-b}' if c else f'x = 1, y = {-b}'])


def c3s3_mcq(r):
    return mcqbank([
        ('The diagonal elements of a skew-symmetric matrix are …', 'all zero', ['all equal to 1', 'all equal', 'any real numbers'], 'aᵢᵢ = −aᵢᵢ ⇒ aᵢᵢ = 0.'),
        ('If A is any square matrix, then A + Aᵀ is …', 'symmetric', ['skew-symmetric', 'a zero matrix', 'an identity matrix'], '(A + Aᵀ)ᵀ = Aᵀ + A.'),
        ('If A is any square matrix, then A − Aᵀ is …', 'skew-symmetric', ['symmetric', 'diagonal', 'scalar'], '(A − Aᵀ)ᵀ = −(A − Aᵀ).'),
        ('(AB)ᵀ is equal to …', 'BᵀAᵀ', ['AᵀBᵀ', 'AB', 'BA'], 'Reversal law for transposes.'),
        ('If A is a symmetric matrix, then Aᵀ = …', 'A', ['−A', 'O', 'I'], 'Definition.'),
        ('If A and B are symmetric matrices of the same order, then AB − BA is …', 'skew-symmetric', ['symmetric', 'a zero matrix', 'an identity matrix'], '(AB − BA)ᵀ = BA − AB.'),
        ('For any matrix A, (Aᵀ)ᵀ = …', 'A', ['Aᵀ', '−A', 'I'], 'Transposing twice returns A.'),
    ])(r)


def c3s3_verify(r):
    A, B = rand_mat(r, 2, 3, -3, 5), rand_mat(r, 3, 2, -3, 5)
    AB = mmul(A, B)
    return Q(f'For A = {mstr(A)} and B = {mstr(B)}, verify that (AB)ᵀ = BᵀAᵀ.', f'(AB)ᵀ = BᵀAᵀ = {mstr(tr(AB))}',
             f'AB = {mstr(AB)}, so (AB)ᵀ = {mstr(tr(AB))} (1 mark); BᵀAᵀ = {mstr(mmul(tr(B), tr(A)))} (1 mark); equal (1 mark).')


def c3s3_ar(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    return arbank([
        (f'The matrix [0, {a}, −{b}; −{a}, 0, {a + b}; {b}, −{a + b}, 0] is skew-symmetric.', 'A square matrix A is skew-symmetric if Aᵀ = −A.', 'a', 'Each aᵢⱼ = −aⱼᵢ and the diagonal is zero.'),
        (f'The matrix [{a}, {b}; −{b}, {a}] is skew-symmetric.', 'The diagonal elements of a skew-symmetric matrix are zero.', 'd', f'The diagonal has {a} ≠ 0, so A is false; R is true.'),
        ('Every square matrix can be written as the sum of a symmetric and a skew-symmetric matrix.', 'A = ½(A + Aᵀ) + ½(A − Aᵀ).', 'a', 'R gives the required decomposition.'),
        (f'For A = [{a}, {b}; {b}, {a + b}], the matrix A² is symmetric.', '(AB)ᵀ = BᵀAᵀ.', 'a', '(A²)ᵀ = AᵀAᵀ = A² as Aᵀ = A.'),
        ('A matrix which is both symmetric and skew-symmetric is the identity matrix.', 'If Aᵀ = A and Aᵀ = −A then A = −A.', 'd', 'Then A = O (the zero matrix), so A is false; R is true.'),
    ])(r)


def c3s3_case(r):
    n = 3
    A = rand_mat(r, 3, 3, -4, 7)
    P = mscale(madd(A, tr(A)), Fr(1, 2))
    Qm = mscale(madd(A, tr(A), 1, -1), Fr(1, 2))
    who = name(r)
    return Q((f'{who} records the number of messages sent between three friends in a week as the matrix A = {mstr(A)}, where aᵢⱼ is the number sent by friend i to friend j minus a fixed baseline. '
              f'(i) Find Aᵀ. (ii) Find the symmetric part P = ½(A + Aᵀ). (iii) Find the skew-symmetric part Q = ½(A − Aᵀ) and check that its diagonal entries are zero.'),
             f'(i) {mstr(tr(A))} (ii) {mstr(P)} (iii) {mstr(Qm)}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c3s3_explain(r):
    return xbank([
        ('Show that for any square matrix A, A + Aᵀ is symmetric and A − Aᵀ is skew-symmetric.', '(A + Aᵀ)ᵀ = A + Aᵀ; (A − Aᵀ)ᵀ = −(A − Aᵀ).', 'Use (Aᵀ)ᵀ = A and (A ± B)ᵀ = Aᵀ ± Bᵀ (1 mark each).'),
        ('Explain why all diagonal entries of a skew-symmetric matrix are zero.', 'aᵢᵢ = −aᵢᵢ ⇒ 2aᵢᵢ = 0.', 'Put i = j in aᵢⱼ = −aⱼᵢ (2 marks).'),
        ('If A and B are symmetric matrices of the same order, show that AB is symmetric if and only if AB = BA.', '(AB)ᵀ = BᵀAᵀ = BA.', 'AB symmetric ⇔ (AB)ᵀ = AB ⇔ BA = AB (2 marks).'),
        ('Show that the matrix BᵀAB is symmetric or skew-symmetric according as A is symmetric or skew-symmetric.', '(BᵀAB)ᵀ = BᵀAᵀB.', 'If Aᵀ = A it equals BᵀAB; if Aᵀ = −A it equals −BᵀAB (2 marks).'),
    ])(r)


# ---- st4 invertible matrices

def c3s4_verify(r):
    A = unimod(r, 2, (1, -1))
    B = inv(A)
    return Q(f'Show that B = {mstr(B)} is the inverse of A = {mstr(A)}.', 'AB = BA = I, so B = A⁻¹', f'AB = {mstr(mmul(A, B))} and BA = {mstr(mmul(B, A))} (1 mark each).')


def c3s4_formula(r):
    while True:
        A = rand_mat(r, 2, 2, -4, 8)
        d = det(A)
        if d not in (0,):
            break
    Ai = inv(A)
    W1 = mscale([[A[1][1], A[0][1]], [A[1][0], A[0][0]]], 1 / d)
    W2 = mscale(adj(A), d) if d not in (1, -1) else mscale(adj(A), -1)
    W3 = tr(Ai) if tr(Ai) != Ai else mscale(Ai, 2)
    return Q(f'Find the inverse of the matrix A = {mstr(A)}, if it exists.', f'A⁻¹ = {mstr(Ai)}', f'|A| = {fz(d)} ≠ 0; A⁻¹ = (1/|A|)[d, −b; −c, a] = {mstr(Ai)}.',
             dist3(f'A⁻¹ = {mstr(Ai)}', [f'A⁻¹ = {mstr(W1)}', f'A⁻¹ = {mstr(W2)}', f'A⁻¹ = {mstr(W3)}']))


def c3s4_poly(r):
    while True:
        A = rand_mat(r, 2, 2, -3, 6)
        t, d = A[0][0] + A[1][1], det(A)
        if d != 0 and t != 0:
            break
    Ai = inv(A)
    eq = f'A²{term(-t, "A")}{term(d, "I")}'
    return Q(f'For A = {mstr(A)}, show that {eq} = O and hence find A⁻¹.', f'A⁻¹ = {mstr(Ai)}',
             f'A² = {mstr(mmul(A, A))} (1 mark); {eq} = O verified (2 marks); multiply by A⁻¹: A{term(-t, "I")}{term(d, "A⁻¹")} = O ⇒ A⁻¹ = ({term(t, "I", first=True)} − A)/{fpar(d)} = {mstr(Ai)} (2 marks).')


def c3s4_mcq(r):
    return mcqbank([
        ('If A and B are invertible matrices of the same order, then (AB)⁻¹ = …', 'B⁻¹A⁻¹', ['A⁻¹B⁻¹', 'AB', 'BA'], 'Reversal law.'),
        ('The inverse of a square matrix, if it exists, is …', 'unique', ['not unique', 'always the identity', 'always symmetric'], 'If B and C are inverses, B = B(AC) = (BA)C = C.'),
        ('A square matrix A has an inverse if and only if …', '|A| ≠ 0', ['|A| = 0', 'A is symmetric', 'A is diagonal'], 'Non-singular matrices are invertible.'),
        ('If A is invertible, then (Aᵀ)⁻¹ = …', '(A⁻¹)ᵀ', ['A', '−A⁻¹', 'Aᵀ'], 'Transpose of AA⁻¹ = I.'),
        ('If A² = I, then A⁻¹ = …', 'A', ['I', 'O', 'Aᵀ'], 'A·A = I.'),
        ('A rectangular matrix of order 2 × 3 …', 'does not possess an inverse', ['has an inverse of order 3 × 2', 'has a unique inverse', 'has an inverse of order 2 × 3'], 'Only square matrices can be invertible.'),
    ])(r)


def c3s4_ar(r):
    while True:
        A = rand_mat(r, 2, 2, -4, 7)
        if det(A) != 0:
            break
    k = r.randint(2, 5)
    S = [[k, 2 * k], [1, 2]]
    return arbank([
        (f'The matrix {mstr(A)} is invertible.', f'Its determinant is {fz(det(A))} ≠ 0.', 'a', 'Non-zero determinant ⇒ invertible.'),
        (f'The matrix {mstr(S)} is invertible.', f'Its determinant is {k * 2 - 2 * k}.', 'd', 'det = 0, so it is singular; A false, R true.'),
        ('If AB = BA = I, then B is the inverse of A.', 'The inverse of a square matrix is unique.', 'b', 'Both true; A is the definition, uniqueness does not explain it.'),
        ('(AB)⁻¹ = A⁻¹B⁻¹ for invertible matrices A, B of the same order.', '(AB)(B⁻¹A⁻¹) = I.', 'd', 'The correct law is (AB)⁻¹ = B⁻¹A⁻¹; A false, R true.'),
    ])(r)


def c3s4_case(r):
    A = unimod(r, 2, (1, -1))
    Ai = inv(A)
    word = r.choice(['GO', 'HI', 'OK', 'UP', 'ME', 'WE', 'NO', 'BE', 'IT', 'AT', 'ON', 'US'])
    v = [ord(word[0]) - 64, ord(word[1]) - 64]
    c = [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]
    who1, who2 = two_names(r)
    return Q((f'{who1} sends a two-letter code word to {who2}. Letters are numbered A = 1, B = 2, …, Z = 26; the word is written as a column X and sent as Y = KX with the key K = {mstr(A)}. '
              f'{who2} receives Y = [{c[0]}; {c[1]}]. (i) Find |K|. (ii) Find K⁻¹. (iii) Decode the word.'),
             f'(i) {fz(det(A))} (ii) {mstr(Ai)} (iii) X = K⁻¹Y = [{v[0]}; {v[1]}]: {word}',
             '(i) 1 mark (ii) 1 mark (iii) X = K⁻¹Y and letters (2 marks).')


def c3s4_explain(r):
    return xbank([
        ('Prove that the inverse of a square matrix, if it exists, is unique.', 'If B and C are both inverses of A then B = C.', 'B = BI = B(AC) = (BA)C = IC = C (2 marks).'),
        ('Prove that (AB)⁻¹ = B⁻¹A⁻¹ for invertible matrices A and B of the same order.', '(AB)(B⁻¹A⁻¹) = I = (B⁻¹A⁻¹)(AB).', 'Associativity: A(BB⁻¹)A⁻¹ = AA⁻¹ = I (2 marks).'),
        ('If A is a square matrix such that A² = A, show that (I + A)³ = 7A + I.', '(I + A)³ = I + 3A + 3A² + A³ = I + 7A.', 'A³ = A²·A = A·A = A; I and A commute (2 marks).'),
        ('Explain why a matrix with a row of zeros cannot be invertible.', 'Any product AB then has a row of zeros, so AB ≠ I.', 'The zero row of A gives a zero row in AB (2 marks).'),
    ])(r)


# ======================================================================= ch04 Determinants

def c4s1_eval(r):
    n = r.choice([2, 3, 3])
    A = rand_mat(r, n, n, -4, 7)
    d = det(A)
    W = det(tr(A)[::-1]) if n == 3 else Fr(A[0][0] * A[1][1] + A[0][1] * A[1][0])
    return Q(f'Evaluate the determinant |A| where A = {mstr(A)}.', fz(d), f'Expanding along the first row: |A| = {fz(d)}.', dist3(fz(d), [fz(-d), fz(W), fz(d + 2), fz(d * 2)]))


def c4s1_solve(r):
    kind = r.randint(0, 1)
    if kind == 0:
        c = r.randint(2, 8)
        p, q = r.sample([1, 2, 3, 4, 5, 6, 8, 9, 12, 18], 2)
        val = c * c - p * q
        x2 = val + p * q
        rt = math.isqrt(x2)
        return Q(f'Find the values of x if |x, {p}; {q}, x| = |{c}, {p}; {q}, {c}|.', f'x = ±{rt}', f'x² − {p * q} = {c * c} − {p * q} ⇒ x² = {c * c} ⇒ x = ±{c}.', [f'x = {c}', f'x = ±{c * c}', f'x = ±{p * q}'])
    a, b = r.randint(1, 5), r.randint(1, 6)
    k = r.randint(-5, 8)
    # |2x, a; b, x| = k  -> 2x² − ab = k
    while (k + a * b) % 2 or not (k + a * b) > 0 or math.isqrt((k + a * b) // 2) ** 2 != (k + a * b) // 2:
        k = r.randint(-5, 60)
    rt = math.isqrt((k + a * b) // 2)
    return Q(f'Find x if |2x, {a}; {b}, x| = {k}.', f'x = ±{rt}', f'2x² − {a * b} = {k} ⇒ x² = {(k + a * b) // 2} ⇒ x = ±{rt}.', [f'x = {rt}', f'x = ±{(k + a * b) // 2}', f'x = ±{rt + 1}'])


def c4s1_prop(r):
    n = r.choice([2, 3])
    d = r.choice([-4, -3, -2, 2, 3, 4, 5, 6])
    k = r.choice([2, 3, -2, 4, 5])
    kind = r.randint(0, 2)
    if kind == 0:
        ans = k ** n * d
        return Q(f'If A is a square matrix of order {n} and |A| = {d}, find |{k}A|.', fz(ans), f'|kA| = kⁿ|A| = ({k}){_sup(n)} × {d} = {ans}.', dist3(fz(ans), [fz(k * d), fz(k ** 2 * d if n == 3 else k ** 3 * d), fz(k + d)]))
    if kind == 1:
        e = r.randint(2, 3)
        return Q(f'If A is a square matrix with |A| = {d}, find |A{_sup(e)}| and |Aᵀ|.', f'|A{_sup(e)}| = {d ** e}, |Aᵀ| = {d}', f'|Aⁿ| = |A|ⁿ and |Aᵀ| = |A|.',
                 [f'|A{_sup(e)}| = {e * d}, |Aᵀ| = {d}', f'|A{_sup(e)}| = {d ** e}, |Aᵀ| = {-d}', f'|A{_sup(e)}| = {d ** e}, |Aᵀ| = {fz(Fr(1, d))}'])
    d2 = r.choice([-3, -2, 2, 3, 4])
    return Q(f'A and B are square matrices of order {n} with |A| = {d} and |B| = {d2}. Find |AB| and |{k}AB|.', f'|AB| = {d * d2}, |{k}AB| = {k ** n * d * d2}',
             f'|AB| = |A||B| = {d * d2}; |{k}AB| = {k}{_sup(n)} × {d * d2} = {k ** n * d * d2}.',
             [f'|AB| = {d + d2}, |{k}AB| = {k * (d + d2)}', f'|AB| = {d * d2}, |{k}AB| = {k * d * d2}', f'|AB| = {d * d2}, |{k}AB| = {k ** (n + 1) * d * d2}'])


def c4s1_lin(r):
    while True:
        A = rand_mat(r, 3, 3, -3, 5)
        i, j = r.randint(0, 2), r.randint(0, 2)
        A0 = [row[:] for row in A]
        A0[i][j] = 0
        A1 = [row[:] for row in A]
        A1[i][j] = 1
        d0, d1 = det(A0), det(A1)
        slope = d1 - d0
        if slope != 0:
            x = -d0 / slope
            if x.denominator == 1 and abs(x) <= 12:
                break
    disp = [[fz(v) for v in row] for row in A]
    disp[i][j] = 'x'
    M = '[' + '; '.join(', '.join(row) for row in disp) + ']'
    return Q(f'Find x if the determinant of {M} is 0.', f'x = {fz(x)}', f'Expanding, the determinant equals {fz(slope)}x {"+" if d0 >= 0 else "−"} {fz(abs(d0))} = 0 ⇒ x = {fz(x)}.',
             dist3(f'x = {fz(x)}', [f'x = {fz(-x)}' if x else 'x = 1', f'x = {fz(x + 1)}', f'x = {fz(x - 2)}']))


def c4s1_mcq(r):
    return mcqbank([
        ('If A is a square matrix of order 3 and |A| = 5, then |2A| is …', '40', ['10', '20', '80'], '2³ × 5.'),
        ('The value of a determinant is unchanged if …', 'its rows and columns are interchanged', ['two rows are interchanged', 'a row is multiplied by 2', 'two columns are interchanged'], '|Aᵀ| = |A|.'),
        ('If two rows of a determinant are identical, its value is …', '0', ['1', '−1', 'the square of a row element'], 'Interchanging them changes the sign but not the determinant.'),
        ('If A is a skew-symmetric matrix of order 3, then |A| is …', '0', ['1', '−1', 'a perfect square'], '|A| = |Aᵀ| = |−A| = −|A|.'),
        ('For a square matrix A of order n, |kA| = …', 'kⁿ|A|', ['k|A|', 'n k|A|', 'k²|A|'], 'Each of the n rows is multiplied by k.'),
        ('If A is invertible, then |A⁻¹| = …', '1/|A|', ['|A|', '−|A|', '|A|²'], '|A||A⁻¹| = |I| = 1.'),
    ])(r)


def c4s1_ar(r):
    a, b, c = r.sample(range(1, 9), 3)
    n = r.choice([2, 3])
    k = r.randint(2, 4)
    return arbank([
        (f'The determinant of [{a}, {b}, {c}; {a}, {b}, {c}; {c}, {a}, {b}] is 0.', 'If two rows of a determinant are identical, its value is zero.', 'a', 'Rows 1 and 2 are identical.'),
        (f'If |A| = {a} for a matrix of order {n}, then |{k}A| = {k * a}.', f'|kA| = kⁿ|A| for a matrix of order n.', 'd', f'|{k}A| = {k ** n * a}; A false, R true.'),
        (f'The determinant of [0, {a}, −{b}; −{a}, 0, {c}; {b}, −{c}, 0] is 0.', 'The determinant of a skew-symmetric matrix of odd order is zero.', 'a', 'R explains A.'),
        ('|AB| = |A||B| for square matrices A, B of the same order.', 'Matrix multiplication is commutative.', 'c', 'A is true; R is false.'),
    ])(r)


def c4s1_case(r):
    while True:
        A = rand_mat(r, 3, 3, -3, 6)
        d = det(A)
        if d != 0:
            break
    k = r.choice([2, 3])
    who = name(r)
    return Q((f'{who}\'s project uses the matrix A = {mstr(A)} to scale shapes in a design app. (i) Find |A|. (ii) Find |Aᵀ| without expanding again. '
              f'(iii) Find |{k}A| and |A²|.'),
             f'(i) {fz(d)} (ii) {fz(d)} (iii) |{k}A| = {fz(k ** 3 * d)}, |A²| = {fz(d * d)}', '(i) 1 mark (ii) 1 mark (iii) 1 mark each.')


def c4s1_explain(r):
    return xbank([
        ('Explain why the determinant of a skew-symmetric matrix of order 3 is zero.', '|A| = |Aᵀ| = |−A| = (−1)³|A| = −|A| ⇒ |A| = 0.', 'Use |Aᵀ| = |A| and |kA| = k³|A| (2 marks).'),
        ('Without expanding, explain why |1, 2, 3; 2, 4, 6; 5, 7, 9| = 0.', 'Row 2 = 2 × Row 1.', 'Taking 2 common gives two identical rows (2 marks).'),
        ('Explain why |kA| ≠ k|A| for a square matrix of order 3 unless k³ = k.', '|kA| = k³|A|.', 'Each of the 3 rows contributes a factor k (2 marks).'),
    ])(r)


# ---- st2 area of a triangle

def _pts(r, k=3, lo=-6, hi=8):
    while True:
        P = [(r.randint(lo, hi), r.randint(lo, hi)) for _ in range(k)]
        a2 = P[0][0] * (P[1][1] - P[2][1]) + P[1][0] * (P[2][1] - P[0][1]) + P[2][0] * (P[0][1] - P[1][1])
        if a2 != 0:
            return P, a2


def _pt(p):
    return f'({fz(p[0])}, {fz(p[1])})'


def c4s2_area(r):
    P, a2 = _pts(r)
    A = Fr(abs(a2), 2)
    return Q(f'Using determinants, find the area of the triangle with vertices {_pt(P[0])}, {_pt(P[1])} and {_pt(P[2])}.', f'{fz(A)} sq units',
             f'Area = ½|x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)| = ½|{fz(a2)}| = {fz(A)} sq units.', [f'{abs(a2)} sq units', f'{fz(A / 2)} sq units', f'{fz(A + 1)} sq units'])


def c4s2_k(r):
    P, a2 = _pts(r)
    # replace P[2] = (k, y3): area expression linear in k
    x3, y3 = P[2]
    coef = P[0][1] - P[1][1]
    if coef == 0:
        raise ValueError
    const = P[0][0] * (P[1][1] - y3) + P[1][0] * (y3 - P[0][1])
    area = Fr(abs(a2), 2)
    k1 = Fr(2 * area - const, coef)
    k2 = Fr(-2 * area - const, coef)
    return Q(f'Find the values of k if the area of the triangle with vertices {_pt(P[0])}, {_pt(P[1])} and (k, {y3}) is {fz(area)} sq units.', f'k = {fz(max(k1, k2))} or k = {fz(min(k1, k2))}',
             f'½|Δ| = {fz(area)} where Δ = {term(coef, "k", first=True)}{term(const, "")} (1 mark); Δ = ±{fz(2 * area)} gives both values (2 marks).',
             [f'k = {fz(k1)} only', f'k = {fz(-k1)} or k = {fz(-k2)}', f'k = {fz(k1 + 1)} or k = {fz(k2 - 1)}'])


def c4s2_col(r):
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    dx, dy = r.choice([(1, 2), (2, 1), (1, -3), (3, 1), (2, -1), (1, 1), (-1, 2)])
    t2, t3 = r.sample([-2, -1, 2, 3, 4], 2)
    P = [(x1, y1), (x1 + t2 * dx, y1 + t2 * dy), (x1 + t3 * dx, y1 + t3 * dy)]
    if r.random() < 0.5:
        return Q(f'Using determinants, show that the points {_pt(P[0])}, {_pt(P[1])} and {_pt(P[2])} are collinear.', 'Collinear (area = 0)',
                 '|x₁ y₁ 1; x₂ y₂ 1; x₃ y₃ 1| = 0, so the triangle has zero area.', ['Not collinear', 'Collinear only if they lie on y = x', 'Cannot be decided'])
    k = P[2][1]
    return Q(f'Find k if the points {_pt(P[0])}, {_pt(P[1])} and ({P[2][0]}, k) are collinear.', f'k = {k}', f'Set the area determinant to 0 and solve: k = {k}.', num_distractors(k, -k, k + 2, k - 3))


def c4s2_line(r):
    P, a2 = _pts(r)
    (x1, y1), (x2, y2) = P[0], P[1]
    if (x1, y1) == (x2, y2):
        raise ValueError
    a, b, c = y1 - y2, x2 - x1, x1 * y2 - x2 * y1
    g = math.gcd(math.gcd(abs(a), abs(b)), abs(c)) or 1
    a, b, c = a // g, b // g, c // g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    eq = (term(a, 'x', first=True) + term(b, 'y') if a else term(b, 'y', first=True)) + (term(c, '') if c else '') + ' = 0'
    return Q(f'Using determinants, find the equation of the line joining {_pt(P[0])} and {_pt(P[1])}.', eq,
             f'|x, y, 1; {x1}, {y1}, 1; {x2}, {y2}, 1| = 0 (1 mark) ⇒ {eq} (2 marks).',
             dist3(eq, [(term(b, 'x', first=True) + term(a, 'y') + (term(c, '') if c else '') + ' = 0') if b else 'x + y = 0', (term(a, 'x', first=True) + term(b, 'y') + (term(-c, '') if c else ' + 1') + ' = 0') if a else 'y = 1',
                        (term(a, 'x', first=True) + term(-b, 'y') + (term(c, '') if c else '') + ' = 0') if a and b else 'x − y = 0']))


def c4s2_mcq(r):
    return mcqbank([
        ('If the area of a triangle with vertices (x₁, y₁), (x₂, y₂), (x₃, y₃) is Δ, then |x₁, y₁, 1; x₂, y₂, 1; x₃, y₃, 1| equals …', '±2Δ', ['Δ', '±Δ/2', 'Δ²'], 'Δ = ½|det|.'),
        ('Three points are collinear if and only if …', 'the area determinant is zero', ['the area determinant is 1', 'they lie in the first quadrant', 'their x-coordinates are equal'], 'Zero area.'),
        ('The area of a triangle is always taken as …', 'the absolute value of ½ × determinant', ['the determinant itself', 'half the determinant, with sign', 'twice the determinant'], 'Area is positive.'),
        ('If the points (2, −3), (k, −1) and (0, 4) are collinear, then k = …', '10/7', ['7/10', '−10/7', '2'], '2(−1 − 4) + k(4 + 3) + 0 = 0 ⇒ k = 10/7.'),
    ])(r)


def c4s2_ar(r):
    P, a2 = _pts(r)
    return arbank([
        (f'The area of the triangle with vertices {_pt(P[0])}, {_pt(P[1])}, {_pt(P[2])} is {fz(Fr(abs(a2), 2))} sq units.', 'Area = ½|x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)|.', 'a', f'The determinant is {a2}.'),
        (f'The area of the triangle with vertices {_pt(P[0])}, {_pt(P[1])}, {_pt(P[2])} is {fz(Fr(abs(a2), 2))} sq units.', 'If three points are collinear, the area determinant is zero.', 'b', 'Both true; R is about collinearity, not this area.'),
        (f'The points (1, 2), (2, 4) and (3, 6) are collinear.', 'The determinant |1, 2, 1; 2, 4, 1; 3, 6, 1| is 0.', 'a', 'Zero area ⇒ collinear.'),
        (f'The area of a triangle can be negative when the vertices are taken clockwise.', 'The determinant changes sign when two rows are interchanged.', 'd', 'Area is taken as the absolute value, so A is false; R is true.'),
    ])(r)


def c4s2_case(r):
    P, a2 = _pts(r, 3, 0, 12)
    s = r.choice([10, 5, 20])
    A = Fr(abs(a2), 2)
    who = name(r)
    return Q((f'{who}\'s family owns a triangular plot near {r.choice(CITIES)}. On a map with 1 unit = {s} m, its corners are at {_pt(P[0])}, {_pt(P[1])} and {_pt(P[2])}. '
              f'(i) Write the determinant used to find the area. (ii) Find the area on the map. (iii) Find the actual area of the plot in m².'),
             f'(i) ½|{P[0][0]}, {P[0][1]}, 1; {P[1][0]}, {P[1][1]}, 1; {P[2][0]}, {P[2][1]}, 1| (ii) {fz(A)} sq units (iii) {fz(A * s * s)} m²',
             f'(i) 1 mark (ii) 1 mark (iii) each sq unit = {s * s} m² (2 marks).')


# ---- st3 minors, cofactors, adjoint, inverse

def c4s3_minor(r):
    A = rand_mat(r, 3, 3, -4, 8)
    i, j = r.randint(0, 2), r.randint(0, 2)
    M = det(minor_m(A, i, j))
    C = (-1) ** (i + j) * M
    return Q(f'For A = {mstr(A)}, find the minor M{_sub(i + 1)}{_sub(j + 1)} and the cofactor A{_sub(i + 1)}{_sub(j + 1)}.', f'M{_sub(i + 1)}{_sub(j + 1)} = {fz(M)}, A{_sub(i + 1)}{_sub(j + 1)} = {fz(C)}',
             f'Delete row {i + 1} and column {j + 1}: M = {fz(M)}; cofactor = (−1)^{i + j + 2} M = {fz(C)}.',
             dist3(f'M{_sub(i + 1)}{_sub(j + 1)} = {fz(M)}, A{_sub(i + 1)}{_sub(j + 1)} = {fz(C)}', [f'M{_sub(i + 1)}{_sub(j + 1)} = {fz(M)}, A{_sub(i + 1)}{_sub(j + 1)} = {fz(-C)}' if M else f'M{_sub(i + 1)}{_sub(j + 1)} = 1, A{_sub(i + 1)}{_sub(j + 1)} = 1',
                                                                              f'M{_sub(i + 1)}{_sub(j + 1)} = {fz(-M)}, A{_sub(i + 1)}{_sub(j + 1)} = {fz(-M)}' if M else f'M{_sub(i + 1)}{_sub(j + 1)} = 2, A{_sub(i + 1)}{_sub(j + 1)} = −2',
                                                                              f'M{_sub(i + 1)}{_sub(j + 1)} = {fz(M + 2)}, A{_sub(i + 1)}{_sub(j + 1)} = {fz(C + 2)}']))


def c4s3_adj2(r):
    A = rand_mat(r, 2, 2, -6, 9)
    J = adj(A)
    return Q(f'Find the adjoint of the matrix A = {mstr(A)}.', f'adj A = {mstr(J)}', 'For [a, b; c, d], adj = [d, −b; −c, a].',
             dist3(f'adj A = {mstr(J)}', [f'adj A = {mstr([[A[1][1], A[0][1]], [A[1][0], A[0][0]]])}', f'adj A = {mstr(mscale(J, -1))}', f'adj A = {mstr(tr(J))}']))


def c4s3_adjdet(r):
    n = r.choice([2, 3])
    d = r.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6])
    kind = r.randint(0, 1)
    if kind == 0:
        ans = d ** (n - 1)
        return Q(f'If A is a non-singular square matrix of order {n} with |A| = {d}, find |adj A|.', fz(ans), f'|adj A| = |A|ⁿ⁻¹ = ({d}){_sup(n - 1)} = {ans}.', dist3(fz(ans), [fz(d ** n), fz(d), fz(Fr(1, d))]))
    ans = Fr(1, d)
    return Q(f'If A is a square matrix of order {n} with |A| = {d}, find |A⁻¹| and |A·adj A|.', f'|A⁻¹| = {fz(ans)}, |A·adj A| = {fz(Fr(d) ** n)}', f'|A⁻¹| = 1/|A|; A·adj A = |A|I so its determinant is |A|ⁿ = {d ** n}.',
             [f'|A⁻¹| = {fz(d)}, |A·adj A| = {fz(d)}', f'|A⁻¹| = {fz(-ans)}, |A·adj A| = {fz(d ** 2)}', f'|A⁻¹| = {fz(ans)}, |A·adj A| = {fz(d)}'])


def c4s3_inv3(r):
    A = unimod(r, 3, (1, -1, 2, -2, 3, -3, 4, 5, -4, 6))
    Ai = inv(A)
    J = adj(A)
    return Q(f'Find the inverse of the matrix A = {mstr(A)} using the adjoint method.', f'A⁻¹ = (1/{fz(det(A))}) {mstr(J)} = {mstr(Ai)}',
             f'|A| = {fz(det(A))} ≠ 0 (1 mark); cofactors and adj A = {mstr(J)} (3 marks); A⁻¹ = adj A/|A| (1 mark).')


def c4s3_verify(r):
    A = rand_mat(r, 2, 2, -5, 8) if r.random() < 0.5 else rand_mat(r, 3, 3, -3, 5)
    d = det(A)
    n = len(A)
    return Q(f'Verify that A(adj A) = (adj A)A = |A|I for A = {mstr(A)}.', f'Both products equal {fz(d)}I = {mstr(mscale(eye(n), d))}',
             f'adj A = {mstr(adj(A))} (1 mark); A(adj A) = {mstr(mmul(A, adj(A)))} (1 mark); (adj A)A is the same and |A| = {fz(d)} (1 mark).')


def c4s3_mcq(r):
    return mcqbank([
        ('If A is a square matrix of order n, then A(adj A) = …', '|A|I', ['adj A', '|A|ⁿ', 'I'], 'Basic identity.'),
        ('If A is a non-singular matrix of order 3 and |A| = 4, then |adj A| = …', '16', ['4', '64', '12'], '|A|² = 16.'),
        ('A square matrix A is singular if …', '|A| = 0', ['|A| ≠ 0', 'A = Aᵀ', 'A is diagonal'], 'Definition.'),
        ('If A = [2, 3; 5, −2], then A⁻¹ = …', '(1/19)A', ['−(1/19)A', '19A', 'A'], '|A| = −19, adj A = [−2, −3; −5, 2] = −A, so A⁻¹ = A/19.'),
        ('The sum of the products of the elements of a row with the cofactors of another row is …', '0', ['|A|', '1', '−|A|'], 'Expansion by alien cofactors.'),
        ('(adj A)ᵀ is equal to …', 'adj (Aᵀ)', ['adj A', '−adj A', 'A'], 'Transpose and adjoint commute.'),
    ])(r)


def c4s3_ar(r):
    d = r.choice([2, 3, 4, 5, -2, -3])
    n = r.choice([2, 3])
    return arbank([
        (f'If A is of order {n} with |A| = {d}, then |adj A| = {d ** (n - 1)}.', '|adj A| = |A|ⁿ⁻¹ for a matrix of order n.', 'a', 'Direct use of the result.'),
        (f'If A is of order 3 with |A| = {d}, then |adj A| = {d ** 3}.', 'A(adj A) = |A|I.', 'd', f'|adj A| = |A|² = {d * d}; A false, R true.'),
        ('A singular matrix has no inverse.', 'A⁻¹ = adj A/|A| requires |A| ≠ 0.', 'a', 'R explains A.'),
        ('The cofactor of an element aᵢⱼ is (−1)ⁱ⁺ʲ Mᵢⱼ.', 'The minor Mᵢⱼ is the determinant left after deleting row i and column j.', 'b', 'Both true, but R defines the minor, not why the sign appears.'),
    ])(r)


def c4s3_case(r):
    A = unimod(r, 3, (1, -1, 2, -2))
    Ai = inv(A)
    who = name(r)
    return Q((f'{who}, a student intern at a {r.choice(CITIES)} start-up, encodes data with the matrix A = {mstr(A)}. '
              f'(i) Find |A|. (ii) Find the cofactors A₁₁, A₁₂ and A₁₃. (iii) Find A⁻¹.'),
             f'(i) {fz(det(A))} (ii) {fz(cof(A, 0, 0))}, {fz(cof(A, 0, 1))}, {fz(cof(A, 0, 2))} (iii) {mstr(Ai)}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ---- st4 systems by the matrix method

def _sys(r, n):
    while True:
        A = rand_mat(r, n, n, -3, 5)
        d = det(A)
        if d != 0 and abs(d) <= 30 and sum(1 for row in A for x in row if x == 0) <= (1 if n == 2 else 3):
            break
    X = [r.randint(-4, 5) for _ in range(n)]
    B = [sum(A[i][j] * X[j] for j in range(n)) for i in range(n)]
    return A, X, B


def c4s4_two(r):
    A, X, B = _sys(r, 2)
    eqs = ', '.join(lin_eq(A[i], B[i], 'xy') for i in range(2))
    return Q(f'Solve the system of equations {eqs} by the matrix method.', f'x = {X[0]}, y = {X[1]}',
             f'AX = B with |A| = {fz(det(A))} ≠ 0 (1 mark); X = A⁻¹B = (1/{fz(det(A))}){mstr(adj(A))}{mstr([[b] for b in B])} (1 mark); x = {X[0]}, y = {X[1]} (1 mark).',
             [f'x = {X[1]}, y = {X[0]}' if X[0] != X[1] else f'x = {X[0] + 1}, y = {X[1]}', f'x = {-X[0]}, y = {-X[1]}' if any(X) else 'x = 1, y = 1', f'x = {X[0] + 1}, y = {X[1] - 1}'])


def c4s4_three(r):
    A, X, B = _sys(r, 3)
    eqs = '; '.join(lin_eq(A[i], B[i]) for i in range(3))
    return Q(f'Solve the following system of equations by the matrix method: {eqs}.', f'x = {X[0]}, y = {X[1]}, z = {X[2]}',
             f'|A| = {fz(det(A))} ≠ 0 so a unique solution exists (1 mark); adj A = {mstr(adj(A))} (2 marks); X = A⁻¹B gives x = {X[0]}, y = {X[1]}, z = {X[2]} (2 marks).')


def c4s4_consist(r):
    kind = r.randint(0, 2)
    if kind == 0:
        A, X, B = _sys(r, 2)
        eqs = ', '.join(lin_eq(A[i], B[i], 'xy') for i in range(2))
        return Q(f'Examine the consistency of the system {eqs}.', 'Consistent (unique solution)', f'|A| = {fz(det(A))} ≠ 0, so the system has a unique solution.',
                 ['Inconsistent', 'Consistent with infinitely many solutions', 'Cannot be decided'])
    a, b = r.choice([(1, 2), (2, 3), (3, 1), (2, -1), (1, -3), (4, 3)])
    k = r.randint(2, 4)
    c1 = r.randint(1, 9)
    if kind == 1:
        c2 = k * c1 + r.choice([1, 2, -1, 3])
        eqs = f'{lin_eq([a, b], c1, "xy")}, {lin_eq([k * a, k * b], c2, "xy")}'
        return Q(f'Examine the consistency of the system {eqs}.', 'Inconsistent', f'|A| = 0 and (adj A)B ≠ O, so the system has no solution (the lines are parallel).',
                 ['Consistent (unique solution)', 'Consistent with infinitely many solutions', 'Consistent with exactly two solutions'])
    eqs = f'{lin_eq([a, b], c1, "xy")}, {lin_eq([k * a, k * b], k * c1, "xy")}'
    return Q(f'Examine the consistency of the system {eqs}.', 'Consistent with infinitely many solutions', '|A| = 0 and (adj A)B = O; the second equation is a multiple of the first.',
             ['Inconsistent', 'Consistent (unique solution)', 'Consistent with exactly two solutions'])


def c4s4_word(r):
    items = r.sample(['onions', 'wheat', 'rice', 'potatoes', 'sugar', 'dal', 'tomatoes'], 3)
    while True:
        A = [[r.randint(1, 6) for _ in range(3)] for _ in range(3)]
        if det(A) != 0:
            break
    X = [r.randint(2, 9) * 5 for _ in range(3)]
    B = [sum(A[i][j] * X[j] for j in range(3)) for i in range(3)]
    ns = r.sample(['Meena', 'Rahul', 'Farhan', 'Gauri', 'Kunal', 'Priya', 'Om', 'Lakshmi'], 3)
    lines = '; '.join(f'{ns[i]} buys {A[i][0]} kg {items[0]}, {A[i][1]} kg {items[1]} and {A[i][2]} kg {items[2]} for ₹{B[i]}' for i in range(3))
    return Q(f'At a market in {r.choice(CITIES)}: {lines}. Find the price per kg of each item using the matrix method.',
             f'{items[0]} ₹{X[0]}, {items[1]} ₹{X[1]}, {items[2]} ₹{X[2]} per kg',
             f'Form AX = B with A = {mstr(A)} (1 mark); |A| = {fz(det(A))} (1 mark); adj A and X = A⁻¹B (2 marks); prices (1 mark).')


def c4s4_given_inv(r):
    A, X, B = _sys(r, 3)
    Ai = inv(A)
    J = adj(A)
    d = det(A)
    eqs = '; '.join(lin_eq(A[i], B[i]) for i in range(3))
    return Q(f'Given that A = {mstr(A)} and B = {mstr(J)} satisfy AB = {fz(d)}I, find A⁻¹ and use it to solve {eqs}.',
             f'A⁻¹ = (1/{fz(d)})B; x = {X[0]}, y = {X[1]}, z = {X[2]}', f'AB = {fz(d)}I ⇒ A⁻¹ = B/{fz(d)} (2 marks); X = A⁻¹C (2 marks); values (1 mark).')


def c4s4_mcq(r):
    return mcqbank([
        ('For the system AX = B, if |A| ≠ 0, then the system has …', 'a unique solution', ['no solution', 'infinitely many solutions', 'exactly two solutions'], 'X = A⁻¹B.'),
        ('For the system AX = B, if |A| = 0 and (adj A)B ≠ O, then the system is …', 'inconsistent', ['consistent with a unique solution', 'consistent with infinitely many solutions', 'homogeneous'], 'No solution.'),
        ('A system of equations having one or more solutions is called …', 'consistent', ['inconsistent', 'singular', 'homogeneous'], 'Definition.'),
        ('The system x + y = 2, 2x + 2y = 4 has …', 'infinitely many solutions', ['a unique solution', 'no solution', 'exactly two solutions'], 'The equations are the same line.'),
        ('The system x + 2y = 2, 2x + 4y = 3 has …', 'no solution', ['a unique solution', 'infinitely many solutions', 'exactly one solution with y = 0'], 'Parallel lines.'),
    ])(r)


def c4s4_ar(r):
    A, X, B = _sys(r, 2)
    eqs = ', '.join(lin_eq(A[i], B[i], 'xy') for i in range(2))
    a, b, c = r.randint(1, 4), r.randint(1, 4), r.randint(1, 6)
    return arbank([
        (f'The system {eqs} has a unique solution.', f'The coefficient matrix has determinant {fz(det(A))} ≠ 0.', 'a', 'Non-singular ⇒ unique solution X = A⁻¹B.'),
        (f'The system {lin_eq([a, b], c, "xy")}, {lin_eq([2 * a, 2 * b], 2 * c + 1, "xy")} has a unique solution.', 'If |A| = 0, the system AX = B may be inconsistent.', 'd', '|A| = 0 and (adj A)B ≠ O: no solution, so A is false; R is true.'),
        (f'The system {lin_eq([a, b], c, "xy")}, {lin_eq([3 * a, 3 * b], 3 * c, "xy")} is consistent.', 'The two equations represent the same line.', 'a', 'Infinitely many solutions.'),
    ])(r)


def c4s4_case(r):
    while True:
        A = [[1, 1, 1], [r.randint(1, 3), r.randint(0, 3), r.randint(1, 3)], [r.randint(0, 2), r.randint(1, 3), r.randint(-1, 2)]]
        if det(A) != 0:
            break
    X = [r.randint(2, 9) * 1000 for _ in range(3)]
    B = [sum(A[i][j] * X[j] for j in range(3)) for i in range(3)]
    who = name(r)
    return Q((f'{who} invests a total of {inr(B[0])} in three schemes P, Q and R. The conditions give the equations x + y + z = {B[0]}, {lin_eq(A[1], B[1])[:-len(str(B[1])) - 3]} = {B[1]}, {lin_eq(A[2], B[2])[:-len(str(B[2])) - 3]} = {B[2]}, '
              f'where x, y, z are the amounts (in ₹) in P, Q, R. (i) Write the system as AX = B. (ii) Find |A| and state why a unique solution exists. (iii) Find x, y, z.'),
             f'(i) A = {mstr(A)}, B = [{B[0]}; {B[1]}; {B[2]}] (ii) |A| = {fz(det(A))} ≠ 0 (iii) x = {inr(X[0])}, y = {inr(X[1])}, z = {inr(X[2])}',
             '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c4s4_explain(r):
    return xbank([
        ('Explain the condition under which the system AX = B (A a square matrix) has a unique solution, and write that solution.', '|A| ≠ 0; X = A⁻¹B.', 'Pre-multiply AX = B by A⁻¹ (2 marks).'),
        ('Explain how you would decide whether a system AX = B with |A| = 0 is consistent.', 'Find (adj A)B: if it is not O, inconsistent; if it is O, the system may have infinitely many solutions or none.', 'Test of (adj A)B (2 marks).'),
        ('Why can the matrix method not be used directly to solve 2x + 3y = 5, 4x + 6y = 10?', 'The coefficient matrix is singular (|A| = 0), so A⁻¹ does not exist.', 'Here (adj A)B = O and the system has infinitely many solutions (2 marks).'),
    ])(r)


# ======================================================================= table

FAMILIES = {
    S + '01-st1': [F('C1', 'D2', 'mcq', c1s1_def), F('C1', 'D1', 'short', c1s1_count), F('C2', 'D2', 'mcq', c1s1_props), F('C2', 'D3', 'mcq', c1s1_ar, kinds=('ar',)),
                   F('C2', 'D2', 'explain', c1s1_people), F('C3', 'D2', 'numerical', c1s1_rule), F('C3', 'D3', 'multi_step', c1s1_add), F('C3', 'D1', 'mcq', c1s1_std_mcq),
                   F('C4', 'D3', 'case', c1s1_case), F('C4', 'D4', 'multi_step', c1s1_std), F('C3', 'D4', 'multi_step', c1s1_add), F('C2', 'D3', 'mcq', c1s1_props)],
    S + '01-st2': [F('C1', 'D2', 'mcq', c1s2_mcq), F('C1', 'D1', 'short', c1s2_modz), F('C2', 'D2', 'explain', c1s2_explain), F('C2', 'D3', 'mcq', c1s2_ar, kinds=('ar',)),
                   F('C2', 'D2', 'numerical', c1s2_partition), F('C3', 'D2', 'numerical', c1s2_class), F('C3', 'D3', 'multi_step', c1s2_closure), F('C3', 'D4', 'long', c1s2_prove),
                   F('C4', 'D3', 'case', c1s2_case), F('C4', 'D4', 'long', c1s2_nn), F('C4', 'D5', 'long', c1s2_nn), F('C3', 'D1', 'numerical', c1s2_class)],
    S + '01-st3': [F('C1', 'D2', 'mcq', c1s3_mcq), F('C1', 'D1', 'short', c1s3_count), F('C2', 'D2', 'explain', c1s3_square), F('C2', 'D3', 'mcq', c1s3_ar, kinds=('ar',)),
                   F('C2', 'D2', 'mcq', c1s3_finite), F('C3', 'D2', 'numerical', c1s3_count), F('C3', 'D3', 'multi_step', c1s3_linear), F('C3', 'D4', 'long', c1s3_rational),
                   F('C4', 'D3', 'case', c1s3_case), F('C4', 'D4', 'long', c1s3_rational), F('C4', 'D5', 'long', c1s3_d5), F('C3', 'D1', 'mcq', c1s3_finite)],
    S + '02-st1': [F('C1', 'D2', 'mcq', c2s1_branch), F('C1', 'D1', 'mcq', c2s1_branch), F('C2', 'D2', 'explain', c2s1_explain), F('C2', 'D3', 'mcq', c2s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c2s1_domain), F('C3', 'D3', 'numerical', c2s1_domain), F('C3', 'D4', 'numerical', c2s1_domain_sq), F('C4', 'D3', 'case', c2s1_case),
                   F('C4', 'D4', 'numerical', c2s1_domain_sq), F('C3', 'D1', 'short', c2s3_pv)],
    S + '02-st2': [F('C1', 'D2', 'mcq', c2s2_mcq), F('C1', 'D1', 'mcq', c2s2_point), F('C2', 'D2', 'explain', c2s2_explain), F('C2', 'D3', 'mcq', c2s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'mcq', c2s2_point), F('C3', 'D3', 'numerical', c2s2_read), F('C4', 'D3', 'case', c2s2_case), F('C4', 'D4', 'explain', c2s2_explain), F('C3', 'D1', 'numerical', c2s2_read)],
    S + '02-st3': [F('C1', 'D2', 'mcq', c2s3_mcq), F('C1', 'D1', 'short', c2s3_pv), F('C2', 'D2', 'short', c2s3_pv), F('C2', 'D3', 'mcq', c2s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c2s3_eval), F('C3', 'D3', 'numerical', c2s3_reduce), F('C3', 'D4', 'numerical', c2s3_mixed), F('C4', 'D3', 'case', c2s3_case),
                   F('C4', 'D4', 'multi_step', c2s3_long), F('C4', 'D5', 'multi_step', c2s3_long), F('C3', 'D1', 'numerical', c2s3_eval)],
    S + '03-st1': [F('C1', 'D2', 'mcq', c3s1_mcq), F('C1', 'D1', 'short', c3s1_count), F('C2', 'D2', 'short', c3s1_orders), F('C2', 'D3', 'mcq', c3s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c3s1_construct), F('C3', 'D3', 'numerical', c3s1_equal), F('C4', 'D3', 'case', c3s1_case), F('C2', 'D2', 'explain', c3s1_explain), F('C3', 'D1', 'numerical', c3s1_equal)],
    S + '03-st2': [F('C1', 'D2', 'mcq', c3s2_order), F('C1', 'D1', 'short', c3s2_lin), F('C2', 'D2', 'explain', c3s2_explain), F('C2', 'D3', 'mcq', c3s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c3s2_mul), F('C3', 'D3', 'multi_step', c3s2_ch), F('C3', 'D4', 'long', c3s2_sales, gap='G7'), F('C4', 'D3', 'case', _c3s2_case2, gap='G7'),
                   F('C4', 'D4', 'long', c3s2_power), F('C4', 'D5', 'long', c3s2_sales, gap='G7'), F('C3', 'D1', 'numerical', c3s2_lin), F('C2', 'D2', 'numerical', c3s2_mul)],
    S + '03-st3': [F('C1', 'D2', 'mcq', c3s3_mcq), F('C1', 'D1', 'short', c3s3_tr), F('C2', 'D2', 'explain', c3s3_explain), F('C2', 'D3', 'mcq', c3s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c3s3_find), F('C3', 'D3', 'multi_step', c3s3_verify), F('C4', 'D3', 'case', c3s3_case), F('C4', 'D4', 'long', c3s3_split), F('C3', 'D1', 'numerical', c3s3_tr)],
    S + '03-st4': [F('C1', 'D2', 'mcq', c3s4_mcq), F('C2', 'D2', 'explain', c3s4_explain), F('C2', 'D3', 'mcq', c3s4_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c3s4_formula),
                   F('C3', 'D2', 'numerical', c3s4_verify), F('C3', 'D3', 'numerical', c3s4_formula), F('C4', 'D3', 'case', c3s4_case, gap='G7'), F('C4', 'D4', 'long', c3s4_poly), F('C1', 'D1', 'mcq', c3s4_mcq)],
    S + '04-st1': [F('C1', 'D2', 'mcq', c4s1_mcq), F('C1', 'D1', 'short', c4s1_eval), F('C2', 'D2', 'numerical', c4s1_prop), F('C2', 'D3', 'mcq', c4s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c4s1_eval), F('C3', 'D3', 'numerical', c4s1_solve), F('C4', 'D3', 'case', c4s1_case), F('C3', 'D4', 'numerical', c4s1_lin), F('C2', 'D2', 'explain', c4s1_explain)],
    S + '04-st2': [F('C1', 'D2', 'mcq', c4s2_mcq), F('C2', 'D2', 'explain', c4s2_col), F('C2', 'D3', 'mcq', c4s2_ar, kinds=('ar',)), F('C3', 'D1', 'numerical', c4s2_area),
                   F('C3', 'D2', 'numerical', c4s2_area), F('C3', 'D3', 'multi_step', c4s2_k), F('C4', 'D3', 'case', c4s2_case, gap='G7'), F('C3', 'D4', 'multi_step', c4s2_line), F('C4', 'D4', 'multi_step', c4s2_k)],
    S + '04-st3': [F('C1', 'D2', 'mcq', c4s3_mcq), F('C1', 'D1', 'short', c4s3_adj2), F('C2', 'D2', 'numerical', c4s3_adjdet), F('C2', 'D3', 'mcq', c4s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c4s3_minor), F('C3', 'D3', 'multi_step', c4s3_verify), F('C3', 'D4', 'long', c4s3_inv3), F('C4', 'D3', 'case', c4s3_case),
                   F('C4', 'D4', 'long', c4s3_inv3), F('C4', 'D5', 'long', c4s3_inv3), F('C3', 'D1', 'numerical', c4s3_adj2)],
    S + '04-st4': [F('C1', 'D2', 'mcq', c4s4_mcq), F('C1', 'D1', 'short', c4s4_consist), F('C2', 'D2', 'explain', c4s4_explain), F('C2', 'D3', 'mcq', c4s4_ar, kinds=('ar',)),
                   F('C2', 'D2', 'mcq', c4s4_consist), F('C3', 'D2', 'numerical', c4s4_two), F('C3', 'D3', 'multi_step', c4s4_two), F('C3', 'D4', 'long', c4s4_three),
                   F('C4', 'D3', 'case', c4s4_case, gap='G7'), F('C4', 'D4', 'long', c4s4_word, gap='G7'), F('C4', 'D5', 'long', c4s4_given_inv), F('C3', 'D1', 'numerical', c4s4_two)],
}
