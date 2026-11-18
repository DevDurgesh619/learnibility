"""CBSE class 9 science families, chapters 9-12 (Sound Waves; Reproduction; Diversity and
Classification; Earth as a System)."""
from __future__ import annotations

from qbank import name, two_names, num, inr
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, sig

S = 'cbse-g9-science-ch'

# ======================= ch09 Sound Waves
# NCERT table: speed of sound at 25 °C (m/s)
MEDIA = [('air (at 0 °C)', 331), ('air (at 25 °C)', 346), ('distilled water', 1498), ('sea water', 1531), ('iron', 5950), ('aluminium', 6420)]

c9s1_defs = [
    ('a mechanical wave', 'a disturbance that travels through a material medium by the vibration of its particles'),
    ('a longitudinal wave', 'a wave in which the particles of the medium vibrate parallel to the direction of propagation of the wave'),
    ('a transverse wave', 'a wave in which the particles of the medium vibrate perpendicular to the direction of propagation of the wave'),
    ('a compression', 'a region of high pressure and density in a longitudinal wave where particles are crowded together'),
    ('a rarefaction', 'a region of low pressure and density in a longitudinal wave where particles are spread apart'),
    ('a medium', 'the substance (solid, liquid or gas) through which sound travels'),
]
c9s1_mc = [
    ('Sound cannot travel through:', 'vacuum', 'water', 'steel', 'air'),
    ('Sound waves in air are:', 'longitudinal', 'transverse', 'electromagnetic', 'both transverse and longitudinal'),
    ('In a sound wave, what travels from the source to the listener?', 'the disturbance (energy)', 'the particles of air', 'the source itself', 'the air as a wind'),
    ('A vibrating tuning fork touched to water makes:', 'the water splash', 'no effect', 'the water freeze', 'the water boil'),
    ('Sound is produced by:', 'vibrating objects', 'objects at rest', 'only metal objects', 'only electrical devices'),
    ('The human voice is produced by vibrations of the:', 'vocal cords', 'eardrum', 'tongue', 'teeth'),
    ('Which travels fastest through a given distance?', 'sound in iron', 'sound in water', 'sound in air', 'sound in vacuum'),
]
c9s1_src = {
    'vocal cords': ['a person singing', 'a child talking', 'a baby crying'],
    'a stretched string': ['a sitar', 'a veena', 'a guitar', 'a violin'],
    'a stretched membrane': ['a tabla', 'a dholak', 'a mridangam'],
    'an air column': ['a flute', 'a shehnai', 'a whistle', 'a conch shell'],
    'a metal plate or bar': ['a school bell', 'a temple bell', 'cymbals (manjira)'],
}
c9s1_why = [
    ('Why can astronauts on the Moon not talk to each other directly, even when standing close?', 'There is no air on the Moon, and sound needs a material medium to travel, so they use radio sets.', '1 mark: no medium. 1 mark: radio used.'),
    ('Why do we hear the sound of an approaching train earlier by putting an ear to the rail?', 'Sound travels much faster in solids (steel) than in air, so it reaches the ear through the rail first.', '1 mark: faster in solids. 1 mark: reaches earlier.'),
    ('Why is sound called a mechanical wave?', 'It needs a material medium, and travels by the vibration of the particles of that medium.', '1 mark: needs medium. 1 mark: particles vibrate.'),
    ('Why do we see a flash of lightning before we hear the thunder?', 'Light travels at 3 × 10⁸ m/s, which is far faster than sound in air (about 344 m/s).', '1 mark: light faster. 1 mark: speeds compared.'),
    ('Explain how sound travels from a vibrating drum to your ear.', 'The drum skin pushes and pulls the air next to it, forming compressions and rarefactions; these pass from layer to layer of air to the ear; the air particles only vibrate about their mean positions.', '1 mark: compressions/rarefactions. 1 mark: particles do not travel.'),
]
c9s1_ar = [
    ('Sound cannot travel through vacuum.', 'Sound is a mechanical wave that needs a material medium.', 'a', 'R explains A.'),
    ('Sound travels faster in iron than in air.', 'Iron is a solid with tightly packed particles.', 'a', 'Particles in solids are closely bound, so the disturbance is passed on faster; R explains A.'),
    ('Sound waves in air are longitudinal.', 'Air particles vibrate perpendicular to the direction of the wave.', 'c', 'A is true; R is false – in sound waves particles vibrate parallel to the direction of propagation.'),
    ('A bell rung inside a jar becomes fainter as air is pumped out.', 'Light cannot travel through vacuum.', 'c', 'A is true; R is false – light can travel through vacuum, and R is not the reason for A.'),
]


def c9s1_time(r):
    md, v = r.choice(MEDIA)
    d = r.choice([500, 1000, 1500, 2000, 3000, 6000])
    t = d / v
    return {'stem': f'How long will sound take to travel {d} m through {md}? (speed of sound in {md} = {v} m/s)',
            'answer': f'{sig(t)} s', 'key': f't = d/v = {d}/{v} = {sig(t)} s.',
            'distractors': [f'{sig(v / d)} s', f'{sig(t * 2)} s', f'{sig(t / 2)} s']}


def c9s1_lightning(r):
    t = r.choice([2, 3, 4, 5, 6, 8, 10])
    v = r.choice([340, 344, 346])
    d = v * t
    nm = name(r)
    return {'stem': f'{nm} sees a lightning flash and hears the thunder {t} s later. How far away is the lightning? (speed of sound in air = {v} m/s; ignore the time taken by light)',
            'answer': f'{d} m ({num(d / 1000, 3)} km)', 'key': f'd = v × t = {v} × {t} = {d} m.',
            'distractors': [f'{d // 2} m', f'{d * 2} m', f'{round(v / t)} m']}


c9s2_defs = [
    ('frequency', 'the number of oscillations (compressions passing a point) per unit time, measured in hertz (Hz)'),
    ('wavelength', 'the distance between two consecutive compressions or two consecutive rarefactions, measured in metres'),
    ('amplitude', 'the maximum displacement of the particles of the medium from their mean position'),
    ('the time period', 'the time taken for one complete oscillation of the density of the medium'),
    ('pitch', 'the characteristic of sound that depends on its frequency; a higher frequency gives a higher pitch'),
    ('loudness', 'the characteristic of sound that depends on the square of the amplitude of the wave'),
    ('timbre (quality)', 'the characteristic that distinguishes two sounds of the same pitch and loudness'),
    ('a tone', 'a sound of a single frequency'),
]
c9s2_mc = [
    ('The unit of frequency is:', 'hertz', 'metre', 'second', 'decibel'),
    ('Pitch of a sound depends on its:', 'frequency', 'amplitude', 'speed', 'wavelength only in vacuum'),
    ('Loudness of a sound depends on its:', 'amplitude', 'frequency', 'time period', 'speed'),
    ('Which has the higher pitch?', 'the buzzing of a mosquito', 'the roar of a lion', 'the beat of a drum', 'the sound of thunder'),
    ('If the frequency of a sound wave doubles in the same medium, its wavelength:', 'is halved', 'doubles', 'stays the same', 'becomes four times'),
    ('Two consecutive compressions are separated by:', 'one wavelength', 'half a wavelength', 'one amplitude', 'one time period'),
    ('The speed of a sound wave in a medium depends mainly on:', 'the nature and temperature of the medium', 'the frequency of the source', 'the amplitude of the wave', 'the loudness of the sound'),
    ('Musical sounds of the same pitch from a sitar and a flute are told apart by their:', 'timbre (quality)', 'frequency', 'speed', 'wavelength'),
]
c9s2_why = [
    ('Why does a woman\'s voice usually sound shriller than a man\'s?', 'Her vocal cords are usually shorter and thinner, so they vibrate with a higher frequency, giving a higher pitch.', '1 mark: higher frequency. 1 mark: pitch.'),
    ('Why does a sound become fainter as we move away from the source?', 'The energy spreads over a larger area, so the amplitude of the wave reaching the ear decreases, and loudness falls.', '1 mark: amplitude decreases. 1 mark: loudness.'),
    ('Distinguish between loudness and intensity of sound.', 'Intensity is the sound energy passing through unit area per second (a physical quantity); loudness is the ear\'s response to it, which also depends on the listener.', '1 mark each.'),
    ('Why does the speed of sound in air increase on a hot day?', 'The speed of sound in a gas increases with temperature, because faster-moving particles pass on the disturbance more quickly.', '1 mark: rises with temperature. 1 mark: reason.'),
]
c9s2_ar = [
    ('A sound of higher frequency has a higher pitch.', 'Pitch is how the brain interprets the frequency of an emitted sound.', 'a', 'R explains A.'),
    ('Loudness of a sound is increased by hitting a drum harder.', 'A harder hit makes the drum skin vibrate with a larger amplitude.', 'a', 'R explains A.'),
    ('In a given medium, a sound of higher frequency has a shorter wavelength.', 'The speed of sound in a medium is fixed under the same physical conditions, so v = fλ.', 'a', 'Since v is fixed, λ = v/f decreases as f rises; R explains A.'),
    ('The speed of sound depends on its frequency.', 'All frequencies of sound travel at the same speed in a given medium.', 'd', 'A is false; R is true.'),
    ('Two sounds of the same pitch and loudness can be told apart.', 'They differ in timbre (quality).', 'a', 'R explains A.'),
]


def c9s2_v(r):
    f, lam, md = r.choice([(500, 0.68, 'air'), (1000, 0.34, 'air'), (200, 1.7, 'air'), (256, 1.3, 'air'), (440, 0.78, 'air'), (250, 1.38, 'air'),
                           (400, 0.86, 'air'), (2000, 0.172, 'air'), (100, 3.44, 'air'), (1000, 1.5, 'water'), (500, 3, 'water'), (2000, 0.75, 'water'),
                           (1000, 5.95, 'iron'), (500, 11.9, 'iron')])
    v = f * lam
    return {'stem': f'A sound wave in {md} has a frequency of {f} Hz and a wavelength of {num(lam, 3)} m. What is its speed?',
            'answer': f'{num(v, 1)} m/s', 'key': f'v = fλ = {f} × {num(lam, 3)} = {num(v, 1)} m/s.',
            'distractors': [f'{num(f / lam, 1)} m/s', f'{sig(lam / f)} m/s', f'{num(f + lam, 2)} m/s']}


def c9s2_lam(r):
    md, v = r.choice(MEDIA)
    f = r.choice([100, 200, 250, 500, 1000, 2000, 5000, 10000])
    lam = v / f
    return {'stem': f'A tuning fork of frequency {f} Hz is sounded in {md}. What is the wavelength of the sound? (speed of sound = {v} m/s)',
            'answer': f'{sig(lam)} m', 'key': f'λ = v/f = {v}/{f} = {sig(lam)} m.',
            'distractors': [f'{sig(f / v)} m', f'{sig(v * f)} m', f'{sig(lam * 2)} m']}


def c9s2_T(r):
    f = r.choice([20, 50, 100, 200, 250, 400, 500, 1000, 2000, 5000, 20000])
    T = 1 / f
    ms = T * 1000
    return {'stem': f'What is the time period of a sound wave of frequency {f} Hz?',
            'answer': f'{sig(T)} s ({sig(ms)} ms)', 'key': f'T = 1/f = 1/{f} = {sig(T)} s.',
            'distractors': [f'{f} s', f'{sig(T * 10)} s', f'{sig(2 / f)} s']}


def c9s2_count(r):
    f = r.choice([50, 100, 200, 256, 400, 500])
    t = r.choice([2, 3, 5, 10, 0.5])
    n = f * t
    return {'stem': f'A source of {f} Hz vibrates for {num(t)} s. How many compressions does it produce, and what is its time period?',
            'answer': f'{num(n)} compressions; T = {sig(1 / f)} s', 'key': f'Number = f × t = {f} × {num(t)} = {num(n)}. T = 1/{f} = {sig(1 / f)} s.'}


def c9s2_graph(r):
    md, v = r.choice(MEDIA)
    T = r.choice([0.001, 0.002, 0.004, 0.005, 0.01])
    f = 1 / T
    lam = v * T
    return {'stem': f'A sound wave travels through {md}. The distance between two consecutive compressions is {num(lam, 3)} m, and a compression passes a point every {num(T, 4)} s. Find (a) the frequency, (b) the speed of the wave.',
            'answer': f'(a) {num(f)} Hz (b) {num(v, 1)} m/s', 'key': f'f = 1/T = 1/{num(T, 4)} = {num(f)} Hz; v = fλ = {num(f)} × {num(lam, 3)} = {num(v, 1)} m/s.'}


def c9s2_compare(r):
    f1 = r.choice([200, 250, 400, 500])
    k = r.choice([2, 4])
    v = r.choice([340, 344])
    l1, l2 = v / f1, v / (f1 * k)
    return {'stem': f'Two sounds of {f1} Hz and {f1 * k} Hz travel through air (v = {v} m/s). Find both wavelengths and state which sound has the higher pitch.',
            'answer': f'{sig(l1)} m and {sig(l2)} m; the {f1 * k} Hz sound has the higher pitch.',
            'key': f'λ = v/f: {v}/{f1} = {sig(l1)} m; {v}/{f1 * k} = {sig(l2)} m. Higher frequency, higher pitch.'}


c9s3_defs = [
    ('an echo', 'the sound heard after reflection from a distant obstacle, at least 0.1 s after the original sound'),
    ('reverberation', 'the persistence of sound in a big hall due to repeated reflections from the walls, ceiling and floor'),
    ('a sound board', 'a curved board placed behind a speaker so that sound reflected from it spreads evenly across the hall'),
    ('a megaphone', 'a horn-shaped tube that sends sound by multiple reflection in one direction without spreading'),
    ('a stethoscope', 'a medical instrument in which the sound of the heartbeat reaches the doctor\'s ears by multiple reflection'),
]
c9s3_mc = [
    ('For an echo to be heard, the minimum time gap between the original and reflected sound is:', '0.1 s', '1 s', '0.01 s', '10 s'),
    ('The minimum distance of an obstacle from the source for an echo to be heard in air (344 m/s) is about:', '17.2 m', '34.4 m', '10 m', '1.72 m'),
    ('Reverberation in an auditorium is reduced by:', 'covering the walls and ceiling with sound-absorbing materials', 'using bare marble walls', 'making the hall larger', 'adding glass windows'),
    ('The ceilings of concert halls are often curved so that:', 'sound reaches all parts of the hall after reflection', 'there is no echo', 'sound is absorbed', 'light is reflected'),
    ('Sound is reflected from a surface following the law that:', 'the angle of incidence equals the angle of reflection', 'the angle of reflection is double the angle of incidence', 'it is never reflected', 'the reflected sound has a higher pitch'),
    ('Which device uses multiple reflection of sound?', 'stethoscope', 'loudspeaker cone', 'microphone', 'telephone wire'),
]
c9s3_why = [
    ('Why are the walls of a cinema hall covered with fibreboard, curtains or rough plaster?', 'These materials absorb sound and reduce repeated reflections, so reverberation is reduced and speech is clear.', '1 mark: absorb sound. 1 mark: reduce reverberation.'),
    ('Why is no echo heard in a small room?', 'The reflected sound returns in less than 0.1 s, because the walls are closer than about 17 m, so it merges with the original sound.', '1 mark: < 0.1 s. 1 mark: distance < 17 m.'),
    ('Why is a soundboard placed behind the stage in large halls?', 'It is a curved board with the speaker at its focus; sound reflected from it spreads evenly towards the audience.', '1 mark: curved reflector. 1 mark: even spread.'),
    ('Why do rolls of thunder sound long when lightning strikes once?', 'The sound is reflected many times from clouds and the land, so the echoes reach us one after another.', '1 mark: multiple reflection. 1 mark: successive echoes.'),
]
c9s3_ar = [
    ('An echo is not heard in a small room.', 'The sensation of sound persists in the brain for about 0.1 s.', 'a', 'The reflected sound returns within 0.1 s and merges with the original; R explains A.'),
    ('A stethoscope works on the principle of multiple reflection of sound.', 'Sound travels faster in solids than in air.', 'b', 'Both are true, but R does not explain A.'),
    ('Excessive reverberation is undesirable in an auditorium.', 'Repeated reflections make speech and music unclear.', 'a', 'R explains A.'),
    ('Sound obeys the laws of reflection.', 'Sound needs a medium to travel.', 'b', 'Both true; R does not explain A.'),
]


