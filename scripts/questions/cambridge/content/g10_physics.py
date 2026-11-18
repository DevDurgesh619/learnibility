"""Cambridge IGCSE Physics 0625 (2026-28), coursebook chapters 14-25 (grade 10)."""
import math
from ._lib import topic, mcq, sf, sci, sup, person, two_people, city, near, num_mcq

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

# =========================================================== 1 Waves
t1 = topic('General properties of waves', 'general wave properties', 'transverse longitudinal', 'wave motion', 'properties of waves')
t1.fixed('C1', (1, 2), [
    ('Which statement describes what a wave transfers?', 'Energy, without transferring matter', 'A wave transfers energy from one place to another; the particles of the medium only oscillate about fixed positions.',
     ['Matter, without transferring energy', 'Both matter and energy', 'Neither matter nor energy, only momentum']),
    ('In a transverse wave, how do the particles of the medium vibrate?', 'At right angles to the direction of energy transfer', 'Transverse: oscillation perpendicular to the direction of travel of the wave (e.g. light, water ripples).',
     ['Parallel to the direction of energy transfer', 'In circles around the direction of travel', 'They do not vibrate at all']),
    ('Which of these is a longitudinal wave?', 'Sound wave in air', 'Sound is longitudinal: the air particles oscillate parallel to the direction of travel, forming compressions and rarefactions.',
     ['Light wave', 'Ripple on a water surface', 'Microwave']),
    ('What is the amplitude of a wave?', 'The maximum displacement of a point from its rest position', 'Amplitude = maximum displacement from the undisturbed (rest) position, measured from the centre line to a crest.',
     ['The distance from a crest to the next crest', 'The number of waves passing a point each second', 'The distance from a crest to a trough']),
    ('What name is given to the regions of a longitudinal wave where the particles are closest together?', 'Compressions', 'Compressions: particles crowded together (higher pressure); rarefactions: particles spread out.',
     ['Rarefactions', 'Crests', 'Wavefronts']),
    ('What is the unit of frequency?', 'hertz (Hz)', 'Frequency is the number of waves per second; 1 Hz = 1 wave per second.',
     ['metre (m)', 'second (s)', 'metre per second (m/s)']),
    ('Define the wavelength of a wave.', 'The distance between two neighbouring points in phase, e.g. crest to crest.', '1 mark: distance between a point and the next identical point on the wave (crest to adjacent crest or compression to adjacent compression).'),
    ('State what is meant by a wavefront.', 'A line joining neighbouring points on a wave that are in phase (e.g. all along one crest).', '1 mark: line joining points in phase / along one crest; wavefronts are drawn one wavelength apart.'),
])
t1.fixed('C2', (2, 3), [
    ('A cork floats on a pond as ripples pass it. Explain why the cork bobs up and down but does not move towards the bank.', 'Water waves are transverse and transfer energy, not water; the water (and cork) only oscillates up and down about a fixed position.', '1 mark: wave transfers energy not matter; 1 mark: water/cork oscillates about a fixed position (perpendicular to wave travel).'),
    ('Explain the difference between a transverse and a longitudinal wave, giving one example of each.', 'Transverse: vibrations at right angles to energy transfer (e.g. light, water ripples). Longitudinal: vibrations parallel to energy transfer (e.g. sound).', '1 mark each for the two directions; 1 mark for one correct example of each.'),
    ('Explain why sound cannot travel through a vacuum but light can.', 'Sound is a mechanical wave that needs particles to pass vibrations along; light is an electromagnetic wave that needs no medium.', '1 mark: sound needs a medium (particles to vibrate); 1 mark: light is EM, does not need a medium.'),
    ('A slinky spring is pushed and pulled along its length. Describe the wave produced and how its compressions move.', 'A longitudinal wave: coils oscillate along the length; compressions and rarefactions travel along the spring while each coil returns to its rest position.', '1 mark: longitudinal; 1 mark: compressions/rarefactions move along, coils oscillate about rest positions.'),
    ('Explain in one line why a wave with a larger amplitude carries more energy.', 'The particles are displaced further from rest, so more energy is needed to produce and is carried by the oscillation.', '1 mark: larger displacement of particles means more energy transferred.'),
])


@t1.add('C2', (2, 3, 4), 'explain')
def t1_compare(r, D):
    f1, f2 = r.sample([2, 4, 5, 8, 10, 20, 25, 40, 50], 2)
    med = r.choice(['ripple tank', 'stretched spring', 'rope'])
    return {'stem': f'Two waves travel along the same {med} at the same speed. Wave P has frequency {f1} Hz and wave Q has frequency {f2} Hz. Without calculating, state which wave has the longer wavelength and explain why.',
            'answer': f"Wave {'P' if f1 < f2 else 'Q'} (the lower frequency). Since v = fλ and v is the same, λ is inversely proportional to f.",
            'key': '1 mark: correct wave; 1 mark: same speed so λ ∝ 1/f (v = fλ).'}


@t1.add('C3', (1, 2, 3))
def t1_period(r, D):
    f = r.choice([2, 4, 5, 8, 10, 20, 25, 50, 100, 250, 500]) if D < 3 else r.choice([0.5, 1.25, 2.5, 12.5, 40, 125, 400, 800])
    T = 1 / f
    if D == 1:
        opts, ans = num_mcq(r, T, [f, 2 * T, T / 2, 1 / (2 * f) if f != 0.5 else 4], unit=' s')
        return {'stem': f'A wave has a frequency of {sf(f)} Hz. What is its period?', 'options': opts, 'answer': ans, 'key': f'T = 1/f = 1/{sf(f)} = {sf(T)} s.'}
    return {'stem': f'A wave has a frequency of {sf(f)} Hz. Calculate its period, giving the unit.', 'answer': f'{sf(T)} s', 'key': f'T = 1/f (1 mark) = 1/{sf(f)} = {sf(T)} s (1 mark).'}


@t1.add('C3', (2, 3, 4))
def t1_count(r, D):
    n = r.choice([12, 15, 18, 24, 30, 36, 45, 60])
    t = r.choice([3, 4, 5, 6, 10, 12])
    d = r.choice([0.6, 0.9, 1.2, 1.5, 1.8, 2.4])
    waves = r.choice([3, 4, 5, 6])
    f = n / t
    lam = d / waves
    v = f * lam
    return {'stem': f'In a ripple tank, {n} waves pass a point in {t} s. A student measures the distance across {waves + 1} neighbouring crests as {sf(d)} m. Calculate (a) the frequency, (b) the wavelength and (c) the speed of the waves.',
            'answer': f'(a) {sf(f)} Hz (b) {sf(lam)} m (c) {sf(v)} m/s',
            'key': f'(a) f = {n}/{t} = {sf(f)} Hz; (b) {waves + 1} crests span {waves} wavelengths so λ = {sf(d)}/{waves} = {sf(lam)} m; (c) v = fλ = {sf(f)} × {sf(lam)} = {sf(v)} m/s. Common error: dividing by {waves + 1}.',
            'type': 'multi_step'}


t2 = topic('The wave equation', 'wave equation', 'speed frequency wavelength', 'v = fλ')
t2.fixed('C1', (1, 2), [
    ('Which equation links wave speed v, frequency f and wavelength λ?', 'v = fλ', 'Wave equation: speed = frequency × wavelength.', ['v = f/λ', 'v = λ/f', 'f = vλ']),
    ('If the frequency of a wave doubles and its speed stays the same, what happens to its wavelength?', 'It halves', 'v = fλ with v constant, so λ ∝ 1/f; doubling f halves λ.', ['It doubles', 'It stays the same', 'It quadruples']),
    ('A wave passes from deep to shallow water. Which quantity stays the same?', 'Frequency', 'Frequency is set by the source and does not change on refraction; speed and wavelength both decrease in shallow water.', ['Speed', 'Wavelength', 'Direction']),
])


@t2.add('C3', (1, 2, 3, 4))
def t2_speed(r, D):
    kinds = [('sound wave in air', 340, (20, 20000)), ('water wave', None, (0.5, 5)), ('wave on a string', None, (50, 400))]
    k = r.choice(['speed', 'wavelength', 'frequency'])
    if D <= 2:
        f = r.choice([2, 4, 5, 10, 20, 25, 50, 200, 250, 500, 680, 850, 1700])
        lam = r.choice([0.2, 0.4, 0.5, 0.8, 1.5, 2.0, 2.5, 3.0])
    else:
        f = r.choice([256, 330, 440, 512, 1.6, 3.2, 12.5, 7.5e3])
        lam = r.choice([0.034, 0.75, 1.32, 0.0125, 4.5, 0.66, 0.045])
    v = f * lam
    if k == 'speed':
        stem, ans, key = f'A wave has frequency {sf(f)} Hz and wavelength {sf(lam)} m. Calculate its speed.', f'{sf(v)} m/s', f'v = fλ = {sf(f)} × {sf(lam)} = {sf(v)} m/s.'
    elif k == 'wavelength':
        stem, ans, key = f'A wave travels at {sf(v)} m/s with a frequency of {sf(f)} Hz. Calculate its wavelength.', f'{sf(lam)} m', f'λ = v/f = {sf(v)}/{sf(f)} = {sf(lam)} m.'
    else:
        stem, ans, key = f'A wave of wavelength {sf(lam)} m travels at {sf(v)} m/s. Calculate its frequency.', f'{sf(f)} Hz', f'f = v/λ = {sf(v)}/{sf(lam)} = {sf(f)} Hz.'
    if D == 1:
        opts, a = mcq(r, ans, near(r, float(ans.split()[0].replace(',', '')), fmtf=lambda x: sf(x) + ' ' + ans.split()[1]))
        return {'stem': stem.replace('Calculate', 'What is'), 'options': opts, 'answer': a, 'key': key}
    return {'stem': stem, 'answer': ans, 'key': key + ' (1 mark equation/substitution, 1 mark answer with unit)'}


@t2.add('C3', (3, 4), 'numerical')
def t2_units(r, D):
    f_khz = r.choice([1.5, 2.0, 2.5, 3.4, 5.0, 6.8, 8.5])
    v = r.choice([340, 330, 1500, 1480])
    medium = 'air' if v < 400 else 'sea water'
    lam = v / (f_khz * 1000)
    return {'stem': f'A {"loudspeaker" if v < 400 else "sonar transmitter"} produces sound of frequency {sf(f_khz)} kHz in {medium}, where sound travels at {v} m/s. Calculate the wavelength in cm.',
            'answer': f'{sf(lam * 100)} cm', 'key': f'f = {sf(f_khz)} × 10³ Hz; λ = v/f = {v}/{sf(f_khz * 1000)} = {sf(lam)} m = {sf(lam * 100)} cm. Unit conversion kHz → Hz is the usual error.'}


@t2.add('C4', (3, 4, 5), 'multi_step')
def t2_refraction(r, D):
    f = r.choice([4, 5, 6, 8, 10, 12])
    l1 = r.choice([3.0, 2.5, 2.0, 4.0, 3.5])
    ratio = r.choice([0.5, 0.6, 0.75, 0.8])
    v1 = f * l1 / 100
    v2 = v1 * ratio
    l2 = l1 * ratio
    return {'stem': f'A ripple tank vibrator runs at {f} Hz. In the deep region the wavelength is {sf(l1)} cm. The waves cross into a shallow region where their speed falls to {sf(v2)} m/s. (a) Calculate the speed in the deep region. (b) Calculate the wavelength in the shallow region. (c) Explain what happens to the direction of the waves if they meet the boundary at an angle.',
            'answer': f'(a) {sf(v1)} m/s (b) {sf(l2)} cm (c) They refract towards the normal because they slow down.',
            'key': f'(a) v = fλ = {f} × {sf(l1 / 100)} = {sf(v1)} m/s [2]; (b) f unchanged = {f} Hz, λ = {sf(v2)}/{f} = {sf(l2 / 100)} m = {sf(l2)} cm [2]; (c) wave slows, bends towards the normal [1].'}


@t2.add('C2', (2, 3, 4), 'explain')
def t2_claim(r, D):
    f = r.choice([200, 400, 500, 800, 1000])
    return {'stem': f'{person(r)} says: "If I make a sound of frequency {2 * f} Hz instead of {f} Hz, it will travel twice as fast because v = fλ." Explain why this is wrong.',
            'answer': 'Wave speed depends on the medium, not on the frequency. Doubling f halves λ, so v stays the same.',
            'key': '1 mark: speed set by medium; 1 mark: λ halves so fλ is unchanged.'}


t3 = topic('Reflection, refraction and diffraction of waves', 'reflection refraction diffraction', 'diffraction', 'ripple tank behaviour')
t3.fixed('C1', (1, 2), [
    ('What happens to the wavelength of water waves when they diffract through a gap?', 'It stays the same', 'Diffraction changes the direction/spreading, not the speed, frequency or wavelength.', ['It increases', 'It decreases', 'It becomes zero']),
    ('Diffraction is greatest when the gap width is', 'about the same as the wavelength', 'Spreading is most noticeable when gap ≈ λ.', ['much larger than the wavelength', 'twice the amplitude', 'much smaller than the amplitude']),
    ('When a plane water wave reflects off a straight barrier, which is true?', 'The angle of incidence equals the angle of reflection', 'Law of reflection: i = r, measured from the normal; λ and f are unchanged.', ['The wavelength doubles', 'The frequency halves', 'The wave speed increases']),
    ('Why do water waves refract when they enter shallower water?', 'Their speed changes', 'Waves slow down in shallow water; the change of speed at an angle changes direction.', ['Their frequency changes', 'Their amplitude changes', 'They lose all their energy']),
])
t3.fixed('C2', (2, 3), [
    ('Explain why you can hear someone talking in the next room through an open doorway even though you cannot see them.', 'Sound wavelengths (about 0.3 m to 3 m) are similar to the width of a doorway so sound diffracts strongly; light wavelengths are far smaller, so light hardly diffracts.', '1 mark: diffraction of sound; 1 mark: comparison of wavelength with gap size for sound vs light.'),
    ('Explain why long-wave radio signals can be received behind hills but signals of much shorter wavelength often cannot.', 'Long-wave radio has wavelengths comparable to the size of hills, so it diffracts around them; short wavelengths diffract very little.', '1 mark: diffraction around obstacles; 1 mark: long λ diffracts more.'),
    ('Describe how wavefronts change when plane waves pass through a gap much wider than their wavelength.', 'They pass straight through with only slight curving at the edges; the wavelength is unchanged.', '1 mark: little spreading (edges only); 1 mark: same wavelength.'),
    ('Explain why the wavefronts get closer together when water waves move into a shallow region.', 'The waves slow down but the frequency stays the same, so λ = v/f decreases.', '1 mark: speed decreases; 1 mark: f constant so λ decreases.'),
    ('A harbour wall has a narrow entrance. Explain why boats moored just inside the wall, out of line with the entrance, still rock.', 'Waves diffract as they pass through the entrance and spread into the region behind the wall.', '1 mark: diffraction at gap; 1 mark: spreading reaches the shadow region.'),
])


@t3.add('C3', (2, 3, 4), 'explain')
def t3_gap(r, D):
    lam = r.choice([1.0, 1.5, 2.0, 2.5, 3.0])
    g1 = lam * r.choice([1, 1.2])
    g2 = lam * r.choice([5, 6, 8, 10])
    return {'stem': f'Water waves of wavelength {sf(lam)} cm approach two gaps: gap A is {sf(g1)} cm wide and gap B is {sf(g2)} cm wide. Sketch-describe the wavefronts beyond each gap and state which shows more diffraction.',
            'answer': 'Gap A: wavefronts spread out as near-semicircles; gap B: wavefronts mostly straight with slight curving at the edges. Gap A shows more diffraction; wavelength unchanged in both.',
            'key': '1 mark: A spreads (curved); 1 mark: B mainly straight; 1 mark: same wavelength drawn/stated.'}


@t3.add('C4', (3, 4), 'case')
def t3_harbour(r, D):
    lam = r.choice([8, 10, 12, 15, 20])
    return {'stem': f'Engineers in {city(r)} are designing a harbour where incoming ocean waves have a wavelength of about {lam} m. Two entrance widths are proposed: {lam} m and {lam * 6} m. Using ideas about diffraction, evaluate which entrance would give calmer water for boats moored to one side of the entrance.',
            'answer': f'The {lam * 6} m entrance: when the gap is much larger than λ the waves diffract little, so less wave energy spreads to the sides. A {lam} m gap would spread waves widely into the harbour (though it lets in less energy overall).',
            'key': '1 mark: diffraction greatest when gap ≈ λ; 1 mark: wide gap gives little spreading to the side; 1 mark: balanced point (narrow gap admits less energy but spreads it); 1 mark: clear conclusion.'}


@t3.add('C3', (2, 3), 'numerical')
def t3_reflect(r, D):
    ang = r.choice([20, 25, 30, 35, 40, 50, 55, 60])
    return {'stem': f'Plane water waves strike a straight barrier. The wavefronts make an angle of {ang}° with the barrier. State the angle of incidence (from the normal) and the angle that the reflected wavefronts make with the barrier.',
            'answer': f'Angle of incidence = {ang}°; reflected wavefronts also make {ang}° with the barrier.',
            'key': f'The angle between wavefront and barrier equals the angle between ray and normal, so i = {ang}° [1]; i = r so reflected wavefronts at {ang}° [1].'}


CHAPTERS[1] = [t1, t2, t3]

# =========================================================== 2 Electromagnetic spectrum
EM = ['radio waves', 'microwaves', 'infrared', 'visible light', 'ultraviolet', 'X-rays', 'gamma rays']
USES = [
    ('radio waves', 'radio and television transmissions', 'long wavelength diffracts around hills and buildings and reflects off the ionosphere for long-distance broadcasting'),
    ('radio waves', 'astronomy and RFID tags', 'they pass through dust clouds and can carry coded signals over short and long ranges'),
    ('microwaves', 'satellite television and mobile phones', 'they pass through the atmosphere and can be focused into narrow beams'),
    ('microwaves', 'cooking food in a microwave oven', 'they are absorbed by water molecules in food, which heats up'),
    ('infrared', 'remote controls for televisions', 'low energy and short range, easily produced by an LED'),
    ('infrared', 'thermal imaging cameras', 'all warm objects emit infrared, more from hotter objects'),
    ('infrared', 'optical fibres for broadband', 'it travels along glass fibres by total internal reflection with little absorption'),
    ('visible light', 'photography and vision', 'it is detected by the eye and by camera sensors'),
    ('ultraviolet', 'detecting forged banknotes', 'it makes fluorescent security ink glow'),
    ('ultraviolet', 'sterilising water', 'high-energy photons kill bacteria'),
    ('X-rays', 'medical imaging of bones', 'they pass through soft tissue but are absorbed by dense bone'),
    ('X-rays', 'airport security scanners', 'they penetrate bags but are absorbed by dense metal objects'),
    ('gamma rays', 'sterilising medical equipment', 'high energy kills microorganisms even through packaging'),
    ('gamma rays', 'treating cancer (radiotherapy)', 'a focused beam delivers enough energy to kill cancer cells'),
]
HAZ = [
    ('microwaves', 'internal heating of body cells'), ('infrared', 'skin burns'), ('ultraviolet', 'damage to surface cells and eyes, leading to skin cancer and eye conditions'),
    ('X-rays', 'mutation or damage to cells, leading to cancer'), ('gamma rays', 'mutation or damage to cells, leading to cancer'),
]
t4 = topic('Regions and properties of the electromagnetic spectrum', 'electromagnetic spectrum', 'properties of electromagnetic waves', 'regions')
t4.fixed('C1', (1, 2), [
    ('What is the speed of all electromagnetic waves in a vacuum?', '3.0 × 10⁸ m/s', 'All EM waves travel at 3.0 × 10⁸ m/s in a vacuum (and approximately in air).', ['3.4 × 10² m/s', '3.0 × 10⁶ m/s', '1.5 × 10⁸ m/s']),
    ('Which list is in order of increasing frequency?', 'radio, microwave, infrared, visible', 'Frequency increases from radio to gamma; wavelength decreases.', ['visible, infrared, microwave, radio', 'X-ray, ultraviolet, visible, infrared', 'microwave, radio, visible, infrared']),
    ('Which electromagnetic radiation has the longest wavelength?', 'Radio waves', 'Radio waves have the longest wavelength (up to km) and lowest frequency.', ['Gamma rays', 'Infrared', 'Ultraviolet']),
    ('Which region lies between visible light and X-rays in the spectrum?', 'Ultraviolet', 'Order: ... visible, ultraviolet, X-rays, gamma.', ['Infrared', 'Microwaves', 'Radio waves']),
    ('Electromagnetic waves are', 'transverse waves that can travel through a vacuum', 'All EM waves are transverse and need no medium.', ['longitudinal waves that need a medium', 'transverse waves that need a medium', 'longitudinal waves that travel through a vacuum']),
])


@t4.add('C1', (1, 2, 3))
def t4_order(r, D):
    a, b = sorted(r.sample(range(len(EM)), 2))
    q = r.choice(['frequency', 'wavelength'])
    hi = EM[b] if q == 'frequency' else EM[a]
    opts, ans = mcq(r, hi, [e for e in EM if e != hi])
    return {'stem': f'Which has the higher {q}: {EM[a]} or {EM[b]}?', 'options': opts, 'answer': ans, 'key': f'Order of increasing frequency (decreasing wavelength): {", ".join(EM)}. So {hi} has the higher {q}.'}


@t4.add('C2', (2, 3), 'explain')
def t4_same(r, D):
    a, b = r.sample(EM, 2)
    return {'stem': f'State two properties that {a} and {b} have in common, and one way in which they differ.',
            'answer': f'Both are transverse, travel at 3.0 × 10⁸ m/s in a vacuum and can travel through a vacuum (any two). They differ in wavelength/frequency (and energy).',
            'key': '1 mark each for two shared properties (transverse; same speed in vacuum; no medium needed; can be reflected/refracted); 1 mark: different wavelength/frequency.'}


@t4.add('C3', (2, 3, 4), 'numerical')
def t4_calc(r, D):
    reg = r.choice([('radio', 1e5, 1e8, 'Hz'), ('microwave', 1e9, 3e10, 'Hz'), ('infrared', 1e12, 3e14, 'Hz'), ('X-ray', 1e17, 1e19, 'Hz')])
    f = reg[1] * r.choice([1.5, 2, 2.5, 3, 4, 5, 6, 7.5])
    lam = 3e8 / f
    return {'stem': f'A {reg[0]} signal has a frequency of {sci(f, 2)} Hz. Calculate its wavelength in a vacuum (speed of light = 3.0 × 10⁸ m/s).',
            'answer': f'{sci(lam, 2)} m', 'key': f'λ = c/f = 3.0 × 10⁸ / {sci(f, 2)} = {sci(lam, 2)} m [2].'}


@t4.add('C3', (1, 2), 'numerical')
def t4_radio(r, D):
    stn = r.choice([88.5, 91.1, 94.3, 97.7, 100.0, 102.4, 105.0])
    lam = 3e8 / (stn * 1e6)
    opts, ans = num_mcq(r, lam, [lam * 10, lam / 10, stn / 3, 3e8 / stn], unit=' m')
    return {'stem': f'An FM radio station broadcasts at {stn} MHz. What is the wavelength of the signal?', 'options': opts, 'answer': ans,
            'key': f'λ = 3.0 × 10⁸ / ({stn} × 10⁶) = {sf(lam)} m.'}


t5 = topic('Uses and hazards of electromagnetic waves', 'uses', 'hazards', 'dangers', 'harmful effects', 'safety precautions', 'applications of electromagnetic waves')


