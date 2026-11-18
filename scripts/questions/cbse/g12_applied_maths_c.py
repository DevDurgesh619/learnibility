"""CBSE class 12 Applied Mathematics (241): families for ch07 (probability distributions), ch08 (inferential
statistics), ch09 (time series), ch10 (perpetuity and sinking funds), ch11 (bonds, EMI, rate of return, CAGR) and
ch12 (linear method of depreciation)."""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from g12_applied_maths_h import (F, Q, ar, mcqbank, arbank, xbank, fz, fpar, dist3, name, two_names, inr, num, CITIES,
                                 rs, pct, binom, area0, T_05, T_01, surd)

S = 'cbse-g12-applied-maths-ch'


def r4(x):
    return round(x, 4)


def money(x):
    return rs(round(x, 2))


# ======================================================================= ch07 st1 random variables: mean and variance

c7s1_mcq = mcqbank([
    ('For a probability distribution, Σ P(X = xᵢ) = …', '1', ['0', 'the mean', 'n'], 'Total probability.'),
    ('Var(X) = …', 'E(X²) − [E(X)]²', ['E(X²)', '[E(X)]² − E(X²)', 'E(X) − E(X²)'], 'Computational formula.'),
    ('The standard deviation of X is …', '√Var(X)', ['Var(X)²', 'E(X)/n', 'E(X²)'], 'Definition.'),
    ('If every value of X is increased by 5, the variance …', 'remains the same', ['increases by 5', 'increases by 25', 'is doubled'], 'Var(X + c) = Var(X).'),
    ('E(aX + b) = …', 'aE(X) + b', ['aE(X)', 'a²E(X) + b', 'E(X) + b'], 'Linearity of expectation.'),
    ('Var(aX + b) = …', 'a²Var(X)', ['aVar(X) + b', 'aVar(X)', 'a²Var(X) + b'], 'Constant shift does not change spread.'),
    ('A random variable is …', 'a real-valued function on the sample space', ['an event', 'a probability', 'a constant'], 'Definition.'),
])


def _dist(r):
    n = r.choice([3, 4, 5])
    xs = sorted(r.sample(range(-2, 7), n))
    while True:
        ks = [r.randint(1, 5) for _ in xs]
        tot = sum(ks)
        if tot in (5, 8, 10, 12, 15, 16, 20):
            break
    return xs, ks, tot


def c7s1_k(r):
    xs, ks, tot = _dist(r)
    ps = [Fr(k, tot) for k in ks]
    mean = sum(x * p for x, p in zip(xs, ps))
    var = sum(x * x * p for x, p in zip(xs, ps)) - mean * mean
    tab = ', '.join(f'P(X = {fz(x)}) = {k if k > 1 else ""}k' for x, k in zip(xs, ks))
    ans = f'k = 1/{tot}; E(X) = {fz(mean)}; Var(X) = {fz(var)}'
    return Q(f'A random variable X has the distribution {tab}. Find k, the mean and the variance of X.', ans,
             f'Σ P = {tot}k = 1 ⇒ k = 1/{tot} (1 mark); E(X) = Σ xP = {fz(mean)} (1 mark); E(X²) = {fz(sum(x * x * p for x, p in zip(xs, ps)))}, Var = E(X²) − [E(X)]² = {fz(var)} (1 mark).',
             dist3(ans, [f'k = 1/{tot}; E(X) = {fz(mean)}; Var(X) = {fz(var + mean * mean)}', f'k = {tot}; E(X) = {fz(mean * tot)}; Var(X) = {fz(var)}', f'k = 1/{tot}; E(X) = {fz(mean + 1)}; Var(X) = {fz(var)}']))


def c7s1_mean(r):
    xs, ks, tot = _dist(r)
    ps = [Fr(k, tot) for k in ks]
    mean = sum(x * p for x, p in zip(xs, ps))
    tab = ', '.join(f'P(X = {fz(x)}) = {fz(p)}' for x, p in zip(xs, ps))
    return Q(f'Find the mean of the random variable X with distribution {tab}.', fz(mean), f'E(X) = Σ xᵢpᵢ = {fz(mean)}.',
             dist3(fz(mean), [fz(Fr(sum(xs), len(xs))), fz(sum(x * x * p for x, p in zip(xs, ps))), fz(mean + Fr(1, tot)), fz(-mean) if mean else '1']))


def c7s1_coins(r):
    n = r.choice([2, 3, 4])
    what = r.choice(['heads', 'tails'])
    ps = [Fr(binom(n, k), 2 ** n) for k in range(n + 1)]
    mean = Fr(n, 2)
    var = Fr(n, 4)
    ans = f'E(X) = {fz(mean)}, Var(X) = {fz(var)}'
    return Q(f'A fair coin is tossed {n} times. Let X be the number of {what}. Find the probability distribution of X, its mean and variance.', ans,
             f'P(X = k) = ⁿCₖ/2ⁿ: {", ".join(fz(p) for p in ps)} (1 mark); E(X) = {fz(mean)} (1 mark); E(X²) = {fz(sum(k * k * p for k, p in enumerate(ps)))}, Var = {fz(var)} (1 mark).',
             dist3(ans, [f'E(X) = {fz(mean)}, Var(X) = {fz(mean)}', f'E(X) = {n}, Var(X) = {fz(var)}', f'E(X) = {fz(mean)}, Var(X) = {fz(var * 2)}']))


def c7s1_draw(r):
    g, b = r.randint(2, 6), r.randint(3, 9)
    n = g + b
    good, bad = r.choice([('defective', 'non-defective'), ('red', 'black'), ('rotten', 'good')])
    ps = [Fr(binom(g, k) * binom(b, 2 - k), binom(n, 2)) for k in range(3)]
    mean = sum(k * p for k, p in enumerate(ps))
    var = sum(k * k * p for k, p in enumerate(ps)) - mean * mean
    item = 'bulbs' if good == 'defective' else ('apples' if good == 'rotten' else 'balls')
    ans = f'E(X) = {fz(mean)}, Var(X) = {fz(var)}'
    return Q(f'Two {item} are drawn without replacement from a lot of {g} {good} and {b} {bad} {item}. If X is the number of {good} {item} drawn, find the mean and variance of X.', ans,
             f'P(X = 0, 1, 2) = {", ".join(fz(p) for p in ps)} (2 marks); E(X) = {fz(mean)} (1 mark); Var(X) = E(X²) − [E(X)]² = {fz(var)} (2 marks).',
             dist3(ans, [f'E(X) = {fz(mean)}, Var(X) = {fz(var + mean * mean)}', f'E(X) = {fz(Fr(2 * g, n) + Fr(1, n))}, Var(X) = {fz(var)}', f'E(X) = {fz(mean)}, Var(X) = {fz(mean * (1 - mean / 2))}']))


def c7s1_game(r):
    who = name(r)
    win = r.choice([10, 20, 30, 50, 100])
    lose = r.choice([5, 10, 15, 20])
    k = r.choice([(1, 6), (2, 6), (1, 4), (3, 8), (1, 3)])
    p = Fr(*k)
    ev = win * p - lose * (1 - p)
    verdict = 'favourable' if ev > 0 else 'unfavourable' if ev < 0 else 'fair'
    event = {Fr(1, 6): 'a six on a fair die', Fr(1, 3): 'a 5 or 6 on a fair die', Fr(1, 4): 'a club when a card is drawn from a well-shuffled pack', Fr(3, 8): 'exactly two heads in three tosses of a coin'}[p]
    return Q(f'In a fair-stall game, {who} wins ₹{win} on getting {event}, and otherwise loses ₹{lose}. Find the expected gain and say whether the game is favourable to {who}.', f'₹{fz(ev)}; {verdict}',
             f'P(win) = {fz(p)} (1 mark); E = {win} × {fz(p)} − {lose} × {fz(1 - p)} = {fz(ev)} (2 marks).',
             dist3(f'₹{fz(ev)}; {verdict}', [f'₹{fz(win * p)}; favourable', f'₹{fz(-ev)}; {"unfavourable" if ev > 0 else "favourable"}', f'₹{fz(win * p + lose * (1 - p))}; favourable']))


def c7s1_ar(r):
    k = r.randint(0, 2)
    c = r.randint(2, 9)
    v = r.randint(2, 9)
    if k == 0:
        return ar(f'If Var(X) = {v}, then Var(X + {c}) = {v}.', 'Adding a constant shifts all values but does not change their spread.', 'a', 'Var(X + c) = Var(X).')
    if k == 1:
        return ar(f'If Var(X) = {v}, then Var({c}X) = {c * v}.', 'Var(aX) = a²Var(X).', 'd', f'Var({c}X) = {c * c * v}; A false, R true.')
    return ar('P(X = 0) = 0.3, P(X = 1) = 0.5, P(X = 2) = 0.3 is a probability distribution.', 'The probabilities of a distribution must add up to 1.', 'd', 'The sum is 1.1; A false, R true.')


def c7s1_case(r):
    xs, ks, tot = _dist(r)
    ps = [Fr(k, tot) for k in ks]
    xs = [abs(x) + 1 for x in xs]
    if len(set(xs)) < len(xs):
        raise ValueError
    mean = sum(x * p for x, p in zip(xs, ps))
    var = sum(x * x * p for x, p in zip(xs, ps)) - mean * mean
    who = name(r)
    tab = '; '.join(f'{x} orders with probability {fz(p)}' for x, p in zip(xs, ps))
    return Q((f'{who}, who runs a cloud kitchen in {r.choice(CITIES)}, notes the number of orders X received in a 10-minute slot: {tab}. '
              f'(i) Verify that this is a probability distribution. (ii) Find the expected number of orders. (iii) Find the variance.'),
             f'(i) Σ P = 1 (ii) {fz(mean)} (iii) {fz(var)}', '(i) 1 mark (ii) 1 mark (iii) E(X²) − [E(X)]² (2 marks).')


# ======================================================================= ch07 st2 binomial distribution

c7s2_mcq = mcqbank([
    ('For a binomial distribution B(n, p), the mean is …', 'np', ['npq', 'n/p', '√(npq)'], 'Standard result.'),
    ('For a binomial distribution B(n, p), the variance is …', 'npq', ['np', 'np²', '√(np)'], 'Standard result.'),
    ('In a binomial distribution, the trials are …', 'independent, with the same probability of success', ['dependent', 'infinitely many', 'with changing probability of success'], 'Bernoulli trials.'),
    ('For a binomial variate, mean and variance satisfy …', 'mean > variance', ['mean < variance', 'mean = variance always', 'variance = 0'], 'npq < np as q < 1.'),
    ('P(X = r) for B(n, p) is …', 'ⁿCᵣ pʳ qⁿ⁻ʳ', ['pʳ qⁿ⁻ʳ', 'ⁿCᵣ pⁿ⁻ʳ qʳ', 'e⁻ᵖ pʳ/r!'], 'Binomial formula.'),
    ('The number of parameters of a binomial distribution is …', '2 (n and p)', ['1', '3', '0'], 'n and p.'),
])


def c7s2_prob(r):
    n = r.randint(4, 8)
    p = r.choice([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(1, 5), Fr(1, 6), Fr(2, 3), Fr(3, 4)])
    k = r.randint(0, 2)
    rr = r.randint(1, n - 1)
    q = 1 - p
    if k == 0:
        val = binom(n, rr) * p ** rr * q ** (n - rr)
        stem = f'If X ~ B({n}, {fz(p)}), find P(X = {rr}).'
        key = f'P(X = {rr}) = ⁿCᵣpʳqⁿ⁻ʳ = {binom(n, rr)} × ({fz(p)})^{rr} × ({fz(q)})^{n - rr} = {fz(val)}.'
        wr = [fz(p ** rr * q ** (n - rr)), fz(binom(n, rr) * p ** (n - rr) * q ** rr), fz(binom(n, rr) * p ** rr)]
    elif k == 1:
        val = 1 - q ** n
        stem = f'If X ~ B({n}, {fz(p)}), find P(X ≥ 1).'
        key = f'P(X ≥ 1) = 1 − P(X = 0) = 1 − ({fz(q)})^{n} = {fz(val)}.'
        wr = [fz(q ** n), fz(1 - p ** n), fz(n * p * q ** (n - 1))]
    else:
        val = sum(binom(n, i) * p ** i * q ** (n - i) for i in range(rr + 1))
        stem = f'If X ~ B({n}, {fz(p)}), find P(X ≤ {rr}).'
        key = f'P(X ≤ {rr}) = Σ from r = 0 to {rr} of ⁿCᵣpʳqⁿ⁻ʳ = {fz(val)}.'
        wr = [fz(1 - val), fz(binom(n, rr) * p ** rr * q ** (n - rr)), fz(val - q ** n)]
    return Q(stem, fz(val), key, dist3(fz(val), wr + [fz(val / 2)]))


def c7s2_mv(r):
    n = r.randint(5, 60)
    p = r.choice([Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(1, 5), Fr(2, 5), Fr(3, 4), Fr(1, 10)])
    k = r.randint(0, 1)
    m, v = n * p, n * p * (1 - p)
    if k == 0:
        return Q(f'Find the mean and variance of the binomial distribution B({n}, {fz(p)}).', f'mean = {fz(m)}, variance = {fz(v)}', f'mean = np, variance = npq with q = {fz(1 - p)}.',
                 dist3(f'mean = {fz(m)}, variance = {fz(v)}', [f'mean = {fz(v)}, variance = {fz(m)}', f'mean = {fz(m)}, variance = {fz(m * m)}', f'mean = {fz(m)}, variance = {fz(n * p * p)}']))
    if m.denominator != 1 or v.denominator > 4:
        raise ValueError
    return Q(f'The mean and variance of a binomial distribution are {fz(m)} and {fz(v)}. Find n and p.', f'n = {n}, p = {fz(p)}',
             f'q = variance/mean = {fz(1 - p)} (1 mark); p = {fz(p)}, n = mean/p = {n} (2 marks).',
             dist3(f'n = {n}, p = {fz(p)}', [f'n = {fz(m / (1 - p)) if (m / (1 - p)).denominator == 1 else n + 1}, p = {fz(1 - p)}', f'n = {fz(m)}, p = {fz(p)}', f'n = {2 * n}, p = {fz(p / 2)}']))


def c7s2_word(r):
    n = r.randint(4, 8)
    ctx = r.choice([('bulbs from a lot in which', 'are defective', 'defective'), ('students of a school in which', 'wear spectacles', 'wear spectacles'),
                    ('seeds of a variety of which', 'fail to germinate', 'fail to germinate'), ('customers of a bank of whom', 'use UPI daily', 'use UPI daily')])
    pc = r.choice([10, 20, 25, 30, 40, 50])
    p = Fr(pc, 100)
    q = 1 - p
    k = r.randint(0, 2)
    rr = r.randint(1, min(3, n - 1))
    if k == 0:
        val = binom(n, rr) * p ** rr * q ** (n - rr)
        ask = f'exactly {rr} {ctx[2]}'
    elif k == 1:
        val = q ** n
        ask = f'none {ctx[2]}'
    else:
        val = 1 - q ** n - n * p * q ** (n - 1)
        ask = f'at least 2 {ctx[2]}'
    return Q(f'A sample of {n} is taken from {ctx[0]} {pc}% {ctx[1]}. Assuming a binomial distribution, find the probability that {ask}.', f'{fz(val)} ≈ {num(float(val), 4)}',
             f'n = {n}, p = {fz(p)}, q = {fz(q)} (1 mark); use P(X = r) = ⁿCᵣpʳqⁿ⁻ʳ (2 marks).', dist3(f'{fz(val)} ≈ {num(float(val), 4)}', [f'{fz(1 - val)} ≈ {num(float(1 - val), 4)}', f'{fz(p ** rr)} ≈ {num(float(p ** rr), 4)}', f'{fz(q ** (n - 1))} ≈ {num(float(q ** (n - 1)), 4)}']))


def c7s2_ar(r):
    k = r.randint(0, 2)
    n = r.randint(4, 40)
    if k == 0:
        return ar(f'For B({n}, 1/2), the mean is {fz(Fr(n, 2))} and the variance is {fz(Fr(n, 4))}.', 'For B(n, p), mean = np and variance = npq.', 'a', 'Direct use.')
    if k == 1:
        return ar('A binomial distribution can have mean 4 and variance 6.', 'For a binomial distribution, variance = npq < np = mean.', 'd', 'Variance must be less than the mean; A false, R true.')
    return ar(f'Drawing {r.randint(3, 5)} cards one by one without replacement and counting aces is a binomial experiment.', 'Binomial trials must be independent with constant p.', 'd', 'Without replacement the trials are dependent; A false, R true.')