def c9s3_echo(r):
    d = r.choice([34, 51, 68, 85, 102, 170, 172, 340, 500])
    v = r.choice([340, 344, 346])
    t = 2 * d / v
    nm = name(r)
    return {'stem': f'{nm} claps standing {d} m from a tall wall. After how long is the echo heard? (speed of sound = {v} m/s)',
            'answer': f'{sig(t)} s', 'key': f't = 2d/v = 2 × {d}/{v} = {sig(t)} s.',
            'distractors': [f'{sig(t / 2)} s', f'{sig(t * 2)} s', f'{sig(v / d)} s']}


def c9s3_dist(r):
    t = r.choice([0.5, 1, 1.5, 2, 3, 4, 5])
    v = r.choice([340, 344, 346])
    d = v * t / 2
    place = r.choice(['a cliff in the Western Ghats', 'a hill near Shimla', 'a tall building in Mumbai', 'a canyon in the Chambal ravines', 'a fort wall in Jaipur'])
    return {'stem': f'A boy shouts towards {place} and hears the echo after {num(t)} s. How far is the reflecting surface? (speed of sound = {v} m/s)',
            'answer': f'{num(d, 1)} m', 'key': f'd = vt/2 = {v} × {num(t)}/2 = {num(d, 1)} m.',
            'distractors': [f'{num(v * t, 1)} m', f'{num(d / 2, 1)} m', f'{num(v / t, 1)} m']}


def c9s3_min(r):
    v = r.choice([331, 340, 344, 346, 1498, 1531])
    d = v * 0.1 / 2
    med = {331: 'air at 0 °C', 340: 'air', 344: 'air at 22 °C', 346: 'air at 25 °C', 1498: 'distilled water', 1531: 'sea water'}[v]
    return {'stem': f'Find the minimum distance of a reflecting surface for an echo to be heard in {med}, where sound travels at {v} m/s. (persistence of hearing = 0.1 s)',
            'answer': f'{num(d, 2)} m', 'key': f'Total path = v × 0.1 = {num(v * 0.1, 1)} m, so d = {num(v * 0.1, 1)}/2 = {num(d, 2)} m.',
            'distractors': [f'{num(v * 0.1, 1)} m', f'{num(d * 4, 1)} m', f'{num(v / 0.1, 1)} m']}


def c9s3_two(r):
    d1 = r.choice([170, 204, 255, 340])
    d2 = r.choice([510, 680, 850, 1020])
    v = 340
    t1, t2 = 2 * d1 / v, 2 * d2 / v
    a, b = two_names(r)
    return {'stem': f'{a} stands between two cliffs, {d1} m from one and {d2} m from the other, and fires a cracker. When are the first and second echoes heard, and what is the gap between them? (v = {v} m/s)',
            'answer': f'First at {sig(t1)} s, second at {sig(t2)} s; gap {sig(t2 - t1)} s.',
            'key': f't = 2d/v: 2 × {d1}/{v} = {sig(t1)} s; 2 × {d2}/{v} = {sig(t2)} s; difference {sig(t2 - t1)} s.'}


c9s4_defs = [
    ('the audible range', 'the range of frequencies from about 20 Hz to 20 000 Hz that the human ear can hear'),
    ('infrasound', 'sound of frequency below 20 Hz, which humans cannot hear'),
    ('ultrasound', 'sound of frequency above 20 kHz, which humans cannot hear'),
    ('SONAR', 'Sound Navigation And Ranging, a device that uses ultrasonic waves to find the distance, direction and speed of underwater objects'),
    ('echocardiography', 'the use of ultrasonic waves reflected from parts of the heart to form an image of the heart'),
    ('ultrasonography', 'a technique that uses ultrasonic waves to form images of internal organs'),
    ('the eardrum (tympanic membrane)', 'a thin membrane in the ear that vibrates when compressions and rarefactions of sound fall on it'),
    ('the cochlea', 'the part of the inner ear that converts vibrations into electrical signals sent by the auditory nerve to the brain'),
]
c9s4_cats = {
    'infrasound': ['sound made by whales to communicate (below 20 Hz)', 'vibrations before an earthquake', 'rhinoceros calls at 5 Hz', 'a simple pendulum swinging at 1 Hz'],
    'audible sound': ['a human voice at 500 Hz', 'a tabla beat at 200 Hz', 'a whistle at 3000 Hz', 'a tuning fork of 256 Hz'],
    'ultrasound': ['a bat\'s squeak at 50 kHz', 'a dog whistle at 25 kHz', 'a SONAR pulse at 40 kHz', 'sound used in ultrasonography at 2 MHz', 'a dolphin click at 100 kHz'],
}
c9s4_mc = [
    ('The audible range of the human ear is:', '20 Hz to 20 kHz', '2 Hz to 2 kHz', '20 kHz to 200 kHz', '0 Hz to 20 Hz'),
    ('Bats find their way in the dark by using:', 'ultrasound', 'infrasound', 'light', 'heat'),
    ('Ultrasound is used to clean electronic parts and spiral tubes because:', 'it can reach places that are hard to reach and shake off dust', 'it heats the parts', 'it is a transverse wave', 'it can be seen'),
    ('In the ear, the vibrations of the eardrum are amplified by:', 'three bones in the middle ear (hammer, anvil, stirrup)', 'the cochlea', 'the outer ear', 'the auditory nerve'),
    ('SONAR is used to measure the:', 'depth of the sea', 'height of a mountain', 'speed of light', 'temperature of water'),
    ('Ultrasound is used to break small stones in the kidney because:', 'its high-energy vibrations break the stones into fine grains', 'it melts them', 'it dissolves them chemically', 'it freezes them'),
    ('Which part of the ear converts pressure variations into electrical signals?', 'cochlea', 'pinna', 'eardrum', 'ear canal'),
]
c9s4_why = [
    ('Why is ultrasound, and not audible sound, used in SONAR?', 'Ultrasound has very high frequency, so it travels along well-defined straight paths without spreading much, and it is not disturbed by other sounds.', '1 mark: straight path. 1 mark: little spreading.'),
    ('Why is ultrasound preferred to X-rays for scanning a foetus in the womb?', 'Ultrasound is harmless to the growing baby, while X-rays can damage tissues.', '1 mark: safe. 1 mark: X-rays harmful.'),
    ('Why can elephants and whales "talk" over long distances without humans hearing them?', 'They use infrasound (below 20 Hz), which is below the human audible range and travels long distances.', '1 mark: infrasound. 1 mark: below 20 Hz.'),
    ('Describe the role of the pinna and the eardrum in hearing.', 'The pinna collects sound and sends it through the ear canal; the eardrum vibrates in and out with the compressions and rarefactions.', '1 mark each.'),
]
c9s4_ar = [
    ('Ultrasound can be used to detect cracks in metal blocks.', 'Ultrasound is reflected back from a crack or flaw in the metal.', 'a', 'R explains A.'),
    ('Humans cannot hear the sound produced by a bat.', 'Bats produce ultrasound, with frequencies above 20 kHz.', 'a', 'R explains A.'),
    ('SONAR uses infrasound.', 'Infrasound travels in straight lines without spreading.', 'd', 'A is false – SONAR uses ultrasound; R is false too, so neither holds.'),
    ('Some animals become disturbed before an earthquake.', 'Earthquakes produce low-frequency infrasound before the main shock waves.', 'a', 'R explains A.'),
]
c9s4_ar[2] = ('SONAR uses ultrasonic waves.', 'Ultrasonic waves travel along well-defined paths without much spreading.', 'a', 'R explains A.')


def c9s4_depth(r):
    t = r.choice([0.8, 1, 1.2, 2, 2.4, 3, 4, 5])
    v = r.choice([1500, 1531])
    d = v * t / 2
    ship = r.choice(['INS Sindhughosh', 'a fishing trawler off Kochi', 'a research ship in the Bay of Bengal', 'a Coast Guard vessel near Visakhapatnam'])
    return {'stem': f'A SONAR on {ship} sends an ultrasonic pulse to the sea bed and receives the echo after {num(t)} s. If sound travels at {v} m/s in sea water, how deep is the sea?',
            'answer': f'{num(d, 1)} m', 'key': f'd = vt/2 = {v} × {num(t)}/2 = {num(d, 1)} m.',
            'distractors': [f'{num(v * t, 1)} m', f'{num(d / 2, 1)} m', f'{num(v / t, 1)} m']}


def c9s4_time(r):
    d = r.choice([750, 1000, 1500, 2296.5, 3062, 4593])
    v = 1531
    t = 2 * d / v
    return {'stem': f'A submarine is {num(d, 1)} m above the sea bed. After how long will its SONAR receive the echo from the sea bed? (speed of sound in sea water = {v} m/s)',
            'answer': f'{sig(t)} s', 'key': f't = 2d/v = 2 × {num(d, 1)}/{v} = {sig(t)} s.',
            'distractors': [f'{sig(d / v)} s', f'{sig(t * 2)} s', f'{sig(v / d)} s']}


def c9s4_class(r):
    f = r.choice([5, 10, 15, 25, 100, 500, 2000, 15000, 25000, 40000, 60000, 100000])
    k = 'infrasound' if f < 20 else ('ultrasound' if f > 20000 else 'audible sound')
    fs = f'{f // 1000} kHz' if f >= 1000 and f % 1000 == 0 else f'{f} Hz'
    return {'stem': f'A sound has a frequency of {fs}. Is it infrasound, audible sound or ultrasound?', 'answer': k,
            'key': f'Audible range 20 Hz–20 kHz; {fs} is {k}.', 'distractors': [x for x in ['infrasound', 'audible sound', 'ultrasound', 'electromagnetic wave'] if x != k]}


def c9s4_bat(r):
    f = r.choice([30000, 40000, 50000, 60000, 80000, 100000])
    v = r.choice([340, 344])
    lam = v / f
    return {'stem': f'A bat emits ultrasound of frequency {f // 1000} kHz in air (v = {v} m/s). Find the wavelength in millimetres, and explain why humans cannot hear it.',
            'answer': f'{sig(lam * 1000)} mm; {f // 1000} kHz is above the upper limit of human hearing (20 kHz).',
            'key': f'λ = v/f = {v}/{f} = {sig(lam)} m = {sig(lam * 1000)} mm. Above 20 kHz.'}


c9_hots = [
    ('A sound wave travels 1.5 km in sea water in 1 s. Its frequency is 1500 Hz. Find its wavelength. If the same source is sounded in air (344 m/s), what will be the new wavelength and will the pitch change?', 'In water λ = 1500/1500 = 1 m. In air λ = 344/1500 = 0.229 m. Frequency (and so pitch) stays the same; only speed and wavelength change.', '1 mark each.'),
    ('A person clapping rhythmically near a 200 m distant wall finds that the echo coincides with the next clap when he claps 50 times a minute. Estimate the speed of sound.', 'Time between claps = 60/50 = 1.2 s = time for 400 m return path; v = 400/1.2 = 333 m/s.', '1 mark time. 1 mark path. 1 mark speed.'),
    ('A stone is dropped into a 44.1 m deep well and the splash is heard 3.13 s later. Find the speed of sound (g = 9.8 m/s²).', 'Fall time: h = ½gt², t = √(2 × 44.1/9.8) = 3 s. Sound takes 0.13 s, so v = 44.1/0.13 ≈ 339 m/s.', '1 mark fall time. 1 mark sound time. 1 mark speed.'),
    ('An auditorium has a marble floor and bare concrete walls, and people complain that speeches are unclear. Explain the cause and suggest three changes.', 'Too much reverberation from repeated reflections. Use curtains or fibreboard panels on walls, carpets on the floor, cushioned seats and perforated false ceilings to absorb sound.', '1 mark cause. 2 marks changes.'),
]


def c9_case(r):
    t = r.choice([1.2, 2, 2.4, 3])
    v = 1531
    d = v * t / 2
    f = r.choice([25000, 40000, 50000])
    return {'stem': (f'Read: A research ship in the Arabian Sea uses SONAR of frequency {f // 1000} kHz. The pulse returns from the sea bed after {num(t)} s. Speed of sound in sea water = {v} m/s.\n'
                     '(i) Is the pulse audible to humans? Why? (ii) Find the depth of the sea. (iii) Find the wavelength of the pulse in sea water. (iv) Why is ultrasound used in SONAR?'),
            'answer': f'(i) No; {f // 1000} kHz is above 20 kHz. (ii) {num(d, 1)} m. (iii) {sig(v / f)} m. (iv) It travels in straight, well-defined paths with little spreading.',
            'key': '1 mark each part.'}


def c9_case2(r):
    d = r.choice([85, 170, 255, 340])
    v = 340
    nm = name(r)
    return {'stem': (f'Read: {nm} visits a large empty hall with bare walls and notices that her voice persists for a long time. Outside, she shouts towards a hill {d} m away and hears an echo. (v = {v} m/s)\n'
                     '(i) What is the persistence of sound in the hall called? (ii) After how long is the echo from the hill heard? (iii) What is the least distance needed for an echo? (iv) Suggest one way to reduce the persistence of sound in the hall.'),
            'answer': f'(i) Reverberation. (ii) {sig(2 * d / v)} s. (iii) 17 m (about 17.2 m at 344 m/s). (iv) Cover the walls with curtains, fibreboard or rough plaster.',
            'key': '1 mark each part.'}


c9_long = [
    ('What is meant by a longitudinal wave? Describe with a diagram how sound travels as compressions and rarefactions in air. Define wavelength, frequency, amplitude and time period, and write the relation between speed, frequency and wavelength.',
     'A wave where particles vibrate parallel to the direction of travel. A vibrating object pushes air forward forming a compression (high density) and moving back forms a rarefaction (low density); these travel outward. Wavelength: distance between two consecutive compressions; frequency: oscillations per second (Hz); amplitude: maximum disturbance from the mean; time period T = 1/f. v = fλ.',
     '1 mark definition; 2 marks propagation; 1 mark terms; 1 mark relation.'),
    ('What is ultrasound? Explain how SONAR works and derive the formula for depth. Write three other uses of ultrasound.',
     'Sound above 20 kHz. SONAR has a transmitter that sends an ultrasonic pulse and a detector that receives its reflection; if the echo returns after t, the pulse travels 2d, so 2d = vt and d = vt/2. Uses: cleaning hard-to-reach parts, detecting cracks in metals, echocardiography, ultrasonography, breaking kidney stones.',
     '1 mark definition; 2 marks working and formula; 2 marks uses.'),
    ('Describe the structure and working of the human ear with a labelled diagram.',
     'Outer ear (pinna and ear canal) collects sound; the eardrum vibrates with compressions and rarefactions; the middle ear bones (hammer, anvil, stirrup) amplify the vibrations and pass them to the inner ear; the cochlea converts them into electrical signals that the auditory nerve carries to the brain.',
     '1 mark outer; 2 marks middle; 2 marks inner.'),
    ('What is an echo? State the conditions for hearing an echo and calculate the minimum distance needed in air at 344 m/s. Explain reverberation and two ways to reduce it in a hall.',
     'Echo: reflected sound heard separately. Conditions: gap ≥ 0.1 s, a large reflecting surface. Minimum distance = 344 × 0.1/2 = 17.2 m. Reverberation: persistence by repeated reflections; reduce with sound-absorbing materials (fibreboard, curtains, rough plaster) and seats of absorbent material.',
     '1 mark echo; 1 mark conditions; 1 mark calculation; 2 marks reverberation.'),
]

