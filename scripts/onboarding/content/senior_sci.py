"""Senior (grades 11-12) slot banks for Physics, Chemistry, Mathematics and Biology.

Items are shared across boards; each slot's ref is a keyword ref (dsl.K) that resolves to the closest
subtopic in that board's grade map. Grade 11 prerequisites point at grade 10 subjects (CBSE and IB teach
one 'science' subject in grade 10, Cambridge three), grade 12 prerequisites at grade 11 subjects.
"""
from dsl import S, K

SCI10_PHY = {'cbse': 'science', 'cambridge': 'physics', 'ib': 'science'}
SCI10_CHE = {'cbse': 'science', 'cambridge': 'chemistry', 'ib': 'science'}
SCI10_BIO = {'cbse': 'science', 'cambridge': 'biology', 'ib': 'science'}

# ---------------------------------------------------------------- Physics
PHYSICS_PRE_G11 = [
    S(K(10, SCI10_PHY, {'cbse': 'electric power', 'cambridge': 'kilowatt-hour', 'ib': 'power stations'}),
      'Electrical power and energy', [
        ('A 2 kW heater runs for 3 hours. How much energy does it use?', '6 kWh', ['0.67 kWh', '5 kWh', '6000 kWh'],
         'E = P x t = 2 kW x 3 h'),
    ]),
    S(K(10, SCI10_PHY, {'cbse': 'ohm', 'cambridge': 'r = v/i', 'ib': 'transformers'}), "Ohm's law and resistance", [
        ('A 6 V battery drives a current of 2 A through a resistor. What is its resistance?', '3 Ω', ['12 Ω', '8 Ω', '0.33 Ω'],
         'R = V ÷ I'),
        ('Two 4 Ω resistors are connected in parallel. What is the combined resistance?', '2 Ω', ['8 Ω', '4 Ω', '16 Ω'],
         '1/R = 1/4 + 1/4'),
    ]),
    S(K(10, SCI10_PHY, {'cbse': 'magnetic field and field lines', 'cambridge': 'transformers', 'ib': 'transformers'}),
      'Magnetic effects and transformers', [
        ('A transformer that increases voltage is called a', 'step-up transformer', ['step-down transformer', 'rectifier', 'fuse'],
         'More turns on the secondary coil'),
        ('A transformer has 100 primary turns and 500 secondary turns. The input is 12 V. What is the output?', '60 V',
         ['2.4 V', '12 V', '600 V'], 'Vs/Vp = Ns/Np = 5'),
        ('Why is electricity transmitted at very high voltage over long distances?', 'A smaller current flows, so less energy is lost as heat',
         ['High voltage travels faster', 'Cables need less insulation', 'It increases the current'], 'Power loss = I²R'),
    ]),
    S(K(10, SCI10_PHY, {'cbse': 'refraction: laws', 'cambridge': 'reflection, refraction', 'ib': 'telescopes'}),
      'Refraction of light and waves', [
        ('When light passes from air into glass, it', 'slows down and bends towards the normal',
         ['speeds up and bends away from the normal', 'does not change direction at any angle', 'stops completely'],
         'Glass is optically denser'),
        ('Why does a straw look bent in a glass of water?', 'Light from the straw refracts as it leaves the water',
         ['The water bends the straw', 'Light reflects off the glass', 'The straw absorbs light'], 'Refraction at the surface'),
        ('Light travels at 3 x 10⁸ m/s in air and 2 x 10⁸ m/s in glass. What is the refractive index of the glass?', '1.5',
         ['0.67', '6', '1.0'], 'n = speed in air ÷ speed in glass'),
    ]),
]

PHYSICS_CUR_G11 = [
    S(K(11, 'physics', {'cbse': 'dimension|units', 'cambridge': 'si base|units', 'ib': 'kinematics'}), 'SI units and physical quantities', [
        ('Which of these is an SI base unit?', 'kilogram', ['newton', 'joule', 'watt'], 'N, J and W are derived units'),
        ('Which of these is a vector quantity?', 'velocity', ['speed', 'mass', 'energy'], 'Velocity has a direction'),
        ('What are the base units of force (the newton)?', 'kg m s⁻²', ['kg m s⁻¹', 'kg m² s⁻²', 'kg s⁻²'], 'F = ma'),
    ]),
    S(K(11, 'physics', 'velocity|kinematics'), 'Displacement, velocity and motion graphs', [
        ('The gradient of a displacement-time graph gives the', 'velocity', ['acceleration', 'distance', 'force'],
         'Change in displacement over time'),
        ('A car travels 120 m north in 10 s then 40 m south in 10 s. What is its average velocity?', '4 m/s north',
         ['8 m/s north', '6 m/s north', '0 m/s'], 'Displacement 80 m north over 20 s'),
        ('A velocity-time graph is a horizontal line above the time axis. What does it show?', 'Constant velocity, zero acceleration',
         ['The object is at rest', 'Constant acceleration', 'The object is slowing down'], 'Gradient is zero'),
    ]),
    S(K(11, 'physics', 'equations of motion|uniformly accelerated|accelerat'), 'Equations of uniformly accelerated motion', [
        ('A ball is dropped from rest. Ignoring air resistance, what is its speed after 2 s? (g = 10 m/s²)', '20 m/s',
         ['10 m/s', '5 m/s', '40 m/s'], 'v = u + at'),
        ('A car accelerates from 10 m/s to 30 m/s in 4 s. How far does it travel?', '80 m', ['40 m', '120 m', '160 m'],
         's = ½(u + v)t = ½ x 40 x 4'),
        ('A stone is thrown up at 15 m/s. How high does it rise? (g = 10 m/s²)', '11.25 m', ['15 m', '22.5 m', '1.5 m'],
         'v² = u² - 2gs with v = 0'),
    ]),
    S(K(11, 'physics', 'newton|laws of motion|dynamics'), "Newton's laws and momentum", [
        ("Newton's first law says an object keeps moving at constant velocity unless", 'a resultant force acts on it',
         ['it runs out of energy', 'it is heavy', 'gravity is zero'], 'Inertia'),
        ('A 2 kg trolley moving at 3 m/s has momentum of', '6 kg m/s', ['1.5 kg m/s', '9 kg m/s', '5 kg m/s'], 'p = mv'),
        ('A 0.5 kg ball hits a wall at 4 m/s and bounces back at 4 m/s. What is the change in momentum?', '4 kg m/s',
         ['0 kg m/s', '2 kg m/s', '8 kg m/s'], 'Direction reverses: 0.5 x (4 - (-4))'),
    ]),
]

