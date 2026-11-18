"""Cambridge IGCSE First Language English 0500 (grade 10): writing units.

Writing skills (W1–W5), directed writing (Paper 2 Section A), descriptive and narrative composition, and
argumentative / discursive composition. All source texts, model paragraphs, sentences and titles are
original. Extended tasks are level-marked like Cambridge: directed writing splits Reading and Writing,
compositions split Content and structure from Style and accuracy (roughly 16 : 24).
Shared machinery (Text, feature / classify / rewrite templates, level keys) comes from g8_english.
"""
import re

from ._lib import topic, mcq, compose, person, city  # noqa: F401
from .g8_english import (Q, clean, cap, upto, bands, STYLE, CONTENT, DEF, Text, Feat, mk, levels_key, reading_key, points_key, compose_templates, extended_templates,
                         build_parts, feature_templates, classify_templates, rewrite_templates, settle_fixed_marks, keypts)

PROFILE = {'mark_scale': {'long': (2.5, 3)}, 'wordy': True}
CHAPTERS = {}

WORDS10 = {1: '150–200', 2: '200–250', 3: '250–350', 4: '350–450', 5: '350–450'}

STYLE10 = ('vocabulary is wide, precise and used for deliberate effect; sentence structures are varied and controlled to create effects; register is consistently appropriate; spelling, punctuation and grammar are almost always accurate (W3–W5)',
           'vocabulary is generally appropriate with some ambition; some variety of sentence structure; register mostly appropriate; errors are occasional and minor (W3–W5)',
           'vocabulary is simple or imprecise; sentence structures are repetitive; register may be inconsistent; frequent errors sometimes affect clarity (W3–W5)')


def comp_key(m, genre, ind):
    """Composition: Content and structure (W1–W2) about 40%, Style and accuracy (W3–W5) about 60%."""
    return levels_key(m, genre, ind, style=STYLE10, split=0.4).replace('Content and structure –', 'Content and structure (W1–W2) –')


def directed_key(m, reading_ind, writing_ind):
    a = max(1, round(m * 0.4))
    b = m - a
    lo, mi, hi = bands(a)
    slo, smi, shi = bands(b)
    return (f'Level-marked out of {m}: Reading {a} marks, Writing {b} marks. '
            f'Reading – top band ({hi}): ideas from both texts selected, developed and critically evaluated; a clear, sustained judgement of your own; middle band ({mi}): relevant ideas from both texts with some evaluation; lower band ({lo}): ideas mostly repeated from the texts with little evaluation. '
            f'Writing – top band ({shi}): form, voice and register consistently suited to the audience and purpose; well structured and cohesive; precise, varied language; accurate; middle band ({smi}): mostly appropriate form and register; clear structure; generally accurate; lower band ({slo}): form or register insecure; loosely organised; errors affect clarity. '
            f'Indicative reading content: {reading_ind} Writing: {writing_ind}')


def comp_task(D, stem, genre, ind, model, C='C4'):
    m = mk(C, D, 'long', PROFILE)
    return {'stem': clean(stem) + f' Write about {WORDS10.get(D, "350–450")} words.', 'answer': model, 'key': comp_key(m, genre, ind), 'type': 'long'}


def comp_templates(t, tasks, genre, C='C4', D=(2, 3, 4, 5)):
    tasks = list(tasks)

    @t.add(C, D, 'long')
    def comp(r, D_):
        stem, ind, model = r.choice(tasks)
        return comp_task(D_, stem, genre, ind, model, C=C)


def pick_frame(r, frames, **kw):
    return r.choice(frames).format(**kw)


# =========================================================== 1 Writing skills

# ---------------------------------------------------------------- 1.1 W1–W5
WOBJ = [
    ('W1', 'articulate experience and express what is thought, felt and imagined'),
    ('W2', 'organise and structure ideas and opinions for deliberate effect'),
    ('W3', 'use a range of vocabulary and sentence structures appropriate to context'),
    ('W4', 'use register appropriate to context'),
    ('W5', 'make accurate use of spelling, punctuation and grammar'),
]
WEAK = [
    ('The market was busy. There were lots of people. It was noisy. There were lots of stalls.', 'W3', 'vocabulary is vague (‘lots of’) and every sentence is a short simple sentence, so there is no range of vocabulary or sentence structure.',
     'Model: Shoppers jostled between the stalls, haggling over mangoes and bolts of indigo cloth, while a radio blared from somewhere behind a mountain of melons.'),
    ('Dear Sir, hey, I think your plan for the park is well bad and you should totally scrap it.', 'W4', 'the register is far too informal for a formal letter to an official (hey, well bad, totally).',
     'Model: Dear Sir, I am writing to express my concerns about the proposed changes to the park, which I believe should be reconsidered.'),
    ('Its been a long time since there was rain, the crops are dying and the farmers is worried.', 'W5', 'there are errors of apostrophe (Its), a comma splice and subject–verb agreement (farmers is).',
     'Model: It has been a long time since it rained; the crops are dying and the farmers are worried.'),
    ('First I will talk about the cost. Also uniforms are smart. Another thing is cost again. In conclusion uniforms.', 'W2', 'ideas are poorly organised: points repeat, there is no logical sequence and the conclusion is undeveloped.',
     'Model: begin with the strongest point (cost), develop it with evidence, then move to a second distinct point (identity), and end with a conclusion that weighs them.'),
    ('The sunset was nice and I felt good.', 'W1', 'the writer does not convey the experience, thoughts or feelings in a developed, imaginative way; ‘nice’ and ‘good’ say almost nothing.',
     'Model: The sun sank into the harbour like a coin into a well, and for the first time in weeks I felt the knot in my chest begin to loosen.'),
    ('The thing is that the thing about recycling is that it is a good thing for things like the planet.', 'W3', 'repetition of ‘thing’ shows a very limited vocabulary and a clumsy structure.',
     'Model: Recycling conserves resources and reduces the waste that pollutes the planet.'),
    ('In my speech to the governors I will be like, guys, we really need a new library.', 'W4', 'the register (be like, guys) does not suit a formal speech to school governors.',
     'Model: Members of the board, I would like to make the case today for investing in a new library.'),
    ('Despite the rain. We carried on walking, we was soaked by the time we reached the hut.', 'W5', 'a sentence fragment, a comma splice and an agreement error (we was).',
     'Model: Despite the rain, we carried on walking; we were soaked by the time we reached the hut.'),
    ('Then this happened and then that happened and then we went home and then it was the end.', 'W2', 'the narrative has no shaping: events are listed with ‘and then’, with no development, pace or deliberate effect.',
     'Model: select a key moment, slow it down with detail, and end on an image that reflects the significance of the day.'),
    ('I was scared. Very scared. Really very scared.', 'W1', 'feelings are stated rather than conveyed; the writer does not show the experience imaginatively.',
     'Model: My breath came in short, shallow gulps, and every creak of the stairs seemed to land directly on the back of my neck.'),
]
t11 = topic('Writing objectives W1–W5', 'writing objectives w1–w5', 'ideas organisation vocabulary accuracy')
t11.fixed('C1', (1, 2), [
    ('In IGCSE First Language English compositions, how are the marks divided?', 'Content and structure, and Style and accuracy', 'Compositions are marked for Content and structure (W1–W2) and Style and accuracy (W3–W5).',
     ['Reading and Speaking', 'Handwriting and length', 'Spelling only']),
    ('Which objective is mainly assessed by the overall shape and paragraphing of a piece?', 'W2', 'W2: organise and structure ideas and opinions for deliberate effect.', ['W1', 'W4', 'W5']),
    ('A student uses slang in a formal report. Which objective is most affected?', 'W4', 'W4: register appropriate to context.', ['W1', 'W2', 'W5']),
    ('Which of these best describes ‘deliberate effect’ in W2?', 'Choices of structure made on purpose to influence the reader', 'E.g. delaying a revelation, a one-line paragraph, a circular ending.', ['Writing as much as possible', 'Using the longest words available', 'Copying the structure of the source text']),
    ('Which feature most clearly shows a range of sentence structures (W3)?', 'Mixing short simple sentences with longer complex sentences for effect', 'Range = variety used purposefully.', ['Starting every sentence with ‘The’', 'Using only compound sentences', 'Writing one very long paragraph']),
])


@t11.add('C1', (1, 2, 3))
def t11_obj(r, D):
    code, desc = r.choice(WOBJ)
    opts, ans = mcq(r, code, [c for c, _ in WOBJ if c != code])
    return {'stem': f'Which writing objective requires you to {desc}?', 'options': opts, 'answer': ans, 'key': f'{code}: {desc}.'}


@t11.add('C1', (1, 2, 3))
def t11_diag(r, D):
    text, code, why, _ = r.choice(WEAK)
    opts, ans = mcq(r, code, [c for c, _ in WOBJ if c != code])
    return {'stem': f'A student writes: {Q(text)} Which writing objective is this sentence weakest on?', 'options': opts, 'answer': ans, 'key': f'{code}: {why}'}


@t11.add('C2', (1, 2, 3, 4), 'explain')
def t11_explain(r, D):
    text, code, why, _ = r.choice(WEAK)
    m = mk('C2', D)
    desc = dict(WOBJ)[code]
    return {'stem': f'Explain why this extract would score poorly on {code} ({desc}): {Q(text)}', 'answer': cap(why),
            'key': f'{upto(m)}: identifies the specific weakness; links it to {code}; suggests how it could be improved.'}


@t11.add('C3', (1, 2, 3, 4, 5), 'explain')
def t11_improve(r, D):
    text, code, why, model = r.choice(WEAK)
    m = mk('C3', D)
    return {'stem': f'Improve this extract so that it meets {code} ({dict(WOBJ)[code]}) more successfully, then explain one change you made: {Q(text)}',
            'answer': f'{model} The weakness was that {why}', 'key': f'{upto(m)}: a rewrite that clearly addresses {code}; meaning kept or developed; explanation of the improvement; no new errors.'}


W_TASKS = [
    ('Describe the moment you arrive somewhere for the first time.', 'descriptive'), ('Write a story with the title ‘The Return’.', 'narrative'),
    ('Write a story that begins: ‘Nobody had told me the house would be empty.’', 'narrative'), ('Describe a place that is busy in the morning and deserted at night.', 'descriptive'),
    ('‘Young people today have too much choice.’ Write an argument for or against this view.', 'argument'), ('Write a discursive essay on whether cities or villages offer a better life.', 'discursive'),
]


@t11.add('C4', (2, 3, 4, 5), 'long')
def t11_comp(r, D):
    stem, genre = r.choice(W_TASKS)
    tail = r.choice([' After your composition, add three brief notes explaining how you addressed W1–W2 (ideas and structure) and W3–W5 (style and accuracy).',
                     ' Plan briefly first, and make deliberate structural choices you could explain.', ''])
    ind = {'descriptive': 'vivid, focused detail; atmosphere; structure based on shifts of focus or time; no slide into narrative.',
           'narrative': 'engaging plot with a clear arc; convincing characters; deliberate pace and tension; effective ending.',
           'argument': 'clear stance; developed reasons with evidence; counter-argument rebutted; cohesive paragraphs; strong conclusion.',
           'discursive': 'both sides developed; evaluation; balanced tone; reasoned conclusion.'}[genre]
    return comp_task(D, stem + tail, genre, ind, f'Model approach: {ind}')


# ---------------------------------------------------------------- 1.2 sentence structures for effect
S_TYPES = ['simple sentence', 'compound sentence', 'complex sentence', 'compound-complex sentence', 'minor sentence', 'periodic sentence', 'tricolon (list of three)', 'parenthesis']
S_SNIP = [
    ('The door opened.', 'simple sentence', 'a single main clause gives a stark, sudden effect.'),
    ('The lights flickered, and the room fell silent.', 'compound sentence', 'two main clauses joined by ‘and’ balance two actions.'),
    ('When the lights flickered, the room fell silent.', 'complex sentence', 'the subordinate clause sets up the condition for the main event.'),
    ('When the lights flickered, the room fell silent, but nobody moved.', 'compound-complex sentence', 'a subordinate clause plus two main clauses develops a layered moment.'),
    ('Nothing. Not a sound.', 'minor sentence', 'fragments without main verbs create stillness and emphasis.'),
    ('After the long drive through the rain, after the wrong turnings and the arguments over the map, after the fuel light had glowed for twenty kilometres, we finally saw the lights of the village.', 'periodic sentence', 'the main clause is delayed until the end, building anticipation and relief.'),
    ('The city was loud, crowded and relentless.', 'tricolon (list of three)', 'three adjectives build a cumulative, rhythmic impression.'),
    ('My grandfather – who had never once raised his voice – slammed the table.', 'parenthesis', 'the inserted information heightens the shock of the action.'),
    ('She ran.', 'simple sentence', 'the brevity mirrors the sudden action.'),
    ('Although the evidence was strong, the jury hesitated, and the court waited.', 'compound-complex sentence', 'the structure holds tension across several clauses.'),
    ('Heat, dust, flies, silence.', 'minor sentence', 'a verbless list builds a harsh atmosphere quickly.'),
    ('The old harbour (now almost empty of boats) still smelled of salt and diesel.', 'parenthesis', 'the bracketed aside adds a wistful detail about change.'),
]
S_EFFECT = [
    ('The corridor stretched ahead, lined with doors that had not been opened for years, each one stamped with a faded number, each handle dull with dust. I reached for number nine. Locked.',
     'A long, cumulative sentence slows the pace and builds atmosphere; the short sentence and the one-word minor sentence ‘Locked.’ halt the reader abruptly, creating frustration and suspense.'),
    ('We waited. We waited through the morning and through the heat of the afternoon, and still the bus did not come.',
     'The short opening sentence is then repeated and expanded into a longer one, mimicking the stretching time and growing frustration.'),
    ('Because she had promised, because her mother had asked her, because there was nobody else, Amara stayed.',
     'The repeated fronted subordinate clauses build reasons before the very short main clause, emphasising duty and the weight of her decision.'),
    ('The crowd surged. Someone screamed. A child’s hand slipped from mine.', 'Three short sentences create a fast, fragmented pace that reflects panic and confusion.'),
    ('It was beautiful – it was also, I realised too late, the most dangerous place I had ever stood.', 'The dash and parenthetical ‘I realised too late’ create a twist in the middle of the sentence, shifting the tone from wonder to danger.'),
    ('Not the shouting. Not the broken glass. It was the silence afterwards that frightened me.', 'Two minor sentences dismiss expected sources of fear, building to the main clause that reveals the real one; the delay gives it impact.'),
]
FLAT = [
    ('The storm came. The wind was strong. The trees moved. The windows rattled. We were scared.',
     'Model: Without warning, the storm swept in from the sea. The wind tore at the palms until they bent double, and every window in the house rattled in its frame. We did not speak. We could not.'),
    ('I went into the exam hall. I sat down. I looked at the paper. I did not know the first answer.',
     'Model: Thirty rows of silent desks waited in the exam hall. I sat, turned the paper over with damp fingers and read the first question – once, twice, three times. Nothing.'),
    ('The market opens at six. People arrive. They set up stalls. It gets noisy.',
     'Model: At six, as the first grey light seeps over the rooftops, the traders arrive; within minutes tarpaulins snap open, crates thud onto trestles and the square erupts into a hundred bargaining voices.'),
    ('She found the letter. She read it. She cried.', 'Model: When she finally found the letter – tucked inside the cover of her father’s old atlas – she read it standing up, too afraid to sit. Then she cried.'),
    ('The city at night is quiet. The streets are empty. The lights are on.', 'Model: At night the city exhales. Streets that roared all day lie empty under the amber lights, and only a lone taxi, gliding past the shuttered shops, disturbs the silence.'),
]
t12 = topic('Varying sentence structures for effect', 'varying sentence structures for effect')
t12.fixed('C1', (1, 2), [
    ('What is a periodic sentence?', 'A sentence in which the main clause is delayed until the end', 'It builds suspense or emphasis by holding back the main point.', ['A sentence that uses a full stop', 'A sentence about time', 'A sentence with no subordinate clause']),
    ('What is the usual effect of a sequence of short sentences in a tense moment?', 'It speeds up the pace and creates tension', 'Short sentences fragment the action and increase urgency.', ['It slows the pace and relaxes the reader', 'It makes the writing more formal', 'It has no effect']),
    ('What does a compound-complex sentence contain?', 'at least two main clauses and at least one subordinate clause', 'E.g. ‘When it rained, we stayed in, but they went out.’', ['one main clause only', 'no verbs', 'only subordinate clauses']),
    ('Which technique delays information to build suspense?', 'Fronting subordinate clauses before the main clause', 'Delay makes the reader wait for the key information.', ['Using only simple sentences', 'Removing all punctuation', 'Starting with the conclusion']),
])
classify_templates(t12, S_SNIP, S_TYPES, ['Which sentence structure is used here? {q}', 'Identify the type of sentence structure in: {q}'],
                   C2frames=['This is a {label}: {q} Explain its effect.'],
                   C3frames=[('Identify the sentence structure in {q}, explain its effect, and write a sentence of your own about a storm using the same structure.',
                              lambda it: f'{cap(it[1])}: {it[2]} Own sentence: any accurate {it[1]} about a storm.', lambda it, m: f'{upto(m)}: 1 for {it[1]}; 1 for effect; remaining mark(s) for an accurate original example.')])
t12.fixed('C2', (2, 3, 4), [(f'Explain how the writer varies sentence structure for effect in: {Q(a)}', b, '1 mark: identifies the structures; 1 mark: effect on pace/tension/emphasis; a further mark for linking structure to meaning.') for a, b in S_EFFECT])
rewrite_templates(t12, [('Rewrite this passage, varying the sentence structures to create a more powerful effect.', a, b, 'Award for a deliberate range of structures (e.g. fronted clauses, periodic sentence, minor sentence) that clearly enhances effect; accurate punctuation.') for a, b in FLAT],
                  ['{ins} {q}', 'Here is a flat paragraph: {q} {ins} Then explain one choice you made.'], D=(2, 3, 4, 5))
SS_TOPICS = ['the last minutes before a storm breaks', 'a hospital waiting room at night', 'a stadium as the final whistle blows', 'a fishing village before dawn', 'a train pulling out of a station', 'an abandoned fairground']
comp_templates(t12, [(f'Write a descriptive piece about {x}, using a deliberate variety of sentence structures (including at least one periodic sentence and one minor sentence) to control pace and atmosphere.',
                      'sentence structures varied purposefully; pace controlled; atmosphere sustained; no slide into narrative.', f'Model approach: open with a long, cumulative sentence that establishes {x}; shift to short sentences at the key moment; end with a minor sentence or a periodic sentence for impact.')
                     for x in SS_TOPICS], 'descriptive')

