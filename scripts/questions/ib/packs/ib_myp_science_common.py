"""Shared builders for the IB MYP Sciences packs (ib-g8-science, ib-g10-science).

inquiry(R, key, *investigations)  criterion B items (variables, research question, hypothesis, multi-part planning
                                   tasks, method design, evaluating a weak method, data-processing plan, risk assessment)
dataset(R, key, *contexts)         criterion C items (data tables with three trials: means, anomalies, % change,
                                   spread of repeats, trend + explanation, multi-part analysis) with computed answers
Both register templates with style 'inquiry' / 'data' so mock tasks can request them.
"""
from __future__ import annotations

import math
import re

from _common import F, Registry, T, fmt, mcq, name, num_distractors, two_names, CITIES  # noqa: F401

MARKBAND_D = ('MYP criterion D (0-8, scaled): 7-8 explains thoroughly how the science is applied to address the issue, discusses and '
              'evaluates the implications (moral, ethical, social, economic, political, cultural or environmental), and documents sources '
              'consistently; 5-6 explains and discusses; 3-4 outlines; 1-2 states.')


def g(x, sf=3):
    if x == 0:
        return '0'
    s = f'{x:.{sf}g}'
    return fmt(x, sf) if 'e' in s else s


def sci(x, sf=3):
    m_ = math.floor(math.log10(abs(x)))
    return f'{x / 10 ** m_:.{sf}g} × 10^{m_}'


SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def evx(R, key, *items):
    R.f[key].evaluate = list(R.f[key].evaluate) + list(items)


def exx(R, key, *items):
    R.f[key].extended = list(R.f[key].extended) + list(items)


def _lc(t):
    """Lower-case a table label for use mid-sentence, keeping acronyms and formulas (GM, CO₂, pH, DNA)."""
    return ' '.join(w if any(c.isupper() for c in w[1:]) or any(c.isdigit() or c in '₀₁₂₃₄₅₆₇₈₉' for c in w) else w.lower() for w in t.split(' '))


def _short(txt):
    t = re.split(r' – | \(| = |, |; | measured | read | from a | counted ', txt)[0].strip()
    return t[0].lower() + t[1:] if t[:2] != t[:2].upper() else t


