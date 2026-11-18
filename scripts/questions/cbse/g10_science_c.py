"""CBSE class 10 science families, chapters 9-13 (Light – Reflection and Refraction; The Human Eye
and the Colourful World; Electricity; Magnetic Effects of Electric Current; Our Environment).
New Cartesian sign convention throughout: distances measured from the pole/optical centre,
along the incident light positive. Mirror: 1/v + 1/u = 1/f, m = −v/u. Lens: 1/v − 1/u = 1/f, m = v/u."""
from __future__ import annotations

import math

from qbank import name, num, inr
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, cap, sig

S = 'cbse-g10-science-ch'
SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')


def sci(x: float, n: int = 3) -> str:
    if x == 0:
        return '0'
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    if round(m, n - 1) >= 10:
        m /= 10
        e += 1
    return f'{sig(m, n)} × 10{str(e).translate(SUP)}'


def cm(x: float) -> str:
    return f'{"+" if x > 0 else "−"}{num(abs(x), 1)} cm'


def describe(real: bool, m: float) -> str:
    size = 'same size' if abs(abs(m) - 1) < 1e-9 else ('magnified' if abs(m) > 1 else 'diminished')
    return f'{"real" if real else "virtual"}, {"inverted" if m < 0 else "erect"}, {size}'


# ======================= ch09 Light – Reflection and Refraction
def mirror_case(r, kind=None):
    kind = kind or r.choice(['concave', 'convex'])
    F = r.choice([10, 12, 15, 20, 25, 30])
    if kind == 'concave':
        k = r.choice([0.5, 0.6, 0.75, 1.5, 2, 2.5, 3, 4])
        f = -F
    else:
        k = r.choice([0.5, 1, 1.5, 2, 3])
        f = F
    u = -k * F
    v = 1 / (1 / f - 1 / u)
    m = -v / u
    return kind, f, u, v, m


def c9s2_mirror(r):
    kind, f, u, v, m = mirror_case(r)
    h = r.choice([2, 3, 4, 5, 6])
    real = v < 0
    return {'stem': f'An object {h} cm high is placed {num(-u, 1)} cm in front of a {kind} mirror of focal length {num(abs(f))} cm. Find the position, nature and size of the image.',
            'answer': f'v = {cm(v)} ({"in front of" if real else "behind"} the mirror); {describe(real, m)}; height {"+" if m > 0 else "−"}{sig(abs(m * h), 3)} cm (m = {sig(m, 3)})',
            'key': f'f = {cm(f)}, u = {cm(u)}. 1/v = 1/f − 1/u ⇒ v = {cm(v)}. m = −v/u = {sig(m, 3)}; h′ = m × h = {sig(m * h, 3)} cm. (1 mark v, 1 mark m, 1 mark nature)'}


def c9s2_v(r):
    kind, f, u, v, m = mirror_case(r)
    d = [cm(-v), cm(1 / (1 / f + 1 / u)) if abs(1 / f + 1 / u) > 1e-9 else cm(v * 2), cm(v * 2)]
    return {'stem': f'An object is placed {num(-u, 1)} cm in front of a {kind} mirror of focal length {num(abs(f))} cm. Where is the image formed?',
            'answer': cm(v), 'key': f'1/v = 1/f − 1/u = 1/({cm(f)}) − 1/({cm(u)}) ⇒ v = {cm(v)}.', 'distractors': d}


def c9s2_m(r):
    kind = r.choice(['concave', 'convex'])
    h = r.choice([2, 4, 5, 10])
    if kind == 'concave':
        m = r.choice([-2, -3, -0.5, 2, 3, 4, -1])
    else:
        m = r.choice([0.5, 0.25, 0.2, 0.4])
    u = -r.choice([10, 15, 20, 30, 40])
    v = -m * u
    return {'stem': f'A {kind} mirror produces an image of magnification {sig(m, 2)} of an object {h} cm high placed {num(-u)} cm in front of it. Find the height and position of the image and state its nature.',
            'answer': f'h′ = {sig(m * h, 3)} cm; v = {cm(v)}; {describe(v < 0, m)}', 'key': f'h′ = m × h = {sig(m * h, 3)} cm. m = −v/u ⇒ v = −m × u = {cm(v)}.'}


def c9s2_long(r):
    kind = r.choice(['concave', 'convex'])
    k, f, u, v, m = mirror_case(r, kind)
    h = r.choice([2, 3, 4, 5])
    real = v < 0
    use = {'concave': 'shaving mirrors, dentists\' mirrors, headlights, solar furnaces', 'convex': 'rear-view mirrors in vehicles (wider field of view)'}[kind]
    return {'stem': (f'An object {h} cm tall is placed {num(-u, 1)} cm in front of a {kind} mirror of focal length {num(abs(f))} cm. (a) Using the mirror formula, find the position of the image. '
                     f'(b) Find its size and magnification. (c) State its nature. (d) Describe the ray diagram you would draw. (e) Give one use of this type of mirror.'),
            'answer': (f'(a) v = {cm(v)}. (b) m = {sig(m, 3)}; h′ = {sig(m * h, 3)} cm. (c) {cap(describe(real, m))}. (d) A ray parallel to the axis reflects through (or appears to come from) F; a ray towards the centre of curvature C reflects back along itself; the image is where they meet '
                       f'({"in front of" if real else "behind"} the mirror). (e) {cap(use)}.'),
            'key': '1 mark each part.'}


c9s1_defs = [
    ('the pole', 'the centre of the reflecting surface of a spherical mirror, denoted P'),
    ('the centre of curvature', 'the centre of the sphere of which the reflecting surface of a spherical mirror is a part, denoted C'),
    ('the principal axis', 'the straight line passing through the pole and the centre of curvature of a spherical mirror'),
    ('the principal focus of a concave mirror', 'the point on the principal axis where rays parallel to the axis meet after reflection'),
    ('the focal length', 'the distance between the pole and the principal focus of a spherical mirror'),
    ('the aperture', 'the diameter of the reflecting surface of a spherical mirror'),
    ('the radius of curvature', 'the radius of the sphere of which the mirror is a part; it is twice the focal length'),
]
c9s1_img = {
    'a real, inverted image smaller than the object, between F and C': ['an object beyond C'],
    'a real, inverted image of the same size, at C': ['an object at C'],
    'a real, inverted, magnified image beyond C': ['an object between C and F'],
    'a highly magnified image at infinity': ['an object at F'],
    'a virtual, erect, magnified image behind the mirror': ['an object between P and F'],
    'a highly diminished point-sized image at F': ['an object at infinity'],
}
c9s1_img = {f'formed by a concave mirror with {v[0]}': [k] for k, v in c9s1_img.items()}
c9s1_use = {
    'a concave mirror': ['a torch reflector', 'a shaving mirror', 'a dentist\'s mirror', 'a solar furnace', 'vehicle headlights'],
    'a convex mirror': ['a rear-view mirror in a car', 'a mirror at a blind turn on a hill road', 'a security mirror in a shop'],
    'a plane mirror': ['a dressing-table mirror', 'a periscope'],
}
c9s1_mc = [
    ('The focal length of a spherical mirror of radius of curvature 20 cm is:', '10 cm', '20 cm', '40 cm', '5 cm'),
    ('A convex mirror always forms an image that is:', 'virtual, erect and diminished', 'real and inverted', 'virtual and magnified', 'real and same size'),
    ('No matter how far you stand from a mirror, your image appears erect. The mirror may be:', 'plane or convex', 'only concave', 'only plane', 'concave or plane only'),
    ('A ray passing through the centre of curvature of a concave mirror, after reflection:', 'is reflected back along the same path', 'passes through F', 'becomes parallel to the axis', 'is absorbed'),
    ('A ray parallel to the principal axis, after reflection from a convex mirror:', 'appears to diverge from the principal focus', 'passes through C', 'passes through F', 'retraces its path'),
    ('To get an image of the same size as the object with a concave mirror, the object must be at:', 'C', 'F', 'infinity', 'between P and F'),
]
c9s1_why = [
    ('Why are convex mirrors used as rear-view mirrors in vehicles?', 'They always give an erect, diminished image and have a wider field of view, so the driver sees a larger area of traffic behind.', '1 mark erect/diminished. 1 mark wide field.'),
    ('Why do dentists use concave mirrors?', 'When the tooth is between P and F, a concave mirror forms an erect, magnified image, making it easy to see.', '1 mark position. 1 mark magnified erect.'),
    ('Why is a concave mirror used in a torch?', 'The bulb is placed at the focus; the reflected rays come out as a strong parallel beam.', '2 marks.'),
    ('How will you find the approximate focal length of a concave mirror in the laboratory?', 'Form a sharp image of a distant object (sun or a distant tree) on a screen; the distance between the mirror and the screen is the focal length.', '1 mark method. 1 mark distance = f.'),
]
c9s1_ar = [
    ('The focal length of a spherical mirror is half its radius of curvature.', 'For spherical mirrors of small aperture, R = 2f.', 'a', 'R explains A.'),
    ('A convex mirror is used as a rear-view mirror.', 'It forms an erect and diminished image and has a wider field of view.', 'a', 'R explains A.'),
    ('A concave mirror always forms a real image.', 'A concave mirror can converge light.', 'd', 'A is false (it forms a virtual image when the object is between P and F); R is true.'),
]


def c9s1_RF(r):
    R = r.choice([10, 16, 20, 24, 30, 32, 40, 50, 60])
    kind = r.choice(['concave', 'convex'])
    q = r.random() < 0.5
    if q:
        return {'stem': f'The radius of curvature of a {kind} mirror is {R} cm. What is its focal length?', 'answer': f'{num(R / 2)} cm', 'key': f'f = R/2 = {R}/2 = {num(R / 2)} cm.',
                'distractors': [f'{R} cm', f'{R * 2} cm', f'{num(R / 4)} cm']}
    return {'stem': f'The focal length of a {kind} mirror is {num(R / 2)} cm. What is its radius of curvature?', 'answer': f'{R} cm', 'key': f'R = 2f = 2 × {num(R / 2)} = {R} cm.',
            'distractors': [f'{num(R / 4)} cm', f'{num(R / 2)} cm', f'{R * 2} cm']}


c9s2_defs = [
    ('the mirror formula', 'the relation 1/v + 1/u = 1/f between the object distance u, image distance v and focal length f of a spherical mirror'),
    ('magnification', 'the ratio of the height of the image to the height of the object'),
    ('the New Cartesian sign convention', 'the rule that distances are measured from the pole, those along the incident light are positive and those against it negative, heights above the axis positive'),
    ('a real image', 'an image formed where rays actually meet, which can be obtained on a screen'),
    ('a virtual image', 'an image formed where rays only appear to meet, which cannot be obtained on a screen'),
]
c9s2_mc = [
    ('In the New Cartesian sign convention, the object distance u is always:', 'negative', 'positive', 'zero', 'equal to f'),
    ('A negative value of magnification shows that the image is:', 'real and inverted', 'virtual and erect', 'magnified only', 'at infinity'),
    ('The focal length of a convex mirror is taken as:', 'positive', 'negative', 'zero', 'infinite'),
    ('A magnification of +0.5 means the image is:', 'erect and half the size of the object', 'inverted and half the size', 'erect and twice the size', 'real and same size'),
    ('The image formed by a concave mirror is seen to be virtual, erect and larger. The object is placed:', 'between the pole and the focus', 'at the focus', 'at C', 'beyond C'),
]
c9s2_why = [
    ('Why is the magnification of a convex mirror always positive and less than 1?', 'It always forms a virtual, erect image (positive m) that is smaller than the object.', '1 mark each.'),
    ('Why do we use a sign convention in mirror formula problems?', 'So that a single formula works for all cases, and the signs tell us the position (in front/behind) and nature of the image.', '2 marks.'),
]
c9s2_ar = [
    ('A magnification of −1 means the image is real, inverted and of the same size.', 'Negative magnification indicates an inverted image.', 'a', 'R explains A.'),
    ('The focal length of a concave mirror is negative.', 'The focus of a concave mirror is in front of the mirror, against the direction of incident light.', 'a', 'R explains A.'),
    ('A convex mirror can form a real image.', 'A convex mirror diverges light.', 'd', 'A is false; R is true.'),
]

RI = [('air', 1.0003), ('ice', 1.31), ('water', 1.33), ('alcohol', 1.36), ('kerosene', 1.44), ('fused quartz', 1.46), ('turpentine oil', 1.47), ('benzene', 1.50),
      ('crown glass', 1.52), ('Canada balsam', 1.53), ('rock salt', 1.54), ('carbon disulphide', 1.63), ('dense flint glass', 1.65), ('ruby', 1.71), ('sapphire', 1.77), ('diamond', 2.42)]
c9s3_defs = [
    ('refraction', 'the bending of light when it passes obliquely from one transparent medium into another'),
    ('the refractive index', 'the ratio of the speed of light in vacuum (or one medium) to the speed of light in another medium'),
    ('an optically denser medium', 'a medium with a larger refractive index, in which light travels more slowly'),
    ('Snell\'s law', 'the law that the ratio of the sine of the angle of incidence to the sine of the angle of refraction is constant for a given pair of media'),
    ('lateral displacement', 'the perpendicular shift of the emergent ray from the direction of the incident ray when light passes through a glass slab'),
]
c9s3_mc = [
    ('When light goes from air into glass, it bends:', 'towards the normal', 'away from the normal', 'along the surface', 'not at all'),
    ('The emergent ray from a rectangular glass slab is:', 'parallel to the incident ray', 'perpendicular to the incident ray', 'along the normal', 'bent towards the base'),
    ('A ray of light falling along the normal on a glass slab:', 'goes straight without bending', 'bends towards the normal', 'bends away from the normal', 'is totally reflected'),
    ('A pencil partly immersed in water appears bent at the surface because of:', 'refraction', 'reflection', 'dispersion', 'scattering'),
    ('The speed of light in vacuum is:', '3 × 10⁸ m/s', '3 × 10⁶ m/s', '3 × 10¹⁰ m/s', '3 × 10⁵ m/s'),
    ('Which has the highest optical density?', 'diamond', 'water', 'kerosene', 'crown glass'),
]
c9s3_why = [
    ('Why does a lemon kept in water in a glass tumbler appear larger than its actual size?', 'Light from the lemon bends at the curved water–glass–air surfaces, which act like a converging lens and magnify it.', '1 mark refraction. 1 mark lens action.'),
    ('Why does the bottom of a tank of water appear raised?', 'Light from the bottom bends away from the normal as it leaves water, so it seems to come from a point higher up.', '2 marks.'),
    ('What does a refractive index of 2.42 for diamond mean?', 'Light travels 2.42 times faster in vacuum than in diamond.', '2 marks.'),
]
c9s3_ar = [
    ('Light bends towards the normal when it enters water from air.', 'Water is optically denser than air.', 'a', 'R explains A.'),
    ('The emergent ray from a glass slab is parallel to the incident ray.', 'The bending at the two parallel faces is equal and opposite.', 'a', 'R explains A.'),
    ('Kerosene is optically denser than water though it is lighter.', 'Optical density is not the same as mass density.', 'a', 'R explains A.'),
    ('Light travels faster in glass than in air.', 'Glass has a higher refractive index than air.', 'd', 'A is false; R is true.'),
]


