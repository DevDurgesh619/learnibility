"""CBSE Class 11 Biology, chapters 11-15: Photosynthesis in Higher Plants, Respiration in Plants, Plant Growth and
Development, Breathing and Exchange of Gases, Body Fluids and Circulation.

Fact tables for g11_chemistry_kit.py; Calvin-cycle ATP/NADPH, glycolysis/ATP yields, RQ, growth rates,
respiratory volumes and cardiac output are computed here.
"""
from __future__ import annotations

from fractions import Fraction

from qbank import F, mcq, num
from g11_chemistry_kit import cap, sf

P = 'cbse-g11-biology'


def _w(good, cands, fmt=str):
    out = []
    for c in cands:
        s = fmt(c)
        if s != fmt(good) and s not in out:
            out.append(s)
    return out[:3]


# ---------------------------------------------------------------- ch11 photosynthesis

def calvin_cost(r):
    n = r.choice([1, 2, 3, 4, 5, 6, 8, 10, 12])
    path = r.choice(['C3', 'C4'])
    co2 = 6 * n
    atp = (18 if path == 'C3' else 30) * n
    nadph = 12 * n
    what = r.choice(['ATP', 'NADPH'])
    good = atp if what == 'ATP' else nadph
    cands = [18 * n, 30 * n, 12 * n, 24 * n, 3 * n, 6 * n, 36 * n]
    return mcq(f'How many molecules of {what} are needed to synthesise {n} molecule{"s" if n > 1 else ""} of glucose ({co2} CO₂ fixed) in a {path} plant?',
               str(good), _w(good, cands), f'Per CO₂: 3 ATP and 2 NADPH in the Calvin cycle (C4 plants use 2 extra ATP per CO₂). For {co2} CO₂: {what} = {good}.', r)


def calvin_turns(r):
    n = r.choice([1, 2, 3, 4, 5, 10])
    co2 = 6 * n
    return {'stem': f'Calculate the number of turns of the Calvin cycle and the number of ATP and NADPH molecules needed to make {n} molecule{"s" if n > 1 else ""} of glucose in a C3 plant.',
            'answer': f'{co2} turns; {18 * n} ATP and {12 * n} NADPH',
            'key': f'One turn fixes one CO₂ and uses 3 ATP + 2 NADPH (1); one glucose needs 6 turns, so {n} glucose need {co2} turns, {18 * n} ATP and {12 * n} NADPH (1).',
            'distractors': [f'{n} turns; {3 * n} ATP and {2 * n} NADPH', f'{co2} turns; {12 * n} ATP and {18 * n} NADPH', f'{co2} turns; {30 * n} ATP and {12 * n} NADPH'],
            'marks': 2}


CH11S1 = {
    'topic': 'early experiments, the site of photosynthesis and pigments',
    'terms': [('photosynthesis', 'a physico-chemical process by which green plants use light energy to synthesise organic compounds'),
              ('chlorophyll a', 'the chief pigment of photosynthesis, which appears bright or blue-green in chromatography'),
              ('accessory pigments', 'pigments such as chlorophyll b, xanthophylls and carotenoids that absorb light and transfer the energy to chlorophyll a'),
              ('absorption spectrum', 'a graph showing the ability of a pigment to absorb light of different wavelengths'),
              ('action spectrum', 'a graph showing the rate of photosynthesis at different wavelengths of light'),
              ('stroma lamellae', 'flat membranous tubules connecting the grana in a chloroplast'),
              ('grana', 'stacks of thylakoids in the chloroplast where light is trapped and ATP and NADPH are formed')],
    'tf': (['Joseph Priestley in 1770 showed that plants restore to the air whatever breathing animals and burning candles remove.', 'Jan Ingenhousz showed that sunlight is essential for plants to purify air fouled by burning candles or breathing animals.',
            'Julius von Sachs provided evidence that glucose is made in the green parts of plants and stored as starch.', 'T.W. Engelmann used a prism and the green alga Cladophora with aerobic bacteria to plot the first action spectrum.',
            'Cornelius van Niel showed that photosynthesis is a light-dependent reaction in which hydrogen from an oxidisable compound reduces CO₂.', 'The O₂ evolved by green plants comes from water, not from CO₂.',
            'Chlorophyll a is the chief pigment associated with photosynthesis.'],
           [('The O₂ released in photosynthesis comes from CO₂.', 'Van Niel and later isotope studies showed the O₂ comes from H₂O.'),
            ('Engelmann found that aerobic bacteria accumulated mainly in the green region of light.', 'The bacteria accumulated mainly in the blue and red regions of the spectrum.'),
            ('Chlorophyll a appears yellow in chromatography.', 'Chlorophyll a appears bright or blue-green; xanthophylls are yellow and carotenoids yellow to yellow-orange.'),
            ('The dark reactions of photosynthesis occur in the grana.', 'The light reactions occur in the grana; enzymatic (dark) reactions occur in the stroma.'),
            ('Photosynthesis occurs only in the leaves of plants.', 'It occurs in leaves and also in other green parts of the plant.')]),
    'orders': [('chronological order of discoveries in photosynthesis', ['Joseph Priestley (1770)', 'Jan Ingenhousz (1730–1799)', 'Julius von Sachs (1854)', 'T.W. Engelmann (1843–1909)'], 'From restoration of air, to need of light, to starch formation, to action spectrum.', '→')],
    'ar': [('Leaves appear green.', 'Chlorophylls absorb mainly blue and red light and reflect green light.', 'a', 'Green light is not absorbed.'),
           ('The rate of photosynthesis is maximum in blue and red light.', 'Chlorophyll a absorbs maximally in the blue and red regions.', 'a', 'Action spectrum matches absorption spectrum of chlorophyll a.'),
           ('Accessory pigments protect chlorophyll a from photo-oxidation.', 'Accessory pigments absorb wavelengths not absorbed by chlorophyll a.', 'b', 'Both are true; the second explains a wider range of light use, not protection.'),
           ('The O₂ evolved in photosynthesis comes from CO₂.', 'Van Niel showed that hydrogen from water reduces CO₂ in green plants.', 'd', 'O₂ comes from H₂O; R is true.')],
    'features': {'intro': 'In a paper chromatogram of leaf pigments, one band is described:', 'q': 'Identify the pigment', 'what': 'pigment', 'compare': False, 'long': False,
                 'items': [('chlorophyll a', ['bright or blue-green colour', 'chief pigment of photosynthesis', 'present in the reaction centre', 'absorbs maximally in blue and red']),
                           ('chlorophyll b', ['yellow-green colour', 'accessory pigment', 'transfers energy to chlorophyll a', 'part of light-harvesting complexes']),
                           ('xanthophylls', ['yellow colour', 'accessory pigment', 'absorbs a wider range of wavelengths', 'protects chlorophyll a from photo-oxidation']),
                           ('carotenoids', ['yellow to yellow-orange colour', 'accessory pigment', 'absorbs a wider range of wavelengths', 'protects chlorophyll a from photo-oxidation'])]},
    'qa': [('C4', 'D3', 'case', 'Imitating a classic experiment, Saanvi placed a filament of a green alga in a drop of water with aerobic bacteria and lit it with light split by a prism. The bacteria gathered at two regions.\n(i) Whose experiment is this? (1 mark)\n(ii) In which regions of light did the bacteria gather? (1 mark)\n(iii) Why did they gather there, and what did the experiment show? (2 marks)',
            '(i) T.W. Engelmann. (ii) Blue and red. (iii) Oxygen was evolved most where photosynthesis was fastest, attracting aerobic bacteria; it gave the first action spectrum, which resembles the absorption spectrum of chlorophyll a and b.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the early experiments that led to the present understanding of photosynthesis.',
            'Priestley (1770) – mouse and candle in bell jar, plants restore air; Ingenhousz – sunlight needed, oxygen bubbles from green parts in light; Sachs (1854) – glucose made in green parts and stored as starch; Engelmann – action spectrum with Cladophora and aerobic bacteria, blue and red light; van Niel – H₂O is the hydrogen donor and O₂ comes from water: 6CO₂ + 12H₂O → C₆H₁₂O₆ + 6H₂O + 6O₂.',
            '1 mark each scientist.')],
    'q3': [('Distinguish between an absorption spectrum and an action spectrum. What does their overlap indicate?',
            'Absorption spectrum – ability of a pigment to absorb different wavelengths; action spectrum – rate of photosynthesis at different wavelengths. They largely overlap for chlorophyll a, showing chlorophyll a is the chief pigment and most photosynthesis occurs in blue and red light.',
            '1 mark each.')],
}

CH11S2 = {
    'topic': 'the light reaction',
    'terms': [('light-harvesting complexes (LHC)', 'groups of pigment molecules bound to proteins in PS I and PS II that make up antennae'),
              ('reaction centre', 'a single chlorophyll a molecule in each photosystem that receives the excitation energy'),
              ('P700', 'the reaction centre chlorophyll a of PS I, with an absorption peak at 700 nm'),
              ('P680', 'the reaction centre chlorophyll a of PS II, with an absorption peak at 680 nm'),
              ('photolysis of water', 'the splitting of water into H⁺, [O] and electrons, associated with PS II'),
              ('Z scheme', 'the characteristic zig-zag shape of the electron flow from PS II to PS I in non-cyclic photophosphorylation'),
              ('photophosphorylation', 'the synthesis of ATP from ADP and inorganic phosphate in the presence of light'),
              ('chemiosmotic hypothesis', 'the explanation of ATP synthesis as linked to a proton gradient across a membrane')],
    'tf': (['Light reactions include light absorption, water splitting, oxygen release and formation of ATP and NADPH.', 'The splitting of water is associated with PS II.',
            'The water-splitting complex is on the inner side of the thylakoid membrane.', 'Cyclic photophosphorylation occurs in the stroma lamellae.',
            'In cyclic photophosphorylation only ATP is formed, not NADPH.', 'The ATP synthase enzyme has a transmembrane channel CF₀ and a CF₁ part protruding into the stroma.'],
           [('Cyclic photophosphorylation produces both ATP and NADPH.', 'Only ATP is synthesised; NADPH is formed in non-cyclic photophosphorylation.'),
            ('Photolysis of water is associated with PS I.', 'Photolysis of water is associated with PS II.'),
            ('Protons accumulate in the stroma during the light reaction.', 'Protons accumulate in the lumen of the thylakoid; the stroma becomes poorer in H⁺.'),
            ('The stroma lamellae have both PS I and PS II and NADP reductase.', 'Stroma lamellae lack PS II and NADP reductase; they carry out cyclic flow only.'),
            ('PS I and PS II are named in the order they act in electron flow.', 'They are named in the order of their discovery, not their function.')]),
    'orders': [('sequence of electron flow in the Z scheme', ['water', 'PS II (P680)', 'electron transport chain (cytochromes)', 'PS I (P700)', 'NADP⁺'], 'Electrons from water pass to PS II, then via ETS to PS I and finally reduce NADP⁺.', '→')],
    'ar': [('Protons accumulate inside the thylakoid lumen during the light reaction.', 'Water is split on the inner side of the membrane, and the electron carrier pumps protons from the stroma into the lumen.', 'a', 'Both add H⁺ to the lumen.'),
           ('ATP is synthesised when protons move from the lumen to the stroma.', 'The proton gradient across the thylakoid membrane drives ATP synthase.', 'a', 'Chemiosmosis.'),
           ('Cyclic photophosphorylation does not produce NADPH.', 'In the cyclic flow electrons from PS I return to PS I via the ETS.', 'a', 'Electrons do not reach NADP⁺.'),
           ('The splitting of water occurs in PS I.', 'O₂ is released as a by-product of photolysis of water.', 'd', 'Water splitting is associated with PS II; R is true.')],
    'features': {'intro': 'A process of the light reaction has these features:', 'q': 'Identify the process', 'what': 'process',
                 'items': [('non-cyclic photophosphorylation', ['both PS II and PS I involved', 'electrons from water reach NADP⁺', 'forms ATP and NADPH', 'O₂ is released']),
                           ('cyclic photophosphorylation', ['only PS I involved', 'electrons cycle back to PS I', 'only ATP formed', 'occurs in stroma lamellae']),
                           ('photolysis of water', ['associated with PS II', 'occurs on the inner side of the thylakoid membrane', 'releases H⁺, [O] and electrons', 'supplies electrons to replace those lost by PS II'])]},
    'qa': [('C4', 'D3', 'case', 'In an experiment, isolated chloroplasts were placed in light. When a chemical that made the thylakoid membrane leaky to protons was added, ATP formation stopped although electrons still flowed.\n(i) Name the hypothesis that explains this result. (1 mark)\n(ii) Where do protons accumulate during the light reaction? (1 mark)\n(iii) Explain how the proton gradient leads to ATP synthesis. (2 marks)',
            '(i) Chemiosmotic hypothesis. (ii) In the lumen of the thylakoid. (iii) Protons diffuse back to the stroma through the CF₀ channel of ATP synthase; this causes a conformational change in CF₁, which synthesises ATP from ADP and Pi.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Explain the Z scheme of the light reaction. How is ATP produced by chemiosmosis?',
            'PS II (P680) absorbs light, electrons excited and passed through the ETS (cytochromes) downhill to PS I (P700); PS I electrons excited to another acceptor and pass to NADP⁺ forming NADPH; water split at PS II replaces electrons and releases O₂. Proton gradient: photolysis inside lumen, carrier pumps H⁺ into lumen, NADP reductase removes H⁺ from stroma; H⁺ flows out through CF₀ of ATP synthase; CF₁ makes ATP.',
            '3 marks Z scheme; 2 marks chemiosmosis.')],
    'q3': [('Give three differences between cyclic and non-cyclic photophosphorylation.',
            'Cyclic – only PS I; electrons return to PS I; only ATP formed; no photolysis or O₂; in stroma lamellae. Non-cyclic – PS II and PS I; electrons from water go to NADP⁺; ATP and NADPH; O₂ released; in grana.',
            '1 mark each.'),
           ('What three events create the proton gradient across the thylakoid membrane?',
            'Splitting of water on the inner side releases H⁺ in the lumen; the electron carrier transfers H⁺ from stroma to lumen as electrons move through the photosystems; NADP reductase on the stroma side removes H⁺ from the stroma while reducing NADP⁺.',
            '1 mark each.')],
}