PHYSICS_PRE_G12 = [
    S(K(11, 'physics', 'momentum'), 'Conservation of momentum', [
        ('A 1 kg ball at 6 m/s hits a stationary 2 kg ball and they move off together. What is their speed?', '2 m/s',
         ['3 m/s', '6 m/s', '1 m/s'], 'Momentum 6 = 3v'),
    ]),
    S(K(11, 'physics', 'work|energy'), 'Work, energy and power', [
        ('Work done by a force equals', 'force x distance moved in the direction of the force', ['force ÷ time', 'mass x velocity',
                                                                                                  'power x distance'], 'W = Fs'),
        ('A 50 kg student climbs 4 m of stairs in 5 s. What is the useful power? (g = 10 N/kg)', '400 W', ['2000 W', '40 W', '1000 W'],
         'mgh ÷ t = 2000 J ÷ 5 s'),
    ]),
    S(K(11, 'physics', 'circular|projectile|motion in a plane'), 'Projectiles and circular motion', [
        ('For a projectile, ignoring air resistance, the horizontal velocity', 'stays constant', ['increases', 'decreases to zero', 'reverses'],
         'No horizontal force'),
        ('An object moves in a circle at constant speed. Its acceleration is', 'towards the centre of the circle',
         ['zero', 'along the direction of motion', 'away from the centre'], 'Centripetal acceleration'),
        ('A ball is thrown horizontally at 10 m/s from a 20 m high cliff. How far from the base does it land? (g = 10 m/s²)', '20 m',
         ['10 m', '40 m', '200 m'], 'Fall time √(2 x 20 ÷ 10) = 2 s, then 10 x 2'),
    ]),
    S(K(11, 'physics', 'oscillat|simple harmonic|waves|wave'), 'Waves and oscillations', [
        ('The time for one complete oscillation is the', 'period', ['frequency', 'amplitude', 'wavelength'], 'T = 1/f'),
        ('A pendulum makes 20 oscillations in 10 s. What is its frequency?', '2 Hz', ['0.5 Hz', '200 Hz', '10 Hz'], '20 ÷ 10'),
        ('In simple harmonic motion, where is the speed of the oscillator greatest?', 'At the equilibrium position',
         ['At maximum displacement', 'It is the same everywhere', 'Halfway to maximum displacement only'],
         'All energy is kinetic at the centre'),
    ]),
]

PHYSICS_CUR_G12 = [
    S(K(12, 'physics', "coulomb|electric field|electric charges"), "Electric fields and Coulomb's law", [
        ('Like charges', 'repel each other', ['attract each other', 'have no effect on each other', 'cancel out'], 'Basic electrostatics'),
        ('If the distance between two point charges is doubled, the force between them becomes', 'one quarter as large',
         ['half as large', 'twice as large', 'four times as large'], 'Inverse square law'),
        ('What is the field strength between parallel plates 0.02 m apart with a p.d. of 400 V?', '20 000 V/m',
         ['8 V/m', '400 V/m', '0.00005 V/m'], 'E = V ÷ d'),
    ]),
    S(K(12, 'physics', 'moving charges|force on a|magnetic field|magnetic'), 'Magnetic force on currents and moving charges', [
        ("The direction of the force on a current-carrying wire in a magnetic field is given by", "Fleming's left-hand rule",
         ["Fleming's right-hand rule", "Lenz's law", "Ohm's law"], 'Motor effect'),
        ('A 0.5 m wire carrying 4 A lies at right angles to a 0.2 T field. What is the force on it?', '0.4 N', ['10 N', '2.5 N', '1.6 N'],
         'F = BIL'),
        ('Why does a charged particle moving at right angles to a uniform magnetic field travel in a circle?',
         'The force is always perpendicular to its velocity', ['The field speeds it up', 'The force is along its velocity',
                                                               'The particle loses charge'], 'It provides centripetal force'),
    ]),
    S(K(12, 'physics', 'electromagnetic induction|induction|faraday'), "Electromagnetic induction: Faraday and Lenz", [
        ('An e.m.f. is induced in a coil when', 'the magnetic flux through it changes', ['it is stationary in a steady field',
                                                                                         'it is made of plastic', 'no magnet is nearby'],
         "Faraday's law"),
        ("Lenz's law states that the induced current", 'opposes the change that produces it', ['adds to the change', 'is always zero',
                                                                                               'flows only in straight wires'],
         'A consequence of energy conservation'),
        ('The flux through a 100-turn coil falls from 0.03 Wb to 0 in 0.1 s. What is the average induced e.m.f.?', '30 V',
         ['0.3 V', '3 V', '300 V'], 'ε = NΔΦ/Δt = 100 x 0.03 ÷ 0.1'),
    ]),
    S(K(12, 'physics', 'photoelectric|quantum|photon'), 'Photons and the photoelectric effect', [
        ('Light behaves as a stream of particles called', 'photons', ['electrons', 'neutrons', 'phonons'], 'Quanta of light'),
        ('In the photoelectric effect, increasing the intensity of light above the threshold frequency increases',
         'the number of electrons emitted', ['the maximum kinetic energy of each electron', 'the threshold frequency', 'the work function'],
         'More photons per second, same energy each'),
        ('Why does red light fail to eject electrons from zinc even when very bright?', 'Each red photon has less energy than the work function of zinc',
         ['Red light has too many photons', 'Zinc reflects all light', 'Bright light cools the metal'], 'E = hf is too small'),
    ]),
]