def inquiry(R, key, *invs):
    """Each investigation: dict(ctx, iv, dv, cvs=[(variable, how/why)], hyp, method, weak=(weakness, improvement), safety).
    ctx is a phrase like 'how the temperature of the water affects ...'."""

    def inq(rng, slot):
        v = rng.choice(invs)
        who = name(rng)
        full = (slot.marks or 0) >= 5 or (slot.d >= 4 and rng.random() < 0.6)
        if full:
            c1, c2 = rng.sample(v['cvs'], 2)
            cvkey = '; '.join(f'{a} ({b})' for a, b in v['cvs'])
            frame = rng.randrange(3)
            if frame == 0:
                stem = (f'{who} is investigating {v["ctx"]}.\n(a) State the independent variable. [1]\n(b) State the dependent variable and how it will be measured. [1]\n'
                        f'(c) Identify two control variables and explain why each must be kept constant. [2]\n(d) Formulate a testable hypothesis and explain it using scientific reasoning. [2]')
                ans = f'(a) {v["iv"]}. (b) {v["dv"]}. (c) {c1[0]} – {c1[1]}; {c2[0]} – {c2[1]}. (d) {v["hyp"]}'
                key_ = (f'(a) 1: {v["iv"]}. (b) 1: {v["dv"]} (must include how/units). (c) 1 each, variable + reason: any two of {cvkey}. '
                        f'(d) 1 for a testable if/then prediction linking IV and DV, 1 for correct scientific reasoning: {v["hyp"]}')
            elif frame == 1:
                stem = (f'A class is planning an investigation into {v["ctx"]}.\n(a) Write a focused research question. [1]\n(b) Explain how the independent variable will be changed, giving a suitable range. [1]\n'
                        f'(c) Describe how the dependent variable will be measured and how many repeats are needed. [2]\n(d) Explain how {c1[0]} will be controlled and why. [1]\n(e) Identify one safety or ethical consideration. [1]')
                ans = (f'(a) How does {_short(v["iv"])} affect {_short(v["dv"])}? (b) {v["iv"]} – at least five values across a sensible range. '
                       f'(c) {v["dv"]}; at least three repeats and a mean. (d) {c1[0]} – {c1[1]}. (e) {v.get("safety", "appropriate safety precautions")}.')
                key_ = (f'(a) 1 names IV and DV. (b) 1 method of changing the IV with ≥5 values. (c) 1 measurement method with instrument/units; 1 ≥3 repeats and mean. '
                        f'(d) 1 how and why {c1[0]} is controlled ({c1[1]}). (e) 1 relevant point, e.g. {v.get("safety", "eye protection")}.')
            else:
                stem = (f'{who} predicts the outcome of an investigation into {v["ctx"]}.\n(a) Formulate a hypothesis that includes a scientific explanation. [2]\n'
                        f'(b) Identify the independent and dependent variables. [2]\n(c) State two variables that must be controlled. [1]\n(d) Sketch the shape of the graph you would expect if the hypothesis is correct and explain how it would support the hypothesis. [1]')
                ans = f'(a) {v["hyp"]} (b) IV: {v["iv"]}; DV: {v["dv"]}. (c) {c1[0]}; {c2[0]}. (d) A graph of the DV against the IV showing the predicted trend; if the data follow this trend within the spread of repeats, the hypothesis is supported.'
                key_ = (f'(a) 1 testable prediction; 1 scientific reasoning: {v["hyp"]} (b) 1 IV: {v["iv"]}; 1 DV: {v["dv"]}. (c) 1 any two of {cvkey}. (d) 1 graph shape consistent with the hypothesis, linked to support.')
            return dict(stem=stem, answer=ans, markingKey=key_, type='multi_step', marks=slot.marks or 6, gap='G4')
        kind = rng.choice(['iv', 'dv', 'cv', 'why', 'hyp', 'rq'])
        if kind == 'iv':
            return dict(stem=f'{who} is investigating {v["ctx"]}. Identify the independent variable in this investigation.', answer=v['iv'],
                        markingKey=f'1 mark: {v["iv"]} (the variable that is deliberately changed). The measured variable scores 0.', type='short', marks=1, gap='G4')
        if kind == 'dv':
            return dict(stem=f'In an investigation into {v["ctx"]}, state the dependent variable and describe how {who} should measure it.', answer=v['dv'],
                        markingKey=f'1 mark for naming the dependent variable, 1 mark for a valid measuring method/instrument with unit: {v["dv"]}.', type='short', marks=2, gap='G4')
        if kind == 'cv':
            return dict(stem=f'{who} plans to investigate {v["ctx"]}. State three variables that must be controlled to make this a fair test.',
                        answer='Any three of: ' + '; '.join(a for a, b in v['cvs']),
                        markingKey='1 mark each, max 3: ' + '; '.join(f'{a} – {b}' for a, b in v['cvs']) + '. The independent or dependent variable scores 0.', type='short', marks=3, gap='G4')
        if kind == 'why':
            c = rng.choice(v['cvs'])
            cvq = f'{c[0]} must be used in every trial' if c[0].startswith('the same ') else f'this control must be applied in the same way in every trial: {c[0]}'
            return dict(stem=f'In an investigation into {v["ctx"]}, explain why {cvq}.', answer=c[1],
                        markingKey=f'1 mark: a change in this variable ({c[0]}) would also affect the dependent variable; 1 mark for the specific reason: {c[1]}. Then only the independent variable is responsible for any change (validity).', type='explain', marks=2, gap='G4')
        if kind == 'rq':
            return dict(stem=f'{who} wants to find out {v["ctx"]}. Write a focused research question for this investigation that names both the independent and the dependent variable.',
                        answer=f'How does {_short(v["iv"])} affect {_short(v["dv"])}?',
                        markingKey=f'1 mark: names the independent variable ({v["iv"]}); 1 mark: names the measurable dependent variable ({v["dv"]}) in a question form.', type='short', marks=2, gap='G4')
        return dict(stem=f'{who} is investigating {v["ctx"]}. Formulate a testable hypothesis and justify it using scientific knowledge.', answer=v['hyp'],
                    markingKey=f'1 mark: testable prediction in "if … then …" form linking the independent and dependent variables; 1-2 marks: scientific explanation. Model: {v["hyp"]}', type='explain', marks=3, gap='G4')
    R.t.setdefault(key, []).append(T('C3', (1, 5), inq, 'multi_step', 'inquiry', 'inquiry'))

    def design(rng, slot):
        v = rng.choice(invs)
        who = name(rng)
        k = rng.choice(['method', 'process', 'risk'] + (['weak'] if v.get('weak') else []))
        if k == 'process':
            return dict(stem=f'{who} plans an investigation into {v["ctx"]}. Describe how the results should be recorded, processed and presented, and explain how the reliability and validity of the conclusion will be judged.',
                        answer=f'Results table with the independent variable ({v["iv"]}) in the first column and repeat readings of the dependent variable with units in headings; calculate means (ignoring anomalies); plot a suitable graph of the mean dependent variable against the independent variable with a line of best fit; describe the trend and compare with the hypothesis; judge reliability from the spread of repeats and validity from how well variables were controlled.',
                        type='multi_step', marks=5, gap='G4',
                        markingKey='1 table with IV, repeats and units; 1 means calculated, anomalies identified and excluded; 1 appropriate graph (line graph/scatter for continuous IV, bar chart for categorical) with line of best fit; 1 trend compared with hypothesis; 1 reliability (spread of repeats) and validity (controls) discussed.')
        if k == 'risk':
            return dict(stem=f'Write a risk assessment for an investigation into {v["ctx"]}. Identify two hazards, the risk each poses and how each risk will be reduced, and explain one ethical or environmental consideration.',
                        answer=f'Key hazard(s): {v.get("safety", "equipment and materials used")}. For each hazard: state what could go wrong, how likely/serious it is, and the precaution. Ethical/environmental: e.g. minimise waste and dispose of chemicals correctly, treat living organisms and volunteers with respect and consent.',
                        type='multi_step', marks=5, gap='G4',
                        markingKey=f'2 two relevant hazards with the risk explained (e.g. {v.get("safety", "")}); 2 a specific precaution for each; 1 relevant ethical or environmental consideration.')
        if k == 'method':
            stem = (f'Design a safe and valid method to investigate {v["ctx"]}. In your answer include the variables, the equipment, '
                    f'the range and number of values of the independent variable, the number of repeats, safety and how the data will be recorded and processed.')
            return dict(stem=stem, answer=v['method'], type='multi_step', marks=6, gap='G4',
                        markingKey=f'MYP criterion B: 1 independent variable with at least 5 values in a sensible range; 1 dependent variable and how it is measured; 1 at least two controls and how they are controlled; 1 logical step-by-step procedure with equipment; 1 at least 3 repeats and calculation of a mean; 1 relevant safety point ({v.get("safety", "appropriate eye protection and care with equipment")}). Model: {v["method"]}')
        w, imp = v['weak']
        stem = (f'{who} investigated {v["ctx"]}. The method had this weakness: {w}. Evaluate how this weakness affects the validity of the results and suggest an improvement to the method.')
        return dict(stem=stem, answer=imp, type='multi_step', marks=4, gap='G5',
                    markingKey=f'1 identifies how the weakness introduces error or an uncontrolled variable; 1 states the effect on the results/conclusion; 1-2 a specific, practical improvement: {imp}')
    R.t.setdefault(key, []).append(T('C4', (3, 5), design, 'multi_step', 'inquiry', 'design'))


