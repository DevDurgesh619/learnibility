"""CBSE class 8 science (NCERT Curiosity) families, chapters 5-9."""
from __future__ import annotations

from qbank import name, two_names, num, num_distractors, mcq
from sci_kit import DEF, TERM, MC, SA, ARF, CLS, SORT, CASE, LONG, G, cap, sig

S = 'cbse-g8-science-ch'
g = 9.8

# ======================= ch05 Exploring Forces
c5s1_defs = [
    ('a force', 'a push or a pull on an object'),
    ('the newton', 'the SI unit of force, written N'),
    ('net force', 'the single force that has the same effect as all the forces acting on an object together'),
    ('balanced forces', 'forces on an object that cancel each other so that its state of motion does not change'),
    ('unbalanced forces', 'forces whose combined effect is not zero, so that they change the speed or direction of an object'),
    ('the magnitude of a force', 'the strength or size of a force'),
]
c5s1_effects = {
    'a change in shape': ['pressing a ball of dough into a roti', 'squeezing a sponge', 'stretching a rubber band', 'kneading clay into a pot', 'crushing an empty can'],
    'a change in speed': ['pedalling a bicycle harder', 'applying brakes to a scooter', 'kicking a football lying at rest', 'pushing a stalled car to start it'],
    'a change in direction': ['a batsman hitting a ball towards the boundary', 'a goalkeeper deflecting a ball', 'turning the handle of a bicycle', 'a carrom striker bouncing off the edge'],
}
c5s1_mc = [
    ('Which of these CANNOT be done by applying a force?', 'Change the mass of an object', 'Change the shape of an object', 'Change the speed of an object', 'Change the direction of motion'),
    ('Two children pull a box with 30 N and 20 N in opposite directions. The net force on the box is:', '10 N towards the 30 N pull', '50 N', '10 N towards the 20 N pull', 'zero'),
    ('When two forces act on an object in the same direction, the net force is:', 'the sum of the two forces', 'the difference of the two forces', 'always zero', 'the larger force only'),
    ('A force always acts:', 'when objects interact with each other', 'on objects at rest only', 'on moving objects only', 'without any object'),
    ('If equal forces act on a box from opposite sides, the box:', 'does not move', 'moves towards the left', 'moves towards the right', 'moves upwards'),
]


def c5s1_net(r):
    a, b = two_names(r)
    f1, f2 = r.randint(15, 90), r.randint(15, 90)
    same = r.random() < 0.4
    if same:
        ans = f'{f1 + f2} N'
        key = f'Same direction: forces add, {f1} + {f2} = {f1 + f2} N.'
        stem = f'{a} and {b} push a heavy almirah in the same direction with forces of {f1} N and {f2} N. What is the net force on it?'
        d = [f'{abs(f1 - f2)} N', f'{f1 * f2} N', '0 N']
    else:
        if f1 == f2:
            f2 += 5
        big = a if f1 > f2 else b
        ans = f'{abs(f1 - f2)} N towards {big}'
        key = f'Opposite directions: subtract, {max(f1, f2)} − {min(f1, f2)} = {abs(f1 - f2)} N, in the direction of the larger force ({big}).'
        stem = f'In a tug of war, {a} pulls with {f1} N and {b} pulls with {f2} N in the opposite direction. Find the net force and its direction.'
        d = [f'{f1 + f2} N towards {big}', f'{abs(f1 - f2)} N towards {a if big == b else b}', '0 N']
    return {'stem': stem, 'answer': ans, 'key': key, 'distractors': d}


c5s1_why = [
    ('A football lying on the ground does not move by itself. Why does it start moving when kicked?', 'An unbalanced force (the kick) acts on it and changes its state from rest to motion.', '1 mark: unbalanced force. 1 mark: changes state of motion.'),
    ('Why does a moving bicycle slow down and stop when we stop pedalling?', 'Friction between the tyres and the road, and air resistance, act opposite to the motion and reduce the speed.', '1 mark: friction/opposing force. 1 mark: speed reduces.'),
    ('Give one example each where a force changes (i) the shape and (ii) the direction of motion of an object.', '(i) Pressing dough into a roti; (ii) a batsman hitting a moving ball.', '1 mark each.'),
]
c5s1_ar = [
    ('In a tug of war, if both teams pull equally hard, the rope does not move.', 'Equal and opposite forces on an object are balanced and the net force is zero.', 'a', 'R explains A.'),
    ('A force can change the shape of an object.', 'A force always makes an object move.', 'c', 'A true; R false—forces can also balance or deform without motion.'),
    ('The net force on a box pushed by two people in the same direction is the sum of their forces.', 'Forces acting in the same direction add up.', 'a', 'R explains A.'),
]
c5s1_hots = [
    ('A goalkeeper catches a fast football. Name all the effects of the force applied by the goalkeeper on the ball.', 'The ball slows down and stops (change in speed); its direction changes if deflected; it is squeezed slightly (change in shape).', '1 mark per effect (max 3).'),
    ('Kavya says a book lying on a table has no force acting on it because it is not moving. Explain why she is wrong.', 'Gravity pulls the book down and the table pushes it up; these forces are balanced, so the net force is zero and the book stays at rest.', '1 mark: two forces named. 1 mark: balanced, net zero.'),
    ('Three boys push a cart: two push forward with 40 N each and one pushes backward with 50 N. Will the cart move? Explain with the net force.', 'Net force = 40 + 40 − 50 = 30 N forward; it is unbalanced, so the cart starts moving forward.', '1 mark: calculation. 1 mark: direction and conclusion.'),
]
c5s1_case = [
    ('Read: During a school game, Aditya pushes a stationary ball, Riya hits it sideways with a bat, and finally Arjun stops it with his foot, flattening it slightly.\n'
     '(i) Which effect of force does Aditya\'s push show? (ii) What does Riya\'s hit change? (iii) Name two effects of Arjun\'s force. (iv) Are all these contact forces?',
     '(i) Change from rest to motion (speed). (ii) Direction of motion. (iii) Stops the ball (speed) and changes its shape. (iv) Yes, all are muscular contact forces.', '1 mark each.'),
]

c5s2_defs = [
    ('a contact force', 'a force that acts only when two objects are in contact with each other'),
    ('muscular force', 'the force produced by the action of muscles in our body or in animals'),
    ('friction', 'the force that opposes the motion of one surface over another surface in contact'),
    ('static friction', 'the friction that prevents an object at rest from starting to move'),
    ('sliding friction', 'the friction acting when one surface slides over another'),
]
c5s2_mc = [
    ('Friction always acts:', 'opposite to the direction of motion', 'in the direction of motion', 'upwards', 'only on moving liquids'),
    ('Bullocks pulling a cart use:', 'muscular force', 'magnetic force', 'electrostatic force', 'gravitational force only'),
    ('Which needs a larger force?', 'Starting to push a heavy box at rest', 'Keeping it sliding once it moves', 'Both need exactly the same', 'Neither needs force'),
    ('Rolling friction is ______ sliding friction.', 'smaller than', 'larger than', 'equal to', 'unrelated to'),
]
c5s2_why = [
    ('Why is it easier to walk on a rough road than on a wet marble floor?', 'A rough road gives more friction, so our feet do not slip; a wet marble floor is smooth and friction is less.', '1 mark: friction more on rough surface. 1 mark: slipping on smooth.'),
    ('Why do we need a larger push to start moving a heavy box than to keep it moving?', 'Static friction is larger than sliding friction.', '1 mark: static > sliding. 1 mark: application.'),
    ('Why is friction called a "necessary evil"?', 'It helps us walk, write, hold things and brake vehicles, but it also wears out parts, wastes energy and produces heat.', '1 mark: uses. 1 mark: drawbacks.'),
]
c5s2_ar = [
    ('Friction is a contact force.', 'Friction acts between two surfaces in contact.', 'a', 'R explains A.'),
    ('A ball rolling on grass stops sooner than one rolling on a cement floor.', 'Grass offers more friction than a smooth cement floor.', 'a', 'R explains A.'),
    ('Muscular force is a non-contact force.', 'Muscular force can act only when the body is in contact with the object.', 'd', 'A false; R true.'),
]
c5s2_hots = [
    ('Explain why it is difficult to write on a glass surface with a pen but easy to write on paper.', 'Writing needs friction between the nib and the surface; paper is rough and gives friction, glass is very smooth.', '1 mark: friction needed. 1 mark: glass smooth.'),
    ('A carrom board is sprinkled with fine powder before a game. How does this help, and why would sprinkling sand spoil the game?', 'Powder makes the surface smoother and reduces friction, so coins slide easily; sand is rough and would increase friction.', '1 mark: powder reduces friction. 1 mark: sand increases it.'),
]

c5s3_defs = [
    ('a non-contact force', 'a force that acts on an object without being in contact with it'),
    ('magnetic force', 'the force exerted by a magnet on another magnet or on magnetic materials such as iron'),
    ('electrostatic force', 'the force exerted by a charged object on another charged or uncharged object'),
    ('gravitational force', 'the force of attraction between any two objects that have mass'),
    ('gravity', 'the force with which the Earth pulls objects towards its centre'),
]
c5s3_cats = {
    'a contact force': ['the push of a hand opening a door', 'friction between tyres and road', 'a horse pulling a tonga', 'the force of a hammer on a nail', 'a racket hitting a shuttlecock'],
    'a non-contact force': ['a magnet pulling an iron pin from a distance', 'a rubbed balloon attracting bits of paper', 'a mango falling from a tree', 'the Moon being pulled by the Earth', 'a comb after combing dry hair attracting hair'],
}
c5s3_mc = [
    ('A plastic scale rubbed on dry hair attracts bits of paper. The force is:', 'electrostatic force', 'magnetic force', 'muscular force', 'friction'),
    ('Which force keeps the Moon moving around the Earth?', 'Gravitational force', 'Magnetic force', 'Electrostatic force', 'Friction'),
    ('Two magnets are brought close with their north poles facing. They will:', 'repel each other', 'attract each other', 'not affect each other', 'stick together'),
    ('Which statement about gravitational force is correct?', 'It is always attractive', 'It is always repulsive', 'It acts only on living things', 'It acts only on the Earth'),
    ('Which force can be both attractive and repulsive?', 'Magnetic force', 'Gravitational force', 'Muscular force only', 'Friction'),
]
c5s3_why = [
    ('Why does a mango fall downwards and not upwards when it breaks from the tree?', 'The Earth pulls everything towards its centre by gravitational force.', '1 mark: gravity. 1 mark: towards the Earth\'s centre.'),
    ('Why does a balloon rubbed on wool stick to a wall?', 'Rubbing charges the balloon; the charged balloon exerts an electrostatic force on the wall.', '1 mark: charged by rubbing. 1 mark: electrostatic attraction.'),
    ('Why is magnetic force called a non-contact force?', 'A magnet attracts iron objects even from a distance, without touching them.', '1 mark: acts at a distance. 1 mark: example.'),
]
c5s3_ar = [
    ('A magnet can lift an iron pin without touching it.', 'Magnetic force is a non-contact force.', 'a', 'R explains A.'),
    ('An apple falls to the ground.', 'The Earth attracts the apple by gravitational force.', 'a', 'R explains A.'),
    ('Electrostatic force acts only between objects in contact.', 'A charged comb can attract bits of paper from a distance.', 'd', 'A false; R true.'),
]
c5s3_hots = [
    ('How can you find out whether a metal paperclip is attracted by a magnet or by electrostatic force from a rubbed comb? Plan a quick test.',
     'Bring an unrubbed magnet close: a steel clip is attracted by magnetic force. Bring a rubbed comb near small paper bits and the clip: paper bits are attracted (electrostatic); a magnet does not attract paper.',
     '1 mark: test with magnet. 1 mark: test with comb and paper. 1 mark: conclusion.'),
    ('A floating ring magnet stays above another ring magnet on a pencil. Name the forces acting on it and explain why it floats.',
     'Gravity pulls it down; magnetic repulsion from the lower magnet (like poles facing) pushes it up; these balance, so it floats.',
     '1 mark: forces named. 1 mark: balance explained.'),
]

c5s4_defs = [
    ('mass', 'the quantity of matter in an object, measured in kilograms'),
    ('weight', 'the force with which the Earth pulls an object towards itself, measured in newtons'),
    ('a spring balance', 'a device that measures force (such as weight) by the stretching of a spring'),
]
c5s4_mc = [
    ('Which of the following stays the same when an astronaut goes from the Earth to the Moon?', 'Her mass', 'Her weight', 'The pull of gravity on her', 'The reading of a spring balance under her'),
    ('The SI unit of weight is:', 'newton', 'kilogram', 'gram', 'litre'),
    ('A spring balance measures:', 'force', 'mass directly', 'volume', 'density'),
    ('The weight of an object on the Moon is about ______ of its weight on the Earth.', 'one-sixth', 'six times', 'one-half', 'the same'),
]


def c5s4_weight(r):
    m = r.choice([2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 40, 45, 50])
    w = m * g
    return {'stem': f'What is the weight of a {num(m)} kg bag of rice on the Earth? (Take g = 9.8 m/s².)', 'answer': f'{num(w, 1)} N',
            'key': f'Weight = mass × g = {num(m)} × 9.8 = {num(w, 1)} N.', 'distractors': [f'{num(m)} N', f'{num(m)} kg', f'{num(w / 6, 1)} N']}