# ---------------------------------------------------------------- Chemistry
CHEMISTRY_PRE_G11 = [
    S(K(10, SCI10_CHE, {'cbse': 'balancing', 'cambridge': 'hydrated|water of crystallisation', 'ib': 'mole concept'}), 'Chemical equations and quantities', [
        ('How many atoms are in one molecule of H₂SO₄?', '7', ['3', '6', '4'], '2 H + 1 S + 4 O'),
    ]),
    S(K(10, SCI10_CHE, {'cbse': 'ph scale', 'cambridge': 'titration', 'ib': 'concentration'}), 'Acids, bases and neutralisation', [
        ('Acid + alkali gives', 'a salt and water', ['only hydrogen', 'an oxide and carbon dioxide', 'a metal and water'],
         'Neutralisation'),
        ('Which salt forms when hydrochloric acid reacts with sodium hydroxide?', 'sodium chloride', ['sodium sulfate', 'sodium nitrate',
                                                                                                     'sodium carbonate'], 'Chloride from HCl'),
    ]),
    S(K(10, SCI10_CHE, {'cbse': 'homologous', 'cambridge': 'homologous|organic', 'ib': 'alkanes and alkenes'}), 'Alkanes, alkenes and homologous series', [
        ('The general formula of the alkanes is', 'CₙH₂ₙ₊₂', ['CₙH₂ₙ', 'CₙH₂ₙ₋₂', 'CₙHₙ'], 'Saturated hydrocarbons'),
        ('Which test distinguishes an alkene from an alkane?', 'Bromine water is decolourised by the alkene',
         ['Limewater turns milky with the alkane', 'A glowing splint relights with the alkene', 'Both turn litmus red'],
         'Addition across C=C'),
        ('Ethene and propene belong to the same homologous series. What do they share?', 'The same functional group and general formula',
         ['The same molecular mass', 'The same boiling point', 'The same number of carbon atoms'], 'They differ by CH₂'),
    ]),
    S(K(10, SCI10_CHE, {'cbse': 'reactivity series', 'cambridge': 'reactivity series|reactivity of metals', 'ib': 'exothermic'}), 'Reactivity and energy changes', [
        ('A reaction that releases heat to the surroundings is', 'exothermic', ['endothermic', 'reversible only', 'neutral'],
         'Temperature rises'),
        ('Which metal can be extracted from its oxide by heating with carbon?', 'iron', ['potassium', 'sodium', 'magnesium'],
         'Metals below carbon in the reactivity series'),
        ('Why is aluminium extracted by electrolysis rather than with carbon?', 'Aluminium is more reactive than carbon',
         ['Aluminium is a non-metal', 'Carbon is too expensive', 'Aluminium oxide is a gas'], 'Carbon cannot reduce it'),
    ]),
]

CHEMISTRY_CUR_G11 = [
    S(K(11, 'chemistry', 'avogadro|mole concept|the mole|molar mass|amount'), 'The mole and molar mass', [
        ('One mole of any substance contains about', '6.02 x 10²³ particles', ['6.02 x 10²³ grams', '1000 particles', '22.4 particles'],
         "Avogadro's constant"),
        ('How many moles are in 36 g of water (H₂O, Mr = 18)?', '2 mol', ['0.5 mol', '18 mol', '648 mol'], 'n = m ÷ M'),
        ('What mass of CO₂ forms when 12 g of carbon burns completely? (C = 12, O = 16)', '44 g', ['12 g', '32 g', '28 g'],
         '1 mol C gives 1 mol CO₂'),
    ]),
    S(K(11, 'chemistry', 'electronic configuration|electron config|orbital|quantum'), 'Electron configuration and orbitals', [
        ('How many electrons can an s orbital hold?', '2', ['1', '6', '8'], 'Two electrons with opposite spins'),
        ('What is the electron configuration of sodium (Z = 11)?', '1s² 2s² 2p⁶ 3s¹', ['1s² 2s² 2p⁷', '1s² 2s⁸ 3s¹', '1s² 2s² 2p⁶ 3p¹'],
         'Fill in order of energy'),
        ('Why is 4s filled before 3d in potassium?', 'The 4s subshell is lower in energy than 3d at that point',
         ['3d does not exist', '4s holds more electrons', 'Electrons are filled at random'], 'Aufbau principle'),
    ]),
    S(K(11, 'chemistry', 'periodic trends|ionisation energy|periodicity|ionisation|periodic'), 'Periodic trends', [
        ('Across a period from left to right, atomic radius generally', 'decreases', ['increases', 'stays the same', 'doubles'],
         'Greater nuclear charge pulls electrons closer'),
        ('Which element has the highest first ionisation energy in Period 3?', 'argon', ['sodium', 'magnesium', 'chlorine'],
         'Noble gas, full shell'),
        ('Why is the first ionisation energy of aluminium lower than that of magnesium?',
         'The outer electron of Al is in a 3p orbital, higher in energy and more shielded',
         ['Al has fewer protons', 'Mg is a noble gas', 'Al has a full outer shell'], 'Subshell effect'),
    ]),
    S(K(11, 'chemistry', 'vsepr|shape|covalent|bonding'), 'Chemical bonding and molecular shape', [
        ('A covalent bond is', 'a shared pair of electrons', ['a transfer of electrons', 'a sea of electrons', 'an attraction between ions only'],
         'Atoms share electrons'),
        ('What is the shape of a methane (CH₄) molecule?', 'tetrahedral', ['linear', 'trigonal planar', 'bent'],
         'Four bonding pairs, 109.5°'),
        ('Why is the bond angle in water (about 104.5°) smaller than in methane?', 'Lone pairs repel more than bonding pairs',
         ['Oxygen is smaller than carbon', 'Water has more bonds', 'Hydrogen atoms attract each other'], 'VSEPR theory'),
    ]),
]

