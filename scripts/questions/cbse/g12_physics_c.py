"""CBSE class 12 physics (NCERT Physics XII) families, chapters 11-14."""
from __future__ import annotations

import math

from qbank import F, ar, mcq, num, sup, name, two_names, CITIES  # noqa: F401
from g11_physics_util import polish, sig, g, NUM, NUM2, pool_mcq, pool_ar, pool_txt, term_mcq, tf_mcq  # noqa: F401

S = 'cbse-g12-physics-ch'
H = 6.63e-34
C = 3e8
QE = 1.6e-19
ME = 9.1e-31
MP = 1.67e-27
MN = 1.675e-27
K = 9e9
U_MEV = 931.5

METALS = [('caesium', 2.14), ('potassium', 2.30), ('sodium', 2.75), ('calcium', 3.20), ('molybdenum', 4.17), ('nickel', 5.15)]


# ======================================================== ch11 Dual Nature of Radiation and Matter
# st1 electron emission, photoelectric effect (experimental)

c11s1_terms = term_mcq([('work function', 'the minimum energy needed by an electron to escape from a metal surface'), ('threshold frequency', 'the minimum frequency of light that can eject photoelectrons'),
                        ('stopping potential', 'the negative collector potential that just stops the most energetic photoelectrons'), ('saturation current', 'the maximum photocurrent, when all emitted electrons are collected'),
                        ('thermionic emission', 'emission of electrons from a heated metal'), ('field emission', 'emission of electrons by a very strong electric field (~10⁸ V m⁻¹)')],
                       'Which of the following defines {a}?', 'Which term is {b}?', '{a}: {b}.')

c11s1_tf = tf_mcq('the photoelectric effect',
                  ['Photoelectric emission is instantaneous.', 'The saturation current is proportional to the intensity of light.', 'The stopping potential depends on the frequency, not on the intensity.',
                   'Below the threshold frequency, no emission occurs however intense the light.', 'The maximum kinetic energy of photoelectrons increases linearly with frequency.'],
                  ['The stopping potential increases with intensity.', 'Emission occurs below the threshold frequency if the light is intense enough.', 'There is a measurable time lag before emission begins.',
                   'The maximum kinetic energy depends on the intensity of light.', 'The saturation current is independent of intensity.'])

c11s1_explain = pool_txt([
    ('Why does the photocurrent reach a saturation value as the collector potential is increased?', 'At high positive potential all emitted electrons are collected; the number emitted per second is fixed by the intensity.', '2 marks.'),
    ('Why can\'t the wave theory explain the existence of a threshold frequency?', 'Wave theory says energy depends on intensity, so any frequency should eject electrons after enough time; experiment shows a sharp threshold.', '2 marks.'),
    ('Draw and explain the graph of stopping potential against frequency for two metals.', 'Parallel straight lines with slope h/e; intercepts on the frequency axis are the threshold frequencies, different for each metal.', '2 marks.'),
])

c11s1_ar = pool_ar([
    ('The stopping potential does not change when the intensity of incident light is increased.', 'The maximum kinetic energy of photoelectrons depends only on the frequency of light and the metal.', 'a', 'R explains A.'),
    ('Photoelectric current increases with intensity of light (above threshold).', 'More photons per second eject more electrons per second.', 'a', 'R explains A.'),
    ('Alkali metals such as caesium emit electrons even with visible light.', 'Alkali metals have low work functions.', 'a', 'R explains A.'),
    ('Photoelectric emission occurs for any frequency if the intensity is large.', 'Intensity is proportional to the number of photons per second.', 'd', 'A is false; R is true.'),
])


def c11s1_thr(r):
    m, w = r.choice(METALS)
    nu0 = w * QE / H
    lam0 = H * C / (w * QE)
    return NUM2(f'The work function of {m} is {g(w)} eV. Find its threshold frequency and threshold wavelength. (h = 6.63 × 10⁻³⁴ J s)', (nu0, lam0 * 1e9), ('Hz', 'nm'),
                f'ν₀ = φ/h = {g(w)} × 1.6 × 10⁻¹⁹/(6.63 × 10⁻³⁴) = {sig(nu0)} Hz (1); λ₀ = c/ν₀ = {sig(lam0 * 1e9)} nm (1).', wrongs=[(w / H, lam0 * 1e9), (nu0, lam0 * 1e6), (nu0 * 2, lam0 * 1e9 / 2)])


def c11s1_V0(r):
    V0 = r.choice([0.5, 0.8, 1, 1.2, 1.5, 2])
    K_ = QE * V0
    v = math.sqrt(2 * K_ / ME)
    return NUM2(f'The stopping potential in a photoelectric experiment is {g(V0)} V. Find the maximum kinetic energy and the maximum speed of the emitted electrons.', (K_, v), ('J', 'm s⁻¹'),
                f'K_max = eV₀ = {sig(K_)} J (1); v = √(2K/m) = {sig(v)} m s⁻¹ (1).', wrongs=[(V0, v), (K_, math.sqrt(K_ / ME)), (K_ * 2, v * math.sqrt(2))])


def c11s1_eV(r):
    w = r.choice([1.8, 2.14, 2.3, 2.75, 3.2, 4.2, 5.1])
    return NUM(f'Express a work function of {g(w)} eV in joule.', w * QE, 'J', f'1 eV = 1.6 × 10⁻¹⁹ J ⇒ φ = {g(w)} × 1.6 × 10⁻¹⁹ = {{ans}}.', wrongs=[w / QE, w * QE * 10, w * 1e-19], gap='G3')


c11s1_graph = pool_mcq([
    ('In a photoelectric experiment the intensity of light is doubled, the frequency unchanged. The stopping potential', 'stays the same', ['doubles', 'halves', 'becomes four times'], 'V₀ depends only on ν.'),
    ('In a photoelectric experiment the intensity of light is doubled, the frequency unchanged. The saturation current', 'doubles', ['stays the same', 'halves', 'becomes zero'], 'Number of photoelectrons ∝ intensity.'),
    ('The graph of stopping potential V₀ against frequency ν for a metal is a straight line whose slope is', 'h/e', ['e/h', 'φ/e', 'h'], 'eV₀ = hν − φ.'),
    ('For the same frequency of light, two metals A and B give stopping potentials 1.0 V and 2.0 V. The metal with the larger work function is', 'A', ['B', 'both equal', 'cannot be decided'], 'φ = hν − eV₀ is larger for smaller V₀.'),
])


def c11s1_case(r):
    who = name(r)
    m, w = r.choice(METALS[:4])
    lam = r.choice([300, 350, 400])
    E = 1240 / lam
    V0 = E - w
    if V0 < 0.1:
        raise ValueError
    return {'stem': (f'{who} studies the photoelectric effect using a {m} cathode (work function {g(w)} eV) and light of wavelength {lam} nm.\n'
                     '(i) Find the photon energy in eV. (ii) Find the stopping potential. (iii) What happens to the stopping potential if the intensity is doubled? (iv) What happens to the photocurrent if the wavelength is increased beyond the threshold?'),
            'answer': f'(i) {sig(E)} eV (ii) {sig(V0)} V (iii) no change (iv) it becomes zero (no emission)',
            'key': '(i) E = hc/λ = 1240/λ(nm) eV (1). (ii) eV₀ = E − φ (1). (iii) (1). (iv) (1).'}


# st2 Einstein's equation, photons

c11s2_terms = term_mcq([('Einstein\'s photoelectric equation', 'K_max = hν − φ₀'), ('energy of a photon', 'E = hν = hc/λ'), ('momentum of a photon', 'p = h/λ'),
                        ('photon', 'a quantum of electromagnetic radiation with zero rest mass')],
                       'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c11s2_tf = tf_mcq('photons',
                  ['A photon has zero rest mass.', 'All photons of a given frequency have the same energy.', 'Photons are electrically neutral.', 'Photon energy is inversely proportional to wavelength.',
                   'The number of photons is not necessarily conserved in a collision.'],
                  ['A photon has a large rest mass.', 'Photons are deflected by electric fields.', 'Photon energy increases with wavelength.', 'More intense light has photons of higher energy.',
                   'Photon energy depends on the intensity.'])

c11s2_explain = pool_txt([
    ('Explain using Einstein\'s equation why there is a threshold frequency.', 'K_max = hν − φ₀ ≥ 0 requires ν ≥ φ₀/h = ν₀.', '2 marks.'),
    ('How does Einstein\'s photon picture explain the instantaneous nature of photoelectric emission?', 'Energy is absorbed in one photon-electron collision, not accumulated over time.', '2 marks.'),
    ('Why do photoelectrons have a range of kinetic energies up to K_max?', 'Electrons deeper in the metal lose energy in collisions before escaping; only surface electrons have K_max.', '2 marks.'),
])

c11s2_ar = pool_ar([
    ('The maximum kinetic energy of photoelectrons increases linearly with frequency.', 'K_max = hν − φ₀.', 'a', 'R explains A.'),
    ('A photon of violet light has more energy than a photon of red light.', 'E = hc/λ and violet light has shorter wavelength.', 'a', 'R explains A.'),
    ('Increasing the intensity of light increases the energy of each photon.', 'Intensity is proportional to the number of photons per second per unit area.', 'd', 'A is false; R is true.'),
])


def c11s2_E(r):
    lam = r.choice([400, 450, 500, 550, 600, 650, 248, 310])
    E = H * C / (lam * 1e-9)
    return NUM2(f'Find the energy of a photon of wavelength {lam} nm in joule and in electron volt.', (E, E / QE), ('J', 'eV'), f'E = hc/λ = 6.63 × 10⁻³⁴ × 3 × 10⁸/({lam} × 10⁻⁹) = {sig(E)} J = {sig(E / QE)} eV.',
                wrongs=[(E * 1e9, E / QE * 1e9), (H * lam * 1e-9 / C, E / QE), (E, E * QE)])


def c11s2_K(r):
    m, w = r.choice(METALS)
    nu = r.choice([8, 9, 10, 12, 15]) * 1e14
    E = H * nu / QE
    Km = E - w
    if Km <= 0.05:
        raise ValueError
    return NUM(f'Light of frequency {g(nu)} Hz falls on a {m} surface (work function {g(w)} eV). Find the maximum kinetic energy of the photoelectrons in eV.', Km, 'eV',
               f'hν = 6.63 × 10⁻³⁴ × {g(nu)}/(1.6 × 10⁻¹⁹) = {sig(E)} eV (1); K_max = hν − φ = {{ans}} (1).', wrongs=[E + w, E, w - E if w > E else Km * 2])


def c11s2_V0(r):
    m, w = r.choice(METALS[:5])
    lam = r.choice([200, 250, 300, 330, 400])
    E = 1240 / lam
    V0 = E - w
    if V0 <= 0.05:
        raise ValueError
    return NUM(f'Ultraviolet light of wavelength {lam} nm falls on a {m} surface (work function {g(w)} eV). Find the stopping potential. (hc = 1240 eV nm)', V0, 'V',
               f'E = hc/λ = 1240/{lam} = {sig(E)} eV (1); eV₀ = E − φ ⇒ V₀ = {{ans}} (2).', wrongs=[E, E + w, V0 * 2])