# ---------------------------------------------------------------- 1.3 vocabulary and register
VAGUE = [
    ('The man walked down the street.', 'walked', ['strolled', 'staggered', 'marched', 'shuffled'], 'each verb suggests a different mood or condition: relaxed, injured or drunk, purposeful, old or weary.'),
    ('The food smelled good.', 'good', ['fragrant', 'smoky', 'pungent', 'sweet'], 'precise adjectives create a specific sensory impression.'),
    ('The noise was loud.', 'loud', ['deafening', 'thunderous', 'shrill', 'booming'], 'each adjective suggests a different kind of sound.'),
    ('She was happy about the result.', 'happy', ['elated', 'relieved', 'content', 'jubilant'], 'each word reflects a different degree or type of happiness.'),
    ('The building was old.', 'old', ['crumbling', 'venerable', 'dilapidated', 'ancient'], 'connotations range from decay to respect.'),
    ('He said he was not guilty.', 'said', ['insisted', 'protested', 'muttered', 'declared'], 'speech verbs reveal attitude and tone.'),
]
CONNOT = [
    ('slender', 'skinny', 'positive connotation (graceful) versus negative (underfed)'), ('confident', 'arrogant', 'positive (self-assured) versus negative (overbearing)'),
    ('thrifty', 'stingy', 'positive (careful with money) versus negative (mean)'), ('curious', 'nosy', 'positive (inquisitive) versus negative (intrusive)'),
    ('determined', 'stubborn', 'positive (persevering) versus negative (unreasonable)'), ('home', 'house', 'emotional warmth versus a neutral building'),
    ('cosy', 'cramped', 'pleasant smallness versus uncomfortable smallness'), ('youthful', 'childish', 'positive energy versus immaturity'),
]
REG_SHIFT = [
    ('a formal letter to a newspaper editor', 'Honestly, the new car park is a total joke and it’s wrecking the town centre.', 'Model: I believe the new car park is seriously damaging the character and economy of the town centre.'),
    ('a speech to a school assembly', 'Data indicates a statistically significant correlation between sleep duration and academic attainment.', 'Model: Here is something worth knowing: the more you sleep, the better you are likely to do in your exams.'),
    ('an article for a teenage magazine', 'It is recommended that adolescents engage in a minimum of sixty minutes of physical activity daily.', 'Model: Aim for at least an hour of moving about every day – dance, football, a long walk, whatever you enjoy.'),
    ('a report to the school board', 'Loads of kids reckon the canteen food is pretty rubbish these days.', 'Model: A significant proportion of students surveyed expressed dissatisfaction with the current canteen menu.'),
    ('a letter of application', 'I’m dead good with people and I’m up for anything.', 'Model: I communicate well with people of all ages and I am eager to take on new responsibilities.'),
    ('a blog post for young travellers', 'Visitors are advised to exercise caution when utilising public transport after dark.', 'Model: Heads up: take care on buses and trains late at night – stick to busy carriages and keep your bag close.'),
]
AMBITIOUS = [('very big', 'colossal'), ('very small', 'minuscule'), ('very tired', 'exhausted'), ('very angry', 'furious'), ('very cold', 'glacial'), ('very hungry', 'ravenous'), ('very old', 'ancient'), ('very quiet', 'hushed'), ('very bright', 'dazzling'), ('very sad', 'desolate')]
t13 = topic('Precise and ambitious vocabulary; register for audience', 'precise and ambitious vocabulary', 'register for audience')
t13.fixed('C1', (1, 2), [
    ('What does it mean to say vocabulary is ‘precise’?', 'Each word is chosen to convey exactly the intended meaning or effect', 'Precision beats length: ‘limped’ is more precise than ‘walked slowly’.', ['The longest possible words are used', 'Words are spelled correctly', 'The same word is repeated for clarity']),
    ('Which is the most effective replacement for ‘very scared’ in a tense narrative?', 'petrified', 'A single precise word is stronger than an intensifier + vague adjective.', ['really scared', 'scared a lot', 'very very scared']),
    ('What is the main risk of using ‘ambitious’ vocabulary without care?', 'Words may be used inaccurately or sound unnatural', 'Ambition must be matched by accuracy and suitability (W3).', ['The writing becomes too short', 'The examiner cannot read it', 'There is no risk']),
])


@t13.add('C1', (1, 2, 3))
def t13_amb(r, D):
    plain, amb = r.choice(AMBITIOUS)
    others = [a for p_, a in AMBITIOUS if a != amb]
    opts, ans = mcq(r, amb, r.sample(others, 3))
    return {'stem': f'Which single word is the most precise replacement for {Q(plain)}?', 'options': opts, 'answer': ans, 'key': f'{Q(amb)} means {plain}.'}


@t13.add('C2', (1, 2, 3, 4), 'explain')
def t13_vague(r, D):
    s, w, opts, why = r.choice(VAGUE)
    a, b = r.sample(opts, 2)
    m = mk('C2', D)
    if m == 1:
        return {'stem': f'Replace {Q(w)} in {Q(s)} with {Q(a)}. What does the new word suggest?', 'answer': f'{Q(a)} is more precise: {why}', 'key': keypts('1 mark: valid connotation of the new word.')}
    return {'stem': f'In {Q(s)}, compare the effect of replacing {Q(w)} with {Q(a)} and with {Q(b)}.', 'answer': f'Both are more precise than {Q(w)}; {why}',
            'key': f'{upto(m)}: connotation of {Q(a)}; connotation of {Q(b)}; comparison of the impressions created.'}


@t13.add('C2', (2, 3, 4), 'explain')
def t13_connot(r, D):
    a, b, why = r.choice(CONNOT)
    return {'stem': f'A writer could describe a character as {Q(a)} or as {Q(b)}. Explain how the choice affects the reader’s view of the character.', 'answer': f'The words have similar denotation but different connotations: {why}.',
            'key': keypts('1 mark: identifies the difference in connotation; 1 mark: effect on how the reader judges the character.')}


@t13.add('C3', (2, 3, 4, 5), 'short')
def t13_reg(r, D):
    aud, s, model = r.choice(REG_SHIFT)
    m = mk('C3', D)
    return {'stem': f'Rewrite this sentence so that its register suits {aud}, and explain two choices you made: {Q(s)}', 'answer': model,
            'key': f'{upto(m)}: register appropriate to {aud}; meaning kept; two explained choices (vocabulary, contractions, sentence length, address).'}


REG_PAIRS = [('a formal email to a museum asking to arrange a class visit', 'a message to classmates telling them about the visit'), ('a speech to parents about a fundraising event', 'a social-media post for students about the same event'),
             ('a report to the council on litter in a park', 'a leaflet for children encouraging them to use the bins'), ('a letter of complaint to a sports shop', 'a review of the same shop for a website read by teenagers')]


@t13.add('C4', (2, 3, 4, 5), 'long')
def t13_two(r, D):
    a, b = r.choice(REG_PAIRS)
    m = mk('C4', D, 'long', PROFILE)
    return {'stem': f'Write two short texts on the same subject: (1) {a}; (2) {b}. Then write a paragraph analysing how and why your vocabulary and register differ. Write about {WORDS10.get(D)} words in total.',
            'answer': 'Model approach: text 1 formal (full forms, polite modals, precise nouns, clear purpose and sign-off); text 2 informal and lively (direct address, contractions, colloquial but controlled language); analysis naming specific choices and linking them to audience and purpose.',
            'key': levels_key(m, ('both texts precisely judged for audience and purpose; analysis perceptive and specific', 'two recognisably different registers; analysis identifies some choices', 'register barely changes; analysis vague'),
                              'formality markers; vocabulary choice; sentence length; modes of address; purpose.', style=STYLE10), 'type': 'long'}


# ---------------------------------------------------------------- 1.4 spelling, punctuation and grammar
SPAG = [
    ('Neither of the candidates have answered the question.', 'Neither of the candidates has answered the question.', 'agreement: ‘neither’ takes a singular verb'),
    ('The committee have decided to postpone there meeting.', 'The committee has decided to postpone its meeting.', 'homophone (there/its) and collective-noun agreement (British English also accepts ‘have … their’ consistently)'),
    ('Walking into the room, the smell of smoke was overwhelming.', 'Walking into the room, I noticed that the smell of smoke was overwhelming.', 'dangling modifier: the smell was not walking'),
    ('It was late, we decided to leave.', 'It was late, so we decided to leave.', 'comma splice'),
    ('She was sat on the wall when the bus past.', 'She was sitting on the wall when the bus passed.', 'non-standard ‘was sat’; homophone past/passed'),
    ('The students books were left in the hall.', 'The students’ books were left in the hall.', 'plural possessive apostrophe'),
    ('He runs to the door, opened it and stared.', 'He ran to the door, opened it and stared.', 'tense inconsistency'),
    ('Between you and I, the plan will fail.', 'Between you and me, the plan will fail.', 'pronoun case after a preposition'),
    ('There are less people here than yesterday.', 'There are fewer people here than yesterday.', 'fewer (countable) versus less (uncountable)'),
    ('The affect of the drought was devastating.', 'The effect of the drought was devastating.', 'affect (verb) / effect (noun)'),
    ('I would of come if I had known.', 'I would have come if I had known.', '‘would of’ should be ‘would have’'),
    ('Each team must bring their own equipment, and they must arrive on time, they will be disqualified otherwise.', 'Each team must bring its own equipment and arrive on time; otherwise, it will be disqualified.', 'comma splice and pronoun consistency'),
]
SPAG_PARA = [
    ('As the train pulled into the station their was a sudden silence. Nobody moved, everyone was watching the man on the platform. He was holding a sign, it said only one word: Welcome. Who was he waiting for.',
     'As the train pulled into the station, there was a sudden silence. Nobody moved; everyone was watching the man on the platform. He was holding a sign that said only one word: Welcome. Who was he waiting for?',
     ['comma after fronted clause', 'their → there', 'comma splice → semicolon', 'comma splice → relative clause', 'question mark']),
    ('The documentary, which was filmed in the Amazon, show how deforestation effects local communities. It argues that goverments must act now.',
     'The documentary, which was filmed in the Amazon, shows how deforestation affects local communities. It argues that governments must act now.',
     ['show → shows (agreement)', 'effects → affects', 'goverments → governments']),
    ('Me and my sister was walking home when we seen the fire. We run to the nearest house, and phoned the fire brigade who arrived in minutes.',
     'My sister and I were walking home when we saw the fire. We ran to the nearest house and phoned the fire brigade, who arrived in minutes.',
     ['Me and my sister → My sister and I', 'was → were', 'seen → saw', 'run → ran', 'comma placement before relative clause']),
    ('Its often said that the citys oldest market is it’s heart. Every morning, hundreds of traders arrive, they set up there stalls before dawn.',
     'It’s often said that the city’s oldest market is its heart. Every morning, hundreds of traders arrive; they set up their stalls before dawn.',
     ['Its → It’s', 'citys → city’s', 'it’s → its', 'comma splice', 'there → their']),
]
t14 = topic('Spelling, punctuation and grammar accuracy', 'spelling punctuation and grammar accuracy')
t14.fixed('C1', (1, 2), [
    ('Which sentence is punctuated correctly?', 'The results were clear: the experiment had failed.', 'A colon after a complete clause introduces the explanation.', ['The results were clear, the experiment had failed.', 'The results, were clear the experiment had failed.', 'The results were: clear the experiment had failed.']),
    ('Which sentence uses the apostrophe correctly?', 'The children’s coats were hung by the door.', 'Irregular plural + ’s.', ['The childrens’ coats were hung by the door.', 'The childrens coats were hung by the door.', 'The children’s’ coats were hung by the door.']),
    ('Which word correctly completes the sentence: ‘The weather had little ____ on the result.’', 'effect', 'Effect is the noun; affect is usually the verb.', ['affect', 'affects', 'effects']),
    ('Which sentence keeps the tense consistent?', 'She opened the window and looked out at the rain.', 'Both verbs are in the past tense.', ['She opens the window and looked out at the rain.', 'She opened the window and looks out at the rain.', 'She opening the window and looked out at the rain.']),
])


@t14.add('C1', (1, 2, 3))
def t14_correct(r, D):
    bad, good, why = r.choice(SPAG)
    others = [b for b, g, w in SPAG if b != bad]
    opts, ans = mcq(r, good, [bad] + r.sample(others, 2))
    return {'stem': 'Which of these sentences is grammatically correct and accurately punctuated?', 'options': opts, 'answer': ans, 'key': f'{Q(good)} is correct; the original error was {why}.'}


@t14.add('C2', (1, 2, 3, 4), 'explain')
def t14_explain(r, D):
    bad, good, why = r.choice(SPAG)
    m = mk('C2', D)
    return {'stem': f'Identify and explain the error in this sentence, then correct it: {Q(bad)}', 'answer': f'Error: {why}. Corrected: {Q(good)}', 'key': f'{upto(m)}: names the error; explains the rule; gives a correct version.'}


@t14.add('C3', (2, 3, 4, 5), 'short')
def t14_para(r, D):
    bad, good, errs = r.choice(SPAG_PARA)
    m = mk('C3', D)
    return {'stem': f'Proofread this paragraph and rewrite it with all errors corrected: {Q(bad)}', 'answer': f'Model: {Q(good)}', 'key': f'{upto(m)}: ' + '; '.join(errs) + '. Deduct for new errors.'}


@t14.add('C4', (2, 3, 4, 5), 'multi_step')
def t14_c4(r, D):
    bad, good, errs = r.choice(SPAG_PARA)
    s1, s2 = r.sample(SPAG, 2)
    parts = [
        lambda r: (f'Proofread and correct this paragraph: {Q(bad)}', f'{Q(good)}', f'1 mark per error corrected, up to {min(5, len(errs))}: ' + '; '.join(errs) + f' [{min(5, len(errs))}]'),
        lambda r: (f'Explain the rule broken in {Q(s1[0])}.', s1[2], '1 mark rule; 1 mark correction [2]'),
        lambda r: (f'Correct {Q(s2[0])} and explain why your version is correct.', f'{Q(s2[1])} – {s2[2]}', '1 mark correction; 1 mark explanation [2]'),
        lambda r: ('Write two sentences of your own about a journey: one using a semicolon correctly and one using a colon correctly.', 'Any two accurate sentences, e.g. ‘The road was flooded; we turned back.’ / ‘We had one hope left: the night bus.’', '1 mark each [2]'),
        lambda r: ('Explain why accurate punctuation matters for the reader, with one example of how a comma can change meaning.', 'Punctuation controls meaning and clarity, e.g. ‘Let’s eat, Grandma’ versus ‘Let’s eat Grandma’.', '1 mark reason; 1 mark example [2]'),
    ]
    return compose(r, 'Answer the following questions on accuracy (W5).', parts, k=(3, 4, 5), type_='multi_step')


# ---------------------------------------------------------------- 1.5 planning, paragraphing and cohesion
COHESION = [
    ('Many coastal towns depend on fishing. ____, overfishing threatens their future.', 'However', ['Similarly', 'Therefore', 'For instance'], 'contrast'),
    ('The policy saved money. ____, it reduced waiting times.', 'Moreover', ['Nevertheless', 'Conversely', 'In contrast'], 'addition'),
    ('Fuel prices rose sharply. ____, fewer people drove to work.', 'Consequently', ['Admittedly', 'Likewise', 'Meanwhile'], 'consequence'),
    ('____ the evidence is incomplete, it strongly suggests a link.', 'Although', ['Because', 'Therefore', 'Moreover'], 'concession'),
    ('Some cities have banned cars from their centres. Oslo, ____, has removed most parking spaces.', 'for example', ['however', 'consequently', 'nevertheless'], 'exemplification'),
    ('Critics argue the scheme is costly. ____, the long-term savings are substantial.', 'Nevertheless', ['Furthermore', 'Similarly', 'For example'], 'rebuttal/contrast'),
    ('____, the arguments for change outweigh those against it.', 'On balance', ['For instance', 'Firstly', 'Meanwhile'], 'evaluation/conclusion'),
    ('The first plan was rejected. ____, a second plan was drawn up.', 'Subsequently', ['Conversely', 'Admittedly', 'Likewise'], 'time sequence'),
]
REF_CHAINS = [
    ('The council announced a new recycling scheme. This initiative will begin in June.', '‘This initiative’ refers back to ‘a new recycling scheme’, linking the sentences without repetition.'),
    ('Many students struggle with sleep. Such problems often affect concentration.', '‘Such problems’ summarises the previous idea and links it to its consequences.'),
    ('Engineers proposed a bridge; residents preferred a tunnel. The latter would cost twice as much.', '‘The latter’ refers precisely to the tunnel, avoiding repetition.'),
    ('The first argument concerns cost. The second, and perhaps more important, concerns safety.', 'Ordinal signposts and ellipsis (‘The second [argument]’) guide the reader through the structure.'),
    ('Rainforests regulate the climate. They also shelter millions of species. Protecting them is therefore essential.', 'The pronouns ‘They’ and ‘them’ maintain the topic, and ‘therefore’ signals the conclusion.'),
]
PARA_PLANS = [
    ('a descriptive composition about a harbour from dawn to night', ['dawn: stillness and first light', 'morning: boats leaving and noise building', 'midday: heat and emptiness', 'evening: return of the boats', 'night: lights on water, quiet'], 'chronological shifts in time'),
    ('an argumentative essay on banning cars from city centres', ['introduction and stance', 'strongest reason: air quality, with evidence', 'second reason: safety and space', 'counter-argument (businesses) and rebuttal', 'conclusion and call to action'], 'logical argument with rebuttal before the conclusion'),
    ('a narrative about getting lost in a forest', ['opening in medias res: realising the path has gone', 'flashback: the decision to leave the group', 'rising tension: night approaching', 'climax: a sound in the trees', 'resolution: rescue and reflection'], 'in medias res with flashback and rising tension'),
    ('a discursive essay on school uniforms', ['introduction: the debate', 'arguments for: equality and identity', 'arguments against: cost and self-expression', 'evaluation: compromise options', 'conclusion: reasoned judgement'], 'balanced structure leading to evaluation'),
]
t15 = topic('Planning, paragraphing and cohesion', 'planning paragraphing and cohesion', 'extended writing')
t15.fixed('C1', (1, 2), [
    ('What is cohesion in writing?', 'The way sentences and paragraphs are linked so that the text flows logically', 'Created by connectives, reference words, repetition and topic sentences.', ['The number of paragraphs', 'Using only short sentences', 'Correct spelling']),
    ('What is a topic sentence?', 'A sentence that states the main idea of a paragraph', 'Usually first; it guides the reader.', ['The final sentence of an essay', 'A sentence with a quotation', 'A sentence that asks a question']),
    ('Why might a writer use a one-sentence paragraph?', 'To give a key moment or idea dramatic emphasis', 'A deliberate structural choice (W2).', ['Because they ran out of time', 'To avoid using full stops', 'To make the essay longer']),
    ('Which is the best use of planning time in an exam composition?', 'A short plan of paragraph topics and the ending, made before writing', 'Brief plans improve structure without wasting time.', ['Writing a full draft twice', 'Skipping the plan to write more', 'Copying the question several times']),
])


@t15.add('C1', (1, 2, 3))
def t15_gap(r, D):
    s, a, ds, fn = r.choice(COHESION)
    opts, ans = mcq(r, a, ds)
    return {'stem': f'Choose the discourse marker that best completes: {Q(s)}', 'options': opts, 'answer': ans, 'key': f'‘{a}’ signals {fn}.'}


t15.fixed('C2', (2, 3), [(f'Explain how cohesion is achieved in: {Q(a)}', b, '1 mark: identifies the cohesive device; 1 mark: explains how it links ideas.') for a, b in REF_CHAINS])


@t15.add('C3', (2, 3, 4, 5), 'short')
def t15_order(r, D):
    task, paras, why = r.choice(PARA_PLANS)
    idx = list(range(5))
    while idx == sorted(idx):
        r.shuffle(idx)
    L = 'ABCDE'
    m = mk('C3', D)
    jumble = ' '.join(f'{L[j]}: {paras[k]}' for j, k in enumerate(idx))
    order = ''.join(L[idx.index(k)] for k in range(5))
    return {'stem': f'These paragraph topics for {task} are jumbled. {jumble} Put them in the most effective order and explain the structural principle you used.',
            'answer': f'{order} – {why}.', 'key': f'{upto(m)}: correct or justifiable order ({order}); explanation of the structural principle ({why}); comment on the effect of the opening and ending.'}


@t15.add('C4', (2, 3, 4, 5), 'long')
def t15_plan(r, D):
    stem, genre = r.choice(W_TASKS)
    m = mk('C4', D, 'long', PROFILE)
    return {'stem': f'Composition task: {stem} Write a paragraph plan (one line per paragraph), then write the composition. Use topic sentences and a range of cohesive devices, and make at least one deliberate structural choice. Write about {WORDS10.get(D)} words.',
            'answer': 'Model approach: a 4–6 paragraph plan; paragraphs linked by discourse markers and reference chains; a deliberate structural choice (e.g. one-line paragraph, circular ending, delayed revelation).',
            'key': comp_key(m, genre, 'plan followed; paragraphing logical and purposeful; cohesive devices varied; structural choice deliberate.')}


CHAPTERS[1] = [t11, t12, t13, t14, t15]


# =========================================================== 2 Directed writing (Paper 2 Section A)

class Pair:
    """Two original source texts on one issue, with points, weaknesses and directed tasks."""

    def __init__(self, issue, A, B, tasks):
        self.issue = issue
        self.A, self.B = A, B      # dicts: label, text, points [..], weak [(claim, weakness)], view
        self.tasks = tasks         # (task stem, form, audience)