def c5s4_moon(r):
    who = name(r)
    m = r.choice([30, 36, 42, 45, 48, 54, 60, 66])
    we = m * g
    wm = we / 6
    return {'stem': f'{who} has a mass of {m} kg. Find {who}\'s weight on the Earth and on the Moon (g = 9.8 m/s²; gravity on the Moon is about one-sixth). What is the mass on the Moon?',
            'answer': f'Earth: {num(we, 1)} N; Moon: about {num(wm, 1)} N; mass stays {m} kg.',
            'key': f'W = {m} × 9.8 = {num(we, 1)} N; on Moon {num(we, 1)} ÷ 6 ≈ {num(wm, 1)} N; mass does not change.'}


def c5s4_spring(r):
    k = r.choice([2, 4, 5])  # cm per newton
    w = r.choice([2, 3, 4, 5, 6, 8])
    ext = k * w
    new = r.choice([1.5, 2, 3])
    return {'stem': f'A spring balance stretches {ext} cm when an object of weight {w} N hangs from it. How much will it stretch for an object of weight {num(w * new)} N (assume the stretch is proportional to the force)?',
            'answer': f'{num(ext * new)} cm', 'key': f'Stretch per newton = {ext} ÷ {w} = {k} cm/N; {num(w * new)} × {k} = {num(ext * new)} cm.',
            'distractors': num_distractors(ext * new, ext + new, ext * w, ext)}


c5s4_why = [
    ('Why is it correct to say "the mass of the bag is 5 kg" but not "the weight of the bag is 5 kg"?', 'Mass is measured in kilograms; weight is a force and is measured in newtons (about 49 N for 5 kg).', '1 mark: mass in kg. 1 mark: weight in N.'),
    ('Why would a spring balance show a smaller reading on the Moon for the same object?', 'The Moon\'s gravity is weaker (about one-sixth), so it pulls the object with less force.', '1 mark: weaker gravity. 1 mark: smaller weight.'),
]
c5s4_ar = [
    ('The mass of an object is the same on the Earth and on the Moon.', 'Mass is the quantity of matter, which does not depend on gravity.', 'a', 'R explains A.'),
    ('Weight is measured in kilograms.', 'Weight is a force.', 'd', 'A false (newtons); R true.'),
    ('An astronaut weighs less on the Moon.', 'The Moon has no gravity.', 'c', 'A true; R false: the Moon\'s gravity is about one-sixth of Earth\'s.'),
]

c5s5_defs = [
    ('a lubricant', 'a substance such as oil or grease that reduces friction between moving parts'),
    ('ball bearings', 'small steel balls placed between moving parts to replace sliding with rolling friction'),
    ('streamlined shape', 'a shape, narrow in front, that reduces the drag of air or water on a moving object'),
    ('drag', 'the frictional force exerted by a fluid such as air or water on an object moving through it'),
]
c5s5_cats = {
    'a way of increasing friction': ['treads on tyres', 'sprinkling sand on a slippery path', 'gymnasts applying powder to their hands', 'spikes on sports shoes', 'grooves on shoe soles'],
    'a way of reducing friction': ['oiling a squeaky door hinge', 'using ball bearings in a cycle wheel', 'polishing a surface', 'putting wheels under a suitcase', 'the streamlined shape of a boat'],
}
c5s5_mc = [
    ('Friction depends on:', 'the nature of the two surfaces and how hard they are pressed together', 'only the colour of the surfaces', 'only the speed of the object', 'the shape of the object\'s shadow'),
    ('Why do aeroplanes and fish have streamlined shapes?', 'To reduce the drag of air or water', 'To increase friction', 'To look attractive', 'To increase their weight'),
    ('Which reduces friction the most?', 'Rolling on wheels', 'Sliding on a rough floor', 'Dragging on sand', 'Dragging on a carpet'),
    ('Friction produces:', 'heat', 'light only', 'magnetism', 'sound only'),
]
c5s5_why = [
    ('Why are tyres of vehicles made with grooves (treads)?', 'Treads increase friction with the road, giving better grip and preventing skidding, especially on wet roads.', '1 mark: increase friction. 1 mark: grip/prevent skid.'),
    ('Why does a match stick light when struck against the rough side of the box?', 'Friction between the head and the rough surface produces enough heat to ignite the chemicals.', '1 mark: friction. 1 mark: heat ignites.'),
    ('Why do we rub our hands together on a cold day?', 'Friction between the palms produces heat that warms them.', '1 mark: friction. 1 mark: heat.'),
    ('Why are ball bearings used in the hubs of bicycle wheels?', 'They replace sliding friction with much smaller rolling friction, so the wheel turns easily.', '1 mark: rolling friction. 1 mark: smaller.'),
]
c5s5_ar = [
    ('Machine parts are oiled regularly.', 'Oil reduces friction, wear and heating of moving parts.', 'a', 'R explains A.'),
    ('Kabaddi players rub soil on their hands.', 'Soil reduces friction and helps the grip.', 'c', 'A true; R false—soil increases friction for a better grip.'),
    ('Rolling friction is less than sliding friction.', 'Luggage bags are fitted with wheels.', 'b', 'Both true, but R is an application, not the explanation.'),
]


def c5s5_surface(r):
    surfaces = [('a glass sheet', 140), ('a newspaper', 95), ('a cotton towel', 60), ('sand', 30), ('a polished marble floor', 125), ('a jute mat', 50)]
    picks = r.sample(surfaces, 3)
    who = name(r)
    rows = '; '.join(f'{s} – {d} cm' for s, d in picks)
    best = max(picks, key=lambda x: x[1])[0]
    worst = min(picks, key=lambda x: x[1])[0]
    return {'stem': f'{who} rolled the same marble down the same ramp onto different surfaces and measured how far it travelled: {rows}. Which surface has the most friction and which the least? Give a reason.',
            'answer': f'Most friction: {worst}; least: {best}.',
            'key': f'The marble stops soonest where friction is largest ({worst}) and travels farthest where it is smallest ({best}). 1 mark each + 1 mark reason.'}


c5_case = [
    ('Read: Siddharth\'s cycle squeaks and is hard to pedal. His father oils the chain and axle. On a rainy day the brakes are less effective and Siddharth skids at a turn.\n'
     '(i) Why does oiling make pedalling easier? (ii) Why do brakes work less well when wet? (iii) Which feature of the tyres helps prevent skidding? (iv) Give one disadvantage of friction in a cycle.',
     '(i) Oil reduces friction between moving parts. (ii) Water forms a thin layer that reduces friction between brake pads and rim. (iii) Treads on tyres. (iv) Wear and tear of tyres/brake pads; energy lost as heat.',
     '1 mark each.'),
    ('Read: A shopkeeper finds it hard to push a heavy carton of books across the floor. When he puts it on a trolley with wheels, he can move it easily. Later he sprinkles talcum powder on a carrom board.\n'
     '(i) Which type of friction acts when the carton is pushed on the floor? (ii) Why is the trolley easier? (iii) What does the powder do? (iv) Name one force other than friction acting on the carton.',
     '(i) Sliding friction (static at the start). (ii) Rolling friction is much less than sliding friction. (iii) Reduces friction so the striker and coins slide easily. (iv) Gravity (weight) or the push of the floor/muscular force.',
     '1 mark each.'),
]
c5_long = [
    ('What is friction? Explain two factors on which it depends. Describe two ways of increasing and two ways of reducing friction, with one example each.',
     'Friction is the force opposing relative motion between surfaces in contact. It depends on the nature of the surfaces (rough surfaces give more) and how hard they are pressed together (heavier objects, more friction). Increase: treads on tyres, sand on slippery roads. Reduce: lubricants such as oil, ball bearings/wheels, polishing, streamlining.',
     '1 mark: definition; 2 marks: factors; 2 marks: ways with examples.'),
    ('Distinguish between contact and non-contact forces with two examples each. Explain why a ball thrown up comes back down and why the ball stops when it rolls on the ground.',
     'Contact forces act only on touching (muscular force, friction); non-contact forces act from a distance (magnetic, electrostatic, gravitational). A ball comes down because gravity pulls it; a rolling ball stops because friction opposes its motion.',
     '2 marks: distinction with examples; 1.5 marks each explanation.'),
    ('Distinguish between mass and weight (any three points). A girl of mass 45 kg goes to the Moon. Find her weight on the Earth and on the Moon (g = 9.8 m/s², Moon\'s gravity one-sixth).',
     'Mass: quantity of matter, kg, same everywhere, measured by a beam balance. Weight: pull of gravity, newton, changes with place, measured by a spring balance. Earth: 45 × 9.8 = 441 N; Moon: 441 ÷ 6 = 73.5 N.',
     '3 marks: differences; 2 marks: calculations.'),
]

# ======================= ch06 Pressure, Winds, Storms and Cyclones
c6s1_defs = [
    ('pressure', 'the force acting perpendicularly on a unit area of a surface'),
    ('the pascal', 'the SI unit of pressure, equal to one newton per square metre'),
    ('thrust', 'the force acting perpendicular to a surface'),
]
c6s1_mc = [
    ('Pressure is calculated as:', 'force ÷ area', 'force × area', 'area ÷ force', 'force + area'),
    ('Why do school bags have wide straps?', 'Wide straps spread the weight over a larger area, so pressure on the shoulders is less', 'Wide straps are lighter', 'Wide straps increase pressure', 'Wide straps look stylish only'),
    ('A sharp knife cuts better than a blunt one because:', 'its thin edge has a small area, so the pressure is large', 'it is heavier', 'it has a larger area', 'it has less force'),
    ('Camels can walk easily on sand because their feet:', 'are broad, which reduces pressure on the sand', 'are sharp', 'are small', 'are very hard'),
    ('Which unit is used for pressure?', 'N/m²', 'N·m', 'kg/m³', 'm/s'),
]


def c6s1_p(r):
    F = r.choice([50, 100, 120, 200, 250, 300, 400, 450, 500, 600, 800, 1000, 1200])
    A = r.choice([0.01, 0.02, 0.04, 0.05, 0.1, 0.2, 0.25, 0.5, 1, 2])
    P = F / A
    return {'stem': f'A force of {F} N acts on an area of {num(A)} m². Calculate the pressure.', 'answer': f'{num(P)} Pa',
            'key': f'P = F ÷ A = {F} ÷ {num(A)} = {num(P)} N/m² = {num(P)} Pa.', 'distractors': [f'{num(F * A)} Pa', f'{num(A / F, 5)} Pa', f'{num(P / 10)} Pa']}


def c6s1_brick(r):
    l, b, h = r.choice([(0.2, 0.1, 0.05), (0.25, 0.12, 0.08), (0.3, 0.15, 0.1), (0.24, 0.1, 0.07)])
    W = r.choice([20, 24, 30, 36, 40, 48])
    faces = [(l * b, f'{num(l)} m × {num(b)} m'), (l * h, f'{num(l)} m × {num(h)} m'), (b * h, f'{num(b)} m × {num(h)} m')]
    pmax = W / (b * h)
    pmin = W / (l * b)
    return {'stem': f'A brick of weight {W} N measures {num(l)} m × {num(b)} m × {num(h)} m. Find the largest and smallest pressure it can exert on the ground, and say which face it rests on each time.',
            'answer': f'Largest {sig(pmax, 4)} Pa on the {num(b)} m × {num(h)} m face; smallest {sig(pmin, 4)} Pa on the {num(l)} m × {num(b)} m face.',
            'key': f'Smallest area {sig(b * h, 3)} m² gives P = {W} ÷ {sig(b * h, 3)} = {sig(pmax, 4)} Pa; largest area {sig(l * b, 3)} m² gives {sig(pmin, 4)} Pa. 1 mark each area, 1 mark each pressure, 1 mark faces.'}


def c6s1_force(r):
    P = r.choice([2000, 5000, 8000, 10000, 12000, 15000, 20000])
    A = r.choice([0.02, 0.03, 0.04, 0.05, 0.06])
    F = P * A
    who = name(r)
    return {'stem': f'{who} stands on the floor and exerts a pressure of {P} Pa. The total area of contact of the feet is {num(A)} m². What is {who}\'s weight?',
            'answer': f'{num(F)} N', 'key': f'F = P × A = {P} × {num(A)} = {num(F)} N.', 'distractors': [f'{num(P / A)} N', f'{num(A / P, 6)} N', f'{num(F / 9.8, 1)} N']}


c6s1_why = [
    ('Why do nails have pointed tips?', 'The small area of the tip produces a large pressure for the same force, so the nail goes into wood easily.', '1 mark: small area. 1 mark: large pressure.'),
    ('Why are heavy trucks fitted with many wide tyres?', 'Many wide tyres spread the weight over a larger area, reducing pressure so the road and tyres are not damaged.', '1 mark: larger area. 1 mark: less pressure.'),
    ('Why does a person sink less in soft snow when wearing skis?', 'Skis have a large area, so the pressure on the snow is reduced.', '1 mark: area. 1 mark: less pressure.'),
]
c6s1_ar = [
    ('It is easier to cut vegetables with a sharp knife.', 'A sharp edge has a small area and produces greater pressure.', 'a', 'R explains A.'),
    ('Pressure increases when the area increases for the same force.', 'Pressure is force per unit area.', 'd', 'A false: pressure decreases; R true.'),
    ('Railway tracks are laid on wide sleepers.', 'Wide sleepers increase the pressure on the ground.', 'c', 'A true; R false: they reduce pressure.'),
]
c6s1_hots = [
    ('Why can a person lie on a bed of hundreds of nails without getting hurt, but cannot stand on one nail?', 'The weight is shared by many nails, so the total area is large and the pressure at each point is small; on one nail the whole weight acts on a tiny area, giving huge pressure.', '1 mark: many nails, large area. 1 mark: small pressure. 1 mark: single nail.'),
    ('An elephant weighs about 40 times more than a woman wearing pencil heels, yet the heels can damage a wooden floor more easily. Explain.', 'The heel tip has a very small area, so the pressure it exerts can be larger than that of an elephant\'s broad feet.', '1 mark: small area of heel. 1 mark: pressure comparison.'),
]