def c11s2_rate(r):
    P = r.choice([1, 2, 5, 10, 100]) * 1e-3
    lam = r.choice([450, 532, 632.8, 650])
    n = P * lam * 1e-9 / (H * C)
    return NUM(f'A laser emits light of wavelength {g(lam)} nm with a power of {g(P * 1000)} mW. How many photons does it emit per second?', n, 's⁻¹',
               f'Energy per photon E = hc/λ = {sig(H * C / (lam * 1e-9))} J (1); n = P/E (1) = {{ans}} (1).', wrongs=[P / (H * lam * 1e-9), n / 1000, n * 2], gap='G5')


def c11s2_hphi(r):
    h_ = 6.6e-34
    phi = r.choice([2.0, 2.2, 2.5, 3.0])
    n1 = r.choice([8, 9, 10]) * 1e14
    n2 = n1 + r.choice([2, 3, 4]) * 1e14
    v1 = (h_ * n1 / QE) - phi
    v2 = (h_ * n2 / QE) - phi
    v1r, v2r = round(v1, 3), round(v2, 3)
    hh = QE * (v2r - v1r) / (n2 - n1)
    ph = hh * n1 / QE - v1r
    if v1r <= 0:
        raise ValueError
    return NUM2(f'When light of frequency {g(n1)} Hz falls on a metal the stopping potential is {g(v1r)} V; for {g(n2)} Hz it is {g(v2r)} V. Find Planck\'s constant and the work function of the metal (in eV).', (hh, ph), ('J s', 'eV'),
                f'eV₀ = hν − φ (1); subtract: h = e(V₂ − V₁)/(ν₂ − ν₁) = {sig(hh)} J s (2); φ = hν₁/e − V₁ = {sig(ph)} eV (2).', wrongs=[((v2r - v1r) / (n2 - n1), ph), (hh, ph + v1r), (hh * 2, ph)], gap='G5')


def c11s2_will(r):
    m, w = r.choice(METALS)
    lam = r.choice([300, 400, 450, 500, 550, 600])
    E = 1240 / lam
    yes = E > w
    return mcq(f'Light of wavelength {lam} nm falls on {m} (work function {g(w)} eV). Will photoelectrons be emitted? (hc = 1240 eV nm)',
               f'{"Yes" if yes else "No"}, because the photon energy is {sig(E)} eV, {"more" if yes else "less"} than {g(w)} eV',
               [f'{"No" if yes else "Yes"}, because the photon energy is {sig(E)} eV, {"less" if yes else "more"} than {g(w)} eV', f'Yes, but only if the intensity is high enough',
                f'No, because emission needs a time lag of a few seconds'], f'E = 1240/{lam} = {sig(E)} eV; emission needs E > φ.', r)


def c11s2_p(r):
    lam = r.choice([400, 500, 600, 0.1, 1])
    p = H / (lam * 1e-9)
    return NUM(f'Find the momentum of a photon of wavelength {g(lam)} nm.', p, 'kg m s⁻¹', f'p = h/λ = 6.63 × 10⁻³⁴/({g(lam)} × 10⁻⁹) = {{ans}}.', wrongs=[H * lam * 1e-9, H * C / (lam * 1e-9), p * C], gap='G3')


c11s2_derive = pool_txt([
    ('State Einstein\'s photoelectric equation and use it to explain the experimental laws of the photoelectric effect.', 'K_max = hν − φ₀', 'Equation and meaning (2); threshold (1); V₀ independent of intensity (1); instantaneous, current ∝ intensity (1).'),
    ('Explain the graph of stopping potential against frequency, and how h and φ₀ can be found from it.', 'V₀ = (h/e)ν − φ₀/e', 'Equation (2); slope h/e (1); intercept −φ₀/e and ν₀ (2).'),
])


# st3 de Broglie

c11s3_terms = term_mcq([('de Broglie wavelength', 'λ = h/p = h/(mv)'), ('de Broglie wavelength of an electron accelerated through V volts', 'λ = 1.227/√V nm'),
                        ('de Broglie wavelength in terms of kinetic energy', 'λ = h/√(2mK)'), ('wave-particle duality', 'matter and radiation both show wave and particle properties')],
                       'Which of the following gives the {a}?', 'Which term is {b}?', '{a}: {b}.')

c11s3_tf = tf_mcq('matter waves',
                  ['A faster electron has a shorter de Broglie wavelength.', 'Macroscopic objects have extremely small de Broglie wavelengths.', 'The de Broglie wavelength does not depend on the charge of the particle.',
                   'Electron microscopes use the wave nature of electrons.'],
                  ['A faster electron has a longer de Broglie wavelength.', 'Only charged particles have de Broglie waves.', 'A cricket ball shows easily measurable diffraction.',
                   'de Broglie wavelength increases with momentum.'])

c11s3_explain = pool_txt([
    ('Why don\'t we observe the wave nature of a moving cricket ball?', 'Its momentum is so large that λ = h/p (~10⁻³⁴ m) is far smaller than any aperture.', '2 marks.'),
    ('An electron and a proton have the same kinetic energy. Which has the longer de Broglie wavelength? Why?', 'The electron: λ = h/√(2mK) and the electron mass is smaller.', '2 marks.'),
    ('Why does an electron microscope have far better resolution than an optical microscope?', 'Electrons accelerated through kilovolts have λ ~ 10⁻¹¹ m, much shorter than visible light.', '2 marks.'),
])

c11s3_ar = pool_ar([
    ('An electron and a proton moving with the same speed have different de Broglie wavelengths.', 'λ = h/(mv) depends on mass.', 'a', 'R explains A.'),
    ('The de Broglie wavelength of an electron decreases when the accelerating voltage is increased.', 'λ = 1.227/√V nm.', 'a', 'R explains A.'),
    ('A particle at rest has zero de Broglie wavelength.', 'λ = h/p.', 'd', 'A is false: λ → ∞ as p → 0; R is true.'),
])


def c11s3_V(r):
    V = r.choice([50, 100, 150, 400, 900, 10000])
    lam = 1.227 / math.sqrt(V)
    return NUM(f'Find the de Broglie wavelength of an electron accelerated from rest through a potential difference of {V} V.', lam, 'nm', f'λ = 1.227/√V nm = 1.227/√{V} = {{ans}}.', wrongs=[1.227 / V, 1.227 * math.sqrt(V) / 100, lam * 10], gap='G3')


def c11s3_mv(r):
    obj, m, v = r.choice([('a ball of mass 0.06 kg', 0.06, r.choice([10, 20, 30])), ('an electron', ME, r.choice([1, 2, 5]) * 1e6), ('a dust particle of mass 1 μg', 1e-9, r.choice([1, 2.2]))])
    lam = H / (m * v)
    return NUM(f'Find the de Broglie wavelength of {obj} moving at {g(v)} m s⁻¹.', lam, 'm', f'λ = h/(mv) = 6.63 × 10⁻³⁴/({g(m)} × {g(v)}) = {{ans}}.', wrongs=[H * m * v, H / m, lam * 1e9])


def c11s3_K(r):
    p, m = r.choice([('a neutron', MN), ('a proton', MP), ('an electron', ME)])
    Kev = r.choice([0.025, 1, 10, 100, 150])
    lam = H / math.sqrt(2 * m * Kev * QE)
    return NUM(f'Find the de Broglie wavelength of {p} of kinetic energy {g(Kev)} eV.', lam, 'm', f'λ = h/√(2mK) = 6.63 × 10⁻³⁴/√(2 × {g(m)} × {g(Kev * QE)}) = {{ans}}.',
               wrongs=[H / (2 * m * Kev * QE), H / math.sqrt(m * Kev * QE), lam * 1e9])


def c11s3_ratio(r):
    pairs = [('a proton and an alpha particle', 1, 1, 4, 2), ('a proton and a deuteron', 1, 1, 2, 1), ('an alpha particle and a deuteron', 4, 2, 2, 1)]
    t, m1, q1, m2, q2 = r.choice(pairs)
    f = math.sqrt(m2 * q2 / (m1 * q1))
    return NUM(f'{t[0].upper() + t[1:]} are accelerated from rest through the same potential difference. Find the ratio λ₁ : λ₂ of their de Broglie wavelengths (first to second).', f, '',
               f'K = qV ⇒ λ = h/√(2mqV) ∝ 1/√(mq) (2); λ₁/λ₂ = √(m₂q₂/(m₁q₁)) = √({m2 * q2}/{m1 * q1}) = {{ans}} (1).', wrongs=[1 / f, m2 / m1, f * f], gap='G5')


def c11s3_same(r):
    lam = r.choice([0.1, 0.5, 1, 2])
    p = H / (lam * 1e-9)
    Ee = p * p / (2 * ME) / QE
    Ep = p * C / QE
    return NUM2(f'An electron and a photon each have a wavelength of {g(lam)} nm. Find the energy of each (in eV).', (Ee, Ep), ('eV', 'eV'),
                f'Same λ ⇒ same p = h/λ = {sig(p)} kg m s⁻¹ (1); electron: K = p²/2m = {sig(Ee)} eV (2); photon: E = pc = {sig(Ep)} eV (2).', wrongs=[(Ep, Ee), (Ee * 2, Ep), (Ee, Ep / 2)], gap='G5')


# ======================================================== ch12 Atoms
# st1 alpha-particle scattering, Rutherford model

c12s1_terms = term_mcq([('distance of closest approach', 'the distance at which an alpha particle moving head-on momentarily stops: r₀ = 2kZe²/K'), ('impact parameter', 'the perpendicular distance of the initial velocity of the alpha particle from the centre of the nucleus'),
                        ('nucleus (Rutherford)', 'a tiny, dense, positively charged core containing almost all the mass of the atom'), ('Geiger-Marsden experiment', 'scattering of alpha particles by a thin gold foil')],
                       'Which of the following describes the {a}?', 'Which term is {b}?', '{a}: {b}.')

c12s1_tf = tf_mcq("Rutherford's alpha-scattering experiment",
                  ['Most alpha particles passed through the gold foil undeflected.', 'A very small fraction were deflected by more than 90°.', 'Small impact parameter means large scattering angle.',
                   'The size of the nucleus is about 10⁻⁵ of the size of the atom.'],
                  ['Most alpha particles were scattered back.', 'Large impact parameter means large scattering angle.', 'The nucleus occupies most of the volume of the atom.',
                   'Rutherford\'s model explained the stability of the atom.'])

c12s1_explain = pool_txt([
    ('What did Rutherford conclude from the fact that most alpha particles went straight through the gold foil?', 'Most of the atom is empty space.', '2 marks.'),
    ('Why was a very thin gold foil used in the alpha-scattering experiment?', 'To make sure each alpha particle was scattered by only one nucleus.', '2 marks.'),
    ('State one drawback of Rutherford\'s model of the atom.', 'An orbiting (accelerated) electron should radiate energy and spiral into the nucleus; it also cannot explain line spectra.', '2 marks.'),
])

c12s1_ar = pool_ar([
    ('Only a very small fraction of alpha particles are scattered back in the Geiger-Marsden experiment.', 'The nucleus is very small compared with the atom.', 'a', 'R explains A.'),
    ('Rutherford\'s model cannot explain the stability of atoms.', 'An accelerated charge radiates electromagnetic energy.', 'a', 'R explains A.'),
    ('Alpha particles with smaller impact parameter are deflected less.', 'The Coulomb force is stronger closer to the nucleus.', 'd', 'A is false: they are deflected more; R is true.'),
])