PAIRS = [
    Pair('replacing school textbooks with tablets',
         dict(label='Text A, a blog post by a secondary-school teacher, ‘Why I Swapped Paper for Pixels’', view='strongly in favour of tablets', text="""
Last year my class swapped printed textbooks for tablets, and I will never go back. A single tablet holds every book a
student needs, so no more aching backs from overloaded bags. Digital texts are updated instantly, while our old
geography books still described a country that changed its name a decade ago. Interactive diagrams and videos bring
difficult ideas to life, and students who struggle can listen to texts read aloud. Of course, screens can distract, but
that is a matter of teaching discipline, not a reason to stay in the past. Every student in my class now reads more.
The future of learning is digital; schools that refuse to accept this are failing their students.""",
              points=['lighter bags/health', 'up-to-date content', 'interactive diagrams and videos', 'accessibility (texts read aloud)', 'students read more'],
              weak=[('Every student in my class now reads more.', 'an unsupported generalisation based on one class, with no evidence of how reading was measured'),
                    ('schools that refuse to accept this are failing their students', 'an exaggerated claim that presents a false choice between tablets and failure'),
                    ('that is a matter of teaching discipline, not a reason to stay in the past', 'dismisses a serious concern (distraction) without evidence')]),
         dict(label='Text B, a newspaper article by an education researcher, ‘The Case for the Printed Page’', view='cautious and largely against', text="""
Before schools rush to replace books with tablets, they should look at the evidence. Several studies suggest that
students remember more of what they read on paper than on screen, particularly for long, complex texts. Tablets are
expensive to buy, insure and repair, and a broken screen can leave a student without any books at all. Many families
cannot afford reliable internet at home, so 'digital homework' widens the gap between rich and poor. Teachers also
report that notifications and games compete constantly for attention. This is not an argument against technology,
which has real value for research and accessibility. It is an argument for balance: keep printed books at the heart of
learning and use tablets where they genuinely help.""",
              points=['better recall on paper for long texts', 'cost of buying/insuring/repairing', 'broken screen = no books', 'internet access inequality', 'distraction from notifications', 'balance: use tablets where they help'],
              weak=[('Several studies suggest that students remember more of what they read on paper', 'the studies are not named or quantified, so the reader cannot judge them'),
                    ('Teachers also report that notifications and games compete constantly for attention', 'anecdotal reports; ‘constantly’ may exaggerate')]),
         [('Write a letter to your headteacher, who is deciding whether to replace all textbooks with tablets next year. Evaluate the views in both texts and give your own recommendation.', 'letter', 'your headteacher'),
          ('Write a speech for a debate at your school on the motion ‘Tablets should replace textbooks’. Evaluate the ideas in both texts and argue your own view.', 'speech', 'students and teachers at a school debate'),
          ('Write an article for your school magazine evaluating the arguments in both texts about tablets and printed books.', 'article', 'readers of a school magazine')]),
    Pair('tourism on a small island',
         dict(label='Text A, an article from the island’s tourism board, ‘Open Arms, Open Island’', view='strongly in favour of more tourism', text="""
Tourism is the lifeblood of our island. Last year more than 200,000 visitors brought in money that paid for a new
clinic, resurfaced roads and kept our schools open. Over a third of islanders now work in hotels, restaurants, boat
tours and craft shops, and young people no longer have to leave to find work. Visitors fall in love with our beaches,
our food and our festivals, and many return year after year. A new cruise terminal would allow us to welcome twice as
many guests. Some worry about crowds, but with good planning there is room for everyone. If we close our doors, others
will open theirs, and our children will pay the price.""",
              points=['income paid for clinic, roads, schools', 'jobs for over a third of islanders', 'young people can stay', 'visitors return and value culture', 'cruise terminal could double visitors'],
              weak=[('with good planning there is room for everyone', 'a vague reassurance that gives no detail of the planning'),
                    ('If we close our doors, others will open theirs, and our children will pay the price.', 'emotive scare tactic and false choice between expansion and closing doors')]),
         dict(label='Text B, a letter to a newspaper from a long-time island resident', view='opposed to further expansion', text="""
Sir, I have lived on this island for sixty years, and I no longer recognise it. In summer, cruise ships unload thousands
of passengers into a harbour built for fishing boats. Rents have tripled as houses become holiday lets, and my
granddaughter, a nurse, cannot afford to live in the village where she grew up. The coral reef our grandparents fished
is bleached and broken by careless snorkellers and boat anchors. Yes, tourism brings money, but much of it flows to
hotel companies based abroad. A second cruise terminal would turn our home into a theme park. We need fewer, better
visitors who respect the island, not more of them. Yours faithfully, Mrs R. Fonseca""",
              points=['overcrowded harbour', 'rents tripled; locals priced out', 'damage to coral reef', 'profits go abroad', 'want fewer, better visitors'],
              weak=[('Rents have tripled as houses become holiday lets', 'a striking figure with no source given'),
                    ('A second cruise terminal would turn our home into a theme park.', 'emotive hyperbole rather than evidence')]),
         [('Write a speech to be given at a public meeting on the island, where residents will vote on whether to build a second cruise terminal. Evaluate the views in both texts and give your own opinion.', 'speech', 'island residents at a public meeting'),
          ('Write a letter to the island council evaluating the arguments in both texts and recommending what the council should do about tourism.', 'letter', 'the island council'),
          ('Write an article for a travel magazine evaluating the effects of tourism on the island, using ideas from both texts.', 'article', 'readers of a travel magazine')]),
    Pair('the role of zoos today',
         dict(label='Text A, a speech by the director of a city zoo', view='in favour of modern zoos', text="""
Good evening. Modern zoos are not the prisons of the past. Our animals live in large, carefully designed habitats, and
every species has a care plan written by vets and behaviour experts. More importantly, zoos are arks. Our breeding
programme has returned more than fifty endangered tortoises to the wild, and we fund conservation rangers in three
countries. Every year, 400,000 visitors, half of them children, see living animals up close, and many tell us it is
the moment they began to care about nature. A documentary cannot do that. Close the zoos, and we close the door on the
next generation of conservationists.""",
              points=['large designed habitats', 'expert care plans', 'breeding programmes return animals to the wild', 'fund rangers abroad', 'education and inspiring children'],
              weak=[('many tell us it is the moment they began to care about nature', 'anecdotal evidence from visitors chosen by the zoo'),
                    ('Close the zoos, and we close the door on the next generation of conservationists.', 'a sweeping prediction presented as certain')]),
         dict(label='Text B, an article by an animal-welfare campaigner, ‘Bigger Cages Are Still Cages’', view='against keeping most animals in zoos', text="""
However well designed, an enclosure is a tiny fraction of an animal's natural range. Elephants walk many kilometres a
day in the wild; in captivity, many develop repetitive swaying and pacing, signs of stress that keepers call
'stereotypic behaviour'. Only a small proportion of species kept in zoos are part of programmes that return animals to
the wild; most are there because visitors like to see them. Conservation money is vital, but it could be raised and
spent directly protecting habitats, where it does the most good. If zoos truly exist for conservation, they should
keep only the species that need them, in sanctuaries designed around the animals rather than the visitors.""",
              points=['enclosures far smaller than natural range', 'stress behaviours (swaying, pacing)', 'few species in release programmes', 'money better spent protecting habitats', 'keep only species that need it, in sanctuaries'],
              weak=[('Only a small proportion of species kept in zoos are part of programmes that return animals to the wild', 'no figure is given, so the claim is hard to check'),
                    ('most are there because visitors like to see them', 'an assertion about motive with no evidence')]),
         [('Write a letter to your local newspaper responding to both texts and giving your view on whether the city zoo should be expanded.', 'letter', 'readers of a local newspaper'),
          ('Write a speech for a school debate on the motion ‘Zoos do more harm than good’, evaluating the arguments in both texts.', 'speech', 'a school debate audience'),
          ('Write an article for a wildlife magazine evaluating the arguments for and against zoos presented in the two texts.', 'article', 'readers of a wildlife magazine')]),
    Pair('teenagers having part-time jobs',
         dict(label='Text A, advice from a careers adviser, ‘Your First Job Is Your Best Teacher’', view='strongly in favour', text="""
A Saturday job teaches lessons no classroom can. You learn to arrive on time, deal politely with difficult customers
and work as part of a team. Employers tell me that applicants with work experience stand out immediately. Earning your
own money also teaches you its value: you think twice about spending forty hours' wages on a pair of trainers. Most
students can easily manage eight hours a week without their studies suffering, and many find that a busy schedule
actually makes them more organised. Start small, choose something you enjoy, and you will gain confidence that lasts a
lifetime.""",
              points=['punctuality, customer skills, teamwork', 'employers value experience', 'learn the value of money', 'eight hours manageable', 'busy schedule improves organisation', 'confidence'],
              weak=[('Most students can easily manage eight hours a week without their studies suffering', 'a generalisation that ignores differences in workload and circumstances'),
                    ('Employers tell me that applicants with work experience stand out immediately', 'second-hand, anecdotal evidence')]),
         dict(label='Text B, a blog post by a sixteen-year-old student, ‘Too Tired to Learn’', view='critical, from personal experience', text="""
I took a job in a café last September because everyone said it would look good on my CV. By November I was working
fourteen hours a week, closing at ten on school nights because they were short-staffed and I didn't feel I could say
no. My grades dropped in every subject. I was too tired to concentrate, and I stopped going to football. Some of my
friends cope fine, and the money was useful, but nobody warned me how hard it is to set limits when your manager is an
adult and you are not. If you take a job, agree your hours in writing and protect your sleep. I wish I had.""",
              points=['hours crept up (8 to 14)', 'late closing on school nights', 'grades dropped; too tired', 'gave up hobbies', 'hard for teenagers to set limits', 'advice: agree hours in writing, protect sleep'],
              weak=[('My grades dropped in every subject.', 'a single personal case that may not represent others'),
                    ('Some of my friends cope fine', 'acknowledges that her experience may not be typical, which weakens a general conclusion')]),
         [('Write a letter to the parents of students in your year, evaluating the views in both texts and advising them about part-time jobs.', 'letter', 'parents of students'),
          ('Write a speech to be given at a school assembly about whether students should take part-time jobs, evaluating both texts.', 'speech', 'students at a school assembly'),
          ('Write an article for a teenage magazine evaluating the advice in both texts and giving your own guidance.', 'article', 'readers of a teenage magazine')]),
    Pair('building protected cycle lanes in a city centre',
         dict(label='Text A, a press release from the city council, ‘Safer Streets for Everyone’', view='in favour of the scheme', text="""
From next spring, the city will open twelve kilometres of protected cycle lanes linking the station, the university and
the market. In cities that have built similar networks, cycling has often doubled within five years. Fewer cars mean
cleaner air: road transport currently produces more than half of the city's air pollution. The lanes will be separated
from traffic by kerbs, making them safe enough for children and older riders. Businesses will benefit too, as people
on bikes stop more often and shop locally. The scheme is funded by a national grant and will not raise local taxes.""",
              points=['12 km linking key places', 'cycling doubled elsewhere', 'cleaner air (road transport > half of pollution)', 'kerb-separated lanes are safe', 'cyclists shop locally', 'funded by national grant'],
              weak=[('In cities that have built similar networks, cycling has often doubled within five years', '‘often’ and unnamed cities make the evidence vague'),
                    ('Businesses will benefit too, as people on bikes stop more often and shop locally', 'a prediction stated as certainty with no local evidence')]),
         dict(label='Text B, a letter from a market trader to the local newspaper', view='opposed', text="""
The council's cycle lanes will remove sixty parking spaces from Market Street. My customers are not students on bicycles;
they are families buying a week's vegetables and older people who cannot carry heavy bags on a bus. When the council
closed Bridge Road for repairs last year, my takings fell by a third in a month. I am not against cycling, and cleaner
air is welcome, but nobody asked the traders. A lane on the quieter parallel street would give cyclists a safe route
without cutting off the market from the people who keep it alive.""",
              points=['loss of sixty parking spaces', 'customers need cars for heavy shopping', 'takings fell by a third during road closure', 'traders not consulted', 'alternative route on parallel street'],
              weak=[('When the council closed Bridge Road for repairs last year, my takings fell by a third in a month.', 'one trader’s experience during a different situation (a full road closure)'),
                    ('My customers are not students on bicycles', 'a generalisation that may not reflect all customers')]),
         [('Write a speech to be given at a council meeting where the cycle-lane plan will be discussed. Evaluate both texts and propose what the council should do.', 'speech', 'councillors and residents'),
          ('Write a letter to the city council evaluating the arguments in both texts and giving your view on the cycle-lane scheme.', 'letter', 'the city council'),
          ('Write an article for a local news website evaluating the cycle-lane debate, using ideas from both texts.', 'article', 'readers of a local news website')]),
    Pair('spending public money on space exploration',
         dict(label='Text A, an article by a planetary scientist, ‘Why We Must Keep Looking Up’', view='strongly in favour', text="""
Space exploration is not a luxury; it is an investment. Satellites developed for space now forecast storms, guide
farmers and connect remote villages to the internet. Research for space missions has helped improve water-purification
methods and medical imaging. Studying other planets helps us understand climate change on our own. And exploration
inspires: countless young people choose to study science because of a rocket launch or a photograph of Earth from
space. The cost sounds enormous, but space agencies usually receive well under one per cent of national budgets.
Abandoning space would save little and cost us our future.""",
              points=['satellites for weather, farming, internet', 'spin-offs (water purification, medical imaging)', 'helps understand climate change', 'inspires young scientists', 'small share of national budgets'],
              weak=[('countless young people choose to study science because of a rocket launch', '‘countless’ is vague and the link is not evidenced'),
                    ('Abandoning space would save little and cost us our future.', 'an exaggerated conclusion presented as fact')]),
         dict(label='Text B, an opinion column, ‘Fix the Earth First’', view='against high spending on space', text="""
While billions are spent sending robots to Mars, millions of people on Earth lack clean water. That is not a choice I
can defend. Supporters of space programmes point to useful inventions, but many of those could have been developed
more cheaply by funding the research directly. Private companies are now racing to launch rockets, so governments need
not compete with them. If we want to inspire young people, let them see us solve the climate crisis, end hunger and
rebuild crumbling schools. Mars will still be there in fifty years; the communities flooded by rising seas may not be.""",
              points=['money could provide clean water', 'inventions could be funded directly', 'private companies can take over', 'inspiration from solving Earth’s problems', 'urgency of climate crisis'],
              weak=[('many of those could have been developed more cheaply by funding the research directly', 'a hypothetical claim with no evidence'),
                    ('That is not a choice I can defend.', 'presents a false choice: space spending versus clean water')]),
         [('Write a letter to a government minister evaluating the arguments in both texts and giving your view on whether funding for space exploration should be increased.', 'letter', 'a government minister'),
          ('Write a speech for a youth parliament debate on whether governments should spend money on space exploration, evaluating both texts.', 'speech', 'members of a youth parliament'),
          ('Write an article for a science magazine for young people evaluating the arguments in both texts.', 'article', 'young readers of a science magazine')]),
]
for _p in PAIRS:
    for _d in (_p.A, _p.B):
        _d['text'] = clean(_d['text'])
        for _c, _w in _d['weak']:
            assert _c.replace("'", "'") in _d['text'], _c

FORM_CONV = {
    'letter': 'appropriate greeting (Dear …), purpose stated in the opening, formal register, paragraphs, polite sign-off (Yours faithfully/sincerely)',
    'speech': 'greeting to the audience, direct address, rhetorical devices, signposting for listeners, memorable ending with thanks or a call to action',
    'article': 'headline and possibly a strapline, engaging opening, clear angle, paragraphs developing the argument, effective conclusion',
}

# ---------------------------------------------------------------- 2.1 reading and evaluating two texts
t21 = topic('Reading and evaluating ideas from two texts', 'reading and evaluating ideas from two texts')


@t21.add('C1', (1, 2, 3))
def t21_ret(r, D):
    P = r.choice(PAIRS)
    side = r.choice(['A', 'B'])
    d = P.A if side == 'A' else P.B
    other = P.B if side == 'A' else P.A
    pt = r.choice(d['points'])
    opts, ans = mcq(r, pt, r.sample(other['points'], 3))
    return {'stem': f'Read {d["label"]}: {Q(d["text"])} Which of these points is made in Text {side}?', 'options': opts, 'answer': ans,
            'key': f'Text {side} makes the point: {pt}. The other options come from the other text on {P.issue}.'}


@t21.add('C1', (1, 2, 3))
def t21_view(r, D):
    P = r.choice(PAIRS)
    side = r.choice(['A', 'B'])
    d = P.A if side == 'A' else P.B
    views = ['strongly in favour', 'cautious and largely against', 'opposed', 'neutral, with no opinion', 'critical, from personal experience', 'in favour, but only for private companies']
    opts, ans = mcq(r, d['view'], [v for v in views if v != d['view'] and not (d['view'].split()[0] == v.split()[0])])
    return {'stem': f'Read {d["label"]}: {Q(d["text"])} Which best describes the writer’s attitude to {P.issue}?', 'options': opts, 'answer': ans, 'key': f'The writer is {d["view"]}.'}


@t21.add('C2', (1, 2, 3, 4), 'explain')
def t21_weak(r, D):
    P = r.choice(PAIRS)
    d = r.choice([P.A, P.B])
    claim, why = r.choice(d['weak'])
    m = mk('C2', D)
    return {'stem': f'In {d["label"].split(", ", 1)[1]}, the writer states: {Q(claim)} Explain why a reader might question this claim.', 'answer': cap(why) + '.',
            'key': f'{upto(m)}: identifies the weakness (generalisation, lack of evidence, exaggeration, false choice); explains why it reduces the claim’s reliability; may suggest what evidence is needed.'}


@t21.add('C3', (2, 3, 4, 5), 'explain')
def t21_eval(r, D):
    P = r.choice(PAIRS)
    side = r.choice(['A', 'B'])
    d = P.A if side == 'A' else P.B
    n = 2 if D <= 3 else 3
    m = mk('C3', D)
    return {'stem': f'Read {d["label"]}: {Q(d["text"])} Identify {n} ideas the writer uses to support their view on {P.issue}, and evaluate how convincing each is.',
            'answer': 'Ideas: ' + '; '.join(d['points'][:n + 1]) + '. Evaluation: ' + '; '.join(f'{Q(c)} – {w}' for c, w in d['weak']),
            'key': f'{upto(m)}: 1 per relevant idea; further marks for evaluation (quality of evidence, generalisation, bias, omission) rather than simple agreement.'}


@t21.add('C3', (2, 3, 4, 5), 'explain')
def t21_compare(r, D):
    P = r.choice(PAIRS)
    m = mk('C3', D)
    ka, kb = r.choice(P.A['points']), r.choice(P.B['points'])
    return {'stem': f'Text A on {P.issue} argues: {Q(ka)}. Text B argues: {Q(kb)}. Text A: {Q(P.A["text"])} Text B: {Q(P.B["text"])} Which point do you find more convincing, and why? Refer to the evidence in both texts.',
            'answer': f'Either view may be argued if supported: weigh the evidence offered for each (Text A is {P.A["view"]}; Text B is {P.B["view"]}). Weaknesses: ' + '; '.join(w for _, w in P.A['weak'] + P.B['weak']),
            'key': f'{upto(m)}: clear judgement; evidence from both texts; evaluation of the quality of evidence; recognition of bias or perspective.'}


@t21.add('C4', (2, 3, 4, 5), 'multi_step')
def t21_c4(r, D):
    P = r.choice(PAIRS)
    parts = [
        lambda r: (f'List three reasons Text A gives in support of its view on {P.issue}.', '; '.join(P.A['points'][:3]), '1 mark per reason [3]'),
        lambda r: ('List three concerns or arguments raised in Text B.', '; '.join(P.B['points'][:3]), '1 mark per point [3]'),
        lambda r: (f'Choose one claim from Text A and explain why it may be unreliable.', '; '.join(f'{Q(c)}: {w}' for c, w in P.A['weak']), '1 mark claim; 2 marks evaluation [3]'),
        lambda r: (f'Choose one claim from Text B and explain why it may be unreliable.', '; '.join(f'{Q(c)}: {w}' for c, w in P.B['weak']), '1 mark claim; 2 marks evaluation [3]'),
        lambda r: (f'Which text presents the stronger case overall? Give your own judgement with reasons.', f'Any reasoned judgement weighing evidence from both (A: {P.A["view"]}; B: {P.B["view"]}).', 'Level-marked: top (5–6) balanced, evaluative, evidence from both; middle (3–4) some evaluation; lower (1–2) assertion. [6]'),
    ]
    return compose(r, f'Read the two texts about {P.issue}. Text A: {Q(P.A["text"])} Text B: {Q(P.B["text"])}', parts, k=(2, 3, 4), type_='multi_step')


# ---------------------------------------------------------------- 2.2 writing an argument, speech or letter from sources
t22 = topic('Writing an argument, speech or letter from source material', 'writing an argument speech or letter from source material')


DW_ROLES = ['You are a student representative on your school council.', 'You are the parent of two teenagers.', 'You are a member of a local youth group.',
            'You are a journalist who has read both texts.', 'You are a resident who has followed the debate closely.', 'You are a teacher with strong views on the issue.']
