"""CBSE class 9 science families, chapters 1-4 (Cell; Tissues in Action; Describing Motion; Mixtures and Separation)."""
from __future__ import annotations

import math

from qbank import name, two_names, num, num_distractors, mcq
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, cap, sig

S = 'cbse-g9-science-ch'

# ======================= ch01 Cell
c1s1_defs = [
    ('the cell theory', 'the theory that all living organisms are made of cells, the cell is the basic unit of life, and all cells arise from pre-existing cells'),
    ('a cell', 'the structural and functional unit of life'),
    ('protoplasm', 'the living substance of the cell, consisting of the cytoplasm and the nucleus'),
    ('a compound microscope', 'a microscope with two sets of lenses (objective and eyepiece) used to observe cells'),
]
c1s1_sci = [
    ('Robert Hooke', 'observed cells in a thin slice of cork in 1665 and coined the term "cell"'),
    ('Antonie van Leeuwenhoek', 'first observed free-living cells in pond water with an improved microscope in 1674'),
    ('Robert Brown', 'discovered the nucleus in the cell in 1831'),
    ('Purkinje', 'coined the term "protoplasm" for the fluid substance of the cell in 1839'),
    ('Schleiden and Schwann', 'proposed that all plants and animals are composed of cells (cell theory, 1838–39)'),
    ('Rudolf Virchow', 'expanded the cell theory by suggesting that all cells arise from pre-existing cells (1855)'),
]


def c1s1_who(r):
    n, d = r.choice(c1s1_sci)
    return mcq(f'Which scientist {d}?', n, r.sample([x[0] for x in c1s1_sci if x[0] != n], 3), f'{n} {d}.', r)


c1s1_mc = [
    ('The cells in cork observed by Robert Hooke were:', 'dead cells with only cell walls', 'living cells with nuclei', 'animal cells', 'bacteria'),
    ('Which statement is part of the cell theory?', 'New cells arise from pre-existing cells', 'All cells contain chloroplasts', 'Viruses are made of cells', 'Cells arise from non-living matter'),
    ('The invention of which instrument made the discovery of cells possible?', 'The microscope', 'The telescope', 'The thermometer', 'The barometer'),
]
c1s1_why = [
    ('Why is the cell called the structural and functional unit of life?', 'All organisms are built of cells (structure), and every life process such as respiration, nutrition and excretion takes place in cells (function).', '1 mark: structure. 1 mark: function.'),
    ('Why did Hooke see only empty boxes in cork?', 'Cork is made of dead cells; only the cell walls remain, without cytoplasm or nucleus.', '1 mark: dead cells. 1 mark: only walls remain.'),
]
c1s1_ar = [
    ('All cells arise from pre-existing cells.', 'This idea was added to the cell theory by Rudolf Virchow.', 'b', 'Both true; R gives the history, not the reason.'),
    ('Viruses are an exception to the cell theory.', 'Viruses are not made of cells.', 'a', 'R explains A.'),
    ('Robert Hooke saw nuclei in cork cells.', 'Cork cells are dead.', 'd', 'A false; R true.'),
]
c1s1_hots = [
    ('Why are viruses not considered to fit the cell theory, and why do they still interest biologists?', 'They are not made of cells and cannot reproduce outside a host cell; but inside cells they reproduce using the cell\'s machinery, showing a property of life.', '1 mark: not cellular. 1 mark: reproduce only in host. 1 mark: link to life.'),
    ('How did improvements in lenses change biology between Hooke (1665) and Brown (1831)?', 'Better lenses gave higher magnification and clearer images, allowing observation of living cells, single-celled organisms and finally the nucleus, which led to the cell theory.', '1 mark per valid link (max 3).'),
]

c1s2_defs = [
    ('diffusion', 'the spontaneous movement of a substance from a region of higher concentration to a region of lower concentration'),
    ('osmosis', 'the movement of water molecules through a selectively permeable membrane from a region of higher water concentration to a region of lower water concentration'),
    ('a selectively permeable membrane', 'a membrane that allows only some substances to pass through it'),
    ('a hypotonic solution', 'a solution outside the cell with a higher water concentration than the cell, so the cell gains water'),
    ('a hypertonic solution', 'a solution outside the cell with a lower water concentration than the cell, so the cell loses water'),
    ('an isotonic solution', 'a solution with the same water concentration as the cell, so there is no net movement of water'),
    ('plasmolysis', 'the shrinkage of the cytoplasm away from the cell wall when a plant cell loses water by osmosis'),
    ('endocytosis', 'the process by which the flexible plasma membrane engulfs food and other material from outside, as in Amoeba'),
]
c1s2_sol = {
    'a hypotonic solution': ['distilled water', 'rain water', 'tap water (very dilute)'],
    'a hypertonic solution': ['concentrated salt solution', 'strong sugar syrup', 'brine'],
}


def c1s2_predict(r):
    obj = r.choice([('a raisin', 'swells'), ('a deshelled egg', 'swells'), ('a slice of potato', 'becomes firm (gains water)'), ('red onion peel cells', 'become turgid')])
    sol, eff = r.choice([('distilled water', 'gain'), ('concentrated salt solution', 'lose')])
    effect = {'gain': obj[1], 'lose': 'shrinks / becomes limp (loses water)'}[eff]
    return {'stem': f'Predict what happens when {obj[0]} is kept in {sol} for some hours. Explain using osmosis.',
            'answer': f'It {effect}.',
            'key': f'{cap(sol)} is {"hypotonic" if eff == "gain" else "hypertonic"} to the cells, so water moves {"into" if eff == "gain" else "out of"} them by osmosis through the selectively permeable membrane (1 + 1 marks).'}


c1s2_mc = [
    ('Carbon dioxide produced in cells moves out into the surroundings by:', 'diffusion', 'osmosis', 'endocytosis', 'active transport only'),
    ('When a plant cell is placed in a hypertonic solution, it:', 'loses water and undergoes plasmolysis', 'gains water and bursts', 'remains unchanged', 'gains water and becomes turgid'),
    ('An animal cell placed in distilled water will most likely:', 'swell and may burst', 'shrink', 'stay the same', 'form a cell wall'),
    ('The cell wall of plants is mainly made of:', 'cellulose', 'chitin', 'lipids', 'proteins'),
    ('The plasma membrane is made of:', 'lipids and proteins', 'cellulose only', 'starch', 'DNA'),
    ('The cell wall of fungi is made of:', 'chitin', 'cellulose', 'peptidoglycan only', 'lignin'),
]
c1s2_why = [
    ('Why do plant cells not burst in fresh water, while animal cells may?', 'The rigid cell wall of plant cells resists the pressure of water entering; animal cells have only a thin, flexible membrane.', '1 mark: rigid wall. 1 mark: no wall in animal cells.'),
    ('Why is salt sprinkled on leeches or slugs to make them fall off?', 'The salt forms a hypertonic solution on their moist skin; water leaves their cells by osmosis and they shrivel.', '1 mark: hypertonic. 1 mark: water loss.'),
    ('Why do raisins swell when soaked in water?', 'Water is more concentrated outside; it enters the raisin cells by osmosis.', '1 mark: higher water concentration outside. 1 mark: osmosis.'),
    ('Why is the plasma membrane called selectively permeable?', 'It allows some substances such as water, oxygen and carbon dioxide to pass but prevents others.', '1 mark: allows some. 1 mark: blocks others.'),
]
c1s2_ar = [
    ('A dried raisin swells when placed in water.', 'Water moves into the raisin by osmosis.', 'a', 'R explains A.'),
    ('Plasmolysis occurs when a plant cell is placed in a hypotonic solution.', 'In a hypotonic solution the cell gains water.', 'd', 'A false: plasmolysis occurs in a hypertonic solution; R true.'),
    ('Plant cells can withstand very dilute external media.', 'The cell wall prevents the cell from bursting.', 'a', 'R explains A.'),
    ('Amoeba takes in food by endocytosis.', 'The plasma membrane of Amoeba is flexible.', 'a', 'R explains A.'),
]
c1s2_hots = [
    ('Pickles and jams do not spoil easily. Use the idea of osmosis to explain why.', 'High salt or sugar makes a hypertonic medium; any microbe on the food loses water by osmosis and cannot grow.', '1 mark: hypertonic. 1 mark: microbe dehydrates.'),
    ('A gardener over-fertilises a pot so that the soil water becomes very concentrated. The plant wilts though it is watered. Explain.', 'The soil solution becomes hypertonic to root cells, so water moves out of the roots by osmosis instead of in; the plant loses water and wilts.', '1 mark: hypertonic soil. 1 mark: water leaves roots. 1 mark: wilting.'),
    ('Design an experiment with potato cups to show osmosis. Include a control.', 'Make three hollow potato cups in water troughs: A empty, B with sugar, C boiled potato with sugar. After some hours water rises in B only; A shows no change (control), C shows none because boiled cells are dead.', '1 mark: set-up. 1 mark: control(s). 1 mark: result and conclusion.'),
]

c1s3_org = [
    ('nucleus', 'controls the activities of the cell and contains chromosomes'),
    ('mitochondria', 'release energy from food in the form of ATP, and are called the powerhouses of the cell'),
    ('plastids (chloroplasts)', 'contain chlorophyll and carry out photosynthesis'),
    ('endoplasmic reticulum (ER)', 'is a network of membrane-bound tubes that transports materials; the rough type makes proteins'),
    ('Golgi apparatus', 'packages and dispatches materials made in the cell, and forms lysosomes'),
    ('lysosomes', 'contain digestive enzymes that break down worn-out cell parts and foreign material'),
    ('vacuoles', 'store cell sap and give turgidity to plant cells'),
    ('ribosomes', 'are the sites of protein synthesis'),
]


def c1s3_fn(r):
    o, f = r.choice(c1s3_org)
    wrong = r.sample([x[0] for x in c1s3_org if x[0] != o], 3)
    return mcq(f'Which cell organelle {f}?', o, wrong, f'The {o} {f}.', r)


def c1s3_rev(r):
    o, f = r.choice(c1s3_org)
    wrong = r.sample([x[1] for x in c1s3_org if x[0] != o], 3)
    return mcq(f'What is the main function of the {o}?', cap(f), [cap(w) for w in wrong], f'The {o} {f}.', r)


c1s3_defs = [
    ('chromosomes', 'thread-like structures in the nucleus made of DNA and protein that carry genetic information'),
    ('a gene', 'a functional segment of DNA that carries information for a characteristic'),
    ('suicide bags', 'a name for lysosomes, because they can digest their own cell when it is damaged'),
    ('the powerhouse of the cell', 'a name for mitochondria, because they release energy from food'),
    ('membrane biogenesis', 'the making of new cell membrane, using proteins and lipids made by the ER'),
]
c1s3_mc = [
    ('Which organelles have their own DNA and ribosomes?', 'Mitochondria and plastids', 'Golgi and lysosomes', 'ER and vacuoles', 'Lysosomes and ribosomes'),
    ('Which organelle is NOT bound by a membrane?', 'Ribosome', 'Mitochondrion', 'Lysosome', 'Golgi apparatus'),
    ('Leucoplasts are plastids that:', 'store starch, oils and proteins', 'contain chlorophyll', 'make proteins', 'digest worn-out organelles'),
    ('The Golgi apparatus was first described by:', 'Camillo Golgi', 'Robert Brown', 'Robert Hooke', 'Rudolf Virchow'),
    ('Detoxification of many poisons and drugs in liver cells occurs in the:', 'smooth endoplasmic reticulum', 'ribosomes', 'nucleus', 'vacuole'),
]
c1s3_why = [
    ('Why are lysosomes called suicide bags?', 'When a cell is damaged, its lysosomes may burst and their enzymes digest the cell itself.', '1 mark: enzymes. 1 mark: digest own cell.'),
    ('Why are mitochondria more numerous in muscle cells?', 'Muscle cells do a lot of work and need much energy; mitochondria release that energy as ATP.', '1 mark: high energy need. 1 mark: ATP.'),
    ('Why are vacuoles larger in plant cells than in animal cells?', 'Plant vacuoles store cell sap, water and wastes and keep the cell turgid and rigid; animal cells rely less on this.', '1 mark: storage. 1 mark: turgidity.'),
    ('Why is the nucleus important in cell division?', 'It contains chromosomes with DNA that are copied and passed on to the daughter cells.', '1 mark: chromosomes/DNA. 1 mark: inheritance to daughters.'),
]
c1s3_ar = [
    ('Mitochondria are called the powerhouses of the cell.', 'Mitochondria release energy in the form of ATP.', 'a', 'R explains A.'),
    ('Ribosomes are found only in plant cells.', 'Ribosomes are the sites of protein synthesis.', 'd', 'A false: in all cells; R true.'),
    ('Rough ER looks rough under the electron microscope.', 'Ribosomes are attached to its surface.', 'a', 'R explains A.'),
    ('Chloroplasts are found in all plant cells.', 'Chloroplasts carry out photosynthesis.', 'd', 'A false: root and onion-bulb cells lack them; R true.'),
]
c1s3_hots = [
    ('What would happen to a cell if its Golgi apparatus stopped working?', 'Proteins and other materials made in the cell would not be packaged and dispatched; secretion would stop and new lysosomes would not form.', '1 mark: packaging stops. 1 mark: secretion/lysosomes affected.'),
    ('A cell has no nucleus. Can it divide? Give an example of such a cell and explain how it survives.', 'No, it cannot divide; mature red blood cells of mammals have no nucleus, survive about 120 days and are replaced by new cells made in the bone marrow.', '1 mark: cannot divide. 1 mark: RBC example. 1 mark: replacement.'),
    ('Explain how the ER, ribosomes and Golgi apparatus work together to make and send out a protein such as an enzyme.', 'Ribosomes on the rough ER make the protein; the ER carries it to the Golgi; the Golgi modifies and packages it into vesicles that leave the cell.', '1 mark per organelle role in sequence.'),
]