def c12s1_closest(r):
    Kmev = r.choice([4, 5, 5.5, 7.7, 8])
    Z, el = r.choice([(79, 'gold'), (47, 'silver'), (29, 'copper'), (82, 'lead')])
    r0 = 2 * K * Z * QE * QE / (Kmev * 1e6 * QE)
    return NUM(f'An alpha particle of kinetic energy {g(Kmev)} MeV is projected head-on at a {el} nucleus (Z = {Z}). Find the distance of closest approach.', r0, 'm',
               f'K = k(2e)(Ze)/r₀ ⇒ r₀ = 2kZe²/K (2) = 2 × 9 × 10⁹ × {Z} × (1.6 × 10⁻¹⁹)²/({g(Kmev)} × 1.6 × 10⁻¹³) = {{ans}} (1).',
               wrongs=[r0 / 2, K * Z * QE / (Kmev * 1e6), r0 * 1000], gap='G3')


def c12s1_factor(r):
    k = r.choice([2, 3, 4])
    return NUM(f'If the kinetic energy of the alpha particle is made {k} times, by what factor does its distance of closest approach to a given nucleus change?', 1 / k, '', f'r₀ = 2kZe²/K ∝ 1/K ⇒ factor = 1/{k} = {{ans}}.',
               wrongs=[float(k), 1 / k ** 2, 1 / math.sqrt(k)], gap='G3')


def c12s1_need(r):
    d = r.choice([10, 20, 30, 50])
    Z, el = r.choice([(79, 'gold'), (29, 'copper')])
    Kj = 2 * K * Z * QE * QE / (d * 1e-15)
    return NUM(f'What minimum kinetic energy (in MeV) must an alpha particle have to approach a {el} nucleus (Z = {Z}) to within {d} fm, moving head-on?', Kj / QE / 1e6, 'MeV',
               f'K = 2kZe²/r₀ (2) = 2 × 9 × 10⁹ × {Z} × (1.6 × 10⁻¹⁹)²/({d} × 10⁻¹⁵) J (1) = {sig(Kj)} J = {{ans}} (1).', wrongs=[Kj / QE / 2e6, Kj / QE / 1e3, Kj / QE / 1e6 * 2], gap='G5')


c12s1_mcq = pool_mcq([
    ('In the alpha-scattering experiment, the number of alpha particles scattered through large angles was', 'very small', ['very large', 'about half of all', 'zero'], 'Only about 1 in 8000 was scattered by more than 90°.'),
    ('The distance of closest approach of an alpha particle to a nucleus gives an estimate of', 'an upper limit on the size of the nucleus', ['the size of the atom', 'the mass of the nucleus', 'the wavelength of the alpha particle'], 'The nucleus must be smaller than r₀.'),
    ('According to Rutherford, the atom consists of', 'a tiny massive positive nucleus with electrons revolving round it', ['a uniform sphere of positive charge with embedded electrons', 'electrons at the centre with protons outside', 'only neutral particles'], 'Nuclear model.'),
])


# st2 Bohr model

c12s2_terms = term_mcq([('Bohr\'s quantisation condition', 'angular momentum mvr = nh/2π'), ('radius of the nth orbit of hydrogen', 'r_n = 0.529 n² Å'),
                        ('energy of the nth level of hydrogen', 'E_n = −13.6/n² eV'), ('Bohr\'s frequency condition', 'hν = E_i − E_f'), ('ionisation energy of hydrogen (ground state)', '13.6 eV')],
                       'Which of the following gives {a}?', 'Which term is {b}?', '{a}: {b}.')

c12s2_tf = tf_mcq('the Bohr model',
                  ['Electrons in stationary orbits do not radiate.', 'The total energy of the electron in an orbit is negative.', 'Kinetic energy = −(total energy) in a Bohr orbit.',
                   'The orbital radius is proportional to n².', 'The speed of the electron decreases as n increases.'],
                  ['Electrons radiate continuously while in a stationary orbit.', 'The total energy of the electron in an orbit is positive.', 'Orbital radius is proportional to n.',
                   'Speed of the electron increases with n.', 'The Bohr model explains spectra of all multi-electron atoms.'])

c12s2_explain = pool_txt([
    ('State Bohr\'s three postulates.', 'Stationary orbits without radiation; angular momentum = nh/2π; radiation hν = E_i − E_f on jumping.', '2 marks.'),
    ('Why is the total energy of an electron in a Bohr orbit negative?', 'It is bound to the nucleus; energy must be supplied to free it (zero at infinity).', '2 marks.'),
    ('What is the significance of the negative sign in E_n = −13.6/n² eV?', 'The electron is bound; 13.6/n² eV is needed to remove it from level n.', '2 marks.'),
])

c12s2_ar = pool_ar([
    ('The total energy of the electron in a hydrogen atom is negative.', 'The electron is bound to the nucleus.', 'a', 'R explains A.'),
    ('Energy levels of hydrogen come closer together at higher n.', 'E_n ∝ −1/n².', 'a', 'R explains A.'),
    ('In a Bohr orbit, the kinetic energy of the electron is twice its total energy.', 'PE = −2KE in a Bohr orbit.', 'd', 'A is false: KE = −E; R is true.'),
])


def c12s2_r(r):
    n = r.choice([1, 2, 3, 4, 5])
    Z, sp = r.choice([(1, 'a hydrogen atom'), (2, 'a He⁺ ion'), (3, 'a Li²⁺ ion')])
    rn = 0.529 * n * n / Z
    return NUM(f'Find the radius of the n = {n} orbit of {sp} using the Bohr model. (Bohr radius a₀ = 0.529 Å)', rn, 'Å', f'r_n = a₀n²/Z = 0.529 × {n}²/{Z} = {{ans}}.', wrongs=[0.529 * n / Z, 0.529 * n * n * Z, 0.529 * n * n], gap='G3')


def c12s2_E(r):
    n = r.choice([1, 2, 3, 4, 5])
    Z, sp = r.choice([(1, 'hydrogen'), (2, 'He⁺'), (1, 'hydrogen')])
    E = -13.6 * Z * Z / (n * n)
    return NUM(f'Find the energy of the electron in the n = {n} level of {sp}.', E, 'eV', f'E_n = −13.6 Z²/n² = −13.6 × {Z * Z}/{n * n} = {{ans}}.', wrongs=[-E, -13.6 * Z / n, -13.6 * Z * Z / n])


def c12s2_jump(r):
    ni, nf = r.choice([(1, 2), (1, 3), (2, 3), (2, 4), (1, 4), (3, 5)])
    dE = 13.6 * (1 / ni ** 2 - 1 / nf ** 2)
    return NUM2(f'How much energy is needed to excite a hydrogen atom from n = {ni} to n = {nf}? What is the wavelength of the photon emitted when it returns directly to n = {ni}? (hc = 1240 eV nm)', (dE, 1240 / dE), ('eV', 'nm'),
                f'ΔE = 13.6(1/{ni}² − 1/{nf}²) = {sig(dE)} eV (1.5); λ = hc/ΔE = 1240/{sig(dE)} = {sig(1240 / dE)} nm (1.5).', wrongs=[(13.6 / nf ** 2, 1240 * nf ** 2 / 13.6), (dE, 1240 * dE), (13.6 * (1 / ni - 1 / nf), 1240 / (13.6 * (1 / ni - 1 / nf)))])


def c12s2_ion(r):
    n = r.choice([1, 2, 3, 4])
    return NUM(f'How much energy is needed to ionise a hydrogen atom whose electron is in the n = {n} level?', 13.6 / n ** 2, 'eV', f'Energy needed = 0 − E_n = 13.6/{n}² = {{ans}}.', wrongs=[13.6, 13.6 / n, 13.6 * n * n], gap='G3')


def c12s2_KEPE(r):
    n = r.choice([1, 2, 3, 4])
    E = -13.6 / n ** 2
    return NUM2(f'The total energy of the electron in the n = {n} state of hydrogen is {sig(E)} eV. Find its kinetic energy and potential energy in this state.', (-E, 2 * E), ('eV', 'eV'),
                f'In a Bohr orbit K = −E = {sig(-E)} eV (1.5) and U = 2E = {sig(2 * E)} eV (1.5).', wrongs=[(E, -2 * E), (-2 * E, E), (-E / 2, E / 2)], gap='G5')


def c12s2_v(r):
    n = r.choice([1, 2, 3, 4])
    v = 2.18e6 / n
    T = 2 * math.pi * 0.529e-10 * n * n / v
    return NUM2(f'In the Bohr model, the speed of the electron in the ground state of hydrogen is 2.18 × 10⁶ m s⁻¹. Find its speed in the n = {n} orbit and the time for one revolution there.', (v, T), ('m s⁻¹', 's'),
                f'v_n = v₁/n = {sig(v)} m s⁻¹ (1); r_n = 0.529n² Å (1); T = 2πr_n/v_n = {sig(T)} s (1).', wrongs=[(2.18e6 * n, T / n ** 2), (2.18e6 / n ** 2, T), (v, T * 2 * math.pi)])


c12s2_derive = pool_txt([
    ('Using Bohr\'s postulates, derive the expression for the radius of the nth orbit of the hydrogen atom.', 'r_n = n²h²ε₀/(πme²)', 'Centripetal = Coulomb force (2); mvr = nh/2π (1); eliminate v (2).'),
    ('Derive the expression for the total energy of the electron in the nth orbit of hydrogen, and show that it is negative.', 'E_n = −me⁴/(8ε₀²n²h²) = −13.6/n² eV', 'KE = ke²/2r (2); PE = −ke²/r (1); total −ke²/2r with r_n (2).'),
])


def c12s2_case(r):
    who = name(r)
    return {'stem': (f'{who} draws the energy-level diagram of the hydrogen atom: E₁ = −13.6 eV, E₂ = −3.4 eV, E₃ = −1.51 eV, E₄ = −0.85 eV.\n'
                     '(i) What is the ionisation energy from the ground state? (ii) Which transition among these gives the longest-wavelength Lyman line? Find its energy. (iii) How many spectral lines can be emitted when atoms fall from n = 4 to the ground state? (iv) Which of these lines are in the visible (Balmer) series?'),
            'answer': '(i) 13.6 eV (ii) n = 2 → 1, 10.2 eV (iii) 6 (iv) 3 → 2 and 4 → 2',
            'key': '(i) (1). (ii) smallest energy gap to n = 1 (1). (iii) n(n − 1)/2 (1). (iv) transitions ending on n = 2 (1).'}


# st3 spectra

SERIES = [('Lyman series', 'transitions ending on n = 1, in the ultraviolet'), ('Balmer series', 'transitions ending on n = 2, in the visible region'),
          ('Paschen series', 'transitions ending on n = 3, in the infrared'), ('Brackett series', 'transitions ending on n = 4, in the infrared'), ('Pfund series', 'transitions ending on n = 5, in the far infrared')]

c12s3_terms = term_mcq(SERIES, 'The {a} of hydrogen consists of', 'Which series of hydrogen consists of {b}?', '{a}: {b}.')