c6s2_defs = [
    ('atmospheric pressure', 'the pressure exerted by the air of the atmosphere on everything on the Earth'),
    ('liquid pressure', 'the pressure exerted by a liquid on the walls and base of its container and on objects in it'),
    ('a barometer', 'an instrument used to measure atmospheric pressure'),
]
c6s2_mc = [
    ('Water comes out with the greatest force from the hole that is:', 'lowest in the bottle', 'highest in the bottle', 'in the middle', 'at the cap'),
    ('The walls of a dam are made thicker at the bottom because:', 'water pressure increases with depth', 'water is heavier at the top', 'it looks better', 'air pressure is more at the bottom'),
    ('A liquid exerts pressure:', 'in all directions, including on the walls of the container', 'only downwards', 'only upwards', 'only sideways'),
    ('Atmospheric pressure ______ as we go up a mountain.', 'decreases', 'increases', 'stays the same', 'first increases then doubles'),
    ('A rubber sucker sticks to a smooth wall because:', 'air pressure outside presses it against the wall', 'it is magnetic', 'glue is present', 'gravity pulls it to the wall'),
    ('When water is filled in a balloon, it bulges at the sides. This shows that water exerts pressure:', 'on the sides too', 'only on the bottom', 'only upwards', 'on nothing'),
]
c6s2_why = [
    ('Why do we not feel the very large atmospheric pressure acting on our body?', 'The pressure inside our body is nearly equal and balances the outside pressure.', '1 mark: inside pressure. 1 mark: balanced.'),
    ('Why does ink sometimes leak from a fountain pen in an aeroplane?', 'Air pressure outside drops at high altitude while the air inside the pen is at higher pressure, pushing ink out.', '1 mark: lower outside pressure. 1 mark: inside pushes ink.'),
    ('Why do mountaineers sometimes get nose bleeding at high altitudes?', 'Atmospheric pressure is low, so the higher blood pressure inside can burst thin blood vessels in the nose.', '1 mark: low outside pressure. 1 mark: vessels burst.'),
    ('Why do we make two holes in a sealed tin of oil before pouring?', 'Air enters through one hole and keeps the pressure inside equal to outside, so oil flows smoothly from the other.', '1 mark: air enters. 1 mark: pressure balance.'),
]
c6s2_ar = [
    ('Water spurts farthest from the lowest hole of a water bottle.', 'Liquid pressure increases with depth.', 'a', 'R explains A.'),
    ('Air pressure is greater at the top of a mountain than at sea level.', 'There is less air above us at higher altitude.', 'd', 'A false; R true.'),
    ('A drinking straw works because of air pressure.', 'Sucking lowers the pressure inside the straw, so atmospheric pressure pushes the liquid up.', 'a', 'R explains A.'),
]
c6s2_hots = [
    ('Explain with reasons the shape of the wall of the Bhakra dam if water pressure increases with depth.', 'The wall is broader at the base and narrower at the top, because the pressure of water is greatest at the bottom and must be resisted there.', '1 mark: shape. 1 mark: reason.'),
    ('Predict and explain what happens if you suck all the air out of a thin plastic bottle with its cap shut except for your mouth.', 'The bottle gets crushed inwards because pressure inside falls and the higher atmospheric pressure outside pushes its walls in.', '1 mark: crushed. 1 mark: reason.'),
]

c6s3_defs = [
    ('wind', 'moving air, which flows from a region of high pressure to one of low pressure'),
    ('a sea breeze', 'wind blowing from the sea towards the land during the day'),
    ('a land breeze', 'wind blowing from the land towards the sea at night'),
    ('convection', 'the transfer of heat by the movement of warm air or liquid rising and cooler air or liquid sinking'),
    ('monsoon winds', 'seasonal winds that blow from the oceans towards land in summer and bring rain to India'),
]
c6s3_mc = [
    ('Warm air rises because it is:', 'lighter (less dense) than cool air', 'heavier than cool air', 'always moist', 'pushed by the Sun'),
    ('During the day, a breeze blows from the sea to the land because:', 'land heats faster, air over it rises, and cooler air from the sea moves in', 'the sea heats faster than land', 'land cools faster during the day', 'air always moves from land to sea'),
    ('Air moves from regions of:', 'high pressure to low pressure', 'low pressure to high pressure', 'cold to hotter places only at night', 'low altitude to space'),
    ('The south-west monsoon winds in India come from:', 'the Indian Ocean and the Arabian Sea', 'the Himalayas', 'the Thar Desert', 'the Arctic'),
    ('Exhaust fans are fitted near the ceiling of a kitchen because:', 'hot air rises and goes out through them', 'cold air rises', 'they look better there', 'smoke is heavy'),
]
c6s3_why = [
    ('Why is the land breeze blowing at night from land to sea?', 'At night land cools faster than the sea; air over the sea is warmer and rises, so cooler air from land moves towards the sea.', '1 mark: land cools faster. 1 mark: air moves to low pressure over sea.'),
    ('Why do hot-air balloons rise?', 'The air inside is heated, becomes less dense than the surrounding air and rises, carrying the balloon.', '1 mark: heated air less dense. 1 mark: rises.'),
    ('Uneven heating of the Earth causes winds. Explain with one example.', 'Air over hotter regions expands and rises, creating low pressure; cooler, high-pressure air moves in. Example: winds blow from the poles towards the equator.', '1 mark: uneven heating → pressure difference. 1 mark: example.'),
]
c6s3_ar = [
    ('Sea breeze blows during the daytime.', 'Land heats up faster than water in sunlight.', 'a', 'R explains A.'),
    ('Warm air sinks.', 'Warm air is denser than cool air.', 'e', ''),
    ('Winds blow from low pressure to high pressure.', 'Air moves to fill regions of low pressure.', 'd', 'A false: high to low; R true.'),
]
c6s3_ar[1] = ('Warm air rises.', 'Warm air is less dense than the cooler air around it.', 'a', 'R explains A.')
c6s3_hots = [
    ('Ventilators (small windows) in old houses are placed high on the walls. Explain how they keep rooms cool using the idea of convection.', 'Hot air rises and escapes through the high ventilators while cooler air enters through doors and windows below, setting up a convection current.', '1 mark: hot air rises out. 1 mark: cool air enters below.'),
    ('Fishermen in Kerala sail out in the early morning and return in the afternoon. How do land and sea breezes help them?', 'Early morning the land breeze (land to sea) carries the boats out; in the afternoon the sea breeze (sea to land) brings them back.', '1 mark: land breeze out. 1 mark: sea breeze back.'),
]

c6s4_defs = [
    ('a cyclone', 'a very large storm system with strong winds spiralling around a low-pressure centre'),
    ('the eye of a cyclone', 'the calm, clear central region of a cyclone with very low pressure'),
    ('a thunderstorm', 'a storm with lightning, thunder, strong winds and heavy rain, formed when warm moist air rises rapidly'),
    ('a storm surge', 'a rise in sea level pushed onto the coast by the strong winds of a cyclone'),
    ('a tornado', 'a dark funnel-shaped cloud of violently rotating winds reaching from the sky to the ground'),
]
c6s4_mc = [
    ('Which agency issues cyclone warnings in India?', 'India Meteorological Department (IMD)', 'ISRO only', 'Reserve Bank of India', 'NCERT'),
    ('Cyclones form over:', 'warm ocean waters', 'cold deserts', 'snow-covered mountains', 'dry land'),
    ('During a thunderstorm, it is safest to:', 'stay indoors away from metal objects and water taps', 'stand under a tall tree', 'hold an umbrella in an open field', 'swim in a pond'),
    ('The centre of a cyclone where the weather is calm is called the:', 'eye', 'wall', 'tail', 'arm'),
    ('Cyclones affect the east coast of India more often because:', 'more cyclones form in the warm Bay of Bengal', 'the east coast is colder', 'there is no sea there', 'mountains attract them'),
]
c6s4_why = [
    ('Why should we not take shelter under a tall tree during a thunderstorm?', 'Lightning tends to strike tall objects; the current can pass through the tree to a person standing nearby.', '1 mark: tall objects struck. 1 mark: danger to person.'),
    ('How does warm, moist air over the ocean lead to the formation of a cyclone?', 'Warm moist air rises, creating low pressure; water vapour condenses releasing heat, which makes air rise faster; surrounding air rushes in and spirals.', '1 mark: rising air/low pressure. 1 mark: condensation heat and spiralling.'),
    ('Why are people living near the coast moved to cyclone shelters before a cyclone hits?', 'Strong winds, heavy rain and storm surges can flood low-lying coastal areas and destroy houses.', '1 mark: storm surge/flooding. 1 mark: wind damage.'),
]
c6s4_ar = [
    ('The eye of a cyclone is calm.', 'The eye is a region of very low pressure with little wind and no clouds.', 'a', 'R explains A.'),
    ('Cyclones form over cold land.', 'Cyclones need warm, moist air to form.', 'd', 'A false; R true.'),
    ('Early warnings by IMD save lives during cyclones.', 'Warnings give people time to move to safe shelters.', 'a', 'R explains A.'),
]
c6s4_hots = [
    ('Prepare a list of five things a family in coastal Odisha should do when IMD issues a cyclone warning, with a reason for each.',
     'Listen to radio/TV updates (know path and timing); store drinking water and dry food (supply may be cut); keep a torch, batteries and first-aid kit; secure loose objects (they become missiles); move to a cyclone shelter if told (storm surge).',
     '1 mark per action with reason (max 5).'),
    ('Satellite images show a cyclone 600 km from the coast, moving at 15 km/h. Estimate how many hours people have before it reaches the coast, and why this information is useful.',
     '600 ÷ 15 = 40 hours; this allows time for evacuation and preparations.', '1 mark: calculation. 1 mark: use.'),
]
c6_case = [
    ('Read: An IMD bulletin says: "A deep depression over the Bay of Bengal has intensified into a cyclonic storm. Wind speed 90–100 km/h, gusting to 110 km/h. Landfall expected near Puri in 36 hours. Fishermen advised not to venture into the sea."\n'
     '(i) Where did the cyclone form and why there? (ii) What is meant by landfall? (iii) Why are fishermen warned? (iv) Name one danger other than strong wind.',
     '(i) Bay of Bengal—warm ocean water provides warm moist air. (ii) The cyclone\'s centre crossing the coastline. (iii) High waves and winds can capsize boats. (iv) Storm surge/flooding/heavy rain.',
     '1 mark each.'),
    ('Read: Pooja made three holes at different heights in a tall plastic bottle filled with water. Water came out of all three; the stream from the lowest hole travelled the farthest.\n'
     '(i) What does this show about liquid pressure and depth? (ii) Why does water come out sideways? (iii) What happens to the streams as the water level falls? (iv) Give one real-life application.',
     '(i) Pressure increases with depth. (ii) Liquids exert pressure on the walls (in all directions). (iii) They become weaker and fall closer. (iv) Dam walls are thicker at the bottom.',
     '1 mark each.'),
]
c6_long = [
    ('Explain how a thunderstorm and a cyclone are formed. Describe the structure of a cyclone and list three safety measures to be taken during a cyclone.',
     'Thunderstorm: warm moist air rises rapidly, cools, forms tall clouds with lightning and thunder. Cyclone: over warm seas, warm moist air rises, condensation releases heat, low pressure deepens, winds spiral in. Structure: calm low-pressure eye surrounded by a wall of strong winds and heavy rain. Safety: follow IMD warnings, move to shelters, store food and water, avoid going to sea.',
     '1 mark: thunderstorm; 2 marks: cyclone formation and eye; 2 marks: safety.'),
    ('Define pressure and give its SI unit. Explain why (a) porters place a round cloth on their heads, (b) liquid pressure increases with depth, and solve: a box of weight 600 N rests on a base of area 0.3 m²; find the pressure.',
     'Pressure = force per unit area, Pa (N/m²). (a) the cloth increases the area of contact and reduces pressure on the head. (b) deeper water has more water above it pushing down. Pressure = 600 ÷ 0.3 = 2000 Pa.',
     '1 mark: definition and unit; 1 mark each (a), (b); 2 marks numerical.'),
]

# ======================= ch07 Particulate Nature of Matter
c7s1_defs = [
    ('matter', 'anything that has mass and occupies space'),
    ('diffusion', 'the spreading and mixing of particles of one substance among those of another on their own'),
    ('a particle', 'a very tiny bit of a substance, too small to be seen even with a microscope'),
    ('dissolving', 'the mixing of a solid into a liquid so that its particles spread between the particles of the liquid'),
]
c7s1_mc = [
    ('When a crystal of potassium permanganate is put in water, the colour spreads. This shows that:', 'matter is made of tiny particles that move', 'water is coloured', 'the crystal is magnetic', 'particles do not move'),
    ('The smell of incense sticks reaches us across a room because of:', 'diffusion of the scent particles in air', 'gravity', 'friction', 'magnetism'),
    ('Diffusion is fastest in:', 'gases', 'liquids', 'solids', 'all equally'),
    ('A drop of ink spreads faster in:', 'hot water', 'cold water', 'ice', 'oil'),
    ('When 50 mL of water and 50 mL of alcohol are mixed, the total volume is slightly less than 100 mL. This shows that:', 'there are spaces between particles', 'particles are destroyed', 'alcohol evaporates instantly', 'water has no particles'),
]
c7s1_why = [
    ('Why does sugar seem to disappear when stirred in water, though the water tastes sweet?', 'Sugar breaks into tiny particles that spread into the spaces between water particles; they are still present, so the water is sweet.', '1 mark: particles in spaces. 1 mark: still present.'),
    ('Why does the smell of hot food reach us faster than that of cold food?', 'At higher temperature particles move faster, so the smell particles diffuse faster.', '1 mark: faster particles. 1 mark: faster diffusion.'),
    ('Why does diffusion take place very slowly in solids?', 'Particles in solids are tightly packed and only vibrate in place, so they cannot move into each other easily.', '1 mark: tight packing. 1 mark: little movement.'),
]
c7s1_ar = [
    ('A crystal of copper sulphate colours a whole beaker of water.', 'Matter is made up of a very large number of extremely small particles.', 'a', 'R explains A.'),
    ('Diffusion is faster in liquids than in gases.', 'Particles of gases move freely and fast.', 'd', 'A false; R true.'),
    ('The scent of a perfume spreads through a room.', 'Particles of the perfume diffuse into the air.', 'a', 'R explains A.'),
]