c1s4_defs = [
    ('a prokaryotic cell', 'a cell without a well-defined nucleus and without membrane-bound organelles, such as a bacterium'),
    ('a eukaryotic cell', 'a cell with a nucleus bounded by a nuclear membrane and with membrane-bound organelles'),
    ('the nucleoid', 'the poorly defined nuclear region of a prokaryotic cell containing only nucleic acids'),
    ('a multicellular organism', 'an organism made of many cells with division of labour among them'),
]
c1s4_cats = {
    'a prokaryote': ['bacteria', 'blue-green algae (cyanobacteria)', 'Lactobacillus', 'E. coli'],
    'a eukaryote': ['Amoeba', 'yeast', 'Paramecium', 'onion cell', 'human cheek cell', 'Chlamydomonas'],
}
c1s4_uni = {
    'a unicellular organism': ['Amoeba', 'Paramecium', 'Chlamydomonas', 'bacteria', 'yeast', 'Euglena'],
    'a multicellular organism': ['fungi such as mushroom', 'Hydra', 'earthworm', 'mango plant', 'human being'],
}
c1s4_mc = [
    ('Which feature is found in a prokaryotic cell?', 'Nucleoid without nuclear membrane', 'Mitochondria', 'Golgi apparatus', 'Nuclear membrane'),
    ('In a single-celled organism, the cell:', 'performs all the life functions', 'performs only respiration', 'cannot reproduce', 'depends on other cells'),
    ('Division of labour is seen in:', 'multicellular organisms', 'only bacteria', 'viruses', 'only Amoeba'),
    ('Which organelle is present in both prokaryotic and eukaryotic cells?', 'Ribosomes', 'Mitochondria', 'Endoplasmic reticulum', 'Golgi apparatus'),
]
c1s4_why = [
    ('Why can a single cell of Amoeba carry out all life processes but a single human cell cannot live alone?', 'Amoeba\'s cell does all functions itself; human cells are specialised for particular jobs and depend on other cells for food, oxygen and removal of wastes.', '1 mark: Amoeba all functions. 1 mark: human cells specialised and interdependent.'),
    ('Why are bacteria called prokaryotes?', 'Their genetic material lies in a nucleoid not enclosed by a nuclear membrane, and they lack membrane-bound organelles.', '1 mark: no nuclear membrane. 1 mark: no membrane-bound organelles.'),
]
c1s4_ar = [
    ('Bacteria are prokaryotes.', 'Bacteria lack a nuclear membrane.', 'a', 'R explains A.'),
    ('Mitochondria are present in bacteria.', 'Bacteria have membrane-bound organelles.', 'e', ''),
    ('Multicellular organisms show division of labour.', 'Different cells are specialised for different functions.', 'a', 'R explains A.'),
]
c1s4_ar[1] = ('Bacteria lack mitochondria.', 'Prokaryotic cells do not have membrane-bound organelles.', 'a', 'R explains A.')
c1_case = [
    ('Read: Students placed onion peels in three watch glasses: A with water, B with a strong salt solution and C with water after boiling the peel. After 20 minutes, under the microscope, cells in B showed the coloured contents pulled away from the cell wall; A and C cells looked normal.\n'
     '(i) Name the change seen in B. (ii) Why did it occur? (iii) What will happen if B peels are put back in water? (iv) Why did boiled peels (C) not show this change in salt solution, if tried?',
     '(i) Plasmolysis. (ii) Water left the cells by osmosis into the hypertonic salt solution. (iii) The cells regain water and become turgid (deplasmolysis). (iv) Boiling kills cells; the membrane is no longer selectively permeable, so osmosis does not occur.',
     '1 mark each.'),
    ('Read: An electron micrograph of a liver cell shows many mitochondria, much smooth ER and many lysosomes, while a pancreas cell shows a lot of rough ER and a large Golgi apparatus.\n'
     '(i) Which organelle releases energy? (ii) Why does the liver cell have much smooth ER? (iii) Why does the pancreas cell have a lot of rough ER and Golgi? (iv) Name the organelle that digests worn-out parts.',
     '(i) Mitochondria. (ii) Smooth ER helps in detoxifying poisons and drugs and making lipids, which is the liver\'s work. (iii) It makes and secretes digestive enzymes (proteins); rough ER makes them and Golgi packages and dispatches them. (iv) Lysosomes.',
     '1 mark each.'),
]
c1_long = [
    ('Describe the structure and function of any five cell organelles. Draw (describe) a labelled diagram of a plant cell showing the parts that are absent in animal cells.',
     'Nucleus (control, chromosomes); mitochondria (ATP, powerhouse); ER (transport, protein/lipid synthesis); Golgi (packaging, lysosome formation); lysosomes (digestion); plastids (photosynthesis); vacuoles (storage, turgidity). Plant cell: cell wall, plasma membrane, nucleus, large central vacuole, chloroplasts; cell wall, plastids and large vacuole are absent in animal cells.',
     '1 mark per organelle (max 3); 2 marks diagram and parts absent in animal cells.'),
    ('What is osmosis? Explain what happens when a plant cell and an animal cell are placed in hypotonic, isotonic and hypertonic solutions.',
     'Osmosis: movement of water through a selectively permeable membrane from higher to lower water concentration. Hypotonic: cells gain water; animal cell may burst, plant cell becomes turgid (wall prevents bursting). Isotonic: no net change. Hypertonic: cells lose water; animal cell shrinks, plant cell plasmolyses.',
     '1 mark definition; 4 marks for the three cases (both cell types).'),
]

# ======================= ch02 Tissues in Action
c2s1_defs = [
    ('a tissue', 'a group of cells similar in structure that work together to perform a particular function'),
    ('division of labour', 'the sharing of different functions among different groups of specialised cells in a multicellular organism'),
    ('an organ', 'a structure made of different tissues working together for a particular function'),
    ('differentiation', 'the process by which cells take up a permanent shape, size and function'),
]
c2s1_mc = [
    ('The correct order of organisation in a multicellular organism is:', 'cell → tissue → organ → organ system → organism', 'tissue → cell → organ → organism', 'organ → tissue → cell → organism', 'cell → organ → tissue → organism'),
    ('Plants have more dead supportive tissue than animals because:', 'they are stationary and need strength to stay upright', 'they move a lot', 'they do not grow', 'they have no cells'),
    ('Growth in plants is limited to certain regions because:', 'dividing (meristematic) tissue is present only there', 'all plant cells divide', 'plants do not grow', 'animals eat other parts'),
]
c2s1_why = [
    ('Why do multicellular organisms need tissues?', 'Different functions are carried out more efficiently by groups of specialised cells; tissues allow division of labour.', '1 mark: specialisation. 1 mark: efficiency.'),
    ('How is the structure of plant tissues related to the way plants live, compared with animals?', 'Plants are stationary and need support, so they have much dead supporting tissue and growth only in certain regions; animals move and need more living tissue and energy.', '1 mark: plants. 1 mark: animals.'),
]
c2s1_ar = [
    ('Multicellular organisms show division of labour.', 'Groups of cells are specialised to carry out particular functions.', 'a', 'R explains A.'),
    ('Unicellular organisms have tissues.', 'A tissue is a group of similar cells.', 'd', 'A false; R true.'),
]

c2s2_defs = [
    ('meristematic tissue', 'plant tissue made of actively dividing cells, found at growing regions'),
    ('apical meristem', 'meristem at the tips of stems and roots that increases their length'),
    ('lateral meristem (cambium)', 'meristem that increases the girth of the stem or root'),
    ('intercalary meristem', 'meristem at the base of leaves or internodes, as in grasses'),
    ('parenchyma', 'simple permanent tissue of living, thin-walled, loosely packed cells that stores food'),
    ('collenchyma', 'simple permanent tissue of living cells thickened at the corners that gives flexibility'),
    ('sclerenchyma', 'simple permanent tissue of dead cells with walls thickened by lignin that gives strength'),
    ('xylem', 'complex tissue that carries water and minerals from the roots to other parts'),
    ('phloem', 'complex tissue that carries food from the leaves to other parts of the plant'),
]
c2s2_cats = {
    'a component of xylem': ['tracheids', 'vessels', 'xylem parenchyma', 'xylem fibres'],
    'a component of phloem': ['sieve tubes', 'companion cells', 'phloem fibres', 'phloem parenchyma'],
}
c2s2_type = {
    'a simple permanent tissue': ['parenchyma', 'collenchyma', 'sclerenchyma'],
    'a complex permanent tissue': ['xylem', 'phloem'],
    'a meristematic tissue': ['apical meristem', 'cambium', 'intercalary meristem'],
}
c2s2_mc = [
    ('Which of these is the only dead component of phloem?', 'Phloem fibres', 'Sieve tubes', 'Companion cells', 'Phloem parenchyma'),
    ('Chlorenchyma is parenchyma that:', 'contains chloroplasts and makes food', 'stores air in aquatic plants', 'is dead', 'carries water'),
    ('Aerenchyma helps aquatic plants to:', 'float, because of large air cavities', 'conduct food', 'grow in length', 'make seeds'),
    ('The husk of a coconut is made of:', 'sclerenchyma', 'parenchyma', 'collenchyma', 'xylem'),
    ('The leaf stalk of many plants bends without breaking because of:', 'collenchyma', 'sclerenchyma', 'xylem', 'cork'),
    ('Stomata are surrounded by:', 'two guard cells', 'companion cells', 'sieve tubes', 'cork cells'),
    ('The tissue that protects older stems, made of dead cells with suberin, is:', 'cork', 'parenchyma', 'phloem', 'meristem'),
]
c2s2_why = [
    ('Why does the grass grow back quickly after being grazed?', 'Grasses have intercalary meristems at the base of leaves and internodes, which keep dividing.', '1 mark: intercalary meristem. 1 mark: location.'),
    ('Why is sclerenchyma called a dead tissue, and what is its function?', 'Its cells are dead with walls thickened by lignin and almost no internal space; it gives strength and hardness.', '1 mark: dead/lignin. 1 mark: strength.'),
    ('Why do desert plants have a thick waxy cuticle on the epidermis?', 'It reduces water loss by evaporation and protects against drying.', '1 mark: waterproof. 1 mark: reduces water loss.'),
    ('How do guard cells open and close stomata?', 'When guard cells take in water they swell and curve, opening the pore; when they lose water they become flaccid and close it.', '1 mark: swelling opens. 1 mark: losing water closes.'),
]
c2s2_ar = [
    ('Xylem conducts water in one direction only.', 'Xylem carries water from roots to leaves.', 'a', 'R explains A.'),
    ('Phloem transports food in both directions.', 'Food moves from leaves to storage organs and from storage to growing parts.', 'a', 'R explains A.'),
    ('Meristematic cells have large vacuoles.', 'Meristematic cells are actively dividing.', 'd', 'A false: they lack vacuoles; R true.'),
    ('Cork cells prevent loss of water.', 'Cork cells have suberin in their walls.', 'a', 'R explains A.'),
]
c2s2_hots = [
    ('If the tip of a growing root is cut off, the root stops growing in length but the plant may still grow thicker. Explain.', 'Removing the root tip removes the apical meristem responsible for length; lateral meristem (cambium) can still increase girth.', '1 mark: apical meristem lost. 1 mark: lateral meristem still works.'),
    ('A farmer notices that the stem of a plant has been chewed in a ring around it, removing the bark and phloem. What will happen to the roots and why?', 'Food from the leaves cannot reach the roots through phloem, so the roots starve and eventually die (girdling).', '1 mark: phloem cut. 1 mark: roots starve.'),
]