CH11S3 = {
    'topic': 'the Calvin cycle and the C4 pathway',
    'terms': [('Calvin cycle', 'the cyclic biosynthetic pathway of CO₂ fixation into carbohydrate, with carboxylation, reduction and regeneration'),
              ('RuBisCO', 'ribulose bisphosphate carboxylase-oxygenase, the most abundant enzyme in the world, which carboxylates RuBP'),
              ('3-phosphoglyceric acid (PGA)', 'the first stable product of CO₂ fixation in C3 plants, a 3-carbon acid'),
              ('oxaloacetic acid (OAA)', 'the first stable product of CO₂ fixation in C4 plants, a 4-carbon acid'),
              ('Kranz anatomy', 'the leaf anatomy of C4 plants with large bundle sheath cells arranged in a wreath around vascular bundles'),
              ('PEP carboxylase (PEPcase)', 'the primary CO₂-fixing enzyme in the mesophyll cells of C4 plants'),
              ('phosphoenol pyruvate (PEP)', 'the 3-carbon primary CO₂ acceptor in the mesophyll cells of C4 plants')],
    'groups': [('a C4 plant', ['maize', 'sorghum', 'sugarcane', 'Amaranthus']), ('a C3 plant', ['wheat', 'rice', 'potato', 'mustard'])],
    'tf': (['Melvin Calvin used radioactive ¹⁴C in algal photosynthesis studies to discover the first CO₂ fixation product, PGA.', 'In C3 plants the primary CO₂ acceptor is the 5-carbon ribulose bisphosphate (RuBP).',
            'The Calvin cycle occurs in all photosynthetic plants, whether C3 or C4.', 'In C4 plants the Calvin cycle takes place in the bundle sheath cells.',
            'Bundle sheath cells of C4 plants are rich in chloroplasts, have thick walls impervious to gas exchange and have no intercellular spaces.', 'Mesophyll cells of C4 plants lack RuBisCO.'],
           [('The Calvin cycle occurs only in C3 plants.', 'The Calvin cycle occurs in all photosynthetic plants; C4 plants run it in bundle sheath cells.'),
            ('In C4 plants the first stable product is PGA.', 'In C4 plants the first stable product is the 4-carbon OAA; PGA is the first product in C3 plants.'),
            ('Bundle sheath cells of C4 plants lack RuBisCO.', 'Bundle sheath cells are rich in RuBisCO; mesophyll cells lack it and have PEPcase.'),
            ('C4 plants need fewer ATP per CO₂ fixed than C3 plants.', 'C4 plants need 5 ATP per CO₂ (versus 3 in C3) but avoid photorespiration.'),
            ('The primary acceptor in C3 plants is a 3-carbon compound.', 'RuBP, a 5-carbon ketose sugar, is the primary acceptor.')]),
    'orders': [('sequence of stages of the Calvin cycle', ['carboxylation', 'reduction', 'regeneration'], 'CO₂ is fixed to RuBP, PGA is reduced to carbohydrate using ATP and NADPH, then RuBP is regenerated.', '→'),
               ('sequence of events in the C4 pathway', ['PEP accepts CO₂ in mesophyll', 'OAA formed', 'converted to malic or aspartic acid', 'transported to bundle sheath', 'CO₂ released and enters Calvin cycle', 'pyruvate returns to mesophyll'], 'Hatch and Slack pathway.', '→')],
    'ar': [('C4 plants have higher productivity in tropical conditions.', 'They lack photorespiration because RuBisCO in bundle sheath cells works at a high CO₂ concentration.', 'a', 'More carbon fixed.'),
           ('Bundle sheath cells of C4 plants have thick walls.', 'The thick walls are impervious to gaseous exchange and help keep CO₂ concentrated.', 'a', 'Prevents CO₂ leakage and O₂ entry.'),
           ('The C4 pathway is called the Hatch and Slack pathway.', 'In C4 plants the first stable product of CO₂ fixation is a 4-carbon acid.', 'b', 'Both true; the name comes from its discoverers.'),
           ('RuBisCO is present in the mesophyll cells of C4 plants.', 'PEPcase is the primary CO₂-fixing enzyme in C4 plants.', 'd', 'Mesophyll cells of C4 plants lack RuBisCO; R is true.')],
    'features': {'intro': 'A plant shows these features:', 'q': 'Identify the type of plant', 'what': 'plant',
                 'items': [('a C3 plant', ['first stable product is PGA', 'primary CO₂ acceptor is RuBP', 'no Kranz anatomy', 'photorespiration occurs']),
                           ('a C4 plant', ['first stable product is OAA', 'primary CO₂ acceptor is PEP', 'Kranz anatomy present', 'photorespiration absent'])]},
    'fams': [F('C3', 'D3', 'mcq', calvin_cost), F('C3', 'D4', 'numerical', calvin_turns, marks=2), F('C4', 'D4', 'mcq', calvin_cost)],
    'qa': [('C4', 'D3', 'case', 'Leaf sections of maize and wheat from a farm near Ludhiana were compared. Maize showed large cells with many chloroplasts around the veins; wheat did not.\n(i) What is this special anatomy of maize called? (1 mark)\n(ii) Which enzyme fixes CO₂ first in the mesophyll of maize? (1 mark)\n(iii) Why is maize more productive than wheat at high temperatures and high light? (2 marks)',
            '(i) Kranz anatomy. (ii) PEP carboxylase (PEPcase). (iii) Maize is a C4 plant: CO₂ is concentrated in bundle sheath cells, so RuBisCO works as a carboxylase and photorespiration is avoided; the optimum temperature is higher.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the three stages of the Calvin cycle. Calculate the ATP and NADPH needed to make one glucose molecule.',
            'Carboxylation – CO₂ + RuBP → 2 PGA by RuBisCO; reduction – PGA reduced to carbohydrate using 2 ATP and 2 NADPH per CO₂; regeneration – RuBP regenerated using 1 ATP per CO₂. Per CO₂: 3 ATP, 2 NADPH; one glucose needs 6 turns: 18 ATP and 12 NADPH.',
            '3 marks stages; 2 marks calculation.')],
    'q3': [('Give three differences between C3 and C4 plants.',
            'C3 – primary acceptor RuBP, first product PGA, no Kranz anatomy, photorespiration present, Calvin cycle in mesophyll. C4 – primary acceptor PEP, first product OAA, Kranz anatomy, no photorespiration, Calvin cycle in bundle sheath, tolerate higher temperatures.',
            '1 mark each.')],
}

CH11S4 = {
    'topic': 'photorespiration and factors affecting photosynthesis',
    'terms': [('photorespiration', 'a process in which RuBisCO binds O₂ instead of CO₂, forming one PGA and one phosphoglycolate, with no sugar or ATP produced'),
              ("Blackman's law of limiting factors", 'the principle that when a process is affected by several factors, its rate is determined by the factor nearest to its minimal value'),
              ('light saturation', 'the light intensity beyond which an increase in light does not increase the rate of photosynthesis'),
              ('limiting factor', 'the factor that directly affects a process if its quantity is changed, being present at sub-optimal level'),
              ('CO₂ fertilisation', 'growing crops such as tomatoes and bell pepper in greenhouses enriched with CO₂ to raise yields')],
    'groups': [('an external factor affecting photosynthesis', ['light', 'CO₂ concentration', 'temperature', 'water']),
               ('an internal (plant) factor affecting photosynthesis', ['number, size, age and orientation of leaves', 'mesophyll cells and chloroplasts', 'internal CO₂ concentration', 'amount of chlorophyll'])],
    'tf': (['RuBisCO has a much greater affinity for CO₂ than for O₂ when both are at equal concentration.', 'Photorespiration produces neither sugar nor ATP; it results in the release of CO₂ with the use of ATP.',
            'Photorespiration does not occur in C4 plants.', 'CO₂ is the major limiting factor for photosynthesis.', 'Light saturation occurs at about 10 per cent of full sunlight.',
            'C3 plants respond to higher CO₂ concentrations with increased rates of photosynthesis.', 'C4 plants show saturation at about 360 µL L⁻¹ of CO₂.'],
           [('Photorespiration produces ATP and sugar.', 'There is neither synthesis of sugars nor of ATP; ATP is used up.'),
            ('C4 plants have a lower temperature optimum than C3 plants.', 'C4 plants respond to higher temperatures and show a higher rate of photosynthesis; C3 plants have a lower optimum.'),
            ('Light is the most common limiting factor for photosynthesis in nature.', 'Except for plants in shade or dense forests, light is rarely limiting; CO₂ is the major limiting factor.'),
            ('Water stress has no effect on photosynthesis.', 'Water stress causes stomata to close, reducing CO₂ availability, and leaves wilt.')]),
    'ar': [('C4 plants do not show photorespiration.', 'CO₂ is concentrated at the site of RuBisCO in bundle sheath cells, so RuBisCO functions as a carboxylase.', 'a', 'High CO₂ minimises oxygenase activity.'),
           ('Tomatoes in greenhouses give higher yields when CO₂ is enriched.', 'C3 plants respond to higher CO₂ concentration with increased photosynthesis.', 'a', 'CO₂ is limiting for C3 plants.'),
           ('Very high light intensity may decrease photosynthesis.', 'Excess light can break down chlorophyll.', 'a', 'Photo-oxidation of chlorophyll.'),
           ('Photorespiration is a useful process that increases crop yield.', 'In photorespiration RuBP combines with O₂.', 'd', 'Photorespiration is wasteful; R is true.')],
    'features': {'intro': 'A factor affecting photosynthesis is described:', 'q': 'Identify the factor', 'what': 'factor', 'compare': False, 'long': False,
                 'items': [('light', ['quality, intensity and duration matter', 'linear relation at low intensities', 'saturation at about 10% of full sunlight', 'very high intensity may break down chlorophyll']),
                           ('carbon dioxide', ['present at 0.03–0.04 per cent in the atmosphere', 'major limiting factor', 'C3 plants respond to higher concentrations', 'used in greenhouse enrichment for tomatoes']),
                           ('temperature', ['affects the enzymatic dark reactions', 'C4 plants have a higher optimum', 'optimum depends on the habitat of the plant', 'tropical plants have a higher optimum than temperate plants']),
                           ('water', ['affects photosynthesis indirectly', 'stress causes stomata to close', 'reduces CO₂ availability', 'leaves wilt and metabolic activity falls'])]},
    'qa': [('C4', 'D3', 'case', 'A farmer near Nashik grows tomatoes in a polyhouse and adds CO₂ to the air inside. On bright days his yield increases, but raising light intensity further does not help.\n(i) Why does adding CO₂ increase the yield? (1 mark)\n(ii) Why does more light not help beyond a point? (1 mark)\n(iii) State Blackman\'s law of limiting factors and apply it here. (2 marks)',
            '(i) CO₂ is the major limiting factor and tomato (C3) responds to higher CO₂. (ii) Light saturation is reached at about 10% of full sunlight; another factor becomes limiting. (iii) When several factors affect a process, the rate is determined by the factor nearest its minimal value; here CO₂ (not light) limits the rate.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'What is photorespiration? Why is it absent in C4 plants? Explain the effect of light and CO₂ on photosynthesis.',
            'RuBisCO binds O₂: RuBP + O₂ → PGA + phosphoglycolate; no sugar or ATP, CO₂ released, ATP used; wasteful. C4 plants concentrate CO₂ in bundle sheath cells so RuBisCO works as a carboxylase. Light – linear at low intensity, saturates at ~10% full sunlight, excess damages chlorophyll. CO₂ – major limiting factor; 0.03–0.04%; C4 saturate at ~360 µL L⁻¹, C3 respond beyond 450 µL L⁻¹; greenhouse enrichment.',
            '2 marks photorespiration; 1 mark C4; 2 marks factors.')],
    'q3': [('Why is photorespiration considered a wasteful process? Why does it not occur in C4 plants?',
            'RuBisCO combines RuBP with O₂ forming PGA and phosphoglycolate; there is no synthesis of sugar or ATP, CO₂ is released and ATP is consumed. In C4 plants malate releases CO₂ in bundle sheath cells, raising its concentration so RuBisCO acts as a carboxylase.',
            '2 marks wasteful; 1 mark C4.')],
}

# ---------------------------------------------------------------- ch12 respiration

def atp_yield(r):
    n = r.choice([1, 2, 3, 4, 5, 6, 10])
    kind = r.choice(['aerobic', 'glycolysis', 'fermentation'])
    per = {'aerobic': 38, 'glycolysis': 2, 'fermentation': 2}[kind]
    good = per * n
    desc = {'aerobic': 'complete aerobic oxidation (net gain as per NCERT)', 'glycolysis': 'glycolysis alone (net gain)', 'fermentation': 'alcoholic fermentation by yeast (net gain)'}[kind]
    cands = [38 * n, 36 * n, 2 * n, 4 * n, 8 * n, 19 * n]
    return mcq(f'What is the net number of ATP molecules gained from {n} molecule{"s" if n > 1 else ""} of glucose by {desc}?', str(good), _w(good, cands),
               f'Net ATP per glucose: aerobic 38, glycolysis 2, fermentation 2. For {n} glucose: {good}.', r)