CHEMISTRY_PRE_G12 = [
    S(K(11, 'chemistry', 'avogadro|mole concept|the mole|molar mass|amount'), 'Moles and concentration', [
        ('What is the concentration of 0.5 mol of NaCl dissolved to make 250 cm³ of solution?', '2 mol/dm³',
         ['0.125 mol/dm³', '0.5 mol/dm³', '125 mol/dm³'], '0.5 ÷ 0.25 dm³'),
    ]),
    S(K(11, 'chemistry', 'enthalpy change|first law|thermodynamics|energetics|enthalpy'), 'Enthalpy changes', [
        ('A negative ΔH means the reaction is', 'exothermic', ['endothermic', 'at equilibrium', 'very slow'], 'Heat is released'),
        ('Breaking bonds is', 'endothermic', ['exothermic', 'neither', 'always spontaneous'], 'Energy is needed to separate atoms'),
    ]),
    S(K(11, 'chemistry', 'le chatelier|dynamic equilibrium|equilibri'), "Equilibrium and Le Chatelier's principle", [
        ('At dynamic equilibrium, the rates of the forward and reverse reactions are', 'equal', ['both zero', 'very different', 'increasing'],
         'Concentrations stay constant'),
        ('For N₂ + 3H₂ ⇌ 2NH₃, increasing the pressure shifts the equilibrium', 'to the right, towards fewer gas molecules',
         ['to the left', 'nowhere', 'to the side with more molecules'], '4 moles of gas become 2'),
        ('The forward reaction is exothermic. What happens to the yield if the temperature is raised?', 'It decreases',
         ['It increases', 'It is unchanged', 'It doubles'], 'Equilibrium shifts in the endothermic direction'),
    ]),
    S(K(11, 'chemistry', 'redox|oxidation'), 'Redox and oxidation numbers', [
        ('Oxidation is', 'loss of electrons', ['gain of electrons', 'gain of hydrogen', 'loss of oxygen'], 'OIL RIG'),
        ('What is the oxidation number of manganese in KMnO₄?', '+7', ['+4', '+2', '-1'], '+1 + x + 4(-2) = 0'),
        ('In Zn + Cu²⁺ → Zn²⁺ + Cu, which species is the oxidising agent?', 'Cu²⁺', ['Zn', 'Zn²⁺', 'Cu'],
         'Cu²⁺ gains electrons, oxidising zinc'),
    ]),
]

CHEMISTRY_CUR_G12 = [
    S(K(12, 'chemistry', 'electrode potential|galvanic|electrochemi'), 'Electrochemical cells', [
        ('In a galvanic cell, oxidation takes place at the', 'anode', ['cathode', 'salt bridge', 'voltmeter'], 'An Ox, Red Cat'),
        ('What is the role of a salt bridge?', 'It completes the circuit and keeps the solutions electrically neutral',
         ['It supplies electrons', 'It stops all ions moving', 'It increases the voltage to infinity'], 'Ions flow through it'),
        ('E° for Zn²⁺/Zn is -0.76 V and for Cu²⁺/Cu is +0.34 V. What is the cell e.m.f.?', '1.10 V', ['-0.42 V', '0.42 V', '-1.10 V'],
         'E°cell = E°cathode - E°anode'),
    ]),
    S(K(12, 'chemistry', 'kinetics|rate'), 'Reaction kinetics and rate', [
        ('Which change usually increases the rate of a reaction?', 'raising the temperature', ['using larger lumps', 'diluting the solution',
                                                                                              'removing the catalyst'], 'More successful collisions'),
        ('A catalyst speeds up a reaction by', 'providing a route with lower activation energy', ['raising the temperature', 'changing ΔH',
                                                                                                  'being used up'], 'Alternative pathway'),
        ('For a first-order reaction, doubling the reactant concentration', 'doubles the rate', ['has no effect', 'quadruples the rate',
                                                                                                'halves the rate'], 'Rate = k[A]'),
    ]),
    S(K(12, 'chemistry', 'transition|d- and f-block|d-block|periodic table'), 'Transition elements', [
        ('Transition metals often form', 'coloured compounds', ['only white compounds', 'no ions', 'only gases'],
         'Partly filled d subshells'),
        ('Why do transition metals show variable oxidation states?', '4s and 3d electrons are close in energy and can both be lost',
         ['They have no d electrons', 'They are all noble gases', 'They have only one valence electron'], 'Similar energies'),
        ('Why are transition metals and their compounds good catalysts?', 'They can change oxidation state and adsorb reactants on their surface',
         ['They are very unreactive', 'They have low density', 'They always dissolve'], 'Variable oxidation states'),
    ]),
    S(K(12, 'chemistry', 'brønsted|ph,|ph scale|acid'), 'Acids, bases and solutions', [
        ('A Brønsted-Lowry acid is a', 'proton donor', ['proton acceptor', 'electron donor', 'hydroxide donor'], 'It gives H⁺'),
        ('What is the pH of 0.01 mol/dm³ HCl?', '2', ['1', '0.01', '12'], 'pH = -log[H⁺] = -log(10⁻²)'),
        ('A buffer solution', 'resists changes in pH when small amounts of acid or base are added',
         ['always has pH 7', 'is a strong acid', 'changes pH quickly'], 'Weak acid and its conjugate base'),
    ]),
]