# ======================= ch10 Reproduction
c10s1_defs = [
    ('reproduction', 'the process by which living organisms produce new individuals of their own kind'),
    ('asexual reproduction', 'reproduction in which a single parent produces offspring without the fusion of gametes'),
    ('binary fission', 'the division of a parent cell into two equal daughter cells'),
    ('multiple fission', 'the division of a parent cell into many daughter cells at the same time'),
    ('budding', 'asexual reproduction in which a new individual develops as an outgrowth (bud) from the parent'),
    ('fragmentation', 'asexual reproduction in which the body breaks into pieces, each growing into a new organism'),
    ('regeneration', 'the ability of a fully differentiated organism to give rise to new individuals from its body parts'),
    ('DNA copying', 'the making of copies of DNA, which carries the information for inheritance, before a cell divides'),
]
c10s1_cats = {
    'binary fission': ['Amoeba', 'Paramecium', 'bacteria', 'Leishmania'],
    'multiple fission': ['Plasmodium (malaria parasite)', 'some algae such as Chlamydomonas in cysts'],
    'budding': ['yeast', 'Hydra'],
    'fragmentation': ['Spirogyra', 'some sea worms'],
    'regeneration': ['Planaria', 'starfish'],
}
c10s1_cats['multiple fission'] = ['Plasmodium (malaria parasite)', 'encysted Amoeba under unfavourable conditions']
c10s1_mc = [
    ('In Amoeba, binary fission can take place:', 'in any plane', 'only lengthwise', 'only across', 'only in the nucleus'),
    ('Leishmania, which causes kala-azar, divides by binary fission:', 'in a definite plane, lengthwise', 'in any plane', 'into many cells', 'by budding'),
    ('The main advantage of sexual over asexual reproduction is that it:', 'produces variation', 'is faster', 'needs one parent', 'needs less energy'),
    ('Offspring produced by asexual reproduction are:', 'genetically similar to the parent', 'always different from the parent', 'always sterile', 'formed from gametes'),
    ('Small variations in DNA copying are useful because they:', 'help species survive changes in the environment', 'make all offspring identical', 'stop reproduction', 'make cells die'),
    ('Plasmodium reproduces by multiple fission:', 'forming many daughter cells at once', 'forming two equal cells', 'forming buds', 'forming spores on hyphae'),
]
c10s1_why = [
    ('Why is reproduction essential for a species even though it is not needed for an individual to survive?', 'Individuals die, and reproduction keeps the population and species going over generations.', '1 mark: individual survives without it. 1 mark: continuity of species.'),
    ('Why does a population of bacteria grow very fast?', 'Each bacterium divides into two by binary fission in a short time, so numbers double every generation.', '1 mark: binary fission. 1 mark: doubling.'),
    ('Why is variation useful for the survival of a species?', 'If the environment changes (for example, temperature rises), some varied individuals may be able to survive, so the species is not wiped out.', '1 mark: changed environment. 1 mark: some survive.'),
    ('How is regeneration different from reproduction in organisms like Planaria?', 'Regeneration is regrowth of a whole organism from a cut piece by specialised cells; it is not the normal way most organisms reproduce.', '1 mark: from body piece. 1 mark: not usual reproduction.'),
]
c10s1_ar = [
    ('Organisms produced by asexual reproduction show very little variation.', 'Only one parent is involved, and the DNA is copied almost exactly.', 'a', 'R explains A.'),
    ('Amoeba is immortal in the sense that the parent never dies of old age.', 'The parent Amoeba divides into two daughter cells and disappears into them.', 'a', 'R explains A.'),
    ('Hydra can reproduce by budding.', 'Hydra uses regenerative cells for reproduction by budding.', 'a', 'R explains A.'),
    ('Planaria can regenerate from a small piece of its body.', 'Planaria reproduces only by sexual means.', 'c', 'A is true; R is false.'),
]


def c10s1_grow(r):
    t = r.choice([20, 30, 40, 60])
    h = r.choice([2, 3, 4, 5, 6])
    n0 = r.choice([1, 2, 5, 10, 100])
    gens = h * 60 // t
    n = n0 * 2 ** gens
    return {'stem': f'A bacterium divides by binary fission every {t} minutes. Starting with {n0} bacteri{"um" if n0 == 1 else "a"}, how many will be present after {h} hours if none die?',
            'answer': str(n),
            'key': f'Generations = {h} × 60/{t} = {gens}; N = {n0} × 2^{gens} = {n}.',
            'distractors': [str(n0 * gens * 2), str(n0 * 2 ** (gens - 1)), str(n0 * 2 ** (gens + 1))]}


c10s2_defs = [
    ('vegetative propagation', 'the production of new plants from vegetative parts such as root, stem or leaf'),
    ('a spore', 'a tiny reproductive body covered by a thick wall, which grows into a new organism in favourable conditions'),
    ('a sporangium', 'a blob-like structure on a hypha of a fungus such as Rhizopus that contains spores'),
    ('tissue culture', 'growing new plants from cells or tissue taken from the growing tip of a plant in an artificial medium'),
    ('layering', 'artificial vegetative propagation in which a branch is bent to the ground and covered with soil until it roots'),
    ('grafting', 'joining a cut stem of one plant (scion) onto a rooted plant (stock) so they grow as one'),
    ('a cutting', 'a piece of stem with a bud planted in moist soil to grow a new plant'),
]
c10s2_cats = {
    'propagated by leaves': ['Bryophyllum', 'begonia'],
    'propagated by stem cuttings': ['rose', 'sugarcane', 'money plant', 'hibiscus (gudhal)'],
    'propagated by layering': ['jasmine', 'bougainvillea', 'grapevine'],
    'propagated by grafting': ['mango', 'guava', 'citrus (lemon, orange)', 'apple'],
    'propagated by underground stems': ['potato (tuber)', 'ginger (rhizome)', 'onion (bulb)', 'turmeric (rhizome)'],
    'propagated by roots': ['sweet potato', 'dahlia'],
}
c10s2_mc = [
    ('Bryophyllum is propagated by:', 'buds on the margin of its leaves', 'seeds only', 'spores', 'budding of its root'),
    ('Rhizopus (bread mould) reproduces by:', 'spore formation', 'budding', 'binary fission', 'fragmentation'),
    ('Plants such as banana, orange, rose and jasmine have lost the capacity to produce seeds, so they are grown by:', 'vegetative propagation', 'spores', 'pollination only', 'binary fission'),
    ('An advantage of vegetative propagation is that:', 'plants bear flowers and fruits earlier than those grown from seeds', 'it produces many varieties', 'it needs two parents', 'plants are always disease-free'),
    ('The "eyes" of a potato are:', 'buds that grow into new plants', 'roots', 'seeds', 'spores'),
    ('Spores of Rhizopus are protected by:', 'thick walls', 'a fruit', 'a seed coat', 'a cuticle of wax'),
    ('Tissue culture is commonly used to grow:', 'orchids and ornamental plants', 'only wheat', 'only bacteria', 'animals'),
]
c10s2_why = [
    ('Why are bananas and roses grown by vegetative propagation and not from seeds?', 'They have lost the capacity to produce viable seeds, and vegetative propagation gives plants identical to the parent.', '1 mark: no viable seeds. 1 mark: identical plants.'),
    ('Why does bread kept in a damp place become mouldy, while dry bread does not?', 'Spores of Rhizopus are present in the air and need moisture to germinate and grow hyphae.', '1 mark: spores in air. 1 mark: need moisture.'),
    ('Give two advantages of grafting used by mango growers in Ratnagiri.', 'The fruit quality of the desired variety (scion) is kept exactly; the trees fruit earlier on a hardy, established root stock.', '1 mark each.'),
    ('How does tissue culture help farmers?', 'Many disease-free plants identical to a good parent can be produced quickly from a small piece of tissue, even out of season.', '1 mark: many identical. 1 mark: disease-free/fast.'),
]
c10s2_ar = [
    ('Plants grown by vegetative propagation are identical to the parent.', 'They are produced from a single parent without the fusion of gametes.', 'a', 'R explains A.'),
    ('Spores can survive harsh conditions.', 'Spores are covered by thick walls.', 'a', 'R explains A.'),
    ('Rhizopus reproduces by budding.', 'Rhizopus forms sporangia on its hyphae.', 'd', 'A is false (it reproduces by spores); R is true.'),
    ('Sugarcane is grown from stem cuttings.', 'Sugarcane stems have nodes with buds.', 'a', 'R explains A.'),
]

c10s3_defs = [
    ('pollination', 'the transfer of pollen grains from the anther to the stigma of a flower'),
    ('self-pollination', 'the transfer of pollen from the anther to the stigma of the same flower or another flower of the same plant'),
    ('cross-pollination', 'the transfer of pollen from the anther of one flower to the stigma of a flower on another plant of the same kind'),
    ('fertilisation', 'the fusion of the male and female gametes to form a zygote'),
    ('a zygote', 'the cell formed by the fusion of a male gamete and a female gamete'),
    ('germination', 'the process by which the embryo in a seed grows into a seedling under suitable conditions'),
    ('a unisexual flower', 'a flower that has either stamens or pistil, but not both'),
    ('a bisexual flower', 'a flower that has both stamens and pistil'),
    ('the stamen', 'the male reproductive part of a flower, made of anther and filament'),
    ('the pistil (carpel)', 'the female reproductive part of a flower, made of stigma, style and ovary'),
]
c10s3_parts = {
    'a part of the stamen': ['anther', 'filament'],
    'a part of the pistil': ['stigma', 'style', 'ovary', 'ovule'],
    'a non-reproductive part of a flower': ['sepal', 'petal', 'thalamus', 'pedicel'],
}
c10s3_sex = {
    'a unisexual flower': ['papaya flower', 'watermelon flower', 'cucumber flower', 'maize tassel'],
    'a bisexual flower': ['hibiscus', 'mustard flower', 'rose', 'petunia', 'pea flower'],
}
c10s3_after = {
    'the seed': ['ovule'], 'the fruit': ['ovary'], 'the embryo': ['zygote'],
}
c10s3_mc = [
    ('After fertilisation, the ovary develops into the:', 'fruit', 'seed', 'embryo', 'petal'),
    ('After fertilisation, the ovule develops into the:', 'seed', 'fruit', 'pollen', 'stigma'),
    ('The male gametes in a flower are found inside the:', 'pollen grains', 'ovules', 'sepals', 'stigma'),
    ('The pollen tube grows through the:', 'style to reach the ovule', 'filament to reach the anther', 'sepal to reach the petal', 'stem to reach the root'),
    ('Which agent pollinates the brightly coloured, scented flowers of mango?', 'insects', 'water', 'gravity', 'light'),
    ('Which part of the pistil receives pollen?', 'stigma', 'style', 'ovary', 'ovule'),
    ('The female gamete (egg) of a flower is present in the:', 'ovule', 'anther', 'filament', 'petal'),
    ('Wind-pollinated flowers such as maize usually have:', 'light, dry pollen in large amounts', 'bright petals and nectar', 'sticky heavy pollen', 'strong scent'),
]
c10s3_why = [
    ('Why do insect-pollinated flowers have bright petals, scent and nectar?', 'These attract insects such as bees and butterflies, which carry pollen from one flower to another.', '1 mark: attract insects. 1 mark: carry pollen.'),
    ('Why do wind-pollinated plants produce a very large amount of pollen?', 'Wind carries pollen randomly and most is wasted, so large amounts increase the chance of reaching a stigma.', '1 mark: random. 1 mark: chance.'),
    ('Why is cross-pollination useful to plants?', 'It brings pollen with different genes, producing variation in the offspring, which helps them adapt.', '1 mark: different genes. 1 mark: variation.'),
    ('Why does the pollen tube have to grow to reach the ovule?', 'The ovule with the egg is deep inside the ovary, so the male gamete is carried down the style by the tube to reach the egg.', '1 mark: ovule deep in ovary. 1 mark: tube carries gamete.'),
    ('Why do the petals and sepals of most flowers wither after fertilisation?', 'Their job of attracting pollinators and protecting the bud is over; the plant\'s food goes to the developing fruit and seeds.', '1 mark: job over. 1 mark: resources to fruit.'),
]
c10s3_ar = [
    ('Papaya cannot self-pollinate.', 'Papaya plants bear unisexual flowers, with male and female flowers on different plants.', 'a', 'R explains A.'),
    ('The ovary develops into a fruit after fertilisation.', 'The ovule develops into a seed after fertilisation.', 'b', 'Both are true; R does not explain A.'),
    ('Flowers pollinated by wind are usually small and dull.', 'They do not need to attract insects.', 'a', 'R explains A.'),
    ('Fertilisation in flowering plants takes place in the stigma.', 'The pollen grain lands on the stigma.', 'd', 'A is false – fertilisation takes place inside the ovule; R is true.'),
]
c10s3_seq = ['pollen lands on the stigma', 'a pollen tube grows down the style', 'the male gamete reaches the ovule', 'the male gamete fuses with the egg to form a zygote', 'the zygote develops into an embryo', 'the ovule becomes a seed and the ovary a fruit']


def c10s3_order(r):
    k = r.randint(4, 6)
    st = r.randint(0, len(c10s3_seq) - k)
    seq = c10s3_seq[st:st + k]
    sh = seq[:]
    while sh == seq:
        r.shuffle(sh)
    L = '; '.join(f'({i + 1}) {x}' for i, x in enumerate(sh))
    order = ', '.join(str(sh.index(x) + 1) for x in seq)
    return {'stem': f'Arrange these steps of sexual reproduction in a flowering plant in the correct order: {L}.', 'answer': f'{order}', 'key': 'Correct sequence: ' + ' → '.join(seq) + '.'}


