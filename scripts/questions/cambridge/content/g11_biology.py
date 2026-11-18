"""Cambridge International AS Biology 9700, syllabus topics 1-11 (CUP coursebook 5th ed. ch 1-11), grade 11.

Paper 1 (MCQ), Paper 2 (AS structured) and Paper 3 (advanced practical skills) styles.
Knowledge-pack builders and the practical() engine (variables, results tables with repeats and
anomalies, means, trends, improvements, controls, graphs) are shared from g9_biology.py.
Parameterised templates cover the AS calculations: eyepiece graticule calibration, magnification,
dilutions, Mr of polymers, Q10 and rates, Km/Vmax, water potential, SA:V, mitotic index,
Chargaff ratios, Meselson-Stahl, translation with a codon table, potometer and stomatal density,
dissociation curves, cardiac output and ECGs, incidence, herd immunity and antibody responses.
"""
import math
from ._lib import compose, sf, sci, person, city, relation  # noqa: F401
from .g9_biology import cap, low, fx, Q, MQ, NQ, T, facts, mcqs, explain, shorts, longs, myths, pct, add_practical, trend_text  # noqa: F401

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}


def mn(x):
    """Typographic minus sign."""
    return str(x).replace('-', '−')


def cases(r, items, k):
    return r.sample(items, min(k, len(items)))


def mag_item(r, D, specimens, unit_out='μm'):
    """Magnification / actual size from an image length (mm) and a specimen list [(name, lo, hi) in μm]."""
    name, lo, hi = r.choice(specimens)
    name = __import__('re').sub(r' \((?:length|width|diameter|thickness|height)\)', '', name)
    act = r.uniform(lo, hi)
    act = float(sf(act, 2))
    Ms = [m for m in (50, 100, 200, 400, 500, 800, 1000, 1500, 2000, 2500, 4000, 5000, 8000, 10000, 15000, 20000, 25000, 40000, 50000, 80000, 100000, 150000, 200000)
          if 15 <= act * m / 1000 <= 140]
    if not Ms:
        return None
    M = r.choice(Ms)
    img = round(act * M / 1000)          # mm
    act = img * 1000 / M                 # μm, recomputed so the arithmetic is exact
    nm = act < 1
    a_txt = f'{sf(act * 1000, 3)} nm' if nm else f'{sf(act, 3)} μm'
    mode = r.randrange(3) if D >= 2 else r.randrange(2)
    p = person(r)
    if mode == 0:
        if D == 1:
            return NQ(r, f'An electron micrograph shows {name} with an image length of {img} mm. The magnification is ×{M:,}. What is the actual length of {name}?',
                      act * 1000 if nm else act, [x * (1000 if nm else 1) for x in (act * 10, act / 10, act * 1000, img * M / 1000)], ' nm' if nm else ' μm',
                      f'actual = image ÷ magnification = {img} mm ÷ {M:,} = {a_txt}.', f=lambda v: sf(v, 3))
        st = f'{p} measures the image of {name} in a micrograph as {img} mm. The magnification is ×{M:,}. Calculate the actual length of {name}, giving your answer in {"nanometres (nm)" if nm else "micrometres (μm)"}.'
        key = f'A = I ÷ M [1]; {img} mm = {img * 1000:,} μm; {img * 1000:,} ÷ {M:,} = {sf(act, 3)} μm [1]' + (f'; × 1000 = {sf(act * 1000, 3)} nm [1] [3]' if nm else ' [2]')
        return Q(st, a_txt, key, 'numerical')
    if mode == 1:
        if D == 1:
            return NQ(r, f'The actual length of {name} is {a_txt}. In a photomicrograph it is {img} mm long. What is the magnification?', M, [M / 10, M * 10, M / 1000, M * 100], '',
                      f'M = I ÷ A = {img * 1000:,} μm ÷ {sf(act, 3)} μm = ×{M:,}.', f=lambda v: '×' + f'{v:,.0f}' if v >= 1 else '×' + sf(v, 2))
        st = f'The actual length of {name} is {a_txt}. In a photomicrograph produced by {p}, the image of {name} is {img} mm long. Calculate the magnification of the photomicrograph. Show your working.'
        return Q(st, f'×{M:,}', f'M = I ÷ A [1]; same units: {img} mm = {img * 1000:,} μm' + (f' = {img * 1000000:,} nm' if nm else '') + f' [1]; M = ×{M:,} [1] [3]', 'numerical')
    bar = [b for b in (0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500) if 10 <= b * M / 1000 <= 60]
    if not bar:
        return None
    b = r.choice(bar)
    bl = b * M / 1000
    b_txt = f'{fx(b * 1000)} nm' if b < 1 else f'{fx(b)} μm'
    st = f'A micrograph of {name} has a scale bar labelled {b_txt}. The scale bar is {fx(bl, 1)} mm long and the image of {name} is {img} mm long. (a) Use the scale bar to calculate the magnification. (b) Calculate the actual length of {name}.'
    return Q(st, f'(a) ×{M:,} (b) {a_txt}', f'(a) {fx(bl, 1)} mm = {fx(bl * 1000, 1)} μm; {fx(bl * 1000, 1)} ÷ {fx(b, 2)} = ×{M:,} [2] (b) {img * 1000:,} μm ÷ {M:,} = {a_txt} [2]', 'numerical', 4)


# ===================================================================== 1 Cell structure
t = T('Light and electron microscopes: magnification, resolution and calculating actual size using eyepiece graticule and stage micrometer', 'light and electron microscopes')
facts(t, [('magnification', 'the number of times larger an image is than the real size of the object (image size ÷ actual size)'),
          ('resolution', 'the ability to distinguish between two separate points; the smallest distance between two points that can still be seen as separate'),
          ('eyepiece graticule', 'a transparent scale in the eyepiece of a light microscope, with arbitrary divisions that must be calibrated for each objective lens'),
          ('stage micrometer', 'a microscope slide with a scale of known divisions (often 0.01 mm = 10 μm each) used to calibrate an eyepiece graticule'),
          ('transmission electron microscope', 'a microscope in which a beam of electrons passes through a thin section, giving high-resolution images of internal structure'),
          ('scanning electron microscope', 'a microscope in which electrons are reflected from the surface of a specimen, giving a three-dimensional image of the surface'),
          ('nanometre', 'one thousandth of a micrometre (1 nm = 10⁻³ μm = 10⁻⁹ m)')])
mcqs(t, [('What is the approximate maximum resolution of a light microscope?', '200 nm', 'Limited by the wavelength of light (about 400–700 nm): about 200 nm (0.2 μm).', ['0.5 nm', '2 nm', '20 μm']),
         ('Why does an electron microscope have a higher resolution than a light microscope?', 'Electron beams have a much shorter wavelength than light', 'Resolution depends on wavelength; electrons have a much shorter wavelength.', ['Electrons can be focused with glass lenses', 'Electron microscopes use stains', 'Electron microscopes have more lenses']),
         ('Which structure can be seen with an electron microscope but not with a light microscope?', 'A ribosome', 'Ribosomes (about 20–25 nm) are below the resolution of a light microscope.', ['A nucleus', 'A chloroplast', 'A cell wall']),
         ('How many micrometres are in 0.25 mm?', '250 μm', '1 mm = 1000 μm.', ['25 μm', '2.5 μm', '2500 μm']),
         ('Why must an eyepiece graticule be recalibrated when the objective lens is changed?', 'The graticule scale stays the same but the specimen is magnified by a different amount', 'The graticule is in the eyepiece, so the value of each division depends on the objective.', ['The stage micrometer changes size', 'The resolution of the eyepiece changes', 'The light intensity changes'])])
shorts(t, [('State the formula linking actual size, image size and magnification.', 'Actual size = image size ÷ magnification (A = I ÷ M).', '[1]'),
           ('State two advantages of a light microscope compared with an electron microscope.', 'Living specimens can be viewed; natural colour / stains seen; cheaper and portable; simple preparation.', 'any two [2]')])
explain(t, [('Explain the difference between magnification and resolution.', 'Magnification is how many times larger the image is than the object; resolution is the ability to distinguish two close points as separate. Increasing magnification beyond the resolution limit gives no more detail.', 'magnification defined [1]; resolution defined [1]; more magnification gives no more detail beyond the resolution limit [1] [3]'),
            ('Explain why living cells cannot be viewed with a transmission electron microscope.', 'The specimen must be in a vacuum (electrons are scattered by air) and must be very thin, dehydrated and stained with heavy metals, which kills the cells.', 'vacuum [1]; preparation (thin sections / dehydration / heavy-metal stains) kills cells [1] [2]'),
            ('Describe how an eyepiece graticule is calibrated using a stage micrometer.', 'Place the stage micrometer on the stage and line up its scale with the graticule scale; count how many stage micrometer divisions match a number of graticule divisions; calculate the length of one graticule division (e.g. in μm); repeat for each objective lens.', 'line up scales [1]; count matching divisions [1]; calculate value of one division [1] [3]'),
            ('Explain why a scanning electron micrograph shows the surface of a cell but not its organelles.', 'In SEM the electron beam is reflected (scattered) from the surface rather than passing through the specimen, so it gives a 3-D image of the surface only.', 'electrons reflected from surface [1]; no internal detail / 3-D surface image [1] [2]'),
            ('Explain why images from an electron microscope are in black and white, though they are often coloured afterwards.', 'Electrons are not visible light and have no colour; the image is formed on a screen from electrons hitting it, so false colour is added by computer.', 'electrons have no colour / not visible light [1]; false colour added [1] [2]')])
myths(t, [('An electron microscope has a higher resolution because it has a higher magnification.', 'Its higher resolution is due to the shorter wavelength of electrons; magnification alone does not increase resolution.'),
          ('One division on an eyepiece graticule is always 10 μm.', 'Graticule divisions are arbitrary; their value depends on the objective lens and must be calibrated with a stage micrometer.'),
          ('To calculate actual size you multiply the image size by the magnification.', 'Actual size = image size ÷ magnification.')])

CELLS_1 = [('a lymphocyte', 7, 12), ('a palisade mesophyll cell', 30, 80), ('a guard cell', 20, 45), ('a red blood cell', 6.5, 8.5), ('a cheek epithelial cell', 40, 70),
           ('an onion epidermal cell', 120, 250), ('a root tip meristem cell', 10, 25), ('a Paramecium', 120, 280), ('a pollen grain', 20, 60), ('a xylem vessel element (width)', 30, 120)]
ORGANELLE_SIZES = [('a mitochondrion', 1, 4), ('a chloroplast', 3, 8), ('a nucleus', 6, 15), ('a ribosome', 0.02, 0.03), ('a bacterium', 1, 5), ('a lysosome', 0.2, 0.8),
                   ('a centriole (length)', 0.3, 0.5), ('a Golgi vesicle', 0.05, 0.1), ('a starch grain', 2, 10), ('a microvillus (length)', 0.8, 1.5)]


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def magnif(r, D):
    return mag_item(r, D, CELLS_1 + ORGANELLE_SIZES)


@t.add('C1', (1, 2, 3), 'mcq')
def unit_conv(r, D):
    v = r.choice([0.002, 0.04, 0.35, 1.2, 2.5, 7.5, 15, 25, 120, 450])
    m = r.randrange(3)
    if m == 0:
        return NQ(r, f'Convert {fx(v, 3)} mm into micrometres.', v * 1000, [v * 100, v * 10000, v / 1000], ' μm', '1 mm = 1000 μm.', f=lambda z: fx(z, 4))
    if m == 1:
        return NQ(r, f'Convert {fx(v, 3)} μm into nanometres.', v * 1000, [v * 100, v * 10, v / 1000], ' nm', '1 μm = 1000 nm.', f=lambda z: fx(z, 4))
    return NQ(r, f'A structure is {fx(v * 1000, 3)} nm long. What is this length in micrometres?', v, [v * 1000, v * 10, v / 10], ' μm', '1000 nm = 1 μm.', f=lambda z: fx(z, 4))


def _calib(r):
    for _ in range(40):
        val = r.choice([1.25, 2.5, 4, 5, 10, 12.5, 25])
        N = r.choice([20, 40, 50, 80, 100])
        S = N * val / 10
        if S == int(S) and 2 <= S <= 100:
            return val, N, int(S)
    return 2.5, 40, 10


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def graticule(r, D):
    val, N, S = _calib(r)
    obj = {1.25: '×100 (oil immersion)', 2.5: '×40', 4: '×25', 5: '×20', 10: '×10', 12.5: '×8', 25: '×4'}[val]
    cell, lo, hi = r.choice(CELLS_1)
    k = round(r.uniform(lo, hi) / val)
    if k < 4 or k > 100:
        return None
    size = k * val
    p = person(r)
    intro = f'{p} calibrates an eyepiece graticule using a stage micrometer with divisions of 0.01 mm. With the {obj} objective, {N} eyepiece graticule divisions line up exactly with {S} stage micrometer divisions.'
    if D == 1:
        return NQ(r, intro + ' What is the length of one eyepiece graticule division?', val, [S / N, N / S * 10, val * 10, val / 10], ' μm',
                  f'{S} × 10 μm = {S * 10} μm; ÷ {N} = {fx(val, 2)} μm per division.', f=lambda z: fx(z, 3))
    st = intro + f' (a) Calculate the length of one eyepiece graticule division in μm. (b) {cap(cell)} measures {k} eyepiece divisions. Calculate its actual length.'
    ans = f'(a) {fx(val, 2)} μm (b) {fx(size, 2)} μm'
    key = f'(a) {S} divisions × 10 μm = {S * 10} μm [1]; ÷ {N} = {fx(val, 2)} μm [1] (b) {k} × {fx(val, 2)} = {fx(size, 2)} μm [1]'
    m = 3
    if D >= 3:
        M = r.choice([x for x in (100, 200, 250, 400, 500, 1000) if 20 <= size * x / 1000 <= 150] or [None])
        if M:
            st += f' (c) {p} draws the cell {fx(size * M / 1000, 1)} mm long. Calculate the magnification of the drawing.'
            ans += f' (c) ×{M}'
            key += f' (c) {fx(size * M / 1000, 1)} mm = {fx(size * M, 0)} μm; ÷ {fx(size, 2)} = ×{M} [2]'
            m += 2
    if D >= 4:
        st += ' (d) Explain why the calibration must be repeated if the objective lens is changed.'
        ans += ' (d) The graticule is in the eyepiece, so its scale is not magnified by the objective; each division represents a different actual length at each magnification.'
        key += ' (d) graticule not magnified by objective [1]; value of each division changes [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (2, 3, 4, 5), 'case')
def micro_case(r, D):
    val, N, S = _calib(r)
    cell, lo, hi = r.choice(CELLS_1)
    ks = [round(r.uniform(lo, hi) / val) for _ in range(5)]
    if min(ks) < 4 or max(ks) > 100:
        return None
    mean = sum(ks) / 5 * val
    intro = (f'{person(r)} in {city(r)} measures five examples of {cell} using an eyepiece graticule. At the magnification used, {N} graticule divisions equal {S} divisions of a stage micrometer '
             f'(1 division = 10 μm). The lengths in graticule divisions were {", ".join(map(str, ks))}.')
    parts = [lambda r: ('Calculate the mean actual length of the cells in μm.', f'{fx(mean, 1)} μm', f'one division = {S * 10} ÷ {N} = {fx(val, 2)} μm [1]; mean divisions = {fx(sum(ks) / 5, 1)} [1]; × {fx(val, 2)} = {fx(mean, 1)} μm [1] [3]'),
             lambda r: ('Explain why five cells were measured rather than one.', 'Cells vary in size; a mean of several gives a more representative / reliable value.', 'variation between cells [1]; mean more representative [1] [2]'),
             lambda r: ('State one source of error when measuring with an eyepiece graticule and suggest how to reduce it.', 'Cell edges may not line up with divisions / estimating part divisions; use a higher magnification or measure more cells.', 'error [1]; improvement [1] [2]'),
             lambda r: ('Suggest why the cells could not be measured accurately using the scale on a ruler held against the eyepiece.', 'The ruler is not in the optical path; its scale is not superimposed on the image and is not calibrated against a known length.', '[1]'),
             lambda r: ('Explain why these cells could be studied with a light microscope but their ribosomes could not.', 'The cells are larger than the resolution of a light microscope (about 200 nm); ribosomes (about 25 nm) are smaller than this, so need an electron microscope.', 'resolution limit 200 nm [1]; ribosomes smaller [1] [2]'),
             lambda r: ('Compare the preparation of a specimen for a light microscope with preparation for a transmission electron microscope.', 'LM: thin section or smear, water mount, coloured stains, can be living. TEM: very thin section, dehydrated, heavy-metal stains, in vacuum, must be dead.', 'two valid comparisons [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


longs(t, [('Compare light microscopes and electron microscopes, with reference to magnification, resolution and the specimens that can be viewed.', 'LM: light (wavelength 400–700 nm), resolution about 200 nm, magnification up to ×1500, living or dead specimens, colour stains, cheap. EM: electrons (short wavelength), resolution about 0.5 nm, magnification up to ×500 000, vacuum so dead specimens, heavy-metal stains, black and white images, TEM sections vs SEM surfaces, expensive.',
           'resolution values [2]; reason (wavelength) [1]; magnification values [1]; specimens living / dead and preparation [1]; TEM vs SEM [1] [6]'),
          ('Describe how you would use a light microscope, eyepiece graticule and stage micrometer to determine the mean diameter of cells in a prepared slide.', 'Calibrate graticule: line up with stage micrometer, find value of one division for the objective; replace with specimen slide; measure diameter of each cell in graticule divisions; measure at least 5–10 cells chosen at random; convert to μm; calculate mean.',
           'calibration steps [2]; same objective [1]; measure several cells / random [1]; convert divisions to μm [1]; mean [1] [6]')])
t1a = t

ORG = {'nucleus': ('contains chromosomes (DNA) and controls the cell; site of transcription; nucleolus makes ribosomes', 'surrounded by a double membrane (nuclear envelope) with nuclear pores'),
       'rough endoplasmic reticulum': ('synthesis of proteins (by attached ribosomes) and transport of proteins to the Golgi body', 'a network of flattened membrane-bound sacs (cisternae) with ribosomes on the outer surface'),
       'smooth endoplasmic reticulum': ('synthesis of lipids and steroids such as cholesterol and steroid hormones', 'a network of membrane-bound tubules without ribosomes'),
       'Golgi body': ('modifies proteins (e.g. adds carbohydrate to make glycoproteins), packages them into vesicles and makes lysosomes', 'a stack of curved, flattened membrane sacs (cisternae) with vesicles at the edges'),
       'mitochondrion': ('site of aerobic respiration (Krebs cycle and oxidative phosphorylation) producing ATP', 'double membrane, the inner one folded into cristae, with a matrix containing 70S ribosomes and circular DNA'),
       'ribosome': ('site of protein synthesis (translation)', 'two subunits of rRNA and protein, not membrane-bound; 80S in cytoplasm, 70S in mitochondria and chloroplasts'),
       'lysosome': ('contains hydrolytic enzymes that digest worn-out organelles, engulfed material and whole cells', 'a spherical vesicle surrounded by a single membrane'),
       'chloroplast': ('site of photosynthesis', 'double membrane, internal membranes (thylakoids) stacked into grana, stroma containing starch grains, 70S ribosomes and circular DNA'),
       'centriole': ('involved in forming the spindle during nuclear division in animal cells', 'a hollow cylinder of nine triplets of microtubules; found in pairs in the centrosome'),
       'microvilli': ('increase the surface area of the cell surface membrane for absorption', 'finger-like extensions of the cell surface membrane'),
       'cilia': ('beat to move fluid or mucus along a surface', 'hair-like extensions of the cell surface membrane containing a 9 + 2 arrangement of microtubules'),
       'cell wall': ('gives mechanical strength and prevents the cell bursting in dilute solutions', 'made of cellulose microfibrils in plants; fully permeable'),
       'large permanent vacuole': ('stores cell sap and keeps the cell turgid', 'a fluid-filled sac surrounded by a membrane called the tonoplast'),
       'plasmodesmata': ('allow cytoplasm and substances to pass directly between neighbouring plant cells', 'narrow channels through plant cell walls lined by cell surface membrane')}
ANIMAL_ONLY = ['centriole', 'microvilli', 'cilia']
PLANT_ONLY = ['chloroplast', 'cell wall', 'large permanent vacuole', 'plasmodesmata']
SPECIAL = [('a pancreatic acinar cell secreting digestive enzymes', 'rough endoplasmic reticulum and Golgi body', 'large amounts of protein are made on the RER and packaged into secretory vesicles by the Golgi body'),
           ('a sperm cell swimming to an egg', 'mitochondria', 'aerobic respiration provides ATP for movement of the flagellum'),
           ('a liver cell detoxifying drugs and making cholesterol', 'smooth endoplasmic reticulum', 'lipids and steroids are made and toxins are broken down in the SER'),
           ('a neutrophil that ingests bacteria', 'lysosomes', 'lysosomes fuse with phagocytic vesicles and their hydrolytic enzymes digest the bacteria'),
           ('a palisade mesophyll cell', 'chloroplasts', 'chloroplasts absorb light for photosynthesis'),
           ('an epithelial cell lining the small intestine', 'microvilli and mitochondria', 'microvilli increase surface area for absorption and mitochondria supply ATP for active transport'),
           ('a ciliated cell in the trachea', 'cilia and mitochondria', 'cilia beat to move mucus, using ATP from many mitochondria'),
           ('a plasma cell producing antibodies', 'rough endoplasmic reticulum and Golgi body', 'antibodies are glycoproteins made on the RER and modified and packaged by the Golgi body'),
           ('a cell in the adrenal cortex secreting steroid hormones', 'smooth endoplasmic reticulum', 'steroid hormones are lipids synthesised by the SER'),
           ('a heart muscle cell', 'mitochondria', 'continuous contraction requires a large supply of ATP from aerobic respiration'),
           ('a root hair cell absorbing mineral ions', 'mitochondria', 'active transport of ions against their concentration gradient needs ATP')]
facts(t := T('Ultrastructure of animal and plant cells and functions of organelles', 'ultrastructure of animal and plant cells'),
      [(k, v[0]) for k, v in ORG.items() if k not in ('cilia', 'microvilli')] + [('ATP', 'the universal energy currency of cells, made mainly in mitochondria by aerobic respiration')])


@t.add('C1', (1, 2, 3), 'mcq')
def org_struct(r, D):
    name = r.choice(list(ORG))
    others = [k for k in ORG if k != name]
    st = r.choice(['An electron micrograph shows an organelle with this structure:', 'Which organelle is described here?', 'Identify the cell structure with the following features:'])
    return MQ(r, f'{st} "{ORG[name][1]}".', cap(name), [cap(o) for o in others], f'{cap(name)}: {ORG[name][1]}.')


@t.add('C1', (1, 2, 3), 'mcq')
def org_where(r, D):
    m = r.randrange(3)
    if m == 0:
        a = r.choice(PLANT_ONLY)
        return MQ(r, 'Which structure is found in a typical plant cell but not in a typical animal cell?', cap(a), [cap(x) for x in ['mitochondrion', 'Golgi body', 'ribosome', 'nucleus', 'centriole', 'lysosome']], f'{cap(a)} is a plant-cell structure.')
    if m == 1:
        a = r.choice(ANIMAL_ONLY)
        return MQ(r, 'Which structure is found in some animal cells but not in typical plant cells?', cap(a), [cap(x) for x in ['cell wall', 'chloroplast', 'large permanent vacuole', 'plasmodesmata', 'nucleus']], f'{cap(a)} occur in animal cells only.')
    a = r.choice(['mitochondrion', 'chloroplast'])
    return MQ(r, 'Which organelle contains circular DNA and 70S ribosomes and is surrounded by a double membrane, and is found in both plant and animal cells?', 'Mitochondrion', ['Chloroplast', 'Golgi body', 'Lysosome', 'Rough endoplasmic reticulum'], 'Mitochondria occur in both cell types; chloroplasts are plant only.')


@t.add('C3', (1, 2, 3, 4), 'short')
def org_suggest(r, D):
    a, b = r.sample(SPECIAL, 2)
    if D == 1:
        wrong = list({x[1] for x in SPECIAL if x[1] != a[1]})
        return MQ(r, f'Which organelles would you expect to be especially numerous in {a[0]}?', cap(a[1]), [cap(w) for w in wrong], f'{cap(a[1])}: {a[2]}.')
    st = f'Suggest which organelles would be present in large numbers in {a[0]}, and explain why.'
    key = f'{a[1]} [1]; {a[2]} [1] [2]'
    if D >= 3:
        st = f'Suggest and explain which organelles would be particularly numerous in (i) {a[0]} (ii) {b[0]}.'
        return Q(st, f'(i) {cap(a[1])}: {a[2]}. (ii) {cap(b[1])}: {b[2]}.', f'(i) {a[1]} [1]; reason [1] (ii) {b[1]} [1]; reason [1] [4]', 'short')
    return Q(st, f'{cap(a[1])}: {a[2]}.', key, 'short')


@t.add('C3', (2, 3, 4, 5), 'case')
def org_volume(r, D):
    types = [('liver cell', 22), ('heart muscle cell', 36), ('pancreatic acinar cell', 8), ('fat storage cell', 3), ('sperm midpiece', 45), ('skin epidermal cell', 6)]
    pick = r.sample(types, 3)
    vals = [(n, round(v * r.uniform(0.85, 1.15), 1)) for n, v in pick]
    vol = r.choice([1500, 2000, 2500, 3000, 4000])
    hi = max(vals, key=lambda x: x[1])
    intro = f'Scientists in {city(r)} estimated the percentage of cell volume occupied by mitochondria in three cell types: ' + '; '.join(f'{n} {v}%' for n, v in vals) + '.'
    parts = [lambda r: (f'A {vals[0][0]} has a volume of {vol} μm³. Calculate the volume occupied by its mitochondria.', f'{fx(vol * vals[0][1] / 100, 1)} μm³', f'{vals[0][1]} ÷ 100 × {vol} [1] = {fx(vol * vals[0][1] / 100, 1)} μm³ [1] [2]'),
             lambda r: (f'Calculate how many times greater the percentage is in the {hi[0]} than in the cell type with the lowest value.', f'{fx(hi[1] / min(v for _, v in vals), 1)}', f'{hi[1]} ÷ {min(v for _, v in vals)} = {fx(hi[1] / min(v for _, v in vals), 1)} [2]'),
             lambda r: (f'Suggest why the {hi[0]} has the highest proportion of mitochondria.', 'It has a high demand for ATP (e.g. contraction / movement / active processes), supplied by aerobic respiration in mitochondria.', 'high ATP demand linked to function [1]; aerobic respiration in mitochondria [1] [2]'),
             lambda r: ('Describe the structure of a mitochondrion as seen in an electron micrograph.', 'Double membrane (envelope); inner membrane folded into cristae; matrix containing 70S ribosomes, circular DNA and granules.', 'double membrane [1]; cristae [1]; matrix with ribosomes / DNA [1] [3]'),
             lambda r: ('Explain why mitochondria cannot be seen in detail with a light microscope.', 'They are only about 1 μm wide, close to the resolution limit of a light microscope (about 0.2 μm), so internal cristae cannot be resolved.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


mcqs(t, [('Which sequence shows the route taken by an extracellular protein from its site of synthesis to secretion?', 'Ribosome on RER → RER → vesicle → Golgi body → vesicle → cell surface membrane',
          'Protein made on ribosomes of RER, transported in vesicles to the Golgi body, modified and packaged into secretory vesicles which fuse with the cell surface membrane (exocytosis).',
          ['Golgi body → RER → vesicle → lysosome → cell surface membrane', 'Ribosome in cytoplasm → nucleus → Golgi body → cell surface membrane', 'Smooth ER → lysosome → Golgi body → vesicle → cell surface membrane']),
         ('Which organelle is surrounded by a single membrane?', 'Lysosome', 'Nucleus, mitochondrion and chloroplast have double membranes; lysosome has one.', ['Nucleus', 'Mitochondrion', 'Chloroplast']),
         ('Which structure does not have a membrane?', 'Ribosome', 'Ribosomes and centrioles are non-membrane-bound.', ['Golgi body', 'Lysosome', 'Smooth endoplasmic reticulum'])])
shorts(t, [('State the function of the nucleolus.', 'Makes ribosomes (synthesises rRNA and assembles ribosomal subunits).', '[1]'),
           ('State two structural differences between the rough and smooth endoplasmic reticulum.', 'RER has ribosomes on its surface, SER does not; RER is mainly flattened sacs (cisternae), SER is mainly tubules.', '[2]')])
explain(t, [('Explain how the RER and Golgi body work together to produce glycoproteins for secretion.', 'Polypeptides made by ribosomes on RER enter the cisternae and are folded; vesicles carry them to the Golgi body, which adds carbohydrate and modifies them; they are packaged into secretory vesicles that fuse with the cell surface membrane.', 'protein made on RER [1]; vesicles to Golgi [1]; carbohydrate added / modified [1]; secretory vesicles / exocytosis [1] [4]'),
            ('Explain why ATP is described as the universal energy currency.', 'ATP is used in all cells as the immediate source of energy for processes such as active transport and protein synthesis; it is made in respiration and hydrolysed to ADP + Pi, releasing energy in small, manageable amounts.', 'used by all cells / all processes [1]; hydrolysis releases energy in small amounts [1] [2]'),
            ('Explain the role of the nuclear pores.', 'They allow large molecules such as mRNA and ribosomal subunits to leave the nucleus and molecules such as nucleotides and enzymes to enter.', 'mRNA / ribosomes out [1]; substances in [1] [2]'),
            ('Explain why lysosomes are important in cells such as phagocytes.', 'Lysosomes fuse with phagocytic vesicles containing bacteria and release hydrolytic enzymes that digest them.', 'fuse with phagocytic vesicle [1]; hydrolytic enzymes digest [1] [2]'),
            ('Describe the role of centrioles in an animal cell.', 'Centrioles in the centrosome organise microtubules to form the spindle that separates chromosomes during nuclear division; they also form basal bodies of cilia.', 'spindle / microtubule organising [1]; separating chromosomes in division [1] [2]')])
myths(t, [('Plant cells do not have mitochondria because they have chloroplasts.', 'Plant cells have both mitochondria and chloroplasts; they respire all the time.'),
          ('The Golgi body makes proteins.', 'Proteins are made by ribosomes (often on RER); the Golgi body modifies and packages them.'),
          ('Ribosomes are surrounded by a single membrane.', 'Ribosomes are not membrane-bound; they are made of rRNA and protein.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def secretion_case(r, D):
    prot, cell = r.choice([('insulin', 'a β cell in the islets of Langerhans'), ('amylase', 'a salivary gland cell'), ('trypsinogen', 'a pancreatic acinar cell'), ('antibodies', 'a plasma cell'), ('mucin (a glycoprotein)', 'a goblet cell')])
    t_ = r.choice([3, 5, 10, 20])
    intro = f'Researchers in {city(r)} supplied {cell} with radioactively labelled amino acids for {t_} minutes and then tracked the radioactivity as the cell made and secreted {prot}.'
    parts = [lambda r: ('State, in order, the organelles in which the radioactivity would appear.', 'Ribosomes on RER → RER cisternae → transport vesicles → Golgi body → secretory vesicles → (outside cell).', 'RER [1]; Golgi [1]; secretory vesicles [1] [3]'),
             lambda r: ('Explain why the radioactivity first appears in the rough endoplasmic reticulum.', 'Amino acids are joined into polypeptides by ribosomes attached to the RER, and the polypeptide enters the RER lumen.', '[2]'),
             lambda r: (f'Describe how {prot} leaves the cell.', 'By exocytosis: secretory vesicles move to and fuse with the cell surface membrane, releasing the contents; this requires ATP.', 'vesicles fuse with membrane [1]; exocytosis / ATP [1] [2]'),
             lambda r: ('Suggest why this cell contains many mitochondria.', 'To provide ATP for protein synthesis, vesicle movement and exocytosis.', '[2]'),
             lambda r: ('Explain why the cell would also contain a large nucleolus.', 'The nucleolus makes ribosomes; many ribosomes are needed for the high rate of protein synthesis.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of a typical plant cell as seen with an electron microscope and compare it with a typical animal cell.', 'Both: nucleus with envelope and pores, nucleolus, RER, SER, Golgi, mitochondria, 80S ribosomes, cell surface membrane. Plant only: cellulose cell wall, plasmodesmata, chloroplasts with grana, large permanent vacuole with tonoplast. Animal only: centrioles, sometimes microvilli and cilia; small temporary vacuoles; glycogen rather than starch.',
           'four shared structures [2]; plant-only features [2]; animal-only features [1]; storage carbohydrate / vacuole contrast [1] [6]'),
          ('Explain how the structure of mitochondria and chloroplasts suggests that they evolved from prokaryotic cells.', 'Both have double membranes, circular DNA not associated with histones, 70S ribosomes like prokaryotes, divide by binary fission, similar size to bacteria (endosymbiont theory).', 'double membrane [1]; circular DNA [1]; 70S ribosomes [1]; size / division [1]; endosymbiosis explained [1] [5]')])
t1b = t

PRO = [('cell wall made of peptidoglycan (murein)', 'prokaryote'), ('circular DNA free in the cytoplasm', 'prokaryote'), ('70S ribosomes only', 'prokaryote'), ('plasmids', 'prokaryote'),
       ('no membrane-bound organelles', 'prokaryote'), ('DNA associated with histone proteins in linear chromosomes', 'eukaryote'), ('a nucleus with a nuclear envelope', 'eukaryote'),
       ('80S ribosomes in the cytoplasm', 'eukaryote'), ('mitochondria and endoplasmic reticulum', 'eukaryote'), ('a diameter of about 40 μm', 'eukaryote'), ('a diameter of about 2 μm', 'prokaryote')]
t = T('Prokaryotic cells compared with eukaryotic cells', 'prokaryotic cells compared with eukaryotic cells')
facts(t, [('prokaryote', 'an organism whose cells have no nucleus or membrane-bound organelles, such as a bacterium'), ('eukaryote', 'an organism whose cells contain a nucleus and membrane-bound organelles'),
          ('plasmid', 'a small circular loop of DNA in bacteria, separate from the main chromosome, often carrying genes such as antibiotic resistance'),
          ('peptidoglycan', 'the polymer of sugars and amino acids (murein) that makes up bacterial cell walls'), ('capsule', 'a slimy outer layer around some bacteria that protects them and helps them stick to surfaces'),
          ('70S ribosome', 'the smaller type of ribosome found in prokaryotes, mitochondria and chloroplasts')])


@t.add('C1', (1, 2, 3), 'mcq')
def pro_feat(r, D):
    m = r.randrange(3)
    if m == 0:
        a = r.choice([f for f, k in PRO if k == 'prokaryote'])
        return MQ(r, 'Which feature is found in prokaryotic cells but not in eukaryotic cells?', cap(a), [cap(f) for f, k in PRO if k == 'eukaryote'], f'{cap(a)} is a prokaryotic feature.')
    if m == 1:
        a = r.choice([f for f, k in PRO if k == 'eukaryote'])
        return MQ(r, 'Which feature is found in eukaryotic cells but not in prokaryotic cells?', cap(a), [cap(f) for f, k in PRO if k == 'prokaryote'], f'{cap(a)} is a eukaryotic feature.')
    a = r.choice(['ribosomes', 'a cell surface membrane', 'DNA', 'cytoplasm'])
    return MQ(r, 'Which structure is present in both prokaryotic and eukaryotic cells?', cap(a), ['A nuclear envelope', 'Mitochondria', 'Golgi body', 'Endoplasmic reticulum', 'Chromosomes with histones'], 'Both have ribosomes, cell surface membrane, cytoplasm and DNA.')


@t.add('C3', (2, 3, 4), 'short')
def pro_classify(r, D):
    p = r.random() < 0.5
    pool = [f for f, k in PRO if (k == 'prokaryote') == p]
    feats = r.sample(pool, 2) + [r.choice(['a cell surface membrane', 'ribosomes', 'cytoplasm'])]
    org = r.choice(['a cell found in a soil sample', 'a cell isolated from a hot spring', 'a cell from a pond water sample', 'a cell grown from a throat swab'])
    kind = 'prokaryotic' if p else 'eukaryotic'
    st = f'A scientist in {city(r)} examines {org} with an electron microscope and records: {"; ".join(feats)}. State whether the cell is prokaryotic or eukaryotic and give two reasons from the observations.'
    return Q(st, f'{cap(kind)}: {feats[0]}; {feats[1]}.', f'{kind} [1]; two correct reasons from the observations (not the shared feature) [2] [3]', 'short')


@t.add('C3', (1, 2, 3, 4), 'numerical')
def pro_size(r, D):
    b = round(r.uniform(0.8, 4), 1)
    e = r.choice([10, 15, 20, 30, 50, 80, 100])
    if D == 1:
        return NQ(r, f'A bacterium is {b} μm long and a liver cell is {e} μm wide. How many times wider is the liver cell?', e / b, [b / e, e - b, e * b], '', f'{e} ÷ {b} = {fx(e / b, 1)}.', f=lambda v: fx(v, 1))
    vb = 4 / 3 * math.pi * (b / 2) ** 3
    ve = 4 / 3 * math.pi * (e / 2) ** 3
    st = f'A spherical bacterium (coccus) has a diameter of {b} μm and a spherical eukaryotic cell has a diameter of {e} μm. (a) Calculate how many times larger the diameter of the eukaryotic cell is. (b) Using V = 4/3 πr³, calculate how many times larger its volume is.'
    ans = f'(a) {fx(e / b, 1)} (b) {sf(ve / vb, 3)}'
    key = f'(a) {e} ÷ {b} = {fx(e / b, 1)} [1] (b) volumes {sf(ve, 3)} μm³ and {sf(vb, 3)} μm³ [1]; ratio {sf(ve / vb, 3)} (= ratio of diameters cubed) [1]'
    m = 3
    if D >= 3:
        st += ' (c) Explain why prokaryotic cells do not need specialised transport systems inside the cell.'
        ans += ' (c) Their small size gives a large surface area to volume ratio and short diffusion distances, so diffusion is fast enough.'
        key += ' (c) large SA:V [1]; short diffusion distance [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


mcqs(t, [('Which type of ribosome is found in the cytoplasm of a bacterial cell?', '70S', 'Prokaryotes have 70S ribosomes; eukaryotic cytoplasm has 80S.', ['80S', '60S', '90S']),
         ('Which substance makes up the cell wall of a bacterium?', 'Peptidoglycan', 'Bacterial walls: peptidoglycan (murein); plants: cellulose; fungi: chitin.', ['Cellulose', 'Chitin', 'Lignin'])])
shorts(t, [('State three structures found in a typical bacterial cell that are not found in a typical animal cell.', 'Cell wall (peptidoglycan); plasmids; capsule; circular DNA free in cytoplasm; flagellum of prokaryotic type; pili.', 'any three [3]'),
           ('State the role of plasmids in bacteria.', 'Carry extra genes (e.g. antibiotic resistance) that can be passed to other bacteria.', '[1]')])
explain(t, [('Explain why antibiotics that target 70S ribosomes can be used to treat bacterial infections in humans.', 'Bacteria have 70S ribosomes but human cytoplasm has 80S ribosomes, so bacterial protein synthesis is inhibited without harming human cells (mostly).', '70S vs 80S [1]; selective inhibition of bacterial protein synthesis [1] [2]'),
            ('Compare the genetic material of a prokaryote with that of a eukaryote.', 'Prokaryote: circular DNA free in cytoplasm (nucleoid), no histones, plasmids may be present. Eukaryote: linear DNA in chromosomes in a nucleus, associated with histones.', 'circular vs linear [1]; no nucleus vs nucleus [1]; histones [1] [3]'),
            ('Explain why bacteria cannot carry out the modification of proteins in the same way as eukaryotic cells.', 'They lack membrane-bound organelles such as the RER and Golgi body, which modify and package proteins (e.g. adding carbohydrate).', 'no RER / Golgi [1]; these modify proteins [1] [2]')])
myths(t, [('Bacteria have no ribosomes because they have no endoplasmic reticulum.', 'Bacteria have 70S ribosomes free in the cytoplasm.'), ('Prokaryotic cells have no DNA because they have no nucleus.', 'Prokaryotes have circular DNA free in the cytoplasm (and often plasmids).'),
          ('Bacterial cell walls are made of cellulose, like plant cells.', 'Bacterial cell walls are made of peptidoglycan (murein).')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def pro_case(r, D):
    org = r.choice(['Escherichia coli', 'Streptococcus pneumoniae', 'Vibrio cholerae', 'Staphylococcus aureus'])
    L = round(r.uniform(1.0, 3.0), 1)
    M = r.choice([10000, 15000, 20000, 25000])
    intro = f'A transmission electron micrograph of {org} at ×{M:,} shows a cell wall, a capsule, a circular DNA molecule, plasmids, 70S ribosomes and a flagellum. The cell is {fx(L * M / 1000, 1)} mm long in the micrograph.'
    parts = [lambda r: ('Calculate the actual length of the cell in μm.', f'{fx(L, 2)} μm', f'{fx(L * M / 1000, 1)} mm = {fx(L * M, 0)} μm; ÷ {M:,} = {fx(L, 2)} μm [2]'),
             lambda r: ('List three ways in which this cell differs from a cell from the human lining of the trachea.', 'No nucleus (DNA free / circular); peptidoglycan wall; capsule; 70S not 80S ribosomes; plasmids; no membrane-bound organelles; prokaryotic flagellum not cilia.', 'any three [3]'),
             lambda r: ('State the function of the capsule.', 'Protects the bacterium (from phagocytosis / drying out) and helps it stick to surfaces.', '[1]'),
             lambda r: ('Explain why the bacterium is classified as a prokaryote.', 'It has no nucleus and no membrane-bound organelles; its DNA is free in the cytoplasm.', '[2]'),
             lambda r: ('Suggest why the presence of plasmids may make infections with this bacterium more difficult to treat.', 'Plasmids may carry antibiotic-resistance genes that can be transferred to other bacteria.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Compare the structure of a prokaryotic cell with that of a eukaryotic animal cell.', 'Prokaryote: 0.5–5 μm, no nucleus, circular DNA without histones, plasmids, 70S ribosomes, peptidoglycan wall, sometimes capsule / pili / flagellum, no membrane-bound organelles. Eukaryote: 10–100 μm, nucleus with envelope, linear chromosomes with histones, 80S ribosomes, no wall, membrane-bound organelles (mitochondria, ER, Golgi, lysosomes). Both: cell surface membrane, cytoplasm, ribosomes, DNA.',
           'similarities [1]; size [1]; nucleus / DNA form [1]; ribosomes [1]; wall [1]; organelles [1] [6]')])
t1c = t

t = T('Viruses: structure and non-cellular nature', 'viruses')
facts(t, [('virus', 'a non-cellular infectious particle made of nucleic acid surrounded by a protein coat, which can only reproduce inside a host cell'),
          ('capsid', 'the protein coat of a virus, made of protein subunits called capsomeres'), ('capsomere', 'one of the protein subunits that make up a viral capsid'),
          ('envelope', 'an outer layer of phospholipid membrane, taken from the host cell, found around some viruses such as HIV and influenza'),
          ('bacteriophage', 'a virus that infects bacteria')])
mcqs(t, [('Why are viruses described as non-cellular?', 'They have no cytoplasm, ribosomes or cell membrane of their own', 'Viruses have only nucleic acid and a protein coat (sometimes an envelope); they cannot metabolise.', ['They are smaller than bacteria', 'They contain RNA instead of DNA', 'They cause disease']),
         ('Which genetic material can be found in viruses?', 'DNA or RNA, but not both', 'A virus contains either DNA or RNA.', ['DNA only', 'RNA only', 'Both DNA and RNA']),
         ('What is the typical size range of viruses?', '20–300 nm', 'Most viruses are 20–300 nm, too small for light microscopes.', ['1–5 μm', '10–100 μm', '0.1–1 nm'])])
shorts(t, [('State the three structures that may make up a virus particle.', 'Nucleic acid (DNA or RNA), protein coat (capsid), and in some an envelope (phospholipid).', '[2]'),
           ('State why viruses can only be seen with an electron microscope.', 'They are smaller (20–300 nm) than the resolution limit of a light microscope (about 200 nm).', '[1]')])
explain(t, [('Explain why viruses are described as obligate parasites.', 'They have no metabolism or ribosomes of their own, so they can only reproduce inside a host cell using its enzymes, ribosomes and ATP.', 'no metabolism / ribosomes [1]; must use host cell to reproduce [1] [2]'),
            ('Explain why antibiotics are not effective against viruses.', 'Antibiotics target bacterial structures or processes (cell walls, 70S ribosomes) that viruses do not have; viruses reproduce inside host cells.', 'no cell wall / ribosomes / metabolism [1]; inside host cells [1] [2]'),
            ('Explain how the envelope of HIV helps it infect host cells.', 'The envelope contains glycoproteins that bind to CD4 receptors on T helper cells; the envelope fuses with the cell surface membrane so the capsid enters the cell.', 'glycoproteins bind receptors [1]; fusion with membrane [1] [2]')])
myths(t, [('Viruses are very small bacteria.', 'Viruses are non-cellular particles with no cytoplasm or ribosomes; bacteria are prokaryotic cells.'), ('All viruses contain DNA.', 'Some viruses, such as HIV, measles and influenza, contain RNA instead.')])
VIRUSES = [('a tobacco mosaic virus particle (length)', 0.28, 0.32), ('an influenza virus', 0.08, 0.12), ('HIV', 0.1, 0.12), ('a measles virus', 0.12, 0.25), ('a bacteriophage T4 (length)', 0.18, 0.22), ('a poliovirus', 0.025, 0.032)]


@t.add('C3', (1, 2, 3, 4), 'numerical')
def virus_mag(r, D):
    return mag_item(r, D, VIRUSES)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def virus_case(r, D):
    v, nuc, host = r.choice([('HIV', 'RNA', 'T helper lymphocytes'), ('the measles virus', 'RNA', 'cells lining the respiratory tract'), ('influenza virus', 'RNA', 'epithelial cells of the airways'), ('a bacteriophage', 'DNA', 'bacteria'), ('tobacco mosaic virus', 'RNA', 'tobacco leaf cells')])
    d = r.choice([30, 60, 80, 100, 120, 200])
    intro = f'A student in {city(r)} reads that {v} contains {nuc}, has a diameter of about {d} nm and infects {host}.'
    parts = [lambda r: ('Calculate the diameter of the virus in μm.', f'{fx(d / 1000, 3)} μm', f'{d} ÷ 1000 = {fx(d / 1000, 3)} μm [1]'),
             lambda r: ('Explain why the virus cannot be seen with a light microscope.', f'{d} nm is below the resolution of a light microscope (about 200 nm), so the particle cannot be distinguished.', '[2]'),
             lambda r: ('Give three reasons why viruses are not considered to be living cells.', 'No cell membrane / cytoplasm; no ribosomes; no metabolism / respiration; cannot reproduce outside a host cell; crystallise.', 'any three [3]'),
             lambda r: ('Describe the structure of a typical virus particle.', 'Nucleic acid core (DNA or RNA) surrounded by a protein capsid made of capsomeres; some have a phospholipid envelope with glycoproteins.', '[3]'),
             lambda r: (f'Explain why {v} infects only {host}.', 'Proteins / glycoproteins on the virus surface are complementary to specific receptors found only on the surface of those cells.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of viruses and explain why they are not classified as living organisms.', 'Nucleic acid (DNA or RNA), capsid of capsomeres, some enveloped with glycoproteins; 20–300 nm. Not living: non-cellular, no cytoplasm / ribosomes / metabolism, reproduce only inside host cells, can be crystallised.', 'structure [3]; reasons not living [3] [6]')])
t1d = t
CHAPTERS[1] = [t1a, t1b, t1c, t1d]


# ===================================================================== 2 Biological molecules
TESTS = [('reducing sugar', "Benedict's test: add Benedict's solution and heat in a water bath at about 80 °C", 'blue → green / yellow / orange / brick-red precipitate'),
         ('starch', 'add iodine in potassium iodide solution', 'orange-brown → blue-black'),
         ('protein', 'biuret test: add biuret reagent (sodium hydroxide and copper(II) sulfate)', 'blue → purple / lilac'),
         ('lipid', 'emulsion test: shake with ethanol, then pour into water', 'clear → white (milky) emulsion'),
         ('non-reducing sugar', "after a negative Benedict's test, boil with dilute hydrochloric acid, neutralise with sodium hydrogencarbonate, then repeat the Benedict's test", 'blue → brick-red precipitate after acid hydrolysis')]
t = T('Monomers, polymers and macromolecules; condensation and hydrolysis; tests for biological molecules', 'monomers, polymers and macromolecules')
facts(t, [('monomer', 'a relatively simple molecule that is used as a basic building block for the synthesis of a polymer'), ('polymer', 'a giant molecule made from many similar repeating subunits (monomers) joined together'),
          ('macromolecule', 'a large biological molecule such as a protein, polysaccharide or nucleic acid'), ('condensation reaction', 'a reaction in which two molecules are joined together with the removal of a molecule of water'),
          ('hydrolysis', 'a reaction in which a bond is broken by the addition of a molecule of water'), ('reducing sugar', 'a sugar that can donate electrons to (reduce) another molecule, such as copper(II) ions in Benedict\'s solution')])


@t.add('C1', (1, 2, 3), 'mcq')
def test_id(r, D):
    sub, method, res = r.choice(TESTS)
    m = r.randrange(2)
    if m == 0:
        return MQ(r, f'Which test would be used to detect the presence of {sub} in a sample?', cap(method) + '.', [cap(x[1]) + '.' for x in TESTS if x[0] != sub], f'{cap(sub)}: {method}; positive result {res}.')
    return MQ(r, f'Which colour change shows a positive result in the test for {sub}?', cap(res), [cap(x[2]) for x in TESTS if x[0] not in (sub, 'non-reducing sugar', 'reducing sugar')] + ['Blue → colourless'], f'{cap(sub)}: {res}.')


@t.add('C3', (2, 3, 4), 'short')
def test_results(r, D):
    foods = {'glucose solution': {'reducing sugar'}, 'sucrose solution': {'non-reducing sugar'}, 'egg white': {'protein'}, 'vegetable oil': {'lipid'}, 'potato extract': {'starch'},
             'milk': {'reducing sugar', 'protein', 'lipid'}, 'onion juice': {'reducing sugar'}, 'flour suspension': {'starch', 'protein'}, 'peanut extract': {'lipid', 'protein'}}
    names = r.sample(list(foods), 3 if D <= 2 else 4)
    lab = 'PQRS'
    rows = []
    for L, n in zip(lab, names):
        c = foods[n]
        rows.append(f"{L}: Benedict's {'brick-red' if 'reducing sugar' in c else 'blue'}; iodine {'blue-black' if 'starch' in c else 'orange-brown'}; biuret {'purple' if 'protein' in c else 'blue'}; emulsion {'white emulsion' if 'lipid' in c else 'clear'}")
    st = f'{person(r)} tested {len(names)} unlabelled samples, {", ".join(lab[:len(names)])}. The results were: ' + '. '.join(rows) + '. The samples were ' + ', '.join(sorted(names)) + '. Identify each sample, giving a reason for each.'
    ans = '; '.join(f'{L} = {n}' for L, n in zip(lab, names))
    m = len(names)
    hint = ''
    if any('non-reducing sugar' in foods[n] for n in names):
        hint = ' Note: sucrose gives negative results for all four tests listed; a non-reducing sugar test (acid hydrolysis then Benedict\'s) would confirm it.'
    return Q(st, ans + '.' + hint, f'one mark per correct identification with reason linked to the test results [{m}]', 'short', m)


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def dilution(r, D):
    stock = r.choice([1.0, 2.0, 5.0, 10.0])
    unit = r.choice(['%', 'mmol dm⁻³', 'g dm⁻³'])
    V = r.choice([10, 20, 25, 50])
    sol = r.choice(['glucose', 'sucrose', 'starch', 'albumin', 'maltose'])
    fr = r.sample([0.1, 0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8], 3)
    fr.sort()
    targets = [stock * f for f in fr]
    if D == 1:
        c = targets[1]
        v = c / stock * V
        return NQ(r, f'A {fx(stock)} {unit} {sol} stock solution is diluted with distilled water to make {V} cm³ of a {fx(c, 3)} {unit} solution. What volume of stock solution is needed?', v, [V - v, c * V, V / c], ' cm³', f'C₁V₁ = C₂V₂: V₁ = {fx(c, 3)} × {V} ÷ {fx(stock)} = {fx(v, 2)} cm³.', f=lambda z: fx(z, 2))
    if D >= 4:
        n = r.choice([4, 5])
        dil = r.choice([2, 10])
        series = [stock / dil ** i for i in range(n)]
        st = (f'{person(r)} makes a serial dilution of a {fx(stock)} {unit} {sol} solution, diluting by a factor of {dil} at each step and making {V} cm³ of each solution. '
              f'(a) State the concentrations of the {n} solutions. (b) Describe how each dilution is made. (c) Explain why a serial dilution is used rather than diluting the stock solution directly each time.')
        vs = V / dil
        return Q(st, f'(a) {", ".join(fx(c, 4) for c in series)} {unit} (b) Transfer {fx(vs, 2)} cm³ of the previous solution and add {fx(V - vs, 2)} cm³ of distilled water; mix. (c) Small volumes / errors are not compounded across a wide range; it is quick and gives a logarithmic range of concentrations.',
                 f'(a) all concentrations correct [2] (b) {fx(vs, 2)} cm³ + {fx(V - vs, 2)} cm³ water [1]; use previous solution / mix [1] (c) easier to measure / wide range quickly [1] [5]', 'numerical', 5)
    st = f'{person(r)} has a {fx(stock)} {unit} {sol} solution and distilled water. Copy and complete a table to show the volumes needed to make {V} cm³ of each of these concentrations: ' + ', '.join(f'{fx(c, 3)} {unit}' for c in targets) + '.'
    ans = '; '.join(f'{fx(c, 3)} {unit}: {fx(c / stock * V, 2)} cm³ stock + {fx(V - c / stock * V, 2)} cm³ water' for c in targets)
    m = 3
    if D >= 3:
        st += ' State the units in each column heading.'
        m = 4
    return Q(st, ans + '.', f'V(stock) = C ÷ {fx(stock)} × {V}; one mark per correct row [3]' + (' ; headings with units, e.g. "volume of stock solution / cm³" [1] [4]' if m == 4 else ''), 'numerical', m)


@t.add('C3', (2, 3, 4, 5), 'case')
def benedict_semi(r, D):
    concs = [0.0, 0.1, 0.25, 0.5, 1.0, 2.0]
    cols = ['blue', 'green', 'yellow', 'orange', 'red-orange', 'brick red']
    i = r.randrange(1, 6)
    lo, hi = concs[i - 1], concs[i]
    fruit = r.choice(['grape juice', 'apple juice', 'a urine sample', 'onion extract', 'a sports drink', 'honey diluted 1 in 100'])
    intro = (f'{person(r)} carried out a semi-quantitative Benedict\'s test. Standard glucose solutions of ' + ', '.join(fx(c, 2) for c in concs) + ' % gave the colours ' + ', '.join(cols) +
             f' respectively. {cap(fruit)} gave a colour between {cols[i - 1]} and {cols[i]}.')
    parts = [lambda r: ('Estimate the concentration of reducing sugar in the sample.', f'Between {fx(lo, 2)}% and {fx(hi, 2)}%', f'between {fx(lo, 2)} and {fx(hi, 2)}% [1]'),
             lambda r: ('State three variables that must be kept the same for each tube.', 'Volume of sample / standard; volume of Benedict\'s solution; temperature of water bath; heating time.', 'any three [3]'),
             lambda r: ('Explain why the colour changes from blue towards brick red as the glucose concentration increases.', 'Reducing sugar reduces blue Cu²⁺ ions to Cu⁺, forming a red-brown precipitate of copper(I) oxide; more sugar gives more precipitate, so the mixture of blue solution and red precipitate shifts in colour.', 'Cu²⁺ reduced [1]; more precipitate with more sugar [1] [2]'),
             lambda r: ('Suggest how the method could be improved to give a more precise value.', 'Use a colorimeter to measure absorbance / transmission (after filtering the precipitate) and plot a calibration curve; or use more standards with smaller intervals.', '[2]'),
             lambda r: ('Explain why the colours give only a semi-quantitative estimate.', 'Judging colour is subjective and colours between standards cannot be measured; only a range can be given.', '[2]'),
             lambda r: ('State the safety precaution needed when heating the tubes.', 'Use a water bath (not a direct flame), wear eye protection, and point tubes away from people.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


@t.add('C3', (1, 2, 3), 'short')
def water_count(r, D):
    n = r.randint(6, 400)
    kind = r.choice([('glucose monomers to form an unbranched chain of amylose', n - 1, 'glycosidic'), ('amino acids to form a single polypeptide', n - 1, 'peptide'), ('nucleotides to form a single polynucleotide strand', n - 1, 'phosphodiester')])
    if D == 1:
        return NQ(r, f'How many molecules of water are released when {n} {kind[0]}?', kind[1], [n, n + 1, 2 * n, n - 2], '', f'{n} monomers form {n - 1} bonds by condensation, each releasing one water molecule.', f=lambda v: str(int(v)))
    return Q(f'{n} {kind[0]}. State (a) the type of reaction involved, (b) the type of bond formed, and (c) the number of water molecules released.',
             f'(a) Condensation (b) {kind[2]} bond (c) {kind[1]}', f'(a) condensation [1] (b) {kind[2]} [1] (c) {n} − 1 = {kind[1]} [1] [3]', 'short', 3)


mcqs(t, [('Which reaction breaks a glycosidic bond?', 'Hydrolysis', 'Bonds between monomers are broken by adding water.', ['Condensation', 'Oxidation', 'Phosphorylation']),
         ('Which molecule is not a polymer?', 'Triglyceride', 'Triglycerides are made of glycerol and three fatty acids, not repeating monomers; they are macromolecules but not polymers.', ['Cellulose', 'Glycogen', 'DNA'])])
shorts(t, [("Describe how to test a solution for non-reducing sugar.", "Do a Benedict's test first (negative); boil a fresh sample with dilute HCl to hydrolyse glycosidic bonds; neutralise with sodium hydrogencarbonate; heat with Benedict's: brick-red precipitate.", 'acid hydrolysis [1]; neutralise [1]; Benedict\'s positive [1] [3]'),
           ('State why the emulsion test for lipids uses ethanol and then water.', 'Lipids dissolve in ethanol but not in water; when added to water they come out of solution as tiny droplets that form a white emulsion.', '[2]')])
explain(t, [('Explain why a sample must be neutralised after acid hydrolysis in the test for non-reducing sugar.', "Benedict's test only works in alkaline conditions; the acid would react with the Benedict's reagent, so it is neutralised with an alkali such as sodium hydrogencarbonate.", "Benedict's needs alkaline conditions [1]; neutralise acid [1] [2]"),
            ('Explain why sucrose gives a negative result with Benedict\'s solution but a positive result after boiling with acid.', 'In sucrose the reducing groups of glucose and fructose are used in the glycosidic bond, so it is non-reducing; acid hydrolyses the bond, releasing reducing monosaccharides.', 'reducing groups involved in bond [1]; acid hydrolysis releases glucose / fructose [1] [2]'),
            ('Explain the difference between a condensation reaction and a hydrolysis reaction, using maltose as an example.', 'Condensation: two α-glucose join by a 1,4 glycosidic bond, releasing water, forming maltose. Hydrolysis: water is added to break the glycosidic bond, giving two α-glucose molecules.', 'condensation removes water [1]; hydrolysis adds water [1]; example [1] [3]'),
            ('Explain why Benedict\'s test is described as semi-quantitative.', 'The colour of the precipitate depends on the concentration of reducing sugar, so it can be compared with standards to estimate concentration, but cannot give an exact value.', '[2]')])
myths(t, [("A brick-red precipitate in Benedict's test shows that a sample contains starch.", "Brick-red precipitate shows reducing sugar; starch is detected with iodine (blue-black)."),
          ('Hydrolysis reactions release water.', 'Hydrolysis uses water to break bonds; condensation releases water.'),
          ('Sucrose is a reducing sugar because it contains glucose.', 'Sucrose is a non-reducing sugar: the reducing groups are used in the glycosidic bond.')])


@t.add('C4', (2, 3, 4, 5), 'case')
def unknown_case(r, D):
    food = r.choice(['a new breakfast cereal', 'a powdered infant formula', 'a vegetable smoothie', 'a protein bar', 'a fruit yoghurt'])
    intro = f'A food-science student in {city(r)} is asked to find out which biological molecules are present in {food}.'
    parts = [lambda r: ('Describe how the student would test for protein and state the positive result.', 'Add biuret reagent (or NaOH then dilute CuSO₄) to a solution of the food; blue → purple.', '[2]'),
             lambda r: ("The Benedict's test is negative. Describe how the student could show whether a non-reducing sugar is present.", "Boil with dilute HCl, cool, neutralise with sodium hydrogencarbonate, heat with Benedict's solution; brick-red precipitate = non-reducing sugar present.", '[3]'),
             lambda r: ('Describe how to test for lipid and explain why the food must not first be dissolved in water.', 'Shake with ethanol, decant into water: white emulsion. Lipid is insoluble in water so it would not dissolve and be extracted.', '[3]'),
             lambda r: ('Suggest a suitable negative control for these tests.', 'Repeat each test with distilled water instead of the food sample to show the reagents alone do not give a positive result.', '[2]'),
             lambda r: ('Suggest how the student could compare the concentration of reducing sugar in two brands.', "Use the same volume of each with the same volume of Benedict's, same temperature and time, then compare colour with standards or use a colorimeter / mass of precipitate.", '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


longs(t, [('Describe the tests you would use to identify reducing sugars, non-reducing sugars, starch, lipids and proteins, giving positive results.', "Reducing: Benedict's, heat, brick-red. Non-reducing: acid hydrolysis, neutralise, Benedict's. Starch: iodine, blue-black. Lipid: ethanol emulsion, white. Protein: biuret, purple.", 'one mark per test with result [5]; control or semi-quantitative point [1] [6]')])
t2a = t

t = T('Carbohydrates: α- and β-glucose, glycosidic bonds; starch, glycogen and cellulose', 'carbohydrates')
facts(t, [('monosaccharide', 'a single sugar unit such as glucose, fructose or ribose, with the general formula (CH₂O)n'), ('disaccharide', 'a sugar made of two monosaccharides joined by a glycosidic bond, e.g. maltose, sucrose, lactose'),
          ('glycosidic bond', 'a C–O–C bond formed by condensation between two monosaccharides'), ('amylose', 'the unbranched, helical component of starch made of α-glucose joined by 1,4 glycosidic bonds'),
          ('amylopectin', 'the branched component of starch made of α-glucose with 1,4 and 1,6 glycosidic bonds'), ('glycogen', 'the highly branched storage polysaccharide of animals and fungi, made of α-glucose'),
          ('cellulose', 'a polysaccharide of β-glucose joined by 1,4 glycosidic bonds forming straight chains linked by hydrogen bonds into microfibrils')])
POLY = {'amylose': ('α-glucose', '1,4 only', 'unbranched helix', 'compact energy store in plants; insoluble, no osmotic effect'),
        'amylopectin': ('α-glucose', '1,4 and 1,6 (branch about every 25 units)', 'branched', 'energy store in plants; branches allow faster hydrolysis'),
        'glycogen': ('α-glucose', '1,4 and 1,6 (branch about every 10 units)', 'highly branched, compact', 'energy store in animal liver and muscle; many ends for rapid hydrolysis to glucose'),
        'cellulose': ('β-glucose', '1,4 with alternate glucose rotated 180°', 'straight chains, hydrogen-bonded into microfibrils', 'strength of plant cell walls; high tensile strength')}


@t.add('C1', (1, 2, 3), 'mcq')
def poly_id(r, D):
    n = r.choice(list(POLY))
    mon, bond, shape, fn = POLY[n]
    st = r.choice([f'A polysaccharide is made of {mon} joined by {bond} glycosidic bonds and is {shape}. Which polysaccharide is it?',
                   f'Which polysaccharide has this function: {fn}?'])
    return MQ(r, st, cap(n), [cap(x) for x in POLY if x != n] + ['Sucrose'], f'{cap(n)}: {mon}, {bond}, {shape}; {fn}.')


@t.add('C1', (1, 2), 'mcq')
def disacch(r, D):
    dd = {'maltose': 'Two α-glucose molecules', 'sucrose': 'α-glucose and fructose', 'lactose': 'β-galactose and α-glucose'}
    n = r.choice(list(dd))
    return MQ(r, f'Which monosaccharides make up {n}?', dd[n], [v for k, v in dd.items() if k != n] + ['Two β-glucose molecules', 'Fructose and galactose'], f'{cap(n)}: {low(dd[n]) if dd[n][0] == "T" else dd[n]}.')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def poly_mr(r, D):
    n = r.choice([3, 4, 5, 6, 8, 10, 12, 20, 50, 100, 250, 500, 1000])
    mr = 180 * n - 18 * (n - 1)
    if D == 1:
        return NQ(r, f'The Mr of glucose is 180 and of water is 18. What is the Mr of a chain of {n} glucose units joined by glycosidic bonds?', mr, [180 * n, 180 * n - 18 * n, 162 * n + 36], '', f'{n} × 180 − {n - 1} × 18 = {mr:,}.', f=lambda v: f'{int(v):,}')
    st = f'An unbranched chain of {n} α-glucose molecules is made by condensation. The Mr of glucose is 180 and of water is 18. (a) State the number of glycosidic bonds. (b) Calculate the Mr of the chain.'
    ans = f'(a) {n - 1} (b) {mr:,}'
    key = f'(a) {n - 1} [1] (b) {n} × 180 = {180 * n:,}; − {n - 1} × 18 = {mr:,} [2]'
    m = 3
    if D >= 4:
        br = r.choice([2, 3, 4])
        st += f' (c) The chain is part of a glycogen molecule with {br} branch points. State the type of glycosidic bond at each branch point and explain how branching helps animals.'
        ans += ' (c) 1,6 glycosidic bonds; many ends allow enzymes to hydrolyse glycogen rapidly to release glucose for respiration.'
        key += ' (c) 1,6 [1]; many ends for rapid hydrolysis [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4), 'short')
def poly_compare(r, D):
    a, b = r.sample(list(POLY), 2)
    A, B = POLY[a], POLY[b]
    st = f'Compare the structures of {a} and {b}, and relate one difference to their functions.'
    ans = f'{cap(a)}: {A[0]}, {A[1]} bonds, {A[2]}; {A[3]}. {cap(b)}: {B[0]}, {B[1]} bonds, {B[2]}; {B[3]}.'
    return Q(st, ans, 'monomer comparison [1]; bond type / branching [1]; shape [1]; difference linked to function [1] [4]', 'short')


mcqs(t, [('What is the difference between α-glucose and β-glucose?', 'The position of the –H and –OH groups on carbon atom 1', 'In α-glucose the OH on C1 is below the ring; in β-glucose it is above.', ['The number of carbon atoms', 'The position of the –OH on carbon 6', 'β-glucose is a pentose']),
         ('Which feature of cellulose gives it high tensile strength?', 'Many hydrogen bonds between parallel straight chains forming microfibrils', 'Alternate β-glucose rotated 180° gives straight chains that hydrogen-bond.', ['1,6 glycosidic branch points', 'Coiled helical chains', 'Ester bonds between chains']),
         ('Which type of glycosidic bond is found at the branch points of amylopectin?', '1,6 glycosidic bonds', 'Branches are formed by 1,6 bonds.', ['1,4 glycosidic bonds', 'Ester bonds', 'Peptide bonds'])])
shorts(t, [('State two ways in which the structure of glycogen differs from that of amylose.', 'Glycogen is highly branched (1,6 bonds) whereas amylose is unbranched (1,4 only); glycogen chains are shorter / more compact; amylose forms a helix.', '[2]'),
           ('State the function of the hydrogen bonds between cellulose molecules.', 'They hold parallel chains together to form microfibrils, giving high tensile strength.', '[1]')])
explain(t, [('Explain how the structure of starch makes it suitable as a storage molecule.', 'Insoluble, so no osmotic effect and does not diffuse out of cells; compact (helical amylose); branched amylopectin gives many ends for rapid hydrolysis; made of α-glucose, easily hydrolysed to glucose for respiration.', 'insoluble / no osmotic effect [1]; compact [1]; branches for rapid hydrolysis [1]; glucose released [1] [4]'),
            ('Explain why glycogen is more suitable than starch as an energy store in animals.', 'Glycogen is more highly branched, so has more ends for enzymes to act on, allowing glucose to be released more rapidly for the higher metabolic rate of animals.', 'more branches [1]; more ends / faster hydrolysis [1]; animals more active / higher rate of respiration [1] [3]'),
            ('Explain how the structure of cellulose is related to its function in plant cell walls.', 'β-glucose with alternate units rotated 180° form straight chains; many hydrogen bonds link parallel chains into microfibrils, which are laid in layers giving high tensile strength so cells do not burst.', 'β-glucose / alternate rotation [1]; straight chains [1]; hydrogen bonds / microfibrils [1]; tensile strength [1] [4]'),
            ('Explain why glucose is not stored in cells as glucose.', 'Glucose is soluble and would lower the water potential, causing water to enter by osmosis; it could also diffuse out or take part in reactions; polysaccharides are insoluble.', 'soluble / osmotic effect [1]; would leave cell / react [1] [2]')])
myths(t, [('Cellulose is a storage molecule in plants.', 'Cellulose is structural; plants store glucose as starch.'), ('Glycogen is made of β-glucose.', 'Glycogen, like starch, is made of α-glucose; cellulose is made of β-glucose.'),
          ('Amylose is branched because it has 1,6 glycosidic bonds.', 'Amylose is unbranched (1,4 only); amylopectin and glycogen have 1,6 branch points.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def carb_case(r, D):
    tissue, poly = r.choice([('potato tuber cells', 'starch'), ('human liver cells', 'glycogen'), ('skeletal muscle of an athlete', 'glycogen'), ('cotton fibres', 'cellulose'), ('wheat endosperm', 'starch'), ('the cell walls of celery', 'cellulose')])
    intro = f'A researcher in {city(r)} extracts the main polysaccharide from {tissue} and finds that it is {poly}.'
    parts = [lambda r: ('Describe how two α-glucose molecules join together by a condensation reaction.', 'Condensation between the OH on C1 of one glucose and the OH on C4 of the other; water removed; 1,4 glycosidic bond formed.', 'C1 and C4 [1]; water removed [1]; 1,4 glycosidic bond [1] [3]'),
             lambda r: (f'Describe how {poly} could be hydrolysed to release glucose.', 'Glycosidic bonds broken by adding water, catalysed by enzymes (amylase / glycogen phosphorylase, or cellulase for cellulose) or by boiling with acid.', 'water added to glycosidic bonds [1]; enzyme / acid named [1] [2]')]
    if poly == 'cellulose':
        parts += [lambda r: ('Explain how the structure of cellulose gives plant cell walls their strength.', 'β-glucose with alternate units inverted forms straight chains; many hydrogen bonds link parallel chains into microfibrils; microfibrils in layers give high tensile strength.', 'β-glucose / straight chains [1]; hydrogen bonds between chains [1]; microfibrils / tensile strength [1] [3]'),
                  lambda r: ('Explain why humans cannot digest cellulose.', 'Humans do not produce cellulase; the β 1,4 glycosidic bonds do not fit the active site of amylase.', 'no cellulase [1]; amylase specific to α bonds [1] [2]')]
    else:
        parts += [lambda r: (f'Explain why {poly} is suitable as an energy store.', 'Insoluble, so no effect on water potential; compact; branched molecules have many ends for rapid hydrolysis; made of α-glucose, which is easily released for respiration.', 'insoluble / no osmotic effect [1]; compact [1]; easily hydrolysed to glucose [1] [3]'),
                  lambda r: (f'Describe how to test the extract for {poly} and state the expected result.', 'Add iodine in potassium iodide solution: orange-brown to blue-black.' if poly == 'starch' else 'Add iodine in potassium iodide solution: it turns red-brown (glycogen gives a weaker red-brown colour, not blue-black).', 'iodine solution [1]; correct colour [1] [2]')]
    parts.append(lambda r: ('Compare the structure of glycogen with that of cellulose.', 'Glycogen: α-glucose, 1,4 and 1,6 bonds, highly branched, compact. Cellulose: β-glucose, 1,4 bonds only, straight chains, hydrogen bonds between chains forming microfibrils.', 'two differences [2]; one similarity (glucose / glycosidic bonds / polysaccharide) [1] [3]'))
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the molecular structure of starch, glycogen and cellulose and explain how each structure is related to its function.', 'Starch: amylose helix (α 1,4) + amylopectin (α 1,4, 1,6), compact insoluble store. Glycogen: α-glucose, highly branched (1,6 every ~10), rapid hydrolysis. Cellulose: β-glucose 1,4, alternate units inverted, straight chains, H-bonds, microfibrils, tensile strength.',
           'starch structure [2]; glycogen [1]; cellulose [2]; function links [2] [7]')])
t2b = t

FA = [('palmitic acid', 256, 'saturated'), ('stearic acid', 284, 'saturated'), ('oleic acid', 282, 'monounsaturated'), ('linoleic acid', 280, 'polyunsaturated'), ('lauric acid', 200, 'saturated'), ('myristic acid', 228, 'saturated')]
t = T('Lipids: triglycerides, ester bonds and phospholipids', 'lipids')
facts(t, [('triglyceride', 'a lipid made of one glycerol molecule joined to three fatty acids by ester bonds'), ('ester bond', 'the bond formed by condensation between a carboxyl group of a fatty acid and a hydroxyl group of glycerol'),
          ('saturated fatty acid', 'a fatty acid with no carbon–carbon double bonds in its hydrocarbon chain'), ('unsaturated fatty acid', 'a fatty acid with one or more C=C double bonds, which put kinks in the chain'),
          ('phospholipid', 'a lipid in which one fatty acid of a triglyceride is replaced by a phosphate-containing group, giving a hydrophilic head and two hydrophobic tails'),
          ('hydrophobic', 'repelled by water; non-polar, so does not mix with or dissolve in water')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def trig_mr(r, D):
    fas = [r.choice(FA) for _ in range(3)]
    mr = 92 + sum(f[1] for f in fas) - 3 * 18
    names = ', '.join(f'{f[0]} (Mr {f[1]})' for f in fas)
    if D == 1:
        f = fas[0]
        mr1 = 92 + 3 * f[1] - 54
        return NQ(r, f'Glycerol has Mr 92 and {f[0]} has Mr {f[1]}. What is the Mr of a triglyceride containing three {f[0]} molecules? (Mr of water = 18)', mr1, [92 + 3 * f[1], 92 + 3 * f[1] - 18, 92 + f[1] - 18], '', f'92 + 3 × {f[1]} − 3 × 18 = {mr1}.', f=lambda v: str(int(v)))
    st = f'A triglyceride is formed from glycerol (Mr 92) and three fatty acids: {names}. (a) State the number of ester bonds and of water molecules released. (b) Calculate the Mr of the triglyceride (Mr of water = 18).'
    ans = f'(a) 3 ester bonds; 3 water molecules (b) {mr}'
    key = f'(a) 3 and 3 [1] (b) 92 + {" + ".join(str(f[1]) for f in fas)} = {92 + sum(f[1] for f in fas)} [1]; − 54 = {mr} [1]'
    m = 3
    if D >= 3:
        u = any(f[2] != 'saturated' for f in fas)
        st += ' (c) Predict whether this triglyceride is more likely to be a fat or an oil at room temperature, and explain why.'
        ans += (' (c) An oil (liquid): unsaturated fatty acids have kinks, so molecules cannot pack closely, lowering the melting point.' if u else ' (c) A fat (solid): saturated chains are straight and pack closely, so the melting point is high.')
        key += ' (c) correct prediction [1]; kinks / packing explanation [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (1, 2, 3, 4), 'numerical')
def energy_store(r, D):
    lip, carb = r.choice([(37, 16), (38, 17), (39, 17), (39, 16)])
    E = r.choice([800, 1200, 2000, 5000, 9000])
    org = r.choice(['a migrating bird', 'a hibernating bear', 'a desert camel', 'a seed of a sunflower', 'a migrating salmon'])
    ml, mc = E / lip, E / carb
    if D == 1:
        return NQ(r, f'Lipid releases {lip} kJ g⁻¹ and carbohydrate {carb} kJ g⁻¹ when respired. What mass of lipid stores {E} kJ?', ml, [mc, E * lip / 1000, ml * 2], ' g', f'{E} ÷ {lip} = {fx(ml, 1)} g.', f=lambda v: fx(v, 1))
    st = f'Respiration of lipid releases about {lip} kJ g⁻¹ and of carbohydrate about {carb} kJ g⁻¹. {cap(org)} needs to store {E} kJ of energy. (a) Calculate the mass of lipid and of carbohydrate needed. (b) Calculate the mass saved by storing lipid.'
    ans = f'(a) lipid {fx(ml, 1)} g; carbohydrate {fx(mc, 1)} g (b) {fx(mc - ml, 1)} g'
    key = f'(a) {E} ÷ {lip} = {fx(ml, 1)} g [1]; {E} ÷ {carb} = {fx(mc, 1)} g [1] (b) {fx(mc - ml, 1)} g [1]'
    m = 3
    if D >= 3:
        st += f' (c) Explain why lipid is a better energy store for {org}.'
        ans += ' (c) Lipid releases more than twice as much energy per gram, so less mass is carried; it is insoluble and also releases metabolic water / provides insulation.'
        key += ' (c) more energy per gram / less mass [1]; extra benefit (metabolic water / insulation / buoyancy) [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


mcqs(t, [('Which groups react to form an ester bond in a triglyceride?', 'A hydroxyl group of glycerol and a carboxyl group of a fatty acid', 'Condensation between –OH of glycerol and –COOH of fatty acid.', ['An amine group and a carboxyl group', 'Two hydroxyl groups of glucose', 'A phosphate group and a hydroxyl group of a sugar']),
         ('Which property of phospholipids allows them to form a bilayer in water?', 'They have a hydrophilic head and hydrophobic tails', 'Heads face water; tails face inwards away from water.', ['They are soluble in water', 'They contain ester bonds', 'They have three fatty acid tails']),
         ('Why do triglycerides release more energy per gram than carbohydrates?', 'They contain a higher proportion of hydrogen atoms (C–H bonds)', 'More C–H bonds and less oxygen per unit mass.', ['They contain glycerol', 'They are hydrophobic', 'They contain ester bonds'])])
shorts(t, [('State three functions of triglycerides in organisms.', 'Energy store; thermal insulation; buoyancy; protection of organs; source of metabolic water.', 'any three [3]'),
           ('Describe how a phospholipid differs from a triglyceride.', 'One fatty acid is replaced by a phosphate group (hydrophilic head), so it has two fatty acid tails.', '[2]')])
explain(t, [('Explain why triglycerides are insoluble in water.', 'Their fatty acid hydrocarbon tails are non-polar and cannot form hydrogen bonds with water; the ester bonds hide the polar groups.', 'non-polar / hydrophobic tails [1]; no hydrogen bonds with water [1] [2]'),
            ('Explain how phospholipids form a bilayer in cell membranes.', 'The hydrophilic phosphate heads face the aqueous cytoplasm and tissue fluid, while the hydrophobic fatty acid tails face inwards away from water, forming two layers.', 'heads face water [1]; tails inwards [1] [2]'),
            ('Explain why camels store fat in their humps rather than water.', 'Respiration of fat releases a large amount of metabolic water as well as energy, and fat is a compact, high-energy store.', 'metabolic water [1]; energy dense [1] [2]'),
            ('Explain why unsaturated fatty acids make membranes more fluid.', 'Double bonds cause kinks in the tails so phospholipids cannot pack closely together.', '[2]')])
myths(t, [('Triglycerides are polymers of fatty acids.', 'Triglycerides contain glycerol plus three fatty acids; they are not made of repeating monomers.'), ('Saturated fats have double bonds that make them solid.', 'Saturated fatty acids have no C=C double bonds; straight chains pack closely, so fats are solid.'),
          ('Phospholipids are completely hydrophobic.', 'Phospholipids have a hydrophilic phosphate head and hydrophobic tails.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def lipid_case(r, D):
    a = r.choice(['an emperor penguin', 'a grey seal', 'an Arctic fox', 'a humpback whale'])
    th = r.choice([3, 4, 5, 6, 8, 10])
    intro = f'{cap(a)} living in a cold environment has a layer of blubber about {th} cm thick, made mainly of triglycerides.'
    parts = [lambda r: ('Describe the structure of a triglyceride molecule.', 'One glycerol joined to three fatty acids by ester bonds formed in condensation reactions.', '[2]'),
             lambda r: ('Explain two ways in which the blubber helps the animal survive.', 'Thermal insulation reduces heat loss; energy store for times when food is scarce; buoyancy.', 'two functions explained [2]'),
             lambda r: ('Explain why triglycerides are a more efficient energy store than glycogen.', 'They release about twice as much energy per gram (more C–H bonds), are insoluble and stored without water.', '[2]'),
             lambda r: ('Suggest why the triglycerides in the animal\'s feet contain more unsaturated fatty acids.', 'Unsaturated fats have lower melting points so they stay liquid / flexible at low temperatures.', '[2]'),
             lambda r: ('Describe how to test a sample of blubber for lipid.', 'Grind with ethanol, decant into water: white emulsion forms.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of a triglyceride and of a phospholipid and explain how their structures are related to their roles in organisms.', 'Triglyceride: glycerol + 3 fatty acids by ester bonds (condensation), hydrophobic, energy store, insulation, metabolic water. Phospholipid: glycerol + 2 fatty acids + phosphate head, amphipathic, forms bilayers in membranes.',
           'triglyceride structure [2]; functions [2]; phospholipid structure [1]; bilayer explanation [1] [6]')])
t2c = t

AA = {'glycine': 75, 'alanine': 89, 'serine': 105, 'cysteine': 121, 'valine': 117, 'leucine': 131, 'lysine': 146, 'glutamic acid': 147, 'phenylalanine': 165}
t = T('Proteins: amino acids, peptide bonds and primary to quaternary structure; haemoglobin and collagen', 'proteins')
facts(t, [('primary structure', 'the sequence of amino acids in a polypeptide chain'), ('secondary structure', 'the regular coiling (α-helix) or folding (β-pleated sheet) of a polypeptide held by hydrogen bonds between –C=O and –NH groups'),
          ('tertiary structure', 'the overall 3-D folding of a polypeptide held by hydrogen, ionic and disulfide bonds and hydrophobic interactions between R groups'),
          ('quaternary structure', 'the association of two or more polypeptide chains (and sometimes prosthetic groups) in a protein'),
          ('peptide bond', 'the C–N bond formed by condensation between the carboxyl group of one amino acid and the amine group of another'),
          ('globular protein', 'a protein with a compact, roughly spherical shape, usually soluble, with a metabolic role (e.g. haemoglobin, enzymes)'),
          ('fibrous protein', 'a protein of long strands, usually insoluble, with a structural role (e.g. collagen, keratin)'),
          ('disulfide bond', 'a strong covalent S–S bond between the R groups of two cysteine molecules')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def peptide_count(r, D):
    prot = r.choice([('insulin', [21, 30]), ('haemoglobin', [141, 141, 146, 146]), ('a dimeric enzyme', [r.randint(150, 400)] * 2), ('a single-chain hormone', [r.randint(20, 120)]),
                     ('a collagen molecule', [r.randint(1000, 1060)] * 3), ('a trimeric receptor', [r.randint(80, 250)] * 3)])
    name, chains = prot
    n = sum(chains)
    c = len(chains)
    pb = n - c
    if D == 1:
        return NQ(r, f'{cap(name)} contains {c} polypeptide chain{"s" if c > 1 else ""} with a total of {n} amino acids. How many peptide bonds does it contain?', pb, [n, n - 1, n + c, n - 2 * c], '', f'Each chain of k amino acids has k − 1 peptide bonds: {n} − {c} = {pb}.', f=lambda v: f'{int(v):,}')
    mr = n * 128 - 18 * pb
    st = f'{cap(name)} is made of {c} polypeptide chain{"s" if c > 1 else ""} containing ' + (' and '.join(str(x) for x in chains) if c <= 4 else str(n)) + ' amino acids. (a) Calculate the number of peptide bonds. (b) Taking the mean Mr of an amino acid as 128 and of water as 18, estimate the Mr of the protein (ignore any prosthetic groups).'
    ans = f'(a) {pb:,} (b) {mr:,}'
    key = f'(a) {n} − {c} = {pb:,} [1] (b) {n} × 128 = {n * 128:,} [1]; − {pb:,} × 18 = {mr:,} [1]'
    m = 3
    if D >= 3:
        st += ' (c) State the level of protein structure shown by a protein with more than one polypeptide chain, and name the bonds that may hold the chains together.'
        ans += ' (c) Quaternary structure; hydrogen bonds, ionic bonds, disulfide bonds and hydrophobic interactions.'
        key += ' (c) quaternary [1]; two bond types [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (1, 2, 3), 'short')
def dipeptide(r, D):
    a, b = r.sample(list(AA), 2)
    mr = AA[a] + AA[b] - 18
    if D == 1:
        return NQ(r, f'{cap(a)} (Mr {AA[a]}) and {b} (Mr {AA[b]}) join to form a dipeptide. What is the Mr of the dipeptide?', mr, [AA[a] + AA[b], mr - 18, AA[a] + AA[b] + 18], '', f'{AA[a]} + {AA[b]} − 18 = {mr}.', f=lambda v: str(int(v)))
    return Q(f'{cap(a)} (Mr {AA[a]}) and {b} (Mr {AA[b]}) join by a condensation reaction. (a) Name the bond formed and the groups that react. (b) Calculate the Mr of the dipeptide (Mr water = 18).',
             f'(a) Peptide bond; carboxyl (–COOH) group of one amino acid and amine (–NH₂) group of the other (b) {mr}', f'(a) peptide [1]; –COOH and –NH₂ [1] (b) {AA[a]} + {AA[b]} − 18 = {mr} [1] [3]', 'short', 3)


BONDS = [('hydrogen bonds', 'between polar R groups (and between –NH and –C=O in secondary structure); weak, broken by heat'), ('ionic bonds', 'between oppositely charged R groups (–NH₃⁺ and –COO⁻); broken by changes in pH'),
         ('disulfide bonds', 'covalent bonds between sulfur atoms of two cysteine R groups; strong'), ('hydrophobic interactions', 'between non-polar R groups, which cluster in the centre of globular proteins away from water')]


@t.add('C1', (1, 2, 3), 'mcq')
def bond_id(r, D):
    b, d = r.choice(BONDS)
    return MQ(r, f'Which type of bond or interaction in a protein forms {d.split(";")[0]}?', cap(b), [cap(x[0]) for x in BONDS if x[0] != b] + ['Peptide bonds'], f'{cap(b)}: {d}.')


mcqs(t, [('Which feature of haemoglobin is an example of quaternary structure?', 'It has two α and two β polypeptide chains', 'Quaternary = more than one polypeptide chain.', ['It contains peptide bonds', 'Each chain is folded into α-helices', 'It has a specific sequence of amino acids']),
         ('Why is glycine found at every third position in collagen?', 'Its small R group (H) allows the three chains to pack tightly in a triple helix', 'Glycine is the smallest amino acid.', ['It forms disulfide bonds', 'It is charged', 'It is hydrophobic']),
         ('Which ion is found in each haem group of haemoglobin?', 'Fe²⁺', 'Each haem contains Fe²⁺, which binds one O₂.', ['Mg²⁺', 'Ca²⁺', 'Cu²⁺'])])
shorts(t, [('Draw or describe the general structure of an amino acid.', 'A central carbon atom bonded to an amine group (–NH₂), a carboxyl group (–COOH), a hydrogen atom and an R group.', 'four groups correct [2]'),
           ('State two differences between globular and fibrous proteins.', 'Globular: compact / spherical, soluble, metabolic roles (e.g. enzymes, haemoglobin). Fibrous: long strands, insoluble, structural roles (e.g. collagen).', '[2]')])
explain(t, [('Explain how the structure of haemoglobin is related to its function.', 'Globular and soluble so it is carried in red blood cells; four polypeptides each with a haem group containing Fe²⁺ that binds O₂, so each molecule carries 4 O₂; hydrophobic R groups inside, hydrophilic outside; quaternary structure allows cooperative binding.', 'soluble / globular [1]; four haem groups / Fe²⁺ bind O₂ [1]; hydrophilic outside [1]; cooperative binding / shape change [1] [4]'),
            ('Explain how the structure of collagen is related to its function.', 'Three polypeptide chains wound into a triple helix with glycine every third residue allowing tight packing; hydrogen bonds between chains; molecules cross-linked covalently into staggered fibrils and fibres, giving high tensile strength in tendons, skin and bone.', 'triple helix [1]; glycine / tight packing [1]; cross-links / fibrils [1]; tensile strength [1] [4]'),
            ('Explain why a change in one amino acid can change the function of a protein.', 'The primary structure determines how the chain folds; a different R group may form different bonds, changing the tertiary structure and so the shape of the active site or binding site.', 'primary determines folding [1]; different R group bonds [1]; shape / function changes [1] [3]'),
            ('Explain why high temperature denatures proteins but does not break peptide bonds.', 'Heat increases kinetic energy, breaking weak hydrogen and ionic bonds that hold the tertiary structure; strong covalent peptide bonds remain, so the primary structure is unchanged.', 'hydrogen / ionic bonds broken [1]; tertiary shape lost [1]; peptide bonds covalent and stable [1] [3]')])
myths(t, [('Peptide bonds are broken when a protein is denatured.', 'Denaturation breaks hydrogen, ionic and sometimes disulfide bonds; peptide bonds remain intact.'), ('Collagen is a globular protein because it has quaternary structure.', 'Collagen is fibrous; quaternary structure (three chains) is found in both types.'),
          ('The secondary structure of a protein is held by bonds between R groups.', 'Secondary structure is held by hydrogen bonds between –C=O and –NH groups of the backbone.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def protein_case(r, D):
    p = r.choice([('haemoglobin', 'globular', 'transports oxygen in red blood cells'), ('collagen', 'fibrous', 'gives strength to tendons and skin'), ('lysozyme', 'globular', 'an enzyme in tears that digests bacterial cell walls'), ('keratin', 'fibrous', 'forms hair and nails')])
    intro = f'{cap(p[0])} is a {p[1]} protein that {p[2]}. A student in {city(r)} researches how its structure relates to its function.'
    parts = [lambda r: ('Describe what is meant by the primary, secondary and tertiary structure of a protein.', 'Primary: amino acid sequence; secondary: α-helix / β-pleated sheet held by H-bonds between backbone groups; tertiary: 3-D folding held by bonds between R groups.', '[3]'),
             lambda r: (f'Explain why {p[0]} is described as {p[1]}.', 'Globular: compact, spherical, soluble, hydrophilic R groups outside. ' if p[1] == 'globular' else 'Fibrous: long parallel chains, insoluble, repetitive sequence, structural role.', '[2]'),
             lambda r: ('Name the four types of bond or interaction that stabilise tertiary structure.', 'Hydrogen bonds, ionic bonds, disulfide bonds, hydrophobic interactions.', 'four [2]; two or three [1] [2]'),
             lambda r: (f'Suggest the effect on the function of {p[0]} of heating it to 80 °C.', 'Hydrogen and ionic bonds break, so the 3-D shape is lost (denatured); it can no longer carry out its function.', '[2]'),
             lambda r: ('Describe how a peptide bond is formed.', 'Condensation between –COOH of one amino acid and –NH₂ of the next, removing water and forming –CO–NH–.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Compare the structures of haemoglobin and collagen and explain how each is related to its function.', 'Haemoglobin: globular, 4 polypeptides (2α 2β), haem with Fe²⁺, soluble, hydrophilic outside, binds 4 O₂. Collagen: fibrous, 3 polypeptides in triple helix, glycine every third, H-bonds, cross-links into fibrils and fibres, insoluble, tensile strength.',
           'haemoglobin structure [2]; function link [1]; collagen structure [2]; function link [1]; comparison point [1] [7]')])
t2d = t

t = T('Water: hydrogen bonding and properties important to organisms', 'water')
facts(t, [('hydrogen bond', 'a weak attraction between a slightly positive hydrogen atom of one molecule and a slightly negative atom (such as oxygen) of another'), ('dipole', 'a molecule with an uneven distribution of charge, slightly positive at one end and slightly negative at the other'),
          ('specific heat capacity', 'the energy needed to raise the temperature of 1 kg of a substance by 1 °C (4.2 kJ kg⁻¹ °C⁻¹ for water)'), ('latent heat of vaporisation', 'the energy needed to change a liquid into a gas without a change in temperature (about 2.4 kJ g⁻¹ for water)'),
          ('cohesion', 'the attraction between water molecules due to hydrogen bonding'), ('solvent', 'a liquid in which solutes dissolve; water dissolves polar and ionic substances')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def water_heat(r, D):
    m = r.choice([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
    dT = r.choice([2, 3, 5, 8, 10, 15])
    E = m * 4.2 * dT
    if D == 1:
        return NQ(r, f'Water has a specific heat capacity of 4.2 kJ kg⁻¹ °C⁻¹. How much energy raises the temperature of {fx(m, 2)} kg of water by {dT} °C?', E, [E * 10, E / dT, 4.2 * dT], ' kJ', f'{fx(m, 2)} × 4.2 × {dT} = {fx(E, 2)} kJ.', f=lambda v: fx(v, 2))
    lh = 2.4
    org, masses, sws = r.choice([('a marathon runner', [55, 60, 65, 70], [0.8, 1.0, 1.5, 2.0]), ('a racehorse during a race', [450, 500, 550], [4.0, 5.0, 6.0, 8.0]),
                                 ('a footballer in a hot stadium', [65, 70, 75, 80], [0.5, 0.8, 1.0, 1.5]), ('a farm worker in the midday sun', [55, 60, 70, 80], [0.4, 0.6, 1.0, 1.2])])
    sw = r.choice(sws)
    st = f'The latent heat of vaporisation of water is {lh} kJ g⁻¹. {cap(org)} in {city(r)} loses {fx(sw, 1)} dm³ (= {int(sw * 1000)} g) of sweat, all of which evaporates. (a) Calculate the energy removed from the body.'
    Ev = sw * 1000 * lh
    ans = f'(a) {fx(Ev, 0):} kJ'
    key = f'(a) {int(sw * 1000)} × {lh} = {fx(Ev, 0)} kJ [2]'
    mk_ = 2
    if D >= 3:
        mass = r.choice(masses)
        c = 3.5
        dT2 = Ev / (mass * c)
        st += f' (b) The body has a mass of {mass} kg and a mean specific heat capacity of {c} kJ kg⁻¹ °C⁻¹. Calculate the rise in body temperature that would have occurred if this energy had not been removed.'
        ans += f' (b) {fx(dT2, 1)} °C'
        key += f' (b) {fx(Ev, 0)} ÷ ({mass} × {c}) = {fx(dT2, 1)} °C [2]'
        mk_ += 2
    if D >= 4:
        st += ' (c) Explain, in terms of hydrogen bonding, why evaporation of water has a large cooling effect.'
        ans += ' (c) Many hydrogen bonds must be broken for molecules to escape, so a lot of energy (heat) is taken from the body surface.'
        key += ' (c) hydrogen bonds broken [1]; large energy absorbed from skin [1]'
        mk_ += 2
    return Q(st, ans, key + f' [{mk_}]', 'numerical', mk_)


PROPS = [('high specific heat capacity', 'water temperature changes slowly, so aquatic habitats and the internal temperature of organisms stay stable', 'many hydrogen bonds must be broken to increase molecular motion'),
         ('high latent heat of vaporisation', 'evaporation of sweat or transpiration has a strong cooling effect', 'hydrogen bonds must be broken for molecules to escape as vapour'),
         ('good solvent', 'polar and ionic substances dissolve, so it is a medium for reactions and transport in blood, xylem and phloem', 'water molecules are dipoles that cluster around ions and polar molecules'),
         ('cohesion', 'columns of water can be pulled up xylem vessels in the transpiration stream', 'hydrogen bonds attract water molecules to one another'),
         ('high surface tension', 'small organisms such as pond skaters can walk on the surface', 'cohesion between molecules at the surface'),
         ('ice is less dense than liquid water', 'ice floats and insulates the water below, so aquatic organisms survive in winter', 'hydrogen bonds hold molecules in an open lattice in ice')]


@t.add('C1', (1, 2, 3), 'mcq')
def water_prop(r, D):
    p, use, why = r.choice(PROPS)
    return MQ(r, f'Which property of water explains this: {use}?', cap(p), [cap(x[0]) for x in PROPS if x[0] != p], f'{cap(p)}: {why}.')


@t.add('C3', (2, 3, 4), 'short')
def water_apply(r, D):
    a, b = r.sample(PROPS, 2)
    if D <= 2:
        return Q(f'Explain how the {a[0]} of water is important to living organisms.', f'{cap(a[1])}; {a[2]}.', 'importance [1]; explained by hydrogen bonding / dipoles [1] [2]', 'short')
    return Q(f'Explain how (i) the {a[0]} and (ii) the {b[0]} of water are important to living organisms, referring to hydrogen bonding.', f'(i) {cap(a[1])}; {a[2]}. (ii) {cap(b[1])}; {b[2]}.', '(i) importance [1]; explanation [1] (ii) importance [1]; explanation [1] [4]', 'short')


mcqs(t, [('Why is a water molecule polar?', 'Oxygen attracts the shared electrons more strongly than hydrogen', 'Oxygen is more electronegative, so O is δ⁻ and H is δ⁺.', ['It has two hydrogen atoms', 'It forms ionic bonds', 'It is a small molecule']),
         ('Which property of water allows it to act as a transport medium in blood?', 'It is a good solvent for polar and ionic substances', 'Glucose, ions and urea dissolve in plasma water.', ['It has a high latent heat of vaporisation', 'Ice floats on water', 'It has high surface tension'])])
shorts(t, [('Describe the hydrogen bonding between water molecules.', 'The δ⁺ hydrogen of one molecule is attracted to the δ⁻ oxygen of another; each molecule can form up to four hydrogen bonds.', '[2]'),
           ('State two roles of water as a reactant in organisms.', 'Hydrolysis reactions (digestion); photosynthesis (source of electrons / hydrogen).', '[2]')])
explain(t, [('Explain why water has a high specific heat capacity and why this is important to organisms.', 'Hydrogen bonds restrict movement of molecules, so much energy is needed to raise temperature; body and habitat temperatures remain stable, so enzymes work efficiently.', 'H-bonds absorb energy [1]; stable temperature [1]; enzymes / habitats [1] [3]'),
            ('Explain why ice floats and why this is important for aquatic organisms.', 'In ice, hydrogen bonds hold molecules further apart in a lattice, so ice is less dense than water; ice forms on the surface and insulates the water below, so it does not freeze and organisms survive.', 'lattice / less dense [1]; insulates water below [1] [2]'),
            ('Explain how water acts as a solvent for sodium chloride.', 'Water molecules are dipoles; δ⁻ oxygens surround Na⁺ and δ⁺ hydrogens surround Cl⁻, separating the ions.', '[2]')])
myths(t, [('Hydrogen bonds are strong covalent bonds within water molecules.', 'Hydrogen bonds are weak attractions between water molecules; the bonds within a molecule are covalent.'), ('Ice sinks because it is solid.', 'Ice is less dense than liquid water and floats, because hydrogen bonds hold molecules in an open lattice.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def water_case(r, D):
    lake = r.choice(['Lake Baikal', 'a pond in Toronto', 'a lake in the Andes', 'a reservoir in Seoul'])
    a, w = r.choice([(-8, 4), (-15, 4), (-20, 4), (-5, 4)])
    intro = f'In winter, the air above {lake} falls to {a} °C. The surface freezes, but the water at the bottom stays at about {w} °C, and fish survive.'
    parts = [lambda r: ('Explain why ice forms at the surface rather than at the bottom.', 'Water is densest at 4 °C so it sinks; ice is less dense (open lattice held by hydrogen bonds) and floats.', '[2]'),
             lambda r: ('Explain how the ice layer helps the fish survive.', 'Ice insulates the water below, reducing heat loss, so water stays liquid; fish can still move and obtain oxygen.', '[2]'),
             lambda r: ('Explain why the temperature of the lake water changes only slowly through the year.', 'High specific heat capacity: much energy is needed to break hydrogen bonds and change the temperature.', '[2]'),
             lambda r: ('Explain why oxygen and carbon dioxide can still be used by organisms in the water.', 'Water is a solvent; the gases dissolve and diffuse to gills / leaves.', '[1]'),
             lambda r: ('Describe how hydrogen bonds form between water molecules.', 'Water is polar (δ⁻ O, δ⁺ H); δ⁺ H of one molecule attracts δ⁻ O of another.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how hydrogen bonding gives water the properties that make it important to living organisms.', 'Polar molecule / dipole; hydrogen bonds. Solvent (transport, reactions); high SHC (stable temperatures); high latent heat (cooling by sweating / transpiration); cohesion and surface tension (xylem, pond skaters); ice less dense (insulation).',
           'polarity and H-bonds [2]; four properties each linked to importance [4] [6]')])
t2e = t
CHAPTERS[2] = [t2a, t2b, t2c, t2d, t2e]


# ===================================================================== 3 Enzymes
t = T('Mode of action of enzymes: lock-and-key and induced-fit hypotheses; lowering activation energy', 'mode of action of enzymes')
facts(t, [('enzyme', 'a protein molecule that is a biological catalyst, speeding up a metabolic reaction without being permanently changed'),
          ('active site', 'the region of an enzyme with a specific 3-D shape to which the substrate binds'), ('activation energy', 'the energy that must be supplied to make a reaction start'),
          ('enzyme–substrate complex', 'the temporary structure formed when a substrate binds to the active site of an enzyme'),
          ('induced fit', 'the hypothesis that the active site changes shape slightly as the substrate binds, so that it fits more closely around the substrate'),
          ('lock-and-key hypothesis', 'the hypothesis that the substrate fits exactly into a rigid active site with a complementary shape'),
          ('extracellular enzyme', 'an enzyme that is secreted and works outside the cell that made it, such as amylase in saliva'), ('intracellular enzyme', 'an enzyme that works inside the cell that made it, such as catalase')])
mcqs(t, [('How does an enzyme increase the rate of a reaction?', 'It lowers the activation energy', 'Binding in the active site strains bonds / brings molecules together, lowering activation energy.', ['It increases the kinetic energy of substrate molecules', 'It raises the temperature', 'It provides energy to the substrate']),
         ('Why is each enzyme specific to one substrate?', 'Its active site has a shape complementary to only one substrate', 'The active site shape is determined by the tertiary structure.', ['It is made of amino acids', 'It is a globular protein', 'It is not used up in the reaction']),
         ('Which is an example of an extracellular enzyme?', 'Amylase in saliva', 'Secreted and works outside the cell.', ['Catalase in liver cells', 'ATP synthase in mitochondria', 'DNA polymerase in the nucleus'])])
shorts(t, [('Name two intracellular enzymes and two extracellular enzymes.', 'Intracellular: catalase, DNA polymerase, ATP synthase. Extracellular: amylase, trypsin, lipase, pepsin.', 'two of each [2]'),
           ('State what is meant by the specificity of an enzyme.', 'An enzyme catalyses only one reaction / acts on one substrate, because the active site is complementary to that substrate only.', '[1]')])
explain(t, [('Compare the lock-and-key and induced-fit hypotheses of enzyme action.', 'Both: substrate binds to a specific active site forming an enzyme–substrate complex. Lock-and-key: active site rigid, exactly complementary. Induced fit: active site changes shape slightly as substrate binds, moulding round it and putting strain on bonds.', 'similarity [1]; lock-and-key rigid [1]; induced fit shape change [1] [3]'),
            ('Explain how the formation of an enzyme–substrate complex lowers the activation energy.', 'Binding holds substrates close together in the correct orientation, or the change in shape strains bonds in the substrate, so they break more easily.', '[2]'),
            ('Explain why an enzyme can be used again and again.', 'It is not changed by the reaction; after products leave the active site, it is free to bind another substrate.', '[2]'),
            ('Explain why the tertiary structure of an enzyme is essential to its function.', 'The tertiary structure (held by bonds between R groups) determines the 3-D shape of the active site, which must be complementary to the substrate.', '[2]')])
myths(t, [('Enzymes provide energy for reactions.', 'Enzymes lower the activation energy; they do not supply energy.'), ('The active site and substrate have the same shape.', 'The active site has a shape complementary to the substrate.'),
          ('Enzymes are killed at high temperatures.', 'Enzymes are proteins, not living things; they are denatured.')])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def act_energy(r, D):
    u = r.choice([75, 86, 120, 150, 200])
    c = round(u * r.uniform(0.2, 0.55))
    rx = r.choice(['the breakdown of hydrogen peroxide', 'the hydrolysis of sucrose', 'the hydrolysis of a peptide', 'the hydrolysis of urea'])
    if D == 1:
        return NQ(r, f'The activation energy for {rx} is {u} kJ mol⁻¹ without an enzyme and {c} kJ mol⁻¹ with an enzyme. By what percentage does the enzyme reduce the activation energy?', (u - c) / u * 100, [c / u * 100, (u - c) / c * 100, u - c], '%', f'({u} − {c}) ÷ {u} × 100 = {fx((u - c) / u * 100, 1)}%.', f=lambda v: fx(v, 1))
    st = f'The activation energy for {rx} is {u} kJ mol⁻¹ without a catalyst and {c} kJ mol⁻¹ with an enzyme. (a) Calculate the percentage reduction in activation energy. (b) Sketch or describe an energy-level diagram for the reaction with and without the enzyme.'
    ans = f'(a) {fx((u - c) / u * 100, 1)}% (b) Same starting and end energy levels; the enzyme curve has a lower peak; activation energy is measured from the reactants to the peak.'
    key = f'(a) ({u} − {c}) ÷ {u} × 100 = {fx((u - c) / u * 100, 1)}% [2] (b) lower peak with enzyme [1]; same energy of reactants / products [1]'
    m = 4
    if D >= 3:
        st += ' (c) Explain how the enzyme lowers the activation energy.'
        ans += ' (c) The substrate binds to the active site forming an enzyme–substrate complex; induced fit strains bonds or holds reactants together so bonds break / form more easily.'
        key += ' (c) E–S complex [1]; strain / orientation [1]'
        m = 6
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def initial_rate(r, D):
    v0 = r.choice([0.4, 0.6, 0.8, 1.2, 1.5, 2.0])
    tmax = r.choice([8, 10, 12])
    pmax = v0 * tmax * 1.2
    ts = [0, 1, 2, 3, 4, 6, 8, 10]
    ps = [pmax * (1 - math.exp(-v0 * t_ / pmax)) for t_ in ts]
    prod, unit = r.choice([('oxygen', 'cm³'), ('glucose', 'mg'), ('product', 'μmol'), ('reducing sugar', 'mg')])
    intro = f'{person(r)} measured the {prod} produced by an enzyme reaction. Time / min: {", ".join(map(str, ts))}. Total {prod} / {unit}: {", ".join(fx(p, 1) for p in ps)}.'
    r1 = float(fx(ps[1], 1)) / 1
    if D == 1:
        return NQ(r, intro + ' What is the mean rate of reaction during the first minute?', r1, [r1 / 2, float(fx(ps[-1], 1)) / 10, r1 * 2], f' {unit} min⁻¹', f'{fx(ps[1], 1)} ÷ 1 = {fx(r1, 2)} {unit} min⁻¹.', f=lambda v: fx(v, 2))
    a, b = 2, 8
    rr = (float(fx(ps[ts.index(b)], 1)) - float(fx(ps[ts.index(a)], 1))) / (b - a)
    st = intro + f' (a) Calculate the mean rate in the first minute. (b) Calculate the mean rate between {a} and {b} minutes. (c) Explain why the rate decreases with time.'
    ans = f'(a) {fx(r1, 2)} {unit} min⁻¹ (b) {fx(rr, 2)} {unit} min⁻¹ (c) Substrate is used up, so there are fewer enzyme–substrate collisions per unit time and fewer E–S complexes form.'
    key = f'(a) {fx(r1, 2)} [1] (b) ({fx(ps[ts.index(b)], 1)} − {fx(ps[ts.index(a)], 1)}) ÷ {b - a} = {fx(rr, 2)} [2] (c) substrate concentration falls [1]; fewer collisions / E–S complexes [1]'
    m = 5
    if D >= 4:
        st += ' (d) Explain why the initial rate is used when comparing enzyme activity under different conditions.'
        ans += ' (d) At the start, substrate concentration is known and has not yet been depleted, and product has not built up, so the rate reflects only the condition being tested.'
        key += ' (d) substrate not yet limiting / known concentration [1]; fair comparison [1]'
        m = 7
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def lysozyme_case(r, D):
    enz, sub, prod = r.choice([('lysozyme', 'peptidoglycan in bacterial cell walls', 'smaller sugar fragments'), ('sucrase', 'sucrose', 'glucose and fructose'), ('catalase', 'hydrogen peroxide', 'water and oxygen'), ('maltase', 'maltose', 'two glucose molecules')])
    intro = f'{cap(enz)} catalyses the breakdown of {sub} into {prod}. Researchers in {city(r)} used X-ray crystallography and found that the active site changes shape slightly when the substrate binds.'
    parts = [lambda r: ('State which hypothesis of enzyme action is supported by this evidence, and explain why.', 'Induced fit: the active site is not rigid, it changes shape around the substrate.', '[2]'),
             lambda r: ('Explain why the enzyme cannot catalyse the breakdown of other substrates.', 'The active site has a specific shape complementary only to its substrate (determined by tertiary structure); other substrates cannot bind / form an E–S complex.', '[2]'),
             lambda r: ('Describe the sequence of events from substrate binding to release of products.', 'Substrate collides with and binds to active site; enzyme–substrate complex forms; active site changes shape / strain on bonds; enzyme–product complex; products released; enzyme unchanged.', '[3]'),
             lambda r: ('Explain why a mutation changing one amino acid far from the active site might still stop the enzyme working.', 'It can change bonding between R groups, so the tertiary structure and active site shape change.', '[2]'),
             lambda r: ('Draw or describe an energy diagram showing the effect of the enzyme.', 'Reaction profile with lower activation energy peak with enzyme; same overall energy change.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how enzymes catalyse reactions, with reference to the lock-and-key and induced-fit hypotheses and to activation energy.', 'Globular proteins with active site; tertiary structure gives specific shape; substrate collides and binds forming E–S complex; lock-and-key rigid fit vs induced fit shape change; strain / orientation lowers activation energy; products released; enzyme unchanged.',
           'active site / specificity [2]; E–S complex [1]; two hypotheses contrasted [2]; activation energy [1] [6]')])
t3a = t

t = T('Factors affecting enzyme action: temperature, pH, enzyme and substrate concentration', 'factors affecting enzyme action')
facts(t, [('optimum temperature', 'the temperature at which an enzyme catalyses a reaction at the maximum rate'), ('denaturation', 'a permanent change in the 3-D shape of a protein (and its active site) caused by breaking hydrogen and ionic bonds'),
          ('optimum pH', 'the pH at which an enzyme works fastest'), ('temperature coefficient (Q10)', 'the factor by which the rate of a reaction increases for a 10 °C rise in temperature'),
          ('limiting factor', 'the factor in shortest supply, which limits the rate of a reaction'), ('buffer solution', 'a solution that resists changes in pH, used to keep pH constant in enzyme investigations')])
mcqs(t, [('Why does the rate of an enzyme reaction increase from 10 °C to 30 °C?', 'Molecules have more kinetic energy so collisions between enzyme and substrate are more frequent', 'More kinetic energy → more successful collisions and E–S complexes.', ['The active site gets larger', 'Activation energy increases', 'More enzyme molecules are made']),
         ('When substrate concentration is very high, increasing it further has no effect on rate. What is the limiting factor?', 'Enzyme concentration', 'All active sites are occupied; more enzyme would increase rate.', ['Substrate concentration', 'Activation energy', 'Product concentration']),
         ('Why does a change in pH away from the optimum reduce enzyme activity?', 'It alters the charges on R groups, breaking ionic and hydrogen bonds in the active site', 'H⁺ / OH⁻ change charges on amino acids in the active site and tertiary structure.', ['It increases kinetic energy', 'It breaks peptide bonds', 'It increases substrate concentration'])])
shorts(t, [('State why a buffer is used in an investigation of the effect of temperature on enzyme activity.', 'To keep pH constant, because pH also affects enzyme activity (control variable).', '[1]'),
           ('Describe how the rate of reaction can be calculated from the time taken for a reaction to reach an end point.', 'Rate = 1 ÷ time (e.g. s⁻¹); multiply by 1000 for convenient numbers.', '[1]')])
explain(t, [('Explain why the rate of an enzyme-catalysed reaction falls rapidly above the optimum temperature.', 'Increased vibration breaks hydrogen and ionic bonds holding the tertiary structure; the active site changes shape so substrate no longer fits; the enzyme is denatured and fewer E–S complexes form.', 'bonds break [1]; active site shape changes [1]; fewer E–S complexes / denatured [1] [3]'),
            ('Explain the effect of increasing enzyme concentration on the rate of reaction when substrate is in excess.', 'More active sites are available, so more E–S complexes form per unit time; rate increases in proportion to enzyme concentration.', '[2]'),
            ('Explain why the rate of reaction levels off as substrate concentration increases.', 'At high substrate concentration all active sites are occupied at any moment (saturated); enzyme concentration becomes the limiting factor; the rate reaches Vmax.', 'active sites saturated [1]; enzyme limiting [1]; Vmax [1] [3]'),
            ('Explain why enzymes from organisms living in hot springs have higher optimum temperatures.', 'Their tertiary structure contains more bonds (e.g. disulfide / ionic bonds) that resist breaking at high temperature, so the active site keeps its shape.', '[2]')])
myths(t, [('At low temperatures enzymes are denatured.', 'At low temperatures enzymes are inactive (little kinetic energy) but not denatured; activity returns when warmed.'),
          ('The optimum temperature of all enzymes is 37 °C.', 'Optimum temperatures vary; human enzymes are often near 37–40 °C, but thermophile enzymes may work best above 70 °C.'),
          ('Adding more substrate always increases the rate of reaction.', 'Once active sites are saturated, enzyme concentration limits the rate.')])

CAT_T = {'setup': lambda r, p: f'{p} added 2 cm³ of catalase extract (from celery) to 10 cm³ of hydrogen peroxide solution at pH 7, and collected the oxygen in a gas syringe for 1 minute at different temperatures.',
         'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 20, 30, 40, 50, 60], [15, 25, 35, 45, 55, 65], [20, 30, 40, 50, 60]]),
         'dv': ('volume of oxygen collected in 1 minute', 'cm³'), 'y': lambda x, k: max(0.5, k * 24 * math.exp(-((x - 40) ** 2) / 260)), 'dp': 1,
         'controls': ['volume and concentration of hydrogen peroxide', 'volume and concentration of catalase extract', 'pH (use a buffer)', 'time allowed to equilibrate in the water bath', 'collection time'],
         'why': ('As temperature rises to the optimum, molecules have more kinetic energy so more E–S complexes form per second; above the optimum, hydrogen bonds in the enzyme break, the active site changes shape and the enzyme is denatured.', 'kinetic energy / collisions [1]; optimum [1]; denaturation and active site shape [1] [3]'),
         'improve': ['use a thermostatically controlled water bath', 'pre-incubate the enzyme and substrate separately at the test temperature', 'use a gas syringe rather than counting bubbles'],
         'control': 'Use boiled (denatured) catalase extract with hydrogen peroxide at each temperature; little oxygen should be produced, showing that oxygen production is due to the active enzyme.',
         'extra': [lambda r, d: ('Calculate the temperature coefficient Q10 between the two lowest temperatures tested.', f'{fx(d["means"][1] / d["means"][0], 2)}', f'Q10 = rate at (T + 10) ÷ rate at T = {fx(d["means"][1], 2)} ÷ {fx(d["means"][0], 2)} = {fx(d["means"][1] / d["means"][0], 2)} [2]') if d['xs'][1] - d['xs'][0] == 10 else ('Calculate the mean rate of oxygen production per second at the highest temperature tested.', f'{fx(d["means"][-1] / 60, 3)} cm³ s⁻¹', f'{fx(d["means"][-1], 2)} ÷ 60 = {fx(d["means"][-1] / 60, 3)} [1]')]}
add_practical(t, CAT_T, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))

AMY_PH = {'setup': lambda r, p: f'{p} mixed amylase with starch solution in buffers of different pH at 35 °C. Every 10 s a drop of the mixture was tested with iodine solution on a spotting tile, and the time taken until the iodine no longer turned blue-black was recorded.',
          'iv': ('pH', ''), 'xs': lambda r: r.choice([[4, 5, 6, 7, 8, 9], [3, 5, 7, 9, 11], [5, 6, 7, 8]]), 'xfmt': lambda s_: f'pH {s_}', 'prep': 'at',
          'dv': ('time for starch to disappear', 's'), 'y': lambda x, k: k * (40 + 28 * (x - 6.8) ** 2), 'dp': 0,
          'controls': ['temperature', 'volume and concentration of amylase', 'volume and concentration of starch', 'interval between samples', 'volume of iodine solution'],
          'why': ('The shortest time (fastest rate) is near the optimum pH of amylase; at other pH values H⁺ or OH⁻ ions alter charges on R groups, breaking ionic and hydrogen bonds, so the active site shape changes and fewer E–S complexes form.', 'optimum identified [1]; charges on R groups / bonds broken [1]; active site shape / fewer E–S complexes [1] [3]'),
          'improve': ['test more frequently (e.g. every 5 s) to reduce the uncertainty in the end point', 'use a colorimeter to judge the end point objectively', 'use a narrower range of pH near the optimum'],
          'control': 'Use boiled amylase (or water instead of amylase) with starch at each pH; the iodine should stay blue-black, showing starch breakdown is caused by the enzyme.',
          'extra': [lambda r, d: ('Calculate the rate of reaction, as 1000 ÷ time, at the optimum pH tested.', f'{fx(1000 / min(d["means"]), 2)} s⁻¹', f'1000 ÷ {fx(min(d["means"]), 1)} = {fx(1000 / min(d["means"]), 2)} [2]'),
                    lambda r, d: ('State the uncertainty in the times recorded and explain why.', '±10 s (or ±5 s): samples were tested only every 10 s, so the end point lies between two tests.', '±10 s [1]; sampling interval [1] [2]')]}
add_practical(t, AMY_PH, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))

TRYP = {'setup': lambda r, p: f'{p} added trypsin solutions of different concentrations to milk-powder suspension at 30 °C and recorded the time for the suspension to become clear as casein was hydrolysed.',
        'iv': ('trypsin concentration', '%'), 'xs': lambda r: r.choice([[0.2, 0.4, 0.6, 0.8, 1.0], [0.25, 0.5, 0.75, 1.0], [0.1, 0.2, 0.4, 0.6, 0.8, 1.0]]),
        'dv': ('time for milk to clear', 's'), 'y': lambda x, k: k * 60 / x, 'dp': 0,
        'controls': ['volume and concentration of milk suspension', 'temperature', 'pH (buffer)', 'volume of trypsin solution', 'end point judged the same way (e.g. a cross seen through the tube)'],
        'why': ('Higher trypsin concentration gives more active sites, so more enzyme–substrate complexes form per second and casein is hydrolysed faster; time is inversely proportional to concentration because substrate is in excess.', 'more active sites [1]; more E–S complexes per unit time [1]; substrate in excess [1] [3]'),
        'improve': ['use a colorimeter to measure the end point', 'place a printed cross behind the tube and record when it becomes visible'],
        'control': 'Use boiled trypsin solution with the milk suspension; it should not clear.',
        'extra': [lambda r, d: ('Calculate the rate of reaction (1 ÷ time) for the highest trypsin concentration, in s⁻¹.', f'{sf(1 / d["means"][-1], 3)} s⁻¹', f'1 ÷ {fx(d["means"][-1], 1)} = {sf(1 / d["means"][-1], 3)} s⁻¹ [2]'),
                  lambda r, d: ('Describe how you would make 10 cm³ of a 0.4% trypsin solution from a 1.0% stock solution.', '4 cm³ of 1.0% stock + 6 cm³ distilled water.', '4 cm³ stock [1]; 6 cm³ water [1] [2]')]}
add_practical(t, TRYP, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4), 'numerical')
def q10(r, D):
    T1 = r.choice([10, 15, 20, 25])
    r1 = round(r.uniform(0.8, 3.0), 2)
    qv = round(r.uniform(1.7, 2.6), 1)
    r2 = round(r1 * qv, 2)
    if D == 1:
        return NQ(r, f'The rate of an enzyme reaction is {r1} units s⁻¹ at {T1} °C and {r2} units s⁻¹ at {T1 + 10} °C. What is the Q10?', r2 / r1, [r1 / r2, r2 - r1, (r2 - r1) / 10], '', f'Q10 = {r2} ÷ {r1} = {fx(r2 / r1, 2)}.', f=lambda v: fx(v, 2))
    t1, t2 = r.choice([(40, 120), (25, 90), (60, 200), (30, 75)])
    tt1 = round(t2 / qv)
    st = f'In an investigation in {city(r)}, an enzyme took {t2} s to reach the end point at {T1} °C and {tt1} s at {T1 + 10} °C. (a) Calculate the rate (1000 ÷ time) at each temperature. (b) Calculate Q10.'
    ra, rb = 1000 / t2, 1000 / tt1
    ans = f'(a) {fx(ra, 2)} s⁻¹ and {fx(rb, 2)} s⁻¹ (b) {fx(rb / ra, 2)}'
    key = f'(a) 1000 ÷ {t2} = {fx(ra, 2)}; 1000 ÷ {tt1} = {fx(rb, 2)} [2] (b) {fx(rb, 2)} ÷ {fx(ra, 2)} = {fx(rb / ra, 2)} [1]'
    m = 3
    if D >= 3:
        st += ' (c) Explain why Q10 for enzyme reactions falls sharply at higher temperatures.'
        ans += ' (c) Above the optimum the enzyme is denatured, so the rate no longer increases with temperature (Q10 falls below 1).'
        key += ' (c) denaturation [1]; rate falls / Q10 < 1 [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'case')
def plan_enzyme(r, D):
    enz, sub, meas = r.choice([('catalase from potato', 'hydrogen peroxide', 'volume of oxygen in a gas syringe'), ('amylase', 'starch', 'time until iodine no longer turns blue-black'), ('lipase', 'milk with phenolphthalein', 'time for pink colour to disappear'),
                               ('pectinase', 'apple pulp', 'volume of juice collected in 10 minutes'), ('bromelain from pineapple', 'gelatine', 'time for gelatine to liquefy')])
    iv = r.choice(['temperature', 'pH', 'enzyme concentration', 'substrate concentration'])
    intro = f'{person(r)} plans an investigation into the effect of {iv} on the activity of {enz}, using {sub} as substrate and measuring the {meas}.'
    parts = [lambda r: (f'Identify the independent and dependent variables.', f'Independent: {iv}; dependent: {meas} (or rate calculated from it).', '[2]'),
             lambda r: ('Describe how you would change the independent variable and suggest a suitable range of at least five values.', {'temperature': 'Thermostatic water baths at 20, 30, 40, 50, 60 °C, equilibrating enzyme and substrate separately.', 'pH': 'Buffer solutions at pH 3, 5, 7, 9, 11.', 'enzyme concentration': 'Dilute stock to 0.2, 0.4, 0.6, 0.8, 1.0% using C₁V₁ = C₂V₂.', 'substrate concentration': 'Dilute stock substrate to five concentrations, e.g. 0.5, 1, 2, 3, 4%.'}[iv], 'method [1]; five suitable values [1] [2]'),
             lambda r: ('List three variables that must be standardised and explain how.', 'Any three of temperature (water bath), pH (buffer), volumes and concentrations (syringes / pipettes), time of measurement — excluding the independent variable.', 'three variables with method [3]'),
             lambda r: ('Describe how you would ensure the results are reliable and how you would process them.', 'Repeat at least three times at each value, identify anomalies, calculate means, convert to rate (1 ÷ time or volume ÷ time), plot rate against the independent variable.', '[3]'),
             lambda r: ('Identify one hazard and state a precaution.', 'Hydrogen peroxide / enzymes are irritants or allergens: wear goggles and gloves; hot water: use tongs.', '[1]'),
             lambda r: ('Predict the results and sketch the shape of the expected graph.', {'temperature': 'Rate rises to an optimum then falls steeply (denaturation).', 'pH': 'Bell-shaped curve with a peak at the optimum pH.', 'enzyme concentration': 'Rate increases linearly with enzyme concentration (substrate in excess).', 'substrate concentration': 'Rate increases then levels off at Vmax.'}[iv], '[2]')]
    return compose(r, intro, parts, k=(3, 4, 5), type_='case')


longs(t, [('Describe and explain the effects of temperature and pH on the rate of an enzyme-catalysed reaction.', 'Temperature: rate increases with kinetic energy / collisions up to optimum; Q10 about 2; above optimum H-bonds break, active site changes, denaturation, rate falls. pH: optimum; H⁺/OH⁻ change charges on R groups, ionic/H-bonds broken, active site shape changes; extreme pH denatures.',
           'temperature rise explained [2]; denaturation [2]; pH optimum and explanation [2] [6]'),
          ('Explain why the rate of an enzyme-catalysed reaction changes with substrate concentration and with enzyme concentration.', 'Substrate: rate increases as more collisions / E–S complexes, then levels at Vmax when active sites saturated; enzyme then limiting. Enzyme: with excess substrate, rate proportional to enzyme concentration (more active sites); levels if substrate becomes limiting.',
           'substrate effect [3]; enzyme effect [2]; limiting factor idea [1] [6]')])
t3b = t

t = T('Competitive and non-competitive inhibition', 'competitive and non-competitive inhibition')
facts(t, [('competitive inhibitor', 'a molecule with a shape similar to the substrate that binds to the active site, preventing the substrate from binding'),
          ('non-competitive inhibitor', 'a molecule that binds to an enzyme at a site other than the active site, changing the shape of the active site'),
          ('allosteric site', 'a site on an enzyme, other than the active site, to which a regulatory molecule can bind'),
          ('end-product inhibition', 'the control of a metabolic pathway in which the final product inhibits an enzyme earlier in the pathway'),
          ('reversible inhibitor', 'an inhibitor that binds temporarily to an enzyme and can leave it again')])
mcqs(t, [('What is the effect of increasing substrate concentration on the inhibition caused by a competitive inhibitor?', 'The inhibition is reduced', 'Substrate out-competes inhibitor for active sites; Vmax can still be reached.', ['The inhibition increases', 'There is no effect', 'The enzyme is denatured']),
         ('Which describes a non-competitive inhibitor?', 'It binds to a site other than the active site and changes its shape', 'Increasing substrate does not overcome it; Vmax is lowered.', ['It has the same shape as the substrate', 'It binds to the substrate', 'Its effect is overcome by adding more substrate']),
         ('Malonate has a similar shape to succinate, the substrate of succinate dehydrogenase. What type of inhibitor is malonate?', 'Competitive', 'Similar shape → binds to active site.', ['Non-competitive', 'Allosteric activator', 'Coenzyme'])])
shorts(t, [('State one example of a competitive inhibitor and one example of a non-competitive inhibitor.', 'Competitive: malonate (succinate dehydrogenase), penicillin (transpeptidase), ethanol in methanol poisoning. Non-competitive: cyanide (cytochrome oxidase), heavy-metal ions such as lead / mercury.', '[2]'),
           ('State how the Vmax is affected by a competitive and by a non-competitive inhibitor.', 'Competitive: Vmax unchanged (reached at higher substrate concentration). Non-competitive: Vmax reduced.', '[2]')])
explain(t, [('Explain why increasing the substrate concentration overcomes competitive inhibition but not non-competitive inhibition.', 'Competitive inhibitor and substrate compete for the active site; more substrate means more likely to bind than the inhibitor. A non-competitive inhibitor binds elsewhere and changes the active site, so substrate cannot bind whatever its concentration.', 'competition for active site [1]; more substrate wins [1]; non-competitive changes active site shape [1] [3]'),
            ('Explain how end-product inhibition controls a metabolic pathway.', 'The end product binds (non-competitively, at an allosteric site) to an enzyme early in the pathway, reducing its activity; when the product is used up, the inhibition is removed. This prevents waste of resources.', '[3]'),
            ('Explain why heavy-metal ions such as mercury are non-competitive inhibitors.', 'They bind to –SH groups of R groups away from the active site, disrupting bonds (e.g. disulfide bonds) and changing the tertiary structure and active site shape.', '[2]')])
myths(t, [('Non-competitive inhibitors bind to the active site but more weakly.', 'Non-competitive inhibitors bind to a site other than the active site.'), ('Competitive inhibitors permanently denature the enzyme.', 'Competitive inhibitors usually bind reversibly and do not change the enzyme\'s shape.')])


def mm_table(r, Vmax, Km, kind, I_f):
    S = [0.5, 1, 2, 4, 8, 16]
    base = [Vmax * s / (Km + s) for s in S]
    if kind == 'competitive':
        inh = [Vmax * s / (Km * I_f + s) for s in S]
    else:
        inh = [Vmax / I_f * s / (Km + s) for s in S]
    return S, base, inh


@t.add('C3', (2, 3, 4, 5), 'case')
def inhib_data(r, D):
    Vmax = r.choice([20, 40, 50, 80, 100])
    Km = r.choice([1, 1.5, 2])
    kind = r.choice(['competitive', 'non-competitive'])
    I_f = r.choice([2, 2.5, 3, 4])
    S, base, inh = mm_table(r, Vmax, Km, kind, I_f)
    intro = (f'{person(r)} measured the initial rate of an enzyme reaction (μmol min⁻¹) at different substrate concentrations (mmol dm⁻³), with and without substance X. '
             f'Substrate concentration: {", ".join(fx(s, 1) for s in S)}. Rate without X: {", ".join(fx(v, 1) for v in base)}. Rate with X: {", ".join(fx(v, 1) for v in inh)}.')
    pct_ = (base[0] - inh[0]) / base[0] * 100
    pct2 = (base[-1] - inh[-1]) / base[-1] * 100
    reason = ('the percentage inhibition becomes much smaller at high substrate concentration, as substrate out-competes X for the active site' if kind == 'competitive'
              else 'the percentage inhibition stays about the same at all substrate concentrations and the maximum rate is lowered, so more substrate cannot overcome it')
    parts = [lambda r: ('Calculate the percentage inhibition at the lowest and highest substrate concentrations.', f'{fx(pct_, 1)}% and {fx(pct2, 1)}%', f'({fx(base[0], 1)} − {fx(inh[0], 1)}) ÷ {fx(base[0], 1)} × 100 = {fx(pct_, 1)}% [1]; ({fx(base[-1], 1)} − {fx(inh[-1], 1)}) ÷ {fx(base[-1], 1)} × 100 = {fx(pct2, 1)}% [1] [2]'),
             lambda r: ('Identify the type of inhibition caused by X, using the data to support your answer.', f'{cap(kind)}: {reason}.', f'{kind} [1]; data-based reason [1] [2]'),
             lambda r: ('Explain how X reduces the rate of reaction.', 'X has a similar shape to the substrate and binds to the active site, so fewer E–S complexes form.' if kind == 'competitive' else 'X binds at a site other than the active site, changing the tertiary structure and shape of the active site so substrate cannot bind.', '[2]'),
             lambda r: ('Describe how the data would appear on a graph of rate against substrate concentration.', 'Both curves rise then level off; with X the curve is lower but approaches the same maximum at high substrate.' if kind == 'competitive' else 'Both curves rise then level off; with X the curve levels off at a lower maximum (Vmax reduced).', '[2]'),
             lambda r: ('State two variables that should be kept constant.', 'Temperature; pH; enzyme concentration; concentration of X.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def inhib_case(r, D):
    drug, enz, use = r.choice([('penicillin', 'transpeptidase, which cross-links peptidoglycan in bacterial walls', 'treating bacterial infections'), ('methotrexate', 'dihydrofolate reductase, needed for DNA synthesis', 'cancer chemotherapy'),
                               ('ethanol', 'alcohol dehydrogenase, which converts methanol into toxic methanal', 'treating methanol poisoning'), ('captopril', 'angiotensin-converting enzyme (ACE)', 'reducing high blood pressure')])
    intro = f'In a hospital in {city(r)}, {drug} is used for {use}. It inhibits {enz}, and its effect is reduced when the concentration of the normal substrate is high.'
    parts = [lambda r: (f'Identify the type of inhibition shown by {drug}, giving a reason.', 'Competitive: its effect is reduced by high substrate concentration, as substrate competes for the active site.', '[2]'),
             lambda r: (f'Suggest a feature of the {drug} molecule that allows it to inhibit the enzyme.', 'Its shape is similar to the substrate / complementary to the active site.', '[1]'),
             lambda r: ('Explain why a drug that acts as a non-competitive inhibitor would not be reversed by adding substrate.', 'It binds elsewhere and changes active site shape; substrate cannot bind regardless of concentration.', '[2]'),
             lambda r: ('Describe the effect of the drug on the Vmax and on the substrate concentration needed to reach half Vmax.', 'Vmax unchanged; higher substrate concentration needed to reach Vmax/2 (apparent Km increases).', '[2]'),
             lambda r: ('Suggest why the dose of the drug must be controlled carefully.', 'Too little: substrate out-competes it, no effect; too much: may inhibit enzymes in healthy cells / side effects.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Compare competitive and non-competitive inhibition of enzymes, and explain how end-product inhibition regulates metabolic pathways.', 'Competitive: similar shape, binds active site, reversible, overcome by high substrate, Vmax unchanged, Km increased. Non-competitive: binds elsewhere (allosteric), changes active-site shape, not overcome by substrate, Vmax reduced. End-product inhibition: product inhibits early enzyme, negative feedback, prevents waste.',
           'competitive [2]; non-competitive [2]; effect of substrate / Vmax [1]; end-product inhibition [1] [6]')])
t3c = t

t = T('Vmax, Michaelis–Menten constant Km and immobilised enzymes', 'vmax, michaelis–menten constant km and immobilised enzymes')
facts(t, [('Vmax', 'the maximum rate of an enzyme-catalysed reaction, reached when all active sites are saturated with substrate'),
          ('Michaelis–Menten constant (Km)', 'the substrate concentration at which an enzyme works at half its maximum rate (½Vmax)'),
          ('affinity', 'how readily an enzyme binds to its substrate; a low Km indicates a high affinity'),
          ('immobilised enzyme', 'an enzyme held in an inert matrix such as alginate beads, so that it can be reused and kept separate from the product'),
          ('alginate', 'a polysaccharide from seaweed that forms beads in calcium chloride solution, used to immobilise enzymes')])
mcqs(t, [('Enzyme A has a Km of 0.2 mmol dm⁻³ and enzyme B has a Km of 2.0 mmol dm⁻³ for the same substrate. Which statement is correct?', 'Enzyme A has the higher affinity for the substrate', 'Lower Km → half Vmax at lower substrate concentration → higher affinity.', ['Enzyme B has the higher affinity', 'Enzyme A has the higher Vmax', 'Both have the same affinity']),
         ('Which is an advantage of immobilising an enzyme?', 'The enzyme can be reused and does not contaminate the product', 'Also often more stable to temperature and pH changes.', ['The enzyme works faster than in solution', 'No substrate is needed', 'The active site becomes larger']),
         ('Why is Km a useful measure of enzyme affinity rather than Vmax?', 'Km does not depend on enzyme concentration, whereas Vmax does', 'Vmax rises with enzyme concentration; Km is a property of the enzyme.', ['Km is easier to measure', 'Vmax is never reached', 'Km is always larger than Vmax'])])
shorts(t, [('Describe how to immobilise an enzyme in alginate beads.', 'Mix enzyme with sodium alginate solution; drip from a syringe into calcium chloride solution; beads form; wash with distilled water.', '[3]'),
           ('State two advantages of immobilised enzymes in industry.', 'Reusable; product not contaminated; more stable at higher temperature / wider pH; continuous process; easy separation.', '[2]')])
explain(t, [('Explain why an immobilised enzyme may give a lower rate than the same enzyme free in solution.', 'Substrate must diffuse into the bead to reach the active sites, and some active sites are inaccessible, so fewer collisions occur per unit time.', '[2]'),
            ('Explain why immobilised enzymes are often more stable at high temperatures.', 'The matrix holds the enzyme molecules and restricts changes in shape, so the tertiary structure is less easily disrupted.', '[2]'),
            ('Explain how Km and Vmax can be estimated from a graph of initial rate against substrate concentration.', 'Read off the plateau value as Vmax; halve it; find the substrate concentration that gives ½Vmax on the curve: this is Km.', 'Vmax plateau [1]; ½Vmax [1]; read Km [1] [3]')])
myths(t, [('An enzyme with a high Km has a high affinity for its substrate.', 'A high Km means a high substrate concentration is needed to reach half Vmax, i.e. a low affinity.'), ('Km is half of Vmax.', 'Km is the substrate concentration at which the rate is half Vmax; it is not a rate.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def km_data(r, D):
    Vmax = r.choice([24, 40, 60, 80, 120])
    Km = r.choice([0.5, 1.0, 2.0, 2.5, 4.0])
    S = [Km / 4, Km / 2, Km, Km * 2, Km * 5, Km * 10, Km * 20]
    v = [Vmax * s / (Km + s) for s in S]
    enz = r.choice(['invertase', 'lactase', 'catalase', 'a protease from papaya', 'acetylcholinesterase'])
    if D == 1:
        return NQ(r, f'The Vmax of {enz} is {Vmax} μmol min⁻¹. At what rate is Km measured?', Vmax / 2, [Vmax, Vmax / 4, Vmax * 2], ' μmol min⁻¹', f'Km is the substrate concentration giving ½Vmax = {fx(Vmax / 2)} μmol min⁻¹.', f=lambda z: fx(z, 1))
    st = (f'The initial rate of reaction of {enz} was measured at different substrate concentrations. Substrate / mmol dm⁻³: {", ".join(fx(s, 3) for s in S)}. Rate / μmol min⁻¹: {", ".join(fx(x, 1) for x in v)}. '
          f'Vmax was found to be {Vmax} μmol min⁻¹. (a) State the rate that corresponds to ½Vmax. (b) Use the data to find Km.')
    ans = f'(a) {fx(Vmax / 2, 1)} μmol min⁻¹ (b) {fx(Km, 3)} mmol dm⁻³'
    key = f'(a) {Vmax} ÷ 2 = {fx(Vmax / 2, 1)} [1] (b) substrate concentration at rate {fx(Vmax / 2, 1)} = {fx(Km, 3)} mmol dm⁻³ [1]'
    m = 2
    if D >= 3:
        k2 = Km * r.choice([0.2, 0.25, 5, 4])
        st += f' (c) A second enzyme catalysing the same reaction has Km = {fx(k2, 3)} mmol dm⁻³. Compare the affinities of the two enzymes for the substrate.'
        hi = enz if Km < k2 else 'the second enzyme'
        ans += f' (c) {cap(hi)} has the lower Km and so the higher affinity: it reaches half its maximum rate at a lower substrate concentration.'
        key += ' (c) lower Km identified [1]; higher affinity explained [1]'
        m += 2
    if D >= 4:
        st += ' (d) Explain why the rate does not increase above Vmax however much substrate is added.'
        ans += ' (d) All active sites are occupied (saturated); enzyme concentration limits the rate.'
        key += ' (d) active sites saturated [1]; enzyme limiting [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


IMMOB = {'setup': lambda r, p: f'{p} packed lactase immobilised in alginate beads into a column and passed milk through at different flow rates, testing the glucose concentration of the product with test strips.',
         'iv': ('flow rate of milk', 'cm³ min⁻¹'), 'xs': lambda r: r.choice([[1, 2, 4, 6, 8], [2, 4, 6, 8, 10], [0.5, 1, 2, 3, 4, 5]]),
         'dv': ('glucose concentration in product', 'mmol dm⁻³'), 'y': lambda x, k: k * 30 / (1 + 0.35 * x), 'dp': 1,
         'controls': ['temperature of milk', 'mass / number of beads in the column', 'concentration of lactase used to make the beads', 'size of the beads', 'type of milk (lactose concentration)'],
         'why': ('At faster flow rates the milk is in contact with the immobilised lactase for less time, so fewer lactose molecules bind to active sites and less is hydrolysed to glucose and galactose.', 'less contact time [1]; fewer E–S complexes / less hydrolysis [1]; glucose from lactose hydrolysis [1] [3]'),
         'improve': ['use a glucose biosensor or colorimeter instead of test strips for more precise values', 'use beads of uniform size made with the same syringe'],
         'control': 'Pass milk through a column of alginate beads made without lactase; no glucose should be detected, showing the enzyme is responsible.',
         'extra': [lambda r, d: ('Explain one advantage of using immobilised lactase rather than lactase in solution to make lactose-free milk.', 'The enzyme is not present in the milk (no separation needed) and can be reused; a continuous process is possible.', '[2]')]}
add_practical(t, IMMOB, C3D=(2, 3, 4), C4D=(3, 4, 5))


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def km_case(r, D):
    k1, k2 = r.choice([(0.1, 1.5), (0.05, 0.8), (0.2, 3.0), (0.5, 5.0)])
    iso = r.choice([('hexokinase', 'glucokinase', 'glucose'), ('enzyme isolated from a thermophilic bacterium', 'the same enzyme from E. coli', 'substrate'), ('lactase variant L1', 'lactase variant L2', 'lactose')])
    intro = f'A biotechnology company in {city(r)} compares two enzymes that act on {iso[2]}: {iso[0]} (Km = {k1} mmol dm⁻³) and {iso[1]} (Km = {k2} mmol dm⁻³). Both have similar Vmax values.'
    parts = [lambda r: ('State which enzyme has the higher affinity for the substrate and explain your answer.', f'{cap(iso[0])}: lower Km, so half Vmax is reached at a lower substrate concentration.', '[2]'),
             lambda r: ('Describe how Km could be found from experimental data.', 'Measure initial rates at a range of substrate concentrations; plot rate against concentration; find Vmax from plateau; Km = substrate concentration at ½Vmax.', '[3]'),
             lambda r: ('Suggest which enzyme would be more useful when the substrate concentration is very low, and why.', f'{cap(iso[0])}: it binds substrate readily and works near its maximum rate at low concentrations.', '[2]'),
             lambda r: ('Describe how the company could immobilise the chosen enzyme.', 'Mix with sodium alginate and drip into calcium chloride to form beads; pack into a column.', '[2]'),
             lambda r: ('Give two advantages of immobilising the enzyme.', 'Reused; product free of enzyme; more stable; continuous process.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain the meaning of Vmax and Km, and discuss the advantages and disadvantages of using immobilised enzymes.', 'Vmax: maximum rate, all active sites saturated, depends on enzyme concentration. Km: substrate concentration at ½Vmax; low Km = high affinity; compare enzymes. Immobilised: reusable, no contamination, stable, continuous; disadvantages: cost of immobilising, lower rate due to diffusion, some active sites blocked.',
           'Vmax [1]; Km and affinity [2]; advantages [2]; disadvantages [1] [6]')])
t3d = t
CHAPTERS[3] = [t3a, t3b, t3c, t3d]


# ===================================================================== 4 Cell membranes and transport
MEMB = {'phospholipids': 'form the bilayer, a barrier to water-soluble (polar) molecules and ions, and give the membrane fluidity',
        'cholesterol': 'regulates fluidity: restricts movement of phospholipids at high temperature and prevents close packing at low temperature; adds stability',
        'channel proteins': 'form water-filled pores that allow specific ions or polar molecules to pass by facilitated diffusion',
        'carrier proteins': 'change shape to move specific molecules across the membrane by facilitated diffusion or active transport',
        'glycoproteins': 'act as receptors for hormones and other signalling molecules and as antigens in cell recognition',
        'glycolipids': 'act as cell-surface markers (antigens) for cell recognition and help cells attach to one another'}
t = T('Fluid mosaic model: phospholipids, proteins, glycoproteins, glycolipids and cholesterol', 'fluid mosaic model')
facts(t, [('fluid mosaic model', 'the model of membrane structure in which proteins are scattered in a fluid phospholipid bilayer and can move within it'),
          ('glycocalyx', 'the layer of carbohydrate chains of glycoproteins and glycolipids on the outer surface of the cell surface membrane'),
          ('intrinsic protein', 'a protein that spans or is embedded within the phospholipid bilayer (transmembrane), such as a channel or carrier protein'),
          ('extrinsic protein', 'a protein on the surface of the membrane, attached to phospholipids or intrinsic proteins'),
          ('partially permeable', 'allowing some molecules (such as water and small non-polar molecules) to pass but not others')] + [(k[:-1] if k.endswith('s') else k, v) for k, v in list(MEMB.items())[:2]])


@t.add('C1', (1, 2, 3), 'mcq')
def memb_role(r, D):
    k = r.choice(list(MEMB))
    return MQ(r, f'Which membrane component has this role: it {MEMB[k]}?', cap(k), [cap(x) for x in MEMB if x != k], f'{cap(k)} {MEMB[k]}.')


@t.add('C3', (1, 2, 3, 4), 'numerical')
def memb_thick(r, D):
    th = r.choice([7, 7.5, 8, 10])
    M = r.choice([150000, 200000, 250000, 300000, 400000])
    img = th * M / 1e6
    if D == 1:
        return NQ(r, f'A cell surface membrane appears {fx(img, 2)} mm thick in an electron micrograph at ×{M:,}. What is its actual thickness?', th, [th * 10, th / 10, th * 1000], ' nm', f'{fx(img, 2)} mm = {fx(img * 1e6, 0)} nm; ÷ {M:,} = {fx(th, 1)} nm.', f=lambda v: fx(v, 2))
    st = f'In an electron micrograph at ×{M:,}, the cell surface membrane of a red blood cell appears as two dark lines with a light band between them; the total width is {fx(img, 2)} mm. (a) Calculate the actual thickness of the membrane in nm. (b) Explain why the membrane appears as two dark lines separated by a lighter band.'
    return Q(st, f'(a) {fx(th, 1)} nm (b) The heavy-metal stain binds to the hydrophilic phosphate heads on each side, but not to the hydrophobic fatty acid tails in the middle.',
             f'(a) {fx(img, 2)} mm = {fx(img * 1e6, 0)} nm [1]; ÷ {M:,} = {fx(th, 1)} nm [1] (b) heads stained [1]; tails not stained [1] [4]', 'numerical', 4)


BEET = {'setup': lambda r, p: f'{p} cut equal-sized discs of beetroot, washed them, and placed them in distilled water for 30 minutes at different temperatures. The absorbance of the water (caused by red betalain pigment that leaked from the cells) was measured with a colorimeter.',
        'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[20, 30, 40, 50, 60, 70], [10, 25, 40, 55, 70], [30, 40, 50, 60, 70, 80]]),
        'dv': ('absorbance', 'arbitrary units'), 'y': lambda x, k: k * (0.05 + 0.9 / (1 + math.exp(-(x - 52) / 5))), 'dp': 2,
        'controls': ['number, size and surface area of beetroot discs', 'volume of distilled water', 'time in the water', 'washing of discs before the experiment', 'filter / wavelength used in the colorimeter'],
        'why': ('At low temperatures little pigment leaks out. As temperature increases, phospholipids gain kinetic energy and the bilayer becomes more fluid; above about 45–50 °C membrane proteins denature, leaving gaps, so pigment leaks out of the vacuole and cell.', 'increased fluidity of phospholipids [1]; proteins denatured above about 50 °C [1]; pigment leaks through gaps in tonoplast / cell surface membrane [1] [3]'),
        'improve': ['use a cork borer and blade to cut discs of identical size', 'wash discs until no pigment leaks before starting, to remove pigment from cut cells', 'use a thermostatically controlled water bath'],
        'control': 'Discs kept in distilled water at room temperature (or at 20 °C) show the baseline leakage from cut cells; this shows that any extra leakage is caused by temperature.',
        'extra': [lambda r, d: ('Explain why the discs were washed in distilled water before the investigation.', 'To remove pigment released from cells broken when the discs were cut, so that only pigment leaking through damaged membranes is measured.', '[2]'),
                  lambda r, d: ('Explain why the colorimeter is set to zero (calibrated) using distilled water before readings are taken.', 'So that the absorbance recorded is due only to pigment in the solution, not the water or the cuvette.', '[1]')]}
add_practical(t, BEET, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))
mcqs(t, [('Why is the membrane described as "fluid"?', 'Phospholipids and many proteins can move laterally within the bilayer', 'The components move about; proteins form a "mosaic".', ['It contains water', 'It is a liquid', 'It is fully permeable']),
         ('Which molecules can diffuse directly through the phospholipid bilayer?', 'Oxygen and carbon dioxide', 'Small non-polar molecules dissolve in the hydrophobic core.', ['Glucose and amino acids', 'Sodium and chloride ions', 'Proteins and starch'])])
shorts(t, [('State the approximate thickness of a cell surface membrane.', 'About 7–10 nm.', '[1]'),
           ('State two functions of membranes within cells.', 'Compartmentalisation (separate reactions in organelles); provide surfaces for enzymes (e.g. cristae); control what enters / leaves organelles; form vesicles.', '[2]')])
explain(t, [('Explain why ions cannot diffuse through the phospholipid bilayer.', 'Ions are charged and surrounded by water molecules, so they cannot pass through the hydrophobic core of fatty acid tails; they need channel or carrier proteins.', '[2]'),
            ('Explain the role of cholesterol in membranes.', 'Cholesterol molecules sit between phospholipids, restricting movement at high temperature and preventing tight packing at low temperature, so regulating fluidity; also reduces permeability to ions and water.', '[3]'),
            ('Explain how glycoproteins are involved in cell signalling and recognition.', 'Their carbohydrate chains act as receptors with specific shapes for hormones / signal molecules, and as antigens recognised by the immune system.', '[2]')])
myths(t, [('The membrane is rigid, with proteins fixed in position.', 'Membranes are fluid; phospholipids and many proteins move laterally.'), ('Cholesterol always makes membranes more fluid.', 'Cholesterol regulates fluidity: it reduces fluidity at high temperatures and prevents solidifying at low temperatures.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def memb_case(r, D):
    org = r.choice(['a bacterium from a hot spring', 'an Arctic fish', 'a desert lizard', 'a plant adapted to frost'])
    intro = f'Researchers in {city(r)} analysed the cell surface membrane of {org} and compared its phospholipids and cholesterol content with those of a related species from a temperate climate.'
    parts = [lambda r: ('Draw or describe the fluid mosaic model of membrane structure.', 'Phospholipid bilayer (heads outwards, tails inwards); intrinsic and extrinsic proteins; glycoproteins and glycolipids on outer surface; cholesterol in bilayer.', '[3]'),
             lambda r: ('Suggest how the fatty acids in the phospholipids might differ in a cold-adapted organism, and explain why.', 'More unsaturated fatty acids (kinks) so phospholipids pack less tightly and the membrane stays fluid at low temperatures.', '[2]'),
             lambda r: ('Explain the importance of keeping the membrane at the right fluidity.', 'Proteins need to move / change shape (carriers, receptors); too fluid → leaky; too rigid → transport and vesicle formation fail.', '[2]'),
             lambda r: ('Explain why the membrane is partially permeable.', 'Hydrophobic core lets small non-polar molecules through but blocks ions / polar molecules, which need specific proteins.', '[2]'),
             lambda r: ('Describe one way to show that membranes become more permeable at high temperatures.', 'Beetroot discs in water at different temperatures; measure pigment leakage with a colorimeter.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the fluid mosaic model of membrane structure and explain the roles of its components.', 'Phospholipid bilayer (barrier to polar substances); cholesterol (fluidity / stability); channel and carrier proteins (transport); glycoproteins and glycolipids (receptors, recognition, adhesion); fluid because components move; mosaic of proteins.',
           'bilayer structure [2]; cholesterol [1]; proteins [1]; glycoproteins / glycolipids [1]; fluid and mosaic explained [1] [6]')])
t4a = t

t = T('Cell signalling across membranes via receptors', 'cell signalling')
facts(t, [('cell signalling', 'the process by which a signal molecule from one cell causes a response in another cell'), ('ligand', 'a signalling molecule that binds to a specific receptor'),
          ('receptor', 'a protein (often a glycoprotein) with a specific shape that binds a particular signalling molecule'), ('second messenger', 'a molecule such as cyclic AMP that relays a signal inside the cell after the receptor is activated'),
          ('signal transduction', 'the conversion of an external signal into a response inside the cell, often via a cascade of reactions')])
mcqs(t, [('Why can steroid hormones such as oestrogen pass directly through the cell surface membrane?', 'They are lipid-soluble (non-polar)', 'Steroids dissolve in the phospholipid bilayer and bind receptors inside the cell.', ['They are very large', 'They are proteins', 'They are charged']),
         ('Why does a hormone affect only its target cells?', 'Only target cells have receptors complementary to the hormone', 'Receptor shape is specific to the ligand.', ['The hormone is carried only to those cells', 'Other cells destroy the hormone', 'Only target cells have mitochondria'])])
shorts(t, [('List the stages of cell signalling across a membrane.', 'Signal released → transported to target → binds to specific receptor → signal transduction (e.g. G protein / second messenger) → response (e.g. enzyme cascade).', '[3]'),
           ('State why water-soluble signalling molecules cannot enter the cell.', 'They are polar / large and cannot cross the hydrophobic bilayer, so they bind to receptors on the surface.', '[1]')])
explain(t, [('Explain how a small signal can produce a large response inside a cell.', 'Binding of one ligand activates many second-messenger molecules, each activating many enzymes in a cascade, so the signal is amplified.', '[2]'),
            ('Explain why the shape of a receptor is important in cell signalling.', 'The receptor\'s binding site is complementary to only one signalling molecule, so only that ligand triggers a response.', '[2]'),
            ('Suggest how a drug could block a signalling pathway at the receptor.', 'It has a similar shape to the ligand and binds to the receptor without activating it, preventing the ligand binding.', '[2]')])
myths(t, [('All hormones enter their target cells to have an effect.', 'Water-soluble hormones such as glucagon bind to surface receptors and act via second messengers.'), ('Receptors on the membrane are made of phospholipids.', 'Receptors are proteins, often glycoproteins.')])
SIG = [('glucagon', 'liver cells', 'binds a surface receptor, activating a G protein and adenylyl cyclase to make cyclic AMP, which activates enzymes that break down glycogen', 'water-soluble'),
       ('adrenaline', 'liver and muscle cells', 'binds a surface receptor, raising cyclic AMP and activating an enzyme cascade that releases glucose', 'water-soluble'),
       ('insulin', 'muscle and liver cells', 'binds a receptor that is a tyrosine kinase, leading to insertion of glucose transporter proteins into the membrane', 'water-soluble'),
       ('oestrogen', 'cells of the uterus lining', 'diffuses through the membrane and binds a receptor in the cytoplasm; the complex enters the nucleus and changes gene transcription', 'lipid-soluble'),
       ('ADH', 'collecting duct cells', 'binds a surface receptor, causing vesicles containing aquaporins to fuse with the membrane', 'water-soluble'),
       ('acetylcholine', 'muscle cells at a neuromuscular junction', 'binds receptor proteins that are ion channels, opening them so sodium ions enter', 'water-soluble')]


@t.add('C3', (1, 2, 3, 4), 'short')
def sig_apply(r, D):
    h, tgt, mech, sol = r.choice(SIG)
    if D == 1:
        return MQ(r, f'Where is the receptor for {h} located?', 'Inside the cell (cytoplasm)' if sol == 'lipid-soluble' else 'On the cell surface membrane', ['On the cell surface membrane', 'Inside the cell (cytoplasm)', 'In the cell wall', 'In the mitochondria', 'In the blood plasma'], f'{cap(h)} is {sol}; {mech}.')
    st = f'{cap(h)} acts on {tgt}. (a) Explain whether its receptor is on the cell surface or inside the cell. (b) Outline how binding of {h} leads to a response.'
    return Q(st, f'(a) {"Inside the cell: it is lipid-soluble and crosses the bilayer" if sol == "lipid-soluble" else "On the cell surface: it is water-soluble and cannot cross the bilayer"}. (b) It {mech}.', '(a) location with reason [2] (b) binding to specific receptor [1]; transduction / response [1] [4]', 'short', 4)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def sig_case(r, D):
    h, tgt, mech, sol = r.choice(SIG)
    intro = f'A pharmacologist in {city(r)} is studying how {h} acts on {tgt}. She finds that 1 molecule of {h} binding to a receptor leads to the production of about {r.choice([10, 100, 1000])} times as many product molecules inside the cell.'
    parts = [lambda r: ('Describe the general stages in cell signalling.', 'Signal secreted and transported; binds to specific receptor on / in target cell; transduction (e.g. second messenger); cellular response.', '[3]'),
             lambda r: ('Explain why only target cells respond.', 'Only they have receptors complementary in shape to the hormone.', '[2]'),
             lambda r: ('Explain how the signal is amplified.', 'Each activated receptor activates many second-messenger molecules / enzymes in a cascade, each acting on many substrate molecules.', '[2]'),
             lambda r: (f'Describe how {h} affects the target cell.', f'It {mech}.', '[2]'),
             lambda r: ('Suggest how a drug might reduce the response to the hormone.', 'Bind to (block) the receptor; inhibit an enzyme in the cascade; reduce receptor number.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the main stages of cell signalling and explain the difference between signalling by water-soluble and lipid-soluble molecules.', 'Secretion, transport, binding to specific receptor, transduction, response. Water-soluble: surface receptors (glycoproteins), G proteins / second messenger cAMP, enzyme cascade, amplification. Lipid-soluble: cross bilayer, intracellular receptor, alter transcription.',
           'stages [2]; water-soluble mechanism [2]; lipid-soluble mechanism [1]; amplification / specificity [1] [6]')])
t4b = t

t = T('Simple and facilitated diffusion, osmosis and water potential', 'simple and facilitated diffusion')
facts(t, [('diffusion', 'the net movement of molecules or ions from a region of higher concentration to a region of lower concentration down a concentration gradient, as a result of their random movement'),
          ('facilitated diffusion', 'the diffusion of specific polar molecules or ions through a membrane via channel or carrier proteins'),
          ('osmosis', 'the net movement of water molecules from a region of higher water potential to a region of lower water potential through a partially permeable membrane'),
          ('water potential (ψ)', 'a measure of the tendency of water to move from one place to another; pure water has a water potential of zero and solutions have negative values'),
          ('solute potential (ψs)', 'the contribution of dissolved solutes to water potential; always negative'), ('pressure potential (ψp)', 'the contribution of pressure (e.g. of a cell wall) to water potential; usually positive in turgid plant cells'),
          ('plasmolysis', 'the loss of water from a plant cell so that the cell surface membrane pulls away from the cell wall'), ('turgid', 'describes a plant cell that is full of water, with the protoplast pushing against the cell wall')])
mcqs(t, [('Which is the water potential of pure water at atmospheric pressure?', '0 kPa', 'Pure water has the highest water potential, defined as zero.', ['100 kPa', '−100 kPa', '1 kPa']),
         ('What happens to an animal cell placed in a solution with a much lower water potential than its cytoplasm?', 'It loses water by osmosis and shrinks (crenates)', 'Water moves out to the lower water potential.', ['It gains water and bursts', 'It becomes turgid', 'It becomes plasmolysed']),
         ('Which factor does not affect the rate of simple diffusion across a membrane?', 'The number of carrier proteins', 'Carrier proteins affect facilitated diffusion only.', ['Surface area', 'Concentration gradient', 'Temperature'])])
shorts(t, [('State the equation linking water potential, solute potential and pressure potential.', 'ψ = ψs + ψp', '[1]'),
           ('State two ways in which facilitated diffusion differs from simple diffusion.', 'Uses channel / carrier proteins; specific to particular molecules; rate limited by number of proteins (levels off); for polar / charged substances.', '[2]')])
explain(t, [('Explain why a plant cell placed in pure water does not burst.', 'Water enters by osmosis; the protoplast pushes against the strong cellulose cell wall, which exerts pressure (pressure potential rises) until ψ inside = 0, so no further net entry.', 'water enters by osmosis [1]; wall resists / pressure potential [1]; equilibrium [1] [3]'),
            ('Explain why red blood cells burst when placed in distilled water.', 'Distilled water has a higher water potential than the cytoplasm; water enters by osmosis; there is no cell wall, so the cell swells and the membrane bursts (haemolysis).', '[3]'),
            ('Explain why the rate of facilitated diffusion levels off at high concentration gradients.', 'The number of channel / carrier proteins is limited; when all are in use, they become the limiting factor.', '[2]'),
            ('Explain how the rate of diffusion of oxygen across a membrane is affected by temperature.', 'Higher temperature gives molecules more kinetic energy, so they move faster and diffusion is faster.', '[2]')])
myths(t, [('Osmosis is the movement of water from a dilute solution to a concentrated solution through any membrane.', 'Osmosis is net movement of water from higher to lower water potential through a partially permeable membrane.'),
          ('A cell with a water potential of −800 kPa has more water potential than one at −300 kPa.', '−300 kPa is the higher (less negative) water potential; water moves from −300 kPa to −800 kPa.'),
          ('Facilitated diffusion uses ATP because it uses proteins.', 'Facilitated diffusion is passive; it uses the concentration gradient, not ATP.')])
relation(t, 'C2', (2, 3, 4), 'rate ∝ (surface area × concentration difference) ÷ thickness', 'rate of diffusion across the membrane',
         {'surface area': 1, 'concentration difference': 1, 'thickness of the membrane': -1},
         ['Oxygen diffuses across the wall of a capillary into a muscle fibre.', 'Carbon dioxide diffuses into a leaf mesophyll cell.', 'A drug diffuses across an artificial membrane in a laboratory model.', 'Urea diffuses across the membrane of a dialysis tube.'])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def wp_calc(r, D):
    a_s = -r.choice([600, 700, 800, 900, 1000, 1200])
    a_p = r.choice([200, 300, 400, 500])
    b_s = -r.choice([400, 500, 600, 700, 800, 1100, 1300])
    b_p = r.choice([100, 200, 300, 400, 600])
    A, B = a_s + a_p, b_s + b_p
    if A == B:
        return None
    a_s, a_p, b_s, b_p, A_, B_ = (mn(x) for x in (a_s, a_p, b_s, b_p, A, B))
    if D == 1:
        return NQ(r, f'A plant cell has a solute potential of {a_s} kPa and a pressure potential of {a_p} kPa. What is its water potential?', A, [A - 2 * int(a_p), -A, A + 100], ' kPa', f'ψ = ψs + ψp = {a_s} + {a_p} = {A_} kPa.', f=lambda v: mn(int(v)))
    hi, lo = ('A', 'B') if A > B else ('B', 'A')
    st = f'Two adjacent plant cells, A and B, are in {r.choice(["a leaf", "a root", "a potato tuber", "an onion bulb"])}. Cell A: ψs = {a_s} kPa, ψp = {a_p} kPa. Cell B: ψs = {b_s} kPa, ψp = {b_p} kPa. (a) Calculate the water potential of each cell. (b) State the direction of net water movement and explain why.'
    ans = f'(a) A: {A_} kPa; B: {B_} kPa (b) From {hi} to {lo}, by osmosis, because {hi} has the higher (less negative) water potential.'
    key = f'(a) A = {a_s} + {a_p} = {A_} [1]; B = {b_s} + {b_p} = {B_} [1] (b) {hi} → {lo} [1]; higher to lower water potential [1]'
    m = 4
    if D >= 4:
        sol = -r.choice([300, 500, 900, 1200, 1500])
        a_sn = -int(a_s.replace('−', '')) if a_s.startswith('−') else int(a_s)
        st += f' (c) Cell A is placed in a sucrose solution with ψ = {mn(sol)} kPa. Predict what happens to cell A and explain your answer.'
        if sol > A:
            ans += f' (c) Cell A gains water by osmosis (solution ψ {mn(sol)} kPa is higher than {A_} kPa) and becomes more turgid; the wall prevents bursting.'
        elif sol < a_sn:
            ans += f' (c) Cell A loses water by osmosis (solution ψ {mn(sol)} kPa is lower than {A_} kPa); its pressure potential falls to zero and, because the solution is below its solute potential, it becomes plasmolysed.'
        else:
            ans += f' (c) Cell A loses water by osmosis (solution ψ {mn(sol)} kPa is lower than {A_} kPa) and becomes less turgid (flaccid), but not fully plasmolysed.'
        key += ' (c) direction of water movement with comparison of ψ [1]; correct outcome for the cell [1]'
        m = 6
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


POTATO = {'setup': lambda r, p: f'{p} cut cylinders of potato tissue with a cork borer, blotted and weighed them, and left them in sucrose solutions of different concentrations for 24 hours. Each cylinder was then blotted and re-weighed, and the percentage change in mass was calculated.',
          'iv': ('sucrose concentration', 'mol dm⁻³'), 'xs': lambda r: r.choice([[0.0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [0.0, 0.15, 0.3, 0.45, 0.6, 0.75]]),
          'dv': ('percentage change in mass', '%'), 'y': lambda x, k: (0.30 * k - x) * 40 + 0.0, 'dp': 1, 'neg': True, 'noise': 0.06,
          'controls': ['size / surface area of potato cylinders (same cork borer)', 'temperature', 'time in solution', 'volume of solution', 'same potato / variety', 'blotting method'],
          'trend': lambda d: 'As the sucrose concentration increases, the percentage change in mass decreases: tissue gains mass in dilute solutions and loses mass in concentrated solutions.',
          'why': ('In dilute solutions the solution has a higher water potential than the potato cells, so water enters by osmosis and mass increases; in concentrated solutions the solution has a lower water potential, so water leaves by osmosis and mass decreases.', 'gain: water enters from higher ψ [1]; loss: water leaves to lower ψ [1]; osmosis through partially permeable membranes [1] [3]'),
          'improve': ['blot each cylinder in the same way before weighing', 'use more concentrations close to the point of no change', 'cover the tubes to prevent evaporation'],
          'control': None, 'graph': True,
          'extra': [lambda r, d: ('Explain why percentage change in mass is calculated rather than change in mass.', 'The cylinders have different starting masses; percentage change allows a fair comparison.', '[2]'),
                    lambda r, d: ('Use the results to estimate the sucrose concentration with the same water potential as the potato tissue, and explain how you did this.', f'About {fx(0.30 * d["kk"], 2)} mol dm⁻³: the concentration where the percentage change in mass is zero (where the line crosses the x-axis).', 'concentration where change = 0 / x-intercept [1]; value within range [1] [2]')]}
add_practical(t, POTATO, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3), 'numerical')
def pct_mass(r, D):
    m0 = round(r.uniform(1.5, 4.0), 2)
    ch = r.choice([-18, -12, -8, -5, 4, 7, 10, 15])
    m1 = round(m0 * (1 + ch / 100), 2)
    p = (m1 - m0) / m0 * 100
    if D == 1:
        return NQ(r, f'A potato cylinder had a mass of {fx(m0, 2)} g before and {fx(m1, 2)} g after 24 h in a sucrose solution. What is the percentage change in mass?', p, [-p, (m1 - m0) / m1 * 100, m1 - m0], '%', f'({fx(m1, 2)} − {fx(m0, 2)}) ÷ {fx(m0, 2)} × 100 = {mn(fx(p, 1))}%.', f=lambda v: mn(fx(v, 1)))
    st = f'A cylinder of {r.choice(["potato", "sweet potato", "carrot", "beetroot"])} tissue had an initial mass of {fx(m0, 2)} g. After 24 hours in a sucrose solution its mass was {fx(m1, 2)} g. (a) Calculate the percentage change in mass. (b) Compare the water potential of the tissue with that of the solution, and explain.'
    gain = m1 > m0
    return Q(st, f'(a) {mn(fx(p, 1))}% (b) ' + ('The solution had a higher water potential than the tissue, so water entered the cells by osmosis.' if gain else 'The solution had a lower water potential than the tissue, so water left the cells by osmosis.'),
             f'(a) ({fx(m1, 2)} − {fx(m0, 2)}) ÷ {fx(m0, 2)} × 100 [1] = {mn(fx(p, 1))}% [1] (b) comparison of ψ [1]; osmosis direction [1] [4]', 'numerical', 4)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def osmo_case(r, D):
    ctx = r.choice(['A gardener in Lima waters a pot plant with fertiliser solution that is far too concentrated and the plant wilts.', 'A nurse in Manila accidentally prepares an intravenous drip using distilled water instead of saline.',
                    'Farmers in a coastal area near Dhaka find that sea water has flooded their rice fields.', 'A chef in Lisbon sprinkles salt on slices of aubergine and notices liquid appearing on the surface.'])
    intro = ctx
    parts = [lambda r: ('Explain the effect in terms of water potential.', 'The external solution has a different water potential from the cells; water moves by osmosis from higher to lower water potential (out of cells into concentrated solution, or into cells from pure water).', '[3]'),
             lambda r: ('Describe what would happen to a plant cell if it lost a lot of water.', 'Vacuole shrinks, pressure potential falls, cell becomes flaccid; then plasmolysed as membrane pulls away from cell wall.', '[2]'),
             lambda r: ('Explain why animal cells are more at risk than plant cells when placed in a solution of high water potential.', 'Animal cells have no cell wall, so they swell and burst; the plant cell wall resists expansion.', '[2]'),
             lambda r: ('State the meaning of the term water potential.', 'The tendency of water to move from one place to another; pure water = 0, solutions negative.', '[1]'),
             lambda r: ('Calculate the water potential of a cell with ψs = −750 kPa and ψp = 250 kPa.', '−500 kPa', '−750 + 250 = −500 kPa [1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain the processes of simple diffusion, facilitated diffusion and osmosis, and describe the effects of placing plant and animal cells in solutions of different water potential.', 'Diffusion: random movement, down gradient, through bilayer (small non-polar). Facilitated: channel / carrier proteins, specific, passive. Osmosis: water from high to low ψ through partially permeable membrane. Higher external ψ: animal cells burst, plant cells turgid. Lower: animal crenate, plant plasmolysed.',
           'three processes defined [3]; animal cells [1]; plant cells [2] [6]')])
t4c = t

t = T('Active transport, endocytosis and exocytosis; surface area to volume ratio', 'active transport')
facts(t, [('active transport', 'the movement of molecules or ions through transport proteins across a membrane against their concentration gradient, using energy from ATP'),
          ('endocytosis', 'the bulk transport of materials into a cell by infolding of the cell surface membrane to form a vesicle'), ('exocytosis', 'the bulk transport of materials out of a cell by fusion of vesicles with the cell surface membrane'),
          ('phagocytosis', 'endocytosis of solid material, such as bacteria, into a phagocytic vesicle'), ('pinocytosis', 'endocytosis of liquid or small dissolved molecules'),
          ('sodium–potassium pump', 'a carrier protein that uses ATP to pump three Na⁺ out of a cell and two K⁺ in')])
mcqs(t, [('Which process requires ATP?', 'Uptake of mineral ions by root hair cells against a concentration gradient', 'Against the gradient → active transport → ATP.', ['Diffusion of oxygen into alveolar capillaries', 'Osmosis into a root hair cell', 'Facilitated diffusion of glucose into red blood cells']),
         ('What is the surface area to volume ratio of a cube with sides of 2 cm?', '3 : 1', 'SA = 6 × 4 = 24 cm²; V = 8 cm³; 24 : 8 = 3 : 1.', ['1 : 3', '6 : 1', '2 : 1']),
         ('Which substance would inhibit active transport but not facilitated diffusion?', 'Cyanide, which stops ATP production in respiration', 'Active transport needs ATP; facilitated diffusion does not.', ['A substance blocking channel proteins', 'A substance lowering the temperature to 30 °C', 'Glucose'])])
shorts(t, [('State two examples of active transport in organisms.', 'Na⁺/K⁺ pump; uptake of mineral ions by root hairs; loading sucrose into phloem; absorption of glucose in the ileum (co-transport); reabsorption in the kidney.', '[2]'),
           ('State the formula for the surface area to volume ratio of a cube of side length L.', 'SA:V = 6L² : L³ = 6/L.', '[1]')])
explain(t, [('Explain how a carrier protein moves a molecule by active transport.', 'The molecule binds to a specific site on the carrier; ATP is hydrolysed, phosphorylating the protein and changing its shape; the molecule is released on the other side; the carrier returns to its original shape.', 'binding [1]; ATP hydrolysis / shape change [1]; release on other side [1] [3]'),
            ('Explain why large organisms need specialised exchange surfaces and transport systems.', 'As size increases, SA:V decreases, so the surface is too small to supply the volume by diffusion, and diffusion distances become too long.', 'SA:V falls [1]; diffusion too slow / distance too great [1] [2]'),
            ('Explain why cells that carry out a lot of active transport contain many mitochondria.', 'Active transport requires ATP, produced by aerobic respiration in mitochondria.', '[2]'),
            ('Describe how a phagocyte takes in a bacterium by endocytosis.', 'Receptors bind the bacterium; the cell surface membrane folds around it (pseudopodia) and fuses, forming a phagocytic vesicle; requires ATP.', '[3]')])
myths(t, [('Active transport moves substances down their concentration gradient using ATP.', 'Active transport moves substances against their concentration gradient.'), ('Larger cubes have a larger surface area to volume ratio.', 'As size increases, volume increases faster than surface area, so SA:V decreases.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def sav(r, D):
    sides = sorted(r.sample([0.5, 1, 1.5, 2, 2.5, 3, 4, 5], 3))
    if D == 1:
        L = sides[1]
        return NQ(r, f'What is the surface area to volume ratio of a cube of agar with sides of {fx(L, 1)} cm?', 6 / L, [L / 6, 6 * L, 6 / L ** 2], ' : 1', f'SA = 6 × {fx(L, 1)}² = {fx(6 * L * L, 2)} cm²; V = {fx(L ** 3, 3)} cm³; ratio = {fx(6 / L, 2)} : 1.', f=lambda v: fx(v, 2))
    rows = '; '.join(f'{fx(L, 1)} cm cube: SA {fx(6 * L * L, 2)} cm², V {fx(L ** 3, 3)} cm³, SA:V {fx(6 / L, 2)} : 1' for L in sides)
    st = f'{person(r)} cut agar cubes with sides of {", ".join(fx(L, 1) for L in sides)} cm. (a) Calculate the surface area, volume and surface area to volume ratio of each cube.'
    ans = f'(a) {rows}'
    key = '(a) surface areas correct [1]; volumes correct [1]; ratios correct [1]'
    m = 3
    if D >= 3:
        st += ' (b) The cubes contain an alkali and phenolphthalein (pink) and are placed in dilute hydrochloric acid. Predict which cube becomes colourless first, and explain why.'
        ans += f' (b) The {fx(sides[0], 1)} cm cube: it has the largest SA:V, so acid diffuses in through a relatively larger surface and has a shorter distance to reach the centre.'
        key += ' (b) smallest cube [1]; largest SA:V / shortest distance [1]'
        m = 5
    if D >= 5:
        st += ' (c) Relate these results to the need for specialised exchange surfaces in large multicellular organisms.'
        ans += ' (c) Large organisms have a small SA:V and long diffusion distances, so diffusion across the body surface cannot supply all cells; they need exchange surfaces with large surface area (e.g. alveoli, villi) and mass transport systems.'
        key += ' (c) small SA:V / long distance [1]; exchange surfaces + transport system [1]'
        m = 7
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


AGAR = {'setup': lambda r, p: f'{p} cut cubes of agar containing phenolphthalein and sodium hydroxide (pink) with different side lengths, placed them in 1 mol dm⁻³ hydrochloric acid and timed how long each took to become colourless.',
        'iv': ('side length of cube', 'cm'), 'xs': lambda r: r.choice([[0.5, 1.0, 1.5, 2.0, 2.5], [0.5, 1.0, 2.0, 3.0], [0.4, 0.8, 1.2, 1.6, 2.0]]),
        'dv': ('time to become colourless', 's'), 'y': lambda x, k: k * 300 * (x / 2) ** 2, 'dp': 0,
        'controls': ['concentration and volume of acid', 'temperature', 'concentration of alkali and indicator in the agar', 'the cubes being fully covered by acid'],
        'why': ('Larger cubes have a smaller surface area to volume ratio and the acid must diffuse a greater distance to reach the centre, so they take longer to become colourless.', 'smaller SA:V [1]; greater diffusion distance [1]; time increases more than proportionally [1] [3]'),
        'improve': ['cut cubes with a scalpel against a ruler on a tile to make them accurate', 'judge the end point against a white tile'], 'control': None,
        'extra': [lambda r, d: (f'Calculate the surface area to volume ratio of the smallest cube.', f'{fx(6 / d["xs"][0], 2)} : 1', f'6 × {fx(d["xs"][0], 2)}² ÷ {fx(d["xs"][0], 2)}³ = {fx(6 / d["xs"][0], 2)} [2]')]}
add_practical(t, AGAR, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def transport_case(r, D):
    cell, sub, ctx = r.choice([('root hair cell', 'nitrate ions', 'the soil contains 0.2 mmol dm⁻³ and the cytoplasm 15 mmol dm⁻³'), ('epithelial cell of the small intestine', 'glucose', 'glucose concentration in the cell is higher than in the lumen'),
                               ('companion cell', 'sucrose', 'sucrose is loaded into sieve tubes'), ('cell in the thyroid gland', 'iodide ions', 'iodide concentration in the cells is about 30 times that in blood')])
    intro = f'In a {cell}, {sub} are absorbed even though {ctx}. When a respiratory inhibitor is added, uptake stops.'
    parts = [lambda r: ('Name the process by which the substance is absorbed and explain the evidence.', 'Active transport: moves against the concentration gradient and stops when respiration (ATP supply) is inhibited.', '[2]'),
             lambda r: ('Describe how a carrier protein carries out this process.', 'Binds substance; ATP hydrolysed, carrier changes shape; releases substance inside; returns to shape.', '[3]'),
             lambda r: ('Suggest two features you would expect to see in this cell in an electron micrograph.', 'Many mitochondria; many carrier proteins / microvilli / folded membrane for large surface area.', '[2]'),
             lambda r: ('Compare active transport with facilitated diffusion.', 'Both use specific transport proteins; active uses ATP and moves against gradient; facilitated is passive and down gradient.', '[2]'),
             lambda r: ('Explain why low oxygen concentration in the surroundings would reduce uptake.', 'Less aerobic respiration, so less ATP for active transport.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe active transport, endocytosis and exocytosis, and explain why each requires energy.', 'Active transport: carrier proteins, against gradient, ATP changes carrier shape (e.g. Na⁺/K⁺ pump). Endocytosis: membrane infolds to form vesicles (phagocytosis / pinocytosis). Exocytosis: vesicles fuse with membrane to secrete (e.g. enzymes, hormones). ATP for carrier shape changes and for moving vesicles / membrane.',
           'active transport [2]; endocytosis [1]; exocytosis [1]; ATP role [1]; examples [1] [6]')])
t4d = t
CHAPTERS[4] = [t4a, t4b, t4c, t4d]


# ===================================================================== 5 The mitotic cell cycle
t = T('Chromosome structure: chromatids, centromere and telomeres', 'chromosome structure')
facts(t, [('chromatid', 'one of two identical copies of a DNA molecule, joined at the centromere after DNA replication'), ('centromere', 'the region of a chromosome where the two sister chromatids are held together and where spindle fibres attach (via the kinetochore)'),
          ('telomere', 'a repetitive, non-coding DNA sequence at the end of a chromosome that protects genes from being lost during replication'),
          ('histone', 'a positively charged protein around which DNA is wound to form chromatin'), ('chromatin', 'the loosely coiled complex of DNA and histone proteins found in the nucleus during interphase'),
          ('homologous chromosomes', 'a pair of chromosomes with the same genes at the same loci, one from each parent'), ('diploid', 'having two complete sets of chromosomes (2n)')])
mcqs(t, [('What holds two sister chromatids together?', 'The centromere', 'Sister chromatids are joined at the centromere until anaphase.', ['The telomere', 'The spindle', 'A histone']),
         ('Why are telomeres needed?', 'DNA polymerase cannot copy the very end of a DNA molecule, so some DNA is lost at each replication', 'Telomeres are non-coding repeats that are lost instead of genes.', ['They attach spindle fibres', 'They code for histones', 'They join homologous chromosomes']),
         ('Which molecule is DNA wound around to form nucleosomes?', 'Histone proteins', 'Positively charged histones attract negatively charged DNA.', ['Tubulin', 'RNA polymerase', 'Collagen'])])
shorts(t, [('Describe the structure of a chromosome at the start of mitosis.', 'Two identical sister chromatids (each one DNA molecule wound around histones, highly condensed) joined at a centromere, with telomeres at the ends.', '[3]'),
           ('State why chromosomes condense at the start of mitosis.', 'Condensed (supercoiled) chromosomes are shorter and thicker so they can be separated without tangling or breaking.', '[1]')])
explain(t, [('Explain why telomeres are important for cells that divide many times.', 'Each round of replication shortens the DNA; telomeres are lost rather than coding genes; when telomeres are too short the cell stops dividing.', '[2]'),
            ('Explain why the two chromatids of a chromosome are genetically identical.', 'They are formed by semi-conservative replication of one DNA molecule during S phase.', '[2]'),
            ('Explain the role of histones in a chromosome.', 'DNA is negatively charged and wraps around positive histones forming nucleosomes; this packs the long DNA into a small nucleus and allows condensation.', '[2]')])
myths(t, [('A chromosome always has two chromatids.', 'After anaphase and during G1 each chromosome is a single chromatid (one DNA molecule).'), ('Telomeres contain the most important genes.', 'Telomeres are non-coding repetitive sequences.')])
ORGS = [('humans', 46), ('a chimpanzee', 48), ('a dog', 78), ('a fruit fly', 8), ('a maize plant', 20), ('an onion', 16), ('a potato', 48), ('a horse', 64), ('a cat', 38), ('a rice plant', 24), ('a garden pea', 14)]


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def chrom_count(r, D):
    org, n2 = r.choice(ORGS)
    stage = r.choice(['G1', 'G2', 'metaphase', 'anaphase', 'telophase (each new nucleus)'])
    dna = {'G1': n2, 'G2': 2 * n2, 'metaphase': 2 * n2, 'anaphase': 2 * n2, 'telophase (each new nucleus)': n2}[stage]
    if D == 1:
        return NQ(r, f'A body cell of {org} has {n2} chromosomes. How many DNA molecules are in the nucleus during G2?', 2 * n2, [n2, n2 // 2, 4 * n2], '', f'After S phase each of the {n2} chromosomes has two chromatids (DNA molecules): {2 * n2}.', f=lambda v: str(int(v)))
    st = (f'The diploid number of {org} is {n2}. Copy and complete the table to show the number of chromosomes, chromatids (where chromosomes have two) and DNA molecules in one cell at: G1, G2, metaphase, and in each daughter nucleus at the end of telophase.')
    ans = f'G1: {n2} chromosomes, {n2} DNA molecules (single chromatids). G2: {n2} chromosomes, {2 * n2} chromatids, {2 * n2} DNA molecules. Metaphase: {n2} chromosomes, {2 * n2} chromatids, {2 * n2} DNA. Telophase (each nucleus): {n2} chromosomes, {n2} DNA molecules.'
    m = 4
    if D >= 4:
        st += f' Explain why the number of DNA molecules in a cell at {stage} is {dna}.'
        ans += ' ' + {'G1': 'In G1 each chromosome is one DNA molecule.', 'G2': 'DNA replicated in S phase, so each chromosome has two chromatids.', 'metaphase': 'Replicated chromosomes line up; each has two chromatids.',
                      'anaphase': 'Chromatids separate but are still in one cell, so the total is unchanged.', 'telophase (each new nucleus)': 'Each nucleus receives one chromatid of each chromosome.'}[stage]
        m = 5
    return Q(st, ans, 'one mark per correct stage [4]' + (' ; explanation [1] [5]' if m == 5 else ''), 'numerical', m)


@t.add('C3', (1, 2, 3, 4), 'numerical')
def telomere_loss(r, D):
    L0 = r.choice([8000, 10000, 12000, 15000])
    loss = r.choice([50, 80, 100, 150, 200])
    crit = r.choice([3000, 4000, 5000])
    n = (L0 - crit) // loss
    if D == 1:
        return NQ(r, f'A telomere is {L0:,} base pairs long and loses {loss} base pairs at each cell division. How long will it be after 20 divisions?', L0 - 20 * loss, [L0 - loss, L0 - 2 * 20 * loss, 20 * loss], ' bp', f'{L0:,} − 20 × {loss} = {L0 - 20 * loss:,} bp.', f=lambda v: f'{int(v):,}')
    st = f'In cultured human fibroblasts, telomeres start at about {L0:,} base pairs and shorten by about {loss} base pairs each division. Cells stop dividing when telomeres reach {crit:,} base pairs. (a) Calculate the maximum number of divisions. (b) Explain why cells stop dividing when telomeres become too short.'
    return Q(st, f'(a) {n} divisions (b) Further replication would lose coding DNA (genes) from the chromosome ends, so the cell stops dividing (senescence).', f'(a) ({L0:,} − {crit:,}) ÷ {loss} = {n} [2] (b) genes would be lost [1]; senescence / stops dividing [1] [4]', 'numerical', 4)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def chrom_case(r, D):
    org, n2 = r.choice(ORGS)
    intro = f'A karyotype prepared from a dividing cell of {org} in a laboratory in {city(r)} shows {n2} chromosomes, each made of two chromatids, arranged in {n2 // 2} homologous pairs.'
    parts = [lambda r: ('State the stage of the cell cycle at which the cells were most likely stopped, and explain why.', 'Metaphase: chromosomes are most condensed and visible, each with two chromatids.', '[2]'),
             lambda r: ('Calculate the number of DNA molecules in the cell.', f'{2 * n2}', f'{n2} × 2 = {2 * n2} [1]'),
             lambda r: ('Explain the meaning of homologous chromosomes.', 'Same genes at the same loci; one maternal and one paternal; same size and centromere position (may have different alleles).', '[2]'),
             lambda r: ('Describe the role of the centromere during mitosis.', 'Holds sister chromatids together; spindle microtubules attach at the kinetochore; centromere splits in anaphase so chromatids separate.', '[2]'),
             lambda r: ('Explain why telomeres are present at the ends of the chromosomes.', 'Non-coding repeats lost at each replication instead of genes; protect chromosome ends.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of a chromosome, including the roles of histones, the centromere and telomeres.', 'DNA wound around histones (nucleosomes), coiled into chromatin; condensed in division; two sister chromatids after replication, joined at centromere (kinetochore for spindle); telomeres = repetitive non-coding ends protecting genes during replication.',
           'DNA + histones [2]; chromatids and centromere [2]; telomeres [2] [6]')])
t5a = t

PHASES = {'prophase': 'chromosomes condense and become visible as two chromatids; nuclear envelope breaks down; centrioles move to the poles and the spindle forms',
          'metaphase': 'chromosomes line up on the equator of the spindle, attached by their centromeres to spindle microtubules',
          'anaphase': 'centromeres divide and sister chromatids are pulled to opposite poles by shortening spindle microtubules',
          'telophase': 'chromatids reach the poles and decondense; nuclear envelopes re-form around each set; spindle breaks down'}
t = T('The mitotic cell cycle: interphase, mitosis and cytokinesis', 'the mitotic cell cycle')
facts(t, [('cell cycle', 'the regular sequence of events between one cell division and the next: interphase, mitosis and cytokinesis'), ('interphase', 'the stage between divisions (G1, S and G2) when the cell grows, replicates DNA and prepares for division'),
          ('mitosis', 'nuclear division that produces two genetically identical nuclei with the same number of chromosomes as the parent nucleus'), ('cytokinesis', 'the division of the cytoplasm to form two cells after nuclear division'),
          ('S phase', 'the stage of interphase in which DNA is replicated'), ('spindle', 'a structure of microtubules that attaches to centromeres and separates chromatids during nuclear division'),
          ('mitotic index', 'the proportion of cells in a sample that are undergoing mitosis (number of cells in mitosis ÷ total number of cells)')])


@t.add('C1', (1, 2, 3), 'mcq')
def phase_id(r, D):
    p = r.choice(list(PHASES))
    return MQ(r, f'In which stage of mitosis does the following occur: {PHASES[p]}?', cap(p), [cap(x) for x in PHASES if x != p] + ['Interphase'], f'{cap(p)}: {PHASES[p]}.')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def mitotic_index(r, D):
    tot = r.choice([200, 250, 300, 400, 500])
    pro, met, ana, tel = r.randint(10, 30), r.randint(5, 15), r.randint(2, 8), r.randint(3, 10)
    mit = pro + met + ana + tel
    inter = tot - mit
    cyc = r.choice([12, 16, 18, 20, 22, 24])
    src = r.choice(['an onion root tip squash', 'a garlic root tip', 'a broad bean root tip', 'a section of a tumour biopsy'])
    if D == 1:
        return NQ(r, f'In {src}, {mit} out of {tot} cells were in mitosis. What is the mitotic index?', mit / tot, [inter / tot, mit / inter, tot / mit], '', f'{mit} ÷ {tot} = {fx(mit / tot, 3)}.', f=lambda v: fx(v, 3))
    st = f'{person(r)} examined {src} stained with acetic orcein and counted: interphase {inter}, prophase {pro}, metaphase {met}, anaphase {ana}, telophase {tel}. (a) Calculate the mitotic index. (b) The cell cycle lasts {cyc} hours. Calculate the time spent in metaphase, in minutes.'
    tm = met / tot * cyc * 60
    ans = f'(a) {fx(mit / tot, 3)} (b) {fx(tm, 1)} minutes'
    key = f'(a) {mit} ÷ {tot} = {fx(mit / tot, 3)} [2] (b) {met} ÷ {tot} × {cyc} × 60 = {fx(tm, 1)} min [2]'
    m = 4
    if D >= 3:
        st += ' (c) Explain why most cells were in interphase.'
        ans += ' (c) Interphase is the longest stage of the cycle (growth, DNA replication, protein synthesis), so at any moment most cells are in it.'
        key += ' (c) longest stage [1]; proportion of cells ∝ time in stage [1]'
        m += 2
    if D >= 5:
        st += ' (d) Suggest why cells from the tip of a root are used, and why the tip is treated with hydrochloric acid before staining.'
        ans += ' (d) The meristem at the tip has many dividing cells; acid hydrolyses the middle lamella / breaks cell walls apart so cells spread in a single layer when squashed and stain enters.'
        key += ' (d) meristem / many dividing cells [1]; acid separates cells / single layer [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


mcqs(t, [('During which stage of the cell cycle is DNA replicated?', 'S phase of interphase', 'Synthesis phase.', ['G1', 'Prophase', 'Anaphase']),
         ('How does cytokinesis differ in plant and animal cells?', 'Plant cells form a cell plate; animal cells form a cleavage furrow', 'Vesicles from Golgi build a new wall in plants; membrane pinches in animals.', ['Only plant cells undergo cytokinesis', 'Animal cells form a cell plate; plant cells pinch in', 'Plant cells use centrioles'])])
shorts(t, [('State three events that occur during interphase.', 'Cell grows; organelles replicated; DNA replicated (S phase); proteins / ATP made; checks for errors.', '[3]'),
           ('State the role of the spindle in mitosis.', 'Microtubules attach to centromeres and pull sister chromatids to opposite poles.', '[1]')])
explain(t, [('Explain why mitosis produces genetically identical daughter cells.', 'DNA is replicated semi-conservatively to give identical sister chromatids; in anaphase one chromatid of each chromosome goes to each pole, so each nucleus gets an identical full set.', '[3]'),
            ('Explain why the cell cycle is controlled by checkpoints.', 'Checkpoints ensure DNA is replicated correctly and chromosomes are attached to the spindle before division, preventing mutations or wrong chromosome numbers being passed on.', '[2]'),
            ('Describe and explain what happens during anaphase.', 'Centromeres split; spindle microtubules shorten pulling sister chromatids (now chromosomes) to opposite poles, centromere first; requires ATP.', '[3]')])
myths(t, [('DNA replication happens during prophase.', 'DNA replication happens in S phase of interphase.'), ('Interphase is a resting stage when nothing happens.', 'During interphase the cell grows, replicates DNA and organelles, and synthesises proteins.')])
ROOT = {'setup': lambda r, p: f'{p} grew garlic roots in water at different temperatures, then prepared root tip squashes and counted the number of cells in mitosis out of 200 cells in each field of view.',
        'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 15, 20, 25, 30, 35], [5, 10, 15, 20, 25, 30], [15, 20, 25, 30, 35]]),
        'dv': ('number of cells in mitosis (out of 200)', 'cells'), 'y': lambda x, k: max(2, k * 34 * math.exp(-((x - 25) ** 2) / 140)), 'dp': 0,
        'controls': ['time spent growing', 'time of day roots were cut', 'length of root tip used', 'concentration and time in hydrochloric acid', 'stain and squashing method', 'number of cells counted'],
        'why': ('Mitosis is controlled by enzymes (e.g. for DNA replication and spindle formation); as temperature rises towards the optimum enzymes work faster, so more cells are dividing; above the optimum, enzymes denature and fewer cells divide.', 'enzymes control the cycle [1]; faster up to optimum [1]; denaturation / fewer cells above [1] [3]'),
        'improve': ['count cells in several fields of view from several root tips and calculate a mean', 'cut all roots at the same time of day'],
        'control': None,
        'extra': [lambda r, d: ('Calculate the mitotic index at the temperature with the highest mean count.', f'{fx(max(d["means"]) / 200, 3)}', f'{fx(max(d["means"]), 1)} ÷ 200 = {fx(max(d["means"]) / 200, 3)} [2]'),
                  lambda r, d: ('Explain why the root tips were placed in hydrochloric acid at 60 °C before staining.', 'To hydrolyse the middle lamella and separate the cells so they spread into a single layer; also stops division (fixes the cells).', '[2]')]}
add_practical(t, ROOT, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C4', (3, 4, 5), 'multi_step')
def cycle_case(r, D):
    g1, s_, g2, m = r.choice([(10, 8, 4, 1), (8, 6, 4, 1), (11, 7, 4, 2), (6, 6, 3, 1)])
    tot = g1 + s_ + g2 + m
    intro = f'In a population of cultured human cells in {city(r)}, the cell cycle takes {tot} hours: G1 {g1} h, S {s_} h, G2 {g2} h and mitosis {m} h.'
    parts = [lambda r: ('Calculate the percentage of the cycle spent in interphase.', f'{fx((tot - m) / tot * 100, 1)}%', f'({tot} − {m}) ÷ {tot} × 100 = {fx((tot - m) / tot * 100, 1)}% [2]'),
             lambda r: ('Describe what happens to the mass of DNA in a cell during one cycle.', 'Constant in G1; doubles during S; stays doubled in G2 and mitosis; halves at cytokinesis.', '[3]'),
             lambda r: ('A drug stops spindle formation. Predict and explain the effect on the cells.', 'Cells arrested in metaphase; chromatids cannot be separated, so no anaphase / division.', '[2]'),
             lambda r: ('Calculate how many cells would be produced from one cell in 4 days if all cells keep dividing.', f'{2 ** (96 // tot):,}', f'96 ÷ {tot} = {96 // tot} complete cycles [1]; 2^{96 // tot} = {2 ** (96 // tot):,} [1] [2]'),
             lambda r: ('Describe the events of prophase.', cap(PHASES['prophase']) + '.', '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the events of the mitotic cell cycle, including interphase, the stages of mitosis and cytokinesis.', 'Interphase: G1 growth, S DNA replication, G2 preparation. Prophase, metaphase, anaphase, telophase described. Cytokinesis: furrow in animals, cell plate in plants.', 'interphase [2]; four stages [4]; cytokinesis [1] [7]')])
t5b = t

t = T('Role of mitosis in growth, repair and asexual reproduction; stem cells and cancer', 'role of mitosis')
facts(t, [('stem cell', 'an unspecialised cell that can divide by mitosis an unlimited number of times and can differentiate into specialised cell types'),
          ('totipotent', 'describes a stem cell that can differentiate into any type of cell, including those of the placenta (e.g. a zygote)'),
          ('pluripotent', 'describes a stem cell that can form almost any cell type of the body (e.g. embryonic stem cells)'),
          ('multipotent', 'describes a stem cell that can form a limited range of cell types (e.g. bone marrow stem cells forming blood cells)'),
          ('tumour', 'a mass of cells formed by uncontrolled mitosis'), ('carcinogen', 'a factor or substance that causes cancer, such as tar, UV light or ionising radiation'),
          ('metastasis', 'the spread of cancer cells from a primary tumour to form secondary tumours elsewhere in the body')])
mcqs(t, [('Which is a role of mitosis?', 'Replacing worn-out skin cells', 'Mitosis gives genetically identical cells for growth, repair, replacement and asexual reproduction.', ['Producing gametes', 'Producing genetic variation', 'Halving chromosome number']),
         ('What is the main cause of cancer?', 'Mutations in genes that control cell division', 'Mutations in proto-oncogenes / tumour suppressor genes lead to uncontrolled mitosis.', ['Infection by bacteria', 'Lack of stem cells', 'Too few mitochondria']),
         ('Which type of stem cell is found in adult bone marrow?', 'Multipotent', 'Bone marrow stem cells form blood cell types only.', ['Totipotent', 'Pluripotent', 'Unipotent zygote'])])
shorts(t, [('State three roles of mitosis in organisms.', 'Growth; repair of tissues; replacement of cells; asexual reproduction; clonal expansion of lymphocytes.', '[3]'),
           ('Name two carcinogens.', 'Tar in tobacco smoke; UV light; X-rays / ionising radiation; asbestos; some viruses.', '[2]')])
explain(t, [('Explain how a tumour forms.', 'Mutation in genes controlling the cell cycle (proto-oncogenes become oncogenes / tumour suppressor genes inactivated); cell divides repeatedly by mitosis without control; mass of cells forms.', '[3]'),
            ('Explain why many anti-cancer drugs also cause hair loss.', 'They target rapidly dividing cells (e.g. by stopping DNA replication or spindle formation); hair follicle cells also divide rapidly.', '[2]'),
            ('Explain why stem cells are important in the treatment of leukaemia.', 'Bone marrow stem cells (from a donor) can divide and differentiate into all blood cell types, replacing cells destroyed by treatment.', '[2]')])
myths(t, [('Cancer cells divide by meiosis.', 'Cancer cells divide by uncontrolled mitosis.'), ('All stem cells can become any kind of cell.', 'Only totipotent / pluripotent stem cells can; adult stem cells are usually multipotent.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def tumour_growth(r, D):
    td = r.choice([2, 3, 4, 5, 6, 8])
    t_ = td * r.choice([3, 4, 5, 6, 8, 10])
    n0 = r.choice([1, 10, 100, 1000])
    n = n0 * 2 ** (t_ // td)
    if D == 1:
        return NQ(r, f'A culture of {n0} cancer cells doubles in number every {td} days. How many cells are present after {t_} days?', n, [n0 * 2 * (t_ // td), n / 2, n * 2], '', f'{t_} ÷ {td} = {t_ // td} doublings; {n0} × 2^{t_ // td} = {n:,}.', f=lambda v: f'{int(v):,}')
    n0 = r.choice([1000, 5000, 10000, 50000])
    n = n0 * 2 ** (t_ // td)
    st = f'A tumour in a patient in {city(r)} was estimated to contain {n0:,} cells at diagnosis, and the cells doubled every {td} days. (a) Calculate the number of cells after {t_} days if untreated. (b) State the type of cell division involved and explain why the cells are genetically identical.'
    ans = f'(a) {n:,} (b) Mitosis: DNA replicated, then sister chromatids separated equally into each daughter nucleus.'
    key = f'(a) {t_ // td} doublings [1]; {n0:,} × 2^{t_ // td} = {n:,} [1] (b) mitosis [1]; identical chromatids separated [1]'
    m = 4
    if D >= 4:
        st += ' (c) Explain why a tumour is more dangerous if it is malignant rather than benign.'
        ans += ' (c) Malignant cells invade tissues and spread by blood / lymph (metastasis) forming secondary tumours; benign tumours stay in one place.'
        key += ' (c) invade / metastasis [1]; benign localised [1]'
        m = 6
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4), 'short')
def mitosis_role(r, D):
    ex = [('a starfish regrowing a lost arm', 'repair / regeneration'), ('a potato plant producing tubers', 'asexual reproduction'), ('a baby growing in length', 'growth'), ('the lining of the small intestine being renewed every few days', 'replacement of cells'),
          ('a cut on the skin healing', 'repair'), ('Hydra producing buds', 'asexual reproduction'), ('a B lymphocyte producing a clone of plasma cells', 'clonal expansion in the immune response'), ('a strawberry plant producing runners', 'asexual reproduction')]
    a, b = r.sample(ex, 2)
    return Q(f'State the role of mitosis in each example and explain why the daughter cells must be genetically identical: (i) {a[0]} (ii) {b[0]}.', f'(i) {cap(a[1])} (ii) {cap(b[1])}. Identical cells keep the same genes so new cells function like the originals / offspring are clones adapted to the same environment.',
             '(i) [1] (ii) [1]; genetically identical explanation [1] [3]', 'short', 3)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def cancer_case(r, D):
    can, carc = r.choice([('lung cancer', 'tar in cigarette smoke'), ('skin cancer (melanoma)', 'UV radiation from sunlight'), ('cervical cancer', 'human papillomavirus (HPV)'), ('leukaemia', 'ionising radiation')])
    intro = f'Doctors in {city(r)} are studying patients with {can}, which is linked to {carc}.'
    parts = [lambda r: (f'Explain how {carc} can lead to the development of a tumour.', 'It causes mutations in genes controlling the cell cycle (oncogenes / tumour suppressor genes), leading to uncontrolled mitosis and a mass of cells.', '[3]'),
             lambda r: ('Distinguish between a benign and a malignant tumour.', 'Benign: slow, encapsulated, does not spread. Malignant: invades tissues, spreads by metastasis.', '[2]'),
             lambda r: ('Suggest how a drug that inhibits DNA replication could slow tumour growth, and why it has side effects.', 'Cells cannot complete S phase so do not divide; other rapidly dividing cells (hair follicles, gut lining, bone marrow) are also affected.', '[3]'),
             lambda r: ('Suggest one way the risk of this cancer could be reduced.', 'Avoid the carcinogen (stop smoking / sunscreen / vaccination against HPV / limit radiation exposure).', '[1]'),
             lambda r: ('Explain why cancer is more common in older people.', 'More time to accumulate mutations in many genes; repair mechanisms less effective.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain the significance of mitosis in growth, repair and asexual reproduction, and discuss the roles of stem cells and the development of cancer.', 'Identical cells for growth, repair, replacement, asexual reproduction, clonal expansion. Stem cells: unspecialised, divide, differentiate; totipotent / pluripotent / multipotent; replace cells. Cancer: mutations in control genes, uncontrolled mitosis, tumour, metastasis, carcinogens.',
           'roles of mitosis [2]; stem cells [2]; cancer [2] [6]')])
t5c = t
CHAPTERS[5] = [t5a, t5b, t5c]


# ===================================================================== 6 Nucleic acids and protein synthesis
_B = 'UCAG'
_AA1 = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
_AA3 = {'F': 'Phe', 'L': 'Leu', 'S': 'Ser', 'Y': 'Tyr', '*': 'STOP', 'C': 'Cys', 'W': 'Trp', 'P': 'Pro', 'H': 'His', 'Q': 'Gln', 'R': 'Arg', 'I': 'Ile', 'M': 'Met',
        'T': 'Thr', 'N': 'Asn', 'K': 'Lys', 'V': 'Val', 'A': 'Ala', 'D': 'Asp', 'E': 'Glu', 'G': 'Gly'}
CODE = {a + b + c: _AA3[_AA1[16 * i + 4 * j + k]] for i, a in enumerate(_B) for j, b in enumerate(_B) for k, c in enumerate(_B)}
SENSE = [c for c, a in CODE.items() if a not in ('STOP', 'Met')]
COMP_D = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
MRNA_FROM_T = {'A': 'U', 'T': 'A', 'C': 'G', 'G': 'C'}
ANTI = {'A': 'U', 'U': 'A', 'C': 'G', 'G': 'C'}


def template_of(mrna):
    return ''.join({'A': 'T', 'U': 'A', 'C': 'G', 'G': 'C'}[b] for b in mrna)


def codons(s):
    return [s[i:i + 3] for i in range(0, len(s) - len(s) % 3, 3)]


def translate(m):
    out = []
    for c in codons(m):
        a = CODE[c]
        if a == 'STOP':
            out.append('STOP')
            break
        out.append(a)
    return out


def code_table(r, cods, extra=4):
    pool = list(dict.fromkeys(cods + r.sample(SENSE, extra)))
    r.shuffle(pool)
    return '; '.join(f'{c} = {CODE[c]}' for c in pool)


t = T('Structure of nucleotides, ATP, DNA and RNA', 'structure of nucleotides')
facts(t, [('nucleotide', 'a molecule made of a pentose sugar, a phosphate group and a nitrogen-containing base'), ('purine', 'a base with a double-ring structure: adenine or guanine'),
          ('pyrimidine', 'a base with a single-ring structure: cytosine, thymine or uracil'), ('phosphodiester bond', 'the bond formed by condensation between the phosphate of one nucleotide and the sugar of the next in a polynucleotide'),
          ('complementary base pairing', 'the pairing of A with T (or U in RNA) by two hydrogen bonds and C with G by three hydrogen bonds'),
          ('antiparallel', 'describes the two strands of DNA, which run in opposite directions (one 5′→3′, the other 3′→5′)'),
          ('ATP', 'adenosine triphosphate: a phosphorylated nucleotide (adenine, ribose and three phosphate groups) that is the universal energy currency of cells')])
mcqs(t, [('Which components make up a DNA nucleotide?', 'Deoxyribose, a phosphate group and one of A, T, C or G', 'DNA uses deoxyribose and thymine.', ['Ribose, a phosphate group and one of A, U, C or G', 'Deoxyribose, three phosphate groups and adenine', 'Ribose, a phosphate group and one of A, T, C or G']),
         ('How many hydrogen bonds form between cytosine and guanine?', 'Three', 'C–G three; A–T two.', ['Two', 'One', 'Four']),
         ('Which is a difference between DNA and RNA?', 'RNA contains uracil instead of thymine', 'Also ribose vs deoxyribose; RNA usually single-stranded.', ['DNA contains ribose', 'RNA is always double-stranded', 'DNA contains uracil']),
         ('Which bond is hydrolysed when ATP releases energy for cell processes?', 'The bond between the second and third phosphate groups', 'ATP → ADP + Pi, catalysed by ATPase.', ['The bond between ribose and adenine', 'A peptide bond', 'A hydrogen bond between bases'])])
shorts(t, [('State three differences between DNA and RNA.', 'DNA: deoxyribose, thymine, double-stranded, long. RNA: ribose, uracil, single-stranded, shorter.', '[3]'),
           ('State two features of ATP that make it suitable as the energy currency of cells.', 'Releases energy in small, manageable amounts; hydrolysed in one step; soluble and easily transported; quickly regenerated from ADP + Pi.', '[2]')])
explain(t, [('Explain why a purine always pairs with a pyrimidine in DNA.', 'A two-ring purine with a one-ring pyrimidine gives a constant width of the double helix; the hydrogen-bonding patterns are complementary (A–T, C–G).', '[2]'),
            ('Explain how the structure of DNA makes it stable.', 'Sugar–phosphate backbone joined by strong covalent phosphodiester bonds; bases protected inside helix; many hydrogen bonds between base pairs; base stacking.', '[3]'),
            ('Explain why DNA with a high proportion of C–G pairs needs a higher temperature to separate its strands.', 'C–G pairs have three hydrogen bonds compared with two for A–T, so more energy is needed to break them.', '[2]')])
myths(t, [('The bases in DNA are joined to each other by phosphodiester bonds.', 'Bases pair by hydrogen bonds; phosphodiester bonds join sugar and phosphate along each strand.'), ('ATP stores large amounts of energy for long periods.', 'ATP is an immediate energy source, used quickly and regenerated; long-term stores are lipids and polysaccharides.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def chargaff(r, D):
    a = r.choice([18, 20, 22, 24, 26, 28, 29, 30, 31, 32, 34])
    g = 50 - a
    org = r.choice(['a bacterium', 'wheat', 'a sea urchin', 'a human liver cell', 'a virus with double-stranded DNA', 'yeast'])
    if D == 1:
        return NQ(r, f'In double-stranded DNA from {org}, {a}% of the bases are adenine. What percentage are guanine?', g, [a, 100 - a, 2 * g], '%', f'A = T = {a}%; A + T = {2 * a}%; C + G = {100 - 2 * a}%, so G = {g}%.', f=lambda v: fx(v, 1))
    bp = r.choice([1200, 1500, 2400, 3000, 6000, 9000])
    st = f'A double-stranded DNA molecule from {org} contains {bp:,} base pairs, and {a}% of its bases are adenine. (a) Calculate the percentage of each of the other three bases. (b) Calculate the number of cytosine bases in the molecule.'
    nC = round(2 * bp * g / 100)
    ans = f'(a) T {a}%, G {g}%, C {g}% (b) {nC:,}'
    key = f'(a) T = {a}% [1]; G = C = (100 − {2 * a}) ÷ 2 = {g}% [1] (b) {2 * bp:,} bases × {g}% = {nC:,} [2]'
    m = 4
    if D >= 3:
        hb = 2 * round(bp * 2 * a / 100 / 2) + 3 * round(bp * 2 * g / 100 / 2)
        st += ' (c) Calculate the total number of hydrogen bonds between the bases.'
        ans += f' (c) {hb:,}'
        key += f' (c) A–T pairs {round(bp * a / 100 * 2 / 2) * 1:,} × 2 + C–G pairs {round(bp * g / 100 * 2 / 2):,} × 3 = {hb:,} [2]'
        m += 2
    if D >= 5:
        st += ' (d) Explain why the percentages of bases in single-stranded RNA from the same cell do not follow the same rule.'
        ans += ' (d) RNA is single-stranded, so bases are not paired with complementary bases; A need not equal U, nor C equal G.'
        key += ' (d) single-stranded / no complementary pairing [1]'
        m += 1
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (1, 2, 3, 4), 'numerical')
def dna_length(r, D):
    bp = r.choice([1500, 3000, 4500, 6000, 12000, 30000])
    L = bp * 0.34
    if D == 1:
        return NQ(r, f'Each base pair in DNA adds 0.34 nm to the length of the molecule. How long is a gene of {bp:,} base pairs?', L, [L * 10, L / 10, bp / 0.34], ' nm', f'{bp:,} × 0.34 = {fx(L, 1)} nm.', f=lambda v: fx(v, 1))
    turns = bp / 10
    st = f'A gene of {bp:,} base pairs codes for a polypeptide. Each base pair adds 0.34 nm, and there are 10 base pairs per turn of the helix. (a) Calculate the length of the gene in μm. (b) Calculate the number of turns. (c) Assuming the whole gene is coding and includes a stop codon, calculate the maximum number of amino acids in the polypeptide.'
    return Q(st, f'(a) {fx(L / 1000, 3)} μm (b) {fx(turns, 0)} (c) {bp // 3 - 1:,}', f'(a) {bp:,} × 0.34 = {fx(L, 1)} nm = {fx(L / 1000, 3)} μm [2] (b) {bp:,} ÷ 10 = {fx(turns, 0)} [1] (c) {bp:,} ÷ 3 = {bp // 3:,} codons; minus stop = {bp // 3 - 1:,} [2] [5]', 'numerical', 5)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def atp_case(r, D):
    n = r.choice([40, 50, 60, 70, 80])
    intro = f'An athlete in {city(r)} uses about {n} kg of ATP per day, but the body contains only about 50 g of ATP at any one time.'
    parts = [lambda r: ('Describe the structure of ATP.', 'Adenine + ribose (adenosine) + three phosphate groups.', '[2]'),
             lambda r: ('Explain how the body can use so much ATP with such a small amount present.', 'ATP is continuously hydrolysed to ADP + Pi and regenerated from them by respiration; it is recycled many times a day.', '[2]'),
             lambda r: ('Calculate how many times each ATP molecule is recycled per day, on average.', f'{fx(n * 1000 / 50, 0)}', f'{n} × 1000 ÷ 50 = {fx(n * 1000 / 50, 0)} [1]'),
             lambda r: ('Give three uses of ATP in muscle cells.', 'Contraction (myosin heads); active transport of Ca²⁺; protein synthesis; glycogen synthesis.', '[3]'),
             lambda r: ('Explain why ATP rather than glucose is used as the immediate energy source.', 'Hydrolysis of ATP is one step releasing small usable amounts; glucose release needs many steps and too much energy at once.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of DNA and compare it with the structure of RNA.', 'Polynucleotides: deoxyribose, phosphate, bases A T C G; phosphodiester bonds; double helix, antiparallel, complementary base pairing by hydrogen bonds (A–T 2, C–G 3); purine–pyrimidine. RNA: ribose, uracil, single-stranded, shorter; types mRNA, tRNA, rRNA.',
           'nucleotide [1]; backbone [1]; double helix / antiparallel [1]; base pairing [1]; RNA differences [2] [6]')])
t6a = t

t = T('Semi-conservative replication of DNA', 'semi-conservative replication')
facts(t, [('semi-conservative replication', 'DNA replication in which each new molecule contains one strand from the original molecule and one newly synthesised strand'),
          ('DNA helicase', 'the enzyme that breaks hydrogen bonds between bases to unwind and separate the two strands of DNA'),
          ('DNA polymerase', 'the enzyme that joins free activated nucleotides to form a new strand complementary to the template, working in the 5′ to 3′ direction'),
          ('DNA ligase', 'the enzyme that joins Okazaki fragments on the lagging strand by forming phosphodiester bonds'),
          ('leading strand', 'the new strand synthesised continuously in the 5′ to 3′ direction towards the replication fork'),
          ('lagging strand', 'the new strand synthesised discontinuously as short Okazaki fragments, away from the replication fork')])
mcqs(t, [('Which enzyme forms phosphodiester bonds between Okazaki fragments?', 'DNA ligase', 'Ligase joins the fragments.', ['DNA helicase', 'RNA polymerase', 'Topoisomerase']),
         ('Why can DNA polymerase only build a new strand in the 5′ to 3′ direction?', 'It can only add nucleotides to the 3′ end of a growing strand', 'Hence one strand is discontinuous.', ['It can only bind to adenine', 'The 5′ end is always on the leading strand', 'It needs ATP at the 5′ end']),
         ('In Meselson and Stahl\'s experiment, what did the DNA band look like after one generation in ¹⁴N medium?', 'A single band at an intermediate (hybrid) density', 'Each molecule had one ¹⁵N strand and one ¹⁴N strand.', ['One heavy and one light band', 'A single heavy band', 'A single light band'])])
shorts(t, [('Name the enzymes involved in DNA replication and state the role of each.', 'Helicase: breaks hydrogen bonds / unwinds; DNA polymerase: joins nucleotides to form new strand; ligase: joins Okazaki fragments.', '[3]'),
           ('State why DNA replication must be accurate.', 'So that daughter cells receive identical genetic information; errors are mutations that may change proteins.', '[1]')])
explain(t, [('Explain why replication is described as semi-conservative.', 'Each new DNA molecule consists of one original (parental) strand, conserved, and one newly made strand.', '[2]'),
            ('Explain why one strand is copied continuously and the other in fragments.', 'The strands are antiparallel; DNA polymerase works only 5′→3′, so one strand is made continuously towards the fork and the other in short fragments away from it, later joined by ligase.', '[3]'),
            ('Explain how complementary base pairing ensures accurate replication.', 'Free nucleotides pair with exposed bases on the template only in the combinations A–T and C–G, so the new strand is complementary to the template and identical to the original partner strand.', '[2]')])
myths(t, [('In replication, the original DNA molecule stays intact and a completely new copy is made.', 'This is conservative replication; DNA replication is semi-conservative.'), ('DNA polymerase breaks the hydrogen bonds between the two strands.', 'DNA helicase breaks the hydrogen bonds; DNA polymerase joins nucleotides.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def meselson(r, D):
    n = r.choice([2, 3, 4, 5])
    tot = 2 ** n
    hyb = 2 / tot * 100
    light = 100 - hyb
    if D == 1:
        return NQ(r, f'Bacteria with DNA containing only ¹⁵N were grown in ¹⁴N medium for {n} generations. What percentage of DNA molecules are hybrid (¹⁵N/¹⁴N)?', hyb, [light, 50, 100 / n], '%', f'After {n} generations, {tot} molecules from each original; 2 are hybrid: 2 ÷ {tot} × 100 = {fx(hyb, 2)}%.', f=lambda v: fx(v, 2))
    st = (f'In an experiment like that of Meselson and Stahl, E. coli was grown for many generations in medium containing ¹⁵N, then transferred to ¹⁴N medium. DNA was extracted and centrifuged after each generation. '
          f'(a) State the expected percentages of heavy (¹⁵N/¹⁵N), hybrid and light (¹⁴N/¹⁴N) DNA after {n} generations in ¹⁴N. (b) Explain your answer.')
    ans = f'(a) heavy 0%, hybrid {fx(hyb, 2)}%, light {fx(light, 2)}% (b) Each original ¹⁵N strand is conserved and always pairs with a new ¹⁴N strand, so there are always 2 hybrid molecules per original molecule; all other molecules ({tot - 2} of {tot}) are light.'
    key = f'(a) heavy 0 [1]; hybrid 2 ÷ {tot} = {fx(hyb, 2)}% [1]; light {fx(light, 2)}% [1] (b) parental strands conserved [1]; each pairs with new ¹⁴N strand [1]'
    m = 5
    if D >= 4:
        st += ' (c) Describe the results that would have been obtained after one generation if replication were conservative.'
        ans += ' (c) Two bands: one heavy (original molecule) and one light (completely new molecule), each 50%.'
        key += ' (c) heavy band + light band [1]; no hybrid [1]'
        m = 7
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (1, 2, 3, 4), 'numerical')
def rep_rate(r, D):
    rate = r.choice([50, 100, 500, 1000])
    size = r.choice([4.6e6, 1.2e7, 3.0e9])
    forks = r.choice([2]) if size < 2e7 else r.choice([10000, 20000, 30000])
    t_s = size / (rate * forks)
    org = 'E. coli (one origin, two forks)' if size == 4.6e6 else ('yeast (many origins)' if size == 1.2e7 else 'a human cell (many origins)')
    if size == 1.2e7:
        forks = r.choice([400, 600, 800])
        t_s = size / (rate * forks)
    if D == 1:
        return NQ(r, f'A DNA polymerase adds {rate} nucleotides per second. How long does it take to copy 60 000 nucleotides?', 60000 / rate, [60000 * rate, rate / 60000 * 1000, 60000 / rate / 60], ' s', f'60 000 ÷ {rate} = {fx(60000 / rate, 1)} s.', f=lambda v: fx(v, 1))
    st = f'The genome of {org} contains {sci(size, 2)} base pairs. Each replication fork copies {rate} base pairs per second and there are {forks:,} replication forks working at once. (a) Calculate the time to replicate the genome in minutes. (b) Explain why eukaryotic chromosomes have many origins of replication.'
    return Q(st, f'(a) {sf(t_s / 60, 3)} min (b) Eukaryotic DNA is very long; with one origin replication would take far too long, so many origins allow S phase to be completed in a few hours.',
             f'(a) {sci(size, 2)} ÷ ({rate} × {forks:,}) = {sf(t_s, 3)} s [1]; ÷ 60 = {sf(t_s / 60, 3)} min [1] (b) long DNA [1]; many origins speed replication [1] [4]', 'numerical', 4)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def rep_case(r, D):
    tmpl = ''.join(r.choice('ATCG') for _ in range(12))
    comp = ''.join(COMP_D[b] for b in tmpl)
    intro = f'A student in {city(r)} models DNA replication. One strand of a short section of DNA has the base sequence {tmpl}.'
    parts = [lambda r: ('Write the base sequence of the complementary strand.', comp, f'{comp} [1]'),
             lambda r: ('Describe the roles of DNA helicase and DNA polymerase in replicating this section.', 'Helicase breaks hydrogen bonds and unwinds the strands; DNA polymerase joins activated nucleotides (complementary to template) by phosphodiester bonds, 5′→3′.', '[3]'),
             lambda r: ('Explain why both new DNA molecules have the same base sequence.', 'Each strand acts as a template; complementary base pairing ensures each new strand is complementary to its template and identical to the old partner strand.', '[2]'),
             lambda r: ('Explain why the cell needs a supply of activated nucleotides and ATP during replication.', 'Nucleotides (with extra phosphates) are the monomers; energy is needed to form phosphodiester bonds / unwind DNA.', '[2]'),
             lambda r: ('Describe the evidence from Meselson and Stahl that supports semi-conservative replication.', '¹⁵N bacteria moved to ¹⁴N; after one generation all DNA hybrid density; after two, half hybrid half light.', '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the process of semi-conservative replication of DNA and the evidence that supports it.', 'Helicase unwinds and breaks H-bonds; strands act as templates; free activated nucleotides pair (A–T, C–G); DNA polymerase forms phosphodiester bonds 5′→3′; leading / lagging strands, Okazaki fragments, ligase; each molecule = one old + one new strand. Meselson–Stahl ¹⁵N/¹⁴N density results.',
           'unwinding [1]; templates and base pairing [1]; polymerase [1]; leading / lagging / ligase [1]; definition [1]; evidence [2] [7]')])
t6b = t

t = T('Transcription, mRNA processing and translation; the genetic code', 'transcription')
facts(t, [('transcription', 'the production of an mRNA molecule complementary to the template strand of a gene, catalysed by RNA polymerase'), ('translation', 'the assembly of a polypeptide at a ribosome using the sequence of codons on mRNA'),
          ('codon', 'a sequence of three bases on mRNA that codes for one amino acid (or a stop signal)'), ('anticodon', 'a sequence of three bases on a tRNA molecule, complementary to a codon on mRNA'),
          ('intron', 'a non-coding sequence within a eukaryotic gene that is removed from primary mRNA by splicing'), ('exon', 'a coding sequence of a gene that remains in mature mRNA after splicing'),
          ('degenerate code', 'a property of the genetic code in which most amino acids are coded for by more than one codon'), ('template strand', 'the strand of DNA that is transcribed (read) to make mRNA')])
mcqs(t, [('Where does transcription take place in a eukaryotic cell?', 'In the nucleus', 'mRNA is made in the nucleus, then leaves through nuclear pores.', ['At ribosomes on the RER', 'In the cytoplasm', 'In the Golgi body']),
         ('What is removed from primary mRNA during processing in eukaryotes?', 'Introns', 'Introns spliced out; exons joined.', ['Exons', 'Codons for the first amino acid', 'The anticodons']),
         ('Which describes the role of tRNA in translation?', 'It carries a specific amino acid and has an anticodon complementary to an mRNA codon', 'tRNA brings amino acids to the ribosome.', ['It carries the code from the nucleus to the ribosome', 'It joins amino acids by peptide bonds', 'It unwinds DNA']),
         ('Why is the genetic code described as degenerate?', 'Most amino acids are coded for by more than one codon', '64 codons, 20 amino acids.', ['Each codon codes for several amino acids', 'Codons overlap', 'The code is different in different organisms'])])
shorts(t, [('State three differences between transcription and translation.', 'Transcription: nucleus, DNA → mRNA, RNA polymerase, RNA nucleotides. Translation: ribosome / cytoplasm, mRNA → polypeptide, tRNA / amino acids, peptide bonds.', '[3]'),
           ('State the role of RNA polymerase.', 'Joins RNA nucleotides complementary to the template strand by phosphodiester bonds, making mRNA.', '[1]')])
explain(t, [('Describe the process of translation.', 'mRNA attaches to ribosome; tRNA with anticodon complementary to start codon brings methionine; second tRNA binds next codon; peptide bond forms between amino acids; ribosome moves along one codon; first tRNA leaves; continues until a stop codon; polypeptide released.', '[4]'),
            ('Explain why the genetic code is described as universal and non-overlapping.', 'Universal: the same codons code for the same amino acids in almost all organisms. Non-overlapping: each base is part of only one codon; read in consecutive triplets.', '[2]'),
            ('Explain why mRNA must be processed before translation in eukaryotic cells.', 'Primary transcript contains introns that do not code for the protein; they are removed by splicing and exons joined, so the mature mRNA has a continuous coding sequence.', '[2]')])
myths(t, [('tRNA molecules carry the genetic code from DNA to the ribosome.', 'mRNA carries the code; tRNA brings specific amino acids.'), ('The anticodon is found on mRNA.', 'Anticodons are on tRNA; codons are on mRNA.'),
          ('The coding strand of DNA is the one transcribed.', 'The template strand is transcribed; the mRNA has the same sequence as the coding strand (with U for T).')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def translation(r, D):
    n = 4 if D <= 2 else (5 if D <= 4 else 6)
    cods = ['AUG'] + [r.choice(SENSE) for _ in range(n - 1)]
    mrna = ''.join(cods)
    tpl = template_of(mrna)
    aas = [CODE[c] for c in cods]
    anti = ' '.join(''.join(ANTI[b] for b in c) for c in cods)
    tab = code_table(r, cods)
    if D == 1:
        c = r.choice(cods[1:])
        a_ = ''.join(ANTI[b] for b in c)
        return MQ(r, f'An mRNA codon is {c}. What is the anticodon on the tRNA that binds to it?', a_, [c, ''.join(COMP_D[b] if b != 'U' else 'A' for b in c), c[::-1], a_[::-1]], f'Anticodon is complementary to the codon: {c} → {a_}.')
    st = f'Part of the template strand of a gene has the base sequence {tpl} (read in the direction of transcription). Use this part of the genetic code (mRNA codons): {tab}. (a) Write the mRNA sequence. (b) Give the sequence of amino acids coded.'
    ans = f'(a) {mrna} (b) {"–".join(aas)}'
    key = f'(a) {mrna} [2] (b) {"–".join(aas)} [2]'
    m = 4
    if D >= 3:
        st += ' (c) Give the anticodons of the tRNA molecules that would bring these amino acids.'
        ans += f' (c) {anti}'
        key += ' (c) all anticodons correct [1]'
        m += 1
    if D >= 5:
        st += ' (d) The mature mRNA of the whole gene is shorter than its primary transcript. Explain why.'
        ans += ' (d) Introns are removed by splicing and exons are joined together.'
        key += ' (d) introns removed / spliced [1]'
        m += 1
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (1, 2, 3, 4), 'numerical')
def splicing(r, D):
    exons = [r.choice([150, 180, 210, 240, 300, 360, 420]) for _ in range(r.choice([3, 4]))]
    introns = [r.choice([200, 450, 600, 900, 1200]) for _ in range(len(exons) - 1)]
    prim = sum(exons) + sum(introns)
    mat = sum(exons)
    if D == 1:
        return NQ(r, f'A primary mRNA transcript of {prim:,} nucleotides contains introns totalling {sum(introns):,} nucleotides. How many nucleotides are in the mature mRNA?', mat, [prim, sum(introns), prim + sum(introns)], '', f'{prim:,} − {sum(introns):,} = {mat:,}.', f=lambda v: f'{int(v):,}')
    st = f'A eukaryotic gene contains {len(exons)} exons of ' + ', '.join(map(str, exons)) + ' base pairs and ' + f'{len(introns)} introns of ' + ', '.join(map(str, introns)) + ' base pairs. (a) Calculate the length of the primary transcript and of the mature mRNA. (b) Assuming the mature mRNA contains only coding codons and one stop codon, calculate the number of amino acids in the polypeptide.'
    return Q(st, f'(a) primary {prim:,} nucleotides; mature {mat:,} nucleotides (b) {mat // 3 - 1}', f'(a) {prim:,} [1]; {mat:,} [1] (b) {mat} ÷ 3 = {mat // 3} codons; − 1 stop = {mat // 3 - 1} [2] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def protein_syn_case(r, D):
    prot, cell = r.choice([('insulin', 'β cells of the pancreas'), ('haemoglobin', 'developing red blood cells'), ('collagen', 'fibroblasts in the skin'), ('amylase', 'salivary gland cells'), ('an antibody', 'plasma cells')])
    intro = f'Scientists in {city(r)} are studying how {cell} make {prot}.'
    parts = [lambda r: ('Describe how the gene is transcribed.', 'Section of DNA unwinds (H-bonds break); RNA polymerase joins free RNA nucleotides complementary to the template strand (A–U, T–A, C–G); phosphodiester bonds; primary mRNA released.', '[3]'),
             lambda r: ('Explain what happens to the primary transcript before it leaves the nucleus.', 'Introns are removed (spliced out) and exons joined to form mature mRNA.', '[2]'),
             lambda r: ('Describe the role of the ribosome in translation.', 'Holds mRNA and two tRNAs; catalyses formation of peptide bonds; moves along mRNA one codon at a time.', '[3]'),
             lambda r: ('Explain why the same mRNA can be translated by many ribosomes at once, and why this is useful.', 'Ribosomes move along mRNA, so others can attach behind (polysome); many copies of the protein made quickly.', '[2]'),
             lambda r: (f'Suggest why {cell} contain large amounts of RER and many ribosomes.', f'{cap(prot)} is a protein made in large amounts (for secretion / function); ribosomes are the site of translation; RER transports protein to Golgi.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how the information in a gene is used to make a polypeptide in a eukaryotic cell.', 'Transcription: RNA polymerase, template strand, complementary RNA nucleotides, primary mRNA; splicing removes introns; mRNA leaves via nuclear pore; translation at ribosome: codons, tRNA anticodons, amino acids, peptide bonds, start / stop codons; genetic code triplet, degenerate, universal.',
           'transcription [2]; processing [1]; translation [3]; genetic code [1] [7]')])
t6c = t

t = T('Gene mutations: substitution, insertion and deletion and their effects', 'gene mutations')
facts(t, [('gene mutation', 'a change in the sequence of base pairs in a DNA molecule that may result in an altered polypeptide'), ('substitution', 'a mutation in which one base pair is replaced by a different base pair'),
          ('frameshift', 'a change in the reading frame of codons caused by insertion or deletion of a number of bases that is not a multiple of three'),
          ('silent mutation', 'a substitution that does not change the amino acid sequence because the new codon codes for the same amino acid'),
          ('nonsense mutation', 'a substitution that changes a codon for an amino acid into a stop codon, producing a shortened polypeptide'), ('mutagen', 'a factor that increases the rate of mutation, such as UV light, X-rays or certain chemicals')])
mcqs(t, [('Which type of mutation is most likely to have the greatest effect on a polypeptide?', 'Deletion of one base near the start of a gene', 'Causes a frameshift so every following codon changes.', ['Substitution of one base near the end of a gene', 'Deletion of three bases near the end of a gene', 'A silent substitution']),
         ('In sickle cell anaemia, the codon GAG for glutamic acid becomes GUG for valine. What type of mutation is this?', 'Substitution', 'One base replaced: A → U in mRNA (T → A in DNA template).', ['Insertion', 'Deletion', 'Frameshift']),
         ('Why may a substitution have no effect on the polypeptide?', 'The genetic code is degenerate, so the new codon may code for the same amino acid', 'Silent mutation.', ['Substitutions only occur in introns', 'The code is non-overlapping', 'tRNA corrects the error'])])
shorts(t, [('State three types of gene mutation.', 'Substitution, insertion, deletion (of bases).', '[2]'),
           ('Name two mutagens.', 'UV light; X-rays / gamma rays; chemicals in tobacco smoke (e.g. benzene); mustard gas.', '[2]')])
explain(t, [('Explain how the sickle cell mutation leads to the symptoms of sickle cell anaemia.', 'Substitution in the β-globin gene changes glutamic acid to valine (non-polar); haemoglobin molecules stick together at low oxygen, forming fibres; red cells become sickle-shaped, carry less oxygen and block capillaries.', '[4]'),
            ('Explain why an insertion of three bases usually has a smaller effect than an insertion of one base.', 'Three bases add one codon (one extra amino acid) without changing the reading frame; one base causes a frameshift, changing all following codons.', '[2]'),
            ('Explain why a mutation in an intron usually has no effect on the protein.', 'Introns are removed from primary mRNA before translation, so they do not affect the amino acid sequence.', '[2]')])
myths(t, [('All mutations are harmful.', 'Many mutations are neutral (e.g. silent) and some are beneficial.'), ('A substitution always causes a frameshift.', 'A substitution changes only one codon; insertions and deletions cause frameshifts.')])


@t.add('C3', (2, 3, 4, 5), 'numerical')
def mutation_q(r, D):
    for _ in range(30):
        cods = ['AUG'] + [r.choice(SENSE) for _ in range(5)] + ['UAA']
        mrna = ''.join(cods)
        kind = r.choice(['substitution', 'deletion', 'insertion'])
        pos = r.randrange(4, 15)
        if kind == 'substitution':
            nb = r.choice([b for b in 'ACGU' if b != mrna[pos]])
            mut = mrna[:pos] + nb + mrna[pos + 1:]
        elif kind == 'deletion':
            mut = mrna[:pos] + mrna[pos + 1:]
        else:
            nb = r.choice('ACGU')
            mut = mrna[:pos] + nb + mrna[pos:]
        if mut[:3] != 'AUG':
            continue
        a0, a1 = translate(mrna), translate(mut)
        break
    else:
        return None
    tpl0, tpl1 = template_of(mrna), template_of(mut[:len(mut) - len(mut) % 3])
    tab = code_table(r, list(dict.fromkeys(codons(mrna) + codons(mut[:len(mut) - len(mut) % 3]))), extra=2)
    if kind == 'substitution':
        if a0 == a1:
            eff = 'Silent mutation: the new codon codes for the same amino acid (degenerate code), so the polypeptide is unchanged.'
        elif 'STOP' in a1[:-1] or len(a1) < len(a0):
            eff = 'Nonsense mutation: a stop codon is formed early, so the polypeptide is shortened and probably non-functional.'
        else:
            eff = 'Missense mutation: one amino acid is changed, which may alter the tertiary structure and function of the protein.'
    else:
        eff = 'Frameshift: every codon after the mutation is changed, so the amino acid sequence after that point is different (and a stop codon may appear early or be lost); the protein is likely to be non-functional.'
    a1s = '–'.join(a1) + ('' if 'STOP' in a1 else ' … (reading frame continues beyond the sequence shown)')
    st = (f'The mRNA from part of a gene is {mrna}. A mutation in the DNA changes the mRNA to {mut[:len(mut) - len(mut) % 3]}' + ('…' if len(mut) % 3 else '') +
          f'. Use these codons: {tab}. (a) Identify the type of mutation. (b) Give the amino acid sequences coded before and after the mutation. (c) Explain the likely effect on the protein.')
    ans = f'(a) {cap(kind)} (b) Before: {"–".join(a0)}; after: {a1s} (c) {eff}'
    key = f'(a) {kind} [1] (b) original sequence [1]; mutant sequence [1] (c) effect explained [2] [5]'
    m = 5
    if D >= 5:
        st += ' (d) Write the original sequence of the DNA template strand.'
        ans += f' (d) {tpl0}'
        key = key[:-4] + f' (d) {tpl0} [1] [6]'
        m = 6
    return Q(st, ans, key, 'numerical', m)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def sickle_case(r, D):
    pct_ = r.choice([10, 15, 20, 25, 30])
    intro = f'In some regions of West Africa, about {pct_}% of people carry the sickle cell allele, HbS. The mutation is a single base substitution in the gene for the β-globin polypeptide, changing codon 6 of the mRNA from GAG (glutamic acid) to GUG (valine).'
    parts = [lambda r: ('State the DNA template strand triplets for the normal and mutant codons.', 'Normal CTC; mutant CAC.', '[2]'),
             lambda r: ('Explain how the change in one amino acid affects the haemoglobin molecule.', 'Valine is non-polar / hydrophobic, unlike charged glutamic acid; at low oxygen it causes HbS molecules to stick together, forming long fibres that distort the red blood cell.', '[3]'),
             lambda r: ('Explain why a substitution often has a smaller effect than a deletion of one base.', 'A substitution affects only one codon; a deletion causes a frameshift altering all subsequent codons.', '[2]'),
             lambda r: ('Suggest why the allele is common in regions where malaria is common.', 'Heterozygotes are more resistant to malaria, so they survive and reproduce; the allele is selected for.', '[2]'),
             lambda r: ('Describe two symptoms of sickle cell anaemia.', 'Anaemia / tiredness (less oxygen carried); pain and organ damage from blocked capillaries.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the different types of gene mutation and explain how each can affect the structure and function of a protein, using sickle cell anaemia as an example.', 'Substitution (silent, missense, nonsense), insertion and deletion (frameshift). Effects on primary → tertiary structure. Sickle cell: GAG→GUG, Glu→Val, HbS polymerises at low O₂, sickling, blocked capillaries, anaemia.',
           'three types [2]; frameshift [1]; silent / nonsense [1]; protein structure link [1]; sickle cell [2] [7]')])
t6d = t
CHAPTERS[6] = [t6a, t6b, t6c, t6d]


# ===================================================================== 7 Transport in plants
t = T('Structure of transport tissues: xylem vessels and phloem sieve tubes in stems, roots and leaves', 'structure of transport tissues')
facts(t, [('xylem vessel', 'a long, hollow tube made of dead cells joined end to end with no end walls, with lignified walls, that carries water and mineral ions'),
          ('sieve tube element', 'a living phloem cell with little cytoplasm and no nucleus, joined end to end with others through sieve plates, that carries sucrose and amino acids'),
          ('companion cell', 'a cell next to a sieve tube element, with a nucleus, many mitochondria and many ribosomes, that loads sucrose and keeps the sieve element alive'),
          ('lignin', 'a strong, waterproof polymer deposited in the walls of xylem vessels, preventing collapse'), ('pit', 'a gap in the lignified wall of a xylem vessel that allows water to move sideways between vessels'),
          ('vascular bundle', 'a group of xylem and phloem tissues, found in the stem, root (stele) and leaf veins'), ('endodermis', 'the layer of cells around the vascular tissue of a root, whose walls contain the Casparian strip')])
TISS = [('in the centre of a root, in a star-shaped arrangement', 'xylem'), ('between the arms of the xylem in a root', 'phloem'), ('towards the inside of each vascular bundle in a stem', 'xylem'),
        ('towards the outside of each vascular bundle in a stem', 'phloem'), ('towards the upper surface in the midrib of a leaf', 'xylem'), ('towards the lower surface in the midrib of a leaf', 'phloem')]


@t.add('C1', (1, 2, 3), 'mcq')
def tissue_pos(r, D):
    pos, tis = r.choice(TISS)
    return MQ(r, f'In a transverse section of a dicotyledonous plant, which tissue is found {pos}?', cap(tis), ['Xylem' if tis == 'phloem' else 'Phloem', 'Cambium', 'Endodermis', 'Cortex'], f'{cap(tis)} is found {pos}.')


XYS = [('a xylem vessel (diameter)', 30, 150), ('a sieve tube element (diameter)', 10, 40), ('a companion cell (width)', 5, 15), ('a vascular bundle (width)', 200, 800), ('a stoma pore (length)', 10, 30), ('a root hair (length)', 200, 1500)]


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def xyl_mag(r, D):
    return mag_item(r, D, XYS)


mcqs(t, [('Why do xylem vessels have no end walls?', 'So that water can flow in a continuous column with little resistance', 'Dead, hollow, no cross-walls.', ['To allow sucrose to pass', 'To let companion cells enter', 'To increase transpiration']),
         ('Which feature is found in sieve tube elements but not in xylem vessels?', 'Living cytoplasm', 'Sieve elements are living; xylem vessels are dead.', ['Lignified walls', 'A nucleus', 'No end walls']),
         ('What is the function of the many mitochondria in companion cells?', 'To provide ATP for active loading of sucrose into sieve tubes', 'Proton pumps need ATP.', ['To carry out photosynthesis', 'To make lignin', 'To store starch'])])
shorts(t, [('State two ways in which xylem vessels are adapted for transporting water.', 'Dead and hollow (no cytoplasm); no end walls; lignified walls resist collapse under tension; pits allow lateral movement; narrow lumen supports cohesion.', '[2]'),
           ('Describe the structure of a sieve plate.', 'The end wall between sieve tube elements perforated by many pores.', '[1]')])
explain(t, [('Compare the structure of xylem vessels and phloem sieve tubes.', 'Xylem: dead, lignified, no end walls, no cytoplasm, pits. Phloem: living, cellulose walls, sieve plates, little cytoplasm, no nucleus, companion cells. Both: long tubes of cells joined end to end.', 'two differences [2]; one similarity [1] [3]'),
            ('Explain why the xylem in a root is in the centre.', 'Central position resists the pulling (tension) forces as the plant is anchored, and receives water passing through the endodermis.', '[2]'),
            ('Explain the role of lignin in xylem.', 'Strengthens walls so vessels do not collapse under tension; waterproof; supports the plant.', '[2]')])
myths(t, [('Phloem carries water up the plant and xylem carries sugar down.', 'Xylem carries water and minerals upwards; phloem carries assimilates (mainly sucrose) up and down.'), ('Sieve tube elements are dead cells like xylem vessels.', 'Sieve tube elements are living but have no nucleus; they depend on companion cells.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def tissue_case(r, D):
    pl = r.choice(['a sunflower (Helianthus) stem', 'a buttercup (Ranunculus) root', 'a privet (Ligustrum) leaf', 'a bean seedling stem'])
    intro = f'{person(r)} examined a transverse section of {pl} with a light microscope and made a low-power plan diagram.'
    parts = [lambda r: ('Describe the distribution of xylem and phloem in this organ.', 'Stem: vascular bundles in a ring, xylem inside, phloem outside. Root: central xylem (star / X shape) with phloem between the arms. Leaf: xylem upper, phloem lower in the midrib.', '[2]'),
             lambda r: ('State two rules that should be followed when drawing a low-power plan.', 'No individual cells; clear continuous lines; outlines of tissues only; correct proportions; labelled with ruled lines; magnification.', '[2]'),
             lambda r: ('Explain how the stain toluidine blue or phloroglucinol helps to identify xylem.', 'Lignin stains differently (red with phloroglucinol / blue-green with toluidine blue), so lignified xylem is distinguished.', '[2]'),
             lambda r: ('Describe how the structure of a companion cell is related to its function.', 'Many mitochondria (ATP for active loading), many ribosomes, nucleus controls sieve element, plasmodesmata link to sieve element.', '[3]'),
             lambda r: ('The image of a xylem vessel is 12 mm wide at ×200. Calculate its actual width.', '60 μm', '12 mm = 12 000 μm; ÷ 200 = 60 μm [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of xylem vessels, sieve tube elements and companion cells and explain how each is adapted to its function.', 'Xylem: dead, lignified, no end walls, pits; continuous column, resists tension. Sieve tubes: living, sieve plates, few organelles, mass flow. Companion cells: nucleus, many mitochondria and ribosomes, plasmodesmata, active loading.',
           'xylem [2]; sieve tube [2]; companion cell [2] [6]')])
t7a = t

t = T('Transpiration and movement of water: apoplast and symplast pathways, cohesion–tension', 'transpiration')
facts(t, [('transpiration', 'the loss of water vapour from the aerial parts of a plant, mainly through stomata in the leaves'), ('apoplast pathway', 'the movement of water through cell walls and intercellular spaces'),
          ('symplast pathway', 'the movement of water through the cytoplasm of cells, connected by plasmodesmata'), ('Casparian strip', 'a band of suberin in the walls of endodermal cells that blocks the apoplast pathway'),
          ('cohesion', 'the attraction between water molecules due to hydrogen bonds, allowing a continuous column of water to be pulled up xylem'),
          ('adhesion', 'the attraction between water molecules and the walls of xylem vessels'), ('potometer', 'apparatus used to measure the rate of water uptake by a leafy shoot, which is approximately equal to the rate of transpiration'),
          ('root pressure', 'pressure generated in roots by active transport of ions into xylem, which draws in water by osmosis')])
mcqs(t, [('What drives the movement of water up the xylem in a tall tree?', 'Tension created by the evaporation of water from the leaves', 'Cohesion–tension: transpiration pull.', ['Root pressure alone', 'Active transport of water', 'Capillarity alone']),
         ('Why does the Casparian strip force water into the symplast pathway?', 'It is waterproof suberin in the endodermal cell walls', 'Water must cross cell surface membranes, allowing control of ions.', ['It is made of cellulose', 'It contains plasmodesmata', 'It is made of lignified xylem']),
         ('Which condition would decrease the rate of transpiration?', 'High humidity', 'Reduces the water potential gradient between leaf air spaces and the atmosphere.', ['High wind speed', 'High temperature', 'High light intensity'])])
shorts(t, [('State four environmental factors that affect the rate of transpiration.', 'Light intensity; temperature; humidity; wind speed (air movement).', 'four [2]; two or three [1] [2]'),
           ('State why a potometer measures water uptake rather than transpiration.', 'Some water taken up is used in photosynthesis or to keep cells turgid; uptake is not exactly equal to loss.', '[1]')])
explain(t, [('Explain how water moves from the soil into the xylem of a root.', 'Water enters root hair cells by osmosis (higher ψ in soil); moves across cortex via apoplast (cell walls) and symplast (cytoplasm, plasmodesmata); Casparian strip blocks apoplast at endodermis so water enters cytoplasm; enters xylem down a ψ gradient.', '[4]'),
            ('Explain how the cohesion–tension theory accounts for the movement of water up the xylem.', 'Water evaporates from mesophyll walls and diffuses out of stomata; water is drawn from xylem, creating tension; hydrogen bonds (cohesion) hold the column together and adhesion to lignified walls; the whole column is pulled up.', '[4]'),
            ('Explain why the rate of transpiration increases with temperature.', 'Water molecules gain kinetic energy, so evaporation from cell walls and diffusion of water vapour out of stomata increase; warmer air holds more water vapour, increasing the ψ gradient.', '[2]'),
            ('Explain why a shoot must be cut and fitted to a potometer under water.', 'To prevent air entering the xylem, which would break the continuous water column (air lock).', '[2]')])
myths(t, [('Water is actively pumped up the xylem using ATP.', 'Water moves passively by cohesion–tension; xylem vessels are dead.'), ('Transpiration happens only through the leaf cuticle.', 'Most transpiration is through stomata; the waxy cuticle reduces loss.')])
POT = {'setup': lambda r, p: f'{p} set up a bubble potometer with a leafy shoot and measured the distance moved by an air bubble along a capillary tube (radius 0.5 mm) in 5 minutes at different wind speeds produced by a fan.',
       'iv': ('distance from fan', 'cm'), 'xs': lambda r: r.choice([[20, 40, 60, 80, 100], [25, 50, 75, 100, 125], [10, 30, 50, 70, 90]]),
       'dv': ('distance moved by bubble in 5 min', 'mm'), 'y': lambda x, k: k * (12 + 900 / (x + 15)), 'dp': 0,
       'controls': ['the same leafy shoot (same leaf area)', 'light intensity', 'temperature', 'humidity', 'time of measurement'],
       'why': ('Closer to the fan the air moves faster, removing water vapour from around the leaf, so the water potential gradient between the air spaces and the atmosphere is steeper and water vapour diffuses out of the stomata faster; the bubble moves further.', 'faster air movement nearer fan [1]; removes water vapour / steeper gradient [1]; faster diffusion through stomata [1] [3]'),
       'improve': ['leave the shoot to acclimatise for 5 minutes at each distance', 'measure leaf area and calculate rate per unit leaf area', 'use an anemometer to measure the wind speed directly'],
       'control': None,
       'extra': [lambda r, d: ('Calculate the volume of water taken up per minute at the closest distance, using volume = πr² × distance.', f'{fx(math.pi * 0.25 * d["means"][0] / 5, 2)} mm³ min⁻¹', f'π × 0.5² × {fx(d["means"][0], 1)} = {fx(math.pi * 0.25 * d["means"][0], 2)} mm³ [1]; ÷ 5 = {fx(math.pi * 0.25 * d["means"][0] / 5, 2)} mm³ min⁻¹ [1] [2]'),
                 lambda r, d: ('Explain why the shoot was cut under water and the apparatus sealed with petroleum jelly.', 'To stop air entering the xylem and breaking the water column, and to stop leaks so that only uptake by the shoot moves the bubble.', '[2]')]}
add_practical(t, POT, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def potometer(r, D):
    rad = r.choice([0.25, 0.4, 0.5, 0.6, 0.75, 1.0])
    dist = r.choice([18, 24, 30, 36, 45, 54, 60, 72])
    tm = r.choice([2, 3, 4, 5, 10])
    vol = math.pi * rad ** 2 * dist
    rate = vol / tm
    if D == 1:
        return NQ(r, f'In a potometer, the bubble moved {dist} mm along a capillary of radius {rad} mm. What volume of water was taken up? (V = πr²l)', vol, [math.pi * rad * dist, math.pi * (2 * rad) ** 2 * dist, rad ** 2 * dist], ' mm³', f'π × {rad}² × {dist} = {fx(vol, 1)} mm³.', f=lambda v: fx(v, 1))
    st = f'A bubble in the capillary tube of a potometer (internal radius {rad} mm) moved {dist} mm in {tm} minutes. (a) Calculate the volume of water taken up. (b) Calculate the rate of water uptake in mm³ min⁻¹.'
    ans = f'(a) {fx(vol, 1)} mm³ (b) {fx(rate, 2)} mm³ min⁻¹'
    key = f'(a) π × {rad}² × {dist} = {fx(vol, 1)} mm³ [2] (b) ÷ {tm} = {fx(rate, 2)} [1]'
    m = 3
    if D >= 3:
        la = r.choice([20, 25, 40, 50, 80])
        st += f' (c) The total leaf area was {la} cm². Calculate the rate per cm² of leaf.'
        ans += f' (c) {fx(rate / la, 3)} mm³ min⁻¹ cm⁻²'
        key += f' (c) {fx(rate, 2)} ÷ {la} = {fx(rate / la, 3)} [1]'
        m += 1
    if D >= 4:
        st += ' (d) Give two reasons why this rate of water uptake may not equal the rate of transpiration.'
        ans += ' (d) Some water is used in photosynthesis / to maintain turgor; some water may be produced by respiration; leaks from the apparatus.'
        key += ' (d) two reasons [2]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def pathway_case(r, D):
    pl = r.choice(['a maize seedling', 'a tomato plant', 'a mangrove tree', 'a eucalyptus tree 60 m tall'])
    intro = f'A plant physiologist in {city(r)} supplied a dye that moves only through cell walls to the roots of {pl}. The dye was found in the walls of cortex cells but stopped at the endodermis.'
    parts = [lambda r: ('Name the pathway taken by the dye and explain why it stopped at the endodermis.', 'Apoplast pathway; the Casparian strip (suberin) in endodermal walls blocks movement through cell walls.', '[3]'),
             lambda r: ('Explain the advantage to the plant of the Casparian strip.', 'Water and ions must pass through cell surface membranes / cytoplasm, so the plant controls which ions enter xylem; prevents back-flow; allows root pressure.', '[2]'),
             lambda r: ('Describe the symplast pathway.', 'Water moves through cytoplasm of cells, from cell to cell via plasmodesmata, by osmosis.', '[2]'),
             lambda r: ('Explain how water is moved up the stem from the root to the leaves.', 'Evaporation and transpiration create tension; cohesion between water molecules (H-bonds) and adhesion to xylem walls; continuous column pulled up (cohesion–tension).', '[3]'),
             lambda r: ('Suggest why the diameter of the trunk of a tree decreases slightly during the day.', 'Tension in xylem during high transpiration pulls vessel walls inwards slightly.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how water moves from the soil, through a plant, to the atmosphere.', 'Osmosis into root hairs; apoplast and symplast across cortex; Casparian strip and endodermis; into xylem; cohesion–tension and adhesion; leaf: from xylem to mesophyll, evaporation from cell walls into air spaces, diffusion out of stomata; factors.',
           'root uptake [1]; pathways [2]; endodermis [1]; cohesion–tension [2]; leaf / stomata [1] [7]')])
t7b = t

XERO = [('thick waxy cuticle', 'reduces evaporation of water through the epidermis'), ('rolled leaves', 'traps humid air inside the roll, reducing the water potential gradient'),
        ('sunken stomata in pits', 'humid air is trapped in the pit, reducing the water potential gradient'), ('hairs on the leaf surface', 'trap a layer of moist air close to the leaf'),
        ('fewer stomata', 'fewer pores for water vapour to diffuse out'), ('leaves reduced to spines', 'smaller surface area for transpiration'),
        ('stomata that open at night', 'cooler night-time conditions mean less evaporation (CAM plants)'), ('succulent stem storing water', 'stores water for use during drought')]
t = T('Xerophytic adaptations', 'xerophytic adaptations')
facts(t, [('xerophyte', 'a plant adapted to survive in dry conditions with little available water'), ('marram grass', 'a xerophytic dune grass with rolled leaves, sunken stomata and hairs'),
          ('hydrophyte', 'a plant adapted to live in water'), ('succulent', 'a plant that stores water in swollen leaves or stems'), ('stomatal density', 'the number of stomata per unit area of leaf surface')])


@t.add('C1', (1, 2, 3), 'mcq')
def xero_id(r, D):
    f, why = r.choice(XERO)
    return MQ(r, f'How does the following feature of a xerophyte reduce water loss: {f}?', cap(why), [cap(x[1]) for x in XERO if x[0] != f], f'{cap(f)}: {why}.')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def stomatal_density(r, D):
    d = r.choice([0.3, 0.4, 0.5])
    base = r.randint(12, 36)
    counts = [max(3, round(base * r.uniform(0.75, 1.25))) for _ in range(5)]
    area = math.pi * (d / 2) ** 2
    mean = sum(counts) / 5
    dens = mean / area
    pl = r.choice(['a sunflower leaf', 'a leaf of a xerophyte', 'a bean leaf', 'an oleander leaf', 'a maize leaf'])
    if D == 1:
        return NQ(r, f'A field of view has a diameter of {d} mm. What is its area? (area = πr²)', area, [math.pi * d ** 2, math.pi * d, d ** 2], ' mm²', f'r = {d / 2} mm; π × {d / 2}² = {fx(area, 3)} mm².', f=lambda v: fx(v, 3))
    st = f'{person(r)} made a nail-varnish impression of the lower epidermis of {pl} and counted stomata in five fields of view, each {d} mm in diameter: {", ".join(map(str, counts))}. (a) Calculate the mean number of stomata per field of view. (b) Calculate the stomatal density in stomata per mm².'
    ans = f'(a) {fx(mean, 1)} (b) {fx(dens, 0)} mm⁻²'
    key = f'(a) {sum(counts)} ÷ 5 = {fx(mean, 1)} [1] (b) area = π × {d / 2}² = {fx(area, 3)} mm² [1]; {fx(mean, 1)} ÷ {fx(area, 3)} = {fx(dens, 0)} mm⁻² [1]'
    m = 3
    if D >= 3:
        st += ' (c) Explain why several fields of view were counted.'
        ans += ' (c) Stomata are not evenly distributed; a mean of several areas is more representative.'
        key += ' (c) uneven distribution / representative [1]'
        m += 1
    if D >= 4:
        st += ' (d) Suggest how the stomatal density of a xerophyte would compare with that of a mesophyte and explain why.'
        ans += ' (d) Lower density (or stomata sunken / only on inner surface), so less water vapour is lost by diffusion.'
        key += ' (d) lower [1]; less transpiration [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


mcqs(t, [('In marram grass, where are the stomata found?', 'On the inner (upper) surface of the rolled leaf, in pits', 'Humid air trapped in the roll and pits.', ['On the outer surface only', 'Only on the stem', 'Marram grass has no stomata']),
         ('Why do many xerophytes have a thick waxy cuticle?', 'To reduce water loss by evaporation through the epidermis', 'Wax is waterproof.', ['To increase light absorption', 'To protect from herbivores only', 'To increase gas exchange'])])
shorts(t, [('State three xerophytic adaptations of marram grass.', 'Rolled leaves; sunken stomata; hairs inside the roll; thick cuticle on outer surface; hinge cells that roll the leaf.', '[3]'),
           ('Name two xerophytic plants.', 'Marram grass (Ammophila); cacti (Opuntia); pine; Euphorbia; Aloe.', '[2]')])
explain(t, [('Explain how rolled leaves and hairs reduce water loss in marram grass.', 'They trap moist air close to the stomata, raising the water potential outside the stomata, reducing the water potential gradient, so less water vapour diffuses out.', '[3]'),
            ('Explain why xerophytes cannot simply close all stomata permanently.', 'Stomata are needed for gas exchange: CO₂ must enter for photosynthesis.', '[2]'),
            ('Explain how CAM plants such as cacti reduce water loss but still photosynthesise.', 'Stomata open at night when it is cooler and more humid; CO₂ is stored as organic acids and released for photosynthesis during the day with stomata closed.', '[3]')])
myths(t, [('Xerophytes do not transpire.', 'Xerophytes transpire, but their adaptations reduce the rate.'), ('Sunken stomata increase the rate of transpiration by increasing surface area.', 'Sunken stomata trap humid air, reducing the water potential gradient and transpiration.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def xero_case(r, D):
    a, b = r.choice([(12, 3), (9, 2), (15, 4), (10, 3)])
    pl = r.choice(['marram grass on a sand dune', 'a cactus in the Atacama Desert', 'an oleander shrub in a hot dry climate', 'Aloe vera grown in Rajasthan'])
    intro = f'Under the same conditions, a mesophyte lost {a} g of water per day and {pl} of similar leaf area lost {b} g per day.'
    parts = [lambda r: ('Calculate the percentage reduction in water loss for the xerophyte.', f'{fx((a - b) / a * 100, 1)}%', f'({a} − {b}) ÷ {a} × 100 = {fx((a - b) / a * 100, 1)}% [2]'),
             lambda r: ('Describe three structural adaptations that could explain the difference.', 'Thick cuticle; sunken stomata; rolled leaves; hairs; fewer stomata; small leaves / spines.', '[3]'),
             lambda r: ('Explain how one of these adaptations reduces transpiration.', 'E.g. sunken stomata trap humid air, reducing the water potential gradient so less diffusion of water vapour.', '[2]'),
             lambda r: ('Suggest a disadvantage of these adaptations for the plant.', 'Less CO₂ uptake so slower photosynthesis / growth; less evaporative cooling.', '[1]'),
             lambda r: ('Describe how you could compare the water loss of the two plants in a laboratory.', 'Weigh potted plants (pots sealed in plastic) at intervals, or use a potometer; same conditions; calculate loss per unit leaf area.', '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe and explain the structural and physiological adaptations of xerophytic plants that reduce water loss.', 'Thick cuticle; sunken stomata; rolled leaves; hairs; fewer stomata; spines / small leaves; succulent storage; CAM / stomata at night; deep or widespread roots. Each explained by reduced ψ gradient or surface area.',
           'four adaptations [4]; explanation by water potential gradient [2] [6]')])
t7c = t

t = T('Translocation: mass flow of assimilates from source to sink and phloem loading', 'translocation')
facts(t, [('translocation', 'the movement of assimilates such as sucrose and amino acids through phloem from sources to sinks'), ('source', 'a part of a plant where assimilates are loaded into phloem, such as a photosynthesising leaf or a storage organ being mobilised'),
          ('sink', 'a part of a plant where assimilates are removed from phloem and used or stored, such as roots, fruits, buds and growing tips'), ('assimilates', 'substances made by the plant, such as sucrose and amino acids, that are transported in phloem'),
          ('mass flow', 'the movement of a fluid as a whole down a pressure gradient'), ('co-transporter protein', 'a membrane protein that moves two substances together, such as H⁺ and sucrose, in phloem loading')])
mcqs(t, [('Which part of a plant is a sink for sucrose?', 'A developing fruit', 'Sinks use or store assimilates.', ['A mature photosynthesising leaf', 'A storage tuber being mobilised in spring', 'A xylem vessel']),
         ('What creates the high hydrostatic pressure in sieve tubes at the source?', 'Water enters by osmosis after sucrose is loaded, lowering the water potential', 'Mass flow hypothesis.', ['Transpiration pull', 'Root pressure', 'Active transport of water']),
         ('How is sucrose loaded into companion cells?', 'By co-transport with H⁺ ions that were actively pumped out using ATP', 'Proton pump then H⁺–sucrose co-transporter.', ['By simple diffusion', 'By osmosis', 'By exocytosis'])])
shorts(t, [('State two differences between transport in xylem and transport in phloem.', 'Xylem: water and ions, upwards only, passive (tension), dead cells. Phloem: assimilates, up and down, active loading, living cells.', '[2]'),
           ('Name the main form in which carbohydrate is transported in phloem and give a reason.', 'Sucrose: soluble but relatively unreactive / not used by cells along the way.', '[2]')])
explain(t, [('Explain how sucrose is loaded into phloem sieve tubes.', 'Proton pumps in companion cell membranes use ATP to pump H⁺ out; H⁺ diffuses back in with sucrose through co-transporter proteins; sucrose passes into sieve tube via plasmodesmata (or directly).', '[4]'),
            ('Explain how mass flow moves sap from source to sink.', 'At the source sucrose is loaded, lowering ψ; water enters from xylem by osmosis, raising hydrostatic pressure; at the sink sucrose is removed, water leaves; sap flows down the pressure gradient from source to sink.', '[4]'),
            ('Explain why translocation requires energy even though mass flow itself is passive.', 'Loading of sucrose at the source (and sometimes unloading) uses ATP for proton pumps; this creates the pressure gradient.', '[2]')])
myths(t, [('Phloem only carries sugars downwards to the roots.', 'Phloem transports assimilates from source to sink in either direction.'), ('Sucrose moves through phloem by diffusion.', 'Sap moves by mass flow down a hydrostatic pressure gradient.')])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def transloc_rate(r, D):
    dist = r.choice([30, 45, 60, 80, 100, 120])
    tm = r.choice([0.5, 1, 1.5, 2, 3])
    rate = dist / tm
    if D == 1:
        return NQ(r, f'Radioactive sucrose moved {dist} cm through the phloem of a stem in {fx(tm, 1)} hours. What was the rate of translocation?', rate, [dist * tm, tm / dist * 100, rate / 60], ' cm h⁻¹', f'{dist} ÷ {fx(tm, 1)} = {fx(rate, 1)} cm h⁻¹.', f=lambda v: fx(v, 1))
    st = f'A leaf of a {r.choice(["bean", "willow", "sugar beet", "maize"])} plant was supplied with ¹⁴CO₂. Radioactive sucrose was detected in an aphid stylet {dist} cm below the leaf after {fx(tm * 60, 0)} minutes. (a) Calculate the rate of translocation in mm min⁻¹. (b) Explain how the ¹⁴C came to be in sucrose in the phloem. (c) Explain why aphid stylets are useful in investigating translocation.'
    rm = dist * 10 / (tm * 60)
    return Q(st, f'(a) {fx(rm, 2)} mm min⁻¹ (b) ¹⁴CO₂ was fixed in photosynthesis into sugars, converted to sucrose and loaded into phloem at the source. (c) The stylet penetrates a single sieve tube, so pure phloem sap can be collected and analysed (and pressure shown by sap exuding).',
             f'(a) {dist * 10} mm ÷ {fx(tm * 60, 0)} min = {fx(rm, 2)} [2] (b) photosynthesis [1]; loaded into phloem [1] (c) single sieve tube / pure sap [1] [5]', 'numerical', 5)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def ring_case(r, D):
    tree = r.choice(['an apple tree', 'a rubber tree', 'a willow', 'a mango tree'])
    intro = f'A farmer in {city(r)} removed a ring of bark (including the phloem) from the trunk of {tree}. After some weeks, the bark above the ring swelled and the roots began to die, but the leaves did not wilt.'
    parts = [lambda r: ('Explain why the bark above the ring swelled.', 'Sucrose from leaves (source) moving down in phloem accumulated above the ring; water entered by osmosis; cells grew.', '[2]'),
             lambda r: ('Explain why the roots eventually died.', 'Roots are sinks; no sucrose reached them for respiration, so no ATP for active uptake / growth.', '[2]'),
             lambda r: ('Explain why the leaves did not wilt.', 'Xylem (inside the phloem, in the wood) was intact, so water continued to move up.', '[2]'),
             lambda r: ('Describe the mass flow hypothesis for translocation.', 'Loading at source lowers ψ; water enters; high hydrostatic pressure; unloading at sink; flow down pressure gradient.', '[3]'),
             lambda r: ('Suggest one piece of evidence that does not fit the mass flow hypothesis.', 'Different solutes move at different rates / in different directions in the same sieve tube; sieve plates would resist flow.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how assimilates are transported from sources to sinks in a plant.', 'Sources and sinks defined with examples; sucrose made in mesophyll; proton pumps and co-transporters load companion cells and sieve tubes (ATP); low ψ, water enters by osmosis from xylem; high hydrostatic pressure; mass flow; unloading at sinks (diffusion / active), converted to starch or used; water returns to xylem.',
           'source / sink [1]; loading mechanism [2]; osmosis and pressure [2]; mass flow and unloading [2] [7]')])
t7d = t
CHAPTERS[7] = [t7a, t7b, t7c, t7d]


# ===================================================================== 8 Transport in mammals
VESS = {'artery': ('thick wall with much elastic tissue and smooth muscle; narrow lumen; no valves (except at the base of the aorta and pulmonary artery)', 'carries blood away from the heart at high pressure; elastic recoil smooths flow'),
        'vein': ('thin wall with little elastic tissue and muscle; wide lumen; valves', 'carries blood back to the heart at low pressure; valves prevent backflow'),
        'capillary': ('wall one cell thick (endothelium only), with gaps between cells; lumen about 7 μm, just wide enough for a red blood cell', 'allows exchange of substances between blood and tissue fluid over a short diffusion distance'),
        'arteriole': ('small artery with a relatively thick layer of smooth muscle', 'controls blood flow to capillary beds by vasoconstriction and vasodilation')}
t = T('Structure and function of arteries, veins and capillaries; tissue fluid formation', 'structure and function of arteries, veins and capillaries')
facts(t, [('tissue fluid', 'the fluid surrounding cells, formed from blood plasma that leaks out of capillaries, containing no red cells and few proteins'),
          ('hydrostatic pressure', 'the pressure exerted by a fluid; in capillaries it forces plasma out at the arterial end'),
          ('oncotic pressure', 'the tendency of water to move into the blood by osmosis because of plasma proteins (a lower water potential in plasma)'),
          ('lymph', 'tissue fluid that has drained into lymphatic vessels and is returned to the blood'), ('endothelium', 'the single layer of flattened cells lining all blood vessels'),
          ('double circulation', 'a circulation in which blood passes through the heart twice in each complete circuit: pulmonary and systemic')])


@t.add('C1', (1, 2, 3), 'mcq')
def vessel_id(r, D):
    v = r.choice(list(VESS))
    m = r.randrange(2)
    if m == 0:
        return MQ(r, f'Which blood vessel has this structure: {VESS[v][0]}?', cap(v), [cap(x) for x in VESS if x != v] + ['Venule'], f'{cap(v)}: {VESS[v][0]}.')
    return MQ(r, f'Which blood vessel has this function: it {VESS[v][1]}?', cap(v), [cap(x) for x in VESS if x != v] + ['Venule'], f'{cap(v)}: {VESS[v][1]}.')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def tissue_fluid(r, D):
    ha = round(r.uniform(3.8, 4.8), 1)
    hv = round(r.uniform(1.2, 2.0), 1)
    op = round(r.uniform(3.0, 3.5), 1)
    na, nv = ha - op, hv - op
    if D == 1:
        return NQ(r, f'At the arterial end of a capillary the hydrostatic pressure is {ha} kPa and the oncotic pressure (pulling water in) is {op} kPa. What is the net pressure forcing fluid out?', na, [ha + op, op - ha + 2 * (ha - op) + 0.5, ha], ' kPa', f'{ha} − {op} = {fx(na, 1)} kPa outwards.', f=lambda v: fx(v, 1))
    st = (f'In a capillary in the leg, the hydrostatic pressure is {ha} kPa at the arterial end and {hv} kPa at the venous end. The oncotic pressure due to plasma proteins is {op} kPa along the whole capillary. '
          f'(a) Calculate the net pressure at each end and state the direction of fluid movement. (b) Explain why the oncotic pressure stays almost the same along the capillary.')
    ans = f'(a) Arterial end: {fx(na, 1)} kPa outwards (fluid leaves); venous end: {fx(-nv, 1)} kPa inwards (fluid returns). (b) Plasma proteins are too large to pass through the capillary wall, so their concentration in the blood stays high.'
    key = f'(a) {ha} − {op} = {fx(na, 1)} kPa out [1]; {op} − {hv} = {fx(-nv, 1)} kPa in [1]; directions [1] (b) proteins too large to leave [1]'
    m = 4
    if D >= 3:
        st += ' (c) Explain why less fluid returns to the capillary than leaves it, and what happens to the excess.'
        ans += ' (c) The net inward pressure is smaller / acts over less time; the excess tissue fluid drains into lymph vessels and is returned to the blood.'
        key += ' (c) not all returns [1]; drains into lymph [1]'
        m += 2
    if D >= 5:
        st += ' (d) Suggest why a person with a low concentration of plasma proteins develops swelling (oedema).'
        ans += ' (d) Oncotic pressure is lower, so less water returns to the capillary at the venous end; tissue fluid accumulates.'
        key += ' (d) lower oncotic pressure / less reabsorption [1]; fluid accumulates [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4), 'short')
def vessel_compare(r, D):
    a, b = r.sample(['artery', 'vein', 'capillary'], 2)
    return Q(f'Compare the structure of an {a if a[0] in "aeiou" else a} and a {b}, and relate each difference to the function of the vessel.'.replace('a artery', 'an artery').replace('an capillary', 'a capillary').replace('an vein', 'a vein'),
             f'{cap(a)}: {VESS[a][0]}; it {VESS[a][1]}. {cap(b)}: {VESS[b][0]}; it {VESS[b][1]}.', 'three structural differences [3]; each linked to function [1] [4]', 'short', 4)


@t.add('C3', (1, 2, 3, 4), 'numerical')
def wall_ratio(r, D):
    v = r.choice([('artery', 1.2, 3.0), ('vein', 0.3, 0.6)])
    lum = round(r.uniform(2, 8), 1)
    wall = round(lum * r.uniform(v[1] / 4, v[1] / 2 if v[0] == 'artery' else v[2] / 4), 2)
    M = r.choice([10, 20, 40, 50])
    if D == 1:
        return NQ(r, f'In a micrograph at ×{M}, the wall of a blood vessel is {fx(wall * M, 1)} mm thick. What is the actual thickness?', wall, [wall * M * M, wall * 10, wall / 10], ' mm', f'{fx(wall * M, 1)} ÷ {M} = {fx(wall, 2)} mm.', f=lambda z: fx(z, 3))
    ratio = wall / lum
    st = f'A transverse section of a blood vessel viewed at ×{M} shows a lumen diameter of {fx(lum * M, 0)} mm and a wall thickness of {fx(wall * M, 1)} mm. (a) Calculate the actual lumen diameter and wall thickness. (b) Calculate the ratio of wall thickness to lumen diameter. (c) Suggest, with a reason, whether the vessel is an artery or a vein.'
    return Q(st, f'(a) lumen {fx(lum, 2)} mm; wall {fx(wall, 3)} mm (b) {fx(ratio, 2)} : 1 (c) {cap(v[0])}: ' + ('thick wall relative to lumen, to withstand high pressure.' if v[0] == 'artery' else 'thin wall relative to a wide lumen, as blood is at low pressure.'),
             f'(a) ÷ {M} for each [2] (b) {fx(wall, 3)} ÷ {fx(lum, 2)} = {fx(ratio, 2)} [1] (c) {v[0]} with reason [2] [5]', 'numerical', 5)


mcqs(t, [('Why do arteries have a large amount of elastic tissue in their walls?', 'To stretch and recoil, smoothing out pressure surges', 'Elastic recoil maintains pressure between beats.', ['To pump blood', 'To prevent backflow', 'To allow exchange of substances']),
         ('Which component of blood is normally absent from tissue fluid?', 'Red blood cells and large plasma proteins', 'Too large to pass through capillary walls.', ['Glucose', 'Oxygen', 'Water']),
         ('Which describes the mammalian circulation?', 'Closed and double', 'Blood in vessels; passes through heart twice per circuit.', ['Open and single', 'Closed and single', 'Open and double'])])
shorts(t, [('State three substances that pass from blood into tissue fluid at the arterial end of a capillary.', 'Water, glucose, amino acids, oxygen, ions, fatty acids, hormones.', '[2]'),
           ('State two functions of the lymphatic system.', 'Returns excess tissue fluid to the blood; transports fats from the gut; lymph nodes contain lymphocytes for immunity.', '[2]')])
explain(t, [('Explain how tissue fluid is formed and returned to the blood.', 'At arterial end hydrostatic pressure > oncotic pressure, so plasma (water and small solutes) forced out through gaps in capillary walls; at venous end hydrostatic pressure falls below oncotic pressure, so water returns by osmosis; excess drains into lymph.', '[4]'),
            ('Explain why the blood pressure falls as blood flows from arteries through capillaries to veins.', 'Friction with vessel walls and the large total cross-sectional area / resistance of arterioles and capillaries; fluid also leaves at capillaries.', '[2]'),
            ('Explain how the structure of a capillary is adapted for exchange.', 'Wall one cell thick (short diffusion distance); pores between cells; narrow lumen so red cells pass slowly and close to wall; extensive networks give large surface area.', '[3]')])
myths(t, [('Veins always carry deoxygenated blood.', 'The pulmonary vein carries oxygenated blood; veins are defined by carrying blood to the heart.'), ('Tissue fluid is the same as blood plasma.', 'Tissue fluid lacks red cells and most plasma proteins.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def oedema_case(r, D):
    cause, why = r.choice([('kwashiorkor (protein deficiency)', 'Fewer plasma proteins, so oncotic pressure is lower and less water returns to the capillary by osmosis at the venous end.'),
                           ('heart failure, which raises the pressure in veins', 'Hydrostatic pressure at the venous end of capillaries is higher, so less tissue fluid returns to the blood.'),
                           ('a blocked lymph vessel caused by the parasite that causes elephantiasis', 'Excess tissue fluid cannot drain into the lymph, so it accumulates.'),
                           ('long periods of sitting still on a flight', 'Leg muscles do not squeeze the veins, so venous pressure rises and less tissue fluid returns to the capillaries.')])
    intro = f'A doctor in {city(r)} sees a patient with swollen ankles (oedema) caused by {cause}.'
    parts = [lambda r: ('Describe how tissue fluid is normally formed.', 'High hydrostatic pressure at arterial end forces water and small solutes out through capillary walls; proteins and cells stay in blood.', '[3]'),
             lambda r: ('Explain how this cause leads to the build-up of tissue fluid.', why, '[2]'),
             lambda r: ('State the role of the lymphatic system.', 'Drains excess tissue fluid and returns it to the blood near the heart (subclavian veins).', '[2]'),
             lambda r: ('Explain how valves in veins help return blood to the heart.', 'Contraction of skeletal muscles squeezes veins; valves allow flow only towards the heart, preventing backflow.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structures of arteries, veins and capillaries and explain how tissue fluid is formed and returned.', 'Arteries: thick elastic / muscle walls, narrow lumen, high pressure. Veins: thin walls, wide lumen, valves. Capillaries: one-cell endothelium, exchange. Tissue fluid: hydrostatic vs oncotic pressure at arterial and venous ends; lymph.',
           'three vessels [3]; formation [2]; return / lymph [2] [7]')])
t8a = t

HILL = 2.7


def sat(p, p50):
    return 100 * p ** HILL / (p ** HILL + p50 ** HILL)


t = T('Red blood cells, haemoglobin and transport of oxygen and carbon dioxide; the Bohr shift', 'red blood cells')
facts(t, [('haemoglobin', 'the red pigment in red blood cells, a protein with four haem groups, each able to combine reversibly with one oxygen molecule'),
          ('oxyhaemoglobin', 'haemoglobin combined with oxygen'), ('partial pressure of oxygen (pO₂)', 'a measure of the concentration of oxygen in a mixture of gases or a solution, measured in kPa'),
          ('Bohr shift', 'the decrease in the affinity of haemoglobin for oxygen at high carbon dioxide concentrations, shifting the dissociation curve to the right'),
          ('carbonic anhydrase', 'the enzyme in red blood cells that catalyses the reaction of carbon dioxide with water to form carbonic acid'),
          ('chloride shift', 'the movement of chloride ions into red blood cells to balance the movement of hydrogencarbonate ions out'),
          ('carbaminohaemoglobin', 'the compound formed when carbon dioxide combines with amine groups of haemoglobin'), ('haemoglobinic acid', 'haemoglobin that has combined with hydrogen ions, acting as a buffer')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def dissoc(r, D):
    p50 = r.choice([3.4, 3.6, 3.8])
    p50b = p50 + r.choice([0.8, 1.0, 1.2])
    pl = r.choice([12, 13])
    pt = r.choice([5, 4, 3, 2])
    s1, s2, s2b = sat(pl, p50), sat(pt, p50), sat(pt, p50b)
    cap_ = r.choice([20, 19.5, 20.5])
    if D == 1:
        return NQ(r, f'Haemoglobin is {fx(s1, 0)}% saturated in the lungs and {fx(s2, 0)}% saturated in a respiring tissue. What percentage of the oxygen carried is released?', s1 - s2, [s2, 100 - s1, s1 + s2 - 100], '%', f'{fx(s1, 0)} − {fx(s2, 0)} = {fx(s1 - s2, 0)}%.', f=lambda v: fx(v, 0))
    pts = [1, 2, 3, 4, 5, 6, 8, 10, 12, 13]
    tab = ', '.join(f'{p} kPa: {fx(sat(p, p50), 0)}%' for p in pts)
    st = f'The table shows the percentage saturation of human haemoglobin with oxygen at different partial pressures of oxygen: {tab}. Fully saturated blood carries {fx(cap_, 1)} cm³ of oxygen per 100 cm³. (a) Using the data, calculate the volume of oxygen released per 100 cm³ of blood as it passes from the lungs (pO₂ {pl} kPa) to a tissue with pO₂ {fx(pt, 1)} kPa.'
    s1t, s2t = round(sat(pl, p50)), round(sat(pt, p50))
    v = (s1t - s2t) / 100 * cap_
    ans = f'(a) {fx(v, 2)} cm³'
    key = f'(a) saturation falls from {s1t}% to {s2t}% [1]; ({s1t} − {s2t}) ÷ 100 × {fx(cap_, 1)} = {fx(v, 2)} cm³ [1]'
    m = 2
    if D >= 3:
        s2bt = round(s2b)
        vb = (round(sat(pl, p50b)) - s2bt) / 100 * cap_
        st += f' (b) During exercise the carbon dioxide concentration in the tissue rises and the saturation at {fx(pt, 1)} kPa falls to {s2bt}%. Name this effect and calculate the extra oxygen released per 100 cm³ (assume the lung saturation is {round(sat(pl, p50b))}%).'
        ans += f' (b) The Bohr shift; extra = {fx(vb - v, 2)} cm³'
        key += f' (b) Bohr shift [1]; ({round(sat(pl, p50b))} − {s2bt}) ÷ 100 × {fx(cap_, 1)} = {fx(vb, 2)}; − {fx(v, 2)} = {fx(vb - v, 2)} cm³ [2]'
        m += 3
    if D >= 4:
        st += ' (c) Explain how a high carbon dioxide concentration causes haemoglobin to release more oxygen.'
        ans += ' (c) CO₂ diffuses into red cells and forms carbonic acid (carbonic anhydrase), which dissociates into H⁺ and HCO₃⁻; H⁺ binds to haemoglobin, forming haemoglobinic acid and changing its shape, lowering its affinity for oxygen.'
        key += ' (c) carbonic anhydrase / carbonic acid [1]; H⁺ released [1]; H⁺ binds Hb, lowers affinity [1]'
        m += 3
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


mcqs(t, [('Why is the oxygen dissociation curve of haemoglobin S-shaped (sigmoid)?', 'Binding of the first oxygen changes the shape of haemoglobin, making it easier for further oxygen molecules to bind', 'Cooperative binding.', ['Haemoglobin has only one haem group', 'Oxygen is very soluble in plasma', 'Carbon dioxide is released']),
         ('How is most carbon dioxide transported in the blood?', 'As hydrogencarbonate ions in the plasma', 'About 85% as HCO₃⁻; some as carbaminohaemoglobin; a little dissolved.', ['Dissolved in plasma', 'As carbaminohaemoglobin only', 'Bound to the haem iron']),
         ('Why does fetal haemoglobin have a dissociation curve to the left of adult haemoglobin?', 'It has a higher affinity for oxygen, so it can take oxygen from the mother\'s blood in the placenta', 'Higher affinity at the low pO₂ in the placenta.', ['It has a lower affinity for oxygen', 'It carries carbon dioxide instead', 'It has no haem groups']),
         ('Which feature of a red blood cell increases its surface area for gas exchange?', 'Its biconcave disc shape', 'Also no nucleus to make room for haemoglobin.', ['Having many mitochondria', 'Having a nucleus', 'Being 20 μm in diameter'])])
shorts(t, [('State two structural features of red blood cells and explain how each helps oxygen transport.', 'Biconcave shape: large SA:V for diffusion; no nucleus / mitochondria: more room for haemoglobin; small and flexible: pass through capillaries, short diffusion distance.', '[2]'),
           ('Write the equation for the reaction catalysed by carbonic anhydrase.', 'CO₂ + H₂O ⇌ H₂CO₃ (⇌ H⁺ + HCO₃⁻)', '[1]')])
explain(t, [('Explain the role of the chloride shift.', 'HCO₃⁻ formed inside red cells diffuses out into plasma; Cl⁻ moves in to maintain electrical neutrality (balance of charge).', '[2]'),
            ('Explain why the Bohr shift is advantageous during exercise.', 'Respiring muscles release more CO₂; haemoglobin releases more oxygen at the same pO₂ (lower affinity), supplying muscles with more O₂ for aerobic respiration.', '[3]'),
            ('Explain why carbon monoxide is dangerous.', 'It binds to haem far more strongly than oxygen (forming carboxyhaemoglobin), so less oxygen is carried; binding is almost irreversible.', '[2]'),
            ('Explain why people living at high altitude develop more red blood cells.', 'pO₂ is lower, so haemoglobin is less saturated; more red cells / haemoglobin increase oxygen-carrying capacity.', '[2]')])
myths(t, [('The Bohr shift means that haemoglobin binds more oxygen when carbon dioxide is high.', 'High CO₂ reduces the affinity of haemoglobin for oxygen, so more oxygen is released.'), ('Carbon dioxide is carried mainly by haemoglobin.', 'Most CO₂ is carried as hydrogencarbonate ions in the plasma.')])


@t.add('C4', (3, 4, 5), 'multi_step')
def hb_case(r, D):
    org = r.choice([('a llama living high in the Andes', 'left'), ('a fetus in the uterus', 'left'), ('a lugworm in low-oxygen mud', 'left'), ('a small mammal with a high metabolic rate, such as a shrew', 'right')])
    intro = f'Biologists in {city(r)} compared the oxygen dissociation curve of the haemoglobin of {org[0]} with that of adult human haemoglobin. The curve for {org[0]} lies to the {org[1]} of the human curve.'
    parts = [lambda r: ('Explain what this tells you about the affinity of this haemoglobin for oxygen.', 'Higher affinity (left) – more saturated at a given pO₂.' if org[1] == 'left' else 'Lower affinity (right) – releases oxygen more readily.', '[2]'),
             lambda r: ('Suggest why this is an advantage to the organism.', 'Can load oxygen at low pO₂ (high altitude / placenta / mud).' if org[1] == 'left' else 'Oxygen is unloaded more readily to tissues with a high respiration rate.', '[2]'),
             lambda r: ('Explain why the dissociation curve is sigmoid.', 'Cooperative binding: once one O₂ binds, Hb changes shape, making it easier for the next to bind; fourth binds less easily.', '[3]'),
             lambda r: ('Describe how carbon dioxide is transported from respiring tissues to the lungs.', 'Mostly as HCO₃⁻ in plasma (carbonic anhydrase in red cells, chloride shift); some as carbaminohaemoglobin; some dissolved.', '[3]'),
             lambda r: ('Explain the Bohr shift.', 'More CO₂ → more H⁺ → binds Hb → lower affinity → curve shifts right → more O₂ released where CO₂ is high.', '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how oxygen and carbon dioxide are transported in the blood and explain the significance of the Bohr shift.', 'Hb with 4 haem / Fe²⁺, binds 4 O₂ cooperatively, sigmoid curve, loading at high pO₂ in lungs and unloading in tissues. CO₂: dissolved, carbaminohaemoglobin, mostly HCO₃⁻ via carbonic anhydrase, chloride shift, H⁺ buffered by Hb. Bohr shift: high CO₂ lowers affinity, more O₂ released in active tissues.',
           'O₂ transport [2]; curve [1]; CO₂ transport [2]; Bohr shift and significance [2] [7]')])
t8b = t

t = T('The cardiac cycle and pressure changes in the heart', 'the cardiac cycle')
facts(t, [('cardiac cycle', 'the sequence of events in one heartbeat: atrial systole, ventricular systole and diastole'), ('systole', 'the contraction phase of the heart muscle'), ('diastole', 'the relaxation phase of the heart muscle'),
          ('atrioventricular valves', 'valves between the atria and ventricles (tricuspid and bicuspid/mitral) that prevent backflow into the atria when the ventricles contract'),
          ('semilunar valves', 'valves at the base of the aorta and pulmonary artery that prevent backflow into the ventricles'), ('cardiac output', 'the volume of blood pumped by one ventricle per minute (stroke volume × heart rate)'),
          ('stroke volume', 'the volume of blood pumped out of one ventricle in each heartbeat'), ('myogenic', 'describes heart muscle, which contracts without needing nerve impulses')])
mcqs(t, [('When do the atrioventricular valves close?', 'When the pressure in the ventricles rises above the pressure in the atria', 'At the start of ventricular systole.', ['When the pressure in the atria rises above the pressure in the ventricles', 'When pressure in the aorta exceeds that in the ventricle', 'During atrial systole']),
         ('When do the semilunar valves open?', 'When ventricular pressure exceeds the pressure in the arteries', 'Blood is then ejected into the aorta and pulmonary artery.', ['When atrial pressure exceeds ventricular pressure', 'At the start of diastole', 'When the atria contract']),
         ('Why is the wall of the left ventricle thicker than that of the right ventricle?', 'It must generate a higher pressure to pump blood around the whole body', 'Systemic circulation has a higher resistance than pulmonary.', ['It pumps a larger volume of blood', 'It receives blood from the lungs', 'It contains the SAN'])])
shorts(t, [('State the equation linking cardiac output, stroke volume and heart rate.', 'Cardiac output = stroke volume × heart rate.', '[1]'),
           ('Name the valves that prevent backflow of blood from the aorta into the left ventricle.', 'Semilunar (aortic) valves.', '[1]')])
explain(t, [('Describe the pressure changes and valve movements in the left side of the heart during one cardiac cycle.', 'Atrial systole: atrial pressure rises slightly, AV valve open, ventricle fills. Ventricular systole: ventricular pressure rises above atrial, AV valve closes; above aortic, semilunar valve opens, blood ejected. Diastole: ventricular pressure falls below aortic, semilunar valve closes; below atrial, AV valve opens.', '[5]'),
            ('Explain why the pressure in the aorta never falls to zero.', 'Elastic recoil of the aortic wall during diastole maintains pressure; semilunar valves prevent backflow.', '[2]'),
            ('Explain why the atrial walls are thinner than the ventricular walls.', 'Atria pump blood only into the ventricles, a short distance at low pressure.', '[2]')])
myths(t, [('Valves open and close because muscles pull on them.', 'Valves open and close because of pressure differences on either side.'), ('The right ventricle pumps less blood than the left because its wall is thinner.', 'Both ventricles pump the same volume; the left generates higher pressure.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def card_output(r, D):
    sv = r.choice([60, 65, 70, 75, 80, 90, 100, 110])
    cyc = r.choice([0.75, 0.8, 0.9, 1.0, 1.2])
    hr = 60 / cyc
    co = sv * hr / 1000
    p = person(r)
    if D == 1:
        return NQ(r, f'One cardiac cycle takes {cyc} s. What is the heart rate?', hr, [cyc * 60, 60 / cyc / 2, 100 * cyc], ' beats min⁻¹', f'60 ÷ {cyc} = {fx(hr, 0)} beats min⁻¹.', f=lambda v: fx(v, 0))
    st = f'{p}, an athlete in {city(r)}, has a resting cardiac cycle lasting {cyc} s and a resting stroke volume of {sv} cm³. (a) Calculate the heart rate. (b) Calculate the cardiac output in dm³ min⁻¹.'
    ans = f'(a) {fx(hr, 0)} beats min⁻¹ (b) {fx(co, 2)} dm³ min⁻¹'
    key = f'(a) 60 ÷ {cyc} = {fx(hr, 0)} [1] (b) {sv} × {fx(hr, 0)} = {fx(sv * hr, 0)} cm³ min⁻¹ [1]; ÷ 1000 = {fx(co, 2)} dm³ min⁻¹ [1]'
    m = 3
    if D >= 3:
        co2 = r.choice([20, 25, 30])
        hr2 = r.choice([170, 180, 190])
        st += f' (c) During maximal exercise the cardiac output rises to {co2} dm³ min⁻¹ at a heart rate of {hr2} beats min⁻¹. Calculate the stroke volume.'
        ans += f' (c) {fx(co2 * 1000 / hr2, 0)} cm³'
        key += f' (c) {co2} × 1000 ÷ {hr2} = {fx(co2 * 1000 / hr2, 0)} cm³ [2]'
        m += 2
    if D >= 4:
        st += ' (d) Explain why trained athletes usually have a lower resting heart rate than untrained people.'
        ans += ' (d) Training enlarges and strengthens the ventricles, increasing stroke volume, so the same cardiac output is achieved with fewer beats.'
        key += ' (d) larger stroke volume [1]; same output at lower rate [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4, 5), 'case')
def pressure_data(r, D):
    av = round(r.uniform(15.5, 17.5), 1)
    lv = round(r.uniform(16.5, 18.5), 1)
    if lv <= av:
        lv = av + 1.0
    t_ = r.choice([0.1, 0.15, 0.2])
    intro = (f'In a pressure trace from the left side of the heart of a person in {city(r)}, at {t_} s the ventricular pressure rises above the atrial pressure; at {fx(t_ + 0.05, 2)} s it rises above the aortic pressure (about 10.5 kPa); the ventricular pressure peaks at {lv} kPa and the aortic pressure peaks at {av} kPa; '
             f'at {fx(t_ + 0.35, 2)} s the ventricular pressure falls below the aortic pressure.')
    parts = [lambda r: (f'State what happens to the valves at {t_} s and at {fx(t_ + 0.05, 2)} s, and explain why.', f'At {t_} s the atrioventricular (bicuspid) valve closes because ventricular pressure exceeds atrial pressure; at {fx(t_ + 0.05, 2)} s the semilunar valve opens because ventricular pressure exceeds aortic pressure.', '[4]'),
             lambda r: ('Calculate the time during which blood is ejected into the aorta.', '0.3 s', f'{fx(t_ + 0.35, 2)} − {fx(t_ + 0.05, 2)} = 0.3 s [1]'),
             lambda r: ('Explain why the aortic pressure rises and falls less steeply than ventricular pressure.', 'Elastic tissue in the aorta stretches during systole and recoils in diastole, smoothing the pressure.', '[2]'),
             lambda r: ('Suggest how the trace for the right ventricle would differ.', 'Same timing / shape but much lower peak pressure (about a quarter), because the right ventricle has thinner walls and pumps to the lungs.', '[2]'),
             lambda r: ('State the name of the phase when both valves are closed and ventricular pressure is rising.', 'Isovolumetric (isovolumic) contraction, early ventricular systole.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


@t.add('C4', (3, 4, 5), 'multi_step')
def heart_case(r, D):
    cond = r.choice(['a leaking (incompetent) bicuspid valve', 'a narrowed (stenosed) aortic semilunar valve', 'a hole in the septum between the ventricles'])
    intro = f'A cardiologist in {city(r)} examines a patient with {cond}.'
    parts = [lambda r: ('Describe the normal sequence of events in one cardiac cycle.', 'Atrial systole (ventricles fill); ventricular systole (AV valves close, semilunar open, ejection); diastole (semilunar close, AV open, atria and ventricles fill).', '[3]'),
             lambda r: ('Explain how this condition reduces the efficiency of the heart.', {'l': 'Blood flows back into the left atrium during ventricular systole, so less blood is pumped into the aorta.', 'n': 'The ventricle must generate a higher pressure to eject blood through the narrow opening; less blood ejected; heart muscle thickens.', 'h': 'Oxygenated and deoxygenated blood mix; blood flows from left to right ventricle, reducing output to the body.'}[cond[2]], '[2]'),
             lambda r: ('Explain why the left ventricle wall is thicker than the right.', 'It pumps blood at higher pressure through the whole systemic circulation.', '[2]'),
             lambda r: ('The patient\'s stroke volume is 55 cm³ and heart rate 90 beats min⁻¹. Calculate cardiac output.', '4.95 dm³ min⁻¹', '55 × 90 = 4950 cm³ min⁻¹ = 4.95 dm³ min⁻¹ [2]'),
             lambda r: ('Explain why heart valves are needed.', 'To keep blood flowing in one direction / prevent backflow when pressure changes.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the cardiac cycle, explaining the pressure changes and the opening and closing of the valves.', 'Atrial systole; ventricular systole with AV closure and semilunar opening; diastole with semilunar closure and AV opening; pressures in atria, ventricles and aorta; elastic recoil; left vs right.',
           'atrial systole [1]; ventricular systole and valves [2]; diastole and valves [2]; pressure explanations [2] [7]')])
t8c = t

t = T('Control of the heartbeat: SAN, AVN and Purkyne tissue; interpreting ECGs', 'control of the heartbeat')
facts(t, [('sinoatrial node (SAN)', 'the pacemaker: a patch of muscle in the wall of the right atrium that initiates each heartbeat by sending out waves of excitation'),
          ('atrioventricular node (AVN)', 'a patch of tissue in the septum that delays the wave of excitation by about 0.1 s before passing it to the Purkyne tissue'),
          ('Purkyne tissue', 'specialised muscle fibres in the septum (bundle of His) and ventricle walls that conduct excitation rapidly to the base (apex) of the ventricles'),
          ('electrocardiogram (ECG)', 'a recording of the electrical activity of the heart detected by electrodes on the skin'), ('P wave', 'the part of an ECG that shows depolarisation of the atria'),
          ('QRS complex', 'the part of an ECG that shows depolarisation of the ventricles'), ('T wave', 'the part of an ECG that shows repolarisation of the ventricles'),
          ('atrioventricular septum', 'a band of non-conducting fibrous tissue that stops excitation spreading directly from atria to ventricles')])
mcqs(t, [('Why is there a delay of about 0.1 s at the AVN?', 'So that the atria finish contracting and the ventricles fill before they contract', 'Ensures atrial systole is complete.', ['To allow the SAN to recover', 'To let the semilunar valves open', 'To prevent the P wave']),
         ('Why do the ventricles contract from the base (apex) upwards?', 'Purkyne tissue carries excitation to the apex first, so blood is pushed up towards the arteries', 'Like squeezing a tube from the bottom.', ['The SAN is at the apex', 'The AVN is in the ventricle wall', 'The valves are at the apex']),
         ('Which part of an ECG represents ventricular depolarisation?', 'QRS complex', 'P = atria; QRS = ventricles; T = ventricular repolarisation.', ['P wave', 'T wave', 'PR interval'])])
shorts(t, [('State the meaning of the term myogenic.', 'Heart muscle contracts and relaxes without nervous stimulation; the beat starts within the muscle (SAN).', '[1]'),
           ('Describe the pathway of the wave of excitation through the heart.', 'SAN → across atria (atria contract) → AVN (delay) → bundle of His / Purkyne tissue in septum → apex → up ventricle walls.', '[3]')])
explain(t, [('Explain why the wave of excitation cannot pass directly from the atria to the ventricles.', 'A layer of non-conducting fibrous tissue separates them; excitation passes only through the AVN.', '[2]'),
            ('Explain how an ECG can show that a person has had a heart attack.', 'Damaged muscle conducts abnormally, giving changes such as an altered ST segment, abnormal QRS or arrhythmia.', '[2]'),
            ('Explain why an artificial pacemaker may be fitted to a patient whose SAN does not work properly.', 'It sends regular electrical impulses to the heart muscle, replacing the SAN, so the heart beats at a regular rate.', '[2]')])
myths(t, [('The heartbeat is started by impulses from the brain.', 'The heartbeat is myogenic, initiated by the SAN; the brain only changes the rate.'), ('The P wave shows the ventricles contracting.', 'The P wave shows atrial depolarisation; the QRS complex shows ventricular depolarisation.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ecg(r, D):
    speed = 25
    rr = r.choice([15, 18, 20, 22, 25, 30, 12, 10])
    hr = 60 * speed / rr
    if D == 1:
        return NQ(r, f'On an ECG recorded at 25 mm s⁻¹, the distance between two R peaks is {rr} mm. What is the heart rate?', hr, [rr * 60 / speed, hr / 2, speed * rr], ' beats min⁻¹', f'R–R time = {rr} ÷ 25 = {fx(rr / 25, 2)} s; 60 ÷ {fx(rr / 25, 2)} = {fx(hr, 0)}.', f=lambda v: fx(v, 0))
    pr = r.choice([3, 4, 5, 6])
    st = f'An ECG of a patient in {city(r)} was recorded on paper moving at 25 mm s⁻¹. The R–R interval was {rr} mm and the PR interval was {pr} mm. (a) Calculate the heart rate. (b) Calculate the PR interval in seconds and state what it represents.'
    ans = f'(a) {fx(hr, 0)} beats min⁻¹ (b) {fx(pr / 25, 2)} s; the time for excitation to spread from the SAN through the atria and the AVN delay to the ventricles.'
    key = f'(a) {rr} ÷ 25 = {fx(rr / 25, 2)} s [1]; 60 ÷ {fx(rr / 25, 2)} = {fx(hr, 0)} [1] (b) {pr} ÷ 25 = {fx(pr / 25, 2)} s [1]; atria to ventricles / AVN delay [1]'
    m = 4
    if D >= 3:
        st += ' (c) A normal resting rate is 60–100 beats min⁻¹. State whether this patient\'s rate is normal, slow (bradycardia) or fast (tachycardia).'
        ans += ' (c) ' + ('Fast (tachycardia).' if hr > 100 else ('Slow (bradycardia).' if hr < 60 else 'Normal.'))
        key += ' (c) correct category [1]'
        m += 1
    if D >= 4:
        st += ' (d) Explain what the QRS complex and T wave represent.'
        ans += ' (d) QRS: depolarisation of the ventricles (just before ventricular systole); T: repolarisation of the ventricles.'
        key += ' (d) QRS [1]; T [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def ecg_case(r, D):
    prob = r.choice([('the PR interval is much longer than normal', 'delay at the AVN is prolonged (heart block)'), ('there are P waves with no QRS complex after some of them', 'some impulses from the atria do not reach the ventricles (heart block)'),
                     ('there are no clear P waves and the QRS complexes are irregular', 'atria are not contracting in a coordinated way (atrial fibrillation)'), ('the QRS complexes are wide and irregular and very rapid', 'ventricles are contracting abnormally (ventricular fibrillation)')])
    intro = f'A doctor in {city(r)} studies the ECG of a patient and notices that {prob[0]}.'
    parts = [lambda r: ('Suggest what is happening in the patient\'s heart.', cap(prob[1]) + '.', '[2]'),
             lambda r: ('Describe how a heartbeat is normally initiated and coordinated.', 'SAN in right atrium sends wave of excitation over atria (contract); non-conducting tissue; AVN delays; Purkyne tissue in septum to apex; ventricles contract from base upwards.', '[4]'),
             lambda r: ('Explain the importance of the delay at the AVN.', 'Atria finish contracting and ventricles fill fully before ventricular systole.', '[2]'),
             lambda r: ('Explain what the P wave, QRS complex and T wave of a normal ECG represent.', 'P: atrial depolarisation; QRS: ventricular depolarisation; T: ventricular repolarisation.', '[3]'),
             lambda r: ('Suggest a treatment, giving a reason.', 'An artificial pacemaker / defibrillation to restore a regular coordinated rhythm.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how the heartbeat is initiated and controlled, and how an ECG is used to show the electrical activity of the heart.', 'Myogenic; SAN pacemaker; wave across atria; non-conducting layer; AVN delay; Purkyne tissue / bundle of His; apex upwards. ECG: P atria, QRS ventricles, T repolarisation; heart rate from R–R; abnormalities.',
           'SAN [1]; atria / AVN delay [2]; Purkyne [1]; ECG features [2]; use [1] [7]')])
t8d = t
CHAPTERS[8] = [t8a, t8b, t8c, t8d]


# ===================================================================== 9 Gas exchange
AIRWAY = {'trachea': {'cartilage': 'C-shaped rings', 'ciliated epithelium': 'present', 'goblet cells': 'present', 'smooth muscle': 'present', 'elastic fibres': 'present'},
          'bronchus': {'cartilage': 'irregular plates', 'ciliated epithelium': 'present', 'goblet cells': 'present', 'smooth muscle': 'present', 'elastic fibres': 'present'},
          'bronchiole': {'cartilage': 'absent', 'ciliated epithelium': 'present (in larger bronchioles)', 'goblet cells': 'few or absent', 'smooth muscle': 'present', 'elastic fibres': 'present'},
          'alveolus': {'cartilage': 'absent', 'ciliated epithelium': 'absent (squamous epithelium)', 'goblet cells': 'absent', 'smooth muscle': 'absent', 'elastic fibres': 'present'}}
t = T('Structure of the gas exchange system: trachea, bronchi, bronchioles and alveoli; tissues present', 'structure of the gas exchange system')
facts(t, [('cartilage', 'a firm, flexible tissue that supports the trachea and bronchi and keeps them open'), ('smooth muscle', 'involuntary muscle in the walls of airways that contracts to narrow them'),
          ('elastic fibres', 'fibres of elastin that stretch during inspiration and recoil during expiration'), ('squamous epithelium', 'a layer of thin, flat cells forming the walls of alveoli and capillaries'),
          ('bronchiole', 'a small airway with no cartilage, whose diameter is controlled by smooth muscle'), ('alveolus', 'a tiny air sac with walls of squamous epithelium, the site of gas exchange')])


@t.add('C1', (1, 2, 3), 'mcq')
def airway_q(r, D):
    tis = r.choice(['cartilage', 'goblet cells', 'smooth muscle', 'ciliated epithelium'])
    if tis == 'cartilage':
        return MQ(r, 'In which part of the gas exchange system is cartilage present as C-shaped rings?', 'Trachea', ['Bronchiole', 'Alveolus', 'Bronchus', 'Capillary'], 'Trachea: C-shaped rings; bronchi: irregular plates; none in bronchioles.')
    if tis == 'goblet cells':
        return MQ(r, 'Which region of the gas exchange system has no goblet cells, cilia or smooth muscle, but does have elastic fibres?', 'Alveolus', ['Trachea', 'Bronchus', 'Bronchiole'], 'Alveolar walls: squamous epithelium and elastic fibres.')
    if tis == 'smooth muscle':
        return MQ(r, 'Which airway has smooth muscle and elastic fibres but no cartilage?', 'Bronchiole', ['Trachea', 'Bronchus', 'Alveolus'], 'Bronchioles lack cartilage; smooth muscle controls diameter.')
    return MQ(r, 'Which tissue is found in the trachea, bronchi and larger bronchioles but not in alveoli?', 'Ciliated epithelium', ['Elastic fibres', 'Squamous epithelium', 'Capillary endothelium'], 'Alveoli are lined by squamous epithelium.')


@t.add('C3', (2, 3, 4), 'short')
def airway_id(r, D):
    reg = r.choice(list(AIRWAY))
    feats = AIRWAY[reg]
    keys = r.sample(list(feats), 3 if D <= 3 else 4)
    desc = '; '.join(f'{k}: {feats[k]}' for k in keys)
    st = f'A student in {city(r)} examined a section of lung tissue and recorded: {desc}. Identify the region of the gas exchange system and give two reasons.'
    return Q(st, f'{cap(reg)}: ' + '; '.join(f'{k} {feats[k]}' for k in keys[:2]) + '.', f'{reg} [1]; two reasons from the observations [2] [3]', 'short', 3)


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def gx_mag(r, D):
    return mag_item(r, D, [('the wall of an alveolus (thickness)', 0.2, 0.6), ('an alveolus (diameter)', 200, 300), ('a goblet cell (length)', 20, 40), ('a cilium (length)', 5, 10), ('a bronchiole (diameter)', 300, 1000),
                           ('a ciliated epithelial cell (height)', 25, 50), ('a capillary (diameter)', 6, 9)])


mcqs(t, [('What is the function of the smooth muscle in bronchioles?', 'To contract and narrow the airway, controlling air flow', 'Constriction during an asthma attack is caused by smooth muscle.', ['To keep the airway open', 'To produce mucus', 'To carry out gas exchange']),
         ('Why is cartilage absent from bronchioles?', 'They are small enough to stay open without it, and this allows their diameter to change', 'Smooth muscle changes their diameter.', ['They have elastic fibres instead of epithelium', 'They are part of the alveoli', 'Cartilage would block gas exchange'])])
shorts(t, [('State the function of the elastic fibres in the alveolar walls.', 'They stretch during inspiration and recoil during expiration, helping to push air out; prevent alveoli bursting.', '[2]'),
           ('Name the tissues found in the wall of the trachea.', 'Cartilage, ciliated epithelium, goblet cells, smooth muscle, elastic fibres (glands, connective tissue).', '[3]')])
explain(t, [('Explain why the trachea is supported by C-shaped rings of cartilage rather than complete rings.', 'Cartilage prevents collapse when pressure falls during inspiration; the gap allows the oesophagus to expand when food is swallowed and lets the trachea flex.', '[2]'),
            ('Explain how the distribution of cartilage, smooth muscle and elastic fibres changes from trachea to alveoli.', 'Cartilage decreases (rings → plates → none); smooth muscle present to bronchioles, absent in alveoli; elastic fibres throughout.', '[3]'),
            ('Explain why an asthma attack makes breathing difficult.', 'Smooth muscle in bronchioles contracts and the lining becomes inflamed with extra mucus, narrowing the airways and increasing resistance to air flow.', '[2]')])
myths(t, [('Gas exchange takes place across the walls of the bronchioles.', 'Gas exchange happens across alveolar walls.'), ('All airways contain cartilage to keep them open.', 'Bronchioles have no cartilage; their diameter is controlled by smooth muscle.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def airway_case(r, D):
    intro = f'{person(r)}, a student in {city(r)}, examined prepared slides of transverse sections of the trachea, a bronchiole and alveolar tissue with a light microscope.'
    parts = [lambda r: ('Describe two differences you would expect between the trachea and a bronchiole.', 'Trachea has C-shaped cartilage rings and many goblet cells; bronchiole has no cartilage, more smooth muscle relative to size, few goblet cells.', '[2]'),
             lambda r: ('Explain how the structure of the alveolar wall is related to its function.', 'Squamous epithelium one cell thick – short diffusion distance; elastic fibres for recoil; close contact with capillaries.', '[3]'),
             lambda r: ('An alveolus has an image diameter of 50 mm at ×200. Calculate its actual diameter in μm.', '250 μm', '50 mm = 50 000 μm; ÷ 200 = 250 μm [2]'),
             lambda r: ('Suggest why the slides are stained.', 'To increase contrast so different tissues / cells are distinguished.', '[1]'),
             lambda r: ('State the function of goblet cells and cilia.', 'Goblet cells secrete mucus that traps particles; cilia beat to move mucus up to the throat.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the distribution and functions of cartilage, ciliated epithelium, goblet cells, smooth muscle and elastic fibres in the gas exchange system.', 'Cartilage: trachea rings, bronchi plates, keeps airways open. Ciliated epithelium and goblet cells: trachea to bronchioles, mucus escalator. Smooth muscle: trachea to bronchioles, controls diameter. Elastic fibres: throughout, recoil.',
           'cartilage [2]; cilia / goblet [2]; smooth muscle [1]; elastic fibres [1] [6]')])
t9a = t

t = T('Gas exchange at alveoli and adaptations for efficient diffusion', 'gas exchange at alveoli')
facts(t, [('gas exchange', 'the diffusion of oxygen from alveolar air into the blood and of carbon dioxide from the blood into the alveolar air'),
          ('ventilation', 'the movement of air into and out of the lungs, which maintains a steep concentration gradient in the alveoli'),
          ('surfactant', 'a phospholipid secretion that reduces surface tension in alveoli, preventing them from collapsing'),
          ('tidal volume', 'the volume of air breathed in or out in a normal breath, about 0.5 dm³ at rest'), ('diffusion distance', 'the distance gases must diffuse, about 0.5–1 μm from alveolar air to the red blood cell')])
mcqs(t, [('Which feature of the alveoli maintains a steep concentration gradient for oxygen?', 'Continuous ventilation and blood flow', 'Removing O₂-rich blood and bringing fresh air keeps the gradient steep.', ['Elastic fibres', 'Surfactant', 'Cartilage']),
         ('What is the approximate total surface area of the alveoli in an adult human?', '70 m²', 'About 300–700 million alveoli give 70 m².', ['0.7 m²', '7000 m²', '7 cm²'])])
shorts(t, [('State four features of the alveoli that make gas exchange efficient.', 'Large surface area; thin walls (one cell, short distance); good blood supply (capillary network); ventilation; moist surface; elastic fibres.', '[2]'),
           ('State why red blood cells are squeezed against capillary walls in the lungs.', 'The capillary lumen is narrow, so the diffusion distance is shorter and the cells move slowly.', '[1]')])
explain(t, [('Explain how the structure of the alveoli and capillaries gives a short diffusion distance.', 'Alveolar wall and capillary wall are each one squamous cell thick; capillaries are in close contact with alveoli; narrow capillaries press red cells against the wall.', '[3]'),
            ('Explain how ventilation and blood flow maintain a steep concentration gradient.', 'Breathing brings fresh air high in O₂ and removes CO₂; blood flow carries O₂ away and brings CO₂, so the gradients are maintained.', '[2]'),
            ('Explain why emphysema reduces the efficiency of gas exchange.', 'Alveolar walls break down, reducing surface area; loss of elastic fibres reduces recoil and ventilation.', '[2]')])
myths(t, [('Oxygen is actively transported into the blood in the lungs.', 'Oxygen diffuses passively down its concentration gradient.'), ('Alveoli are lined with ciliated epithelium.', 'Alveoli have squamous epithelium; cilia are in the airways.')])
relation(t, 'C2', (2, 3, 4), "Fick's law: rate ∝ (surface area × concentration difference) ÷ diffusion distance", 'rate of diffusion of oxygen into the blood',
         {'surface area': 1, 'concentration difference': 1, 'diffusion distance': -1},
         ['In the lungs of a patient, gas exchange is studied.', 'A climber ascends to high altitude.', 'A patient with fibrosis has thickened alveolar walls.', 'An athlete exercises hard and breathes deeply.'])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ventilation(r, D):
    tv = r.choice([0.4, 0.45, 0.5, 0.55, 0.6])
    br = r.choice([12, 14, 15, 16, 18])
    pv = tv * br
    if D == 1:
        return NQ(r, f'A person breathes {br} times per minute with a tidal volume of {tv} dm³. What is the pulmonary ventilation rate?', pv, [tv + br, br / tv, pv * 60], ' dm³ min⁻¹', f'{tv} × {br} = {fx(pv, 2)} dm³ min⁻¹.', f=lambda v: fx(v, 2))
    tv2 = r.choice([1.5, 2.0, 2.5, 3.0])
    br2 = r.choice([30, 35, 40, 45])
    st = f'At rest, {person(r)} has a tidal volume of {tv} dm³ and a breathing rate of {br} breaths min⁻¹. During exercise these become {tv2} dm³ and {br2} breaths min⁻¹. (a) Calculate the ventilation rate at rest and during exercise. (b) Calculate the percentage increase.'
    pv2 = tv2 * br2
    ans = f'(a) rest {fx(pv, 2)} dm³ min⁻¹; exercise {fx(pv2, 2)} dm³ min⁻¹ (b) {fx((pv2 - pv) / pv * 100, 0)}%'
    key = f'(a) {tv} × {br} = {fx(pv, 2)} [1]; {tv2} × {br2} = {fx(pv2, 2)} [1] (b) ({fx(pv2, 2)} − {fx(pv, 2)}) ÷ {fx(pv, 2)} × 100 = {fx((pv2 - pv) / pv * 100, 0)}% [2]'
    m = 4
    if D >= 3:
        st += ' (c) Explain why ventilation increases during exercise.'
        ans += ' (c) Muscles respire faster, producing more CO₂ and using more O₂; increased ventilation maintains steep concentration gradients at the alveoli so more O₂ diffuses in and CO₂ out.'
        key += ' (c) more respiration [1]; maintains gradients [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4, 5), 'case')
def alv_data(r, D):
    sa1 = r.choice([60, 70, 80])
    sa2 = round(sa1 * r.uniform(0.3, 0.55))
    th1 = r.choice([0.5, 0.6])
    th2 = round(th1 * r.uniform(2, 4), 1)
    cond = r.choice(['emphysema', 'pulmonary fibrosis'])
    intro = f'A study in {city(r)} compared healthy lungs with lungs affected by {cond}. Healthy: alveolar surface area {sa1} m², diffusion distance {th1} μm. Affected: surface area {sa2} m², diffusion distance {th2} μm.'
    f = (sa2 / sa1) * (th1 / th2)
    parts = [lambda r: ('Calculate the percentage decrease in surface area.', f'{fx((sa1 - sa2) / sa1 * 100, 1)}%', f'({sa1} − {sa2}) ÷ {sa1} × 100 = {fx((sa1 - sa2) / sa1 * 100, 1)}% [2]'),
             lambda r: ("Using Fick's law, estimate the rate of diffusion in the affected lung as a fraction of the healthy rate (assume the same concentration difference).", f'{fx(f, 3)} (about {fx(f * 100, 0)}%)', f'({sa2} ÷ {sa1}) × ({th1} ÷ {th2}) [1] = {fx(f, 3)} [1] [2]'),
             lambda r: ('Explain why the patient becomes breathless on mild exertion.', 'Less oxygen diffuses into the blood per minute, so less is supplied to muscles for aerobic respiration; breathing rate rises to compensate.', '[2]'),
             lambda r: ('Describe how the structure of healthy alveoli is adapted for gas exchange.', 'Large surface area; walls one cell thick; capillary network; elastic fibres; surfactant; moist.', '[3]'),
             lambda r: (f'Suggest a cause of {cond}.', 'Smoking (tar and chemicals causing inflammation, phagocyte enzymes destroying elastin).' if cond == 'emphysema' else 'Inhaling dust / fibres (e.g. asbestos), or scarring after infection.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


@t.add('C4', (3, 4, 5), 'multi_step')
def altitude_case(r, D):
    alt = r.choice([3500, 4500, 5000, 5500])
    po = round(21 * math.exp(-alt / 8000), 1)
    intro = f'A mountaineer climbs to {alt:,} m in the Himalayas, where the partial pressure of oxygen in the air is about {po} kPa compared with 21 kPa at sea level.'
    parts = [lambda r: ('Calculate the percentage reduction in the partial pressure of oxygen.', f'{fx((21 - po) / 21 * 100, 1)}%', f'(21 − {po}) ÷ 21 × 100 = {fx((21 - po) / 21 * 100, 1)}% [2]'),
             lambda r: ('Explain why less oxygen diffuses into the blood at this altitude.', 'Lower pO₂ in alveoli gives a smaller concentration gradient between air and blood, so the rate of diffusion falls.', '[2]'),
             lambda r: ('Explain how the alveoli are adapted for rapid diffusion.', 'Large surface area; thin squamous epithelium; dense capillaries; ventilation; moist lining.', '[3]'),
             lambda r: ('Suggest two ways in which the body adjusts after several weeks at altitude.', 'More red blood cells / haemoglobin; deeper and faster breathing; more capillaries; more myoglobin / mitochondria.', '[2]'),
             lambda r: ('Explain why haemoglobin is less saturated with oxygen at high altitude.', 'At lower pO₂, haemoglobin is lower on the dissociation curve (lower saturation).', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how the alveoli and their blood supply are adapted for efficient gas exchange.', 'Many alveoli → large SA; squamous epithelium and capillary endothelium → short distance; ventilation and blood flow → steep gradients; moist lining; surfactant; elastic fibres; red cells squeezed against wall; Fick\'s law.',
           'surface area [1]; distance [2]; gradients [2]; other feature [1] [6]')])
t9b = t

t = T('Ciliated epithelium, goblet cells and mucus in protecting the airways', 'ciliated epithelium')
facts(t, [('goblet cell', 'a cell in the epithelium of the airways that secretes mucus'), ('mucus', 'a sticky secretion containing glycoproteins (mucins) that traps dust, pollen and pathogens'),
          ('cilia', 'hair-like structures on epithelial cells that beat in a coordinated way to move mucus towards the throat'), ('mucus escalator', 'the continuous movement of mucus with trapped particles up the airways by cilia, to be swallowed'),
          ('mucous glands', 'glands in the submucosa of the trachea and bronchi that secrete mucus')])
mcqs(t, [('What is the function of the cilia in the trachea?', 'To move mucus with trapped particles up towards the throat', 'Mucus escalator.', ['To absorb oxygen', 'To trap particles directly', 'To produce mucus']),
         ('Which effect does tobacco smoke have on the airways?', 'It paralyses cilia and increases mucus production', 'Mucus accumulates, leading to coughing and infection.', ['It increases the number of cilia', 'It dissolves mucus', 'It strengthens cartilage'])])
shorts(t, [('State two substances or particles trapped by mucus.', 'Dust; pollen; bacteria; viruses; spores.', '[2]'),
           ('State why ciliated cells contain many mitochondria.', 'To provide ATP for the beating of cilia.', '[1]')])
explain(t, [('Explain how the mucus escalator protects the lungs.', 'Goblet cells secrete mucus that traps pathogens and particles; cilia beat to move mucus up to the throat, where it is swallowed, so particles do not reach the alveoli.', '[3]'),
            ('Explain why people who smoke develop a "smoker\'s cough".', 'Smoke paralyses / destroys cilia and increases mucus secretion; mucus accumulates and can only be removed by coughing.', '[2]'),
            ('Explain why people with cystic fibrosis get frequent lung infections.', 'Their mucus is very thick and sticky, so cilia cannot move it; bacteria trapped in mucus multiply.', '[2]')])
myths(t, [('Cilia trap pathogens.', 'Mucus traps pathogens; cilia move the mucus.'), ('Goblet cells are found in the alveoli.', 'Goblet cells are in the trachea, bronchi and larger bronchioles, not alveoli.')])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def mucus_speed(r, D):
    sp = r.choice([4, 5, 6, 8, 10, 12])
    dist = r.choice([10, 12, 15])
    if D == 1:
        return NQ(r, f'Mucus moves up the trachea at {sp} mm min⁻¹. How long does it take to move {dist} cm?', dist * 10 / sp, [dist / sp, sp * dist, dist * 10 * sp / 60], ' min', f'{dist * 10} mm ÷ {sp} = {fx(dist * 10 / sp, 1)} min.', f=lambda v: fx(v, 1))
    sp2 = round(sp * r.uniform(0.2, 0.5), 1)
    st = f'In a healthy person in {city(r)}, mucus moves up the trachea at {sp} mm min⁻¹. In a long-term smoker the rate is {sp2} mm min⁻¹. The trachea is {dist} cm long. (a) Calculate the time taken for mucus to travel the length of the trachea in each person. (b) Explain the difference and suggest one consequence for the smoker.'
    return Q(st, f'(a) healthy {fx(dist * 10 / sp, 1)} min; smoker {fx(dist * 10 / sp2, 1)} min (b) Smoke paralyses / destroys cilia (and increases mucus), so mucus moves more slowly; pathogens remain longer in the airways, increasing infections (bronchitis) and coughing.',
             f'(a) {dist * 10} ÷ {sp} = {fx(dist * 10 / sp, 1)} [1]; {dist * 10} ÷ {sp2} = {fx(dist * 10 / sp2, 1)} [1] (b) cilia damaged [1]; consequence [1] [4]', 'numerical', 4)


@t.add('C3', (2, 3, 4), 'short')
def cilia_apply(r, D):
    sc = r.choice([('a person working in a dusty cement factory', 'more mucus is produced to trap dust; cilia may become overloaded'), ('a child with cystic fibrosis', 'thick, sticky mucus cannot be moved by cilia, so bacteria remain and infections are frequent'),
                   ('a smoker of 20 cigarettes a day', 'tar paralyses cilia and goblet cells increase, so mucus accumulates and must be coughed up'), ('a person with a cold caused by a virus', 'more mucus is secreted to trap viruses; cilia move it up and out')])
    return Q(f'Explain how the mucus and cilia of the airways are affected in {sc[0]}, and the consequence for that person.', cap(sc[1]) + '.', 'effect on mucus / cilia [1]; consequence [1] [2]', 'short', 2)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def smoking_case(r, D):
    n = r.choice([10, 15, 20, 30])
    yrs = r.choice([10, 15, 20, 25])
    intro = f'A patient in {city(r)} has smoked {n} cigarettes a day for {yrs} years and now has chronic bronchitis.'
    parts = [lambda r: ('Calculate the total number of cigarettes smoked (assume 365 days per year).', f'{n * 365 * yrs:,}', f'{n} × 365 × {yrs} = {n * 365 * yrs:,} [1]'),
             lambda r: ('Describe the normal roles of goblet cells and cilia.', 'Goblet cells secrete mucus that traps particles and pathogens; cilia beat to move mucus up to the throat.', '[2]'),
             lambda r: ('Explain how smoking leads to chronic bronchitis.', 'Tar paralyses / destroys cilia; goblet cells and mucous glands enlarge and produce more mucus; mucus accumulates and bacteria multiply; inflammation; airways narrow; persistent cough.', '[3]'),
             lambda r: ('Suggest why the patient is at greater risk of lung infections.', 'Pathogens trapped in mucus are not removed and can multiply.', '[1]'),
             lambda r: ('Explain why the patient becomes short of breath.', 'Mucus and inflammation narrow the airways, so less air reaches alveoli; reduced ventilation and gas exchange.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how the airways are protected by ciliated epithelium, goblet cells and mucus, and explain how smoking affects this protection.', 'Goblet cells and glands secrete mucus (mucins) that traps dust and pathogens; cilia beat in coordinated waves moving mucus up to the throat (mucus escalator); swallowed. Smoking: tar paralyses / destroys cilia, more goblet cells, mucus accumulates, infection, bronchitis, coughing.',
           'mucus [1]; goblet cells [1]; cilia / escalator [2]; effects of smoking [2] [6]')])
t9c = t
CHAPTERS[9] = [t9a, t9b, t9c]


# ===================================================================== 10 Infectious diseases
DIS = {'cholera': ('Vibrio cholerae', 'bacterium', 'drinking water or eating food contaminated with faeces from infected people', 'severe watery diarrhoea and dehydration, caused by a toxin acting on the intestine'),
       'malaria': ('Plasmodium falciparum (and other Plasmodium species)', 'protoctist', 'bites of infected female Anopheles mosquitoes (the vector); also blood transfusion and from mother to fetus', 'fever, chills and anaemia as the parasite destroys red blood cells'),
       'tuberculosis (TB)': ('Mycobacterium tuberculosis (and M. bovis)', 'bacterium', 'droplets in the air from coughs and sneezes of infected people; M. bovis via unpasteurised milk', 'persistent cough, weight loss and damage to lung tissue'),
       'HIV/AIDS': ('human immunodeficiency virus (HIV)', 'virus', 'exchange of body fluids: unprotected sex, sharing needles, infected blood products, mother to child across the placenta, at birth or in breast milk', 'destruction of T helper cells, leading to AIDS and opportunistic infections'),
       'measles': ('measles virus (a morbillivirus)', 'virus', 'droplets in the air from coughs and sneezes of infected people; highly infectious', 'fever, rash and risk of complications such as pneumonia, especially in malnourished children')}
t = T('Causes and transmission of cholera, malaria, tuberculosis, HIV/AIDS and measles', 'causes and transmission')
facts(t, [('infectious disease', 'a disease caused by a pathogen that can be passed from one person to another'), ('pathogen', 'an organism that causes disease, such as a bacterium, virus, fungus or protoctist'),
          ('vector', 'an organism that carries a pathogen from one host to another, such as the Anopheles mosquito for malaria'), ('transmission', 'the passing of a pathogen from one host to another'),
          ('endemic', 'describes a disease that is always present in a population'), ('incidence', 'the number of new cases of a disease per unit of population in a given time'), ('prevalence', 'the number of people with a disease at a particular time in a population')])


@t.add('C1', (1, 2, 3), 'mcq')
def dis_q(r, D):
    d = r.choice(list(DIS))
    m = r.randrange(3)
    if m == 0:
        return MQ(r, f'Which pathogen causes {d}?', cap(DIS[d][0]), [cap(DIS[x][0]) for x in DIS if x != d], f'{cap(d)}: {DIS[d][0]} ({DIS[d][1]}).')
    if m == 1:
        return MQ(r, f'How is {d} transmitted?', cap(DIS[d][2]) + '.', [cap(DIS[x][2]) + '.' for x in DIS if x != d and DIS[x][2] != DIS[d][2]], f'{cap(d)}: {DIS[d][2]}.')
    return MQ(r, f'Which type of organism is the pathogen that causes {d}?', cap(DIS[d][1]), [x for x in ['Bacterium', 'Virus', 'Protoctist', 'Fungus'] if x.lower() != DIS[d][1]], f'{cap(d)}: {DIS[d][0]} is a {DIS[d][1]}.')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def incidence(r, D):
    d = r.choice(list(DIS))
    pop = r.choice([250000, 800000, 1200000, 2500000, 5000000])
    c1 = r.randint(80, 2000)
    c2 = round(c1 * r.uniform(0.3, 1.8))
    yr = r.choice([2015, 2018, 2020])
    inc1, inc2 = c1 / pop * 100000, c2 / pop * 100000
    if D == 1:
        return NQ(r, f'A district with a population of {pop:,} recorded {c1:,} new cases of {d} in one year. What is the incidence per 100 000 people?', inc1, [c1 / pop * 1000, c1 / pop * 100, inc1 * 10], '', f'{c1:,} ÷ {pop:,} × 100 000 = {fx(inc1, 1)}.', f=lambda v: fx(v, 1))
    st = f'A health ministry recorded {c1:,} new cases of {d} in {yr} and {c2:,} in {yr + 4} in a region with a population of {pop:,} (assume constant). (a) Calculate the incidence per 100 000 people in each year. (b) Calculate the percentage change in incidence.'
    ch = (c2 - c1) / c1 * 100
    ans = f'(a) {fx(inc1, 1)} and {fx(inc2, 1)} per 100 000 (b) {mn(fx(ch, 1))}% (' + ('a decrease)' if ch < 0 else 'an increase)')
    key = f'(a) {c1:,} ÷ {pop:,} × 100 000 = {fx(inc1, 1)} [1]; {fx(inc2, 1)} [1] (b) ({c2:,} − {c1:,}) ÷ {c1:,} × 100 = {mn(fx(ch, 1))}% [2]'
    m = 4
    if D >= 3:
        st += f' (c) Describe how {d} is transmitted and suggest one reason for the change.'
        ans += f' (c) {cap(DIS[d][2])}. ' + (f'Possible reason for the fall: better control, e.g. {CTRL[d][0]}.' if c2 < c1 else 'Possible reason for the rise: breakdown of control measures (e.g. ' + CTRL[d][0] + '), drug resistance, migration or conflict.')
        key += ' (c) transmission [1]; reason consistent with change [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


mcqs(t, [('Which disease is caused by a protoctist?', 'Malaria', 'Plasmodium is a protoctist.', ['Cholera', 'Tuberculosis', 'Measles']),
         ('Which disease is spread by droplet infection?', 'Tuberculosis', 'TB and measles are airborne.', ['Cholera', 'Malaria', 'HIV/AIDS']),
         ('Which cells are infected and destroyed by HIV?', 'T helper lymphocytes', 'HIV binds CD4 receptors on T helper cells.', ['Red blood cells', 'B lymphocytes only', 'Neutrophils'])])
shorts(t, [('Name the vector of malaria and state how it transmits the pathogen.', 'Female Anopheles mosquito; takes up gametes in a blood meal and injects infective stages (with saliva) when it next bites.', '[2]'),
           ('State two factors that increase the spread of TB.', 'Overcrowded living conditions; poor ventilation; HIV infection; malnutrition; drinking unpasteurised milk.', '[2]')])
explain(t, [('Explain why HIV infection leads to AIDS.', 'HIV infects and destroys T helper cells; the immune system can no longer coordinate responses; opportunistic infections such as TB and pneumonia develop.', '[3]'),
            ('Explain why cholera is common after floods or in refugee camps.', 'Sewage contaminates drinking water; overcrowding; lack of clean water and sanitation allow faecal–oral transmission.', '[2]'),
            ('Explain why measles is particularly dangerous for malnourished children.', 'Their immune systems are weaker, so complications such as pneumonia, encephalitis and blindness (with vitamin A deficiency) are more likely.', '[2]')])
myths(t, [('Malaria is caused by mosquitoes.', 'Malaria is caused by the protoctist Plasmodium; the mosquito is the vector.'), ('HIV and AIDS are the same thing.', 'HIV is the virus; AIDS is the syndrome that develops when the immune system is severely damaged.'),
          ('Cholera is spread through the air.', 'Cholera is spread by food or water contaminated with faeces.')])


@t.add('C4', (3, 4, 5), 'multi_step')
def dis_case(r, D):
    d = r.choice(list(DIS))
    c = city(r)
    intro = f'Public-health officials in {c} are investigating an outbreak of {d}.'
    parts = [lambda r: ('Name the causative organism and state the type of pathogen.', f'{cap(DIS[d][0])}; {DIS[d][1]}.', '[2]'),
             lambda r: ('Describe how the disease is transmitted.', cap(DIS[d][2]) + '.', '[2]'),
             lambda r: ('Describe the main effects of the disease on the body.', cap(DIS[d][3]) + '.', '[2]'),
             lambda r: ('Suggest two social or economic factors that could increase the spread of the disease.', 'Overcrowding; poverty / poor sanitation; lack of health care or vaccination; migration / conflict; lack of education.', '[2]'),
             lambda r: ('Suggest why it is important to identify the pathogen quickly.', 'To choose the correct treatment (e.g. antibiotics are useless against viruses) and control measures.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the causes and methods of transmission of cholera, malaria, TB, HIV/AIDS and measles.', 'Cholera: Vibrio cholerae, faecal–oral water/food. Malaria: Plasmodium, Anopheles vector. TB: Mycobacterium, droplets / milk. HIV: virus, body fluids. Measles: virus, droplets.', 'one mark per disease [5]; extra detail [2] [7]')])
t10a = t

CTRLX = {'cholera': [('provide clean, treated (chlorinated) drinking water', 'chlorine kills Vibrio cholerae, so water is no longer a route of faecal–oral transmission'),
                     ('proper sewage disposal and sanitation', 'faeces containing the bacteria do not contaminate water supplies or food'),
                     ('boil water and wash hands', 'boiling kills the bacteria; hand washing removes bacteria before food is handled'),
                     ('oral rehydration therapy for patients', 'replaces lost water and ions so patients survive while the infection clears, reducing deaths'),
                     ('vaccination of people at risk', 'gives people immunity, so fewer become infected and shed the bacteria')],
         'malaria': [('use insecticide-treated mosquito nets', 'stop female Anopheles mosquitoes biting at night and kill them, so Plasmodium is not transmitted'),
                     ('spray insecticides on walls of houses', 'kills adult mosquitoes that rest on walls after feeding, reducing the vector population'),
                     ('drain stagnant water where mosquitoes breed', 'removes breeding sites for mosquito larvae, reducing the number of vectors'),
                     ('antimalarial drugs (prophylaxis and treatment)', 'kill Plasmodium in the blood, so fewer gametocytes are available to mosquitoes and fewer people become ill'),
                     ('release fish that eat larvae', 'biological control reduces mosquito larvae and so the number of adult vectors')],
         'tuberculosis (TB)': [('BCG vaccination', 'gives immunity (especially to children), so fewer people develop TB and spread it'),
                               ('contact tracing and isolating infected people', 'infectious people are found and treated, so they do not spread droplets to others'),
                               ('long courses of several antibiotics (DOTS)', 'kill Mycobacterium completely and reduce the chance of resistance; observed treatment makes sure the course is completed'),
                               ('better housing and ventilation', 'reduces overcrowding so fewer droplets are inhaled by others'),
                               ('pasteurising milk and testing cattle', 'kills M. bovis in milk and removes infected cattle')],
         'HIV/AIDS': [('use of condoms', 'a barrier prevents exchange of body fluids during sex'), ('not sharing needles (needle exchange)', 'prevents transfer of infected blood between drug users'),
                      ('screening donated blood', 'infected blood is not used in transfusions'), ('antiretroviral drugs (including to prevent mother-to-child transmission)', 'lower the viral load, so the person is much less likely to transmit HIV'),
                      ('education and testing', 'people know their status and change behaviour, so transmission falls')],
         'measles': [('vaccination (MMR) with high coverage', 'gives individual immunity and herd immunity so the virus cannot spread'), ('isolating infected people', 'prevents droplet transmission to susceptible people'),
                     ('vitamin A supplements for children', 'reduce the severity of the disease and deaths, though not transmission'), ('contact tracing during outbreaks', 'identifies exposed people who can be vaccinated or isolated quickly')]}
CTRL = {k: [m for m, _ in v] for k, v in CTRLX.items()}
t = T('Preventing and controlling the spread of infectious diseases', 'preventing and controlling the spread')
facts(t, [('herd immunity', 'protection of unvaccinated people in a population when a large enough proportion is immune that the pathogen cannot spread effectively'),
          ('contact tracing', 'finding and testing people who have been in contact with an infected person'), ('quarantine', 'isolation of people who may have been exposed to an infectious disease'),
          ('basic reproduction number (R₀)', 'the average number of people infected by one infected person in a population with no immunity'), ('antiretroviral drugs', 'drugs that slow the replication of retroviruses such as HIV')])


@t.add('C1', (1, 2, 3), 'mcq')
def ctrl_q(r, D):
    d = r.choice(list(CTRL))
    m = r.choice(CTRL[d])
    others = [x for k, v in CTRL.items() if k != d for x in v if x not in CTRL[d]]
    return MQ(r, f'Which measure is used specifically to control the spread of {d}?', cap(m), [cap(o) for o in r.sample(others, 6)], f'{cap(d)}: {"; ".join(CTRL[d])}.')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def herd(r, D):
    d, r0 = r.choice([('measles', r.choice([12, 15, 18])), ('mumps', r.choice([5, 6, 7])), ('rubella', r.choice([5, 6])), ('polio', r.choice([5, 6, 7])), ('diphtheria', r.choice([6, 7]))])
    hit = (1 - 1 / r0) * 100
    if D == 1:
        return NQ(r, f'The R₀ of {d} is {r0}. Using threshold = (1 − 1/R₀) × 100, what percentage of the population must be immune for herd immunity?', hit, [100 / r0, hit / 2, 100 - hit / 2], '%', f'(1 − 1/{r0}) × 100 = {fx(hit, 1)}%.', f=lambda v: fx(v, 1))
    eff = r.choice([90, 93, 95, 97])
    cov = hit / eff * 100
    st = f'The basic reproduction number (R₀) of {d} is about {r0}. (a) Calculate the herd immunity threshold using (1 − 1/R₀) × 100. (b) The vaccine is {eff}% effective. Calculate the vaccination coverage needed to reach the threshold.'
    ans = f'(a) {fx(hit, 1)}% (b) {fx(cov, 1)}%' + (' – more than 100%, so herd immunity cannot be reached with this vaccine alone' if cov > 100 else '')
    key = f'(a) (1 − 1/{r0}) × 100 = {fx(hit, 1)}% [2] (b) {fx(hit, 1)} ÷ {eff / 100} = {fx(cov, 1)}% [2]'
    m = 4
    if D >= 3:
        st += ' (c) Explain how herd immunity protects babies too young to be vaccinated.'
        ans += ' (c) Most people around them are immune, so the pathogen cannot spread through the population and is unlikely to reach the baby.'
        key += ' (c) few susceptible hosts / chain of transmission broken [1]; baby unlikely to meet infected person [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4), 'short')
def ctrl_explain(r, D):
    d = r.choice(list(CTRLX))
    (a, ea), (b, eb) = r.sample(CTRLX[d], 2)
    return Q(f'Explain how each of these measures helps to control {d}: (i) {a} (ii) {b}.', f'(i) {cap(ea)}. (ii) {cap(eb)}.',
             '(i) explanation linked to transmission / effect on pathogen or vector [2] (ii) explanation [2] [4]', 'short', 4)


mcqs(t, [('Why is it difficult to develop a vaccine against malaria?', 'Plasmodium has several stages in its life cycle with different antigens, and spends time inside host cells', 'Antigenic variation and intracellular stages.', ['Plasmodium is a virus', 'Malaria is not infectious', 'Mosquitoes destroy vaccines']),
         ('Which measure reduces mother-to-child transmission of HIV?', 'Antiretroviral drugs during pregnancy and avoiding breastfeeding where safe alternatives exist', 'Reduces viral load and exposure.', ['BCG vaccination', 'Mosquito nets', 'Boiling drinking water'])])
shorts(t, [('State three ways to control the spread of cholera.', 'Clean / chlorinated water; sewage treatment; hygiene and hand washing; boiling water; vaccination.', '[3]'),
           ('State two reasons why TB is difficult to control.', 'Long antibiotic course needed; drug-resistant strains; many people with latent infection; link with HIV; overcrowding.', '[2]')])
explain(t, [('Explain why insecticide-treated bed nets reduce the incidence of malaria.', 'Anopheles mosquitoes feed at night; nets stop them biting sleeping people and the insecticide kills them, so fewer transmit Plasmodium.', '[3]'),
            ('Explain why measles was eliminated from some countries but has returned.', 'High vaccination coverage gave herd immunity; when coverage fell (e.g. vaccine hesitancy, conflict) the pathogen spread again among unvaccinated people.', '[2]'),
            ('Explain why there is no vaccine yet for HIV.', 'HIV mutates rapidly, changing its antigens; it hides inside T helper cells; it destroys the cells needed for the immune response.', '[3]')])
myths(t, [('Antibiotics can be used to control the spread of measles.', 'Measles is caused by a virus; antibiotics do not affect viruses. Vaccination controls it.'), ('Herd immunity requires everyone to be vaccinated.', 'Herd immunity needs only a large enough proportion of people to be immune.')])


@t.add('C4', (3, 4, 5), 'multi_step')
def control_case(r, D):
    d = r.choice(['malaria', 'cholera', 'tuberculosis (TB)', 'measles'])
    c = r.choice(['a refugee camp near Cox\'s Bazar', 'a flooded district in Sindh', 'a crowded city district in Lagos', 'a rural area of Mozambique'])
    intro = f'Health workers are planning a programme to reduce {d} in {c}.'
    parts = [lambda r: ('Suggest and explain three measures that could be included.', ' '.join(f'{cap(m)}: {e}.' for m, e in CTRLX[d][:3]), 'three measures, each explained [3]'),
             lambda r: ('Explain why the programme may be difficult to carry out in this location.', 'Overcrowding, poverty, poor infrastructure (water, sanitation, roads), lack of health workers, conflict, cost of drugs / vaccines, cultural factors.', '[3]'),
             lambda r: ('Describe how the success of the programme could be measured.', 'Record the number of new cases (incidence) per 100 000 before and after, over several years, compared with a similar area.', '[2]'),
             lambda r: ('Discuss whether global eradication of this disease is realistic.', 'Eradication needs an effective vaccine, no animal reservoir, easy diagnosis and global cooperation, as with smallpox. ' + {'malaria': 'Malaria has a mosquito vector, several Plasmodium species, drug and insecticide resistance and only partly effective vaccines, so eradication is unlikely soon.', 'cholera': 'Cholera bacteria survive in water and the environment and immunity is short-lived, so eradication depends on clean water for everyone and is unlikely soon.', 'tuberculosis (TB)': 'TB has latent infections, drug-resistant strains, a cattle reservoir (M. bovis), a partly effective vaccine and a link with HIV, so eradication is unlikely soon.', 'measles': 'Measles has no animal reservoir and an effective vaccine, so eradication is possible in principle, but requires about 95% coverage everywhere.'}[d], '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Discuss the biological, social and economic factors that need to be considered in the prevention and control of malaria, cholera, TB, HIV/AIDS and measles.', 'Biological: vectors, pathogen variation, resistance, latent infections, vaccine availability. Social: overcrowding, sanitation, education, cultural practices, conflict. Economic: cost of drugs, nets, water treatment, health workers. Examples of measures for each disease.',
           'biological factors [2]; social [2]; economic [1]; specific examples [2] [7]')])
t10b = t

t = T('Antibiotics: how they work, antibiotic resistance and reducing its impact', 'antibiotics')
facts(t, [('antibiotic', 'a chemical (originally from a microorganism) that kills or inhibits the growth of bacteria without harming human cells'),
          ('bactericidal', 'describes an antibiotic that kills bacteria'), ('bacteriostatic', 'describes an antibiotic that stops bacteria growing and dividing'),
          ('antibiotic resistance', 'the ability of a bacterium to survive exposure to an antibiotic that would normally kill it or stop its growth'),
          ('MRSA', 'meticillin-resistant Staphylococcus aureus, a strain of bacteria resistant to many antibiotics'),
          ('horizontal gene transfer', 'the passing of genes, often on plasmids, from one bacterium to another, including between species, by conjugation'),
          ('penicillin', 'an antibiotic that inhibits the enzymes that form cross-links in bacterial cell walls, so bacteria burst by osmosis')])
mcqs(t, [('How does penicillin kill bacteria?', 'It prevents cross-links forming in the cell wall, so the bacterium bursts by osmosis', 'Inhibits transpeptidase during wall synthesis.', ['It denatures bacterial ribosomes', 'It dissolves the cell membrane', 'It stops the bacterium respiring']),
         ('Why does penicillin not harm human cells?', 'Human cells do not have peptidoglycan cell walls', 'Selective toxicity.', ['Human cells have 70S ribosomes', 'Human cells are too large', 'Human cells have cellulose walls']),
         ('How does antibiotic resistance first arise in a population of bacteria?', 'By a random mutation in a bacterium\'s DNA', 'Mutation is random; the antibiotic then selects resistant bacteria.', ['The antibiotic causes the bacteria to mutate', 'Bacteria become used to the antibiotic', 'Humans become immune to the antibiotic'])])
shorts(t, [('State three ways to reduce the development of antibiotic resistance.', 'Prescribe only when needed (not for viruses); complete the course; use narrow-spectrum antibiotics; reduce use in farming; hygiene in hospitals; rotate antibiotics.', '[3]'),
           ('State why antibiotics are ineffective against viruses.', 'Viruses lack cell walls, ribosomes and metabolism targeted by antibiotics; they reproduce inside host cells.', '[1]')])
explain(t, [('Explain how a population of antibiotic-resistant bacteria develops.', 'Random mutation gives a resistance allele; when the antibiotic is used, susceptible bacteria die; resistant ones survive and reproduce by binary fission, passing on the allele; plasmids spread it horizontally; over generations most are resistant (natural selection).', '[4]'),
            ('Explain why patients should finish a course of antibiotics even if they feel better.', 'To kill all bacteria, including those that are less susceptible; stopping early leaves survivors that can multiply and be selected for resistance.', '[2]'),
            ('Explain why antibiotic resistance spreads more rapidly in bacteria than resistance in animals.', 'Bacteria reproduce very quickly (short generation time); resistance genes on plasmids can be transferred between bacteria, even different species.', '[2]')])
myths(t, [('Bacteria become resistant because they get used to the antibiotic.', 'Resistance arises by random mutation and is selected by the antibiotic; individual bacteria do not adapt.'), ('People become resistant to antibiotics.', 'Bacteria, not people, become resistant.'),
          ('Antibiotics can cure flu.', 'Flu is caused by a virus; antibiotics have no effect on viruses.')])
DISC = {'setup': lambda r, p: f'{p} spread a culture of bacteria evenly on nutrient agar plates and placed paper discs soaked in different concentrations of an antibiotic on them. After 48 hours at 25 °C, the diameter of the clear zone around each disc was measured.',
        'iv': ('antibiotic concentration', 'μg cm⁻³'), 'xs': lambda r: r.choice([[5, 10, 20, 40, 80], [10, 25, 50, 100, 200], [2, 4, 8, 16, 32]]),
        'dv': ('diameter of clear zone', 'mm'), 'y': lambda x, k: k * (8 + 5 * math.log2(x)), 'dp': 0,
        'controls': ['type and volume of bacterial culture', 'volume of nutrient agar', 'size of paper disc', 'volume of antibiotic solution on each disc', 'incubation temperature and time'],
        'trend': lambda d: 'As the antibiotic concentration increases, the diameter of the clear zone increases, but by smaller amounts at higher concentrations.',
        'why': ('The antibiotic diffuses out of the disc into the agar; a higher concentration diffuses further at a concentration high enough to kill or inhibit bacteria, so the clear zone (no bacterial growth) is wider.', 'diffusion from disc [1]; higher concentration reaches further [1]; bacteria killed / inhibited in clear zone [1] [3]'),
        'improve': ['measure the diameter in two directions at right angles and take the mean', 'use three plates for each concentration'],
        'control': 'A disc soaked in sterile distilled water; there should be no clear zone, showing that the antibiotic causes the inhibition.',
        'extra': [lambda r, d: ('Calculate the area of the clear zone at the highest concentration (area = πr²).', f'{fx(math.pi * (d["means"][-1] / 2) ** 2, 0)} mm²', f'r = {fx(d["means"][-1] / 2, 2)} mm [1]; π × r² = {fx(math.pi * (d["means"][-1] / 2) ** 2, 0)} mm² [1] [2]'),
                  lambda r, d: ('State two aseptic techniques that should be used and explain why.', 'Flame the loop / neck of the bottle; lift the lid only slightly; tape the lid without sealing completely; prevents contamination by other microorganisms and escape of bacteria.', '[2]')]}
add_practical(t, DISC, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def resist_growth(r, D):
    gt = r.choice([20, 30, 40, 60])
    hrs = r.choice([4, 6, 8, 10])
    n = hrs * 60 // gt
    n0 = r.choice([1, 10, 100])
    N = n0 * 2 ** n
    if D == 1:
        return NQ(r, f'A bacterium divides every {gt} minutes. Starting with one resistant bacterium, how many are present after {hrs} hours?', 2 ** n, [2 * n, 2 ** (n - 1), n ** 2], '', f'{hrs} × 60 ÷ {gt} = {n} divisions; 2^{n} = {2 ** n:,}.', f=lambda v: f'{int(v):,}')
    st = f'In a patient in {city(r)}, {n0} antibiotic-resistant bacteri{"um" if n0 == 1 else "a"} survive{"s" if n0 == 1 else ""} a course of antibiotics. The generation time is {gt} minutes. (a) Calculate the number of resistant bacteria after {hrs} hours (assume no deaths). (b) Explain why the population after this time is almost entirely resistant.'
    ans = f'(a) {sci(N, 3) if N >= 1e6 else f"{N:,}"} (b) The antibiotic killed susceptible bacteria (selection pressure); only resistant bacteria survived and reproduced, passing on the resistance allele to all their offspring.'
    key = f'(a) {n} generations [1]; {n0} × 2^{n} = {sci(N, 3) if N >= 1e6 else f"{N:,}"} [1] (b) selection by antibiotic [1]; resistant survive and reproduce / pass on allele [1]'
    m = 4
    if D >= 4:
        st += ' (c) Explain how the resistance gene could pass to a different species of bacterium.'
        ans += ' (c) If it is on a plasmid, it can be copied and transferred by conjugation (horizontal gene transfer) through a pilus.'
        key += ' (c) plasmid [1]; conjugation / horizontal transfer [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def mrsa_case(r, D):
    a, b = r.choice([(12, 40), (8, 35), (15, 45), (5, 30)])
    intro = f'In a hospital in {city(r)}, the percentage of Staphylococcus aureus infections caused by MRSA rose from {a}% to {b}% over ten years.'
    parts = [lambda r: ('Calculate the percentage increase in the proportion of MRSA infections.', f'{fx((b - a) / a * 100, 0)}%', f'({b} − {a}) ÷ {a} × 100 = {fx((b - a) / a * 100, 0)}% [2]'),
             lambda r: ('Explain how MRSA became common in the hospital.', 'Random mutation gave resistance; heavy antibiotic use killed susceptible bacteria; resistant ones survived, reproduced and spread between patients (natural selection); plasmid transfer.', '[4]'),
             lambda r: ('Suggest three measures the hospital could take to reduce MRSA infections.', 'Hand washing / alcohol gel; screening and isolating carriers; cleaning; reducing unnecessary antibiotic use; using narrow-spectrum antibiotics.', '[3]'),
             lambda r: ('Explain why hospitals are places where resistant bacteria are more likely to spread.', 'Many patients on antibiotics (strong selection); weakened immune systems; close contact; invasive procedures.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how antibiotics such as penicillin act on bacteria, how resistance develops and spreads, and how its impact can be reduced.', 'Penicillin inhibits cross-linking enzymes → weak wall → osmotic lysis; not effective on viruses / human cells. Resistance: random mutation, selection, survival and reproduction, plasmids, conjugation. Reduction: fewer prescriptions, complete course, narrow-spectrum, hygiene, less in farming, new antibiotics.',
           'mode of action [2]; development of resistance [3]; reducing impact [2] [7]')])
t10c = t
CHAPTERS[10] = [t10a, t10b, t10c]


# ===================================================================== 11 Immunity
t = T('Phagocytes and the non-specific immune response', 'phagocytes')
facts(t, [('phagocyte', 'a white blood cell that engulfs and digests pathogens and debris by phagocytosis, such as a neutrophil or macrophage'),
          ('neutrophil', 'a short-lived phagocyte with a lobed nucleus that is the first to arrive at a site of infection'),
          ('macrophage', 'a long-lived phagocyte, formed from a monocyte, that engulfs pathogens and presents their antigens to lymphocytes'),
          ('antigen', 'a molecule (often a protein or glycoprotein) that stimulates an immune response and the production of antibodies'),
          ('chemotaxis', 'movement of cells such as phagocytes towards chemicals released at a site of infection'), ('phagosome', 'the vesicle containing an engulfed pathogen inside a phagocyte'),
          ('opsonin', 'a molecule, such as an antibody, that binds to a pathogen and makes it easier for phagocytes to engulf it')])
STEPS = ['Chemicals released by pathogens and damaged cells attract phagocytes (chemotaxis)', 'Receptors on the phagocyte bind to the pathogen', 'The cell surface membrane extends around the pathogen and engulfs it by endocytosis',
         'A phagocytic vesicle (phagosome) forms', 'Lysosomes fuse with the vesicle and release hydrolytic enzymes', 'The pathogen is digested and the products are absorbed or removed']


@t.add('C1', (1, 2, 3), 'mcq')
def phago_order(r, D):
    i = r.randrange(1, len(STEPS))
    return MQ(r, f'In phagocytosis, which step comes immediately after this one: "{STEPS[i - 1]}"?', STEPS[i], [x for j, x in enumerate(STEPS) if j != i and j != i - 1], 'Sequence: ' + ' → '.join(STEPS) + '.')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def wbc_count(r, D):
    tot = r.choice([100, 200, 250, 400])
    neu = round(tot * r.uniform(0.5, 0.7))
    lym = round(tot * r.uniform(0.2, 0.32))
    mon = round(tot * r.uniform(0.03, 0.08))
    eos = tot - neu - lym - mon
    if eos < 0:
        return None
    if D == 1:
        return NQ(r, f'In a blood smear, {neu} of {tot} white blood cells counted were neutrophils. What percentage is this?', neu / tot * 100, [neu / (tot - neu) * 100, tot / neu, 100 - neu / tot * 100], '%', f'{neu} ÷ {tot} × 100 = {fx(neu / tot * 100, 1)}%.', f=lambda v: fx(v, 1))
    wbc = r.choice([6.5, 7.0, 8.0, 12.0, 15.0])
    st = (f'{person(r)} examined a stained blood smear and counted {tot} white blood cells: neutrophils {neu}, lymphocytes {lym}, monocytes {mon}, others {eos}. (a) Calculate the percentage of each of neutrophils and lymphocytes. '
          f'(b) The total white cell count is {fx(wbc, 1)} × 10⁹ dm⁻³. Calculate the number of neutrophils per dm³.')
    ans = f'(a) neutrophils {fx(neu / tot * 100, 1)}%; lymphocytes {fx(lym / tot * 100, 1)}% (b) {fx(wbc * neu / tot, 2)} × 10⁹ dm⁻³'
    key = f'(a) {neu} ÷ {tot} × 100 = {fx(neu / tot * 100, 1)}% [1]; {lym} ÷ {tot} × 100 = {fx(lym / tot * 100, 1)}% [1] (b) {fx(neu / tot, 3)} × {fx(wbc, 1)} × 10⁹ = {fx(wbc * neu / tot, 2)} × 10⁹ [2]'
    m = 4
    if D >= 3:
        st += ' (c) Describe how you would distinguish a neutrophil from a lymphocyte in the smear.'
        ans += ' (c) Neutrophil: lobed nucleus, granular cytoplasm, larger (10–12 μm). Lymphocyte: large round nucleus filling most of the cell, little cytoplasm, smaller (about 7 μm).'
        key += ' (c) neutrophil lobed nucleus [1]; lymphocyte large round nucleus / little cytoplasm [1]'
        m += 2
    if D >= 5:
        st += f' (d) A normal count is 4–11 × 10⁹ dm⁻³. Suggest what the patient\'s count indicates.'
        ans += ' (d) ' + ('Above normal: likely a bacterial infection, as more neutrophils are produced.' if wbc > 11 else 'Within the normal range: no evidence of a major infection.')
        key += ' (d) correct interpretation [1]'
        m += 1
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


mcqs(t, [('Which white blood cell is the first to arrive in large numbers at a site of infection?', 'Neutrophil', 'Neutrophils are short-lived and numerous.', ['Macrophage', 'B lymphocyte', 'Plasma cell']),
         ('Where do macrophages come from?', 'Monocytes that leave the blood and enter tissues', 'Monocytes mature into macrophages.', ['Neutrophils that divide', 'B lymphocytes', 'Red blood cells']),
         ('Why is the response of phagocytes described as non-specific?', 'They engulf many different types of pathogen in the same way', 'Not specific to a particular antigen.', ['They only attack bacteria', 'They make antibodies', 'They remember previous infections'])])
shorts(t, [('State two differences between neutrophils and macrophages.', 'Neutrophils: lobed nucleus, short-lived, first to arrive, many in blood. Macrophages: large, long-lived, in tissues, present antigens to lymphocytes.', '[2]'),
           ('State the role of lysosomes in phagocytes.', 'They fuse with phagocytic vesicles and release hydrolytic enzymes to digest the pathogen.', '[1]')])
explain(t, [('Describe and explain how a neutrophil destroys a bacterium.', 'Attracted by chemicals (chemotaxis); receptors bind bacterium; engulfs by endocytosis into a phagocytic vesicle; lysosomes fuse and release hydrolytic enzymes; bacterium digested.', '[4]'),
            ('Explain the role of macrophages in linking the non-specific and specific immune responses.', 'Macrophages engulf pathogens, partly digest them and display antigens on their surface (antigen-presenting cells); these activate specific T helper lymphocytes.', '[3]'),
            ('Explain why there are many lysosomes in phagocytes.', 'Many pathogens are engulfed; lysosomes supply hydrolytic enzymes to digest them.', '[2]')])
myths(t, [('Phagocytes produce antibodies.', 'Antibodies are produced by plasma cells (from B lymphocytes); phagocytes engulf pathogens.'), ('Phagocytes only attack one type of pathogen.', 'Phagocytes are non-specific and engulf many types.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def phago_case(r, D):
    path = r.choice(['Staphylococcus bacteria entering a cut on the hand', 'Streptococcus bacteria in the throat', 'Mycobacterium tuberculosis in the alveoli', 'spores of a fungus inhaled into the lungs'])
    intro = f'A pathology lecturer in {city(r)} describes the body\'s response to {path}.'
    parts = [lambda r: ('Explain how phagocytes reach the site of infection.', 'Damaged cells and pathogens release chemicals (e.g. histamine) causing inflammation; capillaries become leaky; phagocytes squeeze out and move towards chemicals (chemotaxis).', '[3]'),
             lambda r: ('Describe phagocytosis by a neutrophil.', ' → '.join(STEPS) + '.', '[4]'),
             lambda r: ('Explain how antibodies make phagocytosis more effective.', 'Antibodies act as opsonins / cause agglutination; phagocytes have receptors for antibodies, so they bind and engulf pathogens more easily.', '[2]'),
             lambda r: ('State one difference between the role of neutrophils and macrophages.', 'Macrophages present antigens to lymphocytes / are long-lived; neutrophils are short-lived first responders.', '[1]'),
             lambda r: ('Suggest why pus forms at an infected cut.', 'Dead neutrophils, bacteria and tissue debris accumulate.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the origin and roles of neutrophils and macrophages and explain how phagocytosis destroys pathogens.', 'Both from bone marrow stem cells; neutrophils short-lived, lobed nucleus, first responders; monocytes → macrophages in tissues, long-lived, antigen presentation. Phagocytosis: chemotaxis, binding, endocytosis, phagosome, lysosomes, hydrolytic enzymes, digestion.',
           'origin [1]; neutrophils [1]; macrophages / antigen presentation [2]; phagocytosis steps [3] [7]')])
t11a = t

t = T('Lymphocytes: B cells, T cells, clonal selection and memory cells', 'lymphocytes')
facts(t, [('B lymphocyte', 'a lymphocyte that matures in the bone marrow and, when activated, divides to form plasma cells that secrete antibodies and memory cells'),
          ('T helper cell', 'a T lymphocyte that releases cytokines to stimulate B cells to divide and secrete antibodies, and to activate T killer cells and macrophages'),
          ('T killer cell', 'a T lymphocyte that attaches to and destroys infected body cells displaying a specific antigen'), ('plasma cell', 'an activated B lymphocyte that secretes large amounts of antibody'),
          ('memory cell', 'a long-lived lymphocyte that remains after an immune response and responds quickly if the same antigen enters the body again'),
          ('clonal selection', 'the selection of the lymphocyte with receptors complementary to a particular antigen, which then divides by mitosis (clonal expansion)'),
          ('self antigen', 'an antigen on the body\'s own cells that does not normally stimulate an immune response'), ('cytokine', 'a signalling molecule released by cells such as T helper cells that stimulates other immune cells')])
mcqs(t, [('Where do T lymphocytes mature?', 'In the thymus', 'B cells mature in bone marrow; T cells in the thymus.', ['In the bone marrow', 'In the spleen', 'In the liver']),
         ('Why is the secondary immune response faster than the primary response?', 'Memory cells recognise the antigen and divide rapidly', 'More cells with the right receptors are already present.', ['Antibodies from the first infection remain at high concentration', 'Phagocytes have learned the antigen', 'The pathogen is weaker']),
         ('Which cells secrete antibodies?', 'Plasma cells', 'Plasma cells are differentiated B cells.', ['T helper cells', 'T killer cells', 'Memory T cells'])])
shorts(t, [('State the roles of T helper cells and T killer cells.', 'T helper: release cytokines that stimulate B cells and T killer cells / macrophages. T killer: bind to and destroy infected / cancer cells.', '[2]'),
           ('State what is meant by clonal expansion.', 'Repeated mitosis of a selected lymphocyte to produce many identical cells with the same receptor.', '[1]')])
explain(t, [('Explain how clonal selection leads to the production of antibodies against a specific antigen.', 'Each B cell has receptors for one antigen; the B cell with complementary receptors binds the antigen; stimulated by T helper cytokines, it divides by mitosis (clonal expansion); differentiates into plasma cells secreting the specific antibody and memory cells.', '[4]'),
            ('Explain why the immune system does not usually attack the body\'s own cells.', 'During development, lymphocytes with receptors complementary to self antigens are destroyed, so only those recognising non-self antigens remain.', '[2]'),
            ('Explain how T killer cells destroy virus-infected cells.', 'Infected cells display viral antigens on their surface; T killer cells with complementary receptors bind and release chemicals (perforins) that make holes in the membrane, killing the cell.', '[3]')])
myths(t, [('Memory cells are antibodies that stay in the blood.', 'Memory cells are long-lived lymphocytes; antibodies decline after an infection.'), ('B cells destroy infected cells directly.', 'B cells form plasma cells that secrete antibodies; T killer cells destroy infected cells.')])


@t.add('C3', (2, 3, 4, 5), 'case')
def response_data(r, D):
    lag1 = r.choice([7, 8, 10, 12])
    pk1 = r.choice([10, 15, 20, 25])
    lag2 = r.choice([2, 3, 4])
    fold = r.choice([8, 10, 15, 20])
    pk2 = pk1 * fold
    day2 = r.choice([28, 35, 42])
    intro = (f'A volunteer in {city(r)} was injected with an antigen on day 0 and again on day {day2}. After the first injection, antibody was first detected after {lag1} days and peaked at {pk1} arbitrary units. '
             f'After the second injection, antibody was detected after {lag2} days and peaked at {pk2} arbitrary units.')
    parts = [lambda r: ('Calculate how many times greater the peak concentration was after the second injection.', f'{fold}', f'{pk2} ÷ {pk1} = {fold} [1]'),
             lambda r: ('Calculate the percentage reduction in the time before antibody was detected.', f'{fx((lag1 - lag2) / lag1 * 100, 0)}%', f'({lag1} − {lag2}) ÷ {lag1} × 100 = {fx((lag1 - lag2) / lag1 * 100, 0)}% [2]'),
             lambda r: ('Explain the differences between the primary and secondary responses.', 'Memory cells produced in the primary response are present in larger numbers; they recognise the antigen quickly, divide rapidly and form many plasma cells, so antibody is made sooner and in greater amounts.', 'memory cells [1]; faster clonal expansion [1]; more plasma cells / antibody [1] [3]'),
             lambda r: ('Explain why there is a delay before antibodies appear after the first injection.', 'Few lymphocytes have complementary receptors; time needed for clonal selection, activation by T helper cells, division and differentiation into plasma cells.', '[2]'),
             lambda r: ('Suggest why the antibody concentration falls after each peak.', 'Antigen has been removed so plasma cells stop secreting / die; antibodies are broken down.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


@t.add('C3', (1, 2, 3, 4), 'numerical')
def clone_calc(r, D):
    ct = r.choice([6, 8, 10, 12])
    days = r.choice([3, 4, 5])
    n = days * 24 // ct
    if D == 1:
        return NQ(r, f'An activated B lymphocyte divides every {ct} hours. How many cells are in the clone after {days} days?', 2 ** n, [2 * n, n ** 2, 2 ** (n - 1)], '', f'{days * 24} ÷ {ct} = {n} divisions; 2^{n} = {2 ** n:,}.', f=lambda v: f'{int(v):,}')
    pc = r.choice([0.8, 0.9, 0.95])
    rate = r.choice([2000, 5000, 10000])
    N = 2 ** n
    st = f'An activated B lymphocyte divides by mitosis every {ct} hours for {days} days. (a) Calculate the number of cells produced. (b) {int(pc * 100)}% of these become plasma cells, each secreting {rate:,} antibody molecules per second. Calculate the number of antibody molecules secreted per second by the clone.'
    return Q(st, f'(a) {N:,} (b) {sci(N * pc * rate, 3)}', f'(a) {n} divisions; 2^{n} = {N:,} [2] (b) {N:,} × {pc} = {fx(N * pc, 0)} plasma cells [1]; × {rate:,} = {sci(N * pc * rate, 3)} s⁻¹ [1] [4]', 'numerical', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def lymph_case(r, D):
    v = r.choice(['measles virus', 'influenza virus', 'hepatitis B virus', 'SARS-CoV-2'])
    intro = f'A child in {city(r)} is infected with {v} for the first time.'
    parts = [lambda r: ('Describe the roles of T helper cells in the response.', 'Bind to antigens presented by macrophages; divide; release cytokines that stimulate B cells (to divide and secrete antibody) and T killer cells and macrophages.', '[3]'),
             lambda r: ('Explain how T killer cells help to end the infection.', 'Recognise viral antigens on infected cells; bind and destroy them, so virus cannot replicate.', '[2]'),
             lambda r: ('Describe how B cells respond to the virus.', 'B cell with complementary receptor binds antigen; clonal selection and expansion (mitosis); plasma cells secrete antibodies; memory cells formed.', '[4]'),
             lambda r: ('Explain why the child is unlikely to suffer from the disease if infected again.', 'Memory cells give a fast, large secondary response, destroying the virus before symptoms develop (active immunity).', '[2]'),
             lambda r: ('Explain why a person can catch influenza many times.', 'The virus mutates, changing its antigens (antigenic drift), so memory cells do not recognise it.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the roles of B and T lymphocytes in the specific immune response, explaining clonal selection and the importance of memory cells.', 'Origin and maturation (bone marrow / thymus); self vs non-self; antigen presentation; clonal selection and expansion; T helper cytokines; plasma cells and antibodies; T killer cells; memory cells, secondary response faster and larger.',
           'B cells / plasma cells [2]; T helper / killer [2]; clonal selection [1]; memory / secondary response [2] [7]')])
t11b = t

t = T('Antibody structure and function', 'antibody structure and function')
facts(t, [('antibody', 'a globular glycoprotein (immunoglobulin) secreted by plasma cells that binds to a specific antigen'), ('variable region', 'the part at the tip of each arm of an antibody, with a different amino acid sequence in each antibody, that forms the antigen-binding site'),
          ('constant region', 'the part of an antibody that is the same in all antibodies of a class and binds to receptors on phagocytes'), ('hinge region', 'the flexible part of an antibody that allows the arms to move so it can bind to antigens a variable distance apart'),
          ('agglutination', 'the clumping together of pathogens by antibodies, making them easier for phagocytes to engulf'), ('neutralisation', 'the action of antibodies in binding to toxins or viruses so they cannot bind to host cells'),
          ('disulfide bond', 'a covalent bond that holds the heavy and light polypeptide chains of an antibody together')])
mcqs(t, [('How many polypeptide chains make up a typical IgG antibody?', 'Four: two heavy and two light chains', 'Held together by disulfide bonds.', ['Two heavy chains only', 'Three: one heavy and two light chains', 'One long chain']),
         ('Which part of an antibody gives it its specificity?', 'The variable region', 'Its amino acid sequence determines the shape of the antigen-binding site.', ['The constant region', 'The hinge region', 'The disulfide bonds']),
         ('How many antigen-binding sites does one IgG antibody molecule have?', 'Two', 'One at the tip of each arm.', ['One', 'Four', 'Ten'])])
shorts(t, [('State three ways in which antibodies help to destroy pathogens.', 'Agglutination; neutralisation of toxins / viruses; opsonisation (marking for phagocytosis); activating complement to lyse cells.', '[3]'),
           ('State the level of protein structure shown by an antibody, and why.', 'Quaternary: it has more than one polypeptide chain (four).', '[1]')])
explain(t, [('Explain how the structure of an antibody is related to its function.', 'Variable regions form two specific antigen-binding sites complementary to one antigen; two sites allow agglutination; hinge gives flexibility; constant region binds phagocyte receptors; disulfide bonds stabilise the structure.', '[4]'),
            ('Explain why each antibody binds to only one antigen.', 'The amino acid sequence of the variable region determines a specific 3-D shape of the binding site, complementary only to that antigen.', '[2]'),
            ('Explain how agglutination helps the immune response.', 'Each antibody binds two pathogens, clumping them; clumps cannot spread or enter cells and are easily engulfed by phagocytes.', '[2]')])
myths(t, [('Antibodies kill bacteria by digesting them.', 'Antibodies bind to antigens; phagocytes (or complement) destroy the pathogens.'), ('Antibodies are made of carbohydrate.', 'Antibodies are glycoproteins: proteins with some carbohydrate attached.')])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def antibody_calc(r, D):
    hc, lc = r.choice([(446, 214), (450, 214), (440, 220)])
    if D == 1:
        n = r.choice([5, 10, 50, 100])
        return NQ(r, f'How many antigen-binding sites are there on {n} IgG antibody molecules?', 2 * n, [n, 4 * n, n // 2], '', f'Each IgG has 2 binding sites: {n} × 2 = {2 * n}.', f=lambda v: str(int(v)))
    tot = 2 * hc + 2 * lc
    pb = tot - 4
    st = f'An IgG antibody contains two heavy chains of {hc} amino acids and two light chains of {lc} amino acids. (a) Calculate the total number of amino acids and the number of peptide bonds. (b) Name the bonds that hold the four chains together.'
    ans = f'(a) {tot:,} amino acids; {pb:,} peptide bonds (b) Disulfide bonds (with hydrogen bonds / other interactions)'
    key = f'(a) 2 × {hc} + 2 × {lc} = {tot:,} [1]; {tot:,} − 4 = {pb:,} [1] (b) disulfide [1]'
    m = 3
    if D >= 3:
        st += ' (c) Explain why antibodies produced against different antigens have different amino acid sequences only in part of each chain.'
        ans += ' (c) The variable regions differ to give binding sites complementary to different antigens; constant regions are the same so they bind the same phagocyte receptors.'
        key += ' (c) variable region specific to antigen [1]; constant region same function [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def antibody_case(r, D):
    tox = r.choice(['tetanus toxin', 'diphtheria toxin', 'snake venom', 'the cholera toxin'])
    intro = f'A patient in {city(r)} is treated for exposure to {tox} with an injection of antibodies that bind to it.'
    parts = [lambda r: ('Draw or describe the structure of an antibody molecule.', 'Y-shaped; two heavy and two light chains; disulfide bonds; variable regions with antigen-binding sites at tips; constant region; hinge region.', '[4]'),
             lambda r: (f'Explain how the antibodies prevent {tox} harming the patient.', 'They bind to the toxin (neutralisation), changing / blocking its shape so it cannot bind to receptors on body cells; complexes are engulfed by phagocytes.', '[2]'),
             lambda r: ('State the type of immunity given by this injection and explain why it is short-lived.', 'Artificial passive immunity: no memory cells are made and the injected antibodies are broken down.', '[3]'),
             lambda r: ('Explain why each antibody is specific to one antigen.', 'Variable region amino acid sequence gives a binding site complementary to one antigen.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of an antibody and explain how antibodies help to protect the body against pathogens.', 'Glycoprotein; four chains (2 heavy, 2 light); disulfide bonds; variable regions / antigen-binding sites; constant region; hinge. Functions: agglutination, neutralisation, opsonisation, activating complement / lysis, binding to phagocytes.',
           'structure [3]; functions [3] [6]')])
t11c = t

IMM = {'natural active': [('a child recovering from chickenpox', 'the child\'s own lymphocytes made antibodies and memory cells after infection')],
       'artificial active': [('a traveller given a yellow fever vaccine', 'the vaccine contains antigens that stimulate the person to make antibodies and memory cells'), ('a baby given the MMR vaccine', 'the vaccine stimulates memory cell production')],
       'natural passive': [('a breastfed baby receiving antibodies in milk', 'antibodies are received from the mother; no memory cells are made'), ('a fetus receiving antibodies across the placenta', 'IgG antibodies cross from the mother; no memory cells are made')],
       'artificial passive': [('a person bitten by a snake given antivenom', 'ready-made antibodies are injected; no memory cells are made'), ('a person given an injection of anti-tetanus antibodies after a deep cut', 'injected antibodies give immediate protection but no memory cells')]}
t = T('Active and passive immunity; vaccination and monoclonal antibodies', 'active and passive immunity')
facts(t, [('active immunity', 'immunity gained when an antigen stimulates the immune system to produce antibodies and memory cells'), ('passive immunity', 'immunity gained when antibodies are received from another source, so no memory cells are made'),
          ('vaccine', 'a preparation containing antigens (e.g. dead or attenuated pathogens, toxoids or mRNA) given to stimulate active immunity'),
          ('monoclonal antibodies', 'identical antibodies produced by a single clone of cells, all specific to one antigen'), ('hybridoma', 'a cell formed by fusing a plasma (B) cell with a cancer (myeloma) cell, which divides indefinitely and secretes one type of antibody'),
          ('attenuated', 'describes a pathogen that has been weakened so that it causes an immune response but not disease')])


@t.add('C1', (1, 2, 3), 'mcq')
def imm_type(r, D):
    k = r.choice(list(IMM))
    ex, why = r.choice(IMM[k])
    return MQ(r, f'Which type of immunity is shown by {ex}?', cap(k), [cap(x) for x in IMM if x != k] + ['Non-specific'], f'{cap(k)}: {why}.')


@t.add('C3', (2, 3, 4), 'short')
def imm_classify(r, D):
    ks = r.sample(list(IMM), 2)
    exs = [r.choice(IMM[k]) for k in ks]
    st = f'For each example, state the type of immunity (natural or artificial, active or passive) and explain whether it is long-lasting: (i) {exs[0][0]} (ii) {exs[1][0]}.'
    ans = ' '.join(f'({"i" * (j + 1)}) {cap(k)}: {e[1]}; ' + ('long-lasting (memory cells).' if 'active' in k else 'short-lived (no memory cells; antibodies broken down).') for j, (k, e) in enumerate(zip(ks, exs)))
    return Q(st, ans, '(i) type [1]; duration with reason [1] (ii) type [1]; duration with reason [1] [4]', 'short', 4)


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def vacc_data(r, D):
    v = r.choice([('measles', 'MCV1'), ('diphtheria–tetanus–pertussis', 'DTP3'), ('polio', 'Pol3'), ('hepatitis B', 'HepB3')])
    pop = r.choice([40000, 60000, 85000, 120000])
    vac = round(pop * r.uniform(0.7, 0.97))
    if D == 1:
        return NQ(r, f'In a district, {vac:,} of {pop:,} children received {v[1]} vaccine. What was the vaccination coverage?', vac / pop * 100, [(pop - vac) / pop * 100, vac / pop, pop / vac * 100], '%', f'{vac:,} ÷ {pop:,} × 100 = {fx(vac / pop * 100, 1)}%.', f=lambda z: fx(z, 1))
    st = f'In a region of {city(r)}, {vac:,} out of {pop:,} one-year-old children received {v[1]} ({v[0]}) vaccine. (a) Calculate the percentage coverage. (b) Calculate how many children remained unvaccinated.'
    cov = vac / pop * 100
    ans = f'(a) {fx(cov, 1)}% (b) {pop - vac:,}'
    key = f'(a) {vac:,} ÷ {pop:,} × 100 = {fx(cov, 1)}% [1] (b) {pop:,} − {vac:,} = {pop - vac:,} [1]'
    m = 2
    if D >= 3:
        st += ' (c) Explain how vaccination protects an individual child.'
        ans += ' (c) The vaccine contains antigens that stimulate B and T cells; clonal selection; plasma cells make antibodies and memory cells are produced, so a later infection triggers a fast secondary response.'
        key += ' (c) antigens stimulate lymphocytes [1]; memory cells [1]; secondary response [1]'
        m += 3
    if D >= 4:
        st += f' (d) {"Measles requires about 95% coverage for herd immunity. Comment on the coverage in this region." if v[0] == "measles" else "Suggest two reasons why coverage may be below target."}'
        ans += (' (d) ' + ('Coverage is ' + ('above' if cov >= 95 else 'below') + ' 95%, so herd immunity ' + ('should be' if cov >= 95 else 'is not') + ' achieved; outbreaks are ' + ('unlikely.' if cov >= 95 else 'possible among unvaccinated children.')) if v[0] == 'measles'
                else ' (d) Difficulty reaching remote areas / cold-chain problems; cost; vaccine hesitancy; conflict; missed follow-up doses.')
        key += ' (d) valid comment / two reasons [2]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


mcqs(t, [('Why does passive immunity give only short-term protection?', 'No memory cells are produced and the antibodies are broken down', 'Antibodies have a limited life.', ['The antibodies are too specific', 'Passive immunity only works in children', 'Antigens are destroyed']),
         ('Why is a myeloma (cancer) cell fused with a plasma cell to make monoclonal antibodies?', 'Plasma cells do not divide, but the hybridoma divides indefinitely while secreting the antibody', 'Combines antibody production with immortality.', ['Myeloma cells make antibodies', 'Plasma cells are too small', 'To make the antibody non-specific']),
         ('Which is an example of artificial active immunity?', 'Receiving a vaccine against polio', 'Antigen given artificially → own antibodies and memory cells.', ['Receiving antibodies in breast milk', 'Recovering from measles', 'Receiving antivenom'])])
shorts(t, [('State two uses of monoclonal antibodies.', 'Diagnosis (e.g. pregnancy tests, detecting pathogens); treatment (e.g. targeting cancer cells, Herceptin; rheumatoid arthritis); blood typing; research.', '[2]'),
           ('Describe the difference between active and passive immunity.', 'Active: own immune response, antibodies and memory cells made, long-lasting, takes time. Passive: antibodies received, no memory cells, immediate, short-lived.', '[2]')])
explain(t, [('Describe how monoclonal antibodies are produced.', 'Inject a mouse with the antigen; extract B cells / plasma cells from spleen; fuse with myeloma cells to form hybridomas; select the hybridoma making the required antibody; culture it (cloned) to produce large amounts of identical antibody.', '[4]'),
            ('Explain why vaccines often need booster injections.', 'A second dose triggers a secondary response, producing more memory cells and a higher, longer-lasting antibody level.', '[2]'),
            ('Explain how monoclonal antibodies can be used to diagnose a disease.', 'They bind specifically to an antigen of the pathogen (or a marker molecule); linked to a dye / enzyme, they show whether the antigen is present (e.g. test strips).', '[3]')])
myths(t, [('Vaccines contain antibodies that fight the disease.', 'Most vaccines contain antigens that stimulate the body to make its own antibodies and memory cells.'), ('Passive immunity gives lifelong protection.', 'Passive immunity is short-lived because no memory cells are made.')])


@t.add('C4', (3, 4, 5), 'multi_step')
def mab_case(r, D):
    use = r.choice([('a home pregnancy test that detects hCG in urine', 'diagnosis'), ('trastuzumab (Herceptin), which binds to HER2 receptors on breast cancer cells', 'treatment'), ('a rapid test strip for malaria antigens in blood', 'diagnosis'), ('a test that detects the antigens of SARS-CoV-2 in a nasal swab', 'diagnosis')])
    intro = f'A biotechnology company in {city(r)} produces monoclonal antibodies for {use[0]}.'
    parts = [lambda r: ('Outline how the monoclonal antibodies are produced.', 'Mouse injected with antigen; plasma (B) cells collected from spleen; fused with myeloma cells → hybridomas; select hybridoma producing correct antibody; clone and culture; harvest antibody.', '[4]'),
             lambda r: ('Explain why the antibodies bind only to the target molecule.', 'All are identical with the same variable region, complementary to one specific antigen / epitope.', '[2]'),
             lambda r: (f'Explain how the antibodies are used in {use[1]}.', 'Antibodies attached to a dye / enzyme bind the antigen if present, producing a visible signal.' if use[1] == 'diagnosis' else 'They bind to the receptors on cancer cells, blocking growth signals and marking the cells for destruction by the immune system.', '[2]'),
             lambda r: ('Suggest one problem with using mouse antibodies to treat humans.', 'They are recognised as foreign (non-self) antigens and trigger an immune response; so they are "humanised".', '[2]'),
             lambda r: ('Compare the protection given by vaccination with that given by an injection of antibodies.', 'Vaccination: active, memory cells, long-lasting but slow to develop. Antibody injection: passive, immediate, short-lived, no memory.', '[3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def vacc_case(r, D):
    v = r.choice([('measles', 'attenuated (weakened) live virus'), ('polio (oral vaccine)', 'attenuated live virus'), ('tetanus', 'toxoid (inactivated toxin)'), ('COVID-19', 'mRNA coding for the spike protein'), ('cholera', 'killed bacteria')])
    intro = f'A vaccination campaign in {city(r)} uses a {v[0]} vaccine containing {v[1]}.'
    parts = [lambda r: ('Explain how the vaccine gives long-term protection.', 'Antigens stimulate B and T cells with complementary receptors; clonal selection and expansion; plasma cells make antibodies; memory cells remain and give a fast secondary response on infection.', '[4]'),
             lambda r: ('State the type of immunity produced.', 'Artificial active immunity.', '[1]'),
             lambda r: ('Explain why the vaccine does not cause the disease.', 'The pathogen is weakened / killed / only an antigen or toxoid is present, so it cannot reproduce or cause harm but still has the antigens.', '[2]'),
             lambda r: ('Explain why it is important that a high percentage of the population is vaccinated.', 'Herd immunity: too few susceptible people for the pathogen to spread, protecting those who cannot be vaccinated.', '[2]'),
             lambda r: ('Suggest one reason why some vaccines need a second dose.', 'Booster triggers a secondary response, increasing memory cells and antibody levels.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Distinguish between active and passive immunity and between natural and artificial immunity, and describe the production and uses of monoclonal antibodies.', 'Four types with examples; memory cells vs none; duration; vaccines; monoclonal production (immunise mouse, plasma cells, myeloma fusion, hybridoma, cloning); uses in diagnosis (pregnancy tests) and treatment (cancer).',
           'active vs passive [2]; natural vs artificial with examples [2]; monoclonal production [2]; uses [1] [7]')])
t11d = t
CHAPTERS[11] = [t11a, t11b, t11c, t11d]


# ===================================================================== Paper 1-style application MCQs (C2)
P1 = [
    (t1a, [('A student increases the magnification of a light microscope from ×400 to ×1000 but sees no more detail of a mitochondrion. Which explains this?', 'The resolution of the light microscope is limited by the wavelength of light', 'Magnification beyond the resolution limit gives no extra detail.', ['The mitochondrion is too large to be seen at ×1000', 'The eyepiece graticule has not been calibrated', 'Mitochondria are only visible in living cells']),
          ('With a ×10 objective, one eyepiece division = 10 μm. What is the value of one division with a ×40 objective?', '2.5 μm', 'Four times the magnification → each division represents a quarter of the length.', ['40 μm', '10 μm', '0.25 μm'])]),
    (t1b, [('Cells of an organ contain large amounts of rough endoplasmic reticulum and Golgi body. What is the main function of these cells?', 'Secretion of proteins', 'RER makes proteins, Golgi packages them for secretion.', ['Storage of lipids', 'Contraction', 'Detoxification of steroids']),
          ('A drug stops lysosomes forming. Which process would be affected first in a macrophage?', 'Digestion of engulfed bacteria', 'Lysosomes supply hydrolytic enzymes to phagosomes.', ['Synthesis of proteins', 'Aerobic respiration', 'Replication of DNA'])]),
    (t2b, [('A molecule is made of β-glucose joined by 1,4 glycosidic bonds with every other glucose inverted. What is its main property?', 'High tensile strength from hydrogen-bonded parallel chains', 'Cellulose forms microfibrils.', ['Rapid hydrolysis from many branches', 'Compact helical storage', 'Solubility in water'])]),
    (t2d, [('An amino acid with a non-polar R group is replaced by one with a charged R group inside a globular protein. What is the most likely effect?', 'The tertiary structure changes because different bonds form between R groups', 'Ionic bonds may form instead of hydrophobic interactions.', ['The number of peptide bonds changes', 'The protein becomes fibrous', 'The primary structure is unchanged'])]),
    (t3b, [('An enzyme reaction rate doubles between 20 °C and 30 °C. What is the Q10?', '2', 'Q10 = rate at (T + 10) ÷ rate at T.', ['0.5', '10', '20']),
          ('Which change would increase the initial rate of an enzyme reaction when substrate concentration is limiting?', 'Increasing the substrate concentration', 'Below saturation, substrate limits the rate.', ['Adding a non-competitive inhibitor', 'Lowering the temperature to 5 °C', 'Changing the pH away from the optimum'])]),
    (t3c, [('Adding more substrate restores the rate of an inhibited enzyme reaction to Vmax. Which type of inhibitor is present?', 'Competitive', 'Competitive inhibition is overcome by high substrate concentration.', ['Non-competitive', 'Irreversible heavy-metal ion', 'Allosteric non-competitive'])]),
    (t4c, [('Cell X has ψ = −400 kPa and cell Y has ψ = −700 kPa. Which statement is correct?', 'Water moves from X to Y by osmosis', 'Water moves from higher (less negative) to lower water potential.', ['Water moves from Y to X by osmosis', 'There is no net movement of water', 'Solutes move from X to Y by osmosis']),
          ('A potato cylinder gains mass in a sucrose solution. What can be concluded?', 'The water potential of the solution was higher than that of the potato cells', 'Water entered by osmosis.', ['The solution was more concentrated than the cell sap', 'Sucrose entered by active transport', 'The cells were plasmolysed'])]),
    (t4d, [('A cube of side 3 cm is cut into 27 cubes of side 1 cm. What happens to the total surface area to volume ratio?', 'It increases from 2 : 1 to 6 : 1', 'SA:V = 6/L.', ['It decreases from 6 : 1 to 2 : 1', 'It stays at 6 : 1', 'It increases from 3 : 1 to 9 : 1'])]),
    (t5b, [('A cell has 12 chromosomes in G1. How many chromatids are present at metaphase of mitosis?', '24', 'Each of 12 chromosomes has two chromatids after S phase.', ['12', '6', '48'])]),
    (t6a, [('DNA from a bacterium contains 32% guanine. What percentage of its bases is thymine?', '18%', 'G = C = 32%; A + T = 36%; T = 18%.', ['32%', '36%', '68%'])]),
    (t6c, [('A tRNA molecule has the anticodon UAC. Which DNA template-strand triplet corresponds to the codon it binds?', 'TAC', 'Codon AUG; template TAC.', ['ATG', 'UAC', 'AUG'])]),
    (t6b, [('E. coli with only ¹⁵N DNA is grown in ¹⁴N for two generations. What fraction of DNA molecules is hybrid?', 'One half', 'Two of four molecules are hybrid.', ['One quarter', 'All', 'None'])]),
    (t7b, [('Which change would increase the rate of water uptake measured by a potometer?', 'Moving the shoot into moving air', 'Wind removes water vapour, steepening the ψ gradient.', ['Covering the leaves with petroleum jelly', 'Placing a clear plastic bag over the shoot', 'Moving the shoot into the dark'])]),
    (t7d, [('Which process creates the high hydrostatic pressure at the source end of a sieve tube?', 'Water entering by osmosis after sucrose is actively loaded', 'Loading lowers ψ.', ['Transpiration pull from the leaves', 'Active transport of water into sieve tubes', 'Root pressure from the roots'])]),
    (t8b, [('During exercise, the oxygen dissociation curve of haemoglobin shifts to the right. Which explains this?', 'Higher carbon dioxide concentration lowers the affinity of haemoglobin for oxygen', 'Bohr shift.', ['Higher oxygen concentration in the muscles', 'Less carbonic anhydrase in red cells', 'Haemoglobin binds carbon dioxide at the haem group'])]),
    (t8c, [('A heart has a stroke volume of 70 cm³ and a cardiac output of 5.6 dm³ min⁻¹. What is the heart rate?', '80 beats min⁻¹', '5600 ÷ 70 = 80.', ['70 beats min⁻¹', '0.0125 beats min⁻¹', '392 beats min⁻¹'])]),
    (t8d, [('The R–R interval on an ECG recorded at 25 mm s⁻¹ is 20 mm. What is the heart rate?', '75 beats min⁻¹', '20 ÷ 25 = 0.8 s; 60 ÷ 0.8 = 75.', ['80 beats min⁻¹', '50 beats min⁻¹', '125 beats min⁻¹'])]),
    (t9b, [('The thickness of the alveolar wall doubles while surface area and concentration difference stay the same. What happens to the rate of diffusion?', 'It halves', "Fick's law: rate ∝ 1/thickness.", ['It doubles', 'It quarters', 'It stays the same'])]),
    (t10a, [('Which pair shows a disease and its correct method of transmission?', 'Tuberculosis – droplets in the air', 'TB is airborne; cholera is faecal–oral; malaria is vector-borne.', ['Cholera – mosquito bites', 'Malaria – contaminated water', 'HIV – droplets in the air'])]),
    (t10c, [('Why does the number of resistant bacteria increase when an antibiotic is used frequently?', 'The antibiotic kills susceptible bacteria, so resistant bacteria survive and reproduce', 'Natural selection.', ['The antibiotic causes mutations for resistance', 'Bacteria learn to break down the antibiotic', 'Patients become immune to the antibiotic'])]),
    (t11b, [('After a second exposure to the same antigen, antibody is produced faster and in greater quantity. Which cells are responsible?', 'Memory B cells', 'Memory cells give the secondary response.', ['Neutrophils', 'Red blood cells', 'Macrophages only'])]),
    (t11d, [('A person is given an injection of antibodies against rabies after a bite. What type of immunity results?', 'Artificial passive', 'Ready-made antibodies; no memory cells.', ['Artificial active', 'Natural passive', 'Natural active'])]),
]
for _t, _e in P1:
    mcqs(_t, _e, D=(2, 3), C='C2')


# ===================================================================== marking-key enrichment
# Some part keys above give only a mark total ("[2]"). Turn every bare total into explicit mark
# points taken from the model answer, so each key lists what earns each mark.
import re as _re  # noqa: E402

_BARE = _re.compile(r'^\s*(?:any (?:one|two|three|four|five|six)[^\[;]*)?\[(\d+)\]\s*$')
_LAB = _re.compile(r'\((?:[a-h]|i{1,3}|iv)\) ')


def _chunks(ans, n):
    parts = [p.strip(' .') for p in _re.split(r';\s+|\.\s+(?=[A-Z])', ans) if p.strip(' .')]
    if len(parts) < n:
        more = []
        for p in parts:
            more.extend(x.strip(' .') for x in _re.split(r',\s+|\s+→\s+', p) if x.strip(' .'))
        if len(more) > len(parts):
            parts = more
    return parts


def mark_points(ans, n):
    ps = _chunks(ans, n)
    if not ps:
        return f'{ans} [{n}]'
    if n == 1:
        return f'{"; ".join(ps)} [1]'
    if len(ps) > n:
        return f'any {n} from: ' + '; '.join(ps) + f' (1 mark each) [{n}]'
    k = len(ps)
    each = [n // k + (1 if i < n % k else 0) for i in range(k)]
    return '; '.join(f'{p} [{m}]' for p, m in zip(ps, each)) + f' [{n}]'


def _split_labels(s):
    idx = [m.start() for m in _LAB.finditer(s)]
    if not idx or idx[0] != 0 and not s[:idx[0]].strip() == '':
        return None
    out = []
    for i, a in enumerate(idx):
        b = idx[i + 1] if i + 1 < len(idx) else len(s)
        lab = s[a:s.index(')', a) + 1]
        out.append((lab, s[s.index(')', a) + 2:b].strip()))
    return out


def enrich(ans, key):
    m = _BARE.match(key)
    if m:
        return mark_points(ans, int(m.group(1)))
    kp, ap = _split_labels(key), _split_labels(ans)
    if not kp or not ap or len(kp) != len(ap) or any(k[0] != a[0] for k, a in zip(kp, ap)):
        return key
    if not any(_BARE.match(k[1]) for k in kp):
        return key
    return ' '.join(f'{lab} ' + (mark_points(a[1], int(_BARE.match(k).group(1))) if _BARE.match(k) else k) for (lab, k), a in zip(kp, ap))


_NEG = _re.compile(r'(?<![\w)\]′])-(?=\d)')


def _minus(x):
    return _NEG.sub('−', x)


def _wrap(fn):
    def g(r, D):
        q = fn(r, D)
        if q and not q.get('options'):
            q['key'] = enrich(q['answer'], q['key'])
        if q:
            for f_ in ('stem', 'answer', 'key'):
                q[f_] = _minus(q[f_])
            if q.get('options'):
                q['options'] = [_minus(o) for o in q['options']]
        return q
    g.__name__ = getattr(fn, '__name__', 'tpl')
    return g


for _tps in CHAPTERS.values():
    for _t in _tps:
        for _tp in _t.templates:
            _tp.fn = _wrap(_tp.fn)
        for _C, _ents in getattr(_t, 'entries', {}).items():
            _t.entries[_C] = [((e[0], e[1], enrich(e[1], e[2])) + tuple(e[3:]), d) for e, d in _ents]