@t5.add('C1', (1, 2))
def t5_use(r, D):
    reg, use, why = r.choice(USES)
    opts, ans = mcq(r, reg, [e for e in EM if e != reg])
    return {'stem': f'Which type of electromagnetic radiation is used for {use}?', 'options': opts, 'answer': ans, 'key': f'{reg.capitalize()}: {why}.'}


@t5.add('C2', (2, 3), 'explain')
def t5_why(r, D):
    reg, use, why = r.choice(USES)
    return {'stem': f'Explain why {reg} are suitable for {use}.'.replace('visible light are', 'visible light is').replace('infrared are', 'infrared is').replace('ultraviolet are', 'ultraviolet is'),
            'answer': why[0].upper() + why[1:] + '.', 'key': f'1 mark: property ({why.split(",")[0]}); 1 mark: linked to the use.'}


@t5.add('C1', (1, 2, 3))
def t5_haz(r, D):
    reg, h = r.choice(HAZ)
    others = [x[1] for x in HAZ if x[1] != h] + ['no harmful effects at any intensity', 'turning bones transparent']
    opts, ans = mcq(r, h, others)
    return {'stem': f'Which is a harmful effect of excessive exposure to {reg}?', 'options': opts, 'answer': ans, 'key': f'{reg.capitalize()}: {h}.'}


@t5.add('C3', (2, 3, 4), 'case')
def t5_scenario(r, D):
    sc = r.choice([
        ('A hospital wants to check whether a patient has a broken wrist.', 'X-rays', 'pass through soft tissue but are absorbed by bone, so bone shows on the detector', 'minimise exposure; radiographer stands behind lead screen; patient wears lead apron'),
        ('A water company wants to kill bacteria in drinking water without adding chemicals.', 'ultraviolet', 'high-energy UV damages the DNA of bacteria', 'shield the lamps so workers’ skin and eyes are not exposed'),
        ('Firefighters need to find people inside a smoke-filled building.', 'infrared (thermal imaging)', 'warm bodies emit more infrared than surroundings and IR passes through smoke better than visible light', 'none significant at these intensities'),
        ('A company sends television signals from a satellite to homes across a continent.', 'microwaves', 'they pass through the atmosphere (ionosphere) and can be sent as a narrow beam to a dish', 'beam intensity at ground level is low'),
        ('A hospital needs to sterilise sealed plastic syringes.', 'gamma rays', 'very penetrating, so they kill microbes through the packaging without heating the plastic', 'source kept in thick lead/concrete shielding, handled remotely'),
        ('A bank wants staff to check whether notes are forged.', 'ultraviolet', 'genuine notes have security marks that fluoresce under UV', 'use low-intensity lamps and avoid looking into them'),
    ])
    return {'stem': f'{sc[0]} Suggest which electromagnetic radiation should be used, explain why it is suitable, and describe one safety precaution.',
            'answer': f'{sc[1]}: {sc[2]}. Precaution: {sc[3]}.', 'key': '1 mark: correct radiation; 1 mark: property linked to use; 1 mark: sensible precaution.'}


@t5.add('C4', (3, 4, 5), 'long')
def t5_eval(r, D):
    q = r.choice([
        ('Some people worry that using mobile phones (microwaves) is as dangerous as having X-rays. Evaluate this claim.', 'X-rays are ionising: high-frequency photons can damage DNA and cause cancer. Mobile-phone microwaves are non-ionising and low power; their main effect is slight heating of tissue. So the claim is not justified, though limiting exposure is sensible.'),
        ('A sunbed company claims that UV tanning is "a healthy source of vitamin D with no risks". Evaluate this claim using your knowledge of the electromagnetic spectrum.', 'UV does help skin make vitamin D, but UV is high-frequency and damages surface cells and eyes; repeated exposure raises skin-cancer risk and causes premature ageing. The "no risks" part is false; short sunlight exposure gives vitamin D more safely.'),
        ('A dentist takes more X-ray images than necessary "to be safe". Discuss the benefits and risks of this practice.', 'Benefit: better diagnosis of hidden decay. Risk: each X-ray dose is ionising and adds to the chance of cell mutation; doses should be as low as reasonably achievable, so only necessary images should be taken.'),
    ])
    return {'stem': q[0], 'answer': q[1], 'key': '1 mark each: identifies type of radiation and its frequency/energy; ionising vs non-ionising; correct hazard; any benefit; justified conclusion (max 5).'}


t6 = topic('Communication: analogue and digital signals', 'communication', 'digital', 'analogue', 'signals')
t6.fixed('C1', (1, 2), [
    ('A digital signal is one that', 'has only a limited number of values, usually two (0 and 1)', 'Digital: discrete values (on/off); analogue: continuously varying.', ['varies continuously in amplitude', 'can only be sent by radio waves', 'cannot be transmitted through optical fibres']),
    ('Which electromagnetic wave is used to carry signals inside optical fibres?', 'Infrared (or visible light)', 'Optical fibres usually carry infrared, guided by total internal reflection.', ['Radio waves', 'Gamma rays', 'Microwaves']),
    ('Bluetooth and Wi-Fi use which type of electromagnetic wave?', 'Microwaves (and short-wavelength radio)', 'Wireless networking uses about 2.4 GHz and 5 GHz microwaves.', ['Infrared', 'Ultraviolet', 'X-rays']),
])
t6.fixed('C2', (2, 3, 4), [
    ('Explain two advantages of sending a signal digitally rather than as an analogue signal.', 'Noise can be removed when digital signals are regenerated, so quality stays high; more data can be sent per second and data can be compressed or encrypted.', '1 mark each for two: regeneration removes noise; higher transmission rate; easily processed/stored by computers.'),
    ('Explain why a digital signal can be "cleaned up" by a regenerator but an analogue signal cannot.', 'The regenerator only has to decide whether each pulse is 0 or 1 and send a fresh pulse, so noise is removed; noise added to an analogue signal cannot be told apart from the signal and is amplified with it.', '1 mark: only two levels to decide between; 1 mark: analogue noise amplified with signal.'),
    ('Explain why satellite phones use microwaves rather than long-wave radio.', 'Microwaves pass through the ionosphere to reach the satellite; long-wave radio is reflected by the ionosphere.', '1 mark each.'),
])


@t6.add('C3', (2, 3, 4), 'numerical')
def t6_delay(r, D):
    h = r.choice([36000, 35800, 20200, 550, 1200])
    t = 2 * h * 1000 / 3e8
    return {'stem': f'A signal is sent from a ground station to a satellite at a height of {h:,} km and straight back. Calculate the time taken (speed of microwaves = 3.0 × 10⁸ m/s).',
            'answer': f'{sf(t)} s', 'key': f'distance = 2 × {h:,} × 10³ m; t = d/v = {sf(2 * h * 1000)} / 3.0 × 10⁸ = {sf(t)} s. Forgetting the return journey halves the answer.'}


CHAPTERS[2] = [t4, t5, t6]

# =========================================================== 3 Magnetism
t7 = topic('Magnets and magnetic materials', 'magnetic materials', 'magnets', 'poles', 'induced magnetism', 'permanent temporary')
t7.fixed('C1', (1, 2), [
    ('Which of these metals is magnetic?', 'Nickel', 'Iron, steel, nickel and cobalt are magnetic; aluminium, copper and brass are not.', ['Copper', 'Aluminium', 'Brass']),
    ('What happens when the north pole of one magnet is brought near the north pole of another?', 'They repel', 'Like poles repel, unlike poles attract.', ['They attract', 'Nothing happens', 'Both become south poles']),
    ('Which material is best for the core of an electromagnet?', 'Soft iron', 'Soft iron is easily magnetised and loses its magnetism quickly (temporary magnet).', ['Steel', 'Copper', 'Plastic']),
    ('Which material is best for making a permanent magnet?', 'Steel', 'Steel is hard to magnetise but keeps its magnetism.', ['Soft iron', 'Aluminium', 'Glass']),
    ('What is meant by induced magnetism?', 'A magnetic material becoming a magnet when placed in a magnetic field', 'Induced magnetism: a magnetic material is magnetised by a nearby magnet; the near end gets the opposite pole.', ['A magnet losing its magnetism when heated', 'A current produced in a wire moving in a field', 'The force between two like poles']),
])
t7.fixed('C2', (2, 3, 4), [
    ('Explain why an unmagnetised iron nail is attracted to either pole of a magnet.', 'Magnetism is induced in the nail: the end nearest the magnet becomes the opposite pole, so it is always attracted.', '1 mark: induced magnetism; 1 mark: near end opposite pole → attraction.'),
    ('Explain why repulsion, not attraction, is the only sure test that an object is a magnet.', 'Attraction occurs between a magnet and any magnetic material, so it does not prove the object is a magnet; only a magnet can repel another magnet.', '1 mark each.'),
    ('Describe how to demagnetise a steel bar using electricity.', 'Place it in a coil carrying alternating current and slowly pull it out of the coil (or reduce the a.c. to zero).', '1 mark: a.c. coil; 1 mark: withdraw slowly / reduce current.'),
    ('A chain of iron paper clips hangs from a magnet. Explain what happens when the magnet is removed if the clips are soft iron, and if they are steel.', 'Soft iron clips lose their induced magnetism and fall apart; steel clips keep some magnetism and may stay together.', '1 mark each.'),
    ('Explain why scrap-yard cranes use electromagnets rather than permanent magnets.', 'The magnetism can be switched off to drop the load, and its strength can be changed with the current.', '1 mark each.'),
])


@t7.add('C3', (2, 3, 4), 'explain')
def t7_test(r, D):
    a, b = r.sample(['A', 'B', 'C', 'D'], 2)
    return {'stem': f'{person(r)} has three identical-looking bars: one is a magnet, one is soft iron and one is aluminium. Bar {a} attracts the north pole of a compass; bar {b} has no effect. Describe further tests to identify all three bars and explain the reasoning.',
            'answer': f'Bar {b} is aluminium (not magnetic). Test bar {a} with both compass poles: if one end repels a pole, {a} is the magnet; if it attracts both poles, it is soft iron and the remaining bar is the magnet.',
            'key': '1 mark: non-magnetic identified; 1 mark: repulsion test; 1 mark: correct conclusion logic.'}


t8 = topic('Magnetic fields', 'magnetic field', 'field lines', 'field pattern', 'plotting compass')
t8.fixed('C1', (1, 2), [
    ('Magnetic field lines outside a bar magnet point', 'from the north pole to the south pole', 'Direction of the field = direction a free north pole would move: N to S outside the magnet.', ['from the south pole to the north pole', 'in circles around the middle', 'away from both poles']),
    ('Where is the magnetic field of a bar magnet strongest?', 'At the poles', 'Field lines are closest together at the poles.', ['In the middle of the magnet', 'Far from the magnet', 'Equally strong everywhere']),
    ('Which apparatus can be used to plot the field lines around a bar magnet?', 'A plotting compass', 'Move a small plotting compass and mark the direction its needle points; iron filings show the pattern but not the direction.', ['A voltmeter', 'A ruler alone', 'A thermometer']),
])
t8.fixed('C2', (2, 3, 4), [
    ('Explain why magnetic field lines never cross.', 'At any point the field has only one direction; if lines crossed, a compass there would point two ways at once.', '1 mark each.'),
    ('Describe the field between a north pole and a south pole placed close together, facing each other.', 'Fairly uniform: parallel, equally spaced lines from N to S in the gap.', '1 mark: parallel equally spaced; 1 mark: N → S direction.'),
    ('Describe the magnetic field between two north poles placed near each other.', 'Field lines from both poles curve away; there is a neutral point midway where the fields cancel.', '1 mark: lines repel/curve away; 1 mark: neutral point.'),
    ('Explain how iron filings show a magnetic field pattern but do not show its direction.', 'Each filing becomes a tiny induced magnet and lines up with the field, but filings have no marked north end, so the direction is not shown.', '1 mark each.'),
])


@t8.add('C3', (2, 3), 'explain')
def t8_spacing(r, D):
    return {'stem': f'On a field diagram, point {r.choice("PQRX")} has field lines {r.choice([2, 3, 4])} times closer together than point {r.choice("YZ")}. State what this tells you about the field and suggest where each point might be on a bar magnet.',
            'answer': 'The field is stronger where lines are closer; the first point is nearer a pole, the second further away (or near the middle/side).',
            'key': '1 mark: closer lines = stronger field; 1 mark: sensible positions.'}


@t8.add('C4', (3, 4), 'case')
def t8_plan(r, D):
    return {'stem': f'{person(r)} wants to compare the strength of two bar magnets using only a plotting compass and a metre rule. Plan an experiment, stating the measurements, control variables and how the result will be decided.',
            'answer': 'Place the compass on a line east–west so the Earth’s field is perpendicular; bring each magnet along the same line until the needle deflects by a fixed angle (e.g. 45°) and measure the distance from the compass. The magnet that does this from further away is stronger. Control: same orientation, same compass, no other magnetic materials nearby; repeat and average.',
            'key': '1 mark: measure distance for a fixed deflection (or deflection at fixed distance); 1 mark: control variables (orientation, location away from iron); 1 mark: repeats; 1 mark: conclusion rule.'}


t9 = topic('Electromagnets and the magnetic effect of a current', 'electromagnet', 'magnetic effect of current', 'solenoid', 'coil')
t9.fixed('C1', (1, 2), [
    ('What is the shape of the magnetic field around a long straight wire carrying a current?', 'Concentric circles around the wire', 'The field lines are circles centred on the wire; the right-hand grip rule gives the direction.', ['Straight lines parallel to the wire', 'Straight lines radiating out from the wire', 'There is no field around a straight wire']),
    ('Which change makes an electromagnet stronger?', 'Increasing the number of turns on the coil', 'Strength increases with more turns, more current or adding a soft-iron core.', ['Using a copper core', 'Reducing the current', 'Using fewer turns']),
    ('The field inside a long current-carrying solenoid is', 'strong and uniform', 'Inside a solenoid the lines are parallel and close together.', ['zero', 'weak and circular', 'strongest at the outside']),
])
t9.fixed('C2', (2, 3, 4), [
    ('Explain how reversing the current in a solenoid affects its magnetic field.', 'The field reverses direction, so the poles at the ends swap; the strength is unchanged.', '1 mark each.'),
    ('Explain why a relay can use a small current to switch on a large current.', 'The small current magnetises an electromagnet, which attracts an iron armature and closes separate contacts in the high-current circuit.', '1 mark: electromagnet attracts armature; 1 mark: closes separate circuit.'),
    ('Explain how the right-hand grip rule gives the direction of the field around a wire.', 'Grip the wire with the right hand, thumb pointing in the direction of conventional current; the curled fingers show the field direction.', '1 mark each.'),
])


@t9.add('C3', (2, 3, 4), 'explain')
def t9_design(r, D):
    n1, n2 = r.sample([50, 100, 150, 200, 300], 2)
    i1, i2 = r.sample([0.5, 1.0, 1.5, 2.0], 2)
    return {'stem': f'Electromagnet X has {n1} turns and carries {i1} A; electromagnet Y has {n2} turns and carries {i2} A. Both have identical soft-iron cores. Predict which is stronger and explain.',
            'answer': ('X' if n1 * i1 > n2 * i2 else 'Y' if n2 * i2 > n1 * i1 else 'Both equal') + f' – strength depends on turns × current ({n1 * i1:g} for X, {n2 * i2:g} for Y).',
            'key': '1 mark: strength increases with turns and current; 1 mark: compares the product and concludes.'}


CHAPTERS[3] = [t7, t8, t9]

# =========================================================== 4 Static electricity
t10 = topic('Charging by friction and electric charge', 'charge', 'charging by friction', 'static', 'positive negative charge')
t10.fixed('C1', (1, 2), [
    ('When a polythene rod is rubbed with a cloth it becomes negatively charged. Why?', 'Electrons move from the cloth to the rod', 'Only electrons move in charging by friction; the rod gains electrons.', ['Protons move from the rod to the cloth', 'Electrons move from the rod to the cloth', 'Positive charges are created in the cloth']),
    ('Two negatively charged balloons are held close together. What happens?', 'They repel each other', 'Like charges repel.', ['They attract each other', 'They both become positive', 'Nothing happens']),
    ('What is the unit of electric charge?', 'coulomb (C)', 'Charge is measured in coulombs.', ['ampere (A)', 'volt (V)', 'ohm (Ω)']),
    ('Which of these is a good electrical insulator?', 'Plastic', 'Insulators (plastic, rubber, glass, dry wood) do not let electrons move freely.', ['Copper', 'Aluminium', 'Graphite']),
])
t10.fixed('C2', (2, 3, 4), [
    ('A rubbed balloon sticks to a neutral wall. Explain why.', 'The negative balloon repels electrons in the wall surface away, leaving the surface positively charged by induction; unlike charges attract.', '1 mark: charge induced in wall; 1 mark: attraction of unlike charges.'),
    ('Explain why a metal rod held in the hand cannot be charged by rubbing, but a plastic rod can.', 'Metal is a conductor, so any charge flows away through the hand to earth; plastic is an insulator so charge stays where it is.', '1 mark each.'),
    ('Explain why charging by friction cannot produce a positive charge by "adding protons".', 'Protons are fixed in the nuclei; only electrons are free to move, so an object becomes positive by losing electrons.', '1 mark each.'),
    ('A student rubs a glass rod with silk and it becomes positive. Explain what has happened to the silk and why.', 'The silk gains the electrons lost by the glass, so it becomes equally negatively charged; charge is conserved.', '1 mark: silk negative; 1 mark: equal and opposite (conservation).'),
])


@t10.add('C3', (2, 3, 4), 'numerical')
def t10_electrons(r, D):
    q = r.choice([1.6e-9, 3.2e-9, 4.8e-10, 8.0e-9, 1.6e-8, 2.4e-9])
    n = q / 1.6e-19
    return {'stem': f'A rod gains a charge of −{sci(q, 2)} C when rubbed. The charge on one electron is −1.6 × 10⁻¹⁹ C. Calculate how many electrons were transferred to the rod.',
            'answer': f'{sci(n, 2)} electrons', 'key': f'n = Q/e = {sci(q, 2)} / 1.6 × 10⁻¹⁹ = {sci(n, 2)} [2].'}


t11 = topic('Electric fields and uses and dangers of static', 'electric field', 'uses of static', 'dangers', 'earthing')
t11.fixed('C1', (1, 2, 3), [
    ('The direction of an electric field at a point is the direction of the force on', 'a small positive charge placed there', 'Field direction = direction of force on a positive test charge.', ['an electron placed there', 'a neutron placed there', 'a small magnet placed there']),
    ('The electric field lines around an isolated positive point charge', 'point radially outwards', 'Lines leave positive charges and enter negative ones.', ['point radially inwards', 'form circles around the charge', 'are parallel lines']),
    ('Why are aircraft earthed before refuelling?', 'To stop charge building up and causing a spark that ignites fuel vapour', 'Fuel flowing through the hose can charge the aircraft; earthing lets charge flow safely away.', ['To make the fuel flow faster', 'To keep the fuel cool', 'To charge the fuel tank positively']),
])
t11.fixed('C2', (2, 3, 4), [
    ('Describe the electric field between two parallel plates, one positive and one negative.', 'Uniform: parallel, equally spaced lines from the positive plate to the negative plate (curving slightly at the edges).', '1 mark: parallel equally spaced; 1 mark: + to −.'),
    ('Explain how an electrostatic paint sprayer gives an even coat and wastes less paint.', 'Paint droplets are given the same charge, so they repel and spread out; the object is given the opposite charge (or earthed) so droplets are attracted to it, even round the back.', '1 mark: droplets repel → even spray; 1 mark: attracted to object → less waste.'),
    ('Explain why you sometimes get a small shock touching a metal door handle after walking on a nylon carpet.', 'Friction between shoes and carpet charges your body; when you touch the earthed metal handle, charge flows suddenly through you to earth.', '1 mark each.'),
])


@t11.add('C4', (3, 4, 5), 'long')
def t11_eval(r, D):
    sc = r.choice([
        ('A factory producing flour dust has had small fires. The manager says static electricity cannot be the cause because "the machines are all plastic and do not conduct". Evaluate this statement.',
         'Plastic insulators are exactly where charge builds up by friction because it cannot flow away; a spark can ignite fine dust. The statement is wrong; earthing metal parts, using conducting materials and humidifying the air would reduce the risk.'),
        ('A photocopier uses static charge on a drum to attract toner. Explain how the image is formed and suggest why copies are poor on very humid days.',
         'The drum is charged; light from the white areas of the original discharges the drum there, leaving a charged image of the dark areas; toner is attracted to charged regions and transferred to paper, then fused by heat. Humid air conducts slightly so charge leaks away, giving faint copies.'),
    ])
    return {'stem': sc[0], 'answer': sc[1], 'key': '1 mark each: charge by friction on insulators; cannot flow away; spark/attraction mechanism; link to context; justified judgement (max 5).'}


CHAPTERS[4] = [t10, t11]

# =========================================================== 5 Electrical quantities
t12 = topic('Electric current and charge', 'current', 'charge', 'q = it', 'ammeter')
t12.fixed('C1', (1, 2), [
    ('Electric current is', 'the rate of flow of charge', 'I = Q/t: current is charge passing a point per second.', ['the energy per unit charge', 'the opposition to the flow of charge', 'the force on a moving charge']),
    ('How is an ammeter connected in a circuit?', 'In series with the component', 'An ammeter measures the current through a component so it is placed in series; it has very low resistance.', ['In parallel with the component', 'Across the cell only', 'It is not connected, it is held near the wire']),
    ('In a metal wire, the charges that move to form a current are', 'free electrons', 'Metals conduct because of free (delocalised) electrons.', ['protons', 'positive ions', 'neutrons']),
    ('Conventional current flows from', 'the positive terminal to the negative terminal', 'Conventional current: + to − around the external circuit; electrons flow the other way.', ['the negative terminal to the positive terminal', 'both terminals into the middle', 'earth to the cell']),
])


@t12.add('C3', (1, 2, 3, 4), 'numerical')
def t12_qit(r, D):
    I = r.choice([0.2, 0.25, 0.4, 0.5, 1.5, 2.0, 2.5, 3.0, 4.0, 12.0])
    t = r.choice([10, 20, 30, 45, 60, 120, 300])
    mode = r.choice(['Q', 'I', 't'])
    if D >= 3:
        tmin = r.choice([2, 5, 8, 10, 15])
        Q = I * tmin * 60
        return {'stem': f'A current of {sf(I)} A flows through a heater element for {tmin} minutes. Calculate the charge that passes.', 'answer': f'{sf(Q)} C',
                'key': f't = {tmin} × 60 = {tmin * 60} s; Q = It = {sf(I)} × {tmin * 60} = {sf(Q)} C. Forgetting to convert minutes is the usual error.'}
    Q = I * t
    if mode == 'Q':
        stem, ans, key = f'A current of {sf(I)} A flows for {t} s. Calculate the charge that flows.', f'{sf(Q)} C', f'Q = It = {sf(I)} × {t} = {sf(Q)} C.'
    elif mode == 'I':
        stem, ans, key = f'A charge of {sf(Q)} C passes a point in {t} s. Calculate the current.', f'{sf(I)} A', f'I = Q/t = {sf(Q)}/{t} = {sf(I)} A.'
    else:
        stem, ans, key = f'How long does it take for {sf(Q)} C of charge to pass when the current is {sf(I)} A?', f'{sf(t)} s', f't = Q/I = {sf(Q)}/{sf(I)} = {t} s.'
    if D == 1:
        v = float(ans.split()[0].replace(',', ''))
        opts, a = num_mcq(r, v, [v * 2, v / 2, v * 10, v / 10], unit=' ' + ans.split()[1])
        return {'stem': stem.replace('Calculate the', 'What is the'), 'options': opts, 'answer': a, 'key': key}
    return {'stem': stem, 'answer': ans, 'key': key}