c10s4_defs = [
    ('a gamete', 'a reproductive cell (sperm or egg) containing half the number of chromosomes of a body cell'),
    ('internal fertilisation', 'fertilisation that takes place inside the female\'s body, as in humans, cows and hens'),
    ('external fertilisation', 'fertilisation that takes place outside the female\'s body, usually in water, as in frogs and fish'),
    ('a viviparous animal', 'an animal that gives birth to young ones'),
    ('an oviparous animal', 'an animal that lays eggs'),
    ('metamorphosis', 'the transformation of a larva into an adult through drastic changes'),
    ('puberty', 'the period when the reproductive organs mature and the body becomes capable of reproduction'),
    ('adolescence', 'the period of life (about 11–19 years) between childhood and adulthood when the body undergoes many changes'),
    ('a hormone', 'a chemical messenger secreted by an endocrine gland directly into the blood'),
]
c10s4_cats = {
    'oviparous': ['hen', 'frog', 'lizard', 'butterfly', 'crocodile', 'sparrow'],
    'viviparous': ['human', 'cow', 'dog', 'cat', 'elephant', 'goat'],
}
c10s4_fert = {
    'internal fertilisation': ['human', 'cow', 'hen', 'dog', 'lizard'],
    'external fertilisation': ['frog', 'fish (rohu)', 'starfish', 'toad'],
}
c10s4_mc = [
    ('The male gametes in humans are produced in the:', 'testes', 'ovaries', 'uterus', 'oviduct'),
    ('In humans, fertilisation normally takes place in the:', 'oviduct (fallopian tube)', 'uterus', 'vagina', 'ovary'),
    ('The embryo gets nutrition from the mother\'s blood through the:', 'placenta', 'oviduct', 'ovary', 'testes'),
    ('The hormone testosterone is produced by the:', 'testes', 'ovaries', 'thyroid', 'pancreas'),
    ('Which hormone controls the changes in girls at puberty?', 'oestrogen', 'testosterone', 'insulin', 'thyroxine'),
    ('A frog lays a large number of eggs because:', 'fertilisation is external and many eggs are lost', 'it has a large body', 'eggs need no water', 'the eggs are fertilised inside'),
    ('The stages of metamorphosis in a frog are:', 'egg → tadpole → adult', 'egg → larva → pupa → adult', 'egg → adult', 'tadpole → egg → adult'),
    ('Iodised salt is recommended to prevent goitre, a disease of the:', 'thyroid gland', 'pancreas', 'adrenal gland', 'pituitary gland'),
]
c10s4_why = [
    ('Why do fish and frogs lay hundreds of eggs, while hens lay only a few?', 'Fish and frogs have external fertilisation in water, and many eggs and young are lost to currents and predators; a hen\'s eggs are fertilised inside and protected.', '1 mark: external fertilisation, losses. 1 mark: hen protected.'),
    ('Why is a balanced diet especially important during adolescence?', 'It is a period of rapid growth and development, so the body needs more proteins, iron, calcium and vitamins.', '1 mark: rapid growth. 1 mark: nutrients.'),
    ('Why is personal hygiene important for adolescents?', 'Sweat and oil glands become more active, so bathing and clean clothes are needed to prevent infections and body odour.', '1 mark: glands active. 1 mark: prevent infection.'),
    ('Why should adolescents say no to drugs?', 'Drugs are addictive and harm the body and mind; once taken, it is very hard to give them up.', '1 mark: addictive. 1 mark: harmful.'),
]
c10s4_ar = [
    ('Frogs lay a large number of eggs.', 'Frogs show external fertilisation.', 'a', 'Many eggs are lost in water, so many are laid; R explains A.'),
    ('The placenta is important for the developing embryo.', 'Oxygen and nutrients pass from the mother\'s blood to the embryo through it.', 'a', 'R explains A.'),
    ('Hens are viviparous animals.', 'Hens lay eggs.', 'd', 'A is false (hens are oviparous); R is true.'),
    ('Voice breaks in boys at puberty.', 'The larynx (voice box) grows larger at puberty.', 'a', 'R explains A.'),
]


def c10s4_tadpole(r):
    n = r.choice([500, 800, 1000, 1500, 2000, 3000])
    p = r.choice([5, 8, 10, 12, 20])
    s = n * p // 100
    nm = name(r)
    return {'stem': f'{nm} studies a frog spawn of {n} eggs in a village pond near Nashik. If only {p}% of the eggs survive to become adult frogs, how many frogs develop? Why does the frog need to lay so many eggs?',
            'answer': f'{s} frogs; fertilisation and development are external, so most eggs and tadpoles are lost.',
            'key': f'{p}% of {n} = {s}. External fertilisation and no parental protection mean heavy losses.'}


c10_hots = [
    ('A gardener in Pune wants many mango trees giving fruit of exactly the same quality as her best tree, and quickly. Should she sow seeds or use grafting? Give two reasons.', 'Grafting: the scion from the best tree keeps exactly its fruit quality, while seeds give variation; grafted trees fruit earlier.', '1 mark choice. 1 mark each reason.'),
    ('If all members of a crop are produced by vegetative propagation from one plant, what risk does the farmer face? Explain.', 'They are genetically identical, so a disease or pest that attacks one can wipe out the whole crop; there is no variation to resist it.', '1 mark identical. 1 mark disease risk. 1 mark no variation.'),
    ('A papaya grower finds that one of her plants never bears fruit although it flowers every year. Suggest a reason and a remedy.', 'Papaya bears unisexual flowers on separate plants; the plant is probably a male plant. She should grow female plants with a few male plants nearby for pollination.', '1 mark male plant. 1 mark unisexual. 1 mark remedy.'),
    ('Explain why a seed from a cross-pollinated plant may produce a plant slightly different from both parents.', 'Cross-pollination brings together gametes from two plants with different DNA; fertilisation combines them, producing new combinations (variation).', '1 mark two parents. 1 mark fusion. 1 mark variation.'),
]
c10_case = [
    ('Read: Ravi cut a Planaria into three pieces in the lab; each grew into a complete worm in two weeks. He also saw small outgrowths on a Hydra which detached and became new Hydras, and a slice of bread kept in a humid box developed black dots on white threads.\n'
     '(i) Name the process seen in Planaria. (ii) Name the process seen in Hydra. (iii) Name the organism on the bread and its mode of reproduction. (iv) Are the offspring in these cases similar to or different from the parent? Why?',
     '(i) Regeneration. (ii) Budding. (iii) Rhizopus (bread mould); spore formation from sporangia. (iv) Similar, because only one parent is involved and there is no fusion of gametes.', '1 mark each part.'),
    ('Read: A flower of a mustard plant has four sepals, four yellow petals, six stamens and a pistil. Bees visit it, and later the petals fall and a long pod develops containing many seeds.\n'
     '(i) Is the flower unisexual or bisexual? (ii) What is the role of the bees? (iii) Which part of the flower develops into the pod? (iv) What did the ovules develop into?',
     '(i) Bisexual. (ii) They carry pollen to the stigma (pollination). (iii) The ovary. (iv) Seeds.', '1 mark each part.'),
]
c10_long = [
    ('Draw a labelled diagram of a flower. Describe pollination, fertilisation and the changes in the flower after fertilisation.',
     'Parts: sepals, petals, stamens (anther, filament), pistil (stigma, style, ovary with ovules). Pollination: transfer of pollen to the stigma, by self or cross means by wind, water or insects. Fertilisation: the pollen tube grows through the style to the ovule; the male gamete fuses with the egg to form a zygote. Afterwards the zygote becomes the embryo, the ovule a seed, the ovary a fruit; petals, sepals, stamens and style wither.',
     '1 mark diagram; 1 mark pollination; 2 marks fertilisation; 1 mark changes.'),
    ('Describe four methods of asexual reproduction with one example each. Why is asexual reproduction considered less useful for long-term survival of a species?',
     'Binary fission (Amoeba), multiple fission (Plasmodium), budding (yeast, Hydra), fragmentation (Spirogyra), regeneration (Planaria), spore formation (Rhizopus), vegetative propagation (potato). Asexual offspring are nearly identical to the parent, so there is little variation to survive changes in the environment.',
     '1 mark each method (4); 1 mark reason.'),
    ('What are the changes seen in boys and girls at puberty? Name the hormones responsible and explain the importance of a balanced diet, hygiene and physical exercise during adolescence.',
     'Increase in height, growth of hair, voice changes (larynx grows in boys), active sweat and oil glands, development of sex organs; breasts in girls, facial hair in boys. Hormones: testosterone (boys), oestrogen (girls), controlled by the pituitary. Diet for rapid growth; hygiene to prevent infections; exercise for health and fitness.',
     '2 marks changes; 1 mark hormones; 2 marks diet/hygiene/exercise.'),
    ('Compare sexual reproduction in humans and in frogs in terms of fertilisation, development and care of the young.',
     'Humans: internal fertilisation in the oviduct; the embryo grows in the uterus fed through the placenta; viviparous; long parental care. Frogs: external fertilisation in water; many eggs laid; egg → tadpole → adult by metamorphosis; oviparous; little parental care.',
     '2 marks humans; 2 marks frogs; 1 mark comparison.'),
]

# ======================= ch11 Diversity and Classification
c11s1_defs = [
    ('classification', 'the grouping of organisms into categories based on their similarities and differences'),
    ('a species', 'a group of similar organisms that can interbreed to produce fertile offspring'),
    ('taxonomy', 'the science of identifying, naming and classifying organisms'),
    ('a genus', 'a group of closely related species'),
    ('biodiversity', 'the variety of living organisms found in a region'),
    ('a phylum', 'the category that groups related classes of animals; in plants the equivalent is a division'),
]
HIER = ['kingdom', 'phylum (division)', 'class', 'order', 'family', 'genus', 'species']
c11s1_mc = [
    ('The basic unit of classification is:', 'species', 'genus', 'family', 'kingdom'),
    ('Which is the most fundamental characteristic used to separate living organisms into broad groups?', 'whether cells are prokaryotic or eukaryotic', 'their colour', 'their size', 'where they live'),
    ('Which of these groups has the largest number of organisms?', 'kingdom', 'class', 'genus', 'species'),
    ('Members of which category show the greatest similarity?', 'species', 'genus', 'order', 'phylum'),
    ('Two organisms are in the same family. They must also be in the same:', 'order', 'genus', 'species', 'none of these'),
    ('Who proposed the five-kingdom classification?', 'Robert Whittaker', 'Carolus Linnaeus', 'Charles Darwin', 'Ernst Haeckel'),
]
c11s1_why = [
    ('Why do we need to classify organisms?', 'It makes the study of the huge variety of organisms easy, shows how they are related, and helps in identifying new organisms.', '1 mark: easy study. 1 mark: relationships.'),
    ('Why is the number of organisms in a category larger at higher levels of the hierarchy?', 'Higher categories group organisms by fewer, broader characteristics, so they include many lower groups; lower categories need more shared features.', '1 mark: broader features. 1 mark: include lower groups.'),
    ('Why is the type of cell (prokaryotic or eukaryotic) a fundamental basis of classification?', 'It decides the whole design of the organism: presence of a nucleus and membrane-bound organelles affects every other process.', '1 mark: basic design. 1 mark: affects other features.'),
    ('Why is the presence of a backbone a more important basis for classifying animals than the colour of the skin?', 'A backbone affects the whole body design and is shared by large groups; skin colour varies even within a species.', '1 mark: body design. 1 mark: colour varies.'),
]
c11s1_ar = [
    ('Species is the lowest category in the hierarchy of classification.', 'Members of a species can interbreed to produce fertile offspring.', 'b', 'Both are true; R defines a species but does not explain why it is the lowest category.'),
    ('Kingdom has the largest number of organisms among the categories.', 'Organisms in a kingdom share only a few broad features.', 'a', 'R explains A.'),
    ('Bats and birds are placed in the same class because both can fly.', 'Classification is based on body design and not on one similar habit.', 'd', 'A is false (bats are mammals, birds are aves); R is true.'),
]


def c11s1_hier(r):
    i = r.randint(0, len(HIER) - 2)
    q = r.choice(['next lower', 'next higher'])
    if q == 'next lower' or i == 0:
        q = 'next lower'
        a = HIER[i + 1]
        x = HIER[i]
    else:
        a = HIER[i - 1]
        x = HIER[i]
    wrong = [h for h in HIER if h not in (a, x)]
    return {'stem': f'In the hierarchy of classification, which category comes {q} to {x}?', 'answer': a,
            'key': 'Kingdom → phylum (division) → class → order → family → genus → species.', 'distractors': random_sample(r, wrong, 3)}


def random_sample(r, xs, k):
    return r.sample(xs, k)


def c11s1_sortH(r):
    k = r.randint(4, 6)
    st = r.randint(0, len(HIER) - k)
    seq = HIER[st:st + k]
    sh = seq[:]
    while sh == seq:
        r.shuffle(sh)
    return {'stem': f'Arrange these categories from the highest (broadest) to the lowest: {", ".join(sh)}.', 'answer': ' → '.join(seq),
            'key': '½ mark per category placed correctly. Order: ' + ' → '.join(HIER) + '.'}


# (common name, kingdom, phylum/division, class or note)
ORG = [
    ('mango', 'Plantae', 'Angiosperms', 'dicot'), ('wheat', 'Plantae', 'Angiosperms', 'monocot'),
    ('pine', 'Plantae', 'Gymnosperms', ''), ('fern', 'Plantae', 'Pteridophyta', ''), ('moss (Funaria)', 'Plantae', 'Bryophyta', ''),
    ('Spirogyra', 'Plantae', 'Thallophyta', ''), ('mushroom', 'Fungi', '', ''), ('yeast', 'Fungi', '', ''),
    ('bacteria', 'Monera', '', ''), ('Anabaena', 'Monera', '', ''), ('Amoeba', 'Protista', '', ''), ('Paramecium', 'Protista', '', ''),
    ('earthworm', 'Animalia', 'Annelida', ''), ('cockroach', 'Animalia', 'Arthropoda', ''), ('snail', 'Animalia', 'Mollusca', ''),
    ('starfish', 'Animalia', 'Echinodermata', ''), ('Hydra', 'Animalia', 'Cnidaria (Coelenterata)', ''), ('tapeworm', 'Animalia', 'Platyhelminthes', ''),
    ('roundworm (Ascaris)', 'Animalia', 'Nematoda', ''), ('sponge', 'Animalia', 'Porifera', ''),
    ('frog', 'Animalia', 'Chordata', 'Amphibia'), ('rohu', 'Animalia', 'Chordata', 'Pisces'), ('lizard', 'Animalia', 'Chordata', 'Reptilia'),
    ('peacock', 'Animalia', 'Chordata', 'Aves'), ('tiger', 'Animalia', 'Chordata', 'Mammalia'),
]
c11s2_k = {
    'Monera': ['bacteria', 'Anabaena', 'blue-green algae', 'Rhizobium'],
    'Protista': ['Amoeba', 'Paramecium', 'Euglena', 'diatoms'],
    'Fungi': ['mushroom', 'yeast', 'Penicillium', 'Rhizopus (bread mould)', 'Aspergillus'],
    'Plantae': ['mango', 'fern', 'moss', 'pine', 'Spirogyra'],
    'Animalia': ['earthworm', 'frog', 'starfish', 'cockroach', 'human'],
}
c11s2_kd = {f'kingdom {k}': v for k, v in c11s2_k.items()}
c11s2_defs = [
    ('Monera', 'the kingdom of prokaryotic organisms without a defined nucleus, such as bacteria and blue-green algae'),
    ('Protista', 'the kingdom of unicellular eukaryotic organisms, such as Amoeba, Paramecium and diatoms'),
    ('Fungi', 'the kingdom of heterotrophic eukaryotes with cell walls of chitin that feed saprophytically on decaying matter'),
    ('Plantae', 'the kingdom of multicellular eukaryotes with cell walls that make their own food by photosynthesis'),
    ('Animalia', 'the kingdom of multicellular eukaryotes without cell walls that are heterotrophic'),
    ('a saprophyte', 'an organism that obtains nutrition from dead and decaying organic matter'),
    ('a lichen', 'a symbiotic association between a fungus and blue-green algae (or green algae)'),
]
c11s2_feat = {
    'Monera': ['prokaryotic cells with no defined nucleus', 'may be autotrophic or heterotrophic, unicellular'],
    'Protista': ['unicellular eukaryotes', 'use cilia, flagella or pseudopodia for movement'],
    'Fungi': ['cell wall of chitin', 'saprophytic heterotrophs'],
    'Plantae': ['multicellular eukaryotes with cell walls, mostly autotrophic', 'contain chlorophyll'],
    'Animalia': ['multicellular eukaryotes without cell walls, heterotrophic', 'most can move from place to place'],
}
c11s2_mc = [
    ('Blue-green algae (cyanobacteria) belong to the kingdom:', 'Monera', 'Protista', 'Plantae', 'Fungi'),
    ('The cell wall of fungi is made of:', 'chitin', 'cellulose', 'protein', 'lipid'),
    ('A lichen is an association of:', 'fungus and alga', 'fungus and bacterium', 'alga and moss', 'two fungi'),
    ('Which kingdom has organisms that are multicellular, eukaryotic and without cell walls?', 'Animalia', 'Plantae', 'Fungi', 'Monera'),
    ('Which feature separates Monera from all other kingdoms?', 'absence of a defined nucleus', 'presence of cell wall', 'mode of nutrition', 'size'),
    ('Mushrooms are not placed in Plantae because they:', 'lack chlorophyll and are saprophytes with chitin cell walls', 'are unicellular', 'are prokaryotes', 'can move'),
]
c11s2_why = [
    ('Why is Euglena difficult to classify as a plant or an animal?', 'It has chlorophyll and makes food like a plant, but moves by a flagellum and can take in food like an animal; it is placed in Protista.', '1 mark plant feature. 1 mark animal feature.'),
    ('Why are fungi called saprophytes?', 'They absorb nutrients from dead and decaying organic matter.', '2 marks.'),
    ('Give two differences between Monera and Protista.', 'Monera are prokaryotic with no defined nucleus; Protista are eukaryotic with a nucleus. Monera lack membrane-bound organelles; Protista have them.', '1 mark each.'),
    ('On what three bases did Whittaker divide organisms into five kingdoms?', 'Cell structure (prokaryotic/eukaryotic), body organisation (unicellular/multicellular), and mode of nutrition (autotrophic/heterotrophic).', '1 mark each (any two for 2 marks).'),
]
c11s2_ar = [
    ('Bacteria are placed in Monera.', 'Bacteria are prokaryotes without a well-defined nucleus.', 'a', 'R explains A.'),
    ('Fungi are placed in a separate kingdom from plants.', 'Fungi lack chlorophyll and have cell walls of chitin.', 'a', 'R explains A.'),
    ('Amoeba belongs to kingdom Animalia.', 'Amoeba is a unicellular eukaryote.', 'd', 'A is false (Amoeba is in Protista); R is true.'),
    ('Lichens grow on bare rocks.', 'A fungus and an alga live together in a lichen, the alga making food.', 'a', 'R explains A.'),
]


