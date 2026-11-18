"""IB DP Chemistry SL/HL (first assessment 2025), DP year 1 – ib-g11-chemistry.

Structure 1 (particulate nature, nuclear atom, electron configurations, the mole, ideal gases),
Reactivity 2.1 (stoichiometry), Structure 2 (ionic, covalent, metallic models and materials) and
Reactivity 1 (enthalpy, energy cycles, fuels, entropy and spontaneity – HL).

Numerical items are parametric and compute their answers with IB data-booklet values
(see ib_chemistry_common). Answers are quoted to 3 significant figures unless the data justify
fewer. Mock = HL Paper 1A (40 MCQ) + 1B (data-based, 35 marks) + Paper 2 (90 marks).
"""
from __future__ import annotations

import math
from fractions import Fraction

from _common import F, Registry, T, mcq, name, two_names, sup, CITIES  # noqa: F401
from ib_chemistry_common import (AR, BE, CONFIG, CW, EN, ENAME, HF, IE1, MOCK, NA, RGAS, S0, VM, Z, H_PLANCK,  # noqa: F401
                                  C_LIGHT, atoms, chem, dp, ion, make_templates, mr, nmcq, num, p1b, pct_error,
                                  pick, q, repeat_readings, sf, sgn)

R = Registry()
templates = make_templates(R)


def init(subject_id):
    pass


# =============================================================================================
# ch01 S1.1 Particulate nature of matter and S1.2 The nuclear atom
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('element', 'a substance made of only one type of atom, which cannot be broken down into simpler substances by chemical means'),
           ('compound', 'a substance made of two or more different elements chemically bonded in a fixed ratio'),
           ('mixture', 'two or more substances physically combined in variable proportions and not chemically bonded'),
           ('homogeneous mixture', 'a mixture with uniform composition and properties throughout, in a single phase'),
           ('heterogeneous mixture', 'a mixture with non-uniform composition in which the different components or phases can be distinguished'),
           ('solvent', 'the component of a solution, usually present in the larger amount, in which the solute dissolves'),
           ('retardation factor (Rf)', 'the distance travelled by a component divided by the distance travelled by the solvent front in chromatography')],
    facts=[('Which of the following is a compound?', 'sodium chloride', ['air', 'brass', 'seawater'], 'Sodium chloride has Na and Cl chemically combined in a fixed 1:1 ratio; the others are mixtures.'),
           ('Which technique is most suitable for obtaining pure water from seawater?', 'distillation', ['filtration', 'paper chromatography', 'crystallisation'], 'Distillation separates the volatile solvent (water) from the dissolved salts.'),
           ('Which mixture can be separated by fractional distillation?', 'ethanol and water', ['sand and water', 'iron filings and sulfur', 'salt and sand'], 'Fractional distillation separates miscible liquids with different boiling points.'),
           ('Which property is used to separate the components in paper chromatography?', 'different relative attraction to the stationary and mobile phases', ['different boiling points', 'different particle sizes', 'different densities'], 'Components partition differently between the stationary phase (paper/water) and the mobile phase (solvent).'),
           ('Which is a homogeneous mixture?', 'a solution of copper(II) sulfate in water', ['a suspension of chalk in water', 'oil floating on water', 'granite'], 'A solution has a single phase with uniform composition.'),
           ('Which separation technique relies on a difference in solubility between hot and cold solvent?', 'recrystallisation', ['filtration', 'simple distillation', 'magnetic separation'], 'Impure solid is dissolved in minimum hot solvent; the desired product crystallises on cooling while impurities stay in solution.'),
           ('Air is classified as a mixture because', 'its composition varies and its components keep their own properties', ['it contains only elements', 'it is a gas', 'it cannot be separated'], 'Mixtures have variable composition and are separable by physical means (e.g. fractional distillation of liquid air).')],
    why=[('Explain why the properties of a compound differ from those of the elements it is made from.', 'In a compound the atoms are chemically bonded, forming a new substance with its own structure and bonding; e.g. sodium (reactive metal) and chlorine (toxic gas) form sodium chloride, a stable ionic solid.'),
         ('Explain why a mixture has no fixed melting point while a pure substance has a sharp melting point.', 'In a pure substance all particles are identical so the lattice breaks down at one temperature; in a mixture the composition varies and impurities disrupt the lattice, so melting occurs over a range (usually lower).'),
         ('Explain how filtration separates an insoluble solid from a liquid.', 'The solid particles are too large to pass through the pores of the filter paper and remain as the residue; the liquid and dissolved substances pass through as the filtrate.'),
         ('Explain why fractional distillation can separate ethanol (boiling point 78 °C) from water (100 °C).', 'The more volatile ethanol vaporises more readily; repeated condensation and re-vaporisation on the large surface area of the fractionating column enriches the vapour in ethanol, which distils over first at about 78 °C.'),
         ('Explain why the solvent front must be marked as soon as a chromatogram is removed from the tank.', 'The solvent evaporates quickly and the front becomes invisible; its position is needed to calculate Rf = distance moved by spot / distance moved by solvent.'),
         ('Explain why the starting line on a paper chromatogram is drawn in pencil and placed above the solvent level.', 'Pencil (graphite) does not dissolve in the solvent and so will not move; if the spots were below the solvent level they would dissolve into the solvent instead of travelling up the paper.'),
         ('Explain why the Rf value of a substance can be used to help identify it.', 'Under the same conditions (same solvent, stationary phase and temperature) a given substance always partitions in the same way and so has a characteristic Rf; comparing with standards helps identify it.')],
    contrast=[('a compound', 'a mixture', 'A compound has elements chemically bonded in a fixed ratio and can only be separated chemically; a mixture has components not chemically bonded, in variable proportions, separable by physical methods.'),
              ('a homogeneous mixture', 'a heterogeneous mixture', 'A homogeneous mixture has uniform composition in one phase (e.g. salt solution); a heterogeneous mixture has non-uniform composition with visibly distinct phases (e.g. sand in water).'),
              ('simple distillation', 'fractional distillation', 'Simple distillation separates a volatile liquid from dissolved solids (or liquids with very different boiling points); fractional distillation uses a fractionating column to separate miscible liquids with close boiling points.'),
              ('the filtrate', 'the residue', 'The filtrate is the liquid (with dissolved substances) that passes through the filter paper; the residue is the insoluble solid left on the paper.')],
    misc=[('Salt water is a compound because the salt and water cannot be seen separately.', 'Salt water is a homogeneous mixture: the salt is not chemically bonded to the water, the proportions can vary and the salt can be recovered by evaporation.'),
          ('A substance with a high Rf value is more strongly attracted to the paper.', 'A high Rf means the substance moved further with the solvent: it is more attracted to the mobile phase (more soluble in the solvent) and less to the stationary phase.'),
          ('Distillation works because the solid has a higher density than the liquid.', 'Distillation depends on a difference in volatility (boiling point), not density; the liquid vaporises and condenses while the non-volatile solute remains.'),
          ('Elements are always made of single, separate atoms.', 'Many elements exist as molecules (O₂, Cl₂, P₄, S₈) or giant structures (diamond, metals); an element simply contains only one type of atom.')],
    cases=[('the fractional distillation of crude oil in a refinery', 'Crude oil is heated and the vapour rises up a column that is hotter at the bottom; fractions condense at different heights according to boiling point.', 'separation of miscible liquids by fractional distillation', 'Each fraction contains hydrocarbons with a similar range of chain lengths (and so boiling points), showing separation based on volatility.'),
           ('the desalination of seawater in plants in the Middle East', 'Multi-stage flash distillation evaporates seawater and condenses the vapour as fresh water, leaving brine.', 'the separation of a solvent from a solution', 'Water is volatile and the dissolved salts are not, so distillation yields pure water – but it is very energy intensive.'),
           ('forensic analysis of ink from a forged cheque using paper chromatography', 'The ink is spotted beside inks from suspects\' pens and the chromatogram developed in the same solvent.', 'identification of components using Rf values', 'Matching patterns of spots with identical Rf values under identical conditions links the ink to a pen.'),
           ('the extraction of salt from rock salt', 'Rock salt is crushed, dissolved in water, filtered to remove sand and the filtrate evaporated/crystallised.', 'combining dissolving, filtration and crystallisation', 'Each step exploits a different physical property: solubility, particle size and volatility of the solvent.')],
    evaluate=[('Paper chromatography is a sufficient technique to prove that a food colouring contains only permitted dyes.', ['it is cheap, quick and needs only a tiny sample', 'matching Rf values with reference dyes is good evidence'], ['two different dyes may have the same Rf in one solvent', 'Rf depends on conditions and colourless components are invisible', 'confirmatory techniques (two solvents, HPLC, mass spectrometry) are needed for proof'], 'Chromatography is a useful screening method, but proof requires matching in more than one solvent system and ideally an instrumental method.'),
              ('Distillation is the best way to provide drinking water for a coastal city.', ['produces very pure water from an unlimited source', 'reliable and independent of rainfall'], ['very high energy demand and associated CO₂ emissions', 'brine waste harms marine ecosystems', 'reverse osmosis is usually cheaper per m³'], 'Distillation is effective but costly; the best choice depends on available energy (e.g. waste heat or solar), with reverse osmosis often preferred.')],
    extended=[('A mixture contains sand, sodium chloride and iodine. Iodine sublimes on gentle heating. Describe, giving the property exploited at each stage, how a pure, dry sample of each component could be obtained.', 'Heat the mixture gently in an evaporating basin under a cold surface: iodine sublimes and is collected (volatility). Add water to the residue and stir: NaCl dissolves (solubility). Filter: sand is the residue (particle size); wash and dry it. Evaporate/crystallise the filtrate to obtain NaCl (volatility of solvent).', 6, 'multi_step'),
              ('Plan an investigation, using paper chromatography, to find out whether an orange drink contains the dye E110 (sunset yellow). Include the procedure, how the results would be analysed and one limitation.', 'Draw a pencil base line; spot the drink extract and a reference sample of E110 side by side; place in a tank with solvent below the line; cover; remove when the solvent front is near the top and mark it; calculate Rf values. Same Rf and colour as the reference suggests E110 is present. Limitation: another dye could share the Rf – repeat with a different solvent.', 6, 'multi_step')],
))

MIXES = [('sand and water', 'filtration', 'sand is insoluble and its particles are too large to pass through the filter paper'),
         ('copper(II) sulfate crystals from its aqueous solution', 'crystallisation', 'evaporating some water then cooling gives crystals as solubility falls'),
         ('pure water from ink', 'simple distillation', 'water is volatile while the dyes are not'),
         ('ethanol from a fermented sugar solution', 'fractional distillation', 'ethanol and water are miscible liquids with different boiling points'),
         ('the dyes in a black felt-tip ink', 'paper chromatography', 'the dyes partition differently between the stationary and mobile phases'),
         ('iron filings from sulfur powder', 'magnetic attraction', 'iron is magnetic and sulfur is not'),
         ('oil and water', 'a separating funnel', 'the liquids are immiscible and form two layers of different density'),
         ('nitrogen and oxygen from liquefied air', 'fractional distillation', 'N₂ (−196 °C) and O₂ (−183 °C) have different boiling points'),
         ('chalk (calcium carbonate) from a suspension in water', 'filtration', 'calcium carbonate is insoluble in water'),
         ('benzoic acid from a small amount of soluble impurity', 'recrystallisation', 'benzoic acid is much more soluble in hot water than in cold water'),
         ('a coloured impurity in a drug sample', 'chromatography', 'components of the sample travel different distances'),
         ('cyclohexane from water', 'a separating funnel', 'cyclohexane is immiscible with water and less dense')]
TECHS = ['filtration', 'crystallisation', 'simple distillation', 'fractional distillation', 'paper chromatography',
         'a separating funnel', 'magnetic attraction', 'recrystallisation', 'sublimation']


@R.add('ch01-st1', 'C3', (1, 3), 'mcq')
def c3_sep_mcq(rng, slot):
    mix, tech, why = pick(rng, MIXES)
    wrong = [t for t in TECHS if t != tech and not (tech in t or t in tech)]
    stem = pick(rng, [f'Which technique is most suitable to separate {mix}?', f'A student needs to obtain {mix}. Which method should be used?'])
    return mcq(rng, stem, tech, rng.sample(wrong, 3), f'{tech[0].upper() + tech[1:]}: {why}.')


@R.add('ch01-st1', 'C3', (2, 4), 'short')
def c3_sep_short(rng, slot):
    mix, tech, why = pick(rng, MIXES)
    stem = pick(rng, [f'Identify the most suitable technique to separate {mix} and state the physical property it relies on.',
                      f'Suggest how {mix} could be separated in the laboratory, explaining why the method works.'])
    return dict(stem=stem, answer=f'{tech[0].upper() + tech[1:]}: {why}.', markingKey=f'Technique: {tech} (1); property/explanation: {why} (1).', type='short', marks=2)


@R.add('ch01-st1', 'C3', (1, 4), 'numerical')
def c3_rf(rng, slot):
    front = round(rng.uniform(6.0, 12.0), 1)
    spot = round(front * rng.uniform(0.15, 0.9), 1)
    rf = spot / front
    who = name(rng)
    dye = pick(rng, ['a red food dye', 'chlorophyll a', 'an amino acid stained with ninhydrin', 'a blue ink component', 'carotene', 'a yellow pigment from a highlighter', 'a dye from a sports drink'])
    if slot.d <= 2:
        stem = f'In a paper chromatogram obtained by {who}, the solvent front moved {front} cm from the base line and {dye} moved {spot} cm. Calculate the Rf value.'
        return num(stem, f'{rf:.2f}', f'Rf = {spot}/{front} (M1) = {rf:.2f}, no units (A1).', 2)
    if slot.d == 3:
        stem = f'{who} obtained a chromatogram on which {dye} had an Rf value of {rf:.2f}. The solvent front was {front} cm above the base line. Determine how far the spot travelled.'
        return num(stem, f'{rf * front:.1f} cm', f'distance = Rf × solvent front distance = {rf:.2f} × {front} (M1) = {rf * front:.1f} cm (A1).', 2)
    s2 = round(front * rng.uniform(0.15, 0.9), 1)
    if abs(s2 - spot) < 0.6:
        return None
    rf2 = s2 / front
    stem = (f'{who} analysed an extract containing {dye}. Two spots appeared, {spot} cm and {s2} cm from the base line; the solvent front was {front} cm from the base line. '
            f'A reference sample of the dye has Rf = {rf2:.2f} in this solvent. Calculate both Rf values and deduce which spot could be the dye, stating why this is not conclusive.')
    return num(stem, f'Rf = {rf:.2f} and {rf2:.2f}; the spot at {s2} cm matches the reference', f'Rf values {rf:.2f} and {rf2:.2f} (M1 A1); spot at {s2} cm matches (A1); another substance could share the Rf – confirm with a second solvent or co-spotting (R1).', 4, 'multi_step')


CLASSIFY = [('brass', 'mixture (alloy) – homogeneous'), ('distilled water', 'compound'), ('graphite', 'element'),
            ('air', 'mixture – homogeneous'), ('sea water', 'mixture – homogeneous'), ('ozone, O₃', 'element'),
            ('sodium hydrogencarbonate', 'compound'), ('granite', 'mixture – heterogeneous'), ('mercury', 'element'),
            ('milk', 'mixture – heterogeneous (colloid)'), ('glucose', 'compound'), ('steel', 'mixture (alloy) – homogeneous'),
            ('sulfur, S₈', 'element'), ('carbon dioxide', 'compound'), ('muddy river water', 'mixture – heterogeneous')]


@R.add('ch01-st1', 'C1', (1, 3), 'short')
def c1_classify(rng, slot):
    items = rng.sample(CLASSIFY, 3)
    stem = 'Classify each of the following as an element, a compound or a mixture (state whether any mixture is homogeneous or heterogeneous): ' + '; '.join(i[0] for i in items) + '.'
    ans = '; '.join(f'{a}: {b}' for a, b in items)
    return dict(stem=stem, answer=ans, markingKey=ans + ' (1 mark per correct classification).', type='short', marks=3 if slot.d >= 2 else 2)


R.mcqs('ch01-st1', 'C2', (1, 4), [
    ('A sample of a white solid melts over the range 118–123 °C. The literature melting point of the pure substance is 122 °C. What does this suggest?', 'The sample is impure.', ['The sample is pure.', 'The sample is a compound, not an element.', 'The thermometer reads too high.'], 'Impurities lower and broaden the melting range.'),
    ('In paper chromatography, which statement explains why two dyes separate?', 'They have different affinities for the mobile and stationary phases.', ['They have different colours.', 'They have different masses so move at different speeds.', 'The solvent reacts with one of the dyes.'], 'Separation depends on partitioning between the two phases.'),
    ('Why is a fractionating column packed with glass beads?', 'to provide a large surface area for repeated condensation and vaporisation', ['to catalyse the separation', 'to absorb water from the vapour', 'to cool the vapour quickly to room temperature'], 'Many condensation-vaporisation cycles enrich the vapour in the more volatile component.'),
    ('Which change shows that iron sulfide is a compound rather than a mixture of iron and sulfur?', 'It is not attracted by a magnet.', ['It is a solid.', 'It can be ground into a powder.', 'It has a dark colour.'], 'Iron in the mixture is magnetic; in FeS iron is chemically combined and the compound has new properties.'),
    ('A green leaf extract gives four spots on a chromatogram. Which conclusion is valid?', 'The extract contains at least four coloured components.', ['The extract contains exactly four substances.', 'All four substances are compounds of magnesium.', 'The extract is a homogeneous compound.'], 'Colourless components or co-running substances may be hidden, so “at least”.'),
])

repeat_readings(R, 'ch01-st1', 'the distance moved by a dye spot', 'cm', 3.0, 8.0, 1,
                ['ran three chromatograms of the same food colouring under identical conditions.',
                 'repeated a paper chromatography experiment to check the reproducibility of a dye spot.'])


@p1b(R, 'ch01-st1')
def p1b_chromatography(rng, slot):
    front = round(rng.uniform(8.0, 11.0), 1)
    refs = {'E102 (tartrazine)': rng.uniform(0.15, 0.3), 'E129 (allura red)': rng.uniform(0.35, 0.5), 'E133 (brilliant blue)': rng.uniform(0.6, 0.8)}
    refs = {k: round(v, 2) for k, v in refs.items()}
    k_in = rng.sample(list(refs), 2)
    spots = sorted(round(refs[k] * front + rng.uniform(-0.1, 0.1), 1) for k in k_in)
    rfs = [s / front for s in spots]
    tab = '\n'.join(f'{k}: Rf = {v:.2f}' for k, v in refs.items())
    intro = (f'A student analysed a sweet coating by paper chromatography using a water/ethanol solvent. The solvent front travelled {front} cm. '
             f'Two spots appeared at {spots[0]} cm and {spots[1]} cm from the base line. Reference dyes run under identical conditions gave:\n{tab}')
    match = [min(refs, key=lambda k: abs(refs[k] - r)) for r in rfs]
    return dict(intro=intro, parts=[
        ('Calculate the Rf value of each spot.', f'{rfs[0]:.2f} and {rfs[1]:.2f}', f'Rf = distance moved by spot / distance moved by solvent front (M1); {rfs[0]:.2f} and {rfs[1]:.2f} (A1).', 2),
        ('Deduce which dyes are present in the coating.', ' and '.join(match), f'{match[0]} and {match[1]} – closest Rf values (A1).', 1),
        ('The ruler has a precision of ±0.1 cm. Determine the percentage uncertainty in the Rf value of the lower spot.', f'{(0.1 / spots[0] + 0.1 / front) * 100:.1f} %', f'% uncertainty = 0.1/{spots[0]} × 100 + 0.1/{front} × 100 (M1) = {(0.1 / spots[0] + 0.1 / front) * 100:.1f} % (A1).', 2),
        ('Explain why the beaker was covered with a lid while the chromatogram developed.', 'To saturate the air with solvent vapour so the solvent does not evaporate from the paper and the solvent front rises evenly.', 'Prevents evaporation of the solvent from the paper / keeps atmosphere saturated (1); gives reproducible Rf values (1).', 2)],
        extras=[('Suggest why a second, different solvent should be used before drawing a firm conclusion.', 'Different dyes may have the same Rf in one solvent; agreement in two solvents is much stronger evidence.', 'Coincident Rf in one solvent possible (1).', 1)])


R.facts('ch01-st2', F(
    terms=[('kinetic molecular theory', 'the model in which matter consists of particles in constant random motion whose average kinetic energy is proportional to the absolute temperature'),
           ('absolute zero', 'the lowest possible temperature, 0 K (−273.15 °C), at which particles have minimum kinetic energy'),
           ('sublimation', 'the direct change of state from solid to gas without passing through the liquid state'),
           ('deposition', 'the direct change of state from gas to solid'),
           ('melting point', 'the temperature at which the solid and liquid states of a pure substance are in equilibrium at a given pressure'),
           ('evaporation', 'the change from liquid to gas that occurs at the surface of a liquid at temperatures below its boiling point')],
    facts=[('What is 25 °C on the Kelvin scale?', '298 K', ['−248 K', '25 K', '273 K'], 'T/K = T/°C + 273.15 ≈ 298 K.'),
           ('During the melting of a pure solid, the temperature stays constant because', 'the energy supplied is used to overcome attractions between particles', ['the particles stop moving', 'the kinetic energy of the particles increases', 'heat is lost to the surroundings'], 'Energy goes into breaking intermolecular attractions (potential energy), not raising average kinetic energy.'),
           ('Which change of state is exothermic?', 'condensation', ['melting', 'boiling', 'sublimation'], 'Forming attractions between particles releases energy.'),
           ('The average kinetic energy of gas particles is directly proportional to', 'the absolute temperature', ['the Celsius temperature', 'the pressure only', 'the molar mass'], 'Ek(average) ∝ T in kelvin.'),
           ('Which describes the particles in a liquid?', 'close together, irregularly arranged and able to move past each other', ['far apart and moving rapidly in straight lines', 'in fixed positions in a regular lattice', 'close together and stationary'], 'Liquids: close-packed, disordered, particles can slide past one another.'),
           ('Which process occurs when solid carbon dioxide (dry ice) is left at room temperature?', 'sublimation', ['melting', 'condensation', 'deposition'], 'At 1 atm CO₂ passes directly from solid to gas at −78 °C.')],
    why=[('Explain, in terms of particles, why the temperature of water remains at 100 °C while it boils.', 'The energy supplied is used to overcome the intermolecular forces (hydrogen bonds) between water molecules as they separate into the gas, increasing potential energy rather than average kinetic energy, so temperature stays constant.'),
         ('Explain why gases are much easier to compress than liquids.', 'In a gas the particles are far apart with large spaces between them, so they can be pushed closer together; in a liquid particles are already in contact.'),
         ('Explain why the Kelvin scale, rather than the Celsius scale, must be used in gas calculations.', 'The Kelvin scale starts at absolute zero, so values are proportional to the average kinetic energy of the particles; Celsius has an arbitrary zero, so ratios of Celsius temperatures have no physical meaning.'),
         ('Explain why evaporation causes the remaining liquid to cool.', 'Only the particles with the highest kinetic energy escape from the surface, so the average kinetic energy (and therefore temperature) of the remaining particles falls.'),
         ('Explain why a gas spreads to fill its container (diffuses).', 'Gas particles move rapidly and randomly with negligible attractions between them, so they spread from regions of high concentration until evenly distributed.'),
         ('Explain why the heating curve of a pure substance shows a longer plateau for boiling than for melting.', 'Boiling requires essentially all the attractions between particles to be overcome as they separate completely, which needs far more energy than melting, where particles remain close together.')],
    contrast=[('evaporation', 'boiling', 'Evaporation occurs only at the surface and at any temperature below the boiling point; boiling occurs throughout the liquid, at a fixed temperature where vapour pressure equals external pressure.'),
              ('sublimation', 'deposition', 'Sublimation is solid → gas (endothermic); deposition is gas → solid (exothermic).'),
              ('temperature', 'heat', 'Temperature is a measure of the average kinetic energy of the particles; heat is energy transferred because of a temperature difference.')],
    misc=[('At 0 °C the particles of a substance stop moving.', 'Particles have minimum kinetic energy only at absolute zero (0 K = −273 °C); at 0 °C (273 K) they still vibrate/move.'),
          ('When ice melts the water molecules break into hydrogen and oxygen atoms.', 'Melting only overcomes intermolecular forces (hydrogen bonds) between molecules; the covalent O–H bonds within molecules remain intact.'),
          ('Doubling the temperature of a gas from 20 °C to 40 °C doubles the average kinetic energy of its particles.', 'Average kinetic energy is proportional to absolute temperature: 293 K → 313 K is only a 1.07-fold increase.'),
          ('During boiling the temperature rises because the particles move faster.', 'For a pure substance the temperature stays constant during boiling; energy is used to overcome intermolecular forces, not to raise kinetic energy.')],
    evaluate=[('The kinetic molecular theory is a good model for explaining the behaviour of all states of matter.', ['explains diffusion, pressure, changes of state and the effect of temperature', 'links macroscopic temperature to particle kinetic energy'], ['treats particles as simple spheres and ignores the details of bonding', 'does not quantitatively predict properties of liquids and solids', 'cannot explain quantum effects at very low temperatures'], 'It is a powerful qualitative model, especially for gases, but has limited predictive power for condensed phases – models are simplifications (NOS).')],
    extended=[('A heating curve is obtained for a pure sample of ethanol heated from −130 °C to 100 °C (melting point −114 °C, boiling point 78 °C). Sketch and describe the curve, explaining each section in terms of particles and energy.', 'Rising section (solid warming: vibrations increase); plateau at −114 °C (melting: energy overcomes attractions, temperature constant); rising section (liquid warming); longer plateau at 78 °C (boiling: particles separate completely); rising section (gas warming). Gradients depend on heat capacities.', 6, 'multi_step')],
))

SUBST = [('ethanol', -114, 78), ('water', 0, 100), ('mercury', -39, 357), ('bromine', -7, 59), ('methane', -182, -162),
         ('iodine', 114, 184), ('benzene', 6, 80), ('sodium chloride', 801, 1413), ('sulfur', 115, 445),
         ('ammonia', -78, -33), ('propanone', -95, 56), ('octane', -57, 126), ('chlorine', -102, -34), ('gallium', 30, 2400)]


@R.add('ch01-st2', 'C3', (1, 3), 'short')
def c3_state(rng, slot):
    s, mp, bp = pick(rng, SUBST)
    t = rng.choice([mp - rng.randint(5, 40), (mp + bp) // 2, bp + rng.randint(5, 60)])
    st_ = 'solid' if t < mp else 'gas' if t > bp else 'liquid'
    if slot.d <= 1 or rng.random() < 0.5:
        stem = f'{s.capitalize()} has a melting point of {mp} °C and a boiling point of {bp} °C. State its physical state at {t} °C.'
        return dict(stem=stem, answer=st_, markingKey=f'{st_} ({t} °C is {"below the melting point" if st_ == "solid" else "above the boiling point" if st_ == "gas" else "between the melting and boiling points"}) (1).', type='short', marks=1)
    tk = t + 273
    stem = f'The melting point of {s} is {mp + 273} K and its boiling point is {bp + 273} K. Deduce the physical state of {s} at {t} °C, showing your reasoning.'
    return dict(stem=stem, answer=f'{st_} ({t} °C = {tk} K)', markingKey=f'Converts {t} °C to {tk} K (M1); compares with {mp + 273} K and {bp + 273} K to give {st_} (A1).', type='short', marks=2)


@R.add('ch01-st2', 'C1', (1, 2), 'numerical')
def c1_kelvin(rng, slot):
    if rng.random() < 0.5:
        c = rng.choice([-196, -78, -40, 0, 18, 25, 37, 60, 100, 250, 450, 1083, -183, -33])
        return num(f'Convert {c} °C to kelvin.', f'{c + 273} K', f'T/K = {c} + 273 = {c + 273} K (A1).', 1)
    k = rng.choice([77, 195, 250, 273, 310, 350, 400, 623, 1000, 90])
    return num(f'Convert {k} K to degrees Celsius.', f'{k - 273} °C', f'T/°C = {k} − 273 = {k - 273} °C (A1).', 1)


@R.add('ch01-st2', 'C3', (2, 4), 'mcq')
def c3_ke_ratio(rng, slot):
    t1 = rng.choice([-73, 0, 27, 50, 127, 227, 77])
    t2 = rng.choice([t for t in [127, 327, 227, 527, 100, 373, 427] if t > t1])
    r = (t2 + 273) / (t1 + 273)
    stem = f'The temperature of a sample of {pick(rng, ["helium", "argon", "nitrogen", "neon", "oxygen"])} gas is raised from {t1} °C to {t2} °C. By what factor does the average kinetic energy of the particles increase?'
    wrongs = [t2 / t1 if t1 not in (0,) else 2 * r + 1, (t2 - t1) / 273 + 0.5, r ** 2, math.sqrt(r)]
    return nmcq(rng, stem, r, wrongs, '', f'Ek ∝ T/K: ({t2} + 273)/({t1} + 273) = {sf(r)}. Using Celsius values is the common error.', extra=False)


@R.add('ch01-st2', 'C3', (2, 4), 'short')
def c3_heating_curve(rng, slot):
    s, mp, bp = pick(rng, SUBST[:9])
    t0 = mp - rng.choice([20, 30, 40])
    t1 = bp + rng.choice([10, 20, 30])
    stem = (f'A pure sample of {s} is heated at a constant rate from {t0} °C to {t1} °C. The temperature–time graph shows two horizontal sections. '
            f'State the temperatures of the two horizontal sections and explain why the second horizontal section is longer than the first.')
    ans = f'{mp} °C (melting) and {bp} °C (boiling); boiling requires the intermolecular attractions to be overcome completely so far more energy (time) is needed than for melting.'
    return dict(stem=stem, answer=ans, markingKey=f'{mp} °C and {bp} °C (1); energy used to overcome attractions, temperature constant (1); vaporisation separates particles completely – greater enthalpy change than fusion (1).', type='explain', marks=3)


R.mcqs('ch01-st2', 'C2', (1, 4), [
    ('Which statement explains why a gas exerts pressure on the walls of its container?', 'Gas particles collide with the walls and change momentum.', ['Gas particles are attracted to the walls.', 'Gas particles expand when heated.', 'Gas particles are heavier than air.'], 'Pressure is force per unit area from collisions.'),
    ('Two gases are at the same temperature. Which quantity must be the same for both?', 'the average kinetic energy of the particles', ['the average speed of the particles', 'the mass of the particles', 'the density of the gas'], 'Average Ek depends only on T; lighter particles move faster.'),
    ('Why does the temperature of a liquid stay constant while it boils at constant pressure?', 'Energy is used to separate the particles rather than increase their kinetic energy.', ['The heater turns off.', 'The particles lose kinetic energy to the walls.', 'The bonds within molecules break.'], 'Latent heat increases potential energy.'),
    ('A sample of iodine is gently warmed and purple vapour forms with no liquid appearing. Which process occurs?', 'sublimation', ['evaporation', 'condensation', 'deposition'], 'Solid → gas directly.'),
    ('Which change increases the rate of evaporation of a liquid at constant temperature?', 'increasing the surface area of the liquid', ['increasing the depth of the liquid', 'covering the container', 'increasing the pressure above the liquid'], 'More particles at the surface can escape.'),
])


R.facts('ch01-st3', F(
    terms=[('isotopes', 'atoms of the same element with the same number of protons but different numbers of neutrons'),
           ('atomic number (Z)', 'the number of protons in the nucleus of an atom'),
           ('mass number (A)', 'the total number of protons and neutrons in the nucleus of an atom'),
           ('nucleon', 'a particle found in the nucleus: a proton or a neutron'),
           ('ion', 'a charged particle formed when an atom or group of atoms loses or gains electrons'),
           ('radioisotope', 'an isotope with an unstable nucleus that decays, emitting radiation')],
    facts=[('What is the relative mass of an electron compared with a proton?', 'about 1/1840 (5 × 10⁻⁴)', ['1', '0', '1/2'], 'Electron mass ≈ 1/1836 of a proton (data booklet: 5.4 × 10⁻⁴).'),
           ('Isotopes of an element have the same', 'number of protons and chemical properties', ['mass number', 'number of neutrons', 'physical properties'], 'Same Z and electron configuration so same chemistry; different A.'),
           ('Which particles are found in the nucleus of an atom?', 'protons and neutrons', ['protons and electrons', 'neutrons and electrons', 'only protons'], 'The nucleus contains the nucleons.'),
           ('Which isotope is used as the standard for relative atomic masses?', 'carbon-12', ['hydrogen-1', 'oxygen-16', 'carbon-14'], 'Ar is defined relative to 1/12 of the mass of a ¹²C atom.'),
           ('Which property differs between ³⁵Cl and ³⁷Cl atoms?', 'density of the gas', ['number of electrons', 'chemical reactivity', 'number of protons'], 'Isotopes differ in mass-dependent physical properties such as density and rate of diffusion.'),
           ('Which radioisotope is used in medical imaging and diagnosis?', 'technetium-99m', ['carbon-12', 'uranium-238', 'helium-4'], 'Tc-99m emits gamma rays and has a short half-life (6 h).')],
    why=[('Explain why isotopes of an element have identical chemical properties.', 'Chemical properties depend on the number and arrangement of electrons; isotopes have the same number of protons and therefore the same number of electrons and the same electron configuration.'),
         ('Explain why almost all the mass of an atom is concentrated in its nucleus.', 'Protons and neutrons each have a relative mass of about 1, whereas electrons have a relative mass of only about 1/1840.'),
         ('Explain why an atom is electrically neutral.', 'It contains equal numbers of protons (each +1) and electrons (each −1), so the charges cancel.'),
         ('Explain why carbon-14 is useful for dating archaeological samples.', 'Living organisms maintain a constant ¹⁴C:¹²C ratio; after death ¹⁴C decays with a known half-life (5730 years) so the remaining ratio indicates age.'),
         ('Explain why ³⁷Cl₂ gas diffuses more slowly than ³⁵Cl₂ gas at the same temperature.', 'At the same temperature the molecules have the same average kinetic energy; heavier ³⁷Cl₂ molecules therefore have a lower average speed.')],
    contrast=[('atomic number', 'mass number', 'Atomic number is the number of protons; mass number is the number of protons plus neutrons.'),
              ('an atom', 'an ion', 'An atom is neutral (protons = electrons); an ion is charged because it has lost or gained electrons.'),
              ('mass number', 'relative atomic mass', 'Mass number is a whole number for one isotope (p + n); relative atomic mass is the weighted mean mass of the naturally occurring isotopes relative to 1/12 of ¹²C, usually not a whole number.')],
    misc=[('Isotopes have different chemical properties because they have different masses.', 'Chemical properties depend on electron configuration, which is the same for isotopes; only mass-dependent physical properties differ.'),
          ('A Mg²⁺ ion has two more electrons than a magnesium atom.', 'A 2+ ion has lost two electrons: Mg²⁺ has 10 electrons, the Mg atom 12.'),
          ('The mass number is the number of neutrons in the nucleus.', 'The mass number is protons + neutrons; neutrons = A − Z.')],
    cases=[('radiocarbon dating of the Ötzi “iceman” found in the Alps', 'Measuring the remaining ¹⁴C in his tissue dated him to about 5300 years ago.', 'the use of radioisotopes', 'Isotopes of carbon behave identically chemically, so ¹⁴C is incorporated in living tissue, while its decay rate provides a clock.'),
           ('iodine-131 treatment for thyroid cancer', 'Patients swallow ¹³¹I which the thyroid absorbs like ordinary iodine; its beta radiation destroys thyroid tissue.', 'identical chemical properties of isotopes', 'The body cannot distinguish ¹³¹I from ¹²⁷I chemically, so the radioisotope goes exactly where iodine is used.'),
           ('cobalt-60 used to sterilise surgical equipment', 'Gamma rays from ⁶⁰Co kill bacteria on packaged instruments.', 'applications of radioisotopes', 'Highly penetrating gamma radiation from an unstable nucleus can sterilise without heating.')],
    evaluate=[('The use of radioisotopes in medicine brings more benefits than risks.', ['diagnosis with tracers (Tc-99m) is non-invasive', 'targeted therapy (I-131) treats cancers effectively', 'short half-lives limit exposure'], ['ionising radiation can damage healthy cells and DNA', 'risks to staff and in disposal of waste', 'production requires nuclear reactors'], 'With careful choice of isotope (short half-life, appropriate radiation) and dose control the benefits generally outweigh the risks.')],
    extended=[('Gallium has two stable isotopes, ⁶⁹Ga and ⁷¹Ga. (a) State the number of protons, neutrons and electrons in a ⁷¹Ga³⁺ ion. (b) Explain why the two isotopes react identically with hydrochloric acid. (c) Suggest one physical property that would differ between samples of the pure isotopes.', '(a) 31 p, 40 n, 28 e; (b) same electron configuration/same number of electrons; (c) density (or rate of diffusion, melting point slightly).', 4, 'multi_step')],
))

ISO = [('H', 1, 2), ('H', 1, 3), ('C', 6, 13), ('C', 6, 14), ('N', 7, 15), ('O', 8, 18), ('F', 9, 19), ('Na', 11, 23),
       ('Mg', 12, 26), ('Al', 13, 27), ('P', 15, 31), ('S', 16, 34), ('Cl', 17, 35), ('Cl', 17, 37), ('K', 19, 39),
       ('Ca', 20, 44), ('Fe', 26, 56), ('Co', 27, 60), ('Cu', 29, 63), ('Cu', 29, 65), ('Zn', 30, 64), ('Br', 35, 79),
       ('Br', 35, 81), ('Sr', 38, 90), ('I', 53, 131), ('U', 92, 235), ('U', 92, 238), ('Tc', 43, 99), ('Ag', 47, 107),
       ('Pb', 82, 208), ('Li', 3, 7), ('B', 5, 11), ('Si', 14, 30), ('Ar', 18, 40), ('Ti', 22, 48)]
CHARGES = {'H': [1, -1], 'Na': [1], 'Mg': [2], 'Al': [3], 'K': [1], 'Ca': [2], 'Fe': [2, 3], 'Cu': [1, 2], 'Zn': [2], 'Sr': [2],
           'Li': [1], 'Ag': [1], 'Pb': [2], 'Co': [2, 3], 'Ti': [4], 'F': [-1], 'Cl': [-1], 'Br': [-1], 'I': [-1], 'O': [-2],
           'S': [-2], 'N': [-3], 'P': [-3]}


def nuc(sym, z, a, ch=0):
    c = '' if ch == 0 else sup(('' if abs(ch) == 1 else str(abs(ch))) + ('+' if ch > 0 else '-'))
    return f'{sup(a)}{sym}{c}'


@R.add('ch01-st3', 'C1', (1, 3), 'short')
def c1_pne(rng, slot):
    sym, z, a = pick(rng, ISO)
    ch = rng.choice([0] + CHARGES.get(sym, [])) if slot.d >= 2 else 0
    e = z - ch
    n = a - z
    stem = pick(rng, [f'State the number of protons, neutrons and electrons in {nuc(sym, z, a, ch)} (Z = {z}).',
                      f'Deduce the numbers of subatomic particles in the species {sym}-{a}{"" if ch == 0 else " as the " + ion(sym + ("" if abs(ch) == 1 else str(abs(ch))) + ("+" if ch > 0 else "-")) + " ion"}. The atomic number of {sym} is {z}.'])
    return dict(stem=stem, answer=f'{z} protons, {n} neutrons, {e} electrons', markingKey=f'p = Z = {z}; n = A − Z = {a} − {z} = {n}; e = {z} − ({ch}) = {e}. (2 marks for all three correct, 1 mark for two.)', type='short', marks=2)


@R.add('ch01-st3', 'C3', (1, 4), 'mcq')
def c3_iso_mcq(rng, slot):
    pool = rng.sample(ISO, 4)
    kind = rng.choice(['more_n', 'equal_np', 'most_n'])
    if kind == 'more_n':
        # which has more neutrons than protons by largest margin
        best = max(pool, key=lambda t: t[2] - 2 * t[1])
        if sum(1 for t in pool if t[2] - 2 * t[1] == best[2] - 2 * best[1]) > 1:
            return None
        stem = 'Which atom has the greatest excess of neutrons over protons?'
        why = f'{nuc(*best)}: n − p = {best[2] - best[1]} − {best[1]} = {best[2] - 2 * best[1]}.'
    elif kind == 'most_n':
        best = max(pool, key=lambda t: t[2] - t[1])
        if sum(1 for t in pool if t[2] - t[1] == best[2] - best[1]) > 1:
            return None
        stem = 'Which atom contains the largest number of neutrons?'
        why = f'{nuc(*best)} has {best[2] - best[1]} neutrons (A − Z).'
    else:
        eq = [t for t in ISO if t[2] == 2 * t[1]]
        best = pick(rng, eq)
        others = [t for t in ISO if t[2] != 2 * t[1]]
        pool = [best] + rng.sample(others, 3)
        stem = 'Which atom contains equal numbers of protons, neutrons and electrons?'
        why = f'{nuc(*best)}: Z = {best[1]}, n = {best[2] - best[1]}.'
    return mcq(rng, stem + ' (Atomic numbers: ' + ', '.join(f'{t[0]} {t[1]}' for t in dict.fromkeys(pool)) + ')',
               nuc(*best), [nuc(*t) for t in pool if t != best][:3], why)


@R.add('ch01-st3', 'C3', (2, 4), 'mcq')
def c3_ion_mcq(rng, slot):
    sym, z, a = pick(rng, [t for t in ISO if CHARGES.get(t[0])])
    ch = pick(rng, CHARGES[sym])
    e = z - ch
    n = a - z
    stem = f'How many electrons and neutrons are present in {nuc(sym, z, a, ch)}? (Z = {z})'
    right = f'{e} electrons, {n} neutrons'
    wrongs = [f'{z + ch} electrons, {n} neutrons', f'{e} electrons, {a} neutrons', f'{z} electrons, {n} neutrons', f'{n} electrons, {e} neutrons']
    return mcq(rng, stem, right, [w for w in wrongs if w != right][:3], f'electrons = {z} − ({ch}) = {e}; neutrons = {a} − {z} = {n}.')


@R.add('ch01-st3', 'C3', (2, 5), 'short')
def c3_identify(rng, slot):
    sym, z, a = pick(rng, ISO)
    ch = rng.choice([0] + CHARGES.get(sym, []))
    e = z - ch
    n = a - z
    stem = f'A species contains {z} protons, {n} neutrons and {e} electrons. Identify the species, giving its nuclear symbol with mass number{" and charge" if ch else ""}.'
    return dict(stem=stem, answer=nuc(sym, z, a, ch), markingKey=f'Element from Z = {z}: {sym} (1); mass number {a} = {z} + {n} (1); ' + (f'charge {ch:+d} from {z} − {e} (1).' if ch else 'neutral as p = e (1).'), type='short', marks=3)


R.mcqs('ch01-st3', 'C2', (1, 4), [
    ('Which pair of species has the same number of electrons?', 'Na⁺ and F⁻', ['Na and Na⁺', 'Cl⁻ and Br⁻', 'Mg²⁺ and Ca²⁺'], 'Both have 10 electrons (isoelectronic).'),
    ('Why do ¹²C and ¹⁴C have the same chemical properties?', 'They have the same electron configuration.', ['They have the same mass number.', 'They have the same number of nucleons.', 'They are both stable.'], 'Chemistry depends on electrons.'),
    ('Which statement about the ¹H, ²H and ³H isotopes is correct?', 'They each have one proton but different numbers of neutrons.', ['They each have one neutron.', 'They have different numbers of electrons.', 'Only ¹H is an isotope of hydrogen.'], 'Same Z = 1; n = 0, 1, 2.'),
    ('An ion X²⁻ has 18 electrons and 16 neutrons. What is the mass number of X?', '32', ['34', '36', '18'], 'Z = 18 − 2 = 16; A = 16 + 16 = 32.'),
    ('An ion Y³⁺ has 10 electrons and 14 neutrons. What is its mass number?', '27', ['24', '21', '17'], 'Z = 13; A = 13 + 14 = 27 (aluminium).'),
])


R.facts('ch01-st4', F(
    terms=[('relative atomic mass (Ar)', 'the weighted mean mass of the atoms of an element, taking account of the abundances of its isotopes, relative to one-twelfth of the mass of a carbon-12 atom'),
           ('mass spectrometer', 'an instrument that ionises a sample and separates the ions by their mass-to-charge ratio to give a spectrum of relative abundance against m/z'),
           ('percentage abundance', 'the percentage of the atoms of an element that are a particular isotope'),
           ('mass-to-charge ratio (m/z)', 'the quantity on the horizontal axis of a mass spectrum; for singly charged ions it equals the relative mass of the ion')],
    facts=[('In a mass spectrum of an element, what does the height of each peak represent?', 'the relative abundance of that isotope', ['the mass of that isotope', 'the number of neutrons in the isotope', 'the charge on the ion'], 'Peak height ∝ number of ions of that m/z.'),
           ('Why is the relative atomic mass of chlorine (35.45) not a whole number?', 'It is a weighted mean of the masses of ³⁵Cl and ³⁷Cl.', ['Chlorine atoms contain a fraction of a neutron.', 'Electrons have a large mass.', 'It is measured relative to hydrogen.'], 'Ar is an abundance-weighted mean.'),
           ('What is plotted on the x-axis of a mass spectrum?', 'mass-to-charge ratio (m/z)', ['relative abundance', 'time', 'wavelength'], 'Ions are separated by m/z.'),
           ('A mass spectrum of Cl₂ shows peaks at m/z 70, 72 and 74. What causes the peak at m/z 72?', '³⁵Cl–³⁷Cl⁺ molecular ions', ['³⁷Cl⁺ ions with 2+ charge', '³⁵Cl₂²⁺ ions', '⁷²Ge contamination'], '35 + 37 = 72.')],
    why=[('Explain why the relative atomic mass of copper (63.55) is closer to 63 than to 65.', 'Copper consists of ⁶³Cu and ⁶⁵Cu; the weighted mean lies closer to 63 because ⁶³Cu is the more abundant isotope (about 69 %).'),
         ('Explain why a mass spectrum of naturally occurring bromine, Br₂, shows three molecular-ion peaks.', 'Bromine has two isotopes (⁷⁹Br and ⁸¹Br) in roughly equal amounts, so Br₂ molecules can be ⁷⁹Br⁷⁹Br (158), ⁷⁹Br⁸¹Br (160) or ⁸¹Br⁸¹Br (162), in ratio about 1:2:1.'),
         ('Explain why relative atomic masses have no units.', 'They are ratios: the mean mass of an atom divided by one-twelfth of the mass of a carbon-12 atom, so the units cancel.')],
    contrast=[('relative atomic mass', 'relative isotopic mass', 'Relative isotopic mass is the mass of one isotope relative to 1/12 of ¹²C; relative atomic mass is the abundance-weighted mean of the isotopic masses of the element.')],
    misc=[('The relative atomic mass of an element is the mass number of its most common isotope.', 'Ar is the weighted mean of all isotopes present, so it is usually not a whole number (e.g. Cl 35.45, not 35).'),
          ('In the mass spectrum of chlorine the peak at m/z 37 is the tallest because ³⁷Cl is heavier.', 'Peak height shows abundance, not mass: the ³⁵Cl peak is about three times taller because ³⁵Cl is about 75 % of chlorine atoms.')],
    evaluate=[('Relative atomic masses quoted to two decimal places in the data booklet are exact constants of nature.', ['they are measured very precisely by mass spectrometry', 'used consistently in calculations worldwide'], ['isotopic abundances vary slightly with the source of a sample (e.g. boron, lead)', 'IUPAC now gives some Ar values as intervals', 'precision is limited by measurement'], 'They are conventional representative values; small natural variations mean they are not exact constants, which matters in high-precision work.')],
))

ELEM_ISO = [('chlorine', 'Cl', [(35, 75.78), (37, 24.22)]), ('copper', 'Cu', [(63, 69.15), (65, 30.85)]),
            ('bromine', 'Br', [(79, 50.69), (81, 49.31)]), ('boron', 'B', [(10, 19.9), (11, 80.1)]),
            ('lithium', 'Li', [(6, 7.59), (7, 92.41)]), ('gallium', 'Ga', [(69, 60.11), (71, 39.89)]),
            ('silver', 'Ag', [(107, 51.84), (109, 48.16)]), ('magnesium', 'Mg', [(24, 78.99), (25, 10.00), (26, 11.01)]),
            ('silicon', 'Si', [(28, 92.23), (29, 4.68), (30, 3.09)]), ('rubidium', 'Rb', [(85, 72.17), (87, 27.83)]),
            ('antimony', 'Sb', [(121, 57.21), (123, 42.79)]), ('iridium', 'Ir', [(191, 37.3), (193, 62.7)]),
            ('europium', 'Eu', [(151, 47.81), (153, 52.19)]), ('thallium', 'Tl', [(203, 29.52), (205, 70.48)])]


@R.add('ch01-st4', 'C3', (1, 4), 'numerical')
def c3_ar(rng, slot):
    nm, sym, iso = pick(rng, ELEM_ISO)
    if rng.random() < 0.4:  # perturbed hypothetical sample (e.g. from a meteorite)
        iso = [(m, a) for m, a in iso]
        if len(iso) == 2:
            a0 = round(iso[0][1] + rng.uniform(-6, 6), 1)
            iso = [(iso[0][0], a0), (iso[1][0], round(100 - a0, 1))]
        ctx = pick(rng, ['A sample of {} from a meteorite', 'An isotopically enriched sample of {}', 'A sample of {} analysed in a geology laboratory'])
    else:
        ctx = pick(rng, ['Naturally occurring {}', 'A sample of {} from a mineral', '{} extracted from ore'])
    ctx = ctx.format(nm)
    ar = sum(m * a for m, a in iso) / 100
    tab = ', '.join(f'{sup(m)}{sym} {a} %' for m, a in iso)
    stem = f'{ctx[0].upper() + ctx[1:]} has the following isotopic composition: {tab}. Calculate the relative atomic mass of {sym} in this sample to two decimal places.'
    wrong = sum(m for m, _ in iso) / len(iso)
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Calculate the', 'What is the'), ar, [wrong, sum(m * a for m, a in iso), iso[0][0] * iso[1][1] / 100 + iso[1][0] * iso[0][1] / 100 if len(iso) == 2 else wrong + 0.5], '',
                    f'Ar = Σ(mass × abundance)/100 = {ar:.2f}. A simple mean of the masses ({wrong:.2f}) ignores abundance.', n=4, extra=True)
    return num(stem, f'{ar:.2f}', 'Ar = (' + ' + '.join(f'{m} × {a}' for m, a in iso) + f')/100 (M1) = {ar:.2f} (A1).', 2)


@R.add('ch01-st4', 'C3', (2, 5), 'numerical')
def c3_abundance(rng, slot):
    nm, sym, iso = pick(rng, [e for e in ELEM_ISO if len(e[2]) == 2])
    (m1, a1), (m2, a2) = iso
    ar = round((m1 * a1 + m2 * a2) / 100, 2)
    x = (ar - m2) / (m1 - m2) * 100
    stem = pick(rng, [f'{nm.capitalize()} has two isotopes, {sup(m1)}{sym} and {sup(m2)}{sym}, and a relative atomic mass of {ar:.2f}. Calculate the percentage abundance of each isotope.',
                      f'The relative atomic mass of a sample of {nm} is {ar:.2f}. The sample contains only {sup(m1)}{sym} and {sup(m2)}{sym}. Determine the percentage of {sup(m1)}{sym} atoms in the sample.'])
    return num(stem, f'{sup(m1)}{sym} {x:.1f} %, {sup(m2)}{sym} {100 - x:.1f} %', f'Let x = % of {sup(m1)}{sym}: {m1}x + {m2}(100 − x) = {ar:.2f} × 100 (M1); x = {x:.1f} % (A1); other isotope {100 - x:.1f} % (A1).', 3)


@R.add('ch01-st4', 'C4', (3, 5), 'multi_step')
def c4_diatomic(rng, slot):
    nm, sym, iso = pick(rng, [('chlorine', 'Cl', (35, 37)), ('bromine', 'Br', (79, 81))])
    p = rng.choice([0.75, 0.7, 0.6, 0.5, 0.8]) if sym == 'Cl' else rng.choice([0.5, 0.55, 0.6, 0.45])
    a, b = iso
    r = (p * p, 2 * p * (1 - p), (1 - p) ** 2)
    mx = max(r)
    rel = [x / mx * 100 for x in r]
    stem = (f'A sample of {nm} contains {p * 100:.0f} % {sup(a)}{sym} and {(1 - p) * 100:.0f} % {sup(b)}{sym}. '
            f'(a) State the m/z values of the molecular-ion peaks expected for {sym}₂⁺. (b) Calculate the relative heights of these peaks, taking the tallest as 100. (c) Calculate Ar for this sample.')
    ar = p * a + (1 - p) * b
    ans = f'(a) {2 * a}, {a + b}, {2 * b}; (b) {rel[0]:.0f} : {rel[1]:.0f} : {rel[2]:.0f}; (c) {ar:.2f}'
    key = f'(a) {2 * a}, {a + b}, {2 * b} (A1). (b) probabilities {p:.2f}² = {r[0]:.3f}, 2 × {p:.2f} × {1 - p:.2f} = {r[1]:.3f}, {1 - p:.2f}² = {r[2]:.3f} (M1); scaled {rel[0]:.0f} : {rel[1]:.0f} : {rel[2]:.0f} (A1). (c) {ar:.2f} (A1).'
    return num(stem, ans, key, 5, 'multi_step')


R.mcqs('ch01-st4', 'C2', (1, 4), [
    ('Element X has two isotopes, ¹⁰X and ¹¹X, and Ar = 10.8. Which statement is correct?', '¹¹X is more abundant than ¹⁰X.', ['¹⁰X is more abundant than ¹¹X.', 'The isotopes are equally abundant.', 'X has a third isotope of mass 12.'], 'The mean is nearer 11.'),
    ('A mass spectrum of an element shows peaks at m/z 24 (79 %), 25 (10 %) and 26 (11 %). What is the element?', 'magnesium', ['sodium', 'carbon', 'chromium'], 'Ar ≈ 24.3 – magnesium.'),
    ('Which change would NOT affect the position (m/z) of a peak in a mass spectrum?', 'increasing the amount of sample', ['changing the isotope', 'forming a 2+ ion instead of a 1+ ion', 'fragmentation of the molecule'], 'The amount changes abundance (height), not m/z.'),
    ('Why does the mass spectrum of neon show a small peak at m/z 10?', 'some ²⁰Ne atoms form ²⁰Ne²⁺ ions', ['¹⁰Ne is an isotope of neon', 'neon combines with hydrogen', 'electrons are detected'], 'm/z = 20/2 = 10.'),
])


@p1b(R, 'ch01-st4')
def p1b_mass_spec(rng, slot):
    nm, sym, iso = pick(rng, [e for e in ELEM_ISO if len(e[2]) == 3] + [e for e in ELEM_ISO if e[0] in ('copper', 'gallium', 'boron', 'rubidium')])
    tot = sum(a for _, a in iso)
    hts = [round(a / max(a for _, a in iso) * 100, 1) for _, a in iso]
    tab = '\n'.join(f'm/z {m} | relative peak height {h}' for (m, _), h in zip(iso, hts))
    ar = sum(m * h for (m, _), h in zip(iso, hts)) / sum(hts)
    intro = f'The mass spectrum of a sample of {nm} gave the following peaks (singly charged ions only):\n{tab}'
    return dict(intro=intro, parts=[
        ('Calculate the percentage abundance of each isotope.', ', '.join(f'{m}: {h / sum(hts) * 100:.1f} %' for (m, _), h in zip(iso, hts)), 'Each height ÷ sum of heights × 100 (M1); correct percentages (A1).', 2),
        ('Calculate the relative atomic mass of the sample to two decimal places.', f'{ar:.2f}', f'Σ(m/z × height)/Σheights (M1) = {ar:.2f} (A1).', 2),
        ('Identify the element from its relative atomic mass and state one reason why the value may differ slightly from the data booklet value.', f'{nm}; isotopic abundances vary slightly between natural sources / peak-height measurement uncertainty.', f'{nm} (1); valid reason (1).', 2),
        ('Explain why the sample must be ionised before it can be analysed.', 'Only charged particles can be accelerated and deflected (separated) by electric/magnetic fields and detected.', 'Ions are accelerated/deflected/detected (1).', 1)],
        extras=[('State why a small peak at half the m/z of the most abundant isotope could appear.', 'Formation of 2+ ions, which have half the m/z value.', '2+ ions (1).', 1)])


# =============================================================================================
# ch02 S1.3 Electron configurations
# =============================================================================================
ORDER = [('1s', 2), ('2s', 2), ('2p', 6), ('3s', 2), ('3p', 6), ('4s', 2), ('3d', 10), ('4p', 6), ('5s', 2), ('4d', 10), ('5p', 6)]
EXC = {24: {'4s': 1, '3d': 5}, 29: {'4s': 1, '3d': 10}}


def config(zz):
    """Ground-state configuration as an ordered list of (sublevel, electrons), written in n order."""
    left = zz
    occ = {}
    for sl, cap in ORDER:
        if left <= 0:
            break
        k = min(cap, left)
        occ[sl] = k
        left -= k
    if zz in EXC:
        occ.update(EXC[zz])
    return sorted(occ.items(), key=lambda t: (int(t[0][0]), 'spdf'.index(t[0][1])))


def config_ion(zz, ch):
    occ = dict(config(zz))
    rem = ch
    # remove from highest n first (4p, then 4s before 3d)
    for sl in sorted(occ, key=lambda s: (-int(s[0]), -'spdf'.index(s[1]))):
        while rem > 0 and occ[sl] > 0:
            occ[sl] -= 1
            rem -= 1
    if ch < 0:
        return config(zz - ch)
    return sorted([(k, v) for k, v in occ.items() if v > 0], key=lambda t: (int(t[0][0]), 'spdf'.index(t[0][1])))


def cfg_s(c):
    return ' '.join(f'{sl}{sup(n)}' for sl, n in c)


NOBLE = [(2, 'He'), (10, 'Ne'), (18, 'Ar'), (36, 'Kr')]


def cfg_short(c):
    tot = sum(n for _, n in c)
    core = max((g for g in NOBLE if g[0] <= tot), default=None)
    if core is None:
        return cfg_s(c)
    core_cfg = dict(config(core[0]))
    rest = [(sl, n) for sl, n in c if not (sl in core_cfg and core_cfg[sl] == n)]
    return f'[{core[1]}] ' + cfg_s(rest) if rest else f'[{core[1]}]'


def unpaired(c):
    tot = 0
    for sl, n in c:
        orb = {'s': 1, 'p': 3, 'd': 5}[sl[1]]
        tot += n if n <= orb else 2 * orb - n
    return tot


R.facts('ch02-st1', F(
    terms=[('emission spectrum', 'the pattern of specific frequencies (lines) of electromagnetic radiation emitted when excited electrons fall to lower energy levels'),
           ('continuous spectrum', 'a spectrum containing all wavelengths (colours) over a range, with no gaps, such as that of white light'),
           ('line spectrum', 'a spectrum consisting of discrete lines at particular frequencies, produced by transitions between fixed energy levels'),
           ('ground state', 'the lowest-energy arrangement of the electrons in an atom'),
           ('excited state', 'an arrangement in which one or more electrons occupy higher energy levels than in the ground state'),
           ('convergence', 'the decrease in spacing between spectral lines at higher frequency, as energy levels get closer together')],
    facts=[('Which transition in a hydrogen atom produces a line in the visible region of the spectrum?', 'n = 3 → n = 2', ['n = 2 → n = 1', 'n = 4 → n = 3', 'n = 1 → n = 2'], 'Transitions to n = 2 give the visible (Balmer) series.'),
           ('Transitions to which energy level give the ultraviolet lines of the hydrogen spectrum?', 'n = 1', ['n = 2', 'n = 3', 'n = ∞'], 'The Lyman series (to n = 1) is in the UV.'),
           ('Which colour of visible light has the highest energy per photon?', 'violet', ['red', 'yellow', 'green'], 'Violet has the shortest wavelength and highest frequency.'),
           ('How does the spacing of lines change in the hydrogen emission spectrum at higher frequency?', 'The lines get closer together (converge).', ['The lines get further apart.', 'The spacing stays the same.', 'The lines disappear.'], 'Energy levels converge at higher n.'),
           ('What is the relationship between the energy of a photon and its frequency?', 'E = hf (directly proportional)', ['E = h/f', 'E = hf²', 'E = f/h'], 'Planck relation, data booklet.')],
    why=[('Explain why the hydrogen emission spectrum consists of lines rather than a continuous band.', 'Electrons can only occupy fixed (quantised) energy levels; each line corresponds to a transition between two levels and so a photon of one specific energy (frequency, E = hf).'),
         ('Explain why lines in the hydrogen emission spectrum converge at higher frequencies.', 'The energy levels get closer together as n increases, so the energy differences for transitions from high n to the same lower level become more similar.'),
         ('Explain how the emission spectrum of an element can be used to identify it.', 'Each element has a unique set of energy levels, so the pattern of lines (frequencies) emitted is characteristic of that element, like a fingerprint.'),
         ('Explain why the Lyman series lines have higher energy than the Balmer series lines.', 'Lyman transitions end at n = 1; the gap between n = 1 and any higher level is larger than the gap to n = 2, so photons emitted have greater energy (UV rather than visible).')],
    contrast=[('a continuous spectrum', 'a line spectrum', 'A continuous spectrum contains all wavelengths in a range; a line spectrum contains only specific wavelengths corresponding to transitions between discrete energy levels.'),
              ('an emission spectrum', 'an absorption spectrum', 'An emission spectrum shows bright lines from photons emitted as electrons fall to lower levels; an absorption spectrum shows dark lines at the same frequencies where photons are absorbed as electrons are promoted.')],
    misc=[('Each line in the hydrogen spectrum is produced when an electron jumps up to a higher energy level.', 'Emission lines come from electrons falling from higher to lower levels and emitting photons; promotion absorbs energy (absorption spectrum).'),
          ('Red light photons have more energy than blue light photons because red is at the top of the spectrum.', 'Red has a longer wavelength and lower frequency, so by E = hf its photons have less energy than blue.')],
    cases=[('the discovery of helium in the Sun in 1868', 'Astronomers observed a yellow line (587.6 nm) in the solar spectrum that matched no known element.', 'line spectra as fingerprints of elements', 'Because each element has unique energy levels, an unknown line implied a new element, later found on Earth.'),
           ('flame tests used to identify metal ions in a laboratory', 'Sodium gives a yellow-orange flame, lithium crimson, copper(II) blue-green.', 'emission spectra', 'Heat excites electrons; their return to lower levels emits photons of characteristic frequencies.'),
           ('sodium street lamps', 'Low-pressure sodium lamps emit almost monochromatic light at about 589 nm.', 'electron transitions between fixed energy levels', 'The dominant 3p → 3s transition in sodium emits photons of one energy, hence one colour.')],
    evaluate=[('The Bohr model of the atom is adequate for explaining atomic spectra.', ['explains the hydrogen line spectrum and convergence quantitatively', 'introduces quantised energy levels'], ['fails for atoms with more than one electron', 'cannot explain sublevels, orbital shapes or relative line intensities', 'replaced by quantum mechanical model with orbitals'], 'Bohr explains hydrogen well but is limited; the orbital (quantum mechanical) model is needed for multi-electron atoms – theories are refined in light of evidence.')],
))

LAMBDA_COL = [(410, 'violet'), (434, 'blue-violet'), (486, 'blue-green'), (656, 'red'), (589, 'yellow-orange'), (540, 'green'), (700, 'red')]


def h_level(n):
    return -1312 / n ** 2  # kJ mol⁻¹


@R.add('ch02-st1', 'C3', (1, 5), 'numerical')
def c3_photon(rng, slot):
    kind = rng.choice(['lam_E', 'f_lam', 'E_lam', 'trans'])
    if kind == 'trans' or slot.d >= 4:
        hi = rng.randint(3, 7)
        lo = rng.choice([1, 2, 2, 3]) if hi > 3 else rng.choice([1, 2])
        if lo >= hi:
            return None
        dE = h_level(hi) - h_level(lo)  # kJ mol-1 positive
        Ej = dE * 1000 / NA
        lam = H_PLANCK * C_LIGHT / Ej * 1e9
        region = 'ultraviolet' if lam < 400 else 'visible' if lam < 700 else 'infrared'
        stem = (f'The energy of an electron in level n of a hydrogen atom is given by Eₙ = −1312/n² kJ mol⁻¹. '
                f'Calculate the wavelength, in nm, of the photon emitted when an electron falls from n = {hi} to n = {lo}, and state the region of the electromagnetic spectrum.')
        return num(stem, f'{sf(lam)} nm ({region})', f'ΔE = 1312(1/{lo}² − 1/{hi}²) = {sf(dE)} kJ mol⁻¹ (M1); per photon = {sf(dE)} × 10³/6.02 × 10²³ = {sf(Ej)} J (M1); λ = hc/E = {sf(lam)} nm (A1); {region} (A1).', 4, 'multi_step')
    lam = rng.choice([121.6, 102.6, 410.2, 434.0, 486.1, 656.3, 589.0, 253.7, 365.0, 1875])
    f = C_LIGHT / (lam * 1e-9)
    E = H_PLANCK * f
    Em = E * NA / 1000
    who = name(rng)
    if kind == 'f_lam':
        stem = f'{who} measures a spectral line at {lam} nm. Calculate the frequency of this radiation.'
        return num(stem, q(f, 'Hz'), f'f = c/λ = 3.00 × 10⁸/({lam} × 10⁻⁹) (M1) = {q(f, "Hz")} (A1). Conversion of nm to m required.', 2)
    if kind == 'lam_E':
        stem = f'Calculate the energy of one photon of wavelength {lam} nm.'
        if slot.d <= 2:
            return nmcq(rng, stem.replace('Calculate', 'What is'), E, [H_PLANCK * C_LIGHT / lam, E * NA, H_PLANCK * lam * 1e-9 / C_LIGHT * 1e34 * 1e-19], 'J', f'E = hc/λ = (6.63 × 10⁻³⁴ × 3.00 × 10⁸)/({lam} × 10⁻⁹) = {q(E, "J")}.', extra=True)
        return num(stem, q(E, 'J'), f'E = hc/λ (M1) = 6.63 × 10⁻³⁴ × 3.00 × 10⁸/({lam} × 10⁻⁹) = {q(E, "J")} (A1).', 2)
    stem = f'Calculate the energy, in kJ mol⁻¹, carried by one mole of photons of wavelength {lam} nm.'
    return num(stem, q(Em, 'kJ mol⁻¹'), f'E(photon) = hc/λ = {q(E, "J")} (M1); × 6.02 × 10²³ ÷ 1000 (M1) = {q(Em, "kJ mol⁻¹")} (A1).', 3)


@R.add('ch02-st1', 'C3', (2, 4), 'mcq')
def c3_series_mcq(rng, slot):
    hi = rng.randint(3, 7)
    lo = rng.choice([1, 2])
    lam = H_PLANCK * C_LIGHT / ((h_level(hi) - h_level(lo)) * 1000 / NA) * 1e9
    region = 'ultraviolet' if lam < 400 else 'visible'
    stem = f'An electron in a hydrogen atom falls from n = {hi} to n = {lo}. Which describes the emitted radiation?'
    other = 'visible' if region == 'ultraviolet' else 'ultraviolet'
    right = f'{region}, wavelength {sf(lam)} nm'
    wr = [f'{other}, wavelength {sf(lam)} nm', f'{region}, wavelength {sf(lam * 2.3)} nm', f'infrared, wavelength {sf(lam * 4.1)} nm']
    return mcq(rng, stem, right, wr, f'ΔE = 1312(1/{lo}² − 1/{hi}²) kJ mol⁻¹ → λ = {sf(lam)} nm ({region}; transitions to n = 1 are UV, to n = 2 visible).')


R.mcqs('ch02-st1', 'C2', (1, 4), [
    ('Which statement explains why the line spectrum of hydrogen provides evidence for energy levels?', 'Only photons of specific energies are emitted.', ['Photons of all energies are emitted.', 'Hydrogen atoms have only one electron.', 'The lines are all in the visible region.'], 'Discrete lines → discrete levels.'),
    ('As the frequency of electromagnetic radiation increases, which also increases?', 'photon energy', ['wavelength', 'speed in a vacuum', 'amplitude'], 'E = hf; c is constant so λ falls.'),
    ('The line with the longest wavelength in the visible hydrogen spectrum corresponds to which transition?', 'n = 3 → n = 2', ['n = 6 → n = 2', '∞ → n = 2', 'n = 2 → n = 1'], 'Smallest energy gap ending at n = 2 → red line 656 nm.'),
    ('Which change in an atom produces a dark line in an absorption spectrum?', 'an electron is promoted to a higher energy level by absorbing a photon', ['an electron falls to a lower level', 'the atom loses a proton', 'the atom emits a photon'], 'Absorption removes that frequency from the transmitted light.'),
])

EXAMPLE_Z = [z for z in range(1, 37)]


def esym(zz):
    return ELEMENTS_LIST[zz - 1]


ELEMENTS_LIST = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
                 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr']

R.facts('ch02-st2', F(
    terms=[('atomic orbital', 'a region of space around the nucleus in which there is a high probability of finding an electron; each orbital holds a maximum of two electrons'),
           ('Aufbau principle', 'electrons occupy the lowest-energy orbitals available first'),
           ("Hund's rule", 'electrons fill orbitals of equal energy singly, with parallel spins, before pairing'),
           ('Pauli exclusion principle', 'an orbital can hold at most two electrons, and they must have opposite spins'),
           ('sublevel', 'a group of orbitals of equal energy within a main energy level (s, p, d or f)'),
           ('degenerate orbitals', 'orbitals that have the same energy, such as the three 2p orbitals')],
    facts=[('What is the maximum number of electrons in the n = 3 energy level?', '18', ['8', '9', '32'], '2n² = 18 (3s, 3p, 3d).'),
           ('How many orbitals are there in a d sublevel?', '5', ['3', '7', '10'], 'A d sublevel has five orbitals, holding 10 electrons.'),
           ('What is the shape of an s orbital?', 'spherical', ['dumbbell-shaped', 'square planar', 'tetrahedral'], 's orbitals are spherically symmetric.'),
           ('Which sublevel is filled immediately after 4s?', '3d', ['4p', '4d', '3p'], 'Aufbau order: 4s then 3d then 4p.'),
           ('What is the maximum number of electrons in the 4f sublevel?', '14', ['7', '10', '18'], '7 orbitals × 2.'),
           ('How many orbitals are there in the n = 2 energy level?', '4', ['2', '8', '3'], 'One 2s + three 2p = n² = 4.')],
    why=[("Explain, using Hund's rule, why a nitrogen atom has three unpaired electrons.", "N is 1s² 2s² 2p³. The three 2p orbitals are degenerate; electrons occupy them singly with parallel spins before pairing because this minimises repulsion, so each 2p orbital holds one electron."),
         ('Explain why the 4s sublevel fills before the 3d sublevel.', 'In potassium and calcium the 4s sublevel is lower in energy than 3d, so by the Aufbau principle it is occupied first.'),
         ('Explain why the two electrons in the same orbital must have opposite spins.', 'The Pauli exclusion principle states no two electrons in an atom can have the same set of quantum numbers; two electrons sharing an orbital differ only in spin, so their spins must be opposite.'),
         ('Explain what is meant by a 2p orbital having a “dumbbell” shape.', 'There is a high probability of finding the electron in two lobes on opposite sides of the nucleus along one axis, with a node (zero probability) at the nucleus.')],
    contrast=[('an orbital', 'an orbit (Bohr model)', 'An orbit is a fixed circular path at a fixed distance; an orbital is a three-dimensional region of high electron probability with a characteristic shape.'),
              ('an s orbital', 'a p orbital', 'An s orbital is spherical and each s sublevel has one orbital; a p orbital is dumbbell-shaped and each p sublevel has three orbitals (px, py, pz) at right angles.')],
    misc=[('The third energy level can hold only 8 electrons.', 'n = 3 can hold 2n² = 18 electrons (3s² 3p⁶ 3d¹⁰); 8 is the number in 3s and 3p only.'),
          ('In oxygen the four 2p electrons occupy two orbitals as two pairs.', "By Hund's rule they occupy all three 2p orbitals: one pair and two unpaired electrons with parallel spins."),
          ('An orbital is the path an electron follows around the nucleus.', 'An orbital is a region of space where there is a high probability of finding the electron; electrons do not follow defined paths.')],
    evaluate=[('The Aufbau principle correctly predicts the electron configuration of every element.', ['correct for most of the first 36 elements', 'gives a systematic basis for the periodic table'], ['exceptions such as Cr and Cu (and many heavier elements) exist', 'sublevel energies change with nuclear charge and electron number, e.g. 3d below 4s once filled', 'predicted order of ion formation (4s lost first) is not obvious from filling order'], 'Aufbau is a useful guideline but not a law; real configurations depend on subtle energy balances.')],
))


@R.add('ch02-st2', 'C3', (1, 4), 'short')
def c3_full_config(rng, slot):
    zz = rng.choice([z for z in range(3, 37) if z not in EXC])
    sy = esym(zz)
    c = config(zz)
    stem = pick(rng, [f'Write the full electron configuration of {ENAME[sy]} (Z = {zz}).',
                      f'Deduce the ground-state electron configuration of a {sy} atom, using spdf notation. (Z = {zz})',
                      f'State the full electron configuration of an atom with {zz} electrons and identify the element.'])
    return dict(stem=stem, answer=f'{cfg_s(c)} ({sy})', markingKey=f'{cfg_s(c)} – correct order and superscripts (A1); 1 mark deducted for any wrong sublevel occupancy. Element: {sy}.', type='short', marks=2 if slot.d >= 2 else 1)


@R.add('ch02-st2', 'C3', (1, 4), 'mcq')
def c3_config_mcq(rng, slot):
    zz = rng.choice([z for z in range(5, 37) if z not in EXC and z not in (19, 20)])
    sy = esym(zz)
    c = config(zz)
    right = cfg_s(c)
    w1 = cfg_s(config(zz + 1))
    w2 = cfg_s(config(zz - 1))
    # wrong order: fill 3d before 4s or p overfilled
    w3 = right.replace('4s²', '4s¹') if '4s²' in right and '3d' in right else cfg_s(config(zz + 2))
    return mcq(rng, f'What is the ground-state electron configuration of {ENAME[sy]} (Z = {zz})?', right, [w1, w2, w3],
               f'{sy} has {zz} electrons: {right}.')


@R.add('ch02-st2', 'C3', (2, 5), 'short')
def c3_count(rng, slot):
    zz = rng.choice(range(5, 37))
    sy = esym(zz)
    c = config(zz)
    kind = rng.choice(['unpaired', 'p', 's', 'orbitals'])
    if kind == 'unpaired':
        v = unpaired(c)
        stem = f'Deduce the number of unpaired electrons in a ground-state {ENAME[sy]} atom.'
        key = f'Configuration {cfg_s(c)} (M1); applying Hund’s rule to the partly filled sublevel gives {v} unpaired electron(s) (A1).'
    elif kind == 'p':
        v = sum(n for sl, n in c if sl[1] == 'p')
        stem = f'State the total number of electrons in p orbitals in an atom of {ENAME[sy]}.'
        key = f'{cfg_s(c)}: p electrons = {v} (A1).'
    elif kind == 's':
        v = sum(n for sl, n in c if sl[1] == 's')
        stem = f'How many electrons occupy s orbitals in a ground-state atom of {ENAME[sy]}?'
        key = f'{cfg_s(c)}: s electrons = {v} (A1).'
    else:
        v = sum(1 if n else 0 for sl, n in c for _ in range({"s": 1, "p": 3, "d": 5}[sl[1]]) if False) + sum(min(n, {"s": 1, "p": 3, "d": 5}[sl[1]]) for sl, n in c)
        stem = f'Determine the number of orbitals that contain at least one electron in a ground-state {ENAME[sy]} atom.'
        key = f'{cfg_s(c)}; occupied orbitals = {v} (each sublevel contributes min(electrons, number of orbitals) by Hund’s rule) (A1).'
    return dict(stem=stem + f' (Z = {zz})', answer=str(v), markingKey=key, type='short', marks=2 if kind == 'unpaired' else 1)


@R.add('ch02-st2', 'C3', (2, 4), 'mcq')
def c3_identify_cfg(rng, slot):
    zz = rng.choice([z for z in range(5, 37) if z not in EXC])
    c = config(zz)
    sy = esym(zz)
    opts = [sy, esym(zz - 1), esym(zz + 1) if zz < 36 else esym(zz - 2), esym(zz - 8) if zz > 10 else esym(zz + 2)]
    if len(set(opts)) < 4:
        return None
    return mcq(rng, f'An atom has the ground-state electron configuration {cfg_s(c)}. Which element is it?', sy, opts[1:],
               f'Total electrons = {zz} → {ENAME[sy]}.')


R.mcqs('ch02-st2', 'C2', (1, 4), [
    ('Which orbital diagram for the 2p sublevel of carbon follows Hund’s rule?', '↑ ↑ _ (two singly occupied orbitals, parallel spins)', ['↑↓ _ _ (one orbital paired)', '↑ ↓ _ (opposite spins in separate orbitals)', '↑↑ _ _ (two parallel electrons in one orbital)'], 'Singly fill degenerate orbitals with parallel spins; two parallel electrons in one orbital would violate Pauli.'),
    ('Which principle is violated by the configuration 1s³?', 'the Pauli exclusion principle', ['Hund’s rule', 'the Aufbau principle', 'the octet rule'], 'An orbital holds at most two electrons.'),
    ('Which principle is violated by the ground-state configuration 1s² 2s¹ 2p¹ for beryllium?', 'the Aufbau principle', ['the Pauli exclusion principle', 'Hund’s rule', 'none – it is correct'], '2s is lower in energy and should be filled first (this is an excited state).'),
    ('How many electrons can occupy the set of three 3p orbitals?', '6', ['3', '2', '10'], 'Three orbitals × 2 electrons.'),
    ('Which sublevel does not exist?', '2d', ['3d', '4f', '2p'], 'n = 2 has only s and p sublevels.'),
])


@R.add('ch02-st2', 'C4', (3, 5), 'multi_step')
def c4_config_reason(rng, slot):
    zz = rng.choice([z for z in range(7, 36) if z not in EXC])
    sy = esym(zz)
    c = config(zz)
    u = unpaired(c)
    last = c[-1]
    stem = (f'For an atom of {ENAME[sy]} (Z = {zz}): (a) write the full electron configuration; (b) draw (describe) the orbital diagram for its highest-energy sublevel using arrows; '
            f'(c) state the number of unpaired electrons and explain the reason in terms of Hund’s rule and the Pauli principle.')
    orbs = {'s': 1, 'p': 3, 'd': 5}[last[0][1]]
    n = last[1]
    boxes = []
    for i in range(orbs):
        e = (1 if i < n else 0) + (1 if i < n - orbs else 0)
        boxes.append('[↑↓]' if e == 2 else '[↑]' if e == 1 else '[ ]')
    ans = f'(a) {cfg_s(c)}; (b) {last[0]}: {" ".join(boxes)}; (c) {u}'
    key = f'(a) {cfg_s(c)} (A1). (b) {last[0]} orbitals {" ".join(boxes)} – singly filled first, parallel spins (A1). (c) {u} unpaired (A1); degenerate orbitals singly occupied before pairing to minimise repulsion; paired electrons have opposite spins (Pauli) (R1).'
    return num(stem, ans, key, 4, 'multi_step')


R.facts('ch02-st3', F(
    terms=[('condensed electron configuration', 'an electron configuration written with the previous noble gas core in square brackets followed by the outer electrons, e.g. [Ne] 3s¹'),
           ('orbital diagram', 'a representation of electron configuration in which each orbital is drawn as a box and electrons as arrows showing spin'),
           ('noble gas core', 'the inner electrons of an atom that have the same configuration as the preceding noble gas'),
           ('valence electrons', 'the electrons in the outer energy level (and, for transition elements, the partly filled d sublevel) that take part in bonding')],
    facts=[('What is the condensed electron configuration of chromium (Z = 24)?', '[Ar] 3d⁵ 4s¹', ['[Ar] 3d⁴ 4s²', '[Ar] 3d⁶', '[Ar] 4s² 4p⁴'], 'A half-filled 3d sublevel is energetically favourable.'),
           ('What is the condensed electron configuration of copper (Z = 29)?', '[Ar] 3d¹⁰ 4s¹', ['[Ar] 3d⁹ 4s²', '[Ar] 3d¹⁰ 4s²', '[Ar] 4s² 3d⁹ 4p¹'], 'A full 3d sublevel is energetically favourable.'),
           ('When a transition element forms a positive ion, electrons are removed first from', 'the 4s sublevel', ['the 3d sublevel', 'the 3p sublevel', 'whichever sublevel was filled last'], 'Once 3d is occupied, 4s is higher in energy and is emptied first.'),
           ('Which ion has the configuration [Ar] 3d⁵?', 'Fe³⁺', ['Fe²⁺', 'Mn³⁺', 'Cr³⁺'], 'Fe [Ar] 3d⁶ 4s²; remove 4s² then one 3d.'),
           ('How many unpaired electrons does a chromium atom have in its ground state?', '6', ['4', '5', '2'], '[Ar] 3d⁵ 4s¹: five 3d + one 4s.')],
    why=[('Explain why the electron configuration of chromium is [Ar] 3d⁵ 4s¹ rather than [Ar] 3d⁴ 4s².', 'The 3d and 4s sublevels are very close in energy; promoting one 4s electron gives a half-filled 3d sublevel with six unpaired parallel spins, which minimises electron–electron repulsion and is lower in energy overall.'),
         ('Explain why Fe³⁺ is more stable than Fe²⁺ with respect to further oxidation in many environments.', 'Fe³⁺ has a half-filled [Ar] 3d⁵ configuration, with each d orbital singly occupied, which is relatively stable (lower repulsion); Fe²⁺ (3d⁶) has one paired d electron.'),
         ('Explain why 4s electrons are removed before 3d electrons when transition elements ionise.', 'Once the 3d sublevel contains electrons, the 4s electrons are on average further from the nucleus and higher in energy, so they are lost first.')],
    contrast=[('a full electron configuration', 'a condensed electron configuration', 'A full configuration lists every occupied sublevel from 1s; a condensed configuration replaces the inner electrons with the symbol of the preceding noble gas in brackets.')],
    misc=[('Fe²⁺ has the configuration [Ar] 3d⁴ 4s² because the last electrons added were 3d electrons.', 'Electrons are removed from 4s first: Fe²⁺ is [Ar] 3d⁶.'),
          ('Copper is [Ar] 3d⁹ 4s² because the Aufbau principle must always be followed.', 'Copper is an exception: [Ar] 3d¹⁰ 4s¹, because a full 3d sublevel is lower in energy overall.')],
    evaluate=[('Exceptions such as chromium and copper show that the Aufbau principle is not useful.', ['real configurations deviate from predictions', 'heavier elements show even more exceptions'], ['Aufbau correctly predicts almost all of the first 36 elements', 'exceptions can be explained by the small 3d/4s energy gap and the stability of half-filled/full sublevels'], 'Aufbau remains a valuable rule of thumb; exceptions refine rather than invalidate it.')],
))

TM_IONS = [(22, 2), (22, 4), (23, 3), (24, 3), (24, 2), (25, 2), (25, 7), (26, 2), (26, 3), (27, 2), (27, 3), (28, 2), (29, 1), (29, 2), (30, 2), (21, 3)]
MAIN_IONS = [(11, 1), (12, 2), (13, 3), (8, -2), (9, -1), (16, -2), (17, -1), (19, 1), (20, 2), (7, -3), (15, -3), (35, -1), (3, 1), (34, -2)]


def ion_name(zz, ch):
    s = esym(zz)
    return ion(s + ('' if abs(ch) == 1 else str(abs(ch))) + ('+' if ch > 0 else '-'))


@R.add('ch02-st3', 'C3', (1, 4), 'short')
def c3_ion_cfg(rng, slot):
    zz, ch = pick(rng, TM_IONS + MAIN_IONS)
    c = config_ion(zz, ch)
    stem = pick(rng, [f'Write the condensed electron configuration of {ion_name(zz, ch)} (Z of {esym(zz)} = {zz}).',
                      f'Deduce the electron configuration, using noble-gas notation, of the {ion_name(zz, ch)} ion. (Z = {zz})'])
    key = f'{esym(zz)} atom {cfg_short(config(zz))} (M1); ' + ('remove 4s electrons before 3d; ' if zz > 20 and ch > 0 else '') + f'{ion_name(zz, ch)}: {cfg_short(c)} (A1).'
    return dict(stem=stem, answer=cfg_short(c), markingKey=key, type='short', marks=2)


@R.add('ch02-st3', 'C3', (2, 4), 'mcq')
def c3_ion_cfg_mcq(rng, slot):
    zz, ch = pick(rng, TM_IONS)
    c = config_ion(zz, ch)
    right = cfg_short(c)
    # common error: remove 3d first
    occ = dict(config(zz))
    rem = ch
    for sl in ['3d', '4s']:
        while rem > 0 and occ.get(sl, 0) > 0:
            occ[sl] -= 1
            rem -= 1
    w1 = cfg_short(sorted([(k, v) for k, v in occ.items() if v > 0], key=lambda t: (int(t[0][0]), 'spdf'.index(t[0][1]))))
    w2 = cfg_short(config(zz))
    w3 = cfg_short(config_ion(zz, ch + 1)) if ch < 7 else cfg_short(config_ion(zz, ch - 1))
    return mcq(rng, f'What is the electron configuration of {ion_name(zz, ch)}?', right, [w1, w2, w3],
               f'{esym(zz)} is {cfg_short(config(zz))}; remove 4s electrons first, then 3d: {right}.')


@R.add('ch02-st3', 'C1', (1, 3), 'short')
def c1_condensed(rng, slot):
    zz = rng.choice(range(11, 37))
    c = config(zz)
    return dict(stem=f'Write the condensed electron configuration of {ENAME[esym(zz)]}.', answer=cfg_short(c),
                markingKey=f'{cfg_short(c)} (A1)' + (' – note the exception: half-filled/full 3d sublevel.' if zz in EXC else '.'), type='short', marks=1)


@R.add('ch02-st3', 'C3', (2, 5), 'short')
def c3_orbital_diagram(rng, slot):
    zz, ch = pick(rng, TM_IONS + [(24, 0), (29, 0), (26, 0), (25, 0)])
    c = config_ion(zz, ch) if ch else config(zz)
    d = dict(c).get('3d', 0)
    s4 = dict(c).get('4s', 0)
    boxes = []
    for i in range(5):
        e = (1 if i < d else 0) + (1 if i < d - 5 else 0)
        boxes.append('[↑↓]' if e == 2 else '[↑]' if e == 1 else '[ ]')
    s_box = '[↑↓]' if s4 == 2 else '[↑]' if s4 == 1 else '[ ]'
    u = unpaired(c)
    sp = ion_name(zz, ch) if ch else f'an atom of {ENAME[esym(zz)]}'
    stem = f'Draw an orbital (arrow-in-box) diagram for the 3d and 4s sublevels of {sp}, and state the number of unpaired electrons.'
    return dict(stem=stem, answer=f'3d: {" ".join(boxes)}  4s: {s_box}; {u} unpaired', markingKey=f'{cfg_short(c)} (M1); 3d {" ".join(boxes)} with parallel spins in singly occupied orbitals, 4s {s_box} (A1); {u} unpaired electrons (A1).', type='short', marks=3)


R.mcqs('ch02-st3', 'C2', (1, 4), [
    ('Which species has the same electron configuration as argon?', 'K⁺', ['Na⁺', 'Ca', 'Br⁻'], 'K⁺: 18 electrons, [Ne] 3s² 3p⁶.'),
    ('Which ion has no unpaired electrons?', 'Zn²⁺', ['Cu²⁺', 'Fe²⁺', 'Mn²⁺'], 'Zn²⁺ is [Ar] 3d¹⁰.'),
    ('Which atom has the largest number of unpaired electrons?', 'Cr', ['Mn', 'Fe', 'V'], 'Cr [Ar] 3d⁵ 4s¹ has six.'),
    ('The configuration [Ar] 3d¹⁰ belongs to which species?', 'Cu⁺', ['Cu', 'Cu²⁺', 'Ni'], 'Cu [Ar] 3d¹⁰ 4s¹ loses its 4s electron.'),
    ('Which is the correct electron configuration of Ti²⁺?', '[Ar] 3d²', ['[Ar] 4s²', '[Ar] 3d² 4s²', '[Ar] 3d¹ 4s¹'], 'Ti [Ar] 3d² 4s²; 4s lost first.'),
])


R.facts('ch02-st4', F(
    terms=[('first ionisation energy', 'the minimum energy required to remove one mole of electrons from one mole of gaseous atoms in their ground state to form one mole of gaseous 1+ ions'),
           ('successive ionisation energies', 'the energies required to remove electrons one after another from an atom, each from an increasingly positive gaseous ion'),
           ('effective nuclear charge', 'the net positive charge experienced by an outer electron, equal to the nuclear charge reduced by shielding from inner electrons'),
           ('shielding', 'the reduction in attraction between the nucleus and outer electrons caused by repulsion from inner electrons')],
    facts=[('Which equation represents the first ionisation energy of magnesium?', 'Mg(g) → Mg⁺(g) + e⁻', ['Mg(s) → Mg⁺(g) + e⁻', 'Mg(g) → Mg²⁺(g) + 2e⁻', 'Mg(g) + e⁻ → Mg⁻(g)'], 'Gaseous atoms, one electron removed.'),
           ('Which element in period 2 has the highest first ionisation energy?', 'neon', ['fluorine', 'lithium', 'oxygen'], 'Ne has the greatest nuclear charge with the same shielding.'),
           ('Why is the first ionisation energy of oxygen lower than that of nitrogen?', 'The paired 2p electron in oxygen experiences extra repulsion.', ['Oxygen has a smaller nuclear charge.', 'Oxygen’s electron is in a higher energy level.', 'Nitrogen has more shielding.'], 'Spin-pair repulsion in 2p⁴.'),
           ('Why is the first ionisation energy of aluminium lower than that of magnesium?', 'Its outer electron is in a 3p orbital, higher in energy and more shielded than 3s.', ['Aluminium has fewer protons.', 'Aluminium has a paired electron.', 'Aluminium is a non-metal.'], '3p is higher energy and shielded by 3s².'),
           ('How does the first ionisation energy change down group 1?', 'It decreases.', ['It increases.', 'It stays the same.', 'It first increases then decreases.'], 'Outer electron further from the nucleus and more shielded.')],
    why=[('Explain why the first ionisation energy generally increases across period 3.', 'Nuclear charge increases while electrons are added to the same main energy level, so shielding stays roughly constant; the effective nuclear charge increases and atomic radius decreases, so outer electrons are held more strongly.'),
         ('Explain why there is a large increase between the second and third ionisation energies of magnesium.', 'The third electron is removed from the 2p sublevel, a main energy level closer to the nucleus with much less shielding, so it is far more strongly attracted than the 3s electrons.'),
         ('Explain why successive ionisation energies of an element always increase.', 'Each electron is removed from an increasingly positive ion; the same nuclear charge attracts fewer electrons, with less repulsion between them, so each removal requires more energy.'),
         ('Explain why the first ionisation energy decreases down group 2.', 'The outer electron is in a higher main energy level, further from the nucleus and more shielded by inner electrons, which outweighs the increase in nuclear charge.')],
    contrast=[('first ionisation energy', 'second ionisation energy', 'First IE removes one electron from a gaseous atom (X(g) → X⁺(g) + e⁻); second IE removes an electron from the gaseous 1+ ion (X⁺(g) → X²⁺(g) + e⁻) and is always larger.')],
    misc=[('Ionisation energy decreases across a period because the number of electrons increases.', 'IE generally increases across a period: extra electrons go into the same energy level with little extra shielding while the nuclear charge increases.'),
          ('The large jump in successive ionisation energies occurs when an electron is removed from a filled sublevel.', 'The large jump occurs when an electron is removed from a new main energy level closer to the nucleus (inner shell).')],
    evaluate=[('Successive ionisation energy data provide strong evidence for the existence of main energy levels and sublevels.', ['large jumps match the start of a new inner shell', 'smaller discontinuities match s/p sublevels', 'first IE trends across periods show 2/3 and 5/6 dips'], ['data are indirect – inferred via a model', 'the model must assume shielding and nuclear charge effects'], 'IE data are strong supporting evidence consistent with the quantum model, though interpretation relies on that model.')],
))

SUCC = {'Na': [496, 4562, 6910, 9543, 13354], 'Mg': [738, 1451, 7733, 10543, 13630], 'Al': [578, 1817, 2745, 11577, 14842],
        'Si': [787, 1577, 3232, 4356, 16091, 19805], 'P': [1012, 1907, 2914, 4964, 6274, 21267], 'S': [1000, 2252, 3357, 4556, 7004, 8496, 27107],
        'Li': [520, 7298, 11815], 'Be': [900, 1757, 14849, 21007], 'B': [801, 2427, 3660, 25026], 'C': [1086, 2353, 4621, 6223, 37831],
        'K': [419, 3052, 4420, 5877], 'Ca': [590, 1145, 4912, 6491, 8153], 'Cl': [1251, 2298, 3822, 5159, 6542, 9362, 11018, 33604]}
GROUP = {'Na': 1, 'Mg': 2, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Li': 1, 'Be': 2, 'B': 13, 'C': 14, 'K': 1, 'Ca': 2, 'Cl': 17}


@R.add('ch02-st4', 'C3', (2, 5), 'short')
def c3_succ_group(rng, slot):
    el = pick(rng, list(SUCC))
    data = SUCC[el]
    jump = max(range(1, len(data)), key=lambda i: data[i] / data[i - 1])
    g = GROUP[el]
    lab = pick(rng, ['Element X', 'Element Q', 'An unknown element', 'Element M'])
    stem = (f'The successive ionisation energies of {lab[0].lower() + lab[1:] if lab.startswith("An") else lab} (kJ mol⁻¹) are: {", ".join(str(v) for v in data)}. '
            f'Deduce the group of the periodic table to which it belongs, explaining your reasoning.')
    gs = f'group {g}'
    return dict(stem=stem, answer=f'{gs} ({jump} outer electron{"s" if jump > 1 else ""})',
                markingKey=f'Largest jump between IE{jump} ({data[jump - 1]}) and IE{jump + 1} ({data[jump]}) (M1); so {jump} electron(s) in the outer shell, next electron from an inner shell closer to the nucleus (R1); {gs} (A1).', type='short', marks=3)


@R.add('ch02-st4', 'C3', (1, 4), 'mcq')
def c3_ie_order(rng, slot):
    pool = rng.sample(['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca'], 4)
    kind = rng.choice(['high', 'low'])
    best = max(pool, key=lambda e: IE1[e]) if kind == 'high' else min(pool, key=lambda e: IE1[e])
    stem = f'Which element has the {"highest" if kind == "high" else "lowest"} first ionisation energy?'
    return mcq(rng, stem, ENAME[best], [ENAME[e] for e in pool if e != best],
               'First IEs / kJ mol⁻¹: ' + ', '.join(f'{e} {IE1[e]}' for e in pool) + '.')


@R.add('ch02-st4', 'C2', (2, 4), 'explain')
def c2_ie_pair(rng, slot):
    pairs = [('Be', 'B', 'the outer electron of B is in a 2p orbital, higher in energy and shielded by 2s²'),
             ('Mg', 'Al', 'the outer electron of Al is in a 3p orbital, higher in energy and shielded by 3s²'),
             ('N', 'O', 'O has a pair of electrons in one 2p orbital; the extra repulsion makes one easier to remove'),
             ('P', 'S', 'S has a paired 3p electron that experiences additional repulsion'),
             ('Na', 'K', 'the outer electron of K is in n = 4, further from the nucleus and more shielded'),
             ('F', 'Cl', 'the outer electron of Cl is in n = 3, further from the nucleus and more shielded'),
             ('Ne', 'Na', 'the outer electron of Na is in a new main level (3s), further out and shielded by 10 inner electrons'),
             ('Mg', 'Ca', 'the outer electrons of Ca are in n = 4, further from the nucleus with more shielding')]
    hi, lo, why = pick(rng, pairs)
    if IE1[hi] < IE1[lo]:
        hi, lo = lo, hi
    stem = f'The first ionisation energy of {ENAME[hi]} is {IE1[hi]} kJ mol⁻¹ and that of {ENAME[lo]} is {IE1[lo]} kJ mol⁻¹. Explain this difference.'
    return dict(stem=stem, answer=why[0].upper() + why[1:] + '.', markingKey=f'{why} (2); reference to attraction between nucleus and outer electron (1).', type='explain', marks=3)


R.mcqs('ch02-st4', 'C2', (1, 4), [
    ('The first five ionisation energies of an element are 738, 1451, 7733, 10543 and 13630 kJ mol⁻¹. In which group is the element?', '2', ['1', '3', '5'], 'Big jump after the 2nd electron.'),
    ('Why is the second ionisation energy of sodium much larger than its first?', 'The second electron is removed from a full inner shell closer to the nucleus.', ['Sodium has a high nuclear charge.', 'The second electron is in a 3p orbital.', 'Na⁺ is a noble gas.'], 'Removal from n = 2.'),
    ('Which shows the general trend in first ionisation energy across a period and down a group?', 'increases across, decreases down', ['decreases across, increases down', 'increases across, increases down', 'decreases across, decreases down'], 'Effective nuclear charge vs distance/shielding.'),
    ('Which element has a first ionisation energy lower than that of the element before it in period 3?', 'aluminium', ['silicon', 'phosphorus', 'chlorine'], 'Al (3p¹) is lower than Mg (3s²).'),
])


@p1b(R, 'ch02-st4')
def p1b_ie_graph(rng, slot):
    el = pick(rng, [e for e in SUCC if len(SUCC[e]) >= 5])
    data = SUCC[el]
    logs = [math.log10(v) for v in data]
    tab = '\n'.join(f'{i + 1} | {v} | {math.log10(v):.2f}' for i, v in enumerate(data))
    jump = max(range(1, len(data)), key=lambda i: data[i] / data[i - 1])
    intro = f'The table shows the successive ionisation energies of an element in period 2 or 3.\n\nElectron removed | IE / kJ mol⁻¹ | log₁₀(IE)\n{tab}'
    return dict(intro=intro, parts=[
        ('Suggest why log₁₀(IE) rather than IE is plotted against the number of the electron removed.', 'The values cover a very wide range; a log scale allows all the values and the jumps to be seen clearly on one graph.', 'Wide range of values compressed (1).', 1),
        ('Identify the position of the largest increase and deduce the group number of the element.', f'between electrons {jump} and {jump + 1}; group {GROUP[el]}', f'Jump between IE{jump} and IE{jump + 1} (M1); group {GROUP[el]} (A1).', 2),
        ('Write an equation for the second ionisation energy of the element.', f'{el}⁺(g) → {el}²⁺(g) + e⁻', 'Correct species with (g) state symbols (1).', 1),
        ('Explain why each successive ionisation energy is greater than the previous one.', 'Electrons are removed from increasingly positive ions; the remaining electrons experience less repulsion and are attracted more strongly by the same nuclear charge.', 'Increasingly positive ion (1); less repulsion/greater attraction per electron (1).', 2),
        ('Identify the element.', f'{ENAME[el]}', f'{ENAME[el]} (1).', 1)],
        extras=[('State why the ionisation energy values are given for gaseous species.', 'So that only the energy to remove the electron is measured, without contributions from breaking bonds/lattice forces.', 'Isolated atoms/ions, no other interactions (1).', 1)])


R.facts('ch02-st5', F(
    terms=[('convergence limit', 'the frequency (or wavelength) at which the lines of a spectral series merge, corresponding to an electron being removed completely (n = ∞)'),
           ('ionisation energy from spectra', 'the energy of a photon at the convergence limit of the series ending in the ground state, multiplied by the Avogadro constant')],
    facts=[('In the hydrogen emission spectrum, which series is used to find the ionisation energy of hydrogen?', 'the series in the ultraviolet ending at n = 1 (Lyman)', ['the visible series ending at n = 2', 'the infrared series ending at n = 3', 'any series'], 'Ionisation is from the ground state n = 1.'),
           ('What does the convergence limit of the Lyman series correspond to?', 'the transition n = ∞ → n = 1', ['the transition n = 2 → n = 1', 'the transition n = ∞ → n = 2', 'the first line of the series'], 'At convergence the electron comes from infinity.'),
           ('The convergence limit of the Lyman series of hydrogen is at 91.2 nm. What is the first ionisation energy of hydrogen?', '1.31 × 10³ kJ mol⁻¹', ['2.18 × 10⁻¹⁸ kJ mol⁻¹', '1.31 kJ mol⁻¹', '3.29 × 10¹⁵ kJ mol⁻¹'], 'E = hc/λ × NA = 1312 kJ mol⁻¹.')],
    why=[('Explain why the convergence limit of a series ending at n = 1 gives the ionisation energy of a hydrogen atom.', 'At the convergence limit the electron falls from n = ∞ (where it is no longer bound) to the ground state n = 1; the photon energy equals the energy needed to remove an electron from n = 1 to infinity, i.e. the ionisation energy (per atom).'),
         ('Explain why the convergence limit can be difficult to read directly from an emission spectrum, and how it is found in practice.', 'The lines become so close that they merge and cannot be resolved; the limit is found by plotting the difference in frequency between successive lines against frequency and extrapolating to zero difference.')],
    misc=[('The ionisation energy of hydrogen can be found from the convergence limit of the visible (Balmer) series.', 'The Balmer series ends at n = 2, so its convergence limit gives the energy to remove an electron from n = 2, not from the ground state; the Lyman (n = 1) series must be used.')],
    evaluate=[('Using a convergence limit is a more reliable way to determine ionisation energy than electrical (electron-impact) methods.', ['spectral frequencies can be measured very precisely', 'no need to ionise samples in a field'], ['the limit must often be extrapolated, introducing uncertainty', 'only practical for simple atoms with clear series', 'multi-electron atoms give complex spectra'], 'For hydrogen the spectroscopic method is extremely precise; for complex atoms, it is limited and complementary methods are used.')],
))


@R.add('ch02-st5', 'C3', (1, 5), 'numerical')
def c3_converge(rng, slot):
    kind = rng.choice(['lam', 'freq', 'rev'])
    if kind == 'lam':
        lam = round(rng.uniform(60, 240), 1)
        E = H_PLANCK * C_LIGHT / (lam * 1e-9)
        IE = E * NA / 1000
        el = pick(rng, ['an element X', 'a gaseous element in a discharge tube', 'an alkali metal vapour', 'a hydrogen-like ion'])
        stem = f'The convergence limit of the series of lines ending at the ground state in the emission spectrum of {el} is at a wavelength of {lam} nm. Calculate the first ionisation energy, in kJ mol⁻¹.'
        return num(stem, q(IE, 'kJ mol⁻¹'), f'E = hc/λ = 6.63 × 10⁻³⁴ × 3.00 × 10⁸/({lam} × 10⁻⁹) = {q(E, "J")} (M1); × 6.02 × 10²³ (M1); ÷ 1000 = {q(IE, "kJ mol⁻¹")} (A1).', 3)
    if kind == 'freq':
        f = rng.uniform(1.0, 4.0) * 1e15
        f = float(f'{f:.3g}')
        IE = H_PLANCK * f * NA / 1000
        stem = f'The convergence limit of the ground-state series in the spectrum of a gaseous atom occurs at a frequency of {sf(f)} s⁻¹. Determine the first ionisation energy of the element in kJ mol⁻¹.'
        if slot.d <= 2:
            return nmcq(rng, stem.replace('Determine', 'What is'), IE, [IE * 1000, H_PLANCK * f, IE / NA * 1000 * 1e18], 'kJ mol⁻¹',
                        f'IE = hf × NA/1000 = {q(IE, "kJ mol⁻¹")}.', extra=True)
        return num(stem, q(IE, 'kJ mol⁻¹'), f'E = hf = {q(H_PLANCK * f, "J")} (M1); IE = E × NA/1000 = {q(IE, "kJ mol⁻¹")} (A1).', 2)
    IEv = pick(rng, [('sodium', 496), ('lithium', 520), ('potassium', 419), ('hydrogen', 1312), ('helium', 2372), ('magnesium', 738), ('calcium', 590)])
    E = IEv[1] * 1000 / NA
    lam = H_PLANCK * C_LIGHT / E * 1e9
    stem = f'The first ionisation energy of {IEv[0]} is {IEv[1]} kJ mol⁻¹. Calculate the wavelength, in nm, at which the convergence limit of its ground-state series would be expected.'
    return num(stem, q(lam, 'nm'), f'E per atom = {IEv[1]} × 10³/6.02 × 10²³ = {q(E, "J")} (M1); λ = hc/E (M1) = {q(lam, "nm")} (A1).', 3)


R.mcqs('ch02-st5', 'C2', (1, 4), [
    ('Why do the lines in the Lyman series converge?', 'The energy levels get closer together as n increases.', ['The electrons slow down.', 'The nucleus attracts electrons less at low n.', 'Photons lose energy as they travel.'], 'Spacing of levels decreases with n.'),
    ('Which quantity is calculated directly from the convergence frequency f using E = hf?', 'the ionisation energy of one atom', ['the ionisation energy of one mole of atoms', 'the electron affinity', 'the energy of the n = 2 level'], 'Multiply by NA for per mole.'),
    ('A convergence limit at a higher frequency indicates', 'a higher ionisation energy', ['a lower ionisation energy', 'a larger atom', 'more energy levels'], 'E = hf.'),
])


@R.add('ch02-st5', 'C3', (2, 4), 'mcq')
def c3_converge_mcq(rng, slot):
    lam = rng.choice([91.2, 50.4, 135.0, 241.3, 285.6, 204.6, 162.1])
    IE = H_PLANCK * C_LIGHT / (lam * 1e-9) * NA / 1000
    return nmcq(rng, f'The convergence limit of the ground-state series of an atom is at {lam} nm. What is its first ionisation energy?', IE,
                [IE * 1000, H_PLANCK * C_LIGHT / lam * NA, IE / 10], 'kJ mol⁻¹', f'IE = hcNA/λ = {q(IE, "kJ mol⁻¹")} (λ in m, divide J by 1000).')


@p1b(R, 'ch02-st5', d=(3, 5))
def p1b_convergence(rng, slot):
    # hydrogen Lyman lines; frequency differences vs frequency, extrapolate
    ns = [2, 3, 4, 5, 6, 7]
    fs = [round(3.29 * (1 - 1 / n ** 2), 3) * 1e15 for n in ns]
    dfs = [fs[i + 1] - fs[i] for i in range(len(fs) - 1)]
    rows = '\n'.join(f'{fs[i] / 1e15:.3f} | {dfs[i] / 1e15:.3f}' for i in range(len(dfs)))
    fconv = 3.29e15
    IE = H_PLANCK * fconv * NA / 1000
    intro = ('The frequencies of lines in the Lyman series of hydrogen were measured. The difference Δf between each line and the next was calculated.\n\n'
             f'f / 10¹⁵ Hz | Δf / 10¹⁵ Hz\n{rows}')
    return dict(intro=intro, parts=[
        ('Explain why Δf decreases as f increases.', 'The energy levels get closer together at higher n, so successive lines are closer in energy/frequency.', 'Levels converge at high n (1).', 1),
        ('Describe how a graph of Δf against f can be used to find the convergence limit.', 'Plot Δf (y) against f (x), draw a line of best fit and extrapolate to Δf = 0; the f-intercept is the convergence frequency.', 'Plot and best-fit curve/line (1); extrapolate to Δf = 0 (1).', 2),
        (f'The convergence limit is found to be {fconv / 1e15:.2f} × 10¹⁵ Hz. Calculate the ionisation energy of hydrogen in kJ mol⁻¹.', q(IE, 'kJ mol⁻¹'), f'E = hf = {q(H_PLANCK * fconv, "J")} (M1); × NA/1000 = {q(IE, "kJ mol⁻¹")} (A1).', 2),
        ('State why the frequencies of lines close to the convergence limit have a larger uncertainty.', 'The lines are very close together and difficult to resolve.', 'Lines crowd together/hard to resolve (1).', 1),
        ('Explain why this series, rather than the visible series, must be used.', 'Only the series ending at n = 1 (the ground state) relates to removal of an electron from the ground state.', 'Ground state n = 1 (1).', 1)])


# =============================================================================================
# ch03 S1.4 Counting particles by mass: the mole
# =============================================================================================
CMPD = [('water', 'H2O'), ('carbon dioxide', 'CO2'), ('sodium chloride', 'NaCl'), ('glucose', 'C6H12O6'),
        ('calcium carbonate', 'CaCO3'), ('ammonia', 'NH3'), ('sulfuric acid', 'H2SO4'), ('ethanol', 'C2H5OH'),
        ('magnesium oxide', 'MgO'), ('copper(II) sulfate pentahydrate', 'CuSO4.5H2O'), ('aluminium oxide', 'Al2O3'),
        ('methane', 'CH4'), ('sodium hydroxide', 'NaOH'), ('calcium hydroxide', 'Ca(OH)2'), ('ammonium nitrate', 'NH4NO3'),
        ('iron(III) oxide', 'Fe2O3'), ('potassium manganate(VII)', 'KMnO4'), ('sucrose', 'C12H22O11'),
        ('aspirin', 'C9H8O4'), ('paracetamol', 'C8H9NO2'), ('caffeine', 'C8H10N4O2'), ('urea', 'CO(NH2)2'),
        ('sodium carbonate', 'Na2CO3'), ('ammonium sulfate', '(NH4)2SO4'), ('propane', 'C3H8'), ('ethanoic acid', 'CH3COOH'),
        ('silver nitrate', 'AgNO3'), ('magnesium sulfate heptahydrate', 'MgSO4.7H2O'), ('zinc chloride', 'ZnCl2'),
        ('calcium phosphate', 'Ca3(PO4)2')]


def nat(f):
    return sum(atoms(f).values())


R.facts('ch03-st1', F(
    terms=[('mole', 'the SI unit of amount of substance; one mole contains exactly 6.02214076 × 10²³ elementary entities'),
           ('Avogadro constant (NA)', 'the number of particles per mole of substance, 6.02 × 10²³ mol⁻¹'),
           ('molar mass (M)', 'the mass of one mole of a substance, in g mol⁻¹, numerically equal to its relative formula mass'),
           ('relative formula mass (Mr)', 'the sum of the relative atomic masses of all the atoms in the formula of a substance'),
           ('amount of substance', 'the quantity, measured in moles, that is proportional to the number of specified particles in a sample')],
    facts=[('What is the molar mass of water?', '18.02 g mol⁻¹', ['17.01 g mol⁻¹', '18.02 g', '10.00 g mol⁻¹'], '2 × 1.01 + 16.00 = 18.02 g mol⁻¹.'),
           ('Which sample contains the greatest number of atoms?', '1 mol of CH₄', ['1 mol of CO₂', '1 mol of He', '1 mol of NaCl'], 'CH₄ has 5 atoms per formula unit.'),
           ('Which equation links amount, mass and molar mass?', 'n = m/M', ['n = M/m', 'n = m × M', 'n = m/NA'], 'Amount in mol = mass in g ÷ molar mass in g mol⁻¹.'),
           ('How many molecules are in 0.500 mol of oxygen gas?', '3.01 × 10²³', ['6.02 × 10²³', '1.20 × 10²⁴', '3.01 × 10²²'], 'N = n × NA.'),
           ('What is the SI unit of molar mass?', 'g mol⁻¹', ['g', 'mol g⁻¹', 'mol'], 'Mass per amount.')],
    why=[('Explain why the mole is needed in chemistry.', 'Atoms and molecules are far too small to count individually; the mole links a countable mass of substance to a fixed number of particles (6.02 × 10²³), allowing reacting quantities to be calculated from equations.'),
         ('Explain why 1 mol of carbon dioxide and 1 mol of water have different masses but contain the same number of molecules.', 'One mole of any substance contains NA particles; the mass of a mole depends on the mass of each particle, and CO₂ molecules (44.01) are heavier than H₂O molecules (18.02).'),
         ('Explain why 12.01 g of carbon and 24.31 g of magnesium contain the same number of atoms.', 'Each is the molar mass of the element, so each contains 1 mol, i.e. 6.02 × 10²³ atoms.')],
    contrast=[('relative molecular mass', 'molar mass', 'Relative molecular mass is a dimensionless ratio (relative to 1/12 of ¹²C); molar mass is the mass of one mole and has units g mol⁻¹ – numerically equal.'),
              ('the number of molecules', 'the number of atoms in a sample', 'Number of molecules = n × NA; number of atoms = n × NA × atoms per molecule.')],
    misc=[('One mole of oxygen gas contains 6.02 × 10²³ oxygen atoms.', 'Oxygen gas is O₂: one mole contains 6.02 × 10²³ molecules and 1.20 × 10²⁴ atoms.'),
          ('The molar mass of magnesium is 24.31 g.', 'Molar mass has units of g mol⁻¹; 24.31 g is the mass of one mole.')],
    evaluate=[('The redefinition of the mole in 2019 (fixing NA exactly) was a significant improvement.', ['NA is now exact, independent of an artefact or a ¹²C mass measurement', 'consistent with the other SI base units defined by constants'], ['makes no practical difference to everyday calculations', 'molar mass of ¹²C is no longer exactly 12 g mol⁻¹'], 'Conceptually cleaner and more stable at the highest precision, though invisible in school-level calculations (NOS: measurement standards evolve).')],
))


@R.add('ch03-st1', 'C3', (1, 5), 'numerical')
def c3_mole(rng, slot):
    nm, f = pick(rng, CMPD)
    M = mr(f)
    kind = rng.choice(['m2n', 'n2m', 'm2N', 'atoms', 'N2m'])
    who = name(rng)
    if kind == 'm2n':
        m = round(rng.uniform(1, 100), rng.choice([1, 2]))
        n = m / M
        stem = pick(rng, [f'Calculate the amount, in mol, of {nm} ({chem(f)}) in {m} g.', f'{who} weighs out {m} g of {nm}, {chem(f)}. Calculate the amount of substance in this sample.'])
        if slot.d <= 2:
            return nmcq(rng, stem.replace('Calculate', 'What is'), n, [m * M, M / m, m / (M / 2)], 'mol', f'M({chem(f)}) = {M:.2f} g mol⁻¹; n = {m}/{M:.2f} = {q(n, "mol")}.')
        return num(stem, q(n, 'mol'), f'M = {M:.2f} g mol⁻¹ (M1); n = m/M = {m}/{M:.2f} = {q(n, "mol")} (A1).', 2)
    if kind == 'n2m':
        n = float(f'{rng.uniform(0.01, 3):.3g}')
        m = n * M
        stem = f'Calculate the mass of {sf(n)} mol of {nm}, {chem(f)}.'
        return num(stem, q(m, 'g'), f'M = {M:.2f} g mol⁻¹ (M1); m = nM = {sf(n)} × {M:.2f} = {q(m, "g")} (A1).', 2)
    if kind == 'm2N':
        m = round(rng.uniform(0.5, 50), 2)
        N = m / M * NA
        stem = f'Calculate the number of formula units (or molecules) in {m} g of {nm}, {chem(f)}.'
        return num(stem, sf(N), f'n = {m}/{M:.2f} = {sf(m / M)} mol (M1); N = n × NA = {sf(N)} (A1).', 2)
    if kind == 'N2m':
        N = float(f'{rng.uniform(1, 9.9):.3g}') * 10 ** rng.randint(20, 24)
        m = N / NA * M
        stem = f'A sample of {nm} contains {sf(N)} molecules (formula units). Calculate its mass.'
        return num(stem, q(m, 'g'), f'n = N/NA = {sf(N)}/6.02 × 10²³ = {sf(N / NA)} mol (M1); m = n × {M:.2f} = {q(m, "g")} (A1).', 2)
    # atoms
    el = pick(rng, list(atoms(f)))
    k = atoms(f)[el]
    m = round(rng.uniform(1, 60), 2)
    Nat = m / M * k * NA
    stem = f'Calculate the number of {ENAME.get(el, el)} atoms in {m} g of {nm}, {chem(f)}.'
    if slot.d <= 3:
        return nmcq(rng, stem.replace('Calculate', 'What is'), Nat, [m / M * NA, m / M * nat(f) * NA, m * NA], '', f'n = {m}/{M:.2f} mol; × {k} {el} atoms per formula unit × NA = {sf(Nat)}. Forgetting the factor {k} is the common error.')
    return num(stem, sf(Nat), f'n({chem(f)}) = {m}/{M:.2f} = {sf(m / M)} mol (M1); n({el}) = {k} × {sf(m / M)} (M1); N = {sf(Nat)} (A1).', 3)


@R.add('ch03-st1', 'C1', (1, 3), 'numerical')
def c1_mr(rng, slot):
    nm, f = pick(rng, CMPD)
    M = mr(f)
    return num(f'Calculate the molar mass of {nm}, {chem(f)}.', f'{M:.2f} g mol⁻¹', ' + '.join(f'{k} × {AR[e]:.2f}' for e, k in atoms(f).items()) + f' = {M:.2f} g mol⁻¹ (A1).', 1)


@R.add('ch03-st1', 'C4', (3, 5), 'multi_step')
def c4_mole_multi(rng, slot):
    kind = rng.choice(['hydrate', 'tablet', 'compare'])
    if kind == 'hydrate':
        salt, fs, nw = pick(rng, [('copper(II) sulfate', 'CuSO4', 5), ('magnesium sulfate', 'MgSO4', 7), ('sodium carbonate', 'Na2CO3', 10), ('barium chloride', 'BaCl2', 2), ('iron(II) sulfate', 'FeSO4', 7), ('cobalt(II) chloride', 'CoCl2', 6)])
        m1 = round(rng.uniform(2.0, 6.0), 3)
        mh = mr(fs) + nw * mr('H2O')
        nh = m1 / mh
        m2 = round(nh * mr(fs), 3)
        mw = m1 - m2
        x = (mw / mr('H2O')) / (m2 / mr(fs))
        stem = (f'A {m1:.3f} g sample of hydrated {salt}, {chem(fs)}·xH₂O, was heated to constant mass. The anhydrous residue had a mass of {m2:.3f} g. '
                f'(a) Calculate the amount of anhydrous salt and of water. (b) Determine x. (c) Explain why the sample was heated to constant mass.')
        return num(stem, f'x = {round(x)}', f'(a) n(salt) = {m2:.3f}/{mr(fs):.2f} = {sf(m2 / mr(fs))} mol; n(H₂O) = {mw:.3f}/18.02 = {sf(mw / 18.02)} mol (M1 M1). (b) ratio {x:.2f} → x = {round(x)} (A1). (c) to ensure all water of crystallisation is removed (R1).', 5, 'multi_step')
    if kind == 'tablet':
        drug, f, dose = pick(rng, [('aspirin', 'C9H8O4', 300), ('paracetamol', 'C8H9NO2', 500), ('caffeine', 'C8H10N4O2', 65), ('ibuprofen', 'C13H18O2', 200)])
        M = mr(f)
        n = dose / 1000 / M
        N = n * NA
        Nc = N * atoms(f)['C']
        stem = (f'A tablet contains {dose} mg of {drug}, {chem(f)}. (a) Calculate the molar mass of {drug}. (b) Calculate the number of {drug} molecules in one tablet. (c) Calculate the total number of carbon atoms in the {drug} in one tablet.')
        return num(stem, f'(a) {M:.2f} g mol⁻¹; (b) {sf(N)}; (c) {sf(Nc)}', f'(a) {M:.2f} g mol⁻¹ (A1). (b) {dose} mg = {dose / 1000} g (M1); n = {sf(n)} mol; N = {sf(N)} (A1). (c) × {atoms(f)["C"]} = {sf(Nc)} (A1).', 4, 'multi_step')
    (n1, f1), (n2, f2) = rng.sample(CMPD, 2)
    m = round(rng.uniform(5, 50), 1)
    a1 = m / mr(f1) * nat(f1) * NA
    a2 = m / mr(f2) * nat(f2) * NA
    more = n1 if a1 > a2 else n2
    stem = f'Deduce, showing your working, whether {m} g of {n1} ({chem(f1)}) or {m} g of {n2} ({chem(f2)}) contains more atoms.'
    return num(stem, f'{more} ({sf(max(a1, a2))} atoms vs {sf(min(a1, a2))})', f'{n1}: {m}/{mr(f1):.2f} × {nat(f1)} × NA = {sf(a1)} (M1 A1); {n2}: {m}/{mr(f2):.2f} × {nat(f2)} × NA = {sf(a2)} (A1); {more} contains more (A1).', 4, 'multi_step')


R.mcqs('ch03-st1', 'C2', (1, 4), [
    ('Which sample has the greatest mass?', '1.0 mol of CO₂', ['1.0 mol of H₂O', '2.0 mol of He', '1.0 mol of NH₃'], 'CO₂: 44 g; H₂O 18 g; He 8 g; NH₃ 17 g.'),
    ('Which contains the same number of atoms as 1 mol of water molecules?', '1 mol of ozone, O₃', ['1 mol of oxygen gas, O₂', '1 mol of helium', '1 mol of methane, CH₄'], '1 mol H₂O contains 3 mol of atoms; so does 1 mol O₃ (O₂: 2 mol, He: 1 mol, CH₄: 5 mol).'),
    ('The mass of one atom of an element is 3.82 × 10⁻²³ g. What is its molar mass? (NA = 6.02 × 10²³ mol⁻¹)', '23.0 g mol⁻¹', ['6.35 × 10⁻⁴⁷ g mol⁻¹', '0.0435 g mol⁻¹', '3.82 g mol⁻¹'], 'M = mass of one atom × NA.'),
    ('Which sample contains 1.20 × 10²⁴ atoms? (NA = 6.02 × 10²³ mol⁻¹)', '1.00 mol of O₂', ['1.00 mol of CO₂', '1.00 mol of NH₃', '1.00 mol of He'], 'atoms = n × atoms per molecule × NA = 1.00 × 2 × 6.02 × 10²³ = 1.20 × 10²⁴.'),
])


EFC = [('glucose', 'C6H12O6'), ('ethane', 'C2H6'), ('butane', 'C4H10'), ('benzene', 'C6H6'), ('hydrazine', 'N2H4'),
       ('hydrogen peroxide', 'H2O2'), ('ethanoic acid', 'C2H4O2'), ('ethanedioic acid', 'C2H2O4'), ('propene', 'C3H6'),
       ('octane', 'C8H18'), ('naphthalene', 'C10H8'), ('dinitrogen tetroxide', 'N2O4'), ('ethane-1,2-diol', 'C2H6O2'),
       ('cyclohexane', 'C6H12'), ('butanoic acid', 'C4H8O2'), ('phosphorus(V) oxide', 'P4O10'), ('ethyne', 'C2H2'),
       ('styrene', 'C8H8'), ('lactic acid', 'C3H6O3'), ('urea', 'CH4N2O'), ('ethyl ethanoate', 'C4H8O2'), ('fructose', 'C6H12O6'),
       ('iron(III) oxide', 'Fe2O3'), ('magnetite', 'Fe3O4'), ('copper(I) oxide', 'Cu2O'), ('chromium(III) oxide', 'Cr2O3'),
       ('aluminium sulfide', 'Al2S3'), ('magnesium nitride', 'Mg3N2'), ('sodium thiosulfate', 'Na2S2O3'), ('potassium dichromate', 'K2Cr2O7')]


def ef_of(f):
    a = atoms(f)
    g = 0
    for v in a.values():
        g = math.gcd(g, v)
    return {e: v // g for e, v in a.items()}, g


def fstr(d):
    order = sorted(d, key=lambda e: (e != 'C', e != 'H', e)) if 'C' in d else list(d)
    return ''.join(f'{e}{"" if d[e] == 1 else d[e]}' for e in order)


def pct_comp(f, dps=1):
    a = atoms(f)
    M = mr(f)
    return {e: round(AR[e] * k / M * 100, dps) for e, k in a.items()}


def solve_ef(pc):
    r = {e: pc[e] / AR[e] for e in pc}
    mn = min(r.values())
    r = {e: v / mn for e, v in r.items()}
    for k in (1, 2, 3, 4):
        if all(abs(k * v - round(k * v)) < 0.08 for v in r.values()):
            return {e: round(k * v) for e, v in r.items()}, r, k
    return None, r, None


R.facts('ch03-st2', F(
    terms=[('empirical formula', 'the simplest whole-number ratio of the atoms of each element in a compound'),
           ('molecular formula', 'the actual number of atoms of each element in one molecule of a compound; a whole-number multiple of the empirical formula'),
           ('percentage composition by mass', 'the mass of each element in a compound expressed as a percentage of the total mass'),
           ('combustion analysis', 'a technique in which an organic compound is burned in excess oxygen and the masses of CO₂ and H₂O formed are used to find its empirical formula')],
    facts=[('What is the empirical formula of glucose, C₆H₁₂O₆?', 'CH₂O', ['C₆H₁₂O₆', 'C₂H₄O₂', 'CHO'], 'Divide by the highest common factor, 6.'),
           ('A compound has the empirical formula CH₂ and Mr = 56.12. What is its molecular formula?', 'C₄H₈', ['CH₂', 'C₂H₄', 'C₅H₁₀'], '56.12/14.03 = 4.'),
           ('Which pair of compounds has the same empirical formula?', 'ethyne, C₂H₂, and benzene, C₆H₆', ['ethane, C₂H₆, and ethene, C₂H₄', 'methane, CH₄, and ethane, C₂H₆', 'water, H₂O, and hydrogen peroxide, H₂O₂'], 'Both are CH.'),
           ('A ratio of atoms in a calculation comes out as C 1 : H 2.5. What is the empirical formula?', 'C₂H₅', ['CH₂', 'CH₃', 'C₂H₅O'], 'Multiply by 2 to obtain whole numbers.')],
    why=[('Explain why the empirical formula alone cannot identify a compound.', 'Many different compounds share the same simplest ratio (e.g. CH₂O for methanal, ethanoic acid and glucose); the molar mass is needed to find the molecular formula, and even then isomers may exist.'),
         ('Explain why, in an empirical formula calculation, a mole ratio of 1 : 1.33 must be multiplied by 3.', '1.33 ≈ 4/3, so multiplying by 3 gives the smallest whole-number ratio 3 : 4; rounding 1.33 to 1 would give the wrong formula.'),
         ('Explain why an ionic compound such as sodium chloride has only an empirical formula and no molecular formula.', 'It is a giant lattice of ions with no discrete molecules; the formula NaCl represents only the simplest ratio of ions.')],
    contrast=[('empirical formula', 'molecular formula', 'The empirical formula gives the simplest whole-number ratio of atoms; the molecular formula gives the actual number of each atom in a molecule and is n × the empirical formula.')],
    misc=[('The empirical formula of hydrogen peroxide, H₂O₂, is H₂O.', 'Dividing by the common factor 2 gives HO; H₂O is a different compound (water).'),
          ('If an element ratio is 1 : 1.5, round it to 1 : 2.', 'Ratios like 1.5 must not be rounded: multiply by 2 to give 2 : 3.')],
    evaluate=[('Combustion analysis is a reliable method for determining the empirical formula of an organic compound.', ['precise masses of CO₂ and H₂O give C and H directly', 'automated CHN analysers are fast and need milligram samples'], ['incomplete combustion or impurities give wrong ratios', 'oxygen is found only by difference, accumulating errors', 'it gives no information on structure or isomers'], 'Reliable for C and H when combustion is complete and samples pure, but must be combined with mass spectrometry and spectroscopy for full identification.')],
))


@R.add('ch03-st2', 'C3', (1, 5), 'numerical')
def c3_ef(rng, slot):
    nm, f = pick(rng, EFC)
    ef, g = ef_of(f)
    pc = pct_comp(f, 1 if slot.d <= 3 else 2)
    sol, r, k = solve_ef(pc)
    if sol != ef:
        return None
    els = list(pc)
    if slot.d >= 3 and rng.random() < 0.6:
        M = mr(f)
        stem = (f'A compound contains ' + ', '.join(f'{pc[e]} % {ENAME[e]}' for e in els) + f' by mass. Its molar mass is {M:.1f} g mol⁻¹. Determine its empirical and molecular formulae.')
        return num(stem, f'EF {chem(fstr(ef))}; MF {chem(fstr(atoms(f)))}', 'Moles: ' + ', '.join(f'{e} {pc[e]}/{AR[e]:.2f}' for e in els) + f' (M1); ratio ' + ' : '.join(f'{r[e]:.2f}' for e in els) + (f' × {k}' if k > 1 else '') + f' → {chem(fstr(ef))} (A1); M(EF) = {mr(fstr(ef)):.2f}, n = {g} (M1); MF {chem(fstr(atoms(f)))} (A1).', 4, 'multi_step')
    stem = pick(rng, ['A compound has the following percentage composition by mass: ', 'Analysis of a sample shows it contains ', 'A laboratory analysis gives the composition by mass: '])
    stem += ', '.join(f'{ENAME[e]} {pc[e]} %' for e in els) + '. Determine the empirical formula.'
    if slot.d <= 2:
        wr = [fstr({e: v * 2 for e, v in ef.items()}), fstr({e: max(1, round(r[e])) for e in els}), fstr({e: ef[e] for e in reversed(els)}[::-1] if False else {e: (ef[e] + 1 if i == 0 else ef[e]) for i, e in enumerate(els)})]
        return mcq(rng, stem.replace('Determine the empirical formula.', 'What is the empirical formula?'), chem(fstr(ef)), [chem(w) for w in wr if w != fstr(ef)][:3] + ([chem(fstr(atoms(f)))] if g > 1 else [chem(fstr({e: ef[e] + 2 if i == 1 else ef[e] for i, e in enumerate(els)}))]),
                   f'Divide each % by Ar, then by the smallest: ratio ' + ' : '.join(f'{r[e]:.2f}' for e in els) + f' → {chem(fstr(ef))}.')
    return num(stem, chem(fstr(ef)), 'n = %/Ar: ' + ', '.join(f'{e} {pc[e] / AR[e]:.3f}' for e in els) + ' (M1); divide by smallest: ' + ' : '.join(f'{r[e]:.2f}' for e in els) + (f'; multiply by {k}' if k > 1 else '') + f' (M1); {chem(fstr(ef))} (A1).', 3)


@R.add('ch03-st2', 'C4', (3, 5), 'multi_step')
def c4_combustion(rng, slot):
    nm, f = pick(rng, [c for c in EFC if set(atoms(c[1])) <= {'C', 'H', 'O'} and 'C' in atoms(c[1])])
    a = atoms(f)
    m = round(rng.uniform(0.2, 1.5), 3)
    n = m / mr(f)
    mco2 = n * a['C'] * mr('CO2')
    mh2o = n * a['H'] / 2 * mr('H2O')
    mco2, mh2o = round(mco2, 3), round(mh2o, 3)
    nC = mco2 / mr('CO2')
    nH = 2 * mh2o / mr('H2O')
    mO = m - nC * 12.01 - nH * 1.01
    nO = max(mO, 0) / 16.00
    ef, g = ef_of(f)
    vals = {'C': nC, 'H': nH}
    if 'O' in a:
        vals['O'] = nO
    mn = min(vals.values())
    ratio = {e: v / mn for e, v in vals.items()}
    stem = (f'A {m:.3f} g sample of an organic compound containing {"carbon, hydrogen and oxygen" if "O" in a else "carbon and hydrogen"} only was burned completely in excess oxygen, '
            f'forming {mco2:.3f} g of carbon dioxide and {mh2o:.3f} g of water. Determine the empirical formula of the compound, showing all working.')
    key = (f'n(C) = n(CO₂) = {mco2:.3f}/44.01 = {nC:.4f} mol (M1); n(H) = 2 × {mh2o:.3f}/18.02 = {nH:.4f} mol (M1); '
           + (f'm(O) = {m:.3f} − {nC * 12.01:.4f} − {nH * 1.01:.4f} = {mO:.4f} g, n(O) = {nO:.4f} mol (M1); ' if 'O' in a else '')
           + 'ratio ' + ' : '.join(f'{e} {ratio[e]:.2f}' for e in vals) + f' (M1) → {chem(fstr(ef))} (A1).')
    sol = {e: ratio[e] for e in vals}
    ok = None
    for k in (1, 2, 3, 4):
        if all(abs(k * v - round(k * v)) < 0.1 for v in sol.values()):
            ok = {e: round(k * v) for e, v in sol.items()}
            break
    if ok != ef:
        return None
    return num(stem, chem(fstr(ef)), key, 5 if 'O' in a else 4, 'multi_step')


@R.add('ch03-st2', 'C3', (2, 4), 'numerical')
def c3_pct(rng, slot):
    nm, f = pick(rng, CMPD + EFC)
    a = atoms(f)
    el = pick(rng, list(a))
    p = AR[el] * a[el] / mr(f) * 100
    stem = pick(rng, [f'Calculate the percentage by mass of {ENAME[el]} in {nm}, {chem(f)}.', f'Determine the mass of {ENAME[el]} in 50.0 g of {nm}, {chem(f)}.'])
    if stem.startswith('Determine'):
        return num(stem, q(p / 2, 'g'), f'% {el} = {a[el]} × {AR[el]:.2f}/{mr(f):.2f} × 100 = {p:.1f} % (M1); 50.0 × {p:.1f}/100 = {q(p / 2, "g")} (A1).', 2)
    return num(stem, f'{p:.1f} %', f'{a[el]} × {AR[el]:.2f}/{mr(f):.2f} × 100 (M1) = {p:.1f} % (A1).', 2)


@R.add('ch03-st2', 'C3', (2, 5), 'numerical')
def c3_ef_mass(rng, slot):
    metal, ox, f = pick(rng, [('magnesium', 'oxide', 'MgO'), ('copper', 'oxide', 'CuO'), ('iron', 'oxide', 'Fe2O3'), ('tin', 'oxide', 'SnO2'), ('aluminium', 'oxide', 'Al2O3'), ('calcium', 'oxide', 'CaO'), ('zinc', 'oxide', 'ZnO'), ('lead', 'oxide', 'PbO')])
    a = atoms(f)
    M = [e for e in a if e != 'O'][0]
    m1 = round(rng.uniform(0.5, 3.0), 3)
    mox = m1 / (AR[M] * a[M]) * mr(f)
    m2 = round(mox, 3)
    nM = m1 / AR[M]
    nO = (m2 - m1) / 16.00
    r = nO / nM
    who = name(rng)
    stem = f'{who} heated {m1:.3f} g of {metal} in a crucible until it had all reacted with oxygen. The mass of {metal} {ox} formed was {m2:.3f} g. Determine the empirical formula of the oxide.'
    return num(stem, chem(f), f'm(O) = {m2:.3f} − {m1:.3f} = {m2 - m1:.3f} g (M1); n({M}) = {nM:.4f}, n(O) = {nO:.4f} (M1); ratio O/{M} = {r:.2f} → {chem(f)} (A1).', 3)


R.mcqs('ch03-st2', 'C2', (1, 4), [
    ('A hydrocarbon contains 85.6 % carbon by mass. What is its empirical formula?', 'CH₂', ['CH', 'CH₃', 'C₂H₅'], 'C 85.6/12.01 = 7.13; H 14.4/1.01 = 14.3; ratio 1 : 2.'),
    ('Which compound has an empirical formula that is the same as its molecular formula?', 'methane, CH₄', ['ethene, C₂H₄', 'hydrogen peroxide, H₂O₂', 'butane, C₄H₁₀'], 'CH₄ cannot be simplified.'),
    ('Which additional information is needed to find a molecular formula from an empirical formula?', 'the molar mass', ['the density', 'the melting point', 'the percentage of each element'], 'n = M(compound)/M(EF).'),
    ('A compound has the empirical formula CH₂O and molar mass 180 g mol⁻¹. How many carbon atoms are in one molecule?', '6', ['1', '3', '12'], '180/30 = 6.'),
])


@p1b(R, 'ch03-st2')
def p1b_mg_oxide(rng, slot):
    m_cr = round(rng.uniform(20, 30), 2)
    m_mg = round(rng.uniform(0.15, 0.35), 2)
    m_ox = round(m_mg * mr('MgO') / AR['Mg'] * rng.uniform(0.93, 0.98), 2)
    mo = m_ox - m_mg
    r = (mo / 16.00) / (m_mg / AR['Mg'])
    intro = (f'A student heated magnesium ribbon in a lidded crucible to find the empirical formula of magnesium oxide. A balance reading to ±0.01 g was used.\n\n'
             f'mass of crucible + lid / g | {m_cr:.2f}\nmass of crucible + lid + Mg / g | {m_cr + m_mg:.2f}\nmass of crucible + lid + product / g | {m_cr + m_ox:.2f}')
    pu = 0.02 / m_mg * 100
    return dict(intro=intro, parts=[
        ('Calculate the mass of magnesium used and the mass of oxygen that reacted.', f'Mg {m_mg:.2f} g; O {mo:.2f} g', f'{m_mg:.2f} g and {mo:.2f} g (A1 A1).', 2),
        ('Determine the mole ratio Mg : O and comment on the result.', f'1 : {r:.2f} (expected 1 : 1)', f'n(Mg) = {m_mg / AR["Mg"]:.4f}, n(O) = {mo / 16:.4f} (M1); ratio 1 : {r:.2f}, lower than 1 : 1 expected (A1).', 2),
        ('Calculate the percentage uncertainty in the mass of magnesium.', f'{pu:.0f} %', f'two readings: ±0.02 g (M1); 0.02/{m_mg:.2f} × 100 = {pu:.0f} % (A1).', 2),
        ('Suggest one reason why the ratio obtained is lower than expected, and one improvement.', 'Magnesium not fully oxidised (or some reacted with nitrogen / MgO smoke escaped when the lid was lifted); heat to constant mass and lift the lid only briefly.', 'Valid cause (1).', 1)],
        extras=[('Suggest how the percentage uncertainty in the mass of magnesium could be reduced.', 'Use a larger mass of magnesium (or a balance with higher resolution, ±0.001 g).', 'Larger mass / more precise balance (1).', 1)])


SOLUTES = [('sodium chloride', 'NaCl'), ('sodium hydroxide', 'NaOH'), ('copper(II) sulfate', 'CuSO4'), ('potassium manganate(VII)', 'KMnO4'),
           ('glucose', 'C6H12O6'), ('sodium carbonate', 'Na2CO3'), ('potassium hydrogen phthalate', 'C8H5KO4'), ('silver nitrate', 'AgNO3'),
           ('calcium chloride', 'CaCl2'), ('ammonium chloride', 'NH4Cl'), ('potassium iodide', 'KI'), ('iron(II) sulfate', 'FeSO4'),
           ('sodium thiosulfate', 'Na2S2O3'), ('ethanedioic acid', 'C2H2O4'), ('magnesium chloride', 'MgCl2'), ('urea', 'CH4N2O')]

R.facts('ch03-st3', F(
    terms=[('concentration', 'the amount (or mass) of solute per unit volume of solution, usually in mol dm⁻³ or g dm⁻³'),
           ('standard solution', 'a solution whose concentration is known accurately'),
           ('solute', 'the substance that dissolves in a solvent to form a solution'),
           ('dilution', 'the addition of solvent to a solution, which lowers its concentration while the amount of solute stays the same'),
           ('volumetric flask', 'a flask calibrated to contain one precise volume at a given temperature, used to make standard solutions')],
    facts=[('What volume of solution, in dm³, is 250 cm³?', '0.250 dm³', ['250 dm³', '2.50 dm³', '0.0250 dm³'], '1 dm³ = 1000 cm³.'),
           ('Which piece of glassware should be used to prepare 250.0 cm³ of a standard solution?', 'a volumetric flask', ['a measuring cylinder', 'a beaker', 'a conical flask'], 'Volumetric flasks have the smallest uncertainty for a fixed volume.'),
           ('A solution has a concentration of 0.100 mol dm⁻³. What amount of solute is in 25.0 cm³?', '2.50 × 10⁻³ mol', ['2.50 mol', '4.00 × 10⁻³ mol', '0.250 mol'], 'n = cV = 0.100 × 0.0250.'),
           ('What is the concentration of chloride ions in 0.20 mol dm⁻³ calcium chloride, CaCl₂?', '0.40 mol dm⁻³', ['0.20 mol dm⁻³', '0.10 mol dm⁻³', '0.60 mol dm⁻³'], 'Each CaCl₂ gives two Cl⁻.'),
           ('What happens to the amount of solute when a solution is diluted?', 'It stays the same.', ['It increases.', 'It decreases.', 'It depends on the solvent.'], 'Only the volume changes.')],
    why=[('Explain why the total volume of solution, not the volume of water added, is used in concentration calculations.', 'Concentration is amount per unit volume of solution; dissolving a solute changes the volume, so a solution is made up to the mark in a volumetric flask.'),
         ('Explain why a solid should be dissolved in a beaker and the washings transferred to the volumetric flask when making a standard solution.', 'This ensures all the solute is dissolved and transferred, so the amount in the flask is exactly the amount weighed; rinsing transfers traces left on the glassware.'),
         ('Explain why c₁V₁ = c₂V₂ can be used for dilution calculations.', 'Adding solvent does not change the amount of solute: n = c₁V₁ before = c₂V₂ after.')],
    contrast=[('mol dm⁻³', 'g dm⁻³', 'mol dm⁻³ gives the amount of solute per dm³; g dm⁻³ gives its mass per dm³; they are related by the molar mass (g dm⁻³ = mol dm⁻³ × M).'),
              ('a concentrated solution', 'a strong acid', 'Concentration describes how much solute is present per volume; strength describes the extent of dissociation – a strong acid can be dilute.')],
    misc=[('Dissolving 0.10 mol of NaCl in 1.00 dm³ of water gives exactly 0.10 mol dm⁻³.', 'The final solution volume is not exactly 1.00 dm³; the solid should be dissolved and made up to 1.00 dm³ of solution.'),
          ('Diluting 10 cm³ of a solution to 100 cm³ halves its concentration.', 'A tenfold increase in volume reduces the concentration by a factor of 10.')],
    evaluate=[('Expressing the concentration of pollutants in parts per million (ppm) is more useful to the public than mol dm⁻³.', ['ppm is intuitive and used in legal limits', 'convenient for very small concentrations'], ['mol dm⁻³ is needed for stoichiometric and toxicological calculations', 'ppm can be ambiguous (mass/mass or volume/volume)'], 'ppm suits communication and regulation; mol dm⁻³ is essential for chemical calculations – the choice depends on the audience.')],
))


@R.add('ch03-st3', 'C3', (1, 5), 'numerical')
def c3_conc(rng, slot):
    nm, f = pick(rng, SOLUTES)
    M = mr(f)
    kind = rng.choice(['c', 'mass', 'gdm', 'dil', 'dilV', 'ion'])
    who = name(rng)
    V = rng.choice([25.0, 50.0, 100.0, 250.0, 500.0, 200.0, 1000.0])
    if kind == 'c':
        m = round(rng.uniform(0.2, 20), 2)
        c = m / M / (V / 1000)
        stem = f'{who} dissolves {m} g of {nm}, {chem(f)}, in water and makes the solution up to {V:.1f} cm³. Calculate the concentration in mol dm⁻³.'
        if slot.d <= 2:
            return nmcq(rng, stem.replace('Calculate the concentration', 'What is the concentration'), c, [m / M / V, m / V * 1000, m / M * V / 1000], 'mol dm⁻³', f'n = {m}/{M:.2f} = {sf(m / M)} mol; c = n/V = {sf(m / M)}/{V / 1000} = {sf(c)} mol dm⁻³ (V in dm³).')
        return num(stem, q(c, 'mol dm⁻³'), f'n = {m}/{M:.2f} = {sf(m / M)} mol (M1); V = {V / 1000} dm³; c = {q(c, "mol dm⁻³")} (A1).', 2)
    if kind == 'mass':
        c = rng.choice([0.0500, 0.100, 0.200, 0.250, 0.0200, 0.500, 1.00, 0.150])
        m = c * V / 1000 * M
        stem = f'Calculate the mass of {nm}, {chem(f)}, needed to prepare {V:.1f} cm³ of a {sf(c)} mol dm⁻³ standard solution.'
        return num(stem, q(m, 'g'), f'n = cV = {sf(c)} × {V / 1000} = {sf(c * V / 1000)} mol (M1); m = n × {M:.2f} = {q(m, "g")} (A1).', 2)
    if kind == 'gdm':
        c = round(rng.uniform(0.02, 1.5), 3)
        g = c * M
        if rng.random() < 0.5:
            stem = f'A solution of {nm} has a concentration of {sf(c)} mol dm⁻³. Calculate its concentration in g dm⁻³.'
            return num(stem, q(g, 'g dm⁻³'), f'{sf(c)} × {M:.2f} (M1) = {q(g, "g dm⁻³")} (A1).', 2)
        stem = f'A solution of {nm} contains {sf(g)} g dm⁻³. Calculate its concentration in mol dm⁻³.'
        return num(stem, q(c, 'mol dm⁻³'), f'{sf(g)}/{M:.2f} (M1) = {q(c, "mol dm⁻³")} (A1).', 2)
    if kind in ('dil', 'dilV'):
        c1 = rng.choice([2.00, 1.00, 0.500, 0.250, 0.100, 1.50])
        v1 = rng.choice([5.00, 10.0, 20.0, 25.0, 50.0])
        v2 = rng.choice([100.0, 250.0, 500.0, 200.0])
        c2 = c1 * v1 / v2
        if kind == 'dil':
            stem = f'{v1} cm³ of {sf(c1)} mol dm⁻³ {nm} solution is diluted with distilled water to {v2:.1f} cm³ in a volumetric flask. Calculate the new concentration.'
            if slot.d <= 2:
                return nmcq(rng, stem.replace('Calculate the new concentration.', 'What is the new concentration?'), c2, [c1 * v2 / v1, c1 * v1 / (v2 + v1), c1 / v2], 'mol dm⁻³', f'c₂ = c₁V₁/V₂ = {sf(c1)} × {v1}/{v2} = {sf(c2)} mol dm⁻³.')
            return num(stem, q(c2, 'mol dm⁻³'), f'c₁V₁ = c₂V₂ (M1); c₂ = {sf(c1)} × {v1}/{v2} = {q(c2, "mol dm⁻³")} (A1).', 2)
        stem = f'Calculate the volume of {sf(c1)} mol dm⁻³ {nm} solution needed to prepare {v2:.1f} cm³ of a {sf(c2)} mol dm⁻³ solution, and state the volume of water to be added.'
        return num(stem, f'{sf(v1)} cm³; add water to make {v2:.1f} cm³ (≈ {sf(v2 - v1)} cm³ of water)', f'V₁ = c₂V₂/c₁ = {sf(c2)} × {v2}/{sf(c1)} (M1) = {sf(v1)} cm³ (A1); make up to {v2:.1f} cm³ (A1).', 3)
    # ion concentrations
    salt, f2, ions = pick(rng, [('calcium chloride', 'CaCl2', [('Ca2+', 1), ('Cl-', 2)]), ('aluminium sulfate', 'Al2(SO4)3', [('Al3+', 2), ('SO4^2-', 3)]),
                                 ('sodium sulfate', 'Na2SO4', [('Na+', 2), ('SO4^2-', 1)]), ('iron(III) chloride', 'FeCl3', [('Fe3+', 1), ('Cl-', 3)]),
                                 ('potassium phosphate', 'K3PO4', [('K+', 3), ('PO4^3-', 1)]), ('magnesium nitrate', 'Mg(NO3)2', [('Mg2+', 1), ('NO3^-', 2)])])
    c = rng.choice([0.0500, 0.100, 0.150, 0.200, 0.250, 0.300])
    io, k = pick(rng, ions)
    stem = f'Calculate the concentration of {ion(io)} ions in a {sf(c)} mol dm⁻³ solution of {salt}, {chem(f2)}, assuming complete dissociation.'
    if slot.d <= 3:
        return nmcq(rng, stem.replace('Calculate', 'What is'), c * k, [c, c / k if k > 1 else c * 2, c * (k + 1)], 'mol dm⁻³', f'{chem(f2)} → ' + ' + '.join(f'{kk}{ion(ii)}' for ii, kk in ions) + f'; [{ion(io)}] = {k} × {sf(c)} = {sf(c * k)} mol dm⁻³.')
    return num(stem, q(c * k, 'mol dm⁻³'), f'{chem(f2)} → ' + ' + '.join(f'{kk}{ion(ii)}' for ii, kk in ions) + f' (M1); {k} × {sf(c)} = {q(c * k, "mol dm⁻³")} (A1).', 2)


@R.add('ch03-st3', 'C4', (3, 5), 'multi_step')
def c4_serial(rng, slot):
    nm, f = pick(rng, SOLUTES[:8])
    M = mr(f)
    m = round(rng.uniform(1, 5), 3)
    V = 250.0
    c0 = m / M / 0.250
    v1 = rng.choice([10.0, 25.0, 20.0])
    v2 = rng.choice([100.0, 250.0])
    c1 = c0 * v1 / v2
    v3 = rng.choice([5.0, 10.0])
    c2 = c1 * v3 / 100.0
    stem = (f'A standard solution was made by dissolving {m:.3f} g of {nm}, {chem(f)}, in water and making up to {V:.1f} cm³. '
            f'{v1} cm³ of this solution was diluted to {v2:.1f} cm³ (solution B); then {v3} cm³ of B was diluted to 100.0 cm³ (solution C). '
            f'(a) Calculate the concentration of the original solution. (b) Calculate the concentration of solution C in mol dm⁻³ and in mg dm⁻³. (c) State one advantage of serial dilution over weighing a tiny mass directly.')
    return num(stem, f'(a) {q(c0, "mol dm⁻³")}; (b) {q(c2, "mol dm⁻³")} = {q(c2 * M * 1000, "mg dm⁻³")}',
               f'(a) n = {m:.3f}/{M:.2f} = {sf(m / M)} mol; c = {q(c0, "mol dm⁻³")} (M1 A1). (b) dilution factors {v2 / v1:g} and {100 / v3:g} (M1); c(C) = {q(c2, "mol dm⁻³")} (A1); × {M:.2f} × 1000 = {q(c2 * M * 1000, "mg dm⁻³")} (A1). (c) The percentage uncertainty in weighing a very small mass would be very large (R1).', 6, 'multi_step')


R.mcqs('ch03-st3', 'C2', (1, 4), [
    ('Which solution contains the greatest amount of solute?', '50.0 cm³ of 0.200 mol dm⁻³', ['100 cm³ of 0.0500 mol dm⁻³', '25.0 cm³ of 0.300 mol dm⁻³', '200 cm³ of 0.0400 mol dm⁻³'], '0.0100 mol vs 0.00500, 0.00750, 0.00800.'),
    ('Water is added to 100 cm³ of 0.50 mol dm⁻³ NaCl(aq) until the volume is 250 cm³. What is the new concentration?', '0.20 mol dm⁻³', ['1.25 mol dm⁻³', '0.25 mol dm⁻³', '0.33 mol dm⁻³'], '0.50 × 100/250.'),
    ('Which solution has the highest concentration of ions?', '0.10 mol dm⁻³ Al₂(SO₄)₃', ['0.10 mol dm⁻³ NaCl', '0.10 mol dm⁻³ CaCl₂', '0.20 mol dm⁻³ KNO₃'], 'Al₂(SO₄)₃ gives 5 ions per formula unit: 0.50 mol dm⁻³.'),
    ('A student uses a measuring cylinder instead of a volumetric flask to make a standard solution. What is the main effect?', 'larger uncertainty in the concentration', ['the concentration will be systematically too high', 'the solute will not dissolve', 'no effect'], 'Measuring cylinders are less precise.'),
])
repeat_readings(R, 'ch03-st3', 'the mass of solute', 'g', 1.0, 5.0, 3, ['weighed the solid for a standard solution on a ±0.001 g balance several times.', 'checked the mass of a weighing boat containing solute in repeated weighings.'])


R.facts('ch03-st4', F(
    terms=[("Avogadro's law", 'equal volumes of all gases at the same temperature and pressure contain equal numbers of particles'),
           ('molar volume of a gas', 'the volume occupied by one mole of any ideal gas at a stated temperature and pressure; 22.7 dm³ mol⁻¹ at STP (273 K, 100 kPa)'),
           ('standard temperature and pressure (STP)', 'a temperature of 273 K (0 °C) and a pressure of 100 kPa')],
    facts=[('What volume does 2.00 mol of an ideal gas occupy at STP?', '45.4 dm³', ['22.7 dm³', '11.4 dm³', '44.8 dm³'], 'V = n × 22.7.'),
           ('Which contains the same number of molecules as 1.0 dm³ of nitrogen at STP?', '1.0 dm³ of carbon dioxide at STP', ['1.0 g of carbon dioxide', '2.0 dm³ of hydrogen at STP', '1.0 dm³ of water at STP'], "Avogadro's law (water is not a gas at STP)."),
           ('What is the molar volume of an ideal gas at STP according to the IB data booklet?', '22.7 dm³ mol⁻¹', ['22.4 dm³ mol⁻¹', '24.0 dm³ mol⁻¹', '8.31 dm³ mol⁻¹'], 'At 273 K and 100 kPa.'),
           ('2 dm³ of hydrogen reacts with chlorine: H₂(g) + Cl₂(g) → 2HCl(g). What volume of HCl forms at the same T and p?', '4 dm³', ['2 dm³', '1 dm³', '6 dm³'], 'Volume ratio = mole ratio.')],
    why=[("Explain why, according to Avogadro's law, equal volumes of hydrogen and carbon dioxide at the same temperature and pressure contain the same number of molecules.", 'In an ideal gas the volume of the particles themselves is negligible and there are no intermolecular forces, so the volume depends only on the number of particles, T and p, not on their identity or size.'),
         ('Explain why volumes of gases in a reaction are in the same ratio as the coefficients in the balanced equation.', 'At constant T and p, volume is proportional to amount (Avogadro), so the mole ratio from the equation equals the volume ratio.'),
         ('Explain why the molar volume of a gas at room temperature (298 K) is larger than at STP.', 'At constant pressure the volume of a fixed amount of gas is proportional to absolute temperature, so it is larger at 298 K (about 24.8 dm³ mol⁻¹ at 100 kPa).')],
    contrast=[("Avogadro's law", 'the molar volume', "Avogadro's law states equal volumes of gases contain equal numbers of particles at the same T and p; the molar volume is the specific volume of one mole under stated conditions (22.7 dm³ at STP).")],
    misc=[('One mole of liquid water occupies 22.7 dm³ at STP.', 'Molar volume applies only to gases; one mole of liquid water occupies only about 18 cm³.'),
          ('Equal masses of different gases occupy equal volumes at the same temperature and pressure.', 'Equal amounts (moles) occupy equal volumes; equal masses of gases with different molar masses contain different amounts.')],
    evaluate=[("Avogadro's law applies to all gases under all conditions.", ['works well for most gases at ordinary T and p', 'basis of molar volume calculations'], ['real gases deviate at high pressure and low temperature', 'polar or large molecules (e.g. NH₃, CO₂) deviate more due to intermolecular forces and particle volume'], 'It is an ideal-gas law – an excellent approximation at low pressure and high temperature but not exact for real gases.')],
))

GASRX = [('C3H8(g) + 5O2(g) → 3CO2(g) + 4H2O(l)', {'C3H8': 1, 'O2': 5, 'CO2': 3}, 'propane'),
         ('CH4(g) + 2O2(g) → CO2(g) + 2H2O(l)', {'CH4': 1, 'O2': 2, 'CO2': 1}, 'methane'),
         ('N2(g) + 3H2(g) → 2NH3(g)', {'N2': 1, 'H2': 3, 'NH3': 2}, 'nitrogen'),
         ('2CO(g) + O2(g) → 2CO2(g)', {'CO': 2, 'O2': 1, 'CO2': 2}, 'carbon monoxide'),
         ('2C2H6(g) + 7O2(g) → 4CO2(g) + 6H2O(l)', {'C2H6': 2, 'O2': 7, 'CO2': 4}, 'ethane'),
         ('C2H4(g) + 3O2(g) → 2CO2(g) + 2H2O(l)', {'C2H4': 1, 'O2': 3, 'CO2': 2}, 'ethene'),
         ('2SO2(g) + O2(g) → 2SO3(g)', {'SO2': 2, 'O2': 1, 'SO3': 2}, 'sulfur dioxide'),
         ('2NO(g) + O2(g) → 2NO2(g)', {'NO': 2, 'O2': 1, 'NO2': 2}, 'nitrogen monoxide'),
         ('2C4H10(g) + 13O2(g) → 8CO2(g) + 10H2O(l)', {'C4H10': 2, 'O2': 13, 'CO2': 8}, 'butane')]


@R.add('ch03-st4', 'C3', (1, 5), 'numerical')
def c3_molvol(rng, slot):
    kind = rng.choice(['n2V', 'V2m', 'm2V', 'react', 'density'])
    gas, f = pick(rng, [('oxygen', 'O2'), ('carbon dioxide', 'CO2'), ('nitrogen', 'N2'), ('methane', 'CH4'), ('ammonia', 'NH3'), ('chlorine', 'Cl2'), ('hydrogen', 'H2'), ('sulfur dioxide', 'SO2'), ('argon', 'Ar'), ('propane', 'C3H8')])
    M = mr(f)
    if kind == 'n2V':
        n = float(f'{rng.uniform(0.02, 4):.3g}')
        stem = f'Calculate the volume occupied by {sf(n)} mol of {gas} at STP.'
        return num(stem, q(n * VM, 'dm³'), f'V = n × 22.7 = {sf(n)} × 22.7 (M1) = {q(n * VM, "dm³")} (A1).', 2)
    if kind == 'V2m':
        V = round(rng.uniform(0.1, 50), 2)
        m = V / VM * M
        stem = f'Calculate the mass of {sf(V)} dm³ of {gas}, {chem(f)}, measured at STP.'
        if slot.d <= 2:
            return nmcq(rng, stem.replace('Calculate', 'What is'), m, [V * VM * M / 1000, V / 22.4 * M, V * M], 'g', f'n = {sf(V)}/22.7 = {sf(V / VM)} mol; m = {sf(V / VM)} × {M:.2f} = {q(m, "g")}.')
        return num(stem, q(m, 'g'), f'n = V/22.7 = {sf(V / VM)} mol (M1); m = nM = {q(m, "g")} (A1).', 2)
    if kind == 'm2V':
        m = round(rng.uniform(0.5, 100), 1)
        V = m / M * VM
        stem = f'A cylinder releases {m} g of {gas}. Calculate the volume this gas would occupy at STP, in cm³.' if V < 2 else f'Calculate the volume, at STP, occupied by {m} g of {gas}, {chem(f)}.'
        if V < 2:
            return num(stem, q(V * 1000, 'cm³'), f'n = {m}/{M:.2f} (M1); V = n × 22.7 dm³ = {q(V * 1000, "cm³")} (A1).', 2)
        return num(stem, q(V, 'dm³'), f'n = {m}/{M:.2f} = {sf(m / M)} mol (M1); V = {q(V, "dm³")} (A1).', 2)
    if kind == 'density':
        stem = f'Calculate the density of {gas}, {chem(f)}, at STP in g dm⁻³.'
        return num(stem, q(M / VM, 'g dm⁻³'), f'1 mol has mass {M:.2f} g and volume 22.7 dm³ (M1); ρ = {M:.2f}/22.7 = {q(M / VM, "g dm⁻³")} (A1).', 2)
    eq, co, fuel = pick(rng, GASRX)
    sps = list(co)
    a, b = rng.sample(sps, 2)
    Va = rng.choice([10.0, 20.0, 25.0, 50.0, 100.0, 15.0, 40.0, 60.0])
    Vb = Va * co[b] / co[a]
    stem = f'Consider the reaction {chem(eq)}. Calculate the volume of {chem(b)} that reacts with or is produced from {sf(Va)} cm³ of {chem(a)}, all volumes measured at the same temperature and pressure.'
    return num(stem, q(Vb, 'cm³'), f'Volume ratio = mole ratio {chem(a)} : {chem(b)} = {co[a]} : {co[b]} (M1); V = {sf(Va)} × {co[b]}/{co[a]} = {q(Vb, "cm³")} (A1).', 2)


@R.add('ch03-st4', 'C4', (3, 5), 'multi_step')
def c4_gas_mix(rng, slot):
    eq, co, fuel = pick(rng, [g for g in GASRX if 'H2O' in g[0]])
    f = [k for k in co if k not in ('O2', 'CO2')][0]
    vf = rng.choice([10.0, 20.0, 25.0, 30.0, 50.0])
    vo = vf * co['O2'] / co[f] * rng.choice([1.2, 1.5, 2.0, 1.4])
    vo = round(vo)
    used = vf * co['O2'] / co[f]
    vco2 = vf * co['CO2'] / co[f]
    left = vo - used
    stem = (f'{sf(vf)} cm³ of {fuel} is exploded with {vo} cm³ of oxygen: {chem(eq)}. After cooling to the original room temperature and pressure, water is a liquid. '
            f'(a) Determine the volume of each gas remaining. (b) Determine the total gas volume. (c) State and explain how the volume would change if the mixture were then passed through aqueous sodium hydroxide.')
    return num(stem, f'(a) CO₂ {sf(vco2)} cm³, O₂ {sf(left)} cm³; (b) {sf(vco2 + left)} cm³; (c) falls to {sf(left)} cm³ as CO₂ is absorbed', f'(a) O₂ used = {sf(vf)} × {co["O2"]}/{co[f]} = {sf(used)} cm³ (M1); O₂ left {sf(left)} cm³ (A1); CO₂ = {sf(vco2)} cm³ (A1). (b) {sf(vco2 + left)} cm³ (A1). (c) NaOH (an alkali) absorbs the acidic CO₂, leaving {sf(left)} cm³ O₂ (R1).', 5, 'multi_step')


R.mcqs('ch03-st4', 'C2', (1, 4), [
    ('At STP, which gas sample has the greatest volume?', '4.0 g of helium', ['16 g of oxygen', '22 g of carbon dioxide', '14 g of nitrogen'], '4.0 g He = 1.0 mol; the others are 0.50 mol.'),
    ('At constant T and p, 1 volume of a gaseous element reacts with 3 volumes of hydrogen to give 2 volumes of a single product. Which element?', 'nitrogen', ['oxygen', 'chlorine', 'carbon'], 'N₂ + 3H₂ → 2NH₃.'),
    ('Why do 1 mol of H₂ and 1 mol of CO₂ occupy the same volume at STP?', 'Particle volume is negligible compared with the volume of the gas.', ['They have the same mass.', 'They have the same intermolecular forces.', 'They have the same speed.'], 'Ideal-gas behaviour.'),
    ('20 cm³ of methane is burned completely in excess oxygen. What volume of CO₂ forms at the same T and p?', '20 cm³', ['40 cm³', '10 cm³', '60 cm³'], 'CH₄ : CO₂ = 1 : 1.'),
])


# =============================================================================================
# ch04 S1.5 Ideal gases
# =============================================================================================
R.facts('ch04-st1', F(
    terms=[('ideal gas', 'a theoretical gas whose particles have negligible volume, no intermolecular forces, move randomly and undergo perfectly elastic collisions, so that it obeys pV = nRT exactly'),
           ('real gas', 'a gas whose particles have a finite volume and attract one another, so that it deviates from ideal behaviour, especially at high pressure and low temperature'),
           ('elastic collision', 'a collision in which the total kinetic energy of the particles is conserved'),
           ('compression factor', 'the ratio pV/(nRT) for a gas; it equals 1 for an ideal gas')],
    facts=[('Under which conditions does a real gas behave most like an ideal gas?', 'high temperature and low pressure', ['low temperature and high pressure', 'high temperature and high pressure', 'low temperature and low pressure'], 'Particles far apart and fast: forces and particle volume negligible.'),
           ('Which is NOT an assumption of the ideal gas model?', 'Particles attract each other weakly.', ['Particles have negligible volume.', 'Collisions are perfectly elastic.', 'Particles move in rapid random motion.'], 'Ideal: no intermolecular forces.'),
           ('Which gas deviates most from ideal behaviour at 273 K and 100 kPa?', 'ammonia', ['helium', 'hydrogen', 'neon'], 'NH₃ is polar with hydrogen bonding – strongest intermolecular forces.'),
           ('Why does the volume of a real gas at very high pressure exceed the ideal value?', 'The volume of the particles themselves is no longer negligible.', ['Intermolecular attractions increase the volume.', 'The particles move faster.', 'Collisions become elastic.'], 'At high p, particle volume is a significant fraction of the total.')],
    why=[('Explain why real gases deviate from ideal behaviour at low temperatures.', 'At low temperature the particles move more slowly, so intermolecular attractions become significant compared with their kinetic energy; collisions with the walls are less forceful and pressure (pV) is lower than predicted.'),
         ('Explain why helium behaves more ideally than carbon dioxide at the same temperature and pressure.', 'Helium atoms are very small with very weak London dispersion forces; CO₂ molecules are larger, with more electrons and stronger dispersion forces, so attractions and particle volume matter more.'),
         ('Explain why gases deviate from ideal behaviour at high pressure.', 'Particles are forced close together, so the volume of the particles is a significant fraction of the container and intermolecular forces become significant.'),
         ('Explain why a gas would liquefy if cooled enough, although an ideal gas never would.', 'Real particles attract each other; at low enough kinetic energy the attractions hold particles together as a liquid; ideal-gas particles have no attractions so cannot condense.')],
    contrast=[('an ideal gas', 'a real gas', 'An ideal gas has particles of zero volume with no intermolecular forces and obeys pV = nRT exactly; a real gas has particles of finite volume with attractions and deviates, especially at high p and low T.')],
    misc=[('Real gases deviate from ideal behaviour most at high temperatures because the particles move fastest.', 'Deviations are greatest at low temperature (and high pressure), when slow particles allow intermolecular attractions to become significant.'),
          ('The ideal gas model assumes that gas particles have no mass.', 'The model assumes negligible particle volume and no intermolecular forces, not zero mass; particle mass determines momentum transfer in collisions.')],
    evaluate=[('The ideal gas model is useful even though no real gas is ideal.', ['accurate within a few percent for most gases near room conditions', 'simple equation allows quick calculations', 'basis of molar volume and gas stoichiometry'], ['fails for high-pressure industrial processes (e.g. Haber process at 20 MPa)', 'cannot predict condensation', 'polar gases deviate significantly'], 'The model is valuable within its domain of validity; for high pressure or low temperature, corrected models (e.g. van der Waals) are required – a NOS example of model limitations.')],
))

REALG = [('helium', 4.00, 'very weak London forces, tiny atoms'), ('hydrogen', 2.02, 'very weak London forces'), ('neon', 20.18, 'weak London forces'),
         ('nitrogen', 28.02, 'weak London forces'), ('methane', 16.05, 'London forces'), ('carbon dioxide', 44.01, 'stronger London forces, larger molecule'),
         ('ammonia', 17.04, 'hydrogen bonding'), ('sulfur dioxide', 64.07, 'dipole–dipole and London forces'), ('water vapour', 18.02, 'hydrogen bonding'),
         ('hydrogen chloride', 36.46, 'dipole–dipole forces')]
RANK = {'helium': 0, 'hydrogen': 1, 'neon': 2, 'nitrogen': 3, 'methane': 4, 'hydrogen chloride': 5, 'carbon dioxide': 6, 'sulfur dioxide': 7, 'ammonia': 8, 'water vapour': 9}


@R.add('ch04-st1', 'C3', (1, 4), 'mcq')
def c3_most_ideal(rng, slot):
    pool = rng.sample(REALG, 4)
    if rng.random() < 0.5:
        best = min(pool, key=lambda g: RANK[g[0]])
        stem = 'Under the same conditions, which gas behaves most like an ideal gas?'
    else:
        best = max(pool, key=lambda g: RANK[g[0]])
        stem = 'At the same temperature and pressure, which gas shows the greatest deviation from ideal behaviour?'
    return mcq(rng, stem, best[0], [g[0] for g in pool if g != best], f'{best[0]}: {best[2]}. Deviation increases with intermolecular forces and particle size.')


@R.add('ch04-st1', 'C3', (2, 5), 'numerical')
def c3_compress(rng, slot):
    gas, M, why = pick(rng, REALG[3:])
    n = 1.00
    T = rng.choice([273, 298, 350, 400, 250])
    p = rng.choice([100, 1000, 5000, 10000, 20000])  # kPa
    Videal = n * RGAS * T / (p * 1000)  # m3
    Z_ = rng.uniform(0.85, 0.99) if p >= 1000 else rng.uniform(0.98, 1.0)
    Vreal = Videal * Z_
    Vd = Vreal * 1000
    stem = (f'1.00 mol of {gas} at {T} K and {p} kPa occupies {sf(Vd)} dm³. Calculate the volume predicted by the ideal gas equation, '
            f'the ratio pV/(nRT), and explain the deviation.')
    return num(stem, f'ideal {sf(Videal * 1000)} dm³; pV/nRT = {Z_:.3f}', f'V(ideal) = nRT/p = 1.00 × 8.31 × {T}/({p} × 10³) m³ = {sf(Videal * 1000)} dm³ (M1 A1); pV/nRT = {sf(Vd)}/{sf(Videal * 1000)} = {Z_:.3f} (A1); < 1 because intermolecular attractions ({why}) reduce the pressure/volume (R1).', 4, 'multi_step')


R.mcqs('ch04-st1', 'C2', (1, 4), [
    ('Which statement explains why real gases have lower pressures than predicted at low temperature?', 'Attractions between particles reduce the force of collisions with the walls.', ['Particle volume becomes significant.', 'Particles move faster.', 'The number of particles decreases.'], 'Attractions pull particles away from walls.'),
    ('The value of pV/nRT for a gas at very high pressure is greater than 1. Why?', 'The finite volume of the particles reduces the free space available.', ['Attractive forces dominate.', 'The temperature has fallen.', 'The gas has dissociated.'], 'Repulsion/particle volume dominates at high p.'),
    ('Which change makes nitrogen gas behave less ideally?', 'decreasing the temperature at constant pressure', ['increasing the temperature at constant pressure', 'decreasing the pressure at constant temperature', 'increasing the volume of the container'], 'Lower T → attractions more significant.'),
    ('Which property of xenon explains why it deviates more from ideal behaviour than helium?', 'Xenon has many more electrons, so stronger London dispersion forces.', ['Xenon is more reactive.', 'Xenon atoms are lighter.', 'Xenon forms hydrogen bonds.'], 'Polarisability increases with electron number.'),
])


R.facts('ch04-st2', F(
    terms=[('ideal gas equation', 'pV = nRT, where p is pressure in Pa, V volume in m³, n amount in mol, R = 8.31 J K⁻¹ mol⁻¹ and T temperature in K'),
           ("Boyle's law", 'for a fixed amount of gas at constant temperature, pressure is inversely proportional to volume (pV = constant)'),
           ("Charles's law", 'for a fixed amount of gas at constant pressure, volume is directly proportional to absolute temperature (V/T = constant)'),
           ("Gay-Lussac's (pressure) law", 'for a fixed amount of gas at constant volume, pressure is directly proportional to absolute temperature (p/T = constant)'),
           ('gas constant (R)', 'the constant of proportionality in pV = nRT, 8.31 J K⁻¹ mol⁻¹')],
    facts=[('What are the SI units of pressure and volume in pV = nRT?', 'Pa and m³', ['kPa and dm³', 'atm and cm³', 'kPa and m³'], 'With R = 8.31 J K⁻¹ mol⁻¹ use Pa and m³ (or kPa with dm³, which also gives J).'),
           ('A fixed mass of gas at constant temperature has its pressure doubled. What happens to its volume?', 'It halves.', ['It doubles.', 'It stays the same.', 'It quadruples.'], 'Boyle: p ∝ 1/V.'),
           ('Which graph is a straight line through the origin for a fixed mass of gas at constant pressure?', 'V against T (in K)', ['V against T (in °C)', 'p against V', 'V against 1/T'], "Charles's law."),
           ('How many m³ is 500 cm³?', '5.00 × 10⁻⁴ m³', ['0.500 m³', '5.00 × 10⁻² m³', '5.00 × 10⁻⁶ m³'], '1 m³ = 10⁶ cm³.')],
    why=[('Explain, using kinetic theory, why the pressure of a gas increases when it is heated in a sealed rigid container.', 'Heating increases the average kinetic energy and speed of the particles; they collide with the walls more frequently and with greater force, so the pressure increases (p ∝ T at constant V).'),
         ('Explain why the pressure of a gas increases when its volume is reduced at constant temperature.', 'The same number of particles occupy a smaller space, so they hit the walls more often per unit area; average kinetic energy is unchanged, so pressure increases.'),
         ('Explain why a graph of V against temperature in °C for a gas at constant pressure does not pass through the origin.', 'Volume is proportional to absolute temperature; on the Celsius scale zero is 273 K, so the line extrapolates to zero volume at −273 °C rather than at 0 °C.')],
    contrast=[("Boyle's law", "Charles's law", "Boyle's law relates p and V at constant T (inverse proportionality); Charles's law relates V and T at constant p (direct proportionality with T in K).")],
    misc=[('If the temperature of a gas rises from 10 °C to 20 °C at constant pressure, its volume doubles.', 'Volume ∝ absolute temperature: 283 K → 293 K increases V by only 3.5 %.'),
          ('In pV = nRT, volume can be entered in dm³ with pressure in Pa.', 'Units must be consistent: Pa with m³ (or kPa with dm³); Pa with dm³ gives an answer 1000 times too large.')],
    evaluate=[('pV = nRT is the only gas equation a chemist needs.', ['it combines Boyle, Charles and Avogadro in one equation', 'works well for most gases at moderate conditions'], ['not valid for real gases at high pressure/low temperature', 'combined gas law (p₁V₁/T₁ = p₂V₂/T₂) is more convenient when n is constant'], 'It is the central equation but must be applied within its ideal limits and with consistent units.')],
))

GASES = [('nitrogen', 'N2'), ('oxygen', 'O2'), ('carbon dioxide', 'CO2'), ('methane', 'CH4'), ('helium', 'He'), ('argon', 'Ar'),
         ('hydrogen', 'H2'), ('neon', 'Ne'), ('ammonia', 'NH3'), ('propane', 'C3H8'), ('chlorine', 'Cl2'), ('butane', 'C4H10'),
         ('sulfur hexafluoride', 'SF6')]


@R.add('ch04-st2', 'C3', (1, 5), 'numerical')
def c3_pvnrt(rng, slot):
    gas, f = pick(rng, GASES)
    kind = rng.choice(['V', 'p', 'n', 'm', 'T'])
    T = rng.choice([273, 293, 298, 310, 350, 373, 400, 500, 250])
    tc = T - 273
    tdesc = f'{tc} °C' if rng.random() < 0.6 else f'{T} K'
    pk = rng.choice([100, 101, 150, 200, 250, 500, 80.0, 95.0, 120])
    if f == 'SF6':
        AR['F']  # noqa
    M = sum(AR[e] * k for e, k in atoms(f).items()) if all(e in AR for e in atoms(f)) else None
    if M is None:
        return None
    ctx = pick(rng, ['in a gas syringe', 'in a sealed flask', 'in a weather balloon', 'in a steel cylinder', 'in a bulb', 'in a container'])
    if kind == 'V':
        n = float(f'{rng.uniform(0.01, 2):.3g}')
        V = n * RGAS * T / (pk * 1000) * 1000
        stem = f'Calculate the volume, in dm³, occupied by {sf(n)} mol of {gas} {ctx} at {tdesc} and {pk} kPa.'
        if slot.d <= 2:
            return nmcq(rng, stem.replace('Calculate the volume', 'What is the volume'), V, [n * RGAS * tc / pk if tc > 0 else V * 3, V * 1000, V / 1000], 'dm³', f'V = nRT/p = {sf(n)} × 8.31 × {T}/{pk} kPa = {sf(V)} dm³ (kPa with dm³; T in K).')
        return num(stem, q(V, 'dm³'), f'T = {T} K (M1); V = nRT/p = {sf(n)} × 8.31 × {T}/({pk} × 10³) m³ (M1) = {q(V, "dm³")} (A1).', 3)
    if kind == 'p':
        n = float(f'{rng.uniform(0.05, 3):.3g}')
        Vd = rng.choice([1.00, 2.50, 5.00, 10.0, 0.500, 20.0])
        p = n * RGAS * T / (Vd / 1000) / 1000
        stem = f'{sf(n)} mol of {gas} is held {ctx} of volume {sf(Vd)} dm³ at {tdesc}. Calculate the pressure in kPa.'
        return num(stem, q(p, 'kPa'), f'p = nRT/V = {sf(n)} × 8.31 × {T}/({sf(Vd)} × 10⁻³) Pa (M1) = {q(p, "kPa")} (A1).', 2)
    if kind in ('n', 'm'):
        Vc = rng.choice([100, 250, 500, 1000, 50.0, 75.0, 200])
        n = pk * 1000 * Vc * 1e-6 / (RGAS * T)
        if kind == 'n':
            stem = f'A {Vc} cm³ sample of {gas} {ctx} is at {tdesc} and {pk} kPa. Calculate the amount of gas in mol.'
            return num(stem, q(n, 'mol'), f'n = pV/RT = {pk} × 10³ × {Vc} × 10⁻⁶/(8.31 × {T}) (M1, unit conversion) = {q(n, "mol")} (A1).', 2)
        stem = f'Calculate the mass of {gas}, {chem(f)}, in a {Vc} cm³ container at {tdesc} and {pk} kPa.'
        return num(stem, q(n * M, 'g'), f'n = pV/RT = {sf(n)} mol (M1); m = n × {M:.2f} (M1) = {q(n * M, "g")} (A1).', 3)
    n = float(f'{rng.uniform(0.05, 1):.3g}')
    Vd = rng.choice([1.00, 2.00, 5.00, 10.0])
    p = rng.choice([100, 150, 200, 300, 500])
    Tx = p * 1000 * Vd / 1000 / (n * RGAS)
    if Tx < 150 or Tx > 3000:
        return None
    stem = f'At what temperature, in °C, would {sf(n)} mol of {gas} exert a pressure of {p} kPa in a {sf(Vd)} dm³ vessel?'
    return num(stem, f'{Tx - 273:.0f} °C ({sf(Tx)} K)', f'T = pV/nR = {p} × 10³ × {sf(Vd)} × 10⁻³/({sf(n)} × 8.31) (M1) = {sf(Tx)} K (A1) = {Tx - 273:.0f} °C (A1).', 3)


@R.add('ch04-st2', 'C3', (1, 5), 'numerical')
def c3_gaslaws(rng, slot):
    kind = rng.choice(['boyle', 'charles', 'pressure', 'combined'])
    who = name(rng)
    if kind == 'boyle':
        p1 = rng.choice([100, 101, 120, 150, 200])
        V1 = rng.choice([50.0, 100, 250, 500, 30.0, 80.0])
        p2 = rng.choice([v for v in [50, 80, 250, 300, 400, 600] if v != p1])
        V2 = p1 * V1 / p2
        stem = f'{who} compresses {sf(V1)} cm³ of air in a syringe at {p1} kPa to a pressure of {p2} kPa at constant temperature. Calculate the new volume.'
        if slot.d <= 2:
            return nmcq(rng, stem.replace('Calculate the new volume.', 'What is the new volume?'), V2, [V1 * p2 / p1, V1 * p1 / (p2 + p1), V1], 'cm³', f'p₁V₁ = p₂V₂: V₂ = {p1} × {sf(V1)}/{p2} = {sf(V2)} cm³.')
        return num(stem, q(V2, 'cm³'), f'p₁V₁ = p₂V₂ (M1); V₂ = {p1} × {sf(V1)}/{p2} = {q(V2, "cm³")} (A1).', 2)
    if kind == 'charles':
        t1 = rng.choice([0, 15, 20, 25, 27])
        t2 = rng.choice([50, 80, 100, 127, 150, -20, -50])
        V1 = rng.choice([1.00, 2.50, 3.00, 5.00, 10.0])
        V2 = V1 * (t2 + 273) / (t1 + 273)
        stem = f'A balloon holds {sf(V1)} dm³ of helium at {t1} °C. The balloon is moved to a place at {t2} °C at the same pressure. Calculate the new volume.'
        if slot.d <= 3:
            return nmcq(rng, stem.replace('Calculate the new volume.', 'What is the new volume?'), V2, [V1 * t2 / t1 if t1 else V1 * 2.7, V1 * (t1 + 273) / (t2 + 273), V1 + (t2 - t1) / 273], 'dm³', f'V/T constant: V₂ = {sf(V1)} × {t2 + 273}/{t1 + 273} = {sf(V2)} dm³ (T in K).')
        return num(stem, q(V2, 'dm³'), f'T₁ = {t1 + 273} K, T₂ = {t2 + 273} K (M1); V₂ = V₁T₂/T₁ = {q(V2, "dm³")} (A1).', 2)
    if kind == 'pressure':
        t1 = rng.choice([15, 20, 25])
        t2 = rng.choice([40, 50, 60, 80, -10])
        p1 = rng.choice([220, 250, 300, 200])
        p2 = p1 * (t2 + 273) / (t1 + 273)
        stem = f'A car tyre contains air at {p1} kPa and {t1} °C. After driving, the temperature of the air is {t2} °C. Assuming constant volume, calculate the new pressure.'
        return num(stem, q(p2, 'kPa'), f'p/T constant (M1); p₂ = {p1} × {t2 + 273}/{t1 + 273} = {q(p2, "kPa")} (A1).', 2)
    p1, V1, t1 = rng.choice([100, 101, 95.0]), rng.choice([250, 500, 1000, 120]), rng.choice([20, 25, 18])
    p2, t2 = rng.choice([200, 300, 50.0, 400]), rng.choice([0, 100, 150, -30])
    V2 = p1 * V1 * (t2 + 273) / ((t1 + 273) * p2)
    stem = f'A sample of gas occupies {V1} cm³ at {p1} kPa and {t1} °C. Calculate its volume at {p2} kPa and {t2} °C.'
    return num(stem, q(V2, 'cm³'), f'p₁V₁/T₁ = p₂V₂/T₂ (M1); temperatures in K: {t1 + 273} and {t2 + 273} (M1); V₂ = {q(V2, "cm³")} (A1).', 3)


@R.add('ch04-st2', 'C4', (3, 5), 'multi_step')
def c4_airbag(rng, slot):
    kind = rng.choice(['airbag', 'balloon', 'diver'])
    if kind == 'airbag':
        V = rng.choice([50.0, 60.0, 65.0, 70.0])
        T = rng.choice([300, 310, 320, 350])
        p = rng.choice([120, 130, 140, 150])
        n = p * 1000 * V / 1000 / (RGAS * T)
        nNaN3 = n * 2 / 3
        m = nNaN3 * mr('NaN3')
        stem = (f'A car airbag inflates with nitrogen formed by the decomposition 2NaN₃(s) → 2Na(s) + 3N₂(g). The bag must reach a volume of {V} dm³ at {p} kPa and {T} K. '
                f'(a) Calculate the amount of N₂ required. (b) Calculate the minimum mass of sodium azide, NaN₃, needed. (c) Suggest why the real gas behaviour of N₂ makes little difference here.')
        return num(stem, f'(a) {q(n, "mol")}; (b) {q(m, "g")}', f'(a) n = pV/RT = {p} × 10³ × {V} × 10⁻³/(8.31 × {T}) (M1) = {q(n, "mol")} (A1). (b) n(NaN₃) = 2/3 × n(N₂) = {sf(nNaN3)} mol (M1); × 65.02 = {q(m, "g")} (A1). (c) Moderate pressure and temperature; N₂ is non-polar with weak forces – close to ideal (R1).', 5, 'multi_step')
    if kind == 'balloon':
        V1 = rng.choice([5.0, 8.0, 10.0])
        p1, t1 = 100, rng.choice([15, 20, 25])
        p2, t2 = rng.choice([30.0, 25.0, 20.0, 12.0]), rng.choice([-40, -50, -56, -45])
        V2 = p1 * V1 * (t2 + 273) / ((t1 + 273) * p2)
        n = p1 * 1000 * V1 / (RGAS * (t1 + 273))
        stem = (f'A weather balloon is filled with {V1:.1f} m³ of helium at {p1} kPa and {t1} °C at ground level. It rises to an altitude where the pressure is {p2} kPa and the temperature is {t2} °C. '
                f'(a) Calculate the amount of helium. (b) Calculate the volume of the balloon at altitude. (c) Explain, with reference to particles, which change (p or T) has the greater effect on the volume.')
        return num(stem, f'(a) {q(n, "mol")}; (b) {q(V2, "m³")}', f'(a) n = pV/RT = {q(n, "mol")} (M1 A1). (b) V₂ = p₁V₁T₂/(T₁p₂) = {q(V2, "m³")} (M1 A1). (c) pressure falls by a factor of {p1 / p2:.1f} while T falls by only {(t1 + 273) / (t2 + 273):.2f}; fewer collisions per unit area outside allow expansion – pressure dominates (R1).', 5, 'multi_step')
    d = rng.choice([10, 20, 30, 40])
    V1 = rng.choice([1.0, 2.0, 3.0, 4.0])
    p_d = 100 + d * 10.1
    V2 = V1 * p_d / 100
    stem = (f'A diver at a depth of {d} m (pressure {sf(p_d)} kPa) fills her lungs with {V1:.1f} dm³ of air and then rises to the surface (100 kPa) without exhaling. Assume constant temperature. '
            f'(a) Calculate the volume the air would occupy at the surface. (b) Explain, using kinetic theory, why the volume increases. (c) Comment on why divers are trained to exhale while ascending.')
    return num(stem, f'(a) {q(V2, "dm³")}', f'(a) p₁V₁ = p₂V₂ (M1); V₂ = {sf(p_d)} × {V1:.1f}/100 = {q(V2, "dm³")} (A1). (b) Lower external pressure; gas particles collide with the walls; volume increases until internal pressure equals external pressure (R1 R1). (c) The air would expand to many times the lung volume, risking lung damage (R1).', 5, 'multi_step')


R.mcqs('ch04-st2', 'C2', (1, 4), [
    ('The absolute temperature of a fixed mass of gas is doubled and its pressure is halved. What happens to the volume?', 'It increases by a factor of four.', ['It doubles.', 'It stays the same.', 'It halves.'], 'V ∝ T/p: 2 × 2 = 4.'),
    ('Which graph gives a straight line through the origin for a fixed mass of gas at constant temperature?', 'p against 1/V', ['p against V', 'V against T in °C', 'pV against p'], 'Boyle: p = k/V.'),
    ('A student uses T = 25 instead of T = 298 in pV = nRT to calculate an amount of gas. What is the effect on the answer?', 'It is about 12 times too large.', ['It is about 12 times too small.', 'There is no effect.', 'It is 273 times too large.'], 'n = pV/RT: dividing by 25 instead of 298.'),
    ('A sealed flask of gas is heated from 300 K to 600 K. What happens to the pressure?', 'It doubles.', ['It halves.', 'It quadruples.', 'It stays the same.'], 'p ∝ T at constant V.'),
])


R.facts('ch04-st3', F(
    terms=[('molar mass of a volatile liquid (Dumas/syringe method)', 'a method in which a known mass of vapour occupies a measured volume at a known temperature and pressure, giving M = mRT/(pV)'),
           ('gas syringe', 'a graduated syringe used to measure volumes of gas, typically to ±0.5 cm³'),
           ('vapour pressure', 'the pressure exerted by a vapour in equilibrium with its liquid at a given temperature')],
    facts=[('Which expression gives the molar mass of a gas from experimental data?', 'M = mRT/(pV)', ['M = pV/(mRT)', 'M = mpV/(RT)', 'M = RT/(mpV)'], 'n = m/M = pV/RT.'),
           ('When a gas is collected over water, which correction must be made to the measured pressure?', 'subtract the vapour pressure of water at that temperature', ['add the vapour pressure of water', 'multiply by the density of water', 'no correction is needed'], 'p(gas) = p(atm) − p(H₂O).'),
           ('A 0.200 g sample of a gas occupies 0.112 dm³ at STP. What is its molar mass?', '40.5 g mol⁻¹', ['4.05 g mol⁻¹', '0.112 g mol⁻¹', '25.4 g mol⁻¹'], 'n = 0.112/22.7 = 4.93 × 10⁻³ mol; M = 0.200/4.93 × 10⁻³.')],
    why=[('Explain why a butane lighter should be dried thoroughly before re-weighing in an experiment to find the molar mass of butane collected over water.', 'Water absorbed on the lighter would add to its final mass, making the mass of butane released appear smaller and the calculated molar mass too low.'),
         ('Explain why the molar mass determined by collecting a gas over water may be too low if the water vapour is ignored.', 'The gas collected is saturated with water vapour, so the partial pressure of the gas is less than atmospheric pressure; using atmospheric pressure overestimates n and underestimates M.'),
         ('Explain why gases with strong intermolecular forces give less accurate molar masses using pV = nRT.', 'They deviate from ideal behaviour; attractions reduce the pressure/volume compared with the ideal value, so the ideal gas equation gives an inaccurate amount.')],
    misc=[('In the gas syringe experiment, the temperature can be used in °C because only a ratio is needed.', 'pV = nRT requires absolute temperature in kelvin.')],
    evaluate=[('Determining molar mass from gas measurements is less useful today than mass spectrometry.', ['mass spectrometry gives Mr precisely and needs tiny samples', 'gives structural information too'], ['gas methods are cheap and illustrate the gas laws', 'useful in teaching labs and field work', 'accuracy acceptable for identifying simple gases'], 'Mass spectrometry is superior for precise identification, but gas-law methods remain valuable for education and quick estimates.')],
))


@R.add('ch04-st3', 'C3', (1, 5), 'numerical')
def c3_molar_mass_gas(rng, slot):
    gas, f = pick(rng, [('butane', 'C4H10'), ('propane', 'C3H8'), ('carbon dioxide', 'CO2'), ('an unknown hydrocarbon', 'C2H6'), ('a refrigerant gas', 'CH2F2'), ('a volatile liquid vapour', 'C3H6O'), ('a noble gas', 'Ar'), ('an unknown gas', 'SO2'), ('an anaesthetic vapour', 'C2H5OC2H5'.replace('C2H5OC2H5', 'C4H10O'))])
    M = mr(f)
    T = rng.choice([293, 295, 298, 300, 373, 353])
    p = rng.choice([100.0, 101.3, 99.5, 102.0, 98.7])
    V = rng.choice([50.0, 75.0, 100.0, 120.0, 150.0, 200.0, 250.0])  # cm3
    n = p * 1000 * V * 1e-6 / (RGAS * T)
    m = round(n * M * rng.uniform(0.985, 1.015), 3)
    Mexp = m * RGAS * T / (p * 1000 * V * 1e-6)
    ctx = pick(rng, [f'A gas syringe was filled with {gas}.', f'A sample of {gas} was injected into an evacuated bulb.', f'{gas[0].upper() + gas[1:]} was released from a pressurised can into an inverted measuring cylinder.'])
    stem = f'{ctx} A mass of {m:.3f} g of the gas occupied {V:.1f} cm³ at {T} K and {p} kPa. Calculate the molar mass of the gas.'
    if slot.d >= 4:
        stem += ' Suggest its identity from the formulae ' + ', '.join(chem(x) for x in rng.sample(['C4H10', 'C3H8', 'CO2', 'C2H6', 'CH2F2', 'C3H6O', 'Ar', 'SO2', 'C4H10O', 'CH4', 'N2'], 3) + [f]) + '.'
        return num(stem, f'{q(Mexp, "g mol⁻¹")} ({chem(f)}, M = {M:.2f})', f'n = pV/RT = {p} × 10³ × {V} × 10⁻⁶/(8.31 × {T}) = {sf(n)} mol (M1); M = m/n (M1) = {q(Mexp, "g mol⁻¹")} (A1); closest to {chem(f)} (A1).', 4, 'multi_step')
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Calculate the molar mass', 'What is the molar mass'), Mexp, [Mexp * 1000, Mexp / 1000, m * RGAS * (T - 273 if T > 273 else T) / (p * V * 1e-3)], 'g mol⁻¹', f'M = mRT/pV = {m:.3f} × 8.31 × {T}/({p} × 10³ × {V} × 10⁻⁶) = {sf(Mexp)} g mol⁻¹.')
    return num(stem, q(Mexp, 'g mol⁻¹'), f'n = pV/RT (M1); unit conversions to Pa and m³ (M1); M = {q(Mexp, "g mol⁻¹")} (A1).', 3)


@p1b(R, 'ch04-st3')
def p1b_lighter(rng, slot):
    m1 = round(rng.uniform(15, 22), 2)
    T = rng.choice([293, 294, 295, 296, 297])
    pv = {293: 2.34, 294: 2.49, 295: 2.64, 296: 2.81, 297: 2.98}[T]
    patm = round(rng.uniform(99.5, 102.5), 1)
    V = rng.choice([80.0, 90.0, 100.0, 110.0, 120.0])
    pg = patm - pv
    n = pg * 1000 * V * 1e-6 / (RGAS * T)
    dm = round(n * 58.14 * rng.uniform(1.0, 1.04), 2)
    m2 = round(m1 - dm, 2)
    M = dm / n
    Mn = dm * RGAS * T / (patm * 1000 * V * 1e-6)
    err = abs(M - 58.14) / 58.14 * 100
    intro = (f'A student released butane gas from a lighter into an inverted measuring cylinder filled with water, collecting {V:.1f} cm³ of gas. '
             f'The room temperature was {T} K and atmospheric pressure {patm} kPa. The vapour pressure of water at {T} K is {pv} kPa.\n\n'
             f'mass of lighter before / g ± 0.01 | {m1:.2f}\nmass of lighter after (dried) / g ± 0.01 | {m2:.2f}')
    return dict(intro=intro, parts=[
        ('Calculate the partial pressure of butane in the cylinder.', f'{pg:.2f} kPa', f'{patm} − {pv} = {pg:.2f} kPa (A1).', 1),
        ('Calculate the amount of butane collected.', q(n, 'mol'), f'n = pV/RT = {pg:.2f} × 10³ × {V} × 10⁻⁶/(8.31 × {T}) (M1) = {q(n, "mol")} (A1).', 2),
        ('Determine the experimental molar mass of butane and its percentage error compared with 58.14 g mol⁻¹.', f'{q(M, "g mol⁻¹")}; {err:.1f} %', f'M = {dm:.2f}/{sf(n)} = {q(M, "g mol⁻¹")} (A1); % error = {err:.1f} % (A1).', 2),
        ('Calculate the percentage uncertainty in the mass of butane released.', f'{0.02 / dm * 100:.1f} %', f'±0.02 g on {dm:.2f} g (M1) = {0.02 / dm * 100:.1f} % (A1).', 2)],
        extras=[(f'Explain why ignoring the vapour pressure of water would give a lower molar mass ({q(Mn, "g mol⁻¹")}).', 'Using the total pressure overestimates the partial pressure and therefore the amount of butane; M = m/n is then too small.', 'p too high → n too high → M too low (1).', 1),
                ('Suggest why the lighter must be dried before re-weighing.', 'Water clinging to the lighter would make the final mass too high and the mass of butane too low.', 'Water adds mass (1).', 1)])


R.mcqs('ch04-st3', 'C2', (1, 4), [
    ('In a gas syringe experiment, the plunger sticks slightly so the volume reading is too small. What is the effect on the calculated molar mass?', 'It will be too high.', ['It will be too low.', 'No effect.', 'It cannot be determined.'], 'M = mRT/pV: smaller V gives larger M.'),
    ('Why is the temperature of the water bath measured in a Dumas experiment?', 'The vapour temperature is needed in kelvin for pV = nRT.', ['To check the water is boiling.', 'To find the density of the vapour.', 'To calculate the mass of the flask.'], 'T is a variable in the equation.'),
    ('Some of a volatile liquid fails to vaporise in a Dumas flask but is weighed as vapour. What is the effect on the calculated molar mass?', 'too high', ['too low', 'no effect', 'it becomes negative'], 'Extra mass attributed to the same volume.'),
])

GAS_ERRORS = [('the gas was collected over water and the vapour pressure of water was ignored', 'too low', 'p(gas) is overestimated, so n = pV/RT is too large and M = m/n too small'),
              ('the room temperature used in the calculation was 5 K lower than the true temperature', 'too low', 'M = mRT/pV is proportional to T, so a low T gives a low M'),
              ('some gas escaped before the volume was read', 'too high', 'the mass loss includes gas not counted in V, so m/V is too large'),
              ('the lighter was not dried before re-weighing', 'too low', 'retained water makes the final mass too high, so the mass of gas is underestimated'),
              ('air bubbles remained in the measuring cylinder at the start', 'too low', 'the measured volume includes air, so n is overestimated'),
              ('some vapour condensed in the syringe needle before the volume was read', 'too high', 'the measured volume of vapour is too small for the mass recorded'),
              ('the atmospheric pressure was taken as 101.3 kPa when it was actually 97.0 kPa', 'too low', 'p is overestimated; n is too large and M too small'),
              ('the gas being studied is polar and has significant intermolecular attractions', 'too high', 'attractions make the real volume smaller than the ideal value, so pV/RT underestimates n and M = m/n is too high')]


@R.add('ch04-st3', 'C2', (2, 4), 'explain')
def c2_gas_error(rng, slot):
    err, eff, why = pick(rng, GAS_ERRORS)
    exp = pick(rng, ['an experiment to find the molar mass of butane from a lighter', 'a gas-syringe determination of the molar mass of a volatile liquid', 'an investigation to determine the molar mass of an unknown gas'])
    stem = pick(rng, [f'In {exp}, {err}. Predict and explain the effect on the calculated molar mass.',
                      f'During {exp}, {err}. State whether the calculated molar mass will be too high or too low, giving a reason.'])
    return dict(stem=stem, answer=f'{eff[0].upper() + eff[1:]}: {why}.', markingKey=f'{eff} (1); reasoning via M = mRT/pV: {why} (1).', type='explain', marks=2, gap='G7')


@R.add('ch04-st3', 'C2', (1, 4), 'mcq')
def c2_gas_error_mcq(rng, slot):
    err, eff, why = pick(rng, GAS_ERRORS)
    other = 'too high' if eff == 'too low' else 'too low'
    stem = f'In an experiment to determine the molar mass of a gas using M = mRT/(pV), {err}. What is the effect on the calculated molar mass?'
    return mcq(rng, stem, f'It will be {eff}.', [f'It will be {other}.', 'There will be no effect.', 'The effect cannot be predicted from the equation.'], why[0].upper() + why[1:] + '.')


# =============================================================================================
# ch05 R2.1 How much? The amount of chemical change
# =============================================================================================
# (equation text, {species: coefficient}, reactant list, product list, context)
RXNS = [
    ('2Mg(s) + O2(g) → 2MgO(s)', {'Mg': 2, 'O2': 1, 'MgO': 2}, ['Mg', 'O2'], ['MgO'], 'burning magnesium ribbon'),
    ('CaCO3(s) → CaO(s) + CO2(g)', {'CaCO3': 1, 'CaO': 1, 'CO2': 1}, ['CaCO3'], ['CaO', 'CO2'], 'the thermal decomposition of limestone in a lime kiln'),
    ('Fe2O3(s) + 3CO(g) → 2Fe(l) + 3CO2(g)', {'Fe2O3': 1, 'CO': 3, 'Fe': 2, 'CO2': 3}, ['Fe2O3', 'CO'], ['Fe', 'CO2'], 'the reduction of haematite in a blast furnace'),
    ('N2(g) + 3H2(g) → 2NH3(g)', {'N2': 1, 'H2': 3, 'NH3': 2}, ['N2', 'H2'], ['NH3'], 'the Haber process'),
    ('2Al(s) + Fe2O3(s) → Al2O3(s) + 2Fe(l)', {'Al': 2, 'Fe2O3': 1, 'Al2O3': 1, 'Fe': 2}, ['Al', 'Fe2O3'], ['Al2O3', 'Fe'], 'the thermite reaction used to weld railway lines'),
    ('C6H12O6(aq) → 2C2H5OH(aq) + 2CO2(g)', {'C6H12O6': 1, 'C2H5OH': 2, 'CO2': 2}, ['C6H12O6'], ['C2H5OH', 'CO2'], 'the fermentation of glucose'),
    ('CH4(g) + 2O2(g) → CO2(g) + 2H2O(l)', {'CH4': 1, 'O2': 2, 'CO2': 1, 'H2O': 2}, ['CH4', 'O2'], ['CO2', 'H2O'], 'the combustion of natural gas'),
    ('2NaHCO3(s) → Na2CO3(s) + H2O(g) + CO2(g)', {'NaHCO3': 2, 'Na2CO3': 1, 'H2O': 1, 'CO2': 1}, ['NaHCO3'], ['Na2CO3', 'H2O', 'CO2'], 'heating baking soda'),
    ('Zn(s) + CuSO4(aq) → ZnSO4(aq) + Cu(s)', {'Zn': 1, 'CuSO4': 1, 'ZnSO4': 1, 'Cu': 1}, ['Zn', 'CuSO4'], ['ZnSO4', 'Cu'], 'the displacement of copper by zinc'),
    ('2H2O2(aq) → 2H2O(l) + O2(g)', {'H2O2': 2, 'H2O': 2, 'O2': 1}, ['H2O2'], ['H2O', 'O2'], 'the catalytic decomposition of hydrogen peroxide'),
    ('C3H8(g) + 5O2(g) → 3CO2(g) + 4H2O(l)', {'C3H8': 1, 'O2': 5, 'CO2': 3, 'H2O': 4}, ['C3H8', 'O2'], ['CO2', 'H2O'], 'burning propane in a camping stove'),
    ('TiCl4(g) + 2Mg(l) → Ti(s) + 2MgCl2(l)', {'TiCl4': 1, 'Mg': 2, 'Ti': 1, 'MgCl2': 2}, ['TiCl4', 'Mg'], ['Ti', 'MgCl2'], 'the Kroll process for titanium'),
    ('2Al2O3(l) → 4Al(l) + 3O2(g)', {'Al2O3': 2, 'Al': 4, 'O2': 3}, ['Al2O3'], ['Al', 'O2'], 'the electrolysis of molten alumina'),
    ('CaCO3(s) + 2HCl(aq) → CaCl2(aq) + H2O(l) + CO2(g)', {'CaCO3': 1, 'HCl': 2, 'CaCl2': 1, 'H2O': 1, 'CO2': 1}, ['CaCO3', 'HCl'], ['CaCl2', 'H2O', 'CO2'], 'marble chips reacting with hydrochloric acid'),
    ('4NH3(g) + 5O2(g) → 4NO(g) + 6H2O(g)', {'NH3': 4, 'O2': 5, 'NO': 4, 'H2O': 6}, ['NH3', 'O2'], ['NO', 'H2O'], 'the catalytic oxidation of ammonia (Ostwald process)'),
    ('2SO2(g) + O2(g) → 2SO3(g)', {'SO2': 2, 'O2': 1, 'SO3': 2}, ['SO2', 'O2'], ['SO3'], 'the Contact process'),
    ('Cu2O(s) + C(s) → 2Cu(s) + CO(g)', {'Cu2O': 1, 'C': 1, 'Cu': 2, 'CO': 1}, ['Cu2O', 'C'], ['Cu', 'CO'], 'smelting copper(I) oxide with carbon'),
    ('2KClO3(s) → 2KCl(s) + 3O2(g)', {'KClO3': 2, 'KCl': 2, 'O2': 3}, ['KClO3'], ['KCl', 'O2'], 'the decomposition of potassium chlorate'),
    ('C2H5OH(l) + 3O2(g) → 2CO2(g) + 3H2O(l)', {'C2H5OH': 1, 'O2': 3, 'CO2': 2, 'H2O': 3}, ['C2H5OH', 'O2'], ['CO2', 'H2O'], 'the combustion of bioethanol'),
    ('Mg(s) + 2HCl(aq) → MgCl2(aq) + H2(g)', {'Mg': 1, 'HCl': 2, 'MgCl2': 1, 'H2': 1}, ['Mg', 'HCl'], ['MgCl2', 'H2'], 'magnesium reacting with hydrochloric acid'),
]
SOLIDS = {'Mg', 'MgO', 'CaCO3', 'CaO', 'Fe2O3', 'Fe', 'Al', 'Al2O3', 'C6H12O6', 'NaHCO3', 'Na2CO3', 'Zn', 'CuSO4', 'Cu', 'Ti', 'Cu2O', 'C', 'KClO3', 'KCl', 'MgCl2', 'TiCl4', 'H2O2', 'C2H5OH', 'ZnSO4', 'CaCl2'}

R.facts('ch05-st1', F(
    terms=[('stoichiometry', 'the quantitative relationship between the amounts of reactants and products in a chemical reaction, given by the coefficients of the balanced equation'),
           ('mole ratio', 'the ratio of the amounts of any two species in a reaction, taken from the coefficients in the balanced equation'),
           ('law of conservation of mass', 'in a chemical reaction the total mass of the products equals the total mass of the reactants, as atoms are neither created nor destroyed'),
           ('state symbols', 'the symbols (s), (l), (g) and (aq) written after formulae to show physical state')],
    facts=[('What is the coefficient of O₂ when the equation C₄H₁₀ + O₂ → CO₂ + H₂O is balanced with whole numbers?', '13', ['6.5', '9', '4'], '2C₄H₁₀ + 13O₂ → 8CO₂ + 10H₂O.'),
           ('In 2H₂ + O₂ → 2H₂O, what amount of water forms from 3.0 mol of H₂ with excess O₂?', '3.0 mol', ['1.5 mol', '6.0 mol', '2.0 mol'], 'H₂ : H₂O = 1 : 1.'),
           ('Which is conserved in all chemical reactions?', 'the total number of atoms of each element', ['the total number of molecules', 'the total volume', 'the total amount in moles'], 'Atoms are rearranged, not created or destroyed.'),
           ('What does the state symbol (aq) mean?', 'dissolved in water', ['a liquid', 'an acid', 'a solid suspended in water'], 'Aqueous solution.')],
    why=[('Explain why the coefficients in a balanced equation give mole ratios but not mass ratios.', 'Coefficients count particles (and so moles); different substances have different molar masses, so equal numbers of moles have different masses.'),
         ('Explain why the mass of a crucible containing magnesium increases when the magnesium is burned.', 'Magnesium combines with oxygen from the air; the product MgO includes the mass of the oxygen atoms added, so mass increases while total mass (including O₂ used) is conserved.'),
         ('Explain why the mass of a flask containing marble chips and hydrochloric acid decreases during the reaction.', 'Carbon dioxide gas is produced and escapes from the open flask; total mass is conserved if the gas is included.')],
    misc=[('In 2Mg + O₂ → 2MgO, 2 g of magnesium reacts with 1 g of oxygen.', 'The coefficients are mole ratios: 2 mol Mg (48.62 g) react with 1 mol O₂ (32.00 g).'),
          ('A balanced equation can be balanced by changing the subscripts in the formulae.', 'Subscripts define the substance; only coefficients may be changed when balancing.')],
    evaluate=[('Stoichiometric calculations based on balanced equations give the mass of product that will actually be obtained.', ['give the theoretical maximum quantity', 'essential for planning industrial processes'], ['side reactions, incomplete reactions and losses in separation reduce the real yield', 'reversible reactions reach equilibrium'], 'They give the theoretical yield; real yields are lower and must be measured.')],
))


def eqp(eq):
    return chem(eq)


@R.add('ch05-st1', 'C3', (1, 5), 'numerical')
def c3_react_mass(rng, slot):
    eq, co, rs, ps, ctx = pick(rng, RXNS)
    a = pick(rng, rs)
    b = pick(rng, [s for s in co if s != a])
    ma = float(f'{rng.uniform(1, 500) if slot.d >= 3 else rng.uniform(1, 50):.3g}')
    unit_a, scale = ('kg', 1000) if slot.d >= 4 and rng.random() < 0.5 else ('g', 1)
    na = ma * scale / mr(a)
    nb = na * co[b] / co[a]
    mb = nb * mr(b) / scale
    stem = pick(rng, [f'In {ctx}, {eqp(eq)}. Calculate the mass of {chem(b)} that {"forms from" if b not in rs else "reacts with"} {sf(ma)} {unit_a} of {chem(a)}.',
                      f'Consider the reaction {eqp(eq)} ({ctx}). Determine the mass of {chem(b)} {"produced" if b not in rs else "required"} when {sf(ma)} {unit_a} of {chem(a)} reacts completely.'])
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Calculate the mass', 'What mass').replace('Determine the mass', 'What mass'), mb, [na * mr(b) / scale, na * co[a] / co[b] * mr(b) / scale, ma * co[b] / co[a]], unit_a,
                    f'n({chem(a)}) = {sf(ma)}/{mr(a):.2f} = {sf(na)} mol; × {co[b]}/{co[a]} = {sf(nb)} mol {chem(b)}; × {mr(b):.2f} = {q(mb, unit_a)}.')
    return num(stem, q(mb, unit_a), f'n({chem(a)}) = {sf(ma)}{" × 10³" if scale > 1 else ""}/{mr(a):.2f} = {sf(na)} mol (M1); n({chem(b)}) = {sf(na)} × {co[b]}/{co[a]} = {sf(nb)} mol (M1); m = {q(mb, unit_a)} (A1).', 3)


ALKANES = [('methane', 1), ('ethane', 2), ('propane', 3), ('butane', 4), ('pentane', 5), ('hexane', 6), ('heptane', 7), ('octane', 8), ('nonane', 9), ('decane', 10)]
ALCOHOLS = [('methanol', 1), ('ethanol', 2), ('propan-1-ol', 3), ('butan-1-ol', 4), ('pentan-1-ol', 5), ('hexan-1-ol', 6)]


def combustion(nC, nH, nO=0, co_=False):
    """Balanced whole-number coefficients for CxHyOz + O2 → CO2 (or CO) + H2O."""
    o_needed2 = (2 * nC if not co_ else nC) + nH / 2 - nO  # O atoms needed (as O2 = /2)
    fr = Fraction(o_needed2).limit_denominator() / 2
    k = fr.denominator
    k = k * (2 if (nH * k) % 2 else 1)
    fr = Fraction(o_needed2) / 2
    k = 1
    while not ((fr * k).denominator == 1 and (Fraction(nH, 2) * k).denominator == 1):
        k += 1
    return k, int(fr * k), nC * k, int(Fraction(nH, 2) * k)


def fuel_formula(nC, alc=False):
    h = 2 * nC + 2
    if alc:
        return f'C{nC if nC > 1 else ""}H{h - 1}OH' if nC > 1 else 'CH3OH', nC, h, 1
    return f'C{nC if nC > 1 else ""}H{h}', nC, h, 0


@R.add('ch05-st1', 'C3', (1, 4), 'mcq')
def c3_balance(rng, slot):
    if rng.random() < 0.5:
        nm, n = pick(rng, ALKANES)
        f, c, h, o = fuel_formula(n)
    else:
        nm, n = pick(rng, ALCOHOLS)
        f, c, h, o = fuel_formula(n, True)
    k, o2, co2, h2o = combustion(c, h, o)
    stem = f'The equation for the complete combustion of {nm} is balanced using the smallest whole numbers: __{chem(f)} + __O₂ → __CO₂ + __H₂O. What is the coefficient of O₂?'
    wr = [o2 + 1, o2 - 1 if o2 > 2 else o2 + 2, co2 + h2o, (2 * c + h // 2) if (2 * c + h // 2) != o2 else o2 + 3]
    wr = [str(w) for w in wr if w != o2 and w > 0]
    return mcq(rng, stem, str(o2), list(dict.fromkeys(wr))[:3], f'{k}{chem(f)} + {o2}O₂ → {co2}CO₂ + {h2o}H₂O; check O: {2 * o2 + 0} on the left (+{k * o} in fuel) = {2 * co2 + h2o} on the right.')


@R.add('ch05-st1', 'C1', (1, 3), 'short')
def c1_balance_eq(rng, slot):
    nm, n = pick(rng, ALKANES + ALCOHOLS)
    alc = (nm, n) in ALCOHOLS
    f, c, h, o = fuel_formula(n, alc)
    k, o2, co2, h2o = combustion(c, h, o)
    s = f'{"" if k == 1 else k}{chem(f)}(' + ('l' if (alc or n >= 5) else 'g') + f') + {o2}O₂(g) → {co2}CO₂(g) + {h2o}H₂O(l)'
    return dict(stem=f'Write a balanced equation, with state symbols, for the complete combustion of {nm}.', answer=s, markingKey=f'Correct formulae (1); balanced: {s} (1); state symbols not required for the balancing mark.', type='short', marks=2)


@R.add('ch05-st1', 'C4', (3, 5), 'multi_step')
def c4_industrial(rng, slot):
    eq, co, rs, ps, ctx = pick(rng, [r for r in RXNS if len(r[3]) >= 1 and r[4] in ('the reduction of haematite in a blast furnace', 'the thermite reaction used to weld railway lines', 'the Kroll process for titanium', 'the electrolysis of molten alumina', 'the thermal decomposition of limestone in a lime kiln', 'the Haber process', 'the Contact process')])
    prod = {'Fe2O3': 'Fe', 'Al': 'Fe', 'TiCl4': 'Ti', 'Al2O3': 'Al', 'CaCO3': 'CaO', 'N2': 'NH3', 'SO2': 'SO3'}[rs[0]]
    target = rng.choice([1.00, 2.50, 5.00, 10.0, 50.0, 100])  # tonnes
    ra = rs[0]
    n_p = target * 1e6 / mr(prod)
    n_r = n_p * co[ra] / co[prod]
    m_r = n_r * mr(ra) / 1e6
    by = [p for p in ps if p != prod]
    extra = ''
    key_extra = ''
    if by:
        b = by[0]
        m_b = n_p * co[b] / co[prod] * mr(b) / 1e6
        extra = f' (b) Calculate the mass of {chem(b)} formed at the same time.'
        key_extra = f' (b) n({chem(b)}) = {sf(n_p * co[b] / co[prod])} mol; mass = {q(m_b, "tonnes")} (A1).'
    stem = (f'In {ctx}, {eqp(eq)}. A plant needs to produce {sf(target)} tonnes of {chem(prod)} per day. (a) Calculate the minimum mass of {chem(ra)} needed per day, in tonnes (1 tonne = 10⁶ g).' + extra +
            ' (c) Suggest one reason why more than this mass is used in practice.')
    return num(stem, f'(a) {q(m_r, "tonnes")}', f'(a) n({chem(prod)}) = {sf(target)} × 10⁶/{mr(prod):.2f} = {sf(n_p)} mol (M1); n({chem(ra)}) = × {co[ra]}/{co[prod]} = {sf(n_r)} mol (M1); m = {q(m_r, "tonnes")} (A1).' + key_extra + ' (c) incomplete reaction/side reactions/impure raw materials/losses (R1).', 5, 'multi_step')


R.mcqs('ch05-st1', 'C2', (1, 4), [
    ('Iron(III) oxide is reduced: Fe₂O₃ + 3CO → 2Fe + 3CO₂. What amount of CO is needed to produce 1.0 mol of Fe?', '1.5 mol', ['3.0 mol', '0.67 mol', '2.0 mol'], 'CO : Fe = 3 : 2.'),
    ('What mass of oxygen reacts with 12.01 g of carbon to form carbon dioxide?', '32.00 g', ['16.00 g', '12.01 g', '44.01 g'], '1 mol C reacts with 1 mol O₂.'),
    ('When 10 g of calcium carbonate is heated, 5.6 g of calcium oxide remains. What mass of carbon dioxide was released?', '4.4 g', ['5.6 g', '10 g', '15.6 g'], 'Conservation of mass.'),
    ('Which equation is correctly balanced?', '2Al + 3Cl₂ → 2AlCl₃', ['Al + Cl₂ → AlCl₃', '2Al + 2Cl₂ → 2AlCl₃', 'Al + 3Cl → AlCl₃'], 'Atoms: 2 Al, 6 Cl each side.'),
])


R.facts('ch05-st2', F(
    terms=[('limiting reactant', 'the reactant that is completely used up first in a reaction and so determines the maximum amount of product'),
           ('excess reactant', 'a reactant present in more than the amount needed to react with the limiting reactant, so some remains at the end')],
    facts=[('2H₂ + O₂ → 2H₂O. 4 mol of H₂ is mixed with 3 mol of O₂. Which is limiting?', 'H₂', ['O₂', 'neither', 'H₂O'], '4 mol H₂ needs only 2 mol O₂.'),
           ('N₂ + 3H₂ → 2NH₃. 2.0 mol N₂ and 3.0 mol H₂ react completely. What amount of NH₃ forms?', '2.0 mol', ['4.0 mol', '6.0 mol', '1.0 mol'], 'H₂ limiting: 3.0 × 2/3.'),
           ('Why is one reactant often used in excess in industry?', 'to ensure the more expensive reactant reacts completely', ['to slow down the reaction', 'to reduce the yield', 'because balanced equations are not accurate'], 'Maximises conversion of the costly reactant.')],
    why=[('Explain why the limiting reactant cannot be identified simply by comparing the masses of the reactants.', 'Reactions occur in mole ratios; the masses must be converted to amounts and compared with the stoichiometric ratio in the balanced equation.'),
         ('Explain why the amount of product depends only on the limiting reactant.', 'Once the limiting reactant is used up the reaction stops; the excess reactant has nothing left to react with.')],
    misc=[('The reactant with the smaller mass is always the limiting reactant.', 'Compare amounts divided by their coefficients: a smaller mass of a low-M substance may be a larger amount.'),
          ('The reactant with the smaller amount in moles is always limiting.', 'The coefficients matter: compare n/coefficient for each reactant.')],
    evaluate=[('Using a large excess of one reactant is always good practice.', ['ensures complete conversion of the valuable reactant', 'may shift equilibria to the right'], ['wastes resources and lowers atom economy', 'excess must be separated and recycled or disposed of, adding cost and environmental impact'], 'A modest excess of the cheaper reactant is sensible; large excesses are wasteful and are minimised in green chemistry.')],
))


@R.add('ch05-st2', 'C3', (1, 5), 'numerical')
def c3_limiting(rng, slot):
    eq, co, rs, ps, ctx = pick(rng, [r for r in RXNS if len(r[2]) == 2])
    a, b = rs
    p = pick(rng, ps)
    na_ = rng.uniform(0.05, 2)
    ratio = rng.choice([0.5, 0.7, 1.4, 2.0, 0.8, 1.25])
    nb_ = na_ * co[b] / co[a] * ratio
    ma, mb = float(f'{na_ * mr(a):.3g}'), float(f'{nb_ * mr(b):.3g}')
    na_, nb_ = ma / mr(a), mb / mr(b)
    lim = a if na_ / co[a] < nb_ / co[b] else b
    exc = b if lim == a else a
    nlim = na_ if lim == a else nb_
    npr = nlim * co[p] / co[lim]
    mp = npr * mr(p)
    nexc_left = (nb_ if exc == b else na_) - nlim * co[exc] / co[lim]
    stem = f'{sf(ma)} g of {chem(a)} is mixed with {sf(mb)} g of {chem(b)}: {eqp(eq)}. '
    if slot.d <= 2:
        return mcq(rng, stem + 'Which reactant is limiting, and what amount of ' + chem(p) + ' can form?',
                   f'{chem(lim)}; {sf(npr)} mol', [f'{chem(exc)}; {sf(npr)} mol', f'{chem(exc)}; {sf((nb_ if exc == b else na_) * co[p] / co[exc])} mol', f'{chem(lim)}; {sf(nlim)} mol' if co[p] != co[lim] else f'{chem(lim)}; {sf(npr * 2)} mol'],
                   f'n/coefficient: {chem(a)} {sf(na_ / co[a])}, {chem(b)} {sf(nb_ / co[b])} → {chem(lim)} limiting; n({chem(p)}) = {sf(npr)} mol.')
    if slot.d == 3:
        stem += f'Determine the limiting reactant and the maximum mass of {chem(p)} that can form.'
        return num(stem, f'{chem(lim)} limiting; {q(mp, "g")}', f'n({chem(a)}) = {sf(na_)} mol, n({chem(b)}) = {sf(nb_)} mol (M1); compare with {co[a]} : {co[b]} → {chem(lim)} limiting (A1); n({chem(p)}) = {sf(npr)} mol, m = {q(mp, "g")} (A1).', 3)
    stem += f'(a) Identify the limiting reactant. (b) Calculate the maximum mass of {chem(p)}. (c) Calculate the mass of the excess reactant left unreacted.'
    return num(stem, f'(a) {chem(lim)}; (b) {q(mp, "g")}; (c) {q(nexc_left * mr(exc), "g")} of {chem(exc)}', f'(a) amounts {sf(na_)} and {sf(nb_)} mol; {chem(lim)} limiting (M1 A1). (b) {q(mp, "g")} (A1). (c) {chem(exc)} used = {sf(nlim * co[exc] / co[lim])} mol; left = {sf(nexc_left)} mol = {q(nexc_left * mr(exc), "g")} (M1 A1).', 5, 'multi_step')


@R.add('ch05-st2', 'C2', (2, 4), 'explain')
def c2_limiting_explain(rng, slot):
    eq, co, rs, ps, ctx = pick(rng, [r for r in RXNS if len(r[2]) == 2])
    a, b = rs
    m = rng.choice([10.0, 20.0, 50.0, 100])
    na, nb = m / mr(a), m / mr(b)
    lim = a if na / co[a] < nb / co[b] else b
    stem = f'Equal masses ({m:g} g each) of {chem(a)} and {chem(b)} are mixed for {ctx}: {eqp(eq)}. Explain which reactant is limiting.'
    return dict(stem=stem, answer=f'{chem(lim)}: n/coefficient is {sf(na / co[a])} for {chem(a)} and {sf(nb / co[b])} for {chem(b)}.', markingKey=f'Converts masses to amounts ({sf(na)} and {sf(nb)} mol) (1); compares with mole ratio {co[a]} : {co[b]} (1); {chem(lim)} limiting (1).', type='explain', marks=3)


R.mcqs('ch05-st2', 'C2', (1, 4), [
    ('Zn + 2HCl → ZnCl₂ + H₂. 0.10 mol Zn is added to 0.10 mol HCl. Which statement is correct?', 'HCl is limiting and 0.050 mol H₂ forms.', ['Zn is limiting and 0.10 mol H₂ forms.', 'Neither is in excess.', 'HCl is limiting and 0.10 mol H₂ forms.'], '0.10 mol HCl reacts with 0.050 mol Zn.'),
    ('CH₄ + 2O₂ → CO₂ + 2H₂O. 1.0 mol CH₄ is burned in 1.0 mol O₂. Which remains at the end?', '0.50 mol CH₄', ['0.50 mol O₂', '1.0 mol CH₄', 'nothing'], 'O₂ limiting; it uses 0.50 mol CH₄.'),
    ('In a precipitation, adding more of reactant A no longer increases the mass of precipitate. This shows that', 'the other reactant has become limiting', ['A is the limiting reactant', 'the reaction is reversible', 'the precipitate is dissolving'], 'Product is set by the limiting reactant.'),
])


R.facts('ch05-st3', F(
    terms=[('theoretical yield', 'the maximum mass (or amount) of product that can be obtained from the limiting reactant, calculated from the balanced equation'),
           ('experimental yield', 'the actual mass (or amount) of product obtained in an experiment'),
           ('percentage yield', 'experimental yield ÷ theoretical yield × 100'),
           ('atom economy', 'the mass of the desired product divided by the total mass of all reactants (or products) in the balanced equation, × 100')],
    facts=[('Which type of reaction always has an atom economy of 100 %?', 'an addition reaction with a single product', ['a substitution reaction', 'a neutralisation reaction', 'a decomposition reaction'], 'All reactant atoms end up in the one product.'),
           ('A reaction has a theoretical yield of 20.0 g and an experimental yield of 15.0 g. What is the percentage yield?', '75.0 %', ['133 %', '25.0 %', '5.0 %'], '15.0/20.0 × 100.'),
           ('Which is NOT a reason for a percentage yield below 100 %?', 'using excess of one reactant', ['side reactions', 'loss of product during purification', 'the reaction reaching equilibrium'], 'Excess reactant does not lower yield from the limiting reactant.')],
    why=[('Explain why a reaction with a high percentage yield can still have a low atom economy.', 'Percentage yield compares product obtained with the maximum possible from that reaction; atom economy depends on the equation itself – if large amounts of by-products form, much of the reactant mass is wasted even at 100 % yield.'),
         ('Explain why chemists in industry aim for a high atom economy.', 'Less waste is produced, fewer raw materials are needed per kg of product, costs and environmental impact are lower – a principle of green chemistry.'),
         ('Explain why a percentage yield above 100 % indicates an experimental problem.', 'The product cannot exceed the theoretical maximum; an apparent yield above 100 % usually means the product is impure or wet (e.g. contains solvent or water).')],
    contrast=[('percentage yield', 'atom economy', 'Percentage yield measures how efficiently a reaction was carried out (actual/theoretical); atom economy measures how much of the reactant mass ends up in the desired product according to the equation.')],
    misc=[('A reaction with 100 % yield must have 100 % atom economy.', 'Yield and atom economy are independent: a substitution reaction can give 100 % yield but still produce by-products, so its atom economy is below 100 %.')],
    evaluate=[('Atom economy is a better measure of the sustainability of a process than percentage yield.', ['it highlights waste built into the chemistry', 'encourages addition reactions and catalytic routes'], ['ignores yield, energy use, solvents and toxicity of reagents', 'by-products may be useful and sold', 'a full life-cycle analysis is needed'], 'Atom economy is one useful indicator, but sustainability requires yield, energy, waste, hazards and by-product use to be considered together.')],
))

AE_RXNS = [('the production of hydrogen by steam reforming', 'CH4 + H2O → CO + 3H2', {'CH4': 1, 'H2O': 1}, ('H2', 3)),
           ('the extraction of iron', 'Fe2O3 + 3CO → 2Fe + 3CO2', {'Fe2O3': 1, 'CO': 3}, ('Fe', 2)),
           ('the hydration of ethene to make ethanol', 'C2H4 + H2O → C2H5OH', {'C2H4': 1, 'H2O': 1}, ('C2H5OH', 1)),
           ('making ethanol by fermentation', 'C6H12O6 → 2C2H5OH + 2CO2', {'C6H12O6': 1}, ('C2H5OH', 2)),
           ('the production of lime', 'CaCO3 → CaO + CO2', {'CaCO3': 1}, ('CaO', 1)),
           ('the Haber process', 'N2 + 3H2 → 2NH3', {'N2': 1, 'H2': 3}, ('NH3', 2)),
           ('making chloromethane from methane', 'CH4 + Cl2 → CH3Cl + HCl', {'CH4': 1, 'Cl2': 1}, ('CH3Cl', 1)),
           ('making titanium by the Kroll process', 'TiCl4 + 2Mg → Ti + 2MgCl2', {'TiCl4': 1, 'Mg': 2}, ('Ti', 1)),
           ('making aspirin from salicylic acid', 'C7H6O3 + C4H6O3 → C9H8O4 + C2H4O2', {'C7H6O3': 1, 'C4H6O3': 1}, ('C9H8O4', 1)),
           ('making copper(II) sulfate from copper(II) oxide', 'CuO + H2SO4 → CuSO4 + H2O', {'CuO': 1, 'H2SO4': 1}, ('CuSO4', 1)),
           ('making ethyl ethanoate by esterification', 'CH3COOH + C2H5OH → CH3COOC2H5 + H2O', {'CH3COOH': 1, 'C2H5OH': 1}, ('CH3COOC2H5', 1))]


@R.add('ch05-st3', 'C3', (1, 5), 'numerical')
def c3_ae(rng, slot):
    ctx, eq, re_, (p, k) = pick(rng, AE_RXNS)
    tot = sum(mr(f) * n for f, n in re_.items())
    ae = k * mr(p) / tot * 100
    stem = f'Calculate the atom economy for {ctx}: {chem(eq)}, where the desired product is {chem(p)}.'
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Calculate', 'What is'), ae, [mr(p) / tot * 100 if k > 1 else ae / 2, 100 - ae, k * mr(p) / mr(list(re_)[0]) * 100], '%', f'AE = {k} × {mr(p):.2f}/{tot:.2f} × 100 = {ae:.1f} %.', extra=True)
    return num(stem, f'{ae:.1f} %', f'M(desired) = {k} × {mr(p):.2f} = {k * mr(p):.2f} (M1); total reactants = {tot:.2f} (M1); AE = {ae:.1f} % (A1).', 3)


@R.add('ch05-st3', 'C3', (1, 5), 'numerical')
def c3_yield(rng, slot):
    eq, co, rs, ps, ctx = pick(rng, RXNS)
    a = rs[0]
    p = pick(rng, [x for x in ps if x in SOLIDS or x in ('NH3', 'SO3', 'Fe', 'Ti', 'Al', 'C2H5OH', 'Cu', 'CaO', 'MgO')] or ps)
    m = float(f'{rng.uniform(1, 80):.3g}')
    th = m / mr(a) * co[p] / co[a] * mr(p)
    pc = rng.uniform(55, 96)
    act = float(f'{th * pc / 100:.3g}')
    pc = act / th * 100
    who = name(rng)
    if slot.d <= 2:
        stem = f'In {ctx}, {who} obtains {sf(act)} g of {chem(p)}. The theoretical yield is {sf(th)} g. Calculate the percentage yield.'
        return num(stem, f'{pc:.1f} %', f'{sf(act)}/{sf(th)} × 100 (M1) = {pc:.1f} % (A1).', 2)
    stem = f'{who} carries out {ctx}: {eqp(eq)}. Starting with {sf(m)} g of {chem(a)} (limiting), {sf(act)} g of {chem(p)} is obtained. Calculate the theoretical yield and the percentage yield.'
    if slot.d >= 4:
        stem += ' Suggest two reasons why the yield is below 100 %.'
        return num(stem, f'{q(th, "g")}; {pc:.1f} %', f'n({chem(a)}) = {sf(m / mr(a))} mol (M1); theoretical m({chem(p)}) = {q(th, "g")} (A1); % yield = {pc:.1f} % (A1); two of: incomplete reaction, side reactions, loss on transfer/filtration/purification, reversible reaction (R1 R1).', 5, 'multi_step')
    return num(stem, f'{q(th, "g")}; {pc:.1f} %', f'n({chem(a)}) = {sf(m / mr(a))} mol (M1); theoretical yield {q(th, "g")} (A1); {pc:.1f} % (A1).', 3)


@R.add('ch05-st3', 'C4', (3, 5), 'multi_step')
def c4_routes(rng, slot):
    r1, r2 = rng.sample([r for r in AE_RXNS if r[3][0] in ('C2H5OH',)] + [r for r in AE_RXNS if r[3][0] == 'C2H5OH'], 2) if False else (AE_RXNS[2], AE_RXNS[3])
    y1, y2 = rng.choice([5, 8, 10, 15]), rng.choice([85, 90, 92, 95])
    ae1 = mr('C2H5OH') / (mr('C2H4') + mr('H2O')) * 100
    ae2 = 2 * mr('C2H5OH') / mr('C6H12O6') * 100
    stem = (f'Ethanol can be manufactured by (route 1) hydration of ethene, C₂H₄ + H₂O → C₂H₅OH, with a single-pass conversion of about {y1} % (unreacted ethene is recycled), '
            f'or (route 2) fermentation of glucose, C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂, with a yield of about {y2} %. '
            f'(a) Calculate the atom economy of each route. (b) Evaluate the two routes, considering atom economy, yield, raw materials and environmental impact.')
    return num(stem, f'(a) route 1 {ae1:.0f} %, route 2 {ae2:.1f} %; (b) balanced evaluation', f'(a) route 1 = 46.08/46.08 × 100 = {ae1:.0f} % (A1); route 2 = 2 × 46.08/180.18 × 100 = {ae2:.1f} % (M1 A1). (b) Route 1: 100 % AE, continuous, fast, but uses non-renewable crude-oil ethene, high T/p energy; low single-pass conversion offset by recycling (R1). Route 2: renewable feedstock, low temperature, but AE only {ae2:.0f} % (CO₂ by-product), batch, slow, needs distillation and land for crops (R1); justified conclusion (R1).', 6, 'multi_step')


R.mcqs('ch05-st3', 'C2', (1, 4), [
    ('Which change would increase the atom economy of a process?', 'finding a use for the by-product', ['increasing the temperature', 'using a catalyst', 'increasing the yield'], 'Counting a useful by-product as desired product raises the effective atom economy; yield and rate do not change the equation.'),
    ('A student obtains a percentage yield of 112 % for a recrystallised solid. What is the most likely reason?', 'The product was not completely dry.', ['The reaction went to completion.', 'Some product was lost during filtration.', 'The limiting reactant was impure.'], 'Retained solvent adds mass.'),
    ('Which reaction type typically has the lowest atom economy?', 'a substitution reaction producing a by-product of large mass', ['an addition reaction', 'a polymerisation by addition', 'a combination reaction forming one product'], 'By-products waste atoms.'),
])


R.facts('ch05-st4', F(
    terms=[('titration', 'a technique in which a solution of known concentration is added from a burette to a measured volume of another solution until the reaction is just complete (the equivalence point)'),
           ('equivalence point', 'the point in a titration at which the reactants have been added in exactly the stoichiometric ratio'),
           ('end point', 'the point at which the indicator changes colour, ideally coinciding with the equivalence point'),
           ('concordant titres', 'titres that agree closely, typically within ±0.10 cm³, used to calculate the mean titre'),
           ('back titration', 'a technique in which an excess of reagent is added to the analyte and the unreacted excess is then titrated to find how much reacted')],
    facts=[('Which apparatus delivers a fixed volume of solution (e.g. 25.00 cm³) most precisely?', 'a volumetric pipette', ['a measuring cylinder', 'a beaker', 'a burette read only once'], 'Pipettes have low uncertainty for a fixed volume.'),
           ('Why is the conical flask not rinsed with the solution it will contain before a titration?', 'Extra solution left in the flask would change the amount of reactant.', ['The solution would evaporate.', 'The indicator would be diluted.', 'The burette would be contaminated.'], 'Only the pipetted amount should be present; rinse with distilled water.'),
           ('Titres of 24.50, 24.15, 24.20 and 24.10 cm³ are obtained. Which mean titre should be used?', '24.15 cm³', ['24.24 cm³', '24.50 cm³', '24.30 cm³'], 'Discard the rough/anomalous 24.50; mean of concordant values.'),
           ('What is the uncertainty of a titre from a burette read to ±0.05 cm³?', '±0.10 cm³', ['±0.05 cm³', '±0.025 cm³', '±0.20 cm³'], 'Two readings (initial and final).')],
    why=[('Explain why the burette is rinsed with the titrant solution before filling.', 'Any water left inside would dilute the titrant, lowering its concentration and giving a larger titre.'),
         ('Explain why a white tile is placed under the conical flask during a titration.', 'It makes the colour change of the indicator easier to see, so the end point is judged more precisely.'),
         ('Explain why a back titration is used to find the amount of calcium carbonate in an antacid tablet.', 'CaCO₃ is insoluble and reacts slowly, so it cannot be titrated directly; an excess of acid is added to react completely, and the excess is titrated with standard alkali.')],
    contrast=[('the end point', 'the equivalence point', 'The equivalence point is when stoichiometric amounts have reacted; the end point is when the indicator changes colour – a good indicator makes them coincide.')],
    misc=[('The first (rough) titre should be included in the mean.', 'The rough titre is only a guide to the approximate end point; only concordant accurate titres are averaged.')],
    evaluate=[('Titration is the most reliable method for finding the concentration of an acid.', ['simple, cheap and very precise with concordant titres', 'uses only standard glassware'], ['subjective judgement of the end point', 'unsuitable for coloured solutions or weak/weak systems with indicators', 'pH-meter or conductometric titrations are more objective'], 'Titration is highly reliable when an appropriate indicator and good technique are used; instrumental end-point detection can improve it further.')],
))

TITR = [('hydrochloric acid', 'HCl', 'sodium hydroxide', 'NaOH', 1, 1, 'HCl(aq) + NaOH(aq) → NaCl(aq) + H₂O(l)'),
        ('sulfuric acid', 'H2SO4', 'sodium hydroxide', 'NaOH', 1, 2, 'H₂SO₄(aq) + 2NaOH(aq) → Na₂SO₄(aq) + 2H₂O(l)'),
        ('hydrochloric acid', 'HCl', 'sodium carbonate', 'Na2CO3', 2, 1, 'Na₂CO₃(aq) + 2HCl(aq) → 2NaCl(aq) + H₂O(l) + CO₂(g)'),
        ('nitric acid', 'HNO3', 'potassium hydroxide', 'KOH', 1, 1, 'HNO₃(aq) + KOH(aq) → KNO₃(aq) + H₂O(l)'),
        ('ethanoic acid', 'CH3COOH', 'sodium hydroxide', 'NaOH', 1, 1, 'CH₃COOH(aq) + NaOH(aq) → CH₃COONa(aq) + H₂O(l)'),
        ('sulfuric acid', 'H2SO4', 'ammonia', 'NH3', 1, 2, 'H₂SO₄(aq) + 2NH₃(aq) → (NH₄)₂SO₄(aq)'),
        ('hydrochloric acid', 'HCl', 'calcium hydroxide', 'Ca(OH)2', 2, 1, 'Ca(OH)₂(aq) + 2HCl(aq) → CaCl₂(aq) + 2H₂O(l)'),
        ('ethanedioic acid', 'H2C2O4', 'sodium hydroxide', 'NaOH', 1, 2, 'H₂C₂O₄(aq) + 2NaOH(aq) → Na₂C₂O₄(aq) + 2H₂O(l)')]


@R.add('ch05-st4', 'C3', (1, 5), 'numerical')
def c3_titration(rng, slot):
    an, af, bn, bf, ka, kb, eq = pick(rng, TITR)
    cb = rng.choice([0.100, 0.0500, 0.200, 0.150, 0.125, 0.0800])
    vb = rng.choice([25.00, 20.00, 10.00])
    ca_true = rng.uniform(0.04, 0.25)
    nb = cb * vb / 1000
    na = nb * ka / kb
    va = round(na / ca_true * 1000, 2)
    if not 10 < va < 45:
        return None
    ca = na / (va / 1000)
    who = name(rng)
    frame = rng.randrange(3)
    if frame == 0:
        stem = f'{who} titrated {vb:.2f} cm³ of {sf(cb)} mol dm⁻³ {bn} with {an}. The mean titre was {va:.2f} cm³. {eq}. Calculate the concentration of the {an}.'
    elif frame == 1:
        stem = f'A {vb:.2f} cm³ aliquot of {sf(cb)} mol dm⁻³ {bn} required {va:.2f} cm³ of {an} for neutralisation ({eq}). Determine the concentration of the acid.'
    else:
        stem = f'In a titration, {va:.2f} cm³ of {an} exactly neutralised {vb:.2f} cm³ of {bn} of concentration {sf(cb)} mol dm⁻³. The equation is {eq}. Find the concentration of the {an} in mol dm⁻³.'
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Calculate the concentration', 'What is the concentration').replace('Determine the concentration', 'What is the concentration').replace('Find the concentration', 'What is the concentration'), ca,
                    [nb / (va / 1000), cb * va / vb, nb * kb / ka / (va / 1000) if ka != kb else ca * 2], 'mol dm⁻³', f'n(base) = {sf(nb)} mol; n(acid) = × {ka}/{kb} = {sf(na)} mol; c = {sf(na)}/{va / 1000:.5f} = {sf(ca)} mol dm⁻³.')
    return num(stem, q(ca, 'mol dm⁻³'), f'n({chem(bf)}) = {sf(cb)} × {vb / 1000} = {sf(nb)} mol (M1); n({chem(af)}) = {sf(nb)} × {ka}/{kb} = {sf(na)} mol (M1); c = {sf(na)}/{va / 1000:.5f} = {q(ca, "mol dm⁻³")} (A1).', 3)


@R.add('ch05-st4', 'C3', (2, 5), 'numerical')
def c3_gas_stoich(rng, slot):
    metal, f, k = pick(rng, [('magnesium', 'Mg', 1), ('zinc', 'Zn', 1), ('calcium carbonate', 'CaCO3', 1), ('aluminium', 'Al', 1.5), ('sodium hydrogencarbonate', 'NaHCO3', 1)])
    gas = 'CO2' if 'C' in f else 'H2'
    eqs = {'Mg': 'Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)', 'Zn': 'Zn(s) + H₂SO₄(aq) → ZnSO₄(aq) + H₂(g)', 'CaCO3': 'CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)',
           'Al': '2Al(s) + 6HCl(aq) → 2AlCl₃(aq) + 3H₂(g)', 'NaHCO3': 'NaHCO₃(s) + HCl(aq) → NaCl(aq) + H₂O(l) + CO₂(g)'}
    m = round(rng.uniform(0.05, 0.6), 3)
    n = m / mr(f) * k
    T = rng.choice([273, 293, 298])
    if T == 273:
        V = n * VM * 1000
        cond = 'at STP (molar volume 22.7 dm³ mol⁻¹)'
        key = f'n({chem(gas)}) = {m}/{mr(f):.2f} × {k} = {sf(n)} mol (M1); V = n × 22.7 dm³ = {q(V, "cm³")} (A1).'
    else:
        V = n * RGAS * T / 100000 * 1e6
        cond = f'at {T} K and 100 kPa'
        key = f'n({chem(gas)}) = {sf(n)} mol (M1); V = nRT/p = {sf(n)} × 8.31 × {T}/(1.00 × 10⁵) m³ (M1) = {q(V, "cm³")} (A1).'
    stem = f'{m:.3f} g of {metal} reacts completely with excess acid: {eqs[f]}. Calculate the volume of {chem(gas)} produced {cond}, in cm³.'
    return num(stem, q(V, 'cm³'), key, 3 if T != 273 else 2)


@R.add('ch05-st4', 'C4', (3, 5), 'multi_step')
def c4_back_titration(rng, slot):
    tab = round(rng.uniform(0.40, 0.80), 3)
    frac_ = rng.uniform(0.6, 0.9)
    nca = tab * frac_ / mr('CaCO3')
    vhcl, chcl = 50.00, rng.choice([0.500, 0.400, 0.600])
    ntot = chcl * vhcl / 1000
    nexc = ntot - 2 * nca
    cna = rng.choice([0.200, 0.100, 0.250])
    vna = round(nexc / cna * 1000, 2)
    if not 5 < vna < 48:
        return None
    nexc = cna * vna / 1000
    nca = (ntot - nexc) / 2
    pct = nca * mr('CaCO3') / tab * 100
    prod = pick(rng, ['an antacid tablet', 'a sample of eggshell', 'a sample of limestone', 'a sample of blackboard chalk'])
    stem = (f'{prod[0].upper() + prod[1:]} of mass {tab:.3f} g was added to {vhcl:.2f} cm³ of {sf(chcl)} mol dm⁻³ HCl (an excess). After the reaction CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂ was complete, '
            f'the excess acid required {vna:.2f} cm³ of {sf(cna)} mol dm⁻³ NaOH for neutralisation. Determine the percentage by mass of CaCO₃ in the sample.')
    return num(stem, f'{pct:.1f} %', f'n(HCl) total = {sf(ntot)} mol (M1); excess n(HCl) = n(NaOH) = {sf(nexc)} mol (M1); HCl reacted = {sf(ntot - nexc)} mol (M1); n(CaCO₃) = ½ × = {sf(nca)} mol (M1); mass = {sf(nca * mr("CaCO3"))} g; {pct:.1f} % (A1).', 5, 'multi_step')


R.mcqs('ch05-st4', 'C2', (1, 4), [
    ('25.0 cm³ of 0.10 mol dm⁻³ H₂SO₄ is neutralised by NaOH. What amount of NaOH is needed?', '5.0 × 10⁻³ mol', ['2.5 × 10⁻³ mol', '1.25 × 10⁻³ mol', '5.0 mol'], 'n(H₂SO₄) = 2.5 × 10⁻³; × 2.'),
    ('A burette is not rinsed with the titrant, only with water. What is the effect on the titre?', 'The titre is too large.', ['The titre is too small.', 'No effect.', 'The end point is not seen.'], 'Diluted titrant: more volume needed.'),
    ('Air bubble in the burette tip escapes during the titration. What is the effect on the recorded titre?', 'It appears larger than it should.', ['It appears smaller.', 'No effect.', 'The indicator changes too early.'], 'Volume reading includes the bubble.'),
    ('Which reading should be recorded for a burette with the bottom of the meniscus exactly halfway between 22.1 and 22.2 cm³?', '22.15 cm³', ['22.1 cm³', '22.2 cm³', '22.150 cm³'], 'Read to the nearest 0.05 cm³.'),
])


@p1b(R, 'ch05-st4')
def p1b_titration(rng, slot):
    cb = rng.choice([0.100, 0.0950, 0.105])
    mean = round(rng.uniform(21.0, 26.0), 2)
    t = [round(mean + rng.uniform(-0.6, 1.2), 2) if i == 0 else round(mean + rng.uniform(-0.06, 0.06), 2) for i in range(4)]
    t[0] = round(mean + rng.choice([0.5, 0.7, 0.9]), 2)
    conc = t[1:]
    m = sum(conc) / 3
    ns = cb * m / 1000
    ca = ns / 0.025
    pv = 0.10 / m * 100 + 0.06 / 25.00 * 100
    tab = '\n'.join(f'{"rough" if i == 0 else i} | {x:.2f}' for i, x in enumerate(t))
    intro = (f'25.00 cm³ (±0.06 cm³) of hydrochloric acid was pipetted into a conical flask and titrated with {sf(cb)} mol dm⁻³ sodium hydroxide using phenolphthalein. Burette readings are ±0.05 cm³.\n\nTitration | titre / cm³\n{tab}')
    return dict(intro=intro, parts=[
        ('Calculate the mean titre, explaining which values you used.', f'{m:.2f} cm³ (rough titre excluded)', f'Concordant titres only (rough excluded) (M1); mean = {m:.2f} cm³ (A1).', 2),
        ('Calculate the concentration of the hydrochloric acid.', q(ca, 'mol dm⁻³'), f'n(NaOH) = {sf(cb)} × {m / 1000:.5f} = {sf(ns)} mol (M1); c(HCl) = {sf(ns)}/0.02500 = {q(ca, "mol dm⁻³")} (A1).', 2),
        ('Calculate the total percentage uncertainty in the concentration, considering the titre and the pipette only.', f'{pv:.2f} %', f'titre ±0.10/{m:.2f} × 100 + pipette 0.06/25.00 × 100 (M1) = {pv:.2f} % (A1).', 2),
        ('State the colour change at the end point.', 'colourless to (pale) pink', 'colourless → pink (1).', 1)],
        extras=[('Suggest why the rough titre is larger than the others.', 'The titrant was added quickly in large portions, overshooting the end point.', 'Overshoot during fast addition (1).', 1)])


# =============================================================================================
# ch06 S2.1 The ionic model
# =============================================================================================
CATIONS = [('sodium', 'Na', 1), ('potassium', 'K', 1), ('lithium', 'Li', 1), ('silver', 'Ag', 1), ('ammonium', 'NH4', 1),
           ('magnesium', 'Mg', 2), ('calcium', 'Ca', 2), ('barium', 'Ba', 2), ('zinc', 'Zn', 2), ('copper(II)', 'Cu', 2),
           ('iron(II)', 'Fe', 2), ('iron(III)', 'Fe', 3), ('aluminium', 'Al', 3), ('lead(II)', 'Pb', 2), ('copper(I)', 'Cu', 1),
           ('chromium(III)', 'Cr', 3), ('strontium', 'Sr', 2), ('manganese(II)', 'Mn', 2)]
ANIONS = [('chloride', 'Cl', 1), ('bromide', 'Br', 1), ('iodide', 'I', 1), ('fluoride', 'F', 1), ('oxide', 'O', 2), ('sulfide', 'S', 2),
          ('nitride', 'N', 3), ('hydroxide', 'OH', 1), ('nitrate', 'NO3', 1), ('sulfate', 'SO4', 2), ('carbonate', 'CO3', 2),
          ('phosphate', 'PO4', 3), ('hydrogencarbonate', 'HCO3', 1), ('ethanoate', 'CH3COO', 1), ('sulfite', 'SO3', 2),
          ('nitrite', 'NO2', 1), ('hydrogensulfate', 'HSO4', 1), ('phosphide', 'P', 3)]
POLY = {'NH4', 'OH', 'NO3', 'SO4', 'CO3', 'PO4', 'HCO3', 'CH3COO', 'SO3', 'NO2', 'HSO4'}


def ionic_formula(cat, an):
    _, cs, cq = cat
    _, as_, aq = an
    g = math.gcd(cq, aq)
    nc, na = aq // g, cq // g

    def part(sym, n):
        if n == 1:
            return sym
        return f'({sym}){n}' if sym in POLY else f'{sym}{n}'
    if as_ == 'CH3COO':
        return ('(CH3COO)' + str(na) if na > 1 else 'CH3COO') + part(cs, nc)
    return part(cs, nc) + part(as_, na)


def ion_sym(sym, q_, neg=False):
    c = ('' if q_ == 1 else str(q_)) + ('-' if neg else '+')
    return chem(sym + '^' + c) if sym in POLY or sym[-1].isdigit() else ion(sym + c)


R.facts('ch06-st1', F(
    terms=[('ionic bond', 'the electrostatic attraction between oppositely charged ions'),
           ('cation', 'a positively charged ion, formed when an atom loses one or more electrons'),
           ('anion', 'a negatively charged ion, formed when an atom gains one or more electrons'),
           ('isoelectronic', 'having the same number of electrons (and electron configuration) as another species'),
           ('ionic radius', 'the radius of an ion in an ionic lattice; cations are smaller and anions larger than their parent atoms')],
    facts=[('What is the charge on the ion formed by an element in group 16?', '2−', ['2+', '6+', '6−'], 'Gains two electrons to complete an octet.'),
           ('Which pair of elements is most likely to form an ionic compound?', 'potassium and fluorine', ['carbon and oxygen', 'nitrogen and hydrogen', 'sulfur and chlorine'], 'Large electronegativity difference: metal + non-metal.'),
           ('Which ion is isoelectronic with neon?', 'Mg²⁺', ['Ca²⁺', 'Cl⁻', 'K⁺'], 'Mg²⁺ has 10 electrons.'),
           ('What happens to electrons when sodium reacts with chlorine?', 'One electron is transferred from each Na atom to a Cl atom.', ['Electrons are shared equally.', 'Chlorine loses an electron to sodium.', 'Electrons are delocalised.'], 'Na → Na⁺ + e⁻; Cl + e⁻ → Cl⁻.')],
    why=[('Explain why magnesium forms Mg²⁺ ions rather than Mg⁺ or Mg³⁺ ions.', 'Losing the two 3s electrons gives the stable [Ne] configuration; removing a third electron would require breaking into the inner 2p shell, which needs far more energy (very large third ionisation energy).'),
         ('Explain why a sodium ion is smaller than a sodium atom.', 'Na⁺ has lost its only 3s electron, so it has one fewer occupied shell; the remaining electrons are attracted by the same nuclear charge, which pulls them closer.'),
         ('Explain why a chloride ion is larger than a chlorine atom.', 'The extra electron increases electron–electron repulsion in the outer shell while the nuclear charge is unchanged, so the electron cloud expands.'),
         ('Explain why the ions in the series O²⁻, F⁻, Na⁺, Mg²⁺ decrease in radius.', 'They are isoelectronic (10 electrons); nuclear charge increases from 8 to 12, so the same electrons are pulled closer to the nucleus.')],
    contrast=[('a cation', 'an anion', 'A cation is positive, formed by losing electrons (usually metals); an anion is negative, formed by gaining electrons (usually non-metals).')],
    misc=[('Ionic bonds form because sodium wants to lose an electron.', 'Atoms have no desires; the overall process is energetically favourable because the lattice energy released when oppositely charged ions attract outweighs the energy needed to form the ions.'),
          ('An ionic bond is the transfer of electrons from a metal to a non-metal.', 'Electron transfer forms the ions; the ionic bond itself is the electrostatic attraction between the oppositely charged ions.')],
    evaluate=[('The octet rule is a reliable way to predict the charges on ions.', ['correctly predicts charges for groups 1, 2, 13, 15–17', 'simple and quick'], ['transition metals form ions with variable charges that do not have octets (Fe²⁺, Fe³⁺)', 'heavier p-block metals (Pb²⁺, Sn²⁺) do not follow it', 'energetics (IE vs lattice enthalpy) are the real explanation'], 'Useful for main-group elements but limited; charge depends on the balance of ionisation energies and lattice enthalpy.')],
))

GROUP_CHARGE = {'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1, 'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Al': 3,
                'N': -3, 'P': -3, 'O': -2, 'S': -2, 'Se': -2, 'F': -1, 'Cl': -1, 'Br': -1, 'I': -1}
GROUPN = {'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1, 'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Al': 13,
          'N': 15, 'P': 15, 'O': 16, 'S': 16, 'Se': 16, 'F': 17, 'Cl': 17, 'Br': 17, 'I': 17}


@R.add('ch06-st1', 'C3', (1, 5), 'short')
def c3_ion_from_group(rng, slot):
    m = pick(rng, [e for e in GROUP_CHARGE if GROUP_CHARGE[e] > 0])
    nm_ = pick(rng, [e for e in GROUP_CHARGE if GROUP_CHARGE[e] < 0])
    qm, qn = GROUP_CHARGE[m], -GROUP_CHARGE[nm_]
    g = math.gcd(qm, qn)
    f = f'{m}{"" if qn // g == 1 else qn // g}{nm_}{"" if qm // g == 1 else qm // g}'
    if slot.d <= 2:
        stem = f'{ENAME[m].capitalize()} (group {GROUPN[m]}) reacts with {ENAME[nm_]} (group {GROUPN[nm_]}). State the charges on the ions formed and deduce the formula of the compound.'
        return dict(stem=stem, answer=f'{ion(m + ("" if qm == 1 else str(qm)) + "+")} and {ion(nm_ + ("" if qn == 1 else str(qn)) + "-")}; {chem(f)}', markingKey=f'Charges from group numbers (1); formula balanced for neutrality: {chem(f)} (1).', type='short', marks=2)
    zm, zn = Z[m], Z[nm_]
    stem = (f'Describe, in terms of electrons, the formation of the ionic compound between {ENAME[m]} (Z = {zm}) and {ENAME[nm_]} (Z = {zn}), giving the electron configurations of the ions and the formula of the compound.')
    cm = cfg_short(config_ion(zm, qm)) if zm <= 36 else ''
    cn = cfg_short(config_ion(zn, -qn)) if zn <= 36 else ''
    return dict(stem=stem, answer=f'Each {m} loses {qm} electron(s) → {ion(m + ("" if qm == 1 else str(qm)) + "+")} ({cm}); each {nm_} gains {qn} → {ion(nm_ + ("" if qn == 1 else str(qn)) + "-")} ({cn}); {chem(f)}; ions held by electrostatic attraction in a lattice.',
                markingKey=f'Electron transfer from {m} to {nm_} with correct numbers (1); configurations {cm} and {cn} (1); formula {chem(f)} (1); electrostatic attraction between oppositely charged ions in a lattice (1).', type='explain', marks=4)


@R.add('ch06-st1', 'C3', (1, 4), 'mcq')
def c3_isoelectronic(rng, slot):
    species = [('O', -2), ('F', -1), ('Na', 1), ('Mg', 2), ('Al', 3), ('N', -3), ('S', -2), ('Cl', -1), ('K', 1), ('Ca', 2), ('P', -3), ('Ne', 0), ('Ar', 0)]
    tgt = pick(rng, [s for s in species])
    ne = Z[tgt[0]] - tgt[1]
    same = [s for s in species if Z[s[0]] - s[1] == ne and s != tgt]
    diff = [s for s in species if Z[s[0]] - s[1] != ne]
    if not same:
        return None
    lab = lambda s: s[0] if s[1] == 0 else ion(s[0] + ('' if abs(s[1]) == 1 else str(abs(s[1]))) + ('+' if s[1] > 0 else '-'))
    r = pick(rng, same)
    w = rng.sample(diff, 3)
    return mcq(rng, f'Which species is isoelectronic with {lab(tgt)}?', lab(r), [lab(x) for x in w], f'{lab(tgt)} and {lab(r)} both have {ne} electrons.')


@R.add('ch06-st1', 'C3', (2, 4), 'mcq')
def c3_radius_order(rng, slot):
    series = [[('N', -3, 146), ('O', -2, 140), ('F', -1, 133), ('Na', 1, 102), ('Mg', 2, 72), ('Al', 3, 54)],
              [('P', -3, 212), ('S', -2, 184), ('Cl', -1, 181), ('K', 1, 138), ('Ca', 2, 100)]]
    ser = pick(rng, series)
    pool = rng.sample(ser, 4 if len(ser) >= 4 else 3)
    lab = lambda s: ion(s[0] + ('' if abs(s[1]) == 1 else str(abs(s[1]))) + ('+' if s[1] > 0 else '-'))
    srt = sorted(pool, key=lambda s: -s[2])
    right = ' > '.join(lab(s) for s in srt)
    wr = [' > '.join(lab(s) for s in reversed(srt)), ' > '.join(lab(s) for s in sorted(pool, key=lambda s: Z[s[0]])[::-1]), ' > '.join(lab(s) for s in (srt[1:2] + srt[0:1] + srt[2:]))]
    wr = [w for w in wr if w != right]
    if len(set(wr)) < 3:
        wr.append(' > '.join(lab(s) for s in (srt[:-2] + srt[-1:] + srt[-2:-1])))
    return mcq(rng, 'Which shows the ions in order of decreasing ionic radius?', right, list(dict.fromkeys(wr))[:3],
               'Isoelectronic ions: radius falls as nuclear charge rises (' + ', '.join(f'{lab(s)} {s[2]} pm' for s in srt) + ').')


R.mcqs('ch06-st1', 'C2', (1, 4), [
    ('Which is the best description of ionic bonding?', 'electrostatic attraction between oppositely charged ions', ['sharing of electron pairs between atoms', 'attraction between cations and delocalised electrons', 'attraction between permanent dipoles'], 'Definition.'),
    ('Element X forms X³⁺ and element Y forms Y²⁻. What is the formula of the compound?', 'X₂Y₃', ['X₃Y₂', 'XY', 'X₂Y'], 'Total charge 2(3+) + 3(2−) = 0.'),
    ('Which atom forms an ion that is larger than the atom?', 'sulfur', ['sodium', 'calcium', 'aluminium'], 'Anions are larger than their atoms.'),
    ('Why do noble gases rarely form ions?', 'They have full outer shells and very high ionisation energies.', ['They are gases.', 'They have no electrons in the outer shell.', 'Their nuclei are unstable.'], 'Stable configurations; high IE.'),
])


R.facts('ch06-st2', F(
    terms=[('polyatomic ion', 'an ion made of two or more covalently bonded atoms carrying an overall charge, such as SO₄²⁻ or NH₄⁺'),
           ('Roman numeral in a name', 'the oxidation state of a metal that can form ions of different charge, e.g. iron(III) = Fe³⁺'),
           ('formula unit', 'the simplest ratio of ions in an ionic compound, used because ionic compounds have no molecules')],
    facts=[('What is the formula of the sulfate ion?', 'SO₄²⁻', ['SO₃²⁻', 'S²⁻', 'SO₄⁻'], 'Sulfite is SO₃²⁻; sulfide S²⁻.'),
           ('What is the formula of ammonium phosphate?', '(NH₄)₃PO₄', ['NH₄PO₄', 'NH₄(PO₄)₃', '(NH₄)₂PO₄'], 'Three NH₄⁺ balance PO₄³⁻.'),
           ('What is the name of Fe₂O₃?', 'iron(III) oxide', ['iron(II) oxide', 'diiron trioxide(II)', 'iron oxide(III)'], 'Fe must be 3+ to balance three O²⁻.'),
           ('What is the charge on the hydrogencarbonate ion?', '1−', ['2−', '1+', '2+'], 'HCO₃⁻.')],
    why=[('Explain why brackets are needed in the formula Ca(OH)₂ but not in NaOH.', 'Brackets show that the subscript 2 applies to the whole hydroxide ion; in NaOH there is only one hydroxide ion so no brackets are needed.'),
         ('Explain why Roman numerals are used in the names of compounds of transition elements such as copper.', 'Transition elements form ions with more than one possible charge (Cu⁺ and Cu²⁺); the Roman numeral states the oxidation state, so the formula is unambiguous.')],
    misc=[('The formula of aluminium sulfate is AlSO₄.', 'Al³⁺ and SO₄²⁻ must balance: Al₂(SO₄)₃.'),
          ('Magnesium hydroxide is MgOH₂.', 'Brackets are needed: Mg(OH)₂; MgOH₂ would mean one O and two H atoms.')],
    evaluate=[('Systematic (IUPAC) names should completely replace traditional names such as “baking soda” or “ferric chloride”.', ['unambiguous international communication', 'encodes formula information'], ['traditional names are familiar to the public and industry', 'systematic names can be long and confusing for non-specialists'], 'Systematic names should be used in science, while common names remain useful in everyday contexts – an example of language and knowledge (TOK).')],
))


@R.add('ch06-st2', 'C3', (1, 5), 'short')
def c3_name_to_formula(rng, slot):
    cat = pick(rng, CATIONS)
    an = pick(rng, ANIONS)
    if cat[1] == 'NH4' and an[1] in ('O', 'S', 'N', 'P', 'OH'):
        return None
    f = ionic_formula(cat, an)
    nmc = f'{cat[0]} {an[0]}'
    if rng.random() < 0.5:
        stem = pick(rng, [f'Deduce the formula of {nmc}.', f'Write the formula of the ionic compound {nmc}, showing how the charges balance.'])
        return dict(stem=stem, answer=chem(f), markingKey=f'Ions {ion_sym(cat[1], cat[2])} and {ion_sym(an[1], an[2], True)} (1); charges balance in {chem(f)} (1).', type='short', marks=2)
    stem = pick(rng, [f'Name the compound {chem(f)}.', f'State the name of the ionic compound with the formula {chem(f)}.'])
    return dict(stem=stem, answer=nmc, markingKey=f'{nmc} (1)' + ('; Roman numeral required for the variable-charge metal (1).' if '(' in cat[0] else '.'), type='short', marks=2 if '(' in cat[0] else 1)


@R.add('ch06-st2', 'C3', (1, 4), 'mcq')
def c3_formula_mcq(rng, slot):
    cat = pick(rng, [c for c in CATIONS if c[2] > 1 or c[1] == 'NH4'])
    an = pick(rng, [a for a in ANIONS if a[2] > 1 or a[1] in POLY])
    if cat[1] == 'NH4' and an[1] in ('O', 'S', 'N', 'P', 'OH'):
        return None
    f = ionic_formula(cat, an)
    w = set()
    w.add(cat[1] + an[1] if cat[1] not in POLY else cat[1] + an[1])
    w.add(ionic_formula((cat[0], cat[1], an[2] + 1), an))
    w.add(ionic_formula((cat[0], cat[1], an[2]), (an[0], an[1], cat[2])) if cat[2] != an[2] else ionic_formula(cat, (an[0], an[1], an[2] + 1)))
    w.add(ionic_formula(cat, (an[0], an[1], cat[2])) if cat[2] != an[2] else cat[1] + '2' + an[1])
    w.discard(f)
    wl = [chem(x) for x in w if chem(x) != chem(f)]
    if len(wl) < 3:
        return None
    return mcq(rng, f'What is the formula of {cat[0]} {an[0]}?', chem(f), wl[:3], f'{ion_sym(cat[1], cat[2])} and {ion_sym(an[1], an[2], True)}: {chem(f)} is neutral.')


@R.add('ch06-st2', 'C1', (1, 3), 'short')
def c1_poly(rng, slot):
    an = pick(rng, [a for a in ANIONS if a[1] in POLY] + [('ammonium', 'NH4', -1)])
    if an[1] == 'NH4':
        return dict(stem='State the formula and charge of the ammonium ion.', answer='NH₄⁺', markingKey='NH₄⁺ (1).', type='short', marks=1)
    return dict(stem=pick(rng, [f'State the formula, including charge, of the {an[0]} ion.', f'Give the formula of the {an[0]} ion.']), answer=ion_sym(an[1], an[2], True), markingKey=f'{ion_sym(an[1], an[2], True)} – formula and charge both required (1).', type='short', marks=1)


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step')
def c4_precip(rng, slot):
    a_cat, a_an, ppt_cat, ppt_an, ppt, colour = pick(rng, [
        (('silver', 'Ag', 1), ('nitrate', 'NO3', 1), ('sodium', 'Na', 1), ('chloride', 'Cl', 1), 'AgCl', 'white'),
        (('barium', 'Ba', 2), ('chloride', 'Cl', 1), ('sodium', 'Na', 1), ('sulfate', 'SO4', 2), 'BaSO4', 'white'),
        (('lead(II)', 'Pb', 2), ('nitrate', 'NO3', 1), ('potassium', 'K', 1), ('iodide', 'I', 1), 'PbI2', 'yellow'),
        (('copper(II)', 'Cu', 2), ('sulfate', 'SO4', 2), ('sodium', 'Na', 1), ('hydroxide', 'OH', 1), 'Cu(OH)2', 'blue'),
        (('iron(III)', 'Fe', 3), ('chloride', 'Cl', 1), ('sodium', 'Na', 1), ('hydroxide', 'OH', 1), 'Fe(OH)3', 'orange-brown'),
        (('calcium', 'Ca', 2), ('chloride', 'Cl', 1), ('sodium', 'Na', 1), ('carbonate', 'CO3', 2), 'CaCO3', 'white')])
    f1 = ionic_formula(a_cat, a_an)
    f2 = ionic_formula(ppt_cat, ppt_an)
    spect = ionic_formula(ppt_cat, a_an)
    stem = (f'Aqueous {a_cat[0]} {a_an[0]} is mixed with aqueous {ppt_cat[0]} {ppt_an[0]} and a precipitate ({colour}) forms. '
            f'(a) Write the formulae of the two reactants. (b) Identify the precipitate and write an ionic equation, with state symbols, for its formation. (c) Identify the spectator ions. (d) Name the salt left in solution.')
    q1, q2 = a_cat[2], ppt_an[2]
    g = math.gcd(q1, q2)
    ie = f'{"" if q2 // g == 1 else q2 // g}{ion_sym(a_cat[1], a_cat[2])}(aq) + {"" if q1 // g == 1 else q1 // g}{ion_sym(ppt_an[1], ppt_an[2], True)}(aq) → {chem(ppt)}(s)'
    return num(stem, f'(a) {chem(f1)}, {chem(f2)}; (b) {chem(ppt)}: {ie}; (c) {ion_sym(ppt_cat[1], ppt_cat[2])} and {ion_sym(a_an[1], a_an[2], True)}; (d) {ppt_cat[0]} {a_an[0]}',
               f'(a) {chem(f1)} and {chem(f2)} (A1). (b) {chem(ppt)} (A1); {ie} – balanced with state symbols (A1). (c) {ion_sym(ppt_cat[1], ppt_cat[2])} and {ion_sym(a_an[1], a_an[2], True)} (A1). (d) {ppt_cat[0]} {a_an[0]}, {chem(spect)} (A1).', 5, 'multi_step')


R.mcqs('ch06-st2', 'C2', (1, 4), [
    ('Which formula is correct?', 'Al₂(SO₄)₃', ['Al(SO₄)₃', 'Al₃(SO₄)₂', 'AlSO₄'], 'Charge balance 2 × 3+ = 3 × 2−.'),
    ('What is the charge of the metal ion in Cu₂O?', '1+', ['2+', '1−', '2−'], 'O²⁻ balanced by two Cu⁺.'),
    ('Which compound contains the nitride ion?', 'Mg₃N₂', ['Mg(NO₃)₂', 'Mg(NO₂)₂', 'NH₄Cl'], 'Nitride = N³⁻.'),
    ('How many ions are present in one formula unit of calcium phosphate, Ca₃(PO₄)₂?', '5', ['13', '2', '3'], '3 Ca²⁺ + 2 PO₄³⁻.'),
])


R.facts('ch06-st3', F(
    terms=[('ionic lattice', 'a giant three-dimensional regular arrangement of alternating cations and anions held together by electrostatic attraction'),
           ('lattice enthalpy', 'the standard enthalpy change when one mole of a solid ionic compound is separated into its gaseous ions; it is endothermic, e.g. NaCl(s) → Na⁺(g) + Cl⁻(g)'),
           ('coordination number', 'the number of nearest oppositely charged ions surrounding a given ion in a lattice (6 in NaCl)'),
           ('brittleness', 'the tendency of an ionic solid to shatter when a force displaces layers so that ions of like charge come next to each other and repel')],
    facts=[('Why do ionic compounds have high melting points?', 'Many strong electrostatic attractions between ions in the lattice must be overcome.', ['Their molecules are large.', 'They contain covalent bonds.', 'They have delocalised electrons.'], 'Giant lattice.'),
           ('Under which conditions does sodium chloride conduct electricity?', 'when molten or dissolved in water', ['as a solid', 'only as a solid at high pressure', 'never'], 'Ions must be mobile.'),
           ('Which compound has the largest lattice enthalpy?', 'MgO', ['NaCl', 'KBr', 'CsI'], 'Higher charges and smaller ions.'),
           ('What is the coordination number of each ion in the sodium chloride lattice?', '6', ['4', '8', '12'], 'Octahedral arrangement.'),
           ('Which factor increases lattice enthalpy?', 'smaller ionic radii', ['larger ionic radii', 'lower ionic charges', 'a lower melting point'], 'Lattice enthalpy ∝ charge product / sum of radii.')],
    why=[('Explain why solid sodium chloride does not conduct electricity but molten sodium chloride does.', 'In the solid the ions are held in fixed positions in the lattice and cannot move; when molten the lattice breaks down and the ions are free to move and carry charge.'),
         ('Explain why ionic compounds are brittle.', 'A force can shift layers of ions so that ions of the same charge come next to each other; the repulsion between like charges causes the lattice to split.'),
         ('Explain why magnesium oxide has a much higher melting point (2852 °C) than sodium chloride (801 °C).', 'Mg²⁺ and O²⁻ have double charges and are smaller than Na⁺ and Cl⁻, so the electrostatic attractions (lattice enthalpy) are much stronger.'),
         ('Explain why many ionic compounds dissolve in water but not in hexane.', 'Polar water molecules are attracted to the ions (ion–dipole attractions), releasing energy that helps overcome the lattice; non-polar hexane cannot interact strongly with ions.')],
    contrast=[('the volatility of ionic compounds', 'the volatility of simple molecular compounds', 'Ionic compounds have low volatility (high boiling points) because strong ionic bonds throughout the lattice must be broken; simple molecular compounds are volatile because only weak intermolecular forces must be overcome.')],
    misc=[('Sodium chloride conducts electricity when solid because it contains charged particles.', 'Ions are present but fixed in the lattice; conduction requires mobile charge carriers, so the solid does not conduct.'),
          ('Lattice enthalpy is the energy released when one mole of a solid is formed from its elements.', 'That is the enthalpy of formation; lattice enthalpy (IB definition) is the endothermic change for separating 1 mol of solid into gaseous ions.')],
    evaluate=[('Lattice enthalpy alone determines whether an ionic compound is soluble in water.', ['high lattice enthalpy compounds (MgO, CaF₂) tend to be insoluble', 'lattice must be broken for dissolving'], ['hydration enthalpies of the ions are equally important', 'entropy changes contribute to ΔG of solution', 'many compounds with high lattice enthalpy are still soluble (e.g. MgSO₄)'], 'Solubility depends on the balance of lattice and hydration enthalpies and entropy, not lattice enthalpy alone.')],
))

LATT = [('NaF', 'Na', 'F', 1, 1, 102, 133, 930), ('NaCl', 'Na', 'Cl', 1, 1, 102, 181, 790), ('NaBr', 'Na', 'Br', 1, 1, 102, 196, 754),
        ('NaI', 'Na', 'I', 1, 1, 102, 220, 705), ('KF', 'K', 'F', 1, 1, 138, 133, 829), ('KCl', 'K', 'Cl', 1, 1, 138, 181, 720),
        ('KBr', 'K', 'Br', 1, 1, 138, 196, 691), ('KI', 'K', 'I', 1, 1, 138, 220, 650), ('LiF', 'Li', 'F', 1, 1, 76, 133, 1049),
        ('LiCl', 'Li', 'Cl', 1, 1, 76, 181, 864), ('MgO', 'Mg', 'O', 2, 2, 72, 140, 3791), ('CaO', 'Ca', 'O', 2, 2, 100, 140, 3401),
        ('MgCl2', 'Mg', 'Cl', 2, 1, 72, 181, 2540), ('CaCl2', 'Ca', 'Cl', 2, 1, 100, 181, 2271), ('BaO', 'Ba', 'O', 2, 2, 135, 140, 3054),
        ('CsI', 'Cs', 'I', 1, 1, 167, 220, 604), ('MgF2', 'Mg', 'F', 2, 1, 72, 133, 2978), ('SrO', 'Sr', 'O', 2, 2, 118, 140, 3223)]


@R.add('ch06-st3', 'C3', (1, 4), 'mcq')
def c3_latt_order(rng, slot):
    pool = rng.sample(LATT, 4)
    vals = [p[7] for p in pool]
    if len(set(vals)) < 4:
        return None
    hi = rng.random() < 0.5
    best = max(pool, key=lambda p: p[7]) if hi else min(pool, key=lambda p: p[7])
    return mcq(rng, f'Which compound has the {"largest" if hi else "smallest"} lattice enthalpy?', chem(best[0]), [chem(p[0]) for p in pool if p != best],
               'Lattice enthalpy increases with ionic charge and decreases with ionic radius: ' + ', '.join(f'{chem(p[0])} {p[7]}' for p in pool) + ' kJ mol⁻¹.')


@R.add('ch06-st3', 'C2', (2, 4), 'explain')
def c2_latt_pair(rng, slot):
    a, b = rng.sample(LATT, 2)
    if abs(a[7] - b[7]) < 30:
        return None
    if a[7] < b[7]:
        a, b = b, a
    if a[3] * a[4] > b[3] * b[4]:
        reason = f'the ions in {chem(a[0])} carry higher charges ({ion(a[1] + ("" if a[3] == 1 else str(a[3])) + "+")}, {ion(a[2] + ("" if a[4] == 1 else str(a[4])) + "-")})'
        if a[5] + a[6] < b[5] + b[6]:
            reason += ' and are smaller'
    else:
        reason = f'the ions in {chem(a[0])} are smaller (sum of radii {a[5] + a[6]} pm vs {b[5] + b[6]} pm) with the same charges'
    stem = f'The lattice enthalpy of {chem(a[0])} is {a[7]} kJ mol⁻¹ and that of {chem(b[0])} is {b[7]} kJ mol⁻¹. Explain this difference.'
    return dict(stem=stem, answer=f'Stronger electrostatic attraction in {chem(a[0])}: {reason}.', markingKey=f'{reason} (1); ions closer together / greater charge density gives stronger electrostatic attraction (1); more energy needed to separate the ions (1).', type='explain', marks=3)


@R.add('ch06-st3', 'C3', (2, 5), 'short')
def c3_property_predict(rng, slot):
    sub, data, kind = pick(rng, [
        ('X', 'melting point 1080 °C; does not conduct when solid; conducts when molten and when dissolved; brittle', 'ionic'),
        ('Y', 'melting point −95 °C; does not conduct in any state; insoluble in water', 'simple molecular'),
        ('Z', 'melting point 1660 °C; conducts when solid and when molten; malleable', 'metallic'),
        ('W', 'melting point 1710 °C; does not conduct in any state; insoluble in all solvents; very hard', 'giant covalent (covalent network)'),
        ('V', 'melting point 714 °C; solid does not conduct; aqueous solution conducts', 'ionic'),
        ('U', 'boiling point 80 °C; dissolves in hexane but not in water; does not conduct', 'simple molecular (non-polar)')])
    stem = f'Substance {sub} has the following properties: {data}. Deduce the type of bonding and structure in {sub}, giving reasons based on two properties.'
    return dict(stem=stem, answer=kind, markingKey=f'{kind} (1); two properties correctly linked to structure (e.g. conduction only when ions/electrons mobile, melting point reflecting strength of forces) (2).', type='explain', marks=3)


R.mcqs('ch06-st3', 'C2', (1, 4), [
    ('Which property is typical of ionic compounds?', 'They conduct electricity when molten.', ['They are malleable.', 'They have low melting points.', 'They conduct as solids.'], 'Mobile ions when molten.'),
    ('Which explains why KCl has a lower lattice enthalpy than NaCl?', 'K⁺ is larger than Na⁺.', ['K⁺ has a higher charge.', 'K is less reactive.', 'KCl is covalent.'], 'Larger ions → weaker attraction.'),
    ('Which equation represents the lattice enthalpy of calcium chloride?', 'CaCl₂(s) → Ca²⁺(g) + 2Cl⁻(g)', ['Ca(s) + Cl₂(g) → CaCl₂(s)', 'Ca²⁺(aq) + 2Cl⁻(aq) → CaCl₂(s)', 'CaCl₂(s) → Ca(g) + Cl₂(g)'], 'Solid → gaseous ions (endothermic).'),
    ('Why does an ionic crystal shatter when struck?', 'Layers shift so ions with like charges repel.', ['Delocalised electrons are lost.', 'Covalent bonds break.', 'The ions lose their charge.'], 'Brittleness.'),
])


R.facts('ch06-st1', F(**{**R.f['ch06-st1'].__dict__,
    'evaluate': R.f['ch06-st1'].evaluate + [
        ('Describing sodium chloride as made of “NaCl molecules” is acceptable shorthand.', ['the formula NaCl gives the correct 1:1 ratio', 'simplifies equations'], ['there are no discrete molecules: each ion is surrounded by six oppositely charged ions', 'the term misleads about properties such as high melting point and conductivity when molten'], 'It is misleading; “formula unit” should be used because the bonding is non-directional throughout a giant lattice.'),
        ('Ionic and covalent bonding are completely different types of bonding.', ['ionic bonding involves electron transfer and ions; covalent bonding involves shared pairs', 'they give very different properties'], ['bonding is a continuum: most compounds have partial ionic and partial covalent character', 'polarisation of anions by small, highly charged cations gives covalent character (e.g. AlCl₃)'], 'They are idealised extremes of a continuum described by electronegativity difference (bonding triangle).')],
    'extended': [('Calcium (Z = 20) reacts with nitrogen (Z = 7) when heated. (a) Give the electron configurations of the atoms and ions involved. (b) Deduce the formula of the product, explaining how the charges balance. (c) Explain why the product has a high melting point.', '(a) Ca [Ar] 4s² → Ca²⁺ [Ar]; N [He] 2s² 2p³ → N³⁻ [Ne]. (b) Ca₃N₂: 3 × (+2) = 2 × (−3) = 6 electrons transferred. (c) Giant ionic lattice with strong electrostatic attraction between highly charged ions; much energy is needed to separate them.', 6, 'multi_step'),
                 ('Lithium reacts with oxygen to form lithium oxide. Describe the formation of lithium oxide in terms of electron transfer, draw the electron arrangements (dot-and-cross) of the ions and explain why the compound conducts electricity only when molten.', '2Li → 2Li⁺ + 2e⁻; O + 2e⁻ → O²⁻; Li₂O. Dot-and-cross: [Li]⁺ with empty outer shell (shown as 1s²), [O]²⁻ with 8 outer electrons (six dots, two crosses), square brackets with charges. Solid: ions fixed; molten: ions mobile and carry charge.', 5, 'multi_step')]}))


@R.add('ch06-st1', 'C4', (3, 5), 'multi_step')
def c4_ion_formation(rng, slot):
    m = pick(rng, ['Na', 'Mg', 'Al', 'K', 'Ca', 'Li'])
    x = pick(rng, ['O', 'F', 'Cl', 'S', 'N'])
    qm, qx = GROUP_CHARGE[m], -GROUP_CHARGE[x]
    g = math.gcd(qm, qx)
    f = f'{m}{"" if qx // g == 1 else qx // g}{x}{"" if qm // g == 1 else qm // g}'
    e_tr = qm * (qx // g)
    stem = (f'{ENAME[m].capitalize()} reacts with {ENAME[x]} to form an ionic compound. (a) Deduce its formula. (b) State the total number of electrons transferred per formula unit. '
            f'(c) Explain, using the successive ionisation energies of {m}, why it forms a {qm}+ ion. (d) Predict, with a reason, whether its melting point is higher or lower than that of sodium chloride.')
    higher = qm * qx > 1
    return num(stem, f'(a) {chem(f)}; (b) {e_tr}; (d) {"higher" if higher else "similar/lower"}',
               f'(a) {chem(f)} (A1). (b) {e_tr} electrons (A1). (c) a large jump after the {["first", "second", "third"][qm - 1]} IE: the next electron would come from an inner shell (R1). (d) ' +
               (f'higher: ions carry greater charge(s) so stronger electrostatic attraction (R1).' if higher else 'similar or lower depending on ion sizes; same charges, compare radii (R1).'), 5, 'multi_step')


R.facts('ch06-st2', F(**{**R.f['ch06-st2'].__dict__,
    'why': R.f['ch06-st2'].why + [
        ('Explain why the formula of an ionic compound must be electrically neutral.', 'The compound as a whole has no net charge; the total positive charge of the cations must equal the total negative charge of the anions, which fixes the ratio of ions.'),
        ('Explain why the names sulfide, sulfite and sulfate refer to different ions.', 'Sulfide is S²⁻ (no oxygen); sulfite is SO₃²⁻ and sulfate SO₄²⁻, oxyanions with more oxygen giving the “-ate” ending, so the suffix encodes composition.'),
        ('Explain how the formula of a hydrated salt such as CuSO₄·5H₂O is interpreted.', 'Each formula unit of copper(II) sulfate is associated with five molecules of water of crystallisation in the lattice; the dot indicates water bound in the crystal, not a covalent bond.')],
    'contrast': [('sulfite', 'sulfate', 'Sulfite is SO₃²⁻ and sulfate is SO₄²⁻: both 2− but sulfate contains one more oxygen atom.'),
                 ('nitrite', 'nitrate', 'Nitrite is NO₂⁻ and nitrate is NO₃⁻; the “-ate” ion has more oxygen.'),
                 ('iron(II) chloride', 'iron(III) chloride', 'Iron(II) chloride, FeCl₂, contains Fe²⁺; iron(III) chloride, FeCl₃, contains Fe³⁺ – the Roman numeral gives the charge.')],
    'misc': R.f['ch06-st2'].misc + [('The formula of calcium nitrate is CaNO₃₂.', 'Brackets are essential around a polyatomic ion that appears more than once: Ca(NO₃)₂.'),
                                    ('Copper(II) oxide has the formula Cu₂O because of the “II”.', 'The (II) shows the charge 2+: one Cu²⁺ balances one O²⁻, so the formula is CuO; Cu₂O is copper(I) oxide.')],
    'evaluate': R.f['ch06-st2'].evaluate + [('Memorising the formulae of polyatomic ions is unnecessary because they can be looked up.', ['data booklets and references are always available in practice', 'understanding charge balance matters more'], ['fluency speeds up all stoichiometry and equation writing', 'recognising ions is needed to interpret names, labels and experimental observations'], 'Knowing the common ions is an essential working vocabulary even if reference sources exist.')],
    'extended': [('A fertiliser label lists “ammonium phosphate” and “potassium nitrate”. (a) Write the formula of each compound. (b) Calculate the percentage by mass of nitrogen in each. (c) Suggest which is the better source of nitrogen per kilogram.', '(a) (NH₄)₃PO₄ and KNO₃. (b) (NH₄)₃PO₄: 3 × 14.01/149.12 × 100 = 28.2 %; KNO₃: 14.01/101.11 × 100 = 13.9 %. (c) ammonium phosphate – about twice the nitrogen content per kg (and it also supplies phosphorus).', 6, 'multi_step')]}))


@R.add('ch06-st2', 'C4', (3, 5), 'multi_step')
def c4_ions_in_salt(rng, slot):
    cat = pick(rng, [c for c in CATIONS if c[1] not in ('NH4',)])
    an = pick(rng, [a for a in ANIONS if a[1] in POLY and a[1] not in ('CH3COO',)])
    f = ionic_formula(cat, an)
    M = mr(f)
    m = rng.choice([1.00, 2.50, 5.00, 10.0])
    a = atoms(f)
    O = a.get('O', 0)
    g = math.gcd(cat[2], an[2])
    ncat, nan = an[2] // g, cat[2] // g
    n = m / M
    stem = (f'(a) Write the formula of {cat[0]} {an[0]}. (b) Calculate its molar mass. (c) Calculate the total amount of ions, in mol, in {m:.2f} g of the compound. '
            f'(d) Calculate the number of oxygen atoms in this sample.')
    return num(stem, f'(a) {chem(f)}; (b) {M:.2f} g mol⁻¹; (c) {q(n * (ncat + nan), "mol")}; (d) {sf(n * O * NA)}',
               f'(a) {chem(f)} (A1). (b) {M:.2f} g mol⁻¹ (A1). (c) n = {m:.2f}/{M:.2f} = {sf(n)} mol; × {ncat + nan} ions (M1) = {q(n * (ncat + nan), "mol")} (A1). (d) × {O} O atoms × NA = {sf(n * O * NA)} (A1).', 5, 'multi_step')


R.mcqs('ch06-st2', 'C2', (1, 4), [
    ('Which pair of names and formulae is correct?', 'sodium sulfite, Na₂SO₃', ['sodium sulfide, Na₂SO₄', 'sodium sulfate, NaSO₄', 'sodium sulfite, NaSO₃'], 'Sulfite SO₃²⁻ needs two Na⁺.'),
    ('Which ion has a 3− charge?', 'phosphate', ['nitrate', 'carbonate', 'hydrogensulfate'], 'PO₄³⁻.'),
    ('What is the name of NH₄HCO₃?', 'ammonium hydrogencarbonate', ['ammonia carbonate', 'ammonium carbonate', 'nitrogen hydrogen carbonate'], 'NH₄⁺ and HCO₃⁻.'),
])


R.facts('ch06-st3', F(**{**R.f['ch06-st3'].__dict__,
    'evaluate': R.f['ch06-st3'].evaluate + [
        ('The ionic model fully explains the properties of all compounds of metals with non-metals.', ['explains high melting points, brittleness and conductivity when molten for NaCl, MgO', 'lattice enthalpy trends follow charge and radius'], ['AlCl₃ sublimes at 180 °C and exists as Al₂Cl₆ molecules – covalent character', 'experimental lattice enthalpies differ from purely ionic theoretical values when polarisation occurs (e.g. AgCl)', 'some metal–non-metal compounds are semiconductors'], 'The ionic model works for compounds with a large electronegativity difference but must be extended for polarising cations and polarisable anions.')],
    'extended': [('Sodium chloride (mp 801 °C), magnesium oxide (mp 2852 °C) and calcium oxide (mp 2613 °C) are all ionic. (a) Explain the order of melting points. (b) Explain why magnesium oxide is used to line furnaces. (c) Suggest why magnesium oxide is insoluble in water while sodium chloride dissolves.', '(a) MgO and CaO: 2+/2− ions, much stronger attraction than 1+/1− in NaCl; Mg²⁺ smaller than Ca²⁺ so MgO > CaO. (b) Very high melting point, thermally stable, electrical insulator when solid. (c) MgO lattice enthalpy (3791 kJ mol⁻¹) is so large that hydration of the ions cannot compensate; NaCl lattice enthalpy is smaller.', 6, 'multi_step'),
                 ('Design an experiment to show that a white solid is ionic. Describe the tests, the expected observations and the reasoning.', 'Test melting point (high, e.g. > 500 °C); test conductivity of solid (none), molten or aqueous (conducts – ions mobile); solubility in water vs hexane (dissolves in water); electrolysis of molten/aqueous sample gives products at electrodes. Together these indicate a giant ionic lattice.', 6, 'multi_step')]}))


@R.add('ch06-st3', 'C3', (1, 5), 'short')
def c3_mp_compare(rng, slot):
    a, b = rng.sample(LATT, 2)
    if abs(a[7] - b[7]) < 40:
        return None
    hi, lo = (a, b) if a[7] > b[7] else (b, a)
    frame = rng.randrange(3)
    if frame == 0:
        stem = f'Predict which of {chem(a[0])} and {chem(b[0])} has the higher melting point, giving a reason.'
    elif frame == 1:
        stem = f'Using ionic charges and radii, deduce whether {chem(a[0])} or {chem(b[0])} has the greater lattice enthalpy.'
    else:
        stem = f'The ionic radii are: {a[1]} ion {a[5]} pm, {a[2]} ion {a[6]} pm, {b[1]} ion {b[5]} pm, {b[2]} ion {b[6]} pm. Suggest which of {chem(a[0])} and {chem(b[0])} has the stronger ionic bonding.'
    ans = f'{chem(hi[0])}: ' + ('higher charges on the ions' if hi[3] * hi[4] > lo[3] * lo[4] else 'smaller ions (shorter distance between ion centres)') + f' (lattice enthalpies {hi[7]} vs {lo[7]} kJ mol⁻¹).'
    return dict(stem=stem, answer=ans, markingKey=f'{chem(hi[0])} (1); reason in terms of ionic charge/radius and strength of electrostatic attraction (1).', type='short', marks=2)


@R.add('ch06-st3', 'C3', (2, 5), 'mcq')
def c3_conduct(rng, slot):
    comp = pick(rng, ['sodium chloride', 'potassium bromide', 'calcium chloride', 'magnesium sulfate', 'lithium fluoride', 'copper(II) sulfate', 'sodium iodide'])
    cond = [('solid', False), ('molten', True), ('dissolved in water', True), ('dissolved in hexane (if it were possible)', False)]
    st_, yes = pick(rng, cond[:3])
    stem = f'Which statement about {comp} {st_} is correct?'
    if yes:
        right = 'It conducts because its ions are free to move.'
        wr = ['It conducts because it has delocalised electrons.', 'It does not conduct because its ions are fixed in a lattice.', 'It does not conduct because it contains no charged particles.']
    else:
        right = 'It does not conduct because its ions are fixed in position.'
        wr = ['It conducts because it contains ions.', 'It conducts because electrons move through the lattice.', 'It does not conduct because it contains no ions.']
    return mcq(rng, stem, right, wr, 'Conduction requires mobile charged particles; ionic compounds conduct only when molten or in solution.')


@R.add('ch06-st3', 'C4', (3, 5), 'multi_step')
def c4_latt_data(rng, slot):
    group = pick(rng, [[l for l in LATT if l[1] == 'Na'], [l for l in LATT if l[1] == 'K'], [l for l in LATT if l[2] == 'O'], [l for l in LATT if l[2] == 'Cl' and l[3] == 1]])
    if len(group) < 3:
        return None
    pts = sorted(group, key=lambda l: l[5] + l[6])
    tab = '\n'.join(f'{chem(l[0])} | {l[5] + l[6]} | {l[7]}' for l in pts)
    stem = (f'The table shows the sum of ionic radii and the lattice enthalpy for several compounds.\n\ncompound | r(cation) + r(anion) / pm | lattice enthalpy / kJ mol⁻¹\n{tab}\n\n'
            f'(a) Describe the trend shown. (b) Explain the trend in terms of electrostatic attraction. (c) Predict, with a reason, how the lattice enthalpy of a compound with ions of double the charge but the same radii would compare.')
    return num(stem, '(a) lattice enthalpy decreases as the sum of radii increases; (c) roughly four times larger', '(a) larger distance → smaller lattice enthalpy (A1). (b) force ∝ product of charges / distance; ions further apart attract less strongly, less energy needed to separate (R1 R1). (c) charge product ×4, so roughly four times larger (e.g. MgO vs NaF) (R1).', 4, 'multi_step')


# =============================================================================================
# ch07 S2.2 The covalent model
# =============================================================================================
# formula, name, central atom, electron domains, lone pairs on central, molecular geometry, angle, polar (None = ion),
# sigma, pi, hybridisation of central atom, bonding pairs (shared pairs), total lone pairs, HL-only
MOLS = [
    ('CH4', 'methane', 'C', 4, 0, 'tetrahedral', '109.5°', False, 4, 0, 'sp³', 4, 0, False),
    ('NH3', 'ammonia', 'N', 4, 1, 'trigonal pyramidal', '107°', True, 3, 0, 'sp³', 3, 1, False),
    ('H2O', 'water', 'O', 4, 2, 'bent (V-shaped)', '104.5°', True, 2, 0, 'sp³', 2, 2, False),
    ('CO2', 'carbon dioxide', 'C', 2, 0, 'linear', '180°', False, 2, 2, 'sp', 4, 4, False),
    ('BF3', 'boron trifluoride', 'B', 3, 0, 'trigonal planar', '120°', False, 3, 0, 'sp²', 3, 9, False),
    ('HCN', 'hydrogen cyanide', 'C', 2, 0, 'linear', '180°', True, 2, 2, 'sp', 4, 1, False),
    ('C2H4', 'ethene (each C)', 'C', 3, 0, 'trigonal planar', '120°', False, 5, 1, 'sp²', 6, 0, False),
    ('C2H2', 'ethyne (each C)', 'C', 2, 0, 'linear', '180°', False, 3, 2, 'sp', 5, 0, False),
    ('CCl4', 'tetrachloromethane', 'C', 4, 0, 'tetrahedral', '109.5°', False, 4, 0, 'sp³', 4, 12, False),
    ('CHCl3', 'trichloromethane', 'C', 4, 0, 'tetrahedral', '109.5° (approximately)', True, 4, 0, 'sp³', 4, 9, False),
    ('PCl3', 'phosphorus trichloride', 'P', 4, 1, 'trigonal pyramidal', 'about 100° (less than 109.5°)', True, 3, 0, 'sp³', 3, 10, False),
    ('O3', 'ozone', 'O', 3, 1, 'bent (V-shaped)', 'about 117° (less than 120°)', True, 2, 1, 'sp²', 3, 6, False),
    ('HCHO', 'methanal', 'C', 3, 0, 'trigonal planar', '120° (approximately)', True, 3, 1, 'sp²', 4, 2, False),
    ('NO3^-', 'the nitrate ion', 'N', 3, 0, 'trigonal planar', '120°', None, 3, 1, 'sp²', 4, 8, False),
    ('CO3^2-', 'the carbonate ion', 'C', 3, 0, 'trigonal planar', '120°', None, 3, 1, 'sp²', 4, 8, False),
    ('BeCl2', 'beryllium chloride (gas)', 'Be', 2, 0, 'linear', '180°', False, 2, 0, 'sp', 2, 6, False),
    ('SiH4', 'silane', 'Si', 4, 0, 'tetrahedral', '109.5°', False, 4, 0, 'sp³', 4, 0, False),
    ('NH4^+', 'the ammonium ion', 'N', 4, 0, 'tetrahedral', '109.5°', None, 4, 0, 'sp³', 4, 0, False),
    ('H3O^+', 'the oxonium ion', 'O', 4, 1, 'trigonal pyramidal', '107°', None, 3, 0, 'sp³', 3, 1, False),
    ('NO2^-', 'the nitrite ion', 'N', 3, 1, 'bent (V-shaped)', 'about 115° (less than 120°)', None, 2, 1, 'sp²', 3, 6, False),
    ('SO2', 'sulfur dioxide', 'S', 3, 1, 'bent (V-shaped)', 'about 117° (less than 120°)', True, None, None, 'sp²', None, None, False),
    ('NCl3', 'nitrogen trichloride', 'N', 4, 1, 'trigonal pyramidal', 'about 107°', True, 3, 0, 'sp³', 3, 10, False),
    ('OF2', 'oxygen difluoride', 'O', 4, 2, 'bent (V-shaped)', 'about 104.5°', True, 2, 0, 'sp³', 2, 8, False),
    ('PCl5', 'phosphorus pentachloride', 'P', 5, 0, 'trigonal bipyramidal', '90° and 120°', False, 5, 0, None, 5, 15, True),
    ('SF6', 'sulfur hexafluoride', 'S', 6, 0, 'octahedral', '90°', False, 6, 0, None, 6, 18, True),
    ('SF4', 'sulfur tetrafluoride', 'S', 5, 1, 'see-saw', 'about 87° and 102° (less than 90° and 120°)', True, 4, 0, None, 4, 13, True),
    ('ClF3', 'chlorine trifluoride', 'Cl', 5, 2, 'T-shaped', 'about 87° (less than 90°)', True, 3, 0, None, 3, 11, True),
    ('XeF4', 'xenon tetrafluoride', 'Xe', 6, 2, 'square planar', '90°', False, 4, 0, None, 4, 14, True),
    ('XeF2', 'xenon difluoride', 'Xe', 5, 3, 'linear', '180°', False, 2, 0, None, 2, 9, True),
    ('BrF5', 'bromine pentafluoride', 'Br', 6, 1, 'square pyramidal', 'about 85° (less than 90°)', True, 5, 0, None, 5, 16, True),
    ('I3^-', 'the triiodide ion', 'I', 5, 3, 'linear', '180°', None, 2, 0, None, 2, 9, True),
]
EDG = {2: 'linear', 3: 'trigonal planar', 4: 'tetrahedral', 5: 'trigonal bipyramidal', 6: 'octahedral'}


def mf(m):
    return chem(m[0])


R.facts('ch07-st1', F(
    terms=[('covalent bond', 'the electrostatic attraction between a shared pair of electrons and the positively charged nuclei of the two bonded atoms'),
           ('Lewis formula', 'a diagram showing all the valence electrons in a molecule or ion as bonding pairs (lines or dots) and lone pairs'),
           ('lone pair', 'a pair of valence electrons on an atom that is not involved in bonding'),
           ('coordination bond', 'a covalent bond in which both shared electrons are provided by the same atom'),
           ('octet rule', 'the tendency of atoms to gain, lose or share electrons until they have eight electrons in their outer (valence) shell'),
           ('bond length', 'the average distance between the nuclei of two bonded atoms')],
    facts=[('Which molecule contains a triple bond?', 'N₂', ['O₂', 'CO₂', 'C₂H₄'], 'N≡N.'),
           ('Which species contains a coordination bond?', 'NH₄⁺', ['NH₃', 'CH₄', 'H₂O'], 'N lone pair donated to H⁺.'),
           ('Which molecule has an incomplete octet on its central atom?', 'BF₃', ['NH₃', 'CF₄', 'H₂O'], 'B has only six valence electrons in BF₃.'),
           ('How do bond length and bond strength change from C–C to C=C to C≡C?', 'length decreases, strength increases', ['length increases, strength increases', 'length decreases, strength decreases', 'both stay the same'], 'More shared electrons pull the nuclei closer and hold them more strongly.'),
           ('Which molecule exceeds the octet on its central atom?', 'SF₆', ['CCl₄', 'NH₃', 'BCl₃'], 'S has 12 electrons in SF₆ (expanded octet, period 3).'),
           ('How many electrons are shared in a double bond?', '4', ['2', '6', '8'], 'Two pairs.')],
    why=[('Explain why a covalent bond holds two atoms together.', 'Both nuclei are attracted electrostatically to the shared pair of electrons located between them; this attraction outweighs the repulsion between the nuclei.'),
         ('Explain why a C≡C triple bond is shorter than a C=C double bond.', 'Six shared electrons between the nuclei produce a greater electron density and stronger attraction, pulling the nuclei closer together.'),
         ('Explain how a coordination bond forms in the oxonium ion, H₃O⁺.', 'A lone pair on the oxygen of H₂O is donated into the empty orbital of an H⁺ ion; once formed, the coordination bond is identical to the other O–H bonds.'),
         ('Explain why elements in period 3 can expand their octet but elements in period 2 cannot.', 'Period 3 atoms are larger and can accommodate more than four electron domains around them (traditionally explained by available 3d orbitals); period 2 atoms have only 2s and 2p orbitals, so at most 8 valence electrons.')],
    contrast=[('a covalent bond', 'a coordination bond', 'In an ordinary covalent bond each atom contributes one electron to the shared pair; in a coordination bond both electrons come from one atom – once formed they are indistinguishable.'),
              ('a bonding pair', 'a lone pair', 'A bonding pair is shared between two atoms; a lone pair belongs to one atom and is not used in bonding.')],
    misc=[('A double bond is twice as strong as a single bond.', 'A C=C bond (614 kJ mol⁻¹) is less than twice a C–C bond (346 kJ mol⁻¹) because the second (π) bond is weaker than the σ bond.'),
          ('All molecules obey the octet rule.', 'Exceptions include incomplete octets (BF₃, BeCl₂), expanded octets (PCl₅, SF₆) and odd-electron species (NO, NO₂).')],
    evaluate=[('Lewis formulae are an adequate model of bonding in molecules.', ['predict bonding and lone pairs, used for VSEPR shapes', 'explain octets and coordination bonds'], ['cannot represent resonance/delocalisation with a single structure', 'say nothing about orbitals, bond energies or magnetism (O₂ is paramagnetic)', 'fail for electron-deficient species'], 'A powerful first model whose limitations are addressed by resonance and orbital (σ/π, hybridisation) models.')],
    extended=[('Hydrazine, N₂H₄, is used as a rocket fuel. (a) Draw its Lewis formula. (b) State the number of bonding pairs and lone pairs. (c) Predict the H–N–H bond angle and explain it. (d) Explain why hydrazine is a liquid at room temperature while ethane (similar Mr) is a gas.', '(a) H₂N–NH₂ with one lone pair on each N. (b) 5 bonding pairs, 2 lone pairs. (c) about 107°: four electron domains (tetrahedral), lone pair repels more strongly. (d) hydrazine forms hydrogen bonds (N–H…N); ethane has only London forces.', 6, 'multi_step')],
))

SIMPLE = [('N2', 'nitrogen', 3, 2), ('Cl2', 'chlorine', 1, 6), ('HCl', 'hydrogen chloride', 1, 3), ('O2', 'oxygen', 2, 4), ('H2O2', 'hydrogen peroxide', 3, 4),
          ('N2H4', 'hydrazine', 5, 2), ('C2H6', 'ethane', 7, 0), ('CH3OH', 'methanol', 5, 2), ('HF', 'hydrogen fluoride', 1, 3), ('F2', 'fluorine', 1, 6)]


@R.add('ch07-st1', 'C3', (1, 5), 'short')
def c3_pairs(rng, slot):
    pool = [(m[0], m[1], m[11], m[12]) for m in MOLS if m[11] is not None and not m[13]] + SIMPLE
    f, nm, bp, lp = pick(rng, pool)
    nm2 = nm.split(' (')[0]
    frame = rng.randrange(3)
    if frame == 0:
        stem = f'Draw the Lewis formula of {nm2} ({chem(f)}) and state the number of bonding pairs and lone pairs it contains.'
    elif frame == 1:
        stem = f'Deduce the total number of shared (bonding) electron pairs and non-bonding (lone) pairs in {chem(f)}.'
    else:
        stem = f'How many lone pairs are there in total in one {"ion" if "^" in f else "molecule"} of {chem(f)}, and how many bonding pairs?'
    return dict(stem=stem, answer=f'{bp} bonding pairs, {lp} lone pairs', markingKey=f'Correct Lewis formula with all valence electrons (1); {bp} bonding pairs (1); {lp} lone pairs (1).', type='short', marks=3 if frame == 0 else 2)


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def c3_pairs_mcq(rng, slot):
    pool = [(m[0], m[11], m[12]) for m in MOLS if m[11] is not None and not m[13]] + [(s[0], s[2], s[3]) for s in SIMPLE]
    f, bp, lp = pick(rng, pool)
    right = f'{bp} bonding pairs and {lp} lone pairs'
    wr = [f'{lp} bonding pairs and {bp} lone pairs', f'{bp} bonding pairs and {lp + rng.choice([1, 2])} lone pairs', f'{bp * 2} bonding pairs and {lp} lone pairs', f'{bp} bonding pairs and {max(0, lp - 1)} lone pairs']
    wr = [w for w in dict.fromkeys(wr) if w != right]
    return mcq(rng, f'How many bonding pairs and lone pairs of electrons are in the Lewis formula of {chem(f)}?', right, wr[:3], f'{chem(f)}: {bp} shared pairs and {lp} non-bonding pairs.')


COORD = [('NH4^+', 'N of NH₃ donates its lone pair to H⁺'), ('H3O^+', 'O of H₂O donates a lone pair to H⁺'), ('CO', 'O donates a lone pair to C, giving C≡O with one coordination bond'),
         ('Al2Cl6', 'a Cl lone pair on each AlCl₃ unit is donated to the electron-deficient Al of the other unit (two coordination bonds)'),
         ('H3NBF3', 'the N lone pair of NH₃ is donated to the empty orbital of B in BF₃'), ('[Cu(H2O)6]^2+', 'each water oxygen donates a lone pair to Cu²⁺ (six coordination bonds)')]


@R.add('ch07-st1', 'C2', (2, 4), 'explain')
def c2_coord(rng, slot):
    f, why = pick(rng, COORD)
    stem = pick(rng, [f'Explain how a coordination bond forms in {chem(f)}.', f'Identify the coordination bond(s) in {chem(f)} and explain which atom provides the electrons.'])
    return dict(stem=stem, answer=why[0].upper() + why[1:] + '.', markingKey=f'{why} (1); both electrons of the shared pair come from the donor atom (1).', type='explain', marks=2)


R.mcqs('ch07-st1', 'C2', (1, 4), [
    ('Which bond is the longest?', 'C–C in ethane', ['C=C in ethene', 'C≡C in ethyne', 'C–C in benzene'], 'Single bonds are longest; benzene has bond order 1.5.'),
    ('How many valence electrons are shown in the Lewis formula of CO₂?', '16', ['12', '8', '22'], '4 + 2 × 6.'),
    ('Which statement about a coordination bond is correct?', 'Both electrons are donated by one atom.', ['It is weaker than other covalent bonds.', 'It is an ionic bond.', 'It forms only between metals.'], 'Definition.'),
    ('Which species has a central atom with only six valence electrons?', 'BCl₃', ['PCl₃', 'NCl₃', 'CCl₄'], 'B: 3 bonding pairs, no lone pairs.'),
])


R.facts('ch07-st2', F(
    terms=[('VSEPR theory', 'the model in which electron domains around a central atom repel one another and arrange themselves as far apart as possible, determining the shape of a molecule'),
           ('electron domain', 'a region of electron density around a central atom: a lone pair, a single bond or a multiple bond each count as one domain'),
           ('electron domain geometry', 'the arrangement of all electron domains (bonding and non-bonding) around a central atom'),
           ('molecular geometry', 'the arrangement of the atoms in a molecule, determined by the positions of the bonding domains only')],
    facts=[('What is the shape of a molecule with four bonding domains and no lone pairs on the central atom?', 'tetrahedral', ['square planar', 'trigonal pyramidal', 'bent'], 'Four domains as far apart as possible: 109.5°.'),
           ('Why is the H–O–H bond angle in water smaller than 109.5°?', 'Lone pairs repel more strongly than bonding pairs.', ['Water is polar.', 'Hydrogen bonds pull the hydrogens together.', 'Oxygen is very electronegative.'], 'LP–LP > LP–BP > BP–BP repulsion.'),
           ('How many electron domains does the carbon atom in CO₂ have?', '2', ['4', '3', '0'], 'Each double bond counts as one domain.'),
           ('What is the bond angle in a trigonal planar molecule?', '120°', ['109.5°', '90°', '180°'], '360°/3.')],
    why=[('Explain why the bond angle in ammonia (107°) is less than that in methane (109.5°).', 'Both have four electron domains in a tetrahedral arrangement, but in NH₃ one is a lone pair; lone pairs are closer to the nucleus and repel bonding pairs more strongly, pushing the N–H bonds closer together.'),
         ('Explain why carbon dioxide is linear.', 'The central carbon has two electron domains (two C=O double bonds) and no lone pairs; these repel to be as far apart as possible, at 180°.'),
         ('Explain why a multiple bond counts as a single electron domain in VSEPR theory.', 'All the electrons of a double or triple bond are located in the same region between the two atoms, so they act as one region of electron density.')],
    contrast=[('electron domain geometry', 'molecular geometry', 'Electron domain geometry includes all domains (bonds and lone pairs); molecular geometry describes only the positions of the atoms – they differ when lone pairs are present (e.g. NH₃: tetrahedral vs trigonal pyramidal).')],
    misc=[('Water is linear because it has only two bonds.', 'Water has four electron domains (two bonds, two lone pairs) in a tetrahedral arrangement; the molecule is bent (104.5°).'),
          ('A double bond counts as two electron domains.', 'A double bond is one electron domain; e.g. CO₂ has two domains and is linear.')],
    evaluate=[('VSEPR theory reliably predicts the shapes of all molecules.', ['correct for most main-group molecules', 'simple to apply from Lewis formulae', 'explains bond-angle reductions due to lone pairs'], ['does not give exact angles (e.g. H₂S 92°)', 'less reliable for transition metal complexes', 'treats domains qualitatively; orbital models are needed for bonding energies'], 'VSEPR is an excellent predictive tool for main-group shapes but is approximate and has limited scope.')],
))


@R.add('ch07-st2', 'C3', (1, 5), 'short')
def c3_vsepr(rng, slot):
    pool = [m for m in MOLS if (not m[13]) or slot.d >= 4]
    m = pick(rng, pool)
    hl = ' (HL)' if m[13] else ''
    frame = rng.randrange(3)
    nm = m[1].split(' (')[0]
    if frame == 0:
        stem = f'Deduce the electron domain geometry and the molecular geometry of {nm}, {mf(m)}, and predict its bond angle.{hl}'
        ans = f'electron domains {m[3]} ({EDG[m[3]]}); molecular geometry {m[5]}; angle {m[6]}'
        key = f'{m[3]} electron domains on {m[2]} ({m[3] - m[4]} bonding, {m[4]} lone) (1); {EDG[m[3]]} domain geometry (1); {m[5]}, {m[6]} (1).'
        return dict(stem=stem, answer=ans, markingKey=key, type='short', marks=3)
    if frame == 1:
        stem = f'Using VSEPR theory, predict the shape of {mf(m)} and explain your answer.{hl}'
        ans = f'{m[5]}: {m[3] - m[4]} bonding domain(s) and {m[4]} lone pair(s) around {m[2]} repel to be as far apart as possible.'
        return dict(stem=stem, answer=ans, markingKey=f'{m[5]} (1); {m[3]} domains around the central atom, including {m[4]} lone pair(s) (1); domains repel to minimise repulsion{"; lone pairs repel more strongly" if m[4] else ""} (1).', type='explain', marks=3)
    stem = f'State the number of electron domains around the central atom in {mf(m)} and the {"ion" if "^" in m[0] else "molecule"}\'s shape.{hl}'
    return dict(stem=stem, answer=f'{m[3]}; {m[5]}', markingKey=f'{m[3]} (1); {m[5]} (1).', type='short', marks=2)


@R.add('ch07-st2', 'C3', (1, 4), 'mcq')
def c3_vsepr_mcq(rng, slot):
    pool = [m for m in MOLS if (not m[13]) or slot.d >= 4]
    m = pick(rng, pool)
    kind = rng.choice(['shape', 'angle'])
    if kind == 'shape':
        shapes = sorted({x[5] for x in MOLS if x[5] != m[5]})
        wr = rng.sample(shapes, 3)
        if m[4] and EDG[m[3]] not in wr and EDG[m[3]] != m[5]:
            wr[0] = EDG[m[3]]
        return mcq(rng, f'What is the molecular geometry of {mf(m)}?', m[5], wr, f'{m[3]} domains ({m[4]} lone pairs) → {m[5]}.')
    angles = ['180°', '120°', '109.5°', '107°', '104.5°', '90°']
    a = m[6].split(' ')[0] if m[6].split(' ')[0] in angles else None
    if not a:
        return None
    wr = rng.sample([x for x in angles if x != a], 3)
    return mcq(rng, f'What is the approximate bond angle in {mf(m)}?', a, wr, f'{m[5]}: {m[6]}.')


R.mcqs('ch07-st2', 'C2', (1, 4), [
    ('Which molecule has the smallest bond angle?', 'H₂O', ['NH₃', 'CH₄', 'BF₃'], 'Two lone pairs: 104.5°.'),
    ('Which pair has the same molecular geometry?', 'NH₃ and PCl₃', ['NH₃ and BF₃', 'H₂O and CO₂', 'CH₄ and XeF₄'], 'Both trigonal pyramidal.'),
    ('Which species is trigonal planar?', 'CO₃²⁻', ['NH₃', 'SO₃²⁻', 'ClO₃⁻'], 'Three domains, no lone pairs on C.'),
    ('What is the electron domain geometry of SF₄? (HL)', 'trigonal bipyramidal', ['tetrahedral', 'see-saw', 'square planar'], 'Five domains: 4 bonding + 1 lone.'),
])


@R.add('ch07-st2', 'C4', (3, 5), 'multi_step')
def c4_vsepr_compare(rng, slot):
    a, b = rng.sample([m for m in MOLS if m[3] == 4 and m[7] is not None or m[0] in ('BF3', 'CO2')], 2)
    if a[5] == b[5]:
        return None
    stem = (f'Compare the shapes and bond angles of {mf(a)} and {mf(b)}. In your answer (a) state the number of bonding and non-bonding domains on each central atom, '
            f'(b) deduce each molecular geometry and bond angle, and (c) explain the difference in bond angle.')
    ans = f'{mf(a)}: {a[3] - a[4]} bonding, {a[4]} lone; {a[5]}, {a[6]}. {mf(b)}: {b[3] - b[4]} bonding, {b[4]} lone; {b[5]}, {b[6]}.'
    return num(stem, ans, f'(a) domain counts for both (A1 A1). (b) geometries and angles (A1 A1). (c) different numbers of domains and/or lone pairs; lone pairs repel more than bonding pairs, compressing angles (R1).', 5, 'multi_step')


R.facts('ch07-st3', F(
    terms=[('electronegativity', 'the relative ability of an atom to attract a shared pair of electrons in a covalent bond'),
           ('polar covalent bond', 'a covalent bond in which the electrons are shared unequally because the atoms differ in electronegativity, giving partial charges δ+ and δ−'),
           ('bond dipole', 'the separation of partial charges along a polar bond, shown with an arrow pointing towards the more electronegative atom'),
           ('polar molecule', 'a molecule with a net dipole moment because its bond dipoles do not cancel, owing to its shape')],
    facts=[('Which element has the highest electronegativity?', 'fluorine', ['oxygen', 'chlorine', 'caesium'], 'F = 4.0 on the Pauling scale.'),
           ('Why is CO₂ non-polar even though its C=O bonds are polar?', 'The linear shape makes the bond dipoles cancel.', ['C and O have the same electronegativity.', 'CO₂ is a gas.', 'The double bonds are non-polar.'], 'Symmetry.'),
           ('Which molecule is polar?', 'CHCl₃', ['CCl₄', 'BF₃', 'CO₂'], 'Unsymmetrical distribution of dipoles.'),
           ('How does electronegativity change across a period?', 'It increases.', ['It decreases.', 'It stays the same.', 'It increases then decreases.'], 'Greater nuclear charge, smaller radius.')],
    why=[('Explain why electronegativity increases across period 3.', 'Nuclear charge increases while electrons are added to the same shell, so shielding is similar; the atomic radius decreases and the bonding pair is attracted more strongly.'),
         ('Explain why water is a polar molecule.', 'The O–H bonds are polar (O more electronegative), and the bent shape means the bond dipoles do not cancel, giving a net dipole with δ− on O.'),
         ('Explain why tetrachloromethane is non-polar although each C–Cl bond is polar.', 'The four identical C–Cl dipoles are arranged tetrahedrally and symmetrically, so they cancel and there is no net dipole.')],
    contrast=[('a polar bond', 'a polar molecule', 'A polar bond has unequal sharing of electrons between two atoms; a polar molecule has a net dipole, which requires polar bonds arranged unsymmetrically.')],
    misc=[('Any molecule containing polar bonds is a polar molecule.', 'Polar bonds can cancel in symmetrical molecules (CO₂, BF₃, CCl₄), giving non-polar molecules.'),
          ('In a C–Cl bond the carbon atom carries a partial negative charge.', 'Chlorine (3.2) is more electronegative than carbon (2.6), so Cl is δ− and C is δ+.')],
    evaluate=[('Electronegativity values can be used to classify every bond sharply as ionic or covalent.', ['large differences (> 1.8) suggest ionic, small differences covalent', 'simple, data-booklet based'], ['bonding is a continuum with no sharp boundary', 'values are relative and derived empirically', 'other factors (polarisation, structure) matter; e.g. HF has ΔEN 1.8 but is covalent'], 'Electronegativity difference indicates the degree of polarity/ionic character on a continuum rather than a strict classification.')],
))

ENPAIRS = [('H', 'Cl'), ('H', 'F'), ('C', 'O'), ('C', 'Cl'), ('N', 'H'), ('O', 'H'), ('C', 'H'), ('Si', 'O'), ('P', 'Cl'), ('S', 'O'),
           ('C', 'F'), ('B', 'F'), ('H', 'Br'), ('C', 'N'), ('N', 'O'), ('Al', 'Cl'), ('Na', 'Cl'), ('Mg', 'O'), ('H', 'I'), ('C', 'Br'), ('S', 'H'), ('Cl', 'F')]


@R.add('ch07-st3', 'C3', (1, 4), 'mcq')
def c3_most_polar(rng, slot):
    pool = rng.sample([p for p in ENPAIRS if p[0] in EN and p[1] in EN], 4)
    d = [abs(EN[a] - EN[b]) for a, b in pool]
    if len(set(round(x, 1) for x in d)) < 4:
        return None
    hi = rng.random() < 0.6
    i = d.index(max(d) if hi else min(d))
    lab = [f'{a}–{b}' for a, b in pool]
    return mcq(rng, f'Which bond is the {"most" if hi else "least"} polar?', lab[i], [x for j, x in enumerate(lab) if j != i],
               'Electronegativity differences: ' + ', '.join(f'{l} {x:.1f}' for l, x in zip(lab, d)) + '.')


@R.add('ch07-st3', 'C3', (1, 5), 'short')
def c3_partial(rng, slot):
    a, b = pick(rng, [p for p in ENPAIRS if EN[p[0]] != EN[p[1]]])
    d = abs(EN[a] - EN[b])
    neg = a if EN[a] > EN[b] else b
    pos = b if neg == a else a
    kind = 'predominantly ionic' if d > 1.8 else 'polar covalent' if d > 0.4 else 'essentially non-polar covalent'
    stem = pick(rng, [f'Using electronegativity values (data booklet), state which atom carries the partial negative charge in a {a}–{b} bond and classify the bond.',
                      f'Calculate the electronegativity difference for the {a}–{b} bond and indicate the bond dipole.'])
    return dict(stem=stem, answer=f'ΔEN = |{EN[a]} − {EN[b]}| = {d:.1f}; {neg} is δ−, {pos} is δ+; {kind}.', markingKey=f'ΔEN = {d:.1f} (1); δ− on {neg} (more electronegative) (1); {kind} (1).', type='short', marks=3 if slot.d >= 3 else 2)


@R.add('ch07-st3', 'C3', (1, 4), 'mcq')
def c3_polar_molecule(rng, slot):
    pol = [m for m in MOLS if m[7] is True]
    non = [m for m in MOLS if m[7] is False]
    if rng.random() < 0.5:
        r = pick(rng, pol)
        w = rng.sample(non, 3)
        stem = 'Which molecule is polar?'
    else:
        r = pick(rng, non)
        w = rng.sample(pol, 3)
        stem = 'Which molecule is non-polar?'
    return mcq(rng, stem, mf(r), [mf(x) for x in w], f'{mf(r)} is {r[5]}; ' + ('bond dipoles do not cancel.' if r[7] else 'symmetrical shape, bond dipoles cancel.'))


@R.add('ch07-st3', 'C2', (2, 4), 'explain')
def c2_polarity_explain(rng, slot):
    m = pick(rng, [x for x in MOLS if x[7] is not None])
    stem = pick(rng, [f'Explain whether {mf(m)} is a polar or a non-polar molecule.', f'Deduce, with reference to its shape, whether {m[1].split(" (")[0]} ({mf(m)}) has a net dipole moment.'])
    ans = f'{"Polar" if m[7] else "Non-polar"}: the bonds are polar, and the {m[5]} shape means the bond dipoles {"do not cancel" if m[7] else "cancel"}.'
    return dict(stem=stem, answer=ans, markingKey=f'Bonds are polar (electronegativity difference) (1); shape {m[5]} (1); dipoles {"do not cancel – polar" if m[7] else "cancel – non-polar"} (1).', type='explain', marks=3)


R.mcqs('ch07-st3', 'C2', (1, 4), [
    ('Which list shows increasing bond polarity?', 'C–H < N–H < O–H < F–H', ['F–H < O–H < N–H < C–H', 'O–H < C–H < F–H < N–H', 'N–H < C–H < F–H < O–H'], 'ΔEN 0.4, 0.8, 1.2, 1.8.'),
    ('Which molecule has polar bonds but is non-polar overall?', 'BF₃', ['NH₃', 'HCl', 'H₂O'], 'Trigonal planar symmetry.'),
    ('A charged rod deflects a stream of liquid. Which liquid is it most likely to be?', 'water', ['hexane', 'tetrachloromethane', 'cyclohexane'], 'Polar molecules are attracted to the rod.'),
])


R.facts('ch07-st4', F(
    terms=[('intermolecular forces', 'the attractive forces between molecules (London dispersion, dipole–dipole and hydrogen bonding), much weaker than covalent bonds'),
           ('London (dispersion) forces', 'attractions between instantaneous dipoles and the induced dipoles they create in neighbouring molecules; present between all molecules and increasing with the number of electrons'),
           ('dipole–dipole forces', 'attractions between the permanent dipoles of polar molecules'),
           ('hydrogen bond', 'the attraction between a hydrogen atom bonded to N, O or F in one molecule and a lone pair on an N, O or F atom of another molecule'),
           ('volatility', 'the tendency of a substance to vaporise; volatile substances have weak intermolecular forces and low boiling points')],
    facts=[('Which substance has hydrogen bonding between its molecules?', 'ethanol, C₂H₅OH', ['methoxymethane, CH₃OCH₃', 'hydrogen sulfide, H₂S', 'methane, CH₄'], 'An O–H group is needed.'),
           ('Why does the boiling point of the halogens increase down the group?', 'The number of electrons increases, so London forces are stronger.', ['Hydrogen bonding increases.', 'The covalent bond gets stronger.', 'The molecules become more polar.'], 'Larger, more polarisable electron clouds.'),
           ('Why does water have a much higher boiling point than hydrogen sulfide?', 'Water molecules form hydrogen bonds.', ['Water has more electrons.', 'H–S bonds are stronger.', 'H₂S is ionic.'], 'H₂S has only weak dipole–dipole and London forces.'),
           ('Which isomer of C₅H₁₂ has the lowest boiling point?', '2,2-dimethylpropane', ['pentane', '2-methylbutane', 'they are all the same'], 'Most compact, smallest surface contact.'),
           ('What is broken when liquid bromine boils?', 'London forces between Br₂ molecules', ['Br–Br covalent bonds', 'hydrogen bonds', 'ionic bonds'], 'Only intermolecular forces are overcome.')],
    why=[('Explain why the boiling points of the alkanes increase with chain length.', 'Longer molecules have more electrons and a larger surface area of contact, so the instantaneous–induced dipole (London) forces between molecules are stronger and more energy is needed to separate them.'),
         ('Explain why ethanol is completely miscible with water but hexane is not.', 'Ethanol can form hydrogen bonds with water through its –OH group; hexane is non-polar and cannot form hydrogen bonds, so water molecules hydrogen-bond to each other instead of mixing.'),
         ('Explain why hydrogen fluoride has a higher boiling point than hydrogen chloride.', 'HF molecules form strong hydrogen bonds (H bonded to highly electronegative F with small size and lone pairs); HCl has only dipole–dipole and London forces.'),
         ('Explain why ice is less dense than liquid water.', 'In ice each molecule forms four hydrogen bonds in an open tetrahedral lattice that holds molecules further apart than in the liquid, where hydrogen bonds constantly break and re-form allowing closer packing.')],
    contrast=[('intermolecular forces', 'intramolecular (covalent) bonds', 'Intermolecular forces act between separate molecules and are weak; covalent bonds hold the atoms within a molecule together and are much stronger.'),
              ('London forces', 'hydrogen bonds', 'London forces arise from temporary dipoles and exist between all molecules; hydrogen bonds are stronger attractions requiring H bonded to N, O or F and a lone pair on N, O or F of another molecule.')],
    misc=[('When water boils, the O–H bonds break.', 'Boiling overcomes the hydrogen bonds between water molecules; the covalent O–H bonds remain intact.'),
          ('Non-polar molecules have no intermolecular forces.', 'All molecules experience London dispersion forces, which can be strong in large molecules (e.g. iodine is a solid).'),
          ('Hydrogen bonds form between any molecules containing hydrogen.', 'Hydrogen bonding requires H covalently bonded to N, O or F; e.g. CH₄ cannot hydrogen-bond.')],
    evaluate=[('Hydrogen bonding is the most important intermolecular force.', ['explains the anomalous properties of water, HF, NH₃', 'essential for DNA base pairing and protein structure'], ['London forces dominate in large molecules (waxes, polymers, iodine)', 'London forces are present in all molecules and often contribute most of the total attraction', 'importance depends on the substance'], 'Hydrogen bonds are the strongest per interaction, but for many large molecules London forces contribute more overall – the importance is context dependent.')],
))

BPS = [[('CH4', 'methane', -162), ('C2H6', 'ethane', -89), ('C3H8', 'propane', -42), ('C4H10', 'butane', -1), ('C5H12', 'pentane', 36), ('C6H14', 'hexane', 69)],
       [('F2', 'fluorine', -188), ('Cl2', 'chlorine', -34), ('Br2', 'bromine', 59), ('I2', 'iodine', 184)],
       [('H2O', 'water', 100), ('H2S', 'hydrogen sulfide', -60), ('H2Se', 'hydrogen selenide', -41), ('H2Te', 'hydrogen telluride', -2)],
       [('NH3', 'ammonia', -33), ('PH3', 'phosphine', -88), ('AsH3', 'arsine', -62), ('SbH3', 'stibine', -17)],
       [('HF', 'hydrogen fluoride', 20), ('HCl', 'hydrogen chloride', -85), ('HBr', 'hydrogen bromide', -67), ('HI', 'hydrogen iodide', -35)],
       [('CH3OCH3', 'methoxymethane', -24), ('C2H5OH', 'ethanol', 78), ('C3H8', 'propane', -42), ('CH3CHO', 'ethanal', 20)],
       [('C5H12', 'pentane', 36), ('CH3CH(CH3)CH2CH3', '2-methylbutane', 28), ('C(CH3)4', '2,2-dimethylpropane', 10)],
       [('CH3OH', 'methanol', 65), ('C2H5OH', 'ethanol', 78), ('C3H7OH', 'propan-1-ol', 97), ('C4H9OH', 'butan-1-ol', 118)]]
IMF = [('CH4', 'London dispersion forces only'), ('HCl', 'dipole–dipole forces (and London forces)'), ('H2O', 'hydrogen bonding (and London forces)'),
       ('NH3', 'hydrogen bonding'), ('CO2', 'London dispersion forces only'), ('CH3OH', 'hydrogen bonding'), ('CHCl3', 'dipole–dipole forces'), ('I2', 'London dispersion forces only'),
       ('HF', 'hydrogen bonding'), ('CH3CHO', 'dipole–dipole forces'), ('CH3COCH3', 'dipole–dipole forces'), ('C6H14', 'London dispersion forces only'), ('CH3NH2', 'hydrogen bonding'),
       ('PH3', 'dipole–dipole forces (weak)'), ('Br2', 'London dispersion forces only'), ('CH3OCH3', 'dipole–dipole forces'), ('CH3COOH', 'hydrogen bonding')]


@R.add('ch07-st4', 'C3', (1, 5), 'short')
def c3_rank_bp(rng, slot):
    ser = pick(rng, BPS)
    k = 3 if len(ser) == 3 or slot.d <= 2 else 4
    pool = rng.sample(ser, k)
    srt = sorted(pool, key=lambda s: s[2])
    stem = pick(rng, ['Arrange the following in order of increasing boiling point, and explain the order: ', 'Predict, with reasons, the order of boiling points (lowest first) of: ']) + ', '.join(f'{s[1]} ({chem(s[0])})' for s in pool) + '.'
    ans = ' < '.join(chem(s[0]) for s in srt) + ' (b.p. ' + ', '.join(f'{s[2]} °C' for s in srt) + ')'
    hb = any(s[0] in ('H2O', 'NH3', 'HF', 'C2H5OH', 'CH3OH', 'C3H7OH', 'C4H9OH') for s in pool)
    return dict(stem=stem, answer=ans, markingKey=f'Correct order {ans} (1); ' + ('hydrogen bonding accounts for the anomalously high value(s) (1); ' if hb else '') + 'London forces increase with number of electrons / surface area (1).', type='explain', marks=3 if hb else 2)


@R.add('ch07-st4', 'C3', (1, 4), 'mcq')
def c3_imf_mcq(rng, slot):
    f, imf = pick(rng, IMF)
    main = 'hydrogen bonding' if 'hydrogen' in imf else 'dipole–dipole forces' if 'dipole' in imf else 'London dispersion forces only'
    opts = ['hydrogen bonding', 'dipole–dipole forces', 'London dispersion forces only', 'ionic bonding']
    return mcq(rng, f'What is the strongest type of intermolecular force between molecules of {chem(f)}?', main, [o for o in opts if o != main][:3], f'{chem(f)}: {imf}.')


@R.add('ch07-st4', 'C3', (1, 4), 'mcq')
def c3_highest_bp(rng, slot):
    ser = pick(rng, BPS)
    pool = rng.sample(ser, min(4, len(ser)))
    if len(pool) < 4:
        pool += rng.sample([x for s in BPS for x in s if x not in pool], 4 - len(pool))
    if len({p[2] for p in pool}) < 4:
        return None
    best = max(pool, key=lambda s: s[2])
    return mcq(rng, 'Which substance has the highest boiling point?', f'{best[1]}', [p[1] for p in pool if p != best], ', '.join(f'{p[1]} {p[2]} °C' for p in pool) + '.')


@R.add('ch07-st4', 'C4', (3, 5), 'multi_step')
def c4_hydrides(rng, slot):
    ser = pick(rng, BPS[2:5])
    tab = '\n'.join(f'{chem(s[0])} | {s[2]}' for s in ser)
    first = ser[0]
    stem = (f'The boiling points of some hydrides are shown.\n\nhydride | boiling point / °C\n{tab}\n\n(a) Describe and explain the trend from the second to the last hydride. '
            f'(b) Explain why {chem(first[0])} does not follow this trend. (c) Predict, with a reason, the boiling point {chem(first[0])} would have if it followed the trend.')
    return num(stem, f'(a) increases: more electrons, stronger London forces; (b) hydrogen bonding in {chem(first[0])}; (c) below the second hydride (extrapolated, roughly −80 to −100 °C)',
               f'(a) b.p. increases down the group (A1); molecules have more electrons/larger, so stronger London forces (R1). (b) {chem(first[0])} forms hydrogen bonds – H bonded to a small, highly electronegative atom with lone pairs (R1); much more energy to separate (R1). (c) extrapolation gives a value lower than {chem(ser[1][0])} (R1).', 5, 'multi_step')


R.mcqs('ch07-st4', 'C2', (1, 4), [
    ('Which explains why propan-1-ol (Mr 60) boils at 97 °C while butane (Mr 58) boils at −1 °C?', 'Propan-1-ol molecules form hydrogen bonds.', ['Butane has fewer electrons.', 'Propan-1-ol has stronger covalent bonds.', 'Butane is ionic.'], 'Similar London forces; H-bonding in the alcohol.'),
    ('Which statement about London dispersion forces is correct?', 'They increase as the number of electrons increases.', ['They exist only between polar molecules.', 'They are stronger than hydrogen bonds in small molecules.', 'They involve permanent dipoles.'], 'More polarisable electron cloud.'),
    ('Which molecule can form hydrogen bonds with water but not with itself?', 'propanone, CH₃COCH₃', ['ethanol, C₂H₅OH', 'methane, CH₄', 'ammonia, NH₃'], 'C=O lone pairs accept H-bonds; no O–H or N–H to donate.'),
])


R.facts('ch07-st5', F(
    terms=[('resonance structures', 'two or more Lewis formulae for a species that differ only in the position of electrons; the real structure is a hybrid with delocalised electrons'),
           ('delocalised electrons', 'electrons shared among more than two atoms, as in benzene, carbonate or graphite'),
           ('sigma (σ) bond', 'a covalent bond formed by the head-on (axial) overlap of orbitals, with electron density along the internuclear axis'),
           ('pi (π) bond', 'a covalent bond formed by the sideways overlap of parallel p orbitals, with electron density above and below the internuclear axis'),
           ('hybridisation', 'the mixing of atomic orbitals on an atom to form new, equivalent hybrid orbitals (sp, sp², sp³) used for σ bonding'),
           ('formal charge', 'the charge an atom would have in a Lewis formula if electrons in bonds were shared equally: FC = V − (L + ½B)'),
           ('covalent network structure', 'a giant structure in which atoms are joined by covalent bonds throughout, e.g. diamond, graphite and silicon dioxide')],
    facts=[('What is the hybridisation of each carbon atom in ethene?', 'sp²', ['sp', 'sp³', 'sp³d'], 'Three electron domains.'),
           ('How many σ and π bonds are in a C≡C triple bond?', 'one σ and two π', ['three σ', 'two σ and one π', 'three π'], 'First bond σ, others π.'),
           ('What is the C–O bond order in the carbonate ion?', '1.33', ['1', '1.5', '2'], 'Four bonding pairs over three bonds (resonance).'),
           ('Which allotrope of carbon conducts electricity?', 'graphite', ['diamond', 'both diamond and graphite', 'neither'], 'Each C has one delocalised electron.'),
           ('What is the structure of silicon dioxide?', 'a covalent network of SiO₄ tetrahedra', ['discrete SiO₂ molecules', 'an ionic lattice of Si⁴⁺ and O²⁻', 'layers like graphite'], 'Each Si bonded to four O; each O to two Si.'),
           ('What is the hybridisation of the carbon atom in CO₂?', 'sp', ['sp²', 'sp³', 'no hybridisation'], 'Two electron domains.')],
    why=[('Explain why all the carbon–carbon bonds in benzene have the same length.', 'Six π electrons are delocalised around the ring (resonance hybrid), so each C–C bond has a bond order of 1.5 and an intermediate length between single and double bonds.'),
         ('Explain why graphite is soft and conducts electricity while diamond is hard and does not.', 'In graphite each sp² C bonds to three others in layers held by weak London forces (layers slide) and has a delocalised electron that moves along the layers; in diamond each sp³ C is bonded to four others in a rigid 3D network with no free electrons.'),
         ('Explain why π bonds are weaker than σ bonds.', 'Sideways overlap of p orbitals is less effective than head-on overlap, so the electron density between the nuclei is lower.'),
         ('Explain why rotation is restricted about a C=C double bond but not a C–C single bond.', 'Rotation would require breaking the π bond, which depends on parallel p orbitals overlapping; a σ bond is cylindrically symmetric so rotation does not affect the overlap.'),
         ('Explain why graphene is an excellent electrical conductor and extremely strong.', 'It is a single layer of sp² carbon atoms with delocalised electrons across the whole sheet, and strong covalent bonds throughout the hexagonal network.')],
    contrast=[('a σ bond', 'a π bond', 'A σ bond forms by head-on overlap with electron density on the internuclear axis; a π bond forms by sideways overlap of p orbitals with density above and below the axis and is weaker.'),
              ('diamond', 'graphite', 'Diamond: each C sp³, four bonds, 3D tetrahedral network, hard, non-conductor; graphite: each C sp², three bonds in hexagonal layers with delocalised electrons, soft, conducts.')],
    misc=[('Resonance means the molecule rapidly flips between the different structures.', 'The real species is a single hybrid structure with delocalised electrons; the individual resonance forms do not exist.'),
          ('Silicon dioxide has a low melting point because it is made of small SiO₂ molecules like CO₂.', 'SiO₂ is a covalent network (each Si bonded to four O); many strong Si–O bonds must break, so its melting point is about 1700 °C.')],
    evaluate=[('Hybridisation is a real physical process that occurs in atoms before they bond.', ['explains equivalent bonds and observed geometries (e.g. CH₄)', 'useful descriptive model linked to VSEPR'], ['it is a mathematical model, not an observed process', 'molecular orbital theory explains some observations better (e.g. photoelectron spectra of CH₄)'], 'Hybridisation is a useful model consistent with molecular shapes but not a literal physical step – an illustration of the role of models in chemistry.')],
))

SP = [('C2H4', 'ethene', 5, 1), ('C2H2', 'ethyne', 3, 2), ('CO2', 'carbon dioxide', 2, 2), ('HCN', 'hydrogen cyanide', 2, 2), ('N2', 'nitrogen', 1, 2),
      ('HCHO', 'methanal', 3, 1), ('CH3COOH', 'ethanoic acid', 7, 1), ('C6H6', 'benzene', 12, 3), ('CH2=CHCH3', 'propene', 8, 1), ('CH3CN', 'ethanenitrile', 5, 2),
      ('CH3CHO', 'ethanal', 6, 1), ('HCOOH', 'methanoic acid', 4, 1), ('CH2=CHCH=CH2', 'buta-1,3-diene', 9, 2), ('C2H6', 'ethane', 7, 0), ('CH3COCH3', 'propanone', 9, 1),
      ('O2', 'oxygen', 1, 1), ('HC≡CCH3', 'propyne', 6, 2), ('CH2=CHCN', 'propenenitrile', 6, 3)]
RES = [('the carbonate ion, CO₃²⁻', 3, '1.33'), ('the nitrate ion, NO₃⁻', 3, '1.33'), ('benzene, C₆H₆', 2, '1.5'), ('ozone, O₃', 2, '1.5'),
       ('the ethanoate ion, CH₃COO⁻', 2, '1.5'), ('the nitrite ion, NO₂⁻', 2, '1.5')]


@R.add('ch07-st5', 'C3', (1, 5), 'short')
def c3_sigma_pi(rng, slot):
    f, nm, s, p = pick(rng, SP)
    stem = pick(rng, [f'Deduce the number of σ and π bonds in a molecule of {nm}, {chem(f)}.', f'State the numbers of sigma and pi bonds in {nm}.'])
    return dict(stem=stem, answer=f'{s} σ, {p} π', markingKey=f'Every single bond is one σ; a double bond is 1σ + 1π; a triple bond 1σ + 2π: {s} σ (1) and {p} π (1).', type='short', marks=2)


@R.add('ch07-st5', 'C3', (1, 4), 'mcq')
def c3_hybrid(rng, slot):
    m = pick(rng, [x for x in MOLS if x[10]])
    opts = ['sp', 'sp²', 'sp³', 'sp³d']
    return mcq(rng, f'What is the hybridisation of the central {m[2]} atom in {mf(m)}?', m[10], [o for o in opts if o != m[10]], f'{m[3]} electron domains → {m[10]}.')


@R.add('ch07-st5', 'C3', (2, 5), 'short')
def c3_resonance(rng, slot):
    sp_, k, bo = pick(rng, RES)
    stem = pick(rng, [f'Draw the resonance structures of {sp_} and deduce the average bond order.', f'Explain, using resonance, why all the bonds in {sp_} are identical, and state the bond order.'])
    return dict(stem=stem, answer=f'{k} equivalent resonance structures; bond order {bo}; electrons delocalised so all bonds identical.', markingKey=f'{k} resonance structures with double bond in different positions (1); delocalised π electrons over the bonds (1); bond order {bo}, intermediate length (1).', type='explain', marks=3)


FC = [('CO₂ drawn as O=C=O', 'C 0, each O 0'), ('carbon monoxide drawn as :C≡O:', 'C −1, O +1'), ('NH₄⁺', 'N +1, each H 0'),
      ('the nitrate ion with one N=O and two N–O bonds', 'N +1, O(double) 0, each O(single) −1'), ('ozone, O=O–O (with lone pairs completing octets)', 'central O +1, terminal O(double) 0, terminal O(single) −1'),
      ('SO₂ drawn as O=S=O (expanded octet)', 'S 0, each O 0'), ('SO₂ drawn as O=S–O (octet on S)', 'S +1, O(double) 0, O(single) −1'), ('H₃O⁺', 'O +1, each H 0'),
      ('the cyanide ion, [:C≡N:]⁻', 'C −1, N 0')]


@R.add('ch07-st5', 'C3', (3, 5), 'short')
def c3_formal_charge(rng, slot):
    sp_, ans = pick(rng, FC)
    stem = f'Calculate the formal charge on each atom in {sp_}. (HL)'
    return dict(stem=stem, answer=ans, markingKey=f'FC = V − (L + ½B) applied to each atom (1); {ans} (1).', type='short', marks=2)


R.mcqs('ch07-st5', 'C2', (1, 4), [
    ('Which property of graphite is explained by its delocalised electrons?', 'electrical conductivity', ['softness', 'high melting point', 'insolubility'], 'Mobile electrons carry charge.'),
    ('Which statement explains the very high melting point of diamond?', 'Many strong covalent bonds must be broken.', ['Strong London forces between molecules.', 'Ionic bonds between carbon atoms.', 'Delocalised electrons.'], 'Covalent network.'),
    ('Which species has delocalised π electrons?', 'CO₃²⁻', ['CH₄', 'C₂H₆', 'NH₄⁺'], 'Resonance.'),
    ('Which form of carbon is a molecular (not network) substance?', 'fullerene, C₆₀', ['diamond', 'graphite', 'graphene'], 'C₆₀ molecules held by London forces.'),
])


@R.add('ch07-st5', 'C4', (3, 5), 'multi_step')
def c4_bonds_full(rng, slot):
    f, nm, s, p = pick(rng, [x for x in SP if x[0] not in ('O2', 'N2')])
    stem = (f'For {nm}, {chem(f)}: (a) state the number of σ and π bonds; (b) deduce the hybridisation of each carbon atom; (c) explain how a π bond forms; '
            f'(d) predict the bond angle(s) around the carbon atoms.')
    hyb = {'C2H4': 'both sp²', 'C2H2': 'both sp', 'CO2': 'sp', 'HCN': 'sp', 'HCHO': 'sp²', 'CH3COOH': 'CH₃ sp³; COOH sp²', 'C6H6': 'all sp²', 'CH2=CHCH3': 'CH₂ and CH sp²; CH₃ sp³',
           'CH3CN': 'CH₃ sp³; CN sp', 'CH3CHO': 'CH₃ sp³; CHO sp²', 'HCOOH': 'sp²', 'CH2=CHCH=CH2': 'all sp²', 'C2H6': 'both sp³', 'CH3COCH3': 'CH₃ sp³; C=O sp²', 'HC≡CCH3': 'C≡C carbons sp; CH₃ sp³', 'CH2=CHCN': 'C=C carbons sp²; C≡N carbon sp'}[f]
    ang = {'sp': '180°', 'sp²': '120°', 'sp³': '109.5°'}
    import re as _re
    angs = ', '.join(dict.fromkeys(ang[h] for h in _re.findall(r'sp[²³]?', hyb)))
    return num(stem, f'(a) {s} σ, {p} π; (b) {hyb}; (d) {angs}', f'(a) {s} σ, {p} π (A1 A1). (b) {hyb} (A1). (c) sideways overlap of unhybridised p orbitals above and below the σ bond axis (R1). (d) {angs} (A1).', 5, 'multi_step')


R.f['ch07-st3'].extended = [
    ('Dichloromethane, CH₂Cl₂, and tetrachloromethane, CCl₄, are both tetrahedral. (a) Explain why CH₂Cl₂ is polar but CCl₄ is not. (b) Predict which liquid would be deflected by a charged rod. (c) Suggest, with a reason, which has the higher boiling point (CCl₄ 77 °C, CH₂Cl₂ 40 °C) and why polarity alone does not decide this.', '(a) In CCl₄ four identical C–Cl dipoles cancel symmetrically; in CH₂Cl₂ the C–H and C–Cl dipoles differ so there is a net dipole. (b) CH₂Cl₂. (c) CCl₄ has the higher b.p. because it has many more electrons (74 vs 42) and stronger London forces, which outweigh the dipole–dipole forces in CH₂Cl₂.', 6, 'multi_step'),
    ('Using electronegativity values, (a) rank the bonds C–H, C–O, O–H and C–F in order of increasing polarity; (b) explain why methanol is polar; (c) explain why the C–F bond, though very polar, is very strong.', '(a) C–H (0.4) < C–O (0.8) < O–H (1.2) < C–F (1.4). (b) polar C–O and O–H bonds in a bent arrangement around O – dipoles do not cancel. (c) short bond with large ionic contribution adding to the covalent attraction (bond enthalpy 492 kJ mol⁻¹).', 5, 'multi_step')]
R.f['ch07-st3'].evaluate.append(('The Pauling electronegativity scale is an objective measurement.', ['values are derived from measured bond enthalpies', 'consistent and widely used'], ['electronegativity cannot be measured directly – it is a derived, relative concept', 'other scales (Mulliken, Allred–Rochow) give different values', 'values depend on oxidation state and hybridisation'], 'It is a useful but constructed quantity; its numbers are model-dependent rather than directly measured.'))


@R.add('ch07-st3', 'C4', (3, 5), 'multi_step')
def c4_polarity_pair(rng, slot):
    a = pick(rng, [m for m in MOLS if m[7] is True and not m[13]])
    b = pick(rng, [m for m in MOLS if m[7] is False and not m[13]])
    x, y = (a, b) if rng.random() < 0.5 else (b, a)
    stem = (f'{mf(x)} and {mf(y)} both contain polar bonds. (a) Deduce the shape of each molecule. (b) Explain which molecule is polar. '
            f'(c) Predict which liquid would be deflected by a charged rod and which would be more soluble in water, giving reasons.')
    return num(stem, f'(a) {mf(x)} {x[5]}, {mf(y)} {y[5]}; (b) {mf(a)} polar; (c) {mf(a)} deflected and more soluble in water',
               f'(a) shapes (A1 A1). (b) {mf(a)}: {a[5]} – dipoles do not cancel; {mf(b)}: {b[5]} – dipoles cancel (R1). (c) polar {mf(a)} is attracted to the charged rod (R1); polar molecules interact with polar water (dipole–dipole/H-bonds) (R1).', 5, 'multi_step')


R.f['ch07-st4'].extended = [
    ('The boiling points of methane, ethane, propane and butane are −162, −89, −42 and −1 °C. (a) Describe and explain the trend. (b) Butan-1-ol (Mr 74) boils at 118 °C while pentane (Mr 72) boils at 36 °C. Explain the difference. (c) Predict, with a reason, how the boiling point of 2-methylpropan-2-ol compares with butan-1-ol.', '(a) b.p. rises with chain length: more electrons and larger surface area → stronger London forces. (b) butan-1-ol forms hydrogen bonds through O–H; pentane has London forces only. (c) lower (83 °C): more branched, compact molecule with smaller surface contact (and the OH is more hindered), so weaker London forces.', 6, 'multi_step'),
    ('Explain the following in terms of intermolecular forces: (a) iodine is a solid at room temperature while chlorine is a gas; (b) ice floats on water; (c) propanone mixes with water although it cannot hydrogen-bond to itself.', '(a) I₂ has many more electrons (106 vs 34) – much stronger London forces. (b) hydrogen-bonded open lattice in ice is less dense. (c) the C=O oxygen lone pairs accept hydrogen bonds from water molecules; dipole–dipole interactions also help.', 6, 'multi_step')]
R.f['ch07-st4'].evaluate.append(('Boiling point is a reliable indicator of the strength of intermolecular forces.', ['higher b.p. reflects more energy needed to separate molecules', 'trends in homologous series are clear'], ['b.p. also depends on molar mass, shape and entropy of vaporisation', 'comparisons are only fair between molecules of similar size', 'ionic and network solids have high b.p. due to bonds, not IMF'], 'Boiling point is a good indicator only when comparing similar molecular substances.'))


@R.add('ch07-st4', 'C4', (3, 5), 'multi_step')
def c4_bp_pairs(rng, slot):
    pairs = [(('C2H5OH', 'ethanol', 78), ('CH3OCH3', 'methoxymethane', -24), 'isomers with the same Mr; ethanol has an O–H group and forms hydrogen bonds; the ether has only dipole–dipole and London forces'),
             (('C3H8', 'propane', -42), ('CH3CHO', 'ethanal', 20), 'similar Mr (44); ethanal is polar with dipole–dipole forces; propane has only London forces'),
             (('HF', 'hydrogen fluoride', 20), ('HCl', 'hydrogen chloride', -85), 'HF forms strong hydrogen bonds; HCl has dipole–dipole and London forces only'),
             (('C5H12', 'pentane', 36), ('C(CH3)4', '2,2-dimethylpropane', 10), 'isomers; the straight chain has greater surface contact so stronger London forces'),
             (('Br2', 'bromine', 59), ('ICl', 'iodine monochloride', 97), 'similar numbers of electrons; ICl is polar so has dipole–dipole forces in addition to London forces'),
             (('CH3COOH', 'ethanoic acid', 118), ('C3H7OH', 'propan-1-ol', 97), 'both H-bond, but ethanoic acid forms hydrogen-bonded dimers and has more H-bonding sites')]
    (a, b, why) = pick(rng, pairs)
    hi, lo = (a, b) if a[2] > b[2] else (b, a)
    stem = (f'{a[1].capitalize()} ({chem(a[0])}) boils at {a[2]} °C and {b[1]} ({chem(b[0])}) at {b[2]} °C. (a) Identify all the intermolecular forces present in each substance. '
            f'(b) Explain the difference in boiling points. (c) Suggest which substance has the higher enthalpy of vaporisation and why.')
    return num(stem, f'(b) {why}; (c) {hi[1]}', f'(a) forces in each correctly identified (A1 A1). (b) {why} (R1 R1). (c) {hi[1]}: stronger intermolecular forces need more energy to separate the molecules (R1).', 5, 'multi_step')


# =============================================================================================
# ch08 S2.3 The metallic model and S2.4 From models to materials
# =============================================================================================
R.facts('ch08-st1', F(
    terms=[('metallic bond', 'the electrostatic attraction between a lattice of positive metal ions (cations) and a “sea” of delocalised electrons'),
           ('delocalised electrons', 'valence electrons that are not associated with a particular atom and can move throughout the metal lattice'),
           ('malleability', 'the ability of a material to be hammered or pressed into shape without breaking'),
           ('ductility', 'the ability of a material to be drawn out into a wire'),
           ('transition element', 'an element that has an incomplete d sublevel in its atom or in one of its common ions')],
    facts=[('Why are metals good electrical conductors?', 'Delocalised electrons can move through the lattice when a potential difference is applied.', ['Their ions move to the electrodes.', 'They contain free protons.', 'Their atoms are close together.'], 'Mobile charge carriers.'),
           ('Why is magnesium’s melting point higher than sodium’s?', 'Mg²⁺ is smaller and more highly charged, and each atom contributes two delocalised electrons.', ['Mg is more reactive.', 'Mg has a larger atomic radius.', 'Mg forms covalent bonds.'], 'Stronger metallic bonding.'),
           ('How do the melting points of the group 1 metals change down the group?', 'They decrease.', ['They increase.', 'They stay the same.', 'They increase then decrease.'], 'Larger ions; weaker attraction to delocalised electrons.'),
           ('Why is zinc not considered a transition element?', 'Zn and Zn²⁺ both have a full 3d sublevel.', ['Zinc is not a metal.', 'Zinc has no d electrons.', 'Zinc forms coloured compounds.'], '[Ar] 3d¹⁰ 4s² and [Ar] 3d¹⁰.'),
           ('Which property is characteristic of transition elements?', 'variable oxidation states', ['low melting points', 'colourless compounds only', 'low densities'], 'Similar energies of 4s and 3d electrons.')],
    why=[('Explain why metals are malleable.', 'The layers of cations can slide over one another when a force is applied; the delocalised electrons move with them and continue to hold the lattice together, so the metal changes shape without breaking.'),
         ('Explain why aluminium has a higher melting point than sodium.', 'Al³⁺ has a higher charge and smaller radius than Na⁺ and contributes three delocalised electrons per atom, so the electrostatic attraction between cations and electrons is much stronger.'),
         ('Explain why transition metals generally have higher melting points than group 1 metals.', 'Both 4s and 3d electrons can be delocalised, giving more delocalised electrons per atom and smaller, more highly charged cations – stronger metallic bonding.'),
         ('Explain why metals are good thermal conductors.', 'Delocalised electrons can move freely and transfer kinetic energy rapidly through the lattice, in addition to vibrations of the ions.')],
    contrast=[('metallic bonding', 'ionic bonding', 'Metallic bonding is the attraction between cations and delocalised electrons (non-directional, allows malleability); ionic bonding is the attraction between oppositely charged ions in a fixed lattice (brittle).')],
    misc=[('Metals conduct electricity because their positive ions move.', 'In a solid metal the cations are fixed; it is the delocalised electrons that move and carry the current.'),
          ('A metallic bond is a bond between two metal atoms.', 'Metallic bonding is non-directional: it is the attraction between all the cations and the sea of delocalised electrons throughout the lattice.')],
    evaluate=[('The “sea of electrons” model fully explains the properties of metals.', ['explains conductivity, malleability, ductility and lustre qualitatively', 'explains melting point trends using charge density'], ['cannot explain why some metals are much better conductors than others', 'does not explain magnetism or the semiconductor behaviour of metalloids', 'band theory is needed for a quantitative picture'], 'A useful qualitative model with limitations that band theory addresses.')],
    extended=[('Explain the trend in the melting points of sodium (98 °C), magnesium (650 °C) and aluminium (660 °C), and suggest why aluminium is used for overhead power cables while sodium is not.', 'Increasing cation charge (1+, 2+, 3+), decreasing radius and more delocalised electrons per atom across the period → stronger metallic bonding (Al and Mg similar in practice). Aluminium: good conductor, low density, corrosion resistant (oxide layer), strong enough; sodium reacts violently with water and is soft.', 6, 'multi_step')],
))

MPS = [('Li', 181, 1), ('Na', 98, 1), ('K', 63, 1), ('Rb', 39, 1), ('Cs', 28, 1), ('Mg', 650, 2), ('Ca', 842, 2), ('Sr', 777, 2), ('Al', 660, 3),
       ('Fe', 1538, None), ('Cu', 1085, None), ('Ti', 1668, None), ('Cr', 1907, None), ('Ni', 1455, None)]


@R.add('ch08-st1', 'C3', (1, 4), 'mcq')
def c3_mp_metal(rng, slot):
    pool = rng.sample(MPS, 4)
    best = max(pool, key=lambda m: m[1])
    return mcq(rng, 'Which metal has the highest melting point?', ENAME[best[0]], [ENAME[m[0]] for m in pool if m != best],
               'Melting points / °C: ' + ', '.join(f'{m[0]} {m[1]}' for m in pool) + '. Stronger metallic bonding: smaller, more highly charged cations with more delocalised electrons (d electrons in transition metals).')


@R.add('ch08-st1', 'C2', (2, 4), 'explain')
def c2_metal_pair(rng, slot):
    a, b = rng.sample([m for m in MPS if m[2]], 2)
    if a[1] < b[1]:
        a, b = b, a
    if a[2] > b[2]:
        why = f'{a[0]} forms {a[2]}+ ions and contributes {a[2]} delocalised electrons per atom (vs {b[2]} for {b[0]}), and its cations are smaller'
    else:
        why = f'both form {a[2]}+ ions, but {a[0]} has a smaller ionic radius, so its cations are closer to the delocalised electrons'
    stem = f'{ENAME[a[0]].capitalize()} melts at {a[1]} °C and {ENAME[b[0]]} at {b[1]} °C. Explain the difference in terms of metallic bonding.'
    return dict(stem=stem, answer=why[0].upper() + why[1:] + ', giving stronger metallic bonding.', markingKey=f'{why} (1); stronger electrostatic attraction between cations and delocalised electrons in {a[0]} (1); more energy needed to break the lattice (1).', type='explain', marks=3)


TM_COMP = [('KMnO4', 'Mn', 7), ('K2Cr2O7', 'Cr', 6), ('Fe2O3', 'Fe', 3), ('FeSO4', 'Fe', 2), ('CuCl', 'Cu', 1), ('CuSO4', 'Cu', 2), ('MnO2', 'Mn', 4),
           ('V2O5', 'V', 5), ('TiCl4', 'Ti', 4), ('CrCl3', 'Cr', 3), ('K2MnO4', 'Mn', 6), ('NiO', 'Ni', 2), ('Co2O3', 'Co', 3), ('VO2', 'V', 4)]
OXN = {'K': 1, 'Na': 1, 'O': -2, 'Cl': -1, 'S': 6}


@R.add('ch08-st1', 'C3', (2, 5), 'short')
def c3_tm_ox(rng, slot):
    f, m, ox = pick(rng, TM_COMP)
    stem = pick(rng, [f'Deduce the oxidation state of {m} in {chem(f)} and write the electron configuration of the {m} ion with this charge. (HL)', f'State the oxidation state of {ENAME[m]} in {chem(f)}. (HL)'])
    c = cfg_short(config_ion(Z[m], ox))
    if stem.startswith('State'):
        return dict(stem=stem, answer=f'+{ox}', markingKey=f'Sum of oxidation states = 0 with K +1, O −2, Cl −1, SO₄ −2: {m} = +{ox} (1).', type='short', marks=1)
    return dict(stem=stem, answer=f'+{ox}; {c}', markingKey=f'+{ox} (1); remove 4s electrons first: {c} (1).', type='short', marks=2)


R.mcqs('ch08-st1', 'C2', (1, 4), [
    ('Which best explains why copper can be drawn into wires?', 'Layers of ions can slide while delocalised electrons maintain the bonding.', ['Copper atoms are held by covalent bonds.', 'Copper has a low melting point.', 'The ions repel each other strongly.'], 'Non-directional bonding.'),
    ('Which property of transition elements is due to an incomplete d sublevel?', 'formation of coloured compounds', ['high electrical conductivity of all metals', 'high density of all metals', 'reaction with acids'], 'd–d transitions absorb visible light.'),
    ('Which metal has the strongest metallic bonding?', 'aluminium', ['sodium', 'potassium', 'magnesium'], 'Al³⁺: highest charge density, three electrons delocalised.'),
    ('Why does scandium count as a transition element even though Sc³⁺ has no d electrons?', 'The Sc atom has an incomplete d sublevel ([Ar] 3d¹ 4s²).', ['Sc³⁺ is coloured.', 'Scandium is in group 2.', 'Sc forms only covalent compounds.'], 'Definition includes the atom.'),
])


R.facts('ch08-st2', F(
    terms=[('bonding triangle (van Arkel–Ketelaar diagram)', 'a triangular plot of electronegativity difference against average electronegativity that locates a binary substance on the continuum between ionic, covalent and metallic bonding'),
           ('bonding continuum', 'the idea that bonding varies gradually between the ideal ionic, covalent and metallic types rather than falling into distinct categories'),
           ('percentage ionic character', 'an estimate of the extent of ionic bonding in a substance based on the electronegativity difference of its elements')],
    facts=[('Which quantity is plotted on the vertical axis of the bonding triangle in the data booklet?', 'difference in electronegativity, ΔX', ['average electronegativity', 'melting point', 'ionisation energy'], 'x-axis: average X; y-axis: ΔX.'),
           ('Where on the bonding triangle is a substance with a low average electronegativity and ΔX ≈ 0 found?', 'metallic corner', ['ionic corner', 'covalent corner', 'centre of the triangle'], 'e.g. Na, Mg.'),
           ('Where would chlorine, Cl₂, appear on the bonding triangle?', 'the covalent corner (ΔX = 0, high average X)', ['the metallic corner', 'the ionic vertex', 'the middle of the base'], 'Two identical non-metal atoms.'),
           ('Which substance has the greatest ionic character?', 'CsF', ['NaCl', 'MgO', 'AlCl₃'], 'ΔX = 3.2.')],
    why=[('Explain why the bonding triangle uses both the average electronegativity and the difference in electronegativity.', 'The difference distinguishes ionic from non-ionic bonding, but substances with a small difference can be metallic (low average) or covalent (high average); both coordinates are needed.'),
         ('Explain why aluminium chloride shows significant covalent character although it is a metal–non-metal compound.', 'The electronegativity difference (1.6) is moderate; the small, highly charged Al³⁺ ion polarises the Cl⁻ electron cloud, giving electron sharing – AlCl₃ sublimes at low temperature and forms Al₂Cl₆ molecules.')],
    misc=[('Every compound of a metal with a non-metal is purely ionic.', 'Bonding is a continuum: e.g. AlCl₃ (ΔX 1.6) has substantial covalent character; pure ionic bonding is an idealisation.')],
    evaluate=[('The bonding triangle is a better model than classifying substances as simply ionic, covalent or metallic.', ['shows bonding as a continuum', 'predicts intermediate properties (e.g. AlCl₃, SiO₂)', 'quantitative and data based'], ['only applies to binary compounds', 'electronegativity is itself an approximate scale', 'does not capture structure (molecular vs network)'], 'It is more nuanced and predictive, though still a model with limitations – useful together with structural information.')],
))

TRI = [('NaCl', 'Na', 'Cl', 'ionic'), ('CsF', 'Cs', 'F', 'ionic'), ('MgO', 'Mg', 'O', 'ionic'), ('KBr', 'K', 'Br', 'ionic'), ('CaF2', 'Ca', 'F', 'ionic'),
       ('LiF', 'Li', 'F', 'ionic'), ('Cl2', 'Cl', 'Cl', 'covalent (non-polar)'), ('CH4', 'C', 'H', 'covalent'), ('CO2', 'C', 'O', 'polar covalent'),
       ('SiO2', 'Si', 'O', 'polar covalent'), ('AlCl3', 'Al', 'Cl', 'polar covalent (intermediate)'), ('H2O', 'H', 'O', 'polar covalent'),
       ('Na', 'Na', 'Na', 'metallic'), ('Mg', 'Mg', 'Mg', 'metallic'), ('Cu', 'Cu', 'Cu', 'metallic'), ('CuZn (brass)', 'Cu', 'Zn', 'metallic'),
       ('SiC', 'Si', 'C', 'covalent'), ('PCl3', 'P', 'Cl', 'polar covalent'), ('Fe', 'Fe', 'Fe', 'metallic'), ('KCl', 'K', 'Cl', 'ionic'), ('NH3', 'N', 'H', 'polar covalent'), ('F2', 'F', 'F', 'covalent (non-polar)')]


@R.add('ch08-st2', 'C3', (1, 5), 'short')
def c3_triangle(rng, slot):
    f, a, b, kind = pick(rng, TRI)
    d = abs(EN[a] - EN[b])
    av = (EN[a] + EN[b]) / 2
    stem = pick(rng, [f'Using electronegativity values from the data booklet, calculate the average electronegativity and the electronegativity difference for {chem(f)}, and deduce its position on the bonding triangle.',
                      f'Determine the coordinates of {chem(f)} on the bonding triangle (average X, ΔX) and state the predominant type of bonding.'])
    return dict(stem=stem, answer=f'average X = {av:.2f}, ΔX = {d:.1f}; {kind}', markingKey=f'X({a}) = {EN[a]}, X({b}) = {EN[b]} (1); average {av:.2f} and ΔX {d:.1f} (1); {kind} region (1).', type='short', marks=3)


@R.add('ch08-st2', 'C3', (1, 4), 'mcq')
def c3_triangle_mcq(rng, slot):
    f, a, b, kind = pick(rng, TRI)
    main = 'ionic' if kind.startswith('ionic') else 'metallic' if kind.startswith('metallic') else 'covalent'
    opts = ['ionic', 'covalent', 'metallic', 'hydrogen bonding']
    d = abs(EN[a] - EN[b])
    av = (EN[a] + EN[b]) / 2
    return mcq(rng, f'{chem(f)} has an average electronegativity of {av:.2f} and an electronegativity difference of {d:.1f}. Which type of bonding predominates?', main, [o for o in opts if o != main],
               f'Position on the bonding triangle: {kind}.')


@R.add('ch08-st2', 'C4', (3, 5), 'multi_step')
def c4_triangle_pair(rng, slot):
    a, b = rng.sample(TRI, 2)
    if a[3].split(' ')[0] == b[3].split(' ')[0]:
        return None
    stem = (f'Using the bonding triangle, compare the bonding in {chem(a[0])} and {chem(b[0])}. (a) Calculate the coordinates of each. (b) Deduce the predominant bonding. '
            f'(c) Predict one physical property of each that follows from its bonding and explain it.')
    da, aa = abs(EN[a[1]] - EN[a[2]]), (EN[a[1]] + EN[a[2]]) / 2
    db, ab = abs(EN[b[1]] - EN[b[2]]), (EN[b[1]] + EN[b[2]]) / 2
    return num(stem, f'{chem(a[0])}: ({aa:.2f}, {da:.1f}) {a[3]}; {chem(b[0])}: ({ab:.2f}, {db:.1f}) {b[3]}', f'(a) coordinates (A1 A1). (b) {a[3]} and {b[3]} (A1). (c) one property each linked to bonding, e.g. conductivity, melting point, malleability, solubility (R1 R1).', 5, 'multi_step')


R.mcqs('ch08-st2', 'C2', (1, 4), [
    ('Which pair has the smallest electronegativity difference?', 'Cu and Zn (brass)', ['Na and Cl', 'Si and O', 'H and O'], 'ΔX = 0.2 – metallic.'),
    ('Moving from the ionic vertex towards the covalent corner of the bonding triangle, what happens?', 'ΔX decreases and average X increases', ['ΔX increases', 'average X decreases', 'both stay constant'], 'Covalent corner: ΔX 0, high X.'),
    ('Which substance would be placed nearest the metallic corner?', 'caesium', ['fluorine', 'sodium chloride', 'silicon'], 'Lowest X, ΔX = 0.'),
])


R.facts('ch08-st3', F(
    terms=[('alloy', 'a mixture of a metal with one or more other elements (usually metals), with metallic bonding, e.g. steel, brass, bronze'),
           ('addition polymer', 'a polymer formed when many unsaturated monomers (with C=C) join together without loss of any atoms'),
           ('condensation polymer', 'a polymer formed when monomers with two functional groups join with the loss of a small molecule such as water or HCl at each link'),
           ('repeating unit', 'the smallest section of a polymer chain that repeats to give the whole chain'),
           ('monomer', 'a small molecule that can join with many others to form a polymer'),
           ('plastic', 'a synthetic polymer that can be moulded; its properties depend on chain length, branching and intermolecular forces')],
    facts=[('Why are alloys usually harder than the pure metal?', 'Different-sized atoms disrupt the regular layers, making it harder for layers to slide.', ['They contain covalent bonds.', 'They have no delocalised electrons.', 'Their atoms are all the same size.'], 'Distorted lattice.'),
           ('Which small molecule is eliminated when a polyamide forms from a diamine and a dicarboxylic acid?', 'water', ['hydrogen', 'carbon dioxide', 'ammonia'], 'Amide link –CONH– with loss of H₂O.'),
           ('Which monomer forms poly(chloroethene), PVC?', 'CH₂=CHCl', ['CH₃CH₂Cl', 'CCl₂=CCl₂', 'CH₂=CH₂'], 'Chloroethene.'),
           ('Which linkage is present in polyesters such as PET?', '–COO– (ester)', ['–CONH– (amide)', '–O– (ether)', '–C=C–'], 'Formed from diols and dicarboxylic acids.'),
           ('What is the main metal in bronze?', 'copper (with tin)', ['iron (with carbon)', 'zinc (with copper)', 'aluminium (with magnesium)'], 'Bronze = Cu/Sn.')],
    why=[('Explain why the addition polymerisation of ethene has an atom economy of 100 %.', 'All the atoms of the ethene monomers end up in the polymer; the C=C π bonds open and join monomers with no by-product.'),
         ('Explain why poly(ethene) is not biodegradable.', 'It contains only strong, non-polar C–C and C–H bonds, which micro-organisms’ enzymes cannot break down; it is chemically unreactive.'),
         ('Explain why polyamides such as Kevlar are very strong.', 'Long chains are held together by many hydrogen bonds between amide C=O and N–H groups on neighbouring chains, and the rigid chains align closely.'),
         ('Explain why steel is harder than pure iron.', 'Carbon atoms (much smaller) occupy spaces in the iron lattice, disrupting the regular layers so they cannot slide easily over each other.')],
    contrast=[('addition polymerisation', 'condensation polymerisation', 'Addition polymerisation joins alkene monomers via their C=C bonds with no by-product; condensation polymerisation joins monomers with two functional groups each, eliminating a small molecule (e.g. H₂O) at each link.'),
              ('a monomer', 'a repeating unit', 'A monomer is the starting molecule; the repeating unit is the structure that repeats in the polymer (for addition polymers the C=C becomes C–C).')],
    misc=[('Poly(ethene) contains C=C double bonds like ethene.', 'In polymerisation the C=C π bond breaks and the chain contains only C–C single bonds.'),
          ('An alloy is a compound of metals with a fixed formula.', 'An alloy is a mixture whose composition can vary; the elements are not combined in a fixed ratio.')],
    evaluate=[('Plastics have done more harm than good to the environment.', ['durability leads to persistent waste and microplastics in oceans', 'made from fossil fuels; incineration releases CO₂ and toxins'], ['light packaging reduces transport fuel; extends food life', 'essential in medicine and safety equipment', 'recycling and bioplastics can reduce impacts'], 'Plastics bring major benefits; the harm stems mainly from single-use design and poor waste management – solutions lie in reduction, recycling and biodegradable alternatives.')],
))

ADD_P = [('ethene', 'CH2=CH2', '–CH₂–CH₂–', 'poly(ethene)', 'C2H4'), ('propene', 'CH2=CHCH3', '–CH₂–CH(CH₃)–', 'poly(propene)', 'C3H6'),
         ('chloroethene', 'CH2=CHCl', '–CH₂–CHCl–', 'poly(chloroethene) (PVC)', 'C2H3Cl'), ('phenylethene', 'CH2=CHC6H5', '–CH₂–CH(C₆H₅)–', 'poly(phenylethene) (polystyrene)', 'C8H8'),
         ('tetrafluoroethene', 'CF2=CF2', '–CF₂–CF₂–', 'poly(tetrafluoroethene) (PTFE)', 'C2F4'), ('propenenitrile', 'CH2=CHCN', '–CH₂–CH(CN)–', 'poly(propenenitrile) (acrylic)', 'C3H3N'),
         ('but-2-ene', 'CH3CH=CHCH3', '–CH(CH₃)–CH(CH₃)–', 'poly(but-2-ene)', 'C4H8'), ('1,1-dichloroethene', 'CH2=CCl2', '–CH₂–CCl₂–', 'poly(1,1-dichloroethene)', 'C2H2Cl2')]
COND_P = [('nylon-6,6', 'hexane-1,6-diamine', 'C6H16N2', 'hexanedioic acid', 'C6H10O4', 'amide', 2),
          ('PET', 'ethane-1,2-diol', 'C2H6O2', 'benzene-1,4-dicarboxylic acid', 'C8H6O4', 'ester', 2),
          ('Kevlar', 'benzene-1,4-diamine', 'C6H8N2', 'benzene-1,4-dicarboxylic acid', 'C8H6O4', 'amide', 2)]


@R.add('ch08-st3', 'C3', (1, 5), 'short')
def c3_polymer(rng, slot):
    mono, f, ru, poly, mf_ = pick(rng, ADD_P)
    kind = rng.choice(['ru', 'mono', 'n'])
    if kind == 'ru':
        stem = pick(rng, [f'Draw (write) the repeating unit of the addition polymer formed from {mono}, {chem(f)}.', f'Deduce the structure of the repeating unit of {poly}.'])
        return dict(stem=stem, answer=ru, markingKey=f'{ru} – two carbon atoms in the backbone, no C=C, continuation bonds at each end (1); correct substituents (1).', type='short', marks=2)
    if kind == 'mono':
        stem = f'The repeating unit of an addition polymer is {ru}. Identify the monomer and name the polymer.'
        return dict(stem=stem, answer=f'{mono} ({chem(f)}); {poly}', markingKey=f'{chem(f)} with C=C (1); {poly} (1).', type='short', marks=2)
    Mn = rng.choice([28000, 42000, 56000, 100000, 150000, 250000])
    n = Mn / mr(mf_)
    stem = f'A sample of {poly} has an average molar mass of {Mn} g mol⁻¹. Calculate the average number of {mono} monomer units per chain.'
    return dict(stem=stem, answer=f'{n:.0f}', markingKey=f'M(monomer) = {mr(mf_):.2f} g mol⁻¹ (M1); n = {Mn}/{mr(mf_):.2f} = {n:.0f} (A1).', type='numerical', marks=2)


@R.add('ch08-st3', 'C3', (2, 5), 'numerical')
def c3_condensation(rng, slot):
    poly, a, fa, b, fb, link, w = pick(rng, COND_P)
    Mru = mr(fa) + mr(fb) - w * mr('H2O')
    Mp = rng.choice([20000, 30000, 45000, 60000])
    n = Mp / Mru
    stem = (f'{poly} is a condensation polymer made from {a} ({chem(fa)}) and {b} ({chem(fb)}). (a) State the type of linkage formed and the small molecule eliminated. '
            f'(b) Calculate the molar mass of the repeating unit. (c) Estimate the number of repeating units in a chain of molar mass {Mp} g mol⁻¹.')
    return num(stem, f'(a) {link}, water; (b) {Mru:.2f} g mol⁻¹; (c) {n:.0f}', f'(a) {link} link, H₂O (A1). (b) {mr(fa):.2f} + {mr(fb):.2f} − {w} × 18.02 (M1) = {Mru:.2f} g mol⁻¹ (A1). (c) {Mp}/{Mru:.2f} = {n:.0f} (A1).', 4, 'multi_step')


ALLOYS = [('brass', {'Cu': 0.70, 'Zn': 0.30}), ('bronze', {'Cu': 0.88, 'Sn': 0.12}), ('stainless steel', {'Fe': 0.74, 'Cr': 0.18, 'Ni': 0.08}),
          ('lead-free solder', {'Sn': 0.965, 'Ag': 0.030, 'Cu': 0.005}), ('sterling silver', {'Ag': 0.925, 'Cu': 0.075}), ('18-carat gold', {'Au': 0.75, 'Ag': 0.125, 'Cu': 0.125}),
          ('duralumin', {'Al': 0.94, 'Cu': 0.04, 'Mg': 0.01, 'Mn': 0.01})]


@R.add('ch08-st3', 'C3', (2, 5), 'numerical')
def c3_alloy(rng, slot):
    nm, comp = pick(rng, ALLOYS)
    m = rng.choice([5.00, 10.0, 25.0, 50.0, 100])
    el = pick(rng, list(comp))
    me = m * comp[el]
    ne = me / AR[el]
    stem = pick(rng, [f'A {sf(m)} g sample of {nm} contains {comp[el] * 100:g} % {ENAME[el]} by mass. Calculate the amount, in mol, of {ENAME[el]} atoms in the sample.',
                      f'{nm.capitalize()} has the mass composition ' + ', '.join(f'{v * 100:g} % {k}' for k, v in comp.items()) + f'. Calculate the number of {el} atoms in {sf(m)} g of the alloy.'])
    if 'number' in stem:
        return num(stem, sf(ne * NA), f'm({el}) = {sf(me)} g (M1); n = {sf(me)}/{AR[el]:.2f} = {sf(ne)} mol (M1); N = {sf(ne * NA)} (A1).', 3)
    return num(stem, q(ne, 'mol'), f'm({el}) = {m:g} × {comp[el]} = {sf(me)} g (M1); n = {sf(me)}/{AR[el]:.2f} = {q(ne, "mol")} (A1).', 2)


R.mcqs('ch08-st3', 'C2', (1, 4), [
    ('Which monomer could form a condensation polymer on its own?', 'H₂N(CH₂)₅COOH', ['CH₂=CH₂', 'CH₃COOH', 'CH₃NH₂'], 'Two different functional groups in one molecule.'),
    ('Which polymer is formed by addition polymerisation?', 'poly(propene)', ['nylon-6,6', 'PET', 'Kevlar'], 'From the alkene propene.'),
    ('How many water molecules are eliminated in forming one repeating unit of nylon-6,6?', '2', ['1', '3', '0'], 'Two amide links per repeating unit.'),
    ('Why are thermoplastics such as poly(ethene) softened by heating?', 'The weak intermolecular forces between chains are overcome.', ['Covalent bonds in the chains break.', 'The polymer depolymerises.', 'Cross-links form.'], 'Chains slide.'),
])


R.facts('ch08-st4', F(
    terms=[('composite', 'a material made of two or more distinct phases (a matrix and a reinforcement) combining their properties, e.g. fibreglass or reinforced concrete'),
           ('ceramic', 'an inorganic, non-metallic solid (often ionic/covalent oxides, carbides or nitrides) that is hard, brittle and heat resistant'),
           ('semiconductor', 'a material, such as silicon, whose electrical conductivity is between that of a conductor and an insulator and increases with temperature'),
           ('nanomaterial', 'a material with at least one dimension between 1 and 100 nm, often with properties different from the bulk material')],
    facts=[('Why are ceramics brittle?', 'Their ionic/covalent bonds are directional or fixed, so layers cannot slide without breaking bonds.', ['They contain delocalised electrons.', 'They are mixtures.', 'They have weak intermolecular forces.'], 'No mechanism for plastic deformation.'),
           ('Which property makes carbon-fibre composites suitable for racing-bicycle frames?', 'high strength-to-weight ratio', ['high electrical resistance', 'low melting point', 'high density'], 'Light and strong.'),
           ('Which material is a covalent network semiconductor used in solar cells?', 'silicon', ['copper', 'poly(ethene)', 'sodium chloride'], 'Covalent network with small band gap.'),
           ('Which describes the bonding in silicon carbide used in cutting tools?', 'a covalent network', ['metallic', 'ionic lattice of Si⁴⁺ and C⁴⁻', 'simple molecular'], 'Very hard, high melting point.')],
    why=[('Explain why reinforced concrete is a better structural material than concrete alone.', 'Concrete is strong in compression but weak in tension; steel bars have high tensile strength, so the composite resists both compression and tension.'),
         ('Explain how the type of bonding in a material determines whether it conducts electricity.', 'Conduction needs mobile charged particles: metals have delocalised electrons; ionic materials conduct only when ions are mobile (molten/aqueous); covalent networks conduct only if there are delocalised electrons (graphite) – most are insulators.'),
         ('Explain why graphene has been described as a “wonder material”.', 'A single layer of sp² carbon with strong covalent bonds and delocalised electrons: extremely strong, light, flexible, transparent and an excellent electrical and thermal conductor.')],
    cases=[('the use of carbon-fibre reinforced polymers in the Boeing 787 airliner', 'About half of the airframe by mass is composite, reducing weight and fuel use by about 20 %.', 'composite materials', 'Strong fibres in a polymer matrix combine high strength and stiffness with low density.'),
           ('silicon solar panels on rooftops in Germany', 'Doped silicon converts sunlight into electricity.', 'semiconductors from covalent network structures', 'Silicon’s small band gap allows light to promote electrons into conduction.'),
           ('ceramic tiles on the Space Shuttle', 'Silica tiles protected the shuttle from re-entry temperatures of over 1200 °C.', 'properties of ceramics', 'Strong covalent network gives high melting point and very low thermal conductivity.'),
           ('Kevlar in body armour', 'Aligned polyamide chains absorb the energy of bullets.', 'polymers whose properties come from intermolecular forces', 'Extensive hydrogen bonding between rigid chains gives very high tensile strength.')],
    evaluate=[('The properties of a material can be predicted entirely from its type of bonding.', ['bonding explains conductivity, melting point, hardness, brittleness', 'the bonding triangle links composition to properties'], ['structure (molecular vs network, crystal size, defects) is equally important', 'composites and nanomaterials have properties not shown by components', 'processing (heat treatment, alignment of polymer chains) changes properties'], 'Bonding is a key starting point, but structure, composition and processing must also be considered.'),
              ('Bioplastics are the solution to plastic pollution.', ['made from renewable resources', 'some are compostable (PLA)'], ['need industrial composting conditions', 'land use competition with food crops', 'can contaminate recycling streams'], 'They help in some applications but are not a complete solution; reduction and better recycling remain essential.')],
    extended=[('A designer must choose a material for (i) a kitchen saucepan, (ii) its handle and (iii) a non-stick coating. Suggest a suitable material for each and justify your choices in terms of bonding and structure.', '(i) stainless steel/aluminium: metallic bonding, good thermal conductor, malleable, high mp; (ii) thermosetting polymer (e.g. Bakelite) or wood: poor thermal conductor, cross-linked so does not soften on heating; (iii) PTFE: strong C–F bonds, unreactive, low-friction surface due to weak London forces.', 6, 'multi_step')],
))

MAT = [('a material for electrical wiring', 'copper', 'metallic bonding with delocalised electrons – excellent conductor, ductile'),
       ('a furnace lining', 'magnesium oxide (ceramic)', 'giant ionic lattice with very high melting point; electrical insulator'),
       ('drink bottles', 'PET (polyester)', 'light, strong, transparent, unreactive polymer'),
       ('a cutting-tool tip', 'diamond or silicon carbide', 'covalent network – extremely hard'),
       ('aircraft body panels', 'carbon-fibre composite or aluminium alloy', 'high strength-to-weight ratio'),
       ('lubricant for locks', 'graphite', 'layers held by weak London forces slide over each other'),
       ('non-stick pan coatings', 'PTFE', 'very unreactive C–F bonds; low surface friction'),
       ('microchips', 'silicon', 'covalent network semiconductor whose conductivity can be controlled by doping'),
       ('bullet-proof vests', 'Kevlar', 'hydrogen-bonded aligned polyamide chains with very high tensile strength'),
       ('window glass', 'soda-lime silica glass', 'amorphous covalent network – transparent, hard, unreactive')]


@R.add('ch08-st4', 'C3', (1, 5), 'short')
def c3_material(rng, slot):
    use, mat, why = pick(rng, MAT)
    stem = pick(rng, [f'Suggest a suitable material for {use} and explain your choice in terms of its bonding and structure.', f'Explain why {mat} is used for {use}.'])
    return dict(stem=stem, answer=f'{mat}: {why}.', markingKey=f'{mat} (1); property needed for the use (1); linked to bonding/structure: {why} (1).', type='explain', marks=3)


R.mcqs('ch08-st4', 'C2', (1, 4), [
    ('Which property of glass-fibre reinforced polymer comes mainly from the glass fibres?', 'tensile strength', ['flexibility', 'low density', 'resistance to corrosion'], 'Fibres carry the load.'),
    ('Which material would be expected to be an electrical insulator and to shatter on impact?', 'alumina ceramic', ['aluminium', 'graphite', 'copper'], 'Ionic/covalent, brittle.'),
    ('Why is graphite used in pencils?', 'Its layers slide off easily because the forces between layers are weak.', ['It is very hard.', 'It conducts electricity.', 'It is a metal.'], 'Weak London forces between layers.'),
])


@R.add('ch08-st1', 'C4', (3, 5), 'multi_step')
def c4_metal_props(rng, slot):
    a, b = rng.sample([m for m in MPS if m[2]], 2)
    use = pick(rng, ['overhead power cables', 'aircraft alloys', 'heat sinks for computer processors', 'coolant in some nuclear reactors', 'saucepans'])
    stem = (f'(a) Describe the bonding in {ENAME[a[0]]} and {ENAME[b[0]]}. (b) Explain, with reference to their melting points ({a[1]} °C and {b[1]} °C), which has the stronger metallic bonding. '
            f'(c) Explain why both metals conduct electricity and heat. (d) Discuss one factor, other than conductivity, that determines whether a metal is suitable for {use}.')
    hi = a if a[1] > b[1] else b
    return num(stem, f'(b) {ENAME[hi[0]]}', f'(a) lattice of cations in a sea of delocalised electrons (A1). (b) {ENAME[hi[0]]}: higher charge/smaller cation/more delocalised electrons (R1 R1). (c) delocalised electrons move and carry charge/energy (R1). (d) e.g. density, cost, reactivity/corrosion, melting point, strength (R1).', 5, 'multi_step')


R.f['ch08-st1'].evaluate.append(('Transition metals are more useful than main-group metals.', ['higher strength and melting points (Fe, Ti) for construction', 'variable oxidation states make them excellent catalysts', 'coloured compounds for pigments'], ['aluminium and magnesium are lighter and corrosion resistant', 'many transition metals are expensive, scarce or toxic (Co, Cr)', 'group 1/2 metals have specialist uses (Li batteries)'], 'Usefulness depends on the application; transition metals dominate structural and catalytic uses, while main-group metals win where low density or specific electrochemistry is needed.'))

R.f['ch08-st2'].why += [
    ('Explain why silicon dioxide (ΔX = 1.5) is described as polar covalent rather than ionic.', 'The electronegativity difference is moderate and the average electronegativity is high (2.65), placing SiO₂ in the polar covalent region; electrons are shared unequally in Si–O bonds rather than transferred.'),
    ('Explain why brass is placed in the metallic region of the bonding triangle.', 'Cu and Zn have low and similar electronegativities (ΔX 0.2, average about 1.8); neither atom attracts electrons strongly, so valence electrons are delocalised.'),
    ('Explain why properties such as melting point and conductivity change gradually across the bonding triangle.', 'Bonding changes continuously with ΔX and average X, so the degree of electron transfer, sharing or delocalisation, and therefore the properties, vary gradually rather than abruptly.')]
R.f['ch08-st2'].contrast = [('ionic bonding', 'polar covalent bonding', 'Ionic bonding involves (near-)complete electron transfer at large ΔX; polar covalent bonding involves unequal sharing at moderate ΔX – they lie at different points on a continuum.'),
                            ('the metallic corner', 'the covalent corner of the bonding triangle', 'Both have ΔX ≈ 0, but the metallic corner has low average electronegativity (electrons delocalised) while the covalent corner has high average electronegativity (electrons localised in shared pairs).')]
R.f['ch08-st2'].misc.append(('A substance with ΔX = 0 must be covalent.', 'ΔX = 0 can be covalent (Cl₂) or metallic (Na); the average electronegativity decides which.'))
R.mcqs('ch08-st2', 'C2', (1, 4), [
    ('Which compound would show the most covalent character?', 'AlI₃', ['NaF', 'MgO', 'KCl'], 'Smallest ΔX (1.1) and highly polarisable I⁻.'),
    ('Why is SiCl₄ a liquid at room temperature while NaCl is a high-melting solid?', 'SiCl₄ is molecular covalent (ΔX 1.3); NaCl is ionic (ΔX 2.3).', ['SiCl₄ has stronger ionic bonds.', 'NaCl has hydrogen bonds.', 'SiCl₄ is metallic.'], 'Position on the triangle.'),
    ('Which coordinates (average X, ΔX) correspond to a predominantly ionic compound?', '(2.1, 2.3)', ['(1.0, 0.0)', '(3.0, 0.2)', '(2.6, 0.4)'], 'Large ΔX.'),
])


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step')
def c4_polymer_compare(rng, slot):
    mono, f, ru, poly, mf_ = pick(rng, ADD_P)
    cp = pick(rng, COND_P)
    stem = (f'Compare the formation of {poly} and {cp[0]}. (a) Name the type of polymerisation in each and write the repeating unit of {poly}. (b) State the small molecule eliminated, if any, in each. '
            f'(c) Explain why {cp[0]} can be hydrolysed (broken down by water/acid) while {poly} cannot. (d) Evaluate one environmental consequence of the widespread use of {poly}.')
    return num(stem, f'(a) addition ({ru}); condensation; (b) none; water; (c) {cp[5]} links are polar and can be hydrolysed; C–C backbone cannot', f'(a) addition, repeating unit {ru}; condensation (A1 A1). (b) none for addition, H₂O for {cp[0]} (A1). (c) {cp[5]} linkage contains polar C=O/C–N(O) bonds attacked by water; only strong non-polar C–C/C–H in {poly} (R1). (d) persistence in landfill/oceans or CO₂/toxic gases on incineration; recycling as mitigation (R1).', 5, 'multi_step')


R.f['ch08-st3'].extended = [
    ('Pure aluminium is soft. (a) Explain why adding 4 % copper (duralumin) makes it much harder. (b) Explain why the alloy still conducts electricity. (c) Suggest why duralumin rather than steel is used for aircraft bodies.', '(a) Cu atoms of different size disrupt the regular layers of Al ions so layers cannot slide easily. (b) Metallic bonding retained – delocalised electrons. (c) Much lower density with high strength and good corrosion resistance.', 5, 'multi_step')]

R.f['ch08-st4'].why += [
    ('Explain why polymers are generally poor conductors of electricity.', 'Their electrons are localised in covalent bonds and there are no mobile ions or delocalised electrons (except in special conjugated polymers).'),
    ('Explain why nanoparticles of a material can behave differently from the bulk material.', 'A much larger fraction of atoms is at the surface (large surface area to volume ratio), and quantum effects at the nanoscale change optical, electrical and catalytic properties.')]
R.f['ch08-st4'].contrast = [('a ceramic', 'a metal', 'Ceramics (ionic/covalent) are hard, brittle, heat resistant and usually insulating; metals (metallic bonding) are malleable, ductile and conduct electricity and heat.'),
                            ('a thermoplastic', 'a thermosetting polymer', 'Thermoplastics have chains held by intermolecular forces and soften on heating (can be remoulded); thermosets are cross-linked by covalent bonds and do not soften but char.')]
R.f['ch08-st4'].misc = [('Composites are simply alloys of polymers.', 'A composite contains distinct phases (matrix + reinforcement) that remain separate; an alloy is a metallic mixture with metallic bonding.'),
                        ('All ceramics are poor conductors of heat.', 'Most ceramics are thermal insulators, but some (e.g. silicon carbide, aluminium nitride) conduct heat well.')]
R.mcqs('ch08-st4', 'C2', (1, 4), [
    ('Which material is a thermosetting polymer?', 'Bakelite (phenol–methanal resin)', ['poly(ethene)', 'PVC', 'nylon-6,6'], 'Cross-linked; does not soften.'),
    ('Which property of silicon makes it useful in electronics?', 'its conductivity can be increased by doping', ['it is a good insulator at all temperatures', 'it is a metal', 'it is soluble in water'], 'Semiconductor.'),
])


# =============================================================================================
# ch09 R1.1 Measuring enthalpy changes and R1.2 Energy cycles
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('exothermic reaction', 'a reaction that releases thermal energy to the surroundings; ΔH is negative and the surroundings get warmer'),
           ('endothermic reaction', 'a reaction that absorbs thermal energy from the surroundings; ΔH is positive and the surroundings get cooler'),
           ('enthalpy change (ΔH)', 'the heat energy transferred between a system and its surroundings at constant pressure'),
           ('standard conditions', 'a pressure of 100 kPa and (usually) a temperature of 298 K, with solutions at 1 mol dm⁻³, shown by the symbol ⦵'),
           ('activation energy (Ea)', 'the minimum energy that colliding particles need for a reaction to occur'),
           ('system and surroundings', 'the system is the chemicals reacting; the surroundings are everything else, including the solvent, container and air')],
    facts=[('In an exothermic reaction, how does the enthalpy of the products compare with that of the reactants?', 'The products have lower enthalpy.', ['The products have higher enthalpy.', 'They are equal.', 'It depends on the activation energy.'], 'Energy is released, so ΔH < 0.'),
           ('Which process is endothermic?', 'melting ice', ['combustion of methane', 'neutralisation of HCl by NaOH', 'condensation of steam'], 'Energy is absorbed to overcome hydrogen bonds.'),
           ('What are standard conditions in thermochemistry?', '100 kPa and a specified temperature, usually 298 K', ['101.3 kPa and 273 K', '1 atm and 0 °C', '100 kPa and 273 K only'], 'IB: 100 kPa, 298 K.'),
           ('On an energy profile, ΔH is the difference in enthalpy between', 'products and reactants', ['the transition state and reactants', 'the transition state and products', 'the catalysed and uncatalysed paths'], 'ΔH = H(products) − H(reactants).'),
           ('Which reaction has a positive ΔH?', 'thermal decomposition of calcium carbonate', ['burning hydrogen', 'respiration', 'rusting of iron'], 'Endothermic decomposition.')],
    why=[('Explain why the temperature of the surroundings rises during an exothermic reaction.', 'The products have less enthalpy than the reactants; the difference is transferred as heat from the system to the surroundings, increasing the average kinetic energy of the surrounding particles.'),
         ('Explain why most exothermic reactions still require an initial input of energy.', 'Bonds in the reactants must first be broken (or particles must collide with energy ≥ Ea) to reach the transition state; energy released when new bonds form later exceeds that absorbed.'),
         ('Explain why ΔH for a reaction depends on the physical states of the reactants and products.', 'Changes of state involve enthalpy changes themselves (e.g. condensing H₂O(g) to H₂O(l) releases 44 kJ mol⁻¹), so different states give different total enthalpy changes.'),
         ('Explain why chemical systems tend to become more stable when exothermic reactions occur.', 'Products at lower enthalpy have stronger bonding overall; energy has been released to the surroundings, so the products are energetically more stable.')],
    contrast=[('an exothermic reaction', 'an endothermic reaction', 'An exothermic reaction releases heat (ΔH < 0, surroundings warm up, products lower in enthalpy); an endothermic reaction absorbs heat (ΔH > 0, surroundings cool, products higher in enthalpy).'),
              ('heat', 'temperature', 'Heat is energy transferred because of a temperature difference (J); temperature measures the average kinetic energy of particles (K).')],
    misc=[('In an endothermic reaction the reaction mixture gets hot because energy is absorbed.', 'An endothermic reaction absorbs heat from its surroundings, so the mixture and container feel colder.'),
          ('A negative ΔH means the reaction will happen quickly.', 'ΔH concerns energy change, not rate; rate depends on activation energy and conditions (e.g. diamond → graphite is exothermic but extremely slow).')],
    evaluate=[('Energy profiles give a complete description of a reaction.', ['show ΔH and Ea and the effect of catalysts', 'help predict whether heating is needed'], ['give no information on rate constants, mechanism steps or entropy', 'are idealised one-dimensional plots of complex multi-dimensional changes'], 'They are useful summaries of energetics but not of kinetics or spontaneity in full.')],
))


@R.add('ch09-st1', 'C3', (1, 5), 'numerical')
def c3_profile(rng, slot):
    hr = rng.choice([0, 50, 100, 150, 200, 250, 300])
    hp = hr + rng.choice([-280, -190, -120, -75, -40, 35, 60, 90, 150, 210])
    ht = max(hr, hp) + rng.choice([40, 75, 100, 130, 180, 220])
    dH = hp - hr
    ea_f = ht - hr
    ea_r = ht - hp
    kind = rng.choice(['dH', 'eaf', 'ear', 'all'])
    data = f'On an energy profile, the reactants are at {hr} kJ mol⁻¹, the transition state at {ht} kJ mol⁻¹ and the products at {hp} kJ mol⁻¹.'
    if kind == 'dH':
        return nmcq(rng, data + ' What is ΔH for the forward reaction?', dH, [-dH, ea_f, ea_r], 'kJ mol⁻¹', f'ΔH = H(products) − H(reactants) = {hp} − {hr} = {sgn(dH)} kJ mol⁻¹.', extra=False, signed=True) if dH else None
    if kind == 'eaf':
        return num(data + ' Determine the activation energy of the forward reaction and state whether the reaction is exothermic or endothermic.', f'Ea = {ea_f} kJ mol⁻¹; {"exothermic" if dH < 0 else "endothermic"}', f'Ea = {ht} − {hr} = {ea_f} kJ mol⁻¹ (A1); ΔH = {sgn(dH)} kJ mol⁻¹ so {"exothermic" if dH < 0 else "endothermic"} (A1).', 2)
    if kind == 'ear':
        return num(data + ' Calculate the activation energy of the reverse reaction.', f'{ea_r} kJ mol⁻¹', f'Ea(reverse) = H(TS) − H(products) = {ht} − {hp} = {ea_r} kJ mol⁻¹ (A1); equivalently Ea(forward) − ΔH (M1).', 2)
    stem = (f'For a reaction, ΔH = {sgn(dH)} kJ mol⁻¹ and the activation energy of the forward reaction is {ea_f} kJ mol⁻¹. (a) Sketch the energy profile, labelling ΔH and Ea. '
            f'(b) Calculate the activation energy of the reverse reaction. (c) A catalyst lowers Ea(forward) by {ea_f // 3} kJ mol⁻¹. State the effect on ΔH and on Ea(reverse).')
    return num(stem, f'(b) {ea_r} kJ mol⁻¹; (c) ΔH unchanged; Ea(reverse) = {ea_r - ea_f // 3} kJ mol⁻¹', f'(a) products {"below" if dH < 0 else "above"} reactants; Ea from reactants to peak; ΔH between reactants and products (A1 A1). (b) Ea(rev) = Ea(fwd) − ΔH = {ea_f} − ({dH}) = {ea_r} (A1). (c) ΔH unchanged (A1); Ea(rev) also falls by {ea_f // 3} to {ea_r - ea_f // 3} kJ mol⁻¹ (A1).', 5, 'multi_step')


PROCS = [('burning methane in a Bunsen burner', 'exothermic'), ('dissolving ammonium nitrate in water (instant cold pack)', 'endothermic'), ('photosynthesis', 'endothermic'),
         ('respiration of glucose', 'exothermic'), ('the reaction of sodium with water', 'exothermic'), ('thermal decomposition of copper(II) carbonate', 'endothermic'),
         ('neutralisation of hydrochloric acid with sodium hydroxide', 'exothermic'), ('evaporation of sweat from skin', 'endothermic'), ('condensation of steam on a cold window', 'exothermic'),
         ('the thermite reaction', 'exothermic'), ('electrolysis of water', 'endothermic'), ('freezing of water', 'exothermic'), ('breaking the H–H bond in hydrogen', 'endothermic'),
         ('the reaction of citric acid with sodium hydrogencarbonate', 'endothermic'), ('setting of concrete (hydration of cement)', 'exothermic')]


@R.add('ch09-st1', 'C3', (1, 4), 'mcq')
def c3_exo_endo(rng, slot):
    p, k = pick(rng, PROCS)
    opts = {'exothermic': 'exothermic; ΔH negative; surroundings warm up', 'endothermic': 'endothermic; ΔH positive; surroundings cool down'}
    wr = ['exothermic; ΔH positive; surroundings warm up', 'endothermic; ΔH negative; surroundings cool down', opts['endothermic' if k == 'exothermic' else 'exothermic']]
    return mcq(rng, f'Which describes {p}?', opts[k], wr, f'{p[0].upper() + p[1:]} is {k}.')


R.mcqs('ch09-st1', 'C2', (1, 4), [
    ('A reaction mixture in a beaker becomes colder. Which statement is correct?', 'The reaction is endothermic and ΔH is positive.', ['The reaction is exothermic and ΔH is positive.', 'The reaction is endothermic and ΔH is negative.', 'Heat flows from the reaction to the surroundings.'], 'System absorbs heat from surroundings.'),
    ('Which statement about a catalysed reaction is correct?', 'ΔH is unchanged but Ea is lower.', ['ΔH becomes more negative.', 'Ea increases.', 'Both ΔH and Ea decrease.'], 'Catalysts provide an alternative pathway.'),
    ('Which symbol indicates a standard enthalpy change?', 'ΔH⦵', ['ΔH°C', 'ΔHₛ', 'ΔG'], 'Standard conditions symbol.'),
    ('Which energy change accompanies bond breaking?', 'Energy is absorbed (endothermic).', ['Energy is released (exothermic).', 'No energy change.', 'Energy is released only for single bonds.'], 'Bond breaking is always endothermic.'),
])


R.facts('ch09-st2', F(
    terms=[('calorimetry', 'the experimental measurement of heat transferred in a reaction from the temperature change of a known mass of a substance (usually water)'),
           ('specific heat capacity', 'the energy needed to raise the temperature of 1 g of a substance by 1 K; for water 4.18 J g⁻¹ K⁻¹'),
           ('enthalpy of combustion', 'the enthalpy change when one mole of a substance is completely burned in oxygen under standard conditions'),
           ('enthalpy of neutralisation', 'the enthalpy change when an acid and a base react to form one mole of water'),
           ('heat loss', 'transfer of heat to or from the surroundings that is not measured by the calorimeter, a major systematic error')],
    facts=[('Which equation is used to calculate the heat transferred in a calorimetry experiment?', 'Q = mcΔT', ['Q = m/cΔT', 'Q = mc/ΔT', 'Q = nΔH/m'], 'm in g, c in J g⁻¹ K⁻¹, ΔT in K.'),
           ('In Q = mcΔT for a reaction in solution, what is m?', 'the mass of the solution (water) being heated', ['the mass of the reactant', 'the molar mass', 'the mass of the calorimeter only'], 'Assume density 1.00 g cm⁻³.'),
           ('Why is a polystyrene cup used as a calorimeter?', 'It is a good insulator with a low heat capacity.', ['It reacts with the solution.', 'It conducts heat well.', 'It is transparent.'], 'Reduces heat loss.'),
           ('Experimental enthalpies of combustion from a spirit burner are usually less exothermic than data-booklet values. Why?', 'Heat is lost to the surroundings and combustion is incomplete.', ['The thermometer is too accurate.', 'Water has a high specific heat capacity.', 'Too much fuel is burned.'], 'Major systematic errors.')],
    why=[('Explain why the temperature–time graph is extrapolated back to the time of mixing in a calorimetry experiment.', 'Heat is lost to the surroundings while the temperature is rising; extrapolating the cooling line back to the time of mixing estimates the maximum temperature that would have been reached with no heat loss, giving a more accurate ΔT.'),
         ('Explain why the enthalpy change of neutralisation for strong acids with strong bases is almost constant (about −57 kJ mol⁻¹).', 'Strong acids and bases are fully ionised, so the reaction in each case is H⁺(aq) + OH⁻(aq) → H₂O(l); the spectator ions do not contribute.'),
         ('Explain why ΔH is negative when the temperature of the water in a calorimeter rises.', 'The heat gained by the water came from the reacting system, which therefore lost enthalpy; by convention heat released by the system gives a negative ΔH.')],
    contrast=[('q (heat transferred)', 'ΔH (enthalpy change)', 'q = mcΔT is the heat energy gained by the surroundings in joules; ΔH = −q/n expresses it per mole of reaction, with the sign showing the direction (negative for exothermic).')],
    misc=[('In Q = mcΔT, m is the mass of the fuel burned.', 'm is the mass of the water (or solution) whose temperature changes; the amount of fuel is used afterwards to find ΔH per mole.'),
          ('A larger volume of the same solutions will give a larger temperature rise.', 'Both heat released and mass heated scale up, so ΔT is (ideally) the same; only the total heat increases.')],
    evaluate=[('Coffee-cup calorimetry gives accurate values for enthalpies of reaction.', ['simple and quick; good for reactions in solution', 'results with neutralisation are often within 5 % of literature'], ['heat loss to surroundings and cup', 'assumes density and specific heat capacity of solution equal water', 'thermometer resolution limits precision for small ΔT'], 'Useful for comparison and teaching; for accurate data bomb calorimetry and careful corrections are needed.')],
))


@R.add('ch09-st2', 'C3', (1, 5), 'numerical')
def c3_calorimetry(rng, slot):
    kind = rng.choice(['neut', 'comb', 'disp', 'q', 'dT'])
    who = name(rng)
    if kind == 'neut':
        acid, base, k = pick(rng, [('hydrochloric acid', 'sodium hydroxide', 1), ('nitric acid', 'potassium hydroxide', 1), ('sulfuric acid', 'sodium hydroxide', 2), ('ethanoic acid', 'sodium hydroxide', 1)])
        v = rng.choice([25.0, 50.0, 100.0])
        c = rng.choice([1.00, 2.00, 0.500, 1.50])
        dHt = -57.1 if 'ethanoic' not in acid else -55.9
        nw = c * v / 1000 * k
        m = 2 * v
        dT = -dHt * 1000 * nw / (m * CW)
        dT = round(dT * rng.uniform(0.92, 1.0), 1)
        q_ = m * CW * dT
        dH = -q_ / nw / 1000
        stem = (f'{who} mixed {v:.1f} cm³ of {sf(c)} mol dm⁻³ {acid} with {v:.1f} cm³ of {sf(c * k)} mol dm⁻³ {base} in a polystyrene cup. The temperature rose by {dT} K. '
                f'Calculate the enthalpy change of neutralisation per mole of water formed. (Assume the solution has a density of 1.00 g cm⁻³ and c = 4.18 J g⁻¹ K⁻¹.)')
        if slot.d <= 2:
            return nmcq(rng, stem.replace('Calculate the enthalpy', 'What is the enthalpy'), dH, [-dH, -v * CW * dT / nw / 1000, dH * 1000], 'kJ mol⁻¹', f'q = {m:.0f} × 4.18 × {dT} = {sf(q_)} J; n(H₂O) = {sf(nw)} mol; ΔH = −{sf(q_)}/{sf(nw)} = {sgn(dH)} kJ mol⁻¹. Using only one volume, or a positive sign, are common errors.', extra=False, signed=True)
        return num(stem, sgn(dH, 3, 'kJ mol⁻¹'), f'q = mcΔT = {m:.0f} × 4.18 × {dT} = {sf(q_)} J (M1); n(H₂O) = {sf(nw)} mol (M1); ΔH = −q/n = {sgn(dH, 3, "kJ mol⁻¹")} (A1, negative sign required).', 3)
    if kind == 'comb':
        fuel, f, lit = pick(rng, [('ethanol', 'C2H5OH', -1367), ('methanol', 'CH3OH', -726), ('propan-1-ol', 'C3H7OH', -2021), ('butan-1-ol', 'C4H9OH', -2676), ('hexane', 'C6H14', -4163), ('paraffin wax', 'C25H52', -15100)])
        mw = rng.choice([100.0, 150.0, 200.0, 250.0])
        mf_ = round(rng.uniform(0.30, 1.20), 2)
        n = mf_ / mr(f)
        dT = round(-lit * 1000 * n * rng.uniform(0.45, 0.75) / (mw * CW), 1)
        q_ = mw * CW * dT
        dH = -q_ / n / 1000
        stem = (f'A spirit burner containing {fuel}, {chem(f)}, was used to heat {mw:.1f} g of water in a copper can. The mass of the burner decreased by {mf_:.2f} g and the water temperature rose by {dT} K. '
                f'Calculate the experimental enthalpy of combustion of {fuel}.')
        if slot.d >= 4:
            stem += f' The data-booklet value is {lit} kJ mol⁻¹: calculate the percentage error and suggest two reasons for it.'
            err = abs(dH - lit) / abs(lit) * 100
            return num(stem, f'{sgn(dH, 3, "kJ mol⁻¹")}; {err:.0f} %', f'q = {mw:.1f} × 4.18 × {dT} = {sf(q_)} J (M1); n = {mf_:.2f}/{mr(f):.2f} = {sf(n)} mol (M1); ΔH = {sgn(dH, 3, "kJ mol⁻¹")} (A1); % error {err:.0f} % (A1); heat loss to air/can, incomplete combustion (soot), evaporation of fuel (R1).', 5, 'multi_step')
        return num(stem, sgn(dH, 3, 'kJ mol⁻¹'), f'q = mcΔT = {sf(q_)} J (M1); n(fuel) = {sf(n)} mol (M1); ΔH = −q/n = {sgn(dH, 3, "kJ mol⁻¹")} (A1).', 3)
    if kind == 'disp':
        v = rng.choice([25.0, 50.0])
        c = rng.choice([0.500, 1.00, 0.200])
        n = c * v / 1000
        dT = round(217000 * n / (v * CW) * rng.uniform(0.85, 0.97), 1)
        q_ = v * CW * dT
        dH = -q_ / n / 1000
        stem = (f'Excess zinc powder was added to {v:.1f} cm³ of {sf(c)} mol dm⁻³ copper(II) sulfate solution: Zn(s) + CuSO₄(aq) → ZnSO₄(aq) + Cu(s). The maximum temperature rise, found by extrapolation, was {dT} K. '
                f'Determine ΔH for the reaction in kJ mol⁻¹.')
        return num(stem, sgn(dH, 3, 'kJ mol⁻¹'), f'q = {v:.1f} × 4.18 × {dT} = {sf(q_)} J (M1); n(CuSO₄) = {sf(n)} mol – zinc in excess (M1); ΔH = {sgn(dH, 3, "kJ mol⁻¹")} (A1).', 3)
    if kind == 'q':
        m = rng.choice([50.0, 100.0, 200.0, 250.0, 500.0])
        dT = round(rng.uniform(2, 40), 1)
        q_ = m * CW * dT
        stem = f'Calculate the heat energy, in kJ, needed to raise the temperature of {m:.0f} g of water by {dT} K.'
        return nmcq(rng, stem.replace('Calculate the heat energy', 'What heat energy'), q_ / 1000, [q_, m * dT / CW / 1000, q_ / 100000], 'kJ', f'q = mcΔT = {m:.0f} × 4.18 × {dT} = {sf(q_)} J = {sf(q_ / 1000)} kJ.', extra=False)
    salt, f, dHs = pick(rng, [('ammonium nitrate', 'NH4NO3', 25.7), ('potassium chloride', 'KCl', 17.2), ('sodium hydroxide', 'NaOH', -44.5), ('calcium chloride', 'CaCl2', -82.8), ('ammonium chloride', 'NH4Cl', 14.8)])
    m = round(rng.uniform(2, 8), 2)
    V = rng.choice([50.0, 100.0])
    n = m / mr(f)
    dT = -dHs * 1000 * n / (V * CW)
    stem = f'The enthalpy of solution of {salt} is {sgn(dHs)} kJ mol⁻¹. Predict the temperature change when {m:.2f} g of {salt} dissolves in {V:.0f} cm³ of water, assuming no heat loss.'
    return num(stem, f'{"rise" if dT > 0 else "fall"} of {abs(dT):.1f} K', f'n = {m:.2f}/{mr(f):.2f} = {sf(n)} mol (M1); q = n × |ΔH| = {sf(abs(dHs) * 1000 * n)} J (M1); ΔT = q/(mc) = {abs(dT):.1f} K, a {"rise" if dT > 0 else "fall"} (A1).', 3)


@p1b(R, 'ch09-st2', d=(3, 5))
def p1b_cooling(rng, slot):
    T0 = round(rng.uniform(19.5, 22.5), 1)
    dT = round(rng.uniform(6, 12), 1)
    times = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
    tm = 90  # mixing at 90 s
    cool = rng.uniform(0.010, 0.018)  # K per s
    temps = []
    for t in times:
        if t < tm:
            temps.append(T0)
        elif t == tm:
            temps.append(round(T0 + dT * 0.55, 1))
        else:
            temps.append(round(T0 + dT - cool * (t - tm), 1))
    tmax = T0 + dT
    c = rng.choice([1.00, 0.500])
    v = 50.0
    n = c * v / 1000
    q_ = 100 * CW * dT
    dH = -q_ / n / 1000
    tab = '\n'.join(f'{t} | {T:.1f}' for t, T in zip(times, temps))
    intro = (f'50.0 cm³ of {sf(c)} mol dm⁻³ HCl(aq) was placed in a polystyrene cup and its temperature recorded every 30 s. At 90 s, 50.0 cm³ of {sf(c)} mol dm⁻³ NaOH(aq) at the same temperature was added. The thermometer reads to ±0.1 °C.\n\n'
             f'time / s | temperature / °C\n{tab}')
    return dict(intro=intro, parts=[
        ('Explain why the maximum recorded temperature is not used directly to find ΔT.', 'Heat is lost to the surroundings while the mixture warms and after mixing; extrapolation corrects for this heat loss.', 'Heat loss during the temperature rise (1).', 1),
        ('By extrapolating the cooling section back to 90 s, determine the temperature change.', f'ΔT ≈ {dT:.1f} K', f'Extrapolated T at 90 s ≈ {tmax:.1f} °C (M1); ΔT = {tmax:.1f} − {T0:.1f} = {dT:.1f} K (A1).', 2),
        ('Calculate ΔH of neutralisation in kJ mol⁻¹.', sgn(dH, 3, 'kJ mol⁻¹'), f'q = 100.0 × 4.18 × {dT:.1f} = {sf(q_)} J (M1); n = {sf(n)} mol; ΔH = {sgn(dH, 3, "kJ mol⁻¹")} (A1).', 2),
        ('Calculate the percentage uncertainty in ΔT.', f'{0.2 / dT * 100:.1f} %', f'±0.2 K (two readings) / {dT:.1f} × 100 (M1) = {0.2 / dT * 100:.1f} % (A1).', 2)],
        extras=[('State one assumption made in the calculation of q.', 'The solution has the density (1.00 g cm⁻³) and specific heat capacity (4.18 J g⁻¹ K⁻¹) of water / the cup absorbs no heat.', 'Any valid assumption (1).', 1)])


pct_error(R, 'ch09-st2', 'the enthalpy of combustion of ethanol', 'kJ mol⁻¹', -1367, 0.45, 0.8,
          ['used a spirit burner to heat water in a copper calorimeter.', 'burned ethanol beneath an aluminium can of water.'],
          ['heat lost to the surroundings (experimental value less exothermic) – use a draught shield and lid / insulate the calorimeter', 'incomplete combustion producing soot – ensure a good air supply', 'heat absorbed by the copper can not included – include its heat capacity in the calculation'], signed=True)

R.mcqs('ch09-st2', 'C2', (1, 4), [
    ('25 cm³ of 1.0 mol dm⁻³ HCl and 25 cm³ of 1.0 mol dm⁻³ NaOH give ΔT = 6.8 K. What ΔT would 50 cm³ of each give?', '6.8 K', ['13.6 K', '3.4 K', '27.2 K'], 'Twice the heat but twice the mass.'),
    ('Which change would reduce heat loss in a spirit-burner experiment?', 'shielding the flame and calorimeter from draughts', ['using a larger flame', 'using a glass beaker instead of a copper can', 'stirring less'], 'Less convection loss.'),
    ('Which error makes the calculated enthalpy of combustion less exothermic than the true value?', 'heat lost to the air', ['weighing the burner before evaporation of fuel', 'using too much water', 'using a more precise thermometer'], 'Less heat reaches the water.'),
])


R.facts('ch09-st3', F(
    terms=[("Hess's law", 'the total enthalpy change for a reaction is independent of the route taken, provided the initial and final conditions are the same'),
           ('standard enthalpy of formation (ΔHf⦵)', 'the enthalpy change when one mole of a substance is formed from its elements in their standard states under standard conditions'),
           ('standard enthalpy of combustion (ΔHc⦵)', 'the enthalpy change when one mole of a substance is burned completely in oxygen under standard conditions'),
           ('energy cycle', 'a diagram showing alternative routes between reactants and products, used with Hess’s law to calculate an unknown enthalpy change')],
    facts=[('What is the standard enthalpy of formation of O₂(g)?', '0 kJ mol⁻¹', ['−249 kJ mol⁻¹', '+498 kJ mol⁻¹', 'it cannot be defined'], 'Elements in their standard states have ΔHf = 0.'),
           ('Which equation represents ΔHf⦵ of water?', 'H₂(g) + ½O₂(g) → H₂O(l)', ['2H₂(g) + O₂(g) → 2H₂O(l)', 'H₂O(l) → H₂(g) + ½O₂(g)', '2H(g) + O(g) → H₂O(l)'], 'One mole of product from elements in standard states.'),
           ('If ΔH for A → B is −50 kJ mol⁻¹, what is ΔH for 2B → 2A?', '+100 kJ mol⁻¹', ['−100 kJ mol⁻¹', '+50 kJ mol⁻¹', '−50 kJ mol⁻¹'], 'Reverse (change sign) and double.'),
           ('Which expression gives ΔH of reaction from enthalpies of formation?', 'ΣΔHf(products) − ΣΔHf(reactants)', ['ΣΔHf(reactants) − ΣΔHf(products)', 'ΣΔHf(products) + ΣΔHf(reactants)', 'ΣΔHc(products) − ΣΔHc(reactants)'], 'Hess cycle via elements.')],
    why=[("Explain why Hess's law follows from the law of conservation of energy.", 'Enthalpy is a state function: if two routes between the same states gave different enthalpy changes, a cycle could create energy, contradicting conservation of energy.'),
         ('Explain why the enthalpy of formation of methane cannot be measured directly.', 'Carbon and hydrogen do not react cleanly to form only methane under standard conditions; the value is found indirectly from enthalpies of combustion using a Hess cycle.'),
         ('Explain why, when using ΔHc data, ΔHr = ΣΔHc(reactants) − ΣΔHc(products).', 'In the cycle both reactants and products are burned to the same combustion products; the route via combustion goes forward from reactants and backward from products, so the products’ values are subtracted.')],
    contrast=[('enthalpy of formation', 'enthalpy of combustion', 'Enthalpy of formation refers to 1 mol of compound made from its elements in standard states; enthalpy of combustion refers to 1 mol of substance burned completely in oxygen.')],
    misc=[('The enthalpy of formation of CO₂ is the same as the enthalpy of combustion of carbon only by coincidence.', 'It is not coincidence: C(graphite) + O₂(g) → CO₂(g) is both the formation equation of CO₂ and the combustion equation of carbon.'),
          ('When an equation is reversed, ΔH stays the same.', 'Reversing a reaction reverses the sign of ΔH.')],
    evaluate=[('Hess’s law calculations using tabulated ΔHf values give the true enthalpy change of any reaction.', ['tabulated values are accurately measured', 'avoid difficult direct measurements'], ['tabulated values refer to standard conditions; real conditions differ', 'states must be correct (H₂O(l) vs H₂O(g))', 'data uncertainties propagate'], 'Reliable for standard conditions when correct states are used, but real-condition values may differ.')],
))

HESS_RX = [({'CH4(g)': 1, 'O2(g)': 2}, {'CO2(g)': 1, 'H2O(l)': 2}), ({'C2H5OH(l)': 1, 'O2(g)': 3}, {'CO2(g)': 2, 'H2O(l)': 3}),
           ({'CaCO3(s)': 1}, {'CaO(s)': 1, 'CO2(g)': 1}), ({'NH3(g)': 4, 'O2(g)': 5}, {'NO(g)': 4, 'H2O(g)': 6}), ({'NO2(g)': 2}, {'N2O4(g)': 1}),
           ({'Fe2O3(s)': 1, 'CO(g)': 3}, {'Fe(s)': 2, 'CO2(g)': 3}), ({'SO2(g)': 2, 'O2(g)': 1}, {'SO3(g)': 2}), ({'C2H4(g)': 1, 'H2(g)': 1}, {'C2H6(g)': 1}),
           ({'C2H4(g)': 1, 'H2O(g)': 1}, {'C2H5OH(l)': 1}), ({'CH3OH(l)': 2, 'O2(g)': 3}, {'CO2(g)': 2, 'H2O(l)': 4}), ({'Al(s)': 2, 'Fe2O3(s)': 1}, {'Al2O3(s)': 1, 'Fe(s)': 2}),
           ({'C3H8(g)': 1, 'O2(g)': 5}, {'CO2(g)': 3, 'H2O(l)': 4}), ({'C6H12O6(s)': 1, 'O2(g)': 6}, {'CO2(g)': 6, 'H2O(l)': 6}), ({'C2H2(g)': 1, 'H2(g)': 2}, {'C2H6(g)': 1}),
           ({'N2H4(l)': 1, 'O2(g)': 1}, {'N2(g)': 1, 'H2O(l)': 2}), ({'H2O2(l)': 2}, {'H2O(l)': 2, 'O2(g)': 1}), ({'CuO(s)': 1, 'H2(g)': 1}, {'Cu(s)': 1, 'H2O(l)': 1}),
           ({'PCl3(l)': 1, 'Cl2(g)': 1}, {'PCl5(s)': 1}), ({'C6H6(l)': 2, 'O2(g)': 15}, {'CO2(g)': 12, 'H2O(l)': 6}), ({'CH3COOH(l)': 1, 'O2(g)': 2}, {'CO2(g)': 2, 'H2O(l)': 2})]


def hf(sp):
    return HF.get(sp, 0)


def side(d):
    return ' + '.join(f'{"" if k == 1 else k}{chem(s)}' for s, k in d.items())


@R.add('ch09-st3', 'C3', (1, 5), 'numerical')
def c3_hess_hf(rng, slot):
    re_, pr = pick(rng, HESS_RX)
    dH = sum(k * hf(s) for s, k in pr.items()) - sum(k * hf(s) for s, k in re_.items())
    eq = f'{side(re_)} → {side(pr)}'
    used = [s for s in list(re_) + list(pr) if s in HF]
    tab = ', '.join(f'{chem(s)} {hf(s)}' for s in used)
    stem = pick(rng, [f'Calculate the standard enthalpy change for {eq}, using the following ΔHf⦵ values / kJ mol⁻¹: {tab}.', f'Using standard enthalpies of formation (kJ mol⁻¹: {tab}), determine ΔH⦵ for the reaction {eq}.'])
    rev = -dH
    nocoef = sum(hf(s) for s in pr) - sum(hf(s) for s in re_)
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Calculate the standard', 'What is the standard').replace('determine ΔH⦵', 'what is ΔH⦵'), dH, [rev, nocoef if nocoef != dH else dH + 2 * hf(used[0]), sum(k * hf(s) for s, k in pr.items()) + sum(k * hf(s) for s, k in re_.items())], 'kJ mol⁻¹',
                    f'ΔH = ΣΔHf(products) − ΣΔHf(reactants) = {sgn(dH)} kJ mol⁻¹ (elements = 0).', extra=False, signed=True)
    return num(stem, sgn(dH, 4, 'kJ mol⁻¹'), f'ΣΔHf(products) = {sum(k * hf(s) for s, k in pr.items())} (M1); ΣΔHf(reactants) = {sum(k * hf(s) for s, k in re_.items())} (M1); ΔH = {sgn(dH, 4, "kJ mol⁻¹")} (A1).', 3)


HC = {'C(s)': -394, 'H2(g)': -286, 'CH4(g)': -891, 'C2H6(g)': -1561, 'C3H8(g)': -2219, 'C4H10(g)': -2878, 'C2H4(g)': -1411, 'C2H2(g)': -1301,
      'CH3OH(l)': -726, 'C2H5OH(l)': -1367, 'C6H6(l)': -3268, 'C6H12O6(s)': -2803, 'CH3COOH(l)': -874, 'C8H18(l)': -5470, 'C3H7OH(l)': -2021}


@R.add('ch09-st3', 'C3', (2, 5), 'numerical')
def c3_hess_hc(rng, slot):
    sp = pick(rng, [s for s in HC if s not in ('C(s)', 'H2(g)')])
    a = atoms(sp.split('(')[0])
    nC, nH, nO = a.get('C', 0), a.get('H', 0), a.get('O', 0)
    dHf = nC * HC['C(s)'] + nH / 2 * HC['H2(g)'] - HC[sp]
    o2 = Fraction(nO, 2)
    eq = f'{nC if nC > 1 else ""}C(s) + {Fraction(nH, 2) if nH != 2 else ""}H₂(g)' + (f' + {o2 if o2 != 1 else ""}O₂(g)' if nO else '') + f' → {chem(sp)}'
    stem = (f'Calculate the standard enthalpy of formation of {chem(sp)}: {eq}, using the enthalpies of combustion / kJ mol⁻¹: C(s) {HC["C(s)"]}, H₂(g) {HC["H2(g)"]}, {chem(sp)} {HC[sp]}.')
    return num(stem, sgn(dHf, 3, 'kJ mol⁻¹'), f'ΔHf = ΣΔHc(reactants) − ΣΔHc(products) (M1) = {nC}({HC["C(s)"]}) + {nH / 2:g}({HC["H2(g)"]}) − ({HC[sp]}) (M1) = {sgn(dHf, 3, "kJ mol⁻¹")} (A1).', 3)


CYCLES = [
    ('C(s) + ½O₂(g) → CO(g)', [('C(s) + O₂(g) → CO₂(g)', -394, 1), ('CO(g) + ½O₂(g) → CO₂(g)', -283, -1)]),
    ('2C(s) + 3H₂(g) → C₂H₆(g)', [('C(s) + O₂(g) → CO₂(g)', -394, 2), ('H₂(g) + ½O₂(g) → H₂O(l)', -286, 3), ('C₂H₆(g) + 3½O₂(g) → 2CO₂(g) + 3H₂O(l)', -1561, -1)]),
    ('S(s) + 1½O₂(g) → SO₃(g)', [('S(s) + O₂(g) → SO₂(g)', -297, 1), ('2SO₂(g) + O₂(g) → 2SO₃(g)', -198, 0.5)]),
    ('N₂(g) + 2O₂(g) → 2NO₂(g)', [('N₂(g) + O₂(g) → 2NO(g)', 181, 1), ('2NO(g) + O₂(g) → 2NO₂(g)', -114, 1)]),
    ('C₂H₄(g) + H₂(g) → C₂H₆(g)', [('C₂H₄(g) + 3O₂(g) → 2CO₂(g) + 2H₂O(l)', -1411, 1), ('H₂(g) + ½O₂(g) → H₂O(l)', -286, 1), ('C₂H₆(g) + 3½O₂(g) → 2CO₂(g) + 3H₂O(l)', -1561, -1)]),
    ('2Fe(s) + 1½O₂(g) → Fe₂O₃(s)', [('2Al(s) + Fe₂O₃(s) → 2Fe(s) + Al₂O₃(s)', -852, -1), ('2Al(s) + 1½O₂(g) → Al₂O₃(s)', -1676, 1)]),
    ('CaO(s) + CO₂(g) → CaCO₃(s)', [('CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)', -17, -1), ('CaO(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l)', -195, 1)]),
    ('MgO(s) + 2HCl(aq) → MgCl₂(aq) + H₂O(l) from Mg data', [('Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)', -467, 1), ('H₂(g) + ½O₂(g) → H₂O(l)', -286, 1), ('Mg(s) + ½O₂(g) → MgO(s)', -602, -1)]),
    ('CuSO₄(s) + 5H₂O(l) → CuSO₄·5H₂O(s)', [('CuSO₄(s) + aq → CuSO₄(aq)', -66.5, 1), ('CuSO₄·5H₂O(s) + aq → CuSO₄(aq)', 11.7, -1)]),
    ('C(graphite) → C(diamond)', [('C(graphite) + O₂(g) → CO₂(g)', -393.5, 1), ('C(diamond) + O₂(g) → CO₂(g)', -395.4, -1)]),
]


@R.add('ch09-st3', 'C3', (2, 5), 'numerical')
def c3_hess_manip(rng, slot):
    target, steps = pick(rng, CYCLES)
    tgt = target.split(' from ')[0]
    dH = sum(v * k for _, v, k in steps)
    lines = '\n'.join(f'ΔH{i + 1} = {sgn(v)} kJ mol⁻¹: {e}' for i, (e, v, k) in enumerate(steps))
    stem = f'Use the following data to calculate ΔH for {tgt}.\n{lines}'
    ops = '; '.join(f'{"reverse " if k < 0 else ""}{"" if abs(k) == 1 else ("× " + format(abs(k), "g") + " ")}equation {i + 1}' for i, (_, _, k) in enumerate(steps))
    expr = ' + '.join(f'({format(k, "g")} × {sgn(v)})' for _, v, k in steps)
    return num(stem, sgn(dH, 4, 'kJ mol⁻¹'), f'Manipulate: {ops} (M1); ΔH = {expr} (M1) = {sgn(dH, 4, "kJ mol⁻¹")} (A1).', 3)


@R.add('ch09-st3', 'C4', (3, 5), 'multi_step')
def c4_hess_design(rng, slot):
    salt, f, hydr, w, d1, d2 = pick(rng, [('copper(II) sulfate', 'CuSO4', 'CuSO4.5H2O', 5, -66.5, 11.7), ('magnesium sulfate', 'MgSO4', 'MgSO4.7H2O', 7, -91.2, 16.1), ('sodium carbonate', 'Na2CO3', 'Na2CO3.10H2O', 10, -26.7, 67.9)])
    dH = d1 - d2
    stem = (f'The enthalpy change for {chem(f)}(s) + {w}H₂O(l) → {chem(hydr)}(s) cannot be measured directly. ΔH(solution) of anhydrous {salt} is {sgn(d1)} kJ mol⁻¹ and of the hydrate is {sgn(d2)} kJ mol⁻¹. '
            f'(a) Draw a Hess cycle linking the three enthalpy changes. (b) Calculate the enthalpy of hydration of the anhydrous salt. (c) Explain why this enthalpy change cannot be measured directly. (d) Suggest why the experimental values may be inaccurate.')
    return num(stem, f'(b) {sgn(dH, 3, "kJ mol⁻¹")}', f'(a) both solids → same aqueous solution (A1). (b) ΔH = ΔH(anhydrous) − ΔH(hydrate) = {d1} − ({d2}) (M1) = {sgn(dH, 3, "kJ mol⁻¹")} (A1). (c) cannot control exactly 5/7/10 mol water reacting; the solid would partly dissolve and the reaction is slow (R1). (d) heat loss in calorimetry; the anhydrous solid absorbs moisture before use (R1).', 5, 'multi_step')


R.mcqs('ch09-st3', 'C2', (1, 4), [
    ('Given ΔHf(CO₂) = −394 and ΔHf(CO) = −111 kJ mol⁻¹, what is ΔH for 2CO(g) + O₂(g) → 2CO₂(g)?', '−566 kJ mol⁻¹', ['−283 kJ mol⁻¹', '+566 kJ mol⁻¹', '−1010 kJ mol⁻¹'], '2(−394) − 2(−111).'),
    ('Which substance has ΔHf⦵ = 0?', 'Br₂(l)', ['Br₂(g)', 'O₃(g)', 'C(diamond)'], 'Standard state of bromine is liquid.'),
    ('What is the relationship between ΔH₁, ΔH₂ and ΔH₃ if A → B (ΔH₁), B → C (ΔH₂) and A → C (ΔH₃)?', 'ΔH₃ = ΔH₁ + ΔH₂', ['ΔH₃ = ΔH₁ − ΔH₂', 'ΔH₁ = ΔH₂ + ΔH₃', 'ΔH₃ = −(ΔH₁ + ΔH₂)'], 'Route independence.'),
])


R.facts('ch09-st4', F(
    terms=[('bond enthalpy', 'the energy required to break one mole of a covalent bond in gaseous molecules under standard conditions'),
           ('average bond enthalpy', 'the mean energy needed to break one mole of a given type of bond, averaged over many different compounds'),
           ('Born–Haber cycle', 'an energy cycle for the formation of an ionic compound from its elements, used to calculate lattice enthalpy (HL)'),
           ('electron affinity', 'the enthalpy change when one mole of electrons is added to one mole of gaseous atoms to form one mole of gaseous 1− ions'),
           ('enthalpy of atomisation', 'the enthalpy change when one mole of gaseous atoms is formed from the element in its standard state')],
    facts=[('Which expression gives ΔH from bond enthalpies?', 'Σ(bonds broken) − Σ(bonds formed)', ['Σ(bonds formed) − Σ(bonds broken)', 'Σ(bonds broken) + Σ(bonds formed)', 'ΣΔHf(products) − Σ(bonds broken)'], 'Breaking absorbs, forming releases.'),
           ('Why do ΔH values from average bond enthalpies differ from those using ΔHf data?', 'Average bond enthalpies are means over many compounds and apply only to gases.', ['Bond enthalpies are always negative.', 'Hess’s law does not apply.', 'Bond enthalpies include lattice energy.'], 'Approximation.'),
           ('The second electron affinity of oxygen is', 'endothermic, because an electron is added to a negative ion', ['exothermic, because oxygen is electronegative', 'zero', 'the same as the first'], 'Repulsion between O⁻ and the incoming electron.'),
           ('In a Born–Haber cycle for NaCl, which step is exothermic?', 'Cl(g) + e⁻ → Cl⁻(g)', ['Na(s) → Na(g)', 'Na(g) → Na⁺(g) + e⁻', '½Cl₂(g) → Cl(g)'], 'First electron affinity is negative.')],
    why=[('Explain why the enthalpy change for a reaction calculated from average bond enthalpies is only approximate.', 'Bond enthalpies are averaged over many compounds, but the actual strength of a bond depends on its molecular environment; the values also assume all species are gaseous.'),
         ('Explain why bond breaking is endothermic and bond making exothermic.', 'Energy must be supplied to overcome the attraction between the nuclei and the shared pair; when a bond forms, this attraction is established and energy is released.'),
         ('Explain why a Born–Haber cycle is needed to determine lattice enthalpy.', 'Lattice enthalpy (separating a solid into gaseous ions) cannot be measured directly; it is calculated from measurable quantities (ΔHf, atomisation, ionisation energies, electron affinities) using Hess’s law.')],
    contrast=[('bond enthalpy', 'lattice enthalpy', 'Bond enthalpy is the energy to break one mole of a covalent bond in gaseous molecules; lattice enthalpy is the energy to separate one mole of an ionic solid into gaseous ions.')],
    misc=[('The reaction is exothermic because more bonds are broken than made.', 'The sign depends on the energies, not the number of bonds: exothermic if the bonds formed release more energy than is needed to break those broken.'),
          ('Average bond enthalpies can be used for reactions involving liquids such as water(l) without correction.', 'Bond enthalpies refer to the gaseous state; condensation enthalpy must be included for liquids.')],
    evaluate=[('Bond enthalpy calculations are a reliable way to find enthalpies of reaction.', ['quick estimates when ΔHf data are unavailable', 'give insight into which bonds dominate the energy change'], ['average values ignore molecular environment (errors of 5–10 %)', 'valid only for gases', 'cannot be used for ionic or metallic substances'], 'Useful estimates, but ΔHf-based Hess calculations are more accurate.')],
))

BE_RX = [('CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(g)', {'C-H': 4, 'O=O': 2}, {'C=O': 2, 'O-H': 4}),
         ('C₂H₄(g) + H₂(g) → C₂H₆(g)', {'C=C': 1, 'H-H': 1}, {'C-C': 1, 'C-H': 2}),
         ('H₂(g) + Cl₂(g) → 2HCl(g)', {'H-H': 1, 'Cl-Cl': 1}, {'H-Cl': 2}),
         ('H₂(g) + Br₂(g) → 2HBr(g)', {'H-H': 1, 'Br-Br': 1}, {'H-Br': 2}),
         ('N₂(g) + 3H₂(g) → 2NH₃(g)', {'N≡N': 1, 'H-H': 3}, {'N-H': 6}),
         ('C₂H₄(g) + Br₂(g) → C₂H₄Br₂(g)', {'C=C': 1, 'Br-Br': 1}, {'C-C': 1, 'C-Br': 2}),
         ('CH₄(g) + Cl₂(g) → CH₃Cl(g) + HCl(g)', {'C-H': 1, 'Cl-Cl': 1}, {'C-Cl': 1, 'H-Cl': 1}),
         ('2H₂(g) + O₂(g) → 2H₂O(g)', {'H-H': 2, 'O=O': 1}, {'O-H': 4}),
         ('C₃H₈(g) + 5O₂(g) → 3CO₂(g) + 4H₂O(g)', {'C-C': 2, 'C-H': 8, 'O=O': 5}, {'C=O': 6, 'O-H': 8}),
         ('C₂H₂(g) + 2H₂(g) → C₂H₆(g)', {'C≡C': 1, 'H-H': 2}, {'C-C': 1, 'C-H': 4}),
         ('H₂(g) + F₂(g) → 2HF(g)', {'H-H': 1, 'F-F': 1}, {'H-F': 2}),
         ('N₂H₄(g) + O₂(g) → N₂(g) + 2H₂O(g)', {'N-N': 1, 'N-H': 4, 'O=O': 1}, {'N≡N': 1, 'O-H': 4}),
         ('C₂H₅OH(g) + 3O₂(g) → 2CO₂(g) + 3H₂O(g)', {'C-C': 1, 'C-H': 5, 'C-O': 1, 'O-H': 1, 'O=O': 3}, {'C=O': 4, 'O-H': 6}),
         ('C₂H₄(g) + H₂O(g) → C₂H₅OH(g)', {'C=C': 1, 'O-H': 1}, {'C-C': 1, 'C-H': 1, 'C-O': 1}),
         ('2H₂O₂(g) → 2H₂O(g) + O₂(g)', {'O-O': 2}, {'O=O': 1}),
         ('H₂(g) + I₂(g) → 2HI(g)', {'H-H': 1, 'I-I': 1}, {'H-I': 2}),
         ('CH₄(g) + 4Cl₂(g) → CCl₄(g) + 4HCl(g)', {'C-H': 4, 'Cl-Cl': 4}, {'C-Cl': 4, 'H-Cl': 4})]


def be_txt(d):
    return ' + '.join(f'{k} × {b.replace("-", "–")} ({BE[b]})' if k > 1 else f'{b.replace("-", "–")} ({BE[b]})' for b, k in d.items())


@R.add('ch09-st4', 'C3', (1, 5), 'numerical')
def c3_bond_enthalpy(rng, slot):
    eq, br, fo = pick(rng, BE_RX)
    sb = sum(BE[b] * k for b, k in br.items())
    sf_ = sum(BE[b] * k for b, k in fo.items())
    dH = sb - sf_
    stem = pick(rng, [f'Using average bond enthalpies from the data booklet, calculate ΔH for {eq}.', f'Estimate the enthalpy change for the reaction {eq} using the bond enthalpies (kJ mol⁻¹) in the data booklet.'])
    if slot.d <= 2:
        bonds = sorted(set(br) | set(fo))
        stem += ' (Bond enthalpies / kJ mol⁻¹: ' + ', '.join(f'{b.replace("-", "–")} {BE[b]}' for b in bonds) + ')'
        return nmcq(rng, stem.replace('calculate ΔH', 'what is ΔH').replace('Estimate the enthalpy change', 'What is the enthalpy change'), dH, [-dH, sb + sf_, sum(BE[b] for b in br) - sum(BE[b] for b in fo)], 'kJ mol⁻¹',
                    f'Broken: {sb}; formed: {sf_}; ΔH = {sb} − {sf_} = {sgn(dH)} kJ mol⁻¹.', extra=False, signed=True)
    return num(stem, sgn(dH, 4, 'kJ mol⁻¹'), f'bonds broken = {be_txt(br)} = {sb} kJ (M1); bonds formed = {be_txt(fo)} = {sf_} kJ (M1); ΔH = {sb} − {sf_} = {sgn(dH, 4, "kJ mol⁻¹")} (A1).', 3)


BH = [('NaCl', 'Na', 'Cl', -411, 107, [496], 121, [-349], 1, 1), ('KCl', 'K', 'Cl', -437, 89, [419], 121, [-349], 1, 1),
      ('NaBr', 'Na', 'Br', -361, 107, [496], 112, [-325], 1, 1), ('LiF', 'Li', 'F', -616, 159, [520], 79, [-328], 1, 1),
      ('MgO', 'Mg', 'O', -602, 148, [738, 1451], 249, [-141, 753], 1, 1), ('MgCl2', 'Mg', 'Cl', -641, 148, [738, 1451], 121, [-349], 1, 2),
      ('CaCl2', 'Ca', 'Cl', -796, 178, [590, 1145], 121, [-349], 1, 2), ('KBr', 'K', 'Br', -394, 89, [419], 112, [-325], 1, 1),
      ('CaO', 'Ca', 'O', -635, 178, [590, 1145], 249, [-141, 753], 1, 1), ('NaF', 'Na', 'F', -574, 107, [496], 79, [-328], 1, 1)]


@R.add('ch09-st4', 'C3', (3, 5), 'numerical')
def c3_born_haber(rng, slot):
    f, m, x, dHf, atm, ies, atx, eas, nm_, nx = pick(rng, BH)
    le = -dHf + atm + sum(ies) + nx * atx + nx * sum(eas)
    data = (f'ΔHf({chem(f)}) = {dHf}; atomisation of {m} = +{atm}; ionisation energ{"ies" if len(ies) > 1 else "y"} of {m} = ' + ', '.join(f'+{v}' for v in ies) +
            f'; atomisation of {x} (per mole of {x} atoms) = +{atx}; electron affinit{"ies" if len(eas) > 1 else "y"} of {x} = ' + ', '.join(sgn(v) for v in eas) + ' (all kJ mol⁻¹)')
    stem = f'Use the following data to calculate the lattice enthalpy of {chem(f)} (HL): {data}.'
    expr = f'−({dHf}) + {atm} + {" + ".join(str(v) for v in ies)} + {nx} × {atx} + {nx} × ({" + ".join(str(v) for v in eas)})'
    if slot.d <= 3:
        return nmcq(rng, stem.replace('calculate the lattice', 'what is the lattice').rstrip('.') + '?', le, [le + 2 * dHf, -le, le - 2 * nx * sum(eas)], 'kJ mol⁻¹', f'ΔH(lattice) = {expr} = {sgn(le)} kJ mol⁻¹ (endothermic as defined).', extra=False, signed=True)
    return num(stem, sgn(le, 4, 'kJ mol⁻¹'), f'Cycle: ΔHf = atomisations + IEs + EAs − ΔH(lattice) (M1); ΔH(lattice) = {expr} (M1) = {sgn(le, 4, "kJ mol⁻¹")} (A1).', 3)


@R.add('ch09-st4', 'C4', (3, 5), 'multi_step')
def c4_be_vs_hf(rng, slot):
    eq, br, fo = pick(rng, [r for r in BE_RX if 'O₂' in r[0] and 'H₂O(g)' in r[0] and 'H₂O₂' not in r[0]])
    dHbe = sum(BE[b] * k for b, k in br.items()) - sum(BE[b] * k for b, k in fo.items())
    match = {'CH₄': ({'CH4(g)': 1, 'O2(g)': 2}, {'CO2(g)': 1, 'H2O(g)': 2}), 'C₃H₈': ({'C3H8(g)': 1, 'O2(g)': 5}, {'CO2(g)': 3, 'H2O(g)': 4}),
             '2H₂': ({'H2(g)': 2, 'O2(g)': 1}, {'H2O(g)': 2})}
    key = next((k for k in match if eq.startswith(k)), None)
    if not key:
        return None
    re_, pr = match[key]
    dHf_ = sum(k * hf(s) for s, k in pr.items()) - sum(k * hf(s) for s, k in re_.items())
    stem = (f'For {eq}: (a) calculate ΔH using average bond enthalpies; (b) calculate ΔH using ΔHf⦵ values (CO₂(g) −394, H₂O(g) −242, CH₄(g) −74, C₃H₈(g) −105 kJ mol⁻¹); '
            f'(c) explain why the two values differ; (d) state which value is more reliable.')
    return num(stem, f'(a) {sgn(dHbe)} kJ mol⁻¹; (b) {sgn(dHf_)} kJ mol⁻¹', f'(a) broken − formed = {sgn(dHbe)} kJ mol⁻¹ (M1 A1). (b) ΣΔHf(products) − ΣΔHf(reactants) = {sgn(dHf_)} kJ mol⁻¹ (M1 A1). (c) bond enthalpies are averages from many compounds, not specific to these molecules (R1). (d) ΔHf value – based on measured data for the actual substances (R1).', 6, 'multi_step')


R.mcqs('ch09-st4', 'C2', (1, 4), [
    ('Which bond requires the most energy to break?', 'N≡N', ['O=O', 'C=C', 'H–H'], '945 kJ mol⁻¹.'),
    ('Why is the lattice enthalpy of MgO much greater than that of NaCl?', 'Mg²⁺ and O²⁻ have higher charges and smaller radii.', ['MgO has covalent bonds.', 'Mg has a lower ionisation energy.', 'O has a more exothermic first electron affinity.'], 'Charge density.'),
    ('Which process is represented by the first electron affinity of chlorine?', 'Cl(g) + e⁻ → Cl⁻(g)', ['½Cl₂(g) + e⁻ → Cl⁻(g)', 'Cl⁻(g) → Cl(g) + e⁻', 'Cl₂(g) + 2e⁻ → 2Cl⁻(g)'], 'Gaseous atoms.'),
])


# =============================================================================================
# ch10 R1.3 Energy from fuels
# =============================================================================================
FUELS = [('methane', 'CH4', -891, None, 'g'), ('ethane', 'C2H6', -1561, None, 'g'), ('propane', 'C3H8', -2219, None, 'g'), ('butane', 'C4H10', -2878, None, 'g'),
         ('pentane', 'C5H12', -3509, 0.626, 'l'), ('hexane', 'C6H14', -4163, 0.655, 'l'), ('octane', 'C8H18', -5470, 0.703, 'l'), ('methanol', 'CH3OH', -726, 0.792, 'l'),
         ('ethanol', 'C2H5OH', -1367, 0.789, 'l'), ('propan-1-ol', 'C3H7OH', -2021, 0.803, 'l'), ('butan-1-ol', 'C4H9OH', -2676, 0.810, 'l'), ('hydrogen', 'H2', -286, None, 'g'),
         ('glucose', 'C6H12O6', -2803, None, 's'), ('benzene', 'C6H6', -3268, 0.876, 'l')]

R.facts('ch10-st1', F(
    terms=[('complete combustion', 'burning a fuel in a plentiful supply of oxygen, so that carbon is fully oxidised to carbon dioxide and hydrogen to water'),
           ('incomplete combustion', 'burning a fuel in a limited supply of oxygen, producing carbon monoxide and/or carbon (soot) as well as water'),
           ('specific energy', 'the energy released per unit mass of fuel, in kJ kg⁻¹ (or kJ g⁻¹)'),
           ('energy density', 'the energy released per unit volume of fuel, in kJ dm⁻³ (or kJ cm⁻³)'),
           ('fuel', 'a substance that releases useful energy when it reacts, usually by combustion with oxygen')],
    facts=[('Which product forms in incomplete but not in complete combustion of a hydrocarbon?', 'carbon monoxide', ['carbon dioxide', 'water', 'oxygen'], 'Limited oxygen.'),
           ('Why is carbon monoxide toxic?', 'It binds strongly to haemoglobin, reducing oxygen transport in the blood.', ['It is acidic.', 'It causes acid rain.', 'It depletes ozone.'], 'Carboxyhaemoglobin.'),
           ('Which fuel has the highest specific energy?', 'hydrogen', ['octane', 'ethanol', 'coal'], 'About 142 kJ g⁻¹.'),
           ('What is the main observation when a hydrocarbon burns with insufficient oxygen?', 'a yellow, smoky (sooty) flame', ['a blue flame', 'no flame', 'a colourless flame with no residue'], 'Carbon particles glow and form soot.')],
    why=[('Explain why hydrogen has a very high specific energy but a low energy density as a gas.', 'Hydrogen has a very low molar mass (2.02 g mol⁻¹), so a large amount of energy is released per gram, but as a gas at room pressure it occupies a large volume, so energy per dm³ is low unless compressed or liquefied.'),
         ('Explain why alcohols release less energy per mole than alkanes with the same number of carbon atoms.', 'Alcohols are already partially oxidised (contain an O atom); fewer bonds to oxygen are formed on combustion, so less energy is released.'),
         ('Explain why incomplete combustion releases less energy than complete combustion.', 'Carbon is only partly oxidised (to CO or C), so fewer strong C=O bonds are formed in CO₂ and less energy is released overall.')],
    contrast=[('specific energy', 'energy density', 'Specific energy is energy released per unit mass (kJ kg⁻¹); energy density is energy released per unit volume (kJ dm⁻³); they differ depending on the density of the fuel.'),
              ('complete combustion', 'incomplete combustion', 'Complete combustion in excess oxygen gives CO₂ and H₂O and releases maximum energy; incomplete combustion in limited oxygen gives CO and/or C as well, and releases less energy.')],
    misc=[('Fuels with the highest enthalpy of combustion per mole are always the best fuels for cars.', 'Practical choice depends on specific energy, energy density, cost, safety, emissions and availability; per-mole values favour large molecules but per-mass values may not.')],
    evaluate=[('Energy density is more important than specific energy when choosing a fuel for vehicles.', ['fuel tanks have limited volume', 'liquid fuels like petrol and diesel have high energy density'], ['mass matters for aircraft and rockets', 'specific energy and safety both affect range and efficiency', 'cost and emissions are major factors'], 'For road vehicles energy density is critical, for aircraft both matter; the best choice balances energy, safety, cost and environmental impact.')],
))


@R.add('ch10-st1', 'C3', (1, 5), 'numerical')
def c3_specific_energy(rng, slot):
    nm, f, dH, rho, st_ = pick(rng, FUELS)
    M = mr(f)
    se = -dH / M  # kJ g-1
    kind = rng.choice(['se', 'ed', 'mass', 'energy'])
    if kind == 'ed' and rho:
        ed = se * rho * 1000  # kJ dm-3
        stem = f'The enthalpy of combustion of {nm} is {dH} kJ mol⁻¹ and its density is {rho} g cm⁻³. Calculate its energy density in kJ dm⁻³.'
        return num(stem, q(ed, 'kJ dm⁻³'), f'specific energy = {-dH}/{M:.2f} = {sf(se)} kJ g⁻¹ (M1); × {rho} g cm⁻³ × 1000 cm³ dm⁻³ (M1) = {q(ed, "kJ dm⁻³")} (A1).', 3)
    if kind == 'mass':
        E = rng.choice([1000, 5000, 10000, 50000, 2.5e5])
        m = E / se
        stem = f'Calculate the minimum mass of {nm} ({chem(f)}, ΔHc = {sgn(dH, 4)} kJ mol⁻¹) that must be burned to release {sf(E)} kJ of energy.'
        return num(stem, q(m, 'g'), f'n = {sf(E)}/{-dH} = {sf(E / -dH)} mol (M1); m = n × {M:.2f} = {q(m, "g")} (A1).', 2)
    if kind == 'energy':
        m = rng.choice([1.00, 5.00, 10.0, 100, 1000])
        E = m / M * -dH
        stem = f'Calculate the energy released when {sf(m)} g of {nm} is burned completely (ΔHc = {sgn(dH, 4)} kJ mol⁻¹).'
        return nmcq(rng, f'What energy is released when {sf(m)} g of {nm} is burned completely, given ΔHc = {sgn(dH, 4)} kJ mol⁻¹?', E, [m * -dH, E / 1000, m * M * -dH / 1000], 'kJ', f'n = {sf(m)}/{M:.2f}; E = n × {-dH} = {sf(E)} kJ.', extra=False)
    stem = f'Calculate the specific energy of {nm}, {chem(f)}, in kJ g⁻¹, given ΔHc = {sgn(dH, 4)} kJ mol⁻¹.'
    return num(stem, q(se, 'kJ g⁻¹'), f'specific energy = |ΔHc|/M = {-dH}/{M:.2f} (M1) = {q(se, "kJ g⁻¹")} (A1).', 2)


@R.add('ch10-st1', 'C3', (1, 4), 'short')
def c3_incomplete(rng, slot):
    nm, n = pick(rng, ALKANES[:8] + ALCOHOLS[:4])
    alc = (nm, n) in ALCOHOLS
    f, c, h, o = fuel_formula(n, alc)
    prod = rng.choice(['CO', 'C'])
    # balance CxHyOz + a O2 -> x P + y/2 H2O  (P = CO or C)
    oatoms = (c if prod == 'CO' else 0) + Fraction(h, 2) - o
    a = Fraction(oatoms, 2)
    k = 1
    while (a * k).denominator != 1 or (Fraction(h, 2) * k).denominator != 1:
        k += 1
    eq = f'{"" if k == 1 else k}{chem(f)} + {a * k}O₂ → {c * k}{"CO" if prod == "CO" else "C"} + {Fraction(h, 2) * k}H₂O'
    stem = f'Write a balanced equation for the incomplete combustion of {nm} to form {"carbon monoxide" if prod == "CO" else "carbon (soot)"} and water.'
    return dict(stem=stem, answer=eq, markingKey=f'Correct products (1); balanced: {eq} (1).', type='short', marks=2)


@R.add('ch10-st1', 'C4', (3, 5), 'multi_step')
def c4_fuel_compare(rng, slot):
    a, b = rng.sample([x for x in FUELS if x[3]], 2)
    sa, sb = -a[2] / mr(a[1]), -b[2] / mr(b[1])
    ea, eb = sa * a[3] * 1000, sb * b[3] * 1000
    stem = (f'Compare {a[0]} (ΔHc = {a[2]} kJ mol⁻¹, density {a[3]} g cm⁻³) and {b[0]} (ΔHc = {b[2]} kJ mol⁻¹, density {b[3]} g cm⁻³) as fuels. '
            f'(a) Calculate the specific energy and energy density of each. (b) Deduce which fuel would allow a car with a 50 dm³ tank to travel further. (c) Discuss one other factor that should be considered.')
    better = a[0] if ea > eb else b[0]
    return num(stem, f'(a) {a[0]}: {sf(sa)} kJ g⁻¹, {sf(ea)} kJ dm⁻³; {b[0]}: {sf(sb)} kJ g⁻¹, {sf(eb)} kJ dm⁻³; (b) {better}',
               f'(a) specific energies {sf(sa)} and {sf(sb)} kJ g⁻¹ (A1 A1); energy densities {sf(ea)} and {sf(eb)} kJ dm⁻³ (A1). (b) {better} – higher energy per volume (R1). (c) e.g. CO₂ per kJ, renewable source, cost, toxicity, volatility (R1).', 5, 'multi_step')


R.mcqs('ch10-st1', 'C2', (1, 4), [
    ('Why do longer-chain alkanes have more exothermic enthalpies of combustion per mole?', 'Each extra CH₂ adds bonds whose combustion releases more energy.', ['They have stronger intermolecular forces.', 'They burn more completely.', 'They have lower molar masses.'], 'About 650 kJ mol⁻¹ per CH₂.'),
    ('Which fuel produces the least CO₂ per kJ of energy released?', 'methane', ['octane', 'coal', 'ethanol'], 'Highest H:C ratio.'),
    ('A gas boiler produces a yellow flame and soot. What is the most likely cause?', 'insufficient oxygen supply', ['too much oxygen', 'the gas is hydrogen', 'the gas is pure methane'], 'Incomplete combustion.'),
])


R.facts('ch10-st2', F(
    terms=[('fossil fuel', 'a fuel (coal, crude oil, natural gas) formed over millions of years from the remains of ancient organisms; non-renewable'),
           ('biofuel', 'a fuel produced from recently living biomass, such as bioethanol or biodiesel; considered renewable'),
           ('greenhouse gas', 'a gas such as CO₂, CH₄ or H₂O that absorbs and re-emits infrared radiation, warming the lower atmosphere'),
           ('carbon neutral', 'describing a process with no net release of CO₂ to the atmosphere over its life cycle'),
           ('transesterification', 'the reaction of a vegetable oil (triglyceride) with an alcohol such as methanol, catalysed by a base, to produce biodiesel (methyl esters) and glycerol')],
    facts=[('Which fossil fuel releases the most CO₂ per unit of energy produced?', 'coal', ['natural gas', 'crude oil', 'all release the same'], 'Coal is mainly carbon with little hydrogen.'),
           ('How does carbon dioxide act as a greenhouse gas?', 'It absorbs infrared radiation emitted by the Earth’s surface, which changes its bond vibrations.', ['It absorbs ultraviolet radiation from the Sun.', 'It reflects visible light.', 'It destroys ozone.'], 'IR-active vibrations (bending, asymmetric stretch).'),
           ('Which equation represents the fermentation of glucose to make bioethanol?', 'C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', ['C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', 'C₂H₄ + H₂O → C₂H₅OH', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂'], 'Anaerobic yeast respiration.'),
           ('Which is a disadvantage of biofuels?', 'Land used for fuel crops may compete with food production.', ['They are non-renewable.', 'They contain sulfur.', 'They cannot be used in engines.'], 'Food vs fuel.')],
    why=[('Explain why bioethanol is described as carbon neutral in principle but not in practice.', 'CO₂ released on burning equals that absorbed by the crop during photosynthesis, but fossil fuels are used in farming, fertiliser production, transport and distillation, so there is a net release.'),
         ('Explain how the combustion of fossil fuels contributes to climate change.', 'Burning releases CO₂ that had been locked away for millions of years; increased atmospheric CO₂ absorbs more of the infrared radiation emitted by Earth, enhancing the greenhouse effect and raising average temperatures.'),
         ('Explain why burning coal can cause acid rain.', 'Coal contains sulfur compounds which burn to SO₂; SO₂ is oxidised and dissolves in rainwater forming sulfuric acid (and H₂SO₃).')],
    contrast=[('fossil fuels', 'biofuels', 'Fossil fuels formed over millions of years and are finite, releasing ancient carbon; biofuels come from recent biomass, are renewable and recycle atmospheric carbon (in principle carbon neutral).')],
    misc=[('Biofuels produce no carbon dioxide when burned.', 'Biofuels release CO₂ on combustion; the claimed benefit is that a similar amount was recently absorbed during plant growth.'),
          ('The greenhouse effect is caused by the hole in the ozone layer.', 'These are separate issues: the greenhouse effect is IR absorption by gases such as CO₂ and CH₄; ozone depletion involves UV and CFCs.')],
    cases=[('Brazil’s sugar-cane ethanol programme', 'Since the 1970s most Brazilian cars run on ethanol or ethanol–petrol blends made by fermenting sugar cane.', 'biofuels as alternatives to fossil fuels', 'Reduced oil imports and net CO₂ emissions, but raised concerns about land use and deforestation.'),
           ('the Keeling curve measured at Mauna Loa, Hawaii', 'Atmospheric CO₂ rose from about 315 ppm in 1958 to over 420 ppm today.', 'the impact of fossil-fuel combustion', 'Direct evidence that human combustion of fossil fuels is increasing greenhouse gas concentrations.'),
           ('the 1952 Great Smog of London', 'Coal smoke and SO₂ trapped by a temperature inversion caused thousands of deaths.', 'environmental impact of fossil fuels', 'Incomplete combustion particulates and sulfur oxides from coal have severe health effects.')],
    evaluate=[('Replacing petrol with bioethanol will solve the problem of climate change from transport.', ['renewable, reduces fossil carbon emissions', 'can be blended with petrol in existing cars'], ['farming and processing still emit CO₂ and N₂O', 'land use competes with food and drives deforestation', 'lower energy density means more fuel needed'], 'Bioethanol can reduce emissions but cannot alone solve the problem; electrification, efficiency and reduced demand are also needed.'),
              ('Natural gas is a suitable “bridge fuel” in the transition from coal to renewables.', ['about half the CO₂ per kWh of coal', 'flexible power generation backing up renewables'], ['methane leakage is a potent greenhouse gas (about 80 × CO₂ over 20 years)', 'locks in fossil infrastructure', 'still a non-renewable fossil fuel'], 'It reduces emissions relative to coal only if methane leakage is minimised and it is phased out on a clear timetable.')],
))


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def c3_co2_per_kj(rng, slot):
    a, b = rng.sample([x for x in FUELS if 'C' in atoms(x[1])], 2)
    ca, cb = atoms(a[1])['C'], atoms(b[1])['C']
    ra = ca * mr('CO2') / -a[2] * 1000  # g CO2 per MJ
    rb = cb * mr('CO2') / -b[2] * 1000
    if slot.d <= 2:
        stem = f'Calculate the mass of CO₂ produced per MJ of energy released when {a[0]} (ΔHc = {a[2]} kJ mol⁻¹) burns completely.'
        return num(stem, q(ra, 'g MJ⁻¹'), f'{ca} mol CO₂ (= {ca * mr("CO2"):.2f} g) per {-a[2]} kJ (M1); per 1000 kJ = {q(ra, "g")} (A1).', 2)
    better = a[0] if ra < rb else b[0]
    stem = (f'Compare {a[0]} (ΔHc = {a[2]} kJ mol⁻¹) and {b[0]} (ΔHc = {b[2]} kJ mol⁻¹) by calculating the mass of CO₂ produced per MJ of energy released. Deduce which has the lower carbon footprint per unit energy.')
    return num(stem, f'{a[0]} {sf(ra)} g MJ⁻¹; {b[0]} {sf(rb)} g MJ⁻¹; {better}', f'mol CO₂ per mol fuel from formula (M1); {sf(ra)} and {sf(rb)} g CO₂ per MJ (A1 A1); {better} lower (A1).', 4, 'multi_step')


@R.add('ch10-st2', 'C3', (2, 5), 'numerical')
def c3_journey(rng, slot):
    fuel, f, dH, rho, _ = pick(rng, [x for x in FUELS if x[3] and 'C' in atoms(x[1])])
    V = rng.choice([5.0, 10.0, 20.0, 40.0, 50.0])
    m = V * 1000 * rho
    n = m / mr(f)
    co2 = n * atoms(f)['C'] * mr('CO2') / 1000
    stem = f'A vehicle uses {V:g} dm³ of {fuel} ({chem(f)}, density {rho} g cm⁻³) on a journey. Calculate the mass of CO₂, in kg, released assuming complete combustion.'
    return num(stem, q(co2, 'kg'), f'm(fuel) = {V:g} × 1000 × {rho} = {sf(m)} g (M1); n = {sf(n)} mol (M1); n(CO₂) = {atoms(f)["C"]} × n; m(CO₂) = {q(co2, "kg")} (A1).', 3)


R.mcqs('ch10-st2', 'C2', (1, 4), [
    ('Which property of a molecule allows it to act as a greenhouse gas?', 'It absorbs infrared radiation because its vibrations change the dipole moment.', ['It is non-polar.', 'It absorbs ultraviolet radiation.', 'It has a high molar mass.'], 'IR-active.'),
    ('Which gas is NOT a greenhouse gas?', 'nitrogen', ['methane', 'water vapour', 'dinitrogen monoxide'], 'N₂ has no IR-active vibrations.'),
    ('Which is produced when biodiesel is made by transesterification?', 'glycerol', ['ethanol', 'carbon dioxide', 'glucose'], 'Triglyceride + 3CH₃OH → 3 methyl esters + glycerol.'),
])


R.facts('ch10-st3', F(
    terms=[('fuel cell', 'an electrochemical cell that converts the chemical energy of a continuously supplied fuel and oxidant directly into electrical energy'),
           ('hydrogen fuel cell', 'a fuel cell in which hydrogen is oxidised at the anode and oxygen reduced at the cathode, with water as the only product'),
           ('electrolyte (in a fuel cell)', 'the ion-conducting medium, such as a proton-exchange membrane or aqueous KOH, that allows ions to move between electrodes'),
           ('efficiency of a fuel cell', 'the ratio of useful electrical energy produced to the energy released by the reaction (often ΔG/ΔH)')],
    facts=[('What is the overall reaction in a hydrogen fuel cell?', '2H₂ + O₂ → 2H₂O', ['2H₂O → 2H₂ + O₂', 'H₂ + Cl₂ → 2HCl', 'CH₄ + 2O₂ → CO₂ + 2H₂O'], 'Same as combustion but without flame.'),
           ('In an acidic (PEM) hydrogen fuel cell, what is the anode half-equation?', 'H₂ → 2H⁺ + 2e⁻', ['O₂ + 4H⁺ + 4e⁻ → 2H₂O', '2H⁺ + 2e⁻ → H₂', 'H₂ + 2OH⁻ → 2H₂O + 2e⁻'], 'Oxidation at the anode.'),
           ('In an alkaline hydrogen fuel cell, what is the cathode half-equation?', 'O₂ + 2H₂O + 4e⁻ → 4OH⁻', ['H₂ + 2OH⁻ → 2H₂O + 2e⁻', 'O₂ + 4H⁺ + 4e⁻ → 2H₂O', '4OH⁻ → O₂ + 2H₂O + 4e⁻'], 'Reduction of oxygen.'),
           ('What are the products of a methanol fuel cell?', 'carbon dioxide and water', ['only water', 'carbon monoxide and hydrogen', 'methanal'], 'CH₃OH + 1½O₂ → CO₂ + 2H₂O.')],
    why=[('Explain why fuel cells are more efficient than combustion engines for converting chemical energy into useful work.', 'They convert chemical energy directly into electrical energy without first producing heat, so they are not limited by the heat-engine (Carnot) efficiency; less energy is wasted as heat.'),
         ('Explain why a hydrogen fuel cell does not run down like a primary cell.', 'Reactants are supplied continuously from external tanks and products removed; the electrodes are not consumed.'),
         ('Explain why hydrogen fuel cell vehicles are only truly “zero emission” if the hydrogen is made using renewable energy.', 'Most hydrogen is made by steam reforming of methane (releasing CO₂); only if it is made by electrolysis powered by renewables are life-cycle emissions low.')],
    contrast=[('a fuel cell', 'a primary cell', 'A fuel cell has reactants supplied continuously and can operate indefinitely; a primary cell contains a fixed amount of reactants and stops when they are used up, and cannot be recharged.')],
    misc=[('Hydrogen fuel cells produce electricity by burning hydrogen.', 'There is no combustion: hydrogen is oxidised electrochemically at the anode and electrons flow through the external circuit.')],
    evaluate=[('Hydrogen fuel cells are the best option for future transport.', ['only water emitted at point of use', 'fast refuelling and long range compared with batteries', 'high efficiency'], ['hydrogen storage requires high pressure or very low temperature', 'most hydrogen comes from fossil fuels', 'catalysts use expensive platinum', 'infrastructure is limited'], 'Promising for heavy transport, but batteries currently suit cars better; green hydrogen production is the key condition.')],
))


@R.add('ch10-st3', 'C3', (1, 5), 'numerical')
def c3_fuel_cell(rng, slot):
    kind = rng.choice(['eff', 'energy', 'mass'])
    if kind == 'eff':
        fuel, dH, dG = pick(rng, [('hydrogen', -286, -237), ('methanol', -726, -702), ('hydrogen (water vapour product)', -242, -229)])
        eff = dG / dH * 100
        stem = f'For a {fuel} fuel cell, ΔH = {dH} kJ mol⁻¹ and ΔG = {dG} kJ mol⁻¹. Calculate the maximum theoretical efficiency.'
        return num(stem, f'{eff:.0f} %', f'efficiency = ΔG/ΔH × 100 (M1) = {dG}/{dH} × 100 = {eff:.0f} % (A1).', 2)
    if kind == 'energy':
        m = rng.choice([1.00, 5.00, 10.0, 100, 500])
        eff = rng.choice([40, 50, 55, 60])
        E = m / mr('H2') * 286 * eff / 100
        stem = f'A hydrogen fuel cell operates at {eff} % efficiency. Calculate the electrical energy produced from {m:g} g of hydrogen (ΔHc of H₂ = −286 kJ mol⁻¹).'
        return num(stem, q(E, 'kJ'), f'n(H₂) = {m:g}/2.02 = {sf(m / 2.02)} mol (M1); energy released = {sf(m / 2.02 * 286)} kJ (M1); × {eff}/100 = {q(E, "kJ")} (A1).', 3)
    E = rng.choice([1000, 5000, 20000, 1e5])
    eff = rng.choice([45, 50, 60])
    m = E / (286 * eff / 100) * mr('H2')
    stem = f'Calculate the mass of hydrogen needed by a fuel cell of efficiency {eff} % to supply {sf(E)} kJ of electrical energy (ΔHc(H₂) = −286 kJ mol⁻¹).'
    return num(stem, q(m, 'g'), f'energy needed from reaction = {sf(E)}/{eff / 100} = {sf(E / (eff / 100))} kJ (M1); n = /286 = {sf(m / 2.02)} mol (M1); m = {q(m, "g")} (A1).', 3)


@R.add('ch10-st3', 'C3', (2, 5), 'short')
def c3_fc_half(rng, slot):
    kind, an, ca, ov = pick(rng, [('acidic (proton exchange membrane) hydrogen', 'H₂ → 2H⁺ + 2e⁻', 'O₂ + 4H⁺ + 4e⁻ → 2H₂O', '2H₂ + O₂ → 2H₂O'),
                                  ('alkaline hydrogen', 'H₂ + 2OH⁻ → 2H₂O + 2e⁻', 'O₂ + 2H₂O + 4e⁻ → 4OH⁻', '2H₂ + O₂ → 2H₂O'),
                                  ('acidic methanol', 'CH₃OH + H₂O → CO₂ + 6H⁺ + 6e⁻', 'O₂ + 4H⁺ + 4e⁻ → 2H₂O', '2CH₃OH + 3O₂ → 2CO₂ + 4H₂O')])
    stem = f'For an {kind} fuel cell, write the half-equations at the anode and cathode and the overall equation. State the direction of electron flow in the external circuit.'
    return dict(stem=stem, answer=f'anode: {an}; cathode: {ca}; overall: {ov}; electrons flow from anode to cathode', markingKey=f'anode (oxidation) {an} (1); cathode (reduction) {ca} (1); overall {ov} (1); electrons anode → cathode (1).', type='short', marks=4)


R.mcqs('ch10-st3', 'C2', (1, 4), [
    ('In a hydrogen fuel cell, at which electrode does oxidation occur?', 'the anode, where hydrogen is supplied', ['the cathode, where oxygen is supplied', 'both electrodes', 'neither electrode'], 'An Ox, Red Cat.'),
    ('What is the role of the platinum on the electrodes of a PEM fuel cell?', 'catalyst', ['electrolyte', 'reactant', 'insulator'], 'Speeds up the electrode reactions.'),
    ('Which ions move through the electrolyte of an acidic hydrogen fuel cell?', 'H⁺ from anode to cathode', ['OH⁻ from cathode to anode', 'electrons from anode to cathode', 'O²⁻ from cathode to anode'], 'Proton exchange membrane.'),
])


R.f['ch10-st3'].extended = [
    ('A hydrogen fuel cell bus uses 8.0 kg of hydrogen per 100 km. (a) Calculate the energy released per 100 km (ΔHc(H₂) = −286 kJ mol⁻¹). (b) If the cell is 50 % efficient, calculate the electrical energy available. (c) Compare the CO₂ emissions with a diesel bus, considering how the hydrogen is produced.', '(a) n = 8000/2.02 = 3960 mol; E = 1.13 × 10⁶ kJ. (b) 5.66 × 10⁵ kJ. (c) no CO₂ at the exhaust; but hydrogen from steam reforming releases CO₂ (CH₄ + 2H₂O → CO₂ + 4H₂), so the life-cycle benefit depends on using green hydrogen from renewable electrolysis.', 6, 'multi_step'),
    ('Compare a hydrogen fuel cell with a lithium-ion battery as a power source for cars, referring to energy density, refuelling/recharging, efficiency and environmental impact.', 'Fuel cell: high specific energy of H₂, fast refuelling, long range, but storage at 70 MPa, Pt catalyst, limited infrastructure, overall well-to-wheel efficiency lower. Battery: high efficiency (~90 %), established charging network, but heavy, slower recharge, mining of Li/Co. Judgement: batteries suit cars; fuel cells suit heavy/long-range transport.', 6, 'multi_step')]
R.f['ch10-st3'].evaluate.append(('Methanol fuel cells are more practical than hydrogen fuel cells for portable devices.', ['methanol is a liquid – easy to store and transport, high energy density', 'no high-pressure tanks'], ['produce CO₂', 'methanol is toxic', 'methanol crossover through the membrane lowers efficiency', 'slower anode kinetics'], 'For small portable devices the storage advantage of methanol often outweighs its drawbacks, but hydrogen gives cleaner, more efficient operation where storage is feasible.'))


@R.add('ch10-st3', 'C4', (3, 5), 'multi_step')
def c4_fc_full(rng, slot):
    m = rng.choice([1.0, 2.0, 5.0, 6.0])
    eff = rng.choice([40, 50, 60])
    t = rng.choice([1, 2, 5, 10])  # hours
    n = m * 1000 / mr('H2')
    E = n * 286 * eff / 100
    P = E * 1000 / (t * 3600)
    stem = (f'A hydrogen fuel cell is supplied with {m:g} kg of hydrogen and operates at {eff} % efficiency for {t} hour(s). (a) Write the overall equation. (b) Calculate the electrical energy produced. '
            f'(c) Calculate the average power output in kW. (d) State and explain one advantage and one disadvantage of using hydrogen as a fuel.')
    return num(stem, f'(b) {q(E, "kJ")}; (c) {q(P / 1000, "kW")}', f'(a) 2H₂ + O₂ → 2H₂O (A1). (b) n = {sf(n)} mol; × 286 × {eff / 100} = {q(E, "kJ")} (M1 A1). (c) P = E/t = {q(P / 1000, "kW")} (A1). (d) e.g. only water produced / high specific energy; storage and production from fossil fuels (R1).', 6, 'multi_step')


# =============================================================================================
# ch11 R1.4 Entropy and spontaneity (HL)
# =============================================================================================
ENT_RX = [({'CaCO3(s)': 1}, {'CaO(s)': 1, 'CO2(g)': 1}, 'the thermal decomposition of calcium carbonate'),
          ({'N2(g)': 1, 'H2(g)': 3}, {'NH3(g)': 2}, 'the Haber process'),
          ({'SO2(g)': 2, 'O2(g)': 1}, {'SO3(g)': 2}, 'the Contact process'),
          ({'CH4(g)': 1, 'O2(g)': 2}, {'CO2(g)': 1, 'H2O(l)': 2}, 'the combustion of methane'),
          ({'NO2(g)': 2}, {'N2O4(g)': 1}, 'the dimerisation of nitrogen dioxide'),
          ({'H2O2(l)': 2}, {'H2O(l)': 2, 'O2(g)': 1}, 'the decomposition of hydrogen peroxide'),
          ({'C2H4(g)': 1, 'H2(g)': 1}, {'C2H6(g)': 1}, 'the hydrogenation of ethene'),
          ({'Mg(s)': 2, 'O2(g)': 1}, {'MgO(s)': 2}, 'the burning of magnesium'),
          ({'Fe2O3(s)': 1, 'CO(g)': 3}, {'Fe(s)': 2, 'CO2(g)': 3}, 'the reduction of iron(III) oxide by carbon monoxide'),
          ({'Al(s)': 2, 'Fe2O3(s)': 1}, {'Al2O3(s)': 1, 'Fe(s)': 2}, 'the thermite reaction'),
          ({'CuO(s)': 1, 'H2(g)': 1}, {'Cu(s)': 1, 'H2O(l)': 1}, 'the reduction of copper(II) oxide by hydrogen'),
          ({'H2O(l)': 1}, {'H2O(g)': 1}, 'the vaporisation of water'),
          ({'NO(g)': 2, 'O2(g)': 1}, {'NO2(g)': 2}, 'the oxidation of nitrogen monoxide'),
          ({'C(s)': 1, 'CO2(g)': 1}, {'CO(g)': 2}, 'the reaction of carbon with carbon dioxide'),
          ({'C(s)': 1, 'H2O(g)': 1}, {'CO(g)': 1, 'H2(g)': 1}, 'the formation of water gas'),
          ({'CO(g)': 2, 'O2(g)': 1}, {'CO2(g)': 2}, 'the combustion of carbon monoxide'),
          ({'ZnO(s)': 1, 'C(s)': 1}, {'Zn(s)': 1, 'CO(g)': 1}, 'the extraction of zinc by carbon'),
          ({'C2H5OH(l)': 1, 'O2(g)': 3}, {'CO2(g)': 2, 'H2O(l)': 3}, 'the combustion of ethanol')]


def dS_of(re_, pr):
    return sum(k * S0[s] for s, k in pr.items()) - sum(k * S0[s] for s, k in re_.items())


def dH_of(re_, pr):
    return sum(k * hf(s) for s, k in pr.items()) - sum(k * hf(s) for s, k in re_.items())


def gas_change(re_, pr):
    return sum(k for s, k in pr.items() if '(g)' in s) - sum(k for s, k in re_.items() if '(g)' in s)


R.facts('ch11-st1', F(
    terms=[('entropy (S)', 'a measure of the dispersal of energy and matter in a system: the number of possible arrangements of particles and their energy'),
           ('standard entropy (S⦵)', 'the entropy of one mole of a substance under standard conditions, in J K⁻¹ mol⁻¹; always positive above 0 K'),
           ('entropy change (ΔS)', 'the difference between the total entropy of the products and that of the reactants: ΔS = ΣS(products) − ΣS(reactants)')],
    facts=[('Which change has the largest increase in entropy?', 'H₂O(l) → H₂O(g)', ['H₂O(g) → H₂O(l)', 'H₂O(l) → H₂O(s)', 'H₂O(s) at 250 K → H₂O(s) at 260 K'], 'Liquid to gas: large increase in disorder.'),
           ('What are the units of standard entropy?', 'J K⁻¹ mol⁻¹', ['kJ mol⁻¹', 'J mol⁻¹', 'K J⁻¹ mol⁻¹'], 'Note: J, not kJ.'),
           ('Which state of matter has the highest entropy for a given substance?', 'gas', ['solid', 'liquid', 'all equal'], 'Most dispersed.'),
           ('Why is the standard entropy of an element not zero, unlike its enthalpy of formation?', 'Entropy is an absolute quantity that is zero only for a perfect crystal at 0 K.', ['Elements are unstable.', 'Entropy is always negative.', 'Elements are always gases.'], 'Third law.')],
    why=[('Explain why the entropy of a substance increases when it melts.', 'In the liquid the particles are more disordered and can move past each other, so there are many more possible arrangements of particles and energy than in the ordered solid.'),
         ('Explain why a reaction producing more moles of gas than it consumes usually has a positive ΔS.', 'Gases have much higher entropy than solids or liquids; increasing the number of gas particles increases the number of ways matter and energy can be dispersed.'),
         ('Explain why dissolving sodium chloride in water increases entropy.', 'The ions leave the ordered lattice and become dispersed through the solution, increasing the number of possible arrangements (outweighing the ordering of water molecules around the ions).')],
    contrast=[('entropy', 'enthalpy', 'Entropy (J K⁻¹ mol⁻¹) measures the dispersal of matter and energy; enthalpy (kJ mol⁻¹) measures heat content – a reaction’s spontaneity depends on both via ΔG.')],
    misc=[('Entropy always decreases when a gas is cooled because ΔH is negative.', 'Entropy decreases on cooling because particles have fewer accessible energy states; the sign of ΔS is not determined by ΔH.'),
          ('The standard entropy of O₂(g) is zero because it is an element.', 'Standard entropies are absolute and positive (O₂ 205 J K⁻¹ mol⁻¹); only ΔHf of elements is defined as zero.')],
    evaluate=[('Counting moles of gas is a reliable way to predict the sign of ΔS for a reaction.', ['gas entropy dominates, so the rule works for most reactions', 'quick qualitative prediction'], ['fails when the number of gas moles is unchanged', 'dissolving, mixing and changes in molecular complexity also matter', 'quantitative ΔS requires standard entropies'], 'A good first approximation, but calculations with S⦵ values are needed when gas moles are equal or effects compete.')],
))


@R.add('ch11-st1', 'C3', (1, 5), 'numerical')
def c3_dS(rng, slot):
    re_, pr, ctx = pick(rng, ENT_RX)
    dS = dS_of(re_, pr)
    eq = f'{side(re_)} → {side(pr)}'
    tab = ', '.join(f'{chem(s)} {S0[s]:g}' for s in dict.fromkeys(list(re_) + list(pr)))
    stem = pick(rng, [f'Calculate ΔS⦵ for {ctx}: {eq}. Standard entropies / J K⁻¹ mol⁻¹: {tab}.', f'Using the standard entropy values (J K⁻¹ mol⁻¹) {tab}, determine the standard entropy change for {eq}.'])
    nocoef = sum(S0[s] for s in pr) - sum(S0[s] for s in re_)
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Calculate ΔS⦵', 'What is ΔS⦵').replace('determine the standard entropy change', 'what is the standard entropy change'), dS, [-dS, nocoef if abs(nocoef - dS) > 1 else dS + 50, dS / 1000], 'J K⁻¹ mol⁻¹', f'ΔS = ΣS(products) − ΣS(reactants) = {sgn(dS)} J K⁻¹ mol⁻¹.', extra=False, signed=True)
    return num(stem, sgn(dS, 3, 'J K⁻¹ mol⁻¹'), f'ΣS(products) = {sum(k * S0[s] for s, k in pr.items()):g}, ΣS(reactants) = {sum(k * S0[s] for s, k in re_.items()):g} (M1, coefficients used); ΔS = {sgn(dS, 3, "J K⁻¹ mol⁻¹")} (A1).', 2)


@R.add('ch11-st1', 'C3', (1, 4), 'mcq')
def c3_dS_sign(rng, slot):
    re_, pr, ctx = pick(rng, [r for r in ENT_RX if gas_change(r[0], r[1]) != 0])
    g = gas_change(re_, pr)
    eq = f'{side(re_)} → {side(pr)}'
    right = 'positive: the number of moles of gas increases' if g > 0 else 'negative: the number of moles of gas decreases'
    wr = ['positive: the number of moles of gas decreases', 'negative: the number of moles of gas increases', 'zero: the reaction is balanced', 'positive: the reaction is exothermic']
    return mcq(rng, f'Predict the sign of ΔS for {eq}.', right, [w for w in wr if w != right][:3], f'Gas moles change by {g:+d}.')


@R.add('ch11-st1', 'C2', (2, 4), 'explain')
def c2_dS_explain(rng, slot):
    re_, pr, ctx = pick(rng, ENT_RX)
    g = gas_change(re_, pr)
    dS = dS_of(re_, pr)
    eq = f'{side(re_)} → {side(pr)}'
    stem = f'Predict and explain the sign of the entropy change for {ctx}, {eq}.'
    reason = f'gas moles change from {sum(k for s, k in re_.items() if "(g)" in s)} to {sum(k for s, k in pr.items() if "(g)" in s)}' if g else 'the number of moles of gas does not change, so ΔS is small and its sign depends on the S⦵ values'
    return dict(stem=stem, answer=f'{"positive" if dS > 0 else "negative"} ({sgn(dS)} J K⁻¹ mol⁻¹): {reason}.', markingKey=f'sign {"+" if dS > 0 else "−"} (1); {reason} – gases have much higher entropy than solids/liquids (1).', type='explain', marks=2)


R.mcqs('ch11-st1', 'C2', (1, 4), [
    ('Which process has a negative entropy change?', 'condensation of steam', ['dissolving sugar in water', 'sublimation of iodine', 'decomposition of CaCO₃'], 'Gas → liquid.'),
    ('Which substance has the highest standard entropy?', 'C₃H₈(g)', ['C(s, graphite)', 'H₂O(l)', 'NaCl(s)'], 'Complex gaseous molecule.'),
    ('For 2H₂(g) + O₂(g) → 2H₂O(l), ΔS is', 'large and negative', ['large and positive', 'approximately zero', 'impossible to predict'], '3 mol gas → liquid.'),
])


R.facts('ch11-st2', F(
    terms=[('Gibbs energy change (ΔG)', 'the energy change that combines enthalpy and entropy, ΔG = ΔH − TΔS; a reaction is spontaneous (thermodynamically favourable) when ΔG is negative'),
           ('spontaneous reaction', 'a reaction that, once started, proceeds without continuous external input of energy; ΔG < 0 (it may still be very slow)'),
           ('standard Gibbs energy of formation', 'the Gibbs energy change when one mole of a compound is formed from its elements in their standard states under standard conditions')],
    facts=[('When is a reaction spontaneous at all temperatures?', 'when ΔH is negative and ΔS is positive', ['when ΔH is positive and ΔS is negative', 'when both are negative', 'when both are positive'], 'ΔG always negative.'),
           ('Why must ΔS be divided by 1000 when using ΔG = ΔH − TΔS with ΔH in kJ mol⁻¹?', 'ΔS is usually given in J K⁻¹ mol⁻¹.', ['T is in °C.', 'ΔG is in J.', 'Entropy is always very large.'], 'Units must match.'),
           ('A reaction has ΔG⦵ = −30 kJ mol⁻¹ but does not occur at room temperature. Why?', 'The activation energy is too high, so the rate is negligible.', ['ΔG must be positive.', 'The reaction is endothermic.', 'Entropy decreases.'], 'Kinetics vs thermodynamics.'),
           ('A reaction with ΔH > 0 and ΔS < 0 is', 'never spontaneous', ['always spontaneous', 'spontaneous at high temperature', 'spontaneous at low temperature'], 'ΔG always positive.')],
    why=[('Explain why an endothermic reaction can be spontaneous.', 'If ΔS is positive and the temperature is high enough, the TΔS term exceeds ΔH, so ΔG = ΔH − TΔS becomes negative.'),
         ('Explain why a negative ΔG does not mean that a reaction will be observed to occur quickly.', 'ΔG indicates thermodynamic feasibility only; the rate depends on the activation energy, so a spontaneous reaction may be extremely slow (e.g. diamond → graphite).'),
         ('Explain why ΔG combines both the system and the surroundings.', 'ΔH/T represents the entropy change of the surroundings due to heat transfer; −ΔG/T = ΔS(system) + ΔS(surroundings) = ΔS(total), which must be positive for a spontaneous change.')],
    contrast=[('a spontaneous reaction', 'a fast reaction', 'Spontaneity (ΔG < 0) concerns whether a reaction is thermodynamically favourable; speed concerns kinetics (activation energy); they are independent.')],
    misc=[('All exothermic reactions are spontaneous.', 'An exothermic reaction with a large negative ΔS may have positive ΔG at high temperature (e.g. N₂ + 3H₂ → 2NH₃ above about 460 K).'),
          ('If ΔG is negative the reaction goes to completion.', 'Negative ΔG⦵ means K > 1 and products are favoured at equilibrium, but the reaction still reaches equilibrium rather than completion.')],
    evaluate=[('ΔG⦵ values are sufficient to decide whether an industrial process is viable.', ['identify feasible reactions and favourable temperatures', 'link to equilibrium constants'], ['rates may be far too slow without catalysts', 'real conditions are non-standard', 'costs, safety, yield and environmental factors are also decisive'], 'ΔG⦵ is a necessary first screen, but kinetics, equilibrium position under real conditions and economics decide viability.')],
))


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def c3_dG(rng, slot):
    re_, pr, ctx = pick(rng, ENT_RX)
    dH = dH_of(re_, pr)
    dS = dS_of(re_, pr)
    T = rng.choice([298, 298, 500, 800, 1000, 1200, 400])
    dG = dH - T * dS / 1000
    eq = f'{side(re_)} → {side(pr)}'
    stem = f'For {ctx}, {eq}, ΔH⦵ = {sgn(dH, 4)} kJ mol⁻¹ and ΔS⦵ = {sgn(dS, 4)} J K⁻¹ mol⁻¹. Calculate ΔG at {T} K and state whether the reaction is spontaneous at this temperature.'
    spont = 'spontaneous' if dG < 0 else 'not spontaneous'
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Calculate ΔG at', 'What is ΔG at').replace(' and state whether the reaction is spontaneous at this temperature.', '?'), dG, [dH - T * dS, dH + T * dS / 1000, dH - (T - 273) * dS / 1000], 'kJ mol⁻¹',
                    f'ΔG = ΔH − TΔS = {dH} − {T} × ({dS:g}/1000) = {sgn(dG)} kJ mol⁻¹. Forgetting to convert J to kJ is the common error.', extra=False, signed=True)
    return num(stem, f'{sgn(dG, 3, "kJ mol⁻¹")}; {spont}', f'ΔS converted to {dS / 1000:+.3f} kJ K⁻¹ mol⁻¹ (M1); ΔG = {dH} − {T}({dS / 1000:+.3f}) = {sgn(dG, 3, "kJ mol⁻¹")} (A1); {spont} because ΔG {"<" if dG < 0 else ">"} 0 (A1).', 3)


@R.add('ch11-st2', 'C4', (3, 5), 'multi_step')
def c4_full_gibbs(rng, slot):
    re_, pr, ctx = pick(rng, [r for r in ENT_RX if all(s in HF or s.split('(')[0] in ('O2', 'H2', 'N2', 'Fe', 'Al', 'Cu', 'Zn', 'Mg', 'C') for s in list(r[0]) + list(r[1]))])
    dH = dH_of(re_, pr)
    dS = dS_of(re_, pr)
    T = rng.choice([298, 1000])
    dG = dH - T * dS / 1000
    eq = f'{side(re_)} → {side(pr)}'
    used = list(dict.fromkeys(list(re_) + list(pr)))
    tab = '\n'.join(f'{chem(s)} | {hf(s)} | {S0[s]:g}' for s in used)
    stem = (f'Consider {ctx}: {eq}.\n\nspecies | ΔHf⦵ / kJ mol⁻¹ | S⦵ / J K⁻¹ mol⁻¹\n{tab}\n\n(a) Calculate ΔH⦵. (b) Calculate ΔS⦵. (c) Calculate ΔG at {T} K and deduce whether the reaction is spontaneous. '
            + ('(d) Calculate the temperature at which the reaction becomes (or stops being) spontaneous.' if dH * dS > 0 else '(d) Explain why the spontaneity of this reaction does not depend on temperature.'))
    ans = f'(a) {sgn(dH)} kJ mol⁻¹; (b) {sgn(dS)} J K⁻¹ mol⁻¹; (c) {sgn(dG)} kJ mol⁻¹, {"spontaneous" if dG < 0 else "not spontaneous"}'
    if dH * dS > 0:
        Tc = dH / (dS / 1000)
        ans += f'; (d) {sf(Tc)} K'
        dk = f'(d) T = ΔH/ΔS = {dH}/{dS / 1000:.3f} = {sf(Tc)} K (A1).'
    else:
        dk = f'(d) ΔH and ΔS have signs such that ΔG is {"always negative" if dH < 0 else "always positive"} (R1).'
    return num(stem, ans, f'(a) ΣΔHf(products) − ΣΔHf(reactants) = {sgn(dH)} (A1). (b) {sgn(dS)} J K⁻¹ mol⁻¹ (A1). (c) ΔG = ΔH − TΔS with ΔS in kJ (M1) = {sgn(dG)} kJ mol⁻¹ (A1). {dk}', 6, 'multi_step')


R.mcqs('ch11-st2', 'C2', (1, 4), [
    ('A reaction has ΔH = −100 kJ mol⁻¹ and ΔS = −200 J K⁻¹ mol⁻¹. At which temperatures is it spontaneous?', 'below 500 K', ['above 500 K', 'at all temperatures', 'at no temperature'], 'ΔG < 0 when T < ΔH/ΔS = 500 K.'),
    ('What is ΔG for a system at equilibrium?', '0', ['negative', 'positive', 'equal to ΔH'], 'No net driving force.'),
    ('Which combination gives a reaction that is spontaneous only at high temperatures?', 'ΔH > 0, ΔS > 0', ['ΔH < 0, ΔS > 0', 'ΔH < 0, ΔS < 0', 'ΔH > 0, ΔS < 0'], 'TΔS must exceed ΔH.'),
])


R.facts('ch11-st3', F(
    terms=[('crossover temperature', 'the temperature T = ΔH/ΔS at which ΔG = 0, above or below which the spontaneity of a reaction changes sign'),
           ('position of equilibrium and ΔG', 'a negative ΔG⦵ corresponds to K > 1 (products favoured); a positive ΔG⦵ corresponds to K < 1 (reactants favoured)'),
           ('ΔG⦵ = −RT ln K', 'the relationship between the standard Gibbs energy change and the equilibrium constant at temperature T')],
    facts=[('At equilibrium, which statement about ΔG is correct?', 'ΔG = 0', ['ΔG⦵ = 0', 'ΔG is at a maximum', 'ΔG = ΔH'], 'No further net change.'),
           ('If ΔG⦵ is large and negative, what can be deduced about K?', 'K ≫ 1', ['K ≪ 1', 'K = 1', 'K = 0'], 'ΔG⦵ = −RT ln K.'),
           ('For a reaction with ΔH > 0 and ΔS > 0, how does raising the temperature affect ΔG?', 'ΔG becomes more negative.', ['ΔG becomes more positive.', 'ΔG is unchanged.', 'ΔG becomes zero.'], '−TΔS term grows.'),
           ('What is ΔG⦵ when K = 1?', '0', ['1', '−RT', 'RT'], 'ln 1 = 0.')],
    why=[('Explain why the decomposition of calcium carbonate is not spontaneous at room temperature but is spontaneous in a lime kiln.', 'ΔH (+178 kJ mol⁻¹) and ΔS (+161 J K⁻¹ mol⁻¹) are both positive; at 298 K the TΔS term (48 kJ) is smaller than ΔH so ΔG > 0; above about 1100 K, TΔS exceeds ΔH and ΔG < 0.'),
         ('Explain why the Haber process becomes less thermodynamically favourable at high temperature.', 'ΔH is negative and ΔS is negative; as T rises, −TΔS becomes a larger positive term, so ΔG becomes less negative and eventually positive (above about 460 K); K decreases.'),
         ('Explain the relationship between the sign of ΔG⦵ and the position of equilibrium.', 'Since ΔG⦵ = −RT ln K, a negative ΔG⦵ gives ln K > 0 so K > 1 and products predominate; positive ΔG⦵ gives K < 1 and reactants predominate.')],
    contrast=[('ΔG', 'ΔG⦵', 'ΔG⦵ refers to standard conditions (all species at standard state) and determines K; ΔG refers to the actual mixture and becomes zero at equilibrium.')],
    misc=[('At equilibrium ΔG⦵ = 0.', 'At equilibrium ΔG = 0; ΔG⦵ is a fixed value for the reaction at that temperature and equals −RT ln K.')],
    evaluate=[('Increasing the temperature always makes reactions more spontaneous.', ['true for reactions with positive ΔS', 'higher temperatures also increase rate'], ['for reactions with negative ΔS, higher T makes ΔG less negative', 'exothermic equilibria shift left at higher T'], 'The effect depends on the sign of ΔS: higher temperatures favour entropy-increasing reactions only.')],
))


@R.add('ch11-st3', 'C3', (1, 5), 'numerical')
def c3_crossover(rng, slot):
    re_, pr, ctx = pick(rng, [r for r in ENT_RX if dH_of(r[0], r[1]) * dS_of(r[0], r[1]) > 0])
    dH = dH_of(re_, pr)
    dS = dS_of(re_, pr)
    Tc = dH / (dS / 1000)
    eq = f'{side(re_)} → {side(pr)}'
    above = dH > 0
    stem = f'For {eq}, ΔH⦵ = {sgn(dH, 4)} kJ mol⁻¹ and ΔS⦵ = {sgn(dS, 4)} J K⁻¹ mol⁻¹. Determine the temperature {"above" if above else "below"} which the reaction is spontaneous.'
    if slot.d <= 2:
        return nmcq(rng, stem.replace('Determine the temperature', 'What is the temperature').rstrip('.') + '?', Tc, [dH / dS, Tc - 273, dS / dH * 1000], 'K', f'ΔG = 0 when T = ΔH/ΔS = {dH}/({dS:g}/1000) = {sf(Tc)} K.', extra=False)
    return num(stem, q(Tc, 'K'), f'Set ΔG = 0: T = ΔH/ΔS (M1) = {dH}/{dS / 1000:+.3f} (unit conversion) = {q(Tc, "K")} (A1); spontaneous {"above" if above else "below"} this temperature (A1).', 3)


@R.add('ch11-st3', 'C3', (2, 5), 'numerical')
def c3_K_from_dG(rng, slot):
    re_, pr, ctx = pick(rng, ENT_RX)
    T = rng.choice([298, 500, 700])
    dG = dH_of(re_, pr) - T * dS_of(re_, pr) / 1000
    lnK = -dG * 1000 / (RGAS * T)
    if abs(lnK) > 200:
        return None
    K = math.exp(lnK)
    eq = f'{side(re_)} → {side(pr)}'
    stem = f'At {T} K, ΔG⦵ for {eq} is {sgn(dG, 3)} kJ mol⁻¹. Calculate the equilibrium constant K at this temperature and comment on the position of equilibrium. (R = 8.31 J K⁻¹ mol⁻¹)'
    return num(stem, f'K = {sf(K)}; {"products" if K > 1 else "reactants"} favoured', f'ln K = −ΔG⦵/RT = −({sf(dG)} × 1000)/(8.31 × {T}) = {lnK:.2f} (M1); K = e^{lnK:.2f} = {sf(K)} (A1); K {">" if K > 1 else "<"} 1 so {"products" if K > 1 else "reactants"} predominate (A1).', 3)


@R.add('ch11-st3', 'C2', (2, 4), 'explain')
def c2_temp_effect(rng, slot):
    re_, pr, ctx = pick(rng, ENT_RX)
    dH = dH_of(re_, pr)
    dS = dS_of(re_, pr)
    eq = f'{side(re_)} → {side(pr)}'
    if dH < 0 and dS > 0:
        a = 'spontaneous at all temperatures: ΔH negative and −TΔS negative, so ΔG is always negative'
    elif dH > 0 and dS < 0:
        a = 'never spontaneous: both terms positive, so ΔG is always positive'
    elif dH < 0:
        a = f'spontaneous only below {sf(dH / (dS / 1000))} K: at high T the positive −TΔS term outweighs the negative ΔH'
    else:
        a = f'spontaneous only above {sf(dH / (dS / 1000))} K: at high T the negative −TΔS term outweighs the positive ΔH'
    stem = f'For {ctx}, ΔH⦵ = {sgn(dH, 4)} kJ mol⁻¹ and ΔS⦵ = {sgn(dS, 4)} J K⁻¹ mol⁻¹. Explain how temperature affects the spontaneity of the reaction.'
    return dict(stem=stem, answer=a[0].upper() + a[1:] + '.', markingKey=f'Uses ΔG = ΔH − TΔS (1); {a} (2).', type='explain', marks=3)


R.mcqs('ch11-st3', 'C2', (1, 4), [
    ('For an exothermic reaction with a decrease in entropy, increasing the temperature', 'makes ΔG less negative and lowers K', ['makes ΔG more negative and raises K', 'has no effect on ΔG', 'makes ΔH positive'], '−TΔS is positive.'),
    ('If ΔG⦵ = +20 kJ mol⁻¹ at 298 K, which is correct?', 'K < 1 and reactants predominate at equilibrium', ['K > 1', 'the reaction cannot occur at all', 'the reaction is at equilibrium'], 'Positive ΔG⦵ → ln K < 0.'),
    ('At the crossover temperature of a reaction', 'ΔG⦵ = 0 and K = 1', ['ΔH = 0', 'ΔS = 0', 'the rate is maximum'], 'T = ΔH/ΔS.'),
])


@R.add('ch02-st5', 'C4', (3, 5), 'multi_step')
def c4_converge_compare(rng, slot):
    a, b = rng.sample([('lithium', 520), ('sodium', 496), ('potassium', 419), ('rubidium', 403), ('caesium', 376), ('hydrogen', 1312)], 2)
    la = H_PLANCK * C_LIGHT / (a[1] * 1000 / NA) * 1e9
    lb = H_PLANCK * C_LIGHT / (b[1] * 1000 / NA) * 1e9
    stem = (f'The first ionisation energies of {a[0]} and {b[0]} are {a[1]} and {b[1]} kJ mol⁻¹. (a) Calculate the wavelength of the convergence limit of the ground-state series for each element. '
            f'(b) State the region of the electromagnetic spectrum for each. (c) Explain, in terms of atomic structure, why the two values differ.')
    reg = lambda l: 'ultraviolet' if l < 400 else 'visible' if l < 700 else 'infrared'
    return num(stem, f'(a) {a[0]} {sf(la)} nm, {b[0]} {sf(lb)} nm; (b) {reg(la)}, {reg(lb)}', f'(a) λ = hcNA/IE: {sf(la)} nm and {sf(lb)} nm (M1 A1 A1). (b) {reg(la)} / {reg(lb)} (A1). (c) the element with the lower IE has its outer electron further from the nucleus and more shielded, so it needs less energy (longer wavelength) (R1).', 5, 'multi_step')


R.f['ch02-st5'].extended = [('Explain how the first ionisation energy of hydrogen can be determined from its emission spectrum. Include the series used, how the convergence limit is found and the calculation from the convergence frequency of 3.29 × 10¹⁵ Hz.', 'Use the Lyman (UV) series, which ends at n = 1 (ground state). Lines converge; plot Δf against f and extrapolate to Δf = 0 to find the limit (3.29 × 10¹⁵ Hz). E = hf = 2.18 × 10⁻¹⁸ J per atom; × NA = 1.31 × 10⁶ J mol⁻¹ = 1312 kJ mol⁻¹.', 6, 'multi_step')]


@R.add('ch11-st1', 'C4', (3, 5), 'multi_step')
def c4_dS_predict(rng, slot):
    a, b = rng.sample(ENT_RX, 2)
    stem = (f'Consider (I) {side(a[0])} → {side(a[1])} and (II) {side(b[0])} → {side(b[1])}. (a) Predict the sign of ΔS for each, giving reasons. '
            f'(b) Calculate ΔS⦵ for each using the data booklet standard entropies. (c) Explain which reaction shows the greater increase in disorder, and whether your predictions in (a) were correct.')
    sa, sb = dS_of(*a[:2]), dS_of(*b[:2])
    return num(stem, f'(b) I {sgn(sa)} J K⁻¹ mol⁻¹, II {sgn(sb)} J K⁻¹ mol⁻¹', f'(a) signs predicted from change in moles of gas/states (R1 R1). (b) I = {sgn(sa)}, II = {sgn(sb)} J K⁻¹ mol⁻¹ (A1 A1). (c) {"I" if sa > sb else "II"} has the more positive ΔS; comparison with predictions (R1).', 5, 'multi_step')


R.f['ch11-st1'].extended = [('Ammonium nitrate dissolves in water spontaneously although the process is endothermic (ΔH = +25.7 kJ mol⁻¹). (a) Explain, in terms of entropy, why the process is spontaneous. (b) Estimate the minimum ΔS needed at 298 K. (c) Suggest why the temperature of the solution falls.', '(a) ions leave the ordered lattice and disperse – large increase in entropy of the system outweighs the decrease in entropy of the surroundings (heat absorbed). (b) ΔS > ΔH/T = 25700/298 = 86 J K⁻¹ mol⁻¹. (c) energy absorbed from the water to break the lattice is greater than released by hydration.', 6, 'multi_step'),
                            ('Arrange in order of increasing standard entropy, giving reasons: H₂O(s), H₂O(l), H₂O(g), C(diamond), CH₄(g), C₃H₈(g).', 'C(diamond) (2.4) < H₂O(s) < H₂O(l) (70) < CH₄(g) (186) < H₂O(g) (189) < C₃H₈(g) (270): solids < liquids < gases; among gases, more atoms/complexity gives more ways to distribute energy.', 5, 'multi_step')]


@R.add('ch11-st3', 'C4', (3, 5), 'multi_step')
def c4_kiln(rng, slot):
    re_, pr, ctx = pick(rng, [r for r in ENT_RX if dH_of(r[0], r[1]) * dS_of(r[0], r[1]) > 0])
    dH, dS = dH_of(re_, pr), dS_of(re_, pr)
    Tc = dH / (dS / 1000)
    T1 = 298
    T2 = rng.choice([int(Tc * 1.3) // 50 * 50, int(Tc * 0.7) // 50 * 50]) if Tc > 200 else 1000
    g1, g2 = dH - T1 * dS / 1000, dH - T2 * dS / 1000
    stem = (f'For {ctx}, {side(re_)} → {side(pr)}, ΔH⦵ = {sgn(dH)} kJ mol⁻¹ and ΔS⦵ = {sgn(dS)} J K⁻¹ mol⁻¹. (a) Calculate ΔG⦵ at {T1} K and at {T2} K. '
            f'(b) Determine the temperature at which ΔG⦵ = 0. (c) Explain how the equilibrium constant changes as the temperature passes this value. (d) Comment on the assumption that ΔH and ΔS do not change with temperature.')
    return num(stem, f'(a) {sgn(g1)} and {sgn(g2)} kJ mol⁻¹; (b) {sf(Tc)} K', f'(a) {sgn(g1)} kJ mol⁻¹ at 298 K and {sgn(g2)} kJ mol⁻¹ at {T2} K (A1 A1). (b) T = ΔH/ΔS = {sf(Tc)} K (A1). (c) K passes from {"<1 to >1" if dH > 0 else ">1 to <1"} since ΔG⦵ = −RT ln K (R1). (d) both vary slightly with T, so the calculated temperature is an estimate (R1).', 6, 'multi_step')


R.f['ch11-st3'].extended = [('The industrial reduction of zinc oxide by carbon, ZnO(s) + C(s) → Zn(s) + CO(g), has ΔH⦵ = +239 kJ mol⁻¹ and ΔS⦵ = +190 J K⁻¹ mol⁻¹. (a) Show that the reaction is not spontaneous at 298 K. (b) Calculate the minimum temperature for the reaction to be spontaneous. (c) Explain why a much higher temperature than this is used in practice.', '(a) ΔG = 239 − 298(0.190) = +182 kJ mol⁻¹ > 0. (b) T = 239/0.190 = 1260 K. (c) faster rate; zinc is removed as vapour (above b.p. 1180 K), shifting the equilibrium; ΔH and ΔS vary with temperature.', 6, 'multi_step')]


# =============================================================================================
# Extra Paper 1A application items (data in the stem, so each draw is a distinct question)
# =============================================================================================
def _lst(xs):
    xs = list(xs)
    return ', '.join(xs[:-1]) + ' and ' + xs[-1]


@R.add('ch02-st4', 'C3', (1, 4), 'mcq')
def c3x_ie_named(rng, slot):
    pool = sorted(rng.sample([e for e in IE1 if e not in ('H', 'He')], 4), key=lambda e: Z[e])
    kind = rng.choice(['highest', 'lowest'])
    best = (max if kind == 'highest' else min)(pool, key=lambda e: IE1[e])
    stem = f'Consider the elements {_lst(ENAME[e] for e in pool)}. Which of these has the {kind} first ionisation energy?'
    return mcq(rng, stem, ENAME[best], [ENAME[e] for e in pool if e != best],
               'First IEs / kJ mol⁻¹: ' + ', '.join(f'{e} {IE1[e]}' for e in pool) + '. IE rises across a period (greater nuclear charge, similar shielding) and falls down a group (outer electron further away, more shielded).')


@R.add('ch02-st4', 'C3', (2, 4), 'mcq')
def c3x_succ_identity(rng, slot):
    el = pick(rng, list(SUCC))
    data = SUCC[el]
    k = rng.randint(min(4, len(data)), len(data))
    shown = '; '.join(f'IE{i + 1} = {v}' for i, v in enumerate(data[:k]))
    others = [e for e in SUCC if GROUP[e] != GROUP[el]]
    wr = rng.sample(others, 3)
    if rng.random() < 0.5:
        stem = f'The first {k} successive ionisation energies of element X, in kJ mol⁻¹, are: {shown}. Which element could X be?'
        return mcq(rng, stem, ENAME[el], [ENAME[e] for e in wr],
                   f'The largest jump is after electron {GROUP[el] % 10}, so X has {GROUP[el] % 10} valence electron(s) and is in group {GROUP[el]}: {ENAME[el]}.')
    ion = f'X{sup(GROUP[el] % 10) if GROUP[el] % 10 > 1 else ""}⁺' if GROUP[el] % 10 <= 3 else None
    v = GROUP[el] % 10
    right = f'group {GROUP[el]}'
    wrs = [f'group {g}' for g in sorted({GROUP[e] for e in SUCC} - {GROUP[el]})]
    rng.shuffle(wrs)
    stem = f'Successive ionisation energies (kJ mol⁻¹) of an element X: {shown}. To which group does X belong?'
    return mcq(rng, stem, right, wrs[:3], f'The biggest increase is between IE{v} and IE{v + 1}: {v} outer electron(s), so {right}.' + (f' X forms {ion} ions.' if ion else ''))


@R.add('ch02-st4', 'C3', (2, 4), 'mcq')
def c3x_ie_per_atom(rng, slot):
    el = pick(rng, [e for e in IE1])
    v = IE1[el] * 1000 / NA
    stem = f'The first ionisation energy of {ENAME[el]} is {IE1[el]} kJ mol⁻¹. What is the minimum energy needed to remove one electron from a single gaseous atom of {ENAME[el]}?'
    return nmcq(rng, stem, v, [IE1[el] / NA, IE1[el] * 1000 * NA, v * 1000], 'J', f'{IE1[el]} × 10³ J mol⁻¹ ÷ 6.02 × 10²³ mol⁻¹ = {sf(v)} J (remember kJ → J).', extra=True)


@R.add('ch04-st1', 'C3', (1, 4), 'mcq')
def c3x_ideal_named(rng, slot):
    pool = rng.sample(REALG, 4)
    pool.sort(key=lambda g: g[1])
    kind = rng.choice(['most', 'least'])
    best = (min if kind == 'most' else max)(pool, key=lambda g: RANK[g[0]])
    stem = f'Samples of {_lst(g[0] for g in pool)} are all at 250 K and 5000 kPa. Which gas behaves {kind} like an ideal gas?'
    return mcq(rng, stem, best[0], [g[0] for g in pool if g != best],
               f'{best[0]}: {best[2]}. Deviation from ideal behaviour increases with the strength of intermolecular forces and the size of the particles.')


@R.add('ch04-st1', 'C3', (2, 4), 'mcq')
def c3x_z_factor(rng, slot):
    gas = pick(rng, [g[0] for g in REALG[2:]])
    T = rng.choice([200, 250, 273, 300, 350, 400, 500])
    p = rng.choice([500, 1000, 2000, 5000, 10000, 20000, 40000])
    z = round(rng.uniform(0.80, 0.97), 2) if rng.random() < 0.6 else round(rng.uniform(1.03, 1.30), 2)
    if z < 1:
        right = 'Attractive forces between the particles are significant.'
    else:
        right = 'The volume of the particles themselves is significant.'
    wr = ['The gas behaves ideally under these conditions.', 'The attractive forces between the particles are significant.' if z > 1 else 'The volume of the particles themselves is significant.',
          'The particles have a lower kinetic energy than predicted.' if z > 1 else 'The particles collide elastically with the container walls.', 'The amount of gas has decreased.']
    wr = [w for w in wr if w.lower().strip('.') != right.lower().strip('.')]
    stem = f'For a sample of {gas} at {T} K and {p} kPa, the measured value of pV/(nRT) is {z:.2f}. Which statement best explains this value?'
    return mcq(rng, stem, right, wr[:3], f'pV/nRT = 1 for an ideal gas. {"Less than 1: attractions reduce the pressure (and volume)." if z < 1 else "Greater than 1: the finite particle volume reduces free space, so the real volume exceeds the ideal volume."}')


@R.add('ch04-st1', 'C3', (1, 3), 'mcq')
def c3x_ideal_conditions(rng, slot):
    gas = pick(rng, [g[0] for g in REALG])
    kind = rng.choice(['most', 'least'])
    right = 'high temperature and low pressure' if kind == 'most' else 'low temperature and high pressure'
    wr = ['low temperature and low pressure', 'high temperature and high pressure', 'low temperature and high pressure' if kind == 'most' else 'high temperature and low pressure']
    stem = f'Under which conditions does {gas} behave {kind} like an ideal gas?'
    return mcq(rng, stem, right, wr, 'High T: kinetic energy overcomes attractions; low p: particles far apart so their volume is negligible.' if kind == 'most' else 'Low T: attractions significant; high p: particle volume significant compared with the container.')


VAL = {'H': 1, 'Be': 2, 'B': 3, 'C': 4, 'N': 5, 'O': 6, 'F': 7, 'Si': 4, 'P': 5, 'S': 6, 'Cl': 7, 'Br': 7, 'I': 7, 'Xe': 8}


def _charge(f):
    if '^' not in f:
        return 0
    c = f.split('^')[1]
    n = int(c[:-1]) if c[:-1] else 1
    return n if c.endswith('+') else -n


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def c3x_valence_e(rng, slot):
    pool = [m[0] for m in MOLS] + [s[0] for s in SIMPLE]
    f = pick(rng, sorted(set(pool)))
    at = atoms(f)
    if any(e not in VAL for e in at):
        return None
    neutral = sum(VAL[e] * n for e, n in at.items())
    ch = _charge(f)
    v = neutral - ch
    sp = 'ion' if ch else 'molecule'
    stem = f'How many valence electrons in total must be shown in the Lewis formula of the {chem(f)} {sp}?'
    wr = [neutral + ch, neutral, v + 2, v - 2, v + 1, 2 * v] if ch else [v + 2, v - 2, v + 1, v - 1]
    wr = [str(w) for w in dict.fromkeys(wr) if w != v and w > 0]
    return mcq(rng, stem, str(v), wr[:3], ' + '.join(f'{n} × {VAL[e]} ({e})' for e, n in at.items()) + (f' {"−" if ch > 0 else "+"} {abs(ch)} (charge)' if ch else '') + f' = {v} electrons ({v // 2} pairs).')


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def c3x_octet(rng, slot):
    inc = ['BF3', 'BeCl2', 'BCl3', 'AlCl3']
    exp_ = ['PCl5', 'SF6', 'SF4', 'ClF3', 'XeF4', 'XeF2', 'BrF5', 'IF7']
    ok = ['CH4', 'NH3', 'H2O', 'CO2', 'CCl4', 'PCl3', 'NCl3', 'OF2', 'HCN', 'SiH4', 'CF4', 'N2', 'C2H4']
    kind = rng.choice(['fewer', 'more'])
    right = pick(rng, inc if kind == 'fewer' else exp_)
    wr = rng.sample(ok, 3)
    others = sorted([right] + wr)
    stem = f'Which of {_lst(chem(x) for x in others)} has {"fewer" if kind == "fewer" else "more"} than eight electrons in the valence shell of its central atom?'
    return mcq(rng, stem, chem(right), [chem(w) for w in wr], f'{chem(right)} {"has an incomplete octet (B/Be/Al with only 4–6 valence electrons)" if kind == "fewer" else "has an expanded octet (period 3+ central atom with more than four electron domains)"}; the others obey the octet rule.')


@R.add('ch07-st1', 'C3', (1, 4), 'mcq')
def c3x_coord_named(rng, slot):
    yes = ['NH4^+', 'H3O^+', 'CO', 'Al2Cl6', 'NH3BF3']
    no = ['NH3', 'H2O', 'CH4', 'CO2', 'HCl', 'N2', 'C2H6', 'BF3', 'H2O2', 'CH3OH']
    right = pick(rng, yes)
    wr = rng.sample(no, 3)
    stem = f'Which of the following contains a coordination (dative covalent) bond: {_lst(chem(x) for x in sorted([right] + wr))}?'
    return mcq(rng, stem, chem(right), [chem(w) for w in wr], f'In {chem(right)} one atom supplies both electrons of a shared pair (e.g. N or O lone pair → H⁺, O → C in CO, N → B in H₃N–BF₃, Cl → Al in Al₂Cl₆).')


def _dEN(a, b):
    return round(abs(EN[a] - EN[b]), 1)


@R.add('ch07-st3', 'C3', (1, 4), 'mcq')
def c3x_most_polar_bond(rng, slot):
    for _ in range(20):
        pool = rng.sample(ENPAIRS, 4)
        ds = [_dEN(a, b) for a, b in pool]
        kind = rng.choice(['most', 'least'])
        t = max(ds) if kind == 'most' else min(ds)
        if ds.count(t) == 1:
            break
    else:
        return None
    best = pool[ds.index(t)]
    b = lambda p: f'{p[0]}–{p[1]}'
    stem = f'Using electronegativity values from the data booklet, which of the bonds {_lst(b(p) for p in sorted(pool))} is the {kind} polar?'
    return mcq(rng, stem, b(best), [b(p) for p in pool if p != best], 'ΔEN: ' + ', '.join(f'{b(p)} {d:.1f}' for p, d in zip(pool, ds)) + '. The larger the electronegativity difference, the more polar the bond.')


@R.add('ch07-st3', 'C3', (1, 4), 'mcq')
def c3x_polar_molecule(rng, slot):
    pol = [m for m in MOLS if m[7] is True]
    non = [m for m in MOLS if m[7] is False]
    kind = rng.choice(['polar', 'non-polar'])
    if kind == 'polar':
        right = pick(rng, pol)
        wr = rng.sample(non, 3)
    else:
        right = pick(rng, non)
        wr = rng.sample(pol, 3)
    pool = sorted([right] + wr, key=lambda m: m[0])
    stem = f'Which of the molecules {_lst(mf(m) for m in pool)} is {kind}?'
    return mcq(rng, stem, mf(right), [mf(m) for m in wr],
               f'{mf(right)} is {right[5]}; ' + ('the bond dipoles do not cancel, so it has a net dipole.' if kind == 'polar' else 'its bond dipoles cancel by symmetry (or the bonds are non-polar).'))


@R.add('ch07-st3', 'C3', (1, 3), 'mcq')
def c3x_den(rng, slot):
    a, b = pick(rng, ENPAIRS)
    d = _dEN(a, b)
    neg = a if EN[a] > EN[b] else b
    other = b if neg == a else a
    right = f'{d:.1f}, with the δ− end on {neg}'
    wr = [f'{d:.1f}, with the δ− end on {other}', f'{EN[a] + EN[b]:.1f}, with the δ− end on {neg}', f'{max(d + 0.4, 0.4):.1f}, with the δ− end on {neg}' if d < 1.5 else f'{d - 0.4:.1f}, with the δ− end on {neg}']
    stem = f'What is the electronegativity difference for the {a}–{b} bond, and which atom carries the partial negative charge?'
    if d == 0:
        return None
    return mcq(rng, stem, right, wr, f'EN({a}) = {EN[a]}, EN({b}) = {EN[b]}; ΔEN = {d:.1f}; the more electronegative atom ({neg}) is δ−.')


IMF_TYPE = {f: ('hydrogen bonding' if 'hydrogen' in t else 'dipole–dipole forces' if 'dipole' in t else 'London dispersion forces') for f, t in IMF}


@R.add('ch07-st4', 'C3', (1, 4), 'mcq')
def c3x_highest_bp(rng, slot):
    ser = pick(rng, BPS)
    pool = rng.sample(ser, min(4, len(ser)))
    if len(pool) < 3:
        return None
    kind = rng.choice(['highest', 'lowest'])
    best = (max if kind == 'highest' else min)(pool, key=lambda x: x[2])
    stem = f'Which of {_lst(x[1] for x in sorted(pool, key=lambda x: x[1]))} has the {kind} boiling point?'
    return mcq(rng, stem, best[1], [x[1] for x in pool if x != best],
               'Boiling points / °C: ' + ', '.join(f'{x[1]} {x[2]}' for x in pool) + '. Hydrogen bonding > dipole–dipole > London forces; London forces increase with the number of electrons and surface area.')


@R.add('ch07-st4', 'C3', (1, 4), 'mcq')
def c3x_strongest_imf(rng, slot):
    f = pick(rng, sorted(IMF_TYPE))
    right = IMF_TYPE[f]
    wr = [x for x in ['hydrogen bonding', 'dipole–dipole forces', 'London dispersion forces', 'covalent bonds', 'ionic bonds'] if x != right]
    rng.shuffle(wr)
    if 'covalent bonds' not in wr[:3]:
        wr = ['covalent bonds'] + wr
    stem = f'What is the strongest type of intermolecular force between molecules of {chem(f)} in the liquid state?'
    return mcq(rng, stem, right, wr[:3], f'{chem(f)}: {dict(IMF)[f]}. Covalent bonds are intramolecular, not intermolecular.')


HB_BOND = {'H2O': 'O–H', 'NH3': 'N–H', 'HF': 'F–H', 'CH3OH': 'O–H', 'C2H5OH': 'O–H', 'CH3NH2': 'N–H', 'CH3COOH': 'O–H'}


@R.add('ch07-st4', 'C3', (2, 4), 'mcq')
def c3x_hbond_pair(rng, slot):
    hb = ['H2O', 'NH3', 'HF', 'CH3OH', 'C2H5OH', 'CH3NH2', 'CH3COOH']
    nohb = ['CH4', 'HCl', 'CO2', 'CHCl3', 'CH3CHO', 'CH3COCH3', 'C6H14', 'PH3', 'CH3OCH3', 'H2S', 'HBr', 'CCl4']
    kind = rng.choice(['can', 'cannot'])
    if kind == 'can':
        right = pick(rng, hb)
        wr = rng.sample(nohb, 3)
    else:
        right = pick(rng, nohb)
        wr = rng.sample(hb, 3)
    stem = f'Which substance {"forms" if kind == "can" else "does not form"} hydrogen bonds between its own molecules: {_lst(chem(x) for x in sorted([right] + wr))}?'
    return mcq(rng, stem, chem(right), [chem(w) for w in wr], 'Hydrogen bonding between identical molecules needs H bonded directly to N, O or F and a lone pair on N, O or F. ' + (f'{chem(right)} has {HB_BOND[right]} bonds.' if kind == 'can' else f'{chem(right)} has no H attached to N, O or F.'))


@R.add('ch07-st5', 'C3', (1, 4), 'mcq')
def c3x_sp_named(rng, slot):
    f, nm, s, p = pick(rng, SP)
    right = f'{s} σ and {p} π'
    wr = [f'{s + p} σ and {p} π', f'{s - p} σ and {p} π' if s > p else f'{s} σ and {p + 1} π', f'{s} σ and {2 * p if p else 1} π', f'{s + 1} σ and {p} π']
    wr = [w for w in dict.fromkeys(wr) if w != right]
    stem = f'How many sigma (σ) and pi (π) bonds are present in one molecule of {nm}?'
    return mcq(rng, stem, right, wr[:3], f'{chem(f)}: each single bond is σ; a double bond is σ + π; a triple bond is σ + 2π. Total {s} σ, {p} π.')


@R.add('ch07-st5', 'C3', (1, 4), 'mcq')
def c3x_angle_hyb(rng, slot):
    m = pick(rng, [x for x in MOLS if x[10]])
    right = f'{m[10]} and {m[5]}'
    shapes = sorted({x[5] for x in MOLS if not x[13]} - {m[5]})
    hybs = [h for h in ['sp', 'sp²', 'sp³'] if h != m[10]]
    wr = [f'{hybs[0]} and {m[5]}', f'{m[10]} and {rng.choice(shapes)}', f'{hybs[1]} and {rng.choice(shapes)}']
    wr = [w for w in dict.fromkeys(wr) if w != right]
    stem = f'Which describes the hybridisation of the central atom and the molecular geometry of {mf(m)}?'
    return mcq(rng, stem, right, wr, f'{m[3]} electron domains ({m[4]} lone pair{"s" if m[4] != 1 else ""}) → {m[10]}; geometry {m[5]}.')


@R.add('ch08-st1', 'C3', (1, 4), 'mcq')
def c3x_mp_named(rng, slot):
    pool = sorted(rng.sample(MPS, 4), key=lambda m: m[0])
    kind = rng.choice(['highest', 'lowest'])
    best = (max if kind == 'highest' else min)(pool, key=lambda m: m[1])
    stem = f'Which of the metals {_lst(ENAME[m[0]] for m in pool)} has the {kind} melting point?'
    return mcq(rng, stem, ENAME[best[0]], [ENAME[m[0]] for m in pool if m != best],
               'Melting points / °C: ' + ', '.join(f'{m[0]} {m[1]}' for m in pool) + '. Metallic bonding is stronger for smaller, more highly charged cations with more delocalised electrons.')


@R.add('ch08-st1', 'C3', (1, 4), 'mcq')
def c3x_tm_ox_mcq(rng, slot):
    f, m, ox = pick(rng, TM_COMP)
    wr = [f'+{x}' for x in sorted({ox - 1, ox + 1, ox - 2, ox + 2, 2 * ox} - {ox}) if 0 < x <= 8]
    rng.shuffle(wr)
    stem = f'In the compound {chem(f)}, the oxidation state of the transition element is'
    return mcq(rng, stem, f'+{ox}', wr[:3], f'Oxidation states sum to zero (K +1, O −2, Cl −1, SO₄ −2), so {m} = +{ox}.')


TM_IONS2 = [('Sc', 3), ('Ti', 2), ('Ti', 3), ('V', 2), ('V', 3), ('Cr', 3), ('Mn', 2), ('Mn', 3), ('Fe', 2), ('Fe', 3), ('Co', 2), ('Co', 3), ('Ni', 2), ('Cu', 1), ('Cu', 2), ('Zn', 2)]


@R.add('ch08-st1', 'C3', (2, 4), 'mcq')
def c3x_tm_ion_cfg(rng, slot):
    el, ch = pick(rng, TM_IONS2)
    right = cfg_short(config_ion(Z[el], ch))
    # common error: remove 3d before 4s
    occ = dict(config(Z[el]))
    w1 = dict(occ)
    rem = ch
    for sl in ('3d', '4s'):
        while rem and w1.get(sl, 0):
            w1[sl] -= 1
            rem -= 1
    w1 = cfg_short(sorted([(k, v) for k, v in w1.items() if v], key=lambda t: (int(t[0][0]), 'spdf'.index(t[0][1]))))
    w2 = cfg_short(config(Z[el]))
    w3 = cfg_short(config_ion(Z[el], ch + 1)) if ch < 3 else cfg_short(config_ion(Z[el], ch - 1))
    wr = [w for w in dict.fromkeys([w1, w2, w3]) if w != right]
    if len(wr) < 3:
        wr.append(cfg_short(config_ion(Z[el], max(1, ch - 1))) if ch > 1 else cfg_short(config_ion(Z[el], 3)))
        wr = [w for w in dict.fromkeys(wr) if w != right]
    stem = f'What is the ground-state electron configuration of the {ENAME[el]} ion {el}{sup(ch) if ch > 1 else ""}⁺?'
    return mcq(rng, stem, right, wr[:3], f'{el}: {cfg_short(config(Z[el]))}. The 4s electrons are lost before the 3d electrons, giving {right}.')


@R.add('ch08-st4', 'C3', (1, 4), 'mcq')
def c3x_material_choice(rng, slot):
    use, mat, why = pick(rng, MAT)
    wr = [x[1] for x in rng.sample([x for x in MAT if x[1] != mat], 3)]
    stem = f'Which material is the most suitable choice for {use}?'
    return mcq(rng, stem, mat, wr, f'{mat}: {why}.')


@R.add('ch08-st4', 'C3', (1, 4), 'mcq')
def c3x_property_bonding(rng, slot):
    kinds = {
        'metallic': (rng.randint(60, 1700), 'conducts electricity as a solid and when molten', 'is malleable', 'is insoluble in water'),
        'ionic': (rng.randint(600, 2900), 'does not conduct as a solid but conducts when molten or dissolved', 'is brittle', 'is soluble in water' if rng.random() < 0.6 else 'is insoluble in water'),
        'covalent network': (rng.randint(1400, 3600), 'does not conduct electricity in any state', 'is very hard', 'is insoluble in water and in organic solvents'),
        'simple molecular (covalent)': (rng.randint(-200, 150), 'does not conduct electricity in any state', 'is soft as a solid', 'dissolves in hexane'),
    }
    k = pick(rng, list(kinds))
    mp, cond, mech, sol = kinds[k]
    if k == 'metallic' and mp < 100:
        mp = rng.randint(180, 1700)
    props = [f'melts at {mp} °C', cond, mech, sol]
    show = props[:1] + rng.sample(props[1:], 2)
    stem = f'A solid material X {_lst(show)}. Which type of bonding and structure is X most likely to have?'
    return mcq(rng, stem, k, [x for x in kinds if x != k], f'{", ".join(show)} → {k}: ' + {'metallic': 'cations in a sea of delocalised electrons', 'ionic': 'lattice of oppositely charged ions, mobile only when molten/aqueous', 'covalent network': 'giant lattice of strong covalent bonds', 'simple molecular (covalent)': 'molecules held by weak intermolecular forces'}[k] + '.')


R.mcqs('ch05-st2', 'C1', (1, 4), [
    ('What is meant by the limiting reactant in a chemical reaction?', 'the reactant that is completely consumed and so determines the maximum amount of product', ['the reactant present in the smallest mass', 'the reactant with the smallest coefficient in the equation', 'the reactant that is left over at the end'], 'Limiting = used up first, after allowing for the mole ratio.'),
    ('How is the percentage yield of a reaction calculated?', '(experimental yield ÷ theoretical yield) × 100', ['(theoretical yield ÷ experimental yield) × 100', '(mass of product ÷ mass of all reactants) × 100', '(Mr of desired product ÷ sum of Mr of all products) × 100'], 'Percentage yield compares the actual with the theoretical amount.'),
    ('How is the atom economy of a reaction calculated?', '(molar mass of desired product ÷ total molar mass of all reactants) × 100', ['(actual yield ÷ theoretical yield) × 100', '(moles of product ÷ moles of reactants) × 100', '(mass of waste ÷ mass of product) × 100'], 'Atom economy uses the balanced equation, not experimental masses.'),
    ('What is the theoretical yield of a reaction?', 'the maximum amount of product calculated from the limiting reactant, assuming complete reaction', ['the amount of product actually isolated', 'the amount of product formed at equilibrium', 'the mass of the excess reactant'], 'Calculated from stoichiometry.'),
    ('Why is a reactant often used in excess in a synthesis?', 'to ensure that the more expensive or important reactant is completely converted', ['to increase the atom economy', 'to lower the activation energy', 'to make the theoretical yield larger than 100%'], 'Using one reagent in excess drives the conversion of the other.'),
    ('Which statement about a reaction with an atom economy of 100% is correct?', 'all the atoms of the reactants end up in the desired product', ['the percentage yield must be 100%', 'the reaction must be exothermic', 'no limiting reactant is present'], 'For example, addition reactions.'),
])