def krebs_count(r):
    n = r.choice([1, 2, 3, 4, 5, 6])
    what = r.choice(['NADH₂ (NADH + H⁺)', 'FADH₂', 'ATP (as GTP/ATP by substrate-level phosphorylation)', 'CO₂'])
    per_turn = {'NADH₂ (NADH + H⁺)': 3, 'FADH₂': 1, 'ATP (as GTP/ATP by substrate-level phosphorylation)': 1, 'CO₂': 2}[what]
    unit = r.choice(['acetyl CoA', 'glucose'])
    turns = n if unit == 'acetyl CoA' else 2 * n
    good = per_turn * turns
    cands = [good // 2 if good % 2 == 0 else good + 3, good * 2, good + 1, per_turn * n * 3, good - 1 if good > 1 else good + 4]
    return mcq(f'How many molecules of {what} are produced in the Krebs cycle from {n} molecule{"s" if n > 1 else ""} of {unit}?',
               str(good), _w(good, cands), f'Each turn (one acetyl CoA) gives 3 NADH₂, 1 FADH₂, 1 ATP and 2 CO₂; one glucose gives 2 acetyl CoA. {turns} turn(s) × {per_turn} = {good}.', r)


def rq_calc(r):
    subs = [('glucose (C₆H₁₂O₆)', 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', 6, 6), ('tripalmitin (C₅₁H₉₈O₆)', '2C₅₁H₉₈O₆ + 145O₂ → 102CO₂ + 98H₂O', 102, 145),
            ('oxalic acid (C₂H₂O₄)', '2C₂H₂O₄ + O₂ → 4CO₂ + 2H₂O', 4, 1), ('malic acid (C₄H₆O₅)', 'C₄H₆O₅ + 3O₂ → 4CO₂ + 3H₂O', 4, 3),
            ('tartaric acid (C₄H₆O₆)', '2C₄H₆O₆ + 5O₂ → 8CO₂ + 6H₂O', 8, 5), ('citric acid (C₆H₈O₇)', '2C₆H₈O₇ + 9O₂ → 12CO₂ + 8H₂O', 12, 9)]
    s, eq, c, o = r.choice(subs)
    rq = c / o
    good = num(rq, 2)
    cands = [num(o / c, 2), '1', '0.7', '0.9', num(rq + 0.5, 2), '4']
    return {'stem': f'Calculate the respiratory quotient (RQ) when {s} is the respiratory substrate. The balanced equation is: {eq}.',
            'answer': f'RQ = {c}/{o} = {good}', 'key': f'RQ = volume of CO₂ evolved / volume of O₂ consumed (1) = {c}/{o} = {good} (1).',
            'distractors': [f'RQ = {x}' for x in _w(good, cands)], 'marks': 2}


CH12S1 = {
    'topic': 'glycolysis and fermentation',
    'terms': [('glycolysis', 'the partial oxidation of glucose to two molecules of pyruvic acid in the cytoplasm, also called the EMP pathway'),
              ('fermentation', 'the incomplete oxidation of glucose under anaerobic conditions by sets of reactions in which pyruvic acid is converted to CO₂ and ethanol or to lactic acid'),
              ('substrate-level phosphorylation', 'direct synthesis of ATP from a high-energy substrate, as in the conversion of PEP to pyruvic acid'),
              ('respiration', 'the breaking of C–C bonds of complex compounds through oxidation within cells, leading to release of energy'),
              ('respiratory substrates', 'compounds that are oxidised during respiration, usually carbohydrates'),
              ('lactic acid fermentation', 'the reduction of pyruvic acid to lactic acid by lactate dehydrogenase, as in some bacteria and in muscles during vigorous exercise')],
    'tf': (['Glycolysis takes place in the cytoplasm of all living organisms.', 'In glycolysis, glucose is partially oxidised to two molecules of pyruvic acid.',
            'Glycolysis was given by Gustav Embden, Otto Meyerhof and J. Parnas.', 'In plants glucose is derived from sucrose by the enzyme invertase.',
            'Yeasts poison themselves to death when the alcohol concentration reaches about 13 per cent.', 'In fermentation, less than seven per cent of the energy in glucose is released.'],
           [('Glycolysis occurs in the mitochondria.', 'Glycolysis occurs in the cytoplasm.'),
            ('Glycolysis requires oxygen.', 'Glycolysis is common to aerobic and anaerobic respiration and does not need oxygen.'),
            ('In alcoholic fermentation, pyruvic acid is converted to lactic acid.', 'Yeast converts pyruvic acid to CO₂ and ethanol; lactic acid is formed in muscles and some bacteria.'),
            ('Fermentation releases most of the energy stored in glucose.', 'Less than 7% of the energy in glucose is released and not all of it is trapped as ATP.')]),
    'orders': [('sequence of glycolysis', ['glucose', 'glucose-6-phosphate', 'fructose-6-phosphate', 'fructose 1,6-bisphosphate', 'triose phosphate', '1,3-bisphosphoglycerate', '3-phosphoglyceric acid', 'phosphoenol pyruvate', 'pyruvic acid'], 'EMP pathway as in NCERT.', '→')],
    'ar': [('Muscles develop fatigue during vigorous exercise.', 'Under anaerobic conditions pyruvic acid is reduced to lactic acid in muscles.', 'a', 'Lactic acid accumulates.'),
           ('Glycolysis is the only process of respiration in anaerobic organisms.', 'Glycolysis does not require oxygen.', 'a', 'It works without O₂.'),
           ('NAD⁺ is regenerated during fermentation.', 'NADH + H⁺ is used to reduce pyruvic acid or acetaldehyde.', 'a', 'Allows glycolysis to continue.'),
           ('Fermentation yields 38 ATP per glucose.', 'Fermentation is incomplete oxidation of glucose.', 'd', 'Net gain is only 2 ATP; R is true.')],
    'features': {'intro': 'A pathway of glucose breakdown has these features:', 'q': 'Identify the pathway', 'what': 'pathway',
                 'items': [('alcoholic fermentation', ['occurs in yeast under anaerobic conditions', 'pyruvic acid converted to CO₂ and ethanol', 'enzymes pyruvic acid decarboxylase and alcohol dehydrogenase', 'net gain 2 ATP per glucose']),
                           ('lactic acid fermentation', ['occurs in muscles during vigorous exercise and in some bacteria', 'pyruvic acid reduced to lactic acid', 'enzyme lactate dehydrogenase', 'no CO₂ released']),
                           ('aerobic respiration', ['requires O₂', 'complete oxidation of glucose to CO₂ and H₂O', 'Krebs cycle and ETS in mitochondria', 'net gain of 38 ATP per glucose (NCERT)'])]},
    'fams': [F('C3', 'D3', 'mcq', atp_yield)],
    'qa': [('C4', 'D3', 'case', 'At a bakery in Kolkata, dough left with yeast becomes soft and spongy, and a faint smell of alcohol is noticed.\n(i) Name the process. (1 mark)\n(ii) Name the products formed from pyruvic acid. (1 mark)\n(iii) Why does this process yield little energy? Name the enzymes involved. (2 marks)',
            '(i) Alcoholic fermentation. (ii) CO₂ (makes dough spongy) and ethanol. (iii) Glucose is only partially oxidised; net gain 2 ATP; enzymes pyruvic acid decarboxylase and alcohol dehydrogenase.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the steps of glycolysis. Where are ATP used and formed? What is the net gain?',
            'Glucose phosphorylated to G6P by hexokinase (ATP used); isomerised to F6P; phosphorylated to fructose 1,6-bisphosphate (ATP used); split into two triose phosphates; PGAL oxidised to 1,3-BPGA (NADH + H⁺ formed); 1,3-BPGA → 3-PGA (ATP formed); PEP → pyruvic acid (ATP formed). 2 ATP used, 4 ATP formed directly; net 2 ATP and 2 NADH per glucose.',
            '3 marks steps; 2 marks energetics.')],
    'q3': [('Distinguish between alcoholic and lactic acid fermentation on three points.',
            'Alcoholic – in yeast; pyruvic acid → CO₂ + ethanol; enzymes pyruvic acid decarboxylase and alcohol dehydrogenase; CO₂ released. Lactic acid – in muscles and some bacteria; pyruvic acid → lactic acid; enzyme lactate dehydrogenase; no CO₂ released.',
            '1 mark each.')],
}

CH12S2 = {
    'topic': 'aerobic respiration: the Krebs cycle and the electron transport system',
    'terms': [('oxidative decarboxylation', 'the conversion of pyruvic acid to acetyl CoA by pyruvic dehydrogenase, releasing CO₂ and NADH'),
              ('Krebs cycle', 'the tricarboxylic acid cycle in the mitochondrial matrix that oxidises acetyl CoA'),
              ('citric acid', 'the 6-carbon first product of the Krebs cycle, formed by condensation of acetyl CoA with OAA and water'),
              ('electron transport system (ETS)', 'the metabolic pathway in the inner mitochondrial membrane through which electrons pass from one carrier to another'),
              ('oxidative phosphorylation', 'the synthesis of ATP using energy from oxidation-reduction reactions of the ETS'),
              ('complex V (ATP synthase)', 'the enzyme complex of the inner mitochondrial membrane with F₀ and F₁ parts that synthesises ATP')],
    'tf': (['The Krebs cycle takes place in the matrix of mitochondria.', 'Oxygen acts as the final hydrogen acceptor in aerobic respiration.', 'Ubiquinone receives reducing equivalents from both FADH₂ and NADH.',
            'Cytochrome c is a small protein attached to the outer surface of the inner membrane that transfers electrons between complex III and complex IV.', 'One NADH gives rise to 3 ATP and one FADH₂ to 2 ATP in oxidative phosphorylation.',
            'The F₁ headpiece of ATP synthase is the site of ATP synthesis from ADP and Pi.'],
           [('The ETS is located in the matrix of the mitochondrion.', 'The ETS is present in the inner mitochondrial membrane.'),
            ('Oxygen is the first electron acceptor of the ETS.', 'Oxygen is the final acceptor; it combines with electrons and H⁺ to form water.'),
            ('The F₀ part of ATP synthase synthesises ATP.', 'F₀ forms the proton channel; F₁ synthesises ATP.'),
            ('Pyruvic acid is converted to acetyl CoA in the cytoplasm.', 'Oxidative decarboxylation occurs in the mitochondrial matrix.'),
            ('One turn of the Krebs cycle produces 3 ATP directly.', 'One turn gives 1 ATP (GTP) by substrate-level phosphorylation, besides 3 NADH and 1 FADH₂.')]),
    'orders': [('sequence of electron flow in the mitochondrial ETS', ['NADH', 'complex I', 'ubiquinone', 'complex III', 'cytochrome c', 'complex IV', 'O₂'], 'Electrons pass from NADH to O₂ through complexes I, III and IV.', '→')],
    'ar': [('Oxygen is vital for aerobic respiration even though it acts only at the end of the process.', 'Oxygen drives the whole process by removing hydrogen from the system as the final acceptor.', 'a', 'Without O₂ the ETS stops.'),
           ('NADH yields more ATP than FADH₂ in oxidative phosphorylation.', 'Electrons from NADH enter the ETS at complex I, while those from FADH₂ enter at complex II.', 'a', 'More proton pumping from NADH.'),
           ('The Krebs cycle is also called the citric acid cycle.', 'Citric acid is the first product of the cycle.', 'a', 'Named after its first product.'),
           ('Glycolysis takes place inside mitochondria.', 'Pyruvic acid enters the mitochondria for further oxidation.', 'd', 'Glycolysis occurs in the cytoplasm; R is true.')],
    'features': {'intro': 'A stage of aerobic respiration has these features:', 'q': 'Identify the stage', 'what': 'stage',
                 'items': [('oxidative decarboxylation of pyruvate', ['occurs in the mitochondrial matrix', 'catalysed by pyruvic dehydrogenase', 'produces acetyl CoA, CO₂ and NADH', 'needs coenzyme A and NAD⁺']),
                           ('the Krebs cycle', ['occurs in the mitochondrial matrix', 'starts with condensation of acetyl CoA and OAA', 'produces 3 NADH, 1 FADH₂, 1 ATP per turn', 'releases 2 CO₂ per turn']),
                           ('the electron transport system', ['located in the inner mitochondrial membrane', 'electrons pass through complexes I to IV', 'O₂ is the final acceptor', 'forms water']),
                           ('oxidative phosphorylation', ['ATP synthesised by complex V', 'driven by the proton gradient', 'protons pass through F₀ channel', 'F₁ headpiece synthesises ATP'])]},
    'fams': [F('C3', 'D3', 'mcq', krebs_count), F('C4', 'D4', 'mcq', krebs_count)],
    'qa': [('C4', 'D3', 'case', 'A poison such as cyanide blocks complex IV (cytochrome c oxidase) of the mitochondria in a patient admitted to a hospital in Ranchi.\n(i) What is the normal role of complex IV? (1 mark)\n(ii) What would happen to ATP production by oxidative phosphorylation? (1 mark)\n(iii) Explain why the Krebs cycle would also slow down. (2 marks)',
            '(i) It passes electrons to O₂, the final acceptor, forming water. (ii) It would stop because electron flow and proton pumping stop. (iii) NADH and FADH₂ can no longer be oxidised, so NAD⁺ and FAD are not regenerated for the Krebs cycle reactions.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the Krebs cycle and the electron transport system. How is ATP formed in oxidative phosphorylation?',
            'Acetyl CoA + OAA + H₂O → citric acid (citrate synthase); isomerised to isocitrate; two decarboxylations → α-ketoglutaric acid → succinyl CoA; succinyl CoA → succinic acid (GTP/ATP); OAA regenerated; per turn 3 NADH, 1 FADH₂, 1 ATP, 2 CO₂. ETS: NADH → complex I → ubiquinone; FADH₂ → complex II → ubiquinone; → complex III → cytochrome c → complex IV → O₂ + H⁺ → water. Proton gradient; H⁺ flows through F₀ of complex V; F₁ synthesises ATP; 3 ATP per NADH, 2 per FADH₂.',
            '2 marks Krebs; 2 marks ETS; 1 mark oxidative phosphorylation.')],
    'q3': [('Name the products of one turn of the Krebs cycle and state where they go.',
            '3 NADH + H⁺ and 1 FADH₂ – go to the ETS for oxidative phosphorylation; 1 ATP (GTP) – used by the cell; 2 CO₂ – released; OAA regenerated for the next turn.',
            '1 mark each for NADH/FADH₂, ATP, CO₂.')],
}

CH12S3 = {
    'topic': 'the respiratory balance sheet, amphibolic pathway and respiratory quotient',
    'terms': [('respiratory balance sheet', 'a theoretical calculation of the net ATP gain per glucose molecule oxidised, assuming a sequential, orderly pathway'),
              ('amphibolic pathway', 'a pathway involved in both breakdown (catabolism) and synthesis (anabolism), as the respiratory pathway is'),
              ('respiratory quotient (RQ)', 'the ratio of the volume of CO₂ evolved to the volume of O₂ consumed in respiration'),
              ('acetyl CoA', 'the common intermediate through which fats and proteins enter the respiratory pathway')],
    'groups': [('a substrate with RQ of 1', ['glucose', 'fructose', 'sucrose']), ('a substrate with RQ less than 1', ['tripalmitin (fat)', 'proteins']),
               ('a substrate with RQ more than 1', ['oxalic acid', 'malic acid', 'tartaric acid'])],
    'tf': (['When carbohydrates are used as substrate, the RQ is 1.', 'When fats are used in respiration, the RQ is less than 1.', 'The RQ of proteins is about 0.9.',
            'Fats are broken down into glycerol and fatty acids; fatty acids enter the pathway as acetyl CoA.', 'Glycerol enters the respiratory pathway after being converted to PGAL.',
            'The net gain of 38 ATP per glucose is a theoretical value based on assumptions.'],
           [('The RQ of fats is greater than 1.', 'The RQ of fats is less than 1, e.g. 0.7 for tripalmitin.'),
            ('Respiration is purely a catabolic process.', 'It is amphibolic: intermediates are also used to synthesise fats, proteins and other compounds.'),
            ('Proteins enter the respiratory pathway only as glucose.', 'Proteins are broken into amino acids, which after deamination enter at pyruvic acid, acetyl CoA or stages of the Krebs cycle.'),
            ('In living systems only glucose is respired and all pathways work simultaneously and independently.', 'The balance sheet assumes this; in reality pathways work simultaneously, intermediates are withdrawn and other substrates enter.')]),
    'ar': [('The respiratory pathway is called amphibolic.', 'Its intermediates are used in both catabolism and anabolism.', 'a', 'Example: acetyl CoA used for fatty acid synthesis.'),
           ('The RQ of tripalmitin is 0.7.', 'Fats are poor in oxygen, so more O₂ is consumed than CO₂ released.', 'a', '102 CO₂ / 145 O₂ = 0.7.'),
           ('The calculation of 38 ATP per glucose is only theoretical.', 'Pathways in a living cell work simultaneously and substrates enter and are withdrawn as needed.', 'a', 'Assumptions of the balance sheet do not hold.'),
           ('The RQ of organic acids is less than 1.', 'Organic acids are rich in oxygen.', 'd', 'RQ of organic acids is more than 1; R is true.')],
    'features': {'intro': 'A respiratory substrate is described:', 'q': 'Identify the substrate class', 'what': 'substrate', 'compare': False,
                 'items': [('carbohydrates', ['RQ equal to 1', 'equal volumes of CO₂ evolved and O₂ consumed', 'commonest substrate', 'enter as glucose']),
                           ('fats', ['RQ less than 1, e.g. 0.7', 'broken to glycerol and fatty acids', 'fatty acids enter as acetyl CoA', 'glycerol enters as PGAL']),
                           ('proteins', ['RQ about 0.9', 'broken to amino acids by proteases', 'amino acids deaminated', 'enter at pyruvic acid, acetyl CoA or the Krebs cycle']),
                           ('organic acids', ['RQ more than 1', 'rich in oxygen', 'e.g. oxalic and malic acid', 'consume less O₂ than CO₂ released'])]},
    'fams': [F('C3', 'D3', 'numerical', rq_calc, marks=2), F('C3', 'D4', 'numerical', rq_calc, marks=2)],
    'qa': [('C4', 'D3', 'case', 'In a seed germination experiment in Mysuru, germinating groundnut seeds released 70 mL of CO₂ while consuming 100 mL of O₂, and germinating wheat grains released 50 mL of CO₂ while consuming 50 mL of O₂.\n(i) Calculate the RQ for each. (2 marks)\n(ii) Identify the main respiratory substrate in each. (1 mark)\n(iii) Why is the RQ of fats less than 1? (1 mark)',
            '(i) Groundnut 70/100 = 0.7; wheat 50/50 = 1. (ii) Groundnut – fats; wheat – carbohydrates (starch). (iii) Fats contain less oxygen relative to carbon and hydrogen, so more O₂ is needed than CO₂ released.',
            '(i) 1 + 1 (ii) 1 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'What are the assumptions of the respiratory balance sheet? Explain why the respiratory pathway is considered amphibolic.',
            'Assumptions: sequential, orderly pathway (glycolysis → TCA → ETS); NADH from glycolysis enters mitochondria for oxidative phosphorylation; no intermediate used to synthesise other compounds; only glucose respired, no alternative substrates enter. Net 38 ATP theoretical. Amphibolic: fats enter as acetyl CoA/PGAL and acetyl CoA is withdrawn for fatty acid synthesis; proteins enter after deamination and intermediates are withdrawn for amino acid synthesis; so both catabolism and anabolism.',
            '2 marks assumptions; 3 marks amphibolic.')],
    'q3': [('How do fats and proteins enter the respiratory pathway?',
            'Fats → glycerol and fatty acids; fatty acids are degraded to acetyl CoA and enter the Krebs cycle; glycerol converted to PGAL enters glycolysis. Proteins → amino acids by proteases; after deamination, depending on structure, they enter as pyruvic acid, acetyl CoA or within the Krebs cycle.',
            '1½ marks each.')],
}

# ---------------------------------------------------------------- ch13 plant growth

def growth_rate(r):
    a0 = r.choice([2, 4, 5, 8, 10, 12, 20, 25])
    a1 = a0 * r.choice([2, 3, 4, 5])
    t = r.choice([1, 2, 4, 5])
    abs_rate = (a1 - a0) / t
    rel = Fraction(a1 - a0, a0 * t)
    what = r.choice(['absolute', 'relative'])
    if what == 'absolute':
        good = f'{num(abs_rate, 2)} cm² per day'
        wrong = [f'{num(x, 2)} cm² per day' for x in dict.fromkeys([a1 / t, a1 - a0, abs_rate * 2, abs_rate / 2]) if num(x, 2) != num(abs_rate, 2)][:3]
        key = f'Absolute growth rate = increase per unit time = ({a1} − {a0})/{t} = {num(abs_rate, 2)} cm² per day.'
    else:
        good = f'{num(float(rel), 3)} per day'
        wrong = [f'{num(x, 3)} per day' for x in dict.fromkeys([float(rel) * 2, (a1 - a0) / a1 / t, a1 / a0, float(rel) / 2]) if num(x, 3) != num(float(rel), 3)][:3]
        key = f'Relative growth rate = growth per unit time / initial parameter = ({a1} − {a0})/({a0} × {t}) = {num(float(rel), 3)} per day.'
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'A leaf grew from {a0} cm² to {a1} cm² in {t} day{"s" if t > 1 else ""}. What is its {what} growth rate?', good, wrong, key, r)


def exp_growth(r):
    w0 = r.choice([1, 2, 5, 10])
    rr = r.choice([0.1, 0.2, 0.3, 0.5])
    t = r.choice([2, 4, 5, 10])
    import math
    w = w0 * math.exp(rr * t)
    return {'stem': f'A plant in its exponential phase grows according to W₁ = W₀e^(rt). If the initial size W₀ = {w0} g and the relative growth rate r = {rr} per day, find the size after {t} days. (Take e as 2.718.)',
            'answer': f'{sf(w, 3)} g', 'key': f'W₁ = {w0} × e^({rr} × {t}) = {w0} × e^{num(rr * t, 2)} (1) = {sf(w, 3)} g (1).',
            'distractors': [f'{sf(w0 * (1 + rr * t), 3)} g', f'{sf(w0 * rr * t, 3)} g', f'{sf(w * 2, 3)} g'], 'marks': 2}


CH13S1 = {
    'topic': 'growth, growth rates, differentiation and development',
    'terms': [('growth', 'an irreversible permanent increase in size of an organ, its parts or even of an individual cell'),
              ('open form of growth', 'the ability of plants to grow throughout life due to meristems at certain locations'),
              ('arithmetic growth', 'growth in which only one daughter cell continues to divide after mitosis, giving a linear curve'),
              ('geometric growth', 'growth in which both progeny cells continue to divide, with an initial slow lag phase followed by a rapid exponential phase'),
              ('differentiation', 'the process by which cells derived from meristems mature to perform specific functions'),
              ('dedifferentiation', 'the regaining of the capacity to divide by differentiated cells, as in the formation of interfascicular cambium'),
              ('redifferentiation', 'the loss of the capacity to divide again by cells produced by dedifferentiated cells, which then mature to perform specific functions'),
              ('plasticity', 'the ability of plants to follow different pathways in response to environment or phases of life to form different structures, e.g. heterophylly')],
    'groups': [('an example of heterophylly due to the environment', ['buttercup']), ('an example of heterophylly in development', ['cotton', 'coriander', 'larkspur'])],
    'tf': (['A maize root apical meristem can give rise to more than 17,500 new cells per hour.', 'Cells of a watermelon may increase in size by up to 3,50,000 times.',
            'The pollen tube can grow in length by cell elongation.', 'The sigmoid growth curve has a lag phase, a log or exponential phase and a stationary phase.',
            'Growth in plants requires water, oxygen, nutrients and an optimum temperature.', 'Tracheary elements lose their protoplasm during differentiation.'],
           [('Growth is a reversible increase in size.', 'Growth is an irreversible, permanent increase in size.'),
            ('Arithmetic growth gives a sigmoid curve.', 'Arithmetic growth gives a linear curve; geometric growth gives a sigmoid curve when limited.'),
            ('Absolute growth rate compares growth per unit time relative to the initial size.', 'That is the relative growth rate; absolute growth rate is total growth per unit time.'),
            ('Plants grow only up to a certain age.', 'Plants show indeterminate (open) growth throughout life due to meristems.')]),
    'orders': [('phases of growth in the meristematic zone of a root tip', ['meristematic phase', 'elongation phase', 'maturation phase'], 'Cells divide at the apex, elongate behind it and mature further away.', '→'),
               ('phases of a sigmoid growth curve', ['lag phase', 'log (exponential) phase', 'stationary phase'], 'Slow start, rapid growth, then a plateau as nutrients become limiting.', '→')],
    'ar': [('Plant growth is described as open.', 'Plants have meristems that retain the capacity to divide throughout life.', 'a', 'Continuous addition of new cells.'),
           ('Interfascicular cambium forms by dedifferentiation.', 'Fully differentiated parenchyma cells regain the capacity to divide.', 'a', 'Definition of dedifferentiation.'),
           ('Heterophylly in buttercup is an example of plasticity.', 'Leaves of buttercup in air differ from those produced in water.', 'a', 'Environment-induced form.'),
           ('Relative growth rate is the same for two leaves that show the same absolute increase.', 'Relative growth rate takes the initial size into account.', 'd', 'Leaves of different initial size have different relative rates; R is true.')],
    'features': {'intro': 'A phase of plant growth is described:', 'q': 'Identify the phase', 'what': 'phase',
                 'items': [('the meristematic phase', ['cells at the root and shoot apex divide constantly', 'rich in protoplasm', 'large conspicuous nuclei', 'thin cellulosic primary walls with many plasmodesmata']),
                           ('the elongation phase', ['zone just behind the meristem', 'increased vacuolation', 'cell enlargement', 'new cell wall deposition']),
                           ('the maturation phase', ['further away from the apex', 'cells attain maximal size', 'cell wall thickening', 'protoplasmic modifications'])]},
    'fams': [F('C3', 'D3', 'mcq', growth_rate), F('C4', 'D4', 'numerical', exp_growth, marks=2)],
    'qa': [('C4', 'D3', 'case', 'Two leaves A and B were measured by Kunal in Dehradun. Leaf A grew from 5 cm² to 10 cm²; leaf B grew from 50 cm² to 55 cm² in the same day.\n(i) Compare their absolute growth rates. (1 mark)\n(ii) Calculate their relative growth rates. (2 marks)\n(iii) Which leaf shows faster relative growth and why is this measure useful? (1 mark)',
            '(i) Both 5 cm² per day – equal. (ii) A: 5/5 = 1 (100%) per day; B: 5/50 = 0.1 (10%) per day. (iii) Leaf A; relative growth rate takes the initial size into account.',
            '(i) 1 (ii) 1 + 1 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'Distinguish between arithmetic and geometric growth with equations and curves. What are the conditions for growth?',
            'Arithmetic: one daughter cell divides, the other differentiates; Lt = L₀ + rt; linear curve (root elongating at constant rate). Geometric: both divide; initial lag, exponential (log) phase, stationary phase – sigmoid curve; W₁ = W₀e^(rt). Conditions: water (turgidity, enzymatic activity), oxygen (metabolic energy), nutrients, optimum temperature, light and gravity.',
            '3 marks growth types; 2 marks conditions.')],
    'q3': [('Explain differentiation, dedifferentiation and redifferentiation with an example of each.',
            'Differentiation – meristem cells mature for specific functions, e.g. tracheary elements lose protoplasm and develop lignified walls; dedifferentiation – differentiated cells regain the ability to divide, e.g. interfascicular cambium and cork cambium from parenchyma; redifferentiation – cells formed again lose the ability to divide and mature, e.g. secondary xylem from cambium.',
            '1 mark each.')],
}

CH13S2 = {
    'topic': 'plant growth regulators',
    'terms': [('auxins', 'plant growth regulators, first isolated from human urine, such as IAA, that promote apical dominance and rooting'),
              ('gibberellins', 'acidic plant growth regulators, more than 100 of which are known, that cause stem elongation and bolting'),
              ('cytokinins', 'plant growth regulators with cytokinesis-promoting activity, first discovered as kinetin from autoclaved herring sperm DNA'),
              ('ethylene', 'a simple gaseous plant growth regulator that promotes ripening of fruits and senescence'),
              ('abscisic acid (ABA)', 'a plant growth inhibitor that acts as a stress hormone and induces dormancy and stomatal closure'),
              ('apical dominance', 'the phenomenon in which the growing apical bud inhibits the growth of lateral buds'),
              ('bolting', 'internode elongation just prior to flowering in rosette plants such as cabbage, promoted by gibberellins'),
              ('parthenocarpy', 'the formation of fruits without fertilisation, induced by auxins in tomatoes')],
    'groups': [('a plant growth promoter', ['auxins', 'gibberellins', 'cytokinins']), ('a plant growth inhibitor', ['abscisic acid', 'ethylene'])],
    'groups2': [('a natural auxin', ['IAA (indole-3-acetic acid)', 'IBA (indole butyric acid)']), ('a synthetic auxin', ['NAA (naphthalene acetic acid)', '2,4-D']),
                ('a source of ethylene used in agriculture', ['ethephon'])],
    'tf': (['Charles Darwin and his son Francis Darwin observed that coleoptiles of canary grass bend towards a unilateral light source.', 'F.W. Went isolated auxin from the tips of oat coleoptiles.',
            'E. Kurosawa reported the bakanae (foolish seedling) disease of rice caused by the fungus Gibberella fujikuroi.', 'Skoog and Miller identified kinetin.',
            '2,4-D is widely used to kill dicotyledonous weeds without affecting mature monocot plants.', 'Gibberellins are used to increase the length of grape stalks and to elongate apples.',
            'Ethylene promotes rapid internode/petiole elongation in deep water rice plants.', 'ABA is called the stress hormone.'],
           [('Cytokinins promote apical dominance.', 'Cytokinins help overcome apical dominance; auxins promote it.'),
            ('Ethylene delays ripening of fruits.', 'Ethylene promotes ripening and enhances respiration rate during ripening (respiratory climacteric).'),
            ('ABA promotes seed germination.', 'ABA inhibits seed germination and induces dormancy.'),
            ('Gibberellins were first isolated from human urine.', 'Auxins were first isolated from human urine; gibberellins were found from Gibberella fujikuroi.'),
            ('2,4-D is used to kill monocot weeds in wheat fields.', '2,4-D kills dicot weeds and does not affect mature monocot plants.')]),
    'ar': [('Removal of the shoot tip results in growth of lateral buds.', 'Auxin from the apical bud inhibits growth of lateral buds (apical dominance).', 'a', 'Removing the source of auxin releases lateral buds; used in tea plantations and hedge-making.'),
           ('Spraying sugarcane with gibberellins increases yield.', 'Gibberellins increase the length of the stem, where sugar is stored.', 'a', 'Up to 20 tonnes per acre more.'),
           ('ABA is called the stress hormone.', 'ABA increases tolerance of plants to various kinds of stresses and closes stomata.', 'a', 'Stress tolerance.'),
           ('Cytokinins delay leaf senescence.', 'They promote nutrient mobilisation.', 'a', 'Nutrient mobilisation delays senescence.'),
           ('Ethylene is used to delay flowering in pineapple.', 'Ethylene is a gaseous PGR.', 'd', 'Ethylene promotes and synchronises flowering in pineapple; R is true.')],
    'features': {'intro': 'A plant growth regulator shows these effects:', 'q': 'Identify the PGR', 'what': 'PGR',
                 'items': [('auxin', ['initiates rooting in stem cuttings', 'promotes apical dominance', 'induces parthenocarpy in tomatoes', '2,4-D form used as a weedicide']),
                           ('gibberellin', ['increases length of grape stalks', 'causes bolting in cabbage', 'speeds up malting in brewing', 'hastens maturity in conifers']),
                           ('cytokinin', ['promotes cell division', 'helps produce new leaves and chloroplasts', 'overcomes apical dominance', 'delays leaf senescence']),
                           ('ethylene', ['promotes ripening of fruits', 'promotes senescence and abscission', 'breaks seed and bud dormancy', 'induces flowering in mango and pineapple']),
                           ('abscisic acid', ['inhibits seed germination', 'stimulates closure of stomata', 'induces dormancy', 'increases tolerance to stress'])]},
    'qa': [('C4', 'D3', 'case', 'A fruit seller in Surat keeps unripe mangoes in a closed box with a few ripe bananas, and they ripen faster. A tea planter in Assam regularly plucks the tips of tea bushes.\n(i) Which PGR released by ripe bananas speeds ripening? (1 mark)\n(ii) Why does plucking tips make tea bushes bushy? (1 mark)\n(iii) Name one compound used to supply this PGR commercially and two other uses of it. (2 marks)',
            '(i) Ethylene. (ii) Removal of the apical bud removes the source of auxin, so apical dominance is broken and lateral buds grow. (iii) Ethephon; promotes and synchronises flowering in pineapple, induces flowering in mango, promotes female flowers in cucumber, breaks seed dormancy, hastens fruit ripening.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the discovery and physiological effects of auxins and gibberellins.',
            'Auxin: Darwins – coleoptile phototropism; Went isolated auxin from oat coleoptile tips; first isolated from human urine; IAA, IBA natural, NAA, 2,4-D synthetic. Effects – rooting of cuttings, flowering in pineapple, prevents premature fruit drop, apical dominance, parthenocarpy, xylem differentiation, weedicide. Gibberellin: Kurosawa – bakanae disease of rice by Gibberella fujikuroi; GA₃; effects – stem elongation, grape stalks, apple shape, delay senescence, malting, sugarcane yield, early seed production in conifers, bolting.',
            '2½ marks each.')],
    'q3': [('Give the physiological effects of cytokinins.',
            'Promote cell division; help produce new leaves and chloroplasts in leaves; promote lateral shoot growth and adventitious shoot formation; help overcome apical dominance; promote nutrient mobilisation, delaying leaf senescence.',
            '1 mark each for any three.'),
           ('Name the PGR you would use to (i) induce rooting in a twig, (ii) quickly ripen a fruit, (iii) delay leaf senescence.',
            '(i) Auxin (IBA/NAA); (ii) ethylene (ethephon); (iii) cytokinin.', '1 mark each.')],
}

CH13S3 = {
    'topic': 'seed germination, dormancy, photoperiodism and vernalisation',
    'terms': [('seed dormancy', 'a condition in which a seed fails to germinate even under favourable external conditions because of internal (endogenous) factors'),
              ('photoperiodism', 'the response of plants to periods of day and night'),
              ('long day plants', 'plants that require exposure to light for a period exceeding a critical duration to induce flowering'),
              ('short day plants', 'plants that must be exposed to light for a period less than a critical duration before flowering is initiated'),
              ('day-neutral plants', 'plants in which there is no correlation between exposure to light duration and induction of flowering'),
              ('vernalisation', 'the dependence of flowering on exposure to low temperature, which prevents precocious reproductive development'),
              ('scarification', 'breaking an impermeable seed coat by mechanical abrasions or vigorous shaking to overcome dormancy')],
    'tf': (['Seed dormancy may be due to an impermeable, hard seed coat, chemical inhibitors such as ABA or an immature embryo.', 'The site of perception of photoperiod is the leaf.',
            'Some varieties of wheat, barley and rye have spring and winter varieties.', 'Biennial plants are monocarpic plants that flower and die in the second season.',
            'Winter varieties of cereals, if planted in spring, normally fail to flower before the end of the growing season.', 'Dormancy can be overcome by treatment with gibberellic acid and nitrates.'],
           [('The shoot apex perceives the photoperiod directly.', 'The leaves perceive the light/dark periods; a hormonal signal moves to the shoot apex.'),
            ('Vernalisation refers to exposure of plants to high temperature.', 'Vernalisation is exposure to low temperature to promote flowering.'),
            ('All plants need a specific photoperiod to flower.', 'Day-neutral plants flower irrespective of the duration of light.'),
            ('Seed dormancy is caused only by external factors.', 'Dormancy is due to internal (endogenous) factors; quiescence is due to unfavourable external conditions.')]),
    'ar': [('Winter wheat must be exposed to low temperature to flower.', 'Vernalisation prevents precocious reproductive development late in the growing season.', 'a', 'Cold exposure induces flowering in the next season.'),
           ('The leaves perceive the photoperiodic stimulus.', 'A hormonal substance is thought to move from the leaves to the shoot apices for flowering.', 'a', 'Florigen hypothesis.'),
           ('Gibberellic acid can break seed dormancy.', 'Gibberellins counter the inhibitory effects of ABA.', 'a', 'Promotes germination.'),
           ('Biennial plants flower in their first season.', 'Biennials such as sugarbeet, cabbages and carrots need a cold treatment to flower.', 'd', 'They flower in the second season after vernalisation; R is true.')],
    'features': {'intro': 'A plant\'s flowering behaviour is described:', 'q': 'Identify the type of plant', 'what': 'type',
                 'items': [('a long day plant', ['flowers when the light period exceeds a critical duration', 'flowering induced by long days', 'responds to photoperiod perceived in leaves', 'short nights favour flowering']),
                           ('a short day plant', ['flowers when the light period is below a critical duration', 'flowering induced by short days', 'responds to photoperiod perceived in leaves', 'long uninterrupted dark period needed']),
                           ('a day-neutral plant', ['no correlation between light duration and flowering', 'flowers in any photoperiod', 'not photoperiodically sensitive', 'flowering depends on other factors'])]},
    'qa': [('C4', 'D3', 'case', 'A farmer in Himachal Pradesh sowed a winter variety of wheat in spring by mistake. The crop grew well but did not flower before the end of the season.\n(i) Why did the crop not flower? (1 mark)\n(ii) Name the phenomenon involved. (1 mark)\n(iii) What is its significance, and name one biennial plant that shows it. (2 marks)',
            '(i) Winter varieties need a period of low temperature before flowering. (ii) Vernalisation. (iii) It prevents precocious reproductive development late in the season so the plant matures properly; sugarbeet, cabbage or carrot.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'What is seed dormancy? Give its causes and the methods of overcoming it. Briefly explain photoperiodism.',
            'Dormancy – failure to germinate under favourable external conditions due to internal factors. Causes: hard impermeable seed coat, chemical inhibitors (ABA, phenolics, para-ascorbic acid), immature embryo. Overcoming: scarification, gibberellic acid, nitrates, changing light and temperature. Photoperiodism – response to day/night duration; long day, short day and day-neutral plants; leaves perceive the stimulus; hormonal signal to shoot apex.',
            '3 marks dormancy; 2 marks photoperiodism.')],
    'q3': [('Give three causes of seed dormancy and one method to overcome each.',
            'Hard impermeable seed coat – scarification (mechanical abrasion, shaking); chemical inhibitors such as ABA, phenolics, para-ascorbic acid – gibberellic acid or nitrates; immature embryo – changing light and temperature conditions/after-ripening.',
            '1 mark each.')],
}

# ---------------------------------------------------------------- ch14 breathing

VOL = {'tidal volume (TV)': 500, 'inspiratory reserve volume (IRV)': 3000, 'expiratory reserve volume (ERV)': 1100, 'residual volume (RV)': 1200}


def lung_capacity(r):
    tv = r.choice([450, 500, 550])
    irv = r.choice([2500, 2800, 3000, 3200])
    erv = r.choice([1000, 1100, 1200])
    rv = r.choice([1100, 1200, 1300])
    caps = {'inspiratory capacity (IC)': (tv + irv, 'TV + IRV'), 'expiratory capacity (EC)': (tv + erv, 'TV + ERV'),
            'functional residual capacity (FRC)': (erv + rv, 'ERV + RV'), 'vital capacity (VC)': (erv + tv + irv, 'ERV + TV + IRV'),
            'total lung capacity (TLC)': (rv + erv + tv + irv, 'RV + ERV + TV + IRV')}
    c = r.choice(list(caps))
    good, form = caps[c]
    others = [v for k, (v, _) in caps.items() if v != good]
    wrong = [f'{x} mL' for x in dict.fromkeys(others) if x != good][:3]
    if len(wrong) < 3:
        raise ValueError('few')
    return mcq(f'For a healthy person, TV = {tv} mL, IRV = {irv} mL, ERV = {erv} mL and RV = {rv} mL. What is the {c}?', f'{good} mL', wrong,
               f'{c} = {form} = {good} mL.', r)


def minute_vol(r):
    tv = r.choice([400, 450, 500, 550, 600])
    rate = r.choice([12, 14, 15, 16, 18])
    mv = tv * rate
    return {'stem': f'A person breathes {rate} times a minute with a tidal volume of {tv} mL. How much air does the person inspire or expire per minute and per hour?',
            'answer': f'{mv} mL per minute ({num(mv / 1000, 2)} L); {num(mv * 60 / 1000, 1)} L per hour',
            'key': f'Volume per minute = TV × rate = {tv} × {rate} = {mv} mL (1); per hour = {mv} × 60 = {mv * 60} mL = {num(mv * 60 / 1000, 1)} L (1).',
            'distractors': [f'{tv + rate} mL per minute', f'{mv * 60} mL per minute', f'{mv // 2} mL per minute'], 'marks': 2}


CH14S1 = {
    'topic': 'respiratory organs and the human respiratory system',
    'terms': [('breathing', 'the process of exchange of O₂ from the atmosphere with CO₂ produced by the cells'),
              ('alveoli', 'very thin, irregular-walled, vascularised bag-like structures at the ends of bronchioles where gases are exchanged'),
              ('pleura', 'the double-layered membrane covering the lungs, with pleural fluid between the layers that reduces friction'),
              ('epiglottis', 'a thin elastic cartilaginous flap that prevents the entry of food into the larynx during swallowing'),
              ('larynx', 'a cartilaginous box, the sound box, that helps in sound production'),
              ('conducting part', 'the part of the respiratory system from the external nostrils up to the terminal bronchioles, which transports, cleans and humidifies air'),
              ('respiratory or exchange part', 'the alveoli and their ducts, the site of actual diffusion of O₂ and CO₂ between blood and air')],
    'groups': [('an animal that respires through the body surface', ['sponges', 'coelenterates', 'flatworms', 'earthworms']),
               ('an animal that respires through tracheal tubes', ['insects']), ('an animal that respires through gills', ['fishes', 'prawns', 'many molluscs']),
               ('an animal that respires through lungs', ['reptiles', 'birds', 'mammals'])],
    'tf': (['The trachea divides at the level of the fifth thoracic vertebra into right and left primary bronchi.', 'The trachea, bronchi and initial bronchioles are supported by incomplete cartilaginous rings.',
            'The thoracic chamber is formed dorsally by the vertebral column, ventrally by the sternum, laterally by the ribs and on the lower side by the diaphragm.', 'Frogs can respire through their moist skin.',
            'Earthworms use their moist cuticle for gas exchange.', 'The thoracic chamber is anatomically an air-tight chamber.'],
           [('The trachea is supported by complete cartilaginous rings.', 'It is supported by incomplete (C-shaped) cartilaginous rings.'),
            ('Gas exchange occurs in the trachea and bronchi.', 'Gas exchange occurs in the alveoli; the trachea and bronchi only conduct air.'),
            ('Insects respire through gills.', 'Insects respire through a network of tracheal tubes.'),
            ('The pleura increases friction on the lung surface.', 'Pleural fluid reduces friction on the lung surface.')]),
    'orders': [('path of air through the human respiratory system', ['external nostrils', 'nasal chamber', 'pharynx', 'larynx', 'trachea', 'bronchi', 'bronchioles', 'alveoli'], 'Air passes from nostrils to the alveoli.', '→')],
    'ar': [('Food does not normally enter the larynx during swallowing.', 'The epiglottis covers the glottis during swallowing.', 'a', 'Prevents choking.'),
           ('The conducting part warms and humidifies the inhaled air.', 'Its function is also to clear the air of foreign particles.', 'b', 'Both true; R gives another function.'),
           ('Earthworms can exchange gases through their skin.', 'Earthworms have a moist cuticle.', 'a', 'Gases diffuse through moist surfaces.'),
           ('The thoracic cavity is not air-tight.', 'The lungs are in the thoracic chamber.', 'd', 'The chamber is air-tight, which is needed for breathing; R is true.')],
    'features': {'intro': 'A part of the human respiratory system has these features:', 'q': 'Identify the part', 'what': 'part', 'compare': False,
                 'items': [('the larynx', ['cartilaginous box', 'helps in sound production', 'also called the sound box', 'opening covered by the epiglottis during swallowing']),
                           ('the trachea', ['straight tube extending to the mid-thoracic cavity', 'divides at the fifth thoracic vertebra', 'supported by incomplete cartilaginous rings', 'part of the conducting zone']),
                           ('the alveoli', ['very thin, irregular-walled sacs', 'richly supplied with blood capillaries', 'site of gas exchange', 'form the respiratory part']),
                           ('the pleura', ['double-layered covering of the lungs', 'contains pleural fluid', 'reduces friction on the lung surface', 'outer layer in contact with the thoracic lining'])]},
    'qa': [('C4', 'D3', 'case', 'Aisha choked briefly while laughing and eating at the same time at a family dinner in Jaipur.\n(i) Which structure normally prevents food from entering the windpipe? (1 mark)\n(ii) Why did choking occur? (1 mark)\n(iii) Name the conducting part of the respiratory system and two of its functions. (2 marks)',
            '(i) Epiglottis. (ii) The glottis was open for breathing/laughing when food was swallowed, so food entered the larynx. (iii) External nostrils to terminal bronchioles; transports air to alveoli, clears it of foreign particles, humidifies it and brings it to body temperature.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the human respiratory system with a labelled diagram. List the steps involved in respiration.',
            'External nostrils, nasal chamber, pharynx, larynx (sound box), epiglottis, trachea (incomplete rings), divides at T5 into primary bronchi, secondary and tertiary bronchi, bronchioles, terminal bronchioles, alveoli; lungs covered by double pleura in the air-tight thoracic chamber with diaphragm. Steps: breathing (pulmonary ventilation); diffusion across alveolar membrane; transport by blood; diffusion between blood and tissues; utilisation of O₂ by cells (cellular respiration).',
            '3 marks system; 2 marks steps.')],
    'q3': [('List the five steps of respiration in humans.',
            'Breathing or pulmonary ventilation; diffusion of gases (O₂ and CO₂) across the alveolar membrane; transport of gases by blood; diffusion of O₂ and CO₂ between blood and tissues; utilisation of O₂ by cells for catabolic reactions and release of CO₂.',
            '3 marks for five steps (½ each, with 1 for the correct order).')],
}

CH14S2 = {
    'topic': 'the mechanism of breathing and respiratory volumes',
    'terms': [('inspiration', 'the process by which atmospheric air is drawn into the lungs when intra-pulmonary pressure is less than atmospheric pressure'),
              ('expiration', 'the process by which alveolar air is released out when intra-pulmonary pressure is higher than atmospheric pressure'),
              ('tidal volume', 'the volume of air inspired or expired during a normal respiration, approximately 500 mL'),
              ('inspiratory reserve volume', 'the additional volume of air a person can inspire by a forcible inspiration, averaging 2500–3000 mL'),
              ('expiratory reserve volume', 'the additional volume of air a person can expire by a forcible expiration, averaging 1000–1100 mL'),
              ('residual volume', 'the volume of air remaining in the lungs even after a forcible expiration, averaging 1100–1200 mL'),
              ('vital capacity', 'the maximum volume of air a person can breathe in after a forced expiration, equal to ERV + TV + IRV'),
              ('spirometer', 'an instrument used to estimate the volume of air involved in breathing movements')],
    'groups': [('a respiratory volume', ['tidal volume', 'inspiratory reserve volume', 'expiratory reserve volume', 'residual volume']),
               ('a pulmonary capacity', ['inspiratory capacity', 'expiratory capacity', 'functional residual capacity', 'vital capacity', 'total lung capacity'])],
    'tf': (['Inspiration is initiated by the contraction of the diaphragm, which increases the volume of the thoracic chamber in the antero-posterior axis.', 'Contraction of the external intercostal muscles lifts up the ribs and sternum.',
            'A healthy human breathes 12–16 times per minute.', 'Healthy man can inspire or expire approximately 6000 to 8000 mL of air per minute.',
            'The ability to increase the strength of inspiration and expiration is aided by additional muscles in the abdomen.', 'Residual volume cannot be measured directly with a spirometer.'],
           [('During inspiration the diaphragm relaxes.', 'The diaphragm contracts and flattens during inspiration; it relaxes during expiration.'),
            ('Inspiration occurs when intra-pulmonary pressure is higher than atmospheric pressure.', 'Inspiration occurs when it is lower; expiration when it is higher.'),
            ('Vital capacity includes the residual volume.', 'VC = ERV + TV + IRV; total lung capacity includes RV.'),
            ('Tidal volume is about 3000 mL.', 'Tidal volume is about 500 mL; IRV is 2500–3000 mL.')]),
    'orders': [('sequence of events in inspiration', ['diaphragm and external intercostal muscles contract', 'thoracic volume increases', 'pulmonary volume increases', 'intra-pulmonary pressure falls below atmospheric', 'air rushes into the lungs'], 'Volume up, pressure down, air in.', '→')],
    'ar': [('Air moves into the lungs during inspiration.', 'Intra-pulmonary pressure falls below the atmospheric pressure.', 'a', 'Negative pressure gradient.'),
           ('The lungs can never be completely emptied.', 'Some air, the residual volume, remains even after forcible expiration.', 'a', 'RV ~1100–1200 mL.'),
           ('Vital capacity is higher in athletes.', 'Vital capacity is the maximum volume of air a person can breathe out after a forced inspiration.', 'b', 'Both true; definition does not explain why it is higher in athletes.'),
           ('Contraction of the diaphragm causes expiration.', 'Expiration takes place when intra-pulmonary pressure is higher than atmospheric pressure.', 'd', 'Diaphragm contraction causes inspiration; R is true.')],
    'features': {'intro': 'A phase of breathing has these features:', 'q': 'Identify the phase', 'what': 'phase',
                 'items': [('inspiration', ['diaphragm contracts and flattens', 'external intercostal muscles contract', 'thoracic and pulmonary volumes increase', 'intra-pulmonary pressure falls below atmospheric']),
                           ('expiration', ['diaphragm relaxes and returns to dome shape', 'intercostal muscles relax', 'thoracic and pulmonary volumes decrease', 'intra-pulmonary pressure rises above atmospheric'])]},
    'fams': [F('C3', 'D3', 'mcq', lung_capacity), F('C3', 'D4', 'numerical', minute_vol, marks=2), F('C4', 'D4', 'mcq', lung_capacity)],
    'qa': [('C4', 'D3', 'case', 'At a sports medicine clinic in Pune, a swimmer blew into a spirometer. After a normal breath out, she exhaled forcibly an extra 1200 mL; her normal breath was 550 mL and after a normal breath in she could inhale an additional 3300 mL.\n(i) Name the three volumes measured. (1 mark)\n(ii) Calculate her vital capacity. (2 marks)\n(iii) Why can a spirometer not measure her total lung capacity directly? (1 mark)',
            '(i) ERV = 1200 mL, TV = 550 mL, IRV = 3300 mL. (ii) VC = ERV + TV + IRV = 1200 + 550 + 3300 = 5050 mL. (iii) TLC includes the residual volume, which always remains in the lungs and cannot be exhaled.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'Explain the mechanism of breathing in humans. Define tidal volume, vital capacity and total lung capacity.',
            'Inspiration – diaphragm and external intercostal muscles contract; thoracic volume increases antero-posteriorly and dorso-ventrally; pulmonary volume increases; intra-pulmonary pressure falls; air enters. Expiration – muscles relax; volume decreases; pressure rises; air leaves; abdominal muscles help in forced breathing. TV ~500 mL; VC = ERV + TV + IRV; TLC = RV + ERV + TV + IRV (or VC + RV).',
            '3 marks mechanism; 2 marks definitions.')],
    'q3': [('Define (i) inspiratory capacity, (ii) functional residual capacity and (iii) total lung capacity, giving the formula for each.',
            '(i) IC = TV + IRV – total air a person can inspire after a normal expiration; (ii) FRC = ERV + RV – air remaining in the lungs after a normal expiration; (iii) TLC = RV + ERV + TV + IRV or VC + RV – total air accommodated in the lungs after a forced inspiration.',
            '1 mark each.')],
}

CH14S3 = {
    'topic': 'the exchange and transport of gases and the regulation of respiration',
    'terms': [('partial pressure', 'the pressure contributed by an individual gas in a mixture of gases'),
              ('oxyhaemoglobin', 'the compound formed when oxygen binds reversibly to haemoglobin'),
              ('oxygen dissociation curve', 'the sigmoid curve obtained when percentage saturation of haemoglobin with O₂ is plotted against pO₂'),
              ('carbamino-haemoglobin', 'the compound formed when CO₂ is carried by haemoglobin'),
              ('carbonic anhydrase', 'an enzyme in RBCs that catalyses the reversible formation of carbonic acid from CO₂ and water'),
              ('respiratory rhythm centre', 'a specialised centre in the medulla region of the brain primarily responsible for regulating breathing'),
              ('pneumotaxic centre', 'a centre in the pons region that moderates the functions of the respiratory rhythm centre')],
    'tf': (['About 97 per cent of O₂ is transported by RBCs in the blood and the remaining 3 per cent in a dissolved state through plasma.', 'Nearly 20–25 per cent of CO₂ is transported by RBCs and 70 per cent as bicarbonate.',
            'The solubility of CO₂ is 20–25 times higher than that of O₂.', 'Every 100 mL of oxygenated blood can deliver around 5 mL of O₂ to the tissues under normal physiological conditions.',
            'Every 100 mL of deoxygenated blood delivers approximately 4 mL of CO₂ to the alveoli.', 'The diffusion membrane is made of three major layers: alveolar squamous epithelium, endothelium of capillaries and the basement substance between them.',
            'Oxygen plays an insignificant role in the regulation of respiratory rhythm.'],
           [('pO₂ in the alveoli is lower than in the deoxygenated blood.', 'Alveolar pO₂ (104 mm Hg) is higher than in deoxygenated blood (40 mm Hg), so O₂ diffuses into blood.'),
            ('Most CO₂ is carried as carbamino-haemoglobin.', 'About 70% of CO₂ is carried as bicarbonate; 20–25% as carbamino-haemoglobin.'),
            ('High pCO₂ and high H⁺ favour the formation of oxyhaemoglobin.', 'Low pCO₂, high pO₂, lower H⁺ and lower temperature favour oxyhaemoglobin formation, as in the alveoli.'),
            ('The respiratory rhythm centre is in the pons.', 'It is in the medulla; the pneumotaxic centre is in the pons.'),
            ('O₂ is more soluble than CO₂.', 'CO₂ is 20–25 times more soluble than O₂.')]),
    'ar': [('CO₂ diffuses more readily than O₂ across the diffusion membrane.', 'The solubility of CO₂ is 20–25 times higher than that of O₂.', 'a', 'Higher solubility, more diffusion per unit pressure difference.'),
           ('Oxyhaemoglobin dissociates in the tissues.', 'In the tissues pO₂ is low, pCO₂ is high, H⁺ is high and temperature is higher.', 'a', 'Conditions favour dissociation.'),
           ('The oxygen dissociation curve is sigmoid.', 'Binding of O₂ to haemoglobin depends on the partial pressure of O₂.', 'b', 'Both true; R alone does not explain the sigmoid shape.'),
           ('A chemosensitive area near the rhythm centre is highly sensitive to O₂.', 'Increase in CO₂ and H⁺ activates the chemosensitive area.', 'd', 'It is sensitive to CO₂ and H⁺, not O₂; R is true.')],
    'features': {'intro': 'Conditions at a site in the body are:', 'q': 'Identify the site', 'what': 'site',
                 'items': [('the alveoli', ['high pO₂ (104 mm Hg)', 'low pCO₂ (40 mm Hg)', 'lesser H⁺ concentration and lower temperature', 'oxyhaemoglobin is formed']),
                           ('the tissues', ['low pO₂ (40 mm Hg)', 'high pCO₂ (45 mm Hg)', 'high H⁺ concentration and higher temperature', 'oxyhaemoglobin dissociates'])]},
    'qa': [('C4', 'D3', 'case', 'A mountaineer climbing in Ladakh breathes faster at high altitude. His doctor explains that his blood still carries most oxygen bound to a pigment in RBCs.\n(i) Name the pigment and the compound it forms with O₂. (1 mark)\n(ii) What percentage of O₂ is carried this way? (1 mark)\n(iii) Name the centre that regulates breathing rhythm and the chemical factors that normally stimulate it. (2 marks)',
            '(i) Haemoglobin; oxyhaemoglobin. (ii) About 97%. (iii) Respiratory rhythm centre in the medulla; increase in CO₂ and H⁺ ions sensed by the chemosensitive area (and receptors in aortic arch and carotid artery).',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Explain the transport of O₂ and CO₂ in blood. Describe the factors affecting the binding of O₂ with haemoglobin.',
            'O₂: 97% as oxyhaemoglobin (each Hb binds up to four O₂), 3% dissolved in plasma; dissociation curve sigmoid; alveoli – high pO₂, low pCO₂, low H⁺, lower temperature → binding; tissues – opposite → dissociation; 5 mL O₂ per 100 mL blood. CO₂: 20–25% as carbamino-haemoglobin, 70% as bicarbonate via carbonic anhydrase (CO₂ + H₂O ⇌ H₂CO₃ ⇌ HCO₃⁻ + H⁺), 7% dissolved; 4 mL CO₂ per 100 mL deoxygenated blood released at alveoli.',
            '2 marks O₂; 2 marks CO₂; 1 mark factors.')],
    'q3': [('Explain the role of carbonic anhydrase in the transport of CO₂.',
            'Present in high concentration in RBCs (and in small amounts in plasma). At tissues, high pCO₂: CO₂ + H₂O → H₂CO₃ → HCO₃⁻ + H⁺; bicarbonate carried in plasma. At alveoli, low pCO₂: reaction reverses, releasing CO₂ and H₂O, and CO₂ is exhaled.',
            '1 mark location; 1 mark tissues; 1 mark alveoli.')],
}

CH14S4 = {
    'topic': 'disorders of the respiratory system',
    'terms': [('asthma', 'difficulty in breathing causing wheezing due to inflammation of bronchi and bronchioles'),
              ('emphysema', 'a chronic disorder in which alveolar walls are damaged, decreasing the respiratory surface'),
              ('occupational respiratory disorders', 'diseases such as silicosis and asbestosis caused by long exposure to dust at work'),
              ('fibrosis', 'proliferation of fibrous tissue that causes serious lung damage after long exposure to dust')],
    'tf': (['Cigarette smoking is one of the major causes of emphysema.', 'Asthma causes wheezing due to inflammation of the bronchi and bronchioles.',
            'Workers in stone-breaking or grinding industries should wear protective masks.', 'Long exposure to dust can give rise to inflammation leading to fibrosis.'],
           [('Emphysema increases the respiratory surface.', 'Damage to alveolar walls decreases the respiratory surface.'),
            ('Silicosis is caused by a virus.', 'Silicosis is an occupational disorder caused by long exposure to silica dust.'),
            ('Asthma is caused by damage to alveolar walls.', 'Asthma is due to inflammation of the bronchi and bronchioles; emphysema damages alveolar walls.'),
            ('Dust in industries does not affect the respiratory system.', 'Long exposure to dust can cause inflammation and fibrosis of the lungs.')]),
    'ar': [('Smokers are at a higher risk of emphysema.', 'Cigarette smoking is one of the major causes of emphysema.', 'a', 'Smoke damages alveolar walls.'),
           ('Workers in stone-grinding units wear protective masks.', 'Long exposure to dust causes inflammation leading to fibrosis.', 'a', 'Masks prevent dust inhalation.'),
           ('Emphysema increases the efficiency of gas exchange.', 'In emphysema alveolar walls are damaged.', 'd', 'It reduces gas exchange surface; R is true.')],
    'features': {'intro': 'A respiratory disorder shows these features:', 'q': 'Identify the disorder', 'what': 'disorder',
                 'items': [('asthma', ['difficulty in breathing', 'wheezing', 'inflammation of bronchi and bronchioles', 'may be triggered by allergens']),
                           ('emphysema', ['chronic disorder', 'alveolar walls damaged', 'respiratory surface decreased', 'cigarette smoking is a major cause']),
                           ('occupational respiratory disorders', ['caused by dust at the workplace', 'e.g. silicosis and asbestosis', 'inflammation leading to fibrosis', 'prevented by protective masks'])]},
    'qa': [('C4', 'D3', 'case', 'Ramesh, who has worked for 20 years in a stone-crushing unit near Jodhpur without a mask, now has a persistent cough and breathlessness. His X-ray shows scarring of the lungs.\n(i) Name the likely disorder. (1 mark)\n(ii) What type of disorder is it? (1 mark)\n(iii) Explain how it damages the lungs and suggest two preventive measures. (2 marks)',
            '(i) Silicosis. (ii) Occupational respiratory disorder. (iii) Long exposure to silica dust causes inflammation leading to fibrosis (proliferation of fibrous tissue), reducing lung function; wear protective masks, use dust control/wet methods, regular health check-ups.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Describe asthma, emphysema and occupational respiratory disorders. Suggest measures to prevent them.',
            'Asthma – wheezing and breathing difficulty due to inflammation of bronchi and bronchioles; avoid allergens. Emphysema – chronic; alveolar walls damaged, respiratory surface decreased; smoking a major cause; avoid smoking. Occupational – silicosis, asbestosis from long exposure to dust in grinding or stone-breaking industries; inflammation, fibrosis; protective masks, dust control.',
            '1½ marks each disorder; ½ mark prevention.')],
    'q3': [('Distinguish between asthma and emphysema on three points.',
            'Asthma – inflammation of bronchi and bronchioles; wheezing; often allergic and episodic. Emphysema – damage to alveolar walls; reduced respiratory surface; chronic, smoking a major cause.',
            '1 mark each.')],
}

# ---------------------------------------------------------------- ch15 body fluids

def cardiac_output(r):
    sv = r.choice([60, 65, 70, 75, 80])
    hr = r.choice([60, 70, 72, 75, 80, 90])
    co = sv * hr
    what = r.choice(['co', 'sv', 'hr'])
    if what == 'co':
        stem = f'A person has a stroke volume of {sv} mL and a heart rate of {hr} beats per minute. What is the cardiac output?'
        good = f'{num(co / 1000, 3)} L per minute'
        wrong = [f'{num(x, 3)} L per minute' for x in (co / 100, (sv + hr) / 1000 * 10, co / 2000)]
        key = f'Cardiac output = stroke volume × heart rate = {sv} × {hr} = {co} mL ≈ {num(co / 1000, 3)} L per minute.'
    elif what == 'sv':
        stem = f'The cardiac output of a person is {co} mL per minute and the heart rate is {hr} beats per minute. What is the stroke volume?'
        good = f'{sv} mL'
        wrong = [f'{x} mL' for x in dict.fromkeys([sv * 2, sv + 10, round(co / 60), hr]) if x != sv][:3]
        key = f'Stroke volume = cardiac output / heart rate = {co}/{hr} = {sv} mL.'
    else:
        stem = f'A person has a cardiac output of {co} mL per minute and a stroke volume of {sv} mL. What is the heart rate?'
        good = f'{hr} beats per minute'
        wrong = [f'{x} beats per minute' for x in dict.fromkeys([hr + 12, hr - 10, 2 * hr, sv]) if x != hr][:3]
        key = f'Heart rate = cardiac output / stroke volume = {co}/{sv} = {hr} beats per minute.'
    if len(set(wrong)) < 3 or good in wrong:
        raise ValueError('few')
    return mcq(stem, good, wrong, key, r)


BLOOD = {  # group: (antigens, antibodies in plasma, can donate to, can receive from)
    'A': ('A', 'anti-B', ['A', 'AB'], ['A', 'O']),
    'B': ('B', 'anti-A', ['B', 'AB'], ['B', 'O']),
    'AB': ('A and B', 'none', ['AB'], ['A', 'B', 'AB', 'O']),
    'O': ('none', 'anti-A and anti-B', ['A', 'B', 'AB', 'O'], ['O']),
}


def blood_group(r):
    g = r.choice(list(BLOOD))
    ag, ab, to, frm = BLOOD[g]
    t = r.randrange(3)
    if t == 0:
        wrong = [BLOOD[x][0] for x in BLOOD if x != g]
        return mcq(f'Which antigens are present on the RBCs of a person with blood group {g}?', ag, wrong,
                   f'Group {g}: antigen(s) {ag} on the RBC surface; antibodies {ab} in plasma.', r)
    if t == 1:
        good = ab
        wrong = [BLOOD[x][1] for x in BLOOD if BLOOD[x][1] != ab]
        return mcq(f'Which antibodies are present in the plasma of a person with blood group {g}?', good, wrong[:3],
                   f'Group {g}: antigens {ag} on RBCs; antibodies {ab} in plasma.', r)
    good = ', '.join(frm)
    wrong = [', '.join(BLOOD[x][3]) for x in BLOOD if x != g]
    return mcq(f'A person of blood group {g} can safely receive blood from donors of group(s):', good, wrong[:3],
               f'Group {g} has {ab} antibodies; it can receive from {good}.', r)


CH15S1 = {
    'topic': 'blood, blood groups, coagulation and lymph',
    'terms': [('plasma', 'the straw-coloured, viscous fluid part of blood that constitutes nearly 55 per cent of blood'),
              ('formed elements', 'erythrocytes, leucocytes and platelets, which constitute nearly 45 per cent of blood'),
              ('erythroblastosis foetalis', 'a condition in which anti-Rh antibodies from an Rh⁻ mother destroy the RBCs of her Rh⁺ foetus in a later pregnancy'),
              ('universal donor', 'a person with blood group O, who can donate blood to persons of any ABO group'),
              ('universal recipient', 'a person with blood group AB, who can accept blood from persons of any ABO group'),
              ('lymph', 'a colourless fluid formed from interstitial fluid that contains specialised lymphocytes and transports fats absorbed through lacteals'),
              ('serum', 'plasma without the clotting factors'),
              ('thrombokinase', 'an enzyme complex formed by a cascade of reactions that converts prothrombin into thrombin')],
    'groups': [('a granulocyte', ['neutrophils', 'eosinophils', 'basophils']), ('an agranulocyte', ['lymphocytes', 'monocytes'])],
    'groups2': [('a plasma protein', ['fibrinogen', 'globulins', 'albumins']), ('a formed element', ['erythrocytes', 'leucocytes', 'platelets'])],
    'tf': (['A healthy adult has 5 to 5.5 million RBCs per mm³ of blood.', 'RBCs have an average life span of 120 days, after which they are destroyed in the spleen.',
            'Neutrophils are the most abundant WBCs (60–65 per cent).', 'Basophils are the least abundant WBCs (0.5–1 per cent) and secrete histamine, serotonin and heparin.',
            'Platelets are cell fragments produced from megakaryocytes.', 'Calcium ions play a very important role in clotting.', 'About 80 per cent of humans are Rh positive.'],
           [('Mature mammalian RBCs have a nucleus.', 'Mature RBCs of most mammals are devoid of a nucleus and are biconcave.'),
            ('Lymphocytes are the most abundant WBCs.', 'Neutrophils are the most abundant; lymphocytes form 20–25 per cent.'),
            ('Blood group O has both A and B antigens.', 'Group O has no A or B antigen; AB has both.'),
            ('Rh incompatibility affects the first pregnancy severely.', 'The first foetus is usually safe; antibodies formed after delivery affect later Rh⁺ pregnancies.'),
            ('Albumins are involved in clotting.', 'Fibrinogens are involved in clotting; albumins help in osmotic balance and globulins in defence.')]),
    'ar': [('Persons with blood group O are called universal donors.', 'Their RBCs have no A or B antigens.', 'a', 'No antigen for recipient antibodies to react with.'),
           ('An Rh⁻ mother carrying an Rh⁺ foetus needs anti-Rh antibodies after the first delivery.', 'Anti-Rh antibodies prevent sensitisation of the mother to Rh antigens of the foetus.', 'a', 'Prevents erythroblastosis foetalis in later pregnancies.'),
           ('Blood does not clot inside healthy blood vessels.', 'Clotting is triggered by injury that activates platelets and factors in the plasma.', 'a', 'No injury, no cascade.'),
           ('Blood group AB is the universal donor.', 'Blood group AB has no anti-A or anti-B antibodies.', 'd', 'AB is the universal recipient; R is true.')],
    'features': {'intro': 'A white blood cell has these features:', 'q': 'Identify the cell', 'what': 'cell',
                 'items': [('neutrophils', ['most abundant WBCs (60–65%)', 'phagocytic', 'destroy foreign organisms', 'granulocytes']),
                           ('eosinophils', ['2–3 per cent of WBCs', 'resist infections', 'associated with allergic reactions', 'granulocytes']),
                           ('basophils', ['least abundant WBCs (0.5–1%)', 'secrete histamine, serotonin and heparin', 'involved in inflammatory reactions', 'granulocytes']),
                           ('lymphocytes', ['20–25 per cent of WBCs', 'B and T forms', 'responsible for immune responses', 'agranulocytes']),
                           ('monocytes', ['6–8 per cent of WBCs', 'phagocytic', 'agranulocytes', 'largest WBCs'])]},
    'fams': [F('C3', 'D3', 'mcq', blood_group), F('C4', 'D4', 'mcq', blood_group)],
    'qa': [('C4', 'D3', 'case', 'Priya (Rh⁻) is expecting her second child; her first child was Rh⁺. Her doctor in Indore had given her an injection soon after the first delivery.\n(i) What condition was the injection meant to prevent? (1 mark)\n(ii) What did the injection contain? (1 mark)\n(iii) Explain why the first child was not affected but the second could be. (2 marks)',
            '(i) Erythroblastosis foetalis. (ii) Anti-Rh antibodies. (iii) During the first pregnancy the bloods are separated by the placenta, but during delivery some foetal Rh⁺ blood enters the mother, who makes anti-Rh antibodies; in later pregnancies these cross the placenta and destroy the RBCs of an Rh⁺ foetus.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the composition of blood. Explain the ABO blood groups and the mechanism of blood coagulation.',
            'Plasma (55%) – 90–92% water, proteins 6–8% (fibrinogen, globulins, albumins), minerals, glucose, amino acids, clotting factors. Formed elements (45%) – RBCs (5–5.5 million/mm³, haemoglobin 12–16 g/100 mL, 120 days), WBCs (6000–8000/mm³: neutrophils, eosinophils, basophils, lymphocytes, monocytes), platelets (1.5–3.5 lakh/mm³). ABO – A, B antigens; antibodies; O universal donor, AB universal recipient. Clotting – injury activates platelets/tissue factors → thrombokinase → prothrombin → thrombin → fibrinogen → fibrin threads trap formed elements; Ca²⁺ needed.',
            '2 marks composition; 1½ ABO; 1½ clotting.')],
    'q3': [('Explain the cascade of blood coagulation.',
            'Injury stimulates platelets to release factors and activates factors in plasma; an enzyme complex thrombokinase is formed; it converts inactive prothrombin into thrombin; thrombin converts fibrinogen into fibrin, whose threads trap dead and damaged formed elements to form a clot; calcium ions are essential.',
            '1 mark each step.'),
           ('Distinguish between blood and lymph on three points.',
            'Blood – red, has RBCs, platelets and plasma proteins including fibrinogen; flows in blood vessels; transports O₂. Lymph – colourless, no RBCs, fewer proteins, has specialised lymphocytes; flows in lymphatic vessels; carries nutrients and hormones and absorbs fats through lacteals.',
            '1 mark each.')],
}

CH15S2 = {
    'topic': 'the human heart, cardiac cycle and ECG',
    'terms': [('sino-atrial node (SAN)', 'a patch of nodal tissue in the right upper corner of the right atrium that generates the maximum number of action potentials and acts as the pacemaker'),
              ('atrio-ventricular node (AVN)', 'nodal tissue in the lower left corner of the right atrium close to the atrio-ventricular septum'),
              ('bundle of His', 'the atrio-ventricular bundle from the AVN that passes through the inter-ventricular septum and divides into right and left bundles'),
              ('cardiac cycle', 'the sequential events in the heart that are cyclically repeated, consisting of systole and diastole of both atria and ventricles'),
              ('stroke volume', 'the volume of blood pumped out by each ventricle during a cardiac cycle, approximately 70 mL'),
              ('cardiac output', 'the volume of blood pumped out by each ventricle per minute, averaging 5000 mL in a healthy person'),
              ('electrocardiograph (ECG)', 'a graphical representation of the electrical activity of the heart during a cardiac cycle'),
              ('tricuspid valve', 'the valve with three muscular flaps that guards the opening between the right atrium and the right ventricle')],
    'groups': [('a part of the conducting (nodal) system of the heart', ['SA node', 'AV node', 'bundle of His', 'Purkinje fibres']),
               ('a valve of the human heart', ['tricuspid valve', 'bicuspid (mitral) valve', 'semilunar valves'])],
    'tf': (['The heart is mesodermally derived and is situated in the thoracic cavity between the two lungs, slightly tilted to the left.', 'The heart is protected by a double-walled membranous bag, the pericardium.',
            'The SAN can generate about 70–75 action potentials per minute.', 'The P-wave represents the excitation (depolarisation) of the atria.',
            'The QRS complex represents the depolarisation of the ventricles.', 'The T-wave represents the return of the ventricles from the excited to the normal state (repolarisation).', 'The first heart sound "lub" is due to closure of the tricuspid and bicuspid valves.'],
           [('The AV node is the pacemaker of the heart.', 'The SA node is the pacemaker as it generates the maximum number of action potentials.'),
            ('The P-wave represents ventricular depolarisation.', 'The P-wave represents atrial depolarisation; QRS represents ventricular depolarisation.'),
            ('The second heart sound is due to closure of the AV valves.', 'The second sound "dub" is due to closure of the semilunar valves.'),
            ('The duration of a cardiac cycle is 0.6 s.', 'With 72 beats per minute, the cardiac cycle lasts about 0.8 s.'),
            ('The bicuspid valve guards the opening between the right atrium and right ventricle.', 'The tricuspid valve guards it; the bicuspid (mitral) valve is on the left side.')]),
    'orders': [('path of the cardiac impulse', ['SA node', 'atrial musculature', 'AV node', 'bundle of His', 'bundle branches', 'Purkinje fibres', 'ventricular musculature'], 'The impulse from SAN spreads through atria to AVN and then through the bundle of His to ventricles.', '→'),
               ('sequence of events in a cardiac cycle starting from joint diastole', ['joint diastole', 'atrial systole', 'ventricular systole', 'ventricular diastole'], 'All chambers relax, atria contract, ventricles contract, then relax.', '→')],
    'ar': [('The SAN is called the pacemaker.', 'It generates the maximum number of action potentials and initiates and maintains the rhythmic contractile activity of the heart.', 'a', 'It sets the pace.'),
           ('Heart beat rate can be determined by counting QRS complexes.', 'Each QRS complex corresponds to ventricular depolarisation in one beat.', 'a', 'One QRS per beat.'),
           ('Blood flows only in one direction in the heart.', 'The valves allow flow only in one direction.', 'a', 'Valves prevent backflow.'),
           ('Human heart is ectodermal in origin.', 'The human heart is situated in the thoracic cavity.', 'd', 'The heart is mesodermal; R is true.')],
    'features': {'intro': 'A wave or part of a standard ECG is described:', 'q': 'Identify it', 'what': 'wave', 'compare': False, 'long': False,
                 'items': [('the P-wave', ['electrical excitation of the atria', 'atrial depolarisation', 'leads to contraction of both atria', 'first wave of the ECG']),
                           ('the QRS complex', ['depolarisation of the ventricles', 'initiates ventricular contraction', 'counted to determine heart rate', 'begins after the P-wave']),
                           ('the T-wave', ['return of ventricles from excited to normal state', 'ventricular repolarisation', 'end of the T-wave marks the end of systole', 'last wave of the cycle'])]},
    'fams': [F('C3', 'D3', 'mcq', cardiac_output), F('C4', 'D4', 'mcq', cardiac_output)],
    'qa': [('C4', 'D3', 'case', 'The ECG of a 60-year-old patient at a hospital in Mumbai showed abnormal QRS complexes and an irregular gap between successive waves.\n(i) What does the QRS complex represent? (1 mark)\n(ii) How can the heart rate be found from the ECG? (1 mark)\n(iii) Explain why ECG is of clinical significance. (2 marks)',
            '(i) Depolarisation of the ventricles. (ii) By counting the number of QRS complexes in a given time period. (iii) Any deviation in the shape of the ECG indicates a possible abnormality or disease, so it is of great clinical significance in diagnosing heart conditions.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',)),
           ('C4', 'D5', 'long', 'Describe the events of the cardiac cycle. Explain the role of the nodal tissue.',
            'Joint diastole – all chambers relaxed, AV valves open, blood flows into ventricles (about 70%); atrial systole – increases flow by about 30%; ventricular systole – AV valves close (lub), semilunar valves open, blood into pulmonary artery and aorta; ventricular diastole – semilunar valves close (dub), pressure falls, AV valves open. 0.8 s; stroke volume ~70 mL; cardiac output ~5 L. Nodal tissue: SAN pacemaker 70–75 action potentials/min → atria → AVN → bundle of His → bundle branches → Purkinje fibres → ventricles.',
            '3 marks cycle; 2 marks nodal tissue.')],
    'q3': [('Explain the heart sounds and the events responsible for them.',
            'Two prominent sounds are heard with a stethoscope during each cycle. "Lub" – first sound, due to closure of the tricuspid and bicuspid valves at the start of ventricular systole. "Dub" – second sound, due to closure of the semilunar valves at the start of ventricular diastole.',
            '1 mark each sound; 1 mark clinical significance or timing.')],
}

