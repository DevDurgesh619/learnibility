"""Shared English kit for the QB-CBSE English subjects cbse-g8-english, cbse-g9-english and cbse-g12-english.

Copyright rule: no textbook passage is reproduced. Every passage and extract here is original writing on
the chapter's theme (or a short paraphrase in our own words of a well-known moment), and text-based
questions only use safe, well-known facts (author, characters, theme, message).

A subject module describes each chapter as a dict (see g8_english_a.py) and calls `build_subject`.
Subtopic specs:
    LIT(...)      literature subtopic: facts, true/false statements, A-R pairs, explain/think/long prompts
    VOCAB(...)    vocabulary subtopic (uses the chapter's vocab list plus optional extra words)
    GRAM(engine)  grammar subtopic, engine name from eng_kit_g8_g9_g12_grammar.ENGINES
    WRITE(form)   writing subtopic (notice, letter, diary, article, ...)
    READ()        reading-skill subtopic (uses the subject's passages and data passages)
"""
from __future__ import annotations

import random
import re

from qbank import F, Builder, ar, mcq, GIRLS, BOYS, CITIES, onorm

# ---------------------------------------------------------------- people, places, dates

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
SCHOOLS = ['Kendriya Vidyalaya', 'Delhi Public School', 'DAV Public School', 'Army Public School', 'Jawahar Navodaya Vidyalaya',
           'Sarvodaya Vidyalaya', "St. Xavier's School", 'Government Senior Secondary School', 'Bal Bharati Public School',
           'Sainik School', 'Modern School', 'Vidya Niketan', 'Gyan Jyoti School', 'Ryan International School', 'Springdales School']
CLUBS = ['Literary Club', 'Eco Club', 'Heritage Club', 'Science Club', 'Readers\' Club', 'Cultural Committee', 'Student Council',
         'Interact Club', 'Nature Club', 'Debating Society', 'Quiz Club', 'Social Service League']