t13 = topic('Electromotive force and potential difference', 'e.m.f.', 'emf', 'potential difference', 'voltage', 'voltmeter')
t13.fixed('C1', (1, 2), [
    ('A voltmeter is connected', 'in parallel across the component', 'Voltmeters measure the p.d. across a component and have very high resistance.', ['in series with the component', 'in series with the cell only', 'between the ammeter and the cell']),
    ('The electromotive force (e.m.f.) of a source is', 'the electrical work done by the source in moving a unit charge around a complete circuit', 'e.m.f. = energy supplied per unit charge by the source (V = W/Q).', ['the current produced by the source', 'the resistance of the source', 'the charge stored in the source']),
    ('One volt is equal to one', 'joule per coulomb', '1 V = 1 J/C.', ['coulomb per second', 'joule per second', 'ampere per ohm']),
])


@t13.add('C3', (2, 3, 4), 'numerical')
def t13_wq(r, D):
    V = r.choice([1.5, 3.0, 4.5, 6.0, 9.0, 12, 230])
    Q = r.choice([2, 5, 10, 20, 40, 60, 150])
    W = V * Q
    m = r.choice(['W', 'V'])
    if m == 'W':
        return {'stem': f'A {sf(V)} V battery moves {Q} C of charge around a circuit. Calculate the energy it transfers.', 'answer': f'{sf(W)} J', 'key': f'W = QV = {Q} × {sf(V)} = {sf(W)} J.'}
    return {'stem': f'A source transfers {sf(W)} J of energy when {Q} C of charge passes through it. Calculate its e.m.f.', 'answer': f'{sf(V)} V', 'key': f'E = W/Q = {sf(W)}/{Q} = {sf(V)} V.'}


@t13.add('C2', (2, 3), 'explain')
def t13_cells(r, D):
    n = r.choice([2, 3, 4])
    v = r.choice([1.5, 1.2, 2.0])
    return {'stem': f'{n} cells, each of e.m.f. {v} V, are connected in series in a torch, but one is put in the wrong way round. Explain the total e.m.f.',
            'answer': f'{sf((n - 2) * v)} V: the reversed cell cancels the e.m.f. of one correctly placed cell, so total = ({n} − 2) × {v} V.',
            'key': '1 mark: e.m.f.s in series add with direction; 1 mark: correct value.'}


t14 = topic('Resistance', 'resistance', 'ohm', 'v = ir', 'resistivity', 'i-v characteristics', 'length cross-section')
t14.fixed('C1', (1, 2), [
    ('What is the unit of resistance?', 'ohm (Ω)', 'R = V/I, measured in ohms.', ['volt (V)', 'ampere (A)', 'watt (W)']),
    ('For a metal wire at constant temperature, the current–voltage graph is', 'a straight line through the origin', 'Ohmic conductor: I ∝ V at constant temperature.', ['a curve getting steeper', 'a horizontal line', 'zero until 0.7 V then rising steeply']),
    ('How does the resistance of a wire change if its length is doubled?', 'It doubles', 'R ∝ L (same material and thickness).', ['It halves', 'It is unchanged', 'It quadruples']),
    ('How does the resistance of a wire change if its cross-sectional area is doubled?', 'It halves', 'R ∝ 1/A.', ['It doubles', 'It is unchanged', 'It quadruples']),
    ('Why does the resistance of a filament lamp increase as the current increases?', 'The filament gets hotter', 'Higher temperature → ions vibrate more → more collisions with electrons.', ['The filament gets shorter', 'The voltage falls', 'The electrons move faster with less collision']),
])
t14.fixed('C2', (2, 3, 4), [
    ('Explain, using ideas about electrons, why a thinner wire has more resistance than a thicker wire of the same material and length.', 'A thinner wire has fewer free electrons per unit length available to carry current / a narrower path, so a given p.d. drives a smaller current.', '1 mark each.'),
    ('Sketch-describe the I–V graph of a semiconductor diode and explain its use.', 'Almost zero current in reverse and below about 0.6–0.7 V forward; current rises steeply above that. It lets current flow in one direction only (rectification).', '1 mark: graph shape; 1 mark: one-way conduction.'),
    ('A student says, "Resistance is the gradient of the I–V graph." Explain the error.', 'R = V/I. On an I–V graph (I on the y-axis) the gradient is I/V = 1/R, so a steeper line means a smaller resistance.', '1 mark each.'),
])


@t14.add('C3', (1, 2, 3, 4), 'numerical')
def t14_vir(r, D):
    R = r.choice([2, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 47, 100, 220])
    I = r.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1.5, 2.0])
    V = R * I
    m = r.choice('VIR')
    if m == 'V':
        stem, ans, key = f'A current of {sf(I)} A passes through a {R} Ω resistor. Calculate the potential difference across it.', f'{sf(V)} V', f'V = IR = {sf(I)} × {R} = {sf(V)} V.'
    elif m == 'I':
        stem, ans, key = f'A potential difference of {sf(V)} V is applied across a {R} Ω resistor. Calculate the current.', f'{sf(I)} A', f'I = V/R = {sf(V)}/{R} = {sf(I)} A.'
    else:
        stem, ans, key = f'The p.d. across a lamp is {sf(V)} V and the current is {sf(I)} A. Calculate its resistance.', f'{sf(R)} Ω', f'R = V/I = {sf(V)}/{sf(I)} = {R} Ω.'
    if D == 1:
        v = float(ans.split()[0]); u = ans.split()[1]
        opts, a = num_mcq(r, v, [v * 2, v / 2, V * I if m != 'V' else R / I, (I / R) if m == 'R' else v * 10], unit=' ' + u)
        return {'stem': stem.replace('Calculate the', 'What is the').replace('Calculate its', 'What is its'), 'options': opts, 'answer': a, 'key': key}
    if D == 4:
        mA = I * 1000
        return {'stem': f'A {R} kΩ resistor carries a current of {sf(mA / 1000)} mA. Calculate the p.d. across it.', 'answer': f'{sf(R * mA / 1000)} V',
                'key': f'V = IR = {sf(mA / 1000)} × 10⁻³ A × {R} × 10³ Ω = {sf(R * mA / 1000)} V. Prefixes kΩ and mA cancel.'}
    return {'stem': stem, 'answer': ans, 'key': key}


@t14.add('C3', (3, 4, 5), 'numerical')
def t14_wire(r, D):
    R = r.choice([4, 6, 8, 12, 16, 20])
    kL = r.choice([2, 3, 0.5])
    kA = r.choice([2, 3, 4, 0.5])
    R2 = R * kL / kA
    return {'stem': f'A wire has a resistance of {R} Ω. A second wire of the same metal is {sf(kL)} times as long and has {sf(kA)} times the cross-sectional area. Calculate the resistance of the second wire.',
            'answer': f'{sf(R2)} Ω', 'key': f'R ∝ L/A, so R₂ = {R} × {sf(kL)} / {sf(kA)} = {sf(R2)} Ω [3].'}


@t14.add('C4', (3, 4, 5), 'case')
def t14_practical(r, D):
    Ls = [20, 40, 60, 80, 100]
    rpm = r.choice([0.08, 0.1, 0.12, 0.15])
    I0 = r.choice([0.5, 0.4])
    Vs = [round(rpm * L / 100 * I0 * 10 + 0, 2) for L in Ls]
    return {'stem': f'In a practical, {person(r)} measures the p.d. across different lengths of constantan wire while keeping the current at {I0} A. Results (length/cm, p.d./V): ' + '; '.join(f'{L}, {v}' for L, v in zip(Ls, Vs)) + '. (a) Calculate the resistance for each length. (b) Describe the relationship. (c) State one source of error and how to reduce it.',
            'answer': '(a) R = V/I: ' + ', '.join(sf(v / I0) + ' Ω' for v in Vs) + '. (b) R is directly proportional to length (doubling L doubles R). (c) Wire heating changes R: switch off between readings / use small current; or contact position uncertainty: use crocodile clips at marked positions.',
            'key': '(a) 2 marks; (b) 1 mark proportional; (c) 1 mark error + 1 mark improvement.'}


t15 = topic('Electrical power and energy', 'electrical power', 'energy', 'p = iv', 'kilowatt-hour', 'cost of electricity')
t15.fixed('C1', (1, 2), [
    ('Which equation gives electrical power?', 'P = IV', 'Power = current × p.d.', ['P = V/I', 'P = I/V', 'P = V + I']),
    ('What is a kilowatt-hour (kWh)?', 'The energy transferred by a 1 kW appliance in 1 hour', '1 kWh = 1000 W × 3600 s = 3.6 × 10⁶ J.', ['The power of a 1 kW appliance', 'The current in a 1 kW appliance', 'One thousand watts per hour']),
])


@t15.add('C3', (1, 2, 3), 'numerical')
def t15_piv(r, D):
    V = r.choice([12, 230, 120, 240, 9, 6])
    I = r.choice([0.5, 2, 4, 5, 8, 10, 0.25, 1.5])
    P = V * I
    if r.random() < 0.5:
        return {'stem': f'An appliance draws {sf(I)} A from a {V} V supply. Calculate its power.', 'answer': f'{sf(P)} W', 'key': f'P = IV = {sf(I)} × {V} = {sf(P)} W.'}
    return {'stem': f'A {sf(P)} W appliance is connected to a {V} V supply. Calculate the current it draws.', 'answer': f'{sf(I)} A', 'key': f'I = P/V = {sf(P)}/{V} = {sf(I)} A.'}


@t15.add('C3', (3, 4), 'numerical')
def t15_cost(r, D):
    app = r.choice([('kettle', 2.4, 0.25), ('electric shower', 9.5, 0.2), ('heater', 2.0, 3.5), ('air conditioner', 1.8, 6), ('oven', 3.0, 1.5), ('washing machine', 0.5, 2)])
    days = r.choice([7, 30])
    price = r.choice([0.15, 0.18, 0.22, 0.25, 0.30])
    E = app[1] * app[2] * days
    cost = E * price
    return {'stem': f'A {app[1]} kW {app[0]} is used for {sf(app[2])} hours each day. Electricity costs ${price:.2f} per kWh. Calculate the cost of using it for {days} days.',
            'answer': f'${cost:.2f}', 'key': f'E = P × t = {app[1]} kW × {sf(app[2])} h × {days} = {sf(E)} kWh [2]; cost = {sf(E)} × {price:.2f} = ${cost:.2f} [1].'}


@t15.add('C4', (3, 4, 5), 'multi_step')
def t15_fuse(r, D):
    V = 230
    P = r.choice([60, 500, 800, 1200, 2000, 2800, 2900])
    I = P / V
    fuses = [3, 5, 13]
    f = next(x for x in fuses if x >= I * 1.0 and x > I)
    t = r.choice([5, 10, 20, 30])
    E = P * t * 60
    return {'stem': f'A {P} W appliance runs from the {V} V mains for {t} minutes. (a) Calculate the current. (b) Choose a suitable fuse from 3 A, 5 A and 13 A and justify your choice. (c) Calculate the energy transferred in joules.',
            'answer': f'(a) {sf(I)} A (b) {f} A – the smallest rating just above the normal current (c) {sci(E, 3)} J',
            'key': f'(a) I = P/V = {P}/{V} = {sf(I)} A [2]; (b) {f} A, just above working current so it melts if a fault increases the current [2]; (c) E = Pt = {P} × {t * 60} = {sf(E)} J [2].'}


CHAPTERS[5] = [t12, t13, t14, t15]

# =========================================================== 6 Circuits
t16 = topic('Series circuits', 'series circuits', 'series', 'combined resistance series')
t16.fixed('C1', (1, 2), [
    ('In a series circuit, the current is', 'the same at every point', 'There is only one path, so the same charge per second passes every point.', ['largest near the positive terminal', 'shared equally between components', 'zero after the first lamp']),
    ('Two resistors of 4 Ω and 6 Ω are in series. What is their combined resistance?', '10 Ω', 'Series: R = R₁ + R₂.', ['2.4 Ω', '24 Ω', '1.5 Ω']),
    ('In a series circuit, the sum of the p.d.s across the components equals', 'the e.m.f. of the supply', 'Energy supplied per coulomb = energy transferred per coulomb in the components.', ['the current', 'zero', 'the largest single p.d.']),
])


@t16.add('C3', (2, 3, 4), 'multi_step')
def t16_calc(r, D):
    R1, R2 = r.sample([2, 3, 4, 5, 6, 8, 10, 12, 15], 2)
    I = r.choice([0.2, 0.25, 0.4, 0.5, 1.0])
    E = I * (R1 + R2)
    return {'stem': f'A {sf(E)} V battery is connected in series with resistors of {R1} Ω and {R2} Ω. Calculate (a) the total resistance, (b) the current and (c) the p.d. across the {R1} Ω resistor.',
            'answer': f'(a) {R1 + R2} Ω (b) {sf(I)} A (c) {sf(I * R1)} V', 'key': f'(a) {R1} + {R2} = {R1 + R2} Ω; (b) I = {sf(E)}/{R1 + R2} = {sf(I)} A; (c) V = IR = {sf(I)} × {R1} = {sf(I * R1)} V. One mark each step.'}


@t16.add('C2', (2, 3, 4), 'explain')
def t16_explain(r, D):
    n = r.choice([2, 3, 4])
    return {'stem': f'{n} identical lamps are connected in series to a battery. Explain what happens to the brightness if one more identical lamp is added in series.',
            'answer': 'All lamps get dimmer: total resistance increases so the current falls, and the e.m.f. is shared between more lamps.',
            'key': '1 mark: resistance up/current down; 1 mark: p.d. shared / dimmer.'}


t17 = topic('Parallel circuits', 'parallel circuits', 'parallel', 'combined resistance parallel')
t17.fixed('C1', (1, 2), [
    ('In a parallel circuit, the current from the source is', 'equal to the sum of the currents in the branches', 'Current splits at a junction: I = I₁ + I₂.', ['the same in every branch', 'smaller than the current in any branch', 'zero when a branch is added']),
    ('Two 6 Ω resistors are connected in parallel. What is the combined resistance?', '3 Ω', '1/R = 1/6 + 1/6 → R = 3 Ω.', ['12 Ω', '6 Ω', '36 Ω']),
    ('Combined resistance of two resistors in parallel is always', 'less than the smaller resistor', 'Adding a parallel path always lowers the total resistance.', ['more than the larger resistor', 'equal to their sum', 'between the two values']),
])
t17.fixed('C2', (2, 3, 4), [
    ('Explain why lights in a house are wired in parallel.', 'Each lamp gets the full mains p.d.; each can be switched independently; if one fails the others stay on.', '1 mark each for two reasons.'),
    ('Explain why adding another resistor in parallel decreases the total resistance of a circuit.', 'It provides an extra path for charge, so more current flows for the same p.d.; R = V/I is smaller.', '1 mark each.'),
])


@t17.add('C3', (2, 3, 4, 5), 'multi_step')
def t17_calc(r, D):
    pairs = [(6, 3), (12, 6), (4, 4), (10, 15), (20, 30), (12, 4), (6, 12), (8, 24)]
    R1, R2 = r.choice(pairs)
    V = r.choice([6, 12, 9, 24])
    Rp = R1 * R2 / (R1 + R2)
    I1, I2 = V / R1, V / R2
    return {'stem': f'Resistors of {R1} Ω and {R2} Ω are connected in parallel across a {V} V supply. Calculate (a) the current in each resistor, (b) the total current and (c) the combined resistance.',
            'answer': f'(a) {sf(I1)} A and {sf(I2)} A (b) {sf(I1 + I2)} A (c) {sf(Rp)} Ω',
            'key': f'(a) I = V/R in each branch (full {V} V across each) [2]; (b) sum = {sf(I1 + I2)} A [1]; (c) R = V/I = {V}/{sf(I1 + I2)} = {sf(Rp)} Ω or 1/R = 1/{R1} + 1/{R2} [2].'}


t18 = topic('Potential dividers and sensing circuits', 'potential divider', 'thermistor', 'ldr', 'light-dependent resistor', 'sensors')
t18.fixed('C1', (1, 2), [
    ('How does the resistance of a light-dependent resistor (LDR) change as light intensity increases?', 'It decreases', 'LDR: more light → lower resistance.', ['It increases', 'It stays the same', 'It becomes infinite']),
    ('How does the resistance of an NTC thermistor change as temperature increases?', 'It decreases', 'NTC thermistor: hotter → lower resistance.', ['It increases', 'It stays the same', 'It doubles every degree']),
])
t18.fixed('C2', (2, 3, 4), [
    ('In a potential divider made of a fixed resistor and an LDR, the output is taken across the LDR. Explain what happens to the output p.d. when it gets dark.', 'In the dark the LDR resistance increases, so it takes a larger share of the supply p.d.; the output rises.', '1 mark: R of LDR rises; 1 mark: larger share of p.d.'),
    ('Explain how a thermistor in a potential divider could switch on a fan when a room gets hot.', 'As temperature rises the thermistor resistance falls; with the output across the fixed resistor, the p.d. across it rises and can switch on a transistor/relay that runs the fan.', '1 mark each for R falls, p.d. share changes, switching device.'),
])


@t18.add('C3', (2, 3, 4), 'numerical')
def t18_divider(r, D):
    Vin = r.choice([6, 9, 12])
    R1, R2 = r.choice([(1, 2), (2, 1), (3, 1), (1, 3), (4, 2), (5, 10), (10, 20)])
    Vout = Vin * R2 / (R1 + R2)
    return {'stem': f'A potential divider has R₁ = {R1} kΩ and R₂ = {R2} kΩ in series across a {Vin} V supply. Calculate the output p.d. across R₂.',
            'answer': f'{sf(Vout)} V', 'key': f'V_out = V_in × R₂/(R₁ + R₂) = {Vin} × {R2}/{R1 + R2} = {sf(Vout)} V [2].'}


@t18.add('C4', (3, 4, 5), 'multi_step')
def t18_design(r, D):
    Vin = 12
    Rldr_dark = r.choice([20, 30, 40])
    Rldr_light = r.choice([1, 2])
    Rf = r.choice([5, 10])
    vd = Vin * Rldr_dark / (Rldr_dark + Rf)
    vl = Vin * Rldr_light / (Rldr_light + Rf)
    return {'stem': f'A street-light controller uses an LDR in series with a {Rf} kΩ resistor across a 12 V supply, with the output taken across the LDR. The LDR is {Rldr_light} kΩ in daylight and {Rldr_dark} kΩ at night. (a) Calculate the output p.d. in daylight and at night. (b) The lamp switches on when the output exceeds 6 V. Explain whether the circuit works as intended.',
            'answer': f'(a) Day: {sf(vl)} V; night: {sf(vd)} V. (b) Yes: {sf(vd)} V > 6 V at night switches the lamp on; {sf(vl)} V < 6 V in daylight keeps it off.',
            'key': f'(a) 2 marks each using V = 12 × R_LDR/(R_LDR + {Rf}); (b) 1 mark comparison with 6 V, 1 mark conclusion.'}


t19 = topic('Electrical safety', 'electrical safety', 'fuse', 'earthing', 'circuit breaker', 'hazards')
t19.fixed('C1', (1, 2), [
    ('In a three-pin plug, which wire is connected to the fuse?', 'Live', 'The fuse is in the live wire so it disconnects the high-voltage side when it melts.', ['Neutral', 'Earth', 'None of them']),
    ('What is the purpose of the earth wire in a metal-cased appliance?', 'To carry current safely to earth if the live wire touches the case', 'A low-resistance path to earth causes a large current that blows the fuse.', ['To make the appliance work faster', 'To carry the normal working current', 'To reduce the voltage of the supply']),
    ('Which is an advantage of a circuit breaker over a fuse?', 'It can be reset rather than replaced', 'Circuit breakers trip quickly and can be reset.', ['It is cheaper to replace', 'It works only on direct current', 'It increases the current']),
    ('What is meant by "double insulation"?', 'The appliance has a non-conducting case so no earth wire is needed', 'Plastic casing means live parts cannot touch accessible metal.', ['Two fuses are fitted in series', 'The cable has two earth wires', 'The plug has two live pins']),
])
t19.fixed('C2', (2, 3, 4), [
    ('Explain why the fuse must be placed in the live wire rather than the neutral wire.', 'If the fuse blows in the live wire, the appliance is disconnected from the high voltage; in the neutral it would stay live and dangerous.', '1 mark each.'),
    ('Explain how a fuse and an earth wire together protect a person when the live wire touches a metal case.', 'The current flows through the low-resistance earth wire; this large current melts the fuse, cutting off the live supply, so the case does not stay live.', '1 mark: path to earth; 1 mark: large current; 1 mark: fuse melts/disconnects.'),
    ('State three hazards of mains electricity and how each is reduced.', 'Damaged insulation (replace cables); overheating cables from too much current (correct fuse/ thicker cable); damp conditions (keep water away, use RCDs).', '1 mark per hazard with matching precaution.'),
])
CHAPTERS[6] = [t16, t17, t18, t19]

# =========================================================== 7 Electromagnetic forces
t20 = topic('Force on a current-carrying conductor', 'motor effect', 'force on a conductor', "fleming's left-hand rule", 'force on charged particles')
t20.fixed('C1', (1, 2), [
    ("In Fleming's left-hand rule, the second finger points in the direction of", 'the conventional current', 'First finger: Field; seCond finger: Current; thuMb: Motion (force).', ['the magnetic field', 'the force', 'the electron flow']),
    ('Which change reverses the direction of the force on a current-carrying wire in a magnetic field?', 'Reversing the current', 'Reversing either the current or the field reverses the force; reversing both leaves it unchanged.', ['Doubling the current', 'Using a thicker wire', 'Reversing both the current and the field']),
    ('When is the force on a current-carrying wire in a magnetic field zero?', 'When the wire is parallel to the field', 'Force is greatest when wire ⟂ field, zero when parallel.', ['When the wire is perpendicular to the field', 'When the current is largest', 'When the field is strongest']),
])
t20.fixed('C2', (2, 3, 4), [
    ('Explain why a current-carrying wire placed between the poles of a magnet experiences a force.', 'The magnetic field of the current interacts with the field of the magnet; the fields combine to be stronger on one side and weaker on the other, pushing the wire.', '1 mark: field around wire; 1 mark: interaction gives force.'),
    ('A beam of electrons passes through a magnetic field at right angles. Explain why its path curves.', 'Moving charges are a current, so each electron feels a force at right angles to its velocity and to the field; this continually changes its direction.', '1 mark each.'),
    ('Explain how increasing the current affects the force on a wire in a magnetic field, and why.', 'The force increases (in proportion to current) because the magnetic field around the wire is stronger, so the interaction is greater.', '1 mark each.'),
])


@t20.add('C3', (2, 3, 4), 'explain')
def t20_flem(r, D):
    dirs = [('north to south across the page (left to right)', 'into the page', 'upwards'), ('left to right', 'out of the page', 'downwards'),
            ('into the page', 'left to right', 'downwards'), ('right to left', 'into the page', 'downwards')]
    f, c, m = r.choice(dirs)
    return {'stem': f"A magnetic field acts {f} and a wire carries a current {c}. Use Fleming's left-hand rule to find the direction of the force on the wire, and state what would happen if the current were reversed.",
            'answer': f'Force acts {m}; reversing the current reverses the force.', 'key': '1 mark: correct direction using F-field, C-current, M-motion; 1 mark: reversal.'}