def c11s2_ident(r):
    k = r.choice(list(c11s2_feat))
    f1, f2 = c11s2_feat[k]
    others = [x for x in c11s2_feat if x != k]
    return {'stem': f'An organism shows these features: {f1}; {f2}. To which kingdom does it belong?', 'answer': k,
            'key': f'{f1.capitalize()} and {f2} are features of {k}.', 'distractors': r.sample(others, 3)}


c11s3_div = {
    'Thallophyta': ['Spirogyra', 'Ulothrix', 'Cladophora', 'Chara', 'Ulva'],
    'Bryophyta': ['Riccia', 'Marchantia', 'Funaria (moss)'],
    'Pteridophyta': ['Marsilea', 'ferns', 'horsetails (Equisetum)', 'Selaginella'],
    'Gymnosperms': ['pine', 'deodar', 'Cycas', 'Ginkgo'],
    'Angiosperms': ['mango', 'wheat', 'rice', 'pea', 'neem', 'banana'],
}
c11s3_dv = {f'a member of {k}': v for k, v in c11s3_div.items()}
c11s3_cot = {
    'a monocot': ['wheat', 'rice', 'maize', 'banana', 'coconut', 'sugarcane', 'onion'],
    'a dicot': ['pea', 'mango', 'neem', 'mustard', 'gram', 'sunflower', 'tomato'],
}
c11s3_feat = {
    'Thallophyta': 'a plant body not differentiated into root, stem and leaves; mostly aquatic (algae)',
    'Bryophyta': 'a plant body with stem and leaf-like structures but no vascular tissue; called the amphibians of the plant kingdom',
    'Pteridophyta': 'a body with roots, stems and leaves and vascular tissue, but no seeds',
    'Gymnosperms': 'naked seeds not enclosed in a fruit; usually perennial, evergreen and woody',
    'Angiosperms': 'seeds enclosed in fruits; flowers present',
}
c11s3_defs = [
    ('cryptogams', 'plants with hidden reproductive organs that do not produce seeds: thallophyta, bryophyta and pteridophyta'),
    ('phanerogams', 'plants with well-developed reproductive tissues that produce seeds: gymnosperms and angiosperms'),
    ('a gymnosperm', 'a seed plant whose seeds are naked, not enclosed in a fruit'),
    ('an angiosperm', 'a flowering plant whose seeds are enclosed inside a fruit'),
    ('a cotyledon', 'a seed leaf of the embryo, which often stores food'),
    ('a vascular tissue', 'specialised tissue (xylem and phloem) that conducts water and food in a plant'),
]
c11s3_mc = [
    ('Which group is called the "amphibians of the plant kingdom"?', 'Bryophyta', 'Thallophyta', 'Pteridophyta', 'Gymnosperms'),
    ('The first plants to have vascular tissue were:', 'Pteridophyta', 'Bryophyta', 'Thallophyta', 'Angiosperms'),
    ('Seeds of gymnosperms are:', 'naked', 'inside a fruit', 'absent', 'inside a pod'),
    ('A monocot seed has:', 'one cotyledon', 'two cotyledons', 'no cotyledon', 'three cotyledons'),
    ('Monocots usually have leaves with:', 'parallel venation', 'reticulate venation', 'no veins', 'needle-like veins'),
    ('A dicot plant usually has:', 'a tap root system', 'a fibrous root system', 'no root', 'only aerial roots'),
    ('Ferns reproduce by:', 'spores', 'seeds', 'fruits', 'budding'),
]
c11s3_why = [
    ('Why are bryophytes called the amphibians of the plant kingdom?', 'They live on land but need water for fertilisation and reproduction.', '1 mark: land. 1 mark: water for reproduction.'),
    ('Why are pteridophytes, bryophytes and thallophytes called cryptogams?', 'Their reproductive organs are hidden ("crypto"), and they do not produce seeds.', '1 mark: hidden organs. 1 mark: no seeds.'),
    ('How will you tell a monocot from a dicot plant growing in a field?', 'Monocot: parallel venation, fibrous roots, flower parts in threes; dicot: reticulate venation, tap root, parts in fours or fives.', '1 mark each.'),
    ('Why are angiosperms called flowering plants?', 'They produce flowers, which form fruits enclosing the seeds.', '2 marks.'),
]
c11s3_ar = [
    ('Pine is a gymnosperm.', 'Pine has naked seeds not enclosed in fruits.', 'a', 'R explains A.'),
    ('Ferns are vascular plants.', 'Ferns produce seeds.', 'c', 'A is true; R is false – ferns reproduce by spores.'),
    ('Spirogyra is a thallophyte.', 'Its body is not differentiated into root, stem and leaves.', 'a', 'R explains A.'),
    ('Wheat is a dicot.', 'Wheat has fibrous roots and parallel venation.', 'd', 'A is false (wheat is a monocot); R is true.'),
]


def c11s3_ident(r):
    k = r.choice(list(c11s3_feat))
    others = [x for x in c11s3_feat if x != k]
    return {'stem': f'A plant group shows this feature: {c11s3_feat[k]}. Name the group.', 'answer': k, 'key': f'This describes {k}.', 'distractors': r.sample(others, 3)}


c11s4_ph = {
    'Porifera': ['Sycon', 'Spongilla', 'Euplectella'],
    'Cnidaria (Coelenterata)': ['Hydra', 'sea anemone', 'jellyfish', 'corals'],
    'Platyhelminthes': ['Planaria', 'liver fluke', 'tapeworm'],
    'Nematoda': ['Ascaris (roundworm)', 'Wuchereria (filarial worm)', 'pinworm'],
    'Annelida': ['earthworm', 'leech', 'Nereis'],
    'Arthropoda': ['cockroach', 'butterfly', 'prawn', 'spider', 'scorpion', 'housefly', 'crab'],
    'Mollusca': ['snail', 'octopus', 'Pila', 'mussel'],
    'Echinodermata': ['starfish', 'sea urchin', 'sea cucumber'],
}
c11s4_pd = {f'a member of {k}': v for k, v in c11s4_ph.items()}
c11s4_cl = {
    'Pisces': ['rohu', 'catla', 'shark', 'seahorse'],
    'Amphibia': ['frog', 'toad', 'salamander'],
    'Reptilia': ['lizard', 'snake', 'crocodile', 'turtle'],
    'Aves': ['peacock', 'sparrow', 'pigeon', 'ostrich', 'crow'],
    'Mammalia': ['tiger', 'cow', 'bat', 'whale', 'human', 'monkey'],
}
c11s4_cd = {f'a member of class {k}': v for k, v in c11s4_cl.items()}
c11s4_ch = {
    'a vertebrate': ['frog', 'lizard', 'sparrow', 'rohu', 'cow'],
    'a non-chordate': ['earthworm', 'cockroach', 'snail', 'starfish', 'Hydra', 'tapeworm'],
}
c11s4_feat = {
    'Porifera': 'a non-motile animal with pores all over the body and a canal system',
    'Cnidaria (Coelenterata)': 'aquatic animals with a body cavity, two layers of cells and tentacles with stinging cells',
    'Platyhelminthes': 'bilaterally symmetrical, flattened animals with three cell layers and no true body cavity',
    'Nematoda': 'cylindrical worms with a pseudocoelom, often parasites causing elephantiasis or intestinal infection',
    'Annelida': 'segmented worms with a true body cavity (coelom)',
    'Arthropoda': 'animals with jointed legs and an open circulatory system',
    'Mollusca': 'soft-bodied animals often with a shell and a muscular foot',
    'Echinodermata': 'spiny-skinned marine animals with a water-driven tube system for movement',
}
c11s4_cfeat = {
    'Pisces': 'cold-blooded, aquatic, breathe through gills, scales on the body, two-chambered heart',
    'Amphibia': 'cold-blooded, no scales, moist skin with mucus glands, three-chambered heart, live in water and on land',
    'Reptilia': 'cold-blooded, scaly skin, breathe through lungs, lay eggs with tough coverings on land',
    'Aves': 'warm-blooded, feathers, forelimbs modified into wings, four-chambered heart, lay eggs',
    'Mammalia': 'warm-blooded, hair on the skin, mammary glands to feed young, four-chambered heart',
}
c11s4_defs = [
    ('a chordate', 'an animal that has a notochord at some stage of its life'),
    ('the notochord', 'a long rod-like support structure running along the back of an animal, separating nerve tissue from the gut'),
    ('a vertebrate', 'a chordate with a true vertebral column (backbone) and internal skeleton'),
    ('a coelom', 'a true body cavity lined by mesoderm, in which well-developed organs can be accommodated'),
    ('bilateral symmetry', 'a body that can be divided into two identical left and right halves by only one plane'),
    ('a warm-blooded animal', 'an animal whose body temperature stays constant whatever the surroundings, such as birds and mammals'),
    ('a cold-blooded animal', 'an animal whose body temperature changes with the surroundings, such as fish, amphibians and reptiles'),
]
c11s4_mc = [
    ('The largest group of animals is:', 'Arthropoda', 'Mollusca', 'Annelida', 'Chordata'),
    ('Which animals have a four-chambered heart?', 'birds and mammals', 'fishes and amphibians', 'amphibians only', 'reptiles only'),
    ('Which of these is a mammal that can fly?', 'bat', 'sparrow', 'flying fish', 'butterfly'),
    ('A whale is placed among mammals because it:', 'feeds its young on milk from mammary glands', 'lives in water', 'has fins', 'is very large'),
    ('Earthworms differ from roundworms in having:', 'a segmented body with a true coelom', 'a cylindrical body', 'no organs', 'jointed legs'),
    ('Which phylum has animals with jointed legs?', 'Arthropoda', 'Annelida', 'Mollusca', 'Nematoda'),
    ('Which animal has a water-driven tube system?', 'starfish', 'snail', 'earthworm', 'Hydra'),
]
c11s4_why = [
    ('Why is a bat placed in Mammalia and not in Aves?', 'It has hair, gives birth to young and feeds them with milk from mammary glands; it has no feathers.', '1 mark: hair/mammary glands. 1 mark: no feathers.'),
    ('Why are frogs called amphibians?', 'They live both in water and on land; their larvae (tadpoles) live in water and they need water to lay eggs.', '1 mark: water and land. 1 mark: eggs in water.'),
    ('Why are birds and mammals called warm-blooded?', 'They maintain a constant body temperature regardless of the surrounding temperature.', '2 marks.'),
    ('Give two differences between a chordate and a non-chordate.', 'Chordates have a notochord and a dorsal nerve cord; non-chordates lack a notochord and have a ventral nerve cord (if any).', '1 mark each.'),
]
c11s4_ar = [
    ('A whale is a mammal.', 'It has mammary glands and gives birth to young ones.', 'a', 'R explains A.'),
    ('Cockroach is an arthropod.', 'It has jointed legs and an open circulatory system.', 'a', 'R explains A.'),
    ('Snakes are cold-blooded animals.', 'Their body temperature changes with the surroundings.', 'a', 'R explains A.'),
    ('Starfish is a fish.', 'Starfish lives in the sea.', 'd', 'A is false (starfish is an echinoderm); R is true.'),
]


def c11s4_ident(r):
    k = r.choice(list(c11s4_feat))
    others = [x for x in c11s4_feat if x != k]
    return {'stem': f'Name the phylum of animals with this feature: {c11s4_feat[k]}.', 'answer': k, 'key': f'This describes {k}.', 'distractors': r.sample(others, 3)}


def c11s4_cident(r):
    k = r.choice(list(c11s4_cfeat))
    others = [x for x in c11s4_cfeat if x != k]
    return {'stem': f'A vertebrate is described as: {c11s4_cfeat[k]}. To which class does it belong?', 'answer': k, 'key': f'These are features of {k}.', 'distractors': r.sample(others, 3)}


BIN = [
    ('human', 'Homo sapiens'), ('mango', 'Mangifera indica'), ('tiger', 'Panthera tigris'), ('lion', 'Panthera leo'),
    ('peacock', 'Pavo cristatus'), ('rice', 'Oryza sativa'), ('wheat', 'Triticum aestivum'), ('neem', 'Azadirachta indica'),
    ('house fly', 'Musca domestica'), ('frog', 'Rana tigrina'), ('cat', 'Felis catus'), ('dog', 'Canis familiaris'),
    ('cow', 'Bos indicus'), ('pea', 'Pisum sativum'), ('potato', 'Solanum tuberosum'), ('tulsi', 'Ocimum sanctum'),
]
c11s5_defs = [
    ('binomial nomenclature', 'the system of naming an organism with two words, the genus name followed by the species name'),
    ('the scientific name', 'the internationally accepted two-word name of an organism, the same in all languages'),
    ('the generic name', 'the first word of a scientific name, which names the genus and begins with a capital letter'),
    ('the specific name (epithet)', 'the second word of a scientific name, which names the species and begins with a small letter'),
]
c11s5_mc = [
    ('Binomial nomenclature was introduced by:', 'Carolus Linnaeus', 'Robert Whittaker', 'Gregor Mendel', 'Robert Hooke'),
    ('Which is the correct way to write the scientific name of the mango?', 'Mangifera indica', 'mangifera indica', 'Mangifera Indica', 'MANGIFERA INDICA'),
    ('In "Panthera leo", "Panthera" is the name of the:', 'genus', 'species', 'family', 'order'),
    ('When handwritten, a scientific name should be:', 'underlined, each word separately', 'written in capitals', 'put in quotes', 'written with both words capitalised'),
    ('Scientific names are useful because they are:', 'the same all over the world', 'easy to pronounce', 'in Hindi', 'different in each country'),
]
c11s5_why = [
    ('Why do scientists use scientific names instead of common names like "aam" or "mango"?', 'Common names differ from place to place and language to language; a scientific name is unique and the same worldwide.', '1 mark: common names vary. 1 mark: unique.'),
    ('State any two rules for writing scientific names.', 'The genus name begins with a capital letter and the species name with a small letter; the name is printed in italics or underlined separately when handwritten.', '1 mark each.'),
]
c11s5_ar = [
    ('The tiger and the lion belong to the same genus.', 'Their scientific names Panthera tigris and Panthera leo share the first word.', 'a', 'R explains A.'),
    ('The species name in a scientific name starts with a capital letter.', 'The genus name starts with a capital letter.', 'd', 'A is false; R is true.'),
    ('Scientific names avoid confusion among scientists of different countries.', 'Each organism has only one scientific name accepted worldwide.', 'a', 'R explains A.'),
]