# ---------------------------------------------------------------- Mathematics
MATHS_PRE_G11 = [
    S(K(10, 'maths', {'cbse': 'discriminant|nature of roots|quadratic formula|quadratic', 'cambridge': 'quadratic formula|quadratic', 'ib': 'solving quadratic'}), 'Quadratic equations', [
        ('Solve x² - 7x + 12 = 0.', 'x = 3 or x = 4', ['x = -3 or x = -4', 'x = 2 or x = 6', 'x = 12'], '(x - 3)(x - 4) = 0'),
    ]),
    S(K(10, 'maths', {'cbse': 'introduction to trigonometry|trigonometric ratios', 'cambridge': 'sine rule|trigonometry',
                      'ib': 'non-right|trigonometr'}), 'Trigonometric ratios', [
        ('What is sin 30°?', '1/2', ['√3/2', '1', '√2'], 'Standard value'),
        ('If tan θ = 3/4 and θ is acute, what is sin θ?', '3/5', ['4/5', '3/4', '5/3'], 'A 3-4-5 triangle'),
    ]),
    S(K(10, 'maths', {'cbse': 'arithmetic progression|progressions', 'cambridge': 'sequence|functions', 'ib': 'arithmetic sequences'}),
      'Sequences and nth term', [
        ('What is the 10th term of 4, 7, 10, ...?', '31', ['30', '34', '28'], '4 + 9 x 3'),
        ('Which term of 5, 9, 13, ... is 81?', '20th', ['19th', '21st', '16th'], '5 + 4(n - 1) = 81'),
        ('The sum of the first n odd numbers 1 + 3 + 5 + ... is', 'n²', ['2n', 'n(n + 1)', '2n - 1'], 'Sum of an AP'),
    ]),
    S(K(10, 'maths', {'cbse': 'probability', 'cambridge': 'tree diagrams|probability', 'ib': 'probability'}), 'Probability with combined events', [
        ('A coin is tossed and a die is rolled. What is P(head and a 6)?', '1/12', ['1/6', '1/2', '7/12'], '½ x 1/6'),
        ('A bag has 4 red and 6 blue balls. Two are drawn without replacement. What is P(both red)?', '2/15',
         ['4/25', '4/10', '1/5'], '4/10 x 3/9'),
        ('P(A) = 0.5, P(B) = 0.4 and P(A and B) = 0.2. What is P(A or B)?', '0.7', ['0.9', '0.2', '0.1'],
         'P(A) + P(B) - P(A and B)'),
    ]),
]

MATHS_CUR_G11 = [
    S(K(11, 'maths', 'quadratic'), 'Quadratics: completing the square', [
        ('If x² - 6x + 5 is written as (x - a)² + b, what is a?', '3', ['6', '-3', '5'], 'Half of -6'),
        ('Complete the square: x² + 4x + 7 = (x + 2)² + c. What is c?', '3', ['7', '11', '-3'], '(x + 2)² = x² + 4x + 4'),
        ('What is the minimum value of x² - 8x + 20?', '4', ['20', '-4', '8'], '(x - 4)² + 4'),
    ]),
    S(K(11, 'maths', 'function'), 'Functions: domain, range and composition', [
        ('If f(x) = 2x + 1, what is f(4)?', '9', ['8', '6', '10'], '2 x 4 + 1'),
        ('If f(x) = x + 3 and g(x) = 2x, what is f(g(5))?', '13', ['16', '10', '11'], 'g(5) = 10, then f(10)'),
        ('What is the inverse of f(x) = 3x - 6?', 'f⁻¹(x) = (x + 6)/3', ['f⁻¹(x) = 3x + 6', 'f⁻¹(x) = (x - 6)/3', 'f⁻¹(x) = x/3 - 6'],
         'Swap x and y, then solve'),
    ]),
    S(K(11, 'maths', 'trigonometric functions|circular measure|radian|trigonometr'), 'Radian measure and trigonometric functions', [
        ('How many radians are in 180°?', 'π', ['2π', 'π/2', '360'], 'Half a turn'),
        ('Convert 60° to radians.', 'π/3', ['π/6', '2π/3', '60π'], '60 x π/180'),
        ('What is the length of an arc of radius 6 cm subtending 2 radians at the centre?', '12 cm', ['3 cm', '6π cm', '36 cm'], 's = rθ'),
    ]),
    S(K(11, 'maths', 'binomial|permutation|series'), 'Counting and the binomial expansion', [
        ('How many ways can 3 different books be arranged on a shelf?', '6', ['3', '9', '27'], '3! = 6'),
        ('How many ways can a committee of 2 be chosen from 5 people?', '10', ['20', '25', '5'], '⁵C₂ = 10'),
        ('What is the coefficient of x² in (1 + x)⁵?', '10', ['5', '20', '25'], '⁵C₂'),
    ]),
]

MATHS_PRE_G12 = [
    S(K(11, 'maths', 'function'), 'Functions and their inverses', [
        ('If f(x) = x² and g(x) = x - 1, what is g(f(3))?', '8', ['4', '9', '2'], 'f(3) = 9, then g(9)'),
    ]),
    S(K(11, 'maths', 'geometric progression|geometric sequence|geometric'), 'Geometric sequences and series', [
        ('What is the common ratio of 3, 6, 12, 24, ...?', '2', ['3', '6', '1/2'], '6 ÷ 3'),
        ('What is the sum to infinity of 8 + 4 + 2 + 1 + ...?', '16', ['15', '8', 'infinite'], 'a ÷ (1 - r) = 8 ÷ 0.5'),
    ]),
    S(K(11, 'maths', {'cbse': 'trigonometr', 'cambridge': 'trigonometric identit|trigonometr', 'ib': 'radian|trigonometr'}), 'Trigonometric identities and equations', [
        ('sin²θ + cos²θ =', '1', ['0', 'tan θ', '2'], 'Pythagorean identity'),
        ('Solve sin x = 0.5 for 0° ≤ x ≤ 360°.', 'x = 30° or 150°', ['x = 30° only', 'x = 60° or 120°', 'x = 30° or 330°'],
         'Sine is positive in the first two quadrants'),
        ('Simplify (1 - cos²θ) / sin θ.', 'sin θ', ['cos θ', 'tan θ', '1'], '1 - cos²θ = sin²θ'),
    ]),
    S(K(11, 'maths', {'cbse': 'permutation', 'cambridge': 'binomial', 'ib': 'binomial'}), 'Permutations, combinations and binomial terms', [
        ('How many different 3-letter arrangements can be made from the letters of MATHS (no repeats)?', '60', ['10', '125', '15'],
         '5 x 4 x 3'),
        ('How many ways can a team of 3 be chosen from 7 players?', '35', ['210', '21', '343'], '⁷C₃ = 35'),
        ('What is the term independent of x in (x + 1/x)⁴?', '6', ['4', '1', '12'], '⁴C₂ x² (1/x)²'),
    ]),
]