c12s3_tf = tf_mcq('the hydrogen spectrum',
                  ['The Balmer series lies in the visible region.', 'Each element has its own characteristic line spectrum.', 'The series limit has the shortest wavelength of the series.',
                   'de Broglie explained Bohr\'s quantisation: an orbit holds a whole number of electron wavelengths.'],
                  ['The Lyman series lies in the visible region.', 'The series limit has the longest wavelength of the series.', 'Line spectra are continuous.',
                   'The Paschen series lies in the ultraviolet.'])

c12s3_explain = pool_txt([
    ('How did de Broglie explain Bohr\'s second postulate?', 'Stationary orbits have circumference equal to a whole number of electron wavelengths: 2πr = nλ = nh/mv ⇒ mvr = nh/2π.', '2 marks.'),
    ('Why do atoms emit line spectra rather than continuous spectra?', 'Energy levels are discrete; photons are emitted only with energies equal to the differences between levels.', '2 marks.'),
])

c12s3_ar = pool_ar([
    ('The lines of the Lyman series lie in the ultraviolet region.', 'Transitions to n = 1 involve large energy differences.', 'a', 'R explains A.'),
    ('Bohr\'s quantisation condition follows from de Broglie\'s hypothesis.', 'A stable orbit must contain a whole number of electron wavelengths.', 'a', 'R explains A.'),
    ('The Balmer series lies in the infrared region.', 'Balmer lines end on n = 2.', 'd', 'A is false: it is visible; R is true.'),
])

RH = 1.097e7


def c12s3_lam(r):
    n1 = r.choice([1, 2, 3])
    n2 = n1 + r.choice([1, 2, 3])
    inv = RH * (1 / n1 ** 2 - 1 / n2 ** 2)
    return NUM(f'Find the wavelength of the spectral line emitted when the electron in a hydrogen atom jumps from n = {n2} to n = {n1}. (R = 1.097 × 10⁷ m⁻¹)', 1e9 / inv, 'nm',
               f'1/λ = R(1/{n1}² − 1/{n2}²) = {sig(inv)} m⁻¹ ⇒ λ = {{ans}}.', wrongs=[1e9 * inv / 1e14, 1e9 / (RH * (1 / n1 - 1 / n2)), 2e9 / inv])


def c12s3_lines(r):
    n = r.choice([3, 4, 5, 6])
    return NUM(f'Hydrogen atoms are excited to the n = {n} level. How many different spectral lines can they emit as they return to the ground state?', n * (n - 1) / 2, '',
               f'Number of lines = n(n − 1)/2 = {n} × {n - 1}/2 = {{ans}}.', wrongs=[n - 1, n * n, n * (n + 1) / 2], gap='G3', n=2)


def c12s3_limit(r):
    n1, nm = r.choice([(1, 'Lyman'), (2, 'Balmer'), (3, 'Paschen')])
    lam = n1 ** 2 / RH * 1e9
    return NUM(f'Find the shortest wavelength (series limit) of the {nm} series of hydrogen. (R = 1.097 × 10⁷ m⁻¹)', lam, 'nm', f'Series limit: n₂ → ∞, 1/λ = R/{n1}² ⇒ λ = {n1}²/R = {{ans}}.',
               wrongs=[1e9 / RH, n1 / RH * 1e9, lam * 4 / 3])


def c12s3_ratio(r):
    a, b = r.choice([(('Lyman', 1), ('Balmer', 2)), (('Balmer', 2), ('Paschen', 3)), (('Lyman', 1), ('Paschen', 3)), (('Paschen', 3), ('Brackett', 4))])
    kind = r.choice(['longest', 'shortest'])
    if kind == 'longest':
        la = 1 / (1 / a[1] ** 2 - 1 / (a[1] + 1) ** 2)
        lb = 1 / (1 / b[1] ** 2 - 1 / (b[1] + 1) ** 2)
        k = f'Longest λ: transition from n + 1 to n, 1/λ = R(1/n² − 1/(n + 1)²) (2); ratio = [1/{b[1]}² − 1/{b[1] + 1}²]/[1/{a[1]}² − 1/{a[1] + 1}²] (2) = {{ans}} (1).'
    else:
        la, lb = a[1] ** 2, b[1] ** 2
        k = f'Shortest λ (series limit): 1/λ = R/n² ⇒ λ = n²/R (2); ratio = {a[1]}²/{b[1]}² (2) = {{ans}} (1).'
    return NUM(f'Find the ratio of the {kind} wavelength in the {a[0]} series to the {kind} wavelength in the {b[0]} series of hydrogen.', la / lb, '', k,
               wrongs=[lb / la, a[1] / b[1], la / lb * 2], gap='G5')


def c12s3_deB(r):
    n = r.choice([1, 2, 3, 4])
    rn = 0.529e-10 * n * n
    lam = 2 * math.pi * rn / n
    return NUM(f'Using de Broglie\'s explanation of Bohr\'s orbits, find the de Broglie wavelength of the electron in the n = {n} orbit of hydrogen (r_n = 0.529n² Å).', lam * 1e10, 'Å',
               f'2πr_n = nλ (2) ⇒ λ = 2πr_n/n = 2π × 0.529 × {n} Å (1) = {{ans}} (1).', wrongs=[2 * math.pi * rn * 1e10, lam * 1e10 / n, 0.529 * n], gap='G5')


def c12s3_which(r):
    n2, n1, s = r.choice([(3, 1, 'Lyman'), (5, 2, 'Balmer'), (4, 3, 'Paschen'), (6, 4, 'Brackett'), (2, 1, 'Lyman'), (4, 2, 'Balmer')])
    others = [x[0] for x in SERIES if not x[0].startswith(s)]
    return mcq(f'The transition from n = {n2} to n = {n1} in a hydrogen atom produces a line of the', f'{s} series', r.sample(others, 3), f'Lines ending on n = {n1} belong to the {s} series.', r)


# ======================================================== ch13 Nuclei
# st1 composition and size

c13s1_terms = term_mcq([('isotopes', 'nuclides with the same Z but different A'), ('isobars', 'nuclides with the same A but different Z'), ('isotones', 'nuclides with the same number of neutrons N'),
                        ('atomic mass unit', '1/12 of the mass of a carbon-12 atom, 1.660539 × 10⁻²⁷ kg'), ('nuclear radius', 'R = R₀A^(1/3), with R₀ ≈ 1.2 fm')],
                       'Which of the following defines {a}?', 'Which term is {b}?', '{a}: {b}.')

c13s1_tf = tf_mcq('the nucleus',
                  ['Nuclear density is nearly the same for all nuclei.', 'The nuclear radius is proportional to A^(1/3).', 'A nucleus contains Z protons and A − Z neutrons.',
                   'The neutron was discovered by Chadwick.'],
                  ['Nuclear density increases with mass number.', 'Nuclear radius is proportional to A.', 'A nucleus contains A protons and Z neutrons.',
                   'Isotopes have the same number of neutrons.'])

c13s1_explain = pool_txt([
    ('Show that nuclear density is independent of mass number.', 'Volume ∝ R³ ∝ A and mass ∝ A, so density = mass/volume is constant (~2.3 × 10¹⁷ kg m⁻³).', '2 marks.'),
    ('Why are isotopes of an element chemically identical?', 'They have the same number of protons and hence the same electron arrangement.', '2 marks.'),
])

c13s1_ar = pool_ar([
    ('The density of nuclear matter is the same for all nuclei.', 'R = R₀A^(1/3), so volume ∝ A.', 'a', 'R explains A.'),
    ('Isotopes of an element have the same chemical properties.', 'Isotopes have the same atomic number.', 'a', 'R explains A.'),
    ('Isobars have the same number of neutrons.', 'Isobars have the same mass number.', 'd', 'A is false; R is true.'),
])

NUCS = [('¹²C', 6, 12), ('¹⁴N', 7, 14), ('¹⁶O', 8, 16), ('²³Na', 11, 23), ('²⁷Al', 13, 27), ('⁴⁰Ca', 20, 40), ('⁵⁶Fe', 26, 56), ('⁶⁴Cu', 29, 64), ('¹⁰⁷Ag', 47, 107),
        ('¹⁹⁷Au', 79, 197), ('²⁰⁸Pb', 82, 208), ('²³⁵U', 92, 235), ('²³⁸U', 92, 238), ('¹²⁵Te', 52, 125)]


def c13s1_count(r):
    s, Z, A = r.choice(NUCS)
    return {'stem': f'How many protons and neutrons are there in the nucleus {s} (Z = {Z})?', 'answer': f'{Z} protons, {A - Z} neutrons', 'key': f'Protons = Z = {Z}; neutrons N = A − Z = {A} − {Z} = {A - Z}.',
            'distractors': [f'{A - Z} protons, {Z} neutrons', f'{Z} protons, {A} neutrons', f'{A} protons, {Z} neutrons']}


def c13s1_R(r):
    s, Z, A = r.choice(NUCS)
    R = 1.2 * A ** (1 / 3)
    return NUM(f'Estimate the radius of the nucleus {s}. (R₀ = 1.2 fm)', R, 'fm', f'R = R₀A^(1/3) = 1.2 × {A}^(1/3) = {{ans}}.', wrongs=[1.2 * A, 1.2 * A ** 0.5, 1.2 * Z ** (1 / 3)], gap='G3')


def c13s1_ratio(r):
    (s1, A1), (s2, A2) = r.sample([('⁸Be', 8), ('²⁷Al', 27), ('⁶⁴Cu', 64), ('¹²⁵Te', 125), ('²¹⁶Po', 216), ('¹H', 1)], 2)
    f = (A1 / A2) ** (1 / 3)
    return NUM(f'Find the ratio of the nuclear radii of {s1} and {s2}.', f, '', f'R ∝ A^(1/3) ⇒ R₁/R₂ = ({A1}/{A2})^(1/3) = {{ans}}.', wrongs=[A1 / A2, (A1 / A2) ** 0.5, (A2 / A1) ** (1 / 3)])


def c13s1_density(r):
    s, Z, A = r.choice(NUCS)
    m = A * 1.66e-27
    R = 1.2e-15 * A ** (1 / 3)
    rho = m / (4 / 3 * math.pi * R ** 3)
    return NUM(f'Estimate the density of the nucleus {s}. (1 u = 1.66 × 10⁻²⁷ kg, R₀ = 1.2 fm) Compare it with the density of water.', rho, 'kg m⁻³',
               f'm ≈ A u = {sig(m)} kg (1); R = R₀A^(1/3) = {sig(R)} m (1); ρ = m/(4πR³/3) = {{ans}} (1), about 10¹⁴ times that of water; the same for all nuclei.', wrongs=[rho * A, rho / 1000, m / R ** 3], gap='G5')


def c13s1_avg(r):
    el, (m1, p1), (m2, p2) = r.choice([('chlorine', (34.98, 75.4), (36.98, 24.6)), ('boron', (10.01, 19.9), (11.01, 80.1)), ('copper', (62.93, 69.2), (64.93, 30.8))])
    avg = (m1 * p1 + m2 * p2) / 100
    return NUM(f'Natural {el} has two isotopes of masses {m1} u ({p1}%) and {m2} u ({p2}%). Find its average atomic mass.', avg, 'u', f'm = ({m1} × {p1} + {m2} × {p2})/100 = {{ans}}.', wrongs=[(m1 + m2) / 2, m1, m2], n=4)


