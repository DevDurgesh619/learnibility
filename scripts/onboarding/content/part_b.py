"""Part B reasoning: 16 items (4 numerical, 4 verbal, 4 abstract pattern, 4 spatial), three age bands.

Abstract and spatial items are fully described in words; a few also carry a simple SVG.
Verbal deduction items also feed p65 (logical deduction). Every item feeds p69 via its target time.
"""

def R(domain, d, stem, correct, wrong, why, seconds, extra=None, svg=None):
    base = {'numerical': ['p62', 'p68'], 'verbal': ['p61'], 'abstract': ['p63'], 'spatial': ['p64']}[domain]
    it = {'domain': domain, 'difficulty': d, 'stem': stem, 'options': [correct] + wrong, 'answer': correct,
          'explanation': why, 'seconds': seconds, 'paramIds': base + (extra or []) + ['p69']}
    if svg:
        it['svg'] = svg
    return it


SHAPES_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 60" width="300" height="60">'
              '<circle cx="30" cy="30" r="20" fill="none" stroke="currentColor" stroke-width="3"/>'
              '<rect x="70" y="10" width="40" height="40" fill="none" stroke="currentColor" stroke-width="3"/>'
              '<polygon points="150,10 172,50 128,50" fill="none" stroke="currentColor" stroke-width="3"/>'
              '<circle cx="210" cy="30" r="20" fill="none" stroke="currentColor" stroke-width="3"/>'
              '<text x="270" y="40" font-size="28" text-anchor="middle" fill="currentColor">?</text></svg>')

GRID_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" width="180" height="180" '
            'stroke="currentColor" fill="none" stroke-width="2">'
            '<rect x="0" y="0" width="180" height="180"/><line x1="60" y1="0" x2="60" y2="180"/>'
            '<line x1="120" y1="0" x2="120" y2="180"/><line x1="0" y1="60" x2="180" y2="60"/>'
            '<line x1="0" y1="120" x2="180" y2="120"/>'
            '<circle cx="30" cy="30" r="18"/><rect x="72" y="12" width="36" height="36"/>'
            '<polygon points="150,12 168,48 132,48"/>'
            '<polygon points="30,72 48,108 12,108"/><circle cx="90" cy="90" r="18"/>'
            '<rect x="132" y="72" width="36" height="36"/>'
            '<text x="90" y="160" font-size="28" text-anchor="middle" fill="currentColor" stroke="none">?</text></svg>')

DIE_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 140" width="160" height="140" '
           'stroke="currentColor" fill="none" stroke-width="2">'
           '<polygon points="20,40 100,40 100,120 20,120"/><polygon points="20,40 50,15 130,15 100,40"/>'
           '<polygon points="100,40 130,15 130,95 100,120"/>'
           '<text x="60" y="88" font-size="26" text-anchor="middle" fill="currentColor" stroke="none">2</text>'
           '<text x="75" y="34" font-size="18" text-anchor="middle" fill="currentColor" stroke="none">1</text>'
           '<text x="115" y="75" font-size="20" text-anchor="middle" fill="currentColor" stroke="none">3</text></svg>')

