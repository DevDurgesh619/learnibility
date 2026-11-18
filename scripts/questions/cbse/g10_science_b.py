"""CBSE class 10 science families, chapters 5-8 (Life Processes; Control and Coordination; How do
Organisms Reproduce?; Heredity)."""
from __future__ import annotations

from qbank import name, num
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, cap, sig

S = 'cbse-g10-science-ch'


def _order(r, seq, what):
    k = r.randint(4, min(6, len(seq)))
    st = r.randint(0, len(seq) - k)
    s = seq[st:st + k]
    sh = s[:]
    while sh == s:
        r.shuffle(sh)
    L = '; '.join(f'({i + 1}) {x}' for i, x in enumerate(sh))
    return {'stem': f'Arrange these steps of {what} in the correct order: {L}.', 'answer': ', '.join(str(sh.index(x) + 1) for x in s),
            'key': 'Correct order: ' + ' → '.join(s) + '.'}


# ======================= ch05 Life Processes
c5s1_defs = [
    ('nutrition', 'the process of taking in food and using it for energy, growth and repair'),
    ('autotrophic nutrition', 'nutrition in which an organism makes its own food from simple inorganic substances such as carbon dioxide and water'),
    ('heterotrophic nutrition', 'nutrition in which an organism takes in complex food made by other organisms'),
    ('photosynthesis', 'the process by which green plants make carbohydrates from carbon dioxide and water using sunlight and chlorophyll'),
    ('stomata', 'tiny pores on the surface of leaves through which gases are exchanged'),
    ('peristalsis', 'the rhythmic contraction of the muscles of the alimentary canal that pushes food forward'),
    ('emulsification', 'the breaking of large fat globules into smaller ones by bile salts'),
    ('villi', 'finger-like projections of the inner lining of the small intestine that increase the surface area for absorption'),
    ('holozoic nutrition', 'nutrition in which the organism takes in whole food and breaks it down inside the body'),
    ('parasitic nutrition', 'nutrition in which an organism obtains food from another living organism (the host) without killing it'),
]
c5s1_mode = {
    'autotrophic': ['green plants', 'blue-green algae', 'grass'],
    'saprotrophic': ['bread mould', 'mushroom', 'yeast'],
    'parasitic': ['Cuscuta (amar-bel)', 'ticks', 'lice', 'tapeworm', 'leeches'],
    'holozoic': ['Amoeba', 'humans', 'dogs', 'cows'],
}
c5s1_mode = {f'{k} nutrition': v for k, v in c5s1_mode.items()}
c5s1_enz = {
    'salivary amylase': ['converts starch into sugar (maltose) in the mouth'],
    'pepsin': ['digests proteins in the stomach in an acidic medium'],
    'trypsin': ['digests proteins in the small intestine (from pancreatic juice)'],
    'lipase': ['breaks down emulsified fats into fatty acids and glycerol'],
    'hydrochloric acid in gastric juice': ['makes the medium acidic for pepsin and kills germs'],
    'bile from the liver': ['makes the food alkaline and emulsifies fats'],
    'mucus in the stomach': ['protects the inner lining of the stomach from acid'],
}
c5s1_enz = {f'the role of {k}': v for k, v in c5s1_enz.items()}
c5s1_mc = [
    ('The raw materials for photosynthesis are:', 'carbon dioxide and water', 'oxygen and water', 'glucose and oxygen', 'starch and water'),
    ('Which event does NOT occur during photosynthesis?', 'oxidation of glucose to release energy', 'absorption of light energy by chlorophyll', 'splitting of water into hydrogen and oxygen', 'reduction of carbon dioxide to carbohydrates'),
    ('Desert plants take up carbon dioxide at night and store it as:', 'an intermediate acid, used in the day', 'starch', 'glucose', 'oxygen'),
    ('Opening and closing of stomata is controlled by:', 'guard cells', 'xylem', 'phloem', 'root hairs'),
    ('Starch is first digested in the:', 'mouth', 'stomach', 'large intestine', 'oesophagus'),
    ('Bile is produced by the:', 'liver', 'pancreas', 'gall bladder', 'stomach'),
    ('The exit of faeces is regulated by the:', 'anal sphincter', 'oesophagus', 'gall bladder', 'villi'),
    ('Amoeba takes in food using:', 'pseudopodia, forming a food vacuole', 'cilia', 'a mouth', 'stomata'),
    ('Iodine solution turns blue-black with:', 'starch', 'glucose', 'protein', 'fat'),
]
c5s1_why = [
    ('Why is the small intestine long and coiled in herbivores like cows?', 'Cellulose in grass takes a long time to digest, so a longer small intestine gives more time and area.', '1 mark cellulose. 1 mark more time.'),
    ('Why are villi important in the small intestine?', 'They increase the surface area for absorption and are richly supplied with blood vessels that carry the absorbed food.', '1 mark area. 1 mark blood vessels.'),
    ('How do guard cells open the stomata?', 'Water flows into the guard cells, they swell and the pore opens; when they lose water they shrink and the pore closes.', '1 mark swell. 1 mark shrink.'),
    ('Why is the destarched plant used in the experiment to show that chlorophyll is needed for photosynthesis?', 'Keeping the plant in the dark removes the existing starch, so any starch found later must have been made during the experiment.', '2 marks.'),
    ('Why does the stomach secrete mucus?', 'Mucus protects the inner lining of the stomach from hydrochloric acid, which would otherwise damage it.', '2 marks.'),
]
c5s1_ar = [
    ('The small intestine of herbivores is longer than that of carnivores.', 'Cellulose in plant food needs more time to digest.', 'a', 'R explains A.'),
    ('Bile does not contain any enzyme but helps in digestion.', 'Bile salts emulsify fats.', 'a', 'R explains A.'),
    ('Photosynthesis is an endothermic process.', 'Light energy is absorbed and stored as chemical energy in glucose.', 'a', 'R explains A.'),
    ('Pepsin works in an alkaline medium.', 'The stomach contains hydrochloric acid.', 'd', 'A is false (pepsin works in an acidic medium); R is true.'),
]
c5s1_seq = ['ingestion of food in the mouth', 'digestion of starch by saliva', 'food carried down the oesophagus by peristalsis', 'digestion of proteins in the stomach', 'complete digestion in the small intestine', 'absorption through villi', 'absorption of water in the large intestine', 'egestion through the anus']


def c5s1_ord(r):
    return _order(r, c5s1_seq, 'human digestion')


c5s2_defs = [
    ('respiration', 'the breakdown of food (glucose) in cells to release energy'),
    ('aerobic respiration', 'respiration in the presence of oxygen, giving carbon dioxide, water and a large amount of energy'),
    ('anaerobic respiration', 'respiration in the absence of oxygen, giving less energy'),
    ('fermentation', 'anaerobic breakdown of glucose by yeast to give ethanol and carbon dioxide'),
    ('ATP', 'adenosine triphosphate, the energy currency of the cell'),
    ('alveoli', 'tiny balloon-like air sacs in the lungs where gas exchange takes place'),
    ('pyruvate', 'the three-carbon molecule formed when glucose is broken down in the cytoplasm'),
    ('haemoglobin', 'the respiratory pigment in red blood cells that carries oxygen'),
]
c5s2_path = {
    'occurs in yeast and gives ethanol and carbon dioxide': ['fermentation in yeast'],
    'occurs in muscle cells during heavy exercise and gives lactic acid': ['anaerobic respiration in muscles'],
    'occurs in mitochondria and gives carbon dioxide, water and much energy': ['aerobic respiration'],
}
c5s2_cats = {
    'aerobic respiration': ['takes place in mitochondria', 'gives carbon dioxide and water', 'releases a large amount of energy', 'needs oxygen'],
    'anaerobic respiration': ['takes place in the cytoplasm only', 'gives ethanol or lactic acid', 'releases less energy', 'occurs without oxygen'],
}
c5s2_mc = [
    ('The first step of glucose breakdown into pyruvate occurs in the:', 'cytoplasm', 'mitochondria', 'nucleus', 'chloroplast'),
    ('Cramps in the leg muscles after a long run are due to:', 'accumulation of lactic acid', 'accumulation of ethanol', 'excess oxygen', 'excess glucose'),
    ('Fish take in oxygen dissolved in water through:', 'gills', 'lungs', 'skin only', 'stomata'),
    ('The rate of breathing in aquatic organisms is faster than in terrestrial organisms because:', 'the amount of dissolved oxygen in water is low', 'water is heavy', 'they have no lungs', 'water is warm'),
    ('The rings of cartilage in the throat ensure that:', 'the air passage does not collapse', 'food is swallowed', 'air is warmed', 'blood flows'),
    ('In plants, gas exchange takes place through:', 'stomata and lenticels', 'xylem', 'phloem', 'root caps'),
    ('Carbon dioxide is carried in the blood mostly:', 'dissolved in plasma', 'by haemoglobin only', 'by platelets', 'by white blood cells'),
]
c5s2_why = [
    ('Why do we need a respiratory pigment such as haemoglobin?', 'Oxygen diffuses too slowly to reach every cell of a large body; haemoglobin carries large amounts of oxygen quickly.', '1 mark size. 1 mark carries oxygen.'),
    ('How are the alveoli designed for maximum gas exchange?', 'They are numerous, thin-walled and balloon-like, giving a very large surface area (about 80 m²) and are surrounded by blood capillaries.', '1 mark area. 1 mark capillaries.'),
    ('Why do muscles get cramps during vigorous exercise?', 'Oxygen supply falls short, so pyruvate is converted to lactic acid by anaerobic respiration; lactic acid builds up.', '1 mark oxygen lack. 1 mark lactic acid.'),
    ('Why is the air passage lined with hair and mucus?', 'They filter dust and germs from the inhaled air.', '2 marks.'),
]
c5s2_ar = [
    ('Aquatic animals breathe faster than terrestrial animals.', 'The amount of dissolved oxygen in water is lower than in air.', 'a', 'R explains A.'),
    ('Yeast is used in making bread.', 'Yeast respires anaerobically to give carbon dioxide, which makes the dough rise.', 'a', 'R explains A.'),
    ('Aerobic respiration releases more energy than anaerobic respiration.', 'Glucose is completely broken down into CO₂ and water in aerobic respiration.', 'a', 'R explains A.'),
    ('Lungs collapse completely after we breathe out.', 'The lungs always contain a residual volume of air.', 'd', 'A is false; R is true.'),
]
c5s2_seq = ['air enters through the nostrils', 'it passes through the pharynx and larynx', 'it moves down the trachea', 'it enters the bronchi', 'it passes into bronchioles', 'it reaches the alveoli where gases are exchanged']


def c5s2_ord(r):
    return _order(r, c5s2_seq, 'the path of air in the human respiratory system')


def c5s2_breath(r):
    br = r.choice([12, 14, 15, 16, 18, 20])
    tv = r.choice([0.4, 0.5, 0.6])
    m = r.choice([1, 5, 10, 60])
    vol = br * tv * m
    nm = name(r)
    return {'stem': f'{nm} breathes {br} times a minute at rest, taking in about {num(tv)} L of air each time. How much air is breathed in {m} minute{"s" if m > 1 else ""}? Where in the lungs is oxygen absorbed?',
            'answer': f'{num(vol, 1)} L; in the alveoli', 'key': f'{br} × {num(tv)} × {m} = {num(vol, 1)} L. Gas exchange takes place in the alveoli.'}