def c9s3_speed(r):
    m, n = r.choice(RI[1:])
    v = 3e8 / n
    return {'stem': f'The refractive index of {m} is {n}. Find the speed of light in {m}. (c = 3 × 10⁸ m/s)', 'answer': f'{sci(v)} m/s',
            'key': f'v = c/n = 3 × 10⁸/{n} = {sci(v)} m/s.', 'distractors': [f'{sci(3e8 * n)} m/s', f'{sci(v / 10)} m/s', f'{sci(3e8 / (n + 0.5))} m/s']}


def c9s3_rel(r):
    (a, na), (b, nb) = r.sample(RI[1:], 2)
    n21 = nb / na
    return {'stem': f'The refractive indices of {a} and {b} are {na} and {nb}. Find the refractive index of {b} with respect to {a}. In which medium does light travel faster?',
            'answer': f'{sig(n21, 3)}; faster in {a if na < nb else b}', 'key': f'n = n({b})/n({a}) = {nb}/{na} = {sig(n21, 3)}. Lower refractive index ⇒ higher speed: {a if na < nb else b}.'}


def c9s3_denser(r):
    xs = r.sample(RI[1:], 4)
    if len({n for _, n in xs}) < 4:
        raise ValueError
    a = max(xs, key=lambda t: t[1])
    q = r.random() < 0.5
    if q:
        a = min(xs, key=lambda t: t[1])
        return {'stem': 'In which of these media does light travel fastest? ' + ', '.join(f'{m} (n = {n})' for m, n in xs), 'answer': f'{a[0]} (n = {a[1]})',
                'key': 'Speed v = c/n: smallest n means fastest.', 'distractors': [f'{m} (n = {n})' for m, n in xs if m != a[0]]}
    return {'stem': 'Which of these is optically densest? ' + ', '.join(f'{m} (n = {n})' for m, n in xs), 'answer': f'{a[0]} (n = {a[1]})',
            'key': 'The largest refractive index means the optically densest medium.', 'distractors': [f'{m} (n = {n})' for m, n in xs if m != a[0]]}


def c9s3_vv(r):
    (a, na), (b, nb) = r.sample(RI[1:], 2)
    va = 3e8 / na
    vb = 3e8 / nb
    return {'stem': f'Light travels in {a} at {sci(va)} m/s and in {b} at {sci(vb)} m/s. Find the refractive index of {a} with respect to {b}, and state which is optically denser.',
            'answer': f'{sig(vb / va, 3)}; {a if na > nb else b} is optically denser', 'key': f'n = v({b})/v({a}) = {sig(vb / va, 3)}. The medium in which light is slower is denser.'}


def lens_case(r, kind=None):
    kind = kind or r.choice(['convex', 'concave'])
    F = r.choice([10, 12, 15, 20, 25])
    if kind == 'convex':
        k = r.choice([0.5, 0.6, 0.75, 1.5, 2, 2.5, 3, 4])
        f = F
    else:
        k = r.choice([0.5, 1, 1.5, 2, 3])
        f = -F
    u = -k * F
    v = 1 / (1 / f + 1 / u)
    m = v / u
    return kind, f, u, v, m


def c9s4_lens(r):
    kind, f, u, v, m = lens_case(r)
    h = r.choice([2, 3, 4, 5])
    real = v > 0
    return {'stem': f'An object {h} cm high is placed {num(-u, 1)} cm from a {kind} lens of focal length {num(abs(f))} cm. Find the position, nature and size of the image.',
            'answer': f'v = {cm(v)} ({"on the other side of" if real else "on the same side as the object, in front of"} the lens); {describe(real, m)}; height {"+" if m > 0 else "−"}{sig(abs(m * h), 3)} cm (m = {sig(m, 3)})',
            'key': f'f = {cm(f)}, u = {cm(u)}. 1/v = 1/f + 1/u ⇒ v = {cm(v)}. m = v/u = {sig(m, 3)}; h′ = {sig(m * h, 3)} cm. (1 mark each step)'}


def c9s4_v(r):
    kind, f, u, v, m = lens_case(r)
    alt = 1 / (1 / f - 1 / u) if abs(1 / f - 1 / u) > 1e-9 else v * 3
    return {'stem': f'An object is placed {num(-u, 1)} cm from a {kind} lens of focal length {num(abs(f))} cm. Where is the image formed?', 'answer': cm(v),
            'key': f'1/v = 1/f + 1/u ⇒ v = {cm(v)}.', 'distractors': [cm(-v), cm(alt) if cm(alt) != cm(v) else cm(v * 3), cm(v * 2)]}


def c9s4_power(r):
    kind = r.choice(['convex', 'concave'])
    f = r.choice([10, 20, 25, 40, 50, 80, 100, 200]) * (1 if kind == 'convex' else -1)
    P = 100 / f
    return {'stem': f'Find the power of a {kind} lens of focal length {num(abs(f))} cm.', 'answer': f'{"+" if P > 0 else "−"}{num(abs(P), 2)} D',
            'key': f'P = 1/f (in metres) = 1/({num(f / 100, 2)} m) = {num(P, 2)} D. {"Convex: positive" if P > 0 else "Concave: negative"}.',
            'distractors': [f'{"−" if P > 0 else "+"}{num(abs(P), 2)} D', f'{"+" if P > 0 else "−"}{num(abs(f) / 100, 2)} D', f'{"+" if P > 0 else "−"}{num(abs(P) * 10, 2)} D']}


def c9s4_combo(r):
    p1 = r.choice([2, 2.5, 4, 5, -1, -2])
    p2 = r.choice([-1.5, -0.5, 1, 1.5, 3, -2.5])
    P = p1 + p2
    if abs(P) < 1e-9:
        raise ValueError
    f = 100 / P
    return {'stem': f'Two thin lenses of power {num(p1, 2)} D and {num(p2, 2)} D are placed in contact. Find the power and focal length of the combination. Is it converging or diverging?',
            'answer': f'P = {num(P, 2)} D; f = {num(f, 1)} cm; {"converging" if P > 0 else "diverging"}', 'key': f'P = P₁ + P₂ = {num(p1, 2)} + ({num(p2, 2)}) = {num(P, 2)} D; f = 1/P = {num(f / 100, 3)} m = {num(f, 1)} cm.'}


def c9s4_long(r):
    kind, f, u, v, m = lens_case(r)
    h = r.choice([2, 3, 4, 5])
    real = v > 0
    P = 100 / f
    return {'stem': (f'An object {h} cm tall is placed {num(-u, 1)} cm from a {kind} lens of focal length {num(abs(f))} cm. (a) Find the position of the image. (b) Find the magnification and height of the image. '
                     f'(c) State its nature. (d) Find the power of the lens. (e) Describe the ray diagram.'),
            'answer': (f'(a) v = {cm(v)}. (b) m = {sig(m, 3)}; h′ = {sig(m * h, 3)} cm. (c) {cap(describe(real, m))}. (d) P = {num(P, 2)} D. (e) A ray parallel to the axis passes through (or appears to come from) F₂ after refraction; '
                       f'a ray through the optical centre goes undeviated; the image is where they {"meet" if real else "appear to meet"}.'),
            'key': '1 mark each part.'}


c9s4_defs = [
    ('a convex lens', 'a lens thicker at the middle than at the edges, which converges light'),
    ('a concave lens', 'a lens thinner at the middle than at the edges, which diverges light'),
    ('the optical centre', 'the central point of a lens through which a ray passes without deviation'),
    ('the power of a lens', 'the reciprocal of its focal length in metres; its SI unit is the dioptre'),
    ('one dioptre', 'the power of a lens whose focal length is 1 metre'),
    ('the lens formula', 'the relation 1/v − 1/u = 1/f between the object distance, image distance and focal length of a lens'),
]
c9s4_img = {
    'a real, inverted, diminished image between F₂ and 2F₂': ['an object beyond 2F₁'],
    'a real, inverted image of the same size at 2F₂': ['an object at 2F₁'],
    'a real, inverted, enlarged image beyond 2F₂': ['an object between F₁ and 2F₁'],
    'a virtual, erect, enlarged image on the same side as the object': ['an object between F₁ and the optical centre'],
    'a point-sized image at F₂': ['an object at infinity'],
    'an infinitely large image at infinity': ['an object at F₁'],
}
c9s4_img = {f'formed by a convex lens with {v[0]}': [k] for k, v in c9s4_img.items()}
c9s4_mc = [
    ('A concave lens always gives an image that is:', 'virtual, erect and diminished', 'real and inverted', 'virtual and magnified', 'real and same size'),
    ('The power of a convex lens is:', 'positive', 'negative', 'zero', 'infinite'),
    ('A lens of power −2 D is:', 'concave, with focal length 50 cm', 'convex, with focal length 50 cm', 'concave, with focal length 2 m', 'convex, with focal length 2 m'),
    ('A magnifying glass is a:', 'convex lens with the object within its focal length', 'concave lens', 'convex mirror', 'plane mirror'),
    ('The SI unit of power of a lens is the:', 'dioptre', 'metre', 'watt', 'joule'),
    ('An optician prescribes a lens of +1.5 D. The lens is:', 'converging', 'diverging', 'plane', 'cylindrical'),
]
c9s4_why = [
    ('Why is a convex lens called a converging lens?', 'Parallel rays of light passing through it bend towards each other and meet at the principal focus.', '2 marks.'),
    ('How will you distinguish between a convex and a concave lens by touching and by looking through them?', 'Convex is thicker in the middle; it magnifies nearby print. Concave is thinner in the middle; print looks smaller.', '1 mark each.'),
    ('Why does a concave lens never form a real image?', 'It diverges the refracted rays, which never actually meet; they only appear to come from a point on the same side as the object.', '2 marks.'),
]
c9s4_ar = [
    ('A convex lens can form both real and virtual images.', 'The nature of the image depends on the position of the object.', 'a', 'R explains A.'),
    ('The power of a concave lens is negative.', 'Its focal length is negative by the sign convention.', 'a', 'R explains A.'),
    ('A lens of focal length 25 cm has a power of +4 D.', 'P = 1/f, with f in metres.', 'a', 'R explains A (assuming a convex lens).'),
    ('A concave lens is used as a magnifying glass.', 'A concave lens diverges light.', 'd', 'A is false; R is true.'),
]
c9_hots = [
    ('A student finds the image of a distant tree on a screen 20 cm from a lens. What type of lens is it, and what is its power? Where should a candle be placed to get an image of the same size?', 'Convex lens; f = 20 cm, P = +5 D. At 2F, i.e. 40 cm from the lens (image also at 40 cm on the other side).', '1 mark lens. 1 mark power. 1 mark position.'),
    ('One half of a convex lens is covered with black paper. Will it produce a complete image? Explain.', 'Yes, the full image is formed, because rays from every point of the object still pass through the uncovered half; the image is less bright.', '1 mark yes. 1 mark reason. 1 mark brightness.'),
    ('A ray of light enters a glass slab (n = 1.5) from air. Is the speed of light in glass more or less? Find it, and explain why the emergent ray is parallel to the incident ray.', 'Less: v = 3 × 10⁸/1.5 = 2 × 10⁸ m/s. The bending towards the normal at the first face and away at the second are equal and opposite.', '1 mark less. 1 mark speed. 1 mark parallel.'),
    ('You are given a concave mirror and a convex mirror of the same size. Which will you use as a reflector in a car headlight and which as a side-view mirror? Justify.', 'Concave mirror for the headlight (bulb at F gives a parallel beam); convex mirror as side-view mirror (erect, diminished image, wide field of view).', '1 mark each choice. 1 mark reasons.'),
]


def c9_case(r):
    kind, f, u, v, m = lens_case(r, 'convex')
    if v < 0:
        raise ValueError
    return {'stem': (f'Read: In a school laboratory in Jabalpur, Ishaan places a candle {num(-u, 1)} cm from a convex lens of focal length {num(f)} cm and moves a screen to get a sharp image.\n'
                     '(i) At what distance from the lens is the screen placed? (ii) Find the magnification. (iii) Is the image real or virtual, erect or inverted? (iv) What is the power of the lens?'),
            'answer': f'(i) {num(v, 1)} cm on the other side. (ii) m = {sig(m, 3)}. (iii) Real and inverted. (iv) +{num(100 / f, 2)} D.', 'key': '1 mark each part.'}


c9_long = [
    ('Draw ray diagrams to show the formation of images by a concave mirror when the object is (a) beyond C (b) between C and F (c) between F and P. State the nature, position and size of the image in each case.',
     '(a) Between F and C, real, inverted, diminished. (b) Beyond C, real, inverted, magnified. (c) Behind the mirror, virtual, erect, magnified. Ray diagrams use a ray parallel to the axis (reflects through F) and a ray through C (reflects back along itself).',
     '1⅔ marks each case (rounded).'),
    ('State the laws of refraction. Define refractive index and absolute refractive index. Draw a ray diagram for refraction through a rectangular glass slab and mark the angle of incidence, angle of refraction, angle of emergence and lateral displacement.',
     'Laws: incident ray, refracted ray and normal lie in one plane; sin i/sin r = constant (Snell\'s law). Refractive index n₂₁ = v₁/v₂; absolute n = c/v. Slab diagram: ray bends towards normal at entry, away at exit; emergent ray parallel to incident, laterally displaced.',
     '2 marks laws; 1 mark definitions; 2 marks diagram.'),
]

# ======================= ch10 The Human Eye and the Colourful World
c10s1_defs = [
    ('the cornea', 'the thin transparent membrane at the front of the eye where most of the refraction of light takes place'),
    ('the iris', 'the dark muscular diaphragm behind the cornea that controls the size of the pupil'),
    ('the pupil', 'the opening in the iris that regulates the amount of light entering the eye'),
    ('the retina', 'the light-sensitive screen at the back of the eye on which the image is formed'),
    ('the ciliary muscles', 'muscles that change the curvature, and so the focal length, of the eye lens'),
    ('accommodation', 'the ability of the eye lens to adjust its focal length to see near and far objects clearly'),
    ('the near point', 'the minimum distance (about 25 cm for a normal eye) at which objects can be seen clearly without strain'),
    ('the far point', 'the farthest point up to which the eye can see objects clearly; infinity for a normal eye'),
    ('the optic nerve', 'the nerve that carries electrical signals from the retina to the brain'),
]
c10s1_cats = {
    'controls the amount of light entering the eye': ['the iris', 'the pupil'],
    'changes the focal length of the eye lens': ['the ciliary muscles'],
    'refracts most of the light entering the eye': ['the cornea'],
    'converts light into electrical signals': ['the retina'],
    'carries signals to the brain': ['the optic nerve'],
}
c10s1_mc = [
    ('The image formed on the retina is:', 'real and inverted', 'virtual and erect', 'real and erect', 'virtual and inverted'),
    ('When we look at distant objects, the ciliary muscles are:', 'relaxed and the lens is thin', 'contracted and the lens is thick', 'relaxed and the lens is thick', 'contracted and the lens is thin'),
    ('The least distance of distinct vision for a normal young adult is about:', '25 cm', '25 m', '2.5 cm', '250 cm'),
    ('The far point of a normal eye is at:', 'infinity', '25 cm', '1 m', '100 m'),
    ('A cataract is a condition in which:', 'the crystalline lens becomes milky and cloudy', 'the retina is torn', 'the cornea is curved', 'the pupil is too large'),
    ('In bright light, the pupil:', 'contracts', 'expands', 'stays the same', 'closes completely'),
]
c10s1_why = [
    ('Why does it take some time to see objects in a dim room when we enter from bright sunlight?', 'The pupil was small in bright light; it takes time to expand to let enough light in.', '2 marks.'),
    ('Why is a normal eye unable to see clearly objects placed closer than 25 cm?', 'The focal length of the eye lens cannot be decreased below a certain minimum, so the image of a very close object cannot be focused on the retina.', '2 marks.'),
    ('Why do we have two eyes and not one?', 'Two eyes give a wider field of view (about 180°), help judge depth and distance (three-dimensional vision), and improve detection of faint objects.', '1 mark each (any two).'),
]
c10s1_ar = [
    ('The eye can see objects at different distances.', 'The ciliary muscles change the focal length of the eye lens.', 'a', 'R explains A.'),
    ('The pupil becomes smaller in bright light.', 'The iris controls the size of the pupil.', 'a', 'R explains A.'),
    ('Most refraction in the eye occurs at the eye lens.', 'The eye lens is a convex lens.', 'd', 'A is false (most refraction occurs at the cornea); R is true.'),
]