def c7s1_dilute(r):
    n = r.choice([3, 4, 5, 6])
    who = name(r)
    return {'stem': f'{who} dissolved 2–3 crystals of potassium permanganate in 100 mL of water and then diluted it {n} times, each time taking 10 mL and adding 90 mL of water. The last solution is still faintly coloured. What does this tell us about the particles in one crystal?',
            'answer': 'One crystal contains millions of tiny particles that keep dividing into still smaller ones.',
            'key': f'Even after {n} dilutions (by 10 each time, i.e. 10^{n}), colour remains: the crystal must contain an enormous number of very small particles (2 marks).'}


c7s1_hots = [
    ('Design an activity to show that diffusion is faster at higher temperature. What will you keep the same?', 'Add a drop of ink (or a crystal of potassium permanganate) gently to two beakers, one of hot and one of cold water; observe the spread over time. Keep the same: volume of water, size of drop/crystal, beakers, no stirring.', '1 mark: set-up. 1 mark: observation. 1 mark: controlled variables.'),
    ('A teacher sprays room freshener at one corner. Students near the corner smell it in 5 seconds, those at the far end in 25 seconds. In winter it takes even longer. Explain both observations.', 'Particles diffuse through air and take more time to travel farther; in winter the air is colder and the particles move more slowly.', '1 mark: distance. 1 mark: temperature.'),
]

c7s2_defs = [
    ('a solid', 'a state of matter with a fixed shape and fixed volume, in which particles are tightly packed'),
    ('a liquid', 'a state of matter with a fixed volume but no fixed shape, which takes the shape of its container'),
    ('a gas', 'a state of matter with neither a fixed shape nor a fixed volume, in which particles move freely'),
    ('fluids', 'liquids and gases, which can flow'),
]
c7s2_cats = {
    'a solid': ['ice cube', 'iron rod', 'chalk', 'wooden block', 'salt crystal', 'stone'],
    'a liquid': ['milk', 'kerosene', 'coconut oil', 'mercury', 'honey', 'water'],
    'a gas': ['oxygen', 'steam', 'carbon dioxide', 'LPG vapour', 'nitrogen', 'air in a balloon'],
}
c7s2_cmp = [
    ('Which state has the largest spaces between particles?', 'Gas', 'Liquid', 'Solid', 'All have equal spaces'),
    ('In which state do particles only vibrate about fixed positions?', 'Solid', 'Liquid', 'Gas', 'Liquid and gas'),
    ('Which state of matter takes the shape of its container but has a fixed volume?', 'Liquid', 'Solid', 'Gas', 'None'),
    ('The particles move fastest in:', 'a gas', 'a liquid', 'a solid', 'all equally'),
    ('Which statement about the particles of a liquid is correct?', 'They are close together but can slide past one another', 'They are fixed in position', 'They are very far apart', 'They do not move at all'),
]
c7s2_why = [
    ('Why does a gas fill the whole of any container in which it is kept?', 'Gas particles move freely and very fast in all directions with large spaces between them, and the attraction between them is very weak.', '1 mark: free motion. 1 mark: weak attraction/large spaces.'),
    ('Why does a solid have a fixed shape?', 'Its particles are tightly packed with strong attraction and can only vibrate in fixed positions.', '1 mark: strong attraction. 1 mark: fixed positions.'),
    ('A sponge can be pressed, yet it is a solid. Explain.', 'A sponge has tiny holes filled with air; pressing pushes out the air, not the particles of the solid closer together.', '1 mark: pores with air. 1 mark: air expelled.'),
]
c7s2_ar = [
    ('Liquids take the shape of the container.', 'Particles of a liquid can move and slide over one another.', 'a', 'R explains A.'),
    ('Gases have a fixed volume.', 'Gas particles move freely in all directions.', 'd', 'A false; R true.'),
    ('Solids are rigid.', 'The particles of a solid are held strongly in fixed positions.', 'a', 'R explains A.'),
]
c7s2_hots = [
    ('Sand flows when poured and takes the shape of a jar. Is sand a liquid? Justify.', 'No. Each sand grain is a solid with fixed shape and volume; sand only appears to flow because the grains are separate and slide over each other.', '1 mark: no. 1 mark: each grain is a solid.'),
    ('Using the particle model, explain why we can smell perfume but not a piece of iron.', 'Perfume is a liquid that evaporates easily, and its particles move into the air and reach our nose; iron particles are tightly held in the solid and do not escape.', '1 mark: perfume particles escape. 1 mark: iron particles held.'),
]

c7s3_defs = [
    ('interparticle attraction', 'the force of attraction that holds the particles of matter together'),
    ('interparticle space', 'the empty space between the particles of matter'),
    ('compressibility', 'the property of matter by which its volume can be reduced by applying pressure'),
    ('fluidity', 'the ability of a substance to flow'),
]
c7s3_mc = [
    ('Which is the most compressible?', 'Air', 'Water', 'Iron', 'Wood'),
    ('LPG is stored in cylinders in liquid form because gases:', 'can be compressed into a small volume', 'cannot be compressed', 'are heavier than liquids', 'have fixed volume'),
    ('The force of attraction between particles is strongest in:', 'solids', 'liquids', 'gases', 'all equally'),
    ('A syringe filled with water and sealed at the tip:', 'cannot be pushed in much', 'can be pushed in fully', 'gets heavier', 'expands'),
    ('Oxygen cylinders used in hospitals contain a lot of gas because:', 'gas particles can be pushed close together under pressure', 'oxygen is a solid', 'gases have no particles', 'gases expand under pressure'),
]
c7s3_why = [
    ('Why can we compress air in a syringe easily but not water?', 'Air particles have large spaces between them; water particles are already close together.', '1 mark: spaces in gas. 1 mark: liquid close packed.'),
    ('Why do we need to apply more force to break a piece of chalk than to move our hand through water?', 'Attraction between particles in a solid is much stronger than in a liquid.', '1 mark: stronger in solid. 1 mark: weaker in liquid.'),
    ('Why does CNG used in vehicles take up little space?', 'Natural gas is compressed to high pressure, so its particles are pushed close together into a small volume.', '1 mark: compressed. 1 mark: particles closer.'),
]
c7s3_ar = [
    ('Gases are highly compressible.', 'Gas particles have large spaces between them.', 'a', 'R explains A.'),
    ('Liquids flow but solids do not.', 'Interparticle attraction in liquids is weaker than in solids.', 'a', 'R explains A.'),
    ('Water can be compressed easily.', 'Water is a liquid.', 'd', 'A false; R true.'),
]
c7s3_hots = [
    ('Arrange iron, water and air in increasing order of (i) interparticle space and (ii) interparticle attraction. Explain how the order matches their compressibility.',
     '(i) Iron < water < air. (ii) Air < water < iron. Larger spaces and weaker attraction make air the most compressible; iron, with the smallest spaces, is hardly compressible.', '1 mark each order. 1 mark explanation.'),
    ('A balloon is pressed from all sides and becomes smaller, but returns to its size when released. Explain using particles.', 'The air particles are pushed closer into the spaces between them; when released, the fast-moving particles push the walls back out.', '1 mark: compressed spaces. 1 mark: particles push back.'),
]

c7s4_defs = [
    ('melting', 'the change of a solid into a liquid on heating'),
    ('the melting point', 'the temperature at which a solid changes into a liquid'),
    ('boiling', 'the rapid change of a liquid into a gas throughout the liquid at a fixed temperature'),
    ('the boiling point', 'the temperature at which a liquid boils'),
    ('evaporation', 'the slow change of a liquid into vapour at the surface, at any temperature below its boiling point'),
    ('condensation', 'the change of a gas or vapour into a liquid on cooling'),
    ('freezing', 'the change of a liquid into a solid on cooling'),
]
c7s4_cats = {
    'an example of melting': ['butter softening in a hot pan', 'ice cream dripping in the sun', 'wax dripping from a burning candle', 'ice turning into water'],
    'an example of evaporation': ['wet clothes drying on a line', 'a puddle drying after rain', 'sweat drying on the skin', 'salt left in pans of sea water'],
    'an example of condensation': ['water drops outside a glass of cold water', 'mist on a mirror after a hot bath', 'dew on grass in the morning', 'drops on the lid of a cooking pot'],
}
c7s4_mc = [
    ('The temperature of ice remains at 0 °C while it is melting because:', 'the heat supplied is used to overcome the attraction between particles', 'heat is lost to the air', 'the thermometer is faulty', 'ice does not absorb heat'),
    ('The boiling point of pure water at sea level is:', '100 °C', '0 °C', '50 °C', '37 °C'),
    ('Which change of state happens when steam touches a cold plate?', 'Condensation', 'Evaporation', 'Melting', 'Boiling'),
    ('Evaporation is faster when:', 'the air is dry and windy', 'the air is humid and still', 'the temperature is low', 'the surface area is small'),
    ('On heating, the particles of a solid:', 'vibrate faster and move apart', 'stop moving', 'become smaller', 'become heavier'),
]
c7s4_why = [
    ('Why do we feel cool after sweating?', 'Sweat evaporates by taking heat from our body, so the skin cools.', '1 mark: evaporation. 1 mark: takes heat from body.'),
    ('Why is water kept in an earthen pot (matka) cool in summer?', 'Water seeps through tiny pores and evaporates from the surface, taking heat from the remaining water.', '1 mark: seepage + evaporation. 1 mark: cooling.'),
    ('Why do clothes dry faster on a sunny, windy day?', 'Heat increases evaporation and wind carries away the water vapour, so more water can evaporate.', '1 mark: temperature. 1 mark: wind.'),
]
c7s4_ar = [
    ('Ice at 0 °C feels colder than water at 0 °C.', 'Ice absorbs extra heat from our hand to melt.', 'a', 'R explains A.'),
    ('Evaporation causes cooling.', 'During evaporation, particles absorb heat from the surroundings.', 'a', 'R explains A.'),
    ('Boiling takes place at any temperature.', 'Evaporation takes place only at the boiling point.', 'e', ''),
]
c7s4_ar[2] = ('Boiling takes place at a fixed temperature.', 'Evaporation takes place only at the boiling point.', 'c', 'A true; R false: evaporation happens at all temperatures.')


def c7s4_graph(r):
    s = r.choice([('wax', 55), ('naphthalene', 80), ('a solid X', 45), ('a solid Y', 70)])
    who = name(r)
    t0 = s[1] - r.randint(15, 25)
    return {'stem': f'{who} heated {s[0]} from {t0} °C and recorded the temperature every minute. The temperature rose steadily, stayed at {s[1]} °C for 4 minutes, and then rose again. (i) What is the melting point? (ii) Why did the temperature stay constant? (iii) What is the state of the substance during the constant part?',
            'answer': f'(i) {s[1]} °C. (ii) Heat was used to overcome interparticle attraction (melting), not to raise temperature. (iii) A mixture of solid and liquid.',
            'key': '1 mark each.'}


c7s4_hots = [
    ('A wet cloth is spread out fully on one line and another identical cloth is folded and hung. Which dries faster? Explain using particles.', 'The spread cloth: larger surface area lets more water particles escape at the same time.', '1 mark: spread cloth. 1 mark: surface area.'),
    ('In hilly areas water boils below 100 °C and dal takes longer to cook. Explain.', 'Air pressure is lower at heights, so water boils at a lower temperature; the lower temperature cooks food more slowly.', '1 mark: low pressure lowers boiling point. 1 mark: slower cooking.'),
]
c7_case = [
    ('Read: Tara put an ice cube in a dry steel tumbler. After a few minutes, water drops appeared on the outside of the tumbler, and the ice inside started melting into water.\n'
     '(i) Where did the drops outside come from? (ii) Name this change. (iii) Why did the ice melt? (iv) Would drops form on a very dry winter day as easily? Explain.',
     '(i) Water vapour in the air. (ii) Condensation. (iii) It absorbed heat from the surroundings. (iv) Fewer drops, because there is less water vapour in dry air.',
     '1 mark each.'),
    ('Read: Two students placed a drop of blue ink in a beaker of hot water and in a beaker of cold water. In the hot water, the colour spread through the beaker in 2 minutes; in the cold water it took 10 minutes.\n'
     '(i) Name the process. (ii) Why was it faster in hot water? (iii) Why does it not need stirring? (iv) What would happen in a beaker of honey? Why?',
     '(i) Diffusion. (ii) Particles move faster at higher temperature. (iii) Particles of liquids keep moving on their own. (iv) Much slower, because honey is thick and its particles move with difficulty.',
     '1 mark each.'),
]
c7_long = [
    ('Compare solids, liquids and gases on the basis of (i) arrangement of particles, (ii) interparticle spaces, (iii) interparticle attraction, (iv) shape and volume, (v) compressibility. Give one example of each.',
     'Solid: closely packed, very small spaces, strongest attraction, fixed shape and volume, almost incompressible (iron). Liquid: close but can move, small spaces, weaker attraction, fixed volume no fixed shape, slightly compressible (water). Gas: far apart, large spaces, weakest attraction, no fixed shape or volume, highly compressible (oxygen).',
     '1 mark per point of comparison (max 5).'),
    ('With the help of the particle model, describe what happens when ice is heated from −10 °C until it becomes steam. Explain why temperature stays constant at two stages.',
     'Ice particles vibrate faster as temperature rises to 0 °C; at 0 °C heat breaks attraction and ice melts, temperature constant; water heats to 100 °C, particles move faster; at 100 °C heat is used to separate particles completely into steam, temperature constant; steam particles move freely.',
     '1 mark per stage (max 4) + 1 mark for explaining constant temperature.'),
]