t21 = topic('The d.c. motor', 'd.c. motor', 'motor', 'commutator', 'turning effect on a coil')
t21.fixed('C1', (1, 2), [
    ('What is the purpose of the split-ring commutator in a d.c. motor?', 'To reverse the current in the coil every half turn', 'Reversing the current each half turn keeps the coil turning in the same direction.', ['To increase the current', 'To stop the coil overheating', 'To change a.c. into d.c. in the supply']),
    ('Which change would make a d.c. motor turn faster?', 'Increasing the number of turns on the coil', 'Speed increases with more turns, larger current or a stronger field.', ['Using a weaker magnet', 'Reducing the current', 'Removing the commutator']),
])
t21.fixed('C2', (2, 3, 4), [
    ('Explain why the coil of a simple d.c. motor would not keep turning without a commutator.', 'After half a turn the forces on the sides would push the coil back the other way, so it would just rock to the vertical position and stop.', '1 mark each.'),
    ('Explain why the two sides of a coil in a motor experience forces in opposite directions.', 'The current flows in opposite directions in the two sides, so by Fleming’s left-hand rule the forces are opposite, giving a turning effect.', '1 mark each.'),
    ('Explain why the coil in a motor is wound on a soft-iron core.', 'The iron concentrates the magnetic field, increasing the force and turning effect.', '1 mark each.'),
])


@t21.add('C4', (3, 4, 5), 'long')
def t21_eval(r, D):
    return {'stem': f'{person(r)} builds a model d.c. motor but it turns very slowly. Suggest and explain three changes that would increase its speed, and one reason why a real motor might still be less efficient than expected.',
            'answer': 'Increase the current (larger force); add more turns (more force overall); use a stronger magnet or curved pole pieces with a soft-iron core (stronger field). Efficiency lost to friction at the brushes/axle and heating of the coil resistance.',
            'key': '1 mark per valid change with explanation (max 3 changes → up to 4 marks); 1 mark for efficiency loss.'}


CHAPTERS[7] = [t20, t21]

# =========================================================== 8 Electromagnetic induction
t22 = topic('Electromagnetic induction', 'electromagnetic induction', 'induced e.m.f.', 'induced emf', 'faraday', 'lenz')
t22.fixed('C1', (1, 2), [
    ('An e.m.f. is induced in a wire when', 'the wire cuts magnetic field lines', 'Induction needs relative movement or a changing field linked to the conductor.', ['the wire is held still in a steady field', 'a current is switched off in a different room', 'the wire is heated']),
    ('Which change increases the e.m.f. induced when a magnet is pushed into a coil?', 'Moving the magnet faster', 'Faster motion, stronger magnet or more turns increases the e.m.f.', ['Using fewer turns', 'Holding the magnet still inside the coil', 'Using a weaker magnet']),
    ('The direction of an induced current is always such that it', 'opposes the change producing it', 'Lenz’s law: the induced current opposes the change that causes it.', ['helps the change producing it', 'flows from north to south', 'is the same as the field direction']),
])
t22.fixed('C2', (2, 3, 4), [
    ('A magnet is held stationary inside a coil connected to a meter. Explain why the meter reads zero.', 'No field lines are being cut / the field through the coil is not changing, so no e.m.f. is induced.', '1 mark each.'),
    ('A magnet’s north pole is pushed into a coil. Explain, using Lenz’s law, what pole forms at that end of the coil.', 'A north pole forms, which repels the incoming north pole, opposing the change.', '1 mark: north; 1 mark: opposes motion.'),
    ('Explain why pulling a magnet out of a coil gives a meter deflection in the opposite direction to pushing it in.', 'The change in the field is reversed, so the induced e.m.f. (and current) is reversed.', '1 mark each.'),
])


@t22.add('C3', (2, 3, 4), 'explain')
def t22_predict(r, D):
    a = r.choice(['twice as fast', 'with the south pole first', 'with a coil of twice as many turns', 'and then held still'])
    ans = {'twice as fast': 'Larger deflection (about double), same direction.', 'with the south pole first': 'Same size deflection in the opposite direction.',
           'with a coil of twice as many turns': 'Larger deflection (about double), same direction.', 'and then held still': 'Deflection while moving, then zero once the magnet stops.'}[a]
    return {'stem': f'A north pole is pushed into a coil and the meter needle flicks to the right. Predict what happens if the magnet is pushed in {a}, and explain.', 'answer': ans,
            'key': '1 mark prediction; 1 mark reason (rate of cutting field lines / direction of change).'}


t23 = topic('The a.c. generator', 'a.c. generator', 'generator', 'slip rings', 'alternator')
t23.fixed('C1', (1, 2), [
    ('In an a.c. generator, what are slip rings used for?', 'To keep a continuous connection between the rotating coil and the external circuit', 'Slip rings and brushes connect the spinning coil to the circuit without twisting wires; the output stays alternating.', ['To reverse the current every half turn', 'To increase the speed of rotation', 'To store charge']),
    ('The e.m.f. of an a.c. generator is greatest when the plane of the coil is', 'parallel to the magnetic field', 'Coil sides then cut field lines fastest.', ['perpendicular to the magnetic field', 'at 45° to the field', 'the same at every position']),
])


@t23.add('C3', (2, 3, 4), 'numerical')
def t23_freq(r, D):
    rps = r.choice([5, 10, 25, 50, 60])
    k = r.choice(['doubled', 'halved'])
    f2 = rps * 2 if k == 'doubled' else rps / 2
    return {'stem': f'A coil in a generator turns {rps} times per second. (a) State the frequency of the output. (b) The speed of rotation is {k}. Describe two changes to the output graph.',
            'answer': f'(a) {rps} Hz (b) frequency becomes {sf(f2)} Hz and the peak e.m.f. is {k} as well.',
            'key': '1 mark: f = rotations per second; 1 mark: new frequency; 1 mark: peak voltage changes the same way.'}


t24 = topic('Transformers and power transmission', 'transformer', 'step-up', 'step-down', 'transmission of electricity', 'national grid', 'power loss')
t24.fixed('C1', (1, 2), [
    ('A step-up transformer has', 'more turns on the secondary coil than on the primary', 'Vs/Vp = Ns/Np; step-up means Ns > Np.', ['fewer turns on the secondary coil', 'equal turns on both coils', 'no iron core']),
    ('Why do transformers only work with alternating current?', 'A changing magnetic field is needed to induce an e.m.f. in the secondary coil', 'Direct current gives a steady field, so no e.m.f. is induced.', ['Direct current would melt the core', 'Alternating current has a higher voltage', 'Direct current cannot pass through copper']),
    ('Why is electricity transmitted at very high voltages?', 'To reduce the current and so reduce energy lost as heat in the cables', 'P = IV: for the same power, higher V means lower I; loss = I²R.', ['To make electricity travel faster', 'To make the cables lighter', 'To increase the frequency']),
])


@t24.add('C3', (1, 2, 3, 4), 'numerical')
def t24_turns(r, D):
    Vp = r.choice([230, 240, 11000, 400000, 25000, 120])
    Np = r.choice([200, 400, 500, 1000, 2000, 4000])
    Ns = r.choice([20, 50, 100, 10000, 40000, 8000])
    Vs = Vp * Ns / Np
    stem = f'A transformer has {Np} turns on the primary and {Ns} turns on the secondary. The primary voltage is {Vp:,} V. Calculate the secondary voltage and state whether it is step-up or step-down.'
    return {'stem': stem, 'answer': f'{sf(Vs)} V; {"step-up" if Ns > Np else "step-down"}', 'key': f'Vs = Vp × Ns/Np = {Vp:,} × {Ns}/{Np} = {sf(Vs)} V [2]; {"step-up" if Ns > Np else "step-down"} [1].'}


@t24.add('C4', (3, 4, 5), 'multi_step')
def t24_loss(r, D):
    P = r.choice([2e6, 5e6, 1e7, 2e7])
    R = r.choice([2, 4, 5, 8, 10])
    V1, V2 = r.choice([(25000, 400000), (11000, 275000), (20000, 132000)])
    I1, I2 = P / V1, P / V2
    L1, L2 = I1 ** 2 * R, I2 ** 2 * R
    return {'stem': f'A power station sends {sci(P, 2)} W along cables of total resistance {R} Ω. Compare the power lost in the cables if it is transmitted at {V1:,} V and at {V2:,} V, and explain the result. Assume the transformers are 100% efficient.',
            'answer': f'At {V1:,} V: I = {sf(I1)} A, loss = {sci(L1, 3)} W. At {V2:,} V: I = {sf(I2)} A, loss = {sci(L2, 3)} W. Raising V by ×{sf(V2 / V1)} cuts I by the same factor and loss by its square (×{sf((V2 / V1) ** 2)}).',
            'key': '1 mark each current (I = P/V); 1 mark each loss (P = I²R); 1 mark explanation of square law.'}


@t24.add('C3', (3, 4), 'numerical')
def t24_current(r, D):
    Vp, Vs = r.choice([(230, 12), (230, 6), (240, 24), (120, 9)])
    Is = r.choice([0.5, 1.0, 2.0, 2.5, 4.0])
    Ip = Vs * Is / Vp
    return {'stem': f'A phone charger transformer steps {Vp} V down to {Vs} V and supplies a current of {sf(Is)} A to the phone. Assuming 100% efficiency, calculate the current in the primary coil.',
            'answer': f'{sf(Ip)} A', 'key': f'VpIp = VsIs → Ip = {Vs} × {sf(Is)}/{Vp} = {sf(Ip)} A [3].'}


CHAPTERS[8] = [t22, t23, t24]

# =========================================================== 9 The nuclear atom
t25 = topic('Atomic structure and the nuclear model', 'atomic structure', 'nuclear model', 'rutherford', 'alpha scattering', 'atom')
t25.fixed('C1', (1, 2), [
    ('In the alpha-particle scattering experiment, most alpha particles passed straight through the gold foil. What did this show?', 'Most of the atom is empty space', 'Most α passed through undeflected → atom mostly empty space.', ['The nucleus is negatively charged', 'Electrons are in the nucleus', 'Atoms are solid spheres']),
    ('A very small number of alpha particles bounced back. What did this show?', 'The atom has a tiny, dense, positively charged nucleus', 'Large deflections need a concentrated positive charge and mass.', ['Electrons are very heavy', 'Gold atoms are uncharged', 'Alpha particles are negatively charged']),
    ('Which particles are found in the nucleus?', 'Protons and neutrons', 'Nucleons = protons + neutrons; electrons orbit outside.', ['Protons and electrons', 'Neutrons and electrons', 'Only electrons']),
    ('The proton number (atomic number) of a nucleus is', 'the number of protons', 'Z = number of protons; A = protons + neutrons.', ['the number of neutrons', 'the number of protons plus neutrons', 'the number of electron shells']),
])


@t25.add('C3', (1, 2, 3), 'numerical')
def t25_count(r, D):
    nuc = r.choice([('carbon', 'C', 6, 14), ('oxygen', 'O', 8, 16), ('sodium', 'Na', 11, 23), ('uranium', 'U', 92, 235), ('iodine', 'I', 53, 131), ('cobalt', 'Co', 27, 60), ('strontium', 'Sr', 38, 90), ('radium', 'Ra', 88, 226)])
    n, s, Z, A = nuc
    return {'stem': f'The nuclide {n}-{A} is written as {s} with nucleon number {A} and proton number {Z}. State the number of protons, neutrons and electrons in a neutral atom.',
            'answer': f'{Z} protons, {A - Z} neutrons, {Z} electrons', 'key': f'protons = Z = {Z}; neutrons = A − Z = {A - Z}; electrons = protons in neutral atom = {Z}.'}


@t25.add('C2', (2, 3, 4), 'explain')
def t25_iso(r, D):
    e = r.choice([('carbon', 6, 12, 14), ('hydrogen', 1, 1, 3), ('uranium', 92, 235, 238), ('chlorine', 17, 35, 37), ('iodine', 53, 127, 131)])
    return {'stem': f'{e[0].capitalize()}-{e[2]} and {e[0]}-{e[3]} are isotopes. Explain what this means and why they have the same chemical properties.',
            'answer': f'Same number of protons ({e[1]}) but different numbers of neutrons ({e[2] - e[1]} and {e[3] - e[1]}). Chemical properties depend on electrons, and both have {e[1]} electrons.',
            'key': '1 mark: same protons; 1 mark: different neutrons; 1 mark: same electron arrangement → same chemistry.'}


@t25.add('C4', (3, 4), 'long')
def t25_model(r, D):
    return {'stem': 'Describe the alpha-particle scattering experiment and explain how its results led scientists to replace the "plum pudding" model of the atom with the nuclear model.',
            'answer': 'Alpha particles were fired at thin gold foil in a vacuum; detectors recorded deflections. Most passed straight through (mostly empty space), some were deflected (positive charge concentrated), a very few bounced back (tiny dense nucleus with most of the mass). The plum-pudding model, with spread-out positive charge, predicted only tiny deflections, so it was replaced.',
            'key': '1 mark set-up; 3 marks for the three observations with conclusions; 1 mark why plum pudding fails.'}


@t25.add('C4', (4, 5), 'case')
def t25_scale(r, D):
    nuc = r.choice([1e-14, 1.5e-14, 8e-15])
    atom = r.choice([1e-10, 1.4e-10, 2e-10])
    ratio = atom / nuc
    st = r.choice(['football stadium of diameter 200 m', 'city of diameter 10 km'])
    big = 200 if 'stadium' in st else 10000
    return {'stem': f'A gold nucleus has a diameter of about {sci(nuc, 2)} m and the atom about {sci(atom, 2)} m. (a) Calculate how many times wider the atom is. (b) If the atom were scaled up to a {st}, estimate the diameter of the nucleus. (c) Comment on what this shows about the alpha-scattering results.',
            'answer': f'(a) {sci(ratio, 2)} times (b) about {sf(big / ratio * 1000)} mm (c) The nucleus is tiny, so most alpha particles miss it completely and pass straight through.',
            'key': '1 mark ratio; 2 marks scaled size with units; 1 mark link to scattering.'}


t26 = topic('Nuclear fission and fusion', 'fission', 'fusion', 'chain reaction', 'nuclear energy')
t26.fixed('C1', (1, 2), [
    ('Nuclear fission is', 'the splitting of a large nucleus into two smaller nuclei', 'Fission: U-235 absorbs a neutron and splits, releasing energy and 2–3 neutrons.', ['the joining of two small nuclei', 'the emission of an alpha particle', 'the loss of electrons from an atom']),
    ('Nuclear fusion happens in', 'the core of the Sun', 'Fusion of hydrogen nuclei into helium powers stars.', ['nuclear power stations today', 'the Earth’s crust', 'chemical batteries']),
    ('In a fission reactor, the control rods', 'absorb neutrons to control the rate of reaction', 'Boron/cadmium rods absorb neutrons; lowering them slows the chain reaction.', ['slow neutrons down', 'cool the reactor', 'produce extra neutrons']),
    ('Why do fusion reactions need extremely high temperatures?', 'Nuclei must move fast enough to overcome the electrostatic repulsion between them', 'Both nuclei are positive and repel.', ['To melt the fuel', 'To produce neutrons', 'To slow nuclei down']),
])
t26.fixed('C2', (2, 3, 4), [
    ('Explain how a chain reaction occurs in uranium-235.', 'A neutron is absorbed by a U-235 nucleus, which splits releasing energy and 2 or 3 neutrons; these can be absorbed by further U-235 nuclei, causing more fissions.', '1 mark: neutron absorbed and fission; 1 mark: neutrons released cause further fissions.'),
    ('State one similarity and one difference between fission and fusion.', 'Both release large amounts of energy from the nucleus (mass converted). Fission splits heavy nuclei; fusion joins light nuclei.', '1 mark each.'),
    ('Explain why the moderator is needed in a thermal fission reactor.', 'It slows down the fast neutrons released, because slow (thermal) neutrons are much more likely to be absorbed by U-235 and cause fission.', '1 mark each.'),
])
CHAPTERS[9] = [t25, t26]

# =========================================================== 10 Radioactivity
t27 = topic('Types of radiation and their properties', 'alpha beta gamma', 'types of radiation', 'ionising', 'penetrating', 'detection', 'background radiation')
t27.fixed('C1', (1, 2), [
    ('Which type of radiation is stopped by a sheet of paper?', 'Alpha', 'α: stopped by paper/few cm of air; β: by a few mm of aluminium; γ: reduced by thick lead/concrete.', ['Beta', 'Gamma', 'X-rays']),
    ('Which type of radiation is the most ionising?', 'Alpha', 'α particles are large and highly charged so they ionise strongly.', ['Beta', 'Gamma', 'All are equally ionising']),
    ('A beta particle is', 'a fast-moving electron emitted from the nucleus', 'β⁻ forms when a neutron changes into a proton and an electron.', ['a helium nucleus', 'an electromagnetic wave', 'a neutron']),
    ('Which of these is a source of background radiation?', 'Radon gas from rocks', 'Background: radon, rocks/buildings, cosmic rays, food and drink, medical sources.', ['Mobile phone signals', 'Visible light', 'Sound from traffic']),
    ('Which detector is commonly used in school to measure radioactivity?', 'Geiger–Müller tube with a counter', 'A GM tube and counter (or ratemeter) records counts per minute.', ['Ammeter', 'Thermometer', 'Light-dependent resistor']),
    ('What is the composition of an alpha particle?', 'Two protons and two neutrons', 'α = helium-4 nucleus, charge +2.', ['One electron', 'One proton and one neutron', 'Two electrons']),
])
t27.fixed('C2', (2, 3, 4), [
    ('Explain why alpha radiation is the most dangerous inside the body but the least dangerous outside it.', 'Alpha is highly ionising, so inside it damages nearby cells strongly; outside it is stopped by the dead outer layer of skin or a few cm of air.', '1 mark each.'),
    ('Explain how alpha, beta and gamma radiation are deflected differently in an electric field.', 'α (positive) deflects towards the negative plate, β (negative) deflects more strongly towards the positive plate as it is much lighter, γ is undeflected (no charge).', '1 mark each for α, β, γ.'),
    ('Explain why the count rate measured near a source should be corrected for background radiation.', 'Background radiation is always present and adds to the counts; it must be measured without the source and subtracted to get the count rate from the source alone.', '1 mark each.'),
])


@t27.add('C3', (2, 3, 4), 'case')
def t27_absorb(r, D):
    bg = r.choice([15, 18, 20, 24, 30])
    no = r.choice([480, 600, 720, 850])
    paper = no - r.choice([0, 5])
    al = r.choice([bg + 2, bg + 4, bg + 6, round(no * 0.6)])
    lead = r.choice([bg + 1, bg + 3, round(no * 0.3)])
    has_b = al < paper * 0.8
    has_g = lead > bg + 10 or al > bg + 30 and not has_b
    kinds = ['beta' if has_b else None, 'gamma' if (al > bg + 10) else None]
    kinds = [k for k in kinds if k]
    return {'stem': f'A student measures count rates (counts/min) from a source: no absorber {no}; paper {paper}; 3 mm aluminium {al}; 2 cm lead {lead}. Background is {bg} counts/min. Deduce which types of radiation the source emits, explaining each step.',
            'answer': ('No alpha (paper hardly changes the count). ' + ('Aluminium greatly reduces the count, so beta is present. ' if has_b else 'Aluminium makes little difference, so no beta. ') +
                       ('Count after aluminium stays above background, so gamma is present.' if al > bg + 10 else 'Count after aluminium is about background, so no gamma.')),
            'key': '1 mark each for reasoning on alpha, beta and gamma using the absorber data and background.'}


t28 = topic('Radioactive decay and nuclear equations', 'radioactive decay', 'decay equations', 'nuclear equations', 'random')
t28.fixed('C1', (1, 2), [
    ('Radioactive decay is described as random. This means', 'it is impossible to predict when a particular nucleus will decay', 'Each nucleus has a fixed probability of decay per second; the moment is unpredictable.', ['all nuclei decay at the same time', 'decay can be speeded up by heating', 'only odd-numbered nuclei decay']),
    ('When a nucleus emits an alpha particle, its proton number', 'decreases by 2', 'α emission: A − 4, Z − 2.', ['increases by 1', 'decreases by 4', 'stays the same']),
    ('When a nucleus emits a beta particle, its nucleon number', 'stays the same', 'β⁻: a neutron becomes a proton: A unchanged, Z + 1.', ['decreases by 4', 'increases by 1', 'decreases by 1']),
    ('Gamma emission changes', 'neither the proton number nor the nucleon number', 'γ is energy only; the nucleus loses energy.', ['the proton number by 1', 'the nucleon number by 4', 'both numbers by 2']),
])


@t28.add('C3', (2, 3, 4), 'numerical')
def t28_eq(r, D):
    nuc = r.choice([('U', 92, 238, 'Th', 'alpha'), ('Ra', 88, 226, 'Rn', 'alpha'), ('Po', 84, 210, 'Pb', 'alpha'), ('Am', 95, 241, 'Np', 'alpha'),
                    ('C', 6, 14, 'N', 'beta'), ('Sr', 38, 90, 'Y', 'beta'), ('I', 53, 131, 'Xe', 'beta'), ('Co', 27, 60, 'Ni', 'beta'), ('Th', 90, 234, 'Pa', 'beta')])
    s, Z, A, d, k = nuc
    if k == 'alpha':
        A2, Z2 = A - 4, Z - 2
        eq = f'{s}-{A} (Z = {Z}) → {d}-{A2} (Z = {Z2}) + α (He-4, Z = 2)'
    else:
        A2, Z2 = A, Z + 1
        eq = f'{s}-{A} (Z = {Z}) → {d}-{A2} (Z = {Z2}) + β (e, Z = −1)'
    return {'stem': f'{s}-{A} (proton number {Z}) decays by {k} emission to form {d}. Write the decay equation and give the nucleon and proton numbers of {d}.',
            'answer': f'{d}: nucleon number {A2}, proton number {Z2}. {eq}', 'key': f'1 mark nucleon number {A2}; 1 mark proton number {Z2}; 1 mark balanced equation (top and bottom numbers conserved).'}


@t28.add('C4', (4, 5), 'multi_step')
def t28_chain(r, D):
    A, Z = 238, 92
    seq = r.choice([['alpha', 'beta', 'beta'], ['alpha', 'alpha', 'beta'], ['beta', 'alpha', 'alpha', 'beta']])
    a, z = A, Z
    for s in seq:
        if s == 'alpha':
            a -= 4; z -= 2
        else:
            z += 1
    return {'stem': f'Uranium-238 (Z = 92) decays by the sequence {", then ".join(seq)}. Find the nucleon number and proton number of the final nucleus, showing each step.',
            'answer': f'Nucleon number {a}, proton number {z}', 'key': 'α: A − 4, Z − 2; β: A unchanged, Z + 1. 1 mark per correct step, 1 mark final answer.'}


t29 = topic('Half-life', 'half-life', 'half life', 'activity', 'decay curve')
t29.fixed('C1', (1, 2), [
    ('The half-life of a radioactive isotope is', 'the time taken for half the nuclei in a sample to decay', 'Half-life = time for activity (or number of undecayed nuclei) to halve.', ['half the time for all the nuclei to decay', 'the time for one nucleus to decay', 'the time for the mass of the sample to halve exactly']),
    ('After three half-lives, what fraction of the original radioactive nuclei remains?', '1/8', '1 → 1/2 → 1/4 → 1/8.', ['1/3', '1/6', '1/4']),
])