MATHS_CUR_G12 = [
    S(K(12, 'maths', 'inverse trig|trigonometr'), 'Trigonometric identities and inverse functions', [
        ('What is sin⁻¹(1/2) in radians?', 'π/6', ['π/3', 'π/2', '1/2'], 'sin(π/6) = 1/2'),
        ('cos²θ - sin²θ is equal to', 'cos 2θ', ['sin 2θ', '1', 'tan 2θ'], 'Double-angle identity'),
        ('What is tan⁻¹(1) + tan⁻¹(√3)?', '7π/12', ['π/2', '5π/12', 'π/3'], 'π/4 + π/3'),
    ]),
    S(K(12, 'maths', 'chain rule|product|quotient|differentiab|differentiation'), 'Chain, product and quotient rules', [
        ('What is d/dx of (2x + 1)³?', '6(2x + 1)²', ['3(2x + 1)²', '(2x + 1)²', '6x(2x + 1)²'], 'Chain rule: 3(2x + 1)² x 2'),
        ('What is d/dx of x²·sin x?', '2x sin x + x² cos x', ['2x cos x', 'x² cos x', '2x sin x - x² cos x'], 'Product rule'),
        ('What is d/dx of eˣ / x?', 'eˣ(x - 1)/x²', ['eˣ/x²', 'eˣ(x + 1)/x²', 'eˣ'], 'Quotient rule'),
    ]),
    S(K(12, 'maths', 'integrat'), 'Integration', [
        ('∫ 2x dx =', 'x² + c', ['2 + c', 'x + c', '2x² + c'], 'Reverse of differentiation'),
        ('Evaluate ∫₀² 3x² dx.', '8', ['12', '6', '24'], '[x³] from 0 to 2'),
        ('What is the area between y = x² and the x-axis from x = 0 to x = 3?', '9', ['27', '3', '6'], '[x³/3] from 0 to 3'),
    ]),
    S(K(12, 'maths', 'vector'), 'Vectors and the scalar product', [
        ('What is the magnitude of the vector (3, 4)?', '5', ['7', '12', '25'], '√(9 + 16)'),
        ('What is the scalar (dot) product of (1, 2, 3) and (4, 0, -1)?', '1', ['7', '0', '-1'], '4 + 0 - 3'),
        ('Two non-zero vectors have a dot product of 0. What does this mean?', 'They are perpendicular', ['They are parallel', 'They are equal',
                                                                                                         'One is zero'], 'cos 90° = 0'),
    ]),
]

# ---------------------------------------------------------------- Biology
BIOLOGY_PRE_G11 = [
    S(K(10, SCI10_BIO, {'cbse': 'mendel', 'cambridge': 'inheritance|monohybrid', 'ib': 'genetic|biotechnolog'}), 'Inheritance and variation', [
        ('A cross between two heterozygous tall pea plants (Tt x Tt) gives what ratio of tall to dwarf?', '3 : 1',
         ['1 : 1', '1 : 2 : 1', 'all tall'], 'TT, Tt, Tt are tall; tt is dwarf'),
    ]),
    S(K(10, SCI10_BIO, {'cbse': 'respiration', 'cambridge': 'aerobic respiration', 'ib': 'carbon cycle'}), 'Respiration', [
        ('Aerobic respiration produces', 'carbon dioxide and water', ['oxygen and glucose', 'lactic acid only', 'ethanol only'],
         'Glucose + oxygen → CO₂ + water'),
        ('Why does aerobic respiration release more energy than anaerobic respiration?', 'Glucose is fully broken down',
         ['It is faster', 'It uses no glucose', 'It happens only in plants'], 'Anaerobic breakdown is incomplete'),
    ]),
    S(K(10, SCI10_BIO, {'cbse': 'accumulation of variation|variation', 'cambridge': 'variation|selection', 'ib': 'natural selection'}),
      'Variation and natural selection', [
        ('Differences between individuals of the same species are called', 'variation', ['adaptation', 'mutation only', 'evolution'],
         'Genetic and environmental causes'),
        ('Which is an example of continuous variation in humans?', 'height', ['blood group', 'tongue rolling', 'eye colour type only'],
         'It has a range of values'),
        ('Why does variation within a population matter for natural selection?', 'Some variants survive and reproduce better, passing on their alleles',
         ['All individuals die equally', 'Variation stops evolution', 'Organisms choose their variations'], 'Selection acts on variation'),
    ]),
    S(K(10, SCI10_BIO, {'cbse': 'ecosystem|energy flow', 'cambridge': 'food chains|organisms and their environment', 'ib': 'energy flow'}),
      'Ecosystems and energy flow', [
        ('An organism that eats only plants is a', 'herbivore', ['carnivore', 'decomposer', 'producer'], 'Primary consumer'),
        ('Why do pyramids of biomass usually narrow towards the top?', 'Energy and biomass are lost at each trophic level',
         ['Top predators are small', 'Plants are heavier', 'Decomposers remove the top'], 'Respiration and waste'),
        ('A pesticide becomes more concentrated in birds of prey than in insects. This is called', 'biological magnification',
         ['eutrophication', 'photosynthesis', 'decomposition'], 'It builds up along the food chain'),
    ]),
]