ROLES = ['Secretary', 'President', 'Joint Secretary', 'Coordinator', 'Student Coordinator']
VENUES = ['the school auditorium', 'the assembly ground', 'the multipurpose hall', 'the school library', 'the activity room', 'the conference hall']
TIMES = ['9:00 a.m.', '9:30 a.m.', '10:00 a.m.', '10:30 a.m.', '11:00 a.m.', '12:00 noon', '2:00 p.m.', '2:30 p.m.', '3:00 p.m.', '4:00 p.m.']
GRADES = {8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'}

PRON_F = {'he': 'she', 'him': 'her', 'his': 'her', 'hers': 'hers', 'himself': 'herself', 'He': 'She', 'His': 'Her', 'Him': 'Her'}
PRON_M = {'he': 'he', 'him': 'him', 'his': 'his', 'hers': 'his', 'himself': 'himself', 'He': 'He', 'His': 'His', 'Him': 'Him'}


def person(r: random.Random):
    """Return (name, pronoun dict)."""
    if r.random() < 0.5:
        return r.choice(GIRLS), PRON_F
    return r.choice(BOYS), PRON_M


def date(r: random.Random) -> str:
    return f'{r.randint(2, 28)} {r.choice(MONTHS)} {r.choice([2026, 2027])}'


def school(r: random.Random) -> tuple[str, str]:
    c = r.choice(CITIES)
    return f'{r.choice(SCHOOLS)}, {c}', c


def slots(r: random.Random, grade: int) -> dict:
    n, p = person(r)
    n2, p2 = person(r)
    while n2 == n:
        n2, p2 = person(r)
    sch, city = school(r)
    return {'name': n, 'name2': n2, 'he': p['he'], 'his': p['his'], 'him': p['him'], 'He': p['He'], 'His': p['His'],
            'school': sch, 'city': city, 'date': date(r), 'date2': date(r), 'club': r.choice(CLUBS), 'role': r.choice(ROLES),
            'venue': r.choice(VENUES), 'time': r.choice(TIMES), 'class': GRADES.get(grade, 'IX'),
            'section': r.choice('ABCDE'), 'n': r.choice([20, 25, 30, 40, 50, 60]), 'city2': r.choice([c for c in CITIES if c != city])}


def fill(t: str, s: dict) -> str:
    return t.format(**s)


def lf(s: str) -> str:
    """Lower-case the first letter (unless it starts a proper noun we cannot detect: keep acronyms and 'I')."""
    if not s:
        return s
    w = s.split(' ', 1)[0]
    if w in ('I',) or w.isupper() or (len(w) > 1 and w[1:].lower() != w[1:]):
        return s
    return s[0].lower() + s[1:]


def stop(s: str) -> str:
    s = s.strip()
    return s if s[-1:] in '.?!"\'' else s + '.'


def roman(i: int) -> str:
    return ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii'][i]


def inline_opts(opts) -> str:
    return '  '.join(f'({"abcd"[i]}) {o}' for i, o in enumerate(opts))


def need(cond):
    if not cond:
        raise ValueError('not enough data')


# ---------------------------------------------------------------- subtopic specs

def LIT(**kw):
    return dict(kind='lit', **kw)


def VOCAB(**kw):
    return dict(kind='vocab', **kw)


def GRAM(engine, **kw):
    return dict(kind='gram', engine=engine, **kw)


def WRITE(form, **kw):
    return dict(kind='write', form=form, **kw)


def READ(**kw):
    return dict(kind='read', **kw)


# ---------------------------------------------------------------- writing forms

WORDS = {'notice': ['50', 'not more than 50'], 'letter': ['120–150'], 'email': ['120–150'], 'diary': ['100–120', '80–100'],
         'article': ['120–150'], 'paragraph': ['100–120', '80–100'], 'speech': ['120–150'], 'story': ['150–180', '120–150'],
         'report': ['120–150'], 'invitation': ['50', 'not more than 50'], 'reply': ['50', 'not more than 50'], 'bio': ['100–120'],
         'brochure': ['80–100', '100–120'], 'essay': ['200–250'], 'description': ['120–150'], 'editor': ['120–150'],
         'job': ['120–150'], 'interview': ['8–10 questions'], 'formal_invitation': ['50', 'not more than 50']}

FORMAT_KEY = {
    'notice': 'Format (1): the word NOTICE, name of the institution, date of issue, a clear heading, name and designation of the writer. '
              'Content: what, when (date and time), where, who may take part and whom to contact.',
    'letter': "Format (1): sender's address, date, receiver's address, subject line, salutation, body in paragraphs, complimentary close "
              "(Yours faithfully/sincerely) and name. Content: purpose in the first paragraph, details, request or suggestion, polite close.",
    'editor': "Format (1): sender's address, date, The Editor with the newspaper's name and address, subject line, Sir/Madam, body, "
              "Yours faithfully and name. Content: the issue, its causes and effects, suggestions, appeal to the authorities.",
    'email': 'Format (1): To, Subject and (optionally) Cc lines, salutation, body in short paragraphs, closing and name. '
             'Content: purpose stated early, details, suggestions, polite close.',
    'diary': 'Format (1): day, date and time; first-person, personal and reflective tone; past tense for events and present for feelings; '
             'name or signature at the end (optional). Content: what happened, feelings, reflection or resolve.',
    'article': "Format (1): a catchy title and the writer's name (byline). Content: introduction, body paragraphs with causes, effects or "
               'examples, and a conclusion with suggestions or a call to action.',
    'paragraph': 'Format (1): a topic sentence, supporting details in logical order, and a concluding sentence. Content: relevant ideas '
                 'with examples; vivid, precise words.',
    'speech': 'Format (1): greeting the audience, introducing yourself and the topic, body with points and examples, conclusion and thanks. '
              'Content: persuasive, direct address to listeners.',
    'story': 'Format (1): a suitable title; the given opening used; development, climax and ending. Content: characters, sequence of '
             'events, dialogue where useful, and a clear message or twist.',
    'report': "Format (1): heading, byline (reporter's name), place and date. Content: what, when, where, who, how; highlights, "
              'chief guest or speakers, outcome; past tense, impersonal style.',
    'invitation': 'Format (1): first person, warm and informal; the occasion, date, time and venue; request to confirm; name of the sender. ',
    'formal_invitation': 'Format (1): third person (e.g. "The Principal and staff request the pleasure of your company"), occasion, '
                         'date, time and venue, RSVP with contact. No salutation or signature.',
    'reply': 'Format (1): reference to the invitation, acceptance or regret with reason, thanks; sender\'s name and address/date as required.',
    'bio': 'Format (1): name and a striking opening; birth, family and education; career and achievements in order; qualities; legacy.',
    'brochure': 'Format (1): catchy title, short sections or bullet points (attractions, how to reach, best time to visit, tips), contact or website.',
    'essay': 'Format (1): title, introduction, three or four body paragraphs, conclusion. Content: relevant ideas developed with examples.',
    'description': 'Format (1): introduction to the object/process/place, details in a logical order (appearance, materials, steps or parts), '
                   'conclusion. Content: factual, impersonal; present tense; sequence words.',
    'job': 'Format (1): covering letter (addresses, date, subject, salutation, body, close) and a résumé (personal details, qualifications, '
           'experience, skills, references). Content: post applied for, suitability, availability for interview.',
    'interview': 'Format (1): a short introduction and a sequence of open-ended questions moving from background to views to future plans, '
                 'and a polite close. Content: questions that draw out the interviewee\'s experience and opinions.',
}

FORM_LABEL = {'notice': 'notice', 'letter': 'formal letter', 'editor': 'letter to the editor', 'email': 'formal e-mail', 'diary': 'diary entry',
              'article': 'article', 'paragraph': 'paragraph', 'speech': 'speech', 'story': 'story', 'report': 'report',
              'invitation': 'informal invitation', 'formal_invitation': 'formal invitation', 'reply': 'reply to an invitation',
              'bio': 'biographical sketch', 'brochure': 'travel brochure', 'essay': 'essay', 'description': 'factual description',
              'job': 'job application with résumé', 'interview': 'set of interview questions'}


def form_marks(form: str, grade: int) -> int:
    if form in ('notice', 'invitation', 'formal_invitation', 'reply'):
        return 4 if grade >= 11 else 5
    if form in ('essay',):
        return 10 if grade == 9 else 5
    return 5


def writing_item(r, grade, form, template, points, marks=None):
    s = slots(r, grade)
    s['words'] = r.choice(WORDS.get(form, ['120–150']))
    stem = fill(template, s)
    if '{words}' not in template and form != 'interview':
        stem = stem.rstrip() + f' (Word limit: {s["words"]} words.)'
    m = marks or form_marks(form, grade)
    expr = 1 if m <= 4 else 2 if m <= 6 else 4
    content = m - 1 - expr
    key = (f'{FORMAT_KEY[form]} Content ({content} mark{"s" if content != 1 else ""}): {points}. Expression ({expr} mark{"s" if expr != 1 else ""}): fluency, accuracy of grammar and spelling, '
           f'appropriate register and word limit.')
    lab = FORM_LABEL[form]
    return {'stem': stem, 'answer': f'{"An" if lab[0] in "aeiou" else "A"} {lab} covering: {points}.', 'key': key, 'marks': m,
            'minutes': {4: 7, 5: 9, 10: 16}.get(m, 8), 'gap': 'G7' if len(stem.split()) > 60 else None}


# Format facts, A-R and explain prompts for writing subtopics (general, not chapter-bound).
FORM_FACTS = {
    'notice': [
        ('What is the usual word limit for a school notice in the CBSE paper?', '50 words', '150 words', '20 words', '250 words', 'A notice is brief: about 50 words.'),
        ('Where is the word NOTICE written in a notice?', 'At the top, after the name of the institution', 'At the end, after the signature', 'Inside the body, before the date', 'It is not written at all', 'The institution\'s name and NOTICE come first.'),
        ('Which of these must a notice about an event include?', 'Date, time and venue of the event', 'A complimentary close such as "Yours faithfully"', 'The receiver\'s address', 'A salutation such as "Dear Sir"', 'A notice has no salutation or receiver\'s address.'),
        ('A notice is signed with the writer\'s …', 'name and designation', 'address and phone number', 'roll number and section only', 'nickname', 'Name and designation tell readers who issued it.'),
        ('Which heading suits a notice about a tree-plantation drive?', 'TREE PLANTATION DRIVE', 'Dear Students, Please Read', 'Yours Sincerely', 'From the Principal\'s Desk to All of You', 'The heading is short and in capitals.'),
        ('Which tone is right for a notice?', 'Formal and clear', 'Chatty and humorous', 'Emotional and poetic', 'Sarcastic', 'A notice informs everyone formally.'),
        ('Why is a notice often placed inside a box?', 'To set it apart as a display item on a notice board', 'Because the box carries one mark for neatness of drawing', 'Because a box replaces the heading', 'So that no date is needed', 'The box shows it is a notice for display.'),
    ],
    'letter': [
        ('Which complimentary close is used in a formal letter to an official?', 'Yours faithfully', 'Your loving friend', 'With love', 'Cheers', 'Formal letters to officials end with "Yours faithfully" (or "Yours sincerely").'),
        ('In a formal letter, the subject line comes …', 'after the receiver\'s address and before the salutation', 'after the complimentary close', 'before the sender\'s address', 'at the very end', 'The subject sits just above "Sir/Madam".'),
        ('Which salutation suits a letter to the Editor?', 'Sir/Madam', 'Dear Friend', 'Hi there', 'Respected Mother', 'Formal letters use "Sir/Madam".'),
        ('Which of these does NOT belong in a formal letter?', 'Slang and abbreviations like "gonna"', 'A subject line', 'The date', 'A clear request or suggestion', 'Formal letters avoid slang.'),
        ('The first paragraph of a letter of complaint should …', 'state the purpose of writing', 'thank the reader for past favours at length', 'give the writer\'s life story', 'list suggestions only', 'State the purpose at once.'),
        ('In a letter to the Editor, the writer\'s address is written …', 'at the top left, before the date', 'below the signature', 'inside the subject line', 'after the salutation', 'Sender\'s address comes first.'),
    ],
    'email': [
        ('In a formal e-mail, the purpose is best stated in the …', 'subject line and the first lines of the body', 'last line only', 'Cc field', 'signature', 'A clear subject and opening tell the reader why you are writing.'),
        ('Which field shows the main receiver of an e-mail?', 'To', 'Cc', 'Bcc', 'Subject', '"To" is for the main receiver.'),
        ('Which subject line is best for an e-mail suggesting improvements to the school library?', 'Suggestions to improve the school library', 'Hello!!!', 'Please read this urgently now', 'Library', 'It is specific and brief.'),
        ('Which closing suits a formal e-mail to a principal?', 'Regards / Yours sincerely, followed by the name', 'XOXO', 'Bye-bye!', 'Love you', 'A formal closing and name.'),
        ('"Cc" in an e-mail is used to …', 'send a copy to someone who should be informed', 'hide the sender\'s name', 'mark the mail as urgent', 'attach a file', 'Cc = carbon copy.'),
        ('Which of these is NOT good practice in a formal e-mail?', 'Writing the whole body in capital letters', 'Short paragraphs', 'A clear subject line', 'A polite closing', 'Capitals read as shouting.'),
    ],
    'editor': [
        ('A letter to the Editor is mainly written to …', 'draw public attention to an issue of general interest', 'ask for a personal favour from the editor', 'invite the editor to a birthday party', 'complain about a friend', 'It raises a public issue through the newspaper.'),
        ('Which closing is correct in a letter to the Editor?', 'Yours faithfully', 'Your loving son', 'With warm hugs', 'See you soon', 'It is a formal letter.'),
        ('What usually comes in the last paragraph of a letter to the Editor?', 'Suggestions and an appeal to the authorities', 'The date of the letter', 'The subject line', 'A joke to end on a light note', 'End with suggestions and an appeal.'),
        ('Which subject line suits a letter to the Editor about broken ramps at a railway station?', 'Need for safe ramps for wheelchair users at the railway station', 'My train journey', 'Hello Editor', 'Please print my name', 'It names the issue precisely.'),
        ('In a letter to the Editor, the receiver\'s address begins with …', 'The Editor, followed by the newspaper\'s name and address', 'Dear Editor Uncle', 'The Principal', 'To whomsoever it may concern', 'The Editor + newspaper.'),
    ],
    'diary': [
        ('A diary entry is usually written in the …', 'first person', 'third person', 'second person only', 'passive voice only', 'It records the writer\'s own experiences.'),
        ('Which of these is placed at the top of a diary entry?', 'Day, date and time', 'Subject line', 'Receiver\'s address', 'NOTICE', 'Diary entries start with day/date/time.'),
        ('The tone of a diary entry is generally …', 'personal and reflective', 'official and impersonal', 'commanding', 'advertising', 'It is private writing.'),
        ('Which opening suits a diary entry?', 'Dear Diary, today was a day I will never forget.', 'Sir, I beg to state that …', 'NOTICE: All students are informed …', 'Ladies and gentlemen, …', 'A personal opening.'),
        ('Events of the day in a diary entry are usually narrated in the …', 'past tense', 'future tense', 'imperative mood', 'passive voice', 'They have already happened.'),
        ('A good diary entry ends with …', 'a reflection, feeling or resolution', 'a subject line', 'an RSVP', 'the address of the writer', 'It closes with reflection.'),
    ],
    'article': [
        ('What must an article have at the top?', 'A title and the writer\'s name (byline)', 'A salutation', 'The receiver\'s address', 'A complimentary close', 'Title + byline.'),
        ('The conclusion of an article usually …', 'sums up and offers suggestions or a call to action', 'introduces a completely new topic', 'gives the date of writing', 'lists the writer\'s address', 'End with suggestions.'),
        ('Which title is the most effective for an article on saving water?', 'Every Drop Counts', 'An Article', 'Water Is a Thing', 'My Writing Work', 'Catchy and relevant.'),
        ('An article is meant for …', 'readers of a magazine, newspaper or school journal', 'a single close friend', 'the writer alone', 'a bank manager', 'It is for a wide readership.'),
        ('Which of these makes the body of an article stronger?', 'Facts, examples and causes-and-effects in separate paragraphs', 'One long paragraph with no examples', 'Repeating the title many times', 'Using only questions', 'Organised, supported points.'),
        ('A speech differs from an article mainly because a speech …', 'addresses listeners directly and greets the audience', 'has a byline', 'has no conclusion', 'is always shorter than 50 words', 'Speeches are spoken to an audience.'),
    ],
    'paragraph': [
        ('The first sentence of a paragraph that states its main idea is called the …', 'topic sentence', 'concluding sentence', 'supporting detail', 'caption', 'It introduces the main idea.'),
        ('Which of these best supports a descriptive paragraph about a place?', 'Details that appeal to sight, sound and smell', 'A list of unrelated facts', 'A subject line', 'A salutation', 'Sensory details make description vivid.'),
        ('A good concluding sentence …', 'sums up the main idea or leaves a final impression', 'starts a new topic', 'repeats the first sentence word for word', 'gives the writer\'s address', 'It rounds off the paragraph.'),
        ('Which order suits a paragraph describing how to make a clay pot?', 'Chronological order of steps', 'Random order', 'Alphabetical order', 'Reverse order of importance only', 'Steps follow time order.'),
        ('Linking words such as "moreover", "however" and "finally" help a paragraph to be …', 'coherent', 'longer only', 'informal', 'poetic', 'They connect ideas.'),
        ('A biographical sketch is usually written in the …', 'third person', 'first person', 'second person', 'imperative', 'It describes someone else\'s life.'),
        ('Which of these belongs in a travel brochure?', 'Key attractions, how to reach, best time to visit', 'A complimentary close', 'A subject line and salutation', 'Day, date and time of writing', 'Brochures guide visitors.'),
    ],
    'story': [
        ('A story that begins with a given opening line must …', 'continue logically from that line', 'ignore the given line', 'end with the given line', 'be a poem', 'Use the given beginning.'),
        ('The turning point of greatest tension in a story is the …', 'climax', 'title', 'setting', 'moral', 'The climax is the high point.'),
        ('Which of these makes a story lively?', 'Dialogue and vivid description', 'Bullet points', 'A subject line', 'Statistics tables', 'Dialogue and description.'),
        ('A moral at the end of a story …', 'states the lesson the story teaches', 'lists the characters', 'gives the date', 'names the author', 'It is the lesson.'),
        ('Stories are usually narrated in the …', 'past tense', 'future tense', 'imperative', 'passive voice throughout', 'Narration is in the past.'),
    ],
    'report': [
        ('A newspaper report usually begins with …', 'a heading, byline, and the place and date', 'Dear Sir', 'Yours faithfully', 'Day, date and time', 'Heading, byline, place/date.'),
        ('A report on a past school event is written mainly in the …', 'past tense and impersonal style', 'future tense', 'first person, emotional style', 'imperative', 'It records what happened.'),
        ('Which question does the opening of a report answer?', 'What, when, where and who', 'Why the reporter likes the event', 'How old the reporter is', 'What the weather will be tomorrow', 'The key facts.'),
        ('Which of these is the best heading for a report on a cleanliness drive?', 'Students Lead Cleanliness Drive in Local Park', 'My Report', 'Dear Readers', 'A Day', 'Specific and newsy.'),
        ('Quoting the chief guest in a report …', 'adds authenticity and interest', 'is not allowed', 'replaces the heading', 'must be in capital letters', 'Quotes make reports lively.'),
    ],
    'invitation': [
        ('A formal invitation is written in the …', 'third person', 'first person', 'second person', 'imperative', 'e.g. "The Principal requests the pleasure of your company".'),
        ('RSVP on an invitation means …', 'please reply', 'please come early', 'dress formally', 'no gifts', 'From French: répondez s\'il vous plaît.'),
        ('Which detail is essential in an invitation?', 'Date, time and venue', 'Receiver\'s roll number', 'Subject line', 'A complimentary close like "Yours faithfully"', 'Guests need these to attend.'),
        ('An informal invitation to a friend is written in the …', 'first person, in a warm tone', 'third person, very formally', 'passive voice', 'language of a notice', 'It is personal.'),
        ('A reply accepting an invitation should …', 'thank the host and confirm attendance', 'ignore the date and time', 'ask for a new invitation', 'be written as a notice', 'Thank and confirm.'),
    ],
    'job': [
        ('A résumé (bio-data) sent with a job application lists …', 'personal details, qualifications, experience and skills', 'only hobbies', 'the employer\'s address only', 'a poem about the job', 'Résumé = summary of qualifications.'),
        ('The first paragraph of a job application should mention …', 'the post applied for and where it was advertised', 'the applicant\'s favourite food', 'the salary of the manager', 'a complaint', 'Purpose first.'),
        ('Which closing suits a job application?', 'Yours faithfully / Yours sincerely', 'Love', 'Bye', 'Your friend forever', 'Formal close.'),
        ('References in a résumé are …', 'people who can vouch for the applicant\'s work or character', 'books the applicant has read', 'the applicant\'s relatives only', 'not needed ever', 'Referees vouch for you.'),
        ('Which is the best subject line for a job application?', 'Application for the post of Receptionist', 'Job', 'Please give me work', 'Hello', 'Specific.'),
    ],
    'interview': [
        ('Good interview questions are mostly …', 'open-ended, inviting detailed answers', 'yes/no questions only', 'rude or personal', 'very long speeches', 'Open questions draw out views.'),
        ('Interview questions should move …', 'from simple background questions to deeper views', 'randomly', 'from the end to the beginning', 'only around the interviewer\'s life', 'Logical order helps.'),
        ('Which of these is an open-ended question?', 'What inspired you to start this work?', 'Are you happy?', 'Is your name Meera?', 'Did you come by bus?', 'It cannot be answered in one word.'),
        ('Before an interview, a good interviewer should …', 'research the interviewee\'s work', 'avoid learning anything about the person', 'prepare only yes/no questions', 'write the answers in advance', 'Preparation leads to sharper questions.'),
        ('An interview usually closes with …', 'thanks to the interviewee', 'a complaint', 'a new topic', 'a subject line', 'A polite close.'),
    ],
}
FORM_FACTS['speech'] = FORM_FACTS['article']
FORM_FACTS['bio'] = FORM_FACTS['paragraph']
FORM_FACTS['brochure'] = FORM_FACTS['paragraph']
FORM_FACTS['essay'] = FORM_FACTS['paragraph'] + FORM_FACTS['article'][:4]
FORM_FACTS['description'] = [f for f in FORM_FACTS['paragraph'] if 'brochure' not in f[0] and 'biographical' not in f[0]] + [
    ('A factual description of an object should mainly give …', 'accurate details of its appearance, materials and use', 'the writer\'s opinions only', 'a story with dialogue', 'a list of prices', 'Facts, in order.'),
    ('A factual description is usually written in the …', 'present tense, in a neutral tone', 'future tense, in a humorous tone', 'imperative mood', 'first person, as a diary', 'Neutral present.'),
    ('Which detail suits a factual description of a palm-leaf fan?', 'It is about 30 cm across, woven from dried palm leaves, with a bamboo handle.', 'I think fans are the best thing ever!', 'Once upon a time there was a fan.', 'Dear Sir/Madam,', 'Specific, measurable detail.')]
FORM_FACTS['formal_invitation'] = FORM_FACTS['invitation']
FORM_FACTS['reply'] = FORM_FACTS['invitation']

FORM_AR = {
    'notice': [('A notice is written in a formal, impersonal style.', 'A notice is written in a chatty, personal style.',
                'A notice is meant to inform a large group of people at once.', 'A notice is meant for one close friend.',
                'Because it addresses everyone, it must be formal and clear.'),
               ('A notice does not have a salutation such as "Dear Sir".', 'A notice always begins with "Dear Sir".',
                'A notice is displayed for all readers rather than addressed to one person.', 'A notice is posted to one person\'s home address.',
                'It is displayed for everyone, so no salutation is needed.')],
    'letter': [('A formal letter avoids slang and contractions.', 'A formal letter should use slang to sound friendly.',
                'A formal letter is written to an official or an organisation.', 'A formal letter is written only to family members.',
                'Writing to officials needs a formal register.'),
               ('The subject line helps the receiver understand the letter quickly.', 'The subject line confuses the receiver.',
                'The subject line states the purpose of the letter in a few words.', 'The subject line repeats the sender\'s address.',
                'It sums up the purpose.')],
    'diary': [('A diary entry is written in the first person.', 'A diary entry is written in the third person.',
               'A diary records the writer\'s own experiences and feelings.', 'A diary records only official instructions.',
               'Personal experience is told as "I".')],
    'article': [('An article needs a catchy title.', 'An article should never have a title.',
                 'A title draws readers and tells them what the article is about.', 'A title is used only in diary entries.',
                 'The title attracts and informs readers.')],
    'paragraph': [('A paragraph should begin with a topic sentence.', 'A paragraph should begin with its concluding sentence.',
                   'The topic sentence tells the reader the main idea.', 'The topic sentence gives the date of writing.',
                   'It introduces the main idea.')],
    'story': [('A story must have a climax.', 'A story never needs a turning point.',
               'The climax is the point of highest tension that leads to the ending.', 'The climax is the list of characters.',
               'Tension builds to a climax.')],
    'report': [('A report on a past event is written in the past tense.', 'A report on a past event is written in the future tense.',
                'A report records what has already taken place.', 'A report predicts what will happen next year.',
                'Past events need the past tense.')],
    'invitation': [('A formal invitation is written in the third person.', 'A formal invitation is written in the first person.',
                    'Formal invitations follow a fixed, impersonal convention.', 'Formal invitations are always handwritten poems.',
                    'Convention requires third person.')],
    'email': [('A formal e-mail needs a clear subject line.', 'A formal e-mail should leave the subject line blank.',
               'The subject line tells the receiver what the e-mail is about before it is opened.', 'The subject line is read only after the signature.',
               'It previews the purpose.')],
    'job': [('A résumé is attached to a job application.', 'A résumé is never sent with a job application.',
             'A résumé sums up the applicant\'s qualifications and experience.', 'A résumé is a list of the employer\'s rules.',
             'It supports the application.')],
    'interview': [('Interview questions should be open-ended.', 'Interview questions should all be yes/no questions.',
                   'Open questions encourage the interviewee to share views and experience.', 'Open questions stop the interviewee from talking.',
                   'Open questions draw out detail.')],
    'editor': [('A letter to the Editor deals with an issue of public concern.', 'A letter to the Editor deals with a private family matter.',
                'Newspapers print such letters for the general public to read.', 'Newspapers never print letters from readers.',
                'It is for public readers.')],
}
for _k in ('speech',):
    FORM_AR[_k] = FORM_AR['article']
for _k in ('bio', 'brochure', 'essay', 'description'):
    FORM_AR[_k] = FORM_AR['paragraph']
FORM_AR['formal_invitation'] = FORM_AR['invitation']
FORM_AR['reply'] = FORM_AR['invitation']

FORM_EXPLAIN = {
    'notice': [('Why must a notice be brief and contain the date, time and venue? ', 'Readers glance at notice boards quickly; the key facts must be found at once so they can act on them.'),
               ('How is a notice different from a formal letter?', 'A notice is displayed for many readers, has no salutation, receiver\'s address or complimentary close, and is limited to about 50 words; a letter is addressed to one receiver.')],
    'letter': [('Why is a formal letter divided into paragraphs?', 'Each paragraph deals with one point (purpose, details, request), which makes the letter clear and easy to follow.'),
               ('Why should a letter of request be polite even when the writer is unhappy?', 'Politeness makes the reader more willing to help; a respectful tone keeps the focus on the problem, not on anger.')],
    'editor': [('Why does a letter to the Editor end with suggestions?', 'Pointing out a problem is not enough; suggestions show how it can be solved and make the appeal to the authorities stronger.')],
    'email': [('Why is a specific subject line important in a formal e-mail?', 'Busy readers decide from the subject line whether and when to open a mail; a precise subject also makes the mail easy to find later.')],
    'diary': [('Why is a diary entry written in an informal, personal style?', 'It is written for oneself, so the writer records honest feelings and reflections in a natural first-person voice.'),
              ('What makes a diary entry more than a list of events?', 'Feelings and reflection: the writer explains how the events felt and what they learnt or resolve to do.')],
    'article': [('Why does an article need a catchy title and a byline?', 'The title attracts readers and states the topic; the byline tells readers who wrote it.'),
                ('Why should an article end with suggestions or a call to action?', 'It leaves readers with a clear idea of what they can do, which gives the article a purpose.')],
    'paragraph': [('Why should a descriptive paragraph use sensory details?', 'Details of sight, sound, smell and touch help the reader picture the place or person and make the writing vivid.'),
                  ('Why are linking words important in a paragraph?', 'They connect sentences logically (addition, contrast, sequence) so the paragraph reads smoothly.')],
    'story': [('Why should a story include dialogue?', 'Dialogue reveals character and moves the action forward in a lively way.')],
    'report': [('Why is a report written in an impersonal style?', 'A report presents facts objectively for readers; personal feelings would make it less reliable.')],
    'invitation': [('Why must an invitation mention RSVP or a contact?', 'The host needs to know how many guests will come in order to plan the event.')],
    'job': [('Why should a résumé be attached to a job application?', 'It gives the employer the applicant\'s qualifications and experience in an organised form, so the letter itself can stay short.')],
    'interview': [('Why are open-ended questions better than yes/no questions in an interview?', 'They invite the person to explain experiences and opinions, giving readers richer information.')],
}
for _k in ('speech',):
    FORM_EXPLAIN[_k] = FORM_EXPLAIN['article']
for _k in ('bio', 'brochure', 'essay', 'description'):
    FORM_EXPLAIN[_k] = FORM_EXPLAIN['paragraph']
FORM_EXPLAIN['formal_invitation'] = FORM_EXPLAIN['invitation']
FORM_EXPLAIN['reply'] = FORM_EXPLAIN['invitation']

# Elements of a draft, for "which element is missing" items (label, template).
DRAFT = {
    'notice': [('name of the institution', '{SCHOOL}'), ('the word NOTICE', 'NOTICE'), ('date of issue', '{date}'),
               ('heading', '{HEADING}'), ('body with details', '{BODY}'), ('name and designation of the writer', '{name}\n{role}, {club}')],
    'letter': [("sender's address", '{school}'), ('date', '{date}'), ("receiver's address", 'The Principal\n{school}'),
               ('subject line', 'Subject: {SUBJECT}'), ('salutation', 'Sir/Madam'), ('body', '{BODY}'),
               ('complimentary close', 'Yours faithfully'), ("writer's name", '{name}')],
    'email': [('To line', 'To: principal@school.edu.in'), ('subject line', 'Subject: {SUBJECT}'), ('salutation', 'Dear Sir/Madam,'),
              ('body', '{BODY}'), ('closing', 'Regards,'), ("writer's name", '{name}, Class {class}')],
    'diary': [('day, date and time', '{DAY}, {date}, 9:30 p.m.'), ('salutation to the diary', 'Dear Diary,'), ('body', '{BODY}'),
              ('signature', '{name}')],
    'invitation': [('occasion', '{OCCASION}'), ('date and time', 'on {date} at {time}'), ('venue', 'at {venue}'), ('RSVP / contact', 'RSVP: {name} (Class {class})')],
}
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

INFORMAL_FORMAL = [
    ("Hey, we need you to fix the fans in our class ASAP.", "We request you to kindly get the fans in our classroom repaired at the earliest."),
    ("The canteen food is super bad these days.", "The quality of food in the school canteen has declined considerably of late."),
    ("Kids can't cross the road 'cause there's no zebra crossing.", "Children find it unsafe to cross the road because there is no zebra crossing."),
    ("Pls give us more library books.", "We would be grateful if more books could be added to the library."),
    ("The buses are always late, it's really annoying.", "The buses are frequently delayed, which causes great inconvenience."),
    ("Thanks a ton for the cool workshop!", "We are sincerely grateful to you for conducting the informative workshop."),
    ("Lots of garbage is lying all over the park.", "A large amount of waste has been left scattered across the park."),
    ("I wanna join the summer camp.", "I wish to enrol in the summer camp."),
    ("Your shop sold me a broken fan, not cool.", "The fan I purchased from your store was found to be defective."),
    ("Can you tell me when the results will come out?", "Kindly inform me of the date on which the results will be declared."),
    ("Loads of people turned up for the event.", "The event was attended by a large number of people."),
    ("We're gonna have a meeting on Friday.", "A meeting will be held on Friday."),
    ("The ramp at the station is a total mess.", "The ramp at the station is in a state of disrepair."),
    ("Honestly, the water problem is driving us crazy.", "The shortage of water has caused residents serious distress."),
    ("Give me a call if you need anything.", "Please feel free to contact me if you require any further information."),
    ("Stop chopping trees, guys!", "We appeal to everyone to stop the felling of trees."),
]


def g_form_fact(form):
    facts = FORM_FACTS[form]

    def g(r):
        q, a, d1, d2, d3, why = r.choice(facts)
        return mcq(q, a, [d1, d2, d3], why, r)
    return g


def g_ar_from(tuples, others=()):
    """A-R items from (A, A_false, R, R_false, why) tuples; 'b' pairs A with a true reason from another tuple."""
    def g(r):
        t = r.choice(tuples)
        A, Af, R, Rf, why = t
        codes = ['a']
        if Rf:
            codes.append('c')
        if Af:
            codes.append('d')
        if len(t) > 5 and t[5]:
            codes.append('b')
        code = r.choice(codes)
        if code == 'a':
            return ar(A, R, 'a', f'Both are true and R explains A: {why}')
        if code == 'c':
            return ar(A, Rf, 'c', f'A is true, but R is false; in fact, {lf(R)}')
        if code == 'd':
            return ar(Af, R, 'd', f'A is false; in fact, {lf(A)} R is true.')
        return ar(A, t[5], 'b', f'Both statements are true, but R does not explain A. A is explained by this: {why}')
    return g


def g_explain(pairs, suffix, marks=2, think=False):
    def g(r):
        q, a = r.choice(pairs)
        key = (f'Accept any well-reasoned answer. Value points: {a}' if think else f'Value points: {a}')
        return {'stem': f'{q} {suffix}'.strip(), 'answer': a, 'key': key + f' ({marks} marks: content and expression.)', 'marks': marks}
    return g


def g_form_explain(form):
    return g_explain(FORM_EXPLAIN[form], 'Answer in about 40 words.')


def g_draft_missing(form, ch_topic):
    elems = DRAFT[form]

    def g(r):
        s = slots(r, 9)
        topic = r.choice(ch_topic)
        s.update(SCHOOL=s['school'].upper(), HEADING=topic['heading'].upper(), BODY=fill(topic['body'], s), SUBJECT=topic['subject'],
                 DAY=r.choice(DAYS), OCCASION=topic['occasion'])
        drop = r.randrange(len(elems))
        shown = [fill(t, s) for i, (_, t) in enumerate(elems) if i != drop]
        others = [lab for i, (lab, _) in enumerate(elems) if i != drop]
        wrong = r.sample(others, 3)
        stem = (f'{s["name"]} wrote this draft of a {FORM_LABEL[form]}. Read it and answer.\n\n' + '\n'.join(shown) +
                '\n\nWhich essential element is missing from the draft?')
        return mcq(stem, elems[drop][0], wrong, f'The {elems[drop][0]} is missing; every other element is present.', r)
    return g


def g_register(r):
    a, b = r.choice(INFORMAL_FORMAL)
    return {'stem': f'Rewrite this sentence from a student\'s draft letter in a formal register: "{a}"',
            'answer': b, 'key': f'Model answer: "{b}" (Accept any formal version without slang or contractions; 1 mark.)'}


# ---------------------------------------------------------------- literature families

def meta_facts(ch, subject_chapters):
    """Author and genre recall items from chapter metadata."""
    out = []
    authors = sorted({c['author'] for c in subject_chapters.values() if c.get('author')})
    if ch.get('author') and len(authors) >= 4:
        out.append(('author', ch['author'], [a for a in authors if a != ch['author']]))
    forms = ['poem', 'play', 'short story', 'news report', 'biographical account']
    if ch.get('form') in ('poem', 'play', 'short story'):
        out.append(('genre', ch['form'], [g for g in forms if g != ch['form']]))
    return out


def g_meta(ch, metas):
    def g(r):
        kind, ans, pool = r.choice(metas)
        need(len(pool) >= 3)
        wrong = r.sample(pool, 3)
        if kind == 'author':
            stem = r.choice([f"Who wrote '{ch['title']}'?", f"'{ch['title']}' was written by …", f"Name the writer of '{ch['title']}'."])
            return mcq(stem, ans, wrong, f"'{ch['title']}' is by {ans}.", r)
        stem = r.choice([f"'{ch['title']}' is written in the form of a …", f"In which form is '{ch['title']}' written?"])
        return mcq(stem, ans, wrong, f"'{ch['title']}' is a {ans}.", r)
    return g


def g_fact(facts):
    def g(r):
        f = r.choice(facts)
        q, a, d1, d2, d3 = f[:5]
        why = f[5] if len(f) > 5 else f'{a}.'
        return mcq(q, a, [d1, d2, d3], why, r)
    return g


LEADS_T = ["Which of the following statements about {ref} is correct?", "Which of these statements about {ref} is true?",
           "Pick the accurate statement about {ref}."]
LEADS_F = ["Which of the following statements about {ref} is NOT correct?", "Which of these statements about {ref} is false?",
           "Pick the statement about {ref} that is NOT accurate."]


def g_true(ref, true, false):
    def g(r):
        need(len(false) >= 3)
        t = r.choice(true)
        return mcq(r.choice(LEADS_T).format(ref=ref), t, r.sample(false, 3), f'Correct: "{t}" The other statements contradict the text.', r)
    return g


def g_false(ref, true, false):
    def g(r):
        need(len(true) >= 3)
        f = r.choice(false)
        return mcq(r.choice(LEADS_F).format(ref=ref), f, r.sample(true, 3), f'"{f}" is not correct; the other three statements are true.', r)
    return g


def g_long(pairs, words, marks):
    def g(r):
        q, pts = r.choice(pairs)
        return {'stem': f'{q} Answer in about {words} words.', 'answer': pts,
                'key': f'Value points: {pts} Content {marks - 2}, organisation and expression 2.', 'marks': marks, 'minutes': marks + 3,
                'gap': 'G5'}
    return g


# ---------------------------------------------------------------- editing / rearrangement on true statements

SWAPS = [(r'\bis\b', 'are'), (r'\bwas\b', 'were'), (r'\bhas\b', 'have'), (r'\bdoes\b', 'do'), (r'\bare\b', 'is'), (r'\bwere\b', 'was'), (r'\bhave\b', 'has')]
PAST_PP = {'went': 'gone', 'saw': 'seen', 'took': 'taken', 'gave': 'given', 'wrote': 'written', 'ate': 'eaten', 'began': 'begun',
           'knew': 'known', 'grew': 'grown', 'drew': 'drawn', 'spoke': 'spoken', 'broke': 'broken', 'chose': 'chosen', 'flew': 'flown',
           'fell': 'fallen', 'rose': 'risen', 'drove': 'driven', 'forgot': 'forgotten', 'hid': 'hidden', 'threw': 'thrown', 'sang': 'sung',
           'swam': 'swum', 'drank': 'drunk', 'did': 'done', 'showed': 'shown'}


def inject_error(s: str, r: random.Random):
    """Return (wrong sentence, wrong word, correct word) with exactly one grammatical error, or None."""
    cands = []
    for pat, rep in SWAPS:
        for m in re.finditer(pat, s):
            cands.append((m.start(), m.end(), rep))
    for m in re.finditer(r'\b([Aa]n) (?=[aeiouAEIOU])', s):
        cands.append((m.start(1), m.end(1), 'a' if m.group(1) == 'an' else 'A'))
    for m in re.finditer(r'\b([Aa]) (?=[bcdfgjklmnpqrstvwxyzBCDFGJKLMNPQRSTVWXYZ])', s):
        cands.append((m.start(1), m.end(1), 'an' if m.group(1) == 'a' else 'An'))
    for m in re.finditer(r'\b(' + '|'.join(PAST_PP) + r')\b', s):
        cands.append((m.start(), m.end(), PAST_PP[m.group(1)]))
    if not cands:
        return None
    a, b, rep = r.choice(cands)
    return s[:a] + rep + s[b:], rep, s[a:b]


def g_edit(statements):
    def g(r):
        s = r.choice(statements)
        x = inject_error(s, r)
        need(x)
        wrong, w, c = x
        return {'stem': f'The following sentence about the chapter has one grammatical error. Identify the error and write the correction.\n"{wrong}"',
                'answer': f'{w} → {c}', 'key': f'Error: "{w}"; correction: "{c}". Correct sentence: "{s}" (1 mark)', 'marks': 1}
    return g


def jumble(s: str, r: random.Random):
    w = s.rstrip('.').split()
    if not 6 <= len(w) <= 16:
        return None
    chunks, i = [], 0
    while i < len(w):
        k = r.choice([2, 2, 3]) if len(w) - i > 3 else len(w) - i
        chunks.append(' '.join(w[i:i + k]))
        i += k
    if len(chunks) < 3:
        return None
    order = chunks[:]
    for _ in range(10):
        r.shuffle(order)
        if order != chunks:
            break
    return ' / '.join(order)


def g_rearrange(statements):
    def g(r):
        s = r.choice(statements)
        j = jumble(s, r)
        need(j)
        return {'stem': f'Rearrange the following words and phrases to form a meaningful sentence:\n{j}',
                'answer': s, 'key': f'"{s}" (1 mark; accept any other grammatically correct order with the same meaning.)', 'marks': 1}
    return g


# ---------------------------------------------------------------- vocabulary

def g_vocab(words, mode, ctx=''):
    """words: (word, meaning, synonym, antonym|None, sentence with ___)."""
    def g(r):
        w = r.choice(words)
        word, meaning, syn, ant, sent = w
        others = [x for x in words if x is not w]
        if mode == 'meaning':
            need(len(others) >= 3)
            ds = [x[1] for x in r.sample(others, 3)]
            stem = r.choice([f"What does '{word}' mean?", f"Choose the meaning of '{word}'{ctx}.", f"The word '{word}' means …"])
            return mcq(stem, meaning, ds, f"'{word}' means {meaning}.", r)
        if mode == 'syn':
            need(syn and len([x for x in others if x[2]]) >= 3)
            ds = [x[2] for x in r.sample([x for x in others if x[2]], 3)]
            return mcq(r.choice([f"Choose the word closest in meaning to '{word}'.", f"Which word is a synonym of '{word}'?"]), syn, ds,
                       f"'{word}' ({meaning}) ≈ '{syn}'.", r)
        if mode == 'ant':
            need(ant and syn)
            pool = [x[3] for x in others if x[3]]
            need(len(pool) >= 2)
            ds = [syn] + r.sample(pool, 2)
            return mcq(r.choice([f"Choose the word opposite in meaning to '{word}'.", f"Which word is an antonym of '{word}'?"]), ant, ds,
                       f"'{word}' means {meaning}; its opposite is '{ant}'. ('{syn}' is a synonym, not an antonym.)", r)
        if mode == 'blank':
            need(len(others) >= 3 and '___' in sent)
            ds = [x[0] for x in r.sample(others, 3)]
            return mcq(f'Choose the word that best completes the sentence: "{sent}"', word, ds,
                       f"'{word}' ({meaning}) fits the context.", r)
        if mode == 'replace':
            need(syn and '___' in sent)
            full = sent.replace('___', word)
            return {'stem': f'Rewrite the sentence, replacing \'{word}\' with a word or phrase of similar meaning: "{full}"',
                    'answer': sent.replace('___', syn), 'key': f"Model: '{syn}' (or another word meaning {meaning}). 1 mark.", 'marks': 1}
        if mode == 'use':
            return {'stem': f"Use '{word}' in a sentence of your own that makes its meaning clear{ctx}.",
                    'answer': sent.replace('___', word), 'key': f"'{word}' = {meaning}. Model: \"{sent.replace('___', word)}\" Award 1 mark for correct "
                    'use in context and 1 for a grammatically correct sentence.', 'marks': 2}
        if mode == 'context':
            need('___' in sent)
            full = sent.replace('___', word)
            return {'stem': f'Explain the meaning of \'{word}\' as it is used in this sentence: "{full}"',
                    'answer': meaning, 'key': f"'{word}' here means {meaning} (accept '{syn}' or an equivalent). 1 mark meaning, 1 mark for explaining the context.",
                    'marks': 2} if syn else {'stem': f'Explain the meaning of \'{word}\' as used in: "{full}"', 'answer': meaning,
                                              'key': f'{meaning}. 2 marks.', 'marks': 2}
        if mode == 'cloze':
            need(len(others) >= 4)
            picks = [w] + r.sample(others, 3)
            r.shuffle(picks)
            extra = r.choice([x for x in others if x not in picks])
            box = sorted([p[0] for p in picks] + [extra[0]])
            sents = [p[4].replace('___', f'({roman(i)}) ______') for i, p in enumerate(picks)]
            ans = '; '.join(f'({roman(i)}) {p[0]}' for i, p in enumerate(picks))
            return {'stem': 'Fill in the blanks with words from the box. One word is extra.\nBox: ' + ', '.join(box) + '\n' + ' '.join(sents),
                    'answer': ans, 'key': f'{ans}. ({extra[0]} is not used.) 1 mark each.', 'marks': 4, 'minutes': 5}
        raise ValueError(mode)
    return g


def g_vocab_ar(words):
    def g(r):
        w = r.choice([x for x in words if x[2]])
        word, meaning, syn, ant, sent = w
        others = [x for x in words if x is not w and x[2]]
        need(others)
        full = sent.replace('___', word)
        code = r.choice('acd')
        if code == 'a':
            return ar(f"In the sentence \"{full}\", '{word}' can be replaced by '{syn}' without changing the meaning.",
                      f"'{word}' and '{syn}' both mean {meaning}.", 'a', f"'{syn}' is a synonym of '{word}'.")
        o = r.choice(others)
        if code == 'c':
            return ar(f"In the sentence \"{full}\", '{word}' can be replaced by '{syn}' without changing the meaning.",
                      f"'{word}' means {o[1]}.", 'c', f"'{word}' means {meaning}, not {o[1]}.")
        return ar(f"In the sentence \"{full}\", '{word}' can be replaced by '{o[2]}' without changing the meaning.",
                  f"'{word}' means {meaning}.", 'd', f"'{o[2]}' does not mean {meaning}; '{syn}' would fit.")
    return g


def g_vocab_para(words, topics, grade):
    def g(r):
        k = 4 if len(words) >= 6 else 3
        ws = r.sample([w[0] for w in words], k)
        t = r.choice(topics)
        n, _ = person(r)
        return {'stem': f"{n} has to write a paragraph of 80–100 words on '{t}'. Write it, using at least {k - 1} of these words "
                        f"from the chapter correctly: {', '.join(ws)}. Underline the words you use.",
                'answer': f'A coherent paragraph on {t} using the words correctly.',
                'key': 'Format/organisation 1 (topic sentence, development, conclusion); correct use of the words 2; content and expression 2.',
                'marks': 5, 'minutes': 8}
    return g


# ---------------------------------------------------------------- extracts (original passages on the chapter)

def _ex_stem(intro, text):
    return f'{intro}\n\n"{text}"\n\n'


def g_extract_one(ch, extracts, mcq_only):
    def g(r):
        text, qs = r.choice(extracts)[1:3]
        pool = [q for q in qs if (len(q) > 2 and q[2]) == mcq_only]
        need(pool)
        q = r.choice(pool)
        intro = ch['extract_intro']
        if mcq_only:
            return mcq(_ex_stem(intro, text) + q[0], q[1], q[2], f'{q[1]}.', r)
        return {'stem': _ex_stem(intro, text) + q[0], 'answer': q[1], 'key': f'{q[1]} (1–2 marks for a complete answer.)',
                'marks': 2 if len(q[1].split()) > 12 else 1}
    return g


def extract_set(r, ch, extracts, n):
    text, qs = r.choice(extracts)[1:3]
    need(len(qs) >= n)
    picks = r.sample(range(len(qs)), n)
    picks.sort()
    lines, ans = [], []
    for i, k in enumerate(picks):
        q = qs[k]
        if len(q) > 2 and q[2]:
            opts = [q[1]] + list(q[2])
            r.shuffle(opts)
            lines.append(f'({roman(i)}) {q[0]}  {inline_opts(opts)}')
            ans.append(f'({roman(i)}) ({"abcd"[opts.index(q[1])]}) {q[1]}')
        else:
            lines.append(f'({roman(i)}) {q[0]}')
            ans.append(f'({roman(i)}) {q[1]}')
    stem = _ex_stem(ch['extract_intro'], text) + 'Answer the following:\n' + '\n'.join(lines)
    a = ' '.join(ans)
    return {'stem': stem, 'answer': a, 'key': a + f' (1 mark each, {n} marks.)', 'marks': n, 'minutes': n + 2, 'gap': 'G7'}


def g_extract_set(ch, extracts, n):
    return lambda r: extract_set(r, ch, extracts, n)


# ---------------------------------------------------------------- reading passages (original)

def g_passage_one(passages, mcq_only):
    def g(r):
        p = r.choice(passages)
        qs = [q for q in p['qs'] if bool(len(q) > 3 and q[3]) == mcq_only]
        need(qs)
        q = r.choice(qs)
        para = p['paras'][q[0]]
        head = f'Read this paragraph from a passage titled "{p["title"]}".\n\n{para}\n\n'
        if mcq_only:
            return mcq(head + q[1], q[2], q[3], f'{q[2]}.', r)
        return {'stem': head + q[1], 'answer': q[2], 'key': f'{q[2]} (1–2 marks.)', 'marks': 2 if len(q[2].split()) > 10 else 1, 'gap': 'G7'}
    return g


def passage_set(r, passages, n):
    p = r.choice(passages)
    need(len(p['qs']) >= n)
    picks = sorted(r.sample(range(len(p['qs'])), n), key=lambda k: (p['qs'][k][0], k))
    lines, ans = [], []
    for i, k in enumerate(picks):
        q = p['qs'][k]
        if len(q) > 3 and q[3]:
            opts = [q[2]] + list(q[3])
            r.shuffle(opts)
            lines.append(f'({roman(i)}) {q[1]}  {inline_opts(opts)}')
            ans.append(f'({roman(i)}) ({"abcd"[opts.index(q[2])]}) {q[2]}')
        else:
            lines.append(f'({roman(i)}) {q[1]}')
            ans.append(f'({roman(i)}) {q[2]}')
    body = '\n\n'.join(f'{j + 1}. {t}' for j, t in enumerate(p['paras']))
    stem = f'Read the passage below and answer the questions that follow.\n\n{p["title"]}\n\n{body}\n\n' + '\n'.join(lines)
    a = ' '.join(ans)
    return {'stem': stem, 'answer': a, 'key': a + f' (1 mark each, {n} marks.)', 'marks': n, 'minutes': round(n * 1.6), 'gap': 'G7'}


# Data-based (case-based factual) passages: numbers are random, answers computed.
DATA_TOPICS = [
    dict(t='how students travel to school', who='students', q='how they usually travel to school',
         cats=['walking', 'cycling', 'school bus', 'public transport', 'private car or two-wheeler'], word='commute'),
    dict(t='reading habits', who='students', q='what they read most often in their free time',
         cats=['storybooks and novels', 'comics', 'newspapers', 'magazines', 'nothing at all'], word='leisure'),
    dict(t='screen time', who='teenagers', q='how many hours a day they spend on screens outside school',
         cats=['less than one hour', 'one to two hours', 'two to four hours', 'more than four hours'], word='excessive'),
    dict(t='waste segregation at home', who='households', q='how they dispose of household waste',
         cats=['separate wet and dry waste', 'compost kitchen waste', 'mix all waste in one bin', 'burn some of the waste'], word='segregate'),
    dict(t='sports participation', who='students', q='which sport they play regularly',
         cats=['cricket', 'football', 'badminton', 'kabaddi', 'athletics', 'no sport'], word='regularly'),
    dict(t='buying handmade products', who='shoppers at a city fair', q='how often they buy handmade craft products',
         cats=['every month', 'a few times a year', 'only during festivals', 'never'], word='artisans'),
    dict(t='letters and messages', who='adults', q='how they most often send messages to relatives',
         cats=['instant messaging apps', 'phone calls', 'e-mail', 'handwritten letters or postcards'], word='correspondence'),
    dict(t='water use', who='families', q='which activity uses most of their daily water',
         cats=['bathing', 'washing clothes', 'cooking and drinking', 'cleaning the house', 'gardening'], word='conserve'),
    dict(t='music in daily life', who='students', q='when they listen to music most',
         cats=['while studying', 'while travelling', 'while exercising', 'before sleeping', 'rarely or never'], word='soothing'),
    dict(t='care for elderly neighbours', who='residents of a housing society', q='how often they spend time with elderly people in their area',
         cats=['daily', 'every week', 'once a month', 'hardly ever'], word='companionship'),
    dict(t='energy use', who='households', q='which appliance they think uses the most electricity at home',
         cats=['air conditioner', 'refrigerator', 'water heater', 'fans and lights', 'television'], word='consumption'),
    dict(t='accessibility of public places', who='wheelchair users', q='which facility they find missing most often in public places',
         cats=['ramps', 'accessible toilets', 'lifts', 'reserved parking', 'tactile paths and signs'], word='accessible'),
]
WORD_MEANS = {'commute': 'travel regularly between home and a place of work or study', 'leisure': 'free time',
              'excessive': 'more than is necessary or healthy', 'segregate': 'separate into groups', 'regularly': 'at frequent, even intervals',
              'artisans': 'skilled workers who make things by hand', 'correspondence': 'communication by letters or messages',
              'conserve': 'protect from waste or loss', 'soothing': 'calming', 'companionship': 'the pleasure of being with others',
              'consumption': 'the amount used', 'accessible': 'easy to reach, enter or use'}
WORD_WRONG = list(WORD_MEANS.values())


def _split(r, k):
    while True:
        cuts = sorted(r.sample(range(4, 96), k - 1))
        parts = [b - a for a, b in zip([0] + cuts, cuts + [100])]
        if min(parts) >= 4 and len(set(parts)) == k:
            return parts


def data_case(r, grade, n_q, topics=None, one='mcq'):
    tp = r.choice(topics or DATA_TOPICS)
    cats = tp['cats']
    k = len(cats)
    pct = _split(r, k)
    total = r.choice([200, 300, 400, 500, 600, 800, 1000])
    city = r.choice(CITIES)
    year = r.choice([2025, 2026])
    order = sorted(range(k), key=lambda i: -pct[i])
    lines = '; '.join(f'{cats[i]} – {pct[i]}%' for i in range(k))
    passage = (f'A survey on {tp["t"]} was carried out in {city} in {year}. {total} {tp["who"]} were asked {tp["q"]}. '
               f'The results were: {lines}. The organisers said the findings would help them plan better, and they encouraged '
               f'people to think about how they {tp["word"]} and use their time and resources.' if tp['word'] in ('commute', 'conserve', 'segregate')
               else f'A survey on {tp["t"]} was carried out in {city} in {year}. {total} {tp["who"]} were asked {tp["q"]}. '
               f'The results were: {lines}. The word "{tp["word"]}" came up often in the discussion that followed the survey.')
    hi, lo = order[0], order[-1]
    a, b = r.sample(range(k), 2)
    qs = []
    qs.append((f'Which response was the most common?', cats[hi], [cats[i] for i in order[1:4]]))
    qs.append((f'Which response was the least common?', cats[lo], [cats[i] for i in order[:3]]))
    qs.append((f'How many {tp["who"]} chose "{cats[a]}"?', str(total * pct[a] // 100),
               [str(total * pct[b] // 100), str(pct[a]), str(total * pct[a] // 10)]))
    diff = abs(pct[a] - pct[b])
    qs.append((f'By how many percentage points does "{cats[a]}" differ from "{cats[b]}"?', str(diff),
               [str(pct[a] + pct[b]), str(diff + 5), str(abs(diff - 3) or 2)]))
    top2 = pct[order[0]] + pct[order[1]]
    qs.append((f'What percentage of {tp["who"]} chose one of the two most common responses taken together?', f'{top2}%',
               [f'{pct[order[0]]}%', f'{100 - top2}%', f'{top2 + 10}%']))
    maj = 'more than half' if pct[hi] > 50 else 'less than half'
    qs.append((f'Did more than half of the {tp["who"]} choose "{cats[hi]}"? Give the figure.', f'{"Yes" if pct[hi] > 50 else "No"} – {pct[hi]}%, which is {maj}.', None))
    true_s = f'"{cats[order[0]]}" was chosen by more {tp["who"]} than "{cats[order[1]]}".'
    false1 = f'"{cats[order[-1]]}" was chosen by more {tp["who"]} than "{cats[order[0]]}".'
    false2 = f'Every response was chosen by the same number of {tp["who"]}.'
    false3 = f'The survey was carried out in {r.choice([c for c in CITIES if c != city])}.'
    qs.append(('Which of these statements is supported by the survey?', true_s, [false1, false2, false3]))
    w = tp['word']
    qs.append((f'In the passage, the word "{w}" means …', WORD_MEANS[w], r.sample([x for x in WORD_WRONG if x != WORD_MEANS[w]], 3)))
    qs.append((f'Suggest one reason why "{cats[lo]}" may have been chosen by so few {tp["who"]}.',
               'Any sensible reason linked to the context (cost, habit, lack of access, awareness, time) – 1 mark.', None))
    qs.append((f'Write one suggestion the organisers could make, based on the survey on {tp["t"]}.',
               'Any practical suggestion that follows from the figures – 1 mark.', None))
    qs.append((f'What fraction of the {tp["who"]} did NOT choose "{cats[a]}"? Answer as a percentage.', f'{100 - pct[a]}%',
               [f'{pct[a]}%', f'{100 - pct[b]}%', f'{50 - pct[a] if pct[a] < 50 else pct[a] - 50}%']))
    qs.append((f'Rank the top three responses, starting with the most common.', ', '.join(cats[i] for i in order[:3]), None))
    # de-duplicate MCQ distractors that may coincide with the answer
    clean = []
    for q, a_, ds in qs:
        if ds:
            seen, d2 = {onorm(a_)}, []
            for d in ds:
                if onorm(d) not in seen:
                    d2.append(d)
                    seen.add(onorm(d))
            fill_ = [f'{x}%' if a_.endswith('%') else str(x) for x in range(7, 99, 11)]
            for x in fill_:
                if len(d2) == 3:
                    break
                if onorm(x) not in seen:
                    d2.append(x)
                    seen.add(onorm(x))
            ds = d2
        clean.append((q, a_, ds))
    qs = clean
    if n_q == 1:
        q, a_, ds = r.choice([x for x in qs if bool(x[2]) == (one == 'mcq')])
        stem = f'Read the survey report and answer.\n\n{passage}\n\n{q}'
        if ds:
            return mcq(stem, a_, ds, f'{a_} (worked from the figures).', r)
        return {'stem': stem, 'answer': a_, 'key': a_, 'marks': 1, 'gap': 'G7'}
    need(len(qs) >= n_q)
    picks = sorted(r.sample(range(len(qs)), n_q))
    lines_, ans = [], []
    for i, kk in enumerate(picks):
        q, a_, ds = qs[kk]
        if ds:
            opts = [a_] + ds
            r.shuffle(opts)
            lines_.append(f'({roman(i)}) {q}  {inline_opts(opts)}')
            ans.append(f'({roman(i)}) ({"abcd"[opts.index(a_)]}) {a_}')
        else:
            lines_.append(f'({roman(i)}) {q}')
            ans.append(f'({roman(i)}) {a_}')
    stem = f'Read the survey report and answer the questions that follow.\n\n{passage}\n\n' + '\n'.join(lines_)
    a_ = ' '.join(ans)
    return {'stem': stem, 'answer': a_, 'key': a_ + f' (1 mark each.)', 'marks': n_q, 'minutes': round(n_q * 1.5), 'gap': 'G7'}


# ---------------------------------------------------------------- family assembly

def lit_families(ch, st, chs, grade, extracts, statements_all, others_ar):
    ref = st.get('ref', ch['ref'])
    out = []
    facts = st.get('facts', [])
    true, false = st.get('true', []), st.get('false', [])
    sw = '40–50' if grade >= 11 else 'about 40'
    if facts:
        out += [F('C1', 'D1', 'mcq', g_fact(facts)), F('C1', 'D2', 'mcq', g_fact(facts))]
    if st.get('meta'):
        out.append(F('C1', 'D2', 'mcq', g_meta(ch, st['meta'])))
    if true and false:
        out += [F('C2', 'D2', 'mcq', g_true(ref, true, false)), F('C2', 'D3', 'mcq', g_false(ref, true, false))]
    if st.get('ar'):
        out.append(F('C2', 'D3', 'mcq', g_ar_from(st['ar'], others_ar), kinds=('ar',)))
    if st.get('explain'):
        out.append(F('C2', 'D2', 'explain', g_explain(st['explain'], f'Answer in {sw} words.')))
        out.append(F('C3', 'D3', 'explain', g_explain(st['explain'][::-1], f'Answer in {sw} words.')))
    if st.get('think'):
        out.append(F('C4', 'D3', 'explain', g_explain(st['think'], f'Answer in {sw} words.', think=True), gap='G5'))
    if st.get('long'):
        w = '120–150' if grade >= 11 else '100–120'
        out.append(F('C4', 'D4', 'long', g_long(st['long'], w, 6 if grade == 9 else 5)))
    if extracts:
        if any(len(q) > 2 and q[2] for e in extracts for q in e[2]):
            out.append(F('C3', 'D2', 'mcq', g_extract_one(ch, extracts, True)))
        if any(not (len(q) > 2 and q[2]) for e in extracts for q in e[2]):
            out.append(F('C3', 'D3', 'short', g_extract_one(ch, extracts, False)))
        out.append(F('C3', 'D4', 'case', g_extract_set(ch, extracts, 4)))
    if grade <= 10 and statements_all:
        out.append(F('C3', 'D2', 'short', g_edit(statements_all), gap='G3'))
        out.append(F('C3', 'D1', 'short', g_rearrange(statements_all), gap='G3'))
    if ch.get('vocab') and not ch.get('_has_vocab_st'):
        out.append(F('C3', 'D1', 'mcq', g_vocab(ch['vocab'], 'meaning', ' as used in the chapter')))
    return out


def vocab_families(ch, st, grade):
    words = list(st.get('words', [])) + ([] if st.get('own_only') else list(ch.get('vocab', [])))
    topics = ch.get('topics', [ch['title']])
    out = [F('C1', 'D1', 'mcq', g_vocab(words, 'meaning')), F('C1', 'D2', 'mcq', g_vocab(words, 'meaning', ' in the chapter context')),
           F('C2', 'D2', 'mcq', g_vocab(words, 'syn')), F('C2', 'D3', 'mcq', g_vocab_ar(words), kinds=('ar',)),
           F('C2', 'D3', 'explain', g_vocab(words, 'context')), F('C3', 'D1', 'mcq', g_vocab(words, 'blank')),
           F('C3', 'D2', 'short', g_vocab(words, 'replace')), F('C3', 'D4', 'case', g_vocab(words, 'cloze')),
           F('C4', 'D3', 'explain', g_vocab(words, 'use')), F('C4', 'D4', 'long', g_vocab_para(words, topics, grade))]
    if sum(1 for w in words if w[3]) >= 3:
        out.append(F('C2', 'D3', 'mcq', g_vocab(words, 'ant')))
    for extra in st.get('extra', []):
        out.append(extra)
    return out


def write_families(ch, st, grade, ch_prompts):
    form = st['form']
    out = [F('C1', 'D1', 'mcq', g_form_fact(form)), F('C1', 'D2', 'mcq', g_form_fact(form)), F('C2', 'D2', 'explain', g_form_explain(form)),
           F('C2', 'D3', 'mcq', g_ar_from(FORM_AR[form]), kinds=('ar',)), F('C3', 'D3', 'short', g_register)]
    dform = form if form in DRAFT else ('letter' if form in ('editor', 'job') else None)
    if dform and st.get('draft'):
        out.append(F('C3', 'D2', 'mcq', g_draft_missing(dform, st['draft'])))
    prompts = [p for p in ch_prompts] + [p for p in st.get('prompts', [])]
    need(prompts)

    def gw(r, hard=False):
        p = r.choice(prompts)
        return writing_item(r, grade, p[0], p[1], p[2])
    out += [F('C4', 'D4', 'long', gw), F('C4', 'D5', 'long', gw), F('C3', 'D4', 'long', gw)]
    if st.get('opening'):
        out.append(F('C4', 'D3', 'explain', g_explain(st['opening'], '', marks=2)))
    if st.get('extra'):
        out += st['extra']
    return out


READ_FACTS = [
    ('Reading a passage quickly to get its general idea is called …', 'skimming', 'scanning', 'summarising', 'paraphrasing', 'Skim for gist.'),
    ('Looking quickly through a text for a specific fact, such as a date, is called …', 'scanning', 'skimming', 'editing', 'proofreading', 'Scan for detail.'),
    ('In note-making, main points are shown under …', 'headings and numbered sub-headings', 'long full sentences', 'a salutation', 'quotation marks only', 'Notes use headings and sub-points.'),
    ('Which of these is a proper abbreviation for use in notes?', 'govt. (government)', 'gvrnmnt', 'G!', 'gov-ment', 'Standard, recognisable abbreviations.'),
    ('A summary should be about … of the original passage.', 'one-third', 'twice the length', 'the same length', 'one-tenth of a line', 'A summary is roughly a third of the original.'),
    ('Which question helps you infer the writer\'s attitude?', 'What words show the writer\'s feelings about the topic?', 'How many paragraphs are there?', 'What is the font size?', 'Who printed the book?', 'Word choice reveals attitude.'),
    ('The central idea of a passage is usually found in …', 'the title and the opening/topic sentences', 'the page number', 'the last word only', 'the punctuation marks', 'Topic sentences carry the main idea.'),
    ('An inference is …', 'a conclusion drawn from clues in the text', 'a word copied from the text', 'a spelling mistake', 'the title of the passage', 'Reading between the lines.'),
    ('A list of abbreviations used should be given …', 'at the end of the notes (a key)', 'inside the title', 'nowhere', 'in the first sentence of the summary', 'Key to abbreviations.'),
]
READ_AR = [('Skimming helps a reader find the main idea quickly.', 'Skimming helps a reader find one exact date.', 'Skimming means reading quickly for the general sense.',
            'Skimming means reading every word slowly.', 'Skim = gist.'),
           ('Notes should be brief.', 'Notes should repeat the passage in full.', 'Notes record only the key points in a short form.', 'Notes must contain every sentence of the text.', 'Brevity.'),
           ('An inference is not stated directly in the text.', 'An inference is always copied from the text.', 'It is a conclusion the reader draws from clues and evidence.', 'It is a word found in the title.', 'Reading between the lines.')]
READ_EXPLAIN = [('How is note-making different from writing a summary?', 'Notes list key points under headings with abbreviations; a summary is a short continuous paragraph in full sentences.'),
                ('Why is it useful to skim a passage before answering questions on it?', 'Skimming gives the overall idea and structure, so you know where to look for details later.'),
                ('What makes a good title for a passage?', 'It is short, catchy and sums up the central idea of the passage.'),
                ('How can you find the meaning of a difficult word without a dictionary?', 'Use context clues: the sentence around it, examples, contrasts, and word parts such as prefixes.')]


def read_families(ch, st, grade, passages):
    out = [F('C1', 'D1', 'mcq', g_fact(READ_FACTS)), F('C1', 'D2', 'mcq', g_fact(READ_FACTS)), F('C2', 'D3', 'mcq', g_ar_from(READ_AR), kinds=('ar',)),
           F('C2', 'D2', 'explain', g_explain(READ_EXPLAIN, 'Answer in about 40 words.'))]
    if passages:
        out += [F('C3', 'D2', 'mcq', g_passage_one(passages, True), gap='G7'), F('C3', 'D3', 'short', g_passage_one(passages, False), gap='G7')]
    topics = st.get('data_topics')
    out += [F('C3', 'D1', 'mcq', lambda r: data_case(r, grade, 1, topics), gap='G7'),
            F('C4', 'D3', 'short', lambda r: data_case(r, grade, 1, topics, one='short'), gap='G7'),
            F('C3', 'D4', 'case', lambda r: data_case(r, grade, 5, topics), gap='G7')]
    for extra in st.get('extra', []):
        out.append(extra)
    return out


def build_subject(sid, generated_by, grade, chapters, mock_pattern, passages=None, mock_extra=None, seed=None):
    """chapters: {n: chapter dict}. passages: {chapter n: [passage dicts]} for reading subtopics.
    mock_extra(chapters, families) -> {st_id: [Family]} mock-only families."""
    from eng_kit_g8_g9_g12_grammar import gram_families
    fams = {}
    mock_fams = {}
    all_ar = []
    for n, ch in chapters.items():
        for k, st in ch['sts'].items():
            all_ar += st.get('ar', [])
    for n, ch in chapters.items():
        cid = f'{sid}-ch{n:02d}'
        g = ch.get('genre', 'chapter')
        ch.setdefault('ref', f"the {g} '{ch['title']}'")
        ch.setdefault('extract_intro', f"Read the passage below, based on the {g} '{ch['title']}', and answer.")
        ch['_has_vocab_st'] = any(st['kind'] == 'vocab' for st in ch['sts'].values())
        metas = meta_facts(ch, chapters)
        first_lit = next((k for k, st in ch['sts'].items() if st['kind'] == 'lit'), None)
        for k, st in ch['sts'].items():
            sid_ = f'{cid}-st{k}'
            kind = st['kind']
            exs = [e for e in ch.get('extracts', []) if e[0] == k]
            prompts = [p for p in ch.get('writing', []) if p[3] in (0, k)]
            if kind == 'lit':
                if k == first_lit and metas:
                    st = dict(st, meta=metas)
                stmts = st.get('true', []) + st.get('statements', [])
                fl = lit_families(ch, st, chapters, grade, exs, stmts, [a for a in all_ar if a not in st.get('ar', [])])
                if prompts:
                    fl.append(F('C4', 'D5', 'long', (lambda ps: lambda r: _w(r, grade, ps))(prompts)))
                fams[sid_] = fl
            elif kind == 'vocab':
                fams[sid_] = vocab_families(ch, st, grade)
            elif kind == 'gram':
                fams[sid_] = gram_families(st, ch, grade)
            elif kind == 'write':
                fams[sid_] = write_families(ch, st, grade, [(p[0], p[1], p[2]) for p in ch.get('writing', []) if p[0] == st['form'] or p[3] == k])
            elif kind == 'read':
                fams[sid_] = read_families(ch, st, grade, (passages or {}).get(n, []))
            else:
                raise SystemExit(kind)
    if mock_extra:
        mock_fams = mock_extra(chapters, fams)
    return fams, mock_fams


def _w(r, grade, prompts):
    p = r.choice(prompts)
    return writing_item(r, grade, p[0], p[1], p[2])


class EngBuilder(Builder):
    """Builder whose mocks may also use mock-only families (reading passages, writing tasks, extract sets)."""

    def __init__(self, *a, mock_families=None, **kw):
        super().__init__(*a, **kw)
        self.mock_families = mock_families or {}

    def _mocks(self, chapters):
        for st, fl in self.mock_families.items():
            for f in fl:
                f.st = st
            self.families.setdefault(st, []).extend(fl)
        return super()._mocks(chapters)


# ---------------------------------------------------------------- mock-only family helpers

def mock_writing(ch, grade, forms, kind, marks, C='C4', D='D4'):
    ps = [p for p in ch.get('writing', []) if p[0] in forms]
    if not ps:
        return []

    def g(r):
        p = r.choice(ps)
        return writing_item(r, grade, p[0], p[1], p[2], marks=marks)
    return [F(C, D, 'long', g, kinds=(kind,), gap='G5')]


def mock_short_set(ch, grade, n, kind, marks_each=2, sts=None):
    pairs = []
    for k, st in ch['sts'].items():
        if st['kind'] == 'lit' and (sts is None or k in sts):
            pairs += [(q, a) for q, a in st.get('explain', []) + st.get('think', [])]
    if len(pairs) < n:
        return []
    w = '40–50' if grade >= 11 else 'about 40'

    def g(r):
        ps = r.sample(pairs, n)
        stem = f'Answer the following questions in {w} words each.\n' + '\n'.join(f'({roman(i)}) {q}' for i, (q, _) in enumerate(ps))
        a = ' '.join(f'({roman(i)}) {x}' for i, (_, x) in enumerate(ps))
        return {'stem': stem, 'answer': a, 'key': a + f' ({marks_each} marks each.)', 'marks': n * marks_each}
    return [F('C2', 'D3', 'explain', g, kinds=(kind,))]


def mock_long(ch, grade, kind, marks):
    pairs = []
    for st in ch['sts'].values():
        if st['kind'] == 'lit':
            pairs += st.get('long', [])
    if not pairs:
        return []
    w = '120–150' if grade >= 11 else '100–120'
    return [F('C4', 'D4', 'long', g_long(pairs, w, marks), kinds=(kind,))]


def mock_extract(ch, n, kind):
    exs = [e for e in ch.get('extracts', []) if len(e[2]) >= n]
    if not exs:
        return []
    return [F('C3', 'D3', 'case', g_extract_set(ch, exs, n), kinds=(kind,))]


def first_st(ch, cid, kinds=('lit',)):
    for k, st in ch['sts'].items():
        if st['kind'] in kinds:
            return f'{cid}-st{k}'
    return f'{cid}-st{min(ch["sts"])}'


def mock_extra_g8_g9(sid, grade, passages):
    """Mock-only families for the class 8/9 paper design (14 questions, 80 marks):
    Reading 2 x 10 (readA passage, readB data case); Grammar 2 x 5; Writing 4 x 5; Literature: 2 extracts x 5,
    2 short-answer sets x 4, 2 long answers x 6."""
    from eng_kit_g8_g9_g12_grammar import mock_grammar

    def extra(chapters, fams):
        out = {}
        for n, ch in chapters.items():
            cid = f'{sid}-ch{n:02d}'
            for k, st in ch['sts'].items():
                stid = f'{cid}-st{k}'
                if st['kind'] == 'gram':
                    out.setdefault(stid, []).extend(mock_grammar(st, ch, grade, 5, 'grammar5'))
                if st['kind'] == 'read':
                    ps = passages.get(n, [])
                    if ps:
                        out.setdefault(stid, []).append(F('C3', 'D3', 'case', (lambda ps_: lambda r: passage_set(r, ps_, 10))(ps), kinds=('readA',), gap='G7'))
                    out.setdefault(stid, []).append(F('C3', 'D3', 'case', lambda r: data_case(r, grade, 10, st.get('data_topics')), kinds=('readB',), gap='G7'))
            wst = next((f'{cid}-st{k}' for k, st in ch['sts'].items() if st['kind'] == 'write'), first_st(ch, cid))
            prompts = [p[:3] for p in ch.get('writing', [])]
            for k, st in ch['sts'].items():
                prompts += [p[:3] for p in st.get('prompts', [])]
            if prompts:
                out.setdefault(wst, []).append(F('C4', 'D4', 'long', (lambda ps_: lambda r: writing_item(r, grade, *r.choice(ps_), marks=5))(prompts), kinds=('writing5',), gap='G5'))
            lst = first_st(ch, cid)
            exs = ch.get('extracts', [])
            if exs:
                est = f'{cid}-st{exs[0][0]}'
                out.setdefault(est, []).extend(mock_extract(ch, 5, 'extract5'))
            out.setdefault(lst, []).extend(mock_short_set(ch, grade, 2, 'litshort4'))
            out.setdefault(lst, []).extend(mock_long(ch, grade, 'litlong6', 6))
        return out
    return extra


PATTERN_G8_G9 = [(1, 10, 'readA'), (1, 10, 'readB'), (2, 5, 'grammar5'), (4, 5, 'writing5'), (2, 5, 'extract5'), (2, 4, 'litshort4'), (2, 6, 'litlong6')]


def run(sid, generated_by, grade, chapters, pattern, passages, mock_extra, accuracy=None):
    fams, mock_fams = build_subject(sid, generated_by, grade, chapters, pattern, passages, mock_extra)
    b = EngBuilder(sid, generated_by, fams, pattern, mock_families=mock_fams, mock_minutes_per_mark=2.25)
    files = b.build()
    b.write(files, accuracy)
    print(f'{sid}: wrote {sum(len(v) for v in files.values())} questions')
    return files
