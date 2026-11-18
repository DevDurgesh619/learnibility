"""Cambridge International A Level Biology 9700, syllabus topics 12-19 (CUP coursebook 5th ed. ch 12-19), grade 12.

Paper 4 (A Level structured) and Paper 5 (planning, analysis and evaluation) styles, with Paper 1-style
MCQs for recall. Knowledge-pack builders and practical() (results tables with repeats, anomalies,
means, trends, improvements, controls) are shared from g9_biology.py; the marking-key enrichment
(bare part totals turned into mark points) is shared from g11_biology.py.

Parameterised templates cover the A2 calculations and data skills: ATP yield and efficiency, RQ from
formulae and gas volumes, respirometers, Rf values, Calvin-cycle bookkeeping, inverse-square light
intensity, filtration and reabsorption, cascade amplification, conduction velocity and refractory
periods, sarcomere band widths, genetic crosses (codominance, multiple alleles, sex linkage, dihybrid,
epistasis, linkage), chi-squared, t-test, Hardy-Weinberg, sequence comparisons, Simpson's index,
Spearman's rank, Lincoln index, restriction mapping, PCR and gel electrophoresis.
"""
import math
import itertools
from ._lib import compose, sf, sci, person, two_people, city, relation  # noqa: F401
from .g9_biology import cap, low, fx, Q, MQ, NQ, T, facts, mcqs, explain, shorts, longs, myths, pct, add_practical, trend_text  # noqa: F401
from .g11_biology import enrich, _wrap as _bio_wrap

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}


def case(r, intro, parts, k=(2, 3, 4), typ='case'):
    return compose(r, intro, parts, k=k, type_=typ)


def P_(text, ans, key):
    """A compose part that does not depend on r."""
    return lambda r: (text, ans, key)


def apply_items(t, rows, C='C3', D=(2, 3, 4), typ='short'):
    """rows: (scenario frames list, question, answer, key ending [n]). Each frame is a different context."""
    def fn(r, D_):
        frames, qn, ans, key = r.choice(rows)
        fr = r.choice(frames)
        st = fr.format(p=person(r), c=city(r)) + ' ' + qn
        return Q(st, ans, key, typ)
    fn.__name__ = 'apply'
    t.add(C, D, typ)(fn)


CRIT_CHI = {1: (3.84, 6.64), 2: (5.99, 9.21), 3: (7.82, 11.34), 4: (9.49, 13.28), 5: (11.07, 15.09)}
CRIT_T = {4: 2.78, 5: 2.57, 6: 2.45, 7: 2.36, 8: 2.31, 9: 2.26, 10: 2.23, 11: 2.20, 12: 2.18, 13: 2.16, 14: 2.14, 15: 2.13, 16: 2.12, 17: 2.11, 18: 2.10,
          19: 2.09, 20: 2.09, 22: 2.07, 24: 2.06, 26: 2.06, 28: 2.05, 30: 2.04, 38: 2.02}
CRIT_RS = {5: 1.00, 6: 0.89, 7: 0.79, 8: 0.76, 9: 0.68, 10: 0.65, 11: 0.60, 12: 0.59, 14: 0.54, 16: 0.51}


# ===================================================================== 1 Energy and respiration
t = T('The need for energy in living organisms; ATP structure, synthesis and role', 'need for energy in living organisms')
facts(t, [('ATP', 'adenosine triphosphate: a phosphorylated nucleotide of adenine, ribose and three phosphate groups that is the universal energy currency of cells'),
          ('energy currency', 'a molecule that is made in one place and used to transfer energy in small, usable amounts to energy-requiring reactions anywhere in the cell'),
          ('substrate-linked phosphorylation', 'the production of ATP by direct transfer of a phosphate group from a phosphorylated substrate molecule to ADP'),
          ('oxidative phosphorylation', 'the production of ATP using energy released as electrons pass along the electron transport chain, coupled by chemiosmosis'),
          ('ATP synthase', 'the enzyme in the inner mitochondrial and thylakoid membranes that makes ATP from ADP and Pi as protons diffuse through it'),
          ('anabolic reaction', 'a reaction that builds large molecules from smaller ones and requires energy, such as protein synthesis'),
          ('active transport', 'the movement of ions or molecules against their concentration gradient through carrier proteins, using energy from ATP hydrolysis')])
mcqs(t, [('Which molecules are produced when ATP is hydrolysed?', 'ADP and inorganic phosphate', 'ATP + H₂O → ADP + Pi, releasing about 30.5 kJ mol⁻¹.', ['AMP and glucose', 'ADP and ribose', 'Adenine and three phosphates']),
         ('Approximately how much energy is released by hydrolysis of one mole of ATP to ADP and Pi?', '30.5 kJ', 'The standard value used is about 30.5 kJ mol⁻¹.', ['2870 kJ', '305 kJ', '3.05 kJ']),
         ('Which sugar is present in a molecule of ATP?', 'Ribose', 'ATP = adenine + ribose + three phosphate groups.', ['Deoxyribose', 'Glucose', 'Fructose']),
         ('Which of these processes in a cell does NOT require ATP?', 'Diffusion of oxygen into a mitochondrion', 'Diffusion is passive; the others need ATP.', ['Active uptake of potassium ions', 'Synthesis of a polypeptide', 'Contraction of a muscle fibre']),
         ('Which is the main reason that ATP, rather than glucose, is used as the immediate energy source in cells?', 'ATP releases energy in small amounts in a single hydrolysis step', 'Glucose releases too much energy in many steps; ATP gives manageable amounts quickly.', ['ATP contains more energy per molecule than glucose', 'ATP can be stored in large amounts', 'ATP is insoluble so stays in the cell'])])
shorts(t, [('State three processes in a mammal that require energy from ATP.', 'Muscle contraction; active transport (e.g. sodium–potassium pump); anabolic reactions such as protein synthesis; nerve impulse transmission (restoring resting potential); exocytosis; DNA replication.', 'any three [3]'),
           ('State two ways in which ATP is synthesised in cells.', 'Substrate-linked phosphorylation (in glycolysis and Krebs cycle); oxidative phosphorylation / chemiosmosis (in mitochondria); photophosphorylation (in chloroplasts).', 'any two [2]'),
           ('Name the components of an ATP molecule.', 'Adenine (base), ribose (pentose sugar) and three phosphate groups.', 'adenine [1]; ribose and three phosphates [1] [2]')])
explain(t, [('Explain why ATP is described as the universal energy currency.', 'ATP is used in all organisms; it is made in respiration (or photosynthesis) and moved to where energy is needed; its hydrolysis releases energy in small, usable amounts for many different reactions.', 'used in all cells/organisms [1]; made in one place and used in another / links energy-releasing and energy-requiring reactions [1]; small amounts released in one step [1] [3]'),
            ('Explain why living organisms need a continuous supply of energy.', 'Energy is needed for anabolic reactions, active transport, movement and (in mammals and birds) maintaining body temperature; energy is lost as heat at each transfer so it must be replaced.', 'two named uses [2]; energy lost as heat / not recycled [1] [3]'),
            ('Explain why ATP cannot be stored in large amounts and must be constantly regenerated.', 'ATP is unstable (easily hydrolysed) and a cell contains only a small amount; it is used within seconds, so ADP and Pi are rephosphorylated continuously by respiration.', 'unstable / easily hydrolysed [1]; only small quantity present / turnover [1]; ADP recycled by respiration [1] [3]'),
            ('Explain the role of ATP in the active transport of sodium and potassium ions across a cell surface membrane.', 'ATP is hydrolysed by the carrier protein (an ATPase); the phosphate binds to the protein and changes its shape, so 3 Na⁺ are moved out and 2 K⁺ in against their concentration gradients.', 'ATP hydrolysed by carrier / ATPase [1]; phosphorylation causes shape change [1]; ions moved against gradient [1] [3]'),
            ('Explain why a cell with a high rate of protein synthesis contains many mitochondria.', 'Peptide bond formation and tRNA charging require ATP; mitochondria carry out aerobic respiration (Krebs cycle and oxidative phosphorylation) and produce most of the cell\'s ATP.', 'protein synthesis needs ATP [1]; mitochondria site of aerobic respiration / most ATP [1] [2]')])
myths(t, [('ATP contains a lot of energy stored in high-energy bonds, which is released when the bonds are broken.', 'Breaking bonds requires energy; energy is released overall during ATP hydrolysis because the bonds formed in the products (ADP, Pi and water interactions) release more energy than is used.'),
          ('Respiration produces energy.', 'Energy cannot be produced; respiration releases (transfers) chemical energy from organic molecules and uses it to make ATP.'),
          ('ATP is made only in mitochondria.', 'ATP is also made in the cytoplasm (glycolysis) and in chloroplasts (photophosphorylation); prokaryotes make ATP on their cell surface membranes.'),
          ('Plants do not need ATP from respiration because they make ATP in photosynthesis.', 'ATP made in the light-dependent reactions is used in the Calvin cycle; plant cells respire all the time to make ATP for other processes, including in roots and at night.'),
          ('ATP is the same as energy.', 'ATP is a molecule; its hydrolysis to ADP and Pi releases energy that cells use for work.')])
mcqs(t, [('A cell is treated with a poison that stops ATP synthesis. Which process continues unaffected for the longest time?', 'Facilitated diffusion of glucose', 'Passive processes need no ATP.', ['Exocytosis of hormones', 'Uptake of nitrate by active transport', 'Synthesis of glycogen']),
         ('A muscle contains about 5 μmol ATP per gram but uses about 2 μmol ATP per gram per second during exercise. Which is the best conclusion?', 'ATP must be regenerated continuously from ADP and Pi', 'The store would last only about 2–3 s.', ['ATP is stored in muscle for long periods', 'Muscle does not use ATP for contraction', 'ATP is made from glucose without ADP'])], D=(2, 3), C='C2')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def atp_eff(r, D):
    sub, kJ = r.choice([('glucose', 2870), ('glucose', 2880), ('a fatty acid (palmitic acid)', 9790), ('sucrose', 5640)])
    n = r.choice({'glucose': [30, 32, 34, 36, 38], 'sucrose': [60, 64, 68], 'a fatty acid (palmitic acid)': [106, 108, 129]}[sub])
    e = r.choice([30.5, 30.6, 31])
    eff = n * e / kJ * 100
    if D == 1:
        return NQ(r, f'Complete aerobic respiration of one mole of {sub} releases {kJ} kJ. It produces {n} mol of ATP, each storing {e} kJ mol⁻¹. What is the efficiency of ATP production?',
                  eff, [eff / 100, 100 - eff, kJ / (n * e)], '%', f'efficiency = {n} × {e} ÷ {kJ} × 100 = {fx(eff, 1)}%.', f=lambda v: fx(v, 1))
    p = person(r)
    st = f'{p} reads that the complete oxidation of one mole of {sub} releases {kJ} kJ of energy and yields about {n} mol of ATP. Hydrolysis of ATP releases {e} kJ mol⁻¹.'
    parts = [P_('Calculate the percentage efficiency with which energy from the substrate is transferred to ATP.', f'{fx(eff, 1)}%', f'energy in ATP = {n} × {e} = {fx(n * e, 1)} kJ [1]; ÷ {kJ} × 100 = {fx(eff, 1)}% [1] [2]'),
             P_('State what happens to the rest of the energy.', 'It is released as heat (thermal energy).', 'heat [1]; used to maintain body temperature in endotherms [1] [2]'),
             P_('Suggest why the actual yield of ATP per mole of substrate in a cell is often lower than the theoretical value.', 'Some protons leak back across the inner membrane without passing through ATP synthase; energy is used to transport ADP/Pi and pyruvate into the mitochondrion; some reduced NAD from glycolysis enters via a shuttle giving less ATP.', 'proton leakage [1]; energy used for transport into mitochondrion / shuttle [1] [2]')]
    if D >= 3:
        mol = r.choice([0.5, 1.5, 2.5, 4.0])
        parts.append(P_(f'A person respires {mol} mol of {sub} in a day. Calculate the number of moles of ATP produced.', f'{fx(mol * n, 1)} mol', f'{mol} × {n} = {fx(mol * n, 1)} mol [1]'))
    return case(r, st, parts, k=(1, 2) if D <= 2 else (2, 3), typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def atp_turnover(r, D):
    mass = r.choice([40, 45, 50, 60, 70, 75, 80])
    used = r.choice([35, 40, 50, 60, 65])  # kg ATP per day
    pool = r.choice([50, 80, 100, 150, 250])  # g present at any time
    mr = 507
    mol = used * 1000 / mr
    turns = used * 1000 / pool
    st = (f'An adult of mass {mass} kg in {city(r)} hydrolyses about {used} kg of ATP per day, yet the body contains only about {pool} g of ATP at any one time. The relative molecular mass of ATP is {mr}.')
    parts = [P_('Calculate how many times, on average, each ATP molecule is recycled per day.', f'{fx(turns, 0)} times', f'{used} kg = {used * 1000} g [1]; {used * 1000} ÷ {pool} = {fx(turns, 0)} [1] [2]'),
             P_('Calculate the number of moles of ATP hydrolysed per day.', f'{fx(mol, 0)} mol', f'{used * 1000} g ÷ {mr} = {fx(mol, 0)} mol [2]'),
             P_('Explain what these figures show about ATP as an energy store.', 'ATP is not a long-term store; it is used immediately and constantly regenerated from ADP and Pi by respiration.', 'not a store / immediate source [1]; continually regenerated [1] [2]'),
             P_(f'Using 30.5 kJ mol⁻¹, calculate the energy released per day by ATP hydrolysis.', f'{fx(mol * 30.5 / 1000, 1)} MJ', f'{fx(mol, 0)} × 30.5 = {fx(mol * 30.5, 0)} kJ [1]; = {fx(mol * 30.5 / 1000, 1)} MJ [1] [2]')]
    return case(r, st, parts, k=(2, 3), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def atp_case(r, D):
    org, cell = r.choice([('a hummingbird', 'flight muscle cells'), ('a cheetah', 'leg muscle cells'), ('a sprinter', 'fast-twitch muscle fibres'), ('a firefly', 'light-organ cells'),
                          ('an electric eel', 'electrocyte cells'), ('a honeybee', 'flight muscle cells')])
    pct_m = r.randint(25, 40)
    st = f'Scientists studying {org} found that mitochondria occupy about {pct_m}% of the volume of its {cell}, compared with about 5% in skin cells.'
    parts = [P_('Explain the difference in mitochondrial volume.', f'{cap(cell)} have a very high demand for ATP (e.g. for contraction / active processes); more mitochondria allow more aerobic respiration and oxidative phosphorylation.', 'high ATP demand linked to function [1]; mitochondria site of most ATP synthesis / Krebs and ETC [1] [2]'),
             P_('Describe the structure of an ATP molecule.', 'Adenine (a purine base) joined to ribose, with a chain of three phosphate groups attached to the ribose.', 'adenine [1]; ribose [1]; three phosphate groups [1] [3]'),
             P_('Give two reasons why ATP is suitable as the immediate energy source for these cells.', 'Hydrolysed in a single step (fast release); releases a small, manageable quantity of energy; soluble and moves easily; can be regenerated quickly.', 'any two [2]'),
             P_('Suggest why these cells also contain a store of creatine phosphate.', 'Creatine phosphate can rapidly donate a phosphate to ADP to regenerate ATP during short bursts of activity, faster than respiration can supply it.', 'regenerates ATP from ADP [1]; rapid / during sudden high demand [1] [2]'),
             P_('Explain why these cells release a lot of heat when active.', 'Energy transfer in respiration and ATP hydrolysis is inefficient; much of the energy is released as heat.', 'inefficiency [1]; heat released in respiration / ATP use [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the structure of ATP and explain its roles in living organisms.', 'Adenine, ribose, three phosphates; hydrolysis by ATPase to ADP + Pi releasing 30.5 kJ mol⁻¹; small amounts; single step; universal; made by substrate-linked and oxidative phosphorylation and photophosphorylation; used in active transport, muscle contraction, anabolic reactions, phosphorylating substrates (e.g. glucose in glycolysis), nerve impulses, cell division.',
           'structure [2]; hydrolysis and energy release [1]; reasons suited [1]; synthesis routes [1]; named uses [2] [7]'),
          ('Explain why organisms need energy and compare the ways in which ATP is synthesised.', 'Energy for work: anabolism, active transport, movement, temperature; substrate-linked phosphorylation: phosphate transferred directly from substrate in glycolysis/Krebs, small amounts; oxidative phosphorylation: ETC on cristae, proton gradient, ATP synthase, most ATP; photophosphorylation in thylakoids using light energy.',
           'need for energy [2]; substrate-linked described [1]; chemiosmosis described [2]; photophosphorylation [1]; comparison of yield / location [1] [7]')])
t1a = t

# ---------------------------------------------------------------------
t = T('Glycolysis, link reaction and Krebs cycle', 'glycolysis, link reaction and krebs cycle')
facts(t, [('glycolysis', 'the splitting of glucose (via phosphorylated hexose) into two molecules of pyruvate in the cytoplasm, with a net gain of 2 ATP and 2 reduced NAD'),
          ('link reaction', 'the decarboxylation and dehydrogenation of pyruvate in the mitochondrial matrix to form acetyl coenzyme A'),
          ('Krebs cycle', 'a cycle of reactions in the mitochondrial matrix in which acetyl groups are oxidised, releasing CO₂ and forming reduced NAD, reduced FAD and ATP'),
          ('decarboxylation', 'the removal of carbon dioxide from a molecule'),
          ('dehydrogenation', 'the removal of hydrogen from a molecule, catalysed by a dehydrogenase, usually with transfer to a coenzyme such as NAD'),
          ('coenzyme A', 'a coenzyme that carries acetyl groups from the link reaction into the Krebs cycle'),
          ('NAD', 'nicotinamide adenine dinucleotide: a coenzyme that accepts hydrogen in dehydrogenation reactions and carries it to the electron transport chain'),
          ('triose phosphate', 'a three-carbon phosphorylated sugar formed when fructose 1,6-bisphosphate splits in glycolysis')])
mcqs(t, [('Where in a eukaryotic cell does glycolysis take place?', 'Cytoplasm', 'Glycolysis is in the cytoplasm; link and Krebs in the matrix.', ['Mitochondrial matrix', 'Inner mitochondrial membrane', 'Intermembrane space']),
         ('Which compound combines with acetyl coenzyme A at the start of the Krebs cycle?', 'Oxaloacetate (4C)', 'Acetyl (2C) + oxaloacetate (4C) → citrate (6C).', ['Citrate (6C)', 'Pyruvate (3C)', 'α-ketoglutarate (5C)']),
         ('How many carbon atoms are in a molecule of citrate?', '6', 'Citrate is a 6C compound.', ['4', '5', '3']),
         ('Which process in glycolysis uses ATP?', 'Phosphorylation of glucose and fructose phosphate', 'Two ATP are used to phosphorylate the hexose, raising its energy level.', ['Oxidation of triose phosphate', 'Conversion of triose phosphate to pyruvate', 'Splitting of fructose bisphosphate']),
         ('What is the net gain of ATP per glucose molecule in glycolysis?', '2', '4 ATP made by substrate-linked phosphorylation, 2 used: net 2.', ['4', '36', '1']),
         ('Which product of the link reaction is a waste product?', 'Carbon dioxide', 'Pyruvate → acetyl CoA + CO₂ + reduced NAD.', ['Acetyl coenzyme A', 'Reduced NAD', 'Oxaloacetate'])])
shorts(t, [('State the products of the link reaction for one molecule of pyruvate.', 'Acetyl coenzyme A, one CO₂ and one reduced NAD.', 'acetyl CoA [1]; CO₂ and reduced NAD [1] [2]'),
           ('State the role of the phosphorylation of glucose at the start of glycolysis.', 'Makes glucose more reactive (raises its energy level) and traps it in the cell so it can be split into two triose phosphates.', '[2]'),
           ('Name the two coenzymes that are reduced in the Krebs cycle.', 'NAD and FAD.', '[1]')])
explain(t, [('Explain why the Krebs cycle is described as a cycle.', 'Oxaloacetate (4C) accepts the acetyl group to form citrate and is regenerated at the end of the sequence, so it can accept another acetyl group.', 'oxaloacetate combines with acetyl CoA [1]; oxaloacetate regenerated [1] [2]'),
            ('Explain why the Krebs cycle cannot continue in the absence of oxygen even though no oxygen is used in the cycle itself.', 'Without oxygen as the final electron acceptor the ETC stops, so reduced NAD and FAD are not reoxidised; no NAD/FAD is available to accept hydrogen in the dehydrogenation steps, so the cycle stops.', 'oxygen is final electron acceptor [1]; reduced NAD/FAD not reoxidised [1]; no NAD/FAD for dehydrogenation [1] [3]'),
            ('Describe what happens to pyruvate in the link reaction.', 'Pyruvate is actively transported into the matrix; it is decarboxylated (CO₂ removed) and dehydrogenated (NAD reduced); the 2C acetyl group combines with coenzyme A to form acetyl CoA.', 'enters matrix [1]; decarboxylation [1]; dehydrogenation / reduced NAD [1]; acetyl CoA formed [1] [4]'),
            ('Explain how glycolysis produces a net gain of ATP.', 'Two ATP are used to phosphorylate the hexose; each of the two triose phosphates is oxidised and converted to pyruvate, producing 2 ATP by substrate-linked phosphorylation, so 4 are made in total: net gain of 2.', '2 ATP used [1]; 4 ATP made by substrate-linked phosphorylation [1]; net 2 [1] [3]'),
            ('Explain the importance of dehydrogenation reactions in the Krebs cycle.', 'Hydrogen atoms removed are accepted by NAD and FAD; the reduced coenzymes carry hydrogen (electrons) to the ETC, where most of the ATP is made by oxidative phosphorylation.', 'hydrogen to NAD/FAD [1]; carried to ETC [1]; most ATP made there [1] [3]')])
myths(t, [('Glycolysis takes place in the mitochondria.', 'Glycolysis takes place in the cytoplasm; only pyruvate enters the mitochondrion.'),
          ('The Krebs cycle produces most of the ATP made in aerobic respiration.', 'The Krebs cycle makes only 2 ATP per glucose directly; its main role is producing reduced NAD and FAD for oxidative phosphorylation, which makes most ATP.'),
          ('Glucose enters the mitochondrion and is broken down in the Krebs cycle.', 'Glucose is broken down to pyruvate in the cytoplasm; pyruvate enters the mitochondrion.'),
          ('Oxygen is used up in the Krebs cycle.', 'Oxygen is used only at the end of the electron transport chain as the final electron acceptor.')])
mcqs(t, [('A drug inhibits the enzyme that converts citrate to the 5C compound. Which substance will accumulate first?', 'Citrate', 'Substrate of the blocked step accumulates.', ['Oxaloacetate', 'Carbon dioxide', 'Reduced FAD']),
         ('Radioactive carbon is supplied in the methyl (CH₃) group of acetyl CoA. In which molecule is the label found first?', 'Citrate', 'Acetyl CoA combines with oxaloacetate to form citrate.', ['Pyruvate', 'Glucose', 'Carbon dioxide released in the link reaction']),
         ('Arsenite inhibits the conversion of pyruvate to acetyl CoA. Which change occurs in a cell treated with arsenite?', 'Pyruvate concentration rises and CO₂ release from mitochondria falls', 'Link reaction is blocked.', ['Glycolysis stops immediately', 'Oxygen uptake increases', 'More reduced FAD is made'])], D=(2, 3), C='C2')

STAGE_OUT = {'glycolysis': {'ATP (net)': 2, 'reduced NAD': 2, 'reduced FAD': 0, 'CO₂': 0},
             'the link reaction': {'ATP (net)': 0, 'reduced NAD': 2, 'reduced FAD': 0, 'CO₂': 2},
             'the Krebs cycle': {'ATP (net)': 2, 'reduced NAD': 6, 'reduced FAD': 2, 'CO₂': 4}}


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def stage_count(r, D):
    stages = list(STAGE_OUT)
    k = r.choice([1, 2, 3]) if D >= 2 else 1
    ss = sorted(r.sample(stages, k), key=stages.index)
    prod = r.choice(['ATP (net)', 'reduced NAD', 'reduced FAD', 'CO₂'])
    n_gl = r.choice([1, 1, 2, 3, 5, 10]) if D >= 3 else 1
    tot = sum(STAGE_OUT[s][prod] for s in ss) * n_gl
    sname = ' and '.join(ss) if k < 3 else 'glycolysis, the link reaction and the Krebs cycle'
    gtxt = 'one molecule of glucose' if n_gl == 1 else f'{n_gl} molecules of glucose'
    stem = f'How many molecules of {prod.replace(" (net)", "")}{" (net gain)" if prod.startswith("ATP") else ""} are produced in {sname} from {gtxt}?'
    key = '; '.join(f'{s}: {STAGE_OUT[s][prod]} per glucose' for s in ss) + (f'; × {n_gl}' if n_gl > 1 else '') + f' = {tot}.'
    if D <= 3:
        wrong = [tot + 2, tot // 2 if tot else 1, tot * 2 if tot else 4, tot + 1, abs(tot - 2) or 3]
        return NQ(r, stem, tot, wrong, '', key, f=lambda v: str(int(v)))
    return Q('Calculate ' + stem[0].lower() + stem[1:].replace('How many', 'how many').rstrip('?') + '. Show your working, treating each stage separately.', str(tot), key + ' Per-stage values [1]; correct total [1] [2]', 'numerical')


KREBS = [('acetyl coenzyme A (2C) + oxaloacetate (4C)', 'citrate (6C)', 'no CO₂ or reduced coenzyme; coenzyme A released'),
         ('citrate (6C)', 'a 5C compound (α-ketoglutarate)', 'decarboxylation and dehydrogenation: CO₂ released and NAD reduced'),
         ('the 5C compound', 'a 4C compound', 'decarboxylation and dehydrogenation: CO₂ released, NAD reduced; ATP made by substrate-linked phosphorylation'),
         ('the 4C compound', 'oxaloacetate (4C)', 'dehydrogenations only: FAD reduced and NAD reduced; no CO₂')]


@t.add('C2', (2, 3, 4), 'explain')
def krebs_step(r, D):
    a, b, what = r.choice(KREBS)
    p = person(r)
    st = r.choice([f'In the Krebs cycle, {a} is converted to {b}. Describe what happens in this step.',
                   f'{p} is labelling a diagram of the Krebs cycle. State the types of reaction involved, and the products other than the carbon compound, when {a} is converted to {b}.',
                   f'Explain how the number of carbon atoms changes when {a} is converted to {b} in the Krebs cycle.'])
    return Q(st, cap(what) + '.', f'{cap(what)} [2]', 'explain')


@t.add('C3', (2, 3, 4, 5), 'short')
def label_trace(r, D):
    lab = r.choice([('carbon-14 in carbon atom 1 of glucose', 'pyruvate, then the CO₂ released in the link reaction (or acetyl CoA, depending on the carbon)', 'glucose → triose phosphate → pyruvate in glycolysis; carbon is lost as CO₂ in link reaction or Krebs cycle'),
                    ('carbon-14 in the carboxyl group of pyruvate', 'the CO₂ released in the link reaction', 'the carboxyl carbon of pyruvate is removed by decarboxylation in the link reaction'),
                    ('carbon-14 in the acetyl group of acetyl CoA', 'citrate, then the 5C and 4C compounds and eventually CO₂ in later turns of the cycle', 'acetyl group joins oxaloacetate to form citrate; carbons are released as CO₂ in later turns'),
                    ('oxygen-18 in oxygen gas', 'water', 'oxygen is the final electron acceptor and is reduced to water at the end of the ETC'),
                    ('hydrogen-3 (tritium) on the glucose', 'reduced NAD, then water formed at the end of the ETC', 'hydrogen removed by dehydrogenases goes to NAD/FAD, then to the ETC; protons and electrons combine with oxygen to form water')])
    what, where, why = lab
    p = person(r)
    tissue = r.choice(['yeast cells', 'isolated liver cells', 'a suspension of mitochondria with cytoplasm', 'root tip cells', 'cultured muscle cells'])
    st = f'{p} supplies {tissue} with a substrate containing {what}. Predict where the label will appear and explain your answer.'
    return Q(st, f'In {where}: {why}.', f'correct molecule [1]; reason ({why}) [1] [2]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def krebs_case(r, D):
    pyr = r.choice([2, 4, 5, 6, 8, 10])
    p = person(r)
    st = (f'{p} isolated mitochondria from {r.choice(["rat liver", "pigeon flight muscle", "potato tuber", "beef heart", "cauliflower florets"])} and suspended them in a buffered solution containing pyruvate, ADP, Pi and oxygen. '
          f'Over 20 minutes, {pyr} μmol of pyruvate were completely oxidised.')
    parts = [P_('Calculate how many μmol of carbon dioxide were released.', f'{pyr * 3} μmol', f'each pyruvate: 1 CO₂ in link reaction + 2 in Krebs cycle = 3 [1]; {pyr} × 3 = {pyr * 3} μmol [1] [2]'),
             P_('Calculate how many μmol of reduced NAD were formed.', f'{pyr * 4} μmol', f'per pyruvate: 1 (link) + 3 (Krebs) = 4 [1]; {pyr} × 4 = {pyr * 4} μmol [1] [2]'),
             P_('Explain why glucose was not used as the substrate.', 'Mitochondria cannot use glucose: glycolysis enzymes are in the cytoplasm and there is no glucose carrier in the outer/inner membrane; pyruvate is the substrate that enters mitochondria.', 'glycolysis in cytoplasm [1]; glucose cannot enter / pyruvate enters mitochondria [1] [2]'),
             P_('Predict and explain the effect of removing oxygen from the suspension.', 'CO₂ release would stop: no final electron acceptor, so reduced NAD/FAD are not oxidised; no NAD/FAD for the link reaction and Krebs cycle.', 'CO₂ release falls/stops [1]; no NAD regenerated [1]; dehydrogenation stops [1] [3]'),
             P_('Explain why ADP and Pi were included in the solution.', 'They are needed for ATP synthesis (substrate-linked and oxidative phosphorylation); without them chemiosmosis stops and so electron transport and the Krebs cycle slow down.', 'needed for ATP synthesis [1]; respiration coupled to ATP synthesis [1] [2]'),
             P_('Name the location within the mitochondrion where the link reaction and Krebs cycle take place.', 'The matrix.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the stages of glycolysis, the link reaction and the Krebs cycle.', 'Glycolysis (cytoplasm): glucose phosphorylated twice using 2 ATP to fructose bisphosphate; split into 2 triose phosphate; oxidised (NAD reduced) to pyruvate; 4 ATP by substrate-linked phosphorylation (net 2). Link (matrix): pyruvate decarboxylated and dehydrogenated, acetyl CoA. Krebs: acetyl + oxaloacetate → citrate (6C); decarboxylations to 5C and 4C; reduced NAD ×3, FAD ×1, ATP ×1 per turn; oxaloacetate regenerated.',
           'glycolysis phosphorylation and splitting [2]; oxidation and ATP yield [1]; link reaction [2]; Krebs citrate [1]; decarboxylation / dehydrogenation / products per turn [2] [8]'),
          ('Explain how the structure of a mitochondrion is adapted for its functions in respiration.', 'Outer membrane with transport proteins (pyruvate entry); matrix contains Krebs and link reaction enzymes, coenzymes, mitochondrial DNA and 70S ribosomes; inner membrane folded into cristae giving large surface area for ETC and ATP synthase; inner membrane impermeable to protons; small intermembrane space allows proton gradient to build quickly.',
           'matrix enzymes / link and Krebs [2]; cristae surface area [1]; ETC and ATP synthase on inner membrane [1]; impermeable to H⁺ [1]; intermembrane space [1]; DNA/ribosomes to make own proteins [1] [7]')])
t1b = t

# ---------------------------------------------------------------------
t = T('Oxidative phosphorylation, electron transport chain and chemiosmosis in mitochondria', 'oxidative phosphorylation, electron transport chain')
facts(t, [('electron transport chain', 'a series of electron carrier proteins in the inner mitochondrial membrane that pass electrons from reduced NAD/FAD to oxygen, releasing energy used to pump protons'),
          ('chemiosmosis', 'the synthesis of ATP driven by the diffusion of protons down their electrochemical gradient through ATP synthase'),
          ('proton gradient', 'a difference in hydrogen ion concentration across a membrane, built up by active pumping of protons, that stores energy'),
          ('final electron acceptor', 'oxygen, which combines with electrons and protons at the end of the electron transport chain to form water'),
          ('cristae', 'the folds of the inner mitochondrial membrane that give a large surface area for electron carriers and ATP synthase'),
          ('intermembrane space', 'the narrow region between the outer and inner mitochondrial membranes into which protons are pumped'),
          ('uncoupler', 'a substance that makes the inner membrane leaky to protons so that electron transport continues but ATP synthesis stops')])
mcqs(t, [('Where are the electron carriers of the electron transport chain located in a mitochondrion?', 'Inner mitochondrial membrane', 'On the cristae.', ['Outer mitochondrial membrane', 'Matrix', 'Intermembrane space']),
         ('Into which region are protons pumped by the electron transport chain?', 'Intermembrane space', 'This builds a proton gradient across the inner membrane.', ['Matrix', 'Cytoplasm', 'Stroma']),
         ('What is the role of oxygen in aerobic respiration?', 'It is the final electron acceptor, forming water', 'O₂ + 4H⁺ + 4e⁻ → 2H₂O.', ['It oxidises glucose directly in glycolysis', 'It combines with carbon to form CO₂', 'It phosphorylates ADP']),
         ('Through which protein do protons diffuse back into the matrix to drive ATP synthesis?', 'ATP synthase', 'ATP synthase allows facilitated diffusion of H⁺ coupled to ATP synthesis.', ['Cytochrome oxidase', 'NAD dehydrogenase', 'Coenzyme A']),
         ('Which of these provides the energy that is used to pump protons across the inner mitochondrial membrane?', 'Electrons passing along the chain of carriers', 'Energy released as electrons move to lower energy levels.', ['Hydrolysis of ATP', 'Light absorbed by pigments', 'Diffusion of oxygen'])])
shorts(t, [('State why reduced FAD yields less ATP than reduced NAD.', 'Reduced FAD passes its electrons to a carrier further along the chain, so fewer protons are pumped per pair of electrons.', 'enters chain later [1]; fewer protons pumped [1] [2]'),
           ('Name the products formed at the end of the electron transport chain.', 'Water (from oxygen, electrons and protons).', '[1]')])
explain(t, [('Explain how the electron transport chain produces a proton gradient.', 'Reduced NAD/FAD donate electrons (and protons) to the chain; electrons pass along carriers by redox reactions, releasing energy; this energy is used by carrier proteins to pump protons from the matrix into the intermembrane space.', 'electrons from reduced NAD/FAD [1]; redox / energy released as electrons pass [1]; protons pumped into intermembrane space [1] [3]'),
            ('Explain how ATP is synthesised by chemiosmosis in a mitochondrion.', 'High proton concentration in the intermembrane space; inner membrane impermeable to protons; protons diffuse back into the matrix through ATP synthase down their electrochemical gradient; this causes the enzyme to rotate/change shape and catalyse ADP + Pi → ATP.', 'proton gradient [1]; membrane impermeable except via ATP synthase [1]; diffusion through ATP synthase [1]; ADP + Pi → ATP [1] [4]'),
            ('Explain why cyanide, which inhibits the final carrier (cytochrome oxidase), quickly stops ATP synthesis.', 'Electrons cannot pass to oxygen, so the chain backs up; no electron flow means no protons pumped; the proton gradient is lost and ATP synthase stops; NAD is not regenerated so the Krebs cycle also stops.', 'electron flow stops [1]; no proton pumping / gradient [1]; no chemiosmosis / ATP [1]; NAD not regenerated [1] [4]'),
            ('Explain why the inner mitochondrial membrane being impermeable to protons is essential for ATP synthesis.', 'Protons can only return through ATP synthase, so the gradient is maintained and its energy is used to make ATP; leakage would dissipate the gradient as heat.', 'gradient maintained [1]; protons forced through ATP synthase [1] [2]'),
            ('Explain how the folding of the inner mitochondrial membrane increases the rate of ATP production.', 'Cristae give a large surface area for many electron transport chains and ATP synthase molecules, so more oxidative phosphorylation per mitochondrion.', 'large surface area [1]; more ETC / ATP synthase [1] [2]')])
myths(t, [('Protons are pumped into the matrix by the electron transport chain.', 'Protons are pumped from the matrix into the intermembrane space; they diffuse back into the matrix through ATP synthase.'),
          ('ATP synthase uses energy from ATP to pump protons.', 'In mitochondria ATP synthase makes ATP using the energy of protons diffusing down their gradient.'),
          ('Oxygen accepts electrons at the start of the electron transport chain.', 'Oxygen is the final electron acceptor at the end of the chain.'),
          ('Oxidative phosphorylation takes place in the matrix.', 'It takes place on the inner mitochondrial membrane (cristae); ATP synthase heads face the matrix.')])
mcqs(t, [('DNP makes the inner mitochondrial membrane permeable to protons. What is the effect of DNP on respiring cells?', 'Oxygen uptake continues but ATP synthesis falls and more heat is released', 'DNP is an uncoupler.', ['Oxygen uptake stops and ATP synthesis increases', 'Glycolysis stops', 'Both oxygen uptake and heat release fall']),
         ('Oligomycin blocks the proton channel of ATP synthase. What happens to the pH of the intermembrane space shortly after adding oligomycin?', 'It falls further (becomes more acidic), then electron transport slows', 'Protons accumulate as they cannot flow back.', ['It rises immediately', 'It does not change', 'It becomes alkaline because protons enter the matrix']),
         ('In which order do electrons pass in the electron transport chain?', 'Reduced NAD → carriers in the inner membrane → oxygen', 'NAD → carriers → O₂.', ['Oxygen → carriers → NAD', 'ATP synthase → carriers → oxygen', 'Reduced FAD → NAD → ATP synthase'])], D=(2, 3), C='C2')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def atp_yield(r, D):
    nad_y, fad_y = r.choice([(2.5, 1.5), (3, 2)])
    ss = r.choice([['the link reaction'], ['the Krebs cycle'], ['the link reaction', 'the Krebs cycle'], ['glycolysis', 'the link reaction', 'the Krebs cycle']])
    nad = sum(STAGE_OUT[s]['reduced NAD'] for s in ss)
    fad = sum(STAGE_OUT[s]['reduced FAD'] for s in ss)
    sl = sum(STAGE_OUT[s]['ATP (net)'] for s in ss)
    ox = nad * nad_y + fad * fad_y
    tot = ox + sl
    stxt = ', '.join(ss[:-1]) + ' and ' + ss[-1] if len(ss) > 1 else ss[0]
    st = (f'Assume that each reduced NAD gives {fx(nad_y, 1)} ATP and each reduced FAD gives {fx(fad_y, 1)} ATP by oxidative phosphorylation. '
          f'Calculate the total number of ATP molecules made from one glucose molecule as a result of {stxt}, including any ATP made by substrate-linked phosphorylation.')
    key = f'reduced NAD = {nad}, reduced FAD = {fad} [1]; {nad} × {fx(nad_y, 1)} + {fad} × {fx(fad_y, 1)} = {fx(ox, 1)} [1]; + {sl} substrate-linked = {fx(tot, 1)} [1] [3]'
    if D <= 2:
        return NQ(r, st.replace('Calculate the total', 'What is the total'), tot, [ox, tot + 2, nad + fad + sl, tot * 2], '', key, f=lambda v: fx(v, 1))
    if D >= 4:
        st += ' Suggest why the number of ATP molecules actually made is usually lower.'
        return Q(st, f'{fx(tot, 1)} ATP; actual yield lower because of proton leakage and energy used to transport pyruvate/ADP/Pi into the mitochondrion.', key.replace('[3]', '') + 'proton leak or transport cost [1] [4]', 'numerical')
    return Q(st, f'{fx(tot, 1)} ATP', key, 'numerical')


@t.add('C3', (2, 3, 4, 5), 'case')
def ph_gradient(r, D):
    m = round(r.uniform(7.6, 8.0), 1)
    s = round(m - r.choice([0.5, 0.7, 1.0, 1.2, 1.4]), 1)
    ratio = 10 ** (m - s)
    p = person(r)
    st = f'{p} measured the pH in the matrix of actively respiring mitochondria as {fx(m, 1)} and in the intermembrane space as {fx(s, 1)}.'
    parts = [P_('Calculate how many times greater the hydrogen ion concentration is in the intermembrane space than in the matrix.', f'{sf(ratio, 3)} times', f'difference = {fx(m - s, 1)} pH units [1]; 10^{fx(m - s, 1)} = {sf(ratio, 3)} [1] [2]'),
             P_('Explain how this difference in pH is produced.', 'Energy from electrons passing along the ETC is used to pump protons from the matrix into the intermembrane space.', 'ETC / electron flow [1]; protons pumped into intermembrane space [1] [2]'),
             P_('Predict the effect of adding an uncoupler such as DNP on the pH difference and explain your answer.', 'The difference would decrease (pH values become similar) because protons leak back across the membrane without passing through ATP synthase.', 'difference falls [1]; protons leak back / gradient dissipated [1] [2]'),
             P_('Explain how this pH difference is used to make ATP.', 'Protons diffuse down their gradient through ATP synthase into the matrix; this drives phosphorylation of ADP to ATP (chemiosmosis).', 'diffusion through ATP synthase [1]; ADP + Pi → ATP [1] [2]')]
    return case(r, st, parts, k=(2, 3))


INHIB = [('cyanide', 'inhibits cytochrome oxidase, the last carrier, so electrons cannot pass to oxygen', 'oxygen uptake stops; ATP synthesis stops; reduced NAD accumulates'),
         ('DNP', 'acts as an uncoupler, carrying protons across the inner membrane', 'oxygen uptake continues (or rises); ATP synthesis falls; heat production rises'),
         ('oligomycin', 'blocks the proton channel of ATP synthase', 'ATP synthesis stops; proton gradient becomes very steep so electron transport and oxygen uptake slow'),
         ('rotenone', 'blocks the transfer of electrons from reduced NAD to the first carrier', 'oxygen uptake from NAD-linked substrates stops, but reduced FAD (e.g. from succinate) can still supply electrons'),
         ('carbon monoxide', 'binds to cytochrome oxidase in place of oxygen', 'electron flow to oxygen is blocked; oxygen uptake and ATP synthesis fall')]


@t.add('C4', (2, 3, 4, 5), 'case')
def inhib_case(r, D):
    (a, wa, ea), (b, wb, eb) = r.sample(INHIB, 2)
    p = person(r)
    st = f'{p} investigates two respiratory poisons on a suspension of isolated mitochondria supplied with a substrate, ADP and Pi. {cap(a)} {wa}. {cap(b)} {wb}.'
    parts = [P_(f'Predict the effects of {a} on oxygen uptake and ATP synthesis.', cap(ea) + '.', f'{ea} [2]'),
             P_(f'Predict the effects of {b} on oxygen uptake and ATP synthesis.', cap(eb) + '.', f'{eb} [2]'),
             P_('Explain why oxygen uptake can be used as a measure of the rate of electron transport.', 'Oxygen is the final electron acceptor; each pair of electrons that passes along the chain reduces half an oxygen molecule to water, so oxygen use is proportional to electron flow.', 'oxygen final acceptor [1]; proportional to electron flow [1] [2]'),
             P_('Explain why electron transport and ATP synthesis are described as coupled.', 'Electron transport pumps protons; the proton gradient is used to make ATP; if ATP synthesis stops, the gradient builds up and slows electron transport.', 'gradient links the two [1]; one cannot normally occur without the other [1] [2]'),
             P_('Describe the role of the intermembrane space in chemiosmosis.', 'Protons are pumped into this small space so their concentration rises quickly, creating a steep gradient across the inner membrane.', 'protons accumulate there [1]; small volume gives steep gradient [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how oxidative phosphorylation produces ATP in a mitochondrion.', 'Reduced NAD and FAD release H; H splits into H⁺ and e⁻; electrons passed along carriers in inner membrane (redox); energy released pumps H⁺ into intermembrane space; proton gradient; H⁺ diffuse through ATP synthase; ADP + Pi → ATP; oxygen final electron acceptor forming water; NAD regenerated.',
           'H from reduced NAD/FAD [1]; electrons along carriers [1]; energy pumps protons [1]; gradient [1]; ATP synthase [1]; ADP + Pi [1]; oxygen + water [1] [7]'),
          ('Explain the effects of cyanide on a cell, starting from its effect on the electron transport chain.', 'Inhibits cytochrome oxidase; electrons not passed to oxygen; chain stops; no proton pumping; no ATP from chemiosmosis; reduced NAD/FAD not oxidised so NAD/FAD unavailable; Krebs and link reaction stop; only glycolysis with anaerobic regeneration of NAD; ATP-requiring processes (active transport, contraction) fail; lactate builds up; cell death.',
           'site of action [1]; electron flow stops [1]; no proton gradient / ATP [1]; NAD not regenerated [1]; Krebs stops [1]; anaerobic only, little ATP [1]; consequence for cell [1] [7]')])
t1c = t

# ---------------------------------------------------------------------
t = T('Anaerobic respiration in mammals and yeast; respiratory substrates and respiratory quotient', 'anaerobic respiration in mammals and yeast')
facts(t, [('respiratory quotient', 'the ratio of the volume of carbon dioxide given out to the volume of oxygen taken in during respiration in a given time (RQ = CO₂ ÷ O₂)'),
          ('respiratory substrate', 'an organic molecule that can be oxidised in respiration to release energy, such as carbohydrate, lipid or protein'),
          ('ethanol fermentation', 'anaerobic respiration in yeast and plants in which pyruvate is decarboxylated to ethanal and reduced to ethanol, regenerating NAD'),
          ('lactate fermentation', 'anaerobic respiration in mammalian muscle in which pyruvate is reduced to lactate by lactate dehydrogenase, regenerating NAD'),
          ('oxygen debt', 'the extra oxygen taken in after exercise to oxidise lactate (in the liver) and restore ATP and creatine phosphate levels'),
          ('aerenchyma', 'tissue with large air spaces found in rice stems and roots that allows oxygen to diffuse to submerged tissues')])
mcqs(t, [('What is the main purpose of converting pyruvate to lactate in mammalian muscle during anaerobic respiration?', 'To regenerate NAD so glycolysis can continue', 'Reduced NAD is reoxidised.', ['To produce extra ATP', 'To release carbon dioxide', 'To store energy as lactate for growth']),
         ('Which substrate releases the most energy per gram when respired?', 'Lipid', 'About 39 kJ g⁻¹ compared with about 17 kJ g⁻¹ for carbohydrate and protein.', ['Carbohydrate', 'Protein', 'Glucose']),
         ('What is the RQ of a tissue respiring only carbohydrate aerobically?', '1.0', 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O: 6 ÷ 6.', ['0.7', '0.9', '1.4']),
         ('Which enzyme converts ethanal to ethanol in yeast?', 'Alcohol dehydrogenase', 'Ethanal is reduced using reduced NAD.', ['Pyruvate decarboxylase', 'Lactate dehydrogenase', 'ATP synthase']),
         ('How many molecules of ATP (net) are produced per glucose in anaerobic respiration?', '2', 'Only glycolysis produces ATP.', ['0', '4', '32']),
         ('Lipids release more energy per gram than carbohydrates mainly because they contain', 'more hydrogen atoms per molecule, giving more reduced NAD and FAD', 'Energy comes mainly from hydrogen passing to the ETC.', ['more oxygen atoms', 'more carbon dioxide', 'phosphate groups'])])
shorts(t, [('State the approximate RQ values for carbohydrate, lipid and protein.', 'Carbohydrate 1.0; lipid 0.7; protein 0.9.', 'all three [2]; two [1] [2]'),
           ('State two products of anaerobic respiration in yeast.', 'Ethanol and carbon dioxide (and a small amount of ATP).', '[2]'),
           ('State two adaptations of rice for growing in waterlogged soil.', 'Aerenchyma in stems/roots; tolerance of high ethanol concentration / high alcohol dehydrogenase activity; fast-growing stems keep leaves above water; shallow roots.', 'any two [2]')])
explain(t, [('Explain why far less ATP is produced in anaerobic respiration than in aerobic respiration.', 'Only glycolysis produces ATP (net 2); without oxygen the ETC cannot accept electrons, so no oxidative phosphorylation; link reaction and Krebs cycle stop; much energy remains in lactate or ethanol.', 'only glycolysis [1]; no ETC / oxidative phosphorylation [1]; Krebs stops [1]; energy left in product [1] [4]'),
            ('Explain why an RQ greater than 1 suggests that some anaerobic respiration is taking place.', 'Anaerobic respiration in yeast/plants produces CO₂ without using oxygen, so CO₂ given out exceeds O₂ taken in.', 'CO₂ produced without O₂ uptake [1]; ratio > 1 [1] [2]'),
            ('Explain why lipids have a lower RQ than carbohydrates.', 'Lipids contain relatively little oxygen and more hydrogen, so more oxygen is needed to oxidise the hydrogen to water for each CO₂ produced.', 'less oxygen in molecule / more H [1]; more O₂ needed per CO₂ [1] [2]'),
            ('Compare anaerobic respiration in mammals and yeast.', 'Both: glycolysis, 2 ATP, NAD regenerated by reducing pyruvate (product). Mammals: pyruvate → lactate, one step, no CO₂, reversible. Yeast: pyruvate → ethanal + CO₂ → ethanol, two steps, irreversible.', 'similarity [1]; lactate vs ethanol [1]; CO₂ released only in yeast [1]; reversibility / number of steps [1] [4]'),
            ('Explain what happens to lactate after vigorous exercise in a mammal.', 'Lactate is carried in the blood to the liver; it is oxidised back to pyruvate, which can be respired aerobically or converted to glucose/glycogen; the extra oxygen needed is the oxygen debt.', 'transported to liver [1]; converted to pyruvate [1]; respired or to glucose/glycogen [1]; uses extra O₂ (debt) [1] [4]')])
myths(t, [('Anaerobic respiration in humans produces carbon dioxide and lactic acid.', 'Lactate fermentation in mammals produces no CO₂; only lactate (and 2 ATP per glucose).'),
          ('An RQ of 0.7 shows that the organism is respiring anaerobically.', 'An RQ of about 0.7 indicates aerobic respiration of lipid; anaerobic respiration in yeast gives RQ above 1.'),
          ('Lactate is converted back into glucose in the muscle cells.', 'Most lactate is transported to the liver, where it is oxidised to pyruvate or converted to glucose/glycogen.'),
          ('Proteins are the main respiratory substrate in a healthy well-fed mammal.', 'Carbohydrate and fat are the main substrates; protein is used mainly during starvation.')])

SUBSTRATES = [('glucose', 'C6H12O6', 6, 12, 6), ('stearic acid', 'C18H36O2', 18, 36, 2), ('palmitic acid', 'C16H32O2', 16, 32, 2), ('oleic acid', 'C18H34O2', 18, 34, 2),
              ('tripalmitin', 'C51H98O6', 51, 98, 6), ('triolein', 'C57H104O6', 57, 104, 6), ('malic acid', 'C4H6O5', 4, 6, 5), ('citric acid', 'C6H8O7', 6, 8, 7),
              ('sucrose', 'C12H22O11', 12, 22, 11), ('lauric acid', 'C12H24O2', 12, 24, 2), ('oxalic acid', 'C2H2O4', 2, 2, 4), ('glycerol', 'C3H8O3', 3, 8, 3)]
_SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def _frm(f):
    return f.translate(_SUB)


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def rq_formula(r, D):
    name, f, c, h, o = r.choice(SUBSTRATES)
    o2 = c + h / 4 - o / 2
    rq = c / o2
    if D == 1:
        return NQ(r, f'Complete aerobic respiration of one molecule of {name} uses {fx(o2, 1)} molecules of oxygen and produces {c} molecules of carbon dioxide. What is the RQ?',
                  rq, [o2 / c, 1.0 if abs(rq - 1) > 0.05 else 0.7, rq + 0.2, rq - 0.15], '', f'RQ = CO₂ ÷ O₂ = {c} ÷ {fx(o2, 1)} = {fx(rq, 2)}.', f=lambda v: fx(v, 2))
    eq = f'{_frm(f)} + {fx(o2, 1)}O₂ → {c}CO₂ + {fx(h / 2, 1)}H₂O'
    if D == 2:
        return Q(f'The equation for the complete aerobic respiration of {name} is {eq}. Calculate the respiratory quotient (RQ).', fx(rq, 2), f'RQ = CO₂ ÷ O₂ [1]; {c} ÷ {fx(o2, 1)} = {fx(rq, 2)} [1] [2]', 'numerical')
    st = f'{name.capitalize()} has the formula {_frm(f)}. Construct a balanced equation for its complete aerobic respiration and calculate the RQ.'
    key = f'{eq} [2]; RQ = {c} ÷ {fx(o2, 1)} = {fx(rq, 2)} [1] [3]'
    if D >= 4:
        st += ' Comment on what this RQ suggests about the type of substrate.'
        kind = 'a lipid / fatty acid (RQ about 0.7)' if rq < 0.8 else ('a carbohydrate (RQ = 1)' if abs(rq - 1) < 0.03 else ('an organic acid: RQ above 1 because the substrate is already highly oxidised' if rq > 1.03 else 'a substrate between lipid and carbohydrate'))
        return Q(st, f'{eq}; RQ = {fx(rq, 2)}; consistent with {kind}.', key.replace(' [3]', '') + f'; {kind} [1] [4]', 'numerical')
    return Q(st, f'{eq}; RQ = {fx(rq, 2)}', key, 'numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def rq_gas(r, D):
    sub, rq = r.choice([('lipid', r.uniform(0.68, 0.72)), ('carbohydrate', r.uniform(0.98, 1.02)), ('protein', r.uniform(0.88, 0.92)), ('carbohydrate with some anaerobic respiration', r.uniform(1.25, 1.6)),
                        ('a mixture of carbohydrate and lipid', r.uniform(0.8, 0.86))])
    o2 = round(r.uniform(0.8, 3.5), 2)
    co2 = round(o2 * rq, 2)
    rq = co2 / o2
    org = r.choice(['germinating castor oil seeds', 'germinating pea seeds', 'germinating wheat grains', 'blowfly larvae', 'yeast in glucose solution', 'germinating sunflower seeds', 'woodlice', 'maggots'])
    tm = r.choice([10, 15, 20, 30])
    st = f'In {tm} minutes, {org} took in {fx(o2, 2)} cm³ of oxygen and gave out {fx(co2, 2)} cm³ of carbon dioxide.'
    parts = [P_('Calculate the respiratory quotient.', fx(rq, 2), f'RQ = CO₂ ÷ O₂ = {fx(co2, 2)} ÷ {fx(o2, 2)} [1] = {fx(rq, 2)} [1] [2]'),
             P_('Calculate the respiratory quotient and suggest which respiratory substrate is being used.', f'RQ = {fx(rq, 2)}; {sub}, as the RQ is close to the value for this substrate.', f'RQ = {fx(co2, 2)} ÷ {fx(o2, 2)} = {fx(rq, 2)} [1]; {sub} [1]; reason linked to RQ value [1] [3]'),
             P_('Calculate the rate of oxygen uptake per hour.', f'{fx(o2 * 60 / tm, 2)} cm³ h⁻¹', f'{fx(o2, 2)} × 60 ÷ {tm} = {fx(o2 * 60 / tm, 2)} [1]')]
    if D >= 4:
        parts.append(P_('Explain why the RQ of germinating seeds may change over the first few days of germination.', 'Stored lipid or starch is used first and the substrate changes as stores are depleted or converted (e.g. lipid converted to sugar); early on, low oxygen inside the seed coat may cause anaerobic respiration (RQ > 1).', 'change of substrate [1]; anaerobic respiration early on / seed coat impermeable [1] [2]'))
    return case(r, st, parts, k=(2, 3), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def anaer_case(r, D):
    scen = r.randrange(3)
    p = person(r)
    if scen == 0:
        lac0 = round(r.uniform(0.8, 1.5), 1)
        lacp = round(r.uniform(8, 14), 1)
        st = f'{p}, an athlete in {city(r)}, ran 400 m at maximum speed. Blood lactate rose from {fx(lac0, 1)} mmol dm⁻³ at rest to {fx(lacp, 1)} mmol dm⁻³ two minutes after the race and returned to the resting level after about 40 minutes.'
        parts = [P_('Calculate the percentage increase in blood lactate concentration.', f'{fx(pct(lac0, lacp), 0)}%', f'({fx(lacp, 1)} − {fx(lac0, 1)}) ÷ {fx(lac0, 1)} × 100 [1] = {fx(pct(lac0, lacp), 0)}% [1] [2]'),
                 P_('Explain why lactate was produced during the race.', 'Oxygen could not be supplied fast enough for aerobic respiration; pyruvate was reduced to lactate by lactate dehydrogenase to regenerate NAD so that glycolysis could continue producing ATP.', 'insufficient oxygen [1]; pyruvate reduced [1]; NAD regenerated [1]; glycolysis continues [1] [4]'),
                 P_('Explain why the athlete continued to breathe deeply after the race.', 'To repay the oxygen debt: extra oxygen is used to oxidise lactate in the liver (to pyruvate/glucose) and to resynthesise ATP and creatine phosphate and reoxygenate myoglobin.', 'oxygen debt [1]; lactate oxidised in liver [1]; restore ATP / creatine phosphate [1] [3]'),
                 P_('Suggest why lactate takes several minutes to reach its highest concentration in the blood after the race.', 'Lactate must diffuse out of the muscle cells into the blood; it continues to be released after exercise stops.', '[1]')]
    elif scen == 1:
        st = (f'Rice is grown in flooded paddy fields in {city(r)}. In waterlogged conditions the roots of most plants die, but rice roots survive. '
              f'Researchers found that alcohol dehydrogenase activity in rice roots rose by {r.randint(4, 12)} times after flooding.')
        parts = [P_('Explain why the roots of most plants die in waterlogged soil.', 'Water fills air spaces so little oxygen reaches roots; roots respire anaerobically, producing little ATP for active uptake of ions, and ethanol accumulates to toxic levels.', 'lack of oxygen [1]; anaerobic respiration / little ATP [1]; ethanol toxic [1] [3]'),
                 P_('Explain the advantage of the increase in alcohol dehydrogenase activity.', 'Ethanal is reduced to ethanol more rapidly, so NAD is regenerated and glycolysis can continue to provide ATP.', 'NAD regenerated [1]; glycolysis / ATP continues [1] [2]'),
                 P_('Describe how aerenchyma helps rice to survive flooding.', 'Large air spaces in stem and root tissue allow oxygen to diffuse from the leaves above water down to the roots, allowing aerobic respiration.', 'air spaces [1]; oxygen diffuses to roots [1] [2]'),
                 P_('State the products of anaerobic respiration in rice root cells.', 'Ethanol, carbon dioxide and a small amount of ATP.', '[2]')]
    else:
        g = r.choice([5, 10, 20])
        st = f'{p} mixed {g} g of yeast with glucose solution in a sealed flask in {city(r)}. After the oxygen was used up, carbon dioxide was still released and ethanol accumulated.'
        parts = [P_('Describe the reactions by which yeast converts pyruvate to ethanol.', 'Pyruvate is decarboxylated to ethanal by pyruvate decarboxylase (CO₂ released); ethanal is reduced to ethanol by alcohol dehydrogenase using reduced NAD.', 'decarboxylation to ethanal [1]; reduction to ethanol [1]; NAD regenerated [1] [3]'),
                 P_('Explain why the yeast population eventually stopped growing.', 'Ethanol accumulated to toxic concentrations / glucose was used up; little ATP is made by anaerobic respiration.', 'ethanol toxic [1]; substrate used up / little ATP [1] [2]'),
                 P_('Predict the RQ of the yeast once the oxygen has been used up, and explain.', 'Very large / infinite: CO₂ is still released but no oxygen is taken in.', 'very high / > 1 [1]; CO₂ without O₂ uptake [1] [2]'),
                 P_('Calculate the theoretical maximum ratio of ATP produced per glucose by aerobic respiration to that produced by anaerobic respiration, using 32 ATP for aerobic respiration.', '16 : 1', '32 ÷ 2 = 16 [1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Compare anaerobic respiration in a mammalian muscle with anaerobic respiration in yeast, and explain why the yield of ATP is low.', 'Both: glycolysis only, 2 ATP net, pyruvate is hydrogen acceptor so NAD regenerated. Mammal: lactate dehydrogenase, lactate, no CO₂, reversible, lactate to liver. Yeast: pyruvate decarboxylase → ethanal + CO₂; alcohol dehydrogenase → ethanol; irreversible. Low yield: no oxygen as final acceptor so ETC stops, no oxidative phosphorylation, Krebs stops, energy remains in lactate/ethanol.',
           'similarities [2]; mammal pathway [1]; yeast pathway [2]; reasons for low yield [2] [7]'),
          ('Explain what is meant by respiratory quotient and how RQ values can be used to identify respiratory substrates.', 'RQ = CO₂ produced ÷ O₂ used; carbohydrate 1.0; lipid 0.7 (more H relative to O so more O₂ needed); protein 0.9; mixed substrates give intermediate values; RQ > 1 anaerobic respiration or conversion of carbohydrate to lipid; measured with respirometer using KOH/soda lime; example calculation from equation.',
           'definition [1]; three values [2]; reason lipid lower [1]; RQ > 1 [1]; method of measurement [1] [6]')])
t1d = t

# ---------------------------------------------------------------------
t = T('Investigating respiration rates with respirometers and redox indicators', 'investigating respiration rates with respirometers')
facts(t, [('respirometer', 'apparatus that measures the rate of oxygen uptake by respiring organisms from the movement of a fluid in a capillary tube'),
          ('soda lime', 'a solid that absorbs carbon dioxide, used in a respirometer so that changes in volume are due to oxygen uptake only'),
          ('redox indicator', 'a dye such as methylene blue or DCPIP that changes colour when it is reduced by accepting hydrogen'),
          ('compensating tube', 'a second tube containing no organisms, used to cancel out effects of changes in temperature and pressure'),
          ('methylene blue', 'a redox indicator that is blue when oxidised and colourless when reduced by dehydrogenase activity in respiring cells')])
mcqs(t, [('Why is potassium hydroxide solution placed in a respirometer?', 'To absorb carbon dioxide', 'Movement of the fluid then shows oxygen uptake only.', ['To absorb oxygen', 'To provide water for the organisms', 'To keep the pH constant']),
         ('In which direction does the coloured fluid in a respirometer with soda lime move when organisms respire aerobically?', 'Towards the organisms', 'O₂ is taken in and CO₂ absorbed, so the gas volume falls.', ['Away from the organisms', 'It does not move', 'It moves randomly']),
         ('Methylene blue added to a yeast suspension becomes colourless. What has happened to the methylene blue?', 'It has been reduced by accepting hydrogen', 'Dehydrogenases transfer H to the dye.', ['It has been oxidised', 'It has been hydrolysed', 'It has been absorbed by the yeast'])])
shorts(t, [('State two variables that must be controlled when measuring the effect of temperature on the respiration rate of seeds in a respirometer.', 'Mass/number of seeds; type and age of seeds; volume of KOH/soda lime; time allowed to equilibrate; diameter of capillary.', 'any two [2]'),
           ('State the formula used to calculate the volume of oxygen taken up from the distance moved by the fluid in a capillary tube.', 'Volume = πr²h, where r is the radius of the capillary bore and h is the distance moved.', '[1]')])
explain(t, [('Explain why a respirometer containing organisms is left in the water bath for several minutes before readings are taken.', 'To allow the apparatus and organisms to reach the temperature of the water bath (equilibrate), so that changes in volume are due to respiration and not gas expansion or contraction.', 'equilibrate to temperature [1]; avoids volume changes from heating/cooling [1] [2]'),
            ('Explain how a respirometer could be used to measure the RQ of germinating seeds.', 'Measure volume change with KOH (O₂ uptake, x); repeat without KOH (difference between O₂ uptake and CO₂ output, y); CO₂ = x − y (if movement towards seeds is positive); RQ = (x − y) ÷ x.', 'with KOH gives O₂ [1]; without KOH gives O₂ − CO₂ [1]; calculation of RQ [1] [3]'),
            ('Explain why a control tube containing glass beads of the same volume as the seeds is used.', 'It compensates for changes in temperature and atmospheric pressure, so any movement in the experimental tube is caused by respiration only.', 'temperature/pressure changes [1]; movement due to respiration only [1] [2]'),
            ('Explain why the rate of decolourisation of methylene blue can be used as a measure of the rate of respiration in yeast.', 'Dehydrogenase enzymes in respiration remove hydrogen from substrates; methylene blue accepts this hydrogen instead of NAD and becomes colourless, so a faster colour change means faster dehydrogenation / respiration.', 'dehydrogenase activity [1]; dye reduced by H [1]; faster change = faster rate [1] [3]')])
myths(t, [('In a respirometer with soda lime, the fluid moves because the organisms produce carbon dioxide.', 'Soda lime absorbs the CO₂; the fluid moves because oxygen is taken in, reducing the volume of gas.'),
          ('Methylene blue turns colourless because it is broken down by respiration.', 'Methylene blue is reduced (accepts hydrogen from dehydrogenation reactions) and can be reoxidised to blue by shaking with air.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def capillary(r, D):
    dmm = r.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
    dist = r.choice([12, 18, 24, 30, 36, 42, 48, 55, 60])
    tmin = r.choice([5, 10, 15, 20])
    mass = r.choice([2.0, 2.5, 4.0, 5.0, 8.0, 10.0])
    rr = dmm / 2
    vol = math.pi * rr ** 2 * dist
    rate = vol / tmin / mass
    org = r.choice(['germinating mung beans', 'germinating barley grains', 'woodlice', 'mealworms', 'maggots', 'germinating peas', 'locusts'])
    p = person(r)
    if D == 1:
        return NQ(r, f'In a respirometer, the fluid in a capillary tube of radius {fx(rr, 2)} mm moved {dist} mm. What volume of oxygen was taken up? (volume = πr²h)', vol, [math.pi * dmm ** 2 * dist, 2 * math.pi * rr * dist, vol / 10, rr * dist], ' mm³',
                  f'π × {fx(rr, 2)}² × {dist} = {sf(vol, 3)} mm³.')
    st = f'{p} placed {fx(mass, 1)} g of {org} in a respirometer containing soda lime at 25 °C. The coloured fluid in the capillary tube (internal diameter {fx(dmm, 1)} mm) moved {dist} mm in {tmin} minutes.'
    parts = [P_('Calculate the volume of oxygen taken up, in mm³.', f'{sf(vol, 3)} mm³', f'radius = {fx(rr, 2)} mm [1]; π × {fx(rr, 2)}² × {dist} = {sf(vol, 3)} mm³ [1] [2]'),
             P_('Calculate the rate of oxygen uptake in mm³ g⁻¹ min⁻¹.', f'{sf(rate, 3)} mm³ g⁻¹ min⁻¹', f'{sf(vol, 3)} ÷ {tmin} ÷ {fx(mass, 1)} [1] = {sf(rate, 3)} [1] [2]'),
             P_('Explain why the fluid moved towards the organisms.', 'Oxygen was taken up and the CO₂ released was absorbed by the soda lime, so the volume (pressure) of gas in the tube fell.', 'O₂ used [1]; CO₂ absorbed so volume falls [1] [2]'),
             P_('Suggest why the respirometer was kept in a water bath during the experiment.', 'Changes in temperature would change the gas volume / rate of respiration; keeping temperature constant makes it a controlled variable.', '[1]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


RESP_T = {'setup': lambda r, p: f'{p} measured the rate of respiration of 5 g samples of germinating seeds at different temperatures using a respirometer containing soda lime. The distance moved by the fluid in the capillary tube in 10 minutes was recorded.',
          'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 15, 20, 25, 30, 35], [5, 15, 25, 35, 45], [10, 20, 30, 40, 50]]),
          'dv': ('distance moved by fluid in 10 minutes', 'mm'), 'y': lambda x, k: max(1.0, k * 6 * math.exp(0.065 * x) * (1 if x <= 38 else math.exp(-0.25 * (x - 38)))), 'dp': 0,
          'controls': ['mass of seeds', 'type and age of seeds', 'volume of soda lime', 'time allowed for equilibration', 'diameter of capillary tube', 'time interval'],
          'why': ('As temperature rises, enzymes (e.g. dehydrogenases) and substrates have more kinetic energy, so there are more successful collisions and respiration is faster; at high temperatures enzymes denature and the rate falls.', 'kinetic energy / collisions [1]; enzymes in respiration named [1]; denaturation at high temperature [1] [3]'),
          'improve': ['use a thermostatically controlled water bath', 'use a syringe to reset the fluid and a larger number of seeds', 'use a compensating tube with glass beads to allow for pressure changes'],
          'control': 'Set up an identical respirometer with an equal volume of glass beads (or boiled seeds) instead of live seeds; any fluid movement is then due to temperature or pressure changes, not respiration.',
          'extra': [lambda r, d: ('The capillary tube has a radius of 0.5 mm. Calculate the volume of oxygen absorbed at the highest temperature tested.', f'{sf(math.pi * 0.25 * d["means"][-1], 3)} mm³', f'π × 0.5² × {fx(d["means"][-1], 1)} [1] = {sf(math.pi * 0.25 * d["means"][-1], 3)} mm³ [1] [2]')]}
add_practical(t, RESP_T, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))

DCPIP_Y = {'setup': lambda r, p: f'{p} investigated the effect of glucose concentration on the respiration of yeast. 2 cm³ of methylene blue was added to 10 cm³ of yeast suspension in glucose solution at 30 °C, and the time taken for the blue colour to disappear was recorded.',
           'iv': ('glucose concentration', '%'), 'xs': lambda r: r.choice([[0.5, 1, 2, 4, 6], [1, 2, 3, 4, 5], [0.25, 0.5, 1, 2, 4]]),
           'dv': ('time for methylene blue to decolourise', 's'), 'y': lambda x, k: k * (60 + 600 / (1 + 2.2 * x)), 'dp': 0,
           'controls': ['temperature', 'volume and concentration of yeast suspension', 'volume of methylene blue', 'type of yeast', 'time yeast was activated before the test'],
           'why': ('With more glucose, more substrate is available for glycolysis and Krebs cycle dehydrogenases, so hydrogen is released faster and methylene blue is reduced faster; at high concentrations another factor (enzyme activity) limits the rate.', 'more substrate [1]; dehydrogenases reduce dye faster [1]; levels off as another factor limits [1] [3]'),
           'improve': ['use a colorimeter to judge the end point', 'compare against a colour standard of fully decolourised suspension', 'do not shake the tubes, as oxygen reoxidises the dye'],
           'control': 'Use boiled yeast (or no yeast) with the same glucose solution and methylene blue; it should stay blue, showing that the colour change is caused by respiring yeast.',
           'extra': [lambda r, d: ('Calculate the rate of respiration, as 1000 ÷ time, for the highest glucose concentration.', f'{fx(1000 / d["means"][-1], 2)} s⁻¹', f'1000 ÷ {fx(d["means"][-1], 1)} = {fx(1000 / d["means"][-1], 2)} [1]')]}
add_practical(t, DCPIP_Y, C3D=(2, 3, 4), C4D=(3, 4, 5))

longs(t, [('Describe how you would use a respirometer to investigate the effect of temperature on the rate of oxygen uptake by germinating seeds.', 'Seeds on gauze above KOH/soda lime; control tube with glass beads of equal volume; water bath at set temperatures (e.g. 10–40 °C); equilibrate 10 min with tap open; close; record distance moved by fluid in set time; volume = πr²h; repeat 3 times; same mass of seeds; reset with syringe; calculate rate per gram per minute.',
           'apparatus and KOH [1]; control tube [1]; range of temperatures / water bath [1]; equilibration [1]; measurement and πr²h [1]; controlled variables [1]; repeats and rate calculation [1] [7]'),
          ('Plan an investigation, using a redox indicator, to determine the effect of temperature on the rate of respiration of yeast.', 'IV temperature (five values, 20–60 °C, water bath); DV time for methylene blue/DCPIP to decolourise; same volume/concentration of yeast and glucose; equilibrate separately; add dye, start timer; colour standard for end point; no shaking; repeat ×3, mean; rate = 1/time; control with boiled yeast; safety.',
           'variables identified [2]; method of measuring end point [1]; controlled variables [2]; repeats/rate [1]; control [1] [7]')])
t1e = t

CHAPTERS[1] = [t1a, t1b, t1c, t1d, t1e]


# ===================================================================== 2 Photosynthesis
t = T('Photosynthesis as an energy transfer process: chloroplast structure and photosynthetic pigments; chromatography', 'photosynthesis as an energy transfer process')
facts(t, [('photosystem', 'a cluster of light-harvesting pigment molecules (antenna complex) around a reaction centre containing chlorophyll a, in the thylakoid membrane'),
          ('absorption spectrum', 'a graph showing the amount of light of each wavelength absorbed by a pigment'),
          ('action spectrum', 'a graph showing the rate of photosynthesis at each wavelength of light'),
          ('accessory pigment', 'a pigment such as chlorophyll b or a carotenoid that absorbs light of other wavelengths and passes the energy to chlorophyll a'),
          ('thylakoid', 'a flattened membrane sac inside a chloroplast containing photosystems, electron carriers and ATP synthase'),
          ('granum', 'a stack of thylakoids in a chloroplast, giving a large surface area for the light-dependent reactions'),
          ('stroma', 'the fluid matrix of a chloroplast that contains the enzymes of the Calvin cycle, starch grains, 70S ribosomes and circular DNA'),
          ('Rf value', 'the distance moved by a pigment spot divided by the distance moved by the solvent front in chromatography')])
mcqs(t, [('Which colours of light are absorbed most strongly by chlorophyll a?', 'Blue and red', 'Peaks near 430 nm and 660 nm; green is reflected.', ['Green and yellow', 'Red and green', 'Yellow and orange']),
         ('Where in the chloroplast does the Calvin cycle take place?', 'Stroma', 'Light-independent reactions occur in the stroma.', ['Thylakoid membrane', 'Thylakoid space (lumen)', 'Outer membrane']),
         ('Which pigment is found at the reaction centre of both photosystems?', 'Chlorophyll a', 'P680 (PSII) and P700 (PSI) are forms of chlorophyll a.', ['Chlorophyll b', 'Carotene', 'Xanthophyll']),
         ('Which pigment usually has the highest Rf value in paper chromatography with a non-polar solvent?', 'Carotene', 'Carotene is the least polar and moves furthest.', ['Chlorophyll b', 'Chlorophyll a', 'Xanthophyll']),
         ('What is the main role of carotenoids in the chloroplast?', 'To absorb light of wavelengths not absorbed by chlorophyll and to protect chlorophyll from damage', 'Accessory pigments widen the absorption range and are photoprotective.', ['To fix carbon dioxide', 'To split water', 'To store starch'])])
shorts(t, [('State the equation for the calculation of an Rf value.', 'Rf = distance moved by the pigment ÷ distance moved by the solvent front.', '[1]'),
           ('Name the two products of the light-dependent reactions that are used in the Calvin cycle.', 'ATP and reduced NADP.', '[2]'),
           ('State two ways in which a chloroplast is adapted for photosynthesis.', 'Large surface area of thylakoid membranes (grana) for pigments and electron carriers; stroma contains Calvin cycle enzymes; double envelope keeps enzymes in; DNA and ribosomes to make own proteins; grana close to stroma.', 'any two [2]')])
explain(t, [('Explain why photosynthesis is described as an energy transfer process.', 'Light energy is absorbed by chlorophyll and transferred to chemical energy in ATP and reduced NADP, and then to chemical energy in carbohydrates such as triose phosphate.', 'light energy absorbed [1]; to ATP / reduced NADP [1]; to carbohydrate [1] [3]'),
            ('Explain the difference between an absorption spectrum and an action spectrum, and why the two are similar in shape.', 'Absorption: light absorbed by a pigment at each wavelength; action: rate of photosynthesis at each wavelength; similar because the light absorbed by the pigments is what drives photosynthesis.', 'absorption defined [1]; action defined [1]; absorbed light used in photosynthesis [1] [3]'),
            ('Explain why a mixture of pigments is more advantageous to a plant than chlorophyll a alone.', 'Different pigments absorb different wavelengths, so a wider range of the light spectrum is used and passed to the reaction centre, increasing the rate of photosynthesis.', 'different wavelengths absorbed [1]; energy passed to reaction centre / more light used [1] [2]'),
            ('Explain how chromatography separates photosynthetic pigments.', 'Pigments differ in solubility in the solvent and in attraction to the paper/stationary phase; more soluble, less strongly adsorbed pigments travel further with the solvent, so pigments form separate spots.', 'solubility in solvent [1]; adsorption to stationary phase [1]; different distances [1] [3]'),
            ('Explain how the thylakoid membranes are adapted for the light-dependent reactions.', 'Large surface area in grana for many photosystems; contain pigments arranged in photosystems, electron carriers and ATP synthase; enclose a small lumen for building a proton gradient.', 'surface area [1]; photosystems / carriers / ATP synthase [1]; lumen for proton gradient [1] [3]')])
myths(t, [('Plants absorb green light best, which is why they look green.', 'Chlorophyll absorbs red and blue light and reflects (or transmits) green light, so leaves look green.'),
          ('The Calvin cycle takes place in the thylakoids.', 'The Calvin cycle takes place in the stroma; the light-dependent reactions take place in the thylakoid membranes.'),
          ('The pigment with the lowest Rf value is the most soluble in the solvent.', 'The lowest Rf pigment is the least soluble / most strongly adsorbed; the most soluble travels furthest.')])
mcqs(t, [('A leaf extract is separated by chromatography. Spot X moved 3.2 cm when the solvent moved 8.0 cm. What is the Rf of X?', '0.40', '3.2 ÷ 8.0 = 0.40.', ['2.5', '0.25', '4.8']),
         ('An action spectrum shows a high rate of photosynthesis at 480 nm, where chlorophyll a absorbs little light. What is the best explanation?', 'Accessory pigments such as carotenoids absorb this light and pass energy to chlorophyll a', 'Carotenoids absorb 400–500 nm.', ['Green light is absorbed by chlorophyll a', 'Light at 480 nm is used directly in the Calvin cycle', 'Chlorophyll a reflects light at 480 nm'])], D=(2, 3), C='C2')

PIGMENTS = [('carotene', 'orange-yellow', 0.95), ('xanthophyll', 'yellow', 0.71), ('chlorophyll a', 'blue-green', 0.65), ('chlorophyll b', 'yellow-green', 0.45), ('phaeophytin', 'grey', 0.81)]


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def rf_calc(r, D):
    front = round(r.uniform(7.0, 12.0), 1)
    pg = r.sample(PIGMENTS, 3)
    pg.sort(key=lambda x: -x[2])
    noise = [round(x[2] + r.uniform(-0.03, 0.03), 2) for x in pg]
    dists = [round(front * v, 1) for v in noise]
    rfs = [d / front for d in dists]
    p = person(r)
    if D == 1:
        i = r.randrange(3)
        return NQ(r, f'In a chromatogram of leaf pigments the solvent front moved {fx(front, 1)} cm and a {pg[i][1]} spot moved {fx(dists[i], 1)} cm. What is the Rf value of the spot?', rfs[i], [front / dists[i], 1 - rfs[i], dists[i] / 10], '',
                  f'Rf = {fx(dists[i], 1)} ÷ {fx(front, 1)} = {fx(rfs[i], 2)}.', f=lambda v: fx(v, 2))
    tbl = '; '.join(f'{n}: {fx(v, 2)}' for n, _, v in sorted(PIGMENTS, key=lambda x: -x[2]))
    st = (f'{p} separated the pigments in a leaf extract by thin-layer chromatography. The solvent front moved {fx(front, 1)} cm. Three spots were seen: '
          + ', '.join(f'spot {chr(65 + j)} ({pg[j][1]}) {fx(dists[j], 1)} cm' for j in range(3)) + f' from the origin. Published Rf values for this solvent are: {tbl}.')
    parts = [P_('Calculate the Rf value of each spot.', '; '.join(f'{chr(65 + j)} {fx(rfs[j], 2)}' for j in range(3)), 'distance ÷ solvent front [1]; all three correct [1] [2]'),
             P_('Use the Rf values to identify the pigments.', '; '.join(f'{chr(65 + j)} = {pg[j][0]}' for j in range(3)), 'two correct [1]; all three [1] [2]'),
             P_('Explain why the origin line is drawn in pencil and kept above the level of the solvent.', 'Pencil (graphite) does not dissolve and run in the solvent; if the origin were below the solvent the pigments would dissolve into the solvent in the beaker.', 'pencil insoluble [1]; pigments would dissolve into solvent [1] [2]'),
             P_('Suggest why thin-layer chromatography gives better separation than paper chromatography.', 'The finer, more uniform stationary phase gives faster runs and sharper, more compact spots.', '[1]')]
    if D >= 4:
        parts.append(P_('Explain why the chromatogram should be marked as soon as it is removed from the tank.', 'The solvent front evaporates quickly and pigments fade in light, so the positions must be recorded at once.', '[2]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def spectrum_case(r, D):
    alga = r.choice(['a red alga from deep water', 'a brown seaweed', 'a cyanobacterium', 'a shade plant from a rainforest floor'])
    pk = r.choice([500, 520, 540, 560])
    st = f'Researchers in {city(r)} measured the action spectrum of {alga}. Unlike a typical land plant, its rate of photosynthesis was high at {pk} nm, a wavelength that chlorophyll a absorbs poorly.'
    parts = [P_('Suggest an explanation for the high rate of photosynthesis at this wavelength.', f'The organism has accessory pigments (e.g. phycoerythrin / fucoxanthin) that absorb light at about {pk} nm and pass the energy to chlorophyll a in the reaction centre.', 'accessory pigment [1]; absorbs this wavelength [1]; energy passed to reaction centre [1] [3]'),
             P_('Explain why this is an advantage for the organism in its habitat.', 'Red and blue light are absorbed by water (or by the canopy), so the light reaching it is mainly green/blue-green; pigments that absorb these wavelengths allow photosynthesis.', 'light quality in habitat [1]; can use available wavelengths [1] [2]'),
             P_('Describe how you could separate and identify the pigments of this organism.', 'Grind with solvent (propanone), spot repeatedly on origin of TLC plate, run in non-polar solvent in a closed tank, mark solvent front, calculate Rf values and compare with known values.', 'extraction [1]; concentrated spot [1]; run solvent and mark front [1]; Rf compared [1] [4]'),
             P_('Explain how the structure of the chloroplast allows the light-dependent and light-independent reactions to take place at the same time.', 'Light-dependent reactions on thylakoid membranes and Calvin cycle enzymes in the stroma are separate compartments, close together, so ATP and reduced NADP pass directly to the stroma.', 'separate locations [1]; products pass directly to stroma [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the structure of a chloroplast and explain how it is adapted for photosynthesis.', 'Double envelope; thylakoids stacked into grana joined by intergranal lamellae; photosystems, electron carriers and ATP synthase in thylakoid membranes; lumen for proton gradient; stroma with Calvin cycle enzymes (rubisco), starch grains, lipid droplets, 70S ribosomes, circular DNA.',
           'envelope [1]; grana / thylakoids and surface area [2]; photosystems and pigments [1]; lumen [1]; stroma enzymes [1]; DNA/ribosomes [1] [7]'),
          ('Describe how chromatography can be used to separate photosynthetic pigments, and explain the significance of the different pigments to the plant.', 'Extraction with solvent; concentrated spot on origin; solvent below origin; tank lid; mark front; Rf values. Chlorophyll a primary pigment at reaction centres; chlorophyll b, carotenoids accessory pigments absorb other wavelengths and pass energy; carotenoids protect chlorophyll; wider absorption range.',
           'method [3]; Rf [1]; role of chlorophyll a [1]; accessory pigments [2] [7]')])
t2a = t

# ---------------------------------------------------------------------
t = T('Light-dependent reactions: cyclic and non-cyclic photophosphorylation and photolysis', 'light-dependent reactions')
facts(t, [('photolysis', 'the splitting of water by light energy (at photosystem II) into protons, electrons and oxygen'),
          ('photophosphorylation', 'the synthesis of ATP from ADP and Pi using energy from light, by chemiosmosis in the thylakoid membranes'),
          ('non-cyclic photophosphorylation', 'the light-driven flow of electrons from water through PSII and PSI to NADP, producing ATP, reduced NADP and oxygen'),
          ('cyclic photophosphorylation', 'the flow of electrons from PSI back to the electron transport chain and back to PSI, producing ATP only'),
          ('NADP', 'nicotinamide adenine dinucleotide phosphate: the coenzyme that accepts electrons and protons at the end of non-cyclic photophosphorylation'),
          ('photoactivation', 'the excitation of electrons in chlorophyll to a higher energy level when the pigment absorbs light')])
mcqs(t, [('Which photosystem is involved in cyclic photophosphorylation?', 'Photosystem I only', 'Electrons from PSI return via carriers to PSI.', ['Photosystem II only', 'Both photosystems', 'Neither photosystem']),
         ('What is the source of the oxygen released in photosynthesis?', 'Water', 'Photolysis: 2H₂O → 4H⁺ + 4e⁻ + O₂.', ['Carbon dioxide', 'Glucose', 'RuBP']),
         ('Which products are formed in non-cyclic but not in cyclic photophosphorylation?', 'Reduced NADP and oxygen', 'Cyclic makes only ATP.', ['ATP only', 'ATP and oxygen', 'Glucose and ATP']),
         ('Where are protons pumped during the light-dependent reactions?', 'Into the thylakoid space (lumen)', 'Protons accumulate in the lumen and flow out through ATP synthase into the stroma.', ['Into the stroma', 'Out of the chloroplast', 'Into the intermembrane space']),
         ('What replaces the electrons lost from photosystem II?', 'Electrons from photolysis of water', 'Water is the electron donor.', ['Electrons from photosystem I', 'Electrons from reduced NADP', 'Electrons from ATP'])])
shorts(t, [('State the three products of photolysis of water.', 'Protons (H⁺), electrons and oxygen.', '[2]'),
           ('State the final electron acceptor in non-cyclic photophosphorylation.', 'NADP (forming reduced NADP).', '[1]')])
explain(t, [('Describe the role of photosystem II in non-cyclic photophosphorylation.', 'Light absorbed by PSII excites electrons in the chlorophyll a reaction centre to a higher energy level; they are emitted and passed to the electron transport chain; electrons are replaced by photolysis of water, releasing oxygen and protons.', 'light excites electrons [1]; passed to ETC [1]; replaced from photolysis [1]; O₂ and H⁺ produced [1] [4]'),
            ('Explain how ATP is made by chemiosmosis in the chloroplast.', 'Energy from electrons in the ETC pumps protons from the stroma into the thylakoid lumen; protons from photolysis add to this; protons diffuse back into the stroma through ATP synthase, driving ADP + Pi → ATP.', 'proton pumping into lumen [1]; photolysis adds H⁺ [1]; diffusion through ATP synthase [1]; ATP made [1] [4]'),
            ('Explain why cyclic photophosphorylation is useful to a plant.', 'It provides extra ATP without reduced NADP; the Calvin cycle needs ATP and reduced NADP in a 3:2 ratio, and ATP is needed for other processes such as active transport in guard cells.', 'ATP only [1]; extra ATP for Calvin cycle ratio / other processes [1] [2]'),
            ('Compare cyclic and non-cyclic photophosphorylation.', 'Both: in thylakoid membranes, light excites electrons, ETC and chemiosmosis make ATP. Cyclic: PSI only, electrons return to PSI, no photolysis, no O₂, no reduced NADP. Non-cyclic: PSII and PSI, photolysis, O₂ released, reduced NADP formed.', 'similarity [1]; photosystems [1]; photolysis/O₂ [1]; reduced NADP [1] [4]')])
myths(t, [('The oxygen released by plants comes from carbon dioxide.', 'The oxygen comes from the photolysis of water at photosystem II; the oxygen in CO₂ ends up in carbohydrate and water.'),
          ('Cyclic photophosphorylation produces reduced NADP.', 'Cyclic photophosphorylation produces only ATP; electrons return to PSI rather than reducing NADP.'),
          ('Light energy is used directly to make glucose in the light-dependent reactions.', 'Light energy is used to make ATP and reduced NADP; carbohydrate is made in the Calvin cycle using these products.')])
mcqs(t, [('DCMU blocks electron flow from photosystem II to the electron transport chain. Which process will continue in isolated chloroplasts treated with DCMU in the light?', 'Cyclic photophosphorylation', 'PSI cycling does not need PSII.', ['Oxygen release', 'Reduction of NADP by electrons from water', 'Photolysis of water at its normal rate']),
         ('Isolated chloroplasts are illuminated in a solution containing DCPIP, which becomes colourless. What does this show?', 'Electrons from the light-dependent reactions have reduced DCPIP', 'DCPIP acts as an artificial electron acceptor in place of NADP (the Hill reaction).', ['Carbon dioxide has been fixed', 'Starch has been made', 'The chloroplasts have been killed'])], D=(2, 3), C='C2')


HILL = {'setup': lambda r, p: f'{p} extracted chloroplasts from spinach leaves into ice-cold buffer. Equal volumes of chloroplast suspension and DCPIP solution were placed at different distances from a lamp and the time taken for the blue colour to disappear was recorded.',
        'iv': ('distance from the lamp', 'cm'), 'xs': lambda r: r.choice([[10, 15, 20, 30, 40], [5, 10, 20, 30, 40, 50], [10, 20, 30, 40, 50]]),
        'dv': ('time for DCPIP to decolourise', 's'), 'y': lambda x, k: k * (40 + 0.12 * x * x), 'dp': 0,
        'controls': ['temperature', 'volume of chloroplast suspension', 'volume and concentration of DCPIP', 'wavelength / colour of light (same lamp)', 'pH of buffer'],
        'why': ('Further from the lamp the light intensity is lower (∝ 1/d²), so fewer electrons are excited in the photosystems per second; DCPIP accepts these electrons in place of NADP, so it is reduced more slowly.', 'light intensity falls with distance / inverse square [1]; fewer electrons excited [1]; DCPIP is electron acceptor [1] [3]'),
        'improve': ['use a colorimeter to judge the end point', 'use a heat filter (water bath / glass of water) between lamp and tubes', 'carry out the experiment in a darkened room'],
        'control': 'An identical tube wrapped in aluminium foil (kept in the dark): DCPIP should stay blue, showing that light is needed. A tube with boiled chloroplasts shows that functional chloroplasts are required.',
        'extra': [lambda r, d: ('Calculate the relative light intensity, 1/d², at the closest distance tested.', f'{sf(1 / d["xs"][0] ** 2, 3)} cm⁻²', f'1 ÷ {d["xs"][0]}² = {sf(1 / d["xs"][0] ** 2, 3)} [1]'),
                  lambda r, d: ('Explain why the chloroplasts were kept in ice-cold buffer.', 'Low temperature slows enzymes that might damage chloroplasts; buffer keeps pH constant and isotonic solution prevents chloroplasts bursting.', 'cold reduces enzyme damage [1]; buffer / isotonic [1] [2]')]}
add_practical(t, HILL, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (2, 3, 4, 5), 'short')
def ld_predict(r, D):
    sc = r.choice([('PSII is inhibited by a herbicide', 'Oxygen release and reduced NADP production stop; only cyclic photophosphorylation (ATP) continues.', 'O₂ stops [1]; NADP not reduced [1]; cyclic ATP may continue [1] [3]'),
                   ('the thylakoid membranes are made leaky to protons', 'ATP production falls because no proton gradient can form, though electron flow (and NADP reduction) may continue.', 'no proton gradient [1]; ATP falls [1] [2]'),
                   ('all NADP in the stroma has been reduced', 'Non-cyclic flow stops because there is no electron acceptor; cyclic photophosphorylation increases to make ATP.', 'non-cyclic stops [1]; cyclic increases [1] [2]'),
                   ('the light intensity is suddenly doubled (CO₂ not limiting)', 'More electrons are excited per second so the rate of ATP and reduced NADP production and oxygen release increase.', 'more excitation [1]; more ATP/NADPH/O₂ [1] [2]'),
                   ('water labelled with ¹⁸O is supplied to the plant', 'The labelled oxygen appears in the oxygen gas released, because O₂ comes from photolysis of water.', 'label in O₂ [1]; photolysis [1] [2]'),
                   ('chloroplasts are illuminated with only light of wavelength 700 nm', 'PSI is excited but PSII (680 nm) much less, so mainly cyclic photophosphorylation occurs; little O₂ or reduced NADP is produced.', 'PSI excited [1]; mostly cyclic / little O₂ [1] [2]')])
    what, ans, key = sc
    p = person(r)
    st = r.choice([f'{p} predicts the effect on the light-dependent reactions when {what}. Explain what {p} should predict.', f'Explain the effect on the light-dependent reactions in a chloroplast if {what}.',
                   f'In an experiment in {city(r)}, {what}. Predict and explain the effect on the products of the light-dependent reactions.'])
    return Q(st, ans, key, 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def ld_case(r, D):
    o2 = r.randint(30, 90)
    st = f'A suspension of isolated chloroplasts in buffer released {o2} μmol of oxygen per hour per mg chlorophyll when illuminated with an artificial electron acceptor present, but almost none when the acceptor was absent.'
    parts = [P_(f'Calculate the number of μmol of water split per hour per mg chlorophyll.', f'{2 * o2} μmol', f'2H₂O → O₂ + 4H⁺ + 4e⁻ [1]; {o2} × 2 = {2 * o2} [1] [2]'),
             P_('Calculate the number of μmol of electrons released per hour per mg chlorophyll.', f'{4 * o2} μmol', f'4 e⁻ per O₂ [1]; {o2} × 4 = {4 * o2} [1] [2]'),
             P_('Explain why almost no oxygen was released without the electron acceptor.', 'Isolated chloroplasts lose their stroma NADP or it becomes fully reduced; with no acceptor, electrons cannot leave PSI, so electron flow and photolysis stop.', 'no electron acceptor [1]; electron flow / photolysis stops [1] [2]'),
             P_('Describe the route of electrons from water to NADP.', 'Water → PSII (excited by light) → electron transport chain → PSI (re-excited) → ferredoxin/NADP reductase → NADP.', 'PSII [1]; ETC [1]; PSI to NADP [1] [3]'),
             P_('Explain how the light-dependent reactions produce a proton gradient across the thylakoid membrane.', 'Protons from photolysis are released into the lumen; energy from electrons in the ETC pumps protons from the stroma into the lumen; NADP reduction removes protons from the stroma.', 'photolysis in lumen [1]; pumping [1]; NADP reduction removes stroma H⁺ [1] [3]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the light-dependent reactions of photosynthesis.', 'Light absorbed by photosystems; electrons excited in reaction centre chlorophyll a; PSII → ETC → PSI → NADP; photolysis replaces electrons from PSII, releasing O₂ and H⁺; energy from ETC pumps H⁺ into lumen; ATP synthase chemiosmosis; reduced NADP; cyclic: PSI electrons return to ETC, ATP only.',
           'photoactivation [1]; non-cyclic route [2]; photolysis [1]; chemiosmosis [2]; cyclic [1] [7]'),
          ('Compare the production of ATP in mitochondria and chloroplasts.', 'Both chemiosmosis, ETC in membranes, ATP synthase, proton gradient. Mitochondria: energy from reduced NAD/FAD (oxidation of substrates), protons into intermembrane space, O₂ final acceptor forming water. Chloroplasts: energy from light, protons into thylakoid lumen, water is electron donor, NADP final acceptor, O₂ released.',
           'similarities [2]; energy source [1]; proton location [1]; electron source / acceptor [2] [6]')])
t2b = t

# ---------------------------------------------------------------------
t = T('Light-independent reactions: the Calvin cycle', 'light-independent reactions')
facts(t, [('Calvin cycle', 'the cycle of reactions in the stroma in which CO₂ is fixed by RuBP, reduced to triose phosphate using ATP and reduced NADP, and RuBP is regenerated'),
          ('RuBP', 'ribulose bisphosphate: a five-carbon compound that accepts carbon dioxide in the Calvin cycle'),
          ('rubisco', 'ribulose bisphosphate carboxylase: the enzyme that catalyses the fixation of CO₂ by combining it with RuBP'),
          ('GP', 'glycerate 3-phosphate: the three-carbon compound formed when the unstable six-carbon intermediate splits'),
          ('triose phosphate', 'the three-carbon sugar formed by reduction of GP; used to make glucose, amino acids and lipids and to regenerate RuBP'),
          ('carbon fixation', 'the incorporation of inorganic carbon (CO₂) into an organic molecule, here RuBP')])
mcqs(t, [('Which molecule combines with carbon dioxide in the Calvin cycle?', 'Ribulose bisphosphate (RuBP)', 'RuBP (5C) + CO₂ → 2 GP, catalysed by rubisco.', ['Glycerate 3-phosphate', 'Triose phosphate', 'Oxaloacetate']),
         ('Which products of the light-dependent reactions are used to reduce GP to triose phosphate?', 'ATP and reduced NADP', 'ATP provides energy and reduced NADP provides hydrogen.', ['ATP and oxygen', 'Reduced NAD and ATP', 'Oxygen and reduced NADP']),
         ('How many carbon atoms are in a molecule of GP?', '3', 'GP is glycerate 3-phosphate (3C).', ['5', '6', '2']),
         ('What fraction of the triose phosphate made in the Calvin cycle is used to regenerate RuBP?', 'Five sixths', 'Of every six TP, five regenerate three RuBP; one is used to make products.', ['One sixth', 'One half', 'All of it']),
         ('Which substance is used in the regeneration of RuBP from triose phosphate?', 'ATP', 'Phosphorylation by ATP regenerates RuBP.', ['Reduced NADP', 'Oxygen', 'Water'])])
shorts(t, [('Name the enzyme that fixes carbon dioxide in the Calvin cycle.', 'Rubisco (ribulose bisphosphate carboxylase).', '[1]'),
           ('State three uses of triose phosphate in a plant cell, other than regenerating RuBP.', 'Synthesis of glucose (then sucrose, starch, cellulose); glycerol and fatty acids (lipids); amino acids; respiration.', 'any three [3]')])
explain(t, [('Explain why the Calvin cycle stops soon after a plant is placed in the dark.', 'In the dark, the light-dependent reactions stop so no ATP or reduced NADP is made; GP cannot be reduced to TP and RuBP cannot be regenerated, so CO₂ fixation stops.', 'no ATP / reduced NADP [1]; GP not reduced [1]; RuBP not regenerated [1] [3]'),
            ('Explain why the Calvin cycle is described as light-independent although it does not take place for long in the dark.', 'Its reactions do not directly use light; but they depend on a continuous supply of ATP and reduced NADP from the light-dependent reactions.', 'no light used directly [1]; depends on products of LDR [1] [2]'),
            ('Describe the three main stages of the Calvin cycle.', 'Fixation: CO₂ + RuBP → 2 GP (rubisco); reduction: GP → TP using ATP and reduced NADP; regeneration: most TP converted to RuBP using ATP.', 'fixation [1]; reduction [1]; regeneration [1] [3]'),
            ('Explain why rubisco is often described as the most abundant protein on Earth.', 'Rubisco is a slow enzyme (few reactions per second) and also reacts with oxygen, so leaves must contain very large amounts to fix enough CO₂.', 'slow / low turnover [1]; large amounts needed [1] [2]')])
myths(t, [('The Calvin cycle takes place only at night.', 'The Calvin cycle runs in the light, when ATP and reduced NADP are available; it stops soon after dark.'),
          ('Glucose is the first product of carbon fixation.', 'The first product is GP (glycerate 3-phosphate); glucose is made later from triose phosphate.'),
          ('Reduced NADP is used to fix carbon dioxide onto RuBP.', 'Rubisco fixes CO₂ without ATP or reduced NADP; reduced NADP is used to reduce GP to triose phosphate.')])

CALVIN = [('the light is switched off', 'GP concentration rises and RuBP concentration falls', 'RuBP still combines with CO₂ to form GP, but GP cannot be reduced (no ATP/reduced NADP) and RuBP is not regenerated'),
          ('the carbon dioxide concentration is reduced to a very low level', 'RuBP concentration rises and GP concentration falls', 'less RuBP is used in fixation, but RuBP is still regenerated from TP; GP is still reduced to TP but is not replaced'),
          ('the light intensity is increased (CO₂ still high)', 'GP falls slightly and RuBP rises', 'more ATP and reduced NADP so GP is reduced faster and RuBP regenerated faster'),
          ('the temperature is lowered from 25 °C to 5 °C', 'the rates of all steps fall, so CO₂ fixation slows', 'Calvin cycle reactions are enzyme-catalysed (e.g. rubisco), so less kinetic energy means fewer enzyme–substrate collisions'),
          ('an inhibitor of rubisco is added', 'RuBP accumulates and GP falls', 'RuBP is still regenerated from TP but cannot combine with CO₂')]


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def calvin_change(r, D):
    what, res, why = r.choice(CALVIN)
    alga = r.choice(['Chlorella', 'Scenedesmus', 'a suspension of spinach chloroplasts', 'Elodea leaves', 'a culture of cyanobacteria'])
    if D == 1:
        wrong = [x[1] for x in CALVIN if x[1] != res]
        return MQ(r, f'{alga[0].upper() + alga[1:]} is photosynthesising steadily. What happens to the levels of Calvin cycle intermediates when {what}?', cap(res), [cap(w) for w in wrong], f'{cap(res)}: {why}.')
    st = r.choice([f'{person(r)} supplies {alga} with radioactive ¹⁴CO₂ and measures the radioactivity in GP and RuBP. Then {what}. Predict and explain the changes in GP and RuBP.',
                   f'In an experiment with {alga}, {what}. Explain the effect on the Calvin cycle.'])
    return Q(st, f'{cap(res)}: {why}.', f'prediction: {res} [1]; explanation: {why} [2] [3]', 'short')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def calvin_count(r, D):
    nco2 = r.choice([1, 3, 6, 12, 18, 30, 60])
    item = r.choice(['ATP', 'reduced NADP', 'GP', 'triose phosphate', 'turns of the cycle', 'molecules of hexose'])
    per = {'ATP': 3, 'reduced NADP': 2, 'GP': 2, 'triose phosphate': 2, 'turns of the cycle': 1, 'molecules of hexose': 1 / 6}[item]
    v = nco2 * per
    if v != int(v):
        return None
    v = int(v)
    stem = f'How many {item} are {"used" if item in ("ATP", "reduced NADP") else ("needed" if item.startswith("turns") else "formed")} when {nco2} molecule{"s" if nco2 > 1 else ""} of CO₂ {"are" if nco2 > 1 else "is"} fixed in the Calvin cycle?'
    key = f'per CO₂: 3 ATP, 2 reduced NADP, 2 GP, 2 TP (one sixth of TP leaves); 6 turns per hexose. {nco2} × {fx(per, 3)} = {v}.'
    if D <= 2:
        return NQ(r, stem, v, [v * 2, max(1, v // 2), v + nco2, v * 3], '', key, f=lambda x: str(int(x)))
    st = (f'{person(r)} calculates the requirements of the Calvin cycle. ' + stem.replace('How many', 'Calculate how many').rstrip('?') + '. Show your working.')
    if D >= 4:
        st += ' Hence state the ratio of ATP to reduced NADP required and explain how the chloroplast meets this ratio.'
        return Q(st, f'{v}; ATP : reduced NADP = 3 : 2; extra ATP is supplied by cyclic photophosphorylation.', f'{key} [2]; 3 : 2 [1]; cyclic photophosphorylation [1] [4]', 'numerical')
    return Q(st, str(v), key + ' Per-CO₂ value [1]; answer [1] [2]', 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def calvin_case(r, D):
    secs = r.choice([2, 3, 5])
    st = (f'In Calvin\'s "lollipop" experiment, a suspension of Chlorella was illuminated and supplied with ¹⁴CO₂. Samples were run into hot methanol after different times and the labelled compounds separated by two-way chromatography. '
          f'After {secs} s most radioactivity was in GP; after 30 s it was also in triose phosphate, hexose phosphates and RuBP.')
    parts = [P_('Explain why the samples were run into hot methanol.', 'Hot methanol kills the cells and denatures the enzymes instantly, stopping the reactions at a known time.', 'kills / denatures enzymes [1]; stops reactions at exact time [1] [2]'),
             P_('Explain why GP was the first labelled compound.', 'CO₂ is fixed by combining with RuBP (rubisco) to form an unstable 6C compound that immediately splits into two GP.', 'RuBP + CO₂ [1]; forms GP first [1] [2]'),
             P_('Explain why radioactivity later appeared in RuBP.', 'Labelled triose phosphate is used to regenerate RuBP, so the label passes into RuBP.', 'TP regenerates RuBP [1]; label carried [1] [2]'),
             P_('Explain why two-way chromatography was used.', 'Many compounds with similar Rf values in one solvent are separated better by running in a second solvent at right angles.', '[2]'),
             P_('Describe the reduction of GP to triose phosphate.', 'GP is phosphorylated using ATP and reduced using hydrogen from reduced NADP to form triose phosphate; ADP and NADP return to the thylakoids.', 'ATP [1]; reduced NADP [1]; products return [1] [3]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the Calvin cycle and explain how it depends on the light-dependent reactions.', 'In stroma: CO₂ + RuBP (5C) → unstable 6C → 2 GP (rubisco); GP reduced to TP using ATP and reduced NADP from LDR; 5 of 6 TP regenerate RuBP using ATP; 1 TP used for glucose, sucrose, starch, amino acids, lipids; depends on ATP and reduced NADP; stops in dark; ADP and NADP return to thylakoids.',
           'fixation [2]; reduction [2]; regeneration [1]; products [1]; dependence on LDR [1] [7]'),
          ('Explain how the products of the Calvin cycle are used to make the range of organic molecules found in a plant.', 'TP → glucose (hexose phosphate) → sucrose for transport, starch for storage, cellulose for walls; TP → glycerol and acetyl CoA → fatty acids → lipids; GP/TP + nitrate (NH₂ groups) → amino acids → proteins; nucleotides; respiration.',
           'carbohydrates [2]; lipids [2]; amino acids with nitrogen [2] [6]')])
t2c = t

# ---------------------------------------------------------------------
t = T('Limiting factors and investigating the rate of photosynthesis', 'limiting factors and investigating the rate of photosynthesis')
facts(t, [('limiting factor', 'the factor that is in shortest supply relative to need and so limits the rate of a process; increasing it increases the rate'),
          ('compensation point', 'the light intensity at which the rate of photosynthesis equals the rate of respiration, so there is no net gas exchange'),
          ('inverse square law', 'the relationship that light intensity is inversely proportional to the square of the distance from a point light source'),
          ('glasshouse enrichment', 'the deliberate raising of CO₂ concentration, temperature and light in a glasshouse to remove limiting factors and increase yield')])
mcqs(t, [('At low light intensity, which factor is most likely to limit the rate of photosynthesis?', 'Light intensity', 'On the steep part of the curve, light is limiting.', ['Carbon dioxide concentration', 'Temperature', 'Chlorophyll content']),
         ('A lamp is moved from 10 cm to 20 cm from a plant. By what factor does the light intensity change?', 'It falls to one quarter', 'Intensity ∝ 1/d²: (10/20)² = 1/4.', ['It halves', 'It doubles', 'It falls to one eighth']),
         ('Why is sodium hydrogencarbonate added to the water around pondweed in a photosynthesis experiment?', 'To provide a source of carbon dioxide', 'HCO₃⁻ supplies CO₂ so it is not limiting.', ['To provide oxygen', 'To keep the pH acidic', 'To kill bacteria']),
         ('Which of these limits the rate of photosynthesis on a bright, warm day in a sealed glasshouse?', 'Carbon dioxide concentration', 'CO₂ is often limiting when light and temperature are high.', ['Light intensity', 'Oxygen concentration', 'Water potential of the soil'])])
shorts(t, [('State three factors that can limit the rate of photosynthesis.', 'Light intensity, carbon dioxide concentration, temperature (also light wavelength, water supply).', 'any three [2]'),
           ('Describe how the rate of photosynthesis of a water plant can be measured.', 'Count the bubbles of oxygen given off per minute, or collect the gas in a capillary tube / photosynthometer and measure its volume per minute.', '[2]')])
explain(t, [('Explain why increasing the temperature from 15 °C to 25 °C may have no effect on the rate of photosynthesis at low light intensity.', 'At low light intensity, light is the limiting factor; temperature affects only the enzyme-catalysed Calvin cycle, which is already limited by the supply of ATP and reduced NADP.', 'light limiting [1]; temperature affects Calvin cycle enzymes not light-dependent reactions [1] [2]'),
            ('Explain how growers can use their knowledge of limiting factors to increase crop yields in glasshouses.', 'Raise CO₂ (paraffin burners/CO₂ cylinders), supplementary lighting at suitable wavelengths and heating to optimum; each is raised until another factor limits; balance cost against extra yield.', 'CO₂ [1]; light [1]; temperature [1]; cost-effectiveness / another factor limits [1] [4]'),
            ('Explain why counting bubbles is not an accurate method of measuring the rate of photosynthesis.', 'Bubbles vary in size; some oxygen dissolves in the water or is used in respiration; gas may contain other gases; bubbles hard to count at high rates.', 'bubble size varies [1]; another valid reason [1] [2]'),
            ('Explain why the rate of oxygen production by a plant is not the same as the rate of photosynthesis.', 'Some of the oxygen produced is used in respiration by the plant, so the oxygen released is net (apparent) photosynthesis.', 'oxygen used in respiration [1]; measured = net rate [1] [2]')])
myths(t, [('If light intensity is doubled, the rate of photosynthesis will always double.', 'Only while light is the limiting factor; at higher intensities another factor such as CO₂ or temperature limits the rate.'),
          ('Increasing temperature always increases the rate of photosynthesis.', 'Above the optimum, enzymes such as rubisco denature and stomata may close, so the rate falls; at low light, temperature has little effect.'),
          ('Moving a lamp twice as far away halves the light intensity.', 'Light intensity is proportional to 1/d², so doubling the distance reduces intensity to one quarter.')])
relation(t, 'C2', (2, 3), 'light intensity ∝ 1/d²', 'light intensity at the plant', {'distance from the lamp': -2},
         ['In a pondweed experiment, a lamp is used as the only light source.', 'A student investigates the Hill reaction using a bench lamp.', 'A plant in a dark room is lit by a single bulb.'])

PONDWEED = {'setup': lambda r, p: f'{p} placed a piece of Elodea in 0.5% sodium hydrogencarbonate solution at 25 °C and counted the bubbles released per minute with a lamp at different distances.',
            'iv': ('distance from the lamp', 'cm'), 'xs': lambda r: r.choice([[5, 10, 15, 20, 25, 30], [10, 20, 30, 40, 50], [8, 12, 16, 20, 30, 40]]),
            'dv': ('number of bubbles per minute', ''), 'y': lambda x, k: max(1, k * 60 * (1 - math.exp(-900 / (x * x * 3.5)))), 'dp': 0,
            'controls': ['temperature (use a water bath / heat filter)', 'concentration of sodium hydrogencarbonate', 'the same piece of pondweed', 'time allowed to adjust to each light intensity', 'background light (dark room)'],
            'why': ('Closer to the lamp the light intensity is higher (∝ 1/d²), so more light energy is absorbed and the light-dependent reactions are faster, producing more oxygen; at the closest distances another factor such as CO₂ concentration or temperature limits the rate, so it levels off.', 'light intensity and distance [1]; faster LDR / more O₂ [1]; another factor limits at high intensity [1] [3]'),
            'improve': ['collect the gas in a photosynthometer and measure the volume', 'place a heat filter (beaker of water) between lamp and plant', 'allow 5 minutes acclimatisation at each distance'],
            'extra': [lambda r, d: ('Calculate the light intensity at the nearest distance relative to the furthest distance.', f'{fx((d["xs"][-1] / d["xs"][0]) ** 2, 1)} times greater', f'intensity ∝ 1/d² [1]; ({d["xs"][-1]} ÷ {d["xs"][0]})² = {fx((d["xs"][-1] / d["xs"][0]) ** 2, 1)} [1] [2]')]}
add_practical(t, PONDWEED, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (2, 3, 4, 5), 'case')
def limit_graph(r, D):
    lo, hi = r.choice([(0.01, 0.1), (0.02, 0.15), (0.03, 0.12)])
    t1, t2 = r.choice([(15, 25), (20, 30), (10, 20)])
    plat = [round(r.uniform(18, 26), 0), round(r.uniform(32, 44), 0), round(r.uniform(44, 60), 0)]
    st = (f'A graph shows the rate of photosynthesis of a crop plant against light intensity under three conditions: A — {lo}% CO₂ at {t1} °C (levels off at {fx(plat[0])} units); '
          f'B — {hi}% CO₂ at {t1} °C (levels off at {fx(plat[1])} units); C — {hi}% CO₂ at {t2} °C (levels off at {fx(plat[2])} units). At low light intensities the three curves are identical.')
    parts = [P_('State the limiting factor at low light intensities. Give a reason.', 'Light intensity: all three curves are the same, so CO₂ and temperature have no effect; the rate increases as light increases.', 'light intensity [1]; curves identical / rate rises with light [1] [2]'),
             P_('Identify the factor limiting the rate for curve A at high light intensity. Explain your answer using the data.', f'CO₂ concentration: raising CO₂ from {lo}% to {hi}% (curve B) increased the plateau from {fx(plat[0])} to {fx(plat[1])} units.', 'CO₂ [1]; comparison A and B with data [1] [2]'),
             P_('Identify the factor limiting the rate for curve B at high light intensity. Explain your answer.', f'Temperature: raising the temperature to {t2} °C (curve C) raised the plateau to {fx(plat[2])} units.', 'temperature [1]; comparison B and C [1] [2]'),
             P_('Explain why increasing temperature increases the rate only at high light intensity.', 'Temperature affects the enzyme-controlled Calvin cycle (e.g. rubisco); at low light the supply of ATP/reduced NADP limits the rate instead.', 'enzymes of Calvin cycle [1]; light limits at low intensity [1] [2]'),
             P_(f'Calculate the percentage increase in the maximum rate from A to C.', f'{fx(pct(plat[0], plat[2]), 0)}%', f'({fx(plat[2])} − {fx(plat[0])}) ÷ {fx(plat[0])} × 100 = {fx(pct(plat[0], plat[2]), 0)}% [2]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4))


longs(t, [('Explain the concept of limiting factors with reference to light intensity, carbon dioxide concentration and temperature in photosynthesis.', 'Rate limited by factor in shortest supply; light: LDR, ATP/reduced NADP; rises then plateaus when another factor limits; CO₂: substrate for rubisco, RuBP fixation; temperature: enzymes of Calvin cycle, optimum, denaturation above; graphs: curves at different CO₂/temperature; at low light, temperature and CO₂ have no effect.',
           'definition [1]; light [2]; CO₂ [1]; temperature [2]; interaction/graph description [1] [7]'),
          ('Plan an investigation into the effect of light intensity on the rate of photosynthesis of a water plant.', 'IV light intensity via lamp distance (5 distances, 1/d²); DV volume of O₂ in photosynthometer per 5 min (or bubbles); controls: temperature (heat filter, water bath), NaHCO₃ concentration, same plant, wavelength, acclimatise 5 min, darkened room; repeat 3 times, mean; plot rate vs 1/d²; safety with lamp and water.',
           'IV and how varied [1]; DV and how measured [2]; controlled variables [2]; repeats/acclimatisation [1]; data processing [1] [7]')])
t2d = t

CHAPTERS[2] = [t2a, t2b, t2c, t2d]


# ===================================================================== 3 Homeostasis
t = T('Homeostasis in mammals: negative feedback and the role of hormones and nerves', 'homeostasis in mammals')
facts(t, [('homeostasis', 'the maintenance of a constant internal environment (e.g. blood glucose, core temperature, water potential) within narrow limits'),
          ('negative feedback', 'a control mechanism in which a change from the set point is detected and responses act to reverse the change and return the factor to the set point'),
          ('positive feedback', 'a mechanism in which a change causes responses that increase the change further, as in the release of oxytocin during childbirth'),
          ('receptor', 'a cell or organ that detects a stimulus, i.e. a change in a factor, and passes information to a coordinator'),
          ('effector', 'a muscle or gland that carries out a response to restore the factor to its set point'),
          ('set point', 'the ideal value of a physiological factor around which it is kept by homeostatic control'),
          ('hormone', 'a chemical messenger secreted by an endocrine gland directly into the blood and carried to target cells with specific receptors')])
mcqs(t, [('Which structure acts as the coordinator in the control of body temperature?', 'Hypothalamus', 'The hypothalamus contains the thermoregulatory centre.', ['Pituitary gland', 'Skin', 'Kidney']),
         ('Which is an example of negative feedback?', 'A fall in blood glucose causes glucagon secretion, which raises blood glucose', 'The response reverses the change.', ['Oxytocin release increases uterine contractions, causing more oxytocin release', 'Blood clotting factors activate more clotting factors', 'An action potential opens more sodium channels']),
         ('Which factor is NOT kept constant by homeostasis in mammals?', 'The volume of the stomach contents', 'Homeostasis regulates the internal environment (tissue fluid/blood).', ['Core body temperature', 'Blood glucose concentration', 'Water potential of blood']),
         ('What is the advantage of nervous coordination compared with hormonal coordination?', 'It is faster and more precisely targeted', 'Nerve impulses are rapid and go to specific effectors.', ['Its effects last longer', 'It affects many organs at once', 'It needs no receptors'])])
shorts(t, [('State three physiological factors that are controlled by homeostasis in mammals.', 'Core temperature; blood glucose concentration; water potential of the blood; pH; carbon dioxide concentration; blood pressure.', 'any three [3]'),
           ('State the components of a homeostatic control system.', 'Receptor, coordinator (control centre), effector, with negative feedback.', '[2]')])
explain(t, [('Explain why it is important to keep the water potential of the blood constant.', 'Changes in water potential of tissue fluid would cause cells to gain water by osmosis and burst, or lose water and shrink; cell metabolism depends on correct concentrations.', 'osmosis into/out of cells [1]; cells burst/shrink or metabolism disrupted [1] [2]'),
            ('Explain why the core temperature of a mammal must be kept close to 37 °C.', 'Enzymes work at an optimum; higher temperatures denature enzymes and lower temperatures reduce kinetic energy, so metabolic reactions would be slowed or stop.', 'enzymes optimum [1]; denaturation / slow reactions [1] [2]'),
            ('Describe how negative feedback keeps a factor within narrow limits.', 'A receptor detects a deviation from the set point; the coordinator sends signals to effectors; the effectors reverse the change; once normal, the stimulus is removed and the response stops.', 'receptor detects change [1]; effector response reverses it [1]; response switched off when normal [1] [3]'),
            ('Compare nervous and hormonal communication in mammals.', 'Nervous: electrical impulses along neurones, very fast, short-lived, localised to specific effectors. Hormonal: chemicals in blood, slower, longer-lasting, widespread to all cells with receptors.', 'electrical vs chemical [1]; speed [1]; duration [1]; localised vs widespread [1] [4]'),
            ('Explain why a hormone affects only certain cells in the body.', 'Only target cells have the specific receptor (on the membrane or inside the cell) that is complementary in shape to the hormone.', 'target cells have receptors [1]; complementary shape [1] [2]')])
myths(t, [('Negative feedback keeps a factor at exactly the same value all the time.', 'Negative feedback keeps a factor fluctuating within narrow limits around the set point.'),
          ('Hormones travel along nerves to their target cells.', 'Hormones are secreted into the blood and carried throughout the body; only target cells with receptors respond.'),
          ('Homeostasis controls the composition of the contents of the gut.', 'Homeostasis controls the internal environment (blood and tissue fluid); the gut contents are outside the body tissues.')])

HOMEO = [('core body temperature rises above 37.5 °C', 'thermoreceptors in the hypothalamus', 'the hypothalamus', 'sweat glands secrete more sweat; arterioles in the skin dilate; hair erector muscles relax', 'temperature falls back towards 37 °C'),
         ('blood glucose concentration rises after a meal', 'β cells in the islets of Langerhans', 'the pancreas (islets)', 'liver and muscle cells take up glucose and convert it to glycogen in response to insulin', 'blood glucose falls back to about 5 mmol dm⁻³'),
         ('the water potential of the blood falls during dehydration', 'osmoreceptors in the hypothalamus', 'the hypothalamus and posterior pituitary', 'collecting duct cells insert aquaporins in response to ADH and reabsorb more water', 'blood water potential rises back towards normal'),
         ('core body temperature falls below 36.5 °C', 'thermoreceptors in the hypothalamus and skin', 'the hypothalamus', 'skeletal muscles shiver; arterioles in the skin constrict; hair erector muscles contract; metabolism increases', 'temperature rises back towards 37 °C'),
         ('blood glucose concentration falls during exercise', 'α cells in the islets of Langerhans', 'the pancreas (islets)', 'liver cells break down glycogen to glucose (glycogenolysis) and make glucose by gluconeogenesis in response to glucagon', 'blood glucose rises back to about 5 mmol dm⁻³'),
         ('blood carbon dioxide concentration rises during exercise', 'chemoreceptors in the medulla and the carotid and aortic bodies', 'the breathing centre in the medulla', 'intercostal muscles and diaphragm contract faster and more strongly', 'CO₂ concentration falls back to normal')]


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def feedback_apply(r, D):
    stim, rec, coord, eff, out = r.choice(HOMEO)
    if D == 1:
        wrong = [h[1] for h in HOMEO if h[1] != rec]
        return MQ(r, f'Which receptors detect the change when {stim}?', cap(rec), [cap(w) for w in wrong], f'{cap(rec)}.')
    p = person(r)
    st = f'{p}, in {city(r)}, experiences a situation in which {stim}. Describe how negative feedback restores the normal value, naming the receptor, coordinator and effectors.'
    return Q(st, f'Receptor: {rec}; coordinator: {coord}; effectors/response: {eff}; result: {out}; once normal, the response is reduced (negative feedback).',
             f'receptor [1]; coordinator [1]; effector response [1]; return to set point and response switched off [1] [4]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def homeo_case(r, D):
    t0 = round(r.uniform(36.8, 37.2), 1)
    tmax = round(r.uniform(38.0, 39.2), 1)
    p = person(r)
    st = f'{p} ran a half-marathon in {city(r)} on a hot day. Core body temperature rose from {fx(t0, 1)} °C to {fx(tmax, 1)} °C during the race; {p} lost about {fx(r.uniform(1.2, 2.8), 1)} dm³ of water as sweat.'
    parts = [P_('Explain why core temperature rose during the race.', 'Muscle contraction requires much ATP from respiration; respiration is inefficient, releasing heat; heat production exceeded heat loss in hot conditions.', 'respiration releases heat [1]; production exceeds loss / hot air [1] [2]'),
             P_('Describe the responses that increase heat loss from the skin.', 'Vasodilation of arterioles in the skin so more blood flows near the surface and loses heat by radiation; sweating, heat lost as sweat evaporates; hair erector muscles relax.', 'vasodilation [1]; sweating / evaporation [1]; hairs flat [1] [3]'),
             P_('Explain why the loss of water in sweat requires a second homeostatic response.', 'Loss of water lowers blood water potential; osmoreceptors in the hypothalamus detect this and more ADH is released, so the kidneys reabsorb more water.', 'blood water potential falls [1]; osmoreceptors / ADH [1]; more water reabsorbed [1] [3]'),
             P_('Explain why this is an example of negative feedback.', 'The rise in temperature is detected and responses act to lower it back to the set point; responses decrease as temperature returns to normal.', 'response opposes change [1]; switched off near set point [1] [2]'),
             P_(f'Calculate the rise in core temperature as a percentage of the starting value.', f'{fx((tmax - t0) / t0 * 100, 1)}%', f'({fx(tmax, 1)} − {fx(t0, 1)}) ÷ {fx(t0, 1)} × 100 = {fx((tmax - t0) / t0 * 100, 1)}% [1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain the principles of homeostasis, using the control of core body temperature as an example.', 'Constant internal environment; receptor, coordinator, effector; negative feedback; thermoreceptors in skin and hypothalamus; hypothalamus as coordinator; effectors: sweat glands, arterioles (vasodilation/vasoconstriction), skeletal muscles (shivering), hair erector muscles; liver/thyroxine metabolism; responses switched off at set point; nervous and hormonal.',
           'definition [1]; components [1]; negative feedback [1]; receptors/coordinator for temperature [1]; responses to heat [1]; responses to cold [1]; nervous and hormonal roles [1] [7]')])
t3a = t

# ---------------------------------------------------------------------
t = T('Excretion: kidney structure, ultrafiltration and selective reabsorption in the nephron', 'excretion: kidney structure')
facts(t, [('excretion', 'the removal of toxic waste products of metabolism, such as urea and carbon dioxide, from the body'),
          ('deamination', 'the removal of the amine group from excess amino acids in the liver, forming ammonia, which is converted to urea'),
          ('ultrafiltration', 'the filtration of blood under high pressure in the glomerulus, through the capillary endothelium, basement membrane and podocytes, into the Bowman\'s capsule'),
          ('selective reabsorption', 'the uptake of useful substances such as glucose, amino acids, ions and water from the filtrate back into the blood, mainly in the proximal convoluted tubule'),
          ('podocyte', 'a cell of the inner wall of Bowman\'s capsule with foot-like processes that leave filtration slits'),
          ('basement membrane', 'the layer of collagen and glycoproteins between the glomerular capillary endothelium and the podocytes, which acts as the main filter'),
          ('glomerular filtration rate', 'the volume of fluid filtered from the glomeruli into the Bowman\'s capsules per minute (about 125 cm³ min⁻¹ in a human)')])
mcqs(t, [('Which substance is normally present in glomerular filtrate but absent from the urine of a healthy person?', 'Glucose', 'Glucose is filtered and then all reabsorbed in the PCT.', ['Urea', 'Sodium ions', 'Water']),
         ('Which substance is normally absent from glomerular filtrate?', 'Plasma proteins such as albumin', 'Proteins with RMM above about 69 000 are too large to pass the basement membrane.', ['Glucose', 'Urea', 'Amino acids']),
         ('Why is blood pressure in the glomerulus high?', 'The efferent arteriole has a smaller diameter than the afferent arteriole', 'Narrow efferent arteriole builds up hydrostatic pressure.', ['The glomerulus is close to the heart', 'The efferent arteriole is wider than the afferent arteriole', 'Podocytes pump blood']),
         ('Where are most glucose and amino acids reabsorbed?', 'Proximal convoluted tubule', 'Microvilli, many mitochondria and co-transporters in PCT cells.', ['Loop of Henle', 'Distal convoluted tubule', 'Collecting duct']),
         ('Where in the liver is urea made from ammonia?', 'In the ornithine cycle in hepatocytes', 'Ammonia + CO₂ → urea via the ornithine cycle.', ['In the bile duct', 'In the Kupffer cells', 'In the hepatic portal vein'])])
shorts(t, [('Name the three layers through which substances pass during ultrafiltration.', 'Capillary endothelium (with pores), basement membrane, podocytes (filtration slits) of Bowman\'s capsule.', '[3]'),
           ('State why urea must be removed from the body.', 'Urea is a toxic nitrogenous waste product of deamination; it would affect cell metabolism / water potential if it accumulated.', '[1]')])
explain(t, [('Explain how glucose is reabsorbed in the proximal convoluted tubule.', 'Sodium–potassium pumps on the basal membrane actively remove Na⁺ from PCT cells, lowering Na⁺ concentration inside; Na⁺ diffuses in from filtrate via co-transporter proteins carrying glucose with it (facilitated diffusion); glucose diffuses out into blood through carriers.', 'Na⁺ pumped out across basal membrane [1]; Na⁺ gradient [1]; co-transport of glucose [1]; glucose diffuses into blood [1] [4]'),
            ('Explain how the cells of the proximal convoluted tubule are adapted for reabsorption.', 'Microvilli give a large surface area; many mitochondria provide ATP for active transport; many co-transporter proteins; tight junctions; close to capillaries.', 'microvilli [1]; mitochondria [1]; carrier/co-transporter proteins [1] [3]'),
            ('Explain how the structure of the glomerulus and Bowman\'s capsule allows ultrafiltration.', 'Wide afferent and narrow efferent arterioles create high hydrostatic pressure; fenestrated endothelium; basement membrane acts as filter; podocytes with filtration slits; water potential gradient favours filtration.', 'pressure difference [1]; pores in endothelium [1]; basement membrane filter [1]; podocytes [1] [4]'),
            ('Explain why the concentration of urea in the filtrate increases along the nephron.', 'Urea is not actively reabsorbed (only some diffuses back), while large volumes of water are reabsorbed from the filtrate, so the urea is concentrated.', 'water reabsorbed [1]; urea mostly not reabsorbed [1] [2]'),
            ('Explain why glucose appears in the urine of a person with untreated diabetes.', 'Blood glucose concentration is so high that the filtrate contains more glucose than the co-transporters in the PCT can reabsorb; the carriers are saturated so excess glucose stays in the filtrate.', 'high blood/filtrate glucose [1]; carriers saturated [1] [2]')])
myths(t, [('Glucose is not filtered in the glomerulus, so it does not appear in urine.', 'Glucose is filtered (it is small); all of it is normally reabsorbed in the proximal convoluted tubule.'),
          ('Urine is filtered blood.', 'Filtrate contains plasma without proteins and cells; urine is the filtrate after selective reabsorption and secretion have changed its composition.'),
          ('The kidneys make urea.', 'Urea is made in the liver by deamination and the ornithine cycle; the kidneys remove it from the blood.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def filtration(r, D):
    gfr = r.choice([110, 115, 120, 125, 130])
    urine = round(r.uniform(0.6, 2.0), 1)
    pg = r.choice([4.5, 5.0, 5.5])
    urea_p, urea_u = round(r.uniform(0.25, 0.35), 2), round(r.uniform(15, 25), 1)
    reab = (gfr - urine) / gfr * 100
    if D == 1:
        return NQ(r, f'The glomerular filtration rate of a person is {gfr} cm³ min⁻¹ and urine is produced at {fx(urine, 1)} cm³ min⁻¹. What percentage of the water in the filtrate is reabsorbed?', reab,
                  [100 - reab, urine / gfr * 1000, gfr / urine], '%', f'({gfr} − {fx(urine, 1)}) ÷ {gfr} × 100 = {fx(reab, 1)}%.', f=lambda v: fx(v, 1))
    p = person(r)
    st = (f'Measurements on {p}, a healthy adult, gave: glomerular filtration rate {gfr} cm³ min⁻¹; urine production {fx(urine, 1)} cm³ min⁻¹; plasma glucose {fx(pg, 1)} mmol dm⁻³; '
          f'urea concentration {fx(urea_p, 2)} g dm⁻³ in plasma and {fx(urea_u, 1)} g dm⁻³ in urine.')
    load = gfr * pg / 1000
    parts = [P_('Calculate the percentage of the filtered water that is reabsorbed.', f'{fx(reab, 1)}%', f'({gfr} − {fx(urine, 1)}) ÷ {gfr} [1] × 100 = {fx(reab, 1)}% [1] [2]'),
             P_('Calculate the volume of filtrate produced in 24 hours, in dm³.', f'{fx(gfr * 60 * 24 / 1000, 0)} dm³', f'{gfr} × 60 × 24 = {gfr * 1440:,} cm³ [1] = {fx(gfr * 1.44, 0)} dm³ [1] [2]'),
             P_('Calculate how many times more concentrated urea is in the urine than in the plasma.', f'{fx(urea_u / urea_p, 0)} times', f'{fx(urea_u, 1)} ÷ {fx(urea_p, 2)} = {fx(urea_u / urea_p, 0)} [1]'),
             P_('Calculate the amount of glucose filtered per minute, in mmol, and state how much of it appears in the urine.', f'{fx(load, 3)} mmol min⁻¹; none appears in urine', f'{gfr} cm³ × {fx(pg, 1)} mmol dm⁻³ ÷ 1000 = {fx(load, 3)} mmol [1]; all reabsorbed / none in urine [1] [2]'),
             P_('Explain why the urea concentration in the urine is much higher than in the plasma.', 'Most of the water in the filtrate is reabsorbed but most urea is not, so urea becomes concentrated.', 'water reabsorbed [1]; urea retained [1] [2]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'short')
def nephron_table(r, D):
    sub = r.choice([('protein', 'present (about 70 g dm⁻³)', 'absent', 'absent', 'too large to pass through the basement membrane'),
                    ('glucose', 'present', 'present at the same concentration', 'absent', 'filtered, then all reabsorbed by co-transport in the PCT'),
                    ('urea', 'present', 'present at the same concentration', 'much higher concentration', 'filtered; water reabsorbed but most urea is not'),
                    ('sodium ions', 'present', 'present at the same concentration', 'present at variable concentration', 'filtered; most reabsorbed by active transport, amount adjusted in the DCT and collecting duct'),
                    ('amino acids', 'present', 'present at the same concentration', 'absent', 'filtered; all reabsorbed in the PCT by co-transport with Na⁺'),
                    ('red blood cells', 'present', 'absent', 'absent', 'cells are far too large to pass through the endothelium and basement membrane')])
    name, pl, fi, ur, why = sub
    st = f'A table compares the composition of blood plasma, glomerular filtrate and urine. For {name}: plasma — {pl}; filtrate — {fi}; urine — {ur}. Explain these observations.'
    if D >= 4:
        st += ' Suggest how the urine of a person with kidney damage to the basement membrane would differ.'
        return Q(st, f'{cap(why)}. With a damaged basement membrane, protein (and possibly blood cells) would appear in the urine.', f'filtration explained [1]; reabsorption/concentration explained [1]; protein in urine with damage [1] [3]', 'short')
    return Q(st, cap(why) + '.', f'{why} [2]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def kidney_case(r, D):
    drug = r.choice(['a drug that inhibits the sodium–potassium pumps of the PCT cells', 'a drug (SGLT2 inhibitor) that blocks the sodium–glucose co-transporter in the PCT', 'a drug that narrows the afferent arteriole'])
    st = f'A clinician in {city(r)} is investigating the effect of {drug} on kidney function.'
    eff = {'pumps': ('Glucose, amino acids, Na⁺ and water reabsorption would all fall, because the Na⁺ gradient that drives co-transport would not be maintained.', 'no Na⁺ gradient [1]; co-transport reduced [1]; glucose and water lost in urine [1] [3]'),
           'SGLT2': ('Glucose would not be reabsorbed so it would appear in the urine; this lowers blood glucose in people with type 2 diabetes; more water would also be lost (osmotic effect).', 'glucose not reabsorbed [1]; glucose in urine [1]; lowers blood glucose / water loss [1] [3]'),
           'afferent': ('Glomerular blood pressure would fall, so the rate of ultrafiltration (GFR) would decrease and less urine would be produced; urea would build up in the blood.', 'lower hydrostatic pressure [1]; lower GFR [1]; consequence [1] [3]')}
    k = 'pumps' if 'pumps' in drug else ('SGLT2' if 'SGLT2' in drug else 'afferent')
    parts = [P_('Predict and explain the effect of the drug.', eff[k][0], eff[k][1]),
             P_('Describe the route taken by a molecule of urea from the blood in the glomerulus to the collecting duct.', 'Through pores in the capillary endothelium, the basement membrane and between podocytes into the Bowman\'s capsule; along the PCT, loop of Henle and DCT into the collecting duct.', 'three filtration layers [1]; correct order of nephron regions [1] [2]'),
             P_('Explain why proteins and red blood cells do not normally pass into the filtrate.', 'The basement membrane acts as a filter that holds back molecules with RMM above about 69 000 and cells; red cells are too large to pass the endothelial pores.', 'basement membrane filter [1]; size limit [1] [2]'),
             P_('Explain why the PCT cells contain many mitochondria.', 'They provide ATP for active transport of Na⁺ out of the cells by the Na⁺/K⁺ pumps, which drives co-transport of glucose and amino acids.', 'ATP for active transport [1]; Na⁺ gradient for co-transport [1] [2]'),
             P_('Explain why the hydrostatic pressure in the glomerular capillaries is high.', 'The efferent arteriole is narrower than the afferent arteriole and the glomerulus receives blood from the renal artery at high pressure.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the structure of a nephron and explain how ultrafiltration and selective reabsorption take place.', 'Bowman\'s capsule with glomerulus; PCT; loop of Henle; DCT; collecting duct. Ultrafiltration: high pressure, afferent wider than efferent, endothelium pores, basement membrane, podocytes, filtrate composition. Selective reabsorption in PCT: microvilli, mitochondria, Na⁺/K⁺ pump on basal side, co-transport of glucose/amino acids, water by osmosis, all glucose reabsorbed.',
           'nephron regions [2]; ultrafiltration mechanism [2]; filtrate composition [1]; PCT adaptations [1]; co-transport mechanism [1]; water by osmosis [1] [8]'),
          ('Explain how urea is formed and removed from the body.', 'Excess amino acids deaminated in liver; amine group → ammonia; ammonia + CO₂ → urea in ornithine cycle; urea into blood; filtered in glomerulus; not reabsorbed (mostly); concentrated as water reabsorbed; stored in bladder and removed in urine.',
           'deamination [2]; ornithine cycle [1]; transport in blood [1]; ultrafiltration [1]; concentration in nephron [1] [6]')])
t3b = t

# ---------------------------------------------------------------------
t = T('Osmoregulation: ADH and aquaporins', 'osmoregulation: adh and aquaporins')
facts(t, [('osmoregulation', 'the control of the water potential of the blood and body fluids'),
          ('ADH', 'antidiuretic hormone: a hormone made in the hypothalamus and released from the posterior pituitary that increases the permeability of the collecting ducts to water'),
          ('aquaporin', 'a channel protein in a membrane that allows water molecules to pass through rapidly'),
          ('osmoreceptor', 'a cell in the hypothalamus that detects changes in the water potential of the blood'),
          ('collecting duct', 'the final part of the nephron, passing through the medulla, where the water content of urine is adjusted under the control of ADH'),
          ('loop of Henle', 'the hairpin section of the nephron that creates a low water potential in the medulla by a countercurrent multiplier')])
mcqs(t, [('Where is ADH released into the blood?', 'Posterior pituitary gland', 'ADH is made in the hypothalamus and released from the posterior pituitary.', ['Anterior pituitary gland', 'Adrenal cortex', 'Kidney cortex']),
         ('What is the effect of ADH on the cells of the collecting duct?', 'Vesicles containing aquaporins fuse with the cell surface membrane', 'More water channels so more water is reabsorbed.', ['Aquaporins are removed from the membrane', 'Sodium ions are pumped into the filtrate', 'The cells become impermeable to water']),
         ('Which change causes an increase in ADH secretion?', 'A fall in the water potential of the blood', 'Detected by osmoreceptors in the hypothalamus.', ['A rise in the water potential of the blood', 'Drinking a large volume of water', 'A fall in blood glucose']),
         ('Which part of the loop of Henle is impermeable to water?', 'The ascending limb', 'Ions are pumped out of the ascending limb but water cannot follow.', ['The descending limb', 'The whole loop', 'Neither limb']),
         ('What happens to urine when ADH secretion is low?', 'A large volume of dilute urine is produced', 'Collecting ducts become less permeable to water.', ['A small volume of concentrated urine is produced', 'Urine contains glucose', 'Urine contains protein'])])
shorts(t, [('State the role of the hypothalamus in osmoregulation.', 'Its osmoreceptors detect changes in blood water potential; its neurosecretory cells make ADH, which passes down axons to the posterior pituitary.', '[2]'),
           ('Name the second messenger that is produced when ADH binds to receptors on collecting duct cells.', 'Cyclic AMP (cAMP).', '[1]')])
explain(t, [('Explain how ADH increases water reabsorption in the collecting duct.', 'ADH binds to receptors on collecting duct cells; this activates adenylyl cyclase forming cAMP, which leads to phosphorylation and fusion of vesicles containing aquaporins with the luminal membrane; water moves by osmosis through aquaporins into the medulla (low water potential) and into the blood.', 'binds receptor [1]; cAMP / phosphorylation [1]; aquaporin vesicles fuse [1]; osmosis into medulla/blood [1] [4]'),
            ('Explain how the loop of Henle produces a region of low water potential in the medulla.', 'Na⁺ and Cl⁻ are actively transported out of the thick ascending limb, which is impermeable to water; this lowers the water potential of the medulla tissue fluid; water leaves the descending limb by osmosis; the countercurrent arrangement builds up the gradient, greatest at the tip of the loop.', 'active transport of ions out of ascending limb [1]; ascending limb impermeable [1]; water leaves descending limb [1]; countercurrent multiplier [1] [4]'),
            ('Explain why desert mammals such as kangaroo rats have very long loops of Henle.', 'A longer loop creates a steeper water potential gradient in the medulla, so more water can be reabsorbed from the collecting ducts by osmosis and very concentrated urine is produced.', 'steeper gradient [1]; more water reabsorbed / concentrated urine [1] [2]'),
            ('Explain what happens to ADH secretion and urine production after a person drinks a large volume of water.', 'Blood water potential rises; osmoreceptors detect the rise; less ADH released; aquaporins removed from collecting duct membranes by endocytosis; less water reabsorbed; large volume of dilute urine.', 'water potential rises [1]; less ADH [1]; fewer aquaporins [1]; more dilute urine [1] [4]')])
myths(t, [('ADH is made by the posterior pituitary gland.', 'ADH is made by neurosecretory cells in the hypothalamus and stored in and released from the posterior pituitary.'),
          ('ADH causes active transport of water out of the collecting duct.', 'Water moves by osmosis through aquaporins; ADH increases the number of aquaporins in the membrane.'),
          ('When you are dehydrated, your kidneys stop producing urine.', 'Urine is still produced to remove urea, but its volume is small and it is concentrated.')])


@t.add('C3', (1, 2, 3, 4, 5), 'case')
def adh_data(r, D):
    times = [0, 30, 60, 90, 120, 150]
    peak = r.choice([30, 60])
    base = round(r.uniform(0.8, 1.2), 1)
    top = round(r.uniform(8, 14), 1)
    vols = [base] + [round(base + (top - base) * math.exp(-((tt - peak - 15) ** 2) / 1800), 1) for tt in times[1:]]
    vol = r.choice([1.0, 1.5])
    p = person(r)
    if D == 1:
        return MQ(r, f'{p} drinks {fx(vol, 1)} dm³ of water. What happens next?', 'Less ADH is secreted and more dilute urine is produced', ['More ADH is secreted and less urine is produced', 'ADH secretion stops permanently', 'Glucose appears in the urine'], 'Blood water potential rises; ADH falls; fewer aquaporins.')
    st = (f'{p} drank {fx(vol, 1)} dm³ of water at time 0 in a study in {city(r)}. The rate of urine production (cm³ min⁻¹) at 30-minute intervals was: ' + ', '.join(f'{tt} min: {fx(v, 1)}' for tt, v in zip(times, vols)) + '.')
    mx = max(vols)
    tm = times[vols.index(mx)]
    parts = [P_('Describe the changes in the rate of urine production.', f'The rate rose from {fx(base, 1)} cm³ min⁻¹ to a peak of {fx(mx, 1)} cm³ min⁻¹ at {tm} min, then fell back towards the original rate.', 'rise to peak with data [1]; fall [1] [2]'),
             P_('Explain the increase in urine production.', 'Water absorbed from gut raised blood water potential; osmoreceptors in hypothalamus detected this; less ADH released from posterior pituitary; collecting ducts less permeable (fewer aquaporins); less water reabsorbed.', 'water potential rises [1]; osmoreceptors [1]; less ADH [1]; fewer aquaporins / less reabsorption [1] [4]'),
             P_('Suggest why it took time for the rate of urine production to increase.', 'Water must be absorbed from the gut into the blood; ADH already in the blood must be broken down; aquaporins must be removed from membranes.', 'absorption time [1]; ADH removal / aquaporins removed [1] [2]'),
             P_(f'Calculate the percentage increase in urine production rate from 0 min to the peak.', f'{fx(pct(base, mx), 0)}%', f'({fx(mx, 1)} − {fx(base, 1)}) ÷ {fx(base, 1)} × 100 = {fx(pct(base, mx), 0)}% [2]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4))


@t.add('C4', (2, 3, 4, 5), 'case')
def di_case(r, D):
    kind = r.choice(['central (cranial) diabetes insipidus, in which the posterior pituitary releases little ADH', 'nephrogenic diabetes insipidus, in which collecting duct cells have faulty ADH receptors', 'a mutation in the gene for aquaporin-2'])
    vol = r.randint(8, 18)
    p = person(r)
    st = f'{p} has {kind}. {p} produces about {vol} dm³ of dilute urine per day, compared with about 1.5 dm³ normally.'
    treat = 'Giving synthetic ADH (desmopressin) would help, because the collecting ducts can still respond to it.' if 'central' in kind else 'Synthetic ADH would not help, because the collecting duct cells cannot respond to ADH (or lack functional aquaporins).'
    parts = [P_('Explain why this condition causes a large volume of dilute urine.', 'Collecting duct cells do not insert aquaporins into their membranes, so they remain impermeable to water; little water is reabsorbed by osmosis into the medulla.', 'aquaporins not inserted [1]; low permeability [1]; less reabsorption [1] [3]'),
             P_('Suggest whether a synthetic form of ADH would be an effective treatment. Explain your answer.', treat, 'correct decision [1]; reason [1] [2]'),
             P_('Explain why the person feels very thirsty.', 'Large water loss lowers blood water potential; osmoreceptors in the hypothalamus detect this and stimulate the thirst centre.', 'low water potential [1]; osmoreceptors / thirst [1] [2]'),
             P_(f'Calculate how many times more urine than normal the person produces.', f'{fx(vol / 1.5, 1)} times', f'{vol} ÷ 1.5 = {fx(vol / 1.5, 1)} [1]'),
             P_('Describe the role of cyclic AMP in the action of ADH.', 'ADH binding activates adenylyl cyclase, forming cAMP; cAMP activates protein kinase, which phosphorylates proteins so that vesicles of aquaporins move to and fuse with the luminal membrane.', 'cAMP formed [1]; protein kinase / phosphorylation [1]; vesicles fuse [1] [3]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how the water potential of the blood is controlled in a mammal.', 'Osmoreceptors in hypothalamus detect fall in water potential; shrink; nerve impulses to posterior pituitary; ADH released into blood; binds receptors on collecting duct cells; cAMP; aquaporin vesicles fuse; more water reabsorbed by osmosis into medulla (low ψ from loop of Henle); small volume concentrated urine; negative feedback: rise in ψ reduces ADH, aquaporins removed by endocytosis.',
           'osmoreceptors [1]; ADH production and release [1]; target cells and cAMP [1]; aquaporins [1]; osmosis into medulla [1]; loop of Henle gradient [1]; opposite response / negative feedback [1] [7]')])
t3c = t

# ---------------------------------------------------------------------
t = T('Control of blood glucose: insulin, glucagon, cAMP second messenger; testing for glucose', 'control of blood glucose')
facts(t, [('insulin', 'a hormone secreted by β cells of the islets of Langerhans that lowers blood glucose concentration'),
          ('glucagon', 'a hormone secreted by α cells of the islets of Langerhans that raises blood glucose concentration'),
          ('glycogenesis', 'the conversion of glucose into glycogen for storage, mainly in liver and muscle cells'),
          ('glycogenolysis', 'the breakdown of glycogen to glucose, stimulated by glucagon and adrenaline'),
          ('gluconeogenesis', 'the synthesis of glucose from non-carbohydrate sources such as amino acids and glycerol'),
          ('second messenger', 'a molecule such as cyclic AMP that is produced inside a cell when a hormone binds to a membrane receptor and relays the signal'),
          ('GLUT4', 'a glucose transporter protein in muscle and fat cells that is moved into the cell surface membrane in response to insulin')])
mcqs(t, [('Which cells secrete glucagon?', 'α cells of the islets of Langerhans', 'α cells → glucagon; β cells → insulin.', ['β cells of the islets of Langerhans', 'Hepatocytes', 'Cells of the adrenal medulla']),
         ('Which enzyme converts ATP to cyclic AMP when glucagon binds to its receptor?', 'Adenylyl cyclase', 'G protein activates adenylyl cyclase.', ['Protein kinase A', 'Glycogen phosphorylase', 'Glycogen synthase']),
         ('Why does glucagon affect liver cells but not muscle cells?', 'Only liver cells have glucagon receptors', 'Target cells need specific receptors.', ['Muscle cells store no glycogen', 'Glucagon cannot leave the blood in muscle', 'Muscle cells have no adenylyl cyclase']),
         ('How does insulin increase the uptake of glucose by muscle cells?', 'It causes vesicles containing GLUT4 transporters to fuse with the cell surface membrane', 'More glucose carriers in the membrane.', ['It opens sodium channels', 'It converts glucose to glycogen in the blood', 'It activates adenylyl cyclase']),
         ('Which feature of a test strip for glucose makes it specific to glucose?', 'It contains the enzyme glucose oxidase', 'Enzyme specificity: glucose oxidase reacts only with glucose.', ['It contains Benedict\'s reagent', 'It changes colour with any reducing sugar', 'It contains insulin'])])
shorts(t, [('State two effects of insulin on liver cells.', 'Increases glucose uptake; activates glycogen synthase (glycogenesis); increases respiration of glucose; inhibits gluconeogenesis; increases conversion to fat.', 'any two [2]'),
           ('Name the two enzymes on a glucose test strip.', 'Glucose oxidase and peroxidase.', '[2]'),
           ('State the normal concentration of glucose in human blood.', 'About 4–6 mmol dm⁻³ (about 90 mg per 100 cm³).', '[1]')])
explain(t, [('Explain how glucagon causes the release of glucose from a liver cell.', 'Glucagon binds to a receptor on the liver cell membrane; this activates a G protein and adenylyl cyclase; ATP is converted to cAMP; cAMP activates protein kinase A, which starts an enzyme cascade activating glycogen phosphorylase; glycogen is broken down to glucose, which diffuses out of the cell.', 'binds receptor [1]; adenylyl cyclase / cAMP [1]; protein kinase / cascade [1]; glycogen phosphorylase / glycogenolysis [1]; glucose leaves [1] [5]'),
            ('Explain why the cAMP cascade allows a small amount of glucagon to have a large effect.', 'Each step activates many molecules of the next enzyme, so the signal is amplified: one glucagon molecule leads to the release of millions of glucose molecules.', 'each enzyme activates many [1]; amplification [1] [2]'),
            ('Explain how a glucose test strip detects glucose in urine.', 'Glucose oxidase converts glucose (and oxygen) to gluconic acid and hydrogen peroxide; peroxidase uses the hydrogen peroxide to oxidise a colourless chromogen to a coloured compound; colour intensity is compared with a chart.', 'glucose oxidase [1]; H₂O₂ produced [1]; peroxidase and chromogen colour [1]; compared with chart [1] [4]'),
            ('Explain why insulin and glucagon are said to be antagonistic.', 'They have opposite effects on blood glucose: insulin lowers it and glucagon raises it; the balance between them keeps blood glucose within narrow limits.', 'opposite effects [1]; balance controls concentration [1] [2]'),
            ('Explain how a biosensor measures the blood glucose concentration of a person with diabetes.', 'Glucose oxidase immobilised on an electrode oxidises glucose; the reaction produces a small electric current proportional to glucose concentration, which is read on a digital display.', 'immobilised glucose oxidase [1]; current proportional to concentration [1] [2]')])
myths(t, [('Insulin converts glucose into glycogen.', 'Insulin is a hormone, not an enzyme; it stimulates enzymes such as glycogen synthase in target cells to make glycogen.'),
          ('Glucagon is the same as glycogen.', 'Glucagon is a peptide hormone that raises blood glucose; glycogen is a polysaccharide store.'),
          ('Glucagon enters the liver cell and breaks down glycogen.', 'Glucagon binds to a receptor on the cell surface membrane; the signal is passed on by cAMP to enzymes inside the cell.')])
mcqs(t, [('Cholera toxin keeps G proteins permanently active. What would happen in a liver cell with active G proteins?', 'cAMP concentration would remain high and glycogen would be continually broken down', 'Adenylyl cyclase stays active.', ['Glycogen synthesis would increase', 'Insulin receptors would be blocked', 'Glucagon could no longer bind to the cell']),
         ('A person\'s urine test strip shows a positive result for glucose. Which is the most likely explanation?', 'Blood glucose exceeds the renal threshold so not all filtered glucose is reabsorbed', 'Carriers in the PCT are saturated.', ['The glomerulus does not filter glucose', 'Insulin is present in the urine', 'Glucose is secreted into the collecting duct'])], D=(2, 3), C='C2')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def cascade(r, D):
    steps = r.choice([2, 3, 4])
    amps = [r.choice([10, 20, 50, 100]) for _ in range(steps)]
    tot = 1
    for a in amps:
        tot *= a
    names = ['each activated adenylyl cyclase makes {a} cAMP molecules', 'each cAMP leads to activation of {a} protein kinase molecules', 'each protein kinase activates {a} phosphorylase kinase molecules', 'each phosphorylase kinase activates {a} glycogen phosphorylase molecules'][:steps]
    st = 'In a liver cell, one activated glucagon receptor activates one adenylyl cyclase molecule, which starts a cascade: ' + '; '.join(n.format(a=a) for n, a in zip(names, amps)) + '.'
    if D <= 2:
        return NQ(r, st + ' How many molecules are activated at the last step for each glucagon receptor activated?', tot, [sum(amps), tot / amps[-1], tot * 10, max(amps) * steps], '',
                  ' × '.join(map(str, amps)) + f' = {tot:,}.', f=lambda v: f'{int(v):,}')
    g = r.choice([100, 500, 1000, 2000])
    st += f' Each active glycogen phosphorylase releases {g} glucose molecules per second.'
    return Q(st + ' Calculate the number of glucose molecules released per second for each glucagon receptor activated, and explain the advantage of this mechanism.', f'{tot * g:,} (= {sci(tot * g, 2)}); a small hormone signal gives a large, rapid response (amplification).',
             f'{" × ".join(map(str, amps))} × {g} [1] = {tot * g:,} [1]; amplification / fast large response [1] [3]', 'numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def calib_curve(r, D):
    concs = [0, 2, 4, 6, 8, 10]
    k = r.uniform(0.09, 0.12)
    absb = [round(0.02 + k * c * (1 - 0.02 * c), 2) for c in concs]
    target = r.uniform(2.5, 9.5)
    a = round(0.02 + k * target * (1 - 0.02 * target), 2)
    # interpolate
    for i in range(len(concs) - 1):
        if absb[i] <= a <= absb[i + 1]:
            c = concs[i] + (a - absb[i]) / (absb[i + 1] - absb[i]) * (concs[i + 1] - concs[i])
            break
    else:
        return None
    p = person(r)
    st = (f'{p} made a calibration curve for glucose using a glucose oxidase–peroxidase reagent, which forms a coloured product, and a colorimeter. '
          f'Absorbance values for glucose standards (mmol dm⁻³): ' + ', '.join(f'{cc}: {fx(aa, 2)}' for cc, aa in zip(concs, absb)) + f'. A fasting blood plasma sample treated in the same way gave an absorbance of {fx(a, 2)}.')
    parts = [P_('Use the data to estimate the glucose concentration of the sample.', f'{fx(c, 1)} mmol dm⁻³', f'between {concs[i]} and {concs[i + 1]} mmol dm⁻³ [1]; interpolation gives {fx(c, 1)} mmol dm⁻³ (± 0.2) [1] [2]'),
             P_('State whether this person\'s blood glucose concentration is within the normal fasting range. Explain your answer.', ('Yes: it lies within about 4–6 mmol dm⁻³.' if 4 <= c <= 6 else ('No: it is above the normal range of about 4–6 mmol dm⁻³ (hyperglycaemia), which may indicate diabetes.' if c > 6 else 'No: it is below the normal range (hypoglycaemia).')), 'correct comparison with 4–6 mmol dm⁻³ [1]'),
             P_('Explain why a series of standard solutions was used.', 'To produce a calibration curve so that the absorbance of an unknown can be converted to a concentration; colorimeters vary so standards must be measured under the same conditions.', 'calibration curve [1]; same conditions / instrument [1] [2]'),
             P_('Suggest why reagents containing glucose oxidase are preferred to Benedict\'s solution for measuring glucose in blood or urine.', 'They are specific for glucose (other reducing sugars do not react), quick, do not require heating and are portable.', 'specific [1]; quick / no heating [1] [2]')]
    return case(r, st, parts, k=(2, 3), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def gtt_case(r, D):
    times = [0, 30, 60, 90, 120]
    a = [round(x, 1) for x in (r.uniform(4.5, 5.2), r.uniform(7.5, 8.5), r.uniform(6.0, 7.0), r.uniform(5.0, 5.6), r.uniform(4.6, 5.2))]
    b = [round(x, 1) for x in (r.uniform(7.5, 8.5), r.uniform(12, 14), r.uniform(14, 16), r.uniform(13, 15), r.uniform(11, 13))]
    p1, p2 = two_people(r)
    st = (f'In a glucose tolerance test, {p1} and {p2} fasted overnight and then drank 75 g of glucose. Blood glucose (mmol dm⁻³) at 0, 30, 60, 90 and 120 min was: '
          f'{p1}: {", ".join(fx(x, 1) for x in a)}; {p2}: {", ".join(fx(x, 1) for x in b)}.')
    parts = [P_(f'Explain the changes in the blood glucose of {p1} between 30 and 120 minutes.', 'Rise detected by β cells; insulin secreted; liver and muscle cells take up glucose (GLUT4), convert to glycogen and respire more; blood glucose returns to normal by 120 min.', 'β cells / insulin [1]; uptake by cells / GLUT4 [1]; glycogenesis [1]; data quoted [1] [4]'),
             P_(f'Suggest, with reasons, which person may have diabetes.', f'{p2}: high fasting glucose ({fx(b[0], 1)} mmol dm⁻³), very high peak and slow return; still {fx(b[-1], 1)} at 120 min.', f'{p2} [1]; two pieces of evidence from data [2] [3]'),
             P_('Distinguish between type 1 and type 2 diabetes.', 'Type 1: β cells destroyed (autoimmune), no insulin made, treated with insulin injections. Type 2: insulin produced but target cells less responsive (insulin resistance), linked to obesity, treated with diet/exercise/drugs.', 'type 1 [1]; type 2 [1]; treatment difference [1] [3]'),
             P_(f'Calculate the percentage increase in blood glucose of {p1} from 0 to 30 minutes.', f'{fx(pct(a[0], a[1]), 0)}%', f'({fx(a[1], 1)} − {fx(a[0], 1)}) ÷ {fx(a[0], 1)} × 100 = {fx(pct(a[0], a[1]), 0)}% [2]'),
             P_('Explain why people with diabetes may use a biosensor rather than urine test strips to monitor their glucose.', 'Biosensors measure the current blood concentration quantitatively; urine strips only show glucose once the renal threshold is exceeded and reflect earlier levels.', 'blood vs urine / current value [1]; quantitative [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how the concentration of glucose in the blood is controlled, including the role of the second messenger cAMP.', 'Set point ~5 mmol dm⁻³; detected by α and β cells of islets; insulin from β cells: GLUT4 vesicles, glycogenesis, respiration, fat; glucagon from α cells binds liver receptors; G protein; adenylyl cyclase; cAMP; protein kinase A cascade; glycogen phosphorylase; glycogenolysis and gluconeogenesis; amplification; negative feedback.',
           'detection by islet cells [1]; insulin effects [2]; glucagon receptor and G protein [1]; cAMP and kinase cascade [2]; glucagon effects [1]; negative feedback [1] [8]'),
          ('Describe how glucose can be measured in urine and in blood, and explain why measurements are important for people with diabetes.', 'Dip sticks: glucose oxidase + peroxidase + chromogen; colour chart; semi-quantitative. Biosensor: glucose oxidase on electrode, current, digital readout; blood sample. Importance: adjust insulin dose/diet, avoid hypoglycaemia and hyperglycaemia, long-term damage.',
           'dip stick chemistry [2]; colour chart [1]; biosensor [2]; importance [1] [6]')])
t3d = t

# ---------------------------------------------------------------------
t = T('Homeostasis in plants: stomatal opening and closing and the role of abscisic acid', 'homeostasis in plants')
facts(t, [('abscisic acid', 'a plant hormone (ABA) produced in response to water stress that causes stomata to close'),
          ('guard cell', 'one of a pair of cells surrounding a stoma whose changes in turgor open and close the pore'),
          ('stomatal aperture', 'the width of the opening (pore) between a pair of guard cells'),
          ('water stress', 'a condition in which a plant loses water faster than it can be absorbed by the roots')])
mcqs(t, [('Which ion moves into guard cells when stomata open?', 'Potassium ions', 'K⁺ influx lowers water potential so water enters.', ['Calcium ions', 'Sodium ions', 'Chloride ions only']),
         ('Which change causes stomata to close?', 'ABA binding to receptors on guard cells', 'ABA triggers Ca²⁺ entry and K⁺ loss.', ['Increase in light intensity', 'Decrease in CO₂ concentration in the leaf', 'Proton pumping out of guard cells']),
         ('Why does a guard cell bend outwards when it becomes turgid?', 'Its inner wall is thicker and less elastic than its outer wall, and cellulose microfibrils are arranged radially', 'Uneven wall thickening makes it curve.', ['Its outer wall is thicker than its inner wall', 'It has no chloroplasts', 'It loses water when it opens'])])
shorts(t, [('State two environmental conditions that cause stomata to open.', 'Light (blue light); low CO₂ concentration inside the leaf; high humidity / water availability.', 'any two [2]'),
           ('State why stomatal closure is a homeostatic response.', 'It reduces water loss by transpiration, keeping the water content of the plant tissues within limits.', '[1]')])
explain(t, [('Explain how stomata open.', 'In light, proton pumps in guard cell membranes use ATP to pump H⁺ out; this creates an electrochemical gradient; K⁺ channels open and K⁺ enters; malate is made from starch; water potential falls; water enters by osmosis; guard cells become turgid and bend apart.', 'proton pumping [1]; K⁺ enter [1]; water potential falls, osmosis [1]; turgid guard cells curve / wall structure [1] [4]'),
            ('Explain how abscisic acid causes stomata to close.', 'ABA binds to receptors on guard cell membranes; Ca²⁺ enters the cytoplasm and acts as a second messenger; this opens channels so K⁺ (and anions) leave and inhibits proton pumps; water potential of guard cells rises; water leaves by osmosis; cells become flaccid and the pore closes.', 'ABA receptor [1]; Ca²⁺ second messenger [1]; K⁺ leave [1]; water leaves, flaccid [1] [4]'),
            ('Explain why stomatal opening and closing involves a compromise for the plant.', 'Open stomata allow CO₂ to diffuse in for photosynthesis but also allow water vapour loss; closing conserves water but limits photosynthesis.', 'CO₂ for photosynthesis [1]; water loss [1] [2]')])
myths(t, [('Stomata close at night because guard cells run out of water.', 'At night proton pumps stop, K⁺ leave and water leaves by osmosis, so guard cells become flaccid; this is an active, controlled response.'),
          ('ABA is produced only in the leaves.', 'ABA is produced in roots (and leaves) when water is scarce and is carried in the xylem to the leaves.')])

ABA = {'setup': lambda r, p: f'{p} floated epidermal strips from a broad bean leaf on solutions of different ABA concentrations in bright light for 1 hour, then measured the stomatal aperture of 10 stomata using an eyepiece graticule.',
       'iv': ('ABA concentration', 'μmol dm⁻³'), 'xs': lambda r: r.choice([[0, 0.1, 1, 10, 100], [0, 1, 5, 10, 50], [0, 0.5, 2, 8, 32]]),
       'dv': ('mean stomatal aperture', 'μm'), 'y': lambda x, k: k * (2 + 10 / (1 + (x / 3) ** 0.8)) if x > 0 else k * 12, 'dp': 1, 'reps': 3, 'noise': 0.06,
       'controls': ['light intensity', 'temperature', 'age and position of the leaf', 'time on the solution', 'concentration of K⁺ in the solution'],
       'why': ('ABA binds to receptors on guard cells, causing Ca²⁺ to enter and K⁺ to leave, so water leaves by osmosis and the guard cells become flaccid; higher concentrations bind more receptors so more stomata close.', 'ABA receptor [1]; K⁺ loss / Ca²⁺ [1]; water out, flaccid guard cells [1] [3]'),
       'improve': ['measure more stomata chosen at random', 'use strips from the same leaf', 'calibrate the eyepiece graticule with a stage micrometer'],
       'control': 'Strips floated on the same buffer without ABA (0 μmol dm⁻³), to show the aperture without ABA under the same conditions.', 'graph': True}
add_practical(t, ABA, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C4', (2, 3, 4, 5), 'case')
def stoma_case(r, D):
    crop = r.choice(['maize', 'wheat', 'sorghum', 'tomato', 'cotton'])
    st = f'During a drought in a farming region near {city(r)}, the ABA concentration in the xylem sap of {crop} plants rose about {r.randint(10, 50)}-fold before any wilting was seen.'
    parts = [P_('Explain how this rise in ABA would help the plants survive the drought.', 'ABA travels to leaves and binds to guard cell receptors; stomata close; transpiration falls so water is conserved.', 'ABA to leaves [1]; stomata close [1]; less transpiration [1] [3]'),
             P_('Suggest a disadvantage to the plants of the response.', 'CO₂ uptake falls so photosynthesis and growth (yield) decrease; leaves may overheat with less evaporative cooling.', 'less CO₂ / photosynthesis [1]; reduced yield / overheating [1] [2]'),
             P_('Describe the role of calcium ions in the response of guard cells to ABA.', 'Ca²⁺ act as a second messenger; they enter the cytoplasm (from outside and from vacuole) and open anion and K⁺ channels and inhibit H⁺ pumps.', 'second messenger [1]; effect on channels [1] [2]'),
             P_('Suggest why ABA concentration rose before wilting occurred.', 'Roots in drying soil detect water stress and produce ABA, sending a signal to leaves before leaf cells lose turgor.', '[2]')]
    return case(r, st, parts, k=(2, 3))


longs(t, [('Describe the mechanism of stomatal opening and closing, including the role of abscisic acid.', 'Guard cell structure: thick inner wall, radial microfibrils; opening: light, H⁺ pumps, K⁺ in, malate, ψ falls, water in, turgid; closing: dark or ABA; ABA from roots/leaves in water stress, binds receptors, Ca²⁺ second messenger, K⁺ and anions out, H⁺ pumps inhibited, water out, flaccid; balance between CO₂ uptake and water loss.',
           'guard cell structure [1]; opening mechanism [2]; ABA production [1]; ABA mechanism [2]; compromise [1] [7]')])
t3e = t

CHAPTERS[3] = [t3a, t3b, t3c, t3d, t3e]


# ===================================================================== 4 Control and coordination
t = T('Hormonal communication: endocrine glands and the control of the menstrual cycle; contraceptive pill', 'hormonal communication')
facts(t, [('endocrine gland', 'a ductless gland that secretes hormones directly into the blood'),
          ('FSH', 'follicle-stimulating hormone: secreted by the anterior pituitary; stimulates follicle development and oestrogen secretion'),
          ('LH', 'luteinising hormone: secreted by the anterior pituitary; a surge causes ovulation and development of the corpus luteum'),
          ('oestrogen', 'a steroid hormone secreted by developing follicles that stimulates repair of the endometrium and, at high levels, the LH surge'),
          ('progesterone', 'a steroid hormone secreted by the corpus luteum that maintains the endometrium and inhibits FSH and LH secretion'),
          ('corpus luteum', 'the structure that forms from the follicle after ovulation and secretes progesterone'),
          ('ovulation', 'the release of a secondary oocyte from a mature follicle in the ovary, around day 14 of the cycle')])
mcqs(t, [('Which hormone causes ovulation?', 'LH', 'A surge of LH around day 14 triggers ovulation.', ['FSH', 'Progesterone', 'Oxytocin']),
         ('Which structure secretes progesterone in the second half of the menstrual cycle?', 'Corpus luteum', 'The corpus luteum develops from the ruptured follicle.', ['Anterior pituitary', 'Developing follicle', 'Hypothalamus']),
         ('How does the combined contraceptive pill prevent pregnancy?', 'Oestrogen and progesterone inhibit FSH and LH secretion so no follicles develop and no ovulation occurs', 'Negative feedback on the pituitary.', ['It kills sperm in the vagina', 'It stimulates the LH surge', 'It destroys the corpus luteum']),
         ('What causes menstruation at the end of a cycle in which fertilisation has not occurred?', 'A fall in progesterone as the corpus luteum degenerates', 'Without progesterone the endometrium breaks down.', ['A rise in LH', 'A rise in oestrogen', 'A rise in FSH'])])
shorts(t, [('Name the two hormones secreted by the anterior pituitary gland that control the ovarian cycle.', 'FSH and LH.', '[2]'),
           ('State two effects of progesterone in the menstrual cycle.', 'Maintains / thickens the endometrium; inhibits FSH and LH secretion by negative feedback.', '[2]')])
explain(t, [('Explain how a high concentration of oestrogen causes ovulation.', 'Rising oestrogen from the developing follicle has a positive feedback effect on the anterior pituitary (and hypothalamus), causing a surge in LH (and FSH), which causes the follicle to rupture and release the oocyte.', 'positive feedback [1]; LH surge [1]; follicle ruptures [1] [3]'),
            ('Explain why progesterone levels remain high if fertilisation occurs.', 'The embryo secretes hCG, which maintains the corpus luteum, so it continues to secrete progesterone, keeping the endometrium for implantation.', 'hCG from embryo [1]; corpus luteum maintained [1] [2]'),
            ('Explain the roles of negative feedback in the control of the menstrual cycle.', 'Progesterone (and oestrogen) from the corpus luteum inhibit FSH and LH secretion, so no new follicles develop; when the corpus luteum degenerates, progesterone falls, FSH rises again and a new cycle starts.', 'progesterone inhibits FSH/LH [1]; no new follicles [1]; fall allows new cycle [1] [3]'),
            ('Explain why the contraceptive pill is taken daily for 21 days followed by 7 days without.', 'Daily doses keep oestrogen/progesterone high to suppress FSH and LH; stopping for 7 days causes the hormones to fall so the endometrium breaks down (withdrawal bleed).', 'constant levels needed [1]; break causes fall and bleed [1] [2]')])
myths(t, [('FSH is secreted by the ovaries.', 'FSH is secreted by the anterior pituitary gland; the ovaries secrete oestrogen and progesterone.'),
          ('Ovulation is caused by a surge in progesterone.', 'Ovulation is caused by a surge in LH; progesterone rises after ovulation from the corpus luteum.'),
          ('The contraceptive pill works by killing sperm.', 'The pill contains hormones that suppress FSH and LH so that no follicles mature and no ovulation occurs.')])

CYCLE = [(3, 'FSH', 'low-moderate and rising', 'menstruation; new follicles begin to develop'),
         (10, 'oestrogen', 'rising to a peak', 'endometrium repaired and thickening'),
         (14, 'LH', 'at its peak', 'ovulation'),
         (21, 'progesterone', 'at its peak', 'corpus luteum active; endometrium maintained'),
         (27, 'progesterone', 'falling', 'corpus luteum degenerating; endometrium about to break down')]


@t.add('C3', (1, 2, 3, 4), 'short')
def cycle_day(r, D):
    day, h, lev, ev = r.choice(CYCLE)
    if D <= 2:
        wrong = [c[3] for c in CYCLE if c[0] != day]
        return MQ(r, f'In a typical 28-day menstrual cycle, which event occurs at about day {day}?', cap(ev), [cap(w) for w in wrong], f'Day {day}: {ev}; {h} {lev}.')
    st = f'{person(r)} is studying hormone data for a woman with a regular 28-day cycle. On day {day}, the concentration of {h} is {lev}. Explain the significance of this hormone level at this stage of the cycle.'
    expl = {'FSH': 'FSH from the anterior pituitary stimulates follicles to develop and secrete oestrogen, starting a new cycle after progesterone has fallen.',
            'oestrogen': 'Oestrogen from the growing follicle repairs the endometrium; at high levels it triggers the LH surge by positive feedback.',
            'LH': 'The LH surge causes the mature follicle to rupture and release the secondary oocyte (ovulation) and the follicle to become the corpus luteum.',
            'progesterone': 'Progesterone from the corpus luteum maintains the endometrium for implantation and inhibits FSH/LH; ' + ('it is falling because the corpus luteum degenerates if no embryo is present, so menstruation follows.' if lev == 'falling' else 'its high level prevents new follicles developing.')}[h]
    return Q(st, expl, f'source gland/structure [1]; effect at this stage [1]; feedback link [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def pill_case(r, D):
    pg = r.choice(['a combined pill containing synthetic oestrogen and progesterone', 'a progesterone-only pill', 'an emergency contraceptive containing a high dose of progesterone'])
    st = f'A health clinic in {city(r)} is explaining how {pg} works to a group of students.'
    parts = [P_('Explain how this pill prevents pregnancy.', 'The synthetic hormones inhibit FSH and LH secretion by the anterior pituitary (negative feedback), so follicles do not mature and there is no LH surge or ovulation; progesterone also thickens cervical mucus.', 'inhibits FSH/LH [1]; no follicle development/ovulation [1]; cervical mucus [1] [3]'),
             P_('Explain why the pill must be taken at about the same time each day.', 'Synthetic hormones are broken down; regular doses keep their concentrations high enough to suppress FSH and LH.', '[2]'),
             P_('Suggest one social or ethical issue linked to the use of oral contraceptives.', 'Allows control of family size / women\'s careers; side effects and health risks (e.g. thrombosis); religious objections; no protection against STIs.', 'any one with explanation [2]'),
             P_('Describe the role of the hypothalamus in the menstrual cycle.', 'It secretes GnRH, which stimulates the anterior pituitary to release FSH and LH; it responds to oestrogen and progesterone feedback.', '[2]')]
    return case(r, st, parts, k=(2, 3))


longs(t, [('Describe the hormonal control of the human menstrual cycle and explain how the contraceptive pill prevents pregnancy.', 'GnRH; FSH stimulates follicle growth and oestrogen; oestrogen repairs endometrium, inhibits FSH, then high oestrogen positive feedback → LH surge → ovulation day 14; corpus luteum secretes progesterone, maintains endometrium, inhibits FSH/LH; degenerates → progesterone falls → menstruation; pill: synthetic oestrogen/progesterone, negative feedback, no FSH/LH, no ovulation.',
           'FSH and follicles [1]; oestrogen effects [1]; LH surge and ovulation [1]; corpus luteum and progesterone [1]; menstruation [1]; pill mechanism [2] [7]')])
t4a = t

# ---------------------------------------------------------------------
t = T('Nervous communication: neurones, resting and action potentials and saltatory conduction', 'nervous communication')
facts(t, [('resting potential', 'the potential difference of about −70 mV across the membrane of a neurone that is not transmitting an impulse, inside negative'),
          ('action potential', 'a rapid, temporary reversal of the potential difference across a neurone membrane, from −70 mV to about +30 mV'),
          ('depolarisation', 'the change in membrane potential towards positive as voltage-gated sodium channels open and Na⁺ diffuse in'),
          ('repolarisation', 'the return of the membrane potential towards negative as K⁺ channels open and K⁺ diffuse out'),
          ('refractory period', 'the time after an action potential during which another action potential cannot be generated (or needs a larger stimulus)'),
          ('threshold', 'the potential difference (about −50 mV) that must be reached for voltage-gated Na⁺ channels to open and an action potential to be produced'),
          ('saltatory conduction', 'the jumping of action potentials from one node of Ranvier to the next along a myelinated axon'),
          ('node of Ranvier', 'a short gap in the myelin sheath where the axon membrane is exposed and action potentials occur')])
mcqs(t, [('Which ions diffuse into the axon during depolarisation?', 'Sodium ions', 'Voltage-gated Na⁺ channels open.', ['Potassium ions', 'Chloride ions', 'Calcium ions']),
         ('What is the approximate resting potential of a neurone?', '−70 mV', 'Inside negative relative to outside.', ['+30 mV', '0 mV', '−30 mV']),
         ('How many sodium and potassium ions are moved by one cycle of the sodium–potassium pump?', '3 Na⁺ out and 2 K⁺ in', 'Uses one ATP per cycle.', ['2 Na⁺ out and 3 K⁺ in', '3 Na⁺ in and 2 K⁺ out', '1 Na⁺ out and 1 K⁺ in']),
         ('Why do impulses travel faster along myelinated neurones?', 'Action potentials occur only at nodes of Ranvier and jump between them', 'Saltatory conduction.', ['Myelin conducts electricity', 'Myelinated axons have more sodium channels along their length', 'Myelin increases the resting potential']),
         ('Which is a function of the refractory period?', 'It ensures impulses travel in one direction only', 'Also separates impulses and limits frequency.', ['It increases the size of action potentials', 'It allows impulses to merge', 'It speeds up conduction']),
         ('Which type of neurone carries impulses from receptors to the central nervous system?', 'Sensory neurone', 'Sensory → relay → motor.', ['Motor neurone', 'Relay neurone', 'Intermediate neurone'])])
shorts(t, [('State two factors that increase the speed of conduction of an action potential.', 'Myelination (saltatory conduction); larger axon diameter; higher temperature (up to a point).', 'any two [2]'),
           ('Name the structure that converts a stimulus into a generator potential in the skin.', 'A receptor (sensory receptor such as a Pacinian corpuscle).', '[1]')])
explain(t, [('Explain how a resting potential is maintained.', 'The Na⁺/K⁺ pump actively transports 3 Na⁺ out and 2 K⁺ in; the membrane is more permeable to K⁺ (more K⁺ channels open), so K⁺ diffuse out; organic anions inside; inside is left negative at about −70 mV.', 'pump 3 Na⁺ out 2 K⁺ in [1]; K⁺ leak out [1]; membrane less permeable to Na⁺ [1]; inside negative [1] [4]'),
            ('Describe the events that occur during an action potential.', 'Stimulus causes some Na⁺ channels to open; threshold reached; many voltage-gated Na⁺ channels open, Na⁺ diffuse in, depolarisation to +30 mV; Na⁺ channels close, K⁺ channels open, K⁺ diffuse out, repolarisation; hyperpolarisation; pump restores resting potential.', 'threshold [1]; Na⁺ in / depolarisation [1]; K⁺ out / repolarisation [1]; hyperpolarisation and restoration [1] [4]'),
            ('Explain why action potentials are described as all-or-nothing.', 'If threshold is reached an action potential of the same size (+30 mV) is always produced; below threshold none is produced; stimulus strength is coded by frequency of impulses, not size.', 'same size if threshold reached [1]; none below [1]; frequency codes intensity [1] [3]'),
            ('Explain how local circuits cause an action potential to move along an unmyelinated axon.', 'Na⁺ that enter at the depolarised region diffuse sideways along the axon; this depolarises the next region to threshold, opening its Na⁺ channels; the region behind is refractory so the impulse moves forwards.', 'Na⁺ diffuse sideways [1]; next region reaches threshold [1]; refractory behind [1] [3]'),
            ('Explain how saltatory conduction increases the speed of transmission.', 'Myelin insulates the axon so depolarisation occurs only at nodes of Ranvier; local circuits extend from node to node, so the impulse jumps and fewer depolarisations are needed.', 'myelin insulates [1]; action potentials only at nodes [1]; jumps / fewer depolarisations [1] [3]')])
myths(t, [('A stronger stimulus produces a bigger action potential.', 'Action potentials are all-or-nothing and the same size; a stronger stimulus produces a higher frequency of action potentials.'),
          ('During an action potential, sodium ions are pumped into the axon.', 'Na⁺ diffuse in through voltage-gated channels; the pump moves Na⁺ out.'),
          ('Myelin conducts the impulse along the axon.', 'Myelin is an insulator; it forces depolarisation to occur only at the nodes of Ranvier.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def conduction(r, D):
    kind = r.choice([('a myelinated motor neurone', 40, 110), ('an unmyelinated C fibre', 0.5, 2.5), ('a squid giant axon', 18, 28), ('a myelinated sensory neurone', 30, 80)])
    name, lo, hi = kind
    v = round(r.uniform(lo, hi), 1 if hi < 5 else 0)
    dist = r.choice([0.02, 0.05, 0.1, 0.15, 0.3, 0.5, 0.8, 1.0]) if hi > 5 else r.choice([0.005, 0.01, 0.02, 0.03])
    tms = dist / v * 1000
    if not (0.1 <= tms <= 100):
        return None
    tms = round(tms, 2)
    v = dist / (tms / 1000)
    if D == 1:
        return NQ(r, f'An action potential travels {fx(dist * 100, 1)} cm along {name} in {fx(tms, 2)} ms. What is the conduction speed?', v, [v / 1000, v * 10, v / 10, dist / tms], ' m s⁻¹',
                  f'speed = distance ÷ time = {fx(dist, 3)} m ÷ {fx(tms / 1000, 5)} s = {sf(v, 3)} m s⁻¹.')
    p = person(r)
    st = f'{p} stimulated {name} and recorded action potentials at two electrodes {fx(dist * 100, 1)} cm apart. The action potential arrived at the second electrode {fx(tms, 2)} ms after the first.'
    parts = [P_('Calculate the conduction speed in m s⁻¹.', f'{sf(v, 3)} m s⁻¹', f'{fx(dist * 100, 1)} cm = {fx(dist, 3)} m and {fx(tms, 2)} ms = {fx(tms / 1000, 5)} s [1]; speed = {sf(v, 3)} m s⁻¹ [1] [2]'),
             P_('Explain why this speed is ' + ('high' if hi > 20 else 'low') + ' compared with other neurones.', ('The axon is myelinated (saltatory conduction between nodes of Ranvier) and/or has a large diameter.' if 'myelinated' in name and 'un' not in name else ('The giant axon has a very large diameter, which reduces resistance and increases local circuit spread; it is not myelinated.' if 'giant' in name else 'The axon is unmyelinated and narrow, so depolarisation must occur along the whole membrane by local circuits.')), 'myelination / diameter linked to speed [2]'),
             P_('Explain why the action potential is not reduced in size as it travels along the axon.', 'Each region of membrane generates a new full-sized action potential when it reaches threshold (all-or-nothing); energy comes from ion gradients along the axon.', 'regenerated at each region [1]; all-or-nothing [1] [2]')]
    if D >= 3:
        rp = r.choice([1, 2, 2.5, 4, 5])
        parts.append(P_(f'The refractory period of this neurone is {fx(rp, 1)} ms. Calculate the maximum frequency of action potentials.', f'{fx(1000 / rp, 0)} Hz', f'1 ÷ {fx(rp / 1000, 4)} s = {fx(1000 / rp, 0)} impulses per second [2]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'short')
def ap_trace(r, D):
    pts = [('A', 'the membrane potential rises from −70 mV to −50 mV', 'some Na⁺ channels open in response to the stimulus, Na⁺ diffuse in; threshold is reached'),
           ('B', 'the potential rises rapidly from −50 mV to +30 mV', 'voltage-gated Na⁺ channels open; Na⁺ diffuse in rapidly down their electrochemical gradient (depolarisation)'),
           ('C', 'the potential falls from +30 mV to −70 mV', 'Na⁺ channels close; voltage-gated K⁺ channels open; K⁺ diffuse out (repolarisation)'),
           ('D', 'the potential falls below −70 mV to about −80 mV', 'K⁺ channels are slow to close so too many K⁺ leave (hyperpolarisation)'),
           ('E', 'the potential returns to −70 mV', 'K⁺ channels close; the Na⁺/K⁺ pump and leak channels restore the resting potential')]
    lab, what, why = r.choice(pts)
    st = r.choice([f'A trace of an action potential recorded by {person(r)} shows a stage in which {what}. Explain the changes in ion movement responsible.',
                   f'On an oscilloscope trace of an action potential, at stage {lab} {what}. Explain what is happening to ion channels at this stage.'])
    return Q(st, cap(why) + '.', f'{why} [2]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def nerve_case(r, D):
    cond = r.choice([('multiple sclerosis', 'the myelin sheath of neurones in the CNS is damaged by the immune system', 'Saltatory conduction is lost in damaged regions; impulses travel more slowly or are blocked because local circuits cannot reach the next node.'),
                     ('Guillain–Barré syndrome', 'antibodies damage the myelin of peripheral neurones', 'Conduction is slowed or blocked in peripheral neurones because depolarisation cannot jump between nodes; muscles weaken.'),
                     ('poisoning by tetrodotoxin from a pufferfish', 'the toxin blocks voltage-gated sodium channels', 'No depolarisation can occur, so no action potentials are produced; muscles, including those for breathing, are paralysed.'),
                     ('the effect of a local anaesthetic such as lidocaine', 'the drug blocks voltage-gated sodium channels in sensory neurones', 'Action potentials cannot be generated or conducted in sensory neurones, so impulses from pain receptors do not reach the brain.')])
    name, what, eff = cond
    st = f'In {name}, {what}.'
    parts = [P_('Explain the effect on the transmission of nerve impulses.', eff, f'{eff} [3]'),
             P_('Describe the structure of a myelinated motor neurone.', 'Cell body in CNS with nucleus and many RER (Nissl); dendrites; long axon; myelin sheath formed by Schwann cells; nodes of Ranvier; motor end plates at the muscle.', 'cell body and dendrites [1]; axon with Schwann cells / myelin [1]; nodes [1]; end plates [1] [4]'),
             P_('Explain how the resting potential is restored after an action potential.', 'K⁺ diffuse out through K⁺ channels (repolarisation); Na⁺/K⁺ pump uses ATP to move 3 Na⁺ out and 2 K⁺ in to restore the ion concentrations.', 'K⁺ out [1]; pump restores gradients [1] [2]'),
             P_('Explain why neurones contain many mitochondria.', 'ATP is needed for the Na⁺/K⁺ pump to maintain the resting potential and for vesicle movement/neurotransmitter synthesis at synapses.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how a resting potential is maintained and how an action potential is produced and transmitted along a myelinated neurone.', 'Na⁺/K⁺ pump 3:2; K⁺ leak; −70 mV; stimulus → threshold; voltage-gated Na⁺ channels open, Na⁺ in, +30 mV; K⁺ channels open, K⁺ out; hyperpolarisation; refractory period; local circuits; myelin by Schwann cells insulates; saltatory conduction node to node; faster; all-or-nothing; one direction.',
           'resting potential [2]; depolarisation [1]; repolarisation / hyperpolarisation [1]; refractory period [1]; local circuits [1]; saltatory conduction [1] [7]')])
t4b = t

# ---------------------------------------------------------------------
t = T('Synapses: cholinergic synapse structure and transmission', 'synapses: cholinergic synapse')
facts(t, [('synapse', 'a junction between two neurones (or a neurone and an effector) across which impulses are passed by neurotransmitters'),
          ('acetylcholine', 'the neurotransmitter released at cholinergic synapses and neuromuscular junctions'),
          ('acetylcholinesterase', 'the enzyme in the synaptic cleft that hydrolyses acetylcholine into choline and ethanoic acid (acetate)'),
          ('synaptic cleft', 'the gap of about 20 nm between the presynaptic and postsynaptic membranes'),
          ('neuromuscular junction', 'a synapse between a motor neurone and a muscle fibre'),
          ('summation', 'the combined effect of several excitatory postsynaptic potentials, from one or more presynaptic neurones, that together reach threshold')])
mcqs(t, [('Which ions enter the presynaptic knob when an action potential arrives?', 'Calcium ions', 'Voltage-gated Ca²⁺ channels open; Ca²⁺ triggers exocytosis.', ['Sodium ions', 'Potassium ions', 'Chloride ions']),
         ('How is acetylcholine removed from the synaptic cleft?', 'It is hydrolysed by acetylcholinesterase', 'Choline is reabsorbed into the presynaptic knob.', ['It diffuses into the blood', 'It is pumped into the postsynaptic neurone', 'It is broken down by ATP']),
         ('Why can impulses pass across a synapse in one direction only?', 'Only the presynaptic knob contains vesicles of neurotransmitter, and only the postsynaptic membrane has receptors', 'Structural asymmetry.', ['The synaptic cleft is too wide', 'Action potentials can only travel towards the cell body', 'Acetylcholine is made in the postsynaptic neurone']),
         ('What is the effect of acetylcholine binding to receptors on the postsynaptic membrane?', 'Sodium ion channels open and the membrane depolarises', 'Receptors are ligand-gated Na⁺ channels.', ['Potassium ions enter and the membrane hyperpolarises', 'Calcium ions leave the postsynaptic neurone', 'The vesicles fuse with the postsynaptic membrane'])])
shorts(t, [('State two roles of synapses in the nervous system.', 'Ensure one-way transmission; allow integration/summation of impulses; filter out low-level stimuli; allow divergence and convergence; adaptation / habituation; memory and learning.', 'any two [2]'),
           ('State the products of hydrolysis of acetylcholine.', 'Choline and ethanoic acid (acetate).', '[1]')])
explain(t, [('Describe how an impulse is transmitted across a cholinergic synapse.', 'Action potential arrives at presynaptic knob; voltage-gated Ca²⁺ channels open, Ca²⁺ diffuse in; vesicles move and fuse with presynaptic membrane, releasing ACh by exocytosis; ACh diffuses across cleft and binds to receptors; Na⁺ channels open, depolarisation; if threshold reached, action potential; ACh hydrolysed by acetylcholinesterase; choline reabsorbed.', 'Ca²⁺ in [1]; exocytosis of ACh [1]; diffusion and binding to receptors [1]; Na⁺ in, depolarisation [1]; ACh hydrolysed and recycled [1] [5]'),
            ('Explain why acetylcholine must be broken down quickly after it has bound to its receptors.', 'Otherwise Na⁺ channels would stay open and the postsynaptic membrane would remain depolarised, causing continuous impulses (e.g. sustained muscle contraction) and preventing new signals.', 'channels stay open / continuous depolarisation [1]; consequence [1] [2]'),
            ('Explain why the presynaptic knob contains many mitochondria.', 'ATP is needed to resynthesise acetylcholine from choline and acetyl CoA, to move vesicles and to pump Ca²⁺ back out.', 'ATP for synthesis of ACh [1]; for vesicle transport / Ca²⁺ pumping [1] [2]'),
            ('Explain how summation at synapses allows integration of information.', 'A single presynaptic impulse may release too little transmitter to reach threshold; several impulses in quick succession (temporal) or from several neurones (spatial) add together; inhibitory synapses can cancel excitatory ones.', 'temporal [1]; spatial [1]; inhibition / integration [1] [3]')])
myths(t, [('The action potential jumps across the synaptic cleft.', 'Transmission across the cleft is chemical: neurotransmitter diffuses across and binds to receptors.'),
          ('Acetylcholine enters the postsynaptic neurone to cause depolarisation.', 'Acetylcholine binds to receptors on the postsynaptic membrane; the opening of Na⁺ channels causes depolarisation.'),
          ('Acetylcholinesterase is released from vesicles in the presynaptic knob.', 'Acetylcholinesterase is located in the synaptic cleft, attached to the postsynaptic membrane.')])

DRUGS = [('an organophosphate insecticide', 'inhibits acetylcholinesterase', 'ACh is not broken down, so postsynaptic Na⁺ channels stay open; continuous depolarisation causes sustained contraction / spasms and paralysis'),
         ('curare', 'binds to acetylcholine receptors without opening the channels', 'ACh cannot bind, so no depolarisation of the muscle fibre; flaccid paralysis'),
         ('nicotine', 'binds to and opens acetylcholine receptors (an agonist)', 'mimics ACh, causing depolarisation of postsynaptic neurones even without ACh'),
         ('botulinum toxin', 'prevents the release of acetylcholine from vesicles', 'no ACh released so no depolarisation of the muscle; muscles are paralysed'),
         ('α-bungarotoxin from snake venom', 'binds irreversibly to acetylcholine receptors at the neuromuscular junction', 'ACh cannot bind so muscle fibres are not depolarised; paralysis, including breathing muscles'),
         ('a drug that blocks voltage-gated calcium channels in the presynaptic membrane', 'stops Ca²⁺ entering the presynaptic knob', 'vesicles do not fuse with the membrane so no ACh is released; no transmission')]


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def drug_apply(r, D):
    d, how, eff = r.choice(DRUGS)
    if D == 1:
        wrong = [x[2] for x in DRUGS if x[0] != d]
        return MQ(r, f'{cap(d)} {how}. What is the effect at a cholinergic synapse?', cap(eff), [cap(w) for w in wrong[:5]], f'{cap(eff)}.')
    st = r.choice([f'{cap(d)} {how}. Explain the effect of {d} on transmission at a neuromuscular junction.', f'{person(r)} reads that {d} {how}. Predict and explain the effect on synaptic transmission.'])
    return Q(st, cap(eff) + '.', f'effect on ACh / receptors [1]; effect on postsynaptic membrane [1]; consequence for muscle / neurone [1] [3]', 'short')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def syn_delay(r, D):
    dist = r.choice([4, 6, 8, 10, 12])  # cm
    v = r.choice([20, 25, 40, 50])
    syn = r.choice([1, 2, 3, 4])
    delay = round(r.uniform(0.3, 0.6), 1)
    tot = dist / 100 / v * 1000 + syn * delay
    st = (f'A reflex pathway in an experimental animal contains {syn} synapse{"s" if syn > 1 else ""} and a total neurone length of {dist} cm. Impulses travel along the neurones at {v} m s⁻¹, and the delay at each synapse is {fx(delay, 1)} ms.')
    parts = [P_('Calculate the total time from stimulus to response, ignoring the time taken at the receptor and effector.', f'{fx(tot, 2)} ms', f'conduction: {dist / 100} m ÷ {v} = {fx(dist / 100 / v * 1000, 2)} ms [1]; synapses {syn} × {fx(delay, 1)} = {fx(syn * delay, 1)} ms [1]; total {fx(tot, 2)} ms [1] [3]'),
             P_('Calculate the percentage of the total time taken by synaptic transmission.', f'{fx(syn * delay / tot * 100, 0)}%', f'{fx(syn * delay, 1)} ÷ {fx(tot, 2)} × 100 = {fx(syn * delay / tot * 100, 0)}% [1]'),
             P_('Explain why transmission across a synapse is slower than conduction along an axon.', 'Transmission involves several steps: Ca²⁺ entry, exocytosis, diffusion of ACh across the cleft and binding to receptors before depolarisation.', 'chemical steps listed [1]; diffusion is slow [1] [2]'),
             P_('Suggest why reflex arcs have few synapses.', 'Fewer synapses means less synaptic delay so the response is faster, protecting the body from harm.', '[1]')]
    return case(r, st, parts, k=(2, 3), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def syn_case(r, D):
    cond = r.choice(['myasthenia gravis, in which antibodies block and destroy acetylcholine receptors at neuromuscular junctions', 'Alzheimer\'s disease, in which cholinergic neurones in the brain are lost and acetylcholine levels fall'])
    treat = 'an acetylcholinesterase inhibitor'
    st = f'{cap(cond)}. Doctors in {city(r)} treat it with {treat}.'
    parts = [P_('Explain the symptoms of the condition in terms of synaptic transmission.', ('Fewer functional receptors mean less depolarisation of the muscle fibre membrane; threshold is often not reached so muscles are weak and tire quickly.' if 'myasthenia' in cond else 'Less acetylcholine is released, so postsynaptic neurones are depolarised less often; transmission in memory pathways fails.'), 'link to receptors / ACh amount [1]; less depolarisation [1]; consequence [1] [3]'),
             P_('Explain how the treatment helps.', 'Inhibiting acetylcholinesterase means acetylcholine stays in the cleft longer and at a higher concentration, so it binds to the remaining receptors more often and depolarisation is more likely to reach threshold.', 'ACh not hydrolysed [1]; stays longer / more binding [1]; threshold reached [1] [3]'),
             P_('Suggest a possible side effect of the treatment.', 'Excess stimulation at other cholinergic synapses (e.g. muscle twitching, slow heart rate, excess salivation).', '[1]'),
             P_('Describe the structure of a cholinergic synapse.', 'Presynaptic knob with mitochondria, vesicles of ACh, voltage-gated Ca²⁺ channels; synaptic cleft ~20 nm; postsynaptic membrane with ACh receptors (ligand-gated Na⁺ channels) and acetylcholinesterase.', 'presynaptic features [1]; cleft [1]; postsynaptic receptors / enzyme [1] [3]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the structure of a cholinergic synapse and explain how an impulse is transmitted across it.', 'Presynaptic knob, mitochondria, vesicles, Ca²⁺ channels; cleft; postsynaptic receptors, AChE. Action potential → Ca²⁺ in → vesicles fuse → exocytosis of ACh → diffuses → binds receptors → Na⁺ channels open → EPSP → threshold → action potential; ACh hydrolysed; choline reabsorbed, ACh resynthesised with ATP; one-way.',
           'structure [2]; Ca²⁺ and exocytosis [1]; diffusion and binding [1]; depolarisation / threshold [1]; breakdown and recycling [1]; one-way transmission [1] [7]')])
t4c = t

# ---------------------------------------------------------------------
t = T('Muscle contraction: sarcomere structure and the sliding filament model', 'muscle contraction')
facts(t, [('sarcomere', 'the repeating unit of a myofibril, between two Z lines, which shortens during contraction'),
          ('A band', 'the dark band of a sarcomere, equal to the length of the myosin (thick) filaments; it does not change length during contraction'),
          ('I band', 'the light band of a sarcomere containing only actin (thin) filaments; it shortens during contraction'),
          ('H zone', 'the central region of the A band containing only myosin; it shortens during contraction'),
          ('sarcoplasmic reticulum', 'the specialised endoplasmic reticulum of a muscle fibre that stores calcium ions and releases them when the fibre is depolarised'),
          ('T-tubule', 'an infolding of the sarcolemma that carries depolarisation deep into the muscle fibre'),
          ('tropomyosin', 'a protein that lies along actin filaments and covers the myosin-binding sites when the muscle is relaxed')])
mcqs(t, [('Which part of a sarcomere stays the same length during contraction?', 'A band', 'The A band is the length of myosin filaments.', ['I band', 'H zone', 'Distance between Z lines']),
         ('To which protein do calcium ions bind to start muscle contraction?', 'Troponin', 'Ca²⁺ binds troponin, which moves tropomyosin off the binding sites.', ['Tropomyosin', 'Myosin', 'Actin']),
         ('What is the role of ATP in muscle contraction?', 'Its hydrolysis allows the myosin head to detach from actin and re-cock', 'ATP binding detaches the head; hydrolysis recocks it.', ['It binds to troponin', 'It forms the actin filaments', 'It releases calcium from mitochondria']),
         ('Where are calcium ions stored in a relaxed muscle fibre?', 'Sarcoplasmic reticulum', 'Released when depolarisation spreads via T-tubules.', ['Mitochondria', 'Nucleus', 'Myosin filaments'])])
shorts(t, [('State two changes in the appearance of a sarcomere when it contracts.', 'I band shortens; H zone shortens/disappears; Z lines move closer together; A band stays the same.', 'any two [2]'),
           ('Name the two proteins that make up the thick and thin filaments of a myofibril.', 'Myosin (thick) and actin (thin).', '[1]')])
explain(t, [('Describe the sliding filament model of muscle contraction.', 'Ca²⁺ binds to troponin, moving tropomyosin to expose binding sites on actin; myosin heads bind forming cross-bridges; heads tilt (power stroke) pulling actin towards the centre of the sarcomere, releasing ADP and Pi; ATP binds, heads detach; ATP hydrolysed, heads re-cock and bind further along; filaments slide, sarcomere shortens.', 'Ca²⁺ / troponin / tropomyosin [1]; cross-bridges [1]; power stroke [1]; ATP detaches / recocks [1]; filaments slide, not shorten [1] [5]'),
            ('Explain how an action potential at the neuromuscular junction leads to the release of calcium ions inside the muscle fibre.', 'ACh depolarises the sarcolemma; the action potential spreads along the sarcolemma and down T-tubules; this causes Ca²⁺ channels in the sarcoplasmic reticulum to open; Ca²⁺ diffuse into the sarcoplasm.', 'sarcolemma depolarised [1]; T-tubules [1]; SR releases Ca²⁺ [1] [3]'),
            ('Explain why rigor mortis occurs after death.', 'Without respiration no ATP is made; myosin heads cannot detach from actin, so cross-bridges stay attached and the muscles remain rigid.', 'no ATP [1]; heads cannot detach [1] [2]'),
            ('Explain why muscle fibres contain many mitochondria.', 'Large amounts of ATP are needed for detaching and re-cocking myosin heads and for pumping Ca²⁺ back into the sarcoplasmic reticulum.', 'ATP for cross-bridge cycling [1]; for Ca²⁺ pumping [1] [2]')])
myths(t, [('During contraction the actin and myosin filaments shorten.', 'The filaments do not change length; they slide past each other so the sarcomere shortens.'),
          ('The A band shortens when a muscle contracts.', 'The A band stays the same length because it equals the length of the myosin filaments; the I band and H zone shorten.'),
          ('ATP is needed for the myosin head to attach to actin.', 'Attachment needs exposed binding sites (Ca²⁺); ATP is needed for the head to detach and to re-cock.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def sarcomere(r, D):
    my = r.choice([1.5, 1.6])
    ac = r.choice([1.0, 0.95])
    S1 = round(r.uniform(2.3, 3.2), 1)
    S2 = round(r.uniform(1.9, S1 - 0.2), 1)
    if S2 < my or S2 >= S1:
        return None
    def bands(S):
        return max(0, round(S - my, 2)), max(0, round(S - 2 * ac, 2))
    I1, H1 = bands(S1)
    I2, H2 = bands(S2)
    p = person(r)
    st = f'In a myofibril studied by {p}, each myosin filament is {fx(my, 2)} μm long and each actin filament extends {fx(ac, 2)} μm from the Z line. A relaxed sarcomere is {fx(S1, 2)} μm long; when contracted it is {fx(S2, 2)} μm long.'
    if D == 1:
        return NQ(r, st + ' What is the width of the A band in the contracted sarcomere?', my, [S2 - my, S2, my / 2, S1 - S2], ' μm', f'A band = length of myosin = {fx(my, 2)} μm in any state.', f=lambda v: fx(v, 2))
    parts = [P_('Calculate the total width of the I band (both halves) in the relaxed sarcomere.', f'{fx(I1, 2)} μm', f'I band = sarcomere − A band = {fx(S1, 2)} − {fx(my, 2)} [1] = {fx(I1, 2)} μm [1] [2]'),
             P_('Calculate the width of the H zone in the relaxed and contracted sarcomere.', f'relaxed {fx(H1, 2)} μm; contracted {fx(H2, 2)} μm', f'H = sarcomere − 2 × actin length [1]; {fx(H1, 2)} and {fx(H2, 2)} μm [1] [2]'),
             P_('State the width of the A band in the contracted sarcomere and explain your answer.', f'{fx(my, 2)} μm; the myosin filaments do not shorten, so the A band stays the same.', 'value [1]; myosin unchanged [1] [2]'),
             P_('Calculate the percentage decrease in sarcomere length.', f'{fx((S1 - S2) / S1 * 100, 1)}%', f'({fx(S1, 2)} − {fx(S2, 2)}) ÷ {fx(S1, 2)} × 100 = {fx((S1 - S2) / S1 * 100, 1)}% [1]')]
    if D >= 4:
        parts.append(P_('Explain why a sarcomere generates less force if it is stretched so that there is no overlap of actin and myosin.', 'No overlap means myosin heads cannot form cross-bridges with actin, so no power strokes and no force.', 'no cross-bridges [1]; no power stroke [1] [2]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def muscle_case(r, D):
    st = r.choice([f'A researcher in {city(r)} treated isolated muscle fibres with a drug that prevents the reuptake of calcium ions into the sarcoplasmic reticulum.',
                   f'Isolated myofibrils in {city(r)} were placed in solutions with and without ATP and calcium ions, and their lengths were observed under a microscope.',
                   f'{person(r)} examined electron micrographs of a muscle fibre fixed while relaxed and while contracted.'])
    parts = [P_('Predict and explain the effect of preventing reuptake of calcium ions into the sarcoplasmic reticulum.', 'The muscle would stay contracted: Ca²⁺ stays bound to troponin, binding sites remain exposed and cross-bridges keep forming as long as ATP is available.', 'stays contracted [1]; Ca²⁺ stays bound to troponin [1]; binding sites exposed [1] [3]'),
             P_('Explain why myofibrils contract only when both ATP and calcium ions are present.', 'Ca²⁺ is needed to move tropomyosin and expose myosin-binding sites on actin; ATP is needed for the myosin heads to detach and re-cock so that cycling continues.', 'role of Ca²⁺ [1]; role of ATP [1] [2]'),
             P_('Describe how the appearance of a sarcomere differs between relaxed and contracted states in electron micrographs.', 'Contracted: Z lines closer, I band narrower, H zone narrower or absent, A band unchanged.', 'I band [1]; H zone [1]; A band unchanged [1] [3]'),
             P_('Explain the role of troponin and tropomyosin.', 'In relaxed muscle tropomyosin covers the myosin-binding sites on actin; when Ca²⁺ binds troponin it changes shape and pulls tropomyosin away, exposing the sites.', 'tropomyosin blocks sites [1]; Ca²⁺ / troponin moves it [1] [2]'),
             P_('Explain the role of creatine phosphate in muscle.', 'It donates a phosphate group to ADP to regenerate ATP rapidly during intense activity.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the structure of a sarcomere and explain how a muscle fibre contracts.', 'Z lines, actin thin filaments, myosin thick filaments; A band, I band, H zone, M line; neuromuscular junction ACh → depolarisation of sarcolemma → T-tubules → SR releases Ca²⁺ → troponin → tropomyosin moves → cross-bridges → power stroke (ADP + Pi released) → ATP binds, detach → ATP hydrolysed, recock → sliding; relaxation: Ca²⁺ pumped back.',
           'sarcomere structure [2]; excitation to Ca²⁺ release [2]; troponin/tropomyosin [1]; cross-bridge cycle [2]; relaxation [1] [8]')])
t4d = t

# ---------------------------------------------------------------------
t = T('Control and coordination in plants: rapid responses in the Venus fly trap; auxins and gibberellins', 'control and coordination in plants')
facts(t, [('auxin', 'a plant hormone (IAA) that stimulates cell elongation by loosening cell walls'),
          ('gibberellin', 'a plant hormone that causes stem elongation and stimulates the breakdown of starch stores during seed germination'),
          ('acid growth hypothesis', 'the idea that auxin causes proton pumping into cell walls, lowering pH and activating expansins that loosen the walls so cells elongate'),
          ('expansin', 'a protein activated at low pH that loosens the links between cellulose microfibrils in a plant cell wall'),
          ('Venus fly trap', 'a carnivorous plant whose modified leaves close rapidly when sensitive hairs are touched twice, triggering action potentials')])
mcqs(t, [('How does auxin cause cell elongation?', 'It stimulates proton pumping into the cell wall, lowering the pH so expansins loosen the wall', 'Acid growth hypothesis.', ['It increases cell division only', 'It makes the cell wall thicker', 'It breaks down cellulose completely']),
         ('In a germinating barley seed, gibberellin stimulates the synthesis of which enzyme?', 'Amylase', 'Amylase in the aleurone layer digests starch in the endosperm.', ['Lipase', 'Rubisco', 'Catalase']),
         ('What is needed to trigger closure of a Venus fly trap leaf?', 'Two stimuli of sensory hairs within about 20 seconds', 'Two action potentials in quick succession.', ['A single touch of any part of the leaf', 'Light falling on the leaf', 'An increase in temperature'])])
shorts(t, [('State two differences between control and coordination in plants and in mammals.', 'Plants have no nervous system; responses mainly hormonal and slower; plant hormones often diffuse cell to cell rather than via blood; plant hormones affect growth; some electrical signalling only (e.g. Venus fly trap).', 'any two [2]'),
           ('State the role of the aleurone layer in a germinating cereal seed.', 'It secretes amylase in response to gibberellin; amylase hydrolyses starch in the endosperm to maltose for the embryo.', '[2]')])
explain(t, [('Explain how the leaves of a Venus fly trap close rapidly.', 'Touching sensory hairs opens ion channels, generating receptor potentials and an action potential; two action potentials within about 20 s trigger rapid movement of ions and water in the hinge cells (and acid growth of outer cells), so the leaf changes shape from convex to concave and snaps shut.', 'hairs touched, action potential [1]; two needed [1]; ion and water movement / turgor change [1]; shape change snaps shut [1] [4]'),
            ('Explain how gibberellin brings about the mobilisation of starch in a germinating barley seed.', 'Water uptake causes the embryo to release gibberellin; gibberellin diffuses to the aleurone layer; it causes breakdown of DELLA proteins so the transcription factor (PIF) can activate the amylase gene; amylase is secreted into the endosperm and hydrolyses starch to maltose, which is used by the embryo.', 'GA from embryo [1]; aleurone [1]; DELLA broken down / gene transcribed [1]; amylase hydrolyses starch [1] [4]'),
            ('Explain why dwarf varieties of some plants are short and how gibberellin affects them.', 'Dwarf varieties have a mutation in a gene for an enzyme in gibberellin synthesis, so they make little active gibberellin and have short internodes; applying gibberellin causes them to grow tall.', 'little GA / mutation [1]; GA causes stem elongation [1] [2]')])
myths(t, [('Auxin causes plant cells to divide faster.', 'At A Level, auxin is studied as causing cell elongation by loosening cell walls (acid growth); cell division is not the main effect in elongating shoots.'),
          ('The Venus fly trap closes because its leaves contain muscles.', 'Plants have no muscles; closure results from rapid changes in turgor and cell wall properties in the leaf after action potentials.')])

IAA = {'setup': lambda r, p: f'{p} floated 10 mm sections cut from wheat coleoptiles in solutions of different auxin (IAA) concentrations for 24 hours in the dark, then measured their final lengths.',
       'iv': ('IAA concentration', 'mg dm⁻³'), 'xs': lambda r: r.choice([[0, 0.001, 0.01, 0.1, 1, 10], [0, 0.01, 0.1, 1, 10, 100]]),
       'dv': ('mean increase in length', 'mm'), 'y': lambda x, k: k * (0.8 + 4.5 * math.exp(-((math.log10(x) + 0.5) ** 2) / 1.6)) if x > 0 else k * 0.8, 'dp': 1,
       'controls': ['temperature', 'initial length of sections', 'age of coleoptiles', 'volume of solution', 'darkness (light breaks down auxin)', 'sucrose concentration in solution'],
       'why': ('Auxin stimulates proton pumping into the cell walls; the low pH activates expansins that loosen cellulose cross-links, so cells take up water and elongate; at very high concentrations auxin inhibits growth.', 'proton pumping / acid growth [1]; expansins loosen walls [1]; inhibition at high concentration [1] [3]'),
       'improve': ['use more sections per concentration', 'measure with a ruler under a magnifying lens or use image analysis', 'remove the tips so the coleoptile does not produce its own auxin'],
       'control': 'Sections in buffer solution with no IAA, showing the growth without added auxin.'}
add_practical(t, IAA, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))

longs(t, [('Describe the role of plant hormones in controlling growth, with reference to auxin and gibberellin.', 'Auxin made in shoot tip, diffuses down; binds receptor; proton pumps; low pH in wall; expansins; cell elongation; water uptake. Gibberellin: stem elongation (internodes), dwarf mutants; germination: embryo releases GA, aleurone, DELLA degraded, PIF transcription factor, amylase gene, starch to maltose.',
           'auxin source [1]; acid growth [2]; gibberellin stem elongation [1]; germination sequence [2]; DELLA / gene expression [1] [7]')])
t4e = t

CHAPTERS[4] = [t4a, t4b, t4c, t4d, t4e]


# ===================================================================== 5 Inheritance
from fractions import Fraction  # noqa: E402
from collections import Counter  # noqa: E402


def gametes(g):
    """g: tuple of loci, each a tuple of 2 alleles (or 1 for a male X-linked locus 'Y')."""
    out = []
    for combo in itertools.product(*g):
        out.append(combo)
    return out


def cross(g1, g2, pheno):
    cnt = Counter()
    for a in gametes(g1):
        for b in gametes(g2):
            child = tuple(tuple(sorted((x, y))) for x, y in zip(a, b))
            cnt[pheno(child)] += 1
    return cnt


def ratio_txt(cnt, order=None):
    keys = order or sorted(cnt, key=lambda k: -cnt[k])
    keys = [k for k in keys if cnt.get(k)]
    if len(keys) == 1:
        return f'all {keys[0]}'
    g = 0
    for k in keys:
        g = math.gcd(g, cnt[k])
    return ' : '.join(f'{cnt[k] // g} {k}' for k in keys)


MONO = [  # organism, trait, alleles (dominant first), genotype->phenotype, kind
    ('pea plants', 'seed shape', 'R', 'r', {'RR': 'round', 'Rr': 'round', 'rr': 'wrinkled'}, 'dominance'),
    ('Drosophila', 'wing shape', 'V', 'v', {'VV': 'normal wings', 'Vv': 'normal wings', 'vv': 'vestigial wings'}, 'dominance'),
    ('tomato plants', 'stem colour', 'A', 'a', {'AA': 'purple stem', 'Aa': 'purple stem', 'aa': 'green stem'}, 'dominance'),
    ('cattle', 'coat colour', 'Cᴿ', 'Cᵂ', {'CᴿCᴿ': 'red', 'CᴿCᵂ': 'roan', 'CᵂCᵂ': 'white'}, 'codominance'),
    ('humans', 'haemoglobin type', 'Hbᴬ', 'Hbˢ', {'HbᴬHbᴬ': 'unaffected', 'HbᴬHbˢ': 'sickle cell trait', 'HbˢHbˢ': 'sickle cell anaemia'}, 'codominance'),
    ('snapdragon plants', 'flower colour', 'Cᴿ', 'Cᵂ', {'CᴿCᴿ': 'red', 'CᴿCᵂ': 'pink', 'CᵂCᵂ': 'white'}, 'codominance'),
    ('humans', 'cystic fibrosis', 'F', 'f', {'FF': 'unaffected', 'Ff': 'unaffected (carrier)', 'ff': 'cystic fibrosis'}, 'dominance'),
    ('maize plants', 'grain colour', 'P', 'p', {'PP': 'purple grain', 'Pp': 'purple grain', 'pp': 'yellow grain'}, 'dominance')]


def _pm(spec):
    _, _, A, a, tab, _ = spec

    def f(child):
        x, y = child[0]
        k = (x + y) if x == A or (x != a) else (y + x)
        if k not in tab:
            k = y + x
        return tab[k].replace(' (carrier)', '')
    return f


def _gt(A, a, n):
    return (A, A) if n == 2 else ((A, a) if n == 1 else (a, a))


def mono_q(r, D):
    spec = r.choice(MONO)
    org, trait, A, a, tab, kind = spec
    n1, n2 = r.choice([(1, 1), (1, 0), (2, 0), (1, 2), (2, 1)])
    g1, g2 = _gt(A, a, n1), _gt(A, a, n2)
    order = [tab[A + A], tab[A + a].replace(' (carrier)', ''), tab[a + a]]
    order = list(dict.fromkeys(order))
    cnt = cross((g1,), (g2,), _pm(spec))
    rt = ratio_txt(cnt, order)
    p1 = tab[g1[0] + g1[1]]
    p2 = tab[g2[0] + g2[1]]
    art = lambda w: ('an ' if w[0] in 'aeiou' else 'a ') + w  # noqa: E731
    st = f'In {org}, {trait} is controlled by a gene with two alleles, {A} and {a}' + (' (codominant)' if kind == 'codominance' else f' ({A} dominant)') + f'. {cap(art(p1))} individual with genotype {g1[0]}{g1[1]} is crossed with {art(p2)} individual with genotype {g2[0]}{g2[1]}.'
    if D == 1:
        nums = ' : '.join(w.split(' ')[0] for w in rt.split(' : ')) if ' : ' in rt else 'all one phenotype'
        wrong = ['3 : 1', '1 : 1', '1 : 2 : 1', 'all one phenotype', '9 : 3 : 3 : 1']
        return MQ(r, st + ' What is the expected ratio of phenotypes in the offspring?', nums, [w for w in wrong if w != nums], f'Gametes {g1[0]}, {g1[1]} × {g2[0]}, {g2[1]}; offspring {rt}.')
    gam1 = ', '.join(dict.fromkeys(g1))
    gam2 = ', '.join(dict.fromkeys(g2))
    key = f'parental genotypes {g1[0]}{g1[1]} × {g2[0]}{g2[1]} [1]; gametes {gam1} and {gam2} [1]; offspring genotypes from Punnett square [1]; phenotypes with ratio {rt} [1] [4]'
    if D >= 4:
        tgt = r.choice([o for o in order if cnt.get(o)])
        frac = Fraction(cnt[tgt], sum(cnt.values()))
        nkids = r.choice([4, 8, 40, 120, 200])
        st += f' Use a genetic diagram to show the expected phenotypes of the offspring, and calculate how many of {nkids} offspring would be expected to be {tgt}.'
        return Q(st, f'{rt}; expected {tgt}: {frac} × {nkids} = {fx(float(frac) * nkids, 1)}', key.replace(' [4]', '') + f'; {frac} × {nkids} = {fx(float(frac) * nkids, 1)} [1] [5]', 'numerical')
    ask = 'Draw a genetic diagram to show the expected genotypes and phenotypes of the offspring, and state the phenotypic ratio.'
    q = Q(st + ' ' + ask, rt, key, 'numerical')
    q['_scen'], q['_ask'] = st, ask
    return q


ABO_G = {'IᴬIᴬ': 'A', 'IᴬIᵒ': 'A', 'IᴮIᴮ': 'B', 'IᴮIᵒ': 'B', 'IᴬIᴮ': 'AB', 'IᵒIᵒ': 'O'}


def _abo(child):
    x, y = child[0]
    return 'group ' + (ABO_G.get(x + y) or ABO_G[y + x])


def abo_q(r, D):
    gs = list(ABO_G)
    g1, g2 = r.sample(gs, 2)
    s1 = (g1[:2], g1[2:])
    s2 = (g2[:2], g2[2:])
    cnt = cross((s1,), (s2,), _abo)
    rt = ratio_txt(cnt, ['group A', 'group B', 'group AB', 'group O'])
    p1, p2 = two_people(r)
    st = f'Human ABO blood groups are controlled by three alleles: Iᴬ and Iᴮ (codominant) and Iᵒ (recessive). {p1} has genotype {g1} (blood group {ABO_G[g1]}) and {p2} has genotype {g2} (blood group {ABO_G[g2]}).'
    if D <= 2:
        wrong_all = ['group A', 'group B', 'group AB', 'group O']
        poss = [k for k in cnt]
        imp = [w for w in wrong_all if w not in poss]
        if not imp:
            return None
        bad = r.choice(imp)
        right = [w for w in wrong_all if w in poss]
        return MQ(r, st + ' Which blood group is NOT possible among their children?', cap(bad), [cap(x) for x in right] + [cap(x) for x in imp if x != bad], f'Gametes {s1[0]}/{s1[1]} × {s2[0]}/{s2[1]}; possible children: {rt}.')
    ask = 'Use a genetic diagram to show the possible blood groups of their children and the probability of each.'
    q = Q(st + ' ' + ask, rt, f'gametes {", ".join(dict.fromkeys(s1))} and {", ".join(dict.fromkeys(s2))} [1]; offspring genotypes [1]; blood groups and probabilities ({rt}) [1] [3]', 'numerical')
    q['_scen'], q['_ask'] = st, ask
    return q


XL = [('haemophilia', 'H', 'h', 'blood clots normally', 'haemophilia'), ('red-green colour blindness', 'B', 'b', 'normal colour vision', 'red-green colour blind'),
      ('Duchenne muscular dystrophy', 'D', 'd', 'unaffected', 'muscular dystrophy')]
SUPX = {'H': 'ᴴ', 'h': 'ʰ', 'B': 'ᴮ', 'b': 'ᵇ', 'D': 'ᴰ', 'd': 'ᵈ'}


def xl_q(r, D):
    dis, A, a, norm, aff = r.choice(XL)
    XA, Xa = 'X' + SUPX[A], 'X' + SUPX[a]
    mom = r.choice([(XA, Xa), (XA, XA), (Xa, Xa)])
    dad = r.choice([XA, Xa])
    if dis.startswith('Duchenne') and (dad == Xa or mom == (Xa, Xa)):
        return None
    if mom == (XA, XA) and dad == XA:
        return None
    kids = Counter()
    for m in mom:
        for d in (dad, 'Y'):
            if d == 'Y':
                kids['son ' + (aff if m == Xa else norm)] += 1
            else:
                g = (m, d)
                if Xa in g and XA not in g:
                    kids['daughter ' + aff] += 1
                elif Xa in g:
                    kids['daughter carrier (' + norm + ')'] += 1
                else:
                    kids['daughter ' + norm] += 1
    st = f'{dis.capitalize()} is caused by a recessive allele {a} of a gene on the X chromosome (dominant allele {A}). A woman with genotype {mom[0]}{mom[1]} ({"carrier" if mom == (XA, Xa) else (aff if mom == (Xa, Xa) else norm)}) has children with a man with genotype {dad}Y ({aff if dad == Xa else norm}), in a family referred to a genetic clinic in {city(r)}.'
    son_aff = Fraction(sum(v for k, v in kids.items() if k == 'son ' + aff), sum(v for k, v in kids.items() if k.startswith('son')))
    key = f'gametes {", ".join(dict.fromkeys(mom))} and {dad}, Y [1]; offspring genotypes [1]; phenotypes by sex [1]; probability a son is affected = {son_aff} [1] [4]'
    ans = '; '.join(f'{k}: {Fraction(v, 4)}' for k, v in sorted(kids.items())) + f' of all children. Probability that a son is affected = {son_aff}.'
    if D <= 2:
        wrong = [str(x) for x in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(3, 4)) if x != son_aff]
        return MQ(r, st + ' What is the probability that a son of this couple has ' + aff.replace('red-green colour blind', 'red-green colour blindness') + '?', str(son_aff), wrong, ans)
    ask = 'Draw a genetic diagram to show the possible genotypes and phenotypes of their children. Explain why ' + dis + ' is more common in males than in females.'
    q = Q(st + ' ' + ask, ans + ' Males have only one X chromosome, so a single recessive allele is expressed; females need two copies.', key.replace(' [4]', '') + '; males have one X / no second allele on Y [1] [5]', 'numerical')
    q['_scen'], q['_ask'] = st, ask
    return q


DI = [('pea plants', ('R', 'r', 'round', 'wrinkled'), ('Y', 'y', 'yellow', 'green'), 'seeds'),
      ('Drosophila', ('E', 'e', 'grey body', 'ebony body'), ('V', 'v', 'normal wings', 'vestigial wings'), 'flies'),
      ('tomato plants', ('D', 'd', 'tall', 'dwarf'), ('A', 'a', 'purple stem', 'green stem'), 'plants'),
      ('guinea pigs', ('B', 'b', 'black coat', 'white coat'), ('R', 'r', 'rough coat', 'smooth coat'), 'animals')]


def _dip(g1, g2):
    def f(child):
        a = g1[2] if g1[0] in child[0] else g1[3]
        b = g2[2] if g2[0] in child[1] else g2[3]
        return f'{a}, {b}'
    return f


def di_q(r, D):
    org, ga, gb, noun = r.choice(DI)
    het = ((ga[0], ga[1]), (gb[0], gb[1]))
    rec = ((ga[1], ga[1]), (gb[1], gb[1]))
    kind = r.choice(['F1 self', 'test', 'mixed'])
    if kind == 'F1 self':
        P1, P2 = het, het
    elif kind == 'test':
        P1, P2 = het, rec
    else:
        P1, P2 = het, ((ga[0], ga[1]), (gb[1], gb[1]))
    f = _dip(ga, gb)
    cnt = cross(P1, P2, f)
    order = [f'{ga[2]}, {gb[2]}', f'{ga[2]}, {gb[3]}', f'{ga[3]}, {gb[2]}', f'{ga[3]}, {gb[3]}']
    rt = ratio_txt(cnt, order)
    gt = lambda P: ''.join(P[0]) + ''.join(P[1])  # noqa: E731
    gam = lambda P: ', '.join(dict.fromkeys(x + y for x, y in itertools.product(P[0], P[1])))  # noqa: E731
    st = f'In {org}, {ga[2]} ({ga[0]}) is dominant to {ga[3]} ({ga[1]}) and {gb[2]} ({gb[0]}) is dominant to {gb[3]} ({gb[1]}). The genes are on different chromosomes. {org.capitalize()} with genotype {gt(P1)} are crossed with {org} with genotype {gt(P2)}.'
    if D <= 2:
        nums = ' : '.join(w.split(' ')[0] for w in rt.split(' : '))
        wrong = [w for w in ['9 : 3 : 3 : 1', '1 : 1 : 1 : 1', '3 : 1', '3 : 3 : 1 : 1', '1 : 2 : 1'] if w != nums]
        return MQ(r, st + ' What is the expected phenotypic ratio of the offspring?', nums, wrong, f'Gametes {gam(P1)} × {gam(P2)}; {rt}.')
    key = f'gametes {gam(P1)} and {gam(P2)} [1]; Punnett square of offspring genotypes [1]; phenotypes identified [1]; ratio {rt} [1] [4]'
    ask = 'Use a genetic diagram to determine the expected phenotypes of the offspring and their ratio.'
    q = Q(st + ' ' + ask, rt, key, 'numerical')
    q['_scen'], q['_ask'] = st, ask
    return q


t = T('Meiosis: stages and how it produces genetic variation', 'meiosis: stages')
facts(t, [('meiosis', 'a reduction division in which a diploid nucleus divides twice to produce four genetically different haploid nuclei'),
          ('homologous chromosomes', 'a pair of chromosomes with the same genes at the same loci, one from each parent, that pair up in meiosis I'),
          ('bivalent', 'a pair of homologous chromosomes associated together during prophase I of meiosis'),
          ('chiasma', 'the point at which non-sister chromatids of homologous chromosomes cross over and exchange sections during prophase I'),
          ('crossing over', 'the exchange of sections between non-sister chromatids of a homologous pair, producing new combinations of alleles'),
          ('independent assortment', 'the random orientation of homologous pairs on the equator in metaphase I, so that each gamete receives a random mixture of maternal and paternal chromosomes'),
          ('haploid', 'a cell or nucleus with one set of chromosomes (n)'),
          ('allele', 'a variant form of a gene, found at the same locus on homologous chromosomes')])
mcqs(t, [('At which stage of meiosis do homologous chromosomes separate?', 'Anaphase I', 'Homologues separate in anaphase I; chromatids in anaphase II.', ['Anaphase II', 'Metaphase I', 'Prophase II']),
         ('During which stage does crossing over occur?', 'Prophase I', 'Chiasmata form between non-sister chromatids in prophase I.', ['Metaphase I', 'Anaphase II', 'Telophase I']),
         ('A cell with 2n = 8 undergoes meiosis. How many chromosomes are in each daughter cell?', '4', 'Haploid n = 4.', ['8', '2', '16']),
         ('Which process produces new combinations of alleles on the same chromosome?', 'Crossing over', 'Independent assortment shuffles whole chromosomes; crossing over shuffles alleles along chromatids.', ['Independent assortment', 'Random fertilisation', 'Mitosis']),
         ('At which stage of meiosis do sister chromatids separate?', 'Anaphase II', 'Centromeres divide in anaphase II.', ['Anaphase I', 'Prophase I', 'Metaphase I'])])
shorts(t, [('State three ways in which sexual reproduction produces genetic variation.', 'Crossing over in prophase I; independent assortment of homologues in metaphase I (and of chromatids in metaphase II); random fertilisation of gametes; (random mutation).', '[3]'),
           ('State two differences between meiosis and mitosis.', 'Meiosis: two divisions vs one; four vs two daughter cells; haploid vs diploid; genetically different vs identical; homologues pair and cross over only in meiosis.', 'any two [2]')])
explain(t, [('Explain why meiosis is necessary in sexually reproducing organisms.', 'Gametes must be haploid so that when they fuse at fertilisation the diploid chromosome number is restored and stays constant from generation to generation; meiosis also produces variation.', 'haploid gametes [1]; diploid restored at fertilisation [1]; variation [1] [3]'),
            ('Explain how independent assortment produces genetic variation.', 'In metaphase I each homologous pair lines up randomly on the equator, so the maternal or paternal chromosome may go to either pole; the number of combinations is 2ⁿ (n = haploid number).', 'random orientation of pairs [1]; each gamete gets mixture [1]; 2ⁿ combinations [1] [3]'),
            ('Explain how crossing over increases genetic variation.', 'Non-sister chromatids of homologues break and rejoin at chiasmata, exchanging sections; this produces chromatids with new combinations of alleles of linked genes.', 'chiasmata / exchange between non-sister chromatids [1]; new allele combinations [1] [2]'),
            ('Describe the behaviour of chromosomes during meiosis I.', 'Prophase I: chromosomes condense, homologues pair into bivalents, crossing over; metaphase I: bivalents on equator, random orientation; anaphase I: homologues pulled to opposite poles; telophase I: two haploid nuclei.', 'prophase I [1]; metaphase I [1]; anaphase I [1]; telophase I [1] [4]')])
myths(t, [('Crossing over happens between sister chromatids.', 'Crossing over happens between non-sister chromatids of homologous chromosomes; sister chromatids are identical so exchange would not produce new combinations.'),
          ('Chromatids separate in anaphase I.', 'In anaphase I homologous chromosomes separate; chromatids separate in anaphase II.'),
          ('Meiosis produces two diploid cells.', 'Meiosis produces four haploid cells (in animals usually gametes).')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def assort(r, D):
    org, n2 = r.choice([('a fruit fly', 8), ('a pea plant', 14), ('a human', 46), ('a cat', 38), ('a domestic dog', 78), ('a mosquito', 6), ('a tomato plant', 24), ('a rice plant', 24), ('a maize plant', 20), ('a chicken', 78)])
    n = n2 // 2
    combos = 2 ** n
    if D == 1:
        return NQ(r, f'The diploid number of {org} is {n2}. Ignoring crossing over, how many genetically different gametes can be produced by independent assortment?', combos, [n2 ** 2, 2 ** n2, n * 2, combos * 2], '',
                  f'2ⁿ = 2^{n} = {combos:,}.', f=lambda v: f'{int(v):,}')
    p = person(r)
    st = f'{p} is studying meiosis in {org}, which has a diploid number of {n2}.'
    parts = [P_('State the number of chromosomes in a gamete.', str(n), f'n = {n} [1]'),
             P_('Calculate the number of possible combinations of chromosomes in the gametes due to independent assortment alone.', f'{combos:,}', f'2ⁿ [1] = 2^{n} = {combos:,} [1] [2]'),
             P_('Calculate the number of possible chromosome combinations in a zygote formed by random fertilisation of two such gametes.', f'{combos * combos:,} ({sci(combos * combos, 3)})', f'(2ⁿ)² = {combos:,}² [1] = {sci(combos * combos, 3)} [1] [2]'),
             P_('Explain why the actual number of genetically different gametes is much greater than this.', 'Crossing over during prophase I produces new combinations of alleles within chromosomes.', 'crossing over [1]; new combinations of alleles on chromatids [1] [2]')]
    if D >= 3:
        dna = r.choice([6.0, 7.0, 8.0])
        parts.append(P_(f'A diploid cell of this organism in G1 contains {fx(dna, 1)} arbitrary units of DNA. State the DNA content of a cell at the end of meiosis I and of each gamete.', f'end of meiosis I: {fx(dna, 1)} units per cell; gamete: {fx(dna / 2, 1)} units', f'doubled to {fx(2 * dna, 1)} after S phase, halved at meiosis I = {fx(dna, 1)} [1]; gamete {fx(dna / 2, 1)} [1] [2]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


STAGES_M = [('prophase I', 'chromosomes condense; homologous chromosomes pair to form bivalents; crossing over at chiasmata; nuclear envelope breaks down'),
            ('metaphase I', 'bivalents line up on the equator of the spindle, with random orientation of each pair'),
            ('anaphase I', 'homologous chromosomes are pulled to opposite poles; chromatids stay joined at centromeres'),
            ('telophase I', 'two nuclei form, each with the haploid number of chromosomes (each still of two chromatids)'),
            ('metaphase II', 'chromosomes line up individually on the equators of two new spindles at right angles to the first'),
            ('anaphase II', 'centromeres divide and sister chromatids are pulled to opposite poles'),
            ('telophase II', 'four haploid nuclei form; cytokinesis gives four cells')]


@t.add('C3', (1, 2, 3, 4), 'short')
def meiosis_id(r, D):
    st_, desc = r.choice(STAGES_M)
    if D <= 2:
        return MQ(r, f'A photomicrograph of an anther cell shows that {desc}. Which stage of meiosis is shown?', cap(st_), [cap(s[0]) for s in STAGES_M if s[0] != st_], f'{cap(st_)}: {desc}.')
    n2 = r.choice([4, 6, 8])
    return Q(f'A cell from an organism with 2n = {n2} is seen in {st_}. Describe what is happening in the cell at this stage, and state how many chromatids are present in the cell (or each of the two cells if after meiosis I).',
             f'{cap(desc)}. Chromatids: ' + (f'{2 * n2}' if st_ in ('prophase I', 'metaphase I', 'anaphase I') else (f'{n2} per cell' if st_ in ('telophase I', 'metaphase II') else f'{n2} per cell, separating into {n2 // 2} per daughter nucleus')) + '.',
             'description [2]; correct chromatid number [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def meiosis_case(r, D):
    n2 = r.choice([4, 6])
    st = f'A student in {city(r)} draws diagrams of meiosis in a cell with 2n = {n2}, in which one homologous pair carries alleles A and a, and another carries B and b.'
    parts = [P_('Draw or describe the possible arrangements of these chromosomes at metaphase I and the gametes produced, ignoring crossing over.', 'Two arrangements: AB/ab or Ab/aB on the same side; gametes AB, ab, Ab, aB in equal proportions.', 'two arrangements [1]; four gamete types [1] [2]'),
             P_('Explain how crossing over between the A/a locus and the centromere would change the gametes from one cell.', 'Each meiosis would then produce four different gametes, rather than two types, because one chromatid of each homologue exchanges the allele.', 'non-sister chromatids exchange alleles [1]; four different gametes from one cell [1] [2]'),
             P_('Explain why gametes produced by meiosis are genetically different from each other while cells produced by mitosis are identical.', 'Mitosis: no pairing, no crossing over, chromatids separate so daughter cells receive identical copies; meiosis: crossing over and independent assortment of homologues, plus halving of chromosome number.', 'mitosis identical copies [1]; crossing over [1]; independent assortment [1] [3]'),
             P_('State the number of chromosomes in each cell at the end of meiosis II.', str(n2 // 2), '[1]'),
             P_('Suggest why errors in meiosis such as non-disjunction can lead to conditions such as Down syndrome.', 'If homologues or chromatids fail to separate, a gamete may have an extra chromosome; fertilisation gives a zygote with three copies (trisomy 21).', 'non-disjunction [1]; extra chromosome / trisomy [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the behaviour of chromosomes during meiosis and explain how meiosis contributes to genetic variation.', 'Prophase I bivalents, chiasmata, crossing over; metaphase I random orientation; anaphase I homologues separate; telophase I; meiosis II chromatids separate; four haploid cells; variation by crossing over (new combinations of linked alleles), independent assortment (2ⁿ), random fertilisation, mutation.',
           'meiosis I stages [3]; meiosis II [1]; crossing over [1]; independent assortment [1]; random fertilisation [1] [7]')])
t5a = t

# ---------------------------------------------------------------------
t = T('Monohybrid and dihybrid crosses including codominance, multiple alleles and sex linkage', 'monohybrid and dihybrid crosses')
facts(t, [('genotype', 'the alleles possessed by an organism for a particular gene or genes'),
          ('phenotype', 'the observable characteristics of an organism, resulting from its genotype and the environment'),
          ('codominance', 'a situation in which both alleles in a heterozygote are fully expressed in the phenotype'),
          ('multiple alleles', 'the existence of more than two alleles of a gene in a population, as in the ABO blood group gene'),
          ('sex linkage', 'the location of a gene on the X chromosome, so that its inheritance pattern differs between males and females'),
          ('test cross', 'a cross between an organism with a dominant phenotype and a homozygous recessive organism, used to find whether it is homozygous or heterozygous'),
          ('homozygous', 'having two identical alleles of a gene'),
          ('F1 generation', 'the first filial generation: the offspring of a cross between two pure-breeding parents')])
mcqs(t, [('What is the expected phenotypic ratio of the offspring of a cross between two heterozygotes for a gene showing complete dominance?', '3 : 1', 'Aa × Aa → 1 AA : 2 Aa : 1 aa.', ['1 : 2 : 1', '1 : 1', '9 : 3 : 3 : 1']),
         ('Why do females rarely show sex-linked recessive conditions such as haemophilia?', 'They need to inherit two copies of the recessive allele, one on each X chromosome', 'Males have only one X.', ['The allele is on the Y chromosome', 'Females have no X chromosomes', 'The allele is dominant in females']),
         ('A man with blood group AB has children with a woman of blood group O. What blood groups are possible in their children?', 'A and B only', 'IᴬIᴮ × IᵒIᵒ → IᴬIᵒ or IᴮIᵒ.', ['A, B, AB and O', 'AB and O only', 'O only']),
         ('From which parent does a son inherit an X-linked allele?', 'His mother', 'Sons inherit Y from their father.', ['His father', 'Either parent equally', 'Both parents']),
         ('What ratio is expected from a dihybrid test cross of a double heterozygote with unlinked genes?', '1 : 1 : 1 : 1', 'AaBb × aabb.', ['9 : 3 : 3 : 1', '3 : 1', '1 : 2 : 1'])])
shorts(t, [('Explain what is meant by a pure-breeding (true-breeding) organism.', 'An organism that is homozygous for the gene(s) considered, so it always produces offspring with the same phenotype when crossed with a similar organism.', '[1]'),
           ('State why a test cross uses a homozygous recessive organism.', 'Its gametes all carry the recessive allele, so the offspring phenotypes directly reveal the alleles in the gametes of the other parent.', '[2]')])
explain(t, [('Explain why a carrier of a sex-linked recessive condition is always female.', 'Females have two X chromosomes so can be heterozygous (one dominant, one recessive allele) without showing the condition; males have one X so a recessive allele is always expressed.', 'females two X / heterozygous [1]; males hemizygous so always express [1] [2]'),
            ('Explain how a test cross can be used to determine the genotype of a tall pea plant.', 'Cross it with a dwarf (tt) plant; if all offspring are tall the plant is TT; if about half are dwarf the plant is Tt.', 'cross with tt [1]; interpretation of results [1] [2]'),
            ('Explain the inheritance of tortoiseshell coat colour in cats, which is almost always found in females.', 'Coat colour gene on X with codominant alleles Xᴼ (orange) and Xᴮ (black); females XᴼXᴮ show both colours (tortoiseshell); males have one X so are either orange or black.', 'X-linked [1]; codominance in heterozygous females [1]; males have one allele [1] [3]'),
            ('Explain why a cross between two individuals with sickle cell trait gives a 1 : 2 : 1 ratio of phenotypes.', 'Alleles Hbᴬ and Hbˢ are codominant, so heterozygotes have a distinct phenotype (sickle cell trait); HbᴬHbˢ × HbᴬHbˢ gives 1 HbᴬHbᴬ : 2 HbᴬHbˢ : 1 HbˢHbˢ, each a different phenotype.', 'codominance [1]; genotype ratio = phenotype ratio [1] [2]')])
myths(t, [('A 3 : 1 ratio means that exactly three out of every four offspring will show the dominant phenotype.', 'A ratio gives probabilities; in a small sample the numbers may differ by chance.'),
          ('A son can inherit haemophilia from his father.', 'A son inherits his X chromosome from his mother; he receives a Y from his father.'),
          ('A person with blood group O has no blood group alleles.', 'Blood group O people are homozygous IᵒIᵒ; the Iᵒ allele codes for a non-functional enzyme so no A or B antigen is made.')])

for _fn, _nm in ((mono_q, 'mono'), (abo_q, 'abo'), (xl_q, 'xlink'), (di_q, 'dihybrid')):
    _fn.__name__ = _nm
    t.add('C3', (1, 2, 3, 4, 5), 'numerical')(_fn)


@t.add('C2', (2, 3, 4), 'explain')
def pedigree(r, D):
    sc = r.choice([('Two unaffected parents have an affected daughter.', 'autosomal recessive', 'The trait is recessive (parents are carriers); it cannot be X-linked recessive because the father would then be affected.'),
                   ('An affected man and an unaffected woman have only affected daughters and only unaffected sons, in several families.', 'X-linked dominant', 'All daughters receive the father\'s X so are affected; sons receive his Y.'),
                   ('Two unaffected parents have an affected son; the mother\'s brother is also affected; no females in the family are affected.', 'X-linked recessive (most likely)', 'The mother is a carrier; sons receive her X; males with one recessive allele show the trait.'),
                   ('Two affected parents have an unaffected child.', 'autosomal dominant', 'Both parents must be heterozygous; the child inherited the recessive allele from each, so the trait cannot be recessive.')])
    obs, mode, why = sc
    st = r.choice([f'In a pedigree studied by {person(r)}: {obs} Suggest the mode of inheritance and explain your reasoning.', f'A genetic counsellor in {city(r)} notes that {low(obs)} Explain what this suggests about how the condition is inherited.'])
    return Q(st, f'{cap(mode)}: {why}', f'mode of inheritance [1]; reasoning from the pedigree [1] [2]', 'explain')


@t.add('C4', (2, 3, 4, 5), 'case')
def cross_case(r, D):
    q = r.choice([di_q, xl_q, mono_q, abo_q])(r, 3)
    if not q or '_scen' not in q:
        return None
    main = P_(q['_ask'], q['answer'], q['key'])
    parts = [main,
             P_('Explain what is meant by the term allele.', 'A variant form of a gene found at the same locus on homologous chromosomes.', 'variant form of gene [1]; same locus [1] [2]'),
             P_('Explain why the observed numbers of offspring in such a cross usually differ from the expected ratio.', 'Fertilisation is random, so the ratio is a probability; with small numbers chance deviations are large; some genotypes may have lower survival.', 'random fertilisation / chance [1]; small sample [1] [2]'),
             P_('Name a statistical test that could be used to find whether the differences between observed and expected numbers are significant, and state the null hypothesis.', 'The chi-squared (χ²) test; null hypothesis: there is no significant difference between observed and expected numbers.', 'chi-squared [1]; null hypothesis [1] [2]')]
    for _ in range(10):
        out = case(r, q['_scen'], parts, k=(2, 3))
        if out and q['_ask'] in out['stem']:
            return out
    return None


longs(t, [('Explain, using genetic diagrams, the inheritance of ABO blood groups and of haemophilia.', 'ABO: three alleles Iᴬ, Iᴮ (codominant), Iᵒ (recessive); six genotypes, four phenotypes; e.g. IᴬIᵒ × IᴮIᵒ gives A, B, AB, O 1:1:1:1. Haemophilia: X-linked recessive, XᴴXʰ × XᴴY → daughters XᴴXᴴ, XᴴXʰ; sons XᴴY, XʰY; half of sons affected; males hemizygous; females rarely affected.',
           'ABO alleles and dominance [2]; correct ABO diagram [2]; X-linkage explained [1]; correct haemophilia diagram [2] [7]')])
t5b = t

# ---------------------------------------------------------------------
t = T('Autosomal linkage, epistasis and the chi-squared test', 'autosomal linkage, epistasis')
facts(t, [('autosomal linkage', 'the presence of two or more genes on the same autosome, so that their alleles tend to be inherited together'),
          ('epistasis', 'the interaction of two genes in which one gene affects or masks the expression of another'),
          ('recombinant', 'an offspring with a combination of alleles not found in either parent, produced by crossing over between linked genes'),
          ('recombination frequency', 'the percentage of offspring that are recombinants; it increases with the distance between linked genes'),
          ('chi-squared test', 'a statistical test used to find whether the difference between observed and expected frequencies of categorical data is significant'),
          ('null hypothesis', 'the hypothesis that there is no significant difference between observed and expected results, and any difference is due to chance'),
          ('degrees of freedom', 'the number of categories minus one in a chi-squared test')])
mcqs(t, [('What is the critical value of χ² at p = 0.05 with 3 degrees of freedom?', '7.82', 'From tables: 3.84 (1 df), 5.99 (2), 7.82 (3).', ['3.84', '5.99', '9.49']),
         ('A dihybrid test cross gives far more parental types than recombinant types. What is the most likely explanation?', 'The two genes are linked on the same chromosome', 'Alleles are inherited together unless crossing over occurs.', ['The genes are on different chromosomes', 'One allele is codominant', 'The genes show epistasis']),
         ('Which ratio results from recessive epistasis in a dihybrid cross of two double heterozygotes?', '9 : 3 : 4', 'e.g. mouse coat colour: aa masks the other gene.', ['9 : 3 : 3 : 1', '12 : 3 : 1', '15 : 1']),
         ('Which ratio results from dominant epistasis in a dihybrid cross of two double heterozygotes?', '12 : 3 : 1', 'A dominant allele of one gene masks the other gene.', ['9 : 3 : 4', '9 : 7', '1 : 1 : 1 : 1']),
         ('If the calculated χ² value is greater than the critical value at p = 0.05, what should be concluded?', 'The difference between observed and expected results is significant and the null hypothesis is rejected', 'Probability that the difference is due to chance is below 5%.', ['The difference is due to chance', 'The null hypothesis is accepted', 'The expected ratio has been confirmed'])])
shorts(t, [('State the formula for the chi-squared test.', 'χ² = Σ (O − E)² ÷ E, where O is observed and E expected numbers.', '[1]'),
           ('State why linked genes can still produce recombinant offspring.', 'Crossing over between non-sister chromatids during prophase I can separate the alleles of linked genes.', '[1]')])
explain(t, [('Explain how autosomal linkage changes the results of a dihybrid test cross.', 'Linked alleles are on the same chromosome and pass to gametes together, so parental combinations are more frequent than expected (not 1 : 1 : 1 : 1); recombinants appear only if crossing over occurs between the loci, so they are fewer.', 'alleles inherited together [1]; parental types more frequent [1]; recombinants from crossing over [1] [3]'),
            ('Explain why a 9 : 3 : 4 ratio is seen in the inheritance of coat colour in mice.', 'One gene (A/a) determines whether pigment is made; homozygous aa animals are albino whatever the alleles of the second gene (B/b, black or brown); the aa class combines 3 + 1 of the 9 : 3 : 3 : 1, giving 9 : 3 : 4.', 'epistatic gene masks second gene [1]; aa all albino [1]; combines classes to 9 : 3 : 4 [1] [3]'),
            ('Explain why 9 : 7 ratios are found in some dihybrid crosses, such as flower colour in sweet peas.', 'Two genes control two steps in a pathway to the pigment; a dominant allele of both is needed for colour; any aa or bb genotype blocks the pathway, so 9 coloured : 7 white.', 'two enzymes in pathway [1]; need dominant allele of both [1]; 9 : 7 [1] [3]'),
            ('Explain why the chi-squared test is used rather than simply comparing numbers.', 'Observed results always vary from expected by chance; the test gives a probability that the difference is due to chance, so we can decide objectively whether it is significant.', 'chance variation [1]; probability / significance [1] [2]')])
myths(t, [('If the χ² value is less than the critical value, the null hypothesis has been proved.', 'The test only shows that there is no significant difference (we accept the null hypothesis at that probability level); it does not prove it.'),
          ('Linked genes are always inherited together.', 'Crossing over in prophase I can separate linked alleles, producing recombinants.'),
          ('Degrees of freedom equal the number of offspring minus one.', 'Degrees of freedom equal the number of categories (classes) minus one.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def chi_sq(r, D):
    sc = r.choice([('9 : 3 : 3 : 1', [9, 3, 3, 1], 'a dihybrid cross between two double heterozygotes'), ('1 : 1 : 1 : 1', [1, 1, 1, 1], 'a dihybrid test cross'),
                   ('3 : 1', [3, 1], 'a monohybrid cross between two heterozygotes'), ('9 : 3 : 4', [9, 3, 4], 'a cross between double heterozygous mice (recessive epistasis)'),
                   ('12 : 3 : 1', [12, 3, 1], 'a cross between double heterozygous squash plants (dominant epistasis)'), ('1 : 2 : 1', [1, 2, 1], 'a cross between two roan cattle (codominance)'),
                   ('9 : 7', [9, 7], 'a cross between double heterozygous sweet pea plants (complementary genes)')])
    rname, w, what = sc
    N = r.choice([160, 200, 240, 320, 400, 480]) if sum(w) == 16 else r.choice([120, 160, 200, 240, 300])
    E = [N * x / sum(w) for x in w]
    linked = r.random() < 0.4 and len(w) == 4
    obs = []
    for i, e in enumerate(E):
        if linked:
            f = 1.35 if i in (0, 3) else 0.6
        else:
            f = r.uniform(0.88, 1.12)
        obs.append(max(1, round(e * f)))
    diff = N - sum(obs)
    obs[0] += diff
    chi = sum((o - e) ** 2 / e for o, e in zip(obs, E))
    df = len(w) - 1
    crit = CRIT_CHI[df][0]
    sig = chi > crit
    concl = (f'χ² = {fx(chi, 2)} > {crit}, so the difference is significant (p < 0.05); reject the null hypothesis' if sig else f'χ² = {fx(chi, 2)} < {crit}, so the difference is not significant; accept the null hypothesis that results fit {rname}')
    p = person(r)
    tbl = ', '.join(f'class {i + 1}: {o}' for i, o in enumerate(obs))
    st = f'{p} carried out {what} and expected a {rname} ratio. The observed numbers of offspring were {tbl} (total {N}).'
    rows = '; '.join(f'E = {fx(e, 1)}, (O − E)²/E = {fx((o - e) ** 2 / e, 3)}' for o, e in zip(obs, E))
    if D == 1:
        return NQ(r, st + ' How many degrees of freedom should be used in a chi-squared test?', df, [len(w), N - 1, df + 2, 1 if df != 1 else 4], '', f'Degrees of freedom = number of classes − 1 = {df}.', f=lambda v: str(int(v)))
    parts = [P_('Calculate the expected numbers for each class.', ', '.join(fx(e, 1) for e in E), f'N × fraction: {", ".join(fx(e, 1) for e in E)} [1]'),
             P_(f'Calculate the value of χ². The critical value of χ² at p = 0.05 for {df} degree{"s" if df > 1 else ""} of freedom is {crit}. State what your value of χ² shows.', concl + '.',
                f'{rows} [1]; Σ = {fx(chi, 2)} [1]; compare with {crit} [1]; correct conclusion about significance / null hypothesis [1] [4]'),
             P_('State the number of degrees of freedom for this test and explain how it is found.', f'{df}: the number of classes ({len(w)}) minus one.', '[1]')]
    if D >= 4:
        parts.append(P_('Suggest a biological explanation for the result.', ('The large excess of parental classes (1 and 4) suggests the genes are linked on the same chromosome; recombinants arise only by crossing over.' if linked and sig else ('The deviation suggests another factor, such as reduced survival of one genotype or linkage.' if sig else 'The genes are inherited as predicted (e.g. on different chromosomes / independent assortment); differences are due to chance in random fertilisation.')), 'valid explanation linked to result [2]'))
        parts.append(P_('State the null hypothesis for this test.', f'There is no significant difference between the observed and expected numbers; any difference is due to chance.', '[1]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def recomb(r, D):
    org, ga, gb, _ = r.choice(DI)
    N = r.choice([200, 400, 500, 800, 1000])
    rf = r.choice([0.06, 0.1, 0.12, 0.17, 0.2, 0.25, 0.3, 0.36])
    rec = round(N * rf)
    par = N - rec
    p1 = round(par / 2 + r.randint(-5, 5)); p2 = par - p1
    r1 = rec // 2; r2 = rec - r1
    st = (f'In {org}, the genes for {ga[2].split()[-1] if " " in ga[2] else "trait 1"} and {gb[2].split()[-1] if " " in gb[2] else "trait 2"} are on the same chromosome. A double heterozygote ({ga[0]}{gb[0]}/{ga[1]}{gb[1]}) was test-crossed with a homozygous recessive. '
          f'Offspring: {ga[2]}, {gb[2]} {p1}; {ga[3]}, {gb[3]} {p2}; {ga[2]}, {gb[3]} {r1}; {ga[3]}, {gb[2]} {r2}.')
    parts = [P_('Identify the recombinant offspring and explain how they were produced.', f'{ga[2]}, {gb[3]} and {ga[3]}, {gb[2]}: produced by crossing over between the two loci in prophase I of meiosis in the heterozygous parent.', 'recombinant classes [1]; crossing over in prophase I [1] [2]'),
             P_('Calculate the recombination frequency.', f'{fx(rec / N * 100, 1)}%', f'({r1} + {r2}) ÷ {N} × 100 [1] = {fx(rec / N * 100, 1)}% [1] [2]'),
             P_('Explain what the recombination frequency suggests about the positions of the two genes.', 'A low frequency means the loci are close together on the chromosome, so crossing over between them is rare; a higher frequency means they are further apart.', 'frequency related to distance [1]; crossing over less likely between close genes [1] [2]'),
             P_('State the ratio expected if the genes were not linked.', '1 : 1 : 1 : 1', '[1]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def epistasis_case(r, D):
    sys_ = r.choice([('mice', 'A (allows pigment)', 'a (no pigment, albino)', 'B (black)', 'b (brown)', [('black', 9), ('brown', 3), ('albino', 4)], 'recessive epistasis: aa is albino regardless of B/b'),
                     ('squash plants', 'W (white, blocks colour)', 'w (allows colour)', 'Y (yellow)', 'y (green)', [('white', 12), ('yellow', 3), ('green', 1)], 'dominant epistasis: any W gives white fruit regardless of Y/y'),
                     ('sweet pea plants', 'C (enzyme 1 made)', 'c (no enzyme 1)', 'P (enzyme 2 made)', 'p (no enzyme 2)', [('purple', 9), ('white', 7)], 'complementary genes: both C_ and P_ needed for purple pigment')])
    org, A, a, B, b, cls, why = sys_
    trait = {'mice': 'coat colour', 'squash plants': 'fruit colour', 'sweet pea plants': 'flower colour'}[org]
    N = r.choice([160, 320, 480])
    E = [N * n / 16 for _, n in cls]
    O = [max(1, round(e * r.uniform(0.9, 1.1))) for e in E]
    O[0] += N - sum(O)
    chi = sum((o - e) ** 2 / e for o, e in zip(O, E))
    df = len(cls) - 1
    crit = CRIT_CHI[df][0]
    st = (f'In {org}, {trait} is controlled by two unlinked genes: {A} / {a}, and {B} / {b}. Two double heterozygotes were crossed and produced ' + ', '.join(f'{o} {c}' for (c, _), o in zip(cls, O)) + f' offspring.')
    ratio = ' : '.join(str(n) for _, n in cls)
    parts = [P_('Explain the ratio of phenotypes obtained.', f'Close to {ratio}: {why}.', f'expected ratio {ratio} [1]; epistatic interaction explained [2] [3]'),
             P_(f'Calculate χ² for the hypothesis that the offspring are in a {ratio} ratio. The critical value at p = 0.05 for {df} degree{"s" if df > 1 else ""} of freedom is {crit}. Interpret your result.',
                f'χ² = {fx(chi, 2)}; ' + ('not significant; accept the null hypothesis: results fit the ratio' if chi < crit else 'significant; reject the null hypothesis'),
                f'expected {", ".join(fx(e, 0) for e in E)} [1]; χ² = {fx(chi, 2)} [1]; comparison with {crit} [1]; conclusion [1] [4]'),
             P_('Explain what is meant by epistasis.', 'An interaction between two genes in which one gene affects or masks the expression of another.', '[1]'),
             P_('Draw a genetic diagram to show the gametes and the genotypes that give each phenotype.', f'Gametes {A[0]}{B[0]}, {A[0]}{b[0]}, {a[0]}{B[0]}, {a[0]}{b[0]} from each parent; 16 combinations grouped into ' + ', '.join(c for c, _ in cls) + '.', 'four gamete types [1]; genotypes assigned to phenotypes [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how autosomal linkage and epistasis can each cause the results of a dihybrid cross to differ from a 9 : 3 : 3 : 1 ratio, and how the chi-squared test is used to evaluate such results.', 'Linkage: genes on same chromosome, alleles inherited together, parental types in excess, recombinants via crossing over, RF. Epistasis: one gene masks another, 9:3:4 (recessive), 12:3:1 (dominant), 9:7 (complementary), examples. χ²: null hypothesis, expected from ratio, Σ(O−E)²/E, df = classes − 1, compare critical value at p = 0.05.',
           'linkage [2]; epistasis with example ratio [2]; null hypothesis [1]; calculation [1]; df and interpretation [1] [7]')])
t5c = t

# ---------------------------------------------------------------------
t = T('Gene control: lac operon, transcription factors and gibberellin/DELLA', 'gene control: lac operon')
facts(t, [('operon', 'a group of structural genes in a prokaryote that are transcribed together from one promoter and controlled by one operator'),
          ('structural gene', 'a gene that codes for a protein that is not involved in controlling other genes, such as β-galactosidase'),
          ('regulatory gene', 'a gene that codes for a protein, such as the lac repressor, that controls the expression of other genes'),
          ('repressor protein', 'a protein that binds to the operator and prevents RNA polymerase from transcribing the structural genes'),
          ('operator', 'the region of DNA next to the structural genes to which a repressor protein binds'),
          ('promoter', 'the region of DNA to which RNA polymerase binds to begin transcription'),
          ('transcription factor', 'a protein that binds to DNA (e.g. at a promoter) and switches transcription of a gene on or off'),
          ('inducible enzyme', 'an enzyme that is synthesised only when its substrate is present, such as β-galactosidase')])
mcqs(t, [('In the lac operon, what happens when lactose is absent?', 'The repressor binds to the operator and RNA polymerase cannot transcribe the genes', 'The structural genes are off.', ['The repressor binds to lactose', 'RNA polymerase transcribes lacZ, lacY and lacA', 'β-galactosidase is produced in large amounts']),
         ('How does lactose switch on the lac operon?', 'It binds to the repressor, changing its shape so it cannot bind to the operator', 'Lactose (allolactose) is the inducer.', ['It binds to the promoter', 'It activates RNA polymerase directly', 'It is transcribed into mRNA']),
         ('Which enzyme coded by the lac operon allows lactose to enter the cell?', 'Lactose permease', 'lacY codes for permease; lacZ for β-galactosidase.', ['β-galactosidase', 'Transacetylase', 'RNA polymerase']),
         ('How does gibberellin stimulate the transcription of genes in plant cells?', 'It causes the breakdown of DELLA proteins, freeing transcription factors', 'DELLA proteins inhibit PIF transcription factors.', ['It binds directly to the promoter', 'It acts as RNA polymerase', 'It inhibits transcription factors'])])
shorts(t, [('State the names of the three structural genes in the lac operon and what each codes for.', 'lacZ: β-galactosidase; lacY: lactose permease; lacA: transacetylase.', '[2]'),
           ('Distinguish between a repressible and an inducible enzyme.', 'An inducible enzyme is made only when its substrate is present (gene normally off); a repressible enzyme is made unless a repressor is activated (gene normally on).', '[2]')])
explain(t, [('Explain how the lac operon allows E. coli to produce β-galactosidase only when lactose is present.', 'Regulatory gene makes repressor that binds operator, blocking RNA polymerase; lactose binds repressor, changing its shape so it leaves the operator; RNA polymerase binds promoter and transcribes lacZ, lacY, lacA; enzymes made; saves energy when lactose absent.', 'repressor binds operator [1]; lactose binds repressor / shape change [1]; RNA polymerase transcribes [1]; saves resources [1] [4]'),
            ('Explain how transcription factors control gene expression in eukaryotes.', 'Transcription factors bind to specific DNA sequences such as promoters; some help RNA polymerase bind and start transcription, others prevent it; different cells contain different factors so different genes are expressed.', 'bind specific DNA [1]; activate or repress RNA polymerase binding [1]; cell-specific expression [1] [3]'),
            ('Explain the role of DELLA proteins in the response of a seed to gibberellin.', 'DELLA proteins bind to transcription factors (PIF) and prevent transcription of genes such as amylase; gibberellin binds a receptor and causes DELLA to be destroyed (ubiquitination/proteasome), so PIF can promote transcription.', 'DELLA inhibit transcription factor [1]; gibberellin causes DELLA breakdown [1]; genes transcribed [1] [3]')])
myths(t, [('Lactose binds to the operator to switch the lac operon on.', 'Lactose binds to the repressor protein, which changes shape and can no longer bind to the operator.'),
          ('The regulatory gene is part of the operon and is switched off with it.', 'The regulatory gene (lacI) has its own promoter and is transcribed continuously; it is not part of the operon.'),
          ('All cells in an organism express the same genes.', 'All cells contain the same genes but different transcription factors switch different genes on and off.')])

LAC = [('a mutation in the regulatory gene produces a repressor that cannot bind to the operator', 'β-galactosidase is made all the time (constitutively), with or without lactose'),
       ('a mutation in the operator means the repressor cannot bind to it', 'β-galactosidase is made all the time, with or without lactose'),
       ('a mutation in the regulatory gene produces a repressor that cannot bind lactose', 'β-galactosidase is never made, even when lactose is present'),
       ('a mutation in the promoter prevents RNA polymerase from binding', 'none of the three enzymes is made, even with lactose present'),
       ('a mutation in lacY produces a non-functional permease', 'little lactose enters the cell so little β-galactosidase is induced; lactose is not used'),
       ('lactose is added to a culture growing in a medium with no other sugar', 'lactose enters, binds the repressor and the structural genes are transcribed, so β-galactosidase is produced within minutes')]


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def lac_apply(r, D):
    what, res = r.choice(LAC)
    if D == 1:
        return MQ(r, f'In a strain of E. coli, {what}. What is the effect on β-galactosidase production?', cap(res), [cap(x[1]) for x in LAC if x[1] != res], f'{cap(res)}.')
    st = r.choice([f'{person(r)} studies a strain of E. coli in which {what}. Predict and explain the effect on the production of β-galactosidase.', f'Explain the effect on the lac operon if {what}.'])
    return Q(st, cap(res) + '.', 'prediction [1]; explanation in terms of repressor / operator / RNA polymerase [2] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def lac_case(r, D):
    t1 = r.choice([20, 30, 40])
    st = f'E. coli were grown in a medium containing glucose only; at {t1} minutes lactose was added. β-galactosidase activity was negligible before {t1} minutes and rose rapidly from about {t1 + 3} minutes.'
    parts = [P_('Explain why β-galactosidase activity was negligible before lactose was added.', 'The repressor protein made by the regulatory gene was bound to the operator, so RNA polymerase could not transcribe lacZ.', 'repressor on operator [1]; no transcription [1] [2]'),
             P_('Explain why β-galactosidase activity rose after lactose was added.', 'Lactose entered (via a few permease molecules), bound to the repressor, changed its shape; repressor left the operator; RNA polymerase transcribed lacZ, lacY, lacA; mRNA translated.', 'lactose binds repressor [1]; repressor released [1]; transcription and translation [1] [3]'),
             P_('Suggest why there was a delay of a few minutes.', 'Time is needed for lactose to enter, and for transcription and translation of the genes.', '[1]'),
             P_('Explain the advantage to E. coli of this control mechanism.', 'Enzymes are made only when needed, so energy and amino acids are not wasted making unnecessary proteins.', '[2]'),
             P_('Compare gene control in the lac operon with control by transcription factors in eukaryotes.', 'Lac: repressor binds operator next to genes transcribed together on one mRNA. Eukaryotes: transcription factors bind promoter/enhancer of individual genes; can activate or repress; each gene usually has its own promoter.', 'operon vs individual genes [1]; repressor vs activating/repressing factors [1] [2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how the lac operon controls the production of β-galactosidase in E. coli, and how gibberellin controls gene expression in plants.', 'Operon: promoter, operator, lacZ, lacY, lacA; regulatory gene lacI makes repressor; repressor binds operator, blocking RNA polymerase; lactose binds repressor → shape change → released; transcription; inducible. Gibberellin: binds receptor; DELLA protein degraded; PIF transcription factor freed; binds promoter; amylase gene transcribed in aleurone.',
           'operon components [2]; lactose absent [1]; lactose present [2]; DELLA mechanism [2] [7]')])
t5d = t

CHAPTERS[5] = [t5a, t5b, t5c, t5d]


# ===================================================================== 6 Selection and evolution
def mean_sd(xs):
    n = len(xs)
    m = sum(xs) / n
    s = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    return m, s


def crit_t(df):
    keys = sorted(CRIT_T)
    best = max(k for k in keys if k <= df) if df >= keys[0] else keys[0]
    return CRIT_T[best], best


t = T('Variation: continuous and discontinuous; t-test', 'variation: continuous and discontinuous')
facts(t, [('continuous variation', 'variation in which a characteristic has a range of values between two extremes, such as height, usually controlled by many genes and influenced by the environment'),
          ('discontinuous variation', 'variation in which a characteristic falls into distinct categories with no intermediates, such as ABO blood group, usually controlled by one or a few genes'),
          ('polygene', 'one of several genes, each with a small additive effect, that together control a continuously variable characteristic'),
          ('standard deviation', 'a measure of the spread of data about the mean; about 68% of values lie within one standard deviation of the mean in a normal distribution'),
          ('t-test', 'a statistical test used to find whether the difference between the means of two samples of continuous data is significant'),
          ('standard error', 'an estimate of how close a sample mean is likely to be to the true population mean (SM = s ÷ √n)')])
mcqs(t, [('Which is an example of discontinuous variation in humans?', 'ABO blood group', 'Distinct categories, controlled by one gene.', ['Height', 'Body mass', 'Skin colour']),
         ('Which statistical test compares the means of two samples of continuous data?', 'The t-test', 'χ² is for categorical data.', ['The chi-squared test', 'Spearman\'s rank correlation', 'Simpson\'s index of diversity']),
         ('How many degrees of freedom are used in a t-test comparing two samples of 12 and 10 measurements?', '20', 'df = n₁ + n₂ − 2.', ['22', '21', '11']),
         ('Why is continuous variation often influenced strongly by the environment?', 'Many genes each have small effects, so environmental factors can shift the phenotype along the range', 'Polygenic characters show environmental effects.', ['It is controlled by one gene with two alleles', 'The environment changes the alleles', 'It has distinct categories'])])
shorts(t, [('State two differences between continuous and discontinuous variation.', 'Continuous: range of values, many genes (polygenic), large environmental effect, normal distribution. Discontinuous: distinct categories, one or few genes, little environmental effect, bar chart.', 'any two [2]'),
           ('State the null hypothesis for a t-test comparing the mean leaf lengths of plants in two habitats.', 'There is no significant difference between the mean leaf lengths in the two habitats.', '[1]')])
explain(t, [('Explain why characteristics controlled by several genes show continuous variation.', 'Each gene has alleles that add a small amount to the phenotype (additive effect); many combinations of alleles give a range of phenotypes; the environment adds further variation.', 'many genes, additive [1]; many combinations / range [1]; environment [1] [3]'),
            ('Explain how genotype and environment both contribute to the variation in the height of a crop plant.', 'Genotype sets the potential height through alleles of many genes; environmental factors (light, water, minerals, temperature) determine how far that potential is reached; phenotype results from the interaction.', 'genetic potential [1]; environmental factors [1]; interaction [1] [3]'),
            ('Explain why a t-test is more reliable than simply comparing two means.', 'Means differ by chance; the t-test takes into account the spread (standard deviation) and sample size, giving the probability that the difference is due to chance.', 'chance variation [1]; uses spread and sample size [1] [2]'),
            ('Explain why the standard deviation is a useful statistic when describing continuous data.', 'It shows the spread/variability of data around the mean; a small SD means values are close to the mean; it allows comparison of variation between samples.', 'spread around mean [1]; comparison / reliability [1] [2]')])
myths(t, [('Discontinuous variation is always caused by the environment.', 'Discontinuous variation is usually genetic, controlled by one or a few genes with little environmental influence.'),
          ('If the t value is larger than the critical value, the difference is due to chance.', 'A t value larger than the critical value means the difference is significant (p < 0.05) and unlikely to be due to chance.'),
          ('A large standard deviation means the mean is large.', 'Standard deviation measures spread of the data around the mean, not the size of the mean.')])

TT = [('leaf length', 'mm', 'leaves of ivy growing in shade', 'leaves of ivy growing in full sun', 60, 45, 6),
      ('shell length', 'mm', 'dog whelks on a sheltered shore', 'dog whelks on an exposed shore', 30, 26, 2.5),
      ('number of stomata in a field of view', '', 'leaves from the top of a tree', 'leaves from the bottom of a tree', 28, 22, 3),
      ('wing length', 'mm', 'house sparrows from a rural area', 'house sparrows from a city', 76, 74, 1.8),
      ('seed mass', 'mg', 'bean seeds from plants given fertiliser', 'bean seeds from plants without fertiliser', 920, 850, 45),
      ('body length', 'mm', 'Daphnia from a pond with fish', 'Daphnia from a pond without fish', 2.6, 3.0, 0.3)]


@t.add('C3', (2, 3, 4, 5), 'numerical')
def t_test(r, D):
    name, u, a, b, m1, m2, sd = r.choice(TT)
    n1 = r.choice([8, 10, 12, 15])
    n2 = r.choice([8, 10, 12, 15])
    same = r.random() < 0.35
    if same:
        m2 = m1 + (m2 - m1) * 0.15
    dp = 1 if m1 < 10 else 0
    xs = [round(r.gauss(m1, sd), dp) for _ in range(n1)]
    ys = [round(r.gauss(m2, sd), dp) for _ in range(n2)]
    if dp == 0:
        xs = [int(x) for x in xs]; ys = [int(y) for y in ys]
    ma, sa = mean_sd(xs)
    mb, sb = mean_sd(ys)
    tv = abs(ma - mb) / math.sqrt(sa ** 2 / n1 + sb ** 2 / n2)
    df = n1 + n2 - 2
    crit, dfk = crit_t(df)
    sig = tv > crit
    p = person(r)
    st = f'{p} measured the {name} of {a} (sample A, n = {n1}) and {b} (sample B, n = {n2}). Sample A: mean {fx(ma, dp + 2)}{(" " + u) if u else ""}, standard deviation {fx(sa, 3)}. Sample B: mean {fx(mb, dp + 2)}, standard deviation {fx(sb, 3)}.'
    if D >= 4:
        st = f'{p} measured the {name} of {a} (sample A) and {b} (sample B). Results{(" (" + u + ")") if u else ""}: A: {", ".join(str(x) for x in xs)}; B: {", ".join(str(y) for y in ys)}.'
    conc = (f't = {fx(tv, 2)} > {crit}, so the difference between the means is significant at p = 0.05; reject the null hypothesis' if sig else f't = {fx(tv, 2)} < {crit}, so the difference is not significant at p = 0.05; accept the null hypothesis')
    parts = [P_('State a null hypothesis for this investigation.', f'There is no significant difference between the mean {name} of the two samples.', '[1]'),
             P_(f'Calculate the value of t, using t = |x̄₁ − x̄₂| ÷ √(s₁²/n₁ + s₂²/n₂). The critical value of t at p = 0.05 for {dfk} degrees of freedom is {crit}. State the number of degrees of freedom and what your value of t shows.',
                f't = {fx(tv, 2)}; df = {n1} + {n2} − 2 = {df}; {conc}.',
                f'difference in means = {fx(abs(ma - mb), 3)} [1]; √({fx(sa, 3)}²/{n1} + {fx(sb, 3)}²/{n2}) = {fx(math.sqrt(sa ** 2 / n1 + sb ** 2 / n2), 3)} [1]; t = {fx(tv, 2)} [1]; df = {df} [1]; correct comparison and conclusion [1] [5]'),
             P_('Explain why a t-test, rather than a chi-squared test, is appropriate for these data.', 'The data are continuous measurements (approximately normally distributed) and two means are being compared; χ² is for counts in categories.', '[2]')]
    if D >= 4:
        parts.insert(1, P_('Calculate the mean and standard deviation of each sample.', f'A: mean {fx(ma, dp + 2)}, s = {fx(sa, 3)}; B: mean {fx(mb, dp + 2)}, s = {fx(sb, 3)}', 'means [1]; standard deviations [1] [2]'))
        parts.append(P_('Suggest one reason, other than chance, for any difference between the samples.', 'Environmental differences between the two sites (e.g. light, exposure, predation) or genetic differences between the populations (selection).', '[1]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C3', (1, 2, 3, 4), 'numerical')
def sd_calc(r, D):
    xs = sorted(r.sample(range(12, 40), 6))
    m, s = mean_sd(xs)
    what = r.choice(['the number of seeds per pod in a sample of bean pods', 'the lengths (mm) of six limpet shells', 'the number of lenticels on six twigs', 'the heights (cm) of six maize seedlings'])
    if D == 1:
        return NQ(r, f'The values for {what} were {", ".join(map(str, xs))}. What is the mean?', m, [sum(xs), m + 2, (max(xs) + min(xs)) / 2 + 3, s], '', f'Σ = {sum(xs)}; ÷ 6 = {fx(m, 2)}.', f=lambda v: fx(v, 2))
    return Q(f'The values for {what} were {", ".join(map(str, xs))}. Calculate the mean and the standard deviation, using s = √(Σ(x − x̄)² ÷ (n − 1)).', f'mean {fx(m, 2)}; s = {fx(s, 2)}',
             f'mean = {fx(m, 2)} [1]; Σ(x − x̄)² = {fx(sum((x - m) ** 2 for x in xs), 2)} [1]; ÷ 5, square root: s = {fx(s, 2)} [1] [3]', 'numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def var_case(r, D):
    org = r.choice(['a population of maize plants', 'a herd of goats', 'a clone of strawberry plants', 'a population of wild rabbits'])
    st = f'{person(r)} measured the height or mass of individuals in {org} in {city(r)} and found that the data formed a normal distribution.'
    parts = [P_('Explain why the data form a normal distribution.', 'The characteristic shows continuous variation: it is controlled by many genes (polygenes) with additive effects, plus environmental effects; most individuals are near the mean with few at the extremes.', 'polygenic [1]; additive / environment [1]; most near mean [1] [3]'),
             P_('Suggest why individuals of the clone still show variation.', 'Clones are genetically identical, so their variation must be caused by the environment (e.g. light, water, nutrients).' if 'clone' in org else 'Both genetic and environmental differences contribute; e.g. different alleles and different access to food.', '[2]'),
             P_('Describe how you would decide whether the mean value differs significantly from that of a second population.', 'Measure a large random sample from each; calculate means and standard deviations; carry out a t-test with df = n₁ + n₂ − 2; compare t with the critical value at p = 0.05.', 'random samples [1]; t-test [1]; compare with critical value [1] [3]'),
             P_('Explain the difference between variation caused by genes and variation caused by the environment in terms of whether it can be inherited.', 'Genetic variation is passed to offspring in gametes; environmental variation is not inherited (it changes the phenotype, not the alleles).', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Compare continuous and discontinuous variation and explain how genes and the environment contribute to each.', 'Discontinuous: categories, one/few genes, alleles with large effects, dominance/codominance, little environment (e.g. blood group). Continuous: range, polygenes with additive small effects, environment (height, mass), normal distribution; phenotype = genotype + environment; t-test for comparison.',
           'definitions [2]; genetic basis of each [2]; environmental influence [1]; examples [1]; statistical treatment [1] [7]')])
t6a = t

# ---------------------------------------------------------------------
t = T('Natural selection: stabilising, directional and disruptive selection; genetic drift; Hardy–Weinberg principle', 'natural selection')
facts(t, [('natural selection', 'the process by which individuals with alleles that give an advantage in a particular environment are more likely to survive and reproduce, so the allele frequency increases'),
          ('selection pressure', 'an environmental factor, such as predation or disease, that affects the chances of survival and reproduction of individuals'),
          ('stabilising selection', 'selection that favours intermediate phenotypes and acts against extremes, reducing variation (e.g. human birth mass)'),
          ('directional selection', 'selection that favours one extreme phenotype, shifting the mean (e.g. antibiotic resistance)'),
          ('disruptive selection', 'selection that favours both extremes and acts against intermediates, possibly leading to two forms'),
          ('genetic drift', 'a random change in allele frequency, most significant in small populations'),
          ('gene pool', 'all the alleles of all the genes in a population at a given time'),
          ('founder effect', 'the loss of genetic variation when a small group of individuals starts a new population')])
mcqs(t, [('Which type of selection is shown when the mean birth mass of human babies stays constant over many generations?', 'Stabilising', 'Very small and very large babies have lower survival.', ['Directional', 'Disruptive', 'Artificial']),
         ('Which statement about the Hardy–Weinberg principle is correct?', 'Allele frequencies stay constant if there is no selection, mutation, migration or drift and mating is random', 'Conditions for equilibrium.', ['Allele frequencies always change each generation', 'It applies only to small populations', 'It predicts the rate of mutation']),
         ('In the Hardy–Weinberg equation p² + 2pq + q² = 1, what does 2pq represent?', 'The frequency of heterozygotes', 'p² homozygous dominant, q² homozygous recessive.', ['The frequency of the dominant allele', 'The frequency of homozygous recessives', 'The frequency of the recessive allele']),
         ('Why is genetic drift more important in small populations?', 'Chance events have a larger effect on allele frequencies when there are few individuals', 'Random sampling error is greater in small samples.', ['Small populations have more mutations', 'Selection pressures are stronger in small populations', 'Mating is always random in small populations']),
         ('Bacteria exposed to an antibiotic become resistant over time. Which type of selection is this?', 'Directional', 'Resistant extreme favoured.', ['Stabilising', 'Disruptive', 'Genetic drift'])])
shorts(t, [('State the two Hardy–Weinberg equations.', 'p + q = 1; p² + 2pq + q² = 1.', '[2]'),
           ('State four conditions required for the Hardy–Weinberg principle to apply.', 'Large population; random mating; no mutation; no migration (gene flow); no selection.', 'any four [2]')])
explain(t, [('Explain how antibiotic resistance spreads in a population of bacteria.', 'Random mutation produces an allele for resistance; antibiotic is the selection pressure; non-resistant bacteria are killed; resistant bacteria survive and reproduce, passing the allele on (vertically, or by plasmid transfer); frequency of the allele increases (directional selection).', 'mutation [1]; selection pressure [1]; survival and reproduction of resistant [1]; allele frequency increases [1] [4]'),
            ('Explain how the sickle cell allele is maintained at a high frequency in regions with malaria.', 'Heterozygotes (sickle cell trait) are more resistant to malaria and do not have severe anaemia; they survive and reproduce more than either homozygote; so both alleles are kept in the population (heterozygote advantage).', 'heterozygote resistant to malaria [1]; HbˢHbˢ anaemia / HbᴬHbᴬ malaria [1]; both alleles maintained [1] [3]'),
            ('Explain the difference between natural selection and genetic drift.', 'Selection changes allele frequencies non-randomly because some alleles increase fitness; drift changes allele frequencies randomly by chance, especially in small populations, regardless of advantage.', 'selection non-random / advantage [1]; drift random / chance [1]; small populations [1] [3]'),
            ('Explain how disruptive selection could lead to two distinct forms in a population.', 'If both extremes are favoured (e.g. two food sources) and intermediates are selected against, individuals with alleles for extreme phenotypes survive and reproduce more; the population becomes bimodal and may split into two.', 'extremes favoured [1]; intermediates selected against [1]; bimodal / possible speciation [1] [3]')])
myths(t, [('Bacteria become resistant to antibiotics because they are exposed to them.', 'The resistance allele arises by random mutation; the antibiotic only selects for bacteria that already have it.'),
          ('Natural selection produces the mutations that an organism needs.', 'Mutations are random; selection acts on existing variation.'),
          ('In the Hardy–Weinberg equation, q² is the frequency of the recessive allele.', 'q is the frequency of the recessive allele; q² is the frequency of homozygous recessive individuals.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def hardy(r, D):
    cond = r.choice([('cystic fibrosis', 'people', 'of European descent'), ('phenylketonuria', 'babies', 'screened in one country'), ('albinism', 'people', 'in a small island population'),
                     ('a recessive white-flowered allele', 'plants', 'in a meadow'), ('a recessive dark wing colour', 'moths', 'in a city park'), ('sickle cell anaemia', 'people', 'in a malarial region')])
    name, who, where = cond
    one_in = r.choice([25, 50, 100, 400, 900, 1600, 2500, 10000]) if 'sickle' not in name else r.choice([25, 50, 100])
    q2 = 1 / one_in
    q = math.sqrt(q2)
    pp = 1 - q
    het = 2 * pp * q
    if D == 1:
        return NQ(r, f'In a population, 1 in {one_in:,} {who} has {name} (homozygous recessive). What is the frequency of the recessive allele?', q, [q2, 1 - q, 2 * q, q * 0.5], '',
                  f'q² = 1/{one_in:,}; q = √{fx(q2, 6)} = {fx(q, 4)}.', f=lambda v: fx(v, 4))
    p = person(r)
    st = f'{p} is studying {name} among {who} {where}. About 1 in {one_in:,} {who} show the condition, which is caused by a homozygous recessive genotype.'
    parts = [P_('Calculate the frequency of the recessive allele, q.', fx(q, 4), f'q² = 1 ÷ {one_in:,} = {fx(q2, 6)} [1]; q = {fx(q, 4)} [1] [2]'),
             P_('Calculate the frequency of the dominant allele, p.', fx(pp, 4), f'p = 1 − q = {fx(pp, 4)} [1]'),
             P_('Calculate the percentage of the population who are heterozygous carriers.', f'{fx(het * 100, 2)}%', f'2pq = 2 × {fx(pp, 4)} × {fx(q, 4)} [1] = {fx(het, 4)} = {fx(het * 100, 2)}% [1] [2]'),
             P_('State two assumptions made when using the Hardy–Weinberg principle.', 'Large population; random mating; no selection, mutation or migration.', 'any two [2]')]
    if D >= 4:
        N = r.choice([50000, 100000, 250000, 1000000])
        parts.append(P_(f'Estimate the number of carriers in a population of {N:,}.', f'{fx(het * N, 0)}', f'{fx(het, 4)} × {N:,} = {fx(het * N, 0)} [1]'))
        parts.append(P_('Suggest why the Hardy–Weinberg principle may not give accurate predictions for this population.', 'Selection may act on the genotype (e.g. heterozygote advantage or reduced survival of homozygotes); migration; non-random mating; small population size (drift).', 'any one valid reason [1]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


SELS = [('Over 50 years the mean beak depth of a finch species on an island increased after a drought left only large, hard seeds.', 'directional', 'birds with deeper beaks could crack the hard seeds, survived and reproduced, so alleles for deep beaks increased'),
        ('In a population of salmon, large males fight for females and very small males sneak matings, while medium-sized males rarely reproduce.', 'disruptive', 'both extremes reproduce more than intermediates, so alleles for both extremes are favoured'),
        ('Human babies of very low or very high birth mass have higher mortality than babies of about 3.5 kg.', 'stabilising', 'intermediate phenotypes survive best, so the mean stays constant and variation decreases'),
        ('After warfarin was used widely, rats in some cities became resistant to it.', 'directional', 'rats with the resistance allele survived poisoning and reproduced, so the resistance allele frequency increased'),
        ('On a beach with black and white pebbles, both very dark and very pale snails survive bird predation better than intermediate-coloured snails.', 'disruptive', 'extreme colours are camouflaged on one pebble type each; intermediates are seen and eaten'),
        ('In a mountain lake, the mean body size of a fish species stayed the same for thousands of years while the climate was stable.', 'stabilising', 'in a constant environment, intermediate sizes are best adapted, so extremes are selected against')]


@t.add('C3', (1, 2, 3, 4), 'short')
def sel_type(r, D):
    desc, typ, why = r.choice(SELS)
    if D == 1:
        return MQ(r, desc + ' Which type of selection is shown?', cap(typ), ['Stabilising', 'Directional', 'Disruptive', 'Genetic drift'], f'{cap(typ)}: {why}.')
    return Q(desc + ' Identify the type of selection and explain how it changes the population.', f'{cap(typ)} selection: {why}.', f'type [1]; explanation in terms of survival, reproduction and allele frequency [2] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def drift_case(r, D):
    N0 = r.choice([12, 20, 30, 50])
    st = f'A population of {N0} lizards was carried to a new island in {city(r)}\'s region by a storm. After 30 generations, the frequency of an allele for striped skin was {fx(r.uniform(0.6, 0.9), 2)}, compared with {fx(r.uniform(0.1, 0.3), 2)} on the mainland.'
    parts = [P_('Explain how the founder effect could account for this difference.', 'The founders were a small, random sample of the mainland population, which by chance had a high frequency of the striped allele; the new population started with different allele frequencies and less genetic variation.', 'small sample [1]; by chance not representative [1]; reduced variation [1] [3]'),
             P_('Explain how genetic drift could change the allele frequency further on the island.', 'In a small population, random differences in which individuals reproduce change allele frequencies by chance from generation to generation; alleles may be lost or fixed.', 'random / chance [1]; small population [1]; loss or fixation [1] [3]'),
             P_('Suggest how natural selection could also explain the high frequency of the striped allele.', 'If striped skin gives better camouflage on the island, striped lizards survive and reproduce more, increasing the allele frequency (directional selection).', 'selective advantage [1]; survival and reproduction / allele frequency [1] [2]'),
             P_('State why the Hardy–Weinberg principle would not apply to the island population.', 'The population is small (drift) and there may be selection, so allele frequencies are not constant.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how natural selection can change allele frequencies in a population, with reference to stabilising, directional and disruptive selection.', 'Variation by mutation and meiosis; overproduction; competition; selection pressures; individuals with advantageous alleles survive and reproduce, pass on alleles; stabilising favours intermediates (birth mass); directional shifts mean (antibiotic resistance); disruptive favours extremes; genetic drift in small populations; Hardy–Weinberg to detect change.',
           'variation and overproduction [1]; selection and allele frequency [2]; stabilising [1]; directional [1]; disruptive [1]; drift / HW [1] [7]')])
t6b = t

# ---------------------------------------------------------------------
t = T('Artificial selection: selective breeding of crops and dairy cattle', 'artificial selection')
facts(t, [('artificial selection', 'selection by humans of individuals with desirable characteristics to breed, so that the frequency of desired alleles increases over generations'),
          ('selective breeding', 'the deliberate crossing of chosen parents over many generations to produce organisms with desired traits'),
          ('inbreeding depression', 'the reduced vigour and fertility of offspring from closely related parents, caused by increased homozygosity of harmful recessive alleles'),
          ('hybrid vigour', 'the increased yield, size or resistance of F1 hybrids from crossing two different inbred lines'),
          ('progeny testing', 'assessing the breeding value of a bull by measuring the milk yield of his daughters')])
mcqs(t, [('Why is milk yield in bulls assessed by progeny testing?', 'Bulls do not produce milk, so their daughters\' yields are measured', 'The bull carries alleles for milk yield.', ['Bulls produce more milk than cows', 'Bulls are infertile', 'Milk yield is not inherited']),
         ('What is the main reason for growing F1 hybrid maize?', 'Hybrid vigour gives uniform, high-yielding plants', 'Crossing two inbred lines.', ['Hybrids are always disease-free', 'Hybrids breed true for many generations', 'Hybrids need no fertiliser']),
         ('Which characteristic was selected for in the breeding of modern bread wheat?', 'Short stems that resist lodging and high grain yield', 'Dwarfing alleles (reduced gibberellin response).', ['Tall stems', 'Seeds that fall from the ear easily', 'Low gluten content']),
         ('How does artificial selection differ from natural selection?', 'Humans choose which individuals reproduce, based on traits useful to humans', 'The selection pressure is human choice.', ['It does not involve alleles', 'It only occurs in plants', 'It increases genetic diversity'])])
shorts(t, [('State two characteristics that are selected for in dairy cattle.', 'High milk yield; high fat/protein content; docile temperament; disease resistance (e.g. mastitis); good udder shape.', 'any two [2]'),
           ('State why inbreeding of crop plants can reduce yields.', 'Increased homozygosity exposes harmful recessive alleles, reducing vigour (inbreeding depression).', '[1]')])
explain(t, [('Explain how a farmer could use selective breeding to increase milk yield in a herd of dairy cattle.', 'Measure milk yield of cows; choose cows with highest yield; choose bulls whose daughters have high yields (progeny testing); breed using artificial insemination; select the best offspring and repeat over many generations.', 'select high-yield cows [1]; progeny-tested bulls [1]; AI / IVF [1]; repeat over generations [1] [4]'),
            ('Explain why inbreeding and hybridisation are both used in the breeding of maize.', 'Inbreeding produces homozygous, uniform lines but with low vigour; crossing two different inbred lines produces heterozygous F1 hybrids with hybrid vigour and uniformity; seed must be produced each year.', 'inbred lines uniform but weak [1]; crossing gives hybrid vigour [1]; F1 uniform / new seed yearly [1] [3]'),
            ('Explain how breeders have produced varieties of rice and wheat resistant to fungal diseases.', 'Cross a high-yield variety with a variety (often wild) carrying alleles for resistance; select offspring showing resistance and high yield; backcross and repeat selection over many generations.', 'cross with resistant variety [1]; select desired offspring [1]; repeat / backcross [1] [3]'),
            ('Explain why selective breeding reduces genetic diversity.', 'Only a few individuals with desired traits are used as parents, so many alleles are lost from the gene pool; offspring become more homozygous.', 'few parents [1]; alleles lost / homozygosity [1] [2]')])
myths(t, [('Selective breeding creates new alleles for the desired characteristic.', 'Selective breeding increases the frequency of existing alleles; new alleles arise only by mutation.'),
          ('F1 hybrid seeds can be saved and replanted to give the same high yield.', 'The F2 generation shows segregation of alleles and loses the uniformity and hybrid vigour, so new F1 seed must be bought each year.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def breed_data(r, D):
    sp = r.choice([('dairy cows', 'mean annual milk yield', 'kg', 4000, 9000), ('maize', 'mean grain yield', 't ha⁻¹', 2.0, 9.5), ('wheat', 'mean grain yield', 't ha⁻¹', 1.5, 7.5), ('rice', 'mean grain yield', 't ha⁻¹', 2.0, 6.5)])
    org, var, u, lo, hi = sp
    y0 = round(r.uniform(lo, lo * 1.2), 1 if lo < 100 else -1)
    y1 = round(r.uniform(hi * 0.85, hi), 1 if lo < 100 else -1)
    yr0, yr1 = r.choice([(1960, 2020), (1950, 2010), (1970, 2020), (1965, 2015)])
    inc = pct(y0, y1)
    rate = (y1 - y0) / (yr1 - yr0)
    dp = 1 if lo < 100 else 0
    if D == 1:
        return NQ(r, f'The {var} of {org} in a country rose from {fx(y0, dp)} {u} in {yr0} to {fx(y1, dp)} {u} in {yr1}. What was the percentage increase?', inc, [inc / 100, y1 / y0 * 10, 100 - inc], '%', f'({fx(y1, dp)} − {fx(y0, dp)}) ÷ {fx(y0, dp)} × 100 = {fx(inc, 0)}%.', f=lambda v: fx(v, 0))
    st = f'Records from a breeding programme in {city(r)} show that the {var} of {org} rose from {fx(y0, dp)} {u} in {yr0} to {fx(y1, dp)} {u} in {yr1}.'
    parts = [P_('Calculate the percentage increase.', f'{fx(inc, 0)}%', f'({fx(y1, dp)} − {fx(y0, dp)}) ÷ {fx(y0, dp)} × 100 [1] = {fx(inc, 0)}% [1] [2]'),
             P_('Calculate the mean rate of increase per year.', f'{fx(rate, 3 if dp else 0)} {u} per year', f'{fx(y1 - y0, dp)} ÷ {yr1 - yr0} = {fx(rate, 3 if dp else 0)} [1]'),
             P_('Suggest two reasons, other than selective breeding, for the increase.', 'Better nutrition / feed or fertiliser; irrigation; pesticides / veterinary care; improved management and machinery.', 'any two [2]'),
             P_(f'Describe how selective breeding could have contributed to this increase in {org}.', ('Cows with the highest yields bred with progeny-tested bulls by artificial insemination; best offspring selected each generation.' if 'cows' in org else 'Plants with the highest yields (and short stems, disease resistance) selected as parents; crossed and selected over many generations; F1 hybrids / dwarf varieties.'), 'selection of parents [1]; repeated over generations [1] [2]')]
    if D >= 4:
        parts.append(P_('Discuss one disadvantage of intensive selective breeding.', 'Loss of genetic diversity, so the population is vulnerable to new diseases or environmental change; inbreeding depression; welfare problems (e.g. lameness, mastitis in high-yield cows).', 'disadvantage [1]; explanation [1] [2]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def breed_case(r, D):
    crop = r.choice([('wheat', 'resistance to rust fungus and short stems'), ('rice', 'tolerance of flooding and high yield'), ('maize', 'drought tolerance and uniform cobs'), ('cassava', 'resistance to mosaic virus')])
    st = f'Plant breeders in {city(r)} want to produce a new variety of {crop[0]} with {crop[1]}.'
    parts = [P_('Outline how they could use selective breeding to do this.', 'Identify varieties (including wild relatives / landraces) with each trait; cross them; grow offspring and select those with both traits; self or backcross and select over many generations until true-breeding.', 'sources of alleles [1]; cross [1]; select offspring [1]; repeat over generations [1] [4]'),
             P_('Explain why breeders keep collections of wild relatives and traditional varieties in seed banks.', 'They contain alleles (genetic diversity) lost from modern varieties, such as disease resistance, that can be bred into crops in future.', 'source of alleles [1]; future breeding / resistance [1] [2]'),
             P_('Explain why the dwarfing alleles in modern wheat and rice increased yield.', 'Short stems (reduced response to or production of gibberellin) resist lodging (falling over) and more photosynthate goes to grain rather than stem.', 'reduced gibberellin effect [1]; resist lodging / more to grain [1] [2]'),
             P_('Suggest one advantage of genetic engineering compared with selective breeding for this purpose.', 'Faster; a single gene can be transferred without unwanted alleles; genes can come from other species.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how artificial selection has been used to improve the milk yield of dairy cattle and the yield of cereal crops.', 'Dairy: record yields, select high-yield cows, progeny testing of bulls, AI, IVF/embryo transfer, repeat over generations. Cereals: select high-yield, disease-resistant, short-stem plants; dwarf varieties (gibberellin); inbreeding and hybridisation for hybrid vigour in maize; crossing with wild varieties for resistance; reduced genetic diversity.',
           'dairy selection [2]; progeny testing / AI [1]; cereal traits [1]; inbreeding and hybrid vigour [2]; disadvantage [1] [7]')])
t6c = t

# ---------------------------------------------------------------------
t = T('Evolution and speciation: allopatric and sympatric speciation; molecular comparisons', 'evolution and speciation')
facts(t, [('species', 'a group of organisms with similar morphology, physiology and behaviour that can interbreed to produce fertile offspring and are reproductively isolated from other species'),
          ('speciation', 'the formation of a new species from an existing one'),
          ('allopatric speciation', 'speciation that occurs when populations are separated by a geographical barrier and diverge until they can no longer interbreed'),
          ('sympatric speciation', 'speciation that occurs within the same area, through ecological, behavioural or genetic (e.g. polyploidy) isolation'),
          ('reproductive isolation', 'the inability of two populations to interbreed and produce fertile offspring, due to prezygotic or postzygotic barriers'),
          ('polyploidy', 'the possession of more than two complete sets of chromosomes, which can lead to instant sympatric speciation in plants'),
          ('molecular clock', 'the use of the number of differences in DNA or protein sequences, and the rate at which they accumulate, to estimate when two species diverged')])
mcqs(t, [('What usually starts allopatric speciation?', 'A geographical barrier separating two populations', 'e.g. a mountain range or sea.', ['Polyploidy', 'A change in mating behaviour within one area', 'Random mating']),
         ('Why is a mule (horse × donkey) not a new species?', 'Mules are infertile', 'Odd chromosome number (63) prevents meiosis.', ['Mules cannot survive', 'Mules look like horses', 'Mules have no chromosomes']),
         ('Two species have very few differences in the amino acid sequence of cytochrome c. What does this suggest?', 'They share a recent common ancestor', 'Fewer differences, more closely related.', ['They are unrelated', 'They live in the same habitat', 'Cytochrome c has no function']),
         ('Which is an example of a prezygotic isolating mechanism?', 'Different courtship behaviours', 'Behavioural isolation prevents mating.', ['Hybrid infertility', 'Hybrid inviability', 'Hybrid breakdown'])])
shorts(t, [('State three types of isolating mechanism that can lead to sympatric speciation.', 'Behavioural (courtship); ecological / habitat; temporal (breeding seasons); mechanical; polyploidy / chromosomal.', 'any three [3]'),
           ('Name two molecules whose sequences are compared to find evolutionary relationships.', 'DNA (e.g. mitochondrial DNA or rRNA genes) and proteins (e.g. cytochrome c, haemoglobin).', '[2]')])
explain(t, [('Explain how allopatric speciation occurs.', 'A geographical barrier separates a population; no gene flow; different selection pressures, mutations and drift in each; allele frequencies diverge; eventually they cannot interbreed (reproductive isolation) even if reunited.', 'barrier / no gene flow [1]; different selection / mutation / drift [1]; allele frequencies change [1]; reproductive isolation [1] [4]'),
            ('Explain how polyploidy can lead to the formation of a new plant species in a single generation.', 'Non-disjunction in meiosis produces diploid gametes; these fuse to form a tetraploid; the tetraploid cannot produce fertile offspring with the diploid parents (triploid offspring are sterile) but can breed with itself.', 'diploid gametes [1]; tetraploid [1]; triploid hybrids sterile / reproductive isolation [1] [3]'),
            ('Explain why comparisons of DNA sequences give more reliable evidence of relationships than comparisons of appearance.', 'Similar appearance may result from convergent evolution; DNA differences accumulate at a roughly constant rate, so numbers of differences reflect time since divergence; data are quantitative.', 'convergence [1]; molecular clock / quantitative [1] [2]'),
            ('Explain how mitochondrial DNA has been used to study human evolution.', 'mtDNA is inherited only from the mother and does not recombine; it mutates relatively quickly; comparing sequences shows relationships and dates divergence; supports African origin of modern humans.', 'maternal inheritance / no recombination [1]; mutation rate [1]; conclusion [1] [3]')])
myths(t, [('Two organisms that can mate must belong to the same species.', 'They must produce fertile offspring; horses and donkeys mate but mules are infertile.'),
          ('Individuals evolve during their lifetime to adapt to their environment.', 'Populations evolve through changes in allele frequency over generations; individuals do not evolve.'),
          ('Sympatric speciation requires a geographical barrier.', 'Sympatric speciation happens in the same area, through behavioural, ecological or chromosomal isolation.')])

BASES = 'ACGT'


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def seq_compare(r, D):
    L = r.choice([18, 21, 24, 27, 30])
    ref = ''.join(r.choice(BASES) for _ in range(L))
    sp = r.choice([['species A', 'species B', 'species C', 'species D'], ['the grey wolf', 'the coyote', 'the red fox', 'the domestic dog'], ['the chimpanzee', 'the gorilla', 'the orangutan', 'the human']])
    diffs = sorted(r.sample(range(1, 9), 3))
    seqs = {}
    for name, d in zip(sp[1:], diffs):
        s_ = list(ref)
        for i in r.sample(range(L), d):
            s_[i] = r.choice([b for b in BASES if b != s_[i]])
        seqs[name] = ''.join(s_)
    count = {n: sum(1 for a, b in zip(ref, s_) if a != b) for n, s_ in seqs.items()}
    order = sorted(count, key=lambda n: count[n])
    st = f'Part of the DNA sequence of a gene in {sp[0]} is {ref}. The same region in three other species is: ' + '; '.join(f'{n}: {seqs[n]}' for n in sp[1:]) + '.'
    if D == 1:
        return MQ(r, st + f' Which species is most closely related to {sp[0]}?', cap(order[0]), [cap(x) for x in order[1:]] + [cap(sp[0]) + ' is equally related to all three'], f'Differences: ' + ', '.join(f'{n} {count[n]}' for n in sp[1:]) + '; fewest = closest.')
    parts = [P_(f'Count the number of base differences between {sp[0]} and each of the other species.', ', '.join(f'{n}: {count[n]}' for n in sp[1:]), 'all three correct [2]'),
             P_(f'Use your answers to state which species is most closely related to {sp[0]}. Explain your answer.', f'{cap(order[0])}: fewest differences, so most recent common ancestor (mutations have had least time to accumulate).', 'correct species [1]; fewest differences → recent common ancestor [1] [2]'),
             P_(f'Calculate the percentage difference between {sp[0]} and {order[-1]}.', f'{fx(count[order[-1]] / L * 100, 1)}%', f'{count[order[-1]]} ÷ {L} × 100 = {fx(count[order[-1]] / L * 100, 1)}% [1]'),
             P_('Suggest why scientists compare long sequences rather than short ones like this.', 'A short sequence gives few differences, so chance has a large effect; longer sequences give more reliable estimates of relatedness.', '[2]')]
    if D >= 4:
        rate = r.choice([1, 2, 0.5])
        parts.append(P_(f'Assuming one base difference accumulates in this region every {fx(rate, 1)} million years, estimate when {sp[0]} and {order[0]} last shared a common ancestor.', f'about {fx(count[order[0]] * rate, 1)} million years ago', f'{count[order[0]]} × {fx(rate, 1)} = {fx(count[order[0]] * rate, 1)} million years [1]; (assumes constant rate) [1] [2]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


SPEC = [('Two populations of squirrels became separated when the Grand Canyon formed, and are now different species.', 'allopatric', 'a geographical barrier stopped gene flow'),
        ('Apple maggot flies that lay eggs on apples mate on apples, while those on hawthorn mate on hawthorn, in the same orchard; the two groups are diverging.', 'sympatric', 'ecological / behavioural isolation in the same area'),
        ('A new species of cord grass (Spartina anglica) arose from a sterile hybrid whose chromosome number doubled.', 'sympatric', 'polyploidy produced a fertile allopolyploid that is reproductively isolated from both parents'),
        ('Finches on different Galápagos islands, separated by sea, evolved into different species with different beak shapes.', 'allopatric', 'populations were separated by water and adapted to different food sources'),
        ('Cichlid fish in one African lake evolved into many species that prefer mates of different colours.', 'sympatric', 'behavioural (mate choice) isolation within the same lake'),
        ('Two populations of a frog species were separated when a river changed course, and now have different mating calls and cannot interbreed.', 'allopatric', 'a geographical barrier (river) separated them; their calls diverged')]


@t.add('C3', (1, 2, 3, 4), 'short')
def spec_type(r, D):
    desc, typ, why = r.choice(SPEC)
    if D == 1:
        return MQ(r, desc + ' Which type of speciation is this?', cap(typ), ['Allopatric', 'Sympatric', 'Artificial selection', 'Genetic drift only'], f'{cap(typ)}: {why}.')
    return Q(desc + ' Identify the type of speciation and explain how reproductive isolation arose.', f'{cap(typ)} speciation: {why}.', 'type [1]; isolating mechanism explained [1]; link to no gene flow / divergence [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def spec_case(r, D):
    st = f'Two populations of a ground beetle on either side of a mountain range near {city(r)} were found to differ in body colour and in the timing of their breeding seasons. When brought together in the laboratory they mated but produced few fertile offspring.'
    parts = [P_('Explain how the two populations could have become different.', 'The mountains are a geographical barrier preventing gene flow; different selection pressures (climate, predators) on each side; different mutations and genetic drift; allele frequencies diverged.', 'barrier / no gene flow [1]; selection [1]; mutation / drift [1] [3]'),
             P_('Discuss whether the two populations should be classified as separate species.', 'They are reproductively isolated to a large extent (few fertile offspring, different breeding times), so they may be separate species, but some fertile offspring mean isolation is incomplete; molecular evidence could help decide.', 'evidence for [1]; evidence against / incomplete [1]; need for further data [1] [3]'),
             P_('Describe how DNA sequencing could be used to investigate how long ago the populations separated.', 'Sequence the same gene(s) (e.g. mtDNA) in both; count differences; use a molecular clock (known mutation rate) to estimate time since divergence.', 'sequence same genes [1]; count differences [1]; molecular clock [1] [3]'),
             P_('Name the type of isolating mechanism shown by the different breeding seasons.', 'Temporal (seasonal) isolation — a prezygotic mechanism.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Explain how new species arise by allopatric and by sympatric speciation, and how molecular evidence can be used to show relationships between species.', 'Species definition; allopatric: barrier, no gene flow, different selection/mutation/drift, reproductive isolation; sympatric: same area, behavioural/ecological/temporal isolation, polyploidy in plants; molecular: DNA/protein sequences, differences accumulate over time, fewer differences = more closely related, molecular clock, mtDNA.',
           'definition of species [1]; allopatric [2]; sympatric with example [2]; molecular evidence [2] [7]')])
t6d = t

CHAPTERS[6] = [t6a, t6b, t6c, t6d]


# ===================================================================== 7 Classification, biodiversity and conservation
t = T('Classification: three domains, kingdoms and taxonomic hierarchy; viruses', 'classification: three domains')
facts(t, [('domain', 'the highest taxonomic rank: Bacteria, Archaea or Eukarya'),
          ('Archaea', 'a domain of prokaryotes with cell walls lacking peptidoglycan, membrane lipids with ether bonds, and some features (e.g. RNA polymerase, histone-like proteins) similar to eukaryotes'),
          ('taxonomic hierarchy', 'the arrangement of taxa in ranks: domain, kingdom, phylum, class, order, family, genus, species'),
          ('binomial nomenclature', 'the naming of each species with two Latin names, the genus followed by the species'),
          ('protoctist', 'a eukaryote that is not an animal, plant or fungus, often single-celled, such as Amoeba or Plasmodium'),
          ('virus', 'a non-cellular particle of nucleic acid in a protein coat, classified by the type of nucleic acid (DNA or RNA) and whether it is single- or double-stranded')])
mcqs(t, [('Which is the correct order of taxonomic ranks, from largest to smallest?', 'Domain, kingdom, phylum, class, order, family, genus, species', 'Use a mnemonic for D K P C O F G S.', ['Kingdom, domain, phylum, order, class, family, genus, species', 'Domain, kingdom, class, phylum, order, family, species, genus', 'Domain, phylum, kingdom, class, family, order, genus, species']),
         ('Which feature is found in Bacteria but not in Archaea?', 'Peptidoglycan in the cell wall', 'Archaeal walls lack peptidoglycan.', ['70S ribosomes', 'Circular DNA', 'A cell surface membrane']),
         ('Which kingdom has organisms with chitin cell walls that feed by extracellular digestion?', 'Fungi', 'Saprotrophic or parasitic, hyphae.', ['Plantae', 'Protoctista', 'Animalia']),
         ('How are viruses classified?', 'By the type of nucleic acid they contain and whether it is single- or double-stranded', 'Viruses are not placed in a domain.', ['By their cell wall composition', 'By the type of ribosomes', 'By the kingdom of their host']),
         ('In the name Panthera leo, what does Panthera represent?', 'The genus', 'Binomial: Genus species.', ['The species', 'The family', 'The order'])])
shorts(t, [('State three features of organisms in the kingdom Plantae.', 'Multicellular; eukaryotic cells with cellulose cell walls; chloroplasts and photosynthesis (autotrophic); large permanent vacuole; starch as storage carbohydrate.', 'any three [3]'),
           ('State two ways in which Archaea resemble Eukarya more than Bacteria.', 'Similar RNA polymerase; histone-like proteins associated with DNA; similar ribosomal proteins; introns in some genes.', 'any two [2]')])
explain(t, [('Explain why viruses are not included in the three-domain classification.', 'Viruses are non-cellular; they have no cytoplasm, ribosomes or metabolism and can only reproduce inside host cells, so they do not fit the features of any domain.', 'non-cellular [1]; no metabolism / ribosomes / only reproduce in host [1] [2]'),
            ('Explain why the three-domain system replaced the five-kingdom system.', 'Molecular evidence (rRNA sequences, membrane lipids, RNA polymerase) showed that prokaryotes form two very different groups, Bacteria and Archaea, which are as different from each other as from eukaryotes.', 'molecular / rRNA evidence [1]; two prokaryote groups very different [1] [2]'),
            ('Compare the features of the kingdoms Fungi and Plantae.', 'Both eukaryotic with cell walls. Fungi: chitin walls, heterotrophic, no chloroplasts, hyphae, glycogen store. Plants: cellulose walls, autotrophic with chloroplasts, starch store.', 'cell wall composition [1]; nutrition [1]; storage carbohydrate / body form [1] [3]'),
            ('Explain the advantages of using scientific (binomial) names.', 'Each species has a unique name used internationally, avoiding confusion from local common names; the genus name shows close relationships.', 'universal / unique [1]; shows relationship [1] [2]')])
myths(t, [('Archaea are just a type of bacteria.', 'Archaea form a separate domain; they differ from Bacteria in cell wall, membrane lipids, rRNA and RNA polymerase.'),
          ('Fungi are plants because they have cell walls and do not move.', 'Fungi have chitin walls, no chloroplasts and are heterotrophic, so they form a separate kingdom.'),
          ('Viruses belong to the domain Bacteria because they are microscopic.', 'Viruses are non-cellular and are not classified into any domain.')])

HIER = [('lion', ['Eukarya', 'Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Felidae', 'Panthera', 'leo']),
        ('human', ['Eukarya', 'Animalia', 'Chordata', 'Mammalia', 'Primates', 'Hominidae', 'Homo', 'sapiens']),
        ('domestic dog', ['Eukarya', 'Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Canidae', 'Canis', 'familiaris']),
        ('honeybee', ['Eukarya', 'Animalia', 'Arthropoda', 'Insecta', 'Hymenoptera', 'Apidae', 'Apis', 'mellifera']),
        ('garden pea', ['Eukarya', 'Plantae', 'Tracheophyta', 'Magnoliopsida', 'Fabales', 'Fabaceae', 'Pisum', 'sativum']),
        ('African elephant', ['Eukarya', 'Animalia', 'Chordata', 'Mammalia', 'Proboscidea', 'Elephantidae', 'Loxodonta', 'africana'])]
RANKS = ['domain', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']


@t.add('C3', (1, 2, 3, 4), 'short')
def hier_q(r, D):
    org, h = r.choice(HIER)
    i = r.randrange(1, 8)
    if D <= 2:
        return MQ(r, f'The classification of the {org} is: ' + ', '.join(h[:i]) + ', ?, ' + ', '.join(h[i + 1:]) + f'. Which taxonomic rank is missing?', cap(RANKS[i]), [cap(x) for x in RANKS if x != RANKS[i]][:6], f'Order: {", ".join(RANKS)}; missing rank = {RANKS[i]} ({h[i]}).')
    sh = list(zip(RANKS, h))
    r.shuffle(sh)
    return Q(f'The taxa to which the {org} belongs are given in random order: ' + ', '.join(n for _, n in sh) + '. Arrange them in order from domain to species, naming each rank, and write the scientific name correctly.',
             '; '.join(f'{rk}: {n}' for rk, n in zip(RANKS, h)) + f'. Scientific name: {h[6]} {h[7]}.', 'correct order [2]; ranks named [1]; binomial written with capital genus and lower-case species [1] [4]', 'short')


DOMF = [('a prokaryote with peptidoglycan cell walls and ester-linked membrane lipids', 'Bacteria'), ('a prokaryote living in a hot spring, with ether-linked membrane lipids and no peptidoglycan', 'Archaea'),
        ('a single-celled organism with a nucleus, chloroplasts and two flagella, but no cell wall', 'Eukarya (kingdom Protoctista)'), ('a multicellular heterotroph with chitin cell walls and hyphae', 'Eukarya (kingdom Fungi)'),
        ('a methane-producing prokaryote from a cow\'s rumen with histone-like proteins', 'Archaea'), ('a multicellular organism with cellulose cell walls and chloroplasts', 'Eukarya (kingdom Plantae)'),
        ('a multicellular heterotroph whose cells have no cell walls and which has a nervous system', 'Eukarya (kingdom Animalia)')]


@t.add('C3', (1, 2, 3, 4), 'short')
def dom_id(r, D):
    desc, ans = r.choice(DOMF)
    if D <= 2:
        return MQ(r, f'A newly described organism is {desc}. To which group does it belong?', ans, [x[1] for x in DOMF if x[1] != ans], f'{ans}.')
    return Q(f'{person(r)} examined {desc}. State, with reasons, the domain (and kingdom, if appropriate) in which it should be classified.', f'{ans}: features given match this group.', f'correct group [1]; two features used as reasons [2] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def class_case(r, D):
    v = r.choice([('HIV', 'single-stranded RNA', 'retrovirus with reverse transcriptase'), ('the measles virus', 'single-stranded RNA', 'enveloped'), ('the smallpox virus', 'double-stranded DNA', 'large, complex'),
                   ('the tobacco mosaic virus', 'single-stranded RNA', 'rod-shaped, infects plants'), ('a bacteriophage (T4)', 'double-stranded DNA', 'infects bacteria')])
    st = f'Scientists in {city(r)} are classifying organisms isolated from a hot spring, together with a virus, {v[0]}, which contains {v[1]}.'
    parts = [P_('Explain how they would decide whether a prokaryote isolated from the hot spring belongs to the Bacteria or the Archaea.', 'Test the cell wall for peptidoglycan; analyse membrane lipids (ether vs ester bonds); sequence rRNA genes and compare; examine RNA polymerase.', 'cell wall [1]; membrane lipids [1]; rRNA sequencing [1] [3]'),
             P_(f'Explain how {v[0]} is classified.', f'By its nucleic acid: {v[1]}; and other features ({v[2]}); viruses are not placed in a domain because they are non-cellular.', 'nucleic acid type and strandedness [1]; not in domains [1] [2]'),
             P_('Describe the features of the kingdom Protoctista.', 'Eukaryotic; mostly single-celled (some multicellular algae); some photosynthetic (plant-like), some heterotrophic (animal-like); diverse group not fitting other kingdoms.', 'eukaryotic [1]; diverse features [1] [2]'),
             P_('Explain why classification systems change over time.', 'New evidence, especially molecular data (DNA, rRNA sequences), changes our understanding of relationships, so groups are revised.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the three-domain system of classification and the features of the four eukaryotic kingdoms.', 'Domains Bacteria, Archaea, Eukarya with distinguishing features (walls, lipids, rRNA, ribosomes, histones); Eukarya kingdoms: Protoctista, Fungi (chitin, heterotrophic, hyphae), Plantae (cellulose, chloroplasts, autotrophic), Animalia (no wall, heterotrophic, nervous coordination); hierarchy; viruses separate.',
           'three domains with features [3]; four kingdoms [3]; hierarchy / viruses [1] [7]')])
t7a = t

# ---------------------------------------------------------------------
t = T("Biodiversity: random sampling, quadrats, transects, Simpson's index and Spearman's rank / Pearson's correlation", 'biodiversity: random sampling')
facts(t, [('biodiversity', 'the variety of ecosystems, habitats, species and genetic diversity within species in an area'),
          ('species richness', 'the number of different species present in an area'),
          ('species evenness', 'how evenly the individuals in an area are spread among the species present'),
          ("Simpson's index of diversity", 'a measure of biodiversity, D = 1 − Σ(n/N)², that takes account of species richness and evenness; values range from 0 (low) to 1 (high)'),
          ('random sampling', 'a method of sampling in which every part of an area has an equal chance of being sampled, e.g. using random number coordinates'),
          ('belt transect', 'a line across a habitat along which quadrats are placed at regular intervals, used to study changes in distribution'),
          ('mark-release-recapture', 'a method of estimating the population size of mobile animals using the Lincoln index: N = (n₁ × n₂) ÷ m₂'),
          ('correlation', 'a relationship between two variables; it does not prove that one causes the other')])
mcqs(t, [('Why are quadrats placed at coordinates from a random number generator?', 'To avoid bias in choosing sampling sites', 'Every point has an equal chance of selection.', ['To make sampling faster', 'To sample only the most diverse areas', 'To ensure all quadrats contain the same species']),
         ("What does a Simpson's index of diversity close to 1 indicate?", 'High biodiversity', 'D = 1 − Σ(n/N)²; values near 1 mean high richness and evenness.', ['Low biodiversity', 'Only one species present', 'One dominant species']),
         ('Which method is most suitable for estimating the population of beetles in a field?', 'Mark-release-recapture', 'For mobile animals.', ['Frame quadrats', 'Line transect', 'Point quadrats']),
         ("When should Spearman's rank correlation be used rather than Pearson's correlation?", 'When the data are not normally distributed or are ranked', 'Pearson\'s requires normally distributed interval data.', ['When there is a causal relationship', 'When comparing two means', 'When data are categorical counts']),
         ('Which method is best for studying how plant species change from the edge of a woodland into a field?', 'A belt transect', 'Systematic sampling along an environmental gradient.', ['Random quadrats across the whole area', 'Mark-release-recapture', 'Pitfall traps placed randomly'])])
shorts(t, [("State the formula for Simpson's index of diversity.", 'D = 1 − Σ(n/N)², where n = number of individuals of each species and N = total number of individuals.', '[1]'),
           ('State three assumptions made when using the Lincoln index.', 'No births, deaths, immigration or emigration between samples; marks not lost and do not affect survival; marked individuals mix randomly with the population; equal chance of capture.', 'any three [3]')])
explain(t, [('Explain why biodiversity is important.', 'Ecosystem stability and services (pollination, nutrient cycling, water purification); sources of food, medicines and genes for crops; economic (tourism); ethical / aesthetic reasons.', 'any three valid reasons [3]'),
            ('Explain the difference between species richness and biodiversity measured with Simpson\'s index.', 'Richness counts species only; Simpson\'s index also accounts for evenness (relative abundance), so two areas with the same richness can have different diversity.', 'richness = number of species [1]; Simpson\'s includes evenness [1] [2]'),
            ('Explain why systematic sampling along a transect is used instead of random sampling in some studies.', 'Where there is an environmental gradient (e.g. shore, woodland edge), a transect shows how distribution changes with the gradient; random sampling might miss zones.', 'environmental gradient [1]; shows change in distribution [1] [2]'),
            ('Explain why a significant correlation does not show that one variable causes the other.', 'Both variables may be affected by a third factor, or the correlation may be coincidental; an experiment controlling other variables is needed to show causation.', 'third variable / coincidence [1]; experiment needed [1] [2]')])
myths(t, [("A Simpson's index of 0 means there are no species in the area.", 'D = 0 means there is only one species (no diversity); the area may still contain many individuals.'),
          ('A high Spearman\'s rank coefficient proves that one factor causes the change in the other.', 'Correlation does not prove causation; other factors may be responsible.'),
          ('In mark-release-recapture, more marked animals in the second sample means a larger population.', 'A higher proportion of marked animals in the second sample indicates a smaller population.')])

SPP = ['daisy', 'clover', 'dandelion', 'plantain', 'buttercup', 'ryegrass', 'yarrow', 'moss', 'thistle', 'self-heal']


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def simpson(r, D):
    k = r.choice([4, 5, 6]) if D >= 3 else r.choice([3, 4])
    sp = r.sample(SPP, k)
    ns = [r.randint(2, 40) for _ in sp]
    N = sum(ns)
    s2 = sum((n / N) ** 2 for n in ns)
    Dv = 1 - s2
    site = r.choice(['a school field', 'a road verge', 'a grazed pasture', 'a lawn in a park', 'a meadow'])
    tbl = ', '.join(f'{s} {n}' for s, n in zip(sp, ns))
    if D == 1:
        return NQ(r, f'In {site}, the numbers of each species counted were: {tbl}. Calculate Simpson\'s index of diversity, D = 1 − Σ(n/N)².', Dv, [s2, 1 - Dv / 2, Dv / k, min(0.99, Dv + 0.15)], '',
                  f'N = {N}; Σ(n/N)² = {fx(s2, 3)}; D = {fx(Dv, 3)}.', f=lambda v: fx(v, 2))
    p = person(r)
    st = f'{p} sampled {site} in {city(r)} using ten randomly placed 0.5 m × 0.5 m quadrats. Total numbers of each plant species: {tbl}.'
    parts = [P_("Calculate Simpson's index of diversity, D = 1 − Σ(n/N)².", fx(Dv, 3), f'N = {N} [1]; Σ(n/N)² = ' + ' + '.join(f'({n}/{N})²' for n in ns) + f' = {fx(s2, 3)} [1]; D = {fx(Dv, 3)} [1] [3]'),
             P_('State what the value of D indicates about the biodiversity of the area.', ('Fairly high biodiversity: D is close to 1, so species richness and evenness are high.' if Dv > 0.7 else 'Relatively low biodiversity: D is well below 1, so one or two species dominate.'), 'correct interpretation linked to value [1]'),
             P_('Describe how the quadrats were placed randomly.', 'Lay two tape measures at right angles as axes; use a random number generator to give coordinates; place the quadrat at each coordinate.', 'grid / axes [1]; random number coordinates [1] [2]'),
             P_('Calculate the mean density of the most common species per m², given that ten quadrats were used.', f'{fx(max(ns) / 2.5, 1)} per m²', f'area sampled = 10 × 0.25 = 2.5 m² [1]; {max(ns)} ÷ 2.5 = {fx(max(ns) / 2.5, 1)} per m² [1] [2]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


def rank(vals):
    srt = sorted(vals)
    out = []
    for v in vals:
        idx = [i for i, x in enumerate(srt) if x == v]
        out.append(sum(idx) / len(idx) + 1)
    return out


SPEAR = [('distance from the woodland edge', 'm', 'light intensity', 'lux'), ('soil moisture content', '%', 'number of rushes per quadrat', ''), ('height above low tide', 'm', 'percentage cover of barnacles', '%'),
         ('soil pH', '', 'number of earthworms per quadrat', ''), ('trampling (number of people passing per hour)', '', 'plantain density per m²', '')]


@t.add('C3', (2, 3, 4, 5), 'numerical')
def spearman(r, D):
    x1, u1, x2, u2 = r.choice(SPEAR)
    n = r.choice([7, 8, 9, 10])
    xs = r.sample(range(1, 60), n)
    sign = r.choice([1, -1])
    noise = r.choice([3, 8, 20])
    ys = [max(0, round(30 + sign * 0.6 * x + r.gauss(0, noise))) for x in xs]
    if len(set(ys)) < n:
        return None
    rx, ry = rank(xs), rank(ys)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rs = 1 - 6 * d2 / (n * (n * n - 1))
    crit = CRIT_RS[n]
    sig = abs(rs) > crit
    p = person(r)
    st = f'{p} recorded {x1} and {x2} at {n} sampling points: ' + '; '.join(f'({x}, {y})' for x, y in zip(xs, ys)) + f'.'
    conc = f'|rₛ| = {fx(abs(rs), 2)} {">" if sig else "<"} {crit}, so the ' + ('correlation is significant at p = 0.05: there is a ' + ('positive' if rs > 0 else 'negative') + ' correlation' if sig else 'correlation is not significant at p = 0.05')
    parts = [P_('State a null hypothesis for this investigation.', f'There is no correlation between {x1} and {x2}.', '[1]'),
             P_(f"Calculate Spearman's rank correlation coefficient, rₛ = 1 − 6Σd² ÷ (n(n² − 1)). The critical value of rₛ for n = {n} at p = 0.05 is {crit}. Interpret your result.", f'rₛ = {fx(rs, 2)}; ' + conc + '.',
                f'ranks assigned [1]; Σd² = {fx(d2, 1)} [1]; rₛ = 1 − (6 × {fx(d2, 1)}) ÷ ({n} × {n * n - 1}) = {fx(rs, 2)} [1]; comparison with {crit} [1]; conclusion [1] [5]'),
             P_('Describe the trend shown by the data in words.', ('In general, as ' + x1 + ' increases, ' + x2 + (' increases.' if rs > 0 else ' decreases.')) if abs(rs) > 0.3 else 'There is no clear trend.', '[1]')]
    if D >= 4:
        parts.append(P_('Explain why Spearman\'s rank test was used rather than Pearson\'s correlation coefficient.', 'The data may not be normally distributed (counts / small sample), and Spearman\'s uses ranks, so it is suitable for non-parametric data.', '[2]'))
        parts.append(P_('Suggest why a significant correlation does not prove a causal link.', 'Another factor that varies with the first (e.g. soil moisture with light) may be responsible.', '[1]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def lincoln(r, D):
    org = r.choice(['woodlice', 'ground beetles', 'snails', 'grasshoppers', 'freshwater shrimps', 'field mice'])
    N = r.choice([120, 180, 240, 300, 400, 600, 900])
    n1 = r.choice([30, 40, 50, 60, 80])
    n2 = r.choice([30, 40, 50, 60, 75])
    m2 = max(2, round(n1 * n2 / N))
    est = n1 * n2 / m2
    if D == 1:
        return NQ(r, f'{n1} {org} were caught, marked and released. Later, {n2} were caught, of which {m2} were marked. What is the estimated population size?', est, [n1 + n2, n1 * m2 / n2, n2 * m2, est / 2], '', f'N = (n₁ × n₂) ÷ m₂ = ({n1} × {n2}) ÷ {m2} = {fx(est, 0)}.', f=lambda v: fx(v, 0))
    p = person(r)
    st = f'{p} caught {n1} {org} in a garden in {city(r)}, marked each with a dot of non-toxic paint and released them. Two days later {n2} were caught, of which {m2} were marked.'
    parts = [P_('Estimate the population size using the Lincoln index.', fx(est, 0), f'N = (n₁ × n₂) ÷ m₂ [1] = ({n1} × {n2}) ÷ {m2} = {fx(est, 0)} [1] [2]'),
             P_('State two assumptions made in this estimate.', 'No births/deaths or migration between samples; marks not lost and do not affect survival or behaviour; marked animals mix randomly.', 'any two [2]'),
             P_('Explain why the marks must not make the animals more visible to predators.', 'Marked animals would be eaten more, so fewer marked recaptured, overestimating the population.', 'fewer recaptured [1]; overestimate [1] [2]'),
             P_('Explain why the animals were left for two days before the second sample.', 'To allow marked animals to mix randomly with the rest of the population.', '[1]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def transect_case(r, D):
    dists = [0, 5, 10, 15, 20, 25]
    light = sorted([r.randint(200, 12000) for _ in dists], reverse=r.choice([True, False]))
    cover = [max(0, min(100, round(l / 130 + r.uniform(-8, 8)))) for l in light]
    st = (f'{person(r)} used a belt transect from inside a woodland to an open field in {city(r)}. At 5 m intervals, light intensity (lux) and percentage cover of grass were: '
          + '; '.join(f'{d} m: {l} lux, {c}%' for d, l, c in zip(dists, light, cover)) + '.')
    parts = [P_('Describe how the percentage cover of grass in a quadrat would be estimated.', 'Use a 1 m² quadrat divided into 100 squares; count the squares more than half covered by grass, or use a point frame; each square = 1%.', 'grid quadrat [1]; counting method [1] [2]'),
             P_('Describe the relationship between light intensity and grass cover.', 'Grass cover is higher where light intensity is higher (positive correlation).', '[1]'),
             P_("Name a statistical test to find whether the correlation is significant, and state why it is suitable.", "Spearman's rank correlation; the data are paired measurements that may not be normally distributed.", 'test [1]; reason [1] [2]'),
             P_('Suggest two other abiotic factors that could change along the transect.', 'Soil moisture; soil pH; temperature; humidity; mineral ion concentration; leaf litter depth.', 'any two [2]'),
             P_('Explain why a belt transect was used rather than random sampling.', 'There is a gradient of conditions from woodland to field; a transect samples systematically along it, showing how distribution changes.', '[2]'),
             P_('Suggest how the reliability of the results could be improved.', 'Repeat the transect several times at different places; take light readings at the same time of day / repeated; use more quadrats.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how you would investigate whether the distribution of a plant species is correlated with soil moisture across a habitat, and how you would analyse your results.', 'Belt transect across gradient; quadrats at regular intervals; percentage cover / density; measure soil moisture (dry mass method or probe); repeat transects; plot scatter graph; Spearman\'s rank: null hypothesis, ranks, d², formula, compare critical value at p = 0.05; correlation not causation; Pearson\'s if normally distributed.',
           'sampling method [2]; measuring abundance [1]; measuring moisture [1]; statistical test [2]; limitation [1] [7]'),
          ("Explain what is meant by biodiversity and describe how Simpson's index is used to compare the biodiversity of two areas.", 'Biodiversity: ecosystem, species (richness and evenness), genetic. Random sampling with quadrats; identify and count each species; D = 1 − Σ(n/N)²; higher D = higher diversity; compare D values; also compare with standard deviation / repeated samples.',
           'levels of biodiversity [2]; sampling [2]; formula and interpretation [2]; comparison [1] [7]')])
t7b = t

# ---------------------------------------------------------------------
t = T('Threats to biodiversity and conservation: protected areas, zoos, seed banks, IVF and the role of CITES', 'threats to biodiversity and conservation')
facts(t, [('endangered species', 'a species at risk of extinction because its numbers are low or falling'),
          ('CITES', 'the Convention on International Trade in Endangered Species: an international agreement that regulates or bans trade in endangered species and their products'),
          ('seed bank', 'a facility where seeds are dried and stored at low temperature to conserve the genetic diversity of plants'),
          ('captive breeding', 'the breeding of endangered animals in zoos to increase their numbers, often for later reintroduction'),
          ('alien (invasive) species', 'a species introduced to an area where it does not naturally occur, which may outcompete or prey on native species'),
          ('national park', 'a protected area in which human activities are restricted to conserve ecosystems and species'),
          ('frozen zoo', 'a store of frozen gametes and embryos used in assisted reproduction of endangered animals')])
mcqs(t, [('Which is the main reason that seeds are dried before storage in a seed bank?', 'To prevent germination and reduce damage to cells when frozen', 'Low water content and low temperature keep seeds viable for decades.', ['To kill any pathogens', 'To make them lighter to transport', 'To increase their mass']),
         ('Which is a role of CITES?', 'Regulating international trade in endangered species', 'Appendices list species with banned or controlled trade.', ['Funding all national parks', 'Running seed banks', 'Breeding animals in zoos']),
         ('Which technique allows a female of an endangered species to give birth to young of a related species?', 'Embryo transfer into a surrogate mother', 'IVF and embryo transfer use surrogates.', ['Artificial selection', 'Cloning by cuttings', 'Mark-release-recapture']),
         ('Why is the introduction of an alien species a threat to biodiversity?', 'It may outcompete, prey on or bring disease to native species that have no adaptations to it', 'e.g. cane toads, grey squirrels.', ['It always increases genetic diversity', 'It reduces the number of habitats', 'It decreases mutation rates'])])
shorts(t, [('State four threats to biodiversity.', 'Habitat loss/destruction (deforestation, agriculture); overexploitation (hunting, fishing); pollution; climate change; invasive alien species; disease.', 'any four [2]'),
           ('State two roles of modern zoos in conservation.', 'Captive breeding and reintroduction; education; research; maintaining genetic diversity (studbooks); frozen zoos.', 'any two [2]')])
explain(t, [('Explain why small populations of endangered species are at greater risk of extinction.', 'Low genetic diversity (founder effect, drift, inbreeding) reduces ability to adapt to change or disease; chance events can wipe out the population; inbreeding depression lowers fertility.', 'low genetic diversity [1]; inbreeding / drift [1]; vulnerable to disease / chance events [1] [3]'),
            ('Explain how assisted reproduction (IVF, embryo transfer, surrogacy) helps conservation.', 'Gametes/embryos can be frozen and transported instead of animals; more offspring from valuable females via superovulation; surrogate mothers of related species; increases genetic diversity by using unrelated donors.', 'freezing / transport of gametes [1]; more offspring [1]; surrogacy / genetic diversity [1] [3]'),
            ('Explain why it is important to preserve genetic diversity in seed banks as well as in protected areas.', 'Seed banks store many alleles (e.g. from wild relatives and landraces) safely ex situ; protection against loss of habitat; source of genes for future crop breeding and reintroduction.', 'store alleles / diversity [1]; insurance against loss [1]; future breeding [1] [3]'),
            ('Explain why controlling an invasive alien species can help conserve native species.', 'Removing the alien reduces competition, predation or disease affecting native species, so their populations can recover.', '[2]')])
myths(t, [('Keeping a few individuals of a species in a zoo is enough to save it from extinction.', 'Small captive populations lose genetic diversity; breeding programmes need many unrelated individuals and habitat protection for reintroduction.'),
          ('CITES protects endangered species by running national parks.', 'CITES is an international agreement that regulates trade in endangered species and their products.'),
          ('Seed banks can conserve all plant species.', 'Some seeds (recalcitrant seeds, e.g. many tropical trees) cannot survive drying and freezing, so they need other methods.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def decline(r, D):
    sp, lo, hi = r.choice([('African elephant', 600000, 1300000), ('Sumatran orangutan', 12000, 25000), ('black rhinoceros', 20000, 65000), ('snow leopard', 6000, 9000),
                           ('Bornean orangutan', 150000, 290000), ('hawksbill turtle (nesting females)', 30000, 60000), ('African wild dog', 9000, 20000), ('Asian elephant', 60000, 100000)])
    y0, y1 = r.choice([(1980, 2020), (1990, 2020), (1970, 2015), (1995, 2025)])
    n0 = round(r.uniform(lo, hi), -3)
    n0 = int(n0)
    n1 = round(n0 * r.uniform(0.1, 0.6), -2)
    dec = (n0 - n1) / n0 * 100
    if D == 1:
        return NQ(r, f'The population of the {sp} fell from {n0:,} in {y0} to {int(n1):,} in {y1}. What was the percentage decrease?', dec, [100 - dec, dec / 2, n1 / n0 * 10], '%', f'({n0:,} − {int(n1):,}) ÷ {n0:,} × 100 = {fx(dec, 1)}%.', f=lambda v: fx(v, 1))
    st = f'Surveys show that the population of the {sp} fell from {n0:,} in {y0} to {int(n1):,} in {y1}.'
    parts = [P_('Calculate the percentage decrease in the population.', f'{fx(dec, 1)}%', f'({n0:,} − {int(n1):,}) ÷ {n0:,} × 100 [1] = {fx(dec, 1)}% [1] [2]'),
             P_('Calculate the mean decrease in population per year.', f'{fx((n0 - n1) / (y1 - y0), 0)} per year', f'{int(n0 - n1):,} ÷ {y1 - y0} = {fx((n0 - n1) / (y1 - y0), 0)} [1]'),
             P_('Suggest two likely causes of this decline.', 'Habitat loss (deforestation, agriculture); poaching / illegal trade; climate change; pollution; by-catch.', 'any two relevant to the species [2]'),
             P_('Describe two ways in which the species could be conserved.', 'Protected areas / national parks with anti-poaching patrols; CITES trade ban; captive breeding and reintroduction; habitat restoration and corridors; education.', 'any two [2]')]
    if D >= 4:
        parts.append(P_('Explain why even if numbers recover, the species may still be at risk.', 'The bottleneck has reduced genetic diversity, so the population is less able to adapt to disease or environmental change; inbreeding depression.', 'reduced genetic diversity [1]; consequence [1] [2]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def cons_case(r, D):
    sp = r.choice([('the Arabian oryx', 'was extinct in the wild by 1972 but was bred in zoos and reintroduced to Oman and Saudi Arabia'),
                   ('the giant panda', 'lives in fragmented bamboo forests in China and breeds very slowly in captivity'),
                   ('the northern white rhinoceros', 'has only two surviving females, and frozen sperm and IVF embryos are being used with southern white rhino surrogates'),
                   ('the Wollemi pine', 'was discovered in 2000 with fewer than 100 trees in the wild; seeds and cuttings are now grown in botanic gardens and seed banks')])
    st = f'Conservationists are working to save {sp[0]}, which {sp[1]}.'
    parts = [P_('Explain the advantages of conserving a species in its natural habitat compared with in a zoo or botanic garden.', 'In situ: the whole ecosystem and its interactions are protected; natural behaviour and selection continue; larger populations; cheaper per individual.', 'ecosystem protected [1]; natural behaviour / selection [1]; larger population [1] [3]'),
             P_('Explain why captive breeding programmes keep studbooks of all individuals.', 'To choose breeding pairs that are not closely related, maximising genetic diversity and avoiding inbreeding depression.', '[2]'),
             P_('Discuss the problems of reintroducing captive-bred animals to the wild.', 'Lack of survival skills (hunting, predator avoidance); habitat may still be degraded; disease; low genetic diversity; local people\'s attitudes.', 'any three valid problems [3]'),
             P_('Explain the role of international agreements such as CITES in conserving this species.', 'Ban or regulate trade in the species and its products, reducing incentives for poaching or collection.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Discuss the threats to biodiversity and the methods used to conserve endangered species.', 'Threats: habitat loss, overexploitation, pollution, climate change, alien species. Conservation: protected areas (national parks, marine reserves), zoos and captive breeding, assisted reproduction (IVF, embryo transfer, surrogacy, frozen zoos), seed banks, botanic gardens, CITES, controlling alien species, restoring degraded habitats; problems: cost, genetic diversity, reintroduction.',
           'threats [2]; in situ methods [1]; zoos / captive breeding [1]; assisted reproduction [1]; seed banks [1]; CITES / alien control [1] [7]')])
t7c = t

CHAPTERS[7] = [t7a, t7b, t7c]


# ===================================================================== 8 Genetic technology
ENZ = [('EcoRI', 'GAATTC', 1, 'G^AATTC'), ('BamHI', 'GGATCC', 1, 'G^GATCC'), ('HindIII', 'AAGCTT', 1, 'A^AGCTT'), ('SmaI', 'CCCGGG', 3, 'CCC^GGG (blunt)')]

t = T('Principles of genetic technology: restriction enzymes, ligase, plasmids and recombinant DNA', 'principles of genetic technology')
facts(t, [('restriction enzyme', 'an endonuclease from bacteria that cuts DNA at a specific base sequence (restriction site), often leaving sticky ends'),
          ('sticky ends', 'short single-stranded overhangs left by staggered cuts, which can base-pair with complementary sticky ends'),
          ('DNA ligase', 'an enzyme that joins the sugar–phosphate backbones of DNA fragments by forming phosphodiester bonds'),
          ('plasmid', 'a small, circular, double-stranded DNA molecule in bacteria, used as a vector to carry genes into cells'),
          ('vector', 'a means of carrying a gene into a host cell, such as a plasmid or a virus'),
          ('recombinant DNA', 'DNA made by joining DNA from two different sources'),
          ('reverse transcriptase', 'an enzyme from retroviruses that makes cDNA from an mRNA template'),
          ('marker gene', 'a gene, such as one for fluorescence or antibiotic resistance, used to identify cells that have taken up a plasmid')])
mcqs(t, [('Why is the same restriction enzyme used to cut both the plasmid and the gene to be inserted?', 'To produce complementary sticky ends', 'Same enzyme → same overhangs.', ['To join the fragments together', 'To copy the gene', 'To make the gene express']),
         ('Which enzyme seals the sugar–phosphate backbone of the recombinant plasmid?', 'DNA ligase', 'Phosphodiester bonds formed.', ['DNA polymerase', 'Restriction enzyme', 'Reverse transcriptase']),
         ('Why is mRNA often used as a starting point for producing a human gene to put into bacteria?', 'It has no introns, so bacteria can express the gene', 'Bacteria cannot splice introns; reverse transcriptase makes cDNA.', ['It is double-stranded', 'It contains promoter sequences', 'It is more stable than DNA']),
         ('Which gene is commonly used as a marker in modern genetic engineering?', 'A gene for green fluorescent protein (GFP)', 'GFP fluoresces under UV; replaces antibiotic resistance markers.', ['A gene for insulin', 'A gene for DNA ligase', 'A gene for reverse transcriptase']),
         ('Why must a promoter be added with a gene inserted into a plasmid?', 'So that RNA polymerase can bind and transcribe the gene', 'Without a promoter the gene is not expressed.', ['To cut the plasmid', 'To join sticky ends', 'To make the plasmid replicate'])])
shorts(t, [('State three ways in which a gene can be obtained for genetic engineering.', 'Cut from DNA with restriction enzymes; made from mRNA using reverse transcriptase (cDNA); synthesised from a known sequence (gene machine); amplified by PCR.', 'any three [3]'),
           ('State two features of plasmids that make them suitable vectors.', 'Small; replicate independently in bacteria; have restriction sites; carry marker genes; easily taken up by bacteria.', 'any two [2]')])
explain(t, [('Describe how a recombinant plasmid containing the human insulin gene is produced and inserted into bacteria.', 'Obtain insulin mRNA from β cells, use reverse transcriptase to make cDNA, DNA polymerase for double strand; add promoter and sticky ends; cut plasmid with same restriction enzyme; mix, complementary sticky ends pair; DNA ligase seals; bacteria take up plasmids (heat shock with Ca²⁺ / electroporation); identify transformed bacteria with marker genes; culture in fermenters.', 'cDNA via reverse transcriptase [1]; same restriction enzyme / sticky ends [1]; ligase [1]; transformation [1]; marker selection [1] [5]'),
            ('Explain why marker genes are needed in genetic engineering.', 'Only a small proportion of cells take up the recombinant plasmid; markers (e.g. GFP or antibiotic resistance) allow those cells to be identified and selected.', 'few cells transformed [1]; markers identify / select them [1] [2]'),
            ('Explain why GFP is preferred to antibiotic resistance as a marker.', 'GFP is detected simply by fluorescence without killing cells; avoids spreading antibiotic resistance genes to pathogenic bacteria.', 'easy detection [1]; avoids spreading resistance [1] [2]'),
            ('Explain why the genetic code being universal is important for genetic engineering.', 'The same codons code for the same amino acids in all organisms, so a gene from one organism (e.g. human) is translated into the same protein in another (e.g. bacterium).', 'same codons in all organisms [1]; same protein made [1] [2]')])
myths(t, [('Restriction enzymes join DNA fragments together.', 'Restriction enzymes cut DNA at specific sequences; DNA ligase joins fragments.'),
          ('Human genes can be inserted into bacteria directly from chromosomes and will be expressed.', 'Human genes contain introns that bacteria cannot remove; cDNA from mRNA is used instead, with a bacterial promoter.'),
          ('Sticky ends are held together permanently by hydrogen bonds.', 'Hydrogen bonds between sticky ends are weak; DNA ligase forms phosphodiester bonds to join the backbones permanently.')])


def _site_seq(r, enzyme, nsites, L):
    name, site, cutpos, _ = enzyme
    while True:
        pos = sorted(r.sample(range(4, L - 10), nsites))
        if all(b - a > 8 for a, b in zip(pos, pos[1:])):
            break
    s = []
    i = 0
    for p in pos:
        while len(s) < p:
            s.append(r.choice('ACGT'))
        s.extend(site)
    while len(s) < L:
        s.append(r.choice('ACGT'))
    seq = ''.join(s)
    for e in ENZ:
        pass
    # ensure no accidental extra sites
    idx = [i for i in range(len(seq) - 5) if seq[i:i + 6] == site]
    return seq, idx


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def restriction(r, D):
    enz = r.choice(ENZ)
    name, site, cutpos, note = enz
    if D <= 2:
        circ = r.random() < 0.5
        n = r.choice([1, 2, 3, 4])
        frags = n if circ else n + 1
        return NQ(r, f'{"A circular plasmid" if circ else "A linear piece of DNA"} contains {n} recognition site{"s" if n > 1 else ""} for {name}. How many fragments are produced when it is cut completely?', frags, [frags + 1, max(1, frags - 1), 2 * n, frags + 2], '',
                  f'{"Circular: fragments = number of cuts" if circ else "Linear: fragments = cuts + 1"} = {frags}.', f=lambda v: str(int(v)))
    L = r.choice([40, 45, 50])
    nsites = r.choice([1, 2])
    seq, idx = _site_seq(r, enz, nsites, L)
    if len(idx) != nsites:
        return None
    cuts = [i + cutpos for i in idx]
    bounds = [0] + cuts + [L]
    sizes = [b - a for a, b in zip(bounds, bounds[1:])]
    st = f'{name} recognises the sequence {site} and cuts it {note}. The following single strand (5′→3′) of a linear double-stranded DNA molecule is to be cut: {seq}.'
    parts = [P_(f'State how many {name} sites are present and the lengths (in bases) of the fragments produced.', f'{nsites} site{"s" if nsites > 1 else ""}; fragments of {", ".join(map(str, sizes))} bases', f'sites located [1]; fragment lengths {", ".join(map(str, sizes))} [1] [2]'),
             P_('Explain why the recognition site is described as palindromic.', f'The sequence on one strand read 5′→3′ ({site}) is the same as the complementary strand read 5′→3′.', '[1]'),
             P_('Explain what is meant by sticky ends and why they are useful.' if cutpos != 3 else 'Explain why this enzyme produces blunt ends and why sticky ends are more useful for making recombinant DNA.',
                ('Staggered cuts leave short unpaired single-stranded overhangs; complementary overhangs from DNA cut with the same enzyme pair by hydrogen bonding, making joining easy.' if cutpos != 3 else 'It cuts both strands at the same point (straight across); sticky ends have overhangs that base-pair with complementary ends, so fragments join more efficiently.'), 'overhang / cut description [1]; complementary base pairing to join fragments [1] [2]'),
             P_('Explain why bacteria produce restriction enzymes.', 'To cut up the DNA of invading viruses (bacteriophages); their own DNA is protected by methylation.', 'destroy viral DNA [1]; own DNA protected [1] [2]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def insulin_case(r, D):
    prod = r.choice([('human insulin', 'β cells of the pancreas', 'diabetes'), ('human growth hormone', 'cells of the anterior pituitary', 'growth hormone deficiency'), ('factor VIII', 'liver cells', 'haemophilia'), ('erythropoietin', 'kidney cells', 'anaemia in kidney disease')])
    st = f'A company in {city(r)} produces {prod[0]} for treating {prod[2]} using genetically modified bacteria.'
    parts = [P_(f'Explain why mRNA is extracted from {prod[1]} rather than using the gene from chromosomal DNA.', 'These cells make the protein so contain many copies of its mRNA; mRNA has no introns, so the cDNA made from it can be expressed by bacteria.', 'abundant mRNA in these cells [1]; no introns [1]; bacteria cannot splice [1] [3]'),
             P_('Describe how the cDNA is inserted into a plasmid.', 'Cut plasmid with a restriction enzyme; add matching sticky ends to cDNA (or cut with same enzyme); mix so sticky ends pair; DNA ligase forms phosphodiester bonds; promoter included.', 'same restriction enzyme [1]; complementary sticky ends [1]; ligase [1] [3]'),
             P_('Describe how bacteria that have taken up the recombinant plasmid are identified.', 'The plasmid carries a marker gene such as GFP; colonies that fluoresce under UV light contain the plasmid; (or antibiotic resistance with replica plating).', 'marker gene [1]; detection method [1] [2]'),
             P_(f'Explain the advantages of producing {prod[0]} using genetically modified bacteria.', 'Identical to human protein so fewer immune reactions; large quantities quickly and cheaply in fermenters; no risk of infection from animal/human sources; no ethical issues of using animals.', 'any three [3]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe the principles of genetic engineering, using the production of human insulin by bacteria as an example.', 'Obtain gene: mRNA from β cells → reverse transcriptase → cDNA → double-stranded; restriction enzymes cut plasmid, sticky ends; ligase; promoter; marker gene (GFP); transformation (Ca²⁺ heat shock); select transformed bacteria; culture in fermenter; extract and purify insulin; universal genetic code.',
           'obtaining gene [2]; vector and restriction enzymes [1]; ligase [1]; transformation [1]; markers [1]; production / code [1] [7]')])
t8a = t

# ---------------------------------------------------------------------
t = T('PCR and gel electrophoresis', 'pcr and gel electrophoresis')
facts(t, [('PCR', 'the polymerase chain reaction: a method of making many copies of a specific DNA sequence by cycles of denaturation, annealing and extension'),
          ('primer', 'a short single-stranded DNA sequence complementary to the end of the target sequence, which allows DNA polymerase to start copying'),
          ('Taq polymerase', 'a heat-stable DNA polymerase from the bacterium Thermus aquaticus, used in PCR because it is not denatured at 95 °C'),
          ('gel electrophoresis', 'a technique that separates DNA fragments by size by moving them through an agarose gel in an electric field'),
          ('DNA profiling', 'the analysis of the lengths of variable repeated sequences (STRs/VNTRs) in DNA, giving a pattern of bands unique to an individual'),
          ('annealing', 'the binding of primers to complementary sequences on single-stranded DNA as the mixture cools to about 55–65 °C')])
mcqs(t, [('At what temperature is DNA denatured into single strands in PCR?', 'About 95 °C', 'Breaks hydrogen bonds between bases.', ['About 55 °C', 'About 72 °C', 'About 37 °C']),
         ('Why does DNA move towards the anode in gel electrophoresis?', 'DNA is negatively charged because of its phosphate groups', 'Phosphates carry negative charge.', ['DNA is positively charged', 'The gel pushes it', 'Small fragments carry more charge']),
         ('In gel electrophoresis, which fragments move furthest?', 'The smallest fragments', 'Small fragments move more easily through gel pores.', ['The largest fragments', 'Fragments with most G–C pairs', 'All fragments move the same distance']),
         ('Why is Taq polymerase used in PCR?', 'It is not denatured at the high temperatures used', 'From a thermophilic bacterium.', ['It works fastest at 37 °C', 'It cuts DNA at specific sites', 'It joins Okazaki fragments only']),
         ('What is the temperature for the extension stage of PCR?', 'About 72 °C', 'Optimum for Taq polymerase.', ['About 95 °C', 'About 55 °C', 'About 4 °C'])])
shorts(t, [('State the components needed in a PCR reaction mixture.', 'Template DNA; two primers; Taq polymerase; free nucleotides (dNTPs); buffer (with Mg²⁺).', 'any four [2]'),
           ('State two uses of DNA profiling.', 'Forensic identification of suspects; paternity testing; identifying remains; determining relationships for conservation / immigration; diagnosing genetic disorders.', 'any two [2]')])
explain(t, [('Describe the three stages of one PCR cycle.', 'Denaturation at 95 °C breaks hydrogen bonds, separating strands; annealing at about 55–65 °C allows primers to bind complementary sequences; extension at 72 °C, Taq polymerase adds nucleotides to the 3′ end of primers to make new strands.', 'denaturation [1]; annealing of primers [1]; extension by Taq [1] [3]'),
            ('Explain how gel electrophoresis separates DNA fragments.', 'DNA is loaded into wells at the cathode end; a current is applied; negatively charged DNA moves towards the anode; agarose gel acts as a sieve, smaller fragments moving faster and further; fragments separate by size; stained or labelled to show bands.', 'negative charge to anode [1]; gel as sieve [1]; small move further [1]; visualised [1] [4]'),
            ('Explain how DNA profiling can show whether a man is the biological father of a child.', 'Each band in the child\'s profile must come from either the mother or the father; bands in the child not present in the mother must match bands in the father; if they do not, he is not the father.', 'half bands from each parent [1]; non-maternal bands compared [1]; conclusion rule [1] [3]'),
            ('Explain why primers are needed in PCR.', 'DNA polymerase can only add nucleotides to an existing 3′ end; primers provide this and define which section of DNA is copied.', 'start point for polymerase [1]; specify target region [1] [2]')])
myths(t, [('In gel electrophoresis, large fragments move faster because they are heavier.', 'Small fragments move further because they pass through the gel pores more easily.'),
          ('PCR uses DNA ligase to join nucleotides.', 'PCR uses Taq DNA polymerase to join nucleotides to the primers; ligase is not used.'),
          ('DNA profiling compares the genes that code for proteins.', 'DNA profiling compares variable non-coding repeat sequences (STRs), which differ greatly between individuals.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def pcr_calc(r, D):
    n0 = r.choice([1, 2, 5, 10, 50, 100])
    cyc = r.choice([10, 15, 20, 25, 30])
    copies = n0 * 2 ** cyc
    tcyc = r.choice([2, 2.5, 3, 4])
    if D == 1:
        return NQ(r, f'A PCR reaction starts with {n0} molecule{"s" if n0 > 1 else ""} of double-stranded DNA. How many copies are present after {cyc} cycles, assuming each cycle doubles the DNA?', copies, [n0 * 2 * cyc, n0 * cyc ** 2, copies / 2, copies * 2], '',
                  f'{n0} × 2^{cyc} = {sci(copies, 3)}.', f=lambda v: sci(v, 3))
    p = person(r)
    st = f'{p} amplified a DNA sample from a crime scene in {city(r)}. The reaction started with {n0} copies of the target sequence and ran for {cyc} cycles, each lasting {fx(tcyc, 1)} minutes.'
    parts = [P_('Calculate the number of copies of the target sequence after all cycles, assuming 100% efficiency.', sci(copies, 3), f'{n0} × 2^{cyc} [1] = {sci(copies, 3)} [1] [2]'),
             P_('Calculate the total time taken.', f'{fx(cyc * tcyc, 1)} minutes', f'{cyc} × {fx(tcyc, 1)} = {fx(cyc * tcyc, 1)} min [1]'),
             P_('Suggest why the actual number of copies is lower than calculated.', 'Primers or nucleotides are used up; Taq polymerase gradually loses activity; not every strand is copied each cycle (efficiency below 100%).', 'any one valid reason [1]'),
             P_('Explain why the sample was amplified before DNA profiling.', 'Only a tiny amount of DNA was present; PCR makes enough copies for analysis by electrophoresis.', '[2]')]
    if D >= 4:
        parts.append(P_('Calculate how many cycles would be needed to obtain at least one million copies from one molecule.', '20 cycles', '2^19 = 524 288; 2^20 = 1 048 576 [1]; 20 cycles [1] [2]'))
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'short')
def profile_q(r, D):
    alleles = list(range(3, 20))
    mom = r.sample(alleles, 2)
    dad = r.sample([a for a in alleles if a not in mom], 2)
    child = [r.choice(mom), r.choice(dad)]
    other = r.sample([a for a in alleles if a not in mom and a not in dad], 2)
    men = [('Man 1', dad), ('Man 2', other)]
    r.shuffle(men)
    fath = [m for m, a in men if a is dad][0]
    st = (f'In a paternity case in {city(r)}, a single STR locus was analysed by gel electrophoresis. Band sizes (numbers of repeats): mother {sorted(mom)}; child {sorted(child)}; '
          + '; '.join(f'{m} {sorted(a)}' for m, a in men) + '. Determine which man could be the father. Explain your reasoning.')
    non_mat = [c for c in child if c not in mom] or child
    return Q(st, f'{fath}: the child\'s non-maternal band ({non_mat[0]} repeats) matches one of his bands; the other man has neither.', f'identifies maternal band [1]; non-maternal band matched to {fath} [1]; other man excluded [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def gel_case(r, D):
    dfun = lambda s_: 9.0 - 2.8 * math.log10(s_ / 100)  # noqa: E731
    sizes = sorted(r.sample([200, 500, 1000, 2000, 3000, 5000, 8000], 5), reverse=True)
    dists = [round(dfun(s_), 1) for s_ in sizes]
    cand = [u for u in (300, 400, 700, 1500, 2500, 4000, 6000) if sizes[-1] < u < sizes[0] and all(abs(math.log10(u / s_)) > 0.08 for s_ in sizes)]
    if not cand:
        return None
    unk = r.choice(cand)
    ud = round(dfun(unk), 1)
    st = (f'{person(r)} separated a DNA ladder and an unknown fragment by gel electrophoresis. Ladder fragments (base pairs) and distances moved (cm): ' + ', '.join(f'{s_} bp {fx(d, 1)} cm' for s_, d in zip(sizes, dists))
          + f'. The unknown fragment moved {fx(ud, 1)} cm.')
    parts = [P_('Estimate the size of the unknown fragment, explaining your method.', f'About {unk} bp: plot log(size) against distance for the ladder and read off the size at {fx(ud, 1)} cm.', f'calibration with ladder [1]; estimate in range {int(unk * 0.85)}–{int(unk * 1.15)} bp [1] [2]'),
             P_('Explain why the DNA fragments move through the gel.', 'DNA has negatively charged phosphate groups so moves towards the positive electrode (anode) when a voltage is applied.', '[2]'),
             P_('Explain why the fragments separate.', 'The gel acts as a mesh; smaller fragments move through it more easily and travel further in the same time.', '[2]'),
             P_('Describe how the bands are made visible.', 'Stain with a DNA dye (e.g. ethidium bromide / SYBR safe) and view under UV, or use radioactive or fluorescent probes.', '[1]'),
             P_('Explain why the voltage is switched off before the DNA reaches the end of the gel.', 'The smallest fragments would run off the gel into the buffer and be lost.', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Describe how PCR and gel electrophoresis are used to produce a DNA profile from a small sample, and explain how the profile is interpreted.', 'Extract DNA; PCR: primers for STR loci, Taq, nucleotides, 95/55/72 °C cycles, exponential copying; fluorescent primers; electrophoresis: wells, negative DNA to anode, gel sieve, small further; ladder; visualise; compare band positions; unique pattern; paternity: half bands from each parent; forensic matches.',
           'PCR stages [2]; components [1]; electrophoresis principle [2]; visualisation / ladder [1]; interpretation [1] [7]')])
t8b = t

# ---------------------------------------------------------------------
t = T('Microarrays, bioinformatics, gene therapy and genetic screening', 'microarrays, bioinformatics')
facts(t, [('microarray', 'a small glass slide or chip with thousands of different DNA probes fixed in a grid, used to detect which genes are present or expressed in a sample'),
          ('bioinformatics', 'the collection, storage and analysis of biological information, such as DNA and protein sequences, using computers and databases'),
          ('gene therapy', 'the insertion of a functional allele into a person\'s cells to treat a genetic disorder'),
          ('genetic screening', 'testing people\'s DNA for alleles that cause, or increase the risk of, genetic disorders'),
          ('somatic gene therapy', 'gene therapy in body cells, so the change is not passed to offspring'),
          ('germ-line gene therapy', 'gene therapy in gametes or early embryos, so the change is inherited; not permitted in humans in most countries')])
mcqs(t, [('What is detected when a spot on a microarray fluoresces brightly after hybridisation with labelled cDNA from a tissue?', 'The gene matching that probe is being expressed in the tissue', 'cDNA is made from the tissue\'s mRNA.', ['The gene is absent', 'The probe has been destroyed', 'The tissue has a mutation in that gene']),
         ('Which type of vector is most often used in gene therapy?', 'A modified (inactivated) virus', 'e.g. adeno-associated virus or lentivirus.', ['A bacterial plasmid in a bacterium', 'A restriction enzyme', 'A ribosome']),
         ('Why is gene therapy easier for recessive conditions than for dominant ones?', 'Adding a functional dominant allele masks the faulty recessive one', 'A dominant faulty allele would still be expressed.', ['Recessive alleles are not expressed at all', 'Viruses cannot carry dominant alleles', 'Dominant conditions are not genetic']),
         ('Which disease has been treated by gene therapy that inserts a functional allele into a patient\'s T cells or stem cells?', 'SCID (severe combined immunodeficiency)', 'ADA-SCID was among the first.', ['Influenza', 'Type 2 diabetes', 'Malaria'])])
shorts(t, [('State two uses of bioinformatics.', 'Comparing DNA/protein sequences between species; identifying genes and predicting protein structure; finding mutations; designing primers; tracking pathogen evolution (e.g. malaria parasite).', 'any two [2]'),
           ('Name two conditions for which embryos or adults may be screened.', 'Cystic fibrosis; Huntington\'s disease; sickle cell anaemia; thalassaemia; BRCA1/2 breast cancer alleles; Duchenne muscular dystrophy.', 'any two [2]')])
explain(t, [('Describe how a microarray is used to compare gene expression in cancer cells and normal cells.', 'Extract mRNA from both; make cDNA with reverse transcriptase; label with different fluorescent dyes; mix and apply to microarray; cDNA hybridises to complementary probes; scan; colour/intensity of each spot shows relative expression of each gene.', 'mRNA → cDNA [1]; different fluorescent labels [1]; hybridisation to probes [1]; scanning / colour interpretation [1] [4]'),
            ('Explain why gene therapy for cystic fibrosis has had limited success.', 'Viral vectors/liposomes do not reach enough lung epithelial cells; mucus blocks delivery; immune response to vector; epithelial cells are replaced so treatment must be repeated; inserted gene may be expressed only briefly.', 'delivery problems [1]; immune response [1]; cells replaced / repeat treatment [1] [3]'),
            ('Discuss the ethical issues of genetic screening of embryos.', 'Allows parents to avoid serious disease; but may lead to selection of embryos for non-medical traits ("designer babies"); destruction of embryos; discrimination against disabled people; who decides which conditions; cost.', 'benefit [1]; two issues [2] [3]'),
            ('Explain how bioinformatics has helped research into malaria.', 'The Plasmodium genome was sequenced and stored in databases; comparing sequences identifies genes for surface antigens and drug resistance; helps design vaccines and drugs.', 'genome sequenced / databases [1]; comparisons identify target genes [1]; vaccine / drug design [1] [3]')])
myths(t, [('Somatic gene therapy cures a genetic disorder for future generations.', 'Somatic gene therapy changes only body cells; the faulty allele can still be passed on in gametes.'),
          ('A microarray measures the amount of protein made by each gene.', 'A microarray detects DNA or mRNA (as cDNA) sequences that hybridise with probes, not proteins.'),
          ('Genetic screening changes a person\'s genes.', 'Screening only detects alleles; it does not change them.')])


@t.add('C3', (2, 3, 4, 5), 'case')
def microarray_q(r, D):
    genes = r.sample(['gene P', 'gene Q', 'gene R', 'gene S', 'gene T', 'gene U'], 4)
    cols = [r.choice(['red', 'green', 'yellow', 'black']) for _ in genes]
    if len(set(cols)) < 3:
        return None
    meaning = {'red': 'expressed only (or much more) in the cancer cells', 'green': 'expressed only (or much more) in the normal cells', 'yellow': 'expressed equally in both', 'black': 'not expressed in either'}
    st = (f'cDNA from cancer cells was labelled with a red fluorescent dye and cDNA from normal cells of the same tissue with a green dye. Both were mixed and applied to a microarray. The spots for four genes were: '
          + ', '.join(f'{g} {c}' for g, c in zip(genes, cols)) + '.')
    parts = [P_('State what each colour shows about the expression of each gene.', '; '.join(f'{g}: {meaning[c]}' for g, c in zip(genes, cols)), 'two correct [1]; all correct [1] [2]'),
             P_('Explain why cDNA was made from mRNA rather than using genomic DNA.', 'mRNA is present only for genes being expressed (transcribed); genomic DNA contains all genes whether expressed or not.', 'mRNA shows expression [1]; DNA has all genes [1] [2]'),
             P_('Suggest how this information could be used in treating cancer.', 'Genes over-expressed in cancer cells could be targets for drugs; patterns help classify tumour type and choose treatment.', '[2]'),
             P_('State why the two samples were labelled with different dyes.', 'So that the relative amount of cDNA from each sample binding to each spot can be distinguished on the same array.', '[1]'),
             P_('Explain how the cDNA binds to particular spots on the microarray.', 'Each spot contains many copies of a single-stranded probe; cDNA hybridises by complementary base pairing to its matching probe.', '[2]')]
    return case(r, st, parts, k=(2, 3))


@t.add('C3', (1, 2, 3, 4), 'short')
def therapy_apply(r, D):
    sc = r.choice([('SCID caused by a recessive allele for the enzyme ADA', 'insert a functional ADA allele into the patient\'s own bone marrow stem cells using a viral vector and return them', 'stem cells divide to give many T cells with the functional allele; effect can be long-lasting'),
                   ('cystic fibrosis caused by recessive CFTR alleles', 'deliver functional CFTR alleles to airway epithelial cells using liposomes or a modified virus in an aerosol', 'cells must be treated repeatedly because epithelial cells are replaced'),
                   ('Leber congenital amaurosis (an inherited form of blindness)', 'inject an adeno-associated virus carrying a functional allele into the retina', 'retinal cells do not divide, so the effect is long-lasting'),
                   ('Huntington\'s disease, caused by a dominant allele', 'adding a normal allele would not help; the faulty allele must be silenced (e.g. by RNA interference)', 'a dominant allele is expressed even when a normal allele is present')])
    dis, how, note = sc
    if D == 1:
        return MQ(r, f'Which approach is most suitable for gene therapy of {dis}?', cap(how), [cap(x[1]) for x in [('', 'insert the faulty allele into gametes'), ('', 'remove all copies of the gene from every cell'), ('', 'inject the normal protein directly into the nucleus')]], f'{cap(how)}; {note}.')
    return Q(f'Doctors in {city(r)} are considering gene therapy for a patient with {dis}. Suggest how gene therapy could be carried out and comment on its likely effectiveness.', f'{cap(how)}; {note}.', 'method: vector and target cells [2]; comment on effectiveness [1] [3]', 'short')


@t.add('C4', (2, 3, 4, 5), 'case')
def screen_case(r, D):
    dis = r.choice([('Huntington\'s disease', 'autosomal dominant', 'symptoms appear only in middle age and there is no cure'), ('cystic fibrosis', 'autosomal recessive', 'carriers are unaffected'),
                    ('BRCA1 breast cancer risk', 'dominant allele increasing risk', 'carriers can choose increased monitoring or preventive surgery'), ('β-thalassaemia', 'autosomal recessive', 'carrier screening is offered before marriage in some countries')])
    st = f'A couple in {city(r)} with a family history of {dis[0]} ({dis[1]}) are offered genetic screening; {dis[2]}.'
    parts = [P_('Describe how a person can be screened for a particular allele.', 'Take a sample of cells (blood / cheek swab); extract DNA; amplify the gene by PCR; use a labelled probe, microarray or sequencing to detect the allele.', 'DNA extracted [1]; PCR [1]; probe / sequencing [1] [3]'),
             P_('Discuss the advantages and disadvantages to the couple of being screened.', 'Advantages: informed decisions about having children (e.g. PGD/IVF), early treatment or monitoring. Disadvantages: anxiety; possible discrimination by insurers/employers; difficult decisions about termination; information about relatives.', 'advantage [1]; two disadvantages [2] [3]'),
             P_('Explain what is meant by pre-implantation genetic diagnosis (PGD).', 'Embryos produced by IVF are tested (one cell removed) for the allele; only unaffected embryos are implanted.', '[2]'),
             P_('Explain the role of a genetic counsellor.', 'Explains the risks and the meaning of test results, options available and supports the couple in making their own informed decision.', '[2]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Discuss the uses of microarrays, bioinformatics, gene therapy and genetic screening in medicine, and the ethical issues they raise.', 'Microarrays: gene expression profiles, diagnosis, identifying genes; bioinformatics: databases, sequence comparison, drug/vaccine design; gene therapy: viral vectors/liposomes, SCID, CF, somatic vs germ line, limitations; screening: carriers, PGD, prenatal; ethics: consent, discrimination, designer babies, embryo destruction, cost, access.',
           'microarrays [1]; bioinformatics [1]; gene therapy method [2]; screening [1]; ethics [2] [7]')])
t8c = t

# ---------------------------------------------------------------------
t = T('Genetic technology in agriculture: GM crops, Bt maize and herbicide resistance; ethics', 'genetic technology in agriculture')
facts(t, [('Bt maize', 'maize genetically modified with a gene from Bacillus thuringiensis that codes for a protein toxic to insect larvae such as corn borers'),
          ('herbicide-resistant crop', 'a crop modified with a gene, such as one for a glyphosate-resistant enzyme, so that it survives herbicide spraying'),
          ('Golden Rice', 'rice genetically modified to produce β-carotene (provitamin A) in its endosperm, to reduce vitamin A deficiency'),
          ('GMO', 'a genetically modified organism: one whose DNA has been altered using genetic technology'),
          ('superweed', 'a weed that has acquired herbicide resistance, for example by cross-pollination with a herbicide-resistant crop or by selection')])
mcqs(t, [('What does the gene inserted into Bt maize code for?', 'A protein that is toxic to some insect larvae', 'Cry protein from Bacillus thuringiensis.', ['A herbicide-resistant enzyme', 'β-carotene', 'A nitrogen-fixing enzyme']),
         ('What is a possible environmental risk of growing herbicide-resistant crops?', 'Transfer of the resistance gene to wild relatives by pollen, producing resistant weeds', 'Gene flow to related plants.', ['The crops will need more pesticide', 'The crop will become toxic to humans', 'The crop will stop photosynthesising']),
         ('Why can farmers use less insecticide when growing Bt crops?', 'The plants produce their own toxin that kills the target pests', 'Only insects that eat the crop are affected.', ['The plants repel all insects', 'Insects cannot land on them', 'Bt crops grow faster than insects can feed']),
         ('Why is β-carotene added to Golden Rice?', 'It is converted to vitamin A in the body', 'Reduces vitamin A deficiency and blindness.', ['It makes rice herbicide-resistant', 'It kills pests', 'It increases protein content'])])
shorts(t, [('State two advantages of growing herbicide-resistant crops.', 'Weeds can be killed by spraying without harming the crop; less competition so higher yield; fewer, broad-spectrum herbicide sprays; less ploughing / soil erosion.', 'any two [2]'),
           ('State two concerns about growing GM crops.', 'Gene flow to wild relatives (superweeds); resistance evolving in pests; harm to non-target insects; reduced biodiversity; monopoly of seed companies / cost to farmers; consumer concern about safety.', 'any two [2]')])
explain(t, [('Explain how insect pests could become resistant to Bt toxin and how farmers try to prevent this.', 'Random mutations give some insects resistance; Bt crops select for them, so resistance alleles increase; farmers plant refuges of non-Bt crops so susceptible insects survive and mate with resistant ones, diluting resistance alleles.', 'mutation and selection [1]; allele frequency increases [1]; refuges [1] [3]'),
            ('Discuss the social and economic issues of growing GM crops in developing countries.', 'Benefits: higher yields, less pesticide cost and exposure, improved nutrition (Golden Rice). Issues: high cost of seed each year; dependence on multinational companies; patents; small farmers may be unable to compete; consumer acceptance and export restrictions.', 'benefit [1]; two issues [2] [3]'),
            ('Explain how a crop can be made resistant to the herbicide glyphosate.', 'Glyphosate inhibits an enzyme (EPSPS) needed to make some amino acids; a gene for a bacterial version of the enzyme that is not inhibited is inserted (with a promoter) into the crop, so the crop makes amino acids even when sprayed.', 'glyphosate inhibits enzyme [1]; resistant gene from bacterium inserted [1]; plant survives spraying [1] [3]')])
myths(t, [('Eating GM food will transfer the inserted genes into human cells.', 'DNA in food is digested in the gut; there is no evidence that genes from GM food enter human cells.'),
          ('Bt maize kills all insects that land on it.', 'The Bt protein is toxic only to certain insects (e.g. some caterpillars) that eat the plant tissue.'),
          ('Herbicide-resistant crops are resistant to all herbicides.', 'They are resistant only to the specific herbicide for which the resistance gene was inserted, such as glyphosate.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def gm_data(r, D):
    y_c = round(r.uniform(5.0, 8.0), 1)
    y_g = round(y_c * r.uniform(1.05, 1.3), 1)
    ins_c = r.choice([3, 4, 5, 6])
    ins_g = r.choice([0, 1, 2])
    crop = r.choice(['Bt maize', 'Bt cotton', 'Bt brinjal'])
    unit = 't ha⁻¹'
    inc = pct(y_c, y_g)
    if D == 1:
        return NQ(r, f'In a trial, non-GM maize yielded {fx(y_c, 1)} {unit} and {crop} yielded {fx(y_g, 1)} {unit}. What was the percentage increase in yield?', inc, [inc / 10, y_g - y_c, 100 - inc], '%', f'({fx(y_g, 1)} − {fx(y_c, 1)}) ÷ {fx(y_c, 1)} × 100 = {fx(inc, 1)}%.', f=lambda v: fx(v, 1))
    st = (f'In field trials near {city(r)}, conventional plants yielded a mean of {fx(y_c, 1)} {unit} and needed {ins_c} insecticide sprays per season, while {crop} yielded {fx(y_g, 1)} {unit} and needed {ins_g} spray{"" if ins_g == 1 else "s"}.')
    parts = [P_('Calculate the percentage increase in yield of the GM crop.', f'{fx(inc, 1)}%', f'({fx(y_g, 1)} − {fx(y_c, 1)}) ÷ {fx(y_c, 1)} × 100 [1] = {fx(inc, 1)}% [1] [2]'),
             P_('Explain the higher yield and the reduced number of sprays.', 'The plants make Bt toxin, killing larvae that eat them, so less damage and more photosynthetic tissue; insecticide is only needed for pests not affected by Bt.', 'toxin kills feeding larvae [1]; less damage [1]; fewer sprays [1] [3]'),
             P_('Suggest two environmental benefits of using fewer insecticide sprays.', 'Less harm to non-target insects (pollinators, predators); less pollution of water; less fuel used; less exposure of farm workers.', 'any two [2]'),
             P_('Suggest why the trial should be repeated over several years and sites.', 'Pest numbers and weather vary between years and places; repeats make results more reliable and representative.', '[2]')]
    return case(r, st, parts, k=(2, 3) if D <= 3 else (3, 4), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'case')
def gm_case(r, D):
    crop = r.choice(['Golden Rice', 'herbicide-resistant soya', 'Bt cotton', 'drought-tolerant maize'])
    st = f'A government agency in {city(r)} is deciding whether to allow farmers to grow {crop}.'
    parts = [P_(f'Discuss the arguments for and against allowing farmers to grow {crop}.', 'For: higher yields, less pesticide/herbicide use or better nutrition, food security. Against: gene flow to wild relatives, resistance in pests/weeds, effects on non-target species and biodiversity, seed cost and dependence on companies, consumer opposition, labelling.', 'two arguments for [2]; two arguments against [2] [4]'),
             P_('Explain why GM crops must be tested before being approved.', 'To check that the new protein is not toxic or allergenic to humans or animals and to assess environmental effects such as gene flow.', '[2]'),
             P_('Describe how a gene can be inserted into a plant cell.', 'Use Agrobacterium tumefaciens with a modified Ti plasmid carrying the gene, or a gene gun to shoot DNA-coated gold particles; grow whole plants from transformed cells by tissue culture.', 'vector / method [1]; regeneration from transformed cells [1] [2]'),
             P_('Suggest one way to reduce the risk of the inserted gene spreading to wild plants.', 'Plant buffer zones; grow where no wild relatives occur; use male-sterile varieties; insert gene into chloroplast DNA (not in pollen).', '[1]')]
    return case(r, st, parts, k=(2, 3, 4))


longs(t, [('Discuss the benefits and risks of genetically modified crops, with reference to Bt maize and herbicide-resistant crops.', 'Bt maize: Cry toxin gene, kills corn borer larvae, higher yield, less insecticide, but resistance evolves (refuges), non-target effects. Herbicide-resistant: glyphosate-resistant EPSPS, weed control without harming crop, but superweeds, more herbicide use, reduced weed biodiversity. Social/economic: seed cost, patents, consumer acceptance; Golden Rice nutrition.',
           'Bt mechanism and benefits [2]; herbicide resistance mechanism and benefits [2]; environmental risks [2]; social / ethical issues [1] [7]')])
t8d = t

CHAPTERS[8] = [t8a, t8b, t8c, t8d]


# ===================================================================== Paper 1-style application MCQs (C2, 1 mark)
P1 = [
    (t1d, [('Germinating seeds give out 8.4 cm³ CO₂ while taking in 12.0 cm³ O₂. Which substrate are they most likely respiring?', 'Lipid', 'RQ = 8.4 ÷ 12.0 = 0.70.', ['Carbohydrate', 'Protein', 'Carbohydrate, partly anaerobically']),
           ('Yeast in a sealed flask gives an RQ that rises from 1.0 to 3.5 over several hours. What is the best explanation?', 'Oxygen is running out so more anaerobic respiration takes place', 'CO₂ produced without O₂ uptake.', ['The yeast has switched to respiring lipid', 'The yeast has begun to photosynthesise', 'Lactate is being produced'])]),
    (t1e, [('In a respirometer without KOH, the fluid does not move while germinating peas respire. What does this suggest?', 'The volume of CO₂ released equals the volume of O₂ absorbed', 'RQ = 1, carbohydrate substrate.', ['The peas are not respiring', 'The peas are respiring lipid only', 'The capillary tube is blocked']),
           ('Methylene blue decolourises more slowly when yeast is kept at 5 °C than at 30 °C. Why?', 'Dehydrogenase enzymes work more slowly at the lower temperature', 'Less kinetic energy, fewer collisions.', ['Methylene blue is denatured at 5 °C', 'Yeast cells burst at 5 °C', 'More oxygen dissolves at 5 °C and reduces the dye'])]),
    (t2c, [('A suspension of Chlorella is moved from light to darkness. Which change occurs in the first minute?', 'GP concentration rises and RuBP concentration falls', 'GP no longer reduced; RuBP no longer regenerated.', ['GP falls and RuBP rises', 'Both GP and RuBP rise', 'Both GP and RuBP fall']),
           ('How many turns of the Calvin cycle are needed to make one molecule of glucose?', '6', 'One CO₂ fixed per turn; glucose has six carbons.', ['1', '3', '12'])]),
    (t2d, [('On a graph of rate of photosynthesis against light intensity, the curves at 0.04% and 0.1% CO₂ are identical at low light. Why?', 'Light intensity is the limiting factor at low intensities', 'CO₂ has no effect while light limits.', ['Carbon dioxide is limiting at low light', 'Temperature is limiting at low light', 'Photosynthesis does not occur at low light']),
           ('A lamp is moved from 20 cm to 10 cm from a pondweed. By what factor does light intensity increase?', '4', '(20/10)² = 4.', ['2', '8', '0.5'])]),
    (t3a, [('A person\'s core temperature rises to 38.5 °C. Which response would occur?', 'Vasodilation of arterioles supplying skin capillaries', 'Increases heat loss by radiation.', ['Shivering', 'Contraction of hair erector muscles', 'Vasoconstriction in the skin']),
           ('Which describes positive feedback?', 'A change triggers a response that increases the change further', 'e.g. oxytocin in childbirth.', ['A change triggers a response that reverses it', 'A factor remains at its set point', 'A receptor stops responding'])]),
    (t3b, [('The concentration of glucose in the filtrate in the Bowman\'s capsule is 5 mmol dm⁻³. What is its concentration in the filtrate at the end of the PCT in a healthy person?', '0 mmol dm⁻³', 'All glucose is reabsorbed in the PCT.', ['5 mmol dm⁻³', '10 mmol dm⁻³', '2.5 mmol dm⁻³']),
           ('A person has damage to the basement membranes of the glomeruli. What is likely to be found in the urine?', 'Protein', 'Large molecules pass the damaged filter.', ['Glucose', 'Less urea than normal', 'No water'])]),
    (t3c, [('After a long run on a hot day, which combination is expected?', 'High ADH, small volume of concentrated urine', 'Water lost as sweat lowers blood water potential.', ['Low ADH, large volume of dilute urine', 'High ADH, large volume of dilute urine', 'Low ADH, small volume of concentrated urine']),
           ('Alcohol inhibits ADH release. What is the effect of drinking alcohol on urine?', 'A larger volume of more dilute urine is produced', 'Fewer aquaporins in collecting ducts.', ['A smaller volume of more concentrated urine', 'Glucose appears in urine', 'No change in urine'])]),
    (t3e, [('Epidermal strips are placed in a solution containing ABA in bright light. What happens to the guard cells?', 'They lose K⁺ and water and the stomata close', 'ABA triggers Ca²⁺ signalling and K⁺ efflux.', ['They gain K⁺ and the stomata open', 'They burst', 'They begin photosynthesising faster']),
           ('Why do stomata usually open in the light?', 'Proton pumping leads to K⁺ uptake, lowering the water potential of guard cells', 'Water enters by osmosis; turgid cells open the pore.', ['Light heats the guard cells so they expand', 'Light breaks down ABA in the roots', 'Light causes guard cells to lose water'])]),
    (t4a, [('A blood test shows high progesterone and low FSH on day 21 of a cycle. What does this indicate?', 'An active corpus luteum is inhibiting FSH secretion', 'Progesterone negative feedback.', ['Ovulation is about to occur', 'Menstruation is taking place', 'The follicle is still developing']),
           ('Which hormone surge is detected by an ovulation test kit?', 'LH', 'LH surge precedes ovulation by about 24–36 h.', ['FSH', 'Progesterone', 'hCG'])]),
    (t4b, [('A neurone has a refractory period of 2 ms. What is the maximum frequency of impulses it can carry?', '500 Hz', '1 ÷ 0.002 s = 500 per second.', ['50 Hz', '2000 Hz', '200 Hz']),
           ('A drug opens extra potassium channels in a neurone membrane at rest. What is the likely effect?', 'The membrane becomes hyperpolarised so action potentials are harder to produce', 'More K⁺ leaves, inside more negative.', ['The neurone fires more often', 'The resting potential becomes positive', 'Sodium channels stay open'])]),
    (t4c, [('Calcium ions are removed from the tissue fluid around a presynaptic knob. What is the effect?', 'Acetylcholine is not released', 'Ca²⁺ entry triggers exocytosis.', ['Acetylcholine is released continuously', 'The postsynaptic membrane is hyperpolarised', 'Acetylcholinesterase is inhibited']),
           ('Why does repeated stimulation of a synapse at high frequency eventually fail to produce postsynaptic action potentials?', 'Vesicles of neurotransmitter are used up faster than they are replaced', 'Synaptic fatigue.', ['Calcium channels are destroyed', 'The synaptic cleft closes', 'Receptors move to the presynaptic membrane'])]),
    (t4d, [('A sarcomere contracts from 2.8 μm to 2.2 μm. Which band stays the same width?', 'A band', 'Myosin filaments do not shorten.', ['I band', 'H zone', 'Z line spacing']),
           ('Which event directly causes the myosin head to detach from actin?', 'ATP binding to the myosin head', 'ATP binding reduces affinity for actin.', ['Calcium ions binding to troponin', 'ADP being released', 'Tropomyosin covering binding sites'])]),
    (t4e, [('Gibberellin is applied to a dwarf pea variety. What is the expected result?', 'The stems elongate to normal height', 'Dwarf varieties lack active gibberellin.', ['The plant becomes shorter', 'Seeds stop germinating', 'Leaves lose chlorophyll']),
           ('Coleoptile sections grow faster in a buffer at pH 5 than at pH 7 with no auxin. What does this support?', 'The acid growth hypothesis', 'Low pH activates expansins.', ['Auxin is destroyed at low pH', 'Gibberellin causes elongation', 'Cell division is stimulated by alkaline pH'])]),
    (t5a, [('A cell has 12 chromosomes in G1 of the cell cycle. How many chromosomes are in each cell at the end of meiosis II?', '6', 'Haploid number.', ['12', '24', '3']),
           ('Which process during meiosis separates alleles of two genes on the same chromosome?', 'Crossing over between non-sister chromatids', 'Linked alleles can be separated only by crossing over.', ['Independent assortment', 'Separation of sister chromatids', 'Cytokinesis'])]),
    (t5b, [('A woman who is a carrier of haemophilia has children with a man without haemophilia. What proportion of their daughters are expected to have haemophilia?', '0', 'Daughters receive the father\'s Xᴴ.', ['1/4', '1/2', '1']),
           ('Two pea plants heterozygous for seed shape are crossed. What fraction of the round-seeded offspring are expected to be heterozygous?', '2/3', 'Of 3 round, 2 are Rr.', ['1/2', '1/4', '3/4'])]),
    (t5c, [('In a test cross of a double heterozygote, 45% of offspring are each of two parental types and 5% each of two recombinant types. What is the recombination frequency?', '10%', '5 + 5 = 10%.', ['5%', '45%', '90%']),
           ('A χ² value of 9.2 is obtained with 3 degrees of freedom (critical value 7.82). What is concluded?', 'The difference is significant, so the null hypothesis is rejected', '9.2 > 7.82.', ['The difference is due to chance', 'The null hypothesis is accepted', 'The test is invalid with 3 degrees of freedom'])]),
    (t5d, [('An E. coli strain makes β-galactosidase even when no lactose is present. Which mutation could cause this?', 'A mutation in the operator so the repressor cannot bind', 'Constitutive expression.', ['A mutation in the promoter so RNA polymerase cannot bind', 'A mutation in lacZ', 'A mutation so the repressor binds lactose more tightly']),
           ('A barley mutant cannot break down DELLA proteins. What happens when it is treated with gibberellin?', 'Amylase is not produced in the aleurone layer', 'DELLA continues to inhibit the transcription factor.', ['Amylase production increases', 'Starch is broken down faster', 'The seed germinates sooner'])]),
    (t6a, [('Which characteristic shows continuous variation?', 'Leaf length in a population of oak trees', 'Range of values, polygenic.', ['ABO blood group', 'Presence or absence of horns in cattle', 'Sex in mammals']),
           ('A t-test gives t = 1.85 with a critical value of 2.10 at p = 0.05. What should be concluded?', 'There is no significant difference between the means', '1.85 < 2.10.', ['The means are significantly different', 'The null hypothesis is rejected', 'The data are normally distributed'])]),
    (t6b, [('In a population, 16% show a recessive phenotype. What is the frequency of the dominant allele?', '0.6', 'q² = 0.16, q = 0.4, p = 0.6.', ['0.4', '0.84', '0.16']),
           ('After a flood kills most of a small population at random, allele frequencies change. What is this an example of?', 'Genetic drift (a bottleneck)', 'Random change, not selection.', ['Directional selection', 'Stabilising selection', 'Artificial selection'])]),
    (t6c, [('Why do breeders cross two different inbred lines of maize?', 'To produce uniform F1 plants showing hybrid vigour', 'Heterozygous F1 are vigorous and uniform.', ['To produce homozygous plants', 'To reduce yield variation in the F2', 'To introduce new mutations']),
           ('Which is a disadvantage of intensive selective breeding of dairy cattle?', 'Loss of genetic diversity in the breed', 'Few bulls used widely.', ['Increased genetic diversity', 'Lower milk yields', 'More alleles in the gene pool'])]),
    (t6d, [('A diploid plant species (2n = 14) and a related species (2n = 18) form a sterile hybrid whose chromosome number doubles. How many chromosomes does the new fertile species have?', '32', '7 + 9 = 16, doubled = 32.', ['16', '28', '36']),
           ('Two populations of frogs in the same pond breed at different times of year. What type of isolation is this?', 'Temporal isolation', 'Prezygotic.', ['Geographical isolation', 'Hybrid sterility', 'Mechanical isolation'])]),
    (t7a, [('An organism has 70S ribosomes, no nucleus and cell membranes containing ether-linked lipids. In which domain is it classified?', 'Archaea', 'Ether-linked lipids are characteristic of Archaea.', ['Bacteria', 'Eukarya', 'Protoctista']),
           ('A single-celled organism has a nucleus, chloroplasts and no cell wall. In which kingdom is it placed?', 'Protoctista', 'Eukaryotic, not plant/animal/fungus.', ['Plantae', 'Fungi', 'Bacteria'])]),
    (t7b, [('Two meadows each contain the same five species. Meadow X has a higher Simpson\'s index than meadow Y. What does this show?', 'Individuals in X are spread more evenly among the species', 'Same richness; higher evenness.', ['X has more species than Y', 'X has fewer individuals than Y', 'Y has a dominant species absent from X']),
           ('30 snails are marked and released; later 40 are caught, of which 6 are marked. What is the estimated population?', '200', '30 × 40 ÷ 6 = 200.', ['76', '180', '1200'])]),
    (t7c, [('Why are frozen embryos used in captive breeding programmes?', 'They can be stored and transported easily to increase genetic diversity in other populations', 'Frozen zoo.', ['They always develop into twins', 'They increase inbreeding', 'They avoid the need for surrogate mothers']),
           ('Which threat to biodiversity does CITES aim to reduce?', 'Overexploitation through international trade', 'Trade in endangered species.', ['Climate change', 'Habitat loss from farming', 'Pollution of rivers'])]),
    (t8a, [('A plasmid with one EcoRI site is cut with EcoRI. How many fragments are produced?', '1', 'A circular plasmid cut once gives one linear fragment.', ['2', '0', '3']),
           ('Why must bacteria be treated with calcium ions and a heat shock?', 'To make their membranes more permeable so they take up plasmids', 'Transformation.', ['To kill the bacteria', 'To cut the plasmid', 'To activate the marker gene'])]),
    (t8b, [('A PCR starts with one DNA molecule. How many molecules are present after 5 cycles?', '32', '2⁵ = 32.', ['10', '25', '64']),
           ('In a DNA profile, a child has a band not present in the mother. Where must this band come from?', 'The biological father', 'Each band is inherited from one parent.', ['A mutation in the child', 'The mother\'s other chromosome', 'Either grandparent but not the father'])]),
    (t8c, [('A microarray spot glows green when cDNA from normal cells is green-labelled and cDNA from tumour cells is red-labelled. What does this show?', 'The gene is expressed in normal cells but not (or much less) in tumour cells', 'Green = normal only.', ['The gene is expressed only in tumour cells', 'The gene is expressed equally in both', 'The gene is absent from the genome']),
           ('Why does somatic gene therapy for cystic fibrosis need to be repeated?', 'The treated airway epithelial cells are regularly replaced', 'New cells lack the inserted allele.', ['The CFTR allele is dominant', 'The vector integrates into gametes', 'The patient makes antibodies against CFTR protein'])]),
    (t8d, [('Why do farmers growing Bt crops plant refuges of non-Bt crops nearby?', 'To slow the evolution of Bt resistance in pests', 'Susceptible insects mate with resistant ones.', ['To increase the yield of the Bt crop', 'To attract pollinators', 'To provide a source of Bt protein']),
           ('Glyphosate-resistant soya is sprayed with glyphosate. What happens?', 'Weeds die but the soya survives', 'Resistant EPSPS enzyme.', ['Both weeds and soya die', 'Neither weeds nor soya are affected', 'The soya grows more slowly than the weeds'])]),
]
for _t, _e in P1:
    mcqs(_t, _e, D=(1, 2, 3), C='C2')


# ===================================================================== finalise: marking-key enrichment (shared with g11_biology)
for _tps in CHAPTERS.values():
    for _t in _tps:
        for _tp in _t.templates:
            _tp.fn = _bio_wrap(_tp.fn)
        # no auto-paired two-part items: their 4-6 marks would land in 1-mark mock slots and unbalance mock totals
        _t.entries = {}