c5s3_defs = [
    ('the double circulation', 'the passage of blood twice through the heart in one complete cycle, once for the body and once for the lungs'),
    ('an artery', 'a thick-walled blood vessel that carries blood away from the heart to the organs'),
    ('a vein', 'a blood vessel that carries blood from the organs back to the heart and has valves'),
    ('a capillary', 'the smallest blood vessel, with walls one cell thick, where exchange with tissues occurs'),
    ('lymph', 'a colourless fluid with less protein than plasma that drains from tissues into lymphatic vessels'),
    ('platelets', 'blood cells that help in clotting of blood at the site of an injury'),
    ('transpiration', 'the loss of water as water vapour from the aerial parts of a plant'),
    ('translocation', 'the transport of soluble products of photosynthesis through phloem'),
    ('blood pressure', 'the force that blood exerts against the walls of a vessel'),
]
c5s3_cats = {
    'oxygenated blood': ['the pulmonary vein', 'the left atrium', 'the left ventricle', 'the aorta'],
    'deoxygenated blood': ['the vena cava', 'the right atrium', 'the right ventricle', 'the pulmonary artery'],
}
c5s3_vt = {
    'carried by xylem': ['water from the roots to the leaves', 'dissolved minerals from the soil', 'nitrates absorbed by the roots'],
    'carried by phloem': ['sucrose from the leaves to the roots', 'amino acids to storage organs', 'food to growing buds'],
}
c5s3_mc = [
    ('The heart of fishes has:', 'two chambers', 'three chambers', 'four chambers', 'one chamber'),
    ('Amphibians and many reptiles have hearts with:', 'three chambers', 'two chambers', 'four chambers', 'five chambers'),
    ('Valves in the heart and veins:', 'prevent the backflow of blood', 'pump blood', 'make blood', 'clot blood'),
    ('The normal blood pressure of a healthy adult is about:', '120/80 mm of Hg', '80/120 mm of Hg', '200/100 mm of Hg', '60/40 mm of Hg'),
    ('Which blood vessel carries deoxygenated blood to the lungs?', 'pulmonary artery', 'pulmonary vein', 'aorta', 'vena cava'),
    ('The transport of water in xylem is mainly due to:', 'the suction created by transpiration', 'gravity', 'phloem pressure', 'osmosis in leaves only'),
    ('Translocation of food in phloem uses energy from:', 'ATP', 'sunlight directly', 'transpiration', 'gravity'),
    ('Lymph carries digested and absorbed fat from the:', 'small intestine (lacteals)', 'stomach', 'liver', 'kidneys'),
]
c5s3_why = [
    ('Why is it necessary to separate oxygenated and deoxygenated blood in mammals and birds?', 'They need a lot of energy to keep their body temperature constant; separation gives an efficient supply of oxygen.', '1 mark energy/warm-blooded. 1 mark efficient supply.'),
    ('Why are the walls of the ventricles thicker than those of the atria?', 'Ventricles pump blood to the body or lungs, so they need strong, thick muscular walls; the atria only push blood into the ventricles.', '1 mark each.'),
    ('Why do arteries have thick, elastic walls?', 'Blood flows from the heart under high pressure, so the walls must be thick and elastic.', '2 marks.'),
    ('How is water lifted to the tops of tall trees?', 'Transpiration from leaves creates a suction pull that draws water up through the continuous column of xylem; root pressure helps at night.', '1 mark transpiration pull. 1 mark xylem column.'),
    ('Give two functions of transpiration.', 'It helps in absorption and upward movement of water and minerals, and it regulates temperature (cools the plant).', '1 mark each.'),
]
c5s3_ar = [
    ('The pulmonary vein carries oxygenated blood.', 'It carries blood from the lungs to the heart.', 'a', 'R explains A.'),
    ('Veins have valves.', 'Blood in veins is under low pressure.', 'a', 'Valves stop backflow of low-pressure blood; R explains A.'),
    ('Fishes have a single circulation.', 'Blood passes through the heart only once in each cycle in fishes.', 'a', 'R explains A.'),
    ('Phloem transports water.', 'Phloem transports food.', 'd', 'A is false (xylem transports water); R is true.'),
]
c5s3_seq = ['deoxygenated blood from the body enters the right atrium', 'it passes into the right ventricle', 'it is pumped through the pulmonary artery to the lungs', 'oxygenated blood returns by the pulmonary vein to the left atrium', 'it passes into the left ventricle', 'it is pumped through the aorta to the body']


def c5s3_ord(r):
    return _order(r, c5s3_seq, 'blood flow through the human heart')


def c5s3_co(r):
    hr = r.choice([60, 70, 72, 75, 80])
    sv = r.choice([60, 65, 70, 75, 80])
    co = hr * sv / 1000
    nm = name(r)
    return {'stem': f'{nm}\'s heart beats {hr} times a minute and pumps about {sv} mL of blood with each beat from the left ventricle. How much blood is pumped in one minute? Into which blood vessel is it pumped?',
            'answer': f'{num(co, 2)} L per minute; into the aorta', 'key': f'{hr} × {sv} mL = {hr * sv} mL = {num(co, 2)} L. The left ventricle pumps into the aorta.'}


c5s4_defs = [
    ('excretion', 'the biological process of removing harmful nitrogenous metabolic wastes from the body'),
    ('the nephron', 'the basic filtration unit of the kidney'),
    ("Bowman's capsule", 'the cup-shaped upper end of a nephron that encloses the glomerulus'),
    ('the glomerulus', 'a cluster of thin-walled blood capillaries in Bowman\'s capsule where blood is filtered'),
    ('haemodialysis', 'the use of an artificial kidney to remove nitrogenous wastes from the blood of a patient with kidney failure'),
    ('urea', 'the main nitrogenous waste in human urine, made in the liver'),
    ('the urinary bladder', 'a muscular bag that stores urine until it is passed out'),
]
c5s4_organ = {
    'the kidneys': ['filter blood to form urine'],
    'the ureters': ['carry urine from the kidneys to the urinary bladder'],
    'the urinary bladder': ['stores urine'],
    'the urethra': ['carries urine out of the body'],
}
c5s4_organ = {f'the function of {k}': v for k, v in c5s4_organ.items()}
c5s4_plant = {
    'a way plants get rid of wastes': ['storing wastes in leaves that fall off', 'storing wastes as resins and gums in old xylem', 'releasing oxygen through stomata', 'losing excess water by transpiration', 'excreting some wastes into the soil'],
}
c5s4_mc = [
    ('Each kidney has about how many nephrons?', 'about 10 lakh (one million)', 'about 100', 'about 1000', 'about 1 crore'),
    ('The amount of water reabsorbed in the tubule depends on:', 'how much excess water is in the body and how much waste is to be removed', 'the size of the kidney', 'the colour of urine', 'the number of ureters'),
    ('In the nephron, useful substances such as glucose and amino acids are:', 'selectively reabsorbed in the tubule', 'excreted', 'stored in the bladder', 'converted to urea'),
    ('The urinary bladder is under:', 'nervous control', 'hormonal control only', 'no control', 'the control of the liver'),
    ('Plants get rid of excess carbon dioxide and oxygen through:', 'stomata', 'xylem', 'phloem', 'root hairs'),
    ('Haemodialysis differs from the working of a kidney because:', 'there is no reabsorption', 'it adds urea', 'it removes glucose permanently', 'it filters faster'),
]
c5s4_why = [
    ('How is the amount of urine produced regulated?', 'It depends on how much excess water and dissolved waste is in the body; more water is reabsorbed in the tubule when the body needs water.', '1 mark water. 1 mark reabsorption.'),
    ('Why is the kidney called a filtration unit? Name the structure that filters blood.', 'Blood is filtered under pressure in the glomerulus inside Bowman\'s capsule of each nephron; nitrogenous wastes and some useful substances pass into the tubule.', '1 mark glomerulus. 1 mark filtration.'),
    ('Why is an artificial kidney needed by some patients?', 'If the kidneys fail, wastes such as urea build up in the blood and can cause death; the dialyser removes them.', '2 marks.'),
]
c5s4_ar = [
    ('Glucose is normally absent in urine.', 'Glucose is selectively reabsorbed in the tubule of the nephron.', 'a', 'R explains A.'),
    ('Plants do not have special excretory organs.', 'Plants store some wastes in cell vacuoles and in leaves that fall off.', 'a', 'R explains A.'),
    ('Urine is formed in the urinary bladder.', 'The urinary bladder stores urine.', 'd', 'A is false (urine is formed in the kidneys); R is true.'),
]


def c5s4_reab(r):
    f = r.choice([170, 175, 180, 185])
    u = r.choice([1.2, 1.5, 1.8, 2])
    p = (f - u) / f * 100
    return {'stem': f'About {f} L of filtrate is formed in the kidneys of an adult each day, but only about {num(u)} L of urine is passed out. What percentage of the filtrate is reabsorbed? Where does this reabsorption take place?',
            'answer': f'{sig(p, 4)}%; in the tubules of the nephrons', 'key': f'Reabsorbed = {f} − {num(u)} = {num(f - u, 1)} L; % = {num(f - u, 1)}/{f} × 100 = {sig(p, 4)}%.'}


