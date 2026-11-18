"""CBSE class 8 science (NCERT Curiosity) families, chapters 10-13."""
from __future__ import annotations

from qbank import name, two_names, num, num_distractors, mcq
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, cap, sig

S = 'cbse-g8-science-ch'

# ======================= ch10 Light: Mirrors and Lenses
c10s1_defs = [
    ('reflection of light', 'the bouncing back of light when it falls on a smooth, shiny surface'),
    ('the incident ray', 'the ray of light that falls on a reflecting surface'),
    ('the reflected ray', 'the ray of light that bounces back from a reflecting surface'),
    ('the normal', 'the line drawn perpendicular to the reflecting surface at the point where the ray falls'),
    ('the angle of incidence', 'the angle between the incident ray and the normal'),
    ('the angle of reflection', 'the angle between the reflected ray and the normal'),
    ('diffuse reflection', 'reflection from a rough surface in which parallel rays are scattered in different directions'),
    ('regular reflection', 'reflection from a smooth surface such as a mirror in which parallel rays remain parallel'),
]


def c10s1_r(r):
    i = r.choice([15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    return {'stem': f'A ray of light falls on a plane mirror at an angle of incidence of {i}°. What is the angle of reflection?', 'answer': f'{i}°',
            'key': f'By the law of reflection, angle of reflection = angle of incidence = {i}°.', 'distractors': [f'{90 - i}°', f'{2 * i}°', f'{180 - i}°']}


def c10s1_mirror(r):
    m = r.choice([20, 25, 30, 35, 40, 50, 55, 60, 65, 70])
    i = 90 - m
    return {'stem': f'A ray of light makes an angle of {m}° with the surface of a plane mirror. Find the angle of incidence and the angle between the incident and reflected rays.',
            'answer': f'Angle of incidence {i}°; angle between rays {2 * i}°',
            'key': f'Angles are measured from the normal: i = 90° − {m}° = {i}°; r = {i}°; angle between rays = {i} + {i} = {2 * i}°.',
            'distractors': [f'Angle of incidence {m}°; angle between rays {2 * m}°', f'Angle of incidence {i}°; angle between rays {i}°', f'Angle of incidence {m}°; angle between rays {180 - m}°'],
            'gap': 'G2'}


def c10s1_between(r):
    t = r.choice([40, 50, 60, 70, 80, 90, 100, 110, 120])
    return {'stem': f'The angle between the incident ray and the reflected ray is {t}°. What is the angle of incidence?', 'answer': f'{t // 2}°',
            'key': f'Angle between rays = i + r = 2i, so i = {t} ÷ 2 = {t // 2}°.', 'distractors': [f'{t}°', f'{90 - t // 2}°', f'{180 - t}°']}


c10s1_mc = [
    ('According to the laws of reflection, the incident ray, the reflected ray and the normal:', 'all lie in the same plane', 'are all parallel', 'all lie in different planes', 'are always perpendicular to each other'),
    ('A ray falls along the normal on a plane mirror. The angle of reflection is:', '0°', '90°', '45°', '180°'),
    ('We cannot see our image in a wall painted with matt paint because:', 'it is rough and gives diffuse reflection', 'it absorbs all light', 'it is transparent', 'it gives regular reflection'),
    ('Which surface gives regular reflection?', 'A still water surface', 'A sheet of paper', 'A wooden table', 'A cloth'),
]
c10s1_why = [
    ('Why can we see objects that do not give out their own light, such as a book?', 'Light from a source falls on the book and is reflected into our eyes.', '1 mark: reflection. 1 mark: reaches eyes.'),
    ('Does diffuse reflection mean that the laws of reflection are not obeyed? Explain.', 'No. Each ray obeys the laws; the surface is rough, so normals at different points point in different directions and the reflected rays spread out.', '1 mark: laws obeyed. 1 mark: normals differ.'),
]
c10s1_ar = [
    ('The angle of reflection equals the angle of incidence.', 'This is one of the laws of reflection.', 'a', 'R states the law that gives A.'),
    ('A sheet of paper does not form images.', 'Paper gives diffuse reflection because its surface is rough.', 'a', 'R explains A.'),
    ('A ray falling along the normal is reflected at 90°.', 'The angle of incidence for such a ray is 0°.', 'd', 'A false: it is reflected back along the normal (0°); R true.'),
]

c10s2_defs = [
    ('a virtual image', 'an image that cannot be obtained on a screen, formed where rays only appear to meet'),
    ('a real image', 'an image that can be obtained on a screen, formed where rays actually meet'),
    ('lateral inversion', 'the interchange of left and right in the image formed by a plane mirror'),
    ('a kaleidoscope', 'a toy that uses inclined mirrors to form multiple images that make beautiful patterns'),
    ('a periscope', 'an instrument using two plane mirrors to see objects that are not in the direct line of sight'),
]


def c10s2_dist(r):
    who = name(r)
    d = r.choice([0.5, 1, 1.5, 2, 2.5, 3, 4])
    return {'stem': f'{who} stands {num(d)} m in front of a plane mirror. How far is {who} from the image?', 'answer': f'{num(2 * d)} m',
            'key': f'Image is as far behind the mirror as the object is in front: {num(d)} m + {num(d)} m = {num(2 * d)} m.', 'distractors': [f'{num(d)} m', f'{num(d / 2)} m', f'{num(4 * d)} m'], 'gap': 'G2'}


def c10s2_move(r):
    who = name(r)
    d = r.choice([3, 4, 5, 6])
    m = r.choice([1, 1.5, 2])
    nd = d - m
    return {'stem': f'{who} is standing {d} m from a plane mirror and walks {num(m)} m towards it. What is the new distance between {who} and the image?',
            'answer': f'{num(2 * nd)} m', 'key': f'New object distance = {d} − {num(m)} = {num(nd)} m; image distance also {num(nd)} m; total {num(2 * nd)} m.',
            'distractors': [f'{num(nd)} m', f'{num(2 * d - m)} m', f'{num(2 * d)} m']}


def c10s2_images(r):
    a = r.choice([30, 36, 45, 60, 90])
    n = 360 // a - 1
    return {'stem': f'Two plane mirrors are placed at an angle of {a}° to each other with a candle between them. How many images of the candle are formed?', 'answer': str(n),
            'key': f'Number of images = 360°/θ − 1 = 360/{a} − 1 = {n}.', 'distractors': [str(n + 1), str(n - 1 if n > 1 else n + 2), str(2 * n)]}


SYM = list('AHIMOTUVWXY')
NONSYM = list('BCDEFGJKLNPQRSZ')


def c10s2_letter(r):
    good = r.choice(SYM)
    wrong = r.sample(NONSYM, 3)
    return mcq('Which capital letter looks exactly the same when seen in a plane mirror?', good, wrong,
               f'{good} is symmetric about a vertical line, so lateral inversion does not change it.', r)


c10s2_mc = [
    ('The image formed by a plane mirror is:', 'virtual, erect and of the same size', 'real, inverted and smaller', 'real, erect and larger', 'virtual, inverted and of the same size'),
    ('"AMBULANCE" is written in reverse on the front of ambulances so that:', 'drivers ahead can read it correctly in their rear-view mirrors', 'it looks attractive', 'it can be read from inside', 'it is a code'),
    ('If you raise your right hand in front of a plane mirror, your image raises its:', 'left hand', 'right hand', 'both hands', 'no hand'),
    ('A periscope used in submarines contains:', 'two plane mirrors inclined at 45°', 'one convex lens', 'one concave mirror', 'two convex mirrors parallel to each other'),
    ('Two mirrors placed parallel to each other form:', 'an infinite number of images', 'one image', 'two images', 'no image'),
]
c10s2_why = [
    ('Why can the image in a plane mirror not be obtained on a screen?', 'It is virtual: rays only appear to come from behind the mirror; they do not actually meet there.', '1 mark: virtual. 1 mark: rays do not meet.'),
    ('Why do barbers\' shops have mirrors on opposite walls?', 'Parallel mirrors form many images, so customers can see the back of the head.', '1 mark: multiple images. 1 mark: see back.'),
]
c10s2_ar = [
    ('The word "AMBULANCE" is written as a mirror image on vehicles.', 'A plane mirror produces lateral inversion.', 'a', 'R explains A.'),
    ('The image in a plane mirror is real.', 'The image is as far behind the mirror as the object is in front.', 'd', 'A false; R true.'),
    ('A kaleidoscope forms many images.', 'Inclined mirrors produce multiple reflections.', 'a', 'R explains A.'),
]

c10s3_defs = [
    ('a concave mirror', 'a spherical mirror whose reflecting surface curves inwards like the inside of a spoon'),
    ('a convex mirror', 'a spherical mirror whose reflecting surface bulges outwards like the back of a spoon'),
    ('the principal focus of a concave mirror', 'the point where rays parallel to the principal axis meet after reflection'),
    ('a spherical mirror', 'a mirror whose reflecting surface is a part of a hollow sphere'),
]
c10s3_cats = {
    'a use of a concave mirror': ['reflector in a torch', 'shaving mirror', 'dentist\'s mirror to see teeth enlarged', 'solar cooker reflector', 'reflector in vehicle headlights'],
    'a use of a convex mirror': ['rear-view mirror of a scooter', 'mirror at sharp turns of hill roads', 'security mirror in a shop', 'side mirror of a car'],
}
c10s3_mc = [
    ('A convex mirror always forms an image that is:', 'virtual, erect and diminished', 'real, inverted and enlarged', 'real and erect', 'virtual and enlarged'),
    ('When an object is placed very close to a concave mirror, the image is:', 'virtual, erect and enlarged', 'real, inverted and diminished', 'virtual and diminished', 'not formed'),
    ('A concave mirror can form an image on a screen when the object is:', 'far from the mirror', 'very close to the mirror', 'touching the mirror', 'behind the mirror'),
    ('The back side of a shiny steel spoon behaves like a:', 'convex mirror', 'concave mirror', 'plane mirror', 'convex lens'),
    ('Rays parallel to the axis falling on a concave mirror:', 'converge to a point after reflection', 'diverge after reflection', 'pass through the mirror', 'are absorbed'),
]
c10s3_why = [
    ('Why are convex mirrors used as rear-view mirrors in vehicles?', 'They always give an erect image and cover a much wider field of view, though diminished.', '1 mark: erect. 1 mark: wide view.'),
    ('Why does a dentist use a concave mirror to examine teeth?', 'Held close to the teeth, it gives an erect and enlarged image.', '1 mark: close object. 1 mark: enlarged, erect.'),
    ('Why are concave mirrors used in solar cookers?', 'They converge sunlight to a focus, concentrating heat on the cooking pot.', '1 mark: converge. 1 mark: heat.'),
]
c10s3_ar = [
    ('Convex mirrors are used at blind turns on hill roads.', 'Convex mirrors give a wide field of view.', 'a', 'R explains A.'),
    ('A concave mirror always forms a virtual image.', 'A concave mirror converges light.', 'd', 'A false: it can form real images; R true.'),
    ('A torch uses a concave reflector.', 'A bulb at the focus of a concave mirror gives a strong parallel beam.', 'a', 'R explains A.'),
]

c10s4_defs = [
    ('a lens', 'a piece of transparent material with at least one curved surface that refracts light'),
    ('a convex lens', 'a lens that is thicker in the middle than at the edges and converges light'),
    ('a concave lens', 'a lens that is thinner in the middle than at the edges and diverges light'),
    ('refraction', 'the bending of light when it passes from one transparent medium into another'),
]
c10s4_cats = {
    'a device that uses a convex lens': ['magnifying glass', 'camera', 'microscope', 'spectacles for far-sighted people', 'projector'],
    'a device that uses a concave lens': ['spectacles for short-sighted people', 'door peephole (viewer)', 'some torches to spread light'],
}
c10s4_mc = [
    ('A magnifying glass is a:', 'convex lens', 'concave lens', 'plane mirror', 'convex mirror'),
    ('A concave lens always forms an image that is:', 'virtual, erect and diminished', 'real and inverted', 'virtual and enlarged', 'real and enlarged'),
    ('Sunlight focused by a convex lens can burn paper because:', 'the lens converges the light and heat to a point', 'the lens produces fire', 'the lens spreads the light', 'paper reflects light'),
    ('How can you tell a convex lens from a concave lens by touch?', 'A convex lens is thicker in the middle', 'A convex lens is thinner in the middle', 'Both feel the same', 'A concave lens is heavier'),
    ('When an object is far from a convex lens, the image on a screen is:', 'real, inverted and diminished', 'virtual and erect', 'virtual and enlarged', 'not formed'),
]
c10s4_why = [
    ('Why should one never look at the Sun through a convex lens?', 'The lens converges sunlight and can burn the retina and damage the eye.', '1 mark: converges. 1 mark: eye damage.'),
    ('How can you quickly find out whether a lens is convex or concave using printed letters?', 'Hold it close to the letters: a convex lens makes them look bigger, a concave lens makes them look smaller.', '1 mark: convex enlarges. 1 mark: concave diminishes.'),
]
c10s4_ar = [
    ('A convex lens is called a converging lens.', 'Parallel rays passing through a convex lens bend and meet at a point.', 'a', 'R explains A.'),
    ('A concave lens can be used to burn paper in sunlight.', 'A concave lens spreads out the rays passing through it.', 'd', 'A false; R true.'),
    ('Lenses bend light.', 'Light bends when it passes from air into glass.', 'a', 'R explains A.'),
]
c10_hots = [
    ('Gaurav wants to see a wide view of the traffic behind his scooter and also check his face closely while shaving. Which mirror should he use for each purpose? Explain.', 'Convex mirror for the scooter: wide field, erect image. Concave mirror for shaving: close to the face it gives an enlarged, erect image.', '1 mark each choice + 1 mark reasons.'),
    ('You are given a plane mirror, a concave mirror and a convex mirror, all covered so that only their reflections can be seen. How can you identify each by looking at your face?', 'Plane: same-size image at all distances. Concave: enlarged when close, inverted when far. Convex: always smaller and erect.', '1 mark each.'),
    ('A candle is placed 20 cm in front of a plane mirror. The mirror is then moved 5 cm away from the candle. By how much does the image move, and why?', 'The image moves 10 cm. The object distance becomes 25 cm, so the image is 25 cm behind the new mirror position, which is 5 cm further back: total shift 5 + 5 = 10 cm.', '1 mark: 10 cm. 2 marks: reasoning.'),
    ('Explain how a periscope works and why the mirrors are placed at 45°.', 'Light from the object hits the top mirror at 45°, turns through 90° down the tube, hits the lower mirror and turns 90° again into the eye; 45° placement makes each reflection turn light through exactly 90°.', '1 mark: path. 1 mark: 90° turns. 1 mark: 45° reason.'),
]
c10_case = [
    ('Read: At a sharp bend on a hill road near Shimla, a large curved mirror is fixed on a pole. Drivers coming from either side can see vehicles around the corner, though they look small.\n'
     '(i) Which type of mirror is used? (ii) Why do vehicles look small? (iii) Why is this mirror better than a plane mirror here? (iv) Is the image real or virtual?',
     '(i) Convex mirror. (ii) A convex mirror forms diminished images. (iii) It gives a much wider field of view. (iv) Virtual.', '1 mark each.'),
    ('Read: Ananya held a convex lens between a window and the wall of a dark room. At one position, a small, sharp, upside-down picture of the trees outside appeared on the wall.\n'
     '(i) What kind of image is formed? (ii) Can a concave lens do this? Why? (iii) What happens to the image if the lens is moved slightly? (iv) Name one device that works on this principle.',
     '(i) Real, inverted and diminished. (ii) No, a concave lens forms only virtual images. (iii) It becomes blurred. (iv) Camera / projector / eye.', '1 mark each.'),
]
c10_long = [
    ('State the laws of reflection. With a description of a ray diagram, show how an image is formed by a plane mirror and list four characteristics of this image. How many images will two mirrors at 60° form?',
     'Laws: angle of incidence = angle of reflection; incident ray, reflected ray and normal lie in one plane. Rays from the object reflect and appear to come from a point behind the mirror. Image: virtual, erect, same size, laterally inverted, as far behind as the object is in front. Images = 360/60 − 1 = 5.',
     '1 mark laws; 1 mark diagram; 2 marks characteristics; 1 mark number of images.'),
    ('Compare concave and convex mirrors and convex and concave lenses: the nature of images each can form and two uses of each.',
     'Concave mirror: real inverted (object far) or virtual erect enlarged (object close); torch reflector, shaving mirror. Convex mirror: virtual, erect, diminished; rear-view mirror, shop security. Convex lens: real inverted or virtual enlarged; magnifier, camera. Concave lens: virtual, erect, diminished; spectacles for myopia, door viewer.',
     '1¼ marks for each device (images and uses).'),
]

# ======================= ch11 Keeping Time with the Skies
c11s1_defs = [
    ('rotation of the Earth', 'the spinning of the Earth on its axis from west to east, completed in about 24 hours'),
    ('revolution of the Earth', 'the movement of the Earth around the Sun, completed in about 365¼ days'),
    ('the axis of the Earth', 'the imaginary line passing through the North and South Poles about which the Earth spins'),
    ('an equinox', 'a day around 21 March or 23 September when day and night are of nearly equal length everywhere'),
    ('a solstice', 'a day around 21 June or 22 December when the Sun is farthest north or south in the sky'),
]
c11s1_mc = [
    ('Day and night are caused by:', 'the rotation of the Earth on its axis', 'the revolution of the Earth around the Sun', 'the Moon blocking the Sun', 'clouds'),
    ('Seasons occur because:', 'the Earth\'s axis is tilted and the Earth revolves around the Sun', 'the Earth comes very close to the Sun in summer', 'the Moon changes its phases', 'the Sun moves around the Earth'),
    ('The Earth\'s axis is tilted at about ______ to the perpendicular to its orbit.', '23.5°', '45°', '90°', '0°'),
    ('The Sun appears to rise in the east because the Earth rotates:', 'from west to east', 'from east to west', 'from north to south', 'from south to north'),
    ('Around 21 June, places in India have:', 'the longest day of the year', 'the shortest day', 'equal day and night', 'no daylight'),
    ('When it is summer in India, in Australia it is:', 'winter', 'summer', 'spring', 'monsoon'),
]


def c11s1_deg(r):
    h = r.choice([1, 2, 3, 4, 5, 6, 8, 10, 12])
    return {'stem': f'Through how many degrees does the Earth turn on its axis in {h} hour{"s" if h > 1 else ""}?', 'answer': f'{15 * h}°',
            'key': f'The Earth turns 360° in 24 hours, i.e. 15° per hour; {h} × 15 = {15 * h}°.', 'distractors': [f'{24 * h}°', f'{360 // h if h > 1 else 30}°', f'{10 * h}°']}


def c11s1_time(r):
    a = r.choice([15, 30, 45, 60, 75, 90, 120, 150, 180])
    return {'stem': f'How long does the Earth take to rotate through {a}°?', 'answer': f'{num(a / 15)} hours' if a != 15 else '1 hour',
            'key': f'15° per hour, so {a} ÷ 15 = {num(a / 15)} h.', 'distractors': [f'{num(a / 10)} hours', f'{a} minutes', f'{num(a / 30)} hours']}


c11s1_why = [
    ('Why are days longer than nights in Delhi in June?', 'In June the northern hemisphere is tilted towards the Sun, so the Sun is above the horizon for a longer time.', '1 mark: tilt towards Sun. 1 mark: longer daylight.'),
    ('If the Earth\'s axis were not tilted, would there be seasons? Explain.', 'No. Sunlight would fall on each place at the same angle throughout the year and day length would not change, so seasons would not occur.', '1 mark: no. 1 mark: reason.'),
    ('Why is it hotter in summer although the Earth is not nearest to the Sun at that time?', 'Sun\'s rays fall more directly on our hemisphere and days are longer; the distance from the Sun has little effect.', '1 mark: direct rays. 1 mark: longer days.'),
]
c11s1_ar = [
    ('We have day and night.', 'The Earth rotates on its axis.', 'a', 'R explains A.'),
    ('Seasons are caused by the changing distance between the Earth and the Sun.', 'The Earth\'s axis is tilted.', 'd', 'A false: seasons are due to the tilt; R true.'),
    ('The Sun appears to move from east to west across the sky.', 'The Earth rotates from west to east.', 'a', 'R explains A.'),
]

c11s2_phases = ['new moon', 'waxing crescent', 'first quarter', 'waxing gibbous', 'full moon', 'waning gibbous', 'last quarter', 'waning crescent']
c11s2_defs = [
    ('phases of the Moon', 'the different shapes of the bright part of the Moon seen from the Earth during a month'),
    ('a lunar month', 'the time from one new moon to the next, about 29.5 days'),
    ('the new moon (Amavasya)', 'the phase when the Moon is between the Earth and the Sun and its lit side faces away from us'),
    ('the full moon (Purnima)', 'the phase when the whole sunlit face of the Moon is seen from the Earth'),
    ('waxing', 'the increase in the lit part of the Moon from new moon to full moon (Shukla Paksha)'),
    ('waning', 'the decrease in the lit part of the Moon from full moon to new moon (Krishna Paksha)'),
]


def c11s2_after(r):
    d = r.choice([(0, 0), (4, 1), (7, 2), (11, 3), (15, 4), (18, 5), (22, 6), (26, 7)])
    k = r.randint(0, 1)
    days = d[0] + k
    ph = c11s2_phases[d[1]]
    wrong = r.sample([p for p in c11s2_phases if p != ph], 3)
    if days <= 1:
        days = 29
    return mcq(f'About {days} days after a new moon, which phase of the Moon will be seen?', ph, wrong,
               f'New moon (0) → first quarter (~7 days) → full moon (~15 days) → last quarter (~22 days) → new moon (~29.5 days); day {days}: {ph}.', r)


c11s2_mc = [
    ('The Moon shines because:', 'it reflects sunlight', 'it produces its own light', 'it reflects light from the Earth only', 'it is very hot'),
    ('We always see the same face of the Moon because:', 'it takes the same time to rotate once as to revolve around the Earth', 'it does not rotate', 'the Earth does not rotate', 'it is flat'),
    ('A full moon is seen when the:', 'Earth is between the Sun and the Moon', 'Moon is between the Sun and the Earth', 'Sun is between the Earth and the Moon', 'Moon is behind the Sun'),
    ('In Shukla Paksha, the Moon is:', 'waxing', 'waning', 'not visible at all', 'always full'),
    ('About how many days are there between two full moons?', '29.5', '7', '15', '365'),
]
c11s2_why = [
    ('Why can we not see the Moon on a new-moon night?', 'The Moon is between the Earth and the Sun; its sunlit side faces away from the Earth.', '1 mark: position. 1 mark: lit side away.'),
    ('Why does the shape of the Moon appear to change though it is always a sphere?', 'Half the Moon is always lit by the Sun; as it revolves around the Earth, we see different portions of the lit half.', '1 mark: half lit. 1 mark: changing view.'),
]
c11s2_ar = [
    ('The Moon shows phases.', 'As the Moon revolves around the Earth, we see different amounts of its sunlit half.', 'a', 'R explains A.'),
    ('The Moon produces its own light.', 'We see the Moon because it reflects sunlight.', 'd', 'A false; R true.'),
    ('Festivals like Diwali fall on Amavasya.', 'On Amavasya the Moon is between the Earth and the Sun.', 'b', 'Both true; R does not explain why festivals fall then.'),
]

c11s3_defs = [
    ('a solar calendar', 'a calendar based on the time the Earth takes to go around the Sun, about 365¼ days'),
    ('a lunar calendar', 'a calendar based on the phases of the Moon, with 12 lunar months of about 354 days in a year'),
    ('a lunisolar calendar', 'a calendar with lunar months that adds an extra month from time to time to keep in step with the seasons'),
    ('a leap year', 'a year of 366 days, in which February has 29 days'),
    ('adhik maas', 'the extra month added in Indian lunisolar calendars about once every three years'),
]


def c11s3_leap(r):
    y = r.choice([1900, 2000, 2024, 2100, 2028, 2030, 2032, 2026, 2400, 2036, 2050, 2052, 1800, 2044, 2027])
    leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0
    why = ('divisible by 400' if y % 400 == 0 else 'a century year not divisible by 400' if y % 100 == 0 else 'divisible by 4' if y % 4 == 0 else 'not divisible by 4')
    return {'stem': f'Is the year {y} a leap year? Give the rule you used.', 'answer': 'Yes' if leap else 'No',
            'key': f'{y} is {why}, so it is {"" if leap else "not "}a leap year. (Rule: divisible by 4, but century years only if divisible by 400.)',
            'distractors': ['No' if leap else 'Yes', 'Only in the northern hemisphere', 'Cannot be decided']}


c11s3_mc = [
    ('A leap year is needed because the Earth takes about ______ to go around the Sun.', '365¼ days', '365 days exactly', '360 days', '354 days'),
    ('The Islamic (Hijri) calendar is an example of a:', 'lunar calendar', 'solar calendar', 'lunisolar calendar', 'star calendar'),
    ('The Gregorian calendar used for official work in India is a:', 'solar calendar', 'lunar calendar', 'lunisolar calendar', 'weekly calendar'),
    ('Most traditional Indian calendars such as the Vikram Samvat are:', 'lunisolar', 'purely lunar', 'purely solar', 'based on the stars only'),
    ('India\'s national calendar, adopted in 1957, is the:', 'Saka calendar', 'Hijri calendar', 'Julian calendar', 'Chinese calendar'),
]


def c11s3_lunar(r):
    y = r.choice([2, 3, 5, 8, 10])
    diff = 11 * y
    return {'stem': f'A lunar year is about 354 days and a solar year about 365 days. By how many days will a festival fixed by a purely lunar calendar shift in the solar calendar after {y} years?',
            'answer': f'About {diff} days earlier', 'key': f'Each year the lunar calendar falls short by 365 − 354 = 11 days; {y} × 11 = {diff} days.',
            'distractors': [f'About {diff} days later', f'About {y} days earlier', 'It does not shift']}


c11s3_why = [
    ('Why do festivals like Eid come about 11 days earlier every year in the Gregorian calendar?', 'They follow the lunar Hijri calendar, whose year (about 354 days) is about 11 days shorter than the solar year.', '1 mark: lunar calendar. 1 mark: 11-day difference.'),
    ('Why do lunisolar calendars add an extra month (adhik maas) about every three years?', '12 lunar months fall short of the solar year by about 11 days; in about three years this adds up to nearly a month, so a month is added to keep festivals in step with seasons.', '1 mark: 11 days a year. 1 mark: adds up to ~33 days.'),
]
c11s3_ar = [
    ('A leap year has 366 days.', 'The Earth takes about 365¼ days to go around the Sun.', 'a', 'The extra quarter-days add up to one day in 4 years; R explains A.'),
    ('Diwali falls in the same season every year.', 'Indian lunisolar calendars add an extra month from time to time.', 'a', 'R explains A.'),
    ('The year 1900 was a leap year.', 'Century years are leap years only if divisible by 400.', 'd', 'A false; R true.'),
]

c11s4_defs = [
    ('a constellation', 'a group of stars that appear to form a recognisable pattern in the night sky'),
    ('the Pole Star (Dhruva Tara)', 'the star that lies almost directly above the Earth\'s North Pole and appears not to move'),
    ('a light year', 'the distance light travels in one year, used to measure distances to stars'),
    ('nakshatras', 'the 27 star groups along the Moon\'s path used in Indian calendars'),
]
c11s4_mc = [
    ('The Saptarishi (Ursa Major) helps us locate the:', 'Pole Star', 'Moon', 'Sun', 'planet Mars'),
    ('Stars appear to move from east to west in the night sky because:', 'the Earth rotates from west to east', 'stars move very fast', 'the Moon pulls them', 'clouds move'),
    ('The Pole Star helps travellers find the direction:', 'north', 'south', 'east', 'west'),
    ('Orion is called ______ in India.', 'Mriga (the hunter/deer)', 'Saptarishi', 'Dhruva', 'Chandra'),
    ('The Sun is a:', 'star', 'planet', 'satellite', 'constellation'),
]
c11s4_why = [
    ('Why does the Pole Star appear not to move while other stars do?', 'It lies almost directly above the Earth\'s axis of rotation, so it stays in the same place as the Earth rotates.', '1 mark: above axis. 1 mark: no apparent motion.'),
    ('How did farmers and sailors in the past use the night sky to keep time and find direction?', 'Rising of certain stars and constellations marked seasons for sowing; the Pole Star showed the north for travel at night.', '1 mark: seasons. 1 mark: direction.'),
]
c11s4_ar = [
    ('The Pole Star can be used to find the north.', 'The Pole Star lies nearly above the North Pole.', 'a', 'R explains A.'),
    ('Stars are not seen during the day.', 'Stars disappear in the daytime.', 'c', 'A true; R false: they are present but the bright sunlight hides them.'),
]
c11_hots = [
    ('Imagine the Earth took 48 hours to rotate once but still went around the Sun in 365 days. How would day and night and the calendar change?', 'Day and night would each last about 24 hours; there would be only about 182–183 such days in a year, so a calendar would have fewer, longer days; temperature differences between day and night would be larger.', '1 mark each valid consequence (max 3).'),
    ('Rani saw a half moon high in the southern sky just after sunset, with its right side lit. Is the Moon waxing or waning? About how many days later will she see a full moon?', 'A half moon seen high in the sky at sunset is the first quarter, so it is waxing; the full moon comes about 7–8 days later.', '1 mark: waxing/first quarter. 1 mark: 7–8 days.'),
    ('Why did ancient people build calendars based on both the Sun and the Moon?', 'Lunar months are easy to count by watching phases, but seasons follow the Sun; combining both kept months easy to track while keeping festivals and farming in step with seasons.', '1 mark: Moon easy to observe. 1 mark: seasons follow Sun. 1 mark: combination.'),
]
c11_case = [
    ('Read: In a village, an elder says, "We sow wheat when the Krittika star group rises in the evening sky after the rains, and the harvest festival comes on the full moon of Vaisakh."\n'
     '(i) Which kind of calendar uses star groups and the Moon like this? (ii) Why do stars rise at different times in different seasons? (iii) What is the phase of the Moon on Purnima? (iv) Why is such a calendar useful for farmers?',
     '(i) A traditional lunisolar calendar with nakshatras. (ii) As the Earth revolves around the Sun, the night side faces different parts of the sky. (iii) Full moon. (iv) It marks seasons reliably for sowing and harvesting.',
     '1 mark each.'),
]
c11_long = [
    ('Explain how the rotation and revolution of the Earth give us the day and the year. Why do we have seasons? Describe what happens on 21 June and 22 December in the northern hemisphere.',
     'Rotation on its tilted axis in ~24 h gives day and night; revolution around the Sun in ~365¼ days gives the year. Seasons occur because the axis is tilted 23.5°, so each hemisphere gets more direct sunlight and longer days when tilted towards the Sun. 21 June: longest day, summer solstice in the north. 22 December: shortest day, winter solstice.',
     '2 marks: rotation and revolution; 1 mark: seasons; 2 marks: solstices.'),
]

# ======================= ch12 How Nature Works in Harmony
c12s1_defs = [
    ('a producer', 'an organism, usually a green plant, that makes its own food by photosynthesis'),
    ('a consumer', 'an organism that cannot make its own food and depends on other organisms for food'),
    ('a decomposer', 'an organism such as a bacterium or fungus that breaks down dead organisms and wastes'),
    ('a herbivore', 'an animal that eats only plants'),
    ('a carnivore', 'an animal that eats only other animals'),
    ('an omnivore', 'an animal that eats both plants and animals'),
    ('a scavenger', 'an animal that feeds on the dead bodies of other animals, such as a vulture'),
]
c12s1_cats = {
    'a producer': ['grass', 'mango tree', 'algae in a pond', 'wheat plant', 'phytoplankton'],
    'a herbivore': ['deer', 'cow', 'grasshopper', 'rabbit', 'goat'],
    'a carnivore': ['tiger', 'snake', 'frog', 'eagle', 'lion'],
    'an omnivore': ['crow', 'bear', 'human being', 'cockroach', 'pig'],
    'a decomposer': ['mushroom', 'bread mould', 'soil bacteria', 'yeast on rotting fruit'],
}
c12s1_mc = [
    ('Which organisms return nutrients from dead bodies to the soil?', 'Decomposers', 'Producers', 'Herbivores', 'Carnivores'),
    ('Vultures help to keep the environment clean because they are:', 'scavengers that eat dead animals', 'producers', 'herbivores', 'decomposers that make food'),
    ('Interdependence in nature means:', 'organisms depend on one another and on their surroundings', 'each organism lives alone', 'plants do not need animals', 'animals do not need plants'),
    ('Bees and flowers help each other because:', 'bees get nectar and flowers get pollinated', 'bees eat flowers', 'flowers eat bees', 'they do not interact'),
]
c12s1_why = [
    ('Why are plants called producers?', 'They make food from carbon dioxide and water using sunlight, which all other organisms depend on.', '1 mark: make food. 1 mark: others depend.'),
    ('What would happen if there were no decomposers?', 'Dead bodies and wastes would pile up and nutrients would not return to the soil, so plants would not get them.', '1 mark: wastes pile up. 1 mark: no recycling.'),
    ('Explain with one example how plants depend on animals.', 'Plants depend on bees and butterflies for pollination and on birds and animals for seed dispersal; animals also release carbon dioxide used in photosynthesis.', '1 mark: dependence named. 1 mark: example.'),
]
c12s1_ar = [
    ('Green plants are called producers.', 'Green plants make their own food by photosynthesis.', 'a', 'R explains A.'),
    ('Mushrooms are producers.', 'Mushrooms are fungi that absorb nutrients from dead matter.', 'd', 'A false; R true.'),
    ('Decomposers are important for nature.', 'Decomposers return nutrients to the soil.', 'a', 'R explains A.'),
]

c12s2_chains = [
    ['grass', 'grasshopper', 'frog', 'snake', 'eagle'],
    ['phytoplankton', 'zooplankton', 'small fish', 'big fish', 'kingfisher'],
    ['grass', 'deer', 'tiger'],
    ['wheat', 'rat', 'snake', 'hawk'],
    ['leaves', 'caterpillar', 'sparrow', 'cat'],
    ['algae', 'tadpole', 'fish', 'heron'],
    ['grass', 'goat', 'lion'],
    ['mango leaves', 'insect', 'lizard', 'snake'],
]


def c12s2_order(r):
    ch = r.choice([c for c in c12s2_chains if len(c) >= 4])
    sh = ch[:]
    while sh == ch:
        r.shuffle(sh)
    ans = ' → '.join(ch)
    return {'stem': f'Arrange these organisms in a correct food chain: {", ".join(sh)}. Identify the producer and the top consumer.',
            'answer': f'{ans}; producer: {ch[0]}; top consumer: {ch[-1]}', 'key': f'Energy flows from the plant upwards: {ans} (1 mark); producer and top consumer (1 mark).'}


def c12s2_level(r):
    ch = r.choice(c12s2_chains)
    i = r.randint(1, len(ch) - 1)
    lab = ['producer', 'primary consumer (herbivore)', 'secondary consumer', 'tertiary consumer', 'quaternary consumer']
    wrong = [l for j, l in enumerate(lab) if j != i][:3]
    return mcq(f'In the food chain {" → ".join(ch)}, the {ch[i]} is a:', lab[i], wrong, f'{cap(ch[i])} is at level {i + 1}: {lab[i]}.', r)


def c12s2_energy(r):
    E = r.choice([10000, 20000, 50000, 100000, 5000])
    ch = r.choice([c for c in c12s2_chains if len(c) >= 4])
    k = r.randint(2, len(ch) - 1)
    e = E / 10 ** k
    Es = f'{E:,}'.replace(',', ' ')
    return {'stem': f'In the food chain {" → ".join(ch)}, the {ch[0]} store {Es} J of energy. If only about 10% of energy passes to each next level, how much energy reaches the {ch[k]}?',
            'answer': f'{num(e, 3)} J', 'key': f'10% at each step: {E} × (1/10)^{k} = {num(e, 3)} J.',
            'distractors': [f'{num(e * 10, 3)} J', f'{num(e / 10, 4)} J', f'{num(E * 0.1 * k, 1)} J']}


def c12s2_remove(r):
    ch = r.choice([c for c in c12s2_chains if len(c) >= 4])
    i = r.randint(1, len(ch) - 2)
    return {'stem': f'In the food chain {" → ".join(ch)}, what would happen if all the {ch[i]}s were removed?',
            'answer': (f'The {ch[i - 1]} would {"grow unchecked (less eaten)" if i == 1 else "increase in number (fewer predators)"}, and the {ch[i + 1]} population would fall for lack of food; '
                       'the balance of the whole chain would be disturbed.'),
            'key': '1 mark: effect on level below. 1 mark: effect on level above. 1 mark: imbalance.'}


c12s2_defs = [
    ('a food chain', 'a sequence of organisms in which each one is eaten by the next, showing the flow of food and energy'),
    ('a food web', 'a network of many interconnected food chains in an ecosystem'),
    ('a trophic level', 'each step or level in a food chain'),
    ('an ecosystem', 'all the living organisms of an area together with the non-living components with which they interact'),
]
c12s2_mc = [
    ('The ultimate source of energy in almost all food chains is:', 'the Sun', 'green plants', 'water', 'decomposers'),
    ('Energy in a food chain flows:', 'in one direction, from producers to consumers', 'in both directions', 'from consumers to producers', 'in a cycle'),
    ('A food web is more stable than a single food chain because:', 'animals have other food choices if one is lost', 'it has fewer organisms', 'energy is recycled', 'there are no producers'),
    ('Food chains usually have only 3–5 levels because:', 'much energy is lost at every level', 'animals do not eat each other', 'producers are few', 'decomposers stop them'),
]
c12s2_ar = [
    ('Food chains rarely have more than five levels.', 'A large part of the energy is lost as heat at each level.', 'a', 'R explains A.'),
    ('Energy flow in a food chain is unidirectional.', 'Energy passed to a higher level does not come back to the lower level.', 'a', 'R explains A.'),
    ('A food web has only one food chain.', 'A food web is made of interconnected food chains.', 'd', 'A false; R true.'),
]

c12s3_defs = [
    ('the water cycle', 'the continuous movement of water between the Earth\'s surface and the atmosphere by evaporation, condensation and precipitation'),
    ('transpiration', 'the loss of water as vapour from the leaves of plants'),
    ('precipitation', 'water falling from clouds as rain, snow or hail'),
    ('the carbon cycle', 'the circulation of carbon between the air, living organisms, soil and oceans'),
    ('photosynthesis', 'the process by which green plants make food from carbon dioxide and water using sunlight'),
]
c12s3_cats = {
    'a process that adds carbon dioxide to the air': ['respiration of animals', 'burning of wood', 'decay of dead plants', 'burning petrol in vehicles', 'volcanic eruptions'],
    'a process that removes carbon dioxide from the air': ['photosynthesis by trees', 'dissolving of CO₂ in ocean water', 'growth of algae in a pond'],
}
c12s3_wc = {
    'a step in which water changes into vapour': ['evaporation from the sea', 'transpiration from leaves', 'drying of wet clothes'],
    'a step in which vapour changes into water or falls back': ['formation of clouds', 'rainfall', 'dew forming on grass', 'snowfall on mountains'],
}
c12s3_mc = [
    ('Clouds are formed by:', 'condensation of water vapour', 'evaporation of clouds', 'melting of ice', 'transpiration of animals'),
    ('Plants add water vapour to the air by:', 'transpiration', 'photosynthesis', 'condensation', 'precipitation'),
    ('Which process returns carbon from dead organisms to the air?', 'Decomposition', 'Photosynthesis', 'Condensation', 'Transpiration'),
    ('Burning of fossil fuels increases the amount of ______ in the air.', 'carbon dioxide', 'oxygen', 'nitrogen', 'argon'),
]
c12s3_why = [
    ('Why do cutting forests reduce rainfall in an area?', 'Fewer trees means less transpiration, so less water vapour reaches the air to form clouds.', '1 mark: transpiration. 1 mark: fewer clouds/rain.'),
    ('How do animals and plants together keep the carbon dioxide and oxygen in the air balanced?', 'Animals (and plants) release CO₂ by respiration; plants use CO₂ and release oxygen in photosynthesis.', '1 mark: respiration. 1 mark: photosynthesis.'),
]
c12s3_ar = [
    ('The amount of water on the Earth stays nearly constant.', 'Water keeps moving through the water cycle.', 'a', 'R explains A.'),
    ('Burning coal adds carbon dioxide to the air.', 'Coal is made of compounds of carbon.', 'a', 'R explains A.'),
    ('Photosynthesis adds carbon dioxide to the air.', 'Plants take in carbon dioxide to make food.', 'd', 'A false; R true.'),
]

c12s4_defs = [
    ('deforestation', 'large-scale cutting down of forests'),
    ('habitat loss', 'the destruction of the natural home of organisms'),
    ('an invasive species', 'a species brought from elsewhere that spreads and harms local species'),
    ('biodiversity', 'the variety of plants, animals and microorganisms in an area'),
    ('conservation', 'the protection and careful use of natural resources and living organisms'),
]
c12s4_cats = {
    'a human activity that harms ecosystems': ['clearing forests for farms', 'dumping plastic in rivers', 'overfishing', 'excess use of pesticides', 'filling up wetlands for buildings'],
    'an action that helps to protect ecosystems': ['planting native trees', 'setting up wildlife sanctuaries', 'rainwater harvesting', 'using compost instead of chemical fertilisers', 'reducing single-use plastics'],
}
c12s4_mc = [
    ('Excess use of pesticides harms birds of prey mainly because:', 'the pesticide passes up the food chain and builds up in them', 'birds eat pesticide packets', 'it cools the air', 'birds need pesticides'),
    ('Project Tiger was launched in India in:', '1973', '1947', '1990', '2010'),
    ('Which of these is an invasive plant that has spread widely in India?', 'Lantana', 'Neem', 'Peepal', 'Tulsi'),
    ('Vulture numbers in India fell sharply mainly because of:', 'the drug diclofenac in dead cattle they ate', 'too much rain', 'more forests', 'more food'),
]
c12s4_why = [
    ('Why is it harmful to kill all the snakes in an area with many rats?', 'Snakes eat rats; without snakes, rats would multiply and destroy crops and spread diseases.', '1 mark: predator–prey. 1 mark: rats increase.'),
    ('Why are wetlands and mangroves important for nature?', 'They provide habitat for many birds and fish, filter water, and protect coasts from floods and storm surges.', '1 mark: habitat. 1 mark: protection/filtering.'),
]
c12s4_ar = [
    ('Deforestation can lead to loss of species.', 'Forests are the habitat of many plants and animals.', 'a', 'R explains A.'),
    ('Planting a single kind of tree everywhere increases biodiversity.', 'Biodiversity means a variety of living organisms.', 'd', 'A false; R true.'),
    ('Pesticide levels are highest in top consumers.', 'Pesticides are not broken down and build up at each level of the food chain.', 'a', 'R explains A.'),
]
c12_hots = [
    ('In a grassland, deer were protected and wolves were hunted out. After some years, the grass was badly overgrazed and the deer began to starve. Explain this chain of events.', 'Without wolves, deer multiplied; too many deer ate the grass faster than it could grow; then lack of food made deer starve. Predators keep the balance.', '1 mark: deer increase. 1 mark: overgrazing. 1 mark: balance lost.'),
    ('Why do farmers in some places keep owl and kite perches in their fields?', 'Owls and kites eat rats and insects that damage crops; this natural control reduces the need for pesticides.', '1 mark: predators of pests. 1 mark: fewer pesticides.'),
    ('A pond has algae, small fish, big fish and a kingfisher. A factory releases hot water into it and much of the algae die. Predict the effect on each of the other organisms.', 'Small fish decrease for lack of food; big fish decrease next; kingfishers have less to eat and may leave. Decomposers may increase for a while.', '1 mark per correct prediction (max 3).'),
]
c12_case = [
    ('Read: In a village near the Western Ghats, a forest patch was cleared for farming. Soon, the stream nearby dried up earlier each year, monkeys began raiding crops, and the soil was washed away in heavy rains.\n'
     '(i) Why did the stream dry up earlier? (ii) Why did monkeys raid crops? (iii) Why was soil washed away? (iv) Suggest two ways to restore the balance.',
     '(i) Fewer trees, less water held in soil and less transpiration/rain. (ii) Their habitat and food were lost. (iii) Tree roots that held the soil were removed. (iv) Plant native trees; protect remaining forest; build check dams (any two).',
     '1 mark each.'),
    ('Read: A survey in a pond recorded energy stored in organisms: algae 20 000 J, insect larvae 2000 J, small fish 200 J, heron 20 J.\n'
     '(i) Write the food chain. (ii) What percentage of energy passes from one level to the next? (iii) Where does the rest of the energy go? (iv) Why are there fewer herons than insect larvae?',
     '(i) Algae → insect larvae → small fish → heron. (ii) 10%. (iii) Used in life processes and lost as heat. (iv) Very little energy reaches the top level, so it can support only a few herons.',
     '1 mark each.'),
]
c12_long = [
    ('What is a food web? Draw (describe) a food web with at least five organisms of a forest. Explain the role of producers, consumers and decomposers in it, and why energy flow is one-way.',
     'Food web: network of interconnected food chains. Example: grass and trees → deer, rabbit, insects → frog, birds → snake, tiger, eagle. Producers make food; consumers eat others; decomposers break down dead matter and return nutrients. Energy enters from the Sun and is lost as heat at each step; it is not passed back.',
     '1 mark definition; 2 marks web; 1 mark roles; 1 mark one-way flow.'),
    ('Describe the water cycle and the carbon cycle with the main processes in each. How do human activities disturb these cycles?',
     'Water: evaporation from water bodies, transpiration from plants, condensation into clouds, precipitation, run-off and groundwater. Carbon: CO₂ taken in by photosynthesis, returned by respiration, decomposition and combustion; stored in fossil fuels and oceans. Humans: deforestation and burning fossil fuels raise CO₂; paving land reduces groundwater recharge.',
     '2 marks each cycle; 1 mark human impact.'),
]

# ======================= ch13 Our Home: Earth
c13s1_defs = [
    ('the atmosphere', 'the blanket of air that surrounds the Earth'),
    ('the ozone layer', 'a layer of ozone gas in the stratosphere that absorbs most of the harmful ultraviolet rays of the Sun'),
    ('the greenhouse effect', 'the trapping of heat near the Earth\'s surface by gases such as carbon dioxide and water vapour'),
    ('the habitable zone', 'the region around a star where a planet can have liquid water on its surface'),
]
c13s1_mc = [
    ('The most abundant gas in the atmosphere is:', 'nitrogen (about 78%)', 'oxygen (about 78%)', 'carbon dioxide (about 21%)', 'argon (about 21%)'),
    ('Oxygen makes up about ______ of the air.', '21%', '78%', '1%', '50%'),
    ('About what fraction of the Earth\'s surface is covered by water?', 'About 71%', 'About 29%', 'About 50%', 'About 97%'),
    ('Most of the water on the Earth is:', 'salty water in the oceans', 'fresh water in rivers', 'water vapour in the air', 'groundwater'),
    ('Which feature protects life on the Earth from harmful UV rays?', 'The ozone layer', 'The troposphere clouds', 'The Earth\'s crust', 'The oceans'),
    ('Without the natural greenhouse effect, the Earth would be:', 'much colder', 'much hotter', 'exactly the same', 'without oceans of salt'),
]


def c13s1_air(r):
    l, b, h = r.choice([(5, 4, 3), (6, 5, 3), (8, 6, 3), (10, 8, 4), (4, 4, 3)])
    V = l * b * h
    gas, p = r.choice([('nitrogen', 78), ('oxygen', 21)])
    v = V * p / 100
    return {'stem': f'A classroom measures {l} m × {b} m × {h} m. About what volume of {gas} does the air in it contain? (Air is about 78% nitrogen and 21% oxygen by volume.)',
            'answer': f'About {num(v, 1)} m³', 'key': f'Volume of room = {V} m³; {gas} = {p}% of {V} = {num(v, 1)} m³.',
            'distractors': [f'About {num(V * (99 - p) / 100, 1)} m³', f'About {V} m³', f'About {num(v / 10, 2)} m³']}


def c13s1_water(r):
    total = r.choice([100, 1000, 500])
    fresh = 3 * total / 100
    ice = 2 * total / 100
    return {'stem': f'Imagine all the Earth\'s water is {total} litres. About 97% is salty sea water and about 3% is fresh water, of which about two-thirds is locked in ice and glaciers. How many litres of fresh water would be liquid and usable?',
            'answer': f'About {num(fresh - ice, 1)} litres', 'key': f'Fresh water = 3% of {total} = {num(fresh, 1)} L; ice ≈ 2/3 of it = {num(ice, 1)} L; liquid ≈ {num(fresh - ice, 1)} L (about 1%).',
            'distractors': [f'About {num(fresh, 1)} litres', f'About {num(ice, 1)} litres', f'About {num(97 * total / 100, 1)} litres']}


c13s1_why = [
    ('Why is the Earth the only planet in the solar system known to support life?', 'It has liquid water, an atmosphere with oxygen, a suitable temperature range, and an ozone layer and magnetic field that protect from harmful radiation.', '1 mark: water and air. 1 mark: suitable temperature/protection.'),
    ('Why is Venus very hot though Mercury is closer to the Sun?', 'Venus has a thick carbon dioxide atmosphere that traps heat by a strong greenhouse effect.', '1 mark: thick CO₂ atmosphere. 1 mark: greenhouse effect.'),
    ('Why does the Moon have very hot days and very cold nights while the Earth does not?', 'The Moon has no atmosphere to trap heat or block sunlight; the Earth\'s atmosphere moderates temperature.', '1 mark: no atmosphere on Moon. 1 mark: moderation.'),
]
c13s1_ar = [
    ('Life exists on the Earth.', 'The Earth has liquid water, air and a suitable temperature.', 'a', 'R explains A.'),
    ('The ozone layer is harmful to living beings.', 'Ozone absorbs ultraviolet radiation from the Sun.', 'd', 'A false; R true.'),
    ('Carbon dioxide helps keep the Earth warm.', 'Carbon dioxide traps heat in the atmosphere.', 'a', 'R explains A.'),
]

c13s2_layers = [('crust', 'the thin outermost solid layer on which we live'), ('mantle', 'the thick, hot layer below the crust, partly molten in places'),
                ('outer core', 'the liquid layer of iron and nickel around the inner core'), ('inner core', 'the solid, very hot centre of the Earth made of iron and nickel')]
c13s2_atm = [('troposphere', 'the lowest layer, where weather occurs and where we live'), ('stratosphere', 'the layer above the troposphere that contains the ozone layer, where jets fly'),
             ('mesosphere', 'the layer in which most meteors burn up'), ('thermosphere', 'the layer where auroras occur and the International Space Station orbits'),
             ('exosphere', 'the outermost layer that gradually merges into space')]


def c13s2_atm_f(r):
    n, d = r.choice(c13s2_atm)
    wrong = r.sample([x[0] for x in c13s2_atm if x[0] != n], 3)
    return mcq(f'Which layer of the atmosphere is {d}?', n, wrong, f'The {n} is {d}.', r)


def c13s2_earth_f(r):
    n, d = r.choice(c13s2_layers)
    wrong = [x[0] for x in c13s2_layers if x[0] != n]
    return mcq(f'Which layer of the Earth is {d}?', n, wrong, f'The {n} is {d}.', r)


def c13s2_order(r):
    ls = [x[0] for x in c13s2_atm]
    k = r.randint(3, 5)
    st = r.randint(0, 5 - k)
    seq = ls[st:st + k]
    sh = seq[:]
    while sh == seq:
        r.shuffle(sh)
    return {'stem': f'Arrange these layers of the atmosphere from the Earth\'s surface upwards: {", ".join(sh)}.', 'answer': ' → '.join(seq),
            'key': 'Order from the ground: troposphere, stratosphere, mesosphere, thermosphere, exosphere.'}


c13s2_why = [
    ('Why do aeroplanes prefer to fly in the lower stratosphere?', 'There are almost no clouds or weather disturbances there, so the flight is smooth.', '1 mark: no weather. 1 mark: smooth flight.'),
    ('Why do we see "shooting stars"?', 'Meteors entering the atmosphere burn up due to friction with air, mostly in the mesosphere, and glow.', '1 mark: friction with air. 1 mark: burning glow.'),
    ('Why is the crust compared to the skin of an apple?', 'It is extremely thin compared to the size of the Earth, just as the skin is thin compared to the apple.', '1 mark: thin. 1 mark: comparison.'),
]
c13s2_ar = [
    ('Weather changes occur in the troposphere.', 'The troposphere contains most of the water vapour and clouds.', 'a', 'R explains A.'),
    ('The inner core is liquid.', 'The outer core is made of molten iron and nickel.', 'd', 'A false: the inner core is solid; R true.'),
]

c13s3_defs = [
    ('a natural resource', 'any material from nature that is useful to humans, such as water, soil, forests and minerals'),
    ('a renewable resource', 'a resource that can be replaced naturally in a short time, such as forests or water'),
    ('a non-renewable resource', 'a resource that cannot be replaced once used up, or takes millions of years to form, such as coal'),
    ('an inexhaustible resource', 'a resource present in unlimited quantity that is not used up by human activity, such as sunlight'),
    ('rainwater harvesting', 'collecting and storing rainwater for later use or to recharge groundwater'),
    ('sustainable use', 'using resources in a way that meets present needs without harming the needs of future generations'),
]
c13s3_cats = {
    'a renewable resource': ['forests', 'fresh water', 'soil', 'wildlife', 'fish in the sea'],
    'a non-renewable resource': ['coal', 'petroleum', 'natural gas', 'iron ore', 'mica'],
    'an inexhaustible resource': ['sunlight', 'wind', 'air', 'tides'],
}
c13s3_mc = [
    ('Which of these is the best example of "reuse"?', 'Using an old glass jar to store spices', 'Throwing plastic in a bin', 'Burning dry leaves', 'Buying new bags each time'),
    ('Coal and petroleum are called fossil fuels because:', 'they were formed from the remains of living things buried millions of years ago', 'they are found in fossils only', 'they are renewable', 'they come from the Sun directly'),
    ('Which practice conserves water at home?', 'Closing the tap while brushing teeth', 'Washing cars with a running hose', 'Letting taps drip', 'Watering plants at noon'),
    ('PCRA, a body that promotes saving of fuel in India, stands for:', 'Petroleum Conservation Research Association', 'Public Car Repair Agency', 'Power Control and Regulation Act', 'Planet Care and Rescue Association'),
]
c13s3_why = [
    ('Why should we use public transport, bicycles or car pools?', 'They save petrol and diesel, which are non-renewable, and reduce air pollution.', '1 mark: saves fossil fuel. 1 mark: less pollution.'),
    ('Why are forests called renewable, yet we must conserve them?', 'They can regrow, but very slowly; if we cut them faster than they grow, they are lost along with soil, water and wildlife.', '1 mark: regrow slowly. 1 mark: overuse destroys.'),
    ('Why is solar energy a good alternative to coal for producing electricity?', 'Sunlight is inexhaustible and causes no air pollution, while coal is limited and pollutes.', '1 mark: inexhaustible. 1 mark: clean.'),
]
c13s3_ar = [
    ('Coal should be used carefully.', 'Coal is a non-renewable resource that took millions of years to form.', 'a', 'R explains A.'),
    ('Sunlight is an exhaustible resource.', 'Sunlight is available in unlimited amounts.', 'd', 'A false; R true.'),
    ('Rainwater harvesting helps to raise the groundwater level.', 'Collected rainwater can be directed into pits to recharge the ground.', 'a', 'R explains A.'),
]


def c13s3_rain(r):
    a = r.choice([50, 80, 100, 120, 150, 200])
    mm = r.choice([600, 800, 1000, 1200, 1500])
    L = a * mm / 1000 * 1000
    city = r.choice(['Jaipur', 'Chennai', 'Bhopal', 'Pune', 'Lucknow', 'Bengaluru'])
    return {'stem': f'A school roof in {city} has an area of {a} m² and the city receives {mm} mm of rain in a year. About how many litres of rainwater could be harvested in a year? (1 m³ = 1000 L)',
            'answer': f'{num(L)} litres', 'key': f'Volume = area × rainfall = {a} m² × {mm / 1000:g} m = {num(a * mm / 1000, 1)} m³ = {num(L)} L.',
            'distractors': [f'{num(a * mm)} litres', f'{num(L / 10)} litres', f'{num(a * mm / 1000, 1)} litres'], 'gap': 'G2'}


c13s4_defs = [
    ('the solar system', 'the Sun together with the planets, their moons and other bodies that move around it'),
    ('climate change', 'a long-term change in the average weather of the Earth, now mainly caused by human activities'),
    ('global warming', 'the gradual rise in the average temperature of the Earth due to an increase in greenhouse gases'),
]
c13s4_mc = [
    ('The Earth is the ______ planet from the Sun.', 'third', 'second', 'fourth', 'fifth'),
    ('Global warming is mainly caused by:', 'an increase in greenhouse gases like carbon dioxide', 'planting more trees', 'the ozone layer becoming thicker', 'the Moon moving away'),
    ('One result of global warming is:', 'melting of glaciers and a rise in sea level', 'more ice at the poles', 'fewer heat waves', 'cooler summers'),
    ('Which of these steps helps protect our planet?', 'Switching off lights and fans when not needed', 'Burning garbage in the open', 'Using more plastic bags', 'Cutting trees for firewood'),
]
c13s4_why = [
    ('Why is the Earth called a "Goldilocks planet"?', 'It is at just the right distance from the Sun—not too hot, not too cold—so water can stay liquid.', '1 mark: right distance. 1 mark: liquid water.'),
    ('How would a rise in sea level affect coastal cities like Mumbai and Kolkata?', 'Low-lying areas would flood more often, people would be displaced, and sea water could enter farmland and groundwater.', '1 mark: flooding. 1 mark: salinity/displacement.'),
]
c13s4_ar = [
    ('Global warming is a threat to coastal areas.', 'Rising temperatures melt glaciers and raise the sea level.', 'a', 'R explains A.'),
    ('The Earth is too far from the Sun to have liquid water.', 'The Earth lies in the habitable zone of the Sun.', 'd', 'A false; R true.'),
]
c13_hots = [
    ('If the Earth were as close to the Sun as Venus, predict two changes on the Earth and their effect on life.', 'Temperatures would be much higher; oceans would evaporate and liquid water would be lost; more greenhouse gases would trap heat; most life could not survive.', '1 mark per change with effect (max 3).'),
    ('Suggest a five-point plan for your school to become "green", with the resource each point saves.', 'Solar panels (electricity/coal); rainwater harvesting (water); compost pit for food waste (soil/landfill); no single-use plastics (petroleum, wildlife); tree planting and switching off unused lights (forests/electricity).', '1 mark per point with resource (max 5).'),
    ('A family uses a 1.5 kW geyser for 1 hour every day. They switch to a solar water heater. How many units (kWh) of electricity do they save in 30 days, and why does this help the planet?', '1.5 kW × 1 h × 30 = 45 kWh saved; less coal is burnt in power plants, so less CO₂ is released.', '1 mark: 45 kWh. 1 mark: reason.'),
]
c13_case = [
    ('Read: Ritu\'s school in Bhopal measured the water used in a week: 12 000 L for toilets, 4000 L for drinking and cooking, 6000 L for gardening and 2000 L lost in leaking taps.\n'
     '(i) What is the total water used? (ii) What percentage is lost through leaks? (iii) Suggest two ways to cut the water used for toilets and gardening. (iv) Why is saving fresh water important?',
     '(i) 24 000 L. (ii) 2000/24 000 × 100 ≈ 8.3%. (iii) Use dual-flush cisterns, reuse RO waste water, drip irrigation, water in the evening (any two). (iv) Usable fresh water is only about 1% of the Earth\'s water and is limited.',
     '1 mark each.'),
    ('Read: The air on the Earth is about 78% nitrogen, 21% oxygen, 0.9% argon and about 0.04% carbon dioxide. Mars has a thin air of about 95% carbon dioxide; its surface temperature can drop to −125 °C.\n'
     '(i) Which gas do we breathe in for respiration? (ii) Why can humans not breathe on Mars? (iii) Mars has a lot of CO₂—why is it still so cold? (iv) Name one other feature that makes the Earth suitable for life.',
     '(i) Oxygen. (ii) There is hardly any oxygen. (iii) Its atmosphere is very thin and it is farther from the Sun, so little heat is trapped. (iv) Liquid water / ozone layer / suitable temperature.',
     '1 mark each.'),
]
c13_long = [
    ('Describe the layers of the Earth\'s interior and the layers of the atmosphere, giving one feature of each layer.',
     'Interior: crust (thin, solid, we live on it), mantle (thick, hot, partly molten), outer core (liquid iron–nickel), inner core (solid iron–nickel, very hot). Atmosphere: troposphere (weather), stratosphere (ozone, jets), mesosphere (meteors burn), thermosphere (auroras, ISS), exosphere (merges into space).',
     '2 marks interior; 3 marks atmosphere.'),
    ('Classify natural resources with two examples each of renewable, non-renewable and inexhaustible resources. Explain the 3Rs with an example each and suggest why conservation is necessary.',
     'Renewable: forests, water; non-renewable: coal, petroleum; inexhaustible: sunlight, wind. Reduce (switch off lights), Reuse (glass jars), Recycle (paper). Conservation is needed because population is rising, many resources are limited, and overuse harms the environment and future generations.',
     '2 marks classification; 2 marks 3Rs; 1 mark need.'),
]

c11s4_apply = [
    ('A trekker is lost at night in a forest in Uttarakhand. Explain how she can use the Saptarishi to find the north.', 'Find the Saptarishi (Big Dipper); extend the line joining its two pointer stars about five times their distance to reach the Pole Star; the direction of the Pole Star is north.', '1 mark: pointer stars. 1 mark: Pole Star gives north.'),
    ('A photograph taken with the camera pointing at the Pole Star and the shutter left open for 2 hours shows circular arcs of stars around it. What angle does each arc cover, and why?', 'About 30°, because the Earth rotates 15° per hour, so in 2 hours the stars appear to turn 30° around the Pole Star.', '1 mark: 30°. 1 mark: reason.'),
    ('Orion is seen high in the evening sky in winter but not in summer. Explain.', 'As the Earth revolves around the Sun, the night side faces different directions in space; in summer Orion is in the daytime sky near the Sun and cannot be seen.', '1 mark: revolution changes night sky. 1 mark: Orion near Sun in summer.'),
]
c11s4_hots = [
    ('A star is 4 light years away. When we see it tonight, are we seeing it as it is now? Explain what this tells us about looking at the night sky.', 'No. The light left the star 4 years ago, so we see it as it was 4 years ago; looking at distant stars means looking into the past.', '1 mark: no. 1 mark: light travel time. 1 mark: looking back in time.'),
    ('Why would the Pole Star not be useful for finding direction for someone in Australia?', 'The Pole Star lies above the North Pole; from the southern hemisphere it is below the horizon and cannot be seen. People there use the Southern Cross instead.', '1 mark: below horizon. 1 mark: alternative.'),
]
c13s4_apply = [
    ('Your colony in Delhi burns dry leaves every winter. Explain two harmful effects and suggest a better practice.', 'Burning releases smoke, soot and CO₂, worsening air pollution and breathing problems and adding to global warming. Better: compost the leaves.', '1 mark: two effects. 1 mark: alternative.'),
    ('Suggest three things a class 8 student can do every day to reduce global warming.', 'Switch off fans and lights when not needed; walk, cycle or use the school bus; avoid wasting food and plastics; plant and care for trees.', '1 mark per action (max 3).'),
]
c13s4_hots = [
    ('The Moon has no atmosphere and no liquid water. Using these facts, explain why astronauts need special suits and why the Earth is unique.', 'Without air there is no oxygen, no air pressure and no protection from UV rays or temperature extremes; suits supply oxygen, pressure and protection. The Earth has air, liquid water and moderate temperature that support life.', '1 mark: suit needs. 1 mark: Earth unique features. 1 mark: link.'),
    ('Scientists say that the Earth\'s average temperature has risen by about 1 °C in the last 100 years. Why is even this small rise a concern?', 'It melts glaciers and ice sheets, raises sea level, causes more heat waves, droughts and floods, and disturbs crops and wildlife.', '1 mark per effect (max 3).'),
]

FAMILIES = {
    S + '10-st1': [TERM(c10s1_defs), DEF(c10s1_defs), MC(c10s1_mc, C='C1', D='D2'), SA(c10s1_why), ARF(c10s1_ar), G('C3', 'D1', 'numerical', c10s1_r),
                   G('C3', 'D2', 'numerical', c10s1_between), G('C3', 'D3', 'numerical', c10s1_mirror), G('C2', 'D2', 'mcq', c10s1_r),
                   G('C4', 'D4', 'multi_step', c10s1_mirror), SA(c10_hots[3:], C='C4', D='D3')],
    S + '10-st2': [TERM(c10s2_defs), DEF(c10s2_defs), MC(c10s2_mc, C='C1', D='D2'), G('C2', 'D2', 'mcq', c10s2_letter), SA(c10s2_why), ARF(c10s2_ar),
                   G('C3', 'D2', 'numerical', c10s2_dist), G('C3', 'D3', 'numerical', c10s2_images), G('C3', 'D4', 'numerical', c10s2_move),
                   SA(c10_hots[2:3], C='C4', D='D5', type='multi_step'), LONG(c10_long[:1], C='C4', D='D3'), G('C4', 'D4', 'numerical', c10s2_move)],
    S + '10-st3': [TERM(c10s3_defs), DEF(c10s3_defs), CLS(c10s3_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c10s3_mc, C='C1', D='D2'),
                   SA(c10s3_why), ARF(c10s3_ar), SORT(c10s3_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3', n=(2, 2)),
                   CLS(c10s3_cats, 'Which of the following is {}?', C='C3', D='D2', neg=True), SA(c10_hots[:2], C='C4', D='D4', type='multi_step'), CASE(c10_case[:1])],
    S + '10-st4': [TERM(c10s4_defs), DEF(c10s4_defs), CLS(c10s4_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c10s4_mc, C='C1', D='D2'),
                   SA(c10s4_why), ARF(c10s4_ar), SORT(c10s4_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3', n=(1, 2)),
                   CASE(c10_case[1:], C='C4', D='D4'), LONG(c10_long[1:], C='C4', D='D4')],
    S + '11-st1': [TERM(c11s1_defs), DEF(c11s1_defs), MC(c11s1_mc, C='C2', D='D2'), SA(c11s1_why), ARF(c11s1_ar), G('C3', 'D1', 'numerical', c11s1_deg),
                   G('C3', 'D2', 'numerical', c11s1_time), SA(c11_hots[:1], C='C4', D='D5', type='multi_step'), LONG(c11_long, C='C4', D='D4'),
                   G('C1', 'D2', 'mcq', c11s1_deg)],
    S + '11-st2': [TERM(c11s2_defs), DEF(c11s2_defs), MC(c11s2_mc, C='C1', D='D2'), G('C3', 'D2', 'mcq', c11s2_after), SA(c11s2_why), ARF(c11s2_ar),
                   SA(c11_hots[1:2], C='C4', D='D4', type='explain'), G('C3', 'D3', 'mcq', c11s2_after)],
    S + '11-st3': [TERM(c11s3_defs), DEF(c11s3_defs), MC(c11s3_mc, C='C1', D='D2'), G('C3', 'D2', 'short', c11s3_leap), G('C3', 'D3', 'numerical', c11s3_lunar),
                   SA(c11s3_why), ARF(c11s3_ar), SA(c11_hots[2:], C='C4', D='D3', type='multi_step'), CASE(c11_case), G('C4', 'D4', 'numerical', c11s3_lunar)],
    S + '11-st4': [TERM(c11s4_defs), DEF(c11s4_defs), MC(c11s4_mc, C='C1', D='D2'), SA(c11s4_why), ARF(c11s4_ar), SA(c11s4_apply, C='C3', D='D3'), SA(c11s4_hots, C='C4', D='D4', type='multi_step')],
    S + '12-st1': [TERM(c12s1_defs), DEF(c12s1_defs), CLS(c12s1_cats, 'Which of the following is {}?', C='C1', D='D2'), MC(c12s1_mc, C='C2', D='D2'),
                   SA(c12s1_why), ARF(c12s1_ar), SORT(c12s1_cats, 'Classify these organisms as {A} or {B}: {L}.', C='C3', D='D2', n=(2, 2)),
                   CLS(c12s1_cats, 'Which of the following is {}?', C='C3', D='D3', neg=True)],
    S + '12-st2': [TERM(c12s2_defs), DEF(c12s2_defs), MC(c12s2_mc, C='C1', D='D2'), G('C2', 'D2', 'mcq', c12s2_level), ARF(c12s2_ar),
                   G('C3', 'D3', 'explain', c12s2_order), G('C3', 'D2', 'numerical', c12s2_energy), G('C3', 'D4', 'multi_step', c12s2_energy),
                   G('C4', 'D3', 'explain', c12s2_remove), G('C4', 'D4', 'multi_step', c12s2_remove), SA(c12_hots, C='C4', D='D4', type='multi_step'),
                   CASE(c12_case[1:]), LONG(c12_long[:1], C='C4', D='D4')],
    S + '12-st3': [TERM(c12s3_defs), DEF(c12s3_defs), CLS(c12s3_cats, 'Which of the following is {}?', C='C2', D='D2'), CLS(c12s3_wc, 'Which of the following is {}?', C='C3', D='D2'),
                   MC(c12s3_mc, C='C1', D='D2'), SA(c12s3_why), ARF(c12s3_ar), SORT(c12s3_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3', n=(1, 2)),
                   LONG(c12_long[1:], C='C4', D='D3')],
    S + '12-st4': [TERM(c12s4_defs), DEF(c12s4_defs), CLS(c12s4_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c12s4_mc, C='C1', D='D2'),
                   SA(c12s4_why), ARF(c12s4_ar), SORT(c12s4_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3'),
                   CLS(c12s4_cats, 'Which of the following is {}?', C='C3', D='D2', neg=True), CASE(c12_case[:1])],
    S + '13-st1': [TERM(c13s1_defs), DEF(c13s1_defs), MC(c13s1_mc, C='C1', D='D2'), SA(c13s1_why), ARF(c13s1_ar), G('C3', 'D2', 'numerical', c13s1_air),
                   G('C3', 'D4', 'multi_step', c13s1_water), CASE(c13_case[1:]), SA(c13_hots[:1], C='C4', D='D4', type='multi_step'), G('C4', 'D3', 'numerical', c13s1_air)],
    S + '13-st2': [G('C1', 'D2', 'mcq', c13s2_atm_f), G('C1', 'D1', 'mcq', c13s2_earth_f), SA(c13s2_why), ARF(c13s2_ar), G('C3', 'D2', 'short', c13s2_order),
                   LONG(c13_long[:1], C='C4', D='D3'), G('C2', 'D2', 'mcq', c13s2_atm_f)],
    S + '13-st3': [TERM(c13s3_defs), DEF(c13s3_defs), CLS(c13s3_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c13s3_mc, C='C1', D='D2'),
                   SA(c13s3_why), ARF(c13s3_ar), SORT(c13s3_cats, 'Classify these resources as {A} or {B}: {L}.', C='C3', D='D3', n=(2, 2)),
                   CLS(c13s3_cats, 'Which of the following is {}?', C='C3', D='D2', neg=True), G('C3', 'D4', 'numerical', c13s3_rain),
                   G('C4', 'D4', 'multi_step', c13s3_rain), SA(c13_hots[1:], C='C4', D='D4', type='multi_step'), CASE(c13_case[:1]), LONG(c13_long[1:], C='C4', D='D4')],
    S + '13-st4': [TERM(c13s4_defs + c13s1_defs[:2]), DEF(c13s4_defs), MC(c13s4_mc, C='C1', D='D2'), SA(c13s4_why), ARF(c13s4_ar), SA(c13s4_apply, C='C3', D='D3'), SA(c13s4_hots, C='C4', D='D4', type='multi_step')],
}


c12s1_hots = [
    ('In a garden, the gardener sprays a strong insecticide that kills all insects, including bees and butterflies. Predict what will happen to the fruit and vegetable plants next season, and why.', 'Fewer flowers will be pollinated, so fewer fruits and seeds form; birds and frogs that eat insects will also decline.', '1 mark: pollination falls. 1 mark: less fruit. 1 mark: effect on other animals.'),
    ('Which would be more harmful to a forest ecosystem: removing all the tigers or removing all the decomposers? Give a reasoned answer.', 'Removing decomposers would be more harmful: dead matter would pile up and nutrients would not return to the soil, so plants and then all animals would suffer; removing tigers mainly increases herbivores.', '1 mark: choice. 2 marks: reasoning.'),
]
FAMILIES[S + '12-st1'].append(SA(c12s1_hots, C='C4', D='D4', type='multi_step'))

c12s3_hots = [
    ('A large area of forest near a town is cleared and covered with buildings and roads. Predict how this would affect the local water cycle and carbon cycle.', 'Less transpiration and less rain locally; rain runs off concrete instead of soaking in, so groundwater falls and floods increase; fewer trees absorb CO₂ while more vehicles add it, so CO₂ in the air rises.', '1 mark: transpiration/rain. 1 mark: run-off/groundwater. 1 mark: carbon dioxide.'),
    ('A sealed glass jar with moist soil, a small plant and a few earthworms survives for months on a sunny windowsill. Explain how water and carbon keep cycling inside the jar.', 'Water evaporates and transpires, condenses on the glass and drips back; the plant takes in CO₂ for photosynthesis and gives O₂; the worms and microbes respire and decompose, releasing CO₂ and nutrients again.', '1 mark: water cycle. 1 mark: carbon cycle. 1 mark: role of decomposers.'),
]
c13s2_hots = [
    ('Scientists have never drilled through the Earth\'s crust into the mantle. How then do they know that the outer core is liquid? Suggest the kind of evidence used.', 'They study earthquake waves travelling through the Earth: some waves cannot pass through liquids and are not detected on the opposite side, showing a liquid outer core; volcanoes and rocks also give clues about the interior.', '1 mark: earthquake waves. 1 mark: reasoning about liquid. 1 mark: other evidence.'),
    ('Mount Everest is about 8.8 km high and the troposphere reaches about 12 km at the equator but only about 8 km at the poles. Why do climbers on Everest need oxygen cylinders even though they are still in the troposphere?', 'Air becomes thinner with height, so each breath contains much less oxygen near the top of the troposphere, even though the gases are in the same proportion.', '1 mark: air thinner with height. 1 mark: less oxygen per breath.'),
]
FAMILIES[S + '12-st3'].append(SA(c12s3_hots, C='C4', D='D4', type='multi_step'))
FAMILIES[S + '13-st2'].append(SA(c13s2_hots, C='C4', D='D4', type='multi_step'))


# ----------------------------------------------------------------- data-based case generators
def c10_mirror_case(r):
    who = name(r)
    d = r.choice([1, 1.5, 2, 2.5, 3])
    a = r.choice([45, 60, 90])
    return {'stem': (f'Read: In a dance studio, {who} stands {num(d)} m in front of a large plane mirror wall. In one corner, two mirrors meet at {a}°.\n'
                     f'(i) How far is {who}\'s image from {who}? (ii) {who} raises the left hand; which hand does the image raise? '
                     f'(iii) How many images of a ball placed between the corner mirrors will be seen? (iv) Write two other properties of the image in a plane mirror.'),
            'answer': f'(i) {num(2 * d)} m. (ii) The right hand (lateral inversion). (iii) 360/{a} − 1 = {360 // a - 1}. (iv) Virtual and erect; same size as the object.',
            'key': '1 mark each part.'}


def c11_calendar_case(r):
    y = r.choice([2027, 2028, 2029, 2030, 2031, 2032])
    leap = y % 4 == 0
    e = r.choice([5, 8, 12, 15, 20])
    return {'stem': (f'Read: A school calendar committee is planning holidays for {y}. Eid-ul-Fitr follows the lunar Hijri calendar, while Republic Day is always on 26 January (Gregorian, solar).\n'
                     f'(i) Is {y} a leap year? (ii) How many days does February {y} have? (iii) If Eid falls on {e + 11} March this year, about when will it fall next year? '
                     f'(iv) Why does Republic Day not shift like this?'),
            'answer': f'(i) {"Yes" if leap else "No"}. (ii) {29 if leap else 28}. (iii) About {e} March (about 11 days earlier). (iv) It follows the solar calendar, which keeps pace with the Earth\'s revolution.',
            'key': '1 mark each part.'}


def c12_energy_case(r):
    ch = r.choice([c for c in c12s2_chains if len(c) >= 4])
    E = r.choice([10000, 20000, 50000])
    Es = f'{E:,}'.replace(',', ' ')
    return {'stem': (f'Read: In a grassland study, the producers in the food chain {" → ".join(ch)} trap {Es} J of energy from sunlight.\n'
                     f'(i) Name the producer and the top consumer. (ii) Using the 10% idea, how much energy reaches the {ch[2]}? '
                     f'(iii) Where does the remaining energy go at each level? (iv) Why are top consumers fewer in number?'),
            'answer': f'(i) {cap(ch[0])}; {ch[-1]}. (ii) {num(E / 100)} J. (iii) It is used in life processes and lost as heat. (iv) Very little energy reaches the top, so it can support only a few animals.',
            'key': '1 mark each part.'}


def c13_rain_case(r):
    city = r.choice(['Jaipur', 'Chennai', 'Bhopal', 'Pune', 'Lucknow', 'Bengaluru'])
    a = r.choice([80, 100, 120, 150])
    mm = r.choice([600, 800, 1000])
    need = r.choice([2000, 3000, 4000])
    L = a * mm
    return {'stem': (f'Read: A school in {city} plans rooftop rainwater harvesting. The roof area is {a} m² and the yearly rainfall is {mm} mm. The school uses about {need} L of water a day.\n'
                     f'(i) How much rainwater (in litres) can be collected in a year? (1 m² × 1 mm = 1 L) (ii) For about how many days would it meet the school\'s needs? '
                     f'(iii) Is rainwater a renewable resource? (iv) Give one way to use the water other than storing it in tanks.'),
            'answer': f'(i) {num(L)} L. (ii) About {L // need} days. (iii) Yes. (iv) Lead it into a recharge pit to raise the groundwater level.',
            'key': '1 mark each part.'}


FAMILIES[S + '10-st2'].append(G('C4', 'D3', 'case', c10_mirror_case, gap='G7'))
FAMILIES[S + '11-st3'].append(G('C4', 'D3', 'case', c11_calendar_case, gap='G7'))
FAMILIES[S + '12-st2'].append(G('C4', 'D4', 'case', c12_energy_case, gap='G7'))
FAMILIES[S + '13-st3'].append(G('C4', 'D3', 'case', c13_rain_case, gap='G7'))
