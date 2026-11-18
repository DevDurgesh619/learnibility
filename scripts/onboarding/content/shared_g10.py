"""Grade 10 prerequisite slots (grade 9 skills) shared by all three boards; refs point at each board's grade 9 map."""
from dsl import S

MATHS_PRE_G10 = [
    S({'cbse': 'cbse-g9-maths:4:4', 'cambridge': 'cambridge-g9-maths:6:2', 'ib': 'ib-g9-maths:3:3'},
      'Factorising quadratic expressions', items=[
        ('Factorise x² + 5x + 6.', '(x + 2)(x + 3)', ['(x + 1)(x + 6)', '(x - 2)(x - 3)', '(x + 5)(x + 1)'],
         'Find two numbers that multiply to 6 and add to 5'),
    ]),
    S({'cbse': 'cbse-g9-maths:2:4', 'cambridge': 'cambridge-g9-maths:10:1', 'ib': 'ib-g9-maths:7:1'},
      'Gradient and intercept of a straight line', items=[
        ('What is the gradient of the line y = 3x - 2?', '3', ['-2', '2', '1/3'], 'In y = mx + c, m is the gradient'),
        ('What is the gradient of the line through (1, 2) and (4, 11)?', '3', ['9', '1/3', '13/5'], '(11 - 2) ÷ (4 - 1) = 3'),
    ]),
    S({'cbse': 'cbse-g9-maths:7:3', 'cambridge': 'cambridge-g9-maths:8:1', 'ib': 'ib-g9-maths:12:2'},
      'Probability of equally likely and combined outcomes', items=[
        ('A bag holds 3 red and 5 blue counters. One is picked at random. What is the probability it is red?', '3/8',
         ['3/5', '5/8', '1/3'], '3 red out of 8 counters'),
        ('A fair die is rolled. What is the probability of getting a number greater than 4?', '1/3', ['1/2', '1/6', '2/3'],
         'Only 5 and 6 work: 2 out of 6'),
        ('Two fair coins are tossed. What is the probability of getting at least one head?', '3/4', ['1/2', '1/4', '2/3'],
         'HH, HT, TH out of HH, HT, TH, TT'),
    ]),
    S({'cbse': 'cbse-g9-maths:10:3', 'cambridge': 'cambridge-g9-maths:12:1', 'ib': 'ib-g9-maths:11:2'},
      'Mean and median', items=[
        ('What is the mean of 4, 7, 9, 12 and 8?', '8', ['9', '7', '40'], '40 ÷ 5 = 8'),
        ('What is the median of 3, 9, 4, 7, 12 and 5?', '6', ['7', '5', '6.7'], 'Order: 3, 4, 5, 7, 9, 12; middle pair (5 + 7) ÷ 2'),
        ('The mean of five numbers is 12. One number, 20, is removed. What is the mean of the other four?', '10',
         ['8', '12', '11'], 'Total 60 - 20 = 40, and 40 ÷ 4 = 10'),
    ]),
]

SCIENCE_PRE_G10 = [
    S({'cbse': 'cbse-g9-science:5:2', 'cambridge': 'cambridge-g9-physics:3:2', 'ib': 'ib-g9-science:9:2'},
      "Newton's second law, F = ma", items=[
        ('A 1200 kg car accelerates at 2 m/s². What resultant force acts on it?', '2400 N', ['600 N', '1202 N', '0.0017 N'],
         'F = ma = 1200 x 2'),
    ]),
    S({'cbse': 'cbse-g9-science:7:3', 'cambridge': 'cambridge-g9-chemistry:2:4', 'ib': 'ib-g9-science:4:3'},
      'Electron arrangement in shells', items=[
        ('Sodium has the electron arrangement 2,8,1. How many electrons are in its outer shell?', '1', ['2', '8', '11'],
         'The last number is the outer shell'),
        ('An element has the electron arrangement 2,8,7. What happens when it forms an ion?', 'It gains one electron to form a 1- ion',
         ['It loses seven electrons to form a 7+ ion', 'It loses one electron to form a 1+ ion', 'It does not form ions'],
         'Gaining one electron completes the outer shell (chlorine)'),
    ]),
    S({'cbse': 'cbse-g9-science:8:3', 'cambridge': 'cambridge-g9-chemistry:4:2', 'ib': 'ib-g9-science:6:1'},
      'Writing formulae and balancing equations', items=[
        ('Magnesium forms Mg²⁺ ions and oxygen forms O²⁻ ions. What is the formula of magnesium oxide?', 'MgO',
         ['Mg₂O', 'MgO₂', 'Mg₂O₂'], 'The charges balance one to one'),
        ('Aluminium forms Al³⁺ ions and oxygen forms O²⁻ ions. What is the formula of aluminium oxide?', 'Al₂O₃',
         ['AlO', 'Al₃O₂', 'AlO₃'], '2 x (+3) balances 3 x (-2)'),
        ('Which equation is correctly balanced?', '4Fe + 3O₂ → 2Fe₂O₃', ['2Fe + O₂ → Fe₂O₃', 'Fe + 3O₂ → 2Fe₂O₃', '4Fe + O₂ → 2Fe₂O₃'],
         'Count atoms: 4 Fe and 6 O on each side'),
    ]),
    S({'cbse': 'cbse-g9-science:3:3', 'cambridge': 'cambridge-g9-physics:2:3', 'ib': 'ib-g9-science:8:2'},
      'Acceleration and velocity-time graphs', items=[
        ('A cyclist speeds up from 0 to 20 m/s in 5 s. What is the acceleration?', '4 m/s²', ['100 m/s²', '25 m/s²', '0.25 m/s²'],
         'a = change in velocity ÷ time'),
        ('On a velocity-time graph, what does the area under the line show?', 'The distance travelled',
         ['The acceleration', 'The force', 'The time taken'], 'Area = velocity x time'),
        ('A car moving at 20 m/s brakes steadily to rest in 4 s. How far does it travel while braking?', '40 m',
         ['80 m', '5 m', '20 m'], 'Area of the triangle: ½ x 4 x 20'),
    ]),
]