c5_hots = [
    ('A person is advised to take small, frequent meals after the gall bladder is removed. Explain why, in terms of fat digestion.', 'The gall bladder stores bile, which emulsifies fats and makes the food alkaline; without it, bile trickles slowly, so large fatty meals are poorly digested.', '1 mark bile role. 1 mark storage lost. 1 mark advice.'),
    ('A variegated leaf (green and white) of a plant kept in sunlight is tested with iodine. Which parts turn blue-black and what does this show? Why is the plant first kept in the dark?', 'Only the green parts turn blue-black, showing chlorophyll is needed to make starch. The dark period destarches the leaf.', '1 mark result. 1 mark conclusion. 1 mark destarching.'),
    ('Why does a mountaineer climbing Mount Everest carry oxygen cylinders, and what happens to the rate of breathing at high altitude without them?', 'The air at high altitude has less oxygen per breath; the body breathes faster and the heart beats faster to try to get enough oxygen, causing fatigue.', '1 mark low oxygen. 1 mark faster breathing. 1 mark consequence.'),
    ('Compare the transport of water in plants with the transport of blood in humans in terms of pump, tubes and energy used.', 'Plants: no pump; water rises through dead xylem vessels by transpiration pull (passive); food moves in living phloem using ATP. Humans: the heart pumps blood through arteries, veins and capillaries using energy from muscle contraction.', '1 mark each feature.'),
]
c5_case = [
    ('Read: Rani, a 55-year-old woman in Kolkata, has kidney failure. She is put on haemodialysis three times a week. Her doctor explains that each kidney has about ten lakh nephrons and that the dialyser removes urea but cannot reabsorb useful substances.\n'
     '(i) What is the main nitrogenous waste removed? (ii) Name the part of a nephron where blood is filtered. (iii) What happens to glucose in a healthy nephron? (iv) Why does the dialyser need fresh dialysing fluid?',
     '(i) Urea. (ii) The glomerulus in Bowman\'s capsule. (iii) It is selectively reabsorbed in the tubule. (iv) Wastes diffuse into the fluid, so fresh fluid keeps the concentration gradient for diffusion.', '1 mark each part.'),
    ('Read: Athletes at a Bhubaneswar stadium ran a 400 m race. Their breathing rate rose from 15 to 40 breaths per minute, and some felt cramps in their legs.\n'
     '(i) Why does the breathing rate increase? (ii) What causes the cramps? (iii) Write the pathway of glucose breakdown in the muscle during the cramp. (iv) Where in the cell does aerobic respiration release most energy?',
     '(i) To supply more oxygen for aerobic respiration and remove CO₂. (ii) Lactic acid builds up from anaerobic respiration. (iii) Glucose → (cytoplasm) pyruvate → (lack of oxygen) lactic acid + energy. (iv) Mitochondria.', '1 mark each part.'),
    ('Read: In an experiment, a potted plant was kept in the dark for two days, then one leaf was enclosed in a bottle containing KOH (which absorbs CO₂) and the plant was kept in sunlight. The leaf was then tested with iodine.\n'
     '(i) Why was the plant kept in the dark? (ii) What colour did the leaf in the bottle show with iodine? (iii) What does the experiment prove? (iv) Write the balanced equation for photosynthesis.',
     '(i) To destarch the leaves. (ii) No blue-black colour (stays brown/yellowish). (iii) Carbon dioxide is needed for photosynthesis. (iv) 6CO₂ + 12H₂O → (chlorophyll, sunlight) C₆H₁₂O₆ + 6O₂ + 6H₂O.', '1 mark each part.'),
]
c5_long = [
    ('Describe the process of digestion in humans from the mouth to the small intestine, naming the enzymes and their actions. How is the digested food absorbed?',
     'Mouth: salivary amylase converts starch to sugar. Stomach: HCl makes medium acidic, pepsin digests proteins, mucus protects lining. Small intestine: bile from liver makes food alkaline and emulsifies fats; pancreatic juice has trypsin (proteins) and lipase (fats); intestinal juice converts proteins to amino acids, carbohydrates to glucose, fats to fatty acids and glycerol. Villi absorb digested food into blood.',
     '1 mark mouth; 1 mark stomach; 2 marks small intestine; 1 mark absorption.'),
    ('Describe the structure and working of the human heart with a labelled diagram. What is double circulation and why is it necessary?',
     'Four chambers: right and left atria and ventricles; valves prevent backflow. Deoxygenated blood from the vena cava → right atrium → right ventricle → pulmonary artery → lungs; oxygenated blood → pulmonary vein → left atrium → left ventricle → aorta → body. Double circulation: blood passes through the heart twice per cycle; it keeps oxygenated and deoxygenated blood separate, giving efficient oxygen supply to warm-blooded animals.',
     '1 mark diagram; 2 marks pathway; 2 marks double circulation.'),
    ('Describe the structure of a nephron and explain how urine is formed. How do plants get rid of their wastes?',
     'Nephron: Bowman\'s capsule with glomerulus, tubule, collecting duct. Blood filtered in the glomerulus; filtrate contains glucose, amino acids, salts, urea and water; useful substances and water are selectively reabsorbed in the tubule; urine goes to collecting duct → ureter → bladder. Plants: oxygen and CO₂ through stomata, excess water by transpiration, wastes stored in leaves, bark, vacuoles, resins and gums, some excreted into the soil.',
     '1 mark structure; 2 marks urine formation; 2 marks plants.'),
    ('Differentiate between aerobic and anaerobic respiration. Show the breakdown of glucose by different pathways with a flow chart. Explain the mechanism of breathing in humans.',
     'Aerobic: with oxygen, in mitochondria, CO₂ + water + much energy. Anaerobic: without oxygen, in cytoplasm, ethanol + CO₂ (yeast) or lactic acid (muscles), less energy. Glucose → pyruvate (cytoplasm) → ethanol + CO₂ (yeast) / lactic acid (muscle) / CO₂ + H₂O (mitochondria, with O₂). Breathing: diaphragm flattens and ribs lift, chest cavity enlarges, air is sucked in; reverse during exhalation.',
     '2 marks differences; 2 marks flow chart; 1 mark mechanism.'),
]

# ======================= ch06 Control and Coordination
c6s1_defs = [
    ('a neuron', 'the structural and functional unit of the nervous system'),
    ('a synapse', 'the gap between the nerve ending of one neuron and the dendrite of the next, across which a chemical signal passes'),
    ('a reflex action', 'a sudden, automatic response to a stimulus that does not involve thinking'),
    ('a reflex arc', 'the pathway of nerves from a receptor to the spinal cord and back to an effector during a reflex action'),
    ('a receptor', 'a specialised tip of a nerve cell in a sense organ that detects information from the environment'),
    ('an effector', 'a muscle or gland that responds to a nerve impulse'),
    ('the central nervous system', 'the brain and spinal cord'),
    ('the peripheral nervous system', 'the cranial and spinal nerves that connect the central nervous system to all parts of the body'),
]
c6s1_brain = {
    'the cerebrum (fore-brain)': ['thinking, memory and voluntary actions', 'receiving sensory information such as hearing, smell and sight'],
    'the cerebellum (hind-brain)': ['maintaining posture and balance of the body', 'precision of voluntary actions such as picking up a pencil'],
    'the medulla (hind-brain)': ['controlling blood pressure', 'salivation and vomiting', 'regulating heartbeat and breathing'],
    'the hypothalamus (fore-brain)': ['the feeling of hunger'],
}
c6s1_brain = {f'controlled by {k}': v for k, v in c6s1_brain.items()}
c6s1_vol = {
    'a reflex action': ['pulling the hand away from a hot plate', 'blinking when dust enters the eye', 'sneezing', 'knee-jerk response'],
    'a voluntary action': ['writing a letter', 'riding a bicycle', 'talking to a friend', 'walking to school'],
}
c6s1_mc = [
    ('The part of a neuron that receives information is the:', 'dendrite', 'axon', 'nerve ending', 'synapse'),
    ('Reflex arcs are formed in the:', 'spinal cord', 'cerebrum', 'cerebellum', 'medulla only'),
    ('The brain is protected by:', 'a bony box (cranium) and fluid-filled balloon', 'the spinal cord', 'muscles only', 'ribs'),
    ('Which part of the brain maintains posture and balance?', 'cerebellum', 'cerebrum', 'medulla', 'pons'),
    ('At a synapse, the electrical impulse is converted into a:', 'chemical signal', 'mechanical signal', 'sound signal', 'light signal'),
    ('The spinal cord is protected by the:', 'vertebral column', 'skull', 'ribs', 'pelvis'),
    ('An impulse travels in a neuron in the order:', 'dendrite → cell body → axon → nerve ending', 'axon → dendrite → cell body', 'cell body → dendrite → axon', 'nerve ending → axon → dendrite'),
]
c6s1_why = [
    ('Why are reflex actions useful?', 'They give a very quick response to danger without the delay of thinking, protecting the body.', '2 marks.'),
    ('Why does the information flow only in one direction at a synapse?', 'Chemicals are released only from the nerve ending of the axon and received by dendrites of the next neuron.', '2 marks.'),
    ('What are the limitations of using electrical impulses for coordination?', 'They reach only cells connected by nerves, and a cell needs time to reset before sending a new impulse; they cannot act continuously.', '1 mark each.'),
    ('How is the brain protected?', 'It lies in a bony box (cranium) and is surrounded by a fluid-filled balloon that absorbs shocks.', '1 mark each.'),
]
c6s1_ar = [
    ('A reflex action does not involve the thinking part of the brain.', 'Reflex arcs are formed in the spinal cord.', 'a', 'R explains A.'),
    ('Damage to the cerebellum affects balance.', 'The cerebellum maintains posture and balance.', 'a', 'R explains A.'),
    ('Nerve impulses travel from axon to dendrite of the same neuron.', 'Dendrites receive information.', 'd', 'A is false (dendrite → cell body → axon); R is true.'),
]
c6s1_seq = ['the receptor in the skin detects heat', 'the sensory neuron carries the impulse', 'the relay neuron in the spinal cord passes it on', 'the motor neuron carries the impulse', 'the effector muscle contracts and the hand is pulled away']


def c6s1_ord(r):
    return _order(r, c6s1_seq, 'a reflex arc (touching a hot object)')


c6s2_defs = [
    ('a tropism', 'a directional growth movement of a plant part in response to a stimulus'),
    ('phototropism', 'the growth of a plant part towards or away from light'),
    ('geotropism', 'the growth of a plant part in response to gravity'),
    ('hydrotropism', 'the growth of roots towards water'),
    ('chemotropism', 'growth in response to chemicals, such as the pollen tube growing towards the ovule'),
    ('a plant hormone', 'a chemical produced by plants that controls their growth and development'),
    ('thigmonasty', 'a non-directional movement in response to touch, as in the leaves of the touch-me-not plant'),
]
c6s2_hor = {
    'auxin': ['helps cells grow longer and causes bending towards light', 'is made at the shoot tip'],
    'gibberellin': ['helps in the growth of the stem'],
    'cytokinin': ['promotes cell division, found in fruits and seeds'],
    'abscisic acid': ['inhibits growth and causes wilting of leaves'],
}
c6s2_hor = {f'the role of {k}': v for k, v in c6s2_hor.items()}
c6s2_trop = {
    'phototropism': ['a shoot bending towards a window', 'sunflower heads following the Sun'],
    'positive geotropism': ['roots growing downwards'],
    'negative geotropism': ['the shoot growing upwards away from gravity'],
    'hydrotropism': ['roots growing towards a leaking pipe'],
    'chemotropism': ['the pollen tube growing towards the ovule'],
    'thigmotropism': ['tendrils of a pea plant coiling around a support'],
}
c6s2_trop = {f'an example of {k}': v for k, v in c6s2_trop.items()}
c6s2_mc = [
    ('The leaves of the touch-me-not plant fold when touched because:', 'cells change shape by changing the amount of water in them', 'they grow', 'auxin moves', 'they lose chlorophyll'),
    ('When light falls on one side of a shoot, auxin:', 'diffuses to the shady side, making it grow faster so the shoot bends towards light', 'moves to the lighted side', 'is destroyed', 'moves to the roots'),
    ('Which plant hormone inhibits growth?', 'abscisic acid', 'auxin', 'gibberellin', 'cytokinin'),
    ('Tendrils coil around a support because:', 'the part away from the support grows faster', 'the part in contact grows faster', 'they are pulled', 'of gravity'),
    ('Plants respond to stimuli without a nervous system by using:', 'chemicals (hormones) and changes in water content of cells', 'nerves', 'muscles', 'blood'),
]
c6s2_why = [
    ('How is the movement of leaves of the sensitive plant different from the movement of a shoot towards light?', 'The sensitive plant\'s leaves move quickly by losing water from cells, and it is not growth; the shoot bends slowly by growth (phototropism) due to auxin.', '1 mark each.'),
    ('Why does a plant kept near a window bend towards it?', 'Auxin collects on the shaded side of the shoot, making those cells grow longer, so the shoot bends towards light.', '1 mark auxin shady side. 1 mark bending.'),
    ('How do plant hormones help a seed to germinate and the plant to grow?', 'Gibberellins promote stem growth, cytokinins promote cell division, auxins help cells elongate; abscisic acid controls dormancy.', '1 mark each (any two).'),
]
c6s2_ar = [
    ('Shoots show positive phototropism.', 'Auxin makes cells on the shaded side grow longer.', 'a', 'R explains A.'),
    ('Roots grow downwards.', 'Roots are positively geotropic.', 'a', 'R explains A.'),
    ('The folding of touch-me-not leaves is a growth movement.', 'The leaf cells change shape by losing water.', 'd', 'A is false (it is not a growth movement); R is true.'),
]