# ======================= ch08 Elements, Compounds and Mixtures
c8s1_defs = [
    ('a pure substance', 'a substance made of only one kind of particles, with the same composition throughout'),
    ('a mixture', 'two or more substances mixed together in any proportion without forming a new substance'),
    ('a homogeneous mixture', 'a mixture that has the same composition throughout, such as salt solution'),
    ('a heterogeneous mixture', 'a mixture whose components are not evenly spread and can often be seen, such as sand and water'),
]
c8s1_cats = {
    'a pure substance': ['distilled water', 'gold', 'common salt (sodium chloride)', 'sugar', 'oxygen', 'copper'],
    'a mixture': ['air', 'sea water', 'milk', 'brass', 'soil', 'lemonade'],
}
c8s1_hh = {
    'a homogeneous mixture': ['salt solution', 'sugar solution', 'air', 'brass', 'vinegar'],
    'a heterogeneous mixture': ['sand in water', 'oil and water', 'soil', 'poha with peanuts', 'iron filings and sulphur'],
}
c8s1_mc = [
    ('Which property is true for a mixture?', 'Its components keep their own properties', 'It has a fixed melting point', 'It always has a fixed composition', 'Its components cannot be separated'),
    ('Which of these can be separated by using a magnet?', 'Iron filings from sand', 'Salt from water', 'Sugar from water', 'Oil from water'),
    ('Air is a mixture because:', 'its components are present in varying amounts and keep their properties', 'it is made of one gas', 'it cannot be separated', 'it has a fixed formula'),
    ('Tap water is a mixture because it contains:', 'dissolved salts and gases', 'only hydrogen and oxygen atoms', 'only one substance', 'no particles'),
]
c8s1_why = [
    ('Why is milk considered a mixture and not a pure substance?', 'Milk contains water, fat, proteins, sugar and minerals in varying amounts; its composition changes from sample to sample.', '1 mark: many components. 1 mark: varying composition.'),
    ('Why is brass called a homogeneous mixture?', 'Brass is an alloy of copper and zinc mixed uniformly; the composition is the same throughout, though it can vary between samples.', '1 mark: alloy of Cu and Zn. 1 mark: uniform.'),
    ('How can you tell from boiling that a sample of water is not pure?', 'Pure water boils at exactly 100 °C at sea level; impure water boils at a different temperature and leaves a residue on evaporation.', '1 mark: fixed boiling point. 1 mark: residue/different temperature.'),
]
c8s1_ar = [
    ('Salt solution is a homogeneous mixture.', 'Salt is evenly distributed throughout the water.', 'a', 'R explains A.'),
    ('Air is a pure substance.', 'Air contains nitrogen, oxygen, carbon dioxide and other gases.', 'd', 'A false; R true.'),
    ('The components of a mixture keep their properties.', 'No new substance is formed when a mixture is made.', 'a', 'R explains A.'),
]

c8s2_el = [('hydrogen', 'H'), ('oxygen', 'O'), ('carbon', 'C'), ('nitrogen', 'N'), ('sodium', 'Na'), ('potassium', 'K'), ('iron', 'Fe'), ('copper', 'Cu'),
           ('calcium', 'Ca'), ('chlorine', 'Cl'), ('sulphur', 'S'), ('magnesium', 'Mg'), ('aluminium', 'Al'), ('zinc', 'Zn'), ('silver', 'Ag'), ('gold', 'Au'),
           ('mercury', 'Hg'), ('lead', 'Pb'), ('helium', 'He'), ('phosphorus', 'P')]


def c8s2_sym(r):
    n, s = r.choice(c8s2_el)
    wrong = set()
    pool = [x[1] for x in c8s2_el if x[1] != s]
    fakes = {'sodium': ['So', 'Sd'], 'potassium': ['Po', 'Pt'], 'iron': ['Ir', 'In'], 'copper': ['Co', 'Cp'], 'silver': ['Si', 'Sv'], 'gold': ['Go', 'Gd'],
             'mercury': ['Me', 'Mr'], 'lead': ['Le', 'Ld'], 'magnesium': ['Mn', 'Ma'], 'chlorine': ['C', 'Ch']}
    for f in fakes.get(n, []):
        if f != s:
            wrong.add(f)
    while len(wrong) < 3:
        wrong.add(r.choice(pool))
    return mcq(f'The chemical symbol of {n} is:', s, list(wrong)[:3], f'{cap(n)}: {s}.', r)


def c8s2_name(r):
    n, s = r.choice(c8s2_el)
    pool = [x[0] for x in c8s2_el if x[0] != n]
    return mcq(f'Which element has the symbol {s}?', n, r.sample(pool, 3), f'{s} stands for {n}.', r)


c8s2_cmpds = [('water', 'hydrogen and oxygen', 'H₂O'), ('carbon dioxide', 'carbon and oxygen', 'CO₂'), ('common salt (sodium chloride)', 'sodium and chlorine', 'NaCl'),
              ('ammonia', 'nitrogen and hydrogen', 'NH₃'), ('methane', 'carbon and hydrogen', 'CH₄'), ('iron sulphide', 'iron and sulphur', 'FeS'),
              ('calcium carbonate (limestone)', 'calcium, carbon and oxygen', 'CaCO₃'), ('magnesium oxide', 'magnesium and oxygen', 'MgO')]


def c8s2_comp(r):
    c, els, f = r.choice(c8s2_cmpds)
    pool = [x[1] for x in c8s2_cmpds if x[1] != els]
    return mcq(f'Which elements combine to form {c} ({f})?', els, r.sample(pool, 3), f'{cap(c)}, {f}, is made of {els}.', r)


c8s2_defs = [
    ('an element', 'a pure substance made of only one kind of atoms that cannot be broken into simpler substances by chemical methods'),
    ('a compound', 'a pure substance formed when two or more elements combine chemically in a fixed ratio'),
    ('an atom', 'the smallest particle of an element'),
    ('a molecule', 'a group of two or more atoms joined together; the smallest particle of a substance that can exist on its own'),
    ('a chemical symbol', 'a short form of one or two letters used to represent an element'),
]
c8s2_cats = {
    'an element': ['oxygen', 'iron', 'carbon', 'mercury', 'sulphur', 'helium'],
    'a compound': ['water', 'carbon dioxide', 'sugar', 'common salt', 'ammonia', 'baking soda'],
    'a mixture': ['air', 'brass', 'muddy water', 'milk', 'soil', 'tea'],
}
c8s2_why = [
    ('Why is water called a compound and not a mixture of hydrogen and oxygen?', 'Hydrogen and oxygen combine chemically in a fixed ratio (2 : 1 by atoms) to form water, whose properties are completely different from those of the two gases.', '1 mark: chemical combination in fixed ratio. 1 mark: new properties.'),
    ('Why can a compound not be separated into its elements by physical methods such as filtration?', 'Its elements are chemically joined; only chemical methods (such as electrolysis) can break the bonds.', '1 mark: chemical bonds. 1 mark: needs chemical method.'),
    ('Why does a molecule of oxygen (O₂) count as an element and not as a compound?', 'It contains atoms of only one kind (oxygen).', '1 mark: one kind of atom. 1 mark: compounds need two or more kinds.'),
]
c8s2_ar = [
    ('Water is a compound.', 'Water is formed by the chemical combination of hydrogen and oxygen in a fixed ratio.', 'a', 'R explains A.'),
    ('The symbol of sodium is So.', 'Some symbols come from Latin names of elements.', 'd', 'A false (Na, from natrium); R true.'),
    ('Hydrogen is a compound.', 'Hydrogen gas is made of molecules.', 'd', 'A false; R true (H₂ molecules of one kind of atom).'),
]

c8s3_mc = [
    ('When iron filings and sulphur powder are mixed (not heated), which is true?', 'A magnet can pull out the iron', 'A new substance forms', 'The mixture has a fixed composition', 'Iron loses its magnetic property'),
    ('When iron and sulphur are heated together, the product:', 'is not attracted by a magnet', 'can be separated by a magnet', 'is a mixture', 'keeps the properties of iron'),
    ('Which is a property of a compound?', 'Its elements are in a fixed ratio by mass', 'Its components can be separated by a magnet', 'It has variable composition', 'Its components keep their properties'),
    ('Energy is usually given out or taken in when:', 'a compound is formed', 'a mixture is formed', 'sand is mixed with water', 'sugar is mixed with salt'),
]
c8s3_pairs = [
    ('Composition', 'Fixed ratio of elements', 'Any ratio of components'),
    ('Properties', 'New properties, different from those of its elements', 'Components keep their own properties'),
    ('Separation', 'Only by chemical methods', 'By physical methods like filtration, magnet, evaporation'),
    ('Energy change', 'Heat/light usually given out or absorbed', 'Usually no energy change'),
    ('Melting/boiling point', 'Fixed', 'Not fixed'),
]


def c8s3_diff(r):
    k = r.sample(c8s3_pairs, 2)
    return {'stem': f'Distinguish between a compound and a mixture on the basis of {k[0][0].lower()} and {k[1][0].lower()}.',
            'answer': '; '.join(f'{p}: compound – {a}; mixture – {b}' for p, a, b in k),
            'key': '1 mark per correct point of difference.'}


c8s3_why = [
    ('Why does iron sulphide not get attracted by a magnet, though iron does?', 'Iron sulphide is a compound with new properties; the iron in it is chemically combined and no longer behaves like free iron.', '1 mark: compound. 1 mark: new properties.'),
    ('Why does a mixture of iron and sulphur in carbon disulphide leave behind iron, while the compound does not dissolve to give sulphur?', 'In a mixture, sulphur keeps its property of dissolving in carbon disulphide; in the compound sulphur is combined and the compound does not dissolve.', '1 mark: mixture keeps properties. 1 mark: compound behaves differently.'),
]
c8s3_ar = [
    ('A mixture of iron and sulphur can be separated with a magnet.', 'In a mixture, components keep their individual properties.', 'a', 'R explains A.'),
    ('Iron sulphide is attracted by a magnet.', 'Iron sulphide contains iron.', 'd', 'A false; R true—but combined iron does not show magnetism here.'),
    ('Water has a fixed boiling point.', 'Water is a compound.', 'a', 'Pure compounds have fixed boiling points; R explains A.'),
]
c8s3_hots = [
    ('Bhavna has two white powders: one is a mixture of sugar and salt, the other is pure sugar. Suggest two simple tests to tell them apart.', 'Taste a tiny bit (under supervision): the mixture is sweet and salty in parts; heat both: pure sugar melts at a fixed temperature, the mixture does not (salt remains). Also dissolve and test the solution for conduction: salt solution conducts.', '1 mark per valid test (max 2) + 1 for reasoning.'),
    ('Ammonia gas is made of nitrogen and hydrogen, both of which are odourless gases. Ammonia has a sharp smell. What does this tell us about compounds?', 'A compound has properties different from those of the elements that form it.', '1 mark: new properties. 1 mark: reasoning.'),
]