DW_BULLETS = ['evaluate the strongest argument in each text', 'identify and challenge any weak or one-sided evidence', 'explain which ideas you agree with and why',
              'suggest a practical compromise or solution', 'consider who would be most affected by the decision', 'end with a clear recommendation of your own',
              'compare the reliability of the two writers', 'respond to the most emotive claims calmly and logically']


def directed_item(r, D, P, task, form, aud, extra=''):
    m = mk('C4', D, 'long', PROFILE)
    role = r.choice(DW_ROLES)
    bl = r.sample(DW_BULLETS, 3)
    stem = (f'Text A: {Q(P.A["text"])} Text B: {Q(P.B["text"])} {role} {task} {extra}In your {form} you should: {bl[0]}; {bl[1]}; {bl[2]}. '
            'Base your answer on what you have read in both texts, but use your own words. Write about 250–350 words.')
    reading = 'Text A – ' + '; '.join(P.A['points']) + '. Text B – ' + '; '.join(P.B['points']) + '. Evaluation – ' + '; '.join(w for _, w in P.A['weak'] + P.B['weak']) + '.'
    writing = f'{FORM_CONV[form]}; register suited to {aud}.'
    model = (f'Model approach: open in role ({form} to {aud}); summarise the issue; evaluate Text A’s strongest points and weaknesses, then Text B’s; '
             f'weigh them and give a clear, reasoned judgement of your own; close with a recommendation. Conventions: {FORM_CONV[form]}.')
    return {'stem': stem, 'answer': model, 'key': directed_key(m, reading, writing), 'type': 'long'}


@t22.add('C4', (2, 3, 4, 5), 'long')
def t22_task(r, D):
    P = r.choice(PAIRS)
    task, form, aud = r.choice(P.tasks)
    return directed_item(r, D, P, task, form, aud)


@t22.add('C3', (2, 3, 4, 5), 'short')
def t22_plan(r, D):
    P = r.choice(PAIRS)
    task, form, aud = r.choice(P.tasks)
    m = mk('C3', D)
    return {'stem': f'Directed writing task on {P.issue}: {task} Without writing the full answer, write a paragraph-by-paragraph plan that shows which ideas from each text you will use and evaluate.',
            'answer': f'Model plan: (1) opening in role, purpose; (2) strongest points of Text A ({", ".join(P.A["points"][:2])}) with evaluation; (3) Text B’s counter-points ({", ".join(P.B["points"][:2])}) with evaluation; (4) weighing and own judgement; (5) recommendation and sign-off.',
            'key': f'{upto(m)}: ideas from both texts; evaluation planned, not just listing; logical structure; form conventions of a {form}; own judgement included.'}


@t22.add('C3', (2, 3, 4, 5), 'short')
def t22_para(r, D):
    P = r.choice(PAIRS)
    d = r.choice([P.A, P.B])
    claim, why = r.choice(d['weak'])
    task, form, aud = r.choice(P.tasks)
    m = mk('C3', D)
    return {'stem': f'You are writing a {form} to {aud} about {P.issue}. Write one paragraph that refers to this claim from {d["label"].split(",")[0]}, {Q(claim)}, and evaluates it in your own words.',
            'answer': f'Model: the paragraph acknowledges the claim, then evaluates it ({why}), and links to the writer’s own view in an appropriate {form} register.',
            'key': f'{upto(m)}: claim conveyed in own words; evaluation ({why}); register suited to {aud}; link to the overall argument.'}


@t22.add('C2', (2, 3, 4), 'explain')
def t22_why(r, D):
    P = r.choice(PAIRS)
    return {'stem': f'In a directed writing task on {P.issue}, a student simply lists the points from Text A and then the points from Text B. Explain why this would not reach the higher mark bands for Reading, and how the answer could be improved.',
            'answer': 'Higher bands reward evaluation and a developed personal judgement, not reproduction. The student should integrate ideas, question the evidence (e.g. ' + P.A['weak'][0][1] + ') and weigh the texts against each other to reach their own view.',
            'key': keypts('1 mark: listing is reproduction, not evaluation; 1 mark: need to integrate and judge; a further mark for a specific improvement linked to the texts.')}


# ---------------------------------------------------------------- 2.3 form, voice and register
def an(w):
    return ('an ' if w[:1].lower() in 'aeiou' else 'a ') + w


OPENINGS_FORM = [
    ('letter', 'Dear Councillor Mensah, I am writing on behalf of the students of Hilltop School to urge you to reconsider the closure of the youth centre.', 'formal greeting with title and name; purpose stated in the first sentence; formal register'),
    ('speech', 'Good evening, everyone. Look around this hall. Every one of you has, at some point, needed somewhere safe to go.', 'greeting to audience; direct address; imperative; inclusive tone for listeners'),
    ('article', 'Lights Out for the Youth Centre? Behind a peeling blue door on Station Road, thirty teenagers are learning to code, cook and argue.', 'headline as a question; vivid present-tense opening scene to hook readers'),
    ('report', 'This report summarises the findings of a survey of 200 students about the proposed closure of the youth centre and makes three recommendations.', 'impersonal, formal register; clear statement of scope and purpose'),
    ('letter', 'Dear Sir or Madam, I wish to complain about the cancellation of the 7.15 bus service, which has left many students unable to reach school on time.', 'formal greeting for an unknown recipient; complaint stated precisely'),
    ('speech', 'Friends, classmates, teachers – thank you for being here. I want to talk about something we all take for granted: time.', 'tricolon of address; gratitude; signposted topic; spoken rhythm'),
]
FORMS = ['letter', 'speech', 'article', 'report']
SWAP = [
    ('So what can we do? Quite a lot, actually.', 'speech', 'letter', 'Model: I would like to suggest several practical measures that the council could take.'),
    ('The survey found that 64% of respondents supported a later start.', 'report', 'speech', 'Model: Think about this: almost two thirds of you – sixty-four per cent – told us you want a later start. That is not a minority. That is most of this room.'),
    ('Dear Editor, I write to express my concern about the noise from the new factory.', 'letter', 'article', 'Model: Factory Noise Drives Residents to Despair – For the families of Mill Lane, the night shift now begins at 2 a.m., whether they work there or not.'),
    ('Ladies and gentlemen, I ask you tonight to imagine a city without parks.', 'speech', 'report', 'Model: This report considers the likely consequences of reducing the city’s green spaces.'),
    ('It’s a no-brainer: the old library has to stay open.', 'article (informal)', 'letter', 'Model: I strongly believe that the old library should remain open, for the reasons set out below.'),
]
t23 = topic('Using appropriate form, voice and register for the task', 'appropriate form voice and register', 'directed writing form')
t23.fixed('C1', (1, 2), [
    ('Which sign-off is correct for a formal letter that begins ‘Dear Sir or Madam’?', 'Yours faithfully', '‘Yours faithfully’ when the recipient is unnamed; ‘Yours sincerely’ when named.', ['Yours sincerely', 'Love from', 'Cheers']),
    ('Which feature is most typical of a speech rather than an article?', 'Direct address to a listening audience with signposting', 'Speeches are written to be heard.', ['A headline and strapline', 'Footnotes', 'A bibliography']),
    ('What is ‘voice’ in directed writing?', 'The sense of the writer’s role and personality conveyed through the writing', 'E.g. writing convincingly as a concerned resident or a student representative.', ['The volume when reading aloud', 'The number of quotations', 'The handwriting style']),
    ('In a directed writing task, what should you do with the source texts?', 'Use, develop and evaluate their ideas in your own words', 'Copying long phrases is penalised; evaluation is rewarded.', ['Copy the best sentences word for word', 'Ignore them and write your own ideas only', 'Summarise only the first text']),
])
classify_templates(t23, [(txt, lab, why) for lab, txt, why in OPENINGS_FORM], FORMS, ['Which form of writing does this opening most clearly belong to? {q}'],
                   C2frames=['This is the opening of a piece of writing in the form “{label}”: {q} Explain how the writer establishes the form, voice and register.'],
                   C3frames=[('Identify the form of this opening, explain its features and rewrite it as the opening of a different form (letter, speech, article or report): {q}',
                              lambda it: f'{cap(it[1])}: {it[2]}. The rewrite should adopt the conventions of the new form.', lambda it, m: f'{upto(m)}: 1 for the form ({it[1]}); 1 for features; remaining mark(s) for a convincing rewrite in a new form.')])
rewrite_templates(t23, [(f'Rewrite this sentence from {an(a)} so that it would work in {an(b)}.', s, model, f'Award for conventions and register of {an(b)}; meaning kept.') for s, a, b, model in SWAP], ['{ins} {q}'], D=(2, 3, 4))


@t23.add('C4', (2, 3, 4, 5), 'long')
def t23_form(r, D):
    P = r.choice(PAIRS)
    task, form, aud = r.choice(P.tasks)
    extra = f'Pay particular attention to the conventions of a {form} and to a voice and register suited to {aud}. '
    return directed_item(r, D, P, task, form, aud, extra)


# ---------------------------------------------------------------- 2.4 sustained critical response
FLAWS = ['sweeping generalisation', 'anecdotal evidence', 'emotive exaggeration', 'false choice (either/or)', 'unsupported statistic', 'appeal to authority without evidence']
FLAW_SNIP = [
    ('Everyone knows that teenagers spend too much time on their phones.', 'sweeping generalisation', '‘Everyone knows’ assumes agreement and applies the claim to all teenagers.'),
    ('My cousin worked at a café and failed her exams, so part-time jobs are harmful.', 'anecdotal evidence', 'one person’s case is used to draw a general conclusion.'),
    ('This plan will destroy our town forever.', 'emotive exaggeration', '‘destroy’ and ‘forever’ exaggerate to provoke fear rather than reason.'),
    ('Either we build the terminal or our island dies.', 'false choice (either/or)', 'only two extreme options are offered when others exist.'),
    ('Studies show that 90% of people prefer printed books.', 'unsupported statistic', 'no source or sample is given for the figure.'),
    ('A famous actor says zoos are cruel, so they must be.', 'appeal to authority without evidence', 'the person quoted has no relevant expertise and gives no evidence.'),
    ('No sensible parent would ever let their child cycle in the city.', 'sweeping generalisation', 'dismisses all who disagree as not sensible.'),
    ('If we allow phones at break, soon students will be using them in every lesson.', 'emotive exaggeration', 'a slippery-slope prediction with no evidence.'),
    ('Scientists agree that space exploration is the most important investment a country can make.', 'appeal to authority without evidence', 'vague ‘scientists’ with an extreme claim and no evidence.'),
    ('We must either ban cars completely or accept polluted air forever.', 'false choice (either/or)', 'ignores middle options such as partial restrictions.'),
]
t24 = topic('Developing a sustained, critical response with own judgement', 'sustained critical response', 'own judgement')
t24.fixed('C1', (1, 2), [
    ('In directed writing, what does ‘evaluate’ mean?', 'Judge how convincing, reliable or relevant the ideas are', 'Evaluation goes beyond repeating ideas.', ['Copy the main points', 'Count the paragraphs', 'Agree with both writers']),
    ('Which sentence shows evaluation rather than summary?', 'Text A’s claim that every student reads more is weakened by the lack of any evidence beyond one class.', 'It judges the quality of evidence.', ['Text A says students read more.', 'Text A is about tablets.', 'Text A has seven sentences.']),
    ('What makes a judgement ‘sustained’?', 'It is maintained and developed consistently throughout the response', 'The view runs through the whole answer, not just the conclusion.', ['It is stated only in the last line', 'It changes in every paragraph', 'It is the longest sentence']),
])
classify_templates(t24, FLAW_SNIP, FLAWS, ['Which weakness in reasoning does this claim show? {q}', 'A writer argues: {q} What is the main flaw in this argument?'],
                   C2frames=['This claim relies on {label}: {q} Explain why this weakens the argument.'],
                   C3frames=[('Write an evaluative sentence or two that challenges this claim in a directed writing response: {q}',
                              lambda it: f'Model: ‘Although the writer claims this, the argument depends on {it[1]}: {it[2]} A fairer view would need evidence such as surveys or wider examples.’',
                              lambda it, m: f'{upto(m)}: identifies the flaw ({it[1]}); explains why it is weak; suggests what would make the claim stronger; own words.')])


@t24.add('C3', (3, 4, 5), 'explain')
def t24_judge(r, D):
    P = r.choice(PAIRS)
    m = mk('C3', D)
    return {'stem': f'Text A: {Q(P.A["text"])} Text B: {Q(P.B["text"])} Write the concluding paragraph of a directed writing response on {P.issue}, giving your own judgement and justifying it with reference to the strengths and weaknesses of both texts.',
            'answer': f'Model: a clear judgement (e.g. a qualified position or compromise) that acknowledges the strongest point of each text ({P.A["points"][0]}; {P.B["points"][0]}), notes a key weakness ({P.A["weak"][0][1]}) and ends with a recommendation.',
            'key': f'{upto(m)}: own judgement clear; reference to both texts; evaluation of evidence; logical justification; appropriate register.'}


@t24.add('C4', (2, 3, 4, 5), 'long')
def t24_task(r, D):
    P = r.choice(PAIRS)
    task, form, aud = r.choice(P.tasks)
    extra = 'Develop a sustained, critical judgement of your own, challenging weak evidence in both texts. '
    return directed_item(r, D, P, task, form, aud, extra)


CHAPTERS[2] = [t21, t22, t23, t24]


# =========================================================== 3 Descriptive writing

NIGHTMKT = Text('nightmkt', 'description', 'a descriptive piece, ‘The Night Market’', """
By nine o'clock the car park has vanished beneath a city of canvas. Strings of bulbs sag between the stalls like
glowing fruit, and the air is thick with charcoal smoke and the sweet, burnt smell of caramelising sugar. Woks hiss.
A vendor flips a pancake high into the dark and catches it without looking, to a ripple of applause from a group of
children. Somewhere a speaker crackles out an old love song, half drowned by the bargaining of a hundred voices. Under
my feet the tarmac is sticky with spilled syrup, and the heat of the grills presses against my face like an open palm.
Nobody here is in a hurry. The night, it seems, belongs to everyone.""")
NIGHTMKT.f('the car park has vanished beneath a city of canvas', 'metaphor', 'a city of canvas', 'the stalls are so many and so packed that they form a temporary city, suggesting transformation and abundance.')
NIGHTMKT.f('Strings of bulbs sag between the stalls like glowing fruit', 'simile', 'like glowing fruit', 'the lights seem ripe, heavy and inviting, linking light to the market’s food and creating warmth.')
NIGHTMKT.f('Woks hiss.', 'onomatopoeia', 'hiss', 'the two-word sentence captures the sharp sound of cooking and adds energy.', also=('short sentence', 'sibilance'))
NIGHTMKT.f('the heat of the grills presses against my face like an open palm', 'simile', 'like an open palm', 'the heat feels physical and close, almost personal, conveying intensity through touch.', also=('personification', 'sensory imagery'))
NIGHTMKT.f('the air is thick with charcoal smoke and the sweet, burnt smell of caramelising sugar', 'sensory imagery', 'sweet, burnt smell', 'the contrasting smells make the scene vivid and suggest delicious richness.')
NIGHTMKT.f('The night, it seems, belongs to everyone.', 'personification', 'belongs to everyone', 'the final sentence gives the night a generous, communal quality, ending on a warm, inclusive mood.')
NIGHTMKT.x('How does the writer create a lively, welcoming atmosphere?', 'Metaphor of a city of canvas; warm light simile; sound (hiss, crackles, voices); smell and touch; communal details (applause, children); slow, relaxed ending.')

STATION = Text('station', 'description', 'a descriptive piece, ‘The Abandoned Station’', """
The last train left here thirty years ago, and the station has been holding its breath ever since. Weeds have pushed
up between the sleepers and now stand waist-high, nodding in a wind that carries no sound of engines. The clock above
the platform has stopped at twelve minutes past four, its hands folded like those of a patient at rest. Posters advertising
holidays to sunny places peel from the walls in long, curling tongues. In the waiting room a single bench remains, its
paint flaking, a newspaper fused to the slats by years of rain. A pigeon shifts in the rafters. Dust drifts down through
a shaft of light, slow as snow, and settles on nothing.""")
STATION.f('the station has been holding its breath ever since', 'personification', 'holding its breath', 'the station seems frozen in suspense, as if waiting for a train that will never come, creating a melancholy stillness.')
STATION.f('its hands folded like those of a patient at rest', 'simile', 'like those of a patient at rest', 'the stopped clock is linked to sickness or death, deepening the sense of lifelessness.')
STATION.f('peel from the walls in long, curling tongues', 'metaphor', 'curling tongues', 'the posters seem grotesque and mocking, their sunny promises decaying.')
STATION.f('Dust drifts down through a shaft of light, slow as snow, and settles on nothing.', 'simile', 'slow as snow', 'the slow, soft image creates a hushed, eerie atmosphere; ‘settles on nothing’ stresses emptiness.', also=('sibilance',))
STATION.f('A pigeon shifts in the rafters.', 'short sentence', 'A pigeon shifts in the rafters.', 'the tiny movement, isolated in a short sentence, emphasises how silent and empty the station is.')
STATION.x('How does the writer create an atmosphere of abandonment and stillness?', 'Personification (holding its breath); stopped clock simile; decaying posters; single bench; tiny sounds; slow dust image; emptiness in the final phrase.')

MONSOONDESC = Text('monsoondesc', 'description', 'a descriptive piece, ‘The First Rain’', """
For weeks the sky has been a lid of white heat pressed down on the town. Then, one afternoon, the light changes. The
horizon bruises purple. A hot wind snatches washing from the lines and sends dust spinning down the lane in small,
furious circles. The first drops are fat and slow, each one punching a dark coin into the dust. Then the sky splits
open. Rain hammers on the tin roofs with the roar of a stadium, the gutters choke and overflow, and the smell rises from
the ground – that rich, earthy smell, like bread and iron, that means the waiting is over. Children run out barefoot,
faces tipped up, mouths open, drinking the sky.""")
MONSOONDESC.f('the sky has been a lid of white heat pressed down on the town', 'metaphor', 'a lid of white heat', 'the sky traps the town like a lid on a pot, conveying oppressive, suffocating heat.')
MONSOONDESC.f('The horizon bruises purple.', 'metaphor', 'bruises', 'the sky seems injured and swollen, hinting at the violence of the coming storm.', also=('personification', 'short sentence'))
MONSOONDESC.f('each one punching a dark coin into the dust', 'metaphor', 'punching a dark coin', 'the heavy drops leave round marks like coins, and ‘punching’ conveys their force.')
MONSOONDESC.f('Rain hammers on the tin roofs with the roar of a stadium', 'hyperbole', 'the roar of a stadium', 'comparing the rain to a stadium crowd conveys overwhelming, celebratory noise.', also=('onomatopoeia', 'metaphor'))
MONSOONDESC.f('that rich, earthy smell, like bread and iron', 'simile', 'like bread and iron', 'the unusual pairing captures the complex smell of rain on dry ground, both comforting and metallic.', also=('sensory imagery',))
MONSOONDESC.f('faces tipped up, mouths open, drinking the sky', 'metaphor', 'drinking the sky', 'the children seem to drink the rain itself, a joyful image of relief.', also=('listing',))
MONSOONDESC.x('How does the writer convey the build-up to the rain and the relief when it arrives?', 'Oppressive metaphor of the lid; changing light; violent verbs (bruises, snatches, punching); sound of the rain; smell; joyful final image; structure moving from waiting to release.')

CORRIDOR = Text('corridor', 'description', 'a descriptive piece, ‘Ward Seven, 3 a.m.’', """
At three in the morning the hospital corridor is a long, white throat, swallowing sound. The floor has been polished
until it reflects the strip lights in a broken line that runs ahead of me like a road. Somewhere a machine beeps, steady
as a metronome, counting something I would rather not think about. The air smells of disinfectant and of the cold,
stale coffee in the paper cup I am holding. A nurse passes in soft shoes, nods without smiling, and is gone. Behind the
blue curtain at the end, my grandfather is sleeping. I can hear him breathing, a slow scrape like a spade in gravel. I
count the breaths. I do not stop counting.""")
CORRIDOR.f('the hospital corridor is a long, white throat, swallowing sound', 'metaphor', 'a long, white throat', 'the corridor seems to devour noise and the narrator, creating a sinister, sterile silence.', also=('personification',))
CORRIDOR.f('Somewhere a machine beeps, steady as a metronome, counting something I would rather not think about', 'simile', 'steady as a metronome', 'the regular beep marks time passing and hints at the grandfather’s fragile life.', also=('onomatopoeia',))
CORRIDOR.f('a slow scrape like a spade in gravel', 'simile', 'like a spade in gravel', 'the harsh, effortful sound conveys illness and quietly suggests digging, an image linked to death.')
CORRIDOR.f('I count the breaths. I do not stop counting.', 'repetition', 'count', 'the short repeated sentences show the narrator’s anxious fixation and fear of loss.', also=('short sentence',))
CORRIDOR.x('How does the writer create a tense, anxious atmosphere in the hospital?', 'Throat metaphor; reflective floor; machine beeping; smells; brief encounter with the nurse; grandfather’s breathing simile; short final sentences showing anxiety.')