c6s3_defs = [
    ('a hormone', 'a chemical messenger secreted by an endocrine gland directly into the blood'),
    ('an endocrine gland', 'a ductless gland that secretes hormones directly into the blood'),
    ('a feedback mechanism', 'a mechanism in which the level of a substance in the blood controls the secretion of the hormone that regulates it'),
    ('goitre', 'a swelling of the neck due to enlargement of the thyroid gland caused by iodine deficiency'),
    ('diabetes', 'a disease in which the blood sugar level is high because the pancreas does not secrete enough insulin'),
    ('dwarfism', 'a condition of very short height caused by deficiency of growth hormone in childhood'),
]
c6s3_gland = {
    'thyroxin': ['the thyroid gland'], 'insulin': ['the pancreas'], 'adrenaline': ['the adrenal gland'], 'growth hormone': ['the pituitary gland'],
    'testosterone': ['the testes'], 'oestrogen': ['the ovaries'],
}
c6s3_gland = {f'secreted by {v[0]}': [k] for k, v in c6s3_gland.items()}
c6s3_fn = {
    'regulating carbohydrate, protein and fat metabolism': ['thyroxin'],
    'regulating blood sugar level': ['insulin'],
    'preparing the body for an emergency (fight or flight)': ['adrenaline'],
    'regulating growth and development of the body': ['growth hormone'],
    'development of male sex organs and features at puberty': ['testosterone'],
    'development of female sex organs and the menstrual cycle': ['oestrogen'],
}
c6s3_fn = {f'responsible for {k}': v for k, v in c6s3_fn.items()}
GLANDS = [('thyroxin', 'thyroid gland', 'regulates metabolism of carbohydrates, proteins and fats'), ('insulin', 'pancreas', 'regulates blood sugar level'),
          ('adrenaline', 'adrenal gland', 'prepares the body for emergencies'), ('growth hormone', 'pituitary gland', 'regulates growth and development'),
          ('testosterone', 'testes', 'controls male changes at puberty'), ('oestrogen', 'ovaries', 'controls female changes at puberty')]
c6s3_mc = [
    ('Iodised salt is advised to prevent:', 'goitre', 'diabetes', 'dwarfism', 'night blindness'),
    ('Adrenaline increases the:', 'heart rate and breathing rate', 'digestion', 'blood flow to the skin', 'sleep'),
    ('Which gland is called the master gland?', 'pituitary', 'thyroid', 'adrenal', 'pancreas'),
    ('The timing and amount of hormone released are regulated by:', 'feedback mechanisms', 'nerves only', 'food', 'blood cells'),
    ('Insulin is secreted by the:', 'pancreas', 'liver', 'thyroid', 'pituitary'),
    ('Excess growth hormone in childhood leads to:', 'gigantism', 'dwarfism', 'goitre', 'diabetes'),
]
c6s3_why = [
    ('How does adrenaline prepare the body for an emergency?', 'It speeds up the heartbeat and breathing, diverts blood to skeletal muscles from the digestive system and skin, so more oxygen reaches muscles.', '1 mark heart/breathing. 1 mark blood diverted.'),
    ('Why is the use of iodised salt advised?', 'Iodine is needed by the thyroid to make thyroxin; lack of it causes goitre.', '1 mark thyroxin. 1 mark goitre.'),
    ('Explain the feedback control of insulin secretion.', 'When blood sugar rises, the pancreas detects it and secretes more insulin; as sugar falls, insulin secretion is reduced.', '1 mark each.'),
    ('Give two differences between nervous and hormonal coordination.', 'Nervous: electrical impulses, fast, short-lived, through nerves. Hormonal: chemicals in blood, slow, long-lasting, reach all cells.', '1 mark each.'),
]
c6s3_ar = [
    ('Diabetic patients are treated with insulin injections.', 'Insulin lowers the blood sugar level.', 'a', 'R explains A.'),
    ('Endocrine glands do not have ducts.', 'They release hormones directly into the blood.', 'a', 'R explains A.'),
    ('The thyroid gland secretes adrenaline.', 'The adrenal gland is located above the kidneys.', 'd', 'A is false (thyroid secretes thyroxin); R is true.'),
]


def c6s3_match(r):
    h, g, f = r.choice(GLANDS)
    q = r.choice(['gland', 'hormone'])
    if q == 'gland':
        return {'stem': f'Which gland secretes {h}, and what is its function?', 'answer': f'The {g}; it {f}.', 'key': '1 mark gland. 1 mark function.'}
    return {'stem': f'Name the hormone secreted by the {g} and state one effect of its deficiency or excess.', 'answer': f'{cap(h)}; ' + {
        'thyroxin': 'deficiency (of iodine) causes goitre.', 'insulin': 'deficiency causes diabetes (high blood sugar).', 'adrenaline': 'excess raises heart rate and blood pressure (deficiency weakens stress response).',
        'growth hormone': 'deficiency causes dwarfism; excess causes gigantism.', 'testosterone': 'deficiency delays male changes at puberty.', 'oestrogen': 'deficiency delays female changes and affects the menstrual cycle.'}[h],
        'key': '1 mark hormone. 1 mark effect.'}


c6_hots = [
    ('A person who has had a stroke can still feel a pin prick but cannot walk in a balanced way. Which part of the brain is likely damaged? Explain.', 'The cerebellum, which controls posture, balance and precise movement; the sensory pathways to the cerebrum are working.', '1 mark cerebellum. 1 mark balance. 1 mark sensation intact.'),
    ('A plant growing in a pot is laid on its side in the dark. After a few days, which way do the shoot and root grow, and why?', 'The shoot bends upwards (negative geotropism) and the root bends downwards (positive geotropism), controlled by auxin redistribution under gravity.', '1 mark shoot. 1 mark root. 1 mark auxin.'),
    ('Why is a sudden fright followed by a racing heart, while a decision to raise your hand is not?', 'Fright triggers adrenaline release and involuntary/reflex responses via the medulla and hormones; raising a hand is a voluntary action controlled by the cerebrum with no hormone surge.', '1 mark adrenaline. 1 mark involuntary. 1 mark voluntary.'),
    ('A child in a hilly area of Uttarakhand has a swollen neck and is slow in growth. Suggest the cause, the gland involved and a simple preventive measure.', 'Iodine deficiency → thyroid cannot make enough thyroxin → goitre; use iodised salt.', '1 mark each.'),
]
c6_case = [
    ('Read: Arjun touched a hot pan and pulled his hand back at once before he felt pain. Later he carefully picked up a pencil to write about it.\n'
     '(i) What type of action was pulling back the hand? (ii) Where is the arc of this action formed? (iii) Which part of the brain controls the precise action of picking up the pencil? (iv) Write the path of the impulse in a reflex arc.',
     '(i) A reflex action. (ii) In the spinal cord. (iii) The cerebellum (with the cerebrum for the voluntary decision). (iv) Receptor → sensory neuron → relay neuron in spinal cord → motor neuron → effector muscle.', '1 mark each part.'),
    ('Read: A gardener placed a potted seedling in a box with a single hole on one side. After a week the shoot had bent towards the hole, and the roots grew downwards and towards a wet patch of soil.\n'
     '(i) Name the response of the shoot. (ii) Name the hormone responsible. (iii) Which two tropisms do the roots show? (iv) How does the hormone make the shoot bend?',
     '(i) Phototropism (positive). (ii) Auxin. (iii) Positive geotropism and hydrotropism. (iv) Auxin moves to the shaded side and makes those cells grow longer, so the shoot bends towards light.', '1 mark each part.'),
]
c6_long = [
    ('Draw the structure of a neuron and explain its function. What is a reflex arc? Describe it with a flow chart using the example of touching a hot object.',
     'Neuron: dendrites receive information, cell body, long axon conducts impulse to nerve endings; chemicals released at the synapse pass the signal on. Reflex arc: path from receptor → sensory neuron → spinal cord (relay neuron) → motor neuron → effector muscle; quick, without thinking.',
     '2 marks neuron; 1 mark definition; 2 marks flow chart.'),
    ('Name the three main parts of the human brain and give two functions of each. How are the brain and spinal cord protected?',
     'Fore-brain (cerebrum): thinking, voluntary actions, sensory areas; hypothalamus for hunger. Mid-brain: involuntary actions such as reflex movements of head and eyes. Hind-brain: cerebellum (posture, balance, precision), medulla (blood pressure, salivation, vomiting), pons. Brain in cranium with fluid-filled balloon; spinal cord in vertebral column.',
     '1 mark each part (3); 2 marks protection.'),
    ('Name the endocrine glands in humans with the hormones they secrete and one function of each. Explain the feedback mechanism with an example.',
     'Pituitary – growth hormone (growth); thyroid – thyroxin (metabolism); pancreas – insulin (blood sugar); adrenal – adrenaline (emergency); testes – testosterone; ovaries – oestrogen; hypothalamus – releasing hormones. Feedback: rise in blood sugar → pancreas secretes insulin → sugar falls → secretion reduces.',
     '3 marks glands; 2 marks feedback.'),
]

# ======================= ch07 How do Organisms Reproduce?
c7s1_defs = [
    ('DNA', 'deoxyribonucleic acid, the molecule in chromosomes that carries information for inheritance of features'),
    ('variation', 'differences among individuals of a species'),
    ('a population', 'a group of individuals of the same species living in an area'),
    ('a niche', 'the specific role and conditions of an organism in its ecosystem'),
    ('DNA copying', 'the making of two copies of DNA in a cell before it divides'),
]
c7s1_mc = [
    ('The basic event in reproduction is the creation of a:', 'DNA copy', 'new cell membrane', 'new food vacuole', 'new nucleus without DNA'),
    ('Variations are useful for the survival of a species because:', 'some individuals may survive if the environment changes', 'all individuals become identical', 'they stop reproduction', 'they make cells die'),
    ('If the temperature of water rises suddenly, which bacteria are most likely to survive?', 'those with variations resistant to heat', 'those that are identical to the parent', 'all bacteria', 'none'),
    ('DNA copying is not perfectly accurate. This causes:', 'variation', 'death of all cells', 'no change', 'sexual reproduction'),
]
c7s1_why = [
    ('Why is DNA copying essential in reproduction?', 'It passes the body design and features from the parent to the offspring, so the new cell can function like the parent.', '2 marks.'),
    ('Why is variation beneficial to the species but not necessarily to the individual?', 'Variation helps some members survive changes in the environment, keeping the species going; a particular variation may not help the individual itself.', '1 mark species. 1 mark individual.'),
    ('Why do offspring from asexual reproduction show very little variation?', 'Only one parent is involved and DNA is copied with only small errors.', '2 marks.'),
]
c7s1_ar = [
    ('Variation helps in the survival of a species.', 'Some variants may be able to live in changed environments.', 'a', 'R explains A.'),
    ('Offspring produced by DNA copying are exactly identical to the parent.', 'DNA copying is always perfectly accurate.', 'e', ''),
    ('Reproduction is linked to the stability of populations of species.', 'Consistent DNA copying keeps the body designs of a species stable.', 'a', 'R explains A.'),
]
c7s1_ar[1] = ('Offspring produced asexually are similar but not exactly identical to the parent.', 'DNA copying involves small inaccuracies.', 'a', 'R explains A.')