c2s3_defs = [
    ('epithelial tissue', 'the covering or protective tissue in animals, with tightly packed cells and little intercellular space'),
    ('connective tissue', 'animal tissue with cells loosely spaced in an intercellular matrix that binds and supports other tissues'),
    ('muscular tissue', 'animal tissue made of elongated cells that contract and relax to cause movement'),
    ('nervous tissue', 'animal tissue made of neurons that receive and conduct impulses'),
    ('a tendon', 'fibrous connective tissue with great strength but limited flexibility that connects muscle to bone'),
    ('a ligament', 'elastic connective tissue that connects two bones'),
    ('a neuron', 'the cell of nervous tissue with a cell body, dendrites and an axon'),
    ('plasma', 'the fluid matrix of blood in which blood cells are suspended'),
]
c2s3_ex = {
    'an epithelial tissue': ['lining of the mouth', 'outer layer of the skin', 'lining of kidney tubules', 'inner lining of the intestine'],
    'a connective tissue': ['blood', 'bone', 'cartilage', 'tendon', 'adipose tissue'],
    'a muscular tissue': ['biceps muscle', 'muscle of the heart wall', 'muscle of the stomach wall'],
    'a nervous tissue': ['brain', 'spinal cord', 'nerves'],
}
c2s3_musc = [
    ('striated (skeletal) muscle', 'voluntary, cylindrical, unbranched, multinucleate cells with light and dark bands', 'muscles of limbs'),
    ('smooth (unstriated) muscle', 'involuntary, spindle-shaped, uninucleate cells without bands', 'walls of the stomach, intestine and blood vessels'),
    ('cardiac muscle', 'involuntary, cylindrical, branched, uninucleate cells that contract rhythmically throughout life', 'heart'),
]


def c2s3_muscle(r):
    n, f, w = r.choice(c2s3_musc)
    return mcq(f'Which type of muscle is found in the {w}?', n, [x[0] for x in c2s3_musc if x[0] != n] + ['tendon'], f'{cap(n)}: {f}.', r)


def c2s3_muscle_cmp(r):
    a, b = r.sample(c2s3_musc, 2)
    return {'stem': f'Distinguish between {a[0]} and {b[0]} on the basis of structure, control and location.',
            'answer': f'{cap(a[0])}: {a[1]}; found in {a[2]}. {cap(b[0])}: {b[1]}; found in {b[2]}.',
            'key': '1 mark each: structure, voluntary/involuntary control, location.'}


c2s3_mc = [
    ('Fat is stored below the skin and between internal organs in:', 'adipose tissue', 'cartilage', 'bone', 'tendon'),
    ('Cartilage is found in the:', 'nose, ear and ends of bones', 'heart wall', 'stomach lining', 'brain'),
    ('Bone matrix is hard because it contains:', 'calcium and phosphorus compounds', 'fat', 'water only', 'cellulose'),
    ('Which blood component helps in clotting?', 'Platelets', 'Red blood cells', 'White blood cells', 'Plasma proteins only'),
    ('Ciliated columnar epithelium in the respiratory tract helps to:', 'push mucus forward and clear the passage', 'absorb food', 'make blood', 'carry impulses'),
    ('The longest cells in the human body are:', 'nerve cells', 'muscle cells', 'red blood cells', 'bone cells'),
]
c2s3_why = [
    ('Why is blood called a connective tissue?', 'It has cells (RBC, WBC, platelets) suspended in a fluid matrix (plasma) and connects different body parts by transporting materials.', '1 mark: matrix with cells. 1 mark: transport/connects.'),
    ('Why do cardiac muscles never tire, unlike skeletal muscles?', 'Cardiac muscle is specialised for rhythmic contraction and relaxation throughout life, with many mitochondria and a rich blood supply.', '1 mark: rhythmic/involuntary. 1 mark: energy supply.'),
    ('Why are epithelial cells tightly packed?', 'They form a continuous sheet that protects underlying tissues from injury, germs and drying, and controls exchange of materials.', '1 mark: continuous sheet. 1 mark: protection/exchange.'),
    ('How is the structure of a neuron suited to its function?', 'Long axon conducts impulses over long distances; branched dendrites receive signals from many cells.', '1 mark: axon. 1 mark: dendrites.'),
]
c2s3_ar = [
    ('Tendons connect muscles to bones.', 'Tendons are fibrous tissues with great strength but limited flexibility.', 'a', 'R explains why tendons suit this job.'),
    ('Smooth muscles are voluntary.', 'Smooth muscles are found in the walls of the stomach and intestine.', 'd', 'A false: involuntary; R true.'),
    ('Ligaments are elastic.', 'Ligaments connect bone to bone and allow movement at joints.', 'a', 'R explains A.'),
    ('Red blood cells carry oxygen.', 'Red blood cells contain haemoglobin.', 'a', 'R explains A.'),
]
c2s3_hots = [
    ('A cricketer tears a ligament in the knee while another tears a tendon at the ankle. Which injury affects the connection between two bones, and which between muscle and bone? Why do such injuries heal slowly?', 'Ligament: bone to bone; tendon: muscle to bone. Both are fibrous connective tissues with a poor blood supply, so repair is slow.', '1 mark each identification. 1 mark: slow healing reason.'),
    ('Why does the heart keep beating even when we are asleep, while we cannot move our arm without thinking?', 'Heart is made of involuntary cardiac muscle controlled automatically; arm muscles are voluntary skeletal muscles that act on signals from the brain.', '1 mark: cardiac involuntary. 1 mark: skeletal voluntary.'),
]

c2s4_mc = [
    ('Movement of the arm needs the working together of:', 'muscular, skeletal (bone) and nervous tissues', 'only muscular tissue', 'only xylem and phloem', 'only epithelial tissue'),
    ('Water reaches the top of a tall tree mainly through:', 'xylem vessels and tracheids', 'phloem', 'parenchyma', 'cork'),
    ('Blood transports oxygen, food and hormones; this shows the role of:', 'connective tissue in transport', 'epithelial tissue in protection', 'meristem in growth', 'cork in protection'),
]
c2s4_why = [
    ('Explain how different tissues work together when you pick up a book.', 'Nervous tissue carries the message from brain to muscles; skeletal muscles contract; tendons pull the bones; ligaments hold the joints; blood supplies oxygen and food for energy.', '1 mark: nervous. 1 mark: muscle/bone/tendon. (blood optional)'),
    ('How do xylem and phloem together support the life of a plant?', 'Xylem brings water and minerals up for photosynthesis; phloem carries the food made in leaves to all parts; together they supply raw materials and food.', '1 mark: xylem. 1 mark: phloem.'),
]
c2s4_ar = [
    ('Plants can stand upright without a skeleton.', 'Sclerenchyma and xylem give mechanical strength to plants.', 'a', 'R explains A.'),
    ('Bones alone can move the body.', 'Muscles pull on bones through tendons.', 'd', 'A false; R true.'),
]
c2s4_hots = [
    ('A runner sprints 100 m. List the tissues involved in (i) receiving the start signal, (ii) moving the legs, (iii) supplying oxygen, and explain how they are coordinated.', '(i) Nervous tissue (ears to brain). (ii) Skeletal muscle with bones, tendons and ligaments. (iii) Blood (RBC with haemoglobin) and cardiac muscle pumping it. The brain coordinates through nerves.', '1 mark each part.'),
    ('In a potted plant, the roots are in water but the leaves are drooping on a hot day. Which plant tissues are involved and what is going wrong?', 'Xylem is carrying water up, but transpiration through stomata in epidermis is faster than supply; leaf parenchyma cells lose turgidity and droop.', '1 mark: xylem. 1 mark: stomata/transpiration. 1 mark: turgidity.'),
]
c2_case = [
    ('Read: A student examined a thin section of a sunflower stem. She saw small, densely packed cells at the tip with large nuclei; in the middle, large thin-walled cells with spaces; near the corners, cells thickened at the corners; and long tubes with thick walls and no cytoplasm in bundles.\n'
     '(i) Name the tissue at the tip. (ii) Name the thin-walled cells with spaces. (iii) Which tissue provides flexibility? (iv) Which tissue are the long thick-walled tubes, and what do they carry?',
     '(i) Apical meristem. (ii) Parenchyma. (iii) Collenchyma. (iv) Xylem (vessels); water and minerals.', '1 mark each.'),
    ('Read: A blood report shows: RBC 4.1 million/mm³ (normal 4.5–5.5), WBC 14 000/mm³ (normal 4000–11 000), platelets 2.5 lakh/mm³ (normal 1.5–4.5).\n'
     '(i) Which values are outside the normal range? (ii) A high WBC count suggests what? (iii) What function of blood could be affected by the low RBC count? (iv) Which connective tissue type does blood belong to?',
     '(i) RBC (low) and WBC (high). (ii) The body is fighting an infection. (iii) Transport of oxygen (possible anaemia). (iv) A fluid connective tissue.', '1 mark each.'),
]
c2_long = [
    ('Name the four types of animal tissues. Describe the structure, location and function of any two types of connective tissue and the three types of muscle tissue.',
     'Epithelial, connective, muscular, nervous. Connective: blood (fluid matrix plasma, RBC/WBC/platelets; transport), bone (hard matrix of calcium and phosphorus; support), cartilage, tendon, ligament, adipose. Muscles: striated (voluntary, limbs), smooth (involuntary, gut walls), cardiac (involuntary, branched, heart).',
     '1 mark: four types; 2 marks: connective tissues; 2 marks: muscles.'),
    ('Differentiate between meristematic and permanent tissues. Describe the three types of simple permanent tissue and the components of xylem and phloem.',
     'Meristematic: dividing cells, dense cytoplasm, large nucleus, no vacuoles; permanent: cells have lost the ability to divide and are specialised. Parenchyma (living, thin walls, storage), collenchyma (corner thickening, flexibility), sclerenchyma (dead, lignin, strength). Xylem: tracheids, vessels, xylem parenchyma, xylem fibres. Phloem: sieve tubes, companion cells, phloem parenchyma, phloem fibres.',
     '1 mark difference; 2 marks simple tissues; 2 marks complex tissues.'),
]

# ======================= ch03 Describing Motion
c3s1_defs = [
    ('distance', 'the total length of the path travelled by an object'),
    ('displacement', 'the shortest distance from the initial to the final position of an object, with direction'),
    ('a reference point', 'a fixed point or object with respect to which the position of another object is described'),
    ('a scalar quantity', 'a quantity that has only magnitude, such as distance or speed'),
    ('a vector quantity', 'a quantity that has both magnitude and direction, such as displacement or velocity'),
]