def c11s5_name(r):
    c, s = r.choice(BIN)
    others = r.sample([b for a, b in BIN if b != s], 3)
    return {'stem': f'What is the scientific name of the {c}?', 'answer': s, 'key': f'{cap1(c)}: {s} (genus {s.split()[0]}).', 'distractors': others}


def cap1(s):
    return s[:1].upper() + s[1:]


def c11s5_correct(r):
    c, s = r.choice(BIN)
    g, sp = s.split()
    bad = r.choice([f'{g.lower()} {sp}', f'{g} {sp.capitalize()}', f'{sp} {g.lower()}', f'{g.upper()} {sp.upper()}'])
    return {'stem': f'A student writes the scientific name of the {c} as "{bad}". Write it correctly and state the rules broken.',
            'answer': f'{s}: the genus starts with a capital letter, the species with a small letter, genus first; printed in italics (underlined when handwritten).',
            'key': f'Correct form: {s}. 1 mark correct name. 1 mark rules.'}


def c11s5_genus(r):
    c, s = r.choice(BIN)
    part = r.choice(['genus', 'species'])
    a = s.split()[0] if part == 'genus' else s.split()[1]
    other = s.split()[1] if part == 'genus' else s.split()[0]
    return {'stem': f'In the scientific name of the {c}, {s}, which word is the {part} name?', 'answer': a, 'key': f'{s}: genus {s.split()[0]}, species {s.split()[1]}.',
            'distractors': [other, 'Both words together', 'Neither; both are species names']}


c11_hots = [
    ('A student finds an organism in a pond near Bhopal that is green, has a flagellum and moves about, and is unicellular with a nucleus. Classify it to kingdom level, giving two reasons, and say why it is hard to call it a plant or an animal.', 'Euglena, kingdom Protista: unicellular and eukaryotic. It makes food with chlorophyll like plants but moves like animals.', '1 mark kingdom. 1 mark reasons. 1 mark difficulty.'),
    ('Arrange these from the simplest to the most complex in body design and justify: earthworm, Hydra, sponge, Planaria.', 'Sponge (cellular level, pores) → Hydra (two layers, tissue level) → Planaria (three layers, no coelom) → earthworm (true coelom, segmented).', '1 mark order. 2 marks justification.'),
    ('A plant has a woody stem, needle-like leaves and seeds in cones, not in fruits. Another has flowers, fibrous roots and parallel-veined leaves. Classify both to the lowest group you can, giving reasons.', 'First: Gymnosperm (naked seeds in cones). Second: Angiosperm, monocot (flowers, fibrous roots, parallel venation).', '1 mark each identification. 1 mark reasons.'),
    ('A dolphin, a shark and a penguin live in the sea. Classify each into its vertebrate class and give one feature that supports each.', 'Dolphin: Mammalia (mammary glands, lungs, hair at birth). Shark: Pisces (gills, fins, cold-blooded). Penguin: Aves (feathers, lays eggs, warm-blooded).', '1 mark each.'),
]
c11_case = [
    ('Read: On a school trip to the Western Ghats, students found: (A) green threads in a stream, (B) a small green carpet on a damp wall, (C) a plant with feathery leaves having brown dots below, (D) a tall cone-bearing tree, (E) a flowering herb with parallel-veined leaves.\n'
     '(i) Classify A and B. (ii) What are the brown dots in C, and to which group does C belong? (iii) How does D differ from E in its seeds? (iv) Is E a monocot or dicot? Give a reason.',
     '(i) A – Thallophyta (alga, e.g. Spirogyra); B – Bryophyta (moss). (ii) Sori with spores; Pteridophyta (fern). (iii) D (gymnosperm) has naked seeds; E (angiosperm) has seeds inside fruits. (iv) Monocot, because of parallel venation.', '1 mark each part.'),
    ('Read: A zoo in Mysuru has a crocodile, a peacock, a bat and a frog in adjoining enclosures.\n'
     '(i) Which of them are warm-blooded? (ii) Which has a three-chambered heart and moist skin? (iii) Why is the bat not a bird? (iv) To which class does the crocodile belong, and give one feature.',
     '(i) Peacock and bat. (ii) Frog. (iii) It has hair and feeds its young on milk (mammal), and has no feathers. (iv) Reptilia; scaly skin / lays eggs with tough shells / lungs.', '1 mark each part.'),
]
c11_long = [
    ('Describe Whittaker\'s five-kingdom classification. Give the basis of classification and two features and one example of each kingdom.',
     'Basis: cell type, body organisation, mode of nutrition. Monera: prokaryotes, unicellular (bacteria). Protista: unicellular eukaryotes (Amoeba). Fungi: heterotrophic saprophytes, chitin walls (mushroom). Plantae: multicellular autotrophs with cellulose walls (mango). Animalia: multicellular heterotrophs without cell walls (frog).',
     '1 mark basis; 4 marks kingdoms.'),
    ('Classify the plant kingdom into its five groups. Give the distinguishing features and one example of each, and explain cryptogams and phanerogams.',
     'Thallophyta: undifferentiated, algae (Spirogyra). Bryophyta: no vascular tissue, amphibians (moss). Pteridophyta: vascular, no seeds (fern). Gymnosperms: naked seeds (pine). Angiosperms: seeds in fruits (mango). Cryptogams: hidden reproductive organs, no seeds (first three); phanerogams: seed plants (last two).',
     '3 marks groups; 2 marks cryptogams/phanerogams.'),
    ('Give the features and examples of the five classes of vertebrates.',
     'Pisces: gills, scales, two-chambered heart, cold-blooded (rohu). Amphibia: moist skin, three-chambered heart, water and land (frog). Reptilia: scales, lungs, eggs with tough coverings (lizard). Aves: feathers, wings, four-chambered heart, warm-blooded (peacock). Mammalia: hair, mammary glands, four-chambered heart (tiger).',
     '1 mark each class.'),
    ('Describe the features and give examples of the phyla Annelida, Arthropoda, Mollusca and Echinodermata. Which is the largest phylum?',
     'Annelida: segmented, true coelom (earthworm). Arthropoda: jointed legs, open circulation (cockroach). Mollusca: soft body, muscular foot, often a shell (snail). Echinodermata: spiny skin, water-driven tube system, marine (starfish). Arthropoda is the largest.',
     '1 mark each phylum; 1 mark largest.'),
]

# ======================= ch12 Earth as a System
c12s1_defs = [
    ('the lithosphere', 'the solid outer layer of the Earth made of rocks and soil'),
    ('the hydrosphere', 'all the water on the Earth, in oceans, rivers, lakes, ice and underground'),
    ('the atmosphere', 'the blanket of air surrounding the Earth'),
    ('the biosphere', 'the zone of the Earth where life exists, where the lithosphere, hydrosphere and atmosphere meet'),
    ('the ozone layer', 'a layer of ozone (O₃) in the upper atmosphere that absorbs harmful ultraviolet rays from the Sun'),
    ('the greenhouse effect', 'the trapping of the Sun\'s heat by gases such as carbon dioxide and methane in the atmosphere'),
    ('weathering', 'the breaking down of rocks into smaller particles by physical, chemical and biological processes'),
]
c12s1_cats = {
    'a part of the lithosphere': ['granite rock', 'soil in a field', 'the Deccan plateau', 'sand on a beach'],
    'a part of the hydrosphere': ['the Ganga river', 'groundwater', 'the Arabian Sea', 'glaciers of the Himalayas', 'Chilika lake'],
    'a part of the atmosphere': ['oxygen gas', 'carbon dioxide gas', 'the ozone layer', 'nitrogen gas'],
    'a part of the biosphere': ['a mangrove forest', 'earthworms in the soil', 'fish in a river', 'a peepal tree'],
}
c12s1_mc = [
    ('The most abundant gas in air is:', 'nitrogen', 'oxygen', 'carbon dioxide', 'argon'),
    ('Air contains about what percentage of oxygen by volume?', '21%', '78%', '1%', '0.04%'),
    ('The atmosphere keeps the average temperature of the Earth fairly steady because:', 'it prevents a sudden rise in temperature during the day and slows the escape of heat at night', 'it contains only nitrogen', 'it reflects all light', 'it is very thin'),
    ('Winds are caused mainly by:', 'uneven heating of the Earth\'s surface', 'the Moon', 'the rotation of air molecules', 'ozone'),
    ('Soil is formed from rocks mainly by:', 'weathering by the Sun, water, wind and living organisms', 'ozone', 'volcanoes only', 'burning'),
    ('Which sphere includes all living organisms?', 'biosphere', 'lithosphere', 'hydrosphere', 'atmosphere'),
    ('On the Moon, the temperature varies from about −190 °C to 110 °C because:', 'there is no atmosphere', 'it is close to the Sun', 'it has oceans', 'it has ozone'),
]
c12s1_why = [
    ('How does the atmosphere act like a blanket for the Earth?', 'Air is a poor conductor of heat; it prevents a sharp rise in temperature in the day and slows heat loss at night.', '1 mark: day. 1 mark: night.'),
    ('How are lichens and mosses involved in soil formation?', 'Lichens release substances that powder the rock surface, and mosses then grow and break the rock further.', '1 mark each.'),
    ('Why is the ozone layer important for life on Earth?', 'It absorbs most of the harmful ultraviolet radiation from the Sun, which can cause skin cancer and damage organisms.', '1 mark: absorbs UV. 1 mark: UV harmful.'),
    ('How do land and sea breezes form near the coast of Chennai?', 'By day land heats faster, air above it rises and cooler air from the sea moves in (sea breeze); at night the land cools faster and air moves from land to sea (land breeze).', '1 mark each.'),
]
c12s1_ar = [
    ('The Moon has extreme temperatures.', 'The Moon has no atmosphere.', 'a', 'R explains A.'),
    ('Rain falls when water vapour in clouds condenses into drops.', 'Air cools as it rises, so the vapour condenses.', 'a', 'R explains A.'),
    ('The biosphere is the life-supporting zone of the Earth.', 'In it, the lithosphere, hydrosphere and atmosphere interact.', 'a', 'R explains A.'),
    ('Nitrogen is the least abundant gas in the air.', 'Nitrogen makes up 78% of the air.', 'd', 'A is false; R is true.'),
]

c12s2_defs = [
    ('a biogeochemical cycle', 'the cyclic movement of an element or substance between the living and non-living parts of the biosphere'),
    ('nitrogen fixation', 'the conversion of atmospheric nitrogen into compounds such as nitrates and ammonia that plants can use'),
    ('denitrification', 'the conversion of nitrates in the soil back into nitrogen gas by bacteria'),
    ('transpiration', 'the loss of water vapour from the aerial parts of a plant, mainly the leaves'),
    ('photosynthesis', 'the process by which green plants use carbon dioxide and water with sunlight to make glucose and release oxygen'),
    ('respiration', 'the process in which food is broken down using oxygen to release energy, carbon dioxide and water'),
]
c12s2_cats = {
    'adds carbon dioxide to the atmosphere': ['respiration of animals', 'burning of coal in a power plant', 'decomposition of dead leaves', 'a forest fire', 'exhaust of vehicles'],
    'removes carbon dioxide from the atmosphere': ['photosynthesis by plants', 'formation of carbonate shells in the sea', 'dissolving in sea water'],
}
c12s2_cats2 = {
    'part of the nitrogen cycle': ['fixation by Rhizobium in root nodules', 'lightning forming oxides of nitrogen', 'denitrification by bacteria', 'conversion of ammonia to nitrates'],
    'part of the water cycle': ['evaporation from the sea', 'condensation in clouds', 'transpiration from leaves', 'precipitation as rain'],
    'part of the oxygen cycle': ['release of O₂ in photosynthesis', 'use of O₂ in respiration', 'use of O₂ in combustion', 'formation of ozone from O₂'],
}
c12s2_mc = [
    ('Bacteria in the root nodules of pea and gram plants:', 'fix atmospheric nitrogen', 'release oxygen', 'cause disease', 'produce carbon dioxide'),
    ('Which process returns nitrogen gas to the atmosphere?', 'denitrification', 'nitrogen fixation', 'photosynthesis', 'transpiration'),
    ('Carbon is found in the Earth\'s crust as:', 'carbonate and hydrogen carbonate salts in minerals', 'nitrates', 'ozone', 'water'),
    ('Which of these increases the carbon dioxide level in air?', 'burning of fossil fuels', 'photosynthesis', 'growing trees', 'formation of shells'),
    ('Lightning helps in the nitrogen cycle because:', 'it converts nitrogen gas into oxides of nitrogen', 'it releases nitrogen from soil', 'it kills bacteria', 'it destroys ozone'),
    ('Oxygen is used up in nature by:', 'respiration, combustion and formation of oxides of nitrogen', 'photosynthesis only', 'nitrogen fixation only', 'evaporation'),
]
c12s2_why = [
    ('Why do farmers grow pulses between cereal crops?', 'Pulses have Rhizobium bacteria in their root nodules that fix nitrogen, making the soil more fertile for the next crop.', '1 mark: Rhizobium. 1 mark: soil fertility.'),
    ('Why is the level of carbon dioxide in the atmosphere rising?', 'More fossil fuels are burnt in vehicles, factories and power plants, and forests that absorb CO₂ are being cut down.', '1 mark: burning. 1 mark: deforestation.'),
    ('How does transpiration take part in the water cycle?', 'Plants absorb water from the soil and release it as water vapour from their leaves; the vapour condenses into clouds.', '1 mark: absorb and release. 1 mark: forms clouds.'),
    ('Why is the oxygen content of the air almost constant even though it is used up in respiration and burning?', 'Green plants release oxygen in photosynthesis, which balances its use.', '2 marks.'),
]
c12s2_ar = [
    ('Leguminous plants increase soil fertility.', 'Rhizobium bacteria in their root nodules fix atmospheric nitrogen.', 'a', 'R explains A.'),
    ('Increasing CO₂ in the atmosphere leads to global warming.', 'CO₂ traps heat radiated from the Earth.', 'a', 'R explains A.'),
    ('Plants cannot use atmospheric nitrogen directly.', 'Nitrogen is a very unreactive gas.', 'a', 'R explains A.'),
    ('Photosynthesis adds carbon dioxide to the air.', 'Photosynthesis releases oxygen.', 'd', 'A is false (it removes CO₂); R is true.'),
]
c12s2_seq_w = ['water evaporates from the sea and water bodies', 'water vapour rises and cools', 'it condenses into clouds', 'water falls as rain or snow', 'water flows into rivers or seeps into groundwater', 'it returns to the sea']
c12s2_seq_n = ['nitrogen in the air', 'fixed by Rhizobium or lightning into nitrogen compounds', 'converted to nitrates in the soil', 'absorbed by plants to make proteins', 'eaten by animals', 'dead remains decomposed to ammonia', 'nitrates turned back into nitrogen gas by denitrifying bacteria']


def _order(r, seq, what):
    k = r.randint(4, min(6, len(seq)))
    st = r.randint(0, len(seq) - k)
    s = seq[st:st + k]
    sh = s[:]
    while sh == s:
        r.shuffle(sh)
    L = '; '.join(f'({i + 1}) {x}' for i, x in enumerate(sh))
    return {'stem': f'Arrange these steps of the {what} in the correct order: {L}.', 'answer': ', '.join(str(sh.index(x) + 1) for x in s),
            'key': 'Correct order: ' + ' → '.join(s) + '.'}


