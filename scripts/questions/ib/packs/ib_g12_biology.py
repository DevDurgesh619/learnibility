"""IB DP Biology SL/HL (first assessment 2025), DP year 2 – ib-g12-biology.

Themes C (interaction and interdependence: enzymes, respiration, photosynthesis, signalling, neural signalling,
integration, defence, populations, energy and matter) and D (continuity and change: replication, protein
synthesis, mutation, cell division, gene expression, water potential, reproduction, inheritance, homeostasis,
natural selection, stability, climate change), plus Internal Assessment skills.

Data-based items are parametric and compute their answers (enzyme rates, Rf values, respiratory quotients,
conduction velocity, Lincoln index, chi-squared tests, energy-transfer efficiency, PCR and Meselson–Stahl
calculations, translation with the standard genetic code, mitotic index, water potential, genetic crosses,
recombination frequency, Hardy–Weinberg, standard deviation, t-tests and correlation). Mocks mirror HL
Paper 1 (1A + 1B) and Paper 2 (Sections A and B): see ib_biology_common.MOCK.
"""
from __future__ import annotations

import itertools
import math
from fractions import Fraction

from _common import mcq, name, two_names, sup, CITIES  # noqa: F401
from ib_biology_common import (CONFIG, MOCK, Registry, T, CHI_CRIT, T_CRIT, chi_assoc, chi_gof, data_q, dp,  # noqa: F401
                               interp_zero, make_templates, mean, mean_sd_items, nmcq, num, pct_change, pct_items,
                               pearson, pick, pooled_t, sd, sf, signed, simpson, table, topic)

R = Registry()
templates = make_templates(R)


def init(subject_id):
    pass


def S(key, **kw):
    topic(R, key, **kw)


BASES = 'UCAG'
AA = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
CODON = {a + b + c: AA[16 * i + 4 * j + k] for i, a in enumerate(BASES) for j, b in enumerate(BASES) for k, c in enumerate(BASES)}
AA3 = {'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys', 'Q': 'Gln', 'E': 'Glu', 'G': 'Gly', 'H': 'His', 'I': 'Ile',
       'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro', 'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val', '*': 'STOP'}
DCOMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}


def translate(mrna):
    out = []
    for i in range(0, len(mrna) - 2, 3):
        a = CODON[mrna[i:i + 3]]
        out.append(AA3[a])
        if a == '*':
            break
    return out


def rand_orf(rng, n_codons):
    """Random mRNA starting AUG, no internal stop, ending with a stop codon."""
    sense = [c for c, a in CODON.items() if a != '*' and c != 'AUG']
    stops = ['UAA', 'UAG', 'UGA']
    return 'AUG' + ''.join(rng.choice(sense) for _ in range(n_codons - 2)) + rng.choice(stops)


# =============================================================================================
# ch01 C1.1 Enzymes and metabolism
# =============================================================================================
S('ch01-st1',
  terms=[('enzyme', 'a globular protein that acts as a biological catalyst, speeding up a specific reaction without being used up'),
         ('active site', 'the region of an enzyme, formed by a few amino acids, to which the substrate binds and where catalysis occurs'),
         ('metabolism', 'the complex network of interdependent and interacting chemical reactions occurring in living organisms'),
         ('induced-fit model', 'the model in which the active site changes shape slightly as the substrate binds, so that the two fit together closely and bonds in the substrate are strained'),
         ('enzyme–substrate specificity', 'the property that each enzyme catalyses only one reaction or a small group of reactions because only substrates with a complementary shape and chemistry bind to the active site'),
         ('anabolism', 'metabolic reactions that build larger molecules from smaller ones, such as protein synthesis'),
         ('catabolism', 'metabolic reactions that break down larger molecules into smaller ones, such as digestion and respiration')],
  facts=[('Which part of an enzyme determines its specificity?', 'the shape and chemical properties of the active site', ['the total number of amino acids', 'the length of the polypeptide chain only', 'the peptide bonds'], 'Only complementary substrates bind.'),
         ('Which statement about enzymes is correct?', 'they are unchanged at the end of the reaction', ['they are used up in the reaction', 'they raise the activation energy', 'they work equally well at all temperatures'], 'Catalysts are regenerated.'),
         ('Which is an example of an anabolic reaction?', 'synthesis of glycogen from glucose', ['digestion of starch', 'glycolysis', 'hydrolysis of proteins'], 'Anabolism builds macromolecules.'),
         ('Which is an example of a catabolic reaction?', 'hydrolysis of a polypeptide into amino acids', ['DNA replication', 'photosynthesis', 'protein synthesis'], 'Catabolism breaks down molecules.'),
         ('Why must molecules collide for an enzyme-catalysed reaction to occur?', 'the substrate must enter the active site with the correct orientation', ['enzymes only work in solids', 'collisions destroy the enzyme', 'collisions make new enzymes'], 'Movement of substrate (and enzyme) brings them together.')],
  mc2=[('Which observation best supports the induced-fit model rather than the lock-and-key model?', 'X-ray structures show the active site changing shape when the substrate binds.', ['Enzymes are proteins.', 'Enzymes are denatured at high temperature.', 'Enzymes are specific.'], 'Hexokinase closes around glucose.'),
       ('Why can an enzyme catalyse only a specific reaction?', 'Only a substrate with a complementary shape and chemistry can bind to the active site.', ['Enzymes are made of only one amino acid.', 'All substrates have the same shape.', 'Enzymes form covalent bonds with every molecule.'], 'Specificity arises from the 3D structure.'),
       ('Why are enzymes in solution more effective than enzymes immobilised in a solid?', 'Both enzyme and substrate move freely, giving more frequent collisions.', ['Immobilised enzymes are denatured.', 'Enzymes in solution have more active sites.', 'Immobilised enzymes cannot bind substrates.'], 'Immobilisation restricts enzyme movement but allows reuse.'),
       ('Why is metabolism described as a web of interdependent reactions?', 'The product of one reaction is often the substrate of another, linking pathways.', ['All reactions use the same enzyme.', 'Reactions occur only one at a time.', 'Reactions do not share substrates.'], 'Pathways branch and connect.')],
  mc3=[('Lactase is used to make lactose-free milk. It is immobilised on beads in a column through which milk flows. What is an advantage of this method?', 'The enzyme can be reused and does not contaminate the product.', ['The enzyme works faster than in solution.', 'The enzyme is no longer specific.', 'The milk does not need to touch the enzyme.'], 'Immobilisation allows reuse and easy separation.'),
       ('A mutation changes an amino acid far from the active site, yet enzyme activity is lost. What is the best explanation?', 'The change altered the tertiary structure, changing the shape of the active site.', ['The substrate binds to that amino acid.', 'Peptide bonds were broken.', 'The enzyme became more specific.'], 'Folding links distant residues to the active site.'),
       ('Two enzymes act on the same substrate but give different products. What does this show?', 'Each active site binds the substrate in a different way, catalysing a different reaction.', ['Enzymes are not specific.', 'The substrate changes shape spontaneously.', 'Products determine the enzyme.'], 'Specificity is for the reaction, not just the substrate.')],
  why=[('Explain the induced-fit model of enzyme action.', 'The active site is not exactly complementary to the substrate; as the substrate binds, the enzyme (and substrate) change shape slightly so they fit closely; this strains bonds in the substrate, lowering the activation energy and promoting the reaction; products are then released and the active site returns to its original shape.'),
       ('Explain why enzymes are described as specific.', 'The active site has a particular 3D shape and chemical properties (charges, hydrophobic/hydrophilic groups) determined by the tertiary structure; only substrates with a complementary shape and chemistry can bind, so each enzyme catalyses one reaction or a group of similar reactions.'),
       ('Explain why molecular motion and collisions are needed for enzyme catalysis.', 'The substrate must reach the active site; random motion of substrate molecules (and enzyme) in solution causes collisions; only collisions with the correct orientation and sufficient energy lead to binding and reaction; more collisions per second give a higher rate.'),
       ('Explain the relationship between the structure of an enzyme and its function.', 'The primary sequence determines folding into a specific tertiary structure; this creates an active site of particular shape and chemistry; specific substrates bind and catalysis occurs; altering the structure (mutation, denaturation) changes the active site and reduces activity.')],
  contrast=[('the lock-and-key model', 'the induced-fit model', 'In the lock-and-key model the active site is rigid and exactly complementary to the substrate; in the induced-fit model the active site changes shape on binding to fit the substrate closely and strain its bonds.'),
            ('anabolic reactions', 'catabolic reactions', 'Anabolic reactions synthesise complex molecules from simpler ones and require energy (e.g. protein synthesis); catabolic reactions break complex molecules into simpler ones and release energy (e.g. respiration, digestion).'),
            ('intracellular enzymes', 'extracellular enzymes', 'Intracellular enzymes act inside the cell where they are made (e.g. glycolytic enzymes); extracellular enzymes are secreted and act outside the cell (e.g. digestive enzymes in the gut).')],
  misc=[('Enzymes are used up in the reactions they catalyse.', 'Enzymes are catalysts: they are unchanged at the end of the reaction and can be reused many times.'),
        ('The active site and the substrate have the same shape.', 'They have complementary shapes; in the induced-fit model the active site changes shape slightly when the substrate binds.'),
        ('Enzymes provide energy for reactions.', 'Enzymes do not supply energy; they lower the activation energy needed for the reaction to occur.'),
        ('All enzymes work inside cells.', 'Some enzymes are extracellular, such as digestive enzymes secreted into the gut and enzymes secreted by fungi onto their food.')],
  cases=[('hexokinase, the first enzyme of glycolysis', 'X-ray crystallography shows the two lobes of hexokinase close around glucose when it binds.', 'the induced-fit model', 'The change in shape on binding brings catalytic groups into place and excludes water, as predicted by induced fit.'),
         ('lactase used to produce lactose-free milk', 'Immobilised lactase hydrolyses lactose into glucose and galactose as milk flows past.', 'enzyme–substrate specificity and the use of enzymes', 'Lactase acts only on lactose, so other milk components are unchanged; immobilisation allows reuse.'),
         ('digestive enzymes secreted by pancreatic cells', 'Trypsin, lipase and amylase are secreted into the duodenum and act extracellularly.', 'extracellular enzymes', 'They are made inside cells but catalyse reactions outside, breaking down food molecules in the gut lumen.')],
  evaluate=[('The induced-fit model has completely replaced the lock-and-key model.', ['induced fit explains why active sites change shape and how bonds are strained', 'it explains broad specificity of some enzymes'], ['the lock-and-key idea of complementarity is still central and useful in teaching', 'some enzymes change shape very little on binding'], 'Induced fit is the more accurate model, but it builds on rather than discards the complementarity central to lock-and-key; models are refined over time.')],
  extended=[('Explain how the structure of enzymes allows them to act as specific catalysts.', 'Globular proteins; tertiary structure; active site formed by few amino acids; complementary shape/chemistry to substrate; specificity; induced fit – shape change, strain on bonds; lowers activation energy; collision and orientation; products released; enzyme unchanged; denaturation/mutation alter active site.', 8)],
  )

S('ch01-st2',
  terms=[('optimum temperature', 'the temperature at which the rate of an enzyme-catalysed reaction is highest'),
         ('denaturation', 'a permanent change in the shape of an enzyme’s active site, caused by high temperature or extreme pH, so it can no longer bind its substrate'),
         ('substrate concentration', 'the amount of substrate per unit volume, which affects the frequency of enzyme–substrate collisions'),
         ('saturation', 'the point at which all active sites are occupied, so increasing substrate concentration no longer increases the rate'),
         ('optimum pH', 'the pH at which an enzyme has its highest activity')],
  facts=[('What happens to the rate of reaction when substrate concentration is increased beyond saturation?', 'it stays constant', ['it keeps increasing', 'it falls to zero', 'it doubles'], 'All active sites are occupied.'),
         ('Which enzyme has an optimum pH of about 8?', 'trypsin', ['pepsin', 'salivary amylase at pH 2', 'catalase in the stomach'], 'Trypsin acts in the alkaline small intestine.'),
         ('Why does increasing temperature from 10 °C to 30 °C increase the rate of an enzyme reaction?', 'molecules move faster, so collisions between enzyme and substrate are more frequent', ['the enzyme is denatured', 'the active site becomes larger', 'activation energy increases'], 'Kinetic energy rises.'),
         ('What is the optimum temperature of most human enzymes?', 'about 37 °C', ['about 20 °C', 'about 60 °C', 'about 4 °C'], 'Body temperature.')],
  mc2=[('Why does the rate of an enzyme reaction fall rapidly above the optimum temperature?', 'Bonds maintaining the active site break, so the enzyme is denatured.', ['The substrate is used up.', 'Molecules move too slowly.', 'The enzyme becomes more specific.'], 'Hydrogen and ionic bonds break.'),
       ('Why does pH affect enzyme activity?', 'H⁺ and OH⁻ ions change the charges on R groups in and near the active site, affecting binding and shape.', ['pH changes the substrate into a different molecule.', 'pH changes the primary structure.', 'pH only affects temperature.'], 'Ionisation of R groups changes.'),
       ('An enzyme’s rate doubles when substrate concentration doubles, at low concentrations. What does this show?', 'Substrate concentration is the limiting factor at low concentrations.', ['The enzyme is saturated.', 'The enzyme is denatured.', 'Temperature is limiting.'], 'Rate proportional to collisions.'),
       ('Why is the graph of rate against temperature asymmetrical?', 'Rate rises gradually as collisions increase, but falls sharply once denaturation begins.', ['Denaturation is reversible.', 'Enzymes work only at the optimum.', 'Temperature has no effect below the optimum.'], 'Two opposing effects.')],
  mc3=[('Amylase from a thermophilic bacterium has an optimum of 90 °C. Why is it used in industrial starch processing?', 'It remains active at high temperatures where starch gelatinises and reactions are fast.', ['It works only at 37 °C.', 'It is denatured at 50 °C.', 'It converts glucose to starch.'], 'Thermostable enzymes suit hot industrial processes.'),
       ('A student adds more enzyme to a reaction that had reached a plateau due to saturation. What is the expected result?', 'The rate increases because more active sites are available.', ['The rate stays the same.', 'The rate decreases.', 'The reaction stops.'], 'At saturation, enzyme concentration is limiting.'),
       ('Pepsin is placed in a solution of pH 7. What is the most likely result?', 'Little or no activity because the pH is far from its optimum.', ['Maximum activity.', 'It digests starch.', 'It becomes trypsin.'], 'Pepsin works at pH about 2.')],
  why=[('Explain the effect of increasing temperature on the rate of an enzyme-catalysed reaction.', 'As temperature rises, enzyme and substrate molecules gain kinetic energy and collide more often with sufficient energy, so rate increases up to the optimum; above the optimum, vibrations break hydrogen and ionic bonds in the enzyme, changing the active site shape (denaturation), so fewer substrates bind and the rate falls steeply.'),
       ('Explain the effect of substrate concentration on the rate of an enzyme-catalysed reaction.', 'At low substrate concentration, few active sites are occupied, so increasing concentration increases collisions and the rate rises; at higher concentrations most active sites are occupied, so the rate increases less; at saturation all are occupied and the rate stays constant (enzyme concentration is limiting).'),
       ('Explain why different enzymes have different optimum pH values.', 'Each enzyme has R groups whose ionisation must be correct for its active site to bind the substrate; enzymes have evolved to work in different environments (stomach pH 2, small intestine pH 8), so their structures are most stable and active at different pH values.')],
  contrast=[('the effect of temperature below the optimum', 'the effect of temperature above the optimum', 'Below the optimum, increasing temperature increases kinetic energy and collision frequency, raising the rate; above it, increasing temperature denatures the enzyme, lowering the rate.')],
  misc=[('Enzymes are killed at high temperatures.', 'Enzymes are proteins, not living organisms; they are denatured – their shape is changed – not killed.'),
        ('At low temperatures enzymes are denatured.', 'Low temperatures reduce kinetic energy and collisions, slowing the reaction, but do not usually denature enzymes; activity returns on warming.'),
        ('Adding more substrate always increases the rate of an enzyme reaction.', 'Once all active sites are occupied (saturation), adding substrate does not increase the rate.'),
        ('All enzymes have an optimum pH of 7.', 'Optimum pH varies: pepsin about 2, trypsin about 8, salivary amylase about 7.')],
  cases=[('pepsin and trypsin in the human digestive system', 'Pepsin works in the acidic stomach (pH about 2) and trypsin in the alkaline small intestine (pH about 8).', 'the effect of pH on enzyme activity', 'Each has an active site whose R-group charges suit its environment, so each enzyme is most active at a different pH.'),
         ('biological washing powders', 'Proteases and lipases in detergents work at 30–40 °C, saving energy compared with hot washes.', 'the effect of temperature on enzyme activity', 'Enzymes give fast reactions at moderate temperatures; above their optimum they would denature.')],
  evaluate=[('Temperature is the most important factor affecting enzyme activity in the human body.', ['temperature affects every enzyme and fever can denature proteins', 'body temperature is tightly regulated because of this'], ['pH varies more between compartments (stomach vs intestine) than temperature', 'substrate and enzyme concentrations and inhibitors regulate most pathways day to day'], 'Because body temperature is held constant, enzyme activity is mainly controlled by substrate/enzyme concentration, pH in compartments and inhibition; temperature matters most when homeostasis fails.')],
  extended=[('Explain the effects of temperature, pH and substrate concentration on enzyme activity.', 'Temperature: kinetic energy, collisions, optimum, denaturation above; pH: ionisation of R groups, optimum, denaturation at extremes; substrate concentration: rate rises then plateaus at saturation (Vmax); graphs described; examples pepsin/trypsin.', 8)],
  )


def _catalase_dq(rng, slot):
    temps = [10, 20, 30, 40, 50, 60]
    opt = rng.choice([35, 40, 45])
    vmax = rng.uniform(18, 26)
    vols = []
    for t in temps:
        if t <= opt:
            v = vmax * 2 ** ((t - opt) / 10)
        else:
            v = vmax * max(0.05, 1 - (t - opt) / 22)
        vols.append(round(v * rng.uniform(0.95, 1.05), 1))
    src = pick(rng, ['potato tissue', 'liver tissue', 'yeast suspension', 'celery extract'])
    t1, t2 = temps[0], temps[2]
    q10 = vols[2] / vols[1] if vols[1] else None
    intro = (f'Discs of {src} containing catalase were placed in hydrogen peroxide solution at different temperatures. The volume of oxygen collected in 2 minutes was measured.\n\n'
             + table(['Temperature / °C', 'Volume of O₂ in 2 min / cm³'], [(t, f'{v:.1f}') for t, v in zip(temps, vols)]))
    best = temps[vols.index(max(vols))]
    parts = [
        (f'Calculate the mean rate of oxygen production at {temps[3]} °C in cm³ min⁻¹.', f'{vols[3] / 2:.2f} cm³ min⁻¹', f'{vols[3]:.1f}/2 = {vols[3] / 2:.2f} (A1).', 1),
        ('State the temperature at which the highest rate was recorded.', f'{best} °C', f'{best} °C (A1).', 1),
        (f'Calculate the percentage increase in the volume of oxygen between {t1} °C and {t2} °C.', f'{pct_change(vols[0], vols[2]):.0f} %', f'({vols[2]:.1f} − {vols[0]:.1f})/{vols[0]:.1f} × 100 (M1) = {pct_change(vols[0], vols[2]):.0f} % (A1).', 2),
        ('Calculate the temperature coefficient Q₁₀ between 20 °C and 30 °C (rate at 30 °C ÷ rate at 20 °C).', f'{q10:.2f}', f'{vols[2]:.1f}/{vols[1]:.1f} = {q10:.2f} (A1).', 1),
        ('Explain the change in rate above the temperature giving the highest rate.', 'High temperature breaks hydrogen and ionic bonds in catalase; the active site changes shape (denaturation); fewer enzyme–substrate complexes form, so the rate falls.', 'Bonds broken (A1); active site shape changed (A1); fewer ES complexes (A1).', 3),
        ('State two variables that must be controlled.', 'Concentration and volume of H₂O₂; size/number of discs (surface area); pH; time.', 'Any two (A1 A1).', 2),
        ('Suggest why the optimum temperature cannot be stated precisely from these data.', 'Readings were taken at 10 °C intervals; the true optimum could lie anywhere between the intervals either side of the highest reading.', 'Large intervals (A1); need smaller intervals around the peak (A1).', 2),
        ('Suggest one source of error in measuring the volume of oxygen.', 'Oxygen dissolving in water / leaks from the delivery tube / delay in starting timing / reading the measuring cylinder.', 'Any valid source (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch01-st2', _catalase_dq)

S('ch01-st3',
  terms=[('activation energy', 'the minimum energy that reacting molecules must have for a reaction to occur; enzymes lower it'),
         ('rate of reaction', 'the change in concentration (or amount) of substrate or product per unit time'),
         ('initial rate', 'the rate at the start of a reaction, found from the gradient of the tangent to a product–time curve at time zero'),
         ('enzyme–substrate complex', 'the temporary structure formed when a substrate binds to the active site of an enzyme'),
         ('colorimeter', 'an instrument that measures the absorbance or transmission of light by a solution, used to follow reactions that change colour')],
  facts=[('How do enzymes increase the rate of reactions?', 'by lowering the activation energy', ['by increasing the activation energy', 'by supplying energy to the substrate', 'by raising the temperature of the cell'], 'Less energy needed to reach the transition state.'),
         ('How is the rate of a reaction calculated from the time taken to reach an end point?', 'rate = 1/time', ['rate = time × concentration', 'rate = time²', 'rate = time − 1'], 'A shorter time means a faster rate.'),
         ('What does the gradient of a graph of product formed against time represent?', 'the rate of reaction', ['the activation energy', 'the optimum temperature', 'the total product'], 'Rate = change in product/time.'),
         ('Which effect do enzymes have on the overall energy change of a reaction?', 'none – they do not change the energy difference between substrates and products', ['they make it more exothermic', 'they make it endothermic', 'they double it'], 'Only the activation energy changes.')],
  mc2=[('Why does the rate of an enzyme reaction decrease over time in a closed test tube?', 'Substrate is used up, so collisions between enzyme and substrate become less frequent.', ['The enzyme is used up.', 'Products increase the temperature.', 'Activation energy increases.'], 'Substrate concentration falls.'),
       ('Why is the initial rate measured when comparing enzyme activity under different conditions?', 'At the start substrate concentration is known and not yet limiting, so rates are comparable.', ['The reaction has finished.', 'Products have the highest concentration.', 'The enzyme is denatured.'], 'Initial conditions are controlled.'),
       ('Which statement about the energy profile of an enzyme-catalysed reaction is correct?', 'The peak (transition state) is lower than in the uncatalysed reaction.', ['The products have more energy.', 'The substrates have less energy.', 'There is no transition state.'], 'Lower activation energy barrier.')],
  mc3=[('A starch–amylase mixture takes 120 s to stop giving a blue-black colour with iodine at 25 °C and 40 s at 40 °C. By what factor did the rate increase?', '3', ['80', '0.33', '1.5'], 'Rate = 1/t: (1/40)/(1/120) = 3.'),
       ('An enzyme produces 4.8 cm³ of gas in the first 30 s. What is the initial rate in cm³ min⁻¹?', '9.6', ['0.16', '144', '4.8'], '4.8 ÷ 0.5 min = 9.6 cm³ min⁻¹.'),
       ('An energy profile shows an uncatalysed activation energy of 86 kJ mol⁻¹ and a catalysed one of 29 kJ mol⁻¹. By how much has the enzyme lowered the activation energy?', '57 kJ mol⁻¹', ['115 kJ mol⁻¹', '29 kJ mol⁻¹', '2.97 kJ mol⁻¹'], '86 − 29 = 57.')],
  why=[('Explain how enzymes lower the activation energy of reactions.', 'Binding of substrate in the active site (induced fit) strains or distorts bonds within the substrate, holds substrates close together in the correct orientation, and provides a favourable chemical environment, so less energy is needed to reach the transition state.'),
       ('Explain how the rate of an enzyme-catalysed reaction can be measured.', 'By measuring the amount of product formed or substrate used per unit time, e.g. volume of oxygen from catalase per minute, change in colour/absorbance with a colorimeter, or time taken to reach an end point (rate = 1/t); the initial rate is found from the gradient at t = 0.'),
       ('Explain why a tangent is drawn to a product–time curve to find the initial rate.', 'The curve is steepest at the start and becomes less steep as substrate is used up; a tangent at t = 0 gives the gradient (rate) under the starting conditions only.')],
  contrast=[('an uncatalysed reaction', 'an enzyme-catalysed reaction', 'Both have the same energy change between substrates and products; the enzyme-catalysed reaction has a lower activation energy, so more molecules have enough energy to react and the rate is higher.'),
            ('mean rate', 'initial rate', 'Mean rate is the total change divided by total time; initial rate is the rate at the start of the reaction, found from the gradient of the tangent at t = 0 and usually higher than the mean rate.')],
  misc=[('Enzymes give substrates the extra energy they need to react.', 'Enzymes do not supply energy; they lower the activation energy so less energy is required.'),
        ('A reaction that takes longer has a higher rate.', 'Rate is inversely proportional to time: rate = 1/t, so a longer time means a lower rate.'),
        ('Enzymes change the energy released by a reaction.', 'Enzymes do not change the overall energy change; they only lower the activation energy.')],
  cases=[('catalase in liver cells', 'Catalase breaks down hydrogen peroxide into water and oxygen up to millions of times per second.', 'the lowering of activation energy by enzymes', 'Without the enzyme, decomposition of H₂O₂ is very slow because its activation energy is high.'),
         ('measuring amylase activity with iodine solution', 'Samples are tested at intervals until starch is no longer detected (iodine stays yellow-brown).', 'measuring rates of enzyme reactions', 'The time to the end point gives a rate (1/t) that can be compared between conditions.')],
  evaluate=[('Measuring the time to reach an end point is a reliable way to compare enzyme activity.', ['it is simple and gives a rate (1/t) for each condition', 'it needs only basic equipment'], ['judging a colour end point by eye is subjective', 'it gives a mean rate rather than an initial rate'], 'It is acceptable for simple comparisons but continuous measurement (e.g. colorimeter or gas syringe) gives more precise, objective initial rates.')],
  extended=[('Explain how enzymes speed up reactions and describe how the rate of an enzyme-catalysed reaction can be determined experimentally.', 'Activation energy; energy profile diagram; enzyme lowers activation energy, not ΔG; induced fit strains bonds; methods: product (O₂ gas syringe), substrate disappearance (iodine test), colorimeter; rate = amount/time or 1/t; initial rate from tangent; repeats, controls.', 8)],
  )


def _initial_rate_dq(rng, slot):
    times = [0, 30, 60, 90, 120, 150, 180]
    vmax = rng.uniform(20, 32)
    k = rng.uniform(0.012, 0.02)
    p = [round(vmax * (1 - math.exp(-k * t)), 1) for t in times]
    init = vmax * k * 60
    tan = (p[1] - p[0]) / 0.5
    pc = 100 * p[2] / p[-1]
    enz = pick(rng, ['catalase extracted from celery', 'yeast catalase', 'a peroxidase from turnip'])
    intro = (f'The volume of oxygen released when {enz} was added to hydrogen peroxide was measured with a gas syringe every 30 s.\n\n'
             + table(['Time / s', 'Volume of O₂ / cm³'], [(t, f'{v:.1f}') for t, v in zip(times, p)]))
    parts = [
        ('Calculate the mean rate of oxygen production over the first 30 s in cm³ min⁻¹.', f'{tan:.1f} cm³ min⁻¹', f'{p[1]:.1f} cm³ in 0.5 min (M1) = {tan:.1f} cm³ min⁻¹ (A1).', 2),
        ('Calculate the mean rate between 120 s and 180 s in cm³ min⁻¹.', f'{(p[6] - p[4]):.1f} cm³ min⁻¹', f'({p[6]:.1f} − {p[4]:.1f}) cm³ in 1 min = {(p[6] - p[4]):.1f} cm³ min⁻¹ (A1).', 1),
        ('Explain why the rate decreases during the experiment.', 'Hydrogen peroxide (substrate) is used up, so its concentration falls; fewer enzyme–substrate collisions per unit time.', 'Substrate used up (A1); fewer collisions / ES complexes (A1).', 2),
        ('Calculate the percentage of the final volume that had been produced after 60 s.', f'{pc:.0f} %', f'{p[2]:.1f}/{p[-1]:.1f} × 100 = {pc:.0f} % (A1).', 1),
        ('Outline how the initial rate would be found from a graph of these data.', 'Plot volume against time, draw a tangent to the curve at t = 0 and calculate its gradient.', 'Tangent at origin (A1); gradient = rate (A1).', 2),
        ('Predict, with a reason, the effect on the initial rate of doubling the enzyme concentration (with excess substrate).', 'The initial rate would approximately double because twice as many active sites are available.', 'Double (A1) with reason (R1).', 2),
        ('Suggest one reason why the total volume of oxygen collected may be less than expected.', 'Some oxygen dissolves in the solution or escapes before the bung is inserted; the syringe sticks.', 'Valid reason (A1).', 1),
        ('Suggest how the initial rate could be determined more accurately from a graph of the results.', 'Draw a tangent to the curve at time zero and calculate its gradient; take readings at shorter intervals early in the reaction.', 'Tangent at origin (A1); more frequent early readings (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch01-st3', _initial_rate_dq)


@R.add('ch01-st3', 'C3', (1, 5), 'numerical')
def rate_from_time(rng, slot):
    ctx = pick(rng, [('the starch in a starch–amylase mixture to disappear (iodine test)', 's'), ('a milk–trypsin suspension to turn clear', 's'),
                     ('a filter-paper disc soaked in catalase to rise to the surface of hydrogen peroxide', 's'), ('a lipase–milk mixture with phenolphthalein to turn colourless', 's')])
    t1 = rng.randint(40, 300)
    t2 = round(t1 * rng.uniform(0.25, 0.8))
    cond = pick(rng, [('25 °C', '35 °C'), ('pH 5', 'pH 7'), ('0.5 % substrate', '2 % substrate'), ('1 % enzyme', '2 % enzyme')])
    r1, r2 = 1000 / t1, 1000 / t2
    stem = f'The time taken for {ctx[0]} was {t1} s at {cond[0]} and {t2} s at {cond[1]}. Calculate the rate (1000/t, in s⁻¹) under each condition and the percentage increase in rate.'
    p = pct_change(r1, r2)
    return num(stem, f'{r1:.2f} and {r2:.2f} s⁻¹; +{p:.0f} %', f'Rate = 1000/t: {r1:.2f} and {r2:.2f} (A1); ({r2:.2f} − {r1:.2f})/{r1:.2f} × 100 = {p:.0f} % (A1).', 2 if slot.d <= 2 else 3)


S('ch01-st4',
  terms=[('metabolic pathway', 'a chain or cycle of enzyme-catalysed reactions in which the product of one reaction is the substrate of the next'),
         ('competitive inhibitor', 'a molecule with a shape similar to the substrate that binds to the active site, blocking substrate binding'),
         ('non-competitive inhibitor', 'a molecule that binds to a site other than the active site (allosteric site), changing the shape of the enzyme so the substrate cannot bind or react'),
         ('end-product inhibition', 'a form of negative feedback in which the final product of a metabolic pathway inhibits an enzyme early in the pathway'),
         ('allosteric site', 'a site on an enzyme, other than the active site, where a regulatory molecule can bind and alter enzyme activity'),
         ('mechanism-based inhibition', 'irreversible inhibition in which an inhibitor binds covalently to the active site, as when penicillin inhibits transpeptidase')],
  facts=[('Which amino acid inhibits threonine deaminase in an example of end-product inhibition?', 'isoleucine', ['threonine', 'glycine', 'alanine'], 'Isoleucine is the end product of the pathway from threonine.'),
         ('How does a competitive inhibitor reduce enzyme activity?', 'it binds to the active site and prevents substrate binding', ['it binds to an allosteric site', 'it denatures the enzyme', 'it hydrolyses the substrate'], 'It competes with the substrate.'),
         ('Which statement describes non-competitive inhibition?', 'increasing substrate concentration does not overcome the inhibition', ['the inhibitor resembles the substrate', 'Vmax is unchanged', 'the inhibitor binds the active site'], 'Fewer functional enzyme molecules.'),
         ('Which antibiotic acts by mechanism-based inhibition of an enzyme that builds bacterial cell walls?', 'penicillin', ['ethanol', 'insulin', 'aspirin'], 'Penicillin binds irreversibly to transpeptidase.'),
         ('Which is a competitive inhibitor used in medicine?', 'statins, which inhibit HMG-CoA reductase in cholesterol synthesis', ['cyanide', 'penicillin', 'malonate in Krebs cycle only'], 'Statins resemble the substrate.')],
  mc2=[('Why can competitive inhibition be overcome by increasing substrate concentration?', 'The substrate outcompetes the inhibitor for the active site.', ['The inhibitor is destroyed by substrate.', 'The enzyme changes shape permanently.', 'Substrate binds the allosteric site.'], 'Probability of substrate binding increases.'),
       ('Why is end-product inhibition an example of negative feedback?', 'An increase in product reduces its own production by inhibiting an earlier enzyme.', ['Product increases its own production.', 'It speeds up the pathway.', 'It removes the substrate.'], 'Prevents wasteful overproduction.'),
       ('What happens to Vmax in the presence of a non-competitive inhibitor?', 'It decreases.', ['It increases.', 'It is unchanged.', 'It becomes infinite.'], 'Effectively fewer active enzyme molecules.'),
       ('Why are metabolic pathways controlled at the first enzyme rather than the last?', 'Inhibiting the first step prevents intermediates accumulating and saves resources.', ['The last enzyme cannot be inhibited.', 'The first enzyme is the most abundant.', 'Intermediates are needed elsewhere.'], 'Efficient control point.')],
  mc3=[('Without inhibitor an enzyme gives a rate of 40 units; with an inhibitor at the same substrate concentration it gives 28 units. What is the percentage inhibition?', '30 %', ['70 %', '12 %', '43 %'], '(40 − 28)/40 × 100 = 30 %.'),
       ('Malonate resembles succinate and slows the Krebs cycle enzyme succinate dehydrogenase, but its effect disappears at high succinate concentrations. What type of inhibitor is malonate?', 'competitive', ['non-competitive', 'end-product', 'irreversible mechanism-based'], 'Effect overcome by substrate.'),
       ('A graph of rate against substrate concentration with an inhibitor reaches the same maximum as without it, but more slowly. Which inhibitor type is shown?', 'competitive', ['non-competitive', 'denaturing', 'mechanism-based'], 'Vmax unchanged.')],
  why=[('Explain how competitive and non-competitive inhibitors affect enzyme activity.', 'Competitive inhibitors resemble the substrate and bind to the active site, blocking substrate binding; their effect is reduced by high substrate concentration; Vmax unchanged. Non-competitive inhibitors bind to an allosteric site, changing the active site shape; substrate binding/catalysis reduced; high substrate does not overcome it; Vmax decreases.'),
       ('Explain how end-product inhibition controls the synthesis of isoleucine.', 'Threonine is converted to isoleucine in five steps; isoleucine binds to an allosteric site on threonine deaminase, the first enzyme; this inhibits the enzyme so less isoleucine is made when levels are high; as isoleucine falls the enzyme becomes active again – negative feedback.'),
       ('Explain how penicillin kills bacteria.', 'Penicillin binds irreversibly (covalently) to the active site of transpeptidase, which cross-links peptidoglycan; new cell walls are weak; bacteria burst by osmosis as they grow – mechanism-based inhibition.')],
  contrast=[('competitive inhibition', 'non-competitive inhibition', 'Competitive inhibitors bind the active site and are overcome by high substrate concentration (Vmax unchanged); non-competitive inhibitors bind an allosteric site, change the enzyme’s shape and are not overcome by substrate (Vmax reduced).'),
            ('reversible inhibition', 'irreversible (mechanism-based) inhibition', 'Reversible inhibitors bind by weak bonds and can detach; irreversible inhibitors bind covalently and permanently inactivate the enzyme (e.g. penicillin).')],
  misc=[('Non-competitive inhibitors compete with the substrate for the active site.', 'Non-competitive inhibitors bind to an allosteric site, not the active site; they change the enzyme’s shape.'),
        ('End-product inhibition stops a metabolic pathway permanently.', 'End-product inhibition is reversible: when the product concentration falls the inhibitor leaves the enzyme and the pathway resumes.'),
        ('A competitive inhibitor reduces the maximum rate of the enzyme.', 'With enough substrate the maximum rate (Vmax) is reached; a competitive inhibitor only raises the substrate concentration needed.'),
        ('All enzyme inhibitors are harmful poisons.', 'Many inhibitors are useful: drugs such as statins and penicillin, and natural end-product inhibitors that regulate metabolism.')],
  cases=[('the inhibition of threonine deaminase by isoleucine', 'Isoleucine, the end product of a five-step pathway from threonine, binds to an allosteric site on the first enzyme.', 'end-product inhibition', 'High isoleucine switches off its own synthesis by inhibiting the first enzyme, preventing overproduction.'),
         ('statins prescribed to lower blood cholesterol', 'Statins bind to the active site of HMG-CoA reductase in the liver, reducing cholesterol synthesis.', 'competitive inhibition', 'The drug resembles the substrate and competes for the active site.'),
         ('penicillin treatment of bacterial infections', 'Penicillin binds covalently to transpeptidase, preventing cross-linking of peptidoglycan.', 'mechanism-based inhibition', 'Irreversible binding permanently inactivates the enzyme so bacterial walls are weakened.')],
  evaluate=[('Enzyme inhibitors are the most important tool in modern drug development.', ['many important drugs are enzyme inhibitors: statins, penicillin, protease inhibitors for HIV, aspirin', 'knowledge of active site structure allows rational drug design'], ['many drugs act on receptors, ion channels or as replacement hormones', 'resistance can evolve, e.g. bacterial β-lactamases'], 'Enzyme inhibitors are a major class of drugs and structural biology makes them central, but they are one of several important approaches.')],
  extended=[('Distinguish between competitive and non-competitive inhibition and explain how end-product inhibition regulates metabolic pathways.', 'Competitive: active site, substrate-like, overcome by substrate, Vmax same; non-competitive: allosteric site, shape change, Vmax reduced; graphs; examples statins/malonate, cyanide; end-product: isoleucine inhibits threonine deaminase, negative feedback, reversible, efficient; mechanism-based penicillin.', 8)],
  )


def _inhib_dq(rng, slot):
    S_ = [1, 2, 4, 8, 16, 32]
    V = rng.uniform(80, 120)
    Km = rng.uniform(2.5, 4.5)
    comp = rng.random() < 0.5
    Ki = rng.uniform(1.0, 2.0)
    I = 2.0
    v0 = [round(V * s / (Km + s), 0) for s in S_]
    if comp:
        v1 = [round(V * s / (Km * (1 + I / Ki) + s), 0) for s in S_]
    else:
        f = 1 / (1 + I / Ki)
        v1 = [round(V * f * s / (Km + s), 0) for s in S_]
    inh = [100 * (a - b) / a for a, b in zip(v0, v1)]
    intro = ('The initial rate of an enzyme-catalysed reaction (arbitrary units) was measured at different substrate concentrations, with and without a fixed concentration of inhibitor X.\n\n'
             + table(['Substrate / mmol dm⁻³', 'Rate without X', 'Rate with X'], [(s, f'{a:.0f}', f'{b:.0f}') for s, a, b in zip(S_, v0, v1)]))
    typ = 'competitive' if comp else 'non-competitive'
    reason = ('the percentage inhibition decreases as substrate concentration increases, so substrate outcompetes the inhibitor' if comp
              else 'the percentage inhibition stays about the same at all substrate concentrations, so extra substrate does not overcome it')
    parts = [
        ('Calculate the percentage inhibition at 2 mmol dm⁻³ substrate.', f'{inh[1]:.0f} %', f'({v0[1]:.0f} − {v1[1]:.0f})/{v0[1]:.0f} × 100 (M1) = {inh[1]:.0f} % (A1).', 2),
        ('Calculate the percentage inhibition at 32 mmol dm⁻³ substrate.', f'{inh[-1]:.0f} %', f'({v0[-1]:.0f} − {v1[-1]:.0f})/{v0[-1]:.0f} × 100 = {inh[-1]:.0f} % (A1).', 1),
        ('Deduce, with a reason, whether X is a competitive or a non-competitive inhibitor.', f'{typ}: {reason}', f'{typ} (A1); reason from comparison of percentage inhibition (R1).', 2),
        ('Describe the effect of substrate concentration on the rate without inhibitor.', 'Rate increases steeply at low substrate concentrations, then more slowly, approaching a maximum as active sites become saturated.', 'Increase then levelling (A1); saturation explanation (R1).', 2),
        (f'Explain how a {typ} inhibitor reduces the rate of reaction.', ('It has a shape similar to the substrate and binds to the active site, so fewer substrate molecules can bind.' if comp else 'It binds to an allosteric site, changing the shape of the active site so the substrate cannot bind or react.'),
         'Binding site (A1); effect on substrate binding (A1).', 2),
        ('Predict the maximum rate with inhibitor X at very high substrate concentration.', (f'About the same as without X (≈ {V:.0f} units)' if comp else f'Lower than without X (≈ {V / (1 + I / Ki):.0f} units)'), 'Correct prediction consistent with inhibitor type (A1).', 1),
        ('State one variable that must be kept constant.', 'Temperature, pH, enzyme concentration, inhibitor concentration.', 'Any one (A1).', 1),
        ('Explain why the initial rate, rather than the rate after several minutes, was measured.', 'Substrate concentration falls and product accumulates as the reaction proceeds, so only the initial rate reflects the stated substrate concentration.', 'Substrate depletion (A1); valid comparison (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch01-st4', _inhib_dq)


# =============================================================================================
# ch02 C1.2 Cell respiration and C1.3 Photosynthesis
# =============================================================================================
S('ch02-st1',
  terms=[('ATP', 'adenosine triphosphate, a nucleotide that acts as the immediately available energy currency of the cell'),
         ('cell respiration', 'the controlled release of energy from organic compounds in cells to produce ATP'),
         ('anaerobic respiration', 'respiration without oxygen, which yields a small amount of ATP; lactate in animals, ethanol and CO₂ in yeast and plants'),
         ('aerobic respiration', 'respiration using oxygen, in which glucose is fully oxidised to CO₂ and water with a large yield of ATP'),
         ('respiratory quotient', 'the ratio of the volume of CO₂ produced to the volume of O₂ consumed in respiration (RQ = CO₂/O₂)'),
         ('respirometer', 'apparatus used to measure the rate of oxygen uptake by respiring organisms')],
  facts=[('What are the products of anaerobic respiration in yeast?', 'ethanol and carbon dioxide', ['lactate only', 'water and carbon dioxide', 'lactate and carbon dioxide'], 'Used in brewing and baking.'),
         ('What is the product of anaerobic respiration in human muscle?', 'lactate', ['ethanol', 'carbon dioxide and water', 'glucose'], 'NAD is regenerated.'),
         ('Approximately how much ATP does aerobic respiration yield per glucose compared with anaerobic?', 'about 30 molecules compared with 2', ['2 compared with 30', 'the same', '100 compared with 50'], 'Oxidative phosphorylation produces most ATP.'),
         ('When ATP is hydrolysed to ADP, what else is produced?', 'inorganic phosphate and released energy', ['glucose', 'oxygen', 'carbon dioxide'], 'ATP + H₂O → ADP + Pi.'),
         ('What is the RQ for the aerobic respiration of glucose?', '1.0', ['0.7', '0.9', '2.0'], '6 CO₂ produced : 6 O₂ used.')],
  mc2=[('Why is ATP rather than glucose used directly as the energy source for cell activities?', 'ATP releases energy in small, usable amounts in a single hydrolysis step.', ['ATP contains more energy than glucose.', 'Glucose cannot be broken down.', 'ATP is stored for long periods.'], 'Immediate, manageable energy release.'),
       ('Why does anaerobic respiration produce far less ATP than aerobic respiration?', 'Glucose is only partly broken down and there is no oxidative phosphorylation.', ['Anaerobic respiration uses more glucose.', 'It produces more NADH.', 'It occurs in mitochondria.'], 'Only glycolysis yields ATP.'),
       ('Why does the RQ of a person increase above 1.0 during very intense exercise?', 'Extra CO₂ is released from the blood buffer as lactate accumulates.', ['Fat is being respired.', 'Less CO₂ is produced.', 'Oxygen consumption increases more than CO₂.'], 'Bicarbonate buffering releases CO₂.'),
       ('Which is a use of energy from ATP in cells?', 'active transport of ions against concentration gradients', ['diffusion of oxygen', 'osmosis', 'facilitated diffusion'], 'Also synthesis and movement.')],
  mc3=[('A germinating seed uses 2.4 cm³ O₂ and produces 1.7 cm³ CO₂ in an hour. What is its RQ, and what is it probably respiring?', '0.71; lipid', ['1.41; carbohydrate', '0.71; carbohydrate', '1.0; protein'], 'RQ ≈ 0.7 indicates lipid.'),
       ('Yeast in a sealed flask produces CO₂ at a constant rate, but ethanol only appears after several hours. What is the best explanation?', 'Yeast respires aerobically until the oxygen is used up, then switches to anaerobic respiration.', ['Ethanol is made only in light.', 'CO₂ is converted into ethanol.', 'Yeast is an obligate anaerobe.'], 'Facultative anaerobe.')],
  why=[('Explain why ATP is a suitable energy currency for cells.', 'Hydrolysis of the terminal phosphate releases energy in small usable amounts; ATP is soluble and easily moved within cells; it can be rapidly regenerated from ADP and Pi by respiration; it couples energy-releasing and energy-requiring reactions.'),
       ('Explain why lactate is produced in human muscle during vigorous exercise.', 'Oxygen supply cannot meet demand, so oxidative phosphorylation slows; pyruvate is reduced to lactate using NADH, regenerating NAD so glycolysis can continue to produce a small amount of ATP.'),
       ('Explain how a respirometer measures the rate of respiration.', 'Organisms are enclosed with an alkali (e.g. soda lime) that absorbs CO₂; O₂ used reduces gas volume, so a coloured liquid in a capillary moves towards the organisms; distance moved × cross-sectional area per unit time gives the rate of O₂ uptake; a control tube compensates for temperature and pressure changes.')],
  contrast=[('aerobic respiration', 'anaerobic respiration', 'Aerobic respiration uses oxygen, occurs in cytoplasm and mitochondria, fully oxidises glucose to CO₂ and water and yields about 30 ATP; anaerobic respiration occurs without oxygen in the cytoplasm only, gives lactate (animals) or ethanol and CO₂ (yeast/plants) and yields 2 ATP.'),
            ('anaerobic respiration in yeast', 'anaerobic respiration in humans', 'Yeast converts pyruvate to ethanol and CO₂; humans convert pyruvate to lactate with no CO₂ released; both regenerate NAD and yield 2 ATP per glucose.')],
  misc=[('Respiration means breathing.', 'Respiration is the chemical release of energy from organic molecules in cells to make ATP; breathing (ventilation) is the movement of air into and out of the lungs.'),
        ('ATP is a long-term energy store.', 'ATP is an immediate energy source; long-term energy is stored as fats and glycogen/starch.'),
        ('Anaerobic respiration in humans produces carbon dioxide.', 'Anaerobic respiration in humans produces only lactate; CO₂ is produced in anaerobic respiration of yeast and plants.'),
        ('Plants only photosynthesise and do not respire.', 'Plant cells respire all the time, day and night, to produce ATP.')],
  cases=[('bread making with Saccharomyces cerevisiae', 'Yeast ferments sugars in dough, producing CO₂ bubbles that make the bread rise; the ethanol evaporates during baking.', 'anaerobic respiration in yeast', 'Without oxygen, yeast converts pyruvate to ethanol and CO₂.'),
         ('sprint training and lactate threshold in athletes', 'During a 400 m sprint blood lactate can rise more than tenfold.', 'anaerobic respiration in humans', 'When oxygen supply is insufficient, muscles regenerate NAD by making lactate, allowing a short burst of ATP production.')],
  evaluate=[('Anaerobic respiration is an inefficient process that is of little value to organisms.', ['it yields only 2 ATP per glucose compared with about 30', 'lactate accumulation causes fatigue'], ['it allows ATP production when oxygen is limited, e.g. in sprints or waterlogged roots', 'yeast fermentation is the basis of brewing and baking'], 'It is inefficient in ATP per glucose, but very valuable as a rapid, oxygen-independent source of ATP.')],
  extended=[('Compare aerobic and anaerobic respiration and explain the role of ATP in cells.', 'ATP structure and hydrolysis; uses: active transport, synthesis, movement; aerobic: O₂, mitochondria, CO₂ + H₂O, ~30 ATP; anaerobic: cytoplasm, lactate or ethanol + CO₂, 2 ATP, NAD regeneration; respirometers; RQ.', 8)],
  )


@R.add('ch02-st1', 'C3', (1, 5), 'numerical')
def respirometer(rng, slot):
    org = pick(rng, ['germinating pea seeds', 'woodlice', 'blowfly larvae', 'germinating mung beans', 'mealworms', 'yeast beads'])
    r = pick(rng, [0.5, 0.75, 1.0])
    d = rng.randint(12, 80)
    t = pick(rng, [5, 10, 15, 20])
    m = round(rng.uniform(2.0, 12.0), 1)
    vol = math.pi * r * r * d
    rate = vol / t
    stem = (f'A respirometer containing soda lime and {m} g of {org} was used. The coloured liquid moved {d} mm in {t} minutes along a capillary of radius {r} mm. '
            f'Calculate the rate of oxygen uptake in mm³ g⁻¹ min⁻¹.')
    key = f'V = πr²d = π × {r}² × {d} = {sf(vol)} mm³ (M1); ÷ {t} min ÷ {m} g = {sf(rate / m)} mm³ g⁻¹ min⁻¹ (A1).'
    if slot.d >= 4:
        rq = pick(rng, [0.7, 0.8, 0.9, 1.0])
        stem += f' In a second run without soda lime, the liquid moved {round(d * (1 - rq)):d} mm in the same time. Calculate the RQ and suggest which substrate is being respired.'
        sub = 'lipid' if rq <= 0.75 else 'protein or a mixture' if rq < 0.95 else 'carbohydrate'
        return num(stem, f'{sf(rate / m)} mm³ g⁻¹ min⁻¹; RQ = {rq}; {sub}', key + f' Without soda lime net movement = O₂ − CO₂, so CO₂ = {d} − {round(d * (1 - rq))} = {d - round(d * (1 - rq))} mm; RQ = {d - round(d * (1 - rq))}/{d} = {(d - round(d * (1 - rq))) / d:.2f} (M1 A1); {sub} (R1).', 5)
    return num(stem, f'{sf(rate / m)} mm³ g⁻¹ min⁻¹', key, 2)


@R.add('ch02-st1', 'C3', (1, 4), 'mcq')
def rq_mcq(rng, slot):
    subs = [('glucose', 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', 6, 6), ('tripalmitin (a fat)', '2C₅₁H₉₈O₆ + 145O₂ → 102CO₂ + 98H₂O', 102, 145),
            ('oleic acid', 'C₁₈H₃₄O₂ + 25.5O₂ → 18CO₂ + 17H₂O', 18, 25.5), ('the amino acid alanine', '2C₃H₇O₂N + 6O₂ → 5CO₂ + 5H₂O + CO(NH₂)₂', 5, 6),
            ('malic acid', 'C₄H₆O₅ + 3O₂ → 4CO₂ + 3H₂O', 4, 3)]
    nm, eq, c, o = pick(rng, subs)
    rq = c / o
    return nmcq(rng, f'The equation for the aerobic respiration of {nm} is {eq}. What is the respiratory quotient?', f'{rq:.2f}',
                [f'{o / c:.2f}', f'{rq + 0.3:.2f}', f'{abs(rq - 0.3):.2f}', '1.00'], f'RQ = CO₂/O₂ = {c}/{o} = {rq:.2f}.')


S('ch02-st2',
  terms=[('glycolysis', 'the first stage of respiration in the cytoplasm, in which glucose is converted to two pyruvate with a net gain of 2 ATP and 2 reduced NAD'),
         ('link reaction', 'the oxidative decarboxylation of pyruvate in the mitochondrial matrix to form acetyl-CoA, releasing CO₂ and reducing NAD'),
         ('Krebs cycle', 'a cycle of reactions in the mitochondrial matrix in which acetyl groups are oxidised, releasing CO₂ and producing reduced NAD, reduced FAD and ATP'),
         ('oxidative phosphorylation', 'production of ATP using energy released as electrons pass along the electron transport chain, coupled by chemiosmosis'),
         ('chemiosmosis', 'the movement of protons down their concentration gradient through ATP synthase, driving the synthesis of ATP'),
         ('decarboxylation', 'the removal of carbon as CO₂ from a molecule'),
         ('oxidation', 'the loss of electrons or hydrogen (or gain of oxygen) by a substance')],
  facts=[('Where does glycolysis take place?', 'in the cytoplasm', ['in the mitochondrial matrix', 'on the cristae', 'in the intermembrane space'], 'No oxygen required.'),
         ('What is the final electron acceptor in the electron transport chain?', 'oxygen', ['NAD', 'pyruvate', 'carbon dioxide'], 'Oxygen combines with electrons and protons to form water.'),
         ('How many molecules of CO₂ are released per glucose in the link reaction and Krebs cycle combined?', '6', ['2', '4', '3'], '2 in link reaction + 4 in Krebs cycle.'),
         ('Which enzyme synthesises ATP during chemiosmosis?', 'ATP synthase', ['RuBisCO', 'hexokinase', 'DNA polymerase'], 'Protons flow through it.'),
         ('Which molecule combines with acetyl-CoA at the start of the Krebs cycle?', 'oxaloacetate (4C)', ['citrate (6C)', 'pyruvate (3C)', 'glucose (6C)'], 'Forms citrate (6C).')],
  mc2=[('Why does glycolysis require an input of 2 ATP?', 'To phosphorylate glucose, making it more reactive (lowering activation energy for lysis).', ['To produce oxygen.', 'To reduce NAD.', 'To make pyruvate leave the cell.'], 'Phosphorylation before lysis.'),
       ('Why does the Krebs cycle stop if oxygen is unavailable?', 'Reduced NAD cannot be reoxidised by the electron transport chain, so NAD runs out.', ['Oxygen is a substrate of the Krebs cycle.', 'CO₂ cannot be released.', 'Glucose cannot enter mitochondria.'], 'Indirect dependence on O₂.'),
       ('How do electrons in the ETC generate a proton gradient?', 'Energy released as electrons pass between carriers is used to pump protons into the intermembrane space.', ['Electrons carry protons through ATP synthase.', 'Oxygen pumps protons.', 'ATP pumps protons out of the matrix.'], 'Proton pumping by complexes.'),
       ('Why is the mitochondrial inner membrane impermeable to protons except through ATP synthase?', 'So the proton gradient is maintained and can only be dissipated by making ATP.', ['So ATP cannot leave.', 'So oxygen cannot enter.', 'So glucose stays in the matrix.'], 'Uncouplers make it leaky and reduce ATP yield.')],
  mc3=[('A poison blocks ATP synthase. Which effect would be observed first?', 'The proton gradient builds up and ATP production by oxidative phosphorylation stops.', ['Glycolysis stops immediately.', 'More ATP is made.', 'Oxygen consumption rises.'], 'Protons cannot flow back.'),
       ('Dinitrophenol makes the inner mitochondrial membrane leaky to protons. Patients taking it lost weight and overheated. Why?', 'Energy from the proton gradient was released as heat instead of making ATP, so more substrate was respired.', ['It blocked glycolysis.', 'It stopped oxygen uptake.', 'It increased ATP production.'], 'Uncoupling.'),
       ('How many reduced NAD are produced per glucose in the link reaction and Krebs cycle together?', '8', ['2', '6', '10'], '2 (link) + 6 (Krebs).')],
  why=[('Explain the processes that occur in glycolysis.', 'Glucose is phosphorylated twice using 2 ATP; the hexose bisphosphate splits into two triose phosphates (lysis); each triose phosphate is oxidised by removal of hydrogen, reducing NAD; 4 ATP are formed by substrate-level phosphorylation; two pyruvate result; net gain 2 ATP and 2 NADH.'),
       ('Explain the link reaction and the Krebs cycle.', 'Pyruvate enters the matrix and is decarboxylated and oxidised, forming acetyl-CoA, CO₂ and NADH; acetyl (2C) combines with oxaloacetate (4C) to form citrate (6C); two decarboxylations and four oxidations regenerate oxaloacetate, releasing 2 CO₂, 3 NADH, 1 FADH₂ and 1 ATP per turn.'),
       ('Explain how ATP is produced by chemiosmosis in mitochondria.', 'Reduced NAD and FAD donate electrons to the ETC on the cristae; as electrons pass along carriers, energy is used to pump protons into the intermembrane space; a proton gradient builds; protons flow back through ATP synthase, which phosphorylates ADP; oxygen accepts electrons and protons, forming water.')],
  contrast=[('substrate-level phosphorylation', 'oxidative phosphorylation', 'In substrate-level phosphorylation a phosphate group is transferred directly from a substrate to ADP (glycolysis, Krebs); in oxidative phosphorylation ATP is made by ATP synthase using a proton gradient generated by the electron transport chain.'),
            ('the link reaction', 'the Krebs cycle', 'The link reaction converts each pyruvate (3C) to acetyl-CoA (2C), releasing one CO₂ and one NADH; the Krebs cycle oxidises the acetyl group in a cycle starting with oxaloacetate, releasing two CO₂, three NADH, one FADH₂ and one ATP per turn.')],
  misc=[('Oxygen is used in the Krebs cycle to make carbon dioxide.', 'CO₂ in the Krebs cycle comes from decarboxylation of organic molecules; oxygen is used only at the end of the ETC as the final electron acceptor.'),
        ('Glycolysis takes place in the mitochondria.', 'Glycolysis occurs in the cytoplasm; the link reaction and Krebs cycle occur in the mitochondrial matrix.'),
        ('Most ATP in aerobic respiration is made in the Krebs cycle.', 'Most ATP is made by oxidative phosphorylation (chemiosmosis); the Krebs cycle makes only 2 ATP per glucose directly.'),
        ('Protons are pumped into the matrix by the electron transport chain.', 'Protons are pumped from the matrix into the intermembrane space; they flow back into the matrix through ATP synthase.')],
  cases=[('cyanide poisoning', 'Cyanide binds to cytochrome c oxidase, the final complex of the electron transport chain.', 'the role of oxygen in oxidative phosphorylation', 'Electrons cannot pass to oxygen, so the ETC and chemiosmosis stop and ATP production collapses.'),
         ('Peter Mitchell’s chemiosmotic theory (Nobel Prize 1978)', 'Mitchell proposed that a proton gradient across membranes links electron transport to ATP synthesis; it was initially rejected.', 'chemiosmosis', 'Experimental evidence of proton gradients driving ATP synthesis led to acceptance – a paradigm shift.')],
  evaluate=[('The theoretical yield of 38 ATP per glucose is an accurate description of aerobic respiration.', ['counting NADH × 3 and FADH₂ × 2 gives 38 ATP per glucose', 'it gives a useful comparison with anaerobic respiration'], ['proton leak and transport costs mean the real yield is about 30–32 ATP', 'the yield varies with the shuttle used to bring NADH into mitochondria'], 'The 38 figure is a theoretical maximum; measured yields are closer to 30, showing the difference between idealised models and real systems.')],
  extended=[('Describe the stages of aerobic respiration in a eukaryotic cell, including where each occurs and what is produced.', 'Glycolysis (cytoplasm): phosphorylation, lysis, oxidation, 2 pyruvate, net 2 ATP, 2 NADH. Link (matrix): decarboxylation, oxidation, acetyl-CoA, CO₂, NADH. Krebs (matrix): citrate, 2 CO₂, 3 NADH, FADH₂, ATP per turn. ETC (cristae): electrons, proton pumping, gradient, ATP synthase, O₂ final acceptor, water; ~30 ATP.', 8)],
  )


@R.add('ch02-st2', 'C3', (1, 5), 'numerical')
def resp_count(rng, slot):
    n = pick(rng, [1, 2, 3, 4, 5, 10])
    what = rng.randrange(4)
    labels = ['molecules of CO₂ released in the link reaction and Krebs cycle', 'molecules of reduced NAD produced in glycolysis, the link reaction and Krebs cycle',
              'turns of the Krebs cycle', 'molecules of ATP produced by substrate-level phosphorylation (net)']
    vals = [6 * n, 10 * n, 2 * n, 4 * n]
    expl = [f'2 (link) + 4 (Krebs) = 6 per glucose × {n}', f'2 (glycolysis) + 2 (link) + 6 (Krebs) = 10 per glucose × {n}', f'2 acetyl-CoA per glucose × {n}', f'net 2 (glycolysis) + 2 (Krebs) = 4 per glucose × {n}']
    stem = f'Calculate the number of {labels[what]} when {n} molecule{"s" if n > 1 else ""} of glucose {"is" if n == 1 else "are"} respired aerobically.'
    if slot.d >= 4:
        stem += ' Explain why the number of ATP produced by oxidative phosphorylation is much larger.'
        return num(stem, f'{vals[what]}; most ATP is made by chemiosmosis using energy from NADH and FADH₂', f'{expl[what]} = {vals[what]} (A1 A1); reduced NAD/FAD donate electrons to ETC, protons pumped, ATP synthase makes ~2.5 ATP per NADH (R1).', 4)
    return num(stem, f'{vals[what]}', f'{expl[what]} = {vals[what]} (A1).', 2)


RF = [('carotene', 0.95, 'orange-yellow'), ('phaeophytin', 0.83, 'grey'), ('xanthophyll', 0.71, 'yellow'),
      ('chlorophyll a', 0.60, 'blue-green'), ('chlorophyll b', 0.47, 'yellow-green')]

S('ch02-st3',
  terms=[('photosynthetic pigment', 'a molecule that absorbs specific wavelengths of light for photosynthesis, such as chlorophyll a, chlorophyll b and carotenoids'),
         ('absorption spectrum', 'a graph showing the percentage of light absorbed by a pigment at each wavelength'),
         ('action spectrum', 'a graph showing the rate of photosynthesis at each wavelength of light'),
         ('Rf value', 'in chromatography, the distance moved by a pigment divided by the distance moved by the solvent front'),
         ('chromatography', 'a technique for separating the components of a mixture according to their differing solubility in a solvent and attraction to a stationary phase'),
         ('accessory pigment', 'a pigment such as carotene or chlorophyll b that absorbs wavelengths not absorbed by chlorophyll a and passes the energy to it')],
  facts=[('Which colours of light are absorbed most by chlorophyll?', 'red and blue', ['green and yellow', 'green only', 'infrared'], 'Green is reflected, so leaves look green.'),
         ('Why do leaves appear green?', 'chlorophyll reflects and transmits green light', ['chlorophyll absorbs green light', 'leaves contain green carotenoids', 'chloroplasts emit green light'], 'Green is least absorbed.'),
         ('In thin-layer chromatography of leaf pigments, which pigment usually travels furthest?', 'carotene', ['chlorophyll b', 'chlorophyll a', 'xanthophyll'], 'Most soluble in the non-polar solvent.'),
         ('What is the range of wavelengths of visible light?', 'about 400–700 nm', ['about 100–400 nm', 'about 700–1000 nm', 'about 10–100 nm'], 'Violet ~400, red ~700.')],
  mc2=[('Why does the action spectrum closely match the absorption spectrum of chlorophyll?', 'Light must be absorbed by pigments to drive photosynthesis, so wavelengths absorbed most give the highest rates.', ['Photosynthesis does not need light.', 'Only green light is used.', 'Pigments emit light.'], 'Absorption drives the action.'),
       ('Why does a mixture of pigments benefit a plant?', 'Different pigments absorb different wavelengths, widening the range of light used.', ['All pigments absorb the same wavelengths.', 'Mixtures reflect more light.', 'Pigments protect against water loss.'], 'Accessory pigments extend absorption.'),
       ('Why do pigments separate in chromatography?', 'They differ in solubility in the solvent and attraction to the stationary phase.', ['They have different colours.', 'They react with the paper.', 'They are different sizes only.'], 'Partitioning between phases.')],
  mc3=[('In a chromatogram, the solvent front moved 8.0 cm and a yellow-green spot moved 3.8 cm. Using Rf values carotene 0.95, xanthophyll 0.71, chlorophyll a 0.60, chlorophyll b 0.47, identify the pigment.', 'chlorophyll b', ['chlorophyll a', 'xanthophyll', 'carotene'], 'Rf = 3.8/8.0 = 0.48.'),
       ('Elodea in green light produces few bubbles, but many in red and blue light. What does this show?', 'The rate of photosynthesis depends on the wavelengths absorbed by chlorophyll.', ['Green light is most effective.', 'Elodea does not photosynthesise in red light.', 'Bubbles are carbon dioxide.'], 'Matches absorption spectrum.')],
  why=[('Explain why the action spectrum of photosynthesis has peaks in the blue and red regions.', 'Chlorophyll a and b absorb blue (about 430–450 nm) and red (about 640–680 nm) light strongly; absorbed light energy excites electrons in the photosystems, driving the light-dependent reactions, so these wavelengths give the highest rates.'),
       ('Explain how chromatography can be used to separate and identify photosynthetic pigments.', 'Pigment extract is spotted on a baseline; the strip is placed in solvent below the line; solvent moves up carrying pigments at different rates depending on solubility and adsorption; Rf values (distance pigment/distance solvent) and colours are compared with known values to identify them.')],
  contrast=[('an absorption spectrum', 'an action spectrum', 'An absorption spectrum shows how much light each pigment absorbs at each wavelength; an action spectrum shows the rate of photosynthesis at each wavelength.'),
            ('chlorophyll a', 'carotenoids', 'Chlorophyll a is the primary pigment at reaction centres, absorbing red and blue light and appearing blue-green; carotenoids are accessory pigments that absorb blue–green light, appear yellow-orange and protect chlorophyll from excess light.')],
  misc=[('Plants use green light most because they are green.', 'Leaves look green because green light is reflected and transmitted; it is absorbed least and so is used least.'),
        ('The Rf value of a pigment is the distance it moves in centimetres.', 'Rf is a ratio: distance moved by the pigment ÷ distance moved by the solvent front; it has no units and is between 0 and 1.')],
  cases=[('autumn colour change in deciduous trees such as maples', 'Chlorophyll is broken down before leaf fall, revealing yellow-orange carotenoids.', 'the presence of several photosynthetic pigments', 'Carotenoids were present all along as accessory pigments, masked by chlorophyll.'),
         ('Engelmann’s experiment with Spirogyra and aerobic bacteria (1882)', 'Bacteria clustered along the alga where it was lit by red and blue light from a prism.', 'the action spectrum of photosynthesis', 'More O₂ was released at the wavelengths chlorophyll absorbs, so bacteria gathered there.')],
  evaluate=[('LED lighting in vertical farms should provide only red and blue light.', ['red and blue are absorbed most and drive photosynthesis efficiently, saving energy', 'growers report good yields with red/blue LEDs'], ['some green light penetrates deeper into the canopy and drives photosynthesis in lower leaves', 'other wavelengths affect plant development and allow workers to see plant health'], 'Red and blue give the most photosynthesis per unit energy, but adding some green and far-red improves growth and canopy photosynthesis.')],
  extended=[('Describe how photosynthetic pigments can be separated by chromatography and explain the relationship between absorption and action spectra.', 'Extract in solvent; spot; develop; solvent front; Rf; identify carotene, xanthophyll, chlorophyll a, b; absorption spectra of pigments; action spectrum peaks red/blue; trough green; accessory pigments widen range; Engelmann.', 7)],
  )


@R.add('ch02-st3', 'C3', (1, 5), 'numerical')
def rf_calc(rng, slot):
    front = round(rng.uniform(6.0, 12.0), 1)
    k = 2 if slot.d <= 2 else 3 if slot.d == 3 else 4
    pig = rng.sample(RF, k)
    dists = [round(p[1] * front * rng.uniform(0.98, 1.02), 1) for p in pig]
    rf = [d / front for d in dists]
    lines = '; '.join(f'spot {i + 1} ({p[2]}) {d} cm' for i, (p, d) in enumerate(zip(pig, dists)))
    stem = (f'In a chromatogram of a leaf extract the solvent front moved {front} cm. The spots moved: {lines}. Calculate the Rf value of each spot and identify the pigments, '
            f'using reference values carotene 0.95, phaeophytin 0.83, xanthophyll 0.71, chlorophyll a 0.60, chlorophyll b 0.47.')
    ans = '; '.join(f'spot {i + 1}: Rf {r:.2f} = {p[0]}' for i, (p, r) in enumerate(zip(pig, rf)))
    return num(stem, ans, 'Rf = distance moved by spot ÷ distance moved by solvent (M1); ' + '; '.join(f'{d}/{front} = {r:.2f} → {p[0]}' for p, d, r in zip(pig, dists, rf)) + ' (A1 each).', k + 1)


S('ch02-st4',
  terms=[('photosystem', 'a complex of pigment molecules and proteins in the thylakoid membrane that absorbs light and transfers excited electrons; photosystems I and II'),
         ('photolysis', 'the splitting of water molecules using light energy at photosystem II, releasing electrons, protons and oxygen'),
         ('photophosphorylation', 'the production of ATP using energy from light, by chemiosmosis in the thylakoid membrane'),
         ('Calvin cycle', 'the light-independent reactions in the stroma in which CO₂ is fixed by RuBisCO and reduced to triose phosphate using ATP and NADPH'),
         ('RuBisCO', 'ribulose bisphosphate carboxylase, the enzyme that fixes CO₂ by combining it with RuBP'),
         ('ribulose bisphosphate (RuBP)', 'the five-carbon compound that accepts CO₂ in the Calvin cycle and is regenerated using ATP'),
         ('glycerate 3-phosphate (GP)', 'the three-carbon compound formed when CO₂ combines with RuBP, which is reduced to triose phosphate')],
  facts=[('Where do the light-dependent reactions take place?', 'in the thylakoid membranes', ['in the stroma', 'in the cytoplasm', 'in the mitochondrial matrix'], 'Photosystems and ATP synthase are in thylakoids.'),
         ('What is the source of the oxygen released in photosynthesis?', 'water, split by photolysis', ['carbon dioxide', 'glucose', 'RuBP'], 'Shown with ¹⁸O isotopes.'),
         ('Which products of the light-dependent reactions are used in the Calvin cycle?', 'ATP and reduced NADP', ['oxygen and glucose', 'water and CO₂', 'RuBP and GP'], 'They reduce GP and regenerate RuBP.'),
         ('How many carbon atoms are in RuBP?', 'five', ['three', 'six', 'two'], 'CO₂ (1C) + RuBP (5C) → 2 GP (3C).'),
         ('Which enzyme is thought to be the most abundant protein on Earth?', 'RuBisCO', ['ATP synthase', 'catalase', 'amylase'], 'Leaves contain large amounts because it is slow.')],
  mc2=[('Why does the Calvin cycle stop shortly after a plant is put in darkness?', 'ATP and NADPH from the light-dependent reactions run out.', ['RuBisCO is denatured in the dark.', 'CO₂ is not available in darkness.', 'Oxygen inhibits the cycle.'], 'The cycle depends on light reactions.'),
       ('What happens to GP and RuBP levels immediately after the light is switched off?', 'GP rises and RuBP falls.', ['GP falls and RuBP rises.', 'Both rise.', 'Both fall.'], 'GP is not reduced; RuBP not regenerated but still used.'),
       ('Why is the thylakoid lumen small?', 'A high proton concentration builds up quickly for chemiosmosis.', ['It stores starch.', 'It contains RuBisCO.', 'It contains DNA.'], 'Steep gradient drives ATP synthase.'),
       ('Why is photolysis necessary?', 'It replaces electrons lost from photosystem II.', ['It produces CO₂.', 'It makes glucose.', 'It produces ATP directly.'], 'P680 needs electrons after excitation.')],
  mc3=[('After CO₂ supply to an illuminated alga is reduced, which change is expected?', 'RuBP rises and GP falls.', ['GP rises and RuBP falls.', 'Both rise.', 'Oxygen release increases.'], 'Less carboxylation of RuBP.'),
       ('How many turns of the Calvin cycle are needed to make one glucose molecule?', '6', ['1', '3', '12'], 'One CO₂ fixed per turn.'),
       ('In Calvin’s “lollipop” experiment, ¹⁴C appeared first in which compound after 5 seconds?', 'glycerate 3-phosphate', ['glucose', 'RuBP', 'starch'], 'The first stable product of fixation.')],
  why=[('Explain the light-dependent reactions of photosynthesis.', 'Light absorbed by photosystem II excites electrons, which pass along an electron transport chain to photosystem I; energy is used to pump protons into the thylakoid lumen; photolysis of water replaces electrons and releases O₂ and H⁺; protons diffuse through ATP synthase making ATP; PSI re-excites electrons, which reduce NADP.'),
       ('Explain the light-independent reactions (Calvin cycle).', 'RuBisCO fixes CO₂ to RuBP forming two GP; GP is reduced to triose phosphate using ATP and NADPH; for every 6 TP made, 5 are used to regenerate 3 RuBP using ATP and 1 is used to make glucose and other carbohydrates.'),
       ('Explain how chemiosmosis produces ATP in chloroplasts.', 'The electron transport chain uses energy from excited electrons to pump protons from the stroma into the thylakoid lumen; photolysis adds protons; the gradient drives protons back through ATP synthase into the stroma, phosphorylating ADP.')],
  contrast=[('the light-dependent reactions', 'the light-independent reactions', 'Light-dependent reactions occur in thylakoid membranes, need light, split water, release O₂ and produce ATP and NADPH; light-independent reactions occur in the stroma, use ATP and NADPH to fix and reduce CO₂ into triose phosphate.'),
            ('cyclic photophosphorylation', 'non-cyclic photophosphorylation', 'In cyclic photophosphorylation electrons from PSI return to the ETC, producing ATP only; in non-cyclic, electrons flow from water through PSII and PSI to NADP, producing ATP, NADPH and O₂.')],
  misc=[('The light-independent reactions happen only at night.', 'They occur in the light (they need ATP and NADPH from the light-dependent reactions); they are “light-independent” because they do not use light directly.'),
        ('The oxygen released in photosynthesis comes from carbon dioxide.', 'Oxygen comes from the photolysis of water.'),
        ('Glucose is the direct product of the Calvin cycle.', 'The direct product is triose phosphate; glucose and other carbohydrates are made from it.')],
  cases=[('Melvin Calvin’s “lollipop” apparatus experiments (1950s)', 'Chlorella was given ¹⁴CO₂ for seconds, then killed in hot methanol; compounds were separated by chromatography.', 'the light-independent reactions', 'Labelled carbon appeared first in GP, then triose phosphate and RuBP, revealing the order of reactions in the cycle.'),
         ('Ruben and Kamen’s experiments with ¹⁸O (1941)', 'When water contained ¹⁸O, the oxygen released was labelled; when CO₂ was labelled it was not.', 'photolysis', 'Isotope labelling showed the oxygen released comes from water.')],
  evaluate=[('Improving RuBisCO is the best way to increase crop yields.', ['RuBisCO is slow and also reacts with oxygen (photorespiration), wasting energy', 'engineering faster or more CO₂-specific RuBisCO could raise efficiency'], ['yields are often limited by water, nutrients or light capture instead', 'RuBisCO is hard to engineer without losing specificity; other approaches (C4 rice, better canopy) may be easier'], 'RuBisCO is a major bottleneck, but yield depends on many factors; improving it is one promising approach among several.')],
  extended=[('Explain how light energy is converted into chemical energy in the chloroplast.', 'Photosystems absorb light; excited electrons; ETC; proton pumping into lumen; photolysis O₂; ATP synthase chemiosmosis; NADP reduced; Calvin cycle: RuBisCO fixes CO₂ to RuBP, GP reduced to TP with ATP/NADPH; RuBP regenerated; glucose/starch; locations.', 8)],
  )


@R.add('ch02-st4', 'C3', (1, 5), 'numerical')
def calvin_count(rng, slot):
    n = pick(rng, [1, 2, 3, 5, 10])
    f = rng.randrange(3)
    if f == 0:
        return num(f'Calculate the number of CO₂ molecules fixed, turns of the Calvin cycle and molecules of ATP and NADPH used to produce {n} glucose molecule{"s" if n > 1 else ""}.',
                   f'{6 * n} CO₂; {6 * n} turns; {18 * n} ATP; {12 * n} NADPH', f'6 CO₂ and 6 turns per glucose (A1); 18 ATP and 12 NADPH per glucose (A1); × {n} (A1).', 3)
    if f == 1:
        c = pick(rng, [3, 6, 9, 12, 15, 30])
        return num(f'In the Calvin cycle {c} molecules of CO₂ are fixed. State the number of GP molecules formed and the number of triose phosphate molecules available for making carbohydrates (not used to regenerate RuBP).',
                   f'{2 * c} GP; {c // 3} triose phosphate', f'Each CO₂ + RuBP → 2 GP: {2 * c} (A1); {2 * c} TP formed, 5/6 recycled → {c // 3} available (A1).', 2)
    stem = f'A plant fixes {6 * n} molecules of CO₂. Calculate the number of RuBP molecules that combine with CO₂ and explain why the Calvin cycle needs more ATP than NADPH.'
    return num(stem, f'{6 * n} RuBP; ATP is used both to reduce GP and to regenerate RuBP, NADPH only for reduction', f'One RuBP per CO₂: {6 * n} (A1); 2 ATP + 2 NADPH per CO₂ for reduction, plus 1 ATP per CO₂ for RuBP regeneration (R1 A1).', 3)


S('ch02-st5',
  terms=[('limiting factor', 'the factor that is in shortest supply relative to need and therefore limits the rate of a process'),
         ('light compensation point', 'the light intensity at which the rate of photosynthesis equals the rate of respiration, so there is no net gas exchange'),
         ('carbon dioxide enrichment', 'increasing the CO₂ concentration in a greenhouse to increase the rate of photosynthesis and crop yield'),
         ('free-air carbon dioxide enrichment (FACE)', 'field experiments in which CO₂ is released around plants in the open to study the effects of future CO₂ levels'),
         ('saturation point', 'the value of a factor above which further increases do not increase the rate of photosynthesis because another factor is limiting')],
  facts=[('Which three factors commonly limit the rate of photosynthesis?', 'light intensity, CO₂ concentration and temperature', ['oxygen, nitrogen and water', 'soil pH, wind and humidity', 'glucose, starch and chlorophyll'], 'Each can be limiting.'),
         ('Why do greenhouse growers burn paraffin heaters?', 'to raise both temperature and CO₂ concentration', ['to add oxygen', 'to lower humidity', 'to kill pollinators'], 'Combustion produces CO₂ and heat.'),
         ('What is the typical CO₂ concentration used in greenhouse enrichment?', 'about 800–1000 ppm', ['about 40 ppm', 'about 10 000 ppm', 'about 0 ppm'], 'Atmospheric is about 420 ppm.'),
         ('Which method measures the rate of photosynthesis of pondweed?', 'counting bubbles or collecting O₂ released per minute', ['weighing the pondweed', 'measuring the pH only', 'counting chloroplasts'], 'O₂ production indicates rate.')],
  mc2=[('Why does increasing light intensity beyond a certain point not increase the rate of photosynthesis?', 'Another factor such as CO₂ concentration or temperature becomes limiting.', ['Light damages all chlorophyll.', 'Stomata close in light.', 'Respiration stops.'], 'Plateau indicates another limiting factor.'),
       ('Why does temperature limit photosynthesis mainly through the Calvin cycle?', 'The light-independent reactions are enzyme-controlled.', ['Light reactions are enzyme-controlled only.', 'Temperature changes light intensity.', 'Chlorophyll melts.'], 'RuBisCO is temperature-sensitive.'),
       ('Why might FACE experiments give smaller yield increases than greenhouse experiments?', 'In the field other factors such as nitrogen and water often limit growth.', ['CO₂ is not used outdoors.', 'Plants cannot absorb CO₂ in wind.', 'Greenhouses have less light.'], 'Realistic conditions.')],
  mc3=[('A lamp is moved from 20 cm to 10 cm from pondweed. By what factor does light intensity increase?', '4', ['2', '0.5', '0.25'], 'Light intensity ∝ 1/d²: (20/10)² = 4.'),
       ('Raising CO₂ in a tomato greenhouse from 400 to 1000 ppm increased yield from 48 to 60 kg m⁻². What is the percentage increase?', '25 %', ['20 %', '12 %', '150 %'], '(60 − 48)/48 × 100 = 25 %.')],
  why=[('Explain the concept of limiting factors in photosynthesis.', 'The rate of photosynthesis is limited by whichever factor is in shortest supply (light, CO₂ or temperature); increasing that factor increases the rate until another becomes limiting, giving a plateau; only increasing the new limiting factor raises the rate further.'),
       ('Explain why greenhouse growers enrich the air with carbon dioxide.', 'In bright, warm greenhouses CO₂ concentration is often the limiting factor; increasing it to about 1000 ppm increases the rate of the Calvin cycle (more RuBP carboxylation), so more carbohydrate is made and yields rise; growers must balance the cost with the extra yield.'),
       ('Explain how the rate of photosynthesis of pondweed can be investigated in relation to light intensity.', 'Place Elodea in sodium hydrogencarbonate solution at constant temperature; vary distance from a lamp (intensity ∝ 1/d²); allow acclimatisation; count bubbles or collect O₂ in a capillary per minute; repeat at each distance.')],
  contrast=[('a light-limited rate', 'a CO₂-limited rate', 'When light is limiting, increasing light raises the rate while increasing CO₂ has little effect; when CO₂ is limiting, increasing CO₂ raises the rate while extra light has little effect.')],
  misc=[('Increasing light intensity always increases the rate of photosynthesis.', 'Only while light is the limiting factor; beyond saturation, CO₂ or temperature limits the rate.'),
        ('Plants photosynthesise faster the hotter it gets.', 'Above the optimum temperature enzymes such as RuBisCO denature and photorespiration increases, so the rate falls.'),
        ('Doubling the distance of a lamp halves the light intensity.', 'Light intensity is inversely proportional to the square of distance, so doubling distance reduces intensity to a quarter.')],
  cases=[('tomato growers in the Netherlands using CO₂ enrichment', 'Greenhouses are enriched to about 800–1000 ppm CO₂ using waste CO₂ from industry or heaters.', 'carbon dioxide as a limiting factor', 'In bright, warm conditions CO₂ limits photosynthesis, so raising it increases yields.'),
         ('FACE experiments on wheat and rice', 'Crops grown in open-air CO₂ at about 550 ppm showed yield increases of only about 10–15 %, less than in chambers.', 'limiting factors in the field', 'Other factors such as nitrogen, water and temperature limit the response to CO₂ in real conditions.')],
  evaluate=[('Rising atmospheric CO₂ will greatly increase global crop yields.', ['CO₂ is often limiting, and FACE trials show some yield increase in C3 crops', 'higher CO₂ improves water-use efficiency as stomata close partially'], ['FACE increases are smaller than expected and lower the protein and mineral content of grain', 'higher temperatures, droughts and floods linked to climate change will reduce yields'], 'CO₂ fertilisation gives modest gains that are likely to be outweighed by the negative effects of climate change, so large yield increases are unlikely.')],
  extended=[('Explain how light intensity, CO₂ concentration and temperature limit the rate of photosynthesis, and evaluate the use of CO₂ enrichment in greenhouses.', 'Limiting factor concept; graphs and plateaus; light → light-dependent reactions; CO₂ → RuBisCO fixation; temperature → enzymes, denaturation; inverse square law; greenhouses: CO₂ 1000 ppm, cost vs yield, heating, lighting; FACE results; other limits.', 8)],
  )


def _elodea_dq(rng, slot):
    ds = [10, 15, 20, 30, 40, 50]
    k = rng.uniform(4500, 6500)
    vmax = rng.uniform(45, 60)
    rel = [10000 / d ** 2 for d in ds]
    rates = [round(vmax * r / (r + k / 100), 0) for r in rel]
    j = rng.randrange(1, 5)
    intro = ('Pondweed (Elodea) was placed in 1 % sodium hydrogencarbonate solution at 25 °C. A lamp was placed at different distances and the number of bubbles released per minute was counted.\n\n'
             + table(['Distance / cm', 'Relative light intensity (1/d² × 10⁴)', 'Bubbles per minute'], [(d, '?' if i == j else f'{r:.1f}', f'{b:.0f}') for i, (d, r, b) in enumerate(zip(ds, rel, rates))]))
    pc = pct_change(rates[-1], rates[0])
    parts = [
        (f'Calculate the relative light intensity at {ds[j]} cm.', f'{rel[j]:.1f}', f'10⁴/{ds[j]}² = {rel[j]:.1f} (A1).', 1),
        ('Calculate the percentage increase in bubble rate from 50 cm to 10 cm.', f'{pc:.0f} %', f'({rates[0]:.0f} − {rates[-1]:.0f})/{rates[-1]:.0f} × 100 (M1) = {pc:.0f} % (A1).', 2),
        ('Describe the relationship between light intensity and the rate of photosynthesis.', 'Rate increases with light intensity, steeply at low intensities, then levels off at high intensities.', 'Positive relationship (A1); levelling off (A1).', 2),
        ('Explain why the rate levels off at high light intensity.', 'Another factor, such as CO₂ concentration or temperature, becomes limiting.', 'Another limiting factor named (A1); light no longer limiting (R1).', 2),
        ('Explain why sodium hydrogencarbonate solution was used.', 'It provides a supply of CO₂ (as hydrogencarbonate ions) so CO₂ is not limiting at low light.', 'Source of CO₂ (A1).', 1),
        ('Suggest two limitations of counting bubbles to measure the rate.', 'Bubbles vary in size; some O₂ dissolves; bubbles may contain other gases; counting errors at high rates.', 'Two valid limitations (A1 A1).', 2),
        ('Suggest how the effect of the lamp’s heat could be prevented from affecting results.', 'Place a heat filter / beaker of water between lamp and plant, use an LED, or monitor temperature with a thermometer.', 'Valid method (A1).', 1),
        ('Suggest how the investigation could be modified to show that CO₂ concentration can become limiting.', 'Repeat at the highest light intensity with different NaHCO₃ concentrations, keeping temperature constant; the rate should increase with CO₂ concentration.', 'Vary NaHCO₃ at high light (A1); control of temperature/expected result (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch02-st5', _elodea_dq)

pct_items(R, 'ch02-st5', [
    ('Raising the CO₂ concentration in a cucumber greenhouse increased the yield from {a} kg m⁻² to {b} kg m⁻².', 'kg m⁻²', 30, 60, 0.12, 0.35, 1, 'CO₂ was the limiting factor, so more CO₂ increased the rate of carbon fixation by RuBisCO.'),
    ('In a FACE experiment, wheat grain yield changed from {a} t ha⁻¹ at ambient CO₂ to {b} t ha⁻¹ at elevated CO₂.', 't ha⁻¹', 4.0, 7.5, 0.06, 0.16, 2, 'more CO₂ increased photosynthesis, but other factors such as nitrogen limited the response.'),
    ('The rate of oxygen production by an alga changed from {a} to {b} µmol h⁻¹ when the temperature was raised from 25 °C to 40 °C.', 'µmol h⁻¹', 20, 60, -0.6, -0.2, 1, 'above the optimum, enzymes of the Calvin cycle denature and photorespiration rises.'),
])


# =============================================================================================
# ch03 C2.1 Chemical signalling and C2.2 Neural signalling
# =============================================================================================
S('ch03-st1',
  terms=[('receptor', 'a protein with a binding site for a specific signalling chemical (ligand), which changes shape when the ligand binds'),
         ('ligand', 'a signalling chemical that binds specifically to a receptor'),
         ('hormone', 'a signalling chemical secreted by endocrine glands into the blood and transported to target cells elsewhere in the body'),
         ('neurotransmitter', 'a signalling chemical released from a presynaptic neurone that diffuses across a synapse to bind to receptors on a postsynaptic cell'),
         ('quorum sensing', 'a process in bacteria in which signalling molecules accumulate as population density increases, triggering coordinated gene expression'),
         ('cytokine', 'a small protein signalling molecule, especially in the immune system, that acts locally on nearby cells')],
  facts=[('Which bacterium uses quorum sensing to control bioluminescence?', 'Vibrio fischeri', ['Escherichia coli only', 'Streptococcus pneumoniae', 'Thermus aquaticus'], 'Light is produced only at high population density.'),
         ('Where are receptors for steroid hormones usually located?', 'inside the cell (cytoplasm or nucleus)', ['on the outer surface of the plasma membrane', 'in the cell wall', 'in the blood'], 'Steroids cross the membrane.'),
         ('Which is a neurotransmitter?', 'acetylcholine', ['insulin', 'oestradiol', 'thyroxine'], 'Released at synapses.'),
         ('Which signalling chemical is a steroid hormone?', 'testosterone', ['insulin', 'adrenaline', 'glucagon'], 'Steroids are lipids.'),
         ('Which type of molecule are most receptors?', 'proteins', ['carbohydrates', 'lipids', 'nucleic acids'], 'Shape allows specific binding.')],
  mc2=[('Why can insulin not cross the plasma membrane but oestradiol can?', 'Insulin is a large polar protein; oestradiol is a small lipid-soluble steroid.', ['Insulin is a steroid.', 'Oestradiol is a protein.', 'Both cross freely.'], 'Lipid solubility determines membrane crossing.'),
       ('Why do hormones affect only target cells even though they circulate everywhere?', 'Only target cells have receptors with complementary binding sites.', ['Hormones are destroyed in non-target cells.', 'Hormones only enter target organs.', 'All cells respond to all hormones.'], 'Specificity of receptors.'),
       ('Why is quorum sensing advantageous to Vibrio fischeri?', 'Light is produced only when enough bacteria are present to make it visible and useful.', ['It saves light for night.', 'It prevents reproduction.', 'It kills competitors.'], 'Coordinated behaviour saves energy.'),
       ('How do neurotransmitters differ from hormones in the distance they act over?', 'Neurotransmitters act across a synapse (nanometres); hormones travel in blood throughout the body.', ['Neurotransmitters travel in blood.', 'Hormones act only across synapses.', 'Both act over the same distance.'], 'Local vs long distance.')],
  mc3=[('A drug binds to adrenaline receptors without activating them. What effect would it have?', 'It would block the response to adrenaline (antagonist).', ['It would increase the response to adrenaline.', 'It would produce adrenaline.', 'It would have no effect at all.'], 'Beta blockers work like this.'),
       ('In the Hawaiian bobtail squid, Vibrio fischeri glow only in the light organ, not in seawater. Which explanation fits?', 'Bacterial density and autoinducer concentration are high only in the light organ.', ['Seawater kills them.', 'The squid makes the light.', 'Light is produced by the squid’s eyes.'], 'Quorum sensing depends on density.')],
  why=[('Explain how quorum sensing allows bacteria to coordinate behaviour.', 'Each bacterium secretes a signalling molecule (autoinducer); as population density increases its concentration rises; above a threshold it binds receptors and alters gene expression in all cells, e.g. switching on luciferase genes in Vibrio fischeri.'),
       ('Explain the differences between transmembrane receptors and intracellular receptors.', 'Transmembrane receptors bind hydrophilic ligands (e.g. insulin, adrenaline) at the cell surface and pass the signal inside via transduction; intracellular receptors in the cytoplasm/nucleus bind hydrophobic ligands (e.g. steroids) that cross the membrane, and often act directly as transcription factors.'),
       ('Explain why the binding of a ligand to a receptor is specific and reversible.', 'The binding site has a shape and chemistry complementary to the ligand; binding is by weak non-covalent interactions, so the ligand can detach and the signal can be terminated when ligand concentration falls.')],
  contrast=[('hormones', 'neurotransmitters', 'Hormones are secreted into the blood by endocrine glands and act on distant target cells, usually slowly and for longer; neurotransmitters are released at synapses and act across a tiny gap, rapidly and briefly.'),
            ('transmembrane receptors', 'intracellular receptors', 'Transmembrane receptors span the membrane and bind hydrophilic signals outside; intracellular receptors are inside the cell and bind hydrophobic signals such as steroids.')],
  misc=[('All hormones must enter cells to have an effect.', 'Protein/peptide hormones such as insulin bind to receptors on the cell surface and act through signal transduction without entering.'),
        ('Bacteria cannot communicate because they are single-celled.', 'Bacteria communicate by quorum sensing using secreted signalling chemicals.'),
        ('A receptor permanently binds its ligand.', 'Ligand–receptor binding is reversible, allowing signals to be switched off.')],
  cases=[('bioluminescence of Vibrio fischeri in the Hawaiian bobtail squid', 'At high density in the squid’s light organ, autoinducer accumulates and switches on lux genes, producing light that camouflages the squid.', 'quorum sensing', 'Signal concentration reflects population density, so gene expression is coordinated only when enough bacteria are present.'),
         ('beta blockers prescribed for high blood pressure', 'The drugs bind to β-adrenergic receptors in the heart without activating them.', 'receptor–ligand specificity', 'By occupying the receptors they block adrenaline binding and reduce heart rate.')],
  evaluate=[('Chemical signalling is a more effective method of communication than neural signalling.', ['hormones reach all cells with receptors and give long-lasting coordinated responses (e.g. growth)', 'chemical signalling is universal, even in bacteria'], ['neural signalling is much faster and more precisely targeted', 'many responses need both, e.g. adrenaline release by nerves'], 'Each is effective for different purposes: chemical signals for widespread, sustained responses and nerves for rapid, precise ones.')],
  extended=[('Describe the different types of signalling chemicals and explain how receptors allow cells to respond to them.', 'Types: hormones (peptide/steroid/amine), neurotransmitters, cytokines, calcium ions; quorum sensing autoinducers in bacteria. Receptors: specific proteins, complementary binding, reversible; transmembrane (insulin, adrenaline, acetylcholine) vs intracellular (steroids); localised vs distant effects; specificity of target cells.', 8)],
  )

S('ch03-st2',
  terms=[('signal transduction', 'the series of events by which a signal received by a receptor is converted into a response inside the cell'),
         ('G-protein-coupled receptor', 'a transmembrane receptor that, when a ligand binds, activates a G protein inside the cell, which then activates other proteins'),
         ('second messenger', 'a small molecule such as cyclic AMP that relays a signal from a receptor to targets inside the cell'),
         ('tyrosine kinase receptor', 'a transmembrane receptor that, when bound by a ligand such as insulin, phosphorylates tyrosine residues, starting a signalling cascade'),
         ('signalling cascade', 'a sequence of reactions in which each activated protein activates many molecules of the next, amplifying the signal')],
  facts=[('Which second messenger is produced when adrenaline binds to its G-protein-coupled receptor in liver cells?', 'cyclic AMP', ['insulin', 'glucose', 'ATP synthase'], 'Adenylyl cyclase converts ATP to cAMP.'),
         ('Which hormone acts through a tyrosine kinase receptor?', 'insulin', ['adrenaline', 'oestradiol', 'testosterone'], 'Insulin receptors autophosphorylate.'),
         ('What does an activated G protein bind?', 'GTP', ['ATP', 'cAMP', 'glucose'], 'GDP is exchanged for GTP.'),
         ('What is one response of muscle and fat cells to insulin signalling?', 'vesicles containing GLUT4 transporters fuse with the plasma membrane', ['glucose is released into the blood', 'glycogen is broken down', 'the cell divides'], 'More glucose uptake.')],
  mc2=[('Why does a signalling cascade amplify a signal?', 'Each activated enzyme activates many molecules of the next component.', ['Each step destroys the signal.', 'Only one molecule is activated at each step.', 'The ligand enters the cell.'], 'One hormone molecule can lead to millions of product molecules.'),
       ('Why is signal transduction needed for adrenaline but not for oestradiol?', 'Adrenaline is hydrophilic and cannot cross the membrane, so its signal must be relayed inside.', ['Oestradiol is hydrophilic.', 'Adrenaline enters the nucleus.', 'Oestradiol has no receptor.'], 'Surface vs intracellular receptors.'),
       ('How is a G-protein signal switched off?', 'The G protein hydrolyses GTP to GDP and becomes inactive.', ['The receptor is destroyed.', 'cAMP is converted to adrenaline.', 'The cell dies.'], 'Intrinsic GTPase activity.')],
  mc3=[('A mutation causes a G protein to remain permanently bound to GTP. What is the likely effect?', 'The signalling pathway stays switched on even without the ligand.', ['The pathway can never be activated.', 'The receptor is destroyed.', 'cAMP levels fall to zero.'], 'Cholera toxin has a similar effect.'),
       ('Each adrenaline receptor activates 10 G proteins, and each adenylyl cyclase produces 100 cAMP. How many cAMP result from one receptor (assuming each G protein activates one adenylyl cyclase)?', '1000', ['110', '10', '100'], '10 × 100 = 1000 – amplification.')],
  why=[('Explain how adrenaline triggers glycogen breakdown in liver cells.', 'Adrenaline binds to a G-protein-coupled receptor on the surface; the receptor activates a G protein (GDP replaced by GTP); the G protein activates adenylyl cyclase, which converts ATP to cAMP (second messenger); cAMP activates protein kinase A, starting a cascade that activates glycogen phosphorylase; glycogen is hydrolysed to glucose.'),
       ('Explain how insulin signals through a tyrosine kinase receptor.', 'Insulin binds to the extracellular part of the receptor; the receptor subunits phosphorylate tyrosine residues on each other (autophosphorylation); relay proteins bind and are activated, starting a cascade; vesicles with GLUT4 move to and fuse with the membrane, increasing glucose uptake.')],
  contrast=[('G-protein-coupled receptors', 'tyrosine kinase receptors', 'GPCRs activate a G protein, which activates enzymes producing second messengers such as cAMP (e.g. adrenaline); tyrosine kinase receptors phosphorylate tyrosines on themselves when the ligand binds, activating relay proteins (e.g. insulin).')],
  misc=[('Adrenaline enters liver cells and breaks down glycogen directly.', 'Adrenaline binds to a surface receptor; the signal is relayed by a G protein and cAMP, which activate enzymes that break down glycogen.'),
        ('A signal is weakened at each step of a cascade.', 'Signalling cascades amplify the signal: each activated molecule activates many of the next.')],
  cases=[('cholera toxin', 'The toxin modifies a G protein in intestinal cells so it remains active, raising cAMP and causing massive loss of water and ions.', 'G-protein signalling', 'Failure to switch off the G protein keeps the pathway on, showing the importance of signal termination.'),
         ('type 2 diabetes and insulin resistance', 'Target cells respond poorly to insulin even though insulin is present.', 'tyrosine kinase signalling', 'Defects in the receptor or downstream pathway reduce GLUT4 movement to the membrane, so glucose uptake is reduced.')],
  evaluate=[('Signal transduction pathways are good targets for new drugs.', ['many drugs target GPCRs and kinases, e.g. beta blockers and kinase inhibitors in cancer', 'cascades offer several points of control'], ['pathways are shared by many cell types, so drugs may have side effects', 'cells can bypass blocked steps, leading to resistance'], 'They are excellent targets and many drugs act on them, but specificity and resistance are major challenges.')],
  extended=[('Compare the signal transduction pathways of adrenaline and insulin.', 'Both bind surface receptors; adrenaline: GPCR, G protein, GTP, adenylyl cyclase, cAMP, PKA cascade, glycogen breakdown; insulin: tyrosine kinase, autophosphorylation, relay proteins, GLUT4 vesicles fuse, glucose uptake; amplification; termination.', 8)],
  )


@R.add('ch03-st2', 'C3', (2, 5), 'numerical')
def amplification(rng, slot):
    a = pick(rng, [5, 10, 20, 50])
    b = pick(rng, [10, 50, 100, 200])
    c = pick(rng, [10, 100, 500, 1000])
    stem = (f'In a liver cell, one adrenaline–receptor complex activates {a} G proteins; each activates one adenylyl cyclase molecule, which produces {b} cAMP molecules; each cAMP (via protein kinase A) leads to activation of enzymes '
            f'that release {c} glucose molecules from glycogen. Calculate the number of glucose molecules released per receptor activated and explain the significance of this.')
    tot = a * b * c
    return num(stem, f'{tot:,} glucose molecules'.replace(',', ' ') + '; amplification gives a large, rapid response to a small amount of hormone',
               f'{a} × {b} × {c} (M1) = {tot:,} (A1); amplification by cascade – small hormone concentration gives large response (R1).'.replace(',', ' '), 3)


def _glut4_dq(rng, slot):
    ins = [0, 0.1, 1, 10, 100]
    vmax = rng.uniform(9, 14)
    base = rng.uniform(1.0, 1.8)
    ec_n = rng.uniform(0.6, 1.2)
    ec_r = ec_n * rng.uniform(6, 12)
    red = rng.uniform(0.5, 0.7)
    norm = [round(base + vmax * i / (ec_n + i), 1) for i in ins]
    res = [round(base + red * vmax * i / (ec_r + i), 1) for i in ins]
    intro = ('Glucose uptake (nmol per mg protein per min) was measured in fat cells (adipocytes) taken from people with normal insulin sensitivity and from people with insulin resistance, '
             'at different insulin concentrations.\n\n'
             + table(['Insulin / nmol dm⁻³', 'Uptake – normal', 'Uptake – insulin resistant'], [(i, a, b) for i, a, b in zip(ins, norm, res)]))
    fn = norm[-1] / norm[0]
    p = pct_change(norm[2], res[2])
    parts = [
        ('State the glucose uptake by normal cells at 1 nmol dm⁻³ insulin.', f'{norm[2]} nmol mg⁻¹ min⁻¹', f'{norm[2]} (A1).', 1),
        ('Calculate how many times greater the uptake by normal cells is at 100 nmol dm⁻³ insulin than with no insulin.', f'{fn:.1f} times', f'{norm[-1]}/{norm[0]} = {fn:.1f} (A1).', 1),
        ('Calculate the percentage difference in uptake of insulin-resistant cells compared with normal cells at 1 nmol dm⁻³ insulin.', f'{signed(p)} %', f'({res[2]} − {norm[2]})/{norm[2]} × 100 (M1) = {signed(p)} % (A1).', 2),
        ('Compare the responses of the two types of cell to insulin.', 'Both show increasing uptake with insulin that levels off; resistant cells have similar uptake without insulin but lower uptake at every insulin concentration and need higher insulin for a response.', 'Similarity (A1); two differences (A1 A1).', 3),
        ('Explain how insulin binding increases glucose uptake by adipocytes.', 'Insulin binds a tyrosine kinase receptor; autophosphorylation activates relay proteins/cascade; vesicles containing GLUT4 move to and fuse with the plasma membrane; more glucose transporters, more facilitated diffusion of glucose.', 'Receptor/tyrosine kinase (A1); cascade (A1); GLUT4 to membrane (A1).', 3),
        ('Suggest why uptake levels off at high insulin concentrations.', 'All insulin receptors are occupied / all GLUT4 vesicles have been inserted, so transport is at maximum capacity.', 'Receptor or transporter saturation (A1).', 1),
        ('Suggest one reason for the reduced response of insulin-resistant cells.', 'Fewer receptors, defective receptor or relay proteins, fewer GLUT4 transporters or reduced vesicle movement.', 'Any valid reason (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch03-st2', _glut4_dq)


S('ch03-st3',
  terms=[('resting potential', 'the potential difference of about −70 mV across the membrane of a neurone that is not transmitting an impulse'),
         ('action potential', 'a rapid depolarisation and repolarisation of a section of neurone membrane, which propagates along the axon as a nerve impulse'),
         ('depolarisation', 'a change in membrane potential from negative towards positive, caused by Na⁺ ions diffusing into the axon'),
         ('repolarisation', 'the return of membrane potential to a negative value, caused by K⁺ ions diffusing out of the axon'),
         ('threshold potential', 'the membrane potential (about −50 to −55 mV) that must be reached for voltage-gated sodium channels to open and an action potential to start'),
         ('myelin sheath', 'layers of plasma membrane of Schwann cells wrapped around an axon, which insulate it and allow saltatory conduction'),
         ('saltatory conduction', 'conduction of a nerve impulse by jumping from one node of Ranvier to the next along a myelinated axon'),
         ('node of Ranvier', 'a short gap in the myelin sheath where the axon membrane is exposed and action potentials occur')],
  facts=[('What is the typical resting potential of a neurone?', '−70 mV', ['+70 mV', '0 mV', '−7 mV'], 'Inside negative relative to outside.'),
         ('How many ions does the sodium–potassium pump move in each cycle?', '3 Na⁺ out and 2 K⁺ in', ['2 Na⁺ out and 3 K⁺ in', '3 K⁺ out and 2 Na⁺ in', '1 Na⁺ out and 1 K⁺ in'], 'Uses one ATP per cycle.'),
         ('Which cells form the myelin sheath of peripheral neurones?', 'Schwann cells', ['red blood cells', 'osteocytes', 'goblet cells'], 'They wrap around the axon.'),
         ('What is the approximate maximum conduction speed in myelinated human axons?', 'about 100 m s⁻¹', ['about 1 mm s⁻¹', 'about 1 m s⁻¹', 'about 3 × 10⁸ m s⁻¹'], 'Unmyelinated axons conduct at about 1 m s⁻¹.'),
         ('Which ions diffuse into the axon during depolarisation?', 'sodium ions', ['potassium ions', 'chloride ions', 'calcium ions'], 'Voltage-gated Na⁺ channels open.'),
         ('Which instrument is used to display action potentials?', 'an oscilloscope (with microelectrodes)', ['a spirometer', 'a potometer', 'a colorimeter'], 'Shows potential against time.')],
  mc2=[('Why is the inside of a resting axon negative relative to the outside?', 'The Na⁺/K⁺ pump moves more positive ions out than in, and the membrane is more permeable to K⁺, which leaks out.', ['Negative ions are pumped in.', 'Sodium leaks in faster than potassium leaks out.', 'Proteins inside are positively charged.'], 'Pump plus K⁺ leakage.'),
       ('Why does an action potential travel in one direction only along an axon?', 'The region behind the impulse is in its refractory period, with Na⁺ channels inactivated.', ['Myelin blocks one direction.', 'Ions only flow towards the cell body.', 'The axon is tapered.'], 'Refractory period.'),
       ('Why do myelinated axons conduct faster than unmyelinated axons of the same diameter?', 'Depolarisation occurs only at nodes of Ranvier, so the impulse jumps between nodes.', ['Myelin carries ions along the axon.', 'Myelinated axons have more sodium channels along their whole length.', 'Myelin conducts electricity like a wire.'], 'Saltatory conduction.'),
       ('Why does the membrane potential briefly become more negative than −70 mV after an action potential?', 'Voltage-gated K⁺ channels are slow to close, so excess K⁺ leaves (hyperpolarisation).', ['Na⁺ continues to enter.', 'The pump stops.', 'Chloride ions leave.'], 'Overshoot of repolarisation.'),
       ('Why does a stronger stimulus not produce a bigger action potential?', 'Action potentials are all-or-nothing; stimulus strength is coded by frequency of impulses.', ['Larger stimuli open fewer channels.', 'Action potentials are graded.', 'Myelin limits the size.'], 'All-or-nothing principle.')],
  mc3=[('An impulse travels 0.60 m from the spinal cord to a toe in 8.0 ms. What is the conduction speed?', '75 m s⁻¹', ['4.8 m s⁻¹', '0.075 m s⁻¹', '13 m s⁻¹'], 'Speed = 0.60/0.0080 = 75 m s⁻¹.'),
       ('A toxin blocks voltage-gated sodium channels. What is the effect on neurones?', 'No action potentials can be generated, so impulses are not conducted.', ['The resting potential becomes +40 mV.', 'Impulses travel faster.', 'Repolarisation cannot occur but depolarisation can.'], 'Tetrodotoxin from pufferfish acts like this.'),
       ('In multiple sclerosis the myelin sheath is damaged. Which effect is expected?', 'Slower or failed conduction of impulses along affected axons.', ['Faster conduction.', 'No change because myelin is not needed.', 'Increased resting potential.'], 'Loss of saltatory conduction.')],
  why=[('Explain how a resting potential is established and maintained.', 'The Na⁺/K⁺ pump uses ATP to pump 3 Na⁺ out and 2 K⁺ in; the membrane is more permeable to K⁺ (leak channels), so K⁺ diffuses out; negatively charged proteins remain inside; result is about −70 mV inside relative to outside.'),
       ('Explain the events of an action potential.', 'A stimulus depolarises the membrane to threshold; voltage-gated Na⁺ channels open and Na⁺ diffuses in, making the inside positive (about +30 mV); Na⁺ channels close and voltage-gated K⁺ channels open; K⁺ diffuses out (repolarisation); slight hyperpolarisation; resting potential restored by the pump.'),
       ('Explain how an action potential is propagated along an axon.', 'Na⁺ entering at the depolarised region diffuses along inside the axon (local currents) to the next region, depolarising it to threshold; voltage-gated channels open there; the refractory region behind prevents backward propagation.'),
       ('Explain the factors that affect the speed of conduction of nerve impulses.', 'Myelination: saltatory conduction between nodes greatly increases speed; larger axon diameter reduces resistance and increases speed (e.g. giant squid axon); higher temperature increases ion diffusion speed in ectotherms.')],
  contrast=[('myelinated axons', 'unmyelinated axons', 'Myelinated axons conduct by saltatory conduction at up to about 100 m s⁻¹, with action potentials only at nodes of Ranvier; unmyelinated axons depolarise every part of the membrane and conduct at about 1 m s⁻¹.'),
            ('depolarisation', 'repolarisation', 'Depolarisation is caused by Na⁺ moving in through voltage-gated Na⁺ channels, making the inside positive; repolarisation is caused by K⁺ moving out through voltage-gated K⁺ channels, making the inside negative again.')],
  misc=[('During an action potential sodium ions are pumped into the axon.', 'Na⁺ ions diffuse in through voltage-gated channels; the pump moves Na⁺ out.'),
        ('The myelin sheath conducts the nerve impulse.', 'Myelin is an insulator; the impulse jumps between gaps in the myelin (nodes of Ranvier).'),
        ('A stronger stimulus produces larger action potentials.', 'Action potentials are all-or-nothing and always the same size; a stronger stimulus increases their frequency.'),
        ('Nerve impulses are electrons flowing along the axon like a current in a wire.', 'Impulses are waves of depolarisation caused by movement of Na⁺ and K⁺ ions across the membrane.')],
  cases=[('the giant axon of the squid', 'Unmyelinated axons up to 1 mm in diameter conduct impulses at about 25 m s⁻¹ for the escape response.', 'the effect of axon diameter on conduction speed', 'Large diameter reduces resistance to local currents, increasing speed without myelin.'),
         ('multiple sclerosis', 'The immune system damages myelin in the brain and spinal cord, causing problems with movement and vision.', 'the role of myelination', 'Without myelin, saltatory conduction fails, so impulses slow or are blocked.'),
         ('tetrodotoxin from pufferfish', 'The toxin binds to voltage-gated sodium channels, causing paralysis.', 'the role of sodium channels in action potentials', 'Without Na⁺ influx, depolarisation cannot occur, so no impulses are generated.')],
  evaluate=[('Myelination was the most important adaptation for fast nerve conduction in vertebrates.', ['myelinated axons conduct up to 100 m s⁻¹ while thin and space-saving', 'allows large numbers of fast axons in the brain and spinal cord'], ['invertebrates such as squid achieve fast conduction with giant axons', 'myelin requires energy and Schwann/oligodendrocyte support and can be damaged by disease'], 'Myelination allows fast conduction in thin axons, which made complex vertebrate nervous systems possible, although giant axons are an alternative solution.'),
            ('The all-or-nothing nature of action potentials limits the information a nerve can carry.', ['each impulse is the same size, so amplitude cannot carry information'], ['information is coded by frequency of impulses and by which neurones fire', 'all-or-nothing signals do not fade with distance'], 'All-or-nothing signals are reliable over long distances and frequency coding carries information, so it is not a serious limitation.')],
  extended=[('Describe how a resting potential is maintained and explain how an action potential is generated and propagated along a myelinated axon.', 'Na⁺/K⁺ pump, 3:2, ATP; K⁺ leakage; −70 mV; stimulus to threshold; voltage-gated Na⁺ channels, influx, +30 mV; Na⁺ channels close, K⁺ channels open, efflux; hyperpolarisation; refractory period; local currents; myelin from Schwann cells insulates; nodes of Ranvier; saltatory conduction; speed.', 8),
            ('Explain how the structure of a neurone is related to its function.', 'Dendrites receive signals; cell body with nucleus and many ribosomes; long axon carries impulses over distance; myelin and nodes allow saltatory conduction; axon terminals with vesicles release neurotransmitter; membrane with pumps and voltage-gated channels.', 6)],
  )


@R.add('ch03-st3', 'C3', (1, 4), 'numerical')
def conduction_speed(rng, slot):
    who = pick(rng, [('a motor neurone from the spinal cord to a muscle in the foot', 0.8, 1.1, 50, 110), ('a sensory neurone from a fingertip to the spinal cord', 0.6, 0.9, 40, 80),
                     ('an unmyelinated C fibre carrying pain signals', 0.3, 0.9, 0.5, 2.0), ('a giant axon of a squid', 0.05, 0.15, 18, 30)])
    txt, dlo, dhi, slo, shi = who
    d = round(rng.uniform(dlo, dhi), 2)
    v = rng.uniform(slo, shi)
    t = d / v
    t_ms = round(t * 1000, 1 if t < 0.1 else 0)
    v = d / (t_ms / 1000)
    stem = f'An impulse travels {d:.2f} m along {txt} in {t_ms:g} ms. Calculate the conduction speed in m s⁻¹.'
    ans = f'{sf(v)} m s⁻¹'
    key = f'Speed = distance/time = {d:.2f} m ÷ {t_ms / 1000:g} s (M1) = {sf(v)} m s⁻¹ (A1).'
    if slot.d >= 3:
        stem += ' State, with a reason, whether the axon is likely to be myelinated.'
        my = v > 10 and 'giant' not in txt
        ans += '; ' + ('myelinated – speeds above about 10 m s⁻¹ in vertebrates indicate saltatory conduction' if my else ('unmyelinated – the squid achieves its speed by a large axon diameter' if 'giant' in txt else 'unmyelinated – speeds of about 1 m s⁻¹ are typical of unmyelinated axons'))
        key += ' Reasoned deduction (R1).'
        return num(stem, ans, key, 3)
    return num(stem, ans, key, 2)


@R.add('ch03-st3', 'C3', (1, 4), 'mcq')
def conduction_mcq(rng, slot):
    v = pick(rng, [40, 50, 60, 75, 80, 100, 120])
    d = pick(rng, [0.6, 0.8, 0.9, 1.0, 1.2])
    t = d / v * 1000
    stem = f'An impulse travels along a myelinated axon at {v} m s⁻¹. How long does it take to travel {d} m?'
    return nmcq(rng, stem, f'{sf(t)} ms', [f'{sf(t * 10)} ms', f'{sf(t / 10)} ms', f'{sf(v * d)} ms', f'{sf(v / d)} ms'], f't = d/v = {d}/{v} = {sf(t / 1000)} s = {sf(t)} ms.')


def _axon_dq(rng, slot):
    diam = [2, 5, 10, 15, 20]
    km = rng.uniform(5.2, 6.2)
    ku = rng.uniform(1.0, 1.6)
    my = [round(km * x, 0) for x in diam]
    un = [round(ku * math.sqrt(x / 2) * 0.6, 1) for x in diam]
    intro = ('The conduction speed of nerve impulses was measured in myelinated and unmyelinated axons of different diameters in a mammal.\n\n'
             + table(['Axon diameter / µm', 'Myelinated speed / m s⁻¹', 'Unmyelinated speed / m s⁻¹'], [(a, f'{b:.0f}', f'{c:.1f}') for a, b, c in zip(diam, my, un)]))
    ratio = my[2] / un[2]
    tmy = 1.0 / my[2] * 1000
    tun = 1.0 / un[2] * 1000
    parts = [
        ('State the conduction speed of a 10 µm myelinated axon.', f'{my[2]:.0f} m s⁻¹', f'{my[2]:.0f} (A1).', 1),
        ('Calculate how many times faster a 10 µm myelinated axon conducts than an unmyelinated axon of the same diameter.', f'{ratio:.0f} times', f'{my[2]:.0f}/{un[2]:.1f} = {ratio:.0f} (A1).', 1),
        ('Calculate the time taken for an impulse to travel 1.0 m along each type of 10 µm axon.', f'myelinated {tmy:.1f} ms; unmyelinated {tun:.0f} ms', f't = d/v: 1.0/{my[2]:.0f} = {tmy:.1f} ms (A1); 1.0/{un[2]:.1f} = {tun:.0f} ms (A1).', 2),
        ('Describe the effect of axon diameter on conduction speed in myelinated axons.', 'Speed increases in proportion to diameter (approximately linear relationship).', 'Positive relationship (A1); approximately proportional (A1).', 2),
        ('Explain why myelinated axons conduct faster.', 'Myelin insulates the axon; depolarisation occurs only at the nodes of Ranvier; local currents jump from node to node (saltatory conduction), so fewer depolarisations are needed.', 'Insulation (A1); nodes of Ranvier (A1); saltatory conduction (A1).', 3),
        ('Suggest an advantage to a vertebrate of having myelinated rather than giant axons.', 'Fast conduction with thin axons, so many axons can be packed into nerves and the CNS; less space and fewer resources.', 'Valid advantage (A1).', 1),
        ('Suggest why impulses in pain C fibres (unmyelinated) arrive after those in touch fibres (myelinated) from the same area of skin.', 'Unmyelinated axons conduct much more slowly, so their impulses take longer to reach the CNS.', 'Linked to conduction speed (A1).', 1),
        ('Calculate the percentage increase in conduction speed of myelinated axons from 5 µm to 20 µm diameter.', f'{signed(pct_change(my[1], my[4]))} %', f'({my[4]:.0f} − {my[1]:.0f})/{my[1]:.0f} × 100 (M1) = {signed(pct_change(my[1], my[4]))} % (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch03-st3', _axon_dq)


S('ch03-st4',
  terms=[('synapse', 'a junction between two neurones, or between a neurone and an effector cell, across which signals are passed by neurotransmitters'),
         ('synaptic cleft', 'the narrow gap (about 20 nm) between the presynaptic and postsynaptic membranes'),
         ('acetylcholinesterase', 'an enzyme in the synaptic cleft that hydrolyses acetylcholine into acetate and choline, ending its action'),
         ('excitatory postsynaptic potential', 'a small depolarisation of the postsynaptic membrane caused by an excitatory neurotransmitter'),
         ('inhibitory neurotransmitter', 'a neurotransmitter that makes the postsynaptic membrane more negative (hyperpolarised), so an action potential is less likely'),
         ('summation', 'the combined effect of several excitatory postsynaptic potentials, either from one neurone firing repeatedly (temporal) or from several neurones (spatial), to reach threshold'),
         ('nociceptor', 'a sensory receptor that detects stimuli that could damage tissue and gives the sensation of pain'),
         ('endorphins', 'natural painkillers secreted in the brain that bind to opioid receptors and block transmission of pain signals')],
  facts=[('Which ions enter the presynaptic terminal when an action potential arrives?', 'calcium ions', ['sodium ions only', 'chloride ions', 'hydrogen ions'], 'Voltage-gated Ca²⁺ channels open.'),
         ('Which products are formed when acetylcholine is hydrolysed?', 'acetate and choline', ['glucose and fructose', 'amino acids', 'dopamine and serotonin'], 'Choline is reabsorbed into the presynaptic neurone.'),
         ('How does neurotransmitter cross the synaptic cleft?', 'by diffusion', ['by active transport', 'along microtubules', 'by osmosis'], 'The gap is very narrow.'),
         ('Which pesticides bind irreversibly to acetylcholine receptors in insects?', 'neonicotinoids', ['organophosphates only', 'DDT', 'glyphosate'], 'They are not broken down by acetylcholinesterase.'),
         ('Which drug blocks the reuptake of dopamine at synapses?', 'cocaine', ['caffeine', 'aspirin', 'insulin'], 'Dopamine remains in the cleft.')],
  mc2=[('Why is transmission at a synapse one-way?', 'Neurotransmitter is released only from the presynaptic neurone and receptors are only on the postsynaptic membrane.', ['The cleft blocks backward diffusion.', 'Postsynaptic neurones have no ion channels.', 'Acetylcholinesterase is only on the presynaptic side.'], 'Vesicles are presynaptic; receptors postsynaptic.'),
       ('Why must acetylcholine be broken down rapidly in the synaptic cleft?', 'To prevent continuous stimulation of the postsynaptic membrane, so the signal is brief.', ['To make more acetylcholine.', 'To open calcium channels.', 'To speed up diffusion.'], 'Allows separate impulses to be transmitted.'),
       ('Why do neonicotinoids kill insects but have much less effect on mammals?', 'They bind much more strongly to insect acetylcholine receptors than to mammalian ones.', ['Mammals have no acetylcholine.', 'Mammals have no synapses.', 'They are broken down in insects.'], 'Receptor differences.'),
       ('Why does summation allow integration of information?', 'Whether the postsynaptic neurone fires depends on the combined excitatory and inhibitory inputs.', ['Every input causes an action potential.', 'Inhibitory inputs add to excitatory ones.', 'Only one synapse is active at a time.'], 'Neurones integrate signals.')],
  mc3=[('An insecticide inhibits acetylcholinesterase. What happens at synapses in insect muscles?', 'Acetylcholine accumulates, causing continuous stimulation and paralysis.', ['No acetylcholine is released.', 'Calcium channels close.', 'Receptors are destroyed.'], 'Organophosphates act like this.'),
       ('Each EPSP depolarises a postsynaptic neurone by 4 mV from a resting potential of −70 mV. Threshold is −55 mV. How many EPSPs must summate to start an action potential?', '4', ['3', '15', '55'], '15 mV needed; 15/4 = 3.75, so 4 EPSPs.'),
       ('A drug blocks voltage-gated calcium channels in presynaptic terminals. What is the effect?', 'Less neurotransmitter is released, so transmission is reduced.', ['More neurotransmitter is released.', 'Postsynaptic receptors are blocked.', 'Acetylcholinesterase is inhibited.'], 'Ca²⁺ triggers exocytosis.')],
  why=[('Explain the events of synaptic transmission at a cholinergic synapse.', 'Action potential arrives at presynaptic terminal; voltage-gated Ca²⁺ channels open and Ca²⁺ diffuses in; vesicles fuse with membrane (exocytosis) releasing acetylcholine; ACh diffuses across cleft and binds to receptors on the postsynaptic membrane; Na⁺ channels open, Na⁺ enters, depolarisation; ACh hydrolysed by acetylcholinesterase; choline reabsorbed.'),
       ('Explain how excitatory and inhibitory neurotransmitters affect a postsynaptic neurone.', 'Excitatory neurotransmitters open cation (Na⁺) channels, causing depolarisation (EPSP) towards threshold; inhibitory neurotransmitters open Cl⁻ or K⁺ channels, causing hyperpolarisation, making action potentials less likely; the net effect depends on summation.'),
       ('Explain how pain is perceived and how endorphins reduce it.', 'Nociceptors (free nerve endings) are stimulated by damaging heat, pressure or chemicals; impulses pass via sensory neurones to the spinal cord and brain, where pain is perceived in the cerebral cortex; endorphins bind to opioid receptors on neurones, blocking transmission of pain impulses.')],
  contrast=[('excitatory synapses', 'inhibitory synapses', 'At excitatory synapses the neurotransmitter depolarises the postsynaptic membrane, making an action potential more likely; at inhibitory synapses it hyperpolarises the membrane, making one less likely.'),
            ('temporal summation', 'spatial summation', 'Temporal summation is the adding of EPSPs from one presynaptic neurone firing repeatedly in quick succession; spatial summation is the adding of EPSPs from several presynaptic neurones firing at the same time.')],
  misc=[('Action potentials jump across the synaptic cleft.', 'The signal crosses the cleft chemically, as neurotransmitter diffusing to receptors on the postsynaptic membrane.'),
        ('Acetylcholine enters the postsynaptic neurone to cause depolarisation.', 'ACh binds to receptors on the surface; this opens ion channels so Na⁺ enters.'),
        ('Every neurotransmitter release triggers an action potential in the postsynaptic neurone.', 'A single EPSP is usually below threshold; summation of several is needed.'),
        ('Painkillers work by repairing damaged tissue.', 'Many painkillers, like endorphins, block transmission of pain signals at synapses or reduce production of chemicals that stimulate nociceptors.')],
  cases=[('neonicotinoid pesticides and bees', 'Neonicotinoids bind irreversibly to acetylcholine receptors; sublethal doses impair bee foraging and navigation.', 'synaptic transmission', 'The pesticide is not broken down by acetylcholinesterase, so the receptor is permanently activated and transmission is disrupted.'),
         ('cocaine use', 'Cocaine blocks dopamine reuptake transporters in the brain’s reward pathway.', 'the effect of drugs on synapses', 'Dopamine stays in the cleft longer, overstimulating postsynaptic receptors and causing euphoria and addiction.'),
         ('capsaicin in chilli peppers', 'Capsaicin binds to TRPV1 receptors on nociceptors, causing a burning sensation.', 'pain perception', 'TRPV1 channels open, depolarising sensory neurones that normally respond to damaging heat.')],
  evaluate=[('Neonicotinoid pesticides should be banned to protect pollinators.', ['they bind irreversibly to insect acetylcholine receptors and sublethal doses impair bee navigation', 'they persist in soil and water and affect non-target insects'], ['they reduce crop losses and replacements may be more toxic or need spraying', 'evidence from field studies is mixed and other factors (Varroa, habitat loss) also harm bees'], 'Precautionary restrictions such as the EU ban are justified, but alternatives and other causes of pollinator decline must also be addressed.'),
            ('Drugs that act on synapses are too dangerous to use in medicine.', ['many cause addiction or tolerance (e.g. opioids)', 'side effects as synapses are widespread'], ['anaesthetics, antidepressants and painkillers relieve great suffering', 'careful dosing and regulation reduce risks'], 'Synaptic drugs are essential in medicine, but their risks require careful control rather than avoidance.')],
  extended=[('Explain how a nerve impulse is transmitted across a synapse and how the signal is terminated.', 'AP at terminal; voltage-gated Ca²⁺ channels; Ca²⁺ influx; vesicles exocytosis; ACh diffuses; binds receptors; ligand-gated Na⁺ channels; depolarisation/EPSP; threshold, summation; acetylcholinesterase hydrolysis; choline reabsorbed and recycled; ATP needed; one-way.', 8),
            ('Explain how drugs and pesticides can affect synaptic transmission, using named examples.', 'Mimic neurotransmitter (neonicotinoids on ACh receptors, irreversible); block receptors (curare); inhibit enzyme (organophosphates on AChE); block reuptake (cocaine, SSRIs); stimulate release; endorphins/opioids block pain; consequences.', 6)],
  )


@R.add('ch03-st4', 'C3', (2, 5), 'numerical')
def summation_calc(rng, slot):
    rest = pick(rng, [-70, -72, -68, -65])
    thr = pick(rng, [-55, -52, -50])
    e = pick(rng, [2.5, 3, 4, 5, 6])
    need = thr - rest
    n = math.ceil(need / e - 1e-9)
    if slot.d <= 3:
        stem = f'A postsynaptic neurone has a resting potential of {rest} mV and a threshold of {thr} mV. Each EPSP depolarises it by {e:g} mV. Calculate the minimum number of EPSPs that must summate to trigger an action potential.'
        return num(stem, f'{n}', f'Depolarisation needed = {thr} − ({rest}) = {need} mV (M1); {need}/{e:g} = {need / e:.2f}, round up → {n} (A1).', 2)
    i = pick(rng, [3, 4, 5])
    n2 = math.ceil((need + i) / e - 1e-9)
    stem = (f'A postsynaptic neurone has a resting potential of {rest} mV and a threshold of {thr} mV. Each EPSP depolarises it by {e:g} mV. '
            f'(a) Calculate the minimum number of EPSPs needed to reach threshold. (b) An inhibitory neurone simultaneously causes a hyperpolarisation of {i} mV. Calculate the number of EPSPs now needed and explain the significance.')
    return num(stem, f'(a) {n}; (b) {n2}; inhibitory inputs make it harder to reach threshold, allowing integration of signals',
               f'(a) {need}/{e:g} → {n} (A1); (b) ({need} + {i})/{e:g} = {(need + i) / e:.2f} → {n2} (A1); summation of excitatory and inhibitory inputs integrates information (R1).', 3)


def _neonic_dq(rng, slot):
    conc = [0, 1, 2, 5, 10, 20]
    base = rng.uniform(85, 95)
    k = rng.uniform(0.05, 0.09)
    ret = [round(base * math.exp(-k * c) + rng.uniform(-2, 2), 0) for c in conc]
    ret[0] = round(base)
    intro = ('Honeybees were fed sugar solution containing different concentrations of a neonicotinoid pesticide (ng per bee). The percentage of foraging bees that returned to the hive was recorded.\n\n'
             + table(['Dose / ng per bee', 'Bees returning / %'], list(zip(conc, [f'{r:.0f}' for r in ret]))))
    p = pct_change(ret[0], ret[3])
    parts = [
        ('State the percentage of bees returning at a dose of 10 ng per bee.', f'{ret[4]:.0f} %', f'{ret[4]:.0f} (A1).', 1),
        ('Calculate the percentage change in return rate between 0 and 5 ng per bee.', f'{signed(p)} %', f'({ret[3]:.0f} − {ret[0]:.0f})/{ret[0]:.0f} × 100 (M1) = {signed(p)} % (A1).', 2),
        ('Describe the relationship between dose and return rate.', 'Return rate decreases as dose increases; the decrease is steepest at low doses / non-linear.', 'Negative relationship (A1); detail of trend (A1).', 2),
        ('Explain how neonicotinoids affect synaptic transmission in insects.', 'They bind to nicotinic acetylcholine receptors on postsynaptic membranes; are not broken down by acetylcholinesterase; cause continuous depolarisation / overstimulation; disrupting nervous control.', 'Binds ACh receptors (A1); not hydrolysed by AChE (A1); continuous stimulation (A1).', 3),
        ('Suggest why fewer bees return to the hive.', 'Disrupted neural control impairs navigation, memory and flight muscle coordination.', 'Link to nervous function (A1).', 1),
        ('Suggest one limitation of this investigation as evidence for effects in the field.', 'Doses fed may differ from field exposure; single exposure; other stresses absent; lab/field conditions differ.', 'Valid limitation (A1).', 1),
        ('State the purpose of the 0 ng per bee group.', 'A control, to show return rate without the pesticide.', 'Control (A1).', 1),
        ('Suggest why sublethal doses of neonicotinoids may still harm a bee colony.', 'Fewer foragers return, so less nectar and pollen are collected; colony growth and production of new queens fall; navigation and learning are impaired.', 'Reduced foraging/food (A1); effect on colony (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch03-st4', _neonic_dq)


# =============================================================================================
# ch04 C3.1 Integration of body systems and C3.2 Defence against disease
# =============================================================================================
S('ch04-st1',
  terms=[('central nervous system', 'the brain and spinal cord, which process information from receptors and coordinate responses'),
         ('reflex arc', 'the pathway of a reflex: receptor, sensory neurone, relay (interneurone) in the spinal cord, motor neurone and effector'),
         ('effector', 'a muscle or gland that carries out a response'),
         ('cerebellum', 'the part of the brain that coordinates skeletal muscle contraction, balance and fine movement'),
         ('hypothalamus', 'the part of the brain that monitors the blood and links the nervous and endocrine systems by controlling the pituitary gland'),
         ('melatonin', 'a hormone secreted by the pineal gland in darkness that helps regulate circadian rhythms such as the sleep–wake cycle'),
         ('chemoreceptor', 'a receptor that detects chemical changes, such as blood CO₂ concentration or pH, used in controlling ventilation and heart rate')],
  facts=[('Which part of the brain controls ventilation rate and heart rate?', 'the medulla oblongata (brainstem)', ['the cerebellum', 'the cerebral cortex', 'the pineal gland'], 'Involuntary control centres.'),
         ('Which gland secretes melatonin?', 'the pineal gland', ['the pituitary gland', 'the adrenal gland', 'the thyroid gland'], 'Secreted mainly at night.'),
         ('Where is the relay neurone of a pain withdrawal reflex located?', 'in the grey matter of the spinal cord', ['in the cerebellum', 'in the muscle', 'in the skin'], 'Spinal reflex.'),
         ('Which hormone prepares the body for vigorous activity (“fight or flight”)?', 'adrenaline (epinephrine)', ['melatonin', 'insulin', 'thyroxine'], 'Secreted by the adrenal medulla.'),
         ('Which part of the brain is responsible for voluntary movement and conscious thought?', 'the cerebrum (cerebral hemispheres)', ['the medulla', 'the cerebellum', 'the hypothalamus'], 'Cerebral cortex.')],
  mc2=[('Why are reflexes faster than voluntary responses?', 'Few synapses are involved and the impulse does not need to pass through the conscious brain.', ['Reflex neurones are unmyelinated.', 'Reflexes use hormones.', 'Reflexes involve more synapses.'], 'Short pathway.'),
       ('Why is nervous control faster than hormonal control?', 'Impulses travel along neurones at up to 100 m s⁻¹, while hormones are carried in the blood.', ['Hormones are larger molecules.', 'Hormones act only at night.', 'Nerves contain blood.'], 'Speed of transmission.'),
       ('Why does heart rate increase during exercise?', 'Chemoreceptors detect rising CO₂/falling pH, and the medulla sends impulses via sympathetic nerves to the sinoatrial node.', ['The cerebellum slows the heart.', 'Blood pressure falls to zero.', 'Melatonin is secreted.'], 'Medulla integrates signals.'),
       ('Why can a person consciously hold their breath for only a limited time?', 'Rising blood CO₂ is detected by chemoreceptors, and the medulla overrides voluntary control to restart breathing.', ['Oxygen levels rise.', 'The cerebellum stops the lungs.', 'Melatonin increases.'], 'Involuntary control.')],
  mc3=[('A ruler dropped between a person’s fingers falls 18 cm before being caught. Using t = √(2d/g) with g = 9.81 m s⁻², what is the reaction time?', '0.19 s', ['0.036 s', '1.9 s', '0.019 s'], 't = √(2 × 0.18/9.81) = 0.19 s.'),
       ('A person with damage to the cerebellum is most likely to have difficulty with which activity?', 'walking in a straight line and fine coordinated movements', ['breathing at rest', 'producing melatonin', 'digesting food'], 'Cerebellum coordinates movement.'),
       ('Shift workers often have disrupted sleep. Which explanation is best?', 'Light at night suppresses melatonin secretion, disturbing circadian rhythms.', ['Darkness destroys the pineal gland.', 'Melatonin is made in the stomach.', 'Adrenaline causes sleep.'], 'Melatonin is secreted in darkness.')],
  why=[('Explain how a pain withdrawal reflex is carried out.', 'Pain receptors in the skin are stimulated; impulses pass along a sensory neurone through the dorsal root to the spinal cord; synapse with a relay neurone in grey matter; synapse with a motor neurone; impulse to a muscle (effector) which contracts, moving the hand away; involuntary and rapid.'),
       ('Explain how the nervous and endocrine systems are integrated by the hypothalamus.', 'The hypothalamus receives nerve impulses and monitors the blood; it secretes releasing hormones into a portal system to the anterior pituitary and sends neurosecretory signals to the posterior pituitary (e.g. ADH); the pituitary releases hormones controlling other endocrine glands.'),
       ('Explain the role of melatonin in circadian rhythms.', 'The pineal gland secretes melatonin in darkness, controlled by the suprachiasmatic nucleus responding to light from the retina; high melatonin promotes sleep and lowers body temperature; levels fall in the morning; jet lag occurs when the rhythm is out of phase with local time.'),
       ('Explain how the body coordinates changes in heart rate during exercise.', 'Chemoreceptors in the aorta, carotid arteries and medulla detect increased CO₂ and lower pH; baroreceptors detect pressure; the cardiovascular centre in the medulla sends impulses along sympathetic nerves to the SA node; adrenaline also increases heart rate.')],
  contrast=[('nervous communication', 'endocrine communication', 'Nervous communication uses electrical impulses along neurones and neurotransmitters, is fast, short-lived and precisely targeted; endocrine communication uses hormones carried in the blood, is slower, longer-lasting and can affect many tissues.'),
            ('reflex actions', 'voluntary actions', 'Reflex actions are rapid, automatic and involve few neurones, often only the spinal cord; voluntary actions are initiated consciously in the cerebral cortex and are slower and more variable.')],
  misc=[('All reflexes are controlled by the brain.', 'Many reflexes, such as pain withdrawal, are spinal reflexes; the brain is informed but does not initiate the response.'),
        ('Hormones and nerves work completely independently.', 'They are integrated, for example by the hypothalamus and pituitary, and nerves stimulate adrenaline secretion.'),
        ('The cerebellum is responsible for conscious thought.', 'The cerebellum coordinates movement and balance; conscious thought is a function of the cerebral cortex.')],
  cases=[('jet lag after long-haul flights', 'Travellers feel tired and wake at the wrong times for several days.', 'circadian rhythms and melatonin', 'Melatonin secretion follows the old day–night cycle until light exposure resets the suprachiasmatic nucleus.'),
         ('the knee-jerk reflex test used by doctors', 'Tapping the patellar tendon causes the leg to kick forward.', 'reflex arcs', 'A stretch receptor stimulates a sensory neurone that synapses directly with a motor neurone in the spinal cord, so absence indicates nerve damage.')],
  evaluate=[('The brain is the most important organ in integrating the body systems.', ['the brain processes sensory information and controls behaviour', 'the hypothalamus links nervous and endocrine systems'], ['many responses are spinal reflexes or local controls', 'endocrine glands and the heart’s pacemaker act independently of the brain'], 'The brain is central to integration, but spinal cord, endocrine glands and local controls also play vital roles.')],
  extended=[('Explain how the nervous and endocrine systems work together to coordinate the body’s responses, using examples.', 'Nervous: receptors, CNS, effectors, fast; endocrine: hormones in blood, slower, long-lasting; hypothalamus–pituitary link; adrenaline (fight or flight) triggered by nerves; melatonin and circadian rhythm; control of heart rate and ventilation by medulla with chemoreceptors; reflexes.', 8),
            ('Describe the components of a reflex arc and explain why reflexes have survival value.', 'Receptor, sensory neurone, dorsal root, relay neurone, grey matter, motor neurone, effector; few synapses; fast, involuntary; protects from damage (pain withdrawal, blink); posture.', 6)],
  )


@R.add('ch04-st1', 'C3', (1, 4), 'numerical')
def ruler_drop(rng, slot):
    ds = [round(rng.uniform(9, 25), 1) for _ in range(5)]
    if slot.d <= 2:
        d = ds[0]
        t = math.sqrt(2 * d / 100 / 9.81)
        stem = f'In a ruler-drop test, a student caught the ruler after it fell {d} cm. Calculate the reaction time using t = √(2d/g), where g = 9.81 m s⁻².'
        return num(stem, f'{t:.3f} s', f'd = {d / 100:.3f} m (M1); t = √(2 × {d / 100:.3f}/9.81) = {t:.3f} s (A1).', 2)
    ts = [math.sqrt(2 * d / 100 / 9.81) for d in ds]
    m, s_ = mean(ts), sd(ts)
    stem = (f'In five ruler-drop trials a student caught the ruler after it fell {", ".join(str(d) for d in ds)} cm. Using t = √(2d/g) with g = 9.81 m s⁻², '
            'calculate the mean reaction time and its standard deviation.')
    return num(stem, f'mean = {m:.3f} s; SD = {s_:.3f} s', f'Convert each distance to m and calculate t (M1): {", ".join(f"{x:.3f}" for x in ts)} s; mean = {m:.3f} s (A1); SD = {s_:.3f} s (A1).', 3)


def _reaction_dq(rng, slot):
    caff = [round(rng.gauss(0.205, 0.02), 3) for _ in range(6)]
    ctrl = [round(rng.gauss(0.235, 0.02), 3) for _ in range(6)]
    mc, mn = mean(caff), mean(ctrl)
    if mc >= mn:
        return None
    sc, sn = sd(caff), sd(ctrl)
    t = pooled_t(ctrl, caff)
    sig = abs(t) > T_CRIT[10]
    intro = ('Twelve students did a computer reaction-time test. Six drank a caffeinated drink and six drank a decaffeinated drink (control) 30 minutes before the test.\n\n'
             + table(['Student', 'Caffeine / s', 'Control / s'], [(i + 1, f'{a:.3f}', f'{b:.3f}') for i, (a, b) in enumerate(zip(caff, ctrl))]))
    p = pct_change(mn, mc)
    parts = [
        ('Calculate the mean reaction time for each group.', f'caffeine {mc:.3f} s; control {mn:.3f} s', f'{mc:.3f} (A1); {mn:.3f} (A1).', 2),
        ('Calculate the standard deviation of each group.', f'caffeine {sc:.3f} s; control {sn:.3f} s', f'Sample SD: {sc:.3f} (A1); {sn:.3f} (A1).', 2),
        ('Calculate the percentage difference in mean reaction time of the caffeine group compared with the control.', f'{signed(p)} %', f'({mc:.3f} − {mn:.3f})/{mn:.3f} × 100 (M1) = {signed(p)} % (A1).', 2),
        (f'A t-test gives t = {abs(t):.2f}. The critical value for 10 degrees of freedom at p = 0.05 is {T_CRIT[10]}. State a conclusion.',
         ('The difference is significant: caffeine reduces reaction time (reject the null hypothesis).' if sig else 'The difference is not significant at p = 0.05; it may be due to chance (accept the null hypothesis).'),
         f't {"greater" if sig else "less"} than critical value (A1); correct conclusion about null hypothesis (A1).', 2),
        ('Suggest how caffeine could reduce reaction time.', 'Caffeine is a stimulant that blocks adenosine receptors, increasing neuronal activity/neurotransmitter release, so synaptic transmission and processing are faster.', 'Stimulant effect on neurones/synapses (A1).', 1),
        ('Suggest two improvements to the design.', 'Larger sample; same students tested with both drinks (crossover); blind design; control for sleep, habitual caffeine use; several practice trials.', 'Any two (A1 A1).', 2),
        ('Explain why the students should practise the test before measurements are taken.', 'Reaction time improves with practice (learning effect), which would be a confounding variable; practice makes trials comparable.', 'Learning effect (A1); confounding variable/fairness (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch04-st1', _reaction_dq)


S('ch04-st2',
  terms=[('tropism', 'a directional growth response of a plant to a directional stimulus'),
         ('phototropism', 'growth of a plant part towards or away from light'),
         ('gravitropism', 'growth of a plant part in response to gravity; shoots grow upwards (negative) and roots downwards (positive)'),
         ('auxin', 'a plant hormone (indole-3-acetic acid) produced in shoot tips that promotes cell elongation'),
         ('phytohormone', 'a plant growth regulator, such as auxin, gibberellin, cytokinin, ethylene or abscisic acid'),
         ('auxin efflux carrier', 'a membrane protein (PIN protein) that transports auxin out of cells; its position determines the direction of auxin flow'),
         ('acid growth hypothesis', 'the idea that auxin stimulates proton pumps, acidifying the cell wall and loosening it so cells can elongate')],
  facts=[('Where is auxin mainly produced in a shoot?', 'in the shoot tip (apical meristem)', ['in mature leaves only', 'in the roots', 'in the xylem'], 'Auxin moves down from the tip.'),
         ('Which hormone promotes fruit ripening?', 'ethylene', ['auxin', 'cytokinin', 'abscisic acid'], 'A gaseous hormone.'),
         ('Which hormone, produced in roots, promotes cell division in shoots?', 'cytokinin', ['ethylene', 'melatonin', 'abscisic acid'], 'Interacts with auxin.'),
         ('To which side of a shoot does auxin move in unilateral light?', 'the shaded side', ['the lit side', 'the tip only', 'the roots only'], 'Cells there elongate more.'),
         ('What does auxin activate in the plasma membrane to loosen the cell wall?', 'proton (H⁺) pumps', ['sodium–potassium pumps', 'aquaporins', 'calcium channels'], 'Wall becomes acidic.')],
  mc2=[('Why does a shoot bend towards light?', 'Auxin accumulates on the shaded side, causing those cells to elongate more.', ['Cells on the lit side grow faster.', 'Light kills cells on the shaded side.', 'Auxin is destroyed in the dark.'], 'Unequal elongation.'),
       ('Why does auxin cause cell walls to loosen?', 'H⁺ pumped into the wall lowers pH, activating expansins that break bonds between cellulose fibres.', ['Auxin digests cellulose directly.', 'Water dissolves the wall.', 'Auxin adds more cellulose.'], 'Acid growth.'),
       ('Why is ethylene release from one ripe fruit able to ripen others nearby?', 'Ethylene is a gas, and ripening fruit produces more ethylene (positive feedback).', ['Ethylene is a liquid absorbed by roots.', 'Ripe fruits release auxin.', 'Ethylene inhibits ripening.'], 'Positive feedback.'),
       ('Why do roots and shoots respond differently to auxin?', 'Root cells are more sensitive; high auxin concentrations inhibit root cell elongation.', ['Roots contain no auxin.', 'Roots are not living.', 'Shoots lack auxin receptors.'], 'Concentration-dependent effects.')],
  mc3=[('The tip of an oat coleoptile is removed and replaced with an agar block that contained the tip. The block is placed on one side. What happens?', 'The coleoptile bends away from the side with the block.', ['It bends towards the block.', 'It grows straight up.', 'It stops growing.'], 'Auxin diffuses from the block into one side.'),
       ('A mica plate is inserted on the shaded side of a coleoptile tip, just below it. Unilateral light is applied. What is expected?', 'Little or no bending, as auxin cannot move down the shaded side.', ['Greater bending towards light.', 'Bending away from light.', 'The tip dies.'], 'Mica blocks auxin transport.'),
       ('Fruit is stored in warehouses with low oxygen and ethylene scrubbers. Why?', 'To slow ripening by reducing ethylene production and action.', ['To speed up ripening.', 'To kill insects.', 'To increase auxin.'], 'Ethylene triggers ripening.')],
  why=[('Explain how auxin causes phototropism in a shoot.', 'Light is detected by phototropin in the tip; auxin efflux carriers (PIN proteins) redistribute auxin to the shaded side; auxin moves down; on the shaded side auxin stimulates H⁺ pumps, cell wall acidifies, expansins loosen cellulose, cells take in water and elongate more; shoot bends towards light.'),
       ('Explain how auxin can establish a concentration gradient.', 'Auxin enters cells in its protonated form by diffusion or influx carriers; inside it becomes an anion; it can only leave via efflux carriers (PIN proteins); the positioning of PIN proteins on one side of cells directs auxin flow, creating gradients.'),
       ('Explain how plant hormones interact to control growth.', 'Auxin from the shoot tip promotes elongation and apical dominance; cytokinins from roots promote cell division and shoot growth; their ratio controls root versus shoot development; gibberellins promote stem elongation; ethylene ripens fruit; responses depend on concentration and tissue.')],
  contrast=[('positive phototropism', 'negative gravitropism', 'Positive phototropism is growth towards a light source; negative gravitropism is growth against the direction of gravity, i.e. upwards. Both are shown by shoots.'),
            ('auxin', 'cytokinin', 'Auxin is made in shoot tips and promotes cell elongation and apical dominance; cytokinin is made in roots and promotes cell division and shoot growth.')],
  misc=[('Light makes cells on the lit side grow faster.', 'Auxin moves to the shaded side, so cells on the shaded side elongate more.'),
        ('Auxin increases the number of cells in a shoot.', 'Auxin mainly causes elongation of existing cells.'),
        ('Plants cannot respond to their environment because they lack nerves.', 'Plants respond using hormones such as auxin, causing tropisms and other growth responses.')],
  cases=[('Darwin’s and Went’s experiments with oat coleoptiles', 'Removing or covering the tip prevented bending; agar blocks that had held tips caused bending on the side they were placed.', 'the role of the shoot tip in phototropism', 'A chemical (auxin) produced in the tip diffuses down and causes growth on one side.'),
         ('commercial ripening of bananas', 'Green bananas are shipped and then exposed to ethylene gas in ripening rooms before sale.', 'the action of ethylene', 'Ethylene triggers ripening, and positive feedback makes the bananas produce more ethylene.')],
  evaluate=[('Experiments on coleoptiles prove that auxin causes phototropism.', ['removing tips or blocking diffusion prevents bending; agar blocks restore it', 'auxin can be measured on the shaded side'], ['coleoptiles may not represent all plants', 'other hormones and light receptors are also involved; correlation of auxin and growth is not complete proof'], 'Coleoptile experiments provide strong evidence for auxin’s role, supported by molecular studies of PIN proteins, but phototropism involves more than auxin alone.')],
  extended=[('Explain how auxin controls phototropism, including the acid growth hypothesis and the role of efflux carriers.', 'Tip detects light (phototropins); PIN efflux carriers redistribute auxin laterally to shaded side; transport down; auxin binds receptor; gene expression; H⁺ pumps; acid wall; expansins loosen cellulose; turgor drives elongation; unequal growth; bending; Went’s experiments.', 8),
            ('Describe the roles of different plant hormones in controlling growth and development.', 'Auxin: elongation, tropisms, apical dominance; cytokinin: cell division, shoot growth, ratio with auxin; gibberellin: stem elongation, germination; ethylene: ripening, positive feedback; abscisic acid: stomatal closure, dormancy.', 6)],
  )


@R.add('ch04-st2', 'C3', (1, 4), 'numerical')
def coleoptile_calc(rng, slot):
    k = rng.uniform(8, 12)
    c1 = pick(rng, [0.05, 0.1, 0.2])
    c2 = pick(rng, [0.3, 0.4, 0.5])
    a1 = round(k * c1 / 0.1, 1)
    a2 = round(k * c2 / 0.1, 1)
    stem = (f'In a curvature test, agar blocks containing auxin were placed on one side of decapitated coleoptiles. A block with {c1} mg dm⁻³ auxin gave a curvature of {a1}°. '
            f'Assuming curvature is proportional to concentration, predict the curvature with {c2} mg dm⁻³ and explain the direction of bending.')
    return num(stem, f'{a2}°; bending away from the side with the block, because auxin stimulates elongation of cells on that side',
               f'{a1} × {c2}/{c1} = {a2}° (A1); auxin diffuses into cells below the block, which elongate more, bending away (R1).', 2 if slot.d <= 2 else 3)


def _went_dq(rng, slot):
    conc = [0, 0.05, 0.1, 0.2, 0.4, 0.8]
    k = rng.uniform(60, 90)
    cmax = rng.uniform(20, 26)
    curv = [round(cmax * c / (c + k / 1000 * 2), 1) if c else 0.0 for c in conc]
    curv = [c + round(rng.uniform(-0.4, 0.4), 1) if c else 0.0 for c in curv]
    intro = ('Coleoptiles of oat seedlings were decapitated, and agar blocks containing different concentrations of auxin (IAA) were placed on the left side of each cut surface. '
             'The angle of curvature was measured after 90 minutes in darkness.\n\n'
             + table(['IAA / mg dm⁻³', 'Mean curvature / °'], list(zip(conc, [f'{c:.1f}' for c in curv]))))
    p = pct_change(curv[2], curv[3])
    parts = [
        ('State the mean curvature with 0.2 mg dm⁻³ IAA.', f'{curv[3]:.1f}°', f'{curv[3]:.1f} (A1).', 1),
        ('Calculate the percentage increase in curvature when IAA concentration doubled from 0.1 to 0.2 mg dm⁻³.', f'{signed(p)} %', f'({curv[3]:.1f} − {curv[2]:.1f})/{curv[2]:.1f} × 100 (M1) = {signed(p)} % (A1).', 2),
        ('Describe the relationship between IAA concentration and curvature.', 'Curvature increases with IAA concentration, nearly proportionally at low concentrations, then levelling off at higher concentrations.', 'Positive relationship (A1); levelling off (A1).', 2),
        ('State the direction in which the coleoptiles curved, and explain why.', 'To the right (away from the block), because IAA diffused into cells on the left side, which elongated more.', 'Away from block (A1); more elongation on block side (R1).', 2),
        ('Explain how IAA causes cell elongation.', 'IAA activates H⁺ pumps; H⁺ moves into the cell wall; low pH activates expansins; bonds between cellulose microfibrils loosen; water uptake by osmosis stretches the wall.', 'H⁺ pumps (A1); acidic wall/expansins (A1); water uptake and elongation (A1).', 3),
        ('Explain why the experiment was done in darkness.', 'To prevent phototropism / light causing redistribution of auxin, so curvature is due to IAA in the block only.', 'Light would affect auxin distribution (A1).', 1),
        ('Suggest why a block with 0 mg dm⁻³ IAA was included.', 'Control to show that the agar itself does not cause curvature.', 'Control (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch04-st2', _went_dq)


S('ch04-st3',
  terms=[('pathogen', 'an organism or virus that causes disease, such as a bacterium, virus, fungus or protist'),
         ('antigen', 'a molecule, usually a protein or glycoprotein on the surface of a pathogen or cell, that triggers an immune response'),
         ('phagocyte', 'a white blood cell that ingests and digests pathogens by phagocytosis; part of the innate immune system'),
         ('lymphocyte', 'a white blood cell involved in the adaptive (specific) immune response; B lymphocytes produce antibodies and T lymphocytes regulate or kill infected cells'),
         ('clonal selection', 'the activation of the specific lymphocyte whose receptor matches an antigen, followed by its division to form a clone'),
         ('plasma cell', 'an activated B lymphocyte that secretes large amounts of a specific antibody'),
         ('memory cell', 'a long-lived lymphocyte that remains after an infection and allows a faster, stronger secondary response'),
         ('innate immune system', 'non-specific defences present from birth, including skin, mucous membranes, inflammation and phagocytes')],
  facts=[('Which protein forms the mesh of a blood clot?', 'fibrin', ['fibrinogen only', 'thrombin', 'haemoglobin'], 'Fibrinogen is converted to fibrin by thrombin.'),
         ('Which cells release clotting factors at a wound?', 'platelets', ['red blood cells', 'plasma cells', 'neurones'], 'Cell fragments.'),
         ('Which cells activate B lymphocytes in the specific immune response?', 'helper T lymphocytes', ['red blood cells', 'platelets', 'phagocytes only'], 'Helper T cells are activated by antigen-presenting cells.'),
         ('Which tough protein in the outer skin acts as a physical barrier?', 'keratin', ['collagen', 'haemoglobin', 'insulin'], 'Dead, keratinised cells.'),
         ('Which is a primary (first-line) defence against pathogens?', 'mucous membranes that trap pathogens', ['antibodies', 'memory cells', 'plasma cells'], 'Prevents entry.'),
         ('Which enzyme converts fibrinogen into fibrin?', 'thrombin', ['amylase', 'lysozyme', 'pepsin'], 'Final step of the cascade.')],
  mc2=[('Why is the clotting cascade useful?', 'It rapidly amplifies the signal at a wound so a clot forms quickly, sealing the wound.', ['It slows clotting down.', 'It makes antibodies.', 'It dissolves clots.'], 'Each step activates many molecules.'),
       ('Why is the specific immune response slower on first infection than on reinfection?', 'Initially few lymphocytes match the antigen, so clonal expansion takes time; memory cells speed the second response.', ['Antibodies are made only on reinfection.', 'Phagocytes are absent at first.', 'Antigens change.'], 'Primary vs secondary response.'),
       ('Why do helper T cells play a central role in specific immunity?', 'They are needed to activate B lymphocytes, which then divide and form plasma cells.', ['They produce antibodies.', 'They form clots.', 'They are phagocytes.'], 'Activation step.'),
       ('Why can phagocytes respond to many different pathogens?', 'They recognise general features of pathogens rather than specific antigens (non-specific).', ['They make specific antibodies.', 'They have memory.', 'They divide into clones.'], 'Innate immunity.')],
  mc3=[('A patient lacks functional helper T cells. Which is most likely?', 'Antibody production against new pathogens is greatly reduced.', ['Phagocytosis stops completely.', 'Blood cannot clot.', 'Skin no longer forms keratin.'], 'As in AIDS.'),
       ('A B-cell clone doubles every 12 hours. Starting from one activated cell, about how many cells are there after 5 days?', 'about 1000 (2¹⁰ = 1024)', ['about 10', 'about 100', 'about 1 000 000'], '10 doublings in 120 hours.'),
       ('Which sequence describes the specific response?', 'antigen presentation → helper T activation → B-cell activation → clonal expansion → plasma cells secrete antibody', ['B-cell activation → antigen presentation → clotting → plasma cells', 'platelets → fibrin → antibody', 'memory cells → phagocytes → helper T cells'], 'Order of events.')],
  why=[('Explain how blood clotting is triggered and how it seals a wound.', 'Damage exposes collagen; platelets adhere and release clotting factors; a cascade of reactions converts prothrombin to thrombin; thrombin converts soluble fibrinogen into insoluble fibrin; fibrin forms a mesh that traps blood cells, forming a clot that seals the wound.'),
       ('Explain how B lymphocytes are activated to produce antibodies.', 'A macrophage engulfs a pathogen and presents its antigens; a helper T cell with a matching receptor binds and is activated; it activates the B cell with matching antibodies on its surface (that has also bound antigen); the B cell divides by mitosis (clonal expansion); clones differentiate into plasma cells that secrete antibody and memory cells.'),
       ('Explain how phagocytes contribute to defence against pathogens.', 'Phagocytes move by amoeboid motion to sites of infection (attracted by chemicals); recognise pathogens; engulf them by endocytosis into a vesicle; lysosomes fuse and digestive enzymes kill and break down the pathogen; some present antigens to lymphocytes.')],
  contrast=[('the innate immune system', 'the adaptive immune system', 'The innate system is non-specific, present from birth and responds the same way each time (skin, phagocytes, inflammation); the adaptive system is specific to antigens, involves lymphocytes and antibodies, and develops memory.'),
            ('plasma cells', 'memory cells', 'Plasma cells are short-lived and secrete large amounts of antibody during an infection; memory cells are long-lived, do not secrete antibody, and allow a faster secondary response.')],
  misc=[('Antibodies are produced by phagocytes.', 'Antibodies are produced by plasma cells, which are derived from B lymphocytes.'),
        ('Each lymphocyte can respond to any antigen.', 'Each lymphocyte is specific to one antigen; only the matching clone is selected and expanded.'),
        ('Fibrinogen is the protein that forms the clot mesh.', 'Fibrinogen is soluble; thrombin converts it to insoluble fibrin, which forms the mesh.'),
        ('Viruses can be killed by phagocytes only if they are inside cells.', 'Phagocytes engulf free virus particles; infected cells are destroyed by cytotoxic T cells.')],
  cases=[('haemophilia', 'People with haemophilia lack a functional clotting factor (factor VIII or IX) and bleed for longer.', 'the clotting cascade', 'Without one factor the cascade cannot produce enough thrombin, so little fibrin forms.'),
         ('chickenpox and lifelong immunity', 'Most people who have had chickenpox do not get it again.', 'immunological memory', 'Memory cells produced during the first infection allow a rapid secondary response before symptoms develop.')],
  evaluate=[('The innate immune system is more important than the adaptive immune system.', ['innate defences prevent most infections and act immediately', 'phagocytes and inflammation contain infections while adaptive responses develop'], ['adaptive immunity is needed to clear many infections and gives memory', 'vaccination depends on adaptive immunity; people lacking it (e.g. AIDS, SCID) suffer severe infections'], 'Both are essential and interdependent: innate defences provide the first response and activate adaptive responses, which give specificity and memory.')],
  extended=[('Describe the primary defences of the body and explain how the specific immune response leads to the production of antibodies.', 'Skin (keratin, sebum, acidity), mucous membranes, cilia, stomach acid; clotting seals wounds; phagocytes; antigen presentation; helper T cells; B-cell activation; clonal selection and expansion; plasma cells; antibodies; memory cells; secondary response.', 8),
            ('Explain the process of blood clotting and its importance.', 'Wound exposes collagen; platelets release clotting factors; cascade; prothrombin → thrombin; fibrinogen → fibrin; mesh traps cells; prevents blood loss and entry of pathogens; importance of control (coronary thrombosis).', 6)],
  )


@R.add('ch04-st3', 'C3', (2, 5), 'numerical')
def clone_growth(rng, slot):
    dt = pick(rng, [6, 8, 10, 12])
    hrs = dt * pick(rng, [8, 10, 12, 15, 18])
    n0 = pick(rng, [1, 5, 10, 20])
    g = hrs // dt
    N = n0 * 2 ** g
    stem = f'An activated B-lymphocyte clone starts from {n0} cell{"s" if n0 > 1 else ""} and divides by mitosis every {dt} hours. Calculate the number of cells after {hrs} hours (assume no cell death).'
    ans = f'{n0} × 2^{g} = {N:.3g} cells' if N > 1e5 else f'{N} cells'
    if slot.d >= 4:
        stem += ' Explain why this clonal expansion explains the delay in the primary response.'
        return num(stem, ans + '; many divisions are needed before enough plasma cells are present to make large amounts of antibody',
                   f'{hrs}/{dt} = {g} generations (M1); {n0} × 2^{g} = {N:.4g} (A1); delay due to time for clonal expansion and differentiation (R1).', 3)
    return num(stem, ans, f'{hrs}/{dt} = {g} generations (M1); N = {n0} × 2^{g} = {N:.4g} (A1).', 2)


def _wbc_dq(rng, slot):
    norm = [rng.uniform(55, 65), rng.uniform(25, 33), rng.uniform(4, 7), rng.uniform(1, 4), 0.5]
    tot_n = rng.uniform(6.0, 8.0)
    inf = [rng.uniform(75, 85), rng.uniform(10, 16), rng.uniform(3, 6), rng.uniform(0.5, 2), 0.5]
    tot_i = rng.uniform(14, 19)
    norm = [round(100 * x / sum(norm), 1) for x in norm]
    inf = [round(100 * x / sum(inf), 1) for x in inf]
    cells = ['neutrophils (phagocytes)', 'lymphocytes', 'monocytes', 'eosinophils', 'basophils']
    intro = (f'A blood sample from a healthy person and one from a patient with a bacterial infection were analysed. The total white blood cell count was {tot_n:.1f} × 10⁹ dm⁻³ (healthy) '
             f'and {tot_i:.1f} × 10⁹ dm⁻³ (infection). The percentage of each type of white cell is shown.\n\n'
             + table(['Cell type', 'Healthy / %', 'Infection / %'], [(c, f'{a:.1f}', f'{b:.1f}') for c, a, b in zip(cells, norm, inf)]))
    nn = tot_n * norm[0] / 100
    ni = tot_i * inf[0] / 100
    ln, li = tot_n * norm[1] / 100, tot_i * inf[1] / 100
    parts = [
        ('State the percentage of lymphocytes in the healthy sample.', f'{norm[1]:.1f} %', f'{norm[1]:.1f} (A1).', 1),
        ('Calculate the number of neutrophils per dm³ in each sample.', f'healthy {nn:.1f} × 10⁹; infection {ni:.1f} × 10⁹ dm⁻³', f'{tot_n:.1f} × {norm[0]:.1f}/100 = {nn:.1f} (A1); {tot_i:.1f} × {inf[0]:.1f}/100 = {ni:.1f} (A1).', 2),
        ('Calculate how many times more neutrophils per dm³ the patient has than the healthy person.', f'{ni / nn:.1f} times', f'{ni:.1f}/{nn:.1f} = {ni / nn:.1f} (A1).', 1),
        ('The percentage of lymphocytes is lower in the patient. Deduce whether the number of lymphocytes per dm³ is also lower.', f'{"No" if li >= ln else "Yes"} – healthy {ln:.2f} × 10⁹, infection {li:.2f} × 10⁹ dm⁻³; a lower percentage does not mean fewer cells when the total count is higher.',
         f'Calculation of both (M1); correct deduction with reason (A1).', 2),
        ('Explain the increase in neutrophils during a bacterial infection.', 'Neutrophils are phagocytes produced in bone marrow in response to infection; they engulf and digest bacteria by phagocytosis, so more are needed.', 'Phagocytosis of bacteria (A1); increased production (A1).', 2),
        ('Outline the role of lymphocytes in the response to this infection.', 'B lymphocytes are activated by helper T cells, divide to form plasma cells secreting specific antibodies and memory cells.', 'Antibody production (A1); clonal selection/memory (A1).', 2),
        ('Suggest why a raised neutrophil count suggests a bacterial rather than a viral infection.', 'Neutrophils are phagocytes that respond mainly to bacteria; viral infections more often raise lymphocyte counts.', 'Neutrophils engulf bacteria (A1); viral infections → lymphocytes (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch04-st3', _wbc_dq)


S('ch04-st4',
  terms=[('antibody', 'a Y-shaped immunoglobulin protein made of two heavy and two light polypeptide chains with variable regions that bind a specific antigen'),
         ('vaccine', 'a preparation containing antigens (weakened or inactivated pathogen, subunit or mRNA coding for an antigen) that stimulates a primary immune response and memory cells without causing disease'),
         ('herd immunity', 'indirect protection of non-immune individuals when a large enough proportion of a population is immune, so transmission chains are broken'),
         ('basic reproduction number (R₀)', 'the average number of people infected by one infectious person in a fully susceptible population'),
         ('antibiotic', 'a chemical that kills or inhibits the growth of bacteria by targeting processes absent from eukaryotic cells'),
         ('antibiotic resistance', 'the ability of bacteria to survive an antibiotic, arising by mutation or gene transfer and spread by natural selection'),
         ('opsonisation', 'the coating of a pathogen with antibodies so that phagocytes can recognise and engulf it more easily')],
  facts=[('How many polypeptide chains are in one IgG antibody molecule?', '4', ['2', '1', '8'], 'Two heavy and two light chains.'),
         ('Why are antibiotics ineffective against viruses?', 'Viruses lack the bacterial structures and metabolic processes that antibiotics target.', ['Viruses are too large.', 'Viruses are killed by antibodies only.', 'Viruses have cell walls.'], 'No cell wall, no 70S ribosomes of their own.'),
         ('Which bacterium is known as MRSA when resistant to many antibiotics?', 'Staphylococcus aureus', ['Escherichia coli', 'Vibrio cholerae', 'Mycobacterium tuberculosis'], 'Methicillin-resistant S. aureus.'),
         ('Which disease was eradicated worldwide by vaccination by 1980?', 'smallpox', ['measles', 'polio', 'tuberculosis'], 'WHO campaign.'),
         ('Who discovered penicillin?', 'Alexander Fleming', ['Louis Pasteur', 'Edward Jenner', 'Jonas Salk'], 'Discovered in 1928.'),
         ('Which part of an antibody binds the antigen?', 'the variable region', ['the constant region', 'the hinge only', 'the disulfide bond'], 'Its shape is specific.')],
  mc2=[('Why does a vaccine give long-term protection?', 'It causes production of memory cells that allow a rapid secondary response.', ['It contains antibodies that last for life.', 'It kills all pathogens in the body.', 'It changes the person’s DNA.'], 'Active immunity.'),
       ('Why does a higher R₀ require a higher vaccination coverage for herd immunity?', 'Each case would infect more people, so more must be immune to bring the effective reproduction number below 1.', ['Higher R₀ means the disease is less infectious.', 'Vaccines work less well.', 'R₀ does not affect herd immunity.'], 'Threshold = 1 − 1/R₀.'),
       ('Why does overuse of antibiotics increase resistance?', 'Antibiotics kill susceptible bacteria, leaving resistant ones to reproduce (natural selection).', ['Antibiotics cause bacteria to choose resistance.', 'Antibiotics feed resistant bacteria.', 'Resistance is caused by vaccines.'], 'Selection pressure.'),
       ('Why can antibiotics be used without harming human cells?', 'They target structures such as bacterial cell walls or 70S ribosomes not found in human cells.', ['Human cells have cell walls.', 'Antibiotics do not enter the body.', 'Human cells are larger.'], 'Selective toxicity.')],
  mc3=[('Measles has an R₀ of about 15. What proportion of the population must be immune for herd immunity?', 'about 93 %', ['about 15 %', 'about 50 %', 'about 67 %'], '1 − 1/15 = 0.93.'),
       ('A patient stops taking antibiotics after two days because they feel better. What is the risk?', 'Surviving, more resistant bacteria may multiply and spread.', ['The bacteria become viruses.', 'Antibodies are destroyed.', 'Memory cells are lost.'], 'Complete the course.'),
       ('A bacterium with a plasmid carrying a resistance gene is placed with sensitive bacteria. How can resistance spread without mutation?', 'By horizontal gene transfer of the plasmid (conjugation).', ['By meiosis.', 'By vaccination.', 'By antibodies.'], 'Plasmids transfer between bacteria.')],
  why=[('Explain how antibodies help to destroy pathogens.', 'Antibodies bind specific antigens via variable regions; they cause agglutination (clumping) of pathogens; neutralise toxins and viruses by blocking binding sites; opsonise pathogens for phagocytes; activate complement, which lyses bacteria.'),
       ('Explain how vaccination provides immunity.', 'A vaccine contains antigens from a pathogen (weakened, inactivated, subunit or mRNA); it triggers a primary response: antigen presentation, helper T activation, B-cell clonal selection, plasma cells and memory cells; on later infection memory cells give a rapid, large secondary response before disease develops.'),
       ('Explain how antibiotic resistance spreads in a population of bacteria.', 'Random mutations or acquisition of resistance genes on plasmids give some bacteria resistance; antibiotic use kills susceptible bacteria; resistant ones survive and reproduce rapidly by binary fission; genes spread by horizontal gene transfer; resistant strains such as MRSA become common, especially in hospitals.'),
       ('Explain how herd immunity protects unvaccinated people.', 'When a high proportion are immune, an infected person is unlikely to contact a susceptible person; the effective reproduction number falls below 1; chains of transmission are broken; outbreaks die out, protecting babies, the immunocompromised and those who cannot be vaccinated.')],
  contrast=[('active immunity', 'passive immunity', 'Active immunity results from the person’s own immune response to antigens (infection or vaccine) and produces memory cells, so is long-lasting; passive immunity is the transfer of ready-made antibodies (placenta, breast milk, injection) and is immediate but short-lived.'),
            ('the primary immune response', 'the secondary immune response', 'The primary response is slow and produces a low concentration of antibody; the secondary response, due to memory cells, is faster and produces much more antibody for longer.')],
  misc=[('Antibiotics can cure the common cold and influenza.', 'These are viral infections; antibiotics act only on bacteria.'),
        ('Bacteria become resistant because they get used to antibiotics.', 'Resistance arises by random mutation or gene transfer and is selected for by antibiotic use; individual bacteria do not adapt.'),
        ('Vaccines contain antibodies.', 'Vaccines contain antigens (or mRNA coding for them) that stimulate the body to make its own antibodies and memory cells.'),
        ('Herd immunity requires everyone to be vaccinated.', 'Herd immunity requires a threshold proportion, 1 − 1/R₀, of the population to be immune.')],
  cases=[('the eradication of smallpox', 'A global WHO vaccination campaign with ring vaccination eliminated smallpox by 1980.', 'vaccination and herd immunity', 'Smallpox had no animal reservoir and a stable antigen, so vaccination broke all transmission chains.'),
         ('MRSA in hospitals', 'Methicillin-resistant Staphylococcus aureus causes infections that are difficult to treat.', 'antibiotic resistance', 'Heavy antibiotic use in hospitals selects for resistant strains, which spread between patients.'),
         ('Fleming’s discovery of penicillin', 'In 1928 Fleming noticed a clear zone around a Penicillium mould on a plate of Staphylococcus.', 'antibiotics', 'The mould secreted a chemical that killed bacteria, later purified by Florey and Chain.')],
  evaluate=[('Vaccination should be compulsory for all children.', ['high coverage achieves herd immunity, protecting those who cannot be vaccinated', 'diseases such as measles return when coverage falls'], ['individual liberty and parental choice', 'rare side effects; compulsion may increase distrust'], 'Strong incentives and education are justified to reach herd-immunity thresholds; compulsion may be justified for highly infectious diseases such as measles.'),
            ('Antibiotic resistance is mainly caused by doctors over-prescribing antibiotics.', ['prescribing for viral infections and unfinished courses select for resistance'], ['agricultural use in livestock is a major source', 'poor hygiene, sanitation and global travel spread resistant strains'], 'Over-prescribing contributes, but agricultural use and spread of resistant strains are equally important, so a “One Health” approach is needed.')],
  extended=[('Explain the structure of antibodies, how they are produced and how vaccination makes use of this process.', 'Four polypeptides (2 heavy, 2 light), disulfide bonds, variable regions, constant region; plasma cells from activated B cells; helper T cells; clonal selection; agglutination, neutralisation, opsonisation; vaccine antigens; primary response; memory cells; secondary response; herd immunity.', 8),
            ('Explain how antibiotic resistance evolves and outline measures to reduce it.', 'Variation by mutation/plasmid gene transfer; antibiotic selection pressure; survival and reproduction of resistant bacteria; MRSA; measures: reduce prescribing, complete courses, hospital hygiene, limit farm use, new antibiotics, phage therapy.', 6)],
  )


@R.add('ch04-st4', 'C3', (1, 4), 'numerical')
def herd_threshold(rng, slot):
    dis, r0 = pick(rng, [('measles', 15), ('mumps', 5), ('rubella', 6), ('polio', 6), ('diphtheria', 7), ('pertussis', 16), ('smallpox', 5), ('COVID-19 (early variants)', 3), ('influenza', 2)])
    if rng.random() < 0.4:
        r0 = round(r0 * rng.uniform(0.8, 1.2), 1)
    h = 100 * (1 - 1 / r0)
    stem = f'The basic reproduction number (R₀) of {dis} is {r0:g}. Calculate the minimum percentage of the population that must be immune for herd immunity.'
    if slot.d >= 3:
        eff = pick(rng, [85, 90, 95])
        cov = min(h / eff * 100, 999)
        stem += f' If the vaccine is {eff} % effective, calculate the vaccination coverage needed.'
        ans = f'{h:.0f} %; coverage {cov:.0f} %' + (' – impossible (above 100 %), so herd immunity cannot be reached with this vaccine alone' if cov > 100 else '')
        return num(stem, ans, f'1 − 1/R₀ = 1 − 1/{r0:g} = {h / 100:.3f} (M1) → {h:.0f} % (A1); coverage = {h:.1f}/{eff/100:.2f} = {cov:.0f} % (A1).', 3)
    return num(stem, f'{h:.0f} %', f'1 − 1/R₀ = 1 − 1/{r0:g} (M1) = {h:.0f} % (A1).', 2)


@R.add('ch04-st4', 'C2', (1, 4), 'mcq')
def herd_mcq(rng, slot):
    r0 = pick(rng, [2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 18])
    h = 100 * (1 - 1 / r0)
    return nmcq(rng, f'A disease has R₀ = {r0:g}. What proportion of the population must be immune to achieve herd immunity?', f'{h:.0f} %',
                [f'{100 / r0:.0f} %', f'{min(99, r0 * 5):.0f} %', f'{100 - h / 2:.0f} %', f'{h / 2:.0f} %'], f'Herd immunity threshold = 1 − 1/R₀ = 1 − 1/{r0:g} = {h:.0f} %.')


def _zone_dq(rng, slot):
    abx = ['penicillin', 'tetracycline', 'streptomycin', 'erythromycin', 'ampicillin']
    rng.shuffle(abx)
    abx = abx[:4]
    dia = sorted([round(rng.uniform(6.0, 30.0), 0) for _ in range(4)], reverse=True)
    dia[-1] = 6.0
    rng.shuffle(dia)
    disc = 6
    areas = [math.pi * (d / 2) ** 2 - math.pi * (disc / 2) ** 2 for d in dia]
    intro = (f'Paper discs (diameter {disc} mm) soaked in four antibiotics were placed on an agar plate spread with a bacterium isolated from a patient. After 24 hours at 25 °C, the diameter of the clear zone '
             '(including the disc) was measured.\n\n' + table(['Antibiotic', 'Zone diameter / mm'], [(a, f'{d:.0f}') for a, d in zip(abx, dia)]))
    best = abx[dia.index(max(dia))]
    none_ = abx[dia.index(min(dia))]
    i = dia.index(max(dia))
    parts = [
        ('Identify the antibiotic that was most effective against this bacterium.', best, f'{best} – largest zone (A1).', 1),
        (f'Calculate the area of the clear zone (excluding the disc) for {best}.', f'{areas[i]:.0f} mm²', f'π × ({dia[i]:.0f}/2)² − π × ({disc}/2)² (M1) = {areas[i]:.0f} mm² (A1).', 2),
        (f'Explain the result for {none_}.', 'No clear zone beyond the disc: the bacterium is resistant to this antibiotic (or it does not diffuse/act on this species).', 'No inhibition (A1); resistance (R1).', 2),
        ('Explain why the zone of inhibition indicates the effectiveness of an antibiotic.', 'The antibiotic diffuses out from the disc into the agar; where its concentration is high enough it kills or prevents growth of bacteria; a larger zone means bacteria are inhibited at lower concentrations.', 'Diffusion (A1); inhibition of growth (A1).', 2),
        ('Explain why the plates were incubated at 25 °C rather than 37 °C.', 'To reduce the risk of culturing human pathogens.', 'Safety reason (A1).', 1),
        ('Suggest two variables that must be controlled for a fair comparison.', 'Disc size; volume/concentration of antibiotic; agar depth; incubation time and temperature; density of bacterial lawn.', 'Two valid (A1 A1).', 2),
        ('Explain how resistance to antibiotics can become common in a hospital.', 'Mutation or gene transfer gives some bacteria resistance; antibiotic use kills susceptible bacteria; resistant bacteria survive, reproduce and spread between patients.', 'Variation (A1); selection (A1); spread (A1).', 3),
    ]
    return intro, parts


data_q(R, 'ch04-st4', _zone_dq)


S('ch04-st5',
  terms=[('zoonosis', 'an infectious disease that is transmitted from animals to humans'),
         ('epidemiology', 'the study of the distribution, spread and control of diseases in populations'),
         ('pandemic', 'an epidemic of a disease that spreads across many countries or continents'),
         ('case fatality rate', 'the percentage of confirmed cases of a disease that result in death'),
         ('incidence', 'the number of new cases of a disease in a population over a given time, often per 100 000 people'),
         ('HIV', 'human immunodeficiency virus, a retrovirus that infects helper T cells and causes AIDS'),
         ('AIDS', 'acquired immune deficiency syndrome: the condition when HIV has destroyed so many helper T cells that opportunistic infections occur')],
  facts=[('Which cells does HIV infect and destroy?', 'helper T lymphocytes (CD4⁺ cells)', ['red blood cells', 'platelets', 'plasma cells only'], 'Leads to immunodeficiency.'),
         ('Which is a zoonotic disease?', 'rabies', ['cystic fibrosis', 'type 2 diabetes', 'sickle-cell anaemia'], 'Transmitted from animals by bites.'),
         ('Which enzyme does HIV use to make DNA from its RNA genome?', 'reverse transcriptase', ['DNA ligase', 'RNA polymerase', 'helicase'], 'HIV is a retrovirus.'),
         ('How is HIV transmitted?', 'through body fluids: sexual intercourse, shared needles, blood, mother to child', ['by mosquitoes', 'by coughing and sneezing', 'by shaking hands'], 'Not by casual contact.'),
         ('Which animal is thought to be the original reservoir of SARS-CoV-2?', 'bats', ['cattle', 'chickens', 'mosquitoes'], 'Possibly via an intermediate host.')],
  mc2=[('Why are zoonoses increasing in frequency?', 'Habitat destruction, wildlife trade and intensive farming bring humans into closer contact with animal pathogens.', ['Animals are getting more diseases.', 'Vaccines cause zoonoses.', 'Climate is getting colder.'], 'Contact with reservoirs.'),
       ('Why do people with AIDS suffer from opportunistic infections?', 'Loss of helper T cells means B cells are not activated and antibodies are not produced.', ['HIV directly causes tuberculosis.', 'Phagocytes multiply too fast.', 'Platelets stop working.'], 'Immunodeficiency.'),
       ('Why is it difficult to make a vaccine against HIV?', 'HIV mutates rapidly, changing its surface antigens, and it infects the immune cells themselves.', ['HIV has no antigens.', 'HIV is a bacterium.', 'HIV is too large.'], 'Antigenic variation.'),
       ('Why were social distancing and masks used to control COVID-19?', 'SARS-CoV-2 spreads in respiratory droplets and aerosols, so reducing contact reduces transmission.', ['The virus spreads only in food.', 'Masks produce antibodies.', 'Distance kills the virus.'], 'Reduce R.')],
  mc3=[('In one week a city had 2400 new COVID-19 cases in a population of 800 000. What was the weekly incidence per 100 000?', '300', ['3', '30', '3000'], '2400/800 000 × 100 000 = 300.'),
       ('An outbreak has an effective reproduction number of 2. Starting from 10 cases, how many new cases are expected in the fifth generation of infection?', '160', ['20', '100', '320'], '10 × 2⁴ = 160 (generation 1 = 10).'),
       ('Of 5000 confirmed cases, 75 died. What is the case fatality rate?', '1.5 %', ['0.015 %', '15 %', '6.7 %'], '75/5000 × 100 = 1.5 %.')],
  why=[('Explain how HIV leads to AIDS.', 'HIV binds to CD4 receptors on helper T cells; enters; reverse transcriptase makes DNA, integrated into host genome; new viruses made and released, destroying helper T cells; over years helper T cell numbers fall; B cells cannot be activated, so antibody production fails; opportunistic infections and cancers occur (AIDS).'),
       ('Explain the factors that affect the spread of a zoonotic disease such as COVID-19.', 'Spillover from an animal reservoir (bats) possibly via an intermediate host; human-to-human transmission by droplets/aerosols; R value depends on contact rate, duration of infectiousness and transmission probability; asymptomatic spread; population density, travel; control by testing, isolation, distancing, masks, vaccination.'),
       ('Explain why epidemiologists use incidence and case fatality rates rather than total numbers of cases.', 'Rates per 100 000 allow comparison between populations of different size; case fatality rate shows severity; trends over time can be compared; but they depend on testing levels and reporting.')],
  contrast=[('incidence', 'prevalence', 'Incidence is the number of new cases in a given period; prevalence is the total number of existing cases at a particular time.'),
            ('an epidemic', 'a pandemic', 'An epidemic is a rapid increase in cases in a region; a pandemic is an epidemic that has spread across several countries or continents.')],
  misc=[('HIV and AIDS are the same thing.', 'HIV is the virus; AIDS is the syndrome that develops when HIV has destroyed most helper T cells.'),
        ('People die directly from HIV.', 'People with AIDS die from opportunistic infections and cancers because their immune system fails.'),
        ('Zoonoses can only be caught by eating infected meat.', 'Zoonoses spread by bites, contact with animals or their fluids, vectors, droplets and contaminated food or water.'),
        ('A case fatality rate tells you the probability of dying if infected.', 'CFR uses confirmed cases; many mild infections are undetected, so it often overestimates the infection fatality rate.')],
  cases=[('the COVID-19 pandemic', 'SARS-CoV-2 emerged in 2019, probably from bats, and spread worldwide through air travel and respiratory transmission.', 'zoonoses and epidemiology', 'A zoonotic spillover with efficient human-to-human transmission and asymptomatic spread led to a pandemic, controlled by distancing and vaccination.'),
         ('antiretroviral therapy for HIV', 'Combinations of drugs that inhibit reverse transcriptase and protease keep viral loads undetectable.', 'the HIV life cycle', 'Blocking viral replication preserves helper T cells and prevents progression to AIDS, and prevents transmission.'),
         ('bovine tuberculosis', 'Mycobacterium bovis spreads from cattle (and badgers) to humans through unpasteurised milk.', 'zoonotic transmission', 'Pasteurisation and testing of cattle reduce transmission from the animal reservoir.')],
  evaluate=[('Lockdowns were the most effective way to control the COVID-19 pandemic.', ['reduced contact rates lowered R below 1 and prevented health systems being overwhelmed', 'bought time for vaccine development'], ['large economic, educational and mental-health costs', 'vaccination proved more effective in the long term; testing and tracing also mattered'], 'Lockdowns were effective in the short term before vaccines, but vaccination and targeted measures were more sustainable.'),
            ('Preventing future pandemics depends mainly on protecting natural habitats.', ['habitat destruction and wildlife trade increase contact with animal reservoirs'], ['surveillance, rapid vaccine development and public-health systems are also essential', 'intensive farming and antibiotic use also create risks'], 'Habitat protection reduces spillover risk, but surveillance and public-health preparedness are equally important.')],
  extended=[('Explain how HIV affects the immune system and evaluate methods used to control its spread.', 'Retrovirus; CD4 binding; reverse transcriptase; integration; destruction of helper T cells; failure of antibody production; opportunistic infections; control: condoms, testing, needle exchange, antiretroviral therapy, PrEP, preventing mother-to-child transmission; no vaccine due to mutation.', 8),
            ('Using COVID-19 as an example, explain how epidemiological data are used to control a pandemic.', 'Incidence per 100 000, R number, doubling time, CFR; testing and contact tracing; modelling to predict hospital demand; targeting measures (distancing, masks, lockdowns); vaccination coverage and herd immunity; limitations of data.', 6)],
  )


@R.add('ch04-st5', 'C3', (1, 4), 'numerical')
def epi_rates(rng, slot):
    pop = pick(rng, [250_000, 400_000, 650_000, 1_200_000, 2_500_000])
    cases = rng.randint(300, 6000)
    deaths = max(1, round(cases * rng.uniform(0.004, 0.03)))
    inc = cases / pop * 100_000
    cfr = 100 * deaths / cases
    city = pick(rng, CITIES)
    stem = f'In one month, {city} (population {pop:,}) recorded {cases:,} new confirmed cases of an infectious disease and {deaths} deaths among them. Calculate the incidence per 100 000 and the case fatality rate.'.replace(',', ' ')
    ans = f'incidence {inc:.0f} per 100 000; CFR {cfr:.1f} %'
    key = f'{cases}/{pop} × 100 000 = {inc:.0f} (A1); {deaths}/{cases} × 100 = {cfr:.1f} % (A1).'
    if slot.d >= 4:
        stem += ' Suggest why the CFR may overestimate the risk of dying for an infected person.'
        return num(stem, ans + '; many mild/asymptomatic infections are not tested, so the true number of infections is larger', key + ' Undetected cases (R1).', 3)
    return num(stem, ans, key, 2)


@R.add('ch04-st5', 'C3', (2, 5), 'numerical')
def r_growth(rng, slot):
    r = pick(rng, [1.3, 1.5, 2, 2.5, 3])
    n0 = pick(rng, [5, 10, 20, 50])
    g = pick(rng, [3, 4, 5, 6])
    ser = pick(rng, [4, 5, 6, 7])
    new = n0 * r ** (g - 1)
    stem = (f'At the start of an outbreak there are {n0} cases (generation 1). Each case infects on average {r:g} others, and the time between generations is about {ser} days. '
            f'Calculate the expected number of new cases in generation {g}, and the time after the first cases at which this generation appears.')
    return num(stem, f'about {new:.0f} cases; about {(g - 1) * ser} days', f'{n0} × {r:g}^{g - 1} (M1) = {new:.0f} (A1); {g - 1} × {ser} = {(g - 1) * ser} days (A1).', 3)


def _covid_dq(rng, slot):
    wk = list(range(1, 8))
    pop = pick(rng, [500_000, 800_000, 1_000_000])
    g = rng.uniform(1.4, 1.8)
    peak = 4
    c0 = rng.randint(40, 90)
    cases = []
    c = c0
    for i in wk:
        cases.append(round(c))
        c = c * (g if i < peak else rng.uniform(0.55, 0.75))
    inc = [x / pop * 100_000 for x in cases]
    intro = (f'Weekly new confirmed cases of COVID-19 in a town of {pop:,} people are shown. A mask mandate and distancing rules were introduced at the end of week {peak}.\n\n'.replace(',', ' ')
             + table(['Week', 'New cases'], list(zip(wk, cases))))
    gr = cases[2] / cases[1]
    parts = [
        ('State the week with the highest number of new cases.', f'week {cases.index(max(cases)) + 1}', 'Correct week (A1).', 1),
        ('Calculate the weekly incidence per 100 000 in week 4.', f'{inc[3]:.0f} per 100 000', f'{cases[3]}/{pop} × 100 000 (M1) = {inc[3]:.0f} (A1).', 2),
        ('Calculate the weekly growth factor between weeks 2 and 3.', f'{gr:.2f}', f'{cases[2]}/{cases[1]} = {gr:.2f} (A1).', 1),
        ('Describe the trend in cases over the seven weeks.', 'Cases increased rapidly (approximately exponentially) to a peak in week 4/5, then decreased.', 'Increase (A1); peak (A1); decrease (A1).', 3),
        ('Evaluate the claim that the mask mandate caused the fall in cases.', 'The fall began after the mandate, which supports it; but correlation is not causation – other factors (changed behaviour, immunity, testing changes, weather) may contribute; no control town.', 'Supporting point (A1); limitation (A1).', 2),
        ('Explain how masks and distancing reduce transmission of SARS-CoV-2.', 'The virus spreads in respiratory droplets/aerosols; masks trap droplets and distancing reduces exposure, lowering the reproduction number.', 'Mode of transmission (A1); reduce R (A1).', 2),
        ('Suggest why recorded cases may underestimate the true number of infections.', 'Asymptomatic or mild cases not tested; limited testing capacity; false negatives.', 'Valid reason (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch04-st5', _covid_dq)


# =============================================================================================
# ch05 C4.1 Populations and communities and C4.2 Transfers of energy and matter
# =============================================================================================
S('ch05-st1',
  terms=[('population', 'a group of organisms of the same species living in the same area at the same time that can interbreed'),
         ('carrying capacity', 'the maximum population size of a species that an environment can support sustainably'),
         ('capture–mark–release–recapture', 'a method of estimating the size of a population of mobile animals by marking a sample, releasing it and recapturing a second sample'),
         ('Lincoln index', 'the estimate of population size N = M × C / R, where M is the number marked, C the number in the second sample and R the number of marked individuals recaptured'),
         ('random sampling', 'sampling in which every individual or position has an equal chance of being chosen, to avoid bias'),
         ('sigmoid growth curve', 'an S-shaped population growth curve with a lag phase, an exponential phase, a transitional phase and a plateau at carrying capacity'),
         ('density-dependent factor', 'a factor, such as competition, predation or disease, whose effect on a population increases as population density increases')],
  facts=[('Which method is used to estimate the population size of a sessile species such as a plant?', 'random quadrat sampling', ['capture–mark–release–recapture', 'pitfall traps only', 'counting every individual on Earth'], 'Plants do not move.'),
         ('What limits population growth in the plateau phase?', 'density-dependent factors such as competition for resources, predation and disease', ['unlimited resources', 'increased birth rate', 'lack of mutation'], 'Birth rate ≈ death rate.'),
         ('What is the equation of the Lincoln index?', 'N = M × C / R', ['N = M + C − R', 'N = R × C / M', 'N = M / (C × R)'], 'M marked, C second sample, R recaptured marked.'),
         ('Which is a density-independent factor?', 'a severe frost', ['competition for food', 'disease spread', 'predation'], 'Its effect does not depend on density.'),
         ('In which phase of the sigmoid curve is birth rate much greater than death rate?', 'the exponential phase', ['the plateau', 'the lag phase only', 'the decline phase'], 'Resources not limiting.')],
  mc2=[('Why must marks used in capture–recapture not make animals more visible to predators?', 'Marked animals would be eaten more, so fewer are recaptured and N is overestimated.', ['Marked animals would breed more.', 'It would make N underestimated.', 'It has no effect.'], 'Assumption of equal survival.'),
       ('Why does a population stop growing at carrying capacity?', 'Density-dependent factors increase the death rate and/or reduce the birth rate until they are equal.', ['All individuals stop reproducing.', 'Density-independent factors stop.', 'Mutation stops.'], 'Negative feedback.'),
       ('Why is a population in a new, resource-rich habitat able to grow exponentially?', 'There are few limiting factors, so birth rate greatly exceeds death rate.', ['Death rate is higher than birth rate.', 'Carrying capacity has been reached.', 'There is intense competition.'], 'No resource limits.'),
       ('Why should quadrats be placed using random coordinates?', 'To avoid bias in choosing where to sample.', ['To sample only the densest areas.', 'To make sampling faster.', 'To count every plant.'], 'Representative sample.')],
  mc3=[('In a study, 40 snails were marked and released. Later, 50 snails were caught, of which 8 were marked. What is the estimated population?', '250', ['98', '16', '10'], 'N = 40 × 50/8 = 250.'),
       ('Ten 1 m² quadrats contained a total of 34 daisies. The field is 2500 m². What is the estimated population?', '8500', ['340', '3.4', '25 000'], 'Mean 3.4 m⁻² × 2500 m².'),
       ('If many marked individuals emigrate between samples, how does this affect the Lincoln index estimate?', 'N is overestimated because fewer marked individuals are recaptured.', ['N is underestimated.', 'No effect.', 'N becomes zero.'], 'R is smaller than it should be.')],
  why=[('Explain how capture–mark–release–recapture is used to estimate a population and state its assumptions.', 'Capture a sample and mark (M) harmlessly; release and allow mixing; capture a second sample (C) and count marked (R); N = MC/R; assumptions: marks not lost and do not affect survival, random mixing, no births, deaths, immigration or emigration between samples, equal probability of capture.'),
       ('Explain the phases of a sigmoid population growth curve.', 'Lag phase: few individuals, slow growth while adapting; exponential phase: abundant resources, birth rate ≫ death rate; transitional phase: resources become limiting, density-dependent factors increase death rate; plateau at carrying capacity: birth rate = death rate.'),
       ('Explain how random quadrat sampling is used to estimate the population size of a plant species.', 'Mark out the area with tapes as axes; generate random coordinates; place quadrats; count individuals (or estimate % cover) in each; calculate mean per quadrat; scale up: mean density × total area; enough quadrats for reliability.')],
  contrast=[('density-dependent factors', 'density-independent factors', 'Density-dependent factors (competition, predation, disease) have a greater effect as population density increases and regulate population size; density-independent factors (floods, fires, frosts) affect populations regardless of density.'),
            ('random sampling', 'systematic sampling', 'Random sampling places quadrats at random coordinates to avoid bias, suitable for uniform habitats; systematic sampling places them at regular intervals, e.g. along a transect, to study change across an environmental gradient.')],
  misc=[('A population grows exponentially forever if it has enough food.', 'As the population increases other factors such as space, disease and predation limit it; all populations reach a carrying capacity.'),
        ('The Lincoln index counts every individual in the population.', 'It is a statistical estimate based on samples and depends on assumptions.'),
        ('The plateau phase means no births or deaths are occurring.', 'Births and deaths continue at equal rates.')],
  cases=[('yeast grown in a flask of glucose solution', 'Yeast numbers rise slowly, then exponentially, then level off and later decline as glucose runs out and ethanol accumulates.', 'sigmoid population growth', 'Resource limitation and toxic waste are density-dependent factors that set a carrying capacity.'),
         ('reindeer introduced to St Matthew Island in 1944', 'The population rose from 29 to about 6000 by 1963 and then crashed to 42 when lichen food was exhausted.', 'carrying capacity', 'Overshooting carrying capacity destroyed the food supply, causing a population crash.')],
  evaluate=[('Capture–mark–release–recapture gives an accurate estimate of population size.', ['simple and widely used for mobile animals', 'repeated sampling can improve the estimate'], ['assumptions such as no migration and equal catchability are often violated', 'trap-shy or trap-happy animals bias R'], 'It gives a useful estimate when assumptions are approximately met, but results should be treated with caution and checked by repeated sampling.')],
  extended=[('Explain how population size is estimated for sessile and motile organisms and evaluate the methods used.', 'Random quadrats, coordinates, density × area, percentage cover; capture–mark–release–recapture, Lincoln index N = MC/R; assumptions; evaluation: bias, sample size, mark loss, migration, catchability, edge effects.', 8),
            ('Describe and explain the sigmoid growth curve of a population with reference to limiting factors.', 'Lag phase; exponential phase (birth ≫ death, resources abundant); transitional phase; plateau at carrying capacity (birth = death); density-dependent factors: competition, predation, disease, waste; density-independent factors; example yeast or reindeer.', 6)],
  )


@R.add('ch05-st1', 'C3', (1, 5), 'numerical')
def lincoln(rng, slot):
    sp = pick(rng, ['woodlice', 'banded snails', 'ground beetles', 'field voles', 'grasshoppers', 'freshwater shrimps'])
    N = rng.randint(150, 1200)
    M = rng.randint(25, 80)
    C = rng.randint(30, 90)
    R_ = max(2, round(M * C / N))
    est = M * C / R_
    stem = f'A student captured and marked {M} {sp}, released them and returned a day later. A second sample of {C} contained {R_} marked individuals. Estimate the population size using the Lincoln index.'
    if slot.d >= 4:
        stem += ' State two assumptions of this method.'
        return num(stem, f'{est:.0f}; e.g. no migration, births or deaths between samples; marks not lost and do not affect survival',
                   f'N = MC/R = {M} × {C}/{R_} (M1) = {est:.0f} (A1); two assumptions (A1 A1).', 4)
    return num(stem, f'{est:.0f}', f'N = MC/R = {M} × {C}/{R_} (M1) = {est:.0f} (A1).', 2)


@R.add('ch05-st1', 'C3', (1, 4), 'mcq')
def lincoln_mcq(rng, slot):
    M = rng.randint(20, 60)
    C = rng.randint(20, 60)
    R_ = rng.randint(3, 12)
    est = M * C / R_
    stem = f'{M} animals were marked and released. A second sample of {C} included {R_} marked animals. What is the estimated population size?'
    return nmcq(rng, stem, f'{est:.0f}', [f'{M + C - R_:.0f}', f'{M * R_ / C:.0f}', f'{C * R_ / M:.1f}', f'{M * C:.0f}'], f'N = M × C/R = {M} × {C}/{R_} = {est:.0f}.')


@R.add('ch05-st1', 'C3', (1, 4), 'numerical')
def quadrat_pop(rng, slot):
    plant = pick(rng, ['dandelions', 'daisies', 'plantains', 'buttercups', 'orchids'])
    k = pick(rng, [8, 10, 12, 15])
    counts = [rng.randint(0, 9) for _ in range(k)]
    q = pick(rng, [0.25, 0.5, 1.0])
    area = pick(rng, [400, 1200, 2500, 5000, 8000])
    dens = sum(counts) / (k * q)
    stem = f'{k} quadrats, each {q} m², were placed randomly in a {area} m² meadow. The numbers of {plant} were: {", ".join(map(str, counts))}. Estimate the population of {plant} in the meadow.'
    return num(stem, f'{dens * area:.0f}', f'Total = {sum(counts)} in {k * q:g} m² (M1); density = {dens:.2f} m⁻² (M1); × {area} = {dens * area:.0f} (A1).', 3)


def _yeast_dq(rng, slot):
    t = [0, 6, 12, 18, 24, 30, 36, 42]
    K = rng.uniform(80, 120)
    r = rng.uniform(0.22, 0.30)
    n0 = rng.uniform(1.5, 3)
    pop = [round(K / (1 + (K / n0 - 1) * math.exp(-r * x)), 1) for x in t]
    intro = ('Yeast cells were grown in a flask of glucose solution at 25 °C. The population density (millions of cells per cm³) was estimated with a haemocytometer every 6 hours.\n\n'
             + table(['Time / h', 'Population / millions cm⁻³'], list(zip(t, pop))))
    rate = (pop[4] - pop[2]) / 12
    dbl = None
    for i in range(1, len(t)):
        if pop[i] >= 2 * pop[0]:
            dbl = t[i]
            break
    parts = [
        ('State the population density at 24 hours.', f'{pop[4]} million cm⁻³', f'{pop[4]} (A1).', 1),
        ('Calculate the mean rate of population increase between 12 and 24 hours.', f'{rate:.2f} million cm⁻³ h⁻¹', f'({pop[4]} − {pop[2]})/12 (M1) = {rate:.2f} (A1).', 2),
        ('Estimate the carrying capacity of the flask.', f'about {pop[-1]:.0f} million cm⁻³', f'Plateau value ≈ {pop[-1]:.0f} (A1).', 1),
        ('Identify the phases of growth shown and the times at which they occur.', 'Lag/slow growth 0–6 h; exponential about 6–24 h; transitional about 24–30 h; plateau after about 30–36 h.', 'Exponential phase identified (A1); plateau identified (A1); times consistent with data (A1).', 3),
        ('Explain why the population stops increasing.', 'Glucose becomes limiting and ethanol/toxic waste accumulates; competition increases; death rate rises to equal birth rate.', 'Limiting resource (A1); toxins (A1); birth = death (A1).', 3),
        ('Predict, with a reason, how the population would change if the flask were left for several more days.', 'It would decline as glucose is used up and ethanol rises to toxic levels, so death rate exceeds birth rate.', 'Decline (A1); reason (R1).', 2),
        ('Suggest one reason why haemocytometer counts are only estimates.', 'Only a small sample volume is counted; cells clump; live and dead cells are not distinguished; sampling/dilution errors.', 'Valid reason (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch05-st1', _yeast_dq)


S('ch05-st2',
  terms=[('community', 'all the populations of different species living and interacting in an area'),
         ('intraspecific competition', 'competition between individuals of the same species for limited resources'),
         ('interspecific competition', 'competition between individuals of different species for the same limited resources'),
         ('mutualism', 'an interaction between two species in which both benefit'),
         ('parasitism', 'a relationship in which one organism (the parasite) lives in or on a host and benefits while harming it'),
         ('keystone species', 'a species that has a disproportionately large effect on the structure of its community relative to its abundance'),
         ('allelopathy', 'the release by a plant of chemicals that inhibit the growth of other plants nearby'),
         ('invasive species', 'an alien species introduced to an area that spreads rapidly and harms native species or ecosystems')],
  facts=[('Which is an example of mutualism?', 'root nodules of legumes containing Rhizobium bacteria', ['a tapeworm in a human gut', 'a lion hunting a zebra', 'two barnacle species competing for rock'], 'Both partners benefit.'),
         ('Which species is the classic keystone predator studied by Robert Paine?', 'the starfish Pisaster ochraceus', ['the sea otter', 'the honeybee', 'the grey wolf'], 'Its removal reduced diversity.'),
         ('Which statistical test is used to test for an association between two species in quadrats?', 'the chi-squared test for association', ['the t-test', 'Simpson’s index', 'the Lincoln index'], 'Uses a 2 × 2 contingency table.'),
         ('Which is an example of allelopathy?', 'black walnut trees releasing juglone that inhibits other plants', ['bees pollinating flowers', 'lions forming prides', 'ticks feeding on deer'], 'Chemical inhibition.'),
         ('What did the reintroduction of wolves to Yellowstone in 1995 lead to?', 'reduced elk browsing and recovery of willow and aspen', ['extinction of beavers', 'an increase in elk numbers', 'no change in vegetation'], 'Trophic cascade.')],
  mc2=[('Why do predator and prey populations often oscillate?', 'More prey allows predators to increase; more predators reduce prey; fewer prey then reduces predators.', ['Predators and prey never affect each other.', 'Prey eat predators.', 'Both are controlled only by weather.'], 'Lynx–hare cycles.'),
       ('Why can removing a keystone species reduce biodiversity?', 'It has a large effect on community structure; without it one species may dominate or a trophic cascade occurs.', ['Keystone species are always the most abundant.', 'Biodiversity always increases.', 'Other species cannot be affected.'], 'Disproportionate effect.'),
       ('Why must the expected frequency in each cell be at least 5 in a chi-squared test?', 'Small expected values make the chi-squared statistic unreliable.', ['The formula cannot be calculated otherwise.', 'It makes p equal 0.05.', 'It ensures a significant result.'], 'Validity of the test.'),
       ('Why is pathogenicity considered an interspecific relationship?', 'A pathogen of one species lives in and harms a host of another species.', ['It occurs within one species.', 'Pathogens benefit hosts.', 'It involves only plants.'], 'Interaction between species.')],
  mc3=[('Two species occurred together in 30 of 100 quadrats; A was in 50 and B in 40 quadrats in total. What is the expected number of quadrats with both, if they are independent?', '20', ['30', '45', '12'], '(50 × 40)/100 = 20.'),
       ('A chi-squared test for association gave χ² = 6.2 with 1 degree of freedom (critical value 3.84). What is concluded?', 'There is a significant association; reject the null hypothesis.', ['There is no association.', 'The species are the same.', 'The test is invalid.'], '6.2 > 3.84.'),
       ('After sea otters were hunted almost to extinction, kelp forests declined. Which explanation fits?', 'Sea urchins, normally eaten by otters, increased and grazed the kelp.', ['Otters eat kelp.', 'Kelp needs otters for pollination.', 'Urchins declined.'], 'Trophic cascade from a keystone predator.')],
  why=[('Explain how a chi-squared test is used to test for association between two plant species.', 'Record presence/absence of both species in many random quadrats; construct 2 × 2 contingency table; calculate expected frequencies (row total × column total / grand total); χ² = Σ(O − E)²/E; degrees of freedom = 1; compare with critical value 3.84 at p = 0.05; if greater, reject null hypothesis of no association.'),
       ('Explain why some species are described as keystone species.', 'They have a large effect relative to their abundance; e.g. Pisaster starfish prey on mussels, preventing them outcompeting other species; removal leads to reduced diversity; sea otters control urchins that would destroy kelp; wolves control elk, allowing vegetation recovery.'),
       ('Explain the effects of an invasive species on a native community.', 'Invasive species may have no natural predators or diseases; they outcompete native species for resources, prey on natives, introduce diseases or hybridise; native populations decline, biodiversity falls, e.g. cane toads in Australia.')],
  contrast=[('mutualism', 'parasitism', 'In mutualism both species benefit (e.g. Rhizobium and legumes); in parasitism the parasite benefits and the host is harmed (e.g. ticks on deer).'),
            ('intraspecific competition', 'interspecific competition', 'Intraspecific competition is between members of the same species, which have identical needs; interspecific competition is between different species with overlapping niches.')],
  misc=[('A significant chi-squared result proves that one species causes the presence of the other.', 'It shows an association; both may respond to the same environmental factor rather than one causing the other.'),
        ('Keystone species are always the most common species in an ecosystem.', 'Keystone species may be rare; it is their effect on community structure that is disproportionate.'),
        ('Predators always reduce biodiversity.', 'Keystone predators can increase biodiversity by preventing competitive exclusion.')],
  cases=[('Paine’s removal of Pisaster starfish on rocky shores', 'Removing the starfish from plots led to mussels dominating and the number of species falling from 15 to 8.', 'keystone species', 'The predator prevented one competitor from excluding others, maintaining diversity.'),
         ('wolves reintroduced into Yellowstone National Park', 'Elk numbers fell and browsing changed, and willows, aspens and beavers recovered.', 'trophic cascades', 'A top predator altered prey behaviour and numbers, affecting plants and other animals in the community.'),
         ('cane toads in Australia', 'Introduced in 1935 to control beetles, cane toads spread across northern Australia, poisoning native predators.', 'invasive species', 'With no natural predators and toxic skin they spread rapidly and reduced native predator populations.')],
  evaluate=[('Removing invasive species is always beneficial for native ecosystems.', ['invasive species reduce native biodiversity through competition and predation', 'eradication on islands has allowed seabirds to recover'], ['removal can have unexpected effects if natives now depend on the invasive species', 'eradication is costly and often impossible on large land masses'], 'Removal is usually beneficial, especially on islands, but must be planned using an ecosystem approach to avoid unintended consequences.')],
  extended=[('Describe the types of interspecific relationship in communities and explain the role of keystone species.', 'Herbivory, predation, interspecific competition, mutualism (Rhizobium, coral zooxanthellae), parasitism, pathogenicity; predator–prey cycles; keystone species: Pisaster, sea otter, wolves; trophic cascades; effect of removal.', 8),
            ('Explain how ecologists test for association between two species using quadrat data.', 'Null/alternative hypotheses; random quadrats; presence/absence; contingency table; expected values; χ² formula; df = 1; critical value 3.84; interpretation: positive/negative association, shared habitat preference or interaction; limitations.', 6)],
  )


def _assoc_counts(rng):
    n = pick(rng, [60, 80, 100, 120])
    pa, pb = rng.uniform(0.35, 0.65), rng.uniform(0.35, 0.65)
    k = rng.uniform(-0.12, 0.15)
    ab = round(n * max(0.06, pa * pb + k))
    a_only = round(n * pa) - ab
    b_only = round(n * pb) - ab
    neither = n - ab - a_only - b_only
    if min(ab, a_only, b_only, neither) < 3:
        return None
    o = [[ab, a_only], [b_only, neither]]
    e, chi = chi_assoc(o)
    if min(min(r) for r in e) < 5:
        return None
    return n, o, e, chi


ASSOC_PAIRS = [('heather', 'bilberry', 'a moorland'), ('sea plantain', 'thrift', 'a salt marsh'), ('rush', 'sphagnum moss', 'a wet meadow'),
               ('limpets', 'barnacles', 'a rocky shore'), ('bluebell', 'bramble', 'a woodland'), ('marram grass', 'sea holly', 'sand dunes')]


@R.add('ch05-st2', 'C3', (2, 5), 'numerical')
def assoc_calc(rng, slot):
    r = _assoc_counts(rng)
    if r is None:
        return None
    n, o, e, chi = r
    a, b, hab = pick(rng, ASSOC_PAIRS)
    sig = chi > 3.84
    pos = o[0][0] > e[0][0]
    stem = (f'In {hab}, {n} random quadrats were surveyed. {a.capitalize()} and {b} both occurred in {o[0][0]}; {a} alone in {o[0][1]}; {b} alone in {o[1][0]}; neither in {o[1][1]}. '
            f'Calculate χ² for association and state a conclusion (critical value 3.84, p = 0.05, 1 df).')
    concl = (f'significant {"positive" if pos else "negative"} association – reject H₀' if sig else 'no significant association – accept H₀')
    return num(stem, f'χ² = {chi:.2f}; {concl}',
               f'Expected values: {e[0][0]:.1f}, {e[0][1]:.1f}, {e[1][0]:.1f}, {e[1][1]:.1f} (M1); Σ(O − E)²/E (M1) = {chi:.2f} (A1); comparison with 3.84 and conclusion (A1).', 4)


@R.add('ch05-st2', 'C3', (1, 4), 'mcq')
def expected_mcq(rng, slot):
    n = pick(rng, [50, 60, 80, 100, 120, 150])
    ra = rng.randint(n // 4, 3 * n // 4)
    cb = rng.randint(n // 4, 3 * n // 4)
    e = ra * cb / n
    stem = f'In {n} quadrats species A occurred in {ra} and species B in {cb}. What is the expected number of quadrats containing both species if they are distributed independently?'
    return nmcq(rng, stem, f'{e:.1f}', [f'{(ra + cb) / 2:.1f}', f'{ra * cb / 100:.1f}' if n != 100 else f'{ra * cb / 50:.1f}', f'{n - e:.1f}', f'{e / 2:.1f}'],
                f'E = row total × column total / grand total = {ra} × {cb}/{n} = {e:.1f}.')


def _assoc_dq(rng, slot):
    r = _assoc_counts(rng)
    if r is None:
        return None
    n, o, e, chi = r
    a, b, hab = pick(rng, ASSOC_PAIRS)
    sig = chi > 3.84
    pos = o[0][0] > e[0][0]
    intro = (f'A student investigated whether {a} and {b} are associated in {hab}. Presence or absence of each species was recorded in {n} randomly placed quadrats.\n\n'
             + table(['', f'{b} present', f'{b} absent'], [(f'{a} present', o[0][0], o[0][1]), (f'{a} absent', o[1][0], o[1][1])]))
    parts = [
        (f'State the number of quadrats containing {a}.', f'{o[0][0] + o[0][1]}', f'{o[0][0]} + {o[0][1]} = {o[0][0] + o[0][1]} (A1).', 1),
        ('State a null hypothesis for this investigation.', f'There is no association between the distributions of {a} and {b}.', 'No association (A1).', 1),
        ('Calculate the expected number of quadrats containing both species.', f'{e[0][0]:.1f}', f'{o[0][0] + o[0][1]} × {o[0][0] + o[1][0]}/{n} (M1) = {e[0][0]:.1f} (A1).', 2),
        ('Calculate the value of χ².', f'{chi:.2f}', f'Expected values {e[0][0]:.1f}, {e[0][1]:.1f}, {e[1][0]:.1f}, {e[1][1]:.1f} (M1); Σ(O − E)²/E = {chi:.2f} (A1).', 2),
        ('Using a critical value of 3.84, state a conclusion.', (f'χ² > 3.84: reject H₀; significant {"positive" if pos else "negative"} association' if sig else 'χ² < 3.84: accept H₀; no significant association'),
         'Comparison (A1); conclusion including direction where significant (A1).', 2),
        ('Suggest one ecological reason for an association between two plant species.', 'Both prefer the same abiotic conditions (positive) or different conditions/competition/allelopathy (negative); mutualism.', 'Valid reason linked to direction (A1).', 1),
        ('Explain why quadrats were positioned randomly.', 'To avoid bias so that the sample is representative and the statistical test is valid.', 'Avoid bias (A1).', 1),
        ('Outline one limitation of using presence or absence data.', 'It ignores abundance; quadrat size affects results; a single visit may miss seasonal species.', 'Valid limitation (A1).', 1),
        ('Explain why a chi-squared test requires expected values of at least 5 in each cell.', 'With small expected values the χ² statistic is unreliable and the critical values do not apply; more quadrats would be needed.', 'Validity of test (A1); more samples needed (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch05-st2', _assoc_dq)


S('ch05-st3',
  terms=[('ecosystem', 'a community of organisms interacting with each other and with their abiotic environment'),
         ('trophic level', 'the position of an organism in a food chain, based on the number of energy transfers from producers'),
         ('autotroph', 'an organism that synthesises its own carbon compounds from inorganic substances using an external energy source (light or chemical)'),
         ('heterotroph', 'an organism that obtains carbon compounds by feeding on other organisms'),
         ('decomposer', 'a saprotroph that feeds on dead organic matter by secreting digestive enzymes and absorbing the products'),
         ('pyramid of energy', 'a diagram showing the energy flow through each trophic level per unit area per unit time (e.g. kJ m⁻² yr⁻¹)'),
         ('chemoautotroph', 'an autotroph that uses energy from oxidising inorganic chemicals, such as iron(II) or hydrogen sulfide, to make carbon compounds'),
         ('energy transfer efficiency', 'the percentage of energy at one trophic level that is incorporated into the biomass of the next')],
  facts=[('What is the original source of energy for almost all ecosystems?', 'sunlight', ['soil minerals', 'the Earth’s core', 'oxygen'], 'Captured by photosynthesis.'),
         ('What is the typical energy transfer efficiency between trophic levels?', 'about 10 %', ['about 90 %', 'about 50 %', 'about 0.01 %'], 'Most is lost.'),
         ('In what form is most energy lost from food chains?', 'heat from respiration', ['light', 'sound', 'chemical energy in CO₂'], 'Heat cannot be recycled.'),
         ('Which organisms use energy from oxidising iron(II) to fix carbon?', 'chemoautotrophic bacteria such as Acidithiobacillus', ['fungi', 'herbivores', 'algae in the dark'], 'Chemosynthesis.'),
         ('What are the units of a pyramid of energy?', 'kJ m⁻² yr⁻¹', ['kg', 'number of individuals', 'm s⁻¹'], 'Energy per area per time.')],
  mc2=[('Why are food chains rarely longer than four or five trophic levels?', 'So much energy is lost at each transfer that too little remains to support further levels.', ['Matter runs out.', 'Top predators eat producers.', 'Decomposers prevent it.'], 'About 90 % lost per level.'),
       ('Why can a pyramid of energy never be inverted?', 'Energy is lost at every transfer, so each level has less energy than the one below.', ['Producers are always larger.', 'Energy is recycled.', 'Consumers photosynthesise.'], 'Second law of thermodynamics.'),
       ('Why are ecosystems described as open systems?', 'Energy and matter can enter and leave them.', ['Nothing enters or leaves.', 'Only energy is recycled.', 'Only matter enters.'], 'Light enters; heat leaves.'),
       ('Why is energy transfer from producers to herbivores often less efficient than from herbivores to carnivores?', 'Plant material contains much cellulose and lignin that is hard to digest, so more is egested.', ['Herbivores do not respire.', 'Plants contain no energy.', 'Carnivores eat bones.'], 'Digestibility.')],
  mc3=[('Producers fix 24 000 kJ m⁻² yr⁻¹ and primary consumers 1800 kJ m⁻² yr⁻¹. What is the transfer efficiency?', '7.5 %', ['13 %', '0.075 %', '75 %'], '1800/24 000 × 100 = 7.5 %.'),
       ('Which is a correct reason for energy not passing from grass to cattle?', 'Some grass is not eaten, some is egested in faeces, and much is used in respiration.', ['Energy is recycled to the grass.', 'Cattle photosynthesise.', 'Grass stores energy as heat.'], 'Losses at each step.'),
       ('A food chain has 10 000 kJ in producers and 10 % efficiency at each step. How much energy reaches the tertiary consumers?', '10 kJ', ['100 kJ', '1000 kJ', '1 kJ'], '10 000 → 1000 → 100 → 10.')],
  why=[('Explain why energy is lost between trophic levels.', 'Not all of the organisms at one level are eaten; some parts are indigestible and egested; energy is used in respiration and lost as heat; energy remains in dead organisms and is passed to decomposers; only about 10 % becomes biomass in the next level.'),
       ('Explain the roles of decomposers in ecosystems.', 'Saprotrophic bacteria and fungi secrete enzymes onto dead organic matter and absorb products; they release energy from detritus through respiration; they release inorganic nutrients (e.g. nitrates, phosphates) and CO₂ for reuse by producers, recycling matter.'),
       ('Explain why energy flows through ecosystems while chemical elements are recycled.', 'Energy enters as light, is converted to chemical energy and is ultimately lost as heat, which cannot be converted back by organisms; elements such as carbon and nitrogen are reused as decomposers return them to the abiotic environment.')],
  contrast=[('autotrophs', 'heterotrophs', 'Autotrophs make their own carbon compounds from inorganic substances using light or chemical energy; heterotrophs obtain carbon compounds by consuming other organisms.'),
            ('photoautotrophs', 'chemoautotrophs', 'Photoautotrophs use light energy in photosynthesis; chemoautotrophs use energy released by oxidising inorganic substances.')],
  misc=[('Energy is recycled in ecosystems just like carbon.', 'Energy flows through ecosystems and is lost as heat; only matter is recycled.'),
        ('Herbivores convert most of the energy in plants into their own biomass.', 'Typically only about 10 % is converted; the rest is lost in faeces, respiration and uneaten material.'),
        ('Decomposers are not part of food webs.', 'Decomposers receive energy from all trophic levels as dead matter and recycle nutrients.')],
  cases=[('the Silver Springs ecosystem in Florida', 'H. T. Odum measured energy flow: producers about 87 000 kJ m⁻² yr⁻¹ and top carnivores only about 90 kJ m⁻² yr⁻¹.', 'energy loss along food chains', 'Large losses at each trophic level produce a steep pyramid of energy.'),
         ('deep-sea hydrothermal vent communities', 'Tube worms and clams depend on bacteria that oxidise hydrogen sulfide from vents.', 'chemoautotrophy', 'Chemoautotrophic bacteria are the producers, supplying energy to the community without sunlight.')],
  evaluate=[('Eating lower in the food chain is a more efficient way to feed the human population.', ['about 90 % of energy is lost at each trophic level, so plant food supports more people per hectare', 'less land and water are needed'], ['some land is unsuitable for crops but supports grazing', 'animal products supply some nutrients (B12, iron) efficiently'], 'A diet with more plant food is more energy-efficient and sustainable, although some grazing on non-arable land remains useful.')],
  extended=[('Explain how energy flows through an ecosystem and why pyramids of energy have the shape they do.', 'Sunlight; photosynthesis by producers; chemical energy in carbon compounds; feeding passes energy; losses (respiration as heat, egestion, uneaten parts, death to decomposers); ~10 % efficiency; units kJ m⁻² yr⁻¹; pyramids always upright; limits food chain length; Silver Springs.', 8),
            ('Distinguish between autotrophs, heterotrophs and saprotrophs and explain their roles in ecosystems.', 'Photo- and chemoautotrophs fix carbon; consumers ingest; saprotrophs secrete enzymes externally; decomposers recycle nutrients; detritivores; energy flow and nutrient cycling.', 6)],
  )


@R.add('ch05-st3', 'C3', (1, 5), 'numerical')
def efficiency(rng, slot):
    a = rng.randint(8000, 90000)
    eff = rng.uniform(0.04, 0.16)
    b = round(a * eff, -1)
    lv = pick(rng, [('producers', 'primary consumers'), ('primary consumers', 'secondary consumers'), ('secondary consumers', 'tertiary consumers')])
    e = 100 * b / a
    stem = f'In an ecosystem the energy in {lv[0]} is {a:,} kJ m⁻² yr⁻¹ and in {lv[1]} {b:,.0f} kJ m⁻² yr⁻¹. Calculate the efficiency of energy transfer.'.replace(',', ' ')
    if slot.d >= 4:
        stem += ' Give two reasons why the efficiency is so low.'
        return num(stem, f'{e:.1f} %; e.g. energy lost as heat in respiration; parts not eaten or egested as faeces',
                   f'{b:.0f}/{a} × 100 (M1) = {e:.1f} % (A1); two reasons (A1 A1).', 4)
    return num(stem, f'{e:.1f} %', f'{b:.0f}/{a} × 100 (M1) = {e:.1f} % (A1).', 2)


@R.add('ch05-st3', 'C3', (1, 4), 'mcq')
def efficiency_mcq(rng, slot):
    a = pick(rng, [12000, 15000, 20000, 25000, 40000, 50000])
    b = round(a * rng.uniform(0.05, 0.15), -2)
    e = 100 * b / a
    return nmcq(rng, f'Primary consumers receive {a:,} kJ m⁻² yr⁻¹ from producers; secondary consumers receive {b:,.0f} kJ m⁻² yr⁻¹. What is the transfer efficiency?'.replace(',', ' '),
                f'{e:.1f} %', [f'{100 - e:.1f} %', f'{a / b:.1f} %', f'{e / 10:.2f} %', f'{e * 10:.0f} %'], f'{b:.0f}/{a} × 100 = {e:.1f} %.')


def _energy_dq(rng, slot):
    gpp = rng.randint(70000, 95000)
    r_p = round(gpp * rng.uniform(0.55, 0.65))
    npp = gpp - r_p
    herb = round(npp * rng.uniform(0.09, 0.15))
    carn = round(herb * rng.uniform(0.08, 0.14))
    top = round(carn * rng.uniform(0.05, 0.12))
    intro = ('The table shows energy flow (kJ m⁻² yr⁻¹) in a freshwater spring ecosystem.\n\n'
             + table(['Trophic level', 'Energy / kJ m⁻² yr⁻¹'], [('Producers – gross primary production', gpp), ('Producers – respiration', r_p), ('Producers – net primary production', '?'),
                                                               ('Herbivores', herb), ('Carnivores', carn), ('Top carnivores', top)]))
    e1, e2, e3 = 100 * herb / npp, 100 * carn / herb, 100 * top / carn
    parts = [
        ('Calculate the net primary production.', f'{npp} kJ m⁻² yr⁻¹', f'NPP = GPP − R = {gpp} − {r_p} = {npp} (A1).', 1),
        ('Calculate the efficiency of energy transfer from producers (NPP) to herbivores.', f'{e1:.1f} %', f'{herb}/{npp} × 100 (M1) = {e1:.1f} % (A1).', 2),
        ('Calculate the efficiency of transfer from carnivores to top carnivores.', f'{e3:.1f} %', f'{top}/{carn} × 100 = {e3:.1f} % (A1).', 1),
        ('Explain why the energy reaching top carnivores is so small.', 'Energy is lost at each trophic level: respiration (heat), egestion, uneaten parts, death to decomposers; only about 10 % passes on at each step.', 'Two losses (A1 A1); cumulative effect (A1).', 3),
        ('Sketch, in words, the shape of a pyramid of energy for this ecosystem and explain why it cannot be inverted.', 'Each bar is much narrower than the one below (steep pyramid); energy is lost at every transfer, so higher levels always have less energy.', 'Shape (A1); explanation (A1).', 2),
        ('Suggest why the efficiency from herbivores to carnivores differs from that from producers to herbivores.', ('Herbivores digest less of their food (cellulose), so more energy is egested' if e2 > e1 else 'Carnivores spend much energy hunting and maintaining body temperature') + '; differences in digestibility and respiratory losses.', 'Valid reason (A1).', 1),
        ('Suggest two reasons why less than half of gross primary production is available to herbivores.', 'Producers use much of the energy in their own respiration (lost as heat); some biomass dies or is not eaten, or is indigestible.', 'Respiration (A1); not eaten/indigestible (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch05-st3', _energy_dq)


S('ch05-st4',
  terms=[('gross primary production', 'the total amount of energy (or carbon) fixed by producers in photosynthesis per unit area per unit time'),
         ('net primary production', 'gross primary production minus energy used by producers in respiration; the energy available to consumers (NPP = GPP − R)'),
         ('carbon sink', 'a reservoir that absorbs more carbon than it releases, such as growing forests, oceans and peat'),
         ('carbon source', 'a reservoir or process that releases more carbon than it absorbs, such as combustion of fossil fuels'),
         ('carbon flux', 'the rate of transfer of carbon between pools, measured e.g. in gigatonnes per year'),
         ('Keeling curve', 'the record of atmospheric CO₂ concentration measured at Mauna Loa since 1958, showing an annual cycle and a long-term rise'),
         ('secondary production', 'the accumulation of carbon compounds (biomass) in consumers per unit area per unit time')],
  facts=[('Where has atmospheric CO₂ been measured continuously since 1958?', 'Mauna Loa, Hawaii', ['Antarctica only', 'London', 'Mount Everest'], 'Charles Keeling began the record.'),
         ('Approximately what is the current atmospheric CO₂ concentration?', 'about 420 ppm', ['about 280 ppm', 'about 4200 ppm', 'about 42 ppm'], 'Pre-industrial ~280 ppm.'),
         ('Which biome has the highest net primary productivity per unit area on land?', 'tropical rainforest', ['tundra', 'desert', 'boreal forest'], 'Warm, wet and light all year.'),
         ('Which process releases carbon stored in fossil fuels?', 'combustion', ['photosynthesis', 'fossilisation', 'diffusion into oceans'], 'Produces CO₂.'),
         ('How does carbon enter the oceans from the atmosphere?', 'by CO₂ dissolving in water and forming hydrogencarbonate ions', ['as methane only', 'as glucose', 'only through rivers'], 'Ocean is a major sink.')],
  mc2=[('Why does atmospheric CO₂ at Mauna Loa fall each northern summer?', 'Increased photosynthesis in the large land area of the Northern Hemisphere removes CO₂.', ['Respiration increases in summer.', 'Volcanoes stop erupting.', 'Fossil fuel burning stops.'], 'Seasonal cycle.'),
       ('Why is NPP rather than GPP the energy available to herbivores?', 'Some fixed energy is used by producers in their own respiration.', ['Herbivores eat only roots.', 'GPP is stored as heat.', 'NPP includes respiration.'], 'NPP = GPP − R.'),
       ('Why can peat bogs act as long-term carbon sinks?', 'Waterlogged, acidic, anaerobic conditions inhibit decomposition, so organic matter accumulates.', ['Peat photosynthesises at night.', 'Bogs release large amounts of CO₂.', 'Bacteria decompose peat rapidly.'], 'Partial decomposition.'),
       ('Why does deforestation increase atmospheric CO₂?', 'Trees are burnt or decompose, releasing CO₂, and less photosynthesis removes CO₂.', ['Trees release O₂ when cut.', 'Soil absorbs more CO₂.', 'It increases photosynthesis.'], 'Source and lost sink.')],
  mc3=[('A crop has a GPP of 3.5 kg m⁻² yr⁻¹ (dry mass) and loses 1.4 kg m⁻² yr⁻¹ in respiration. What is its NPP?', '2.1 kg m⁻² yr⁻¹', ['4.9 kg m⁻² yr⁻¹', '0.4 kg m⁻² yr⁻¹', '2.5 kg m⁻² yr⁻¹'], 'NPP = GPP − R.'),
       ('Atmospheric CO₂ rose from 316 ppm in 1959 to 420 ppm in 2023. What was the mean rate of increase?', 'about 1.6 ppm per year', ['about 104 ppm per year', 'about 0.16 ppm per year', 'about 16 ppm per year'], '(420 − 316)/64 = 1.6.'),
       ('Why is the seasonal fluctuation in CO₂ smaller in the Southern Hemisphere?', 'There is much less land and vegetation in the Southern Hemisphere.', ['There is no summer there.', 'Plants there do not photosynthesise.', 'It has more volcanoes.'], 'Land area difference.')],
  why=[('Explain the carbon cycle, including the processes that transfer carbon between pools.', 'Photosynthesis fixes atmospheric CO₂ into carbon compounds; feeding passes carbon along food chains; respiration by all organisms releases CO₂; decomposers release CO₂ from dead matter; incomplete decomposition forms peat, coal, oil and gas; combustion releases CO₂; CO₂ dissolves in oceans; limestone forms from shells.'),
       ('Explain the annual and long-term trends shown by the Keeling curve.', 'Annual fluctuation: CO₂ falls in the Northern Hemisphere summer because photosynthesis exceeds respiration, and rises in winter when respiration and decomposition exceed photosynthesis; long-term rise from about 315 ppm (1958) to over 420 ppm because of fossil fuel combustion and deforestation.'),
       ('Explain why tropical rainforests have a higher net primary productivity than deserts or tundra.', 'High light intensity all year, high temperatures for enzyme activity, abundant water; long growing season; deserts lack water, tundra is cold with a short growing season; so GPP is high and NPP remains high despite respiration.')],
  contrast=[('gross primary production', 'net primary production', 'GPP is the total energy or carbon fixed by producers; NPP is what remains after producers’ respiration and is available as biomass for consumers.'),
            ('carbon sinks', 'carbon sources', 'Carbon sinks remove more carbon from the atmosphere than they release (growing forests, oceans, peat); carbon sources release more than they absorb (combustion, deforestation, decomposition of peat).')],
  misc=[('All the carbon fixed by plants is available to herbivores.', 'Plants use a large proportion (often half) in respiration; only NPP is available.'),
        ('The seasonal drop in CO₂ shows that pollution stops in summer.', 'It is due to increased photosynthesis in Northern Hemisphere summer.'),
        ('Oceans are a carbon source.', 'Oceans currently absorb about a quarter of human CO₂ emissions and are a carbon sink, although this causes acidification.')],
  cases=[('the Keeling curve at Mauna Loa', 'CO₂ has risen from about 315 ppm in 1958 to over 420 ppm, with an annual oscillation of about 6 ppm.', 'human effects on the carbon cycle', 'Combustion of fossil fuels adds CO₂ faster than sinks remove it, while seasonal photosynthesis causes the oscillation.'),
         ('peatland drainage in Southeast Asia', 'Draining and burning tropical peat swamps for oil palm releases large amounts of CO₂.', 'carbon sinks becoming sources', 'Aerobic conditions allow decomposition and fire releases stored carbon, converting a sink into a source.')],
  evaluate=[('Planting trees is the best way to reduce atmospheric CO₂ concentrations.', ['growing forests are carbon sinks and have biodiversity co-benefits'], ['trees take decades to grow and may burn or be felled, releasing carbon', 'reducing fossil fuel emissions is more effective; land is limited'], 'Tree planting helps, but reducing fossil-fuel emissions is essential; reforestation should complement, not replace, emission cuts.')],
  extended=[('Describe the carbon cycle and explain how human activities have altered it, with reference to the Keeling curve.', 'Pools and fluxes; photosynthesis, respiration, feeding, decomposition, fossilisation (peat, coal, oil), combustion, ocean dissolution, limestone; human: fossil fuels, deforestation, peat drainage; Keeling curve: annual oscillation explained, long-term rise; consequences.', 8),
            ('Explain the difference between gross and net primary production and the factors that affect primary productivity in different biomes.', 'GPP, NPP = GPP − R; units; factors: light, temperature, water, CO₂, nutrients, growing season; rainforest vs desert vs tundra; secondary production; implications for food chains.', 6)],
  )


@R.add('ch05-st4', 'C3', (1, 4), 'numerical')
def npp_calc(rng, slot):
    eco = pick(rng, ['a tropical rainforest', 'a temperate grassland', 'a wheat field', 'a salt marsh', 'a boreal forest'])
    gpp = round(rng.uniform(1.5, 8.0), 1)
    rp = round(gpp * rng.uniform(0.4, 0.65), 1)
    npp = gpp - rp
    stem = f'The gross primary production of {eco} is {gpp} kg m⁻² yr⁻¹ (dry biomass) and plant respiration uses {rp} kg m⁻² yr⁻¹. Calculate the NPP and the percentage of GPP used in respiration.'
    return num(stem, f'NPP = {npp:.1f} kg m⁻² yr⁻¹; {100 * rp / gpp:.0f} %', f'NPP = GPP − R = {gpp} − {rp} = {npp:.1f} (A1); {rp}/{gpp} × 100 = {100 * rp / gpp:.0f} % (A1).', 2)


def _keeling_dq(rng, slot):
    yrs = [1960, 1970, 1980, 1990, 2000, 2010, 2020]
    base = [317.0, 325.7, 338.8, 354.4, 369.7, 389.9, 414.2]
    co2 = [round(x + rng.uniform(-0.6, 0.6), 1) for x in base]
    amp = round(rng.uniform(5.5, 7.0), 1)
    intro = ('The mean annual atmospheric CO₂ concentration at Mauna Loa, Hawaii, is shown. Within each year the concentration also varies seasonally, '
             f'with a difference of about {amp} ppm between the May maximum and the September/October minimum.\n\n' + table(['Year', 'Mean CO₂ / ppm'], list(zip(yrs, co2))))
    r1 = (co2[1] - co2[0]) / 10
    r2 = (co2[-1] - co2[-2]) / 10
    p = pct_change(co2[0], co2[-1])
    parts = [
        ('State the CO₂ concentration in 1990.', f'{co2[3]} ppm', f'{co2[3]} (A1).', 1),
        ('Calculate the mean rate of increase in CO₂ between 1960 and 1970, and between 2010 and 2020.', f'{r1:.2f} and {r2:.2f} ppm yr⁻¹', f'({co2[1]} − {co2[0]})/10 = {r1:.2f} (A1); ({co2[-1]} − {co2[-2]})/10 = {r2:.2f} (A1).', 2),
        ('Calculate the percentage increase in CO₂ from 1960 to 2020.', f'{signed(p)} %', f'({co2[-1]} − {co2[0]})/{co2[0]} × 100 (M1) = {signed(p)} % (A1).', 2),
        ('Describe the long-term trend.', 'CO₂ concentration increases every decade and the rate of increase is accelerating.', 'Increase (A1); accelerating rate (A1).', 2),
        ('Explain the seasonal variation in CO₂ concentration.', 'In the Northern Hemisphere spring/summer, photosynthesis exceeds respiration, so CO₂ falls to a minimum in autumn; in winter, respiration and decomposition exceed photosynthesis so CO₂ rises to a maximum in May.', 'Photosynthesis in summer (A1); respiration/decomposition in winter (A1); Northern Hemisphere land mass (A1).', 3),
        ('Explain the causes of the long-term rise.', 'Combustion of fossil fuels releases carbon stored for millions of years; deforestation releases CO₂ and reduces photosynthesis; emissions exceed uptake by sinks.', 'Fossil fuels (A1); deforestation (A1).', 2),
        ('Suggest why Mauna Loa is a good site for measuring global CO₂.', 'Remote, high altitude, far from local sources of pollution and vegetation, so measurements represent well-mixed air.', 'Valid reason (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch05-st4', _keeling_dq)


# =============================================================================================
# ch06 D1.1–D1.3 DNA replication, protein synthesis and mutation
# =============================================================================================
S('ch06-st1',
  terms=[('semi-conservative replication', 'DNA replication in which each new double helix contains one original (parental) strand and one newly synthesised strand'),
         ('helicase', 'the enzyme that unwinds the double helix and separates the two strands by breaking hydrogen bonds between bases'),
         ('DNA polymerase', 'the enzyme that adds nucleotides to a growing DNA strand in the 5′ → 3′ direction, using the other strand as a template'),
         ('polymerase chain reaction (PCR)', 'a technique that amplifies a specific DNA sequence by repeated cycles of denaturation, primer annealing and extension using a heat-stable DNA polymerase'),
         ('primer', 'a short single-stranded nucleic acid sequence that binds to a complementary sequence and provides a starting point for DNA polymerase'),
         ('gel electrophoresis', 'a technique that separates DNA fragments (or proteins) by size as they move through a gel in an electric field'),
         ('Okazaki fragments', 'short sections of DNA synthesised discontinuously on the lagging strand during replication, later joined by DNA ligase'),
         ('DNA ligase', 'an enzyme that joins DNA fragments by forming phosphodiester bonds between adjacent nucleotides')],
  facts=[('Which enzyme used in PCR comes from the bacterium Thermus aquaticus?', 'Taq polymerase', ['helicase', 'DNA ligase', 'reverse transcriptase'], 'It is heat-stable.'),
         ('At about what temperature is DNA denatured in PCR?', '95 °C', ['37 °C', '55 °C', '72 °C'], 'Hydrogen bonds break.'),
         ('Towards which electrode do DNA fragments move in gel electrophoresis?', 'the positive electrode (anode)', ['the negative electrode', 'neither – they stay still', 'both equally'], 'Phosphate groups are negative.'),
         ('In which direction does DNA polymerase synthesise new DNA?', '5′ → 3′', ['3′ → 5′', 'both directions equally', 'from the middle outwards only'], 'Adds to the 3′ end.'),
         ('Which isotope did Meselson and Stahl use to label “heavy” DNA?', 'nitrogen-15', ['carbon-14', 'phosphorus-32', 'sulfur-35'], 'Bacteria grown on ¹⁵N medium.'),
         ('Which fragments move furthest in gel electrophoresis?', 'the smallest fragments', ['the largest fragments', 'all equally', 'only circular fragments'], 'Smaller fragments pass through the gel more easily.')],
  mc2=[('Why is replication described as semi-conservative?', 'Each new molecule has one parental strand and one new strand.', ['Both strands are new.', 'Half the bases are changed.', 'Only half the DNA is copied.'], 'One old, one new.'),
       ('Why is a heat-stable polymerase needed in PCR?', 'The reaction is repeatedly heated to 95 °C, which would denature most enzymes.', ['It works faster at low temperatures.', 'It binds primers.', 'It denatures DNA.'], 'Taq polymerase.'),
       ('Why does complementary base pairing ensure accurate replication?', 'Each base on the template pairs only with its complement (A–T, C–G), so the new strand’s sequence is determined.', ['Bases pair randomly.', 'Helicase checks each base.', 'Only purines are copied.'], 'Specific pairing.'),
       ('Why is one strand replicated discontinuously?', 'The strands are antiparallel and DNA polymerase can only add nucleotides to a 3′ end.', ['One strand is RNA.', 'Helicase only unwinds one strand.', 'The lagging strand has no bases.'], 'Okazaki fragments.')],
  mc3=[('After one generation in ¹⁴N medium, DNA from bacteria previously grown in ¹⁵N formed a single band of intermediate density. Which model was ruled out?', 'conservative replication', ['semi-conservative replication', 'dispersive replication', 'none of the models'], 'Conservative would give a heavy and a light band.'),
       ('Starting with 10 copies of a DNA sequence, how many copies are present after 20 PCR cycles?', 'about 10 million (10 × 2²⁰)', ['200', '400', 'about 10 thousand'], '2²⁰ ≈ 1.05 × 10⁶.'),
       ('A DNA profile from a crime scene shares all bands with suspect B but not suspect A. What is concluded?', 'Suspect B’s DNA matches the sample; suspect A is excluded.', ['Both suspects are guilty.', 'Suspect A is guilty.', 'No conclusion can be drawn.'], 'Matching band patterns.')],
  why=[('Explain the process of DNA replication.', 'Helicase unwinds the helix and breaks hydrogen bonds; each strand acts as a template; free nucleotides pair with complementary bases (A–T, C–G); DNA polymerase links nucleotides 5′ → 3′ by phosphodiester bonds; leading strand continuous, lagging strand in Okazaki fragments joined by ligase; result: two identical molecules, each semi-conservative.'),
       ('Explain the steps of the polymerase chain reaction.', 'Heat to about 95 °C to separate strands (denaturation); cool to about 55 °C so primers anneal to complementary sequences flanking the target; heat to about 72 °C for Taq polymerase to extend primers; repeat cycles, doubling the target each time.'),
       ('Explain how gel electrophoresis is used in DNA profiling.', 'DNA is amplified at short tandem repeat loci by PCR; samples are loaded into wells of a gel; an electric field is applied; negatively charged DNA moves towards the anode; smaller fragments move further; a DNA ladder of known sizes is used for comparison; band patterns are compared between samples.'),
       ('Explain how the Meselson–Stahl experiment supported semi-conservative replication.', 'E. coli grown in ¹⁵N medium so DNA heavy; transferred to ¹⁴N; DNA extracted and centrifuged in CsCl density gradient; after one generation one intermediate band (rules out conservative); after two generations intermediate and light bands (rules out dispersive).')],
  contrast=[('the leading strand', 'the lagging strand', 'The leading strand is synthesised continuously towards the replication fork; the lagging strand is synthesised away from the fork in short Okazaki fragments joined by DNA ligase.'),
            ('DNA replication in cells', 'PCR', 'Replication in cells uses helicase to separate strands and many enzymes (primase, ligase) at body temperature; PCR uses heat to separate strands, synthetic primers and Taq polymerase, and copies only a target sequence.')],
  misc=[('In replication, one double helix is entirely old and the other entirely new.', 'This is the conservative model, which Meselson and Stahl disproved; each new helix has one old and one new strand.'),
        ('Larger DNA fragments move further in gel electrophoresis.', 'Smaller fragments move further because they pass through the gel pores more easily.'),
        ('PCR copies the entire genome.', 'PCR amplifies only the sequence between the two primers.'),
        ('DNA polymerase can start a new strand without a primer.', 'DNA polymerase can only add nucleotides to an existing 3′ end, so a primer is needed.')],
  cases=[('the Meselson–Stahl experiment (1958)', 'E. coli moved from ¹⁵N to ¹⁴N medium gave one intermediate band after one generation, then intermediate and light bands.', 'semi-conservative replication', 'Each new molecule contained one heavy parental strand and one light new strand.'),
         ('DNA profiling in forensic investigations', 'Short tandem repeats are amplified by PCR from tiny samples and separated by electrophoresis.', 'PCR and gel electrophoresis', 'Each person’s STR band pattern is almost unique, so samples can be matched to individuals.'),
         ('PCR tests for SARS-CoV-2', 'Viral RNA is reverse-transcribed and specific sequences amplified; fluorescence shows positive samples.', 'PCR amplification', 'Exponential amplification allows tiny amounts of viral genetic material to be detected.')],
  evaluate=[('DNA profiling evidence alone should be enough to convict a suspect.', ['STR profiles at many loci give very low random-match probabilities', 'it has also freed wrongly convicted people'], ['contamination or transfer can place innocent DNA at a scene', 'presence of DNA does not prove a person committed the crime; relatives share profiles'], 'DNA profiling is powerful evidence but should be considered with other evidence, as it shows presence rather than guilt.')],
  extended=[('Explain the process of DNA replication and how experimental evidence supports the semi-conservative model.', 'Helicase; template strands; complementary base pairing; DNA polymerase 5′ → 3′; leading and lagging strands; Okazaki fragments; ligase; primase/primers; proofreading; Meselson–Stahl: ¹⁵N, ¹⁴N, density gradient, results after 1 and 2 generations.', 8),
            ('Outline the stages of PCR and explain how PCR and gel electrophoresis are used together in DNA profiling.', 'Denaturation 95 °C; annealing 55 °C; extension 72 °C; Taq; doubling per cycle; STR loci; electrophoresis; charge and size; ladder; comparison; uses in forensics and paternity.', 6)],
  )


@R.add('ch06-st1', 'C3', (1, 4), 'numerical')
def pcr_copies(rng, slot):
    n0 = pick(rng, [1, 2, 5, 10, 50, 100])
    c = pick(rng, [10, 15, 20, 25, 30])
    tot = n0 * 2 ** c
    stem = f'A PCR reaction starts with {n0} copies of a target DNA sequence. Assuming perfect doubling, calculate the number of copies after {c} cycles.'
    if slot.d >= 3:
        mins = pick(rng, [2, 3, 4])
        stem += f' If each cycle takes {mins} minutes, how long does the PCR take?'
        return num(stem, f'{tot:.3g} copies; {c * mins} minutes', f'{n0} × 2^{c} (M1) = {tot:.3g} (A1); {c} × {mins} = {c * mins} min (A1).', 3)
    return num(stem, f'{tot:.3g} copies', f'{n0} × 2^{c} (M1) = {tot:.3g} (A1).', 2)


@R.add('ch06-st1', 'C3', (2, 5), 'mcq')
def meselson_mcq(rng, slot):
    g = pick(rng, [2, 3, 4, 5])
    tot = 2 ** g
    hyb = 2
    stem = f'E. coli with only ¹⁵N DNA were transferred to ¹⁴N medium and allowed to replicate for {g} generations. What fraction of DNA molecules is hybrid (¹⁵N/¹⁴N)?'
    fr = Fraction(hyb, tot)
    return nmcq(rng, stem, str(fr), [str(Fraction(1, 2)) if fr != Fraction(1, 2) else '1/4', str(Fraction(1, g)), str(1 - fr), '0'],
                f'After {g} generations there are 2^{g} = {tot} molecules; only the 2 containing an original strand are hybrid: 2/{tot} = {fr}.')


def _meselson_dq(rng, slot):
    g = pick(rng, [3, 4])
    intro = ('Meselson and Stahl grew E. coli for many generations in medium containing ¹⁵N, then transferred them to medium containing only ¹⁴N. Samples were taken after each generation, '
             'DNA was extracted and centrifuged in a caesium chloride density gradient. The positions of bands were recorded.\n\n'
             + table(['Generations in ¹⁴N', 'Heavy (¹⁵N/¹⁵N) band', 'Intermediate band', 'Light (¹⁴N/¹⁴N) band'],
                     [(0, 'present', 'absent', 'absent'), (1, 'absent', 'present', 'absent'), (2, 'absent', 'present', 'present'), (g, 'absent', '?', '?')]))
    tot = 2 ** g
    lt = tot - 2
    parts = [
        ('State the result after one generation in ¹⁴N.', 'A single intermediate band only.', 'Intermediate band only (A1).', 1),
        ('Explain how the result after one generation rules out conservative replication.', 'Conservative replication would give one heavy and one light band; only an intermediate band was seen, so each molecule contained heavy and light DNA.', 'Prediction of conservative model (A1); comparison (R1).', 2),
        ('Explain how the result after two generations rules out dispersive replication.', 'Dispersive replication would give a single band of lighter-than-intermediate density; two bands (intermediate and light) were seen.', 'Prediction of dispersive model (A1); comparison (R1).', 2),
        (f'Predict the proportions of intermediate and light DNA after {g} generations.', f'intermediate {Fraction(2, tot)}, light {Fraction(lt, tot)} (ratio 2 : {lt})', f'{tot} molecules from each original (M1); 2 hybrid, {lt} light (A1).', 2),
        ('Explain why ¹⁵N was used to label the DNA.', 'Nitrogen is in the bases of DNA; ¹⁵N makes DNA denser so it can be separated from ¹⁴N DNA by density.', 'Nitrogen in bases (A1); density difference (A1).', 2),
        ('Outline the semi-conservative model of replication.', 'Each strand of the parental helix acts as a template; each new molecule has one original and one new strand.', 'Template strands (A1); one old + one new (A1).', 2),
        ('State the number of DNA molecules descended from one original molecule after three generations.', '8', '2³ = 8 (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch06-st1', _meselson_dq)


def _gel_dq(rng, slot):
    ladder = [5000, 3000, 2000, 1000, 500, 250]
    a = rng.uniform(52, 58)
    b = rng.uniform(16, 19)
    dist = [round(a - b * math.log10(s) + b * 2, 1) for s in ladder]
    if min(dist) <= 2:
        return None
    unk = rng.randint(400, 4000)
    du = round(a - b * math.log10(unk) + b * 2, 1)
    est = 10 ** ((a + 2 * b - du) / b)
    intro = ('A DNA sample was cut with a restriction enzyme and separated by gel electrophoresis alongside a DNA ladder. The distances moved from the well are shown.\n\n'
             + table(['Ladder fragment / bp', 'Distance moved / mm'], list(zip(ladder, dist))) + f'\n\nUnknown fragment X moved {du} mm.')
    i = max(j for j in range(len(ladder)) if dist[j] <= du)
    parts = [
        ('State which ladder fragments X lies between.', f'between {ladder[i]} and {ladder[i + 1]} bp', 'Correct pair (A1).', 1) if i + 1 < len(ladder) else ('State the distance moved by the 1000 bp fragment.', f'{dist[3]} mm', f'{dist[3]} (A1).', 1),
        ('Distance moved is proportional to log₁₀(fragment size). Use the ladder to estimate the size of X.', f'about {est:.0f} bp (accept ±10 %)', f'Plot/use distance vs log size (M1); read off log size {math.log10(est):.2f} (M1); ≈ {est:.0f} bp (A1).', 3),
        ('Explain why DNA fragments move through the gel.', 'DNA has negatively charged phosphate groups and is attracted to the positive electrode.', 'Negative charge (A1); move to anode (A1).', 2),
        ('Explain why fragments of different sizes separate.', 'Smaller fragments move more easily through the pores of the gel, so they travel further in a given time.', 'Size/gel resistance (A1).', 1),
        ('Explain why a DNA ladder is run on the same gel.', 'Fragments of known size give a calibration under identical conditions, allowing sizes of unknown fragments to be estimated.', 'Known sizes (A1); same conditions (A1).', 2),
        ('Outline one use of gel electrophoresis in DNA profiling.', 'Comparing STR band patterns from crime-scene samples with suspects, or in paternity testing.', 'Valid use (A1).', 1),
        ('Explain why the DNA was cut with a restriction enzyme before electrophoresis.', 'Restriction enzymes cut at specific base sequences, producing fragments of characteristic sizes that can be separated and compared.', 'Specific recognition sites (A1); fragments of different lengths (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch06-st1', _gel_dq)


S('ch06-st2',
  terms=[('transcription', 'the synthesis of RNA using a DNA strand as a template, catalysed by RNA polymerase'),
         ('translation', 'the synthesis of a polypeptide on a ribosome, with the amino acid sequence determined by the codons of mRNA'),
         ('codon', 'a sequence of three bases on mRNA that codes for an amino acid or a stop signal'),
         ('anticodon', 'a sequence of three bases on a tRNA molecule that pairs with a complementary codon on mRNA'),
         ('template strand', 'the DNA strand that is transcribed; the mRNA is complementary to it'),
         ('degeneracy of the genetic code', 'the fact that most amino acids are coded for by more than one codon'),
         ('universality of the genetic code', 'the fact that the same codons code for the same amino acids in almost all organisms'),
         ('RNA polymerase', 'the enzyme that separates DNA strands and links RNA nucleotides in the 5′ → 3′ direction during transcription')],
  facts=[('Which codon acts as the start codon?', 'AUG', ['UAA', 'UGA', 'GGG'], 'Codes for methionine.'),
         ('How many different codons are there?', '64', ['20', '61', '4'], '4³ = 64.'),
         ('Which base in RNA replaces thymine?', 'uracil', ['adenine', 'cytosine', 'guanine'], 'U pairs with A.'),
         ('Where does translation take place?', 'on ribosomes in the cytoplasm', ['in the nucleolus only', 'in the nucleus on chromosomes', 'in lysosomes'], 'Free or on rough ER.'),
         ('Which are the three stop codons?', 'UAA, UAG and UGA', ['AUG, UAA and UGG', 'UUU, CCC and GGG', 'AAA, AAG and AGA'], 'They code for no amino acid.'),
         ('What type of bond joins amino acids in a polypeptide?', 'peptide bond', ['phosphodiester bond', 'glycosidic bond', 'hydrogen bond'], 'Formed by condensation on the ribosome.')],
  mc2=[('Why does a triplet code provide enough codons for 20 amino acids?', '4³ = 64 combinations are more than enough, whereas a doublet code would give only 16.', ['Each base codes one amino acid.', 'There are 20 bases.', 'A doublet gives 64 codons.'], 'Minimum triplet.'),
       ('Why can human insulin be produced by bacteria carrying the human gene?', 'The genetic code is universal, so bacterial ribosomes translate the codons into the same amino acids.', ['Bacteria have human ribosomes.', 'The code is different in bacteria.', 'Insulin is a lipid.'], 'Universality.'),
       ('Why is degeneracy of the code an advantage?', 'Some base substitutions do not change the amino acid (silent mutations).', ['It produces more proteins.', 'It allows 64 amino acids.', 'It prevents transcription.'], 'Buffer against mutation.'),
       ('Why is mRNA needed as an intermediate rather than translating DNA directly?', 'DNA stays in the nucleus; mRNA carries copies of the gene to ribosomes in the cytoplasm.', ['DNA is too short.', 'Ribosomes are in the nucleus.', 'DNA contains uracil.'], 'Protects DNA, allows amplification.')],
  mc3=[('The template DNA strand reads 3′-TAC GGA CTT-5′. What is the mRNA sequence?', '5′-AUG CCU GAA-3′', ['5′-TAC GGA CTT-3′', '5′-ATG CCT GAA-3′', '5′-UAC GGA CUU-3′'], 'Complementary, with U for T.'),
       ('An mRNA has 330 bases between and including the start and stop codons. How many amino acids are in the polypeptide?', '109', ['110', '330', '990'], '330/3 = 110 codons, minus the stop codon.'),
       ('Which anticodon pairs with the codon 5′-GCA-3′?', '3′-CGU-5′', ['3′-GCA-5′', '3′-CGT-5′', '3′-UGC-5′'], 'Complementary, antiparallel.')],
  why=[('Explain the process of transcription.', 'RNA polymerase binds to the promoter; separates DNA strands; free RNA nucleotides pair with complementary bases on the template strand (A–U, T–A, C–G, G–C); RNA polymerase links them 5′ → 3′; at the terminator transcription stops; mRNA is released and the DNA rewinds.'),
       ('Explain the process of translation.', 'mRNA binds to the small ribosomal subunit; tRNA with anticodon UAC carrying methionine pairs with AUG; large subunit joins; next tRNA enters the A site; peptide bond forms between amino acids; ribosome moves along one codon; empty tRNA leaves; continues until a stop codon; polypeptide released.'),
       ('Explain how the base sequence of a gene determines the amino acid sequence of a polypeptide.', 'The base sequence of the template strand is transcribed into complementary mRNA; each triplet codon specifies one amino acid; tRNAs with complementary anticodons bring specific amino acids; the order of codons determines the order of amino acids.')],
  contrast=[('transcription', 'translation', 'Transcription makes mRNA from a DNA template using RNA polymerase in the nucleus; translation makes a polypeptide from mRNA on ribosomes in the cytoplasm using tRNA.'),
            ('codons', 'anticodons', 'Codons are base triplets on mRNA; anticodons are complementary base triplets on tRNA that pair with codons.')],
  misc=[('Both strands of a gene are transcribed into mRNA.', 'Only the template strand is transcribed; the mRNA has the same sequence as the coding strand (with U for T).'),
        ('Each codon codes for a different amino acid.', 'Many codons code for the same amino acid (degeneracy), and three are stop codons.'),
        ('Ribosomes make amino acids.', 'Amino acids are brought by tRNA; ribosomes link them by peptide bonds.')],
  cases=[('production of human insulin by genetically modified E. coli', 'The human insulin gene is inserted into bacterial plasmids; bacteria produce insulin used by people with diabetes.', 'the universality of the genetic code', 'Bacteria read the human codons in the same way, so the same amino acid sequence is made.'),
         ('the deciphering of the genetic code by Nirenberg and Matthaei (1961)', 'Synthetic poly-U mRNA added to a cell-free system produced polyphenylalanine.', 'codons', 'This showed that UUU codes for phenylalanine and began the decoding of all 64 codons.')],
  evaluate=[('The genetic code is truly universal.', ['the same codons code for the same amino acids in bacteria, plants and animals', 'genes can be transferred between species and expressed'], ['minor variations exist, e.g. in mitochondria and some protists (UGA codes for tryptophan)'], 'The code is almost universal; small exceptions exist but do not undermine the evidence for common ancestry.')],
  extended=[('Explain how the information in DNA is used to synthesise a polypeptide.', 'Gene; RNA polymerase; promoter; template strand; complementary base pairing; mRNA leaves nucleus; ribosome; start codon AUG; tRNA anticodons; amino acids; peptide bonds; A, P, E sites; stop codon; degeneracy; universality.', 8),
            ('Describe the features of the genetic code and explain their significance.', 'Triplet; 64 codons; degenerate; universal; non-overlapping; start and stop codons; significance: mutations may be silent, gene transfer between species possible, evidence of common ancestry.', 6)],
  )


def _template_of(mrna):
    """Template strand written 3′→5′ for a 5′→3′ mRNA."""
    comp = {'A': 'T', 'U': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(comp[b] for b in mrna)


def _triplets(s):
    return ' '.join(s[i:i + 3] for i in range(0, len(s), 3))


@R.add('ch06-st2', 'C3', (1, 5), 'numerical')
def translate_q(rng, slot):
    n = pick(rng, [5, 6, 7])
    m = rand_orf(rng, n)
    aa = translate(m)
    if slot.d <= 2:
        stem = f'Use the genetic code to give the amino acid sequence coded by this mRNA: 5′-{_triplets(m)}-3′'
        return num(stem, '–'.join(a for a in aa if a != 'STOP'), f'Codons read in triplets from AUG: {", ".join(f"{m[i:i+3]} = {aa[i // 3]}" for i in range(0, len(m), 3))} (A2 for all correct; A1 for one error).', 2, type='short')
    t = _template_of(m)
    stem = f'The template strand of a short gene is 3′-{_triplets(t)}-5′. Give the base sequence of the mRNA and use the genetic code to deduce the polypeptide.'
    return num(stem, f'mRNA 5′-{_triplets(m)}-3′; polypeptide ' + '–'.join(a for a in aa if a != 'STOP'),
               f'Complementary mRNA with U for T (A1); correct codons translated (A1); stop codon {m[-3:]} recognised, so {len(aa) - 1} amino acids (A1).', 3, type='short')


@R.add('ch06-st2', 'C3', (1, 4), 'mcq')
def codon_mcq(rng, slot):
    cod = pick(rng, [c for c, a in CODON.items() if a != '*'])
    aa = AA3[CODON[cod]]
    others = list({AA3[a] for a in set(CODON.values()) if a not in ('*', CODON[cod])})
    rng.shuffle(others)
    anticodon = ''.join({'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}[b] for b in cod)
    if rng.random() < 0.5:
        return nmcq(rng, f'Using the genetic code, which amino acid does the mRNA codon {cod} code for?', aa, others[:4], f'{cod} codes for {aa}.')
    return nmcq(rng, f'A tRNA carries an anticodon 3′-{anticodon}-5′. Which amino acid does it carry?', aa, others[:4], f'The anticodon pairs with codon 5′-{cod}-3′, which codes for {aa}.')


@R.add('ch06-st2', 'C3', (1, 4), 'numerical')
def aa_count(rng, slot):
    n = rng.randint(100, 600)
    bases = 3 * n + 3
    stem = f'The coding region of an mRNA, from the start codon to the stop codon inclusive, is {bases} nucleotides long. How many amino acids are in the polypeptide, and how many tRNA molecules bind (assuming one per amino acid)?'
    return num(stem, f'{n} amino acids; {n} tRNAs', f'{bases}/3 = {n + 1} codons (M1); stop codon codes for no amino acid → {n} (A1).', 2)


S('ch06-st3',
  terms=[('intron', 'a non-coding sequence within a eukaryotic gene that is transcribed but removed from pre-mRNA by splicing'),
         ('exon', 'a sequence of a eukaryotic gene that remains in mature mRNA after splicing and is usually translated'),
         ('splicing', 'removal of introns from pre-mRNA and joining of exons, carried out by spliceosomes'),
         ('alternative splicing', 'the joining of different combinations of exons from one pre-mRNA, so that one gene can code for several polypeptides'),
         ('5′ cap', 'a modified guanine nucleotide added to the 5′ end of pre-mRNA that protects it and helps ribosomes bind'),
         ('poly-A tail', 'a chain of adenine nucleotides added to the 3′ end of pre-mRNA that increases its stability'),
         ('initiator tRNA', 'the tRNA carrying methionine with anticodon UAC that binds to the start codon in the P site to begin translation'),
         ('proteasome', 'a large protein complex that breaks down unwanted or damaged proteins tagged with ubiquitin')],
  facts=[('Where in a eukaryotic cell are introns removed?', 'in the nucleus', ['in the cytoplasm', 'on ribosomes', 'in the Golgi apparatus'], 'Before mRNA is exported.'),
         ('Which part of the ribosome first binds to the mRNA?', 'the small subunit', ['the large subunit', 'the A site of the large subunit', 'the E site'], 'Binds near the 5′ cap and scans to AUG.'),
         ('In which ribosomal site does the initiator tRNA bind?', 'the P site', ['the A site', 'the E site', 'the nucleolus'], 'Next tRNA enters the A site.'),
         ('Which hormone is made as a precursor (preproinsulin) and cleaved to its active form?', 'insulin', ['oestradiol', 'adrenaline', 'testosterone'], 'Post-translational modification.'),
         ('Which organisms do not usually have introns in their genes?', 'prokaryotes', ['humans', 'plants', 'fungi'], 'Introns are typical of eukaryotes.')],
  mc2=[('Why can humans have about 20 000 genes but make many more different proteins?', 'Alternative splicing allows one gene to produce several different polypeptides.', ['Each gene codes for exactly one protein.', 'Introns are translated.', 'Ribosomes change the code.'], 'Different exon combinations.'),
       ('Why is a 5′ cap needed for translation in eukaryotes?', 'It protects the mRNA from degradation and is recognised by the small ribosomal subunit.', ['It acts as a stop codon.', 'It is translated into methionine.', 'It removes introns.'], 'Initiation.'),
       ('Why is the first amino acid of most polypeptides methionine?', 'Translation starts at the codon AUG, which codes for methionine.', ['Methionine is the smallest amino acid.', 'Methionine is attached to the 5′ cap.', 'All amino acids are methionine.'], 'Start codon.'),
       ('Why must a polypeptide often be modified after translation?', 'Many proteins are only active after cleavage, folding or addition of groups such as sugars or phosphates.', ['Translation is always incorrect.', 'All proteins are inactive.', 'Modification removes introns.'], 'e.g. insulin.')],
  mc3=[('A gene has exons of 210, 150 and 330 nucleotides and two introns of 800 nucleotides each. How long is the mature mRNA coding region?', '690 nucleotides', ['2290 nucleotides', '1600 nucleotides', '230 nucleotides'], '210 + 150 + 330 = 690.'),
       ('A gene has four exons; exons 2 and 3 can each be included or skipped. How many different mature mRNAs are possible?', '4', ['2', '8', '16'], '2 × 2 = 4.'),
       ('A mutation removes the poly-A signal from a gene. What is the likely effect?', 'The mRNA is less stable and is degraded faster, so less protein is made.', ['The mRNA is translated more.', 'Introns are no longer removed.', 'The start codon changes.'], 'Poly-A tail stabilises mRNA.')],
  why=[('Explain the post-transcriptional modification of eukaryotic pre-mRNA.', 'A 5′ cap (methylated guanine) is added, protecting mRNA and aiding ribosome binding; a poly-A tail is added to the 3′ end, increasing stability; introns are removed by spliceosomes and exons joined; alternative splicing can produce different mRNAs; mature mRNA leaves via nuclear pores.'),
       ('Explain how translation is initiated.', 'The small ribosomal subunit binds to the 5′ cap of mRNA and moves along it to the start codon AUG; the initiator tRNA with anticodon UAC carrying methionine binds; the large subunit joins so that the initiator tRNA is in the P site; the next tRNA enters the A site.'),
       ('Explain how the insulin molecule is produced from preproinsulin.', 'Preproinsulin is translated on the rough ER; the signal sequence is removed in the ER to give proinsulin; proinsulin folds and forms disulfide bonds; in the Golgi/vesicles the C-peptide is cut out, leaving A and B chains joined by disulfide bonds — active insulin.')],
  contrast=[('introns', 'exons', 'Introns are non-coding sequences that are removed during splicing; exons are retained in mature mRNA and are translated.'),
            ('pre-mRNA', 'mature mRNA', 'Pre-mRNA is the primary transcript containing introns; mature mRNA has had introns removed and a 5′ cap and poly-A tail added.')],
  misc=[('Introns are translated into protein.', 'Introns are removed from pre-mRNA before it leaves the nucleus and are not translated.'),
        ('One gene always codes for exactly one polypeptide.', 'Alternative splicing allows one gene to code for several polypeptides.'),
        ('Proteins are fully functional as soon as translation ends.', 'Many need post-translational modification such as cleavage, folding, glycosylation or phosphorylation.')],
  cases=[('alternative splicing of the Dscam gene in Drosophila', 'One gene can potentially produce over 38 000 different mRNAs through alternative splicing.', 'alternative splicing', 'Different combinations of exons give a huge diversity of proteins from a single gene, used in neurone recognition.'),
         ('the production of insulin from proinsulin', 'Proinsulin is cleaved to remove the C-peptide; C-peptide levels are used to measure insulin production in diabetics.', 'post-translational modification', 'Cleavage of the precursor is needed to form active insulin.')],
  evaluate=[('Introns are “junk DNA” with no function.', ['introns are removed and not translated', 'they increase the energy cost of transcription'], ['introns allow alternative splicing, increasing protein diversity', 'some contain regulatory sequences or code for small RNAs'], 'Introns are not junk: they enable alternative splicing and regulation, although many intron sequences have no known specific function.')],
  extended=[('Explain the modifications made to RNA and polypeptides after transcription and translation in eukaryotes.', '5′ cap; poly-A tail; splicing by spliceosomes; alternative splicing; export from nucleus; initiation of translation; post-translational modification: cleavage (insulin), folding, disulfide bonds, glycosylation in Golgi; proteasome degradation.', 8),
            ('Describe how translation is initiated and explain how the polypeptide is elongated and terminated.', 'Small subunit binds cap; scanning; AUG; initiator tRNA-Met in P site; large subunit; elongation: tRNA in A site, peptide bond, translocation, E site; termination: stop codon, release factor; polysomes.', 6)],
  )


@R.add('ch06-st3', 'C3', (1, 5), 'numerical')
def exon_calc(rng, slot):
    k = pick(rng, [3, 4, 5])
    ex = [3 * rng.randint(30, 120) for _ in range(k)]
    intr = [rng.randint(150, 2500) for _ in range(k - 1)]
    pre = sum(ex) + sum(intr)
    mature = sum(ex)
    stem = f'A eukaryotic gene contains {k} exons of lengths {", ".join(map(str, ex))} nucleotides and introns of {", ".join(map(str, intr))} nucleotides. Calculate the length of the pre-mRNA and of the spliced (coding) mRNA, and the percentage of the pre-mRNA removed.'
    pr = 100 * sum(intr) / pre
    if slot.d >= 4:
        opt = pick(rng, [1, 2])
        stem += f' If {opt} of the internal exons can be skipped independently, how many different mature mRNAs are possible?'
        return num(stem, f'pre-mRNA {pre}; mature {mature}; {pr:.0f} % removed; {2 ** opt} variants',
                   f'Sum of exons and introns = {pre} (A1); exons only = {mature} (A1); {sum(intr)}/{pre} × 100 = {pr:.0f} % (A1); 2^{opt} = {2 ** opt} (A1).', 4)
    return num(stem, f'pre-mRNA {pre} nucleotides; mature {mature} nucleotides; {pr:.0f} % removed',
               f'Sum of exons and introns = {pre} (A1); exons only = {mature} (A1); {sum(intr)}/{pre} × 100 = {pr:.0f} % (A1).', 3)


def _splice_dq(rng, slot):
    ex = [3 * rng.randint(40, 90) for _ in range(5)]
    intr = [rng.randint(300, 1500) for _ in range(4)]
    tissues = [('liver', [1, 2, 3, 4, 5]), ('muscle', [1, 2, 4, 5]), ('brain', [1, 3, 5])]
    rows = []
    for t, inc in tissues:
        L = sum(ex[i - 1] for i in inc)
        rows.append((t, ', '.join(map(str, inc)), L))
    intro = ('A eukaryotic gene has five exons and four introns. The lengths are: exons 1–5: ' + ', '.join(map(str, ex)) + ' nucleotides; introns: ' + ', '.join(map(str, intr)) +
             ' nucleotides. The exons present in the mature mRNA in three tissues are shown.\n\n' + table(['Tissue', 'Exons present', 'Mature mRNA coding length / nucleotides'], [(a, b, '?' if a == 'muscle' else c) for a, b, c in rows]))
    mus = rows[1][2]
    pre = sum(ex) + sum(intr)
    parts = [
        ('State which exons are present in brain mRNA.', 'exons 1, 3 and 5', 'Correct exons (A1).', 1),
        ('Calculate the coding length of the muscle mRNA.', f'{mus} nucleotides', f'{ex[0]} + {ex[1]} + {ex[3]} + {ex[4]} = {mus} (A1).', 1),
        ('Calculate the length of the primary transcript (pre-mRNA), excluding cap and tail.', f'{pre} nucleotides', f'Sum of all exons and introns = {pre} (A1).', 1),
        ('Calculate the maximum number of amino acids coded by the liver mRNA, assuming the stop codon is the last codon of exon 5.', f'{rows[0][2] // 3 - 1}', f'{rows[0][2]}/3 = {rows[0][2] // 3} codons (M1); minus stop = {rows[0][2] // 3 - 1} (A1).', 2),
        ('Explain how these data show alternative splicing.', 'The same gene/pre-mRNA gives different mature mRNAs in different tissues because different combinations of exons are joined.', 'Same gene (A1); different exon combinations (A1).', 2),
        ('Outline two other modifications made to pre-mRNA before it leaves the nucleus.', 'Addition of a 5′ cap; addition of a poly-A tail.', 'Cap (A1); tail (A1).', 2),
        ('Suggest an advantage of alternative splicing to an organism.', 'More different proteins from fewer genes; tissue-specific protein variants.', 'Valid advantage (A1).', 1),
        ('Explain why the polypeptides produced in the three tissues share some amino acid sequences but differ in others.', 'Exons present in all mRNAs code for the same amino acid sequences; exons omitted in some tissues remove those sections, so the proteins differ.', 'Shared exons (A1); omitted exons change sequence (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch06-st3', _splice_dq)


S('ch06-st4',
  terms=[('gene mutation', 'a change in the base sequence of a gene'),
         ('base substitution', 'a mutation in which one base is replaced by another'),
         ('frameshift mutation', 'an insertion or deletion of a number of bases that is not a multiple of three, changing every codon after the mutation'),
         ('nonsense mutation', 'a substitution that changes a codon for an amino acid into a stop codon, shortening the polypeptide'),
         ('mutagen', 'an agent that increases the rate of mutation, such as UV radiation, X-rays or certain chemicals'),
         ('gene knockout', 'a technique in which a gene is made inoperative so that its function can be investigated from the effects of its absence'),
         ('CRISPR–Cas9', 'a gene-editing system in which a guide RNA directs the Cas9 nuclease to cut DNA at a specific sequence'),
         ('conserved sequence', 'a base or amino acid sequence that is identical or very similar across many species, suggesting it is functionally important')],
  facts=[('Which base substitution causes sickle-cell anaemia?', 'A → T in the sixth codon of the β-globin gene, changing GAG to GTG', ['C → G in the first codon', 'deletion of three bases', 'insertion of one base'], 'Glu replaced by Val.'),
         ('Which amino acid replaces glutamic acid in sickle-cell haemoglobin?', 'valine', ['lysine', 'glycine', 'methionine'], 'GAG → GUG.'),
         ('Which is a mutagen?', 'ultraviolet radiation', ['visible red light', 'glucose', 'water'], 'Causes thymine dimers.'),
         ('Which enzyme cuts DNA in the CRISPR system?', 'Cas9', ['DNA ligase', 'helicase', 'reverse transcriptase'], 'Guided by RNA.'),
         ('Which cells must a mutation occur in to be inherited by offspring?', 'germ-line cells (cells that produce gametes)', ['skin cells', 'liver cells', 'any somatic cells'], 'Gametes carry it.')],
  mc2=[('Why is an insertion of one base usually more harmful than a base substitution?', 'It causes a frameshift, changing all codons after the insertion.', ['It changes only one amino acid.', 'It never changes the protein.', 'It removes the start codon.'], 'Reading frame shifts.'),
       ('Why do many base substitutions have no effect on the protein?', 'The genetic code is degenerate, so the new codon may code for the same amino acid.', ['Substitutions occur only in introns.', 'Ribosomes correct them.', 'Mutations always affect stop codons.'], 'Silent mutations.'),
       ('Why can a mutation in a somatic cell cause cancer but not be inherited?', 'It is passed to daughter cells by mitosis but not to gametes.', ['Somatic cells form gametes.', 'Cancer is always inherited.', 'Mitosis removes mutations.'], 'Somatic vs germ-line.'),
       ('Why is the guide RNA essential in CRISPR–Cas9?', 'Its base sequence is complementary to the target DNA, directing Cas9 to cut there.', ['It joins DNA fragments.', 'It codes for Cas9.', 'It translates the gene.'], 'Specificity.')],
  mc3=[('A codon UGG (Trp) mutates to UGA. What type of mutation is this?', 'nonsense – it creates a stop codon', ['silent', 'missense', 'frameshift'], 'UGA is a stop codon.'),
       ('A codon CUU (Leu) mutates to CUC. What is the effect?', 'none – CUC also codes for leucine (silent)', ['leucine is replaced by proline', 'translation stops', 'a frameshift occurs'], 'Degeneracy.'),
       ('Deletion of three consecutive bases within a gene usually causes:', 'loss of one amino acid without a frameshift', ['a frameshift of all later codons', 'no change ever', 'duplication of the gene'], 'A whole codon removed, e.g. ΔF508 in cystic fibrosis.')],
  why=[('Explain how a base substitution leads to sickle-cell anaemia.', 'Substitution A → T in the β-globin gene changes codon GAG to GTG (mRNA GAG → GUG); glutamic acid is replaced by valine at position 6; haemoglobin S polymerises at low oxygen; red blood cells become sickle-shaped, block capillaries and carry less oxygen.'),
       ('Explain the consequences of insertions and deletions in a gene.', 'Insertion or deletion of a number of bases not a multiple of three shifts the reading frame; all downstream codons change; often a premature stop codon arises; the polypeptide is non-functional; deletion of three bases removes one amino acid (e.g. cystic fibrosis ΔF508).'),
       ('Explain how CRISPR–Cas9 can be used to edit genes.', 'A guide RNA complementary to the target sequence is made; it binds Cas9 and guides it to the target in the genome; Cas9 cuts both strands; the cell repairs the cut, often introducing errors (knockout), or a supplied template is inserted by homology-directed repair, editing the gene.')],
  contrast=[('missense mutations', 'nonsense mutations', 'Missense mutations change a codon so that a different amino acid is incorporated; nonsense mutations change a codon into a stop codon, ending translation early.'),
            ('germ-line mutations', 'somatic mutations', 'Germ-line mutations occur in cells that produce gametes and can be inherited; somatic mutations occur in body cells, are passed only to daughter cells and may cause cancer but are not inherited.')],
  misc=[('All mutations are harmful.', 'Most are neutral; some are harmful and a few are beneficial, providing variation for evolution.'),
        ('Mutations happen because an organism needs to adapt.', 'Mutations are random changes; selection then acts on them.'),
        ('A base substitution always changes the amino acid.', 'Because of degeneracy, many substitutions are silent.'),
        ('Gene knockout means removing a gene from all individuals of a species.', 'It is a laboratory technique to inactivate a gene in a model organism to study its function.')],
  cases=[('sickle-cell anaemia', 'A single base substitution in the β-globin gene changes Glu to Val and causes sickling of red blood cells.', 'the effects of a base substitution', 'One amino acid change alters haemoglobin properties and causes disease, while heterozygotes are more resistant to malaria.'),
         ('knockout mice', 'Mice in which a specific gene has been inactivated are used to study gene function and model human diseases.', 'gene knockout', 'The phenotype that results from the missing gene reveals its normal role.'),
         ('CRISPR treatment of sickle-cell disease (Casgevy, 2023)', 'Patients’ stem cells are edited to switch on fetal haemoglobin production and returned to the body.', 'CRISPR–Cas9 gene editing', 'Precise editing of a regulatory gene restores oxygen transport and relieves symptoms.')],
  evaluate=[('Gene editing of human embryos should be permitted to prevent genetic disease.', ['could eliminate serious inherited diseases such as Huntington’s', 'CRISPR is precise and increasingly reliable'], ['off-target edits and mosaicism may cause harm to future generations', 'ethical concerns about consent, designer babies and inequality'], 'Somatic gene therapy is justified, but germ-line editing should remain restricted until safety and ethical issues are resolved.')],
  extended=[('Explain the different types of gene mutation and their consequences, using named examples.', 'Substitution: silent, missense (sickle-cell GAG→GTG, Glu→Val), nonsense; insertion/deletion: frameshift, premature stop; three-base deletion (CF ΔF508); causes: mutagens (UV, X-rays, chemicals), replication errors; germ-line vs somatic; cancer; source of variation.', 8),
            ('Explain how gene knockout and CRISPR–Cas9 are used to study and change gene function.', 'Knockout organisms; observing phenotype; CRISPR: guide RNA, Cas9, double-strand break, repair by NHEJ (knockout) or HDR (insertion); applications: research, crops, sickle-cell treatment; risks: off-target effects; conserved sequences.', 6)],
  )


@R.add('ch06-st4', 'C3', (1, 5), 'mcq')
def mutation_type_mcq(rng, slot):
    for _ in range(20):
        cod = pick(rng, [c for c, a in CODON.items() if a != '*'])
        pos = rng.randrange(3)
        nb = pick(rng, [b for b in 'UCAG' if b != cod[pos]])
        new = cod[:pos] + nb + cod[pos + 1:]
        a1, a2 = CODON[cod], CODON[new]
        kind = 'silent' if a1 == a2 else ('nonsense' if a2 == '*' else 'missense')
        if kind == 'silent' or rng.random() < 0.6:
            break
    lab = {'silent': 'silent (same amino acid)', 'missense': f'missense ({AA3[a1]} → {AA3[a2] if a2 != "*" else "STOP"})', 'nonsense': 'nonsense (stop codon)'}
    opts = {'silent': 'silent (same amino acid)', 'missense': 'missense (different amino acid)', 'nonsense': 'nonsense (stop codon)', 'fs': 'frameshift'}
    corr = opts[kind]
    stem = f'In an mRNA, the codon {cod} ({AA3[a1]}) mutates to {new}. Using the genetic code, classify this mutation.'
    return nmcq(rng, stem, corr, [v for k, v in opts.items() if k != kind], f'{new} codes for {AA3[a2]}, so the mutation is {lab[kind]}.')


@R.add('ch06-st4', 'C3', (2, 5), 'numerical')
def frameshift_q(rng, slot):
    m = rand_orf(rng, 7)
    i = 3 * rng.randint(1, 3) + rng.randrange(3)
    ins = rng.random() < 0.5
    if ins:
        b = pick(rng, 'ACGU')
        m2 = m[:i] + b + m[i:]
        desc = f'insertion of {b} after base {i}'
    else:
        m2 = m[:i] + m[i + 1:]
        desc = f'deletion of base {i + 1} ({m[i]})'
    a1 = translate(m)
    a2 = translate(m2[:len(m2) - len(m2) % 3])
    stem = (f'The mRNA 5′-{_triplets(m)}-3′ undergoes a mutation: {desc}. Use the genetic code to give the original and the mutant amino acid sequences and explain the effect.')
    return num(stem, f'original {"–".join(a1)}; mutant {"–".join(a2)}; frameshift alters all codons after the mutation',
               f'Original translated (A1); mutant codons re-read in new frame (A1); frameshift explanation – all downstream codons change, may introduce early stop or remove stop (R1).', 3, type='short')


def _mutagen_dq(rng, slot):
    dose = [0, 10, 20, 40, 80]
    k = rng.uniform(1.5, 3.0)
    base = rng.uniform(2, 5)
    surv = [round(100 * math.exp(-0.025 * d * rng.uniform(0.9, 1.1)), 0) for d in dose]
    surv[0] = 100
    mut = [round(base + k * d, 0) for d in dose]
    intro = ('Yeast cells were exposed to different doses of ultraviolet (UV) radiation. The percentage surviving and the number of mutant colonies per 10⁶ surviving cells were recorded.\n\n'
             + table(['UV dose / J m⁻²', 'Survival / %', 'Mutants per 10⁶ survivors'], [(d, f'{s:.0f}', f'{m:.0f}') for d, s, m in zip(dose, surv, mut)]))
    f = mut[3] / mut[0]
    parts = [
        ('State the number of mutants per 10⁶ survivors at 20 J m⁻².', f'{mut[2]:.0f}', f'{mut[2]:.0f} (A1).', 1),
        ('Calculate how many times greater the mutation frequency is at 40 J m⁻² than with no UV.', f'{f:.1f} times', f'{mut[3]:.0f}/{mut[0]:.0f} = {f:.1f} (A1).', 1),
        ('Describe the relationship between UV dose and mutation frequency.', 'Mutation frequency increases with dose, approximately linearly.', 'Positive (A1); linear/proportional (A1).', 2),
        ('Explain why mutants occur even with no UV.', 'Spontaneous mutations arise from errors in DNA replication or natural background radiation/chemicals.', 'Spontaneous/replication errors (A1).', 1),
        ('Explain how UV causes mutations.', 'UV is absorbed by DNA bases, forming thymine dimers between adjacent pyrimidines; errors during repair or replication cause base changes.', 'Absorbed by bases/thymine dimers (A1); replication/repair errors (A1).', 2),
        ('Explain why survival decreases at high doses.', 'More DNA damage, including in essential genes; cells cannot repair it, so they die or cannot divide.', 'Damage to essential genes (A1); cell death (A1).', 2),
        ('Suggest why human skin cancer risk increases with sun exposure.', 'UV causes mutations in skin cells, including in genes controlling cell division (oncogenes/tumour suppressors), leading to uncontrolled division.', 'Mutation in cell-cycle genes (A1).', 1),
        ('Explain why mutation frequency is expressed per 10⁶ surviving cells.', 'Many cells are killed at higher doses, so expressing mutants per survivor allows a fair comparison of mutation rate between doses.', 'Survival differs between doses (A1); fair comparison (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch06-st4', _mutagen_dq)


# =============================================================================================
# ch07 D2.1–D2.3 Cell division, gene expression and water potential
# =============================================================================================
S('ch07-st1',
  terms=[('mitosis', 'nuclear division that produces two genetically identical nuclei with the same chromosome number as the parent nucleus'),
         ('meiosis', 'a reduction division of a diploid nucleus into four haploid nuclei, each genetically different'),
         ('cytokinesis', 'division of the cytoplasm to form two daughter cells after nuclear division'),
         ('mitotic index', 'the ratio of the number of cells in mitosis to the total number of cells observed'),
         ('crossing over', 'exchange of sections of chromatids between homologous chromosomes during prophase I of meiosis'),
         ('non-disjunction', 'failure of homologous chromosomes or sister chromatids to separate during meiosis, producing gametes with an abnormal chromosome number'),
         ('homologous chromosomes', 'a pair of chromosomes, one maternal and one paternal, with the same genes at the same loci'),
         ('independent assortment', 'the random orientation of pairs of homologous chromosomes at metaphase I, so that each gamete receives a random mix of maternal and paternal chromosomes')],
  facts=[('In which phase of mitosis do sister chromatids separate?', 'anaphase', ['prophase', 'metaphase', 'telophase'], 'Spindle fibres shorten.'),
         ('How many chromosomes are in a human gamete?', '23', ['46', '92', '22'], 'Haploid.'),
         ('Which condition is caused by non-disjunction of chromosome 21?', 'Down syndrome', ['Turner syndrome', 'haemophilia', 'cystic fibrosis'], 'Trisomy 21.'),
         ('In which phase does crossing over occur?', 'prophase I', ['metaphase II', 'anaphase I', 'telophase II'], 'Bivalents form.'),
         ('How does cytokinesis differ in plant cells?', 'a cell plate forms from vesicles in the middle of the cell', ['a cleavage furrow forms', 'the cell wall dissolves', 'no division occurs'], 'Plant cells have walls.'),
         ('Which tissue is commonly used to observe mitosis in plants?', 'root tip (meristem)', ['leaf epidermis', 'xylem', 'pollen grains'], 'Rapidly dividing cells.')],
  mc2=[('Why must DNA be replicated before mitosis?', 'So that each daughter cell receives a complete copy of the genome.', ['To halve the chromosome number.', 'To cause crossing over.', 'To make cells haploid.'], 'Two sister chromatids.'),
       ('Why does meiosis produce genetically different gametes?', 'Crossing over and random orientation of homologous pairs create new combinations of alleles.', ['DNA is mutated in every meiosis.', 'Sister chromatids are identical.', 'Mitosis follows meiosis.'], 'Sources of variation.'),
       ('Why is the risk of Down syndrome higher in older mothers?', 'Oocytes are arrested in meiosis I for many years, increasing the chance of non-disjunction.', ['Older mothers have more chromosomes.', 'Sperm are affected only.', 'Mitosis fails in the embryo.'], 'Maternal age effect.'),
       ('Why is meiosis needed in sexual life cycles?', 'It halves the chromosome number so fertilisation restores the diploid number.', ['It doubles the chromosome number.', 'It produces identical cells.', 'It repairs DNA.'], 'Constant chromosome number.')],
  mc3=[('An onion root tip slide shows 24 cells in mitosis out of 300 cells. What is the mitotic index?', '0.08', ['0.8', '12.5', '0.24'], '24/300 = 0.08.'),
       ('A species has a diploid number of 8. How many combinations of chromosomes are possible in gametes from independent assortment alone?', '16', ['8', '4', '256'], '2ⁿ where n = 4 pairs.'),
       ('A gamete with 24 chromosomes fertilises a normal human gamete. What is the zygote’s chromosome number?', '47', ['46', '48', '23'], 'Trisomy.')],
  why=[('Explain the events of mitosis.', 'Prophase: chromosomes condense, nuclear membrane breaks down, spindle forms; metaphase: chromosomes line up at the equator, attached to spindle by centromeres; anaphase: centromeres divide and sister chromatids are pulled to opposite poles; telophase: nuclear membranes reform, chromosomes decondense; followed by cytokinesis.'),
       ('Explain how meiosis generates genetic variation.', 'Crossing over between non-sister chromatids of homologous chromosomes in prophase I creates new allele combinations; random orientation of bivalents at metaphase I gives 2ⁿ combinations; random orientation of chromatids in metaphase II; random fertilisation adds further variation.'),
       ('Explain how non-disjunction can lead to Down syndrome.', 'Homologous chromosomes 21 fail to separate in anaphase I (or chromatids in anaphase II); one gamete receives two copies of chromosome 21; fertilisation by a normal gamete gives a zygote with three copies (trisomy 21, 47 chromosomes).')],
  contrast=[('mitosis', 'meiosis', 'Mitosis has one division and produces two genetically identical diploid cells for growth and repair; meiosis has two divisions, involves crossing over and independent assortment, and produces four genetically different haploid cells.'),
            ('anaphase I', 'anaphase II', 'In anaphase I homologous chromosomes separate to opposite poles; in anaphase II sister chromatids separate.')],
  misc=[('Chromosomes are replicated during prophase.', 'DNA is replicated in S phase of interphase, before mitosis begins.'),
        ('Meiosis produces two identical cells.', 'Meiosis produces four genetically different haploid cells.'),
        ('Interphase is a resting phase.', 'Interphase is a metabolically active phase including growth, DNA replication and protein synthesis.'),
        ('Only older mothers have children with Down syndrome.', 'Risk increases with maternal age, but most babies with Down syndrome are born to younger mothers because they have more babies overall.')],
  cases=[('Down syndrome (trisomy 21)', 'People with Down syndrome have 47 chromosomes, with three copies of chromosome 21.', 'non-disjunction', 'Failure of chromosome 21 to separate in meiosis produced a gamete with an extra chromosome.'),
         ('onion root tip squashes in school laboratories', 'Root tips are stained and squashed to observe chromosomes in different stages of mitosis.', 'the mitotic index', 'Counting cells in each phase shows the proportion of time spent in mitosis and the rate of cell division.')],
  evaluate=[('Sexual reproduction is more advantageous than asexual reproduction.', ['meiosis and fertilisation create variation, aiding adaptation to changing environments and resistance to parasites'], ['asexual reproduction is faster, needs no mate, and preserves successful genotypes', 'meiosis breaks up favourable gene combinations; only half of individuals bear young'], 'Sexual reproduction is advantageous in changing environments, while asexual reproduction is better for rapid colonisation of stable ones.')],
  extended=[('Compare mitosis and meiosis and explain how meiosis produces genetic variation.', 'Interphase; phases of mitosis; meiosis I (bivalents, crossing over, homologues separate) and II (chromatids separate); outcome: 2 diploid identical vs 4 haploid different; random orientation 2ⁿ; crossing over; random fertilisation; non-disjunction.', 8),
            ('Explain how the mitotic index is determined and what it shows about cell division.', 'Root tip, stain (toluidine blue/acetic orcein), squash; count cells in mitosis and total; MI = mitotic cells/total; high MI in meristems and tumours; time in phase = fraction × cycle length; sampling and identification errors.', 6)],
  )


@R.add('ch07-st1', 'C3', (1, 5), 'numerical')
def mitotic_index(rng, slot):
    tot = rng.randint(150, 600)
    ph = [rng.randint(5, 30), rng.randint(2, 12), rng.randint(1, 8), rng.randint(2, 10)]
    mit = sum(ph)
    mi = mit / tot
    stem = (f'In a root-tip squash, {tot} cells were counted: {ph[0]} in prophase, {ph[1]} in metaphase, {ph[2]} in anaphase, {ph[3]} in telophase and the rest in interphase. Calculate the mitotic index.')
    if slot.d >= 4:
        cyc = pick(rng, [16, 20, 22, 24])
        t = ph[1] / tot * cyc * 60
        stem += f' The cell cycle lasts {cyc} hours. Estimate the time spent in metaphase in minutes.'
        return num(stem, f'MI = {mi:.3f}; metaphase ≈ {t:.0f} min', f'MI = {mit}/{tot} (M1) = {mi:.3f} (A1); {ph[1]}/{tot} × {cyc} × 60 (M1) = {t:.0f} min (A1).', 4)
    return num(stem, f'{mi:.3f}', f'Cells in mitosis = {mit} (M1); MI = {mit}/{tot} = {mi:.3f} (A1).', 2)


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def assortment_mcq(rng, slot):
    n2 = pick(rng, [4, 6, 8, 10, 12, 14, 16, 20])
    n = n2 // 2
    return nmcq(rng, f'An organism has a diploid number (2n) of {n2}. Ignoring crossing over, how many genetically different gametes can it produce by random orientation of homologous pairs?',
                f'{2 ** n}', [f'{2 ** n2}', f'{n2}', f'{n ** 2}', f'{2 * n}'], f'n = {n} pairs; 2ⁿ = 2^{n} = {2 ** n}.')


def _mi_dq(rng, slot):
    dists = [0.5, 1.0, 2.0, 3.0, 5.0]
    mi = [rng.uniform(0.14, 0.2)]
    for _ in dists[1:]:
        mi.append(mi[-1] * rng.uniform(0.45, 0.8))
    tot = [rng.randint(180, 260) for _ in dists]
    mit = [max(1, round(m * t)) for m, t in zip(mi, tot)]
    mis = [m / t for m, t in zip(mit, tot)]
    j = 2
    intro = ('Squashes were made of sections of a garlic root taken at different distances from the root tip. The number of cells in mitosis and the total number of cells in a field of view were counted.\n\n'
             + table(['Distance from tip / mm', 'Cells in mitosis', 'Total cells', 'Mitotic index'], [(d, a, b, '?' if i == j else f'{m:.3f}') for i, (d, a, b, m) in enumerate(zip(dists, mit, tot, mis))]))
    p = pct_change(mis[0], mis[-1])
    parts = [
        (f'Calculate the mitotic index at {dists[j]} mm.', f'{mis[j]:.3f}', f'{mit[j]}/{tot[j]} = {mis[j]:.3f} (A1).', 1),
        ('Calculate the percentage change in mitotic index between 0.5 mm and 5.0 mm.', f'{signed(p)} %', f'({mis[-1]:.3f} − {mis[0]:.3f})/{mis[0]:.3f} × 100 (M1) = {signed(p)} % (A1).', 2),
        ('Describe the trend in mitotic index.', 'Mitotic index decreases with distance from the root tip.', 'Decrease with distance (A1); highest near tip (A1).', 2),
        ('Explain the trend.', 'The meristem just behind the tip contains actively dividing cells; further back cells elongate and differentiate and stop dividing.', 'Meristem near tip (A1); differentiation further back (A1).', 2),
        ('Explain why the root tip was treated with hydrochloric acid before staining.', 'Acid breaks down the middle lamella/pectin so cells separate and can be squashed into a single layer.', 'Separates cells (A1).', 1),
        ('Suggest two ways to improve the reliability of the mitotic index values.', 'Count more cells/fields of view; use several roots; repeat counts by different observers; use a clear rule for counting cells at the edge.', 'Two valid (A1 A1).', 2),
        ('Suggest why a tumour biopsy may have a high mitotic index.', 'Tumour cells divide uncontrollably, so a higher proportion are in mitosis.', 'Uncontrolled division (A1).', 1),
        ('Explain why the root tips were stained before observation.', 'Chromosomes are colourless; a stain such as toluidine blue binds DNA so chromosomes are visible and the stage of mitosis can be identified.', 'Make chromosomes visible (A1); identify the phase (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch07-st1', _mi_dq)


S('ch07-st2',
  terms=[('cell cycle', 'the sequence of events between one cell division and the next: G1, S, G2 (interphase) and mitosis with cytokinesis'),
         ('cyclin', 'a protein whose concentration rises and falls during the cell cycle and which activates cyclin-dependent kinases'),
         ('cyclin-dependent kinase (CDK)', 'an enzyme that, when bound to cyclin, phosphorylates target proteins to move the cell into the next phase of the cycle'),
         ('checkpoint', 'a control point in the cell cycle where conditions are checked before the cycle continues, e.g. G1/S, G2/M and the spindle checkpoint'),
         ('oncogene', 'a mutated gene that promotes uncontrolled cell division; derived from a normal proto-oncogene'),
         ('tumour suppressor gene', 'a gene, such as p53, whose protein product inhibits the cell cycle or triggers apoptosis; loss of function can lead to cancer'),
         ('metastasis', 'the spread of cancer cells from a primary tumour to other parts of the body, forming secondary tumours'),
         ('apoptosis', 'programmed cell death')],
  facts=[('Which tumour suppressor protein is called “the guardian of the genome”?', 'p53', ['insulin', 'cyclin D', 'Cas9'], 'Stops the cycle when DNA is damaged.'),
         ('In which phase of the cell cycle is DNA replicated?', 'S phase', ['G1', 'G2', 'M phase'], 'Synthesis phase.'),
         ('What do cyclins bind to and activate?', 'cyclin-dependent kinases', ['RNA polymerase', 'DNA ligase', 'ribosomes'], 'Cyclin–CDK complexes.'),
         ('What is a primary tumour?', 'the original tumour at the site where uncontrolled division began', ['a tumour formed by metastasis', 'a benign skin mole only', 'a tumour in the blood'], 'Secondary tumours form elsewhere.'),
         ('Which is a mutagen known to cause lung cancer?', 'chemicals in tobacco smoke', ['vitamin C', 'oxygen', 'glucose'], 'Carcinogens.')],
  mc2=[('Why can mutations in both oncogenes and tumour suppressor genes lead to cancer?', 'Oncogenes stimulate division, while loss of tumour suppressors removes the brakes on division.', ['Both genes code for cyclins only.', 'They make cells divide more slowly.', 'They only affect gametes.'], 'Accelerator and brake.'),
       ('Why do cyclin concentrations need to fall after each phase?', 'So that CDKs are inactivated and the cell cycle cannot proceed until new cyclins are made.', ['Cyclins block DNA replication.', 'Cyclins are toxic.', 'CDKs are always active.'], 'Cyclical control.'),
       ('Why are several mutations usually needed before a cell becomes cancerous?', 'Multiple control mechanisms (oncogenes, tumour suppressors, apoptosis) must fail.', ['One mutation is always enough.', 'Cancer is caused by viruses only.', 'Mutations cancel out.'], 'Multi-step process.'),
       ('Why is the G1/S checkpoint important?', 'It checks DNA damage and cell size before DNA replication, preventing damaged DNA from being copied.', ['It checks spindle attachment.', 'It starts cytokinesis.', 'It separates chromatids.'], 'Prevents propagation of damage.')],
  mc3=[('A cell cycle lasts 20 hours. 45 % of cells in a sample are in G1. Estimate the length of G1.', '9 hours', ['4.5 hours', '45 hours', '11 hours'], '0.45 × 20 = 9 h.'),
       ('A mutation makes p53 non-functional. What is the most likely consequence?', 'Cells with damaged DNA continue to divide instead of arresting or undergoing apoptosis.', ['Cells cannot replicate DNA.', 'Cells stop dividing.', 'Mitosis becomes faster but accurate.'], 'Loss of tumour suppressor.'),
       ('Which observation would indicate a malignant rather than benign tumour?', 'cells invading surrounding tissues and spreading to lymph nodes', ['a slow-growing encapsulated mass', 'cells resembling normal tissue', 'a tumour that does not spread'], 'Metastasis.')],
  why=[('Explain how cyclins control the cell cycle.', 'Different cyclins accumulate at different stages; they bind and activate CDKs; active cyclin–CDK complexes phosphorylate target proteins, triggering events such as DNA replication or mitosis; cyclins are then degraded, so CDKs become inactive; this ensures events occur in the right order.'),
       ('Explain how mutations can lead to the formation of tumours.', 'Mutagens or replication errors cause mutations in proto-oncogenes (becoming oncogenes that stimulate division) and tumour suppressor genes (e.g. p53, losing ability to stop the cycle or trigger apoptosis); cells divide uncontrollably, forming a tumour; further mutations allow invasion and metastasis.'),
       ('Explain the difference between benign and malignant tumours.', 'Benign tumours grow slowly, are usually encapsulated and do not spread; malignant tumours grow rapidly, invade surrounding tissues and metastasise via blood or lymph to form secondary tumours.')],
  contrast=[('proto-oncogenes', 'oncogenes', 'Proto-oncogenes are normal genes that stimulate cell division when needed; oncogenes are mutated forms that are permanently active, stimulating uncontrolled division.'),
            ('benign tumours', 'malignant tumours', 'Benign tumours remain localised and do not invade; malignant tumours invade tissues and spread by metastasis.')],
  misc=[('Cancer is caused by a single mutation.', 'Usually several mutations in different genes are needed.'),
        ('All tumours are cancerous.', 'Benign tumours do not invade or spread and are not cancers.'),
        ('Cyclins are enzymes that phosphorylate proteins.', 'Cyclins are regulatory proteins that activate CDKs; the CDKs are the kinases.')],
  cases=[('Hunt, Hartwell and Nurse’s discovery of cyclins and CDKs', 'They showed that cyclin concentrations in sea urchin eggs rose and fell with each division and identified CDK genes in yeast (Nobel Prize 2001).', 'cell cycle control', 'Cyclical synthesis and destruction of cyclins regulates CDK activity and the progression of the cycle.'),
         ('lung cancer and smoking', 'Smokers have a much greater risk of lung cancer; tobacco smoke contains many carcinogens.', 'mutagens and cancer', 'Carcinogens cause mutations in oncogenes and tumour suppressor genes in lung cells.'),
         ('HeLa cells', 'Cervical cancer cells taken from Henrietta Lacks in 1951 continue to divide in culture today.', 'loss of cell-cycle control', 'Mutations and HPV proteins disable tumour suppressors, so the cells divide indefinitely.')],
  evaluate=[('Cancer is mainly a disease caused by lifestyle.', ['smoking, UV exposure, diet and alcohol increase mutation rates and cancer risk'], ['inherited mutations (BRCA1) and random replication errors cause many cancers', 'ageing increases risk regardless of lifestyle'], 'Lifestyle factors cause a large proportion of cancers, but genetics and chance also play major roles.')],
  extended=[('Explain how the cell cycle is controlled and how loss of control leads to cancer.', 'Phases G1, S, G2, M; checkpoints; cyclins and CDKs; phosphorylation; degradation of cyclins; p53 and DNA damage; apoptosis; proto-oncogenes and oncogenes; tumour suppressors; mutagens; primary and secondary tumours; metastasis.', 8),
            ('Outline the phases of the cell cycle and explain how the duration of each phase can be estimated from observations of cells.', 'G1 growth, S DNA replication, G2 preparation, mitosis, cytokinesis; count cells in each phase; fraction × total cycle length; assumptions (asynchronous population); sources of error.', 6)],
  )


@R.add('ch07-st2', 'C3', (2, 5), 'numerical')
def phase_time(rng, slot):
    cyc = pick(rng, [12, 18, 20, 24])
    fr = [rng.uniform(0.35, 0.5), rng.uniform(0.25, 0.35), rng.uniform(0.1, 0.18)]
    fr.append(1 - sum(fr))
    tot = pick(rng, [200, 400, 500, 800])
    n = [round(f * tot) for f in fr]
    n[3] = tot - sum(n[:3])
    if n[3] <= 0:
        return None
    t = [x / tot * cyc for x in n]
    stem = (f'A sample of {tot} asynchronously dividing cells contained {n[0]} in G1, {n[1]} in S, {n[2]} in G2 and {n[3]} in mitosis. The total cell cycle lasts {cyc} hours. '
            'Estimate the duration of each phase.')
    return num(stem, f'G1 {t[0]:.1f} h; S {t[1]:.1f} h; G2 {t[2]:.1f} h; M {t[3]:.1f} h',
               f'Duration = (number in phase/total) × cycle time (M1): G1 {n[0]}/{tot} × {cyc} = {t[0]:.1f} h; S {t[1]:.1f} h; G2 {t[2]:.1f} h (A1); M {t[3]:.1f} h (A1).', 3)


def _cyclin_dq(rng, slot):
    hrs = [0, 2, 4, 6, 8, 10, 12, 14, 16]
    peak = rng.randint(6, 7)
    cA = [round(5 + 80 * max(0, 1 - abs(h - 2 * peak) / 6), 0) if h <= 2 * peak else 5 for h in hrs]
    intro = ('The concentration of a mitotic cyclin (arbitrary units) was measured in a population of synchronised cells. Cells were observed entering mitosis when cyclin concentration was highest; '
             'shortly afterwards the cyclin concentration fell sharply.\n\n' + table(['Time / h', 'Cyclin concentration / AU'], list(zip(hrs, [f'{c:.0f}' for c in cA]))))
    tmax = hrs[cA.index(max(cA))]
    rate = (cA[hrs.index(tmax)] - cA[hrs.index(tmax) - 2]) / 4
    parts = [
        ('State the time at which cyclin concentration was highest.', f'{tmax} h', f'{tmax} h (A1).', 1),
        (f'Calculate the mean rate of increase in cyclin concentration between {tmax - 4} and {tmax} h.', f'{rate:.1f} AU h⁻¹', f'({cA[hrs.index(tmax)]:.0f} − {cA[hrs.index(tmax) - 2]:.0f})/4 (M1) = {rate:.1f} (A1).', 2),
        ('Explain how this cyclin causes the cell to enter mitosis.', 'Cyclin binds and activates a CDK; the cyclin–CDK complex phosphorylates proteins that cause chromosome condensation, nuclear envelope breakdown and spindle formation.', 'Binds CDK (A1); phosphorylation of targets (A1); mitotic events (A1).', 3),
        ('Explain why the cyclin is rapidly degraded after mitosis begins.', 'To inactivate the CDK so the cell can complete mitosis and return to G1; ensures one division per cycle.', 'CDK inactivation (A1); prevents repeated division/allows exit (A1).', 2),
        ('Predict the effect of a mutation preventing degradation of this cyclin.', 'CDK remains active; cells may be unable to exit mitosis or divide abnormally; loss of cell-cycle control.', 'Valid prediction (A1).', 1),
        ('Suggest why cells were synchronised for this experiment.', 'So all cells are at the same stage, allowing changes in cyclin with cell-cycle stage to be detected.', 'Same stage (A1).', 1),
        ('Outline the role of checkpoints in the cell cycle.', 'Checkpoints (G1/S, G2/M, spindle) check DNA damage, cell size and chromosome attachment before the cycle continues, preventing division of damaged cells.', 'Named checkpoint (A1); function (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch07-st2', _cyclin_dq)


S('ch07-st3',
  terms=[('gene expression', 'the process by which information in a gene is used to make a functional product such as a polypeptide'),
         ('transcription factor', 'a protein that binds to specific DNA sequences such as promoters or enhancers and increases or decreases transcription of a gene'),
         ('promoter', 'a DNA sequence near the start of a gene where RNA polymerase and transcription factors bind'),
         ('epigenetics', 'heritable changes in gene expression that do not involve changes to the base sequence of DNA'),
         ('DNA methylation', 'the addition of methyl groups to cytosine bases (usually in CpG sites), which generally represses transcription'),
         ('histone acetylation', 'the addition of acetyl groups to histone proteins, loosening chromatin and increasing transcription'),
         ('genomic imprinting', 'the expression of a gene depending on whether it was inherited from the mother or the father, controlled by methylation'),
         ('epigenome', 'the overall pattern of chemical modifications (such as methylation and histone modification) on a cell’s DNA and histones')],
  facts=[('Which base is methylated in DNA methylation?', 'cytosine', ['adenine', 'thymine', 'uracil'], 'Often at CpG sites.'),
         ('What is the effect of histone acetylation on chromatin?', 'it becomes less condensed, allowing transcription', ['it becomes more condensed', 'it is digested', 'it is converted to RNA'], 'Euchromatin.'),
         ('Which natural experiment showed epigenetic effects of famine on later generations?', 'the Dutch Hunger Winter of 1944–45', ['the Irish potato famine of 1845 only', 'the Black Death', 'the Dust Bowl'], 'Children born after the famine had altered methylation.'),
         ('Which is an example of an environmental factor affecting gene expression?', 'temperature affecting fur colour in Himalayan rabbits', ['the number of chromosomes', 'the genetic code', 'the structure of DNA nucleotides'], 'Enzyme in fur pigment active only in cool areas.'),
         ('Where do transcription factors bind?', 'to specific DNA sequences such as promoters and enhancers', ['to ribosomes', 'to tRNA', 'to the cell wall'], 'Regulate transcription.')],
  mc2=[('Why do different cell types in one organism have different structures although they have the same genome?', 'Different genes are expressed in each cell type.', ['Each cell type has different DNA.', 'Some cells lose genes.', 'Mutation occurs in each cell.'], 'Differential gene expression.'),
       ('Why does DNA methylation of a promoter usually reduce gene expression?', 'Methyl groups prevent transcription factors and RNA polymerase binding and attract proteins that condense chromatin.', ['It changes the base sequence.', 'It destroys the gene.', 'It speeds up translation.'], 'Repression.'),
       ('Why do monozygotic twins become more different with age?', 'Their epigenetic marks diverge due to different environments and random changes.', ['Their DNA sequences change completely.', 'They have different genes from birth.', 'Methylation is identical for life.'], 'Epigenetic drift.'),
       ('Why can epigenetic changes be inherited by daughter cells?', 'Methylation patterns are copied when DNA is replicated.', ['They change the DNA sequence.', 'They are lost at each division.', 'They are stored in ribosomes.'], 'Maintenance methyltransferase.')],
  mc3=[('A gene’s promoter is highly methylated in liver cells but not in pancreatic cells. Which is most likely?', 'The gene is expressed in pancreatic cells but not liver cells.', ['The gene is expressed in both.', 'The gene is expressed in liver cells only.', 'The gene is absent from liver cells.'], 'Methylation represses.'),
       ('A drug inhibits histone deacetylase. What is the likely effect on gene expression?', 'Histones remain acetylated, so more genes are transcribed.', ['Fewer genes are transcribed.', 'DNA is methylated.', 'Translation stops.'], 'Used in some cancer treatments.'),
       ('Agouti mice fed a diet rich in methyl donors during pregnancy had offspring with brown rather than yellow coats. What does this show?', 'Maternal diet can alter methylation and gene expression in offspring.', ['Diet changes the DNA sequence.', 'Coat colour is not genetic.', 'Methylation increases agouti expression.'], 'Epigenetic effect of environment.')],
  why=[('Explain how DNA methylation and histone modification regulate gene expression.', 'Methylation of cytosine in CpG islands of promoters blocks binding of transcription factors and recruits proteins that condense chromatin, silencing genes; histone acetylation neutralises positive charges, loosening DNA–histone binding and allowing transcription; deacetylation and methylation of histones condense chromatin and repress genes.'),
       ('Explain how transcription factors control gene expression.', 'Transcription factors bind to specific base sequences in promoters or enhancers; activators help RNA polymerase bind and increase transcription; repressors block binding; hormones such as oestradiol can activate transcription factors; combinations of factors give tissue-specific expression.'),
       ('Explain how the environment can influence gene expression.', 'Environmental factors (diet, temperature, stress, toxins) can alter methylation and histone modification; e.g. Himalayan rabbit fur colour depends on temperature-sensitive enzyme; Dutch Hunger Winter offspring had altered methylation of IGF2; changes may persist and sometimes be inherited.')],
  contrast=[('genetic changes', 'epigenetic changes', 'Genetic changes alter the base sequence of DNA (mutations); epigenetic changes alter gene expression through chemical marks such as methylation without changing the base sequence.'),
            ('DNA methylation', 'histone acetylation', 'DNA methylation adds methyl groups to cytosine and generally silences genes; histone acetylation adds acetyl groups to histones, loosening chromatin and activating genes.')],
  misc=[('Epigenetic changes alter the base sequence of DNA.', 'Epigenetic changes affect gene expression without altering the base sequence.'),
        ('All cells in the body express all their genes all the time.', 'Each cell type expresses only a subset of its genes.'),
        ('Epigenetic marks are completely erased in every generation.', 'Most are reset in gametes and early embryos, but some, such as imprints, persist and some may be transgenerational.')],
  cases=[('the Dutch Hunger Winter (1944–45)', 'People exposed to famine before birth had different IGF2 methylation and higher rates of obesity and heart disease decades later.', 'epigenetic effects of the environment', 'Nutrition during development altered methylation patterns, with lasting effects on gene expression.'),
         ('agouti mice', 'Genetically identical mice can be yellow and obese or brown and lean depending on methylation of the agouti gene.', 'DNA methylation', 'Methylation silences the agouti gene, changing phenotype without changing DNA sequence.'),
         ('monozygotic twin studies', 'Older identical twins show greater differences in methylation patterns than young twins.', 'epigenetic drift', 'Different environments and random changes alter epigenetic marks over a lifetime.')],
  evaluate=[('Epigenetics shows that the environment is as important as genes in determining phenotype.', ['methylation and histone changes respond to diet, stress and toxins', 'identical twins diverge in phenotype'], ['the DNA sequence still sets the range of possible phenotypes', 'many epigenetic effects are small or reset each generation'], 'Epigenetics shows genes and environment interact closely; phenotype results from both, rather than one being more important.')],
  extended=[('Explain how gene expression is regulated in eukaryotes, including epigenetic mechanisms.', 'Transcription factors, promoters, enhancers; methylation of cytosine; histone acetylation/deacetylation; chromatin condensation; tissue-specific expression; environment (diet, temperature); inheritance of marks in mitosis; imprinting; twins; Dutch Hunger Winter.', 8),
            ('Describe how the environment can affect the phenotype of an organism through gene expression.', 'Himalayan rabbit, hydrangea flower colour vs pH (not epigenetic), agouti mice, Dutch Hunger Winter, temperature-dependent sex determination in reptiles; mechanisms: methylation, histone modification, enzyme activity.', 6)],
  )


def _methyl_dq(rng, slot):
    n = 7
    meth = sorted(round(rng.uniform(5, 90), 0) for _ in range(n))
    expr = [round(max(1, 100 - 1.0 * m + rng.uniform(-10, 10)), 0) for m in meth]
    r = pearson(meth, expr)
    intro = ('The percentage methylation of the promoter of a tumour suppressor gene and the relative expression of the gene (mRNA, % of normal tissue) were measured in seven tumour samples.\n\n'
             + table(['Sample', 'Promoter methylation / %', 'Relative expression / %'], [(i + 1, f'{a:.0f}', f'{b:.0f}') for i, (a, b) in enumerate(zip(meth, expr))]))
    parts = [
        ('State the relative expression in the sample with the highest methylation.', f'{expr[-1]:.0f} %', f'{expr[-1]:.0f} (A1).', 1),
        ('Calculate the Pearson correlation coefficient between methylation and expression.', f'r = {r:.2f}', f'Use of calculator/formula (M1); r = {r:.2f} (A1).', 2),
        ('Describe the relationship shown.', 'Strong negative correlation: as promoter methylation increases, gene expression decreases.', 'Negative (A1); strong (A1).', 2),
        ('Explain how promoter methylation reduces gene expression.', 'Methyl groups on cytosines block binding of transcription factors/RNA polymerase and recruit proteins that condense chromatin, so the gene is not transcribed.', 'Blocks binding (A1); condensed chromatin (A1).', 2),
        ('Suggest how increased methylation of this gene could contribute to tumour formation.', 'Less tumour suppressor protein is made, so the cell cycle is not stopped and damaged cells are not removed by apoptosis; uncontrolled division.', 'Less tumour suppressor (A1); uncontrolled division (A1).', 2),
        ('Explain why correlation alone does not prove that methylation causes reduced expression.', 'Another factor may cause both; reduced expression could cause methylation; experiment needed (e.g. demethylating drug).', 'Correlation ≠ causation with reason (A1).', 1),
        ('Suggest a possible treatment based on these results.', 'Drugs that inhibit DNA methyltransferase (demethylating agents) or histone deacetylase inhibitors to reactivate the gene.', 'Valid treatment (A1).', 1),
        ('Outline how histone modification could also affect the expression of this gene.', 'Histone acetylation loosens chromatin and increases transcription; deacetylation or histone methylation condenses chromatin and silences the gene.', 'Acetylation (A1); deacetylation/condensation (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch07-st3', _methyl_dq)


S('ch07-st4',
  terms=[('water potential', 'the potential energy of water per unit volume relative to pure water at atmospheric pressure (ψ, in kPa or MPa); water moves from higher to lower ψ'),
         ('solute potential', 'the component of water potential due to dissolved solutes (ψs); always negative or zero'),
         ('pressure potential', 'the component of water potential due to pressure (ψp); positive in turgid plant cells, negative (tension) in xylem'),
         ('turgid', 'describes a plant cell that is full of water, with the cytoplasm pushing against the cell wall'),
         ('plasmolysis', 'the shrinking of the protoplast away from the cell wall when a plant cell loses water in a hypertonic solution'),
         ('isotonic', 'having the same solute concentration (water potential) as another solution, so there is no net movement of water'),
         ('hypotonic', 'having a lower solute concentration (higher water potential) than the cell'),
         ('incipient plasmolysis', 'the point at which the protoplast just begins to pull away from the cell wall, where ψp = 0')],
  facts=[('What is the water potential of pure water at atmospheric pressure?', '0 kPa', ['100 kPa', '−100 kPa', '1 kPa'], 'The reference value.'),
         ('What happens to a red blood cell in pure water?', 'it swells and bursts (haemolysis)', ['it becomes turgid', 'it plasmolyses', 'it shrinks'], 'No cell wall.'),
         ('What is the equation for water potential?', 'ψ = ψs + ψp', ['ψ = ψs − ψp', 'ψ = ψs × ψp', 'ψ = ψp/ψs'], 'Solute plus pressure components.'),
         ('What happens to an animal cell in a hypertonic solution?', 'it shrinks (crenation)', ['it bursts', 'it becomes turgid', 'nothing'], 'Loses water.'),
         ('Why are intravenous drips made of 0.9 % saline?', 'it is isotonic with blood plasma', ['it kills bacteria', 'it provides glucose', 'it is hypotonic'], 'Prevents osmotic damage.')],
  mc2=[('Why do plant cells not burst in pure water?', 'The cell wall resists expansion, so pressure potential rises until ψ inside equals that outside.', ['They have contractile vacuoles.', 'Water cannot enter plant cells.', 'They have no vacuole.'], 'Turgor.'),
       ('Why is solute potential always negative?', 'Solutes reduce the free energy of water compared with pure water, which has ψ = 0.', ['Solutes increase water pressure.', 'Pure water has negative potential.', 'It is measured below zero °C.'], 'Relative to pure water.'),
       ('Why does a potato strip in pure water gain mass?', 'Pure water has a higher water potential than the potato cells, so water enters by osmosis.', ['Pure water has a lower water potential.', 'Solutes enter the strip.', 'Starch absorbs water by diffusion only.'], 'Water moves down the gradient.'),
       ('Why is the tension in xylem described as negative pressure potential?', 'Transpiration pulls water up, so the water is under tension below atmospheric pressure.', ['Xylem is under high positive pressure.', 'Xylem contains no water.', 'Solutes are pumped into xylem.'], 'Cohesion–tension.')],
  mc3=[('A plant cell has ψs = −800 kPa and ψp = +300 kPa. It is placed in a solution with ψ = −700 kPa. Which way does water move?', 'Out of the cell', ['Into the cell', 'No net movement', 'Into the cell until ψp reaches zero'], 'Cell ψ = −500 kPa; water moves from −500 to −700 kPa.'),
       ('Cell A has ψ = −400 kPa and cell B has ψ = −650 kPa. Which statement is correct?', 'Water moves from A to B.', ['Water moves from B to A.', 'No water moves.', 'Solutes move from A to B by osmosis.'], 'Higher (less negative) to lower.'),
       ('At incipient plasmolysis, what is the pressure potential of the cell?', '0 kPa', ['equal to ψs', 'positive and maximum', 'equal to −ψs'], 'Protoplast just leaving the wall.')],
  why=[('Explain the movement of water into and out of plant cells in terms of water potential.', 'Water moves by osmosis from higher to lower ψ; in a hypotonic solution water enters, ψp rises as the protoplast pushes on the wall until ψ inside equals outside (turgid); in a hypertonic solution water leaves, ψp falls to zero and the protoplast shrinks from the wall (plasmolysis).'),
       ('Explain why animal cells need to be kept in isotonic surroundings.', 'Animal cells lack walls; in hypotonic solutions water enters and they swell and burst (haemolysis); in hypertonic solutions water leaves and they shrink (crenation); tissue fluid and plasma are kept isotonic by osmoregulation; medical solutions are isotonic.'),
       ('Explain how the water potential of a plant tissue can be estimated experimentally.', 'Cut equal pieces of tissue; blot and weigh; place in a range of sucrose solutions; leave to equilibrate; reweigh; calculate % change in mass; plot against concentration; the concentration at zero change is isotonic; convert to ψs (ψ of tissue equals ψ of that solution).')],
  contrast=[('solute potential', 'pressure potential', 'Solute potential is due to dissolved solutes and is always zero or negative; pressure potential is due to pressure on the water, positive in turgid cells and negative under tension in xylem.'),
            ('turgid plant cells', 'plasmolysed plant cells', 'Turgid cells have a protoplast pressed against the wall with positive pressure potential; plasmolysed cells have lost water so the protoplast has shrunk away from the wall and ψp is zero.')],
  misc=[('Water moves from a more negative water potential to a less negative one.', 'Water moves from higher (less negative) to lower (more negative) water potential.'),
        ('Plant cells burst in pure water like animal cells.', 'The cell wall prevents bursting; the cell becomes turgid.'),
        ('Solutes move by osmosis.', 'Osmosis is the movement of water; solutes move by diffusion or transport.')],
  cases=[('wilting of lettuce leaves', 'Lettuce left out wilts but becomes crisp again when placed in water.', 'turgor and water potential', 'Water loss lowers ψp and cells become flaccid; in water ψ outside is higher so water enters and cells become turgid again.'),
         ('salt used to preserve food', 'Salting fish or meat prevents bacterial growth.', 'osmosis and water potential', 'The very low ψ outside draws water out of bacterial cells by osmosis, so they cannot grow.')],
  evaluate=[('The water potential model fully explains water movement in plants.', ['ψ = ψs + ψp predicts the direction of osmosis between cells and solutions', 'explains turgor, plasmolysis and xylem tension'], ['water also moves by mass flow and through aquaporins whose regulation affects rates', 'ψ does not predict the rate of movement'], 'The model correctly predicts the direction of water movement but must be combined with membrane permeability and mass flow to explain rates.')],
  extended=[('Explain the concept of water potential and use it to explain the behaviour of plant and animal cells in solutions of different concentrations.', 'Definition; ψ of pure water 0; ψ = ψs + ψp; units; water moves high to low ψ; plant cells: turgid, flaccid, plasmolysis, incipient plasmolysis, wall; animal cells: haemolysis, crenation; isotonic medical solutions; osmoregulation.', 8),
            ('Describe an experiment to determine the water potential of potato tissue and explain how the results are analysed.', 'Cylinders, cork borer, equal size; sucrose series; blot and weigh; equilibration; reweigh; % change; graph; interpolation to zero; ψ = ψs of solution; controls: temperature, time, surface area; repeats.', 6)],
  )


def _psi_s(c, T=298):
    return -c * 8.31 * T


@R.add('ch07-st4', 'C3', (1, 5), 'numerical')
def psi_calc(rng, slot):
    ps = -rng.randint(5, 15) * 100
    pp = rng.randint(1, 8) * 100
    psi = ps + pp
    ext = -rng.randint(2, 14) * 100
    if ext == psi:
        return None
    direction = 'into the cell' if ext > psi else 'out of the cell'
    stem = f'A plant cell has a solute potential of {ps} kPa and a pressure potential of +{pp} kPa. Calculate its water potential and state the direction of net water movement when it is placed in a solution of water potential {ext} kPa.'
    return num(stem, f'ψ = {psi} kPa; water moves {direction}',
               f'ψ = ψs + ψp = {ps} + {pp} = {psi} kPa (A1); water moves from higher to lower ψ, so {direction} (A1).', 2 if slot.d <= 2 else 3)


def _potato_dq(rng, slot):
    conc = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    iso = rng.uniform(0.22, 0.38)
    k = rng.uniform(40, 55)
    pct = [round(k * (iso - c) / (1 + 1.2 * abs(iso - c)) + rng.uniform(-0.8, 0.8), 1) for c in conc]
    m0 = [round(rng.uniform(2.40, 2.70), 2) for _ in conc]
    m1 = [round(a * (1 + p / 100), 2) for a, p in zip(m0, pct)]
    pct2 = [100 * (b - a) / a for a, b in zip(m0, m1)]
    j = 1
    z = interp_zero(conc, pct2)
    if z is None:
        return None
    ps = _psi_s(z)
    intro = ('Potato cylinders were blotted, weighed and placed in sucrose solutions of different concentrations for 24 hours at 25 °C, then blotted and reweighed.\n\n'
             + table(['Sucrose / mol dm⁻³', 'Initial mass / g', 'Final mass / g', 'Change in mass / %'],
                     [(c, f'{a:.2f}', f'{b:.2f}', '?' if i == j else f'{p:+.1f}') for i, (c, a, b, p) in enumerate(zip(conc, m0, m1, pct2))]))
    parts = [
        (f'Calculate the percentage change in mass at {conc[j]} mol dm⁻³.', f'{pct2[j]:+.1f} %', f'({m1[j]:.2f} − {m0[j]:.2f})/{m0[j]:.2f} × 100 (M1) = {pct2[j]:+.1f} % (A1).', 2),
        ('Explain why percentage change in mass, rather than change in mass, was calculated.', 'The cylinders had different initial masses, so percentage change allows fair comparison.', 'Different starting masses (A1).', 1),
        ('Estimate the sucrose concentration that is isotonic with the potato cells.', f'about {z:.2f} mol dm⁻³', f'Concentration at 0 % change by interpolation (M1) ≈ {z:.2f} (A1).', 2),
        (f'Calculate the water potential of the potato cells using ψs = −CRT (R = 8.31 J K⁻¹ mol⁻¹, T = 298 K; result in kPa when C is in mol dm⁻³).', f'about {ps:.0f} kPa',
         f'ψ = −{z:.2f} × 8.31 × 298 (M1) = {ps:.0f} kPa (A1); at isotonic point ψ tissue = ψ solution.', 2),
        ('Explain the change in mass in the 0.0 mol dm⁻³ solution.', 'Water has a higher ψ than the potato cells, so water enters by osmosis; cells become turgid and mass increases.', 'ψ comparison (A1); osmosis into cells (A1).', 2),
        ('Explain why the cylinders were blotted before weighing.', 'To remove surface solution, which would add to the mass and vary between cylinders.', 'Remove surface liquid (A1).', 1),
        ('State two variables that should be controlled.', 'Size/surface area of cylinders; temperature; time; volume of solution; potato variety/source.', 'Two valid (A1 A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch07-st4', _potato_dq)


# =============================================================================================
# ch08 D3.1 Reproduction and D3.2 Inheritance
# =============================================================================================
S('ch08-st1',
  terms=[('asexual reproduction', 'reproduction by one parent without fusion of gametes, producing genetically identical offspring'),
         ('sexual reproduction', 'reproduction involving the fusion of haploid gametes from two parents, producing genetically varied offspring'),
         ('follicle-stimulating hormone (FSH)', 'a hormone from the anterior pituitary that stimulates development of follicles in the ovary and secretion of oestradiol'),
         ('luteinising hormone (LH)', 'a pituitary hormone whose surge triggers ovulation and the formation of the corpus luteum'),
         ('corpus luteum', 'the structure formed from the follicle after ovulation, which secretes progesterone'),
         ('in vitro fertilisation (IVF)', 'fertilisation of eggs by sperm outside the body, after hormone treatment to stimulate the ovaries, followed by transfer of embryos to the uterus'),
         ('implantation', 'the embedding of the blastocyst into the endometrium of the uterus'),
         ('human chorionic gonadotropin (hCG)', 'a hormone secreted by the early embryo that maintains the corpus luteum; detected by pregnancy tests')],
  facts=[('Which hormone surge triggers ovulation?', 'luteinising hormone (LH)', ['progesterone', 'insulin', 'testosterone'], 'Around day 14.'),
         ('Which structure secretes progesterone after ovulation?', 'the corpus luteum', ['the anterior pituitary', 'the hypothalamus', 'the endometrium'], 'Maintains the endometrium.'),
         ('Where is testosterone produced?', 'in interstitial cells of the testes', ['in the prostate gland', 'in the seminal vesicles', 'in the anterior pituitary'], 'Leydig cells.'),
         ('Where does fertilisation normally occur?', 'in the oviduct', ['in the uterus', 'in the ovary', 'in the vagina'], 'Fallopian tube.'),
         ('Which hormone does a pregnancy test detect?', 'hCG', ['FSH', 'oestradiol', 'LH'], 'Produced by the embryo.'),
         ('Which hormone is produced by the ovarian follicle and causes thickening of the endometrium?', 'oestradiol', ['progesterone', 'hCG', 'FSH'], 'Rising oestradiol also triggers the LH surge.')],
  mc2=[('Why does oestradiol exert positive feedback before ovulation?', 'High oestradiol stimulates more LH and FSH secretion, causing the LH surge.', ['It inhibits LH completely.', 'It destroys the corpus luteum.', 'It lowers FSH to zero.'], 'Positive feedback.'),
       ('Why does menstruation begin if fertilisation does not occur?', 'The corpus luteum degenerates, so progesterone falls and the endometrium is no longer maintained.', ['FSH rises sharply.', 'hCG is produced.', 'Oestradiol increases.'], 'Loss of progesterone.'),
       ('Why are women given hormones before IVF?', 'To suppress the natural cycle and then stimulate many follicles to develop so several eggs can be collected.', ['To kill sperm.', 'To prevent implantation.', 'To remove the uterus.'], 'Superovulation.'),
       ('Why is sexual reproduction an advantage in a changing environment?', 'It produces genetic variation, so some offspring may be suited to new conditions.', ['It is faster than asexual reproduction.', 'It needs only one parent.', 'Offspring are identical.'], 'Variation for selection.')],
  mc3=[('A blood test shows high progesterone 21 days after the start of menstruation. What does this suggest?', 'Ovulation has occurred and a corpus luteum is present.', ['Ovulation has not occurred.', 'Menstruation is beginning.', 'FSH is at its peak.'], 'Progesterone comes from the corpus luteum.'),
       ('In an IVF clinic, 360 embryos were transferred and 108 resulted in live births. What is the success rate per embryo?', '30 %', ['3 %', '33 %', '108 %'], '108/360 × 100.'),
       ('A contraceptive pill contains synthetic oestrogen and progesterone. How does it prevent ovulation?', 'It inhibits FSH and LH secretion by negative feedback, so follicles do not mature and no LH surge occurs.', ['It kills eggs.', 'It increases LH.', 'It blocks the oviduct.'], 'Negative feedback.')],
  why=[('Explain the roles of hormones in the menstrual cycle.', 'FSH from the pituitary stimulates follicle development and oestradiol secretion; oestradiol thickens the endometrium and at high levels causes positive feedback giving an LH surge; LH triggers ovulation and formation of the corpus luteum; progesterone maintains the endometrium and inhibits FSH/LH; corpus luteum degenerates, progesterone falls, menstruation.'),
       ('Explain the stages of IVF.', 'Drugs suppress the natural cycle; FSH injections stimulate many follicles; hCG/LH injection matures eggs; eggs collected; mixed with sperm or ICSI; embryos cultured; one or two transferred to the uterus; progesterone supports implantation.'),
       ('Explain how hormones maintain early pregnancy.', 'The embryo secretes hCG, which maintains the corpus luteum; the corpus luteum continues to secrete progesterone and oestradiol, maintaining the endometrium; later the placenta takes over progesterone production.')],
  contrast=[('sexual reproduction', 'asexual reproduction', 'Sexual reproduction involves meiosis and fusion of gametes, producing genetically varied offspring; asexual reproduction involves one parent and mitosis, producing genetically identical offspring.'),
            ('FSH', 'LH', 'FSH stimulates follicle growth and oestradiol secretion; LH triggers ovulation and the development of the corpus luteum.')],
  misc=[('Ovulation happens on the first day of the menstrual cycle.', 'Day 1 is the start of menstruation; ovulation usually occurs around day 14.'),
        ('Progesterone triggers ovulation.', 'The LH surge triggers ovulation; progesterone is secreted afterwards by the corpus luteum.'),
        ('Asexual reproduction is a primitive process that animals never use.', 'Many animals reproduce asexually, e.g. aphids by parthenogenesis and Hydra by budding.')],
  cases=[('the development of IVF by Edwards and Steptoe', 'Louise Brown, the first “test-tube baby”, was born in 1978.', 'hormonal control of reproduction', 'Hormone treatment controlled the ovarian cycle so eggs could be collected, fertilised outside the body and implanted.'),
         ('aphids reproducing by parthenogenesis in summer', 'Female aphids produce clones of daughters rapidly in summer and reproduce sexually in autumn.', 'sexual and asexual reproduction', 'Asexual reproduction allows rapid population growth, while sexual reproduction produces variation before winter.')],
  evaluate=[('IVF should be freely available to all who want it.', ['allows infertile couples to have children', 'success rates improving'], ['high cost to health systems; low success rates in older women', 'risk of multiple births and ovarian hyperstimulation; ethical issues about spare embryos'], 'IVF should be available on the basis of medical need and likelihood of success, with limits to manage costs and risks.')],
  extended=[('Explain how hormones control the menstrual cycle and how this knowledge is used in IVF.', 'FSH, LH, oestradiol, progesterone; follicular phase, ovulation, luteal phase; negative and positive feedback; corpus luteum; menstruation; IVF: down-regulation, FSH superovulation, hCG trigger, egg collection, fertilisation, embryo transfer, progesterone support.', 8),
            ('Compare the structure and function of the male and female reproductive systems.', 'Testes, epididymis, sperm duct, seminal vesicles, prostate, penis; ovaries, oviducts, uterus, endometrium, cervix, vagina; gamete production; hormones; sites of fertilisation and development.', 6)],
  )


def _ivf_dq(rng, slot):
    ages = ['under 35', '35–37', '38–39', '40–42', 'over 42']
    rates = [rng.uniform(0.30, 0.36)]
    for f in [0.8, 0.62, 0.45, 0.2]:
        rates.append(rates[0] * f * rng.uniform(0.95, 1.05))
    cycles = [rng.randint(3000, 6000), rng.randint(1500, 3000), rng.randint(900, 1800), rng.randint(800, 1500), rng.randint(300, 700)]
    births = [round(c * r) for c, r in zip(cycles, rates)]
    pr = [100 * b / c for b, c in zip(births, cycles)]
    j = 3
    intro = ('The number of IVF treatment cycles started and live births at a fertility clinic network are shown by age of the woman.\n\n'
             + table(['Age / years', 'Cycles started', 'Live births', 'Live births per cycle / %'], [(a, c, b, '?' if i == j else f'{p:.1f}') for i, (a, c, b, p) in enumerate(zip(ages, cycles, births, pr))]))
    tot = 100 * sum(births) / sum(cycles)
    parts = [
        (f'Calculate the live birth rate per cycle for women aged {ages[j]}.', f'{pr[j]:.1f} %', f'{births[j]}/{cycles[j]} × 100 (M1) = {pr[j]:.1f} % (A1).', 2),
        ('Calculate the overall live birth rate for all ages.', f'{tot:.1f} %', f'{sum(births)}/{sum(cycles)} × 100 = {tot:.1f} % (A1).', 1),
        ('Describe the relationship between age and success rate.', 'Success rate decreases with age, especially steeply above 40.', 'Decrease (A1); steeper at older ages (A1).', 2),
        ('Suggest reasons for the relationship.', 'Older women have fewer and lower-quality oocytes; more non-disjunction/chromosome abnormalities; lower response to FSH; implantation less likely.', 'Two reasons (A1 A1).', 2),
        ('Outline the role of FSH injections in IVF.', 'Stimulate development of many follicles so several eggs can be collected.', 'Several follicles/eggs (A1).', 1),
        ('Explain why progesterone is given after embryo transfer.', 'Maintains the endometrium so implantation can occur and the embryo is supported.', 'Maintains endometrium (A1); implantation (A1).', 2),
        ('Discuss one ethical issue raised by IVF.', 'Fate of spare embryos; multiple births; cost and access; selection of embryos.', 'Issue with explanation (A1).', 1),
        ('Calculate the percentage difference in live birth rate between the under-35 and over-42 groups.', f'{signed(pct_change(pr[0], pr[-1]))} %', f'({pr[-1]:.1f} − {pr[0]:.1f})/{pr[0]:.1f} × 100 (M1) = {signed(pct_change(pr[0], pr[-1]))} % (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch08-st1', _ivf_dq)

pct_items(R, 'ch08-st1', [
    ('During the follicular phase, a woman’s plasma oestradiol rose from {a} pg cm⁻³ on day 3 to {b} pg cm⁻³ on day 13.', 'pg cm⁻³', 30, 60, 3.0, 6.0, 0, 'the developing follicle secretes increasing amounts of oestradiol under FSH stimulation, leading to positive feedback and the LH surge.'),
    ('Plasma progesterone fell from {a} ng cm⁻³ on day 22 to {b} ng cm⁻³ on day 28.', 'ng cm⁻³', 10, 18, -0.9, -0.7, 1, 'the corpus luteum degenerates when no hCG is produced, so progesterone falls and menstruation begins.'),
])


S('ch08-st2',
  terms=[('pollination', 'the transfer of pollen from an anther to a stigma'),
         ('cross-pollination', 'transfer of pollen from the anther of one plant to the stigma of a different plant of the same species'),
         ('self-incompatibility', 'a genetic mechanism that prevents pollen from fertilising ovules of the same plant, promoting cross-fertilisation'),
         ('double fertilisation', 'in flowering plants, the fusion of one male nucleus with the egg (forming the zygote) and another with two polar nuclei (forming the endosperm)'),
         ('seed dispersal', 'the spreading of seeds away from the parent plant, reducing competition and colonising new areas'),
         ('germination', 'the development of a seed into a seedling, requiring water, oxygen and a suitable temperature'),
         ('stigma', 'the sticky surface of the carpel that receives pollen grains'),
         ('ovule', 'the structure in the ovary containing the female gamete, which develops into a seed after fertilisation')],
  facts=[('Which part of the flower produces pollen?', 'the anther', ['the stigma', 'the ovary', 'the sepal'], 'Part of the stamen.'),
         ('Which structure develops into a seed?', 'the ovule', ['the ovary wall', 'the petal', 'the style'], 'The ovary becomes the fruit.'),
         ('What grows down the style to carry male gametes to the ovule?', 'the pollen tube', ['the filament', 'the radicle', 'the xylem'], 'Grows from the pollen grain.'),
         ('Which is a feature of wind-pollinated flowers?', 'large, feathery stigmas that hang outside the flower', ['large, scented petals', 'nectaries', 'sticky pollen'], 'Catch airborne pollen.'),
         ('Which hormone is released in germinating seeds to stimulate production of amylase?', 'gibberellin', ['auxin', 'ethylene', 'insulin'], 'Starch to maltose.')],
  mc2=[('Why do many plants have mechanisms that prevent self-pollination?', 'Cross-pollination increases genetic variation and avoids inbreeding depression.', ['Self-pollination produces no seeds.', 'Insects cannot self-pollinate flowers.', 'It reduces variation.'], 'Outbreeding.'),
       ('Why do seeds need oxygen to germinate?', 'For aerobic respiration to release energy for growth.', ['To make chlorophyll.', 'For photosynthesis.', 'To dissolve starch.'], 'ATP supply.'),
       ('Why is water needed for germination?', 'To activate enzymes, swell the seed and allow mobilisation of food reserves.', ['To provide light.', 'To make the seed coat harder.', 'To stop respiration.'], 'Imbibition.'),
       ('Why is seed dispersal advantageous?', 'It reduces competition with the parent and siblings and allows colonisation of new areas.', ['It increases competition.', 'It keeps seeds near the parent.', 'It prevents germination.'], 'Colonisation.')],
  mc3=[('Of 250 seeds sown, 190 germinated. What is the germination percentage?', '76 %', ['24 %', '190 %', '1.3 %'], '190/250 × 100.'),
       ('A pollen tube grew 420 µm in 35 minutes. What was its mean growth rate?', '12 µm min⁻¹', ['0.083 µm min⁻¹', '14 700 µm min⁻¹', '120 µm min⁻¹'], '420/35.'),
       ('A flower has brightly coloured petals, nectar and scent. What is its most likely pollinator?', 'insects such as bees', ['wind', 'water', 'gravity'], 'Attracts animals.')],
  why=[('Explain how insect-pollinated flowers are adapted for pollination.', 'Brightly coloured, scented petals and nectar guides attract insects; nectaries reward them; anthers positioned to brush pollen onto the insect; sticky or spiky pollen adheres; stigma positioned to collect pollen from visiting insects.'),
       ('Explain the events from pollination to fertilisation in a flowering plant.', 'Pollen lands on a compatible stigma; the pollen grain germinates and a pollen tube grows down the style by secreting enzymes; the male gametes travel in the tube; it enters the ovule through the micropyle; one male nucleus fuses with the egg (zygote), the other with polar nuclei (endosperm).'),
       ('Explain how a seed germinates.', 'Water is absorbed (imbibition), activating gibberellin production; gibberellin stimulates amylase production in the aleurone layer; starch is hydrolysed to maltose and glucose for respiration; the radicle emerges, then the plumule; growth by mitosis.')],
  contrast=[('insect-pollinated flowers', 'wind-pollinated flowers', 'Insect-pollinated flowers have large coloured scented petals, nectar and sticky pollen; wind-pollinated flowers have small dull petals, exposed anthers and feathery stigmas and produce large amounts of light pollen.'),
            ('self-pollination', 'cross-pollination', 'Self-pollination transfers pollen within the same plant, giving less variation; cross-pollination transfers pollen between different plants, increasing variation.')],
  misc=[('Pollination and fertilisation are the same process.', 'Pollination is pollen transfer to the stigma; fertilisation is fusion of male and female gametes in the ovule.'),
        ('Seeds need light to germinate.', 'Most seeds need water, oxygen and warmth; light is needed by only some species.'),
        ('Fruits develop from ovules.', 'Fruits develop from the ovary wall; seeds develop from ovules.')],
  cases=[('self-incompatibility in Brassica', 'Pollen with an S-allele matching the stigma’s S-alleles is rejected and cannot grow a pollen tube.', 'promotion of cross-pollination', 'The genetic mechanism prevents self-fertilisation, maintaining genetic diversity.'),
         ('honeybees and almond orchards in California', 'Almond growers rent about two million beehives each spring to pollinate the trees.', 'animal pollination', 'Almonds are self-incompatible and need insects to transfer pollen between trees, so yields depend on bees.')],
  evaluate=[('Declines in insect pollinators are a serious threat to food security.', ['about three-quarters of crop types benefit from animal pollination', 'fruit, nut and vegetable yields depend on pollinators'], ['staple cereals (wheat, rice, maize) are wind-pollinated', 'managed bees and hand pollination can partly compensate'], 'Pollinator decline threatens dietary diversity and some crop yields, though staple calorie supply is less affected; it remains a serious concern.')],
  extended=[('Describe the structure of an insect-pollinated flower and explain the processes of pollination, fertilisation and seed dispersal.', 'Sepals, petals, stamens (anther, filament), carpel (stigma, style, ovary, ovule); adaptations for insects; cross-pollination and self-incompatibility; pollen tube growth; double fertilisation; seed and fruit formation; dispersal by wind, animals, explosive mechanisms; germination.', 8),
            ('Explain the conditions needed for seed germination and the role of gibberellin.', 'Water (imbibition, enzymes, transport), oxygen (aerobic respiration), temperature (enzyme activity); dormancy; gibberellin; amylase; starch → maltose; radicle and plumule growth.', 6)],
  )


def _pollen_dq(rng, slot):
    conc = [0, 5, 10, 15, 20, 30]
    opt = pick(rng, [10, 15])
    pk = rng.uniform(9, 14)
    rate = [round(max(0.3, pk * math.exp(-((c - opt) / 10) ** 2) + rng.uniform(-0.4, 0.4)), 1) for c in conc]
    t = 40
    lens = [round(r * t) for r in rate]
    j = 2
    intro = (f'Pollen grains were placed in sucrose solutions of different concentrations. After {t} minutes, the mean length of pollen tubes was measured.\n\n'
             + table(['Sucrose / %', 'Mean tube length / µm', 'Growth rate / µm min⁻¹'], [(c, l, '?' if i == j else f'{l / t:.1f}') for i, (c, l) in enumerate(zip(conc, lens))]))
    best = conc[lens.index(max(lens))]
    parts = [
        (f'Calculate the growth rate in {conc[j]} % sucrose.', f'{lens[j] / t:.1f} µm min⁻¹', f'{lens[j]}/{t} = {lens[j] / t:.1f} (A1).', 1),
        ('Identify the sucrose concentration giving the greatest growth.', f'{best} %', f'{best} % (A1).', 1),
        ('Describe the effect of sucrose concentration on pollen tube growth.', f'Growth increases up to {best} %, then decreases at higher concentrations.', 'Increase to optimum (A1); decrease above (A1).', 2),
        ('Suggest why growth is reduced at high sucrose concentrations.', 'Low water potential of the solution causes water loss from pollen by osmosis, so tubes cannot elongate.', 'Water potential/osmosis (A1).', 1),
        ('Suggest why some sucrose is needed for growth.', 'Provides respiratory substrate for energy and maintains water potential to prevent bursting.', 'Energy/respiration (A1).', 1),
        ('Explain the role of the pollen tube in fertilisation.', 'It grows down the style to the ovule, carrying the male gametes to the egg and polar nuclei for double fertilisation.', 'Carries male gametes (A1); to ovule/micropyle (A1).', 2),
        ('State two variables that should be controlled.', 'Temperature; time; plant species/age of pollen; volume of solution; pH.', 'Two valid (A1 A1).', 2),
        ('Calculate the percentage difference in mean tube length between 0 % sucrose and the optimum concentration.', f'{signed(pct_change(lens[0], max(lens)))} %', f'({max(lens)} − {lens[0]})/{lens[0]} × 100 (M1) = {signed(pct_change(lens[0], max(lens)))} % (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch08-st2', _pollen_dq)


@R.add('ch08-st2', 'C3', (1, 4), 'numerical')
def germ_pct(rng, slot):
    n = pick(rng, [50, 80, 100, 120, 200, 250])
    a = rng.randint(int(n * 0.3), int(n * 0.95))
    cond = pick(rng, ['at 20 °C on moist paper', 'after soaking in gibberellin solution', 'at 5 °C', 'in waterlogged soil', 'after the seed coat was scratched'])
    p = 100 * a / n
    return num(f'Of {n} seeds placed {cond}, {a} germinated within 7 days. Calculate the germination percentage.', f'{p:.0f} %', f'{a}/{n} × 100 (M1) = {p:.0f} % (A1).', 2)


# ---- genetic crosses ----
def _cross(g1, g2):
    out = {}
    for a in g1:
        for b in g2:
            k = tuple(sorted((a, b)))
            out[k] = out.get(k, 0) + 1
    return out


ABO_PHEN = {('A', 'A'): 'A', ('A', 'O'): 'A', ('B', 'B'): 'B', ('B', 'O'): 'B', ('A', 'B'): 'AB', ('O', 'O'): 'O'}
ABO_SYM = {'A': 'Iᴬ', 'B': 'Iᴮ', 'O': 'i'}


def _abo_g(g):
    return ''.join(ABO_SYM[x] for x in g)


@R.add('ch08-st3', 'C3', (1, 5), 'numerical')
def abo_cross(rng, slot):
    gs = [('A', 'A'), ('A', 'O'), ('B', 'B'), ('B', 'O'), ('A', 'B'), ('O', 'O')]
    g1, g2 = pick(rng, gs), pick(rng, gs)
    off = _cross(g1, g2)
    ph = {}
    for k, v in off.items():
        p_ = ABO_PHEN[k]
        ph[p_] = ph.get(p_, 0) + v
    stem = f'A parent of genotype {_abo_g(g1)} has children with a parent of genotype {_abo_g(g2)}. Using a Punnett grid, deduce the possible blood groups of the children and their probabilities.'
    ans = '; '.join(f'group {k}: {Fraction(v, 4)}' for k, v in sorted(ph.items()))
    return num(stem, ans, f'Gametes {ABO_SYM[g1[0]]}/{ABO_SYM[g1[1]]} × {ABO_SYM[g2[0]]}/{ABO_SYM[g2[1]]} (A1); offspring genotypes ' +
               ', '.join(f'{_abo_g(k)} {Fraction(v, 4)}' for k, v in off.items()) + ' (A1); phenotypes and probabilities (A1). Iᴬ and Iᴮ codominant, i recessive.', 3, type='short')


@R.add('ch08-st3', 'C3', (1, 5), 'numerical')
def sexlink_cross(rng, slot):
    trait, a = pick(rng, [('haemophilia', 'h'), ('red–green colour blindness', 'b')])
    A = a.upper()
    mum = pick(rng, [(A, A), (A, a), (a, a)])
    dad = pick(rng, [A, a])
    sons = {}
    daus = {}
    for x in mum:
        sons[x] = sons.get(x, 0) + 1
        k = ''.join(sorted((x, dad)))
        daus[k] = daus.get(k, 0) + 1

    def xg(s):
        return ''.join(f'Xᴴ' if c == A and a == 'h' else 'Xʰ' if c == a and a == 'h' else 'Xᴮ' if c == A else 'Xᵇ' for c in s)
    son_aff = Fraction(sons.get(a, 0), 2)
    dau_aff = Fraction(daus.get(a + a, 0), 2)
    dau_car = Fraction(daus.get(A + a, 0), 2)
    all_aff = Fraction(sons.get(a, 0) + daus.get(a + a, 0), 4)
    stem = (f'{trait.capitalize()} is caused by a recessive allele on the X chromosome. A woman of genotype {xg("".join(mum))} has children with a man of genotype {xg(dad)}Y. '
            'Deduce the probability that (a) a son is affected, (b) a daughter is affected, (c) a daughter is a carrier, and (d) any child is affected.')
    return num(stem, f'(a) {son_aff}; (b) {dau_aff}; (c) {dau_car}; (d) {all_aff}',
               f'Gametes: mother {xg(mum[0])}, {xg(mum[1])}; father {xg(dad)}, Y (A1). Sons receive mother’s X: affected {son_aff} (A1); daughters: affected {dau_aff}, carrier {dau_car} (A1); any child {all_aff} (A1).', 4, type='short')


@R.add('ch08-st3', 'C3', (1, 4), 'mcq')
def mono_mcq(rng, slot):
    sp, dom, rec, A = pick(rng, [('pea plants', 'tall', 'dwarf', 'T'), ('mice', 'black fur', 'brown fur', 'B'), ('tomatoes', 'red fruit', 'yellow fruit', 'R'), ('fruit flies', 'normal wings', 'vestigial wings', 'V')])
    a = A.lower()
    g1, g2 = pick(rng, [((A, a), (A, a)), ((A, a), (a, a)), ((A, A), (a, a)), ((A, A), (A, a))])
    off = _cross(g1, g2)
    rc = off.get((a, a), 0)
    ratio = f'{4 - rc} {dom} : {rc} {rec}' if rc else f'all {dom}'
    wrong = [f'3 {dom} : 1 {rec}', f'1 {dom} : 1 {rec}', f'all {dom}', f'1 {dom} : 3 {rec}', f'all {rec}']
    if ratio == '2 ' + dom + ' : 2 ' + rec:
        ratio = f'1 {dom} : 1 {rec}'
    stem = f'In {sp}, {dom} ({A}) is dominant to {rec} ({a}). What is the expected phenotypic ratio from a cross {"".join(g1)} × {"".join(g2)}?'
    return nmcq(rng, stem, ratio, wrong, f'Offspring genotypes: ' + ', '.join(f'{"".join(sorted(k, key=lambda c: (c.islower(), c)))} {v}/4' for k, v in off.items()) + f' → {ratio}.')


S('ch08-st3',
  terms=[('allele', 'one of the alternative forms of a gene, found at the same locus'),
         ('genotype', 'the alleles of a gene possessed by an individual'),
         ('phenotype', 'the observable characteristics of an individual, resulting from genotype and environment'),
         ('codominance', 'a pattern in which both alleles in a heterozygote are fully expressed in the phenotype, as in AB blood group or roan cattle'),
         ('multiple alleles', 'three or more alleles of a gene in a population, such as Iᴬ, Iᴮ and i for ABO blood groups'),
         ('sex linkage', 'the location of a gene on a sex chromosome (usually X), so that inheritance patterns differ between males and females'),
         ('carrier', 'a heterozygous individual who carries a recessive allele but does not show the phenotype'),
         ('test cross', 'a cross between an individual of dominant phenotype and a homozygous recessive individual to determine whether the first is homozygous or heterozygous')],
  facts=[('What are the possible genotypes of a person with blood group A?', 'IᴬIᴬ or Iᴬi', ['IᴬIᴮ only', 'ii', 'IᴮIᴮ'], 'Iᴬ is dominant to i.'),
         ('Which disorder is sex-linked?', 'haemophilia', ['cystic fibrosis', 'sickle-cell anaemia', 'Huntington’s disease'], 'Allele on the X chromosome.'),
         ('Why are males more often affected by X-linked recessive conditions?', 'they have only one X chromosome, so one recessive allele causes the condition', ['they have two X chromosomes', 'the Y chromosome carries the allele', 'they are always homozygous dominant'], 'Hemizygous.'),
         ('Which cross gives a 3 : 1 phenotypic ratio?', 'Aa × Aa', ['AA × aa', 'Aa × aa', 'AA × AA'], 'Monohybrid heterozygous cross.'),
         ('Which is an example of codominance?', 'roan coat colour in cattle (red and white hairs)', ['tall and dwarf pea plants', 'albinism', 'cystic fibrosis'], 'Both alleles expressed.')],
  mc2=[('Why can two parents with blood group A have a child with blood group O?', 'Both parents may be heterozygous (Iᴬi) and the child inherits i from each.', ['Blood group changes after birth.', 'Iᴬ is recessive.', 'Group O is codominant.'], 'Recessive allele hidden.'),
       ('Why can an affected father not pass an X-linked condition to his sons?', 'Sons receive the father’s Y chromosome, not his X.', ['The allele is on the Y.', 'Sons are always carriers.', 'Fathers cannot be affected.'], 'Y from father.'),
       ('Why is a test cross used with a homozygous recessive parent?', 'The recessive parent contributes only recessive alleles, so offspring phenotypes reveal the other parent’s alleles.', ['It always gives a 3 : 1 ratio.', 'It changes the genotype.', 'It prevents mutation.'], 'Reveals genotype.'),
       ('Why is the observed ratio of offspring often different from the expected ratio?', 'Fertilisation is random, so in small samples chance causes deviations.', ['Mendel’s laws are wrong.', 'Alleles blend.', 'Dominant alleles mutate.'], 'Probability.')],
  mc3=[('A carrier woman for haemophilia (XᴴXʰ) and an unaffected man (XᴴY) have a son. What is the probability that he is affected?', '1/2', ['1/4', '0', '1'], 'Son receives Xʰ with probability 1/2.'),
       ('A roan bull (CᴿCᵂ) is crossed with a white cow (CᵂCᵂ). What proportion of calves are expected to be roan?', '1/2', ['1/4', '3/4', 'all'], 'CᴿCᵂ × CᵂCᵂ → 1 CᴿCᵂ : 1 CᵂCᵂ.'),
       ('Parents with blood groups AB and O have children. Which blood groups are possible?', 'A and B only', ['A, B, AB and O', 'AB and O only', 'O only'], 'Iᴬi or Iᴮi.')],
  why=[('Explain how blood groups are inherited in humans.', 'The ABO gene has multiple alleles Iᴬ, Iᴮ and i; Iᴬ and Iᴮ are codominant and both dominant to i; genotypes IᴬIᴬ/Iᴬi = A, IᴮIᴮ/Iᴮi = B, IᴬIᴮ = AB, ii = O; each parent passes one allele; Punnett grids predict probabilities.'),
       ('Explain the pattern of inheritance of red–green colour blindness.', 'The gene is on the X chromosome (no locus on Y); the allele for colour blindness is recessive; males (XY) with one recessive allele are affected; females need two copies, so are usually carriers; affected males inherit the allele from their mothers; affected fathers pass it to all daughters.'),
       ('Explain how a test cross can be used to find an unknown genotype.', 'Cross the dominant-phenotype individual with a homozygous recessive; if all offspring show the dominant phenotype the individual is probably homozygous; if about half show the recessive phenotype it is heterozygous; large numbers of offspring are needed.')],
  contrast=[('dominant alleles', 'recessive alleles', 'A dominant allele is expressed in the phenotype of a heterozygote; a recessive allele is expressed only when homozygous.'),
            ('codominance', 'complete dominance', 'In codominance both alleles are expressed in a heterozygote (e.g. IᴬIᴮ); in complete dominance only the dominant allele affects the phenotype.')],
  misc=[('Dominant alleles are always more common in the population.', 'Dominance refers to expression in heterozygotes, not frequency; some dominant alleles are rare (e.g. Huntington’s).'),
        ('If two parents have a 1 in 4 chance of an affected child, their fourth child will be affected if the first three were not.', 'Each fertilisation is independent; the probability is 1/4 for every child.'),
        ('Sex-linked conditions only affect males.', 'Females can be affected if homozygous recessive, though this is rarer.')],
  cases=[('haemophilia in Queen Victoria’s descendants', 'Queen Victoria was a carrier; several sons and grandsons in European royal families had haemophilia.', 'sex-linked inheritance', 'Carrier daughters passed the X-linked recessive allele to sons, who were affected.'),
         ('roan cattle', 'Crossing red and white Shorthorn cattle produces roan calves with both red and white hairs.', 'codominance', 'Both alleles are expressed in the heterozygote, so both pigments appear.')],
  evaluate=[('Mendel’s laws explain the inheritance of all characteristics.', ['monohybrid ratios for many single-gene traits match Mendel’s predictions'], ['codominance, multiple alleles, sex linkage, linkage and polygenic traits do not fit simple ratios', 'environment also affects phenotypes'], 'Mendel’s principles underlie inheritance, but many traits need extensions such as codominance, linkage and polygenic inheritance.')],
  extended=[('Explain, using examples, codominance, multiple alleles and sex linkage, and show how Punnett grids are used to predict outcomes of crosses.', 'Definitions; ABO blood groups with genotypes; roan cattle; sex linkage: haemophilia, colour blindness, X and Y; carriers; Punnett grid method; worked examples; probabilities; pedigree analysis.', 8),
            ('Describe how pedigree charts are used to deduce patterns of inheritance.', 'Symbols; dominant vs recessive (unaffected parents with affected child → recessive); autosomal vs X-linked (male bias, no father-to-son transmission); deducing genotypes and carriers; probability calculations.', 6)],
  )


S('ch08-st4',
  terms=[('dihybrid cross', 'a cross involving two genes, each with two alleles'),
         ('linked genes', 'genes located close together on the same chromosome, which tend to be inherited together'),
         ('recombinant', 'an offspring with a combination of alleles different from either parent, produced by crossing over or independent assortment'),
         ('recombination frequency', 'the percentage of recombinant offspring from a test cross; a measure of the distance between linked genes'),
         ('chi-squared test', 'a statistical test comparing observed and expected frequencies to determine whether differences are significant'),
         ('degrees of freedom', 'for a chi-squared goodness-of-fit test, the number of categories minus one'),
         ('null hypothesis', 'the hypothesis that there is no significant difference between observed and expected results')],
  facts=[('What is the expected phenotypic ratio from a dihybrid cross between two double heterozygotes (unlinked genes)?', '9 : 3 : 3 : 1', ['3 : 1', '1 : 1 : 1 : 1', '1 : 2 : 1'], 'Independent assortment.'),
         ('What ratio results from a test cross of a double heterozygote with unlinked genes?', '1 : 1 : 1 : 1', ['9 : 3 : 3 : 1', '3 : 1', '1 : 2 : 1'], 'Four gamete types in equal proportion.'),
         ('How many degrees of freedom are used for a chi-squared test on a 9 : 3 : 3 : 1 ratio?', '3', ['4', '1', '9'], 'Four categories minus one.'),
         ('What is the critical value of χ² for 3 degrees of freedom at p = 0.05?', '7.81', ['3.84', '5.99', '9.49'], 'From the table.'),
         ('Which scientist first showed gene linkage in fruit flies?', 'Thomas Hunt Morgan', ['Gregor Mendel', 'Charles Darwin', 'Rosalind Franklin'], 'Drosophila experiments.')],
  mc2=[('Why do linked genes not give a 9 : 3 : 3 : 1 ratio?', 'They are on the same chromosome and do not assort independently, so parental combinations are more common.', ['They are on different chromosomes.', 'They always cross over.', 'They are sex-linked only.'], 'Linkage.'),
       ('Why does recombination frequency indicate the distance between genes?', 'Crossing over is more likely to occur between genes that are further apart.', ['Close genes always recombine.', 'Recombination is independent of position.', 'Genes far apart are never separated.'], 'Gene mapping.'),
       ('Why is a chi-squared test used for genetic crosses?', 'To determine whether the difference between observed and expected ratios is due to chance.', ['To calculate the mean.', 'To find genotypes directly.', 'To prove Mendel wrong.'], 'Significance.'),
       ('Why are recombinants produced even for linked genes?', 'Crossing over between non-sister chromatids in prophase I exchanges alleles.', ['Linked genes assort independently.', 'Mutation always occurs.', 'Fertilisation separates them.'], 'Crossing over.')],
  mc3=[('A test cross gives 412 parental-type and 88 recombinant offspring. What is the recombination frequency?', '17.6 %', ['21.4 %', '82.4 %', '8.8 %'], '88/500 × 100.'),
       ('A chi-squared value of 2.4 was calculated with 3 degrees of freedom (critical value 7.81). What is concluded?', 'The results fit the expected ratio; differences are due to chance.', ['The genes are linked.', 'The results differ significantly.', 'The test is invalid.'], 'χ² < critical value.'),
       ('In a dihybrid cross AaBb × AaBb, what proportion of offspring are expected to be aabb?', '1/16', ['1/4', '9/16', '3/16'], '1/4 × 1/4.')],
  why=[('Explain the 9 : 3 : 3 : 1 ratio in a dihybrid cross.', 'Each double heterozygote parent (AaBb) produces four gamete types AB, Ab, aB, ab in equal proportions because of independent assortment of homologous pairs in metaphase I; random fertilisation gives 16 combinations; 9 A_B_, 3 A_bb, 3 aaB_, 1 aabb.'),
       ('Explain how a chi-squared test is carried out on the results of a genetic cross.', 'State null hypothesis (no significant difference from expected ratio); calculate expected numbers from total × ratio; χ² = Σ(O − E)²/E; degrees of freedom = categories − 1; compare with critical value at p = 0.05; if χ² is greater, reject the null hypothesis.'),
       ('Explain how linkage affects the outcome of a test cross.', 'Linked genes are on the same chromosome so parental allele combinations are usually inherited together; offspring are mostly parental types; recombinants arise only by crossing over in prophase I; recombinant frequency is less than 50 %; ratio deviates from 1 : 1 : 1 : 1.')],
  contrast=[('unlinked genes', 'linked genes', 'Unlinked genes are on different chromosomes and assort independently, giving 1 : 1 : 1 : 1 in a test cross; linked genes are on the same chromosome, so parental types predominate and recombinants are fewer than 50 %.'),
            ('parental phenotypes', 'recombinant phenotypes', 'Parental phenotypes show the allele combinations present in the parents; recombinant phenotypes show new combinations resulting from crossing over or independent assortment.')],
  misc=[('A significant χ² result proves the hypothesis is wrong.', 'It shows the difference is unlikely to be due to chance at the chosen probability level; it is evidence, not proof.'),
        ('Linked genes are always inherited together.', 'Crossing over can separate them, producing recombinants.'),
        ('A 9 : 3 : 3 : 1 ratio means exactly 9 of every 16 offspring will show both dominant traits.', 'It is a probability; actual numbers vary by chance, which is why a chi-squared test is used.')],
  cases=[('Morgan’s fruit fly experiments', 'Crosses of grey-bodied, normal-winged flies with black-bodied, vestigial-winged flies produced far more parental types than expected for independent assortment.', 'gene linkage', 'The genes are on the same chromosome, and recombinants arise only by crossing over.'),
         ('Mendel’s dihybrid crosses with peas', 'Crossing round yellow with wrinkled green peas gave F2 of 315 round yellow, 108 round green, 101 wrinkled yellow and 32 wrinkled green.', 'independent assortment', 'The ratio close to 9 : 3 : 3 : 1 showed that the two genes assort independently.')],
  evaluate=[('The chi-squared test can show whether two genes are linked.', ['a significant deviation from 1 : 1 : 1 : 1 or 9 : 3 : 3 : 1 suggests linkage', 'excess of parental types indicates linkage'], ['other causes such as reduced viability of some genotypes can also cause deviations', 'small samples have low power'], 'Chi-squared can provide evidence for linkage when combined with the pattern of an excess of parental types, but other explanations must be considered.')],
  extended=[('Explain how the results of dihybrid crosses can be used to determine whether two genes are linked, including the use of the chi-squared test.', 'Independent assortment; 9 : 3 : 3 : 1 and 1 : 1 : 1 : 1; linkage; crossing over; recombinants; recombination frequency; chi-squared: null hypothesis, expected values, formula, df, critical value, conclusion; Morgan’s experiment.', 8),
            ('Explain how independent assortment and crossing over lead to new combinations of alleles.', 'Random orientation of bivalents at metaphase I; 2ⁿ combinations; crossing over at chiasmata between non-sister chromatids; exchange of alleles of linked genes; recombinants; contribution to variation.', 6)],
  )


DIHYB = [('pea plants', ['round yellow', 'round green', 'wrinkled yellow', 'wrinkled green']),
         ('maize', ['purple smooth', 'purple shrunken', 'yellow smooth', 'yellow shrunken']),
         ('tomato plants', ['tall cut-leaf', 'tall potato-leaf', 'dwarf cut-leaf', 'dwarf potato-leaf']),
         ('fruit flies', ['grey normal-winged', 'grey vestigial-winged', 'black normal-winged', 'black vestigial-winged'])]


def _dihyb_counts(rng, ratio):
    n = rng.randint(300, 900)
    tot = sum(ratio)
    obs = [max(1, round(n * r / tot * rng.uniform(0.85, 1.15))) for r in ratio]
    return obs


@R.add('ch08-st4', 'C3', (2, 5), 'numerical')
def dihybrid_chi(rng, slot):
    sp, ph = pick(rng, DIHYB)
    test = rng.random() < 0.4
    ratio = [1, 1, 1, 1] if test else [9, 3, 3, 1]
    obs = _dihyb_counts(rng, ratio)
    e, chi = chi_gof(obs, ratio)
    sig = chi > CHI_CRIT[3]
    cross = 'a test cross of a double heterozygote with a double recessive' if test else 'a cross between two double heterozygotes'
    stem = (f'In {sp}, {cross} produced: ' + ', '.join(f'{o} {p}' for o, p in zip(obs, ph)) +
            f'. Calculate χ² for the expected {" : ".join(map(str, ratio))} ratio and state a conclusion (critical value 7.81, 3 df, p = 0.05).')
    return num(stem, f'χ² = {chi:.2f}; ' + ('significant difference – reject H₀ (genes may be linked or genotypes differ in viability)' if sig else 'not significant – results fit the expected ratio; accept H₀'),
               f'Expected: {", ".join(f"{x:.1f}" for x in e)} (M1); Σ(O − E)²/E (M1) = {chi:.2f} (A1); comparison with 7.81 and conclusion (A1).', 4)


@R.add('ch08-st4', 'C3', (1, 5), 'numerical')
def recomb_freq(rng, slot):
    n = rng.randint(400, 1200)
    rf = rng.uniform(0.05, 0.35)
    rec = round(n * rf)
    par = n - rec
    p1, p2 = round(par * rng.uniform(0.47, 0.53)), None
    p2 = par - p1
    r1 = round(rec * rng.uniform(0.45, 0.55))
    r2 = rec - r1
    f = 100 * rec / n
    stem = (f'In Drosophila, a female heterozygous for body colour and wing length (GgNn, with G and N on the same chromosome) was test-crossed with a ggnn male. Offspring: {p1} grey normal, {p2} black vestigial, '
            f'{r1} grey vestigial and {r2} black normal. Calculate the recombination frequency.')
    if slot.d >= 4:
        stem += ' Explain how the recombinants were produced.'
        return num(stem, f'{f:.1f} %; by crossing over between non-sister chromatids in prophase I of meiosis in the female',
                   f'Recombinants = {r1} + {r2} = {rec} (M1); {rec}/{n} × 100 = {f:.1f} % (A1); crossing over at chiasmata between the loci (R1).', 3)
    return num(stem, f'{f:.1f} %', f'Recombinants = {r1} + {r2} = {rec} (M1); {rec}/{n} × 100 = {f:.1f} % (A1).', 2)


def _dihyb_dq(rng, slot):
    sp, ph = pick(rng, DIHYB)
    ratio = [9, 3, 3, 1]
    obs = _dihyb_counts(rng, ratio)
    if rng.random() < 0.4:
        obs[1] = round(obs[1] * 0.7)
        obs[2] = round(obs[2] * 0.7)
        obs[0] = round(obs[0] * 1.15)
    e, chi = chi_gof(obs, ratio)
    sig = chi > CHI_CRIT[3]
    n = sum(obs)
    intro = (f'Two {sp} heterozygous for two genes were crossed. The phenotypes of the offspring are shown.\n\n'
             + table(['Phenotype', 'Observed', 'Expected (9 : 3 : 3 : 1)', '(O − E)²/E'], [(p, o, f'{x:.1f}' if i else '?', f'{(o - x) ** 2 / x:.2f}' if i else '?') for i, (p, o, x) in enumerate(zip(ph, obs, e))]))
    parts = [
        ('State the total number of offspring.', f'{n}', f'{n} (A1).', 1),
        (f'Calculate the expected number of {ph[0]} offspring.', f'{e[0]:.1f}', f'9/16 × {n} = {e[0]:.1f} (A1).', 1),
        ('Calculate the value of χ².', f'{chi:.2f}', f'({obs[0]} − {e[0]:.1f})²/{e[0]:.1f} = {(obs[0] - e[0]) ** 2 / e[0]:.2f} (M1); sum = {chi:.2f} (A1).', 2),
        ('State the null hypothesis and the number of degrees of freedom.', 'There is no significant difference between observed and expected (9 : 3 : 3 : 1) numbers; 3 degrees of freedom.', 'H₀ (A1); df = 3 (A1).', 2),
        ('Using a critical value of 7.81, state a conclusion.', ('χ² > 7.81: reject H₀ – the results differ significantly from 9 : 3 : 3 : 1' if sig else 'χ² < 7.81: accept H₀ – differences are due to chance; genes assort independently'),
         'Comparison (A1); conclusion (A1).', 2),
        ('Suggest an explanation if the results differed significantly from 9 : 3 : 3 : 1.', 'The genes may be linked on the same chromosome, so parental combinations are more frequent; or some genotypes have lower viability.', 'Linkage (A1); explanation (A1).', 2),
        ('Explain why a 9 : 3 : 3 : 1 ratio is expected for unlinked genes.', 'Independent assortment gives four gamete types in equal proportions from each parent; 16 equally likely combinations.', 'Independent assortment (A1); 16 combinations (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch08-st4', _dihyb_dq)


S('ch08-st5',
  terms=[('continuous variation', 'variation in which a characteristic shows a range of values with no distinct categories, such as height or mass'),
         ('discontinuous variation', 'variation in which individuals fall into distinct categories, such as blood groups'),
         ('polygenic inheritance', 'inheritance of a characteristic controlled by many genes, each with a small additive effect'),
         ('additive alleles', 'alleles that each contribute a small, equal amount to the phenotype'),
         ('normal distribution', 'a symmetrical bell-shaped frequency distribution in which most values cluster around the mean'),
         ('standard deviation', 'a measure of the spread of data around the mean')],
  facts=[('Which human characteristic is an example of polygenic inheritance?', 'skin colour', ['ABO blood group', 'cystic fibrosis', 'haemophilia'], 'Many genes involved.'),
         ('What shape of frequency distribution is typical of continuous variation?', 'a normal (bell-shaped) distribution', ['two separate bars', 'a straight line', 'a U-shape'], 'Most near the mean.'),
         ('Approximately what percentage of values lie within one standard deviation of the mean in a normal distribution?', '68 %', ['95 %', '50 %', '99 %'], '±1 SD.'),
         ('Which factor besides genes affects human height?', 'nutrition', ['blood group', 'eye colour', 'number of chromosomes'], 'Environment.'),
         ('How many phenotype classes are possible for a trait controlled by 3 genes with additive alleles?', '7', ['3', '6', '8'], '2n + 1.')],
  mc2=[('Why does polygenic inheritance produce continuous variation?', 'Many genes each add a small effect, giving many intermediate phenotypes.', ['One gene has two alleles.', 'Alleles are always codominant.', 'The environment has no effect.'], 'Additive effects.'),
       ('Why do environmental factors make variation even more continuous?', 'They modify phenotypes within each genotype class, blurring the boundaries between classes.', ['They change the alleles.', 'They create new genes.', 'They remove variation.'], 'Genotype × environment.'),
       ('Why are extreme phenotypes rare in polygenic traits?', 'They require inheriting all (or no) contributing alleles, which is unlikely.', ['Extreme phenotypes are lethal.', 'Alleles are recessive.', 'Mutations prevent them.'], 'Low probability.'),
       ('Why is height in a population better described by mean and standard deviation than by categories?', 'It varies continuously, so there are no distinct categories.', ['Height has only two values.', 'Height is not inherited.', 'Categories give more information.'], 'Continuous data.')],
  mc3=[('A trait is controlled by two genes with additive alleles (A/a and B/b). What proportion of offspring of AaBb × AaBb have all four contributing alleles?', '1/16', ['1/4', '1/8', '6/16'], '1/4 × 1/4.'),
       ('The mean height of a sample is 170 cm with SD 7 cm. About 95 % of the sample lies between which values?', '156 and 184 cm', ['163 and 177 cm', '149 and 191 cm', '170 and 184 cm'], '± 2 SD.'),
       ('In AaBb × AaBb with additive alleles, which number of contributing alleles is most common?', '2', ['0', '4', '1'], 'Middle class (6/16).')],
  why=[('Explain how polygenic inheritance gives rise to a normal distribution.', 'Many genes (each with additive alleles) contribute to the trait; offspring inherit varying numbers of contributing alleles; intermediate numbers are most likely by probability, extremes least likely; with environmental effects the classes merge into a continuous bell-shaped distribution.'),
       ('Explain why skin colour in humans shows continuous variation.', 'Skin colour is controlled by many genes affecting melanin production, each allele adding a small amount; environment (UV exposure, tanning) also modifies colour; the combination produces a continuous range.'),
       ('Explain the use of mean and standard deviation in describing continuous variation.', 'The mean shows the central value; the standard deviation shows the spread; about 68 % of values lie within ±1 SD and 95 % within ±2 SD in a normal distribution; comparing means and SDs allows populations to be compared.')],
  contrast=[('continuous variation', 'discontinuous variation', 'Continuous variation shows a range of values (e.g. height) and is usually polygenic and affected by environment; discontinuous variation shows distinct categories (e.g. blood groups) and is usually controlled by one or a few genes.'),
            ('monogenic traits', 'polygenic traits', 'Monogenic traits are controlled by one gene, giving distinct phenotypes; polygenic traits are controlled by many genes with additive effects, giving continuous variation.')],
  misc=[('Continuous variation is caused only by the environment.', 'It is usually caused by many genes as well as environmental factors.'),
        ('A trait controlled by several genes cannot be inherited in a predictable way.', 'Each gene is inherited according to Mendel’s laws; probabilities of phenotype classes can be calculated.'),
        ('A larger standard deviation means a larger mean.', 'SD measures spread, not the size of the mean.')],
  cases=[('wheat kernel colour studied by Nilsson-Ehle', 'Crosses of red and white wheat gave F2 with a range of shades in a 1 : 4 : 6 : 4 : 1 ratio.', 'polygenic inheritance', 'Two genes with additive alleles gave five classes, explaining continuous variation by Mendelian genes.'),
         ('human height', 'Height is influenced by hundreds of genetic variants and by nutrition; average height increased in many countries during the 20th century.', 'genes and environment in continuous variation', 'Many genes give a normal distribution, while improved nutrition shifted the mean.')],
  evaluate=[('Human height is determined mainly by genes.', ['heritability estimates of about 80 % in well-nourished populations', 'hundreds of genetic variants identified'], ['average height has risen with nutrition, showing strong environmental effects', 'heritability depends on the population and environment'], 'Genes explain most variation within well-nourished populations, but environment, especially nutrition, strongly affects height across populations and generations.')],
  extended=[('Explain the genetic basis of continuous variation and how it can be analysed statistically.', 'Polygenic inheritance; additive alleles; number of classes 2n + 1; probability of extremes; environmental effects; normal distribution; mean, SD, 68 % and 95 %; examples skin colour, height, wheat colour; comparison with discontinuous variation.', 8),
            ('Compare continuous and discontinuous variation, using examples.', 'Continuous: range, polygenic, environment, height, mass, skin colour, histogram/normal distribution; discontinuous: categories, monogenic, blood group, bar chart; both inherited.', 6)],
  )


@R.add('ch08-st5', 'C3', (1, 5), 'numerical')
def polygenic_calc(rng, slot):
    n = pick(rng, [2, 3, 4])
    cls = 2 * n + 1
    k = rng.randint(0, 2 * n)
    p = Fraction(math.comb(2 * n, k), 4 ** n)
    stem = (f'A trait is controlled by {n} unlinked genes, each with one contributing (additive) allele and one non-contributing allele. '
            f'For a cross between two individuals heterozygous at all {n} genes, calculate (a) the number of phenotype classes and (b) the probability that an offspring has exactly {k} contributing alleles.')
    return num(stem, f'(a) {cls}; (b) {p} ({float(p):.3f})', f'(a) 2n + 1 = {cls} (A1); (b) {2 * n} alleles each with p = 1/2: C({2 * n},{k})/2^{2 * n} (M1) = {math.comb(2 * n, k)}/{4 ** n} = {p} (A1).', 3)


mean_sd_items(R, 'ch08-st5', [
    ('measured the heights of a sample of students.', 'height', 'cm', 155, 180, 0.04, 0),
    ('measured the lengths of a sample of ivy leaves.', 'leaf length', 'mm', 45, 85, 0.12, 0),
    ('weighed a sample of runner bean seeds.', 'seed mass', 'g', 0.8, 1.6, 0.1, 2),
    ('counted the number of spots on the elytra of a sample of ladybirds.', 'spot number', 'spots', 6, 12, 0.15, 0),
])


def _height_dq(rng, slot):
    bins = [150, 155, 160, 165, 170, 175, 180, 185]
    mu = rng.uniform(164, 172)
    s = rng.uniform(5.5, 8)
    N = rng.randint(180, 300)
    freqs = []
    for b in bins:
        lo, hi = b, b + 5
        cdf = lambda x: 0.5 * (1 + math.erf((x - mu) / (s * math.sqrt(2))))
        freqs.append(round(N * (cdf(hi) - cdf(lo))))
    n = sum(freqs)
    mids = [b + 2.5 for b in bins]
    m = sum(f * x for f, x in zip(freqs, mids)) / n
    sd_ = math.sqrt(sum(f * (x - m) ** 2 for f, x in zip(freqs, mids)) / (n - 1))
    modal = bins[freqs.index(max(freqs))]
    intro = ('The heights of a sample of 17-year-old students were recorded.\n\n' + table(['Height / cm', 'Frequency'], [(f'{b}–{b + 4.9:.1f}', f) for b, f in zip(bins, freqs)]))
    parts = [
        ('State the modal class.', f'{modal}–{modal + 4.9:.1f} cm', 'Modal class (A1).', 1),
        ('Estimate the mean height using the class midpoints.', f'{m:.1f} cm', f'Σfx/Σf = {sum(f * x for f, x in zip(freqs, mids)):.1f}/{n} (M1) = {m:.1f} cm (A1).', 2),
        (f'The standard deviation is {sd_:.1f} cm. Calculate the range within which about 95 % of students lie.', f'{m - 2 * sd_:.1f} to {m + 2 * sd_:.1f} cm', f'mean ± 2 SD = {m:.1f} ± {2 * sd_:.1f} (A1).', 1),
        ('Explain why height shows this pattern of variation.', 'It is a polygenic trait with many genes each having small additive effects, plus environmental effects such as nutrition, giving a continuous, normal distribution.', 'Polygenic/additive (A1); environment (A1); normal distribution (A1).', 3),
        ('Suggest two environmental factors that influence height.', 'Nutrition (protein, calcium, vitamin D), disease in childhood, sleep, exercise.', 'Two factors (A1 A1).', 2),
        ('Suggest why the sample should include similar numbers of males and females, or analyse them separately.', 'Males are on average taller, so a mixed sample could be bimodal or biased.', 'Sex difference (A1).', 1),
        ('Explain why a histogram rather than a bar chart is used to display these data.', 'Height is continuous data grouped into classes, so the bars touch with no gaps between them.', 'Continuous data (A1); classes/touching bars (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch08-st5', _height_dq)


# =============================================================================================
# ch09 D3.3 Homeostasis
# =============================================================================================
S('ch09-st1',
  terms=[('homeostasis', 'the maintenance of a constant internal environment within narrow limits despite external changes'),
         ('negative feedback', 'a control mechanism in which a change from the set point triggers responses that reverse the change'),
         ('set point', 'the normal or target value of a variable that homeostatic mechanisms maintain'),
         ('insulin', 'a hormone secreted by β cells of the pancreatic islets when blood glucose is high, which stimulates glucose uptake and glycogen synthesis'),
         ('glucagon', 'a hormone secreted by α cells of the pancreatic islets when blood glucose is low, which stimulates glycogen breakdown in the liver'),
         ('glycogenesis', 'the synthesis of glycogen from glucose, mainly in liver and muscle cells'),
         ('type 1 diabetes', 'a condition in which β cells are destroyed by the immune system so little or no insulin is produced'),
         ('type 2 diabetes', 'a condition in which target cells become resistant to insulin, often linked to obesity and inactivity')],
  facts=[('Which cells secrete insulin?', 'β cells of the islets of Langerhans', ['α cells of the islets', 'hepatocytes', 'acinar cells'], 'In the pancreas.'),
         ('What is the approximate normal fasting blood glucose concentration?', 'about 5 mmol dm⁻³', ['about 50 mmol dm⁻³', 'about 0.5 mmol dm⁻³', 'about 15 mmol dm⁻³'], 'Range about 4–6.'),
         ('Which organ stores glycogen and releases glucose into the blood?', 'the liver', ['the pancreas', 'the kidney', 'the stomach'], 'Under hormonal control.'),
         ('Which type of diabetes is treated mainly with insulin injections?', 'type 1', ['type 2 only', 'neither type', 'gestational only'], 'No insulin produced.'),
         ('Which hormone raises blood glucose?', 'glucagon', ['insulin', 'ADH', 'oxytocin'], 'Stimulates glycogenolysis.')],
  mc2=[('Why is control of blood glucose an example of negative feedback?', 'A rise or fall in glucose triggers hormone secretion that returns glucose to the set point.', ['A rise triggers further rises.', 'Glucose is not controlled.', 'Insulin and glucagon act in the same direction.'], 'Reversal of change.'),
       ('Why can type 2 diabetes often be controlled by diet and exercise?', 'Reducing sugar intake and weight and increasing activity improve insulin sensitivity and reduce glucose peaks.', ['Exercise produces insulin.', 'Diet destroys β cells.', 'Type 2 has no insulin at all.'], 'Lifestyle.'),
       ('Why does blood glucose rise after a meal?', 'Carbohydrates are digested to glucose, which is absorbed into the blood from the small intestine.', ['The liver stops storing glucose.', 'Glucagon is secreted.', 'Insulin rises first.'], 'Absorption.'),
       ('Why do muscle cells take up more glucose when insulin binds to them?', 'Insulin triggers insertion of GLUT4 transporters into the membrane.', ['Insulin carries glucose in.', 'Insulin opens sodium channels.', 'Insulin destroys glycogen.'], 'Facilitated diffusion.')],
  mc3=[('A person’s blood glucose stays above 11 mmol dm⁻³ two hours after drinking 75 g glucose. What does this suggest?', 'diabetes – impaired glucose regulation', ['normal glucose tolerance', 'excess glucagon only', 'hypoglycaemia'], 'Glucose tolerance test.'),
       ('Blood glucose fell from 7.8 to 5.2 mmol dm⁻³ in 60 minutes. What was the mean rate of decrease?', '0.043 mmol dm⁻³ min⁻¹', ['2.6 mmol dm⁻³ min⁻¹', '0.13 mmol dm⁻³ min⁻¹', '0.43 mmol dm⁻³ min⁻¹'], '2.6/60.'),
       ('An athlete runs a long race and blood glucose begins to fall. Which response is expected?', 'Glucagon secretion increases and the liver breaks down glycogen.', ['Insulin secretion increases.', 'The liver stores more glycogen.', 'Glucagon falls.'], 'Restore glucose.')],
  why=[('Explain how blood glucose concentration is controlled.', 'Glucose is monitored by cells of the pancreatic islets; when high, β cells secrete insulin, which causes uptake of glucose by liver, muscle and fat cells (GLUT4) and conversion to glycogen (glycogenesis); when low, α cells secrete glucagon, which stimulates glycogen breakdown (glycogenolysis) in the liver, releasing glucose; negative feedback returns glucose to the set point.'),
       ('Explain the causes and treatment of type 1 and type 2 diabetes.', 'Type 1: autoimmune destruction of β cells, little insulin; treated by insulin injections/pumps and monitoring; type 2: insulin resistance of target cells, linked to obesity, inactivity, genetics; treated by diet, exercise, weight loss and drugs such as metformin, later insulin.'),
       ('Explain why negative feedback is important in homeostasis.', 'It detects deviations from the set point by receptors and triggers effectors to reverse them; keeps variables within narrow limits for optimal enzyme activity and cell function; the response stops once the set point is restored.')],
  contrast=[('insulin', 'glucagon', 'Insulin is secreted by β cells when glucose is high and lowers blood glucose by increasing uptake and glycogen synthesis; glucagon is secreted by α cells when glucose is low and raises blood glucose by stimulating glycogen breakdown.'),
            ('type 1 diabetes', 'type 2 diabetes', 'Type 1 diabetes is caused by autoimmune destruction of β cells so insulin is not produced, usually starting in childhood; type 2 diabetes is caused by insulin resistance, is linked to lifestyle and usually develops in adults.')],
  misc=[('Insulin turns glucose into glycogen directly.', 'Insulin is a hormone that signals cells to take up glucose and activates enzymes that synthesise glycogen.'),
        ('Glucagon and glycogen are the same thing.', 'Glucagon is a hormone; glycogen is a storage polysaccharide.'),
        ('People with type 2 diabetes produce no insulin.', 'They usually produce insulin but their cells respond poorly to it.'),
        ('Negative feedback means the response is harmful.', 'Negative feedback means the response reverses the change, restoring the set point.')],
  cases=[('the discovery of insulin by Banting and Best (1921)', 'Extracts of dog pancreas lowered blood glucose in diabetic dogs; in 1922 insulin saved the life of Leonard Thompson.', 'hormonal control of blood glucose', 'Insulin from β cells is required to lower blood glucose, so replacing it treats type 1 diabetes.'),
         ('the rise in type 2 diabetes worldwide', 'Over 500 million adults have diabetes, most with type 2, linked to obesity and sedentary lifestyles.', 'insulin resistance', 'Excess fat and inactivity reduce the response of target cells to insulin, so blood glucose remains high.')],
  evaluate=[('Type 2 diabetes is caused entirely by lifestyle choices.', ['obesity, high-sugar diets and inactivity strongly increase risk', 'lifestyle change can reverse early type 2 diabetes'], ['genetic factors and ethnicity affect risk', 'socio-economic factors limit access to healthy food and exercise'], 'Lifestyle is a major factor, but genetic and social factors also contribute, so it is not entirely a matter of individual choice.')],
  extended=[('Explain how blood glucose concentration is regulated by negative feedback, and the causes and treatment of diabetes.', 'Set point ~5 mmol dm⁻³; islets of Langerhans α and β cells; insulin: GLUT4, glycogenesis, respiration, fat storage; glucagon: glycogenolysis, gluconeogenesis; negative feedback; type 1 autoimmune; type 2 resistance; treatments; glucose tolerance test.', 8),
            ('Describe the principles of homeostasis using examples.', 'Internal environment; set point; receptors, control centre, effectors; negative feedback; examples: blood glucose, body temperature, water balance; positive feedback contrasts (childbirth, LH surge).', 6)],
  )


def _gtt_dq(rng, slot):
    t = [0, 30, 60, 90, 120, 150]
    normal = [round(x + rng.uniform(-0.3, 0.3), 1) for x in [4.9, 7.6, 6.4, 5.4, 5.0, 4.8]]
    diab = [round(x + rng.uniform(-0.4, 0.4), 1) for x in [7.8, 12.6, 14.8, 13.9, 12.4, 11.0]]
    intro = ('A glucose tolerance test was carried out: after fasting, each person drank 75 g of glucose and blood glucose was measured at intervals.\n\n'
             + table(['Time / min', 'Person A / mmol dm⁻³', 'Person B / mmol dm⁻³'], list(zip(t, normal, diab))))
    rA = (normal[1] - normal[4]) / 90
    pB = pct_change(diab[0], max(diab))
    parts = [
        ('State the maximum blood glucose of person B.', f'{max(diab)} mmol dm⁻³', f'{max(diab)} (A1).', 1),
        ('Calculate the mean rate of decrease in blood glucose of person A between 30 and 120 minutes.', f'{rA:.3f} mmol dm⁻³ min⁻¹', f'({normal[1]} − {normal[4]})/90 (M1) = {rA:.3f} (A1).', 2),
        ('Calculate the percentage increase in blood glucose of person B from 0 minutes to the maximum.', f'{signed(pB)} %', f'({max(diab)} − {diab[0]})/{diab[0]} × 100 (M1) = {signed(pB)} % (A1).', 2),
        ('Deduce, with reasons, which person has diabetes.', 'Person B: high fasting glucose, much higher peak, and glucose still very high after 2 hours (>11 mmol dm⁻³).', 'Person B (A1); two reasons from data (A1 A1).', 3),
        ('Explain the changes in person A’s blood glucose.', 'Glucose absorbed from the gut raises blood glucose; β cells secrete insulin; liver and muscle take up glucose and form glycogen; glucose returns to normal by negative feedback.', 'Absorption (A1); insulin (A1); uptake/glycogenesis (A1).', 3),
        ('Suggest why person B’s glucose fell slowly after 60 minutes.', 'Some glucose uptake still occurs (some insulin or insulin-independent uptake) and glucose is lost in urine when above the renal threshold.', 'Valid suggestion (A1).', 1),
        ('Explain why the test is carried out after fasting.', 'So all start from a baseline glucose not affected by a recent meal, making results comparable.', 'Baseline (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch09-st1', _gtt_dq)

pct_items(R, 'ch09-st1', [
    ('After a meal rich in carbohydrate, a person’s plasma insulin rose from {a} to {b} µU cm⁻³.', 'µU cm⁻³', 5, 12, 4.0, 8.0, 0, 'rising blood glucose stimulates β cells to secrete insulin.'),
    ('During a 2-hour run, the glycogen content of a runner’s liver fell from {a} g to {b} g.', 'g', 80, 110, -0.7, -0.4, 0, 'glucagon (and adrenaline) stimulate glycogen breakdown to maintain blood glucose.'),
    ('Fasting blood glucose of a patient with type 2 diabetes fell from {a} to {b} mmol dm⁻³ after six months of diet and exercise.', 'mmol dm⁻³', 7.5, 10.5, -0.35, -0.15, 1, 'weight loss and exercise increase insulin sensitivity, so cells take up more glucose.'),
])


S('ch09-st2',
  terms=[('thermoregulation', 'the maintenance of a constant core body temperature'),
         ('endotherm', 'an animal that generates heat internally by metabolism to maintain a constant body temperature'),
         ('thermoreceptor', 'a sensory receptor that detects changes in temperature, found in the skin and the hypothalamus'),
         ('vasodilation', 'widening of arterioles supplying skin capillaries, increasing blood flow near the surface and heat loss'),
         ('vasoconstriction', 'narrowing of arterioles supplying skin capillaries, reducing blood flow near the surface and heat loss'),
         ('shivering', 'rapid involuntary contraction of skeletal muscles that generates heat by respiration'),
         ('brown adipose tissue', 'fat tissue with many mitochondria that generates heat by uncoupled respiration (thermogenesis)'),
         ('thyroxine', 'a hormone from the thyroid gland that increases metabolic rate and heat production')],
  facts=[('What is normal human core body temperature?', 'about 37 °C', ['about 35 °C', 'about 40 °C', 'about 30 °C'], 'Optimal for enzymes.'),
         ('Which part of the brain acts as the thermoregulatory centre?', 'the hypothalamus', ['the cerebellum', 'the medulla', 'the cerebral cortex'], 'Monitors blood temperature.'),
         ('Which protein in brown fat mitochondria allows heat generation?', 'thermogenin (uncoupling protein 1)', ['ATP synthase only', 'haemoglobin', 'insulin'], 'Uncouples proton gradient from ATP synthesis.'),
         ('How does sweating cool the body?', 'evaporation of water from the skin absorbs latent heat', ['sweat is cold', 'sweat reflects sunlight', 'sweat contains salt'], 'About 2.4 kJ per g.'),
         ('Which hormone increases metabolic rate in cold conditions?', 'thyroxine', ['ADH', 'insulin', 'melatonin'], 'From the thyroid gland.')],
  mc2=[('Why does vasodilation increase heat loss?', 'More blood flows through capillaries near the skin surface, so more heat is lost by radiation and convection.', ['Blood vessels move to the surface.', 'It reduces sweat production.', 'It increases shivering.'], 'Arterioles dilate.'),
       ('Why do babies rely more on brown adipose tissue than adults?', 'They have a large surface area to volume ratio and cannot shiver effectively.', ['They have no hypothalamus.', 'They sweat more.', 'Brown fat is only made in adults.'], 'Non-shivering thermogenesis.'),
       ('Why is sweating less effective at cooling in humid conditions?', 'Evaporation is slower when the air is already saturated with water vapour.', ['Sweat is not produced.', 'Sweat glands close.', 'Humidity raises skin blood flow.'], 'Evaporation needed.'),
       ('Why do hairs being raised help endotherms keep warm?', 'They trap a layer of air, which is a poor conductor of heat.', ['They produce heat.', 'They release sweat.', 'They increase blood flow.'], 'Insulation; small effect in humans.')],
  mc3=[('Evaporation of 1 g of sweat removes about 2.4 kJ. How much sweat must evaporate to remove 600 kJ?', '250 g', ['1440 g', '25 g', '2.5 g'], '600/2.4 = 250 g.'),
       ('A person enters a cold room. Which combination of responses is expected?', 'vasoconstriction, shivering and increased thyroxine', ['vasodilation, sweating and reduced metabolism', 'vasodilation and shivering only', 'sweating and vasoconstriction'], 'Reduce heat loss, increase production.'),
       ('Core temperature rises to 39 °C during exercise. Where is this detected?', 'thermoreceptors in the hypothalamus', ['thermoreceptors in the pancreas', 'baroreceptors in the aorta', 'chemoreceptors in the kidney'], 'Central receptors.')],
  why=[('Explain how the hypothalamus controls body temperature when the body is too hot.', 'Thermoreceptors in the hypothalamus and skin detect a rise; the hypothalamus sends impulses to effectors: arterioles to skin dilate (vasodilation), sweat glands secrete sweat which evaporates, hair erector muscles relax; metabolic rate may decrease; negative feedback restores 37 °C.'),
       ('Explain how heat is generated and conserved in cold conditions.', 'Vasoconstriction of skin arterioles reduces heat loss; shivering (muscle contraction) generates heat from respiration; brown adipose tissue generates heat by uncoupled respiration; thyroxine increases metabolic rate; hair erection traps air; behaviour such as wearing clothes.'),
       ('Explain the role of thyroxine in thermoregulation.', 'In the cold the hypothalamus secretes TRH, stimulating TSH from the anterior pituitary, which causes the thyroid to secrete thyroxine; thyroxine increases the metabolic rate of cells, so more heat is released by respiration.')],
  contrast=[('vasodilation', 'vasoconstriction', 'Vasodilation widens skin arterioles, increasing blood flow to the surface and heat loss; vasoconstriction narrows them, reducing blood flow and conserving heat.'),
            ('endotherms', 'ectotherms', 'Endotherms generate metabolic heat to keep body temperature constant; ectotherms rely mainly on external heat sources and behaviour, so their temperature varies with the environment.')],
  misc=[('In vasodilation, blood vessels move closer to the skin surface.', 'Vessels do not move; arterioles widen so more blood flows through surface capillaries.'),
        ('Sweat cools you because it is cold.', 'Cooling is due to evaporation, which absorbs heat from the skin.'),
        ('Shivering is a voluntary response to cold.', 'Shivering is an involuntary reflex controlled by the hypothalamus.')],
  cases=[('hypothermia in mountaineers', 'When core temperature falls below 35 °C, people become confused and shivering eventually stops.', 'thermoregulation', 'Heat loss exceeds heat production, so the hypothalamus can no longer maintain core temperature and enzymes slow.'),
         ('brown fat in newborn babies', 'Newborns have deposits of brown adipose tissue between the shoulder blades.', 'non-shivering thermogenesis', 'Uncoupled respiration in brown fat releases heat instead of making ATP, helping babies stay warm.')],
  evaluate=[('Endothermy is a better strategy than ectothermy.', ['endotherms can remain active in cold conditions and at night', 'enzymes work at a constant optimum'], ['endotherms need much more food energy', 'ectotherms survive on less food and in deserts can be very successful'], 'Endothermy gives independence from environmental temperature at a high energy cost; which is better depends on habitat and food supply.')],
  extended=[('Explain how body temperature is regulated in humans.', 'Set point 37 °C; thermoreceptors (skin, hypothalamus); hypothalamus as control centre; responses to heat: vasodilation, sweating, hair flattening; responses to cold: vasoconstriction, shivering, brown fat, thyroxine (TRH, TSH), hair erection; behaviour; negative feedback.', 8),
            ('Explain the importance of maintaining a constant core temperature.', 'Enzymes have optimum temperatures; too high: denaturation; too low: slow reactions; nervous function; consequences of hypothermia and hyperthermia; heat stroke.', 6)],
  )


@R.add('ch09-st2', 'C3', (1, 4), 'numerical')
def sweat_heat(rng, slot):
    who = pick(rng, ['a marathon runner', 'a cyclist', 'a footballer', 'a hiker in hot weather'])
    vol = round(rng.uniform(0.5, 2.5), 2)
    frac = pick(rng, [0.6, 0.7, 0.8, 1.0])
    heat = vol * 1000 * frac * 2.4
    stem = (f'{who.capitalize()} lost {vol} kg of sweat during exercise, of which {int(frac * 100)} % evaporated from the skin. Evaporation of 1 g of water removes 2.4 kJ. Calculate the heat removed by evaporation.')
    return num(stem, f'{heat:.0f} kJ', f'{vol} × 1000 × {frac} = {vol * 1000 * frac:.0f} g evaporated (M1); × 2.4 = {heat:.0f} kJ (A1).', 2)


def _skin_dq(rng, slot):
    t = [0, 5, 10, 15, 20, 25, 30]
    core = [37.0, 37.3, 37.7, 38.0, 38.1, 38.1, 38.0]
    core = [round(x + rng.uniform(-0.05, 0.05), 1) for x in core]
    skin = [round(x + rng.uniform(-0.2, 0.2), 1) for x in [32.5, 33.0, 33.8, 34.4, 34.6, 34.7, 34.6]]
    sweat = [round(x * rng.uniform(0.85, 1.15), 0) for x in [5, 30, 120, 260, 330, 350, 350]]
    intro = ('A student exercised on a cycle ergometer for 30 minutes in a warm room. Core (rectal) temperature, skin temperature and sweat rate were recorded.\n\n'
             + table(['Time / min', 'Core temperature / °C', 'Skin temperature / °C', 'Sweat rate / g h⁻¹'], list(zip(t, core, skin, [f'{s:.0f}' for s in sweat]))))
    heat = sweat[-1] * 2.4
    parts = [
        ('State the maximum core temperature.', f'{max(core)} °C', f'{max(core)} (A1).', 1),
        ('Calculate the heat lost per hour by evaporation at the final sweat rate (2.4 kJ g⁻¹), assuming all sweat evaporates.', f'{heat:.0f} kJ h⁻¹', f'{sweat[-1]:.0f} × 2.4 = {heat:.0f} (A1).', 1),
        ('Describe the changes in core temperature and sweat rate.', 'Core temperature rises during the first 15–20 min then levels off; sweat rate rises sharply after a delay and then plateaus.', 'Core rise then plateau (A1); sweat rise then plateau (A1).', 2),
        ('Explain why core temperature rises at the start of exercise.', 'Muscle contraction increases respiration, which releases heat faster than it is lost.', 'Respiration releases heat (A1); production > loss (A1).', 2),
        ('Explain why core temperature levels off.', 'Hypothalamus detects the rise; sweating and vasodilation increase heat loss until it equals heat production; negative feedback.', 'Hypothalamus (A1); increased heat loss (A1); balance/negative feedback (A1).', 3),
        ('Explain the rise in skin temperature.', 'Vasodilation of arterioles supplying skin capillaries increases blood flow near the surface.', 'Vasodilation (A1).', 1),
        ('Suggest why the student should drink water during prolonged exercise.', 'To replace water lost in sweat and prevent dehydration, which reduces sweating and blood volume.', 'Replace water lost (A1).', 1),
        ('Calculate the rise in core temperature during the first 15 minutes and the mean rate of rise.', f'{core[3] - core[0]:.1f} °C; {(core[3] - core[0]) / 15:.3f} °C min⁻¹', f'{core[3]} − {core[0]} = {core[3] - core[0]:.1f} °C (A1); ÷ 15 = {(core[3] - core[0]) / 15:.3f} °C min⁻¹ (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch09-st2', _skin_dq)


S('ch09-st3',
  terms=[('nephron', 'the functional unit of the kidney, consisting of a glomerulus, Bowman’s capsule, proximal convoluted tubule, loop of Henle, distal convoluted tubule and collecting duct'),
         ('ultrafiltration', 'filtration of blood under high pressure in the glomerulus, forcing small molecules through the basement membrane into Bowman’s capsule'),
         ('selective reabsorption', 'the reabsorption of useful substances such as glucose, amino acids and much of the water and ions from the filtrate back into the blood, mainly in the proximal convoluted tubule'),
         ('osmoregulation', 'the control of the water potential (solute concentration) of body fluids'),
         ('antidiuretic hormone (ADH)', 'a hormone released from the posterior pituitary that increases the permeability of the collecting ducts to water by inserting aquaporins'),
         ('loop of Henle', 'the hairpin-shaped section of the nephron that creates a high solute concentration in the medulla, allowing concentrated urine to be produced'),
         ('podocytes', 'cells of Bowman’s capsule with foot-like extensions that leave filtration slits'),
         ('excretion', 'the removal from the body of waste products of metabolism, such as urea')],
  facts=[('Approximately how much filtrate do human kidneys produce per day?', 'about 180 dm³', ['about 1.5 dm³', 'about 18 dm³', 'about 1800 dm³'], 'Most is reabsorbed.'),
         ('Where is glucose normally reabsorbed?', 'the proximal convoluted tubule', ['the collecting duct', 'the loop of Henle', 'the bladder'], 'By co-transport with Na⁺.'),
         ('Where is ADH released from?', 'the posterior pituitary', ['the anterior pituitary', 'the adrenal cortex', 'the kidney'], 'Made in the hypothalamus.'),
         ('Which nitrogenous waste is excreted by mammals?', 'urea', ['ammonia only', 'uric acid only', 'glucose'], 'Made in the liver from excess amino acids.'),
         ('Which substance is not normally found in the glomerular filtrate?', 'plasma proteins', ['glucose', 'urea', 'sodium ions'], 'Too large to pass the basement membrane.')],
  mc2=[('Why does ultrafiltration occur in the glomerulus?', 'The afferent arteriole is wider than the efferent arteriole, creating high blood pressure in the capillaries.', ['Active transport pumps plasma.', 'Osmosis moves proteins.', 'Bowman’s capsule has low permeability.'], 'Hydrostatic pressure.'),
       ('Why do cells of the proximal convoluted tubule have many mitochondria and microvilli?', 'Microvilli increase surface area and mitochondria supply ATP for active transport during reabsorption.', ['To produce urea.', 'To filter blood.', 'To store glycogen.'], 'Structure–function.'),
       ('Why does ADH secretion increase when a person is dehydrated?', 'Osmoreceptors in the hypothalamus detect low blood water potential.', ['Blood volume rises.', 'Glucose rises.', 'Urine becomes dilute.'], 'Negative feedback.'),
       ('Why is glucose found in the urine of people with untreated diabetes?', 'Filtrate glucose exceeds the maximum rate at which the transport proteins can reabsorb it.', ['Glucose is made in the kidney.', 'Glomeruli stop filtering glucose.', 'ADH carries glucose.'], 'Renal threshold.')],
  mc3=[('The kidneys filter 180 dm³ of fluid per day and produce 1.5 dm³ of urine. What percentage of the filtrate is reabsorbed?', '99.2 %', ['0.8 %', '83 %', '120 %'], '(180 − 1.5)/180 × 100.'),
       ('Urea concentration is 0.3 g dm⁻³ in plasma and 20 g dm⁻³ in urine. By what factor has it been concentrated?', 'about 67 times', ['about 20 times', 'about 6 times', 'about 0.015 times'], '20/0.3.'),
       ('A person drinks 2 dm³ of water. Which change follows?', 'ADH secretion falls; fewer aquaporins; more dilute urine', ['ADH secretion rises; concentrated urine', 'glucose appears in urine', 'filtration stops'], 'High water potential.')],
  why=[('Explain how the structure of the glomerulus and Bowman’s capsule allows ultrafiltration.', 'Afferent arteriole wider than efferent gives high hydrostatic pressure; fenestrated capillary endothelium; basement membrane acts as the filter, retaining proteins and cells; podocytes with filtration slits; water, glucose, urea, ions pass into the capsule.'),
       ('Explain how ADH controls the water content of the blood.', 'Osmoreceptors in the hypothalamus detect low water potential; ADH released from posterior pituitary; ADH binds to receptors on collecting-duct cells; vesicles with aquaporins fuse with membrane; more water reabsorbed by osmosis into the hypertonic medulla; small volume of concentrated urine; negative feedback.'),
       ('Explain the role of the loop of Henle.', 'The ascending limb actively transports Na⁺ and Cl⁻ out into the medulla and is impermeable to water; the descending limb is permeable to water, which leaves by osmosis; countercurrent multiplier creates a high solute concentration deep in the medulla, allowing water to be reabsorbed from collecting ducts.')],
  contrast=[('ultrafiltration', 'selective reabsorption', 'Ultrafiltration is the non-selective, pressure-driven filtration of small molecules from blood into Bowman’s capsule; selective reabsorption is the return of useful substances from the filtrate to the blood by active transport, co-transport and osmosis.'),
            ('the proximal convoluted tubule', 'the collecting duct', 'The proximal convoluted tubule reabsorbs all glucose and amino acids and most water and ions; the collecting duct reabsorbs variable amounts of water under ADH control.')],
  misc=[('The kidney filters only waste products from the blood.', 'All small molecules are filtered, including useful ones, which are then reabsorbed.'),
        ('ADH makes more urine.', 'ADH increases water reabsorption, so less, more concentrated urine is produced.'),
        ('Urea is made in the kidneys.', 'Urea is made in the liver from excess amino acids (deamination); kidneys excrete it.')],
  cases=[('kidney dialysis', 'Patients with kidney failure have blood passed through a dialyser with a partially permeable membrane and dialysis fluid.', 'kidney function', 'Dialysis fluid with normal concentrations of glucose and ions but no urea allows urea and excess ions to diffuse out, replacing filtration.'),
         ('desert mammals such as the kangaroo rat', 'Kangaroo rats survive without drinking and produce very concentrated urine.', 'osmoregulation and the loop of Henle', 'Very long loops of Henle create a high medullary solute concentration so most water is reabsorbed.')],
  evaluate=[('Kidney transplants are a better treatment for kidney failure than dialysis.', ['restores near-normal kidney function and quality of life', 'cheaper in the long term'], ['shortage of donors; long waiting lists', 'requires lifelong immunosuppressants with infection risk; rejection possible'], 'Transplants are generally better where a matched donor is available, while dialysis remains essential for those waiting or unsuitable.')],
  extended=[('Explain how the structure of the nephron allows it to produce urine and regulate the water content of the blood.', 'Glomerulus, Bowman’s capsule, ultrafiltration; PCT microvilli, mitochondria, co-transport of glucose; loop of Henle countercurrent; DCT; collecting duct, ADH, aquaporins; osmoreceptors in hypothalamus; negative feedback; urea excretion.', 8),
            ('Explain the role of the kidney in excretion and osmoregulation, and compare dialysis with kidney transplant as treatments for kidney failure.', 'Excretion of urea; osmoregulation by ADH; dialysis principle (diffusion across membrane, countercurrent, fluid composition); transplant benefits and risks.', 6)],
  )


@R.add('ch09-st3', 'C3', (1, 5), 'numerical')
def reabsorb_calc(rng, slot):
    sub, filt, urine, unit = pick(rng, [('water', 180, None, 'dm³'), ('sodium ions', 600, None, 'g'), ('urea', 54, None, 'g')])
    if sub == 'water':
        urine = round(rng.uniform(0.8, 2.5), 1)
    elif sub == 'sodium ions':
        urine = round(rng.uniform(3, 6), 1)
    else:
        urine = round(rng.uniform(25, 32), 0)
    filt = round(filt * rng.uniform(0.9, 1.1))
    p = 100 * (filt - urine) / filt
    stem = f'In 24 hours a person’s kidneys filtered {filt} {unit} of {sub}, and {urine:g} {unit} appeared in the urine. Calculate the percentage of the filtered {sub} that was reabsorbed.'
    if slot.d >= 4:
        stem += ' Explain why the percentage for urea is much lower than for water.'
        return num(stem, f'{p:.1f} %; urea is a waste product and is not actively reabsorbed (only some diffuses back), whereas water is reabsorbed by osmosis',
                   f'({filt} − {urine:g})/{filt} × 100 (M1) = {p:.1f} % (A1); explanation (R1).', 3)
    return num(stem, f'{p:.1f} %', f'({filt} − {urine:g})/{filt} × 100 (M1) = {p:.1f} % (A1).', 2)


def _nephron_dq(rng, slot):
    subs = ['water', 'glucose', 'amino acids', 'urea', 'sodium ions', 'proteins']
    plasma = [None, round(rng.uniform(0.9, 1.1), 2), round(rng.uniform(0.45, 0.55), 2), round(rng.uniform(0.25, 0.35), 2), round(rng.uniform(3.1, 3.4), 2), round(rng.uniform(70, 80), 0)]
    filt = [None, plasma[1], plasma[2], plasma[3], plasma[4], 0]
    urine = [None, 0, 0, round(rng.uniform(18, 25), 1), round(rng.uniform(3.5, 6.0), 2), 0]
    rows = [(subs[i], plasma[i], filt[i], urine[i]) for i in range(1, 6)]
    gfr = 180
    uvol = round(rng.uniform(1.2, 2.0), 1)
    urine[3] = round(filt[3] * gfr * rng.uniform(0.4, 0.6) / uvol, 1)
    rows = [(subs[i], plasma[i], filt[i], urine[i]) for i in range(1, 6)]
    intro = (f'The concentrations (g dm⁻³) of substances in plasma, glomerular filtrate and urine of a healthy person are shown. Filtrate is produced at {gfr} dm³ per day and urine at {uvol} dm³ per day.\n\n'
             + table(['Substance', 'Plasma', 'Filtrate', 'Urine'], rows))
    cf = urine[3] / plasma[3]
    ufilt = filt[3] * gfr
    uex = urine[3] * uvol
    parts = [
        ('State which substance is present in plasma but not in filtrate.', 'proteins', 'Proteins (A1).', 1),
        ('Calculate the concentration factor of urea from plasma to urine.', f'{cf:.0f}', f'{urine[3]}/{plasma[3]} = {cf:.0f} (A1).', 1),
        ('Calculate the mass of urea filtered and the mass excreted per day, and the percentage reabsorbed.', f'filtered {ufilt:.0f} g; excreted {uex:.0f} g; {100 * (ufilt - uex) / ufilt:.0f} % reabsorbed',
         f'{filt[3]} × {gfr} = {ufilt:.0f} g (A1); {urine[3]} × {uvol} = {uex:.0f} g (A1); ({ufilt:.0f} − {uex:.0f})/{ufilt:.0f} × 100 = {100 * (ufilt - uex) / ufilt:.0f} % (A1).', 3),
        ('Explain why proteins are absent from the filtrate.', 'They are too large to pass through the basement membrane (and filtration slits).', 'Size/basement membrane (A1).', 1),
        ('Explain why glucose is absent from the urine.', 'All glucose is reabsorbed in the proximal convoluted tubule by co-transport with Na⁺ and facilitated diffusion.', 'Reabsorbed in PCT (A1); co-transport/active (A1).', 2),
        ('Explain why urea is more concentrated in urine than in filtrate.', 'Most water is reabsorbed (about 99 %) while much less urea is reabsorbed.', 'Water reabsorption (A1).', 1),
        ('Predict how the urine volume and urea concentration would change if the person became dehydrated.', 'Less urine, with higher urea concentration, because more ADH increases water reabsorption in the collecting ducts.', 'Correct prediction (A1); ADH explanation (A1).', 2),
        ('Predict and explain how the urine of a person with untreated diabetes mellitus would differ.', 'Glucose would be present because filtrate glucose exceeds the reabsorption capacity of the transporters; urine volume increases because glucose lowers the water potential of the filtrate, so less water is reabsorbed.', 'Glucose present with reason (A1); more urine with reason (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch09-st3', _nephron_dq)


# =============================================================================================
# ch10 D4.1–D4.3 Natural selection, stability and change, climate change
# =============================================================================================
S('ch10-st1',
  terms=[('natural selection', 'the process by which individuals with heritable characteristics better suited to the environment survive and reproduce more, so these characteristics become more common'),
         ('selection pressure', 'an environmental factor, such as predation, disease or competition, that affects the survival and reproduction of individuals with particular traits'),
         ('fitness', 'the ability of an individual to survive and reproduce in its environment, relative to others in the population'),
         ('sexual selection', 'selection arising from competition for mates or mate choice, favouring traits that increase mating success'),
         ('heritable variation', 'differences between individuals that are caused by genes and can be passed on to offspring'),
         ('abiotic factor', 'a non-living factor in the environment such as temperature, water or light'),
         ('overproduction of offspring', 'the production of more offspring than the environment can support, leading to competition and a struggle for survival')],
  facts=[('Which is a source of heritable variation?', 'mutation', ['acquired muscle mass', 'a scar from injury', 'a suntan'], 'New alleles.'),
         ('Who studied guppies in Trinidad to show the balance of natural and sexual selection?', 'John Endler', ['Gregor Mendel', 'Robert Paine', 'Charles Keeling'], 'Spots and predation.'),
         ('Which feature of peacocks is a result of sexual selection?', 'the long, colourful tail of males', ['the beak shape', 'the ability to digest seeds', 'the number of chromosomes'], 'Female choice.'),
         ('What did Darwin observe about the beaks of finches in the Galápagos?', 'beak shape varies with diet on different islands', ['all finches have identical beaks', 'beaks change during an individual’s lifetime', 'finches have no beaks'], 'Adaptation to food sources.'),
         ('Which is an abiotic selection pressure?', 'drought', ['predation', 'parasitism', 'competition for mates'], 'Non-living.')],
  mc2=[('Why does overproduction of offspring lead to natural selection?', 'Resources are limited, so there is competition and only the best-adapted survive to reproduce.', ['All offspring survive.', 'It reduces variation.', 'It prevents competition.'], 'Struggle for existence.'),
       ('Why must variation be heritable for natural selection to cause evolution?', 'Only genetic traits are passed to offspring, so only they can increase in frequency.', ['Acquired traits are inherited.', 'Environment changes genes.', 'Variation is always beneficial.'], 'Inheritance needed.'),
       ('Why are bright colours in male guppies less common in streams with many predators?', 'Brightly coloured males are more visible and more likely to be eaten.', ['Predators prefer dull fish.', 'Females prefer dull males.', 'Colours fade in fast water.'], 'Natural selection opposes sexual selection.'),
       ('Why did the frequency of dark peppered moths increase in industrial areas?', 'Dark moths were better camouflaged on soot-covered trees and less often eaten by birds.', ['Soot changed the moths’ genes.', 'Dark moths laid more eggs everywhere.', 'Pale moths migrated away.'], 'Selection by predation.')],
  mc3=[('In a population of beetles, the proportion of dark individuals rose from 12 % to 30 % over 10 generations. What is the most likely explanation?', 'Dark beetles had greater survival and reproduction under a selection pressure.', ['Beetles changed colour to match the background.', 'Mutation rate increased tenfold.', 'Pale beetles learned to hide.'], 'Natural selection.'),
       ('A farmer sprays pesticide every year; after some years it no longer works. What has happened?', 'Resistant individuals survived and reproduced, so resistance became common.', ['The pesticide caused resistance mutations in every insect.', 'The insects learned to avoid it.', 'The pesticide decayed.'], 'Selection of existing variation.'),
       ('Endler moved guppies from a high-predation to a low-predation stream. After about 15 generations, males had more spots. Why?', 'Sexual selection by female choice now outweighed predation pressure.', ['Spots protect from predators.', 'Females became more spotted.', 'Mutation stopped.'], 'Balance of selection pressures.')],
  why=[('Explain how natural selection causes evolution.', 'Populations show heritable variation (mutation, meiosis, fertilisation); more offspring are produced than can survive; competition for resources; individuals with favourable traits are more likely to survive and reproduce; they pass on alleles; allele frequencies change over generations; the population becomes adapted.'),
       ('Explain how sexual selection can lead to traits that reduce survival.', 'Traits such as bright colours or long tails increase mating success through female choice or male competition; individuals with them produce more offspring even if they are more vulnerable to predators; the trait spreads if reproductive benefit exceeds survival cost.'),
       ('Explain Endler’s experiments on guppies.', 'Guppies in streams with many predators have fewer, smaller spots; in low-predation streams males are more colourful; Endler moved guppies between pools and set up artificial ponds; within a few generations spot number changed according to predation pressure; shows balance of natural and sexual selection.')],
  contrast=[('natural selection', 'sexual selection', 'Natural selection favours traits that increase survival and reproduction in the environment; sexual selection favours traits that increase success in obtaining mates, which may reduce survival.'),
            ('heritable variation', 'acquired characteristics', 'Heritable variation is genetic and passed to offspring; acquired characteristics develop during life (e.g. muscles, scars) and are not inherited.')],
  misc=[('Individual organisms evolve during their lifetime.', 'Populations evolve over generations as allele frequencies change; individuals do not.'),
        ('Organisms develop adaptations because they need them.', 'Adaptations arise from random variation that is then selected; need does not cause mutation.'),
        ('Natural selection always produces perfect organisms.', 'Selection works on existing variation and involves trade-offs, so adaptations are often imperfect.'),
        ('“Survival of the fittest” means the strongest individuals survive.', 'Fitness means reproductive success in a given environment, not strength.')],
  cases=[('Endler’s guppies in Trinidad', 'Guppies from high-predation streams moved to low-predation sites evolved brighter colours within about 15 generations.', 'natural and sexual selection', 'Reduced predation pressure allowed sexual selection by female choice to favour colourful males.'),
         ('peppered moths in industrial Britain', 'Dark (melanic) moths increased in polluted areas in the 19th century and decreased after clean-air laws.', 'natural selection by predation', 'Camouflage against the background affected predation by birds, changing allele frequencies.'),
         ('Galápagos finches during the 1977 drought', 'After the drought, medium ground finches with deeper beaks survived better because only large, hard seeds remained.', 'selection pressures', 'A change in food supply selected for beak depth, and the next generation had deeper beaks.')],
  evaluate=[('Natural selection is the only mechanism of evolutionary change.', ['explains adaptation in many examples (finches, moths, antibiotic resistance)'], ['genetic drift and gene flow change allele frequencies randomly or by migration', 'mutation supplies variation; sexual selection is a distinct process'], 'Natural selection is the main cause of adaptation, but other mechanisms such as drift also change allele frequencies.')],
  extended=[('Explain the process of natural selection and discuss evidence that it occurs, using named examples.', 'Variation (mutation, meiosis, sexual reproduction); overproduction; competition; selection pressures (abiotic and biotic); differential survival and reproduction; inheritance; change in allele frequencies; examples: Galápagos finches, peppered moths, Endler’s guppies, antibiotic resistance.', 8),
            ('Explain how sexual selection can produce traits that appear disadvantageous.', 'Female choice, male–male competition; honest signals; peacock tail; guppy spots; trade-off with predation; Endler’s experiments.', 6)],
  )


def _guppy_dq(rng, slot):
    gens = [0, 5, 10, 15, 20]
    lo = [round(x + rng.uniform(-0.4, 0.4), 1) for x in [9.5, 10.3, 11.4, 12.6, 13.1]]
    hi = [round(x + rng.uniform(-0.4, 0.4), 1) for x in [9.5, 8.8, 8.1, 7.6, 7.3]]
    intro = ('Guppies taken from one population were placed in artificial ponds with either no predators or many predators (pike cichlids). The mean number of coloured spots per male was recorded every five generations.\n\n'
             + table(['Generation', 'No predators', 'Many predators'], list(zip(gens, lo, hi))))
    pa = pct_change(lo[0], lo[-1])
    pb = pct_change(hi[0], hi[-1])
    parts = [
        ('State the mean number of spots in the no-predator pond after 15 generations.', f'{lo[3]}', f'{lo[3]} (A1).', 1),
        ('Calculate the percentage change in spot number over 20 generations in each pond.', f'no predators {signed(pa)} %; many predators {signed(pb)} %', f'({lo[-1]} − {lo[0]})/{lo[0]} × 100 = {signed(pa)} % (A1); ({hi[-1]} − {hi[0]})/{hi[0]} × 100 = {signed(pb)} % (A1).', 2),
        ('Explain the change in the pond with many predators.', 'Brightly spotted males are more conspicuous and more likely to be eaten; less spotted males survive and reproduce; alleles for fewer spots increase.', 'Predation of conspicuous males (A1); survival and reproduction (A1); allele frequency change (A1).', 3),
        ('Explain the change in the pond with no predators.', 'Females prefer more colourful males (sexual selection); without predation there is no survival cost, so spot number increases.', 'Female choice (A1); no predation cost (A1).', 2),
        ('Explain why both ponds started with the same population.', 'So differences can be attributed to predation, not to differences in original variation.', 'Control/comparison (A1).', 1),
        ('State one condition necessary for spot number to change by natural selection.', 'Spot number must be heritable (genetically determined) and variable.', 'Heritable variation (A1).', 1),
        ('Suggest why the experiment was continued for 20 generations.', 'Changes in allele frequency by selection take several generations; a long period shows whether the trend is consistent.', 'Several generations needed (A1); consistent trend (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch10-st1', _guppy_dq)

pct_items(R, 'ch10-st1', [
    ('After a drought on Daphne Major, the mean beak depth of medium ground finches changed from {a} mm to {b} mm in the next generation.', 'mm', 8.8, 9.4, 0.03, 0.07, 2, 'only birds with deeper beaks could crack the large, hard seeds that remained, so they survived and passed on alleles for deep beaks.'),
    ('The frequency of the melanic form of the peppered moth near Manchester changed from {a} % to {b} % after clean-air legislation.', '%', 85, 95, -0.7, -0.4, 0, 'cleaner tree bark made dark moths more visible to bird predators, so pale moths had a survival advantage.'),
    ('The percentage of houseflies surviving a standard dose of an insecticide rose from {a} % to {b} % after ten years of spraying.', '%', 2, 10, 3.0, 8.0, 1, 'insecticide killed susceptible flies, so resistant individuals survived and reproduced, increasing resistance alleles.'),
])


S('ch10-st2',
  terms=[('gene pool', 'all the alleles of all the genes in a population at a given time'),
         ('allele frequency', 'the proportion of all copies of a gene in a population that are a particular allele'),
         ('Hardy–Weinberg principle', 'the principle that allele and genotype frequencies remain constant between generations if there is no selection, mutation, migration or genetic drift and mating is random: p² + 2pq + q² = 1'),
         ('stabilising selection', 'selection that favours intermediate phenotypes and acts against both extremes'),
         ('directional selection', 'selection that favours one extreme phenotype, shifting the mean'),
         ('disruptive selection', 'selection that favours both extremes and acts against intermediate phenotypes'),
         ('artificial selection', 'the selective breeding of organisms by humans for desired characteristics')],
  facts=[('In the Hardy–Weinberg equation, what does 2pq represent?', 'the frequency of heterozygotes', ['the frequency of homozygous dominants', 'the frequency of the recessive allele', 'the total population'], 'p² + 2pq + q² = 1.'),
         ('Which is an example of stabilising selection?', 'human birth mass, where very low and very high masses have higher mortality', ['antibiotic resistance', 'peppered moth melanism', 'beak size in two-seed-size environments'], 'Intermediate favoured.'),
         ('Which condition is required for Hardy–Weinberg equilibrium?', 'random mating', ['strong selection', 'high mutation rate', 'a small population'], 'Large, isolated, no selection.'),
         ('What does p + q equal in the Hardy–Weinberg principle?', '1', ['0', '2', '0.5'], 'Two alleles only.'),
         ('Which type of selection may lead to speciation within a population?', 'disruptive selection', ['stabilising selection', 'no selection', 'artificial insemination'], 'Two extremes favoured.')],
  mc2=[('Why do allele frequencies change if a population is not in Hardy–Weinberg equilibrium?', 'Selection, mutation, migration, drift or non-random mating alter the gene pool.', ['The equation stops working.', 'Allele frequencies never change.', 'Dominant alleles always increase.'], 'Departures from conditions.'),
       ('Why does directional selection shift the mean phenotype?', 'Individuals at one extreme have higher fitness, so their alleles increase in frequency.', ['Both extremes are favoured.', 'The intermediate is favoured.', 'Mutation stops.'], 'One extreme favoured.'),
       ('Why can a harmful recessive allele persist in a population?', 'It is hidden in heterozygotes, where it is not selected against.', ['It is always dominant.', 'It is removed only in heterozygotes.', 'It mutates back each generation.'], 'Carriers.'),
       ('Why is genetic drift more significant in small populations?', 'Chance events have a larger proportional effect on allele frequencies.', ['Small populations have more mutations.', 'Selection is stronger in large populations.', 'Drift only occurs in large populations.'], 'Sampling error.')],
  mc3=[('In a population, 16 % of individuals show a recessive phenotype. What is the frequency of the dominant allele?', '0.6', ['0.4', '0.84', '0.16'], 'q² = 0.16, q = 0.4, p = 0.6.'),
       ('If q = 0.3, what percentage of the population are heterozygous?', '42 %', ['21 %', '9 %', '49 %'], '2pq = 2 × 0.7 × 0.3.'),
       ('Cystic fibrosis affects 1 in 2500 people of European descent. What is the approximate carrier frequency?', '1 in 25', ['1 in 50', '1 in 2500', '1 in 5'], 'q = 0.02; 2pq ≈ 0.039.')],
  why=[('Explain how the Hardy–Weinberg equation is used to estimate the frequency of carriers of a recessive allele.', 'The frequency of the recessive phenotype equals q²; take the square root to find q; p = 1 − q; heterozygote (carrier) frequency = 2pq; assumes the population is in equilibrium (large, random mating, no selection, mutation or migration).'),
       ('Explain the three patterns of natural selection.', 'Stabilising selection favours intermediate phenotypes, reducing variation (e.g. birth mass); directional selection favours one extreme, shifting the mean (e.g. antibiotic resistance); disruptive selection favours both extremes, possibly leading to two forms (e.g. beak sizes when seeds are small or large).'),
       ('Explain the conditions required for Hardy–Weinberg equilibrium.', 'Large population (no drift); random mating; no mutation; no migration (gene flow); no natural selection; if these hold, allele and genotype frequencies remain constant; departure indicates evolution.')],
  contrast=[('stabilising selection', 'directional selection', 'Stabilising selection favours the intermediate phenotype and reduces variation without changing the mean; directional selection favours one extreme and shifts the mean.'),
            ('natural selection', 'artificial selection', 'In natural selection the environment determines which individuals reproduce; in artificial selection humans choose individuals with desired traits to breed.')],
  misc=[('Dominant alleles always increase in frequency over time.', 'Dominance does not affect frequency; without selection, frequencies stay constant (Hardy–Weinberg).'),
        ('p² is the frequency of the dominant phenotype.', 'p² is the frequency of homozygous dominants; the dominant phenotype frequency is p² + 2pq.'),
        ('Stabilising selection causes evolution to stop completely.', 'Stabilising selection maintains the mean but allele frequencies can still change through other processes.')],
  cases=[('sickle-cell allele frequency in malarial regions', 'In parts of Africa the HbS allele frequency reaches about 0.1–0.2, much higher than elsewhere.', 'balanced selection and Hardy–Weinberg', 'Heterozygotes are resistant to malaria, so the allele is maintained despite homozygotes having sickle-cell disease.'),
         ('human birth mass', 'Infant mortality is lowest for babies around 3–4 kg and higher for very light and very heavy babies.', 'stabilising selection', 'Extremes have lower survival, so intermediate mass is favoured.'),
         ('African seedcracker finches', 'Birds with either small or large beaks are common, but intermediate beaks are rare, matching two seed sizes.', 'disruptive selection', 'Intermediate beaks are inefficient for both seed types, so both extremes are favoured.')],
  evaluate=[('The Hardy–Weinberg principle is of little use because no real population meets its conditions.', ['real populations experience selection, migration and non-random mating'], ['it provides a null model; deviations show evolution is occurring', 'it allows carrier frequencies to be estimated for genetic counselling'], 'Although no population meets the conditions exactly, the principle is very useful as a baseline for detecting evolution and estimating allele frequencies.')],
  extended=[('Explain the Hardy–Weinberg principle, the conditions under which it applies and how it can be used to study evolution.', 'Gene pool; p + q = 1; p² + 2pq + q² = 1; conditions; calculation of carrier frequency; testing equilibrium with chi-squared; departures show selection, drift, migration, mutation; examples sickle-cell, CF.', 8),
            ('Describe stabilising, directional and disruptive selection, using examples, and explain their effects on the distribution of phenotypes.', 'Graphs; stabilising (birth mass) narrows distribution; directional (antibiotic resistance, finch beaks) shifts mean; disruptive (seedcracker finches) bimodal, possible speciation.', 6)],
  )


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def hw_calc(rng, slot):
    trait = pick(rng, ['albinism', 'cystic fibrosis', 'phenylketonuria', 'a recessive coat colour', 'red–green colour blindness (in a hypothetical autosomal model)'])
    q = rng.uniform(0.05, 0.6)
    q2 = round(q * q, 4)
    if q2 < 0.002:
        q2 = round(q2, 5)
    q = math.sqrt(q2)
    p = 1 - q
    stem = f'In a population in Hardy–Weinberg equilibrium, the frequency of individuals showing {trait} (homozygous recessive) is {q2:g}. Calculate the frequency of the recessive allele, the dominant allele and of heterozygous carriers.'
    return num(stem, f'q = {q:.3f}; p = {p:.3f}; 2pq = {2 * p * q:.3f}',
               f'q = √{q2:g} = {q:.3f} (A1); p = 1 − q = {p:.3f} (A1); 2pq = 2 × {p:.3f} × {q:.3f} = {2 * p * q:.3f} (A1).', 3)


@R.add('ch10-st2', 'C3', (1, 4), 'mcq')
def hw_mcq(rng, slot):
    q = pick(rng, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    p = 1 - q
    if rng.random() < 0.5:
        return nmcq(rng, f'The frequency of homozygous recessive individuals in a population is {q * q:.2f}. Assuming Hardy–Weinberg equilibrium, what is the frequency of heterozygotes?',
                    f'{2 * p * q:.2f}', [f'{p * q:.2f}', f'{p * p:.2f}', f'{1 - q * q:.2f}', f'{q:.2f}'], f'q = {q}, p = {p:.1f}, 2pq = {2 * p * q:.2f}.')
    return nmcq(rng, f'The frequency of the dominant allele is {p:.1f}. What proportion of the population shows the dominant phenotype?',
                f'{p * p + 2 * p * q:.2f}', [f'{p * p:.2f}', f'{2 * p * q:.2f}', f'{p:.2f}' if abs(p - (p * p + 2 * p * q)) > 0.005 else f'{q:.2f}', f'{q * q:.2f}'], f'p² + 2pq = {p * p:.2f} + {2 * p * q:.2f} = {p * p + 2 * p * q:.2f}.')


def _hw_dq(rng, slot):
    n = rng.randint(400, 1200)
    p = rng.uniform(0.35, 0.65)
    dev = rng.uniform(-0.12, 0.12)
    MM = round(n * (p * p + dev * p * (1 - p)))
    MN = round(n * (2 * p * (1 - p) * (1 - dev)))
    NN = n - MM - MN
    if NN < 10:
        return None
    pe = (2 * MM + MN) / (2 * n)
    qe = 1 - pe
    exp = [n * pe * pe, n * 2 * pe * qe, n * qe * qe]
    chi = sum((o - e) ** 2 / e for o, e in zip([MM, MN, NN], exp))
    sig = chi > 3.84
    intro = (f'The MN blood group is controlled by two codominant alleles, Lᴹ and Lᴺ. Blood samples from {n} people in a town were tested.\n\n'
             + table(['Blood group', 'Genotype', 'Number of people'], [('M', 'LᴹLᴹ', MM), ('MN', 'LᴹLᴺ', MN), ('N', 'LᴺLᴺ', NN)]))
    parts = [
        ('State the number of people with blood group MN.', f'{MN}', f'{MN} (A1).', 1),
        ('Calculate the frequency of the Lᴹ allele.', f'p = {pe:.3f}', f'(2 × {MM} + {MN})/(2 × {n}) (M1) = {pe:.3f} (A1).', 2),
        ('Calculate the expected numbers of each genotype if the population is in Hardy–Weinberg equilibrium.', f'M {exp[0]:.1f}; MN {exp[1]:.1f}; N {exp[2]:.1f}', f'p²n, 2pqn, q²n (M1); values {exp[0]:.1f}, {exp[1]:.1f}, {exp[2]:.1f} (A1).', 2),
        ('Calculate χ² and state whether the population is in equilibrium (critical value 3.84, 1 degree of freedom).', f'χ² = {chi:.2f}; ' + ('significant deviation – not in equilibrium' if sig else 'no significant deviation – consistent with equilibrium'),
         f'Σ(O − E)²/E = {chi:.2f} (A1); comparison and conclusion (A1).', 2),
        ('Explain why it is possible to count alleles directly in this example.', 'The alleles are codominant, so each genotype has a distinct phenotype.', 'Codominance (A1).', 1),
        ('Suggest two reasons why a human population might not be in Hardy–Weinberg equilibrium.', 'Non-random mating; migration; small population/drift; selection; mutation.', 'Two reasons (A1 A1).', 2),
        ('Explain why 1 degree of freedom is used even though there are three genotypes.', 'Three categories minus one, minus one more because the allele frequency was estimated from the data.', 'Correct reasoning (A1).', 1),
        ('Calculate the expected proportion of heterozygotes if the frequency of each allele were exactly 0.5.', '0.5 (50 %)', '2pq = 2 × 0.5 × 0.5 = 0.5 (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch10-st2', _hw_dq)


S('ch10-st3',
  terms=[('ecosystem stability', 'the ability of an ecosystem to remain unchanged over time or to return to its previous state after a disturbance'),
         ('tipping point', 'a critical threshold beyond which a small change causes a large, often irreversible, shift in an ecosystem'),
         ('resilience', 'the ability of an ecosystem to recover after a disturbance'),
         ('mesocosm', 'an enclosed experimental system, such as a sealed jar or pond enclosure, used to study ecological processes under controlled conditions'),
         ('eutrophication', 'enrichment of water with nutrients such as nitrates and phosphates, causing algal blooms and oxygen depletion'),
         ('biomagnification', 'the increase in concentration of a persistent pollutant at successive trophic levels in a food chain'),
         ('maximum sustainable yield', 'the largest catch that can be taken from a population each year without reducing its size in the long term'),
         ('keystone species', 'a species with a disproportionately large effect on community structure, whose removal destabilises the ecosystem')],
  facts=[('Which pesticide famously biomagnified and caused thinning of eggshells in birds of prey?', 'DDT', ['glyphosate', 'neonicotinoids', 'penicillin'], 'Rachel Carson’s Silent Spring.'),
         ('Which ecosystem is thought to be near a tipping point where it could turn into savanna?', 'the Amazon rainforest', ['the Sahara desert', 'the Antarctic ice sheet only', 'the Great Barrier Reef only'], 'Deforestation reduces rainfall.'),
         ('What causes the oxygen depletion in eutrophication?', 'aerobic decomposition of dead algae by bacteria', ['photosynthesis by algae', 'fish respiration only', 'evaporation'], 'Increased BOD.'),
         ('Which feature is typical of more stable ecosystems?', 'high biodiversity with complex food webs', ['one dominant species', 'very few trophic levels', 'frequent disturbance'], 'Alternative pathways.'),
         ('What is the main source of nitrates causing eutrophication?', 'run-off of agricultural fertilisers', ['volcanic ash', 'photosynthesis', 'rainwater only'], 'Also sewage.')],
  mc2=[('Why are ecosystems with high biodiversity often more stable?', 'Complex food webs provide alternative food sources if one species declines.', ['They have fewer interactions.', 'They have no predators.', 'Their species never change.'], 'Redundancy.'),
       ('Why does a persistent pesticide reach high concentrations in top predators?', 'It is not broken down or excreted and accumulates as predators eat many contaminated prey.', ['Predators produce it.', 'It is concentrated by photosynthesis.', 'It breaks down in prey.'], 'Biomagnification.'),
       ('Why can fishing above maximum sustainable yield cause a fishery to collapse?', 'More fish are removed than are replaced by reproduction, so the breeding stock declines.', ['Fish grow faster.', 'Nets become more efficient.', 'Fish migrate away permanently.'], 'Overexploitation.'),
       ('Why are mesocosms useful in ecological research?', 'Variables can be controlled and replicated, unlike in natural ecosystems.', ['They are identical to natural ecosystems.', 'They contain no organisms.', 'They prevent all change.'], 'Controlled experiments.')],
  mc3=[('DDT concentration in plankton is 0.04 ppm and in ospreys 25 ppm. What is the biomagnification factor?', '625', ['25', '0.0016', '62.5'], '25/0.04.'),
       ('After nitrate fertiliser run-off, a lake’s dissolved oxygen fell sharply. Which sequence explains this?', 'algal bloom → algae die → bacterial decomposition uses oxygen', ['fish increase → oxygen used → algae die', 'algae photosynthesise more → oxygen falls', 'nitrate reacts with oxygen directly'], 'Eutrophication.'),
       ('Cod in the Grand Banks collapsed in 1992 and have not fully recovered. What does this suggest?', 'A tipping point was crossed and the ecosystem shifted to a new stable state.', ['Cod recover immediately once fishing stops.', 'The ecosystem was unaffected.', 'Fishing had no effect.'], 'Alternative stable states.')],
  why=[('Explain what is meant by a tipping point, using the Amazon rainforest as an example.', 'A tipping point is a threshold beyond which positive feedback drives large change; Amazon trees recycle water through transpiration, producing rainfall; deforestation reduces transpiration and rainfall, causing drought, fires and more tree death; beyond about 20–25 % forest loss the region may shift to savanna.'),
       ('Explain how eutrophication affects aquatic ecosystems.', 'Nitrates and phosphates from fertilisers and sewage stimulate algal growth (bloom); algae block light, so submerged plants die; algae and plants die and are decomposed by aerobic bacteria; biochemical oxygen demand rises; oxygen falls; fish and invertebrates die; biodiversity decreases.'),
       ('Explain how biomagnification occurs and its effects.', 'Persistent, fat-soluble pollutants (DDT, mercury) are absorbed and stored in fatty tissue, not excreted; each consumer eats many organisms from the level below; concentration increases at each trophic level; top predators receive toxic doses, e.g. DDT caused thin eggshells in ospreys and peregrine falcons.')],
  contrast=[('stable ecosystems', 'unstable ecosystems', 'Stable ecosystems resist change and recover quickly after disturbance, typically with high biodiversity and complex food webs; unstable ecosystems change easily and may shift to a different state.'),
            ('bioaccumulation', 'biomagnification', 'Bioaccumulation is the build-up of a pollutant within an individual organism over time; biomagnification is the increase in concentration from one trophic level to the next.')],
  misc=[('Ecosystems always return to their original state after a disturbance.', 'If a tipping point is crossed, an ecosystem may shift to a different stable state.'),
        ('Adding nutrients to a lake always increases its biodiversity.', 'Excess nutrients cause eutrophication, oxygen depletion and loss of biodiversity.'),
        ('Pollutants are most concentrated in producers.', 'Persistent pollutants are most concentrated in top predators due to biomagnification.')],
  cases=[('collapse of the Grand Banks cod fishery', 'Overfishing led to a moratorium in 1992; cod populations remained low for decades.', 'tipping points and sustainability', 'Removing too many breeding fish pushed the ecosystem into a new state dominated by other species.'),
         ('DDT and birds of prey', 'Peregrine falcon and osprey populations crashed in the 1950s–60s and recovered after DDT bans.', 'biomagnification', 'DDT concentrated up the food chain, causing thin eggshells and breeding failure in top predators.'),
         ('sealed mesocosm bottles', 'Sealed jars containing water, plants, microorganisms and small animals can persist for months with only light entering.', 'ecosystem sustainability', 'Energy enters as light while nutrients are recycled by decomposers, showing requirements for a sustainable ecosystem.')],
  evaluate=[('Ecosystems are resilient enough to recover from any human disturbance.', ['many systems recover after pollution is reduced, e.g. birds of prey after DDT bans, rivers after clean-up'], ['tipping points such as cod collapse and coral reef shifts may be irreversible', 'combined stresses reduce resilience'], 'Ecosystems can be resilient, but beyond tipping points recovery may be impossible, so precautionary management is needed.')],
  extended=[('Explain the factors that affect the stability of ecosystems and evaluate the risk of tipping points.', 'Biodiversity, food web complexity, keystone species, nutrient cycling, energy input; resilience; positive feedback; tipping points: Amazon, coral reefs, cod; eutrophication; biomagnification; mesocosms; sustainable practices.', 8),
            ('Describe how human activities can affect the sustainability of ecosystems, using examples.', 'Overfishing and MSY; deforestation; eutrophication; biomagnification of DDT and mercury; invasive species; climate change; sustainable practices: quotas, buffer strips, protected areas.', 6)],
  )


@R.add('ch10-st3', 'C3', (1, 5), 'numerical')
def biomag_calc(rng, slot):
    chain = pick(rng, [['water', 'plankton', 'small fish', 'large fish', 'fish-eating birds'], ['water', 'algae', 'zooplankton', 'herring', 'seals']])
    c = [rng.uniform(0.00002, 0.0001)]
    for _ in chain[1:]:
        c.append(c[-1] * rng.uniform(5, 30))
    c = [float(f'{x:.2g}') for x in c]
    vals = [sf(x, 2) for x in c]
    f = c[-1] / c[1]
    stem = (f'The concentration of a persistent pesticide (ppm) in a food chain was: ' + ', '.join(f'{a} {b}' for a, b in zip(chain, vals)) +
            f'. Calculate the biomagnification factor from {chain[1]} to {chain[-1]}.')
    if slot.d >= 4:
        stem += ' Explain why the concentration increases along the food chain.'
        return num(stem, f'about {sf(f, 2)} times; the pesticide is persistent and fat-soluble, not excreted, and each consumer eats many organisms from the level below',
                   f'{vals[-1]}/{vals[1]} (M1) = {sf(f, 2)} (A1); persistence/storage in fat (R1); consumption of large biomass (R1).', 4)
    return num(stem, f'about {sf(f, 2)} times', f'{vals[-1]}/{vals[1]} (M1) = {sf(f, 2)} (A1).', 2)


def _eutro_dq(rng, slot):
    dist = [0, 100, 200, 400, 800, 1600]
    o2 = [round(x + rng.uniform(-0.3, 0.3), 1) for x in [9.2, 3.1, 2.4, 4.5, 7.2, 8.9]]
    nit = [round(x * rng.uniform(0.9, 1.1), 1) for x in [1.5, 14.0, 12.5, 8.0, 4.0, 2.0]]
    inv = [round(x * rng.uniform(0.85, 1.15)) for x in [12, 3, 2, 5, 9, 11]]
    intro = ('A river was sampled at intervals downstream of a point where run-off from fertilised farmland and a sewage outlet enter it (0 m is just upstream of the outlet).\n\n'
             + table(['Distance / m', 'Dissolved O₂ / mg dm⁻³', 'Nitrate / mg dm⁻³', 'Number of invertebrate taxa'], list(zip(dist, o2, nit, inv))))
    mn = dist[o2.index(min(o2))]
    p = pct_change(o2[0], min(o2))
    parts = [
        ('State the distance at which dissolved oxygen was lowest.', f'{mn} m', f'{mn} m (A1).', 1),
        ('Calculate the percentage decrease in dissolved oxygen from 0 m to its lowest value.', f'{signed(p)} %', f'({min(o2)} − {o2[0]})/{o2[0]} × 100 (M1) = {signed(p)} % (A1).', 2),
        ('Describe the relationship between nitrate concentration and the number of invertebrate taxa.', 'Negative: where nitrate is highest, fewest taxa are found; taxa recover as nitrate decreases downstream.', 'Negative relationship (A1); recovery downstream (A1).', 2),
        ('Explain why dissolved oxygen falls downstream of the outlet.', 'Nutrients cause algal growth; dead algae and organic sewage are decomposed by aerobic bacteria; high biochemical oxygen demand uses up oxygen.', 'Nutrients/algae (A1); decomposition (A1); BOD (A1).', 3),
        ('Explain why oxygen increases further downstream.', 'Nutrients and organic matter are diluted and used up; turbulence reoxygenates water; photosynthesis by plants.', 'Two reasons (A1 A1).', 2),
        ('Suggest why invertebrate taxa are used as indicators of water quality.', 'Different taxa have different oxygen tolerances; they integrate conditions over time and are easily sampled.', 'Valid reason (A1).', 1),
        ('Suggest one way farmers could reduce eutrophication.', 'Buffer strips of vegetation by rivers; apply fertiliser at appropriate times/amounts; use organic fertiliser; avoid spreading before rain.', 'Valid method (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch10-st3', _eutro_dq)


S('ch10-st4',
  terms=[('greenhouse effect', 'the warming of the Earth’s surface and lower atmosphere because greenhouse gases absorb and re-emit long-wave (infrared) radiation'),
         ('anthropogenic', 'caused by human activities'),
         ('greenhouse gas', 'a gas such as carbon dioxide, methane, nitrous oxide or water vapour that absorbs infrared radiation'),
         ('positive feedback (climate)', 'a process in which warming causes changes that cause further warming, such as melting ice reducing albedo or thawing permafrost releasing methane'),
         ('coral bleaching', 'loss of symbiotic zooxanthellae from corals when water is too warm, leaving the coral white and starving'),
         ('phenology', 'the timing of seasonal biological events such as flowering, leaf opening, migration and breeding'),
         ('range shift', 'a change in the geographical distribution of a species, e.g. towards the poles or higher altitudes as the climate warms'),
         ('ocean acidification', 'the decrease in ocean pH caused by absorption of atmospheric CO₂, reducing carbonate ions available for shell formation')],
  facts=[('Which greenhouse gas is produced by cattle and rice paddies?', 'methane', ['oxygen', 'nitrogen', 'argon'], 'From anaerobic microbes.'),
         ('By about how much has global mean surface temperature risen since pre-industrial times?', 'about 1.2 °C', ['about 0.1 °C', 'about 5 °C', 'about 10 °C'], 'IPCC estimates.'),
         ('Which radiation is absorbed by greenhouse gases?', 'long-wave infrared radiation', ['visible light only', 'ultraviolet only', 'gamma rays'], 'Re-emitted from Earth’s surface.'),
         ('What happens to corals when water temperature stays too high?', 'they expel zooxanthellae and bleach', ['they grow faster', 'they produce more calcium carbonate', 'they migrate'], 'Loss of mutualists.'),
         ('Which positive feedback involves sea ice?', 'melting ice exposes dark water, reducing albedo and increasing absorption of heat', ['ice reflects more light as it melts', 'ice releases oxygen', 'ice absorbs CO₂'], 'Albedo effect.')],
  mc2=[('Why does thawing permafrost accelerate climate change?', 'Decomposition of thawed organic matter releases CO₂ and methane, causing more warming.', ['Permafrost absorbs CO₂ when it melts.', 'It increases albedo.', 'It cools the oceans.'], 'Positive feedback.'),
       ('Why can earlier spring leaf opening cause problems for animals?', 'Food peaks may no longer match breeding times (phenological mismatch).', ['Leaves are toxic early.', 'Animals breed earlier than plants always.', 'It has no effect.'], 'e.g. great tits and caterpillars.'),
       ('Why do many species shift their ranges towards the poles?', 'Warming makes formerly cold areas suitable and lowers survival in warmer parts of their range.', ['Magnetic fields change.', 'Day length increases.', 'Predators move to the equator.'], 'Track suitable climate.'),
       ('Why does ocean acidification harm shelled organisms?', 'Lower pH reduces carbonate ion availability, making it harder to build calcium carbonate shells.', ['It increases carbonate.', 'Acid kills only fish.', 'It raises ocean temperature directly.'], 'Carbonate chemistry.')],
  mc3=[('Oak first leafing in a region advanced from day 120 in 1960 to day 108 in 2020. What is the mean rate of change?', '2 days earlier per decade', ['12 days per decade', '0.2 days per decade', '20 days per decade'], '12 days over 6 decades.'),
       ('The treeline on a mountain rose from 1850 m to 1940 m over 50 years. What is the mean rate?', '1.8 m per year', ['90 m per year', '18 m per year', '0.18 m per year'], '90/50.'),
       ('An Arctic species is restricted to tundra. Why is it particularly threatened by warming?', 'Its habitat shrinks as the treeline moves north, and it has nowhere colder to move to.', ['It can move to the equator.', 'Tundra is expanding.', 'Arctic species benefit from warming.'], 'Habitat loss.')],
  why=[('Explain the enhanced greenhouse effect.', 'Short-wave radiation from the Sun passes through the atmosphere and warms the surface; the surface emits long-wave infrared; greenhouse gases (CO₂, CH₄, N₂O, H₂O) absorb and re-emit it, warming the atmosphere; human activities (fossil fuel combustion, deforestation, agriculture) increase greenhouse gas concentrations, so more heat is retained.'),
       ('Explain how climate change affects ecosystems.', 'Range shifts poleward and upwards; changes in phenology causing mismatches between species; coral bleaching from warming and acidification; loss of polar habitats (sea ice) for polar bears and penguins; increased drought and fires; species unable to move face extinction; changes in community composition.'),
       ('Explain how positive feedback mechanisms can accelerate climate change.', 'Melting ice reduces albedo, so more heat is absorbed; thawing permafrost releases CO₂ and methane; warmer oceans absorb less CO₂; drought and fires release carbon from forests; each process causes further warming, possibly crossing tipping points.')],
  contrast=[('the natural greenhouse effect', 'the enhanced greenhouse effect', 'The natural greenhouse effect keeps the Earth about 33 °C warmer than it would be otherwise and is essential for life; the enhanced effect is the additional warming caused by human increases in greenhouse gas concentrations.'),
            ('mitigation', 'adaptation', 'Mitigation reduces the causes of climate change (cutting emissions, increasing sinks); adaptation reduces its impacts (sea walls, drought-resistant crops, conservation corridors).')],
  misc=[('The greenhouse effect is caused by the hole in the ozone layer.', 'Ozone depletion increases UV reaching the surface; the greenhouse effect is due to gases absorbing infrared.'),
        ('Climate change only affects temperature.', 'It also changes rainfall, sea level, ocean pH, extreme weather and the timing of biological events.'),
        ('All species will simply move to cooler areas.', 'Many species cannot disperse fast enough or have no suitable habitat to move to, and may go extinct.')],
  cases=[('coral bleaching on the Great Barrier Reef', 'Mass bleaching events in 2016, 2017, 2020, 2022 and 2024 affected large parts of the reef.', 'effects of climate change', 'Prolonged high sea temperatures cause corals to expel zooxanthellae, and repeated events prevent recovery.'),
         ('great tits and winter moth caterpillars in Wytham Woods', 'Oak leaves and caterpillars emerge earlier with warming, but great tits have advanced egg-laying less.', 'phenological mismatch', 'Chicks hatch after the caterpillar peak, reducing food and breeding success.'),
         ('melting Arctic sea ice', 'September Arctic sea-ice extent has declined by about 13 % per decade since 1979.', 'positive feedback', 'Loss of reflective ice exposes dark ocean that absorbs more heat, accelerating warming.')],
  evaluate=[('Ecosystems will be able to adapt to climate change without human help.', ['species have shifted ranges and phenology in response to past climate changes', 'some populations show rapid evolutionary change'], ['current change is much faster than past natural change', 'habitat fragmentation blocks movement; tipping points such as coral loss'], 'Some species will adapt, but the speed of change and habitat fragmentation mean many will not without conservation measures and emission cuts.')],
  extended=[('Explain the causes of anthropogenic climate change and its effects on ecosystems.', 'Greenhouse effect; CO₂ from fossil fuels and deforestation; methane from agriculture; Keeling curve; positive feedback (albedo, permafrost); effects: range shifts, phenology mismatch, coral bleaching, ocean acidification, polar habitats, extinction risk; mitigation and adaptation.', 8),
            ('Evaluate the evidence that climate change is affecting the timing of biological events.', 'Long-term records of first leafing, flowering, migration and breeding; trends of days per decade; correlation with spring temperature; experiments; mismatch examples; limitations: other factors, correlation vs causation.', 6)],
  )


def _phenology_dq(rng, slot):
    yrs = [1970, 1980, 1990, 2000, 2010, 2020]
    slope = -rng.uniform(0.18, 0.32)
    d0 = rng.randint(112, 122)
    days = [round(d0 + slope * (y - 1970) + rng.uniform(-2, 2)) for y in yrs]
    temp = [round(8.0 - (d - d0) * 0.18 + rng.uniform(-0.2, 0.2), 1) for d in days]
    r = pearson(temp, days)
    rate = (days[-1] - days[0]) / 5
    intro = ('Records of the mean first-leafing date of oak trees (day of year) and mean March–April temperature in a region are shown.\n\n'
             + table(['Year', 'First-leafing date / day', 'Mean March–April temperature / °C'], list(zip(yrs, days, temp))))
    parts = [
        ('State the first-leafing date in 1990.', f'day {days[2]}', f'{days[2]} (A1).', 1),
        ('Calculate the mean change in first-leafing date per decade between 1970 and 2020.', f'{rate:+.1f} days per decade', f'({days[-1]} − {days[0]})/5 (M1) = {rate:+.1f} days per decade (A1).', 2),
        ('Calculate the correlation coefficient between temperature and first-leafing date.', f'r = {r:.2f}', f'r = {r:.2f} (A1); calculator method (M1).', 2),
        ('Describe the relationship between spring temperature and first-leafing date.', 'Strong negative correlation: warmer springs are associated with earlier leafing.', 'Negative (A1); strong (A1).', 2),
        ('Suggest a biological explanation for the trend.', 'Leaf opening is triggered when accumulated warmth passes a threshold; warmer springs reach it earlier.', 'Temperature cue (A1).', 1),
        ('Explain how earlier leafing could affect insectivorous birds.', 'Caterpillars that feed on young leaves peak earlier; if birds do not breed earlier, chicks hatch after the food peak (mismatch), reducing survival.', 'Food peak shifts (A1); mismatch (A1).', 2),
        ('Evaluate the claim that these data prove climate change causes earlier leafing.', 'Strong correlation and plausible mechanism support it, but correlation does not prove causation; other factors (day length, CO₂, urban heat) may contribute; one region only.', 'Supporting point (A1); limitation (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch10-st4', _phenology_dq)

pct_items(R, 'ch10-st4', [
    ('The live coral cover on a reef changed from {a} % to {b} % after a marine heatwave.', '%', 30, 55, -0.6, -0.25, 0, 'high temperatures caused corals to expel zooxanthellae (bleaching); without their photosynthetic partners many corals died.'),
    ('The breeding population of an Arctic seabird changed from {a} pairs to {b} pairs over 30 years as sea ice declined.', 'pairs', 2000, 8000, -0.55, -0.2, 0, 'loss of sea ice reduced the populations of ice-associated prey such as Arctic cod, so less food was available.'),
    ('The mean elevation of a butterfly species’ range in the Pyrenees rose from {a} m to {b} m over 40 years.', 'm', 900, 1500, 0.1, 0.25, 0, 'warming made lower altitudes too hot and higher altitudes suitable, so the range shifted upwards.'),
])


# =============================================================================================
# ch11 Internal Assessment and practical skills
# =============================================================================================
S('ch11-st1',
  terms=[('eyepiece graticule', 'a scale in the eyepiece of a microscope, with arbitrary units, which must be calibrated against a stage micrometer'),
         ('stage micrometer', 'a microscope slide with an accurately ruled scale (often 1 mm divided into 100 divisions of 10 µm) used to calibrate an eyepiece graticule'),
         ('Rf value', 'in chromatography, the distance moved by a substance divided by the distance moved by the solvent front'),
         ('data logger', 'an electronic device that records measurements from sensors (e.g. O₂, CO₂, pH, temperature) at set intervals over time'),
         ('quadrat', 'a square frame of known area used to sample organisms in a habitat'),
         ('transect', 'a line across a habitat along which samples are taken at intervals to study changes with an environmental gradient'),
         ('resolution', 'the ability to distinguish two points close together as separate'),
         ('serial dilution', 'a stepwise dilution of a solution, usually by the same factor each time, to produce a range of concentrations')],
  facts=[('What is the length of one division on a typical stage micrometer?', '10 µm (0.01 mm)', ['1 mm', '1 µm', '100 µm'], '1 mm divided into 100.'),
         ('Which sensor would measure the rate of photosynthesis of pondweed with a data logger?', 'a dissolved oxygen probe', ['a pH probe only', 'a sound sensor', 'a light gate'], 'O₂ is produced.'),
         ('Why is a pencil used to draw the origin line in chromatography?', 'pencil graphite does not dissolve in the solvent', ['ink is too dark', 'pencil marks move with the solvent', 'pencil is cheaper'], 'Ink would run.'),
         ('What must be done when the objective lens is changed?', 'the eyepiece graticule must be recalibrated', ['the stage micrometer must be removed permanently', 'the eyepiece must be changed', 'nothing'], 'Magnification changes.'),
         ('Which method is best for sampling plant distribution across a sand dune system?', 'a belt or line transect', ['random quadrats only', 'capture–recapture', 'pitfall traps'], 'Environmental gradient.')],
  mc2=[('Why must an eyepiece graticule be calibrated?', 'Its divisions have no fixed size in the specimen plane; their value depends on the objective lens magnification.', ['It is always 1 µm per division.', 'It changes the magnification.', 'It measures colour.'], 'Calibration.'),
       ('Why are data loggers useful in investigations?', 'They record frequent, precise measurements over long periods without human error.', ['They always give accurate results regardless of calibration.', 'They replace controls.', 'They increase variation.'], 'Continuous data.'),
       ('Why is two-way chromatography sometimes used for photosynthetic pigments?', 'Pigments with similar Rf in one solvent separate in a second solvent.', ['It is faster.', 'It needs no solvent.', 'It removes chlorophyll.'], 'Better separation.'),
       ('Why should quadrat positions be chosen randomly when comparing two areas?', 'To avoid bias so that samples are representative and statistical tests are valid.', ['To find the most organisms.', 'To save time.', 'To avoid counting rare species.'], 'Reliability.')],
  mc3=[('An eyepiece graticule of 100 divisions aligns with 25 stage micrometer divisions (each 10 µm). What is one eyepiece division worth?', '2.5 µm', ['0.25 µm', '25 µm', '4 µm'], '250 µm/100 divisions.'),
       ('A cell measures 18 eyepiece divisions; each division is 2.5 µm. What is the cell’s length?', '45 µm', ['7.2 µm', '450 µm', '20.5 µm'], '18 × 2.5.'),
       ('A pigment spot moved 3.6 cm while the solvent front moved 8.0 cm. What is its Rf?', '0.45', ['2.2', '4.4', '0.36'], '3.6/8.0.')],
  why=[('Explain how to calibrate an eyepiece graticule and use it to measure a cell.', 'Place stage micrometer on the stage; line up graticule and micrometer scales; count how many micrometer divisions correspond to a number of graticule divisions; calculate the length of one graticule division (e.g. 25 × 10 µm/100 = 2.5 µm); replace with specimen; count graticule divisions across the cell; multiply.'),
       ('Explain how chromatography is used to separate and identify photosynthetic pigments.', 'Grind leaves with solvent to extract pigments; spot concentrated extract on origin line drawn in pencil; place in solvent below origin; solvent moves up carrying pigments at different rates depending on solubility and attraction to paper; measure distances; calculate Rf; compare with known values.'),
       ('Explain the advantages and limitations of using data loggers in biological investigations.', 'Advantages: high frequency of readings, long duration, precision, no reading errors, real-time graphs; limitations: need calibration, cost, probe drift, probe may disturb system, readings only as good as the sensor.')],
  contrast=[('line transects', 'belt transects', 'A line transect records organisms touching a line at intervals; a belt transect uses quadrats placed along the line, giving abundance data over a wider strip.'),
            ('magnification', 'resolution', 'Magnification is how many times larger the image is than the object; resolution is the ability to distinguish two points close together as separate.')],
  misc=[('Eyepiece graticule divisions are always 1 µm.', 'Their value depends on the objective lens and must be calibrated for each objective.'),
        ('Rf values can be greater than 1.', 'Substances cannot move further than the solvent front, so Rf is between 0 and 1.'),
        ('Data loggers make controls unnecessary.', 'They improve measurement, but controlled variables and controls are still needed for a valid experiment.')],
  cases=[('separating chloroplast pigments by thin-layer chromatography', 'Carotene runs near the solvent front, while chlorophyll b travels least.', 'chromatography', 'Different pigments have different solubilities and attraction to the stationary phase, giving different Rf values.'),
         ('using an oxygen probe with yeast in a sealed flask', 'The oxygen concentration falls steadily and then levels off as respiration becomes anaerobic.', 'data logging', 'Continuous readings show the rate of aerobic respiration and when oxygen becomes limiting.')],
  evaluate=[('Digital sensors and data loggers always give better data than manual methods.', ['many readings at precise intervals reduce random error', 'remove human reading errors'], ['probes must be calibrated and can drift', 'some measurements, such as identifying species, still need human skill'], 'Data loggers improve precision and quantity of data, but only when correctly calibrated and suited to the measurement.')],
  extended=[('Describe how microscopy, chromatography and sampling techniques are used in biological investigations, and explain how to ensure that data are reliable.', 'Graticule calibration, measurement, magnification; Rf; quadrats and transects; random sampling; data loggers; repeats; controls; calibration; sample size.', 8),
            ('Explain how to calculate the actual size and magnification of a specimen using an eyepiece graticule and a stage micrometer.', 'Calibration; value of one division; measurement in divisions; actual size; magnification = image/actual; scale bars; units µm and mm.', 6)],
  )


@R.add('ch11-st1', 'C3', (1, 5), 'numerical')
def graticule_cal(rng, slot):
    eg = pick(rng, [40, 50, 80, 100])
    sm = rng.randint(8, 40)
    val = sm * 10 / eg
    cell = rng.randint(6, 60)
    size = cell * val
    obj = pick(rng, ['×10', '×40'])
    stem = (f'Using the {obj} objective, {eg} eyepiece graticule divisions lined up with {sm} stage micrometer divisions (1 division = 10 µm). A cell measured {cell} eyepiece divisions. '
            'Calculate the value of one eyepiece division and the actual length of the cell.')
    if slot.d >= 4:
        img = round(rng.uniform(30, 90), 0)
        mag = img * 1000 / size
        stem += f' The cell is drawn {img:.0f} mm long. Calculate the magnification of the drawing.'
        return num(stem, f'{val:.2f} µm per division; {size:.1f} µm; ×{mag:.0f}',
                   f'{sm} × 10/{eg} = {val:.2f} µm (A1); {cell} × {val:.2f} = {size:.1f} µm (A1); {img:.0f} mm = {img * 1000:.0f} µm (M1); {img * 1000:.0f}/{size:.1f} = ×{mag:.0f} (A1).', 4)
    return num(stem, f'{val:.2f} µm per division; {size:.1f} µm', f'{sm} × 10 µm/{eg} (M1) = {val:.2f} µm (A1); {cell} × {val:.2f} = {size:.1f} µm (A1).', 3)


@R.add('ch11-st1', 'C3', (1, 4), 'mcq')
def rf_mcq(rng, slot):
    front = round(rng.uniform(6.0, 12.0), 1)
    d = round(front * rng.uniform(0.1, 0.95), 1)
    rf = d / front
    return nmcq(rng, f'In a chromatogram the solvent front moved {front} cm and a pigment moved {d} cm from the origin. What is the Rf value?', f'{rf:.2f}',
                [f'{front / d:.2f}', f'{front - d:.2f}', f'{1 - rf:.2f}', f'{rf * 10:.1f}'], f'Rf = {d}/{front} = {rf:.2f}.')


def _datalog_dq(rng, slot):
    t = [0, 2, 4, 6, 8, 10, 12]
    r = rng.uniform(0.35, 0.6)
    o0 = rng.uniform(8.5, 9.2)
    o2 = [round(max(1.2, o0 - r * x) if x <= 10 else max(1.2, o0 - r * 10) - 0.05, 2) for x in t]
    intro = ('An oxygen probe connected to a data logger recorded the dissolved oxygen concentration (mg dm⁻³) in a sealed flask containing germinating peas at 25 °C.\n\n'
             + table(['Time / min', 'Dissolved O₂ / mg dm⁻³'], list(zip(t, o2))))
    rate = (o2[0] - o2[5]) / 10
    parts = [
        ('State the oxygen concentration at 6 minutes.', f'{o2[3]} mg dm⁻³', f'{o2[3]} (A1).', 1),
        ('Calculate the mean rate of oxygen uptake between 0 and 10 minutes.', f'{rate:.3f} mg dm⁻³ min⁻¹', f'({o2[0]} − {o2[5]})/10 (M1) = {rate:.3f} (A1).', 2),
        ('Explain why oxygen concentration decreases.', 'The germinating peas respire aerobically, using oxygen as the final electron acceptor.', 'Aerobic respiration (A1).', 1),
        ('Suggest a suitable control for this experiment.', 'An identical flask with boiled (dead) peas or glass beads of the same volume.', 'Valid control (A1).', 1),
        ('State two advantages of using a data logger rather than manual readings.', 'More frequent readings; continuous record; higher precision; no reading errors; real-time graph.', 'Two advantages (A1 A1).', 2),
        ('Suggest how the probe should be prepared before use.', 'Calibrate it, e.g. in air-saturated water (and zero oxygen solution), and allow it to stabilise.', 'Calibration (A1).', 1),
        ('Predict the effect of carrying out the experiment at 15 °C and explain.', 'Slower decrease in oxygen because enzymes of respiration work more slowly at lower temperature.', 'Prediction (A1); explanation (A1).', 2),
        ('Suggest why the oxygen concentration levels off at the end of the recording.', 'Oxygen becomes too low to support aerobic respiration at the earlier rate, so the peas respire anaerobically and use little oxygen.', 'Oxygen limiting (A1); anaerobic respiration (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch11-st1', _datalog_dq)


S('ch11-st2',
  terms=[('research question', 'a focused, testable question that states the independent and dependent variables and the system being studied'),
         ('independent variable', 'the variable that is deliberately changed by the investigator'),
         ('dependent variable', 'the variable that is measured, which is expected to change in response to the independent variable'),
         ('controlled variable', 'a variable kept constant so that it does not affect the dependent variable'),
         ('control', 'an experimental condition used for comparison, in which the independent variable is absent or at a standard level'),
         ('hypothesis', 'a testable prediction of the relationship between variables, with a scientific explanation'),
         ('validity', 'the extent to which an investigation measures what it is intended to measure, with all other variables controlled'),
         ('repeatability', 'the closeness of results when the same investigator repeats a measurement under the same conditions')],
  facts=[('How many different values of the independent variable are generally recommended for an IA investigation showing a trend?', 'at least five', ['one', 'two', 'exactly three only'], 'To establish a relationship.'),
         ('In an investigation of the effect of temperature on catalase activity, what is the dependent variable?', 'the rate of oxygen production', ['temperature', 'volume of hydrogen peroxide', 'type of enzyme'], 'What is measured.'),
         ('Which is an ethical consideration in a biological investigation?', 'avoiding harm to animals and obtaining consent from human participants', ['using the cheapest equipment', 'collecting more data than needed', 'choosing a famous topic'], 'Ethics.'),
         ('What is the formula used to make dilutions?', 'C₁V₁ = C₂V₂', ['C₁ + V₁ = C₂ + V₂', 'C₁/V₁ = C₂V₂', 'V₁ = C₂/C₁'], 'Dilution equation.'),
         ('Why is a pilot study carried out?', 'to test and refine the method and choose a suitable range of values', ['to produce final results', 'to avoid repeats', 'to change the research question at the end'], 'Planning.')],
  mc2=[('Why must controlled variables be kept constant?', 'So that any change in the dependent variable can be attributed to the independent variable.', ['To increase variation.', 'To make the experiment faster.', 'Because they are dependent variables.'], 'Validity.'),
       ('Why are repeats carried out at each value of the independent variable?', 'To identify anomalies and calculate a mean, improving reliability.', ['To change the independent variable.', 'To avoid using controls.', 'To make results identical.'], 'Reliability.'),
       ('Why might a temperature-controlled water bath be used in an enzyme experiment?', 'Temperature affects enzyme activity, so it must be controlled to avoid confounding the results.', ['It speeds up the reaction always.', 'It measures pH.', 'It is the dependent variable.'], 'Control variable.'),
       ('Why is a focused research question important?', 'It defines exactly what will be changed, measured and in which system, guiding the method.', ['It guarantees a significant result.', 'It removes the need for a hypothesis.', 'It allows any variable to change.'], 'Clarity.')],
  mc3=[('To make 20 cm³ of 0.25 mol dm⁻³ sucrose from 1.0 mol dm⁻³ stock, what volume of stock is needed?', '5.0 cm³', ['4.0 cm³', '15 cm³', '0.25 cm³'], 'C₁V₁ = C₂V₂: V₁ = 0.25 × 20/1.0.'),
       ('A student investigates the effect of light intensity on stomatal opening but uses leaves from different plant species. Which aspect is weakened?', 'validity, because species is an uncontrolled variable', ['precision of the ruler', 'repeatability of light', 'the dependent variable'], 'Confounding variable.'),
       ('A 1 : 10 serial dilution of a 1 % starch solution is performed three times. What is the final concentration?', '0.001 %', ['0.01 %', '0.1 %', '0.0001 %'], '1 % ÷ 10³.')],
  why=[('Explain how to design a valid investigation into the effect of pH on the activity of an enzyme.', 'IV: pH using buffers at at least five values (e.g. 3–9); DV: rate (e.g. time for starch to disappear, O₂ volume per minute); controlled: temperature (water bath), enzyme and substrate concentration and volume, time; control without enzyme; at least three repeats; calculate means and SD.'),
       ('Explain the importance of risk assessment and ethics in biological investigations.', 'Identify hazards (chemicals, microorganisms, heat, sharp tools) and control measures (goggles, aseptic technique, lower temperatures); ethical issues: avoid harming animals, minimise disturbance to habitats, informed consent and anonymity for human subjects, safe disposal.'),
       ('Explain how a serial dilution is carried out and why it is useful.', 'Transfer a fixed volume of stock to a fixed volume of solvent, mix, and repeat using each new solution; gives a range of concentrations differing by a constant factor; useful for wide ranges (e.g. bacteria counts, standard curves) and accuracy.')],
  contrast=[('independent variables', 'dependent variables', 'The independent variable is changed by the investigator; the dependent variable is measured in response.'),
            ('a control', 'controlled variables', 'A control is a separate condition used for comparison (e.g. no enzyme); controlled variables are factors kept constant in all conditions.')],
  misc=[('A control experiment is the same as a controlled variable.', 'A control is a comparison condition; controlled variables are kept constant throughout.'),
        ('More decimal places always mean more accurate data.', 'Accuracy depends on closeness to the true value; decimal places should match the precision of the instrument.'),
        ('A hypothesis is just a guess.', 'A hypothesis is a testable prediction based on scientific reasoning.')],
  cases=[('an IA on the effect of caffeine on Daphnia heart rate', 'Daphnia are placed in caffeine solutions of different concentrations and heart rate is counted under a microscope.', 'designing a valid investigation', 'The temperature of water must be controlled and animals returned unharmed, showing control of variables and ethical practice.'),
         ('an IA on the effect of sucrose concentration on potato mass', 'Potato cylinders are placed in a range of sucrose solutions made by dilution of a 1 mol dm⁻³ stock.', 'use of C₁V₁ = C₂V₂ and controlled variables', 'Accurate dilutions and equal cylinder size, time and temperature allow a valid estimate of the isotonic point.')],
  evaluate=[('Laboratory experiments are more useful than field investigations in biology.', ['variables can be controlled, so causal relationships can be established', 'easier to replicate'], ['field studies are more realistic and show natural interactions', 'some questions (e.g. ecology) cannot be studied in the lab'], 'Both are needed: laboratory experiments establish causes, while field investigations test whether these apply in natural conditions.')],
  extended=[('Describe how to plan a scientific investigation in biology, including variables, method, safety and ethics.', 'Research question; background and hypothesis; IV with range and intervals; DV and method of measurement; controlled variables and how; control; repeats; pilot study; data table; risk assessment; ethical and environmental considerations; statistical analysis planned.', 8),
            ('Explain how the reliability and validity of an investigation can be improved.', 'Repeats and means; SD; larger sample; precise instruments; control of variables; controls; randomisation; blind trials; calibration; avoiding systematic errors.', 6)],
  )


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def dilution_calc(rng, slot):
    sub, unit = pick(rng, [('sucrose', 'mol dm⁻³'), ('glucose', 'mol dm⁻³'), ('hydrogen peroxide', '%'), ('sodium chloride', 'mol dm⁻³'), ('caffeine', 'mg cm⁻³')])
    stock = pick(rng, [1.0, 2.0, 5.0, 10.0])
    final_v = pick(rng, [10, 20, 25, 50, 100])
    targets = sorted({round(stock * f, 3) for f in rng.sample([0.05, 0.1, 0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8], 4)})
    rows = []
    for c in targets:
        v1 = c * final_v / stock
        rows.append(f'{c:g} {unit}: {v1:g} cm³ stock + {final_v - v1:g} cm³ water')
    stem = (f'A student has a {stock:g} {unit} stock solution of {sub}. Calculate the volumes of stock and distilled water needed to make {final_v} cm³ of each of: ' + ', '.join(f'{c:g}' for c in targets) + f' {unit}.')
    return num(stem, '; '.join(rows), f'C₁V₁ = C₂V₂, so V₁ = C₂V₂/C₁ (M1); ' + '; '.join(rows) + ' (A1 for each two correct, max A2).', 3, type='short')


@R.add('ch11-st2', 'C3', (1, 4), 'mcq')
def variable_mcq(rng, slot):
    inv = pick(rng, [
        ('the effect of temperature on the rate of respiration of yeast, measured by CO₂ bubbles per minute', 'temperature', 'number of CO₂ bubbles per minute', ['mass of yeast', 'glucose concentration', 'volume of solution']),
        ('the effect of light intensity on the rate of photosynthesis of Elodea, measured by O₂ volume per minute', 'light intensity', 'volume of O₂ produced per minute', ['temperature of the water', 'length of Elodea', 'NaHCO₃ concentration']),
        ('the effect of sucrose concentration on the change in mass of beetroot discs', 'sucrose concentration', 'percentage change in mass', ['disc size', 'time in solution', 'temperature']),
        ('the effect of caffeine concentration on the heart rate of Daphnia', 'caffeine concentration', 'heart rate (beats per minute)', ['water temperature', 'size of Daphnia', 'time of acclimatisation']),
    ])
    what, iv, dv, cvs = inv
    k = rng.randrange(3)
    if k == 0:
        return nmcq(rng, f'In an investigation of {what}, what is the independent variable?', iv, [dv] + cvs[:2], f'The independent variable is the factor deliberately changed: {iv}.')
    if k == 1:
        return nmcq(rng, f'In an investigation of {what}, what is the dependent variable?', dv, [iv] + cvs[:2], f'The dependent variable is what is measured: {dv}.')
    c = pick(rng, cvs)
    return nmcq(rng, f'In an investigation of {what}, which of these should be a controlled variable?', c, [iv, dv, 'the colour of the student’s pen'], f'{c} could affect the dependent variable, so it must be kept constant.')


S('ch11-st3',
  terms=[('mean', 'the sum of all values divided by the number of values'),
         ('standard deviation', 'a measure of the spread of values around the mean; about 68 % of values in a normal distribution lie within ±1 SD'),
         ('t-test', 'a statistical test used to determine whether the difference between the means of two samples is significant'),
         ('correlation coefficient (r)', 'a value between −1 and +1 that measures the strength and direction of a linear relationship between two variables'),
         ('null hypothesis', 'the hypothesis that there is no significant difference or relationship; it is rejected if p < 0.05'),
         ('significance level', 'the probability (usually 0.05) below which a result is considered unlikely to be due to chance'),
         ('error bars', 'lines on a graph showing variability (e.g. ±1 SD or range) of the data at each point'),
         ('coefficient of determination (r²)', 'the proportion of the variation in one variable that is explained by its linear relationship with the other')],
  facts=[('What value of p is usually taken as the threshold for significance in biology?', '0.05', ['0.5', '0.95', '5'], '5 % probability that results are due to chance.'),
         ('Which test compares the means of two independent samples?', 'the t-test', ['the chi-squared test', 'the Lincoln index', 'Simpson’s index'], 'Requires approximately normal data.'),
         ('What does r = −0.92 indicate?', 'a strong negative correlation', ['a weak positive correlation', 'no correlation', 'causation'], 'Close to −1.'),
         ('How many degrees of freedom are used in a t-test comparing two samples of 8?', '14', ['16', '7', '8'], 'n₁ + n₂ − 2.'),
         ('What do overlapping SD error bars suggest?', 'the difference between means may not be significant', ['the difference is definitely significant', 'the data are invalid', 'there is a correlation'], 'A t-test is needed.')],
  mc2=[('Why is the standard deviation more useful than the range?', 'It uses all the data and is less affected by a single extreme value.', ['It is always smaller.', 'It ignores most data.', 'It shows the mean.'], 'Spread measure.'),
       ('Why does a strong correlation not prove a causal relationship?', 'Another factor could cause both, or the relationship may be coincidental.', ['Correlations are always causal.', 'r is always zero for causes.', 'Correlation requires an experiment.'], 'Correlation ≠ causation.'),
       ('Why is a t-test used rather than simply comparing two means?', 'Differences may be due to chance variation; the t-test shows whether the difference is significant.', ['It calculates the mean.', 'It shows correlation.', 'It avoids repeats.'], 'Statistical inference.'),
       ('Why does a larger sample size usually improve confidence in a result?', 'Random variation has less effect on the mean, so it is a better estimate of the population mean.', ['It increases SD.', 'It removes all error.', 'It changes the hypothesis.'], 'Reduced sampling error.')],
  mc3=[('A t-test gives t = 3.1 with 10 degrees of freedom. The critical value at p = 0.05 is 2.23. What is concluded?', 'The difference is significant; reject the null hypothesis.', ['There is no significant difference.', 'The data are correlated.', 'The test is invalid.'], 't > critical.'),
       ('Values 4, 6, 7, 9, 9 have a mean of 7. What is the sample standard deviation (to 2 d.p.)?', '2.12', ['1.90', '4.50', '2.00'], 'Σ(x − x̄)² = 18; √(18/4).'),
       ('r = 0.6 between two variables. What proportion of the variation in y is explained by x?', '36 %', ['60 %', '6 %', '77 %'], 'r² = 0.36.')],
  why=[('Explain how a t-test is used to compare two sets of data.', 'State null hypothesis (no significant difference between means); calculate means and SDs; calculate t; degrees of freedom = n₁ + n₂ − 2; compare with critical value at p = 0.05; if t > critical value reject H₀ — the difference is significant; assumptions: approximately normal data, similar variance, independent samples.'),
       ('Explain how the standard deviation is used to describe and compare data sets.', 'SD measures spread around the mean; small SD means data are clustered and reliable; about 68 % within ±1 SD, 95 % within ±2 SD; error bars of ±1 SD on graphs; overlapping error bars suggest a difference may not be significant; a t-test is needed to confirm.'),
       ('Explain how correlation is assessed and interpreted.', 'Plot a scatter graph; calculate Pearson r (−1 to +1); sign shows direction, magnitude shows strength; r² shows proportion of variation explained; significance depends on sample size; correlation does not prove causation; experiments are needed to establish cause.')],
  contrast=[('correlation', 'causation', 'Correlation means two variables change together; causation means a change in one variable directly produces a change in the other, which requires experimental evidence.'),
            ('the t-test', 'the chi-squared test', 'The t-test compares the means of two samples of continuous data; the chi-squared test compares observed and expected frequencies of categorical data.')],
  misc=[('If two error bars overlap, the difference is definitely not significant.', 'Overlap suggests it may not be significant, but a statistical test is needed to decide.'),
        ('A significant result proves the hypothesis.', 'It shows the null hypothesis is unlikely; it supports but does not prove the hypothesis.'),
        ('r = 0 means there is no relationship at all.', 'r = 0 means no linear relationship; a non-linear relationship may still exist.')],
  cases=[('comparing stomatal density on sun and shade leaves', 'Students counted stomata on 10 leaves of each type and used a t-test to compare means.', 'the t-test', 'A t value greater than the critical value showed that sun leaves have significantly more stomata.'),
         ('smoking and lung cancer studies in the 1950s', 'Doll and Hill found a strong positive correlation between smoking and lung cancer.', 'correlation and causation', 'Correlation alone did not prove causation, but consistency, dose–response and biological mechanisms later established causation.')],
  evaluate=[('Statistical tests are essential in every biological investigation.', ['they distinguish real effects from chance variation', 'allow objective conclusions'], ['qualitative investigations or very large effects may not need them', 'tests can be misused if assumptions are not met'], 'Statistical tests are essential when conclusions depend on comparing variable data, but they must be chosen and interpreted correctly.')],
  extended=[('Explain how statistical analysis is used to draw conclusions from biological data, with reference to standard deviation, the t-test and correlation.', 'Mean; SD and error bars; normal distribution; t-test: null hypothesis, df, critical value, conclusion; correlation: r, r², scatter graphs; correlation vs causation; sample size; significance level.', 8),
            ('Explain the choice of statistical test for different types of biological data.', 'Continuous data, two groups → t-test; categorical frequencies → chi-squared; relationship between two continuous variables → correlation; diversity → Simpson’s index; assumptions of each.', 6)],
  )


T_CTX = [('stomatal density (stomata mm⁻²) of sun and shade leaves of the same tree', 'sun leaves', 'shade leaves', 140, 100, 15, 0),
         ('length (mm) of limpet shells on exposed and sheltered rocky shores', 'exposed shore', 'sheltered shore', 32, 38, 3.5, 1),
         ('heart rate (beats min⁻¹) of Daphnia in pond water and in 1 % caffeine', 'caffeine', 'pond water', 330, 290, 25, 0),
         ('mass (g) of tomatoes grown with and without added fertiliser', 'fertiliser', 'no fertiliser', 95, 80, 10, 1),
         ('reaction time (ms) of students before and after a sleepless night (different students)', 'after no sleep', 'well rested', 290, 250, 25, 0)]


def _t_data(rng):
    what, a, b, ma, mb, s, k = pick(rng, T_CTX)
    n = pick(rng, [6, 7, 8])
    if rng.random() < 0.3:
        mb = ma + (mb - ma) * 0.3
    xa = [round(rng.gauss(ma, s), k) for _ in range(n)]
    xb = [round(rng.gauss(mb, s), k) for _ in range(n)]
    return what, a, b, xa, xb, k


@R.add('ch11-st3', 'C3', (2, 5), 'numerical')
def ttest_calc(rng, slot):
    what, a, b, xa, xb, k = _t_data(rng)
    n = len(xa)
    t = abs(pooled_t(xa, xb))
    dfree = 2 * n - 2
    crit = T_CRIT[dfree]
    sig = t > crit
    stem = (f'A student measured the {what}. {a.capitalize()}: {", ".join(f"{x:.{k}f}" for x in xa)}. {b.capitalize()}: {", ".join(f"{x:.{k}f}" for x in xb)}. '
            f'Calculate the mean and standard deviation of each sample. A t-test gives t = {t:.2f}; the critical value for {dfree} degrees of freedom at p = 0.05 is {crit}. State a conclusion.')
    return num(stem, f'{a}: mean {mean(xa):.{k + 1}f}, SD {sd(xa):.{k + 1}f}; {b}: mean {mean(xb):.{k + 1}f}, SD {sd(xb):.{k + 1}f}; ' +
               ('t > critical value – significant difference, reject H₀' if sig else 't < critical value – no significant difference, accept H₀'),
               f'Means (A1); SDs (A1); comparison of {t:.2f} with {crit} (M1); correct conclusion about H₀ (A1).', 4)


@R.add('ch11-st3', 'C3', (2, 5), 'numerical')
def corr_calc(rng, slot):
    ctx = pick(rng, [('light intensity (lux) and number of plant species in quadrats', 'light', 'species', 200, 1200, 0.006, 3),
                     ('soil moisture (%) and percentage cover of moss', 'moisture', 'moss cover', 10, 60, 1.2, 8),
                     ('distance from a road (m) and lichen species per tree', 'distance', 'lichen species', 10, 200, 0.03, 1.5)])
    what, xn, yn, lo, hi, slope, noise = ctx
    n = 7
    xs = sorted(round(rng.uniform(lo, hi)) for _ in range(n))
    ys = [max(0, round(slope * x + rng.gauss(0, noise) + 2)) for x in xs]
    if len(set(ys)) < 3:
        return None
    r = pearson(xs, ys)
    stem = f'A student recorded {what}: ' + '; '.join(f'({x}, {y})' for x, y in zip(xs, ys)) + '. Calculate Pearson’s correlation coefficient r and r², and interpret the result.'
    strength = 'strong' if abs(r) >= 0.7 else 'moderate' if abs(r) >= 0.4 else 'weak'
    return num(stem, f'r = {r:.2f}; r² = {r * r:.2f}; {strength} {"positive" if r > 0 else "negative"} correlation – {r * r * 100:.0f} % of variation explained; does not prove causation',
               f'r = {r:.2f} (A1); r² = {r * r:.2f} (A1); interpretation of strength/direction (A1); correlation ≠ causation (R1).', 4)


def _ttest_dq(rng, slot):
    what, a, b, xa, xb, k = _t_data(rng)
    n = len(xa)
    t = abs(pooled_t(xa, xb))
    dfree = 2 * n - 2
    crit = T_CRIT[dfree]
    sig = t > crit
    intro = (f'A student measured the {what}.\n\n' + table(['Sample', a, b], [(i + 1, f'{x:.{k}f}', f'{y:.{k}f}') for i, (x, y) in enumerate(zip(xa, xb))]))
    parts = [
        (f'Calculate the mean for {a}.', f'{mean(xa):.{k + 1}f}', f'Σx/n = {sum(xa):.{k}f}/{n} = {mean(xa):.{k + 1}f} (A1).', 1),
        ('Calculate the standard deviation of each sample.', f'{a} {sd(xa):.{k + 1}f}; {b} {sd(xb):.{k + 1}f}', f'Sample SD: {sd(xa):.{k + 1}f} (A1); {sd(xb):.{k + 1}f} (A1).', 2),
        ('State a null hypothesis for a t-test on these data.', f'There is no significant difference between the mean for {a} and the mean for {b}.', 'H₀ (A1).', 1),
        (f'A t-test gives t = {t:.2f}. Determine the degrees of freedom and, using a critical value of {crit} at p = 0.05, state a conclusion.', f'df = {dfree}; ' + ('t > critical value – reject H₀; significant difference' if sig else 't < critical value – accept H₀; no significant difference'),
         f'df = {n} + {n} − 2 = {dfree} (A1); comparison and conclusion (A1).', 2),
        ('Explain why standard deviation is useful when comparing these samples.', 'It shows the spread of each sample; large overlap of mean ± SD suggests the difference may not be significant; indicates reliability of the means.', 'Spread (A1); link to overlap/reliability (A1).', 2),
        ('Suggest how the investigation could be improved to give more confidence in the conclusion.', 'Increase sample size; random sampling; control other variables; repeat at different times/sites.', 'Two improvements (A1 A1).', 2),
        ('State one assumption of the t-test.', 'Data are approximately normally distributed / samples independent / similar variances.', 'Valid assumption (A1).', 1),
        ('Explain why the sample standard deviation (dividing by n − 1) is used.', 'The data are a sample from a larger population; dividing by n − 1 gives an unbiased estimate of the population standard deviation.', 'Sample, not population (A1); unbiased estimate (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch11-st3', _ttest_dq)

mean_sd_items(R, 'ch11-st3', [
    ('timed how long a starch–amylase mixture took to stop giving a blue-black colour with iodine in repeated trials.', 'time', 's', 60, 180, 0.08, 0),
    ('counted the number of bubbles released per minute by a pondweed in repeated trials.', 'bubble count', 'bubbles min⁻¹', 15, 40, 0.1, 0),
    ('measured the diameter of the zone of inhibition around a garlic-extract disc on replicate plates.', 'zone diameter', 'mm', 8, 20, 0.12, 1),
    ('measured the length of root tips grown for 5 days in replicate Petri dishes.', 'root length', 'mm', 15, 40, 0.15, 1),
])


S('ch11-st4',
  terms=[('random error', 'unpredictable variation in measurements that causes results to scatter around the true value; reduced by repeats'),
         ('systematic error', 'a consistent error in the same direction in all measurements, such as an uncalibrated instrument; not reduced by repeats'),
         ('percentage uncertainty', 'the absolute uncertainty divided by the measured value, multiplied by 100'),
         ('accuracy', 'how close a measurement is to the true value'),
         ('precision', 'how close repeated measurements are to each other'),
         ('anomalous result', 'a result that does not fit the pattern of the other results and may be due to error'),
         ('limitation', 'a weakness in the method that affects the reliability or validity of the conclusion'),
         ('extension', 'a suggested further investigation that builds on the findings of the original one')],
  facts=[('What is the uncertainty of a 10 cm³ measuring cylinder with 0.2 cm³ graduations, using half the smallest division?', '±0.1 cm³', ['±0.2 cm³', '±1 cm³', '±0.01 cm³'], 'Half the smallest division for analogue scales.'),
         ('Which type of error is reduced by taking repeats?', 'random error', ['systematic error', 'zero error', 'calibration error'], 'Mean is more reliable.'),
         ('Which section of the IA discusses strengths and weaknesses of the method?', 'evaluation', ['research design', 'data collection only', 'title page'], 'Includes improvements.'),
         ('What should be done with an anomalous result?', 'identify it, repeat if possible and consider excluding it from the mean with justification', ['delete it without comment', 'always include it in the mean', 'change it to fit the trend'], 'Transparency.'),
         ('Which is an example of a systematic error?', 'a balance that reads 0.05 g when empty', ['variation in reaction time when stopping a stopwatch', 'natural variation between leaves', 'occasional misreading of a scale'], 'Consistent offset.')],
  mc2=[('Why does using a larger quantity reduce percentage uncertainty?', 'The absolute uncertainty stays the same while the measured value increases.', ['Absolute uncertainty decreases.', 'Larger quantities have no uncertainty.', 'It increases accuracy of the instrument.'], '%U = U/value × 100.'),
       ('Why should a conclusion refer to the research question and the data?', 'It must answer the question using the trends and statistics obtained, supported by scientific explanation.', ['It should introduce new data.', 'It should avoid mentioning results.', 'It should only state the hypothesis.'], 'Evidence-based.'),
       ('Why is it important to suggest realistic improvements in an evaluation?', 'Improvements should address the identified limitations and be practical within the investigation.', ['To make the report longer.', 'To change the research question.', 'Because examiners prefer expensive equipment.'], 'Link to weaknesses.'),
       ('Why can results be precise but not accurate?', 'Repeated readings can agree closely but all be shifted from the true value by a systematic error.', ['Precise results are always accurate.', 'Accuracy depends on repeats only.', 'Precision means closeness to the true value.'], 'Systematic error.')],
  mc3=[('A stopwatch reading of 25.0 s has an uncertainty of ±0.5 s (reaction time). What is the percentage uncertainty?', '2 %', ['0.5 %', '5 %', '20 %'], '0.5/25.0 × 100.'),
       ('A student measures 5.0 cm³ with a pipette of uncertainty ±0.1 cm³ and adds it to 20.0 cm³ measured with uncertainty ±0.2 cm³. What is the absolute uncertainty of the total volume?', '±0.3 cm³', ['±0.1 cm³', '±0.2 cm³', '±0.02 cm³'], 'Add absolute uncertainties.'),
       ('Results for 40 °C show times of 22, 24 and 61 s. What should the student do?', 'Treat 61 s as anomalous, repeat the trial and calculate the mean of the consistent values with justification.', ['Include all three in the mean without comment.', 'Change 61 to 23.', 'Discard all the 40 °C results.'], 'Handle anomalies transparently.')],
  why=[('Explain how to write an effective conclusion for an IA.', 'State the relationship found between IV and DV, with reference to processed data (means, trends, statistical test results); state whether the hypothesis is supported; explain the trend using scientific theory; compare with published values; acknowledge uncertainty and the limits of the conclusion.'),
       ('Explain the difference between random and systematic errors and how each can be reduced.', 'Random errors vary unpredictably and scatter results; reduced by repeats, larger samples and more precise instruments; systematic errors shift all results in one direction, e.g. uncalibrated instruments or consistent technique errors; reduced by calibration and better method, not by repeats.'),
       ('Explain how to evaluate the method of an investigation.', 'Identify strengths and weaknesses (limitations) such as uncontrolled variables, measurement uncertainty, sample size and range; explain their effect on the data; suggest specific, realistic improvements; propose extensions that address unanswered questions.')],
  contrast=[('accuracy', 'precision', 'Accuracy is how close a measurement is to the true value; precision is how close repeated measurements are to each other.'),
            ('random errors', 'systematic errors', 'Random errors cause unpredictable scatter and are reduced by repeats; systematic errors shift all readings by the same amount and are reduced only by calibration or a better method.')],
  misc=[('Taking more repeats removes systematic error.', 'Repeats reduce random error; systematic error remains unless the instrument or method is corrected.'),
        ('Human error is a sufficient explanation of a limitation.', 'Limitations should be specific, e.g. difficulty judging the end-point colour, and linked to their effect on data.'),
        ('A conclusion should claim that the hypothesis has been proven.', 'Data can support or refute a hypothesis, but not prove it.')],
  cases=[('an IA on the effect of temperature on lipase activity using phenolphthalein', 'Students found it difficult to judge exactly when the pink colour disappeared.', 'evaluating limitations', 'Subjective end-points introduce random error; a pH probe or colorimeter would improve precision.'),
         ('measuring oxygen production by pondweed using bubble counts', 'Bubbles varied in size and some oxygen dissolved in the water.', 'systematic and random errors', 'Counting bubbles underestimates and varies; collecting gas in a syringe or using an O₂ probe gives more accurate data.')],
  evaluate=[('The evaluation is the most important section of an IA report.', ['shows understanding of the reliability and validity of the data', 'improvements and extensions show scientific thinking'], ['without a sound research design and analysis there is nothing worth evaluating', 'all criteria contribute to the final mark'], 'The evaluation is important, but it depends on good design and analysis; all sections are interdependent.')],
  extended=[('Explain how the analysis, conclusion and evaluation sections of a biology IA should be written.', 'Processing raw data (means, SD, rates, % change); graphs with error bars; statistical tests; uncertainty propagation; conclusion linked to RQ, hypothesis and theory; evaluation: strengths, limitations with effects, realistic improvements, extensions.', 8),
            ('Explain how measurement uncertainties are estimated and propagated in biological investigations.', 'Instrument resolution; half smallest division for analogue; reading/reaction time; absolute and percentage uncertainty; adding absolute for sums; adding percentage for products/quotients; reporting to appropriate significant figures.', 6)],
  )


@R.add('ch11-st4', 'C3', (1, 5), 'numerical')
def pct_uncert(rng, slot):
    inst, u, lo, hi, unit, k = pick(rng, [('a measuring cylinder', 0.5, 10, 50, 'cm³', 1), ('a stopwatch (allowing for reaction time)', 0.3, 15, 120, 's', 1),
                                         ('a balance', 0.01, 0.5, 5.0, 'g', 2), ('a ruler', 0.5, 15, 80, 'mm', 0), ('a thermometer', 0.5, 20, 60, '°C', 1)])
    v = round(rng.uniform(lo, hi), k)
    p = 100 * u / v
    stem = f'A value of {v:.{k}f} {unit} was measured with {inst} with an uncertainty of ±{u:g} {unit}. Calculate the percentage uncertainty.'
    if slot.d >= 4:
        v2 = round(v * pick(rng, [2, 3, 4]), k)
        p2 = 100 * u / v2
        stem += f' Calculate the percentage uncertainty if {v2:.{k}f} {unit} were measured instead, and comment.'
        return num(stem, f'{p:.1f} %; {p2:.1f} %; measuring a larger quantity reduces percentage uncertainty',
                   f'{u:g}/{v:.{k}f} × 100 = {p:.1f} % (A1); {u:g}/{v2:.{k}f} × 100 = {p2:.1f} % (A1); comment (R1).', 3)
    return num(stem, f'{p:.1f} %', f'{u:g}/{v:.{k}f} × 100 (M1) = {p:.1f} % (A1).', 2)


@R.add('ch11-st4', 'C3', (2, 5), 'numerical')
def anomaly_q(rng, slot):
    base = rng.uniform(20, 80)
    vals = [round(base * rng.uniform(0.95, 1.05), 1) for _ in range(4)]
    an = round(base * pick(rng, [1.6, 1.8, 0.5, 0.4]), 1)
    i = rng.randrange(5)
    vals.insert(i, an)
    good = [x for x in vals if x != an]
    m_all, m_good = mean(vals), mean(good)
    stem = (f'Five repeat measurements of the time (s) for a colour change were: {", ".join(f"{x:.1f}" for x in vals)}. Identify the anomalous result, and calculate the mean with and without it. '
            'State which mean should be used and why.')
    return num(stem, f'anomaly {an:.1f} s; mean with it {m_all:.1f} s, without it {m_good:.1f} s; use {m_good:.1f} s because the anomaly does not fit the pattern and is likely due to error (repeat if possible)',
               f'Anomaly identified (A1); means {m_all:.1f} and {m_good:.1f} (A1); justification (R1).', 3)


def _uncert_dq(rng, slot):
    temps = [20, 30, 40, 50, 60]
    times = []
    for tt in temps:
        mu = {20: 180, 30: 95, 40: 52, 50: 70, 60: 160}[tt] * rng.uniform(0.9, 1.1)
        times.append([round(rng.gauss(mu, mu * 0.06)) for _ in range(3)])
    means = [mean(t) for t in times]
    rates = [1000 / m for m in means]
    u = 0.5
    j = 2
    intro = ('A student investigated the effect of temperature on the time taken for amylase to digest starch (iodine end-point). Each temperature was tested three times. The stopwatch uncertainty is ±0.5 s.\n\n'
             + table(['Temperature / °C', 'Trial 1 / s', 'Trial 2 / s', 'Trial 3 / s', 'Mean / s'], [(tt, *t, '?' if i == j else f'{m:.1f}') for i, (tt, t, m) in enumerate(zip(temps, times, means))]))
    pu = 100 * u / means[j]
    best = temps[means.index(min(means))]
    parts = [
        (f'Calculate the mean time at {temps[j]} °C.', f'{means[j]:.1f} s', f'{sum(times[j])}/3 = {means[j]:.1f} (A1).', 1),
        (f'Calculate the rate (1000/mean time) at {temps[j]} °C and at 20 °C.', f'{rates[j]:.1f} and {rates[0]:.1f} s⁻¹', f'1000/{means[j]:.1f} = {rates[j]:.1f} (A1); 1000/{means[0]:.1f} = {rates[0]:.1f} (A1).', 2),
        (f'Calculate the percentage uncertainty in the mean time at {temps[j]} °C due to the stopwatch.', f'{pu:.1f} %', f'0.5/{means[j]:.1f} × 100 = {pu:.1f} % (A1).', 1),
        ('State a conclusion from these data.', f'Rate increases with temperature up to about {best} °C (optimum), then decreases at higher temperatures.', 'Increase to optimum (A1); decrease above (A1).', 2),
        ('Explain the decrease in rate at the highest temperatures.', 'The enzyme denatures: bonds holding the tertiary structure break, the active site changes shape and fewer enzyme–substrate complexes form.', 'Denaturation (A1); active site shape (A1).', 2),
        ('Identify one limitation of the iodine end-point method and suggest an improvement.', 'Judging the end-point colour is subjective; use a colorimeter to measure absorbance at fixed times, or sample more frequently.', 'Limitation (A1); improvement (A1).', 2),
        ('Suggest why the uncertainty from the stopwatch is not the main source of error.', 'Variation between trials (random error from end-point judgement and sampling intervals) is much larger than ±0.5 s.', 'Comparison with trial variation (A1).', 1),
        ('Identify the optimum temperature from these data and suggest how it could be found more precisely.', f'about {best} °C; test smaller intervals (e.g. every 2 °C) between {best - 10} and {best + 10} °C.', 'Optimum from data (A1); smaller intervals around it (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch11-st4', _uncert_dq)


# =============================================================================================
# Additional Paper 1A items (C2 understanding, C3 application) – widen the MCQ pool for six mocks
# =============================================================================================
MORE_MCQ = {
 'ch01-st1': (
    [('Why does an enzyme catalyse only one type of reaction?', 'Its active site is complementary in shape and chemistry to one specific substrate.', ['It is used up in the reaction.', 'It contains many different active sites.', 'It changes the equilibrium of the reaction.'], 'Specificity.'),
     ('Why is the induced-fit model considered better than the lock-and-key model?', 'It explains how the active site changes shape slightly on binding, stressing bonds in the substrate.', ['It shows enzymes are rigid.', 'It shows the substrate changes the enzyme permanently.', 'It shows enzymes have no active site.'], 'Flexible active site.')],
    [('An enzyme from a thermophilic bacterium still works at 80 °C. Which explanation is most likely?', 'Its tertiary structure is stabilised by more bonds (e.g. disulfide bridges), so it does not denature.', ['It has no active site.', 'It is not a protein.', 'Its substrate does not move.'], 'Thermostable enzymes.'),
     ('Immobilised lactase is used to make lactose-free milk. What is an advantage of immobilising the enzyme?', 'The enzyme can be reused and does not contaminate the product.', ['The enzyme works at all temperatures.', 'It increases the activation energy.', 'It changes the product formed.'], 'Industrial use.'),
     ('Molecular motion is greater at 30 °C than at 20 °C. How does this affect enzyme activity below the optimum?', 'More frequent collisions between substrate and active site, so the rate increases.', ['Fewer enzyme–substrate complexes form.', 'The enzyme denatures.', 'Activation energy rises.'], 'Kinetic energy and collisions.')]),
 'ch01-st2': (
    [('Why does the rate of an enzyme reaction level off at high substrate concentrations?', 'All active sites are occupied, so enzyme concentration becomes limiting.', ['The substrate denatures.', 'The enzyme is used up.', 'Products inhibit all reactions.'], 'Saturation.'),
     ('Why does pH affect enzyme activity?', 'Changes in H⁺ concentration alter ionic and hydrogen bonds in the enzyme, changing the active site shape.', ['pH changes the substrate’s DNA.', 'H⁺ ions are the substrate.', 'pH affects only temperature.'], 'Charge on R groups.')],
    [('Pepsin works in the stomach and trypsin in the small intestine. Which is most likely?', 'Pepsin has a low optimum pH (about 2) and trypsin an optimum pH of about 8.', ['Both have an optimum pH of 7.', 'Pepsin has an optimum pH of 8.', 'Trypsin has an optimum pH of 2.'], 'Matched to location.'),
     ('Doubling enzyme concentration, with excess substrate, has which effect on initial rate?', 'It approximately doubles.', ['It halves.', 'It stays the same.', 'It quadruples.'], 'More active sites.'),
     ('An enzyme’s activity at 70 °C does not recover when cooled to 37 °C. Why?', 'Denaturation is permanent: the active site shape has been irreversibly changed.', ['The enzyme is inhibited reversibly.', 'The substrate has evaporated.', 'Enzymes always recover.'], 'Irreversible.')]),
 'ch01-st3': (
    [('Why do enzymes increase the rate of reaction?', 'They lower the activation energy of the reaction.', ['They raise the temperature.', 'They supply energy to the substrate.', 'They increase the activation energy.'], 'Alternative pathway.'),
     ('Why is the initial rate used to compare enzyme activity?', 'Substrate concentration is known and highest at the start, before it falls.', ['The rate is zero at the start.', 'Product is highest at the start.', 'The enzyme is denatured later.'], 'Fair comparison.')],
    [('Oxygen released by catalase was 12 cm³ in the first 30 s. What is the initial rate?', '0.40 cm³ s⁻¹', ['2.5 cm³ s⁻¹', '360 cm³ s⁻¹', '0.04 cm³ s⁻¹'], '12/30.'),
     ('A product–time graph is steepest at the start and levels off. What does the levelling off show?', 'The substrate has been used up, so the reaction has stopped.', ['The enzyme has been used up.', 'The rate is increasing.', 'The temperature has risen.'], 'Substrate depletion.'),
     ('The gradient of a tangent at t = 0 on a graph of product against time gives:', 'the initial rate of reaction', ['the total product formed', 'the activation energy', 'the optimum temperature'], 'Gradient = rate.')]),
 'ch01-st4': (
    [('Why is end-product inhibition an example of negative feedback?', 'Accumulating product inhibits an early enzyme, reducing further production.', ['Product increases enzyme activity.', 'Substrate inhibits the last enzyme.', 'It increases product formation.'], 'Self-regulation.'),
     ('Why can a competitive inhibitor’s effect be overcome by more substrate?', 'Substrate and inhibitor compete for the same active site; more substrate wins more often.', ['Substrate destroys the inhibitor.', 'The inhibitor binds elsewhere.', 'Substrate changes the active site.'], 'Competition.')],
    [('In the isoleucine pathway, isoleucine inhibits threonine deaminase. What happens when isoleucine is in excess?', 'The first enzyme is inhibited, so less isoleucine is produced.', ['More isoleucine is produced.', 'Threonine is destroyed.', 'All enzymes in the cell stop.'], 'End-product inhibition.'),
     ('Ethanol is used to treat methanol poisoning. How does it work?', 'Ethanol competes with methanol for the active site of alcohol dehydrogenase, reducing formation of toxic products.', ['It denatures the enzyme.', 'It binds an allosteric site.', 'It increases methanol breakdown.'], 'Competitive substrate.'),
     ('Cyanide binds to cytochrome c oxidase away from the active site. What kind of inhibitor is it?', 'non-competitive', ['competitive', 'end-product', 'substrate'], 'Allosteric binding.')]),
 'ch02-st1': (
    [('Why is ATP a suitable energy currency?', 'It releases energy in small, usable amounts when hydrolysed and is easily regenerated.', ['It stores energy for years.', 'It cannot be hydrolysed.', 'It is insoluble.'], 'Immediate energy.'),
     ('Why does anaerobic respiration yield much less ATP than aerobic respiration?', 'Glucose is only partly broken down; no Krebs cycle or oxidative phosphorylation.', ['It produces more CO₂.', 'It uses more oxygen.', 'ATP is destroyed.'], '2 vs ~30 ATP.')],
    [('During a sprint, lactate concentration in muscle rises. Why?', 'Oxygen supply is insufficient, so pyruvate is reduced to lactate to regenerate NAD.', ['Lactate is made from fat.', 'Oxygen is in excess.', 'Lactate is a product of the Krebs cycle.'], 'Anaerobic respiration.'),
     ('Yeast in bread dough produce gas that makes the dough rise. Which gas and process?', 'CO₂ from anaerobic respiration (fermentation)', ['O₂ from photosynthesis', 'N₂ from decomposition', 'CO₂ from photosynthesis'], 'Ethanol and CO₂.'),
     ('A respirometer’s fluid drop moves towards the organisms. What does this measure if CO₂ is absorbed by KOH?', 'oxygen uptake by aerobic respiration', ['CO₂ release', 'water loss', 'photosynthesis'], 'Volume decrease = O₂ used.')]),
 'ch02-st2': (
    [('Why is oxygen called the final electron acceptor?', 'It accepts electrons and protons at the end of the electron transport chain, forming water.', ['It donates electrons to NAD.', 'It is used in glycolysis.', 'It is produced in the Krebs cycle.'], 'Keeps chain running.'),
     ('Why does the inner mitochondrial membrane have many folds (cristae)?', 'To give a large surface area for electron transport chains and ATP synthase.', ['To store glucose.', 'To make DNA.', 'To allow free diffusion of protons.'], 'Structure–function.')],
    [('A poison stops ATP synthase. Which immediate effect follows?', 'Protons accumulate in the intermembrane space and ATP production by chemiosmosis stops.', ['Glycolysis stops instantly.', 'Oxygen use increases.', 'The proton gradient disappears.'], 'Chemiosmosis.'),
     ('How many CO₂ molecules are released per glucose in the link reaction and Krebs cycle combined?', '6', ['2', '4', '3'], '2 in link reaction, 4 in Krebs.'),
     ('Where does glycolysis take place?', 'in the cytoplasm', ['in the mitochondrial matrix', 'on the cristae', 'in the intermembrane space'], 'No mitochondria needed.')]),
 'ch02-st3': (
    [('Why do leaves look green?', 'Chlorophyll absorbs red and blue light and reflects green light.', ['Chlorophyll absorbs green light.', 'Leaves emit green light.', 'Carotenoids absorb green.'], 'Reflection.'),
     ('Why does the action spectrum closely match the absorption spectrum of chlorophyll?', 'Wavelengths absorbed by pigments are the ones used to drive photosynthesis.', ['Pigments reflect light used.', 'Photosynthesis uses green light only.', 'They are unrelated.'], 'Absorbed light used.'),
     ('Why are accessory pigments useful?', 'They absorb a wider range of wavelengths and pass energy to chlorophyll a.', ['They make glucose.', 'They split water directly.', 'They reflect red light.'], 'Wider absorption.')],
    [('A pigment has an Rf of 0.95 in a non-polar solvent. Which is it most likely to be?', 'carotene', ['chlorophyll b', 'xanthophyll', 'anthocyanin'], 'Most soluble, moves furthest.'),
     ('Algae placed in light of different colours released most O₂ in blue and red light. What does this show?', 'These wavelengths are absorbed and used most in photosynthesis.', ['Green light is most effective.', 'Algae do not use red light.', 'Oxygen absorbs blue light.'], 'Action spectrum.'),
     ('Engelmann placed aerobic bacteria along an alga lit by a spectrum. Where did bacteria cluster?', 'in the red and blue regions', ['in the green region', 'evenly along the alga', 'only at the ends'], 'Most O₂ released there.')]),
 'ch02-st4': (
    [('Why is water needed in the light-dependent reactions?', 'Photolysis of water supplies electrons to replace those lost from photosystem II.', ['Water is the source of carbon.', 'Water absorbs light.', 'Water makes ATP directly.'], 'Electron source.'),
     ('Why does the Calvin cycle stop in the dark?', 'ATP and reduced NADP from the light-dependent reactions are no longer supplied.', ['RuBisCO is destroyed.', 'CO₂ cannot enter.', 'Glucose is used up.'], 'Dependence on products.')],
    [('After light is switched off, what happens to glycerate 3-phosphate (GP) and RuBP levels?', 'GP rises and RuBP falls.', ['GP falls and RuBP rises.', 'Both rise.', 'Both fall.'], 'GP cannot be reduced; RuBP not regenerated.'),
     ('If CO₂ is suddenly reduced, what happens to RuBP and GP?', 'RuBP rises and GP falls.', ['RuBP falls and GP rises.', 'Both fall.', 'Both rise.'], 'Less carboxylation.'),
     ('Which molecule is regenerated in the Calvin cycle to accept CO₂?', 'ribulose bisphosphate (RuBP)', ['glycerate 3-phosphate', 'triose phosphate only', 'NADP'], 'Cycle continues.')]),
 'ch02-st5': (
    [('Why can increasing temperature raise the rate of photosynthesis only up to a point?', 'Enzymes such as RuBisCO work faster until they begin to denature above the optimum.', ['Light reactions stop at low temperature.', 'CO₂ cannot dissolve at high temperatures.', 'Chlorophyll is made faster.'], 'Enzyme-controlled.'),
     ('Why is light intensity usually limiting early in the morning?', 'Light intensity is low, so the light-dependent reactions limit the rate.', ['CO₂ is absent.', 'Temperature is too high.', 'Stomata are fully closed all day.'], 'Low light.')],
    [('Rate does not increase when light is increased, but does increase when CO₂ is increased. What is the limiting factor?', 'carbon dioxide concentration', ['light intensity', 'chlorophyll', 'oxygen'], 'Only CO₂ raised rate.'),
     ('Paraffin heaters are used in a greenhouse. Which two limiting factors are increased?', 'temperature and CO₂ concentration', ['light and water', 'oxygen and nitrogen', 'humidity and light'], 'Combustion.'),
     ('At the light compensation point, what is the net gas exchange of a leaf?', 'zero – photosynthesis equals respiration', ['maximum O₂ release', 'maximum CO₂ uptake', 'only CO₂ release'], 'Balance.')]),
 'ch03-st1': (
    [('Why do steroid hormones usually have slower but longer-lasting effects?', 'They act on intracellular receptors and alter gene transcription.', ['They act on ion channels.', 'They are broken down instantly.', 'They travel along nerves.'], 'Gene expression.'),
     ('Why can a single hormone have different effects on different tissues?', 'Different tissues have different receptors and signalling pathways.', ['The hormone changes structure.', 'Hormones never act on more than one tissue.', 'Blood alters the hormone.'], 'Receptor-dependent.')],
    [('Calcium ions act as signals in muscle and neurones. What category of signal are they?', 'second messengers / local signalling chemicals', ['steroid hormones', 'neurotransmitters only', 'cytokines'], 'Intracellular signal.'),
     ('Bacteria lacking the receptor for their own autoinducer are grown at high density. What is expected?', 'They do not show quorum-sensing behaviour such as light production.', ['They glow brighter.', 'They glow at low density.', 'They become eukaryotic.'], 'Receptor needed.'),
     ('A hormone is injected and acts within seconds on liver cells without entering them. Which is most likely?', 'a peptide/amine hormone such as adrenaline binding a surface receptor', ['a steroid acting on DNA', 'a lipid entering the nucleus', 'thyroxine'], 'Rapid surface action.')]),
 'ch03-st2': (
    [('Why is cAMP called a second messenger?', 'It relays the signal from the receptor (first messenger binding) to targets inside the cell.', ['It is the hormone.', 'It is a receptor.', 'It carries signals in blood.'], 'Internal relay.'),
     ('Why must signalling pathways be switched off?', 'So cells respond only while the signal is present, allowing control.', ['To save glucose.', 'To destroy receptors.', 'To make cAMP.'], 'Termination.')],
    [('A drug blocks adenylyl cyclase in liver cells. What is the effect of adrenaline?', 'Little or no glycogen breakdown because cAMP is not produced.', ['More glycogen breakdown.', 'Insulin is released.', 'GLUT4 moves to the membrane.'], 'Pathway blocked.'),
     ('Insulin receptors are absent from a cell. What will happen when insulin is present?', 'The cell does not increase glucose uptake.', ['The cell takes up more glucose.', 'Glycogen breaks down.', 'The cell divides.'], 'No receptor, no response.'),
     ('Which response is directly caused by tyrosine kinase signalling in fat cells?', 'movement of GLUT4 vesicles to the plasma membrane', ['opening of Na⁺ channels', 'synthesis of cAMP by G proteins', 'secretion of adrenaline'], 'Insulin pathway.')]),
 'ch03-st4': (
    [('Why does the presynaptic neurone contain many mitochondria?', 'ATP is needed to make neurotransmitter, to re-form vesicles and for active transport.', ['To store calcium.', 'To make glucose.', 'To produce acetylcholinesterase in the cleft.'], 'Energy for transmission.'),
     ('Why is synaptic transmission slower than conduction along an axon?', 'Neurotransmitter release, diffusion and receptor binding take time (synaptic delay).', ['The cleft is very wide.', 'Synapses are myelinated.', 'Impulses travel backwards.'], 'Chemical step.')],
    [('Curare blocks acetylcholine receptors at neuromuscular junctions. What is the effect?', 'Muscles are paralysed because ACh cannot depolarise the muscle membrane.', ['Muscles contract continuously.', 'More ACh is broken down.', 'Calcium entry increases.'], 'Receptor antagonist.'),
     ('SSRIs block reuptake of serotonin. What is the effect at the synapse?', 'Serotonin remains in the cleft longer, increasing stimulation of postsynaptic receptors.', ['Less serotonin is released.', 'Receptors are destroyed.', 'Serotonin is broken down faster.'], 'Antidepressants.'),
     ('Several presynaptic neurones fire at once and the postsynaptic neurone reaches threshold. This is:', 'spatial summation', ['temporal summation', 'saltatory conduction', 'hyperpolarisation'], 'Several inputs at once.')]),
 'ch04-st1': (
    [('Why is the spinal cord described as having grey and white matter?', 'Grey matter contains cell bodies and synapses; white matter contains myelinated axons.', ['Grey matter is dead tissue.', 'White matter contains only blood.', 'They are identical.'], 'Structure.'),
     ('Why is the medulla, not the cerebrum, responsible for breathing?', 'Breathing must continue automatically, even during sleep, without conscious control.', ['The cerebrum has no neurones.', 'The medulla is voluntary.', 'Breathing is controlled by hormones only.'], 'Involuntary control.')],
    [('A patient’s knee-jerk reflex is absent. Which part may be damaged?', 'the sensory or motor neurone of the reflex arc, or the spinal cord segment', ['the cerebellum only', 'the pineal gland', 'the thyroid gland'], 'Reflex arc damage.'),
     ('After breathing into a bag, CO₂ in the blood rises. Which response follows?', 'Chemoreceptors stimulate the medulla to increase ventilation rate.', ['Ventilation decreases.', 'Melatonin is secreted.', 'Heart rate falls.'], 'Feedback.'),
     ('Melatonin levels are highest at:', 'night, in darkness', ['midday', 'after eating', 'during exercise'], 'Circadian rhythm.')]),
 'ch04-st2': (
    [('Why is auxin transport called polar?', 'It moves in one direction because efflux carriers are positioned on one side of cells.', ['It moves only towards the poles of the Earth.', 'It diffuses randomly.', 'It moves only in xylem.'], 'PIN proteins.'),
     ('Why do roots grow downwards?', 'Auxin accumulates on the lower side and inhibits elongation there, so the upper side grows more.', ['Auxin promotes growth on the lower side.', 'Roots are attracted to light.', 'Gravity pulls cells.'], 'Positive gravitropism.')],
    [('Removing the shoot tip of a plant causes side shoots to grow. Why?', 'Removal of auxin from the tip ends apical dominance.', ['More auxin is produced.', 'Cytokinin is removed.', 'Ethylene increases.'], 'Apical dominance.'),
     ('Gardeners dip cuttings in rooting powder. Which hormone does it contain?', 'auxin', ['ethylene', 'abscisic acid', 'insulin'], 'Promotes root formation.'),
     ('A coleoptile with its tip covered by a foil cap is lit from one side. What happens?', 'It grows straight up because the tip cannot detect light.', ['It bends towards the light.', 'It bends away.', 'It stops growing.'], 'Tip detects light.')]),
 'ch04-st3': (
    [('Why does inflammation help fight infection?', 'Increased blood flow and capillary permeability bring phagocytes and proteins to the site.', ['It destroys skin.', 'It lowers temperature.', 'It stops blood flow.'], 'Innate response.'),
     ('Why are memory cells important?', 'They allow a faster and larger antibody response if the same antigen is met again.', ['They produce antibodies immediately.', 'They are phagocytes.', 'They clot blood.'], 'Immunological memory.')],
    [('A cut on the skin becomes red, warm and swollen. What process is this?', 'inflammation', ['clotting only', 'antibody production', 'vaccination'], 'Innate response.'),
     ('Aspirin reduces platelet activity. What is the effect?', 'Blood clots form more slowly, reducing risk of thrombosis but increasing bleeding.', ['Clots form faster.', 'Antibodies increase.', 'Phagocytes stop.'], 'Platelets in clotting.'),
     ('A child exposed to measles for the second time does not become ill. What is the explanation?', 'Memory cells produce a rapid secondary response.', ['Measles is no longer present.', 'Phagocytes have memory.', 'Antibiotics were given.'], 'Secondary response.')]),
 'ch04-st5': (
    [('Why is HIV called a retrovirus?', 'It has an RNA genome that is copied into DNA by reverse transcriptase.', ['It has a DNA genome.', 'It infects bacteria.', 'It reproduces outside cells.'], 'Reverse transcription.'),
     ('Why are antibiotics ineffective against HIV?', 'HIV is a virus that lacks bacterial targets such as cell walls and 70S ribosomes.', ['HIV is resistant to all drugs.', 'HIV is a bacterium.', 'Antibiotics kill helper T cells.'], 'Viruses.')],
    [('An HIV-positive mother takes antiretroviral drugs during pregnancy. What is the main benefit?', 'Lower viral load reduces transmission to the baby.', ['The baby gains immunity to HIV.', 'It cures the mother.', 'It prevents all infections.'], 'Prevention.'),
     ('Bird flu (H5N1) spreads from poultry to farm workers. What type of disease is this?', 'a zoonosis', ['a genetic disorder', 'a deficiency disease', 'an autoimmune disease'], 'Animal to human.'),
     ('A country records 50 000 cases and 1 500 deaths. What is the CFR?', '3 %', ['0.3 %', '33 %', '30 %'], '1500/50 000 × 100.')]),
 'ch05-st4': (
    [('Why is NPP higher in tropical rainforest than in tundra?', 'Higher light, temperature and water allow more photosynthesis over a longer growing season.', ['Tundra plants respire more.', 'Rainforests have less light.', 'Tundra is wetter.'], 'Climatic factors.'),
     ('Why are oceans important in the carbon cycle?', 'CO₂ dissolves in seawater and is used by phytoplankton and stored in sediments and shells.', ['Oceans produce fossil fuels quickly.', 'Oceans release all CO₂.', 'Oceans contain no carbon.'], 'Sink.')],
    [('Over a year a forest’s GPP was 25 t C ha⁻¹ and plant respiration 14 t C ha⁻¹. What was the NPP?', '11 t C ha⁻¹', ['39 t C ha⁻¹', '1.8 t C ha⁻¹', '14 t C ha⁻¹'], 'GPP − R.'),
     ('Which process returns carbon from dead organisms to the atmosphere?', 'decomposition (respiration by saprotrophs)', ['photosynthesis', 'fossilisation', 'combustion of limestone only'], 'Decomposers.'),
     ('Atmospheric CO₂ peaks in May at Mauna Loa. Why?', 'Respiration and decomposition exceeded photosynthesis during the northern winter.', ['Photosynthesis is highest in May.', 'Volcanoes erupt in May.', 'Oceans release CO₂ only in May.'], 'Seasonal cycle.')]),
 'ch06-st3': (
    [('Why are introns removed before translation?', 'They are non-coding; including them would change the amino acid sequence.', ['They contain the start codon.', 'They make mRNA too stable.', 'Ribosomes need them.'], 'Splicing.'),
     ('Why are proteins tagged with ubiquitin?', 'To mark them for breakdown by proteasomes.', ['To export them from the cell.', 'To activate them.', 'To splice them.'], 'Protein turnover.')],
    [('A mutation at an intron–exon boundary prevents splicing. What is a likely result?', 'An intron is retained, changing the protein sequence or introducing a stop codon.', ['The protein is unchanged.', 'The 5′ cap is lost.', 'The gene is duplicated.'], 'Splice-site mutation.'),
     ('Which modification occurs at the 3′ end of pre-mRNA?', 'addition of a poly-A tail', ['addition of a 5′ cap', 'removal of the start codon', 'methylation of thymine'], 'Stability.'),
     ('Proinsulin has 86 amino acids; insulin has 51. What happened?', 'A section (C-peptide) was removed by cleavage after translation.', ['Introns were removed.', 'Translation stopped early.', 'Amino acids were added.'], 'Post-translational modification.')]),
 'ch07-st2': (
    [('Why does p53 increase in cells with damaged DNA?', 'It stops the cycle to allow repair or triggers apoptosis if damage is too great.', ['It speeds up division.', 'It causes mutations.', 'It is a cyclin.'], 'Tumour suppressor.'),
     ('Why are cancer cells often targeted by drugs that disrupt the spindle?', 'Cancer cells divide frequently, so blocking mitosis affects them more.', ['Cancer cells have no spindle.', 'Normal cells never divide.', 'The spindle is only in cancer cells.'], 'Chemotherapy.')],
    [('A cell lacks the cyclin needed for the G1/S transition. What happens?', 'The cell does not enter S phase, so DNA is not replicated.', ['It divides rapidly.', 'It skips mitosis.', 'It enters G2.'], 'Cyclin–CDK needed.'),
     ('Taxol stabilises microtubules and prevents spindle breakdown. Cells arrest in:', 'mitosis (metaphase/anaphase)', ['G1', 'S phase', 'G0'], 'Spindle checkpoint.'),
     ('An inherited mutation in BRCA1 increases breast cancer risk. Why?', 'BRCA1 is a tumour suppressor involved in DNA repair; one faulty copy makes loss of function more likely.', ['BRCA1 is an oncogene.', 'It causes trisomy.', 'It speeds up mitosis directly.'], 'Tumour suppressor.')]),
 'ch07-st3': (
    [('Why can a single transcription factor regulate many genes?', 'Many genes share the same regulatory DNA sequence it binds to.', ['It is made of DNA.', 'It translates mRNA.', 'It binds all DNA randomly.'], 'Shared binding sites.'),
     ('Why are methylation patterns maintained after DNA replication?', 'Enzymes copy methylation onto the new strand at hemimethylated sites.', ['Methyl groups are part of the base sequence.', 'They are removed each cycle.', 'Ribosomes copy them.'], 'Maintenance methylation.')],
    [('Identical twins develop different diseases in old age. Which explanation fits epigenetics?', 'Their methylation and histone modification patterns diverged with different environments.', ['They have different DNA sequences.', 'One twin lost chromosomes.', 'Epigenetics does not differ.'], 'Epigenetic drift.'),
     ('In the Himalayan rabbit, fur grows black where the skin is cool. Why?', 'An enzyme for pigment synthesis is active only at low temperatures.', ['Cold changes the DNA.', 'Warm areas lack the gene.', 'Black fur is due to methylation.'], 'Environment and enzymes.'),
     ('A gene is expressed in muscle but not in liver cells. Which is most likely?', 'Different transcription factors and chromatin states in the two cell types.', ['Liver cells lack the gene.', 'Muscle has more chromosomes.', 'The gene mutates in liver.'], 'Differential expression.')]),
 'ch07-st4': (
    [('Why does ψp become zero when a plant cell is plasmolysed?', 'The protoplast no longer pushes against the cell wall.', ['The wall dissolves.', 'Solutes leave the cell.', 'The cell bursts.'], 'No turgor.'),
     ('Why do red blood cells burst in pure water but plant cells do not?', 'Red blood cells lack a cell wall to resist expansion.', ['Red blood cells have no membrane.', 'Plant cells lack vacuoles.', 'Water cannot enter plant cells.'], 'Cell wall.')],
    [('A cell with ψ = −600 kPa is placed in a solution with ψ = −300 kPa. What happens?', 'Water enters the cell by osmosis.', ['Water leaves the cell.', 'No movement occurs.', 'Solutes enter by osmosis.'], 'Higher to lower ψ.'),
     ('A turgid plant cell has ψs = −700 kPa and ψ = −200 kPa. What is ψp?', '+500 kPa', ['−900 kPa', '−500 kPa', '+900 kPa'], 'ψp = ψ − ψs.'),
     ('Potato tissue gains no mass in 0.25 mol dm⁻³ sucrose. What does this show?', 'The tissue’s water potential equals that of the solution.', ['The tissue is plasmolysed.', 'Sucrose entered the cells.', 'The tissue is dead.'], 'Isotonic.')]),
 'ch08-st1': (
    [('Why does FSH secretion fall after ovulation?', 'High progesterone (and oestradiol) from the corpus luteum inhibit FSH by negative feedback.', ['FSH is used up.', 'hCG stimulates FSH.', 'LH destroys FSH.'], 'Negative feedback.'),
     ('Why do sperm cells have many mitochondria?', 'To supply ATP for movement of the tail (flagellum).', ['To store DNA.', 'To digest the egg.', 'To make testosterone.'], 'Energy for swimming.')],
    [('A woman’s LH surge does not occur. What is the consequence?', 'Ovulation does not take place.', ['Menstruation stops permanently.', 'More eggs are released.', 'Progesterone rises.'], 'LH triggers ovulation.'),
     ('Which hormone level rises first in the menstrual cycle?', 'FSH', ['progesterone', 'LH', 'hCG'], 'Stimulates follicle.'),
     ('A pregnancy test strip contains antibodies. What do they bind?', 'hCG in the urine', ['FSH in the blood', 'oestradiol in saliva', 'LH in the urine only'], 'Monoclonal antibodies.')]),
 'ch08-st2': (
    [('Why do wind-pollinated plants produce huge amounts of pollen?', 'Pollen transfer by wind is random and most pollen grains are wasted.', ['Wind destroys most flowers.', 'Insects eat pollen.', 'Pollen is used for photosynthesis.'], 'Chance transfer.'),
     ('Why is the endosperm important to a developing seed?', 'It stores food (starch, protein) for the embryo during germination.', ['It forms the seed coat.', 'It carries out photosynthesis.', 'It forms the pollen tube.'], 'Food store.')],
    [('Seeds kept dry in a sealed jar do not germinate. Which condition is missing?', 'water', ['light', 'carbon dioxide', 'soil'], 'Imbibition needed.'),
     ('Burdock fruits have hooks. How are they dispersed?', 'by attaching to animal fur', ['by wind', 'by water', 'by explosion'], 'Animal dispersal.'),
     ('Removing the anthers from a flower before it opens prevents:', 'self-pollination', ['cross-pollination', 'germination', 'seed dispersal'], 'Used in plant breeding.')]),
 'ch08-st4': (
    [('Why does crossing over produce recombinants only in a small proportion of gametes for closely linked genes?', 'A chiasma is less likely to form in the short region between them.', ['Crossing over never occurs near genes.', 'Recombinants are lethal.', 'Close genes assort independently.'], 'Distance.'),
     ('Why is the chi-squared test used with raw counts rather than percentages?', 'The test statistic depends on sample size; percentages would hide the number observed.', ['Percentages are always wrong.', 'Counts are easier to graph.', 'The test needs decimals.'], 'Validity.')],
    [('Genes A and B have a recombination frequency of 8 %; A and C 20 %; B and C 12 %. What is the gene order?', 'A – B – C', ['B – A – C', 'A – C – B', 'C – A – B'], 'B lies between A and C.'),
     ('A test cross of AaBb × aabb gives 1 : 1 : 1 : 1. What does this show?', 'The genes are unlinked and assort independently.', ['The genes are linked.', 'A is codominant.', 'B is sex-linked.'], 'Independent assortment.'),
     ('χ² = 11.2 with 3 df (critical 7.81). What is concluded?', 'Reject H₀: significant difference from the expected ratio.', ['Accept H₀.', 'The genes are on different chromosomes.', 'The sample is too large.'], 'χ² > critical.')]),
 'ch08-st5': (
    [('Why does a trait controlled by many genes show a bell-shaped distribution?', 'Intermediate combinations of alleles are far more likely than extreme combinations.', ['Each gene is dominant.', 'The environment removes extremes.', 'Mutations prevent extremes.'], 'Probability.'),
     ('Why is a histogram suitable for continuous variation?', 'Data are grouped into continuous classes with no gaps between them.', ['The data are categories.', 'It shows individual names.', 'It removes variation.'], 'Continuous data.')],
    [('Nilsson-Ehle’s wheat cross gave F2 colour classes in the ratio 1 : 4 : 6 : 4 : 1. How many genes were involved?', '2', ['1', '4', '5'], '2n + 1 = 5 classes.'),
     ('Two heterozygous parents (AaBbCc) for an additive trait have offspring. What proportion has no contributing alleles?', '1/64', ['1/8', '1/16', '1/32'], '(1/4)³.'),
     ('A sample has mean 50 and SD 4. Approximately what percentage of values lie between 46 and 54?', '68 %', ['95 %', '50 %', '99 %'], '±1 SD.')]),
 'ch09-st1': (
    [('Why does the liver store glucose as glycogen rather than glucose?', 'Glycogen is insoluble and compact, so it does not affect water potential.', ['Glucose cannot enter the liver.', 'Glycogen is smaller.', 'Glycogen is a hormone.'], 'Storage.'),
     ('Why are both insulin and glucagon needed?', 'They act antagonistically, allowing correction of both rises and falls in blood glucose.', ['They have the same effect.', 'Insulin raises glucose.', 'Glucagon is only for digestion.'], 'Antagonistic hormones.')],
    [('A person with type 1 diabetes injects too much insulin. What may happen?', 'Blood glucose falls too low (hypoglycaemia).', ['Blood glucose rises.', 'Glucagon is destroyed.', 'β cells regenerate.'], 'Overdose.'),
     ('Metformin reduces glucose release from the liver. Which condition is it used to treat?', 'type 2 diabetes', ['type 1 diabetes only', 'hypothermia', 'haemophilia'], 'Insulin resistance.'),
     ('In an untreated person with type 1 diabetes, which is expected after a meal?', 'Blood glucose rises and stays high because no insulin is secreted.', ['Glucose falls quickly.', 'Insulin rises sharply.', 'Glycogen is formed rapidly.'], 'No insulin.')]),
 'ch09-st2': (
    [('Why does the body temperature of a person with fever stay high despite sweating stopping?', 'The hypothalamus set point has been raised, so the body maintains a higher temperature.', ['The hypothalamus is destroyed.', 'Sweat glands produce heat.', 'Blood stops flowing.'], 'Altered set point.'),
     ('Why do small mammals have higher metabolic rates per gram than large ones?', 'Their large surface area to volume ratio causes faster heat loss.', ['They have more fur.', 'They have less surface area.', 'They do not need to stay warm.'], 'SA:V.')],
    [('A person in cold water stops shivering and becomes confused. What is happening?', 'Hypothermia: heat loss exceeds heat production and core temperature falls.', ['Hyperthermia.', 'Vasodilation is cooling the core.', 'Thyroxine is too high.'], 'Hypothermia.'),
     ('Which response reduces heat loss in a cold environment?', 'vasoconstriction of skin arterioles', ['vasodilation of skin arterioles', 'sweating', 'flattening of hairs'], 'Less blood near surface.'),
     ('An overactive thyroid gland would cause:', 'increased metabolic rate and heat production', ['decreased metabolic rate', 'reduced oxygen use', 'lower body temperature'], 'Thyroxine effect.')]),
 'ch09-st3': (
    [('Why do the collecting ducts pass through the medulla?', 'The high solute concentration of the medulla draws water out of the ducts by osmosis.', ['The medulla filters blood.', 'The medulla secretes urea.', 'Ducts store urine there.'], 'Concentration gradient.'),
     ('Why is urea produced rather than ammonia in mammals?', 'Urea is less toxic and can be stored and excreted in concentrated urine.', ['Urea is more toxic.', 'Ammonia is insoluble.', 'Urea contains no nitrogen.'], 'Toxicity.')],
    [('A drug blocks ADH receptors in the kidney. What is the effect?', 'Large volumes of dilute urine are produced.', ['Small volumes of concentrated urine.', 'Glucose appears in urine.', 'Filtration stops.'], 'Less water reabsorption.'),
     ('Which substance has the same concentration in plasma and glomerular filtrate?', 'glucose', ['plasma proteins', 'red blood cells', 'platelets'], 'Small solutes are freely filtered.'),
     ('Desert mammals have longer loops of Henle. Why?', 'A longer loop creates a steeper solute gradient so more water can be reabsorbed.', ['To filter more blood.', 'To excrete more water.', 'To store urea.'], 'Concentrated urine.')]),
 'ch10-st1': (
    [('Why is antibiotic resistance in bacteria evidence of natural selection?', 'Resistant variants survive antibiotic treatment and reproduce, so their frequency increases.', ['Antibiotics create resistance genes on demand.', 'Bacteria learn.', 'All bacteria become resistant at once.'], 'Selection.'),
     ('Why do populations with low genetic diversity risk extinction?', 'They have fewer variants that might survive a new selection pressure.', ['They reproduce faster.', 'They have more mutations.', 'They never compete.'], 'Adaptability.')],
    [('After a drought, finches with larger beaks survived better. In the next generation, mean beak size increased. Why?', 'Beak size is heritable, so survivors passed on alleles for large beaks.', ['The finches stretched their beaks.', 'Drought caused mutations.', 'Small-beaked birds migrated.'], 'Heritable variation.'),
     ('Female birds prefer males with long tails. Long tails make males easier for predators to catch. Which statement is correct?', 'Tail length depends on the balance of sexual and natural selection.', ['Tails will always get longer.', 'Predation has no effect.', 'Females evolve long tails.'], 'Trade-off.'),
     ('Which is NOT a requirement for natural selection?', 'individuals deliberately changing to suit the environment', ['heritable variation', 'overproduction of offspring', 'differential survival'], 'Lamarckian idea.')]),
 'ch10-st3': (
    [('Why can removing top predators destabilise ecosystems?', 'Herbivore populations may increase and overgraze producers (trophic cascade).', ['Producers always increase.', 'Decomposers disappear.', 'Energy flow increases.'], 'Top-down control.'),
     ('Why does a sealed mesocosm need light but not added food?', 'Producers capture light energy and nutrients are recycled by decomposers.', ['Animals photosynthesise.', 'Energy is recycled.', 'Oxygen is supplied from outside.'], 'Energy flows; matter recycles.')],
    [('Mercury in fish rises from 0.1 ppm in small fish to 1.2 ppm in tuna. What is the biomagnification factor?', '12', ['1.1', '0.08', '120'], '1.2/0.1.'),
     ('Buffer strips of vegetation between fields and rivers help to:', 'absorb nutrients from run-off and reduce eutrophication', ['increase fertiliser run-off', 'raise water temperature', 'add phosphates to rivers'], 'Sustainable farming.'),
     ('A fishing quota is set below maximum sustainable yield. What is the expected effect?', 'The stock can be maintained or increase over time.', ['The stock will collapse.', 'Fish growth stops.', 'Biodiversity falls.'], 'Sustainable harvest.')]),
 'ch10-st4': (
    [('Why is methane a significant greenhouse gas despite its low concentration?', 'Each molecule absorbs much more infrared radiation than a CO₂ molecule.', ['It reflects sunlight.', 'It destroys ozone.', 'It is a liquid.'], 'Global warming potential.'),
     ('Why are coral reefs especially vulnerable to climate change?', 'Corals bleach at small temperature rises and acidification reduces calcification.', ['Corals benefit from warming.', 'Reefs are in polar regions.', 'Corals photosynthesise directly.'], 'Two threats.')],
    [('Polar bear populations decline as sea ice shrinks. Why?', 'They hunt seals from sea ice, so less ice means less food.', ['They overheat in the sun.', 'They are eaten by seals.', 'They migrate south to forests.'], 'Habitat loss.'),
     ('A butterfly’s northern range edge has moved 100 km north in 30 years. What is the mean rate?', 'about 3.3 km per year', ['about 30 km per year', 'about 0.3 km per year', 'about 100 km per year'], '100/30.'),
     ('Which is an example of mitigation of climate change?', 'replacing coal power stations with wind and solar power', ['building higher sea walls', 'planting drought-resistant crops', 'moving species to cooler areas'], 'Reduces emissions.')]),
 'ch11-st3': (
    [('Why are error bars added to graphs of means?', 'They show the variability of the data at each point, helping judge whether differences may be significant.', ['They show the mean.', 'They prove significance.', 'They show the independent variable.'], 'Variability.'),
     ('Why is p = 0.05 used as a threshold?', 'It means there is less than a 5 % probability that the result is due to chance.', ['It proves the hypothesis.', 'It means 95 % of data are correct.', 'It is the mean.'], 'Convention.')],
    [('Two samples of 10 give t = 1.6. The critical value (18 df) is 2.10. What is concluded?', 'No significant difference; accept the null hypothesis.', ['A significant difference.', 'A strong correlation.', 'The data are invalid.'], 't < critical value.'),
     ('Which statistic would best test whether light intensity and plant height are related?', 'Pearson correlation coefficient', ['chi-squared test', 'Lincoln index', 'Simpson’s index'], 'Two continuous variables.'),
     ('Data set A has mean 20, SD 1; set B mean 20, SD 6. Which statement is correct?', 'A’s values are more closely clustered around the mean.', ['B is more reliable.', 'A has a larger spread.', 'They have identical spread.'], 'Smaller SD.')]),
 'ch11-st4': (
    [('Why should a conclusion include a scientific explanation?', 'It links the observed trend to biological theory, showing why the relationship occurs.', ['It replaces the data.', 'It removes the need for evaluation.', 'It changes the results.'], 'Explanation.'),
     ('Why are extensions to an investigation suggested in the evaluation?', 'They propose further questions that follow from the findings.', ['To repeat the same experiment exactly.', 'To hide limitations.', 'To change the original data.'], 'Further research.')],
    [('A balance reads 0.02 g with nothing on it. All masses are therefore:', 'too high by 0.02 g – a systematic error', ['randomly scattered', 'accurate', 'too low by 0.02 g'], 'Zero error.'),
     ('A length of 2.0 cm is measured with ±0.1 cm uncertainty. What is the percentage uncertainty?', '5 %', ['0.5 %', '2 %', '10 %'], '0.1/2.0 × 100.'),
     ('Repeats at one temperature are 30, 31 and 29 s. The results are best described as:', 'precise (repeatable)', ['inaccurate', 'anomalous', 'invalid'], 'Close agreement.')]),
}

for _k, (_m2, _m3) in MORE_MCQ.items():
    R.mcqs(_k, 'C2', (1, 4), _m2)
    R.mcqs(_k, 'C3', (2, 5), _m3)