c8s4_defs = [
    ('a metal', 'an element that is usually hard, shiny, malleable, ductile and a good conductor of heat and electricity'),
    ('a non-metal', 'an element that is usually dull, brittle and a poor conductor of heat and electricity'),
    ('a metalloid', 'an element that shows some properties of metals and some of non-metals, such as silicon'),
    ('malleability', 'the property of being beaten into thin sheets'),
    ('ductility', 'the property of being drawn into thin wires'),
    ('sonority', 'the property of producing a ringing sound when struck'),
]
c8s4_cats = {
    'a metal': ['copper', 'aluminium', 'iron', 'sodium', 'mercury', 'gold', 'zinc'],
    'a non-metal': ['sulphur', 'carbon', 'oxygen', 'phosphorus', 'chlorine', 'iodine', 'nitrogen'],
    'a metalloid': ['silicon', 'boron', 'germanium', 'arsenic'],
}
c8s4_mc = [
    ('Which metal is a liquid at room temperature?', 'Mercury', 'Sodium', 'Iron', 'Zinc'),
    ('Which non-metal is a good conductor of electricity?', 'Graphite (a form of carbon)', 'Sulphur', 'Oxygen', 'Iodine'),
    ('Silicon is used in computer chips because it is a:', 'metalloid that is a semiconductor', 'metal that is very soft', 'non-metal that is a gas', 'metal that rusts'),
    ('Aluminium foil is used to wrap food because aluminium is:', 'malleable', 'brittle', 'a non-metal', 'sonorous only'),
    ('Which property makes copper suitable for electric wires?', 'It is ductile and a good conductor', 'It is brittle', 'It is a non-metal', 'It has a low melting point'),
    ('Iodine is a non-metal that:', 'has a shiny appearance', 'is a liquid', 'conducts electricity well', 'is malleable'),
]
c8s4_why = [
    ('Why are cooking utensils made of metals but their handles of plastic or wood?', 'Metals are good conductors of heat, so food cooks fast; plastic and wood are poor conductors, so the handle stays cool.', '1 mark: metals conduct heat. 1 mark: handles insulate.'),
    ('Why are school bells made of metal?', 'Metals are sonorous; they produce a ringing sound when struck.', '1 mark: sonorous. 1 mark: ringing sound.'),
    ('Why is sodium stored under kerosene?', 'It is very reactive and catches fire when exposed to air and moisture.', '1 mark: highly reactive. 1 mark: kerosene keeps air/water away.'),
]
c8s4_ar = [
    ('Gold is used to make jewellery.', 'Gold is shiny, malleable and does not corrode easily.', 'a', 'R explains A.'),
    ('Sulphur is used to make electric wires.', 'Sulphur is a non-metal and is brittle.', 'd', 'A false; R true.'),
    ('Silicon is called a metalloid.', 'Silicon shows properties of both metals and non-metals.', 'a', 'R explains A.'),
]
c8s4_hots = [
    ('You are given three unlabelled rods: copper, a graphite rod and a sulphur stick. Suggest tests to identify each using a hammer and a battery-bulb tester.', 'Copper: shiny, flattens on hammering, conducts. Graphite: dull grey, brittle but conducts. Sulphur: yellow, brittle, does not conduct.', '1 mark per correct identification with test.'),
    ('Mercury is a metal but is used in thermometers. Which two properties make it suitable?', 'It is a liquid at room temperature that expands evenly on heating, and it is shiny, so its level is easy to see; it is also a good conductor of heat, so it responds quickly.', '1 mark per property (max 2).'),
]
c8_case = [
    ('Read: In a lab, Ishaan made two samples. Sample P: iron filings and sulphur powder stirred together. Sample Q: the same mixture heated strongly till it glowed and turned into a black solid.\n'
     '(i) Which sample is a compound? (ii) What happens when a magnet is brought near each? (iii) Why did Q glow? (iv) Can sulphur be dissolved out of P using carbon disulphide?',
     '(i) Q (iron sulphide). (ii) P: iron filings attracted; Q: not attracted. (iii) Heat is given out when a compound forms. (iv) Yes, sulphur in a mixture keeps its property of dissolving.',
     '1 mark each.'),
    ('Read: A label on a packet of salt says "Iodised salt: sodium chloride with potassium iodate". A bottle of distilled water says "H₂O, 100% pure".\n'
     '(i) Is iodised salt a pure substance? (ii) Name the elements in sodium chloride. (iii) Is distilled water an element or a compound? (iv) Why is iodine added to salt?',
     '(i) No, it is a mixture. (ii) Sodium and chlorine. (iii) A compound. (iv) To prevent goitre (iodine deficiency).',
     '1 mark each.'),
]
c8_long = [
    ('Define element, compound and mixture with two examples each. Give three differences between a compound and a mixture, using iron and sulphur as an example.',
     'Element: one kind of atoms (iron, oxygen). Compound: elements chemically combined in fixed ratio (water, iron sulphide). Mixture: substances mixed in any ratio (air, iron + sulphur powder). Differences: compound has fixed composition, new properties, separated only chemically, energy change; mixture has variable composition, components keep properties (magnet attracts iron), physical separation.',
     '2 marks: definitions with examples; 3 marks: differences.'),
    ('Classify elements as metals, non-metals and metalloids. Compare metals and non-metals on any four physical properties, and give two uses each of metals and non-metals.',
     'Metals: copper, iron; non-metals: sulphur, oxygen; metalloids: silicon, boron. Metals are lustrous, malleable, ductile, sonorous, good conductors; non-metals dull, brittle, poor conductors (except graphite). Uses: copper wires, aluminium foil; oxygen for breathing, chlorine for purifying water, carbon as fuel.',
     '1 mark: classification; 2 marks: comparison; 2 marks: uses.'),
]

# ======================= ch09 Solutes, solvents and solutions
c9s1_defs = [
    ('a solution', 'a homogeneous mixture of two or more substances'),
    ('a solute', 'the substance that dissolves in a solution, usually present in smaller amount'),
    ('a solvent', 'the substance in which the solute dissolves, usually present in larger amount'),
    ('a soluble substance', 'a substance that dissolves in a given solvent'),
    ('an insoluble substance', 'a substance that does not dissolve in a given solvent'),
]
c9s1_sol = [('sugar syrup', 'sugar', 'water'), ('salt solution', 'salt', 'water'), ('lemonade', 'sugar, salt and lemon juice', 'water'),
            ('tincture of iodine', 'iodine', 'alcohol'), ('soda water', 'carbon dioxide', 'water'), ('copper sulphate solution', 'copper sulphate', 'water'),
            ('a solution of nail polish in remover', 'nail polish', 'acetone')]


def c9s1_solute(r):
    s, a, b = r.choice(c9s1_sol)
    pool = [x[1] for x in c9s1_sol if x[1] != a] + ['water', 'alcohol']
    pool = [p for p in pool if p not in (a, b)]
    return mcq(f'In {s}, the solute is:', a, [b] + r.sample(pool, 2), f'{cap(a)} dissolves in {b}; so {a} is the solute and {b} the solvent.', r)


def c9s1_solvent(r):
    s, a, b = r.choice(c9s1_sol)
    pool = ['water', 'alcohol', 'acetone', 'kerosene']
    wrong = [p for p in pool if p != b][:2] + [a]
    return mcq(f'In {s}, the solvent is:', b, wrong, f'{cap(b)} is the solvent in which {a} dissolves.', r)


c9s1_cats = {
    'soluble in water': ['sugar', 'common salt', 'copper sulphate', 'baking soda', 'glucose', 'alum'],
    'insoluble in water': ['sand', 'chalk powder', 'sawdust', 'iron filings', 'wax', 'coconut oil'],
}
c9s1_mc = [
    ('Water is called a universal solvent because:', 'it dissolves a large number of substances', 'it dissolves every substance', 'it is found everywhere', 'it has no colour'),
    ('Oil paint stains are removed with turpentine because:', 'oil paint dissolves in turpentine but not in water', 'turpentine is water', 'oil paint is soluble in water', 'turpentine is a solute'),
    ('Which of these increases the rate at which sugar dissolves?', 'Stirring and using powdered sugar', 'Using sugar lumps and cold water', 'Keeping it still', 'Adding more sugar'),
    ('Aquatic animals breathe oxygen that is:', 'dissolved in water', 'from the bottom mud', 'in solid form', 'made by fish themselves'),
]
c9s1_why = [
    ('Why is water important for living organisms as a solvent?', 'Nutrients, gases and wastes dissolve in water and are carried in blood and plant sap; reactions in cells take place in water.', '1 mark: transport of dissolved substances. 1 mark: reactions.'),
    ('Why does powdered sugar dissolve faster than a sugar cube?', 'Powder has a larger surface area in contact with water, so particles mix with water faster.', '1 mark: surface area. 1 mark: faster mixing.'),
]
c9s1_ar = [
    ('Water dissolves many substances.', 'Water is called a universal solvent.', 'b', 'Both true; R is a name given because of A, not the explanation.'),
    ('Sand dissolves in water when stirred.', 'Stirring helps soluble substances dissolve faster.', 'd', 'A false; R true.'),
    ('A solution is a homogeneous mixture.', 'The solute particles are evenly spread in the solvent.', 'a', 'R explains A.'),
]

c9s2_defs = [
    ('a saturated solution', 'a solution in which no more solute can be dissolved at a given temperature'),
    ('an unsaturated solution', 'a solution in which more solute can be dissolved at the given temperature'),
    ('solubility', 'the maximum amount of a solute that can dissolve in 100 g of a solvent at a given temperature'),
    ('crystallisation', 'the process of getting pure crystals of a substance by cooling a hot saturated solution'),
]
# NCERT Class 9 (Is Matter Around Us Pure) solubility table, g per 100 g water
SOLUB = {'potassium nitrate': {20: 32, 40: 62, 60: 106}, 'common salt': {20: 36, 40: 36, 60: 37},
         'potassium chloride': {20: 35, 40: 40, 60: 46}, 'ammonium chloride': {20: 37, 40: 41, 60: 55}}


def c9s2_sat(r):
    s = r.choice(list(SOLUB))
    T = r.choice([20, 40, 60])
    sol = SOLUB[s][T]
    w = r.choice([50, 100, 200])
    need = sol * w / 100
    return {'stem': f'The solubility of {s} in water at {T} °C is {num(sol, 1)} g per 100 g of water. What mass of {s} is needed to make a saturated solution in {w} g of water at {T} °C?',
            'answer': f'{num(need, 1)} g', 'key': f'Mass = {num(sol, 1)} × {w} ÷ 100 = {num(need, 1)} g.', 'distractors': num_distractors(need, sol, need * 2, sol + w, dp=1)}


def c9s2_cool(r):
    T1, T2 = 60, r.choice([20, 40])
    s = 'potassium nitrate'
    a, b = SOLUB[s][T1], SOLUB[s][T2]
    return {'stem': f'A saturated solution of potassium nitrate in 100 g of water is made at {T1} °C (solubility {a} g) and cooled to {T2} °C (solubility {b} g). What mass of crystals separates out? Name the process.',
            'answer': f'{num(a - b, 1)} g; crystallisation', 'key': f'{a} − {b} = {num(a - b, 1)} g comes out as crystals on cooling (crystallisation).',
            'distractors': [f'{a + b} g; crystallisation', f'{b} g; evaporation', f'{a} g; condensation']}


c9s2_mc = [
    ('How can you test whether a sugar solution is saturated?', 'Add a little more sugar and stir; if it does not dissolve, it is saturated', 'Taste it', 'Check its colour', 'Measure its volume'),
    ('The solubility of most solids in water ______ with an increase in temperature.', 'increases', 'decreases', 'stays the same', 'becomes zero'),
    ('The solubility of gases in water ______ as temperature rises.', 'decreases', 'increases', 'stays the same', 'doubles'),
    ('A saturated solution of sugar at 30 °C is heated to 60 °C. It becomes:', 'unsaturated', 'more saturated', 'a suspension', 'a pure substance'),
    ('Which salt\'s solubility changes the least with temperature?', 'Common salt', 'Potassium nitrate', 'Ammonium chloride', 'Potassium chloride'),
]
c9s2_why = [
    ('Why do fish in ponds sometimes come up to the surface on very hot summer days?', 'Less oxygen dissolves in warm water, so there is less oxygen for fish deep in the pond.', '1 mark: gas solubility falls with temperature. 1 mark: less oxygen.'),
    ('Why does a cold bottle of soda water fizz more when it warms up after opening?', 'Carbon dioxide is less soluble in warm water, so it escapes as bubbles.', '1 mark: less soluble when warm. 1 mark: CO₂ escapes.'),
    ('Why do crystals appear when a hot saturated solution of alum is cooled?', 'Solubility decreases on cooling, so the extra solute can no longer stay dissolved and separates as crystals.', '1 mark: solubility falls. 1 mark: excess separates.'),
]
c9s2_ar = [
    ('More sugar dissolves in hot water than in cold water.', 'Solubility of most solids increases with temperature.', 'a', 'R explains A.'),
    ('A saturated solution can dissolve more solute at the same temperature.', 'A saturated solution holds the maximum solute at that temperature.', 'd', 'A false; R true.'),
    ('Aquatic animals face difficulty in warm water.', 'Oxygen is less soluble in warm water.', 'a', 'R explains A.'),
]

c9s3_defs = [
    ('the concentration of a solution', 'the amount of solute present in a given amount of the solution'),
    ('a dilute solution', 'a solution that contains a small amount of solute in a large amount of solvent'),
    ('a concentrated solution', 'a solution that contains a large amount of solute in a given amount of solvent'),
    ('mass by mass percentage', 'the mass of solute in grams present in 100 g of solution'),
]


def c9s3_mm(r):
    a = r.choice([5, 8, 10, 12, 15, 20, 25, 30, 40])
    w = r.choice([45, 60, 75, 85, 90, 100, 120, 160, 175, 200])
    c = 100 * a / (a + w)
    who = name(r)
    return {'stem': f'{who} dissolves {a} g of salt in {w} g of water. Calculate the concentration of the solution as mass by mass percentage.',
            'answer': f'{sig(c, 3)}%', 'key': f'Mass of solution = {a} + {w} = {a + w} g; concentration = {a} ÷ {a + w} × 100 = {sig(c, 3)}%.',
            'distractors': [f'{sig(100 * a / w, 3)}%', f'{sig(c / 2, 3)}%', f'{a}%'], 'gap': 'G2'}


def c9s3_mass(r):
    c = r.choice([2, 4, 5, 8, 10, 12, 15, 20])
    m = r.choice([50, 100, 150, 200, 250, 400, 500])
    s = c * m / 100
    return {'stem': f'How much sugar and how much water are needed to make {m} g of a {c}% (mass by mass) sugar solution?',
            'answer': f'{num(s, 1)} g sugar and {num(m - s, 1)} g water', 'key': f'Sugar = {c} × {m} ÷ 100 = {num(s, 1)} g; water = {m} − {num(s, 1)} = {num(m - s, 1)} g.',
            'distractors': [f'{c} g sugar and {m} g water', f'{num(s, 1)} g sugar and {m} g water', f'{num(m - s, 1)} g sugar and {num(s, 1)} g water']}


def c9s3_mv(r):
    a = r.choice([2, 5, 10, 15, 20, 25])
    v = r.choice([100, 200, 250, 500])
    c = 100 * a / v
    return {'stem': f'{a} g of glucose is dissolved in water to make {v} mL of solution. What is the concentration as mass by volume percentage?',
            'answer': f'{num(c, 2)}%', 'key': f'Concentration = {a} ÷ {v} × 100 = {num(c, 2)}% (g per 100 mL).', 'distractors': [f'{num(c * 10, 2)}%', f'{num(c / 10, 3)}%', f'{num(a + c, 2)}%']}