BIOLOGY_CUR_G11 = [
    S(K(11, 'biology', {'cbse': 'cell theory|cell: the unit|prokaryotic', 'cambridge': 'cell structure|cell', 'ib': 'cell'}), 'Cell structure', [
        ('The basic unit of life is the', 'cell', ['tissue', 'organ', 'atom'], 'Cell theory'),
        ('Which organelle is found in prokaryotic and eukaryotic cells?', 'ribosome', ['nucleus', 'mitochondrion', 'chloroplast'],
         'Prokaryotes have 70S ribosomes'),
        ('Why can electron microscopes show more detail than light microscopes?', 'Electrons have a much shorter wavelength, giving higher resolution',
         ['They use brighter light', 'They magnify colours', 'Specimens are alive'], 'Resolution depends on wavelength'),
    ]),
    S(K(11, 'biology', 'biological molecules|biomolecule|carbohydrate|nucleic'), 'Biological molecules', [
        ('Proteins are made of', 'amino acids', ['glucose units', 'fatty acids only', 'nucleotides'], 'Joined by peptide bonds'),
        ('Which test identifies a reducing sugar?', "Benedict's test", ['Biuret test', 'Iodine test', 'Emulsion test'],
         'Brick-red precipitate'),
        ('Why does a change in one amino acid sometimes stop a protein working?', 'It can change the folding and so the shape of the active part',
         ['Proteins have no shape', 'Amino acids are all identical', 'It adds glucose'], 'Shape determines function'),
    ]),
    S(K(11, 'biology', {'cbse': 'enzyme', 'cambridge': 'enzyme', 'ib': 'protein|condensation'}), 'Enzymes', [
        ('Enzymes are biological', 'catalysts', ['hormones', 'fuels', 'vitamins'], 'They speed up reactions'),
        ('Why does an enzyme stop working at high temperature?', 'Its active site changes shape (it is denatured)',
         ['It runs out of energy', 'It dissolves', 'It becomes a substrate'], 'Bonds holding its shape break'),
        ('A competitive inhibitor slows an enzyme by', 'binding to the active site and blocking the substrate',
         ['raising the temperature', 'changing the pH', 'destroying the substrate'], 'It resembles the substrate'),
    ]),
    S(K(11, 'biology', 'mitosis|mitotic|cell cycle|cell division|active transport|membrane'), 'Membranes, transport and cell division', [
        ('Movement of molecules against a concentration gradient using energy is', 'active transport', ['diffusion', 'osmosis',
                                                                                                         'facilitated diffusion'],
         'ATP is needed'),
        ('Mitosis produces', 'two genetically identical daughter cells', ['four different cells', 'gametes only', 'one large cell'],
         'For growth and repair'),
        ('Why is cancer described as a disease of the cell cycle?', 'Cells divide by mitosis in an uncontrolled way',
         ['Cells stop dividing', 'Cells only undergo meiosis', 'Cells lose their membranes'], 'Control of the cycle fails'),
    ]),
]

BIOLOGY_PRE_G12 = [
    S(K(11, 'biology', {'cbse': 'enzyme', 'cambridge': 'enzyme', 'ib': 'protein|condensation'}), 'Enzyme action', [
        ('In the lock-and-key model, the substrate fits the enzyme\'s', 'active site', ['nucleus', 'cell wall', 'ribosome'],
         'Complementary shape'),
    ]),
    S(K(11, 'biology', 'fluid mosaic|osmosis|diffusion|transport|membrane'), 'Cell membranes and transport', [
        ('The cell membrane is mainly made of', 'a phospholipid bilayer with proteins', ['cellulose', 'starch', 'chitin'],
         'Fluid mosaic model'),
        ('Why do small cells exchange materials more efficiently than large cells?', 'They have a larger surface area to volume ratio',
         ['They have thicker membranes', 'They have more DNA', 'They are always warmer'], 'More surface per unit volume'),
    ]),
    S(K(11, 'biology', 'nucleic|dna|protein synthesis'), 'DNA and protein synthesis', [
        ('In DNA, adenine pairs with', 'thymine', ['cytosine', 'guanine', 'uracil'], 'Complementary base pairing'),
        ('Which molecule carries the genetic code from the nucleus to the ribosome?', 'mRNA', ['tRNA', 'DNA', 'ATP'], 'Transcription'),
        ('A DNA strand reads ATG CCA. What is the complementary mRNA?', 'UAC GGU', ['TAC GGT', 'ATG CCA', 'UAG CCU'], 'U replaces T in RNA'),
    ]),
    S(K(11, 'biology', 'gas exchange|breathing|transport in|respiration'), 'Gas exchange and transport', [
        ('Gas exchange in the lungs happens in the', 'alveoli', ['trachea', 'bronchi', 'diaphragm'], 'Thin walls, large surface'),
        ('Haemoglobin carries', 'oxygen', ['glucose', 'urea', 'hormones'], 'In red blood cells'),
        ('Why does carbon monoxide poisoning cause tissues to lack oxygen?', 'CO binds to haemoglobin more strongly than oxygen',
         ['CO blocks the trachea', 'CO destroys alveoli instantly', 'CO raises blood pressure'], 'Less haemoglobin is free for O₂'),
    ]),
]

BIOLOGY_CUR_G12 = [
    S(K(12, 'biology', 'respiration'), 'Energy and cell respiration', [
        ('ATP is', 'the energy currency of the cell', ['a hormone', 'a type of DNA', 'a structural protein'], 'Adenosine triphosphate'),
        ('Where does the Krebs cycle take place?', 'mitochondrial matrix', ['cytoplasm', 'nucleus', 'cell membrane'],
         'Glycolysis is in the cytoplasm'),
        ('Why is oxygen called the final electron acceptor?', 'It accepts electrons at the end of the electron transport chain, forming water',
         ['It starts glycolysis', 'It is made in respiration', 'It carries glucose'], 'Without it the chain stops'),
    ]),
    S(K(12, 'biology', 'photosynthes'), 'Photosynthesis', [
        ('The light-dependent reactions of photosynthesis take place in the', 'thylakoid membranes', ['stroma', 'mitochondria', 'nucleus'],
         'Where chlorophyll is'),
        ('Which gas is released by the splitting of water (photolysis)?', 'oxygen', ['carbon dioxide', 'nitrogen', 'hydrogen'],
         'Water → H⁺ + e⁻ + O₂'),
        ('Why does the rate of photosynthesis stop increasing at high light intensity?', 'Another factor, such as CO₂ or temperature, becomes limiting',
         ['Chlorophyll is destroyed', 'Plants close all stomata at once', 'Light stops being absorbed'], 'Limiting factors'),
    ]),
    S(K(12, 'biology', 'homeostasis|hormone|signalling|chemical signal'), 'Homeostasis and chemical signalling', [
        ('Maintaining a constant internal environment is called', 'homeostasis', ['metabolism', 'excretion', 'respiration'], 'Steady state'),
        ('Which hormone lowers blood glucose?', 'insulin', ['glucagon', 'adrenaline', 'thyroxine'], 'From beta cells of the pancreas'),
        ('Negative feedback works by', 'reversing a change to bring a variable back to its set point', ['amplifying the change',
                                                                                                         'stopping all hormones', 'raising the set point'],
         'Corrective response'),
    ]),
    S(K(12, 'biology', 'evolution|selection'), 'Selection and evolution', [
        ('Charles Darwin proposed the theory of', 'evolution by natural selection', ['spontaneous generation', 'blending inheritance',
                                                                                     'use and disuse only'], 'On the Origin of Species'),
        ('Selection that favours one extreme of a range of phenotypes is', 'directional selection', ['stabilising selection',
                                                                                                    'disruptive selection', 'artificial isolation'],
         'The mean shifts'),
        ('Two populations of a species are separated by a mountain range for thousands of years. What may happen?',
         'They may become separate species through allopatric speciation', ['They will stay identical', 'They will merge',
                                                                            'They will stop reproducing'], 'Geographical isolation'),
    ]),
]

