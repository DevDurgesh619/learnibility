"""IB MYP 4 Sciences (integrated biology / chemistry / physics) – ib-g9-science.

Criteria language: A knowing & understanding, B inquiring & designing (research question,
hypothesis, variables, method), C processing & evaluating (data tables, graphs, means, rates,
conclusions, reliability), D reflecting on the impacts of science (ethics, environment,
economics, health). Numerical items compute their own answers.
"""
from __future__ import annotations

import math
import re

from _common import F, Registry, T, fmt, mcq, name, num_distractors, two_names, CITIES

CONFIG = {'minutesPerMark': 1.2, 'mcqMinutes': 1.5}

# MYP 5 Sciences eAssessment-style on-screen exam (practised early in MYP 4): tasks across
# criteria A-D, 20 items, 100 marks; every mock has the same section structure and marks.
MOCK = [
    dict(section='Task 1 – Knowing and understanding: quick-check items (criterion A)', count=6, c=['C1'], d=[1, 2, 2], type='mcq', marks=1),
    dict(section='Task 2 – Knowing and understanding: explain scientific knowledge (criterion A)', count=4, c=['C2'], d=[2, 3, 3], type='explain', marks=4),
    dict(section='Task 3 – Inquiring and designing: hypothesis, variables and method (criterion B)', count=4, c=['C3', 'C3', 'C4'], d=[3, 4], type='multi_step', marks=6, style='inquiry'),
    dict(section='Task 4 – Processing and evaluating: data, graphs and conclusions (criterion C)', count=4, c=['C3'], d=[3, 4], type='multi_step', marks=6, style='data'),
    dict(section='Task 5 – Reflecting on the impacts of science (criterion D)', count=2, c=['C4'], d=[5], type='long', marks=15),
]

R = Registry()

STYLE = {'eval_marks': 8, 'essay_marks': 15,
         'markband': 'MYP criterion D (0-8, scaled): 7-8 explains thoroughly how the science is applied to address the issue, discusses and evaluates the implications (moral, ethical, social, economic, political, cultural or environmental), and documents sources consistently; 5-6 explains and discusses; 3-4 outlines; 1-2 states.'}


def init(subject_id):
    pass


PROPER = {'Newton’s', 'Mendeleev', 'Punnett', 'Rosalind', 'Mendel', 'Rutherford', 'Watson', 'Gregor', 'Queen', 'Huntington’s', 'Earth’s'}
_LC_RE = re.compile(r'(claims that|claim that|the view that|is it true that) ([A-Z][a-z][^ ]*)')


def _lc_fix(stem):
    def sub(m):
        w = m.group(2)
        return m.group(0) if w in PROPER else f'{m.group(1)} {w[0].lower()}{w[1:]}'
    return _LC_RE.sub(sub, stem)


def _wrap(fn):
    def inner(rng, slot):
        out = fn(rng, slot)
        if out and isinstance(out.get('stem'), str):
            out['stem'] = _lc_fix(out['stem'])
        return out
    inner._wrapped = True
    return inner


def templates(st):
    out = R.build(st, STYLE)
    for t in out:
        if not getattr(t.fn, '_wrapped', False):
            t.fn = _wrap(t.fn)
    return out


def r(x, dp=2):
    """Round and format with dp decimals, trimming nothing (data-table style)."""
    return f'{x:.{dp}f}'


def g(x, sf=3):
    """Format to sf significant figures, plain notation."""
    if x == 0:
        return '0'
    s = f'{x:.{sf}g}'
    if 'e' in s:
        return fmt(x, sf)
    return s


# =============================================================================================
# Shared criterion B (inquiry) and criterion C (data) template builders
# =============================================================================================
def _short(txt):
    t = re.split(r' – | \(| = |, |; | measured | read | from a | counted ', txt)[0].strip()
    return t[0].lower() + t[1:] if t[:2] != t[:2].upper() else t


def inquiry(key, *invs):
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
            return dict(stem=stem, answer=ans, markingKey=key_, type='multi_step', marks=6, gap='G4')
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
            return dict(stem=f'In an investigation into {v["ctx"]}, explain why {c[0]} must be kept the same in every trial.', answer=c[1],
                        markingKey=f'1 mark: {c[0]} would also affect the dependent variable; 1 mark for the specific reason: {c[1]}. Then only the independent variable is responsible for any change (validity).', type='explain', marks=2, gap='G4')
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


def dataset(key, *ctxs):
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
            return dict(stem=f'{intro}\n\n{tab}\n\nCalculate the mean {dvn.lower()} when the {ivn.lower()} was {xs[i]} {ivu}.', answer=f'{m:.{dp}f} {dvu}',
                        markingKey=f'M1 ({" + ".join(f"{v:.{c["dp"]}f}" for v in rows[i])}) ÷ 3; A1 {m:.{dp}f} {dvu} (unit and sensible precision).', type='numerical', marks=2, gap='G3')
        if kind == 'anom':
            i, j = an
            return dict(stem=f'{intro}\n\n{tab}\n\nIdentify the anomalous result. Calculate the mean {dvn.lower()} at {xs[i]} {ivu}, excluding the anomaly.',
                        answer=f'Anomaly: {rows[i][j]:.{c["dp"]}f} {dvu} (trial {j + 1} at {xs[i]} {ivu}); mean = {means[i]:.{dp}f} {dvu}',
                        markingKey=f'1 anomaly identified ({rows[i][j]:.{c["dp"]}f}) as it does not fit the pattern of the other repeats; M1 mean of the two remaining values; A1 {means[i]:.{dp}f} {dvu}.', type='numerical', marks=3, gap='G3')
        if kind == 'pct':
            a, b = means[0], means[-1]
            p = (b - a) / a * 100
            return dict(stem=f'{intro}\n\n{tab}\n\nCalculate the percentage change in the mean {dvn.lower()} between {xs[0]} {ivu} and {xs[-1]} {ivu}.',
                        answer=f'{p:+.1f}%', markingKey=f'M1 means {a:.{dp}f} and {b:.{dp}f}; M1 (new − old) ÷ old × 100; A1 {p:+.1f}% ({"increase" if p > 0 else "decrease"}).', type='numerical', marks=3, gap='G3')
        if kind == 'range':
            spreads = [max(row) - min(row) for row in rows]
            i = max(range(len(rows)), key=lambda q: spreads[q])
            return dict(stem=f'{intro}\n\n{tab}\n\nState the {ivn.lower()} at which the repeat readings are least consistent, and calculate the range of the readings at that value. Suggest one way to make the data more reliable.',
                        answer=f'{xs[i]} {ivu}; range = {spreads[i]:.{c["dp"]}f} {dvu}; e.g. take more repeats and discard anomalies / use more precise apparatus',
                        markingKey=f'1 {xs[i]} {ivu}; 1 range = max − min = {max(rows[i]):.{c["dp"]}f} − {min(rows[i]):.{c["dp"]}f} = {spreads[i]:.{c["dp"]}f} {dvu}; 1 valid improvement (more repeats, more precise instrument, control a named variable).', type='short', marks=3, gap='G3')
        if kind == 'trend':
            return dict(stem=f'{intro}\n\n{tab}\n\nDescribe the trend shown by the results and explain it using scientific knowledge.',
                        answer=f'{c["trend"]} {c["why"]}', markingKey=f'1 trend: {c["trend"]}; 1 use of data (quote means/values); 1-2 explanation: {c["why"]}', type='explain', marks=4, gap='G3')
        i, j = an
        ms = ', '.join(f'{x} {ivu}: {m:.{dp}f}' for x, m in zip(xs, means))
        stem = (f'{intro}\n\n{tab}\n\n(a) Identify the anomalous result and suggest one cause. [1]\n(b) Calculate the mean {dvn.lower()} for each {ivn.lower()}, ignoring the anomaly. [2]\n'
                f'(c) Describe the trend and explain it using scientific reasoning. [2]\n(d) State whether the data support the hypothesis that "{c["hyp"] if "hyp" in c else c["trend"]}" and justify your answer. [1]')
        return dict(stem=stem, answer=f'(a) {rows[i][j]:.{c["dp"]}f} at {xs[i]} {ivu}. (b) {ms}. (c) {c["trend"]} {c["why"]} (d) Supported: the means follow the predicted pattern across the range.',
                    markingKey=f'(a) 1 anomaly {rows[i][j]:.{c["dp"]}f} with a plausible cause (misreading, timing error, uncontrolled variable). (b) M1 method, A1 all means correct: {ms} {dvu}. (c) 1 trend with data, 1 scientific explanation: {c["why"]} (d) 1 justified conclusion referring to the processed data.', type='multi_step', marks=6, gap='G3')
    R.t.setdefault(key, []).append(T('C3', (1, 5), data, 'numerical', 'data', 'data'))


# =============================================================================================
# ch01 Cell Division and DNA
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('gene', 'a section of DNA on a chromosome that codes for a specific protein'),
           ('chromosome', 'a long, coiled molecule of DNA (with proteins) found in the nucleus that carries many genes'),
           ('DNA', 'deoxyribonucleic acid: a double-helix polymer of nucleotides that carries the genetic code'),
           ('nucleotide', 'the monomer of DNA, made of a phosphate group, a deoxyribose sugar and one of four bases'),
           ('complementary base pairing', 'the rule that adenine always pairs with thymine and cytosine always pairs with guanine across the two DNA strands'),
           ('genome', 'the entire genetic material of an organism')],
    facts=[('Which base pairs with cytosine in DNA?', 'Guanine', ['Thymine', 'Adenine', 'Uracil'], 'C pairs with G by three hydrogen bonds; A pairs with T.'),
           ('How many chromosomes are found in a normal human body cell?', '46 (23 pairs)', ['23', '44', '92'], 'Human diploid cells have 23 pairs: 22 pairs of autosomes and one pair of sex chromosomes.'),
           ('Which list is in order of size from largest to smallest?', 'Nucleus, chromosome, gene, base', ['Gene, chromosome, nucleus, base', 'Chromosome, nucleus, gene, base', 'Base, gene, chromosome, nucleus'], 'A nucleus holds chromosomes; each chromosome carries many genes; each gene is a sequence of bases.'),
           ('Which scientists are credited with proposing the double-helix model of DNA in 1953, using X-ray data from Rosalind Franklin?', 'James Watson and Francis Crick', ['Gregor Mendel and Charles Darwin', 'Robert Hooke and Antonie van Leeuwenhoek', 'Ernest Rutherford and Niels Bohr'], 'Watson and Crick built the model; Franklin’s Photo 51 showed the helical structure.'),
           ('What holds the two strands of a DNA double helix together?', 'Hydrogen bonds between complementary bases', ['Covalent bonds between phosphate groups', 'Ionic bonds between sugars', 'Peptide bonds between amino acids'], 'Weak hydrogen bonds let the strands separate for copying.')],
    why=[('Explain why the base sequence of a gene determines the protein it codes for.', 'Each group of three bases (a triplet/codon) codes for one amino acid; the order of bases therefore sets the order of amino acids, which determines the protein’s shape and function.'),
         ('Explain why complementary base pairing allows DNA to be copied accurately.', 'When the strands separate, each acts as a template; free nucleotides can only pair A–T and C–G, so each new strand is an exact complement and the two new molecules are identical to the original.'),
         ('Explain why the amount of adenine in a DNA molecule equals the amount of thymine.', 'Every adenine on one strand is paired with a thymine on the other strand, so the numbers must be equal (Chargaff’s rule).'),
         ('Explain why a change in a single base of a gene can lead to a genetic disorder.', 'A changed base can change the triplet and therefore the amino acid; the protein may fold differently and stop working, e.g. sickle-cell anaemia from one base change in the haemoglobin gene.')],
    contrast=[('a gene', 'a chromosome', 'A gene is a short section of DNA coding for one protein; a chromosome is a whole DNA molecule carrying hundreds or thousands of genes.'),
              ('DNA', 'a nucleotide', 'A nucleotide is a single unit (phosphate, sugar, base); DNA is the long polymer of millions of nucleotides in two strands.'),
              ('a gene', 'an allele', 'A gene is a section of DNA for a characteristic; an allele is one alternative version of that gene.')],
    misc=[('Genes are made of chromosomes.', 'It is the other way round: chromosomes are made of DNA, and genes are short sections of that DNA.'),
          ('Only some of your body cells contain DNA for eye colour.', 'Almost every body cell (except mature red blood cells) contains the full genome; genes are switched on or off in different cells.'),
          ('In DNA, adenine pairs with cytosine because both are large bases.', 'Adenine pairs with thymine and cytosine with guanine; a large purine always pairs with a smaller pyrimidine, keeping the helix the same width.')],
    cases=[('the Human Genome Project (completed 2003)', 'Scientists in many countries sequenced the roughly 3 billion base pairs of human DNA and found about 20 000 protein-coding genes.', 'how genes are sections of DNA with a base sequence', 'Reading the base sequence let researchers locate genes along each chromosome and link specific sequences to diseases.'),
           ('Rosalind Franklin’s X-ray photograph “Photo 51”', 'Franklin and Gosling used X-ray crystallography at King’s College London; the X-shaped pattern showed DNA is a helix with regular spacing.', 'the double-helix structure of DNA', 'The pattern gave the evidence (helix, diameter, repeat distance) that Watson and Crick used to build their model.')],
    evaluate=[('Personal genome testing kits sold directly to the public do more good than harm.', ['they can reveal carrier status or risk of conditions so people can make health choices', 'they encourage interest in science and family history'], ['results are probabilistic and may cause anxiety or false reassurance', 'genetic data privacy: companies may share data with insurers or police', 'no genetic counsellor to explain results'], 'The benefit depends on regulation: with privacy protection and access to counselling, benefits can outweigh harms; without them the risks are significant.'),
              ('Scientists should be allowed to patent human genes they have sequenced.', ['patents reward the cost of research and encourage investment', 'they can fund development of tests and treatments'], ['genes are natural, discovered rather than invented', 'patents raise the cost of tests (e.g. BRCA test before the 2013 US Supreme Court ruling) and limit research by others'], 'Most societies now judge that naturally occurring sequences should not be patented, though new methods using them can be.')],
    extended=[('A DNA sample contains 22% thymine. Calculate the percentage of each of the other three bases and explain your reasoning.', 'A = 22% (pairs with T); A + T = 44%, so C + G = 56%; C = G = 28%.', 4),
              ('Outline how the structure of DNA makes it suitable for storing and copying genetic information.', 'Long molecule – stores a huge amount of information as a base sequence; double-stranded with complementary bases – each strand is a template for copying; weak hydrogen bonds – strands separate easily; sugar-phosphate backbone – strong and stable; coiled into chromosomes – fits in the nucleus.', 5)],
))


@R.add('ch01-st1', 'C3', (1, 4), 'numerical')
def chargaff(rng, slot):
    b = rng.choice(['adenine', 'thymine', 'cytosine', 'guanine'])
    p = rng.randint(12, 38)
    pair = {'adenine': 'thymine', 'thymine': 'adenine', 'cytosine': 'guanine', 'guanine': 'cytosine'}[b]
    other = (100 - 2 * p) / 2
    o1, o2 = ('cytosine', 'guanine') if b in ('adenine', 'thymine') else ('adenine', 'thymine')
    org = rng.choice(['a wheat plant', 'a salmon', 'a sample of yeast', 'a human liver cell', 'a sea urchin', 'a strain of E. coli'])
    frames = [f'Analysis of DNA from {org} shows that {p}% of the bases are {b}. Calculate the percentage of {o1}.',
              f'In DNA extracted from {org}, {b} makes up {p}% of the bases. What percentage of the bases are {pair}, and what percentage are {o2}?']
    i = rng.randrange(2)
    ans = f'{other:g}%' if i == 0 else f'{pair}: {p}%; {o2}: {other:g}%'
    return dict(stem=frames[i], answer=ans, markingKey=f'{b} pairs with {pair}, so {pair} = {p}% (M1); {o1} + {o2} = 100 − {2 * p} = {100 - 2 * p}% (M1); each = {other:g}% (A1).', marks=3)


@R.add('ch01-st1', 'C3', (2, 4), 'short')
def complement(rng, slot):
    n = 6 + slot.d * 2
    seq = ''.join(rng.choice('ATCG') for _ in range(n))
    comp = seq.translate(str.maketrans('ATCG', 'TAGC'))
    trip = n // 3
    q = rng.choice([(f'One strand of a section of DNA has the base sequence {seq}. Write the base sequence of the complementary strand.', comp, 2),
                    (f'A gene fragment reads {seq} on one strand. (a) Write the complementary sequence. (b) How many amino acids could this fragment code for?', f'(a) {comp} (b) {trip}', 3)])
    return dict(stem=q[0], answer=q[1], markingKey=f'A↔T and C↔G applied to every base: {comp} (1-2 marks; −1 per error).' + (f' Three bases code for one amino acid: {n} ÷ 3 = {trip} (1).' if q[2] == 3 else ''), marks=q[2])


inquiry('ch01-st1',
        dict(ctx='how the volume of washing-up liquid added affects the mass of DNA extracted from 50 g of strawberries',
             iv='volume of washing-up liquid added (cm³)', dv='mass of DNA precipitated – collected on a glass rod, blotted and weighed on a balance to 0.01 g',
             cvs=[('mass of strawberries', 'more fruit gives more cells and more DNA'), ('volume and temperature of ice-cold ethanol', 'ethanol temperature affects how much DNA precipitates'), ('salt concentration', 'salt helps DNA clump together'), ('mashing time', 'more mashing breaks open more cells')],
             hyp='If more washing-up liquid is added, then more DNA will be extracted up to a point, because detergent breaks down the lipid cell and nuclear membranes, releasing DNA; once all membranes are broken, extra detergent has no effect.',
             method='Mash 50 g strawberries in a sealed bag for 2 min; add 10 cm³ salty water and 0, 2, 4, 6, 8 or 10 cm³ washing-up liquid (make volume up to 20 cm³ with water); filter through a coffee filter; pour 10 cm³ ice-cold ethanol down the side of the tube; wait 5 min; spool DNA on a glass rod, blot and weigh; repeat three times per volume and calculate means.',
             weak=('the ethanol was taken from the fridge for some trials and left at room temperature for others', 'keep the ethanol in an ice bath throughout so every trial uses ethanol at the same low temperature'),
             safety='ethanol is highly flammable – no naked flames; wear eye protection'))

R.facts('ch01-st2', F(
    terms=[('mitosis', 'cell division that produces two genetically identical daughter cells, each with the same number of chromosomes as the parent cell'),
           ('cell cycle', 'the sequence of growth, DNA replication and division that a cell goes through: interphase, mitosis and cytokinesis'),
           ('interphase', 'the longest stage of the cell cycle, in which the cell grows, makes new organelles and replicates its DNA'),
           ('cytokinesis', 'the division of the cytoplasm to form two separate daughter cells after the nucleus has divided'),
           ('chromatid', 'one of the two identical copies of a replicated chromosome, joined to its sister at the centromere'),
           ('tumour', 'a mass of cells formed by uncontrolled mitosis')],
    facts=[('In which stage of mitosis do chromosomes line up along the equator of the cell?', 'Metaphase', ['Prophase', 'Anaphase', 'Telophase'], 'In metaphase spindle fibres attach to centromeres and align the chromosomes at the equator.'),
           ('A skin cell with 46 chromosomes divides by mitosis. How many chromosomes are in each daughter cell?', '46', ['23', '92', '44'], 'Mitosis keeps the chromosome number the same.'),
           ('During which stage of the cell cycle is DNA replicated?', 'Interphase', ['Metaphase', 'Anaphase', 'Cytokinesis'], 'DNA is copied in interphase (the S phase) before division begins.'),
           ('What happens during anaphase?', 'Sister chromatids are pulled to opposite poles of the cell', ['Chromosomes condense and become visible', 'The nuclear membrane re-forms', 'The cytoplasm divides'], 'Spindle fibres shorten and separate the chromatids.'),
           ('Which of the following is NOT a role of mitosis?', 'Producing gametes', ['Growth of an embryo', 'Repairing a cut in the skin', 'Asexual reproduction in yeast'], 'Gametes are produced by meiosis.')],
    why=[('Explain why DNA must be replicated before a cell divides by mitosis.', 'Each daughter cell must receive a full, identical set of chromosomes; copying the DNA first means there are two chromatids per chromosome, one for each new cell.'),
         ('Explain why most of the cells seen in a root-tip squash are in interphase.', 'Interphase is the longest stage of the cell cycle, so at any moment the largest proportion of cells is in it; the proportion of cells in a stage is proportional to the time spent in that stage.'),
         ('Explain why cancer can develop when the control of the cell cycle fails.', 'Mutations in genes that control the cycle let a cell divide by mitosis repeatedly without stopping, forming a tumour; malignant tumours can invade tissues and spread.'),
         ('Explain why a root tip is used to observe mitosis rather than a mature leaf.', 'The root tip contains a meristem where cells are dividing rapidly, so many cells are in mitosis; mature leaf cells have mostly stopped dividing.')],
    contrast=[('a chromosome', 'a chromatid', 'A chromatid is one of two identical copies of a replicated chromosome; after anaphase each chromatid becomes a separate chromosome.'),
              ('mitosis', 'cytokinesis', 'Mitosis is the division of the nucleus; cytokinesis is the division of the cytoplasm that follows.'),
              ('a benign tumour', 'a malignant tumour', 'A benign tumour stays in one place in a capsule; a malignant tumour invades nearby tissue and cells can spread (metastasis) to form secondary tumours.')],
    misc=[('Cells are resting during interphase because they are not dividing.', 'Interphase is very active: the cell grows, makes proteins and organelles and replicates its DNA.'),
          ('In mitosis the chromosome number halves so the daughter cells are smaller.', 'Mitosis keeps the chromosome number the same (46 → 46); halving happens in meiosis.'),
          ('Mitosis produces genetic variation between daughter cells.', 'Mitosis produces genetically identical cells (clones); variation comes from meiosis and fertilisation.')],
    cases=[('HeLa cells, taken from Henrietta Lacks in 1951', 'Cancer cells from her cervical tumour kept dividing indefinitely in culture and have been used in research on polio vaccines and cancer.', 'uncontrolled mitosis in cancer cells', 'They divide without the normal limits of the cell cycle, showing what happens when control of mitosis is lost; the case also raised issues of consent.'),
           ('healing of a grazed knee', 'Cells in the basal layer of the epidermis divide repeatedly to replace damaged cells over several days.', 'the role of mitosis in repair', 'Mitosis produces new, genetically identical skin cells that replace the lost ones.')],
    evaluate=[('Chemotherapy drugs that stop mitosis are the best treatment for cancer.', ['they kill rapidly dividing cancer cells throughout the body, including cells that have spread', 'they can shrink tumours before surgery'], ['they also damage healthy dividing cells (hair follicles, gut lining, bone marrow), causing side effects', 'cancer cells can become resistant', 'surgery, radiotherapy or targeted immunotherapy may work better for some cancers'], 'Chemotherapy is effective but not always best; the choice depends on the type and stage of cancer, often in combination with other treatments.'),
              ('The story of the HeLa cells shows that patients should always give consent before their cells are used in research.', ['respect for autonomy and the family’s right to know', 'companies profited without the family benefiting'], ['in 1951 consent rules did not exist and the research saved millions of lives', 'anonymised samples may be needed for large studies'], 'Informed consent is now an accepted ethical principle; the HeLa case shows why, even though the research brought huge benefits.')],
    extended=[('Describe the main events of each stage of mitosis, in order, and explain how the process produces two genetically identical cells.', 'Prophase: chromosomes condense, nuclear membrane breaks down, spindle forms. Metaphase: chromosomes line up at the equator. Anaphase: sister chromatids separate to opposite poles. Telophase: nuclear membranes re-form; cytokinesis divides the cell. Identical because DNA was copied exactly and each cell gets one chromatid of every chromosome.', 6)],
))


@R.add('ch01-st2', 'C3', (1, 5), 'numerical')
def mitotic_index(rng, slot):
    tot = rng.choice([200, 250, 300, 400, 500])
    m = rng.randint(12, 60)
    who = name(rng)
    tissue = rng.choice(['an onion root tip', 'a garlic root tip', 'a broad bean root tip', 'a section of human skin tumour', 'a hyacinth root tip'])
    mi = m / tot
    if slot.d >= 3:
        cyc = rng.choice([16, 18, 20, 22, 24])
        t = mi * cyc * 60
        return dict(stem=f'{who} counted {tot} cells in a squash of {tissue}; {m} of them were in mitosis. The whole cell cycle takes {cyc} hours. Calculate the mitotic index and estimate how long, in minutes, mitosis lasts.',
                    answer=f'{mi:.3f}; {t:.0f} min', markingKey=f'M1 mitotic index = cells in mitosis ÷ total = {m}/{tot} = {mi:.3f}; M1 time ∝ proportion: {mi:.3f} × {cyc} h × 60; A1 {t:.0f} min.', marks=3)
    return dict(stem=f'In a microscope slide of {tissue}, {who} counted {m} cells in mitosis out of {tot} cells. Calculate the mitotic index as a percentage.',
                answer=f'{mi * 100:.1f}%', markingKey=f'M1 {m} ÷ {tot} × 100; A1 {mi * 100:.1f}%.', marks=2)


@R.add('ch01-st2', 'C3', (2, 4), 'numerical')
def doubling(rng, slot):
    h = rng.choice([20, 24, 30])
    n = rng.randint(3, 7)
    start = rng.choice([1, 10, 50, 100])
    hrs = h * n
    cells = start * 2 ** n
    org = rng.choice(['human fibroblasts', 'mouse stem cells', 'cultured skin cells', 'plant callus cells'])
    return dict(stem=f'A culture of {start} {org} divides by mitosis every {h} hours. Assuming every cell keeps dividing, how many cells will there be after {hrs} hours?',
                answer=f'{cells}', markingKey=f'M1 number of divisions = {hrs} ÷ {h} = {n}; M1 cells = {start} × 2^{n}; A1 {cells}.', marks=3)


dataset('ch01-st2',
        dict(intro='{who} grew garlic roots at different temperatures and counted the number of cells in mitosis in a field of view of 100 cells.', iv=('Temperature', '°C'), xs=[5, 10, 15, 20, 25],
             dv=('Cells in mitosis', 'cells per 100'), f=lambda x: 2 + 0.6 * x, dp=0, trend='As temperature increases from 5 °C to 25 °C, the number of cells in mitosis increases.',
             why='Higher temperature increases the rate of enzyme-controlled reactions such as DNA replication, so the cell cycle runs faster and more cells are dividing at any moment.',
             hyp='as temperature increases, the number of dividing cells increases'))

inquiry('ch01-st2',
        dict(ctx='how the distance from the root tip affects the mitotic index of onion root cells',
             iv='distance from the root tip (mm)', dv='mitotic index – number of cells in mitosis ÷ total cells counted in a field of view at ×400',
             cvs=[('age of the roots', 'older roots may grow at a different rate'), ('stain and time in hydrochloric acid', 'affects how well cells separate and how visible chromosomes are'), ('number of cells counted', 'a larger sample gives a more representative index'), ('temperature the onion is grown at', 'temperature changes the rate of division')],
             hyp='If the distance from the tip increases, then the mitotic index will decrease, because the meristem (dividing zone) is just behind the tip while cells further back elongate and differentiate rather than divide.',
             method='Grow onion roots in water for 5 days at 20 °C; cut 2 mm sections at 0, 2, 4, 6, 8 mm from the tip; warm in 1 M HCl at 60 °C for 5 min, rinse, stain with toluidine blue and squash under a cover slip; count cells in mitosis and total cells in three fields of view at ×400; repeat with 3 roots and calculate mean mitotic index.',
             weak=('only 20 cells were counted in one field of view per section', 'count at least 100 cells across several fields of view so that the index is representative'),
             safety='hydrochloric acid is corrosive and stain can mark skin – wear eye protection and gloves; take care with scalpel'))

R.facts('ch01-st3', F(
    terms=[('meiosis', 'a type of cell division that produces four genetically different haploid cells (gametes) from one diploid cell'),
           ('haploid', 'a cell with one set of chromosomes (n), e.g. 23 in a human gamete'),
           ('diploid', 'a cell with two sets of chromosomes (2n), one from each parent, e.g. 46 in a human body cell'),
           ('gamete', 'a sex cell (sperm or egg in animals, pollen nucleus or ovule in plants) that fuses with another at fertilisation'),
           ('homologous chromosomes', 'a pair of chromosomes, one from each parent, carrying the same genes in the same positions'),
           ('fertilisation', 'the fusion of a male and a female gamete nucleus to form a diploid zygote')],
    facts=[('How many cells are produced when one cell divides by meiosis?', 'Four', ['Two', 'One', 'Eight'], 'Meiosis has two divisions, producing four haploid cells.'),
           ('A dog has 78 chromosomes in its body cells. How many chromosomes are in a dog sperm cell?', '39', ['78', '156', '26'], 'Gametes are haploid: 78 ÷ 2 = 39.'),
           ('Where in the human body does meiosis take place?', 'Testes and ovaries', ['Bone marrow and skin', 'Liver and kidneys', 'Brain and spinal cord'], 'Gametes are made in the reproductive organs.'),
           ('Which process restores the diploid number after meiosis?', 'Fertilisation', ['Mitosis', 'Cytokinesis', 'Differentiation'], 'Two haploid gametes fuse to give a diploid zygote.'),
           ('Which event in meiosis produces new combinations of alleles on the same chromosome?', 'Crossing over between homologous chromosomes', ['Replication of DNA in interphase', 'Cytokinesis', 'Condensing of chromosomes'], 'Crossing over swaps sections between homologous chromatids.')],
    why=[('Explain why gametes must be haploid.', 'At fertilisation two gametes fuse; if each is haploid (n) the zygote is diploid (2n), so the chromosome number stays constant from generation to generation.'),
         ('Explain how meiosis produces genetic variation.', 'Independent assortment: homologous pairs line up randomly, so each gamete gets a different mix of maternal and paternal chromosomes; crossing over swaps sections between homologous chromosomes, creating new allele combinations.'),
         ('Explain why sexual reproduction produces more variation than asexual reproduction.', 'Sexual reproduction uses meiosis (independent assortment, crossing over) and random fertilisation between two parents; asexual reproduction uses mitosis, producing genetically identical clones.'),
         ('Explain why meiosis involves two divisions.', 'The first division separates homologous chromosomes, halving the chromosome number; the second separates sister chromatids, giving four haploid cells with single chromatids.')],
    contrast=[('mitosis', 'meiosis', 'Mitosis: one division, two diploid daughter cells, genetically identical, for growth and repair. Meiosis: two divisions, four haploid cells, genetically different, for making gametes.'),
              ('haploid', 'diploid', 'Haploid cells have one set of chromosomes (n = 23 in humans); diploid cells have two sets (2n = 46).'),
              ('independent assortment', 'crossing over', 'Independent assortment is the random orientation of whole homologous pairs; crossing over is the exchange of sections between chromatids of a homologous pair.')],
    misc=[('Meiosis produces two identical cells, just like mitosis but in the sex organs.', 'Meiosis produces four cells, each haploid and genetically different.'),
          ('A human egg cell has 46 chromosomes because it will become a baby.', 'An egg is haploid with 23 chromosomes; the zygote gets 46 after fertilisation with a 23-chromosome sperm.'),
          ('Identical twins are genetically identical because they came from two eggs fertilised at the same time.', 'Identical twins form when one zygote splits into two embryos; twins from two eggs are non-identical.')],
    cases=[('Down syndrome (trisomy 21)', 'If chromosome 21 fails to separate in meiosis (non-disjunction), a gamete carries an extra copy; the child has 47 chromosomes.', 'the importance of accurate separation of chromosomes in meiosis', 'Errors in meiosis change the chromosome number of the gamete and therefore of every cell of the child.'),
           ('wheat breeding by Norman Borlaug in Mexico', 'Crossing many wheat varieties produced offspring with new combinations of disease resistance and short stems, raising yields worldwide.', 'genetic variation from sexual reproduction', 'Meiosis and fertilisation shuffled alleles from different parents, giving new combinations to select from.')],
    evaluate=[('Sexual reproduction is always better for a species than asexual reproduction.', ['variation lets some individuals survive changes such as new diseases', 'allows natural selection and adaptation'], ['needs two parents and time and energy to find a mate', 'good allele combinations can be broken up', 'asexual reproduction is fast and suits a stable environment (e.g. aphids, potatoes)'], 'Neither is always better; many organisms (strawberries, aphids) use both depending on conditions.')],
    extended=[('A species has a diploid number of 2n = 8. (a) State the number of chromosomes in a gamete. (b) Calculate the number of different combinations of chromosomes possible in the gametes from independent assortment alone. (c) Explain why the real number of genetically different gametes is even larger.', '(a) 4 (b) 2⁴ = 16 (c) crossing over creates new combinations of alleles within chromosomes.', 4)],
))


@R.add('ch01-st3', 'C3', (2, 5), 'numerical')
def assortment(rng, slot):
    org, n2 = rng.choice([('a fruit fly (Drosophila)', 8), ('a pea plant', 14), ('a house mouse', 40), ('a cat', 38), ('a garden snail', 54), ('maize', 20), ('a tomato plant', 24), ('a human', 46), ('a honey bee queen', 32)])
    n = n2 // 2
    combos = 2 ** n
    k = rng.choice(['gamete', 'combos', 'zygote'])
    if k == 'gamete' or (k == 'combos' and n > 12 and slot.d < 4):
        return dict(stem=f'The body cells of {org} contain {n2} chromosomes. State the number of chromosomes in (a) a gamete, (b) a zygote, (c) a cell produced by mitosis.',
                    answer=f'(a) {n} (b) {n2} (c) {n2}', markingKey=f'(a) haploid = {n2}/2 = {n} (1); (b) gametes fuse: {n} + {n} = {n2} (1); (c) mitosis keeps the number: {n2} (1).', marks=3)
    if k == 'zygote':
        return dict(stem=f'A sperm cell of {org} contains {n} chromosomes. How many chromosomes are in its skin cells, and how many homologous pairs is that?',
                    answer=f'{n2}; {n} pairs', markingKey=f'Sperm is haploid, so body cells have 2 × {n} = {n2} (1) arranged in {n} homologous pairs (1).', marks=2)
    return dict(stem=f'{org[0].upper() + org[1:]} has a diploid number of {n2}. Calculate how many genetically different gametes one individual could make by independent assortment alone (ignore crossing over).',
                answer=f'2^{n} = {combos:,}', markingKey=f'M1 n = {n} pairs; M1 combinations = 2^n; A1 {combos:,}.', marks=3)


dataset('ch01-st3',
        dict(intro='{who} took cuttings from one parent pea plant, so all the plants were clones produced by mitosis. The clones were grown with different fertiliser concentrations and measured their height after 6 weeks.', iv=('Fertiliser concentration', 'g/dm³'), xs=[0, 1, 2, 3, 4],
             dv=('Plant height', 'cm'), f=lambda x: 18 + 4 * x, dp=1, trend='Mean plant height increases as fertiliser concentration increases.',
             why='The clones are genetically identical, so the differences are environmental: fertiliser supplies mineral ions such as nitrate for making proteins, so cells divide and grow more.'))

inquiry('ch01-st3',
        dict(ctx='whether pea plants grown from seed (sexual reproduction) show more variation in height than plants grown from cuttings of one parent (asexual reproduction)',
             iv='method of reproduction (seed or cutting)', dv='variation in plant height – heights of 30 plants measured with a ruler to the nearest mm, range and standard deviation calculated',
             cvs=[('light intensity', 'light affects photosynthesis and growth'), ('volume of water each day', 'water supply affects growth'), ('type of compost and pot size', 'mineral supply and root space affect growth'), ('age of plants when measured', 'older plants are taller')],
             hyp='If plants are grown from seed, then their heights will vary more than plants from cuttings, because meiosis and fertilisation produce genetically different offspring, whereas cuttings are clones from mitosis.',
             method='Grow 30 seeds and 30 cuttings from one parent plant in identical pots of the same compost in the same greenhouse; water 50 cm³ daily; after 6 weeks measure height from soil to tip with a ruler; calculate mean, range and standard deviation for each group.',
             weak=('only five plants of each type were measured', 'measure at least 30 plants of each type so the spread is representative and anomalies have less effect'),
             safety='wash hands after handling compost; use a scalpel carefully when taking cuttings'))

R.facts('ch01-st4', F(
    terms=[('stem cell', 'an undifferentiated cell that can divide repeatedly and differentiate into different types of specialised cell'),
           ('differentiation', 'the process by which a cell becomes specialised for a particular function by switching certain genes on and others off'),
           ('embryonic stem cell', 'a stem cell from an early embryo that can differentiate into almost any cell type (pluripotent)'),
           ('adult stem cell', 'a stem cell found in tissues such as bone marrow that can produce only a limited range of cell types'),
           ('meristem', 'a region of undifferentiated, dividing cells in plants, found at root and shoot tips'),
           ('therapeutic cloning', 'producing an embryo with the patient’s own genes so that its stem cells will not be rejected')],
    facts=[('Which of these is a source of adult stem cells used in medicine?', 'Bone marrow', ['Red blood cells', 'Nerve axons', 'Mature skin keratin'], 'Bone marrow stem cells form blood cells and are used in transplants for leukaemia.'),
           ('Where are stem cells found in plants?', 'In meristems at the tips of roots and shoots', ['In the cuticle of leaves', 'In xylem vessels', 'In guard cells only'], 'Meristem cells stay undifferentiated and divide throughout the plant’s life.'),
           ('Which disease has been treated by bone marrow transplants for decades?', 'Leukaemia', ['Influenza', 'Malaria', 'Tuberculosis'], 'Bone marrow stem cells replace the patient’s blood-forming cells.'),
           ('What makes a cell “specialised”?', 'It has a structure adapted to a particular function', ['It can divide faster than other cells', 'It contains more chromosomes', 'It has no nucleus'], 'Differentiation gives cells features such as cilia, long axons or many mitochondria.')],
    why=[('Explain why embryonic stem cells are considered more useful in research than adult stem cells.', 'Embryonic stem cells are pluripotent – they can become almost any cell type – whereas adult stem cells can usually only form a few related types (e.g. blood cells).'),
         ('Explain why a patient may reject stem cells from a donor.', 'The donor cells have different antigens on their surface, so the patient’s immune system recognises them as foreign and attacks them; matching or using the patient’s own cells reduces rejection.'),
         ('Explain why all cells in a body contain the same genes but are specialised differently.', 'During differentiation different genes are switched on or off in different cells, so each type makes different proteins and develops a different structure.'),
         ('Explain why gardeners can grow a whole new plant from a small cutting.', 'Meristem cells in the cutting are undifferentiated and can divide by mitosis and differentiate into all the tissues of a new plant, which is a clone of the parent.')],
    contrast=[('an embryonic stem cell', 'an adult stem cell', 'Embryonic stem cells come from early embryos and can form almost any cell type; adult stem cells are found in some tissues (e.g. bone marrow) and form only a limited range.'),
              ('a stem cell', 'a specialised cell', 'A stem cell is undifferentiated and can divide and become different cell types; a specialised cell has differentiated, has a structure for one function and usually divides rarely.')],
    misc=[('Stem cells can only be found in embryos.', 'Adults have stem cells too, e.g. in bone marrow, skin and the gut lining, though they form a narrower range of cells.'),
          ('Specialised cells have lost the genes they do not use.', 'They keep all their genes; unused genes are switched off, not removed.'),
          ('Animal cells can differentiate throughout life just like plant cells.', 'Most animal cells differentiate early and lose this ability; plant meristem cells can differentiate throughout life.')],
    cases=[('induced pluripotent stem cells (iPS cells) discovered by Shinya Yamanaka in 2006', 'Adult skin cells were reprogrammed with four genes to behave like embryonic stem cells; Yamanaka won the 2012 Nobel Prize.', 'differentiation being reversible by switching genes on', 'Switching on specific genes returned specialised cells to an undifferentiated state, avoiding the need for embryos.'),
           ('bone marrow transplants for children with leukaemia', 'Healthy stem cells from a matched donor are infused into the patient after chemotherapy destroys the cancerous marrow.', 'the medical use of adult stem cells', 'The donor stem cells divide and differentiate into healthy red cells, white cells and platelets.'),
           ('tissue culture of orchids and bananas', 'Growers take tiny pieces of meristem and grow thousands of identical plants on sterile agar with plant hormones.', 'plant stem cells and cloning', 'Meristem cells divide by mitosis and differentiate into whole plants that are clones of the parent.')],
    evaluate=[('Research using human embryonic stem cells should be allowed.', ['could treat diseases such as type 1 diabetes, Parkinson’s and spinal injury', 'embryos used are often spare ones from IVF that would be destroyed'], ['some people believe an embryo has a right to life from conception', 'risk of transplanted cells forming tumours or being contaminated', 'iPS cells may give similar benefits without embryos'], 'Many countries allow it under strict regulation (e.g. up to 14 days, licensed labs); the judgement depends on beliefs about the moral status of the embryo, balanced against potential cures.'),
              ('Unlicensed “stem cell clinics” that sell treatments to the public should be banned.', ['treatments are often unproven and some patients have been harmed (e.g. blindness after eye injections)', 'they exploit desperate patients for high fees'], ['patients have a right to choose treatments', 'banning may push clinics to other countries'], 'Strong regulation and clinical trials protect patients; unproven treatments should not be sold.')],
    extended=[('Outline how stem cells could be used to treat type 1 diabetes and evaluate two problems that must be solved first.', 'Stem cells are grown and treated so they differentiate into insulin-secreting beta cells, then transplanted into the pancreas/liver. Problems: rejection by the immune system (and in type 1 diabetes the body attacks beta cells again); risk of uncontrolled division forming tumours; ethical issues if embryos used; cost.', 6, 'long')],
))

dataset('ch01-st4',
        dict(intro='{who} grew cauliflower tissue-culture explants on agar containing different concentrations of plant hormone and measured the number of shoots formed after 4 weeks.', iv=('Hormone concentration', 'mg/dm³'), xs=[0.0, 0.5, 1.0, 1.5, 2.0],
             dv=('Number of shoots', 'shoots per explant'), f=lambda x: 2 + 5 * x, dp=0, trend='The number of shoots per explant increases as the hormone concentration increases.',
             why='The hormone stimulates meristem (stem) cells to divide by mitosis and differentiate into shoot tissue.'))

inquiry('ch01-st4',
        dict(ctx='how the length of a cauliflower explant affects the number of new shoots that grow from it in tissue culture',
             iv='length of explant (mm)', dv='number of new shoots counted after 4 weeks',
             cvs=[('composition and volume of the agar', 'nutrients and hormones affect growth'), ('temperature and light', 'affect rate of growth'), ('sterility of equipment', 'microbes compete with or kill the explants'), ('part of the cauliflower used', 'different tissues contain different amounts of meristem')],
             hyp='If the explant is longer, then more shoots will form, because it contains more meristem cells that can divide and differentiate.',
             method='Sterilise cauliflower florets in dilute bleach, rinse in sterile water; cut explants of 2, 4, 6, 8, 10 mm; place 5 of each length on sterile hormone agar in sealed tubes; incubate at 25 °C in light for 4 weeks; count shoots and calculate the mean per length.',
             weak=('the scalpel and forceps were not sterilised between explants', 'flame or dip tools in ethanol between cuts so explants are not contaminated by bacteria and fungi'),
             safety='bleach is corrosive – gloves and eye protection; ethanol is flammable'))


# =============================================================================================
# ch02 Genetics and Inheritance
# =============================================================================================
# (organism, letter, dominant phenotype, recessive phenotype)
TRAITS = [('pea plants', 'T', 'tall', 'dwarf'), ('pea plants', 'R', 'round seeds', 'wrinkled seeds'), ('guinea pigs', 'B', 'black fur', 'white fur'),
          ('tomato plants', 'R', 'red fruit', 'yellow fruit'), ('fruit flies', 'G', 'normal wings', 'vestigial wings'), ('cats', 'S', 'short hair', 'long hair'),
          ('maize', 'P', 'purple kernels', 'yellow kernels'), ('rabbits', 'B', 'brown fur', 'white fur'), ('Labrador dogs', 'B', 'black coat', 'brown (chocolate) coat'),
          ('humans', 'F', 'unaffected (no cystic fibrosis)', 'cystic fibrosis'), ('sunflowers', 'Y', 'yellow petals', 'red petals'), ('cattle', 'H', 'hornless (polled)', 'horned')]


def _cross(p1, p2):
    kids = [''.join(sorted(a + b)) for a in p1 for b in p2]
    return kids  # 4 equally likely genotypes ('Tt' sorted puts upper first)


def _geno(letter, n_dom):
    return {2: letter * 2, 1: letter + letter.lower(), 0: letter.lower() * 2}[n_dom]


R.facts('ch02-st1', F(
    terms=[('allele', 'one of two or more alternative forms of a gene, found at the same position on homologous chromosomes'),
           ('genotype', 'the combination of alleles an organism has for a gene, e.g. Bb'),
           ('phenotype', 'the observable characteristics of an organism, resulting from its genotype and the environment'),
           ('dominant allele', 'an allele that is expressed in the phenotype even if only one copy is present (written with a capital letter)'),
           ('recessive allele', 'an allele that is expressed only when two copies are present, i.e. no dominant allele (written with a lower-case letter)'),
           ('homozygous', 'having two identical alleles of a gene, e.g. BB or bb'),
           ('heterozygous', 'having two different alleles of a gene, e.g. Bb'),
           ('codominance', 'when both alleles in a heterozygote are fully expressed in the phenotype, e.g. AB blood group')],
    facts=[('A pea plant has the genotype Tt, where T (tall) is dominant. What is its phenotype?', 'Tall', ['Dwarf', 'Medium height', 'Half tall, half dwarf'], 'One dominant allele is enough for the tall phenotype.'),
           ('Which term describes the genotype rr?', 'Homozygous recessive', ['Homozygous dominant', 'Heterozygous', 'Codominant'], 'Two copies of the recessive allele.'),
           ('A person with blood group AB has which genotype?', 'IᴬIᴮ', ['IᴬIᴬ', 'IᴬIᴼ', 'IᴮIᴼ'], 'Iᴬ and Iᴮ are codominant, so both are expressed.'),
           ('Which statement about a heterozygous organism is correct?', 'It has two different alleles for the gene', ['It shows the recessive phenotype', 'It has two identical dominant alleles', 'It has only one allele for the gene'], 'Hetero = different.')],
    why=[('Explain why two parents with brown eyes can have a child with blue eyes (treat eye colour as a single gene with brown dominant).', 'Both parents can be heterozygous (Bb); each can pass on the recessive allele b, so there is a 1 in 4 chance of a bb (blue-eyed) child.'),
         ('Explain why an organism with the dominant phenotype may have one of two genotypes.', 'A dominant allele is expressed with one copy, so both the homozygous (BB) and the heterozygous (Bb) genotype show the same phenotype.'),
         ('Explain why identical twins raised apart can still differ in phenotype.', 'They have identical genotypes, but phenotype also depends on the environment (diet, exercise, sunlight), so features such as body mass or skin tone can differ.'),
         ('Explain what a test cross is and why it is used.', 'An organism with the dominant phenotype is crossed with a homozygous recessive one; if any offspring show the recessive phenotype the unknown parent must be heterozygous, otherwise it is probably homozygous dominant.')],
    contrast=[('genotype', 'phenotype', 'Genotype is the set of alleles (e.g. Tt); phenotype is the characteristic that is seen (e.g. tall), produced by the genotype interacting with the environment.'),
              ('homozygous', 'heterozygous', 'Homozygous means two identical alleles (TT or tt); heterozygous means two different alleles (Tt).'),
              ('dominance', 'codominance', 'With complete dominance only the dominant allele shows in a heterozygote; with codominance both alleles are expressed (e.g. IᴬIᴮ gives blood group AB).')],
    misc=[('A dominant allele is always the most common allele in a population.', 'Dominance describes expression in a heterozygote, not frequency; e.g. the allele for Huntington’s disease is dominant but rare.'),
          ('Recessive alleles are weaker and eventually disappear from a population.', 'Recessive alleles can persist hidden in heterozygous carriers for many generations.'),
          ('An organism with genotype Bb has two genes for fur colour.', 'It has one gene for fur colour with two different alleles (versions) of that gene.')],
    cases=[('Gregor Mendel’s pea-plant experiments in Brno (1856-1863)', 'Crossing true-breeding tall and dwarf plants gave all-tall offspring; self-crossing these gave a 3 : 1 ratio of tall to dwarf.', 'dominant and recessive alleles', 'The dwarf trait disappeared in the first generation and reappeared in the second, showing the recessive allele was present but hidden in heterozygotes.'),
           ('ABO blood groups in transfusion', 'People with group O have genotype IᴼIᴼ; group AB people are IᴬIᴮ and show both antigens.', 'codominance and recessive alleles', 'Iᴬ and Iᴮ are codominant with each other and both dominant over Iᴼ, which explains the four blood groups.')],
    evaluate=[('Knowing a person’s genotype tells you everything about their phenotype.', ['some single-gene traits (e.g. ABO blood group, cystic fibrosis) are determined by genotype', 'genotype sets the possible range of features'], ['many traits are polygenic and influenced by environment (height, skin colour, intelligence)', 'gene expression can be switched on or off by environmental factors'], 'Genotype is important but phenotype usually results from genotype interacting with the environment, so the claim is only true for a few single-gene characteristics.')],
))


@R.add('ch02-st1', 'C1', (1, 3), 'mcq')
def geno_mcq(rng, slot):
    org, L, dom, rec = rng.choice(TRAITS)
    l = L.lower()
    k = rng.choice(['het', 'rec', 'test', 'homdom'])
    if k == 'het':
        return mcq(rng, f'In {org}, the allele for {dom} ({L}) is dominant to the allele for {rec} ({l}). Which statement describes an individual with genotype {L}{l}?', f'Heterozygous, with the phenotype {dom}',
                   [f'Heterozygous, with the phenotype {rec}', f'Homozygous, with the phenotype {dom}', f'Homozygous, with the phenotype {rec}'], f'{L}{l} has two different alleles; the dominant allele {L} is expressed.')
    if k == 'homdom':
        return mcq(rng, f'In {org}, {dom} ({L}) is dominant to {rec} ({l}). Which statement describes an individual with genotype {L}{L}?', f'Homozygous dominant, with the phenotype {dom}',
                   [f'Heterozygous, with the phenotype {dom}', f'Homozygous recessive, with the phenotype {rec}', f'Homozygous dominant, with the phenotype {rec}'], 'Two identical dominant alleles.')
    if k == 'rec':
        return mcq(rng, f'In {org}, {dom} ({L}) is dominant to {rec} ({l}). What is the phenotype of an individual with genotype {l}{l}?', rec[0].upper() + rec[1:],
                   [dom[0].upper() + dom[1:], 'Intermediate between the two', 'It cannot be predicted from the genotype'], 'The recessive phenotype needs two recessive alleles.')
    return mcq(rng, f'In {org}, {dom} ({L}) is dominant to {rec} ({l}). An individual with {dom} is crossed with one with {rec}; some offspring show {rec}. What is the genotype of the {dom} parent?', 'Heterozygous',
               ['Homozygous dominant', 'Homozygous recessive', 'It could be either homozygous or heterozygous'], f'A {l}{l} offspring needs an {l} allele from each parent, so the {dom} parent must be {L}{l}.')


inquiry('ch02-st1',
        dict(ctx='whether the light intensity seedlings are grown in affects the proportion of albino (white) maize seedlings from a heterozygous cross',
             iv='light intensity (lux, set by distance from a lamp)', dv='number of green and white seedlings counted after 10 days, expressed as a percentage',
             cvs=[('number of seeds per tray (e.g. 100)', 'a larger sample gives a reliable ratio'), ('temperature', 'affects germination rate'), ('water supply', 'affects germination and growth'), ('source of seed (same heterozygous cross)', 'different crosses give different ratios')],
             hyp='If light intensity is changed, then the percentage of white seedlings will stay at about 25%, because albinism is caused by the genotype aa (from a cross Aa × Aa) and the light only affects how green the green seedlings become.',
             method='Sow 100 seeds from an Aa × Aa cross in each of five trays at 10, 20, 40, 60 and 80 cm from a 60 W LED lamp; keep at 22 °C and water 100 cm³ every 2 days; after 10 days count green and white seedlings; repeat with three trays per light level; calculate the mean percentage white and compare with the expected 25%.',
             weak=('only 12 seeds were sown in each tray', 'sow at least 100 seeds per tray: genetic ratios are probabilities, so small samples can differ greatly from 3 : 1 by chance'),
             safety='lamps get hot – keep water away from electrical sockets'))

R.facts('ch02-st2', F(
    terms=[('Punnett square', 'a grid used to show all possible combinations of parental gametes and predict the probability of offspring genotypes'),
           ('monohybrid cross', 'a genetic cross that follows the inheritance of a single gene'),
           ('F1 generation', 'the first generation of offspring from a cross between two parents'),
           ('true-breeding', 'homozygous for a characteristic, so all offspring from self-crossing show the same phenotype'),
           ('test cross', 'crossing an individual of unknown genotype with a homozygous recessive individual to reveal its genotype')],
    facts=[('What ratio of phenotypes is expected from a cross between two heterozygous pea plants (Tt × Tt), with tall dominant?', '3 tall : 1 dwarf', ['1 tall : 1 dwarf', 'All tall', '1 tall : 2 medium : 1 dwarf'], 'TT, Tt, Tt are tall and tt is dwarf.'),
           ('What proportion of offspring from Bb × bb are expected to be bb?', '50%', ['25%', '75%', '0%'], 'Gametes B, b × b, b give Bb, Bb, bb, bb.'),
           ('A cross between TT and tt plants gives what F1 offspring?', 'All heterozygous and tall', ['All homozygous dominant and tall', 'Half tall and half dwarf', '3 tall : 1 dwarf'], 'Every gamete from TT is T and every gamete from tt is t, so all offspring are Tt.')],
    why=[('Explain why the ratios predicted by a Punnett square are rarely obtained exactly in real crosses.', 'Each fertilisation is a random event, so the ratios are probabilities; with small numbers of offspring chance variation means the observed ratio differs from the expected ratio – larger samples come closer.'),
         ('Explain why each gamete carries only one allele of each gene.', 'In meiosis homologous chromosomes separate, so each haploid gamete receives one chromosome of each pair and therefore one allele of each gene.'),
         ('Explain why a 3 : 1 phenotype ratio suggests that both parents are heterozygous.', 'Only Aa × Aa produces the genotypes AA, Aa, Aa, aa in a 1 : 2 : 1 ratio, giving 3 dominant : 1 recessive phenotypes.')],
    misc=[('If two Tt plants have four offspring, exactly three will be tall and one will be dwarf.', 'The 3 : 1 ratio is a probability for each offspring (75% tall); four offspring could be any combination by chance.'),
          ('Two heterozygous parents already have three tall children, so the next child must be dwarf.', 'Each fertilisation is independent; the probability of a dwarf child is still 1/4.'),
          ('In a Punnett square the alleles of one parent are written along both sides.', 'One parent’s gametes go along the top and the other parent’s gametes down the side.')],
    evaluate=[('Punnett squares are a reliable way for families to predict inherited disorders.', ['they give accurate probabilities for single-gene disorders such as cystic fibrosis', 'they help genetic counsellors explain risk'], ['they give probabilities, not certainties, for each child', 'many conditions are polygenic or affected by environment', 'parents’ genotypes may be unknown without testing'], 'Useful for single-gene conditions where the parents’ genotypes are known, but limited as a general prediction tool.')],
))


@R.add('ch02-st2', 'C3', (1, 5), 'numerical')
def punnett(rng, slot):
    org, L, dom, rec = rng.choice(TRAITS)
    l = L.lower()
    pairs = [(1, 1), (1, 0), (2, 0), (2, 1)]
    a, b = rng.choice(pairs)
    p1, p2 = _geno(L, a), _geno(L, b)
    kids = _cross(p1, p2)
    n_rec = sum(1 for k in kids if k == l + l)
    n_dom = 4 - n_rec
    gens = {}
    for k in kids:
        gens[k] = gens.get(k, 0) + 1
    gtxt = ' : '.join(f'{v} {k}' for k, v in sorted(gens.items()))
    ptxt = f'all {dom}' if n_rec == 0 else f'{n_dom} {dom} : {n_rec} {rec}' if n_dom else f'all {rec}'
    if len(gens) == 1:
        gtxt = f'all {kids[0]}'
    who = name(rng)
    frames = ['ratio', 'prob', 'number']
    k = rng.choice(frames if slot.d >= 2 else ['ratio'])
    grid = f'Gametes {p1[0]}, {p1[1]} × {p2[0]}, {p2[1]}; offspring {", ".join(kids)}'
    if k == 'ratio':
        return dict(stem=f'In {org}, the allele for {dom} ({L}) is dominant to the allele for {rec} ({l}). An individual with genotype {p1} is crossed with one with genotype {p2}. Use a Punnett square to give the expected genotype ratio and phenotype ratio of the offspring.',
                    answer=f'Genotypes {gtxt}; phenotypes {ptxt}', markingKey=f'1 correct gametes; 1 Punnett square ({grid}); 1 genotype ratio {gtxt}; 1 phenotype ratio {ptxt}.', marks=4)
    if k == 'prob':
        return dict(stem=f'{who} crosses two {org}: genotypes {p1} and {p2} ({L} = {dom}, dominant; {l} = {rec}). What is the probability that one offspring has the phenotype {rec}? Give your answer as a fraction and a percentage.',
                    answer=f'{n_rec}/4 = {n_rec * 25}%', markingKey=f'M1 Punnett square: {grid}; A1 {n_rec}/4 = {n_rec * 25}%.', marks=2)
    N = rng.choice([40, 60, 80, 120, 200, 360, 480])
    exp = N * n_dom // 4
    return dict(stem=f'A breeder crosses {p1} and {p2} {org} and obtains {N} offspring ({L}: {dom}, dominant; {l}: {rec}). Predict how many offspring are expected to be {dom}.',
                answer=f'{exp}', markingKey=f'M1 proportion {dom} = {n_dom}/4 from Punnett square ({grid}); A1 {n_dom}/4 × {N} = {exp}.', marks=3)


@R.add('ch02-st2', 'C4', (2, 5), 'multi_step')
def chi_obs(rng, slot):
    org, L, dom, rec = rng.choice(TRAITS[:9])
    l = L.lower()
    N = rng.choice([400, 480, 560, 640, 800, 1000])
    cross = rng.choice(['het', 'test'])
    p = 0.75 if cross == 'het' else 0.5
    dom_n = round(N * p * rng.uniform(0.96, 1.04))
    rec_n = N - dom_n
    ratio = dom_n / rec_n
    exp = '3 : 1' if cross == 'het' else '1 : 1'
    par = f'{L}{l} × {L}{l}' if cross == 'het' else f'{L}{l} × {l}{l}'
    return dict(stem=f'A cross between two {org} gave {dom_n} offspring with {dom} and {rec_n} with {rec}. ({L}, {dom}, is dominant.) (a) Calculate the ratio of {dom} to {rec} offspring to 2 decimal places (as x : 1). (b) Deduce the most likely genotypes of the parents and justify your answer with a Punnett square. (c) Explain why the observed ratio is not exactly the expected ratio.',
                answer=f'(a) {ratio:.2f} : 1 (b) {par}, expected {exp} (c) fertilisation is random, so observed numbers vary by chance around the expected ratio',
                markingKey=f'(a) M1 {dom_n} ÷ {rec_n}; A1 {ratio:.2f} : 1. (b) 1 closest to {exp}; 1 parents {par} with correct Punnett square. (c) 1 random fusion of gametes / chance; sample size.', marks=5, gap='G5')


inquiry('ch02-st2',
        dict(ctx='whether drawing coloured beads from two bags (to model gametes from two heterozygous parents) gives a ratio closer to 3 : 1 as the number of draws increases',
             iv='number of pairs of beads drawn (10, 20, 50, 100, 200)', dv='ratio of “dominant” to “recessive” phenotypes – counted from the bead pairs and calculated as x : 1',
             cvs=[('number of each colour in each bag (equal numbers)', 'models a heterozygous parent producing 50% of each gamete'), ('replacing beads after each draw', 'keeps the probability of each allele at 0.5'), ('drawing without looking', 'keeps the selection random')],
             hyp='If more pairs are drawn, then the ratio will get closer to 3 : 1, because each draw is a random event and the effect of chance variation decreases with larger samples.',
             method='Put 50 red (A) and 50 white (a) beads in each of two bags; draw one bead from each bag without looking, record the pair, replace; do 10, 20, 50, 100 and 200 draws; count AA/Aa (dominant) and aa; calculate the ratio and percentage difference from 3 : 1; repeat each sample size three times.',
             weak=('the beads were not put back into the bag after each draw', 'replace each bead after recording so the probability of drawing each allele stays at 0.5 for every draw'),
             safety='pick up any spilled beads to avoid slipping'))

R.facts('ch02-st3', F(
    terms=[('sex chromosomes', 'the pair of chromosomes that determines sex: XX in human females and XY in human males'),
           ('sex-linked characteristic', 'a characteristic controlled by a gene carried on a sex chromosome, usually the X chromosome'),
           ('carrier', 'a person who has one recessive allele for a disorder but does not show it, and can pass it on'),
           ('autosome', 'any chromosome that is not a sex chromosome; humans have 22 pairs')],
    facts=[('Which parent determines the sex of a human baby?', 'The father, because sperm carry either an X or a Y chromosome', ['The mother, because eggs carry X or Y', 'Both parents equally', 'Neither – it depends on temperature'], 'All eggs carry X; half of sperm carry X and half carry Y.'),
           ('What is the probability that a human baby will be a boy?', '0.5', ['0.25', '0.75', '1.0'], 'XX × XY gives XX, XX, XY, XY.'),
           ('Why are sex-linked recessive disorders such as haemophilia more common in males?', 'Males have only one X chromosome, so one recessive allele is expressed', ['Males have two X chromosomes', 'The Y chromosome carries the dominant allele', 'Females cannot inherit X-linked alleles'], 'There is no second X in a male to carry a dominant allele.'),
           ('Which of these is a sex-linked condition in humans?', 'Red-green colour blindness', ['Cystic fibrosis', 'Sickle-cell anaemia', 'Huntington’s disease'], 'The genes for red and green cone pigments are on the X chromosome.')],
    why=[('Explain why a colour-blind man cannot pass colour blindness to his son.', 'A father passes his Y chromosome to his sons, not his X; the colour-blindness allele is on the X chromosome, so sons inherit the X from their mother.'),
         ('Explain why a woman can be a carrier of haemophilia but a man cannot.', 'A woman has two X chromosomes so a dominant normal allele can mask one recessive allele (XᴴXʰ); a man has one X, so if it carries Xʰ he has haemophilia.'),
         ('Explain why, in some reptiles, the sex of offspring is not determined by chromosomes.', 'In many turtles and crocodiles the incubation temperature of the egg determines sex (temperature-dependent sex determination), so warming climates can skew sex ratios.')],
    contrast=[('a sex chromosome', 'an autosome', 'Sex chromosomes (X and Y) determine sex and differ between males and females; autosomes are the other 22 pairs, the same in both sexes.'),
              ('a carrier', 'an affected individual', 'A carrier has one recessive allele masked by a dominant one and shows no symptoms; an affected individual expresses the disorder.')],
    misc=[('Boys get their X chromosome from their father.', 'Boys get their Y from their father and their X from their mother.'),
          ('Haemophilia only affects males because the allele is on the Y chromosome.', 'The allele is on the X chromosome; females can be affected (XʰXʰ) but it is rare.'),
          ('After three girls, a couple is more likely to have a boy next time.', 'Each pregnancy is independent; the probability of a boy is still about 0.5.')],
    cases=[('haemophilia in Queen Victoria’s descendants', 'Queen Victoria was a carrier; her son Leopold had haemophilia and two daughters were carriers who passed it into the Spanish and Russian royal families.', 'X-linked recessive inheritance', 'Carrier females passed Xʰ to about half their sons (affected) and half their daughters (carriers), while no male in the line passed it to a son.')],
    evaluate=[('Parents should be allowed to choose the sex of their baby using IVF and embryo testing.', ['can avoid serious sex-linked disorders such as Duchenne muscular dystrophy', 'reproductive freedom'], ['could unbalance sex ratios in societies with a son preference', 'treats children as products; slippery slope to designer babies', 'IVF is expensive and has health risks'], 'Many countries allow selection only to avoid serious sex-linked disease, not for social reasons; this balances health benefits with social risks.')],
))


@R.add('ch02-st3', 'C3', (1, 5), 'numerical')
def xlinked(rng, slot):
    dis, L = rng.choice([('red-green colour blindness', 'B'), ('haemophilia A', 'H'), ('Duchenne muscular dystrophy', 'D')])
    l = L.lower()
    mum = rng.choice([f'X{L}X{l}', f'X{L}X{L}', f'X{l}X{l}'])
    dad = rng.choice([f'X{L}Y', f'X{l}Y'])
    if dis.startswith('Duchenne') and (dad == f'X{l}Y' or mum == f'X{l}X{l}'):
        mum, dad = f'X{L}X{l}', f'X{L}Y'
    m_g = [mum[:2], mum[2:]]
    d_g = [dad[:2], 'Y']
    kids = [(a, b) for a in m_g for b in d_g]
    sons = [a for a, b in kids if b == 'Y']
    daughters = [(a, b) for a, b in kids if b != 'Y']
    aff_sons = sum(1 for a in sons if a == f'X{l}')
    aff_d = sum(1 for a, b in daughters if a == f'X{l}' and b == f'X{l}')
    car_d = sum(1 for a, b in daughters if (a == f'X{l}') != (b == f'X{l}'))
    p_aff = (aff_sons + aff_d) / 4
    k = rng.choice(['child', 'son', 'carrier'])
    if k == 'child' or slot.d <= 2:
        return dict(stem=f'{dis[0].upper() + dis[1:]} is caused by a recessive allele (X{l}) on the X chromosome. A mother with genotype {mum} and a father with genotype {dad} have a child. Calculate the probability that the child will have {dis}.',
                    answer=f'{int(p_aff * 4)}/4 = {p_aff * 100:g}%', markingKey=f'1 gametes {m_g[0]}, {m_g[1]} and {d_g[0]}, Y; 1 Punnett square: {", ".join(a + b for a, b in kids)}; 1 probability {p_aff * 100:g}%.', marks=3)
    if k == 'son':
        return dict(stem=f'For {dis} (recessive allele X{l}), parents with genotypes {mum} and {dad} are expecting a son. What is the probability that he will be affected?',
                    answer=f'{aff_sons}/2 = {aff_sons * 50}%', markingKey=f'1 a son receives Y from the father and one X from the mother ({m_g[0]} or {m_g[1]}); 1 probability {aff_sons}/2 = {aff_sons * 50}%.', marks=2)
    return dict(stem=f'A couple with genotypes {mum} (mother) and {dad} (father) are concerned about {dis}, an X-linked recessive condition. Using a Punnett square, state the probability that a daughter will be (a) a carrier and (b) affected.',
                answer=f'(a) {car_d}/2 = {car_d * 50}% (b) {aff_d}/2 = {aff_d * 50}%', markingKey=f'1 correct gametes; 1 correct square: {", ".join(a + b for a, b in kids)}; 1 carriers {car_d * 50}%; 1 affected {aff_d * 50}% (of daughters).', marks=4)


dataset('ch02-st3',
        dict(intro='In a survey of students at schools in {who}’s city, the number of colour-blind students per 1000 was recorded for boys in different year groups (Ishihara test).', iv=('Year group', ''), xs=[7, 8, 9, 10, 11],
             dv=('Colour-blind boys', 'per 1000'), f=lambda x: 80, dp=0, trend='The frequency stays roughly constant (about 70-90 per 1000 boys) across all year groups – there is no trend with age.',
             why='Red-green colour blindness is inherited (X-linked recessive), not developed with age, so the frequency depends on allele frequency in the population, about 8% of boys.'))

inquiry('ch02-st3',
        dict(ctx='how the incubation temperature of eggs affects the percentage of female hatchlings in a species of turtle (using published data from a conservation project)',
             iv='incubation temperature (°C)', dv='percentage of hatchlings that are female – sexed by the conservation team',
             cvs=[('species of turtle', 'different species have different pivotal temperatures'), ('humidity of the sand/incubator', 'affects embryo development'), ('number of eggs per temperature', 'larger samples are more reliable'), ('time the eggs spend at the temperature', 'sex is set during a sensitive middle period of incubation')],
             hyp='If incubation temperature increases above about 29 °C, then the percentage of females will increase, because in sea turtles warmer temperatures during the middle third of incubation cause embryos to develop as females.',
             method='Use data from a hatchery: incubators set at 26, 27, 28, 29, 30, 31 °C with 30 eggs each from the same species, all at 80% humidity; record hatchling sex; repeat over three nesting seasons; plot % female against temperature and find the pivotal temperature (50% female).',
             weak=('eggs at different temperatures came from different beaches and species', 'use eggs from the same species and population, randomly allocated to each temperature'),
             safety='follow conservation permits and handle eggs gently and minimally'))

R.facts('ch02-st4', F(
    terms=[('pedigree chart', 'a family-tree diagram that shows how a characteristic or disorder is inherited over several generations'),
           ('inherited disorder', 'a condition caused by a faulty allele that is passed from parents to offspring'),
           ('cystic fibrosis', 'an autosomal recessive disorder of cell membranes that causes thick, sticky mucus in the lungs and digestive system'),
           ('Huntington’s disease', 'an autosomal dominant disorder causing progressive breakdown of nerve cells in the brain, usually from middle age'),
           ('genetic screening', 'testing people or embryos for alleles that cause inherited disorders')],
    facts=[('In a pedigree chart, what does a shaded square usually represent?', 'An affected male', ['An unaffected female', 'A carrier female', 'An unaffected male'], 'Squares are males, circles are females; shading shows the trait.'),
           ('Two unaffected parents have an affected child. What does this show about the allele?', 'It is recessive and both parents are carriers', ['It is dominant', 'It is on the Y chromosome', 'It was caused by the environment'], 'The allele was hidden in both heterozygous parents.'),
           ('Polydactyly (extra fingers or toes) is caused by a dominant allele. A heterozygous father and a homozygous recessive mother have a child. What is the probability that the child has polydactyly?', '50%', ['25%', '75%', '100%'], 'Dd × dd gives Dd, Dd, dd, dd.'),
           ('Which disorder is caused by a recessive allele of the CFTR gene?', 'Cystic fibrosis', ['Huntington’s disease', 'Polydactyly', 'Haemophilia'], 'CF is autosomal recessive.')],
    why=[('Explain how a pedigree chart can show that a disorder is caused by a dominant allele.', 'If every affected person has at least one affected parent, and two affected parents can have an unaffected child, the allele must be dominant (both parents heterozygous, child homozygous recessive).'),
         ('Explain why Huntington’s disease can be passed on even though it is caused by a dominant allele.', 'Symptoms usually appear at 35-45 years, often after the person has had children, so the allele is passed on before the person knows they have it.'),
         ('Explain why marriages between close relatives increase the chance of children with recessive disorders.', 'Relatives share many alleles from common ancestors, so both are more likely to carry the same rare recessive allele, increasing the chance of a homozygous recessive child.')],
    contrast=[('an autosomal recessive disorder', 'an autosomal dominant disorder', 'A recessive disorder appears only in homozygous recessive people and can skip generations through carriers; a dominant disorder appears with one allele and every affected person has an affected parent.')],
    misc=[('Cystic fibrosis is caused by bacteria in the lungs, so it can be caught.', 'CF is an inherited disorder caused by a recessive allele; lung infections are a consequence of the thick mucus, not the cause.'),
          ('A disorder that skips a generation in a pedigree must be dominant.', 'Skipping generations is typical of recessive alleles hidden in carriers.'),
          ('If one parent has a dominant disorder, all the children will have it.', 'If that parent is heterozygous, each child has a 50% chance.')],
    cases=[('Tay-Sachs screening in Ashkenazi Jewish communities (Dor Yeshorim programme)', 'Young people are tested for carrier status; carrier couples are advised before marriage, and the number of affected births has fallen by over 90%.', 'genetic screening for a recessive disorder', 'Only carrier × carrier couples have a 1 in 4 risk, so identifying carriers before having children prevents most cases.'),
           ('Huntington’s disease in families around Lake Maracaibo, Venezuela', 'Very large families with many affected members allowed researchers to map the HTT gene to chromosome 4 in 1983.', 'dominant inheritance shown in a pedigree', 'Affected people appeared in every generation and each child of an affected parent had about a 50% chance of developing the disease.')],
    sources=[('Generation I: an unaffected man (1) and an unaffected woman (2). Generation II: their children – an affected daughter (3), an unaffected son (4) and an unaffected daughter (5). The affected daughter has cystic fibrosis.', 'Pedigree description', 'Deduce the genotypes of individuals 1, 2 and 3 (F = normal, f = cystic fibrosis) and state the probability that individual 5 is a carrier.', '1 and 2 must be Ff (unaffected parents of an ff child); 3 is ff; 5 is FF or Ff, unaffected, so the probability she is a carrier is 2/3.')],
    evaluate=[('All newborn babies should be screened for inherited disorders.', ['early treatment improves outcomes (e.g. diet for PKU, physiotherapy for CF)', 'relatively cheap heel-prick test', 'parents learn their carrier status for future pregnancies'], ['false positives cause anxiety', 'some disorders have no treatment', 'genetic data privacy', 'cost to health services'], 'Screening for treatable disorders is widely justified; screening for untreatable ones raises more ethical questions.'),
              ('Embryos created by IVF should be screened so that only those without inherited disorders are implanted.', ['prevents suffering from serious disorders', 'carrier couples can have healthy children'], ['destroys embryos, which some consider wrong', 'could lead to selection for non-medical traits', 'expensive and not available to all'], 'Pre-implantation genetic diagnosis for serious disorders is accepted in many countries under regulation; selection for other traits is not.')],
))


@R.add('ch02-st4', 'C3', (2, 5), 'numerical')
def pedigree_prob(rng, slot):
    dis, kind, L = rng.choice([('cystic fibrosis', 'rec', 'F'), ('phenylketonuria (PKU)', 'rec', 'P'), ('sickle-cell anaemia', 'rec', 'A'), ('Huntington’s disease', 'dom', 'H'), ('polydactyly', 'dom', 'D'), ('achondroplasia', 'dom', 'A')])
    l = L.lower()
    who1, who2 = two_names(rng)
    if kind == 'rec':
        frame = rng.choice(['both', 'one'])
        if frame == 'both':
            return dict(stem=f'{who1} and {who2} do not have {dis}, but their first child does. {dis[0].upper() + dis[1:]} is caused by a recessive allele. (a) State the genotypes of both parents. (b) What is the probability that their next child will have {dis}? (c) What is the probability that an unaffected child of theirs is a carrier?',
                        answer=f'(a) both {L}{l} (b) 1/4 (c) 2/3', markingKey=f'(a) 1 both {L}{l}: they are unaffected but passed on {l}. (b) 1 Punnett {L}{L}, {L}{l}, {L}{l}, {l}{l}: 1/4. (c) 1 of the three unaffected genotypes, two are {L}{l}: 2/3.', marks=4)
        return dict(stem=f'{who1} has {dis} (a recessive disorder). {who2} is a carrier. What is the probability that their child will have {dis}?',
                    answer='1/2 (50%)', markingKey=f'1 genotypes {l}{l} × {L}{l}; 1 offspring {L}{l}, {L}{l}, {l}{l}, {l}{l}; 1 probability 1/2.', marks=3)
    return dict(stem=f'{who1} is heterozygous for {dis}, which is caused by a dominant allele ({L}). {who2} is unaffected. (a) State both genotypes. (b) Calculate the probability that their first two children will both be unaffected.',
                answer=f'(a) {L}{l} and {l}{l} (b) 1/2 × 1/2 = 1/4', markingKey=f'(a) 1 {L}{l}; 1 {l}{l}. (b) M1 each child 1/2 unaffected; A1 independent events multiply: 1/4.', marks=4)


dataset('ch02-st4',
        dict(intro='A newborn screening programme in {who}’s region recorded the number of babies diagnosed with cystic fibrosis per 100 000 births in five years after screening began.', iv=('Year after screening began', ''), xs=[1, 2, 3, 4, 5],
             dv=('Diagnoses', 'per 100 000 births'), f=lambda x: 40, dp=0, trend='The number of diagnoses stays approximately constant from year to year.',
             why='CF is inherited; screening detects affected babies earlier but does not change how many are born, because carrier frequency in the population stays the same.'))

inquiry('ch02-st4',
        dict(ctx='how the number of generations included in a family pedigree affects how confidently a disorder can be identified as dominant or recessive (using pedigree data from a genetic counselling database)',
             iv='number of generations included (2, 3, 4, 5)', dv='percentage of pedigrees correctly classified as dominant or recessive by a panel of students',
             cvs=[('number of family members per generation', 'larger families show more patterns'), ('the disorders used', 'some patterns are clearer than others'), ('students’ training before the task', 'experience affects accuracy')],
             hyp='If more generations are included, then a higher percentage will be correctly classified, because recessive disorders can skip generations and more generations make the pattern clearer.',
             method='Prepare 20 anonymised pedigrees per number of generations for known dominant and recessive disorders; give them to 30 students after the same 10-minute briefing; record correct classifications; calculate percentage correct for each number of generations.',
             safety='use anonymised data only to protect family privacy'))

R.facts('ch02-st5', F(
    terms=[('variation', 'differences in characteristics between individuals of the same species'),
           ('continuous variation', 'variation in which a characteristic can take any value within a range, e.g. height or mass, usually controlled by many genes and the environment'),
           ('discontinuous variation', 'variation in which a characteristic falls into distinct categories, e.g. blood group, usually controlled by one or a few genes'),
           ('genetic variation', 'differences caused by the different alleles individuals inherit'),
           ('environmental variation', 'differences caused by conditions such as diet, climate or lifestyle')],
    facts=[('Which of these shows discontinuous variation?', 'ABO blood group', ['Height', 'Body mass', 'Hand span'], 'Blood group falls into four distinct categories.'),
           ('Which type of graph should be used to show continuous variation such as leaf length?', 'Histogram', ['Bar chart with gaps', 'Pie chart', 'Line graph through each point'], 'Continuous data are grouped into classes and shown on a histogram with no gaps.'),
           ('Which characteristic is affected only by the environment?', 'A scar from an injury', ['Natural eye colour', 'Blood group', 'Tongue rolling'], 'A scar is acquired, not inherited.')],
    why=[('Explain why height shows continuous variation.', 'Height is controlled by many genes (polygenic), each adding a small amount, and by environmental factors such as diet, so it can take any value within a range and forms a normal distribution.'),
         ('Explain why genetically identical plants grown from cuttings can still differ in height.', 'They have the same alleles, so differences must be environmental – e.g. light, water, minerals and temperature.'),
         ('Explain why variation is important for natural selection.', 'If individuals vary, some have features better suited to the environment; they survive and reproduce more, passing on their alleles.')],
    contrast=[('continuous variation', 'discontinuous variation', 'Continuous variation has a range of values with no categories (height), usually polygenic plus environment; discontinuous variation has distinct groups (blood group), usually one gene.'),
              ('genetic variation', 'environmental variation', 'Genetic variation comes from inherited alleles and can be passed on; environmental variation comes from conditions during life and is not inherited.')],
    misc=[('Bar charts with gaps are the best way to show the heights of a class.', 'Height is continuous; group it into classes and draw a histogram with no gaps.'),
          ('A bodybuilder’s large muscles will be inherited by her children.', 'Muscle size from training is environmental variation, which is not passed on in the DNA.')],
    cases=[('studies of identical twins raised apart (Minnesota Twin Study, 1979-1999)', 'Twins with identical genes but different homes were very similar in height and fingerprints but differed more in body mass and some personality measures.', 'the contributions of genes and environment to variation', 'Features where identical twins stay similar are mostly genetic; features that differ must be strongly affected by the environment.'),
           ('hydrangeas in different gardens', 'The same variety has blue flowers in acidic soil and pink flowers in alkaline soil.', 'environmental variation', 'The genotype is the same, but soil pH changes the availability of aluminium ions and therefore the flower colour.')],
    evaluate=[('Most human characteristics are determined by genes rather than the environment.', ['blood group, eye colour and many disorders are genetic', 'twin studies show high heritability for height'], ['most features are polygenic and influenced by environment (body mass, skin colour, intelligence)', 'gene expression is affected by environment'], 'Most characteristics result from an interaction of genes and environment; only a few are purely genetic.')],
))


@R.add('ch02-st5', 'C3', (1, 5), 'numerical')
def variation_stats(rng, slot):
    what, unit, lo, hi = rng.choice([('hand spans of students', 'cm', 16.0, 23.0), ('lengths of holly leaves', 'mm', 40, 80), ('masses of broad beans', 'g', 1.2, 2.4), ('heights of sunflower seedlings', 'cm', 8.0, 15.0), ('lengths of limpet shells', 'mm', 22, 38)])
    n = 6 + slot.d
    dp = 1 if isinstance(lo, float) else 0
    vals = [round(rng.uniform(lo, hi), dp) for _ in range(n)]
    mean = sum(vals) / n
    rngv = max(vals) - min(vals)
    srt = sorted(vals)
    med = (srt[n // 2] if n % 2 else (srt[n // 2 - 1] + srt[n // 2]) / 2)
    who = name(rng)
    vt = ', '.join(f'{v:.{dp}f}' for v in vals)
    k = rng.choice(['mean', 'median'] if slot.d >= 3 else ['mean'])
    if k == 'mean':
        return dict(stem=f'{who} measured the {what} ({unit}): {vt}. Calculate the mean and the range, and state the type of variation shown.',
                    answer=f'mean = {mean:.{dp + 1}f} {unit}; range = {rngv:.{dp}f} {unit}; continuous variation', markingKey=f'M1 sum ÷ {n}; A1 mean {mean:.{dp + 1}f} {unit}; A1 range {max(vals):.{dp}f} − {min(vals):.{dp}f} = {rngv:.{dp}f} {unit}; 1 continuous (any value in a range).', marks=4)
    return dict(stem=f'The {what} in a sample were ({unit}): {vt}. Find the median and the mean, and suggest which type of graph should be used to display a larger set of these data.',
                answer=f'median = {med:.{dp + 1}f} {unit}; mean = {mean:.{dp + 1}f} {unit}; histogram', markingKey=f'1 ordered list; A1 median {med:.{dp + 1}f}; A1 mean {mean:.{dp + 1}f}; 1 histogram, because the data are continuous.', marks=4)


inquiry('ch02-st5',
        dict(ctx='whether the leaves of ivy growing in shade are larger than the leaves of ivy growing in full sunlight',
             iv='light exposure (shade or full sun, measured with a light meter in lux)', dv='leaf surface area – traced on 1 cm² grid paper and squares counted',
             cvs=[('species of ivy', 'different species have different leaf sizes'), ('position of leaf on the stem (e.g. 5th leaf from tip)', 'leaf age affects size'), ('number of leaves sampled (e.g. 30)', 'larger samples reduce the effect of individual variation'), ('random sampling', 'avoids choosing large leaves')],
             hyp='If ivy grows in shade, then its leaves will have a larger area, because a larger surface absorbs more of the limited light for photosynthesis – an example of environmental variation.',
             method='Choose an ivy plant in deep shade and one in full sun (light meter readings); randomly select 30 leaves from each, always the 5th leaf from a stem tip; trace on 1 cm² grid paper and count squares (more than half = 1); calculate mean, range and plot histograms for each site.',
             weak=('the largest leaves were chosen by eye at each site', 'select leaves randomly (e.g. random numbers to choose stems) so the sample represents the whole population'),
             safety='wear gloves – ivy sap can irritate skin; take care near walls and roads'))


# =============================================================================================
# ch03 Homeostasis and Coordination
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('homeostasis', 'the maintenance of a constant internal environment (e.g. temperature, blood glucose, water) despite changes inside or outside the body'),
           ('negative feedback', 'a control mechanism in which a change from the set point triggers a response that reverses the change'),
           ('receptor', 'a cell or organ that detects a stimulus (a change in the environment)'),
           ('effector', 'a muscle or gland that carries out a response'),
           ('set point', 'the normal value around which a factor is kept, e.g. 37 °C for human core temperature')],
    facts=[('Which of these is NOT controlled by homeostasis in humans?', 'Eye colour', ['Body temperature', 'Blood glucose concentration', 'Water content of the blood'], 'Eye colour is genetically determined and not regulated.'),
           ('What is the normal core body temperature of a human?', 'About 37 °C', ['About 33 °C', 'About 40 °C', 'About 30 °C'], 'Enzymes work best near 37 °C.'),
           ('Which is the correct order in a control system?', 'Stimulus → receptor → coordination centre → effector → response', ['Receptor → stimulus → effector → coordination centre → response', 'Effector → receptor → stimulus → response', 'Stimulus → effector → receptor → response'], 'The change is detected, processed and then acted on.')],
    why=[('Explain why homeostasis is important for enzymes in the body.', 'Enzymes work best at an optimum temperature and pH; if conditions change too much, the active site changes shape (denatures) and metabolic reactions slow or stop.'),
         ('Explain why negative feedback keeps a factor close to the set point rather than at exactly one value.', 'The response only starts once a change is detected and it may overshoot, so the factor fluctuates in a narrow range around the set point.'),
         ('Explain why a fever above 42 °C is dangerous.', 'Very high temperatures denature enzymes and proteins in cells, especially in the brain, so vital reactions stop.')],
    contrast=[('negative feedback', 'positive feedback', 'Negative feedback reverses a change to restore the set point; positive feedback amplifies a change, e.g. oxytocin increasing contractions during childbirth.'),
              ('a receptor', 'an effector', 'A receptor detects a stimulus; an effector (muscle or gland) produces the response.')],
    misc=[('Negative feedback means the body responds badly to a change.', '“Negative” means the response opposes (reverses) the change, returning the factor to its set point.'),
          ('Homeostasis keeps every factor in the body exactly constant.', 'Factors fluctuate within narrow limits around a set point.')],
    cases=[('a thermostat-controlled home heating system', 'When the room cools below 20 °C the thermostat switches the boiler on; when it warms above 20 °C it switches off.', 'negative feedback', 'Like the hypothalamus, the thermostat detects deviation from a set point and triggers a response that reverses it.'),
           ('marathon runners in hot conditions (e.g. Doha 2019 World Championships)', 'Many runners did not finish the night-time women’s marathon at over 30 °C and high humidity; several needed medical treatment for heat exhaustion.', 'the limits of homeostasis', 'Sweating could not remove heat fast enough in humid air, so core temperature rose beyond the range that homeostasis could correct.')],
    evaluate=[('Wearable devices that monitor body temperature and heart rate will greatly improve people’s health.', ['early warning of fever or abnormal heart rhythm', 'encourage healthy behaviour', 'useful data for doctors'], ['data may be inaccurate', 'privacy concerns', 'can cause anxiety; expensive for many people'], 'They can help, especially for people at risk, but accuracy, privacy and access limit the benefit.')],
))

dataset('ch03-st1',
        dict(intro='{who} recorded the core body temperature of a volunteer every 10 minutes while the volunteer sat in a room whose air temperature was increased.', iv=('Room temperature', '°C'), xs=[15, 20, 25, 30, 35],
             dv=('Core temperature', '°C'), f=lambda x: 37.0, dp=1, trend='Core temperature stays almost constant at about 37 °C even though the room temperature increases by 20 °C.',
             why='Negative feedback: the hypothalamus detects any rise and triggers sweating and vasodilation to lose heat, returning core temperature to its set point.'),
        dict(intro='{who} measured the pulse rate of a student before and after exercise of increasing intensity on an exercise bike.', iv=('Power output', 'W'), xs=[0, 50, 100, 150, 200],
             dv=('Pulse rate', 'beats per minute'), f=lambda x: 70 + 0.45 * x, dp=0, trend='Pulse rate increases as power output increases.',
             why='Muscles respire faster and need more oxygen and glucose and produce more carbon dioxide; receptors detect rising CO₂ and the heart beats faster to deliver blood and remove CO₂, keeping blood conditions stable.'))

inquiry('ch03-st1',
        dict(ctx='how the duration of exercise affects the time taken for heart rate to return to its resting value',
             iv='duration of exercise (min, e.g. 1, 2, 3, 4, 5 min of step-ups)', dv='recovery time – time in seconds for pulse rate (measured with a pulse oximeter) to return to the resting rate',
             cvs=[('type and intensity of exercise (step height, steps per minute)', 'more intense exercise raises heart rate more'), ('the same person or people of similar fitness', 'fitter people recover faster'), ('room temperature', 'heat affects heart rate'), ('rest before each trial', 'starting from the resting rate')],
             hyp='If exercise lasts longer, then recovery time will increase, because more CO₂ and lactic acid build up, so negative feedback takes longer to restore normal blood conditions.',
             method='Measure resting pulse with an oximeter; do step-ups at 30 steps/min on a 20 cm step for 1, 2, 3, 4 and 5 min, resting until pulse returns to rest between trials; record time to return to resting rate; repeat three times on different days and calculate means.',
             weak=('pulse was counted at the wrist for 10 s and multiplied by 6', 'use a pulse oximeter or count for a full 60 s to reduce counting error'),
             safety='stop if dizzy; volunteers with medical conditions should not take part'))

R.facts('ch03-st2', F(
    terms=[('neurone', 'a nerve cell specialised to carry electrical impulses'),
           ('synapse', 'the junction between two neurones, across which an impulse is passed by chemical neurotransmitters'),
           ('reflex arc', 'the pathway of neurones involved in a rapid, automatic response: receptor → sensory neurone → relay neurone → motor neurone → effector'),
           ('myelin sheath', 'a fatty insulating layer around some axons that speeds up the transmission of impulses'),
           ('central nervous system (CNS)', 'the brain and spinal cord, which coordinate information from receptors'),
           ('neurotransmitter', 'a chemical released from the end of one neurone that diffuses across a synapse and triggers an impulse in the next neurone')],
    facts=[('Which neurone carries impulses from a receptor to the central nervous system?', 'Sensory neurone', ['Motor neurone', 'Relay neurone', 'Effector neurone'], 'Sensory neurones carry impulses into the CNS.'),
           ('Where are relay neurones found?', 'In the central nervous system (brain and spinal cord)', ['In the skin', 'In muscles', 'In the retina only'], 'Relay neurones link sensory and motor neurones in the CNS.'),
           ('How is an impulse passed across a synapse?', 'A neurotransmitter diffuses across the gap and binds to receptors', ['Electrons jump across the gap', 'The two neurones touch', 'Blood carries the impulse across'], 'The synapse is a chemical junction.'),
           ('Which of these is a reflex action?', 'Pupils narrowing in bright light', ['Catching a ball', 'Writing your name', 'Choosing what to eat'], 'Reflexes are automatic and do not involve conscious thought.'),
           ('Which part of a neurone carries impulses away from the cell body?', 'Axon', ['Dendrite', 'Nucleus', 'Synaptic cleft'], 'Dendrites receive impulses; the axon carries them away.')],
    why=[('Explain why reflex actions are faster than voluntary responses.', 'In a reflex the impulse passes through only a few neurones and synapses via the spinal cord or lower brain, without conscious processing in the cerebral cortex.'),
         ('Explain why the myelin sheath increases the speed of an impulse.', 'Myelin insulates the axon so the impulse jumps between gaps in the sheath (nodes), rather than travelling continuously along the membrane.'),
         ('Explain why impulses can travel in only one direction across a synapse.', 'Neurotransmitter is released only from the presynaptic neurone and receptors are only on the postsynaptic membrane.'),
         ('Explain why reflexes are important for survival.', 'They are automatic and very fast, protecting the body from harm (e.g. withdrawing from a hot object, blinking) before damage occurs.')],
    contrast=[('a sensory neurone', 'a motor neurone', 'A sensory neurone carries impulses from receptors to the CNS; a motor neurone carries impulses from the CNS to effectors.'),
              ('a reflex action', 'a voluntary action', 'A reflex is automatic, rapid and does not involve conscious thought; a voluntary action is consciously decided in the brain and is slower.')],
    misc=[('In a reflex arc the brain decides how to respond.', 'Many reflexes are coordinated by relay neurones in the spinal cord; the brain is informed afterwards.'),
          ('Nerve impulses travel across synapses as electricity.', 'Electrical impulses travel along neurones, but across a synapse the signal is chemical (neurotransmitter diffusion).'),
          ('Nerves and neurones are the same thing.', 'A nerve is a bundle of many neurones (axons) wrapped together.')],
    cases=[('multiple sclerosis (MS)', 'The immune system damages the myelin sheaths of neurones in the brain and spinal cord.', 'the role of the myelin sheath', 'Without myelin, impulses travel more slowly or are blocked, causing problems with movement, vision and balance.'),
           ('the knee-jerk (patellar) reflex test', 'A doctor taps the tendon below the kneecap and the leg kicks forward automatically.', 'a reflex arc', 'Stretch receptors detect the tap; sensory neurone → spinal cord → motor neurone → thigh muscle contracts, without the brain.')],
    evaluate=[('Using drugs that affect synapses, such as caffeine, is harmless for teenagers.', ['moderate caffeine increases alertness', 'widely available and legal'], ['disrupts sleep, which is important for brain development', 'can cause anxiety, raised heart rate and dependence', 'energy drinks contain very high doses'], 'Small amounts are unlikely to harm most people, but high or regular intake can have real effects, so it is not harmless.')],
    extended=[('A student touches a hot pan and pulls her hand away before feeling pain. Describe the pathway of the impulse in this reflex arc, explaining what happens at each synapse, and explain why the pain is felt slightly after the hand moves.', 'Heat receptors in the skin are stimulated; impulse travels along a sensory neurone to the spinal cord; at the synapse neurotransmitter diffuses across and triggers an impulse in a relay neurone; then across a second synapse into a motor neurone; impulse reaches the biceps (effector), which contracts. Pain is felt later because a separate impulse must travel up the spinal cord to the brain and be processed in the cortex.', 6, 'long'),
              ('Some pesticides (organophosphates) stop the enzyme that breaks down neurotransmitter in synapses. Predict and explain the effect on an insect’s muscles, and discuss one risk of using these pesticides near farm workers.', 'Neurotransmitter stays in the synapse and keeps stimulating the next neurone/muscle, so muscles contract continuously (spasms, paralysis) and the insect dies. Humans have the same enzyme, so exposure can poison workers (headaches, breathing problems); protective equipment and safer alternatives are needed.', 5)],
))


@R.add('ch03-st2', 'C3', (1, 5), 'numerical')
def impulse_speed(rng, slot):
    who = name(rng)
    k = rng.choice(['speed', 'time', 'ruler'])
    if k == 'speed':
        d = rng.choice([0.8, 1.0, 1.2, 1.5])
        t = rng.choice([8, 10, 12, 16, 20, 25])
        v = d / (t / 1000)
        return dict(stem=f'An impulse travels {d} m along a motor neurone from the spinal cord to a foot muscle in {t} ms. Calculate the speed of the impulse in m/s.',
                    answer=f'{v:.0f} m/s', markingKey=f'M1 convert {t} ms = {t / 1000} s; M1 speed = distance ÷ time; A1 {v:.0f} m/s.', marks=3)
    if k == 'time':
        v = rng.choice([50, 80, 100, 120])
        d = rng.choice([0.6, 0.9, 1.1, 1.4])
        t = d / v * 1000
        return dict(stem=f'Impulses in a myelinated neurone travel at {v} m/s. How long, in milliseconds, does an impulse take to travel {d} m?',
                    answer=f'{t:.1f} ms', markingKey=f'M1 t = d ÷ v = {d}/{v}; A1 {t / 1000:.4f} s = {t:.1f} ms.', marks=2)
    ds = [round(rng.uniform(9, 20), 1) for _ in range(5)]
    m = sum(ds) / 5
    t = math.sqrt(2 * m / 100 / 9.8)
    return dict(stem=f'In a ruler-drop test, {who} recorded these catch distances (cm): {", ".join(map(str, ds))}. (a) Calculate the mean distance. (b) Use t = √(2d ÷ g), with d in metres and g = 9.8 m/s², to calculate the mean reaction time.',
                answer=f'(a) {m:.1f} cm (b) {t:.3f} s', markingKey=f'(a) M1 sum ÷ 5; A1 {m:.1f} cm. (b) M1 d = {m / 100:.3f} m substituted; A1 {t:.3f} s.', marks=4)


dataset('ch03-st2',
        dict(intro='{who} measured reaction times with an online test after drinking different volumes of a caffeinated drink.', iv=('Volume of drink', 'cm³'), xs=[0, 100, 200, 300, 400],
             dv=('Reaction time', 'ms'), f=lambda x: 300 - 0.12 * x, dp=0, trend='Reaction time decreases as the volume of caffeinated drink increases.',
             why='Caffeine is a stimulant that increases the release of neurotransmitter at synapses, so impulses cross synapses more readily and responses are quicker.'),
        dict(intro='{who} measured reaction time using the ruler-drop test with the dominant hand after different numbers of practice attempts.', iv=('Practice attempts', ''), xs=[0, 5, 10, 15, 20],
             dv=('Catch distance', 'cm'), f=lambda x: 18 - 0.35 * x, dp=1, trend='Catch distance (and so reaction time) decreases with more practice and levels off.',
             why='Practice strengthens the neural pathway, so impulses cross synapses more quickly and the brain anticipates the drop.'))

inquiry('ch03-st2',
        dict(ctx='how the number of hours of sleep the night before affects the reaction time of students measured with a ruler-drop test',
             iv='hours of sleep the night before (recorded by a sleep app)', dv='reaction time – catch distance in cm on a 30 cm ruler, converted to time using t = √(2d/g)',
             cvs=[('hand used (dominant)', 'the dominant hand usually reacts faster'), ('time of day of the test', 'alertness changes during the day'), ('caffeine intake', 'caffeine affects synapses'), ('height of the drop and who drops it', 'a different method of release changes the result')],
             hyp='If students sleep less, then their reaction time will be longer, because tiredness slows the processing of impulses in the brain and at synapses.',
             method='Ask 25 students to record their sleep; at 9 a.m., with no caffeine, each sits with forearm on a table; a partner drops a 30 cm ruler without warning, zero at the thumb; record the catch distance; 5 attempts per student after 2 practice tries; calculate mean and convert to time; plot against hours of sleep.',
             weak=('the person dropping the ruler counted down "3, 2, 1" before each drop', 'drop the ruler at random intervals without warning so students react to the stimulus rather than anticipating it'),
             safety='keep fingers clear of the ruler edge; use a plastic ruler'))

R.facts('ch03-st3', F(
    terms=[('hormone', 'a chemical messenger secreted by an endocrine gland into the blood and carried to a target organ'),
           ('endocrine gland', 'a ductless gland that secretes hormones directly into the bloodstream'),
           ('insulin', 'a hormone secreted by the pancreas when blood glucose is high; it causes cells to take up glucose and the liver to store it as glycogen'),
           ('glucagon', 'a hormone secreted by the pancreas when blood glucose is low; it causes the liver to convert glycogen back to glucose'),
           ('glycogen', 'an insoluble storage carbohydrate made from glucose in the liver and muscles'),
           ('type 1 diabetes', 'a disorder in which the pancreas produces little or no insulin because the beta cells have been destroyed by the immune system'),
           ('type 2 diabetes', 'a disorder in which body cells no longer respond properly to insulin, strongly linked to obesity and inactivity')],
    facts=[('Which organ secretes insulin?', 'Pancreas', ['Liver', 'Adrenal gland', 'Pituitary gland'], 'Beta cells in the islets of the pancreas secrete insulin.'),
           ('Which gland is known as the “master gland” because it controls many other glands?', 'Pituitary gland', ['Thyroid gland', 'Pancreas', 'Adrenal gland'], 'The pituitary secretes hormones such as FSH, TSH and ADH that act on other glands.'),
           ('Which hormone prepares the body for “fight or flight”?', 'Adrenaline', ['Insulin', 'Thyroxine', 'Oestrogen'], 'Adrenaline raises heart rate and blood glucose.'),
           ('What happens to blood glucose after a meal rich in carbohydrates?', 'It rises, and insulin is secreted to bring it down', ['It falls, and glucagon is secreted', 'It stays constant without hormones', 'It rises, and glucagon is secreted'], 'Digested starch is absorbed as glucose.')],
    why=[('Explain how blood glucose concentration is brought back to normal after a meal.', 'The pancreas detects the rise and secretes insulin; insulin causes body cells to take up glucose and the liver to convert glucose to glycogen, so blood glucose falls back to normal (negative feedback).'),
         ('Explain why hormonal responses are slower but longer lasting than nervous responses.', 'Hormones travel in the blood, which takes seconds to minutes to reach target organs, and they remain in the blood until broken down; nerve impulses are electrical and last only milliseconds.'),
         ('Explain why people with type 1 diabetes must inject insulin rather than take it as a tablet.', 'Insulin is a protein, so it would be digested by proteases in the stomach and small intestine before it could be absorbed.'),
         ('Explain why regular exercise reduces the risk of type 2 diabetes.', 'Exercise uses glucose in respiration, reduces body fat and improves how well cells respond to insulin.')],
    contrast=[('insulin', 'glucagon', 'Insulin is released when blood glucose is high and lowers it (glucose → glycogen); glucagon is released when blood glucose is low and raises it (glycogen → glucose).'),
              ('glucagon', 'glycogen', 'Glucagon is a hormone from the pancreas; glycogen is a storage carbohydrate in the liver and muscles that glucagon causes to be broken down.'),
              ('type 1 diabetes', 'type 2 diabetes', 'Type 1: little or no insulin is made (autoimmune), treated with insulin injections; type 2: cells resist insulin, linked to obesity, treated with diet, exercise and drugs such as metformin.'),
              ('the nervous system', 'the endocrine system', 'The nervous system uses electrical impulses along neurones – fast, short-lived, precise; the endocrine system uses hormones in the blood – slower, longer-lasting, widespread.')],
    misc=[('Glucagon is the substance stored in the liver.', 'Glycogen is stored in the liver; glucagon is the hormone that triggers its breakdown.'),
          ('Insulin breaks glucose down to release energy.', 'Insulin is a hormone that causes cells to take up glucose and the liver to store it; respiration releases energy from glucose.'),
          ('Only people who eat a lot of sugar get diabetes.', 'Type 1 is autoimmune and unrelated to diet; type 2 risk is linked to obesity, inactivity and genetics, not only sugar intake.')],
    cases=[('the discovery of insulin by Banting and Best in Toronto (1921)', 'They extracted a substance from dog pancreases that lowered blood glucose in diabetic dogs; in 1922 14-year-old Leonard Thompson became the first patient treated.', 'the role of insulin in controlling blood glucose', 'Diabetic animals without pancreatic insulin had very high blood glucose that fell when the extract was injected.'),
           ('rising rates of type 2 diabetes in the Gulf states', 'Countries such as Kuwait and Qatar have adult diabetes rates of around 20%, linked to rapid changes in diet and inactive lifestyles.', 'lifestyle risk factors for type 2 diabetes', 'Obesity and inactivity reduce the response of cells to insulin, so blood glucose is not controlled.')],
    sources=[('Blood glucose (mmol/dm³) after a 75 g glucose drink. Person A: 0 min 4.8, 30 min 7.6, 60 min 6.4, 120 min 5.0. Person B: 0 min 7.2, 30 min 12.5, 60 min 14.0, 120 min 12.1.', 'Oral glucose tolerance test results', 'Identify which person may have diabetes and justify your answer using the data.', 'Person B: fasting level is high (7.2) and glucose keeps rising to 14.0 and is still 12.1 at 120 min (>11.1 is a diabetes indicator); Person A returns to near 5.0 within 2 h, showing normal insulin response.')],
    evaluate=[('A sugar tax on soft drinks is the best way to reduce type 2 diabetes.', ['reduces sugar intake (e.g. Mexico’s 2014 tax cut purchases by about 7-12%)', 'manufacturers reformulate drinks with less sugar (UK 2018 levy)', 'revenue can fund health education'], ['affects poorer people more', 'people may switch to other sugary foods', 'inactivity and genetics are also major causes'], 'A sugar tax helps but is not enough alone; it works best with education, exercise programmes and food labelling.')],
))


@R.add('ch03-st3', 'C3', (2, 5), 'numerical')
def glucose_rate(rng, slot):
    a = round(rng.uniform(4.2, 5.4), 1)
    peak = round(a + rng.uniform(2.5, 4.5), 1)
    t1 = rng.choice([30, 45, 60])
    t2 = t1 + rng.choice([60, 75, 90])
    end = round(a + rng.uniform(-0.2, 0.4), 1)
    rise = (peak - a) / t1
    fall = (peak - end) / (t2 - t1)
    who = name(rng)
    return dict(stem=f'{who}’s blood glucose was {a} mmol/dm³ before breakfast. It rose to {peak} mmol/dm³ at {t1} min after eating and fell to {end} mmol/dm³ at {t2} min. (a) Calculate the mean rate of rise and the mean rate of fall in mmol/dm³ per minute. (b) Name the hormone responsible for the fall and explain how it works.',
                answer=f'(a) rise {rise:.3f}, fall {fall:.3f} mmol/dm³ per min (b) insulin – cells take up glucose and the liver stores it as glycogen',
                markingKey=f'(a) M1 change ÷ time; A1 rise ({peak} − {a})/{t1} = {rise:.3f}; A1 fall ({peak} − {end})/{t2 - t1} = {fall:.3f}. (b) 1 insulin from the pancreas; 1 glucose taken into cells/converted to glycogen.', marks=5)


dataset('ch03-st3',
        dict(intro='{who} measured the blood glucose concentration of a volunteer at intervals after drinking a 75 g glucose solution.', iv=('Time after drink', 'min'), xs=[0, 30, 60, 90, 120],
             dv=('Blood glucose', 'mmol/dm³'), f=lambda x: 5 + 3.2 * math.sin(math.pi * min(x, 120) / 120) * (1 if x <= 60 else 0.9), dp=1,
             trend='Blood glucose rises to a peak at about 30-60 min and then falls back towards the starting value by 120 min.',
             why='Glucose is absorbed from the gut; the pancreas detects the rise and secretes insulin, so cells take up glucose and the liver stores it as glycogen – negative feedback.'))

inquiry('ch03-st3',
        dict(ctx='how the concentration of glucose in a solution can be estimated using glucose test strips, to model how doctors test urine for diabetes',
             iv='glucose concentration of the standard solutions (0, 0.5, 1, 2, 5, 10 g/dm³)', dv='colour of the test strip after 30 s, matched to a colour chart (or measured with a colorimeter app)',
             cvs=[('time before reading the strip', 'colour keeps developing'), ('temperature of solutions', 'affects the enzyme reaction on the strip'), ('volume/dipping time', 'changes the amount of glucose reaching the strip'), ('lighting when comparing colours', 'affects colour judgement')],
             hyp='If the glucose concentration increases, then the strip colour will become darker, because the enzyme glucose oxidase on the strip produces more coloured product with more glucose.',
             method='Prepare standard glucose solutions by dilution; dip a test strip into each for 2 s; read after exactly 30 s against the chart under the same light; repeat with three strips; use the results to estimate the concentration of three “mystery urine” samples (artificial).',
             weak=('strips were read at different times, from 10 s to 2 min after dipping', 'use a stopwatch and read every strip exactly 30 s after dipping'),
             safety='use artificial urine only; wear eye protection'))

R.facts('ch03-st4', F(
    terms=[('thermoregulation', 'the control of core body temperature by the hypothalamus'),
           ('vasodilation', 'widening of arterioles near the skin surface so more blood flows close to the skin and more heat is lost by radiation'),
           ('vasoconstriction', 'narrowing of arterioles near the skin surface so less blood flows close to the skin and heat is conserved'),
           ('ADH (antidiuretic hormone)', 'a hormone released by the pituitary gland that makes the kidney tubules more permeable to water, so more water is reabsorbed'),
           ('osmoregulation', 'the control of the water content and concentration of the blood, mainly by the kidneys'),
           ('nephron', 'one of about a million tiny tubules in each kidney that filters blood and adjusts its composition')],
    facts=[('Which part of the brain monitors core body temperature?', 'Hypothalamus', ['Cerebellum', 'Medulla', 'Cerebral cortex'], 'Thermoreceptors in the hypothalamus detect blood temperature.'),
           ('What happens to urine when a person is dehydrated?', 'A small volume of concentrated urine is produced', ['A large volume of dilute urine is produced', 'Urine contains glucose', 'No change'], 'More ADH → more water reabsorbed.'),
           ('Which response helps to warm the body when it is cold?', 'Shivering', ['Sweating', 'Vasodilation', 'Releasing less ADH'], 'Shivering muscles respire and release heat.'),
           ('Which substance is normally reabsorbed completely by the kidneys in a healthy person?', 'Glucose', ['Urea', 'Excess water', 'Excess salt'], 'All glucose is reabsorbed in the proximal tubule.')],
    why=[('Explain how sweating cools the body.', 'Sweat glands release water onto the skin; the water evaporates using heat energy from the skin, so the skin and blood are cooled.'),
         ('Explain why people feel hotter in humid weather than in dry weather at the same temperature.', 'In humid air the concentration of water vapour is high, so sweat evaporates more slowly and less heat is removed.'),
         ('Explain how the body responds to drinking a large volume of water.', 'Blood water content rises; the hypothalamus detects it and the pituitary releases less ADH; kidney tubules become less permeable, less water is reabsorbed, and a large volume of dilute urine is produced (negative feedback).'),
         ('Explain why vasoconstriction helps to conserve heat.', 'Arterioles to the skin narrow, so less warm blood flows near the surface and less heat is lost by radiation, keeping heat in the core.')],
    contrast=[('vasodilation', 'vasoconstriction', 'Vasodilation widens skin arterioles to increase heat loss when hot; vasoconstriction narrows them to reduce heat loss when cold.'),
              ('urea', 'urine', 'Urea is a waste product made in the liver from excess amino acids; urine is the liquid made by the kidneys containing water, urea and salts.')],
    misc=[('Blood vessels move closer to the skin surface when we are hot.', 'Blood vessels do not move; arterioles supplying the skin widen (vasodilation), so more blood flows through skin capillaries.'),
          ('ADH makes you produce more urine.', 'ADH increases water reabsorption, so less, more concentrated urine is produced.'),
          ('Shivering is a sign that the body has stopped controlling its temperature.', 'Shivering is an active homeostatic response: rapid muscle contractions release heat from respiration.')],
    cases=[('kidney dialysis', 'Patients with kidney failure are connected to a dialysis machine 3 times a week; blood flows past a partially permeable membrane with dialysis fluid on the other side.', 'the role of the kidneys in water and waste balance', 'The machine removes urea and excess water and salts by diffusion, replacing what failed kidneys can no longer do.'),
           ('hypothermia in mountain climbers on Everest', 'In extreme cold and wind, climbers lose heat faster than the body can generate it; core temperature drops below 35 °C, causing confusion and slowed heart rate.', 'the limits of thermoregulation', 'Vasoconstriction and shivering cannot match the heat lost, so the negative feedback fails.')],
    evaluate=[('Kidney transplants are a better treatment than dialysis for kidney failure.', ['the patient can live normally without dialysis sessions', 'cheaper over many years', 'better quality of life and survival'], ['shortage of donor kidneys; long waiting lists', 'risk of rejection; lifelong immunosuppressant drugs', 'surgery risks'], 'A transplant is usually better for suitable patients, but dialysis remains essential while waiting or when transplant is not possible.'),
              ('Countries should adopt an “opt-out” system for organ donation.', ['increases the number of donors (e.g. Spain has the highest donation rate)', 'most people support donation but never register'], ['may reduce trust; some religious and cultural objections', 'families may still refuse', 'other factors (number of transplant coordinators) matter more'], 'Opt-out can help when combined with a good transplant infrastructure and respect for family and cultural views.')],
))


@R.add('ch03-st4', 'C3', (1, 4), 'numerical')
def kidney_calc(rng, slot):
    k = rng.choice(['filtrate', 'percent', 'sweat'])
    if k == 'filtrate':
        f = rng.choice([150, 160, 170, 180])
        u = round(rng.uniform(1.0, 2.0), 1)
        p = (f - u) / f * 100
        return dict(stem=f'A person’s kidneys filter {f} dm³ of fluid from the blood per day but produce only {u} dm³ of urine. Calculate the percentage of filtered water that is reabsorbed.',
                    answer=f'{p:.1f}%', markingKey=f'M1 reabsorbed = {f} − {u} = {f - u:.1f} dm³; M1 ÷ {f} × 100; A1 {p:.1f}%.', marks=3)
    if k == 'percent':
        before = rng.randint(55, 75)
        after = round(before - rng.uniform(0.8, 2.2), 1)
        loss = before - after
        pct = loss / before * 100
        sport = rng.choice(['a football match in Dubai', 'a 10 km run in Singapore', 'a tennis match in Melbourne'])
        return dict(stem=f'An athlete’s mass was {before} kg before {sport} and {after} kg after it. Assuming the loss is water, calculate the percentage of body mass lost and state one effect this will have on the volume of urine produced.',
                    answer=f'{pct:.1f}%; smaller volume of concentrated urine (more ADH)', markingKey=f'M1 {loss:.1f} ÷ {before} × 100; A1 {pct:.1f}%; 1 more ADH released → less urine, more concentrated.', marks=3)
    ml = rng.choice([400, 600, 800, 1000, 1200])
    E = ml / 1000 * 2260
    return dict(stem=f'Evaporating 1 g of sweat removes 2.26 kJ of heat energy. A cyclist evaporates {ml} g of sweat during a ride. Calculate the heat energy removed in kJ.',
                answer=f'{E:.0f} kJ', markingKey=f'M1 {ml} × 2.26; A1 {E:.0f} kJ.', marks=2)


dataset('ch03-st4',
        dict(intro='{who} filled conical flasks with water at 60 °C, wrapped them in different numbers of layers of cotton cloth (to model insulation by clothing or fur) and recorded the temperature drop after 15 minutes.', iv=('Layers of cloth', ''), xs=[0, 1, 2, 3, 4],
             dv=('Temperature drop', '°C'), f=lambda x: 18 / (1 + 0.45 * x), dp=1, trend='The temperature drop decreases as the number of layers increases, with smaller decreases for each extra layer.',
             why='Layers trap air, a poor conductor, reducing heat loss by conduction and convection – like hair erecting or clothing in thermoregulation.'),
        dict(intro='{who} recorded the volume of urine produced by a volunteer in the hour after drinking different volumes of water.', iv=('Volume of water drunk', 'cm³'), xs=[0, 250, 500, 750, 1000],
             dv=('Urine volume', 'cm³'), f=lambda x: 60 + 0.55 * x, dp=0, trend='Urine volume increases as the volume of water drunk increases.',
             why='Extra water dilutes the blood; less ADH is released by the pituitary, so kidney tubules reabsorb less water and more dilute urine is produced.'))

inquiry('ch03-st4',
        dict(ctx='how the surface area to volume ratio of a “model animal” (flask or tube of hot water) affects its rate of cooling',
             iv='size of container (and so surface area to volume ratio)', dv='rate of cooling – temperature fall in °C per minute measured with a thermometer over 10 min',
             cvs=[('starting temperature of the water', 'a hotter object loses heat faster'), ('room temperature and draughts', 'affect heat loss'), ('material and colour of containers', 'affect conduction and radiation'), ('time interval of readings', 'needed to compare rates')],
             hyp='If the surface area to volume ratio increases, then the rate of cooling will increase, because heat is lost through the surface, so a smaller “animal” has more surface per unit volume to lose heat from.',
             method='Use five boiling tubes/flasks of 25, 50, 100, 250 and 500 cm³; fill with water at 70 °C; record temperature every minute for 10 min in the same room away from draughts; calculate rate of cooling; repeat three times.',
             weak=('the starting temperature varied from 60 °C to 75 °C between flasks', 'heat the water in one kettle and start timing when each flask reaches exactly 70 °C'),
             safety='hot water can scald – use a tray and heat-proof gloves'))


# =============================================================================================
# ch04 Atomic Structure and the Periodic Table
# =============================================================================================
# symbol: (name, Z, common mass number)
ELEMENTS = {'H': ('hydrogen', 1, 1), 'He': ('helium', 2, 4), 'Li': ('lithium', 3, 7), 'Be': ('beryllium', 4, 9), 'B': ('boron', 5, 11), 'C': ('carbon', 6, 12),
            'N': ('nitrogen', 7, 14), 'O': ('oxygen', 8, 16), 'F': ('fluorine', 9, 19), 'Ne': ('neon', 10, 20), 'Na': ('sodium', 11, 23), 'Mg': ('magnesium', 12, 24),
            'Al': ('aluminium', 13, 27), 'Si': ('silicon', 14, 28), 'P': ('phosphorus', 15, 31), 'S': ('sulfur', 16, 32), 'Cl': ('chlorine', 17, 35), 'Ar': ('argon', 18, 40),
            'K': ('potassium', 19, 39), 'Ca': ('calcium', 20, 40), 'Fe': ('iron', 26, 56), 'Cu': ('copper', 29, 64), 'Zn': ('zinc', 30, 65), 'Br': ('bromine', 35, 80),
            'Ag': ('silver', 47, 108), 'I': ('iodine', 53, 127), 'Au': ('gold', 79, 197), 'Pb': ('lead', 82, 207), 'U': ('uranium', 92, 238)}
IONS = {'Na': 1, 'K': 1, 'Li': 1, 'Mg': 2, 'Ca': 2, 'Al': 3, 'O': -2, 'S': -2, 'F': -1, 'Cl': -1, 'N': -3}


def _charge(c):
    return ('' if abs(c) == 1 else str(abs(c))) + ('+' if c > 0 else '−')


def shells(z):
    out = []
    for cap in (2, 8, 8, 2):
        if z <= 0:
            break
        out.append(min(cap, z))
        z -= min(cap, z)
    return out


R.facts('ch04-st1', F(
    terms=[('atomic number (proton number)', 'the number of protons in the nucleus of an atom, which identifies the element'),
           ('mass number (nucleon number)', 'the total number of protons and neutrons in the nucleus of an atom'),
           ('ion', 'an atom or group of atoms that has gained or lost electrons and so carries an electrical charge'),
           ('nucleus', 'the tiny, dense, positively charged centre of an atom containing protons and neutrons'),
           ('element', 'a substance made of only one type of atom, all with the same atomic number')],
    facts=[('What is the relative charge of a neutron?', '0', ['+1', '−1', '+2'], 'Neutrons are neutral.'),
           ('Which particle has the smallest mass?', 'Electron', ['Proton', 'Neutron', 'Nucleus'], 'An electron has about 1/1840 of the mass of a proton.'),
           ('Why is an atom electrically neutral?', 'It has equal numbers of protons and electrons', ['It has equal numbers of protons and neutrons', 'Neutrons cancel the charges', 'Electrons have no charge'], 'Each proton (+1) is balanced by an electron (−1).'),
           ('Approximately what fraction of an atom’s diameter is the diameter of its nucleus?', 'About 1/100 000', ['About 1/2', 'About 1/10', 'About 1/100'], 'Atoms are about 10⁻¹⁰ m across; nuclei about 10⁻¹⁵ m.')],
    why=[('Explain why the mass of an atom is concentrated in its nucleus.', 'Protons and neutrons each have a relative mass of 1, while electrons have a relative mass of only about 1/1840, so almost all the mass is in the nucleus.'),
         ('Explain why a sodium ion has a charge of +1.', 'A sodium atom has 11 protons and 11 electrons; it loses one electron to form Na⁺, leaving 11 protons and 10 electrons, so the overall charge is +1.'),
         ('Explain why the atomic number, not the mass number, identifies an element.', 'All atoms of an element have the same number of protons; the number of neutrons (and so mass number) can vary between isotopes.')],
    contrast=[('atomic number', 'mass number', 'Atomic number is the number of protons; mass number is protons + neutrons.'),
              ('an atom', 'an ion', 'An atom has equal numbers of protons and electrons and no overall charge; an ion has gained or lost electrons and so is charged.')],
    misc=[('The mass number of an atom is the number of protons plus electrons.', 'Mass number is protons plus neutrons; electrons have negligible mass.'),
          ('A chloride ion, Cl⁻, has one more proton than a chlorine atom.', 'It has one more electron; the number of protons (17) never changes in chemical reactions.'),
          ('Electrons orbit inside the nucleus.', 'Electrons are found in shells (energy levels) around the nucleus; the nucleus contains only protons and neutrons.')],
    evaluate=[('Models of the atom used in school are “wrong” and should not be taught.', ['the shell model is a simplification; electrons are actually described by orbitals', 'simple models can create misconceptions'], ['models are useful if they explain observations at the right level', 'the shell model explains bonding, groups and reactivity well', 'science progresses by refining models'], 'Simplified models are valuable when their limitations are made clear; all scientific models are approximations.')],
))


@R.add('ch04-st1', 'C3', (1, 4), 'numerical')
def subatomic(rng, slot):
    sym = rng.choice(list(ELEMENTS))
    nm, z, a = ELEMENTS[sym]
    k = rng.choice(['atom', 'ion'] if sym in IONS and slot.d >= 2 else ['atom'])
    if k == 'atom':
        frame = rng.choice([f'An atom of {nm} is written as {a}/{z} {sym} (mass number {a}, atomic number {z}). State the number of protons, neutrons and electrons it contains.',
                            f'Deduce the numbers of protons, neutrons and electrons in an atom of {nm}-{a} (atomic number {z}).'])
        return dict(stem=frame, answer=f'{z} protons, {a - z} neutrons, {z} electrons', markingKey=f'1 protons = atomic number = {z}; 1 neutrons = {a} − {z} = {a - z}; 1 electrons = protons = {z} (neutral atom).', marks=3)
    c = IONS[sym]
    e = z - c
    return dict(stem=f'A {nm} ion has the symbol {sym}{_charge(c)}. The atom has mass number {a} and atomic number {z}. State the number of protons, neutrons and electrons in the ion.',
                answer=f'{z} protons, {a - z} neutrons, {e} electrons', markingKey=f'1 protons {z}; 1 neutrons {a - z}; 1 electrons {z} − ({c:+d}) = {e} ({"lost" if c > 0 else "gained"} {abs(c)}).', marks=3)


@R.add('ch04-st1', 'C1', (1, 3), 'mcq')
def which_element(rng, slot):
    syms = rng.sample(list(ELEMENTS), 4)
    sym = syms[0]
    nm, z, a = ELEMENTS[sym]
    return mcq(rng, f'An atom has {z} protons and {a - z} neutrons. Which element is it?', ELEMENTS[sym][0].capitalize(), [ELEMENTS[s][0].capitalize() for s in syms[1:]],
               f'The number of protons (atomic number {z}) identifies {nm}.')


R.facts('ch04-st2', F(
    terms=[('isotopes', 'atoms of the same element with the same number of protons but different numbers of neutrons'),
           ('relative atomic mass (Aᵣ)', 'the weighted mean mass of the atoms of an element compared with 1/12 of the mass of a carbon-12 atom'),
           ('abundance', 'the percentage of atoms of an element that are a particular isotope in a natural sample'),
           ('radioisotope', 'an isotope with an unstable nucleus that emits radiation')],
    facts=[('Which statement about isotopes of an element is correct?', 'They have the same chemical properties', ['They have different numbers of protons', 'They have different numbers of electrons in neutral atoms', 'They have the same mass number'], 'Chemistry depends on electrons, which are the same.'),
           ('Why is the relative atomic mass of chlorine 35.5 rather than a whole number?', 'It is a weighted mean of chlorine-35 and chlorine-37 isotopes', ['Chlorine atoms contain half a neutron', 'Electrons add 0.5 to the mass', 'It is rounded incorrectly'], '75% ³⁵Cl and 25% ³⁷Cl average to 35.5.'),
           ('Carbon-14 and carbon-12 differ in the number of which particle?', 'Neutrons', ['Protons', 'Electrons', 'Nuclei'], 'C-14 has 8 neutrons; C-12 has 6.')],
    why=[('Explain why isotopes of the same element have identical chemical properties.', 'Chemical reactions involve electrons; isotopes have the same number of protons and therefore the same number and arrangement of electrons.'),
         ('Explain why isotopes of an element can have different physical properties, such as density.', 'They have different numbers of neutrons, so different masses; e.g. heavy water (D₂O) is about 11% denser than H₂O.'),
         ('Explain how carbon-14 dating can estimate the age of ancient remains.', 'Living organisms take in C-14 from CO₂; after death no more is taken in and C-14 decays with a half-life of about 5730 years, so the fraction remaining shows the time since death.')],
    contrast=[('mass number', 'relative atomic mass', 'Mass number is a whole number for one isotope (protons + neutrons); relative atomic mass is the weighted mean mass of all the isotopes in a natural sample, often not a whole number.')],
    misc=[('Isotopes of hydrogen have different numbers of protons, which is why they have different masses.', 'All hydrogen isotopes have one proton; they differ in neutrons (0, 1, 2).'),
          ('Relative atomic mass is just the mass number of the most common isotope.', 'It is a weighted mean of all isotopes, so it can differ from any single mass number (e.g. Cl = 35.5).')],
    cases=[('radiocarbon dating of Ötzi the Iceman', 'Remains found in the Alps in 1991 were dated using carbon-14 to about 5300 years old.', 'the use of isotopes', 'The proportion of C-14 left compared with living tissue revealed how long ago he died.'),
           ('iodine-131 treatment of overactive thyroid glands', 'Patients swallow a capsule of radioactive iodine, which the thyroid absorbs because it uses iodine to make thyroxine.', 'isotopes having the same chemical properties', 'The body treats I-131 exactly like stable iodine, so it is taken up by the thyroid, where its radiation destroys overactive tissue.')],
    evaluate=[('The medical benefits of radioisotopes outweigh the risks.', ['diagnosis (technetium-99m scans) and cancer treatment save many lives', 'short half-life isotopes limit exposure'], ['radiation can damage healthy cells and cause cancer', 'radioactive waste must be stored safely', 'cost and access issues'], 'With careful dosing and short half-lives, benefits usually outweigh risks for patients, but exposure must be minimised for staff and the public.')],
))

ISOS = [('chlorine', [(35, 75.8), (37, 24.2)]), ('copper', [(63, 69.2), (65, 30.8)]), ('boron', [(10, 19.9), (11, 80.1)]), ('lithium', [(6, 7.6), (7, 92.4)]),
        ('bromine', [(79, 50.7), (81, 49.3)]), ('gallium', [(69, 60.1), (71, 39.9)]), ('silver', [(107, 51.8), (109, 48.2)]), ('rubidium', [(85, 72.2), (87, 27.8)]),
        ('magnesium', [(24, 79.0), (25, 10.0), (26, 11.0)]), ('neon', [(20, 90.5), (21, 0.3), (22, 9.2)]), ('silicon', [(28, 92.2), (29, 4.7), (30, 3.1)])]


@R.add('ch04-st2', 'C3', (1, 5), 'numerical')
def ram(rng, slot):
    el, iso = rng.choice(ISOS)
    if slot.d >= 4 and len(iso) == 2 and rng.random() < 0.6:
        (m1, p1), (m2, p2) = iso
        ar = (m1 * p1 + m2 * p2) / 100
        return dict(stem=f'{el.capitalize()} has two isotopes, {el}-{m1} and {el}-{m2}. Its relative atomic mass is {ar:.2f}. Calculate the percentage abundance of each isotope.',
                    answer=f'{el}-{m1}: {p1:.1f}%; {el}-{m2}: {p2:.1f}%', markingKey=f'M1 let x = % of {m1}: {m1}x + {m2}(100 − x) = {ar:.2f} × 100; M1 solve: x = ({m2} × 100 − {ar * 100:.0f}) ÷ {m2 - m1}; A1 {p1:.1f}% and {p2:.1f}%.', marks=4)
    ar = sum(m * p for m, p in iso) / 100
    txt = ', '.join(f'{el}-{m} ({p}%)' for m, p in iso)
    k = rng.choice(['calc', 'table'])
    stem = (f'A natural sample of {el} contains these isotopes: {txt}. Calculate the relative atomic mass of {el} to 1 decimal place.' if k == 'calc'
            else f'A mass spectrometer gives these abundances for {el}: ' + '; '.join(f'mass {m}: {p}%' for m, p in iso) + '. Calculate the relative atomic mass.')
    return dict(stem=stem, answer=f'{ar:.1f}', markingKey=f'M1 Σ(mass × abundance) = {" + ".join(f"{m} × {p}" for m, p in iso)}; M1 ÷ 100; A1 {ar:.1f} (no units).', marks=3)


@R.add('ch04-st2', 'C3', (1, 3), 'short')
def iso_compare(rng, slot):
    el, iso = rng.choice(ISOS)
    z = next(v[1] for v in ELEMENTS.values() if v[0] == el) if any(v[0] == el for v in ELEMENTS.values()) else {'gallium': 31, 'rubidium': 37}[el]
    (m1, _), (m2, _) = iso[0], iso[1]
    return dict(stem=f'{el.capitalize()} (atomic number {z}) has isotopes of mass number {m1} and {m2}. Compare the numbers of protons, neutrons and electrons in atoms of the two isotopes.',
                answer=f'Both have {z} protons and {z} electrons; {el}-{m1} has {m1 - z} neutrons and {el}-{m2} has {m2 - z} neutrons.',
                markingKey=f'1 same protons ({z}); 1 same electrons ({z}); 1 neutrons {m1 - z} vs {m2 - z}.', marks=3)


R.facts('ch04-st3', F(
    terms=[('electron shell (energy level)', 'a region around the nucleus where electrons with a particular energy are found'),
           ('electron arrangement (configuration)', 'the number of electrons in each shell of an atom, e.g. 2,8,1 for sodium'),
           ('outer shell (valence) electrons', 'the electrons in the highest occupied shell, which determine an element’s chemical properties')],
    facts=[('What is the maximum number of electrons in the first shell?', '2', ['8', '18', '1'], 'The first shell holds 2 electrons.'),
           ('What is the electron arrangement of magnesium (atomic number 12)?', '2,8,2', ['2,10', '2,2,8', '8,2,2'], 'Fill 2, then 8, then the remaining 2.'),
           ('An element has electron arrangement 2,8,7. In which group of the periodic table is it?', 'Group 17 (7)', ['Group 2', 'Group 3', 'Group 8'], 'Seven outer electrons → group 17 (halogens).'),
           ('An element has electron arrangement 2,8,3. In which period is it?', 'Period 3', ['Period 2', 'Period 8', 'Period 13'], 'Three occupied shells → period 3.')],
    why=[('Explain why elements in the same group have similar chemical properties.', 'They have the same number of electrons in their outer shell, and reactions involve outer electrons being lost, gained or shared.'),
         ('Explain why noble gases are unreactive.', 'They have a full outer shell of electrons (2 for helium, 8 for the others), which is very stable, so they do not need to lose, gain or share electrons.'),
         ('Explain how the electron arrangement of an element shows its position in the periodic table.', 'The number of occupied shells gives the period; the number of outer-shell electrons gives the group (for groups 1, 2 and 13-18 in the main block).')],
    contrast=[('a group', 'a period', 'A group is a vertical column of elements with the same number of outer electrons; a period is a horizontal row of elements with the same number of occupied shells.')],
    misc=[('Potassium has the electron arrangement 2,8,9.', 'The third shell holds 8 before the fourth starts for the first 20 elements: potassium is 2,8,8,1.'),
          ('Elements in the same period have similar properties because they have the same number of shells.', 'Properties change across a period; similar properties belong to elements in the same group.')],
    cases=[('Niels Bohr’s explanation of hydrogen’s line spectrum (1913)', 'Hydrogen gas emits only certain colours of light; Bohr proposed that electrons occupy fixed energy levels and emit light when they drop between them.', 'electrons in shells (energy levels)', 'Only specific energy differences are possible, so only specific wavelengths of light are emitted – evidence for shells.'),
           ('neon advertising signs', 'Electricity passed through neon gas excites electrons, which then fall back to lower shells, emitting red-orange light.', 'electron energy levels', 'The colour depends on the energy gaps between neon’s shells.')],
    evaluate=[('The shell model of electron arrangement is a good enough model for MYP chemistry.', ['explains groups, periods, ion charges and bonding', 'simple to draw and use'], ['does not explain elements beyond calcium (transition metals) well', 'electrons are not in fixed circular orbits; quantum model uses orbitals'], 'It is good enough for the first 20 elements and bonding at this level, as long as its limits are recognised.')],
))


@R.add('ch04-st3', 'C3', (1, 4), 'short')
def config(rng, slot):
    sym = rng.choice([s for s, v in ELEMENTS.items() if v[1] <= 20])
    nm, z, a = ELEMENTS[sym]
    sh = shells(z)
    arr = ','.join(map(str, sh))
    grp = {1: 1, 2: 2, 3: 13, 4: 14, 5: 15, 6: 16, 7: 17, 8: 18}[sh[-1]] if z > 2 else (1 if z == 1 else 18)
    k = rng.choice(['arr', 'pos', 'ion'] if sym in IONS and slot.d >= 2 else ['arr', 'pos'])
    if k == 'arr':
        return dict(stem=f'Write the electron arrangement of {nm} (atomic number {z}).', answer=arr, markingKey=f'{arr} (1 per correct shell; total must equal {z}).', marks=2 if z > 10 else 1)
    if k == 'pos':
        return dict(stem=f'{nm.capitalize()} has atomic number {z}. Write its electron arrangement and use it to deduce its group and period.', answer=f'{arr}; group {grp}; period {len(sh)}',
                    markingKey=f'1 {arr}; 1 group {grp} ({sh[-1]} outer electrons{" – full shell" if grp == 18 else ""}); 1 period {len(sh)} ({len(sh)} occupied shells).', marks=3)
    c = IONS[sym]
    ish = shells(z - c)
    return dict(stem=f'Write the electron arrangement of the {nm} atom and of the {sym}{_charge(c)} ion, and explain how the ion forms.', answer=f'atom {arr}; ion {",".join(map(str, ish))}',
                markingKey=f'1 atom {arr}; 1 ion {",".join(map(str, ish))}; 1 {"loses" if c > 0 else "gains"} {abs(c)} electron(s) to get a full outer shell like a noble gas.', marks=3)


@R.add('ch04-st3', 'C1', (1, 2), 'mcq')
def config_mcq(rng, slot):
    sym = rng.choice([s for s, v in ELEMENTS.items() if 3 <= v[1] <= 20])
    nm, z, a = ELEMENTS[sym]
    sh = shells(z)
    right = ','.join(map(str, sh))
    w = [','.join(map(str, [z])) if z <= 10 else '2,' + str(z - 2), ','.join(map(str, shells(z + 1))), ','.join(map(str, shells(z - 1)))]
    if z > 8:
        w.append('8,' + str(z - 8))
    return mcq(rng, f'Which is the electron arrangement of an atom of {nm} (atomic number {z})?', right, w, f'Fill 2, 8, 8, 2: {right}.')


R.facts('ch04-st4', F(
    terms=[('alkali metals', 'the group 1 elements (lithium, sodium, potassium, …): soft, reactive metals that form alkaline hydroxides with water'),
           ('halogens', 'the group 17 elements (fluorine, chlorine, bromine, iodine): reactive non-metals that exist as diatomic molecules'),
           ('noble gases', 'the group 18 elements: unreactive gases with full outer shells'),
           ('halogen displacement reaction', 'a reaction in which a more reactive halogen takes the place of a less reactive halogen in a compound')],
    facts=[('Which gas is produced when sodium reacts with water?', 'Hydrogen', ['Oxygen', 'Carbon dioxide', 'Chlorine'], '2Na + 2H₂O → 2NaOH + H₂'),
           ('How does reactivity change down group 1?', 'It increases', ['It decreases', 'It stays the same', 'It increases then decreases'], 'The outer electron is further from the nucleus and lost more easily.'),
           ('How does reactivity change down group 17?', 'It decreases', ['It increases', 'It stays the same', 'It decreases then increases'], 'It is harder to attract an extra electron into a shell further from the nucleus.'),
           ('What is the physical state of bromine at room temperature?', 'Red-brown liquid', ['Pale green gas', 'Grey-black solid', 'Colourless gas'], 'Fluorine and chlorine are gases, bromine a liquid, iodine a solid.'),
           ('Which solution would turn brown when chlorine water is added?', 'Potassium iodide', ['Potassium chloride', 'Sodium chloride', 'Potassium fluoride'], 'Chlorine displaces iodine: Cl₂ + 2KI → 2KCl + I₂.')],
    why=[('Explain why potassium is more reactive than sodium.', 'Potassium’s outer electron is in a shell further from the nucleus with more shielding by inner shells, so the attraction is weaker and it is lost more easily.'),
         ('Explain why fluorine is more reactive than chlorine.', 'Fluorine is smaller, so an incoming electron is closer to the nucleus and attracted more strongly; it gains an electron more easily.'),
         ('Explain why group 1 metals are stored under oil.', 'They react rapidly with oxygen and water vapour in the air; oil keeps air and moisture away.'),
         ('Explain why the melting point of the halogens increases down the group.', 'The molecules get larger with more electrons, so the intermolecular forces between molecules are stronger and need more energy to overcome.')],
    contrast=[('trends in reactivity in group 1', 'trends in reactivity in group 17', 'Group 1 reactivity increases down the group (electron lost more easily); group 17 reactivity decreases down the group (electron gained less easily).')],
    misc=[('Sodium is a hard, dense metal that sinks in water.', 'Sodium is soft (cut with a knife) and less dense than water, so it floats and fizzes.'),
          ('Iodine displaces chlorine from sodium chloride solution.', 'Iodine is less reactive than chlorine, so no reaction occurs; chlorine would displace iodine.'),
          ('Group 1 metals become less reactive down the group because they get heavier.', 'Reactivity increases down the group because the outer electron is further from the nucleus and more easily lost.')],
    cases=[('chlorination of drinking water (first used continuously in Jersey City, USA, 1908)', 'Adding small amounts of chlorine to water supplies kills bacteria and has greatly reduced cholera and typhoid.', 'the reactivity of halogens', 'Chlorine is a reactive oxidising agent that damages bacterial cells.'),
           ('lithium-ion batteries', 'Phones and electric cars use lithium, the lightest metal, because it gives up its outer electron readily and stores a lot of energy per kilogram.', 'group 1 properties', 'Lithium’s single outer electron is easily lost, making it a good material for storing charge.')],
    evaluate=[('Adding fluoride to public drinking water is a good idea.', ['reduces tooth decay, especially in children from poorer families', 'cheap and reaches everyone'], ['people cannot choose whether to take it', 'too much causes fluorosis', 'toothpaste already provides fluoride'], 'It is effective at low concentrations; whether it is justified depends on balancing public health against individual choice.'),
              ('The growing demand for lithium for batteries is good for the environment.', ['electric vehicles reduce CO₂ emissions and urban air pollution', 'batteries store renewable energy'], ['lithium mining in the Atacama uses huge volumes of water in a desert', 'impacts on local and Indigenous communities', 'battery recycling is limited'], 'Lithium enables a low-carbon transition, but mining must be managed responsibly and recycling increased.')],
))


@R.add('ch04-st4', 'C3', (2, 5), 'short')
def halogen_disp(rng, slot):
    order = ['chlorine', 'bromine', 'iodine']
    sal = {'chlorine': 'chloride', 'bromine': 'bromide', 'iodine': 'iodide'}
    sym = {'chlorine': 'Cl', 'bromine': 'Br', 'iodine': 'I'}
    colour = {'bromine': 'orange', 'iodine': 'brown'}
    h, s = rng.sample(order, 2)
    metal = rng.choice(['potassium', 'sodium'])
    M = 'K' if metal == 'potassium' else 'Na'
    react = order.index(h) < order.index(s)
    stem = f'{name(rng)} adds {h} water to {metal} {sal[s]} solution. Predict whether a reaction occurs. If it does, write the word and balanced symbol equations and describe what is seen.'
    if react:
        ans = f'Yes: {h} + {metal} {sal[s]} → {metal} {sal[h]} + {s}; {sym[h]}₂ + 2{M}{sym[s]} → 2{M}{sym[h]} + {sym[s]}₂; solution turns {colour[s]}.'
        key = f'1 reaction because {h} is more reactive than {s}; 1 word equation; 1 balanced symbol equation; 1 colour change to {colour[s]}.'
    else:
        ans = f'No reaction: {h} is less reactive than {s}, so it cannot displace it.'
        key = f'1 no reaction; 1 reason: {h} is below {s} in group 17 (less reactive); 1 no colour change beyond that of the halogen water.'
    return dict(stem=stem, answer=ans, markingKey=key, marks=4 if react else 3)


dataset('ch04-st4',
        dict(intro='{who}’s teacher demonstrated small pieces of group 1 metals of equal mass reacting with water and recorded the time for each piece to disappear. Data from a published video comparison are used for the heavier metals.', iv=('Period of the metal', ''), xs=[2, 3, 4, 5],
             dv=('Time to disappear', 's'), f=lambda x: 60 / 3 ** (x - 2), dp=1, trend='The time to disappear decreases going down the group (Li, Na, K, Rb), so reactivity increases.',
             why='Down group 1 the outer electron is further from the nucleus and more shielded, so it is lost more easily.'))

R.facts('ch04-st5', F(
    terms=[('plum pudding model', 'J. J. Thomson’s 1904 model of the atom as a sphere of positive charge with negative electrons embedded in it'),
           ('nuclear model', 'Rutherford’s 1911 model of the atom with a tiny, dense, positive nucleus surrounded mostly by empty space containing electrons'),
           ('periodic table', 'an arrangement of the elements in order of increasing atomic number, in groups and periods, so that elements with similar properties line up'),
           ('Mendeleev’s table', 'the 1869 table that arranged elements by atomic mass and properties, leaving gaps for undiscovered elements')],
    facts=[('Who discovered the electron in 1897?', 'J. J. Thomson', ['Ernest Rutherford', 'John Dalton', 'James Chadwick'], 'Thomson used cathode-ray tubes.'),
           ('Who discovered the neutron in 1932?', 'James Chadwick', ['Niels Bohr', 'Dmitri Mendeleev', 'Marie Curie'], 'Chadwick explained the extra mass of nuclei.'),
           ('In the gold foil experiment, what did the small number of alpha particles bouncing back show?', 'The positive charge and mass are concentrated in a tiny nucleus', ['Atoms are solid spheres', 'Electrons are found in shells', 'Gold atoms are negative'], 'Only a dense positive centre could repel alpha particles back.'),
           ('How did Mendeleev order the elements in 1869?', 'Mainly by atomic mass, adjusted to fit properties', ['By atomic number', 'Alphabetically', 'By date of discovery'], 'Protons were not yet known; Moseley later used atomic number.')],
    why=[('Explain why Rutherford’s gold foil results could not be explained by the plum pudding model.', 'In the plum pudding model positive charge is spread out, so alpha particles would pass through with tiny deflections; some were deflected by large angles or bounced back, which needs a small, concentrated positive nucleus.'),
         ('Explain why Mendeleev left gaps in his periodic table.', 'He arranged elements so that those with similar properties were in the same group; where no known element fitted he left a gap and predicted that undiscovered elements (e.g. gallium, germanium) would fill it.'),
         ('Explain why scientific models of the atom changed over time.', 'New experimental evidence (e.g. electron discovery, gold foil scattering, spectra) could not be explained by the old model, so scientists proposed better models that fitted all the evidence.')],
    contrast=[('the plum pudding model', 'the nuclear model', 'The plum pudding model has positive charge spread through the atom with electrons embedded; the nuclear model has a tiny, dense positive nucleus with electrons around it and mostly empty space.'),
              ('Mendeleev’s table', 'the modern periodic table', 'Mendeleev ordered by atomic mass and left gaps; the modern table orders by atomic number, includes noble gases and has no gaps up to element 118.')],
    misc=[('Most alpha particles bounced back from the gold foil.', 'Most passed straight through, showing the atom is mostly empty space; only about 1 in 8000 was deflected back.'),
          ('Mendeleev’s table was accepted immediately because it was complete.', 'It became widely accepted after his predicted elements (gallium 1875, germanium 1886) were discovered with properties close to his predictions.')],
    cases=[('Geiger and Marsden’s gold foil experiment (Manchester, 1909)', 'Alpha particles fired at thin gold foil mostly passed through, a few were deflected at large angles and some bounced back.', 'the nuclear model of the atom', 'Rutherford concluded the atom has a tiny, dense, positive nucleus and is mostly empty space.'),
           ('Mendeleev’s prediction of “eka-silicon”', 'He predicted an element with atomic mass about 72 and density about 5.5 g/cm³; germanium (discovered 1886) had mass 72.6 and density 5.35 g/cm³.', 'how the periodic table allows predictions', 'Placing elements by repeating properties allowed the properties of missing elements to be predicted accurately.')],
    sources=[('“It was quite the most incredible event that has ever happened to me in my life. It was almost as incredible as if you fired a 15-inch shell at a piece of tissue paper and it came back and hit you.”', 'Ernest Rutherford, describing the gold foil results', 'Explain what Rutherford meant and what conclusion he drew about the structure of the atom.', 'He was surprised that heavy, fast alpha particles bounced back from very thin foil; this was impossible if positive charge was spread out (plum pudding), so he concluded that the mass and positive charge are concentrated in a tiny nucleus.')],
    evaluate=[('Mendeleev deserves most of the credit for the periodic table.', ['he left gaps and made accurate predictions that were later confirmed', 'he swapped elements (e.g. Te and I) to match properties'], ['Newlands (law of octaves, 1865) and Meyer had similar ideas', 'Moseley’s work on atomic number fixed the ordering problems', 'Ramsay added the noble gases'], 'Mendeleev’s predictions make his contribution the most important, but the table is the work of many scientists.')],
    extended=[('Describe how the model of the atom developed from Dalton to Chadwick, naming the evidence that led to each change.', 'Dalton (1803): indivisible solid spheres. Thomson (1897/1904): discovered electrons in cathode rays → plum pudding. Rutherford (1911): gold foil scattering → nuclear model. Bohr (1913): line spectra → electrons in fixed energy levels. Chadwick (1932): neutral particle with mass → neutrons in the nucleus.', 6, 'long')],
))


@R.add('ch04-st1', 'C4', (3, 5), 'multi_step')
def particle_puzzle(rng, slot):
    sym = rng.choice([s for s in IONS])
    nm, z, a = ELEMENTS[sym]
    c = IONS[sym]
    e = z - c
    n = a - z
    return dict(stem=f'A particle X has {z} protons, {n} neutrons and {e} electrons. (a) Identify X, giving its symbol, mass number and charge. (b) Explain how X was formed from a neutral atom. (c) Explain why X has the same mass number as the atom it was formed from.',
                answer=f'(a) {sym}{_charge(c)}, mass number {a} ({nm} ion) (b) the atom {"lost" if c > 0 else "gained"} {abs(c)} electron(s) (c) electrons have negligible mass; protons and neutrons are unchanged',
                markingKey=f'(a) 1 {nm} because {z} protons; 1 mass number {z} + {n} = {a}; 1 charge {z} − {e} = {c:+d}. (b) 1 {"loss" if c > 0 else "gain"} of {abs(c)} electron(s) to reach a full outer shell. (c) 1 mass number counts only protons and neutrons; electrons have relative mass ≈ 1/1840.', marks=5, gap='G5')


@R.add('ch04-st2', 'C4', (3, 5), 'multi_step')
def enrich(rng, slot):
    k = rng.choice(['uranium', 'mystery', 'boron'])
    if k == 'uranium':
        p = rng.choice([3.0, 3.5, 4.0, 4.5, 5.0, 20.0])
        nat = (235 * 0.72 + 238 * 99.28) / 100
        enr = (235 * p + 238 * (100 - p)) / 100
        return dict(stem=f'Natural uranium is 0.72% uranium-235 and 99.28% uranium-238. Nuclear fuel is “enriched” to {p}% uranium-235. (a) Calculate the relative atomic mass of natural and of enriched uranium to 3 decimal places. (b) Explain why the isotopes cannot be separated by a chemical reaction. (c) Discuss one benefit and one risk of uranium enrichment technology.',
                    answer=f'(a) natural {nat:.3f}; enriched {enr:.3f} (b) isotopes have the same electron arrangement, so identical chemical properties (c) benefit: low-carbon electricity; risk: highly enriched uranium can be used in nuclear weapons',
                    markingKey=f'(a) M1 weighted mean; A1 {nat:.3f}; A1 {enr:.3f}. (b) 1 same number of electrons → same chemistry; separation uses mass difference (centrifuges). (c) 1 benefit, 1 risk with explanation.', marks=6, gap='G5')
    if k == 'boron':
        p = rng.choice([18.0, 19.0, 20.0, 21.0])
        ar = (10 * p + 11 * (100 - p)) / 100
        return dict(stem=f'A sample of boron from Turkey has a relative atomic mass of {ar:.2f}. Boron has isotopes boron-10 and boron-11. (a) Calculate the percentage abundance of boron-10 in this sample. (b) A second sample from California has Aᵣ = 10.82. Deduce which sample is richer in boron-10 and explain how you know.',
                    answer=f'(a) {p:.0f}% (b) the Turkish sample if {ar:.2f} < 10.82, otherwise the Californian sample: lower Aᵣ means more of the lighter isotope',
                    markingKey=f'(a) M1 10x + 11(100 − x) = {ar * 100:.0f}; A1 x = {p:.0f}%. (b) 1 {"Turkish" if ar < 10.82 else "Californian"} sample; 1 lower relative atomic mass ⇒ larger proportion of B-10.', marks=4)
    el, iso = rng.choice([x for x in ISOS if len(x[1]) == 2])
    (m1, p1), (m2, p2) = iso
    ar = (m1 * p1 + m2 * p2) / 100
    return dict(stem=f'A mass spectrum of an unknown element shows two peaks: mass {m1} (relative abundance {p1}) and mass {m2} (relative abundance {p2}). (a) Calculate the relative atomic mass. (b) Use the periodic table to identify the element. (c) Explain why the two peaks represent atoms of the same element.',
                answer=f'(a) {ar:.1f} (b) {el} (c) same element ⇒ same proton number; masses differ only in neutrons',
                markingKey=f'(a) M1 ({m1} × {p1} + {m2} × {p2}) ÷ 100; A1 {ar:.1f}. (b) 1 {el}. (c) 1 isotopes: same number of protons, different numbers of neutrons.', marks=4)


@R.add('ch04-st3', 'C4', (3, 5), 'multi_step')
def predict_compound(rng, slot):
    metal = rng.choice(['Li', 'Na', 'K', 'Mg', 'Ca', 'Al'])
    non = rng.choice(['O', 'S', 'F', 'Cl', 'N'])
    mz, nz = ELEMENTS[metal][1], ELEMENTS[non][1]
    cm, cn = IONS[metal], -IONS[non]
    l = cm * cn // math.gcd(cm, cn)
    a, b = l // cm, l // cn
    formula = f'{metal}{"" if a == 1 else a}{non}{"" if b == 1 else b}'
    return dict(stem=f'Element X has atomic number {mz} and element Y has atomic number {nz}. (a) Write the electron arrangement of each atom. (b) Predict the charge on the ion each forms and explain your prediction. (c) Deduce the formula of the compound formed between X and Y.',
                answer=f'(a) X {",".join(map(str, shells(mz)))}; Y {",".join(map(str, shells(nz)))} (b) X{_charge(cm)}, Y{_charge(-cn)} (c) X{"" if a == 1 else a}Y{"" if b == 1 else b} (i.e. {formula})',
                markingKey=f'(a) 1 each arrangement. (b) 1 X loses {cm} outer electron(s) → +{cm}; 1 Y gains {cn} → −{cn}; full outer shells. (c) M1 charges balance: {a} × {cm} = {b} × {cn}; A1 X{"" if a == 1 else a}Y{"" if b == 1 else b}.', marks=6, gap='G5')


@R.add('ch04-st3', 'C2', (2, 4), 'explain')
def why_group(rng, slot):
    sym = rng.choice([s for s, v in ELEMENTS.items() if 3 <= v[1] <= 20 and v[1] not in (5, 10, 18)])
    nm, z, a = ELEMENTS[sym]
    sh = shells(z)
    return dict(stem=f'{nm.capitalize()} has atomic number {z}. Explain, using its electron arrangement, why it is placed in period {len(sh)} and predict whether it is likely to form positive or negative ions (or neither).',
                answer=f'{",".join(map(str, sh))}: {len(sh)} occupied shells → period {len(sh)}; {sh[-1]} outer electrons → ' + ('positive ions (loses electrons)' if sh[-1] <= 3 else 'negative ions (gains electrons)' if sh[-1] >= 5 else 'tends to share electrons (covalent) rather than form ions'),
                markingKey='1 correct arrangement; 1 number of shells = period; 1 outer electrons decide ion charge (≤3 lose → positive, ≥5 gain → negative, 4 → shares).', type='explain', marks=3)


# =============================================================================================
# ch05 Chemical Bonding and Structure
# =============================================================================================
R.facts('ch05-st1', F(
    terms=[('ionic bond', 'the strong electrostatic attraction between oppositely charged ions'),
           ('cation', 'a positively charged ion, formed when an atom loses electrons (usually a metal)'),
           ('anion', 'a negatively charged ion, formed when an atom gains electrons (usually a non-metal)'),
           ('dot-and-cross diagram', 'a diagram showing the outer-shell electrons of the atoms or ions in a substance, with electrons from different atoms shown as dots and crosses'),
           ('ionic lattice', 'a regular three-dimensional arrangement of alternating positive and negative ions')],
    facts=[('Ionic bonding usually occurs between which types of element?', 'A metal and a non-metal', ['Two non-metals', 'Two metals', 'A noble gas and a metal'], 'Metals lose electrons; non-metals gain them.'),
           ('What is the formula of the compound formed between magnesium and chlorine?', 'MgCl₂', ['MgCl', 'Mg₂Cl', 'Mg₂Cl₃'], 'Mg²⁺ needs two Cl⁻ ions to balance the charge.'),
           ('In forming sodium chloride, what happens to the electrons?', 'One electron is transferred from sodium to chlorine', ['A pair of electrons is shared', 'Chlorine gives an electron to sodium', 'Electrons become delocalised'], 'Na → Na⁺ + e⁻; Cl + e⁻ → Cl⁻.'),
           ('What is the charge on an aluminium ion?', '3+', ['3−', '2+', '1+'], 'Al (2,8,3) loses three outer electrons.')],
    why=[('Explain why sodium and chlorine form an ionic compound.', 'Sodium (2,8,1) loses its single outer electron to form Na⁺ (2,8); chlorine (2,8,7) gains that electron to form Cl⁻ (2,8,8); both have full outer shells and the oppositely charged ions attract strongly.'),
         ('Explain why the formula of calcium oxide is CaO but the formula of calcium chloride is CaCl₂.', 'Ca forms Ca²⁺; oxide is O²⁻, so one of each balances; chloride is Cl⁻, so two are needed to balance 2+.'),
         ('Explain why a dot-and-cross diagram of an ionic compound shows square brackets and charges.', 'Each ion is a separate charged particle; the brackets show the electrons belong to that ion and the charge shows how many electrons were lost or gained.')],
    contrast=[('a cation', 'an anion', 'A cation is a positive ion formed by losing electrons (e.g. Na⁺); an anion is a negative ion formed by gaining electrons (e.g. Cl⁻).'),
              ('ionic bonding', 'covalent bonding', 'Ionic bonding is the transfer of electrons from metal to non-metal, forming ions that attract; covalent bonding is the sharing of electron pairs between non-metal atoms.')],
    misc=[('In sodium chloride, sodium and chlorine share a pair of electrons.', 'Electrons are transferred, not shared: Na loses one and Cl gains one, forming ions held by electrostatic attraction.'),
          ('An ionic bond is a bond between one sodium ion and one chloride ion only.', 'Each ion is attracted to all neighbouring oppositely charged ions in all directions in the lattice.'),
          ('Metals gain electrons to form negative ions.', 'Metals lose outer electrons to form positive ions.')],
    evaluate=[('Dot-and-cross diagrams are a useful model of ionic bonding.', ['show clearly which electrons are transferred and the resulting charges', 'help predict formulae'], ['electrons from different atoms are identical, so dots and crosses are artificial', 'do not show the 3D lattice or relative sizes of ions'], 'Useful for showing electron transfer and formula but limited; lattice diagrams are needed for structure.')],
    extended=[('Magnesium oxide (MgO) melts at 2852 °C but sodium chloride (NaCl) melts at 801 °C. Both are giant ionic lattices. Use ideas about the charges on the ions to explain the difference, and predict with a reason whether calcium oxide or potassium chloride has the higher melting point.', 'Mg²⁺ and O²⁻ carry double charges, so the electrostatic attraction between ions is much stronger than between Na⁺ and Cl⁻ (single charges) and more energy is needed to separate them. CaO (Ca²⁺, O²⁻) will have the higher melting point than KCl (K⁺, Cl⁻) for the same reason.', 5),
              ('A student says: "Sodium chloride is made of NaCl molecules." Evaluate this statement, using a description of the structure of sodium chloride and an explanation of what its formula means.', 'Incorrect: NaCl is a giant ionic lattice of Na⁺ and Cl⁻ ions; each Na⁺ is surrounded by 6 Cl⁻ and vice versa; there are no separate molecules. The formula NaCl shows the simplest ratio of ions (1 : 1), not a molecule. Molecules are found in covalent simple molecular substances.', 4)],
))


@R.add('ch05-st1', 'C3', (1, 5), 'short')
def ionic_formula(rng, slot):
    metal = rng.choice(['Li', 'Na', 'K', 'Mg', 'Ca', 'Al'])
    non = rng.choice(['O', 'S', 'F', 'Cl', 'N'])
    cm, cn = IONS[metal], -IONS[non]
    l = cm * cn // math.gcd(cm, cn)
    a, b = l // cm, l // cn
    sub = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
    formula = f'{metal}{"" if a == 1 else str(a).translate(sub)}{non}{"" if b == 1 else str(b).translate(sub)}'
    ending = {'O': 'oxide', 'S': 'sulfide', 'F': 'fluoride', 'Cl': 'chloride', 'N': 'nitride'}[non]
    cname = f'{ELEMENTS[metal][0]} {ending}'
    mz, nz = ELEMENTS[metal][1], ELEMENTS[non][1]
    if slot.d <= 2:
        return dict(stem=f'Use the charges on the ions ({metal}{_charge(cm)} and {non}{_charge(-cn)}) to write the formula of {cname}.', answer=formula,
                    markingKey=f'M1 charges balance: {a} × (+{cm}) + {b} × (−{cn}) = 0; A1 {formula}.', marks=2)
    return dict(stem=f'Describe, in terms of electrons, how {ELEMENTS[metal][0]} (atomic number {mz}) and {ELEMENTS[non][0]} (atomic number {nz}) react to form {cname}. Include the electron arrangements of the ions and the formula of the compound.',
                answer=f'Each {ELEMENTS[metal][0]} atom ({",".join(map(str, shells(mz)))}) loses {cm} electron(s) → {metal}{_charge(cm)} ({",".join(map(str, shells(mz - cm)))}); each {ELEMENTS[non][0]} atom ({",".join(map(str, shells(nz)))}) gains {cn} → {non}{_charge(-cn)} ({",".join(map(str, shells(nz + cn)))}); formula {formula}.',
                markingKey=f'1 electron transfer from metal to non-metal; 1 {metal}{_charge(cm)} with arrangement {",".join(map(str, shells(mz - cm)))}; 1 {non}{_charge(-cn)} with arrangement {",".join(map(str, shells(nz + cn)))}; 1 ratio {a} : {b} so {formula}; 1 ions held by electrostatic attraction.', marks=5)


dataset('ch05-st1',
        dict(intro='{who} measured the electrical current through solutions of sodium chloride of different concentrations using a 6 V supply and graphite electrodes.', iv=('Concentration of NaCl', 'g/dm³'), xs=[0, 5, 10, 15, 20],
             dv=('Current', 'mA'), f=lambda x: 2 + 9 * x, dp=0, trend='The current increases as the concentration of sodium chloride increases.',
             why='In solution the Na⁺ and Cl⁻ ions are free to move and carry charge; more concentrated solutions contain more ions per cm³.'))

inquiry('ch05-st1',
        dict(ctx='how the concentration of a salt solution affects how well it conducts electricity',
             iv='concentration of sodium chloride solution (g/dm³)', dv='current in mA measured with an ammeter in series with the electrodes',
             cvs=[('voltage of the power supply', 'higher voltage gives a larger current'), ('distance between and size of the electrodes', 'changes the resistance of the solution'), ('temperature of the solution', 'ions move faster when warmer'), ('depth the electrodes are dipped', 'changes the area in contact with solution')],
             hyp='If the concentration increases, then the current will increase, because there are more mobile ions to carry charge between the electrodes.',
             method='Make NaCl solutions of 0, 5, 10, 15, 20, 25 g/dm³; place 100 cm³ in a beaker; dip two graphite electrodes 3 cm apart to the same depth; connect to a 6 V supply and ammeter; read current after 30 s; rinse electrodes; repeat three times and calculate means.',
             weak=('the electrodes were moved closer together for some solutions', 'clamp the electrodes in a fixed holder so the distance stays at 3 cm'),
             safety='low-voltage supply only; small amounts of chlorine may form at the anode – ventilate the room and keep runs short'))

R.facts('ch05-st2', F(
    terms=[('covalent bond', 'a shared pair of electrons between two non-metal atoms'),
           ('molecule', 'two or more atoms joined together by covalent bonds'),
           ('double bond', 'a covalent bond in which two pairs of electrons are shared between two atoms, e.g. O=O'),
           ('lone pair', 'a pair of outer-shell electrons that is not involved in bonding')],
    facts=[('How many covalent bonds does a carbon atom form in methane, CH₄?', '4', ['2', '1', '3'], 'Carbon has 4 outer electrons and shares each with a hydrogen.'),
           ('How many shared pairs of electrons are in a molecule of nitrogen, N₂?', '3', ['1', '2', '4'], 'N≡N is a triple bond.'),
           ('Which substance contains a double covalent bond?', 'Oxygen, O₂', ['Hydrogen, H₂', 'Chlorine, Cl₂', 'Hydrogen chloride, HCl'], 'O=O: two shared pairs.'),
           ('How many lone pairs does the oxygen atom in a water molecule have?', '2', ['0', '1', '4'], 'Oxygen has 6 outer electrons: 2 in bonds with H, 4 as two lone pairs.')],
    why=[('Explain why atoms form covalent bonds.', 'By sharing pairs of electrons, each atom gains a full outer shell (stable noble-gas arrangement); the shared pair is attracted to both nuclei, holding the atoms together.'),
         ('Explain why hydrogen forms only one covalent bond.', 'Hydrogen has one electron and its only shell holds two, so it needs to share one more electron – one bond.'),
         ('Explain why simple molecular substances have low melting points even though covalent bonds are strong.', 'Melting only overcomes the weak intermolecular forces between molecules, not the strong covalent bonds within them.')],
    contrast=[('a single covalent bond', 'a double covalent bond', 'A single bond is one shared pair of electrons (e.g. H–H); a double bond is two shared pairs (e.g. O=O, C=O in CO₂).'),
              ('covalent bonds', 'intermolecular forces', 'Covalent bonds are strong bonds within a molecule (shared electrons); intermolecular forces are weak attractions between separate molecules.')],
    misc=[('When water boils, the covalent bonds between hydrogen and oxygen atoms break.', 'Boiling overcomes the forces between water molecules; the H₂O molecules stay intact.'),
          ('In a covalent bond one atom gives an electron to the other.', 'In a covalent bond electrons are shared; transfer of electrons forms ionic bonds.')],
    evaluate=[('Ball-and-stick models give a better picture of molecules than dot-and-cross diagrams.', ['show the 3D shape and bond angles', 'show which atoms are bonded'], ['do not show electrons or lone pairs', 'sticks suggest bonds are physical rods; atoms are not hard balls', 'relative sizes are wrong'], 'Each model shows different features; scientists choose the model that best fits the question.')],
    extended=[('Carbon dioxide (CO₂) and silicon dioxide (SiO₂) have similar formulae, but CO₂ is a gas at room temperature and SiO₂ melts at about 1700 °C. Explain this difference in terms of structure and bonding.', 'CO₂ is simple molecular: small O=C=O molecules with strong covalent bonds inside but weak intermolecular forces between molecules, so little energy is needed to separate them. SiO₂ is giant covalent: every Si is bonded to 4 O atoms in a 3D network, so melting needs many strong covalent bonds to be broken.', 5),
              ('Draw dot-and-cross diagrams for ammonia (NH₃) and for methane (CH₄). Use them to explain why an ammonia molecule has one lone pair but methane has none, and predict which molecule has the larger bond angle.', 'N has 5 outer electrons: 3 shared with H atoms and 2 as a lone pair. C has 4 outer electrons, all shared with 4 H atoms. Methane has the larger bond angle (109.5°) because the lone pair in ammonia repels the bonding pairs more strongly, squeezing the angle to about 107°.', 5)],
))

MOLS = [('hydrogen', 'H₂', 1, 0, 'H–H'), ('chlorine', 'Cl₂', 1, 6, 'Cl–Cl'), ('hydrogen chloride', 'HCl', 1, 3, 'H–Cl'), ('water', 'H₂O', 2, 2, 'H–O–H'),
        ('ammonia', 'NH₃', 3, 1, 'three N–H bonds'), ('methane', 'CH₄', 4, 0, 'four C–H bonds'), ('oxygen', 'O₂', 2, 4, 'O=O'), ('nitrogen', 'N₂', 3, 2, 'N≡N'),
        ('carbon dioxide', 'CO₂', 4, 4, 'O=C=O'), ('hydrogen fluoride', 'HF', 1, 3, 'H–F'), ('ethene', 'C₂H₄', 6, 0, 'C=C plus four C–H'), ('hydrogen sulfide', 'H₂S', 2, 2, 'H–S–H')]


@R.add('ch05-st2', 'C3', (1, 4), 'short')
def mol_pairs(rng, slot):
    nm, f, bp, lp, desc = rng.choice(MOLS)
    k = rng.choice(['pairs', 'lone', 'describe'])
    if k == 'pairs':
        return dict(stem=f'Draw a dot-and-cross diagram for a molecule of {nm} ({f}), showing outer electrons only. How many shared pairs of electrons does it contain?', answer=f'{bp} ({desc})',
                    markingKey=f'1 correct number of shared pairs = {bp}; 1 every atom has a full outer shell (H 2, others 8); 1 lone pairs shown ({lp}).', marks=3)
    if k == 'lone':
        return dict(stem=f'State the total number of lone pairs on all the atoms in a molecule of {nm}, {f}, and the number of bonding pairs.', answer=f'{lp} lone pairs; {bp} bonding pairs',
                    markingKey=f'1 {bp} bonding pairs ({desc}); 1 {lp} lone pairs.', marks=2)
    return dict(stem=f'Describe the bonding in a molecule of {nm} ({f}) and explain why each atom is stable.', answer=f'{desc}: {bp} shared pair(s) of electrons; each atom achieves a full outer shell (H: 2, others: 8).',
                markingKey=f'1 covalent bonds: {desc}; 1 shared pairs between non-metal atoms; 1 full outer shells on every atom.', marks=3)


@R.add('ch05-st2', 'C1', (1, 3), 'mcq')
def mol_mcq(rng, slot):
    items = rng.sample(MOLS, 4)
    nm, f, bp, lp, desc = items[0]
    wrong = sorted({x[2] for x in MOLS} - {bp})
    if len(wrong) < 3:
        return None
    return mcq(rng, f'How many pairs of electrons are shared in one molecule of {nm}, {f}?', str(bp), [str(w) for w in rng.sample(wrong, 3)], f'{desc}.')


dataset('ch05-st2',
        dict(intro='{who} used published data to compare the boiling points of the simple molecular hydrides of group 14 (CH₄, SiH₄, GeH₄, SnH₄), measured three times by different laboratories.', iv=('Period', ''), xs=[2, 3, 4, 5],
             dv=('Boiling point', 'K'), f=lambda x: {2: 112, 3: 161, 4: 185, 5: 221}[x], dp=0, trend='Boiling point increases down the group from CH₄ to SnH₄.',
             why='The molecules get larger with more electrons, so the intermolecular forces between them get stronger and more energy is needed to separate them; covalent bonds are not broken.'))

inquiry('ch05-st2',
        dict(ctx='how the number of carbon atoms in an alcohol molecule affects the energy released when it burns (using spirit burners heating water)',
             iv='number of carbon atoms (methanol 1, ethanol 2, propanol 3, butanol 4, pentanol 5)', dv='temperature rise of 100 cm³ of water per gram of fuel burned – thermometer and mass of burner before/after on a 0.01 g balance',
             cvs=[('volume of water', 'same mass of water must be heated'), ('distance from flame to can', 'affects heat transfer'), ('use of a draught shield', 'reduces heat loss'), ('starting temperature of water', 'heat loss depends on temperature difference')],
             hyp='If the number of carbon atoms increases, then the energy released per gram will increase slightly, because larger molecules have more bonds to break and form, releasing more energy overall.',
             method='Weigh a spirit burner; place 100 cm³ water in a copper can 3 cm above the wick inside a draught shield; record temperature; burn until the temperature rises 20 °C; reweigh; calculate energy = 100 × 4.18 × ΔT and divide by mass burned; repeat three times for each alcohol.',
             weak=('no draught shield was used and the can was at different heights', 'use a draught shield and clamp the can at a fixed 3 cm above the wick'),
             safety='alcohols are highly flammable – keep bottles closed and away from flames; wear eye protection; tie hair back'))

R.facts('ch05-st3', F(
    terms=[('giant ionic structure', 'a lattice of millions of oppositely charged ions held by strong electrostatic forces in all directions, e.g. sodium chloride'),
           ('giant covalent structure', 'a huge network of atoms all joined by covalent bonds, e.g. diamond, graphite and silicon dioxide'),
           ('simple molecular structure', 'a substance made of small molecules held together by weak intermolecular forces, e.g. water, carbon dioxide'),
           ('allotrope', 'a different structural form of the same element in the same physical state, e.g. diamond, graphite and graphene')],
    facts=[('Which substance has a giant covalent structure?', 'Silicon dioxide', ['Sodium chloride', 'Carbon dioxide', 'Iodine'], 'SiO₂ (sand) is a network of Si–O bonds.'),
           ('Why does graphite conduct electricity?', 'Each carbon has one delocalised electron that can move between layers', ['It contains ions', 'It is a metal', 'Its layers are held by strong bonds'], 'Each C forms only three bonds.'),
           ('When does sodium chloride conduct electricity?', 'When molten or dissolved in water', ['When solid', 'Never', 'Only when solid and heated'], 'The ions must be free to move.'),
           ('Which property is typical of a simple molecular substance?', 'Low melting and boiling points', ['Conducts when solid', 'Very hard', 'High melting point'], 'Weak intermolecular forces are easily overcome.')],
    why=[('Explain why diamond is very hard and has a very high melting point.', 'Each carbon atom is covalently bonded to four others in a rigid giant 3D network; a lot of energy is needed to break the many strong covalent bonds.'),
         ('Explain why graphite is soft and slippery and used in pencils and lubricants.', 'Graphite has layers of carbon atoms in hexagons; the layers are held by weak forces, so they slide over each other easily.'),
         ('Explain why sodium chloride has a high melting point.', 'It is a giant ionic lattice; strong electrostatic attractions between oppositely charged ions act in all directions and need a lot of energy to overcome.'),
         ('Explain why solid ionic compounds do not conduct electricity but their solutions do.', 'In the solid, ions are fixed in the lattice and cannot move; when dissolved or molten the ions are free to move and carry charge.')],
    contrast=[('diamond', 'graphite', 'In diamond each carbon forms four bonds in a 3D network (hard, non-conductor); in graphite each carbon forms three bonds in layers with delocalised electrons (soft, conducts).'),
              ('a giant covalent structure', 'a simple molecular structure', 'In a giant covalent structure all atoms are linked by covalent bonds (very high melting point); in a simple molecular structure small molecules are held by weak intermolecular forces (low melting point).')],
    misc=[('Graphite conducts electricity because it contains ions.', 'Graphite has no ions; it conducts because of delocalised electrons between the layers.'),
          ('Carbon dioxide is a gas because its covalent bonds are weak.', 'The C=O bonds are strong; CO₂ is a gas because the forces between molecules are weak.')],
    cases=[('graphene, isolated by Geim and Novoselov in Manchester (2004)', 'They peeled single layers of carbon from graphite using sticky tape; graphene is one atom thick, very strong and conducts electricity.', 'how structure determines properties', 'A single layer of hexagonally bonded carbon has strong covalent bonds and delocalised electrons, giving strength and conductivity.'),
           ('silicon dioxide in sand and glass', 'Sand melts only above about 1700 °C, which is why glass-making needs very hot furnaces.', 'giant covalent structures', 'Every Si atom is bonded to four O atoms in a giant network, so many strong bonds must be broken to melt it.')],
    evaluate=[('Graphene will transform technology within the next ten years.', ['extremely strong, light and conductive; possible uses in batteries, flexible screens and water filters'], ['difficult and expensive to produce large defect-free sheets', 'other materials are already cheap and established', 'possible health effects of nanoparticles are not fully known'], 'Graphene has great potential but production and safety challenges mean change is likely to be gradual.')],
))

PROPS = [('sodium chloride', 801, 'conducts only when molten or dissolved', 'giant ionic'), ('magnesium oxide', 2852, 'conducts only when molten', 'giant ionic'),
         ('diamond', 3550, 'does not conduct', 'giant covalent'), ('silicon dioxide', 1710, 'does not conduct', 'giant covalent'), ('graphite', 3652, 'conducts when solid', 'giant covalent'),
         ('methane', -182, 'does not conduct', 'simple molecular'), ('sulfur (S₈)', 115, 'does not conduct', 'simple molecular'), ('iodine', 114, 'does not conduct', 'simple molecular'),
         ('water', 0, 'very poor conductor when pure', 'simple molecular'), ('copper', 1085, 'conducts when solid and liquid', 'giant metallic'), ('potassium bromide', 734, 'conducts only when molten or dissolved', 'giant ionic')]


@R.add('ch05-st3', 'C3', (1, 5), 'short')
def classify(rng, slot):
    letters = 'PQRS'
    items = rng.sample(PROPS, 4 if slot.d >= 3 else 1)
    if len(items) == 1:
        nm, mp, cond, st = items[0]
        return dict(stem=f'Substance X melts at {mp} °C and {cond}. Deduce the type of structure of X and explain your reasoning.', answer=f'{st} ({nm})',
                    markingKey=f'1 {st}; 1 melting point linked to strength of forces/bonds overcome; 1 conductivity linked to mobile charged particles (ions/electrons) or their absence.', marks=3)
    rows = '\n'.join(f'{l}: melting point {mp} °C; {cond}' for l, (nm, mp, cond, st) in zip(letters, items))
    ans = '; '.join(f'{l} {st}' for l, (nm, mp, cond, st) in zip(letters, items))
    return dict(stem=f'The table gives properties of four substances.\n{rows}\nClassify each substance as giant ionic, giant covalent, simple molecular or giant metallic, justifying each choice.', answer=ans,
                markingKey='1 per correct classification with a justification that uses both melting point and conductivity: ' + ans + '.', marks=4)


inquiry('ch05-st3',
        dict(ctx='how to identify the type of structure of four unlabelled white solids (sodium chloride, silicon dioxide, glucose and wax) by testing their properties',
             iv='the substance tested', dv='melting behaviour when heated, solubility in water and electrical conductivity of the solid and of any solution',
             cvs=[('mass of each sample (e.g. 0.5 g)', 'fair comparison of melting and dissolving'), ('volume and temperature of water', 'affects solubility'), ('heating time and Bunsen setting', 'affects whether melting is observed'), ('voltage of the conductivity tester', 'affects whether a current is detected')],
             hyp='If a solid has a giant ionic structure, then it will have a high melting point, dissolve in water and conduct only in solution; simple molecular solids will melt easily and not conduct; giant covalent solids will not melt or conduct.',
             method='Test 0.5 g of each solid: heat gently in a test tube for 2 min (does it melt?); add 0.5 g to 10 cm³ water and stir (does it dissolve?); test the solid and the solution with a 6 V conductivity tester and bulb; record in a results table and classify each.',
             safety='heat gently, point test tubes away from people, wear eye protection; wax is flammable'))

R.facts('ch05-st4', F(
    terms=[('metallic bonding', 'the electrostatic attraction between positive metal ions and a “sea” of delocalised electrons'),
           ('delocalised electrons', 'outer electrons that are not attached to a particular atom and can move freely through the structure'),
           ('alloy', 'a mixture of a metal with one or more other elements, usually other metals or carbon'),
           ('malleable', 'able to be hammered or pressed into shape without breaking'),
           ('ductile', 'able to be drawn out into wires'),
           ('density', 'mass per unit volume of a substance, ρ = m ÷ V')],
    facts=[('Why are metals good conductors of electricity?', 'Delocalised electrons can move through the structure', ['Metal ions move to the electrodes', 'They contain free protons', 'Their atoms share electron pairs'], 'Moving electrons carry charge.'),
           ('Which alloy is made mainly from iron and carbon?', 'Steel', ['Brass', 'Bronze', 'Solder'], 'Steel is iron with up to about 2% carbon.'),
           ('Brass is an alloy of which two metals?', 'Copper and zinc', ['Copper and tin', 'Iron and nickel', 'Lead and tin'], 'Bronze is copper and tin.'),
           ('Why is pure gold mixed with copper or silver to make jewellery?', 'Pure gold is too soft', ['Pure gold is too hard', 'To make it conduct heat', 'To make it magnetic'], '24-carat gold bends and scratches easily.')],
    why=[('Explain why metals are malleable.', 'The positive ions are arranged in regular layers; the layers can slide over each other when a force is applied while the delocalised electrons keep holding them together.'),
         ('Explain why alloys are harder than pure metals.', 'Atoms of the added element are a different size, distorting the regular layers so they cannot slide over each other as easily.'),
         ('Explain why metals have high melting points.', 'There are strong electrostatic attractions between the positive ions and the delocalised electrons throughout the giant structure, needing a lot of energy to overcome.'),
         ('Explain why metals are good conductors of heat.', 'Delocalised electrons gain kinetic energy and move through the metal, transferring energy quickly; vibrating ions also pass energy on.')],
    contrast=[('a pure metal', 'an alloy', 'A pure metal has identical atoms in regular layers that slide easily (soft); an alloy contains atoms of different sizes that distort the layers, making it harder and stronger.'),
              ('metallic bonding', 'ionic bonding', 'Metallic bonding is between positive ions and delocalised electrons in a metal; ionic bonding is between positive and negative ions formed by electron transfer.')],
    misc=[('Metals conduct electricity because their ions move through the metal.', 'The ions are fixed in place; delocalised electrons move and carry the current.'),
          ('An alloy is a compound of two metals with a fixed formula.', 'An alloy is a mixture; its composition can vary (e.g. 18-carat vs 9-carat gold).')],
    cases=[('aluminium-lithium alloys in aircraft (e.g. Airbus A350)', 'Adding lithium makes aluminium lighter and stiffer, reducing aircraft mass and fuel use.', 'alloys having improved properties', 'Different-sized Li atoms disrupt the layers (stronger) and lithium’s low density reduces the overall density.'),
           ('nitinol, a nickel-titanium “shape memory” alloy', 'Dental braces and stents made of nitinol return to their original shape when warmed to body temperature.', 'how alloy structure gives useful properties', 'The arrangement of the two kinds of atom can change and switch back, a property neither pure metal has.')],
    evaluate=[('Recycling metals is always better than extracting new metal from ores.', ['saves energy (recycling aluminium uses about 95% less energy)', 'conserves finite ores and reduces mining damage', 'less landfill'], ['collection and sorting cost money and energy', 'alloys and mixed metals are hard to separate', 'some metals are used in tiny amounts in electronics, making recovery difficult'], 'Recycling is usually better, especially for aluminium and steel, but economics and separation limit it for some metals.')],
))


@R.add('ch05-st4', 'C3', (1, 5), 'numerical')
def density(rng, slot):
    mats = [('aluminium', 2.70), ('iron', 7.87), ('copper', 8.96), ('brass', 8.50), ('lead', 11.3), ('gold', 19.3), ('titanium', 4.51), ('stainless steel', 8.00), ('zinc', 7.13), ('silver', 10.5)]
    nm, rho = rng.choice(mats)
    who = name(rng)
    k = rng.choice(['rho', 'mass', 'block', 'displace', 'identify'] if slot.d >= 3 else ['rho', 'mass', 'block'])
    if k == 'rho':
        v = rng.choice([5.0, 8.0, 12.5, 20.0, 25.0, 40.0])
        m = round(rho * v, 1)
        return dict(stem=f'A sample of {nm} has a mass of {m} g and a volume of {v} cm³. Calculate its density in g/cm³.', answer=f'{m / v:.2f} g/cm³',
                    markingKey=f'M1 ρ = m ÷ V = {m} ÷ {v}; A1 {m / v:.2f} g/cm³.', marks=2)
    if k == 'mass':
        v = rng.choice([15, 30, 45, 60, 120])
        return dict(stem=f'The density of {nm} is {rho} g/cm³. Calculate the mass of a {nm} component with a volume of {v} cm³.', answer=f'{rho * v:.4g} g',
                    markingKey=f'M1 m = ρ × V = {rho} × {v}; A1 {rho * v:.4g} g.', marks=2)
    if k == 'block':
        a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(1, 4)
        v = a * b * c
        m = rho * v
        return dict(stem=f'{who} measures a rectangular block of {nm}: {a} cm × {b} cm × {c} cm, with mass {m:.1f} g. Calculate the density of the block in g/cm³ and in kg/m³.', answer=f'{m / v:.2f} g/cm³ = {m / v * 1000:.0f} kg/m³',
                    markingKey=f'M1 V = {a} × {b} × {c} = {v} cm³; M1 ρ = {m:.1f} ÷ {v}; A1 {m / v:.2f} g/cm³; A1 × 1000 = {m / v * 1000:.0f} kg/m³.', marks=4)
    if k == 'displace':
        v0 = rng.choice([40.0, 50.0, 60.0])
        dv = rng.choice([6.0, 8.0, 10.0, 12.0])
        m = round(rho * dv, 1)
        return dict(stem=f'An irregular piece of metal of mass {m} g is lowered into a measuring cylinder; the water level rises from {v0} cm³ to {v0 + dv} cm³. Calculate the density of the metal and use the table (aluminium 2.70, titanium 4.51, iron 7.87, copper 8.96, silver 10.5, lead 11.3, gold 19.3 g/cm³; brass 8.50, stainless steel 8.00, zinc 7.13) to suggest what it is.',
                    answer=f'{m / dv:.2f} g/cm³; {nm}', markingKey=f'M1 V = {v0 + dv} − {v0} = {dv} cm³ (displacement); M1 ρ = {m} ÷ {dv}; A1 {m / dv:.2f} g/cm³; 1 closest match {nm}.', marks=4)
    karat = rng.choice([(18, 0.75), (14, 0.585), (9, 0.375)])
    frac = karat[1]
    other, ro = rng.choice([('copper', 8.96), ('silver', 10.5)])
    rho_alloy = 1 / (frac / 19.3 + (1 - frac) / ro)
    m = rng.choice([5.0, 8.0, 10.0])
    return dict(stem=f'A {karat[0]}-carat gold ring is {frac * 100:g}% gold and {100 - frac * 100:g}% {other} by mass. Its mass is {m} g. Densities: gold 19.3 g/cm³, {other} {ro} g/cm³. (a) Calculate the volume of gold and of {other} in the ring. (b) Calculate the density of the alloy. (c) Explain how density measurement could detect a fake ring.',
                answer=f'(a) gold {m * frac / 19.3:.3f} cm³, {other} {m * (1 - frac) / ro:.3f} cm³ (b) {rho_alloy:.1f} g/cm³ (c) a fake made of cheaper metal would have a different (usually lower) density',
                markingKey=f'(a) M1 V = m ÷ ρ for each: {m * frac:.2f}/19.3 and {m * (1 - frac):.2f}/{ro}; A1 both. (b) M1 total mass ÷ total volume; A1 {rho_alloy:.1f} g/cm³. (c) 1 compare measured density with expected value.', marks=5)


dataset('ch05-st4',
        dict(intro='{who} added different percentages of tin to copper to make bronze samples and measured their hardness with a school hardness tester (depth of indentation).', iv=('Tin content', '%'), xs=[0, 4, 8, 12, 16],
             dv=('Indentation depth', 'mm'), f=lambda x: 1.6 - 0.07 * x, dp=2, trend='Indentation depth decreases as the percentage of tin increases, so the alloy gets harder.',
             why='Tin atoms are a different size from copper atoms and distort the layers, so layers cannot slide as easily.'))

inquiry('ch05-st4',
        dict(ctx='how the percentage of zinc in brass affects its hardness',
             iv='percentage of zinc in the brass (%)', dv='hardness – diameter of the dent made by dropping a 500 g steel ball from 1.0 m, measured with vernier callipers',
             cvs=[('drop height and mass of the ball', 'more energy makes a bigger dent'), ('thickness and size of samples', 'thin samples bend'), ('temperature of samples', 'metals soften when hot'), ('surface the sample rests on', 'a soft surface absorbs energy')],
             hyp='If the zinc percentage increases (up to about 40%), then the brass will be harder and the dent smaller, because zinc atoms are a different size and disrupt the layers of copper atoms.',
             method='Obtain brass samples of 0, 10, 20, 30 and 40% zinc, each 5 mm thick, on a steel anvil; drop a 500 g ball bearing from 1.0 m through a guide tube; measure the dent diameter with callipers; repeat 3 times on different spots; calculate the mean.',
             weak=('the ball was dropped by hand from roughly 1 m', 'use a clamped guide tube so every drop is from exactly 1.0 m'),
             safety='wear eye protection and keep feet clear of falling ball'))


# =============================================================================================
# ch06 Chemical Equations and Reaction Types
# =============================================================================================
import re as _re

AR = {'H': 1, 'C': 12, 'N': 14, 'O': 16, 'Na': 23, 'Mg': 24, 'Al': 27, 'S': 32, 'Cl': 35.5, 'K': 39, 'Ca': 40, 'Fe': 56, 'Cu': 63.5, 'Zn': 65, 'Br': 80, 'Ag': 108, 'Pb': 207, 'P': 31, 'Li': 7, 'I': 127}
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
UNSUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')


def parse_formula(f):
    f = f.translate(UNSUB)
    def parse(s, i=0):
        out = {}
        while i < len(s):
            if s[i] == '(':
                inner, i = parse(s, i + 1)
                m = _re.match(r'\d+', s[i:])
                k = int(m.group()) if m else 1
                i += len(m.group()) if m else 0
                for e, n in inner.items():
                    out[e] = out.get(e, 0) + n * k
            elif s[i] == ')':
                return out, i + 1
            else:
                m = _re.match(r'([A-Z][a-z]?)(\d*)', s[i:])
                e, n = m.group(1), int(m.group(2) or 1)
                out[e] = out.get(e, 0) + n
                i += len(m.group())
        return out, i
    return parse(f)[0]


def mr(f):
    return sum(AR[e] * n for e, n in parse_formula(f).items())


# (reactants, products) with coefficients – all checked by atom balance at import time.
EQUATIONS = [
    ([(2, 'H2'), (1, 'O2')], [(2, 'H2O')], 'hydrogen + oxygen → water'),
    ([(2, 'Mg'), (1, 'O2')], [(2, 'MgO')], 'magnesium + oxygen → magnesium oxide'),
    ([(1, 'CH4'), (2, 'O2')], [(1, 'CO2'), (2, 'H2O')], 'methane + oxygen → carbon dioxide + water'),
    ([(1, 'N2'), (3, 'H2')], [(2, 'NH3')], 'nitrogen + hydrogen → ammonia'),
    ([(2, 'Na'), (1, 'Cl2')], [(2, 'NaCl')], 'sodium + chlorine → sodium chloride'),
    ([(4, 'Al'), (3, 'O2')], [(2, 'Al2O3')], 'aluminium + oxygen → aluminium oxide'),
    ([(1, 'CaCO3')], [(1, 'CaO'), (1, 'CO2')], 'calcium carbonate → calcium oxide + carbon dioxide'),
    ([(2, 'H2O2')], [(2, 'H2O'), (1, 'O2')], 'hydrogen peroxide → water + oxygen'),
    ([(1, 'Zn'), (2, 'HCl')], [(1, 'ZnCl2'), (1, 'H2')], 'zinc + hydrochloric acid → zinc chloride + hydrogen'),
    ([(1, 'Mg'), (2, 'HCl')], [(1, 'MgCl2'), (1, 'H2')], 'magnesium + hydrochloric acid → magnesium chloride + hydrogen'),
    ([(2, 'Na'), (2, 'H2O')], [(2, 'NaOH'), (1, 'H2')], 'sodium + water → sodium hydroxide + hydrogen'),
    ([(1, 'C3H8'), (5, 'O2')], [(3, 'CO2'), (4, 'H2O')], 'propane + oxygen → carbon dioxide + water'),
    ([(1, 'Fe2O3'), (3, 'CO')], [(2, 'Fe'), (3, 'CO2')], 'iron(III) oxide + carbon monoxide → iron + carbon dioxide'),
    ([(1, 'CuO'), (1, 'H2SO4')], [(1, 'CuSO4'), (1, 'H2O')], 'copper(II) oxide + sulfuric acid → copper(II) sulfate + water'),
    ([(1, 'NaOH'), (1, 'HCl')], [(1, 'NaCl'), (1, 'H2O')], 'sodium hydroxide + hydrochloric acid → sodium chloride + water'),
    ([(2, 'KOH'), (1, 'H2SO4')], [(1, 'K2SO4'), (2, 'H2O')], 'potassium hydroxide + sulfuric acid → potassium sulfate + water'),
    ([(1, 'CaCO3'), (2, 'HCl')], [(1, 'CaCl2'), (1, 'H2O'), (1, 'CO2')], 'calcium carbonate + hydrochloric acid → calcium chloride + water + carbon dioxide'),
    ([(1, 'Fe'), (1, 'CuSO4')], [(1, 'FeSO4'), (1, 'Cu')], 'iron + copper(II) sulfate → iron(II) sulfate + copper'),
    ([(2, 'Al'), (3, 'CuCl2')], [(2, 'AlCl3'), (3, 'Cu')], 'aluminium + copper(II) chloride → aluminium chloride + copper'),
    ([(1, 'C6H12O6'), (6, 'O2')], [(6, 'CO2'), (6, 'H2O')], 'glucose + oxygen → carbon dioxide + water (respiration)'),
    ([(2, 'KI'), (1, 'Cl2')], [(2, 'KCl'), (1, 'I2')], 'potassium iodide + chlorine → potassium chloride + iodine'),
    ([(1, 'Pb(NO3)2'), (2, 'KI')], [(1, 'PbI2'), (2, 'KNO3')], 'lead(II) nitrate + potassium iodide → lead(II) iodide + potassium nitrate'),
    ([(2, 'Cu(NO3)2')], [(2, 'CuO'), (4, 'NO2'), (1, 'O2')], 'copper(II) nitrate → copper(II) oxide + nitrogen dioxide + oxygen'),
    ([(1, 'C2H5OH'), (3, 'O2')], [(2, 'CO2'), (3, 'H2O')], 'ethanol + oxygen → carbon dioxide + water'),
    ([(2, 'Fe'), (3, 'Cl2')], [(2, 'FeCl3')], 'iron + chlorine → iron(III) chloride'),
    ([(1, 'Ca'), (2, 'H2O')], [(1, 'Ca(OH)2'), (1, 'H2')], 'calcium + water → calcium hydroxide + hydrogen'),
    ([(1, 'AgNO3'), (1, 'NaCl')], [(1, 'AgCl'), (1, 'NaNO3')], 'silver nitrate + sodium chloride → silver chloride + sodium nitrate'),
    ([(2, 'Mg'), (1, 'CO2')], [(2, 'MgO'), (1, 'C')], 'magnesium + carbon dioxide → magnesium oxide + carbon'),
    ([(6, 'CO2'), (6, 'H2O')], [(1, 'C6H12O6'), (6, 'O2')], 'carbon dioxide + water → glucose + oxygen (photosynthesis)'),
    ([(1, 'Zn'), (1, 'CuSO4')], [(1, 'ZnSO4'), (1, 'Cu')], 'zinc + copper(II) sulfate → zinc sulfate + copper'),
]


def _atoms(side):
    tot = {}
    for k, f in side:
        for e, n in parse_formula(f).items():
            tot[e] = tot.get(e, 0) + k * n
    return tot


for _l, _r, _w in EQUATIONS:
    assert _atoms(_l) == _atoms(_r), _w


def eq_text(side, coeffs=True):
    return ' + '.join((f'{k}' if coeffs and k > 1 else '') + f.translate(SUB) for k, f in side)


R.facts('ch06-st1', F(
    terms=[('chemical formula', 'symbols and subscript numbers that show the elements in a substance and the ratio of their atoms or ions'),
           ('balanced equation', 'a symbol equation with the same number of atoms of each element on both sides'),
           ('law of conservation of mass', 'in a chemical reaction no atoms are created or destroyed, so the total mass of reactants equals the total mass of products'),
           ('reactant', 'a substance present at the start of a reaction that is used up'),
           ('product', 'a new substance formed in a chemical reaction')],
    facts=[('How many atoms in total are in one formula unit of Ca(OH)₂?', '5', ['4', '3', '6'], '1 Ca + 2 O + 2 H = 5.'),
           ('Why must chemical equations be balanced?', 'Atoms are not created or destroyed in a reaction', ['To make the products heavier', 'To show the reaction is fast', 'Because molecules are conserved'], 'Mass is conserved.'),
           ('What is the formula of the sulfate ion?', 'SO₄²⁻', ['SO₃²⁻', 'S²⁻', 'SO₄⁻'], 'Sulfate is SO₄²⁻; sulfite is SO₃²⁻.'),
           ('What is the formula of calcium nitrate?', 'Ca(NO₃)₂', ['CaNO₃', 'Ca₂NO₃', 'Ca(NO₃)₃'], 'Ca²⁺ needs two NO₃⁻ ions.')],
    why=[('Explain why you must not change the small subscript numbers in formulae when balancing an equation.', 'Changing a subscript changes the substance itself (e.g. H₂O to H₂O₂); only the large coefficients in front of formulae may be changed.'),
         ('Explain why the mass seems to decrease when calcium carbonate is heated in an open crucible.', 'Carbon dioxide gas is produced and escapes into the air; the total mass of all products, including the gas, equals the mass of reactants.'),
         ('Explain why brackets are needed in the formula Mg(OH)₂.', 'The subscript 2 applies to the whole hydroxide ion (one O and one H); without brackets MgOH₂ would mean one O and two H.')],
    misc=[('To balance H₂ + O₂ → H₂O, change the formula of water to H₂O₂.', 'Changing the formula changes the substance; put coefficients in front instead: 2H₂ + O₂ → 2H₂O.'),
          ('Mass is lost when magnesium burns because the flame uses it up.', 'Mass increases: magnesium combines with oxygen from the air to form magnesium oxide; no mass is lost.')],
    evaluate=[('Word equations are just as useful as balanced symbol equations.', ['easier to read for non-chemists', 'name the substances clearly'], ['do not show the ratio of particles reacting', 'cannot be used to calculate masses of reactants and products', 'do not show conservation of atoms'], 'Word equations are useful for identification, but balanced symbol equations are needed for quantitative chemistry.')],
))


@R.add('ch06-st1', 'C3', (1, 5), 'short')
def balance(rng, slot):
    pool = EQUATIONS if slot.d >= 3 else [e for e in EQUATIONS if sum(k for k, _ in e[0] + e[1]) <= 6]
    l, r_, w = rng.choice(pool)
    k = rng.choice(['bal', 'word'] if slot.d >= 3 else ['bal'])
    bal = f'{eq_text(l)} → {eq_text(r_)}'
    if k == 'bal':
        return dict(stem=f'Balance the equation: {eq_text(l, False)} → {eq_text(r_, False)}', answer=bal,
                    markingKey=f'{bal}. 1 correct coefficients for each side; 1 check: atoms of each element equal on both sides (' + ', '.join(f'{e} {n}' for e, n in _atoms(l).items()) + ').', marks=2 if slot.d <= 2 else 3)
    return dict(stem=f'Write a balanced symbol equation for the reaction: {w}.', answer=bal,
                markingKey=f'1 correct formulae for all substances; 1-2 correct balancing: {bal}.', marks=3)


@R.add('ch06-st1', 'C3', (2, 5), 'short')
def count_atoms(rng, slot):
    l, r_, w = rng.choice(EQUATIONS)
    side = rng.choice([l, r_])
    tot = _atoms(side)
    txt = ', '.join(f'{e}: {n}' for e, n in tot.items())
    return dict(stem=f'In the balanced equation {eq_text(l)} → {eq_text(r_)}, count the number of atoms of each element on the {"left" if side is l else "right"}-hand side, and explain why it must equal the number on the other side.',
                answer=f'{txt}; atoms are rearranged, not created or destroyed', markingKey=f'1-2 counts ({txt}), multiplying subscripts by coefficients; 1 conservation of atoms/mass.', marks=3)


R.facts('ch06-st2', F(
    terms=[('state symbol', 'a symbol in an equation showing the physical state: (s) solid, (l) liquid, (g) gas, (aq) aqueous solution'),
           ('synthesis reaction', 'a reaction in which two or more substances combine to form one product, e.g. 2Mg + O₂ → 2MgO'),
           ('decomposition reaction', 'a reaction in which one compound breaks down into two or more simpler substances, often by heating (thermal decomposition)'),
           ('displacement reaction', 'a reaction in which a more reactive element takes the place of a less reactive element in a compound'),
           ('precipitation reaction', 'a reaction between two solutions that forms an insoluble solid (precipitate)'),
           ('neutralisation', 'the reaction of an acid with a base to form a salt and water')],
    facts=[('What does the state symbol (aq) mean?', 'Dissolved in water', ['Liquid', 'Gas', 'Solid in water'], 'Aqueous = in solution in water.'),
           ('Which type of reaction is CaCO₃ → CaO + CO₂?', 'Thermal decomposition', ['Synthesis', 'Displacement', 'Neutralisation'], 'One compound breaks down on heating.'),
           ('Which type of reaction is Zn + CuSO₄ → ZnSO₄ + Cu?', 'Displacement', ['Decomposition', 'Synthesis', 'Combustion'], 'Zinc displaces less reactive copper.'),
           ('What is seen when silver nitrate solution is added to sodium chloride solution?', 'A white precipitate forms', ['A yellow precipitate forms', 'Bubbles of gas', 'No change'], 'Silver chloride is an insoluble white solid.')],
    why=[('Explain why state symbols are useful in equations.', 'They show the physical state of each substance, which tells you, for example, whether a gas is given off, a precipitate forms or a substance is in solution – information needed to carry out or understand the reaction.'),
         ('Explain why the reaction of magnesium with oxygen is described as a synthesis reaction.', 'Two elements combine to form a single new compound, magnesium oxide.'),
         ('Explain why a precipitation reaction can be used to make an insoluble salt.', 'Mixing two soluble salts swaps the ions; the insoluble product forms as a solid that can be filtered, washed and dried.')],
    contrast=[('a synthesis reaction', 'a decomposition reaction', 'Synthesis combines two or more substances into one product; decomposition breaks one compound into two or more simpler substances.'),
              ('(l)', '(aq)', '(l) is a pure liquid such as water or molten metal; (aq) is a substance dissolved in water.')],
    misc=[('Water in an equation should always be written H₂O(aq).', 'Pure water is a liquid, H₂O(l); (aq) means dissolved in water.'),
          ('Displacement reactions only happen between metals and acids.', 'Displacement happens whenever a more reactive element replaces a less reactive one in a compound, e.g. metals in salt solutions or halogens in halide solutions.')],
    cases=[('the thermite reaction used to weld railway tracks', 'Aluminium powder reacts with iron(III) oxide, producing molten iron that runs into the gap between rails: 2Al + Fe₂O₃ → Al₂O₃ + 2Fe.', 'displacement reactions', 'Aluminium is more reactive than iron, so it takes the oxygen and displaces iron; the reaction releases so much heat that the iron is molten.'),
           ('lime kilns', 'For thousands of years limestone (CaCO₃) has been heated in kilns to make quicklime (CaO) for mortar and agriculture.', 'thermal decomposition', 'Heat breaks calcium carbonate into calcium oxide and carbon dioxide.')],
    evaluate=[('Cement production, which depends on decomposing limestone, should be heavily taxed because of its carbon dioxide emissions.', ['cement causes about 8% of global CO₂ emissions, from decomposition of CaCO₃ and fuel burning', 'tax encourages low-carbon alternatives and carbon capture'], ['cement is essential for housing and infrastructure, especially in developing countries', 'costs passed to consumers', 'alternatives are not yet available at scale'], 'A carbon price is justified, but should be combined with support for new technologies and developing economies.')],
))

TYPED = [(e, t) for e, t in zip(EQUATIONS, ['synthesis (also combustion: hydrogen burning in oxygen)', 'synthesis (also combustion: magnesium burning in oxygen)', 'combustion', 'synthesis', 'synthesis', 'synthesis (also combustion: aluminium burning in oxygen)', 'decomposition', 'decomposition', 'displacement', 'displacement',
                                            'displacement', 'combustion', 'displacement (reduction)', 'neutralisation', 'neutralisation', 'neutralisation', 'neutralisation (acid + carbonate)', 'displacement', 'displacement', 'combustion (respiration)',
                                            'displacement', 'precipitation', 'decomposition', 'combustion', 'synthesis', 'displacement', 'precipitation', 'displacement', None, 'displacement']) if t]
STATES = {'H2': 'g', 'O2': 'g', 'H2O': 'l', 'Mg': 's', 'MgO': 's', 'CH4': 'g', 'CO2': 'g', 'N2': 'g', 'NH3': 'g', 'Na': 's', 'Cl2': 'g', 'NaCl': 'aq', 'Al': 's', 'Al2O3': 's',
          'CaCO3': 's', 'CaO': 's', 'H2O2': 'aq', 'Zn': 's', 'HCl': 'aq', 'ZnCl2': 'aq', 'MgCl2': 'aq', 'NaOH': 'aq', 'Fe': 's', 'CuSO4': 'aq', 'FeSO4': 'aq', 'Cu': 's', 'CuCl2': 'aq',
          'AlCl3': 'aq', 'KI': 'aq', 'KCl': 'aq', 'I2': 'aq', 'Pb(NO3)2': 'aq', 'PbI2': 's', 'KNO3': 'aq', 'AgNO3': 'aq', 'AgCl': 's', 'NaNO3': 'aq', 'ZnSO4': 'aq', 'CaCl2': 'aq', 'CuO': 's', 'H2SO4': 'aq', 'KOH': 'aq', 'K2SO4': 'aq'}


@R.add('ch06-st2', 'C3', (1, 4), 'short')
def classify_rxn(rng, slot):
    (l, r_, w), t = rng.choice(TYPED)
    eq = f'{eq_text(l)} → {eq_text(r_)}'
    return dict(stem=f'Classify the reaction {eq} as synthesis, decomposition, displacement, neutralisation, precipitation or combustion, and justify your choice.', answer=t,
                markingKey=f'1 {t}; 1 justification from the equation (e.g. number of reactants/products, element replacing another, acid + base, insoluble product, burning in oxygen).', marks=2)


@R.add('ch06-st2', 'C3', (2, 5), 'short')
def add_states(rng, slot):
    cands = [(l, r_, w) for l, r_, w in EQUATIONS if all(f in STATES for _, f in l + r_) and not w.startswith('sodium + chlorine')]
    l, r_, w = rng.choice(cands)
    def st(side):
        return ' + '.join((f'{k}' if k > 1 else '') + f.translate(SUB) + f'({STATES[f]})' for k, f in side)
    ans = f'{st(l)} → {st(r_)}'
    return dict(stem=f'Add state symbols to this equation for a reaction carried out at room temperature (water as solvent where needed): {eq_text(l)} → {eq_text(r_)}', answer=ans,
                markingKey=f'{ans}. 1 mark per two correct state symbols (max 3). Note: water as a liquid product is (l); dissolved ionic salts and acids are (aq); insoluble salts/metals/oxides (s).', marks=3)


R.facts('ch06-st3', F(
    terms=[('reactivity series', 'a list of metals arranged in order of how readily they react, from most to least reactive'),
           ('oxidation', 'the gain of oxygen (or the loss of electrons) by a substance'),
           ('reduction', 'the loss of oxygen (or the gain of electrons) by a substance'),
           ('ore', 'a rock containing enough of a metal compound to make extraction of the metal economic')],
    facts=[('Which metal is the most reactive?', 'Potassium', ['Magnesium', 'Iron', 'Copper'], 'K > Na > Ca > Mg > Al > Zn > Fe > Cu > Ag > Au.'),
           ('Which metal can be extracted from its oxide by heating with carbon?', 'Iron', ['Aluminium', 'Sodium', 'Magnesium'], 'Carbon is more reactive than iron but less reactive than Al, Mg and Na.'),
           ('What would be seen when an iron nail is placed in blue copper(II) sulfate solution?', 'A pink-brown coating forms and the blue colour fades', ['No change', 'The nail dissolves completely and the solution turns red', 'Bubbles of hydrogen and a white precipitate'], 'Iron displaces copper.'),
           ('How is aluminium extracted from its ore?', 'Electrolysis of molten aluminium oxide', ['Heating with carbon', 'Dissolving in water', 'Panning in rivers'], 'Aluminium is more reactive than carbon.')],
    why=[('Explain why gold is found as the uncombined metal in the Earth’s crust.', 'Gold is very unreactive, so it does not readily react with oxygen, water or other substances and stays as the element.'),
         ('Explain why a displacement reaction can be used to place metals in order of reactivity.', 'A metal only displaces another metal from its compound if it is more reactive, so observing which reactions occur gives the order.'),
         ('Explain why aluminium is very reactive but aluminium window frames do not corrode.', 'Aluminium reacts with oxygen to form a thin, tough layer of aluminium oxide that sticks to the surface and stops further reaction.')],
    contrast=[('oxidation', 'reduction', 'Oxidation is gain of oxygen or loss of electrons; reduction is loss of oxygen or gain of electrons; they always happen together (redox).')],
    misc=[('Copper displaces zinc from zinc sulfate solution because copper is a metal too.', 'Copper is less reactive than zinc so no reaction occurs; zinc would displace copper.'),
          ('In Fe₂O₃ + 3CO → 2Fe + 3CO₂, iron oxide is oxidised.', 'Iron oxide loses oxygen, so it is reduced; carbon monoxide gains oxygen and is oxidised.')],
    cases=[('the blast furnace in steelworks (e.g. in Jamshedpur, India)', 'Iron ore (Fe₂O₃) is heated with coke; carbon monoxide reduces the ore to molten iron.', 'the reactivity series and extraction', 'Carbon is above iron in the reactivity series, so it can remove oxygen from iron oxide.'),
           ('sacrificial zinc blocks on ships’ hulls', 'Blocks of zinc are bolted onto steel hulls and corrode away instead of the steel.', 'relative reactivity of metals', 'Zinc is more reactive than iron, so it loses electrons (is oxidised) in preference, protecting the iron.')],
    evaluate=[('Extracting metals by electrolysis is too expensive and should be replaced by recycling.', ['electrolysis uses huge amounts of electricity (aluminium smelting)', 'recycling aluminium saves about 95% of the energy'], ['recycling cannot meet all demand as consumption grows', 'electrolysis powered by hydroelectricity (e.g. Iceland, Norway) has low emissions', 'some metals cannot be extracted any other way'], 'Recycling should be maximised, but electrolysis remains necessary; its impact depends on the energy source.')],
))

SERIES = ['potassium', 'sodium', 'calcium', 'magnesium', 'aluminium', 'zinc', 'iron', 'lead', 'copper', 'silver', 'gold']
SALTS = {'magnesium': ('magnesium sulfate', 'colourless'), 'zinc': ('zinc sulfate', 'colourless'), 'iron': ('iron(II) sulfate', 'pale green'), 'copper': ('copper(II) sulfate', 'blue'),
         'silver': ('silver nitrate', 'colourless'), 'lead': ('lead(II) nitrate', 'colourless')}
METAL_LOOK = {'copper': 'pink-brown copper', 'silver': 'grey/silver crystals of silver', 'lead': 'grey lead', 'iron': 'dark grey iron', 'zinc': 'grey zinc', 'magnesium': 'grey magnesium'}


@R.add('ch06-st3', 'C3', (1, 5), 'short')
def displacement(rng, slot):
    metal = rng.choice(['magnesium', 'zinc', 'iron', 'copper', 'lead'])
    other = rng.choice([m for m in SALTS if m != metal])
    salt, col = SALTS[other]
    react = SERIES.index(metal) < SERIES.index(other)
    who = name(rng)
    stem = f'{who} places a piece of {metal} into {salt} solution. Predict whether a reaction occurs, explain your prediction and describe what would be observed.'
    if react:
        ans = f'Yes – {metal} is more reactive than {other}, so it displaces {other}: a coating of {METAL_LOOK[other]} forms on the {metal}' + (f' and the {col} colour fades' if col not in ('colourless',) else '') + '; the mixture warms slightly.'
        key = f'1 reaction occurs; 1 {metal} above {other} in the reactivity series; 1 observation: {METAL_LOOK[other]} deposited' + (f', {col} solution fades' if col != 'colourless' else '') + '.'
    else:
        ans = f'No reaction – {metal} is less reactive than {other}, so it cannot displace it.'
        key = f'1 no reaction; 1 {metal} is below {other} in the reactivity series; 1 no visible change.'
    return dict(stem=stem, answer=ans, markingKey=key, marks=3)


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step')
def unknown_series(rng, slot):
    ms = rng.sample(['magnesium', 'zinc', 'iron', 'copper', 'silver'], 3)
    ms.sort(key=SERIES.index)
    labels = rng.sample(['X', 'Y', 'Z'], 3)
    lab = dict(zip(ms, labels))
    obs = []
    for a in ms:
        for b in ms:
            if a != b:
                obs.append(f'{lab[a]} in a solution of a {lab[b]} salt: {"reaction" if SERIES.index(a) < SERIES.index(b) else "no reaction"}')
    rng.shuffle(obs)
    order = ' > '.join(lab[m] for m in ms)
    return dict(stem='Three metals, X, Y and Z, were placed in solutions of each other’s salts. Results:\n' + '\n'.join(obs) + '\n(a) Deduce the order of reactivity of X, Y and Z, most reactive first. (b) Explain your reasoning. (c) Suggest how the reliability of the conclusion could be improved.',
                answer=f'(a) {order} (b) the most reactive metal displaces both others; the least reactive displaces neither (c) repeat with fresh, cleaned metal samples and the same concentration of solutions, or measure temperature rise',
                markingKey=f'(a) 2 for {order} (1 if one pair swapped). (b) 1 a metal displaces only metals below it; 1 counts of reactions used. (c) 1 valid improvement (clean metal surfaces, equal concentrations, repeats, measure temperature change).', marks=5, gap='G5')


dataset('ch06-st3',
        dict(intro='{who} added 1.0 g of powdered metal to 25 cm³ of 0.5 mol/dm³ copper(II) sulfate solution and recorded the maximum temperature rise. Metals were placed in order of their position in the reactivity series (1 = magnesium, 2 = zinc, 3 = iron, 4 = lead).', iv=('Metal', 'position'), xs=[1, 2, 3, 4],
             dv=('Temperature rise', '°C'), f=lambda x: {1: 28, 2: 12, 3: 7, 4: 2}[x], dp=1, trend='The temperature rise is largest for magnesium and decreases for zinc, iron and lead.',
             why='The further apart two metals are in the reactivity series, the more energy is released when one displaces the other, so the reaction is more exothermic.'))

inquiry('ch06-st3',
        dict(ctx='how the position of a metal in the reactivity series affects the temperature rise when it is added to copper(II) sulfate solution',
             iv='the metal used (magnesium, zinc, iron, lead)', dv='maximum temperature rise in °C, measured with a thermometer to 0.5 °C',
             cvs=[('mass and particle size of metal (1.0 g powder)', 'more surface area reacts faster and more metal releases more energy'), ('volume and concentration of copper(II) sulfate', 'more copper ions give more reaction'), ('insulation of the cup', 'reduces heat loss'), ('starting temperature', 'affects heat loss to surroundings')],
             hyp='If the metal is higher in the reactivity series, then the temperature rise will be larger, because a bigger difference in reactivity releases more energy in the displacement reaction.',
             method='Place 25 cm³ of 0.5 mol/dm³ CuSO₄ in a polystyrene cup with a lid; record temperature; add 1.0 g metal powder, stir, record the highest temperature; repeat three times for each metal; calculate mean rises.',
             weak=('a glass beaker without a lid was used', 'use an insulated polystyrene cup with a lid to reduce heat loss'),
             safety='copper(II) sulfate is harmful – eye protection; magnesium powder is flammable'))

R.facts('ch06-st4', F(
    terms=[('relative formula mass (Mᵣ)', 'the sum of the relative atomic masses of all the atoms shown in a formula'),
           ('percentage composition by mass', 'the percentage of the mass of a compound that is due to each element'),
           ('empirical formula', 'the simplest whole-number ratio of atoms of each element in a compound')],
    facts=[('What is the relative formula mass of water, H₂O? (Aᵣ: H = 1, O = 16)', '18', ['17', '10', '34'], '2 × 1 + 16 = 18.'),
           ('What is the Mᵣ of carbon dioxide, CO₂? (Aᵣ: C = 12, O = 16)', '44', ['28', '40', '56'], '12 + 2 × 16 = 44.'),
           ('Which unit does relative formula mass have?', 'None – it is a ratio', ['g', 'g/mol', 'kg'], 'It is relative to 1/12 of carbon-12.')],
    why=[('Explain why percentage composition is useful to farmers choosing a fertiliser.', 'It shows the percentage of nitrogen (or other nutrient) in the fertiliser, so farmers can compare which supplies the most nutrient per kilogram for the money.'),
         ('Explain why relative formula mass has no units.', 'It compares the mass of a formula unit with 1/12 of the mass of a carbon-12 atom, so it is a ratio.')],
    misc=[('The Mᵣ of Ca(OH)₂ is 40 + 16 + 1 × 2 = 58.', 'The 2 applies to both O and H: 40 + 2 × (16 + 1) = 74.'),
          ('The percentage of oxygen in water is 50% because there is one oxygen and two hydrogen atoms.', 'Percentage by mass uses masses: 16/18 × 100 = 88.9%.')],
    cases=[('choosing nitrogen fertilisers in Kenyan smallholder farms', 'Urea, CO(NH₂)₂, contains 46.7% nitrogen, while ammonium nitrate, NH₄NO₃, contains 35%; urea is often cheaper per kg of nitrogen.', 'percentage composition', 'Calculating %N lets farmers compare how much nitrogen each fertiliser delivers per kilogram.')],
    evaluate=[('Fertilisers with the highest percentage of nitrogen are always the best choice.', ['supply more nitrogen per kg, cheaper to transport', 'less needed per field'], ['some forms (urea) lose nitrogen as ammonia gas if not incorporated', 'solubility and release rate matter', 'excess nitrogen causes eutrophication of rivers and lakes'], 'High %N is useful but the best choice also depends on crop, soil, cost and environmental losses.')],
))

COMPOUNDS = [('water', 'H2O'), ('carbon dioxide', 'CO2'), ('sodium chloride', 'NaCl'), ('calcium carbonate', 'CaCO3'), ('sulfuric acid', 'H2SO4'), ('ammonia', 'NH3'),
             ('ammonium nitrate', 'NH4NO3'), ('urea', 'CO(NH2)2'), ('magnesium oxide', 'MgO'), ('copper(II) sulfate', 'CuSO4'), ('glucose', 'C6H12O6'), ('ethanol', 'C2H5OH'),
             ('calcium hydroxide', 'Ca(OH)2'), ('aluminium oxide', 'Al2O3'), ('iron(III) oxide', 'Fe2O3'), ('ammonium sulfate', '(NH4)2SO4'), ('potassium nitrate', 'KNO3'),
             ('magnesium nitrate', 'Mg(NO3)2'), ('sodium hydrogencarbonate', 'NaHCO3'), ('methane', 'CH4'), ('aluminium sulfate', 'Al2(SO4)3')]


@R.add('ch06-st4', 'C3', (1, 5), 'numerical')
def mr_calc(rng, slot):
    nm, f = rng.choice(COMPOUNDS)
    m = mr(f)
    comp = parse_formula(f)
    used = ', '.join(f'{e} = {AR[e]:g}' for e in comp)
    k = rng.choice(['mr', 'pct', 'mass'] if slot.d >= 3 else ['mr', 'pct'])
    if k == 'mr':
        return dict(stem=f'Calculate the relative formula mass (Mᵣ) of {nm}, {f.translate(SUB)}. (Aᵣ: {used})', answer=f'{m:g}',
                    markingKey=f'M1 ' + ' + '.join(f'{n} × {AR[e]:g}' for e, n in comp.items()) + f'; A1 {m:g}.', marks=2)
    e = rng.choice(list(comp))
    p = AR[e] * comp[e] / m * 100
    elname = {'H': 'hydrogen', 'C': 'carbon', 'N': 'nitrogen', 'O': 'oxygen', 'Na': 'sodium', 'Cl': 'chlorine', 'Ca': 'calcium', 'S': 'sulfur', 'Mg': 'magnesium', 'Cu': 'copper', 'Al': 'aluminium', 'Fe': 'iron', 'K': 'potassium'}[e]
    if k == 'pct':
        return dict(stem=f'Calculate the percentage by mass of {elname} in {nm}, {f.translate(SUB)}. (Aᵣ: {used})', answer=f'{p:.1f}%',
                    markingKey=f'M1 Mᵣ = {m:g}; M1 ({comp[e]} × {AR[e]:g}) ÷ {m:g} × 100; A1 {p:.1f}%.', marks=3)
    mass = rng.choice([50, 100, 250, 500, 1000])
    return dict(stem=f'Calculate the mass of {elname} in {mass} g of {nm}, {f.translate(SUB)}. (Aᵣ: {used})', answer=f'{mass * p / 100:.3g} g',
                markingKey=f'M1 Mᵣ = {m:g}; M1 fraction = {comp[e] * AR[e]:g}/{m:g}; A1 {mass * p / 100:.3g} g.', marks=3)


@R.add('ch06-st4', 'C4', (3, 5), 'multi_step')
def fert_compare(rng, slot):
    a, b = rng.sample([('urea', 'CO(NH2)2'), ('ammonium nitrate', 'NH4NO3'), ('ammonium sulfate', '(NH4)2SO4'), ('potassium nitrate', 'KNO3'), ('ammonia', 'NH3')], 2)
    pa = AR['N'] * parse_formula(a[1])['N'] / mr(a[1]) * 100
    pb = AR['N'] * parse_formula(b[1])['N'] / mr(b[1]) * 100
    ca, cb = rng.choice([300, 350, 400, 450, 500]), rng.choice([250, 300, 380, 420, 520])
    costa, costb = ca / (pa / 100 * 1000), cb / (pb / 100 * 1000)
    best = a[0] if costa < costb else b[0]
    return dict(stem=f'A farmer can buy {a[0]} ({a[1].translate(SUB)}) at US${ca} per tonne or {b[0]} ({b[1].translate(SUB)}) at US${cb} per tonne. (Aᵣ: H = 1, N = 14, O = 16, S = 32, K = 39, C = 12) (a) Calculate the percentage of nitrogen in each. (b) Calculate the cost of 1 kg of nitrogen from each fertiliser. (c) Recommend which to buy and give one other factor the farmer should consider.',
                answer=f'(a) {a[0]} {pa:.1f}%, {b[0]} {pb:.1f}% (b) {a[0]} US${costa:.2f}/kg N, {b[0]} US${costb:.2f}/kg N (c) {best}; also consider solubility, losses to air/water, other nutrients (S, K), soil pH',
                markingKey=f'(a) M1 Mᵣ values {mr(a[1]):g}, {mr(b[1]):g}; A1 {pa:.1f}% and {pb:.1f}%. (b) M1 kg N per tonne; A1 {costa:.2f} and {costb:.2f}. (c) 1 {best} (cheaper per kg N); 1 valid other factor.', marks=6, gap='G5')


@R.add('ch06-st1', 'C2', (2, 4), 'explain')
def unbalanced(rng, slot):
    l, r_, w = rng.choice(EQUATIONS)
    left = rng.random() < 0.5
    side = [list(x) for x in (l if left else r_)]
    i = rng.randrange(len(side))
    old = side[i][0]
    side[i][0] = old + 1 if old == 1 or rng.random() < 0.5 else old - 1
    side = [tuple(x) for x in side]
    wl, wr = (side, r_) if left else (l, side)
    if _atoms(wl) == _atoms(wr):
        return None
    diff = [e for e in set(_atoms(wl)) | set(_atoms(wr)) if _atoms(wl).get(e, 0) != _atoms(wr).get(e, 0)]
    return dict(stem=f'{name(rng)} writes the equation {eq_text(wl)} → {eq_text(wr)}. Explain why this equation is not balanced and write the correct balanced equation.',
                answer=f'Atoms of {", ".join(sorted(diff))} are not equal on both sides; correct: {eq_text(l)} → {eq_text(r_)}', type='explain', marks=3,
                markingKey=f'1 counts atoms on each side and identifies the unequal element(s): {", ".join(sorted(diff))}; 1 atoms cannot be created or destroyed; 1 correct equation {eq_text(l)} → {eq_text(r_)}.', gap='G2')


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step')
def reacting_mass(rng, slot):
    cases = [([(1, 'CaCO3')], [(1, 'CaO'), (1, 'CO2')], 'CaCO3', 'CO2', 'heating calcium carbonate in a lime kiln'),
             ([(2, 'Mg'), (1, 'O2')], [(2, 'MgO')], 'Mg', 'MgO', 'burning magnesium ribbon in a crucible'),
             ([(1, 'CuO'), (1, 'H2SO4')], [(1, 'CuSO4'), (1, 'H2O')], 'CuO', 'CuSO4', 'reacting copper(II) oxide with excess sulfuric acid'),
             ([(1, 'Fe2O3'), (3, 'CO')], [(2, 'Fe'), (3, 'CO2')], 'Fe2O3', 'Fe', 'reducing iron(III) oxide in a blast furnace'),
             ([(2, 'Na'), (1, 'Cl2')], [(2, 'NaCl')], 'Na', 'NaCl', 'burning sodium in chlorine')]
    l, r_, a, b, ctx = rng.choice(cases)
    ka = next(k for k, f in l if f == a)
    kb = next(k for k, f in r_ if f == b)
    ma = rng.choice([5.0, 10.0, 12.0, 20.0, 25.0, 50.0, 100.0])
    mb = ma / (ka * mr(a)) * kb * mr(b)
    unit = 'tonnes' if 'furnace' in ctx or 'kiln' in ctx else 'g'
    return dict(stem=f'The equation for {ctx} is {eq_text(l)} → {eq_text(r_)}. (Aᵣ: ' + ', '.join(f'{e} = {AR[e]:g}' for e in sorted(set(_atoms(l)))) + f') (a) Calculate the Mᵣ of {a.translate(SUB)} and of {b.translate(SUB)}. (b) Calculate the maximum mass of {b.translate(SUB)} that can be made from {ma:g} {unit} of {a.translate(SUB)}. (c) Explain how this calculation depends on the law of conservation of mass.',
                answer=f'(a) {mr(a):g} and {mr(b):g} (b) {mb:.3g} {unit} (c) atoms are conserved, so the balanced equation fixes the ratio of masses',
                markingKey=f'(a) 1 each Mᵣ. (b) M1 ratio {ka} × {mr(a):g} : {kb} × {mr(b):g}; M1 {ma:g} × {kb * mr(b):g}/{ka * mr(a):g}; A1 {mb:.3g} {unit}. (c) 1 no atoms lost or gained, so masses are in fixed proportion.', marks=6, gap='G5')


@R.add('ch06-st4', 'C2', (2, 4), 'explain')
def mr_error(rng, slot):
    nm, f = rng.choice([c for c in COMPOUNDS if '(' in c[1]])
    right = mr(f)
    wrong_f = f.replace('(', '').replace(')2', '2').replace(')3', '3')
    wrong = mr(wrong_f)
    if abs(wrong - right) < 0.1:
        return None
    return dict(stem=f'{name(rng)} calculates the Mᵣ of {nm}, {f.translate(SUB)}, as {wrong:g}. Explain the mistake and give the correct value.',
                answer=f'The subscript after the bracket multiplies every atom inside the bracket; correct Mᵣ = {right:g}.', type='explain', marks=2,
                markingKey=f'1 the number outside the bracket applies to all atoms in the bracket (only the last atom was multiplied); 1 correct Mᵣ = {right:g}.', gap='G2')


R.facts('ch06-st1', R.f['ch06-st1'])
R.f['ch06-st1'].why += [('Explain why the total mass stays the same when silver nitrate solution is mixed with sodium chloride solution in a sealed flask, even though a solid forms.', 'The atoms in the reactants are rearranged into the products (silver chloride precipitate and sodium nitrate solution); no atoms enter or leave the closed flask, so the mass is unchanged.'),
                        ('Explain why the formula of aluminium oxide is Al₂O₃.', 'Al forms Al³⁺ and O forms O²⁻; the lowest common multiple of the charges is 6, so 2 Al³⁺ (+6) balance 3 O²⁻ (−6).')]
R.f['ch06-st1'].misc += [('In 2H₂O there are 2 hydrogen atoms and 1 oxygen atom.', 'The coefficient multiplies the whole formula: 2H₂O contains 4 H atoms and 2 O atoms.'),
                         ('Burning a candle destroys matter because the candle gets smaller.', 'The wax reacts with oxygen to form carbon dioxide and water vapour, which escape into the air; mass is conserved.')]
R.f['ch06-st1'].contrast += [('a coefficient', 'a subscript', 'A coefficient (large number in front) shows how many formula units take part; a subscript (small number) shows how many atoms of an element are in one formula unit and cannot be changed when balancing.')]
R.f['ch06-st2'].extended = [('Lead(II) iodide can be made by mixing lead(II) nitrate solution with potassium iodide solution. (a) Write a balanced symbol equation with state symbols. (b) Identify the type of reaction. (c) Describe how a pure, dry sample of the product could be obtained. (d) Suggest one safety precaution.', '(a) Pb(NO₃)₂(aq) + 2KI(aq) → PbI₂(s) + 2KNO₃(aq) (b) precipitation (c) filter, wash the yellow solid with distilled water, dry in a warm oven/on filter paper (d) lead compounds are toxic: wear gloves, avoid ingestion, dispose of waste properly.', 6),
                            ('Classify each reaction and justify: (i) 2H₂O₂(aq) → 2H₂O(l) + O₂(g); (ii) Zn(s) + CuSO₄(aq) → ZnSO₄(aq) + Cu(s); (iii) 4Fe(s) + 3O₂(g) → 2Fe₂O₃(s). Then explain which of the three would show a mass decrease in an open beaker.', '(i) decomposition – one reactant, two products; (ii) displacement – zinc replaces copper; (iii) synthesis/oxidation – two elements form one compound. (i) shows a mass decrease because oxygen gas escapes; (iii) would gain mass from oxygen in air.', 5)]
R.f['ch06-st4'].why += [('Explain why ammonium sulfate contains a smaller percentage of nitrogen than ammonium nitrate even though both contain two nitrogen atoms per formula.', 'Ammonium sulfate (NH₄)₂SO₄ has Mᵣ 132, so 28/132 = 21.2% N; ammonium nitrate NH₄NO₃ has Mᵣ 80, so 28/80 = 35% N – the heavier sulfate group dilutes the nitrogen.'),
                        ('Explain how the percentage composition of a compound can be used to identify which of two possible compounds a sample is.', 'Each compound has a fixed composition; analysing the sample’s mass of each element and comparing with the calculated percentages shows which formula matches.')]
R.f['ch06-st4'].misc += [('The percentage of carbon in methane (CH₄) is 20% because carbon is 1 of 5 atoms.', 'Percentage by mass uses relative atomic masses: 12/16 × 100 = 75%.')]
R.f['ch06-st4'].contrast = [('relative atomic mass', 'relative formula mass', 'Relative atomic mass (Aᵣ) is for one element (weighted mean of its isotopes); relative formula mass (Mᵣ) is the sum of the Aᵣ values of all the atoms in a formula.')]


# =============================================================================================
# ch07 Rates of Reaction
# =============================================================================================
R.facts('ch07-st1', F(
    terms=[('rate of reaction', 'how quickly reactants are used up or products are formed, measured as the change in amount per unit time'),
           ('mean rate of reaction', 'the total change in quantity of product (or reactant) divided by the total time taken'),
           ('gas syringe', 'a graduated glass syringe used to collect and measure the volume of gas produced in a reaction'),
           ('end point (of a reaction)', 'the time at which the reaction stops because one reactant has been used up')],
    facts=[('Which unit is suitable for a rate of reaction measured by gas collection?', 'cm³/s', ['g/cm³', 'cm³', 's/cm³'], 'Volume of gas per unit time.'),
           ('Why does the mass of a flask decrease when marble chips react with hydrochloric acid?', 'Carbon dioxide gas escapes', ['Water evaporates only', 'Mass is destroyed', 'The acid becomes lighter'], 'CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂.'),
           ('Why is a cotton-wool plug placed in the neck of the flask in a mass-loss experiment?', 'To let gas escape but stop acid spray leaving the flask', ['To stop gas escaping', 'To keep the flask warm', 'To speed up the reaction'], 'Spray loss would give extra mass loss.'),
           ('Which method could measure the rate of the reaction between sodium thiosulfate and hydrochloric acid?', 'Timing how long it takes for a cross under the flask to disappear', ['Measuring mass loss', 'Collecting gas in a syringe only', 'Measuring the pH once'], 'A yellow sulfur precipitate makes the solution cloudy.')],
    why=[('Explain why the rate of a reaction decreases as the reaction proceeds.', 'Reactant particles are used up, so their concentration falls; there are fewer collisions per second, so fewer successful collisions and a slower rate.'),
         ('Explain why a gas syringe gives more accurate gas volumes than collecting gas over water in a measuring cylinder for carbon dioxide.', 'Carbon dioxide is fairly soluble in water, so some dissolves and is not measured; a gas syringe collects all the gas directly with finer graduations.'),
         ('Explain why the mass-loss method is not suitable for the reaction of magnesium with hydrochloric acid.', 'The gas produced is hydrogen, which has a very low mass, so the loss in mass is too small to measure accurately on a school balance.')],
    contrast=[('mean rate', 'rate at a particular time', 'Mean rate is total change ÷ total time; the rate at a particular time is the gradient of the tangent to the curve at that time.'),
              ('the mass-loss method', 'the gas-collection method', 'Mass loss measures the decrease in mass as gas escapes (needs a dense gas such as CO₂); gas collection measures the volume of gas in a syringe or over water.')],
    misc=[('When the line on a gas-volume graph becomes flat, the reaction has become very fast.', 'A flat line means no more gas is produced: the reaction has stopped because a reactant is used up.'),
          ('A reaction that produces more gas in total must be faster.', 'Total gas depends on the amount of limiting reactant; rate depends on how quickly it is produced.')],
    evaluate=[('Data loggers are always better than manual readings for measuring rates of reaction.', ['take many readings at precise times, avoiding human reaction-time errors', 'plot graphs automatically'], ['expensive and can fail; sensors need calibration', 'students may not understand the process', 'manual methods are adequate for slow reactions'], 'Data loggers improve precision for fast reactions, but manual methods are valid for slow reactions when carried out carefully.')],
))


def _gas_curve(total, k, ts):
    return [total * (1 - math.exp(-k * t)) for t in ts]


@R.add('ch07-st1', 'C3', (1, 5), 'numerical')
def gas_rate(rng, slot):
    who = name(rng)
    rx = rng.choice([('marble chips and hydrochloric acid', 'carbon dioxide'), ('magnesium ribbon and hydrochloric acid', 'hydrogen'), ('hydrogen peroxide with manganese(IV) oxide catalyst', 'oxygen'), ('zinc granules and sulfuric acid', 'hydrogen')])
    total = rng.choice([60, 72, 80, 90, 96, 100])
    k = rng.uniform(0.012, 0.03)
    ts = [0, 30, 60, 90, 120, 150, 180]
    vs = [round(v) for v in _gas_curve(total, k, ts)]
    tab = 'Time / s: ' + ', '.join(map(str, ts)) + '\nVolume of gas / cm³: ' + ', '.join(map(str, vs))
    kind = rng.choice(['first', 'between', 'overall'] if slot.d >= 3 else ['first', 'overall'])
    if kind == 'first':
        t = rng.choice([30, 60, 90])
        v = vs[ts.index(t)]
        return dict(stem=f'{who} reacted {rx[0]} and collected the {rx[1]} in a gas syringe.\n{tab}\nCalculate the mean rate of reaction in the first {t} s.', answer=f'{v / t:.2f} cm³/s',
                    markingKey=f'M1 {v} cm³ ÷ {t} s; A1 {v / t:.2f} cm³/s (unit required).', marks=2)
    if kind == 'between':
        i = rng.randrange(1, 5)
        a, b = ts[i], ts[i + 2]
        r1 = (vs[i + 2] - vs[i]) / (b - a)
        r0 = vs[2] / 60
        return dict(stem=f'The {rx[1]} produced by {rx[0]} was collected:\n{tab}\n(a) Calculate the mean rate between {a} s and {b} s. (b) Compare it with the mean rate in the first 60 s and explain the difference.',
                    answer=f'(a) {r1:.2f} cm³/s (b) slower than {r0:.2f} cm³/s in the first 60 s because reactant concentration has fallen',
                    markingKey=f'(a) M1 ({vs[i + 2]} − {vs[i]}) ÷ ({b} − {a}); A1 {r1:.2f} cm³/s. (b) 1 first 60 s rate {r0:.2f} cm³/s is higher; 1 fewer reactant particles so fewer collisions per second.', marks=4)
    return dict(stem=f'In an experiment with {rx[0]}, {who} recorded:\n{tab}\nCalculate the mean rate of reaction over the whole 180 s and state the units.', answer=f'{vs[-1] / 180:.3f} cm³/s',
                markingKey=f'M1 {vs[-1]} ÷ 180; A1 {vs[-1] / 180:.3f} cm³/s.', marks=2)


@R.add('ch07-st1', 'C3', (2, 5), 'numerical')
def mass_loss(rng, slot):
    start = round(rng.uniform(150, 180), 2)
    loss = rng.choice([1.20, 1.50, 1.80, 2.10, 2.40])
    k = rng.uniform(0.01, 0.025)
    ts = [0, 60, 120, 180, 240, 300]
    ms = [round(start - loss * (1 - math.exp(-k * t)), 2) for t in ts]
    t = rng.choice([60, 120])
    dm = ms[0] - ms[ts.index(t)]
    tab = 'Time / s: ' + ', '.join(map(str, ts)) + '\nMass of flask and contents / g: ' + ', '.join(f'{m:.2f}' for m in ms)
    return dict(stem=f'Marble chips were added to hydrochloric acid in a conical flask on a balance.\n{tab}\n(a) Calculate the mass of carbon dioxide lost in the first {t} s. (b) Calculate the mean rate of reaction in g/s over this time. (c) Suggest why the readings change less towards the end.',
                answer=f'(a) {dm:.2f} g (b) {dm / t:.4f} g/s (c) acid or marble is being used up, so the rate decreases',
                markingKey=f'(a) A1 {ms[0]:.2f} − {ms[ts.index(t)]:.2f} = {dm:.2f} g. (b) M1 ÷ {t}; A1 {dm / t:.4f} g/s. (c) 1 lower concentration of reactants, fewer collisions.', marks=4)


inquiry('ch07-st1',
        dict(ctx='how the size of marble chips affects the rate at which carbon dioxide is produced with hydrochloric acid',
             iv='size of marble chips (small, medium, large – or powder)', dv='volume of CO₂ collected in a gas syringe every 30 s for 5 min; rate from the initial gradient',
             cvs=[('mass of marble (e.g. 5.0 g)', 'more marble gives more surface'), ('volume and concentration of acid', 'more acid particles increase collision frequency'), ('temperature', 'faster particles collide more often'), ('the same gas syringe and connections', 'leaks would reduce the volume')],
             hyp='If the chips are smaller, then the rate will be higher, because smaller chips have a larger total surface area so more acid particles collide with the marble per second.',
             method='Add 5.0 g of chips to 50 cm³ of 1.0 mol/dm³ HCl in a conical flask; immediately insert a bung connected to a 100 cm³ gas syringe and start the stopwatch; record volume every 30 s for 5 min; repeat three times for each chip size; plot volume–time graphs and compare initial gradients.',
             weak=('the bung was inserted several seconds after the marble was added', 'put the acid in the flask and the chips in a small tube inside, then tip the tube once the bung is sealed so no gas escapes before collection'),
             safety='hydrochloric acid is an irritant – wear eye protection; check the syringe does not jam'))

R.facts('ch07-st2', F(
    terms=[('collision theory', 'the theory that particles react only when they collide with enough energy (at least the activation energy) and the correct orientation'),
           ('activation energy', 'the minimum energy that colliding particles must have for a reaction to occur'),
           ('successful collision', 'a collision between reactant particles with energy equal to or greater than the activation energy, leading to reaction'),
           ('reaction profile (energy level diagram)', 'a graph showing the energy of reactants and products during a reaction, including the activation energy'),
           ('exothermic reaction', 'a reaction that releases energy to the surroundings, so the products have less energy than the reactants'),
           ('endothermic reaction', 'a reaction that takes in energy from the surroundings, so the products have more energy than the reactants')],
    facts=[('According to collision theory, what must happen for particles to react?', 'They must collide with at least the activation energy', ['They must be in the same container', 'They must be at room temperature', 'They must be in solution'], 'Not every collision is successful.'),
           ('On a reaction profile, what is the activation energy?', 'The energy difference from reactants up to the peak of the curve', ['The difference between reactants and products', 'The energy of the products', 'The height of the products above zero'], 'It is the energy barrier.'),
           ('Which is an endothermic process?', 'Thermal decomposition of calcium carbonate', ['Burning methane', 'Neutralisation of an acid', 'Respiration'], 'It needs continuous heating.')],
    why=[('Explain why most collisions between particles do not lead to a reaction.', 'Only a small fraction of colliding particles have energy equal to or greater than the activation energy (and the right orientation); the rest bounce apart unchanged.'),
         ('Explain why a reaction with a high activation energy is usually slow at room temperature.', 'Very few particles have enough energy to overcome the high energy barrier, so there are few successful collisions per second.'),
         ('Explain why a match must be struck before it burns even though combustion is exothermic.', 'The friction provides the activation energy to start the reaction; then the energy released by burning provides activation energy for further reaction.')],
    contrast=[('an exothermic reaction', 'an endothermic reaction', 'An exothermic reaction releases energy (temperature of surroundings rises, products lower in energy); an endothermic reaction absorbs energy (temperature falls, products higher in energy).'),
              ('activation energy', 'overall energy change', 'Activation energy is the barrier from reactants to the peak; overall energy change is the difference in energy between reactants and products.')],
    misc=[('Exothermic reactions do not need activation energy because they give out energy.', 'All reactions need activation energy to break bonds and start; exothermic reactions release more energy than they take in overall.'),
          ('Particles react every time they collide.', 'Only collisions with at least the activation energy (and correct orientation) are successful.')],
    cases=[('self-heating cans and hand warmers', 'Hand warmers contain iron powder that oxidises when exposed to air, warming for hours; self-heating cans use the reaction of calcium oxide with water.', 'exothermic reactions', 'The reactions release energy to the surroundings, so the temperature rises.'),
           ('instant cold packs in sports first aid', 'Squeezing the pack breaks an inner bag so ammonium nitrate dissolves in water and the pack becomes very cold.', 'endothermic processes', 'Dissolving ammonium nitrate absorbs energy from the surroundings, lowering the temperature.')],
    evaluate=[('Collision theory fully explains why reactions happen at different rates.', ['explains effects of temperature, concentration, surface area and catalysts', 'supported by many experiments'], ['does not predict exact rates or activation energies', 'ignores orientation and complex mechanisms in multi-step reactions'], 'It is a powerful qualitative model but limited for precise predictions.')],
))


@R.add('ch07-st2', 'C3', (1, 5), 'numerical')
def profile(rng, slot):
    er = rng.choice([50, 80, 100, 120, 150, 200])
    ep = er + rng.choice([-90, -70, -60, -40, 30, 40, 60])
    peak = max(er, ep) + rng.choice([40, 60, 80, 100, 120])
    ea = peak - er
    dh = ep - er
    kind = 'exothermic' if dh < 0 else 'endothermic'
    k = rng.choice(['both', 'reverse', 'cat'] if slot.d >= 3 else ['both'])
    base = f'On a reaction profile the reactants have an energy of {er} kJ, the peak of the curve is at {peak} kJ and the products have an energy of {ep} kJ.'
    if k == 'both':
        return dict(stem=f'{base} Calculate the activation energy and the overall energy change, and state whether the reaction is exothermic or endothermic.', answer=f'Eₐ = {ea} kJ; ΔE = {dh:+d} kJ; {kind}',
                    markingKey=f'1 Eₐ = {peak} − {er} = {ea} kJ; 1 ΔE = {ep} − {er} = {dh:+d} kJ; 1 {kind} because products are {"lower" if dh < 0 else "higher"} in energy than reactants.', marks=3)
    if k == 'reverse':
        return dict(stem=f'{base} Calculate the activation energy for the reverse reaction (products → reactants) and explain why it differs from the forward activation energy.', answer=f'{peak - ep} kJ',
                    markingKey=f'M1 reverse Eₐ = peak − products = {peak} − {ep}; A1 {peak - ep} kJ; 1 forward and reverse differ by the overall energy change ({abs(dh)} kJ).', marks=3)
    new = peak - rng.choice([20, 30, 40])
    return dict(stem=f'{base} A catalyst lowers the peak to {new} kJ. Calculate the activation energy with and without the catalyst, and state the effect of the catalyst on the overall energy change.', answer=f'without {ea} kJ; with {new - er} kJ; overall energy change unchanged ({dh:+d} kJ)',
                markingKey=f'1 {ea} kJ; 1 {new - er} kJ; 1 overall energy change is unchanged because the reactants and products are the same ({dh:+d} kJ).', marks=3)


@R.add('ch07-st2', 'C3', (2, 5), 'numerical')
def temp_change_energy(rng, slot):
    v = rng.choice([25, 50, 100])
    dT = round(rng.uniform(3.0, 18.0), 1) * rng.choice([1, 1, -1])
    q = v * 4.18 * abs(dT)
    rx = rng.choice(['neutralising sodium hydroxide with hydrochloric acid', 'dissolving ammonium nitrate in water', 'adding zinc powder to copper(II) sulfate solution', 'dissolving calcium chloride in water', 'reacting citric acid with sodium hydrogencarbonate'])
    if 'ammonium nitrate' in rx or 'citric' in rx:
        dT = -abs(dT)
    elif 'neutral' in rx or 'zinc' in rx or 'calcium chloride' in rx:
        dT = abs(dT)
    kind = 'exothermic' if dT > 0 else 'endothermic'
    return dict(stem=f'When {rx}, the temperature of {v} cm³ of solution changed by {dT:+.1f} °C. Use Q = m × c × ΔT (c = 4.18 J/g °C; 1 cm³ of solution has a mass of 1 g) to calculate the energy transferred, and state whether the reaction is exothermic or endothermic.',
                answer=f'{q:.0f} J ({q / 1000:.2f} kJ); {kind}', markingKey=f'M1 {v} × 4.18 × {abs(dT)}; A1 {q:.0f} J; 1 {kind} because the temperature {"rose" if dT > 0 else "fell"}.', marks=3)


inquiry('ch07-st2',
        dict(ctx='how the mass of ammonium nitrate dissolved in water affects the temperature change (for designing a cold pack)',
             iv='mass of ammonium nitrate (1, 2, 3, 4, 5 g)', dv='temperature change in °C of 50 cm³ of water, measured with a digital thermometer',
             cvs=[('volume of water', 'a different volume changes the temperature change for the same energy'), ('starting temperature of water', 'affects heat gain from surroundings'), ('insulation of the cup', 'heat transfer from surroundings'), ('stirring', 'speeds dissolving and mixing')],
             hyp='If more ammonium nitrate is dissolved, then the temperature will fall more, because dissolving is endothermic and more solute absorbs more energy from the water.',
             method='Measure 50 cm³ of water at 20 °C into a polystyrene cup with lid; add 1.0 g ammonium nitrate, stir and record the lowest temperature; repeat for 2, 3, 4, 5 g with fresh water; repeat three times; calculate mean temperature change and energy absorbed using Q = mcΔT.',
             weak=('the thermometer was read after a fixed 10 s rather than at the lowest temperature', 'stir continuously and record the lowest temperature reached'),
             safety='ammonium nitrate is an oxidiser – keep away from heat and flammable material; eye protection'))

R.facts('ch07-st3', F(
    terms=[('catalyst', 'a substance that increases the rate of a reaction without being used up, by providing a pathway with a lower activation energy'),
           ('enzyme', 'a biological catalyst made of protein'),
           ('concentration', 'the amount of solute in a given volume of solution, e.g. in g/dm³ or mol/dm³'),
           ('surface area to volume ratio', 'the amount of surface of a solid compared with its volume; it increases when a solid is broken into smaller pieces')],
    facts=[('What effect does increasing temperature have on the rate of most reactions?', 'It increases the rate', ['It decreases the rate', 'No effect', 'It stops the reaction'], 'Particles move faster and more have energy ≥ Eₐ.'),
           ('Which change would NOT increase the rate of reaction between magnesium and acid?', 'Using a larger piece of magnesium ribbon of the same mass in one lump', ['Using magnesium powder', 'Warming the acid', 'Using more concentrated acid'], 'One lump has a smaller surface area.'),
           ('Which catalyst is used in catalytic converters in cars?', 'Platinum (and rhodium/palladium)', ['Iron', 'Manganese(IV) oxide', 'Nickel'], 'They convert CO and NOₓ to less harmful gases.'),
           ('Which catalyst is used in the Haber process to make ammonia?', 'Iron', ['Platinum', 'Vanadium(V) oxide', 'Copper'], 'Iron catalyst at about 450 °C.')],
    why=[('Explain, using collision theory, why increasing temperature increases the rate of reaction.', 'Particles gain kinetic energy and move faster, so they collide more often; more importantly, a greater proportion of collisions have energy ≥ activation energy, so the frequency of successful collisions increases.'),
         ('Explain why increasing concentration increases the rate of reaction.', 'There are more reactant particles in the same volume, so collisions are more frequent and there are more successful collisions per second.'),
         ('Explain why powdered calcium carbonate reacts faster with acid than marble chips of the same mass.', 'Powder has a much larger surface area, so more particles are exposed to acid and the frequency of collisions increases.'),
         ('Explain how a catalyst increases the rate of reaction.', 'It provides an alternative reaction pathway with a lower activation energy, so a greater proportion of collisions are successful; the catalyst is not used up.')],
    contrast=[('increasing temperature', 'adding a catalyst', 'Increasing temperature gives particles more energy so more exceed the activation energy; a catalyst lowers the activation energy so more collisions succeed at the same temperature.'),
              ('a catalyst', 'a reactant', 'A reactant is used up and changed into products; a catalyst speeds up the reaction but is chemically unchanged at the end.')],
    misc=[('Increasing concentration makes particles move faster.', 'Concentration puts more particles in the same volume; their speed depends on temperature.'),
          ('A catalyst gives the reacting particles more energy.', 'A catalyst lowers the activation energy; it does not give particles energy.'),
          ('Doubling the size of marble chips doubles the rate because there is more marble.', 'Larger chips (same mass) have a smaller surface area, so the rate decreases.')],
    cases=[('catalytic converters, required on new cars in the USA from 1975 and in the EU from 1993', 'Platinum, palladium and rhodium on a ceramic honeycomb convert CO, NOₓ and unburnt hydrocarbons into CO₂, N₂ and H₂O.', 'catalysts and surface area', 'The metals lower activation energy; the honeycomb gives a huge surface area for gas molecules to react on.'),
           ('flour-mill and grain-silo dust explosions', 'Fine flour dust suspended in air has exploded in mills when ignited by a spark.', 'the effect of surface area on rate', 'Tiny particles have an enormous surface area exposed to oxygen, so combustion is extremely fast – an explosion.'),
           ('refrigeration of food', 'Keeping food at 4 °C slows the reactions and microbial growth that cause spoilage.', 'the effect of temperature on rate', 'At lower temperature particles have less energy, so fewer collisions exceed the activation energy, and enzymes in microbes work slowly.')],
    evaluate=[('Catalytic converters have solved the problem of air pollution from cars.', ['greatly reduce CO, NOₓ and hydrocarbon emissions', 'urban air quality has improved in many cities'], ['do not reduce CO₂ emissions, which cause climate change', 'do not work until hot (short journeys)', 'mining platinum-group metals has environmental impacts; theft of converters'], 'They have reduced toxic pollutants greatly, but not CO₂ or particulates, so the problem is not solved.')],
))


@R.add('ch07-st3', 'C3', (1, 5), 'numerical')
def concentration(rng, slot):
    who = name(rng)
    k = rng.choice(['gdm3', 'mass', 'dilute', 'thio'] if slot.d >= 3 else ['gdm3', 'mass'])
    if k == 'gdm3':
        m = rng.choice([2.0, 4.0, 5.0, 7.3, 8.0, 10.0, 12.5])
        v = rng.choice([100, 200, 250, 500])
        c = m / (v / 1000)
        sol = rng.choice(['sodium thiosulfate', 'hydrochloric acid (as HCl)', 'copper(II) sulfate', 'sodium hydroxide'])
        return dict(stem=f'{who} dissolves {m} g of {sol} to make {v} cm³ of solution. Calculate the concentration in g/dm³.', answer=f'{c:g} g/dm³',
                    markingKey=f'M1 volume = {v} ÷ 1000 = {v / 1000} dm³; M1 c = mass ÷ volume; A1 {c:g} g/dm³.', marks=3)
    if k == 'mass':
        c = rng.choice([10, 20, 40, 50, 80])
        v = rng.choice([50, 150, 250, 400])
        return dict(stem=f'What mass of solute is needed to make {v} cm³ of a {c} g/dm³ solution of sodium thiosulfate for a rate experiment?', answer=f'{c * v / 1000:g} g',
                    markingKey=f'M1 m = c × V = {c} × {v / 1000}; A1 {c * v / 1000:g} g.', marks=2)
    if k == 'dilute':
        c0 = rng.choice([40, 50, 60, 80])
        vs = [10, 20, 30, 40, 50]
        tot = 50
        rows = '; '.join(f'{v} cm³ stock + {tot - v} cm³ water → {c0 * v / tot:g} g/dm³' for v in vs)
        v = rng.choice(vs[:-1])
        return dict(stem=f'A stock solution of sodium thiosulfate has a concentration of {c0} g/dm³. {who} makes 50 cm³ of a diluted solution using {v} cm³ of stock solution and {tot - v} cm³ of water. Calculate the new concentration and explain why the total volume is kept at 50 cm³.',
                    answer=f'{c0 * v / tot:g} g/dm³; total volume is a control variable', markingKey=f'M1 {c0} × {v}/{tot}; A1 {c0 * v / tot:g} g/dm³; 1 keeping total volume constant means only concentration changes (fair test). Full dilution table: {rows}.', marks=3)
    cs = [10, 20, 30, 40, 50]
    ts = [round(1500 / c * rng.uniform(0.95, 1.05)) for c in cs]
    i = rng.randrange(5)
    return dict(stem=f'In the “disappearing cross” experiment, times for the cross to disappear were: ' + ', '.join(f'{c} g/dm³: {t} s' for c, t in zip(cs, ts)) + f'. Rate can be estimated as 1/time. Calculate the rate (in s⁻¹) at {cs[i]} g/dm³ and describe the relationship between concentration and rate.',
                answer=f'{1 / ts[i]:.4f} s⁻¹; rate increases as concentration increases (approximately proportional)', markingKey=f'M1 1 ÷ {ts[i]}; A1 {1 / ts[i]:.4f} s⁻¹; 1 higher concentration → shorter time → higher rate (≈ directly proportional).', marks=3)


dataset('ch07-st3',
        dict(intro='{who} timed how long it took for a cross to disappear when 50 cm³ of sodium thiosulfate solution reacted with 5 cm³ of hydrochloric acid at different temperatures.', iv=('Temperature', '°C'), xs=[20, 30, 40, 50, 60],
             dv=('Time for cross to disappear', 's'), f=lambda x: 120 / 2 ** ((x - 20) / 10), dp=0, trend='The time decreases as temperature increases – roughly halving for each 10 °C rise – so the rate increases.',
             why='At higher temperature particles move faster and collide more often, and a greater proportion have energy above the activation energy, so successful collisions are more frequent.'),
        dict(intro='{who} measured the volume of oxygen produced in 60 s when different masses of manganese(IV) oxide catalyst were added to 25 cm³ of hydrogen peroxide.', iv=('Mass of catalyst', 'g'), xs=[0.1, 0.2, 0.3, 0.4, 0.5],
             dv=('Volume of oxygen in 60 s', 'cm³'), f=lambda x: 90 * x / (x + 0.2), dp=0, trend='The volume of oxygen in 60 s increases with mass of catalyst but levels off at higher masses.',
             why='More catalyst gives more surface for the reaction, providing more sites with a lower activation energy; at high masses the hydrogen peroxide concentration becomes the limiting factor.'))

inquiry('ch07-st3',
        dict(ctx='how the concentration of hydrochloric acid affects the rate of reaction with magnesium ribbon',
             iv='concentration of hydrochloric acid (0.2, 0.4, 0.6, 0.8, 1.0 mol/dm³)', dv='time for a 2 cm strip of magnesium to disappear completely, measured with a stopwatch (rate = 1/time)',
             cvs=[('length/mass of magnesium ribbon', 'more magnesium takes longer to react'), ('volume of acid (25 cm³)', 'affects how much acid is in contact'), ('temperature of acid', 'affects particle energy'), ('cleaning the ribbon with sandpaper', 'an oxide layer slows the start of the reaction')],
             hyp='If the acid concentration increases, then the magnesium will disappear faster, because there are more acid particles per cm³ and so more frequent successful collisions with the magnesium surface.',
             method='Clean 2 cm strips of Mg with sandpaper; place 25 cm³ of acid at 20 °C in a boiling tube; add the Mg and start the stopwatch; stop when no Mg remains; repeat three times at each of five concentrations; calculate mean times and 1/time; plot rate against concentration.',
             weak=('some strips were shiny and others were dull and grey', 'clean every strip with sandpaper so the oxide layer does not delay the reaction'),
             safety='hydrogen is flammable – no flames; eye protection for acid'))

R.facts('ch07-st4', F(
    terms=[('gradient of a rate graph', 'the change in the vertical quantity (e.g. volume of gas) divided by the change in time; it equals the rate at that point'),
           ('tangent', 'a straight line that touches a curve at one point, used to find the rate at a particular time'),
           ('initial rate', 'the rate at the very start of a reaction, found from the gradient of the tangent at time zero')],
    facts=[('On a graph of volume of gas against time, what does a steeper line show?', 'A faster rate of reaction', ['A slower rate', 'More product overall', 'A lower temperature'], 'Gradient = rate.'),
           ('Two experiments use the same amounts of reactants but one is warmer. How do the curves compare?', 'The warmer curve is steeper but levels off at the same final volume', ['The warmer curve levels off higher', 'The curves are identical', 'The warmer curve is less steep'], 'Same amount of reactant → same total product.'),
           ('If the amount of limiting reactant is halved, what happens to the final volume of gas?', 'It halves', ['It doubles', 'It stays the same', 'It becomes zero'], 'Total product depends on the limiting reactant.')],
    why=[('Explain why the curve on a graph of product against time levels off.', 'One reactant (the limiting reactant) has been completely used up, so no more product forms and the rate is zero.'),
         ('Explain why drawing a tangent is needed to find the rate at a particular time on a curved graph.', 'The rate changes continuously on a curve; the gradient of the tangent at that point gives the instantaneous rate, while a chord only gives a mean rate.'),
         ('Explain why a reaction is fastest at the start.', 'The concentration of reactants is highest at the start, so collisions are most frequent.')],
    misc=[('Adding a catalyst makes more product, so the curve levels off higher.', 'A catalyst increases the rate (steeper curve) but does not change the amount of product; the final value is the same.'),
          ('Mean rate over the whole reaction equals the rate at the start.', 'The rate is highest at the start and falls; the mean over the whole time is lower than the initial rate.')],
    evaluate=[('Calculating mean rate is good enough to compare reactions.', ['simple to calculate from two readings', 'fair if the same time interval is used for each reaction'], ['hides how the rate changes', 'depends on the time interval chosen', 'initial rate from a tangent is a better comparison'], 'Mean rates over the same short initial interval are acceptable, but initial rates from tangents are more valid.')],
))


@R.add('ch07-st4', 'C3', (1, 5), 'numerical')
def tangent(rng, slot):
    total = rng.choice([50, 60, 80, 100, 120])
    k = rng.uniform(0.015, 0.04)
    t = rng.choice([20, 40, 60, 80])
    vt = total * (1 - math.exp(-k * t))
    grad = total * k * math.exp(-k * t)
    t1, t2 = t - 20, t + 20
    v1 = round(vt - grad * 20, 1)
    v2 = round(vt + grad * 20, 1)
    g = (v2 - v1) / (t2 - t1)
    kind = rng.choice(['tan', 'graph'])
    if kind == 'tan':
        return dict(stem=f'A tangent is drawn to a gas-volume curve at t = {t} s. The tangent passes through the points ({t1} s, {v1} cm³) and ({t2} s, {v2} cm³). Calculate the rate of reaction at {t} s.', answer=f'{g:.2f} cm³/s',
                    markingKey=f'M1 gradient = ({v2} − {v1}) ÷ ({t2} − {t1}); A1 {g:.2f} cm³/s.', marks=2)
    a, b = rng.sample([10, 20, 30, 40, 50, 60, 90, 120], 2)
    a, b = min(a, b), max(a, b)
    va, vb = total * (1 - math.exp(-k * a)), total * (1 - math.exp(-k * b))
    return dict(stem=f'From a graph of oxygen volume against time for the decomposition of hydrogen peroxide, {name(rng)} reads {va:.1f} cm³ at {a} s and {vb:.1f} cm³ at {b} s. Calculate the mean rate between these times. Explain whether the rate at {a} s is greater or less than this mean rate.',
                answer=f'{(vb - va) / (b - a):.2f} cm³/s; the rate at {a} s is greater, because the rate decreases with time as the peroxide is used up',
                markingKey=f'M1 ({vb:.1f} − {va:.1f}) ÷ ({b} − {a}); A1 {(vb - va) / (b - a):.2f} cm³/s; 1 rate at {a} s higher (steeper curve earlier; concentration falls).', marks=3)


@R.add('ch07-st4', 'C4', (3, 5), 'multi_step')
def compare_curves(rng, slot):
    total = rng.choice([60, 80, 100])
    k1 = rng.uniform(0.015, 0.025)
    f = rng.choice([1.5, 2.0, 2.5])
    change = rng.choice([('the acid was warmed by 10 °C', 'same'), ('a catalyst was added', 'same'), ('half the mass of marble was used (marble is limiting)', 'half'), ('powdered marble was used instead of chips', 'same')])
    ts = [0, 30, 60, 90, 120, 180]
    a = [round(total * (1 - math.exp(-k1 * t))) for t in ts]
    tot2 = total / 2 if change[1] == 'half' else total
    k2 = k1 * (1 if change[1] == 'half' else f)
    b = [round(tot2 * (1 - math.exp(-k2 * t))) for t in ts]
    r1, r2 = a[1] / 30, b[1] / 30
    return dict(stem=f'Experiment A: marble chips with hydrochloric acid. Experiment B: the same, except {change[0]}.\nTime / s: {", ".join(map(str, ts))}\nA: volume of CO₂ / cm³: {", ".join(map(str, a))}\nB: volume of CO₂ / cm³: {", ".join(map(str, b))}\n(a) Calculate the mean rate in the first 30 s for each experiment. (b) Compare the final volumes and explain the difference or similarity. (c) Use collision theory to explain the difference in rate.',
                answer=f'(a) A {r1:.2f} cm³/s, B {r2:.2f} cm³/s (b) ' + ('B gives half the final volume because less limiting reactant' if change[1] == 'half' else 'same final volume, same amounts of reactants') + ' (c) ' + {'the acid was warmed by 10 °C': 'more particles have energy ≥ Eₐ and collide more often', 'a catalyst was added': 'lower activation energy pathway', 'half the mass of marble was used (marble is limiting)': 'less surface area of marble, fewer collisions per second', 'powdered marble was used instead of chips': 'larger surface area, more frequent collisions'}[change[0]],
                markingKey=f'(a) M1 volume at 30 s ÷ 30; A1 A {r1:.2f}, B {r2:.2f} cm³/s. (b) 1 comparison of final volumes ({a[-1]} vs {b[-1]} cm³) with reason (amount of limiting reactant). (c) 1-2 collision-theory explanation linked to the change.', marks=6, gap='G5')


dataset('ch07-st4',
        dict(intro='{who} measured the initial rate of reaction (from the tangent at t = 0) between marble chips and hydrochloric acid of different concentrations.', iv=('Acid concentration', 'mol/dm³'), xs=[0.25, 0.50, 0.75, 1.00, 1.25],
             dv=('Initial rate', 'cm³/s'), f=lambda x: 1.6 * x, dp=2, trend='Initial rate increases in proportion to acid concentration – doubling the concentration roughly doubles the rate.',
             why='Doubling concentration doubles the number of acid particles per unit volume, doubling the frequency of collisions with the marble surface.'))

inquiry('ch07-st4',
        dict(ctx='how the temperature of hydrogen peroxide solution affects the initial rate of its decomposition with a manganese(IV) oxide catalyst',
             iv='temperature of hydrogen peroxide (20, 30, 40, 50, 60 °C)', dv='initial rate – gradient of the tangent at t = 0 on a graph of O₂ volume (gas syringe) against time',
             cvs=[('mass of catalyst (0.5 g)', 'more catalyst surface speeds the reaction'), ('volume and concentration of peroxide', 'affect collision frequency and total gas'), ('time intervals for readings (every 10 s)', 'needed to draw an accurate curve'), ('same batch of catalyst powder', 'particle size affects surface area')],
             hyp='If the temperature increases, then the initial rate will increase, because more molecules have energy ≥ activation energy and collide more often.',
             method='Warm 25 cm³ of 10-volume H₂O₂ in a water bath to each temperature; add 0.5 g MnO₂, seal with bung and gas syringe; record volume every 10 s for 2 min; plot graphs; draw tangents at t = 0 and calculate gradients; repeat three times.',
             weak=('the peroxide cooled while the apparatus was assembled', 'keep the flask in the water bath throughout and check the temperature at the start and end'),
             safety='hydrogen peroxide is an irritant/oxidiser – eye protection; MnO₂ is harmful if inhaled'))

R.f['ch07-st2'].extended = [('Sketch and label a reaction profile for the combustion of methane (exothermic), showing the activation energy and the overall energy change. On the same axes show the effect of a catalyst. Explain, using collision theory, why the methane in a gas cooker does not burn until it is lit.', 'Profile: reactants higher than products; hump labelled Eₐ from reactants to peak; ΔE arrow from reactants down to products; catalysed curve with lower peak, same start and end. Methane molecules at room temperature rarely collide with energy ≥ Eₐ; the spark/flame provides the activation energy; then the energy released keeps the reaction going.', 6, 'long'),
                            ('Hydrogen and oxygen can be mixed safely at room temperature, but the mixture explodes with a spark. Use ideas about activation energy and the energy released to explain this, and evaluate the safety of hydrogen as a vehicle fuel.', 'Hydrogen-oxygen reaction has a high Eₐ, so at room temperature almost no collisions are successful; a spark gives some molecules enough energy; the reaction is very exothermic, providing energy for more molecules to react, so it spreads very fast (explosion). Hydrogen is clean (only water) but is highly flammable, leaks easily and needs high-pressure tanks, so strict safety design is needed.', 6, 'long')]
R.f['ch07-st3'].extended = [('A food company wants to slow the browning of cut apples, which is an enzyme-catalysed reaction with oxygen. Suggest three methods, and use collision theory to explain how each one reduces the rate of reaction.', 'Refrigerate – lower temperature, fewer collisions with energy ≥ Eₐ and slower enzyme activity. Coat with lemon juice – low pH changes the enzyme active site (denatures/inhibits) so fewer successful reactions. Seal in packaging with nitrogen or vacuum – lower oxygen concentration, fewer collisions. Keep slices large – smaller surface area exposed.', 6, 'long'),
                            ('In industry the Haber process uses an iron catalyst at about 450 °C. Explain why a catalyst is used, and discuss why manufacturers do not simply use a much higher temperature to increase the rate.', 'Catalyst lowers Eₐ so the rate is economic at a moderate temperature and saves energy costs; it is not used up. Higher temperature would increase rate but costs more fuel, increases CO₂ emissions, and (for this reversible exothermic reaction) reduces the yield of ammonia; a compromise temperature is used.', 6, 'long')]
R.f['ch07-st4'].why += [('Explain how the final volume of gas on a rate graph can be used to identify which reactant was in excess.', 'If increasing the amount of one reactant increases the final volume, that reactant was limiting; if the final volume stays the same, it was in excess.'),
                        ('Explain why the units of rate depend on the measurement made.', 'Rate is change in quantity ÷ time, so it is cm³/s for gas volume, g/s for mass loss and s⁻¹ for 1/time methods.')]
R.f['ch07-st4'].contrast = [('a chord', 'a tangent', 'A chord joins two points on a curve and its gradient gives the mean rate between two times; a tangent touches the curve at one point and its gradient gives the rate at that instant.'),
                            ('a steep curve that levels off at the same height', 'a curve that levels off higher', 'A steeper curve with the same final value means a faster rate with the same amount of limiting reactant; a higher final value means more limiting reactant was used.')]


@R.add('ch07-st4', 'C2', (2, 4), 'explain')
def curve_explain(rng, slot):
    change, desc, why = rng.choice([
        ('the temperature was increased', 'steeper at the start and levels off at the same volume', 'faster particles and more collisions above Eₐ increase the rate; the amount of limiting reactant is unchanged'),
        ('a catalyst was added', 'steeper at the start and levels off at the same volume', 'the catalyst lowers Eₐ so the rate rises, but it does not change the amount of product'),
        ('twice the mass of the limiting reactant was used', 'steeper and levels off at twice the volume', 'more reactant gives more collisions and more product in total'),
        ('the acid was diluted with an equal volume of water, keeping the same moles of acid (acid limiting)', 'less steep but levels off at the same volume', 'lower concentration means fewer collisions per second, but the same number of acid particles react overall'),
        ('marble chips were used instead of the same mass of powder (acid in excess)', 'less steep and levels off at the same volume', 'smaller surface area means fewer collisions per second; the same mass of marble gives the same CO₂')])
    gas = rng.choice(['carbon dioxide', 'hydrogen', 'oxygen'])
    return dict(stem=f'A reaction producing {gas} is repeated but {change}. Describe how the new volume–time curve compares with the original and explain why.', answer=f'The new curve is {desc}: {why}.', type='explain', marks=3,
                markingKey=f'1 initial gradient comparison; 1 final volume comparison ({desc}); 1 explanation: {why}.', gap='G2')


# =============================================================================================
# ch08 Motion
# =============================================================================================
R.facts('ch08-st1', F(
    terms=[('scalar', 'a quantity that has magnitude (size) only, e.g. distance, speed, mass, time'),
           ('vector', 'a quantity that has both magnitude and direction, e.g. displacement, velocity, force, acceleration'),
           ('displacement', 'the straight-line distance from the start point to the end point in a stated direction'),
           ('speed', 'the distance travelled per unit time (a scalar)'),
           ('velocity', 'the displacement per unit time, i.e. speed in a given direction (a vector)'),
           ('average speed', 'total distance travelled divided by total time taken')],
    facts=[('Which of these is a vector quantity?', 'Velocity', ['Speed', 'Distance', 'Mass'], 'Velocity has a direction.'),
           ('A runner completes one lap of a 400 m track. What is her displacement?', '0 m', ['400 m', '200 m', '800 m'], 'She finishes where she started.'),
           ('What is the SI unit of speed?', 'm/s', ['km/h', 'm/s²', 'N'], 'Metres per second.'),
           ('A car drives around a roundabout at a constant 30 km/h. Which statement is true?', 'Its speed is constant but its velocity changes', ['Its velocity is constant', 'Its speed and velocity are both constant', 'It is not moving'], 'Direction changes, so velocity changes.')],
    why=[('Explain why the displacement of a journey can be less than the distance travelled.', 'Distance counts the full path length, but displacement is only the straight-line distance from start to finish; a winding or out-and-back path is longer than the straight line.'),
         ('Explain why an object moving in a circle at constant speed has a changing velocity.', 'Velocity is a vector; although the magnitude stays the same, the direction of motion changes continuously, so the velocity changes.'),
         ('Explain why a distance–time graph for an object moving at constant speed is a straight line.', 'Equal distances are covered in equal times, so distance increases by the same amount each second and the gradient (speed) is constant.')],
    contrast=[('speed', 'velocity', 'Speed is distance per unit time (scalar); velocity is displacement per unit time in a stated direction (vector).'),
              ('distance', 'displacement', 'Distance is the total length of the path (scalar); displacement is the straight-line separation from start to finish with a direction (vector).')],
    misc=[('Two cars travelling at 60 km/h have the same velocity.', 'They only have the same velocity if they move in the same direction; speed is the same but velocity may differ.'),
          ('A negative velocity means the object is slowing down.', 'A negative velocity means motion in the opposite direction to the one chosen as positive.')],
    evaluate=[('Average speed cameras are fairer than fixed speed cameras.', ['measure behaviour over a long stretch, not just at one point', 'drivers cannot simply brake at the camera', 'smoother traffic flow'], ['expensive to install', 'privacy concerns from number-plate tracking', 'drivers may watch speedometer instead of road'], 'Average speed cameras measure what matters (speed over distance) and are fairer, though privacy and cost must be managed.')],
))

VEH = [('a cyclist', (4, 12)), ('a high-speed train', (60, 90)), ('a sprinter', (8, 11)), ('a cheetah', (20, 30)), ('a cargo ship', (5, 10)), ('a commercial jet', (220, 260)), ('a car on a motorway', (25, 33)), ('a swimmer', (1.2, 2.2))]


@R.add('ch08-st1', 'C3', (1, 5), 'numerical')
def speed_calc(rng, slot):
    who = name(rng)
    k = rng.choice(['speed', 'distance', 'time', 'kmh', 'avg', 'disp'] if slot.d >= 3 else ['speed', 'distance', 'time'])
    v_, (lo, hi) = rng.choice(VEH)
    v = round(rng.uniform(lo, hi), 1)
    if k == 'speed':
        t = rng.choice([10, 20, 30, 40, 50, 60, 120])
        d = round(v * t)
        return dict(stem=f'{v_[0].upper() + v_[1:]} travels {d} m in {t} s. Calculate its average speed.', answer=f'{d / t:.3g} m/s', markingKey=f'M1 speed = distance ÷ time = {d} ÷ {t}; A1 {d / t:.3g} m/s.', marks=2)
    if k == 'distance':
        t = rng.choice([5, 15, 25, 45, 90])
        return dict(stem=f'How far does {v_} travelling at {v} m/s go in {t} s?', answer=f'{v * t:.4g} m', markingKey=f'M1 d = v × t = {v} × {t}; A1 {v * t:.4g} m.', marks=2)
    if k == 'time':
        d = rng.choice([100, 400, 1500, 5000, 10000])
        return dict(stem=f'{who} estimates that {v_} moves at {v} m/s. How long will it take to cover {d} m?', answer=f'{d / v:.3g} s', markingKey=f'M1 t = d ÷ v = {d} ÷ {v}; A1 {d / v:.3g} s.', marks=2)
    if k == 'kmh':
        kmh = rng.choice([36, 54, 72, 90, 108, 126, 300])
        t = rng.choice([2, 5, 8])
        return dict(stem=f'A vehicle travels at {kmh} km/h. Convert this speed to m/s and calculate how far the vehicle travels in {t} s.', answer=f'{kmh / 3.6:.3g} m/s; {kmh / 3.6 * t:.3g} m',
                    markingKey=f'M1 × 1000 ÷ 3600 (÷ 3.6); A1 {kmh / 3.6:.3g} m/s; A1 d = v × t = {kmh / 3.6 * t:.3g} m.', marks=3)
    if k == 'avg':
        d1, d2 = rng.randint(2, 15), rng.randint(2, 15)
        t1, t2 = rng.choice([10, 15, 20, 30]), rng.choice([10, 20, 25, 40])
        avg = (d1 + d2) / ((t1 + t2) / 60)
        return dict(stem=f'{who} cycles {d1} km in {t1} minutes, then {d2} km in {t2} minutes. Calculate the average speed for the whole journey in km/h.', answer=f'{avg:.3g} km/h',
                    markingKey=f'M1 total distance {d1 + d2} km; M1 total time {t1 + t2} min = {(t1 + t2) / 60:.3g} h; A1 {avg:.3g} km/h. (Averaging the two speeds is incorrect.)', marks=3)
    e, w = rng.randint(200, 900), rng.randint(100, 800)
    t = rng.choice([200, 300, 400, 500])
    disp = e - w
    return dict(stem=f'{who} walks {e} m east and then {w} m west in a total of {t} s. Calculate (a) the distance travelled, (b) the displacement, (c) the average speed and (d) the average velocity.',
                answer=f'(a) {e + w} m (b) {abs(disp)} m {"east" if disp >= 0 else "west"} (c) {(e + w) / t:.3g} m/s (d) {abs(disp) / t:.3g} m/s {"east" if disp >= 0 else "west"}',
                markingKey=f'1 distance {e + w} m; 1 displacement {abs(disp)} m {"east" if disp >= 0 else "west"}; 1 speed {(e + w)}/{t} = {(e + w) / t:.3g} m/s; 1 velocity {abs(disp)}/{t} = {abs(disp) / t:.3g} m/s with direction.', marks=4)


dataset('ch08-st1',
        dict(intro='{who} used light gates to measure the time for a trolley to travel 1.00 m down ramps of different heights.', iv=('Ramp height', 'cm'), xs=[5, 10, 15, 20, 25],
             dv=('Time to travel 1.00 m', 's'), f=lambda x: 2.2 / math.sqrt(x / 5), dp=2, trend='The time to travel 1.00 m decreases as the ramp height increases, so the average speed increases.',
             why='A higher ramp gives a larger component of weight down the slope, so the trolley accelerates more and reaches higher speeds.'))

inquiry('ch08-st1',
        dict(ctx='how the height of a ramp affects the average speed of a toy car rolling 1.0 m down it',
             iv='height of the raised end of the ramp (cm)', dv='average speed – 1.0 m ÷ time measured with light gates and a data logger',
             cvs=[('length of track used (1.0 m)', 'speed is calculated over a fixed distance'), ('the same toy car', 'mass and friction differ between cars'), ('release method (from rest, not pushed)', 'a push adds initial speed'), ('surface of the ramp', 'friction affects speed')],
             hyp='If the ramp height increases, then the average speed will increase, because more gravitational potential energy is transferred to kinetic energy.',
             method='Set up a 1.2 m ramp; mark start and a point 1.0 m down; position light gates at both; raise the end to 5, 10, 15, 20, 25 cm (measured with a metre rule); release the car from rest; record time; repeat 5 times per height; calculate mean time and speed.',
             weak=('time was measured with a hand-held stopwatch', 'use light gates (or video analysis) to remove reaction-time error of about 0.2 s'),
             safety='place a soft stop at the end of the ramp; keep the track stable'))

R.facts('ch08-st2', F(
    terms=[('acceleration', 'the rate of change of velocity: change in velocity divided by time taken, in m/s²'),
           ('deceleration', 'negative acceleration – a decrease in velocity per unit time'),
           ('velocity–time graph', 'a graph of velocity against time whose gradient gives acceleration and whose area gives displacement'),
           ('uniform acceleration', 'acceleration that stays constant, shown by a straight line on a velocity–time graph')],
    facts=[('What does the gradient of a velocity–time graph represent?', 'Acceleration', ['Distance', 'Speed', 'Force'], 'Gradient = Δv/Δt.'),
           ('What is the unit of acceleration?', 'm/s²', ['m/s', 'm²/s', 'N/kg²'], 'Metres per second per second.'),
           ('On a velocity–time graph, what does a horizontal line show?', 'Constant velocity', ['Stationary object', 'Constant acceleration', 'Deceleration'], 'Zero gradient = zero acceleration.'),
           ('Approximately what is the acceleration of an object in free fall near the Earth’s surface?', '9.8 m/s²', ['98 m/s²', '1 m/s²', '0.98 m/s²'], 'g ≈ 9.8 m/s² (often 10).')],
    why=[('Explain why an object can have a velocity of zero but still be accelerating.', 'Acceleration depends on how velocity is changing; at the top of a throw a ball is momentarily at rest but its velocity is changing at 9.8 m/s² downwards.'),
         ('Explain the difference between the shapes of distance–time and velocity–time graphs for an object accelerating uniformly from rest.', 'The velocity–time graph is a straight line sloping upwards (constant gradient = constant acceleration); the distance–time graph is a curve getting steeper because the speed increases.'),
         ('Explain why a negative gradient on a velocity–time graph means deceleration (if velocity is positive).', 'Velocity is decreasing with time, so the change in velocity is negative and the acceleration is negative.')],
    contrast=[('a distance–time graph', 'a velocity–time graph', 'The gradient of a distance–time graph is speed; the gradient of a velocity–time graph is acceleration and its area is distance travelled.'),
              ('acceleration', 'velocity', 'Velocity is the rate of change of displacement (m/s); acceleration is the rate of change of velocity (m/s²).')],
    misc=[('An object with a large velocity must have a large acceleration.', 'A plane cruising at 250 m/s at constant velocity has zero acceleration; acceleration depends on change in velocity.'),
          ('A downward-sloping line on a velocity–time graph means the object is moving backwards.', 'It means the velocity is decreasing (decelerating); the object is still moving forwards while velocity is positive.')],
    cases=[('Usain Bolt’s 100 m world record (Berlin, 2009)', 'He reached about 12 m/s within about 4 s of the start and finished in 9.58 s.', 'acceleration and velocity–time graphs', 'His velocity–time graph rises steeply at first (large acceleration) then levels off near top speed (zero acceleration).'),
           ('the Formula Rossa roller coaster in Abu Dhabi', 'It accelerates from 0 to about 240 km/h (67 m/s) in 4.9 s.', 'calculating acceleration', 'a = Δv/t = 67/4.9 ≈ 14 m/s², which is about 1.4 times g.')],
    evaluate=[('Electric cars are safer than petrol cars because they accelerate faster.', ['rapid acceleration helps when merging or overtaking', 'low centre of gravity from batteries reduces rollover'], ['high acceleration can lead to loss of control by inexperienced drivers', 'heavier cars cause more damage in collisions', 'safety depends mostly on driver behaviour, braking and design'], 'Faster acceleration is not in itself a safety advantage; safety depends on many design and behavioural factors.')],
))


@R.add('ch08-st2', 'C3', (1, 5), 'numerical')
def accel(rng, slot):
    who = name(rng)
    k = rng.choice(['a', 'v', 't', 'kmh', 'graph'] if slot.d >= 3 else ['a', 'v', 't'])
    if k == 'a':
        u = rng.choice([0, 0, 2, 4, 5, 10])
        v = u + rng.choice([6, 8, 12, 15, 20, 24])
        t = rng.choice([2, 3, 4, 5, 6, 8])
        obj = rng.choice(['A bus', 'A cyclist', 'A lift', 'A motorbike', 'An electric scooter'])
        return dict(stem=f'{obj} speeds up from {u} m/s to {v} m/s in {t} s. Calculate its acceleration.', answer=f'{(v - u) / t:.3g} m/s²',
                    markingKey=f'M1 a = (v − u)/t = ({v} − {u})/{t}; A1 {(v - u) / t:.3g} m/s².', marks=2)
    if k == 'v':
        a = rng.choice([1.5, 2.0, 2.5, 3.0, 4.0])
        t = rng.choice([3, 4, 5, 6, 10])
        u = rng.choice([0, 3, 5])
        return dict(stem=f'A sprinter starting at {u} m/s accelerates at {a} m/s² for {t} s. What is her final velocity?', answer=f'{u + a * t:.3g} m/s',
                    markingKey=f'M1 v = u + at = {u} + {a} × {t}; A1 {u + a * t:.3g} m/s.', marks=2)
    if k == 't':
        u = rng.choice([20, 25, 30])
        a = rng.choice([4, 5, 6, 8])
        return dict(stem=f'A car travelling at {u} m/s brakes with a deceleration of {a} m/s². How long does it take to stop?', answer=f'{u / a:.3g} s',
                    markingKey=f'M1 t = (v − u)/a = (0 − {u})/(−{a}); A1 {u / a:.3g} s.', marks=2)
    if k == 'kmh':
        kmh = rng.choice([72, 90, 100, 108, 126])
        t = rng.choice([4.0, 5.5, 6.2, 8.0, 9.5])
        return dict(stem=f'An electric car accelerates from 0 to {kmh} km/h in {t} s. Calculate its mean acceleration in m/s².', answer=f'{kmh / 3.6 / t:.3g} m/s²',
                    markingKey=f'M1 {kmh} km/h = {kmh / 3.6:.3g} m/s; M1 ÷ {t}; A1 {kmh / 3.6 / t:.3g} m/s².', marks=3)
    v1 = rng.choice([8, 10, 12, 15, 20])
    t1, t2, t3 = rng.choice([4, 5]), rng.choice([10, 12, 15]), rng.choice([18, 20, 22])
    return dict(stem=f'A velocity–time graph for a train shows: velocity rises uniformly from 0 to {v1} m/s in the first {t1} s, stays at {v1} m/s until {t2} s, then falls uniformly to 0 at {t3} s. Calculate the acceleration in each of the three stages.',
                answer=f'{v1 / t1:.3g} m/s²; 0 m/s²; {-v1 / (t3 - t2):.3g} m/s²', markingKey=f'1 stage 1: {v1}/{t1} = {v1 / t1:.3g} m/s²; 1 stage 2: 0 (horizontal line); 1 stage 3: −{v1}/{t3 - t2} = {-v1 / (t3 - t2):.3g} m/s² (deceleration).', marks=3)


dataset('ch08-st2',
        dict(intro='{who} released a trolley from rest on a slope and used a data logger to record its velocity at intervals.', iv=('Time', 's'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Velocity', 'm/s'), f=lambda x: 0.8 * x, dp=2, trend='Velocity increases by about the same amount every 0.5 s – the trolley accelerates uniformly.',
             why='The resultant force down the slope (component of weight minus friction) is constant, so the acceleration is constant (a = F/m).'))

inquiry('ch08-st2',
        dict(ctx='how the angle of a slope affects the acceleration of a trolley rolling down it',
             iv='angle of the slope (5°, 10°, 15°, 20°, 25°, measured with a protractor or phone inclinometer)', dv='acceleration – from two light gates and a card of known length: a = (v₂ − v₁)/t',
             cvs=[('mass of the trolley', 'affects friction'), ('distance between light gates', 'changes the time measured'), ('starting position (from rest)', 'affects velocities'), ('track surface', 'friction')],
             hyp='If the angle increases, then the acceleration will increase, because the component of the trolley’s weight acting down the slope increases while friction changes little.',
             method='Set track at 5° and mark start; place light gates 30 cm and 80 cm down; fix a 10 cm card to the trolley; release from rest; data logger calculates v at each gate and time between; a = Δv/Δt; repeat 3 times; repeat for 10-25°.',
             weak=('the trolley was sometimes released with a small push', 'release the trolley from rest by holding it against a block and removing the block'),
             safety='catch the trolley at the bottom; keep fingers away from the track'))

R.facts('ch08-st3', F(
    terms=[('area under a velocity–time graph', 'equal to the distance travelled (displacement) during that time'),
           ('trapezium rule (for v–t graphs)', 'finding the area of a region with straight sloping top as ½ × (sum of parallel sides) × width'),
           ('average velocity (uniform acceleration)', 'the mean of initial and final velocity, (u + v)/2')],
    facts=[('A car travels at a steady 20 m/s for 10 s. What area under the v–t graph represents this, and what distance is it?', 'A rectangle of 200 m', ['A triangle of 100 m', 'A rectangle of 30 m', 'A triangle of 200 m'], '20 × 10 = 200 m.'),
           ('An object accelerates uniformly from rest to 10 m/s in 4 s. What distance does it travel?', '20 m', ['40 m', '10 m', '2.5 m'], 'Triangle area ½ × 4 × 10.'),
           ('On a v–t graph, an area below the time axis represents what?', 'Displacement in the opposite direction', ['Negative time', 'Deceleration', 'Zero distance'], 'Negative velocity means opposite direction.')],
    why=[('Explain why the area under a velocity–time graph gives the distance travelled.', 'Distance = velocity × time; each thin strip of the graph has area velocity × small time interval, so adding all strips (the area) gives total distance.'),
         ('Explain why counting squares is needed for a curved velocity–time graph.', 'The area under a curve cannot be found exactly with simple shapes, so it is estimated by counting squares (and part squares) and multiplying by the distance each square represents.')],
    misc=[('The distance travelled is the height of the v–t graph at the end.', 'The height is the final velocity; distance is the area under the line.'),
          ('For uniform acceleration from rest, distance = final velocity × time.', 'That would be the rectangle; the correct area is the triangle ½ × v × t.')],
    evaluate=[('Velocity–time graphs from phone GPS apps give accurate distances for sports training.', ['convenient and automatic; area calculated by the app', 'good for long, steady runs'], ['GPS errors of several metres, especially among tall buildings', 'sampling interval misses quick changes in speed', 'poor for short sprints'], 'Good enough for general training but not accurate for sprints or precise measurements.')],
))


@R.add('ch08-st3', 'C3', (1, 5), 'numerical')
def vt_area(rng, slot):
    k = rng.choice(['tri', 'trap', 'multi', 'compare'] if slot.d >= 3 else ['tri', 'trap'])
    if k == 'tri':
        v = rng.choice([6, 8, 10, 12, 15, 20])
        t = rng.choice([4, 5, 6, 8, 10])
        return dict(stem=f'A velocity–time graph shows an object accelerating uniformly from rest to {v} m/s in {t} s. Calculate the distance travelled.', answer=f'{0.5 * v * t:g} m',
                    markingKey=f'M1 area of triangle = ½ × {t} × {v}; A1 {0.5 * v * t:g} m.', marks=2)
    if k == 'trap':
        u, v = rng.choice([(4, 10), (5, 15), (8, 20), (10, 25), (12, 18)])
        t = rng.choice([4, 5, 6, 8])
        return dict(stem=f'A cyclist accelerates uniformly from {u} m/s to {v} m/s in {t} s. Use the area under the velocity–time graph to find the distance travelled.', answer=f'{0.5 * (u + v) * t:g} m',
                    markingKey=f'M1 trapezium ½ × ({u} + {v}) × {t} (or rectangle + triangle); A1 {0.5 * (u + v) * t:g} m.', marks=2)
    if k == 'multi':
        v = rng.choice([10, 12, 15, 18, 20])
        t1, t2, t3 = rng.choice([4, 5, 6]), rng.choice([10, 15, 20]), rng.choice([4, 5, 8])
        d = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
        vehicle = rng.choice(['A tram', 'A metro train', 'An airport shuttle'])
        return dict(stem=f'{vehicle} accelerates uniformly from rest to {v} m/s in {t1} s, travels at {v} m/s for {t2} s, then decelerates uniformly to rest in {t3} s. Sketch the velocity–time graph and calculate (a) the total distance travelled and (b) the average speed for the journey.',
                    answer=f'(a) {d:g} m (b) {d / (t1 + t2 + t3):.3g} m/s', markingKey=f'1 correct sketch; M1 areas: {0.5 * v * t1:g} + {v * t2:g} + {0.5 * v * t3:g}; A1 {d:g} m; A1 average speed {d:g} ÷ {t1 + t2 + t3} = {d / (t1 + t2 + t3):.3g} m/s.', marks=4)
    v = rng.choice([20, 25, 30])
    tr = rng.choice([0.6, 0.7, 0.8, 1.0, 1.5])
    tb = rng.choice([4, 5, 6])
    th, br = v * tr, 0.5 * v * tb
    return dict(stem=f'A driver travelling at {v} m/s sees a hazard. Her reaction time is {tr} s, after which she brakes uniformly to rest in {tb} s. Use a velocity–time graph to calculate the thinking distance, braking distance and stopping distance.',
                answer=f'thinking {th:g} m; braking {br:g} m; stopping {th + br:g} m', markingKey=f'1 thinking = rectangle {v} × {tr} = {th:g} m; 1 braking = triangle ½ × {v} × {tb} = {br:g} m; 1 stopping = {th + br:g} m.', marks=3)


dataset('ch08-st3',
        dict(intro='A cyclist starting from rest recorded her velocity every 2 s on three rides along the same straight road.', iv=('Time', 's'), xs=[2, 4, 6, 8, 10],
             dv=('Velocity', 'm/s'), f=lambda x: 1.2 * x, dp=1, trend='Velocity increases steadily with time, so the acceleration is roughly uniform.',
             why='A constant resultant force from pedalling produces constant acceleration; starting from rest, the distance in 10 s is the triangle area under the v–t graph, ½ × 10 × final velocity.'))

inquiry('ch08-st3',
        dict(ctx='how accurately the area under a velocity–time graph (from a data-logger) predicts the measured distance travelled by a trolley',
             iv='angle of the ramp (to give different accelerations)', dv='percentage difference between the distance from the v–t graph area and the distance measured with a metre rule',
             cvs=[('sampling rate of the data logger', 'fewer readings give a less accurate graph'), ('the same trolley and track', 'friction differences'), ('release from rest', 'initial velocity affects area')],
             hyp='If the acceleration is uniform, then the area under the graph will match the measured distance within a few percent, because distance equals the area under a v–t graph.',
             method='Attach a motion sensor at the top of a ramp; record velocity 20 times per second as the trolley rolls 1.5 m; export the graph; calculate area (trapezia); measure actual distance with a metre rule; repeat at 4 angles, 3 times each; calculate % difference.',
             safety='secure sensor and catch the trolley'))

R.facts('ch08-st4', F(
    terms=[('equations of motion (suvat)', 'equations linking displacement s, initial velocity u, final velocity v, acceleration a and time t for uniform acceleration'),
           ('free fall', 'motion under gravity alone, with acceleration g ≈ 9.8 m/s² downwards (air resistance negligible)'),
           ('initial velocity (u)', 'the velocity at the start of the time interval being considered')],
    facts=[('Which equation links v, u, a and s (no t)?', 'v² = u² + 2as', ['v = u + at', 's = ut + ½at²', 's = (u + v)t'], 'Eliminating t gives v² = u² + 2as.'),
           ('Under what condition can the equations of motion be used?', 'When acceleration is constant', ['When velocity is constant only', 'At any time', 'Only for falling objects'], 'They assume uniform acceleration.'),
           ('A ball is dropped from rest. What is its velocity after 2 s (g = 9.8 m/s², no air resistance)?', '19.6 m/s', ['9.8 m/s', '4.9 m/s', '39.2 m/s'], 'v = 0 + 9.8 × 2.')],
    why=[('Explain why the equations of motion cannot be used for a skydiver over the whole fall.', 'Air resistance increases with speed, so the resultant force and acceleration change; the equations require constant acceleration.'),
         ('Explain why choosing a positive direction is important when using the equations of motion.', 'Displacement, velocity and acceleration are vectors; quantities in the opposite direction must be negative, e.g. g = −9.8 m/s² for a ball thrown upwards.')],
    misc=[('A ball thrown upwards has zero acceleration at the top of its flight.', 'Its velocity is zero at the top, but acceleration is still 9.8 m/s² downwards.'),
          ('If a car doubles its speed, its braking distance doubles.', 'From v² = u² + 2as, braking distance is proportional to u², so it quadruples.')],
    evaluate=[('Using g = 10 m/s² instead of 9.8 m/s² is acceptable in calculations.', ['simplifies arithmetic, only 2% error', 'other uncertainties (air resistance) are often larger'], ['in precise work 2% matters', 'g varies with location (9.78-9.83 m/s²)'], 'Acceptable for estimates when the precision of the data does not justify more; use 9.8 or 9.81 for precise answers.')],
))


@R.add('ch08-st4', 'C3', (1, 5), 'numerical')
def suvat(rng, slot):
    g = 9.8
    k = rng.choice(['drop_v', 'drop_s', 'brake', 'runway', 'throw', 'drop_t'] if slot.d >= 3 else ['drop_v', 'drop_s', 'brake'])
    if k == 'drop_v':
        h = rng.choice([1.25, 5.0, 11.25, 20.0, 31.25, 45.0])
        v = math.sqrt(2 * g * h)
        thing = rng.choice(['A coconut falls', 'A stone is dropped', 'A phone slips and falls', 'A diver steps off a platform and falls'])
        return dict(stem=f'{thing} from rest through {h} m. Ignoring air resistance, calculate its speed just before it lands (g = 9.8 m/s²).', answer=f'{v:.3g} m/s',
                    markingKey=f'M1 v² = u² + 2as = 0 + 2 × 9.8 × {h}; A1 {v:.3g} m/s.', marks=2)
    if k == 'drop_s':
        t = rng.choice([1.0, 1.5, 2.0, 2.5, 3.0])
        return dict(stem=f'A pebble is dropped from rest down a well and hits the water after {t} s. Ignoring air resistance, how deep is the well? (g = 9.8 m/s²)', answer=f'{0.5 * g * t * t:.3g} m',
                    markingKey=f'M1 s = ut + ½at² = 0 + ½ × 9.8 × {t}²; A1 {0.5 * g * t * t:.3g} m.', marks=2)
    if k == 'drop_t':
        h = rng.choice([10, 20, 45, 80])
        t = math.sqrt(2 * h / g)
        return dict(stem=f'How long does an object take to fall {h} m from rest, ignoring air resistance (g = 9.8 m/s²)?', answer=f'{t:.3g} s',
                    markingKey=f'M1 s = ½gt² rearranged t = √(2s/g) = √(2 × {h}/9.8); A1 {t:.3g} s.', marks=2)
    if k == 'brake':
        u = rng.choice([10, 15, 20, 25, 30])
        a = rng.choice([5, 6, 7.5, 8])
        s = u * u / (2 * a)
        return dict(stem=f'A car moving at {u} m/s brakes with a constant deceleration of {a} m/s². Calculate the braking distance.', answer=f'{s:.3g} m',
                    markingKey=f'M1 v² = u² + 2as with v = 0, a = −{a}: 0 = {u}² − 2 × {a} × s; A1 s = {s:.3g} m.', marks=2)
    if k == 'runway':
        v = rng.choice([60, 70, 75, 80])
        a = rng.choice([2.0, 2.5, 3.0])
        s = v * v / (2 * a)
        t = v / a
        return dict(stem=f'An aircraft must reach {v} m/s to take off. It accelerates uniformly from rest at {a} m/s². Calculate (a) the minimum runway length and (b) the time taken.', answer=f'(a) {s:.0f} m (b) {t:.3g} s',
                    markingKey=f'(a) M1 s = v²/(2a) = {v}²/(2 × {a}); A1 {s:.0f} m. (b) M1 t = v/a; A1 {t:.3g} s.', marks=4)
    u = rng.choice([8, 10, 12, 15])
    hmax = u * u / (2 * g)
    tt = 2 * u / g
    return dict(stem=f'A ball is thrown vertically upwards at {u} m/s. Ignoring air resistance (g = 9.8 m/s²), calculate (a) the maximum height and (b) the total time before it returns to the thrower’s hand.', answer=f'(a) {hmax:.3g} m (b) {tt:.3g} s',
                markingKey=f'(a) M1 0 = {u}² − 2 × 9.8 × s; A1 {hmax:.3g} m. (b) M1 time up = {u}/9.8; A1 total {tt:.3g} s (symmetry).', marks=4)


@R.add('ch08-st4', 'C4', (3, 5), 'multi_step')
def stopping_compare(rng, slot):
    u1 = rng.choice([13.4, 15.0, 20.0])
    f = rng.choice([1.5, 2.0])
    u2 = u1 * f
    a = rng.choice([6.5, 7.0, 8.0])
    tr = rng.choice([0.7, 0.8, 1.0])
    s1 = u1 * tr + u1 ** 2 / (2 * a)
    s2 = u2 * tr + u2 ** 2 / (2 * a)
    return dict(stem=f'Near a school the speed limit is {u1:g} m/s; on the main road it is {u2:g} m/s. A driver has a reaction time of {tr} s and the car decelerates at {a} m/s². (a) Calculate the stopping distance at each speed. (b) Show that the braking distance increases by a factor of {f * f:g} when the speed increases by a factor of {f}. (c) Use your answers to justify low speed limits near schools.',
                answer=f'(a) {s1:.3g} m and {s2:.3g} m (b) braking ∝ u², ({f})² = {f * f:g} (c) stopping distance is much shorter at low speed, so drivers can stop before hitting a child who steps out',
                markingKey=f'(a) M1 thinking = u × {tr}; M1 braking = u²/(2 × {a}); A1 {s1:.3g} m; A1 {s2:.3g} m. (b) 1 from v² = u² + 2as, s ∝ u². (c) 1 reasoned link to safety/impact speed.', marks=6, gap='G5')


dataset('ch08-st4',
        dict(intro='{who} dropped a ball from different heights and measured the time to fall with light gates.', iv=('Drop height', 'm'), xs=[0.50, 1.00, 1.50, 2.00, 2.50],
             dv=('Fall time', 's'), f=lambda x: math.sqrt(2 * x / 9.8), dp=3, trend='Fall time increases with height, but not proportionally – doubling the height increases the time by about 1.4 times (√2).',
             why='For uniform acceleration from rest s = ½gt², so t = √(2s/g); time is proportional to the square root of height.'))

R.f['ch08-st2'].extended = [('A lift starts from rest, accelerates uniformly at 1.5 m/s² for 2 s, travels at constant velocity for 6 s, then decelerates uniformly to rest in 3 s. (a) Calculate the maximum velocity. (b) Sketch the velocity–time graph with values. (c) Calculate the deceleration. (d) Calculate the total distance travelled.', '(a) v = 1.5 × 2 = 3 m/s (b) rise 0→3 m/s over 0–2 s, flat to 8 s, fall to 0 at 11 s (c) 3/3 = 1 m/s² (d) 3 + 18 + 4.5 = 25.5 m', 6),
                            ('A student says: "The steeper the line on any motion graph, the faster the object is going." Evaluate this statement for distance–time and velocity–time graphs, using examples.', 'True for distance–time graphs: gradient = speed. Not true for velocity–time graphs: gradient = acceleration; a steep line means velocity is changing quickly, not that the velocity is high – e.g. a car pulling away has a steep v–t line at low speed, while a plane cruising at 250 m/s has a flat line.', 4)]

R.f['ch08-st3'].why += [('Explain why the area under a velocity–time graph for a car that brakes uniformly to rest is a triangle.', 'Velocity falls steadily from u to 0, so the line is straight from (0, u) to (t, 0); the region under it is a right-angled triangle with area ½ × u × t.'),
                        ('Explain how a velocity–time graph can show that two runners travelled the same distance even though their graphs have different shapes.', 'Distance is the area under each graph; different shapes (e.g. fast start then slowing, or steady pace) can enclose the same area.')]
R.f['ch08-st3'].contrast = [('the gradient of a velocity–time graph', 'the area under a velocity–time graph', 'The gradient gives acceleration (m/s²); the area gives distance or displacement (m).'),
                            ('the area under a speed–time graph', 'the area under a velocity–time graph', 'Area under a speed–time graph gives total distance; area under a velocity–time graph gives displacement, with areas below the axis counted as negative.')]
R.f['ch08-st3'].extended = [('Two cars start from rest at the same time. Car A accelerates at 2 m/s² for 10 s and then travels at constant velocity. Car B accelerates at 1.5 m/s² for 16 s and then travels at constant velocity. Using velocity–time graphs, find which car has travelled further after 20 s and by how much.', 'A: v = 20 m/s; area = ½ × 10 × 20 + 20 × 10 = 300 m. B: v = 24 m/s; area = ½ × 16 × 24 + 24 × 4 = 192 + 96 = 288 m. Car A by 12 m.', 6),
                            ('A sprinter’s velocity–time graph is a curve rising from 0 to 11 m/s over the first 5 s, then flat. Explain how you would estimate the distance covered in the first 5 s from the graph, and explain why simply using ½ × 5 × 11 would give an underestimate.', 'Count squares under the curve and multiply by the distance each square represents (or split into trapezia). The curve rises quickly and lies above the straight line from (0,0) to (5,11), so the triangle area (27.5 m) underestimates the true area.', 4)]


@R.add('ch08-st3', 'C2', (2, 4), 'explain')
def vt_compare(rng, slot):
    v1, t1 = rng.choice([(10, 8), (12, 6), (8, 10), (15, 4)])
    v2 = rng.choice([6, 7, 9, 11])
    t2 = t1
    d1, d2 = 0.5 * v1 * t1, v2 * t2
    a, b = two_names(rng)
    winner = a if d1 > d2 else b
    return dict(stem=f'{a} accelerates uniformly from rest to {v1} m/s in {t1} s. {b} runs at a constant {v2} m/s for the same {t2} s. Explain, by comparing the areas under their velocity–time graphs, who travels further.',
                answer=f'{a}: triangle ½ × {t1} × {v1} = {d1:g} m; {b}: rectangle {v2} × {t2} = {d2:g} m; {winner if d1 != d2 else "neither"} travels further.', type='explain', marks=3,
                markingKey=f'1 distance = area under v–t graph; 1 {a} {d1:g} m and {b} {d2:g} m; 1 conclusion.', gap='G2')


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step')
def catch_up(rng, slot):
    a = rng.choice([2.0, 2.5, 3.0])
    v = rng.choice([10, 12, 15])
    t = 2 * v / a
    d = v * t
    return dict(stem=f'A police motorbike starts from rest and accelerates at {a} m/s² at the moment a car passes it at a constant {v} m/s. (a) Sketch both velocity–time graphs on the same axes. (b) Use the areas to show that the motorbike catches the car after {t:g} s. (c) Calculate the distance travelled by then and the motorbike’s velocity at that moment, and comment on whether this is realistic.',
                answer=f'(b) car area {v}t = bike area ½ × {a}t² ⇒ t = 2 × {v}/{a} = {t:g} s (c) {d:g} m; bike velocity {a * t:g} m/s (twice the car’s) – unrealistic if it exceeds legal/safe speeds, and constant acceleration is unlikely',
                markingKey=f'(a) 1 horizontal line at {v} m/s and straight line from origin with gradient {a}. (b) M1 equate areas; A1 t = {t:g} s. (c) A1 {d:g} m; A1 {a * t:g} m/s; 1 sensible evaluation.', marks=6, gap='G5')


R.f['ch08-st4'].why += [('Explain why a ball dropped and a ball thrown horizontally from the same height (with no air resistance) hit the ground at the same time.', 'Vertical motion is independent of horizontal motion; both start with zero vertical velocity and have the same vertical acceleration g, so s = ½gt² gives the same time.'),
                        ('Explain why v = u + at gives a negative velocity if a ball thrown upwards is considered after a long enough time.', 'Taking up as positive, a = −9.8 m/s²; after the top, at exceeds u so v becomes negative, meaning the ball is moving downwards.')]
R.f['ch08-st4'].contrast = [('v = u + at', 'v² = u² + 2as', 'v = u + at links velocity and time (no displacement); v² = u² + 2as links velocity and displacement (no time).'),
                            ('initial velocity u', 'final velocity v', 'u is the velocity at the start of the time interval; v is the velocity at the end of it.')]


@R.add('ch08-st4', 'C2', (2, 4), 'explain')
def suvat_error(rng, slot):
    u = rng.choice([10, 15, 20, 25])
    a = rng.choice([4, 5, 8])
    t = rng.choice([2, 3])
    wrong = u + a * t
    right = u - a * t
    if right < 0:
        return None
    who = name(rng)
    return dict(stem=f'A car travelling at {u} m/s brakes with a deceleration of {a} m/s² for {t} s. {who} uses v = u + at and gets v = {u} + {a} × {t} = {wrong} m/s. Explain the mistake and find the correct velocity.',
                answer=f'Deceleration means a = −{a} m/s²; v = {u} − {a} × {t} = {right} m/s.', type='explain', marks=2,
                markingKey=f'1 acceleration must be negative because velocity decreases (vector direction opposite to motion); 1 v = {right} m/s.', gap='G2')


# =============================================================================================
# ch09 Forces and Newton's Laws
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('force', 'a push or pull on an object, measured in newtons (N); a vector quantity'),
           ('resultant force', 'the single force that has the same effect as all the forces acting on an object combined'),
           ('free-body diagram', 'a diagram of one object showing all the forces acting on it as labelled arrows from the object'),
           ('weight', 'the gravitational force acting on an object, W = m × g'),
           ('normal contact force (reaction)', 'the force exerted by a surface on an object, acting at right angles to the surface'),
           ('balanced forces', 'forces whose resultant is zero, so the object’s velocity does not change')],
    facts=[('A box has a 30 N force pushing right and a 12 N friction force acting left. What is the resultant force?', '18 N to the right', ['42 N to the right', '18 N to the left', '0 N'], '30 − 12 = 18 N.'),
           ('What is the weight of a 5 kg mass on Earth (g = 9.8 N/kg)?', '49 N', ['5 N', '0.5 N', '490 N'], 'W = 5 × 9.8.'),
           ('On a free-body diagram of a book resting on a table, which two forces act on the book?', 'Weight downwards and normal contact force upwards', ['Weight and friction', 'Normal force and air resistance', 'Only weight'], 'They balance, so the resultant is zero.'),
           ('What is the unit of force?', 'Newton (N)', ['Joule (J)', 'Kilogram (kg)', 'Watt (W)'], '1 N = 1 kg m/s².')],
    why=[('Explain why a parachutist falling at a steady speed has a resultant force of zero.', 'Steady speed in a straight line means no acceleration; by Newton’s first law the forces (weight and air resistance) must be balanced.'),
         ('Explain why weight and mass are different quantities.', 'Mass is the amount of matter in an object (kg) and is the same everywhere; weight is the gravitational force on it (N), W = mg, so it depends on the gravitational field strength.'),
         ('Explain why free-body diagrams only show forces acting on the chosen object.', 'The motion of an object depends only on the forces acting on it; including forces it exerts on other objects would give the wrong resultant.')],
    contrast=[('mass', 'weight', 'Mass is the amount of matter (kg), the same everywhere; weight is the gravitational force (N) and changes with g (e.g. smaller on the Moon).'),
              ('balanced forces', 'unbalanced forces', 'Balanced forces give zero resultant – the object stays at rest or at constant velocity; unbalanced forces give a resultant that changes the speed or direction.')],
    misc=[('An astronaut has no mass on the Moon.', 'Mass is unchanged; her weight is about one-sixth of her Earth weight because g on the Moon is 1.6 N/kg.'),
          ('If an object is moving, there must be a resultant force on it.', 'A resultant force is needed to change motion; an object moving at constant velocity has zero resultant force.'),
          ('A book on a table has no forces acting on it because it is not moving.', 'Weight and the normal contact force act on it; they are balanced.')],
    cases=[('a tug-of-war contest', 'When both teams pull with 2000 N the rope does not move; when one team pulls with 2200 N the rope accelerates towards them.', 'resultant forces', 'Equal and opposite pulls give zero resultant; a 200 N resultant accelerates the rope and teams.'),
           ('an astronaut on the International Space Station', 'An 80 kg astronaut floats inside the ISS even though gravity at that height is still about 8.7 N/kg.', 'weight and free-body diagrams', 'Weight still acts (about 700 N), but both the astronaut and the station are in free fall, so there is no normal contact force – she feels weightless.')],
    evaluate=[('Free-body diagrams are the most useful tool for solving force problems.', ['make all forces and directions clear', 'help find the resultant and apply F = ma', 'reduce mistakes'], ['difficult for forces at angles or rotating objects', 'not needed for very simple one-force problems'], 'They are very useful for most problems, especially with several forces, though calculations still require vector addition.')],
    extended=[('A 1200 kg car is towed along a level road by a rope with a tension of 2400 N. Friction and air resistance total 900 N. (a) Draw a free-body diagram of the car showing all four forces. (b) Calculate the weight of the car (g = 9.8 N/kg). (c) Calculate the resultant force and the acceleration.', '(a) tension forwards, resistance backwards, weight down, normal force up (equal to weight). (b) 11 760 N. (c) 2400 − 900 = 1500 N forwards; a = 1500/1200 = 1.25 m/s².', 6),
              ('A student says that a ball thrown upwards has an upward force acting on it while it rises. Evaluate this statement with a free-body diagram.', 'Incorrect: once released, the only forces are weight (down) and small air resistance (down while rising). The ball continues upward because of its velocity (inertia), and slows because the resultant force is downward.', 4)],
))


@R.add('ch09-st1', 'C3', (1, 5), 'numerical')
def resultant(rng, slot):
    k = rng.choice(['line', 'line', 'weight', 'perp', 'four'] if slot.d >= 3 else ['line', 'weight'])
    if k == 'line':
        a, b = rng.randint(10, 90) * 10, rng.randint(5, 80) * 10
        obj = rng.choice(['A boat’s engine pushes it forward with', 'A cyclist’s driving force is', 'A rocket’s thrust is', 'A team pushes a stalled car with'])
        r_ = a - b
        return dict(stem=f'{obj} {a} N. The total resistive force is {b} N. Calculate the size and direction of the resultant force and describe the motion.', answer=f'{abs(r_)} N {"forwards" if r_ > 0 else "backwards" if r_ < 0 else ""}'.strip() + ('; accelerates' if r_ > 0 else '; decelerates' if r_ < 0 else '; constant velocity'),
                    markingKey=f'M1 {a} − {b}; A1 {abs(r_)} N with direction; 1 motion: ' + ('speeds up' if r_ > 0 else 'slows down' if r_ < 0 else 'constant velocity') + '.', marks=3)
    if k == 'weight':
        m = rng.choice([0.5, 2.0, 12, 45, 60, 75, 1200])
        place, gg = rng.choice([('Earth', 9.8), ('the Moon', 1.6), ('Mars', 3.7), ('Jupiter', 24.8)])
        return dict(stem=f'Calculate the weight of a {m} kg object on {place}, where the gravitational field strength is {gg} N/kg.', answer=f'{m * gg:.4g} N',
                    markingKey=f'M1 W = m × g = {m} × {gg}; A1 {m * gg:.4g} N.', marks=2)
    if k == 'perp':
        a, b = rng.choice([(3, 4), (6, 8), (5, 12), (9, 12), (8, 15), (7, 24), (20, 21)])
        sc = rng.choice([100, 500, 1000])
        R_ = math.hypot(a, b) * sc
        ang = math.degrees(math.atan(b / a))
        return dict(stem=f'Two tugboats pull a ship with forces of {a * sc} N east and {b * sc} N north. Calculate the magnitude of the resultant force and its angle north of east.', answer=f'{R_:g} N at {ang:.1f}° north of east',
                    markingKey=f'M1 Pythagoras √({a * sc}² + {b * sc}²); A1 {R_:g} N; M1 tan θ = {b * sc}/{a * sc}; A1 {ang:.1f}°.', marks=4)
    up, down = rng.randint(200, 900), rng.randint(200, 900)
    f, bk = rng.randint(100, 600), rng.randint(100, 600)
    ry, rx = up - down, f - bk
    return dict(stem=f'A free-body diagram shows four forces on a drone: lift {up} N up, weight {down} N down, thrust {f} N forwards and drag {bk} N backwards. Calculate the resultant vertical and horizontal forces and describe the motion they cause.',
                answer=f'vertical {abs(ry)} N {"up" if ry > 0 else "down" if ry < 0 else "(balanced)"}; horizontal {abs(rx)} N {"forwards" if rx > 0 else "backwards" if rx < 0 else "(balanced)"}',
                markingKey=f'1 vertical {up} − {down} = {ry} N; 1 horizontal {f} − {bk} = {rx} N; 1 motion described (accelerates in direction of each non-zero resultant; constant velocity where balanced).', marks=3)


dataset('ch09-st1',
        dict(intro='{who} hung masses on a newton meter on Earth to investigate the relationship between mass and weight.', iv=('Mass', 'kg'), xs=[0.1, 0.2, 0.3, 0.4, 0.5],
             dv=('Weight', 'N'), f=lambda x: 9.8 * x, dp=2, trend='Weight increases in direct proportion to mass (doubling the mass doubles the weight).',
             why='W = mg; the gradient of a weight–mass graph equals the gravitational field strength, about 9.8 N/kg.'))

inquiry('ch09-st1',
        dict(ctx='how the mass of a wooden block affects the force needed to pull it at a steady speed across a bench',
             iv='total mass of the block plus added masses (kg)', dv='pulling force in N read from a newton meter while the block moves at steady speed (equals friction)',
             cvs=[('surface of the bench and block', 'rougher surfaces increase friction'), ('speed of pulling (slow and steady)', 'acceleration would need extra force'), ('direction of pull (horizontal)', 'an angled pull lifts the block'), ('the same newton meter, zeroed', 'zero errors')],
             hyp='If the mass increases, then the pulling force will increase in proportion, because a heavier block presses harder on the bench (larger normal force), increasing friction.',
             method='Weigh the block; attach a 10 N newton meter; pull horizontally at a slow steady speed and read the force; add 100 g masses up to 500 g; repeat 3 times each; plot force against mass.',
             weak=('the block was jerked into motion and the peak reading was recorded', 'read the force once the block is moving at a steady speed (or use a force sensor and take the mean steady reading)'),
             safety='keep masses secure on the block and away from the bench edge'))

R.facts('ch09-st2', F(
    terms=[('Newton’s first law', 'an object remains at rest or moves at constant velocity unless acted on by a resultant force'),
           ('Newton’s second law', 'the acceleration of an object is directly proportional to the resultant force and inversely proportional to its mass: F = ma'),
           ('inertia', 'the tendency of an object to resist changes in its motion; greater mass means greater inertia'),
           ('newton (N)', 'the force that gives a mass of 1 kg an acceleration of 1 m/s²')],
    facts=[('What resultant force is needed to accelerate a 2 kg mass at 3 m/s²?', '6 N', ['1.5 N', '5 N', '0.67 N'], 'F = ma = 2 × 3.'),
           ('If the resultant force on an object doubles and its mass stays the same, what happens to its acceleration?', 'It doubles', ['It halves', 'It stays the same', 'It quadruples'], 'a ∝ F.'),
           ('Why do passengers lurch forwards when a bus brakes suddenly?', 'Their bodies tend to keep moving at the original velocity (inertia)', ['A forward force pushes them', 'The bus pushes them forward', 'Gravity increases'], 'Newton’s first law.'),
           ('A spacecraft far from any planet switches off its engine. What happens?', 'It keeps moving at constant velocity', ['It slows down and stops', 'It falls', 'It speeds up'], 'No resultant force → no change in velocity.')],
    why=[('Explain why a seat belt reduces injury in a crash, using Newton’s first law.', 'When the car stops suddenly, the passenger keeps moving forwards (inertia); the seat belt provides the force to decelerate the passenger with the car, over a longer time and distance, rather than the passenger hitting the dashboard.'),
         ('Explain why a fully loaded lorry accelerates more slowly than an empty one with the same driving force.', 'a = F/m; the same resultant force acting on a larger mass produces a smaller acceleration.'),
         ('Explain why a rocket’s acceleration increases as it burns fuel, even with constant thrust.', 'Its mass decreases as fuel is used; with the same resultant force, a = F/m increases (and weight also falls).')],
    contrast=[('Newton’s first law', 'Newton’s second law', 'The first law says no resultant force means no change in velocity; the second law quantifies what happens when there is a resultant force: F = ma.'),
              ('inertia', 'momentum', 'Inertia is the tendency to resist change in motion, depending on mass; momentum is mass × velocity, a vector that depends on how fast the object moves.')],
    misc=[('A heavier object always falls faster than a light one.', 'Without air resistance all objects fall with the same acceleration g, because a larger weight acts on a proportionally larger mass (a = W/m = g).'),
          ('A force is needed to keep an object moving at constant speed.', 'A resultant force is needed only to change velocity; at constant speed forces are balanced (driving force equals resistance).')],
    cases=[('David Scott’s hammer and feather drop on the Moon (Apollo 15, 1971)', 'He dropped a 1.32 kg hammer and a 30 g falcon feather together; they hit the ground at the same moment.', 'Newton’s second law and free fall', 'With no air, the only force is weight; a = W/m = g for both, so they accelerate equally.'),
           ('crash-test dummies in car safety testing', 'Cars are crashed at 64 km/h into barriers; sensors in dummies record the forces on the head and chest.', 'Newton’s first and second laws', 'The dummy keeps moving (first law) until a force stops it; airbags and crumple zones lengthen the stopping time, reducing deceleration and so the force (F = ma).')],
    evaluate=[('Newton’s laws explain all motion we observe.', ['accurately predict motion from cars to planets', 'used to design vehicles, bridges and spacecraft'], ['fail near the speed of light (relativity)', 'do not apply to atoms and electrons (quantum mechanics)', 'GPS satellites need relativistic corrections'], 'Newton’s laws are excellent for everyday speeds and sizes but are approximations of more general theories.')],
))


@R.add('ch09-st2', 'C3', (1, 5), 'numerical')
def fma(rng, slot):
    k = rng.choice(['F', 'a', 'm', 'net', 'lift'] if slot.d >= 3 else ['F', 'a', 'm'])
    obj, m = rng.choice([('a 0.15 kg cricket ball', 0.15), ('a 1200 kg car', 1200), ('a 60 kg sprinter', 60), ('a 2.5 kg trolley', 2.5), ('a 75 kg cyclist and bike', 75), ('a 40 000 kg truck', 40000), ('a 0.45 kg football', 0.45)])
    if k == 'F':
        a = rng.choice([0.5, 1.2, 2.0, 3.5, 4.0, 8.0])
        return dict(stem=f'Calculate the resultant force needed to give {obj} an acceleration of {a} m/s².', answer=f'{m * a:.4g} N', markingKey=f'M1 F = ma = {m} × {a}; A1 {m * a:.4g} N.', marks=2)
    if k == 'a':
        F_ = round(m * rng.choice([0.8, 1.5, 2.4, 3.0, 5.0]), 2)
        return dict(stem=f'A resultant force of {F_:g} N acts on {obj}. Calculate its acceleration.', answer=f'{F_ / m:.3g} m/s²', markingKey=f'M1 a = F/m = {F_:g}/{m}; A1 {F_ / m:.3g} m/s².', marks=2)
    if k == 'm':
        F_ = rng.choice([120, 300, 450, 900, 2400])
        a = rng.choice([1.5, 2.0, 3.0, 4.0, 6.0])
        return dict(stem=f'A resultant force of {F_} N gives an object an acceleration of {a} m/s². Calculate the mass of the object.', answer=f'{F_ / a:.4g} kg', markingKey=f'M1 m = F/a = {F_}/{a}; A1 {F_ / a:.4g} kg.', marks=2)
    if k == 'net':
        drive = rng.choice([1500, 2000, 2800, 3500])
        res = rng.choice([400, 600, 900, 1200])
        mm = rng.choice([900, 1100, 1400, 1600])
        a = (drive - res) / mm
        return dict(stem=f'A car of mass {mm} kg has a driving force of {drive} N and resistive forces totalling {res} N. Calculate its acceleration, and the acceleration if the resistive forces doubled at higher speed.', answer=f'{a:.3g} m/s²; {(drive - 2 * res) / mm:.3g} m/s²',
                    markingKey=f'M1 resultant = {drive} − {res} = {drive - res} N; A1 a = {a:.3g} m/s²; A1 ({drive} − {2 * res})/{mm} = {(drive - 2 * res) / mm:.3g} m/s².', marks=3)
    mm = rng.choice([500, 650, 800, 1000])
    a = rng.choice([0.5, 1.0, 1.5, 2.0])
    T = mm * (9.8 + a)
    return dict(stem=f'A lift and its passengers have a total mass of {mm} kg. Calculate the tension in the cable when the lift accelerates upwards at {a} m/s² (g = 9.8 N/kg).', answer=f'{T:.4g} N',
                markingKey=f'M1 resultant = T − mg = ma; M1 T = {mm} × (9.8 + {a}); A1 {T:.4g} N.', marks=3)


dataset('ch09-st2',
        dict(intro='{who} pulled a 1.0 kg trolley with different constant forces and measured its acceleration with light gates.', iv=('Resultant force', 'N'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Acceleration', 'm/s²'), f=lambda x: x / 1.0, dp=2, trend='Acceleration increases in direct proportion to the resultant force.',
             why='Newton’s second law: a = F/m; with the mass constant the graph of a against F is a straight line through the origin with gradient 1/m.'),
        dict(intro='{who} pulled trolleys of different masses with a constant 2.0 N resultant force and measured the acceleration with light gates.', iv=('Mass', 'kg'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Acceleration', 'm/s²'), f=lambda x: 2.0 / x, dp=2, trend='Acceleration decreases as mass increases – doubling the mass halves the acceleration.',
             why='a = F/m: acceleration is inversely proportional to mass for a constant resultant force.'))

inquiry('ch09-st2',
        dict(ctx='how the resultant force on a trolley affects its acceleration (Newton’s second law)',
             iv='resultant force – weight of hanging masses on a string over a pulley (0.2 to 1.0 N)', dv='acceleration – from light gates and a data logger (m/s²)',
             cvs=[('total mass of the system (move masses from trolley to hanger)', 'a = F/m, so mass must be constant'), ('friction compensated by slightly tilting the runway', 'friction would reduce the resultant force'), ('distance between light gates', 'affects timing'), ('the same trolley', 'friction and mass differ')],
             hyp='If the resultant force increases, then the acceleration will increase in direct proportion, because Newton’s second law states a = F/m with constant mass.',
             method='Tilt runway until the trolley rolls at constant speed (friction compensated); attach a string over a pulley to a hanger; keep five 20 g masses on the trolley and move them one at a time to the hanger (0.2-1.0 N); release from rest; record acceleration from two light gates; repeat 3 times; plot a against F.',
             weak=('masses were added to the hanger from the bench, so the total mass increased', 'transfer masses from the trolley to the hanger so the total accelerated mass stays constant'),
             safety='place a cushion where the masses land; keep feet clear'))

R.facts('ch09-st3', F(
    terms=[('Newton’s third law', 'when two objects interact, they exert equal and opposite forces on each other'),
           ('interaction pair', 'two forces of the same type and size acting in opposite directions on two different objects'),
           ('thrust', 'the forward force produced when an engine pushes gas or water backwards')],
    facts=[('A swimmer pushes backwards on the water. What is the third-law pair?', 'The water pushes the swimmer forwards', ['The swimmer’s weight', 'Water resistance on the swimmer', 'The swimmer pushes forwards on the water'], 'Equal and opposite forces on different objects.'),
           ('The Earth pulls a falling apple down with 1 N. What force does the apple exert on the Earth?', '1 N upwards', ['0 N', '1 N downwards', 'A tiny force much less than 1 N'], 'The forces in a pair are equal in size.'),
           ('Which pair of forces is NOT a Newton’s third law pair?', 'The weight of a book and the normal force from the table on the book', ['Earth pulls book, book pulls Earth', 'Book pushes table down, table pushes book up', 'Rocket pushes gas back, gas pushes rocket forward'], 'Weight and normal force both act on the book and are different types.')],
    why=[('Explain why third-law forces never cancel each other.', 'They act on different objects, so each affects the motion of a different object; forces only cancel when they act on the same object.'),
         ('Explain how a rocket can accelerate in space where there is no air to push against.', 'The rocket pushes exhaust gases backwards at high speed; by Newton’s third law the gases push the rocket forwards with an equal force.'),
         ('Explain why the Earth does not noticeably accelerate towards a falling ball, even though the forces are equal.', 'a = F/m; the Earth’s mass is about 6 × 10²⁴ kg, so the same force produces a negligibly small acceleration.')],
    contrast=[('a Newton’s third law pair', 'balanced forces on one object', 'A third-law pair acts on two different objects and are the same type; balanced forces act on the same object and can be different types (e.g. weight and normal force).')],
    misc=[('When a horse pulls a cart, the cart pulls back equally, so they cannot move.', 'The pair acts on different objects; the horse moves forward because the ground pushes it forwards more than the cart pulls back on it.'),
          ('In a collision between a truck and a small car, the truck exerts a bigger force on the car.', 'The forces are equal and opposite; the car has a smaller mass so its acceleration (and damage) is greater.')],
    cases=[('SpaceX Falcon 9 launches', 'The engines expel hot gases downwards at around 3 km/s, producing over 7 MN of thrust.', 'Newton’s third law', 'The rocket pushes gas downwards, so the gas pushes the rocket upwards with an equal force.'),
           ('recoil of a fire hose', 'Firefighters must brace themselves because a high-pressure hose pushes back on them.', 'interaction pairs', 'The hose pushes water forwards; the water pushes the hose (and firefighter) backwards.')],
    evaluate=[('Newton’s third law means it is impossible to win a tug-of-war.', ['the rope tension pulls both teams equally'], ['the team that pushes harder on the ground gets a larger forward friction force from the ground', 'the resultant force on each team depends on ground friction minus rope tension'], 'The third law does not prevent winning; the winner pushes harder against the ground.')],
    extended=[('A skater of mass 60 kg pushes a friend of mass 40 kg on ice with a force of 120 N for 0.5 s. (a) State the force on the skater and its direction. (b) Calculate the acceleration of each. (c) Explain why they move apart with different speeds.', '(a) 120 N in the opposite direction (third law). (b) skater 120/60 = 2 m/s²; friend 120/40 = 3 m/s². (c) Equal forces act for the same time but on different masses, so the lighter friend accelerates more and moves faster (1.5 m/s vs 1.0 m/s).', 6),
              ('Identify all the third-law pairs involving a person standing still on the floor, and explain why the person does not accelerate.', 'Earth pulls person down (weight) – person pulls Earth up; person pushes floor down – floor pushes person up. The two forces ON the person (weight and normal force) are balanced, so no acceleration.', 4)],
))


@R.add('ch09-st3', 'C3', (1, 5), 'numerical')
def recoil(rng, slot):
    a, b = two_names(rng)
    ma, mb = rng.choice([40, 45, 50, 55, 60]), rng.choice([60, 65, 70, 80, 90])
    F_ = rng.choice([60, 90, 120, 150, 180])
    t = rng.choice([0.4, 0.5, 0.6, 0.8])
    if slot.d <= 2:
        return dict(stem=f'{a} ({ma} kg) and {b} ({mb} kg) stand on skateboards and push each other apart. {a} pushes {b} with {F_} N. State the force on {a} and calculate the acceleration of each.', answer=f'{F_} N on {a} (opposite direction); {a} {F_ / ma:.3g} m/s², {b} {F_ / mb:.3g} m/s²',
                    markingKey=f'1 {F_} N, opposite direction (third law); 1 {F_}/{ma} = {F_ / ma:.3g} m/s²; 1 {F_}/{mb} = {F_ / mb:.3g} m/s².', marks=3)
    va, vb = F_ / ma * t, F_ / mb * t
    return dict(stem=f'On ice, {a} ({ma} kg) pushes {b} ({mb} kg) with a force of {F_} N for {t} s. Calculate the speed of each after the push and show that their momenta are equal and opposite.',
                answer=f'{a} {va:.3g} m/s; {b} {vb:.3g} m/s; momenta {ma * va:.3g} kg m/s each, opposite directions', markingKey=f'M1 a = F/m for each; M1 v = at; A1 {va:.3g} and {vb:.3g} m/s; A1 p = {ma * va:.3g} kg m/s for both (F × t the same).', marks=4)


inquiry('ch09-st3',
        dict(ctx='how the volume of water in a bottle rocket affects the height it reaches',
             iv='volume of water in a 2 dm³ bottle (200, 400, 600, 800, 1000 cm³)', dv='maximum height – found by measuring the angle of elevation from a fixed distance and using trigonometry (or video analysis)',
             cvs=[('air pressure at launch (e.g. 4 bar on the pump gauge)', 'more pressure gives more thrust'), ('the same bottle, fins and nose cone', 'mass and drag change height'), ('launch angle (vertical)', 'an angle reduces height'), ('wind conditions', 'wind affects the path')],
             hyp='If the volume of water increases, then the height will increase up to an optimum (about one-third full) and then decrease, because more water gives more mass pushed out backwards (more thrust by Newton’s third law), but too much water leaves less space for compressed air and adds mass.',
             method='Fill the bottle with a measured volume of water; attach to launcher; pump to 4 bar; launch vertically; a partner 20 m away measures angle of elevation at the peak; calculate height = 20 × tan θ; three launches per volume; calculate means.',
             weak=('the pump was stopped at different pressures each time', 'use the pressure gauge and launch at exactly 4 bar every time'),
             safety='stand at least 5 m away; wear eye protection; never stand over the launcher'))

R.facts('ch09-st4', F(
    terms=[('friction', 'a force that opposes the relative motion (or attempted motion) of two surfaces in contact'),
           ('air resistance (drag)', 'the frictional force on an object moving through air, which increases with speed'),
           ('terminal velocity', 'the constant maximum velocity reached by a falling object when air resistance equals weight, so the resultant force is zero'),
           ('streamlining', 'shaping an object so that air or water flows smoothly around it, reducing drag')],
    facts=[('What is the resultant force on a skydiver at terminal velocity?', 'Zero', ['Equal to her weight', 'Equal to air resistance', 'Upwards'], 'Weight and drag are balanced.'),
           ('How does opening a parachute change the motion of a skydiver at terminal velocity?', 'Air resistance increases, so she decelerates to a lower terminal velocity', ['She accelerates upwards and rises', 'Her weight decreases', 'Nothing changes'], 'Larger area → larger drag.'),
           ('Which change increases the air resistance on a cyclist?', 'Sitting upright instead of crouching', ['Wearing a tight-fitting suit', 'Using a streamlined helmet', 'Riding more slowly'], 'Larger frontal area increases drag.'),
           ('Which is a useful effect of friction?', 'Grip between tyres and the road', ['Wear on engine parts', 'Heating of machinery', 'Slowing a rocket'], 'Friction lets wheels push on the road.')],
    why=[('Explain why a skydiver reaches a terminal velocity.', 'At first weight is greater than air resistance, so she accelerates; as speed increases, air resistance increases until it equals her weight; the resultant force is then zero, so velocity is constant.'),
         ('Explain why a car has a maximum speed even with the accelerator pressed fully.', 'Air resistance increases with speed until resistive forces equal the maximum driving force; the resultant force becomes zero and the car cannot accelerate further.'),
         ('Explain why lubricating moving parts of a machine improves efficiency.', 'Oil reduces friction between surfaces, so less energy is wasted as heat and less wear occurs.')],
    contrast=[('friction between solid surfaces', 'air resistance', 'Solid friction acts between surfaces in contact and is roughly independent of speed; air resistance acts on objects moving through air and increases rapidly with speed.')],
    misc=[('When a parachute opens, the skydiver moves upwards.', 'She still moves downwards but decelerates, because air resistance briefly exceeds her weight.'),
          ('At terminal velocity there are no forces acting on the falling object.', 'Weight and air resistance still act; they are equal and opposite, so the resultant is zero.')],
    cases=[('Felix Baumgartner’s Red Bull Stratos jump (2012)', 'Jumping from 39 km, he reached about 1358 km/h in the thin upper atmosphere before slowing to a lower terminal velocity as the air became denser.', 'terminal velocity and air resistance', 'In thin air drag is small, so terminal velocity is very high; denser air lower down increased drag, lowering his terminal velocity.'),
           ('Formula 1 car aerodynamics', 'Wings and the car floor create downforce, pushing tyres onto the track for more grip, but also add drag.', 'friction and air resistance', 'More downforce increases friction between tyres and track for cornering, while drag limits top speed – engineers balance the two.')],
    evaluate=[('Reducing friction is always desirable in engineering.', ['less energy wasted, higher efficiency', 'less wear on parts'], ['friction is essential for brakes, tyres, walking and holding objects', 'low friction roads are dangerous in rain or ice'], 'Friction should be reduced where it wastes energy but increased where grip and braking are needed.')],
    extended=[('Describe and explain the motion of a skydiver from leaving the plane to landing, with reference to the forces acting and a sketch velocity–time graph.', '1: weight > drag, accelerates (steep start, gradient ~ 9.8 m/s²). 2: speed increases, drag increases, acceleration decreases (curve flattens). 3: drag = weight, terminal velocity (~55 m/s). 4: parachute opens, drag > weight, decelerates. 5: drag decreases with speed until equal to weight, new lower terminal velocity (~5 m/s). 6: lands.', 6, 'long')],
))


@R.add('ch09-st4', 'C3', (1, 5), 'numerical')
def falling_forces(rng, slot):
    m = rng.choice([60, 70, 75, 80, 90])
    W = m * 9.8
    k = rng.choice(['term', 'accel', 'para'] if slot.d >= 3 else ['term', 'accel'])
    if k == 'term':
        return dict(stem=f'A skydiver of mass {m} kg falls at terminal velocity. Calculate the air resistance acting on her (g = 9.8 N/kg) and explain your answer.', answer=f'{W:.0f} N',
                    markingKey=f'1 at terminal velocity the resultant force is zero; M1 drag = weight = {m} × 9.8; A1 {W:.0f} N.', marks=3)
    if k == 'accel':
        D = rng.choice([200, 300, 400, 500])
        a = (W - D) / m
        return dict(stem=f'A {m} kg skydiver is falling; air resistance on her is {D} N. Calculate her acceleration at that moment (g = 9.8 N/kg).', answer=f'{a:.3g} m/s² downwards',
                    markingKey=f'M1 W = {W:.0f} N; M1 resultant = {W:.0f} − {D} = {W - D:.0f} N; A1 a = {a:.3g} m/s².', marks=3)
    D = rng.choice([1500, 2000, 2500])
    a = (D - W) / m
    return dict(stem=f'When a {m} kg parachutist opens her parachute, the air resistance suddenly becomes {D} N. Calculate her deceleration and describe what happens to her velocity afterwards.', answer=f'{a:.3g} m/s² (upward resultant); she slows until drag falls to {W:.0f} N, then falls at a new, lower terminal velocity',
                markingKey=f'M1 resultant = {D} − {W:.0f} = {D - W:.0f} N upwards; A1 {a:.3g} m/s²; 1 drag decreases as speed falls until it equals weight → lower terminal velocity.', marks=3)


dataset('ch09-st4',
        dict(intro='{who} dropped cupcake cases from 2.0 m and measured the terminal velocity reached for different numbers of stacked cases (more cases = more weight, same shape).', iv=('Number of cases', ''), xs=[1, 2, 3, 4, 5],
             dv=('Terminal velocity', 'm/s'), f=lambda x: 0.9 * math.sqrt(x), dp=2, trend='Terminal velocity increases as the number of cases increases, but not proportionally (about √n).',
             why='More cases give more weight but the same shape; a higher speed is needed for air resistance (which increases with speed²) to balance the larger weight.'))

inquiry('ch09-st4',
        dict(ctx='how the surface area of a paper parachute affects the time it takes to fall 2.0 m',
             iv='surface area of the canopy (cm², e.g. squares of side 10, 15, 20, 25, 30 cm)', dv='time to fall 2.0 m, measured with a stopwatch or from video',
             cvs=[('mass of the load (e.g. one plasticine ball of 5 g)', 'weight affects terminal velocity'), ('drop height (2.0 m)', 'longer falls take longer'), ('string length and material of canopy', 'affect shape and mass'), ('draughts (doors and windows closed)', 'air movement changes the fall')],
             hyp='If the surface area increases, then the fall time will increase, because a larger area gives more air resistance at a given speed, so the terminal velocity is lower.',
             method='Make five canopies of different areas from the same paper with 20 cm strings and 5 g load; drop each from 2.0 m (measured with metre rule) in a draught-free room; time the fall with a video at 60 fps; repeat 5 times; calculate mean times; plot time against area.',
             weak=('the parachutes were thrown downwards rather than released', 'release each parachute from rest, already opened, at the same height'),
             safety='use a stable step stool, not a chair'))

R.facts('ch09-st5', F(
    terms=[('momentum', 'the product of mass and velocity, p = m × v, measured in kg m/s; a vector'),
           ('conservation of momentum', 'in a closed system the total momentum before an event equals the total momentum after it'),
           ('thinking distance', 'the distance travelled during the driver’s reaction time before the brakes are applied'),
           ('braking distance', 'the distance travelled while the brakes are applied until the vehicle stops'),
           ('stopping distance', 'thinking distance + braking distance')],
    facts=[('What is the momentum of a 1000 kg car moving at 20 m/s?', '20 000 kg m/s', ['50 kg m/s', '2000 kg m/s', '200 000 kg m/s'], 'p = mv.'),
           ('Which factor increases thinking distance?', 'Drinking alcohol', ['Worn tyres', 'Wet roads', 'Worn brakes'], 'Alcohol increases reaction time; the others affect braking distance.'),
           ('Which factor increases braking distance?', 'An icy road', ['Tiredness', 'Using a mobile phone', 'Distraction'], 'Less friction between tyres and road.'),
           ('How do crumple zones reduce injuries in a crash?', 'They increase the time taken for the car to stop, reducing the force', ['They increase the speed of the car', 'They make the car heavier', 'They stop the car instantly'], 'F = change in momentum ÷ time.')],
    why=[('Explain why airbags reduce injuries in a collision.', 'The airbag increases the time over which the passenger’s momentum is reduced to zero; since force = change in momentum ÷ time, the force on the passenger is smaller.'),
         ('Explain why stopping distance increases more than in proportion to speed.', 'Thinking distance is proportional to speed, but braking distance is proportional to speed squared (braking work = kinetic energy = ½mv²), so stopping distance rises rapidly at higher speeds.'),
         ('Explain why using a mobile phone while driving increases stopping distance.', 'Distraction increases reaction time, so the car travels further at full speed before braking begins (larger thinking distance).')],
    contrast=[('thinking distance', 'braking distance', 'Thinking distance depends on speed and reaction time (driver factors: tiredness, alcohol, distraction); braking distance depends on speed and road/vehicle conditions (brakes, tyres, ice, mass).'),
              ('momentum', 'kinetic energy', 'Momentum is mv (vector, kg m/s) and is always conserved in collisions; kinetic energy is ½mv² (scalar, J) and is often partly transferred to heat and sound.')],
    misc=[('A heavy truck and a car at the same speed have the same momentum.', 'Momentum depends on mass: the truck has much more momentum and needs a larger force or longer time to stop.'),
          ('Braking distance doubles when speed doubles.', 'Braking distance is proportional to v², so it increases four times.')],
    cases=[('the introduction of compulsory seat belts in Victoria, Australia (1970, the world’s first)', 'Road deaths in Victoria fell by around 18% in the following year.', 'momentum and the forces in collisions', 'Belts stretch slightly, increasing the time to reduce the passenger’s momentum, reducing force; they also stop the passenger hitting the windscreen.'),
           ('20 mph (32 km/h) zones in cities such as London and Paris', 'Studies found fewer and less severe casualties after limits were lowered from 30 mph to 20 mph.', 'stopping distances', 'Lower speed shortens thinking and braking distances, and a pedestrian is hit at a much lower speed, with far less kinetic energy.')],
    evaluate=[('Lowering urban speed limits to 30 km/h is the best way to improve road safety.', ['stopping distance much shorter, fewer collisions', 'pedestrian fatality risk falls sharply at lower impact speeds', 'less noise and pollution'], ['longer journey times and possible driver frustration', 'enforcement is difficult', 'education, road design and vehicle safety also matter'], 'It is one of the most effective measures, especially near schools, but works best combined with road design and enforcement.')],
))


@R.add('ch09-st5', 'C3', (1, 5), 'numerical')
def momentum(rng, slot):
    k = rng.choice(['p', 'stop', 'force', 'collide', 'ke'] if slot.d >= 3 else ['p', 'stop', 'ke'])
    if k == 'p':
        obj, m = rng.choice([('a 0.16 kg hockey ball', 0.16), ('a 70 kg rugby player', 70), ('a 1500 kg car', 1500), ('a 0.058 kg tennis ball', 0.058), ('a 9000 kg bus', 9000)])
        v = rng.choice([4, 8, 12, 15, 25, 30])
        return dict(stem=f'Calculate the momentum of {obj} moving at {v} m/s.', answer=f'{m * v:.4g} kg m/s', markingKey=f'M1 p = mv = {m} × {v}; A1 {m * v:.4g} kg m/s.', marks=2)
    if k == 'ke':
        m = rng.choice([800, 1000, 1200, 1500])
        v = rng.choice([10, 13, 20, 25, 30])
        ke = 0.5 * m * v * v
        F_ = rng.choice([6000, 8000, 10000])
        return dict(stem=f'A {m} kg car is travelling at {v} m/s. (a) Calculate its kinetic energy. (b) The brakes provide a constant braking force of {F_} N. Use work done = force × distance to calculate the braking distance.', answer=f'(a) {ke:.4g} J (b) {ke / F_:.3g} m',
                    markingKey=f'(a) M1 ½ × {m} × {v}²; A1 {ke:.4g} J. (b) M1 work done by brakes = KE; A1 d = {ke:.4g}/{F_} = {ke / F_:.3g} m.', marks=4)
    if k == 'stop':
        v = rng.choice([13, 18, 22, 27, 31])
        rt = rng.choice([0.6, 0.7, 0.9, 1.2, 1.5])
        b = round(v * v / (2 * 7.0), 1)
        return dict(stem=f'A driver travelling at {v} m/s has a reaction time of {rt} s. The braking distance at this speed is {b} m. Calculate the thinking distance and the total stopping distance.', answer=f'thinking {v * rt:.3g} m; stopping {v * rt + b:.3g} m',
                    markingKey=f'M1 thinking = speed × reaction time = {v} × {rt}; A1 {v * rt:.3g} m; A1 stopping = {v * rt:.3g} + {b} = {v * rt + b:.3g} m.', marks=3)
    if k == 'force':
        m = rng.choice([60, 70, 80])
        v = rng.choice([10, 13, 15, 20])
        t1, t2 = rng.choice([0.01, 0.02]), rng.choice([0.1, 0.15, 0.2])
        return dict(stem=f'In a crash a {m} kg passenger moving at {v} m/s is brought to rest. Calculate the average force on the passenger if she stops in (a) {t1} s by hitting the dashboard and (b) {t2} s with an airbag. Explain the difference.',
                    answer=f'(a) {m * v / t1:.4g} N (b) {m * v / t2:.4g} N; the airbag increases the stopping time, so the force is smaller',
                    markingKey=f'M1 Δp = {m} × {v} = {m * v} kg m/s; A1 {m * v / t1:.4g} N; A1 {m * v / t2:.4g} N; 1 F = Δp/t, longer t gives smaller F.', marks=4)
    m1, v1, m2 = rng.choice([1000, 1200, 1500]), rng.choice([10, 15, 20]), rng.choice([800, 1000, 1200])
    v = m1 * v1 / (m1 + m2)
    return dict(stem=f'A {m1} kg car moving at {v1} m/s crashes into a stationary {m2} kg car and they move off together. Use conservation of momentum to find their velocity just after the collision.', answer=f'{v:.3g} m/s',
                markingKey=f'M1 momentum before = {m1} × {v1} = {m1 * v1} kg m/s; M1 = ({m1} + {m2}) × v; A1 {v:.3g} m/s.', marks=3)


dataset('ch09-st5',
        dict(intro='Road-safety data used by {who} show the braking distance of a typical car on a dry road at different speeds (three tests per speed).', iv=('Speed', 'm/s'), xs=[9, 13, 18, 22, 27],
             dv=('Braking distance', 'm'), f=lambda x: x * x / 13.5, dp=1, trend='Braking distance increases more and more steeply with speed; doubling the speed roughly quadruples the braking distance.',
             why='The brakes must transfer all the kinetic energy (½mv²); with a constant braking force, distance = KE ÷ force, so braking distance ∝ v².'))

inquiry('ch09-st5',
        dict(ctx='how the speed of a trolley affects its stopping distance when it runs onto a rough carpet (modelling braking distance)',
             iv='speed of the trolley when it reaches the carpet (set by release height on a ramp and measured with a light gate)', dv='stopping distance on the carpet measured with a metre rule',
             cvs=[('mass of trolley', 'more mass gives more kinetic energy'), ('type of carpet', 'friction force depends on the surface'), ('the same trolley wheels', 'friction differs'), ('release from rest each time', 'speed must depend only on height')],
             hyp='If the speed doubles, then the stopping distance will roughly quadruple, because kinetic energy ∝ v² and the friction force (doing work to stop the trolley) is constant.',
             method='Set ramp at a fixed angle; release trolley from 5 heights; light gate at bottom measures speed; trolley runs onto a 2 m strip of carpet; measure stopping distance; 3 repeats per height; plot stopping distance against speed² to test proportionality.',
             weak=('the carpet strip was rucked up in places', 'tape the carpet flat so the friction force is the same along its length'),
             safety='keep the run-off area clear and stop the trolley safely at the end'))


# =============================================================================================
# ch10 Waves: Properties and the Electromagnetic Spectrum
# =============================================================================================
R.facts('ch10-st1', F(
    terms=[('wave', 'a disturbance that transfers energy (and information) from one place to another without transferring matter'),
           ('transverse wave', 'a wave in which the oscillations are perpendicular (at right angles) to the direction of energy transfer, e.g. light, water ripples'),
           ('longitudinal wave', 'a wave in which the oscillations are parallel to the direction of energy transfer, e.g. sound'),
           ('compression', 'a region of a longitudinal wave where the particles are closer together than normal'),
           ('rarefaction', 'a region of a longitudinal wave where the particles are further apart than normal'),
           ('medium', 'the substance through which a mechanical wave travels')],
    facts=[('Which of these is a longitudinal wave?', 'Sound in air', ['Light', 'Microwaves', 'Ripples on a pond'], 'Air particles oscillate back and forth along the direction of travel.'),
           ('What do all waves transfer?', 'Energy', ['Matter', 'Particles of the medium', 'Mass'], 'The medium oscillates about fixed positions.'),
           ('Which type of wave can travel through a vacuum?', 'Electromagnetic waves', ['Sound waves', 'Water waves', 'Seismic waves'], 'EM waves do not need a medium.'),
           ('Which seismic waves are transverse and cannot pass through the Earth’s liquid outer core?', 'S-waves', ['P-waves', 'Sound waves', 'Surface water waves'], 'Transverse waves cannot travel through liquids.')],
    why=[('Explain why sound cannot travel through space.', 'Sound is a mechanical longitudinal wave that needs particles to vibrate and pass on energy; space is a vacuum with almost no particles.'),
         ('Explain why a cork floating on a pond bobs up and down but does not travel with the ripples.', 'Water waves transfer energy, not matter; water particles (and the cork) oscillate about a fixed position as the wave passes.'),
         ('Explain how seismic waves provide evidence that the Earth has a liquid outer core.', 'S-waves are transverse and cannot travel through liquids; they are not detected in a “shadow zone” on the far side of the Earth from an earthquake, so part of the core must be liquid.')],
    contrast=[('a transverse wave', 'a longitudinal wave', 'In a transverse wave oscillations are perpendicular to the direction of energy transfer (peaks and troughs); in a longitudinal wave oscillations are parallel (compressions and rarefactions).'),
              ('a compression', 'a rarefaction', 'A compression is where particles are squeezed close together (higher pressure); a rarefaction is where they are spread apart (lower pressure).')],
    misc=[('In a sound wave, air molecules travel from the speaker to your ear.', 'Air molecules vibrate back and forth about fixed positions, passing energy along; they do not travel across the room.'),
          ('Light is a longitudinal wave because it travels in straight lines.', 'Light is transverse: its electric and magnetic fields oscillate at right angles to the direction of travel.')],
    cases=[('the 2004 Indian Ocean tsunami', 'An undersea earthquake off Sumatra sent waves across the ocean at around 700 km/h; they reached Sri Lanka about 2 hours later.', 'waves transferring energy, not water', 'In deep ocean the water mostly oscillated with small height while energy travelled vast distances; in shallow coastal water the energy produced huge waves.'),
           ('a “Mexican wave” in a football stadium', 'Spectators stand up and sit down in turn and the wave travels around the stadium.', 'transverse waves', 'Each person moves up and down (perpendicular to the direction the wave travels) without moving around the stadium.')],
    evaluate=[('Earthquake early-warning systems using P-waves are worth the cost.', ['P-waves arrive before damaging S-waves, giving seconds of warning (e.g. Japan, Mexico)', 'trains can be stopped and gas supplies shut off automatically'], ['warning time is very short near the epicentre', 'false alarms reduce trust', 'expensive networks of seismometers'], 'For earthquake-prone cities the benefits in lives saved outweigh the costs, though they complement rather than replace strong building codes.')],
    extended=[('Use a slinky spring to describe how you would demonstrate both a transverse and a longitudinal wave, and explain how each demonstration shows that energy, not matter, is transferred.', 'Transverse: move one end side to side – coils move perpendicular to the wave direction; longitudinal: push and pull the end along the spring – compressions and rarefactions travel along. Tie a ribbon to one coil: it oscillates about a fixed point and does not travel along, while energy reaches the far end.', 5),
              ('Seismometers 5000 km and 9000 km from an earthquake recorded P-waves (8 km/s) and S-waves (4.5 km/s). Calculate the time between the P- and S-wave arrivals at each station and explain how this difference allows scientists to locate an earthquake.', '5000 km: 625 s vs 1111 s, gap 486 s. 9000 km: 1125 s vs 2000 s, gap 875 s. The gap increases with distance, so each station’s gap gives its distance; circles from three stations intersect at the epicentre.', 6)],
))


@R.add('ch10-st1', 'C3', (1, 5), 'numerical')
def seismic(rng, slot):
    d = rng.choice([800, 1200, 2000, 3500, 4800, 6000])
    vp, vs = rng.choice([(8.0, 4.5), (7.5, 4.2), (6.0, 3.5)])
    tp, ts = d / vp, d / vs
    if slot.d <= 2:
        return dict(stem=f'P-waves from an earthquake travel at {vp} km/s. How long do they take to reach a seismometer {d} km away?', answer=f'{tp:.3g} s',
                    markingKey=f'M1 t = d ÷ v = {d}/{vp}; A1 {tp:.3g} s.', marks=2)
    return dict(stem=f'An earthquake is {d} km from a seismic station. P-waves travel at {vp} km/s and S-waves at {vs} km/s. Calculate the time delay between the arrival of the P-waves and the S-waves, and state which type is longitudinal.',
                answer=f'{ts - tp:.3g} s; P-waves are longitudinal', markingKey=f'M1 tP = {tp:.3g} s; M1 tS = {ts:.3g} s; A1 delay {ts - tp:.3g} s; 1 P-waves longitudinal.', marks=4)


inquiry('ch10-st1',
        dict(ctx='how the tension in a stretched slinky spring affects the speed of a longitudinal pulse along it',
             iv='tension – the length the slinky is stretched to (2, 3, 4, 5, 6 m)', dv='speed of a pulse = distance travelled ÷ time, timed with video analysis over several reflections',
             cvs=[('the same slinky', 'different springs have different mass and stiffness'), ('size of the pulse', 'very large pulses may behave differently'), ('surface (smooth floor)', 'friction damps the pulse'), ('measuring distance', 'must be the same length the pulse travels')],
             hyp='If the slinky is stretched further, then the pulse will travel faster, because higher tension means the coils are pulled back more strongly and pass the disturbance on more quickly.',
             method='Lay the slinky on a smooth floor; fix one end; stretch to 2 m; create a single compression by pushing the free end; film at 60 fps alongside a metre rule; time the pulse travelling to the end and back three times; speed = total distance ÷ time; repeat for 3-6 m.',
             weak=('the pulse was timed over one length with a stopwatch', 'time several reflections or use video frame-counting to reduce timing uncertainty'),
             safety='do not let go of a stretched slinky – it can snap back'))

R.facts('ch10-st2', F(
    terms=[('amplitude', 'the maximum displacement of a point on a wave from its rest (equilibrium) position'),
           ('wavelength (λ)', 'the distance from one point on a wave to the equivalent point on the next wave, e.g. crest to crest'),
           ('frequency (f)', 'the number of waves passing a point each second, measured in hertz (Hz)'),
           ('period (T)', 'the time taken for one complete wave to pass a point; T = 1/f'),
           ('wave speed', 'the distance travelled by a wave per second; v = f × λ')],
    facts=[('A wave has a frequency of 50 Hz and a wavelength of 4 m. What is its speed?', '200 m/s', ['12.5 m/s', '54 m/s', '0.08 m/s'], 'v = fλ = 50 × 4.'),
           ('A wave has a period of 0.02 s. What is its frequency?', '50 Hz', ['0.02 Hz', '20 Hz', '500 Hz'], 'f = 1/T.'),
           ('What is the unit of frequency?', 'Hertz (Hz)', ['Metres (m)', 'Seconds (s)', 'Decibels (dB)'], '1 Hz = one wave per second.'),
           ('On a displacement–distance graph of a wave, what is measured from the rest position to a crest?', 'Amplitude', ['Wavelength', 'Period', 'Frequency'], 'Amplitude is the maximum displacement.')],
    why=[('Explain why increasing the frequency of waves in a ripple tank decreases their wavelength.', 'The wave speed in water of a given depth is constant; since v = fλ, if f increases λ must decrease in proportion.'),
         ('Explain why amplitude does not appear in the wave equation v = fλ.', 'Wave speed depends on the medium, not on how much energy (amplitude) the wave carries; amplitude affects energy and loudness/brightness but not speed.'),
         ('Explain how the wave equation v = fλ can be derived.', 'In one period T the wave moves forward one wavelength λ, so speed = λ/T; since f = 1/T, v = fλ.')],
    contrast=[('wavelength', 'amplitude', 'Wavelength is the distance between equivalent points on adjacent waves (horizontal on a graph); amplitude is the maximum displacement from rest (vertical).'),
              ('frequency', 'period', 'Frequency is the number of waves per second (Hz); period is the time for one wave (s); f = 1/T.')],
    misc=[('Amplitude is the distance from a crest to a trough.', 'Amplitude is from the rest position to a crest (or trough) – half the crest-to-trough height.'),
          ('Waves with a higher frequency always travel faster.', 'In a given medium speed is fixed; higher frequency means shorter wavelength (v = fλ).')],
    evaluate=[('Ripple tanks are the best way to teach wave properties.', ['waves are visible and slow enough to measure', 'show reflection, refraction and diffraction clearly'], ['water depth must be kept even, which is hard', 'measurements from shadows are imprecise', 'water waves differ from sound and light in some ways'], 'Ripple tanks are an excellent model but should be combined with simulations and other wave types.')],
))


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def wave_eq(rng, slot):
    k = rng.choice(['v', 'f', 'lam', 'T', 'count', 'ripple'] if slot.d >= 3 else ['v', 'f', 'lam', 'T'])
    ctx = rng.choice([('a ripple-tank wave', 0.15, (2, 12), 'cm'), ('a sound wave in air', 340, (85, 3400), 'm'), ('a wave on a guitar string', 400, (82, 330), 'm'), ('a sound wave in water', 1500, (500, 5000), 'm'), ('an ocean swell', 12, (0.05, 0.12), 'm')])
    nm, v, (flo, fhi), _ = ctx
    if k == 'v':
        f = round(rng.uniform(flo, fhi), 2 if fhi < 1 else 0)
        lam = v / f * rng.uniform(0.95, 1.05)
        lam = round(lam, 3 if lam < 1 else 2 if lam < 10 else 1)
        return dict(stem=f'Calculate the speed of {nm} with frequency {f:g} Hz and wavelength {lam:g} m.', answer=f'{f * lam:.3g} m/s', markingKey=f'M1 v = fλ = {f:g} × {lam:g}; A1 {f * lam:.3g} m/s.', marks=2)
    if k == 'f':
        lam = round(v / rng.uniform(flo, fhi), 3)
        if lam == 0:
            return None
        return dict(stem=f'{nm[0].upper() + nm[1:]} travels at {v} m/s and has a wavelength of {lam:g} m. Calculate its frequency.', answer=f'{v / lam:.3g} Hz', markingKey=f'M1 f = v/λ = {v}/{lam:g}; A1 {v / lam:.3g} Hz.', marks=2)
    if k == 'lam':
        f = round(rng.uniform(flo, fhi), 2 if fhi < 1 else 0)
        return dict(stem=f'{nm[0].upper() + nm[1:]} has a frequency of {f:g} Hz and travels at {v} m/s. Calculate its wavelength.', answer=f'{v / f:.3g} m', markingKey=f'M1 λ = v/f = {v}/{f:g}; A1 {v / f:.3g} m.', marks=2)
    if k == 'T':
        T = rng.choice([0.002, 0.005, 0.01, 0.02, 0.04, 0.25, 2.0, 8.0])
        return dict(stem=f'A wave has a period of {T} s. Calculate its frequency and state how many waves pass a point in one minute.', answer=f'{1 / T:g} Hz; {60 / T:g} waves',
                    markingKey=f'M1 f = 1/T = 1/{T}; A1 {1 / T:g} Hz; A1 × 60 = {60 / T:g}.', marks=3)
    if k == 'count':
        n = rng.randint(8, 30)
        t = rng.choice([5, 10, 15, 20])
        lam = round(rng.uniform(1.5, 6.0), 1)
        f = n / t
        who = name(rng)
        return dict(stem=f'{who} counts {n} waves passing the end of a pier in {t} s. The distance between neighbouring crests is {lam} m. Calculate the frequency, the period and the speed of the waves.', answer=f'f = {f:.3g} Hz; T = {1 / f:.3g} s; v = {f * lam:.3g} m/s',
                    markingKey=f'1 f = {n}/{t} = {f:.3g} Hz; 1 T = 1/f = {1 / f:.3g} s; M1 v = fλ; A1 {f * lam:.3g} m/s.', marks=4)
    n = rng.choice([5, 6, 8, 10])
    L = round(rng.uniform(8, 20), 1)
    f = rng.choice([8, 10, 12, 15, 20])
    lam = L / n / 100
    return dict(stem=f'In a ripple tank, {n} complete wavelengths span {L} cm on the screen below. The vibrating bar has a frequency of {f} Hz. (Assume the shadow is the same size as the waves.) Calculate the wavelength in m and the wave speed.', answer=f'λ = {lam:.4f} m; v = {f * lam:.3g} m/s',
                markingKey=f'M1 λ = {L}/{n} = {L / n:.3g} cm = {lam:.4f} m; M1 v = fλ = {f} × {lam:.4f}; A1 {f * lam:.3g} m/s; 1 measuring many wavelengths reduces uncertainty.', marks=4)


@R.add('ch10-st2', 'C4', (3, 5), 'multi_step')
def wave_graph(rng, slot):
    A = rng.choice([2, 3, 4, 5])
    lam = rng.choice([0.4, 0.6, 0.8, 1.2])
    T = rng.choice([0.02, 0.05, 0.1, 0.2])
    v = lam / T
    return dict(stem=f'A displacement–distance graph of a wave shows crests {A} cm above the rest line and troughs {A} cm below, with crest-to-crest spacing {lam} m. A displacement–time graph for one point shows one complete oscillation every {T} s. (a) State the amplitude, wavelength and period. (b) Calculate the frequency and wave speed. (c) Describe how both graphs would change if the frequency were doubled in the same medium.',
                answer=f'(a) {A} cm, {lam} m, {T} s (b) f = {1 / T:g} Hz, v = {v:.3g} m/s (c) speed unchanged, so λ halves to {lam / 2:g} m (twice as many waves on the distance graph); period halves to {T / 2:g} s (twice as many oscillations on the time graph); amplitude unchanged unless energy changes',
                markingKey=f'(a) 1 amplitude {A} cm (not {2 * A}); 1 λ and T. (b) 1 f = 1/T = {1 / T:g} Hz; 1 v = fλ = {v:.3g} m/s. (c) 1 λ halves; 1 T halves, v constant.', marks=6, gap='G5')


dataset('ch10-st2',
        dict(intro='{who} changed the frequency of the vibrating bar in a ripple tank (constant depth) and measured the wavelength by measuring 10 waves on the screen.', iv=('Frequency', 'Hz'), xs=[5, 10, 15, 20, 25],
             dv=('Wavelength', 'cm'), f=lambda x: 24 / x, dp=2, trend='Wavelength decreases as frequency increases; frequency × wavelength stays approximately constant.',
             why='Wave speed depends on the water depth, which is constant, so v = fλ is constant and λ is inversely proportional to f.'))

inquiry('ch10-st2',
        dict(ctx='how the depth of water in a ripple tank affects the speed of water waves',
             iv='depth of water (0.5, 1.0, 1.5, 2.0, 2.5 cm, measured with a ruler at several points)', dv='wave speed = frequency (from the signal generator) × wavelength (from 10 wavelengths on the screen)',
             cvs=[('frequency of the vibrator', 'speed calculated using v = fλ needs a known f'), ('tank level (even depth)', 'uneven depth changes speed across the tank'), ('lamp height', 'changes the magnification of the shadow pattern'), ('water temperature', 'can change wave speed slightly')],
             hyp='If the water depth increases, then the wave speed will increase, because waves travel faster in deeper water (in shallow water v ≈ √(g × depth)).',
             method='Level the tank using a spirit level; fill to 0.5 cm; set the vibrator to 10 Hz; use a stroboscope or photo to freeze the pattern; measure across 10 wavelengths on the screen; correct for magnification using a ruler on the tank floor; calculate v = fλ; repeat three times; repeat for each depth.',
             weak=('the tank was not level, so the water was deeper at one end', 'level the tank with a spirit level and adjustable feet before each set of readings'),
             safety='mop spills immediately – water near mains lamps; use low-voltage lamp'))

R.facts('ch10-st3', F(
    terms=[('electromagnetic spectrum', 'the continuous range of electromagnetic waves arranged by wavelength or frequency: radio, microwave, infrared, visible, ultraviolet, X-ray, gamma'),
           ('ionising radiation', 'radiation with enough energy to remove electrons from atoms, e.g. UV, X-rays and gamma rays'),
           ('speed of light (c)', 'the speed of all electromagnetic waves in a vacuum, 3.0 × 10⁸ m/s'),
           ('infrared radiation', 'EM radiation with wavelengths longer than visible red light, emitted by warm objects')],
    facts=[('Which electromagnetic wave has the longest wavelength?', 'Radio waves', ['Gamma rays', 'Ultraviolet', 'Visible light'], 'Radio waves can be kilometres long.'),
           ('Which EM wave is used for airport security body scanners and to check luggage?', 'X-rays (and millimetre-wave microwaves for body scanners)', ['Radio waves only', 'Ultraviolet', 'Infrared only'], 'X-rays pass through soft materials but not dense metal.'),
           ('Which part of the EM spectrum can cause sunburn and skin cancer?', 'Ultraviolet', ['Infrared', 'Radio waves', 'Microwaves'], 'UV damages DNA in skin cells.'),
           ('What do all electromagnetic waves have in common?', 'They travel at the same speed in a vacuum', ['They have the same frequency', 'They are longitudinal', 'They need a medium'], 'c = 3.0 × 10⁸ m/s.'),
           ('Which EM wave is used to sterilise surgical instruments?', 'Gamma rays', ['Radio waves', 'Infrared', 'Visible light'], 'Gamma rays kill bacteria.')],
    why=[('Explain why gamma rays are more dangerous than radio waves.', 'Gamma rays have a very high frequency, so each photon carries a lot of energy; they are ionising and can damage DNA, causing mutations and cancer. Radio waves have low energy and are not ionising.'),
         ('Explain why microwaves are used for satellite communication but radio waves are used for long-distance broadcasting on Earth.', 'Microwaves pass through the atmosphere (including the ionosphere) to satellites; long-wave radio waves diffract around hills and reflect from the ionosphere, so they reach far beyond the horizon.'),
         ('Explain why infrared cameras can detect people in the dark.', 'All warm objects emit infrared; people are warmer than their surroundings and emit more infrared, which the camera detects.')],
    contrast=[('ionising radiation', 'non-ionising radiation', 'Ionising radiation (UV, X-rays, gamma) has enough energy to remove electrons from atoms and damage DNA; non-ionising radiation (radio, microwaves, infrared, visible) does not, though it can heat tissue.'),
              ('ultraviolet', 'infrared', 'Ultraviolet has a shorter wavelength and higher frequency than visible light and is ionising; infrared has a longer wavelength and lower frequency and is felt as heat.')],
    misc=[('Gamma rays travel faster than radio waves because they have more energy.', 'All EM waves travel at the same speed in a vacuum; gamma rays have higher frequency and shorter wavelength.'),
          ('Mobile phones emit ionising radiation that causes cancer.', 'Phones use microwaves/radio waves, which are non-ionising; current evidence does not show they cause cancer at normal exposure levels.')],
    cases=[('Wilhelm Röntgen’s discovery of X-rays (1895)', 'He noticed a screen glowing near a cathode-ray tube covered in card; an image of his wife’s hand showed her bones and ring.', 'uses of X-rays', 'X-rays pass through soft tissue but are absorbed by dense bone and metal, producing a shadow image.'),
           ('the James Webb Space Telescope (launched 2021)', 'It observes in infrared to see light from the earliest galaxies and to look through dust clouds.', 'infrared radiation', 'Light from distant galaxies is stretched to infrared wavelengths, and infrared passes through dust that blocks visible light.')],
    evaluate=[('The benefits of using X-rays in medicine outweigh the risks.', ['diagnose fractures, dental problems and lung disease quickly', 'CT scans guide surgery and cancer treatment'], ['ionising: small increase in cancer risk, especially with repeated CT scans', 'radiographers must be shielded'], 'For a justified scan the diagnostic benefit is far greater than the small risk; scans should be used only when needed and doses kept low.'),
              ('Sunbeds should be banned for everyone under 18.', ['UV exposure in youth greatly increases melanoma risk', 'Australia and Brazil have banned commercial sunbeds'], ['personal freedom', 'some argue for vitamin D (although it can be obtained more safely)'], 'The strong evidence of cancer risk justifies a ban for young people.')],
))

EM = [('radio waves', (1e5, 1e9)), ('microwaves', (1e9, 3e11)), ('infrared', (3e11, 4e14)), ('visible light', (4.3e14, 7.5e14)), ('ultraviolet', (7.5e14, 3e16)), ('X-rays', (3e16, 3e19)), ('gamma rays', (3e19, 3e21))]


def _sci(x):
    m_ = math.floor(math.log10(abs(x)))
    return f'{x / 10 ** m_:.3g} × 10^{m_}'


@R.add('ch10-st3', 'C3', (1, 5), 'numerical')
def em_calc(rng, slot):
    c = 3.0e8
    use, f = rng.choice([('a Wi-Fi router', 2.4e9), ('a microwave oven', 2.45e9), ('an FM radio station', 98.5e6), ('a 5G phone network', 3.5e9), ('a TV remote control (infrared)', 3.4e14),
                          ('green light from a laser pointer', 5.64e14), ('a UV-C steriliser lamp', 1.18e15), ('a medical X-ray', 3.0e18), ('an AM radio station', 909e3)])
    lam = c / f
    k = rng.choice(['lam', 'f', 'region'] if slot.d >= 2 else ['lam', 'region'])
    if k == 'lam':
        return dict(stem=f'{use[0].upper() + use[1:]} uses electromagnetic waves of frequency {_sci(f)} Hz. Calculate the wavelength (c = 3.0 × 10^8 m/s).', answer=f'{_sci(lam)} m',
                    markingKey=f'M1 λ = c/f = 3.0 × 10^8 ÷ {_sci(f)}; A1 {_sci(lam)} m.', marks=2)
    if k == 'f':
        return dict(stem=f'The electromagnetic waves used by {use} have a wavelength of {_sci(lam)} m. Calculate their frequency (c = 3.0 × 10^8 m/s).', answer=f'{_sci(f)} Hz',
                    markingKey=f'M1 f = c/λ; A1 {_sci(f)} Hz.', marks=2)
    region = next(n for n, (lo, hi) in EM if lo <= f < hi)
    return dict(stem=f'An EM wave has a frequency of {_sci(f)} Hz. (a) Calculate its wavelength. (b) Identify the region of the electromagnetic spectrum it belongs to.', answer=f'(a) {_sci(lam)} m (b) {region}',
                markingKey=f'(a) M1 λ = c/f; A1 {_sci(lam)} m. (b) 1 {region}.', marks=3)


@R.add('ch10-st3', 'C1', (1, 3), 'mcq')
def em_order(rng, slot):
    names_ = [n for n, _ in EM]
    i = rng.randrange(1, len(names_) - 1)
    k = rng.choice(['above', 'below'])
    right = names_[i + 1] if k == 'above' else names_[i - 1]
    wrong = [n for n in names_ if n not in (right, names_[i])]
    return mcq(rng, f'Which part of the electromagnetic spectrum is next to {names_[i]} on the {"higher" if k == "above" else "lower"}-frequency side?', right, rng.sample(wrong, 3),
               'Order of increasing frequency: radio, microwave, infrared, visible, ultraviolet, X-ray, gamma.')


R.facts('ch10-st4', F(
    terms=[('reflection', 'the bouncing back of a wave when it meets a boundary; the angle of incidence equals the angle of reflection'),
           ('refraction', 'the change in direction of a wave when it passes into a different medium (or depth) because its speed changes'),
           ('diffraction', 'the spreading out of a wave as it passes through a gap or around an obstacle'),
           ('wavefront', 'a line joining points on a wave that are in step, e.g. along a crest')],
    facts=[('When water waves move from deep to shallow water, what happens?', 'They slow down and their wavelength decreases', ['They speed up and their wavelength increases', 'Their frequency changes', 'Nothing changes'], 'Frequency stays the same, so λ falls with v.'),
           ('When is diffraction through a gap most noticeable?', 'When the gap is about the same size as the wavelength', ['When the gap is much larger than the wavelength', 'When there is no gap', 'Only for light'], 'Similar sizes give maximum spreading.'),
           ('What stays the same when a wave refracts?', 'Frequency', ['Speed', 'Wavelength', 'Direction'], 'Frequency is set by the source.')],
    why=[('Explain why water waves change direction when they cross into shallower water at an angle.', 'The part of each wavefront that reaches shallow water first slows down while the rest continues at the original speed, so the wavefront turns (refracts) towards the normal.'),
         ('Explain why you can hear someone talking around a corner but cannot see them.', 'Sound wavelengths (about 0.3-3 m) are similar to the size of a doorway, so sound diffracts around it; light wavelengths are tiny (about 5 × 10⁻⁷ m), so light hardly diffracts.'),
         ('Explain why harbour walls are designed with narrow entrances.', 'Waves diffract through the gap but lose energy as they spread out, so the water inside the harbour is calmer.')],
    contrast=[('refraction', 'diffraction', 'Refraction is a change in direction caused by a change in speed when entering a new medium; diffraction is spreading out through a gap or around an obstacle, with no change of speed.'),
              ('reflection', 'refraction', 'In reflection the wave bounces back into the same medium at the same speed; in refraction it enters a new medium, changes speed and usually direction.')],
    misc=[('Waves change frequency when they enter shallow water.', 'Frequency stays the same; speed and wavelength decrease.'),
          ('A wider harbour entrance causes more diffraction.', 'Diffraction is greatest when the gap is similar to the wavelength; a much wider gap causes less spreading.')],
    cases=[('waves bending around headlands and into bays', 'Ocean waves approaching a coast at an angle turn to become nearly parallel to the shore.', 'refraction', 'Waves slow in shallower water near the shore, so wavefronts bend until they arrive almost parallel to the beach.'),
           ('long-wave radio reception in mountain valleys', 'Long-wave BBC Radio 4 (wavelength about 1.5 km) can be received behind hills where FM (3 m) is weak.', 'diffraction', 'Long wavelengths diffract around large obstacles such as hills; short wavelengths do not.')],
    evaluate=[('Ripple tank models fully explain how light behaves.', ['show reflection, refraction and diffraction patterns similar to light'], ['light is electromagnetic and transverse in a different way', 'light also behaves as particles (photons)', 'ripple speeds and wavelengths are very different'], 'Ripple tanks are a useful analogy for wave behaviour but not a full model of light.')],
    extended=[('Water waves of frequency 4 Hz travel at 0.32 m/s in deep water and 0.20 m/s in shallow water in a ripple tank. (a) Calculate the wavelength in each region. (b) Draw a labelled diagram of wavefronts crossing the boundary at an angle. (c) Explain why the wavefronts change direction.', '(a) deep 0.08 m, shallow 0.05 m (b) closer-spaced wavefronts in shallow water, bent towards the normal (c) one end of each wavefront slows first, so the wavefront turns; frequency is unchanged.', 6),
              ('Design a harbour entrance to minimise waves inside a marina where the incoming waves have a wavelength of 8 m. Justify your design with reference to diffraction and reflection.', 'A wide entrance (much larger than 8 m) lets waves pass straight through with little spreading, so a strong beam of waves reaches boats in line with the gap. A narrow entrance of similar size to the wavelength makes the waves diffract and spread their energy over a wide area, so wave height inside is much lower. Best design: a narrow, angled (offset) entrance so no moorings are in line with it, plus sloping or rough inner walls that absorb rather than reflect wave energy.', 5, 'long')],
))


@R.add('ch10-st4', 'C3', (1, 5), 'numerical')
def depth_change(rng, slot):
    f = rng.choice([2, 4, 5, 8, 10])
    v1 = rng.choice([0.30, 0.32, 0.40, 0.45])
    v2 = round(v1 * rng.choice([0.5, 0.6, 0.75]), 3)
    l1, l2 = v1 / f, v2 / f
    if slot.d <= 2:
        return dict(stem=f'Water waves of frequency {f} Hz travel at {v1} m/s in deep water. Calculate their wavelength.', answer=f'{l1:.3g} m', markingKey=f'M1 λ = v/f = {v1}/{f}; A1 {l1:.3g} m.', marks=2)
    return dict(stem=f'Waves of frequency {f} Hz travel at {v1} m/s in deep water and {v2:g} m/s in shallow water. Calculate the wavelength in each region and state what happens to the frequency.', answer=f'deep {l1:.3g} m; shallow {l2:.3g} m; frequency unchanged ({f} Hz)',
                markingKey=f'M1 λ = v/f; A1 {l1:.3g} m; A1 {l2:.3g} m; 1 frequency stays at {f} Hz (set by source).', marks=4)


dataset('ch10-st4',
        dict(intro='{who} measured the speed of ripples in a ripple tank at different water depths.', iv=('Depth', 'cm'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Wave speed', 'cm/s'), f=lambda x: 31.3 * math.sqrt(x / 1.0), dp=1, trend='Wave speed increases with depth, but less than proportionally (≈ √depth).',
             why='In shallow water v ≈ √(g × depth); waves slow down in shallower water, which is why they refract at a depth boundary.'))

dataset('ch10-st3',
        dict(intro='{who} placed a UV sensor under a clear plastic sheet coated with different numbers of thin layers of sunscreen and measured the UV intensity reaching the sensor under a UV lamp.', iv=('Layers of sunscreen', ''), xs=[0, 1, 2, 3, 4],
             dv=('UV intensity', 'mW/cm²'), f=lambda x: 4.0 * 0.45 ** x, dp=2, trend='UV intensity reaching the sensor falls sharply as the number of layers increases, each layer roughly halving the intensity.',
             why='Sunscreen absorbs or reflects ultraviolet; less ionising UV reaches the skin, reducing DNA damage, sunburn and skin-cancer risk.'))

inquiry('ch10-st3',
        dict(ctx='how the distance from a Wi-Fi router affects the signal strength received by a phone',
             iv='distance from the router (1, 2, 4, 6, 8, 10 m)', dv='signal strength in dBm read from a Wi-Fi analyser app',
             cvs=[('the same phone and app', 'different antennas measure differently'), ('line of sight (no walls between)', 'walls absorb microwaves'), ('router channel and frequency band (2.4 GHz)', 'different bands behave differently'), ('height of the phone', 'reflections from the floor change readings')],
             hyp='If the distance increases, then the signal strength will decrease, because the microwave energy spreads out over a larger area (inverse-square law) and some is absorbed by air and objects.',
             method='Place the router on a table in a long corridor; hold the phone at the same height; read signal strength at each distance after 10 s; take 3 readings at each distance on different days; plot strength against distance.',
             safety='Wi-Fi is non-ionising and low power; take care walking backwards in corridors'))


# =============================================================================================
# ch11 Light and Sound
# =============================================================================================
R.facts('ch11-st1', F(
    terms=[('law of reflection', 'the angle of incidence equals the angle of reflection, both measured from the normal'),
           ('normal', 'an imaginary line drawn at 90° to a surface at the point where a ray meets it'),
           ('virtual image', 'an image that cannot be projected onto a screen because the light rays only appear to come from it'),
           ('specular reflection', 'reflection from a smooth surface in which parallel rays stay parallel, forming a clear image'),
           ('diffuse reflection', 'reflection from a rough surface in which parallel rays are scattered in many directions, so no image forms')],
    facts=[('A ray hits a plane mirror at 35° to the normal. What is the angle of reflection?', '35°', ['55°', '70°', '145°'], 'i = r, both from the normal.'),
           ('Which describes the image in a plane mirror?', 'Virtual, upright, same size, laterally inverted', ['Real, inverted, smaller', 'Virtual, inverted, larger', 'Real, upright, same size'], 'Plane mirror images are virtual and the same size.'),
           ('A person stands 2 m in front of a plane mirror. How far are they from their image?', '4 m', ['2 m', '1 m', '8 m'], 'The image is 2 m behind the mirror.'),
           ('Why is the word AMBULANCE written in reverse on the front of ambulances?', 'So drivers read it correctly in their rear-view mirrors', ['It is a tradition', 'So pedestrians notice it', 'To reflect more light'], 'Mirrors laterally invert images.')],
    why=[('Explain why you can see your reflection in a mirror but not in a sheet of white paper.', 'A mirror is smooth, so parallel rays stay together (specular reflection) and form an image; paper is rough at a microscopic level, so rays scatter in all directions (diffuse reflection) and no image forms.'),
         ('Explain why angles in reflection are measured from the normal rather than from the mirror surface.', 'The normal is well defined for any surface, including curved ones, so the law of reflection applies everywhere; measuring from the surface would give confusing values on curved mirrors.'),
         ('Explain why the image in a plane mirror is described as virtual.', 'The reflected rays diverge and only appear to come from a point behind the mirror; no light actually passes through that point, so the image cannot be formed on a screen.')],
    contrast=[('a real image', 'a virtual image', 'A real image is formed where light rays actually meet and can be projected on a screen; a virtual image is where rays only appear to come from and cannot be projected.'),
              ('specular reflection', 'diffuse reflection', 'Specular reflection from a smooth surface keeps parallel rays parallel and forms an image; diffuse reflection from a rough surface scatters rays in many directions.')],
    misc=[('The angle of reflection is measured between the ray and the mirror.', 'Both angles are measured from the normal (at 90° to the mirror).'),
          ('Rough surfaces do not obey the law of reflection.', 'Each ray still obeys i = r at the point it hits; the normals point in different directions, so rays scatter.')],
    cases=[('periscopes used in submarines and in crowds', 'Two plane mirrors at 45° let the user see over obstacles.', 'the law of reflection', 'Each mirror turns the light through 90° because i = r = 45°, so light from above reaches the eye.'),
           ('the Apollo lunar laser-ranging retroreflectors', 'Astronauts left corner-cube reflectors on the Moon in 1969; lasers from Earth are reflected straight back, measuring the distance to within a few centimetres.', 'reflection and timing', 'Two or three perpendicular mirrors send light back parallel to its path; distance = speed of light × time ÷ 2.')],
    evaluate=[('Solar farms using large mirrors (concentrated solar power) are better than photovoltaic panels.', ['can store heat in molten salt to generate electricity at night', 'large output in sunny deserts (e.g. Noor Ouarzazate, Morocco)'], ['need direct sunlight and large land areas', 'mirrors must be cleaned (water use in deserts)', 'PV is now cheaper and works in diffuse light'], 'CSP is valuable where storage is needed in very sunny regions; PV is generally cheaper elsewhere.')],
    extended=[('Two plane mirrors are placed at 90° to each other. A ray hits the first mirror at an angle of incidence of 30°. (a) Calculate the angle of reflection at the first mirror. (b) Calculate the angle of incidence at the second mirror. (c) Show that the ray leaves parallel to its original direction but reversed, and state one use of this arrangement.', '(a) 30° (b) the reflected ray meets the second mirror at 60° to its normal (90° − 30°) (c) total turn = 180°, so the ray returns parallel; used in bicycle reflectors, cat’s eyes and laser ranging.', 5)],
))


@R.add('ch11-st1', 'C3', (1, 5), 'numerical')
def mirror(rng, slot):
    k = rng.choice(['angle', 'glancing', 'image', 'move', 'tilt'] if slot.d >= 3 else ['angle', 'glancing', 'image'])
    if k == 'angle':
        i = rng.randint(15, 75)
        return dict(stem=f'A ray of light strikes a plane mirror with an angle of incidence of {i}°. State the angle of reflection and the angle between the incident and reflected rays.', answer=f'{i}°; {2 * i}°',
                    markingKey=f'1 r = i = {i}°; 1 angle between rays = {i} + {i} = {2 * i}°.', marks=2)
    if k == 'glancing':
        gl = rng.randint(10, 70)
        return dict(stem=f'A ray hits a plane mirror making an angle of {gl}° with the mirror surface. Calculate the angle of incidence and the angle of reflection.', answer=f'{90 - gl}° and {90 - gl}°',
                    markingKey=f'M1 angle from the normal = 90 − {gl}; A1 i = r = {90 - gl}°.', marks=2)
    if k == 'image':
        d = rng.choice([0.5, 1.2, 1.5, 2.0, 3.5])
        return dict(stem=f'{name(rng)} stands {d} m in front of a plane mirror. State how far behind the mirror the image is and how far the person is from their image.', answer=f'{d} m; {2 * d:g} m',
                    markingKey=f'1 image is the same distance behind the mirror, {d} m; 1 separation = {2 * d:g} m.', marks=2)
    if k == 'move':
        d = rng.choice([2.0, 3.0, 4.0])
        x = rng.choice([0.5, 1.0, 1.5])
        return dict(stem=f'A person stands {d} m from a plane mirror and walks {x} m towards it. By how much does the distance between the person and their image decrease?', answer=f'{2 * x:g} m',
                    markingKey=f'1 new separation = 2 × {d - x:g} = {2 * (d - x):g} m (was {2 * d:g} m); 1 decrease {2 * x:g} m.', marks=2)
    th = rng.choice([5, 10, 15, 20])
    return dict(stem=f'A ray strikes a plane mirror along the normal. The mirror is then rotated by {th}°. By what angle is the reflected ray turned? Explain.', answer=f'{2 * th}°',
                markingKey=f'1 the normal rotates by {th}°, so i = {th}° and r = {th}°; 1 the reflected ray turns through {2 * th}° from the incident ray.', marks=2)


dataset('ch11-st1',
        dict(intro='{who} shone a ray box at a plane mirror and measured the angle of reflection for different angles of incidence, using a protractor.', iv=('Angle of incidence', '°'), xs=[10, 20, 30, 40, 50],
             dv=('Angle of reflection', '°'), f=lambda x: x, dp=0, trend='The angle of reflection is equal to the angle of incidence within measurement uncertainty.',
             why='This is the law of reflection; small differences are due to the width of the ray and protractor reading uncertainty (about ±1°).'))

inquiry('ch11-st1',
        dict(ctx='whether the angle of reflection is always equal to the angle of incidence for a plane mirror',
             iv='angle of incidence (10° to 80° in 10° steps, measured from the normal)', dv='angle of reflection measured with a protractor from the normal',
             cvs=[('the same plane mirror', 'surface quality affects the reflected ray'), ('a narrow single-slit ray', 'wide rays are hard to measure'), ('darkened room', 'faint rays are hard to see'), ('mirror placed exactly on the line', 'misplacement gives errors')],
             hyp='If the angle of incidence increases, then the angle of reflection will increase by the same amount, because light reflects from a smooth surface with i = r.',
             method='Draw a line and a normal on paper; place the mirror on the line; shine a narrow ray from a ray box at 10°; mark the reflected ray with two crosses; measure r; repeat to 80°; repeat the whole set twice; plot r against i.',
             safety='ray boxes get hot; do not look directly into the beam'))

R.facts('ch11-st2', F(
    terms=[('refraction of light', 'the change of direction of light when it passes from one transparent medium to another because its speed changes'),
           ('refractive index (n)', 'the ratio of the speed of light in a vacuum to its speed in a material: n = c/v; also n = sin i ÷ sin r for light entering from air'),
           ('critical angle', 'the angle of incidence in the denser medium at which the angle of refraction is 90°'),
           ('total internal reflection', 'complete reflection of light inside a denser medium when the angle of incidence is greater than the critical angle'),
           ('optical fibre', 'a thin glass or plastic fibre that carries light along its length by repeated total internal reflection')],
    facts=[('When light passes from air into glass, how does it bend?', 'Towards the normal, because it slows down', ['Away from the normal, because it speeds up', 'It does not bend', 'Towards the surface'], 'Glass is optically denser.'),
           ('Which equation is Snell’s law (light entering from air)?', 'n = sin i ÷ sin r', ['n = i ÷ r', 'n = sin r ÷ sin i', 'n = v × c'], 'Ratio of sines.'),
           ('What two conditions are needed for total internal reflection?', 'Light travels from denser to less dense medium and angle of incidence > critical angle', ['Light enters a denser medium at any angle', 'The angle of incidence equals 0°', 'The surfaces are mirrored'], 'Both conditions are required.'),
           ('A ray enters a glass block along the normal. What happens?', 'It passes straight through without bending (but slows down)', ['It bends towards the normal', 'It reflects totally', 'It bends away from the normal'], 'i = 0 gives r = 0.')],
    why=[('Explain why light bends towards the normal when it enters glass from air at an angle.', 'Light slows down in glass; the part of the wavefront that enters first slows first, so the wavefront turns and the ray bends towards the normal.'),
         ('Explain why a swimming pool appears shallower than it really is.', 'Light from the bottom refracts away from the normal as it leaves the water; the eye traces the rays back in straight lines, so they appear to come from a point higher than the real bottom.'),
         ('Explain how optical fibres carry signals around bends.', 'Light hits the inside surface of the fibre at angles greater than the critical angle, so it is totally internally reflected again and again along the fibre with very little loss.'),
         ('Explain why diamonds sparkle more than glass.', 'Diamond has a high refractive index (2.42), so its critical angle is small (about 24°); light is totally internally reflected many times inside before leaving.')],
    contrast=[('refraction', 'total internal reflection', 'Refraction: light passes into the new medium and changes direction; total internal reflection: no light passes out – all is reflected back into the denser medium when i > critical angle.'),
              ('angle of incidence', 'critical angle', 'The angle of incidence is any angle between the incident ray and the normal; the critical angle is the particular angle of incidence (in the denser medium) that gives a refracted angle of 90°.')],
    misc=[('Light bends because it hits the glass surface hard.', 'Light bends because its speed changes in the new medium.'),
          ('Total internal reflection can happen when light goes from air into water.', 'It only happens going from a denser to a less dense medium (e.g. water to air).')],
    cases=[('endoscopes used in keyhole surgery', 'A bundle of optical fibres carries light into the body and an image back out through a small incision.', 'total internal reflection', 'Light inside each fibre hits the walls above the critical angle and is totally reflected, so it travels along a curved path.'),
           ('undersea fibre-optic cables linking continents', 'Cables such as MAREA (Spain-USA, 2017) carry over 200 terabits per second using infrared light pulses.', 'optical fibres', 'Infrared pulses are trapped in the glass core by total internal reflection and travel thousands of kilometres with little loss.')],
    evaluate=[('Fibre-optic broadband should be installed in every rural community, paid for by governments.', ['much faster, more reliable internet for education, healthcare and business', 'reduces the digital divide'], ['very expensive to lay cables to remote areas', 'satellite or 5G may be cheaper alternatives', 'public money could be spent on other priorities'], 'Fibre gives the best long-term service; public funding is justified where markets will not provide it, though other technologies may suit the most remote places.')],
))


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def snell(rng, slot):
    mat, n = rng.choice([('water', 1.33), ('glass', 1.50), ('Perspex', 1.49), ('diamond', 2.42), ('ice', 1.31), ('sapphire', 1.77)])
    k = rng.choice(['r', 'n', 'crit', 'speed', 'tir'] if slot.d >= 3 else ['r', 'n', 'speed'])
    if k == 'r':
        i = rng.choice([20, 30, 40, 45, 50, 60])
        r_ = math.degrees(math.asin(math.sin(math.radians(i)) / n))
        return dict(stem=f'A ray of light in air strikes a block of {mat} (n = {n}) at an angle of incidence of {i}°. Calculate the angle of refraction.', answer=f'{r_:.1f}°',
                    markingKey=f'M1 sin r = sin {i}° ÷ {n} = {math.sin(math.radians(i)) / n:.3f}; A1 r = {r_:.1f}°.', marks=2)
    if k == 'n':
        i = rng.choice([30, 40, 50, 60])
        r_ = round(math.degrees(math.asin(math.sin(math.radians(i)) / n)), 1)
        nn = math.sin(math.radians(i)) / math.sin(math.radians(r_))
        return dict(stem=f'{name(rng)} measures an angle of incidence of {i}° and an angle of refraction of {r_}° for light entering a transparent block from air. Calculate the refractive index and suggest the material using: water 1.33, ice 1.31, Perspex 1.49, glass 1.50, sapphire 1.77, diamond 2.42.', answer=f'{nn:.2f}; {mat}',
                    markingKey=f'M1 n = sin {i}° ÷ sin {r_}°; A1 {nn:.2f}; 1 closest material {mat}.', marks=3)
    if k == 'speed':
        v = 3.0e8 / n
        return dict(stem=f'The refractive index of {mat} is {n}. Calculate the speed of light in {mat} (c = 3.0 × 10^8 m/s).', answer=f'{v / 1e8:.3g} × 10^8 m/s',
                    markingKey=f'M1 v = c/n = 3.0 × 10^8 ÷ {n}; A1 {v / 1e8:.3g} × 10^8 m/s.', marks=2)
    c_ = math.degrees(math.asin(1 / n))
    if k == 'crit':
        return dict(stem=f'Calculate the critical angle for light travelling from {mat} (n = {n}) into air.', answer=f'{c_:.1f}°', markingKey=f'M1 sin c = 1/n = 1/{n}; A1 c = {c_:.1f}°.', marks=2)
    i = rng.choice([max(5, int(c_) - 8), int(c_) + 6])
    tir = i > c_
    return dict(stem=f'Light travelling inside {mat} (n = {n}) meets the boundary with air at an angle of incidence of {i}°. Calculate the critical angle and decide whether total internal reflection occurs. If not, calculate the angle of refraction in air.',
                answer=f'critical angle {c_:.1f}°; ' + ('total internal reflection occurs' if tir else f'no TIR; refracted at {math.degrees(math.asin(min(1, n * math.sin(math.radians(i))))):.1f}°'),
                markingKey=f'M1 sin c = 1/{n}; A1 c = {c_:.1f}°; 1 {i}° {">" if tir else "<"} c so ' + ('TIR' if tir else f'refraction: sin r = {n} × sin {i}°, r = {math.degrees(math.asin(min(1, n * math.sin(math.radians(i))))):.1f}°') + '.', marks=4)


dataset('ch11-st2',
        dict(intro='{who} shone a ray into a semicircular glass block and measured the angle of refraction for different angles of incidence.', iv=('Angle of incidence', '°'), xs=[10, 20, 30, 40, 50],
             dv=('Angle of refraction', '°'), f=lambda x: math.degrees(math.asin(math.sin(math.radians(x)) / 1.5)), dp=1, trend='The angle of refraction increases with the angle of incidence but is always smaller; the ratio sin i/sin r is about 1.5.',
             why='Light slows down in glass and bends towards the normal; Snell’s law gives a constant ratio sin i ÷ sin r equal to the refractive index.'))

inquiry('ch11-st2',
        dict(ctx='how the angle of incidence affects the angle of refraction when light enters a glass block, to find the refractive index of the glass',
             iv='angle of incidence in air (10° to 70°)', dv='angle of refraction in the glass, found by marking the ray path and measuring with a protractor',
             cvs=[('the same glass block', 'different blocks have different refractive indices'), ('colour of light (use one filter)', 'different colours refract by different amounts'), ('narrow ray from the same ray box', 'wide rays reduce precision'), ('drawing the normal accurately at 90°', 'angle errors')],
             hyp='If the angle of incidence increases, then the angle of refraction will increase, with sin i ÷ sin r staying constant, because the speed of light changes by a fixed ratio between air and glass.',
             method='Draw round a rectangular block; draw a normal; shine a narrow ray at 10°, 20° … 70°; mark entry and exit points; remove the block, join points and measure r; repeat each angle twice; plot sin i against sin r – the gradient is n.',
             weak=('a wide beam from a torch was used', 'use a ray box with a single narrow slit so the ray can be marked precisely'),
             safety='ray box lamps get hot; handle glass blocks carefully'))

R.facts('ch11-st3', F(
    terms=[('converging (convex) lens', 'a lens that is thicker in the middle and refracts parallel rays so they meet at a principal focus'),
           ('diverging (concave) lens', 'a lens that is thinner in the middle and spreads parallel rays out so they appear to come from a principal focus'),
           ('principal focus (focal point)', 'the point where rays parallel to the principal axis meet (or appear to come from) after passing through a lens'),
           ('focal length', 'the distance from the centre of a lens to its principal focus'),
           ('magnification', 'image height divided by object height'),
           ('power of a lens', 'the reciprocal of focal length in metres, measured in dioptres (D)')],
    facts=[('Which type of lens is used to correct long-sightedness?', 'Converging (convex)', ['Diverging (concave)', 'Plane glass', 'Cylindrical mirror'], 'It adds converging power so near objects focus on the retina.'),
           ('Which type of lens is used to correct short-sightedness?', 'Diverging (concave)', ['Converging (convex)', 'Bifocal mirror', 'Prism'], 'It spreads the rays so they focus further back, on the retina.'),
           ('An object is placed more than twice the focal length from a converging lens. What is the image like?', 'Real, inverted, diminished', ['Virtual, upright, magnified', 'Real, upright, same size', 'Virtual, inverted, diminished'], 'This is how a camera forms an image.'),
           ('What kind of image does a magnifying glass produce?', 'Virtual, upright, magnified', ['Real, inverted, magnified', 'Real, upright, diminished', 'Virtual, inverted, diminished'], 'The object is inside the focal length.')],
    why=[('Explain why a converging lens can produce a real image but a diverging lens alone cannot.', 'A converging lens bends rays towards each other so they actually meet; a diverging lens spreads rays apart so they never meet – they only appear to come from a point (virtual image).'),
         ('Explain why a thicker converging lens has a shorter focal length.', 'More curved surfaces refract light through larger angles, so parallel rays meet closer to the lens.'),
         ('Explain why a camera must change the distance between the lens and the sensor to focus on near and far objects.', 'The image distance depends on the object distance; for nearer objects the real image forms further behind the lens, so the lens is moved to put the image on the sensor.')],
    contrast=[('a converging lens', 'a diverging lens', 'A converging (convex) lens is thicker in the middle and brings parallel rays to a real focus; a diverging (concave) lens is thinner in the middle and spreads rays so they appear to come from a virtual focus.'),
              ('a real image', 'a virtual image', 'A real image forms where rays meet and can be projected; a virtual image forms where rays only appear to come from and cannot be projected.')],
    misc=[('A magnifying glass makes the object bigger.', 'The object is unchanged; the lens forms a larger virtual image.'),
          ('All images formed by converging lenses are upright.', 'Real images from converging lenses are inverted; only the virtual image (object inside the focal length) is upright.')],
    cases=[('the Hubble Space Telescope mirror problem (1990) and its fix (1993)', 'Hubble’s main mirror was ground to the wrong shape, producing blurry images; astronauts installed corrective optics like “glasses”.', 'focusing and correction of images', 'Additional optics changed the paths of the light rays so they came to a sharp focus, just as lenses correct eyesight.'),
           ('low-cost adjustable glasses (e.g. fluid-filled lenses tested in Ghana and Malawi)', 'Users turn a dial to inject silicone fluid, changing the lens curvature until vision is clear.', 'how lens shape determines focal length', 'Changing curvature changes how much rays are refracted, and therefore the focal length and power of the lens.')],
    evaluate=[('Laser eye surgery is a better solution than glasses for short-sightedness.', ['permanent correction, no glasses or contacts', 'convenient for sport and work'], ['expensive and not available everywhere', 'small risk of complications (dry eyes, glare)', 'not suitable for everyone; vision can still change with age'], 'It is a good option for suitable adults, but glasses remain safer, cheaper and reversible for many people.')],
    extended=[('An object 2.0 cm tall is placed 30 cm from a converging lens of focal length 10 cm. (a) Use the lens equation 1/f = 1/u + 1/v to find the image distance. (b) Calculate the magnification and image height. (c) Describe the image.', '(a) 1/v = 1/10 − 1/30 = 2/30, v = 15 cm (b) m = v/u = 0.5; image height 1.0 cm (c) real, inverted, diminished.', 5)],
))


@R.add('ch11-st3', 'C3', (1, 5), 'numerical')
def lens(rng, slot):
    k = rng.choice(['mag', 'power', 'height', 'lenseq'] if slot.d >= 3 else ['mag', 'power', 'height'])
    if k == 'mag':
        o = rng.choice([0.5, 1.0, 1.5, 2.0, 4.0])
        im = round(o * rng.choice([0.25, 0.5, 2.0, 2.5, 3.0, 4.0]), 2)
        return dict(stem=f'An object {o} cm tall forms an image {im:g} cm tall with a lens. Calculate the magnification and state whether the image is magnified or diminished.', answer=f'{im / o:.3g}; {"magnified" if im > o else "diminished"}',
                    markingKey=f'M1 m = image height ÷ object height = {im:g}/{o}; A1 {im / o:.3g}; 1 {"magnified (m > 1)" if im > o else "diminished (m < 1)"}.', marks=3)
    if k == 'power':
        f = rng.choice([0.10, 0.20, 0.25, 0.40, 0.50, -0.25, -0.50, -1.0])
        P = 1 / f
        return dict(stem=f'A lens has a focal length of {abs(f) * 100:g} cm and is {"converging" if f > 0 else "diverging"}. Calculate its power in dioptres (P = 1/f, f in metres; diverging lenses have negative f).', answer=f'{P:+.3g} D',
                    markingKey=f'M1 f = {f} m; A1 P = 1/{f} = {P:+.3g} D (sign required).', marks=2)
    if k == 'height':
        m = rng.choice([3, 4, 5, 8, 10])
        h = rng.choice([2.0, 3.5, 4.0, 6.0])
        return dict(stem=f'A magnifying glass gives a magnification of {m}. The image of a printed letter is {h} mm tall. How tall is the letter?', answer=f'{h / m:.3g} mm',
                    markingKey=f'M1 object height = image height ÷ m = {h}/{m}; A1 {h / m:.3g} mm.', marks=2)
    f = rng.choice([5, 10, 15, 20])
    u = f * rng.choice([1.5, 2, 3, 4])
    v = 1 / (1 / f - 1 / u)
    m = v / u
    return dict(stem=f'An object is placed {u:g} cm from a converging lens of focal length {f} cm. Use 1/f = 1/u + 1/v to find the image distance, then find the magnification and describe the image.', answer=f'v = {v:.3g} cm; m = {m:.3g}; real, inverted, ' + ('magnified' if m > 1 else 'same size' if abs(m - 1) < 1e-9 else 'diminished'),
                markingKey=f'M1 1/v = 1/{f} − 1/{u:g}; A1 v = {v:.3g} cm; A1 m = v/u = {m:.3g}; 1 real, inverted, {"magnified" if m > 1 else "same size" if abs(m - 1) < 1e-9 else "diminished"}.', marks=4)


dataset('ch11-st3',
        dict(intro='{who} placed a candle at different distances from a converging lens and moved a screen until the image was sharp, measuring the image distance.', iv=('Object distance', 'cm'), xs=[20, 25, 30, 40, 60],
             dv=('Image distance', 'cm'), f=lambda x: 1 / (1 / 15 - 1 / x), dp=1, trend='The image distance decreases as the object distance increases, approaching the focal length (about 15 cm) for distant objects.',
             why='Rays from a more distant object are closer to parallel, so they are brought to a focus nearer to the principal focus; 1/f = 1/u + 1/v.'))

inquiry('ch11-st3',
        dict(ctx='how the object distance affects the image distance for a converging lens, in order to find its focal length',
             iv='object distance u from the lens (20, 25, 30, 40, 50, 60 cm)', dv='image distance v – distance from lens to screen when the image is sharpest, measured with a metre rule',
             cvs=[('the same lens', 'focal length is a property of the lens'), ('lens perpendicular to the bench', 'tilting distorts the image'), ('lighting (dim room)', 'helps judge sharpness'), ('the same object (illuminated cross-wire)', 'consistent judging of sharpness')],
             hyp='If the object distance increases, then the image distance will decrease towards the focal length, because 1/f = 1/u + 1/v.',
             method='Place an illuminated object, lens and screen on an optical bench; set u = 20 cm; move the screen to find the sharpest image; measure v; approach from both sides and average; repeat for each u; plot 1/v against 1/u – the intercepts give 1/f.',
             weak=('the sharp image position was judged once by moving the screen in one direction only', 'find the sharp position approaching from both directions and take the mean, repeating three times'),
             safety='candles: tie hair back; lamps get hot'))

R.facts('ch11-st4', F(
    terms=[('pitch', 'how high or low a sound seems, determined by its frequency'),
           ('loudness', 'how loud a sound seems, determined by its amplitude'),
           ('echo', 'a reflected sound wave heard after the original sound'),
           ('ultrasound', 'sound with a frequency above 20 000 Hz, beyond the range of human hearing'),
           ('range of human hearing', 'approximately 20 Hz to 20 000 Hz, narrowing with age'),
           ('decibel (dB)', 'the unit used to measure sound intensity level')],
    facts=[('What is the approximate speed of sound in air at room temperature?', '340 m/s', ['3 × 10⁸ m/s', '34 m/s', '1500 m/s'], 'About 330-343 m/s depending on temperature.'),
           ('In which medium does sound travel fastest?', 'Steel', ['Air', 'Water', 'A vacuum'], 'About 5000-6000 m/s in steel.'),
           ('If a note becomes louder but stays at the same pitch, what has changed?', 'Amplitude', ['Frequency', 'Wavelength', 'Speed'], 'Loudness depends on amplitude.'),
           ('Which use of ultrasound involves echoes?', 'Prenatal scanning of a fetus', ['Cooking food', 'Radio broadcasting', 'Detecting forged bank notes'], 'Echoes from tissue boundaries build an image.')],
    why=[('Explain why sound travels faster in solids than in gases.', 'Particles in a solid are close together and strongly bonded, so vibrations are passed from particle to particle more quickly.'),
         ('Explain why you see lightning before you hear thunder.', 'Light travels at 3 × 10⁸ m/s and sound at about 340 m/s, so the light arrives almost instantly while the sound takes about 3 s per kilometre.'),
         ('Explain why ultrasound rather than X-rays is used to scan a fetus.', 'Ultrasound is non-ionising and is not known to harm cells, while X-rays are ionising and could damage the developing fetus’s DNA.')],
    contrast=[('pitch', 'loudness', 'Pitch depends on frequency (higher frequency → higher note); loudness depends on amplitude (larger amplitude → louder).'),
              ('sound waves', 'light waves', 'Sound is a longitudinal mechanical wave that needs a medium and travels at about 340 m/s in air; light is a transverse EM wave that can travel through a vacuum at 3 × 10⁸ m/s.')],
    misc=[('A higher-pitched sound travels faster through air.', 'All frequencies travel at the same speed in air; higher pitch means higher frequency and shorter wavelength.'),
          ('In an echo calculation, distance = speed × time.', 'The sound travels there and back, so distance to the reflector = speed × time ÷ 2.')],
    cases=[('bats using echolocation', 'Bats emit ultrasound pulses of 20-100 kHz and listen for echoes to locate insects in the dark.', 'echoes and ultrasound', 'The time delay of the echo shows the distance to the insect; short wavelengths give detailed information about small targets.'),
           ('sonar mapping of the ocean floor', 'Ships send sound pulses downward and time the echoes to map the sea bed, e.g. the search for flight MH370 in the Indian Ocean.', 'echo-sounding', 'depth = speed of sound in water × time ÷ 2.')],
    evaluate=[('Noise pollution from cities and airports should be treated as a serious public-health issue.', ['long-term exposure is linked to stress, sleep disturbance and heart disease (WHO)', 'affects learning in schools under flight paths'], ['noise is hard to avoid in busy economies', 'reducing it (quieter engines, barriers, night bans) is expensive'], 'Evidence of health harm justifies treating noise as a public-health issue, with targeted measures where exposure is highest.')],
))


@R.add('ch11-st4', 'C3', (1, 5), 'numerical')
def echo(rng, slot):
    k = rng.choice(['echo', 'sonar', 'storm', 'speed', 'lam', 'ultra'] if slot.d >= 3 else ['echo', 'storm', 'lam'])
    if k == 'echo':
        t = rng.choice([0.4, 0.6, 0.8, 1.2, 1.5, 2.0])
        v = 340
        return dict(stem=f'{name(rng)} claps in front of a cliff and hears the echo {t} s later. Calculate the distance to the cliff (speed of sound = 340 m/s).', answer=f'{v * t / 2:g} m',
                    markingKey=f'M1 total distance = 340 × {t} = {v * t:g} m; M1 ÷ 2 (there and back); A1 {v * t / 2:g} m.', marks=3)
    if k == 'sonar':
        t = rng.choice([0.8, 1.6, 2.4, 3.0, 4.0, 6.0])
        return dict(stem=f'A ship’s sonar pulse returns from the sea bed after {t} s. The speed of sound in sea water is 1500 m/s. Calculate the depth of the sea.', answer=f'{1500 * t / 2:g} m',
                    markingKey=f'M1 1500 × {t} ÷ 2; A1 {1500 * t / 2:g} m.', marks=2)
    if k == 'storm':
        t = rng.choice([2.0, 3.0, 4.5, 6.0, 9.0])
        return dict(stem=f'Thunder is heard {t} s after a lightning flash is seen. Estimate the distance to the storm (speed of sound 340 m/s) and explain why the light’s travel time can be ignored.', answer=f'{340 * t:g} m (≈ {340 * t / 1000:.2g} km)',
                    markingKey=f'M1 d = 340 × {t}; A1 {340 * t:g} m; 1 light travels at 3 × 10⁸ m/s, so it arrives in about {340 * t / 3e8 * 1e6:.1f} μs – negligible.', marks=3)
    if k == 'speed':
        d = rng.choice([100, 150, 200, 250])
        t = round(d / rng.uniform(330, 350), 2)
        return dict(stem=f'Two students stand {d} m apart. One bangs two blocks together and the other starts a stopwatch on seeing the blocks hit and stops it on hearing the sound, getting {t} s. Calculate the speed of sound and suggest one way to improve the accuracy.', answer=f'{d / t:.0f} m/s; e.g. repeat and average many times, use a longer distance, or use a data logger with microphones',
                    markingKey=f'M1 v = d/t = {d}/{t}; A1 {d / t:.0f} m/s; 1 improvement that reduces reaction-time error.', marks=3)
    if k == 'lam':
        f = rng.choice([256, 440, 512, 1000, 2000, 8000])
        return dict(stem=f'A note of frequency {f} Hz travels through air at 340 m/s. Calculate its wavelength.', answer=f'{340 / f:.3g} m', markingKey=f'M1 λ = v/f = 340/{f}; A1 {340 / f:.3g} m.', marks=2)
    f = rng.choice([2e6, 3.5e6, 5e6])
    t = rng.choice([40e-6, 65e-6, 100e-6])
    d = 1540 * t / 2
    return dict(stem=f'In a medical ultrasound scan, {f / 1e6:g} MHz pulses travel at 1540 m/s in soft tissue. An echo from a boundary returns after {t * 1e6:g} μs. Calculate (a) the depth of the boundary in cm and (b) the wavelength of the ultrasound in mm.', answer=f'(a) {d * 100:.3g} cm (b) {1540 / f * 1000:.3g} mm',
                markingKey=f'(a) M1 1540 × {t * 1e6:g} × 10⁻⁶ ÷ 2; A1 {d * 100:.3g} cm. (b) M1 λ = v/f; A1 {1540 / f * 1000:.3g} mm.', marks=4)


dataset('ch11-st4',
        dict(intro='{who} used an oscilloscope app and a signal generator to measure the wavelength of sound in air at different frequencies.', iv=('Frequency', 'Hz'), xs=[500, 1000, 1500, 2000, 2500],
             dv=('Wavelength', 'cm'), f=lambda x: 34300 / x, dp=1, trend='Wavelength decreases as frequency increases, and frequency × wavelength stays about 340 m/s.',
             why='The speed of sound in air is fixed at a given temperature, so v = fλ means λ is inversely proportional to f.'))

inquiry('ch11-st4',
        dict(ctx='how the temperature of air affects the speed of sound',
             iv='air temperature (°C), changed by testing in a warm room, outdoors and in a cold store', dv='speed of sound = distance between two microphones ÷ time delay measured with a data logger',
             cvs=[('distance between microphones (e.g. 1.00 m)', 'speed is calculated from it'), ('humidity', 'water vapour slightly changes the speed'), ('type of sound pulse (sharp clap or click)', 'a sharp pulse gives a clear start'), ('background noise', 'may trigger the logger falsely')],
             hyp='If the air temperature increases, then the speed of sound will increase, because air particles move faster and pass vibrations on more quickly (about +0.6 m/s per °C).',
             method='Place two microphones 1.00 m apart in line with a sound source; connect to a data logger that records the time between triggers; make a sharp click; record the delay 10 times at each temperature (measured with a thermometer); calculate mean speed.',
             weak=('the microphones were only 10 cm apart', 'increase the separation to at least 1 m so the time delay is much larger than the timing uncertainty'),
             safety='avoid very loud sounds near ears'))

R.f['ch11-st2'].extended = [('An optical fibre has a glass core of refractive index 1.52. (a) Calculate the critical angle at the core–air boundary. (b) Explain why the fibre is surrounded by a cladding of lower refractive index (1.48) and calculate the new critical angle at the core–cladding boundary using sin c = n₂/n₁. (c) Explain one advantage of optical fibres over copper cables for internet data.', '(a) sin c = 1/1.52, c = 41.1° (b) cladding protects the core surface from scratches and prevents light leaking into touching fibres; sin c = 1.48/1.52, c = 76.8° (c) higher bandwidth / less signal loss over long distances / no electrical interference.', 6),
                            ('Describe how you would use a semicircular glass block and a ray box to measure the critical angle of glass, and use your result to calculate the refractive index. Include one source of uncertainty and how to reduce it.', 'Aim the ray at the centre of the flat face from inside the curved side (so it enters the curved face along a normal); increase the angle until the refracted ray just runs along the flat face (90°); mark and measure the angle of incidence = critical angle (≈ 42°); n = 1/sin c ≈ 1.5. Uncertainty: judging the exact angle where refraction stops – repeat, approach from both sides, use a narrow ray in a dark room.', 6, 'long')]


# =============================================================================================
# ch12 Magnetism and Electromagnetism
# =============================================================================================
R.facts('ch12-st1', F(
    terms=[('magnetic field', 'the region around a magnet where a magnetic material or another magnet experiences a force'),
           ('magnetic field line', 'a line showing the direction a north pole would move in a magnetic field; lines go from north to south outside a magnet'),
           ('magnetic material', 'a material that is attracted by a magnet and can be magnetised, e.g. iron, steel, nickel and cobalt'),
           ('induced magnetism', 'magnetism produced temporarily in a magnetic material when it is placed in a magnetic field'),
           ('permanent magnet', 'a magnet that produces its own magnetic field all the time'),
           ('soft magnetic material', 'a material such as iron that is easily magnetised and loses its magnetism easily')],
    facts=[('Which of these is a magnetic material?', 'Nickel', ['Aluminium', 'Copper', 'Brass'], 'Iron, cobalt and nickel (and steel) are magnetic.'),
           ('What happens when two north poles are brought close together?', 'They repel', ['They attract', 'Nothing', 'They become south poles'], 'Like poles repel.'),
           ('Where is the magnetic field of a bar magnet strongest?', 'At the poles', ['In the middle', 'Equally everywhere', 'Far from the magnet'], 'Field lines are closest at the poles.'),
           ('Which instrument can be used to plot the field lines around a magnet?', 'A plotting compass', ['A voltmeter', 'A thermometer', 'A newton meter'], 'The compass needle aligns with the field.'),
           ('Which test proves that an object is a magnet rather than just magnetic?', 'It repels one pole of a known magnet', ['It attracts a magnet', 'It is made of iron', 'It is attracted to steel'], 'Only magnets can repel; magnetic materials are always attracted.')],
    why=[('Explain why repulsion is the only true test for a magnet.', 'A magnetic material and a magnet both attract a magnet, but only a magnet has poles that can repel another magnet’s like pole.'),
         ('Explain why a compass points north.', 'The compass needle is a small magnet that lines up with the Earth’s magnetic field; its north pole is attracted towards the Earth’s magnetic pole in the Arctic, which is actually a magnetic south pole.'),
         ('Explain why a steel paper clip attached to a magnet can pick up another paper clip.', 'The magnetic field induces magnetism in the first clip, making it a temporary magnet that can attract a second clip.'),
         ('Explain why soft iron is used for temporary magnets but steel is used for permanent magnets.', 'Iron is easily magnetised and demagnetised, so it loses magnetism when the field is removed; steel is harder to magnetise but keeps its magnetism.')],
    contrast=[('a permanent magnet', 'an induced magnet', 'A permanent magnet has its own magnetic field all the time; an induced magnet is a magnetic material that becomes magnetic only while it is in another magnetic field.'),
              ('soft iron', 'steel', 'Soft iron magnetises and demagnetises easily (used in electromagnets and transformers); steel is harder to magnetise but keeps its magnetism (used for permanent magnets).')],
    misc=[('All metals are attracted to magnets.', 'Only magnetic metals such as iron, steel, nickel and cobalt are attracted; copper, aluminium and gold are not.'),
          ('Magnetic field lines can cross each other.', 'Field lines never cross; at any point the field has only one direction.'),
          ('The Earth’s geographic North Pole is a magnetic north pole.', 'It attracts the north pole of a compass, so it behaves as a magnetic south pole.')],
    cases=[('the Earth’s magnetic field and the aurora', 'Charged particles from the Sun are guided by the Earth’s magnetic field towards the poles, producing the aurora borealis seen in Norway, Iceland and Canada.', 'magnetic fields exerting forces', 'The field deflects charged particles, protecting the surface from much of the solar wind and concentrating particles near the poles.'),
           ('magnetic separation of scrap metal in recycling plants', 'Large magnets lift steel and iron cans from mixed waste, leaving aluminium cans behind.', 'magnetic and non-magnetic materials', 'Steel is magnetic and is attracted to the magnet; aluminium is not.')],
    evaluate=[('Mining rare-earth metals for powerful neodymium magnets is justified by their use in wind turbines and electric cars.', ['strong magnets make generators and motors efficient, supporting low-carbon energy', 'smaller, lighter motors'], ['mining and refining (e.g. in Bayan Obo, China) produce toxic and radioactive waste', 'supply is concentrated in few countries', 'recycling of magnets is still rare'], 'They are important for decarbonisation, but strict environmental regulation, diversified supply and recycling are needed.')],
    extended=[('Describe how you would use a plotting compass to draw the magnetic field pattern around a bar magnet, and explain how the pattern changes when two bar magnets are placed with (a) opposite poles and (b) like poles facing each other.', 'Place the magnet on paper; put the compass near the N pole, mark the end of the needle, move the compass so its tail is at the mark, repeat to the S pole; draw a smooth line with arrows N→S; repeat from different starting points. (a) Lines go straight across the gap from N to S – strong, uniform field (attraction). (b) Lines push apart and a neutral point with no field forms midway (repulsion).', 6, 'long')],
))

dataset('ch12-st1',
        dict(intro='{who} measured the magnetic field strength at different distances from the pole of a bar magnet using a phone magnetometer app.', iv=('Distance from pole', 'cm'), xs=[2, 4, 6, 8, 10],
             dv=('Field strength', 'μT'), f=lambda x: 4000 / x ** 3, dp=1, trend='The field strength falls rapidly as distance increases; doubling the distance reduces it to about one-eighth.',
             why='Field lines spread out further from the pole, so the field is weaker; for a magnet the field falls roughly with the cube of distance.'))

inquiry('ch12-st1',
        dict(ctx='how the distance between a magnet and a steel paper clip affects the force of attraction',
             iv='distance between the magnet and the clip (cm), set with plastic spacers', dv='force needed to pull the clip away, measured with a sensitive newton meter (or number of clips held)',
             cvs=[('the same magnet', 'magnets differ in strength'), ('the same type of clip', 'mass and steel type affect attraction'), ('spacers of non-magnetic material', 'magnetic spacers would conduct the field'), ('orientation of the magnet pole', 'the field is strongest at the poles')],
             hyp='If the distance increases, then the force will decrease rapidly, because the magnetic field gets weaker further from the pole as field lines spread out.',
             method='Clamp the magnet; place 0.5 cm plastic spacers between magnet and clip (0.5 to 3.0 cm); attach a 1 N newton meter and pull gently until the clip detaches; record the peak force; repeat 3 times per distance; plot force against distance.',
             safety='strong magnets can trap fingers; keep away from phones and bank cards'))

R.facts('ch12-st2', F(
    terms=[('electromagnet', 'a coil of wire, usually wrapped around a soft iron core, that becomes a magnet when a current flows'),
           ('solenoid', 'a long coil of wire that produces a magnetic field similar to a bar magnet when a current flows'),
           ('right-hand grip rule', 'if the fingers of the right hand curl in the direction of the current, the thumb points along the field lines (towards the north pole of a solenoid)'),
           ('soft iron core', 'a core of easily magnetised iron placed inside a coil to make its magnetic field much stronger')],
    facts=[('What is the shape of the magnetic field around a long straight wire carrying a current?', 'Concentric circles around the wire', ['Straight lines parallel to the wire', 'Like a bar magnet', 'No field'], 'Field lines circle the wire.'),
           ('Which change would make an electromagnet stronger?', 'Increasing the number of turns of wire', ['Using a copper core', 'Reducing the current', 'Using fewer turns'], 'More turns, more current or an iron core.'),
           ('What happens to the field of a solenoid when the current direction is reversed?', 'The poles swap', ['It disappears', 'It doubles', 'Nothing changes'], 'Field direction depends on current direction.'),
           ('Why is soft iron, not steel, used for electromagnet cores?', 'It loses its magnetism when the current is switched off', ['It is a better conductor of electricity', 'It is cheaper than all other metals', 'It is not magnetic'], 'Steel would stay magnetised.')],
    why=[('Explain why an electromagnet is more useful than a permanent magnet in a scrapyard crane.', 'The electromagnet can be switched off, so the crane can release the scrap metal where needed; its strength can also be adjusted by changing the current.'),
         ('Explain why adding a soft iron core makes a solenoid’s field much stronger.', 'The iron becomes magnetised (induced magnetism) by the solenoid’s field, adding its own strong field to that of the coil.'),
         ('Explain why the field inside a long solenoid is strong and uniform.', 'The fields from each turn add together inside the coil, producing parallel, closely spaced field lines.')],
    contrast=[('a solenoid', 'an electromagnet', 'A solenoid is a coil of wire that produces a magnetic field when current flows; an electromagnet is usually a solenoid with a soft iron core, making the field much stronger.'),
              ('an electromagnet', 'a permanent magnet', 'An electromagnet works only while current flows and its strength can be changed; a permanent magnet always has its field and its strength is fixed.')],
    misc=[('An electromagnet works because the current flows through the iron core.', 'The current flows only in the coil; the core is magnetised by the coil’s field.'),
          ('Using a copper core would make an electromagnet stronger because copper is a good conductor.', 'Copper is not magnetic, so it does not increase the field; soft iron is used.')],
    cases=[('MRI scanners in hospitals', 'Superconducting electromagnets cooled with liquid helium produce fields of 1.5-3 T, tens of thousands of times stronger than the Earth’s field.', 'the strength of electromagnets', 'Very large currents in many turns of superconducting wire produce an extremely strong, uniform field inside the solenoid.'),
           ('the Shanghai maglev train', 'Electromagnets on the train and track lift it above the guideway and propel it at up to 431 km/h.', 'uses of electromagnets', 'Switching currents in the electromagnets controls attraction and repulsion, removing wheel friction.')],
    evaluate=[('Maglev trains are a better investment than conventional high-speed rail.', ['higher speeds, low friction, less wear and noise', 'very smooth ride'], ['much higher construction cost', 'incompatible with existing rail networks', 'high energy use at top speed'], 'Maglev is technically impressive, but conventional high-speed rail is usually more cost-effective unless very high speed on a dedicated route is essential.')],
    extended=[('Describe how the right-hand grip rule is used to find the poles of a solenoid, and explain three ways to increase the strength of an electromagnet. Suggest why there is a limit to how much the strength can be increased by raising the current.', 'Curl the fingers of the right hand in the direction of conventional current around the coil; the thumb points to the north pole. Stronger: more turns, larger current, soft iron core (also shorter/closer turns). Limit: wires heat up (I²R), insulation can melt, and the iron core saturates so extra current adds little.', 6, 'long'),
              ('An electromagnet with 50 turns picks up 12 paper clips and with 100 turns picks up 23. Analyse whether the number of clips is proportional to the number of turns and suggest two sources of error in this method.', '23/12 ≈ 1.9, close to 2, so roughly proportional (within experimental error). Errors: clips are discrete (resolution ±1 clip); clips cling in chains depending on arrangement; current may change as the wire warms; residual magnetism in the core.', 4)],
))


@R.add('ch12-st2', 'C3', (1, 4), 'short')
def solenoid_poles(rng, slot):
    end = rng.choice(['left', 'right'])
    view = rng.choice(['clockwise', 'anticlockwise'])
    pole = 'south' if view == 'clockwise' else 'north'
    other = 'north' if pole == 'south' else 'south'
    return dict(stem=f'Looking at the {end}-hand end of a solenoid, the current flows {view}. State the pole at the {end}-hand end and at the other end, and describe what happens to a compass placed beyond the {end}-hand end if the current is reversed.',
                answer=f'{end}-hand end: {pole}; other end: {other}; the compass needle turns through 180° when the current is reversed',
                markingKey=f'1 {pole} pole (clockwise = S, anticlockwise = N when viewed from the end, or right-hand grip rule); 1 {other} at the other end; 1 reversing current reverses the poles, so the compass swings round.', marks=3)


dataset('ch12-st2',
        dict(intro='{who} wound different numbers of turns of insulated wire around an iron nail, passed 2.0 A through the coil and counted the number of steel paper clips the electromagnet could hold.', iv=('Number of turns', ''), xs=[10, 20, 30, 40, 50],
             dv=('Paper clips held', 'clips'), f=lambda x: 0.45 * x, dp=0, trend='The number of clips held increases roughly in proportion to the number of turns.',
             why='Each turn adds to the magnetic field; the field of a solenoid is proportional to the number of turns per unit length × current, and the iron core magnifies it.'),
        dict(intro='{who} changed the current through a 30-turn coil wound on an iron nail and counted the steel paper clips it could hold.', iv=('Current', 'A'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Paper clips held', 'clips'), f=lambda x: 6 * x, dp=0, trend='The number of clips held increases as the current increases, roughly in proportion.',
             why='A larger current produces a stronger magnetic field around each turn, which magnetises the iron core more strongly.'))

inquiry('ch12-st2',
        dict(ctx='how the number of turns on an electromagnet affects its strength',
             iv='number of turns of wire (10, 20, 30, 40, 50)', dv='strength – number of identical steel paper clips picked up (or force on a newton meter / reading on a magnetometer)',
             cvs=[('current (set with a variable resistor and checked on an ammeter)', 'a larger current makes a stronger field'), ('the same iron nail core', 'core material affects strength'), ('type of paper clip', 'mass and steel type'), ('time the current flows', 'the wire heats up and resistance changes')],
             hyp='If the number of turns increases, then the electromagnet will pick up more clips, because each turn adds to the magnetic field, making it stronger.',
             method='Wind 10 turns of insulated wire around an iron nail; connect to a low-voltage supply, ammeter and variable resistor; set 1.0 A; dip into a tray of clips and lift; count clips; switch off between trials; repeat 3 times; repeat with 20-50 turns.',
             weak=('the current was not checked and fell as the wire warmed', 'monitor the ammeter and adjust the variable resistor to keep the current at 1.0 A, switching off between trials'),
             safety='the wire can become hot – use low voltage and switch off between readings'))

R.facts('ch12-st3', F(
    terms=[('motor effect', 'the force on a current-carrying conductor placed in a magnetic field'),
           ('Fleming’s left-hand rule', 'a rule for the direction of the force: First finger = Field, seCond finger = Current, thuMb = Motion (force)'),
           ('commutator', 'a split-ring in a DC motor that reverses the current in the coil every half turn so it keeps rotating in the same direction'),
           ('brushes', 'carbon contacts that press against the commutator and connect the rotating coil to the power supply')],
    facts=[('Which change would reverse the direction of rotation of a DC motor?', 'Reversing the current', ['Increasing the current', 'Adding more turns', 'Using a stronger magnet'], 'Reversing current (or field) reverses the force.'),
           ('What is the purpose of the split-ring commutator?', 'To reverse the current in the coil every half turn', ['To increase the voltage', 'To stop the coil overheating', 'To make the field stronger'], 'This keeps the turning effect in one direction.'),
           ('When is the force on a wire in a magnetic field zero?', 'When the wire is parallel to the field lines', ['When the wire is at 90° to the field', 'When the current is large', 'When the magnet is strong'], 'Force is greatest at 90° and zero when parallel.')],
    why=[('Explain why a current-carrying wire in a magnetic field experiences a force.', 'The current produces its own magnetic field around the wire; this interacts with the permanent magnet’s field, producing a force on the wire.'),
         ('Explain how a simple DC motor keeps turning in the same direction.', 'Forces on opposite sides of the coil act in opposite directions, creating a turning effect; the split-ring commutator reverses the current every half turn, so the forces keep turning the coil the same way.'),
         ('Explain three ways to make a DC motor spin faster.', 'Increase the current (higher voltage), use a stronger magnet, or use more turns of wire on the coil – each increases the force on the coil.')],
    contrast=[('the motor effect', 'electromagnetic induction', 'The motor effect: current + magnetic field → force/motion (motors, loudspeakers); induction: motion + magnetic field → induced voltage/current (generators, microphones).')],
    misc=[('In Fleming’s left-hand rule, the thumb shows the direction of the current.', 'The thumb shows motion (force); the second finger shows current and the first finger shows field.'),
          ('A DC motor needs a commutator because the current would otherwise stop.', 'Without a commutator the current would keep flowing but the coil would only rock back and forth, because the forces would reverse their turning effect every half turn.')],
    cases=[('electric bicycles in cities such as Amsterdam and Shenzhen', 'Hub motors use the motor effect: current in coils inside a ring of permanent magnets produces a force that turns the wheel.', 'the motor effect', 'Current-carrying coils in a magnetic field experience forces that create a turning effect.'),
           ('Michael Faraday’s first motor (1821)', 'A wire carrying current hung into a dish of mercury with a magnet in the middle; the wire rotated continuously around the magnet.', 'the motor effect', 'The magnetic field of the current interacted with the magnet’s field, giving a continuous force on the wire.')],
    evaluate=[('Replacing petrol engines with electric motors in all vehicles would solve urban pollution.', ['no exhaust emissions in cities, quieter streets', 'motors are about 90% efficient'], ['brake and tyre particles still pollute', 'electricity may be generated from fossil fuels elsewhere', 'battery production has environmental costs'], 'Electric motors greatly reduce urban air pollution but do not eliminate it; the overall benefit depends on clean electricity and battery recycling.')],
    extended=[('A wire 0.050 m long carries a current of 3.0 A at right angles to a magnetic field of 0.20 T. (a) Use F = BIL to calculate the force. (b) State two ways to double the force. (c) Use Fleming’s left-hand rule to explain how you would find the direction of the force.', '(a) F = 0.20 × 3.0 × 0.050 = 0.030 N (b) double the current; double the field strength; double the length in the field (c) first finger along field (N→S), second along current, thumb gives force direction, at 90° to both.', 5)],
))


@R.add('ch12-st3', 'C3', (1, 5), 'numerical')
def bil(rng, slot):
    B = rng.choice([0.05, 0.10, 0.15, 0.20, 0.40, 0.50])
    I = rng.choice([0.5, 1.5, 2.0, 2.5, 3.0, 4.0])
    L = rng.choice([0.04, 0.05, 0.08, 0.10, 0.25])
    F_ = B * I * L
    k = rng.choice(['F', 'I', 'B'] if slot.d >= 3 else ['F'])
    if k == 'F':
        return dict(stem=f'A wire of length {L} m carrying {I} A lies at right angles to a magnetic field of {B} T. Calculate the force on the wire (F = BIL).', answer=f'{F_:.3g} N', markingKey=f'M1 F = {B} × {I} × {L}; A1 {F_:.3g} N.', marks=2)
    if k == 'I':
        return dict(stem=f'A force of {F_:.3g} N acts on a {L} m length of wire at right angles to a {B} T field. Calculate the current in the wire.', answer=f'{I:g} A', markingKey=f'M1 I = F/(BL) = {F_:.3g}/({B} × {L}); A1 {I:g} A.', marks=2)
    return dict(stem=f'In a motor-effect experiment a {L} m wire carrying {I} A at right angles to a magnetic field experiences a force of {F_:.3g} N on a top-pan balance. Calculate the magnetic flux density.', answer=f'{B:g} T',
                markingKey=f'M1 B = F/(IL); A1 {B:g} T.', marks=2)


@R.add('ch12-st3', 'C3', (2, 4), 'short')
def flhr(rng, slot):
    dirs = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east', 'up': 'down', 'down': 'up'}
    # field, current, force triples in a right-handed set (Fleming LH rule: F = I × B)
    sets = [('east', 'north', 'down'), ('north', 'east', 'up'), ('up', 'east', 'south'), ('east', 'up', 'north'), ('north', 'up', 'west'), ('up', 'north', 'east')]
    fld, cur, frc = rng.choice(sets)
    flip = rng.random() < 0.4
    if flip:
        cur = dirs[cur]
        frc = dirs[frc]
    return dict(stem=f'A straight wire carries current towards the {cur if cur not in ("up", "down") else ("ceiling" if cur == "up" else "floor")}, in a magnetic field pointing {fld if fld not in ("up", "down") else ("upwards" if fld == "up" else "downwards")}. Use Fleming’s left-hand rule to state the direction of the force on the wire.',
                answer=f'{frc if frc not in ("up", "down") else ("upwards" if frc == "up" else "downwards")}',
                markingKey=f'1 first finger along the field ({fld}), second finger along the current ({cur}); 1 thumb gives force: {frc}.', marks=2)


inquiry('ch12-st3',
        dict(ctx='how the current through a wire affects the force on it in a magnetic field (the motor effect), measured with a top-pan balance',
             iv='current through the wire (0.5 to 3.0 A, set with a variable resistor)', dv='force on the wire – change in balance reading (g) converted to newtons',
             cvs=[('length of wire in the field', 'force depends on length (F = BIL)'), ('the same pair of magnets and spacing', 'field strength'), ('angle of wire to field (90°)', 'force depends on angle'), ('zeroing the balance', 'readings must show only the magnetic force')],
             hyp='If the current increases, then the force will increase in direct proportion, because F = BIL with B and L constant.',
             method='Place a U-shaped magnet on a top-pan balance and zero it; clamp a stiff copper rod horizontally between the poles, not touching; pass 0.5, 1.0 … 3.0 A through the rod; record the change in reading; force = Δm × 9.8 (Δm in kg); repeat 3 times; plot force against current.',
             weak=('the current was left on for minutes and the rod became hot', 'switch on only while taking each reading so the resistance and current stay steady'),
             safety='the rod can become hot; use a low-voltage supply'))

R.facts('ch12-st4', F(
    terms=[('relay', 'an electromagnetic switch in which a small current in one circuit operates an electromagnet that switches on a larger current in a second circuit'),
           ('electric bell', 'a device in which an electromagnet repeatedly attracts a soft iron armature, breaking the circuit each time, so the hammer strikes a gong'),
           ('loudspeaker', 'a device in which an alternating current in a coil in a permanent magnet’s field makes a cone vibrate, producing sound'),
           ('armature', 'the soft iron part that is attracted by an electromagnet and moves to open or close contacts')],
    facts=[('Why is a relay used to switch on a car’s starter motor?', 'A small current from the ignition switch safely controls a very large current', ['To increase the voltage of the battery', 'To store charge', 'To make the motor spin backwards'], 'Thin wires and the driver are protected from the large current.'),
           ('In an electric bell, what makes the hammer move back after striking the gong?', 'The circuit breaks so the electromagnet switches off and a spring pulls the armature back', ['The gong pushes it back with magnetism', 'The current reverses', 'Gravity'], 'Make-and-break contacts repeat the cycle.'),
           ('What makes the cone of a loudspeaker vibrate?', 'An alternating current in the coil in a magnetic field', ['A direct current in the cone', 'Air pressure from the amplifier', 'A spring alone'], 'Motor effect with changing current direction.'),
           ('What determines the pitch of the sound from a loudspeaker?', 'The frequency of the alternating current', ['The size of the current only', 'The strength of the magnet', 'The colour of the cone'], 'The cone vibrates at the frequency of the current.')],
    why=[('Explain how a relay works.', 'A small current flows through the relay coil, making it an electromagnet; this attracts an iron armature, which closes contacts in a second circuit, switching on a large current.'),
         ('Explain how a loudspeaker produces sound.', 'An alternating current flows in a coil in the field of a permanent magnet; the motor effect gives a force that reverses with the current, so the coil and attached cone vibrate, producing pressure waves in the air.'),
         ('Explain why the core of a relay must be soft iron.', 'Soft iron magnetises when current flows and loses its magnetism quickly when the current stops, so the armature is released and the contacts open again.')],
    contrast=[('a relay', 'an ordinary switch', 'An ordinary switch is operated by hand and carries the full current; a relay is operated by a small current in its coil and switches a separate, larger current.'),
              ('a loudspeaker', 'a microphone', 'A loudspeaker turns electrical signals into sound using the motor effect; a moving-coil microphone turns sound into electrical signals using electromagnetic induction.')],
    misc=[('In a relay the large current flows through the electromagnet coil.', 'Only the small control current flows through the coil; the large current flows in the separate switched circuit.'),
          ('A louder sound from a loudspeaker means the current has a higher frequency.', 'Louder means a larger amplitude of current (bigger vibrations); higher frequency gives higher pitch.')],
    cases=[('railway signalling interlocks', 'For decades, banks of relays ensured that conflicting signals could not show green at the same time.', 'relays as switches', 'Small control currents operated relays that safely switched signal lamps and points, and wiring between relays prevented dangerous combinations.'),
           ('hearing-aid and headphone drivers', 'Tiny moving-coil drivers convert audio signals into sound close to the ear.', 'the loudspeaker principle', 'A varying current in a small coil in a magnetic field vibrates a diaphragm at the frequency of the signal.')],
    evaluate=[('Electromagnetic relays should be replaced by electronic (solid-state) switches in all devices.', ['no moving parts so no wear or sparking', 'faster switching and silent', 'smaller'], ['relays give complete electrical isolation between circuits', 'relays handle surges and high currents well and are cheap', 'easy to see and test'], 'Solid-state switches are better for many low-power and fast uses, but relays remain useful where isolation and high currents matter.')],
    extended=[('A greenhouse fan (230 V, 5 A) must switch on automatically when a 6 V temperature-sensing circuit detects high temperature. Explain, with a labelled circuit description, how a relay allows this, and give two safety advantages of using a relay.', 'The sensing circuit (thermistor, 6 V) switches current through the relay coil; the coil becomes an electromagnet, attracts the armature and closes contacts in the separate 230 V fan circuit. Advantages: the low-voltage circuit is electrically isolated from mains; small, safe currents in the control wires; the user never touches the mains circuit.', 6, 'long'),
              ('Explain how an electric bell works, describing the role of the electromagnet, armature, spring and contact screw, and explain why it rings continuously while the switch is pressed.', 'Current flows through the coil, making an electromagnet that attracts the soft iron armature; the hammer strikes the gong; the movement separates the contact screw, breaking the circuit; the electromagnet switches off and the spring pulls the armature back, remaking contact; the cycle repeats rapidly while the switch is closed.', 5)],
))

dataset('ch12-st4',
        dict(intro='{who} connected a loudspeaker to a signal generator and measured the amplitude of vibration of the cone (with a laser and ruler) at different input voltages, keeping the frequency at 50 Hz.', iv=('Input voltage', 'V'), xs=[1, 2, 3, 4, 5],
             dv=('Cone amplitude', 'mm'), f=lambda x: 0.6 * x, dp=1, trend='The amplitude of the cone’s vibration increases in proportion to the input voltage.',
             why='A larger voltage gives a larger current in the coil, so the motor-effect force is larger and the cone moves further, producing a louder sound.'))

inquiry('ch12-st4',
        dict(ctx='how the frequency of the signal sent to a loudspeaker affects the loudness of the sound produced at a fixed input voltage',
             iv='frequency set on a signal generator (100, 250, 500, 1000, 2000, 5000 Hz)', dv='sound level in dB measured 1.0 m in front of the speaker with a sound-level meter app',
             cvs=[('input voltage/amplitude', 'larger amplitude gives louder sound'), ('distance and direction of the meter', 'sound level falls with distance'), ('background noise', 'adds to readings'), ('the same speaker and phone', 'devices respond differently')],
             hyp='If the frequency changes, then the loudness will vary, being greatest in the middle of the speaker’s range (about 500-2000 Hz), because a speaker cone responds best near its designed frequency range.',
             method='Place the speaker on a table 1.0 m from a phone on a stand in a quiet room; set the generator to 2 V; record the dB reading at each frequency after 5 s; repeat 3 times; subtract background level; plot dB against frequency (log scale).',
             safety='keep the volume moderate; avoid holding the meter near ears at high frequency'))


# =============================================================================================
# Extra criterion D (reflecting on the impacts of science) and extended items
# =============================================================================================
def _ev(key, *items):
    R.f[key].evaluate = list(R.f[key].evaluate) + list(items)


def _ex(key, *items):
    R.f[key].extended = list(R.f[key].extended) + list(items)


_ev('ch01-st3', ('IVF clinics should be allowed to screen embryos for chromosome abnormalities caused by errors in meiosis.', ['reduces miscarriage and serious conditions from non-disjunction', 'helps older parents, whose risk of meiotic errors is higher'], ['some screened conditions (e.g. Down syndrome) are compatible with fulfilling lives – disability-rights concerns', 'embryos are discarded', 'costly and not available to all'], 'Screening for serious, life-limiting conditions is widely accepted; screening for other conditions is a matter of ongoing ethical debate.'))
_ex('ch01-st3', ('Compare mitosis and meiosis in a table covering: number of divisions, number of daughter cells, chromosome number of daughter cells, genetic similarity, and where each occurs in humans. Then explain why both processes are needed in the life cycle of a human.', 'Mitosis: 1 division, 2 cells, diploid (46), identical, body tissues. Meiosis: 2 divisions, 4 cells, haploid (23), genetically different, testes/ovaries. Meiosis makes gametes so fertilisation restores 46; mitosis then grows the zygote into a body of identical cells and repairs tissue.', 6, 'long'))
_ev('ch02-st1', ('Genetic modification of crops to add useful dominant alleles (e.g. Bt maize, Golden Rice) should be encouraged.', ['increases yields and reduces pesticide use (Bt crops)', 'Golden Rice provides vitamin A where deficiency causes blindness'], ['possible spread of genes to wild relatives', 'seed patents increase farmer dependence on companies', 'public distrust and labelling issues'], 'GM crops can bring large benefits when they are well regulated and accessible to small farmers.'))
_ex('ch02-st1', ('A guinea pig with black fur (B dominant to b, white) may be BB or Bb. Design a breeding test to find its genotype, predicting the offspring for each possibility with Punnett squares, and explain how many offspring you would need before you could be confident of the result.', 'Cross with bb (white). If BB: all offspring Bb – black. If Bb: 1/2 black, 1/2 white. One white offspring proves Bb. If, e.g., 8 offspring are all black, the probability of this from Bb is (1/2)⁸ ≈ 0.4%, so BB is very likely; more offspring increase confidence.', 6))
_ev('ch02-st3', ('Gene therapy for haemophilia, costing over US$2 million per patient, should be funded by public health systems.', ['a single treatment can replace a lifetime of expensive clotting-factor injections', 'greatly improves quality of life'], ['very high upfront cost limits other healthcare spending', 'long-term safety and durability not yet known', 'unequal access between rich and poor countries'], 'It can be cost-effective over a lifetime, but funding decisions must weigh long-term evidence and fairness of access.'))
_ex('ch02-st3', ('A woman whose father had haemophilia marries a man without haemophilia. (a) Deduce the woman’s genotype and explain how you know. (b) Draw a Punnett square for their children. (c) State the probability that a son will have haemophilia and that a daughter will be a carrier.', '(a) XᴴXʰ – her father gave her his only X, which carried Xʰ, but she is unaffected. (b) XᴴXʰ × XᴴY → XᴴXᴴ, XᴴY, XʰXᴴ, XʰY. (c) son affected 1/2; daughter carrier 1/2.', 5))
_ev('ch02-st5', ('Human height is mainly determined by genes, so government nutrition programmes cannot make a population taller.', ['twin studies show height is highly heritable (about 80%)'], ['average heights in South Korea and the Netherlands rose by 10-20 cm in a century with better nutrition and health', 'heritability applies within a population in a given environment, not to changes in environment'], 'Genes set the potential, but nutrition and health strongly affect whether it is reached, so programmes can increase average height.'))
_ex('ch02-st5', ('A class measured the heights of 30 students and the blood groups of the same students. Explain which type of graph should be used for each data set, describe the expected shape of the height graph, and explain the causes of the variation in each characteristic.', 'Height: continuous – histogram with grouped classes; roughly normal (bell-shaped) distribution; caused by many genes plus environment (diet, health). Blood group: discontinuous – bar chart with gaps; four categories; caused by a single gene with three alleles, not affected by the environment.', 6, 'long'))
_ev('ch03-st1', ('Athletes should be allowed to train at altitude or sleep in altitude tents, but not to use EPO.', ['altitude training is natural adaptation: the body makes more red blood cells', 'EPO is a drug that can thicken blood dangerously and is banned by WADA'], ['both achieve the same effect on red blood cells, so the distinction is arguably arbitrary', 'altitude tents are expensive, favouring rich athletes'], 'The distinction is justified mainly by health risks and enforceability, though fairness concerns remain.'))
_ex('ch03-st1', ('Describe the general features of a negative feedback system using the control of body temperature as an example, and explain what would happen if the response continued after the set point had been reached.', 'Stimulus (temperature rises) → receptors (thermoreceptors in hypothalamus/skin) → coordination centre (hypothalamus) → effectors (sweat glands, arterioles) → response (cooling) → temperature returns to 37 °C and response stops. If it continued, temperature would overshoot below the set point (hypothermia), triggering the opposite responses – fluctuation.', 6, 'long'))
_ev('ch03-st3', ('Continuous glucose monitors and insulin pumps should be free for all people with type 1 diabetes.', ['better glucose control reduces long-term complications (blindness, kidney failure)', 'improves quality of life, especially for children'], ['expensive devices and sensors', 'not all patients can use them well without training'], 'Because complications are very costly, providing devices is often cost-effective; access should include training.'))
_ev('ch03-st2', ('Brain–computer interfaces (implants that read neurone signals) should be developed to help people with paralysis.', ['can restore communication and movement (e.g. controlling a cursor or robotic arm)', 'improve independence'], ['surgical risks and infection', 'privacy of neural data', 'high cost; long-term effects unknown'], 'The benefits for people with severe paralysis are significant, but strict ethical oversight and data protection are essential.'))
_ev('ch04-st1', ('Building particle accelerators such as the Large Hadron Collider is a good use of public money.', ['fundamental discoveries (e.g. the Higgs boson, 2012)', 'spin-off technology: the World Wide Web, medical imaging, cancer proton therapy', 'international scientific cooperation'], ['very high cost (billions of euros)', 'no immediate practical benefit from many discoveries', 'money could fund medicine or climate research'], 'Fundamental research has historically produced unexpected benefits, so moderate public funding is justified, though priorities must be debated openly.'))
_ev('ch04-st5', ('Scientists should always share their data openly, as Rosalind Franklin’s data was shared (without her knowledge) with Watson and Crick.', ['open data speeds up discovery', 'others can check results'], ['scientists deserve credit for their work and must consent to sharing', 'Franklin was not properly credited at the time'], 'Open sharing is valuable but must be with consent and proper credit; the DNA story shows the harm of sharing without it.'))
_ex('ch04-st5', ('Mendeleev predicted that eka-aluminium would have a relative atomic mass of about 68, a density of about 5.9 g/cm³ and a low melting point. Gallium, discovered in 1875, has Aᵣ 69.7, density 5.91 g/cm³ and melts at 30 °C. Evaluate how well this supports Mendeleev’s periodic table and explain why scientists value successful predictions.', 'Very close agreement (mass within 3%, density almost exact, low melting point correct) strongly supports the periodic table, because Mendeleev made the prediction before the element was known; a model that predicts new results is more convincing than one that only fits known data.', 5))
_ev('ch05-st3', ('Synthetic diamonds grown in laboratories are better than mined diamonds.', ['same structure and properties as natural diamond', 'avoid mining damage and “conflict diamonds”', 'cheaper'], ['growing them uses a lot of energy (often from fossil fuels)', 'mining supports jobs in countries such as Botswana', 'some buyers value natural rarity'], 'Lab-grown diamonds are chemically identical and usually more ethical, especially if made with renewable energy, but mining communities’ economies must be considered.'))
_ex('ch05-st3', ('Graphite and diamond are both pure carbon. Use their structures to explain why graphite is used for electrodes and pencil “leads” but diamond is used for cutting tools and drill tips.', 'Graphite: each C bonded to 3 others in hexagonal layers; one delocalised electron per atom conducts electricity (electrodes); weak forces between layers let them slide (pencils). Diamond: each C bonded to 4 others in a rigid 3D giant covalent lattice; many strong bonds make it extremely hard (cutting tools) with a very high melting point.', 6, 'long'))
_ev('ch05-st4', ('Steel should be replaced by aluminium alloys in car manufacture.', ['aluminium is about one-third the density, reducing mass and fuel use', 'resists corrosion'], ['more expensive and energy-intensive to extract', 'harder to repair', 'steel is strong, cheap and highly recycled'], 'Aluminium makes sense where mass savings matter (EVs, premium cars) especially with recycled aluminium; steel remains cost-effective for many vehicles.'))
_ex('ch05-st4', ('Explain, using diagrams of the arrangement of particles, why pure copper is soft and malleable but brass (copper with zinc) is harder, and explain why both conduct electricity.', 'Pure copper: identical ions in regular layers that slide easily over each other when a force is applied – soft and malleable. Brass: larger zinc atoms disrupt the layers so they cannot slide as easily – harder. Both have a sea of delocalised electrons that can move through the structure, so both conduct.', 5))
_ev('ch06-st2', ('Making products by precipitation reactions in industry is environmentally acceptable.', ['simple, low-temperature reactions use little energy', 'insoluble products are easy to separate'], ['produce large volumes of waste solution (e.g. dissolved nitrates) that must be treated', 'some precipitates (lead, barium salts) are toxic'], 'Acceptable when waste solutions are treated and toxic materials are handled safely.'))
_ev('ch06-st3', ('Phytomining (using plants to extract metals such as nickel or copper from low-grade soil) should replace traditional mining.', ['can recover metal from waste land and low-grade ores', 'cleans up contaminated land', 'less landscape damage'], ['very slow (years per harvest)', 'yields are small compared with demand', 'the plants must still be burned and the metal extracted by electrolysis or displacement'], 'It is a useful supplement for low-grade ores and land remediation but cannot replace mining at current demand.'))
_ev('ch07-st1', ('Schools should use computer simulations instead of real rate-of-reaction experiments.', ['no chemical hazards or waste', 'can run many trials quickly', 'cheaper'], ['students do not develop practical skills or see real errors and anomalies', 'simulations only show what the model assumes'], 'Simulations are a useful supplement but real experiments are essential for learning to inquire and evaluate.'))
_ex('ch07-st1', ('Compare the gas-syringe method and the mass-loss method for measuring the rate of reaction between calcium carbonate and hydrochloric acid. For each, describe the method, state the units of rate, and give one advantage and one limitation.', 'Gas syringe: collect CO₂ volume at time intervals; rate in cm³/s; advantage – direct, sensitive volume measurement; limitation – syringe can stick, gas escapes before bung inserted. Mass loss: flask on balance, record mass every 30 s; rate in g/s; advantage – simple, continuous readings; limitation – small mass changes, needs a dense gas, unsuitable for H₂.', 6, 'long'))
_ev('ch08-st1', ('Self-driving cars will make roads safer.', ['sensors react faster than humans and do not get tired, drunk or distracted', 'can measure speeds and distances precisely'], ['software errors and sensor failures have caused fatal crashes', 'difficult ethical decisions in unavoidable collisions', 'cyber-security risks'], 'They could reduce human-error crashes significantly, but only with strong testing, regulation and security.'))
_ex('ch08-st1', ('A plane flies 600 km north and then 800 km east in a total time of 2.5 h. (a) Calculate the total distance and the displacement (magnitude and bearing). (b) Calculate the average speed and the average velocity. (c) Explain why the two answers to (b) are different.', '(a) distance 1400 km; displacement √(600² + 800²) = 1000 km on a bearing of 053°. (b) average speed 560 km/h; average velocity 400 km/h on bearing 053°. (c) Speed uses total path length (scalar); velocity uses straight-line displacement with a direction (vector).', 6))
_ev('ch09-st2', ('Speed limiters should be fitted to all new cars.', ['speed is a major factor in crash severity; F = ma means faster crashes need larger forces to stop', 'EU rules require intelligent speed assistance in new cars since 2024'], ['drivers may need extra speed to overtake safely', 'GPS speed-limit data can be wrong', 'reduces personal freedom'], 'Limiters that can be overridden briefly balance safety and practicality.'))
_ev('ch09-st4', ('Cyclists should always be required to wear helmets.', ['helmets reduce the force on the head by increasing the stopping time and spreading the impact', 'reduce serious head injuries'], ['compulsory laws may reduce cycling, harming public health', 'separated cycle lanes reduce crashes more', 'helmets do not protect against all injuries'], 'Helmets clearly protect individuals; whether laws should require them depends on balancing safety with encouraging cycling.'))
_ev('ch09-st5', ('Car manufacturers should make vehicles that protect pedestrians as well as passengers.', ['softer bonnets, pop-up bonnets and external airbags increase the time of impact for pedestrians, reducing force', 'pedestrians and cyclists are a large share of road deaths'], ['adds cost and weight', 'large SUVs with high fronts are popular but more dangerous to pedestrians'], 'Vehicle design should consider all road users; regulation (e.g. Euro NCAP pedestrian ratings) encourages this.'))
_ex('ch09-st5', ('Using ideas about momentum and force, explain how crumple zones, seat belts and airbags work together to reduce injuries in a 50 km/h crash, and suggest why a passenger without a seat belt in the back seat endangers people in the front.', 'In a crash the car and occupants must lose all their momentum; F = Δp ÷ t, so increasing the stopping time reduces force. Crumple zones deform, extending the car’s stopping time; seat belts stretch slightly and hold passengers to the decelerating car; airbags cushion the head over a longer time and larger area. An unbelted rear passenger keeps moving (first law) and hits front occupants with a large force.', 6, 'long'))
_ev('ch10-st4', ('Coastal defences such as sea walls are the best way to protect towns from wave erosion.', ['protect homes and infrastructure immediately', 'reflect wave energy'], ['reflected waves can increase erosion at the base and neighbouring beaches', 'very expensive to build and maintain', 'beach nourishment, offshore reefs and managed retreat may be more sustainable'], 'Sea walls protect high-value areas but can move the problem elsewhere; integrated coastal management is usually better.'))
_ev('ch11-st1', ('Mirrors on roads and in shops (convex safety mirrors) should be used more widely instead of cameras.', ['no power needed, cheap and reliable', 'show a wide field of view to drivers at blind junctions'], ['images are small and distances are hard to judge', 'cameras can record evidence and be monitored remotely'], 'Mirrors are a cheap safety aid at junctions; cameras serve different purposes such as recording.'))
_ev('ch11-st4', ('Ultrasound should replace X-rays wherever possible in medical imaging.', ['non-ionising, so safe for fetuses and repeated scans', 'real-time moving images; portable and cheaper'], ['cannot image well through bone or air (lungs)', 'image quality depends on operator skill'], 'Ultrasound should be used where it gives adequate images, especially in pregnancy, but X-rays remain necessary for bones and lungs.'))
_ex('ch11-st4', ('A fishing boat’s sonar sends a pulse and receives two echoes: one after 0.020 s from a shoal of fish and one after 0.12 s from the sea bed. The speed of sound in sea water is 1500 m/s. (a) Calculate the depth of the fish and of the sea bed. (b) Explain why sonar uses ultrasound rather than audible sound. (c) Discuss one environmental concern about high-intensity sonar.', '(a) fish 1500 × 0.020 ÷ 2 = 15 m; sea bed 1500 × 0.12 ÷ 2 = 90 m. (b) Short wavelength gives detailed images of small objects and the beam can be directed; does not disturb people. (c) Powerful military sonar has been linked to whale and dolphin strandings because it interferes with their echolocation and hearing.', 6))
_ev('ch12-st1', ('Magnetic levitation and strong magnets in consumer products (e.g. magnetic toys) pose too great a risk to children.', ['swallowed powerful magnets can attract through the intestine walls, causing serious injury', 'magnets can damage pacemakers and cards'], ['magnets are very useful and widely safe when used properly', 'labelling and size rules reduce risk'], 'Strong small magnets in toys need strict regulation, but magnets in general are safe and beneficial.'))
_ev('ch12-st3', ('Electric motors should replace internal combustion engines in all public buses within ten years.', ['zero tailpipe emissions improve urban air quality (e.g. Shenzhen’s fully electric fleet)', 'lower running and maintenance costs'], ['high purchase cost and charging infrastructure', 'battery supply chains and range in cold climates', 'electricity may come from fossil fuels'], 'Rapid electrification is achievable in many cities with investment, as Shenzhen shows, but timelines depend on funding and grid capacity.'))
_ex('ch12-st3', ('Describe how a simple DC motor works, referring to the coil, magnets, split-ring commutator and brushes. Explain why the motor would only rock back and forth without the commutator, and state two ways to reverse the direction of rotation.', 'Current flows through the coil via brushes and commutator; the motor effect produces upward force on one side and downward force on the other, creating a turning effect. Every half turn the commutator reverses the current so forces keep turning the coil the same way. Without it, after half a turn the forces would turn it back, so it would oscillate. Reverse the current or reverse the magnetic field (swap the magnets).', 6, 'long'))
_ev('ch12-st4', ('Wireless charging using electromagnetic coils is a good replacement for charging cables.', ['convenient, no wear on connectors', 'can be sealed for waterproof devices'], ['less efficient – more energy wasted as heat', 'slower charging', 'extra devices and materials'], 'Wireless charging is convenient but less efficient; cables remain better for energy use.'))


# =============================================================================================
# Extra criterion B/C tasks so every subtopic has inquiry and data items (used by mock Tasks 3-4)
# =============================================================================================
dataset('ch01-st1',
        dict(intro='{who} extracted DNA from 50 g samples of strawberries using different volumes of washing-up liquid and weighed the DNA collected.', iv=('Volume of washing-up liquid', 'cm³'), xs=[2, 4, 6, 8, 10],
             dv=('Mass of DNA', 'g'), f=lambda x: 0.60 * x / (x + 3), dp=2, trend='The mass of DNA increases with the volume of detergent but levels off above about 6-8 cm³.',
             why='Detergent breaks down the lipid cell and nuclear membranes, releasing DNA; once all the membranes are broken, extra detergent releases no more DNA.'))
dataset('ch02-st1',
        dict(intro='{who} germinated 100 maize seeds from an Aa × Aa cross (A = green, a = albino) in each of three trays at different light intensities and recorded the percentage of albino seedlings.', iv=('Light intensity', 'klux'), xs=[2, 4, 6, 8, 10],
             dv=('Albino seedlings', '%'), f=lambda x: 25.0, dp=0, trend='The percentage of albino seedlings stays close to 25% at every light intensity – there is no trend.',
             why='Albinism is determined by genotype (aa), which occurs in 1/4 of offspring of Aa × Aa; light intensity is environmental and does not change the genotype ratio.'))
dataset('ch02-st2',
        dict(intro='{who} modelled a monohybrid cross by drawing pairs of beads (one from each of two bags containing equal numbers of A and a beads) and calculated the ratio of dominant to recessive phenotypes for different numbers of draws.', iv=('Number of draws', ''), xs=[40, 80, 120, 160, 200],
             dv=('Dominant : recessive ratio', 'x : 1'), f=lambda x: 3.0, dp=2, trend='The ratio is close to 3 : 1 for every sample size, with the spread of repeats getting smaller for larger samples.',
             why='Each pair is a random combination of two gametes from heterozygous parents, so 3/4 show the dominant phenotype; chance variation has less effect in larger samples.'))
dataset('ch02-st5',
        dict(intro='{who} measured the length of ivy leaves (30 leaves per site) at sites with different light intensities.', iv=('Light intensity', 'klux'), xs=[2, 5, 10, 20, 40],
             dv=('Mean leaf length', 'mm'), f=lambda x: 78 - 9 * math.log(x), dp=1, trend='Mean leaf length decreases as light intensity increases.',
             why='This is environmental variation: in shade, larger leaves absorb more of the limited light for photosynthesis.'))
dataset('ch04-st1',
        dict(intro='{who} used a Geiger counter (with the background count subtracted) to measure the count rate from a beta source (beta particles are high-speed electrons emitted from the nucleus) through different thicknesses of aluminium.', iv=('Aluminium thickness', 'mm'), xs=[0.0, 0.5, 1.0, 1.5, 2.0],
             dv=('Count rate', 'counts per minute'), f=lambda x: 900 * math.exp(-1.4 * x), dp=0, trend='The count rate decreases as the thickness of aluminium increases, falling by roughly half for each 0.5 mm.',
             why='Beta particles are electrons that interact with the atoms of aluminium and are gradually absorbed; a few millimetres of aluminium stop almost all of them.'))
dataset('ch04-st2',
        dict(intro='{who} measured the count rate of a sample of the radioisotope protactinium-234 at intervals (background subtracted).', iv=('Time', 's'), xs=[0, 60, 120, 180, 240],
             dv=('Count rate', 'counts per 10 s'), f=lambda x: 400 * 0.5 ** (x / 70), dp=0, trend='The count rate halves about every 70 s – the half-life is about 70 s.',
             why='Radioactive decay is random but each unstable nucleus has the same probability of decaying per second, so the number remaining (and the count rate) halves in equal time intervals.'))
dataset('ch04-st3',
        dict(intro='{who} compared published values (from three data books) of the atomic radius of group 1 elements.', iv=('Number of occupied shells', ''), xs=[2, 3, 4, 5],
             dv=('Atomic radius', 'pm'), f=lambda x: {2: 152, 3: 186, 4: 227, 5: 248}[x], dp=0, trend='Atomic radius increases as the number of occupied electron shells increases.',
             why='Each extra shell places the outer electron further from the nucleus; inner shells shield it, which is also why reactivity increases down group 1.'))
dataset('ch04-st5',
        dict(intro='In a simulation of the Geiger–Marsden gold foil experiment, {who} counted the alpha particles detected per minute at different scattering angles.', iv=('Scattering angle', '°'), xs=[15, 30, 45, 60, 90],
             dv=('Alpha particles detected', 'per minute'), f=lambda x: 1.25 / math.sin(math.radians(x / 2)) ** 4, dp=0, trend='The number of alpha particles detected falls very steeply as the scattering angle increases; very few are scattered through large angles.',
             why='Most alpha particles pass far from any nucleus and are hardly deflected; only those passing very close to the tiny, dense, positive nucleus are scattered through large angles – evidence for the nuclear model.'))
dataset('ch05-st3',
        dict(intro='{who} collected boiling-point data (three sources) for the first five straight-chain alkanes, which are simple molecular substances.', iv=('Number of carbon atoms', ''), xs=[1, 2, 3, 4, 5],
             dv=('Boiling point', 'K'), f=lambda x: {1: 112, 2: 185, 3: 231, 4: 273, 5: 309}[x], dp=0, trend='Boiling point increases as the number of carbon atoms increases.',
             why='Larger molecules have stronger intermolecular forces between them, so more energy is needed to separate them; the covalent bonds inside the molecules are not broken.'))
dataset('ch06-st1',
        dict(intro='{who} heated different masses of magnesium ribbon in a lidded crucible until there was no further change and weighed the magnesium oxide formed.', iv=('Mass of magnesium', 'g'), xs=[0.12, 0.24, 0.36, 0.48, 0.60],
             dv=('Mass of magnesium oxide', 'g'), f=lambda x: x * 40 / 24, dp=2, trend='The mass of magnesium oxide increases in direct proportion to the mass of magnesium, and is always greater than it.',
             why='Magnesium combines with oxygen from the air (2Mg + O₂ → 2MgO); the extra mass is the oxygen gained – mass is conserved and the ratio is fixed by the equation (24 g Mg → 40 g MgO).'))
dataset('ch06-st2',
        dict(intro='{who} heated different masses of calcium carbonate strongly in a crucible (thermal decomposition) and measured the mass lost.', iv=('Mass of calcium carbonate', 'g'), xs=[1.0, 2.0, 3.0, 4.0, 5.0],
             dv=('Mass lost', 'g'), f=lambda x: x * 44 / 100, dp=2, trend='The mass lost increases in proportion to the mass of calcium carbonate heated (about 44% of the starting mass).',
             why='CaCO₃(s) → CaO(s) + CO₂(g); the carbon dioxide gas escapes, and 100 g of CaCO₃ releases 44 g of CO₂.'))
dataset('ch06-st4',
        dict(intro='{who} heated different masses of copper(II) carbonate, CuCO₃, until it fully decomposed to copper(II) oxide, CuO, and weighed the residue. (Aᵣ: Cu = 63.5, C = 12, O = 16)', iv=('Mass of CuCO₃', 'g'), xs=[1.24, 2.47, 3.71, 4.94, 6.18],
             dv=('Mass of CuO', 'g'), f=lambda x: x * 79.5 / 123.5, dp=2, trend='The mass of copper(II) oxide is about 64% of the mass of copper(II) carbonate in every trial.',
             why='Mᵣ CuCO₃ = 123.5 and Mᵣ CuO = 79.5, so the expected fraction is 79.5/123.5 = 64.4%; lower values suggest incomplete decomposition or loss of solid.'))
dataset('ch07-st1',
        dict(intro='{who} added 0.5 g of magnesium ribbon to excess hydrochloric acid and collected the hydrogen in a gas syringe, repeating the experiment three times.', iv=('Time', 's'), xs=[20, 40, 60, 80, 100],
             dv=('Volume of hydrogen', 'cm³'), f=lambda x: 90 * (1 - math.exp(-0.025 * x)), dp=0, trend='The volume increases quickly at first and then more slowly, so the rate decreases with time.',
             why='As magnesium is used up there is less surface to react and fewer collisions per second with acid particles, so the rate falls.'))
dataset('ch07-st2',
        dict(intro='{who} dissolved different masses of ammonium nitrate in 50 cm³ of water in an insulated cup and recorded the fall in temperature.', iv=('Mass of ammonium nitrate', 'g'), xs=[1, 2, 3, 4, 5],
             dv=('Temperature fall', '°C'), f=lambda x: 2.6 * x, dp=1, trend='The temperature fall increases in proportion to the mass dissolved.',
             why='Dissolving ammonium nitrate is endothermic: energy is taken in from the water to break the ionic lattice, so more solute takes in more energy.'))
dataset('ch09-st3',
        dict(intro='{who} launched a 2 dm³ water rocket at 4 bar with different volumes of water and estimated the maximum height using angle measurements.', iv=('Volume of water', 'cm³'), xs=[200, 400, 600, 800, 1000],
             dv=('Maximum height', 'm'), f=lambda x: 30 - 0.00006 * (x - 550) ** 2, dp=1, trend='Height increases with water volume up to about 600 cm³, then decreases.',
             why='The rocket pushes water backwards and the water pushes it forwards (Newton’s third law); more water gives more thrust for longer, but too much leaves little compressed air and adds mass.'))
dataset('ch10-st1',
        dict(intro='{who} stretched a slinky spring along a smooth floor to different lengths and measured the speed of a longitudinal pulse by video analysis.', iv=('Stretched length', 'm'), xs=[2, 3, 4, 5, 6],
             dv=('Pulse speed', 'm/s'), f=lambda x: 1.3 * x, dp=2, trend='Pulse speed increases as the slinky is stretched further, roughly in proportion to the stretched length.',
             why='Stretching the slinky increases its tension, so each coil is pulled back more strongly and passes the compression on more quickly.'))
dataset('ch12-st3',
        dict(intro='{who} placed a magnet on a top-pan balance with a fixed copper rod between its poles and recorded the force on the rod for different currents.', iv=('Current', 'A'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Force on rod', 'mN'), f=lambda x: 12 * x, dp=1, trend='The force increases in direct proportion to the current.',
             why='F = BIL: with the field strength and length in the field constant, the force is proportional to the current (motor effect).'))

inquiry('ch04-st1',
        dict(ctx='how the number of protons in a nucleus affects the percentage of alpha particles deflected by more than 30°, using a Rutherford scattering simulation',
             iv='number of protons in the target nucleus (e.g. 20, 40, 60, 79, 92 in the simulation)', dv='percentage of 1000 alpha particles deflected by more than 30°, counted by the simulation',
             cvs=[('energy of the alpha particles', 'faster particles are deflected less'), ('number of particles fired', 'a larger sample gives a reliable percentage'), ('the same simulation settings (atom spacing, view)', 'changes the number of close approaches')],
             hyp='If the number of protons increases, then a higher percentage of alpha particles will be deflected by large angles, because a larger positive charge repels the positive alpha particles more strongly.',
             method='Open a scattering simulation; set alpha energy to a fixed value; choose nucleus with 20 protons; fire 1000 particles and record the number deflected > 30°; repeat 3 times; repeat for 40, 60, 79 and 92 protons; calculate percentages and plot against proton number.',
             weak=('only 50 particles were fired at each setting', 'fire at least 1000 particles so that rare large-angle deflections are counted reliably'),
             safety='screen breaks every 20 minutes'))
inquiry('ch04-st2',
        dict(ctx='how the number of “undecayed” dice changes with each throw, to model the half-life of a radioisotope',
             iv='number of throws (time, 0 to 10 throws)', dv='number of dice remaining after removing those showing a six (“decayed nuclei”)',
             cvs=[('starting number of dice (100)', 'a larger sample behaves more predictably'), ('type of die (fair, six-sided)', 'the probability of decay must be the same for every “nucleus”'), ('throwing method', 'dice must land randomly')],
             hyp='If the number of throws increases, then the number of dice remaining will decrease exponentially, with a constant “half-life” of about 3.8 throws, because each die has a fixed probability (1/6) of “decaying” per throw, like unstable nuclei.',
             method='Throw 100 dice into a tray; remove those showing six and record the number remaining; repeat until fewer than 5 remain; repeat the whole experiment 3 times; plot mean number remaining against throw number and read the half-life from the graph.',
             weak=('only 20 dice were used', 'use at least 100 dice (or pool class results) because random decay averages out only for large numbers'),
             safety='keep dice off the floor to avoid slips'))
inquiry('ch04-st3',
        dict(ctx='how the metal ion in a compound affects the colour of light emitted in a flame test, measured with a spectroscope',
             iv='metal ion in the chloride (lithium, sodium, potassium, calcium, copper)', dv='wavelength of the brightest emission line (nm), read from a hand spectroscope scale',
             cvs=[('clean wire loop (dipped in acid and flamed between tests)', 'contamination from another ion changes the colour'), ('the same blue Bunsen flame', 'a yellow flame adds its own colour'), ('amount of sample', 'too much sample masks colours'), ('dark background', 'faint colours are hard to see')],
             hyp='If the metal ion changes, then the wavelength of the emitted light will change, because each element has different gaps between its electron energy levels, so electrons falling back emit photons of different energies.',
             method='Dip a nichrome loop in dilute HCl and heat until no colour; dip in solid metal chloride; hold at the edge of a blue Bunsen flame; observe through a spectroscope and record the wavelength of the brightest lines; clean loop and repeat 3 times per metal.',
             weak=('the same loop was used without cleaning between samples', 'clean the loop in acid and flame it until no colour appears before each test'),
             safety='eye protection; hydrochloric acid is an irritant; tie hair back near Bunsen flames'))
inquiry('ch04-st4',
        dict(ctx='how the position of a halogen in group 17 affects whether it can displace other halogens from their salt solutions',
             iv='the halogen solution added (chlorine water, bromine water, iodine solution)', dv='whether a colour change occurs with potassium chloride, bromide and iodide solutions in a spotting tile (and with a few drops of cyclohexane to confirm the halogen formed)',
             cvs=[('number of drops of each solution', 'concentration of the colour depends on amount'), ('concentration of halide solutions', 'affects how visible the change is'), ('time before observing (e.g. 1 min)', 'some reactions take time to show'), ('white background', 'colour judgement')],
             hyp='If the halogen is higher in group 17, then it will displace the halogens below it, because reactivity decreases down the group as the atoms gain an electron less easily.',
             method='In a spotting tile, add 3 drops of each potassium halide solution to separate wells; add 3 drops of each halogen water in turn; observe after 1 minute against a white tile; record colour changes in a grid; repeat; use the results to rank reactivity.',
             weak=('the halogen waters had been stored for weeks and were very pale', 'use freshly prepared halogen solutions so colour changes are clear'),
             safety='work in a fume cupboard; chlorine and bromine are toxic – wear eye protection and gloves'))
inquiry('ch04-st5',
        dict(ctx='how the thickness of the foil affects the number of alpha particles scattered through large angles, using a gold foil experiment simulation',
             iv='thickness of the gold foil (number of atomic layers in the simulation: 1, 2, 4, 8, 16)', dv='number of alpha particles (out of 10 000) scattered through more than 90°',
             cvs=[('alpha particle energy', 'faster alphas are deflected less'), ('number of particles fired', 'sample size'), ('the same target element (gold)', 'nuclear charge affects scattering')],
             hyp='If the foil is thicker, then more alpha particles will be scattered through large angles, because each particle passes more nuclei and has more chances of a close approach to one.',
             method='In the simulation set alpha energy and gold target; fire 10 000 particles at foil thicknesses of 1-16 layers; record the counts above 90°; repeat 3 times; plot the counts against thickness.',
             safety='screen breaks every 20 minutes'))
inquiry('ch06-st1',
        dict(ctx='how the mass of magnesium burned affects the mass of magnesium oxide formed, to test the law of conservation of mass',
             iv='mass of magnesium ribbon (0.10-0.60 g, weighed to 0.01 g)', dv='mass of magnesium oxide – crucible and lid weighed before and after heating to constant mass',
             cvs=[('heating until constant mass', 'ensures all magnesium has reacted'), ('lid lifted briefly to let air in', 'oxygen is needed but smoke (MgO) must not escape'), ('the same balance', 'consistent readings'), ('clean ribbon (sanded)', 'oxide coating adds mass')],
             hyp='If the mass of magnesium increases, then the mass of magnesium oxide will increase in proportion (about 1.67 times), because atoms are conserved and 24 g of Mg combines with 16 g of O to form 40 g of MgO.',
             method='Weigh a crucible and lid; add sanded Mg ribbon and reweigh; heat strongly, lifting the lid occasionally; when no more glowing, heat for 2 more minutes; cool and weigh; reheat to constant mass; repeat for five masses; plot mass of MgO against mass of Mg.',
             weak=('the lid was removed for long periods and white smoke escaped', 'only lift the lid slightly and briefly so oxygen enters but MgO smoke does not escape'),
             safety='do not look directly at burning magnesium; hot crucibles – use tongs and a heat-proof mat'))
inquiry('ch06-st2',
        dict(ctx='how the mass of copper(II) carbonate heated affects the mass of carbon dioxide given off during thermal decomposition',
             iv='mass of copper(II) carbonate (1.0-5.0 g)', dv='mass of CO₂ lost – mass of tube and contents before and after heating to constant mass',
             cvs=[('heating time and strength (to constant mass)', 'incomplete decomposition gives less mass loss'), ('the same balance', 'consistent readings'), ('dry sample', 'water would also be lost'), ('cooling before weighing', 'hot objects give inaccurate balance readings')],
             hyp='If the mass of copper(II) carbonate increases, then the mass of CO₂ lost will increase in proportion, because CuCO₃ → CuO + CO₂ gives a fixed ratio of 44 g of CO₂ per 123.5 g of CuCO₃.',
             method='Weigh a dry boiling tube; add about 1.0 g of copper(II) carbonate and reweigh; heat strongly for 5 min; cool and reweigh; heat again until the mass is constant; repeat for 2, 3, 4, 5 g; observe the colour change from green to black; plot mass lost against starting mass.',
             weak=('the tube was weighed while still hot', 'allow the tube to cool in a desiccator before weighing so convection currents do not affect the balance'),
             safety='eye protection; point tubes away from people; copper compounds are harmful'))
inquiry('ch06-st4',
        dict(ctx='the percentage by mass of magnesium in magnesium oxide, to compare with the value calculated from the formula MgO',
             iv='mass of magnesium used (several different masses, to test whether the percentage is constant)', dv='percentage of magnesium in the oxide = mass of Mg ÷ mass of MgO × 100',
             cvs=[('heating to constant mass', 'all Mg must react'), ('minimal loss of smoke', 'loss of MgO lowers the oxide mass'), ('the same balance (0.01 g)', 'precision'), ('purity of ribbon (sanded)', 'oxide layer changes mass')],
             hyp='If the magnesium is fully converted to MgO, then the percentage by mass of magnesium will be 60%, because Mᵣ of MgO = 40 and Aᵣ of Mg = 24 (24/40 × 100).',
             method='Burn weighed masses of magnesium (0.2-0.6 g) in a lidded crucible to constant mass; calculate % Mg for each; calculate the mean and compare with 60%; identify systematic errors (e.g. incomplete reaction gives a value above 60%).',
             weak=('some magnesium remained unreacted at the end', 'reheat to constant mass and stir the residue with a glass rod to expose unreacted metal'),
             safety='do not look directly at burning magnesium; use tongs'))
inquiry('ch08-st4',
        dict(ctx='how the drop height of a ball affects its fall time, in order to measure the acceleration due to gravity g',
             iv='drop height (0.50, 1.00, 1.50, 2.00, 2.50 m, measured with a metre rule)', dv='fall time measured with light gates or an electromagnet release and trapdoor timer',
             cvs=[('the same small dense ball (e.g. steel)', 'air resistance must be negligible'), ('release from rest', 'u = 0 is assumed in s = ½gt²'), ('measuring height to the bottom of the ball', 'consistent distance'), ('timer started exactly at release', 'systematic timing error')],
             hyp='If the drop height increases, then the fall time will increase in proportion to √height, because s = ½gt² for uniform acceleration from rest; a graph of s against t² will be a straight line with gradient g/2.',
             method='Use an electromagnet to hold a steel ball at each height above a trapdoor connected to a timer; switch off to release and start the timer; the ball opens the trapdoor and stops it; repeat 5 times per height; plot height against t²; g = 2 × gradient.',
             weak=('the ball was dropped by hand and timed with a stopwatch', 'use an electromagnet release and automatic timer to remove reaction-time errors'),
             safety='keep feet clear of falling ball; secure the clamp stand'))
inquiry('ch10-st4',
        dict(ctx='how the width of a gap in a barrier affects the diffraction of water waves in a ripple tank',
             iv='gap width (1, 2, 3, 4, 6 cm), set with two metal barriers', dv='angle of spreading of the waves beyond the gap, measured with a protractor on the shadow image',
             cvs=[('wavelength (fixed vibrator frequency and water depth)', 'diffraction depends on gap width compared with wavelength'), ('water depth', 'changes speed and wavelength'), ('barrier thickness', 'affects the pattern'), ('lamp position', 'changes the projected image')],
             hyp='If the gap width is closer to the wavelength, then the waves will spread out more, because diffraction is greatest when the gap is about the same size as the wavelength.',
             method='Set depth 1 cm and frequency 8 Hz; measure the wavelength from the screen; place barriers to give gaps of 1-6 cm; photograph the pattern; measure the spreading angle on the photo; repeat 3 times; plot spreading angle against gap width ÷ wavelength.',
             weak=('the vibrator frequency was changed between gap widths', 'keep the frequency fixed so the wavelength is the same for all gaps'),
             safety='mop spills; keep water away from the lamp supply'))