def c13s1_class(r):
    pairs = [('¹H and ²H', 'isotopes'), ('¹⁴C and ¹⁴N', 'isobars'), ('³H and ⁴He', 'isotones'), ('²³⁵U and ²³⁸U', 'isotopes'), ('⁴⁰Ar and ⁴⁰Ca', 'isobars'), ('¹³C and ¹⁴N', 'isotones'), ('³H and ³He', 'isobars'), ('¹²C and ¹⁴C', 'isotopes')]
    p, c = r.choice(pairs)
    return mcq(f'The nuclides {p} are', c, [x for x in ('isotopes', 'isobars', 'isotones', 'isomers') if x != c], f'{p}: {c}.', r)


# st2 mass-energy, binding energy

c13s2_terms = term_mcq([('mass defect', 'ΔM = [Zm_p + (A − Z)m_n] − M'), ('binding energy', 'E_b = ΔMc², the energy needed to separate a nucleus into its nucleons'),
                        ('binding energy per nucleon', 'E_b/A, a measure of the stability of the nucleus'), ('energy equivalent of 1 u', '931.5 MeV'), ('Q-value of a reaction', 'Q = (initial mass − final mass)c²')],
                       'Which of the following defines {a}?', 'Which term is {b}?', '{a}: {b}.')

c13s2_tf = tf_mcq('binding energy',
                  ['The binding energy per nucleon is maximum (about 8.75 MeV) near A = 56.', 'The mass of a nucleus is less than the sum of the masses of its nucleons.', 'Both fission of heavy nuclei and fusion of light nuclei release energy.',
                   'For 30 < A < 170 the binding energy per nucleon is nearly constant.'],
                  ['The mass of a nucleus is more than the sum of its nucleons.', 'The binding energy per nucleon is largest for uranium.', 'Fusion of iron nuclei releases energy.',
                   'Binding energy per nucleon increases steadily with A.'])

c13s2_explain = pool_txt([
    ('Why do both fission of heavy nuclei and fusion of light nuclei release energy?', 'In both, products have higher binding energy per nucleon than the reactants (towards the peak near A = 56).', '2 marks.'),
    ('What does the nearly constant value of BE/A for medium nuclei tell us about nuclear forces?', 'Nuclear forces are short-ranged and saturate: each nucleon interacts only with its near neighbours.', '2 marks.'),
])

c13s2_ar = pool_ar([
    ('Iron (A = 56) is one of the most stable nuclei.', 'It has nearly the highest binding energy per nucleon.', 'a', 'R explains A.'),
    ('Energy is released when a uranium nucleus undergoes fission.', 'The fission fragments have higher binding energy per nucleon.', 'a', 'R explains A.'),
    ('The mass of a nucleus is more than the total mass of its nucleons.', 'Energy is needed to separate a nucleus into its nucleons.', 'd', 'A is false: it is less; R is true.'),
])

MH, MNU = 1.007825, 1.008665
NUCM = [('⁴He', 2, 4, 4.002603), ('¹²C', 6, 12, 12.000000), ('¹⁶O', 8, 16, 15.994915), ('⁵⁶Fe', 26, 56, 55.934939), ('²⁰Ne', 10, 20, 19.992440), ('⁷Li', 3, 7, 7.016004), ('²⁰⁹Bi', 83, 209, 208.980388)]


def c13s2_E(r):
    m = r.choice([1, 2, 0.5, 10]) * r.choice([1e-3, 1e-6])
    E = m * C * C
    return NUM(f'How much energy is equivalent to a mass of {g(m * 1000)} g?', E, 'J', f'E = mc² = {g(m)} × (3 × 10⁸)² = {{ans}}.', wrongs=[m * C, m * 1000 * C * C, E / 2], gap='G3')


def c13s2_BE(r):
    s, Z, A, M = r.choice(NUCM)
    dM = Z * MH + (A - Z) * MNU - M
    Eb = dM * U_MEV
    return NUM2(f'Find the mass defect and the binding energy of the {s} nucleus. (Atomic mass of {s} = {M} u, m(¹H) = 1.007825 u, m_n = 1.008665 u, 1 u = 931.5 MeV/c²)', (dM, Eb), ('u', 'MeV'),
                f'ΔM = Z m(¹H) + (A − Z)m_n − M = {Z} × 1.007825 + {A - Z} × 1.008665 − {M} = {sig(dM, 4)} u (1.5); E_b = ΔM × 931.5 = {sig(Eb, 4)} MeV (1.5).',
                wrongs=[(dM, Eb / A), (dM * 2, Eb * 2), (dM, dM * 931.5 * A)], n=4)


def c13s2_bpn(r):
    s, Z, A, M = r.choice(NUCM)
    Eb = (Z * MH + (A - Z) * MNU - M) * U_MEV
    return NUM(f'Find the binding energy per nucleon of {s}. (M = {M} u, m(¹H) = 1.007825 u, m_n = 1.008665 u, 1 u = 931.5 MeV/c²)', Eb / A, 'MeV',
               f'E_b = [Z m(¹H) + (A − Z)m_n − M] × 931.5 = {sig(Eb, 4)} MeV (2); E_b/A = {sig(Eb, 4)}/{A} = {{ans}} (1).', wrongs=[Eb, Eb / Z, Eb / (A - Z)], n=4)


REACT = [('²H + ²H → ³He + n', [2.014102, 2.014102], [3.016029, 1.008665]), ('²H + ³H → ⁴He + n', [2.014102, 3.016049], [4.002603, 1.008665]),
         ('⁷Li + ¹H → 2 ⁴He', [7.016004, 1.007825], [4.002603, 4.002603]), ('²H + ²H → ³H + ¹H', [2.014102, 2.014102], [3.016049, 1.007825])]


def c13s2_Q(r):
    eq, ins, outs = r.choice(REACT)
    Q = (sum(ins) - sum(outs)) * U_MEV
    return NUM(f'Find the Q-value of the reaction {eq}. Atomic masses: ' + ', '.join(f'{m} u' for m in ins + outs) + ' (in the order the particles appear). Is energy released? (1 u = 931.5 MeV/c²)', Q, 'MeV',
               f'Δm = Σm(initial) − Σm(final) = {sig(sum(ins), 7)} − {sig(sum(outs), 7)} = {sig(sum(ins) - sum(outs), 3)} u (2); Q = Δm × 931.5 = {{ans}} (1); positive, so energy is released (1).',
               wrongs=[-Q, Q / 2, Q * 2], n=3, gap='G5')


c13s2_curve = pool_mcq([
    ('The binding energy per nucleon is maximum for nuclei with mass number about', '56', ['4', '120', '238'], 'Peak near iron.'),
    ('The binding energy per nucleon of very light nuclei (A < 10) is', 'smaller than that of medium nuclei', ['larger than that of medium nuclei', 'zero', 'equal to that of iron'], 'Curve rises steeply for small A.'),
    ('Energy is released when two light nuclei fuse because', 'the product has a larger binding energy per nucleon', ['the product has a smaller binding energy per nucleon', 'mass is created', 'protons repel'], 'Moving up the BE curve.'),
    ('A heavy nucleus of BE/A ≈ 7.6 MeV splits into two nuclei of BE/A ≈ 8.5 MeV. The energy released per nucleon is about', '0.9 MeV', ['8.5 MeV', '7.6 MeV', '16.1 MeV'], '8.5 − 7.6 = 0.9 MeV.'),
])

c13s2_long = pool_txt([
    ('Draw the curve of binding energy per nucleon against mass number and explain how it accounts for energy release in fission and fusion.', 'BE/A rises quickly, peaks ~8.75 MeV at A ≈ 56, falls slowly to ~7.6 MeV at A = 238',
     'Curve (2); fusion of light nuclei moves up the curve (1.5); fission of heavy nuclei moves up the curve (1.5).'),
    ('Explain mass defect and binding energy, and show how to calculate the binding energy of a nucleus.', 'E_b = [Zm_p + (A − Z)m_n − M]c²', 'Definitions (2); formula (1); 931.5 MeV/u conversion and example (2).'),
])


def c13s2_case(r):
    a1, b1 = r.choice([(240, 7.6), (236, 7.6)])
    b2 = r.choice([8.4, 8.5])
    return {'stem': (f'In a nuclear reactor, a nucleus of mass number {a1} (BE per nucleon ≈ {b1} MeV) splits into two fragments of mass number about {a1 // 2} each (BE per nucleon ≈ {b2} MeV).\n'
                     '(i) Find the total binding energy of the original nucleus. (ii) Find the total binding energy of the two fragments. (iii) Find the energy released. (iv) Why is this energy released?'),
            'answer': f'(i) {sig(a1 * b1)} MeV (ii) {sig(a1 * b2)} MeV (iii) {sig(a1 * (b2 - b1))} MeV (iv) the fragments are more tightly bound (higher BE per nucleon)',
            'key': '(i) A × BE/A (1). (ii) (1). (iii) difference (1). (iv) BE curve (1).'}


# st3 nuclear force; fission and fusion

c13s3_terms = term_mcq([('nuclear force', 'a strong, short-range attractive force between nucleons, nearly independent of charge'), ('nuclear fission', 'splitting of a heavy nucleus into two lighter nuclei with release of energy'),
                        ('nuclear fusion', 'joining of light nuclei into a heavier nucleus with release of energy'), ('chain reaction', 'a self-sustaining series of fissions caused by neutrons from earlier fissions'),
                        ('moderator', 'a material such as heavy water or graphite that slows down neutrons in a reactor')],
                       'Which of the following describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c13s3_tf = tf_mcq('nuclear forces, fission and fusion',
                  ['Nuclear force is much stronger than the Coulomb force at short range.', 'Nuclear force is nearly the same between n-n, n-p and p-p.', 'Fusion needs very high temperatures.',
                   'The Sun\'s energy comes from fusion of hydrogen into helium.', 'Control rods (e.g. cadmium) absorb neutrons.'],
                  ['Nuclear force acts over large distances like gravity.', 'Nuclear force is purely attractive at all separations.', 'Fusion occurs easily at room temperature.',
                   'The Sun\'s energy comes from fission of uranium.', 'Moderators speed up neutrons.'])

c13s3_explain = pool_txt([
    ('Why is a very high temperature needed for nuclear fusion?', 'Nuclei must have enough kinetic energy to overcome Coulomb repulsion and come within range of the nuclear force.', '2 marks.'),
    ('What is the role of the moderator and control rods in a nuclear reactor?', 'Moderator slows neutrons for efficient fission; control rods absorb neutrons to control the rate.', '2 marks.'),
    ('State two characteristic properties of the nuclear force.', 'Short range (~fm), very strong, charge independent, repulsive below ~0.8 fm, saturating.', '2 marks.'),
])

c13s3_ar = pool_ar([
    ('Fusion requires extremely high temperatures.', 'Positively charged nuclei repel each other.', 'a', 'R explains A.'),
    ('Heavy water is used as a moderator in some reactors.', 'Heavy water slows down neutrons without absorbing many of them.', 'a', 'R explains A.'),
    ('The nuclear force between two protons is much weaker than the Coulomb force between them at 1 fm.', 'The nuclear force is charge independent.', 'd', 'A is false; R is true.'),
])