def c7s2_case(r):
    n = r.randint(5, 8)
    pc = r.choice([10, 20, 25, 40])
    p = Fr(pc, 100)
    q = 1 - p
    who = name(r)
    return Q((f'{who}, a quality inspector in {r.choice(CITIES)}, finds that {pc}% of the phone chargers from a supplier are faulty. A box of {n} chargers is tested. '
              f'(i) Find the mean and variance of the number of faulty chargers. (ii) Find the probability that no charger is faulty. (iii) Find the probability that at most one is faulty.'),
             f'(i) {fz(n * p)}, {fz(n * p * q)} (ii) {fz(q ** n)} (iii) {fz(q ** n + n * p * q ** (n - 1))}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ======================================================================= ch07 st3 Poisson distribution

c7s3_mcq = mcqbank([
    ('For a Poisson distribution with parameter λ, the mean is …', 'λ', ['λ²', '√λ', '1/λ'], 'Standard result.'),
    ('For a Poisson distribution, mean and variance are …', 'equal', ['mean > variance', 'mean < variance', 'unrelated'], 'Both equal λ.'),
    ('P(X = r) for a Poisson variate with parameter λ is …', 'e^(−λ)λʳ/r!', ['λʳ/r!', 'e^λ λʳ/r!', 'ⁿCᵣ λʳ'], 'Poisson formula.'),
    ('The Poisson distribution is a limiting case of the binomial when …', 'n is large, p is small and np = λ is finite', ['n is small and p is large', 'p = 1/2', 'n = 1'], 'Rare events.'),
    ('Which situation is best modelled by a Poisson distribution?', 'number of printing mistakes per page of a book', ['heights of students', 'number of heads in 5 tosses', 'marks out of 100'], 'Rare events in a fixed interval.'),
])


def c7s3_prob(r):
    lam = r.choice([1, 2, 3, Fr(1, 2), Fr(3, 2), 4])
    e = r4(math.exp(-float(lam)))
    k = r.randint(0, 2)
    rr = r.randint(1, 3)
    if k == 0:
        val = e * float(lam) ** rr / math.factorial(rr)
        stem = f'If X follows a Poisson distribution with mean {fz(lam)}, find P(X = {rr}). (Use e^(−{fz(lam)}) = {e}.)'
        sup = '¹²³'[rr - 1]
        lt = fz(lam) if lam.denominator == 1 else f'({fz(lam)})' if isinstance(lam, Fr) else fz(lam)
        key = (f'P(X = {rr}) = e^(−λ)λ{sup}/{rr}! = {e} × {lt}{sup}/{math.factorial(rr)} = {num(val, 4)}.' if rr > 1 else
               f'P(X = 1) = e^(−λ)λ = {e} × {fz(lam)} = {num(val, 4)}.')
    elif k == 1:
        val = 1 - e
        stem = f'If X follows a Poisson distribution with parameter {fz(lam)}, find P(X ≥ 1). (Use e^(−{fz(lam)}) = {e}.)'
        key = f'P(X ≥ 1) = 1 − P(X = 0) = 1 − {e} = {num(val, 4)}.'
    else:
        val = e * (1 + float(lam))
        stem = f'If X follows a Poisson distribution with mean {fz(lam)}, find P(X ≤ 1). (Use e^(−{fz(lam)}) = {e}.)'
        key = f'P(X ≤ 1) = e^(−λ)(1 + λ) = {e} × {num(1 + float(lam))} = {num(val, 4)}.'
    ans = num(val, 4)
    return Q(stem, ans, key, dist3(ans, [num(1 - val, 4), num(e * float(lam), 4), num(float(lam) ** rr / math.factorial(rr) * 0.5, 4), num(e, 4)]))


def c7s3_approx(r):
    n = r.choice([100, 200, 400, 500, 1000])
    lam = r.choice([1, 2, 3, 4])
    p = Fr(lam, n)
    e = r4(math.exp(-lam))
    rr = r.randint(0, 2)
    val = e * lam ** rr / math.factorial(rr)
    item = r.choice(['blades', 'bolts', 'screws', 'pens', 'bulbs'])
    return Q(f'The probability that a {item[:-1]} produced by a machine is defective is {fz(p)}. Using the Poisson approximation, find the probability that a packet of {n} {item} contains {"no" if rr == 0 else f"exactly {rr}"} defective {item[:-1] if rr == 1 else item}. (Use e^(−{lam}) = {e}.)',
             num(val, 4), f'λ = np = {n} × {fz(p)} = {lam} (1 mark); P(X = {rr}) = e^(−{lam}) × {lam}^{rr}/{rr}! = {num(val, 4)} (2 marks).'.replace('^0', '⁰').replace('^1', '¹').replace('^2', '²'),
             dist3(num(val, 4), [num(1 - val, 4), num(e, 4) if rr else num(e * lam, 4), num(float(p) ** rr, 4), num(val / 2, 4)]))


def c7s3_param(r):
    a = r.randint(0, 3)
    k = r.choice([1, 2, 3])
    lam = k * (a + 1)
    lhs = f'P(X = {a})' if k == 1 else f'{k}P(X = {a})'
    ask = r.choice(['mean', 'variance', 'standard deviation'])
    ans = surd(lam) if ask == 'standard deviation' else str(lam)
    pa = f'm^{a}/{math.factorial(a)}' if a > 1 else ('' if a == 0 else 'm')
    work = (f'{lhs} = P(X = {a + 1}) ⇒ {k} · e⁻ᵐ{pa} = e⁻ᵐ m^{a + 1}/{math.factorial(a + 1)} ⇒ m = {k} × {a + 1} = {lam}; '
            f'{ask} = {ans}.').replace('1 · ', '').replace('m^1/1', 'm').replace('m^1/', 'm/').replace('m^2', 'm²').replace('m^3', 'm³').replace('m^4', 'm⁴')
    dist = [str(lam * lam), str(lam + 1), surd(lam) if ask != 'standard deviation' else str(lam), str(k * a) if k * a not in (0, lam) else str(lam + 2)]
    return Q(f'A Poisson variate X satisfies {lhs} = P(X = {a + 1}). Find the {ask} of X.', ans, work, dist3(ans, dist))


def c7s3_ar(r):
    lam = r.randint(2, 9)
    k = r.randint(0, 1)
    if k == 0:
        return ar(f'A Poisson variate with mean {lam} has standard deviation √{lam}.', 'For a Poisson distribution, the variance equals the mean.', 'a', f'σ = √{lam}.')
    return ar(f'A Poisson distribution can have mean {lam} and variance {lam + 2}.', 'For a Poisson distribution, mean = variance = λ.', 'd', 'Mean and variance must be equal; A false, R true.')


def c7s3_case(r):
    lam = r.choice([2, 3, 4])
    e = r4(math.exp(-lam))
    who = name(r)
    return Q((f'At a toll plaza near {r.choice(CITIES)}, {who} records that on average {lam} vehicles arrive per minute, following a Poisson distribution. (Use e^(−{lam}) = {e}.) '
              f'(i) Write P(X = r). (ii) Find the probability that no vehicle arrives in a minute. (iii) Find the probability that at least two vehicles arrive in a minute.'),
             f'(i) e^(−{lam}){lam}ʳ/r! (ii) {num(e, 4)} (iii) {num(1 - e - e * lam, 4)}', '(i) 1 mark (ii) 1 mark (iii) 1 − P(0) − P(1) (2 marks).')


# ======================================================================= ch07 st4 normal distribution

c7s4_mcq = mcqbank([
    ('The standard normal variate is Z = …', '(X − μ)/σ', ['(X − σ)/μ', 'X/σ', '(μ − X)/σ²'], 'Standardisation.'),
    ('The mean and standard deviation of Z are …', '0 and 1', ['1 and 0', '0 and 0', 'μ and σ'], 'Standard normal.'),
    ('The total area under the normal curve is …', '1', ['0.5', '0', 'σ'], 'Total probability.'),
    ('For a normal distribution, mean, median and mode are …', 'equal', ['all different', 'mean > median > mode', 'mode > mean'], 'Symmetry.'),
    ('About what percentage of a normal population lies within μ ± σ?', '68.27%', ['95.45%', '99.73%', '50%'], 'Empirical rule.'),
    ('About what percentage of a normal population lies within μ ± 2σ?', '95.45%', ['68.27%', '99.73%', '90%'], 'Empirical rule.'),
    ('The normal curve is symmetric about …', 'the mean μ', ['zero always', 'σ', 'the median line x = σ'], 'Bell-shaped about μ.'),
])

ZS = [0.5, 0.8, 1.0, 1.2, 1.25, 1.5, 1.6, 1.75, 2.0, 2.2, 2.5, 0.25, 0.75, 1.4, 1.8]


def _musig(r):
    while True:
        mu = r.choice(range(40, 201, 5))
        sig = r.choice([2, 4, 5, 8, 10, 12, 15, 20])
        z = r.choice(ZS)
        x = mu + z * sig
        if float(x).is_integer():
            return mu, sig, z, int(x)


def c7s4_z(r):
    mu, sig, z, x = _musig(r)
    k = r.randint(0, 2)
    a = area0(z)
    if k == 0:
        val, ask = 0.5 - a, f'P(X > {x})'
        key = f'Z = ({x} − {mu})/{sig} = {num(z)} (1 mark); P(Z > {num(z)}) = 0.5 − {a} = {num(0.5 - a, 4)} (2 marks).'
    elif k == 1:
        val, ask = 0.5 + a, f'P(X < {x})'
        key = f'Z = ({x} − {mu})/{sig} = {num(z)} (1 mark); P(Z < {num(z)}) = 0.5 + {a} = {num(0.5 + a, 4)} (2 marks).'
    else:
        x2 = round(mu - z * sig)
        val, ask = 2 * a, f'P({x2} < X < {x})'
        key = f'Z-values ±{num(z)} (1 mark); P(−{num(z)} < Z < {num(z)}) = 2 × {a} = {num(2 * a, 4)} (2 marks).'
    return Q(f'X is normally distributed with mean {mu} and standard deviation {sig}. Find {ask}. (Given: P(0 < Z < {num(z)}) = {a}.)', num(val, 4), key,
             dist3(num(val, 4), [num(a, 4), num(1 - val, 4), num(0.5 + a if k != 1 else 0.5 - a, 4), num(a / 2, 4)]))


def c7s4_count(r):
    mu, sig, z, x = _musig(r)
    N = r.choice([200, 500, 1000, 2000, 5000])
    a = area0(z)
    cnt = round(N * (0.5 - a))
    who = r.choice(['students', 'employees', 'bulbs', 'applicants'])
    what = {'students': 'marks', 'employees': 'monthly wages (in ₹ hundred)', 'bulbs': 'lives (in hundred hours)', 'applicants': 'test scores'}[who]
    return Q(f'The {what} of {N} {who} are normally distributed with mean {mu} and standard deviation {sig}. Estimate how many have more than {x}. (Given: P(0 < Z < {num(z)}) = {a}.)', str(cnt),
             f'Z = ({x} − {mu})/{sig} = {num(z)} (1 mark); P(Z > {num(z)}) = {num(0.5 - a, 4)} (1 mark); number ≈ {N} × {num(0.5 - a, 4)} ≈ {cnt} (1 mark).',
             dist3(str(cnt), [str(round(N * a)), str(round(N * (0.5 + a))), str(N - cnt), str(cnt + 10)]))


def c7s4_ar(r):
    mu = r.choice(range(30, 101, 10))
    sig = r.choice([5, 10])
    k = r.randint(0, 1)
    if k == 0:
        return ar(f'If X ~ N({mu}, {sig}²), then P(X > {mu}) = 0.5.', 'The normal curve is symmetric about its mean.', 'a', 'Half the area lies on each side of μ.')
    return ar(f'If X ~ N({mu}, {sig}²), then Z = (X − {mu})/{sig} has mean {mu}.', 'Standardising subtracts the mean and divides by the standard deviation.', 'd', 'Z has mean 0 and SD 1; A false, R true.')


def c7s4_case(r):
    mu, sig, z, x = _musig(r)
    a = area0(z)
    who = name(r)
    x2 = round(mu - z * sig)
    return Q((f'The time taken by delivery riders of {who}\'s start-up in {r.choice(CITIES)} to deliver an order is normally distributed with mean {mu} minutes and '
              f'standard deviation {sig} minutes. (Given P(0 < Z < {num(z)}) = {a}.) (i) Find the Z-score of {x} minutes. (ii) Find the probability that a delivery takes more than {x} minutes. (iii) Find the probability that it takes between {x2} and {x} minutes.'),
             f'(i) {num(z)} (ii) {num(0.5 - a, 4)} (iii) {num(2 * a, 4)}', '(i) 1 mark (ii) 1 mark (iii) symmetry (2 marks).')


# ======================================================================= ch08 st1 population, sample, sampling methods

c8s1_mcq = mcqbank([
    ('A numerical value describing a population is called …', 'a parameter', ['a statistic', 'a sample', 'a variate'], 'Definition.'),
    ('A numerical value computed from a sample is called …', 'a statistic', ['a parameter', 'a population', 'a census'], 'Definition.'),
    ('Selecting every 10th name from a list after a random start is …', 'systematic sampling', ['simple random sampling', 'stratified sampling', 'cluster sampling'], 'Fixed interval after a random start.'),
    ('Dividing a population into homogeneous groups and sampling from each group is …', 'stratified sampling', ['systematic sampling', 'simple random sampling', 'convenience sampling'], 'Strata.'),
    ('In simple random sampling, …', 'every unit has an equal chance of being selected', ['only the first units are chosen', 'units are chosen by the investigator\'s choice', 'every 5th unit is chosen'], 'Definition.'),
    ('The population mean is usually denoted by …', 'μ', ['x̄', 's', 'n'], 'Notation.'),
    ('The sample mean is usually denoted by …', 'x̄', ['μ', 'σ', 'N'], 'Notation.'),
    ('A complete enumeration of all units of a population is called …', 'a census', ['a sample survey', 'a statistic', 'a stratum'], 'Definition.'),
    ('The difference between a statistic and the corresponding parameter is called …', 'sampling error', ['bias of the census', 'standard deviation', 'a stratum'], 'Definition.'),
])

c8s1_ident = mcqbank([
    ('The average height of all Class XII students in India is a …', 'parameter', ['statistic', 'sample', 'stratum'], 'It describes the whole population.'),
    ('The average height of 200 Class XII students chosen at random is a …', 'statistic', ['parameter', 'population', 'census'], 'It is computed from a sample.'),
    ('A survey selects 50 students from each of the four houses of a school. This is …', 'stratified sampling', ['systematic sampling', 'simple random sampling', 'census'], 'Each house is a stratum.'),
    ('Names of 500 employees are written on slips and 25 slips are drawn from a box. This is …', 'simple random sampling', ['systematic sampling', 'stratified sampling', 'cluster sampling'], 'Lottery method.'),
    ('From the attendance register, every 8th student after a random start of 3 is chosen. This is …', 'systematic sampling', ['simple random sampling', 'stratified sampling', 'convenience sampling'], 'Fixed interval.'),
    ('The proportion of voters in a city supporting a candidate, estimated from 1000 voters, is a …', 'statistic', ['parameter', 'census', 'population'], 'Computed from a sample.'),
])


def c8s1_sys(r):
    N = r.choice(range(200, 2001, 50))
    n = r.choice([d for d in (10, 20, 25, 40, 50) if N % d == 0] or [10])
    if N % n:
        raise ValueError
    k = N // n
    st = r.randint(1, k)
    sel = [st + k * i for i in range(4)]
    return Q(f'A systematic sample of {n} is to be drawn from a list of {N} customers. Find the sampling interval, and list the first four customers selected if the random start is {st}.', f'k = {k}; {", ".join(map(str, sel))}',
             f'k = N/n = {N}/{n} = {k} (1 mark); start {st}, then add {k} each time (1 mark).', dist3(f'k = {k}; {", ".join(map(str, sel))}', [f'k = {n}; {", ".join(str(st + n * i) for i in range(4))}', f'k = {k}; {", ".join(str(st + i) for i in range(4))}', f'k = {k + 1}; {", ".join(str(st + (k + 1) * i) for i in range(4))}']))


def c8s1_strat(r):
    n = r.choice([40, 50, 60, 80, 100, 120])
    while True:
        Ns = [r.choice(range(100, 1001, 50)) for _ in range(3)]
        N = sum(Ns)
        ns = [Fr(n * x, N) for x in Ns]
        if all(v.denominator == 1 for v in ns):
            break
    grp = r.choice([('Science', 'Commerce', 'Humanities'), ('Class X', 'Class XI', 'Class XII'), ('urban', 'semi-urban', 'rural')])
    ans = ', '.join(f'{g}: {fz(v)}' for g, v in zip(grp, ns))
    return Q(f'A school has {Ns[0]} {grp[0]}, {Ns[1]} {grp[1]} and {Ns[2]} {grp[2]} students. A stratified sample of {n} is to be drawn with proportional allocation. How many should be chosen from each stratum?', ans,
             f'nᵢ = n × Nᵢ/N with N = {N} (1 mark each pair).', dist3(ans, [', '.join(f'{g}: {fz(Fr(n, 3))}' for g in grp) if n % 3 == 0 else ', '.join(f'{g}: {fz(v + 1)}' for g, v in zip(grp, ns)), ', '.join(f'{g}: {fz(v)}' for g, v in zip(grp, reversed(ns))), ', '.join(f'{g}: {x // 10}' for g, x in zip(grp, Ns))]))


def c8s1_explain(r):
    return xbank([
        ('Distinguish between a parameter and a statistic, with an example of each.', 'Parameter: describes a population (e.g. μ of all voters); statistic: computed from a sample (e.g. x̄ of 500 voters).', 'Definitions with examples (2 marks).'),
        ('Give two advantages of a sample survey over a census.', 'It is cheaper and quicker, and allows more careful data collection.', 'Any two valid advantages (2 marks).'),
        ('When is stratified sampling preferred to simple random sampling?', 'When the population is heterogeneous but can be split into homogeneous groups.', 'Condition with reason (2 marks).'),
        ('What is meant by a sampling frame?', 'A complete list of the units of the population from which the sample is drawn.', 'Definition (2 marks).'),
        ('Why is the lottery method an example of simple random sampling?', 'Each slip, hence each unit, has an equal chance of being drawn.', 'Equal chance (2 marks).'),
    ])(r)


def c8s1_ar(r):
    return arbank([
        ('The mean income of 100 families selected from a city is a statistic.', 'A statistic is a value computed from sample data.', 'a', 'Sample-based value.'),
        ('A census always gives a better result than a sample survey in practice.', 'A sample survey can be cheaper and quicker and allows more careful checking.', 'd', 'Samples may be more accurate in practice; A false, R true.'),
        ('In systematic sampling, only the first unit is chosen at random.', 'The rest are chosen at a fixed interval k = N/n.', 'a', 'Definition.'),
        ('Stratified sampling divides the population into heterogeneous strata.', 'Strata should be internally homogeneous.', 'd', 'A false, R true.'),
    ])(r)


def c8s1_case(r):
    who = name(r)
    N = r.choice([600, 800, 1200, 1500])
    n = r.choice([30, 40, 50, 60])
    if N % n:
        raise ValueError
    return Q((f'{who} is planning a survey on screen time among the {N} students of a school in {r.choice(CITIES)}. (i) Identify the population and a possible sample. '
              f'(ii) For a systematic sample of {n} students from the roll list, find the interval. (iii) Is the average screen time of the {n} students a parameter or a statistic? Why?'),
             f'(i) All {N} students; e.g. {n} chosen from the roll list (ii) {N // n} (iii) A statistic: it is computed from the sample', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ======================================================================= ch08 st2 sampling distribution and CLT

c8s2_mcq = mcqbank([
    ('The standard deviation of the sampling distribution of the mean is called …', 'the standard error', ['the variance', 'the parameter', 'the bias'], 'Definition.'),
    ('For samples of size n from a population with SD σ, the standard error of x̄ is …', 'σ/√n', ['σ/n', 'σ√n', 'σ²/n'], 'Standard result.'),
    ('By the central limit theorem, for large n the sampling distribution of x̄ is approximately …', 'normal', ['uniform', 'binomial', 'Poisson'], 'CLT.'),
    ('The mean of the sampling distribution of x̄ equals …', 'the population mean μ', ['the sample size', 'σ/√n', 'zero'], 'Unbiasedness of x̄.'),
    ('As the sample size increases, the standard error …', 'decreases', ['increases', 'stays the same', 'becomes negative'], 'σ/√n falls as n rises.'),
    ('The CLT is usually applied when the sample size is at least about …', '30', ['5', '2', '1000'], 'Rule of thumb.'),
])


def c8s2_se(r):
    sig = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    n = r.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, 144])
    se = Fr(sig, int(math.isqrt(n)))
    return Q(f'A population has standard deviation {sig}. Find the standard error of the mean for samples of size {n}.', fz(se) if se.denominator == 1 else f'{fz(se)} ≈ {num(float(se), 3)}',
             f'SE = σ/√n = {sig}/√{n} = {fz(se)}.', dist3(fz(se) if se.denominator == 1 else f'{fz(se)} ≈ {num(float(se), 3)}', [fz(Fr(sig, n)), fz(sig * math.isqrt(n)), fz(Fr(sig * sig, n))]))