CH15S3 = {
    'topic': 'double circulation and the regulation of cardiac activity',
    'terms': [('double circulation', 'the passage of blood twice through the heart in one complete cycle, through pulmonary and systemic circulations'),
              ('pulmonary circulation', 'the pathway of blood from the right ventricle to the lungs and back to the left atrium'),
              ('systemic circulation', 'the pathway of blood from the left ventricle to the body tissues and back to the right atrium'),
              ('hepatic portal system', 'a unique vascular connection in which the hepatic portal vein carries blood from the intestine to the liver before it reaches the systemic circulation'),
              ('coronary system', 'the exclusive system of blood vessels supplying the cardiac musculature'),
              ('auto-excitable heart (myogenic)', 'a heart whose activities are regulated intrinsically by specialised muscles (nodal tissue)')],
    'groups': [('a vessel carrying oxygenated blood', ['pulmonary vein', 'aorta']), ('a vessel carrying deoxygenated blood', ['pulmonary artery', 'superior vena cava', 'inferior vena cava'])],
    'tf': (['The pulmonary artery carries deoxygenated blood to the lungs.', 'The pulmonary veins carry oxygenated blood from the lungs to the left atrium.',
            'Neural signals through the sympathetic nerves can increase the rate of heart beat.', 'Parasympathetic neural signals decrease the rate of heart beat and the speed of conduction.',
            'Adrenal medullary hormones can increase cardiac output.', 'Fishes have a two-chambered heart with one atrium and one ventricle.'],
           [('The pulmonary artery carries oxygenated blood.', 'The pulmonary artery carries deoxygenated blood from the right ventricle to the lungs.'),
            ('Parasympathetic signals increase the heart rate.', 'Sympathetic signals increase it; parasympathetic signals decrease it.'),
            ('The human heart is neurogenic.', 'The human heart is myogenic (auto-excitable); its rhythm is initiated by the SAN.'),
            ('Amphibians and reptiles (except crocodiles) have a four-chambered heart.', 'They have a three-chambered heart; crocodiles, birds and mammals have four chambers.'),
            ('In fishes, the heart pumps oxygenated blood.', 'Fishes have a single circulation; the heart pumps deoxygenated blood to the gills.')]),
    'ar': [('Birds and mammals show double circulation.', 'Oxygenated and deoxygenated blood are completely separated in their four-chambered heart.', 'a', 'Separate pulmonary and systemic circuits.'),
           ('The heart is called myogenic.', 'Its normal activities are regulated intrinsically by specialised muscles (nodal tissue).', 'a', 'Auto-excitable.'),
           ('Amphibians show incomplete double circulation.', 'The single ventricle of amphibians receives both oxygenated and deoxygenated blood.', 'a', 'Mixed blood.'),
           ('The pulmonary vein carries deoxygenated blood.', 'Veins carry blood towards the heart.', 'd', 'The pulmonary vein carries oxygenated blood; R is true.')],
    'features': {'intro': 'An animal group has this type of heart and circulation:', 'q': 'Identify the group', 'what': 'group',
                 'items': [('fishes', ['two-chambered heart', 'one atrium and one ventricle', 'single circulation', 'heart pumps deoxygenated blood to gills']),
                           ('amphibians and most reptiles', ['three-chambered heart', 'two atria and a single ventricle', 'incomplete double circulation', 'mixed blood in the ventricle']),
                           ('crocodiles, birds and mammals', ['four-chambered heart', 'two atria and two ventricles', 'complete double circulation', 'oxygenated and deoxygenated blood fully separated'])]},
    'orders': [('path of blood in pulmonary circulation', ['right atrium', 'right ventricle', 'pulmonary artery', 'lungs', 'pulmonary veins', 'left atrium'], 'Deoxygenated blood goes to the lungs and returns oxygenated.', '→'),
               ('path of blood in systemic circulation', ['left ventricle', 'aorta', 'arteries and capillaries of tissues', 'veins', 'vena cava', 'right atrium'], 'Oxygenated blood goes to the body and returns deoxygenated.', '→')],
    'qa': [('C4', 'D3', 'case', 'Varun, a medical student, traced a red blood cell starting from the left ventricle until it returned to the left ventricle.\n(i) How many times does it pass through the heart? (1 mark)\n(ii) Name the two circulations it goes through. (1 mark)\n(iii) Name the vessel by which it leaves the heart to reach the lungs, and state the nature of blood in it. (2 marks)',
            '(i) Twice. (ii) Systemic and pulmonary circulation. (iii) Pulmonary artery from the right ventricle; it carries deoxygenated blood.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Explain double circulation in humans. How is cardiac activity regulated?',
            'Pulmonary – right ventricle → pulmonary artery → lungs → pulmonary veins → left atrium; systemic – left ventricle → aorta → arteries → capillaries → veins → vena cava → right atrium; hepatic portal system; coronary system. Regulation: myogenic – SAN; ANS centre in the medulla oblongata; sympathetic increases rate, strength and cardiac output; parasympathetic decreases rate and conduction; adrenal medullary hormones increase output.',
            '3 marks circulation; 2 marks regulation.')],
    'q3': [('How is the activity of the heart regulated by the nervous and endocrine systems?',
            'The heart is myogenic (SAN), but a special neural centre in the medulla oblongata can moderate it through the ANS; sympathetic nerves increase rate, strength of ventricular contraction and cardiac output; parasympathetic nerves decrease the rate and conduction speed; adrenal medullary hormones increase cardiac output.',
            '1 mark each.')],
}