# Board swaps: CBSE Class 12 Biology opens with reproduction and genetics (respiration and photosynthesis are Class 11).
_CBSE_BIO12_REPRO = S(K(12, 'biology', 'double fertili|pollination|flowering'), 'Sexual reproduction in flowering plants', [
    ('Transfer of pollen from anther to stigma is called', 'pollination', ['fertilisation', 'germination', 'dispersal'], 'It precedes fertilisation'),
    ('In double fertilisation, one male gamete fuses with the egg. What does the other fuse with?', 'the two polar nuclei, forming the endosperm',
     ['a second egg', 'the pollen tube', 'the ovary wall'], 'Triple fusion gives the triploid endosperm'),
    ('Why do many wind-pollinated flowers have feathery stigmas and no nectar?', 'Feathery stigmas catch airborne pollen and there are no insects to attract',
     ['Nectar would attract wind', 'They self-pollinate only', 'Feathery stigmas make nectar'], 'Adaptation to the pollinating agent'),
])
_CBSE_BIO12_INHERIT = S(K(12, 'biology', 'inheritance|mendel'), 'Principles of inheritance and variation', [
    ("In Mendel's dihybrid cross (RrYy x RrYy), the phenotypic ratio is", '9 : 3 : 3 : 1', ['3 : 1', '1 : 2 : 1', '1 : 1 : 1 : 1'],
     'Independent assortment'),
    ('Red (RR) and white (rr) snapdragons give pink offspring. This is', 'incomplete dominance', ['complete dominance', 'codominance', 'polygenic inheritance'],
     'The heterozygote is intermediate'),
    ('A woman who is a carrier for haemophilia marries a normal man. What fraction of their sons is expected to be haemophilic?', '1/2',
     ['1/4', 'none', 'all'], 'Sons get their X chromosome from the mother'),
])
BIOLOGY_CUR_G12[0] = {'cbse': _CBSE_BIO12_REPRO, 'cambridge': BIOLOGY_CUR_G12[0], 'ib': BIOLOGY_CUR_G12[0]}
BIOLOGY_CUR_G12[1] = {'cbse': _CBSE_BIO12_INHERIT, 'cambridge': BIOLOGY_CUR_G12[1], 'ib': BIOLOGY_CUR_G12[1]}

# Board swaps where a board has no matching topic in that year.
_CBSE_CHEM12_SOLUTIONS = S(K(12, 'chemistry', 'colligative|raoult|solutions'), 'Solutions and colligative properties', [
    ('Molarity is the number of moles of solute per', 'litre of solution', ['kilogram of solvent', 'gram of solute', 'mole of solvent'],
     'mol/L'),
    ('Adding salt to water raises its boiling point. This is an example of a', 'colligative property', ['chemical change', 'catalytic effect',
                                                                                                       'redox reaction'],
     'It depends on the number of solute particles'),
    ('Why does 0.1 m NaCl lower the freezing point of water about twice as much as 0.1 m glucose?', 'NaCl splits into two ions, doubling the particles',
     ['NaCl is heavier', 'Glucose raises the freezing point', 'NaCl reacts with water'], "van't Hoff factor i = 2"),
])
CHEMISTRY_CUR_G12[3] = {'cbse': _CBSE_CHEM12_SOLUTIONS, 'cambridge': CHEMISTRY_CUR_G12[3], 'ib': CHEMISTRY_CUR_G12[3]}

_IB_CHEM11_SHAPES = S(K(11, 'chemistry', {'ib': 'vsepr|polarity'}), 'Molecular shape and polarity', [
    ('Which molecule is linear?', 'CO₂', ['H₂O', 'NH₃', 'CH₄'], 'Two bonding domains, no lone pairs'),
    ('Why is water a polar molecule while carbon dioxide is not?', 'Water is bent, so its bond dipoles do not cancel',
     ['Water has no polar bonds', 'CO₂ has lone pairs on carbon', 'Oxygen is less electronegative than hydrogen'], 'Shape decides overall polarity'),
    ('What is the shape of ammonia (NH₃)?', 'trigonal pyramidal', ['trigonal planar', 'tetrahedral with no lone pair', 'linear'],
     'Three bonding pairs and one lone pair'),
])
CHEMISTRY_PRE_G12[3] = {'cbse': CHEMISTRY_PRE_G12[3], 'cambridge': CHEMISTRY_PRE_G12[3], 'ib': _IB_CHEM11_SHAPES}

_CBSE_BIO12_MOLECULAR = S(K(12, 'biology', 'replication|transcription|dna'), 'Molecular basis of inheritance', [
    ('DNA replication is described as semi-conservative because', 'each new molecule has one old strand and one new strand',
     ['both strands are new', 'only half the DNA is copied', 'RNA is kept'], 'Meselson and Stahl'),
    ('Which enzyme joins nucleotides during DNA replication?', 'DNA polymerase', ['RNA polymerase', 'ligase only', 'amylase'],
     'It adds nucleotides to the growing strand'),
    ('A codon AUG on mRNA codes for methionine. Why is it called the start codon?', 'Translation begins at AUG',
     ['It ends translation', 'It is found only in DNA', 'It codes for every amino acid'], 'It sets the reading frame'),
])
BIOLOGY_CUR_G12[2] = {'cbse': _CBSE_BIO12_MOLECULAR, 'cambridge': BIOLOGY_CUR_G12[2], 'ib': BIOLOGY_CUR_G12[2]}