G8 = [
    R('numerical', 'D1', 'What number comes next? 3, 7, 11, 15, ?', '19', ['18', '21', '20'], 'Add 4 each time', 30),
    R('numerical', 'D2', 'If 4 identical notebooks cost 96, what do 7 notebooks cost at the same rate?', '168',
      ['172', '160', '184'], 'One costs 24; 7 x 24 = 168', 45),
    R('numerical', 'D2', '25% of 80 is the same as 50% of which number?', '40', ['20', '160', '10'],
      '25% of 80 = 20, and 20 is 50% of 40', 45),
    R('numerical', 'D3', 'What number comes next? 2, 6, 12, 20, 30, ?', '42', ['40', '36', '44'],
      'Differences are 4, 6, 8, 10, so add 12', 60),
    R('verbal', 'D1', 'Book is to reading as fork is to ...', 'eating', ['kitchen', 'spoon', 'cooking'],
      'A book is used for reading; a fork is used for eating', 30),
    R('verbal', 'D2', 'Which word does not belong with the others? apple, mango, carrot, banana', 'carrot',
      ['apple', 'mango', 'banana'], 'Carrot is a vegetable; the others are fruits', 30),
    R('verbal', 'D2', 'All squares are rectangles. All rectangles have four sides. Which statement must be true?',
      'All squares have four sides', ['All four-sided shapes are squares', 'Some rectangles do not have four sides',
                                      'All rectangles are squares'],
      'If every square is a rectangle and every rectangle has four sides, every square has four sides', 45, ['p65']),
    R('verbal', 'D3', 'Asha is taller than Ben. Ben is taller than Chitra. Dev is shorter than Chitra. Who is the shortest?',
      'Dev', ['Chitra', 'Ben', 'Asha'], 'Order: Asha > Ben > Chitra > Dev', 60, ['p65']),
    R('abstract', 'D1', 'The shapes repeat in a pattern: circle, square, triangle, circle, square, ? Which shape comes next?',
      'triangle', ['circle', 'square', 'pentagon'], 'The three shapes repeat in the same order', 30, svg=SHAPES_SVG),
    R('abstract', 'D2', 'Figure 1 has 1 black dot, figure 2 has 2 white dots, figure 3 has 3 black dots, figure 4 has 4 white dots. What is figure 5?',
      '5 black dots', ['5 white dots', '6 black dots', '4 black dots'], 'One more dot each time; colours alternate', 45),
    R('abstract', 'D2', 'Which letter comes next? A, C, F, J, O, ?', 'U', ['T', 'V', 'S'],
      'The gaps grow by one: +2, +3, +4, +5, then +6', 60),
    R('abstract', 'D3', "Rule: the third figure keeps the lines that appear in only one of the first two figures and drops lines they share. A vertical line '|' and a horizontal line '-' give a cross '+'. If figure 1 is a cross '+' and figure 2 is a vertical line '|', what is figure 3?",
      "a horizontal line '-'", ["a cross '+'", "a vertical line '|'", 'a blank square'],
      'The vertical line is shared, so it is dropped; the horizontal line stays', 75),
    R('spatial', 'D1', 'A square sheet of paper is folded in half once along a diagonal. What shape do you get?', 'a triangle',
      ['a rectangle', 'a smaller square', 'a pentagon'], 'The diagonal fold puts one corner on the opposite corner', 30),
    R('spatial', 'D2', 'A mirror is held upright beside each capital letter. Which letter looks the same in the mirror?', 'A',
      ['B', 'C', 'R'], 'A has a vertical line of symmetry', 45),
    R('spatial', 'D2', 'A cube is painted on all faces and cut into 27 equal small cubes. How many small cubes have exactly two painted faces?',
      '12', ['8', '6', '1'], 'Those are the middle cubes of the 12 edges', 60),
    R('spatial', 'D3', 'You face north. You turn 90° clockwise, then 180°, then 90° anticlockwise. Which way do you face now?',
      'South', ['North', 'East', 'West'], 'North -> East -> West -> South', 60),
]

G9_10 = [
    R('numerical', 'D1', 'What number comes next? 5, 10, 20, 40, ?', '80', ['60', '45', '100'], 'Double each time', 30),
    R('numerical', 'D2', 'A train travels 240 km in 3 hours. At the same speed, how far does it go in 5 hours?', '400 km',
      ['360 km', '480 km', '420 km'], '80 km per hour x 5 = 400 km', 45),
    R('numerical', 'D2', 'The average of five numbers is 18. Four of them are 15, 20, 12 and 25. What is the fifth?', '18',
      ['20', '16', '22'], 'Total 90; 90 - 72 = 18', 60),
    R('numerical', 'D3', 'A price rises by 20% and then falls by 20%. What is the overall change?', 'A 4% decrease',
      ['No change', 'A 4% increase', 'A 2% decrease'], '1.2 x 0.8 = 0.96', 60),
    R('verbal', 'D1', "Which word is most nearly opposite in meaning to 'scarce'?", 'plentiful', ['rare', 'small', 'costly'],
      "'Scarce' means in short supply", 30),
    R('verbal', 'D2', 'Doctor is to hospital as teacher is to ...', 'school', ['student', 'book', 'lesson'],
      'The place where each works', 30),
    R('verbal', 'D2', 'No reptiles have fur. All snakes are reptiles. Which conclusion follows?', 'No snakes have fur',
      ['Some snakes have fur', 'All furry animals are snakes', 'Some reptiles are not snakes'],
      'Snakes are inside the reptile group, which has no fur; the last option may be true but does not follow', 45, ['p65']),
    R('verbal', 'D3', 'Five friends sit in a row. P is at one end and Q sits next to P. R is in the middle seat. S does not sit next to R. Where does T sit?',
      'Between R and S', ['Next to P', 'At the other end', 'Between Q and R'],
      'Seats 1-5: P, Q, R; S cannot be in 4, so S is in 5 and T in 4', 75, ['p65']),
    R('abstract', 'D1', 'Which letter comes next? Z, X, V, T, ?', 'R', ['S', 'Q', 'P'], 'Go back two letters each time', 30),
    R('abstract', 'D2', 'In a code, CAT is written DBU. How is DOG written?', 'EPH', ['EOG', 'CNF', 'FQI'],
      'Each letter moves one place forward', 45),
    R('abstract', 'D2', 'An arrow turns 90° clockwise at each step. Step 1 points up, step 2 right, step 3 down. Which way does it point at step 6?',
      'Right', ['Up', 'Down', 'Left'], 'The cycle repeats every 4 steps; step 6 = step 2', 45),
    R('abstract', 'D3', 'In a 3 x 3 grid every row and column has one circle, one square and one triangle. Row 1: circle, square, triangle. Row 2: triangle, circle, square. What goes in row 3, column 2?',
      'triangle', ['circle', 'square', 'any shape'], 'Column 2 already has a square and a circle', 75, svg=GRID_SVG),
    R('spatial', 'D1', 'Which solid has one flat circular face and one curved surface meeting at a point?', 'a cone',
      ['a cylinder', 'a sphere', 'a cube'], 'A cone has a circular base and an apex', 30),
    R('spatial', 'D2', 'Six squares are arranged in a cross: a column of four squares with one extra square on each side of the second square. Folded along the lines, this net makes a',
      'cube', ['square pyramid', 'cuboid with an open top', 'triangular prism'], 'This is one of the 11 nets of a cube', 45),
    R('spatial', 'D2', 'A wall clock seen in a mirror appears to show 3:00. What is the real time?', '9:00',
      ['3:00', '6:00', '12:00'], 'A mirror swaps left and right: 3 becomes 9', 45),
    R('spatial', 'D3', 'A 4 cm cube is painted on all faces and cut into 1 cm cubes. How many small cubes have no paint at all?',
      '8', ['16', '24', '27'], 'The unpainted core is 2 x 2 x 2', 75),
]