def c13s3_fission(r):
    m = r.choice([1, 2, 0.5, 5])
    Ef = 200
    N = m * 1000 / 235 * 6.02e23
    E = N * Ef * 1.6e-13
    return NUM(f'Each fission of ²³⁵U releases about {Ef} MeV. Find the energy released by the complete fission of {g(m)} kg of ²³⁵U. (N_A = 6.02 × 10²³ mol⁻¹)', E, 'J',
               f'Number of nuclei N = ({g(m * 1000)}/235) × 6.02 × 10²³ = {sig(N)} (1); E = N × {Ef} × 1.6 × 10⁻¹³ J (1) = {{ans}} (1).', wrongs=[N * Ef, E / 1000, E * 235], gap='G5')


def c13s3_rate(r):
    P = r.choice([100, 200, 500, 1000])
    eff = r.choice([1, 0.25, 0.3])
    n = P * 1e6 / eff / (200 * 1.6e-13)
    t = f' at {int(eff * 100)}% efficiency' if eff < 1 else ''
    return NUM(f'A nuclear power plant produces {P} MW of electrical power{t}. If each fission releases 200 MeV, how many fissions occur per second?', n, 's⁻¹',
               f'Energy per fission = 200 × 1.6 × 10⁻¹³ = 3.2 × 10⁻¹¹ J (1); thermal power = {g(P / eff)} MW (1); fissions per second = P/E = {{ans}} (2).', wrongs=[P * 1e6 / (200 * 1.6e-13), n * 1000, n / 2] if eff < 1 else [n * 1000, n / 2, P / 200], gap='G5')


def c13s3_fusion(r):
    Q = r.choice([3.27, 4.03, 17.6])
    m = r.choice([1, 2])
    mol = m * 1000 / (4.028 if Q < 10 else 5.03)
    N = mol * 6.02e23
    E = N * Q * 1.6e-13
    eq = '²H + ²H fusion' if Q < 10 else '²H + ³H fusion'
    return NUM(f'Each {eq} reaction releases {g(Q)} MeV. Estimate the energy released when {m} kg of fuel (equal moles of the reacting nuclei, molar mass of one reacting pair ≈ {"4.03" if Q < 10 else "5.03"} g) reacts completely.', E, 'J',
               f'Number of reactions = ({m * 1000}/{"4.03" if Q < 10 else "5.03"}) × 6.02 × 10²³ = {sig(N)} (1); E = N × {g(Q)} × 1.6 × 10⁻¹³ J = {{ans}} (2).', wrongs=[E / 1000, E * 2, N * Q], gap='G5')


c13s3_mcq = pool_mcq([
    ('In a nuclear reactor, cadmium rods are used to', 'absorb neutrons and control the chain reaction', ['slow down neutrons', 'produce neutrons', 'cool the reactor'], 'Cadmium has a high neutron absorption cross-section.'),
    ('The source of the Sun\'s energy is', 'fusion of hydrogen into helium', ['fission of uranium', 'chemical burning', 'radioactive decay of radium'], 'Proton-proton cycle.'),
    ('A typical fission of ²³⁵U releases about', '200 MeV', ['2 MeV', '20 eV', '2000 MeV'], '≈ 0.9 MeV per nucleon × 235.'),
    ('The nuclear force is', 'short-ranged and charge independent', ['long-ranged like gravity', 'only between protons', 'repulsive at all distances'], 'Range ~ a few fm.'),
])


# ======================================================== ch14 Semiconductor Electronics
# st1 classification, energy bands

c14s1_terms = term_mcq([('valence band', 'the energy band occupied by valence electrons'), ('conduction band', 'the band above the valence band, where electrons are free to conduct'),
                        ('energy band gap', 'the energy gap E_g between the top of the valence band and the bottom of the conduction band'), ('metal (band picture)', 'conduction and valence bands overlap or the conduction band is partly filled'),
                        ('insulator (band picture)', 'a large band gap, E_g > 3 eV')],
                       'Which of the following describes a {a}?', 'Which term is {b}?', '{a}: {b}.')

c14s1_tf = tf_mcq('energy bands',
                  ['Diamond is an insulator with E_g ≈ 5.4 eV.', 'Silicon has a band gap of about 1.1 eV.', 'At 0 K an intrinsic semiconductor behaves as an insulator.',
                   'In metals, the valence and conduction bands overlap (or the conduction band is partly filled).'],
                  ['Silicon has a band gap of about 5 eV.', 'At 0 K a semiconductor conducts well.', 'Insulators have overlapping bands.', 'Germanium has a larger band gap than diamond.'])

c14s1_explain = pool_txt([
    ('Distinguish between metals, semiconductors and insulators on the basis of energy bands.', 'Metal: bands overlap; semiconductor: small gap (< 3 eV); insulator: large gap (> 3 eV).', '2 marks.'),
    ('Why does the conductivity of a semiconductor increase with temperature?', 'More electrons are thermally excited across the small band gap, creating electron-hole pairs.', '2 marks.'),
])

c14s1_ar = pool_ar([
    ('A semiconductor behaves as an insulator at 0 K.', 'At 0 K no electrons have enough energy to cross the band gap.', 'a', 'R explains A.'),
    ('Diamond is a good insulator.', 'The band gap of diamond is large (≈ 5.4 eV).', 'a', 'R explains A.'),
    ('The resistance of a metal decreases with rise of temperature.', 'Metals have overlapping valence and conduction bands.', 'd', 'A is false; R is true.'),
])


def c14s1_class(r):
    mat, eg = r.choice([('diamond', 5.4), ('silicon', 1.1), ('germanium', 0.7), ('a solid with overlapping bands', 0), ('glass-like solid', 6), ('gallium arsenide', 1.4)])
    c = 'metal (conductor)' if eg == 0 else 'insulator' if eg > 3 else 'semiconductor'
    t = 'with overlapping valence and conduction bands' if eg == 0 else f'with a band gap of {g(eg)} eV'
    return mcq(f'A solid {t} ({mat}) is classified as a', c, [x for x in ('metal (conductor)', 'insulator', 'semiconductor', 'superconductor') if x != c], f'E_g = 0 metal; < 3 eV semiconductor; > 3 eV insulator.', r)


def c14s1_lam(r):
    mat, eg = r.choice([('silicon', 1.1), ('germanium', 0.7), ('gallium arsenide', 1.4), ('a semiconductor', 2.0), ('a semiconductor', 2.8)])
    lam = 1240 / eg
    return NUM(f'What is the maximum wavelength of light that can create electron-hole pairs in {mat} (band gap {g(eg)} eV)? (hc = 1240 eV nm)', lam, 'nm', f'hc/λ ≥ E_g ⇒ λ_max = 1240/{g(eg)} = {{ans}}.',
               wrongs=[1240 * eg, lam / 2, eg / 1240 * 1e6], gap='G3')


def c14s1_detect(r):
    mat, eg = r.choice([('silicon', 1.1), ('germanium', 0.7), ('gallium arsenide', 1.4), ('cadmium sulphide', 2.4), ('a wide-gap semiconductor', 3.0)])
    lam = r.choice([450, 550, 650, 900, 1300, 1600])
    E = 1240 / lam
    yes = E >= eg
    return mcq(f'Can a photodetector made of {mat} (band gap {g(eg)} eV) detect light of wavelength {lam} nm? (hc = 1240 eV nm)',
               f'{"Yes" if yes else "No"}: photon energy {sig(E)} eV is {"more" if yes else "less"} than {g(eg)} eV',
               [f'{"No" if yes else "Yes"}: photon energy {sig(E)} eV is {"less" if yes else "more"} than {g(eg)} eV', 'Yes, any wavelength can be detected if the light is intense',
                f'No, because the band gap must equal exactly {sig(E)} eV'], f'Electron-hole pairs need hν ≥ E_g; hν = 1240/{lam} = {sig(E)} eV.', r)


def c14s1_led(r):
    lam, col = r.choice([(620, 'red'), (590, 'yellow'), (530, 'green'), (470, 'blue'), (850, 'infrared')])
    return NUM(f'An LED is required to emit {col} light of wavelength about {lam} nm. Estimate the band gap of the semiconductor needed. (hc = 1240 eV nm)', 1240 / lam, 'eV',
               f'E_g ≈ hc/λ (2) = 1240/{lam} = {{ans}} (1).', wrongs=[lam / 1240, 1240 / lam / 2, 1240 / lam + 1], gap='G5')


c14s1_mcq = pool_mcq([
    ('The band gap of silicon is about', '1.1 eV', ['0.01 eV', '5.4 eV', '10 eV'], 'Si: 1.1 eV; Ge: 0.7 eV.'),
    ('In an insulator, the forbidden energy gap is', 'more than about 3 eV', ['zero', 'less than 0.1 eV', 'negative'], 'Large gap.'),
    ('At absolute zero, a pure semiconductor is', 'an insulator', ['a good conductor', 'a superconductor', 'a metal'], 'Conduction band empty.'),
])


# st2 intrinsic and extrinsic

c14s2_terms = term_mcq([('intrinsic semiconductor', 'a pure semiconductor with n_e = n_h = n_i'), ('n-type semiconductor', 'doped with a pentavalent impurity such as As; electrons are majority carriers'),
                        ('p-type semiconductor', 'doped with a trivalent impurity such as B; holes are majority carriers'), ('donor impurity', 'a pentavalent atom that gives an extra electron'),
                        ('acceptor impurity', 'a trivalent atom that creates a hole'), ('mass action law', 'n_e n_h = n_i²')],
                       'Which of the following describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c14s2_tf = tf_mcq('extrinsic semiconductors',
                  ['An n-type semiconductor is electrically neutral.', 'In p-type silicon, holes are the majority carriers.', 'Doping increases the conductivity of a semiconductor greatly.',
                   'In equilibrium n_e n_h = n_i².'],
                  ['An n-type semiconductor carries a net negative charge.', 'Phosphorus is an acceptor impurity in silicon.', 'Doping reduces the number of charge carriers.',
                   'In n-type material holes are the majority carriers.'])

c14s2_explain = pool_txt([
    ('Why is an n-type semiconductor electrically neutral even though it has extra electrons?', 'Each donor atom that gives an electron becomes a positive ion; total charge stays zero.', '2 marks.'),
    ('How does doping with boron make silicon p-type?', 'Trivalent B forms three bonds; the missing fourth bond is a hole that can accept an electron.', '2 marks.'),
])

c14s2_ar = pool_ar([
    ('An n-type semiconductor is electrically neutral.', 'Donor atoms become positive ions after giving away electrons.', 'a', 'R explains A.'),
    ('Holes are the majority carriers in a p-type semiconductor.', 'Trivalent impurity atoms create holes.', 'a', 'R explains A.'),
    ('Doping a semiconductor with phosphorus makes it p-type.', 'Phosphorus is pentavalent.', 'd', 'A is false: it becomes n-type; R is true.'),
])

DOP = [('arsenic', 'n-type'), ('phosphorus', 'n-type'), ('antimony', 'n-type'), ('boron', 'p-type'), ('aluminium', 'p-type'), ('indium', 'p-type'), ('gallium', 'p-type')]