c7s2_defs = [
    ('fission', 'the splitting of a unicellular organism into two or more daughter cells'),
    ('fragmentation', 'breaking of a mature organism into pieces, each growing into a new individual'),
    ('regeneration', 'the ability of a fully differentiated organism to grow into new individuals from its body parts'),
    ('budding', 'the formation of a new individual from an outgrowth of the parent'),
    ('vegetative propagation', 'the growth of new plants from the vegetative parts (root, stem, leaf) of a parent plant'),
    ('spore formation', 'reproduction by tiny thick-walled cells (spores) released from sporangia'),
    ('tissue culture', 'growing new plants from cells of a growing tip in an artificial medium'),
]
c7s2_cats = {
    'binary fission': ['Amoeba', 'Leishmania', 'bacteria', 'Paramecium'],
    'multiple fission': ['Plasmodium'],
    'fragmentation': ['Spirogyra'],
    'regeneration': ['Planaria'],
    'budding': ['Hydra', 'yeast'],
    'spore formation': ['Rhizopus', 'Mucor'],
    'vegetative propagation': ['Bryophyllum', 'sugarcane', 'potato', 'banana', 'rose'],
}
c7s2_cats = {f'{k}': v for k, v in c7s2_cats.items()}
c7s2_mc = [
    ('Leishmania divides by binary fission in a definite orientation because of:', 'a whip-like structure at one end', 'its nucleus', 'its spores', 'its buds'),
    ('Bryophyllum is propagated by:', 'buds on the notches of its leaf margins', 'seeds only', 'spores', 'fission'),
    ('Which of these does NOT reproduce by spores?', 'Hydra', 'Rhizopus', 'Mucor', 'fern'),
    ('Most simple multicellular organisms cannot reproduce by cell division alone because:', 'they have specialised cells organised into tissues and organs', 'they are too small', 'they lack DNA', 'they are unicellular'),
    ('An advantage of vegetative propagation is:', 'all plants are genetically similar to the parent', 'it produces great variation', 'it needs two parents', 'it needs pollination'),
]
c7s2_why = [
    ('Why can Planaria regenerate but not complex animals like humans?', 'Planaria has specialised cells that can divide and form all tissues; complex organisms have highly specialised cells that cannot recreate the whole body.', '1 mark each.'),
    ('Why is vegetative propagation practised for growing some types of plants?', 'It gives plants identical to the parent quickly, and is used for plants that do not produce viable seeds (banana, orange, rose).', '1 mark each.'),
    ('How does Plasmodium reproduce?', 'By multiple fission: the nucleus divides many times and the cell splits into many daughter cells at once.', '2 marks.'),
]
c7s2_ar = [
    ('Rhizopus reproduces by spores.', 'Spores are protected by thick walls until they find a moist surface.', 'b', 'Both are true; R does not explain why it uses spores.'),
    ('Plants raised by vegetative propagation bear flowers and fruits earlier.', 'They grow from mature parts of a parent plant.', 'a', 'R explains A.'),
    ('Planaria reproduces by budding.', 'Planaria can regenerate from small pieces.', 'd', 'A is false (Planaria shows regeneration/fragmentation); R is true.'),
]

c7s3_defs = [
    ('pollination', 'the transfer of pollen grains from the anther to the stigma'),
    ('fertilisation', 'the fusion of the male germ cell with the female gamete (egg) to form a zygote'),
    ('a bisexual flower', 'a flower having both stamens and pistil, such as hibiscus and mustard'),
    ('a unisexual flower', 'a flower having either stamens or pistil, such as papaya and watermelon'),
    ('germination', 'the development of the embryo in a seed into a seedling under suitable conditions'),
    ('the plumule', 'the part of the embryo that develops into the shoot'),
    ('the radicle', 'the part of the embryo that develops into the root'),
    ('a cotyledon', 'the seed leaf that stores food for the embryo'),
]
c7s3_parts = {
    'a part of the stamen': ['anther', 'filament'],
    'a part of the pistil (carpel)': ['stigma', 'style', 'ovary'],
    'a part of a seed': ['plumule', 'radicle', 'cotyledon', 'seed coat'],
}
c7s3_after = {
    'develops into the fruit': ['the ovary'], 'develops into the seed': ['the ovule'], 'develops into the embryo': ['the zygote'],
}
c7s3_mc = [
    ('After fertilisation, the ovary develops into the:', 'fruit', 'seed', 'embryo', 'cotyledon'),
    ('The pollen tube reaches the female germ cell in the:', 'ovule', 'stigma', 'style', 'anther'),
    ('Which of these flowers is unisexual?', 'papaya', 'hibiscus', 'mustard', 'rose'),
    ('In the seed, food for the embryo is stored in the:', 'cotyledons', 'plumule', 'radicle', 'seed coat'),
    ('Self-pollination is the transfer of pollen to the stigma of:', 'the same flower or another flower of the same plant', 'a flower of another plant', 'any plant', 'an animal'),
    ('The male germ cell in plants is produced in the:', 'pollen grain', 'ovule', 'stigma', 'petal'),
]
c7s3_why = [
    ('How is the process of pollination different from fertilisation?', 'Pollination is the transfer of pollen from anther to stigma; fertilisation is the fusion of the male germ cell with the egg in the ovule.', '1 mark each.'),
    ('What happens to the parts of a flower after fertilisation?', 'The ovary becomes the fruit, ovules become seeds, the zygote becomes the embryo; petals, sepals, stamens, style and stigma wither and fall.', '1 mark each (two changes).'),
    ('Why does cross-pollination produce more variation than self-pollination?', 'Gametes come from two different plants with different DNA, so new combinations arise.', '2 marks.'),
]
c7s3_ar = [
    ('The ovary develops into a fruit after fertilisation.', 'The ovary contains ovules that become seeds.', 'b', 'Both true; R does not explain why the ovary becomes the fruit.'),
    ('Papaya flowers cannot self-pollinate.', 'Papaya bears unisexual flowers.', 'a', 'R explains A.'),
    ('Fertilisation in flowering plants takes place on the stigma.', 'Pollen grains land on the stigma.', 'd', 'A is false (it takes place in the ovule); R is true.'),
]
c7s3_seq = ['pollen lands on the stigma', 'a pollen tube grows through the style', 'the tube reaches the ovule', 'the male germ cell fuses with the egg to form a zygote', 'the zygote divides to form the embryo', 'the ovule develops a tough coat and becomes a seed', 'the ovary grows and ripens to form a fruit']


def c7s3_ord(r):
    return _order(r, c7s3_seq, 'sexual reproduction in a flowering plant')


c7s4_defs = [
    ('puberty', 'the period of adolescence during which reproductive tissues mature'),
    ('the testes', 'the male reproductive organs that produce sperms and testosterone'),
    ('the ovaries', 'the female reproductive organs that produce eggs and hormones'),
    ('the placenta', 'a disc-like tissue embedded in the uterine wall through which the embryo gets nutrition from the mother\'s blood'),
    ('menstruation', 'the monthly breakdown and removal of the thick uterine lining through the vagina as blood and mucus when the egg is not fertilised'),
    ('contraception', 'methods used to prevent pregnancy'),
    ('a sexually transmitted infection', 'an infection spread by sexual contact, such as gonorrhoea, syphilis and HIV-AIDS'),
    ('the vas deferens', 'the tube that carries sperms from the testes to the urethra'),
]
c7s4_male = {
    'a part of the male reproductive system': ['testes', 'vas deferens', 'seminal vesicles', 'prostate gland', 'scrotum'],
    'a part of the female reproductive system': ['ovary', 'oviduct (fallopian tube)', 'uterus', 'cervix', 'vagina'],
}
c7s4_con = {
    'a barrier method': ['condom', 'diaphragm'],
    'a chemical (hormonal) method': ['oral contraceptive pills'],
    'an intrauterine method': ['copper-T (loop)'],
    'a surgical method': ['vasectomy (blocking the vas deferens)', 'tubectomy (blocking the fallopian tube)'],
}
c7s4_sti = {
    'a bacterial infection': ['gonorrhoea', 'syphilis'],
    'a viral infection': ['HIV-AIDS', 'warts'],
}
c7s4_mc = [
    ('Fertilisation in humans normally takes place in the:', 'oviduct (fallopian tube)', 'uterus', 'vagina', 'ovary'),
    ('The testes are located outside the abdominal cavity in the scrotum because:', 'sperm formation needs a lower temperature than normal body temperature', 'they are too large', 'they need light', 'they need air'),
    ('The time from fertilisation to the birth of a child is about:', 'nine months', 'six months', 'three months', 'twelve months'),
    ('Which method also protects against sexually transmitted infections?', 'condoms', 'copper-T', 'oral pills', 'vasectomy'),
    ('Female foeticide, which is illegal in India, causes:', 'a decline in the female-to-male sex ratio', 'more girls', 'better health', 'no effect'),
    ('Which hormone brings changes in boys at puberty?', 'testosterone', 'oestrogen', 'insulin', 'thyroxin'),
    ('Which of these sexually transmitted infections is caused by a virus?', 'HIV-AIDS', 'gonorrhoea', 'syphilis', 'typhoid'),
    ('Which of these sexually transmitted infections is caused by bacteria?', 'syphilis', 'HIV-AIDS', 'warts', 'common cold'),
]
c7s4_why = [
    ('Why does menstruation occur?', 'If the egg is not fertilised, the thick, spongy lining of the uterus prepared to receive an embryo is not needed, so it breaks and comes out as blood and mucus.', '1 mark no fertilisation. 1 mark lining shed.'),
    ('How does the embryo get nourishment inside the mother\'s body?', 'Through the placenta: villi on the embryo\'s side take glucose and oxygen from the mother\'s blood; wastes pass the other way.', '1 mark placenta. 1 mark exchange.'),
    ('Why are contraceptive methods important for the health of women and society?', 'They prevent unwanted pregnancies, protect women\'s health and help control population growth; condoms also prevent STIs.', '1 mark each.'),
    ('What are the changes in girls at puberty?', 'Breast size increases, dark skin of the nipples, hair in armpits and genital area, menstruation begins, body shape changes.', '1 mark each (any two).'),
]
c7s4_ar = [
    ('The use of condoms helps prevent sexually transmitted infections.', 'Condoms prevent contact of bodily fluids during intercourse.', 'a', 'R explains A.'),
    ('Copper-T is a contraceptive device.', 'It is placed in the uterus to prevent pregnancy.', 'a', 'R explains A.'),
    ('Fertilisation in humans takes place in the uterus.', 'The embryo gets implanted in the uterine wall.', 'd', 'A is false (it occurs in the oviduct); R is true.'),
]
c7s4_seq = ['sperms are formed in the testes', 'they travel through the vas deferens', 'they mix with fluids from the seminal vesicles and prostate', 'they leave through the urethra', 'in the female, a sperm meets the egg in the oviduct', 'the fertilised egg (zygote) gets implanted in the uterus wall']