SOUK = Text('souk', 'description', 'a descriptive piece, ‘The Spice Souk’', """
Step through the arch and the noise closes behind you like a door. The alley is barely wider than my outstretched arms,
roofed with slatted wood that cuts the sunlight into gold bars. Sacks slump open on either side: cinnamon bark curled like
old scrolls, chillies as red as warning lights, turmeric so yellow it seems to hum. A trader scoops cardamom into a paper
cone and presses it into my hand before I can refuse. The smells arrive in layers – clove, then cumin, then something
smoky I cannot name – until my eyes water. A donkey loaded with crates squeezes past, and I flatten myself against a wall
of saffron, laughing, breathless, utterly lost.""")
SOUK.f('the noise closes behind you like a door', 'simile', 'like a door', 'entering the souk feels like entering another world, sealed off from outside.', also=('direct address',))
SOUK.f('slatted wood that cuts the sunlight into gold bars', 'metaphor', 'gold bars', 'the light becomes precious and striped, adding richness and texture to the scene.')
SOUK.f('cinnamon bark curled like old scrolls, chillies as red as warning lights, turmeric so yellow it seems to hum', 'listing', 'cinnamon bark curled like old scrolls', 'the list of vivid comparisons overwhelms the senses, mirroring the abundance of the market.', also=('simile', 'sensory imagery'))
SOUK.f('turmeric so yellow it seems to hum', 'hyperbole', 'so yellow it seems to hum', 'the colour is so intense that it is imagined as sound (synaesthesia), conveying sensory overload.', also=('sensory imagery',))
SOUK.f('The smells arrive in layers – clove, then cumin, then something smoky I cannot name – until my eyes water.', 'sensory imagery', 'in layers', 'smells are structured like layers, guiding the reader through them and building intensity.', also=('listing',))
SOUK.x('How does the writer use sensory detail to bring the souk to life?', 'Sound closing like a door; light as gold bars; similes of colour; layered smells; touch (paper cone); movement (donkey); breathless final tricolon.')

LAKE = Text('lake', 'description', 'a descriptive piece, ‘The Frozen Lake at Dawn’', """
Before sunrise the lake is a sheet of pewter, so still that it seems to have stopped breathing. Frost has furred every
reed along the shore, and each blade wears a fine white coat that crackles when I brush it. My breath hangs in front of
me and refuses to leave. Far out on the ice, a fisherman's hut sits alone, its single window glowing orange, a small,
stubborn ember in all that grey. Then the sun lifts over the pines. Light runs across the ice in a sudden rush, the pewter
turns to rose and gold, and for one long second the whole lake blazes, as if someone has lit it from underneath.""")
LAKE.f('the lake is a sheet of pewter', 'metaphor', 'a sheet of pewter', 'the dull, grey metal suggests a cold, hard, motionless surface.')
LAKE.f('My breath hangs in front of me and refuses to leave.', 'personification', 'refuses to leave', 'the breath seems stubborn, emphasising how cold and still the air is.')
LAKE.f('its single window glowing orange, a small, stubborn ember in all that grey', 'metaphor', 'a small, stubborn ember', 'the warm light contrasts with the cold grey, suggesting human endurance and comfort.', also=('contrast',))
LAKE.f('for one long second the whole lake blazes, as if someone has lit it from underneath', 'hyperbole', 'the whole lake blazes', 'the dramatic image captures the sudden transformation at sunrise and creates awe.', also=('simile', 'metaphor'))
LAKE.x('How does the writer present the change from stillness to light?', 'Pewter metaphor and personified stillness; frost detail and sound; contrast of the ember-like window; turning point ‘Then the sun lifts’; colour shift and blazing final image.')
DESC_TEXTS = [NIGHTMKT, STATION, MONSOONDESC, CORRIDOR, SOUK, LAKE]
DESC_POOL = ['metaphor', 'simile', 'personification', 'onomatopoeia', 'hyperbole', 'sensory imagery', 'repetition', 'short sentence', 'listing', 'contrast', 'pathetic fallacy']

DESC_TITLES = [
    'Describe a market at the moment it opens in the morning.', 'Describe a place you know well during a power cut.', 'Describe the scene at a busy airport arrivals hall.',
    'Describe a beach at the end of the holiday season.', 'Describe a city street during a sudden storm.', 'Describe an old building that is about to be demolished.',
    'Describe the view from a high place at sunset.', 'Describe a crowded bus or train on a hot day.', 'Describe a garden that has been left untended for many years.',
    'Describe a kitchen during the preparation of a festival meal.', 'Describe a school building at night when everyone has gone home.', 'Describe a harbour in the hour before a storm.',
    'Describe a forest in the moments after heavy rain.', 'Describe a waiting room where people are anxious for news.', 'Describe a stadium before, during and after an important match.',
]
DESC_IND = 'focus on a specific place and moment; carefully selected sensory detail; original imagery; deliberate structure (shifts of time, focus or scale); atmosphere sustained; does not become a story.'

# ---------------------------------------------------------------- 3.1 atmosphere and sense of place
ATMOS = ['menacing and tense', 'peaceful and serene', 'lively and joyful', 'desolate and melancholy', 'eerie and unsettling', 'oppressive and suffocating']
ATMOS_SNIP = [
    (NIGHTMKT, 'lively and joyful'), (STATION, 'desolate and melancholy'), (CORRIDOR, 'eerie and unsettling'), (LAKE, 'peaceful and serene'), (SOUK, 'lively and joyful'),
]
NEUTRAL = ['The road led through the forest to the village.', 'There was a house at the end of the street.', 'The classroom was empty after school.', 'The boat was tied up in the harbour.',
           'The park had a pond, some trees and a bench.', 'The train stopped at the small station.', 'The kitchen had a table and a window.', 'The beach was long and the sea was calm.']
ATMOS_MODEL = {'menacing and tense': 'shadows, sharp or threatening verbs, silence broken by sudden sounds, short sentences',
               'peaceful and serene': 'soft sounds, gentle light, slow rhythm, long flowing sentences',
               'lively and joyful': 'bright colours, energetic verbs, music and voices, warm light',
               'desolate and melancholy': 'decay, emptiness, muted colours, absence of people',
               'eerie and unsettling': 'unexplained details, unnatural stillness, odd sounds, things slightly wrong',
               'oppressive and suffocating': 'heat, heaviness, enclosed spaces, verbs of pressing and weighing down'}
t31 = topic('Creating atmosphere and a sense of place', 'creating atmosphere', 'sense of place')
t31.fixed('C1', (1, 2), [
    ('What is atmosphere in descriptive writing?', 'The mood or feeling that a place creates for the reader', 'Built from detail, imagery, sound and sentence rhythm.', ['The weather forecast', 'The order of events in a plot', 'The number of characters']),
    ('Which detail would best create a menacing atmosphere in a forest?', 'Branches clawing at the narrow path', 'Violent, personified verbs suggest threat.', ['Sunlight dappling the moss', 'Birds singing cheerfully', 'A family picnic in a clearing']),
    ('What is pathetic fallacy?', 'Using weather or setting to reflect a mood', 'E.g. a storm building as tension rises.', ['A false argument', 'A type of rhyme', 'A sad character']),
    ('What does a ‘sense of place’ mean in descriptive writing?', 'the reader can vividly imagine a specific, believable location', 'Specific, concrete details create it.', ['the writer names a famous city', 'the description has a map', 'the place is described in one sentence']),
])


@t31.add('C1', (1, 2, 3))
def t31_atmos(r, D):
    T, at = r.choice(ATMOS_SNIP)
    sent = r.choice([f.quote for f in T.feats])
    opts, ans = mcq(r, at, [a for a in ATMOS if a != at and not (at == 'lively and joyful' and a == 'peaceful and serene')])
    return {'stem': f'This line comes from {T.label}: {Q(sent)} Which atmosphere does the piece as a whole create?', 'options': opts, 'answer': ans, 'key': f'The piece is {at}. {T.foci[0][1]}'}


feature_templates(t31, [f for T in (NIGHTMKT, STATION, CORRIDOR, MONSOONDESC) for f in T.feats], DESC_POOL, c1=False)


@t31.add('C3', (1, 2, 3, 4, 5), 'short')
def t31_rewrite(r, D):
    s = r.choice(NEUTRAL)
    at = r.choice(ATMOS)
    m = mk('C3', D)
    return {'stem': f'Rewrite this plain sentence as two or three sentences that create a {at} atmosphere: {Q(s)} Then explain one choice you made.',
            'answer': f'Any rewrite using techniques that suit a {at} atmosphere, e.g. {ATMOS_MODEL[at]}, with an explanation.',
            'key': f'{upto(m)}: atmosphere clearly {at}; precise vocabulary and imagery; sentence rhythm supports the mood; explanation of one choice.'}


comp_templates(t31, [(f'{t_} Focus on creating a strong atmosphere and a vivid sense of place.', DESC_IND, f'Model approach: choose one dominant atmosphere; open with a striking image; build detail through the senses; vary sentence length to control mood; end on an image that crystallises the atmosphere.')
                     for t_ in DESC_TITLES[:8]], 'descriptive')


# ---------------------------------------------------------------- 3.2 sensory detail, imagery and zoom
SENSES = ['sight', 'sound', 'smell', 'touch', 'taste']
SENSE_SNIP = [('the sweet, burnt smell of caramelising sugar', 'smell'), ('Woks hiss.', 'sound'), ('the tarmac is sticky with spilled syrup', 'touch'), ('cuts the sunlight into gold bars', 'sight'),
              ('the cold, stale coffee in the paper cup', 'taste'), ('a slow scrape like a spade in gravel', 'sound'), ('each blade wears a fine white coat that crackles when I brush it', 'touch'),
              ('that rich, earthy smell, like bread and iron', 'smell'), ('chillies as red as warning lights', 'sight'), ('the salt of the spray drying on my lips', 'taste'),
              ('the bargaining of a hundred voices', 'sound'), ('the pewter turns to rose and gold', 'sight')]
ZOOM = [
    ('a crowded railway platform', 'a single abandoned glove on a bench', 'Model: start wide (crowds, announcements), narrow to one bench, then to the glove – its frayed fingers, a ticket stub inside – suggesting a story without telling it.'),
    ('a busy beach', 'a child’s sandcastle as the tide comes in', 'Model: pan across umbrellas and swimmers, then focus on the sandcastle’s crumbling walls and the water filling its moat.'),
    ('a city skyline at night', 'one lit window in an office tower', 'Model: wide view of lights and traffic, then a single window, a figure at a desk, a cold cup of tea.'),
    ('a school sports day', 'the hands of a runner waiting at the start line', 'Model: noise and colour of the crowd, then the runner’s chalky fingers trembling on the track.'),
    ('a mountain village', 'an old woman’s hands kneading bread', 'Model: terraced fields and smoke, then a doorway, then the floury hands moving in a steady rhythm.'),
    ('a hospital waiting room', 'a ticking wall clock', 'Model: rows of anxious faces, then the clock’s second hand dragging forward, its tick unbearably loud.'),
    ('a flower market', 'a single bruised rose on the floor', 'Model: abundance and colour, then the discarded rose, a footprint on its petals.'),
    ('a storm at sea', 'a gull clinging to a mast', 'Model: towering waves and wind, then the gull’s feathers flattened, its claws gripping the wet wood.'),
]
t32 = topic('Using sensory detail, imagery and zoom-in focus', 'sensory detail imagery', 'zoom-in focus')
t32.fixed('C1', (1, 2), [
    ('What is meant by ‘zooming in’ in descriptive writing?', 'Moving from a wide view to a close focus on a small, revealing detail', 'Like a camera lens; small details make a description vivid and original.', ['Writing in very large handwriting', 'Describing only the weather', 'Telling the story faster']),
    ('Which sense is often neglected but very effective in description?', 'Smell', 'Smell is strongly linked to memory and atmosphere.', ['Sight', 'Movement', 'Size']),
    ('What is synaesthesia in description?', 'Describing one sense in terms of another', 'E.g. ‘turmeric so yellow it seems to hum’.', ['Using only sight', 'Listing all five senses', 'A type of punctuation']),
])


@t32.add('C1', (1, 2, 3))
def t32_sense(r, D):
    ph, sense = r.choice(SENSE_SNIP)
    opts, ans = mcq(r, sense, [x for x in SENSES if x != sense])
    return {'stem': f'Which sense does this phrase mainly appeal to? {Q(ph)}', 'options': opts, 'answer': ans, 'key': f'The phrase appeals mainly to {sense}.'}


feature_templates(t32, [f for T in (SOUK, LAKE, MONSOONDESC, NIGHTMKT) for f in T.feats], DESC_POOL)


@t32.add('C3', (2, 3, 4, 5), 'short')
def t32_zoom(r, D):
    wide, close, model = r.choice(ZOOM)
    m = mk('C3', D)
    return {'stem': f'Write a short descriptive paragraph about {wide} that begins with a wide view and gradually zooms in on {close}. Use at least two senses other than sight.',
            'answer': model, 'key': f'{upto(m)}: clear movement from wide to close focus; at least two non-visual senses; original imagery; the final detail is revealing or symbolic.'}


compose_templates(t32, DESC_TEXTS, C=('C3', 'C4'))
comp_templates(t32, [(f'{t_} Use sensory detail and original imagery, and include at least one moment where you zoom in on a small detail.', DESC_IND, 'Model approach: wide establishing view; selective zoom on revealing details; all five senses considered; imagery that is fresh and precise.')
                     for t_ in DESC_TITLES[5:]], 'descriptive')

# ---------------------------------------------------------------- 3.3 structuring description without narrative
D_STRUCT = ['time-lapse (the same place at different times)', 'wide view to close-up (zoom)', 'journey through a space', 'contrast (before and after)', 'circular (returning to the opening image)']
D_PLANS = [
    ('Paragraph 1: the beach at dawn; 2: midday crowds; 3: late afternoon; 4: night, waves only.', D_STRUCT[0], 'each paragraph is a new moment in time, showing change without a plot.'),
    ('Paragraph 1: the whole valley from the hilltop; 2: the village; 3: one house; 4: a cracked cup on the windowsill.', D_STRUCT[1], 'the focus narrows from panorama to a single detail.'),
    ('Paragraph 1: entering the gate; 2: the courtyard; 3: the corridor; 4: the room at the end.', D_STRUCT[2], 'the reader moves through the space step by step.'),
    ('Paragraph 1: the square during the festival; 2: the square the next morning, littered and silent.', D_STRUCT[3], 'two contrasting snapshots highlight change and mood.'),
    ('Paragraph 1: rain on the window; 2–4: the room and memories it holds; 5: the rain on the window again, now easing.', D_STRUCT[4], 'the return to the opening image gives shape and a sense of closure.'),
    ('Paragraph 1: the station at 5 a.m.; 2: rush hour; 3: midnight.', D_STRUCT[0], 'the description is organised by time.'),
    ('Paragraph 1: the ocean from the cliff; 2: the rocks below; 3: a rock pool; 4: a tiny crab in the pool.', D_STRUCT[1], 'zooming down reveals hidden life.'),
    ('Paragraph 1: the forest before the fire; 2: the forest a year after.', D_STRUCT[3], 'before/after contrast conveys loss and recovery.'),
]
t33 = topic('Structuring description without narrative', 'structuring description without narrative', 'moments in time')
t33.fixed('C1', (1, 2), [
    ('What is the main risk in a descriptive composition?', 'Drifting into a story with a plot and events', 'Description should focus on a place or moment, not on what happens next.', ['Using too many adjectives', 'Having more than three paragraphs', 'Writing in the present tense']),
    ('Which tense is often effective for descriptive writing because it creates immediacy?', 'The present tense', 'E.g. ‘The market wakes…’.', ['The future perfect tense', 'The conditional', 'The past perfect only']),
    ('Which of these is a structural device in description rather than narrative?', 'Shifting focus from one part of the scene to another', 'Structure comes from focus, time or space, not plot.', ['A climax and resolution', 'A twist ending', 'A flashback to explain a character’s motive']),
])
classify_templates(t33, D_PLANS, D_STRUCT, ['Which structure does this descriptive plan use? {q}'],
                   C2frames=['This plan uses a {label} structure: {q} Explain how it gives shape to a description without a plot.'],
                   C3frames=[('Identify the structure of this plan, explain its effect, and adapt it for a description of a hospital at night: {q}',
                              lambda it: f'{cap(it[1])}: {it[2]} Adapted plan: any plan for a hospital at night following the same structure.', lambda it, m: f'{upto(m)}: 1 for {it[1]}; 1 for effect; remaining mark(s) for a coherent adapted plan.')])


@t33.add('C3', (2, 3, 4, 5), 'short')
def t33_plan(r, D):
    t_ = r.choice(DESC_TITLES)
    st = r.choice(D_STRUCT)
    m = mk('C3', D)
    return {'stem': f'Plan a five-paragraph descriptive composition for this task, using {an(st)} structure: {Q(t_)} Give the focus of each paragraph and one image or sensory detail for each.',
            'answer': f'Model: five paragraphs organised by {st}; each with a clear focus and a specific image; no plot events; a final paragraph that gives closure.',
            'key': f'{upto(m)}: structure clearly {st}; five distinct foci; specific images; avoids narrative; effective ending planned.'}


t33.fixed('C2', (2, 3, 4), [(f'Read {T.label}: {Q(T.text)} Explain how the writer structures the description.', a, '1 mark per structural point (opening, shifts of focus or time, turning point, ending) linked to effect.')
                             for T, a in [(MONSOONDESC, 'Time-based: weeks of heat → change of light → wind → first drops → downpour → smell → children; it builds like a crescendo from tension to release.'),
                                          (LAKE, 'Moves from pre-dawn stillness and close details (frost, breath) to a distant hut, then the turning point ‘Then the sun lifts’ and a blazing final image.'),
                                          (STATION, 'A tour through the space: tracks and weeds, clock, posters, waiting room, rafters, then the dust – each detail adds to the stillness, ending on emptiness.'),
                                          (SOUK, 'A journey through the alley: entrance, light, sacks of spice, the trader, layered smells, the donkey – the structure mirrors being drawn deeper and getting lost.')]])
comp_templates(t33, [(f'{t_} Structure your description using {st}, and do not let it become a story.', DESC_IND + f' Structure: {st}.', f'Model approach: plan five paragraphs using {st}; one focus and atmosphere per paragraph; link paragraphs with time, place or focus shifts; finish with an image that closes the piece.')
                     for t_ in DESC_TITLES[::2] for st in D_STRUCT[:3]], 'descriptive')

# ---------------------------------------------------------------- 3.4 avoiding cliché and overwriting
CLICHES = [('as cold as ice', 'cold enough to make my teeth ache'), ('the sun was shining brightly', 'sunlight lay across the street like a warm hand'), ('a deafening silence', 'a silence so complete I could hear the fridge hum two rooms away'),
           ('as quiet as a mouse', 'so quiet that the clock seemed loud'), ('it was a dark and stormy night', 'rain drummed on the car roof and the wipers lost every argument'), ('her heart was pounding', 'she could feel her pulse in her fingertips'),
           ('time stood still', 'the second hand seemed to hesitate'), ('the crowd went wild', 'the stands rose in a single roaring wave'), ('white as snow', 'white as a freshly washed sheet'), ('fluffy white clouds', 'clouds piled like unwashed laundry')]