def c14s2_type(r):
    d, t = r.choice(DOP)
    return mcq(f'Pure silicon is doped with a small amount of {d}. The result is', f'an {t} semiconductor' if t[0] == 'n' else f'a {t} semiconductor',
               [f'a p-type semiconductor' if t[0] == 'n' else 'an n-type semiconductor', 'an intrinsic semiconductor', 'an insulator'],
               f'{d.capitalize()} is {"pentavalent (donor)" if t[0] == "n" else "trivalent (acceptor)"}, giving {t}.', r)


def c14s2_n(r):
    ni = r.choice([1.5e16, 1e16, 2.4e19])
    ND = r.choice([1e21, 5e21, 1e22, 5e22]) if ni < 1e19 else r.choice([1e22, 5e22])
    nh = ni * ni / ND
    return NUM2(f'A pure semiconductor has n_i = {g(ni)} m⁻³. It is doped with {g(ND)} donor atoms per m³. Find the electron and hole concentrations, assuming each donor gives one electron.', (ND, nh), ('m⁻³', 'm⁻³'),
                f'n_e ≈ N_D = {sig(ND)} m⁻³ (1); n_h = n_i²/n_e = {sig(nh)} m⁻³ (2).', wrongs=[(ni, ni), (ND, ni), (nh, ND)])


def c14s2_major(r):
    na = r.choice([5e22, 1e23, 5e28])
    Nsi = 5e28
    ppm = r.choice([1, 2, 5, 10])
    N = Nsi * ppm * 1e-6
    d, t = r.choice(DOP)
    return NUM(f'Silicon has about 5 × 10²⁸ atoms per m³. It is doped with {d} at {ppm} part{"s" if ppm > 1 else ""} per million. Find the concentration of majority carriers. Which are they?', N, 'm⁻³',
               f'N = 5 × 10²⁸ × {ppm} × 10⁻⁶ = {{ans}} (2); {d} is {"a donor: electrons" if t[0] == "n" else "an acceptor: holes"} are the majority carriers (1).', wrongs=[Nsi, N * 1e6, N / 10], gap='G5')


# st3 p-n junction

c14s3_terms = term_mcq([('depletion region', 'the region near a junction that has lost its free charge carriers and contains immobile ions'), ('barrier potential', 'the potential difference across the depletion layer that opposes diffusion'),
                        ('forward bias', 'p-side connected to the positive terminal; barrier reduced, large current'), ('reverse bias', 'p-side connected to the negative terminal; barrier increased, tiny current'),
                        ('reverse breakdown', 'sudden large increase of reverse current at a critical reverse voltage')],
                       'Which of the following describes {a}?', 'Which term is {b}?', '{a}: {b}.')

c14s3_tf = tf_mcq('the p-n junction diode',
                  ['The depletion region widens under reverse bias.', 'Diffusion current flows from p to n (holes) when the junction forms.', 'In forward bias the current rises rapidly after the knee voltage.',
                   'The reverse current is due to minority carriers and is nearly independent of voltage (before breakdown).', 'The barrier potential of silicon is about 0.7 V.'],
                  ['The depletion region widens under forward bias.', 'A diode conducts equally in both directions.', 'The reverse current is due to majority carriers.',
                   'The barrier potential of silicon is about 7 V.', 'The depletion region contains many free electrons.'])

c14s3_explain = pool_txt([
    ('Explain how the depletion region and barrier potential are formed in a p-n junction.', 'Electrons diffuse n → p and holes p → n, leaving immobile ions; their field opposes further diffusion and sets up a barrier.', '2 marks.'),
    ('Draw and explain the I-V characteristics of a p-n junction diode.', 'Forward: tiny current up to the knee (~0.7 V for Si) then rapid rise. Reverse: tiny, nearly constant current until breakdown.', '2 marks.'),
    ('Why does the width of the depletion layer change with bias?', 'Forward bias opposes the barrier field and narrows it; reverse bias adds to it and widens it.', '2 marks.'),
])

c14s3_ar = pool_ar([
    ('A p-n junction diode conducts in forward bias.', 'Forward bias lowers the potential barrier.', 'a', 'R explains A.'),
    ('The reverse current of a diode is very small.', 'It is due to minority carriers.', 'a', 'R explains A.'),
    ('The depletion layer contains a large number of free charge carriers.', 'The depletion layer contains immobile ions.', 'd', 'A is false; R is true.'),
])


def c14s3_R(r):
    V1 = r.choice([0.6, 0.65, 0.7])
    dV = r.choice([0.05, 0.1])
    I1 = r.choice([5, 10, 15])
    dI = r.choice([10, 20, 25])
    Rd = dV / (dI * 1e-3)
    return NUM(f'From the forward characteristic of a diode, the current rises from {I1} mA to {I1 + dI} mA when the voltage rises from {g(V1)} V to {g(V1 + dV)} V. Find the dynamic resistance in this range.', Rd, 'Ω',
               f'r_d = ΔV/ΔI = {g(dV)}/({dI} × 10⁻³) = {{ans}}.', wrongs=[V1 / (I1 * 1e-3), dV / dI, (V1 + dV) / ((I1 + dI) * 1e-3)])


def c14s3_ckt(r):
    V = r.choice([3, 5, 6, 9, 12])
    R = r.choice([100, 200, 220, 470, 1000])
    I = (V - 0.7) / R
    return NUM(f'A silicon diode (barrier/knee voltage 0.7 V, negligible resistance after that) is connected in forward bias in series with a {R} Ω resistor across a {V} V battery. Find the current.', I * 1000, 'mA',
               f'I = (V − 0.7)/R = ({V} − 0.7)/{R} = {{ans}}.', wrongs=[V / R * 1000, (V + 0.7) / R * 1000, I], n=3)


def c14s3_bias(r):
    vp, vn = r.choice([(5, 0), (0, -3), (-2, 0), (0, 5), (3, 1), (-5, -1), (1, 3), (-1, -4)])
    fwd = vp > vn
    ans = 'forward biased' if fwd else 'reverse biased'
    return mcq(f'In a p-n junction diode, the p-side is at {num(vp, 0)} V and the n-side is at {num(vn, 0)} V. The diode is', ans,
               ['reverse biased' if fwd else 'forward biased', 'unbiased', 'broken down'], f'p-side at {"higher" if fwd else "lower"} potential than n-side: {ans}.', r)


def c14s3_field(r):
    V0 = r.choice([0.3, 0.6, 0.7])
    d = r.choice([0.5, 1, 2])
    E_ = V0 / (d * 1e-6)
    return NUM(f'The barrier potential of a p-n junction is {g(V0)} V and the width of the depletion region is {g(d)} μm. Estimate the electric field in the depletion region (assume it is uniform).', E_, 'V m⁻¹',
               f'E = V₀/d = {g(V0)}/({g(d)} × 10⁻⁶) = {{ans}}.', wrongs=[V0 * d * 1e-6, V0 / d, E_ / 1000])


def c14s3_two(r):
    V = r.choice([5, 6, 9, 12])
    R = r.choice([100, 200, 500])
    rev = r.random() < 0.5
    I = 0.0 if rev else (V - 0.7) / R
    if rev:
        return {'stem': f'Two identical silicon diodes D₁ and D₂ (knee voltage 0.7 V) are connected in series, back to back (n-side of D₁ to n-side of D₂), with a {R} Ω resistor across a {V} V battery. Find the current.', 'answer': '≈ 0 A',
                'key': 'Whatever the polarity, one of the two diodes is reverse biased (3); so only a negligible reverse current flows (2).', 'distractors': [f'{sig((V - 0.7) / R * 1000)} mA', f'{sig((V - 1.4) / R * 1000)} mA', f'{sig(V / R * 1000)} mA']}
    return NUM(f'Two identical silicon diodes D₁ and D₂ (knee voltage 0.7 V) are connected in parallel, both in forward bias, and the combination is connected in series with a {R} Ω resistor across a {V} V battery. Find the total current and the current through each diode.', I * 1000, 'mA',
               f'Voltage across the parallel diodes = 0.7 V (2); I = ({V} − 0.7)/{R} = {{ans}} (2), shared equally: {sig(I * 500)} mA each (1).', wrongs=[(V - 1.4) / R * 1000, V / R * 1000, I * 500], gap='G5')


c14s3_derive = pool_txt([
    ('Explain with a diagram the formation of the depletion layer and barrier potential in a p-n junction, and how they change in forward and reverse bias.', 'Diffusion leaves immobile ions; barrier V₀; forward bias narrows, reverse bias widens',
     'Diffusion and drift (2); depletion and V₀ (1); forward (1); reverse (1).'),
    ('With a circuit diagram, describe how the forward and reverse I-V characteristics of a diode are obtained, and draw them.', 'Forward: knee ~0.7 V then steep rise; reverse: μA current until breakdown',
     'Circuits (2); forward curve (1.5); reverse curve (1.5).'),
])


def c14s3_case(r):
    who = name(r)
    V = r.choice([0.6, 0.7, 0.75, 0.8])
    I = r.choice([10, 20, 30])
    return {'stem': (f'{who} plots the I-V characteristic of a silicon diode. In forward bias the current is almost zero up to about 0.6 V and then rises steeply; at {g(V)} V it is {I} mA. In reverse bias the current is a few μA until −50 V, when it suddenly rises.\n'
                     '(i) What is the knee voltage? (ii) Find the static resistance at the reading given. (iii) What causes the small reverse current? (iv) What is the sudden rise at −50 V called?'),
            'answer': f'(i) about 0.6-0.7 V (ii) {sig(V / (I * 1e-3))} Ω (iii) minority carriers (iv) reverse breakdown',
            'key': '(i) (1). (ii) R = V/I (1). (iii) (1). (iv) (1).'}


# st4 rectifiers

c14s4_terms = term_mcq([('rectifier', 'a circuit that converts AC into unidirectional (pulsating DC) voltage'), ('half-wave rectifier', 'conducts during only one half of each AC cycle'),
                        ('full-wave rectifier', 'conducts during both halves of the cycle, using two diodes and a centre-tap transformer'), ('filter capacitor', 'a capacitor across the load that smooths the ripple')],
                       'Which of the following describes a {a}?', 'Which term is {b}?', '{a}: {b}.')

c14s4_tf = tf_mcq('rectifiers',
                  ['A half-wave rectifier gives output only in alternate half-cycles.', 'The ripple frequency of a full-wave rectifier on 50 Hz mains is 100 Hz.', 'A capacitor filter smooths the rectified output.',
                   'A centre-tap full-wave rectifier uses two diodes.'],
                  ['The ripple frequency of a half-wave rectifier on 50 Hz mains is 100 Hz.', 'A full-wave rectifier uses only one diode.', 'A rectifier converts DC into AC.',
                   'The filter capacitor is connected in series with the load.'])

c14s4_explain = pool_txt([
    ('Why is a full-wave rectifier preferred to a half-wave rectifier?', 'It uses both halves of the cycle: higher average output, higher efficiency, ripple at twice the frequency (easier to filter).', '2 marks.'),
    ('How does a capacitor filter reduce ripple in a rectifier output?', 'It charges to the peak voltage and discharges slowly through the load between peaks, keeping the voltage nearly constant.', '2 marks.'),
])