def c9s3_compare(r):
    a, b = two_names(r)
    s1, w1 = r.choice([(10, 90), (20, 180), (15, 85), (12, 88)])
    s2, w2 = r.choice([(30, 170), (25, 225), (18, 132), (40, 160)])
    c1, c2 = 100 * s1 / (s1 + w1), 100 * s2 / (s2 + w2)
    if abs(c1 - c2) < 0.5:
        raise ValueError
    more = a if c1 > c2 else b
    return {'stem': f'{a} dissolves {s1} g of sugar in {w1} g of water. {b} dissolves {s2} g of sugar in {w2} g of water. Whose solution is more concentrated? Show your working.',
            'answer': f"{more}'s solution", 'key': f'{a}: {s1}/{s1 + w1} × 100 = {sig(c1, 3)}%; {b}: {s2}/{s2 + w2} × 100 = {sig(c2, 3)}%. {more}\'s is more concentrated.',
            'distractors': [f"{a if more == b else b}'s solution", 'Both are equally concentrated', 'Cannot be compared']}


c9s3_mc = [
    ('Adding more water to a salt solution makes it:', 'more dilute', 'more concentrated', 'saturated', 'a suspension'),
    ('A 10% sugar solution means:', '10 g of sugar in 100 g of solution', '10 g of sugar in 100 g of water', '100 g of sugar in 10 g of water', '10 g of water in 100 g of sugar'),
    ('ORS for a patient with diarrhoea must be made with the correct concentration because:', 'too much or too little salt and sugar can harm the patient', 'concentration does not matter', 'water alone is enough', 'more sugar is always better'),
]
c9s3_why = [
    ('Why is it more useful to state the concentration of a solution as a percentage rather than as "strong" or "weak"?', 'A percentage gives an exact, comparable amount of solute; "strong" or "weak" is vague and differs from person to person.', '1 mark: exact. 1 mark: comparable.'),
    ('Two cups of tea look different in colour. What does this tell you about their concentrations?', 'The darker cup has more dissolved tea (solute) per amount of water, so it is more concentrated.', '1 mark: more solute. 1 mark: concentration.'),
]
c9s3_ar = [
    ('A 20% salt solution is more concentrated than a 5% salt solution.', 'Concentration tells the amount of solute in a given amount of solution.', 'a', 'R explains A.'),
    ('Dissolving 10 g of salt in 100 g of water gives a 10% solution.', 'The mass of the solution is the sum of the masses of solute and solvent.', 'd', 'A false: 10/110 × 100 ≈ 9.1%; R true.'),
    ('Adding water to a solution changes its concentration.', 'The amount of solute stays the same while the amount of solution increases.', 'a', 'R explains A.'),
]

c9s4_defs = [
    ('density', 'the mass per unit volume of a substance'),
    ('relative density', 'the ratio of the density of a substance to the density of water'),
    ('buoyant force', 'the upward force exerted by a liquid on an object placed in it'),
]


def c9s4_d(r):
    obj = r.choice([('a block of wood', 0.6), ('an iron bolt', 7.8), ('a piece of aluminium', 2.7), ('a stone', 2.5), ('a candle', 0.9), ('a cork', 0.25), ('a glass marble', 2.6), ('a plastic toy', 1.2)])
    d = obj[1]
    V = r.choice([10, 20, 25, 40, 50, 80, 100, 120])
    m = d * V
    fl = 'float' if d < 1 else 'sink'
    return {'stem': f'{cap(obj[0])} has a mass of {num(m, 1)} g and a volume of {V} cm³. Find its density. Will it float or sink in water (density 1 g/cm³)?',
            'answer': f'{num(d, 2)} g/cm³; it will {fl}', 'key': f'Density = mass ÷ volume = {num(m, 1)} ÷ {V} = {num(d, 2)} g/cm³; {"less" if d < 1 else "more"} than water, so it {fl}s.',
            'distractors': [f'{num(V / m, 3)} g/cm³; it will {"sink" if fl == "float" else "float"}', f'{num(m * V, 1)} g/cm³; it will sink', f'{num(d, 2)} g/cm³; it will {"sink" if fl == "float" else "float"}']}


def c9s4_m(r):
    sub = r.choice([('milk', 1.03), ('coconut oil', 0.92), ('kerosene', 0.8), ('sea water', 1.025), ('mercury', 13.6), ('honey', 1.4)])
    V = r.choice([50, 100, 200, 250, 500])
    m = sub[1] * V
    return {'stem': f'The density of {sub[0]} is {sub[1]} g/mL. What is the mass of {V} mL of {sub[0]}?', 'answer': f'{num(m, 1)} g',
            'key': f'Mass = density × volume = {sub[1]} × {V} = {num(m, 1)} g.', 'distractors': num_distractors(m, V / sub[1], V, sub[1] + V, dp=1)}


c9s4_float = {
    'an object that floats in water': ['a cork', 'a dry leaf', 'ice', 'a wooden spoon', 'a plastic bottle cap', 'coconut oil drops'],
    'an object that sinks in water': ['an iron nail', 'a stone', 'a coin', 'a glass marble', 'a steel spoon', 'a lump of clay'],
}
c9s4_mc = [
    ('An egg sinks in tap water but floats in strong salt water because:', 'salt water is denser than the egg', 'the egg becomes lighter', 'salt reacts with the shell', 'salt water has less buoyancy'),
    ('Ice floats on water because:', 'ice is less dense than water', 'ice is denser than water', 'ice has no mass', 'water pushes ice down'),
    ('The SI unit of density is:', 'kg/m³', 'kg·m³', 'N/m²', 'm/s²'),
    ('A ship made of iron floats because:', 'its hollow shape makes its average density less than that of water', 'iron is lighter than water', 'water has no pressure', 'iron does not have mass'),
    ('Oil floats on water. This shows that oil:', 'has a lower density than water', 'is heavier than water', 'dissolves in water', 'has a higher density'),
]
c9s4_why = [
    ('Why is it easier to float in the sea than in a river?', 'Sea water is denser because of dissolved salts, so it pushes up with a greater buoyant force.', '1 mark: denser. 1 mark: greater buoyant force.'),
    ('A lump of clay sinks, but the same clay shaped into a bowl floats. Explain.', 'The bowl shape encloses air, so it displaces more water; its overall density becomes less than water.', '1 mark: shape/displaces more water. 1 mark: average density less.'),
]
c9s4_ar = [
    ('An iron nail sinks in water.', 'The density of iron is greater than that of water.', 'a', 'R explains A.'),
    ('A heavy log of wood floats on water.', 'Wood is less dense than water.', 'a', 'Floating depends on density, not just weight; R explains A.'),
    ('Ice sinks in water.', 'Ice is less dense than water.', 'd', 'A false; R true.'),
]
c9s4_hots = [
    ('A lactometer shows that a milk sample has a density of 1.01 g/mL, while pure milk is about 1.03 g/mL. What can you conclude? Explain.', 'The milk has probably been diluted with water (density 1.00 g/mL), lowering its density.', '1 mark: adulterated with water. 1 mark: reason.'),
    ('Arrange honey, water and coconut oil in layers in a glass, from bottom to top, and explain your order using densities (honey 1.4, water 1.0, coconut oil 0.92 g/mL).', 'Bottom: honey; middle: water; top: coconut oil. Denser liquids sink below less dense ones.', '1 mark: order. 1 mark: reason.'),
]
c9_case = [
    ('Read: A health worker in a village prepares ORS by dissolving 2.6 g of salt and 13.5 g of glucose in clean water to make 1 litre (1000 mL) of solution.\n'
     '(i) Name the solvent and the solutes. (ii) Find the concentration of glucose as mass by volume %. (iii) Is the solution homogeneous? (iv) Why must boiled and cooled water be used?',
     '(i) Solvent: water; solutes: salt and glucose. (ii) 13.5 ÷ 1000 × 100 = 1.35%. (iii) Yes. (iv) To kill germs so the patient is not infected again.',
     '1 mark each.'),
    ('Read: Students added sugar spoon by spoon to 100 mL of water at room temperature, stirring each time. After 18 spoons, sugar settled at the bottom. On heating, it dissolved, and more sugar could be added.\n'
     '(i) What kind of solution was formed after 18 spoons? (ii) What did heating show? (iii) What will happen on cooling the hot solution? (iv) Name one use of this process.',
     '(i) A saturated solution. (ii) Solubility of sugar increases with temperature. (iii) Excess sugar will separate out as crystals. (iv) Making sugar crystals/purifying substances (crystallisation).',
     '1 mark each.'),
]
c9_long = [
    ('Explain the terms solute, solvent, saturated solution and concentration with examples. Calculate the mass of salt needed to make 250 g of a 4% (mass by mass) salt solution, and the mass of water.',
     'Solute: substance that dissolves (salt); solvent: substance in which it dissolves (water); saturated: no more solute dissolves at that temperature; concentration: amount of solute in a given amount of solution. Salt = 4 × 250 ÷ 100 = 10 g; water = 240 g.',
     '3 marks: terms; 2 marks: calculation.'),
    ('What is density? A metal block has mass 540 g and volume 200 cm³. Find its density and state whether it floats in water and in mercury (13.6 g/cm³). Explain why a ship made of steel floats.',
     'Density = mass per unit volume. 540 ÷ 200 = 2.7 g/cm³ (aluminium). Sinks in water (1 g/cm³) but floats on mercury. A ship is hollow, so its average density (steel + air) is less than water.',
     '1 mark: definition; 2 marks: calculation and predictions; 2 marks: ship.'),
]