def c12s2_order(r):
    return _order(r, c12s2_seq_w, 'water cycle') if r.random() < 0.5 else _order(r, c12s2_seq_n, 'nitrogen cycle')


def c12s2_co2(r):
    km = r.choice([10, 15, 20, 30, 40, 50])
    days = r.choice([25, 26, 30])
    e = r.choice([120, 150, 180, 200])  # g CO2 per km
    tot = km * days * e / 1000
    nm = name(r)
    tree = 22
    return {'stem': f'{nm}\'s father drives {km} km a day for {days} days a month in Lucknow. If his car emits {e} g of CO₂ per km, how much CO₂ does it give out in a month, and in a year? About how many trees would be needed to absorb a year\'s emission if one tree absorbs {tree} kg a year?',
            'answer': f'{num(tot, 1)} kg a month; {num(tot * 12, 1)} kg a year; at least {-(-tot * 12 // tree):.0f} trees.',
            'key': f'Month: {km} × {days} × {e} g = {num(tot, 1)} kg. Year: × 12 = {num(tot * 12, 1)} kg. Trees: {num(tot * 12, 1)}/{tree} ≈ {tot * 12 / tree:.1f}, so at least {-(-tot * 12 // tree):.0f} trees.'}


c12s3_defs = [
    ('pollution', 'the addition of unwanted substances to air, water or soil that harms living organisms'),
    ('a pollutant', 'a substance that pollutes the environment'),
    ('acid rain', 'rain containing acids formed when oxides of sulphur and nitrogen dissolve in rainwater'),
    ('smog', 'a mixture of smoke and fog that reduces visibility and harms breathing'),
    ('biodegradable waste', 'waste that can be broken down by microorganisms, such as vegetable peels'),
    ('non-biodegradable waste', 'waste that cannot be broken down by microorganisms, such as plastics and glass'),
    ('soil erosion', 'the removal of the fertile top layer of soil by wind or water'),
    ('eutrophication', 'excessive growth of algae in water bodies due to fertiliser run-off, which reduces dissolved oxygen'),
]
c12s3_cats = {
    'an air pollutant': ['carbon monoxide', 'sulphur dioxide', 'suspended particles from crop-stubble burning', 'oxides of nitrogen', 'smoke from brick kilns'],
    'a water pollutant': ['untreated sewage', 'fertiliser run-off', 'industrial effluents with mercury', 'detergents in a lake'],
    'a soil pollutant': ['plastic bags in fields', 'excess pesticides', 'heaps of non-biodegradable waste', 'excessive chemical fertilisers'],
}
c12s3_bio = {
    'biodegradable': ['vegetable peels', 'paper', 'cow dung', 'cotton cloth', 'dry leaves'],
    'non-biodegradable': ['polythene bags', 'glass bottles', 'aluminium cans', 'plastic toys', 'DDT'],
}
c12s3_mc = [
    ('Acid rain is mainly caused by:', 'oxides of sulphur and nitrogen', 'carbon dioxide only', 'oxygen', 'nitrogen gas'),
    ('Which gas is responsible for depletion of the ozone layer?', 'chlorofluorocarbons (CFCs)', 'oxygen', 'nitrogen', 'water vapour'),
    ('Fertiliser run-off into a lake leads to:', 'excessive algal growth and fall in oxygen', 'more fish', 'cleaner water', 'more ozone'),
    ('The Taj Mahal is turning yellowish mainly due to:', 'acid rain and air pollutants from industries', 'old age', 'sunlight', 'rainwater only'),
    ('Planting trees on slopes helps prevent:', 'soil erosion', 'acid rain', 'ozone depletion', 'earthquakes'),
    ('Which practice reduces air pollution in Delhi during winter?', 'not burning crop stubble and using public transport', 'burning more coal', 'using diesel generators', 'burning garbage'),
    ('Carbon monoxide is dangerous because it:', 'combines with haemoglobin and reduces the oxygen carried by blood', 'causes acid rain only', 'depletes ozone', 'causes eutrophication'),
]
c12s3_why = [
    ('Why do fish die in a lake that receives fertiliser run-off from fields?', 'Nutrients cause excess algae; when they die, decomposers use up the dissolved oxygen, so fish suffocate.', '1 mark: algae. 1 mark: oxygen depleted.'),
    ('Why is burning of crop stubble harmful in north India?', 'It releases smoke, fine particles and harmful gases, causing smog, breathing problems and loss of soil nutrients and microbes.', '1 mark: smoke/smog. 1 mark: health/soil.'),
    ('Why should we not throw polythene bags into drains and fields?', 'They are non-biodegradable, block drains, reduce soil fertility, and animals that eat them may die.', '1 mark each.'),
    ('How does deforestation lead to soil erosion?', 'Roots of trees hold the soil; without trees, rain and wind easily wash or blow away the fertile topsoil.', '1 mark: roots hold. 1 mark: washed away.'),
]
c12s3_ar = [
    ('Acid rain damages buildings made of marble.', 'Marble (calcium carbonate) reacts with acids.', 'a', 'R explains A.'),
    ('Plastic bags pollute the soil for many years.', 'Plastics are non-biodegradable.', 'a', 'R explains A.'),
    ('Using CNG in vehicles reduces air pollution.', 'CNG burns more cleanly than petrol or diesel.', 'a', 'R explains A.'),
    ('Vegetable peels are non-biodegradable.', 'Microorganisms can decompose vegetable peels.', 'd', 'A is false; R is true.'),
]


def c12s3_aqi(r):
    vals = r.sample([45, 80, 120, 160, 210, 260, 320, 380, 420, 460], 5)
    city = r.choice(['Delhi', 'Kanpur', 'Patna', 'Lucknow', 'Ghaziabad'])
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    avg = sum(vals) / 5
    bad = [d for d, v in zip(days, vals) if v > 200]
    mx = days[vals.index(max(vals))]
    return {'stem': f'The AQI of {city} for five days was: ' + ', '.join(f'{d} {v}' for d, v in zip(days, vals)) + '. AQI above 200 is "poor". Find (a) the average AQI, (b) the days with poor air, (c) the worst day.',
            'answer': f'(a) {num(avg, 1)} (b) {", ".join(bad) if bad else "none"} (c) {mx}',
            'key': f'Average = {sum(vals)}/5 = {num(avg, 1)}. Days above 200: {", ".join(bad) if bad else "none"}. Highest: {mx} ({max(vals)}).'}


def c12s3_waste(r):
    fam = r.choice([4, 5, 6])
    kg = r.choice([0.4, 0.5, 0.6])
    bio = r.choice([55, 60, 65, 70])
    tot = fam * kg * 30
    b = tot * bio / 100
    nm = name(r)
    return {'stem': f'{nm}\'s family of {fam} produces {num(kg)} kg of waste per person per day, of which {bio}% is biodegradable. How much biodegradable waste do they produce in 30 days, and what can they do with it?',
            'answer': f'{num(b, 1)} kg; compost it in a pit or compost bin to make manure.',
            'key': f'Total = {fam} × {num(kg)} × 30 = {num(tot, 1)} kg; biodegradable = {bio}% = {num(b, 1)} kg. Composting.'}


c12s4_defs = [
    ('a natural hazard', 'a natural event, such as an earthquake, flood, cyclone or landslide, that can cause loss of life and property'),
    ('an earthquake', 'a sudden shaking of the Earth caused by movement of rocks deep below the surface'),
    ('a cyclone', 'a huge, rapidly rotating storm with a low-pressure centre and very strong winds'),
    ('a tsunami', 'a series of huge sea waves caused by an earthquake or volcanic eruption under the sea'),
    ('sustainable development', 'development that meets present needs without harming the ability of future generations to meet theirs'),
    ('rainwater harvesting', 'collecting and storing rainwater for later use or to recharge groundwater'),
    ('a renewable resource', 'a resource that is replenished naturally in a short time, such as solar energy and wind'),
]
c12s4_cats = {
    'a renewable resource': ['solar energy', 'wind energy', 'forests (if managed well)', 'water in rivers'],
    'a non-renewable resource': ['coal', 'petroleum', 'natural gas', 'minerals such as iron ore'],
}
c12s4_haz = {
    'earthquake': ['Bhuj, Gujarat 2001', 'Latur, Maharashtra 1993'],
    'cyclone': ['Cyclone Fani, Odisha 2019', 'Cyclone Amphan, West Bengal 2020'],
    'flood': ['Kerala floods 2018', 'Assam floods in the Brahmaputra valley'],
    'tsunami': ['Indian Ocean tsunami, Tamil Nadu coast 2004'],
    'landslide': ['Kedarnath, Uttarakhand 2013', 'Wayanad, Kerala 2024'],
}
c12s4_haz = {f'an example of a {k}': v for k, v in c12s4_haz.items()}
c12s4_mc = [
    ('During an earthquake, if you are indoors you should:', 'take cover under a sturdy table away from windows', 'run down the stairs', 'stand near glass windows', 'use the lift'),
    ('Earthquake-prone areas in India include:', 'Kashmir, Uttarakhand, the North-East and the Rann of Kutch', 'only Kerala', 'only the Deccan plateau', 'none'),
    ('The intensity of an earthquake is measured on the:', 'Richter scale', 'Celsius scale', 'Beaufort scale only', 'pH scale'),
    ('Which of these helps conserve groundwater?', 'rainwater harvesting', 'using more borewells', 'cementing all open ground', 'cutting trees'),
    ('The 3 Rs to save the environment are:', 'Reduce, Reuse, Recycle', 'Read, Rest, Run', 'Remove, Replace, Repair', 'Reduce, Refill, Run'),
    ('Coastal areas are protected from cyclones and tsunamis by:', 'mangrove forests and early-warning systems', 'cutting mangroves', 'building on beaches', 'filling wetlands'),
]
c12s4_why = [
    ('Why should coal and petroleum be used carefully?', 'They are non-renewable; they took millions of years to form and will run out, and burning them pollutes the air.', '1 mark: non-renewable. 1 mark: pollution.'),
    ('How did early warnings reduce deaths during Cyclone Fani in Odisha?', 'Timely forecasts allowed lakhs of people to be moved to cyclone shelters before the storm reached the coast.', '1 mark: forecast. 1 mark: evacuation.'),
    ('Why are buildings in earthquake zones like Bhuj made with light materials and special designs?', 'They sway without collapsing, and lighter materials cause less harm if they fall.', '1 mark each.'),
    ('How does rainwater harvesting help a city like Chennai?', 'It recharges groundwater and provides water during dry months, reducing shortages.', '1 mark each.'),
]
c12s4_ar = [
    ('Mangrove forests reduce the damage caused by cyclones.', 'Mangroves act as a barrier that slows down winds and waves.', 'a', 'R explains A.'),
    ('Coal is a non-renewable resource.', 'Coal takes millions of years to form.', 'a', 'R explains A.'),
    ('We should use lifts during an earthquake.', 'Lifts move people quickly.', 'd', 'A is false – lifts can fail; use stairs only after shaking stops; R is true.'),
]


def c12s4_rwh(r):
    area = r.choice([50, 80, 100, 120, 150, 200])
    rain = r.choice([600, 800, 1000, 1200, 1400])
    eff = r.choice([0.6, 0.7, 0.8])
    vol = area * rain / 1000 * eff * 1000
    city = r.choice(['Bengaluru', 'Chennai', 'Jaipur', 'Hyderabad', 'Pune'])
    return {'stem': f'A school in {city} has a roof area of {area} m² and gets {rain} mm of rain a year. If {num(eff * 100)}% of the rain falling on the roof can be collected, how many litres can be harvested in a year? (1 m³ = 1000 L)',
            'answer': f'{inr(vol)[1:]} L',
            'key': f'Volume = {area} × {rain / 1000} × {num(eff)} = {num(vol / 1000, 1)} m³ = {inr(vol)[1:]} L.',
            'distractors': [f'{inr(vol / eff)[1:]} L', f'{inr(vol / 1000)[1:]} L', f'{inr(area * rain * eff * 10)[1:]} L']}


def c12s4_solar(r):
    kw = r.choice([2, 3, 5])
    h = r.choice([4, 5])
    rate = r.choice([6, 7, 8])
    units = kw * h * 30
    save = units * rate
    nm = name(r)
    return {'stem': f'{nm}\'s family installs a {kw} kW rooftop solar panel in Ahmedabad that works on average {h} hours of full sunlight a day. How many units (kWh) does it produce in 30 days, and how much money is saved at ₹{rate} per unit?',
            'answer': f'{units} kWh; {inr(save)}', 'key': f'Units = {kw} × {h} × 30 = {units} kWh; saving = {units} × {rate} = {inr(save)}.',
            'distractors': [f'{kw * h} kWh; {inr(kw * h * rate)}', f'{units * 2} kWh; {inr(save * 2)}', f'{units} kWh; {inr(save / 2)}']}


c12_hots = [
    ('A town near a river has a sugar mill that discharges hot waste water and a nearby farm that uses heavy fertilisers. Fish in the river are dying. Give two causes and suggest two remedies.', 'Hot water and fertiliser run-off lower dissolved oxygen (the latter causes algal blooms). Cool and treat the effluent before release; use organic manure and fertilisers in the right amount, and keep a green buffer strip along the bank.', '1 mark each cause. 1 mark remedies.'),
    ('Explain how cutting forests on a hill slope affects the water cycle, the soil and the people living below.', 'Less transpiration and less rain in the area; rain runs off quickly, eroding topsoil; groundwater recharge falls; floods and landslides increase for the people below.', '1 mark each.'),
    ('Suggest how a housing society in Bengaluru can follow the 3 Rs to reduce its waste and water problems.', 'Reduce: avoid plastic and fix leaks; Reuse: reuse bottles, use grey water for gardens; Recycle: segregate dry and wet waste, compost wet waste, recycle paper and plastic; plus rainwater harvesting.', '1 mark each R.'),
    ('Why does the carbon dioxide level rise in cities in winter evenings, and how can trees in parks help?', 'More fuel is burnt for heating and traffic, and still, cold air traps pollutants near the ground; trees absorb CO₂ by photosynthesis in the day and trap dust.', '1 mark cause. 1 mark trapping. 1 mark trees.'),
]
c12_case = [
    ('Read: In 2019, Cyclone Fani hit the Odisha coast with winds of over 200 km/h. Because of early warnings, about 12 lakh people were evacuated to cyclone shelters. Villages behind mangrove belts suffered less damage.\n'
     '(i) What is a cyclone? (ii) How did early warnings help? (iii) Why did mangroves reduce damage? (iv) Suggest one more step to reduce cyclone damage.',
     '(i) A huge rotating storm with a low-pressure centre and strong winds. (ii) People were moved to safety before it struck. (iii) They act as a barrier against winds and storm surges. (iv) Build cyclone-resistant shelters / plant more coastal trees / prepare emergency kits.', '1 mark each part.'),
    ('Read: Farmers in Punjab burn rice stubble in October. Within days the AQI in Delhi rises above 400, schools are closed and many people complain of breathlessness.\n'
     '(i) Name two pollutants released by burning stubble. (ii) Why do people feel breathless? (iii) How does burning harm the soil? (iv) Suggest one alternative to burning.',
     '(i) Fine particles (smoke), carbon monoxide, oxides of nitrogen. (ii) Fine particles and gases damage the lungs and reduce oxygen supply. (iii) It kills useful soil microbes and destroys nutrients. (iv) Use Happy Seeder machines, decompose stubble with bio-decomposer sprays, or use it as cattle feed/fuel pellets.', '1 mark each part.'),
]
c12_long = [
    ('Describe the nitrogen cycle with a labelled flow diagram. Why is the nitrogen cycle important for living organisms?',
     'Nitrogen gas in air → fixed by Rhizobium in root nodules, free-living bacteria and lightning into nitrates/ammonia → absorbed by plants to make proteins and nucleic acids → passed to animals → dead remains and wastes decomposed by bacteria into ammonia → converted to nitrites and nitrates → denitrifying bacteria return nitrogen gas to air. Important because nitrogen is essential for proteins and DNA.',
     '3 marks cycle; 1 mark diagram; 1 mark importance.'),
    ('Describe the carbon cycle and the oxygen cycle. How do human activities disturb them, and what are the consequences?',
     'Carbon: CO₂ taken up in photosynthesis, passed along food chains, returned by respiration, decomposition and combustion; also stored in carbonates and fossil fuels. Oxygen: released in photosynthesis, used in respiration, combustion and formation of oxides. Humans burn fossil fuels and cut forests, raising CO₂: greenhouse effect, global warming, melting glaciers, rise in sea level.',
     '2 marks carbon; 1 mark oxygen; 2 marks disturbance and effects.'),
    ('What are the causes and effects of air and water pollution? Suggest ways to prevent each.',
     'Air: vehicles, factories, burning fuel and stubble; effects – breathing diseases, acid rain, smog, global warming; prevention – CNG/electric vehicles, filters, no stubble burning, more trees. Water: sewage, industrial effluents, fertilisers; effects – diseases, eutrophication, fish death; prevention – sewage treatment, effluent treatment, controlled fertiliser use.',
     '2 marks air; 2 marks water; 1 mark prevention.'),
    ('What is a natural hazard? Describe the precautions to be taken before and during an earthquake, and two ways to use the Earth\'s resources sustainably.',
     'A natural event that causes loss of life and property. Before: earthquake-resistant buildings, fix heavy furniture, emergency kit. During: drop, cover and hold under a table, keep away from windows; if outside, stay in open ground away from buildings and wires. Sustainable use: 3 Rs, rainwater harvesting, renewable energy, afforestation.',
     '1 mark definition; 2 marks precautions; 2 marks sustainable use.'),
]