c14s4_ar = pool_ar([
    ('The output frequency of a full-wave rectifier is twice the input frequency.', 'Both halves of each input cycle give an output pulse in the same direction.', 'a', 'R explains A.'),
    ('A diode can be used as a rectifier.', 'A diode conducts mainly in one direction.', 'a', 'R explains A.'),
    ('A half-wave rectifier uses both halves of the AC cycle.', 'A diode conducts only in forward bias.', 'd', 'A is false; R is true.'),
])


def c14s4_freq(r):
    f = r.choice([50, 60])
    full = r.random() < 0.5
    return NUM(f'The input to a {"full" if full else "half"}-wave rectifier is a {f} Hz AC voltage. What is the frequency of the output ripple?', 2 * f if full else f, 'Hz',
               f'{"Both half-cycles give pulses, so the ripple frequency is 2ν" if full else "One pulse per cycle, so the ripple frequency equals ν"} = {{ans}}.', wrongs=[f if full else 2 * f, f / 2, 4 * f], gap='G3', n=3)


def c14s4_peak(r):
    Vr = r.choice([6, 9, 12, 15, 24])
    Vp = Vr * math.sqrt(2)
    drop = r.random() < 0.5
    out = Vp - 0.7 if drop else Vp
    return NUM(f'The secondary of a transformer gives {Vr} V rms to a half-wave rectifier. Find the peak output voltage across the load{" if the diode drop is 0.7 V" if drop else " (ideal diode)"}.', out, 'V',
               f'V₀ = √2 × V_rms = {sig(Vp)} V{"; minus 0.7 V diode drop" if drop else ""} = {{ans}}.', wrongs=[float(Vr), Vr / math.sqrt(2), Vp + 0.7 if drop else Vp - 0.7])


c14s4_mcq = pool_mcq([
    ('A centre-tap full-wave rectifier uses', 'two diodes', ['one diode', 'three diodes', 'no diodes'], 'One diode per half of the secondary.'),
    ('In a half-wave rectifier, the diode conducts during', 'half of each input cycle', ['the whole input cycle', 'no part of the cycle', 'a quarter of each cycle'], 'Only when forward biased.'),
    ('To reduce ripple in the output of a rectifier, one connects', 'a capacitor in parallel with the load', ['a capacitor in series with the load', 'a resistor in parallel with the diode', 'a second transformer'], 'Capacitor filter.'),
])

c14s4_long = pool_txt([
    ('With a circuit diagram, explain the working of a full-wave rectifier using a centre-tap transformer. Draw the input and output waveforms.', 'Two diodes conduct alternately; output pulses in the same direction for both half-cycles',
     'Circuit (2); working in each half (2); waveforms (1).'),
    ('With a circuit diagram, explain the working of a half-wave rectifier and draw its input and output waveforms.', 'The diode conducts only in the positive half-cycles', 'Circuit (2); working (2); waveforms (1).'),
])


def c14s4_case(r):
    who = name(r)
    Vr = r.choice([9, 12, 15])
    return {'stem': (f'{who} builds a 50 Hz mains adapter: a step-down transformer gives {Vr} V rms, followed by a centre-tap full-wave rectifier and a filter capacitor.\n'
                     '(i) How many diodes are needed? (ii) What is the ripple frequency? (iii) What is the peak voltage across the load (ideal diodes)? (iv) What does the capacitor do?'),
            'answer': f'(i) two (ii) 100 Hz (iii) {sig(Vr * math.sqrt(2))} V (iv) smooths the output by charging to the peak and discharging slowly through the load',
            'key': '(i) (1). (ii) 2ν (1). (iii) √2 V_rms of each half-secondary (1). (iv) filter (1).'}


# ======================================================== families

FAMILIES = {
    S + '11-st1': [F('C1', 'D1', 'mcq', c11s1_terms), F('C1', 'D2', 'mcq', c11s1_tf), F('C2', 'D2', 'explain', c11s1_explain), F('C2', 'D3', 'mcq', c11s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c11s1_eV), F('C3', 'D2', 'numerical', c11s1_thr), F('C3', 'D3', 'numerical', c11s1_V0), F('C4', 'D3', 'mcq', c11s1_graph), F('C3', 'D3', 'case', c11s1_case)],
    S + '11-st2': [F('C1', 'D1', 'mcq', c11s2_terms), F('C1', 'D2', 'mcq', c11s2_tf), F('C2', 'D2', 'explain', c11s2_explain), F('C2', 'D3', 'mcq', c11s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c11s2_derive), F('C3', 'D1', 'short', c11s2_p), F('C3', 'D2', 'numerical', c11s2_E), F('C3', 'D2', 'numerical', c11s2_K),
                   F('C3', 'D3', 'numerical', c11s2_V0), F('C4', 'D3', 'mcq', c11s2_will), F('C4', 'D4', 'multi_step', c11s2_rate), F('C4', 'D5', 'long', c11s2_hphi)],
    S + '11-st3': [F('C1', 'D1', 'mcq', c11s3_terms), F('C1', 'D2', 'mcq', c11s3_tf), F('C2', 'D2', 'explain', c11s3_explain), F('C2', 'D3', 'mcq', c11s3_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c11s3_V), F('C3', 'D2', 'numerical', c11s3_mv), F('C3', 'D3', 'numerical', c11s3_K), F('C4', 'D3', 'numerical', c11s3_ratio),
                   F('C4', 'D4', 'long', c11s3_same)],
    S + '12-st1': [F('C1', 'D1', 'mcq', c12s1_terms), F('C1', 'D2', 'mcq', c12s1_tf), F('C1', 'D1', 'mcq', c12s1_mcq), F('C2', 'D2', 'explain', c12s1_explain), F('C2', 'D3', 'mcq', c12s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c12s1_factor), F('C3', 'D3', 'numerical', c12s1_closest), F('C4', 'D4', 'multi_step', c12s1_need)],
    S + '12-st2': [F('C1', 'D1', 'mcq', c12s2_terms), F('C1', 'D2', 'mcq', c12s2_tf), F('C2', 'D2', 'explain', c12s2_explain), F('C2', 'D3', 'mcq', c12s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c12s2_derive), F('C3', 'D1', 'short', c12s2_r), F('C3', 'D2', 'numerical', c12s2_E), F('C3', 'D2', 'numerical', c12s2_ion),
                   F('C3', 'D3', 'numerical', c12s2_jump), F('C4', 'D3', 'numerical', c12s2_KEPE), F('C4', 'D4', 'multi_step', c12s2_v), F('C3', 'D3', 'case', c12s2_case)],
    S + '12-st3': [F('C1', 'D1', 'mcq', c12s3_terms), F('C1', 'D2', 'mcq', c12s3_tf), F('C2', 'D2', 'explain', c12s3_explain), F('C2', 'D3', 'mcq', c12s3_ar, kinds=('ar',)),
                   F('C3', 'D1', 'mcq', c12s3_which), F('C3', 'D2', 'short', c12s3_lines), F('C3', 'D3', 'numerical', c12s3_lam), F('C4', 'D3', 'numerical', c12s3_limit),
                   F('C4', 'D4', 'multi_step', c12s3_ratio), F('C4', 'D3', 'numerical', c12s3_deB)],
    S + '13-st1': [F('C1', 'D1', 'mcq', c13s1_terms), F('C1', 'D2', 'mcq', c13s1_tf), F('C2', 'D2', 'explain', c13s1_explain), F('C2', 'D3', 'mcq', c13s1_ar, kinds=('ar',)),
                   F('C3', 'D1', 'short', c13s1_count), F('C3', 'D2', 'numerical', c13s1_R), F('C3', 'D3', 'numerical', c13s1_avg), F('C4', 'D3', 'numerical', c13s1_ratio),
                   F('C4', 'D3', 'mcq', c13s1_class), F('C4', 'D4', 'multi_step', c13s1_density)],
    S + '13-st2': [F('C1', 'D1', 'mcq', c13s2_terms), F('C1', 'D2', 'mcq', c13s2_tf), F('C2', 'D2', 'explain', c13s2_explain), F('C2', 'D3', 'mcq', c13s2_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c13s2_long), F('C3', 'D1', 'short', c13s2_E), F('C3', 'D2', 'numerical', c13s2_BE), F('C3', 'D3', 'numerical', c13s2_bpn),
                   F('C4', 'D3', 'mcq', c13s2_curve), F('C4', 'D4', 'long', c13s2_Q), F('C3', 'D3', 'case', c13s2_case)],
    S + '13-st3': [F('C1', 'D1', 'mcq', c13s3_terms), F('C1', 'D2', 'mcq', c13s3_tf), F('C1', 'D1', 'mcq', c13s3_mcq), F('C2', 'D2', 'explain', c13s3_explain), F('C2', 'D3', 'mcq', c13s3_ar, kinds=('ar',)),
                   F('C3', 'D3', 'numerical', c13s3_fission), F('C4', 'D4', 'multi_step', c13s3_rate), F('C4', 'D5', 'multi_step', c13s3_fusion)],
    S + '14-st1': [F('C1', 'D1', 'mcq', c14s1_terms), F('C1', 'D2', 'mcq', c14s1_tf), F('C1', 'D1', 'mcq', c14s1_mcq), F('C2', 'D2', 'explain', c14s1_explain), F('C2', 'D3', 'mcq', c14s1_ar, kinds=('ar',)),
                   F('C3', 'D2', 'mcq', c14s1_class), F('C3', 'D3', 'numerical', c14s1_lam), F('C4', 'D3', 'mcq', c14s1_detect), F('C4', 'D3', 'numerical', c14s1_led)],
    S + '14-st2': [F('C1', 'D1', 'mcq', c14s2_terms), F('C1', 'D2', 'mcq', c14s2_tf), F('C2', 'D2', 'explain', c14s2_explain), F('C2', 'D3', 'mcq', c14s2_ar, kinds=('ar',)),
                   F('C3', 'D1', 'mcq', c14s2_type), F('C3', 'D3', 'numerical', c14s2_n), F('C4', 'D4', 'multi_step', c14s2_major)],
    S + '14-st3': [F('C1', 'D1', 'mcq', c14s3_terms), F('C1', 'D2', 'mcq', c14s3_tf), F('C2', 'D2', 'explain', c14s3_explain), F('C2', 'D3', 'mcq', c14s3_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c14s3_derive), F('C3', 'D1', 'mcq', c14s3_bias), F('C3', 'D2', 'numerical', c14s3_R), F('C3', 'D3', 'numerical', c14s3_ckt),
                   F('C4', 'D3', 'numerical', c14s3_field), F('C4', 'D4', 'long', c14s3_two), F('C3', 'D3', 'case', c14s3_case)],
    S + '14-st4': [F('C1', 'D1', 'mcq', c14s4_terms), F('C1', 'D2', 'mcq', c14s4_tf), F('C2', 'D2', 'explain', c14s4_explain), F('C2', 'D3', 'mcq', c14s4_ar, kinds=('ar',)),
                   F('C2', 'D3', 'long', c14s4_long), F('C3', 'D1', 'short', c14s4_freq), F('C3', 'D2', 'numerical', c14s4_peak), F('C3', 'D2', 'mcq', c14s4_mcq), F('C4', 'D3', 'case', c14s4_case)],
}

FAMILIES = polish(FAMILIES)