ENGLISH_PRE_G10 = [
    S({'cbse': 'cbse-g9-english:1:4', 'cambridge': 'cambridge-g9-english:2:2', 'ib': 'ib-g9-english:2:2'},
      'Inferring feelings and attitudes', items=[
        ('Read: "Meera glanced at the clock again, tapped her pen and read the same line for the fifth time." How is Meera most likely feeling?',
         'Restless and unable to concentrate', ['Calm and relaxed', 'Angry with the clock', 'Proud of her reading'],
         'Repeated glancing and rereading suggest restlessness'),
    ]),
    S({'cbse': 'cbse-g9-english:2:3', 'cambridge': 'cambridge-g9-english:4:3', 'ib': 'ib-g9-english:4:1'},
      'Imagery and its effect', items=[
        ("In 'The wind howled through the empty streets', the wind is given a human or animal quality. This is", 'personification',
         ['simile', 'alliteration', 'onomatopoeia only'], 'An object is given living qualities'),
        ("What is the effect of 'the classroom was a pressure cooker before the exam'?", 'It shows the tension was building and about to burst',
         ['It shows the classroom was hot from cooking', 'It shows the students were hungry', 'It shows the exam was easy'],
         'A pressure cooker builds pressure until it releases'),
    ]),
    S({'cbse': 'cbse-g9-english:5:2', 'cambridge': 'cambridge-g9-english:5:4', 'ib': 'ib-g9-english:6:1'},
      'Claim, evidence and counterargument', items=[
        ('In an argument, the main point the writer wants you to accept is the', 'claim', ['evidence', 'rebuttal', 'anecdote'],
         'Evidence supports the claim'),
        ("Which sentence is a counterargument in an essay arguing for school uniforms?", "Some say uniforms limit students' self-expression.",
         ['Uniforms reduce peer pressure about clothes.', 'A 2023 survey found most parents support uniforms.',
          'Therefore uniforms should stay.'], 'A counterargument presents the opposing view'),
        ("A writer says: 'Everyone I know hates homework, so homework should be banned.' What is the main weakness?",
         'The evidence is a small, personal sample', ['The claim is too short', 'It uses no adjectives', 'It is written in the first person'],
         'A few friends do not represent everyone'),
    ]),
    S({'cbse': 'cbse-g9-english:15:4', 'cambridge': 'cambridge-g9-english:4:4', 'ib': 'ib-g9-english:1:2'},
      'Sentence structure for effect', items=[
        ('Which of these is a complex sentence?', 'When the bell rang, the students rushed out.',
         ['The bell rang.', 'The bell rang and the students rushed out.', 'Rushing out!'], 'It has a main clause and a subordinate clause'),
        ("A story reads: 'The door creaked. Silence. Then footsteps.' What is the effect of the short sentences?", 'They build tension and suspense',
         ['They make the story feel relaxed', 'They explain the setting in detail', 'They show the writer ran out of ideas'],
         'Short, broken sentences slow the reader and create suspense'),
        ('Rearrange into a correct sentence: "the / finally / after / rain / match / the / began / the / stopped"',
         'The match finally began after the rain stopped.',
         ['After the match finally began the rain stopped.', 'The rain finally began after the match stopped.',
          'The match stopped after the rain finally began.'], 'The match could only start once the rain had stopped'),
    ]),
]