FAMILIES = {
    S + '09-st1': [TERM(c9s1_defs), DEF(c9s1_defs), MC(c9s1_mc, C='C1', D='D2'), CLS(c9s1_src, 'In which of these is sound produced by vibration of {}?', C='C2', D='D2', verb='produces sound by vibration of'), SA(c9s1_why), ARF(c9s1_ar),
                   G('C3', 'D2', 'numerical', c9s1_time), G('C3', 'D2', 'numerical', c9s1_lightning), G('C2', 'D2', 'mcq', c9s1_lightning),
                   SA(c9_hots[3:], C='C4', D='D4', type='multi_step'), G('C4', 'D3', 'multi_step', c9s1_time)],
    S + '09-st2': [TERM(c9s2_defs), DEF(c9s2_defs), MC(c9s2_mc, C='C1', D='D2'), SA(c9s2_why), ARF(c9s2_ar), G('C3', 'D1', 'numerical', c9s2_v), G('C3', 'D2', 'numerical', c9s2_lam),
                   G('C3', 'D2', 'numerical', c9s2_T), G('C3', 'D3', 'numerical', c9s2_count), G('C3', 'D4', 'multi_step', c9s2_graph), G('C4', 'D4', 'multi_step', c9s2_compare),
                   SA(c9_hots[:1], C='C4', D='D5', type='multi_step'), LONG(c9_long[:1], C='C4', D='D4'), G('C2', 'D2', 'mcq', c9s2_v), G('C2', 'D2', 'mcq', c9s2_lam)],
    S + '09-st3': [TERM(c9s3_defs), DEF(c9s3_defs), MC(c9s3_mc, C='C1', D='D2'), SA(c9s3_why), ARF(c9s3_ar), G('C3', 'D2', 'numerical', c9s3_echo), G('C3', 'D2', 'numerical', c9s3_dist),
                   G('C3', 'D3', 'numerical', c9s3_min), G('C4', 'D4', 'multi_step', c9s3_two), G('C4', 'D3', 'case', c9_case2, gap='G7'), SA(c9_hots[1:3], C='C4', D='D4', type='multi_step'),
                   LONG(c9_long[3:], C='C4', D='D4'), G('C2', 'D2', 'mcq', c9s3_dist)],
    S + '09-st4': [TERM(c9s4_defs), DEF(c9s4_defs), MC(c9s4_mc, C='C1', D='D2'), CLS(c9s4_cats, 'Which of the following is an example of {}?', C='C2', D='D2'), SA(c9s4_why), ARF(c9s4_ar),
                   G('C3', 'D2', 'numerical', c9s4_depth), G('C3', 'D2', 'numerical', c9s4_time), G('C2', 'D1', 'mcq', c9s4_class), G('C3', 'D3', 'explain', c9s4_bat),
                   G('C4', 'D3', 'case', c9_case, gap='G7'), G('C4', 'D4', 'multi_step', c9s4_bat), LONG(c9_long[1:3], C='C4', D='D3')],
    S + '10-st1': [TERM(c10s1_defs), DEF(c10s1_defs), CLS(c10s1_cats, 'Which of these organisms reproduces by {}?', C='C2', D='D2', verb='reproduces by'), MC(c10s1_mc, C='C1', D='D2'),
                   SA(c10s1_why), ARF(c10s1_ar), G('C3', 'D3', 'numerical', c10s1_grow), G('C2', 'D2', 'mcq', c10s1_grow),
                   SORT(c10s1_cats, 'Group these organisms by mode of reproduction, {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2)),
                   SA(c10_hots[3:], C='C4', D='D4', type='multi_step'), CLS(c10s1_cats, 'Which of these organisms reproduces by {}?', C='C4', D='D3', neg=True, neg_tpl='Which of these organisms does NOT reproduce by {}?', verb='reproduces by'),
                   LONG(c10_long[1:2], C='C4', D='D3')],
    S + '10-st2': [TERM(c10s2_defs), DEF(c10s2_defs), CLS(c10s2_cats, 'Which of the following plants is commonly {}?', C='C2', D='D2'), MC(c10s2_mc, C='C1', D='D2'), SA(c10s2_why), ARF(c10s2_ar),
                   SORT(c10s2_cats, 'Sort these plants into those {A} and those {B}: {L}.', C='C3', D='D3', n=(1, 2)), SA(c10_hots[:2], C='C4', D='D4', type='multi_step'),
                   CASE(c10_case[:1], C='C4', D='D3')],
    S + '10-st3': [TERM(c10s3_defs), DEF(c10s3_defs), CLS(c10s3_parts, 'Which of these is {}?', C='C1', D='D1'), CLS(c10s3_sex, 'Which of these is {}?', C='C2', D='D2'),
                   MC(c10s3_mc, C='C2', D='D2'), SA(c10s3_why), ARF(c10s3_ar), G('C3', 'D3', 'explain', c10s3_order), SORT(c10s3_parts, 'Classify these as {A} or {B}: {L}.', C='C3', D='D2', n=(1, 3)),
                   SA(c10_hots[2:3], C='C4', D='D4', type='multi_step'), CASE(c10_case[1:], C='C3', D='D3'), LONG(c10_long[:1], C='C4', D='D4'),
                   CLS(c10s3_parts, 'Which of these is {}?', C='C3', D='D3', neg=True)],
    S + '10-st4': [TERM(c10s4_defs), DEF(c10s4_defs), CLS(c10s4_cats, 'Which of the following animals is {}?', C='C2', D='D2'), CLS(c10s4_fert, 'Which of these animals shows {}?', C='C1', D='D2', verb='shows'),
                   MC(c10s4_mc, C='C1', D='D2'), SA(c10s4_why), ARF(c10s4_ar), SORT(c10s4_cats, 'Classify these animals as {A} or {B}: {L}.', C='C3', D='D2'),
                   G('C3', 'D3', 'numerical', c10s4_tadpole), G('C4', 'D4', 'multi_step', c10s4_tadpole), LONG(c10_long[2:], C='C4', D='D3'),
                   SORT(c10s4_fert, 'Classify these animals by {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2))],
    S + '11-st1': [TERM(c11s1_defs), DEF(c11s1_defs), MC(c11s1_mc, C='C1', D='D2'), G('C2', 'D2', 'mcq', c11s1_hier), SA(c11s1_why), ARF(c11s1_ar),
                   G('C3', 'D2', 'explain', c11s1_sortH), SA(c11_hots[1:2], C='C4', D='D4', type='multi_step')],
    S + '11-st2': [TERM(c11s2_defs), DEF(c11s2_defs), CLS(c11s2_kd, 'Which of these organisms belongs to {}?', C='C2', D='D2', verb='belongs to'), MC(c11s2_mc, C='C1', D='D2'),
                   G('C3', 'D2', 'mcq', c11s2_ident), SA(c11s2_why), ARF(c11s2_ar), SORT(c11s2_kd, 'Classify these organisms into {A} and {B}: {L}.', C='C3', D='D3', n=(1, 3)),
                   SA(c11_hots[:1], C='C4', D='D4', type='multi_step'), LONG(c11_long[:1], C='C4', D='D4'),
                   CLS(c11s2_kd, 'Which of these organisms belongs to {}?', C='C4', D='D3', neg=True, neg_tpl='Which of these organisms does NOT belong to {}?', verb='belongs to')],
    S + '11-st3': [TERM(c11s3_defs), DEF(c11s3_defs), CLS(c11s3_dv, 'Which of these plants is {}?', C='C2', D='D2'), CLS(c11s3_cot, 'Which of these plants is {}?', C='C1', D='D2'),
                   MC(c11s3_mc, C='C1', D='D2'), G('C3', 'D2', 'mcq', c11s3_ident), SA(c11s3_why), ARF(c11s3_ar), SORT(c11s3_dv, 'Classify these plants as {A} or {B}: {L}.', C='C3', D='D3', n=(1, 3)),
                   SORT(c11s3_cot, 'Classify these plants as {A} or {B}: {L}.', C='C3', D='D2'), SA(c11_hots[2:3], C='C4', D='D4', type='multi_step'),
                   CASE(c11_case[:1], C='C4', D='D3'), LONG(c11_long[1:2], C='C4', D='D4')],
    S + '11-st4': [TERM(c11s4_defs), DEF(c11s4_defs), CLS(c11s4_pd, 'Which of these animals is {}?', C='C2', D='D2'), CLS(c11s4_cd, 'Which of these animals is {}?', C='C2', D='D2'),
                   CLS(c11s4_ch, 'Which of these animals is {}?', C='C1', D='D1'), MC(c11s4_mc, C='C1', D='D2'), G('C3', 'D2', 'mcq', c11s4_ident), G('C3', 'D2', 'mcq', c11s4_cident),
                   SA(c11s4_why), ARF(c11s4_ar), SORT(c11s4_pd, 'Classify these animals as {A} or {B}: {L}.', C='C3', D='D3', n=(1, 3)), SORT(c11s4_cd, 'Classify these animals as {A} or {B}: {L}.', C='C3', D='D3', n=(1, 3)),
                   SA(c11_hots[3:], C='C4', D='D4', type='multi_step'), CASE(c11_case[1:], C='C4', D='D3'), LONG(c11_long[2:], C='C4', D='D4'),
                   CLS(c11s4_cd, 'Which of these animals is {}?', C='C4', D='D3', neg=True)],
    S + '11-st5': [TERM(c11s5_defs), DEF(c11s5_defs), MC(c11s5_mc, C='C1', D='D2'), G('C2', 'D2', 'mcq', c11s5_name), G('C2', 'D1', 'mcq', c11s5_genus), SA(c11s5_why), ARF(c11s5_ar),
                   G('C3', 'D3', 'explain', c11s5_correct),
                   SA([('The lion is Panthera leo and the leopard is Panthera pardus. The domestic cat is Felis catus. Which two are more closely related, and why?', 'The lion and the leopard, because they belong to the same genus Panthera; the cat is in a different genus (Felis), although all are in family Felidae.', '1 mark answer. 1 mark same genus. 1 mark cat different.')], C='C4', D='D4', type='multi_step')],
    S + '12-st1': [TERM(c12s1_defs), DEF(c12s1_defs), CLS(c12s1_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c12s1_mc, C='C1', D='D2'), SA(c12s1_why), ARF(c12s1_ar),
                   SORT(c12s1_cats, 'Classify these as {A} or {B}: {L}.', C='C3', D='D3', n=(1, 3)), CLS(c12s1_cats, 'Which of the following is {}?', C='C3', D='D3', neg=True),
                   SA([('Explain with one example each how the four spheres interact during the formation of rain.', 'Water evaporates from the hydrosphere (sea) into the atmosphere, condenses into clouds and falls on the lithosphere; plants (biosphere) add water by transpiration and use rain to grow.', '1 mark per sphere (any three).'),
                       ('Why can life not exist on the Moon even though it has a lithosphere?', 'It has no atmosphere (no oxygen, no protection from UV, extreme temperatures) and no liquid water, so there is no biosphere.', '1 mark atmosphere. 1 mark water. 1 mark temperature.')], C='C4', D='D4', type='multi_step')],
    S + '12-st2': [TERM(c12s2_defs), DEF(c12s2_defs), CLS(c12s2_cats, 'Which of these {}?', C='C2', D='D2', verb='—'), CLS(c12s2_cats2, 'Which of these is {}?', C='C1', D='D2'),
                   MC(c12s2_mc, C='C1', D='D2'), SA(c12s2_why), ARF(c12s2_ar), G('C3', 'D3', 'explain', c12s2_order), G('C3', 'D3', 'numerical', c12s2_co2),
                   SORT(c12s2_cats2, 'Classify these processes as {A} or {B}: {L}.', C='C3', D='D3', n=(1, 3)), G('C4', 'D4', 'multi_step', c12s2_co2),
                   SA(c12_hots[3:], C='C4', D='D4', type='multi_step'), LONG(c12_long[:2], C='C4', D='D4')],
    S + '12-st3': [TERM(c12s3_defs), DEF(c12s3_defs), CLS(c12s3_cats, 'Which of these is {}?', C='C2', D='D2'), CLS(c12s3_bio, 'Which of these wastes is {}?', C='C1', D='D1'),
                   MC(c12s3_mc, C='C1', D='D2'), SA(c12s3_why), ARF(c12s3_ar), G('C3', 'D3', 'numerical', c12s3_aqi), G('C3', 'D2', 'numerical', c12s3_waste),
                   SORT(c12s3_bio, 'Classify these wastes as {A} or {B}: {L}.', C='C3', D='D2'), SA(c12_hots[:1] + c12_hots[2:3], C='C4', D='D4', type='multi_step'),
                   CASE(c12_case[1:], C='C4', D='D3'), LONG(c12_long[2:3], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c12s3_aqi)],
    S + '12-st4': [TERM(c12s4_defs), DEF(c12s4_defs), CLS(c12s4_cats, 'Which of the following is {}?', C='C2', D='D1'), CLS(c12s4_haz, 'Which of these is {}?', C='C1', D='D2'),
                   MC(c12s4_mc, C='C1', D='D2'), SA(c12s4_why), ARF(c12s4_ar), G('C3', 'D2', 'numerical', c12s4_rwh), G('C3', 'D2', 'numerical', c12s4_solar),
                   SA(c12_hots[1:2], C='C4', D='D4', type='multi_step'), CASE(c12_case[:1], C='C4', D='D3'), LONG(c12_long[3:], C='C4', D='D3'), G('C2', 'D2', 'mcq', c12s4_rwh)],
}