def _tidy(t):
    """Remove the gaps left when a variable has no unit (e.g. pH, counts)."""
    t = t.replace(' / :', ':')
    t = re.sub(r' +([,.;:)])', r'\1', t)
    t = re.sub(r'(?<![\d.,])1 (day|week|hour|minute|month|year|generation|second)s\b', r'1 \1', t)
    return re.sub(r'(?<=\S)  +', ' ', t)


def dataset(R, key, *ctxs):
    """Criterion C table items. ctx: dict(intro, iv=(name, unit), xs=[...], dv=(name, unit), f=lambda x: true y, dp, trend, why)."""

    def make_table(rng, c, anomaly):
        xs = c['xs'](rng) if callable(c['xs']) else c['xs']
        k = rng.uniform(0.85, 1.15)
        rows = []
        for x in xs:
            base = c['f'](x) * k
            rows.append([round(base * rng.uniform(0.96, 1.04), c['dp']) for _ in range(3)])
        an = None
        if anomaly:
            i = rng.randrange(1, len(xs) - 1)
            j = rng.randrange(3)
            rows[i][j] = round(rows[i][j] * rng.choice([1.35, 0.65]), c['dp'])
            an = (i, j)
        return xs, rows, an

    def table_text(c, xs, rows):
        ivn, ivu = c['iv']
        dvn, dvu = c['dv']
        head = (f'{ivn} / {ivu}' if ivu else ivn) + f' | {dvn} / {dvu}: Trial 1 | Trial 2 | Trial 3'
        lines = [head] + [f'{x} | ' + ' | '.join(f'{v:.{c["dp"]}f}' for v in row) for x, row in zip(xs, rows)]
        return '\n'.join(lines)

    def data(rng, slot):
        c = rng.choice(ctxs)
        who = name(rng)
        full = (slot.marks or 0) >= 5
        kind = 'full' if full else rng.choice(['mean', 'anom', 'trend', 'pct', 'range'] if slot.d >= 3 else ['mean', 'mean', 'trend', 'range'])
        xs, rows, an = make_table(rng, c, kind in ('anom', 'full'))
        tab = table_text(c, xs, rows)
        intro = c['intro'].format(who=who)
        dp = c['dp'] + 1 if c['dp'] < 2 else c['dp']
        means = []
        for i, row in enumerate(rows):
            vals = [v for j, v in enumerate(row) if an != (i, j)]
            means.append(sum(vals) / len(vals))
        ivn, ivu = c['iv']
        dvn, dvu = c['dv']
        if kind == 'mean':
            i = rng.randrange(len(xs))
            m = sum(rows[i]) / 3
            return dict(stem=f'{intro}\n\n{tab}\n\nCalculate the mean {_lc(dvn)} when the {_lc(ivn)} was {xs[i]} {ivu}.', answer=f'{m:.{dp}f} {dvu}',
                        markingKey=f'M1 ({" + ".join(f"{v:.{c["dp"]}f}" for v in rows[i])}) ÷ 3; A1 {m:.{dp}f} {dvu} (unit and sensible precision).', type='numerical', marks=2, gap='G3')
        if kind == 'anom':
            i, j = an
            return dict(stem=f'{intro}\n\n{tab}\n\nIdentify the anomalous result. Calculate the mean {_lc(dvn)} at {xs[i]} {ivu}, excluding the anomaly.',
                        answer=f'Anomaly: {rows[i][j]:.{c["dp"]}f} {dvu} (trial {j + 1} at {xs[i]} {ivu}); mean = {means[i]:.{dp}f} {dvu}',
                        markingKey=f'1 anomaly identified ({rows[i][j]:.{c["dp"]}f}) as it does not fit the pattern of the other repeats; M1 mean of the two remaining values; A1 {means[i]:.{dp}f} {dvu}.', type='numerical', marks=3, gap='G3')
        if kind == 'pct':
            a, b = means[0], means[-1]
            p = (b - a) / a * 100
            return dict(stem=f'{intro}\n\n{tab}\n\nCalculate the percentage change in the mean {_lc(dvn)} between {xs[0]} {ivu} and {xs[-1]} {ivu}.',
                        answer=f'{p:+.1f}%', markingKey=f'M1 means {a:.{dp}f} and {b:.{dp}f}; M1 (new − old) ÷ old × 100; A1 {p:+.1f}% ({"increase" if p > 0 else "decrease"}).', type='numerical', marks=3, gap='G3')
        if kind == 'range':
            spreads = [max(row) - min(row) for row in rows]
            i = max(range(len(rows)), key=lambda q: spreads[q])
            return dict(stem=f'{intro}\n\n{tab}\n\nState the {_lc(ivn)} at which the repeat readings are least consistent, and calculate the range of the readings at that value. Suggest one way to make the data more reliable.',
                        answer=f'{xs[i]} {ivu}; range = {spreads[i]:.{c["dp"]}f} {dvu}; e.g. take more repeats and discard anomalies / use more precise apparatus',
                        markingKey=f'1 {xs[i]} {ivu}; 1 range = max − min = {max(rows[i]):.{c["dp"]}f} − {min(rows[i]):.{c["dp"]}f} = {spreads[i]:.{c["dp"]}f} {dvu}; 1 valid improvement (more repeats, more precise instrument, control a named variable).', type='short', marks=3, gap='G3')
        if kind == 'trend':
            return dict(stem=f'{intro}\n\n{tab}\n\nDescribe the trend shown by the results and explain it using scientific knowledge.',
                        answer=f'{c["trend"]} {c["why"]}', markingKey=f'1 trend: {c["trend"]}; 1 use of data (quote means/values); 1-2 explanation: {c["why"]}', type='explain', marks=4, gap='G3')
        i, j = an
        ms = ', '.join(f'{x} {ivu}: {m:.{dp}f}' for x, m in zip(xs, means))
        stem = (f'{intro}\n\n{tab}\n\n(a) Identify the anomalous result and suggest one cause. [1]\n(b) Calculate the mean {_lc(dvn)} for each {_lc(ivn)}, ignoring the anomaly. [2]\n'
                f'(c) Describe the trend and explain it using scientific reasoning. [2]')
        if (slot.marks or 6) >= 6:
            stem += f'\n(d) State whether the data support the hypothesis that "{c["hyp"] if "hyp" in c else c["trend"]}" and justify your answer. [1]'
        return dict(stem=stem, answer=f'(a) {rows[i][j]:.{c["dp"]}f} at {xs[i]} {ivu}. (b) {ms}. (c) {c["trend"]} {c["why"]} (d) Supported: the means follow the predicted pattern across the range.',
                    markingKey=f'(a) 1 anomaly {rows[i][j]:.{c["dp"]}f} with a plausible cause (misreading, timing error, uncontrolled variable). (b) M1 method, A1 all means correct: {ms} {dvu}. (c) 1 trend with data, 1 scientific explanation: {c["why"]} (d) 1 justified conclusion referring to the processed data.', type='multi_step', marks=slot.marks or 6, gap='G3')
    def data_tidy(rng, slot):
        q = data(rng, slot)
        for k in ('stem', 'answer', 'markingKey'):
            q[k] = _tidy(q[k])
        return q
    R.t.setdefault(key, []).append(T('C3', (1, 5), data_tidy, 'numerical', 'data', 'data'))