@t29.add('C3', (1, 2, 3, 4), 'numerical')
def t29_calc(r, D):
    h = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30])
    unit = r.choice(['hours', 'days', 'minutes', 'years'])
    n = r.choice([2, 3, 4, 5]) if D >= 2 else r.choice([1, 2, 3])
    A0 = r.choice([800, 960, 1200, 1600, 2400, 3200, 6400])
    A = A0 / 2 ** n
    m = r.choice(['remain', 'halflife']) if D >= 3 else 'remain'
    if m == 'remain':
        stem = f'A sample has an activity of {A0} Bq. Its half-life is {h} {unit}. Calculate its activity after {h * n} {unit}.'
        return {'stem': stem, 'answer': f'{sf(A)} Bq', 'key': f'{h * n} {unit} = {n} half-lives; {A0} ÷ 2^{n} = {sf(A)} Bq.'}
    return {'stem': f'The activity of a source falls from {A0} Bq to {sf(A)} Bq in {h * n} {unit}. Calculate its half-life.', 'answer': f'{h} {unit}',
            'key': f'{A0} → {sf(A)} is {n} halvings; half-life = {h * n}/{n} = {h} {unit}.'}


@t29.add('C4', (3, 4, 5), 'multi_step')
def t29_bg(r, D):
    bg = r.choice([20, 30, 40])
    h = r.choice([2, 3, 5])
    c0 = r.choice([640, 800, 960, 1280])
    t = h * 3
    measured = c0 / 8 + bg
    return {'stem': f'A Geiger counter records {c0 + bg} counts/min near a source. The background count is {bg} counts/min. The half-life is {h} minutes. Calculate the count rate the counter will record after {t} minutes.',
            'answer': f'{sf(measured)} counts/min', 'key': f'Corrected rate = {c0 + bg} − {bg} = {c0}; {t} min = 3 half-lives → {c0}/8 = {sf(c0 / 8)}; add background back: {sf(measured)} counts/min. Not subtracting background is the usual error.'}


@t29.add('C2', (2, 3, 4), 'explain')
def t29_choose(r, D):
    use = r.choice([('a medical tracer injected into a patient', 'short (hours)', 'gamma', 'it must be detected outside the body and should not stay active in the body for long'),
                    ('a thickness gauge for paper production', 'long (years)', 'beta', 'the count must not fall noticeably during use; beta is partly absorbed by paper so changes in thickness change the count'),
                    ('a smoke detector', 'long (centuries)', 'alpha', 'alpha ionises air strongly over a short range and is stopped by smoke; long half-life means it lasts the detector’s life'),
                    ('tracing leaks in an underground water pipe', 'short (days)', 'gamma', 'gamma passes through soil to the detector; short half-life so the water is not contaminated for long')])
    return {'stem': f'Explain what half-life and type of radiation would be best for {use[0]}.', 'answer': f'Half-life {use[1]}; {use[2]} radiation, because {use[3]}.',
            'key': '1 mark half-life; 1 mark radiation type; 1 mark reason.'}


t30 = topic('Safety precautions and uses of radiation', 'safety', 'uses of radioactivity', 'precautions', 'dose')
t30.fixed('C1', (1, 2), [
    ('Which is a correct safety precaution when handling radioactive sources in school?', 'Use tongs and keep the source pointed away from people', 'Increase distance, reduce time, use shielding; never handle with bare hands.', ['Hold the source in your hand briefly', 'Keep the source in your pocket', 'Look directly into the source']),
    ('Why are radioactive sources stored in lead-lined boxes?', 'Lead absorbs radiation, reducing exposure', 'Dense lead absorbs β and reduces γ.', ['Lead makes the source decay faster', 'Lead keeps the source cool', 'Lead turns gamma into alpha']),
])
t30.fixed('C2', (2, 3, 4), [
    ('Explain the difference between irradiation and contamination.', 'Irradiation is exposure to radiation from an external source (you do not become radioactive); contamination is when radioactive material gets onto or into the body or object, so it keeps emitting radiation.', '1 mark each.'),
    ('Explain why ionising radiation can cause cancer.', 'It ionises atoms in cells, damaging DNA; mutated cells can divide uncontrollably.', '1 mark each.'),
])


@t30.add('C4', (3, 4, 5), 'long')
def t30_eval(r, D):
    sc = r.choice([
        'A town council is deciding whether to allow food irradiation (gamma rays) at a local factory. Evaluate the benefits and risks.',
        'A hospital plans to use a radioactive tracer with a half-life of 6 hours for scanning patients. Discuss whether this is a sensible choice and what precautions are needed.',
    ])
    return {'stem': sc, 'answer': 'Benefits: kills microorganisms/gives clear diagnosis; the item does not become radioactive (irradiation not contamination); short or controlled exposure. Risks: workers/patients receive dose; source must be shielded and handled remotely; long-term storage of sources. Conclusion with justification.',
            'key': '1 mark each: benefit; irradiation vs contamination; risk to people; precaution (shielding/distance/time/half-life choice); justified conclusion (max 5).'}


CHAPTERS[10] = [t27, t28, t29, t30]

# =========================================================== 11 Earth and the Solar System
t31 = topic('The Earth, Moon and Sun', 'earth', 'moon', 'seasons', 'day and night', 'orbit of the earth')
t31.fixed('C1', (1, 2), [
    ('What causes day and night on Earth?', 'The Earth rotating on its axis once every 24 hours', 'Rotation (spin) about the axis; orbit takes a year.', ['The Earth orbiting the Sun', 'The Moon blocking the Sun', 'The Sun orbiting the Earth']),
    ('How long does the Earth take to orbit the Sun?', 'About 365 days', 'One orbit = one year ≈ 365¼ days.', ['24 hours', 'About 28 days', 'About 30 years']),
    ('Why do we see phases of the Moon?', 'Different amounts of the Moon’s sunlit half are visible from Earth as it orbits', 'The Moon reflects sunlight; its orbit changes how much of the lit side faces us.', ['The Earth’s shadow covers different amounts of the Moon', 'The Moon produces less light each night', 'Clouds block part of the Moon']),
    ('What causes the seasons on Earth?', 'The tilt of the Earth’s axis', 'The tilted axis changes the angle and length of daylight through the year.', ['The changing distance from the Sun', 'The Moon’s orbit', 'The Earth’s rotation speed changing']),
])
t31.fixed('C2', (2, 3, 4), [
    ('Explain why it is summer in the Southern Hemisphere when it is winter in the Northern Hemisphere.', 'The tilt of the axis means the Southern Hemisphere is tilted towards the Sun at that time: longer days and more direct sunlight, while the north is tilted away.', '1 mark: tilt; 1 mark: angle/day length effect.'),
    ('Explain why the Moon always shows the same face to the Earth.', 'It rotates on its axis in the same time it takes to orbit the Earth (about 27 days).', '1 mark each.'),
])


@t31.add('C3', (2, 3), 'explain')
def t31_sun(r, D):
    c = r.choice([('Singapore', 'near the equator'), ('Oslo', 'at a high northern latitude'), ('Cape Town', 'in the Southern Hemisphere'), ('Reykjavik', 'near the Arctic Circle')])
    return {'stem': f'Explain why the length of daylight in {c[0]}, which is {c[1]}, varies the way it does through the year.',
            'answer': 'Near the equator day length stays about 12 h all year; at high latitudes it varies greatly (long summer days, short winter days), because the tilt changes how much of each latitude circle is lit.' ,
            'key': '1 mark: tilt of axis; 1 mark: correct pattern for that location.'}


t32 = topic('The Solar System and orbits', 'solar system', 'planets', 'orbital speed', 'gravitational field strength', 'comets')
t32.fixed('C1', (1, 2), [
    ('Which list shows planets in order from the Sun?', 'Mercury, Venus, Earth, Mars, Jupiter', 'Order: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.', ['Venus, Mercury, Earth, Jupiter, Mars', 'Mercury, Earth, Venus, Mars, Saturn', 'Mars, Earth, Venus, Mercury, Jupiter']),
    ('What keeps planets in orbit around the Sun?', 'The gravitational attraction of the Sun', 'Gravity provides the force towards the centre.', ['Magnetic forces', 'Air resistance', 'The planets’ own light']),
    ('The four outer planets are mainly', 'large and made of gas', 'Inner planets: small and rocky; outer: gas giants (formed further from the Sun where volatile substances condensed).', ['small and rocky', 'made of ice only', 'made of iron']),
    ('As a comet approaches the Sun, its speed', 'increases', 'Gravitational potential energy converts to kinetic energy as it falls closer.', ['decreases', 'stays the same', 'drops to zero']),
])


@t32.add('C3', (2, 3, 4), 'numerical')
def t32_orbit(r, D):
    body = r.choice([('Earth', 1.5e11, 365), ('Mars', 2.28e11, 687), ('Venus', 1.08e11, 225), ('the Moon (around Earth)', 3.84e8, 27.3), ('Jupiter', 7.78e11, 4333)])
    n, rr, days = body
    T = days * 24 * 3600
    v = 2 * math.pi * rr / T
    return {'stem': f'{n.capitalize() if n[0] != "t" else n} has an average orbital radius of {sci(rr, 3)} m and an orbital period of {days} days. Calculate its average orbital speed in km/s.',
            'answer': f'{sf(v / 1000)} km/s', 'key': f'T = {days} × 24 × 3600 = {sci(T, 3)} s; v = 2πr/T = 2π × {sci(rr, 3)} / {sci(T, 3)} = {sf(v)} m/s = {sf(v / 1000)} km/s.'}


@t32.add('C3', (1, 2, 3), 'numerical')
def t32_g(r, D):
    p = r.choice([('Mars', 3.7), ('the Moon', 1.6), ('Jupiter', 24.8), ('Venus', 8.9), ('Mercury', 3.7)])
    m = r.choice([40, 55, 60, 70, 80, 120])
    return {'stem': f'The gravitational field strength on {p[0]} is {p[1]} N/kg. Calculate the weight of a {m} kg astronaut there.', 'answer': f'{sf(m * p[1])} N',
            'key': f'W = mg = {m} × {p[1]} = {sf(m * p[1])} N. Mass stays {m} kg.'}


@t32.add('C4', (3, 4, 5), 'case')
def t32_data(r, D):
    return {'stem': 'Data for some planets (distance from Sun / million km; orbital period / Earth years; surface temperature / °C): Mercury 58, 0.24, 167; Venus 108, 0.62, 464; Earth 150, 1.0, 15; Mars 228, 1.9, −65; Jupiter 778, 11.9, −110. (a) Describe the trend between distance and orbital period. (b) Venus is hotter than Mercury although it is further from the Sun. Suggest why. (c) Use the data to estimate the orbital period of a planet at 1430 million km and comment on your method.',
            'answer': '(a) Period increases with distance, faster than in proportion. (b) Venus has a very thick CO₂ atmosphere giving a strong greenhouse effect. (c) About 29 years (Saturn); extrapolating the pattern is uncertain because the relationship is not linear.',
            'key': '(a) 1 mark trend + 1 mark non-linear; (b) 1 mark atmosphere/greenhouse; (c) 1 mark sensible estimate 25–35 years, 1 mark comment on extrapolation.'}


CHAPTERS[11] = [t31, t32]

# =========================================================== 12 Stars and the Universe
t33 = topic('The Sun and the life cycle of stars', 'sun as a star', 'life cycle of stars', 'stellar evolution', 'red giant', 'supernova')
t33.fixed('C1', (1, 2), [
    ('The Sun produces energy by', 'nuclear fusion of hydrogen into helium', 'Fusion in the core releases energy.', ['nuclear fission of uranium', 'burning hydrogen with oxygen', 'radioactive decay of carbon']),
    ('Stars form from', 'clouds of gas and dust (nebulae) collapsing under gravity', 'A nebula collapses to a protostar; fusion begins when it is hot enough.', ['exploding planets', 'black holes', 'comets colliding']),
    ('What will a star about the size of the Sun become at the end of its life?', 'A white dwarf', 'Red giant → planetary nebula → white dwarf.', ['A black hole', 'A neutron star', 'A supernova']),
    ('What may be left after a supernova of a very massive star?', 'A neutron star or a black hole', 'Massive stars: red supergiant → supernova → neutron star or black hole.', ['A white dwarf', 'A protostar', 'A main-sequence star']),
    ('The Sun mainly emits radiation in which regions of the spectrum?', 'Infrared, visible and ultraviolet', 'Most energy is in the IR, visible and UV regions.', ['Radio and microwaves only', 'X-rays and gamma only', 'Sound and infrared']),
])
t33.fixed('C2', (2, 3, 4), [
    ('Explain why a main-sequence star stays stable for billions of years.', 'The outward pressure from the hot gas (from fusion energy) balances the inward pull of gravity.', '1 mark each.'),
    ('Explain why elements heavier than iron are thought to form in supernovae.', 'Fusion in stars can build elements only up to iron; the huge energy of a supernova explosion makes heavier nuclei, which are scattered into space.', '1 mark each.'),
    ('Describe the life cycle of a star much more massive than the Sun.', 'Nebula → protostar → main-sequence star → red supergiant → supernova → neutron star or black hole.', '1 mark per two correct stages in order (max 3).'),
])


@t33.add('C4', (3, 4), 'long')
def t33_compare(r, D):
    return {'stem': f'Compare the life cycles of a star like the Sun and a star {r.choice([10, 15, 20, 25])} times more massive, explaining why their end points differ.',
            'answer': 'Both form from a nebula and spend most of their lives fusing hydrogen on the main sequence. The Sun-like star becomes a red giant, sheds a planetary nebula and leaves a white dwarf. The massive star burns faster, becomes a red supergiant and explodes as a supernova, leaving a neutron star or black hole, because its core gravity is strong enough to collapse beyond the white-dwarf stage.',
            'key': '1 mark shared stages; 2 marks Sun-like path; 2 marks massive path; 1 mark reason (mass/gravity) – max 5.'}


t34 = topic('Galaxies and the expanding Universe', 'galaxies', 'light-year', 'redshift', 'big bang', 'hubble', 'cmbr', 'universe')
t34.fixed('C1', (1, 2), [
    ('A light-year is a unit of', 'distance', 'The distance light travels in one year ≈ 9.5 × 10¹⁵ m.', ['time', 'speed', 'brightness']),
    ('Our galaxy is called', 'the Milky Way', 'The Solar System is in the Milky Way, one of billions of galaxies.', ['Andromeda', 'the Solar System', 'Orion']),
    ('Redshift of light from distant galaxies shows that', 'they are moving away from us', 'Wavelength increases (towards red) when source recedes.', ['they are getting hotter', 'they are moving towards us', 'they contain only red stars']),
    ('What is the cosmic microwave background radiation (CMBR)?', 'Microwave radiation filling the Universe, left over from shortly after the Big Bang', 'CMBR was emitted when the Universe became transparent and has been redshifted to microwaves.', ['Radiation from microwave ovens on Earth', 'Light from the Sun reflected by the Moon', 'Radio signals from satellites']),
])
t34.fixed('C2', (2, 3, 4), [
    ('Explain how redshift supports the Big Bang theory.', 'Light from distant galaxies is redshifted, so they are receding; more distant galaxies have bigger redshift and recede faster, so the Universe is expanding from a single point.', '1 mark each.'),
    ('Explain why the CMBR is evidence for the Big Bang.', 'The theory predicts radiation from a hot early Universe, stretched to microwave wavelengths by expansion; it is observed uniformly in every direction.', '1 mark each.'),
])


@t34.add('C3', (2, 3, 4), 'numerical')
def t34_hubble(r, D):
    H = 2.2e-18
    v = r.choice([1.1e6, 2.2e6, 4.4e6, 6.6e6, 1.32e7])
    d = v / H
    return {'stem': f'A galaxy is receding at {sci(v, 2)} m/s. The Hubble constant H₀ is 2.2 × 10⁻¹⁸ per second. Calculate the distance to the galaxy using v = H₀d.',
            'answer': f'{sci(d, 2)} m', 'key': f'd = v/H₀ = {sci(v, 2)} / 2.2 × 10⁻¹⁸ = {sci(d, 2)} m.'}


@t34.add('C3', (2, 3), 'numerical')
def t34_ly(r, D):
    ly = r.choice([4.2, 8.6, 25, 100, 640, 2500])
    m = ly * 9.46e15
    return {'stem': f'A star is {ly} light-years from Earth. Calculate this distance in metres (1 light-year = 9.46 × 10¹⁵ m), and state how long ago the light we see left the star.',
            'answer': f'{sci(m, 3)} m; {ly} years ago', 'key': f'{ly} × 9.46 × 10¹⁵ = {sci(m, 3)} m [2]; light took {ly} years [1].'}


@t34.add('C4', (4, 5), 'multi_step')
def t34_age(r, D):
    H = r.choice([2.2e-18, 2.3e-18, 2.4e-18])
    T = 1 / H
    yrs = T / 3.15e7
    return {'stem': f'Assuming galaxies have always receded at constant speed, the age of the Universe ≈ 1/H₀. Taking H₀ = {sci(H, 2)} s⁻¹, estimate the age of the Universe in seconds and in years (1 year = 3.15 × 10⁷ s), and comment on one assumption.',
            'answer': f'{sci(T, 2)} s ≈ {sci(yrs, 2)} years. Assumes constant expansion rate; in reality the rate has changed.',
            'key': '1 mark 1/H₀; 1 mark seconds; 1 mark years; 1 mark comment.'}


CHAPTERS[12] = [t33, t34]


# =====================================================================================
# Structured multi-part items (Paper 4 style). Each composer mixes a scenario with a
# random subset of parts, so stems stay distinct.
# =====================================================================================
from ._lib import compose, PEOPLE  # noqa: E402

WAVE_SCENES = [
    ('A student sets up a ripple tank with a vibrating bar.', 'water waves'),
    ('A fishing boat at anchor rises and falls as sea waves pass under it.', 'sea waves'),
    ('A rope tied to a wall is shaken up and down steadily by a student.', 'waves on the rope'),
    ('A long slinky spring on a bench is pushed back and forth at one end.', 'longitudinal waves on the spring'),
    ('A signal generator drives a loudspeaker in a school laboratory.', 'sound waves in air'),
    ('A surfer counts the waves arriving at a beach.', 'ocean waves'),
]


def _wave_c4(r, D):
    intro, what = r.choice(WAVE_SCENES)
    f = r.choice([0.2, 0.25, 0.5, 2, 4, 5, 8, 10, 12.5, 20]) if 'sound' not in what else r.choice([170, 256, 340, 425, 512, 680])
    lam = r.choice([0.02, 0.025, 0.04, 0.05, 0.08]) if f > 1 and 'sound' not in what else (r.choice([4, 6, 8, 12, 15]) if f < 1 else r.choice([0.5, 0.8, 1.0, 1.25, 2.0]))
    if 'sound' in what:
        lam = 340 / f
    v = f * lam
    T = 1 / f
    n = r.choice([10, 12, 15, 20])
    intro2 = f'{intro} The {what} have a frequency of {sf(f)} Hz and a wavelength of {sf(lam)} m.'
    parts = [
        lambda r: ('Calculate the speed of the waves.', f'{sf(v)} m/s', f'v = fλ = {sf(f)} × {sf(lam)} = {sf(v)} m/s [2]'),
        lambda r: ('Calculate the period of the waves.', f'{sf(T)} s', f'T = 1/f = {sf(T)} s [2]'),
        lambda r: (f'Calculate how many waves pass a fixed point in {n} s.', f'{sf(f * n)}', f'number = f × t = {sf(f)} × {n} = {sf(f * n)} [1]'),
        lambda r: (f'Calculate the time for a wave to travel {sf(v * n)} m.', f'{n} s', f't = d/v = {sf(v * n)}/{sf(v)} = {n} s [2]'),
        lambda r: ('The frequency is doubled but the medium is unchanged. State the new wavelength and explain.', f'{sf(lam / 2)} m: speed is fixed by the medium, so λ halves.', '1 mark value; 1 mark reason [2]'),
        lambda r: (f'State whether the {what} are transverse or longitudinal and describe the motion of the particles.', ('Longitudinal: particles oscillate parallel to the direction of travel.' if ('longitudinal' in what or 'sound' in what) else 'Transverse: particles oscillate perpendicular to the direction of travel.'), '1 mark type; 1 mark direction of oscillation [2]'),
    ]
    return compose(r, intro2, parts, k=(2, 3, 4), type_='multi_step')


t2.add('C4', (2, 3, 4, 5), 'multi_step')(_wave_c4)
t1.add('C4', (2, 3, 4), 'multi_step')(_wave_c4)