def c8s2_prob(r):
    mu = r.choice(range(40, 301, 10))
    sig = r.choice([6, 8, 10, 12, 15, 20, 24, 30])
    n = r.choice([36, 64, 100, 144])
    se = Fr(sig, math.isqrt(n))
    z = r.choice([1.0, 1.5, 2.0, 1.25, 0.5, 2.5])
    xb = mu + Fr(z).limit_denominator(4) * se
    if xb.denominator > 2:
        raise ValueError
    a = area0(z)
    return Q(f'The weights of packets have mean {mu} g and standard deviation {sig} g. For random samples of {n} packets, find the probability that the sample mean exceeds {num(float(xb))} g. (Given P(0 < Z < {num(z)}) = {a}.)', num(0.5 - a, 4),
             f'By the CLT, x̄ ~ N({mu}, ({fz(se)})²) (1 mark); Z = ({num(float(xb))} − {mu})/{"(" + fz(se) + ")" if "/" in fz(se) else fz(se)} = {num(z)} (1 mark); P = 0.5 − {a} = {num(0.5 - a, 4)} (1 mark).',
             dist3(num(0.5 - a, 4), [num(0.5 + a, 4), num(a, 4), num(1 - 2 * a, 4)]))


def c8s2_n(r):
    sig = r.choice([4, 5, 6, 8, 10, 12])
    se = r.choice([1, 2, Fr(1, 2)])
    n = (Fr(sig) / se) ** 2
    if n.denominator != 1 or n < 4:
        raise ValueError
    return Q(f'A population has standard deviation {sig}. How large a sample is needed for the standard error of the mean to be {fz(se)}?', f'n = {fz(n)}',
             f'σ/√n = {fz(se)} ⇒ √n = {fz(sig / se)} ⇒ n = {fz(n)}.', dist3(f'n = {fz(n)}', [f'n = {fz(sig / se)}', f'n = {fz(n * 2)}', f'n = {sig * sig}' if sig * sig != n else f'n = {fz(n / 2)}']))


def c8s2_ar(r):
    n = r.choice([16, 25, 36, 64, 100])
    return arbank([
        (f'Quadrupling the sample size halves the standard error of the mean.', 'SE = σ/√n.', 'a', '√(4n) = 2√n.'),
        ('The mean of all sample means equals the population mean.', 'The sample mean is an unbiased estimator of μ.', 'a', 'E(x̄) = μ.'),
        (f'For samples of size {n}, the standard error is σ/{n}.', 'The standard error of the mean is σ/√n.', 'd', f'It is σ/{math.isqrt(n)}; A false, R true.'),
        ('The central limit theorem requires the population itself to be normal.', 'For large n, x̄ is approximately normal whatever the shape of the population.', 'd', 'A false, R true.'),
    ])(r)


def c8s2_case(r):
    mu = r.choice(range(150, 401, 10))
    sig = r.choice([12, 15, 20, 24, 30])
    n = r.choice([36, 64, 100])
    se = Fr(sig, math.isqrt(n))
    z = 2.0
    a = area0(z)
    who = name(r)
    return Q((f'{who} studies the daily footfall at a mall in {r.choice(CITIES)}, with mean {mu} and standard deviation {sig}. Samples of {n} days are taken. '
              f'(i) State the mean of the sampling distribution of x̄. (ii) Find the standard error. (iii) Find the probability that a sample mean lies between {num(float(mu - 2 * se))} and {num(float(mu + 2 * se))}. (Given P(0 < Z < 2) = {a}.)'),
             f'(i) {mu} (ii) {fz(se)} (iii) {num(2 * a, 4)}', '(i) 1 mark (ii) 1 mark (iii) Z = ±2 (2 marks).')


# ======================================================================= ch08 st3 hypothesis testing

c8s3_mcq = mcqbank([
    ('The hypothesis of "no difference" that is tested is called …', 'the null hypothesis H₀', ['the alternative hypothesis', 'the level of significance', 'the critical region'], 'Definition.'),
    ('Rejecting H₀ when it is true is …', 'a Type I error', ['a Type II error', 'a correct decision', 'sampling error'], 'Definition.'),
    ('Accepting H₀ when it is false is …', 'a Type II error', ['a Type I error', 'a correct decision', 'a census error'], 'Definition.'),
    ('The level of significance α is the probability of …', 'a Type I error', ['a Type II error', 'accepting H₀', 'H₁ being true'], 'Definition.'),
    ('For a two-tailed z-test at the 5% level, the critical values are …', '±1.96', ['±2.58', '±1.645', '±3'], 'Standard normal.'),
    ('For a two-tailed z-test at the 1% level, the critical values are …', '±2.58', ['±1.96', '±1.645', '±2.33'], 'Standard normal.'),
    ('H₁: μ > 50 leads to …', 'a right-tailed test', ['a left-tailed test', 'a two-tailed test', 'no test'], 'Direction of H₁.'),
    ('H₁: μ ≠ 50 leads to …', 'a two-tailed test', ['a right-tailed test', 'a left-tailed test', 'a one-tailed test'], 'Both directions.'),
])


def c8s3_z(r):
    mu0 = r.choice(range(40, 301, 10))
    sig = r.choice([5, 6, 8, 10, 12, 15, 20])
    n = r.choice([25, 36, 49, 64, 100])
    se = Fr(sig, math.isqrt(n))
    z = r.choice([0.8, 1.2, 1.5, 1.8, 2.0, 2.2, 2.5, 3.0, -1.2, -2.2, -2.8])
    xb = mu0 + Fr(z).limit_denominator(10) * se
    if (xb * 10).denominator != 1:
        raise ValueError
    lvl, cv = r.choice([('5%', 1.96), ('1%', 2.58)])
    dec = 'reject H₀' if abs(z) > cv else 'do not reject H₀'
    return Q(f'A sample of {n} items has mean {num(float(xb), 1)}. Can it be regarded as drawn from a population with mean {mu0} and SD {sig} at the {lvl} level of significance (two-tailed)?',
             f'|z| = {num(abs(z), 2)}; {dec}',
             f'H₀: μ = {mu0}, H₁: μ ≠ {mu0} (1 mark); z = (x̄ − μ)/(σ/√n) = ({num(float(xb), 1)} − {mu0})/{"(" + fz(se) + ")" if "/" in fz(se) else fz(se)} = {num(z, 2)} (1 mark); critical value {cv}: {dec} (1 mark).',
             dist3(f'|z| = {num(abs(z), 2)}; {dec}', [f'|z| = {num(abs(z), 2)}; {"do not reject H₀" if dec == "reject H₀" else "reject H₀"}', f'|z| = {num(abs(z) * math.sqrt(n), 2)}; reject H₀', f'|z| = {num(abs(z) / math.sqrt(n), 2)}; do not reject H₀']))


def c8s3_explain(r):
    return xbank([
        ('Distinguish between Type I and Type II errors.', 'Type I: rejecting a true H₀; Type II: accepting a false H₀.', '1 mark each.'),
        ('State the steps of testing a hypothesis.', 'State H₀ and H₁; choose α; compute the test statistic; compare with the critical value; conclude.', 'Steps in order (2 marks).'),
        ('What is meant by the critical region?', 'The set of values of the test statistic for which H₀ is rejected.', 'Definition (2 marks).'),
        ('When is a one-tailed test used instead of a two-tailed test?', 'When H₁ states a direction (μ > μ₀ or μ < μ₀).', 'Direction of the alternative (2 marks).'),
    ])(r)


def c8s3_hyp(r):
    mu0 = r.choice(range(20, 501, 10))
    k = r.randint(0, 2)
    ctx = r.choice(['mean life of bulbs (hours)', 'mean weight of a packet (g)', 'mean daily sales (units)', 'mean waiting time (minutes)'])
    if k == 0:
        return Q(f'A manufacturer claims that the {ctx} is {mu0}. A consumer group suspects it is less. Write H₀ and H₁ and state the type of test.', f'H₀: μ = {mu0}; H₁: μ < {mu0}; left-tailed',
                 'Claim in H₀, suspicion in H₁ (1 mark each).', [f'H₀: μ < {mu0}; H₁: μ = {mu0}; left-tailed', f'H₀: μ = {mu0}; H₁: μ ≠ {mu0}; two-tailed', f'H₀: μ = {mu0}; H₁: μ > {mu0}; right-tailed'])
    if k == 1:
        return Q(f'A firm wants to check whether the {ctx} differs from {mu0}. Write H₀ and H₁ and state the type of test.', f'H₀: μ = {mu0}; H₁: μ ≠ {mu0}; two-tailed',
                 '"Differs" gives a two-sided alternative (2 marks).', [f'H₀: μ ≠ {mu0}; H₁: μ = {mu0}; two-tailed', f'H₀: μ = {mu0}; H₁: μ > {mu0}; right-tailed', f'H₀: μ = {mu0}; H₁: μ < {mu0}; left-tailed'])
    return Q(f'An agency claims that a new process increases the {ctx} above {mu0}. Write H₀ and H₁ and state the type of test.', f'H₀: μ = {mu0}; H₁: μ > {mu0}; right-tailed',
             '"Increases" gives a right-tailed alternative (2 marks).', [f'H₀: μ > {mu0}; H₁: μ = {mu0}; right-tailed', f'H₀: μ = {mu0}; H₁: μ ≠ {mu0}; two-tailed', f'H₀: μ = {mu0}; H₁: μ < {mu0}; left-tailed'])


def c8s3_ar(r):
    return arbank([
        ('Decreasing the level of significance from 5% to 1% makes it harder to reject H₀.', 'The critical value moves further from 0 (1.96 to 2.58).', 'a', 'A larger |z| is needed.'),
        ('Accepting H₀ proves that H₀ is true.', 'A test only shows whether the sample evidence is strong enough to reject H₀.', 'd', 'A false, R true.'),
        ('The level of significance is the probability of a Type II error.', 'A Type II error is accepting a false null hypothesis.', 'd', 'α is P(Type I error); A false, R true.'),
        ('H₁: μ ≠ 100 requires a two-tailed test.', 'The alternative allows the mean to be either above or below 100.', 'a', 'Two-sided alternative.'),
    ])(r)