CH15S4 = {
    'topic': 'disorders of the circulatory system',
    'terms': [('hypertension', 'blood pressure higher than normal (120/80 mm Hg); measurements of 140/90 mm Hg or higher indicate it'),
              ('coronary artery disease (CAD)', 'a disorder, often called atherosclerosis, in which the vessels supplying the heart muscle are narrowed by deposits of calcium, fat, cholesterol and fibrous tissues'),
              ('angina pectoris', 'acute chest pain that appears when not enough oxygen reaches the heart muscle'),
              ('heart failure', 'the state of the heart when it is not pumping blood effectively enough to meet the needs of the body, also called congestive heart failure'),
              ('cardiac arrest', 'the condition in which the heart stops beating')],
    'tf': (['Normal blood pressure is 120/80 mm Hg.', 'High blood pressure leads to heart diseases and affects vital organs like the brain and kidney.',
            'Angina can occur in men and women of any age but is more common among the middle-aged and elderly.', 'Heart failure is not the same as cardiac arrest or heart attack.',
            'In CAD, deposits of calcium, fat, cholesterol and fibrous tissue narrow the lumen of arteries.'],
           [('A blood pressure of 110/70 mm Hg indicates hypertension.', 'Hypertension is indicated by 140/90 mm Hg or higher repeatedly; 110/70 is in the normal range.'),
            ('Heart failure is the same as cardiac arrest.', 'In heart failure the heart pumps inefficiently; in cardiac arrest it stops beating.'),
            ('Angina pectoris occurs when excess oxygen reaches the heart muscle.', 'Angina occurs when not enough oxygen reaches the heart muscle.'),
            ('In a reading of 120/80 mm Hg, 80 is the systolic pressure.', '120 is the systolic (pumping) and 80 the diastolic (resting) pressure.')]),
    'groups': [('a disorder of the circulatory system', ['hypertension', 'coronary artery disease', 'angina pectoris', 'heart failure']),
               ('a disorder of the respiratory system', ['asthma', 'emphysema', 'silicosis'])],
    'ar': [('Congestion of the lungs is a main symptom of heart failure.', 'Heart failure is also called congestive heart failure.', 'b', 'Both true; R is a name.'),
           ('Coronary artery disease reduces blood supply to the heart muscle.', 'Deposits of fat, cholesterol, calcium and fibrous tissue narrow the coronary arteries.', 'a', 'Narrowed lumen.'),
           ('Hypertension can damage the kidneys and brain.', 'Persistent high blood pressure affects vital organs.', 'a', 'NCERT.'),
           ('Angina pectoris is caused by excess oxygen to the heart muscle.', 'Angina is acute chest pain.', 'd', 'It is due to too little oxygen; R is true.')],
    'features': {'intro': 'A circulatory disorder is described:', 'q': 'Identify the disorder', 'what': 'disorder', 'compare': False,
                 'items': [('hypertension', ['blood pressure repeatedly 140/90 mm Hg or higher', 'leads to heart diseases', 'affects brain and kidney', 'a lifestyle-related disorder']),
                           ('coronary artery disease', ['also called atherosclerosis', 'affects vessels supplying the heart muscle', 'deposits of calcium, fat, cholesterol and fibrous tissue', 'lumen of arteries narrows']),
                           ('angina pectoris', ['acute chest pain', 'not enough oxygen reaches the heart muscle', 'more common in middle-aged and elderly', 'due to conditions affecting blood flow']),
                           ('heart failure', ['heart not pumping blood effectively', 'congestion of the lungs is a main symptom', 'also called congestive heart failure', 'not the same as cardiac arrest'])]},
    'qa': [('C4', 'D3', 'case', 'Mr Sharma, aged 55, from Lucknow, gets chest pain when climbing stairs that disappears with rest. His blood pressure readings are repeatedly 150/95 mm Hg.\n(i) Name the condition indicated by the chest pain. (1 mark)\n(ii) Is his blood pressure normal? Explain. (1 mark)\n(iii) Explain the likely cause of his chest pain and suggest two lifestyle changes. (2 marks)',
            '(i) Angina pectoris. (ii) No – he has hypertension (140/90 or higher repeatedly; normal is 120/80). (iii) Narrowing of coronary arteries by deposits (CAD) reduces oxygen supply to the heart muscle during exertion; regular exercise, low-fat diet, no smoking, reducing salt and stress.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',)),
           ('C4', 'D5', 'long', 'Describe hypertension, coronary artery disease, angina and heart failure.',
            'Hypertension – BP higher than normal 120/80; 140/90 or higher repeatedly; affects heart, brain and kidney. CAD (atherosclerosis) – deposits of calcium, fat, cholesterol, fibrous tissue narrow coronary arteries. Angina – acute chest pain when not enough O₂ reaches heart muscle; common in middle-aged and elderly. Heart failure – heart not pumping effectively; congestion of lungs; not the same as cardiac arrest or heart attack.',
            '1¼ marks each.')],
    'q3': [('Distinguish between heart failure, cardiac arrest and heart attack.',
            'Heart failure – the heart is not pumping blood effectively enough to meet body needs (congestive); cardiac arrest – the heart stops beating; heart attack – the heart muscle is suddenly damaged by an inadequate blood supply.',
            '1 mark each.')],
}

SPECS = {'ch11-st1': CH11S1, 'ch11-st2': CH11S2, 'ch11-st3': CH11S3, 'ch11-st4': CH11S4,
         'ch12-st1': CH12S1, 'ch12-st2': CH12S2, 'ch12-st3': CH12S3,
         'ch13-st1': CH13S1, 'ch13-st2': CH13S2, 'ch13-st3': CH13S3,
         'ch14-st1': CH14S1, 'ch14-st2': CH14S2, 'ch14-st3': CH14S3, 'ch14-st4': CH14S4,
         'ch15-st1': CH15S1, 'ch15-st2': CH15S2, 'ch15-st3': CH15S3, 'ch15-st4': CH15S4}