def c10s1_acc(r):
    N = r.choice([25, 30, 40, 50])
    k = 'distant (far point at infinity)'
    P_far = 100 / 2.5  # eye length about 2.5 cm (illustrative)
    fn = 1 / (1 / 2.5 + 1 / N)
    return {'stem': f'Assume the eye lens is {num(2.5)} cm from the retina. What focal length must the eye lens have to see (a) a distant object (b) an object {N} cm away clearly? What does this show?',
            'answer': f'(a) 2.5 cm (b) {sig(fn, 3)} cm; the eye lens must become more convex (shorter focal length) for near objects — accommodation.',
            'key': f'(a) u = ∞, v = 2.5 cm ⇒ f = 2.5 cm. (b) 1/f = 1/2.5 − 1/(−{N}) ⇒ f = {sig(fn, 3)} cm.'}


c10s2_defs = [
    ('myopia', 'near-sightedness, a defect in which a person can see nearby objects clearly but not distant ones'),
    ('hypermetropia', 'far-sightedness, a defect in which a person can see distant objects clearly but not nearby ones'),
    ('presbyopia', 'the loss of the power of accommodation of the eye with age, so that the near point recedes'),
    ('bifocal lenses', 'spectacle lenses with a concave upper part for distant vision and a convex lower part for near vision'),
]
c10s2_cats = {
    'myopia': ['excessive curvature of the eye lens', 'elongation of the eyeball', 'image of distant objects formed in front of the retina', 'corrected with a concave lens'],
    'hypermetropia': ['focal length of the eye lens too long', 'eyeball too short', 'image of nearby objects formed behind the retina', 'corrected with a convex lens'],
    'presbyopia': ['weakening of the ciliary muscles with age', 'decreasing flexibility of the eye lens with age', 'often corrected with bifocal lenses'],
}
c10s2_cats = {f'a feature of {k}': v for k, v in c10s2_cats.items()}
c10s2_mc = [
    ('A myopic person uses spectacles with:', 'concave lenses', 'convex lenses', 'plane glass', 'cylindrical lenses'),
    ('A person cannot read a newspaper held at 25 cm but sees distant buses clearly. The defect is:', 'hypermetropia', 'myopia', 'cataract', 'colour blindness'),
    ('The upper part of a bifocal lens is usually:', 'concave, for distant vision', 'convex, for near vision', 'plane', 'concave, for near vision'),
    ('A person needs a lens of power −2.5 D. The defect is:', 'myopia', 'hypermetropia', 'presbyopia only', 'cataract'),
    ('A hypermetropic eye forms the image of a nearby object:', 'behind the retina', 'in front of the retina', 'on the retina', 'on the cornea'),
]
c10s2_why = [
    ('What are the causes of myopia, and how is it corrected?', 'Excessive curvature of the eye lens or elongation of the eyeball; corrected with a concave lens of suitable power.', '1 mark causes. 1 mark correction.'),
    ('Why do elderly people often need bifocal lenses?', 'They may suffer from both myopia and hypermetropia due to presbyopia; the upper concave part corrects distant vision and the lower convex part near vision.', '2 marks.'),
    ('Why is eye donation encouraged?', 'Corneal blindness can be cured by transplanting corneas from donated eyes; one pair of eyes can give vision to up to four people.', '2 marks.'),
]
c10s2_ar = [
    ('A myopic person uses a concave lens.', 'A concave lens diverges light so that the image of distant objects forms on the retina.', 'a', 'R explains A.'),
    ('Presbyopia occurs with age.', 'The ciliary muscles weaken and the lens loses flexibility with age.', 'a', 'R explains A.'),
    ('Hypermetropia is corrected with a concave lens.', 'In hypermetropia the near point is farther than 25 cm.', 'd', 'A is false (it is corrected by a convex lens); R is true.'),
]


def c10s2_myo(r):
    d = r.choice([50, 80, 100, 125, 150, 200, 250, 400])
    f = -d
    P = 100 / f
    nm = name(r)
    return {'stem': f'{nm} cannot see objects beyond {num(d / 100 if d >= 100 else d, 2)} {"m" if d >= 100 else "cm"} clearly. Name the defect and find the nature, focal length and power of the lens needed.',
            'answer': f'Myopia; concave lens of focal length {cm(f)} and power {num(P, 2)} D',
            'key': f'The lens must form an image of a distant object at the far point: u = ∞, v = −{d} cm ⇒ f = −{d} cm = {num(f / 100, 2)} m; P = 1/f = {num(P, 2)} D.',
}


def c10s2_hyp(r):
    N = r.choice([50, 75, 100, 125, 150])
    u, v = -25, -N
    f = 1 / (1 / v - 1 / u)
    P = 100 / f
    nm = name(r)
    return {'stem': f'The near point of {nm}\'s grandfather is {N} cm. What power of lens is needed for him to read a book at 25 cm? Name the defect and the type of lens.',
            'answer': f'Hypermetropia; convex lens of focal length {num(f, 1)} cm, power +{num(P, 2)} D',
            'key': f'The lens must form a virtual image of the book (u = −25 cm) at the near point (v = −{N} cm). 1/f = 1/v − 1/u = −1/{N} + 1/25 ⇒ f = {num(f, 1)} cm; P = 100/f = +{num(P, 2)} D.'}


def c10s2_mcq(r):
    d = r.choice([50, 80, 100, 125, 200, 250])
    P = -100 / d
    return {'stem': f'The far point of a myopic eye is {d} cm. The power of the corrective lens is:', 'answer': f'{num(P, 2)} D', 'key': f'f = −{d} cm; P = 100/f = {num(P, 2)} D.',
            'distractors': [f'+{num(-P, 2)} D', f'{num(P / 2, 2)} D', f'{num(P * 2, 2)} D']}


def c10s2_long(r):
    d = r.choice([80, 100, 125, 200])
    N = r.choice([50, 75, 100])
    Pm = -100 / d
    fh = 1 / (-1 / N + 1 / 25)
    Ph = 100 / fh
    return {'stem': (f'A person has a far point of {d} cm and a near point of {N} cm. (a) Name the two defects. (b) Find the power of the lens needed to correct distant vision. (c) Find the power needed for reading at 25 cm. '
                     '(d) What type of spectacles would suit this person? (e) Give one cause of each defect.'),
            'answer': f'(a) Myopia and hypermetropia (presbyopia). (b) {num(Pm, 2)} D (concave). (c) +{num(Ph, 2)} D (convex). (d) Bifocal lenses – concave upper part, convex lower part. (e) Myopia: elongated eyeball/excess curvature; hypermetropia: short eyeball/long focal length (weak ciliary muscles with age).',
            'key': f'(b) f = −{d} cm. (c) 1/f = −1/{N} + 1/25 ⇒ f = {num(fh, 1)} cm. 1 mark each part.'}