def c7s4_ord(r):
    return _order(r, c7s4_seq, 'human reproduction', )


c7_hots = [
    ('A farmer in Maharashtra grows sugarcane and bananas from cuttings and suckers, not seeds. Give two advantages and one disadvantage of this practice.', 'Advantages: identical plants with known good traits; quick growth; plants that do not form seeds can be grown. Disadvantage: no variation, so a disease can destroy the whole crop.', '2 marks advantages. 1 mark disadvantage.'),
    ('If a woman uses a copper-T, will it protect her from sexually transmitted infections? Explain, and name a method that does.', 'No. Copper-T only prevents pregnancy by acting in the uterus; it does not stop contact with bodily fluids. Condoms protect against STIs.', '1 mark no. 1 mark reason. 1 mark condom.'),
    ('Why is sexual reproduction considered to promote diversity of characters in the offspring, while asexual reproduction does not?', 'Sexual reproduction combines DNA from two parents through gametes (each with half the DNA), producing new combinations; asexual involves one parent with DNA copied nearly exactly.', '1 mark two parents. 1 mark half DNA. 1 mark asexual.'),
    ('Why do germ cells have half the number of chromosomes of body cells? What would happen if they did not?', 'So that when two germ cells fuse, the zygote has the normal (full) number; otherwise the amount of DNA would double in each generation.', '1 mark half. 1 mark restoration. 1 mark doubling.'),
]
c7_case = [
    ('Read: In a school lab, Fatima observed bread mould under a microscope. She saw thread-like hyphae with tiny blob-like structures on top. She also saw a slide of yeast with small outgrowths, and one of Amoeba dividing into two.\n'
     '(i) Name the blob-like structures and what they contain. (ii) Name the mode of reproduction in yeast. (iii) What is the process in Amoeba? (iv) Why do the spores of bread mould not germinate on dry bread?',
     '(i) Sporangia containing spores. (ii) Budding. (iii) Binary fission. (iv) Spores need moisture (and warmth) to germinate.', '1 mark each part.'),
    ('Read: In 2011 the child sex ratio in some districts of India fell to about 830 girls per 1000 boys. The government banned prenatal sex determination and started the "Beti Bachao, Beti Padhao" campaign.\n'
     '(i) What is meant by female foeticide? (ii) Why is prenatal sex determination banned? (iii) Who determines the sex of the child, mother or father? (iv) Suggest one way to improve the sex ratio.',
     '(i) Killing of a female foetus before birth. (ii) To stop female foeticide and maintain a healthy sex ratio. (iii) The father (X or Y chromosome in the sperm). (iv) Awareness campaigns, education of girls, strict enforcement of the law.', '1 mark each part.'),
]
c7_long = [
    ('Draw a labelled diagram of the longitudinal section of a flower. Describe the process of fertilisation in plants and the changes that follow it.',
     'Parts: sepal, petal, stamen (anther, filament), pistil (stigma, style, ovary with ovules). Pollen lands on stigma, pollen tube grows through style to ovule; male germ cell fuses with egg to form zygote. Zygote → embryo; ovule → seed; ovary → fruit; petals, sepals, stamens, style and stigma wither.',
     '2 marks diagram; 2 marks fertilisation; 1 mark changes.'),
    ('Describe the human female reproductive system with a diagram. What happens when the egg is (a) fertilised (b) not fertilised?',
     'Ovaries (produce eggs and hormones), oviducts (egg travels; fertilisation), uterus (implantation, development), cervix, vagina. (a) Zygote implanted in uterus wall; placenta forms; foetus grows for about nine months. (b) The uterine lining breaks down and is shed as menstruation, roughly every month, lasting 2–8 days.',
     '2 marks system; 2 marks (a); 1 mark (b).'),
    ('Describe five methods of asexual reproduction with examples and diagrams. Why is vegetative propagation useful in agriculture?',
     'Binary fission (Amoeba, Leishmania), multiple fission (Plasmodium), fragmentation (Spirogyra), regeneration (Planaria), budding (Hydra, yeast), spore formation (Rhizopus), vegetative propagation (Bryophyllum, potato). Useful: early flowering and fruiting, identical plants, growing seedless plants (banana, orange, grapes).',
     '4 marks methods; 1 mark usefulness.'),
    ('What are the different methods of contraception? Explain how each works. Why should prenatal sex determination not be done?',
     'Barrier (condoms, diaphragm) – stop sperm reaching the egg and protect from STIs; hormonal (pills) – change hormonal balance so eggs are not released; copper-T/loop – placed in the uterus; surgical – vasectomy (vas deferens blocked) or tubectomy (fallopian tube blocked). Prenatal sex determination leads to female foeticide and a falling sex ratio; it is banned by law.',
     '4 marks methods; 1 mark sex determination.'),
]

# ======================= ch08 Heredity
TRAITS = [('height of the stem', 'tall', 'dwarf', 'T', 't'), ('seed shape', 'round', 'wrinkled', 'R', 'r'), ('seed colour', 'yellow', 'green', 'Y', 'y'),
          ('flower colour', 'violet', 'white', 'V', 'v'), ('pod colour', 'green', 'yellow', 'G', 'g')]
c8s1_defs = [
    ('heredity', 'the transmission of characters (traits) from parents to their offspring'),
    ('a trait', 'a characteristic of an organism, such as height or eye colour'),
    ('an inherited trait', 'a trait passed from parents to offspring through genes'),
    ('an acquired trait', 'a trait developed during an individual\'s lifetime that is not passed on to offspring'),
    ('variation', 'differences among the individuals of a species'),
]
c8s1_cats = {
    'an inherited trait': ['colour of the eyes', 'free or attached earlobes', 'blood group', 'curly hair', 'natural skin colour'],
    'an acquired trait': ['a scar from an injury', 'ability to swim', 'muscles built by exercise', 'knowledge of English', 'a tanned skin from sunlight'],
}
c8s1_mc = [
    ('Variation is greatest in organisms produced by:', 'sexual reproduction', 'asexual reproduction', 'binary fission', 'budding'),
    ('Which of these traits is inherited?', 'free earlobes', 'a cut on the finger', 'learning to dance', 'a broken tooth'),
    ('Acquired traits are not passed on to offspring because:', 'they do not change the DNA of germ cells', 'they are harmful', 'they are rare', 'they are dominant'),
    ('In a population of bacteria produced by fission, variation is:', 'very little', 'very high', 'absent always', 'equal to sexual reproduction'),
]
c8s1_why = [
    ('Why is the variation in asexually reproducing organisms less than in sexually reproducing ones?', 'Asexual reproduction has one parent and only minor DNA copying errors; sexual reproduction combines DNA of two parents.', '2 marks.'),
    ('Why are traits acquired during a lifetime not inherited?', 'They are changes in body (somatic) cells, not in the DNA of germ cells, so they cannot be passed to offspring.', '2 marks.'),
]
c8s1_ar = [
    ('A wrestler\'s strong muscles are not inherited by his children.', 'Acquired traits do not change the DNA of germ cells.', 'a', 'R explains A.'),
    ('Sexual reproduction produces more variation than asexual reproduction.', 'It combines the DNA of two parents.', 'a', 'R explains A.'),
    ('Earlobe type is an acquired trait.', 'Earlobe type is controlled by genes.', 'd', 'A is false; R is true.'),
]

c8s2_defs = [
    ('a gene', 'a section of DNA that provides information for one protein and controls a trait'),
    ('a dominant trait', 'a trait that expresses itself in the F1 generation even when only one copy of its gene is present'),
    ('a recessive trait', 'a trait that is hidden in the F1 generation and expresses only when two copies of its gene are present'),
    ('a monohybrid cross', 'a cross between two plants differing in one pair of contrasting traits'),
    ('a dihybrid cross', 'a cross between two plants differing in two pairs of contrasting traits'),
    ('the genotype', 'the genetic make-up of an organism, such as TT, Tt or tt'),
    ('the phenotype', 'the observable characteristic of an organism, such as tall or dwarf'),
    ('the F1 generation', 'the first generation of offspring from a cross between two parents'),
]
c8s2_mc = [
    ('In a monohybrid cross, the phenotypic ratio in the F2 generation is:', '3 : 1', '1 : 2 : 1', '9 : 3 : 3 : 1', '1 : 1'),
    ('In a monohybrid cross, the genotypic ratio in the F2 generation is:', '1 : 2 : 1', '3 : 1', '9 : 3 : 3 : 1', '2 : 1'),
    ('In a dihybrid cross, the F2 phenotypic ratio is:', '9 : 3 : 3 : 1', '3 : 1', '1 : 2 : 1', '1 : 1 : 1 : 1'),
    ('Mendel used which plant for his experiments?', 'garden pea', 'mango', 'wheat', 'rose'),
    ('A plant with genotype Tt is:', 'tall', 'dwarf', 'medium', 'cannot be said'),
    ('The appearance of round green and wrinkled yellow seeds in F2 of a dihybrid cross shows that:', 'traits are inherited independently', 'traits are blended', 'traits are lost', 'only one trait is inherited'),
]
c8s2_why = [
    ('Why did Mendel choose pea plants for his experiments?', 'They have many clear contrasting traits, a short life cycle, produce many seeds, and can be easily self- and cross-pollinated.', '1 mark each (any two).'),
    ('Why do all F1 plants of a cross between pure tall and pure dwarf plants appear tall?', 'Each F1 plant gets T from one parent and t from the other; T (tall) is dominant over t, so all are Tt and tall.', '1 mark Tt. 1 mark dominant.'),
    ('How do we know that the dwarf trait was not lost in the F1 generation?', 'Dwarf plants reappear in the F2 generation (one-fourth) when F1 plants are self-pollinated.', '2 marks.'),
]
c8s2_ar = [
    ('All F1 plants of a cross TT × tt are tall.', 'Tall is dominant over dwarf.', 'a', 'R explains A.'),
    ('Dwarf plants reappear in the F2 generation.', 'The recessive gene is passed on unchanged in F1 hybrids.', 'a', 'R explains A.'),
    ('The genotypic ratio of a monohybrid F2 is 3 : 1.', 'In a monohybrid cross, the phenotypic ratio of F2 is 3 : 1.', 'd', 'A is false (it is 1 : 2 : 1); R is true.'),
]