CLICHE_CTX = {
    'as cold as ice': 'When I stepped off the bus, the wind was as cold as ice.',
    'the sun was shining brightly': 'On the morning of the wedding the sun was shining brightly.',
    'a deafening silence': 'After the announcement there was a deafening silence in the hall.',
    'as quiet as a mouse': 'The library was as quiet as a mouse.',
    'it was a dark and stormy night': 'It was a dark and stormy night when we reached the cottage.',
    'her heart was pounding': 'As she waited for her name to be called, her heart was pounding.',
    'time stood still': 'When the car skidded towards us, time stood still.',
    'the crowd went wild': 'When the final goal went in, the crowd went wild.',
    'white as snow': 'The hospital sheets were white as snow.',
    'fluffy white clouds': 'Above the beach there were fluffy white clouds.',
}
FRESH = ['the moon hung like a fingernail clipping over the rooftops', 'traffic lights blinked at the empty junction', 'the kettle ticked as it cooled', 'rain needled the surface of the pond',
         'the old dog sighed like a deflating cushion', 'sunlight lay in a thin stripe across the floor', 'gulls argued over a chip packet', 'the radiator knocked twice and fell silent']
OVERWRITTEN = [
    ('The incredibly beautiful, stunningly gorgeous, amazingly bright golden yellow sun shone down beautifully on the lovely sparkling blue sea.', 'The sun laid a path of gold across the sea.', 'too many adjectives and adverbs repeat the same idea; one precise image is stronger.'),
    ('The dark, black, gloomy, shadowy, terrifying, frightening forest was very scary.', 'Branches knitted together overhead until the path disappeared.', 'synonyms pile up without adding meaning; showing is more frightening than telling.'),
    ('Like a lion, the wind roared like a monster, like a train, crashing like waves against the house.', 'The wind shouldered the house like an angry crowd.', 'too many mixed similes compete; one controlled image is clearer.'),
    ('My heart was beating extremely fast like a drum, a racing car and a galloping horse all at once.', 'My heart thudded against my ribs.', 'stacked comparisons dilute the effect.'),
    ('The magnificent, splendid, wonderful palace was very, very big and enormously huge.', 'The palace stretched the length of the square, its windows catching the light one after another.', 'repetitive intensifiers; concrete detail conveys size better.'),
    ('Tears of sorrowful sadness rolled down her sad, unhappy face.', 'She wiped her eyes with the back of her hand and kept walking.', 'tautology (sorrowful sadness, sad unhappy); restraint is more moving.'),
]
t34 = topic('Avoiding cliché and overwriting', 'avoiding cliché and overwriting')
t34.fixed('C1', (1, 2), [
    ('What is a cliché?', 'An overused phrase that has lost its originality', 'E.g. ‘as cold as ice’.', ['A new metaphor', 'A spelling mistake', 'A type of sentence']),
    ('What is overwriting?', 'Using too many adjectives, adverbs or images so that the writing becomes cluttered', 'Excess description weakens clarity and effect.', ['Writing more than the word limit', 'Writing too neatly', 'Using paragraphs']),
    ('Which is usually more effective in a description?', 'One precise, original image', 'Precision and control score higher than quantity (W3).', ['Five similes in one sentence', 'A list of ten adjectives', 'Repeating ‘very’ for emphasis']),
])


@t34.add('C1', (1, 2, 3))
def t34_cliche(r, D):
    c, _ = r.choice(CLICHES)
    opts, ans = mcq(r, c, r.sample(FRESH, 3))
    return {'stem': 'Which of these phrases is a cliché that a strong descriptive writer would avoid?', 'options': opts, 'answer': ans, 'key': f'{Q(c)} is a cliché; the others are original, specific images.'}


@t34.add('C2', (1, 2, 3, 4), 'explain')
def t34_over(r, D):
    bad, good, why = r.choice(OVERWRITTEN)
    m = mk('C2', D)
    return {'stem': f'Explain why this sentence is an example of overwriting: {Q(bad)}', 'answer': cap(why), 'key': f'{upto(m)}: identifies the excess (adjectives, intensifiers, mixed images, tautology); explains the effect on the reader; may suggest a fix.'}


rewrite_templates(t34, [(f'Replace the cliché {Q(c)} with an original image, and explain why it is more effective.', CLICHE_CTX[c],
                         f'Model: {Q(f)} – more specific and surprising, so the reader sees and feels it freshly.', 'Award for originality, precision and a clear explanation.') for c, f in CLICHES] +
                 [('Rewrite this overwritten sentence with precision and control.', b, f'Model: {Q(g)}', f'Award for cutting excess ({w}) while keeping or sharpening the image.') for b, g, w in OVERWRITTEN],
                 ['{ins} {q}', '{q} {ins}'], D=(1, 2, 3, 4, 5))
comp_templates(t34, [(f'{t_} Avoid clichés and overwriting: aim for precise, original detail. After your description, write two sentences explaining one cliché you avoided and what you used instead.', DESC_IND + ' Fresh imagery; controlled use of adjectives; reflective note.', 'Model approach: plan two or three central images; test each for originality; prefer concrete nouns and strong verbs; end with a restrained image.')
                     for t_ in DESC_TITLES[1::2]], 'descriptive')
CHAPTERS[3] = [t31, t32, t33, t34]


# =========================================================== 4 Narrative writing

LIFT = Text('lift', 'fiction', 'a narrative extract, ‘Floor Nineteen’', """
The lift shuddered, dropped a few centimetres and stopped. For a moment nobody spoke. The light above the doors
flickered between 18 and 19, as if it could not decide. Then it went out. In the darkness I heard the man beside me
begin to breathe faster, short dry gasps, and the woman in the corner whispered something in a language I did not know.
I pressed the alarm. Nothing. I pressed it again and held it until my thumb ached. Somewhere far above us, a cable
groaned. Then, very softly, the floor began to tilt.""")
LIFT.f('The lift shuddered, dropped a few centimetres and stopped.', 'listing', 'shuddered, dropped a few centimetres and stopped', 'the sequence of verbs mimics the jerky movement, plunging the reader straight into danger.')
LIFT.f('The light above the doors flickered between 18 and 19, as if it could not decide.', 'personification', 'as if it could not decide', 'the hesitating light mirrors the uncertainty of the passengers and stretches the moment.')
LIFT.f('I pressed the alarm. Nothing.', 'short sentence', 'Nothing.', 'the one-word minor sentence crushes hope and heightens fear.')
LIFT.f('Somewhere far above us, a cable groaned.', 'personification', 'groaned', 'the cable seems to be in pain, suggesting it may break and building dread.', also=('onomatopoeia',))
LIFT.f('Then, very softly, the floor began to tilt.', 'cliffhanger', 'the floor began to tilt', 'ending on a quiet but terrifying movement leaves the reader in suspense.')
LIFT.x('How does the writer build tension in this extract?', 'In medias res; short sentences and fragments; sensory details in darkness; personified light and cable; repeated failed actions; slow, soft final cliffhanger.')

AUNTIE = Text('auntie', 'fiction', 'a narrative extract, ‘Auntie Grace Arrives’', """
'Is this the house?' said Auntie Grace, though she could see the number on the gate perfectly well. She looked at the
peeling paint, then at my mother, then at the paint again. 'Well,' she said. 'I suppose it has character.' My mother
smiled the smile she keeps for dentists and tax inspectors. 'Come in, Grace. You must be tired.' 'Tired?' said Auntie
Grace, handing me a suitcase that weighed as much as I did. 'I am seventy-four, child. I have been tired since 1987.' She
swept past us into the hall, ran one gloved finger along the banister, and examined it in silence. My mother closed her
eyes for a moment, and I knew that this was going to be a very long month.""")
AUNTIE.i("'Well,' she said. 'I suppose it has character.'", 'What does this line reveal about Auntie Grace?', 'She is critical and snobbish, delivering an insult disguised as politeness.', '1 mark: critical/snobbish; 1 mark: polite surface hides criticism')
AUNTIE.i("My mother smiled the smile she keeps for dentists and tax inspectors.", 'What does this suggest about the mother’s feelings?', 'She is forcing politeness while feeling tense and reluctant; the humour shows the narrator knows her well.', '1 mark: forced politeness/tension; 1 mark: explanation of the comic comparison')
AUNTIE.i('ran one gloved finger along the banister, and examined it in silence', 'How does this action reveal character without dialogue?', 'She is checking for dust, showing she is judgemental and fussy; the silence makes the criticism more cutting.', '1 mark: judgemental; 1 mark: silence/gesture as criticism')
AUNTIE.f("'I am seventy-four, child. I have been tired since 1987.'", 'hyperbole', 'tired since 1987', 'her dry, exaggerated reply is comic and shows her sharp wit and self-importance.', also=('dialogue',))
AUNTIE.f('handing me a suitcase that weighed as much as I did', 'hyperbole', 'weighed as much as I did', 'the exaggeration adds humour and shows Grace treating the narrator as a porter.')
AUNTIE.x('How does the writer use dialogue and action to present Auntie Grace?', 'Pointed questions; backhanded compliment; sharp witty replies; gestures (gloved finger); reactions of the mother; humorous first-person narrator; ending that anticipates conflict.')

PHOTO = Text('photo', 'fiction', 'the ending of a short story, ‘The Photograph’', """
I found the photograph on the last day, when the house was empty and the removal van was already turning the corner.
It had slipped behind the radiator: my father at twenty, younger than my brother is now, standing on a beach I had never
seen, laughing at something outside the frame. All my life I had known him as a careful man, a man who checked the locks
twice and never sang. I had not known he could laugh like that. I put the photograph in my pocket and stood for a long
time in the bare kitchen. Then I locked the door – once – and walked down the hill towards the station, and I did not
check it again.""")
PHOTO.i("All my life I had known him as a careful man, a man who checked the locks twice and never sang. I had not known he could laugh like that.", 'What realisation does the narrator have?', 'The narrator discovers a carefree side of their father they never knew, changing how they see him.', '1 mark: realisation about the father; 1 mark: contrast between careful man and laughing youth')
PHOTO.i('Then I locked the door – once – and walked down the hill towards the station, and I did not check it again.', 'Why is the final sentence effective?', 'It echoes the father’s habit of checking twice; locking ‘once’ shows the narrator choosing to live more freely, giving a quiet epiphany.', '1 mark: echo of earlier detail; 1 mark: change in the narrator / epiphany')
PHOTO.f('Then I locked the door – once – and walked', 'repetition', 'once', 'the dashes isolate ‘once’, echoing the father’s double-checking and marking the narrator’s change.')
PHOTO.x('How does the writer create an effective ending to the story?', 'Setting of departure; discovery of the photograph; contrast between the father the narrator knew and the young man; quiet epiphany; circular echo of the locks; understated final sentence.')

VOICE_T = Text('voice', 'fiction', 'a narrative extract, ‘My Brother the Genius’', """
My brother Femi is nine and thinks he is a scientist. Yesterday he put Mum's watch in the freezer to see if time would
slow down. It did not, he says, but only because the watch is cheap. Today he is building a rocket from the vacuum
cleaner, which Mum does not know about yet. I am supposed to be watching him, but I am also supposed to be revising,
and you cannot do both, whatever adults say. So I am lying on the sofa, revising the ceiling. If the house explodes,
I would like it known that I was against the vacuum cleaner from the start.""")
VOICE_T.f('So I am lying on the sofa, revising the ceiling.', 'irony', 'revising the ceiling', 'the joke reveals the narrator is not revising at all, creating a comic, self-aware voice.')
VOICE_T.f('If the house explodes, I would like it known that I was against the vacuum cleaner from the start.', 'hyperbole', 'If the house explodes', 'the exaggerated, formal disclaimer is comic and shows the narrator’s dry, teenage voice.', also=('irony',))
VOICE_T.f('It did not, he says, but only because the watch is cheap.', 'irony', 'only because the watch is cheap', 'the narrator reports Femi’s excuse with mock seriousness, highlighting his absurd logic.')
VOICE_T.x('How does the writer create a distinctive narrative voice?', 'First-person present tense; conversational asides to ‘you’; dry humour and irony; affectionate mockery of Femi; comic exaggeration; self-justifying ending.')
NARR_TEXTS = [LIFT, AUNTIE, PHOTO, VOICE_T]
NARR_POOL = ['short sentence', 'personification', 'listing', 'cliffhanger', 'hyperbole', 'irony', 'repetition', 'simile', 'metaphor', 'dialogue']

NARR_TITLES = ['The Return', 'The Key', 'Lost', 'The Stranger', 'The Last Train', 'The Decision', 'Second Chance', 'The Island', 'Footsteps', 'The Gift', 'Breaking Point', 'The Silence', 'Inheritance', 'The Bridge']
NARR_STARTS = ['The phone had been ringing for a long time before I realised it was for me.', 'Nobody in the village had opened the gate for twenty years.', 'I knew as soon as I saw the envelope that everything was about to change.',
               'The storm arrived three hours earlier than the forecast had promised.', 'It was the kind of mistake you only make once.', 'She had promised herself she would never go back.']
NARR_IND = 'engaging opening; convincing characters and setting; deliberate structure with a clear turning point; controlled pace and tension; effective, earned ending; narrative voice sustained.'

# ---------------------------------------------------------------- 4.1 plot and structure
N_STRUCT = ['linear', 'in medias res', 'frame narrative', 'circular', 'dual timeline', 'reverse chronology']
N_PLANS = [
    ('Start with the narrator trapped in a lift, then fill in how they got there, then the rescue.', 'in medias res', 'the story opens at a dramatic moment and explains afterwards.'),
    ('An old woman tells her granddaughter the story of her journey across the border; we return to them at the end.', 'frame narrative', 'a story within a story, framed by the present-day conversation.'),
    ('Open at the bus stop in the rain; end at the same bus stop a year later.', 'circular', 'returning to the opening setting shows how the character has changed.'),
    ('Alternate chapters between a girl in 1965 and her granddaughter today, revealing a family secret.', 'dual timeline', 'two time periods run in parallel and illuminate each other.'),
    ('Begin with the funeral and move backwards, scene by scene, to the first meeting.', 'reverse chronology', 'events are told backwards, so the reader knows the outcome and focuses on causes.'),
    ('Morning: the boy finds the dog. Afternoon: he hides it. Evening: his father discovers it.', 'linear', 'events follow in time order.'),
    ('Start as the boat capsizes, then flash back to the argument on the shore, then return to the struggle in the water.', 'in medias res', 'dramatic opening followed by backstory.'),
    ('A diary found in an attic tells most of the story; the finder’s reaction closes it.', 'frame narrative', 'the found diary is framed by the finder’s story.'),
]
t41 = topic('Planning plot and structure', 'planning plot and structure', 'openings climax and resolution')
t41.fixed('C1', (1, 2), [
    ('In a 350–450 word narrative, what is usually the best approach to plot?', 'A single focused incident with one main turning point', 'Short compositions reward focus and development over many events.', ['As many events as possible', 'A story covering a whole lifetime', 'Several unconnected episodes']),
    ('What is the climax of a narrative?', 'The point of highest tension where the central conflict comes to a head', 'Everything builds to it; the resolution follows.', ['The opening paragraph', 'The title', 'The description of the setting']),
    ('Why should you plan the ending before you start writing?', 'So that you can build towards it and avoid a rushed or random conclusion', 'Planning endings helps control structure (W2).', ['Because endings are not marked', 'So you can write it first', 'Because the ending must be a twist']),
    ('What does ‘resolution’ mean in a story?', 'How the central conflict is settled or left at the end', 'It may be closed or deliberately open.', ['The start of the conflict', 'A list of characters', 'A detailed description']),
])
classify_templates(t41, N_PLANS, N_STRUCT, ['Which narrative structure does this plan use? {q}'],
                   C2frames=['This plan uses a {label} structure: {q} Explain how this structure could make the story more effective.'],
                   C3frames=[('Identify the structure in this plan and explain one advantage and one risk of using it in an exam composition: {q}',
                              lambda it: f'{cap(it[1])}: {it[2]} Risk: confusing time shifts or running out of words before the resolution.', lambda it, m: f'{upto(m)}: 1 for {it[1]}; 1 for an advantage; 1 for a risk; further marks for developed explanation.')])


@t41.add('C3', (2, 3, 4, 5), 'short')
def t41_plan(r, D):
    ti = r.choice(NARR_TITLES)
    st = r.choice(N_STRUCT[:4])
    m = mk('C3', D)
    return {'stem': f'Plan a narrative composition called {Q(ti)} using {an(st)} structure. Outline the opening, the rising action, the climax and the resolution in one or two lines each.',
            'answer': f'Model: opening that hooks (consistent with a {st} structure); rising complications; a single clear climax; a resolution that links back to the title {Q(ti)}.',
            'key': f'{upto(m)}: structure clearly {st}; focused plot; clear climax; resolution earned and linked to the title; realistic for 350–450 words.'}


comp_templates(t41, [(f'Write a story with the title {Q(ti)}.', NARR_IND, f'Model approach for {Q(ti)}: plan a single focused conflict; hook in the first line; build to a clear climax; resolve with an image or line that links back to the title.') for ti in NARR_TITLES] +
                    [(f'Write a story that begins with the sentence: {Q(s)}', NARR_IND, 'Model approach: use the given sentence as a hook; establish character and stakes quickly; build to a turning point; end with resolution or a deliberate open ending.') for s in NARR_STARTS], 'narrative')

# ---------------------------------------------------------------- 4.2 characters and voice
VOICES = ['naive narrator', 'unreliable narrator', 'retrospective adult narrator', 'second-person narrator', 'omniscient narrator', 'stream of consciousness']
VOICE_SNIP = [
    ('Mummy says Uncle Joe has gone to live on a farm far away, which is strange because he hated cows.', 'naive narrator', 'the child does not understand what the reader can infer (Uncle Joe has probably died).'),
    ('I did not take the money. I merely borrowed it without asking, which is completely different.', 'unreliable narrator', 'the narrator’s self-justification shows their account cannot be trusted.'),
    ('I was fourteen that summer, and I believed, as you do at fourteen, that I would never be that unhappy again.', 'retrospective adult narrator', 'the adult looks back on youth with hindsight and wry wisdom.'),
    ('You wake before the alarm. You lie still, listening to the rain, and you remember what day it is.', 'second-person narrator', '‘you’ places the reader inside the experience.'),
    ('In the house on the corner, three people lay awake that night, each believing they alone knew the secret.', 'omniscient narrator', 'the narrator knows all three characters’ thoughts.'),
    ('bus late again rain in my shoes what did she mean by that look why do I always say the wrong thing', 'stream of consciousness', 'unpunctuated, racing thoughts mimic the mind’s flow.'),
    ('The man next door is a spy. I know because he has three bins and nobody needs three bins.', 'naive narrator', 'the child’s comic logic reveals innocence.'),
    ('Looking back, I can see that the argument was never really about the bicycle.', 'retrospective adult narrator', 'hindsight reinterprets the past.'),
]
NEUTRAL_P = ['A boy waits outside the head teacher’s office after being accused of breaking a window.', 'A woman returns to her childhood village after thirty years.', 'Two friends wait for exam results on a hot morning.',
             'A girl gets lost at a crowded festival.', 'A family’s car breaks down on a desert road at night.', 'An old fisherman decides whether to sell his boat.']
t42 = topic('Developing convincing characters and narrative voice', 'developing convincing characters', 'narrative voice')
t42.fixed('C1', (1, 2), [
    ('What makes a narrative voice ‘distinctive’?', 'A consistent, recognisable personality conveyed through vocabulary, rhythm and attitude', 'E.g. the dry humour of a teenage narrator.', ['Using as many characters as possible', 'Writing in the past tense', 'Avoiding dialogue']),
    ('Which is the most effective way to make a character convincing in a short story?', 'Reveal them through specific actions, speech and small details', 'Show, don’t tell; one telling detail is worth a paragraph of description.', ['List their appearance in detail at the start', 'Give them a very unusual name', 'Describe their whole life history']),
    ('What is a naive narrator?', 'A narrator who does not fully understand what they describe, while the reader does', 'Often a child; creates dramatic irony.', ['A narrator who knows everything', 'A narrator who lies deliberately', 'A narrator who addresses ‘you’']),
])
classify_templates(t42, VOICE_SNIP, VOICES, ['Which type of narrative voice is used here? {q}'],
                   C2frames=['This extract uses a {label}: {q} Explain the effect of this voice on the reader.'],
                   C3frames=[('Identify the narrative voice, explain how it is created, and rewrite the extract using a different voice: {q}',
                              lambda it: f'{cap(it[1])}: {it[2]} The rewrite should change perspective, vocabulary and attitude consistently.', lambda it, m: f'{upto(m)}: 1 for {it[1]}; 1 for how it is created; remaining mark(s) for a consistent rewrite in a new voice.')])
feature_templates(t42, VOICE_T.feats + AUNTIE.feats, NARR_POOL, c1=False)
t42.fixed('C2', (2, 3), [(f'In {T.label} the writer writes: {Q(q_)} {qq}', a, k) for T in (AUNTIE,) for q_, qq, a, k in T.infs])