G11_12 = [
    R('numerical', 'D2', 'What number comes next? 2, 3, 5, 8, 13, ?', '21', ['18', '20', '26'],
      'Each term is the sum of the two before it', 30),
    R('numerical', 'D2', 'Money doubles in 6 years at a fixed compound rate. In how many years does it become 8 times?', '18',
      ['24', '12', '48'], '8 = 2³, so three doubling periods', 45),
    R('numerical', 'D3', 'Boys and girls in a class are in the ratio 3 : 5. After 6 more boys join, the ratio is 1 : 1. How many students were there at first?',
      '24', ['32', '30', '16'], '3k + 6 = 5k gives k = 3, so 9 + 15 = 24', 75),
    R('numerical', 'D3', 'One pipe fills a tank in 6 hours; another empties it in 9 hours. If both are open, how long does it take to fill the empty tank?',
      '18 hours', ['15 hours', '3 hours', '7.5 hours'], '1/6 - 1/9 = 1/18 of the tank per hour', 75),
    R('verbal', 'D2', "Which phrase is closest in meaning to 'ubiquitous'?", 'found everywhere',
      ['very rare', 'extremely old', 'highly useful'], 'Ubiquitous means present everywhere', 30),
    R('verbal', 'D2', 'Author is to novel as composer is to ...', 'symphony', ['orchestra', 'piano', 'audience'],
      'What each creates', 30),
    R('verbal', 'D3', 'Some economists are writers. All writers are readers. Which statement must be true?',
      'Some economists are readers', ['All readers are economists', 'All economists are writers', 'No reader is an economist'],
      'The economists who are writers are also readers', 60, ['p65']),
    R('verbal', 'D3', "Claim: 'Since the new study app launched, the school's test scores rose, so the app raised scores.' Which fact, if true, most weakens the claim?",
      'The school also hired extra teachers at the same time', ['The app is free', 'Students said they liked the app',
                                                               'Scores rose most in maths'],
      'Another change at the same time offers a different explanation', 75, ['p65']),
    R('abstract', 'D2', 'What comes next? AZ, BY, CX, ?', 'DW', ['DV', 'EW', 'DX'],
      'First letters go forward, second letters go backward', 30),
    R('abstract', 'D2', 'If 2 ⊕ 3 = 13 and 3 ⊕ 4 = 25, what is 4 ⊕ 5?', '41', ['20', '45', '81'],
      'a ⊕ b = a² + b²: 16 + 25 = 41', 60),
    R('abstract', 'D3', 'What comes next? 1, 2, 6, 24, 120, ?', '720', ['240', '600', '144'],
      'Multiply by 2, 3, 4, 5, then 6', 60),
    R('abstract', 'D3', 'Figures: shaded triangle, unshaded square, shaded pentagon, ... Each figure gains one side and the shading alternates. What is the next figure?',
      'an unshaded hexagon', ['a shaded hexagon', 'an unshaded pentagon', 'a shaded heptagon'],
      'Six sides, and the shading switches back to unshaded', 60),
    R('spatial', 'D2', 'What is the smaller angle between the hour and minute hands of a clock at 3:15?', '7.5°',
      ['0°', '15°', '22.5°'], 'The hour hand has moved a quarter of 30° past the 3', 60),
    R('spatial', 'D2', 'Opposite faces of a die add up to 7. A die shows 1 on top, 2 at the front and 3 on the right. What number is on the bottom?',
      '6', ['5', '4', '2'], 'Bottom is opposite top: 7 - 1 = 6', 45, svg=DIE_SVG),
    R('spatial', 'D3', 'From home you walk 4 km north and then 3 km east. How far are you from home in a straight line?', '5 km',
      ['7 km', '1 km', '6 km'], 'A 3-4-5 right triangle', 45),
    R('spatial', 'D3', 'A 3 x 3 x 3 cube is painted on all faces and cut into 27 small cubes. How many small cubes have exactly one painted face?',
      '6', ['8', '12', '1'], 'One at the centre of each face', 60),
]


def items_for(grade):
    if grade == 8:
        return G8
    if grade in (9, 10):
        return G9_10
    return G11_12