def c3s1_rect(r):
    a, b = r.choice([(3, 4), (6, 8), (5, 12), (9, 12), (8, 15), (12, 16), (20, 21)])
    who = name(r)
    unit = r.choice(['m', 'km'])
    hyp = math.hypot(a, b)
    return {'stem': f'{who} walks {a} {unit} due east and then {b} {unit} due north. Find the distance travelled and the magnitude of the displacement.',
            'answer': f'Distance {a + b} {unit}; displacement {num(hyp)} {unit}',
            'key': f'Distance = {a} + {b} = {a + b} {unit}. Displacement = √({a}² + {b}²) = √{a * a + b * b} = {num(hyp)} {unit} (north-east of start).',
            'distractors': [f'Distance {num(hyp)} {unit}; displacement {a + b} {unit}', f'Distance {a + b} {unit}; displacement {a + b} {unit}', f'Distance {a + b} {unit}; displacement {abs(b - a)} {unit}']}


def c3s1_circle(r):
    rr = r.choice([7, 14, 21, 35, 70])
    frac_ = r.choice([('half', 0.5), ('one full', 1.0), ('one and a half', 1.5), ('a quarter of a', 0.25)])
    circ = 2 * math.pi * rr
    dist = circ * frac_[1]
    disp = {0.5: 2 * rr, 1.0: 0, 1.5: 2 * rr, 0.25: rr * math.sqrt(2)}[frac_[1]]
    return {'stem': f'An athlete runs {frac_[0]} round{"s" if frac_[1] > 1 else ""} of a circular track of radius {rr} m. Find the distance covered and the magnitude of displacement. (Take π = 22/7.)',
            'answer': f'Distance {num(2 * 22 / 7 * rr * frac_[1], 1)} m; displacement {num(disp, 1)} m',
            'key': f'Circumference = 2πr = 2 × 22/7 × {rr} = {num(2 * 22 / 7 * rr, 1)} m; distance = {frac_[1]} × that = {num(2 * 22 / 7 * rr * frac_[1], 1)} m. Displacement is the straight line from start to finish = {num(disp, 1)} m.'}


c3s1_mc = [
    ('Displacement can be zero when the distance travelled is:', 'not zero, if the object returns to its starting point', 'never more than zero', 'always zero', 'negative'),
    ('Which of these is a vector quantity?', 'Displacement', 'Distance', 'Speed', 'Time'),
    ('The magnitude of displacement is always ______ the distance travelled.', 'less than or equal to', 'greater than', 'equal to', 'twice'),
    ('A passenger sitting in a moving bus is at rest with respect to:', 'the bus', 'the trees outside', 'the road', 'a person standing at the bus stop'),
]
c3s1_why = [
    ('Why is it necessary to mention a reference point when describing motion?', 'Motion is relative: an object may be moving with respect to one object and at rest with respect to another.', '1 mark: relative. 1 mark: example or reasoning.'),
    ('Can displacement be greater than distance? Explain.', 'No. Displacement is the shortest path between two positions, so it can at most equal the distance (for straight-line motion in one direction).', '1 mark: no. 1 mark: reasoning.'),
]
c3s1_ar = [
    ('An object can have zero displacement but non-zero distance.', 'Displacement depends only on the initial and final positions.', 'a', 'R explains A.'),
    ('Distance is a vector quantity.', 'Distance has magnitude only.', 'd', 'A false; R true.'),
    ('A tree is at rest with respect to the Earth but in motion with respect to the Sun.', 'Rest and motion are relative terms.', 'a', 'R explains A.'),
]

c3s2_defs = [
    ('speed', 'the distance travelled by an object in unit time'),
    ('velocity', 'the speed of an object in a specified direction'),
    ('average speed', 'the total distance travelled divided by the total time taken'),
    ('uniform motion', 'motion in which an object covers equal distances in equal intervals of time'),
    ('non-uniform motion', 'motion in which an object covers unequal distances in equal intervals of time'),
]


def c3s2_kmh(r):
    v = r.choice([18, 36, 54, 72, 90, 108, 126, 144])
    return {'stem': f'Convert a speed of {v} km/h into m/s.', 'answer': f'{num(v * 5 / 18)} m/s',
            'key': f'1 km/h = 1000 m ÷ 3600 s = 5/18 m/s; {v} × 5/18 = {num(v * 5 / 18)} m/s.', 'distractors': [f'{num(v * 18 / 5)} m/s', f'{num(v / 3.6 * 10)} m/s', f'{num(v / 10)} m/s']}


def c3s2_avg2(r):
    d = r.choice([30, 40, 60, 80, 120])
    v1, v2 = r.choice([(30, 60), (40, 60), (20, 30), (60, 40), (30, 20), (40, 40)])
    if v1 == v2:
        v2 = 60
    who = name(r)
    t = d / v1 + d / v2
    avg = 2 * d / t
    city = r.choice(['Pune to Lonavala', 'Delhi to Meerut', 'Lucknow to Kanpur', 'Chennai to Mahabalipuram'])
    return {'stem': f'{who}\'s family drives {d} km ({city}) at {v1} km/h and returns the same distance at {v2} km/h. Find the average speed for the whole trip.',
            'answer': f'{sig(avg, 3)} km/h', 'key': f'Time = {d}/{v1} + {d}/{v2} = {sig(t, 4)} h; average speed = total distance ÷ total time = {2 * d} ÷ {sig(t, 4)} = {sig(avg, 3)} km/h (not the mean of the speeds).',
            'distractors': [f'{sig((v1 + v2) / 2, 3)} km/h', f'{sig(avg + 5, 3)} km/h', f'{sig(v1 * v2 / 10, 3)} km/h'], 'gap': 'G2'}


def c3s2_speed(r):
    d = r.choice([100, 150, 200, 400, 800, 1500])
    t = r.choice([10, 12.5, 16, 20, 25, 40, 50, 64, 80, 100, 200, 250, 300])
    v = d / t
    return {'stem': f'A cyclist covers {d} m in {num(t)} s. What is the average speed in m/s and in km/h?', 'answer': f'{sig(v, 3)} m/s = {sig(v * 3.6, 3)} km/h',
            'key': f'v = {d} ÷ {num(t)} = {sig(v, 3)} m/s; × 18/5 = {sig(v * 3.6, 3)} km/h.',
            'distractors': [f'{sig(v, 3)} m/s = {sig(v / 3.6, 3)} km/h', f'{sig(t / d, 3)} m/s = {sig(t / d * 3.6, 3)} km/h', f'{sig(v * 2, 3)} m/s = {sig(v * 7.2, 3)} km/h']}


def c3s2_velocity(r):
    L = r.choice([50, 100, 200])
    t1, t2 = r.choice([(25, 25), (40, 50), (20, 30), (50, 50), (30, 40)])
    T = t1 + t2
    return {'stem': f'A swimmer swims one length of a {L} m pool in {t1} s and returns to the start in {t2} s. Find her average speed and average velocity for the whole swim.',
            'answer': f'Average speed {sig(2 * L / T, 3)} m/s; average velocity 0 m/s',
            'key': f'Average speed = {2 * L} ÷ {T} = {sig(2 * L / T, 3)} m/s. Displacement is zero (back at start), so average velocity = 0.',
            'distractors': [f'Average speed {sig(2 * L / T, 3)} m/s; average velocity {sig(2 * L / T, 3)} m/s', f'Average speed 0 m/s; average velocity {sig(2 * L / T, 3)} m/s', f'Average speed {sig(L / T, 3)} m/s; average velocity 0 m/s']}


c3s2_mc = [
    ('The SI unit of speed is:', 'm/s', 'km/h', 'm/s²', 'm'),
    ('A car\'s speedometer measures:', 'instantaneous speed', 'average speed', 'distance', 'displacement'),
    ('The odometer of a vehicle measures:', 'distance travelled', 'speed', 'velocity', 'acceleration'),
    ('An object moving with uniform speed in a circle has:', 'changing velocity', 'constant velocity', 'zero velocity', 'no direction'),
]
c3s2_why = [
    ('Can an object have constant speed but changing velocity? Give an example.', 'Yes. If its direction changes, velocity changes even at constant speed, e.g. a car going round a circular track at steady speed.', '1 mark: yes with reason. 1 mark: example.'),
    ('Why is average speed not always the average of two speeds?', 'Average speed is total distance ÷ total time; when equal distances are covered at different speeds, more time is spent at the lower speed.', '1 mark: definition. 1 mark: time weighting.'),
]
c3s2_ar = [
    ('The motion of a car in city traffic is non-uniform.', 'The car covers unequal distances in equal intervals of time.', 'a', 'R explains A.'),
    ('Speed and velocity are always equal in magnitude.', 'Velocity includes direction.', 'd', 'A false: average speed and average velocity differ when direction changes; R true.'),
    ('Average velocity can be zero while average speed is not.', 'Average velocity depends on displacement.', 'a', 'R explains A.'),
]

c3s3_defs = [
    ('acceleration', 'the rate of change of velocity with time'),
    ('uniform acceleration', 'acceleration in which velocity changes by equal amounts in equal intervals of time'),
    ('retardation (deceleration)', 'negative acceleration, when velocity decreases with time'),
]


def c3s3_a(r):
    u = r.choice([0, 2, 5, 10, 15, 20])
    v = u + r.choice([5, 10, 15, 20, 25])
    t = r.choice([2, 4, 5, 8, 10])
    a = (v - u) / t
    return {'stem': f'A car speeds up from {u} m/s to {v} m/s in {t} s. Find its acceleration.', 'answer': f'{num(a, 2)} m/s²',
            'key': f'a = (v − u)/t = ({v} − {u})/{t} = {num(a, 2)} m/s².', 'distractors': [f'{num(v / t, 2)} m/s²', f'{num((v + u) / t, 2)} m/s²', f'{num((v - u) * t, 2)} m/s²']}


def c3s3_brake(r):
    v = r.choice([10, 12, 15, 20, 25, 30])
    t = r.choice([2, 2.5, 4, 5, 6])
    a = v / t
    s = v * t / 2
    return {'stem': f'A bus moving at {v} m/s applies brakes and stops in {num(t)} s with uniform retardation. Find the retardation and the distance travelled while braking.',
            'answer': f'{num(a, 2)} m/s²; {num(s, 1)} m', 'key': f'a = (0 − {v})/{num(t)} = −{num(a, 2)} m/s² (retardation {num(a, 2)} m/s²); s = ut + ½at² = {v} × {num(t)} − ½ × {num(a, 2)} × {num(t)}² = {num(s, 1)} m.'}


def c3s3_suvat(r):
    kind = r.choice(['v', 's', 'v2'])
    u = r.choice([0, 2, 4, 5, 10])
    a = r.choice([1, 2, 2.5, 4, 5])
    t = r.choice([2, 3, 4, 5, 6, 8, 10])
    who = name(r)
    if kind == 'v':
        v = u + a * t
        return {'stem': f'{who}\'s scooter starts with a velocity of {u} m/s and accelerates uniformly at {num(a)} m/s² for {t} s. Find its final velocity.',
                'answer': f'{num(v)} m/s', 'key': f'v = u + at = {u} + {num(a)} × {t} = {num(v)} m/s.', 'distractors': [f'{num(a * t)} m/s', f'{num(u * t + a)} m/s', f'{num(u + a * t * t)} m/s']}
    if kind == 's':
        s = u * t + 0.5 * a * t * t
        return {'stem': f'A train starting with velocity {u} m/s moves with uniform acceleration {num(a)} m/s². How far does it travel in {t} s?',
                'answer': f'{num(s, 1)} m', 'key': f's = ut + ½at² = {u} × {t} + ½ × {num(a)} × {t}² = {num(s, 1)} m.', 'distractors': [f'{num(u * t + a * t * t, 1)} m', f'{num(0.5 * a * t, 1)} m', f'{num((u + a * t) * t, 1)} m']}
    s = r.choice([20, 25, 40, 50, 100])
    v = math.sqrt(u * u + 2 * a * s)
    return {'stem': f'A ball rolls down a slope with initial velocity {u} m/s and uniform acceleration {num(a)} m/s². What is its velocity after covering {s} m?',
            'answer': f'{sig(v, 3)} m/s', 'key': f'v² = u² + 2as = {u}² + 2 × {num(a)} × {s} = {num(u * u + 2 * a * s)}; v = {sig(v, 3)} m/s.',
            'distractors': [f'{sig(u * u + 2 * a * s, 3)} m/s', f'{sig(u + a * s, 3)} m/s', f'{sig(math.sqrt(2 * a * s) / 2, 3)} m/s']}