FAMILIES = {
    S + '05-st1': [TERM(c5s1_defs), DEF(c5s1_defs), CLS(c5s1_effects, 'Which of the following shows that a force can cause {}?', C='C2', D='D2'),
                   MC(c5s1_mc, C='C2', D='D2'), SA(c5s1_why), ARF(c5s1_ar), G('C3', 'D2', 'numerical', c5s1_net), G('C3', 'D3', 'numerical', c5s1_net),
                   SORT(c5s1_effects, 'Sort these by the effect of force they show — {A} or {B}: {L}.', C='C3', D='D3', n=(2, 2)),
                   SA(c5s1_hots, C='C4', D='D4', type='multi_step'), CASE(c5_case[:1]), LONG(c5_long, C='C4', D='D4')],
    S + '05-st2': [TERM(c5s2_defs), DEF(c5s2_defs), MC(c5s2_mc, C='C1', D='D2'), SA(c5s2_why), ARF(c5s2_ar), G('C3', 'D3', 'explain', c5s5_surface),
                   SA(c5s2_hots, C='C4', D='D3', type='explain')],
    S + '05-st3': [TERM(c5s3_defs), DEF(c5s3_defs), CLS(c5s3_cats, 'Which of the following is an example of {}?', C='C2', D='D2'), MC(c5s3_mc, C='C1', D='D2'),
                   SA(c5s3_why), ARF(c5s3_ar), SORT(c5s3_cats, 'Classify these as {A} or {B}: {L}.', C='C3', D='D3', n=(2, 2)),
                   CLS(c5s3_cats, 'Which of the following is an example of {}?', C='C3', D='D2', neg=True), SA(c5s3_hots, C='C4', D='D4', type='multi_step')],
    S + '05-st4': [DEF(c5s4_defs), MC(c5s4_mc, C='C1', D='D2'), SA(c5s4_why), ARF(c5s4_ar), G('C3', 'D1', 'numerical', c5s4_weight),
                   G('C3', 'D3', 'numerical', c5s4_moon), G('C3', 'D4', 'numerical', c5s4_spring), G('C4', 'D3', 'multi_step', c5s4_moon), G('C4', 'D4', 'numerical', c5s4_spring),
                   G('C2', 'D2', 'mcq', c5s4_weight)],
    S + '05-st5': [TERM(c5s5_defs), DEF(c5s5_defs), CLS(c5s5_cats, 'Which of the following is {}?', C='C2', D='D2'), MC(c5s5_mc, C='C1', D='D2'),
                   SA(c5s5_why), ARF(c5s5_ar), SORT(c5s5_cats, 'Sort these into {A} and {B}: {L}.', C='C3', D='D3', n=(2, 3)),
                   CLS(c5s5_cats, 'Which of the following is {}?', C='C3', D='D2', neg=True), G('C4', 'D3', 'explain', c5s5_surface), CASE(c5_case[1:], C='C4', D='D4')],
    S + '06-st1': [TERM(c6s1_defs + c6s2_defs), DEF(c6s1_defs), MC(c6s1_mc, C='C2', D='D2'), SA(c6s1_why), ARF(c6s1_ar), G('C3', 'D1', 'numerical', c6s1_p),
                   G('C3', 'D2', 'numerical', c6s1_p), G('C3', 'D3', 'numerical', c6s1_force), G('C3', 'D4', 'multi_step', c6s1_brick), G('C4', 'D5', 'multi_step', c6s1_brick),
                   SA(c6s1_hots, C='C4', D='D3', type='explain'), LONG(c6_long, C='C4', D='D4'), G('C1', 'D2', 'mcq', c6s1_p)],
    S + '06-st2': [DEF(c6s2_defs), MC(c6s2_mc, C='C1', D='D2'), SA(c6s2_why), ARF(c6s2_ar),                    SA(c6s2_hots, C='C4', D='D4', type='multi_step'), CASE(c6_case[1:], C='C3', D='D3')],
    S + '06-st3': [TERM(c6s3_defs), DEF(c6s3_defs), MC(c6s3_mc, C='C2', D='D2'), SA(c6s3_why), ARF(c6s3_ar), SA(c6s3_hots, C='C4', D='D3', type='explain')],
    S + '06-st4': [TERM(c6s4_defs), DEF(c6s4_defs), MC(c6s4_mc, C='C1', D='D2'), SA(c6s4_why), ARF(c6s4_ar), SA(c6s4_hots, C='C4', D='D4', type='multi_step'),
                   CASE(c6_case[:1])],
    S + '07-st1': [TERM(c7s1_defs), DEF(c7s1_defs), MC(c7s1_mc, C='C2', D='D2'), SA(c7s1_why), ARF(c7s1_ar), G('C3', 'D3', 'explain', c7s1_dilute),
                   SA(c7s1_hots, C='C4', D='D4', type='multi_step'), CASE(c7_case)],
    S + '07-st2': [TERM(c7s2_defs), DEF(c7s2_defs), CLS(c7s2_cats, 'Which of the following is {} at room temperature?', C='C1', D='D1'), MC(c7s2_cmp, C='C2', D='D2'),
                   SA(c7s2_why), ARF(c7s2_ar), SORT(c7s2_cats, 'Classify as {A} or {B} at room temperature: {L}.', C='C3', D='D2', n=(2, 3)),
                   CLS(c7s2_cats, 'Which of the following is {} at room temperature?', C='C3', D='D3', neg=True), SA(c7s2_hots, C='C4', D='D4', type='multi_step'),
                   LONG(c7_long, C='C4', D='D3')],
    S + '07-st3': [TERM(c7s3_defs), DEF(c7s3_defs), MC(c7s3_mc, C='C2', D='D2'), SA(c7s3_why), ARF(c7s3_ar), SA(c7s3_hots, C='C4', D='D4', type='multi_step')],
    S + '07-st4': [TERM(c7s4_defs), DEF(c7s4_defs), CLS(c7s4_cats, 'Which of the following is {}?', C='C3', D='D2'), MC(c7s4_mc, C='C2', D='D2'),
                   SA(c7s4_why), ARF(c7s4_ar), G('C3', 'D3', 'multi_step', c7s4_graph), SORT(c7s4_cats, 'Classify these changes as {A} or {B}: {L}.', C='C3', D='D3', n=(2, 2)),
                   SA(c7s4_hots, C='C4', D='D4', type='explain'), G('C4', 'D3', 'case', c7s4_graph)],
    S + '08-st1': [TERM(c8s1_defs), DEF(c8s1_defs), CLS(c8s1_cats, 'Which of the following is {}?', C='C2', D='D2'), CLS(c8s1_hh, 'Which of the following is {}?', C='C3', D='D2'),
                   MC(c8s1_mc, C='C1', D='D2'), SA(c8s1_why), ARF(c8s1_ar), SORT(c8s1_hh, 'Classify these mixtures as {A} or {B}: {L}.', C='C3', D='D3')],
    S + '08-st2': [TERM(c8s2_defs), DEF(c8s2_defs), G('C1', 'D1', 'mcq', c8s2_sym), G('C1', 'D2', 'mcq', c8s2_name), G('C2', 'D2', 'mcq', c8s2_comp),
                   CLS(c8s2_cats, 'Which of the following is {}?', C='C3', D='D2'), SA(c8s2_why), ARF(c8s2_ar),
                   SORT(c8s2_cats, 'Classify these substances as {A} or {B}: {L}.', C='C3', D='D3'), CLS(c8s2_cats, 'Which of the following is {}?', C='C3', D='D3', neg=True),
                   LONG(c8_long, C='C4', D='D4')],
    S + '08-st3': [MC(c8s3_mc, C='C1', D='D2'), G('C2', 'D2', 'explain', c8s3_diff), SA(c8s3_why), ARF(c8s3_ar), G('C3', 'D3', 'explain', c8s3_diff),
                   SA(c8s3_hots, C='C4', D='D4', type='multi_step'), CASE(c8_case)],
    S + '08-st4': [TERM(c8s4_defs), DEF(c8s4_defs), CLS(c8s4_cats, 'Which of the following elements is {}?', C='C1', D='D1'), MC(c8s4_mc, C='C2', D='D2'),
                   SA(c8s4_why), ARF(c8s4_ar), SORT(c8s4_cats, 'Classify these elements as {A} or {B}: {L}.', C='C3', D='D2'),
                   CLS(c8s4_cats, 'Which of the following elements is {}?', C='C3', D='D3', neg=True), SA(c8s4_hots, C='C4', D='D4', type='multi_step')],
    S + '09-st1': [TERM(c9s1_defs), DEF(c9s1_defs), G('C1', 'D2', 'mcq', c9s1_solute), G('C2', 'D2', 'mcq', c9s1_solvent), CLS(c9s1_cats, 'Which of these substances is {}?', C='C3', D='D1'),
                   MC(c9s1_mc, C='C2', D='D2'), SA(c9s1_why), ARF(c9s1_ar), SORT(c9s1_cats, 'Sort these into substances {A} and {B}: {L}.', C='C3', D='D2')],
    S + '09-st2': [TERM(c9s2_defs), DEF(c9s2_defs), MC(c9s2_mc, C='C1', D='D2'), SA(c9s2_why), ARF(c9s2_ar), G('C3', 'D3', 'numerical', c9s2_sat),
                   G('C3', 'D4', 'numerical', c9s2_cool), G('C4', 'D3', 'numerical', c9s2_sat), CASE(c9_case[1:], C='C4', D='D4'), G('C2', 'D2', 'mcq', c9s2_cool)],
    S + '09-st3': [TERM(c9s3_defs), DEF(c9s3_defs), MC(c9s3_mc, C='C1', D='D2'), SA(c9s3_why), ARF(c9s3_ar), G('C3', 'D2', 'numerical', c9s3_mm),
                   G('C3', 'D3', 'numerical', c9s3_mass), G('C3', 'D1', 'numerical', c9s3_mv), G('C3', 'D4', 'multi_step', c9s3_compare), G('C4', 'D4', 'multi_step', c9s3_compare),
                   G('C4', 'D3', 'numerical', c9s3_mass), CASE(c9_case[:1]), LONG(c9_long, C='C4', D='D4'), G('C2', 'D2', 'mcq', c9s3_mm)],
    S + '09-st4': [TERM(c9s4_defs + c9s3_defs[:2]), DEF(c9s4_defs), MC(c9s4_mc, C='C2', D='D2'), CLS(c9s4_float, 'Which of the following is {}?', C='C1', D='D2'),
                   SA(c9s4_why), ARF(c9s4_ar), G('C3', 'D2', 'numerical', c9s4_d), G('C3', 'D3', 'numerical', c9s4_m), G('C4', 'D4', 'multi_step', c9s4_d),
                   SA(c9s4_hots, C='C4', D='D3', type='explain')],
}


# ----------------------------------------------------------------- application (C3) and higher-order (C4) items
A3 = {}
A3['06-st3'] = [
    ('Why does smoke from a chimney rise straight up on a calm day but bend towards the land on a summer afternoon at a seaside town?', 'Hot smoke rises because warm air is less dense; in the afternoon, a sea breeze blows from sea to land and pushes the smoke inland.', '1 mark: rising hot air. 1 mark: sea breeze.'),
    ('Where should an air conditioner and a room heater be placed in a room—high or low? Explain.', 'AC high on the wall: cool air sinks and spreads; heater low near the floor: warm air rises and circulates.', '1 mark each with reason.'),
]
A3['06-st4'] = [
    ('IMD warns of a thunderstorm in your town during school hours. List three things students playing in the ground should do.', 'Go indoors quickly into a building; avoid standing under trees or near poles; stay away from metal fences and water; if caught outside, squat low with feet together.', '1 mark per action (max 3).'),
    ('Explain why cyclones weaken quickly after they move over land.', 'Over land they lose their supply of warm, moist air from the sea, which provided the heat energy; friction with land also slows the winds.', '1 mark: loss of moisture/heat. 1 mark: friction.'),
]
A3['07-st3'] = [
    ('Why is it possible to fill a lot of air into a football with a pump, but impossible to fill much water into a full bottle?', 'Air particles have large spaces and can be pushed closer (compressed); water particles are already close and cannot be compressed much.', '1 mark: air compressible. 1 mark: water not.'),
    ('Explain why a wooden block keeps its shape but water poured from a jug takes the shape of a glass.', 'Particles in wood are held by strong attraction in fixed positions; in water the attraction is weaker and particles can slide over one another, so it flows.', '1 mark: strong attraction in solid. 1 mark: liquid flows.'),
]
A4 = {}
A4['08-st1'] = [
    ('A shopkeeper sells "pure ghee" that melts over a wide range of temperatures instead of at one fixed point. What can you conclude, and why?', 'It is probably adulterated (a mixture); a pure substance melts at a fixed temperature, but a mixture melts over a range.', '1 mark: mixture/adulterated. 1 mark: fixed melting point reasoning.'),
    ('Plan how you would separate a mixture of salt, sand and iron filings, naming the property used at each step.', 'Use a magnet to remove iron filings (magnetic); add water and stir to dissolve salt (solubility); filter to remove sand (insoluble); evaporate the filtrate to get salt.', '1 mark per correct step with property (max 3).'),
]
A4['09-st1'] = [
    ('Iodine does not dissolve easily in water, yet a doctor\'s "tincture of iodine" is a clear solution. Explain, and say what this tells us about solvents.', 'Tincture of iodine is iodine dissolved in alcohol; different solvents dissolve different solutes, so water is not a solvent for everything.', '1 mark: alcohol solvent. 1 mark: conclusion.'),
    ('Suggest a quick test to find which of three white powders—sugar, chalk and baking soda—is insoluble in water, and how you could then tell the other two apart.', 'Stir each in water: chalk does not dissolve (milky). Of the two that dissolve, add a few drops of lemon juice or vinegar: baking soda fizzes (CO₂), sugar does not.', '1 mark: solubility test. 1 mark: second test. 1 mark: reasoning.'),
]
for _k, _v in A3.items():
    FAMILIES[S + _k].append(SA(_v, C='C3', D='D3', type='explain'))
for _k, _v in A4.items():
    FAMILIES[S + _k].append(SA(_v, C='C4', D='D4', type='multi_step'))


# ----------------------------------------------------------------- data-based case generators
def c5_spring_case(r):
    who = name(r)
    k = r.choice([1, 1.5, 2, 2.5])  # cm per N
    loads = [1, 2, 3, 4]
    ext = [k * x for x in loads]
    m = r.choice([0.5, 0.6, 0.8])
    w = m * g
    return {'stem': (f'Read: {who} hung different weights on a spring balance and noted the stretch of the spring: '
                     + '; '.join(f'{x} N – {num(e, 1)} cm' for x, e in zip(loads, ext)) +
                     f'.\n(i) How much does the spring stretch for each newton? (ii) What stretch would a 6 N weight produce? '
                     f'(iii) A packet of mass {num(m, 1)} kg is hung from it. Find its weight (g = 9.8 m/s²) and the stretch. (iv) Would the stretch be more, less or the same on the Moon? Why?'),
            'answer': f'(i) {num(k, 1)} cm per N. (ii) {num(6 * k, 1)} cm. (iii) {num(w, 2)} N; about {num(w * k, 1)} cm. (iv) Less, because the Moon pulls the packet with about one-sixth of the force.',
            'key': '1 mark each part.'}


def c6_pressure_case(r):
    who = name(r)
    W = r.choice([400, 450, 500, 550, 600])
    shoe = r.choice([0.02, 0.025, 0.03])
    ski = r.choice([0.3, 0.4, 0.5])
    p1, p2 = W / shoe, W / ski
    return {'stem': (f'Read: {who}, of weight {W} N, stands in soft snow in Gulmarg. The total area of the soles of the boots is {num(shoe, 3)} m², '
                     f'and the total area of a pair of skis is {num(ski, 2)} m².\n(i) Find the pressure on the snow with boots. (ii) Find the pressure with skis. '
                     f'(iii) In which case will {who} sink less, and why? (iv) Give one other example where a larger area is used to reduce pressure.'),
            'answer': f'(i) {num(p1)} Pa. (ii) {num(p2, 1)} Pa. (iii) With skis: the same weight acts on a larger area, so pressure is less. (iv) Wide straps of school bags / broad tyres of tractors / camel\'s broad feet.',
            'key': '1 mark each part.'}


def c9_solub_case(r):
    s = r.choice(['potassium nitrate', 'ammonium chloride', 'potassium chloride'])
    t = SOLUB[s]
    w = r.choice([50, 100, 200])
    return {'stem': (f'Read: The solubility of {s} (g per 100 g of water) is: 20 °C – {t[20]} g; 40 °C – {t[40]} g; 60 °C – {t[60]} g.\n'
                     f'(i) How does solubility change with temperature? (ii) What mass of {s} will make a saturated solution in {w} g of water at 40 °C? '
                     f'(iii) A saturated solution in 100 g of water at 60 °C is cooled to 20 °C. What mass of crystals forms? (iv) Name this method of getting crystals.'),
            'answer': f'(i) It increases with temperature. (ii) {num(t[40] * w / 100, 1)} g. (iii) {t[60]} − {t[20]} = {t[60] - t[20]} g. (iv) Crystallisation.',
            'key': '1 mark each part.'}


FAMILIES[S + '05-st4'].append(G('C4', 'D4', 'case', c5_spring_case, gap='G7'))
FAMILIES[S + '06-st1'].append(G('C4', 'D3', 'case', c6_pressure_case, gap='G7'))
FAMILIES[S + '09-st2'].append(G('C4', 'D3', 'case', c9_solub_case, gap='G7'))