def c8s3_case(r):
    mu0 = r.choice(range(200, 501, 50))
    sig = r.choice([10, 20, 30])
    n = r.choice([36, 64, 100])
    se = Fr(sig, math.isqrt(n))
    z = r.choice([1.5, 2.25, 2.5, 3.0, 1.25])
    xb = mu0 - Fr(z).limit_denominator(4) * se
    if (xb * 100).denominator != 1:
        raise ValueError
    who = name(r)
    dec = 'reject H₀' if z > 1.645 else 'do not reject H₀'
    return Q((f'A juice company claims that its bottles contain {mu0} ml on average (SD {sig} ml). {who} checks {n} bottles in {r.choice(CITIES)} and finds a mean of {num(float(xb), 2)} ml. '
              f'(i) Write H₀ and H₁ to test whether the bottles are under-filled. (ii) Find the test statistic. (iii) Decide at the 5% level (one-tailed critical value −1.645).'),
             f'(i) H₀: μ = {mu0}, H₁: μ < {mu0} (ii) z = {num(-z, 2)} (iii) {dec}', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= ch08 st4 t-test

c8s4_mcq = mcqbank([
    ('The t-test is used when …', 'the sample is small and the population SD is unknown', ['the sample is large and σ is known', 'data are categorical', 'the population is not normal'], 'Student\'s t.'),
    ('For a one-sample t-test with n observations, the degrees of freedom are …', 'n − 1', ['n', 'n + 1', 'n − 2'], 'One parameter estimated.'),
    ('For a two independent samples t-test with sizes n₁ and n₂, the degrees of freedom are …', 'n₁ + n₂ − 2', ['n₁ + n₂', 'n₁ + n₂ − 1', 'n₁n₂'], 'Two means estimated.'),
    ('In the one-sample t-test, t = …', '(x̄ − μ)/(s/√n)', ['(x̄ − μ)/(σ/n)', '(x̄ − μ)√n', 's/(x̄ − μ)'], 'Test statistic.'),
    ('As the degrees of freedom increase, the t-distribution approaches …', 'the standard normal distribution', ['the Poisson distribution', 'a uniform distribution', 'the binomial distribution'], 'Large-sample limit.'),
    ('The t-distribution, compared with the standard normal, has …', 'heavier tails', ['lighter tails', 'a larger peak', 'a non-zero mean'], 'Extra uncertainty from estimating σ.'),
])


def _sample(r, n, mean_target=None):
    while True:
        m = mean_target if mean_target is not None else r.randint(20, 80)
        devs = [r.randint(-6, 6) for _ in range(n - 1)]
        devs.append(-sum(devs))
        if abs(devs[-1]) <= 9 and len(set(devs)) > 2:
            xs = [m + d for d in devs]
            return xs, m, sum(d * d for d in devs)


def c8s4_one(r):
    n = r.choice([5, 6, 8, 9, 10])
    xs, m, ss = _sample(r, n)
    mu0 = m + r.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    s = math.sqrt(ss / (n - 1))
    t = (m - mu0) / (s / math.sqrt(n))
    cv = T_05[n - 1]
    dec = 'reject H₀' if abs(t) > cv else 'do not reject H₀'
    return Q(f'A sample of {n} gives the values {", ".join(map(str, xs))}. Test at the 5% level whether the population mean could be {mu0}. (Given t₀.₀₅ for {n - 1} d.f. = {cv}, two-tailed.)',
             f'x̄ = {m}, s = {num(s, 2)}, |t| = {num(abs(t), 2)}; {dec}',
             f'H₀: μ = {mu0} (1 mark); x̄ = {m}, Σ(x − x̄)² = {ss}, s = √({ss}/{n - 1}) = {num(s, 2)} (2 marks); t = (x̄ − μ)/(s/√n) = {num(t, 2)} (1 mark); compare with {cv}: {dec} (1 mark).',
             dist3(f'x̄ = {m}, s = {num(s, 2)}, |t| = {num(abs(t), 2)}; {dec}', [f'x̄ = {m}, s = {num(math.sqrt(ss / n), 2)}, |t| = {num(abs(m - mu0) / (math.sqrt(ss / n) / math.sqrt(n)), 2)}; {dec}',
                                                                                f'x̄ = {m}, s = {num(s, 2)}, |t| = {num(abs(t), 2)}; {"do not reject H₀" if dec == "reject H₀" else "reject H₀"}', f'x̄ = {m}, s = {num(s, 2)}, |t| = {num(abs(m - mu0) / s, 2)}; do not reject H₀']))


def c8s4_tstat(r):
    n = r.choice([9, 16, 25, 36])
    xb = r.randint(40, 200)
    mu0 = xb + r.choice([-6, -5, -4, -3, 3, 4, 5, 6])
    s = r.choice([3, 4, 5, 6, 8, 10, 12])
    t = Fr((xb - mu0) * math.isqrt(n), s)
    return Q(f'A random sample of {n} observations has mean {xb} and standard deviation s = {s}. Find the t-statistic for testing H₀: μ = {mu0}, and the degrees of freedom.', f't = {fz(t)}' + (f' ≈ {num(float(t), 2)}' if t.denominator != 1 else '') + f'; {n - 1} d.f.',
             f't = (x̄ − μ)/(s/√n) = ({xb} − {mu0})/({s}/{math.isqrt(n)}) (1 mark); d.f. = n − 1 = {n - 1} (1 mark).',
             dist3(f't = {fz(t)}' + (f' ≈ {num(float(t), 2)}' if t.denominator != 1 else '') + f'; {n - 1} d.f.', [f't = {fz(Fr(xb - mu0, s))}; {n - 1} d.f.', f't = {fz(t)}' + (f' ≈ {num(float(t), 2)}' if t.denominator != 1 else '') + f'; {n} d.f.', f't = {fz(Fr((xb - mu0) * n, s))}; {n - 1} d.f.']))


def c8s4_two(r):
    n1, n2 = r.choice([5, 6, 7, 8]), r.choice([5, 6, 7, 8])
    a, m1, ss1 = _sample(r, n1)
    b, m2, ss2 = _sample(r, n2, mean_target=m1 + r.choice([-6, -5, -4, -3, 3, 4, 5, 6, 8]))
    df = n1 + n2 - 2
    sp = math.sqrt((ss1 + ss2) / df)
    t = (m1 - m2) / (sp * math.sqrt(1 / n1 + 1 / n2))
    cv = T_05[df]
    dec = 'the difference is significant' if abs(t) > cv else 'the difference is not significant'
    g1, g2 = r.choice([('Method A', 'Method B'), ('Batch I', 'Batch II'), ('Diet A', 'Diet B'), ('Section A', 'Section B')])
    return Q(f'{g1}: {", ".join(map(str, a))}. {g2}: {", ".join(map(str, b))}. Test at the 5% level whether the two means differ significantly. (Given t₀.₀₅ for {df} d.f. = {cv}, two-tailed.)',
             f'x̄₁ = {m1}, x̄₂ = {m2}, s = {num(sp, 2)}, |t| = {num(abs(t), 2)}; {dec}',
             f'H₀: μ₁ = μ₂ (1 mark); means and Σ(x − x̄)² = {ss1}, {ss2} (1 mark); pooled s = √(({ss1} + {ss2})/{df}) = {num(sp, 2)} (1 mark); t = (x̄₁ − x̄₂)/(s√(1/{n1} + 1/{n2})) = {num(t, 2)} (1 mark); conclusion (1 mark).',
             dist3(f'x̄₁ = {m1}, x̄₂ = {m2}, s = {num(sp, 2)}, |t| = {num(abs(t), 2)}; {dec}', [f'x̄₁ = {m1}, x̄₂ = {m2}, s = {num(sp, 2)}, |t| = {num(abs(t), 2)}; {"the difference is not significant" if "is significant" in dec else "the difference is significant"}',
                                                                                              f'x̄₁ = {m1}, x̄₂ = {m2}, s = {num(math.sqrt((ss1 + ss2) / (n1 + n2)), 2)}, |t| = {num(abs(m1 - m2) / (math.sqrt((ss1 + ss2) / (n1 + n2)) * math.sqrt(1 / n1 + 1 / n2)), 2)}; {dec}',
                                                                                              f'x̄₁ = {m2}, x̄₂ = {m1}, s = {num(sp, 2)}, |t| = {num(abs(t) / 2, 2)}; the difference is not significant']))


def c8s4_ar(r):
    n = r.randint(5, 20)
    return arbank([
        (f'For a one-sample t-test with {n} observations, the degrees of freedom are {n - 1}.', 'One degree of freedom is lost in estimating the mean.', 'a', f'd.f. = n − 1 = {n - 1}.'),
        ('The t-test is preferred to the z-test for large samples with known σ.', 'The t-test is meant for small samples with unknown population SD.', 'd', 'A false, R true.'),
        (f'Two independent samples of sizes {n} and {n + 2} give {2 * n} degrees of freedom for the t-test.', 'For two independent samples, d.f. = n₁ + n₂ − 2.', 'a', f'{n} + {n + 2} − 2 = {2 * n}.'),
        ('In the t-test, s is computed with divisor n.', 'The unbiased estimate of σ² uses divisor n − 1.', 'd', 'A false, R true.'),
    ])(r)


def c8s4_case(r):
    n = r.choice([16, 25])
    xb = r.randint(50, 90)
    mu0 = xb - r.choice([2, 3, 4, 5])
    s = r.choice([4, 5, 6, 8, 10])
    t = Fr((xb - mu0) * math.isqrt(n), s)
    cv = T_05[n - 1]
    who = name(r)
    dec = 'reject H₀' if float(t) > cv else 'do not reject H₀'
    return Q((f'{who}, a teacher in {r.choice(CITIES)}, tries a new revision method with {n} students. Their mean score is {xb} with s = {s}; the usual mean is {mu0}. '
              f'(i) State H₀. (ii) Compute t and the degrees of freedom. (iii) Using t₀.₀₅ = {cv} (two-tailed), decide whether the method has changed the mean score.'),
             f'(i) H₀: μ = {mu0} (ii) t = {num(float(t), 2)}, {n - 1} d.f. (iii) {dec}', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= ch09 st1 components of a time series

c9s1_mcq = mcqbank([
    ('A time series is …', 'a set of observations of a variable arranged in chronological order', ['a set of random numbers', 'a frequency distribution', 'a sample survey'], 'Definition.'),
    ('The general tendency of a time series to increase or decrease over a long period is …', 'secular trend', ['seasonal variation', 'cyclical variation', 'irregular variation'], 'Definition.'),
    ('Variations that repeat within a year are …', 'seasonal variations', ['secular trend', 'cyclical variations', 'irregular variations'], 'Period less than a year.'),
    ('Business cycles of prosperity, recession, depression and recovery are …', 'cyclical variations', ['seasonal variations', 'secular trend', 'irregular variations'], 'Period more than a year.'),
    ('Variations caused by floods, wars or strikes are …', 'irregular variations', ['seasonal variations', 'secular trend', 'cyclical variations'], 'Unpredictable.'),
    ('In the multiplicative model, Y = …', 'T × S × C × I', ['T + S + C + I', 'T × S + C × I', 'T − S − C − I'], 'Model.'),
    ('In the additive model, Y = …', 'T + S + C + I', ['T × S × C × I', 'T × S + C', 'TS − CI'], 'Model.'),
])

c9s1_ident = mcqbank([
    ('Sale of umbrellas rising every monsoon is an example of …', 'seasonal variation', ['secular trend', 'cyclical variation', 'irregular variation'], 'Repeats within a year.'),
    ('Steady growth of India\'s population over decades is an example of …', 'secular trend', ['seasonal variation', 'irregular variation', 'cyclical variation'], 'Long-term movement.'),
    ('A sudden fall in production due to a cyclone is an example of …', 'irregular variation', ['secular trend', 'seasonal variation', 'cyclical variation'], 'Unforeseen cause.'),
    ('Alternating boom and depression in the economy every 7–10 years is an example of …', 'cyclical variation', ['seasonal variation', 'secular trend', 'irregular variation'], 'Business cycle.'),
    ('Higher sale of sweets during Diwali every year is an example of …', 'seasonal variation', ['cyclical variation', 'secular trend', 'irregular variation'], 'Festival season.'),
    ('A steady fall in the death rate over 50 years is an example of …', 'secular trend', ['seasonal variation', 'irregular variation', 'cyclical variation'], 'Long-term.'),
    ('More train bookings during summer vacations every year is an example of …', 'seasonal variation', ['secular trend', 'cyclical variation', 'irregular variation'], 'Repeats annually.'),
    ('A one-time spike in mask sales during an epidemic is an example of …', 'irregular variation', ['seasonal variation', 'secular trend', 'cyclical variation'], 'Unpredictable event.'),
])


def c9s1_explain(r):
    return xbank([
        ('Name the four components of a time series and give one example of any two.', 'Secular trend, seasonal, cyclical and irregular variations; e.g. population growth (trend), woollen sales in winter (seasonal).', 'Components (1 mark); examples (1 mark).'),
        ('Distinguish between seasonal and cyclical variations.', 'Seasonal: period within a year, regular; cyclical: period more than a year (business cycles).', 'Period and regularity (2 marks).'),
        ('State two uses of time series analysis in business.', 'Forecasting future sales/demand and planning production; comparing performance over time.', 'Any two uses (2 marks).'),
        ('When is the multiplicative model preferred to the additive model?', 'When the components are not independent and seasonal effects grow with the trend.', 'Condition (2 marks).'),
    ])(r)


def c9s1_ar(r):
    return arbank([
        ('Rise in demand for woollens in winter is a seasonal variation.', 'Seasonal variations repeat within a period of one year.', 'a', 'Annual pattern.'),
        ('Cyclical variations have a period of less than one year.', 'Business cycles usually last several years.', 'd', 'A false, R true.'),
        ('Irregular variations can be predicted accurately.', 'They arise from random, unforeseen events.', 'd', 'A false, R true.'),
        ('Secular trend describes the long-term movement of a series.', 'It is the general tendency over a long period.', 'a', 'Definition.'),
    ])(r)


def c9s1_case(r):
    who = name(r)
    city = r.choice(CITIES)
    return Q((f'{who} studies 10 years of monthly sales of an air-conditioner dealer in {city}. Sales rise every April–June, have grown steadily over the decade, dipped during a two-year slowdown, and fell sharply in a month of floods. '
              f'(i) Which component explains the April–June rise? (ii) Which explains the steady growth? (iii) Name the components shown by the slowdown and the flood month.'),
             '(i) Seasonal variation (ii) Secular trend (iii) Cyclical variation; irregular variation', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ======================================================================= ch09 st2 moving averages

def _series(r, n):
    base = r.randint(20, 200)
    step = r.randint(-3, 8)
    return [base + step * i + r.randint(-6, 6) for i in range(n)]


def c9s2_three(r):
    k = r.choice([3, 5])
    n = r.choice([6, 7, 8]) if k == 3 else r.choice([7, 8, 9])
    ys = _series(r, n)
    y0 = r.randint(2010, 2016)
    ma = [Fr(sum(ys[i:i + k]), k) for i in range(n - k + 1)]
    yrs = ', '.join(f'{y0 + i}: {v}' for i, v in enumerate(ys))
    ans = ', '.join(num(float(v), 2) for v in ma)
    return Q(f'Compute the {k}-yearly moving averages for the data (year: value) {yrs}.', ans,
             f'Each value is the mean of {k} successive values, placed against the middle year ({y0 + k // 2} onwards) (1 mark per correct set of values; 3 marks).',
             dist3(ans, [', '.join(num(float(Fr(sum(ys[i:i + k]), k)) + 1, 2) for i in range(n - k + 1)), ', '.join(str(sum(ys[i:i + k])) for i in range(n - k + 1)), ', '.join(num(float(Fr(sum(ys[i:i + k - 1]), k - 1)), 2) for i in range(n - k + 2))]))


def c9s2_four(r):
    n = r.choice([7, 8])
    ys = _series(r, n)
    y0 = r.randint(2010, 2016)
    tot = [sum(ys[i:i + 4]) for i in range(n - 3)]
    cen = [Fr(tot[i] + tot[i + 1], 8) for i in range(len(tot) - 1)]
    yrs = ', '.join(f'{y0 + i}: {v}' for i, v in enumerate(ys))
    ans = ', '.join(num(float(v), 3) for v in cen)
    return Q(f'Compute the 4-yearly centred moving averages for the data (year: value) {yrs}.', ans,
             f'4-yearly totals {", ".join(map(str, tot))} (2 marks); 2-item totals of these divided by 8 give the centred averages against {y0 + 2} onwards (3 marks).',
             dist3(ans, [', '.join(num(t / 4, 3) for t in tot), ', '.join(num(float(v) + 0.5, 3) for v in cen), ', '.join(num(float(Fr(tot[i] + tot[i + 1], 4)), 3) for i in range(len(tot) - 1))]))


def c9s2_one(r):
    ys = _series(r, 5)
    k = 3
    y0 = r.randint(2015, 2019)
    i = r.randint(0, 2)
    v = Fr(sum(ys[i:i + 3]), 3)
    return Q(f'Sales (₹ lakh) for {y0}–{y0 + 4} are {", ".join(map(str, ys))}. Find the 3-yearly moving average for {y0 + i + 1}.', num(float(v), 2),
             f'({" + ".join(map(str, ys[i:i + 3]))})/3 = {num(float(v), 2)}.', dist3(num(float(v), 2), [num(float(Fr(sum(ys[i:i + 2]), 2)), 2), num(float(Fr(sum(ys), 5)), 2), str(sum(ys[i:i + 3]))]))


c9s2_mcq = mcqbank([
    ('For an odd period moving average, the averages are placed against …', 'the middle year of each group', ['the first year', 'the last year', 'between two years'], 'Centring.'),
    ('For a 4-yearly moving average, centring is needed because …', 'the averages fall between two years', ['the data are odd in number', 'the trend is non-linear', 'there are no seasons'], 'Even period.'),
    ('A moving average of the right period removes …', 'regular cyclical or seasonal fluctuations of that period', ['the trend', 'all the data', 'the first value only'], 'Smoothing.'),
    ('A drawback of the moving-average method is that …', 'trend values are lost at the beginning and end of the series', ['it needs a straight line', 'it is too mathematical', 'it cannot use yearly data'], 'Loss of end values.'),
    ('The number of 3-yearly moving averages from 10 yearly values is …', '8', ['10', '7', '9'], 'n − k + 1.'),
])


def c9s2_ar(r):
    n = r.randint(7, 15)
    return arbank([
        (f'From {n} yearly values, {n - 2} three-yearly moving averages can be computed.', 'The number of k-period moving averages from n values is n − k + 1.', 'a', f'{n} − 3 + 1.'),
        ('Moving averages give trend values for every year of the series.', 'Values at the beginning and end of the series are lost.', 'd', 'A false, R true.'),
        ('A 4-yearly moving average must be centred.', 'Its averages fall midway between two years.', 'a', 'Even period.'),
    ])(r)


def c9s2_case(r):
    ys = _series(r, 7)
    y0 = r.randint(2012, 2017)
    ma = [Fr(sum(ys[i:i + 3]), 3) for i in range(5)]
    who = name(r)
    return Q((f'{who} tracks the yearly production (thousand tonnes) of a sugar mill near {r.choice(CITIES)} for {y0}–{y0 + 6}: {", ".join(map(str, ys))}. '
              f'(i) How many 3-yearly moving averages can be found? (ii) Find them. (iii) Against which years are the first and last placed?'),
             f'(i) 5 (ii) {", ".join(num(float(v), 2) for v in ma)} (iii) {y0 + 1} and {y0 + 5}', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= ch09 st3 least squares

def _ls(r, n):
    y0 = r.randint(2014, 2019)
    a = r.randint(30, 150)
    b = r.choice([2, 3, 4, 5, 6, -2, -3])
    ys = [a + b * (i - n // 2) + r.randint(-4, 4) for i in range(n)]
    X = [i - n // 2 for i in range(n)]
    A = Fr(sum(ys), n)
    B = Fr(sum(x * y for x, y in zip(X, ys)), sum(x * x for x in X))
    return y0, ys, X, A, B


def c9s3_fit(r):
    n = r.choice([5, 7])
    y0, ys, X, A, B = _ls(r, n)
    mid = y0 + n // 2
    ans = f'y = {num(float(A), 2)} {"+" if B >= 0 else "−"} {num(abs(float(B)), 2)}X, X = t − {mid}'
    return Q(f'Fit a straight-line trend by the method of least squares to the data (year: value) {", ".join(f"{y0 + i}: {v}" for i, v in enumerate(ys))}.', ans,
             f'Take X = t − {mid} so ΣX = 0 (1 mark); Σy = {sum(ys)}, ΣXy = {sum(x * y for x, y in zip(X, ys))}, ΣX² = {sum(x * x for x in X)} (2 marks); a = Σy/n = {num(float(A), 2)}, b = ΣXy/ΣX² = {num(float(B), 2)} (2 marks).',
             dist3(ans, [f'y = {num(float(B), 2)} {"+" if A >= 0 else "−"} {num(abs(float(A)), 2)}X, X = t − {mid}', f'y = {num(float(A), 2)} {"+" if B >= 0 else "−"} {num(abs(float(B)) * 2, 2)}X, X = t − {mid}', f'y = {num(float(A) + 1, 2)} {"+" if B >= 0 else "−"} {num(abs(float(B)), 2)}X, X = t − {mid}']))


def c9s3_pred(r):
    a = r.randint(40, 300)
    b = r.choice([2, 3, 4, 5, 6, 8, Fr(5, 2), Fr(3, 2)])
    mid = r.randint(2018, 2022)
    t = mid + r.randint(3, 8)
    val = a + b * (t - mid)
    return Q(f'The trend equation of sales (₹ lakh) is y = {a} + {fz(b)}X, with origin at {mid} and X in years. Estimate the sales for {t}.', f'₹{num(float(val), 2)} lakh',
             f'X = {t} − {mid} = {t - mid}; y = {a} + {fz(b)} × {t - mid} = {num(float(val), 2)}.', dist3(f'₹{num(float(val), 2)} lakh', [f'₹{num(float(a + b), 2)} lakh', f'₹{num(float(a * (t - mid)), 2)} lakh', f'₹{num(float(a + b * (t - mid + 1)), 2)} lakh']))


def c9s3_trendvals(r):
    n = 5
    y0, ys, X, A, B = _ls(r, n)
    tv = [A + B * x for x in X]
    ans = ', '.join(num(float(v), 2) for v in tv)
    return Q(f'For the data (year: value) {", ".join(f"{y0 + i}: {v}" for i, v in enumerate(ys))}, the least-squares trend is y = {num(float(A), 2)} {"+" if B >= 0 else "−"} {num(abs(float(B)), 2)}X (origin {y0 + 2}). Find the trend values.', ans,
             'Substitute X = −2, −1, 0, 1, 2 (1 mark each pair; 3 marks).', dist3(ans, [', '.join(num(float(A - B * x), 2) for x in X), ', '.join(map(str, ys)), ', '.join(num(float(A + 2 * B * x), 2) for x in X)]))


c9s3_mcq = mcqbank([
    ('In the method of least squares, the trend line minimises …', 'the sum of squares of deviations of actual from trend values', ['the sum of deviations', 'the largest deviation', 'the number of points'], 'Principle of least squares.'),
    ('If X is measured from the middle year of an odd number of years, then ΣX = …', '0', ['n', '1', 'ΣY'], 'Symmetric deviations.'),
    ('With ΣX = 0, the constants of y = a + bX are …', 'a = Σy/n, b = ΣXy/ΣX²', ['a = ΣXy/ΣX², b = Σy/n', 'a = Σy, b = ΣX', 'a = 0, b = Σy/ΣX'], 'Normal equations.'),
    ('In y = a + bX, b gives …', 'the change in trend value per unit of time', ['the trend value at the origin', 'the seasonal index', 'the irregular component'], 'Slope.'),
    ('An advantage of the least-squares method over moving averages is that …', 'it gives trend values for all years and allows forecasting', ['it needs no calculation', 'it removes all variation', 'it ignores the data'], 'Line of best fit.'),
])


def c9s3_ar(r):
    return arbank([
        ('A least-squares trend line can be used to forecast future values.', 'It gives an equation for the trend as a function of time.', 'a', 'Extrapolate the line.'),
        ('In y = a + bX with ΣX = 0, a equals the mean of the observed values.', 'The normal equation Σy = na + bΣX reduces to Σy = na.', 'a', 'a = ȳ.'),
        ('A negative value of b shows an increasing trend.', 'b is the change in the trend value per unit time.', 'd', 'Negative b means a falling trend; A false, R true.'),
    ])(r)


def c9s3_case(r):
    y0, ys, X, A, B = _ls(r, 5)
    t = y0 + 2 + r.randint(4, 7)
    who = name(r)
    return Q((f'{who}, an analyst in {r.choice(CITIES)}, has the yearly profits (₹ lakh) of a firm for {y0}–{y0 + 4}: {", ".join(map(str, ys))}. '
              f'(i) Taking the origin at {y0 + 2}, find ΣXy and ΣX². (ii) Fit the least-squares trend line. (iii) Estimate the profit for {t}.'),
             f'(i) {sum(x * y for x, y in zip(X, ys))}, 10 (ii) y = {num(float(A), 2)} {"+" if B >= 0 else "−"} {num(abs(float(B)), 2)}X (iii) ₹{num(float(A + B * (t - y0 - 2)), 2)} lakh',
             '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= ch10 perpetuity

c10s1_mcq = mcqbank([
    ('A perpetuity is an annuity whose payments …', 'continue for ever', ['last for a fixed number of years', 'are made only once', 'grow without limit'], 'Definition.'),
    ('The present value of an immediate perpetuity of R per period at rate i per period is …', 'R/i', ['Ri', 'R(1 + i)/i²', 'R/(1 + i)'], 'Sum of an infinite GP.'),
    ('The present value of a perpetuity due (payments at the beginning) is …', 'R + R/i', ['R/i', 'R/(i(1 + i))', 'R − R/i'], 'First payment now.'),
    ('The present value of a growing perpetuity with first payment R, growth g and rate i (i > g) is …', 'R/(i − g)', ['R/(i + g)', 'R/i − g', 'R(1 + g)/i'], 'Growing perpetuity.'),
    ('Which is an example of a perpetuity?', 'a scholarship paid every year from an endowment fund for ever', ['a 20-year home loan', 'a 5-year recurring deposit', 'a one-time prize'], 'Payments for ever.'),
])


def c10s1_pv(r):
    R = r.choice(range(1000, 100001, 500))
    i = r.choice([4, 5, 6, 8, 10, 12, 2.5])
    k = r.randint(0, 2)
    ir = i / 100
    if k == 0:
        pv = R / ir
        return Q(f'Find the present value of a perpetuity of {inr(R)} payable at the end of every year, if money is worth {num(i)}% per annum.', money(pv),
                 f'PV = R/i = {R}/{num(ir, 4)} = {money(pv)}.', dist3(money(pv), [money(R * ir), money(R / ir + R), money(R / (1 + ir))]))
    if k == 1:
        pv = R + R / ir
        return Q(f'Find the present value of a perpetuity due of {inr(R)} per year (payments at the beginning of each year) at {num(i)}% per annum.', money(pv),
                 f'PV = R + R/i = {R} + {R}/{num(ir, 4)} = {money(pv)}.', dist3(money(pv), [money(R / ir), money(R / ir - R), money(R * (1 + ir) / ir ** 2)]))
    m = r.choice([2, 4, 12])
    j = ir / m
    Rm = R / m if (R / m).is_integer() else R
    pv = Rm / j
    per = {2: 'half-year', 4: 'quarter', 12: 'month'}[m]
    return Q(f'Find the present value of a perpetuity of {inr(Rm)} payable at the end of every {per}, if money is worth {num(i)}% per annum compounded {"semi-annually" if m == 2 else "quarterly" if m == 4 else "monthly"}.', money(pv),
             f'i per {per} = {num(i)}%/{m} = {num(j, 6)}; PV = R/i = {money(pv)}.', dist3(money(pv), [money(Rm / ir), money(Rm * m / j), money(Rm / j + Rm)]))


def c10s1_find(r):
    i = r.choice([4, 5, 6, 8, 10, 12, 2.5])
    pv = r.choice(range(50000, 2000001, 10000))
    R = pv * i / 100
    k = r.randint(0, 1)
    if k == 0:
        return Q(f'A sum of {inr(pv)} is invested now at {num(i)}% per annum to provide a perpetual annual payment (a perpetuity) at the end of each year. Find the annual payment.', money(R),
                 f'R = PV × i = {pv} × {num(i / 100, 4)} = {money(R)}.', dist3(money(R), [money(pv / i), money(R * 2), money(pv * i)]))
    return Q(f'A perpetuity of {money(R)} per year has a present value of {inr(pv)}. Find the rate of interest per annum.', f'{num(i)}%',
             f'i = R/PV = {num(R)}/{pv} = {num(i / 100, 4)} = {num(i)}%.', dist3(f'{num(i)}%', [f'{num(i * 2)}%', f'{num(i / 2)}%', f'{num(i + 1)}%']))


def c10s1_grow(r):
    R = r.choice(range(1000, 50001, 500))
    i, g = r.choice([(10, 4), (12, 5), (8, 3), (10, 5), (9, 4), (12, 6), (15, 5)])
    pv = R / ((i - g) / 100)
    return Q(f'A company will pay a dividend of {inr(R)} next year, growing at {g}% per year for ever. If the required rate of return is {i}% per annum, find the present value of the dividends.', money(pv),
             f'Growing perpetuity: PV = R/(i − g) = {R}/({i / 100} − {g / 100}) = {money(pv)} (3 marks).'.replace('0.1 ', '0.10 '),
             dist3(money(pv), [money(R / (i / 100)), money(R / ((i + g) / 100)), money(R * (1 + g / 100) / ((i - g) / 100))]))


def c10s1_defer(r):
    R = r.choice(range(5000, 100001, 1000))
    i = r.choice([5, 8, 10])
    m = r.choice([2, 3, 4, 5])
    f = r4((1 + i / 100) ** m)
    pv = R / (i / 100) / f
    return Q(f'Find the present value of a perpetuity of {inr(R)} per year whose first payment is made at the end of {m + 1} years, at {i}% per annum. (Use (1.{i:02d})^{m} = {f}.)'.replace('(1.10)', '(1.1)'), money(pv),
             f'Value at the end of {m} years = R/i = {money(R / (i / 100))} (2 marks); discount {m} years: {money(R / (i / 100))}/{f} = {money(pv)} (3 marks).',
             dist3(money(pv), [money(R / (i / 100)), money(R / (i / 100) / r4((1 + i / 100) ** (m + 1))), money(R / (i / 100) * f)]))


def c10s1_ar(r):
    R = r.choice(range(1000, 20001, 1000))
    i = r.choice([5, 10])
    return arbank([
        (f'The present value of a perpetuity of {inr(R)} per year at {i}% p.a. is {inr(R * 100 // i)}.', 'PV of an immediate perpetuity = R/i.', 'a', 'Direct use.'),
        ('A perpetuity due is worth less than the corresponding immediate perpetuity.', 'In a perpetuity due, each payment is received one period earlier.', 'd', 'It is worth more (R more); A false, R true.'),
        ('The formula R/(i − g) for a growing perpetuity needs i > g.', 'The geometric series of discounted payments converges only if (1 + g)/(1 + i) < 1.', 'a', 'Convergence condition.'),
    ])(r)


def c10s1_case(r):
    R = r.choice(range(10000, 100001, 5000))
    i = r.choice([5, 8, 10])
    who = name(r)
    return Q((f'{who}\'s family wants to set up a scholarship at a college in {r.choice(CITIES)} paying {inr(R)} at the end of every year for ever. Money earns {i}% per annum. '
              f'(i) What type of annuity is this? (ii) How much must be donated now? (iii) How much more is needed if the first scholarship is to be paid immediately?'),
             f'(i) An immediate perpetuity (ii) {money(R / (i / 100))} (iii) {inr(R)} more ({money(R + R / (i / 100))} in all)', '(i) 1 mark (ii) 1 mark (iii) perpetuity due (2 marks).')


# ======================================================================= ch10 st2 sinking fund

c10s2_mcq = mcqbank([
    ('A sinking fund is …', 'a fund built by regular deposits to meet a known future liability', ['a loan repaid in instalments', 'a fund that loses value', 'a one-time deposit'], 'Definition.'),
    ('The periodic deposit R into a sinking fund to accumulate S in n periods at rate i is …', 'R = Si/((1 + i)ⁿ − 1)', ['R = S/n', 'R = S(1 + i)ⁿ', 'R = Si(1 + i)ⁿ/((1 + i)ⁿ − 1)'], 'Future value of an annuity.'),
    ('The amount in a sinking fund after n deposits of R at rate i is …', 'R[(1 + i)ⁿ − 1]/i', ['nR', 'R(1 + i)ⁿ', 'R/i'], 'Annuity amount.'),
    ('A company creates a sinking fund mainly to …', 'replace an asset or repay a debt at a future date', ['pay daily wages', 'reduce taxes immediately', 'buy shares daily'], 'Purpose.'),
])


def _fv(r):
    i = r.choice([4, 5, 6, 8, 10, 12])
    n = r.choice([4, 5, 6, 8, 10])
    f = r4((1 + i / 100) ** n)
    return i, n, f


def c10s2_dep(r):
    i, n, f = _fv(r)
    Sx = r.choice(range(100000, 5000001, 50000))
    R = Sx * (i / 100) / (f - 1)
    return Q(f'How much should be deposited at the end of every year in a sinking fund earning {i}% per annum compounded annually to accumulate {inr(Sx)} in {n} years? (Use (1.{i:02d})^{n} = {f}.)'.replace('(1.10)', '(1.1)'), money(R),
             f'R = Si/((1 + i)ⁿ − 1) = {Sx} × {i / 100}/({f} − 1) = {money(R)} (3 marks).', dist3(money(R), [money(Sx / n), money(Sx * (i / 100) * f / (f - 1)), money(Sx / f)]))


def c10s2_amt(r):
    i, n, f = _fv(r)
    R = r.choice(range(5000, 200001, 5000))
    A = R * (f - 1) / (i / 100)
    return Q(f'A company deposits {inr(R)} at the end of every year into a sinking fund earning {i}% per annum. Find the amount in the fund after {n} years. (Use (1.{i:02d})^{n} = {f}.)'.replace('(1.10)', '(1.1)'), money(A),
             f'A = R[(1 + i)ⁿ − 1]/i = {R}({f} − 1)/{i / 100} = {money(A)}.', dist3(money(A), [money(R * n), money(R * f), money(R * (f - 1))]))


def c10s2_machine(r):
    i, n, f = _fv(r)
    cost = r.choice(range(200000, 3000001, 50000))
    scrap = r.choice(range(10000, cost // 5, 5000))
    need = cost - scrap
    R = need * (i / 100) / (f - 1)
    who = r.choice(['A printing press', 'A textile mill', 'A bakery', 'A courier company'])
    return Q(f'{who} buys a machine for {inr(cost)} with a life of {n} years and scrap value {inr(scrap)}. A new machine will cost the same. Find the annual sinking-fund deposit at {i}% per annum needed to replace it. (Use (1.{i:02d})^{n} = {f}.)'.replace('(1.10)', '(1.1)'), money(R),
             f'Amount needed = {inr(cost)} − {inr(scrap)} = {inr(need)} (2 marks); R = {need} × {i / 100}/({f} − 1) = {money(R)} (3 marks).',
             dist3(money(R), [money(cost * (i / 100) / (f - 1)), money(need / n), money(need * (i / 100) * f / (f - 1))]))


def c10s2_ar(r):
    return arbank([
        ('Deposits into a sinking fund earn compound interest.', 'A sinking fund accumulates like the amount of an ordinary annuity.', 'a', 'Annuity amount.'),
        ('A sinking fund is used to pay back a loan in equal monthly instalments called EMIs.', 'EMIs repay a loan through an amortisation schedule.', 'd', 'Sinking funds accumulate money; A false, R true.'),
        ('A higher interest rate reduces the deposit needed in a sinking fund for the same target.', 'Each deposit grows more in value by the target date.', 'a', 'R = Si/((1 + i)ⁿ − 1) falls as i rises.'),
    ])(r)


def c10s2_case(r):
    i, n, f = _fv(r)
    cost = r.choice(range(500000, 5000001, 100000))
    R = cost * (i / 100) / (f - 1)
    who = name(r)
    return Q((f'{who}\'s school in {r.choice(CITIES)} plans to buy a new bus costing {inr(cost)} in {n} years by depositing a fixed sum at the end of every year in a fund earning {i}% p.a. (Use (1.{i:02d})^{n} = {f}.) '
              f'(i) What is such a fund called? (ii) Find the annual deposit. (iii) Find the total interest earned by the fund.').replace('(1.10)', '(1.1)'),
             f'(i) A sinking fund (ii) {money(R)} (iii) {money(cost - n * round(R, 2))}', '(i) 1 mark (ii) 2 marks (iii) target − total deposits (1 mark).')


# ======================================================================= ch10 st3 applications

def c10s3_endow(r):
    R = r.choice(range(5000, 50001, 1000))
    m = r.choice([1, 2, 3])
    i = r.choice([5, 8, 10])
    who = name(r)
    k = r.randint(0, 1)
    if k == 0:
        nawards = r.randint(2, 5)
        need = nawards * R / (i / 100)
        return Q(f'{who} wants to endow {nawards} annual prizes of {inr(R)} each at a school, paid at the end of every year for ever. If money earns {i}% per annum, how much must be donated?', money(need),
                 f'Annual payment = {nawards} × {R} = {nawards * R} (1 mark); PV = R/i = {money(need)} (2 marks).', dist3(money(need), [money(R / (i / 100)), money(need + nawards * R), money(nawards * R * i)]))
    P = r.choice(range(100000, 2000001, 50000))
    R = P * i / 100
    return Q(f'A trust has {inr(P)} invested at {i}% per annum. What is the largest annual scholarship it can pay for ever?', money(R), f'R = PV × i = {P} × {i / 100} = {money(R)}.', dist3(money(R), [money(P / i), money(R / 2), money(R * 2)]))


def c10s3_compare(r):
    i, n, f = _fv(r)
    cost = r.choice(range(100000, 1000001, 25000))
    scrap = r.choice(range(5000, cost // 5, 5000))
    R = (cost - scrap) * (i / 100) / (f - 1)
    lump = (cost - scrap) / f
    return Q(f'A machine costing {inr(cost)} must be replaced after {n} years; its scrap value will be {inr(scrap)}. Compare (a) a sinking fund with equal deposits at the end of each year, and (b) a single deposit made now, at {i}% p.a. (Use (1.{i:02d})^{n} = {f}.)'.replace('(1.10)', '(1.1)'),
             f'(a) {money(R)} per year (b) {money(lump)} now',
             f'Amount needed {inr(cost - scrap)} (1 mark); (a) R = Si/((1 + i)ⁿ − 1) = {money(R)} (2 marks); (b) P = S/(1 + i)ⁿ = {money(lump)} (2 marks).')


def c10s3_ar(r):
    return arbank([
        ('An endowment that pays a fixed prize every year for ever is valued as a perpetuity.', 'Its payments continue indefinitely.', 'a', 'PV = R/i.'),
        ('To replace a machine, the sinking fund must accumulate the full cost of the new machine even if the old one has scrap value.', 'Scrap value received at replacement reduces the amount needed.', 'd', 'Only cost − scrap is needed; A false, R true.'),
    ])(r)


def c10s3_mcq(r):
    return mcqbank([
        ('The money needed now to fund a prize of ₹R a year for ever at rate i is …', 'R/i', ['Ri', 'R(1 + i)', 'R/(1 + i)'], 'Perpetuity.'),
        ('When an asset is replaced using a sinking fund, the target amount is usually …', 'cost of the new asset − scrap value of the old', ['cost of the new asset + scrap', 'scrap value only', 'annual depreciation'], 'Net requirement.'),
        ('A fund that pays scholarships for ever from its interest is called …', 'an endowment fund', ['a sinking fund', 'an EMI', 'a bond'], 'Terminology.'),
    ])(r)


def c10s3_case(r):
    i, n, f = _fv(r)
    cost = r.choice(range(200000, 2000001, 50000))
    scrap = r.choice(range(10000, cost // 5, 10000))
    R = (cost - scrap) * (i / 100) / (f - 1)
    who = name(r)
    return Q((f'{who} runs a cold-storage unit in {r.choice(CITIES)}. A compressor costing {inr(cost)} will need replacement in {n} years and will then fetch {inr(scrap)} as scrap. Money earns {i}% p.a. (Use (1.{i:02d})^{n} = {f}.) '
              f'(i) Find the amount needed at the end of {n} years. (ii) Find the annual sinking-fund deposit. (iii) Find the total of the deposits.').replace('(1.10)', '(1.1)'),
             f'(i) {inr(cost - scrap)} (ii) {money(R)} (iii) {money(n * round(R, 2))}', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= ch11 st1 bonds

c11s1_mcq = mcqbank([
    ('The face value of a bond is …', 'the amount printed on it, usually repaid at maturity', ['its market price', 'the coupon paid each year', 'the yield'], 'Definition.'),
    ('The coupon of a bond is …', 'the periodic interest = coupon rate × face value', ['the market price', 'the redemption value', 'the yield to maturity'], 'Definition.'),
    ('If the yield (market rate) is higher than the coupon rate, the bond sells …', 'at a discount', ['at a premium', 'at par', 'for free'], 'Price below face value.'),
    ('If the yield is lower than the coupon rate, the bond sells …', 'at a premium', ['at a discount', 'at par', 'below scrap value'], 'Price above face value.'),
    ('The price of a bond is the present value of …', 'its coupons and its redemption value', ['its coupons only', 'its face value only', 'its market price'], 'Valuation.'),
    ('A zero-coupon bond pays …', 'no periodic interest, only the face value at maturity', ['interest every month', 'only interest, never the face value', 'double interest'], 'Definition.'),
])


def _bond(r):
    Fv = r.choice([1000, 5000, 10000, 100000])
    c = r.choice([5, 6, 7, 8, 9, 10, 12])
    y = r.choice([x for x in (5, 6, 7, 8, 9, 10, 12) if x != c])
    n = r.choice([3, 4, 5, 6, 8, 10])
    v = r4((1 + y / 100) ** (-n))
    return Fv, c, y, n, v


def c11s1_price(r):
    Fv, c, y, n, v = _bond(r)
    C = Fv * c / 100
    P = C * (1 - v) / (y / 100) + Fv * v
    kind = 'discount' if y > c else 'premium'
    return Q(f'A bond of face value {inr(Fv)} pays an annual coupon at {c}% and is redeemable at par after {n} years. Find its price if the yield is {y}% per annum. (Use (1.{y:02d})^(−{n}) = {v}.)'.replace('(1.10)', '(1.1)').replace('(1.12)', '(1.12)'),
             f'{money(P)} (at a {kind})',
             f'Coupon C = {money(C)} (1 mark); P = C[1 − (1 + i)⁻ⁿ]/i + F(1 + i)⁻ⁿ (2 marks) = {money(C * (1 - v) / (y / 100))} + {money(Fv * v)} = {money(P)} (2 marks).',
             dist3(f'{money(P)} (at a {kind})', [f'{money(C * n + Fv)} (at a premium)', f'{money(Fv * v)} (at a discount)', f'{money(C * (1 - v) / (y / 100))} (at a discount)']))


def c11s1_coupon(r):
    Fv = r.choice([500, 1000, 2000, 5000, 10000])
    c = r.choice([4, 5, 6, 7.5, 8, 9, 10, 12])
    m = r.choice([1, 2])
    C = Fv * c / 100 / m
    return Q(f'A bond with face value {inr(Fv)} has a coupon rate of {num(c)}% per annum paid {"annually" if m == 1 else "semi-annually"}. Find the coupon payment each period.', money(C),
             f'Coupon = {num(c)}% of {Fv}' + (' ÷ 2' if m == 2 else '') + f' = {money(C)}.', dist3(money(C), [money(Fv * c / 100 * (2 if m == 1 else 1) / 2 if m == 2 else Fv * c / 200), money(Fv * c), money(C * 2 if m == 2 else C / 2)]))


def c11s1_zero(r):
    Fv = r.choice([1000, 5000, 10000, 50000, 100000])
    y = r.choice([5, 6, 8, 10, 12])
    n = r.choice([2, 3, 4, 5, 6])
    v = r4((1 + y / 100) ** (-n))
    P = Fv * v
    return Q(f'Find the price of a zero-coupon bond of face value {inr(Fv)} maturing in {n} years if the yield is {y}% per annum. (Use (1.{y:02d})^(−{n}) = {v}.)'.replace('(1.10)', '(1.1)'), money(P),
             f'P = F(1 + i)⁻ⁿ = {Fv} × {v} = {money(P)}.', dist3(money(P), [money(Fv * (1 - n * y / 100)), money(Fv / (1 + y / 100)), money(Fv * (1 + y / 100) ** n)]))


def c11s1_ar(r):
    return arbank([
        ('A bond with coupon rate 8% sells at a premium when the yield is 6%.', 'When the yield is below the coupon rate, the coupons are worth more than market interest.', 'a', 'Price > face value.'),
        ('A bond always sells at its face value.', 'The price is the present value of coupons and redemption value at the market yield.', 'd', 'Price equals face value only when yield = coupon rate; A false, R true.'),
        ('Bond prices fall when market interest rates rise.', 'Future payments are discounted at a higher rate.', 'a', 'Inverse relation.'),
    ])(r)


def c11s1_case(r):
    Fv, c, y, n, v = _bond(r)
    C = Fv * c / 100
    P = C * (1 - v) / (y / 100) + Fv * v
    who = name(r)
    return Q((f'{who} considers a {n}-year bond of face value {inr(Fv)} with a {c}% annual coupon, redeemable at par, when the market yield is {y}% p.a. (Use (1.{y:02d})^(−{n}) = {v}.) '
              f'(i) Find the annual coupon. (ii) Will the bond sell at a premium or a discount? Why? (iii) Find its fair price.').replace('(1.10)', '(1.1)'),
             f'(i) {money(C)} (ii) {"discount" if y > c else "premium"}: yield {"above" if y > c else "below"} the coupon rate (iii) {money(P)}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ======================================================================= ch11 st2 EMI

c11s2_mcq = mcqbank([
    ('EMI stands for …', 'equated monthly instalment', ['equal market interest', 'estimated monthly income', 'effective monthly interest'], 'Terminology.'),
    ('Under the flat-rate method, interest is charged on …', 'the original principal for the whole term', ['the outstanding balance each month', 'the EMI', 'the interest of the previous month'], 'Flat rate.'),
    ('Under the reducing-balance method, interest each month is charged on …', 'the outstanding principal', ['the original principal', 'the EMI amount', 'the total interest'], 'Reducing balance.'),
    ('By the reducing-balance method, EMI = …', 'Pi(1 + i)ⁿ/((1 + i)ⁿ − 1)', ['P(1 + i)ⁿ/n', 'Pin', '(P + Pin)/n'], 'Present value of an annuity.'),
    ('As the EMIs of a reducing-balance loan are paid, the interest part of each EMI …', 'decreases', ['increases', 'stays the same', 'becomes the whole EMI'], 'Outstanding balance falls.'),
])


def c11s2_flat(r):
    P = r.choice(range(50000, 2000001, 10000))
    rate = r.choice([6, 8, 9, 10, 12, 15])
    yrs = r.choice([1, 2, 3, 4, 5])
    I = P * rate * yrs / 100
    emi = (P + I) / (12 * yrs)
    return Q(f'A loan of {inr(P)} is taken at a flat interest rate of {rate}% per annum for {yrs} year{"s" if yrs > 1 else ""}. Find the EMI.', money(emi),
             f'Interest = P × r × t = {P} × {rate / 100} × {yrs} = {money(I)} (1 mark); EMI = (P + I)/(12 × {yrs}) = {money(emi)} (2 marks).',
             dist3(money(emi), [money(P / (12 * yrs)), money(I / (12 * yrs)), money((P + I) / yrs)]))


def c11s2_reduce(r):
    P = r.choice(range(100000, 5000001, 50000))
    rate = r.choice([6, 9, 12, 18])
    n = r.choice([12, 24, 36, 60])
    i = rate / 1200
    f = r4((1 + i) ** n)
    emi = P * i * f / (f - 1)
    return Q(f'Find the EMI for a loan of {inr(P)} at {rate}% per annum compounded monthly for {n} months, by the reducing-balance method. (Use (1 + {num(i, 4)})^{n} = {f}.)', money(emi),
             f'i = {rate}/1200 = {num(i, 4)} (1 mark); EMI = Pi(1 + i)ⁿ/((1 + i)ⁿ − 1) = {P} × {num(i, 4)} × {f}/({f} − 1) (2 marks) = {money(emi)} (2 marks).',
             dist3(money(emi), [money(P * (1 + rate * n / 1200) / n), money(P / n), money(P * i / (f - 1))]))


def c11s2_split(r):
    P = r.choice(range(100000, 3000001, 50000))
    rate = r.choice([6, 9, 12])
    n = r.choice([12, 24, 36])
    i = rate / 1200
    f = (1 + i) ** n
    emi = round(P * i * f / (f - 1), 2)
    I1 = round(P * i, 2)
    pr1 = round(emi - I1, 2)
    return Q(f'A loan of {inr(P)} at {rate}% p.a. (compounded monthly) is repaid by {n} EMIs of {money(emi)}. Find the interest and principal parts of the first EMI.', f'interest {money(I1)}, principal {money(pr1)}',
             f'Interest = P × i = {P} × {num(i, 4)} = {money(I1)} (2 marks); principal = EMI − interest = {money(pr1)} (1 mark).',
             dist3(f'interest {money(I1)}, principal {money(pr1)}', [f'interest {money(pr1)}, principal {money(I1)}', f'interest {money(P * rate / 100)}, principal {money(emi - P * rate / 100) if emi > P * rate / 100 else money(emi)}', f'interest {money(emi * i)}, principal {money(emi - emi * i)}']))


def c11s2_ar(r):
    return arbank([
        ('For the same rate and term, the flat-rate method costs the borrower more interest than the reducing-balance method.', 'Under the flat rate, interest is charged on the full principal even after part is repaid.', 'a', 'Higher effective rate.'),
        ('In a reducing-balance loan, every EMI contains the same amount of interest.', 'The interest part depends on the outstanding principal, which falls over time.', 'd', 'Interest part falls; A false, R true.'),
        ('A longer loan term reduces the EMI but increases the total interest paid.', 'The principal is spread over more instalments that each carry interest.', 'a', 'Trade-off.'),
    ])(r)


def c11s2_case(r):
    P = r.choice(range(300000, 1500001, 50000))
    rate = r.choice([8, 10, 12])
    yrs = r.choice([2, 3])
    I = P * rate * yrs / 100
    i = rate / 1200
    n = 12 * yrs
    f = r4((1 + i) ** n)
    emi_r = P * i * f / (f - 1)
    who = name(r)
    return Q((f'{who} needs a car loan of {inr(P)} for {yrs} years at {rate}% p.a. Dealer X offers a flat rate; bank Y uses the reducing-balance method (monthly compounding). (Use (1 + {num(i, 6)})^{n} = {f}.) '
              f'(i) Find the EMI with X. (ii) Find the EMI with Y. (iii) Which is cheaper, and by how much in total?'),
             f'(i) {money((P + I) / n)} (ii) {money(emi_r)} (iii) Y, by about {money(P + I - n * round(emi_r, 2))}', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= ch11 st3 rate of return; nominal and effective rates

c11s3_mcq = mcqbank([
    ('Rate of return on an investment = …', '(gain + income)/initial value × 100%', ['final value/initial value', 'income/final value × 100%', 'gain × initial value'], 'Definition.'),
    ('The nominal rate of interest is …', 'the stated annual rate before allowing for compounding frequency', ['the rate after compounding', 'the inflation rate', 'the rate per month'], 'Definition.'),
    ('The effective rate for nominal rate r compounded m times a year is …', '(1 + r/m)ᵐ − 1', ['r/m', 'mr', '(1 + r)ᵐ − 1'], 'Formula.'),
    ('The effective rate is greater than the nominal rate when …', 'interest is compounded more than once a year', ['interest is simple', 'the rate is zero', 'compounding is annual'], 'Compounding effect.'),
    ('The real rate of return is approximately …', 'nominal rate − inflation rate', ['nominal rate + inflation rate', 'inflation rate', 'nominal rate × inflation rate'], 'Fisher approximation.'),
])


def c11s3_ror(r):
    P0 = r.choice(range(10000, 500001, 5000))
    g = r.choice([-10, -5, 5, 8, 10, 12, 15, 20, 25])
    P1 = P0 * (100 + g) // 100
    inc = r.choice([0, 500, 1000, 2000, 5000])
    ror = (P1 - P0 + inc) / P0 * 100
    who = name(r)
    return Q(f'{who} bought shares for {inr(P0)}, received dividends of {inr(inc)} during the year and sold the shares for {inr(P1)} at the end of the year. Find the rate of return.', f'{num(ror, 2)}%',
             f'ROR = (P₁ − P₀ + income)/P₀ × 100 = ({P1} − {P0} + {inc})/{P0} × 100 = {num(ror, 2)}%.'.replace(' + 0)', ')'),
             dist3(f'{num(ror, 2)}%', [f'{num((P1 - P0) / P0 * 100, 2)}%', f'{num((P1 - P0 + inc) / P1 * 100, 2)}%', f'{num(inc / P0 * 100, 2)}%']))


def c11s3_eff(r):
    rate = r.choice([6, 8, 10, 12, 16, 20])
    m = r.choice([2, 4, 12])
    eff = ((1 + rate / 100 / m) ** m - 1) * 100
    how = {2: 'semi-annually', 4: 'quarterly', 12: 'monthly'}[m]
    f = r4((1 + rate / 100 / m) ** m)
    return Q(f'Find the effective rate of interest equivalent to a nominal rate of {rate}% per annum compounded {how}. (Use (1 + {num(rate / 100 / m, 4)})^{m} = {f}.)', f'{num((f - 1) * 100, 2)}%',
             f'Effective rate = (1 + r/m)ᵐ − 1 = {f} − 1 = {num(f - 1, 4)} = {num((f - 1) * 100, 2)}%.', dist3(f'{num((f - 1) * 100, 2)}%', [f'{rate}%', f'{num(rate / m, 2)}%', f'{num(rate * m, 2)}%']))


def c11s3_real(r):
    nom = r.choice([6, 7, 8, 9, 10, 12])
    inf = r.choice([3, 4, 5, 6])
    if inf >= nom:
        raise ValueError
    exact = ((1 + nom / 100) / (1 + inf / 100) - 1) * 100
    return Q(f'An investment earns a nominal return of {nom}% when inflation is {inf}%. Find the real rate of return (exact and approximate).', f'{num(exact, 2)}% (approximately {nom - inf}%)',
             f'Real rate = (1 + n)/(1 + inflation) − 1 = {1 + nom / 100}/{1 + inf / 100} − 1 = {num(exact, 2)}% (2 marks); approximation n − inflation = {nom - inf}% (1 mark).',
             dist3(f'{num(exact, 2)}% (approximately {nom - inf}%)', [f'{nom + inf}% (approximately {nom + inf}%)', f'{num(nom / inf, 2)}% (approximately {nom - inf}%)', f'{nom}% (approximately {nom}%)']))


def c11s3_ar(r):
    return arbank([
        ('A nominal rate of 12% compounded monthly gives an effective rate above 12%.', 'Interest is earned on interest within the year.', 'a', '(1.01)¹² − 1 ≈ 12.68%.'),
        ('If inflation exceeds the nominal return, the real return is positive.', 'Real return ≈ nominal return − inflation.', 'd', 'It is negative; A false, R true.'),
        ('The rate of return includes both capital gain and income received.', 'ROR = (gain + income)/initial value.', 'a', 'Definition.'),
    ])(r)


def c11s3_case(r):
    P0 = r.choice(range(20000, 200001, 10000))
    P1 = P0 * r.choice([105, 108, 110, 112, 115, 120]) // 100
    inc = r.choice([1000, 1500, 2000, 2500])
    inf = r.choice([4, 5, 6])
    ror = (P1 - P0 + inc) / P0 * 100
    who = name(r)
    return Q((f'{who} invested {inr(P0)} in a mutual fund in {r.choice(CITIES)}. After a year the units were worth {inr(P1)} and {inr(inc)} was received as dividend. Inflation was {inf}%. '
              f'(i) Find the capital gain. (ii) Find the rate of return. (iii) Find the approximate real rate of return.'),
             f'(i) {inr(P1 - P0)} (ii) {num(ror, 2)}% (iii) {num(ror - inf, 2)}%', '(i) 1 mark (ii) 2 marks (iii) 1 mark.')


# ======================================================================= ch11 st4 CAGR

CAGR_T = [(Fr(121, 100), 2, 10), (Fr(1331, 1000), 3, 10), (Fr(14641, 10000), 4, 10), (Fr(144, 100), 2, 20), (Fr(1728, 1000), 3, 20), (Fr(169, 100), 2, 30),
          (Fr(2197, 1000), 3, 30), (Fr(11025, 10000), 2, 5), (Fr(115762, 100000), 3, 5), (Fr(11664, 10000), 2, 8), (Fr(125, 100), 2, None), (Fr(2), 5, None), (Fr(15), 1, None)]


def c11s4_cagr(r):
    k = r.choice([0, 1, 2, 3, 4, 5, 6, 7, 9])
    ratio, n, g = CAGR_T[k]
    P0 = r.randint(2, 60) * max(ratio.denominator, 10000)
    P1 = P0 * ratio
    if P1.denominator != 1:
        raise ValueError
    what = r.choice(['the value of an investment', 'a company\'s revenue', 'the sales of a start-up', 'the price of a plot'])
    return Q(f'{what.capitalize()} grew from {inr(P0)} to {inr(int(P1))} in {n} years. Find the compound annual growth rate (CAGR).', f'{g}%',
             f'CAGR = (FV/PV)^(1/n) − 1 = ({fz(ratio)})^(1/{n}) − 1 = {fz(Fr(100 + g, 100))} − 1 = {g}% (3 marks).',
             dist3(f'{g}%', [f'{num(float((ratio - 1) * 100 / n), 2)}%', f'{num(float((ratio - 1) * 100), 2)}%', f'{g + 1}%']))


def c11s4_fv(r):
    P0 = r.choice(range(10000, 1000001, 10000))
    g = r.choice([5, 8, 10, 12, 15, 20])
    n = r.choice([2, 3, 4, 5])
    f = r4((1 + g / 100) ** n)
    return Q(f'An investment of {inr(P0)} grows at a CAGR of {g}%. Estimate its value after {n} years. (Use (1.{g:02d})^{n} = {f}.)'.replace('(1.10)', '(1.1)').replace('(1.20)', '(1.2)'), money(P0 * f),
             f'FV = PV(1 + CAGR)ⁿ = {P0} × {f} = {money(P0 * f)}.', dist3(money(P0 * f), [money(P0 * (1 + g * n / 100)), money(P0 * (1 + g / 100)), money(P0 * f - P0)]))


def c11s4_mcq(r):
    return mcqbank([
        ('CAGR = …', '(FV/PV)^(1/n) − 1', ['(FV − PV)/(n × PV)', 'FV/PV − 1', '(FV/PV)ⁿ − 1'], 'Definition.'),
        ('CAGR measures …', 'the constant yearly rate that would take the beginning value to the ending value', ['the average of yearly returns', 'the total return', 'the inflation rate'], 'Interpretation.'),
        ('An investment doubles in 1 year. Its CAGR is …', '100%', ['50%', '200%', '10%'], '(2)¹ − 1.'),
        ('Compared with the simple average annual growth, CAGR is …', 'less than or equal to it', ['always greater', 'unrelated', 'always double'], 'Compounding smooths growth.'),
    ])(r)


def c11s4_ar(r):
    return arbank([
        ('An investment that grows from ₹10,000 to ₹12,100 in 2 years has a CAGR of 10%.', '(1.1)² = 1.21.', 'a', 'CAGR = √1.21 − 1.'),
        ('An investment that grows from ₹100 to ₹144 in 2 years has a CAGR of 22%.', 'CAGR = (FV/PV)^(1/n) − 1.', 'd', '√1.44 − 1 = 20%; A false, R true.'),
        ('CAGR ignores the ups and downs of individual years.', 'It uses only the beginning value, ending value and number of years.', 'a', 'Smoothed rate.'),
    ])(r)


def c11s4_case(r):
    k = r.choice([0, 1, 3, 5])
    ratio, n, g = CAGR_T[k]
    P0 = r.choice(range(10, 201, 5)) * 100000
    P1 = P0 * ratio
    if P1.denominator != 1:
        raise ValueError
    who = name(r)
    f2 = r4((1 + g / 100) ** 2)
    return Q((f'{who}\'s family business in {r.choice(CITIES)} had revenue {inr(P0)} in 2021 and {inr(int(P1))} in {2021 + n}. '
              f'(i) Find the CAGR. (ii) Find the simple average annual growth rate. (iii) If the CAGR continues, estimate the revenue two years later. (Use (1 + {g / 100})² = {f2}.)'),
             f'(i) {g}% (ii) {num(float((ratio - 1) * 100 / n), 2)}% (iii) {money(float(P1) * f2)}', '(i) 2 marks (ii) 1 mark (iii) 1 mark.')


# ======================================================================= ch12 depreciation

c12s1_mcq = mcqbank([
    ('Depreciation is …', 'the decrease in the value of an asset due to use, wear and tear or obsolescence', ['the increase in the value of an asset', 'the interest on a loan', 'the cost of repairs only'], 'Definition.'),
    ('Scrap (salvage) value is …', 'the estimated value of an asset at the end of its useful life', ['the purchase price', 'the annual depreciation', 'the book value in year 1'], 'Definition.'),
    ('Useful life of an asset is …', 'the period over which it is expected to be used', ['the time since manufacture', 'the guarantee period only', 'the loan period'], 'Definition.'),
    ('Book value of an asset at any time is …', 'cost − accumulated depreciation', ['cost + depreciation', 'scrap value only', 'market price'], 'Definition.'),
    ('Which is a cause of depreciation?', 'obsolescence', ['inflation in prices', 'increase in demand', 'rise in market value'], 'Causes: wear and tear, obsolescence, passage of time, depletion.'),
    ('The cost of an asset for depreciation includes …', 'purchase price plus installation and transport charges', ['purchase price only', 'scrap value only', 'annual repairs'], 'Original cost.'),
])

ASSETS = ['machine', 'delivery van', 'computer system', 'printing press', 'generator', 'photocopier', 'tractor', 'air conditioner']


def _asset(r):
    while True:
        C = r.choice(range(20000, 2000001, 5000))
        n = r.choice([4, 5, 6, 8, 10, 12, 15])
        Sv = r.choice(range(0, C // 4 + 1, 1000))
        D = Fr(C - Sv, n)
        if D.denominator == 1:
            return C, n, Sv, int(D)


def c12s2_dep(r):
    C, n, Sv, D = _asset(r)
    a = r.choice(ASSETS)
    rate = Fr(D * 100, C)
    return Q(f'A {a} costs {inr(C)}, has a useful life of {n} years and a scrap value of {inr(Sv)}. Find the annual depreciation and the rate of depreciation by the straight-line method.', f'{inr(D)} per year; {num(float(rate), 2)}%',
             f'D = (C − S)/n = ({C} − {Sv})/{n} = {D} (2 marks); rate = D/C × 100 = {num(float(rate), 2)}% (1 mark).',
             dist3(f'{inr(D)} per year; {num(float(rate), 2)}%', [f'{inr(C // n)} per year; {num(100 / n, 2)}%', f'{inr(D)} per year; {num(float(Fr(D * 100, C - Sv)), 2)}%', f'{inr((C + Sv) // n)} per year; {num(float(Fr((C + Sv) * 100, n * C)), 2)}%']))


def c12s2_scrap(r):
    C, n, Sv, D = _asset(r)
    k = r.randint(0, 2)
    a = r.choice(ASSETS)
    if k == 0:
        return Q(f'A {a} bought for {inr(C)} is depreciated by the straight-line method at {inr(D)} per year over {n} years. Find its scrap value.', inr(Sv),
                 f'S = C − nD = {C} − {n} × {D} = {Sv}.', dist3(inr(Sv), [inr(C - (n - 1) * D), inr(C - D), inr(n * D)]))
    if k == 1:
        return Q(f'A {a} costs {inr(C)} and has a scrap value of {inr(Sv)}. If the annual depreciation (straight-line) is {inr(D)}, find its useful life.', f'{n} years',
                 f'n = (C − S)/D = {C - Sv}/{D} = {n}.', dist3(f'{n} years', [f'{n + 1} years', f'{C // D} years' if C // D != n else f'{n + 2} years', f'{n - 1} years']))
    inst = r.choice(range(1000, 30001, 1000))
    D2 = Fr(C + inst - Sv, n)
    return Q(f'A {a} is bought for {inr(C)} and {inr(inst)} is spent on its transport and installation. Its useful life is {n} years with scrap value {inr(Sv)}. Find the annual straight-line depreciation.', rs(D2),
             f'Cost = {C} + {inst} = {C + inst} (1 mark); D = ({C + inst} − {Sv})/{n} = {rs(D2)} (2 marks).', dist3(rs(D2), [inr(D), rs(Fr(C + inst, n)), rs(Fr(C - Sv - inst, n))]))


def c12s3_book(r):
    C, n, Sv, D = _asset(r)
    t = r.randint(1, n - 1)
    bv = C - t * D
    a = r.choice(ASSETS)
    return Q(f'A {a} costing {inr(C)} has a useful life of {n} years and scrap value {inr(Sv)}. Find its book value at the end of {t} year{"s" if t > 1 else ""} under the straight-line method.', inr(bv),
             f'D = ({C} − {Sv})/{n} = {D} (1 mark); BV = C − tD = {C} − {t} × {D} = {bv} (2 marks).', dist3(inr(bv), [inr(C - (t + 1) * D), inr(t * D), inr(bv - Sv)]))


def c12s3_schedule(r):
    while True:
        C, n, Sv, D = _asset(r)
        if n <= 6:
            break
    a = r.choice(ASSETS)
    rows = '; '.join(f'year {t}: depreciation {inr(D)}, accumulated {inr(t * D)}, book value {inr(C - t * D)}' for t in range(1, n + 1))
    return Q(f'Prepare a depreciation schedule (straight-line method) for a {a} costing {inr(C)} with a useful life of {n} years and scrap value {inr(Sv)}.', rows,
             f'Annual depreciation ({C} − {Sv})/{n} = {D} (1 mark); accumulated depreciation and book value each year (3 marks); final book value equals scrap value {inr(Sv)} (1 mark).')


def c12s3_sale(r):
    C, n, Sv, D = _asset(r)
    t = r.randint(2, n - 1)
    bv = C - t * D
    sp = bv + r.choice([-1, 1]) * r.choice(range(1000, max(2000, bv // 4), 1000))
    if sp <= 0:
        raise ValueError
    res = f'profit {inr(sp - bv)}' if sp > bv else f'loss {inr(bv - sp)}'
    a = r.choice(ASSETS)
    return Q(f'A {a} bought for {inr(C)} (life {n} years, scrap {inr(Sv)}) is depreciated by the straight-line method and sold at the end of {t} years for {inr(sp)}. Find the profit or loss on sale.', res,
             f'D = {D} (1 mark); BV after {t} years = {bv} (1 mark); compare with {sp}: {res} (1 mark).', dist3(res, [f'{"loss" if sp > bv else "profit"} {inr(abs(sp - bv))}', f'profit {inr(abs(sp - C))}' if sp != C else 'profit ₹0', f'loss {inr(abs(C - t * D - Sv - sp)) if C - t * D - Sv != sp else "₹1"}']))


def c12s1_explain(r):
    return xbank([
        ('State two causes of depreciation.', 'Wear and tear from use; obsolescence (also passage of time, depletion).', 'Any two causes (2 marks).'),
        ('Why is depreciation charged even when an asset is not used?', 'Value falls with the passage of time and obsolescence.', 'Time and obsolescence (2 marks).'),
        ('Distinguish between book value and scrap value.', 'Book value: cost − accumulated depreciation at a date; scrap value: estimated value at the end of useful life.', 'Both definitions (2 marks).'),
        ('Give one advantage and one limitation of the straight-line method.', 'Advantage: simple, equal charge each year; limitation: ignores higher wear and repairs in later years.', '1 mark each.'),
    ])(r)


def c12s1_num(r):
    C, n, Sv, D = _asset(r)
    t = r.randint(1, n - 1)
    a = r.choice(ASSETS)
    return Q(f'A {a} costing {inr(C)} has accumulated depreciation of {inr(t * D)} after {t} years. Find its book value.', inr(C - t * D), 'Book value = cost − accumulated depreciation.',
             dist3(inr(C - t * D), [inr(C + t * D), inr(t * D), inr(C - D)]))


def c12s_ar(r):
    C, n, Sv, D = _asset(r)
    return arbank([
        (f'Under the straight-line method, a {r.choice(ASSETS)} costing {inr(C)} with life {n} years and scrap {inr(Sv)} is depreciated by {inr(D)} every year.', 'The straight-line method charges equal depreciation (C − S)/n each year.', 'a', 'Equal annual charge.'),
        ('Under the straight-line method, the book value falls by a larger amount every year.', 'The annual depreciation is the same every year.', 'd', 'It falls by the same amount; A false, R true.'),
        ('At the end of its useful life, the book value of an asset equals its scrap value.', 'Total depreciation over the life is C − S.', 'a', 'C − (C − S) = S.'),
        ('Installation charges are not part of the cost of an asset for depreciation.', 'All costs to bring the asset into use are capitalised.', 'd', 'They are added to the cost; A false, R true.'),
    ])(r)


def c12s2_case(r):
    C, n, Sv, D = _asset(r)
    t = r.randint(2, n - 1)
    who = name(r)
    a = r.choice(ASSETS)
    return Q((f'{who}\'s firm in {r.choice(CITIES)} buys a {a} for {inr(C)}; its useful life is {n} years and scrap value {inr(Sv)}. '
              f'(i) Find the annual depreciation (straight-line). (ii) Find the rate of depreciation. (iii) Find the book value after {t} years.'),
             f'(i) {inr(D)} (ii) {num(D * 100 / C, 2)}% (iii) {inr(C - t * D)}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


def c12s3_case(r):
    C, n, Sv, D = _asset(r)
    t = r.randint(2, n - 1)
    bv = C - t * D
    sp = bv - r.choice(range(1000, max(2000, bv // 5), 1000))
    if sp <= 0:
        raise ValueError
    who = name(r)
    a = r.choice(ASSETS)
    return Q((f'A {a} bought by {who}\'s company for {inr(C)} (life {n} years, scrap {inr(Sv)}) is depreciated by the straight-line method. (i) Find the depreciation per year. '
              f'(ii) Find the accumulated depreciation and book value after {t} years. (iii) If it is sold then for {inr(sp)}, find the profit or loss.'),
             f'(i) {inr(D)} (ii) {inr(t * D)}; {inr(bv)} (iii) loss {inr(bv - sp)}', '(i) 1 mark (ii) 1 mark (iii) 2 marks.')


# ======================================================================= table

FAMILIES = {
    S + '07-st1': [F('C1', 'D2', 'mcq', c7s1_mcq), F('C1', 'D1', 'short', c7s1_mean), F('C2', 'D2', 'numerical', c7s1_mean), F('C2', 'D3', 'mcq', c7s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s1_coins), F('C3', 'D3', 'multi_step', c7s1_k), F('C3', 'D4', 'long', c7s1_draw), F('C4', 'D3', 'case', c7s1_case),
                   F('C4', 'D4', 'multi_step', c7s1_game), F('C4', 'D5', 'long', c7s1_draw), F('C3', 'D1', 'numerical', c7s1_k)],
    S + '07-st2': [F('C1', 'D2', 'mcq', c7s2_mcq), F('C1', 'D1', 'short', c7s2_mv), F('C2', 'D2', 'numerical', c7s2_prob), F('C2', 'D3', 'mcq', c7s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s2_mv), F('C3', 'D3', 'multi_step', c7s2_word), F('C4', 'D3', 'case', c7s2_case), F('C4', 'D4', 'multi_step', c7s2_word),
                   F('C3', 'D1', 'numerical', c7s2_prob), F('C4', 'D5', 'long', c7s2_word, marks=5)],
    S + '07-st3': [F('C1', 'D2', 'mcq', c7s3_mcq), F('C1', 'D1', 'short', c7s3_prob), F('C2', 'D2', 'numerical', c7s3_prob), F('C2', 'D3', 'mcq', c7s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s3_approx), F('C3', 'D3', 'multi_step', c7s3_approx), F('C4', 'D3', 'case', c7s3_case), F('C4', 'D4', 'numerical', c7s3_param),
                   F('C3', 'D1', 'numerical', c7s3_prob)],
    S + '07-st4': [F('C1', 'D2', 'mcq', c7s4_mcq), F('C1', 'D1', 'short', c7s4_z), F('C2', 'D2', 'numerical', c7s4_z), F('C2', 'D3', 'mcq', c7s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c7s4_z), F('C3', 'D3', 'multi_step', c7s4_count), F('C3', 'D4', 'multi_step', c7s4_count), F('C4', 'D3', 'case', c7s4_case),
                   F('C4', 'D4', 'multi_step', c7s4_z), F('C4', 'D5', 'long', c7s4_count, marks=5), F('C3', 'D1', 'numerical', c7s4_z)],
    S + '08-st1': [F('C1', 'D2', 'mcq', c8s1_mcq), F('C1', 'D1', 'mcq', c8s1_ident), F('C2', 'D2', 'explain', c8s1_explain), F('C2', 'D3', 'mcq', c8s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s1_sys), F('C3', 'D3', 'multi_step', c8s1_strat), F('C4', 'D3', 'case', c8s1_case), F('C3', 'D1', 'numerical', c8s1_sys), F('C2', 'D2', 'mcq', c8s1_ident)],
    S + '08-st2': [F('C1', 'D2', 'mcq', c8s2_mcq), F('C1', 'D1', 'short', c8s2_se), F('C2', 'D2', 'numerical', c8s2_se), F('C2', 'D3', 'mcq', c8s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s2_n), F('C3', 'D3', 'multi_step', c8s2_prob), F('C4', 'D3', 'case', c8s2_case), F('C3', 'D1', 'numerical', c8s2_se)],
    S + '08-st3': [F('C1', 'D2', 'mcq', c8s3_mcq), F('C1', 'D1', 'short', c8s3_hyp), F('C2', 'D2', 'explain', c8s3_explain), F('C2', 'D3', 'mcq', c8s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s3_hyp), F('C3', 'D3', 'multi_step', c8s3_z), F('C3', 'D4', 'multi_step', c8s3_z), F('C4', 'D3', 'case', c8s3_case),
                   F('C4', 'D4', 'long', c8s3_z, marks=5), F('C3', 'D1', 'numerical', c8s3_hyp), F('C2', 'D2', 'numerical', c8s3_hyp)],
    S + '08-st4': [F('C1', 'D2', 'mcq', c8s4_mcq), F('C1', 'D1', 'short', c8s4_tstat), F('C2', 'D2', 'numerical', c8s4_tstat), F('C2', 'D3', 'mcq', c8s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c8s4_tstat), F('C3', 'D3', 'long', c8s4_one), F('C3', 'D4', 'long', c8s4_one), F('C4', 'D3', 'case', c8s4_case),
                   F('C4', 'D4', 'long', c8s4_two), F('C4', 'D5', 'long', c8s4_two), F('C3', 'D1', 'numerical', c8s4_tstat)],
    S + '09-st1': [F('C1', 'D2', 'mcq', c9s1_mcq), F('C1', 'D1', 'mcq', c9s1_ident), F('C2', 'D2', 'explain', c9s1_explain), F('C2', 'D3', 'mcq', c9s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'mcq', c9s1_ident), F('C3', 'D3', 'explain', c9s1_explain), F('C4', 'D3', 'case', c9s1_case), F('C2', 'D2', 'mcq', c9s1_ident)],
    S + '09-st2': [F('C1', 'D2', 'mcq', c9s2_mcq), F('C1', 'D1', 'short', c9s2_one), F('C2', 'D2', 'numerical', c9s2_one), F('C2', 'D3', 'mcq', c9s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c9s2_three), F('C3', 'D3', 'multi_step', c9s2_three), F('C3', 'D4', 'long', c9s2_four), F('C4', 'D3', 'case', c9s2_case),
                   F('C4', 'D4', 'long', c9s2_four), F('C4', 'D5', 'long', c9s2_four), F('C3', 'D1', 'numerical', c9s2_one)],
    S + '09-st3': [F('C1', 'D2', 'mcq', c9s3_mcq), F('C1', 'D1', 'short', c9s3_pred), F('C2', 'D2', 'numerical', c9s3_pred), F('C2', 'D3', 'mcq', c9s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c9s3_pred), F('C3', 'D3', 'multi_step', c9s3_trendvals), F('C3', 'D4', 'long', c9s3_fit), F('C4', 'D3', 'case', c9s3_case),
                   F('C4', 'D4', 'long', c9s3_fit), F('C4', 'D5', 'long', c9s3_fit), F('C3', 'D1', 'numerical', c9s3_pred)],
    S + '10-st1': [F('C1', 'D2', 'mcq', c10s1_mcq), F('C1', 'D1', 'short', c10s1_pv), F('C2', 'D2', 'numerical', c10s1_find), F('C2', 'D3', 'mcq', c10s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s1_pv), F('C3', 'D3', 'multi_step', c10s1_grow), F('C3', 'D4', 'long', c10s1_defer), F('C4', 'D3', 'case', c10s1_case),
                   F('C4', 'D4', 'long', c10s1_defer), F('C4', 'D5', 'multi_step', c10s1_grow), F('C3', 'D1', 'numerical', c10s1_find)],
    S + '10-st2': [F('C1', 'D2', 'mcq', c10s2_mcq), F('C1', 'D1', 'short', c10s2_amt), F('C2', 'D2', 'numerical', c10s2_amt), F('C2', 'D3', 'mcq', c10s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c10s2_dep), F('C3', 'D3', 'multi_step', c10s2_dep), F('C3', 'D4', 'long', c10s2_machine), F('C4', 'D3', 'case', c10s2_case),
                   F('C4', 'D4', 'long', c10s2_machine), F('C4', 'D5', 'long', c10s2_machine), F('C3', 'D1', 'numerical', c10s2_dep)],
    S + '10-st3': [F('C1', 'D2', 'mcq', c10s3_mcq), F('C2', 'D2', 'numerical', c10s3_endow), F('C2', 'D3', 'mcq', c10s3_ar, kinds=('ar',)), F('C3', 'D2', 'numerical', c10s3_endow),
                   F('C3', 'D3', 'long', c10s3_compare), F('C4', 'D3', 'case', c10s3_case), F('C3', 'D1', 'numerical', c10s3_endow), F('C4', 'D4', 'long', c10s3_compare)],
    S + '11-st1': [F('C1', 'D2', 'mcq', c11s1_mcq), F('C1', 'D1', 'short', c11s1_coupon), F('C2', 'D2', 'numerical', c11s1_zero), F('C2', 'D3', 'mcq', c11s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s1_zero), F('C3', 'D3', 'long', c11s1_price), F('C3', 'D4', 'long', c11s1_price), F('C4', 'D3', 'case', c11s1_case),
                   F('C4', 'D4', 'long', c11s1_price), F('C4', 'D5', 'long', c11s1_price), F('C3', 'D1', 'numerical', c11s1_coupon)],
    S + '11-st2': [F('C1', 'D2', 'mcq', c11s2_mcq), F('C1', 'D1', 'short', c11s2_flat), F('C2', 'D2', 'numerical', c11s2_flat), F('C2', 'D3', 'mcq', c11s2_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s2_split), F('C3', 'D3', 'long', c11s2_reduce), F('C3', 'D4', 'long', c11s2_reduce), F('C4', 'D3', 'case', c11s2_case),
                   F('C4', 'D4', 'long', c11s2_reduce), F('C4', 'D5', 'multi_step', c11s2_split), F('C3', 'D1', 'numerical', c11s2_flat)],
    S + '11-st3': [F('C1', 'D2', 'mcq', c11s3_mcq), F('C1', 'D1', 'short', c11s3_ror), F('C2', 'D2', 'numerical', c11s3_ror), F('C2', 'D3', 'mcq', c11s3_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s3_eff), F('C3', 'D3', 'multi_step', c11s3_real), F('C4', 'D3', 'case', c11s3_case), F('C4', 'D4', 'multi_step', c11s3_eff),
                   F('C3', 'D1', 'numerical', c11s3_real)],
    S + '11-st4': [F('C1', 'D2', 'mcq', c11s4_mcq), F('C1', 'D1', 'short', c11s4_fv), F('C2', 'D2', 'numerical', c11s4_cagr), F('C2', 'D3', 'mcq', c11s4_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c11s4_fv), F('C3', 'D3', 'multi_step', c11s4_cagr), F('C4', 'D3', 'case', c11s4_case), F('C4', 'D4', 'multi_step', c11s4_cagr),
                   F('C3', 'D1', 'numerical', c11s4_cagr)],
    S + '12-st1': [F('C1', 'D2', 'mcq', c12s1_mcq), F('C1', 'D1', 'short', c12s1_num), F('C2', 'D2', 'explain', c12s1_explain), F('C2', 'D3', 'mcq', c12s_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s1_num), F('C3', 'D3', 'numerical', c12s2_dep), F('C4', 'D3', 'case', c12s2_case), F('C3', 'D1', 'numerical', c12s1_num)],
    S + '12-st2': [F('C1', 'D2', 'mcq', c12s1_mcq), F('C1', 'D1', 'short', c12s2_dep), F('C2', 'D2', 'numerical', c12s2_scrap), F('C2', 'D3', 'mcq', c12s_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s2_dep), F('C3', 'D3', 'multi_step', c12s2_scrap), F('C4', 'D3', 'case', c12s2_case), F('C4', 'D4', 'multi_step', c12s2_scrap),
                   F('C3', 'D1', 'numerical', c12s2_dep), F('C3', 'D4', 'multi_step', c12s2_scrap)],
    S + '12-st3': [F('C1', 'D2', 'mcq', c12s1_mcq), F('C1', 'D1', 'short', c12s3_book), F('C2', 'D2', 'numerical', c12s3_book), F('C2', 'D3', 'mcq', c12s_ar, kinds=('ar',)),
                   F('C3', 'D2', 'numerical', c12s3_book), F('C3', 'D3', 'multi_step', c12s3_sale), F('C3', 'D4', 'long', c12s3_schedule), F('C4', 'D3', 'case', c12s3_case),
                   F('C4', 'D4', 'long', c12s3_schedule), F('C4', 'D5', 'long', c12s3_sale, marks=5), F('C3', 'D1', 'numerical', c12s3_book)],
}