def c3s3_stop(r):
    v = r.choice([36, 54, 72, 90, 108])
    a = r.choice([3, 4, 5, 6])
    vs = v * 5 / 18
    s = vs * vs / (2 * a)
    t = vs / a
    return {'stem': f'A car moving at {v} km/h on an expressway brakes with a uniform retardation of {a} m/s². Find (i) the time taken to stop and (ii) the stopping distance.',
            'answer': f'(i) {sig(t, 3)} s (ii) {sig(s, 3)} m', 'key': f'u = {v} × 5/18 = {num(vs)} m/s. (i) t = u/a = {num(vs)}/{a} = {sig(t, 3)} s. (ii) v² = u² − 2as ⇒ s = u²/2a = {num(vs * vs)}/{2 * a} = {sig(s, 3)} m. (1 + 1 + 1 marks)'}


c3s3_mc = [
    ('The SI unit of acceleration is:', 'm/s²', 'm/s', 'm²/s', 'km/h'),
    ('An object moving with uniform velocity has acceleration:', 'zero', 'positive', 'negative', 'infinite'),
    ('A freely falling object near the Earth\'s surface has:', 'uniform acceleration', 'uniform velocity', 'zero acceleration', 'decreasing acceleration'),
    ('Which equation relates v, u, a and s?', 'v² = u² + 2as', 'v = u + at', 's = ut + ½at²', 'a = v/t only'),
]
c3s3_why = [
    ('Why is acceleration considered negative when a vehicle slows down?', 'The velocity decreases, so the change (v − u) is negative and acceleration acts opposite to the direction of motion.', '1 mark: v < u. 1 mark: opposite direction.'),
    ('Can an object have zero velocity and non-zero acceleration at the same moment? Give an example.', 'Yes: a ball thrown upwards at its highest point has zero velocity but acceleration due to gravity downwards.', '1 mark: yes. 1 mark: example.'),
]
c3s3_ar = [
    ('A body moving in a circle with constant speed is accelerated.', 'The direction of its velocity keeps changing.', 'a', 'R explains A.'),
    ('If velocity is zero, acceleration must be zero.', 'Acceleration is the rate of change of velocity.', 'd', 'A false (e.g. top of a throw); R true.'),
    ('The equation v = u + at holds for any motion.', 'It is derived for uniform acceleration.', 'd', 'A false; R true.'),
]

c3s4_mc = [
    ('The slope of a distance–time graph gives:', 'speed', 'acceleration', 'distance', 'time'),
    ('The slope of a velocity–time graph gives:', 'acceleration', 'displacement', 'speed', 'distance'),
    ('The area under a velocity–time graph gives:', 'displacement', 'acceleration', 'velocity', 'time'),
    ('A straight line parallel to the time axis on a distance–time graph shows that the object is:', 'at rest', 'moving uniformly', 'accelerating', 'decelerating'),
    ('A straight line parallel to the time axis on a velocity–time graph shows:', 'uniform velocity', 'rest', 'uniform acceleration', 'non-uniform acceleration'),
    ('A curved distance–time graph indicates:', 'non-uniform speed', 'uniform speed', 'rest', 'zero acceleration'),
]


def c3s4_area(r):
    u = r.choice([0, 0, 5, 10])
    v = u + r.choice([10, 15, 20])
    t = r.choice([4, 5, 8, 10])
    s = (u + v) * t / 2
    a = (v - u) / t
    return {'stem': f'A velocity–time graph is a straight line from {u} m/s at t = 0 to {v} m/s at t = {t} s. Find the acceleration and the distance travelled in this time.',
            'answer': f'a = {num(a, 2)} m/s²; distance = {num(s, 1)} m', 'key': f'Slope = ({v} − {u})/{t} = {num(a, 2)} m/s². Area under graph = ½ × ({u} + {v}) × {t} = {num(s, 1)} m.',
            'distractors': [f'a = {num(a, 2)} m/s²; distance = {num(v * t, 1)} m', f'a = {num(v / t, 2)} m/s²; distance = {num(s, 1)} m', f'a = {num(a * t, 2)} m/s²; distance = {num(s / 2, 1)} m']}


def c3s4_trap(r):
    v = r.choice([10, 12, 15, 20])
    t1, t2, t3 = r.choice([(5, 10, 5), (4, 6, 2), (10, 20, 5), (2, 8, 4)])
    s = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    T = t1 + t2 + t3
    return {'stem': f'A metro train starts from rest, accelerates uniformly to {v} m/s in {t1} s, runs at this speed for {t2} s, and then stops uniformly in {t3} s. Using a velocity–time graph, find the total distance and the average speed.',
            'answer': f'{num(s, 1)} m; {sig(s / T, 3)} m/s', 'key': f'Area = ½ × {t1} × {v} + {t2} × {v} + ½ × {t3} × {v} = {num(0.5 * v * t1, 1)} + {v * t2} + {num(0.5 * v * t3, 1)} = {num(s, 1)} m; average speed = {num(s, 1)} ÷ {T} = {sig(s / T, 3)} m/s.'}


def c3s4_dt(r):
    who = name(r)
    pts = [0]
    v = r.choice([2, 3, 4, 5])
    for _ in range(4):
        pts.append(pts[-1] + v)
    rest = r.randint(1, 3)
    ds = ', '.join(f'{x} m' for x in pts)
    return {'stem': f'{who} records the position of a toy car every second: {ds}. Is the motion uniform? What will the distance–time graph look like, and what is the speed?',
            'answer': f'Uniform motion; a straight line through the origin; speed {v} m/s.', 'key': f'Equal distances ({v} m) in equal times, so uniform; slope = {v} m/s (2 marks).'}


c3s4_ar = [
    ('The distance–time graph of an object at rest is parallel to the time axis.', 'The position of an object at rest does not change with time.', 'a', 'R explains A.'),
    ('A distance–time graph can slope downwards with time.', 'Distance travelled can never decrease.', 'd', 'A false: distance cannot decrease (a position–time graph can); R true.'),
    ('The area under a velocity–time graph gives the displacement.', 'Velocity × time = displacement.', 'a', 'R explains A.'),
]
c3s4_why = [
    ('What does the slope of a velocity–time graph tell us, and what does a steeper line mean?', 'The slope gives acceleration; a steeper line means a larger acceleration.', '1 mark: acceleration. 1 mark: steeper = larger.'),
    ('Two distance–time graphs A and B are straight lines through the origin; A is steeper. Which object is faster? Explain.', 'A, because the slope of a distance–time graph is the speed, and A has the greater slope.', '1 mark: A. 1 mark: slope = speed.'),
]

c3s5_defs = [
    ('uniform circular motion', 'motion of an object along a circular path with constant speed'),
    ('centripetal direction', 'the direction towards the centre of the circle in circular motion'),
]


def c3s5_v(r):
    rr = r.choice([7, 14, 21, 35, 42, 70, 105])
    t = r.choice([11, 22, 44, 55, 66, 88])
    v = 2 * 22 / 7 * rr / t
    obj = r.choice(['A cyclist goes once around a circular track', 'A toy train completes one round of a circular track', 'A merry-go-round seat goes once around'])
    return {'stem': f'{obj} of radius {rr} m in {t} s. Find its speed. (π = 22/7)', 'answer': f'{sig(v, 3)} m/s',
            'key': f'v = 2πr/t = 2 × 22/7 × {rr} ÷ {t} = {sig(v, 3)} m/s.', 'distractors': [f'{sig(rr / t, 3)} m/s', f'{sig(22 / 7 * rr / t, 3)} m/s', f'{sig(2 * 22 / 7 * rr * t, 3)} m/s']}


def c3s5_sat(r):
    R = r.choice([42250, 7000, 6800])
    T = {42250: 24, 7000: 1.6, 6800: 1.5}[R]
    v = 2 * math.pi * R / (T * 3600)
    return {'stem': f'A satellite moves in a circular orbit of radius {R} km and completes one orbit in {T} h. Calculate its speed in km/s.', 'answer': f'{sig(v, 3)} km/s',
            'key': f'v = 2πr/T = 2 × 3.14 × {R} ÷ ({T} × 3600) = {sig(v, 3)} km/s.', 'distractors': [f'{sig(v * 3600, 3)} km/s', f'{sig(R / (T * 3600), 3)} km/s', f'{sig(v * 2, 3)} km/s']}


c3s5_mc = [
    ('When a stone tied to a string is whirled in a circle and released, it moves:', 'along the tangent to the circle at that point', 'towards the centre', 'away from the centre radially', 'in a circle'),
    ('In uniform circular motion, which quantity stays constant?', 'Speed', 'Velocity', 'Direction of motion', 'Displacement'),
    ('An athlete running on a circular track with constant speed has:', 'an accelerated motion', 'uniform velocity', 'zero acceleration', 'no change in direction'),
]
c3s5_why = [
    ('Why is uniform circular motion called accelerated motion?', 'The direction of motion changes at every point, so velocity changes, which means there is acceleration.', '1 mark: direction changes. 1 mark: velocity changes → acceleration.'),
    ('Why do sparks from a grinding wheel fly off along straight lines?', 'Each particle leaving the wheel moves along the tangent to the circle at the point where it leaves.', '1 mark: tangent. 1 mark: no longer held in circle.'),
]
c3s5_ar = [
    ('A stone whirled in a circle flies off tangentially when the string breaks.', 'At every point in circular motion the velocity is along the tangent.', 'a', 'R explains A.'),
    ('Uniform circular motion has constant velocity.', 'Speed is constant in uniform circular motion.', 'd', 'A false; R true.'),
]
c3_hots = [
    ('Two cars start together from a signal. Car A accelerates at 2 m/s² from rest; car B moves at a constant 10 m/s. When and where will A catch up with B?', 'A: s = ½ × 2 × t² = t²; B: s = 10t; equal when t² = 10t, t = 10 s; distance = 100 m.', '1 mark each equation. 1 mark: t = 10 s and 100 m.'),
    ('The distance–time graph of a delivery rider is a straight line from 0 to 10 min, flat from 10 to 15 min, and then a steeper straight line to 25 min. Describe the motion in each part.', '0–10 min: uniform speed; 10–15 min: at rest (stopped); 15–25 min: uniform motion at a higher speed than before.', '1 mark per part.'),
    ('A ball is dropped from a height. Sketch (describe) its velocity–time graph and say what the slope and area represent.', 'A straight line through the origin rising with time (uniform acceleration ≈ 9.8 m/s²); slope = acceleration due to gravity; area = distance fallen.', '1 mark shape. 1 mark slope. 1 mark area.'),
    ('An object is moving at a constant 20 m/s. Is it necessarily in uniform motion? Explain with two cases.', 'Not necessarily. On a straight road at constant speed it has uniform velocity; on a circular track at the same speed its direction changes, so its velocity changes and it is accelerating.', '1 mark each case. 1 mark: conclusion.'),
]


def c3_case(r):
    who = name(r)
    u = r.choice([0, 5])
    a = r.choice([1, 2, 3])
    t = r.choice([4, 5, 6])
    v = u + a * t
    s = u * t + 0.5 * a * t * t
    return {'stem': (f'Read: {who} recorded the speedometer reading of a car on a straight road every second after it left a toll plaza. It started at {u} m/s and its speed rose by {a} m/s every second for {t} s.\n'
                     f'(i) Is the motion uniform or non-uniform? (ii) What is the acceleration? (iii) Find the speed at t = {t} s. (iv) Find the distance covered in these {t} s.'),
            'answer': f'(i) Non-uniform (uniformly accelerated). (ii) {a} m/s². (iii) {v} m/s. (iv) {num(s, 1)} m.',
            'key': f'1 mark each: (iii) v = u + at; (iv) s = ut + ½at² = {u} × {t} + ½ × {a} × {t}² = {num(s, 1)} m.'}