def c8s2_mono(r):
    tr, d, rc, D, R = r.choice(TRAITS)
    n = r.choice([400, 800, 1000, 1200, 1600, 2000])
    return {'stem': f'A pure {d} pea plant ({D}{D}) is crossed with a pure {rc} plant ({R}{R}) for {tr}. The F1 plants are self-pollinated and {n} F2 plants are obtained. How many F2 plants are expected to be {rc}? What is the F2 genotypic ratio?',
            'answer': f'{n // 4} {rc} plants; {D}{D} : {D}{R} : {R}{R} = 1 : 2 : 1',
            'key': f'F1 all {D}{R} ({d}). F2 phenotypes 3 {d} : 1 {rc}, so {rc} = {n}/4 = {n // 4}. Genotypes 1 : 2 : 1.'}


def c8s2_monoq(r):
    tr, d, rc, D, R = r.choice(TRAITS)
    n = r.choice([400, 800, 1000, 1200, 1600, 2000])
    q = r.choice(['dom', 'het', 'homodom'])
    if q == 'dom':
        a, what = 3 * n // 4, f'{d} (showing the dominant trait)'
    elif q == 'het':
        a, what = n // 2, f'heterozygous ({D}{R})'
    else:
        a, what = n // 4, f'pure {d} ({D}{D})'
    vals = {3 * n // 4, n // 2, n // 4, n}
    vals.discard(a)
    return {'stem': f'In a monohybrid cross between pure {d} and pure {rc} pea plants, {n} F2 plants are produced. How many are expected to be {what}?', 'answer': str(a),
            'key': f'F2: {D}{D} : {D}{R} : {R}{R} = 1 : 2 : 1 ({n // 4} : {n // 2} : {n // 4}); {d} = {3 * n // 4}.', 'distractors': [str(v) for v in sorted(vals)]}


def c8s2_di(r):
    (t1, d1, r1, D1, R1), (t2, d2, r2, D2, R2) = r.sample(TRAITS[:4], 2)
    n = r.choice([160, 320, 480, 640, 800, 1600])
    k = n // 16
    return {'stem': f'Pure {d1} {d2} pea plants are crossed with pure {r1} {r2} plants. If {n} F2 plants are obtained, how many of each phenotype are expected?',
            'answer': f'{d1} {d2}: {9 * k}; {d1} {r2}: {3 * k}; {r1} {d2}: {3 * k}; {r1} {r2}: {k}',
            'key': f'F2 ratio 9 : 3 : 3 : 1; {n}/16 = {k}; so {9 * k}, {3 * k}, {3 * k}, {k}.'}


def c8s2_testx(r):
    tr, d, rc, D, R = r.choice(TRAITS)
    het = r.random() < 0.5
    n = r.choice([40, 60, 80, 100, 120])
    res = f'about {n // 2} {d} and {n // 2} {rc}' if het else f'all {n} {d}'
    return {'stem': f'A {d} pea plant of unknown genotype is crossed with a {rc} plant ({R}{R}) and gives {res} plants. What is the genotype of the {d} plant? Explain.',
            'answer': f'{D}{R}' if het else f'{D}{D}', 'key': ('A 1 : 1 ratio means the plant gave both ' + D + ' and ' + R + ' gametes: heterozygous.' if het else 'No recessive offspring means the plant gave only ' + D + ' gametes: homozygous dominant.')}


c8s3_defs = [
    ('a chromosome', 'a thread-like structure in the nucleus made of DNA and protein that carries genes'),
    ('an enzyme', 'a protein that speeds up a chemical reaction in the body'),
    ('a gamete (germ cell)', 'a reproductive cell with a single set of chromosomes'),
    ('an allele', 'one of the two forms of a gene, such as T or t'),
]
c8s3_mc = [
    ('A gene for tallness in pea plants controls height by making:', 'an enzyme that produces a growth hormone', 'more leaves', 'more water', 'a sugar'),
    ('Human body cells have how many chromosomes?', '46 (23 pairs)', '23', '44', '92'),
    ('Germ cells in humans contain:', '23 chromosomes (one set)', '46 chromosomes', '22 chromosomes', '44 chromosomes'),
    ('Each gene set is present in a cell as:', 'separate independent pieces called chromosomes', 'one long thread only', 'mitochondria', 'cell membrane'),
    ('If the enzyme that makes a plant hormone works efficiently, the plant will be:', 'tall', 'dwarf', 'without flowers', 'without roots'),
]
c8s3_why = [
    ('How do genes control the characteristics of an organism? Explain using plant height.', 'A gene codes for a protein (enzyme); in pea plants the enzyme makes a growth hormone; an efficient enzyme gives more hormone and a tall plant, while a less efficient one gives a dwarf plant.', '1 mark gene → protein. 1 mark hormone → height.'),
    ('How is the equal genetic contribution of male and female parents ensured in the progeny?', 'Each parent contributes one germ cell with one set of chromosomes; the zygote gets one set from each, restoring the normal number.', '2 marks.'),
]
c8s3_ar = [
    ('Germ cells contain only one set of chromosomes.', 'At fertilisation, the original number of chromosomes is restored in the zygote.', 'a', 'R explains A.'),
    ('Genes control traits by making proteins.', 'Proteins such as enzymes and hormones control body processes.', 'a', 'R explains A.'),
    ('Body cells of humans have 23 chromosomes.', 'Germ cells of humans have 23 chromosomes.', 'd', 'A is false (46); R is true.'),
]


def c8s3_chromo(r):
    org = r.choice([('humans', 46), ('dogs', 78), ('rice', 24), ('onion', 16), ('pea', 14), ('fruit fly', 8), ('cats', 38)])
    n, c = org
    return {'stem': f'Body cells of {n} contain {c} chromosomes. How many chromosomes are present in their gametes and in the zygote? Explain.',
            'answer': f'Gametes {c // 2}; zygote {c}', 'key': f'Gametes have one set ({c // 2}); fertilisation of two gametes restores {c} in the zygote.'}


c8s4_defs = [
    ('sex chromosomes', 'the pair of chromosomes (X and Y) that decides the sex of a person'),
    ('autosomes', 'the chromosomes other than the sex chromosomes'),
    ('sex determination', 'the process by which the sex of an individual is fixed'),
]
c8s4_mc = [
    ('Women have a pair of sex chromosomes:', 'XX', 'XY', 'YY', 'XO'),
    ('The sex of a child is determined by:', 'whether the father\'s sperm carries an X or a Y chromosome', 'the mother', 'the food eaten', 'the season'),
    ('In some reptiles, sex is determined by:', 'the temperature at which the eggs are incubated', 'X and Y chromosomes only', 'the father', 'food'),
    ('A snail can change sex. This shows that sex determination is:', 'not always genetic', 'always by chromosomes', 'by temperature only', 'by the mother'),
    ('The chance of a child being a boy is:', '50%', '25%', '75%', '100%'),
]
c8s4_why = [
    ('Why is the father responsible for the sex of the child?', 'All eggs carry X; sperms carry X or Y. An X-sperm gives a girl (XX), a Y-sperm gives a boy (XY).', '1 mark each.'),
    ('Why is the probability of a boy or a girl about 50% in each birth?', 'Half the sperms carry X and half carry Y, and each has an equal chance of fertilising the egg.', '2 marks.'),
]
c8s4_ar = [
    ('The sex of a child is decided by the father.', 'Sperms carry either an X or a Y chromosome, while all eggs carry X.', 'a', 'R explains A.'),
    ('A couple has three daughters. The fourth child is more likely to be a son.', 'Each birth has an equal chance of a boy or girl.', 'd', 'A is false (each birth is independent, 50%); R is true.'),
    ('In turtles, the sex of the young can depend on temperature.', 'Sex determination is not genetic in all animals.', 'a', 'R explains A.'),
]


def c8s4_prob(r):
    k = r.choice([1, 2, 3])
    nm = name(r)
    return {'stem': f'{nm}\'s parents already have {k} daughter{"s" if k > 1 else ""}. What is the probability that their next child will be a son? Explain using the sex chromosomes.',
            'answer': '50% (1/2)', 'key': 'Mother gives X; father gives X or Y with equal chance; each birth is independent of earlier ones, so P(son, XY) = 1/2.'}


c8_hots = [
    ('A cross between a tall plant with round seeds and a dwarf plant with wrinkled seeds gives all tall, round plants in F1. What can you conclude? What proportion of F2 plants would be dwarf with wrinkled seeds?', 'Tall and round are dominant. F2 gives 9 : 3 : 3 : 1, so 1/16 are dwarf wrinkled.', '1 mark dominance. 1 mark ratio. 1 mark 1/16.'),
    ('A man with blood group A marries a woman with blood group O, and their daughter has blood group O. Is this enough to tell whether the A or the O trait is dominant? Why or why not?', 'No. The daughter could get O from both parents if the father is heterozygous (AO); with one family we cannot test dominance — more data are needed (actually A is dominant over O).', '1 mark no. 1 mark heterozygous father. 1 mark more data.'),
    ('Mendel crossed pure violet-flowered and pure white-flowered pea plants. All F1 plants had violet flowers. When F1 plants were crossed with white-flowered plants, half the offspring were white. Explain with a cross.', 'Violet (V) is dominant. F1: Vv. Vv × vv → Vv (violet) : vv (white) = 1 : 1.', '1 mark dominance. 1 mark F1. 1 mark test cross.'),
    ('How does the creation of variations in a species promote survival, using the example of a population of red beetles that produces a green variant in green bushes?', 'Crows easily see red beetles on green leaves and eat them; green variants are hidden, survive and reproduce, so the proportion of green beetles increases.', '1 mark variation. 1 mark selection. 1 mark survival.'),
]
c8_case = [
    ('Read: Mendel crossed pure tall (TT) pea plants with pure dwarf (tt) plants. All F1 plants were tall. He then self-pollinated the F1 plants and got 1064 F2 plants: 787 tall and 277 dwarf.\n'
     '(i) Which trait is dominant? (ii) What is the genotype of F1 plants? (iii) Calculate the approximate ratio of tall to dwarf in F2. (iv) What will be the genotypes of the tall F2 plants?',
     '(i) Tall. (ii) Tt. (iii) 787 : 277 ≈ 2.84 : 1, about 3 : 1. (iv) TT and Tt (in the ratio 1 : 2).', '1 mark each part.'),
    ('Read: In a hospital in Lucknow, a woman is blamed by her in-laws for giving birth to three daughters in a row.\n'
     '(i) What are the sex chromosomes in a woman and a man? (ii) Who decides the sex of the child? (iii) What is the probability of a son in the fourth birth? (iv) Show the inheritance with a simple cross.',
     '(i) Woman XX; man XY. (ii) The father. (iii) 50%. (iv) XX × XY → XX, XY, XX, XY: half girls, half boys.', '1 mark each part.'),
]
c8_long = [
    ('Describe Mendel\'s monohybrid cross between tall and dwarf pea plants up to the F2 generation with a checkerboard. Write the phenotypic and genotypic ratios and the conclusions drawn.',
     'P: TT × tt; gametes T and t; F1: all Tt (tall). F1 selfed: Tt × Tt; gametes T, t from each; F2: TT, Tt, Tt, tt. Phenotype 3 tall : 1 dwarf; genotype 1 TT : 2 Tt : 1 tt. Conclusions: traits are controlled by factors (genes) in pairs; one is dominant; recessive factors are not lost and reappear in F2.',
     '2 marks cross; 2 marks ratios; 1 mark conclusions.'),
    ('Describe Mendel\'s dihybrid cross between round yellow and wrinkled green seeded pea plants. What is the F2 ratio, and what does it show?',
     'P: RRYY × rryy; F1: RrYy (round yellow). F1 selfed gives 16 combinations: 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green. It shows that the two traits are inherited independently (new combinations appear).',
     '2 marks cross; 2 marks ratio; 1 mark conclusion.'),
    ('How is sex determined in humans? Show with a flow chart. Explain why the statement "the mother decides the sex of the child" is wrong. How is sex determined in some other animals?',
     'Women XX, men XY. Eggs all X; sperms X or Y. X sperm + X egg → XX girl; Y sperm + X egg → XY boy; each 50%. So the father\'s sperm decides. In some reptiles, temperature of incubation; snails can change sex.',
     '2 marks mechanism; 1 mark flow chart; 1 mark explanation; 1 mark other animals.'),
]


FAMILIES = {
    S + '05-st1': [TERM(c5s1_defs), DEF(c5s1_defs), CLS(c5s1_mode, 'Which of these organisms shows {}?', C='C2', D='D2', verb='shows'), CLS(c5s1_enz, 'Which of these describes {}?', C='C1', D='D2', verb='describes', neg=False),
                   MC(c5s1_mc, C='C1', D='D2'), SA(c5s1_why), ARF(c5s1_ar), G('C3', 'D3', 'explain', c5s1_ord), SORT(c5s1_mode, 'Classify these organisms by {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2)),
                   SA(c5_hots[:2], C='C4', D='D4', type='multi_step'), CASE(c5_case[2:], C='C4', D='D3'), LONG(c5_long[:1], C='C4', D='D4'),
                   CLS(c5s1_mode, 'Which of these organisms shows {}?', C='C4', D='D3', neg=True, neg_tpl='Which of these organisms does NOT show {}?', verb='shows')],
    S + '05-st2': [TERM(c5s2_defs), DEF(c5s2_defs), CLS(c5s2_cats, 'Which of these is a feature of {}?', C='C2', D='D2', verb='is a feature of'), MC(c5s2_mc, C='C1', D='D2'), SA(c5s2_why), ARF(c5s2_ar),
                   G('C3', 'D3', 'explain', c5s2_ord), G('C3', 'D2', 'numerical', c5s2_breath),
                   SORT(c5s2_cats, 'Sort these features into {A} and {B}: {L}.', C='C3', D='D3', n=(2, 3)), SA(c5_hots[2:3], C='C4', D='D4', type='multi_step'), CASE(c5_case[1:2], C='C4', D='D3'),
                   LONG(c5_long[3:], C='C4', D='D4')],
    S + '05-st3': [TERM(c5s3_defs), DEF(c5s3_defs), CLS(c5s3_cats, 'Which of these carries {}?', C='C2', D='D2', verb='carries'), CLS(c5s3_vt, 'Which of these is {}?', C='C1', D='D2'), MC(c5s3_mc, C='C1', D='D2'),
                   SA(c5s3_why), ARF(c5s3_ar), G('C3', 'D3', 'explain', c5s3_ord), G('C3', 'D2', 'numerical', c5s3_co), SORT(c5s3_cats, 'Classify these as carrying {A} or {B}: {L}.', C='C3', D='D3'),
                   SA(c5_hots[3:], C='C4', D='D4', type='multi_step'), LONG(c5_long[1:2], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c5s3_ord)],
    S + '05-st4': [TERM(c5s4_defs), DEF(c5s4_defs), CLS(c5s4_organ, 'Which of these is {}?', C='C1', D='D1', verb='is'), MC(c5s4_mc, C='C1', D='D2'), SA(c5s4_why), ARF(c5s4_ar),
                   G('C3', 'D3', 'numerical', c5s4_reab), CASE(c5_case[:1], C='C4', D='D3'), LONG(c5_long[2:3], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c5s4_reab)],
    S + '06-st1': [TERM(c6s1_defs), DEF(c6s1_defs), CLS(c6s1_brain, 'Which of these is {}?', C='C2', D='D2'), CLS(c6s1_vol, 'Which of these is {}?', C='C1', D='D2'), MC(c6s1_mc, C='C1', D='D2'),
                   SA(c6s1_why), ARF(c6s1_ar), G('C3', 'D3', 'explain', c6s1_ord), SORT(c6s1_vol, 'Classify these as {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2)), SORT(c6s1_brain, 'Sort these functions into those {A} and those {B}: {L}.', C='C3', D='D3', n=(1, 2)),
                   SA(c6_hots[:1] + c6_hots[2:3], C='C4', D='D4', type='multi_step'), CASE(c6_case[:1], C='C4', D='D3'), LONG(c6_long[:2], C='C4', D='D4'),
                   CLS(c6s1_vol, 'Which of these is {}?', C='C4', D='D3', neg=True)],
    S + '06-st2': [TERM(c6s2_defs), DEF(c6s2_defs), CLS(c6s2_hor, 'Which of these describes {}?', C='C2', D='D2', verb='describes'), CLS(c6s2_trop, 'Which of these is {}?', C='C1', D='D2'), MC(c6s2_mc, C='C1', D='D2'),
                   SA(c6s2_why), ARF(c6s2_ar), SORT(c6s2_trop, 'Classify these responses as {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2)), SA(c6_hots[1:2], C='C4', D='D4', type='multi_step'), CASE(c6_case[1:], C='C4', D='D3')],
    S + '06-st3': [TERM(c6s3_defs), DEF(c6s3_defs), CLS(c6s3_gland, 'Which hormone is {}?', C='C1', D='D2'), CLS(c6s3_fn, 'Which hormone is {}?', C='C2', D='D2'), MC(c6s3_mc, C='C1', D='D2'),
                   SA(c6s3_why), ARF(c6s3_ar), G('C3', 'D3', 'explain', c6s3_match), SA(c6_hots[3:], C='C4', D='D4', type='multi_step'), LONG(c6_long[2:], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c6s3_match)],
    S + '07-st1': [TERM(c7s1_defs), DEF(c7s1_defs), MC(c7s1_mc, C='C1', D='D2'), SA(c7s1_why), ARF(c7s1_ar), SA(c7_hots[2:3], C='C4', D='D4', type='multi_step'),
                   SA([('A population of bacteria in a pond includes some that can survive at 40 °C. If the pond heats up in summer, what will happen to the population, and why?', 'Most bacteria die, but the heat-resistant variants survive and reproduce, so the population that remains is mainly heat-resistant.', '1 mark most die. 1 mark variants survive. 1 mark population changes.')], C='C3', D='D3', type='multi_step')],
    S + '07-st2': [TERM(c7s2_defs), DEF(c7s2_defs), CLS(c7s2_cats, 'Which of these organisms reproduces by {}?', C='C2', D='D2', verb='reproduces by'), MC(c7s2_mc, C='C1', D='D2'), SA(c7s2_why), ARF(c7s2_ar),
                   SORT(c7s2_cats, 'Group these organisms by mode of reproduction, {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2)), SA(c7_hots[:1], C='C4', D='D4', type='multi_step'), CASE(c7_case[:1], C='C4', D='D3'),
                   LONG(c7_long[2:3], C='C4', D='D4'), CLS(c7s2_cats, 'Which of these organisms reproduces by {}?', C='C4', D='D3', neg=True, neg_tpl='Which of these organisms does NOT reproduce by {}?', verb='reproduces by')],
    S + '07-st3': [TERM(c7s3_defs), DEF(c7s3_defs), CLS(c7s3_parts, 'Which of these is {}?', C='C1', D='D1'), MC(c7s3_mc, C='C1', D='D2'),
                   SA(c7s3_why), ARF(c7s3_ar), G('C3', 'D3', 'explain', c7s3_ord), SORT(c7s3_parts, 'Classify these as {A} or {B}: {L}.', C='C3', D='D2', n=(1, 3)), SA(c7_hots[3:], C='C4', D='D4', type='multi_step'),
                   LONG(c7_long[:1], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c7s3_ord)],
    S + '07-st4': [TERM(c7s4_defs), DEF(c7s4_defs), CLS(c7s4_male, 'Which of these is {}?', C='C1', D='D1'), CLS(c7s4_con, 'Which of these is {} of contraception?', C='C2', D='D2'),
                   MC(c7s4_mc, C='C1', D='D2'), SA(c7s4_why), ARF(c7s4_ar), G('C3', 'D3', 'explain', c7s4_ord), SORT(c7s4_male, 'Classify these as {A} or {B}: {L}.', C='C3', D='D2'),
                   SA(c7_hots[1:2], C='C4', D='D4', type='multi_step'), CASE(c7_case[1:], C='C4', D='D3'), LONG(c7_long[1:2] + c7_long[3:], C='C4', D='D4')],
    S + '08-st1': [TERM(c8s1_defs), DEF(c8s1_defs), CLS(c8s1_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c8s1_mc, C='C1', D='D2'), SA(c8s1_why), ARF(c8s1_ar),
                   SORT(c8s1_cats, 'Classify these traits as {A} or {B}: {L}.', C='C3', D='D2'), SA(c8_hots[3:], C='C4', D='D4', type='multi_step'),
                   CLS(c8s1_cats, 'Which of the following is {}?', C='C3', D='D3', neg=True)],
    S + '08-st2': [TERM(c8s2_defs), DEF(c8s2_defs), MC(c8s2_mc, C='C1', D='D2'), SA(c8s2_why), ARF(c8s2_ar), G('C3', 'D3', 'numerical', c8s2_mono), G('C2', 'D2', 'mcq', c8s2_monoq),
                   G('C3', 'D4', 'multi_step', c8s2_di), G('C3', 'D3', 'explain', c8s2_testx), G('C4', 'D4', 'multi_step', c8s2_testx), SA(c8_hots[:1] + c8_hots[2:3], C='C4', D='D4', type='multi_step'),
                   CASE(c8_case[:1], C='C4', D='D3'), LONG(c8_long[:2], C='C4', D='D4'), G('C4', 'D3', 'mcq', c8s2_monoq)],
    S + '08-st3': [TERM(c8s3_defs), DEF(c8s3_defs), MC(c8s3_mc, C='C1', D='D2'), SA(c8s3_why), ARF(c8s3_ar), G('C3', 'D2', 'explain', c8s3_chromo), SA(c8_hots[1:2], C='C4', D='D4', type='multi_step')],
    S + '08-st4': [TERM(c8s4_defs + c8s3_defs[:2]), DEF(c8s4_defs), MC(c8s4_mc, C='C1', D='D2'), SA(c8s4_why), ARF(c8s4_ar), G('C3', 'D2', 'explain', c8s4_prob), CASE(c8_case[1:], C='C4', D='D3'),
                   LONG(c8_long[2:], C='C4', D='D4')],
}