@t42.add('C3', (2, 3, 4, 5), 'short')
def t42_voice(r, D):
    sit = r.choice(NEUTRAL_P)
    v = r.choice(VOICES[:4])
    m = mk('C3', D)
    return {'stem': f'Situation: {sit} Write the opening paragraph of this story using {an(v)}. Make the voice distinctive.',
            'answer': f'Any opening with a sustained {v}: consistent perspective, characteristic vocabulary and attitude, and details that reveal character.',
            'key': f'{upto(m)}: voice clearly a {v}; sustained and distinctive; character revealed through detail; accurate expression.'}


comp_templates(t42, [(f'Write a story in which the narrator is {who}.', NARR_IND + f' Narrator: {who}; voice distinctive and consistent.', f'Model approach: decide what {who} notices and misses; give them a characteristic way of speaking; let the reader infer more than the narrator says; end with a moment that reveals character.')
                     for who in ['a child who misunderstands what is happening around them', 'an old person looking back on one important day', 'someone who is not telling the whole truth', 'a person who has just moved to a new country',
                                 'a teenager who is trying very hard to appear calm', 'a shopkeeper who sees the same street every day']], 'narrative')

# ---------------------------------------------------------------- 4.3 tension, pace and suspense
TENSION = ['short sentences and fragments', 'delaying the outcome', 'withholding information', 'a ticking clock', 'focusing on small sensory details', 'foreshadowing']
TENSION_SNIP = [
    ('He ran. Left. Right. A dead end.', 'short sentences and fragments', 'the fragments speed up pace and mimic panic.'),
    ('She reached for the handle. Her fingers were cold. The metal was colder. Slowly – so slowly – she began to turn it.', 'delaying the outcome', 'stretching the moment makes the reader wait.'),
    ('Whatever was in the box, Dad said, we must never open it.', 'withholding information', 'the contents are hidden, creating mystery.'),
    ('The boat would leave at six. It was ten to, and we were still two kilometres away.', 'a ticking clock', 'a deadline creates urgency.'),
    ('A single bead of sweat ran down the guard’s neck and disappeared into his collar.', 'focusing on small sensory details', 'close focus slows time and heightens tension.'),
    ('If I had known then what the stranger wanted, I would never have opened the door.', 'foreshadowing', 'a hint of danger to come.'),
    ('The countdown on the screen read 00:47. Then 00:46.', 'a ticking clock', 'the visible countdown increases pressure.'),
    ('Nobody had ever explained why the third floor was locked.', 'withholding information', 'an unexplained mystery makes the reader curious.'),
]
FLAT_N = [
    ('I heard a noise downstairs. I went down and it was a burglar. I called the police and they came.',
     'Model: A sound. Downstairs. Not the cat – the cat was asleep on my feet. I counted to ten, slid out of bed and crept to the top of the stairs. The kitchen light was off. Something moved in the dark below.'),
    ('We were climbing the mountain and the weather got bad and we had to go down quickly.',
     'Model: At noon the sky was blue. By one, a grey wall had swallowed the summit. The wind found every gap in my jacket, and when Kofi shouted, the words were torn away before they reached me.'),
    ('The exam results came out. I opened the envelope and I had passed.',
     'Model: The envelope was thinner than I expected. Thin envelopes, everyone said, meant bad news. I slid my finger under the flap, stopped, and read the address again, as if it might belong to someone else.'),
    ('The car broke down in the desert. We waited and then a truck came and helped us.',
     'Model: The engine coughed twice and died. Silence rushed in. The fuel gauge read empty, the phone read no signal, and the road ran straight to the horizon in both directions, without a single moving thing.'),
]
t43 = topic('Building tension, pace and suspense', 'building tension pace and suspense')
t43.fixed('C1', (1, 2), [
    ('Which technique slows the pace at a climactic moment?', 'Focusing on small sensory details', 'Close detail stretches time and heightens tension.', ['Summarising the action in one sentence', 'Skipping to the next day', 'Adding a new character']),
    ('Which technique speeds up the pace?', 'A series of short sentences and fragments', 'Short units increase urgency.', ['Long descriptive paragraphs', 'Detailed flashbacks', 'Lists of adjectives']),
    ('What is suspense?', 'The anxious uncertainty a reader feels about what will happen', 'Created by danger, mystery and delay.', ['A type of punctuation', 'A happy ending', 'The title of a chapter']),
])
classify_templates(t43, TENSION_SNIP, TENSION, ['Which technique for building tension is used here? {q}'],
                   C2frames=['This extract uses {label}: {q} Explain how it builds suspense.'],
                   C3frames=[('Identify the technique, analyse its effect, and continue the extract for two or three sentences, maintaining the tension: {q}',
                              lambda it: f'{cap(it[1])}: {it[2]} Continuation should sustain the technique.', lambda it, m: f'{upto(m)}: 1 for {it[1]}; 1 for effect; remaining mark(s) for a continuation that sustains tension.')])
feature_templates(t43, LIFT.feats, NARR_POOL)
rewrite_templates(t43, [('Rewrite this flat narrative so that it builds tension and suspense.', a, b, 'Award for deliberate pacing (sentence length), withheld information, sensory focus and a moment of delay; accurate expression.') for a, b in FLAT_N],
                  ['{ins} {q}', '{q} {ins} Explain two techniques you used.'], D=(2, 3, 4, 5))
comp_templates(t43, [(f'Write a story called {Q(ti)} in which suspense builds to a dramatic climax.', NARR_IND + ' Tension built deliberately through pace, delay and withheld information.', 'Model approach: establish normality briefly; introduce a threat or deadline; tighten pace with shorter sentences; slow down at the climax with sensory detail; release tension in the resolution.')
                     for ti in ['The Lift', 'Ten Minutes', 'The Knock', 'Footsteps', 'The Crossing', 'Night Watch', 'The Signal', 'Missing']], 'narrative')
extended_templates(t43, [LIFT])

# ---------------------------------------------------------------- 4.4 dialogue
DIALOGUE_OK = [
    ("“Where are you going?” asked Mum.", ['“Where are you going,” asked Mum?', '“Where are you going?” Asked Mum.', 'Where are you going? asked Mum.']),
    ("“I can’t,” she whispered. “Not tonight.”", ['“I can’t” she whispered, “Not tonight.”', '“I can’t,” she whispered “not tonight”.', 'I can’t, she whispered. Not tonight.']),
    ("Leo shrugged. “It wasn’t my fault.”", ['Leo shrugged, “it wasn’t my fault.”', 'Leo shrugged. “It wasn’t my fault”.', 'Leo shrugged “It wasn’t my fault.”']),
    ("“Wait,” said Grandpa, “there’s something you should know.”", ['“Wait,” said Grandpa, “There’s something you should know.”', '“Wait” said Grandpa “there’s something you should know”.', '“Wait,” said Grandpa. “there’s something you should know.”']),
    ("“Run!” shouted Ama.", ['“Run”! shouted Ama.', '“Run!” Shouted Ama.', '“Run,” shouted Ama!']),
]
REPORTED = [
    ('Mum asked me where I had been and I said I had been at the library, but she did not believe me.', 'Model: “Where have you been?” Mum asked. “At the library,” I said. She folded her arms. “Really.”'),
    ('The coach told the team that they had played badly and that he was disappointed.', 'Model: The coach waited until the door closed. “That,” he said quietly, “was the worst half I have ever watched.”'),
    ('My friend said she was moving to Canada and I said I did not want her to go.', 'Model: “We’re moving,” she said. “To Canada.” I stared at her. “You can’t,” I said. “You just can’t.”'),
    ('The shopkeeper said the shop was closing and asked us to leave.', 'Model: “We’re closing,” the shopkeeper said, already turning the sign. “Out you go.”'),
]
SAID = [('said', ['muttered', 'snapped', 'whispered', 'insisted', 'pleaded'])]
t44 = topic('Writing effective dialogue within narrative', 'writing effective dialogue', 'dialogue within narrative')
t44.fixed('C1', (1, 2), [
    ('When does a new line (paragraph) begin in written dialogue?', 'Each time a different character speaks', 'New speaker, new line.', ['After every sentence', 'Only at the end of the conversation', 'Whenever a question is asked']),
    ('What is the main purpose of dialogue in a short story?', 'To reveal character and move the plot forward', 'Good dialogue does work; avoid small talk.', ['To fill space', 'To list facts', 'To describe the setting in detail']),
    ('What is subtext in dialogue?', 'The meaning beneath what characters actually say', 'E.g. ‘I suppose it has character’ really means ‘it is shabby’.', ['The speech tags', 'The punctuation', 'A footnote']),
    ('Why might a writer avoid too many adverbs in speech tags (e.g. ‘said angrily’)?', 'The words themselves and actions should show the emotion', 'Show tone through what is said and done.', ['Adverbs are grammatically wrong', 'Examiners do not read speech tags', 'Speech must have no tags']),
])


@t44.add('C1', (1, 2, 3))
def t44_punct(r, D):
    good, bad = r.choice(DIALOGUE_OK)
    opts, ans = mcq(r, good, bad)
    return {'stem': 'Which line of dialogue is correctly punctuated?', 'options': opts, 'answer': ans, 'key': f'{good} – punctuation inside the speech marks; capital letter for new speech; lower-case speech tag after a comma, question or exclamation mark.'}


feature_templates(t44, AUNTIE.feats + [Feat(AUNTIE, "'Tired?' said Auntie Grace, handing me a suitcase", 'dialogue', 'Tired?', 'echoing the mother’s word as a question shows Grace’s sharp, combative wit.')], NARR_POOL, c1=False)
t44.fixed('C2', (2, 3, 4), [(f'In {AUNTIE.label}: {Q(q_)} {qq}', a, k) for q_, qq, a, k in AUNTIE.infs] +
          [('Explain how dialogue can reveal a character’s personality more effectively than description.', 'The reader infers personality from how a character speaks (vocabulary, rhythm, what they avoid saying), which is more vivid and engaging than being told.', '1 mark: inference; 1 mark: example of a feature (vocabulary, subtext, rhythm).')])
rewrite_templates(t44, [('Rewrite this reported speech as direct dialogue that reveals the characters’ feelings. Punctuate it correctly.', a, b, 'Award for correct punctuation and layout; dialogue revealing character/subtext; a supporting action or gesture.') for a, b in REPORTED],
                  ['{ins} {q}'], D=(1, 2, 3, 4))
comp_templates(t44, [(f'Write a story in which most of the tension comes from a conversation between {who}.', NARR_IND + ' Dialogue punctuated accurately; each voice distinct; subtext and gesture used.', f'Model approach: establish setting briefly; let the conversation between {who} carry the conflict; use subtext, interruptions and silences; end on a line of dialogue or a telling action.')
                     for who in ['two siblings dividing their late grandmother’s belongings', 'a student and a teacher who suspects them of cheating', 'two old friends meeting after a long silence',
                                 'a parent and teenager on a long car journey', 'a job applicant and an interviewer who already know each other']], 'narrative')

# ---------------------------------------------------------------- 4.5 endings
ENDINGS = ['twist ending', 'circular ending', 'open ending', 'epiphany', 'resolved ending']
END_SNIP = [
    ('Then I locked the door – once – and walked down the hill towards the station, and I did not check it again.', 'epiphany', 'the narrator’s small act shows a new understanding about how to live.'),
    ('As the plane rose, she looked down and saw the house where she had been born, its light still on, exactly as it had been on the night she left.', 'circular ending', 'the final image returns to the opening setting.'),
    ('He reached for the phone. It rang once, twice. He did not answer.', 'open ending', 'the outcome is left uncertain for the reader to consider.'),
    ('The letter was signed in her own handwriting, dated twenty years in the future.', 'twist ending', 'a final revelation changes the meaning of the story.'),
    ('By spring the bridge was rebuilt, the market reopened, and Mrs Adu sold her first mangoes of the year to the same boy who had warned them of the flood.', 'resolved ending', 'the conflict is settled and loose ends tied up.'),
    ('Only then did I understand that my grandfather had never been lost at all; he had simply been going home.', 'epiphany', 'a sudden realisation reframes earlier events.'),
]
WEAK_END = [
    ('And then I woke up and it was all a dream.', 'cancels the story and cheats the reader’s investment', 'Model: replace with a resolution that follows from the events, e.g. a final image that shows how the character has changed.'),
    ('Suddenly a helicopter appeared and rescued everyone. The end.', 'a coincidence solves the problem (deus ex machina); no character agency', 'Model: let the character solve the problem through an earlier-planted skill or decision.'),
    ('Everyone lived happily ever after and nothing bad ever happened again.', 'cliché and unrealistic; ignores the conflict', 'Model: a quieter, specific ending that acknowledges what has been lost or learned.'),
    ('Then I went home and had dinner and went to bed.', 'anticlimactic routine; no significance', 'Model: end on an image or line that reflects the meaning of the day.'),
    ('In the end I realised that friendship is the most important thing in the world, and that is the moral of my story.', 'states the moral directly; tells rather than shows', 'Model: show the realisation through action, e.g. the narrator walking across to sit with the friend.'),
]
t45 = topic('Crafting endings with impact', 'crafting endings with impact', 'endings')
t45.fixed('C1', (1, 2), [
    ('What is an epiphany in a story?', 'A sudden moment of realisation or insight for a character', 'Often the turning point of a quiet ending.', ['A twist caused by a stranger', 'A happy coincidence', 'A long flashback']),
    ('Why is ‘it was all a dream’ usually a weak ending?', 'It cancels the events and the reader’s investment', 'Examiners see it as avoiding resolution.', ['Dreams cannot be described', 'It is too short', 'It must be written in the past tense']),
    ('What does an open ending do?', 'leaves some questions deliberately unanswered for the reader', 'Effective when it feels intentional, not unfinished.', ['tells the reader exactly what happens to every character', 'repeats the title', 'is always a twist']),
])
classify_templates(t45, END_SNIP, ENDINGS, ['What type of ending is this? {q}'],
                   C2frames=['This is an example of {label}: {q} Explain why it might be an effective way to end a story.'])
t45.fixed('C2', (2, 3), [(f'Explain why this ending is weak and how it could be improved: {Q(a)}', f'Weakness: {b}. {c}', '1 mark: identifies weakness; 1 mark: suggests a valid improvement.') for a, b, c in WEAK_END] + [(f'In {PHOTO.label}: {Q(q_)} {qq}', a, k) for q_, qq, a, k in PHOTO.infs])
rewrite_templates(t45, [('Rewrite this weak ending so that it has more impact.', a, c, f'Award for an ending that avoids the weakness ({b}), is earned by the story and leaves a strong final impression.') for a, b, c in WEAK_END], ['{ins} {q}'], D=(2, 3, 4, 5))
SUMMARIES = ['A girl has spent the story searching for her lost dog in a flooded town.', 'Two brothers have argued all day about selling their late father’s fishing boat.', 'A boy has secretly trained for months to enter a running race his parents forbade.',
             'An old woman has been visited by a stranger who claims to be her long-lost son.', 'A student has discovered that her best friend lied about a scholarship.']
comp_templates(t45, [(f'{s} Write the final section of this story ({e}), making sure the ending has impact.', NARR_IND + f' Ending type: {e}; earned by earlier events.', f'Model approach: bring the central conflict to a head; choose a {e}; end with an image or line that echoes the opening or theme.')
                     for s in SUMMARIES for e in ['an epiphany', 'a circular ending', 'an open ending']], 'narrative')
extended_templates(t45, [PHOTO])
CHAPTERS[4] = [t41, t42, t43, t44, t45]


# =========================================================== 5 Argumentative and discursive composition

ARG1 = Text('arg1', 'argument', 'an argumentative essay extract, ‘A Four-Day School Week’', """
Imagine waking up on a Friday with no alarm and a whole day to read, rest or help at home. A four-day school week is not
a fantasy; schools in several countries have trialled it. Supporters report better attendance, happier teachers and
lower running costs. Some will argue that students would simply lose a day of learning. But longer, better-planned days
can cover the same content, and the fifth day could be used for sport, volunteering or independent projects. Exhausted
students learn very little. Rested students learn a great deal. The question is not whether we can afford to change,
but whether we can afford not to.""")
ARG1.f('Imagine waking up on a Friday with no alarm and a whole day to read, rest or help at home.', 'imperative', 'Imagine', 'the command invites readers to picture the benefit personally, making the idea appealing.', also=('direct address', 'rule of three'))
ARG1.f('Some will argue that students would simply lose a day of learning. But longer, better-planned days can cover the same content', 'counter-argument', 'Some will argue', 'the objection is raised and rebutted, making the writer seem fair and confident.')
ARG1.f('Exhausted students learn very little. Rested students learn a great deal.', 'contrast', 'Exhausted students learn very little', 'the parallel short sentences set up a memorable contrast that makes the argument seem simple and obvious.', also=('repetition', 'short sentence'))
ARG1.f('The question is not whether we can afford to change, but whether we can afford not to.', 'repetition', 'can afford', 'the reversed phrase (antithesis) creates a powerful, quotable conclusion that turns the cost argument around.', also=('inclusive pronoun', 'contrast'))
ARG1.f('Supporters report better attendance, happier teachers and lower running costs.', 'rule of three', 'better attendance, happier teachers and lower running costs', 'three benefits give a sense of weight and completeness to the case.', also=('listing',))
ARG1.x('How does the writer try to persuade the reader to support a four-day school week?', 'Imperative hook; claim of trials as evidence (though vague); rule of three; counter-argument and rebuttal; contrasting short sentences; antithesis in the conclusion.')

DISC1 = Text('disc1', 'discursive', 'a discursive essay extract, ‘Is Social Media Good for Young People?’', """
Social media is now part of everyday life for most teenagers, and opinions about its effects are sharply divided. On the
one hand, it allows young people to stay in touch with friends, find communities that share their interests and
discover news and ideas from around the world. For a teenager who feels isolated, an online group can be a lifeline. On
the other hand, research has linked heavy use to poor sleep, anxiety and low self-esteem, particularly when users
compare themselves with carefully edited images. It is also difficult to judge which information is reliable. Perhaps
the most reasonable conclusion is that social media is neither simply good nor simply bad: what matters is how, and
how much, it is used.""")
DISC1.f('On the one hand, it allows young people to stay in touch with friends', 'counter-argument', 'On the one hand', 'the discourse marker signals the first side of a balanced discussion.')
DISC1.f('For a teenager who feels isolated, an online group can be a lifeline.', 'metaphor', 'a lifeline', 'the image suggests online communities can rescue lonely young people, giving emotional weight to the positive side.')
DISC1.f('research has linked heavy use to poor sleep, anxiety and low self-esteem', 'expert opinion', 'research has linked', 'reference to research gives authority to the concerns, although no specific study is named.', also=('listing', 'rule of three'))
DISC1.f('social media is neither simply good nor simply bad: what matters is how, and how much, it is used', 'contrast', 'neither simply good nor simply bad', 'the balanced conclusion rejects extremes and offers a nuanced judgement.')
DISC1.x('How does the writer present a balanced discussion of social media?', 'Neutral opening; signposting (On the one hand / On the other hand); evidence on both sides; measured tone; nuanced conclusion with a colon introducing the key judgement.')

ARG2 = Text('arg2', 'argument', 'an argumentative essay extract, ‘Ban Cars from the City Centre’', """
Every morning, the same scene: engines idling, horns blaring, a grey haze hanging over the square. Our city centre has
become a car park with shops attached. Air pollution is linked to millions of early deaths worldwide each year, and
children, who breathe faster and walk closer to exhaust pipes, are among the most vulnerable. Cities that have
pedestrianised their centres have often seen footfall rise rather than fall. Of course, deliveries and disabled access
must be protected, and they can be, through permits and timed access. But the principle is clear. Streets should belong
to people, not to traffic.""")
ARG2.f('Every morning, the same scene: engines idling, horns blaring, a grey haze hanging over the square.', 'listing', 'engines idling, horns blaring, a grey haze', 'the list of images creates a vivid, unpleasant picture to hook the reader.', also=('sensory imagery', 'rule of three', 'onomatopoeia'))
ARG2.f('Our city centre has become a car park with shops attached.', 'metaphor', 'a car park with shops attached', 'the reversed priorities in the image mock the dominance of cars and make the problem memorable.', also=('hyperbole',))
ARG2.f('Air pollution is linked to millions of early deaths worldwide each year', 'statistic', 'millions of early deaths', 'a large figure lends seriousness and urgency, though it is not specific to this city.')
ARG2.f('Of course, deliveries and disabled access must be protected, and they can be, through permits and timed access.', 'counter-argument', 'Of course', 'conceding practical concerns and offering solutions makes the argument appear reasonable.')
ARG2.f('Streets should belong to people, not to traffic.', 'contrast', 'people, not to traffic', 'the short, balanced final sentence states the principle memorably.', also=('short sentence',))
ARG2.x('How does the writer build a persuasive argument for banning cars?', 'Vivid opening; witty metaphor; statistic and concern for children; evidence from other cities (vague); concession with solutions; short, principled conclusion.')
ARG_TEXTS = [ARG1, DISC1, ARG2]