def c3_case2(r):
    rr = r.choice([35, 70, 105])
    t = r.choice([44, 55, 66])
    who = name(r)
    circ = 2 * 22 / 7 * rr
    return {'stem': (f'Read: {who} cycles around a circular park of radius {rr} m at a steady speed, taking {t} s for each round.\n'
                     f'(i) Find the distance covered in one round (π = 22/7). (ii) Find the speed. (iii) What is the displacement after one complete round? (iv) Is {who} accelerating? Explain.'),
            'answer': f'(i) {num(circ, 1)} m. (ii) {sig(circ / t, 3)} m/s. (iii) Zero. (iv) Yes, the direction of motion keeps changing, so velocity changes.',
            'key': '1 mark each part.'}


c3_long = [
    ('Derive (using a velocity–time graph) the equations v = u + at and s = ut + ½at² for uniformly accelerated motion. A body starting from rest accelerates at 2 m/s² for 5 s; find its final velocity and distance.',
     'Graph: straight line from u to v over time t; slope = (v − u)/t = a ⇒ v = u + at. Area = rectangle ut + triangle ½ × t × (v − u) = ut + ½at². Numerical: v = 0 + 2 × 5 = 10 m/s; s = ½ × 2 × 25 = 25 m.',
     '2 marks each derivation; 1 mark numerical.'),
    ('Distinguish between distance and displacement, and between speed and velocity. A boy runs from his house 300 m east to a shop in 150 s and returns 200 m west in 100 s. Find his average speed and average velocity.',
     'Distance: path length, scalar; displacement: shortest path with direction, vector. Speed: distance/time, scalar; velocity: displacement/time, vector. Average speed = (300 + 200)/250 = 2 m/s. Displacement = 100 m east; average velocity = 100/250 = 0.4 m/s east.',
     '2 marks distinctions; 3 marks numerical.'),
]

# ======================= ch04 Mixtures and Separation
c4s1_defs = [
    ('a pure substance', 'a substance consisting of a single type of particles with fixed composition'),
    ('a mixture', 'matter containing two or more pure substances mixed in any proportion without chemical combination'),
    ('a homogeneous mixture', 'a mixture with uniform composition throughout'),
    ('a heterogeneous mixture', 'a mixture with physically distinct parts and non-uniform composition'),
    ('an alloy', 'a homogeneous mixture of metals, or of a metal and a non-metal, that cannot be separated by physical methods'),
]
c4s1_cats = {
    'a homogeneous mixture': ['sugar in water', 'brass', 'air', 'soda water', 'vinegar', 'salt solution'],
    'a heterogeneous mixture': ['sand and iron filings', 'oil and water', 'chalk in water', 'muddy water', 'milk of magnesia', 'kerosene and water'],
}
c4s1_pure = {
    'a pure substance': ['ice', 'mercury', 'iron', 'carbon dioxide', 'distilled water', 'sodium chloride'],
    'a mixture': ['milk', 'sea water', 'soil', 'brass', 'air', 'wood'],
}
c4s1_mc = [
    ('Brass is considered a mixture because:', 'it shows the properties of its constituents copper and zinc and its composition can vary', 'it has a fixed composition', 'it is made of one element', 'it is formed by a chemical reaction'),
    ('A sample with a sharp melting point is most likely:', 'a pure substance', 'a mixture', 'a colloid', 'a suspension'),
    ('Which of these is NOT a homogeneous mixture?', 'Milk of magnesia', 'Air', 'Brass', 'Sugar solution'),
]
c4s1_why = [
    ('Why is air considered a mixture and not a compound?', 'Its components (nitrogen, oxygen, etc.) keep their properties, are present in varying proportions and can be separated by physical methods such as fractional distillation of liquid air.', '1 mark: variable composition/properties retained. 1 mark: physical separation.'),
    ('Why is an alloy considered a mixture even though it cannot be separated by physical methods?', 'It shows the properties of its constituents and has variable composition (e.g. brass has up to 30% zinc).', '1 mark: properties of constituents. 1 mark: variable composition.'),
]
c4s1_ar = [
    ('Sugar solution is homogeneous.', 'Sugar particles are uniformly distributed in water.', 'a', 'R explains A.'),
    ('A pure substance can have variable composition.', 'A pure substance consists of a single type of particles.', 'd', 'A false; R true.'),
    ('Brass is a mixture.', 'Brass shows the properties of copper and zinc and its composition can vary.', 'a', 'R explains A.'),
]

c4s2_defs = [
    ('a true solution', 'a homogeneous mixture in which particles are smaller than 1 nm and cannot be seen even with a microscope'),
    ('a suspension', 'a heterogeneous mixture in which solid particles are visible to the naked eye and settle on standing'),
    ('a colloid', 'a heterogeneous mixture with particles too small to see individually that do not settle but scatter light'),
    ('the Tyndall effect', 'the scattering of a beam of light by the particles of a colloid, making the path of light visible'),
    ('the dispersed phase', 'the solute-like component of a colloid, present as particles'),
    ('the dispersion medium', 'the component of a colloid in which the dispersed phase is spread'),
    ('solubility', 'the amount of solute present in a saturated solution at a given temperature'),
]
c4s2_cats = {
    'a true solution': ['salt in water', 'sugar in water', 'copper sulphate solution', 'soda water', 'alcohol in water'],
    'a suspension': ['chalk powder in water', 'muddy water', 'sand in water', 'flour in water'],
    'a colloid': ['milk', 'fog', 'shaving cream', 'jelly', 'smoke', 'face cream', 'cheese'],
}
c4s2_coll = [('fog', 'liquid', 'gas', 'aerosol'), ('smoke', 'solid', 'gas', 'aerosol'), ('milk', 'liquid', 'liquid', 'emulsion'), ('face cream', 'liquid', 'liquid', 'emulsion'),
             ('jelly', 'liquid', 'solid', 'gel'), ('cheese', 'liquid', 'solid', 'gel'), ('shaving cream', 'gas', 'liquid', 'foam'), ('foam rubber', 'gas', 'solid', 'foam'),
             ('milk of magnesia', 'solid', 'liquid', 'sol'), ('coloured gemstone', 'solid', 'solid', 'solid sol')]


def c4s2_colltype(r):
    n, dp, dm, t = r.choice(c4s2_coll)
    wrong = [x for x in ['aerosol', 'emulsion', 'gel', 'foam', 'sol'] if x != t]
    return mcq(f'{cap(n)} is a colloid. What type of colloid is it?', t, r.sample(wrong, 3), f'Dispersed phase {dp}, dispersion medium {dm}: {t}.', r)


def c4s2_phase(r):
    n, dp, dm, t = r.choice(c4s2_coll)
    return {'stem': f'Name the dispersed phase, the dispersion medium and the type of colloid in {n}.', 'answer': f'Dispersed phase: {dp}; dispersion medium: {dm}; type: {t}.',
            'key': '½ mark each for phase and medium, 1 mark type.'}


def c4s2_mm(r):
    a = r.choice([5, 10, 12, 15, 20, 25, 36, 40])
    w = r.choice([80, 90, 100, 150, 180, 200, 320])
    c = 100 * a / (a + w)
    return {'stem': f'A solution contains {a} g of common salt in {w} g of water. Calculate the concentration in terms of mass by mass percentage of the solution.',
            'answer': f'{sig(c, 3)}%', 'key': f'Mass of solution = {a} + {w} = {a + w} g; % = {a}/{a + w} × 100 = {sig(c, 3)}%.',
            'distractors': [f'{sig(100 * a / w, 3)}%', f'{sig(a / (a + w), 3)}%', f'{sig(100 * w / (a + w), 3)}%'], 'gap': 'G2'}


def c4s2_mv(r):
    a = r.choice([2, 4, 5, 8, 10, 25])
    v = r.choice([100, 200, 250, 400, 500])
    return {'stem': f'{a} g of urea is dissolved in water to make {v} mL of solution. Find the mass by volume percentage.', 'answer': f'{num(100 * a / v, 2)}%',
            'key': f'Mass by volume % = mass of solute ÷ volume of solution × 100 = {a}/{v} × 100 = {num(100 * a / v, 2)}%.',
            'distractors': [f'{num(a / v, 4)}%', f'{num(v / a, 2)}%', f'{num(1000 * a / v, 2)}%']}


def c4s2_vv(r):
    a = r.choice([10, 20, 25, 40, 50, 70])
    v = r.choice([100, 200, 250, 500])
    if a >= v:
        raise ValueError
    return {'stem': f'{a} mL of ethanol is mixed with water to make {v} mL of solution. Find the concentration as volume by volume percentage.', 'answer': f'{num(100 * a / v, 2)}%',
            'key': f'{a}/{v} × 100 = {num(100 * a / v, 2)}%.', 'distractors': [f'{num(100 * a / (v + a), 2)}%', f'{num(a / v, 3)}%', f'{num(100 * (v - a) / v, 2)}%']}


c4s2_mc = [
    ('Which mixture shows the Tyndall effect?', 'Milk diluted with water', 'Salt solution', 'Sugar solution', 'Copper sulphate solution'),
    ('Particles of a suspension:', 'settle down on standing', 'cannot be seen', 'pass through filter paper', 'never separate'),
    ('The path of sunlight entering a dense forest is visible because of:', 'the Tyndall effect in mist and smoke', 'reflection by leaves', 'refraction in glass', 'dispersion into colours'),
    ('The size of particles in a colloid is roughly:', 'between 1 nm and 1000 nm', 'less than 1 nm', 'more than 1 mm', 'exactly 1 m'),
    ('Which method separates the particles of a colloid?', 'Centrifugation', 'Filtration', 'Decantation', 'Sieving'),
]
c4s2_why = [
    ('Why does a beam of light pass through a salt solution without its path being visible, but its path is visible through milk mixed with water?', 'Salt particles are too small to scatter light; colloidal particles in milk are big enough to scatter light (Tyndall effect).', '1 mark: true solution particles tiny. 1 mark: colloid scatters.'),
    ('Why is a colloid called heterogeneous though it looks uniform?', 'It consists of two phases (dispersed phase and dispersion medium) and its particles can scatter light and be separated by centrifugation.', '1 mark: two phases. 1 mark: evidence.'),
]
c4s2_ar = [
    ('Milk shows the Tyndall effect.', 'Milk is a colloid whose particles scatter light.', 'a', 'R explains A.'),
    ('A suspension is stable.', 'Particles of a suspension settle on standing.', 'd', 'A false; R true.'),
    ('Colloidal particles pass through filter paper.', 'Colloidal particles are smaller than the pores of filter paper.', 'a', 'R explains A.'),
]

c4s3_tech = [
    ('evaporation', 'salt from sea water', 'the solvent evaporates leaving the dissolved solid'),
    ('centrifugation', 'cream from milk', 'rapid spinning forces denser particles to the bottom and lighter ones to the top'),
    ('a separating funnel', 'kerosene from water', 'immiscible liquids form separate layers that can be drained one by one'),
    ('sublimation', 'ammonium chloride from common salt', 'one component changes directly from solid to vapour on heating'),
    ('a magnet', 'iron pins from sand', 'only the magnetic component is attracted'),
    ('filtration', 'sand from water', 'insoluble solid is held back by the filter paper'),
    ('crystallisation', 'pure copper sulphate from an impure sample', 'pure crystals form on cooling a hot saturated solution, impurities stay in solution'),
    ('chromatography', 'different coloured dyes in black ink', 'components move at different rates on absorbent paper'),
    ('simple distillation', 'acetone from its mixture with water', 'liquids with a big difference in boiling points are boiled off one at a time and condensed'),
    ('fractional distillation', 'different gases from liquid air', 'liquids with boiling points differing by less than about 25 K separate in a fractionating column'),
    ('sedimentation and decantation', 'mud from water', 'heavy particles settle and the clear liquid is poured off'),
]


def c4s3_which(r):
    t, ex, why = r.choice(c4s3_tech)
    wrong = r.sample([x[0] for x in c4s3_tech if x[0] != t], 3)
    return mcq(f'Which method is best for separating {ex}?', t, wrong, f'{cap(t)}: {why}.', r)


def c4s3_explain(r):
    t, ex, why = r.choice(c4s3_tech)
    return {'stem': f'Name the method used to separate {ex} and explain the principle on which it works.', 'answer': f'{cap(t)}; {why}.', 'key': '1 mark: method. 1 mark: principle.'}