c10s3_defs = [
    ('dispersion', 'the splitting of white light into its component colours'),
    ('a spectrum', 'the band of coloured components of a light beam'),
    ('the angle of deviation', 'the angle between the incident ray and the emergent ray in a prism'),
    ('a prism', 'a transparent object with two triangular bases and three rectangular faces inclined to each other'),
    ('the angle of the prism', 'the angle between two lateral faces of a prism'),
]
COLOURS = ['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
c10s3_mc = [
    ('In the spectrum of white light, the colour that bends the least is:', 'red', 'violet', 'green', 'blue'),
    ('Dispersion of light occurs because:', 'different colours bend through different angles in glass', 'light reflects', 'light is absorbed', 'light slows down equally for all colours'),
    ('A rainbow is formed by:', 'dispersion, refraction and internal reflection in raindrops', 'scattering by dust', 'reflection from clouds', 'diffraction'),
    ('A rainbow is always formed in the direction:', 'opposite to the Sun', 'of the Sun', 'overhead', 'of the North'),
    ('Isaac Newton showed that white light is made of seven colours by using:', 'a second, inverted prism to recombine the spectrum', 'a mirror', 'a lens', 'a screen alone'),
    ('The sequence of colours in the spectrum is remembered by the acronym:', 'VIBGYOR', 'ROYGBIV only for blue', 'BIGROY', 'GROVYIB'),
]
c10s3_why = [
    ('Why does white light split into colours when it passes through a prism?', 'Different colours travel at different speeds in glass and bend through different angles; red bends least and violet most.', '2 marks.'),
    ('Why does a second prism placed upside down recombine the spectrum into white light?', 'It bends each colour back by the same amount in the opposite direction, so all colours emerge together.', '2 marks.'),
    ('Why can a rainbow be seen only when the Sun is behind the observer?', 'Raindrops act like tiny prisms that refract, disperse and internally reflect sunlight back towards the side of the Sun, so the observer must face away from it.', '2 marks.'),
]
c10s3_ar = [
    ('Red light is deviated the least by a prism.', 'Red light has the highest speed in glass among visible colours.', 'a', 'R explains A.'),
    ('A rainbow is a natural spectrum.', 'Water droplets disperse sunlight.', 'a', 'R explains A.'),
    ('A glass slab disperses white light into colours that are seen on a screen.', 'The faces of a glass slab are parallel.', 'd', 'A is false (colours recombine on emerging); R is true.'),
]


def c10s3_col(r):
    a, b = r.sample(COLOURS, 2)
    q = r.choice(['more', 'less'])
    ia, ib = COLOURS.index(a), COLOURS.index(b)
    ans = (a if ia < ib else b) if q == 'more' else (a if ia > ib else b)
    return {'stem': f'Which of the two colours, {a} or {b}, is deviated {q} by a glass prism?', 'answer': ans, 'key': 'Deviation increases from red to violet (VIBGYOR order: violet most, red least).',
            'distractors': [b if ans == a else a, 'both equally', 'neither']}


def c10s3_order(r):
    xs = r.sample(COLOURS, 4)
    o = sorted(xs, key=COLOURS.index)
    return {'stem': f'Arrange these colours in decreasing order of the deviation they suffer in a prism: {", ".join(xs)}.', 'answer': ' > '.join(o), 'key': 'Violet is deviated most and red least: V > I > B > G > Y > O > R.'}


c10s4_defs = [
    ('atmospheric refraction', 'the refraction of light by the earth\'s atmosphere, whose layers have different optical densities'),
    ('scattering of light', 'the spreading of light in different directions by particles in its path'),
    ('the Tyndall effect', 'the scattering of light by colloidal particles, which makes the path of a beam visible'),
    ('twinkling', 'the flickering of the brightness and position of stars caused by atmospheric refraction'),
]
c10s4_cats = {
    'atmospheric refraction': ['twinkling of stars', 'advanced sunrise and delayed sunset by about 2 minutes', 'the flattened appearance of the Sun at sunrise', 'the wavering of objects seen through hot air above a fire'],
    'scattering of light': ['the blue colour of the clear sky', 'the reddish appearance of the Sun at sunset', 'the white colour of clouds', 'a beam of sunlight visible in a smoke-filled room', 'the black sky seen by astronauts'],
}
c10s4_cats = {f'a result of {k}': v for k, v in c10s4_cats.items()}
c10s4_mc = [
    ('The sky appears blue because:', 'air molecules scatter blue light more than red light', 'the sea reflects blue light', 'the atmosphere absorbs blue light', 'blue light travels fastest'),
    ('Danger signal lights are red because red light:', 'is scattered least by fog and smoke and can be seen from far', 'is cheapest', 'is brightest', 'travels fastest'),
    ('Planets do not twinkle because:', 'they are close and act as extended sources, so the variations average out', 'they emit their own light', 'they are far', 'they move'),
    ('The Sun appears reddish at sunrise and sunset because:', 'light travels a longer path through the atmosphere and most blue light is scattered away', 'the Sun is red then', 'the clouds are red', 'refraction increases'),
    ('To an astronaut in space, the sky appears:', 'dark', 'blue', 'red', 'white'),
    ('The Sun is visible about 2 minutes before actual sunrise due to:', 'atmospheric refraction', 'scattering', 'dispersion', 'reflection'),
]
c10s4_why = [
    ('Why do stars twinkle?', 'Starlight is refracted repeatedly by atmospheric layers of changing density, so the apparent position and brightness of the star fluctuate.', '2 marks.'),
    ('Why does the clear sky look blue?', 'Air molecules and fine particles are smaller than the wavelength of visible light and scatter shorter (blue) wavelengths much more than red.', '2 marks.'),
    ('Why does the Sun appear reddish at sunrise?', 'Light from the Sun near the horizon passes through thicker layers of air; most blue light is scattered away and mainly red light reaches us.', '2 marks.'),
    ('Why are clouds white?', 'Water droplets in clouds are large and scatter all colours almost equally, so the scattered light looks white.', '2 marks.'),
]
c10s4_ar = [
    ('Planets do not twinkle.', 'Planets are much closer and appear as extended sources.', 'a', 'R explains A.'),
    ('The sky appears dark at very high altitudes.', 'There is very little air to scatter sunlight.', 'a', 'R explains A.'),
    ('The Sun appears white at noon.', 'At noon sunlight travels a shorter distance through the atmosphere, so less blue light is scattered.', 'a', 'R explains A.'),
    ('Stars twinkle because of scattering of light.', 'Scattering makes the sky blue.', 'd', 'A is false (it is due to atmospheric refraction); R is true.'),
]
c10_hots = [
    ('A student sitting at the back of the class cannot read the blackboard but can read her book. What defect does she have, what type of lens should she use, and why?', 'Myopia: the image of distant objects forms in front of the retina; a concave lens of suitable power diverges the rays so the image forms on the retina.', '1 mark defect. 1 mark lens. 1 mark reason.'),
    ('Why does the sky appear blue to us but black on the Moon? What colour would the sky appear if the Earth had no atmosphere?', 'Air molecules scatter blue light; the Moon has no atmosphere, so no scattering and the sky is dark; without an atmosphere the Earth\'s sky would also appear dark.', '1 mark each.'),
    ('Why are the traffic signals red for "stop", and why is the colour of the danger signal seen through fog from a distance?', 'Red light has the longest wavelength and is scattered least by fog and smoke, so it reaches far and can be seen from a distance.', '1 mark least scattering. 1 mark longest wavelength. 1 mark visible far.'),
    ('Explain why the time difference between actual sunset and apparent sunset is about 2 minutes. Would this happen on the Moon?', 'Atmospheric refraction bends sunlight so that the Sun appears above the horizon after it has actually set; on the Moon there is no atmosphere, so no such effect.', '1 mark refraction. 1 mark appears above horizon. 1 mark Moon.'),
]


def c10_case(r):
    d = r.choice([100, 125, 200, 250])
    P = -100 / d
    nm = name(r)
    return {'stem': (f'Read: {nm}, a Class X student, finds it hard to read the blackboard from the last bench but can read the textbook easily. An optometrist finds that the student\'s far point is {d} cm.\n'
                     '(i) Name the defect. (ii) Give one possible cause. (iii) What is the type and power of the lens needed? (iv) Draw (describe) how the lens corrects the defect.'),
            'answer': f'(i) Myopia. (ii) Excessive curvature of the eye lens or elongation of the eyeball. (iii) Concave lens of power {num(P, 2)} D (f = −{d} cm). (iv) The concave lens diverges parallel rays so they appear to come from the far point, and the eye focuses them on the retina.',
            'key': '1 mark each part.'}


c10_case_s = [
    ('Read: Rohit, standing on a roof in Shillong after a shower, saw a rainbow in the east in the evening. He also noticed that the setting Sun looked red and that the sky overhead was blue.\n'
     '(i) Why was the rainbow in the east? (ii) Name the three processes in raindrops that form a rainbow. (iii) Why did the setting Sun look red? (iv) Why is the sky overhead blue?',
     '(i) The Sun was in the west; a rainbow forms opposite to the Sun. (ii) Refraction, dispersion and internal reflection. (iii) Light travels a long path through air at sunset, blue light is scattered away and red reaches the eye. (iv) Air molecules scatter blue light more.', '1 mark each part.'),
]
c10_long = [
    ('Describe the structure of the human eye with a labelled diagram and explain how it forms images of near and far objects (accommodation). What is the range of vision of a normal eye?',
     'Cornea (most refraction), iris and pupil (control light), eye lens (fine focusing), ciliary muscles (change lens curvature), retina (screen with light-sensitive cells), optic nerve (signals to brain). Far objects: ciliary muscles relax, lens thin, longer focal length; near objects: muscles contract, lens thick, shorter focal length. Normal range: 25 cm to infinity.',
     '2 marks diagram; 2 marks accommodation; 1 mark range.'),
    ('What is dispersion? Explain with a diagram how a glass prism disperses white light. How is a rainbow formed?',
     'Splitting of white light into colours. In a prism each colour bends through a different angle (red least, violet most), forming the VIBGYOR spectrum on a screen. Rainbow: sunlight is refracted and dispersed on entering raindrops, reflected internally and refracted again on leaving; seen opposite to the Sun.',
     '1 mark definition; 2 marks prism; 2 marks rainbow.'),
    ('Explain the following with reasons: (a) twinkling of stars (b) planets do not twinkle (c) advanced sunrise and delayed sunset (d) the blue colour of the sky (e) the reddish Sun at sunrise.',
     '(a) Atmospheric refraction by layers of varying density makes the star\'s apparent position and brightness flicker. (b) Planets are extended sources; fluctuations average out. (c) Atmospheric refraction raises the apparent position of the Sun near the horizon (about 2 minutes). (d) Scattering of blue light by air molecules. (e) Longer path at the horizon scatters blue away, leaving red.',
     '1 mark each.'),
]

# ======================= ch11 Electricity
E = 1.6e-19
c11s1_defs = [
    ('electric current', 'the rate of flow of electric charge through a conductor'),
    ('one ampere', 'the current when one coulomb of charge flows through a conductor in one second'),
    ('potential difference', 'the work done to move a unit charge from one point to another in an electric circuit'),
    ('one volt', 'the potential difference between two points when 1 joule of work is done to move 1 coulomb of charge between them'),
    ('an ammeter', 'an instrument connected in series in a circuit to measure electric current'),
    ('a voltmeter', 'an instrument connected in parallel across two points to measure potential difference'),
    ('a circuit diagram', 'a diagram showing how electrical components are connected, using standard symbols'),
    ('one coulomb', 'the charge carried by about 6.25 × 10¹⁸ electrons'),
]
c11s1_cats = {
    'connected in series': ['an ammeter', 'a fuse', 'a switch (plug key)'],
    'connected in parallel': ['a voltmeter', 'household appliances in a domestic circuit', 'each light bulb in a house'],
}
c11s1_mc = [
    ('The SI unit of electric charge is the:', 'coulomb', 'ampere', 'volt', 'ohm'),
    ('Conventionally, electric current flows:', 'from the positive to the negative terminal outside the cell', 'from negative to positive', 'in both directions', 'only inside the cell'),
    ('A voltmeter is always connected:', 'in parallel across the component', 'in series with the component', 'to the earth wire', 'across the ammeter'),
    ('The charge on an electron is:', '1.6 × 10⁻¹⁹ C (negative)', '1.6 × 10¹⁹ C', '1 C', '9.1 × 10⁻³¹ C'),
    ('1 mA is equal to:', '10⁻³ A', '10⁻⁶ A', '10³ A', '10⁻² A'),
]
c11s1_why = [
    ('Why is an ammeter connected in series and a voltmeter in parallel?', 'The ammeter must carry the same current that flows through the component; the voltmeter measures the potential difference between two points, so it is connected across them.', '1 mark each.'),
    ('Why does current flow in a conductor only when a cell is connected?', 'The cell maintains a potential difference across the conductor, which makes the charges (electrons) flow.', '2 marks.'),
]
c11s1_ar = [
    ('An ammeter is connected in series.', 'The same current flows through all components in series.', 'a', 'R explains A.'),
    ('Electrons flow from the negative terminal to the positive terminal outside a cell.', 'Electrons are negatively charged.', 'a', 'R explains A.'),
    ('The SI unit of potential difference is the ampere.', 'Potential difference is the work done per unit charge.', 'd', 'A is false (it is the volt); R is true.'),
]


def c11s1_q(r):
    I = r.choice([0.2, 0.5, 1, 1.5, 2, 3, 5])
    t = r.choice([10, 30, 60, 120, 300, 600])
    Q = I * t
    n = Q / E
    return {'stem': f'A current of {num(I)} A flows through a bulb for {t} s. Find the charge that passes and the number of electrons that flow. (e = 1.6 × 10⁻¹⁹ C)',
            'answer': f'Q = {num(Q, 1)} C; {sci(n)} electrons', 'key': f'Q = It = {num(I)} × {t} = {num(Q, 1)} C; n = Q/e = {num(Q, 1)}/(1.6 × 10⁻¹⁹) = {sci(n)}.'}


def c11s1_I(r):
    Q = r.choice([10, 20, 30, 60, 90, 120, 300])
    t = r.choice([5, 10, 20, 30, 60])
    I = Q / t
    return {'stem': f'{Q} C of charge flows through a wire in {t} s. What is the current?', 'answer': f'{num(I, 2)} A', 'key': f'I = Q/t = {Q}/{t} = {num(I, 2)} A.',
            'distractors': [f'{num(Q * t)} A', f'{num(t / Q, 3)} A', f'{num(I * 2, 2)} A']}


def c11s1_W(r):
    V = r.choice([1.5, 3, 6, 9, 12, 220])
    Q = r.choice([2, 5, 10, 20, 50])
    W = V * Q
    return {'stem': f'How much work is done in moving a charge of {Q} C across two points having a potential difference of {num(V)} V?', 'answer': f'{num(W, 1)} J', 'key': f'W = VQ = {num(V)} × {Q} = {num(W, 1)} J.',
            'distractors': [f'{num(V / Q, 3)} J', f'{num(Q / V, 3)} J', f'{num(W * 2, 1)} J']}


RHO = [('silver', 1.60e-8), ('copper', 1.62e-8), ('aluminium', 2.63e-8), ('tungsten', 5.20e-8), ('nickel', 6.84e-8), ('iron', 10.0e-8), ('chromium', 12.9e-8), ('mercury', 94.0e-8)]
c11s2_defs = [
    ('Ohm\'s law', 'the law that the current through a metallic conductor is directly proportional to the potential difference across its ends, at constant temperature'),
    ('resistance', 'the property of a conductor to oppose the flow of charge through it'),
    ('one ohm', 'the resistance of a conductor through which a current of 1 A flows when the potential difference across it is 1 V'),
    ('resistivity', 'the resistance of a conductor of unit length and unit cross-sectional area; it depends only on the material and temperature'),
    ('a rheostat', 'a variable resistance used to change the current in a circuit'),
]
c11s2_cats = {
    'a good conductor': ['silver', 'copper', 'aluminium'],
    'an alloy used in heating elements': ['nichrome', 'constantan', 'manganin'],
    'an insulator': ['glass', 'rubber', 'ebonite', 'dry paper'],
}
c11s2_mc = [
    ('The resistance of a conductor depends on its:', 'length, area of cross-section and material', 'colour', 'shape only', 'mass only'),
    ('The SI unit of resistivity is:', 'ohm metre (Ω m)', 'ohm', 'ohm per metre', 'volt per ampere'),
    ('If the length of a wire is doubled (same thickness), its resistance:', 'doubles', 'halves', 'stays the same', 'becomes four times'),
    ('Alloys are used in electric heaters because they:', 'have high resistivity and do not oxidise easily at high temperature', 'are good conductors', 'melt easily', 'are cheap'),
    ('The V–I graph of a conductor obeying Ohm\'s law is:', 'a straight line through the origin', 'a curve', 'parallel to the V axis', 'parallel to the I axis'),
    ('Copper and aluminium are used for transmission lines because they have:', 'low resistivity', 'high resistivity', 'low density only', 'high melting point only'),
]
c11s2_why = [
    ('Why is tungsten used for the filaments of bulbs?', 'It has a very high melting point (3380 °C) and high resistivity, so it glows white hot without melting.', '1 mark each.'),
    ('Why does the resistance of a wire decrease when its thickness increases?', 'A thicker wire has a larger area of cross-section, giving more paths for the electrons; R ∝ 1/A.', '2 marks.'),
    ('Why are the coils of electric toasters made of an alloy rather than a pure metal?', 'Alloys have higher resistivity and do not oxidise (burn) readily at high temperatures.', '2 marks.'),
]
c11s2_ar = [
    ('The resistance of a wire is doubled when its length is doubled.', 'Resistance is directly proportional to length.', 'a', 'R explains A.'),
    ('Resistivity of a wire changes when it is cut into two halves.', 'Resistivity depends only on the material and temperature.', 'd', 'A is false; R is true.'),
    ('Copper is used for electric wires.', 'Copper has low resistivity.', 'a', 'R explains A.'),
]


def c11s2_ohm(r):
    q = r.choice(['I', 'V', 'R'])
    R = r.choice([2, 4, 5, 10, 12, 20, 24, 48, 100])
    I = r.choice([0.1, 0.25, 0.5, 1, 1.5, 2, 3])
    V = R * I
    if q == 'I':
        return {'stem': f'A potential difference of {num(V, 2)} V is applied across a resistor of {R} Ω. What current flows?', 'answer': f'{num(I, 2)} A', 'key': f'I = V/R = {num(V, 2)}/{R} = {num(I, 2)} A.',
                'distractors': [f'{num(V * R, 2)} A', f'{num(R / V, 3)} A', f'{num(I * 2, 2)} A']}
    if q == 'V':
        return {'stem': f'A current of {num(I, 2)} A flows through a {R} Ω resistor. Find the potential difference across it.', 'answer': f'{num(V, 2)} V', 'key': f'V = IR = {num(I, 2)} × {R} = {num(V, 2)} V.',
                'distractors': [f'{num(R / I, 2)} V', f'{num(I / R, 3)} V', f'{num(V + R, 2)} V']}
    return {'stem': f'A current of {num(I, 2)} A flows through a wire when {num(V, 2)} V is applied. Find its resistance.', 'answer': f'{num(R)} Ω', 'key': f'R = V/I = {num(V, 2)}/{num(I, 2)} = {R} Ω.',
            'distractors': [f'{num(V * I, 2)} Ω', f'{num(I / V, 3)} Ω', f'{num(R * 2)} Ω']}


def c11s2_rho(r):
    m, rho = r.choice(RHO[:6])
    L = r.choice([1, 2, 5, 10, 50, 100, 1000])
    d = r.choice([0.2, 0.3, 0.4, 0.5, 1])
    A = math.pi * (d / 2 * 1e-3) ** 2
    R = rho * L / A
    return {'stem': f'Find the resistance of {"an" if m[0] in "aeiou" else "a"} {m} wire {L} m long and {num(d, 1)} mm in diameter. (resistivity of {m} = {sci(rho)} Ω m; take π = 3.14)',
            'answer': f'{sig(rho * L / (3.14 * (d / 2 * 1e-3) ** 2), 3)} Ω',
            'key': f'A = πr² = 3.14 × ({num(d / 2, 2)} × 10⁻³)² = {sci(3.14 * (d / 2 * 1e-3) ** 2)} m²; R = ρl/A = {sci(rho)} × {L}/{sci(3.14 * (d / 2 * 1e-3) ** 2)} = {sig(rho * L / (3.14 * (d / 2 * 1e-3) ** 2), 3)} Ω.'}


def c11s2_scale(r):
    R = r.choice([2, 4, 5, 8, 10, 12, 20])
    c = r.choice(['length doubled', 'length halved', 'thickness (radius) doubled', 'radius halved', 'stretched to twice its length (volume constant)'])
    k = {'length doubled': 2, 'length halved': 0.5, 'thickness (radius) doubled': 0.25, 'radius halved': 4, 'stretched to twice its length (volume constant)': 4}[c]
    why = {'length doubled': 'R ∝ l', 'length halved': 'R ∝ l', 'thickness (radius) doubled': 'R ∝ 1/A and A ∝ r²', 'radius halved': 'R ∝ 1/r²', 'stretched to twice its length (volume constant)': 'l doubles and A halves, so R becomes 4 times'}[c]
    alts = {num(R * x, 2) for x in (2, 0.5, 4, 0.25, 1)} - {num(R * k, 2)}
    return {'stem': f'A wire has a resistance of {R} Ω. What is its resistance if the wire (same material) has its {c}?', 'answer': f'{num(R * k, 2)} Ω', 'key': f'{why}: {R} × {num(k, 2)} = {num(R * k, 2)} Ω.',
            'distractors': [f'{a} Ω' for a in sorted(alts)][:3]}


def c11s3_series(r):
    Rs = r.sample([1, 2, 3, 4, 5, 6, 8, 10, 12], r.choice([2, 3]))
    V = r.choice([3, 6, 9, 12, 24])
    Rt = sum(Rs)
    I = V / Rt
    return {'stem': f'Resistors of {", ".join(f"{x} Ω" for x in Rs)} are connected in series to a {V} V battery. Find the total resistance, the current and the potential difference across each resistor.',
            'answer': f'R = {Rt} Ω; I = {sig(I, 3)} A; ' + ', '.join(f'{sig(I * x, 3)} V across {x} Ω' for x in Rs),
            'key': f'Series: R = {" + ".join(map(str, Rs))} = {Rt} Ω; I = V/R = {V}/{Rt} = {sig(I, 3)} A; V = IR for each.'}


def c11s3_par(r):
    Rs = r.sample([2, 3, 4, 6, 8, 10, 12, 20, 30], r.choice([2, 3]))
    V = r.choice([6, 12, 24, 120, 220])
    Rp = 1 / sum(1 / x for x in Rs)
    I = V / Rp
    return {'stem': f'Resistors of {", ".join(f"{x} Ω" for x in Rs)} are connected in parallel across a {V} V supply. Find the equivalent resistance, the total current and the current through each resistor.',
            'answer': f'R = {sig(Rp, 3)} Ω; I = {sig(I, 3)} A; ' + ', '.join(f'{sig(V / x, 3)} A through {x} Ω' for x in Rs),
            'key': f'1/R = {" + ".join(f"1/{x}" for x in Rs)} ⇒ R = {sig(Rp, 3)} Ω; I = V/R = {sig(I, 3)} A; each: V/Rᵢ.'}


def c11s3_eq(r):
    a, b = r.sample([2, 3, 4, 5, 6, 10, 12, 15, 20], 2)
    s, p = a + b, a * b / (a + b)
    q = r.random() < 0.5
    ans = f'{sig(s, 3)} Ω' if q else f'{sig(p, 3)} Ω'
    return {'stem': f'What is the equivalent resistance of {a} Ω and {b} Ω connected in {"series" if q else "parallel"}?', 'answer': ans,
            'key': f'Series: {a} + {b} = {s} Ω. Parallel: {a} × {b}/({a} + {b}) = {sig(p, 3)} Ω.', 'distractors': [x for x in dict.fromkeys([f'{sig(p, 3)} Ω' if q else f'{sig(s, 3)} Ω', f'{sig(abs(a - b), 3)} Ω' if a != b else '1 Ω', f'{sig(a * b, 3)} Ω', f'{sig(s / 2, 3)} Ω']) if x != ans][:3]}


def c11s3_mix(r):
    a = r.choice([2, 3, 4, 5, 6])
    b, c = r.choice([(6, 3), (4, 4), (12, 6), (10, 10), (6, 12), (20, 5), (8, 8)])
    V = r.choice([6, 9, 12, 24])
    p = b * c / (b + c)
    Rt = a + p
    I = V / Rt
    Vp = I * p
    return {'stem': f'A {a} Ω resistor is connected in series with a parallel combination of {b} Ω and {c} Ω resistors across a {V} V battery. Find (a) the total resistance (b) the current from the battery (c) the current through the {b} Ω resistor.',
            'answer': f'(a) {sig(Rt, 3)} Ω (b) {sig(I, 3)} A (c) {sig(Vp / b, 3)} A',
            'key': f'Parallel part: {b} × {c}/({b} + {c}) = {sig(p, 3)} Ω; total = {a} + {sig(p, 3)} = {sig(Rt, 3)} Ω; I = {V}/{sig(Rt, 3)} = {sig(I, 3)} A; V across parallel = {sig(Vp, 3)} V; current in {b} Ω = {sig(Vp / b, 3)} A.'}


def c11s3_n(r):
    R = r.choice([10, 12, 20, 30, 40, 60])
    n = r.choice([2, 3, 4, 5, 6])
    return {'stem': f'{n} identical resistors of {R} Ω each are connected (a) in series and (b) in parallel. Find the ratio of the equivalent resistances in (a) and (b).',
            'answer': f'(a) {n * R} Ω (b) {sig(R / n, 3)} Ω; ratio {n * n} : 1', 'key': f'Series nR = {n * R} Ω; parallel R/n = {sig(R / n, 3)} Ω; ratio n² = {n * n}.'}


def c11s3_long(r):
    a = r.choice([2, 4, 5, 6])
    b, c = r.choice([(6, 3), (12, 6), (10, 10), (20, 5)])
    V = r.choice([6, 12, 24])
    p = b * c / (b + c)
    Rt = a + p
    I = V / Rt
    Va = I * a
    Vp = I * p
    P = V * I
    return {'stem': (f'In a circuit, a {a} Ω resistor R₁ is in series with a parallel combination of R₂ = {b} Ω and R₃ = {c} Ω, connected to a {V} V battery. Find: (a) the equivalent resistance (b) the current from the battery '
                     '(c) the potential difference across R₁ and across the parallel part (d) the current through R₂ and R₃ (e) the total power drawn. Why are household appliances connected in parallel, not in series?'),
            'answer': f'(a) {sig(Rt, 3)} Ω (b) {sig(I, 3)} A (c) {sig(Va, 3)} V; {sig(Vp, 3)} V (d) {sig(Vp / b, 3)} A; {sig(Vp / c, 3)} A (e) {sig(P, 3)} W. Parallel: each appliance gets the full voltage, can be switched independently, and draws its own current; total resistance is lower.',
            'key': '1 mark each of (a)–(d) combined with working; 1 mark (e) and reason.'}


c11s3_defs = [
    ('a series connection', 'an arrangement in which resistors are joined end to end so that the same current flows through each'),
    ('a parallel connection', 'an arrangement in which resistors are connected between the same two points so that the potential difference across each is the same'),
    ('the equivalent resistance', 'the single resistance that can replace a combination of resistors without changing the current in the circuit'),
]
c11s3_mc = [
    ('In a series circuit, the current through each resistor is:', 'the same', 'different', 'zero', 'inversely proportional to resistance'),
    ('In a parallel combination, the equivalent resistance is:', 'less than the smallest resistance', 'more than the largest', 'equal to the sum', 'equal to the average'),
    ('In a parallel circuit, the potential difference across each resistor is:', 'the same', 'different', 'zero', 'proportional to resistance'),
    ('Decorative lights connected in series all go off when one bulb fuses because:', 'the circuit is broken', 'the voltage rises', 'the current increases', 'they are in parallel'),
    ('Two resistors of 4 Ω each are connected in parallel. The equivalent resistance is:', '2 Ω', '8 Ω', '4 Ω', '16 Ω'),
]
c11s3_why = [
    ('Why is a series arrangement not used for domestic circuits?', 'If one appliance fails, the circuit breaks and all stop working; each appliance cannot get the full voltage or be switched separately; the total resistance is large.', '1 mark each (any two).'),
    ('Why does the equivalent resistance of resistors in parallel decrease as more resistors are added?', 'Each new resistor provides an extra path for the current, so more total current flows for the same voltage.', '2 marks.'),
]
c11s3_ar = [
    ('In a parallel circuit, if one bulb fuses, the others keep glowing.', 'Each bulb has its own path to the supply.', 'a', 'R explains A.'),
    ('The equivalent resistance of resistors in series is greater than any individual resistance.', 'In series, resistances add up.', 'a', 'R explains A.'),
    ('In a series circuit, the potential difference across each resistor is the same.', 'In a series circuit, the current is the same in each resistor.', 'd', 'A is false; R is true.'),
]

c11s4_defs = [
    ('the heating effect of current', 'the production of heat in a resistor when current flows through it'),
    ('Joule\'s law of heating', 'the law that the heat produced in a resistor is H = I²Rt'),
    ('electric power', 'the rate at which electrical energy is consumed or dissipated'),
    ('one watt', 'the power of a device that consumes 1 joule of energy per second (1 V × 1 A)'),
    ('one kilowatt hour', 'the energy used by a 1 kW appliance in one hour, equal to 3.6 × 10⁶ J'),
    ('an electric fuse', 'a safety device with a wire of low melting point that melts and breaks the circuit when the current is too large'),
]
c11s4_cats = {
    'an application of the heating effect of current': ['an electric iron', 'an electric toaster', 'an electric kettle', 'a filament bulb', 'a fuse'],
    'not based on the heating effect of current': ['an electric fan motor', 'a mobile phone charger\'s transformer', 'an electric bell'],
}
c11s4_mc = [
    ('1 kWh is equal to:', '3.6 × 10⁶ J', '3.6 × 10³ J', '1000 J', '36 J'),
    ('The power of an appliance that draws 5 A at 220 V is:', '1100 W', '44 W', '225 W', '215 W'),
    ('The filament of an electric bulb is filled with:', 'chemically inactive nitrogen or argon', 'oxygen', 'air', 'hydrogen'),
    ('The heat produced in a resistor is directly proportional to the:', 'square of the current', 'current', 'square root of current', 'reciprocal of current'),
    ('A fuse wire should have:', 'a low melting point', 'a high melting point', 'very low resistance', 'high strength'),
    ('Commercial unit of electrical energy is the:', 'kilowatt hour', 'watt', 'joule', 'volt ampere'),
]
c11s4_why = [
    ('Why are bulbs filled with nitrogen or argon?', 'These gases are chemically inactive and prolong the life of the filament by preventing its oxidation.', '2 marks.'),
    ('Why does the cord of an electric heater not glow while its heating element does?', 'The cord is copper with very low resistance, so little heat is produced (H = I²Rt); the element is nichrome with high resistance.', '1 mark each.'),
    ('Why is a fuse connected in series with the live wire?', 'When excess current flows, the fuse wire melts and breaks the circuit, protecting appliances; in series it carries the whole current.', '2 marks.'),
]
c11s4_ar = [
    ('Electric heaters use nichrome coils.', 'Nichrome has high resistivity and a high melting point.', 'a', 'R explains A.'),
    ('A 100 W bulb glows brighter than a 60 W bulb when both are connected in parallel to 220 V.', 'The 100 W bulb has a lower resistance and draws more power.', 'a', 'R explains A.'),
    ('1 kWh = 3600 J.', '1 kW = 1000 W.', 'd', 'A is false (1 kWh = 3.6 × 10⁶ J); R is true.'),
]


def c11s4_heat(r):
    I = r.choice([0.5, 1, 2, 3, 4, 5])
    R = r.choice([5, 10, 20, 30, 40, 50])
    t = r.choice([10, 30, 60, 120, 300, 600])
    H = I * I * R * t
    return {'stem': f'A current of {num(I)} A flows through a resistor of {R} Ω for {t} s. How much heat is produced?', 'answer': f'{sci(H) if H >= 1e5 else num(H)} J',
            'key': f'H = I²Rt = {num(I)}² × {R} × {t} = {num(H)} J.', 'distractors': [f'{num(I * R * t)} J', f'{num(I * I * R)} J', f'{num(H * 2)} J']}


def c11s4_rating(r):
    P = r.choice([40, 60, 100, 200, 500, 1000, 1100, 1500, 2200])
    V = 220
    I = P / V
    R = V * V / P
    return {'stem': f'An electric appliance is rated {P} W, 220 V. Find the current it draws and its resistance when working.', 'answer': f'I = {sig(I, 3)} A; R = {sig(R, 3)} Ω',
            'key': f'I = P/V = {P}/220 = {sig(I, 3)} A; R = V²/P = 220²/{P} = {sig(R, 3)} Ω.'}


APPL = [('LED bulbs', 10, 4, 6), ('tube lights', 40, 3, 5), ('ceiling fans', 75, 3, 8), ('a television', 120, 1, 4), ('a refrigerator', 200, 1, 24),
        ('an electric iron', 1000, 1, 0.5), ('a geyser', 2000, 1, 1), ('an air conditioner', 1500, 1, 6), ('a water pump', 750, 1, 1), ('a mixer-grinder', 500, 1, 0.5)]


def c11s4_bill(r):
    apps = r.sample(APPL, 3)
    rate = r.choice([5, 6, 6.5, 7, 8])
    days = 30
    rows, units = [], 0
    for n, w, k, h in apps:
        units += w * k * h / 1000
        rows.append(f'{k} {n} of {w} W for {num(h)} h a day' if k > 1 else f'{n} of {w} W for {num(h)} h a day')
    U = units * days
    city = r.choice(['Indore', 'Nagpur', 'Patna', 'Kochi', 'Surat', 'Ranchi'])
    return {'stem': f'A house in {city} uses {rows[0]}, {rows[1]} and {rows[2]}. Find the energy used in {days} days in kWh and the cost at ₹{num(rate)} per unit.',
            'answer': f'{num(U, 2)} kWh; {inr(U * rate)}', 'key': f'Daily = {num(units, 3)} kWh; × {days} = {num(U, 2)} kWh; cost = {num(U, 2)} × {num(rate)} = {inr(U * rate)}.'}


def c11s4_energy(r):
    P = r.choice([100, 500, 1000, 1500, 2000])
    h = r.choice([1, 2, 3, 4, 5])
    kwh = P * h / 1000
    J = kwh * 3.6e6
    return {'stem': f'An electric heater of {P} W is used for {h} h. Find the energy consumed in kWh and in joules.', 'answer': f'{num(kwh, 2)} kWh = {sci(J)} J',
            'key': f'E = Pt = {P / 1000} kW × {h} h = {num(kwh, 2)} kWh; × 3.6 × 10⁶ = {sci(J)} J.'}


def c11s4_compare(r):
    p1, p2 = r.sample([40, 60, 100, 200], 2)
    hi = max(p1, p2)
    return {'stem': f'Two bulbs rated {p1} W, 220 V and {p2} W, 220 V are connected in parallel to a 220 V supply. Which has the lower resistance and which glows brighter? Find both resistances.',
            'answer': f'The {hi} W bulb has lower resistance and glows brighter; R = {sig(48400 / p1, 3)} Ω and {sig(48400 / p2, 3)} Ω',
            'key': f'R = V²/P: 48400/{p1} = {sig(48400 / p1, 3)} Ω, 48400/{p2} = {sig(48400 / p2, 3)} Ω. In parallel, the larger P (smaller R) glows brighter.'}


c11_hots = [
    ('Two identical resistors are first connected in series and then in parallel to the same battery. Compare the heat produced in the two cases in the same time.', 'Series: 2R, H₁ = V²t/2R. Parallel: R/2, H₂ = 2V²t/R. H₂/H₁ = 4, so parallel produces four times the heat.', '1 mark each resistance. 1 mark ratio.'),
    ('Why does a bulb in a series string of decorative lights glow dim when more bulbs are added?', 'The total resistance increases, so the current falls; the power in each bulb (I²R) decreases.', '1 mark resistance. 1 mark current. 1 mark power.'),
    ('An electric oven of 2 kW is used in a circuit with a current rating of 5 A at 220 V. What will happen, and why?', 'I = 2000/220 = 9.09 A, more than 5 A; the fuse will blow (or the circuit will overheat) — overloading.', '1 mark current. 1 mark comparison. 1 mark result.'),
    ('How can three resistors of 2 Ω, 3 Ω and 6 Ω be connected to give a total resistance of (a) 4 Ω (b) 1 Ω?', '(a) 2 Ω in series with the parallel combination of 3 Ω and 6 Ω (= 2 Ω): 4 Ω. (b) All three in parallel: 1/2 + 1/3 + 1/6 = 1 ⇒ 1 Ω.', '1½ marks each.'),
]


def c11_case(r):
    P = r.choice([1000, 1500, 2000])
    h = r.choice([1, 2])
    rate = r.choice([6, 7, 8])
    I = P / 220
    U = P * h * 30 / 1000
    return {'stem': (f'Read: Mrs Kulkarni uses an electric geyser rated {P} W, 220 V for {h} h every day in winter. Electricity costs ₹{rate} per unit.\n'
                     '(i) What current does the geyser draw? (ii) What is its resistance? (iii) How many units does it use in 30 days? (iv) What is the cost for 30 days?'),
            'answer': f'(i) {sig(I, 3)} A. (ii) {sig(48400 / P, 3)} Ω. (iii) {num(U, 1)} kWh. (iv) {inr(U * rate)}.', 'key': '1 mark each part.'}


c11_long = [
    ('State Ohm\'s law. Describe an experiment to verify it with a circuit diagram and draw the V–I graph. How does the resistance of a conductor depend on its length, area of cross-section and material?',
     'V ∝ I at constant temperature (V = IR). Circuit: cell(s), plug key, ammeter in series, nichrome wire, voltmeter across the wire; vary cells, record I and V; the V–I graph is a straight line through the origin. R ∝ l, R ∝ 1/A; R = ρl/A, ρ depends on the material.',
     '1 mark law; 2 marks experiment; 1 mark graph; 1 mark factors.'),
    ('Derive the expression for the equivalent resistance of three resistors connected (a) in series (b) in parallel. Give two advantages of parallel connection for domestic wiring.',
     'Series: same current I; V = V₁ + V₂ + V₃ = I(R₁ + R₂ + R₃) ⇒ Rs = R₁ + R₂ + R₃. Parallel: same V; I = I₁ + I₂ + I₃ = V/R₁ + V/R₂ + V/R₃ ⇒ 1/Rp = 1/R₁ + 1/R₂ + 1/R₃. Advantages: each appliance gets full voltage; appliances work independently; lower total resistance.',
     '2 marks each derivation; 1 mark advantages.'),
]

# ======================= ch12 Magnetic Effects of Electric Current
DIR = {'east': (1, 0, 0), 'west': (-1, 0, 0), 'north': (0, 1, 0), 'south': (0, -1, 0), 'vertically upwards': (0, 0, 1), 'vertically downwards': (0, 0, -1)}
NAME_OF = {v: k for k, v in DIR.items()}


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def c12s2_flem(r):
    i, b = r.sample(list(DIR), 2)
    f = cross(DIR[i], DIR[b])
    if f == (0, 0, 0):
        raise ValueError
    a = NAME_OF[f]
    wrong = [k for k in DIR if k not in (a, i, b)][:3]
    if len(wrong) < 3:
        wrong = [k for k in DIR if k != a][:3]
    return {'stem': f'A straight conductor carries current towards the {i.replace("vertically ", "")} in a uniform magnetic field directed towards the {b.replace("vertically ", "")}. Using Fleming\'s left-hand rule, find the direction of the force on the conductor.'.replace('towards the upwards', 'vertically upwards').replace('towards the downwards', 'vertically downwards'),
            'answer': a, 'key': f'Forefinger along the field ({b}), middle finger along the current ({i}); the thumb points {a}.', 'distractors': wrong}


def c12s1_rhtr(r):
    i = r.choice(['vertically upwards', 'vertically downwards'])
    p = r.choice(['east', 'west', 'north', 'south'])
    bdir = cross(DIR[i], DIR[p])
    a = NAME_OF[bdir]
    view = 'anticlockwise' if i == 'vertically upwards' else 'clockwise'
    return {'stem': f'A long straight vertical wire carries current {i}. What is the direction of the magnetic field at a point due {p} of the wire? How do the field lines look when seen from above?',
            'answer': f'Towards the {a}; concentric circles, {view} when seen from above', 'key': f'Right-hand thumb rule: thumb along the current ({i}); fingers curl {view} (seen from above), so at a point to the {p} the field is towards the {a}.'}


def c12s1_dist(r):
    d1 = r.choice([2, 3, 4, 5])
    k = r.choice([2, 3, 4])
    q = r.choice(['distance', 'current'])
    if q == 'distance':
        return {'stem': f'The magnetic field at a distance of {d1} cm from a long straight current-carrying wire is B. What will it be at {d1 * k} cm?', 'answer': f'B/{k}',
                'key': 'B ∝ 1/r for a straight wire, so increasing the distance ' + f'{k} times makes the field 1/{k}.', 'distractors': [f'{k}B', f'B/{k * k}', 'B']}
    return {'stem': f'If the current through a long straight wire is increased {k} times, how does the magnetic field at a given point change?', 'answer': f'It becomes {k} times', 'key': 'B ∝ I.',
            'distractors': [f'It becomes {k * k} times', f'It becomes 1/{k}', 'It does not change']}


c12s1_defs = [
    ('a magnetic field', 'the region around a magnet in which its force can be detected'),
    ('a magnetic field line', 'a path along which a free north pole would tend to move; the tangent at a point gives the field direction'),
    ('a solenoid', 'a coil of many circular turns of insulated copper wire wrapped closely in the shape of a cylinder'),
    ('an electromagnet', 'a strong magnet formed by placing a soft iron core inside a current-carrying solenoid'),
    ('the right-hand thumb rule', 'the rule that if the thumb of the right hand points along the current, the curled fingers give the direction of the magnetic field'),
]
c12s1_cats = {
    'a property of magnetic field lines': ['they never intersect each other', 'they are closer where the field is stronger', 'they emerge from the north pole and merge at the south pole outside a magnet', 'they form closed curves'],
    'a property of the field inside a long solenoid': ['it is uniform', 'the field lines are parallel straight lines', 'it is like that of a bar magnet'],
}
c12s1_mc = [
    ('The magnetic field lines around a straight current-carrying conductor are:', 'concentric circles', 'straight lines', 'ellipses', 'parabolas'),
    ('The magnetic field inside a long solenoid is:', 'uniform', 'zero', 'maximum at the ends', 'circular'),
    ('Two magnetic field lines never intersect because:', 'there would be two directions of the field at one point', 'they are parallel', 'they are weak', 'they are curved'),
    ('Who discovered that a current-carrying wire deflects a compass needle?', 'Hans Christian Oersted', 'Michael Faraday', 'Fleming', 'Ohm'),
    ('The strength of the field of a circular coil increases with:', 'the number of turns and the current', 'the radius only', 'the resistance', 'the length of the wire only'),
    ('The SI unit of magnetic field strength is the:', 'tesla', 'weber', 'ampere', 'gauss only'),
]
c12s1_why = [
    ('Why does a compass needle get deflected when brought near a bar magnet?', 'The compass needle is a small magnet; the magnet\'s field exerts forces on its poles.', '2 marks.'),
    ('Why is soft iron used as the core of an electromagnet?', 'Soft iron is strongly magnetised when current flows and loses its magnetism when the current is switched off.', '2 marks.'),
    ('How can the strength of the field due to a solenoid be increased?', 'Increase the current, increase the number of turns, or place a soft iron core inside.', '1 mark each (any two).'),
]
c12s1_ar = [
    ('Field lines inside a long solenoid are parallel straight lines.', 'The field inside a long solenoid is uniform.', 'a', 'R explains A.'),
    ('Magnetic field lines never intersect.', 'At a point the field has only one direction.', 'a', 'R explains A.'),
    ('The field around a straight wire is strongest far from the wire.', 'The field is inversely proportional to the distance from the wire.', 'd', 'A is false; R is true.'),
]

c12s2_defs = [
    ('Fleming\'s left-hand rule', 'the rule that if the forefinger points along the field and the middle finger along the current, the thumb gives the direction of the force on the conductor'),
    ('an electric motor', 'a device that converts electrical energy into mechanical energy'),
    ('a split ring commutator', 'a device in a motor that reverses the direction of current in the coil every half rotation'),
    ('the armature', 'the coil of many turns wound on a soft iron core in an electric motor'),
    ('brushes', 'carbon contacts that press on the split rings of a motor and connect the coil to the supply'),
]
c12s2_mc = [
    ('The force on a current-carrying conductor in a magnetic field is maximum when the current is:', 'perpendicular to the field', 'parallel to the field', 'at 45° to the field', 'zero'),
    ('The direction of the force on a conductor reverses if:', 'the direction of the current or field is reversed', 'the current is increased', 'the field is increased', 'the conductor is heated'),
    ('In an electric motor, the commutator:', 'reverses the current in the coil every half rotation', 'increases the voltage', 'makes the coil stop', 'acts as a fuse'),
    ('An electric motor converts:', 'electrical energy into mechanical energy', 'mechanical energy into electrical energy', 'heat into electricity', 'light into electricity'),
    ('Which device uses the force on a current-carrying conductor in a magnetic field?', 'a loudspeaker', 'an electric heater', 'a bulb', 'a fuse'),
]
c12s2_why = [
    ('Why does a current-carrying rod placed in a magnetic field move?', 'The field of the current interacts with the external magnetic field, producing a force (Fleming\'s left-hand rule).', '2 marks.'),
    ('Why is a split ring commutator needed in a DC motor?', 'It reverses the current in the coil after every half turn, so the force keeps rotating the coil in the same direction.', '2 marks.'),
    ('How can the force on a current-carrying conductor in a magnetic field be increased?', 'Increase the current, use a stronger magnetic field, or increase the length of the conductor in the field.', '1 mark each (any two).'),
]
c12s2_ar = [
    ('A current-carrying conductor placed parallel to a magnetic field experiences no force.', 'The force is maximum when the current is perpendicular to the field.', 'b', 'Both are true; R does not explain A directly.'),
    ('The direction of rotation of a motor can be reversed by reversing the current.', 'The force on a conductor reverses when the current reverses.', 'a', 'R explains A.'),
    ('An electric motor converts mechanical energy into electrical energy.', 'A motor uses the force on a current-carrying conductor in a magnetic field.', 'd', 'A is false; R is true.'),
]

c12s3_defs = [
    ('the live wire', 'the wire with red (or brown) insulation that carries current at high potential (220 V) in a domestic circuit'),
    ('the neutral wire', 'the wire with black (or blue) insulation, at zero potential, that completes the circuit'),
    ('the earth wire', 'the wire with green insulation, connected to a metal plate deep in the ground, that protects users from shocks'),
    ('overloading', 'the drawing of too much current by connecting too many appliances to a single socket'),
    ('a short circuit', 'direct contact between the live and neutral wires, causing a very large current'),
    ('an MCB', 'a miniature circuit breaker, a switch that automatically cuts off the current when it exceeds a safe value'),
]
c12s3_cats = {
    'the live wire': ['red insulation', 'at 220 V in India'],
    'the neutral wire': ['black insulation', 'at zero potential'],
    'the earth wire': ['green insulation', 'connected to a metal plate buried deep in the earth', 'connected to the metal body of appliances'],
}
c12s3_cats = {f'a feature of {k}': v for k, v in c12s3_cats.items()}
c12s3_mc = [
    ('In India, the domestic supply is:', '220 V AC at 50 Hz', '110 V AC at 60 Hz', '220 V DC', '50 V AC at 220 Hz'),
    ('A fuse is connected in:', 'series with the live wire', 'parallel with the neutral wire', 'the earth wire', 'parallel with the appliance'),
    ('Appliances with metal bodies are earthed so that:', 'any leakage of current goes to the earth and the user does not get a shock', 'they work faster', 'they use less power', 'they do not heat up'),
    ('The circuit for heavy appliances such as geysers usually has a current rating of:', '15 A', '5 A', '1 A', '50 A'),
    ('A short circuit occurs when:', 'the live and neutral wires touch directly', 'the fuse blows', 'too few appliances are used', 'the earth wire is connected'),
]
c12s3_why = [
    ('Why should many appliances not be connected to a single socket?', 'They draw a large total current, which may overheat the wires and cause a fire (overloading).', '2 marks.'),
    ('Why is the earth wire important for appliances like an electric iron or a refrigerator?', 'If the live wire touches the metal body, current flows to the earth through the low-resistance earth wire, so the user does not get a severe shock.', '2 marks.'),
    ('What is the function of a fuse in a domestic circuit?', 'It melts and breaks the circuit when excess current flows due to a short circuit or overloading, protecting appliances and wiring.', '2 marks.'),
]
c12s3_ar = [
    ('A fuse wire is made of a material with a low melting point.', 'It must melt quickly when excess current flows.', 'a', 'R explains A.'),
    ('Overloading can cause a fire.', 'Excess current heats the wires.', 'a', 'R explains A.'),
    ('The earth wire carries current at 220 V.', 'The earth wire has green insulation.', 'd', 'A is false; R is true.'),
]
FUSES = [1, 2, 3, 5, 10, 15, 20, 30]


def c12s3_fuse(r):
    P = r.choice([60, 100, 500, 750, 1000, 1500, 2000, 2500, 3000])
    I = P / 220
    f = min(x for x in FUSES if x >= I * 1.0 + 1e-9)
    return {'stem': f'An electric appliance is rated {P} W, 220 V. Find the current it draws. Which of these fuses is most suitable: {", ".join(f"{x} A" for x in FUSES[:-1])}?',
            'answer': f'{sig(I, 3)} A; a {f} A fuse', 'key': f'I = P/V = {P}/220 = {sig(I, 3)} A; choose the smallest standard fuse just above this: {f} A.'}


def c12s3_load(r):
    apps = r.sample([('an electric iron', 1000), ('a toaster', 800), ('a geyser', 2000), ('a heater', 1500), ('a microwave oven', 1200), ('a television', 100), ('a refrigerator', 250)], 3)
    rating = r.choice([5, 10, 15])
    P = sum(p for _, p in apps)
    I = P / 220
    over = I > rating
    return {'stem': cap(f'{", ".join(f"{n} ({p} W)" for n, p in apps[:2])} and {apps[2][0]} ({apps[2][1]} W) are switched on together in a 220 V circuit with a {rating} A fuse. Find the total current. Will the fuse blow?'),
            'answer': f'{sig(I, 3)} A; {"yes, the fuse blows (overloading)" if over else "no, the current is within the rating"}', 'key': f'Total P = {P} W; I = {P}/220 = {sig(I, 3)} A, compared with {rating} A.'}


c12_hots = [
    ('A horizontal power line carries current from east to west. What is the direction of the magnetic field (a) directly below it (b) directly above it?', '(a) South. (b) North. (Right-hand thumb rule: thumb pointing west; below the wire the field points south, above it north.)', '1½ marks each.'),
    ('placeholder', 'placeholder', 'placeholder'),
    ('Why is it dangerous to touch an electric appliance with wet hands, and how does an earth wire and fuse protect a person?', 'Wet skin has low resistance, so a large current can pass through the body. The earth wire takes leaking current to the ground, and the fuse/MCB breaks the circuit when the current becomes large.', '1 mark each.'),
    ('A student wants to make a strong electromagnet using a solenoid. Suggest three ways and explain why the core should be soft iron and not steel.', 'Increase turns, increase current, use a soft iron core. Soft iron magnetises strongly and loses magnetism when current stops; steel would stay magnetised.', '1 mark ways. 1 mark soft iron. 1 mark steel.'),
]
c12_hots[1] = ('An electron beam moving horizontally towards the north enters a magnetic field directed vertically downwards. In which direction will the beam be deflected? (Current is opposite to the direction of electron flow.)',
               'The current is towards the south. By Fleming\'s left-hand rule (field downwards, current south), the force is towards the east, so the beam is deflected towards the east.', '1 mark current direction. 1 mark rule. 1 mark answer.')


def c12_case(r):
    apps = r.sample([('a geyser', 2000), ('an electric iron', 1000), ('a refrigerator', 250), ('a television', 120), ('a room heater', 1500)], 2)
    P = sum(p for _, p in apps)
    I = P / 220
    return {'stem': (f'Read: In a flat in Pune, {apps[0][0]} ({apps[0][1]} W) and {apps[1][0]} ({apps[1][1]} W) are plugged into the same 15 A circuit at 220 V. The metal bodies are connected to a green wire, and an MCB is fitted.\n'
                     '(i) Find the total current drawn. (ii) Is the circuit overloaded? (iii) What is the purpose of the green wire? (iv) How is an MCB better than a fuse wire?'),
            'answer': f'(i) {sig(I, 3)} A. (ii) {"Yes" if I > 15 else "No"}, compared with 15 A. (iii) It is the earth wire; it carries leakage current to the earth and prevents shocks. (iv) An MCB switches off automatically and can be reset; a fuse wire must be replaced.',
            'key': '1 mark each part.'}


c12_long = [
    ('Describe the pattern of magnetic field lines due to (a) a straight current-carrying conductor (b) a circular loop (c) a solenoid. How do you find the direction of the field in each case? State two factors on which the strength of the field depends.',
     '(a) Concentric circles centred on the wire; right-hand thumb rule. (b) Circles near the wire, nearly straight lines at the centre, perpendicular to the plane of the loop. (c) Like a bar magnet; uniform parallel lines inside, one end behaves as N. Field strength increases with current and number of turns; decreases with distance from the wire.',
     '1 mark each pattern (3); 1 mark rule; 1 mark factors.'),
    ('Draw a schematic diagram of a domestic electric circuit showing the live, neutral and earth wires, fuse/MCB and two separate circuits. Explain the role of earthing and the fuse, and the causes of short circuiting and overloading.',
     'Mains → meter → main fuse/MCB → distribution box; live (red), neutral (black), earth (green); 5 A circuit for lights and fans, 15 A circuit for heavy appliances; appliances in parallel with switches in the live wire. Earthing sends leakage current to the ground; the fuse melts at excess current. Short circuit: live and neutral touch; overloading: too many appliances on one socket or a voltage surge.',
     '2 marks diagram; 1 mark earthing; 1 mark fuse; 1 mark short circuit and overloading.'),
]

# ======================= ch13 Our Environment
CHAINS = [['grass', 'grasshopper', 'frog', 'snake', 'eagle'], ['phytoplankton', 'zooplankton', 'small fish', 'large fish', 'kingfisher'],
          ['grass', 'deer', 'tiger'], ['plants', 'rabbit', 'fox', 'wolf'], ['grass', 'goat', 'human'], ['algae', 'water flea', 'small fish', 'crane'],
          ['wheat', 'mouse', 'snake', 'hawk'], ['grass', 'insects', 'lizard', 'snake', 'peacock']]
LEVEL = ['producer (first trophic level)', 'primary consumer (herbivore)', 'secondary consumer', 'tertiary consumer', 'quaternary consumer']
c13s1_defs = [
    ('an ecosystem', 'all the interacting organisms in an area together with the non-living components of their environment'),
    ('a producer', 'an organism, such as a green plant, that makes food from inorganic substances using sunlight'),
    ('a consumer', 'an organism that depends directly or indirectly on producers for food'),
    ('a decomposer', 'a micro-organism such as bacteria or fungi that breaks down dead remains and wastes into simple substances'),
    ('a food chain', 'a series of organisms in which each feeds on the one before it, showing the transfer of energy'),
    ('a food web', 'a network of interconnected food chains in an ecosystem'),
    ('a trophic level', 'each step or level of a food chain where transfer of energy occurs'),
]
c13s1_cats = {
    'a biotic component': ['plants', 'animals', 'bacteria', 'fungi'],
    'an abiotic component': ['temperature', 'rainfall', 'soil', 'sunlight', 'wind', 'minerals'],
}
c13s1_role = {
    'a producer': ['grass', 'phytoplankton', 'a mango tree', 'algae'],
    'a herbivore': ['a deer', 'a cow', 'a grasshopper', 'a rabbit'],
    'a carnivore': ['a tiger', 'a lion', 'a snake', 'an eagle'],
    'a decomposer': ['a mushroom', 'bacteria in the soil', 'bread mould'],
}
c13s1_mc = [
    ('Which of these is an artificial (man-made) ecosystem?', 'a crop field', 'a forest', 'a pond', 'a lake'),
    ('Which of these groups contains only biodegradable items?', 'grass, flowers and leather', 'grass, wood and plastic', 'fruit peels, cake and lime juice', 'plastic, glass and cake'),
    ('The flow of energy in a food chain is:', 'unidirectional', 'bidirectional', 'cyclic', 'random'),
    ('Decomposers are important because they:', 'replenish the soil by breaking down dead matter', 'make food by photosynthesis', 'are herbivores', 'eat carnivores'),
    ('Which organisms occupy the first trophic level in all food chains?', 'producers', 'herbivores', 'carnivores', 'decomposers'),
]
c13s1_why = [
    ('What will happen if we kill all the organisms at one trophic level?', 'The food chain breaks: organisms of the next level starve and organisms of the previous level may increase too much, upsetting the balance.', '1 mark each.'),
    ('Why is an aquarium called an artificial ecosystem?', 'It is made by humans, with living organisms (fish, plants) and non-living components (water, light, air), and needs human care.', '2 marks.'),
    ('Why do food chains usually have only three or four trophic levels?', 'Only about 10% of energy passes to the next level, so very little energy is left after four levels.', '2 marks.'),
]
c13s1_ar = [
    ('Green plants are called producers.', 'They make food from inorganic substances using sunlight.', 'a', 'R explains A.'),
    ('The flow of energy in a food chain is unidirectional.', 'Energy captured by plants does not return to the Sun.', 'a', 'R explains A.'),
    ('Decomposers are at the first trophic level.', 'Decomposers break down dead matter.', 'd', 'A is false; R is true.'),
]


def c13s1_level(r):
    ch = r.choice(CHAINS)
    i = r.randrange(len(ch))
    a = LEVEL[i]
    wrong = [x for x in LEVEL[:max(len(ch), 4)] if x != a][:3]
    return {'stem': f'In the food chain {" → ".join(ch)}, what is the role of the {ch[i]}?', 'answer': a, 'key': f'Position {i + 1} in the chain: {a}.', 'distractors': wrong}


def c13s1_order(r):
    ch = r.choice([c for c in CHAINS if len(c) >= 4])
    sh = ch[:]
    while sh == ch:
        r.shuffle(sh)
    return {'stem': f'Arrange these into a food chain: {", ".join(sh)}. Name the producer and the top consumer.', 'answer': f'{" → ".join(ch)}; producer: {ch[0]}; top consumer: {ch[-1]}',
            'key': 'Start with the producer and follow "is eaten by".'}


def c13s2_ten(r):
    ch = r.choice(CHAINS)
    E = r.choice([1000, 5000, 10000, 20000, 50000, 100000])
    i = r.randint(1, len(ch) - 1)
    e = E * 0.1 ** i
    return {'stem': f'In the food chain {" → ".join(ch)}, the producers ({ch[0]}) capture {E} kJ of energy. Using the 10 percent law, how much energy is available to the {ch[i]}?', 'answer': f'{num(e, 3)} kJ',
            'key': f'Each transfer passes on 10%: {E} × (0.1)^{i} = {num(e, 3)} kJ.', 'distractors': [f'{num(e * 10, 3)} kJ', f'{num(e / 10, 4)} kJ', f'{num(E * 0.9 ** i, 2)} kJ']}


def c13s2_back(r):
    ch = r.choice([c for c in CHAINS if len(c) >= 4])
    e = r.choice([1, 2, 5, 10, 20])
    k = len(ch) - 1
    E = e * 10 ** k
    return {'stem': f'In the food chain {" → ".join(ch)}, the {ch[-1]} gets {e} kJ of energy. How much energy must have been captured by the {ch[0]}? Why does the chain not have more levels?',
            'answer': f'{E:,} kJ'.replace(',', ' ') if E >= 10000 else f'{E} kJ', 'key': f'Each level gets 10% of the previous: {e} × 10^{k} = {E} kJ. Very little energy is left for further levels.'}


c13s2_defs = [
    ('the 10 percent law', 'the rule that only about 10% of the energy at one trophic level is transferred to the next'),
    ('biological magnification', 'the increase in the concentration of harmful non-biodegradable chemicals at each higher trophic level'),
    ('a pesticide', 'a chemical used to kill pests that harm crops'),
]
c13s2_mc = [
    ('Green plants capture about what percentage of the sunlight falling on their leaves?', '1%', '10%', '50%', '100%'),
    ('Which trophic level will have the maximum concentration of a pesticide such as DDT?', 'the top carnivore', 'the producer', 'the herbivore', 'the decomposer'),
    ('Biological magnification occurs because pesticides are:', 'non-biodegradable and accumulate in fat', 'biodegradable', 'gases', 'water-soluble and excreted'),
    ('The number of individuals at higher trophic levels is smaller because:', 'less energy is available at each higher level', 'they are bigger', 'they eat less', 'they live longer'),
]
c13s2_why = [
    ('Why are human beings at the highest risk of biological magnification?', 'Humans occupy the top level in many food chains, so harmful chemicals accumulate most in our bodies.', '2 marks.'),
    ('Why is the flow of energy in an ecosystem described as unidirectional?', 'Energy moves from the Sun to producers and then to consumers; it is lost as heat at each level and does not return to the previous level.', '2 marks.'),
]
c13s2_ar = [
    ('DDT concentration is maximum in the top carnivores.', 'DDT is non-biodegradable and accumulates at each trophic level.', 'a', 'R explains A.'),
    ('Only about 10% of energy passes to the next trophic level.', 'Much energy is used for life processes and lost as heat.', 'a', 'R explains A.'),
    ('There are more tigers than deer in a forest.', 'Energy decreases at higher trophic levels.', 'd', 'A is false; R is true.'),
]

c13s3_defs = [
    ('ozone', 'a molecule of three oxygen atoms (O₃) that in the upper atmosphere shields the earth from ultraviolet radiation'),
    ('CFCs', 'chlorofluorocarbons, chemicals used in refrigerants and fire extinguishers that deplete the ozone layer'),
    ('biodegradable substances', 'substances that can be broken down by biological processes such as the action of bacteria'),
    ('non-biodegradable substances', 'substances that cannot be broken down by biological processes, such as plastics and DDT'),
    ('the Kyoto Protocol', 'an international agreement to reduce greenhouse gas emissions'),
]
c13s3_cats = {
    'biodegradable': ['vegetable peels', 'paper', 'cotton cloth', 'leather', 'dry leaves', 'cow dung'],
    'non-biodegradable': ['polythene bags', 'glass bottles', 'aluminium cans', 'DDT', 'plastic toys'],
}
c13s3_mc = [
    ('Ozone is formed in the upper atmosphere by the action of:', 'UV radiation on oxygen molecules', 'CFCs on oxygen', 'water on oxygen', 'lightning on nitrogen'),
    ('The ozone layer protects us from:', 'ultraviolet rays that cause skin cancer', 'infrared rays', 'visible light', 'radio waves'),
    ('Which of these practices helps in waste management?', 'separating biodegradable and non-biodegradable waste at home', 'burning plastic', 'throwing waste in rivers', 'using more disposable cups'),
    ('Kulhads (disposable clay cups) were replaced in trains because:', 'making them in large numbers would remove fertile topsoil', 'they were costly', 'they broke easily', 'they were plastic'),
    ('Ozone depletion is mainly caused by:', 'CFCs', 'carbon dioxide', 'oxygen', 'nitrogen'),
]
c13s3_why = [
    ('Why is damage to the ozone layer a cause for concern?', 'More UV radiation would reach the earth, causing skin cancer, cataracts and damage to plants and animals.', '2 marks.'),
    ('Why should biodegradable and non-biodegradable wastes be discarded in separate dustbins?', 'Biodegradable waste can be composted or used for biogas; non-biodegradable waste can be recycled; mixing them makes both harder.', '2 marks.'),
    ('Suggest two changes in your habits to reduce the problem of waste disposal.', 'Carry a cloth bag instead of polythene; compost kitchen waste; reuse containers; avoid disposable items.', '1 mark each (any two).'),
]
c13s3_ar = [
    ('CFCs deplete the ozone layer.', 'CFCs release chlorine that breaks down ozone molecules.', 'a', 'R explains A.'),
    ('Plastics should not be burnt.', 'Burning plastics releases toxic gases.', 'a', 'R explains A.'),
    ('Glass is biodegradable.', 'Glass can be recycled.', 'd', 'A is false; R is true.'),
]


def c13s3_waste(r):
    fam = r.choice([3, 4, 5, 6])
    kg = r.choice([0.3, 0.4, 0.5])
    bio = r.choice([50, 55, 60, 65])
    days = 30
    tot = fam * kg * days
    b = tot * bio / 100
    nm = name(r)
    return {'stem': f'{nm}\'s family of {fam} produces {num(kg)} kg of waste per person per day, of which {bio}% is biodegradable. How much non-biodegradable waste do they produce in {days} days, and what should they do with it?',
            'answer': f'{num(tot - b, 2)} kg; segregate it and send it for recycling (reduce and reuse plastics)', 'key': f'Total = {fam} × {num(kg)} × {days} = {num(tot, 1)} kg; non-biodegradable = {100 - bio}% = {num(tot - b, 2)} kg.'}


c13_hots = [
    ('In a lake, DDT concentration was 0.003 ppm in water, 0.04 ppm in zooplankton, 0.5 ppm in small fish, 2 ppm in large fish and 25 ppm in fish-eating birds. What does this show? Why is it highest in birds?', 'Biological magnification: DDT is non-biodegradable and stored in fat; it accumulates at each trophic level, so the top consumers (birds) have the most.', '1 mark term. 1 mark reason. 1 mark top level.'),
    ('If all the snakes in a grassland were killed, what would happen to the populations of frogs, grasshoppers and grass? Explain.', 'Frogs would increase (no predator), grasshoppers would decrease (more frogs eat them), and grass might increase; the ecosystem balance is upset.', '1 mark each.'),
    ('Why are decomposers called "nature\'s cleaners", and what would happen if there were no decomposers?', 'They break down dead bodies and wastes into simple substances that return to the soil; without them, dead matter would pile up and nutrients would not be recycled.', '1 mark role. 1 mark recycling. 1 mark consequence.'),
    ('A food chain has a top carnivore receiving 20 kJ. If the chain has four trophic levels, how much energy did the producer capture, and what happens to the rest?', 'Producer: 20 × 10 × 10 × 10 = 20 000 kJ. The rest is used in life processes and lost as heat at each level.', '1 mark calculation. 1 mark 10% law. 1 mark heat loss.'),
]


def c13_case(r):
    ch = r.choice([c for c in CHAINS if len(c) >= 4])
    E = r.choice([10000, 20000, 50000])
    return {'stem': (f'Read: A student studying a grassland near Kanha recorded the food chain {" → ".join(ch)}. The producers ({ch[0]}) capture {E} kJ of solar energy.\n'
                     f'(i) Which organism is the producer, and which is the top consumer? (ii) How much energy reaches the {ch[2]}? (iii) If a pesticide is sprayed on the {ch[0]}, which organism will have the highest concentration of it? (iv) Why do food chains rarely have more than four or five levels?'),
            'answer': f'(i) {cap(ch[0])}; {ch[-1]}. (ii) {num(E * 0.01, 2)} kJ. (iii) The {ch[-1]} (biological magnification). (iv) Only about 10% of energy passes to each next level, so little energy remains.',
            'key': '1 mark each part.'}


c13_long = [
    ('What is an ecosystem? Describe its components. Explain the flow of energy in an ecosystem with the 10 percent law, and state why the flow of energy is unidirectional.',
     'An ecosystem: living organisms plus physical environment interacting. Biotic: producers, consumers (herbivores, carnivores, omnivores), decomposers. Abiotic: temperature, rainfall, wind, soil, minerals. Green plants capture about 1% of sunlight; at each level about 10% is passed on and the rest used or lost as heat. Energy does not return to the previous level, so flow is unidirectional.',
     '1 mark definition; 1 mark components; 2 marks energy flow; 1 mark unidirectional.'),
    ('What is biological magnification? Explain with an example. How is ozone formed and depleted? Suggest ways to manage garbage at home and school.',
     'Increase of non-biodegradable chemicals like DDT at higher trophic levels (water → plankton → fish → birds → humans). Ozone: O₂ split by UV into O atoms; O + O₂ → O₃. CFCs release chlorine that destroys ozone. Garbage: segregation, composting, recycling, reducing plastics, reusing items.',
     '2 marks magnification; 1 mark ozone; 2 marks waste management.'),
]


FAMILIES = {
    S + '09-st1': [TERM(c9s1_defs), DEF(c9s1_defs), CLS(c9s1_img, 'Which image is {}?', C='C2', D='D2', verb='is the image'), CLS(c9s1_use, 'Which of these uses {}?', C='C1', D='D2', verb='uses'),
                   MC(c9s1_mc, C='C1', D='D2'), SA(c9s1_why), ARF(c9s1_ar), G('C3', 'D1', 'numerical', c9s1_RF), G('C2', 'D2', 'mcq', c9s1_RF), SA(c9_hots[3:], C='C4', D='D4', type='multi_step'),
                   LONG(c9_long[:1], C='C4', D='D4'), SORT(c9s1_use, 'Sort these by the mirror used, {A} or {B}: {L}.', C='C3', D='D3', n=(1, 2))],
    S + '09-st2': [TERM(c9s2_defs), DEF(c9s2_defs), MC(c9s2_mc, C='C1', D='D2'), SA(c9s2_why), ARF(c9s2_ar), G('C3', 'D3', 'numerical', c9s2_v), G('C2', 'D3', 'mcq', c9s2_v),
                   G('C3', 'D4', 'multi_step', c9s2_mirror), G('C4', 'D4', 'multi_step', c9s2_m), G('C4', 'D4', 'long', c9s2_long)],
    S + '09-st3': [TERM(c9s3_defs), DEF(c9s3_defs), MC(c9s3_mc, C='C1', D='D2'), SA(c9s3_why), ARF(c9s3_ar), G('C3', 'D2', 'numerical', c9s3_speed), G('C2', 'D2', 'mcq', c9s3_speed),
                   G('C3', 'D3', 'numerical', c9s3_rel), G('C2', 'D2', 'mcq', c9s3_denser), G('C3', 'D3', 'numerical', c9s3_vv), SA(c9_hots[2:3], C='C4', D='D4', type='multi_step'),
                   LONG(c9_long[1:2], C='C4', D='D4'), G('C4', 'D4', 'multi_step', c9s3_vv)],
    S + '09-st4': [TERM(c9s4_defs), DEF(c9s4_defs), CLS(c9s4_img, 'Which image is {}?', C='C2', D='D2', verb='is the image'), MC(c9s4_mc, C='C1', D='D2'), SA(c9s4_why), ARF(c9s4_ar),
                   G('C3', 'D2', 'numerical', c9s4_power), G('C2', 'D2', 'mcq', c9s4_power), G('C3', 'D3', 'numerical', c9s4_v), G('C3', 'D4', 'multi_step', c9s4_lens), G('C3', 'D3', 'numerical', c9s4_combo),
                   SA(c9_hots[:2], C='C4', D='D4', type='multi_step'), G('C4', 'D3', 'case', c9_case, gap='G7'), G('C4', 'D4', 'long', c9s4_long), G('C4', 'D4', 'multi_step', c9s4_combo)],
    S + '10-st1': [TERM(c10s1_defs), DEF(c10s1_defs), CLS(c10s1_cats, 'Which part of the eye {}?', C='C2', D='D2', verb='—'), MC(c10s1_mc, C='C1', D='D2'), SA(c10s1_why), ARF(c10s1_ar),
                   G('C3', 'D3', 'numerical', c10s1_acc), G('C4', 'D4', 'multi_step', c10s1_acc), LONG(c10_long[:1], C='C4', D='D4')],
    S + '10-st2': [TERM(c10s2_defs + c10s1_defs[6:8]), DEF(c10s2_defs), CLS(c10s2_cats, 'Which of these is {}?', C='C2', D='D2'), MC(c10s2_mc, C='C1', D='D2'), SA(c10s2_why), ARF(c10s2_ar),
                   G('C3', 'D3', 'numerical', c10s2_myo), G('C3', 'D3', 'numerical', c10s2_hyp), G('C2', 'D2', 'mcq', c10s2_mcq), G('C4', 'D4', 'multi_step', c10s2_hyp),
                   SA(c10_hots[:1], C='C4', D='D4', type='multi_step'), G('C4', 'D3', 'case', c10_case, gap='G7'), G('C4', 'D4', 'long', c10s2_long),
                   SORT(c10s2_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3', n=(1, 2))],
    S + '10-st3': [TERM(c10s3_defs), DEF(c10s3_defs), MC(c10s3_mc, C='C1', D='D2'), SA(c10s3_why), ARF(c10s3_ar), G('C2', 'D2', 'mcq', c10s3_col), G('C3', 'D2', 'explain', c10s3_order),
                   LONG(c10_long[1:2], C='C4', D='D4'), SA([('Two beams of red and violet light enter a prism. Which emerges with the larger deviation, and what does this tell you about their speeds in glass?', 'Violet is deviated more; it travels more slowly in glass (higher refractive index) than red.', '1 mark violet. 1 mark slower. 1 mark refractive index.')], C='C4', D='D4', type='multi_step')],
    S + '10-st4': [TERM(c10s4_defs), DEF(c10s4_defs), CLS(c10s4_cats, 'Which of these is {}?', C='C2', D='D2'), MC(c10s4_mc, C='C1', D='D2'), SA(c10s4_why), ARF(c10s4_ar),
                   SORT(c10s4_cats, 'Classify these as {A} or {B}: {L}.', C='C3', D='D3', n=(2, 3)), SA(c10_hots[1:], C='C4', D='D4', type='multi_step'), CASE(c10_case_s, C='C4', D='D3'),
                   LONG(c10_long[2:], C='C4', D='D4'), CLS(c10s4_cats, 'Which of these is {}?', C='C3', D='D3', neg=True)],
    S + '11-st1': [TERM(c11s1_defs), DEF(c11s1_defs), CLS(c11s1_cats, 'Which of these is {} in a circuit?', C='C1', D='D2', verb='is'), MC(c11s1_mc, C='C1', D='D2'), SA(c11s1_why), ARF(c11s1_ar),
                   G('C3', 'D2', 'numerical', c11s1_I), G('C3', 'D2', 'numerical', c11s1_W), G('C3', 'D3', 'numerical', c11s1_q), G('C2', 'D2', 'mcq', c11s1_I), G('C4', 'D4', 'multi_step', c11s1_q)],
    S + '11-st2': [TERM(c11s2_defs), DEF(c11s2_defs), CLS(c11s2_cats, 'Which of these is {}?', C='C1', D='D2'), MC(c11s2_mc, C='C1', D='D2'), SA(c11s2_why), ARF(c11s2_ar),
                   G('C3', 'D1', 'numerical', c11s2_ohm), G('C2', 'D2', 'mcq', c11s2_ohm), G('C3', 'D3', 'numerical', c11s2_rho), G('C2', 'D3', 'mcq', c11s2_scale), G('C4', 'D4', 'multi_step', c11s2_rho),
                   LONG(c11_long[:1], C='C4', D='D4')],
    S + '11-st3': [TERM(c11s3_defs + c11s2_defs[:2]), DEF(c11s3_defs), MC(c11s3_mc, C='C1', D='D2'), SA(c11s3_why), ARF(c11s3_ar), G('C3', 'D3', 'numerical', c11s3_series),
                   G('C3', 'D3', 'numerical', c11s3_par), G('C2', 'D2', 'mcq', c11s3_eq), G('C3', 'D4', 'multi_step', c11s3_mix), G('C3', 'D3', 'numerical', c11s3_n), G('C4', 'D4', 'multi_step', c11s3_mix),
                   SA(c11_hots[3:], C='C4', D='D5', type='multi_step'), G('C4', 'D4', 'long', c11s3_long), LONG(c11_long[1:], C='C4', D='D4')],
    S + '11-st4': [TERM(c11s4_defs), DEF(c11s4_defs), CLS(c11s4_cats, 'Which of these is {}?', C='C2', D='D2'), MC(c11s4_mc, C='C1', D='D2'), SA(c11s4_why), ARF(c11s4_ar),
                   G('C3', 'D2', 'numerical', c11s4_heat), G('C3', 'D2', 'numerical', c11s4_rating), G('C3', 'D3', 'numerical', c11s4_energy), G('C3', 'D4', 'multi_step', c11s4_bill),
                   G('C4', 'D3', 'explain', c11s4_compare), SA(c11_hots[:3], C='C4', D='D4', type='multi_step'), G('C4', 'D3', 'case', c11_case, gap='G7'), G('C2', 'D2', 'mcq', c11s4_heat)],
    S + '12-st1': [TERM(c12s1_defs), DEF(c12s1_defs), CLS(c12s1_cats, 'Which of these is {}?', C='C2', D='D2'), MC(c12s1_mc, C='C1', D='D2'), SA(c12s1_why), ARF(c12s1_ar),
                   G('C3', 'D3', 'explain', c12s1_rhtr), G('C2', 'D2', 'mcq', c12s1_dist), SA(c12_hots[:1] + c12_hots[3:], C='C4', D='D4', type='multi_step'), LONG(c12_long[:1], C='C4', D='D4'),
                   G('C4', 'D4', 'multi_step', c12s1_rhtr)],
    S + '12-st2': [TERM(c12s2_defs), DEF(c12s2_defs), MC(c12s2_mc, C='C1', D='D2'), SA(c12s2_why), ARF(c12s2_ar), G('C3', 'D3', 'mcq', c12s2_flem), G('C2', 'D2', 'mcq', c12s2_flem),
                   SA(c12_hots[1:2], C='C4', D='D4', type='multi_step'),
                   SA([('A straight wire carrying current from west to east is placed in a magnetic field pointing north. Find the direction of the force. What happens if both current and field are reversed?', 'Force is vertically upwards (Fleming\'s left-hand rule). If both are reversed, the force direction stays the same (upwards).', '1 mark force. 1 mark rule. 1 mark both reversed.')], C='C4', D='D4', type='multi_step'),
                   SA([('Name the rule used to find the direction of force on a current-carrying conductor in a magnetic field and state it.', 'Fleming\'s left-hand rule: stretch the thumb, forefinger and middle finger of the left hand mutually perpendicular; forefinger along the field, middle finger along the current, thumb gives the force (motion).', '1 mark name. 1 mark statement.')], C='C3', D='D2')],
    S + '12-st3': [TERM(c12s3_defs), DEF(c12s3_defs), CLS(c12s3_cats, 'Which of these is {}?', C='C1', D='D2'), MC(c12s3_mc, C='C1', D='D2'), SA(c12s3_why), ARF(c12s3_ar),
                   G('C3', 'D3', 'numerical', c12s3_fuse), G('C3', 'D3', 'numerical', c12s3_load), G('C4', 'D4', 'multi_step', c12s3_load), SA(c12_hots[2:3], C='C4', D='D4', type='multi_step'),
                   G('C4', 'D3', 'case', c12_case, gap='G7'), LONG(c12_long[1:], C='C4', D='D4')],
    S + '13-st1': [TERM(c13s1_defs), DEF(c13s1_defs), CLS(c13s1_cats, 'Which of these is {} of an ecosystem?', C='C1', D='D1'), CLS(c13s1_role, 'Which of these is {}?', C='C2', D='D2'), MC(c13s1_mc, C='C1', D='D2'),
                   SA(c13s1_why), ARF(c13s1_ar), G('C2', 'D2', 'mcq', c13s1_level), G('C3', 'D3', 'explain', c13s1_order), SORT(c13s1_role, 'Classify these organisms as {A} or {B}: {L}.', C='C3', D='D2', n=(1, 3)),
                   SA(c13_hots[1:3], C='C4', D='D4', type='multi_step'), LONG(c13_long[:1], C='C4', D='D4'), G('C4', 'D3', 'case', c13_case, gap='G7')],
    S + '13-st2': [TERM(c13s2_defs + c13s1_defs[:2]), DEF(c13s2_defs), MC(c13s2_mc, C='C1', D='D2'), SA(c13s2_why), ARF(c13s2_ar), G('C3', 'D2', 'numerical', c13s2_ten), G('C2', 'D2', 'mcq', c13s2_ten),
                   G('C3', 'D3', 'numerical', c13s2_back), SA(c13_hots[:1] + c13_hots[3:], C='C4', D='D4', type='multi_step'), G('C4', 'D4', 'multi_step', c13s2_back)],
    S + '13-st3': [TERM(c13s3_defs), DEF(c13s3_defs), CLS(c13s3_cats, 'Which of these is {}?', C='C1', D='D1'), MC(c13s3_mc, C='C1', D='D2'), SA(c13s3_why), ARF(c13s3_ar),
                   SORT(c13s3_cats, 'Classify these wastes as {A} or {B}: {L}.', C='C3', D='D2'), G('C3', 'D2', 'numerical', c13s3_waste),
                   SA([('A town decides to ban single-use plastic bags. Give two environmental benefits and suggest two alternatives.', 'Benefits: less soil and water pollution, fewer drains blocked, fewer animal deaths. Alternatives: cloth or jute bags, paper bags.', '1 mark each benefit; 1 mark alternatives.')], C='C4', D='D4', type='multi_step'),
                   LONG(c13_long[1:], C='C4', D='D4'), CLS(c13s3_cats, 'Which of these is {}?', C='C3', D='D3', neg=True)],
}