ARG_TITLES = ['‘Schools should abolish homework.’', '‘Tourism does more harm than good.’', '‘Every young person should do a year of community service.’', '‘Technology has made us lonelier.’',
              '‘Zoos have no place in the modern world.’', '‘Exams are not a fair way to measure ability.’', '‘Cities should ban cars from their centres.’', '‘Professional athletes are paid too much.’',
              '‘Space exploration is a waste of money.’', '‘Fast fashion should be banned.’', '‘Children should be taught to cook at school.’', '‘Celebrities have a responsibility to be role models.’']
ARG_IND = 'clear, consistent stance; developed reasons with evidence and examples; rhetorical devices used with control; counter-arguments anticipated and rebutted; cohesive paragraphing; persuasive conclusion.'
DISC_IND = 'balanced exploration of both sides with evidence; points weighed and evaluated; measured, objective tone; discourse markers for structure; reasoned judgement in the conclusion.'

# ---------------------------------------------------------------- 5.1 argumentative vs discursive
STANCE = ['argumentative', 'discursive', 'informative', 'narrative']
STANCE_SNIP = [
    ('There can be no doubt: homework is damaging the health of a generation, and it must end.', 'argumentative', 'a single, forceful stance is asserted.'),
    ('There are strong arguments on both sides of the homework debate, and each deserves careful consideration.', 'discursive', 'signals a balanced exploration.'),
    ('Homework was introduced in many countries in the nineteenth century and is now set in most secondary schools.', 'informative', 'presents facts without taking a side.'),
    ('The night before the deadline, Leila stared at her unfinished homework and felt the panic rise.', 'narrative', 'tells a story about a character.'),
    ('Some argue that zoos protect endangered species; others believe they cause unnecessary suffering.', 'discursive', 'presents opposing views neutrally.'),
    ('Zoos are prisons, and it is time we had the courage to close them.', 'argumentative', 'one-sided and persuasive.'),
    ('While tourism brings income, it also places pressure on housing and the environment, so its value depends on how it is managed.', 'discursive', 'weighs both sides and reaches a qualified view.'),
    ('Tourism is the single greatest threat to our island’s future.', 'argumentative', 'a strong, one-sided claim.'),
]
CONVERT = [
    ('Fast fashion is a disaster that should be banned immediately.', 'Model (discursive): Fast fashion makes clothes affordable for many families; however, critics argue that it creates waste and relies on poorly paid workers.'),
    ('Video games rot the brain and waste young people’s time.', 'Model (discursive): Some studies suggest video games can improve problem-solving, while others link excessive gaming to poor sleep and reduced activity.'),
    ('Uniforms are the best way to create equality in schools.', 'Model (discursive): Supporters say uniforms reduce pressure to wear expensive clothes, but opponents argue that they limit self-expression and can be costly.'),
    ('Space exploration is humanity’s greatest achievement and deserves unlimited funding.', 'Model (discursive): Space programmes have produced useful technologies, yet many argue that the money could address urgent problems on Earth.'),
    ('Online learning is far better than classroom teaching.', 'Model (discursive): Online learning offers flexibility and access to resources, although many students miss the support and social contact of a classroom.'),
]
t51 = topic('Argumentative vs discursive writing: purpose and stance', 'argumentative vs discursive writing', 'purpose and stance')
t51.fixed('C1', (1, 2), [
    ('What is the main purpose of an argumentative composition?', 'To persuade the reader to accept a particular point of view', 'Argumentative = one clear stance throughout.', ['To present both sides equally without judgement', 'To tell a story', 'To describe a place']),
    ('What is the main purpose of a discursive composition?', 'To explore different views on an issue in a balanced way before reaching a reasoned conclusion', 'Discursive = balanced exploration.', ['To argue only one side', 'To entertain with a narrative', 'To list facts with no conclusion']),
    ('Which tone is most appropriate for a discursive essay?', 'Measured and objective', 'Discursive writing weighs evidence calmly.', ['Angry and one-sided', 'Comic and exaggerated', 'Informal and chatty']),
    ('In an argumentative essay, how should counter-arguments be used?', 'Raised and then rebutted to strengthen your own case', 'Rebuttal shows awareness and confidence.', ['Ignored completely', 'Accepted as correct', 'Placed only in the title']),
])
classify_templates(t51, STANCE_SNIP, STANCE, ['Is this opening most typical of argumentative, discursive, informative or narrative writing? {q}'],
                   C2frames=['This sentence is {label}: {q} Explain how its stance and tone show this.'])
rewrite_templates(t51, [('Rewrite this one-sided claim as a balanced sentence suitable for a discursive essay.', a, b, 'Award for presenting more than one view, measured tone and a discourse marker of contrast.') for a, b in CONVERT],
                  ['{ins} {q}'], D=(1, 2, 3, 4))


@t51.add('C3', (2, 3, 4, 5), 'short')
def t51_stance(r, D):
    ti = r.choice(ARG_TITLES)
    m = mk('C3', D)
    return {'stem': f'For the statement {ti}, write two short opening paragraphs: one for an argumentative essay and one for a discursive essay. Then explain the key difference in purpose and stance.',
            'answer': 'Model: the argumentative opening states a clear position forcefully (with a hook); the discursive opening introduces the debate and signals that both sides will be weighed. Difference: persuasion versus balanced exploration.',
            'key': f'{upto(m)}: clear stance in the argumentative opening; balance signalled in the discursive opening; appropriate tone for each; accurate explanation of the difference.'}


comp_templates(t51, [(f'{ti} Write an argumentative essay giving your views.', ARG_IND, 'Model approach: hook; clear stance; three developed reasons with evidence; counter-argument rebutted; forceful conclusion.') for ti in ARG_TITLES[:6]], 'argument')
comp_templates(t51, [(f'{ti} Write a discursive essay exploring different views on this statement.', DISC_IND, 'Model approach: introduce the debate; arguments for with evidence; arguments against with evidence; weigh the strongest points; reasoned conclusion.') for ti in ARG_TITLES[6:]], 'discursive')

# ---------------------------------------------------------------- 5.2 persuasive argument with evidence and devices
WEAK_CLAIM = [
    ('Homework is bad.', 'Model: Homework set late at night competes with sleep; when students lose sleep, their memory and concentration suffer, so excessive homework can undermine the learning it is meant to support.'),
    ('Fast fashion harms the planet.', 'Model: Cheap clothing encourages people to buy and discard garments quickly; the textile industry uses vast amounts of water and many items end up in landfill within a year.'),
    ('Sport is good for teenagers.', 'Model: Regular sport improves physical health, but it also teaches teamwork and resilience: a teenager who learns to lose gracefully on the pitch is better prepared for setbacks in life.'),
    ('Tourism helps poor communities.', 'Model: Where tourism income is spent locally – on guesthouses, guides and markets – it can fund schools and clinics, as visitors pay directly for local skills.'),
    ('Reading is important.', 'Model: Reading widely builds vocabulary and empathy; a novel lets us live briefly inside another person’s mind, which few other activities can do.'),
    ('Cars should be banned from city centres.', 'Model: Removing cars from city centres would cut pollution where people gather most, make streets safer for children and free space for trees, seating and markets.'),
]
EVIDENCE = ['statistic', 'expert opinion', 'anecdote', 'example from another place', 'logical reasoning']
EVID_SNIP = [
    ('In a survey of 500 students, 68% said they slept less than eight hours on school nights.', 'statistic', 'precise numbers give weight to the claim.'),
    ('According to a sleep scientist at a national university, teenagers’ body clocks shift later during puberty.', 'expert opinion', 'authority supports the claim.'),
    ('My cousin worked twenty hours a week in a shop and her grades suffered.', 'anecdote', 'a personal story adds human interest but is weak as proof.'),
    ('When Pontevedra in Spain removed most cars from its centre, the streets became busier with pedestrians.', 'example from another place', 'a real-world precedent suggests the idea can work.'),
    ('If students are exhausted, they cannot concentrate; if they cannot concentrate, they cannot learn.', 'logical reasoning', 'a chain of cause and effect makes the conclusion seem inevitable.'),
    ('Three out of four doctors surveyed recommended more outdoor exercise for children.', 'statistic', 'a figure from professionals strengthens the claim.'),
]
t52 = topic('Building a persuasive argument with evidence and rhetorical devices', 'building a persuasive argument', 'evidence and rhetorical devices')
t52.fixed('C1', (1, 2), [
    ('What is a rhetorical device?', 'A technique of language used to persuade or impress an audience', 'E.g. rhetorical questions, tricolon, antithesis, anaphora.', ['A type of evidence', 'A grammatical error', 'A paragraph break']),
    ('What is antithesis?', 'Placing contrasting ideas side by side in a balanced structure', 'E.g. ‘Exhausted students learn very little. Rested students learn a great deal.’', ['Repeating a word at the start of each line', 'Asking a question', 'An exaggeration']),
    ('What is anaphora?', 'Repetition of a word or phrase at the start of successive clauses', 'E.g. ‘We will … We will … We will …’', ['A list of three', 'A rhyme', 'A counter-argument']),
    ('Which type of evidence is generally most convincing in an argument?', 'Specific, reliable data from a named source', 'Precise, credible evidence persuades best; anecdotes are weaker.', ['A vague claim that ‘everyone knows’', 'A single personal story', 'An emotional exclamation']),
])
classify_templates(t52, EVID_SNIP, EVIDENCE, ['Which type of evidence is used here? {q}'],
                   C2frames=['This argument uses {label}: {q} Explain how convincing this type of evidence is.'])
feature_templates(t52, ARG1.feats + ARG2.feats, ['imperative', 'counter-argument', 'contrast', 'repetition', 'rule of three', 'listing', 'metaphor', 'statistic', 'rhetorical question', 'emotive language', 'hyperbole'])
rewrite_templates(t52, [('Develop this undeveloped claim into a persuasive point with a reason, evidence or example and an explanation.', a, b, 'Award for a clear reason, specific evidence or example, explanation of why it matters, and controlled persuasive language.') for a, b in WEAK_CLAIM],
                  ['{ins} {q}', 'A student writes: {q} {ins}'], D=(2, 3, 4, 5))
comp_templates(t52, [(f'{ti} Write an argumentative essay in which you persuade the reader to agree with you. Use a range of evidence and rhetorical devices.', ARG_IND, 'Model approach: rhetorical hook; clear thesis; each paragraph a point + evidence + explanation; devices such as antithesis and tricolon used sparingly; rebuttal; memorable final line.')
                     for ti in ARG_TITLES], 'argument')
extended_templates(t52, [ARG1, ARG2])

# ---------------------------------------------------------------- 5.3 balanced discursive essay
DISC_TOPICS = [('school uniforms', 'equality, identity, lower peer pressure', 'cost, self-expression, comfort'), ('banning mobile phones in schools', 'concentration, less cyberbullying', 'safety, learning tools, independence'),
               ('a four-day school week', 'rest, attendance, lower costs', 'childcare, lost learning, longer days'), ('tourism in fragile places', 'income, jobs, cultural exchange', 'damage, rising rents, overcrowding'),
               ('zoos', 'conservation, education, research', 'stress, small enclosures, money could protect habitats'), ('online learning', 'flexibility, access, self-paced', 'isolation, screen time, unequal internet access'),
               ('part-time jobs for teenagers', 'skills, money, independence', 'tiredness, grades, exploitation'), ('space exploration', 'technology, knowledge, inspiration', 'cost, urgent problems on Earth')]
t53 = topic('Writing a balanced discursive essay', 'balanced discursive essay', 'weighing both sides')
t53.fixed('C1', (1, 2), [
    ('Which discourse marker best introduces the second side of a discursive essay?', 'On the other hand', 'It signals a shift to the opposing view.', ['Furthermore', 'For instance', 'Similarly']),
    ('Where should the writer’s own judgement appear in a discursive essay?', 'In the conclusion, after weighing both sides', 'Discursive essays build towards a reasoned view.', ['In the first sentence only', 'Nowhere at all', 'In every paragraph as a strong opinion']),
    ('What does it mean to ‘weigh’ arguments?', 'Judge which points are stronger and why', 'Evaluation distinguishes high-level discursive writing.', ['Count the number of arguments', 'Repeat every point twice', 'Choose the longest paragraph']),
])
t53.fixed('C2', (2, 3, 4), [(f'Read {DISC1.label}: {Q(DISC1.text)} {qq}', a, k) for qq, a, k in [
    ('Explain how the writer signals a balanced structure.', 'Discourse markers ‘On the one hand’ and ‘On the other hand’ divide the two sides; the conclusion begins ‘Perhaps the most reasonable conclusion’, signalling evaluation.', '1 mark: discourse markers; 1 mark: evaluative conclusion; a further mark for reference to tone.'),
    ('Explain why the conclusion is effective for a discursive essay.', 'It rejects both extremes and offers a nuanced judgement (how and how much social media is used), which follows logically from the balanced discussion.', '1 mark: nuance/qualified judgement; 1 mark: follows from both sides.'),
    ('How could the writer make the evidence more convincing?', 'By naming specific studies, giving figures or examples, and showing how reliable each source is.', '1 mark: specificity; 1 mark: source reliability.'),
]])


@t53.add('C3', (2, 3, 4, 5), 'short')
def t53_plan(r, D):
    tp, pro, con = r.choice(DISC_TOPICS)
    m = mk('C3', D)
    return {'stem': f'Plan a discursive essay on {tp}. Give two developed points for, two against, and a one-sentence conclusion that weighs them.',
            'answer': f'Model: For – {pro}; Against – {con}; Conclusion – a qualified judgement explaining which points carry most weight and why.',
            'key': f'{upto(m)}: two points for with development; two against with development; conclusion that weighs rather than repeats.'}


@t53.add('C3', (2, 3, 4, 5), 'short')
def t53_para(r, D):
    tp, pro, con = r.choice(DISC_TOPICS)
    m = mk('C3', D)
    return {'stem': f'Write the paragraph of a discursive essay on {tp} that moves from the arguments in favour ({pro}) to the arguments against ({con}). Use at least two discourse markers.',
            'answer': 'Model: a topic sentence summarising the case for; a turn with ‘However’/‘On the other hand’; development of one or two arguments against with evidence; a linking sentence that prepares for evaluation.',
            'key': f'{upto(m)}: clear transition; arguments on both sides developed; discourse markers used accurately; measured tone.'}


comp_templates(t53, [(f'Write a discursive essay on {tp}, considering arguments for and against before reaching a conclusion.', DISC_IND + f' For: {pro}. Against: {con}.', f'Model approach: introduction framing the debate on {tp}; paragraph(s) for ({pro}); paragraph(s) against ({con}); evaluation; reasoned conclusion.')
                     for tp, pro, con in DISC_TOPICS], 'discursive')

# ---------------------------------------------------------------- 5.4 counter-argument, rebuttal and conclusions
REBUT = [
    ('Uniforms stop students expressing themselves.', 'Admittedly, uniforms limit choice of clothing; however, self-expression is not only about clothes – students express themselves through their ideas, work and activities, and uniforms reduce costly peer pressure.'),
    ('Banning cars will ruin local businesses.', 'Some traders fear fewer customers; yet evidence from pedestrianised centres suggests that people on foot visit more often and stay longer, and delivery permits can protect business access.'),
    ('A four-day week means less learning.', 'It may seem that removing a day reduces learning, but longer, better-structured days can cover the same content, and rested students learn more effectively.'),
    ('Zoos are necessary to save endangered species.', 'While some breeding programmes are successful, only a minority of zoo species are part of them; conservation funding could achieve more by protecting habitats directly.'),
    ('Homework teaches independence.', 'Independence matters, but it can be developed through projects in school time; excessive homework often teaches stress rather than self-discipline.'),
    ('Tourism creates jobs.', 'Tourism does create jobs, but many are seasonal and low-paid, and profits often go to companies abroad; the benefit depends on how tourism is managed.'),
]
CONCLUSIONS = [
    ('So that is why I think homework should be banned. Thank you for reading.', 'Model: Homework was meant to extend learning; too often it now replaces sleep, rest and family time. It is time to set less, and to set it better.', 'merely restates and adds an informal sign-off; no final impact.'),
    ('In conclusion, there are good and bad points.', 'Model: On balance, the benefits of tourism can outweigh its costs – but only if islanders, not cruise companies, decide how many visitors arrive.', 'vague; no judgement or weighing.'),
    ('To conclude, I have said that cars are bad, pollution is bad and parking is bad.', 'Model: A city centre should be a place to meet, not a place to queue. Removing cars is not an attack on drivers; it is an invitation to everyone else.', 'repetitive list of points; no development or memorable close.'),
    ('In conclusion, also another reason is that zoos are expensive.', 'Model: Zoos can still play a role, but only as sanctuaries for species that truly need them – anything more is entertainment dressed as conservation.', 'introduces a new point instead of concluding.'),
]
t54 = topic('Counter-argument, rebuttal and persuasive conclusions', 'counter-argument rebuttal', 'persuasive conclusions')
t54.fixed('C1', (1, 2), [
    ('What is the purpose of a rebuttal?', 'To show why an opposing argument is weak or less important', 'Rebuttal turns a counter-argument to your advantage.', ['To agree completely with the opposition', 'To introduce the topic', 'To summarise the essay']),
    ('Which phrase best introduces a concession before a rebuttal?', 'Admittedly,', 'Concede, then rebut: ‘Admittedly… however…’.', ['Furthermore,', 'Firstly,', 'For example,']),
    ('What should a strong conclusion avoid?', 'Introducing a completely new argument', 'Conclusions should draw together and leave a lasting impression.', ['Restating the main stance', 'A memorable final sentence', 'A call to action']),
    ('Which ending is most likely to leave a lasting impression?', 'A concise, memorable final sentence linked to the opening idea', 'Echoing the hook can give a satisfying close.', ['Thank you for reading my essay', 'That is all I have to say', 'The end']),
])


@t54.add('C3', (2, 3, 4, 5), 'short')
def t54_rebut(r, D):
    c, model = r.choice(REBUT)
    m = mk('C3', D)
    return {'stem': f'Opponents argue: {Q(c)} Write a paragraph that concedes any valid part of this argument and then rebuts it convincingly.', 'answer': f'Model: {model}',
            'key': f'{upto(m)}: fair statement of the counter-argument; concession marker; rebuttal with reason or evidence; controlled, persuasive tone.'}


t54.fixed('C2', (2, 3, 4), [(f'Explain why this conclusion is weak and how it could be improved: {Q(a)}', f'Weakness: {w} {b}', '1 mark: identifies the weakness; 1 mark: specific improvement; a further mark for linking to impact on the reader.') for a, b, w in CONCLUSIONS])
@t54.add('C2', (1, 2), 'explain')
def t54_weak1(r, D):
    a, b, w = r.choice(CONCLUSIONS)
    m = mk('C2', D)
    return {'stem': f'A student ends an argumentative essay with this sentence: {Q(a)} Explain what makes it an ineffective conclusion.', 'answer': cap(w),
            'key': f'{upto(m)}: identifies the weakness ({w.rstrip(".")}); explains its effect on the reader’s final impression.'}


rewrite_templates(t54, [('Rewrite this conclusion so that it is persuasive and memorable.', a, b, f'Award for a clear final judgement, a link to the essay’s main idea and a memorable final sentence; the original was {w}') for a, b, w in CONCLUSIONS], ['{ins} {q}'], D=(2, 3, 4, 5))
comp_templates(t54, [(f'{ti} Write an argumentative essay. Include at least two counter-arguments, each followed by a rebuttal, and end with a persuasive conclusion.', ARG_IND + ' Counter-arguments fairly stated and convincingly rebutted; conclusion memorable.', 'Model approach: thesis; strongest reason; counter-argument 1 + rebuttal; second reason; counter-argument 2 + rebuttal; conclusion echoing the hook.')
                     for ti in ARG_TITLES], 'argument')
compose_templates(t54, ARG_TEXTS, C=('C4',))
CHAPTERS[5] = [t51, t52, t53, t54]


settle_fixed_marks(CHAPTERS)