def c4s3_multi(r):
    combos = [
        ('salt, sand and ammonium chloride', 'Heat (sublimation) to remove ammonium chloride; add water and filter to remove sand; evaporate the filtrate to get salt.'),
        ('iron filings, sulphur powder and salt', 'Use a magnet to remove iron; dissolve in water and filter out sulphur; evaporate the filtrate to get salt.'),
        ('sand, camphor and common salt', 'Sublime camphor by heating; dissolve the rest in water and filter out sand; evaporate to get salt.'),
        ('oil, water and sand', 'Filter out sand (or let it settle and decant); separate oil and water in a separating funnel.'),
        ('chalk powder, sugar and iron filings', 'Magnet removes iron; dissolve in water, filter out chalk; evaporate or crystallise to get sugar.'),
    ]
    m, ans = r.choice(combos)
    return {'stem': f'Describe, step by step, how you would separate a mixture of {m}.', 'answer': ans, 'key': '1 mark per correct step in a correct order (3 marks).'}


c4s3_mc = [
    ('Why is crystallisation better than evaporation for purifying copper sulphate?', 'Some solids decompose or char on heating to dryness, and soluble impurities remain with the solid in evaporation', 'It is faster', 'It needs no heat', 'It gives more product always'),
    ('Which substance can be separated by sublimation?', 'Camphor', 'Common salt', 'Sugar', 'Sand'),
    ('In a centrifuge, denser particles are forced to:', 'the bottom of the tube', 'the top of the tube', 'the middle of the tube', 'out of the tube'),
    ('A mixture of kerosene and water can be separated using a separating funnel because they are:', 'immiscible liquids of different densities', 'miscible liquids', 'both solids', 'both gases'),
]
c4s3_why = [
    ('Why does a washing machine dryer remove water from clothes?', 'It spins rapidly (centrifugation); water is thrown out through holes while clothes are held by the drum.', '1 mark: spinning. 1 mark: water forced out.'),
    ('How is ammonium chloride separated from common salt, and why does this work?', 'By sublimation: on heating, ammonium chloride changes directly into vapour, which solidifies on a cool funnel; salt stays behind.', '1 mark: sublimation. 1 mark: explanation.'),
]
c4s3_ar = [
    ('Cream is separated from milk by centrifugation.', 'Cream is lighter than the rest of the milk.', 'a', 'R explains A.'),
    ('Salt can be separated from sea water by filtration.', 'Salt is dissolved in sea water.', 'd', 'A false: dissolved salt passes through filter paper; R true.'),
    ('Camphor can be separated from sand by sublimation.', 'Camphor changes directly from solid to vapour on heating.', 'a', 'R explains A.'),
]

c4s4_mc = [
    ('In paper chromatography of ink, the component that rises highest is the one that is:', 'most soluble in the solvent and least held by the paper', 'least soluble', 'heaviest', 'darkest in colour'),
    ('Fractional distillation is used when the boiling points of liquids differ by:', 'less than about 25 K', 'more than 100 K', 'exactly 0 K', 'more than 50 K'),
    ('Which gas is obtained first when liquid air is warmed in a fractional distillation column?', 'Nitrogen (boiling point −196 °C)', 'Oxygen (−183 °C)', 'Argon (−186 °C)', 'Carbon dioxide'),
    ('Petroleum is separated into petrol, diesel and kerosene by:', 'fractional distillation', 'filtration', 'centrifugation', 'chromatography'),
    ('Chromatography is used to:', 'separate colours in a dye and detect drugs in blood', 'separate sand from water', 'purify sugar', 'separate cream'),
    ('In simple distillation, the vapour is converted back to liquid in the:', 'condenser', 'distillation flask', 'thermometer', 'burner'),
]
c4s4_air = [('nitrogen', -196), ('argon', -186), ('oxygen', -183)]


def c4s4_bp(r):
    a, b = r.sample([('acetone', 56), ('water', 100), ('ethanol', 78), ('methanol', 65)], 2)
    diff = abs(a[1] - b[1])
    meth = 'simple distillation' if diff > 25 else 'fractional distillation'
    first = a if a[1] < b[1] else b
    return {'stem': f'{cap(a[0])} boils at {a[1]} °C and {b[0]} at {b[1]} °C. Which method would you use to separate a mixture of the two, and which liquid distils first?',
            'answer': f'{cap(meth)}; {first[0]} distils first.', 'key': f'Difference = {diff} K, {"more" if diff > 25 else "less"} than about 25 K, so {meth}; the lower-boiling {first[0]} distils first.',
            'distractors': [f'{cap("fractional distillation" if meth == "simple distillation" else "simple distillation")}; {first[0]} distils first.', f'{cap(meth)}; {(b if first == a else a)[0]} distils first.', 'Filtration; neither distils.']}


c4s4_why = [
    ('Why is a fractionating column used when the boiling points of two liquids are close?', 'It provides surfaces (glass beads) for repeated condensation and evaporation, so the vapour gradually becomes richer in the lower-boiling liquid.', '1 mark: repeated condensation/evaporation. 1 mark: purer separation.'),
    ('Why is the spot of ink placed above the solvent level in paper chromatography?', 'If it is below, the ink would dissolve directly into the solvent in the beaker instead of rising up the paper with it.', '1 mark: placed above. 1 mark: reason.'),
]
c4s4_ar = [
    ('Different dyes in ink separate on chromatography paper.', 'Dyes that are more soluble in the solvent rise faster.', 'a', 'R explains A.'),
    ('Simple distillation separates liquids with close boiling points.', 'Fractional distillation uses a fractionating column.', 'd', 'A false: needs fractional distillation; R true.'),
]

c4s5_cats = {
    'a physical change': ['melting of ice', 'dissolving sugar in water', 'tearing paper', 'boiling water', 'sublimation of camphor', 'chopping wood', 'stretching a rubber band'],
    'a chemical change': ['burning of a candle wick', 'rusting of iron', 'cooking an egg', 'curdling of milk', 'digestion of food', 'burning of magnesium ribbon', 'souring of milk'],
}
c4s5_defs = [
    ('a physical change', 'a change in which no new substance is formed and the chemical composition stays the same'),
    ('a chemical change', 'a change in which one or more new substances with different properties are formed'),
]
c4s5_mc = [
    ('Burning a candle involves:', 'both physical (melting wax) and chemical (burning) changes', 'only a physical change', 'only a chemical change', 'no change'),
    ('Which observation usually indicates a chemical change?', 'A new substance forms, often with gas, heat or colour change', 'Only the shape changes', 'Only the state changes', 'The object becomes smaller in size'),
]
c4s5_why = [
    ('Is the dissolving of salt in water a physical or a chemical change? Justify.', 'Physical: no new substance forms; salt can be recovered by evaporating the water.', '1 mark: physical. 1 mark: recoverable/no new substance.'),
]
c4s5_ar = [
    ('Rusting of iron is a chemical change.', 'A new substance, iron oxide, is formed.', 'a', 'R explains A.'),
    ('Melting of wax is a chemical change.', 'Melting changes only the state.', 'd', 'A false; R true.'),
]
c4s5_hots = [
    ('When magnesium ribbon burns, a dazzling white light is seen and white powder forms. When ice melts, water forms. Use at least two tests to show which is a chemical change.', 'Magnesium: new substance (MgO) with different properties, cannot be reversed easily, energy given out as light. Ice: same substance (H₂O), reversible by cooling.', '1 mark per valid test (max 3).'),
]


def c4_case(r):
    who = name(r)
    s = r.choice([20, 25, 30, 36])
    w = r.choice([100, 150, 200])
    return {'stem': (f'Read: {who} prepared three mixtures in beakers: A – {s} g of salt in {w} g of water; B – a spoonful of chalk powder in water; C – a few drops of milk in water. A torch beam was passed through each in a dark room.\n'
                     f'(i) In which beakers will the path of light be visible? (ii) Which mixture will settle on standing? (iii) Find the mass by mass % of salt in A. (iv) Classify A, B and C.'),
            'answer': f'(i) B and C (C shows the Tyndall effect; B scatters too, but settles). (ii) B. (iii) {s}/{s + w} × 100 = {sig(100 * s / (s + w), 3)}%. (iv) A: true solution; B: suspension; C: colloid.',
            'key': '1 mark each part.'}


c4_case_t = [
    ('Read: At a refinery near Mathura, crude oil is heated and its vapours pass up a tall column. Petrol vapours condense near the top, kerosene and diesel lower down, and heavy oils at the bottom.\n'
     '(i) Name this method. (ii) On what property does it depend? (iii) Why do fractions with lower boiling points collect near the top? (iv) Name another mixture separated by the same method.',
     '(i) Fractional distillation. (ii) Differences in boiling points. (iii) The column is cooler at the top, so only vapours with low boiling points rise that far before condensing. (iv) Liquid air (nitrogen, oxygen, argon).', '1 mark each.'),
]
c4_long = [
    ('Distinguish between a true solution, a colloid and a suspension on the basis of particle size, stability, filtration and the Tyndall effect. Give two examples of each.',
     'True solution: particles < 1 nm, stable, pass through filter paper, no Tyndall effect (salt, sugar solution). Colloid: 1–1000 nm, stable, pass through filter paper, show Tyndall effect (milk, fog). Suspension: > 1000 nm, unstable (settle), held by filter paper, may scatter light (muddy water, chalk in water).',
     '1 mark per property (4) + 1 mark examples.'),
    ('Describe, with the principle of each, how you would obtain (a) pure water from sea water, (b) different gases from air, (c) coloured dyes from black ink, (d) cream from milk, (e) camphor from a mixture with salt.',
     '(a) Distillation: water boils, vapour condenses, salt stays. (b) Fractional distillation of liquid air (different boiling points). (c) Paper chromatography (different solubility/rates). (d) Centrifugation (density). (e) Sublimation (camphor sublimes).',
     '1 mark each.'),
]