def _refr_c4(r, D):
    f = r.choice([4, 5, 6, 8, 10, 12, 15])
    l1 = r.choice([1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    ratio = r.choice([0.5, 0.6, 0.75, 0.8])
    v1 = f * l1 / 100; v2 = v1 * ratio; l2 = l1 * ratio
    gap = r.choice([1, 1.5, 6, 10])
    intro = r.choice([f'Plane waves of frequency {f} Hz and wavelength {sf(l1)} cm travel across a ripple tank and pass over a sheet of glass that makes the water shallower; their speed there is {sf(v2)} m/s.',
                      f'In a ripple tank the water waves have wavelength {sf(l1)} cm in the deep part. The dipper vibrates at {f} Hz. Over a shallow region the waves move at {sf(v2)} m/s.',
                      f'A model harbour is built in a ripple tank. Waves are produced at {f} Hz with wavelength {sf(l1)} cm in deep water and slow to {sf(v2)} m/s near the model beach.'])
    parts = [
        lambda r: ('Calculate the speed in the deep water.', f'{sf(v1)} m/s', f'v = fλ = {f} × {sf(l1 / 100)} = {sf(v1)} m/s [2]'),
        lambda r: ('Calculate the wavelength in the shallow water.', f'{sf(l2)} cm', f'f unchanged; λ = v/f = {sf(v2)}/{f} = {sf(l2 / 100)} m [2]'),
        lambda r: ('State which quantity does not change as the waves cross into shallow water.', 'Frequency', 'frequency set by source [1]'),
        lambda r: ('Describe what happens to the direction of waves that meet the boundary at an angle, and explain why.', 'They bend towards the normal (refract) because they slow down.', '1 mark direction; 1 mark slowing [2]'),
        lambda r: (f'The waves then pass through a gap {sf(gap * l2)} cm wide. Describe the diffraction pattern.', ('Strong spreading into semicircular wavefronts (gap ≈ λ).' if gap < 2 else 'Little spreading, mainly straight wavefronts with curved edges (gap ≫ λ).'), '1 mark pattern linked to gap/λ; 1 mark wavelength unchanged [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t3.add('C4', (2, 3, 4, 5), 'multi_step')(_refr_c4)
t3.add('C3', (3, 4), 'multi_step')(_refr_c4)
t2.add('C3', (3, 4), 'multi_step')(_refr_c4)


def _em_c4(r, D):
    reg, use, why = r.choice(USES)
    others = [u for u in USES if u[0] != reg]
    o = r.choice(others)
    haz = dict(HAZ).get(reg)
    intro = r.choice([f'A company uses {reg} for {use}.', f'A report describes how {reg} are used for {use}.', f'{person(r)} is researching {use}, which uses {reg}.'])
    f = {'radio waves': 1e8, 'microwaves': 2.4e9, 'infrared': 3e13, 'visible light': 5.5e14, 'ultraviolet': 1e15, 'X-rays': 3e18, 'gamma rays': 3e20}[reg] * r.choice([1, 1.5, 2, 2.5])
    parts = [
        lambda r: ('State the speed of this radiation in a vacuum.', '3.0 × 10⁸ m/s', '[1]'),
        lambda r: (f'A typical frequency used is {sci(f, 2)} Hz. Calculate its wavelength.', f'{sci(3e8 / f, 2)} m', 'λ = c/f [2]'),
        lambda r: ('Explain why this radiation is suitable for this use.', why[0].upper() + why[1:] + '.', '1 mark property; 1 mark link [2]'),
        lambda r: (f'Compare this radiation with {o[0]}, used for {o[1]}, in terms of wavelength and frequency.', f'{reg} has a {"longer" if EM.index(reg) < EM.index(o[0]) else "shorter"} wavelength and {"lower" if EM.index(reg) < EM.index(o[0]) else "higher"} frequency than {o[0]}.', '1 mark each [2]'),
        lambda r: (('Describe one harmful effect of this radiation and one precaution.', f'{haz}; limit exposure time/use shielding.', '1 mark each [2]') if haz else ('Explain why this radiation is considered low-risk at normal intensities.', 'It is low frequency and non-ionising; at low intensity it causes no significant heating.', '[2]')),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


for _t in (t4, t5, t6):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_em_c4)
t4.add('C3', (3, 4), 'multi_step')(_em_c4)


def _magnet_c4(r, D):
    intro = r.choice([
        f'{person(r)} is designing a simple door lock that uses an electromagnet to hold a steel bolt.',
        'A scrap-yard crane uses a large electromagnet to lift old cars.',
        'A recycling plant separates steel cans from aluminium cans on a conveyor belt.',
        'A doorbell uses an electromagnet to make a hammer strike a bell.',
        'A school technician is asked to store some bar magnets and soft-iron rods safely.',
    ])
    parts = [
        lambda r: ('Explain why the core should be made of soft iron rather than steel.', 'Soft iron magnetises and demagnetises easily, so the magnet switches off when the current stops.', '[2]'),
        lambda r: ('State two ways to make the electromagnet stronger.', 'More turns; larger current (or soft-iron core).', '[2]'),
        lambda r: ('Describe how to find the shape and direction of the magnetic field around the magnet.', 'Place a plotting compass at many points and mark the needle direction; join the marks into lines from N to S.', '[2]'),
        lambda r: ('Explain why aluminium is not attracted.', 'Aluminium is not a magnetic material; no magnetism is induced in it.', '[1]'),
        lambda r: ('Explain what happens to an iron object touching the magnet when the current is switched off.', 'Its induced magnetism disappears and it is released/falls.', '[2]'),
        lambda r: ('Suggest why the device could fail if the coil were wound on a steel core.', 'Steel keeps its magnetism, so the object would stay attracted after switching off.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


for _t in (t7, t8, t9):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_magnet_c4)
    _t.add('C3', (3, 4), 'multi_step')(_magnet_c4)


def _static_c4(r, D):
    q = r.choice([1.6e-9, 3.2e-9, 4.8e-9, 6.4e-9, 9.6e-10])
    mat = r.choice([('polythene rod', 'woollen cloth', 'negative'), ('acetate strip', 'cotton cloth', 'positive'), ('balloon', 'jumper', 'negative'), ('perspex ruler', 'silk', 'positive')])
    intro = f'A {mat[0]} is rubbed with a {mat[1]} and becomes {mat[2]}ly charged with a charge of magnitude {sci(q, 2)} C.'
    parts = [
        lambda r: ('Explain, in terms of electrons, how the rod became charged.', f'Electrons moved {"onto" if mat[2] == "negative" else "off"} the {mat[0]} {"from" if mat[2] == "negative" else "onto"} the cloth.', '[2]'),
        lambda r: ('State the charge on the cloth.', f'{"+" if mat[2] == "negative" else "−"}{sci(q, 2)} C (equal and opposite)', '[1]'),
        lambda r: ('Calculate the number of electrons transferred (e = 1.6 × 10⁻¹⁹ C).', f'{sci(q / 1.6e-19, 2)}', 'n = Q/e [2]'),
        lambda r: ('The rod is held near small pieces of paper. Explain why they jump to it.', 'Charge is induced on the paper: opposite charge near the rod, so attraction exceeds repulsion.', '[2]'),
        lambda r: ('Explain why the same experiment does not work with a metal rod held in the hand.', 'Charge flows through the conducting metal and the body to earth.', '[2]'),
        lambda r: ('Describe the electric field pattern around the rod tip if it acts like a point charge.', f'Radial lines {"pointing inwards" if mat[2] == "negative" else "pointing outwards"}.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


for _t in (t10, t11):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_static_c4)
    _t.add('C3', (3, 4), 'multi_step')(_static_c4)

t10b = topic('Conductors and insulators', 'conductors and insulators', 'electron movement', 'conductors')
t10b.fixed('C1', (1, 2), [
    ('Which material is an electrical conductor?', 'Copper', 'Metals have free electrons that move through the lattice.', ['Rubber', 'Glass', 'Dry wood']),
    ('Why do metals conduct electricity?', 'They contain free electrons that can move through the metal', 'Delocalised electrons carry charge.', ['They contain free protons', 'Their atoms are larger', 'They are always hot']),
    ('Why is the outer layer of an electric cable made of PVC?', 'PVC is an insulator, so it stops charge flowing to the user', 'Insulators prevent current reaching people.', ['PVC conducts better than copper', 'PVC makes the current larger', 'PVC is magnetic']),
])
t10b.fixed('C2', (2, 3, 4), [
    ('Explain the difference between an electrical conductor and an insulator in terms of electrons.', 'In conductors, electrons are free to move through the material; in insulators electrons are bound to atoms and cannot move.', '[2]'),
    ('Explain why the charge on a rubbed insulator stays in one place while charge on a conductor spreads out.', 'Electrons cannot move through an insulator, but in a conductor they move freely and repel each other, spreading over the surface.', '[2]'),
    ('Explain how a metal sphere on an insulating stand can be charged by induction using a charged rod.', 'Bring the rod near (electrons repelled or attracted), earth the far side briefly, remove the earth, then the rod: the sphere keeps an opposite charge.', '[3]'),
])
t10b.add('C3', (2, 3, 4), 'multi_step')(_static_c4)
t10b.add('C4', (2, 3, 4, 5), 'multi_step')(_static_c4)
CHAPTERS[4] = [t10, t10b, t11]


def _circ_values(r):
    E = r.choice([6, 9, 12, 24])
    R1, R2, R3 = r.choice([(2, 4, 4), (4, 6, 3), (3, 6, 6), (5, 10, 10), (2, 3, 6), (6, 12, 4), (4, 12, 6)])
    return E, R1, R2, R3


def _circ_c4(r, D):
    E, R1, R2, R3 = _circ_values(r)
    Rp = R2 * R3 / (R2 + R3)
    Rt = R1 + Rp
    I = E / Rt
    V1 = I * R1
    Vp = E - V1
    I2, I3 = Vp / R2, Vp / R3
    intro = r.choice([f'A {E} V battery of negligible internal resistance is connected to a {R1} Ω resistor in series with a parallel combination of {R2} Ω and {R3} Ω resistors.',
                      f'In a circuit, resistor P ({R1} Ω) is in series with two resistors Q ({R2} Ω) and R ({R3} Ω) that are connected in parallel with each other. The supply is {E} V.',
                      f'{person(r)} builds a circuit with a {E} V supply: a {R1} Ω resistor, then a junction leading to {R2} Ω and {R3} Ω resistors in parallel.'])
    parts = [
        lambda r: ('Calculate the combined resistance of the parallel pair.', f'{sf(Rp)} Ω', f'1/R = 1/{R2} + 1/{R3} → {sf(Rp)} Ω [2]'),
        lambda r: ('Calculate the total resistance of the circuit.', f'{sf(Rt)} Ω', f'{R1} + {sf(Rp)} = {sf(Rt)} Ω [1]'),
        lambda r: ('Calculate the current from the battery.', f'{sf(I)} A', f'I = E/R = {E}/{sf(Rt)} = {sf(I)} A [2]'),
        lambda r: (f'Calculate the p.d. across the {R1} Ω resistor.', f'{sf(V1)} V', f'V = IR = {sf(I)} × {R1} [1]'),
        lambda r: (f'Calculate the current in the {R2} Ω resistor.', f'{sf(I2)} A', f'p.d. across pair = {sf(Vp)} V; I = {sf(Vp)}/{R2} [2]'),
        lambda r: (f'The {R3} Ω resistor is removed. State and explain what happens to the battery current.', 'It decreases: total resistance increases (only one path through the parallel section).', '[2]'),
        lambda r: ('Calculate the power dissipated in the whole circuit.', f'{sf(E * I)} W', f'P = EI = {E} × {sf(I)} [2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


for _t in (t16, t17, t18):
    _t.add('C4', (3, 4, 5), 'multi_step')(_circ_c4)
t16.add('C3', (4, 5), 'multi_step')(_circ_c4)
t17.add('C3', (4, 5), 'multi_step')(_circ_c4)

t16b = topic('Circuit symbols and circuit diagrams', 'circuit symbols', 'circuit diagrams', 'drawing and interpreting')
SYMS = [('a cell', 'two parallel lines, one long (positive) and one short'), ('a fixed resistor', 'a small rectangle'), ('a variable resistor', 'a rectangle with an arrow through it'),
        ('a thermistor', 'a rectangle with a line through it and a bent tail (−t°)'), ('a light-dependent resistor', 'a rectangle in a circle with two arrows pointing in'),
        ('a diode', 'a triangle pointing at a bar'), ('a fuse', 'a small rectangle with a line running through it end to end'), ('a lamp', 'a circle with a cross'),
        ('an ammeter', 'a circle containing A'), ('a voltmeter', 'a circle containing V'), ('a switch (open)', 'a break in the line with a hinged lever'), ('a light-emitting diode', 'a diode symbol with two arrows pointing out')]


@t16b.add('C1', (1, 2, 3))
def t16b_sym(r, D):
    n, d = r.choice(SYMS)
    opts, ans = mcq(r, n, [x[0] for x in SYMS if x[0] != n])
    return {'stem': f'A circuit diagram shows {d}. Which component does this symbol represent?', 'options': opts, 'answer': ans, 'key': f'{n.capitalize()} is drawn as {d}.'}


@t16b.add('C2', (2, 3, 4), 'explain')
def t16b_meter(r, D):
    m = r.choice([('ammeter', 'in series', 'it must carry the same current as the component; very low resistance'), ('voltmeter', 'in parallel', 'it measures the energy per coulomb across the component; very high resistance')])
    comp = r.choice(['lamp', 'resistor', 'heater', 'motor', 'thermistor', 'LED'])
    return {'stem': f'A student wants to measure the {"current through" if m[0] == "ammeter" else "p.d. across"} a {comp}. Explain how the {m[0]} should be connected and why.',
            'answer': f'{m[1].capitalize()} with the {comp}, because {m[2]}.', 'key': '1 mark connection; 1 mark reason.'}


@t16b.add('C3', (2, 3, 4), 'explain')
def t16b_interpret(r, D):
    n = r.choice([2, 3])
    sw = r.choice(['S1', 'S2'])
    return {'stem': f'A circuit diagram shows a cell, switch {sw}, an ammeter and {n} lamps in series, with a voltmeter across the last lamp. Describe how the readings change when {sw} is opened, and explain.',
            'answer': 'Both readings fall to zero: opening the switch breaks the only path, so no current flows and no energy is transferred in the lamp.',
            'key': '1 mark both zero; 1 mark single path broken.'}


t16b.add('C4', (3, 4, 5), 'multi_step')(_circ_c4)
t16b.fixed('C2', (2, 3), [
    ('Explain why a diode is drawn with a direction in a circuit diagram.', 'A diode allows current in one direction only (forward bias); the triangle shows the direction of conventional current.', '[2]'),
    ('State the difference between the symbols for a fixed resistor and a variable resistor, and give one use of a variable resistor.', 'Variable resistor has an arrow through the rectangle; used to control current, e.g. a dimmer or volume control.', '[2]'),
])
CHAPTERS[6] = [t16b, t16, t17, t18, t19]


def _safety_c4(r, D):
    P = r.choice([700, 1000, 1500, 2000, 2400, 2800])
    I = P / 230
    fuse = 3 if I < 3 else (5 if I < 5 else 13)
    app = r.choice(['kettle', 'toaster', 'hair dryer', 'iron', 'heater', 'microwave oven'])
    intro = f'A {P} W metal-cased {app} is connected to the 230 V mains with a three-pin plug.'
    parts = [
        lambda r: ('Calculate the normal working current.', f'{sf(I)} A', f'I = P/V = {P}/230 [2]'),
        lambda r: ('Choose a fuse from 3 A, 5 A and 13 A and justify the choice.', f'{fuse} A', 'just above working current [2]'),
        lambda r: ('Explain how the earth wire and fuse protect the user if the live wire touches the case.', 'Large current flows through the low-resistance earth wire, melting the fuse and disconnecting the live supply.', '[3]'),
        lambda r: ('Explain why the cable to the appliance must not be too thin.', 'A thin cable has more resistance and would overheat with this current, risking fire.', '[2]'),
        lambda r: ('State one advantage of a residual current circuit breaker over a fuse.', 'It acts faster and can be reset.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t19.add('C4', (2, 3, 4, 5), 'multi_step')(_safety_c4)
t19.add('C3', (2, 3, 4), 'multi_step')(_safety_c4)
t15.add('C4', (3, 4, 5), 'multi_step')(_safety_c4)


def _qit_c4(r, D):
    I = r.choice([0.2, 0.4, 0.5, 1.2, 1.5, 2.5])
    V = r.choice([3, 6, 9, 12])
    t = r.choice([30, 60, 120, 300, 600])
    Q = I * t; W = Q * V; R = V / I
    intro = r.choice([f'A {V} V battery drives a current of {sf(I)} A through a lamp for {t} s.', f'In a torch, the battery has an e.m.f. of {V} V and the bulb draws {sf(I)} A. It is switched on for {t} s.',
                      f'A small motor connected to a {V} V supply takes a current of {sf(I)} A while running for {t} s.'])
    parts = [
        lambda r: ('Calculate the charge that passes through the device.', f'{sf(Q)} C', 'Q = It [2]'),
        lambda r: ('Calculate the energy transferred by the battery.', f'{sf(W)} J', f'W = QV = {sf(Q)} × {V} [2]'),
        lambda r: ('Calculate the resistance of the device when working.', f'{sf(R)} Ω', 'R = V/I [2]'),
        lambda r: ('Calculate the power of the device.', f'{sf(V * I)} W', 'P = IV [2]'),
        lambda r: ('Explain what is meant by the e.m.f. of the battery.', 'The energy transferred by the battery per unit charge moved around the complete circuit.', '[2]'),
        lambda r: (f'Calculate the number of electrons passing in {t} s (e = 1.6 × 10⁻¹⁹ C).', f'{sci(Q / 1.6e-19, 2)}', 'n = Q/e [2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


for _t in (t12, t13, t14, t15):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_qit_c4)
t12.add('C4', (2, 3, 4, 5), 'multi_step')(_qit_c4)
t13.add('C3', (3, 4, 5), 'multi_step')(_qit_c4)


def _motor_c4(r, D):
    intro = r.choice(['A loudspeaker contains a coil attached to a paper cone, placed in the field of a permanent magnet.', 'A simple d.c. motor has a rectangular coil between the poles of two magnets, connected through a split-ring commutator.',
                      'An electric fan contains a d.c. motor powered by a 12 V battery.', 'A wire is placed between the poles of a U-shaped magnet and connected to a power supply through a switch.',
                      'A beam of electrons enters a region of uniform magnetic field at right angles to the field.'])
    parts = [
        lambda r: ('Explain why there is a force.', 'The magnetic field of the current (moving charges) interacts with the field of the magnet.', '[2]'),
        lambda r: ("State the rule used to predict the direction of the force and what each finger represents.", "Fleming's left-hand rule: first finger field, second finger current, thumb motion.", '[2]'),
        lambda r: ('State two ways to increase the size of the force.', 'Increase the current; use a stronger magnet (or more turns).', '[2]'),
        lambda r: ('State what happens if both the current and the field are reversed.', 'The force stays in the same direction.', '[1]'),
        lambda r: ('Explain the role of the split-ring commutator in keeping rotation continuous.', 'It reverses the current every half turn so the turning effect stays in the same direction.', '[2]'),
        lambda r: ('Describe the effect of replacing the d.c. supply with an a.c. supply.', 'The force reverses direction many times a second, so the object vibrates (as in a loudspeaker).', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t20.add('C4', (2, 3, 4, 5), 'multi_step')(_motor_c4); t20.add('C3', (3, 4), 'multi_step')(_motor_c4)
t21.add('C4', (2, 3, 4, 5), 'multi_step')(_motor_c4); t21.add('C3', (3, 4), 'multi_step')(_motor_c4)
t9.add('C4', (2, 3, 4, 5), 'multi_step')(_motor_c4)
t20b = topic('Force on beams of charged particles', 'beams of charged particles', 'charged particles in a magnetic field', 'electron beam')
t20b.fixed('C1', (1, 2), [
    ('A beam of electrons moves at right angles to a magnetic field. Its path is', 'curved', 'The force is perpendicular to the velocity, so the beam follows a curved (circular) path.', ['straight and faster', 'straight and slower', 'unchanged']),
    ('Compared with the force on electrons, the force on a beam of protons moving the same way in the same field is', 'in the opposite direction', 'Opposite charge, opposite force direction.', ['in the same direction', 'zero', 'along the field lines']),
])
t20b.fixed('C2', (2, 3, 4), [
    ('Explain why a magnetic field does not change the speed of an electron moving at right angles to it.', 'The force is always perpendicular to the motion, so it changes the direction only; no work is done on the electron.', '[2]'),
    ('Explain why electrons travelling parallel to a magnetic field are not deflected.', 'A moving charge feels no force when its motion is parallel to the field lines.', '[2]'),
])
t20b.add('C3', (2, 3, 4), 'multi_step')(_motor_c4); t20b.add('C4', (3, 4, 5), 'multi_step')(_motor_c4)
CHAPTERS[7] = [t9, t20, t21, t20b]


def _induct_c4(r, D):
    Vp = r.choice([230, 240, 11000, 25000])
    Np = r.choice([400, 500, 800, 1000, 1200, 2000])
    Ns = r.choice([20, 40, 50, 60, 100, 4000, 8000])
    Vs = Vp * Ns / Np
    Is = r.choice([0.5, 1, 2, 4])
    intro = r.choice([f'A transformer has {Np} primary turns and {Ns} secondary turns. The primary is connected to a {Vp:,} V a.c. supply.',
                      f'An engineer tests a transformer: primary {Vp:,} V a.c., {Np} turns; secondary {Ns} turns.',
                      f'A transformer at a substation has a primary voltage of {Vp:,} V. The turns ratio Np : Ns is {Np} : {Ns}.'])
    parts = [
        lambda r: ('Calculate the output voltage.', f'{sf(Vs)} V', f'Vs = Vp × Ns/Np [2]'),
        lambda r: ('State whether it is a step-up or step-down transformer.', 'step-up' if Ns > Np else 'step-down', '[1]'),
        lambda r: (f'The secondary current is {sf(Is)} A. Calculate the primary current, assuming 100% efficiency.', f'{sf(Vs * Is / Vp)} A', 'VpIp = VsIs [2]'),
        lambda r: ('Explain how an e.m.f. is induced in the secondary coil.', 'Alternating current in the primary produces a changing magnetic field in the iron core, which links the secondary and induces an e.m.f.', '[3]'),
        lambda r: ('Explain why the transformer would not work with a d.c. supply.', 'A steady current gives a constant field; no change in field so no e.m.f. induced.', '[2]'),
        lambda r: ('Explain why the core is made of soft iron.', 'It is easily magnetised and demagnetised, concentrating the changing field to link both coils.', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


def _gen_c4(r, D):
    rps = r.choice([5, 10, 25, 50])
    gen = r.random() < 0.6
    if gen:
        intro = r.choice([f'A bicycle dynamo has a magnet that spins inside a coil {rps} times per second.', f'A model a.c. generator has a coil rotating {rps} times per second between two magnets.',
                          f'A small wind turbine drives a coil that rotates {rps} times per second in a magnetic field.'])
    else:
        intro = r.choice(['A student pushes a bar magnet into a coil connected to a sensitive centre-zero meter, then pulls it out.', 'A magnet is dropped through a vertical coil connected to a data logger.',
                          'A coil is connected to a galvanometer and a magnet is moved in and out of it.'])
    parts = [
        lambda r: ('Explain why an e.m.f. is induced.', 'The coil cuts / experiences a changing magnetic field.', '[2]'),
        lambda r: ('State two ways of increasing the induced e.m.f.', 'Move/rotate faster; stronger magnet; more turns (any two).', '[2]'),
        lambda r: ("Use Lenz's law to explain why there is a force opposing the motion when current flows.", 'The induced current produces a field that opposes the change/motion, so extra work is needed.', '[2]'),
    ]
    if gen:
        parts += [lambda r: ('State the frequency of the a.c. output.', f'{rps} Hz', '[1]'),
                  lambda r: ('Describe how the output voltage–time graph changes if the speed doubles.', 'Peaks twice as high and twice as many cycles per second.', '[2]'),
                  lambda r: ('State the purpose of the slip rings.', 'They keep the rotating coil connected to the external circuit so the output stays a.c.', '[1]')]
    else:
        parts += [lambda r: ('Describe what the meter shows when the magnet is held still inside the coil.', 'Zero: no change in field, no e.m.f.', '[1]'),
                  lambda r: ('Explain why the meter deflects the opposite way when the magnet is pulled out.', 'The change in field is reversed, so the induced e.m.f. reverses.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t22.add('C4', (2, 3, 4, 5), 'multi_step')(_gen_c4); t22.add('C3', (3, 4), 'multi_step')(_gen_c4)
t23.add('C4', (2, 3, 4, 5), 'multi_step')(_gen_c4); t23.add('C3', (3, 4), 'multi_step')(_gen_c4)
t24.add('C4', (2, 3, 4, 5), 'multi_step')(_induct_c4); t24.add('C3', (2, 3, 4), 'multi_step')(_induct_c4)
t24b = topic('High-voltage transmission and power losses', 'transmission', 'power losses', 'high-voltage', 'p = i²r')
t24b.fixed('C1', (1, 2), [
    ('Which equation gives the power lost as heat in a transmission cable?', 'P = I²R', 'Heating loss depends on the square of the current.', ['P = V/R', 'P = IR', 'P = I/R']),
    ('Doubling the current in a transmission line makes the power lost', 'four times bigger', 'P = I²R: (2I)² = 4I².', ['twice as big', 'half as big', 'unchanged']),
])
t24b.fixed('C2', (2, 3, 4), [
    ('Explain why the national grid uses step-up transformers at power stations and step-down transformers near homes.', 'Stepping up the voltage reduces the current for the same power, reducing I²R heating losses in the cables; stepping down makes the voltage safe for homes.', '[3]'),
    ('Explain why thicker transmission cables reduce energy loss but are not always used.', 'Thicker cables have lower resistance so less I²R loss, but they are heavier and more expensive, needing stronger pylons.', '[2]'),
])
t24b.add('C3', (2, 3, 4), 'numerical')(t24_loss)
t24b.add('C4', (2, 3, 4, 5), 'multi_step')(t24_loss)
t24b.add('C4', (3, 4, 5), 'multi_step')(_induct_c4)
CHAPTERS[8] = [t22, t23, t24, t24b]


def _nuc_c4(r, D):
    nuc = r.choice([('carbon', 'C', 6, 14), ('sodium', 'Na', 11, 24), ('uranium', 'U', 92, 235), ('iodine', 'I', 53, 131), ('cobalt', 'Co', 27, 60), ('strontium', 'Sr', 38, 90), ('radium', 'Ra', 88, 226), ('potassium', 'K', 19, 40)])
    n, s, Z, A = nuc
    intro = r.choice([f'The nuclide {n}-{A} has proton number {Z}.', f'A nucleus of {n} ({s}) has nucleon number {A} and proton number {Z}.', f'{person(r)} is studying the isotope {n}-{A} (Z = {Z}).'])
    parts = [
        lambda r: ('State the number of neutrons in the nucleus.', f'{A - Z}', 'A − Z [1]'),
        lambda r: ('State the number of electrons in a neutral atom.', f'{Z}', '[1]'),
        lambda r: (f'Another isotope of {n} has two more neutrons. State its nucleon number and proton number.', f'{A + 2}; {Z}', '[2]'),
        lambda r: ('Explain why isotopes of an element have the same chemical properties.', 'Same number of protons and electrons; chemistry depends on electrons.', '[2]'),
        lambda r: ('Describe how the alpha-particle scattering experiment showed that the nucleus is small and positive.', 'Most alpha particles passed straight through; a few were deflected through large angles by a small, concentrated positive charge.', '[3]'),
        lambda r: ('State the relative charge and relative mass of a proton, a neutron and an electron.', 'proton +1, 1; neutron 0, 1; electron −1, about 1/1840', '[3]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


t25.add('C4', (2, 3, 4, 5), 'multi_step')(_nuc_c4); t25.add('C3', (3, 4), 'multi_step')(_nuc_c4)
t25b = topic('Proton number, nucleon number and isotopes', 'proton number', 'nucleon number', 'nuclide notation', 'isotopes')
t25b.fixed('C1', (1, 2), [
    ('The nucleon number of a nucleus is the number of', 'protons plus neutrons', 'A = Z + N.', ['protons only', 'neutrons only', 'electrons plus protons']),
    ('Isotopes of the same element have different numbers of', 'neutrons', 'Same Z, different N.', ['protons', 'electrons in a neutral atom', 'electron shells']),
])
t25b.add('C2', (2, 3, 4), 'explain')(t25_iso)
t25b.add('C3', (1, 2, 3), 'numerical')(t25_count)
t25b.add('C3', (3, 4), 'multi_step')(_nuc_c4)
t25b.add('C4', (2, 3, 4, 5), 'multi_step')(_nuc_c4)
t25c = topic('Rutherford alpha-particle scattering', 'rutherford', 'alpha-particle scattering', 'scattering experiment')
t25c.templates = [t for t in t25.templates]
t25c.add('C4', (3, 4, 5), 'case')(t25_scale)


def _fission_c4(r, D):
    intro = r.choice(['A nuclear power station uses uranium-235 as fuel.', 'A science article compares nuclear fission reactors with experimental fusion reactors.', 'Stars such as the Sun release energy in their cores.'])
    parts = [
        lambda r: ('Describe what happens when a uranium-235 nucleus undergoes fission.', 'It absorbs a neutron, becomes unstable and splits into two smaller daughter nuclei, releasing 2–3 neutrons and energy.', '[3]'),
        lambda r: ('Explain how a chain reaction is controlled.', 'Control rods absorb some of the neutrons so that on average one neutron from each fission causes another.', '[2]'),
        lambda r: ('Describe nuclear fusion and state where it occurs naturally.', 'Two light nuclei (e.g. hydrogen) join to form a heavier nucleus (helium), releasing energy; in stars.', '[2]'),
        lambda r: ('Explain why fusion is difficult to achieve on Earth.', 'Very high temperature and pressure are needed to overcome repulsion between positive nuclei; hard to contain.', '[2]'),
        lambda r: ('State one advantage and one disadvantage of fission power compared with burning fossil fuels.', 'No CO₂ emitted during generation; produces long-lived radioactive waste.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t26.add('C4', (2, 3, 4, 5), 'multi_step')(_fission_c4); t26.add('C3', (3, 4), 'multi_step')(_fission_c4)
CHAPTERS[9] = [t25, t25c, t25b, t26]


def _rad_c4(r, D):
    h = r.choice([2, 3, 4, 5, 6, 8])
    unit = r.choice(['minutes', 'hours', 'days'])
    A0 = r.choice([800, 960, 1600, 2400, 3200])
    bg = r.choice([20, 25, 30, 40])
    n = r.choice([2, 3, 4])
    src = r.choice(['an iodine source', 'a technetium tracer', 'a sample of radon gas', 'a protactinium source', 'a sodium tracer'])
    intro = f'A Geiger–Müller tube placed near {src} records a corrected count rate of {A0} counts/min. The background count rate is {bg} counts/min and the half-life is {h} {unit}.'
    parts = [
        lambda r: (f'Calculate the corrected count rate after {h * n} {unit}.', f'{sf(A0 / 2 ** n)} counts/min', f'{n} half-lives: {A0} ÷ 2^{n} [2]'),
        lambda r: (f'Calculate the reading the counter shows after {h * n} {unit}.', f'{sf(A0 / 2 ** n + bg)} counts/min', 'add background [2]'),
        lambda r: ('Explain why the count rate fluctuates even though the half-life is constant.', 'Radioactive decay is random; the number decaying each second varies.', '[2]'),
        lambda r: ('Describe how to measure the background count rate.', 'Remove all sources, record counts over several minutes and find the mean per minute.', '[2]'),
        lambda r: ('State two sources of background radiation.', 'Radon gas from rocks; cosmic rays (or food, buildings, medical).', '[2]'),
        lambda r: (f'Estimate the time for the corrected count rate to fall below {sf(A0 / 16 * 0.9)} counts/min.', f'Just over {4 * h} {unit} (4 half-lives)', '[2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


for _t in (t27, t28, t29, t30):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_rad_c4)
t29.add('C3', (3, 4), 'multi_step')(_rad_c4)
t27.add('C3', (3, 4), 'case')(t27_absorb)
t28.add('C4', (3, 4, 5), 'multi_step')(t28_chain)


def _rad_types_c4(r, D):
    intro = r.choice(['A factory uses a radioactive source and detector to monitor the thickness of aluminium foil.', 'A smoke detector contains a small americium-241 source that emits alpha particles.',
                      'A hospital uses a gamma-emitting tracer to examine a patient’s kidneys.', 'Food is passed through a beam of gamma radiation before packaging.', 'An archaeologist uses carbon-14 to date a wooden bowl.'])
    parts = [
        lambda r: ('State which type of radiation is suitable and explain why.', 'Depends on penetration: alpha for short-range ionisation, beta for thin sheet thickness, gamma to pass through the body or packaging.', '[2]'),
        lambda r: ('Explain why the half-life of the source matters for this use.', 'Long half-life for steady count over years; short half-life for medical use so the dose to the patient is low.', '[2]'),
        lambda r: ('Describe two safety precautions for workers.', 'Shielding (lead), handling with tongs/remote, minimise time, maximise distance, wear dosimeter badge (any two).', '[2]'),
        lambda r: ('Explain the difference between irradiation and contamination in this context.', 'Irradiation: exposed to radiation from outside, does not become radioactive; contamination: radioactive material gets on/in the object.', '[2]'),
        lambda r: ('Explain why ionising radiation can be harmful to living cells.', 'It ionises molecules, damaging DNA and causing mutation or cell death.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


for _t in (t27, t30):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_rad_types_c4)
    _t.add('C3', (3, 4), 'multi_step')(_rad_types_c4)
t30.add('C3', (2, 3), 'explain')(t29_choose)


def _solar_c4(r, D):
    body = r.choice([('Earth', 1.5e11, 365), ('Mars', 2.28e11, 687), ('Venus', 1.08e11, 225), ('Mercury', 5.8e10, 88), ('Jupiter', 7.78e11, 4333)])
    g = {'Earth': 9.8, 'Mars': 3.7, 'Venus': 8.9, 'Mercury': 3.7, 'Jupiter': 24.8}[body[0]]
    m = r.choice([50, 60, 75, 90])
    T = body[2] * 86400
    v = 2 * math.pi * body[1] / T
    intro = f'{body[0]} orbits the Sun at an average distance of {sci(body[1], 3)} m with a period of {body[2]} Earth days. The gravitational field strength at its surface is {g} N/kg.'
    parts = [
        lambda r: ('Calculate the average orbital speed.', f'{sf(v)} m/s', 'v = 2πr/T with T in s [3]'),
        lambda r: (f'Calculate the weight of a {m} kg probe on its surface.', f'{sf(m * g)} N', 'W = mg [2]'),
        lambda r: ('State the force that keeps it in orbit and its direction.', 'Gravitational attraction of the Sun, towards the Sun.', '[2]'),
        lambda r: ('Explain why planets further from the Sun have longer orbital periods.', 'They travel a longer distance per orbit and move more slowly because the Sun’s gravitational field is weaker there.', '[2]'),
        lambda r: ('Describe how the accretion model explains the formation of the planets.', 'A rotating disc of gas and dust around the young Sun; particles collided and clumped by gravity into planets; rocky near the Sun, gaseous further out.', '[3]'),
        lambda r: (f'Calculate the time for light to travel from the Sun to {body[0]}.', f'{sf(body[1] / 3e8)} s', 't = d/c [2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


for _t in (t31, t32):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_solar_c4)
t32.add('C3', (3, 4), 'multi_step')(_solar_c4)
t32b = topic('Orbital speed and gravitational field strength', 'orbital speed', 'v = 2πr/t', 'gravitational field strength of planets')
t32b.templates = [t for t in t32.templates if t.name in ('t32_orbit', 't32_g', '_solar_c4')]
t32b.fixed('C1', (1, 2), [
    ('Which equation gives the average orbital speed?', 'v = 2πr/T', 'Distance round the orbit divided by the period.', ['v = πr²/T', 'v = T/2πr', 'v = 2πT/r']),
    ('Gravitational field strength at a planet’s surface depends mainly on', 'the mass and radius of the planet', 'Larger mass → larger g; larger radius → smaller g at the surface.', ['the planet’s distance from the Sun', 'the temperature of the planet', 'the number of moons']),
])
t32b.fixed('C2', (2, 3, 4), [
    ('Explain why an astronaut has the same mass but a different weight on the Moon.', 'Mass is the amount of matter and does not change; weight = mg and g on the Moon is smaller.', '[2]'),
    ('Explain why the strength of the Sun’s gravitational field decreases with distance and how this affects orbital speed.', 'The field spreads out over a larger area further away; planets further away need less speed to stay in orbit, so they move more slowly.', '[2]'),
])
t32c = topic('Planetary data analysis', 'planetary data', 'data analysis', 'surface temperature')
t32c.templates = [t for t in t32.templates if t.name in ('t32_data', '_solar_c4', 't32_orbit')]
t32c.fixed('C1', (1, 2), [
    ('In data tables for the planets, which generally increases with distance from the Sun?', 'Orbital period', 'Further planets take longer to orbit.', ['Surface temperature', 'Orbital speed', 'Density']),
    ('Which planet does not follow the trend of decreasing surface temperature with distance from the Sun?', 'Venus', 'Venus is hotter than Mercury because of its thick CO₂ atmosphere.', ['Mars', 'Jupiter', 'Mercury']),
])
t32c.fixed('C2', (2, 3, 4), [
    ('Explain why the outer planets have much lower surface temperatures than the inner planets.', 'They are much further from the Sun, so they receive far less radiation per square metre.', '[2]'),
    ('A student says the orbital period is directly proportional to the distance from the Sun. Use the data for Earth (150 million km, 1 year) and Jupiter (778 million km, 11.9 years) to test this.', 'Distance ratio 5.2, period ratio 11.9: period rises faster than distance, so not directly proportional.', '[2]'),
])
CHAPTERS[11] = [t31, t32, t32b, t32c]


def _stars_c4(r, D):
    v = r.choice([1.1e6, 2.2e6, 3.3e6, 4.4e6, 6.6e6])
    H = 2.2e-18
    d = v / H
    intro = r.choice([f'Light from a distant galaxy shows a redshift that corresponds to a recession speed of {sci(v, 2)} m/s.', f'Astronomers measure the speed of a galaxy moving away from the Milky Way as {sci(v, 2)} m/s.',
                      f'A spectrum of a galaxy shows its absorption lines shifted towards the red end; its speed of recession is {sci(v, 2)} m/s.'])
    parts = [
        lambda r: ('Explain what is meant by redshift.', 'An increase in the observed wavelength of light from a receding source.', '[1]'),
        lambda r: ('Calculate the distance to the galaxy (H₀ = 2.2 × 10⁻¹⁸ s⁻¹).', f'{sci(d, 2)} m', 'd = v/H₀ [2]'),
        lambda r: (f'Convert the distance to light-years (1 ly = 9.5 × 10¹⁵ m).', f'{sci(d / 9.5e15, 2)} light-years', '[2]'),
        lambda r: ('Explain how redshift data support the Big Bang theory.', 'More distant galaxies recede faster, so the Universe is expanding from an initial point.', '[2]'),
        lambda r: ('State one other piece of evidence for the Big Bang.', 'Cosmic microwave background radiation.', '[1]'),
        lambda r: ('Estimate the age of the Universe from H₀ and state an assumption.', f'1/H₀ ≈ {sci(1 / H, 2)} s ≈ 1.4 × 10¹⁰ years; assumes constant expansion rate.', '[3]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


def _life_c4(r, D):
    m = r.choice([1, 2, 8, 12, 20, 30])
    intro = r.choice([f'A star of about {m} solar mass{"es" if m > 1 else ""} has just formed from a nebula.', f'Astronomers study a main-sequence star with {m} times the mass of the Sun.', f'A documentary follows the life of a star with {m} times the Sun’s mass.'])
    big = m >= 8
    parts = [
        lambda r: ('Describe how the star formed.', 'Gravity pulled gas and dust in a nebula together; the protostar heated up until fusion of hydrogen began.', '[2]'),
        lambda r: ('Explain why the star is stable during its main-sequence stage.', 'Outward thermal pressure balances the inward gravitational force.', '[2]'),
        lambda r: ('Describe the later stages of the star’s life.', 'Red supergiant → supernova → neutron star or black hole.' if big else 'Red giant → planetary nebula → white dwarf.', '[3]'),
        lambda r: ('Explain why elements formed in stars end up in planets.', 'Supernovae scatter heavy elements into space; they join later nebulae that form new stars and planets.', '[2]'),
        lambda r: ('State the main source of the star’s energy.', 'Nuclear fusion of hydrogen into helium.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t33.add('C4', (2, 3, 4, 5), 'multi_step')(_life_c4); t33.add('C3', (3, 4), 'multi_step')(_life_c4)
t34.add('C4', (2, 3, 4, 5), 'multi_step')(_stars_c4); t34.add('C3', (3, 4), 'multi_step')(_stars_c4)
t33b = topic('The Sun, galaxies and light-years', 'sun as a star', 'galaxies', 'milky way', 'light-years')
t33b.fixed('C1', (1, 2), [
    ('The Sun is', 'a medium-sized star', 'The Sun is a typical main-sequence star of medium size.', ['a planet', 'the largest star in the galaxy', 'a red giant']),
    ('The Milky Way is', 'a galaxy containing billions of stars', 'Our galaxy has 100–400 billion stars.', ['the Solar System', 'a single star', 'a nebula inside the Solar System']),
    ('Light takes about 4.2 years to reach us from the nearest star after the Sun. Its distance is about', '4.2 light-years', 'Distance in light-years = years of travel.', ['4.2 years', '4.2 km', '4.2 × 10⁸ m']),
])
t33b.add('C3', (2, 3), 'numerical')(t34_ly)
t33b.fixed('C2', (2, 3, 4), [
    ('Explain why astronomers use light-years rather than kilometres for distances between stars.', 'The distances are so large that kilometres give unmanageably huge numbers; a light-year is about 9.5 × 10¹² km.', '[2]'),
    ('Explain why we see distant galaxies as they were in the past.', 'Light takes millions or billions of years to reach us, so the light we see left the galaxy long ago.', '[2]'),
    ('The Milky Way is about 100 000 light-years across. Explain what this tells you about the time light takes to cross it.', 'Light would take about 100 000 years to travel from one side to the other.', '[2]'),
])
t33b.add('C4', (2, 3, 4, 5), 'multi_step')(_stars_c4)
t34b = topic('Estimating the age of the Universe', 'age of the universe', 'estimating', 'h0')
t34b.templates = [t for t in t34.templates if t.name in ('t34_age', 't34_hubble', '_stars_c4')]
t34b.fixed('C1', (1, 2), [
    ('The Hubble constant H₀ is the ratio of', 'a galaxy’s recession speed to its distance', 'H₀ = v/d.', ['distance to speed', 'speed to time', 'mass to distance']),
    ('An estimate of the age of the Universe is given by', '1/H₀', 'Time = d/v = 1/H₀ if expansion has been steady.', ['H₀²', 'H₀ × c', 'c/H₀']),
])
t34b.fixed('C2', (2, 3, 4), [
    ('Explain why 1/H₀ gives an estimate of the age of the Universe.', 'If galaxies have moved at constant speed v to distance d, the time taken t = d/v = 1/H₀.', '[2]'),
    ('Suggest why different measurements of H₀ give different estimates of the age of the Universe.', 'Measurements of speed and especially distance have uncertainties; the expansion rate may not have been constant.', '[2]'),
])
CHAPTERS[12] = [t33b, t33, t34, t34b]


# ---------------- extra conceptual (C2) and application (C3) content ----------------
from ._lib import relation  # noqa: E402

CIRC_CTX = ['A student investigates a heating element connected to a power supply.', 'In a school experiment, a resistor is connected to a variable power supply.',
            'An electric kettle element is tested in a laboratory.', 'A torch bulb is connected to a battery pack.', 'A length of nichrome wire is connected in a circuit.',
            'An engineer tests a car headlamp circuit.', 'A phone charger supplies a small circuit board.']
relation(t12, 'C2', (2, 3, 4), 'Q = It', 'charge that flows', {'current': 1, 'time': 1}, CIRC_CTX)
relation(t13, 'C2', (2, 3, 4), 'W = QV', 'energy transferred', {'p.d.': 1, 'charge': 1}, CIRC_CTX)
relation(t14, 'C2', (2, 3, 4), 'R ∝ L/A', 'resistance of the wire', {'length of the wire': 1, 'cross-sectional area of the wire': -1}, ['A wire of constant temperature is used in a circuit.', 'A student compares wires made of the same metal.', 'An engineer chooses a cable for a heater.', 'A constantan wire is tested in a practical.'])
relation(t14, 'C2', (2, 3, 4), 'I = V/R', 'current through the resistor', {'p.d.': 1, 'resistance': -1}, CIRC_CTX)
relation(t15, 'C2', (2, 3, 4), 'P = IV', 'power', {'current': 1, 'p.d.': 1}, CIRC_CTX)
relation(t15, 'C2', (2, 3, 4), 'E = Pt', 'energy transferred', {'power of the appliance': 1, 'time it is switched on': 1}, ['A household appliance is used each evening.', 'A shop runs its air conditioning every day.', 'A family compares electricity bills.'])
relation(t15, 'C3', (3, 4), 'P = I²R', 'power dissipated in the resistor', {'current': 2, 'resistance': 1}, CIRC_CTX)
t12.fixed('C2', (2, 3, 4), [
    ('Explain why the current is the same at all points in a series circuit.', 'Charge is not used up; the same charge passes each point every second because there is only one path.', '[2]'),
    ('Explain the difference between conventional current and electron flow.', 'Conventional current flows from + to −; electrons actually move from − to + around the external circuit.', '[2]'),
    ('Explain why an ammeter must have a very low resistance.', 'It is in series, so a large resistance would reduce the current it is measuring.', '[2]'),
    ('Explain why a current of 2 A for 5 s moves the same charge as 1 A for 10 s.', 'Q = It; 2 × 5 = 1 × 10 = 10 C.', '[2]'),
    ('A student says current is "used up" by a lamp. Explain why this is wrong.', 'The same current flows in and out of the lamp; energy, not charge, is transferred in the lamp.', '[2]'),
    ('Describe what an analogue ammeter and a digital ammeter have in common and one advantage of the digital one.', 'Both are connected in series and measure current; the digital one avoids parallax and reading errors.', '[2]'),
])
t13.fixed('C2', (2, 3, 4), [
    ('Explain the difference between e.m.f. and potential difference.', 'e.m.f. is the energy given per unit charge by a source; p.d. is the energy transferred per unit charge by a component.', '[2]'),
    ('Explain why a voltmeter must have a very high resistance.', 'It is connected in parallel and should take almost no current, so it does not change the circuit.', '[2]'),
    ('Explain why the p.d.s across two lamps in series add up to the e.m.f. of the cell.', 'Energy given to each coulomb by the cell equals the energy transferred by it in the lamps (conservation of energy).', '[2]'),
    ('Explain why two identical lamps in parallel each have the full battery p.d. across them.', 'Each branch connects directly across the battery terminals, so each coulomb transfers the full energy in one lamp.', '[2]'),
])
t14.fixed('C2', (2, 3, 4), [
    ('Explain why the I–V graph for a filament lamp curves.', 'As current rises the filament heats up, its resistance increases, so current rises less steeply.', '[2]'),
    ('Explain why a thermistor can be used as a temperature sensor.', 'Its resistance changes a lot with temperature (NTC: falls as it gets hotter), changing current/p.d.', '[2]'),
    ('Explain why copper is used for connecting wires but nichrome for heating elements.', 'Copper has very low resistance so little energy is wasted; nichrome has higher resistance so it heats up.', '[2]'),
])
t15.fixed('C2', (2, 3, 4), [
    ('Explain why a 3 kW heater costs more to run for an hour than a 100 W lamp.', 'Energy = power × time; the heater transfers 30 times as much energy each hour and you pay per kWh.', '[2]'),
    ('Explain why the kilowatt-hour is used instead of the joule on electricity bills.', 'A joule is tiny; household use is millions of joules, so kWh gives convenient numbers.', '[2]'),
    ('Explain why an appliance rated "2 kW, 230 V" draws a larger current than one rated "1 kW, 230 V".', 'P = IV with V fixed, so I ∝ P; double the power means double the current.', '[2]'),
])

relation(t22, 'C2', (2, 3, 4), 'induced e.m.f. ∝ rate of change of magnetic field', 'induced e.m.f.', {'speed of the magnet': 1, 'number of turns on the coil': 1},
         ['A magnet is pushed into a coil connected to a voltmeter.', 'A bicycle dynamo lights a lamp.', 'A student drops a magnet through a coil and records the e.m.f.'])
relation(t24, 'C2', (2, 3, 4), 'Vs/Vp = Ns/Np', 'output voltage', {'number of secondary turns': 1, 'number of primary turns': -1}, ['A transformer powers a model railway.', 'A laptop charger contains a transformer.', 'A substation transformer is being redesigned.'])
relation(t24b, 'C2', (2, 3, 4), 'P = I²R', 'power lost in the cables', {'current in the cables': 2, 'resistance of the cables': 1}, ['Electricity is sent along overhead cables.', 'A wind farm sends power to the grid along underground cables.', 'A village is supplied through a long cable.'])
t22.fixed('C2', (2, 3, 4), [
    ('Explain why no e.m.f. is induced if the magnet and coil move together at the same speed.', 'There is no relative movement, so no field lines are cut and the field in the coil does not change.', '[2]'),
    ('Explain why a falling magnet passing through a coil gives a negative pulse after a positive pulse.', 'Entering, the field increases; leaving, it decreases — the change reverses, so the e.m.f. reverses.', '[2]'),
    ('Explain why the second pulse is larger when a magnet falls right through a coil.', 'The magnet is moving faster as it leaves, so field lines are cut faster.', '[2]'),
])
t23.fixed('C2', (2, 3, 4), [
    ('Explain why the output of an a.c. generator reverses direction every half turn.', 'Each side of the coil moves up then down through the field, so the direction of cutting reverses.', '[2]'),
    ('Explain why the output of a generator is zero when the coil is perpendicular to the field.', 'At that instant the coil sides move parallel to the field lines, so no lines are cut.', '[2]'),
    ('Compare the a.c. generator and the d.c. motor in terms of energy changes.', 'Generator: kinetic → electrical; motor: electrical → kinetic.', '[2]'),
    ('Explain why slip rings, not a split-ring commutator, are used in an a.c. generator.', 'Slip rings keep each end of the coil connected to the same brush, so the output alternates.', '[2]'),
])
t24.fixed('C2', (2, 3, 4), [
    ('Explain why transformers become warm in use.', 'Some energy is wasted heating the coils (resistance) and the core (eddy currents).', '[2]'),
    ('Explain why a step-down transformer has a larger output current than input current.', 'Power in = power out (ideal); with a lower voltage the current must be larger.', '[2]'),
])

relation(t29, 'C2', (2, 3, 4), 'activity halves each half-life', 'activity after the same time', {'number of half-lives that pass': 1}, ['A tracer is used in a hospital.'], '')
t27.fixed('C2', (2, 3, 4), [
    ('Explain why gamma radiation passes through most materials while alpha does not.', 'Gamma has no charge and no mass, so it interacts weakly; alpha is large and highly charged and loses energy quickly by ionising.', '[2]'),
    ('Explain why a Geiger counter detects alpha particles only if it is very close to the source.', 'Alpha particles travel only a few cm in air before losing their energy.', '[2]'),
    ('Explain why radon gas is a significant source of background radiation in some homes.', 'Radon from granite rock seeps into buildings; it is breathed in and emits alpha particles inside the lungs.', '[2]'),
])
t28.fixed('C2', (2, 3, 4), [
    ('Explain why the nucleon number does not change in beta decay.', 'A neutron changes into a proton (and electron): the total number of nucleons stays the same.', '[2]'),
    ('Explain why a nucleus may emit gamma radiation after alpha or beta decay.', 'The new nucleus is left with excess energy, which it releases as a gamma ray.', '[2]'),
    ('Explain why radioactive decay is described as spontaneous.', 'It is not affected by external conditions such as temperature, pressure or chemical reactions.', '[2]'),
    ('Explain why a sample with a large number of nuclei gives a fairly predictable count rate even though decay is random.', 'With many nuclei, random variations average out; the fraction decaying per second is constant.', '[2]'),
])
t29.fixed('C2', (2, 3, 4), [
    ('Explain why a decay curve never reaches zero.', 'Each half-life halves the remaining amount; there is always some left (in theory).', '[2]'),
    ('Explain how to find the half-life from a graph of activity against time.', 'Read the time for the activity to fall from any value to half that value; repeat and average.', '[2]'),
])
t26.fixed('C2', (2, 3, 4), [
    ('Explain where the energy released in fission comes from.', 'The total mass of the products is slightly less than the original nucleus plus neutron; the lost mass is released as energy.', '[2]'),
    ('Explain why fission products are dangerous.', 'The daughter nuclei are radioactive and some have long half-lives, so waste must be stored safely for a long time.', '[2]'),
])
t25.fixed('C2', (2, 3, 4), [
    ('Explain why the alpha-scattering experiment had to be done in a vacuum.', 'Alpha particles would be absorbed by air after a few cm, so they would not reach the foil or detector.', '[2]'),
    ('Explain why gold foil was used in the alpha-scattering experiment.', 'Gold can be beaten very thin (few atoms thick) and gold nuclei are large and highly charged, giving clear deflections.', '[2]'),
    ('Explain why an atom is electrically neutral.', 'It has equal numbers of protons (+) and electrons (−).', '[2]'),
    ('Describe the difference between the plum-pudding model and the nuclear model.', 'Plum pudding: positive charge spread through the atom with electrons embedded; nuclear: tiny dense positive nucleus with electrons around it, mostly empty space.', '[2]'),
])
t25b.fixed('C2', (2, 3, 4), [
    ('Explain why two isotopes of the same element have different masses.', 'They have different numbers of neutrons, and each neutron adds mass.', '[2]'),
    ('Explain what the notation ²³⁵₉₂U tells you about the nucleus.', 'Nucleon number 235 (protons + neutrons), proton number 92, so 143 neutrons.', '[2]'),
    ('Explain why the proton number identifies the element.', 'Each element has a unique number of protons; changing it changes the element.', '[2]'),
])


@t25b.add('C3', (2, 3, 4), 'numerical')
def t25b_compare(r, D):
    e = r.choice([('carbon', 6, [12, 13, 14]), ('chlorine', 17, [35, 37]), ('hydrogen', 1, [1, 2, 3]), ('uranium', 92, [234, 235, 238]), ('oxygen', 8, [16, 17, 18]), ('iron', 26, [54, 56, 57])])
    a, b = r.sample(e[2], 2)
    return {'stem': f'Compare the nuclei of {e[0]}-{a} and {e[0]}-{b} (proton number {e[1]}): give the numbers of protons and neutrons in each and state what they have in common.',
            'answer': f'{e[0]}-{a}: {e[1]} p, {a - e[1]} n; {e[0]}-{b}: {e[1]} p, {b - e[1]} n. Same proton number, so the same element (isotopes).',
            'key': '1 mark each nucleus; 1 mark isotopes/same Z.'}


t26.add('C3', (2, 3, 4), 'explain')(lambda r, D: {'stem': f'In a reactor, each fission releases on average {r.choice([2.4, 2.5, 2.6, 3])} neutrons. Explain what fraction of these must, on average, go on to cause another fission for steady power, and how {r.choice(["control rods", "the moderator", "the coolant"])} affects the reactor.',
                                                  'answer': 'Exactly one neutron per fission must cause another (the rest are absorbed or escape). Control rods absorb neutrons to set this rate; the moderator slows neutrons so they cause fission; the coolant removes heat to the boiler.',
                                                  'key': '1 mark: one per fission; 1 mark: role of named component.'})

t31.fixed('C2', (2, 3, 4), [
    ('Explain why we see the Moon even though it does not produce light.', 'It reflects light from the Sun towards the Earth.', '[1]'),
    ('Explain why a lunar eclipse can only happen at full moon.', 'Only at full moon is the Earth between the Sun and Moon, so its shadow can fall on the Moon.', '[2]'),
    ('Explain why the Sun appears to move across the sky from east to west.', 'The Earth rotates from west to east on its axis.', '[2]'),
    ('Explain why one year is about 365 days and one day is 24 hours.', 'A year is one orbit of the Sun; a day is one rotation of the Earth on its axis.', '[2]'),
    ('Explain why the Moon takes about one month to go through all its phases.', 'The Moon orbits the Earth about once a month, changing how much of its lit half we see.', '[2]'),
    ('Explain why the Sun is higher in the sky at noon in summer than in winter.', 'The hemisphere is tilted towards the Sun in summer, so the Sun’s rays arrive more directly.', '[2]'),
])
t32.fixed('C2', (2, 3, 4), [
    ('Explain why the inner planets are rocky while the outer planets are gas giants.', 'Near the young Sun it was too hot for volatile substances to condense, so only rock and metal formed planets; further out, gases and ices could gather into giant planets.', '[3]'),
    ('Explain why a comet’s speed changes during its elliptical orbit.', 'Close to the Sun the gravitational pull is stronger and it gains kinetic energy as it falls in; it slows as it moves away.', '[2]'),
    ('Explain the difference between a planet and a moon.', 'A planet orbits the Sun; a moon orbits a planet.', '[1]'),
    ('Explain why a comet develops a tail near the Sun.', 'Heat vaporises ice and the solar wind and radiation push gas and dust away from the Sun.', '[2]'),
    ('Explain why asteroids are classed as minor planets.', 'They are small rocky bodies orbiting the Sun that have not cleared their orbit and are not massive enough to be planets.', '[2]'),
])
relation(t32b, 'C2', (2, 3, 4), 'v = 2πr/T', 'orbital speed', {'orbital radius': 1, 'orbital period': -1}, ['A satellite orbits the Earth.', 'A space agency plans a probe orbiting Mars.', 'An exoplanet is observed orbiting its star.'])
relation(t32b, 'C2', (2, 3, 4), 'W = mg', 'weight of the lander', {'gravitational field strength': 1, 'mass of the lander': 1}, ['A lander is sent to different planets.', 'A rover is tested for a mission.'])

t34.fixed('C2', (2, 3, 4), [
    ('Explain why the redshift of a galaxy tells us it is moving away.', 'When a source recedes, the waves are stretched, so observed wavelength increases towards the red end.', '[2]'),
    ('Explain why the CMBR is now detected as microwaves rather than as visible or infrared light.', 'Expansion of space has stretched the wavelength of the radiation over billions of years.', '[2]'),
    ('Explain what the Big Bang theory states.', 'The Universe began from a very small, very hot, dense point about 13.8 billion years ago and has been expanding since.', '[2]'),
])
t34.add('C3', (2, 3, 4), 'numerical')(t34_age)
relation(t34, 'C2', (2, 3, 4), 'v = H₀d', 'recession speed of the galaxy', {'distance to the galaxy': 1}, ['Astronomers compare galaxies at different distances.', 'A telescope survey measures many galaxies.'])


@t33.add('C3', (2, 3, 4), 'case')
def t33_hr(r, D):
    star = r.choice([('Betelgeuse', 'red supergiant', 'supernova then neutron star or black hole'), ('Sirius B', 'white dwarf', 'cooling slowly into a black dwarf'), ('Proxima Centauri', 'red dwarf main-sequence star', 'very long main-sequence life, then white dwarf'),
                     ('Rigel', 'blue supergiant', 'supernova'), ('the Crab Nebula', 'supernova remnant containing a neutron star', 'the neutron star cools'), ('Aldebaran', 'red giant (about 1–2 solar masses)', 'planetary nebula and white dwarf')])
    return {'stem': f'{star[0]} is a {star[1]}. State the stage of its life cycle it has reached and predict what will happen to it next, giving a reason.',
            'answer': f'{star[1].capitalize()}; next: {star[2]}, because its fate depends on its mass.', 'key': '1 mark stage; 1 mark prediction; 1 mark reason (mass).'}


@t32.add('C3', (2, 3, 4), 'numerical')
def t32_light(r, D):
    p = r.choice([('Mercury', 5.8e10), ('Venus', 1.08e11), ('Mars', 2.28e11), ('Jupiter', 7.78e11), ('Saturn', 1.43e12), ('Neptune', 4.5e12)])
    t = p[1] / 3e8
    return {'stem': f'{p[0]} is {sci(p[1], 3)} m from the Sun. Calculate how long sunlight takes to reach it, in minutes.', 'answer': f'{sf(t / 60)} minutes', 'key': f't = d/c = {sci(p[1], 3)}/3.0 × 10⁸ = {sf(t)} s = {sf(t / 60)} min.'}


@t10.add('C3', (2, 3, 4), 'explain')
def t10_rub(r, D):
    pairs = [('polythene', 'wool', 'negative', 'positive'), ('acetate', 'cloth', 'positive', 'negative'), ('a balloon', 'hair', 'negative', 'positive'), ('perspex', 'silk', 'positive', 'negative'), ('a plastic comb', 'dry hair', 'negative', 'positive')]
    a, b, ca, cb = r.choice(pairs)
    other = r.choice(['a negatively charged rod', 'a positively charged rod'])
    rep = (ca == 'negative') == ('negatively' in other)
    return {'stem': f'{person(r)} rubs {a} with {b}; {a} becomes {ca}. {a.capitalize()} is then brought near {other} hanging from a thread. Describe and explain what happens, and state the charge on {b}.',
            'answer': f'They {"repel" if rep else "attract"} because {"like" if rep else "unlike"} charges {"repel" if rep else "attract"}. {b.capitalize()} is {cb} (electrons transferred {"to" if ca == "negative" else "from"} {a}).',
            'key': '1 mark attraction/repulsion; 1 mark reason; 1 mark charge on cloth with electron transfer.'}


@t11.add('C3', (2, 3, 4), 'explain')
def t11_field(r, D):
    sc = r.choice([('two parallel metal plates connected to a high-voltage supply', 'uniform field: parallel, equally spaced lines from + plate to − plate'),
                   ('an isolated positive point charge', 'radial lines pointing outwards'), ('an isolated negative point charge', 'radial lines pointing inwards'),
                   ('a positive charge near a negative charge', 'lines curve from the positive to the negative charge'), ('two positive charges close together', 'lines curve away from both charges with a neutral point midway')])
    tc = r.choice(['a small positive charge', 'an electron'])
    return {'stem': f'Describe the electric field pattern for {sc[0]}, and state the direction of the force on {tc} placed in the field.',
            'answer': f'{sc[1].capitalize()}. Force on {tc}: {"along" if "positive" in tc else "opposite to"} the field lines.', 'key': '2 marks pattern with direction; 1 mark force direction.'}


relation(t16, 'C2', (2, 3, 4), 'R_total = R₁ + R₂ and I = V/R', 'current in the series circuit', {'supply p.d.': 1}, CIRC_CTX)
relation(t18, 'C2', (2, 3, 4), 'V_out = V_in × R₂/(R₁ + R₂)', 'output p.d.', {'input p.d.': 1}, ['A potential divider provides a reference voltage for a sensor.', 'A volume control uses a potential divider.', 'A light sensor circuit uses a potential divider.'])
t16.fixed('C2', (2, 3, 4), [
    ('Explain why one broken lamp makes all the lamps in a series circuit go out.', 'There is only one path; a break stops the current everywhere.', '[2]'),
    ('Explain why the p.d. across the larger resistor in a series circuit is greater.', 'The same current flows through both; V = IR so the larger R has the larger share of energy per coulomb.', '[2]'),
    ('Explain why adding cells in series makes lamps brighter.', 'The e.m.f.s add, so a larger p.d. drives a larger current through the lamps.', '[2]'),
    ('Explain why the total resistance of resistors in series is larger than any one of them.', 'Charge must pass through each resistor in turn, so the oppositions add.', '[2]'),
])
t17.fixed('C2', (2, 3, 4), [
    ('Explain why the current from the cell increases when a second lamp is added in parallel.', 'A new path is added, total resistance falls, so the total current rises (each branch takes its own current).', '[2]'),
    ('Explain why the branch with the smaller resistance carries the larger current in a parallel circuit.', 'Each branch has the same p.d.; I = V/R so smaller R gives larger I.', '[2]'),
    ('Explain why a fault in one parallel branch does not stop the others working.', 'Each branch is a separate complete path to the supply.', '[2]'),
    ('Explain why sockets in a ring main are connected in parallel.', 'Each appliance gets the full mains p.d. and can be switched on or off independently.', '[2]'),
])
t18.fixed('C2', (2, 3, 4), [
    ('Explain why replacing the fixed resistor in a potential divider with a variable resistor is useful in a sensor circuit.', 'It lets the user adjust the light level or temperature at which the output switches.', '[2]'),
    ('Explain why the output p.d. of a potential divider is shared in the ratio of the resistances.', 'The same current flows through both resistors, so V = IR is proportional to R.', '[2]'),
    ('Explain how a thermistor and a fixed resistor could be arranged so the output p.d. rises as temperature falls.', 'Take the output across the thermistor: as it cools its resistance rises and it takes a larger share of the p.d.', '[2]'),
    ('Explain why an LDR is suitable for an automatic night light.', 'Its resistance rises greatly in the dark, changing the p.d. share and switching the lamp on.', '[2]'),
])
t19.fixed('C2', (2, 3, 4), [
    ('Explain why touching a switch with wet hands is dangerous.', 'Water conducts and lowers skin resistance, so a dangerous current can flow through the body.', '[2]'),
    ('Explain why overloading a socket with many appliances can cause a fire.', 'Total current becomes large; cables heat up (I²R) and insulation may melt or burn.', '[2]'),
    ('Explain why the switch in a lamp circuit should be in the live wire.', 'When switched off, the lamp fitting is then disconnected from the high voltage.', '[2]'),
])
t16b.fixed('C2', (2, 3, 4), [
    ('Explain why circuit diagrams use standard symbols.', 'Everyone can read them the same way; they are quicker to draw and show connections clearly.', '[2]'),
    ('Explain how the symbol for an LED differs from a diode and why.', 'It has arrows pointing away showing that it emits light when current flows.', '[2]'),
    ('Explain why a variable resistor can be used to change the brightness of a lamp.', 'Changing its resistance changes the total resistance and so the current through the lamp.', '[2]'),
])


@t10b.add('C3', (2, 3, 4), 'explain')
def t10b_sort(r, D):
    mats = r.sample(['copper', 'rubber', 'aluminium', 'glass', 'graphite', 'dry wood', 'steel', 'plastic', 'silver', 'paper'], 4)
    cond = {'copper', 'aluminium', 'graphite', 'steel', 'silver'}
    return {'stem': f'Classify these materials as conductors or insulators and explain the difference in terms of electrons: {", ".join(mats)}.',
            'answer': 'Conductors: ' + ', '.join(m for m in mats if m in cond) + '; insulators: ' + ', '.join(m for m in mats if m not in cond) + '. Conductors have free electrons; insulators do not.',
            'key': '2 marks classification; 1 mark explanation.'}


@t10.add('C3', (2, 3, 4), 'numerical')
def t10_share(r, D):
    q = r.choice([2, 4, 6, 8, 12])
    return {'stem': f'Two identical metal spheres on insulating stands carry charges of +{q} nC and −{q // 2 if q % 2 == 0 else q} nC. They touch briefly and are separated. Calculate the final charge on each and explain.',
            'answer': f'{sf((q - (q // 2 if q % 2 == 0 else q)) / 2)} nC each: electrons move until charge is shared equally between identical spheres; total charge is conserved.',
            'key': '1 mark total; 1 mark shared equally; 1 mark conservation.'}


@t34.add('C3', (2, 3, 4), 'case')
def t34_data(r, D):
    gals = r.sample([('A', 50, 1.1e6), ('B', 120, 2.6e6), ('C', 200, 4.4e6), ('D', 310, 6.8e6), ('E', 400, 8.8e6), ('F', 75, 1.65e6)], 3)
    return {'stem': 'Galaxy data (distance / million light-years; recession speed / m/s): ' + '; '.join(f'{g[0]}: {g[1]}, {sci(g[2], 2)}' for g in gals) + '. Describe the relationship and explain what it suggests about the Universe.',
            'answer': 'Speed is (roughly) directly proportional to distance: further galaxies recede faster. This suggests the Universe is expanding, consistent with the Big Bang.',
            'key': '1 mark proportional/positive correlation; 1 mark expansion; 1 mark Big Bang link.'}


@t33.add('C3', (2, 3, 4), 'explain')
def t33_fusion(r, D):
    stage = r.choice(['protostar', 'main-sequence star', 'red giant', 'white dwarf', 'supernova', 'neutron star'])
    info = {'protostar': 'gas and dust collapsing under gravity and heating up; fusion has not yet started', 'main-sequence star': 'hydrogen fusing into helium in the core; forces balanced',
            'red giant': 'hydrogen in the core used up; outer layers expand and cool, helium fusion begins', 'white dwarf': 'hot, dense core left after outer layers are shed; no fusion, slowly cooling',
            'supernova': 'massive star’s core collapses and the star explodes, forming heavy elements', 'neutron star': 'extremely dense remnant made mostly of neutrons after a supernova'}[stage]
    return {'stem': f'Describe what is happening inside a {stage}, and state the stage that comes {r.choice(["before", "after"])} it for a star of suitable mass.', 'answer': info[0].upper() + info[1:] + '.',
            'key': '2 marks description; 1 mark correct neighbouring stage.'}


@t33b.add('C3', (2, 3, 4), 'numerical')
def t33b_dist(r, D):
    ly = r.choice([2.5e6, 1.6e5, 2.3e4, 8.6, 640, 4.4])
    return {'stem': f'An object is {sf(ly) if ly < 1e4 else sci(ly, 2)} light-years away. Calculate its distance in km (1 ly = 9.5 × 10¹² km) and explain what we are seeing when we look at it.', 'answer': f'{sci(ly * 9.5e12, 2)} km; light that left it {sf(ly) if ly < 1e4 else sci(ly, 2)} years ago.',
            'key': '2 marks distance; 1 mark looking back in time.'}


t20.fixed('C1', (1, 2, 3), [
    ('Which quantity does the thumb represent in Fleming’s left-hand rule?', 'The direction of the force (motion)', 'Thumb = thrust/motion.', ['The field', 'The current', 'The voltage']),
    ('The force on a current-carrying wire in a magnetic field is greatest when the wire is', 'at right angles to the field', 'Force maximum when I ⟂ B.', ['parallel to the field', 'at 30° to the field', 'outside the field']),
    ('Which device uses the motor effect?', 'A loudspeaker', 'A coil in a magnet’s field moves the cone.', ['A transformer', 'A thermistor', 'A light-dependent resistor']),
    ('State one factor that affects the size of the force on a current-carrying wire in a magnetic field.', 'The size of the current (or strength of field, or length of wire in the field).', '[1]'),
])
t21.fixed('C1', (1, 2, 3), [
    ('In a d.c. motor, the brushes', 'press against the commutator to connect the coil to the supply', 'Carbon brushes make sliding contact.', ['reverse the magnetic field', 'hold the magnets in place', 'store charge']),
    ('Which energy transfer happens in an electric motor?', 'Electrical to kinetic', 'Motor: electrical → kinetic (plus some thermal).', ['Kinetic to electrical', 'Chemical to electrical', 'Thermal to electrical']),
    ('What happens to a d.c. motor if the current direction is reversed?', 'It turns the opposite way', 'Reversing current reverses the forces.', ['It stops permanently', 'It turns faster in the same direction', 'Nothing changes']),
    ('Name the part of a d.c. motor that reverses the current every half turn.', 'Split-ring commutator', '[1]'),
])
t9.fixed('C1', (1, 2, 3), [
    ('Which rule gives the direction of the magnetic field around a straight current-carrying wire?', 'The right-hand grip rule', 'Thumb = current, fingers = field.', ["Fleming's left-hand rule", "Lenz's law", "Ohm's law"]),
    ('The magnetic field outside a current-carrying solenoid is similar to that of', 'a bar magnet', 'Solenoid field resembles a bar magnet with N and S ends.', ['a horseshoe magnet’s gap', 'a straight wire', 'a point charge']),
    ('Increasing the current in a straight wire makes the magnetic field around it', 'stronger', 'Field strength increases with current.', ['weaker', 'reverse direction', 'disappear']),
    ('State one use of an electromagnet.', 'Relay, electric bell, scrap-yard crane or magnetic door lock.', '[1]'),
])
t20b.fixed('C1', (1, 2, 3), [
    ('A beam of electrons in a magnetic field experiences a force because', 'moving charges form a current', 'Moving charge = current; motor effect applies.', ['electrons are magnetic poles', 'the field is electric', 'electrons have no charge']),
    ('A beam of alpha particles and a beam of electrons enter the same magnetic field. Their deflections are', 'in opposite directions', 'Opposite charges.', ['in the same direction', 'both zero', 'along the field lines']),
    ('Which change increases the deflection of a beam of electrons in a magnetic field?', 'Using a stronger magnetic field', 'Larger B → larger force.', ['Removing the field', 'Turning the field parallel to the beam', 'Using neutrons instead']),
])
