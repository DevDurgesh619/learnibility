"""Part C 'About me': 30 quick student self-report items mapped to 430-parameter IDs.

12 career-interest items (RIASEC, two per letter) feed p200. Exam nerves and sleep are T3:
screened, optional, used only to adapt support (never ranking, fit or allocation).
"""

def scale(low, high):
    return [{'label': f'1 {low}', 'value': 1}, {'label': '2', 'value': 2}, {'label': '3', 'value': 3},
            {'label': '4', 'value': 4}, {'label': f'5 {high}', 'value': 5}]


def opt(*labels):
    return [{'label': l, 'value': v} for l, v in labels]


def C(prompt, param, rtype, options=None, **kw):
    it = {'part': 'C', 'respondent': 'student', 'prompt': prompt, 'responseType': rtype, 'paramId': param}
    if options is not None:
        it['options'] = options
    it.update(kw)
    return it


ENJOY = scale('Not at all', 'Love it')
AGREE = scale('Strongly disagree', 'Strongly agree')

RIASEC = [
    ('R', 'Fixing or building things, like a bicycle, a model or a small circuit'),
    ('R', 'Working outdoors with tools, plants or animals'),
    ('I', 'Doing experiments to find out why something happens'),
    ('I', 'Solving tricky maths or logic puzzles'),
    ('A', 'Drawing, designing, writing stories or making music'),
    ('A', 'Acting, photography or making videos'),
    ('S', 'Explaining something to a friend until they understand it'),
    ('S', 'Volunteering to help people in your community'),
    ('E', 'Leading a team or running a school club'),
    ('E', 'Pitching an idea or starting a small business'),
    ('C', 'Keeping records or organising information neatly'),
    ('C', 'Working with numbers, budgets or spreadsheets'),
]


def items_for(board, grade, stream):
    items = [
        C('On a normal school day, how long do you study at home (not counting tuition)?', 'p31', 'single',
          opt(('Less than 1 hour', 0.5), ('1 to 2 hours', 1.5), ('2 to 3 hours', 2.5), ('3 to 4 hours', 3.5),
              ('More than 4 hours', 4.5)), unit='hours'),
        C('When do you usually study best?', 'p33', 'single',
          opt(('Early morning', 'early_morning'), ('Afternoon', 'afternoon'), ('Evening', 'evening'),
              ('Late night', 'late_night'))),
        C('How long is a typical study session before you take a break?', 'p34', 'single',
          opt(('15 to 20 minutes', 20), ('30 to 45 minutes', 40), ('About an hour', 60), ('90 minutes or more', 90)),
          unit='minutes'),
        C('How often do you revise topics you have already finished?', 'p39', 'single',
          opt(('Rarely', 'rarely'), ('Only before tests', 'before_tests'), ('Every week', 'weekly'), ('Most days', 'daily'))),
        C('How do you usually revise?', 'p40', 'single',
          opt(('Re-reading notes or the textbook', 'reread'), ('Highlighting or rewriting notes', 'rewrite'),
              ('Doing practice questions', 'practice'), ('Testing myself with flashcards or quizzes', 'self_test'),
              ('Explaining it to someone else', 'teach'))),
        C('I put off starting homework until the last minute.', 'p46', 'scale', scale('Never', 'Always')),
        C('Where is your phone while you study?', 'p105', 'single',
          opt(('In another room', 'away'), ('Nearby on silent', 'silent_nearby'), ('With me, I check it often', 'checking'),
              ('I study on my phone', 'study_device'))),
        C('Which helps you learn a new topic most?', 'p48', 'single',
          opt(('Watching a video', 'video'), ('Reading and making notes', 'reading'), ('Trying problems straight away', 'practice'),
              ('Discussing it with someone', 'discussion'))),
        C('Do you prefer studying alone or with others?', 'p50', 'single',
          opt(('Alone', 'solo'), ('With one friend', 'pair'), ('In a group', 'group'), ('It depends on the subject', 'mixed'))),
        C('When you get stuck on a question, what do you usually do first?', 'p49', 'single',
          opt(('Ask my teacher', 'teacher'), ('Ask a friend or sibling', 'peer'), ('Search online or watch a video', 'online'),
              ('Leave it and move on', 'skip'))),
        C('Do you go to tuition or coaching classes?', 'p21', 'single',
          opt(('No', 'none'), ('Yes, for one subject', 'one_subject'), ('Yes, for two or more subjects', 'multi_subject'),
              ('Yes, at a coaching institute', 'institute'))),
        C('I mostly study because ...', 'p123', 'single',
          opt(('I enjoy learning new things', 'intrinsic'), ('I have a goal I want to reach', 'goal'),
              ('I want good marks', 'performance'), ('My family expects it', 'external'))),
        C('If I work hard, I can get much better at a subject I find difficult.', 'p125', 'scale', AGREE),
        C('I like hard problems, even when I might get them wrong.', 'p331', 'scale', AGREE),
        C('Before a test, how nervous do you usually feel?', 'p111', 'scale', scale('Calm', 'Very nervous'),
          helpText='Optional. This only helps us pace your plan and suggest support; it never affects your scores or recommendations.',
          alsoInforms=['p133']),
        C('On school nights, how many hours do you usually sleep?', 'p83', 'single',
          opt(('Less than 6', 5.5), ('6 to 7', 6.5), ('7 to 8', 7.5), ('8 to 9', 8.5), ('More than 9', 9.5)),
          helpText='Optional. Used only to fit your timetable around enough rest.', unit='hours'),
    ]
    for letter, text in RIASEC:
        items.append(C(f'How much would you enjoy this? {text}', 'p200', 'scale', ENJOY, riasec=letter,
                       alsoInforms=['p201']))
    items.append(C('How interested are you in studying abroad after school?', 'p230', 'scale',
                   scale('Not interested', 'Very interested'), alsoInforms=['p231']))
    items.append(C('Which career areas interest you right now? Pick up to three.', 'p198', 'multi',
                   opt(('Engineering and technology', 'engineering'), ('Medicine and health', 'medicine'),
                       ('Business, finance and commerce', 'business'), ('Law, government and public policy', 'law'),
                       ('Design, media and the arts', 'design'), ('Science and research', 'research'),
                       ('Teaching, psychology and social work', 'social'), ('Not sure yet', 'unsure')),
                   max=3, alsoInforms=['p199']))
    assert len(items) == 30, len(items)
    return items