FAMILIES = {
    S + '01-st1': [TERM(c1s1_defs), DEF(c1s1_defs), G('C1', 'D2', 'mcq', c1s1_who), MC(c1s1_mc, C='C2', D='D2'), SA(c1s1_why), ARF(c1s1_ar),
                   SA(c1s1_hots, C='C4', D='D4', type='multi_step'), SA([('Classify these as obeying the cell theory or not: Amoeba, a virus, a mango leaf, a bacterium. Give a reason for the exception.', 'Obey: Amoeba, mango leaf, bacterium (all made of cells). Exception: virus, which is not made of cells.', '1 mark: classification. 1 mark: reason.')], C='C3', D='D3')],
    S + '01-st2': [TERM(c1s2_defs), DEF(c1s2_defs), MC(c1s2_mc, C='C2', D='D2'), CLS(c1s2_sol, 'For a plant cell, which of these is {}?', C='C3', D='D2'),
                   SA(c1s2_why), ARF(c1s2_ar), G('C3', 'D3', 'explain', c1s2_predict), SA(c1s2_hots, C='C4', D='D4', type='multi_step'), CASE(c1_case[:1]),
                   LONG(c1_long[1:], C='C4', D='D4')],
    S + '01-st3': [G('C1', 'D1', 'mcq', c1s3_fn), G('C1', 'D2', 'mcq', c1s3_rev), TERM(c1s3_defs, C='C1', D='D2'), DEF(c1s3_defs), MC(c1s3_mc, C='C2', D='D2'),
                   SA(c1s3_why), ARF(c1s3_ar), SA(c1s3_hots, C='C4', D='D4', type='multi_step'), CASE(c1_case[1:], C='C3', D='D4'), LONG(c1_long[:1], C='C4', D='D3')],
    S + '01-st4': [TERM(c1s4_defs), DEF(c1s4_defs), CLS(c1s4_cats, 'Which of the following is {}?', C='C2', D='D2'), CLS(c1s4_uni, 'Which of the following is {}?', C='C3', D='D1'),
                   MC(c1s4_mc, C='C1', D='D2'), SA(c1s4_why), ARF(c1s4_ar), SORT(c1s4_cats, 'Classify these as {A} or {B}: {L}.', C='C3', D='D3', n=(2, 3)),
                   CLS(c1s4_cats, 'Which of the following is {}?', C='C4', D='D3', neg=True)],
    S + '02-st1': [TERM(c2s1_defs), DEF(c2s1_defs), MC(c2s1_mc, C='C2', D='D2'), SA(c2s1_why), ARF(c2s1_ar), SA(c2s4_hots[1:], C='C4', D='D4', type='multi_step'),
                   SA([('Arrange in increasing order of organisation and give an example of each from the human body: organ, cell, organ system, tissue.', 'Cell (neuron) → tissue (nervous tissue) → organ (brain) → organ system (nervous system).', '1 mark order. 1 mark examples.')], C='C3', D='D3')],
    S + '02-st2': [TERM(c2s2_defs), DEF(c2s2_defs), CLS(c2s2_cats, 'Which of the following is {}?', C='C2', D='D2'), CLS(c2s2_type, 'Which of the following is {}?', C='C1', D='D2'),
                   MC(c2s2_mc, C='C2', D='D2'), SA(c2s2_why), ARF(c2s2_ar), SORT(c2s2_type, 'Classify these plant tissues as {A} or {B}: {L}.', C='C3', D='D2', n=(2, 3)),
                   SORT(c2s2_cats, 'Classify these into {A} and {B}: {L}.', C='C3', D='D3'), SA(c2s2_hots, C='C4', D='D4', type='multi_step'), CASE(c2_case[:1]),
                   LONG(c2_long[1:], C='C4', D='D4')],
    S + '02-st3': [TERM(c2s3_defs), DEF(c2s3_defs), CLS(c2s3_ex, 'Which of the following is {}?', C='C2', D='D2'), G('C1', 'D2', 'mcq', c2s3_muscle), MC(c2s3_mc, C='C2', D='D2'),
                   SA(c2s3_why), ARF(c2s3_ar), G('C3', 'D3', 'multi_step', c2s3_muscle_cmp), SORT(c2s3_ex, 'Classify these as {A} or {B}: {L}.', C='C3', D='D2'),
                   SA(c2s3_hots, C='C4', D='D4', type='multi_step'), CASE(c2_case[1:], C='C3', D='D4'), LONG(c2_long[:1], C='C4', D='D3'),
                   CLS(c2s3_ex, 'Which of the following is {}?', C='C3', D='D3', neg=True)],
    S + '02-st4': [MC(c2s4_mc, C='C1', D='D2'), SA(c2s4_why), ARF(c2s4_ar), SA(c2s4_hots[:1], C='C4', D='D4', type='multi_step'),
                   SA([('A plant is kept in red ink for a few hours and a thin section of its stem is seen under a microscope. Which tissue appears red and why?', 'Xylem appears red because it carries water (with the dye) from the roots upwards.', '1 mark: xylem. 1 mark: reason.'),
                       ('When you touch a hot pan you pull your hand away at once. Name the tissues involved, in order.', 'Nervous tissue (sensory nerve, spinal cord, motor nerve) carries the message; skeletal muscle contracts; tendons and bones move the hand.', '1 mark: nervous. 1 mark: muscle and bone.'),
                       ('Why do athletes need a good blood supply to their leg muscles during a race?', 'Blood (connective tissue) brings oxygen and glucose for respiration and removes carbon dioxide and lactic acid, letting muscles keep working.', '1 mark: supply. 1 mark: removal.')], C='C3', D='D3')],
    S + '03-st1': [TERM(c3s1_defs), DEF(c3s1_defs), MC(c3s1_mc, C='C2', D='D2'), SA(c3s1_why), ARF(c3s1_ar), G('C3', 'D2', 'numerical', c3s1_rect),
                   G('C3', 'D3', 'numerical', c3s1_circle), G('C4', 'D4', 'multi_step', c3s1_circle), G('C1', 'D2', 'mcq', c3s1_rect)],
    S + '03-st2': [TERM(c3s2_defs), DEF(c3s2_defs), MC(c3s2_mc, C='C1', D='D2'), SA(c3s2_why), ARF(c3s2_ar), G('C3', 'D1', 'numerical', c3s2_kmh),
                   G('C3', 'D2', 'numerical', c3s2_speed), G('C3', 'D3', 'numerical', c3s2_velocity), G('C3', 'D4', 'multi_step', c3s2_avg2), G('C4', 'D3', 'numerical', c3s2_avg2),
                   G('C2', 'D2', 'mcq', c3s2_kmh), G('C2', 'D3', 'mcq', c3s2_velocity), G('C4', 'D4', 'case', c3_case2, gap='G7')],
    S + '03-st3': [TERM(c3s3_defs + c3s2_defs[:2]), DEF(c3s3_defs), MC(c3s3_mc, C='C1', D='D2'), SA(c3s3_why), ARF(c3s3_ar), G('C3', 'D1', 'numerical', c3s3_a),
                   G('C3', 'D2', 'numerical', c3s3_suvat), G('C3', 'D3', 'numerical', c3s3_brake), G('C3', 'D4', 'multi_step', c3s3_stop), G('C4', 'D4', 'multi_step', c3s3_stop),
                   G('C4', 'D3', 'case', c3_case, gap='G7'), SA(c3_hots[:1], C='C4', D='D5', type='multi_step'), LONG(c3_long, C='C4', D='D4'), G('C2', 'D2', 'mcq', c3s3_a)],
    S + '03-st4': [MC(c3s4_mc, C='C1', D='D2'), SA(c3s4_why), ARF(c3s4_ar), G('C3', 'D2', 'numerical', c3s4_area), G('C3', 'D3', 'explain', c3s4_dt),
                   G('C3', 'D4', 'multi_step', c3s4_trap), G('C4', 'D4', 'multi_step', c3s4_trap), SA(c3_hots[1:3], C='C4', D='D3', type='multi_step'),
                   G('C2', 'D2', 'mcq', c3s4_area)],
    S + '03-st5': [TERM(c3s5_defs + c3s1_defs[:3]), DEF(c3s5_defs), MC(c3s5_mc, C='C1', D='D2'), SA(c3s5_why), ARF(c3s5_ar), G('C3', 'D2', 'numerical', c3s5_v),
                   G('C3', 'D3', 'numerical', c3s5_sat), SA(c3_hots[3:], C='C4', D='D3', type='multi_step'), G('C2', 'D2', 'mcq', c3s5_v)],
    S + '04-st1': [TERM(c4s1_defs), DEF(c4s1_defs), CLS(c4s1_cats, 'Which of the following is {}?', C='C2', D='D2'), CLS(c4s1_pure, 'Which of the following is {}?', C='C1', D='D2'),
                   MC(c4s1_mc, C='C2', D='D2'), SA(c4s1_why), ARF(c4s1_ar), SORT(c4s1_cats, 'Classify these as {A} or {B}: {L}.', C='C3', D='D2'),
                   SORT(c4s1_pure, 'Classify these as {A} or {B}: {L}.', C='C3', D='D3'), CLS(c4s1_cats, 'Which of the following is {}?', C='C4', D='D3', neg=True)],
    S + '04-st2': [TERM(c4s2_defs), DEF(c4s2_defs), CLS(c4s2_cats, 'Which of the following is {}?', C='C2', D='D2'), G('C1', 'D2', 'mcq', c4s2_colltype), MC(c4s2_mc, C='C2', D='D2'),
                   SA(c4s2_why), ARF(c4s2_ar), G('C3', 'D3', 'explain', c4s2_phase), G('C3', 'D2', 'numerical', c4s2_mm), G('C3', 'D1', 'numerical', c4s2_mv), G('C3', 'D3', 'numerical', c4s2_vv),
                   G('C4', 'D3', 'case', c4_case, gap='G7'), SORT(c4s2_cats, 'Classify as {A} or {B}: {L}.', C='C3', D='D4', type='multi_step'), LONG(c4_long[:1], C='C4', D='D4'),
                   G('C4', 'D4', 'multi_step', c4s2_mm)],
    S + '04-st3': [G('C1', 'D2', 'mcq', c4s3_which), MC(c4s3_mc, C='C2', D='D2'), SA(c4s3_why), ARF(c4s3_ar), G('C3', 'D3', 'explain', c4s3_explain),
                   G('C3', 'D4', 'multi_step', c4s3_multi), G('C4', 'D4', 'multi_step', c4s3_multi), LONG(c4_long[1:], C='C4', D='D4'), G('C2', 'D2', 'mcq', c4s3_which)],
    S + '04-st4': [MC(c4s4_mc, C='C1', D='D2'), G('C3', 'D3', 'numerical', c4s4_bp), SA(c4s4_why), ARF(c4s4_ar), CASE(c4_case_t), G('C2', 'D2', 'mcq', c4s4_bp),
                   SA([('A black sketch-pen ink gives three spots (blue, yellow, red) on chromatography paper, while a blue pen ink gives one blue spot at the same height as the blue spot of the black ink. What can you conclude?', 'Black ink is a mixture of three dyes; blue ink is a single dye, the same as the blue component of the black ink.', '1 mark each conclusion.'),
                       ('Why is fractional distillation, not simple distillation, used to separate oxygen and argon from liquid air?', 'Their boiling points (−183 °C and −186 °C) differ by only 3 K, far less than about 25 K, so a fractionating column is needed.', '1 mark: small difference. 1 mark: fractionating column.')], C='C4', D='D4', type='multi_step')],
    S + '04-st5': [TERM(c4s5_defs + c4s1_defs[:3]), CLS(c4s5_cats, 'Which of the following is {}?', C='C1', D='D1'), MC(c4s5_mc, C='C2', D='D2'), SA(c4s5_why), ARF(c4s5_ar),
                   SORT(c4s5_cats, 'Classify these as {A} or {B}: {L}.', C='C3', D='D2'), SA(c4s5_hots, C='C4', D='D4', type='multi_step'),
                   CLS(c4s5_cats, 'Which of the following is {}?', C='C3', D='D3', neg=True)],
}

# ----------------------------------------------------------------- extra higher-order items
c2_hots2 = [
    ('A plant stem and an animal limb both need support. Compare how plant tissues and animal tissues provide this support.', 'Plants: dead sclerenchyma fibres and lignified xylem give rigidity; collenchyma gives flexible support. Animals: bone (hard connective tissue) forms the skeleton, cartilage gives flexible support, and ligaments and tendons hold bones and muscles together.', '1 mark plants. 1 mark animals. 1 mark comparison (dead vs living tissue).'),
    ('Why does a cut on the skin heal and close over, while a damaged nerve in the spinal cord often does not recover?', 'Skin epithelium has cells that can divide and replace lost cells; mature neurons rarely divide, so damaged nerve cells are not easily replaced.', '1 mark: epithelial cells divide. 1 mark: neurons do not.'),
    ('An aquatic plant like Hydrilla floats while a land plant of the same size would sink. Which tissue helps and how?', 'Aerenchyma—parenchyma with large air cavities—makes the plant buoyant.', '1 mark: aerenchyma. 1 mark: air spaces give buoyancy.'),
    ('A sample of tissue has cells with no intercellular spaces, resting on a membrane, and covering a surface. Another has cells scattered in a large amount of matrix. Identify each and suggest where they may be found.', 'First: epithelial tissue (e.g. lining of mouth, skin). Second: connective tissue (e.g. blood, bone, cartilage).', '1 mark each identification. 1 mark locations.'),
]
c1_hots2 = [
    ('Why are cells so small? Explain using the need for exchange of materials.', 'Materials enter and leave through the cell surface; a small cell has a large surface area for its volume, so diffusion can supply all parts quickly. A very large cell could not exchange materials fast enough.', '1 mark: exchange through surface. 1 mark: surface-area idea. 1 mark: conclusion.'),
    ('If a plant cell\'s plasma membrane were damaged and became fully permeable, what would happen to the cell? Explain.', 'It would lose control over what enters and leaves; useful materials would leak out and harmful ones enter; osmosis would not work and the cell would die.', '1 mark: no selective control. 1 mark: leakage. 1 mark: death/osmosis fails.'),
]
FAMILIES[S + '02-st3'].append(SA(c2_hots2, C='C4', D='D3', type='multi_step'))
FAMILIES[S + '01-st4'].append(SA(c1_hots2, C='C4', D='D4', type='multi_step'))
