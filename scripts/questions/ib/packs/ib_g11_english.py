"""IB DP English A: Language and Literature SL/HL (first assessment 2021) – ib-g11-english (DP year 1).

Areas of exploration: Readers, writers and texts; Time and space (year 1); Intertextuality (year 2).
Seven course concepts: identity, culture, creativity, communication, perspective, transformation,
representation. Assessment: Paper 1 guided textual analysis (SL 1 h 15, one unseen non-literary
passage, 20 marks; HL 2 h 15, two passages, 40 marks), Paper 2 comparative essay (1 h 45, 30 marks),
Individual Oral (15 min, 40 marks), HL essay (1,200–1,500 words, 20 marks).

Item styles
  * C1 – terminology and course knowledge (define / identify / state, MCQs on devices, tone, text type),
  * C2 – explain / distinguish / correct a misconception about how texts make meaning,
  * C3 – reading, inference and writer's-effects questions on ORIGINAL short passages written for this
    bank (advertisements, speeches, columns, blogs, letters, infographics and cartoons described in words,
    poems, prose and drama extracts); a few brief public-domain quotations (Shakespeare, Owen, Dickinson,
    Verlaine, Lange's FSA caption) are quoted and attributed,
  * C4 – guided-analysis paragraphs and essays, evaluation, directed writing and composition, keyed to
    the IB markbands (criteria A–D).
Set texts are referred to only in general terms.
"""
from __future__ import annotations

from _common import F, Registry, T, mcq, name, two_names

CONFIG = {'minutesPerMark': 2.5, 'mcqMinutes': 1.5}

# One mock = HL Paper 1 (two unseen non-literary texts, 20 marks each) + Paper 2 (30 marks) split into
# planning (2 x 5) and comparative analysis (2 x 10). 6 items, 70 marks per mock.
MOCK = [
    dict(section='Paper 1 – Guided textual analysis, Text 1 (criteria A–D)', count=1, c=['C4'], d=[4, 5], type='long', marks=20, style='p1', chapters=[11, 12]),
    dict(section='Paper 1 (HL) – Guided textual analysis, Text 2 (criteria A–D)', count=1, c=['C4'], d=[5, 4], type='long', marks=20, style='p1', chapters=[2, 3, 11, 12]),
    dict(section='Paper 2 – Comparative essay part A: unpacking the question and comparative thesis', count=2, c=['C3', 'C4'], d=[3, 4], type='case', marks=5, style='p2a', chapters=[4, 5, 7, 8]),
    dict(section='Paper 2 – Comparative essay part B: comparative analysis of two literary works', count=2, c=['C4'], d=[4, 5], type='long', marks=10, style='p2b', chapters=[4, 5, 7, 8]),
]

R = Registry()

MARKBAND = ('Markbands (criteria A–D). A Knowledge, understanding and interpretation; B Analysis and evaluation of '
            'authorial choices; C Focus and organisation; D Language. Top band: an insightful, convincing interpretation '
            'supported by well-chosen references; perceptive analysis of how specific choices shape meaning and affect the '
            'audience; a sustained, coherent line of argument; precise, varied, register-appropriate academic language. '
            'Middle band: relevant interpretation and some analysis, but partly descriptive or unevenly supported. '
            'Low band: mostly summary or feature-spotting without effect.')
STYLE = {'eval_marks': 10, 'essay_marks': 15, 'markband': MARKBAND}

P1_BANDS = ('Paper 1 criteria (5 marks each, 20 total). A Understanding and interpretation: grasp of the literal and '
            'implied meaning, references well chosen. B Analysis and evaluation: how textual features and authorial '
            'choices shape meaning, with evaluation of their effect. C Focus and organisation: a clear line of argument '
            'that answers the guiding question (or a chosen focus) and is developed coherently. D Language: clear, '
            'precise, varied academic register and accurate terminology. 5 = excellent, 3 = adequate, 1 = minimal.')
P2_BANDS = ('Paper 2 criteria (30 total: A 10, B 10, C 5, D 5), scaled to this part. A Knowledge, understanding and '
            'interpretation of both works in relation to the question; B Analysis and evaluation of how authorial '
            'choices in each work create meaning, with comparison and contrast; C Focus and organisation – a balanced, '
            'integrated comparison rather than two separate essays; D Language – precise academic register.')
CRIT_B = ('Award marks for: an accurate identification of the feature, a precise reference to the text, and an explanation '
          'of its effect on the intended audience linked to purpose (criterion B). Identification without effect: half marks at most.')
CRIT_A = ('Award marks for an accurate, specific point (criterion A: understanding and interpretation) supported by a '
          'reference to the text; a general assertion without evidence earns at most 1 mark.')

KIND = {
    'ad': 'advertisement', 'speech': 'speech', 'oped': 'opinion column', 'blog': 'blog post', 'letter': 'letter',
    'infographic': 'infographic', 'website': 'web page', 'social': 'social media post', 'news': 'news report',
    'cartoon': 'cartoon', 'brochure': 'travel brochure', 'propaganda': 'propaganda poster', 'photo': 'documentary photograph',
    'prose': 'prose fiction extract', 'poem': 'poem', 'drama': 'drama extract', 'trans': 'extract in translation',
    'meme': 'meme', 'review': 'review', 'satire': 'satirical column', 'parody': 'parody advertisement',
    'campaign': 'campaign poster', 'appeal': 'charity appeal', 'manifesto': 'manifesto', 'script': 'screenplay extract',
    'graphic': 'graphic novel page', 'memoir': 'memoir extract', 'fanfic': 'fan fiction extract', 'story': 'short story extract',
}
KIND_CONV = {
    'ad': 'a headline or slogan, an image, a brand name or logo, persuasive copy and a call to action',
    'speech': 'direct address to a live audience, rhetorical devices for the ear (repetition, tricolon, antithesis) and a memorable close',
    'oped': 'a by-lined, first-person argument on a topical issue, a hook, evidence and anecdote, concession and a clear stance',
    'blog': 'a personal, informal voice, a date or title, chronological or reflective entries, hashtags or links and reader interaction',
    'letter': 'a salutation and sign-off, a named addressee, a clearly stated purpose and a request or demand',
    'infographic': 'a headline, data presented visually (icons, charts, scale), minimal text and a source or call to action',
    'website': 'navigation menus, banners, hyperlinks and buttons, scrolling layout and interactive elements',
    'social': 'brevity, informal register, hashtags, emoji, handles, likes and shares that signal an audience',
    'news': 'a headline and standfirst, the inverted pyramid, attributed quotations and an apparently neutral third-person voice',
    'cartoon': 'a single image or panels, caricature, captions or speech bubbles and visual exaggeration for comment',
    'brochure': 'evocative headings, sensory description, imperatives inviting the reader, images and practical details',
    'propaganda': 'a bold slogan, symbolic imagery, emotive appeals to duty or fear and an instruction to the public',
    'photo': 'framing, composition, lighting and focus, a caption that anchors meaning, and a documentary claim to truth',
    'prose': 'a narrator, characters, setting, plot and narrative time, conveyed through description and dialogue',
    'poem': 'lineation, stanza form, imagery, sound patterning and a speaker',
    'drama': 'dialogue, stage directions, characters in conflict and the expectation of performance before an audience',
    'trans': 'a source text rendered in another language, with the translator\'s choices sometimes visible in notes',
    'meme': 'a recognisable image template, top and bottom text, in-group humour and rapid remixing',
    'review': 'an evaluative judgement, a rating, a summary of the product or work and a recommendation',
    'satire': 'an ironic persona, exaggeration and mock-seriousness used to criticise a target',
    'parody': 'imitation of a recognisable genre or brand, exaggerated so that the original is criticised',
    'campaign': 'a slogan, a striking image, a call to action and the logo of the organisation',
    'appeal': 'a case study or named individual, emotive images, statistics and a donation request',
    'manifesto': 'a collective "we" voice, declarations of belief, numbered demands and a call to join',
    'script': 'scene headings, action lines, character cues and dialogue, written for the camera',
    'graphic': 'panels, gutters, captions, speech balloons and the interplay of word and image',
    'memoir': 'a first-person retrospective narrator, real events shaped by memory and reflection',
    'fanfic': 'borrowed characters or worlds from a source text, new scenarios and a fan community readership',
    'story': 'compression, a small cast, a single situation and often an epiphany or open ending',
}
KIND_WRONG = {
    'ad': ['news report', 'open letter', 'short story extract'], 'speech': ['infographic', 'news report', 'travel brochure'],
    'oped': ['advertisement', 'news report', 'infographic'], 'blog': ['news report', 'speech', 'infographic'],
    'letter': ['advertisement', 'infographic', 'poem'], 'infographic': ['speech', 'blog post', 'letter'],
    'website': ['speech', 'letter', 'poem'], 'social': ['news report', 'speech', 'travel brochure'],
    'news': ['advertisement', 'blog post', 'poem'], 'cartoon': ['speech', 'news report', 'letter'],
    'brochure': ['news report', 'letter', 'speech'], 'propaganda': ['news report', 'blog post', 'letter'],
    'photo': ['speech', 'blog post', 'letter'], 'prose': ['speech', 'advertisement', 'news report'],
    'poem': ['news report', 'advertisement', 'letter'], 'drama': ['news report', 'blog post', 'advertisement'],
    'meme': ['news report', 'speech', 'letter'], 'review': ['speech', 'poem', 'news report'],
    'satire': ['news report', 'advertisement', 'poem'], 'parody': ['news report', 'speech', 'poem'],
    'campaign': ['short story extract', 'letter', 'speech'], 'appeal': ['poem', 'news report', 'review'],
    'manifesto': ['advertisement', 'poem', 'review'], 'script': ['news report', 'advertisement', 'letter'],
    'graphic': ['speech', 'letter', 'news report'], 'memoir': ['advertisement', 'news report', 'speech'],
    'fanfic': ['news report', 'advertisement', 'speech'], 'story': ['advertisement', 'news report', 'speech'],
    'trans': ['advertisement', 'news report', 'speech'],
}
NONLIT = {'ad', 'speech', 'oped', 'blog', 'letter', 'infographic', 'website', 'social', 'news', 'cartoon', 'brochure',
          'propaganda', 'photo', 'meme', 'review', 'satire', 'parody', 'campaign', 'appeal', 'manifesto'}
LIT = {'prose', 'poem', 'drama', 'trans', 'story', 'memoir', 'graphic', 'fanfic', 'script'}
VISUAL = {'ad', 'infographic', 'website', 'cartoon', 'propaganda', 'photo', 'meme', 'campaign', 'parody', 'appeal', 'graphic'}

PASS: list[dict] = []


def P(**kw):
    """One original study passage with its annotation (answers for every question frame)."""
    kw.setdefault('dev', [])
    kw.setdefault('struct', [])
    PASS.append(kw)
    return kw


def label(p):
    return KIND[p['kind']]


def intro(p, neutral=False):
    if neutral:
        return f'Read the following text.\n\n{p["text"]}'
    return f'Read the following {p["title"]}.\n\n{p["text"]}'


def _get(p, note, rng):
    """Return (format-dict, answer) for a note on passage p, or None."""
    if note in ('dev', 'struct'):
        if not p.get(note):
            return None
        e = rng.choice(p[note])
        if note == 'dev':
            return dict(device=e[0], quote=e[1]), f'{e[0][0].upper() + e[0][1:]}: "{e[1]}" – {e[2]}.'
        return dict(feature=e[0]), f'{e[0][0].upper() + e[0][1:]}: {e[1]}.'
    if note == 'concept':
        c = p.get('concept')
        return (dict(cname=c[0]), f'{c[0][0].upper() + c[0][1:]}: {c[1]}') if c else None
    if note == 'kconv':
        ex = []
        if p.get('dev'):
            d0 = rng.choice(p['dev'])
            ex.append(f'"{d0[1]}" ({d0[0]})')
        if p.get('struct'):
            ex.append(p['struct'][0][0])
        exs = ' and '.join(ex) if ex else 'the layout shown'
        return dict(), f'It is a {label(p)}. Conventions: {KIND_CONV[p["kind"]]}. In this text, for example: {exs}, each used to serve the text\'s purpose for its audience.'
    if isinstance(note, tuple):
        parts = [p.get(n) for n in note]
        if not all(parts):
            return None
        return dict(), ' '.join((x[0].upper() + x[1:]).rstrip('.') + '.' for x in parts)
    v = p.get(note)
    if not v:
        return None
    if note in ('purp', 'issue') and p.get('dev'):
        d0 = rng.choice(p['dev'])
        v = f'{v.rstrip(".")}. Supporting feature: "{d0[1]}" ({d0[0]}) – {d0[2]}.'
    return dict(), v


def _fmt(q, p, fd):
    d = dict(fd)
    d.setdefault('gq', p.get('gq', ''))
    d.setdefault('label', label(p))
    d.setdefault('issue', p.get('issue', '').split(':')[0].rstrip('.'))
    if p.get('concept'):
        d.setdefault('cname', p['concept'][0])
    return q.format(**d)


MARKS_BY_D = {1: 2, 2: 2, 3: 3, 4: 4, 5: 6}


def pq(keys, c, d, kinds, note, qs, typ='short', crit=None, marks=None, neutral=False, name_='pq', gap=None):
    """Passage-based question frames: stem = passage + one of qs; answer from the passage annotation."""
    keys = [keys] if isinstance(keys, str) else keys
    kinds = set(kinds) if kinds else None

    def fn(rng, slot):
        pool = [p for p in PASS if (kinds is None or p['kind'] in kinds) and
                (p.get(note) if not isinstance(note, tuple) else all(p.get(n) for n in note))]
        if note == 'kconv':
            pool = [p for p in PASS if kinds is None or p['kind'] in kinds]
        if not pool:
            return None
        p = rng.choice(pool)
        g = _get(p, note, rng)
        if g is None:
            return None
        fd, ans = g
        q = _fmt(rng.choice(qs), p, fd)
        m = marks if marks else ({1: 4, 2: 4, 3: 6, 4: 8, 5: 10}[slot.d] if typ == 'long' else MARKS_BY_D[slot.d])
        out = dict(stem=f'{intro(p, neutral)}\n\n{q}', answer=ans, type=typ, marks=m,
                   markingKey=f'{ans} {crit or CRIT_B}')
        if gap:
            out['gap'] = gap
        return out
    for k in keys:
        R.t.setdefault(k, []).append(T(c, d, fn, typ, None, name_ + '_' + (note if isinstance(note, str) else '_'.join(note))))


def pq_dev_mcq(keys, kinds=None, d=(1, 3)):
    keys = [keys] if isinstance(keys, str) else keys

    def fn(rng, slot):
        pool = [p for p in PASS if (kinds is None or p['kind'] in kinds) and p.get('dev')]
        p = rng.choice(pool)
        e = rng.choice(p['dev'])
        stem = f'{intro(p)}\n\n' + rng.choice([f'The words "{e[1]}" are an example of which feature?',
                                                 f'Which stylistic feature is used in "{e[1]}"?',
                                                 f'Identify the device in the quotation "{e[1]}".'])
        return mcq(rng, stem, e[0], e[3], f'"{e[1]}" is an example of {e[0]}: {e[2]}.')
    for k in keys:
        R.t.setdefault(k, []).append(T('C1', d, fn, 'mcq', None, 'pq_dev_mcq'))


def pq_tone_mcq(keys, kinds=None, d=(1, 3)):
    keys = [keys] if isinstance(keys, str) else keys

    def fn(rng, slot):
        pool = [p for p in PASS if (kinds is None or p['kind'] in kinds) and p.get('tone')]
        p = rng.choice(pool)
        stem = f'{intro(p)}\n\n' + rng.choice(['Which word best describes the overall tone of the text?',
                                                 'The tone of this text is best described as:',
                                                 'Which of the following best captures the writer\'s tone?'])
        return mcq(rng, stem, p['tone'], p['tw'], f'The tone is {p["tone"]}: {p.get("tonex", "")}'.strip())
    for k in keys:
        R.t.setdefault(k, []).append(T('C1', d, fn, 'mcq', None, 'pq_tone_mcq'))


def pq_kind_mcq(keys, kinds=None, d=(1, 2)):
    keys = [keys] if isinstance(keys, str) else keys

    def fn(rng, slot):
        pool = [p for p in PASS if (kinds is None or p['kind'] in kinds) and p['kind'] in KIND_WRONG]
        p = rng.choice(pool)
        stem = f'{intro(p, neutral=True)}\n\n' + rng.choice(['Which text type is this?',
                                                               'This text is best classified as a:',
                                                               'Identify the text type of the extract above.'])
        return mcq(rng, stem, label(p), KIND_WRONG[p['kind']],
                   f'It is a {label(p)}: it uses conventions such as {KIND_CONV[p["kind"]]}.')
    for k in keys:
        R.t.setdefault(k, []).append(T('C1', d, fn, 'mcq', None, 'pq_kind_mcq'))


def pq_para(keys, kinds=None, c='C4', d=(3, 5), frames=None, crit=None, marks=None):
    """Guided-analysis paragraph / essay frames built on the passage guiding question."""
    keys = [keys] if isinstance(keys, str) else keys
    frames = frames or [
        'Guiding question: {gq}\nWrite one analytical paragraph that answers the guiding question, using at least two references to the text.',
        'With reference to the guiding question – "{gq}" – write the thesis and first body paragraph of a Paper 1 guided analysis.',
    ]

    def fn(rng, slot):
        pool = [p for p in PASS if (kinds is None or p['kind'] in kinds) and p.get('gq') and p.get('gqa')]
        p = rng.choice(pool)
        m = marks or (6 if slot.d <= 3 else 10 if slot.d == 4 else 15)
        q = _fmt(rng.choice(frames), p, {})
        if p['kind'] not in NONLIT:
            q = q.replace('a Paper 1 guided analysis', 'a guided literary analysis').replace('Paper 1 ', '')
        return dict(stem=f'{intro(p)}\n\n{q}', answer=p['gqa'], type='long', marks=m,
                    markingKey=f'Indicative content: {p["gqa"]} {crit or MARKBAND}')
    for k in keys:
        R.t.setdefault(k, []).append(T(c, d, fn, 'long', None, 'pq_para'))


# =============================================================================================
# Passage library (original texts written for this bank unless attributed)
# =============================================================================================
P(id='bottle', kind='ad', title='advertisement for a refillable water bottle, displayed on a city bus shelter',
  text=("YOUR 7:42 DOESN'T WAIT. NEITHER DOES THE PLANET.\n"
        "[Image: a commuter's hand grips a matte-green bottle against a blurred, grey crowd.]\n"
        "Every minute, a million plastic bottles are sold worldwide. You only need one.\n"
        "FLOW. Steel-built. Leak-proof. Yours for life.\n"
        "Fill it. Carry it. Keep it.\n"
        "Refill free at 300 stations across the city – find yours on the FLOW app."),
  aud='Busy urban commuters: the time-stamped train ("Your 7:42"), the direct address and the bus-shelter placement target people travelling to work.',
  purp='To persuade commuters to buy a FLOW bottle by presenting the purchase as both convenient and environmentally responsible.',
  ctx='It appears in a city at a time of public concern about single-use plastic; the free refill stations suggest a partnership with the city, so the brand looks civic-minded rather than simply commercial.',
  tone='urgent', tw=['nostalgic', 'melancholic', 'whimsical'], tonex='short imperatives and the time pressure of the headline create urgency.',
  dev=[('statistic', 'Every minute, a million plastic bottles are sold worldwide', 'the figure gives the environmental claim factual weight and makes one person\'s habits part of a vast problem', ['onomatopoeia', 'oxymoron', 'simile']),
       ('tricolon', 'Fill it. Carry it. Keep it.', 'three short imperatives create a memorable rhythm and present the product as a simple daily ritual', ['rhetorical question', 'simile', 'euphemism']),
       ('direct address', "YOUR 7:42 DOESN'T WAIT", 'the second-person pronoun speaks to the individual commuter and ties the advert to their routine', ['oxymoron', 'onomatopoeia', 'simile']),
       ('antithesis', 'a million plastic bottles ... You only need one', 'the contrast between the vast number and a single bottle makes one purchase feel like a sufficient, empowering response', ['onomatopoeia', 'simile', 'rhetorical question'])],
  struct=[('the parallel two-sentence headline in capitals', 'the matching structure ("doesn\'t wait ... Neither does") links the reader\'s personal hurry to a global emergency'),
          ('the closing call to action with the app', 'it moves the reader from feeling to doing and ends on a practical, low-effort next step')],
  visual='Colour contrast isolates the single green bottle against a grey, blurred crowd, so the eco-conscious individual stands out from the masses; the close-up on the hand places the viewer in the commuter\'s position.',
  desire='Desire is constructed by making the bottle a sign of moral distinction (green against grey) and of control over a hectic life, so the buyer purchases an identity, not just a container.',
  gq='How does the advertisement persuade its audience that an individual purchase can address a global problem?',
  gqa=('Thesis: the advertisement shrinks a global crisis to the scale of one commuter\'s routine. (1) The parallel headline links personal and planetary urgency. '
       '(2) The statistic set against "You only need one" turns guilt into empowerment. (3) The imperative tricolon and the green-against-grey image make the purchase simple and morally distinctive. '
       'Evaluation: the text arguably commodifies environmentalism – it solves over-consumption by selling another product (greenwashing).'),
  issue='Consumerism and environmental responsibility: whether buying "green" products can solve problems created by consumption.',
  concept=('representation', 'the eco-conscious consumer is represented as decisive and distinct from the grey, anonymous crowd.'),
  read='An environmentally engaged reader may see a practical call to cut plastic waste; a sceptical reader may read it as greenwashing that sells more products in the name of consuming less.',
  field='science, technology and the environment')

P(id='lingo', kind='ad', title='advertisement for a language-learning app, published in an in-flight magazine',
  text=("[Image: a grandmother and a teenage boy laugh across a kitchen table in Lisbon; steam rises from two cups.]\n"
        "She never learned English. He never learned Portuguese. Until now.\n"
        "Fifteen minutes a day. That's all it takes to turn 'Olá' into a conversation.\n"
        "Lingo Bridge – because some words can't wait for a translator.\n"
        "Download free. First month on us."),
  aud='Travellers and members of multilingual or diaspora families (in-flight magazine readers), especially adults separated from relatives by language.',
  purp='To persuade readers to download the app by associating language learning with family connection rather than with study or work.',
  ctx='Placed in an in-flight magazine, it reaches people literally travelling between language communities, often to visit family abroad.',
  tone='tender', tw=['sarcastic', 'threatening', 'clinical'], tonex='the warm domestic image and the story of reconnection create tenderness.',
  dev=[('parallelism', 'She never learned English. He never learned Portuguese.', 'the mirrored sentences make the language barrier shared and symmetrical, so neither character is blamed and the gap feels poignant', ['onomatopoeia', 'statistic', 'rhetorical question']),
       ('minor sentence', 'Until now.', 'the abrupt fragment marks a turning point and positions the app as the force that changes the family story', ['simile', 'oxymoron', 'rhetorical question']),
       ('emotive language', "some words can't wait for a translator", 'it implies that family love is urgent and cannot be mediated, raising the emotional stakes of the purchase', ['statistic', 'onomatopoeia', 'anaphora'])],
  struct=[('the mini-narrative of the headline (problem – turning point)', 'it compresses a story of separation and reunion into three sentences, with the product as the resolution'),
          ('the low-commitment offer at the end', '"Fifteen minutes a day" and "First month on us" remove practical and financial barriers to acting')],
  visual='The warm kitchen, rising steam and shared laughter connote intimacy; placing the two generations face to face across the table visually enacts the "bridge" of the brand name.',
  desire='The advert sells an emotion – reconnection with family and heritage – so desire for the product is really desire for belonging.',
  gq='How does the advertisement use the representation of family to sell a product?',
  gqa=('Thesis: the advertisement sells an app by selling reconnection across generations. (1) The image of facing figures in a warm kitchen enacts the brand metaphor of a bridge. '
       '(2) Parallel sentences and the fragment "Until now" create a mini-narrative with the app as the turning point. (3) The low-commitment offer removes barriers. '
       'Evaluation: the text idealises language learning, implying fluency is quick, and turns family intimacy into a commercial promise.'),
  issue='Language, migration and family identity: how language barriers separate generations in diaspora communities.',
  concept=('identity', 'family and cultural identity are represented as something recovered through a shared language.'),
  read='A reader from a diaspora family may find it moving and recognise the experience; another reader may resist its sentimentality, seeing it as exploiting family separation to sell subscriptions.',
  lang='The Portuguese greeting "Olá" is left untranslated, signalling heritage and showing that the first step is already shared; language is presented as a marker of family belonging.',
  field='culture, identity and community')

P(id='suv', kind='ad', title='advertisement for a family SUV, printed in a weekend newspaper magazine',
  text=("[Image: a father at the wheel, two children asleep in the back, mountains at dusk through the windscreen.]\n"
        "HE'S GOT THIS.\n"
        "Seven seats. Five-star safety. Zero doubts.\n"
        "The Atlas X7. Built for the man who carries everyone.\n"
        "[Small print: 7.9 L/100 km combined. Model shown with optional extras.]"),
  aud='Fathers and middle-income parents reading a weekend magazine, particularly men who see themselves as family providers.',
  purp='To persuade readers to buy the SUV by linking it to safety and to an ideal of dependable fatherhood.',
  ctx='Weekend newspaper magazines are read at leisure by relatively affluent households; the small-print fuel figure reflects rules that require consumption data, which the design minimises.',
  tone='reassuring', tw=['anxious', 'mocking', 'despairing'], tonex='the calm idiom "HE\'S GOT THIS" and the sleeping children reassure the reader.',
  dev=[('tricolon', 'Seven seats. Five-star safety. Zero doubts.', 'the countdown of numbers moves from product facts to an emotional promise, so confidence seems to be a feature of the car', ['simile', 'rhetorical question', 'onomatopoeia']),
       ('colloquialism', "HE'S GOT THIS", 'the casual, reassuring idiom presents the father as calm and competent and invites male readers to identify with him', ['oxymoron', 'statistic', 'simile']),
       ('metaphor', 'the man who carries everyone', 'it casts the father as protector and provider, linking masculinity to responsibility and to the car\'s size', ['onomatopoeia', 'rhetorical question', 'statistic'])],
  struct=[('the very short headline followed by the three-part list', 'the brevity mirrors the confident, unhesitating masculinity the brand promises'),
          ('the small print placed at the bottom', 'the fuel-consumption information is legally present but visually marginalised, so the emotional message dominates')],
  visual='The father is framed centrally at the wheel with sleeping children behind him; dusk mountains connote adventure and trust; the tiny small print visually downplays fuel consumption.',
  gender='The man is represented as protector and driver and the children as passive passengers; the mother is absent, and the pronoun "He" in the headline assumes the driver and carer is male, reinforcing a traditional provider role.',
  desire='Desire is constructed around being the dependable father: the car is sold as proof of masculine competence and family safety.',
  gq='How does the advertisement construct a particular image of fatherhood?',
  gqa=('Thesis: the advertisement equates good fatherhood with control and protection, and sells the SUV as its proof. (1) The idiom "HE\'S GOT THIS" and the central framing at the wheel present calm masculine competence. '
       '(2) The tricolon turns product data into emotional certainty ("Zero doubts"). (3) The metaphor "carries everyone" and the absent mother naturalise a provider role. '
       'Evaluation: the text excludes female and non-traditional carers and hides environmental cost in the small print.'),
  issue='Gender roles and representation: how advertising reinforces the father as protector and provider.',
  concept=('representation', 'masculinity is represented as calm control and responsibility for others.'),
  read='A reader who values traditional family roles may find it reassuring; a feminist reader may notice the absent mother and the assumption that the protector is male.',
  field='culture, identity and community')

P(id='serum', kind='ad', title='sponsored advertisement for a skincare serum, shown in a social media feed',
  text=("Glow like you mean it.\n"
        "Clinically shown*: 87% saw brighter skin in 14 days.\n"
        "Powered by Vitamin C-12, our exclusive molecule from Swiss labs.\n"
        "Because you deserve skin that tells the truth about you.\n"
        "#NoFilterNeeded – Tap to shop. Free delivery today only.\n"
        "*Survey of 64 women, self-reported results."),
  aud='Young women scrolling social media who are concerned about appearance and receptive to wellness and "authenticity" language.',
  purp='To persuade viewers to buy the serum immediately by combining scientific-sounding authority with appeals to self-worth.',
  ctx='Sponsored posts appear among friends\' content, borrowing their intimacy; the footnote reflects advertising rules that require claims to be qualified, but in tiny type.',
  tone='confident', tw=['hesitant', 'mournful', 'apologetic'], tonex='imperatives and precise claims project confidence.',
  dev=[('statistic', '87% saw brighter skin in 14 days', 'the precise percentage borrows the authority of science, although the footnote reveals a small, self-reported survey', ['onomatopoeia', 'simile', 'alliteration']),
       ('jargon', 'Vitamin C-12, our exclusive molecule from Swiss labs', 'technical-sounding naming and Swiss origin connote precision and expertise, encouraging trust without explanation', ['onomatopoeia', 'rhetorical question', 'anaphora']),
       ('imperative', 'Glow like you mean it', 'the confident command turns a cosmetic result into an expression of personality and determination', ['statistic', 'rhetorical question', 'oxymoron']),
       ('scarcity appeal', 'Free delivery today only', 'a time limit pressures the viewer into an impulse purchase', ['simile', 'personification', 'onomatopoeia'])],
  struct=[('the asterisk linking the claim to the footnote', 'the bold claim is read first and the qualification last, so the doubt arrives after the desire has been created'),
          ('the hashtag and "Tap to shop" at the end', 'they fit the platform\'s conventions and make buying one tap away from reading')],
  visual='The text would be laid over a close-up of glowing skin; the small footnote is visually subordinated to the large statistic.',
  desire='Desire is constructed by linking flawless skin to authenticity ("skin that tells the truth about you") and self-worth ("you deserve"), while scarcity turns desire into immediate action.',
  gender='Women are addressed as consumers whose value is tied to appearance; "you deserve" frames buying as self-care, a common gendered strategy in beauty advertising.',
  gq='How does the advertisement combine scientific authority and emotional appeal to persuade its audience?',
  gqa=('Thesis: the advert uses the language of science to make an emotional promise feel factual. (1) The statistic and jargon ("Vitamin C-12", "Swiss labs") create authority. '
       '(2) "You deserve" and "tells the truth about you" tie the product to self-worth. (3) The scarcity close and platform conventions convert desire into a tap. '
       'Evaluation: the footnote undermines the claim (64 women, self-reported), so the persuasion depends on readers not reading carefully.'),
  issue='Beauty standards and consumer manipulation: pseudo-science and the commodification of self-worth.',
  concept=('perspective', 'the advert positions the viewer to see her natural skin as a problem and the product as the truth.'),
  read='A trusting reader may accept the clinical claim; a critical reader notices the footnote and reads the advert as manipulative pseudo-science.',
  misinfo='The headline claim is technically qualified by the footnote, but the small sample and self-reporting mean "clinically shown" misleads; algorithms then target the post at users already interested in beauty.',
  field='beliefs, values and education')

P(id='summit', kind='speech', title='speech by a student delegate at an international youth climate summit',
  text=("Delegates, I was born in 2008. In my lifetime the sea outside my grandmother's house in Tuvalu has crept forty metres closer. "
        "Forty metres. You measure progress in decades; we measure it in doorsteps. You tell us we are the future. "
        "But we are not the future – we are the present, standing in water. So do not applaud me. Applause is cheap. Act."),
  aud='Adult delegates and policymakers at an international summit, and a wider media audience watching the speech.',
  purp='To challenge leaders to move from symbolic gestures, such as applause for young speakers, to concrete climate action.',
  ctx='Delivered at a summit where young speakers are often celebrated but not listened to; Tuvalu is a low-lying Pacific nation highly vulnerable to sea-level rise, which gives the personal anecdote political force.',
  tone='defiant', tw=['playful', 'resigned', 'flippant'], tonex='short commands and the refusal of applause make the tone defiant.',
  dev=[('repetition', 'forty metres closer. Forty metres.', 'repeating the figure as a fragment forces the audience to pause on a concrete, measurable loss', ['simile', 'onomatopoeia', 'oxymoron']),
       ('antithesis', 'You measure progress in decades; we measure it in doorsteps', 'the contrast sets abstract political time against concrete domestic loss and divides "you" (leaders) from "we" (the young)', ['simile', 'onomatopoeia', 'euphemism']),
       ('imperative', 'Act.', 'the final one-word command shifts responsibility to the audience with blunt force', ['simile', 'statistic', 'rhetorical question']),
       ('metaphor', 'we are the present, standing in water', 'it overturns the cliché "you are the future" and makes the crisis immediate and physical', ['onomatopoeia', 'statistic', 'anaphora'])],
  struct=[('the movement from personal anecdote to collective "we"', 'the speaker begins with one family and widens to a generation, turning private loss into a political claim'),
          ('the progressively shorter final sentences', '"Applause is cheap. Act." accelerates to a climax and leaves the audience with a single instruction')],
  gq='How does the speaker use personal experience to challenge her audience?',
  gqa=('Thesis: the speaker turns a family anecdote into an accusation that leaders mistake gestures for action. (1) Precise detail (2008, forty metres, Tuvalu) gives authority and urgency. '
       '(2) Antithesis divides "you" and "we" and redefines time as loss. (3) Rejecting applause and ending on "Act." turns the audience\'s likely response against them. '
       'Evaluation: the confrontational stance risks alienating listeners, but its brevity makes it highly quotable for the media audience.'),
  issue='Climate justice and intergenerational responsibility.',
  concept=('perspective', 'the young islander\'s perspective challenges the leaders\' sense of time and progress.'),
  read='Sympathetic listeners hear moral clarity; others may hear disrespect for diplomacy – the speech deliberately risks this to be heard.',
  field='science, technology and the environment')

P(id='library', kind='speech', title='speech by a city mayor at the opening of a public library in a multilingual neighbourhood',
  text=("Friends, neighbours – bienvenidos, karibu, welcome. Some people say libraries are relics, that everything we need is on our phones. "
        "But a phone cannot hold a child's hand through her first chapter book. A phone does not stay open late for the night-shift nurse who wants to finish her degree. "
        "This building belongs to you: to every language spoken on these streets, and to every language not yet learned."),
  aud='Residents of the neighbourhood, including multilingual families, workers and local media.',
  purp='To celebrate the library and argue for its value against the claim that digital technology has made libraries obsolete.',
  ctx='Public spending on libraries is often questioned; the multilingual greeting acknowledges a diverse community of migrants.',
  tone='celebratory', tw=['bitter', 'detached', 'menacing'], tonex='greetings and warm images celebrate the community.',
  dev=[('code-switching', 'bienvenidos, karibu, welcome', 'greeting in Spanish, Swahili and English includes migrant communities and enacts the library\'s multilingual purpose', ['statistic', 'onomatopoeia', 'oxymoron']),
       ('anaphora', 'A phone cannot ... A phone does not', 'repeating the subject at the start of successive sentences hammers home what technology cannot do', ['statistic', 'onomatopoeia', 'euphemism']),
       ('personification', "a phone cannot hold a child's hand", 'denying the phone a human action highlights the human care a library offers', ['statistic', 'oxymoron', 'onomatopoeia']),
       ('counter-argument', 'Some people say libraries are relics', 'raising and then rebutting the opposing view makes the speaker seem fair and the conclusion stronger', ['simile', 'onomatopoeia', 'oxymoron'])],
  struct=[('the concession followed by "But"', 'the rebuttal structure turns a common objection into a springboard for the library\'s value'),
          ('the closing tricolon of belonging', 'ending with "every language not yet learned" looks to the future and makes the building a shared possession')],
  lang='Greeting the audience in several languages before English treats each community\'s language as equally welcome; it signals that language is part of identity and civic belonging.',
  gq='How does the mayor construct the library as a place of belonging?',
  gqa=('Thesis: the mayor presents the library as a human, multilingual home rather than a store of information. (1) Code-switching in the greeting includes migrant communities. '
       '(2) Anaphora and personification contrast the phone\'s limits with human care (the child, the nurse). (3) The final possessive "belongs to you" transfers ownership to residents. '
       'Evaluation: the speech is inclusive but sentimental; it avoids questions of funding.'),
  issue='Access to education and cultural inclusion in diverse cities.',
  concept=('community and culture', 'the library is represented as a shared cultural space that holds many languages.'),
  read='Residents may feel recognised; a sceptical taxpayer might see a politician\'s warm words used to justify spending.',
  field='culture, identity and community')

P(id='suffrage', kind='speech', title='speech by a campaigner for women\'s suffrage at a public meeting in Manchester, 1912 (an original pastiche written for study)',
  text=("Gentlemen of the press, you call us unreasonable. Very well. Was it reasonable that my mother paid taxes on a shop she ran for thirty years, "
        "yet could not vote for the men who spent them? Was it reasonable that the law counted her as a citizen when it came to paying, "
        "and as a child when it came to choosing? We have asked politely for forty years. Politeness has been answered with silence. We shall not be silent any longer."),
  aud='A public meeting of supporters and sceptics, and "gentlemen of the press" who will report the speech to a wider, largely male readership.',
  purp='To justify militant campaigning by showing that polite requests for the vote have failed.',
  ctx='In Edwardian Britain women could not vote in parliamentary elections; some property-owning women over 30 gained the vote in 1918 and equal franchise came in 1928. Suffragettes were often described as unreasonable or hysterical in the press.',
  tone='indignant', tw=['jovial', 'apologetic', 'serene'], tonex='repeated challenges and the final vow convey controlled indignation.',
  dev=[('rhetorical question', 'Was it reasonable that my mother paid taxes', 'the question turns the press\'s accusation back on the law and expects the answer "no"', ['simile', 'onomatopoeia', 'statistic']),
       ('antithesis', 'a citizen when it came to paying, and as a child when it came to choosing', 'the balanced contrast exposes the contradiction in how the law treated women', ['onomatopoeia', 'simile', 'statistic']),
       ('personification', 'Politeness has been answered with silence', 'making politeness and silence actors summarises decades of ignored petitions in one image', ['statistic', 'simile', 'onomatopoeia']),
       ('irony', 'you call us unreasonable. Very well.', 'accepting the insult with mock calm prepares to show who is truly unreasonable', ['statistic', 'onomatopoeia', 'simile'])],
  struct=[('the repeated question "Was it reasonable"', 'anaphora builds a cumulative case that reframes the word used against the campaigners'),
          ('the turn from the past ("We have asked") to the future ("We shall not")', 'the speech moves from grievance to resolve, ending on a collective vow')],
  gq='How does the speaker turn the accusation of being "unreasonable" against her opponents?',
  gqa=('Thesis: the speaker reclaims "reasonable" to argue that the law, not the women, is irrational. (1) The ironic "Very well" accepts the label only to test it. '
       '(2) Anaphoric rhetorical questions and the personal example of the mother build a logical case. (3) The antithesis citizen/child exposes legal contradiction; the final vow justifies escalation. '
       'Evaluation: addressing the press directly anticipates hostile reporting and frames the meeting\'s message for a wider public.'),
  issue='Political power and gender equality: who is allowed a voice in democracy.',
  concept=('representation', 'the speaker challenges the press\'s representation of campaigners as unreasonable.'),
  read='Supporters hear justified resolve; a 1912 sceptic might hear a threat; a modern reader sees a familiar strategy of reclaiming an insult.',
  field='politics, power and justice')

P(id='lathe', kind='propaganda', title='home-front poster from a fictional wartime nation, written in the style of 1940s propaganda',
  text=("[Image: a woman in overalls rolls up her sleeve beside a factory gate; behind her, the silhouettes of marching soldiers.]\n"
        "THEIR COURAGE AT THE FRONT.\nYOUR STRENGTH AT THE LATHE.\n"
        "Every shell you make is a letter home.\n"
        "Don't let them down – report for factory work today."),
  aud='Women at home during wartime who could be recruited for industrial work.',
  purp='To recruit women into munitions factories by presenting industrial work as patriotic duty and loyalty to soldiers.',
  ctx='In the Second World War many governments ran poster campaigns to bring women into factories while men served in the armed forces.',
  tone='rousing', tw=['ironic', 'melancholic', 'indifferent'], tonex='capitals, commands and heroic imagery rouse the audience.',
  dev=[('parallelism', 'THEIR COURAGE AT THE FRONT. YOUR STRENGTH AT THE LATHE.', 'the matching structure makes factory work equal to fighting and binds the reader to the soldiers', ['onomatopoeia', 'simile', 'rhetorical question']),
       ('metaphor', 'Every shell you make is a letter home', 'it turns a weapon into an act of love and communication, softening violence and personalising the labour', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('emotive imperative', "Don't let them down", 'the command uses guilt and loyalty to compel action', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the slogan placed above the instruction', 'the emotional appeal comes first, the practical demand ("report ... today") last')],
  visual='The rolled sleeve signals readiness and strength; soldiers\' silhouettes behind her link her body to theirs; she faces the viewer, modelling the action requested.',
  gender='Women are represented as strong and capable workers, but their strength is valued as support for men at the front; the poster expands women\'s roles only for the duration of the war.',
  gq='How does the poster persuade women to take up factory work?',
  gqa=('Thesis: the poster recruits by equating industrial labour with the soldier\'s heroism and with love. (1) Parallel capitals equate front and lathe. '
       '(2) The metaphor "a letter home" transforms shells into affection. (3) The image of the rolled sleeve models readiness, and the imperative uses guilt. '
       'Evaluation: the empowerment is conditional – it serves the war effort rather than women\'s equality.'),
  issue='Power, propaganda and the representation of gender in wartime.',
  concept=('representation', 'women\'s work is represented as patriotic heroism, but in a supporting role.'),
  read='A 1940s reader might feel pride and duty; a modern feminist reader may note how the poster uses women\'s labour while keeping men at the centre of heroism.',
  field='politics, power and justice')

P(id='phones', kind='oped', title='opinion column published in a national newspaper',
  text=("Let me be clear: I am no technophobe. I file this column from a laptop, on a train, while my phone buzzes like a trapped wasp. "
        "But I have watched my own students in Nairobi sit side by side at lunch, heads bowed, in total silence, as if at a funeral. "
        "We would never let a casino open in a school corridor. Why, then, do we allow a slot machine in every pocket?"),
  aud='Parents, teachers and policymakers who read a national newspaper.',
  purp='To argue that schools should restrict smartphones because they are addictive and isolate students.',
  ctx='Written during a public debate about phone bans in schools; the columnist\'s identity as a teacher in Nairobi gives first-hand authority.',
  tone='impassioned', tw=['indifferent', 'celebratory', 'whimsical'], tonex='vivid similes and a pointed question express strong feeling.',
  dev=[('simile', 'my phone buzzes like a trapped wasp', 'the comparison makes the phone irritating and slightly threatening, even for an adult', ['statistic', 'anaphora', 'oxymoron']),
       ('simile', 'in total silence, as if at a funeral', 'it suggests the death of conversation and community', ['statistic', 'anaphora', 'onomatopoeia']),
       ('rhetorical question', 'Why, then, do we allow a slot machine in every pocket?', 'the question forces readers to accept the analogy between phones and gambling', ['simile', 'statistic', 'onomatopoeia']),
       ('concession', 'I am no technophobe', 'anticipating the objection that the writer fears technology makes the argument appear balanced', ['onomatopoeia', 'simile', 'statistic'])],
  struct=[('the opening concession', 'it builds credibility before the attack'),
          ('the analogy saved for the final sentence', 'the casino/slot machine comparison lands as a memorable closing punch')],
  gq='How does the writer persuade readers that smartphones are harmful to students?',
  gqa=('Thesis: the writer persuades through credibility and analogy rather than data. (1) The concession establishes balance. (2) Similes (wasp, funeral) give emotional, sensory weight. '
       '(3) The casino analogy and rhetorical question reframe phones as addictive. Evaluation: the argument relies on anecdote and a loaded analogy; a reader may want evidence.'),
  issue='Technology, attention and the wellbeing of young people.',
  concept=('communication', 'the column argues that phones replace face-to-face communication with silence.'),
  read='A worried parent may find it compelling; a student may object that phones also connect them and that the analogy is unfair.',
  field='science, technology and the environment')

P(id='alfama', kind='oped', title='opinion column in an English-language newspaper in Lisbon',
  text=("My grandmother's street in Alfama now has eleven bakeries and no neighbours. The bakeries sell pastéis de nata to people who will leave on Sunday; "
        "the neighbours who once bought bread there have left for good, priced out by short-term rentals. Tourism, we are told, is our salvation. "
        "Perhaps. But a city that sells its every doorway eventually has nothing left to show its visitors except itself, emptied."),
  aud='Residents, expatriates and decision-makers in Lisbon who read an English-language local paper, as well as tourists.',
  purp='To argue that unregulated tourism and short-term rentals are hollowing out historic neighbourhoods.',
  ctx='Lisbon has experienced rapid growth in tourism and short-term rentals, leading to debates about housing costs in historic districts such as Alfama.',
  tone='wry', tw=['jubilant', 'neutral', 'frivolous'], tonex='irony and understatement ("Perhaps.") create a wry, regretful tone.',
  dev=[('juxtaposition', 'eleven bakeries and no neighbours', 'placing abundance beside absence captures the paradox of a busy but empty street', ['simile', 'rhetorical question', 'onomatopoeia']),
       ('irony', 'Tourism, we are told, is our salvation', '"we are told" distances the writer from the official claim and signals disbelief', ['simile', 'statistic', 'onomatopoeia']),
       ('minor sentence', 'Perhaps.', 'the one-word concession is so brief that it sounds sceptical', ['simile', 'statistic', 'anaphora']),
       ('metaphor', 'a city that sells its every doorway', 'it presents housing as the city\'s body being sold piece by piece', ['statistic', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the opening anecdote about the grandmother\'s street', 'it grounds the argument in personal, local loss'),
          ('the ending on the word "emptied"', 'placing the key word last, after a comma, gives it finality')],
  gq='How does the writer convey the effects of tourism on a local community?',
  gqa=('Thesis: the writer uses irony and contrast to show that tourism empties what it sells. (1) The juxtaposition of bakeries and neighbours. (2) The ironic "we are told" and minor sentence "Perhaps." undermine the official story. '
       '(3) The doorway metaphor and final "emptied" present the city as stripped of life. Evaluation: persuasive through personal voice, though it gives no data on housing.'),
  issue='Overtourism, housing and the loss of local community.',
  concept=('transformation', 'the neighbourhood is shown transformed from a community into a stage set for visitors.'),
  read='A resident may feel vindicated; a business owner who depends on tourism may see the column as nostalgic and one-sided.',
  field='culture, identity and community')

P(id='aiart', kind='oped', title='opinion column on art and artificial intelligence',
  text=("Last week a machine won a regional art prize. The judges, to their credit, were embarrassed. The machine, to its credit, was not – "
        "it cannot be embarrassed, which is precisely the point. Art has never been about the finished picture alone; it is about a person risking something in public. "
        "An algorithm risks nothing. It cannot fail, so it cannot really succeed."),
  aud='Educated general readers interested in culture and technology.',
  purp='To argue that AI-generated images are not art in the full sense because art requires human risk.',
  ctx='Written amid debates about AI image generators winning competitions and their effect on human artists.',
  tone='wry', tw=['hysterical', 'sentimental', 'pleading'], tonex='the mock-praise of the machine creates dry, wry humour.',
  dev=[('parallelism', 'The judges, to their credit, were embarrassed. The machine, to its credit, was not', 'the repeated phrase sets up ironic humour and contrasts human feeling with machine indifference', ['statistic', 'onomatopoeia', 'simile']),
       ('paradox', 'It cannot fail, so it cannot really succeed', 'the apparent contradiction condenses the argument that achievement depends on the possibility of failure', ['simile', 'onomatopoeia', 'statistic']),
       ('short declarative sentence', 'An algorithm risks nothing.', 'its blunt brevity states the core claim as if it were self-evident', ['simile', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the anecdote of the prize followed by a general definition of art', 'the column moves from a news hook to a principle, then to a conclusion'),
          ('the closing paradox', 'the final sentence is designed to be quoted, leaving the reader with the central idea')],
  gq='How does the writer use humour and argument to question whether AI can make art?',
  gqa=('Thesis: the writer uses irony to make a philosophical argument feel like common sense. (1) Parallel "to their credit" humour separates human and machine. '
       '(2) A redefinition of art as risk. (3) The short declarative and closing paradox. Evaluation: the definition is contestable – humans who use AI may still take risks.'),
  issue='Creativity, technology and the value of human art.',
  concept=('creativity', 'the writer defines creativity as human risk-taking, which machines cannot do.'),
  read='An artist may welcome the defence of human creativity; a technologist may argue the column ignores the human who prompts and curates.',
  field='art, creativity and the imagination')

P(id='hanoi', kind='blog', title='post from a travel blog written by a young backpacker in Vietnam',
  text=("Day 12. Hanoi. Honestly? I came for the Instagram shots – the lanterns, the train street, the egg coffee. "
        "What I got was Mrs Lan, who runs a tiny noodle stall and refused to let me pay because I tried (badly) to say 'thank you' in Vietnamese. "
        "Lesson learned: the best stuff here isn't on any list. #slowtravel"),
  aud='Other young travellers and followers of the blog, likely familiar with Instagram culture.',
  purp='To share a personal travel experience and recommend a slower, more human way of travelling.',
  ctx='Travel blogging and social media have made some places famous as photo spots; the writer reflects on this culture.',
  tone='self-deprecating', tw=['authoritative', 'furious', 'solemn'], tonex='"(badly)" and "Honestly?" poke fun at the writer.',
  dev=[('tricolon', 'the lanterns, the train street, the egg coffee', 'the list of clichéd photo spots satirises the tourist checklist', ['simile', 'oxymoron', 'onomatopoeia']),
       ('parenthesis', '(badly)', 'the aside creates self-deprecating humour and makes the writer likeable', ['statistic', 'simile', 'anaphora']),
       ('colloquialism', 'the best stuff here', 'informal diction creates a chatty, peer-to-peer voice', ['statistic', 'onomatopoeia', 'oxymoron']),
       ('rhetorical question', 'Honestly?', 'the one-word question mimics speech and signals a confession to the reader', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the diary-style opening "Day 12. Hanoi."', 'minor sentences establish the blog\'s chronological, personal format'),
          ('the contrast between "I came for" and "What I got"', 'the structure turns expectation into reversal and leads to the moral'),
          ('the closing hashtag', 'it links the post to an online community and summarises the lesson')],
  lang='The informal register, minor sentences ("Day 12. Hanoi."), colloquial diction and hashtag reflect digital conventions; the attempted Vietnamese "thank you" shows language as a gesture of respect.',
  gq='How does the blogger present the difference between tourism and genuine travel?',
  gqa=('Thesis: the blogger uses self-mockery to contrast the photo checklist with a human encounter. (1) The tricolon of photo spots satirises Instagram tourism. (2) The reversal "What I got was Mrs Lan" centres a person. '
       '(3) Self-deprecating parenthesis and hashtag frame the moral for peers. Evaluation: the post still uses the platform it criticises, and Mrs Lan remains a supporting character in the writer\'s story.'),
  issue='Tourism, authenticity and cultural encounter.',
  concept=('perspective', 'the traveller\'s perspective shifts from consumer to guest.'),
  read='Followers may find it charming; a Vietnamese reader might notice that the local person is used to teach the visitor a lesson.',
  persona='The blogger constructs a likeable persona – humble, curious, self-aware – that distinguishes them from "Instagram" tourists while still performing for followers.',
  field='culture, identity and community')

P(id='jollof', kind='blog', title='food blog post by a second-generation Ghanaian-British writer',
  text=("My mum never measured anything. 'Small pepper,' she'd say, and my eyes would water for an hour. "
        "Writing her jollof recipe down for you feels like a betrayal – like pinning a butterfly. "
        "But she is getting older, and I am scared of forgetting. So here it is, in grams and millilitres, with all the love that won't fit in brackets."),
  aud='Readers of a food blog, including members of the Ghanaian diaspora and food lovers curious about West African cooking.',
  purp='To share a family recipe while reflecting on memory, heritage and the loss involved in writing oral knowledge down.',
  ctx='Recipes in many families are passed on orally; second-generation migrants often record them to preserve cultural memory.',
  tone='affectionate', tw=['hostile', 'detached', 'triumphant'], tonex='fond memories of the mother create affection, mixed with fear of loss.',
  dev=[('reported speech', "'Small pepper,' she'd say", 'the mother\'s own phrase brings her voice into the text and creates humour through understatement', ['statistic', 'onomatopoeia', 'oxymoron']),
       ('simile', 'like pinning a butterfly', 'it suggests that fixing the recipe in writing preserves it but kills something living', ['statistic', 'anaphora', 'onomatopoeia']),
       ('metaphor', "all the love that won't fit in brackets", 'brackets, the recipe\'s precise conventions, cannot contain emotion – the measurable versus the unmeasurable', ['statistic', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the move from memory to present fear ("But she is getting older")', 'the turn explains why the writer overcomes her reluctance'),
          ('the ending that leads into the recipe', '"So here it is" makes the reflection an introduction to the practical text that follows')],
  lang='"Small pepper" is an expression from Ghanaian English (meaning "a little chilli") whose understatement is part of the joke; keeping the mother\'s idiom marks family identity and resists translating her into standard measurements.',
  gq='How does the writer explore the relationship between food, memory and identity?',
  gqa=('Thesis: the writer presents the recipe as an act of preservation that also loses something. (1) The mother\'s reported speech and humour. (2) The butterfly simile on the cost of fixing oral knowledge. '
       '(3) The closing metaphor of love that will not fit brackets. Evaluation: the blog genre allows a personal essay to frame practical content.'),
  issue='Cultural memory, migration and identity across generations.',
  concept=('transformation', 'oral family knowledge is transformed into a written, measured recipe.'),
  read='A diaspora reader may recognise the experience of untranslatable family knowledge; a food reader may simply enjoy the warmth before the recipe.',
  field='culture, identity and community')

P(id='skydeck', kind='blog', title='blog post by a wheelchair user reviewing accessibility at a music festival',
  text=("They gave the accessible viewing platform a lovely name: The Sky Deck. It was, in fairness, very close to the sky – up three flights of stairs. "
        "I watched the headliner on a stranger's phone from the bottom step. Five stars for irony, festival people. Zero for planning."),
  aud='Disabled festival-goers, the wider blog readership and, implicitly, the festival organisers.',
  purp='To criticise the festival\'s poor accessibility and hold organisers to account through humour.',
  ctx='Disabled people often report that "accessible" facilities at events are badly designed; blogs and social media are used to publicise this.',
  tone='sardonic', tw=['reverent', 'sentimental', 'neutral'], tonex='mock praise and irony create a sardonic tone.',
  dev=[('irony', 'very close to the sky – up three flights of stairs', 'the deadpan joke exposes the absurdity of an accessible platform that wheelchair users cannot reach', ['simile', 'statistic', 'onomatopoeia']),
       ('bathos', "I watched the headliner on a stranger's phone from the bottom step", 'the anticlimax undercuts the grand name with a humiliating reality', ['onomatopoeia', 'simile', 'statistic']),
       ('parody of a rating', 'Five stars for irony, festival people. Zero for planning.', 'imitating a review score turns the complaint into a memorable verdict', ['simile', 'onomatopoeia', 'oxymoron'])],
  struct=[('the build-up to the punchline after the dash', 'the dash delays the revelation, so the joke and the injustice land together')],
  lang='Direct address ("festival people") and ironic understatement create a conversational, sharp voice that refuses pity and claims authority.',
  gq='How does the writer use humour to criticise the festival?',
  gqa=('Thesis: humour lets the writer expose exclusion without asking for pity. (1) Irony of the "Sky Deck" up three flights. (2) Bathos of watching on a stranger\'s phone. '
       '(3) The parody rating addresses organisers directly. Evaluation: brevity and humour make the post shareable, increasing pressure on the festival.'),
  issue='Disability, access and inclusion in public life.',
  concept=('representation', 'the writer represents herself as an expert critic rather than a victim.'),
  read='Disabled readers may enjoy the solidarity of the joke; organisers may read it as a public warning.',
  field='politics, power and justice')

P(id='varga', kind='letter', title='open letter from a group of secondary teachers to the chief executive of a social media company, published online',
  text=("Dear Ms Varga,\nWe teach your users. Every morning we meet them: tired, anxious, scrolling under desks for the reassurance your notifications promise and never quite deliver. "
        "We do not ask you to switch off the internet. We ask something smaller and harder: switch off the notifications between 10 p.m. and 7 a.m. for under-18s. "
        "You built a product that never sleeps. Let our students."),
  aud='Formally the chief executive; in practice the public, parents and journalists who read the open letter online.',
  purp='To pressure the company into a specific policy change – night-time notification limits for minors.',
  ctx='Open letters are published so that public opinion adds pressure; debates about young people\'s sleep and social media provide the context.',
  tone='measured', tw=['hysterical', 'flippant', 'triumphant'], tonex='a calm, precise request makes the letter measured but firm.',
  dev=[('short declarative sentence', 'We teach your users.', 'the blunt opening links the CEO\'s customers to the teachers\' pupils and establishes authority', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('tricolon', 'tired, anxious, scrolling under desks', 'the list builds a picture of exhausted, dependent students', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('ellipsis (omission)', 'Let our students.', 'leaving out "sleep" forces the reader to complete the sentence, making the point witty and memorable', ['simile', 'statistic', 'onomatopoeia']),
       ('antithesis', 'something smaller and harder', 'the paired adjectives suggest the request is modest yet requires real commitment', ['simile', 'onomatopoeia', 'statistic'])],
  struct=[('the precise request in the middle of the letter', 'stating exact hours makes the demand concrete and difficult to dismiss'),
          ('the two-sentence ending', 'the contrast between a product that "never sleeps" and the elliptical "Let our students" closes with wit')],
  gq='How do the writers make their request persuasive?',
  gqa=('Thesis: the teachers persuade through restraint, authority and wit. (1) "We teach your users" establishes expertise. (2) The tricolon portrays harm. '
       '(3) A specific, modest request and the elliptical ending make refusal look unreasonable. Evaluation: the open-letter form uses public pressure.'),
  issue='Technology, mental health and corporate responsibility towards young people.',
  concept=('communication', 'the letter contrasts the platform\'s constant communication with students\' need for rest.'),
  read='Parents may sign up in support; the company may see a reasonable, low-cost request it can publicly accept.',
  field='science, technology and the environment')

P(id='accent', kind='letter', title='letter to the editor of a regional newspaper in northern England',
  text=("Sir, – Your columnist last week described our local accent as 'charming but unprofessional'. I have been a nurse for twenty-two years. "
        "I have said 'you're alright, love' to frightened patients at three in the morning, and not one has asked for my vowels to be adjusted. "
        "Accent is not a skill deficit. It is where we come from, and where many of your readers still live."),
  aud='The editor, the columnist and the newspaper\'s regional readers, many of whom share the accent.',
  purp='To rebut a columnist\'s claim that the regional accent is unprofessional and to defend accent as part of identity.',
  ctx='Regional accents in England are sometimes stigmatised in professional settings; letters to the editor give readers a public right of reply.',
  tone='indignant', tw=['grovelling', 'whimsical', 'detached'], tonex='controlled anger is expressed through irony and plain statement.',
  dev=[('quotation of the opponent', "'charming but unprofessional'", 'quoting the columnist exposes the condescension in his phrase before rebutting it', ['onomatopoeia', 'simile', 'anaphora']),
       ('anecdote', "I have said 'you're alright, love' to frightened patients", 'the professional experience proves that the accent comforts rather than harms', ['onomatopoeia', 'statistic', 'oxymoron']),
       ('irony', 'not one has asked for my vowels to be adjusted', 'the absurd image mocks the idea that accent affects competence', ['simile', 'onomatopoeia', 'statistic']),
       ('antithesis', 'Accent is not a skill deficit. It is where we come from', 'the "not X but Y" structure redefines accent as identity and place', ['simile', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the formal opening "Sir, –"', 'the traditional convention gives the letter dignity while its content challenges the paper'),
          ('the final sentence linking accent to readers', 'widening from "I" to "many of your readers" makes the insult a community issue')],
  lang='The dialect endearment "you\'re alright, love" is presented as professional comfort; the writer argues that accent marks regional and class identity and that judging it is prejudice.',
  gq='How does the writer challenge prejudice against regional accents?',
  gqa=('Thesis: the writer turns a dismissive phrase into evidence of prejudice. (1) Quoting the columnist. (2) Professional anecdote with dialect phrase. (3) Irony about "vowels" and antithesis redefining accent. '
       'Evaluation: the letter is brief and personal, so it persuades through credibility rather than research.'),
  issue='Accent prejudice, class and regional identity.',
  concept=('identity', 'accent is presented as part of personal and regional identity.'),
  read='Local readers may feel defended; the columnist\'s supporters may still argue that workplaces need standard English.',
  field='culture, identity and community')

P(id='walk', kind='infographic', title='infographic from an international water charity, described in words',
  text=("[Title in bold blue capitals: 'THE WALK'.] [A single dotted line runs right across the page and ends at a small well icon.]\n"
        "Label beside the line: 'The distance many women and girls in rural areas walk for water each day: up to 6 km.'\n"
        "Below: '20 litres. That's what she carries back – about the weight of a full suitcase.'\n"
        "[Bottom panel: a tap icon.] 'A donation of 25 euros helps bring a tap within 15 minutes of her home.'"),
  aud='Potential donors in wealthier countries who can be moved to give.',
  purp='To make the burden of water collection visible and persuade readers to donate.',
  ctx='Charities often use infographics on social media and websites because they are quick to read and easy to share.',
  tone='sobering', tw=['light-hearted', 'boastful', 'nostalgic'], tonex='plain facts and the image of the walk create a sobering tone.',
  dev=[('statistic', 'up to 6 km', 'a concrete distance quantifies daily labour', ['simile', 'onomatopoeia', 'anaphora']),
       ('comparison', 'about the weight of a full suitcase', 'relating the load to a familiar object makes it imaginable for donors who travel', ['onomatopoeia', 'anaphora', 'rhetorical question']),
       ('pronoun "she"', "That's what she carries back", 'the singular pronoun turns a statistic into an individual woman', ['onomatopoeia', 'simile', 'anaphora'])],
  struct=[('the movement from the dotted line to the tap icon', 'the layout tells a problem–solution story, ending on the donor\'s action'),
          ('the title "THE WALK"', 'naming the burden as a single, definite journey gives it weight')],
  visual='The long dotted line visualises distance and makes the journey feel exhausting; the tap icon at the bottom offers relief, so the reader\'s eye travels from burden to solution.',
  gender='The infographic highlights that water collection falls mostly on women and girls, but also represents them only as burdened recipients of help.',
  gq='How does the infographic use visual and verbal features to persuade its audience?',
  gqa=('Thesis: the infographic converts statistics into a journey the reader can imagine. (1) The dotted line visualises distance. (2) The suitcase comparison and "she" personalise data. '
       '(3) The tap icon and specific donation make the solution feel achievable. Evaluation: effective, but risks representing women only as victims.'),
  issue='Access to clean water and gendered labour.',
  concept=('representation', 'the woman is represented through her burden and the donor as her solution.'),
  read='Donors may feel moved and empowered; a postcolonial reader may question the "saviour" positioning of the reader.',
  field='politics, power and justice')

P(id='sleep', kind='infographic', title='infographic from a national youth health service website, described in words',
  text=("[Headline: 'WHERE DOES YOUR PHONE SLEEP?'] [Two bars side by side: a short purple bar labelled 'Phone in bedroom: 7 h 1 min average sleep' and a taller bar labelled 'Phone outside bedroom: 8 h 3 min'.]\n"
        "[Small moon icons fill the taller bar.] 'Each extra hour of evening screen time = about 15 minutes later to sleep.'\n"
        "[Footer:] 'Charge it outside. Sleep inside.' Source: national youth sleep survey, 2025 (illustrative figures)."),
  aud='Teenagers and their parents visiting a youth health website.',
  purp='To inform young people about the link between phones and sleep and persuade them to charge phones outside the bedroom.',
  ctx='Public-health services increasingly publish shareable graphics aimed at young people; the illustrative figures are for this study task.',
  tone='friendly', tw=['threatening', 'sarcastic', 'grief-stricken'], tonex='the playful question and slogan keep the advice friendly rather than preachy.',
  dev=[('personification', 'WHERE DOES YOUR PHONE SLEEP?', 'giving the phone a bedtime makes the advice playful and memorable', ['statistic', 'onomatopoeia', 'oxymoron']),
       ('antithesis', 'Charge it outside. Sleep inside.', 'the paired opposites form a catchy slogan with a clear instruction', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('statistic', '7 h 1 min average sleep', 'precise figures lend scientific credibility', ['simile', 'onomatopoeia', 'anaphora'])],
  struct=[('the bar comparison placed under the headline', 'the visual difference in bar height communicates the message before any text is read')],
  visual='The taller bar filled with moon icons makes "more sleep" visually attractive; purple and night icons create a calm bedtime mood.',
  gq='How does the infographic encourage young people to change their behaviour?',
  gqa=('Thesis: the infographic combines data and playfulness so advice feels friendly. (1) Personified question. (2) Bar comparison and moon icons. (3) Antithetical slogan. Evaluation: correlation is presented as cause.'),
  issue='Digital technology and young people\'s health.',
  concept=('communication', 'complex data is communicated quickly through visual comparison.'),
  read='A teenager may find it light and acceptable; a statistician may note the graphic implies causation from a correlation.',
  misinfo='Even official graphics can simplify: the bar chart shows a correlation between phones in the bedroom and less sleep but presents it as if it proved cause.',
  field='science, technology and the environment')

P(id='campus', kind='website', title='homepage of a fictional university in Singapore, described in words',
  text=("[Banner photograph: four smiling students of different ethnicities walk across a sunlit lawn; one carries a robotic arm.]\n"
        "Headline: 'Shape What's Next.'\n"
        "Menu bar: Study | Research | Life on Campus | Apply Now – 'Apply Now' is an orange button, the only coloured item.\n"
        "Scrolling ticker: 'Ranked #1 in Asia for graduate employability*'.\n"
        "Pop-up chat window: 'Hi! I'm Ava, your student guide. What would you like to discover today?'"),
  aud='Prospective international students aged 17–19 and their parents.',
  purp='To attract applications by presenting the university as diverse, innovative and a route to employment.',
  ctx='Universities compete globally for fee-paying international students; rankings and employability are key selling points.',
  tone='upbeat', tw=['sombre', 'resentful', 'ominous'], tonex='bright images, exclamation and friendly chat create an upbeat tone.',
  dev=[('imperative', "Shape What's Next.", 'the command flatters the reader as a future innovator', ['statistic', 'simile', 'onomatopoeia']),
       ('superlative claim', "Ranked #1 in Asia for graduate employability*", 'a ranking appeals to parents\' concern with careers; the asterisk hints at qualifications', ['simile', 'onomatopoeia', 'oxymoron']),
       ('direct address', "Hi! I'm Ava, your student guide", 'the chatbot\'s friendly first-person voice simulates personal attention', ['oxymoron', 'onomatopoeia', 'statistic'])],
  struct=[('the single orange "Apply Now" button', 'colour contrast directs the eye to the desired action'),
          ('the scrolling ticker', 'motion draws attention to the ranking without requiring a click')],
  visual='The diverse group walking forwards in sunlight connotes inclusion and progress; the robotic arm signals technological innovation; layout guides the eye from banner to orange button.',
  gq='How does the homepage present the university to prospective students?',
  gqa=('Thesis: the homepage sells a future rather than a place. (1) Banner image of diverse students and technology. (2) Imperative headline and ranking. (3) Interactive chatbot and orange call to action. Evaluation: the claims are general and the asterisk hides detail.'),
  issue='Education as a commodity in a global market.',
  concept=('representation', 'student life is represented as diverse, sunny and career-focused.'),
  read='A student may feel excited; a sceptical parent may look for what the asterisk qualifies.',
  field='beliefs, values and education')

P(id='biscuit', kind='website', title='donation page on an animal-rescue charity\'s website, described in words',
  text=("[Photograph: a one-eyed dog looks straight into the camera.]\n"
        "'Meet Biscuit. He was found tied to a motorway barrier in January.'\n"
        "Progress bar: 'This month: 8,450 euros of 10,000 raised.'\n"
        "Buttons: 10 | 25 | 50 | Other. A pre-ticked box: 'Make this a monthly gift'.\n"
        "Footer: '94 cents of every euro goes directly to animal care.'"),
  aud='Animal lovers browsing the charity\'s site, often arriving from social media.',
  purp='To persuade visitors to donate, ideally monthly.',
  ctx='Online fundraising uses interface design (progress bars, default options) to increase giving.',
  tone='poignant', tw=['jocular', 'aggressive', 'indifferent'], tonex='the named, injured dog makes the page poignant.',
  dev=[('direct address', 'Meet Biscuit.', 'the introduction treats the dog as a person the reader meets, creating empathy', ['statistic', 'onomatopoeia', 'oxymoron']),
       ('statistic', '94 cents of every euro', 'reassures donors that money is used well', ['simile', 'onomatopoeia', 'anaphora']),
       ('emotive detail', 'tied to a motorway barrier in January', 'specific cruelty and winter cold provoke pity and anger', ['statistic', 'onomatopoeia', 'oxymoron'])],
  struct=[('the progress bar near the goal', 'showing the target almost reached encourages visitors to help complete it'),
          ('the pre-ticked monthly box', 'a default option nudges donors into regular giving – an interface choice with ethical questions')],
  visual='Biscuit\'s direct gaze creates a "demand" image that confronts the viewer; the buttons arrange choices from low to high so the middle option feels normal.',
  gq='How does the web page use its design and language to encourage donations?',
  gqa=('Thesis: the page combines an emotional story with interface "nudges". (1) The named dog and direct gaze. (2) Emotive detail. (3) Progress bar, button order and pre-ticked box. Evaluation: the default monthly gift may manipulate donors.'),
  issue='Ethics of persuasion in charity fundraising.',
  concept=('communication', 'the interface itself communicates and persuades, not just the words.'),
  read='An animal lover may give gladly; a critical reader may object to the pre-ticked box as a "dark pattern".',
  field='beliefs, values and education')

P(id='grind', kind='social', title='post by a fitness influencer on a photo-sharing platform',
  text=("5 a.m. Rain. Didn't want to. Did it anyway. [flexed-biceps emoji]\n"
        "Here's the thing nobody tells you: motivation is a myth. Discipline is a decision.\n"
        "Link in bio for my 30-day reset plan (only 40 spots left!!)\n"
        "#grindseason #nooffdays #mindset – 214k likes"),
  aud='Young followers interested in fitness and self-improvement.',
  purp='To inspire followers and sell a paid fitness plan by presenting the influencer as a model of discipline.',
  ctx='Influencer culture blends personal posts with marketing; high like counts act as social proof.',
  tone='motivational', tw=['melancholy', 'apologetic', 'bewildered'], tonex='commands and slogans create a motivational tone.',
  dev=[('minor sentences', "5 a.m. Rain. Didn't want to. Did it anyway.", 'clipped fragments mimic the rhythm of effort and make the influencer seem tough and authentic', ['simile', 'statistic', 'rhetorical question']),
       ('antithesis', 'motivation is a myth. Discipline is a decision.', 'the alliterative pair rejects feeling in favour of will-power in a quotable slogan', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('scarcity appeal', 'only 40 spots left!!', 'limited availability pressures followers to buy', ['simile', 'onomatopoeia', 'anaphora']),
       ('hashtags', '#grindseason #nooffdays #mindset', 'tags place the post in a community and promote an ideology of constant work', ['simile', 'onomatopoeia', 'oxymoron'])],
  struct=[('the shift from personal story to sales link', 'the post moves from authenticity to commerce, using the first to sell the second')],
  lang='Dropped subjects ("Didn\'t want to. Did it anyway."), emoji as tone marker, double exclamation marks and hashtags are typical digital conventions that simulate intimate speech.',
  persona='The influencer constructs an online persona of the disciplined, authentic self; the link in bio and scarcity appeal reveal that the persona is also a brand.',
  gq='How does the influencer construct an online persona to persuade followers?',
  gqa=('Thesis: the post presents authenticity as a product. (1) Fragments perform effort. (2) The antithesis slogan. (3) The scarcity appeal and hashtags turn the persona into marketing. Evaluation: "no off days" may promote unhealthy attitudes.'),
  issue='Wellbeing, hustle culture and the monetised self online.',
  concept=('identity', 'identity online is constructed and performed for an audience.'),
  read='A follower may feel inspired; a critic may see toxic productivity and disguised advertising.',
  field='beliefs, values and education')

P(id='towers', kind='social', title='viral post shared on a messaging app',
  text=("SHARE BEFORE THEY DELETE THIS!!! My cousin's friend works at a hospital and says the new phone masts in our city are making people sick. "
        "The media won't report it. Why? Follow the money. Do your own research. [18.2k shares]"),
  aud='Users in private group chats, especially those already distrustful of authorities or media.',
  purp='To spread alarm and encourage sharing by claiming to reveal hidden information.',
  ctx='Messaging apps make posts hard to fact-check; health rumours about mobile networks spread widely during health scares.',
  tone='alarmist', tw=['calm', 'scholarly', 'whimsical'], tonex='capitals and exclamation marks create alarm.',
  dev=[('capitalisation and exclamation', 'SHARE BEFORE THEY DELETE THIS!!!', 'shouting and the threat of deletion create urgency and suggest censorship', ['simile', 'statistic', 'anaphora']),
       ('vague anecdotal source', "My cousin's friend works at a hospital", 'a second-hand, unverifiable source borrows medical authority without accountability', ['simile', 'onomatopoeia', 'oxymoron']),
       ('rhetorical question', 'Why?', 'the question invites suspicion and implies a conspiracy without evidence', ['simile', 'statistic', 'onomatopoeia']),
       ('imperative cliché', 'Follow the money. Do your own research.', 'familiar slogans flatter readers as independent thinkers while discouraging trust in experts', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the instruction to share placed before the claim', 'the reader is asked to act before evaluating the information')],
  misinfo='Features of misinformation: an urgent instruction to share, a claim of suppression ("they"), an unverifiable second-hand source, no data, and slogans that discredit experts; algorithms and forwarding reward emotional content, so it spreads faster than corrections.',
  lang='The register imitates intimate, informal speech among friends, which makes the claim feel trustworthy within the group.',
  gq='How does the post attempt to persuade readers to believe and share its claim?',
  gqa=('Thesis: the post persuades through urgency and suspicion rather than evidence. (1) Capitals and the deletion threat. (2) The vague hospital source. (3) Rhetorical question and slogans that discredit media. Evaluation: share counts act as false social proof.'),
  issue='Misinformation, trust and public health.',
  concept=('communication', 'communication is shaped by the platform: forwarding rewards speed over accuracy.'),
  read='A frightened reader may share it; a media-literate reader recognises classic misinformation markers.',
  field='science, technology and the environment')

P(id='ia_meme', kind='meme', title='meme shared on a student forum, described in words',
  text=("[Image, top: a tiny kitten stares bravely at an enormous, overflowing laundry basket. Top text: 'ME IN SEPTEMBER: I'LL START MY IA EARLY THIS YEAR'.]\n"
        "[Image, bottom: the same kitten, now buried under the laundry, only its ears showing. Bottom text: 'ME, 11:58 P.M. THE NIGHT BEFORE THE DEADLINE'.]"),
  aud='IB students on a forum who share the experience of internal assessment deadlines.',
  purp='To entertain and build solidarity through shared, self-deprecating humour about procrastination.',
  ctx='Memes circulate quickly among students; "IA" (internal assessment) is in-group vocabulary.',
  tone='self-mocking', tw=['earnest', 'hostile', 'reverent'], tonex='the student laughs at themself.',
  dev=[('juxtaposition', "ME IN SEPTEMBER ... ME, 11:58 P.M. THE NIGHT BEFORE THE DEADLINE", 'placing the confident plan beside the buried kitten creates humour from the gap between intention and reality', ['simile', 'statistic', 'onomatopoeia']),
       ('acronym (in-group language)', 'IA', 'the unexplained abbreviation signals that the meme is for insiders and builds community', ['simile', 'onomatopoeia', 'oxymoron'])],
  struct=[('the two-panel before/after template', 'the familiar structure lets readers decode the joke instantly')],
  visual='The kitten\'s small size against the huge basket visualises being overwhelmed; capital Impact-style text is a meme convention.',
  lang='The template "ME IN ... / ALSO ME" is a recognisable meme formula; in-group acronyms and capitals mark the language of online student communities.',
  persona='The poster performs a relatable, chaotic student identity that invites others to say "same".',
  gq='How does the meme use image and text to create shared humour?',
  gqa=('Thesis: the meme turns individual stress into communal comedy. (1) Before/after template. (2) The kitten as an image of vulnerability. (3) In-group acronym. Evaluation: humour normalises procrastination as well as relieving stress.'),
  issue='Student wellbeing and academic pressure.',
  concept=('identity', 'the meme builds a shared student identity through in-group humour.'),
  read='Students laugh in recognition; a teacher might read it as a sign of workload pressure.',
  field='beliefs, values and education')

P(id='singlish', kind='social', title='post by a Singaporean student on a social media platform',
  text=("Exam results out liao. Physics can lah, but English Lit ah... don't ask. Mum already preparing 'the talk'. "
        "Anyway, who wants bubble tea later? Need sugar to process my life choices."),
  aud='The student\'s friends and followers, mostly Singaporean peers.',
  purp='To share news humorously, seek sympathy and arrange to meet friends.',
  ctx='Singlish, an English-based contact variety with features from Malay, Hokkien and other languages, is widely used informally in Singapore alongside Standard English.',
  tone='humorous', tw=['formal', 'furious', 'tragic'], tonex='self-mockery and light complaints make it humorous.',
  dev=[('discourse particles', 'liao ... lah ... ah', 'Singlish particles signal informality, solidarity and attitude (completion, reassurance, hesitation)', ['simile', 'statistic', 'oxymoron']),
       ('ellipsis', "English Lit ah... don't ask", 'the trailing-off suggests a disappointing result without stating it', ['simile', 'statistic', 'onomatopoeia']),
       ('hyperbole', 'Need sugar to process my life choices', 'exaggeration turns disappointment into comedy', ['statistic', 'onomatopoeia', 'anaphora'])],
  struct=[('the shift to "Anyway"', 'the topic change refuses to dwell on bad news and redirects to friendship')],
  lang='The writer code-switches into Singlish (particles "liao", "lah", "ah"; "can" meaning "was fine") to signal in-group identity and casual intimacy; Standard English would sound distant among friends.',
  persona='The post constructs a relatable, humorous persona that handles stress with irony.',
  gq='How does the writer\'s use of language reflect identity and relationships?',
  gqa=('Thesis: Singlish features build solidarity and a playful persona. (1) Particles signal intimacy. (2) Ellipsis and hyperbole manage disappointment. (3) The shift to bubble tea prioritises friendship. Evaluation: outsiders may misread Singlish as "bad English", revealing language prejudice.'),
  issue='Language, identity and the status of local varieties of English.',
  concept=('identity', 'language choice signals local, generational identity.'),
  read='Singaporean peers read warmth; an outsider or prescriptive reader might see "incorrect" English.',
  field='culture, identity and community')

P(id='kerala', kind='news', title='news report from an international news website',
  text=("Headline: Floods sweep through Kerala villages as monsoon intensifies\n"
        "Standfirst: Thousands evacuated; state officials warn more rain is expected\n"
        "Rescue teams in fishing boats ferried residents from rooftops on Tuesday after three days of heavy rain. "
        "\"We lost everything except our lives,\" said Leela Menon, 63, holding a plastic bag of documents. "
        "The meteorological department has issued a red alert for six districts."),
  aud='A general international readership seeking up-to-date information.',
  purp='To inform readers about the floods quickly and credibly, while engaging them through a human story.',
  ctx='Kerala in south-west India is regularly affected by monsoon flooding; international outlets compete to report breaking news.',
  tone='urgent', tw=['comic', 'nostalgic', 'sarcastic'], tonex='dynamic verbs and immediate detail create urgency.',
  dev=[('dynamic verb', 'Floods sweep through', '"sweep" conveys speed and force in the headline', ['simile', 'rhetorical question', 'anaphora']),
       ('eyewitness quotation', '"We lost everything except our lives,"', 'a named survivor\'s words humanise the story and add emotion within a neutral report', ['simile', 'onomatopoeia', 'oxymoron']),
       ('concrete detail', 'holding a plastic bag of documents', 'the small image suggests what people save when everything else is lost', ['onomatopoeia', 'oxymoron', 'rhetorical question'])],
  struct=[('the inverted pyramid', 'the most important facts (what, where, when) come first, with human detail and official warnings after'),
          ('the standfirst', 'it summarises the story and adds the official warning, so a skimming reader gets the essentials')],
  gq='How does the report balance information and human interest?',
  gqa=('Thesis: the report uses news conventions to inform and a single human voice to move. (1) Headline verb and standfirst. (2) Inverted pyramid. (3) The quotation and concrete detail. Evaluation: one quoted victim may stand in for many, and the framing focuses on disaster rather than causes.'),
  issue='Climate change, disaster and how news represents those affected.',
  concept=('representation', 'victims are represented through one dignified, quoted individual.'),
  read='Readers may sympathise; a critical reader may ask why causes (climate, planning) are absent.',
  field='science, technology and the environment')

P(id='headlines', kind='news', title='pair of headlines and opening lines from two newspapers reporting the same student protest',
  text=("Newspaper A: 'Thousands of students march for affordable housing' – Students filled the city centre on Saturday, chanting and carrying handmade banners, to demand rent controls.\n"
        "Newspaper B: 'Student mob brings city centre to standstill' – Shoppers were left stranded on Saturday as crowds of students blocked roads, causing chaos for local businesses."),
  aud='Readers of two newspapers with different political leanings.',
  purp='Both inform readers of the protest, but each frames it to shape the reader\'s attitude – sympathetic (A) or hostile (B).',
  ctx='News outlets often reflect the values of their owners and readerships; protest coverage shows how framing shapes public opinion.',
  tone='contrasting', tw=['identical', 'poetic', 'comic'], tonex='A is sympathetic, B hostile.',
  dev=[('loaded noun', 'Student mob', '"mob" connotes violence and irrationality, delegitimising the protesters', ['simile', 'statistic', 'onomatopoeia']),
       ('purpose clause', 'to demand rent controls', 'Newspaper A states the protesters\' aim, presenting them as rational citizens', ['simile', 'onomatopoeia', 'oxymoron']),
       ('framing through victims', 'Shoppers were left stranded', 'Newspaper B centres inconvenience to shoppers, so the protest is seen as harm', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the choice of grammatical subject', 'A makes students the active subject with a goal; B makes the "mob" the cause of chaos and shoppers the victims')],
  gq='How do the two newspapers shape readers\' opinions of the same event?',
  gqa=('Thesis: the same facts are framed as civic action (A) and disruption (B). (1) Diction: "march" versus "mob". (2) Whose perspective is centred. (3) A includes the demand; B omits it. Evaluation: neither is strictly false; framing operates through selection and connotation.'),
  issue='Media bias, framing and the right to protest.',
  concept=('perspective', 'each outlet presents the event from a different ideological perspective.'),
  read='Readers tend to accept the frame of the paper they already trust – a form of confirmation bias.',
  field='politics, power and justice')

P(id='dinner', kind='cartoon', title='single-panel editorial cartoon, described in words',
  text=("[A giant smartphone towers over a family dinner table like a skyscraper. The parents and two children sit at its base, each gazing up at its glowing screen. "
        "Their plates are untouched. Under the table, the family dog looks up at the reader. Speech bubble from the dog: 'Remember when they used to drop food?']"),
  aud='Newspaper readers, especially parents, who will recognise the scene.',
  purp='To criticise, through humour, the way smartphones dominate family life.',
  ctx='Editorial cartoons comment on current social concerns; screen time and family life are common topics.',
  tone='satirical', tw=['reverent', 'neutral', 'tragic'], tonex='exaggeration and the dog\'s joke make it satirical.',
  dev=[('exaggeration (hyperbole)', 'A giant smartphone towers over a family dinner table like a skyscraper', 'the absurd scale shows the phone\'s dominance over family life', ['statistic', 'onomatopoeia', 'anaphora']),
       ('ironic speech bubble', "'Remember when they used to drop food?'", 'the dog\'s nostalgic complaint is a comic outsider\'s view of family neglect', ['statistic', 'simile', 'anaphora'])],
  struct=[('the placement of the dog looking out at the reader', 'it breaks the frame and makes the reader complicit in the joke')],
  visual='Vertical scale (the phone as skyscraper) versus tiny people creates a power relationship; untouched plates suggest neglected nourishment and togetherness.',
  gq='How does the cartoon use humour to comment on technology and family life?',
  gqa=('Thesis: the cartoon makes a familiar habit absurd. (1) Hyperbolic scale. (2) Untouched plates and upward gazes as worship. (3) The dog as ironic narrator. Evaluation: gentle satire; it amuses rather than accuses.'),
  issue='Technology and family relationships.',
  concept=('perspective', 'the dog\'s outsider perspective makes human behaviour look strange.'),
  read='Parents may laugh guiltily; teenagers may notice the parents are just as absorbed.',
  field='science, technology and the environment')

P(id='floe', kind='cartoon', title='three-panel comic strip, described in words',
  text=("[Panel 1: a world leader at a podium declares, 'We pledge to reach net zero by 2050!' Applause lines fill the background.]\n"
        "[Panel 2: a polar bear on a shrinking ice floe raises a paw: 'Question – what's the plan for this summer?']\n"
        "[Panel 3: the leader, sweating, looks away: 'Next question.']"),
  aud='Readers of a news website, concerned about climate change and political inaction.',
  purp='To satirise long-term climate pledges that avoid immediate action.',
  ctx='Many governments have set distant net-zero targets; critics argue that near-term action is lacking.',
  tone='satirical', tw=['admiring', 'neutral', 'sentimental'], tonex='the bear\'s polite question exposes the leader – satire.',
  dev=[('anthropomorphism', 'a polar bear on a shrinking ice floe raises a paw', 'the bear behaves like a journalist, giving the affected environment a voice', ['statistic', 'onomatopoeia', 'oxymoron']),
       ('irony', "'Next question.'", 'the evasion confirms that there is no immediate plan', ['statistic', 'simile', 'onomatopoeia'])],
  struct=[('the three-panel set-up, question and punchline', 'comic timing builds from confident pledge to exposed evasion')],
  visual='The shrinking floe beside the podium visualises urgency against political theatre; the sweating leader signals discomfort.',
  gq='How does the comic strip criticise political responses to climate change?',
  gqa=('Thesis: the strip contrasts distant promises with present danger. (1) Pledge and applause as performance. (2) The bear as questioner. (3) Evasion as punchline. Evaluation: effective simplification, though it treats all pledges as empty.'),
  issue='Climate change and political accountability.',
  concept=('perspective', 'the non-human perspective of the bear exposes political time-scales.'),
  read='Activists will share it approvingly; a politician might call it unfair simplification.',
  field='science, technology and the environment')

P(id='iceland', kind='brochure', title='extract from a travel brochure for a tour of Iceland',
  text=("Where fire meets ice. Stand where continents drift apart at Thingvellir. Soak beneath the northern lights in steaming geothermal pools. "
        "Let the silence of a black-sand beach rewrite your idea of quiet. This isn't a holiday. It's a reset. "
        "Small groups. Expert local guides. Carbon-offset flights."),
  aud='Affluent travellers seeking adventure and wellbeing, possibly environmentally conscious.',
  purp='To persuade readers to book the tour by presenting Iceland as dramatic, restorative and responsible.',
  ctx='Iceland\'s tourism has grown rapidly; brochures increasingly stress small groups and carbon offsets to reassure eco-conscious travellers.',
  tone='evocative', tw=['bureaucratic', 'cynical', 'anxious'], tonex='sensory imagery creates an evocative tone.',
  dev=[('antithesis', 'Where fire meets ice', 'the opposites capture Iceland\'s volcanic and glacial landscape and promise drama', ['simile', 'statistic', 'rhetorical question']),
       ('imperative', 'Stand where continents drift apart', 'commands place the reader inside the experience', ['simile', 'statistic', 'onomatopoeia']),
       ('personification', 'Let the silence of a black-sand beach rewrite your idea of quiet', 'silence becomes an active force that transforms the visitor', ['statistic', 'onomatopoeia', 'anaphora']),
       ('antithesis', "This isn't a holiday. It's a reset.", 'redefining the trip as self-transformation raises its value', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the shift to verbless fragments at the end', '"Small groups. Expert local guides. Carbon-offset flights." delivers practical reassurance in a quick list after the dream')],
  gq='How does the brochure create a desirable image of Iceland?',
  gqa=('Thesis: the brochure sells transformation, not sightseeing. (1) Antithesis of fire and ice. (2) Imperatives and sensory imagery immerse the reader. (3) The "reset" redefinition and eco-reassurance. Evaluation: the carbon-offset line eases guilt about flying.'),
  issue='Tourism, wellbeing and environmental impact.',
  concept=('representation', 'Iceland is represented as wild, empty and healing – largely without its inhabitants.'),
  read='A stressed professional may long to go; an Icelandic reader may notice that locals appear only as "guides".',
  field='science, technology and the environment')

P(id='lange', kind='photo', title="description of Dorothea Lange's photograph 'Migrant Mother' (1936) with its original caption",
  text=("[A black-and-white photograph. A woman in worn clothes sits under a tent, her hand raised to her chin, her eyes looking past the camera with a worried expression. "
        "Two children lean on her shoulders, faces turned away; a baby lies in her lap. The frame is tight, cutting out the surroundings.]\n"
        "Caption (US Farm Security Administration file): 'Destitute pea pickers in California. Mother of seven children. Age thirty-two. Nipomo, California.'"),
  aud='Originally the American public and policymakers in the 1930s, reached through newspapers; now museum visitors and students.',
  purp='To document rural poverty and build public support for government relief programmes during the Great Depression.',
  ctx='Lange worked for the Farm Security Administration, a New Deal agency that commissioned photographs of poverty; the image became an icon of the Depression. The woman, Florence Owens Thompson, was not named at the time and later said she gained nothing from its fame.',
  tone='sombre', tw=['jubilant', 'playful', 'triumphant'], tonex='the worried gaze and poverty create a sombre mood.',
  dev=[('tight framing', 'The frame is tight, cutting out the surroundings', 'cropping concentrates attention on the mother\'s face and the dependent children, universalising her', ['statistic', 'onomatopoeia', 'simile']),
       ('averted gaze', 'her eyes looking past the camera', 'the gaze into the distance suggests worry about the future rather than a posed portrait', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('caption as anchorage', "'Destitute pea pickers in California. Mother of seven children.'", 'the terse caption fixes the meaning as poverty and dignity, but reduces the woman to a type', ['simile', 'onomatopoeia', 'anaphora'])],
  struct=[('the triangular composition of mother and children', 'it recalls religious images of mother and child, giving the subject dignity')],
  visual='The hand at the chin, the triangular composition and the turned-away children concentrate emotion on the mother\'s face; black-and-white tones emphasise documentary seriousness.',
  gq='How does the photograph and its caption represent poverty?',
  gqa=('Thesis: the image turns one woman into a symbol of a national crisis. (1) Tight framing and composition. (2) Averted gaze. (3) The caption\'s anonymity. Evaluation: powerful advocacy, but it raises ethical questions about consent and the subject\'s lack of voice.'),
  issue='Poverty, representation and the ethics of documentary photography.',
  concept=('representation', 'a real individual is represented as a symbol of poverty, losing her own name.'),
  read='1930s viewers saw a call for relief; modern readers also ask whose story it is and who benefited.',
  field='politics, power and justice')

P(id='rina', kind='photo', title='photograph and caption from a contemporary documentary series on fast fashion, described in words',
  text=("[A young woman sits at a sewing machine in a long row of identical machines under flickering fluorescent light. In the blurred foreground lies a heap of bright T-shirts with price tags reading '4.99'.]\n"
        "Caption: 'Shift 2 of 2. Rina, 19, sews 120 collars an hour.'"),
  aud='Readers of a magazine or exhibition visitors in consumer countries.',
  purp='To expose the human labour behind cheap clothing and prompt reflection on consumption.',
  ctx='Fast fashion relies on low-wage garment production; documentary photography has been used to campaign for workers\' rights.',
  tone='stark', tw=['whimsical', 'celebratory', 'nostalgic'], tonex='the bare caption and harsh light make it stark.',
  dev=[('foreground/background contrast', 'a heap of bright T-shirts with price tags', 'cheap, colourful products in the foreground set against the worker behind them link consumer and producer', ['onomatopoeia', 'rhetorical question', 'simile']),
       ('repetition of form', 'a long row of identical machines', 'the repeated machines suggest mechanised, dehumanising labour', ['onomatopoeia', 'statistic', 'rhetorical question']),
       ('statistic in caption', 'sews 120 collars an hour', 'a precise rate conveys relentless pace', ['simile', 'onomatopoeia', 'anaphora'])],
  struct=[('the caption naming the worker', '"Rina, 19" gives her a name and age, resisting anonymity')],
  visual='Fluorescent light and repetition create a cold, industrial mood; selective focus blurs the products and sharpens the worker, shifting attention from goods to the person.',
  gq='How does the photograph make the viewer reconsider cheap clothing?',
  gqa=('Thesis: the image connects the price tag to the person. (1) Foreground/background composition. (2) Repetition of machines. (3) Naming caption with statistic. Evaluation: naming Rina restores individuality, unlike older documentary practice.'),
  issue='Labour exploitation and consumer responsibility in global supply chains.',
  concept=('representation', 'the worker is represented as an individual with a name, not just a statistic.'),
  read='A shopper may feel guilt; an economist may argue the jobs still matter to the local economy.',
  field='politics, power and justice')

# ---------------- literary passages ----------------
P(id='river', kind='prose', title='opening of a novel (an original extract written for study)',
  text=("The summer the river went quiet, Papa started sleeping in the afternoons. Mama said he was tired from the factory, but the factory had stopped making its noise too, "
        "so I did not see how. I counted the boats that didn't come. Fourteen on Monday. On Tuesday I stopped counting, because Mama said numbers were for people with jobs."),
  pov='First-person child narrator, probably retrospective ("The summer the river went quiet"). The narrator does not understand what the reader infers – that Papa has lost his job – so the naive voice creates dramatic irony and pathos.',
  char='Characters are revealed indirectly: Papa\'s afternoon sleeping suggests depression or shame; Mama\'s evasive explanation and sharp remark ("numbers were for people with jobs") show protectiveness strained by anxiety; the child copes by counting.',
  setting='The silent river and factory evoke an industrial town in economic decline; the silence of the setting mirrors the silence within the family.',
  symbol='The quiet river and silenced factory symbolise the loss of livelihood; counting the absent boats becomes a motif for measuring loss.',
  time='The retrospective opening frames the summer as significant; the short time markers (Monday, Tuesday) compress days and build towards the revealing final remark.',
  tone='melancholy', tw=['exuberant', 'satirical', 'triumphant'], tonex='quiet details of loss create melancholy.',
  dev=[('pathetic fallacy', 'The summer the river went quiet', 'the silent river reflects the family\'s situation and mood', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('minor sentence', 'Fourteen on Monday.', 'the fragment mimics a child\'s matter-of-fact counting and emphasises absence', ['simile', 'rhetorical question', 'oxymoron'])],
  struct=[('the final sentence', 'Mama\'s remark reveals the job loss obliquely and ends the paragraph on adult bitterness')],
  gq='How does the writer use a child narrator to convey a family crisis?',
  gqa=('Thesis: the naive narrator lets the reader understand more than the child, creating pathos. (1) Indirect characterisation of Papa and Mama. (2) Setting as mirror (silent river and factory). (3) The counting motif and final remark. Evaluation: understatement makes the crisis more affecting.'),
  issue='Unemployment, economic decline and its effect on families.',
  concept=('perspective', 'the child\'s limited perspective shapes what is revealed and withheld.'),
  read='Readers may focus on economic hardship or on the child\'s psychological coping.',
  field='politics, power and justice')

P(id='margit', kind='prose', title='extract from a novel (an original extract written for study)',
  text=("Margit checked the oven again. Six o'clock. He had said six. The table was set for two, the good glasses out, the candles not yet lit – no point lighting candles for nobody. "
        "Of course he would be late; he was always late, and she always forgave him, and that was the arrangement, wasn't it? She lit the candles anyway. Let them burn."),
  pov='Third-person limited narration using free indirect discourse: phrases such as "no point lighting candles for nobody" and "wasn\'t it?" blend the narrator\'s voice with Margit\'s thoughts, giving intimate access to her resentment.',
  char='Margit is characterised through actions (checking the oven, setting good glasses) and thoughts: she is hopeful, then resentful and resigned to an unequal "arrangement"; lighting the candles shows a small act of defiance.',
  setting='The domestic setting – oven, table for two, good glasses – shows effort and expectation within a confined, private space.',
  symbol='The candles symbolise hope and romance, then time passing and defiance; "Let them burn" suggests both waste and refusal to wait.',
  time='Clock time ("Six o\'clock. He had said six.") creates tension; the short sentences slow the moment of waiting.',
  tone='resentful', tw=['jubilant', 'detached', 'comic'], tonex='Margit\'s thoughts reveal resentment beneath patience.',
  dev=[('free indirect discourse', "that was the arrangement, wasn't it?", 'the tag question is Margit\'s voice inside the narration, revealing bitterness', ['statistic', 'onomatopoeia', 'simile']),
       ('polysyndeton', 'he was always late, and she always forgave him, and that was the arrangement', 'the repeated "and" conveys the tired repetition of the pattern', ['simile', 'onomatopoeia', 'statistic']),
       ('symbol', 'Let them burn.', 'the final candles become an image of defiance and waste', ['statistic', 'onomatopoeia', 'rhetorical question'])],
  struct=[('short opening sentences', 'they mimic Margit\'s anxious clock-watching'), ('the ending imperative', '"Let them burn" closes on her decision, shifting from waiting to defiance')],
  gq='How does the writer reveal Margit\'s feelings about her relationship?',
  gqa=('Thesis: through free indirect discourse the writer exposes resentment beneath domestic care. (1) Setting and preparation. (2) Polysyndeton and tag question. (3) The candle symbol and final imperative. Evaluation: the absent man is characterised only through Margit\'s waiting, which centres her experience.'),
  issue='Gender roles and emotional labour in relationships.',
  concept=('identity', 'Margit\'s identity is defined by waiting – the extract hints at her resisting this.'),
  read='One reader sees quiet defiance; another sees resignation dressed as defiance.',
  field='culture, identity and community')

P(id='isidro', kind='prose', title='opening of a novel (an original extract written for study)',
  text=("In the town of San Isidro, where the wind came down from the mountains every afternoon at four, nobody owned a clock that told the right time. "
        "The church bell rang when the priest woke, the bus left when the driver had finished his coffee, and the mayor's promises arrived, like the rain, mostly in other people's towns."),
  pov='Third-person omniscient narrator with an ironic, communal voice that surveys the whole town and comments on its habits.',
  char='Characters (priest, driver, mayor) are sketched as types through a single habit each; the mayor is satirised through the simile linking his promises to rain that falls elsewhere.',
  setting='The isolated mountain town, where time is personal rather than official, is established as a place slightly outside modern order, with a hint of magical realism.',
  symbol='The clocks that never tell the right time symbolise the town\'s detachment from official, national time and its own rhythms.',
  time='The iterative "every afternoon at four" establishes habitual time rather than a single event, introducing a world before the plot begins.',
  tone='gently ironic', tw=['furious', 'despairing', 'clinical'], tonex='the narrator\'s affectionate mockery is gently ironic.',
  dev=[('simile', "like the rain, mostly in other people's towns", 'the comparison satirises political promises that never benefit the town', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('tricolon', 'The church bell rang ..., the bus left ..., and the mayor\'s promises arrived', 'the list builds a comic rhythm and climaxes in political satire', ['statistic', 'onomatopoeia', 'oxymoron'])],
  struct=[('the long, flowing sentences', 'they create a leisurely storytelling voice that matches the town\'s slow time')],
  gq='How does the opening establish the town and the narrator\'s attitude to it?',
  gqa=('Thesis: the omniscient narrator creates an affectionately ironic portrait of a town outside official time. (1) The clock motif. (2) The tricolon of habits. (3) The political simile. Evaluation: humour hints at neglect by central government.'),
  issue='Rural communities, political neglect and modernity.',
  concept=('culture', 'local customs of time are presented as a distinct community culture.'),
  read='Some readers enjoy the whimsy; others read sharp political criticism.',
  field='politics, power and justice')

P(id='borrowed', kind='prose', title='extract from a novel narrated in the first person (an original extract written for study)',
  text=("I want to be clear that I did not take the money. I borrowed it, which is different, and I would have returned it on Friday if Friday had gone the way Fridays usually go. "
        "Anyone would have done the same. Ask anyone. Ask my brother – no, don't ask my brother; he has always exaggerated."),
  pov='First-person unreliable narrator: the self-justifying tone, euphemism ("borrowed") and the hurried correction about the brother signal that the reader should doubt the account.',
  char='The narrator is characterised through voice – defensive, evasive and anxious to control the story; the brother is implied to know the truth.',
  setting='Setting is almost absent; the focus on voice suggests a confession or testimony.',
  symbol='The money is less a symbol than a test of the narrator\'s honesty.',
  time='The conditional ("if Friday had gone...") shows the narrator rewriting events; the reader senses an earlier incident retold.',
  tone='defensive', tw=['serene', 'joyful', 'reverent'], tonex='self-justification creates a defensive tone.',
  dev=[('euphemism', 'I borrowed it, which is different', 'the softer word attempts to reframe theft, exposing the narrator\'s self-deception', ['statistic', 'onomatopoeia', 'simile']),
       ('self-correction', "Ask my brother – no, don't ask my brother", 'the dash marks a panicked reversal that reveals the narrator fears contradiction', ['statistic', 'simile', 'onomatopoeia'])],
  struct=[('the opening "I want to be clear"', 'the insistence on clarity ironically warns that the account is unclear')],
  gq='How does the writer make the reader distrust the narrator?',
  gqa=('Thesis: the narrator\'s attempts to control the story reveal unreliability. (1) The opening insistence. (2) Euphemism. (3) Self-correction about the brother. Evaluation: humour makes the narrator sympathetic despite dishonesty.'),
  issue='Truth, self-deception and responsibility.',
  concept=('perspective', 'the single, biased perspective is exposed to the reader.'),
  read='Readers may laugh at or pity the narrator; a few might believe him at first.',
  field='beliefs, values and education')

P(id='signs', kind='prose', title='extract from a novel (an original extract written for study)',
  text=("Afterwards, everyone would say that the signs had been there. The dog that refused to go into the barn. The letter Tomás never opened, propped against the salt jar for a week. "
        "But that morning was ordinary: eggs, rain, the radio murmuring about prices in the capital. Nobody looks for signs on an ordinary morning."),
  pov='Third-person narrator who knows the future ("Afterwards, everyone would say"), giving a retrospective, communal perspective.',
  char='Tomás is characterised through one unopened letter – avoidance or fear.',
  setting='The ordinary domestic morning (eggs, rain, radio) contrasts with the coming disaster.',
  symbol='The unopened letter and the dog refusing to enter the barn work as ominous symbols.',
  time='Prolepsis (flash-forward) – "Afterwards" – reveals that something terrible will happen, so suspense comes from how, not whether; the fragments list the signs.',
  tone='ominous', tw=['jubilant', 'light-hearted', 'flippant'], tonex='foreshadowing makes the ordinary scene ominous.',
  dev=[('foreshadowing (prolepsis)', 'Afterwards, everyone would say that the signs had been there', 'the narrator reveals that disaster is coming, creating suspense and dread', ['simile', 'statistic', 'onomatopoeia']),
       ('asyndetic list', 'eggs, rain, the radio murmuring about prices', 'the plain list makes the morning feel mundane and unguarded', ['simile', 'oxymoron', 'rhetorical question'])],
  struct=[('the fragments listing the signs', 'they isolate each ominous detail like evidence')],
  gq='How does the writer create tension in this extract?',
  gqa=('Thesis: tension comes from the gap between foreknowledge and ordinariness. (1) Prolepsis. (2) Ominous fragments. (3) The mundane list and final generalisation. Evaluation: dread rather than surprise, as in Chronicle-of-a-death style narratives.'),
  issue='Fate, warning and collective responsibility.',
  concept=('perspective', 'a retrospective, communal perspective frames the story.'),
  read='Readers anticipate disaster; some may read the community\'s "everyone would say" as guilt.',
  field='beliefs, values and education')

P(id='suitcase', kind='poem', title="poem 'Suitcase' (an original poem written for study)",
  text=("Suitcase\n\nMy mother packed the country in a suitcase:\ntwo spoons, one photograph, a jar of soil\nthat customs took. She did not argue.\nShe had already lost the bigger things.\n\n"
        "Now she waters basil on a London sill\nand talks to it in a language\nthe neighbours think is weather."),
  form='Free verse in two stanzas, a quatrain and a tercet; the stanza break marks the shift from past departure to present life, and enjambment ("a jar of soil / that customs took") delays the loss.',
  imagery='The metaphor "packed the country in a suitcase" compresses migration into a small object; the confiscated "jar of soil" symbolises the homeland that cannot be carried; the final image of a language "the neighbours think is weather" shows her speech as background noise to others.',
  sound='Plain diction and soft sibilance ("basil", "sill") create quietness; the short sentence "She did not argue." is flat and restrained.',
  speaker='The speaker is the child of a migrant observing the mother with tenderness; restraint and understatement convey grief without stating it.',
  tone='restrained', tw=['jubilant', 'sarcastic', 'hysterical'], tonex='understatement creates restrained sorrow.',
  dev=[('metaphor', 'My mother packed the country in a suitcase', 'it shows how migration reduces a whole homeland to a few objects', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('enjambment', 'a jar of soil / that customs took', 'the line break delays the loss, mimicking the shock', ['simile', 'rhetorical question', 'statistic']),
       ('understatement', 'She had already lost the bigger things.', 'the plain statement implies great losses without naming them', ['simile', 'onomatopoeia', 'statistic'])],
  struct=[('the stanza break between past and present', 'it separates departure and new life, but the second stanza shows the old language persisting')],
  gq='How does the poet present the experience of migration?',
  gqa=('Thesis: the poem conveys migration as loss carried quietly. (1) The suitcase metaphor and confiscated soil. (2) Understatement and enjambment. (3) The final image of unheard language. Evaluation: restraint makes the grief more powerful.'),
  issue='Migration, displacement and cultural identity.',
  concept=('identity', 'the mother\'s identity persists through language and the basil.'),
  read='Readers may focus on loss or on resilience (the basil grows).',
  field='culture, identity and community')

P(id='lighthouse', kind='poem', title="poem 'The Lighthouse Keeper's Daughter' (an original poem written for study)",
  text=("The Lighthouse Keeper's Daughter\n\nShe learned the sea before her name,\nthe way it hushed, the way it roared;\nshe learned that light is not a flame\nbut something patient, kept, restored.\n\n"
        "Now ships go by on satellite,\nthe tower's lamp is switched by phone;\nshe climbs the stairs most nights to light\na dark that no one calls her own."),
  form='Two quatrains in iambic tetrameter with alternate rhyme (ABAB CDCD); the regular form mirrors the discipline of keeping the light, and the turn at "Now" contrasts past vocation with automated present.',
  imagery='The sea is personified ("hushed", "roared"); light is redefined as "patient, kept, restored" – care rather than fire; the closing image of lighting "a dark that no one calls her own" suggests purposeless devotion.',
  sound='Regular rhythm, full rhymes (name/flame, roared/restored) and the soft sounds of "hushed" create a steady, ritual music; the contrast with "satellite" and "phone" introduces modern, mechanical diction.',
  speaker='A third-person speaker observes the daughter with sympathy; the tone moves from reverent to elegiac.',
  tone='elegiac', tw=['triumphant', 'sarcastic', 'frantic'], tonex='the loss of purpose creates an elegiac tone.',
  dev=[('personification', 'the way it hushed, the way it roared', 'giving the sea human sounds shows intimacy with it', ['statistic', 'rhetorical question', 'onomatopoeia']),
       ('tricolon', 'patient, kept, restored', 'the three adjectives define light as care and duty', ['simile', 'rhetorical question', 'statistic']),
       ('volta', 'Now ships go by on satellite', 'the turn shifts from tradition to technology', ['simile', 'onomatopoeia', 'statistic'])],
  struct=[('the rhyme scheme and regular metre', 'the order mirrors routine and makes the final line\'s emptiness more poignant')],
  gq='How does the poet use form to explore the effect of technology on tradition?',
  gqa=('Thesis: strict form embodies the ritual that technology has made unnecessary. (1) Metre and rhyme as discipline. (2) The volta "Now" and modern diction. (3) The final image of purposeless devotion. Evaluation: nostalgic but also questions identity tied to work.'),
  issue='Technology, work and the loss of traditional roles.',
  concept=('transformation', 'technology transforms the daughter\'s inherited role.'),
  read='One reader sees loyalty; another sees inability to move on.',
  field='science, technology and the environment')

P(id='seoul', kind='poem', title="poem 'Rush Hour, Seoul' (an original poem written for study)",
  text=("Rush Hour, Seoul\n\nClick of turnstiles, clack of heels,\nthe subway swallows, swallows, steals\na thousand faces, folds them tight –\nthen spits them, blinking, into light."),
  form='A single quatrain in rhyming couplets (AABB) with a mostly trochaic/iambic four-beat line; the compression mirrors the crush of bodies.',
  imagery='The subway is personified as a mouth that "swallows", "steals" and "spits", turning commuters into food; "folds them tight" suggests compression and loss of individuality.',
  sound='Onomatopoeia ("Click", "clack"), alliteration and sibilance ("subway swallows, swallows, steals") and the harsh plosive "spits" create the noisy, mechanical rhythm of the station.',
  speaker='An observing speaker, detached and slightly ironic, watching the crowd.',
  tone='frenetic', tw=['tranquil', 'mournful', 'reverent'], tonex='rapid sounds create a frenetic energy.',
  dev=[('onomatopoeia', 'Click of turnstiles, clack of heels', 'the hard sounds recreate the station\'s noise', ['statistic', 'rhetorical question', 'simile']),
       ('personification', 'the subway swallows, swallows, steals', 'the subway becomes a devouring creature', ['statistic', 'rhetorical question', 'simile']),
       ('repetition', 'swallows, swallows', 'the repeated verb mimics the rhythm of trains and the endless flow of people', ['statistic', 'simile', 'rhetorical question'])],
  struct=[('the single sentence across four lines', 'one breathless sentence enacts the rush')],
  gq='How does the poet use sound to convey the experience of the city?',
  gqa=('Thesis: sound patterning makes the reader hear and feel the crowd. (1) Onomatopoeia. (2) Sibilant personification. (3) Couplet rhyme and the final release into "light". Evaluation: brief but vivid; the ending suggests disorientation rather than freedom.'),
  issue='Urban life, work and individuality.',
  concept=('representation', 'commuters are represented as anonymous matter consumed by the city.'),
  read='Some readers see dehumanisation; others enjoy the poem\'s energy.',
  field='science, technology and the environment')

P(id='statue', kind='poem', title="poem 'The Statue Speaks' (an original poem written for study)",
  text=("The Statue Speaks\n\nThey raised me in the square in 1889\nand gave me a sword I never held in life.\nEach spring the children climb me for photographs.\nEach autumn someone paints my hands red.\n"
        "I do not mind. I was a merchant, mostly.\nThe war they carved me for was mostly other people's."),
  form='A dramatic monologue in free verse; long, prose-like lines and plain statements suit a conversational persona.',
  imagery='The sword "I never held" exposes the myth-making of public monuments; the red-painted hands suggest protest and accusations of bloodshed.',
  sound='The flat rhythm and repetition of "mostly" create deadpan irony.',
  speaker='The persona is the statue of a historical figure, who undermines his own heroic image; the poet uses the persona to question how history is commemorated.',
  tone='wry', tw=['grandiose', 'hysterical', 'ecstatic'], tonex='the statue\'s understatement is wry.',
  dev=[('persona (dramatic monologue)', 'They raised me in the square in 1889', 'speaking as the statue allows the monument to comment on its own meaning', ['statistic', 'simile', 'onomatopoeia']),
       ('anaphora', 'Each spring ... Each autumn', 'the repeated opening shows the cycles of affection and protest the statue receives', ['simile', 'statistic', 'onomatopoeia']),
       ('irony', 'I was a merchant, mostly.', 'the anticlimax undermines the heroic myth', ['simile', 'onomatopoeia', 'statistic'])],
  struct=[('the last line', 'it reveals that the commemorated war was not his own, undermining the monument\'s purpose')],
  gq='How does the poet use the statue\'s voice to question history?',
  gqa=('Thesis: the persona deflates the heroic myth of public memory. (1) Dramatic monologue. (2) Contrasting seasonal rituals. (3) Ironic understatement. Evaluation: relevant to debates about contested monuments.'),
  issue='Memory, power and contested monuments.',
  concept=('representation', 'the statue questions how the past is represented in public spaces.'),
  read='Some read humour; others read a critique of colonial or militaristic commemoration.',
  field='politics, power and justice')

P(id='radios', kind='poem', title="poem 'For My Grandfather, Who Fixed Radios' (an original poem written for study)",
  text=("For My Grandfather, Who Fixed Radios\n\nHis hands knew static the way a farmer knows rain:\npatient, listening for the voice inside the noise.\nThe day he died, I turned the dial\n"
        "through every station in the city,\nand every one was speaking,\nand none of them was him."),
  form='A short elegy in free verse; the poem moves from portrait (lines 1–2) to the speaker\'s act of mourning (lines 3–6).',
  imagery='The simile "the way a farmer knows rain" gives the grandfather\'s skill patience and closeness to nature; "the voice inside the noise" is a metaphor for finding meaning – and for the speaker\'s search for him.',
  sound='Polysyndeton ("and every one ... and none") slows the ending; the repeated "every" builds to the stark "none".',
  speaker='The grandchild speaks in the first person, revealing grief through action rather than statement.',
  tone='grieving', tw=['flippant', 'ironic', 'exultant'], tonex='the final line conveys quiet grief.',
  dev=[('simile', 'the way a farmer knows rain', 'it presents the skill as patient, intimate knowledge', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('polysyndeton', 'and every one was speaking, / and none of them was him', 'the repeated "and" slows the poem towards its painful conclusion', ['simile', 'statistic', 'rhetorical question']),
       ('metaphor', 'the voice inside the noise', 'it captures repair work and the speaker\'s search for meaning in grief', ['statistic', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the turn at "The day he died"', 'the poem shifts from portrait to absence')],
  gq='How does the poet convey grief?',
  gqa=('Thesis: grief is conveyed through the grandfather\'s own craft. (1) Simile and metaphor of listening. (2) The act of turning the dial. (3) Polysyndeton and the final "none". Evaluation: understatement avoids sentimentality.'),
  issue='Grief, memory and family.',
  concept=('identity', 'the grandfather\'s identity is bound to his craft.'),
  read='Readers may focus on grief or on the inherited skill of listening.',
  field='culture, identity and community')

P(id='owen', kind='poem', title="opening lines of Wilfred Owen's 'Dulce et Decorum Est' (written 1917, published 1920)",
  text=("Bent double, like old beggars under sacks,\nKnock-kneed, coughing like hags, we cursed through sludge,\nTill on the haunting flares we turned our backs\nAnd towards our distant rest began to trudge."),
  form='The lines are in roughly iambic pentameter with alternate rhyme (ABAB), but the rhythm is broken by heavy stresses and caesuras, enacting the soldiers\' exhaustion.',
  imagery='Similes compare young soldiers to "old beggars" and "hags", stripping them of heroic glamour; "sludge" and "haunting flares" create a grim battlefield.',
  sound='Harsh consonants ("Knock-kneed", "coughing", "cursed") and the slow "trudge" create a heavy, painful sound.',
  speaker='A first-person plural speaker ("we") who is one of the soldiers, giving authority and intimacy.',
  tone='bitter', tw=['jubilant', 'whimsical', 'serene'], tonex='degrading images convey bitterness.',
  dev=[('simile', 'like old beggars under sacks', 'it ages and degrades the soldiers, undermining heroic images of war', ['statistic', 'rhetorical question', 'anaphora']),
       ('alliteration', 'Knock-kneed, coughing ... cursed', 'harsh "k" sounds make the line sound painful and jarring', ['statistic', 'rhetorical question', 'simile'])],
  struct=[('the slowed rhythm', 'caesuras and heavy stresses enact the trudging march')],
  gq='How does Owen challenge heroic images of war in these lines?',
  gqa=('Thesis: Owen replaces heroism with degradation. (1) Similes of beggars and hags. (2) Harsh sound. (3) Disrupted metre. Evaluation: the soldier-speaker\'s authority confronts home-front propaganda.'),
  issue='War, propaganda and the reality of suffering.',
  concept=('representation', 'soldiers are represented as broken, not glorious.'),
  read='Readers then and now see an anti-war protest; some may also see compassion for comrades.',
  field='politics, power and justice')

P(id='dickinson', kind='poem', title="first stanza of Emily Dickinson's poem 'Hope is the thing with feathers' (written c. 1861)",
  text=("“Hope” is the thing with feathers –\nThat perches in the soul –\nAnd sings the tune without the words –\nAnd never stops – at all –"),
  form='A quatrain in common (hymn) metre, alternating four- and three-beat lines; Dickinson\'s dashes interrupt the flow and create pauses.',
  imagery='An extended metaphor presents hope as a bird that "perches in the soul" and sings without words – instinctive and wordless.',
  sound='The dashes and the final "at all" slow the rhythm; the hymn-like metre gives a sense of faith.',
  speaker='A reflective speaker defines an abstraction through a concrete image.',
  tone='reflective', tw=['bitter', 'mocking', 'panicked'], tonex='calm definition creates a reflective tone.',
  dev=[('extended metaphor', 'the thing with feathers / That perches in the soul', 'hope becomes a small, living bird, fragile yet persistent', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('dashes', 'never stops – at all –', 'the dashes create pauses and emphasis, making "at all" emphatic', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the use of "And" to start lines 3 and 4', 'it builds an accumulating definition')],
  gq='How does Dickinson make an abstract idea concrete?',
  gqa=('Thesis: an extended metaphor makes hope tangible. (1) The bird image. (2) The wordless song. (3) Dashes and hymn metre. Evaluation: the playful quotation marks around "Hope" invite readers to reconsider the word.'),
  issue='Resilience and the human spirit.',
  concept=('creativity', 'the poet creatively redefines an abstract concept.'),
  read='Readers may take it as comfort or notice that the bird asks nothing in return.',
  field='art, creativity and the imagination')

P(id='kitchen', kind='drama', title='extract from a play (an original extract written for study)',
  text=("[A kitchen, late evening. A single bulb. AMIRA, 17, sits with a university acceptance letter. Her father, KARIM, enters, still in his work jacket.]\n"
        "KARIM: You're up late.\nAMIRA: (folding the letter quickly) Reading.\nKARIM: Reading what?\nAMIRA: Nothing. Just – school.\n"
        "KARIM: (picks up her empty mug, rinses it, his back to her) Your mother would have read everything you wrote. Every word.\n"
        "[Pause. AMIRA slides the letter under the fruit bowl.]"),
  conv='Stage directions reveal what the dialogue hides: Amira folds and hides the letter, so the audience knows more than Karim (dramatic irony); short lines and the pause create subtext about grief and unspoken ambition.',
  staging='The single bulb creates an intimate, isolated pool of light; Karim\'s back turned while rinsing the mug shows emotional distance; the letter under the fruit bowl is a prop that carries the conflict.',
  conflict='The conflict is between Amira\'s ambition (the university letter, implicitly far away) and family loyalty to a grieving father; the absent mother intensifies her guilt.',
  char='Karim is characterised through work clothes and a domestic gesture – tired, caring, grieving; Amira through evasion.',
  ctx='A contemporary domestic drama, possibly in a migrant or working-class family, where a child\'s departure carries economic and emotional weight.',
  tone='tense', tw=['farcical', 'triumphant', 'carefree'], tonex='short lines and concealment create tension.',
  dev=[('stichomythia', "You're up late. / Reading. / Reading what?", 'rapid short exchanges show tension and evasion', ['statistic', 'simile', 'onomatopoeia']),
       ('subtext', 'Your mother would have read everything you wrote', 'Karim\'s line expresses grief and expectation indirectly', ['statistic', 'onomatopoeia', 'oxymoron'])],
  struct=[('the closing stage direction', 'the silent action leaves the conflict unresolved and the audience complicit')],
  gq='How does the playwright create tension between the characters?',
  gqa=('Thesis: tension lies in what is not said. (1) Stichomythia. (2) Stage directions and props. (3) The absent mother and the final pause. Evaluation: the audience\'s knowledge creates dramatic irony.'),
  issue='Family duty, grief and individual ambition.',
  concept=('identity', 'Amira\'s emerging identity conflicts with family roles.'),
  read='Audiences may sympathise with Amira\'s ambition or with Karim\'s loneliness.',
  field='culture, identity and community')

P(id='macbeth', kind='drama', title="extract from Shakespeare's 'Macbeth', Act 5 Scene 5 (c. 1606)",
  text=("MACBETH: Tomorrow, and tomorrow, and tomorrow,\nCreeps in this petty pace from day to day\nTo the last syllable of recorded time ...\n"
        "Life's but a walking shadow, a poor player\nThat struts and frets his hour upon the stage\nAnd then is heard no more."),
  conv='A soliloquy: alone on stage after hearing of his wife\'s death, Macbeth reveals his inner despair directly to the audience; the metatheatrical image of the "poor player" reminds the audience that they are watching a play.',
  staging='The speech is often staged with Macbeth isolated and still, sometimes with the sound of the approaching army, emphasising his loneliness and the futility of his power.',
  conflict='The internal conflict is Macbeth\'s recognition that his ambition has emptied life of meaning, as the tragedy nears its catastrophe.',
  ctx='Written for a Jacobean audience familiar with ideas of divine order and the theatre as a metaphor for life ("all the world\'s a stage").',
  tone='nihilistic', tw=['jubilant', 'hopeful', 'playful'], tonex='images of meaningless time create nihilism.',
  dev=[('repetition', 'Tomorrow, and tomorrow, and tomorrow', 'the repeated word enacts the monotonous, endless passing of days', ['simile', 'statistic', 'onomatopoeia']),
       ('metaphor', "Life's but a walking shadow, a poor player", 'life is reduced to an insubstantial shadow and a bad actor, conveying futility', ['statistic', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the soliloquy placed just after news of Lady Macbeth\'s death', 'its position shows Macbeth\'s emotional exhaustion before the final battle')],
  gq='How does Shakespeare convey Macbeth\'s state of mind?',
  gqa=('Thesis: Macbeth\'s language enacts despair. (1) Repetition of "tomorrow". (2) Metaphors of shadow and player. (3) Soliloquy and metatheatre. Evaluation: the tragic hero gains insight too late.'),
  issue='Ambition, power and its human cost.',
  concept=('perspective', 'the soliloquy gives direct access to Macbeth\'s perspective.'),
  read='Some see pure nihilism; others see a tragic flash of self-knowledge.',
  field='politics, power and justice')

P(id='palm', kind='drama', title='extract from a comedy (an original extract written for study)',
  text=("[A hotel lobby. The audience has just seen DANIEL hide a stolen necklace inside a potted palm.]\n"
        "INSPECTOR: Nobody leaves until I find it.\nDANIEL: (leaning casually against the palm) Quite right, Inspector. A terrible business.\n"
        "INSPECTOR: You seem very calm, Mr Hale.\nDANIEL: I find plants soothing. (He pats the palm.) Don't you?"),
  conv='Dramatic irony: the audience knows the necklace is in the palm, so every gesture Daniel makes towards it creates comic tension; stage directions direct the physical comedy.',
  staging='The palm is the central prop; Daniel\'s casual leaning and patting are visual jokes the audience watches anxiously.',
  conflict='The conflict between detective and thief is played for comedy, with suspense over discovery.',
  char='Daniel is characterised as audacious and witty; the Inspector as suspicious but slow.',
  ctx='A light comedy in the tradition of drawing-room and detective farces.',
  tone='comic', tw=['tragic', 'solemn', 'bitter'], tonex='dramatic irony and wit create comedy.',
  dev=[('dramatic irony', 'I find plants soothing. (He pats the palm.)', 'the audience knows what the plant hides, so the line is funny and suspenseful', ['statistic', 'simile', 'onomatopoeia']),
       ('rhetorical question', "Don't you?", 'Daniel\'s cheeky question taunts the Inspector', ['statistic', 'simile', 'onomatopoeia'])],
  struct=[('the opening stage direction', 'it gives the audience privileged knowledge that powers the scene')],
  gq='How does the playwright create comedy in this extract?',
  gqa=('Thesis: comedy arises from dramatic irony and physical business. (1) The audience\'s knowledge. (2) Daniel\'s gestures. (3) Witty understatement. Evaluation: suspense and laughter work together.'),
  issue='Deception and justice (treated comically).',
  concept=('communication', 'what is said contrasts with what is shown.'),
  read='Audiences enjoy rooting for the charming rogue, which raises questions about sympathy and morality.',
  field='art, creativity and the imagination')

P(id='verlaine', kind='trans', title="first stanza of Paul Verlaine's poem 'Il pleure dans mon cœur' (1874) with two English translations written for study",
  text=("Original: Il pleure dans mon cœur / Comme il pleut sur la ville ; / Quelle est cette langueur / Qui pénètre mon cœur ?\n"
        "Translation A: It weeps in my heart / As it rains on the town; / What is this languor / That pierces my heart?\n"
        "Translation B: My heart is raining / the way the city rains; / what is this heavy dullness / soaking through my veins?"),
  trans='Translation A stays literal and keeps the impersonal "It weeps", echoing the French pun between "il pleure" (it weeps) and "il pleut" (it rains), but loses the rhyme; Translation B gives up the impersonal construction and the pun, but recreates rhyme (rains/veins) and the soft, liquid music; "soaking" interprets "pénètre" as gradual saturation rather than piercing.',
  culture='Verlaine\'s melancholy belongs to French Symbolism, which valued musicality and suggestion over statement; a translator must decide whether to keep meaning or music.',
  tone='melancholic', tw=['exuberant', 'sarcastic', 'angry'], tonex='rain and languor create melancholy.',
  dev=[('simile', 'Comme il pleut sur la ville / As it rains on the town', 'the comparison links inner sorrow to the weather (pathetic fallacy)', ['statistic', 'onomatopoeia', 'anaphora']),
       ('rhetorical question', 'Quelle est cette langueur', 'the speaker cannot name the cause of sadness', ['statistic', 'simile', 'onomatopoeia'])],
  gq='How do the two translations make different choices in rendering the original?',
  gqa=('Thesis: A prioritises fidelity, B prioritises music. (1) The "il pleure / il pleut" pun. (2) Rhyme and sound. (3) "pierces" vs "soaking". Evaluation: no translation keeps everything; each reveals the translator\'s values.'),
  issue='Translation, loss and the movement of culture across languages.',
  concept=('transformation', 'translation transforms the poem while trying to carry it across.'),
  read='A reader who values accuracy prefers A; one who values poetry prefers B.',
  field='art, creativity and the imagination')

P(id='ittekimasu', kind='trans', title='extract from a novel translated from Japanese, with a translator\'s note (an original passage written for study)',
  text=("At the door, Grandmother said, 'Itte rasshai,' as she did every morning, and I answered, 'Ittekimasu,' though we both knew I was not coming back for a long time.\n"
        "[Translator's note: these are the fixed phrases said when someone leaves home – roughly 'go and come back' and 'I will go and come back'. "
        "I have kept the Japanese because no English farewell carries the same promise of return.]"),
  trans='The translator keeps the Japanese phrases and explains them in a note, choosing foreignisation over domestication (e.g. replacing them with "Goodbye"); this preserves the irony that the ritual promise of return is spoken when both know the narrator will not return soon.',
  culture='The everyday ritual phrases express Japanese cultural values of home, belonging and reciprocity; the scene shows how ordinary language carries culture.',
  tone='poignant', tw=['comic', 'aggressive', 'triumphant'], tonex='a ritual of return spoken at a departure is poignant.',
  dev=[('irony', 'though we both knew I was not coming back for a long time', 'the ritual promise of return contrasts with the reality of departure', ['statistic', 'simile', 'onomatopoeia']),
       ('untranslated words', "'Itte rasshai' ... 'Ittekimasu'", 'keeping the Japanese preserves cultural specificity', ['simile', 'statistic', 'anaphora'])],
  gq='How do the passage and the translator\'s note show the challenges of translating culture?',
  gqa=('Thesis: the translator makes cultural loss visible rather than hiding it. (1) Retained phrases. (2) The note as paratext. (3) The irony of the ritual. Evaluation: notes can interrupt the reading experience but preserve meaning.'),
  issue='Language, culture and what is lost in translation.',
  concept=('culture', 'everyday ritual language carries cultural values.'),
  read='Some readers enjoy the visible translator; others prefer seamless translations.',
  field='culture, identity and community')

P(id='doorway', kind='trans', title='extract from a novel translated from Arabic (an original passage written for study)',
  text=("In my father's house, the men ate first. My mother called this respect. My aunt, who had studied law in Cairo before her marriage, called it nothing at all; "
        "she simply ate standing in the kitchen doorway, her plate in one hand and a newspaper in the other, so that she belonged to neither room."),
  power='The family meal ritual encodes male precedence; the mother accepts it as "respect", while the educated aunt resists silently by occupying the threshold – the doorway symbolises her position between tradition and independence.',
  culture='The scene presents a cultural value (men eating first) through different responses within one family, avoiding a single, stereotyped picture of the culture.',
  char='The aunt is characterised by education, silence and the symbolic newspaper; the mother by acceptance.',
  trans='A translator must decide whether to explain the custom or let the scene speak; here it is left unexplained, trusting the reader.',
  tone='understated', tw=['hysterical', 'jubilant', 'sarcastic'], tonex='plain statements carry understated criticism.',
  dev=[('symbol', 'ate standing in the kitchen doorway', 'the threshold symbolises belonging to neither tradition nor freedom', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('contrast', 'My mother called this respect. My aunt ... called it nothing at all', 'two responses to one custom show varied perspectives within a culture', ['simile', 'onomatopoeia', 'statistic'])],
  gq='How does the writer present gender and power in the family?',
  gqa=('Thesis: a small domestic ritual reveals structures of power and quiet resistance. (1) Men eating first. (2) Contrasting women\'s responses. (3) The doorway and newspaper symbols. Evaluation: understatement avoids stereotyping.'),
  issue='Gender, tradition and power in the family.',
  concept=('culture', 'culture is shown as contested from within.'),
  read='Readers may see oppression, quiet resistance, or the complexity of tradition.',
  field='politics, power and justice')

P(id='rosa', kind='trans', title='extract from a short novel translated from Spanish (an original passage written for study)',
  text=("The señora paid Rosa on Fridays, in cash, counting each note aloud as if Rosa might not know her numbers. Rosa had taught three of the señora's children to read. "
        "She said nothing. She folded the money twice and put it in her shoe, where the señora's eyes did not follow."),
  power='Class power is shown through the employer\'s condescending ritual of counting aloud; the irony that Rosa taught the children to read exposes the injustice; hiding the money in her shoe is a small act of private control.',
  culture='The untranslated "señora" keeps the class-marked form of address and the cultural setting of domestic service.',
  char='Rosa is characterised by silence and dignity; the señora by unconscious condescension.',
  trans='Leaving "señora" in Spanish keeps its connotations of class and respect that "madam" or "the lady" would alter.',
  tone='quietly indignant', tw=['jovial', 'celebratory', 'whimsical'], tonex='plain narration carries quiet indignation.',
  dev=[('irony', "as if Rosa might not know her numbers. Rosa had taught three of the señora's children to read", 'the juxtaposition exposes the employer\'s prejudice', ['simile', 'statistic', 'onomatopoeia']),
       ('short sentence', 'She said nothing.', 'the brevity conveys Rosa\'s controlled silence', ['simile', 'statistic', 'onomatopoeia'])],
  gq='How does the writer present the relationship between Rosa and her employer?',
  gqa=('Thesis: a weekly ritual reveals class power and Rosa\'s quiet resistance. (1) The counting aloud. (2) The irony of literacy. (3) The shoe as private space. Evaluation: silence gives Rosa dignity, but also shows she cannot speak.'),
  issue='Class, labour and dignity in domestic work.',
  concept=('representation', 'the domestic worker is represented with dignity and inner life.'),
  read='Readers may feel anger at the employer or admiration for Rosa\'s composure.',
  field='politics, power and justice')

P(id='kafka', kind='trans', title="opening sentence of Franz Kafka's 'Die Verwandlung' (1915) with two English translations written for study",
  text=("Original: Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt.\n"
        "Translation A: As Gregor Samsa awoke one morning from uneasy dreams, he found himself transformed in his bed into a monstrous vermin.\n"
        "Translation B: One morning, waking from troubled dreams, Gregor Samsa found himself changed in his bed into an enormous insect."),
  trans='The key choice is "Ungeziefer": A\'s "monstrous vermin" keeps the word\'s vagueness and its sense of something unclean and unwanted, while B\'s "enormous insect" makes the creature specific and visual, losing the moral disgust; A also keeps the German sentence order (the transformation arrives last), preserving the shock of the final word.',
  culture='Kafka\'s German "Ungeziefer" originally meant an unclean animal unfit for sacrifice; the social disgust it carries supports readings of Gregor as a worker discarded by family and employer.',
  tone='matter-of-fact', tw=['exuberant', 'sentimental', 'sarcastic'], tonex='the impossible event is told in a calm, matter-of-fact way.',
  dev=[('end focus', 'zu einem ungeheueren Ungeziefer verwandelt / into a monstrous vermin', 'placing the transformation at the end of the sentence delays the shock until the last words', ['simile', 'rhetorical question', 'onomatopoeia'])],
  gq='How do the two translations differ in their effect on the reader?',
  gqa=('Thesis: A preserves Kafka\'s ambiguity and sentence order; B gains clarity but loses disgust. (1) "vermin" vs "insect". (2) Word order and end focus. (3) "transformed" vs "changed". Evaluation: translation choices steer interpretation.'),
  issue='Alienation, work and family obligation.',
  concept=('transformation', 'the literal transformation becomes a metaphor that each translation shapes differently.'),
  read='Readers of B may picture a beetle; readers of A may focus on Gregor\'s social rejection.',
  field='beliefs, values and education')

P(id='basho', kind='trans', title="Matsuo Bashō's haiku about an old pond (1686) in romanised Japanese with two English translations written for study",
  text=("Original (romanised): furu ike ya / kawazu tobikomu / mizu no oto\n"
        "Translation A: The old pond – / a frog jumps in, / the sound of water.\n"
        "Translation B: Ancient pond: / a frog leaps – / splash!"),
  trans='Translation A keeps the three-part structure and the quiet ending "the sound of water", which mirrors "mizu no oto" and preserves the stillness after the sound; Translation B compresses the poem and replaces the noun phrase with the onomatopoeic "splash!", which makes it lively but loses the silence the original evokes. The cutting word "ya" is rendered by A\'s dash and B\'s colon.',
  culture='Haiku traditionally juxtapose two images with a cutting word (kireji such as "ya") and contain a seasonal word (kigo – the frog suggests spring); the poem reflects a Zen-influenced attention to a single moment.',
  tone='contemplative', tw=['raucous', 'bitter', 'anxious'], tonex='stillness and a single sound create contemplation.',
  dev=[('onomatopoeia', 'splash!', 'B turns the sound into a sudden, comic event, unlike the stillness of A', ['statistic', 'rhetorical question', 'anaphora'])],
  gq='How do the two translations handle sound and silence differently?',
  gqa=('Thesis: A preserves contemplative stillness, B dramatises the moment. (1) "the sound of water" vs "splash!". (2) Punctuation for "ya". (3) Line length. Evaluation: B is vivid but arguably mistranslates the mood.'),
  issue='Translation, culture and the representation of nature.',
  concept=('transformation', 'each translation transforms the poem\'s balance of sound and silence.'),
  read='Some prefer the energy of B; others feel A is truer to Zen stillness.',
  field='art, creativity and the imagination')


# =============================================================================================
# Paper 2 question bank (original questions in the style of the four general questions on Paper 2)
# =============================================================================================
P2Q = [
    dict(q='In what ways and to what effect do two works you have studied present the tension between individual desire and social expectation?',
         terms='"In what ways" asks about authorial methods; "to what effect" asks about impact on meaning and audience; "individual desire" and "social expectation" must both be defined and shown in tension, not separately.',
         works="Henrik Ibsen's A Doll's House (studied in translation) and F. Scott Fitzgerald's The Great Gatsby – both centre a character whose desires collide with the codes of a class-conscious society, but one is drama and the other first-person retrospective narration, which allows a contrast of form.",
         thesis='Both works dramatise desire constrained by social codes, but where Ibsen moves Nora towards a self-assertive break that the audience witnesses directly, Fitzgerald filters Gatsby\'s desire through Nick\'s retrospective narration so that it becomes a doomed, elegiac illusion.',
         points=['symbols of desire and constraint: Nora\'s forbidden macaroons and the stripped Christmas tree versus Gatsby\'s green light', 'form: stage directions and the audience\'s direct view of Nora versus Nick\'s mediating, partly admiring narration', 'endings: the slammed door as liberation versus "boats against the current" as defeat'],
         ev='A strong answer evaluates how genre shapes the reader\'s judgement: the play invites the audience to judge society, the novel to mourn the dreamer.'),
    dict(q='Discuss how two works you have studied use setting to explore the operation of power.',
         terms='"Setting" includes place, time and social world; "operation of power" requires showing how power works (institutions, surveillance, custom), not just who has it.',
         works="Chinua Achebe's Things Fall Apart and Margaret Atwood's The Handmaid's Tale – both depict a society whose spaces encode authority, one traditional and then colonial, the other theocratic and dystopian.",
         thesis='Achebe and Atwood both make setting an instrument of power, but Achebe shows communal spaces of Umuofia being displaced by colonial church and court, whereas Atwood confines Offred within domestic and institutional spaces that make surveillance intimate.',
         points=['communal versus controlled space: the village gatherings and the egwugwu ceremony versus the Commander\'s household and the Wall', 'the arrival of new institutions (church, courthouse) versus Gilead\'s rebranding of familiar places', 'narrative perspective: Achebe\'s third-person communal view versus Offred\'s restricted first person'],
         ev='Evaluate whether setting reflects power or actively produces it; both suggest that controlling space is controlling people.'),
    dict(q='Compare the ways in which two works you have studied present a character\'s struggle with identity.',
         terms='"Compare" requires similarities and differences; "struggle with identity" implies conflict between how the self is defined by others and by the character.',
         works="Marjane Satrapi's Persepolis and Jhumpa Lahiri's The Namesake – both explore identity across cultures, through a graphic memoir and a third-person novel.",
         thesis='Both works present identity as negotiated between two cultures, but Satrapi visualises the split self through the shifting drawn image of Marji, while Lahiri locates the struggle in a name – Gogol – whose meaning the protagonist must grow into.',
         points=['visual self-representation (the veil, the changing body) versus the motif of naming', 'family as anchor and pressure in both', 'endings: departure from Iran versus Gogol reading the Gogol book his father gave him'],
         ev='Evaluate how form (image versus prose narration) changes the reader\'s access to inner conflict.'),
    dict(q='How and to what extent do two works you have studied use the perspective of an outsider?',
         terms='"How" demands analysis of narrative technique; "to what extent" asks for a judgement about how far the outsider\'s perspective shapes meaning.',
         works="Franz Kafka's The Metamorphosis (in translation) and Mary Shelley's Frankenstein – both centre a being excluded from family and society because of his form.",
         thesis='Kafka and Shelley both use the excluded body to critique the community that rejects it, but Kafka keeps us close to Gregor\'s bewildered consciousness until his death, while Shelley grants the creature his own embedded narrative, making his eloquence an indictment of his creator.',
         points=['narrative position: close third person in Kafka versus nested first-person narratives in Shelley', 'the family\'s response: the Samsas\' relief versus Victor\'s abandonment', 'the outsider\'s voice: Gregor\'s loss of speech versus the creature\'s articulate self-education'],
         ev='Judge the extent: in both, the outsider becomes the moral centre, but Shelley makes the outsider\'s voice heard more fully.'),
    dict(q='In what ways do two works you have studied explore the relationship between memory and truth?',
         terms='"Relationship" requires showing how memory shapes, distorts or preserves truth; works must present memory as an issue.',
         works="Kazuo Ishiguro's The Remains of the Day and Art Spiegelman's Maus – both are built from retrospective accounts whose reliability matters.",
         thesis='Both works expose the gaps between remembered and actual truth, but Ishiguro uses Stevens\'s self-deceiving narration to make the reader detect what he suppresses, whereas Spiegelman frames Vladek\'s testimony with Art\'s present-day questioning so that the making of memory becomes the subject.',
         points=['unreliable narration and omission (Stevens on Lord Darlington and Miss Kenton) versus framed testimony', 'form: understated formal prose versus the graphic medium and the animal metaphor', 'what the works suggest about the cost of remembering or refusing to remember'],
         ev='Evaluate whether either work offers access to truth or only to versions of it.'),
    dict(q='Discuss the ways in which two works you have studied present conflict between generations.',
         terms='"Conflict between generations" requires parent–child or elder–youth tension and its causes; "ways" asks about authorial methods.',
         works="Arthur Miller's Death of a Salesman and Chinua Achebe's Things Fall Apart – fathers whose ideas of success and masculinity alienate their sons.",
         thesis='Both works present fathers whose rigid ideals drive their sons away, but Miller stages Willy and Biff\'s conflict through memory sequences that blur past and present, while Achebe shows Okonkwo\'s fear of weakness pushing Nwoye towards the missionaries, linking a family rupture to a cultural one.',
         points=['the father\'s ideal: being "well liked" versus fear of resembling Unoka', 'staging and structure: expressionistic flashbacks versus chronological tragedy', 'the son\'s rejection: Biff\'s confrontation versus Nwoye\'s conversion'],
         ev='Evaluate how far each work blames the father or the society that shaped him.'),
    dict(q='How do two works you have studied use structure to create tension?',
         terms='"Structure" covers order of events, chronology, acts/chapters and revelation; "tension" may be suspense, dread or dramatic irony.',
         works="Gabriel García Márquez's Chronicle of a Death Foretold (in translation) and Shakespeare's Macbeth – both announce or prophesy the outcome early.",
         thesis='Both works generate tension not from what will happen but from how and why, yet García Márquez reveals Santiago Nasar\'s death in the first sentence and reconstructs it like an investigation, while Shakespeare uses the witches\' prophecies to create a dread that the tragedy steadily fulfils.',
         points=['early revelation versus prophecy', 'fragmented, retrospective investigation versus tightly compressed five-act tragedy', 'the effect of inevitability: collective guilt versus individual damnation'],
         ev='Evaluate whether knowing the end reduces or increases tension.'),
    dict(q='Compare how two works you have studied present the role of women in a patriarchal society.',
         terms='"Role" means expected functions and identities; "patriarchal society" must be shown in the works; the comparison must address both similarity and difference.',
         works="Tennessee Williams's A Streetcar Named Desire and Carol Ann Duffy's collection The World's Wife – a play and a poetry collection that both examine women defined by men.",
         thesis='Both works expose how women are constrained by male power, but Williams stages Blanche\'s destruction as tragedy, whereas Duffy\'s dramatic monologues give the wives of famous men wit and voice, rewriting their roles.',
         points=['voice: Blanche silenced and removed versus Duffy\'s speakers taking the floor', 'tone: tragic versus comic and subversive', 'Stella\'s choice to stay versus the speakers\' re-evaluation of their husbands'],
         ev='Evaluate whether either work offers escape from patriarchy or only critique.'),
    dict(q='Explore how two works you have studied use symbols or motifs to develop their central concerns.',
         terms='"Symbols or motifs" must be specific, recurring elements; "central concerns" means the works\' main themes; analysis must link the two.',
         works="Arundhati Roy's The God of Small Things and F. Scott Fitzgerald's The Great Gatsby – both organise meaning around recurring images.",
         thesis='Both novels use recurring images to connect personal tragedy to social order, but Roy\'s motifs (the History House, the "Love Laws") are fragmented across a non-linear narrative, whereas Fitzgerald\'s (the green light, the valley of ashes, the eyes of Doctor T. J. Eckleburg) build a coherent moral landscape.',
         points=['what each motif represents (caste and forbidden love versus the American Dream)', 'how structure distributes motifs (non-linear versus linear retrospect)', 'the reader\'s work in connecting them'],
         ev='Evaluate how motif structure affects the reader\'s experience of tragedy.'),
    dict(q='In what ways do two works you have studied present the abuse of power?',
         terms='"Abuse of power" requires showing power used illegitimately or harmfully; "ways" demands analysis of method.',
         works="George Orwell's Nineteen Eighty-Four and Shakespeare's Macbeth – a totalitarian state and a tyrant.",
         thesis='Both works show power corrupting truth and life, but Shakespeare locates abuse in one man\'s ambition and conscience, while Orwell depicts an impersonal system – Big Brother, Newspeak, Room 101 – that abuses power to control thought itself.',
         points=['individual versus systemic power', 'language: Macbeth\'s equivocation versus Newspeak', 'outcome: restoration of order versus Winston\'s defeat'],
         ev='Evaluate which vision is more pessimistic and why.'),
    dict(q='To what extent do two works you have studied end with a sense of resolution?',
         terms='"To what extent" requires a judgement; "resolution" could mean plot closure, moral clarity or emotional acceptance.',
         works="Henrik Ibsen's A Doll's House and Kazuo Ishiguro's Never Let Me Go – endings that refuse easy comfort.",
         thesis='Both endings resolve the protagonist\'s understanding but not her situation: Nora\'s exit is a decisive act whose consequences are left open, while Kathy\'s calm acceptance in Norfolk resolves the narrative but not its moral horror.',
         points=['action versus acceptance', 'open consequence (what happens to Nora?) versus foreclosed future', 'the audience\'s or reader\'s unresolved discomfort'],
         ev='Judge whether the lack of resolution is the point of each work.'),
    dict(q='How do two works you have studied use humour or irony to make a serious point?',
         terms='"Humour or irony" must be analysed as methods; "serious point" requires identifying the concern the humour serves.',
         works="Marjane Satrapi's Persepolis and Voltaire's Candide (in translation) – both use comic naivety to expose violence and ideology.",
         thesis='Both works use a naïve perspective to make horror visible, but Satrapi\'s child narrator generates gentle, poignant humour, whereas Voltaire\'s satirical narrator turns Pangloss\'s optimism into absurdity.',
         points=['the naïve viewpoint (young Marji versus Candide)', 'visual comedy versus verbal irony', 'the serious target: political repression versus philosophical optimism'],
         ev='Evaluate whether humour softens or sharpens the critique.'),
    dict(q='Discuss how two works you have studied present the effects of war on individuals.',
         terms='"Effects of war on individuals" requires attention to particular characters or speakers, not war in general.',
         works="Wilfred Owen's poetry and Art Spiegelman's Maus – soldier-poet testimony and second-generation memoir.",
         thesis='Both works present war\'s damage as lasting beyond the battlefield, but Owen\'s first-hand lyric immediacy contrasts with Spiegelman\'s layered account, in which the father\'s trauma reshapes the son\'s life.',
         points=['immediacy versus mediation', 'imagery: gas, mud and bodies versus the animal metaphor', 'legacy: the "old Lie" versus inherited trauma'],
         ev='Evaluate how the medium shapes the reader\'s sense of authenticity.'),
    dict(q='Compare how two works you have studied present a journey, whether literal or metaphorical.',
         terms='"Journey" may be physical travel or inner change; "compare" requires both works to be treated in relation to each other.',
         works="Joseph Conrad's Heart of Darkness and Cormac McCarthy's The Road – journeys through dark landscapes that test moral identity.",
         thesis='Both works use a journey into darkness to test civilisation, but Conrad\'s frame narrative makes Marlow\'s voyage up the river an ambiguous moral education, whereas McCarthy\'s father and son move south through a ruined world where carrying "the fire" means preserving goodness.',
         points=['frame narrative versus spare third-person narration', 'landscape as moral symbol', 'endings: the lie to the Intended versus the boy\'s survival with a new family'],
         ev='Evaluate which journey offers hope.'),
    dict(q='In what ways do two works you have studied explore the conflict between tradition and change?',
         terms='Both "tradition" and "change" must be defined in the context of each work; "ways" asks for methods.',
         works="Chinua Achebe's Things Fall Apart and Anton Chekhov's The Cherry Orchard (in translation) – communities facing the end of an old order.",
         thesis='Both works stage the collapse of a traditional world, but Achebe makes colonial change a violent rupture that destroys Okonkwo, while Chekhov presents the sale of the orchard with tragicomic ambivalence, ending with the sound of the axe.',
         points=['tragic versus tragicomic tone', 'the agent of change (missionaries and colonial government versus Lopakhin the merchant)', 'symbol: the orchard and the axe versus the destroyed clan'],
         ev='Evaluate whether either work mourns or welcomes change.'),
    dict(q='How do two works you have studied use a narrator\'s voice to shape the reader\'s sympathies?',
         terms='"Narrator\'s voice" covers person, tone and reliability; "shape sympathies" asks how the reader is positioned.',
         works="Charlotte Brontë's Jane Eyre and Margaret Atwood's The Handmaid's Tale – first-person female narrators who address the reader.",
         thesis='Both narrators win the reader\'s sympathy by addressing us directly, but Jane\'s confident retrospective voice ("Reader, I married him") claims control of her story, whereas Offred\'s fragmented, self-questioning testimony – later framed by the "Historical Notes" – makes sympathy uneasy.',
         points=['direct address and retrospection', 'reliability and self-correction', 'framing devices that judge the narrator'],
         ev='Evaluate how the framing changes our trust in each narrator.'),
]


def _p1(rng, slot):
    if slot.style != 'p1':
        return None
    pool = [p for p in PASS if p['kind'] in NONLIT and p.get('gq') and p.get('gqa')]
    p = rng.choice(pool)
    stem = ('Paper 1 – Guided textual analysis (SL: 1 hour 15 minutes for one text; HL: 2 hours 15 minutes for two texts).\n\n'
            f'{intro(p)}\n\nGuiding question: {p["gq"]}\n\n'
            'Write a guided textual analysis of the text. You may respond to the guiding question or develop your own focus on how the text creates meaning.')
    return dict(stem=stem, answer=p['gqa'], type='long', marks=20, minutes=60,
                markingKey=f'Indicative content: {p["gqa"]} {P1_BANDS}')


def _p2a(rng, slot):
    if slot.style != 'p2a':
        return None
    it = rng.choice(P2Q)
    if rng.random() < 0.5:
        stem = (f'Paper 2 question: "{it["q"]}"\n\nUnpack the question: identify its key terms and what it requires, '
                'name two literary works you have studied that you would pair to answer it, and justify the pairing.')
        ans = f'{it["terms"]} Suggested pairing: {it["works"]}'
    else:
        stem = (f'Paper 2 question: "{it["q"]}"\n\nWrite a comparative thesis statement and a three-point outline for an essay '
                'that answers this question with reference to two literary works you have studied.')
        ans = f'Model thesis: {it["thesis"]} Outline: ' + '; '.join(f'({i}) {x}' for i, x in enumerate(it['points'], 1)) + '.'
    return dict(stem=stem, answer=ans, type='case', marks=5, minutes=12,
                markingKey=f'{ans} 5 marks: key terms defined (1); demands of the question identified (1); two suitable works justified or an arguable comparative thesis (2); an outline that compares rather than treats the works separately (1). Any suitable works may be credited.')


def _p2b(rng, slot):
    if slot.style != 'p2b':
        return None
    it = rng.choice(P2Q)
    stem = rng.choice([
        f'Paper 2 question: "{it["q"]}"\n\nWrite the comparative analysis section of your essay: develop two integrated comparative points, each analysing specific authorial choices in both works.',
        f'Paper 2 question: "{it["q"]}"\n\nWith reference to two works you have studied, write two comparative body paragraphs that analyse how each writer\'s choices shape meaning and evaluate their effects.',
    ])
    ans = f'Indicative content (example pairing: {it["works"]}) Thesis: {it["thesis"]} Points: ' + '; '.join(it['points']) + f'. {it["ev"]}'
    return dict(stem=stem, answer=ans, type='long', marks=10, minutes=30,
                markingKey=f'{ans} {P2_BANDS} Any suitable pair of studied works may be credited.')


GLOBAL = [T('C4', (4, 5), _p1, 'long', 'p1', 'paper1'), T(('C3', 'C4'), (3, 4), _p2a, 'case', 'p2a', 'paper2a'),
          T('C4', (4, 5), _p2b, 'long', 'p2b', 'paper2b')]


def init(subject_id):
    pass


def templates(st):
    return R.build(st, STYLE) + GLOBAL


def H(key, **kw):
    R.facts(key, F(**kw))


# common question frames ---------------------------------------------------------------------------
AUD_Q = ['Identify the intended audience of this {label}. Support your answer with one reference to the text.',
         'Who is the target audience of the text? Refer to two specific details that suggest this audience.',
         'Explain how the writer signals who the intended audience is.']
PURP_Q = ['State the main purpose of the text and explain how one feature helps to achieve it.',
          'What is the writer trying to achieve in this {label}? Support your answer with evidence.',
          'Outline the purpose of the text and the means by which it pursues that purpose.']
CTX_Q = ['Explain how the context of the text shapes its meaning or its reception.',
         'How might knowledge of the context of production help a reader to interpret this {label}?',
         'Explain one way in which the context in which this text appears affects its message.']
DEV_Q = ['Explain the effect of the {device} "{quote}" on the reader.',
         'Analyse how the phrase "{quote}" contributes to the writer\'s purpose.',
         'Identify the device used in "{quote}" and explain its effect.',
         'Comment on the writer\'s choice of language in "{quote}".']
STRUCT_Q = ['Analyse the effect of {feature} in the text.',
            'Explain how {feature} contributes to the meaning of the text.',
            'How does {feature} shape the reader\'s experience of the text?']
READ_Q = ['Suggest two different ways in which readers might respond to this text, explaining what might lead to each reading.',
          'How might the meaning of this text change for readers with different values or experiences?',
          'Explain how a reader\'s own context might lead to a resistant reading of this text.']
VIS_Q = ['Analyse how the visual elements of the text contribute to its meaning.',
         'Explain how composition, colour or framing are used in this text and their effect.',
         'Discuss the relationship between image and words in this text.']
ISSUE_Q = ['Identify a global issue raised by this text and explain how one stylistic feature presents it.',
           'What global issue does this text engage with? Support your answer with reference to the text.',
           'Explain how the text presents a global issue that has local and transnational significance.']
CONCEPT_Q = ['Explain how this text engages with the course concept of {cname}.',
             'Which of the seven course concepts is most relevant to this text? Justify your choice with reference to the text.',
             'How could this text be used to explore the concept of {cname} in your learner portfolio?']
CRIT_OPEN = 'Credit any well-justified alternative supported by the text; the answer given is the most direct reading.'


# =============================================================================================
# ch01 Introduction to Language A: Language and Literature – texts and the seven concepts
# =============================================================================================
H('ch01-st1',
  terms=[('text', 'anything that can be read or interpreted for meaning – written, spoken, visual or multimodal – produced by someone for an audience and purpose'),
         ('literary work', 'a single work of literature (a novel, a play, a collection of poems or short stories, a work of literary non-fiction) studied in full in the course'),
         ('non-literary text type', 'a category of non-literary text with recognisable conventions, such as an advertisement, speech, opinion column, infographic or blog'),
         ('body of work', 'a collection of non-literary texts by the same author or of the same text type, studied together (for example a set of a photographer\'s images or a campaign\'s posters)'),
         ('multimodal text', 'a text that combines two or more modes of communication, such as words, images, sound, layout and movement')],
  facts=[('How many literary works does an SL student study in Language A: Language and Literature?', 'Four', ['Two', 'Six', 'Eight'], 'SL students study at least four literary works; HL students study at least six.'),
         ('How many literary works does an HL student study in Language A: Language and Literature?', 'Six', ['Four', 'Three', 'Ten'], 'HL students study at least six literary works alongside a range of non-literary texts.'),
         ('Which of these is a non-literary text type?', 'A political cartoon', ['A sonnet', 'A novella', 'A tragedy'], 'Cartoons are non-literary text types; the others are literary forms.'),
         ('What are the three areas of exploration in the course?', 'Readers, writers and texts; Time and space; Intertextuality: connecting texts', ['Language, literature and culture; Power and voice; Form and genre', 'Reading, writing and speaking; Context; Comparison', 'Poetry, prose and drama; Media; Translation'], 'The course is organised into these three areas of exploration.')],
  why=[('Explain why an advertisement can be treated as a "text" worthy of close analysis.', 'It is a deliberate construction made by a writer for a purpose and an audience, so its words, images and layout carry meaning that can be analysed and evaluated just like a literary text.'),
       ('Explain why the course pairs literary works with non-literary texts.', 'Studying them together shows that all texts use language choices to shape meaning and perspective; comparing them reveals how literary and everyday texts represent the same global issues differently.'),
       ('Explain why studying a "body of work" is useful for non-literary texts.', 'Single non-literary texts can be short; a body of work (by one creator or one text type) allows students to identify patterns, recurring techniques and changes over time.')],
  contrast=[('a literary work', 'a non-literary text', 'A literary work is an imaginative or crafted work of literature studied whole (novel, play, poetry collection), usually valued for its aesthetic qualities; a non-literary text is an everyday or functional text (advert, speech, article) whose primary aim is often to inform, persuade or entertain in a specific context.'),
            ('a text type', 'a genre', 'A text type is a category of text defined by its function and conventions (e.g. a speech, an infographic); a genre is a category within literature or media defined by subject and style (e.g. tragedy, science fiction). One text type can contain many genres.')],
  misc=[('Only books can be studied as texts in English Language and Literature.', 'Any crafted artefact that communicates meaning – adverts, photographs, websites, speeches, memes – is a text in the course.'),
        ('Non-literary texts are simpler than literary works and need less analysis.', 'Non-literary texts can be highly crafted; a short advert may use visual composition, connotation and structure as deliberately as a poem.')],
  evaluate=[('Distinguishing literary from non-literary texts is becoming impossible in the digital age.', ['memes, Instagram poetry and fan fiction blur boundaries', 'graphic novels and literary non-fiction combine features'], ['conventions and purposes still differ (a campaign aims to change behaviour; a novel invites interpretation)', 'the course itself relies on the distinction for assessment'], 'The boundary is porous but still useful: it describes tendencies of purpose and form, not rigid categories.')],
  extended=[('Choose one literary work and one non-literary text type you have studied. Explain how each makes meaning, and evaluate whether the same analytical vocabulary works for both.', 'Indicative content: identify conventions of each; show shared tools (diction, imagery, structure, point of view) and different ones (layout, image, typography for the non-literary); judge that the vocabulary overlaps but non-literary analysis needs visual and contextual terms.', 6, 'long')])
pq_kind_mcq('ch01-st1')
pq('ch01-st1', ('C2', 'C3'), (2, 4), None, 'kconv', ['Identify the text type of this extract and explain how two of its conventions are used.',
                                                   'Explain which features of the extract mark it as a particular text type.',
                                                   'Outline the conventions of the text type used here, with examples from the extract.'], crit=CRIT_A)

H('ch01-st2',
  terms=[('identity', 'the sense of who a person or group is, shaped by and expressed through language, culture and representation'),
         ('culture', 'the shared beliefs, values, practices and products of a group, which texts both reflect and shape'),
         ('creativity', 'the imaginative and original use of language and form by a writer, and the reader\'s creative engagement in making meaning'),
         ('communication', 'the process by which meaning passes between a text\'s producer and its audience, affected by medium, context and convention'),
         ('perspective', 'the particular point of view from which a text presents its subject, and the viewpoints readers bring to it'),
         ('transformation', 'the way texts change other texts (adaptation, parody) and can transform readers\' attitudes or the world'),
         ('representation', 'the way a text constructs a version of reality, people or ideas rather than simply reflecting them')],
  facts=[('How many course concepts are there in Language A: Language and Literature?', 'Seven', ['Five', 'Six', 'Nine'], 'The seven concepts are identity, culture, creativity, communication, perspective, transformation and representation.'),
         ('Which of the following is NOT one of the seven course concepts?', 'Genre', ['Perspective', 'Transformation', 'Representation'], 'Genre is important in the course but it is not one of the seven named concepts.')],
  why=[('Explain why "representation" is a central concept when studying advertisements.', 'Advertisements do not show reality neutrally; they construct versions of people, places and lifestyles to persuade, so analysing representation reveals the values and assumptions they promote.'),
       ('Explain how the concept of "perspective" applies to both writers and readers.', 'Writers present events from a chosen point of view, and readers interpret texts through their own experiences and values, so meaning arises from the meeting of two perspectives.'),
       ('Explain why "transformation" is a useful concept for studying adaptations.', 'An adaptation transforms a source text into a new medium or context, and studying what is changed reveals both texts\' assumptions and the new audience\'s values.')],
  contrast=[('representation', 'perspective', 'Representation concerns how a text constructs its subject (e.g. how women are shown); perspective concerns the point of view from which it is presented or read. A single perspective produces a particular representation.'),
            ('identity', 'culture', 'Identity is the sense of self of an individual or group; culture is the shared system of practices and values within which identities form. A text may show an individual identity in tension with its culture.')],
  misc=[('The seven concepts are themes, so each text has only one concept.', 'Concepts are lenses, not themes; any text can be explored through several concepts, and the strongest analysis often connects two or more.'),
        ('Creativity only refers to how original the writer is.', 'Creativity also includes the reader\'s active, imaginative role in constructing meaning and the creative reuse of conventions.')],
  evaluate=[('The concept of representation is more useful for non-literary texts than for literary works.', ['adverts and news openly construct images of groups', 'visual texts make representation easy to analyse'], ['novels and plays also represent class, gender and power', 'literary representation can be more complex and ambiguous'], 'It is equally useful; it simply operates more overtly in non-literary texts and more subtly in literary ones.')],
  extended=[('Choose two of the seven course concepts. Explain how each could help you analyse a speech you have studied, and evaluate which is more illuminating.', 'Indicative content: define each concept; apply to specific features of the speech (e.g. perspective – whose experience is voiced; communication – rhetorical devices for a live audience); reasoned judgement about which reveals more.', 6, 'long')])
pq('ch01-st2', 'C3', (2, 4), None, 'concept', CONCEPT_Q, crit=CRIT_OPEN)
pq('ch01-st2', 'C4', (3, 5), None, 'concept', ['Discuss how the text could be used to explore TWO of the seven course concepts, beginning with {cname}.',
                                              'To what extent is {cname} the most useful concept for understanding this text? Refer closely to the text.'], typ='long', marks=None, crit=MARKBAND)

H('ch01-st3',
  terms=[('learner portfolio', 'an individual collection of a student\'s responses to the texts and works studied, kept throughout the course; it is not assessed but supports all assessments'),
         ('reflective entry', 'a learner portfolio entry in which the student considers their own response, assumptions and learning about a text'),
         ('exploratory entry', 'a learner portfolio entry that tests ideas, asks questions or experiments with creative responses to a text'),
         ('analytical entry', 'a learner portfolio entry that closely examines how specific features of a text create meaning')],
  facts=[('Is the learner portfolio formally assessed by the IB?', 'No – it is not assessed but must be kept and may be requested', ['Yes – it is worth 20% of the final grade', 'Yes – it replaces the Individual Oral', 'Only at HL'], 'The learner portfolio is a required, unassessed part of the course.'),
         ('Which assessment does the learner portfolio most directly help with?', 'All of them – it is the basis for Paper 1, Paper 2, the Individual Oral and the HL essay', ['Only Paper 1', 'Only the Extended Essay', 'Only TOK'], 'The portfolio stores ideas, annotations and connections used across the assessments.')],
  why=[('Explain why the learner portfolio should include creative responses as well as analysis.', 'Writing creatively (for example rewriting a scene from another perspective) helps students understand writers\' choices from the inside and explore the concept of creativity.'),
       ('Explain why keeping a learner portfolio helps with the Individual Oral.', 'The portfolio records global issues and connections between literary and non-literary texts as they are studied, so students can find suitable extracts and a focus for the oral.'),
       ('Explain why reflection on one\'s own assumptions belongs in a learner portfolio.', 'Meaning depends on the reader\'s context; recording how one\'s responses change shows awareness of perspective and helps develop more nuanced interpretations.')],
  contrast=[('an analytical entry', 'a reflective entry', 'An analytical entry examines how textual features create meaning (e.g. annotating imagery); a reflective entry considers the student\'s own response and learning (e.g. how their view of a character changed).')],
  misc=[('The learner portfolio is a polished essay submitted at the end of the course.', 'It is an ongoing, varied collection of entries – notes, annotations, creative pieces and reflections – not a single polished essay, and it is not submitted for marking.'),
        ('Learner portfolio entries should only be written.', 'Entries can be multimodal – mind maps, annotated images, audio recordings or videos.')],
  apply=[('Write a reflective learner portfolio entry (about 150 words) in which you consider how your first impression of a character in a novel you are studying changed after the second chapter.', 'Indicative content: states the first impression and the evidence for it; identifies the moment and the authorial choice that changed it; reflects on what the change reveals about the writer\'s method and the student\'s assumptions.', 4, 'long'),
         ('Design an exploratory learner portfolio entry that connects a poem you have studied with an advertisement on the same global issue. List three things you would include.', 'Possible items: an annotated copy of both texts; a table comparing how each represents the issue; a question for further inquiry (e.g. "Why does the advert simplify what the poem complicates?").', 3)],
  evaluate=[('The learner portfolio is the most important part of the course even though it is not assessed.', ['it underpins every assessment', 'it develops independent thinking'], ['without marks students may neglect it', 'assessments test skills that can be developed elsewhere'], 'Its value depends on use: a rich, regular portfolio is central to success, but its importance lies in what it enables rather than in itself.')],
  extended=[('Write a learner portfolio entry of about 300 words that compares how a literary work and a non-literary text you have studied represent the same global issue, ending with a question for further exploration.', 'Indicative content: clearly identified global issue; at least two specific features from each text; comparison of methods and effects; an open, inquiring question. Markband: insight, specific reference, organisation, clear register.', 8, 'long')])
pq('ch01-st3', 'C3', (2, 4), None, 'issue', ['Write the opening of a learner portfolio entry on this text, identifying the global issue it raises and one question you would like to investigate.',
                                            'In a short learner portfolio note, record the global issue this text engages with and one feature you would analyse.'], crit=CRIT_OPEN)
pq('ch01-st3', 'C4', (3, 5), NONLIT, 'read', ['Write a reflective learner portfolio entry (about 200 words) on this text, considering how readers with different contexts might respond to it.',
                                              'For your learner portfolio, write an exploratory entry comparing your own response to this text with a possible resistant reading.'], typ='long', crit=MARKBAND)


# =============================================================================================
# ch02 Readers, writers and texts: how texts make meaning (non-literary text types)
# =============================================================================================
H('ch02-st1',
  terms=[('audience', 'the people a text is intended for, whose knowledge, values and expectations shape the writer\'s choices'),
         ('purpose', 'what a text aims to achieve – for example to persuade, inform, entertain, provoke or commemorate'),
         ('context of production', 'the circumstances in which a text was created – time, place, culture, medium and the writer\'s situation'),
         ('context of reception', 'the circumstances in which a text is read or viewed, which may differ from those in which it was produced'),
         ('implied reader', 'the reader that a text\'s language and assumptions seem to address, which may differ from any actual reader')],
  facts=[('Which of these best describes the "context of reception" of a 1940s propaganda poster studied today?', 'A 21st-century classroom where students analyse it critically', ['A wartime factory gate in the 1940s', 'The government office that commissioned it', 'The artist\'s studio'], 'Context of reception is where and when the text is read now.'),
         ('A speech delivered at a youth climate summit and later shared online has which kind of audience?', 'A primary (live) audience and a secondary (online) audience', ['Only the people in the room', 'No identifiable audience', 'Only the speaker\'s friends'], 'Texts often have multiple audiences with different expectations.')],
  why=[('Explain why the same advertisement might be interpreted differently by two audiences.', 'Meaning depends on readers\' contexts: values, cultural knowledge and experience lead them to read connotations and images differently.'),
       ('Explain why identifying purpose is the first step in analysing a non-literary text.', 'Purpose explains why the writer made particular choices, so features can be analysed for their effect in achieving that aim rather than merely listed.'),
       ('Explain why a text\'s medium is part of its context.', 'The medium (bus shelter, social feed, newspaper) determines who sees the text, how long they spend with it and what conventions apply.')],
  contrast=[('context of production', 'context of reception', 'Context of production is when, where and why a text was made; context of reception is when, where and by whom it is read. A text may gain new meanings when the two differ.'),
            ('the intended audience', 'the actual audience', 'The intended audience is who the writer had in mind; the actual audience is whoever reads it, including unintended readers such as students analysing it later.')],
  misc=[('A text has only one purpose.', 'Many texts have primary and secondary purposes – an advert may inform and entertain while its main purpose is to persuade.'),
        ('Context means the historical period in which the writer lived.', 'Context includes historical period but also culture, medium, place of publication, audience and the conditions of reading.')],
  evaluate=[('Knowing the context of a non-literary text is more important than close reading of its language.', ['context explains purpose and audience', 'misreading context leads to misinterpretation'], ['Paper 1 texts are unseen and context must be inferred from the language', 'close reading reveals how meaning is made'], 'Both are needed, but on Paper 1 context is usually inferred from close reading, so language analysis is the route to context.')],
  extended=[('Compare how two non-literary texts you have studied address different audiences on the same issue.', 'Indicative content: identifies each audience and evidence; compares register, tone and appeals; evaluates effectiveness for each audience.', 6, 'long')])
pq('ch02-st1', ('C2', 'C3'), (1, 4), NONLIT, 'aud', AUD_Q, crit=CRIT_A)
pq('ch02-st1', ('C2', 'C3'), (1, 4), NONLIT, 'purp', PURP_Q, crit=CRIT_A)
pq('ch02-st1', 'C3', (2, 5), NONLIT, 'ctx', CTX_Q, crit=CRIT_A)
pq('ch02-st1', 'C4', (3, 5), NONLIT, ('aud', 'purp', 'ctx'), ['Analyse how the writer adapts the text to its audience, purpose and context.',
                                                              'Evaluate how effectively the text is shaped for its audience and purpose in its context.'], typ='long', crit=MARKBAND)

H('ch02-st2',
  terms=[('diction', 'the writer\'s choice of words, including their connotations, formality and specificity'),
         ('tone', 'the attitude of the writer or speaker towards the subject or audience, conveyed through language choices'),
         ('register', 'the level of formality of language, chosen to suit audience, purpose and context'),
         ('rhetorical question', 'a question asked for effect rather than to obtain an answer, often to provoke thought or imply a point'),
         ('tricolon', 'a series of three parallel words, phrases or clauses used for rhythm and emphasis'),
         ('antithesis', 'the placing of contrasting ideas side by side in balanced phrases'),
         ('connotation', 'the associations a word carries beyond its literal meaning')],
  facts=[('"We shall fight on the beaches, we shall fight on the landing grounds" uses which device?', 'Anaphora', ['Oxymoron', 'Onomatopoeia', 'Euphemism'], 'Repeating "we shall fight" at the start of successive clauses is anaphora (Churchill, 1940).'),
         ('Which choice shows a shift to an informal register?', 'Using contractions and slang such as "gonna"', ['Using passive constructions', 'Using technical vocabulary', 'Using complete formal sentences'], 'Contractions and slang lower the formality of a text.')],
  why=[('Explain why identifying a device is not enough in Paper 1 analysis.', 'Criterion B rewards analysis of effect: a device only matters because of how it shapes meaning or affects the audience in relation to purpose.'),
       ('Explain why a writer might choose an informal register in a persuasive text.', 'Informality builds intimacy and trust with a peer audience and makes the writer seem authentic rather than authoritative or distant.'),
       ('Explain how connotation can carry bias in a news text.', 'Words with the same literal meaning ("protesters" versus "mob") carry different associations, so a writer can steer opinion while appearing to report facts.')],
  contrast=[('tone', 'mood', 'Tone is the writer\'s attitude conveyed by language; mood is the feeling the text creates in the reader. A sardonic tone may create an amused or uneasy mood.'),
            ('register', 'tone', 'Register is the level of formality; tone is the attitude. A formal register can carry an angry tone, and an informal register a tender one.')],
  misc=[('Rhetorical devices are only found in speeches.', 'Rhetorical devices appear in adverts, columns, letters and social media posts – any text that aims to persuade.'),
        ('Using lots of technical device names makes an analysis stronger.', 'Precise terminology helps (criterion D) but marks depend on analysing effects; a list of names without effects stays in the lower markbands.')],
  evaluate=[('Tone is the single most important feature to analyse in a persuasive text.', ['tone shapes the reader\'s relationship with the writer', 'a misjudged tone can undermine persuasion'], ['tone is produced by diction, syntax and structure, which must be analysed', 'visual and structural features may matter more in multimodal texts'], 'Tone is a useful organising idea, but strong analysis explains how specific choices create it.')],
  extended=[('Write a 250-word persuasive paragraph for a school newsletter arguing for a later start to the school day, using at least three rhetorical devices. Then annotate each device and its intended effect.', 'Indicative content: clear argument for the audience (parents/students); devices such as rhetorical question, tricolon, statistic, anecdote; annotation explains effects. Assessed for persuasiveness, control of register and accuracy of annotation.', 8, 'long')])
pq_dev_mcq('ch02-st2', NONLIT)
pq_tone_mcq('ch02-st2', NONLIT)
pq('ch02-st2', ('C2', 'C3'), (1, 5), NONLIT, 'dev', DEV_Q)
pq('ch02-st2', 'C4', (3, 5), NONLIT, 'dev', ['Analyse how the writer\'s choice of language, including "{quote}", shapes the tone of the text.',
                                              'Evaluate the effectiveness of the {device} "{quote}" and of at least one other stylistic feature in achieving the writer\'s purpose.'], typ='long', crit=MARKBAND)

H('ch02-st3',
  terms=[('headline', 'the title of a news or opinion text, designed to attract attention and summarise or frame the content'),
         ('standfirst', 'a short summary paragraph beneath a headline that expands it and draws the reader in'),
         ('cohesion', 'the way parts of a text are linked through connectives, pronouns, repetition and lexical chains'),
         ('inverted pyramid', 'a news structure that places the most important information first and less important details later'),
         ('call to action', 'a closing instruction that tells the reader what to do, common in adverts and campaigns')],
  facts=[('Which structural feature typically appears at the end of an advertisement?', 'A call to action', ['A standfirst', 'A byline', 'A dateline'], 'Adverts often end by telling the reader what to do next.'),
         ('Why do news reports use the inverted pyramid?', 'So readers get the key facts first and editors can cut from the bottom', ['To hide the main point until the end', 'To create suspense like a short story', 'To present opinions before facts'], 'The inverted pyramid prioritises essential information.')],
  why=[('Explain why the placement of information at the end of a text can be powerful.', 'End position gives emphasis – the reader leaves with that idea – so writers place punchlines, calls to action or key words last.'),
       ('Explain how short paragraphs affect the reader of an online article.', 'They make the text easier to scan on a screen and give each point emphasis, though they may also fragment the argument.'),
       ('Explain how a shift in a text\'s structure can signal a change in argument.', 'A turn such as "But" or a move from anecdote to general claim marks a pivot, guiding the reader from one stage of the argument to the next.')],
  contrast=[('structure', 'layout', 'Structure is the organisation and sequence of ideas (opening, turn, ending); layout is the visual arrangement on the page or screen (columns, images, white space). Both shape reading.'),
            ('cohesion', 'coherence', 'Cohesion is the surface linking of sentences through connectives and reference; coherence is the overall logical sense of the text. A text can be cohesive but incoherent if its ideas do not connect.')],
  misc=[('Structure only matters in long texts like novels.', 'Even a short advert has a deliberate structure – headline, image, body copy, call to action – that guides the reader.'),
        ('A headline simply summarises the article.', 'Headlines also frame and evaluate events, using connotation and word order to shape interpretation.')],
  evaluate=[('In non-literary texts, structure is more important than language.', ['structure controls what the reader sees first and last', 'layout is crucial in visual texts'], ['language creates tone and connotation', 'structure and language work together'], 'Neither dominates; analysis is strongest when it shows how structural placement intensifies language choices.')],
  extended=[('Rewrite the opening of a news report you have studied as an opinion column. Then explain how and why you changed its structure.', 'Indicative content: first-person hook, anecdote or provocative claim; argument with concession; commentary explaining the shift from inverted pyramid to argumentative structure.', 8, 'long')])
pq('ch02-st3', ('C2', 'C3'), (1, 5), NONLIT, 'struct', STRUCT_Q)
pq('ch02-st3', 'C4', (3, 5), NONLIT, 'struct', ['Analyse how the structure of the text, including {feature}, guides the reader towards the writer\'s purpose.',
                                                 'To what extent does the organisation of this text contribute more to its effect than its language? Refer to {feature} and at least one language choice.'], typ='long', crit=MARKBAND)

H('ch02-st4',
  terms=[('reader response', 'an approach that emphasises the reader\'s active role in constructing meaning from a text'),
         ('resistant reading', 'an interpretation that challenges or rejects the values a text seems to promote'),
         ('preferred reading', 'the interpretation a text appears to encourage, in line with the producer\'s intentions'),
         ('polysemy', 'the capacity of a word, image or text to carry several possible meanings')],
  facts=[('A feminist reader rejects the idealised image of a housewife in a 1950s advert. This is an example of:', 'A resistant reading', ['A preferred reading', 'An intentional fallacy', 'A literal reading'], 'Rejecting a text\'s apparent values is a resistant reading.'),
         ('Which statement reflects a reader-response approach?', 'Meaning is created in the interaction between reader and text', ['Meaning is fixed by the author\'s intention', 'Only historical context determines meaning', 'Texts have one correct interpretation'], 'Reader response stresses the reader\'s role.')],
  why=[('Explain why IB examiners reward alternative interpretations in Paper 1.', 'Criterion A rewards interpretation; considering more than one reading shows awareness that texts are open and that readers construct meaning.'),
       ('Explain how a reader\'s cultural context might affect their interpretation of an image.', 'Symbols and colours carry different connotations across cultures, so the same image may signify celebration to one reader and mourning to another.'),
       ('Explain why a text\'s ambiguity can be a strength.', 'Ambiguity invites active engagement and multiple valid readings, allowing a text to speak to different audiences and contexts.')],
  contrast=[('a preferred reading', 'a resistant reading', 'A preferred reading accepts the meaning the text encourages; a resistant reading challenges it from a different set of values or experiences.')],
  misc=[('If readers can interpret texts differently, then any interpretation is valid.', 'Interpretations must be supported by textual evidence; openness does not mean that unsupported readings are acceptable.'),
        ('The writer\'s intention is the only correct meaning of a text.', 'Intentions are often unknowable and meaning also depends on readers and contexts; analysis focuses on effects supported by the text.')],
  evaluate=[('The reader matters more than the writer in creating meaning.', ['readers bring contexts that change meaning', 'texts are reinterpreted over time'], ['writers make the choices that constrain interpretation', 'evidence in the text limits valid readings'], 'Meaning is co-created: the writer shapes the possibilities and the reader activates them.')],
  extended=[('Choose a text you have studied that has provoked controversy. Explain two contrasting readings and evaluate which is better supported by the text.', 'Indicative content: two clearly defined readings with contexts; evidence for each; reasoned evaluation. Markband: nuanced interpretation, specific evidence, balanced judgement.', 8, 'long')])
pq('ch02-st4', ('C3', 'C4'), (2, 5), NONLIT, 'read', READ_Q, crit=CRIT_OPEN)
pq('ch02-st4', 'C2', (2, 4), NONLIT, 'read', ['Explain why this text might be read differently by two different audiences.',
                                              'Explain how one feature of the text could be interpreted in more than one way.'], crit=CRIT_OPEN)


# =============================================================================================
# ch03 Readers, writers and texts: visual and multimodal texts
# =============================================================================================
H('ch03-st1',
  terms=[('composition', 'the arrangement of elements within an image or layout, which guides the viewer\'s eye and creates emphasis'),
         ('framing', 'what is included within or excluded from the edges of an image, and how closely the subject is shown'),
         ('typography', 'the style, size and arrangement of lettering, which carries connotations and creates hierarchy'),
         ('anchorage', 'the way words (such as a caption) fix the meaning of an image that could otherwise be read in several ways'),
         ('salience', 'the prominence of an element in a visual text, created by size, colour, contrast or position'),
         ('vectors', 'lines (real or implied, such as a gaze or a pointing arm) that direct the viewer\'s eye across an image')],
  facts=[('In visual analysis, a subject looking directly at the viewer creates which effect?', 'A "demand" image that confronts or engages the viewer', ['An "offer" image that invites detached viewing', 'A sense of distance and objectivity', 'Visual anchorage'], 'Direct gaze makes a demand on the viewer.'),
         ('A caption that tells the viewer how to interpret an image provides:', 'Anchorage', ['Salience', 'Vectors', 'Typography'], 'Words that fix an image\'s meaning are anchorage (Roland Barthes).')],
  why=[('Explain why colour choices matter in a visual text.', 'Colours carry cultural connotations (green for nature, red for danger) and create contrast, so they guide attention and emotional response.'),
       ('Explain how the rule of thirds can affect the viewer\'s response to an image.', 'Placing a subject on the intersection points rather than the centre creates a dynamic, natural composition that guides the eye and gives space for context.'),
       ('Explain why the relationship between image and text is important in multimodal texts.', 'Words and images can reinforce, extend or contradict each other; their interplay creates meanings neither would produce alone.')],
  contrast=[('a close-up', 'a long shot', 'A close-up fills the frame with the subject\'s face or a detail, creating intimacy and emotion; a long shot shows the subject in their setting, giving context and distance.'),
            ('a "demand" image', 'an "offer" image', 'In a demand image the subject looks at the viewer, requiring a response; in an offer image the subject looks away and is presented for the viewer to contemplate.')],
  misc=[('Visual analysis is just describing what is in the picture.', 'Description is only the start; analysis explains how choices of composition, colour and framing create meaning and affect the viewer.'),
        ('Typography is decoration and does not affect meaning.', 'Typefaces carry connotations (a serif font suggests tradition, a hand-drawn one intimacy) and size creates hierarchy.')],
  evaluate=[('In a multimodal text the image always matters more than the words.', ['images are processed quickly and emotionally', 'salience often belongs to the image'], ['captions anchor meaning', 'slogans are often the most memorable element'], 'Usually the image draws attention but words direct interpretation; their interplay matters most.')],
  extended=[('Describe in words a poster you would design for a campaign against food waste aimed at teenagers, explaining each visual choice (composition, colour, typography, image–text relationship) and its intended effect.', 'Indicative content: clear audience and purpose; justified visual choices with connotations; a slogan anchoring the image; evaluation of likely effect.', 8, 'long')])
pq('ch03-st1', ('C3', 'C4'), (2, 5), VISUAL, 'visual', VIS_Q)
pq('ch03-st1', 'C2', (2, 4), VISUAL, 'visual', ['Explain how one visual choice in this text directs the viewer\'s attention.',
                                                 'Explain why the visual composition of this text suits its purpose.'])
pq_dev_mcq('ch03-st1', VISUAL)

H('ch03-st2',
  terms=[('brand identity', 'the set of values, images and associations a company creates so that consumers recognise and relate to its products'),
         ('aspirational advertising', 'advertising that associates a product with a desirable lifestyle or identity the audience wishes to attain'),
         ('slogan', 'a short, memorable phrase associated with a brand or campaign'),
         ('target market', 'the specific group of consumers a product and its advertising are aimed at'),
         ('greenwashing', 'marketing that exaggerates or misrepresents a product\'s environmental benefits')],
  facts=[('An advert links a watch to images of a mountaineer on a summit. This is mainly an example of:', 'Aspirational advertising', ['Comparative advertising', 'A factual product description', 'A public service announcement'], 'The watch is sold through a desirable identity rather than its features.'),
         ('Which is an example of a "scarcity" technique in advertising?', '"Only 40 spots left!"', ['"Clinically tested"', '"Made in Switzerland"', '"Since 1920"'], 'Limited availability creates urgency.')],
  why=[('Explain why advertisers often sell a feeling or identity rather than the product\'s features.', 'Consumers buy products to express identity and meet emotional needs, so associating a product with belonging, status or self-worth creates stronger desire than functional claims.'),
       ('Explain how advertising can construct desire by first creating a problem.', 'Adverts often present a lack (dull skin, wasted time, isolation) that the reader may not have noticed, and then position the product as the solution.'),
       ('Explain why advertisements often use direct address.', 'Second-person address ("you") makes the reader feel personally spoken to, creating intimacy and placing them inside the scenario.')],
  contrast=[('informative advertising', 'persuasive advertising', 'Informative advertising mainly gives facts about a product (price, features); persuasive advertising uses emotional appeals, imagery and associations to create desire.'),
            ('a slogan', 'a headline', 'A slogan is a lasting phrase identifying a brand across campaigns; a headline is the main line of a particular advert.')],
  misc=[('Adverts only persuade people to buy products.', 'Adverts also sell values, lifestyles and norms (gender roles, beauty standards), shaping culture beyond the purchase.'),
        ('Viewers are passive victims of advertising.', 'Audiences negotiate, resist and parody adverts; media-literate readers recognise techniques.')],
  evaluate=[('Advertising reflects society\'s desires rather than creating them.', ['adverts follow market research', 'trends originate elsewhere'], ['adverts manufacture insecurities and new needs', 'repetition normalises values'], 'Advertising both reflects and amplifies desires; its power lies in turning existing anxieties into needs for products.')],
  extended=[('Compare how two advertisements you have studied construct desire for their products.', 'Indicative content: identify the desire constructed in each; analyse image, slogan, appeals; compare audiences; evaluate ethics.', 8, 'long')])
pq('ch03-st2', ('C3', 'C4'), (2, 5), {'ad'}, 'desire', ['Analyse how the advertisement constructs desire for the product.',
                                                         'How does the advertisement make its audience want the product? Refer to visual and verbal features.',
                                                         'Explain what the advertisement is really selling beyond the product itself.'])
pq('ch03-st2', ('C2', 'C3'), (1, 4), {'ad', 'parody'}, 'dev', ['Explain how the {device} "{quote}" helps to sell the product.',
                                                                'How does "{quote}" appeal to the target market?'])
pq_dev_mcq('ch03-st2', {'ad'})
pq_para('ch03-st2', {'ad'})

H('ch03-st3',
  terms=[('infographic', 'a visual representation of information or data that combines graphics and minimal text to communicate quickly'),
         ('editorial cartoon', 'a drawing that comments on current events or public figures, usually through exaggeration and satire'),
         ('caricature', 'a depiction that exaggerates distinctive features of a person for comic or critical effect'),
         ('panel', 'a single framed image in a comic or comic strip'),
         ('data visualisation', 'the presentation of data in visual form (charts, icons, scales) to reveal patterns')],
  facts=[('Which feature is most typical of an editorial cartoon?', 'Exaggeration used to comment on a current issue', ['Detailed statistical tables', 'A neutral, factual tone', 'Long paragraphs of argument'], 'Cartoons rely on visual exaggeration and satire.'),
         ('Why might an infographic place a large number in bold at the top?', 'To give the key statistic salience and immediate impact', ['To hide the source', 'To slow the reader down', 'To make the text literary'], 'Size and weight create salience.')],
  why=[('Explain why infographics can be misleading even when the data is accurate.', 'Choices of scale, axis, icon size and selection can exaggerate or minimise differences, and correlation can be presented as cause.'),
       ('Explain why cartoons are effective at communicating political criticism.', 'Humour and visual exaggeration make a point instantly and memorably, and laughter can lower readers\' resistance to criticism.'),
       ('Explain the role of timing in a three-panel comic strip.', 'The panels act like beats in a joke – set-up, development, punchline – so the gutter between panels creates anticipation.')],
  contrast=[('an infographic', 'a cartoon', 'An infographic aims to inform through data presented visually and claims objectivity; a cartoon comments on events through exaggeration and humour, openly expressing a viewpoint.')],
  misc=[('Infographics are objective because they present data.', 'Selection of data, design and framing all reflect choices; infographics often persuade as much as inform.'),
        ('Cartoons are not serious texts because they are funny.', 'Humour is a vehicle for serious comment; editorial cartoons can be powerful political critique.')],
  evaluate=[('Infographics communicate complex issues more effectively than written articles.', ['they are quick, shareable and memorable', 'visuals help readers grasp scale'], ['they oversimplify and omit nuance', 'they can mislead through design'], 'They are effective for attention and key facts but cannot replace the explanation and nuance of extended writing.')],
  extended=[('Design (in words) an infographic for students on the environmental cost of fast fashion, and explain how your design choices would persuade the audience.', 'Indicative content: headline, data selection, icons and scale, colour, call to action; justification of each choice for a student audience.', 8, 'long')])
pq('ch03-st3', ('C3', 'C4'), (2, 5), {'infographic', 'cartoon', 'meme'}, 'visual', VIS_Q + ['Explain how the visual design of this text makes its message quick to understand.'])
pq('ch03-st3', ('C2', 'C3'), (1, 4), {'infographic', 'cartoon', 'meme'}, 'purp', PURP_Q)
pq('ch03-st3', 'C3', (2, 4), {'infographic', 'cartoon', 'meme'}, 'dev', DEV_Q)
pq_para('ch03-st3', {'infographic', 'cartoon', 'meme'})

H('ch03-st4',
  terms=[('homepage', 'the main entry page of a website, designed to establish identity and guide users to content'),
         ('navigation bar', 'a menu of links that structures a website and signals its priorities'),
         ('hyperlink', 'a clickable link that connects one page or text to another, allowing non-linear reading'),
         ('user interface', 'the visual and interactive design through which a user operates a digital text'),
         ('dark pattern', 'an interface design that manipulates users into choices they may not intend, such as pre-ticked boxes')],
  facts=[('Why is the "Apply Now" button often the only brightly coloured element on a university homepage?', 'Colour contrast gives salience to the action the site wants users to take', ['It is a legal requirement', 'It hides the button from casual users', 'It indicates a broken link'], 'Salience guides the user towards the call to action.'),
         ('A pre-ticked box that signs donors up for monthly payments is an example of:', 'A dark pattern', ['A hyperlink', 'A banner', 'Anchorage'], 'It nudges users into a choice they may not intend.')],
  why=[('Explain why reading a website is different from reading a printed text.', 'Websites allow non-linear navigation through links, combine moving and interactive elements and are designed for scanning, so the user constructs their own path.'),
       ('Explain how a website\'s navigation menu reflects its values.', 'The order and naming of menu items reveal what the organisation prioritises and how it wants users to see it.'),
       ('Explain why chatbots on websites are a persuasive feature.', 'They simulate personal attention and conversation, making the institution seem friendly and responsive.')],
  contrast=[('a static web page', 'an interactive interface', 'A static page presents fixed content to be read; an interactive interface responds to the user\'s actions (buttons, chat, forms), shaping their path and choices.')],
  misc=[('Websites are neutral containers for information.', 'Website design makes choices about salience, order and interaction that persuade users and construct an identity for the organisation.')],
  apply=[('A charity\'s donation page lists buttons for 10, 25 and 50 euros, with 25 highlighted. Explain the persuasive effect of this design.', 'Highlighting the middle option makes it seem the normal choice (anchoring); users avoid the lowest option, so average donations increase.', 3),
         ('Describe two features you would include on the homepage of a youth mental-health service and explain their effect on a teenage audience.', 'For example: a calm colour palette and friendly informal headline to reduce stigma; a visible "Talk to someone now" button for immediate help; justified with reference to audience needs.', 4)],
  evaluate=[('Interactive digital texts give readers more power than printed texts.', ['readers choose their own paths', 'they can comment and share'], ['algorithms and design steer choices', 'dark patterns manipulate'], 'Readers gain apparent freedom, but interface design often directs that freedom.')],
  extended=[('Compare the homepage of a university with the donation page of a charity: how does each use design to persuade?', 'Indicative content: salience, imagery, calls to action, interactive features; differences in audience and ethics.', 8, 'long')])
pq('ch03-st4', ('C2', 'C3', 'C4'), (1, 5), {'website'}, 'struct', STRUCT_Q + ['Evaluate the ethics of {feature} in this web page.'])
pq('ch03-st4', ('C3', 'C4'), (2, 5), {'website'}, 'visual', VIS_Q + ['Analyse how this web page guides the user\'s eye and actions.'])
pq('ch03-st4', 'C3', (1, 4), {'website'}, 'dev', DEV_Q)
pq('ch03-st4', 'C3', (1, 4), {'website'}, 'aud', AUD_Q)


# =============================================================================================
# ch04 Literary work 1 – prose fiction
# =============================================================================================
PROSE = {'prose', 'story'}
H('ch04-st1',
  terms=[('first-person narration', 'narration by a character within the story using "I", giving direct access to that character\'s perceptions but limiting knowledge'),
         ('third-person omniscient narration', 'narration from outside the story by a narrator who knows the thoughts and actions of all characters'),
         ('third-person limited narration', 'narration from outside the story that stays close to one character\'s perceptions and thoughts'),
         ('focalisation', 'the perspective through which events are perceived in a narrative, which may differ from who is speaking'),
         ('free indirect discourse', 'a technique that blends a character\'s thoughts and idiom into third-person narration without quotation marks'),
         ('unreliable narrator', 'a narrator whose account the reader has reason to doubt because of bias, ignorance, self-deception or deceit')],
  facts=[('"Of course he would be late; he was always late." In a third-person passage, this sentence most likely shows:', 'Free indirect discourse', ['Second-person narration', 'Stream of consciousness in the first person', 'Direct speech'], 'The character\'s thought is blended into the narration without quotation marks.'),
         ('A child narrator who does not understand events the reader can infer creates:', 'Dramatic irony', ['Omniscience', 'Pathetic fallacy', 'Stichomythia'], 'The reader knows more than the narrator.')],
  why=[('Explain why a writer might choose a naïve narrator.', 'A naïve narrator\'s limited understanding forces the reader to infer what is really happening, creating dramatic irony, pathos and active engagement.'),
       ('Explain how focalisation can shape the reader\'s sympathy.', 'Seeing events through one character\'s perceptions gives access to their feelings and reasons, which tends to align the reader with them even if their actions are questionable.'),
       ('Explain why an unreliable narrator makes the reader work harder.', 'The reader must read between the lines, comparing the narrator\'s claims with clues in the text to reconstruct what actually happened.')],
  contrast=[('the narrator', 'the focaliser', 'The narrator is who tells the story; the focaliser is whose perception shapes what is shown. In third-person limited narration the narrator is external but the focaliser is a character.'),
            ('first-person narration', 'third-person limited narration', 'First-person narration uses a character\'s own voice ("I"); third-person limited uses an outside narrator ("she") but stays close to one character\'s perspective, allowing some ironic distance.')],
  misc=[('A first-person narrator always tells the truth because they were there.', 'Being present does not guarantee reliability; first-person narrators may be biased, mistaken or deliberately deceptive.'),
        ('Omniscient narrators have no attitude towards their characters.', 'Omniscient narrators often comment, judge or ironise, giving the narrative a distinctive voice and stance.')],
  evaluate=[('The choice of narrative voice is the most important decision a novelist makes.', ['voice controls access, sympathy and irony', 'the same plot changes completely with a different narrator'], ['structure, characterisation and setting also shape meaning', 'voice works with other elements'], 'Narrative voice is arguably foundational because it filters every other element, though its effects depend on how it interacts with them.')],
  extended=[('Rewrite a key paragraph from a prose work you have studied from a different character\'s point of view, then explain how the change of focalisation alters the meaning.', 'Indicative content: consistent new voice; plausible character perspective; commentary on what is revealed or hidden and how sympathy shifts.', 8, 'long')])
pq('ch04-st1', ('C2', 'C3'), (1, 5), PROSE, 'pov', ['Identify the narrative point of view in this extract and explain its effect on the reader.',
                                                   'How does the narrative voice shape what the reader learns in this extract?',
                                                   'Analyse the narrative perspective of the extract and its effect.',
                                                   'Explain how the choice of narrator affects the reader\'s response to events.'], crit=CRIT_B)
pq('ch04-st1', 'C4', (3, 5), PROSE, 'pov', ['To what extent does the narrative perspective control the reader\'s sympathies in this extract?',
                                            'Evaluate how the writer uses narrative voice and at least one other feature to create meaning in this extract.'], typ='long', crit=MARKBAND)

H('ch04-st2',
  terms=[('direct characterisation', 'the narrator or another character explicitly tells the reader what a character is like'),
         ('indirect characterisation', 'character revealed through speech, actions, thoughts, appearance and others\' reactions, for the reader to infer'),
         ('round character', 'a complex character with conflicting traits who can surprise the reader'),
         ('flat character', 'a simple character built around a single trait or idea'),
         ('foil', 'a character whose contrasting traits highlight those of another character')],
  facts=[('"Papa started sleeping in the afternoons." This is an example of:', 'Indirect characterisation through action', ['Direct characterisation', 'A flat character', 'Free indirect discourse'], 'The reader infers his state of mind from his behaviour.'),
         ('A character whose qualities contrast with the protagonist\'s to highlight them is called a:', 'Foil', ['Narrator', 'Antagonist only', 'Chorus'], 'A foil throws another character\'s traits into relief.')],
  why=[('Explain why writers often prefer indirect characterisation.', 'Showing rather than telling invites readers to infer, making characters feel more realistic and the reader more engaged.'),
       ('Explain how a reader\'s relationship with a character can change during a novel.', 'New information, shifts in focalisation or a character\'s choices can turn sympathy into judgement (or the reverse), which is often central to a work\'s meaning.'),
       ('Explain how minor characters contribute to characterisation of the protagonist.', 'Their reactions, contrasts and dialogue reveal the protagonist\'s traits and position in society.')],
  contrast=[('a round character', 'a flat character', 'A round character is complex and can change or surprise; a flat character is defined by one trait and serves a function. Flat characters are not necessarily weak writing.')],
  misc=[('Readers should like the protagonist for a novel to succeed.', 'Writers often create unlikeable or morally ambiguous protagonists to challenge readers; engagement does not depend on liking.'),
        ('Characters are real people and can be analysed like real people.', 'Characters are constructions; analysis should focus on how the writer creates them and what they represent, not on speculation beyond the text.')],
  evaluate=[('Readers learn most about a character from what other characters say about them.', ['others\' views offer external perspective', 'reputation shapes expectations'], ['actions and thoughts may contradict others\' views', 'narrative voice controls access'], 'Others\' views are useful but potentially biased; actions and the narrative\'s framing are usually more revealing.')],
  extended=[('Analyse how the writer of a prose work you have studied makes the reader feel ambivalent about a central character.', 'Indicative content: specific methods (focalisation, contrasting actions, irony); textual references; discussion of how ambivalence serves the work\'s themes.', 8, 'long')])
pq('ch04-st2', ('C2', 'C3'), (1, 5), PROSE | {'trans', 'drama'}, 'char', ['How does the writer characterise the people in this extract?',
                                                                       'Analyse the methods of characterisation used in this extract.',
                                                                       'What impression of the characters does the extract create, and how?',
                                                                       'Explain how the reader\'s attitude to a character is shaped in this extract.'], crit=CRIT_B)
pq('ch04-st2', 'C4', (3, 5), PROSE | {'trans'}, 'char', ['Discuss how the writer shapes the reader\'s relationship with the characters in this extract.',
                                                       'Evaluate the effectiveness of the indirect characterisation in this extract.'], typ='long', crit=MARKBAND)

H('ch04-st3',
  terms=[('setting', 'the time, place and social environment in which a narrative takes place'),
         ('symbol', 'an object, place or action that represents an idea beyond its literal meaning'),
         ('motif', 'a recurring image, idea or element that develops a theme across a work'),
         ('pathetic fallacy', 'the attribution of human feelings to nature or the weather, often to reflect a character\'s mood'),
         ('atmosphere', 'the emotional quality created by setting and description')],
  facts=[('A storm that breaks out as a character learns of a betrayal is an example of:', 'Pathetic fallacy', ['Foreshadowing only', 'Free indirect discourse', 'Bathos'], 'The weather mirrors the emotional situation.'),
         ('What distinguishes a motif from a symbol?', 'A motif recurs across the work; a symbol may appear once', ['A motif is always an object', 'A symbol is always a colour', 'There is no difference'], 'Recurrence is the key feature of a motif.')],
  why=[('Explain how setting can function as more than background.', 'Setting can mirror characters\' emotions, reflect social forces, create conflict and carry symbolic meaning.'),
       ('Explain why recurring motifs help a reader to interpret a novel.', 'Each recurrence gathers meaning, so the reader traces how the work develops a theme and changes its significance.'),
       ('Explain why a symbol\'s meaning may change during a work.', 'As characters and situations change, the same object takes on new associations; tracing this change shows the work\'s development.')],
  contrast=[('a symbol', 'a motif', 'A symbol stands for an idea beyond itself (a green light for longing); a motif is a recurring element (light, water) that may include symbols and develops meaning through repetition.')],
  misc=[('Every object in a novel is a symbol.', 'Only details that the text emphasises, repeats or links to larger ideas are convincingly symbolic; over-reading weakens analysis.')],
  evaluate=[('Setting is the key to understanding character in prose fiction.', ['social setting shapes characters\' choices', 'place often reflects inner states'], ['characters may resist their setting', 'voice and action also reveal character'], 'Setting is often central, but its importance lies in its interaction with character rather than determining it.')],
  extended=[('Write a 300-word descriptive opening for a short story in which the setting reflects a character\'s hidden emotion, then explain your choices.', 'Indicative content: controlled descriptive writing with pathetic fallacy or symbolic detail; commentary linking setting and emotion. Assessed on creativity, control and insight.', 8, 'long')])
pq('ch04-st3', ('C2', 'C3'), (1, 5), PROSE, 'setting', ['How does the writer use setting in this extract?',
                                                        'Explain how the setting reflects the situation or mood of the characters.',
                                                        'Analyse the function of the setting in this extract.'])
pq('ch04-st3', ('C3', 'C4'), (2, 5), PROSE | {'trans'}, 'symbol', ['Identify a symbol or motif in the extract and explain its significance.',
                                                                   'Analyse how symbolism contributes to the meaning of the extract.',
                                                                   'Discuss how the writer uses symbolic detail to suggest more than is stated.'])

H('ch04-st4',
  terms=[('chronology', 'the order in which events actually happen, which a narrative may follow or rearrange'),
         ('analepsis', 'a flashback: a narrative return to events earlier than the main story'),
         ('prolepsis', 'a flash-forward: a narrative anticipation of events that will happen later'),
         ('foreshadowing', 'hints or signs of events to come'),
         ('closure', 'the degree to which a narrative\'s ending resolves its conflicts and questions'),
         ('in medias res', 'beginning a narrative in the middle of the action')],
  facts=[('"Afterwards, everyone would say that the signs had been there." This sentence is an example of:', 'Prolepsis', ['Analepsis', 'In medias res', 'Stream of consciousness'], 'It flashes forward to a later time.'),
         ('A novel that ends without resolving its central conflict has:', 'An open ending', ['Full closure', 'A frame narrative', 'Linear chronology'], 'Open endings leave questions unanswered.')],
  why=[('Explain why a writer might reveal the ending at the beginning.', 'Revealing the outcome shifts the reader\'s interest from what happens to how and why, creating dread and focusing attention on causes and responsibility.'),
       ('Explain how flashbacks can affect the reader\'s understanding of a character.', 'Analepsis reveals past experiences that explain present behaviour, often changing the reader\'s judgement.'),
       ('Explain why some novels avoid closure.', 'Open endings reflect the uncertainty of life, invite readers to continue thinking and resist simplistic moral resolutions.')],
  contrast=[('story', 'plot', 'The story is the chronological sequence of events; the plot is the order and manner in which the narrative presents them, including rearrangements and emphasis.'),
            ('analepsis', 'prolepsis', 'Analepsis moves back in time to earlier events (flashback); prolepsis moves forward to anticipate later ones (flash-forward).')],
  misc=[('Foreshadowing spoils the suspense of a story.', 'Foreshadowing creates a different kind of suspense – anticipation and dread – and makes the ending feel meaningful.')],
  evaluate=[('Non-linear narratives are more demanding but more rewarding for readers.', ['they mirror memory and trauma', 'readers actively reconstruct events'], ['they can confuse', 'linear narratives can be just as complex'], 'They reward active reading when the fragmentation serves meaning, but complexity is not automatically value.')],
  extended=[('Evaluate how the ending of a prose work you have studied shapes the reader\'s understanding of the whole work.', 'Indicative content: description of the ending; degree of closure; links to themes and structure; evaluation of effect.', 8, 'long')])
pq('ch04-st4', ('C2', 'C3', 'C4'), (1, 5), PROSE, 'time', ['How does the writer handle time in this extract?',
                                                          'Analyse how the structure of the extract creates tension or expectation.',
                                                          'Explain the effect of the narrative\'s treatment of time and sequence in this extract.',
                                                          'Evaluate how the arrangement of events in this extract shapes the reader\'s response.'])
pq('ch04-st4', 'C3', (2, 4), PROSE, 'struct', STRUCT_Q)


# =============================================================================================
# ch05 Literary work 2 – poetry
# =============================================================================================
H('ch05-st1',
  terms=[('metre', 'the pattern of stressed and unstressed syllables in a line of verse'),
         ('iambic pentameter', 'a line of five iambs (unstressed–stressed pairs), ten syllables, common in English verse'),
         ('enjambment', 'the continuation of a sentence beyond the end of a line or stanza without a pause'),
         ('caesura', 'a pause within a line of poetry, often marked by punctuation'),
         ('volta', 'a turn in thought or argument within a poem, especially in a sonnet'),
         ('free verse', 'poetry without regular metre or rhyme scheme'),
         ('sonnet', 'a fourteen-line poem, usually in iambic pentameter, with a set rhyme scheme (Petrarchan or Shakespearean)')],
  facts=[('How many lines are in a sonnet?', 'Fourteen', ['Twelve', 'Sixteen', 'Ten'], 'Sonnets have fourteen lines.'),
         ('A Shakespearean sonnet usually ends with:', 'A rhyming couplet', ['A sestet', 'A refrain', 'A tercet'], 'Shakespearean sonnets are three quatrains plus a couplet (ABAB CDCD EFEF GG).'),
         ('Which line is in iambic tetrameter?', '"She learned the sea before her name"', ['"Tomorrow, and tomorrow, and tomorrow"', '"Click of turnstiles, clack of heels"', '"Life\'s but a walking shadow, a poor player"'], 'It has four iambs: she LEARNED / the SEA / be-FORE / her NAME.')],
  why=[('Explain why a poet might choose a strict form for a poem about chaos or loss.', 'The tension between ordered form and disordered content can suggest an attempt to control grief, or make the breakdown more striking.'),
       ('Explain the effect of enjambment in a poem.', 'Running a sentence over a line break creates momentum or delay, can place surprising emphasis on the first word of the next line, and may enact the meaning.'),
       ('Explain why caesura can be powerful in a line of poetry.', 'A mid-line pause interrupts rhythm, creating emphasis, hesitation or a sense of breaking.')],
  contrast=[('free verse', 'blank verse', 'Free verse has no regular metre or rhyme; blank verse is unrhymed but written in regular iambic pentameter.'),
            ('enjambment', 'end-stopping', 'Enjambment carries a sentence over the line break; end-stopping ends the sense with the line, often with punctuation, creating a pause.')],
  misc=[('Free verse is poetry with no structure.', 'Free verse lacks regular metre and rhyme but uses deliberate structure – line breaks, stanza shapes, repetition – for effect.'),
        ('Rhyme is used in poems simply to make them sound nice.', 'Rhyme creates connections between words, emphasis, closure or irony; poets often use it to link or contrast ideas.')],
  evaluate=[('Form is the most important element of a poem\'s meaning.', ['form shapes rhythm, emphasis and expectation', 'a change of form can signal a change of meaning'], ['imagery and voice carry much of the meaning', 'many readers respond first to language'], 'Form is integral rather than supreme: it matters most when it interacts with imagery and voice.')],
  extended=[('Write a short poem (8–14 lines) in a fixed form of your choice about a place that has changed, then explain how the form supports your meaning.', 'Indicative content: accurate form; purposeful line breaks and rhyme; commentary connecting form and meaning.', 8, 'long')])
pq('ch05-st1', ('C2', 'C3', 'C4'), (1, 5), {'poem'}, 'form', ['How does the form of the poem contribute to its meaning?',
                                                            'Analyse the poet\'s structural choices in this poem.',
                                                            'Explain the effect of the poem\'s stanza form, line length or rhyme.',
                                                            'Evaluate how far the poem\'s form reinforces its content.'])

H('ch05-st2',
  terms=[('imagery', 'language that appeals to the senses and creates pictures in the reader\'s mind'),
         ('metaphor', 'a figure of speech that describes something as if it were something else'),
         ('simile', 'a comparison using "like" or "as"'),
         ('extended metaphor', 'a metaphor developed over several lines or a whole poem'),
         ('sibilance', 'the repetition of "s" and "sh" sounds'),
         ('assonance', 'the repetition of vowel sounds in nearby words'),
         ('onomatopoeia', 'a word whose sound imitates its meaning')],
  facts=[('"Hope is the thing with feathers / That perches in the soul" is an example of:', 'Extended metaphor', ['Onomatopoeia', 'Simile', 'Oxymoron'], 'Hope is developed as a bird over the stanza.'),
         ('"Click of turnstiles, clack of heels" mainly uses:', 'Onomatopoeia', ['Assonance', 'Euphemism', 'Pathetic fallacy'], '"Click" and "clack" imitate sounds.')],
  why=[('Explain why poets use sound patterning.', 'Sound patterns create music, link words, mimic what is described and influence pace and mood, so meaning is felt as well as understood.'),
       ('Explain why a recurring image across a poet\'s body of work is significant.', 'Recurrence reveals the poet\'s preoccupations; tracing how an image develops shows changes in attitude or meaning across poems.'),
       ('Explain the difference in effect between a simile and a metaphor.', 'A simile keeps the comparison visible ("like"), so it can seem tentative or precise; a metaphor fuses the two, creating a stronger, more immediate identification.')],
  contrast=[('alliteration', 'assonance', 'Alliteration repeats initial consonant sounds in nearby words ("coughing ... cursed"); assonance repeats vowel sounds within nearby words (the long "i" in "light like fire"). Alliteration often adds force; assonance often creates a softer musical link.'),
            ('literal imagery', 'figurative imagery', 'Literal imagery describes what is actually there in sensory detail; figurative imagery uses comparisons (metaphor, simile, personification) to suggest something beyond the literal.')],
  misc=[('Naming the sound device is enough to analyse sound in poetry.', 'Analysis must explain how the sound contributes to meaning or mood; naming sibilance without effect earns little credit.'),
        ('Imagery only refers to visual pictures.', 'Imagery appeals to all senses – sound, touch, taste, smell – and to movement and feeling.')],
  evaluate=[('Sound is less important than imagery in poetry read silently.', ['silent reading emphasises meaning and image', 'readers often notice imagery first'], ['readers "hear" poems internally', 'sound shapes pace and mood even in silence'], 'Sound remains important; poems are written for the ear, and silent reading still registers rhythm and sound.')],
  extended=[('Compare how two poems by a poet you have studied use a recurring image, and what the comparison reveals about the poet\'s concerns.', 'Indicative content: identification of the image in each; analysis of context within each poem; development or contrast; link to concerns.', 8, 'long')])
pq('ch05-st2', ('C2', 'C3'), (1, 5), {'poem'}, 'imagery', ['Analyse the imagery in this poem.',
                                                          'How does figurative language contribute to the meaning of the poem?',
                                                          'Explain the effect of one image in the poem.'])
pq('ch05-st2', ('C3', 'C4'), (2, 5), {'poem'}, 'sound', ['Analyse how sound patterning contributes to the poem\'s effect.',
                                                        'How does the poet use sound to reinforce meaning?',
                                                        'Evaluate the contribution of sound and rhythm to the mood of the poem.'])
pq_dev_mcq('ch05-st2', {'poem'})

H('ch05-st3',
  terms=[('speaker', 'the voice that speaks in a poem, which should not be automatically identified with the poet'),
         ('persona', 'a character or mask adopted by the poet as the speaker of a poem'),
         ('dramatic monologue', 'a poem in which a single persona speaks to a silent listener, revealing their character'),
         ('lyric poem', 'a short poem expressing personal thought or feeling, often in the first person'),
         ('collection', 'a book of poems by a poet, studied as a single literary work in the course')],
  facts=[('"The Statue Speaks" is written in the voice of a statue. This technique is called:', 'Using a persona (dramatic monologue)', ['Free indirect discourse', 'Omniscient narration', 'Pathetic fallacy'], 'The poet adopts the voice of a character.'),
         ('Why should students write "the speaker" rather than "the poet"?', 'The voice of a poem is a construction and may not be the poet\'s own', ['Examiners forbid naming poets', 'Poets never write about themselves', 'It sounds more formal'], 'Distinguishing speaker from poet avoids biographical assumptions.')],
  why=[('Explain why a poet might adopt a persona.', 'A persona allows the poet to explore perspectives different from their own, create irony between what the speaker says and what the reader sees, and give voice to the silenced.'),
       ('Explain how tone can shift within a poem.', 'Changes in diction, syntax or address (often at a volta) signal a change in attitude, which may mark the poem\'s emotional development.'),
       ('Explain why studying the tone across a whole collection matters.', 'A collection is one literary work; patterns or shifts in tone across poems reveal the poet\'s range and the development of concerns.')],
  contrast=[('the poet', 'the speaker', 'The poet is the real writer; the speaker is the voice in the poem, which may be a persona. Even first-person lyrics construct a voice rather than transcribe the poet.')],
  misc=[('All first-person poems are autobiographical.', 'The "I" of a poem is a constructed voice; even when drawing on experience, poets shape and fictionalise.')],
  evaluate=[('Dramatic monologue is the most effective way for poetry to explore marginalised perspectives.', ['it gives a voice directly', 'irony can reveal more than the speaker knows'], ['lyric and narrative poems also do this', 'a poet ventriloquising others raises questions of appropriation'], 'It is powerful but not unique, and its ethics depend on who speaks for whom.')],
  extended=[('Write a dramatic monologue (12–16 lines) in the voice of an overlooked object or figure in your community, then explain how your persona creates meaning.', 'Indicative content: consistent persona; implied listener; irony; commentary on the choices.', 8, 'long')])
pq('ch05-st3', ('C2', 'C3'), (1, 5), {'poem'}, 'speaker', ['Describe the speaker of the poem and their attitude to the subject.',
                                                          'How does the poet create the voice of the speaker?',
                                                          'Analyse the tone of the poem and how it is created.'])
pq_tone_mcq('ch05-st3', {'poem'})
pq('ch05-st3', 'C4', (3, 5), {'poem'}, 'speaker', ['Discuss how the poet uses the speaker\'s voice to shape the reader\'s response to the subject.',
                                                    'Evaluate how the speaker\'s tone develops across the poem.'], typ='long', crit=MARKBAND)

H('ch05-st4',
  terms=[('PEEL paragraph', 'a paragraph structure: Point, Evidence, Explanation (analysis of effect), Link back to the question'),
         ('embedded quotation', 'a short quotation integrated grammatically into the writer\'s own sentence'),
         ('topic sentence', 'the opening sentence of a paragraph that states its argument'),
         ('close reading', 'detailed analysis of the language, form and structure of a short passage')],
  facts=[('Which is the best-embedded quotation?', 'The speaker\'s mother "packed the country in a suitcase", reducing a homeland to luggage.', ['Quote: "packed the country in a suitcase". This is a metaphor.', 'There is a metaphor in line 1.', 'The metaphor is good because it is interesting.'], 'The quotation is integrated into the sentence and followed by analysis.'),
         ('What should a topic sentence in an analytical paragraph do?', 'State an argument that answers the question', ['Summarise the plot', 'List all devices in the poem', 'Give the poet\'s biography'], 'A topic sentence makes an analytical claim.')],
  why=[('Explain why short, embedded quotations are better than long ones in analysis.', 'They show precise selection, allow detailed comment on specific words and keep the student\'s argument in control.'),
       ('Explain why each analytical paragraph should link back to the question.', 'Linking keeps the analysis focused (criterion C) and shows how each point supports the overall argument.'),
       ('Explain why analysing a single word can be effective.', 'Zooming in on connotation, sound or position shows precise understanding of how the poet\'s choices shape meaning (criterion B).')],
  contrast=[('summary', 'analysis', 'Summary restates what a text says; analysis explains how and why the writer\'s choices create meaning and effects.')],
  misc=[('A good analytical paragraph mentions as many devices as possible.', 'Depth matters more than breadth: developing one or two well-chosen features fully earns more credit than listing many.')],
  apply=[('Rewrite this weak sentence as an analytical sentence: "The poet uses a simile which is effective."', 'Example: "By comparing the grandfather\'s skill to the way \'a farmer knows rain\', the poet presents his craft as patient, instinctive knowledge rooted in long experience." (names the device, embeds evidence, explains effect).', 3),
         ('Order these parts into a strong analytical paragraph: (a) "This suggests ..."; (b) a topic sentence answering the question; (c) an embedded quotation; (d) a link to the poem\'s wider concern.', 'b, c, a, d – point, evidence, explanation, link.', 2)],
  evaluate=[('Formulaic paragraph structures such as PEEL limit good literary analysis.', ['they help beginners organise', 'they ensure evidence and explanation'], ['they can produce mechanical writing', 'sophisticated analysis weaves several points'], 'They are a useful scaffold early on but should be adapted as analysis becomes more sophisticated.')],
  extended=[('Write one analytical paragraph on a poem you have studied, answering the question: "How does the poet present loss?"', 'Indicative content: topic sentence with argument; two embedded references; analysis of effect; link. Markband: precise, perceptive analysis, controlled register.', 6, 'long')])
pq_para('ch05-st4', {'poem'}, c=('C3', 'C4'), d=(2, 5), frames=['Guiding question: {gq}\nWrite one analytical paragraph that answers the guiding question, using at least two embedded quotations.',
                                                                 'Write a close analytical paragraph on the poem, focusing on the question: "{gq}"',
                                                                 'Plan and write a paragraph answering: "{gq}" Begin with a topic sentence that states your argument.'])


# =============================================================================================
# ch06 Time and space: texts in context (non-literary bodies of work)
# =============================================================================================
H('ch06-st1',
  terms=[('historical context', 'the events, conditions and ideas of the period in which a text was produced'),
         ('cultural context', 'the beliefs, customs and values of the community in which a text was produced or is read'),
         ('political context', 'the power structures, conflicts and ideologies that shape a text\'s production and reception'),
         ('anachronistic reading', 'judging a text from the past purely by present-day values without considering its context'),
         ('zeitgeist', 'the defining spirit or mood of a particular period of history')],
  facts=[('Which piece of contextual knowledge best helps a reader interpret a 1912 suffrage speech?', 'Women could not vote in UK parliamentary elections at the time', ['The speaker\'s favourite colour', 'Modern social media habits', 'The price of the newspaper today'], 'Relevant context explains the text\'s purpose and urgency.'),
         ('Studying a body of work "across time and space" means:', 'Considering how texts relate to the times and places in which they are produced and read', ['Only reading texts from one century', 'Only reading science fiction', 'Ignoring authors\' backgrounds'], 'The Time and space area of exploration focuses on context.')],
  why=[('Explain why the meaning of a text can change over time.', 'Readers in later periods bring different values and knowledge, and events after publication may change the significance of a text\'s language and images.'),
       ('Explain why context should be integrated into analysis rather than added as background.', 'Context is only valuable when it explains a specific choice or effect; a separate history lesson does not show how the text creates meaning.'),
       ('Explain how studying a body of work from one period helps reveal its context.', 'Recurring images and concerns across several texts reveal shared assumptions and pressures of the time.')],
  contrast=[('historical context', 'cultural context', 'Historical context concerns events and conditions of a time (a war, an election); cultural context concerns beliefs, customs and values of a community (attitudes to gender, religion).')],
  misc=[('Texts from the past should be judged only by the values of their own time.', 'Readers can recognise a text\'s original context while still critically evaluating its values from a present perspective; both readings are valid if supported.'),
        ('Context is the same as the writer\'s biography.', 'Biography is one part of context; social, political, cultural and medium-related contexts also shape meaning.')],
  evaluate=[('A text cannot be understood without knowing its historical context.', ['context explains allusions and purpose', 'misreadings occur without it'], ['many texts remain powerful across time', 'close reading reveals much'], 'Context deepens understanding but is not always essential; the strongest readings combine close reading with contextual insight.')],
  extended=[('Choose a non-literary body of work you have studied (for example a set of posters or photographs from one period). Analyse how context shapes the representation of a group within it.', 'Indicative content: specific texts; representation analysed; context integrated to explain choices; evaluation from present perspective.', 8, 'long')])
pq('ch06-st1', ('C2', 'C3', 'C4'), (1, 5), {'speech', 'propaganda', 'photo', 'news', 'oped'}, 'ctx', CTX_Q + ['Evaluate how far a reader needs to know the context to understand this text.'], crit=CRIT_A)
pq('ch06-st1', 'C3', (2, 4), {'speech', 'propaganda', 'photo'}, 'read', ['How might a reader at the time of production and a reader today respond differently to this text?',
                                                                        'Explain how the meaning of this text might change for a present-day reader.'], crit=CRIT_OPEN)

H('ch06-st2',
  terms=[('bias', 'a one-sided presentation that favours a particular viewpoint'),
         ('framing', 'the selection and emphasis of aspects of an event so that it is interpreted in a particular way'),
         ('agenda-setting', 'the media\'s power to influence which issues the public thinks are important'),
         ('editorial', 'an article expressing the official opinion of a newspaper'),
         ('objectivity', 'the journalistic ideal of reporting facts without personal bias')],
  facts=[('One newspaper calls protesters "students marching"; another calls them a "mob". This is an example of:', 'Framing through connotation', ['Objective reporting', 'The inverted pyramid', 'A call to action'], 'Different words frame the same event differently.'),
         ('Which feature suggests a text is an opinion column rather than a news report?', 'A first-person voice arguing a stance', ['An inverted pyramid', 'A dateline', 'Quotations from officials'], 'Columns present a personal argument.')],
  why=[('Explain how news can shape public opinion without stating opinions.', 'Through selection of facts, order of information, choice of sources and the connotations of words, news frames events and steers interpretation.'),
       ('Explain why quoting an eyewitness is effective in a news report.', 'It adds human interest and emotional impact and gives the appearance of authenticity while the reporter remains neutral.'),
       ('Explain why headlines are powerful in shaping opinion.', 'Many readers only see the headline, so its wording and framing determine the impression of the event.')],
  contrast=[('a news report', 'an opinion column', 'A news report aims to present facts in a neutral third-person voice using the inverted pyramid; an opinion column openly argues a personal view, using rhetoric and anecdote.'),
            ('bias', 'framing', 'Bias is a one-sided slant in favour of a view; framing is the broader process of selecting and emphasising aspects of an issue. Framing can produce bias but is present in all reporting.')],
  misc=[('A news report that contains no opinions is unbiased.', 'Bias can operate through selection, order, sources and connotation, even when no explicit opinion is stated.')],
  evaluate=[('Journalism can never be truly objective.', ['every report involves selection and framing', 'journalists have contexts'], ['professional standards and verification reduce bias', 'fact and opinion can still be distinguished'], 'Complete objectivity is impossible, but fairness and accuracy are achievable standards that matter.')],
  extended=[('Write two short news reports (about 120 words each) of the same school event, one framing it positively and one negatively. Then explain the techniques you used.', 'Indicative content: same facts; contrasting diction, order, sources and headlines; commentary naming techniques.', 8, 'long')])
pq('ch06-st2', ('C2', 'C3'), (1, 5), {'news', 'oped'}, 'dev', DEV_Q)
pq('ch06-st2', ('C3', 'C4'), (2, 5), {'news'}, 'struct', STRUCT_Q + ['Evaluate how {feature} shapes the reader\'s opinion of the event.'])
pq('ch06-st2', 'C3', (1, 4), {'news', 'oped'}, 'purp', PURP_Q)
pq_para('ch06-st2', {'news', 'oped'})

H('ch06-st3',
  terms=[('propaganda', 'communication designed to influence a population\'s beliefs or actions, often by emotional appeal and selective information'),
         ('ethos', 'persuasion through the speaker\'s credibility and character'),
         ('pathos', 'persuasion through appeals to the audience\'s emotions'),
         ('logos', 'persuasion through reasoning and evidence'),
         ('anaphora', 'repetition of a word or phrase at the beginning of successive clauses'),
         ('kairos', 'the rhetorical sense of the right moment and context for a message')],
  facts=[('A speaker begins "As a nurse for twenty years ...". This mainly appeals to:', 'Ethos', ['Pathos', 'Logos', 'Kairos'], 'It establishes credibility.'),
         ('"I have a dream" repeated at the start of sentences in Martin Luther King Jr\'s 1963 speech is an example of:', 'Anaphora', ['Antithesis', 'Euphemism', 'Litotes'], 'Repetition at the start of successive sentences is anaphora.')],
  why=[('Explain why political speeches use repetition.', 'Speeches are heard once; repetition helps listeners remember key ideas, builds rhythm and emotion and creates a sense of unity.'),
       ('Explain why propaganda often relies on simple slogans and images.', 'Simple messages are easy to remember and spread, bypass critical thinking and appeal to emotions such as fear or pride.'),
       ('Explain how the context of a speech affects its rhetoric.', 'The occasion, audience and political moment (kairos) determine what appeals will work and what the speaker can say.')],
  contrast=[('persuasion', 'propaganda', 'Persuasion openly tries to convince through argument and appeal; propaganda systematically manipulates, often by distorting or omitting information, usually for a political or state agenda.'),
            ('ethos', 'pathos', 'Ethos persuades through the speaker\'s credibility; pathos persuades through the audience\'s emotions.')],
  misc=[('Emotional appeals in speeches are always manipulative.', 'Pathos can be legitimate when it reflects real stakes; it becomes manipulative when it replaces evidence or exploits fear.')],
  evaluate=[('The rhetoric of political speeches has changed little over time.', ['classical devices (tricolon, anaphora) persist', 'appeals to ethos, pathos, logos are timeless'], ['media changed delivery (radio, TV, social media)', 'shorter soundbites dominate now'], 'Core devices persist, but medium and audience have reshaped length, register and delivery.')],
  extended=[('Write a speech (about 300 words) to be delivered at your school\'s assembly persuading students to take part in a local environmental project. Use at least four rhetorical devices.', 'Indicative content: appropriate register for peers; clear purpose; devices such as anecdote, tricolon, rhetorical questions, imperative close; structure suited to oral delivery. Markband: persuasive, controlled, audience-aware.', 10, 'long')])
pq('ch06-st3', ('C2', 'C3'), (1, 5), {'speech', 'propaganda'}, 'dev', DEV_Q + ['Explain how "{quote}" works on the listener or viewer.'])
pq('ch06-st3', ('C3', 'C4'), (2, 5), {'speech', 'propaganda'}, 'ctx', CTX_Q)
pq_dev_mcq('ch06-st3', {'speech', 'propaganda'})
pq_para('ch06-st3', {'speech', 'propaganda'})

H('ch06-st4',
  terms=[('documentary photography', 'photography that records real people and events, often with a social or political purpose'),
         ('caption', 'text accompanying an image that identifies, explains or frames it'),
         ('iconic image', 'a photograph that comes to symbolise an event or era in collective memory'),
         ('photographic ethics', 'questions of consent, dignity and exploitation raised by photographing real people')],
  facts=[('Dorothea Lange\'s "Migrant Mother" (1936) was made for which organisation?', 'The US Farm Security Administration', ['The United Nations', 'The BBC', 'A fashion magazine'], 'Lange photographed rural poverty for the FSA during the Great Depression.'),
         ('Why can documentary photographs not be treated as purely objective?', 'Photographers choose framing, timing and captions', ['Cameras record everything', 'They are always staged', 'They are always in colour'], 'Choices shape the representation.')],
  why=[('Explain why the caption of a documentary photograph matters.', 'The caption anchors meaning, identifies (or fails to identify) subjects and frames how the viewer interprets the image.'),
       ('Explain why some documentary images raise ethical questions.', 'Subjects may not have consented, may be represented as symbols rather than individuals and may not benefit from the image\'s fame.'),
       ('Explain how a photograph can represent an era.', 'Through selection of a representative subject and symbolic composition, an image condenses complex social conditions into a single memorable scene.')],
  contrast=[('documentary photography', 'advertising photography', 'Documentary photography claims to record reality, often for social purposes; advertising photography is staged to sell, constructing idealised scenes.')],
  misc=[('A photograph shows exactly what happened.', 'Framing, cropping, timing and selection shape what is shown; photographs are constructed representations.')],
  evaluate=[('Documentary photographs are more trustworthy than written accounts of history.', ['they record real moments', 'images are immediate'], ['framing and cropping distort', 'images can be staged or manipulated'], 'They are valuable evidence but are equally constructed; they need contextual and critical reading.')],
  extended=[('Write the caption and a 200-word exhibition label for a documentary photograph of your own community today, explaining what it represents about your time and place.', 'Indicative content: clear description; explanation of framing choices; contextual significance; ethical awareness.', 8, 'long')])
pq('ch06-st4', ('C3', 'C4'), (2, 5), {'photo'}, 'visual', VIS_Q + ['How does the photograph represent its subject? Consider framing and caption.'])
pq('ch06-st4', ('C2', 'C3'), (1, 5), {'photo'}, 'dev', ['Explain the effect of the {device} in this photograph.',
                                                       'How does "{quote}" shape the viewer\'s response?'])
pq('ch06-st4', ('C3', 'C4'), (2, 5), {'photo'}, 'ctx', CTX_Q)
pq('ch06-st4', 'C4', (3, 5), {'photo'}, 'read', READ_Q, typ='long', crit=MARKBAND)


# =============================================================================================
# ch07 Time and space: literary work in translation
# =============================================================================================
TRANS = {'trans'}
H('ch07-st1',
  terms=[('work in translation', 'a literary work originally written in another language, studied in English translation'),
         ('domestication', 'a translation strategy that adapts the text to the target culture so it reads smoothly and familiarly'),
         ('foreignisation', 'a translation strategy that keeps elements of the source culture and language, making the text feel foreign'),
         ('paratext', 'material around a text – titles, prefaces, translator\'s notes, glossaries – that frames how it is read'),
         ('source text', 'the original text from which a translation is made'),
         ('target language', 'the language into which a text is translated')],
  facts=[('Keeping Japanese farewell phrases in an English translation and explaining them in a note is an example of:', 'Foreignisation', ['Domestication', 'Back-translation', 'Paraphrase'], 'The translator preserves the source culture\'s language.'),
         ('A translator\'s preface is an example of:', 'Paratext', ['Subtext', 'Metatheatre', 'Intertext'], 'Material framing the text is paratext.'),
         ('How many works in translation must HL students study as a minimum in Language A: Language and Literature?', 'Two', ['One', 'Three', 'None'], 'SL students study at least one work in translation; HL students at least two.')],
  why=[('Explain why reading a work in translation requires awareness of the translator.', 'The English text is the product of a translator\'s choices about meaning, sound and culture, so some features analysed may be the translator\'s rather than the author\'s.'),
       ('Explain why culture-specific words are hard to translate.', 'They carry associations, customs or values that have no equivalent in the target culture, so any rendering gains or loses meaning.'),
       ('Explain why the course requires works in translation.', 'They expose students to perspectives and cultures beyond their own and show how meaning travels and changes across languages.')],
  contrast=[('domestication', 'foreignisation', 'Domestication makes a translation read as if originally written in the target language (replacing culture-specific items); foreignisation keeps source-culture elements visible, reminding the reader of the text\'s origin.')],
  misc=[('A good translation is a word-for-word copy of the original.', 'Literal translation often loses idiom, tone and sound; good translators balance fidelity to meaning with readability and style.'),
        ('When analysing a translated work, students should ignore the translation and write as if reading the original.', 'Students should analyse the translated text but show awareness that some choices are the translator\'s and that meaning may shift.')],
  evaluate=[('Something essential is always lost in translation.', ['puns, sound and cultural associations rarely survive', 'readers miss context'], ['translation can also gain and illuminate', 'great works remain powerful in translation'], 'Some features are inevitably lost, but translation also creates new meaning; "loss" is only part of the story.')],
  extended=[('Discuss how your reading of a work in translation you have studied was shaped by its being in translation.', 'Indicative content: specific culture-bound items, notes or choices; their effect on interpretation; reflection on cultural distance.', 8, 'long')])
pq('ch07-st1', ('C2', 'C3', 'C4'), (1, 5), TRANS, 'trans', ['Explain one choice made by the translator and its effect on the reader.',
                                                           'Analyse how the translation handles the challenge of carrying meaning across languages.',
                                                           'Evaluate the translator\'s choices in this extract.'], crit=CRIT_B)
pq('ch07-st1', ('C3', 'C4'), (2, 5), TRANS, 'culture', ['What does this extract reveal about the culture of the source text?',
                                                       'Explain how cultural context shapes the meaning of this extract.'], crit=CRIT_A)

H('ch07-st2',
  terms=[('patriarchy', 'a social system in which men hold primary power and authority in family and society'),
         ('class', 'a social hierarchy based on economic position, occupation and status'),
         ('agency', 'a character\'s capacity to act independently and make choices'),
         ('marginalisation', 'the treatment of a person or group as insignificant or peripheral'),
         ('subaltern', 'a person or group excluded from the dominant structures of power and voice')],
  facts=[('An employer counts wages aloud "as if Rosa might not know her numbers". This mainly shows:', 'Condescension that reinforces class power', ['Generosity', 'A neutral transaction', 'Rosa\'s lack of education'], 'The irony is that Rosa taught the children to read.'),
         ('A female character who quietly resists a custom by standing in a doorway shows:', 'Limited agency within a patriarchal structure', ['Complete freedom', 'No awareness of power', 'Comic relief'], 'Her resistance is symbolic and constrained.')],
  why=[('Explain how small domestic details can reveal power relations in a novel.', 'Customs such as who eats first, who serves or who controls money encode hierarchies, so they show power operating in everyday life.'),
       ('Explain why silence can be a form of resistance for characters.', 'Refusing to speak or comply can withhold consent and preserve dignity when open resistance is impossible.'),
       ('Explain why gender and class often intersect in literary works.', 'Characters experience power through several identities at once; a working-class woman may face constraints neither a working-class man nor a wealthy woman experiences.')],
  contrast=[('power', 'agency', 'Power is the capacity to control others or structures; agency is an individual\'s capacity to act for themselves. A character may lack power but still exercise agency.')],
  misc=[('Characters with less power in a work are always passive victims.', 'Writers often show the less powerful resisting through silence, irony, humour or small acts of control.')],
  evaluate=[('Literature in translation gives readers authentic insight into the power structures of other cultures.', ['it presents insiders\' perspectives', 'it can challenge stereotypes'], ['translation and selection mediate it', 'one work cannot represent a culture'], 'It offers valuable insight but should not be read as representing a whole culture.')],
  extended=[('Analyse how a work in translation you have studied represents the relationship between gender and power.', 'Indicative content: specific characters, scenes and choices; context; how representation is constructed; evaluation.', 8, 'long')])
pq('ch07-st2', ('C2', 'C3', 'C4'), (1, 5), TRANS | PROSE, 'power', ['How does the writer present power in this extract?',
                                                                    'Analyse how the extract represents gender or class relationships.',
                                                                    'Explain how a small detail in this extract reveals a power relationship.',
                                                                    'Discuss how the extract presents resistance to power.'], crit=CRIT_B)
pq('ch07-st2', 'C3', (2, 4), TRANS, 'char', ['How are the characters in this extract positioned in relation to power?',
                                            'Explain how characterisation reveals social hierarchy in this extract.'])

H('ch07-st3',
  terms=[('cultural values', 'the beliefs and priorities that a community holds as important'),
         ('ritual', 'a repeated, often ceremonial action that expresses a community\'s values'),
         ('cultural conflict', 'tension arising when different values or traditions meet'),
         ('ethnocentrism', 'judging another culture by the standards of one\'s own')],
  facts=[('A reader who calls a custom in a translated novel "backward" without understanding its context is showing:', 'Ethnocentrism', ['Foreignisation', 'Empathy', 'Close reading'], 'Judging by one\'s own cultural standards is ethnocentric.'),
         ('Fixed everyday phrases said on leaving and returning home show:', 'How ordinary language carries cultural values', ['That language is universal', 'That translation is easy', 'Nothing about culture'], 'Everyday rituals encode values.')],
  why=[('Explain why literary works often show cultural values through conflict.', 'Values become visible when challenged – by outsiders, change or a character\'s rebellion – so conflict dramatises what a culture holds dear.'),
       ('Explain why readers should avoid treating one work as representative of a whole culture.', 'A work presents one writer\'s perspective, often critical, within a diverse culture; generalising creates stereotypes.'),
       ('Explain how rituals in a literary work can reveal character.', 'How characters perform, adapt or resist rituals shows their relationship to their community\'s values.')],
  contrast=[('cultural relativism', 'ethnocentrism', 'Cultural relativism seeks to understand practices within their own cultural context; ethnocentrism judges them by one\'s own culture\'s standards.')],
  misc=[('Works in translation show "exotic" cultures that are completely unlike our own.', 'Exoticising ignores shared human concerns; works in translation often reveal both difference and common experience.')],
  evaluate=[('A reader can never fully understand the cultural values of a work from another culture.', ['insiders\' knowledge and language cannot be fully shared', 'translation mediates'], ['empathy and research build understanding', 'human concerns are shared'], 'Full understanding may be impossible, but meaningful understanding is achievable through careful, contextual reading.')],
  extended=[('Discuss how a work in translation you have studied presents a conflict between cultural values.', 'Indicative content: identify values in conflict; characters and episodes; authorial choices; evaluation of the work\'s stance.', 8, 'long')])
pq('ch07-st3', ('C2', 'C3', 'C4'), (1, 5), TRANS, 'culture', ['What cultural values are suggested in this extract, and how?',
                                                              'Analyse how the extract presents a cultural practice or value.',
                                                              'Explain how this extract might challenge a reader from a different culture.',
                                                              'Evaluate how the extract avoids or reinforces stereotypes about a culture.'], crit=CRIT_A)
pq('ch07-st3', 'C3', (2, 4), TRANS, 'read', READ_Q, crit=CRIT_OPEN)

H('ch07-st4',
  terms=[('literal translation', 'a translation that stays close to the words and structure of the source text'),
         ('free translation', 'a translation that prioritises sense, tone or effect over word-for-word accuracy'),
         ('fidelity', 'faithfulness of a translation to the source text\'s meaning, form or effect'),
         ('equivalence', 'the attempt to produce the same meaning or effect in the target language as in the source')],
  facts=[('Translation A of Verlaine keeps "It weeps"; Translation B writes "My heart is raining". B\'s choice is an example of:', 'Free translation', ['Literal translation', 'Back-translation', 'Transliteration'], 'B gives up the impersonal construction to recreate tone and rhyme.'),
         ('Rendering Kafka\'s "Ungeziefer" as "insect" rather than "vermin" mainly changes:', 'How specific and visual the creature is, and its sense of uncleanness', ['Gregor\'s name', 'The setting', 'The narrative voice'], '"Vermin" keeps vagueness and disgust; "insect" is specific.')],
  why=[('Explain why comparing translations of the same passage is useful.', 'Differences reveal the choices translators must make and which features of the original (sound, ambiguity, culture) are hardest to carry over.'),
       ('Explain why poetry is especially difficult to translate.', 'Poetry depends on sound, rhythm, form and wordplay tied to a specific language, so meaning and music often cannot both be preserved.'),
       ('Explain why there can be no single "correct" translation.', 'Each translation prioritises different values (accuracy, readability, music) for different audiences, so several can be valid.')],
  contrast=[('literal translation', 'free translation', 'Literal translation keeps close to source words and structure, risking awkwardness; free translation recreates sense and effect, risking distortion.')],
  misc=[('The most literal translation is always the most faithful.', 'Fidelity can be to meaning, tone or effect; a literal version may be faithful to words but unfaithful to music or idiom.')],
  apply=[('A source poem ends with a pun that has no English equivalent. Suggest two strategies a translator could use and evaluate one.', 'Strategies: compensate with a different English pun elsewhere; keep the literal meaning and add a note; invent an equivalent pun. Evaluation e.g. compensation keeps playful tone but changes content.', 4),
         ('Translate the French phrase "Il pleut des cordes" (literally "It is raining ropes") in two ways – literally and idiomatically – and explain the difference in effect.', 'Literal: "It is raining ropes" – strange, foreign, vivid image; idiomatic: "It\'s pouring" or "raining cats and dogs" – natural but loses the original image.', 3)],
  evaluate=[('A translator should always aim to be invisible.', ['smooth translations let readers focus on the work', 'readers want natural English'], ['invisibility can erase culture', 'notes show honest mediation'], 'Invisibility suits some texts, but visible translation can be more honest about cultural difference.')],
  extended=[('Compare two translations of a passage from a work in translation you have studied and evaluate which better conveys the original\'s effect.', 'Indicative content: specific differences in diction, syntax, sound; effects on meaning; reasoned judgement.', 8, 'long')])
pq('ch07-st4', ('C2', 'C3', 'C4'), (1, 5), {'trans'}, 'trans', ['Compare the choices made by the translations in this extract and their effects.',
                                                               'Which translation do you find more effective, and why? Refer to specific words.',
                                                               'Explain what is gained and what is lost in the translation(s) shown.',
                                                               'Evaluate how far the translations preserve the effect of the original.'], crit=CRIT_B)
pq_para('ch07-st4', {'trans'})


# =============================================================================================
# ch08 Time and space: drama
# =============================================================================================
DRAMA = {'drama'}
H('ch08-st1',
  terms=[('stage directions', 'instructions in a play script describing setting, movement, tone and action'),
         ('soliloquy', 'a speech in which a character alone on stage reveals their thoughts to the audience'),
         ('aside', 'a remark made by a character to the audience, unheard by other characters on stage'),
         ('dramatic irony', 'a situation in which the audience knows something that a character does not'),
         ('stichomythia', 'rapid dialogue in alternating short lines, often expressing conflict'),
         ('subtext', 'the unspoken meaning beneath what characters say')],
  facts=[('A character alone on stage speaking his thoughts aloud is delivering a:', 'Soliloquy', ['Monologue to other characters', 'Aside', 'Chorus'], 'Soliloquies are spoken alone.'),
         ('In a scene where the audience has seen a thief hide a necklace in a plant, the detective\'s search creates:', 'Dramatic irony', ['Pathetic fallacy', 'Stream of consciousness', 'Bathos'], 'The audience knows more than the character.')],
  why=[('Explain why stage directions are important when studying a play as a literary work.', 'They show how the playwright imagines the play in performance – movement, silence, props – which reveal subtext and character beyond dialogue.'),
       ('Explain how dramatic irony engages an audience.', 'Knowing more than the characters creates suspense, tension or comedy as the audience anticipates consequences the characters cannot see.'),
       ('Explain why a soliloquy changes the audience\'s relationship with a character.', 'Direct access to private thoughts creates intimacy and complicity, even with a villain.')],
  contrast=[('a soliloquy', 'an aside', 'A soliloquy is a longer speech by a character alone on stage revealing their inner thoughts; an aside is a brief remark to the audience while other characters are present but do not hear.'),
            ('dialogue', 'subtext', 'Dialogue is what characters say; subtext is what they mean or feel but do not say.')],
  misc=[('Plays should be analysed only through what characters say.', 'Drama is written for performance; stage directions, silences, props and staging are central to meaning.')],
  evaluate=[('Dramatic irony is the most powerful convention available to a playwright.', ['it creates suspense, comedy and tragedy', 'it actively involves the audience'], ['soliloquy and staging are equally significant', 'some plays rely on surprise instead'], 'It is among the most powerful, but its power depends on how it combines with other conventions.')],
  extended=[('Write a short scene (about 250 words) in which two characters avoid talking about something important. Use stage directions and subtext, then explain your choices.', 'Indicative content: dialogue with clear subtext; purposeful stage directions; commentary on the conventions used.', 8, 'long')])
pq('ch08-st1', ('C2', 'C3', 'C4'), (1, 5), DRAMA, 'conv', ['Identify a dramatic convention used in this extract and explain its effect.',
                                                          'Analyse how the playwright uses dramatic conventions in this extract.',
                                                          'How do the stage directions or dialogue create meaning in this extract?',
                                                          'Evaluate how dramatic conventions shape the audience\'s response to this scene.'])
pq_dev_mcq('ch08-st1', DRAMA)

H('ch08-st2',
  terms=[('staging', 'the way a play is presented in performance, including set, lighting, sound, blocking and costume'),
         ('blocking', 'the planned movement and positioning of actors on stage'),
         ('proxemics', 'the use of space and distance between characters on stage to convey relationships'),
         ('mise-en-scène', 'everything placed on stage – set, props, lighting, costume and actors\' positions'),
         ('fourth wall', 'the imaginary boundary between the stage and the audience in realist theatre')],
  facts=[('A character turning his back while another speaks is an example of:', 'Proxemics and blocking that suggest emotional distance', ['Stichomythia', 'An aside', 'Pathetic fallacy'], 'Positioning conveys relationships.'),
         ('When a character speaks directly to the audience, they:', 'Break the fourth wall', ['Use a set change', 'Use blocking', 'Use a flashback'], 'Direct address breaks the realist boundary.')],
  why=[('Explain why the same play can mean different things in different productions.', 'Directors make choices about staging, casting, setting and emphasis that interpret the script, so meaning changes with each production and audience.'),
       ('Explain how lighting can create meaning on stage.', 'Lighting focuses attention, creates atmosphere and can symbolise isolation, warmth or danger.'),
       ('Explain why props can carry symbolic meaning in drama.', 'Objects handled on stage become focal points of conflict or emotion, like a letter that must be hidden.')],
  contrast=[('the play as text', 'the play in performance', 'The text is the script read on the page, including stage directions; the performance is a specific realisation by a director, actors and designers for an audience, which interprets and changes the text.')],
  misc=[('Stage directions are fixed and every production must follow them exactly.', 'Directors often reinterpret or ignore stage directions; the script is a starting point for performance.')],
  evaluate=[('A play can only be fully understood in performance.', ['drama is written for an audience', 'performance reveals subtext and timing'], ['close reading reveals language and structure', 'each production is one interpretation'], 'Performance completes a play, but the text remains a rich object of analysis in itself.')],
  extended=[('As a director, explain how you would stage a key scene from a play you have studied to emphasise a particular interpretation.', 'Indicative content: specific choices of set, lighting, blocking and sound; justification linked to interpretation and audience.', 8, 'long')])
pq('ch08-st2', ('C2', 'C3', 'C4'), (1, 5), DRAMA, 'staging', ['How might this extract be staged to bring out its meaning?',
                                                             'Analyse how setting, props or lighting contribute to the scene.',
                                                             'As a director, explain one staging choice you would make for this extract and its effect.',
                                                             'Evaluate how important staging is to the meaning of this extract.'])

H('ch08-st3',
  terms=[('context of production', 'the circumstances in which a play was written and first performed'),
         ('context of reception', 'the circumstances in which a play is watched or read by later audiences'),
         ('Jacobean', 'relating to the reign of James I of England (1603–1625), when plays such as Macbeth were first performed'),
         ('naturalism', 'a theatrical movement aiming to present everyday life realistically, associated with Ibsen and Chekhov'),
         ('censorship', 'official control over what may be performed or published')],
  facts=[('Macbeth was first performed during the reign of which monarch?', 'James I', ['Elizabeth I', 'Victoria', 'Charles II'], 'Macbeth (c. 1606) is a Jacobean play.'),
         ('Henrik Ibsen\'s A Doll\'s House (1879) caused controversy mainly because:', 'Nora leaves her husband and children at the end', ['It was written in verse', 'It had no female characters', 'It was set in the future'], 'The ending challenged contemporary ideas of marriage.')],
  why=[('Explain why knowing a play\'s first audience helps interpretation.', 'The first audience\'s beliefs explain what would have shocked, comforted or amused them, revealing the play\'s original force.'),
       ('Explain why modern productions often reset older plays in new periods.', 'Resetting connects the play\'s concerns to contemporary audiences and can reveal new meanings.'),
       ('Explain why the reception of a play can change over time.', 'Changing values (about gender, race, power) alter how audiences respond to characters and endings.')],
  contrast=[('context of production', 'context of reception', 'Context of production is when and where a play was first written and staged; context of reception is when and where later audiences encounter it.')],
  misc=[('The meaning of a play is fixed by the time in which it was written.', 'Each new audience and production reinterprets a play; meaning is shaped by both production and reception contexts.')],
  evaluate=[('Modern audiences cannot experience a Shakespeare play as it was meant to be experienced.', ['language, beliefs and theatre conditions differ', 'original staging is lost'], ['core human conflicts remain', 'new productions create new valid experiences'], 'The original experience cannot be recovered, but this does not lessen the play\'s power or validity of new responses.')],
  extended=[('Discuss how a modern audience\'s response to a play you have studied might differ from that of its first audience.', 'Indicative content: specific contexts; specific scenes; evaluation of changed responses.', 8, 'long')])
pq('ch08-st3', ('C2', 'C3', 'C4'), (1, 5), DRAMA, 'ctx', CTX_Q + ['How might audiences in different periods respond to this extract?'], crit=CRIT_A)

H('ch08-st4',
  terms=[('tragedy', 'a drama in which a protagonist\'s downfall results from a flaw, error or circumstance, evoking pity and fear'),
         ('hamartia', 'the tragic hero\'s error or flaw that leads to downfall'),
         ('catharsis', 'the release of pity and fear felt by an audience at the end of a tragedy (Aristotle)'),
         ('peripeteia', 'a sudden reversal of fortune in a tragedy'),
         ('anagnorisis', 'the moment of recognition or discovery by the tragic hero'),
         ('climax', 'the point of greatest tension in a play\'s structure')],
  facts=[('Who defined tragedy in terms of pity, fear and catharsis?', 'Aristotle', ['Plato', 'Shakespeare', 'Ibsen'], 'Aristotle\'s Poetics.'),
         ('Macbeth\'s "Tomorrow, and tomorrow" speech after his wife\'s death is often read as a moment of:', 'Recognition of the futility of his ambition', ['Comic relief', 'Peripeteia caused by the witches', 'A soliloquy of triumph'], 'It shows despair and insight before the catastrophe.')],
  why=[('Explain why tragedies often reveal the outcome early through prophecy or foreshadowing.', 'Inevitability shifts tension to how the downfall happens and intensifies pity as the audience watches the hero move towards it.'),
       ('Explain how conflict drives the structure of a play.', 'Rising conflict creates tension through the acts, building to a climax and resolution; each scene usually advances or complicates conflict.'),
       ('Explain why internal conflict is important in tragedy.', 'A hero torn between desires engages the audience\'s sympathy and makes the downfall feel chosen and human.')],
  contrast=[('internal conflict', 'external conflict', 'Internal conflict takes place within a character (ambition versus conscience); external conflict is between characters or between a character and society or fate.'),
            ('peripeteia', 'anagnorisis', 'Peripeteia is a reversal of fortune; anagnorisis is the hero\'s moment of recognition, often coinciding with or following the reversal.')],
  apply=[('In Death of a Salesman, Willy Loman is an ageing travelling salesman rather than a king. Explain how Miller still creates a tragic structure around him.', 'Willy has a flaw (his belief in being "well liked" and in the American Dream), suffers reversals (losing his job), experiences partial recognition, and dies; Miller argued for the "tragedy of the common man".', 4),
         ('Identify the climax of a play you have studied and explain how earlier scenes build towards it.', 'Answers will vary: the climax should be the point of highest tension; credit specific earlier scenes that create conflict, foreshadowing or rising stakes.', 4),
         ('A director wants to cut a play\'s opening scene of exposition. Explain what the audience might lose.', 'Exposition introduces characters, relationships and the initial conflict; cutting it could reduce dramatic irony, understanding of motives and the sense of rising action.', 3),
         ('Explain how a comic subplot can intensify a tragedy.', 'Contrast heightens tension and pathos (e.g. the Porter scene in Macbeth after Duncan\'s murder), offers relief before catastrophe and may comment ironically on the main plot.', 3)],
  misc=[('A tragic hero must be a king or noble.', 'Classical tragedy featured noble figures, but modern tragedy (e.g. Miller\'s Death of a Salesman) centres ordinary people.')],
  evaluate=[('Modern plays can still be tragedies in Aristotle\'s sense.', ['ordinary protagonists can have hamartia and evoke pity', 'Miller argued for the "tragedy of the common man"'], ['social forces rather than flaws often cause downfall', 'catharsis may be replaced by discomfort'], 'Modern tragedy adapts Aristotle\'s ideas rather than following them; the emotional core remains.')],
  extended=[('Analyse how the structure of a play you have studied builds and resolves conflict.', 'Indicative content: exposition, rising action, climax, resolution; key scenes; effect on audience; evaluation.', 8, 'long')])
pq('ch08-st4', ('C2', 'C3', 'C4'), (1, 5), DRAMA, 'conflict', ['What conflict is presented in this extract, and how?',
                                                              'Analyse how the playwright develops conflict in this extract.',
                                                              'How does this extract build tension between characters?',
                                                              'Evaluate how the conflict in this extract might drive the rest of the play.'])
pq('ch08-st4', 'C3', (2, 4), DRAMA, 'char', ['How are the characters in this scene presented?', 'Analyse the characterisation in this dramatic extract.'])


# =============================================================================================
# ch09 Time and space: language, culture and identity
# =============================================================================================
LANGK = {'letter', 'blog', 'social', 'speech', 'ad', 'meme'}
H('ch09-st1',
  terms=[('dialect', 'a variety of a language with distinctive vocabulary, grammar and pronunciation, associated with a region or social group'),
         ('accent', 'a distinctive way of pronouncing a language, associated with a region, class or community'),
         ('World Englishes', 'the many varieties of English used around the world, such as Indian, Nigerian, Singaporean and Jamaican English'),
         ('Standard English', 'the variety of English treated as the norm in education, publishing and formal contexts'),
         ('linguistic prejudice', 'negative judgement of people based on the way they speak'),
         ('covert prestige', 'the value speakers place on non-standard varieties as markers of group belonging')],
  facts=[('Which is an example of a World English variety?', 'Singapore Colloquial English (Singlish)', ['Received Pronunciation only', 'Latin', 'Esperanto'], 'Singlish is a local variety of English.'),
         ('A columnist calls a regional accent "unprofessional". This illustrates:', 'Linguistic prejudice', ['Code-switching', 'Covert prestige', 'Standardisation'], 'Judging speakers by accent is linguistic prejudice.')],
  why=[('Explain why accent and dialect are markers of identity.', 'They signal where people come from and which communities they belong to, so speaking a variety expresses regional, class or ethnic identity.'),
       ('Explain why some speakers maintain a non-standard dialect even when they can use Standard English.', 'Covert prestige: the dialect expresses solidarity and belonging, which may matter more than the status of the standard variety.'),
       ('Explain why writers might include dialect in literary or non-literary texts.', 'Dialect creates authentic voice, marks identity and can challenge the dominance of standard varieties.')],
  contrast=[('accent', 'dialect', 'Accent refers only to pronunciation; dialect includes vocabulary and grammar as well as pronunciation.'),
            ('a standard variety', 'a non-standard variety', 'A standard variety is codified and used in formal institutions; a non-standard variety is not, but is equally rule-governed and expressive.')],
  misc=[('Dialects are incorrect versions of English.', 'Dialects are rule-governed systems; "standard" status is social, not linguistic superiority.'),
        ('Everyone except people with regional accents speaks without an accent.', 'Everyone speaks with an accent; some accents are simply treated as neutral because of social prestige.')],
  evaluate=[('Schools should teach only Standard English.', ['it is needed for formal contexts and exams', 'it enables wider communication'], ['it can stigmatise students\' home varieties', 'multilingual and multidialectal skills are valuable'], 'Standard English should be taught as a tool alongside respect for students\' home varieties.')],
  extended=[('Write a letter to a newspaper (about 300 words) responding to a claim that local dialects are dying and should be allowed to disappear.', 'Indicative content: clear stance; letter conventions; examples of dialect and identity; counter-argument; appropriate register.', 10, 'long')])
pq('ch09-st1', ('C2', 'C3', 'C4'), (1, 5), LANGK, 'lang', ['How does the writer\'s use of language reflect identity in this text?',
                                                          'Analyse how dialect, accent or a variety of English is presented in this text.',
                                                          'Explain how language choices in this text signal belonging to a community.',
                                                          'Evaluate how the text challenges or reinforces attitudes to non-standard language.'])

H('ch09-st2',
  terms=[('code-switching', 'moving between two or more languages or varieties within a conversation or text'),
         ('multilingualism', 'the use of more than one language by an individual or community'),
         ('linguistic capital', 'the social and economic value attached to speaking particular languages or varieties'),
         ('language of power', 'a language or variety associated with authority, such as a colonial language or a dominant national language'),
         ('diglossia', 'a situation in which two varieties of a language are used for different social functions')],
  facts=[('A mayor greets an audience "bienvenidos, karibu, welcome". This is an example of:', 'Code-switching', ['Diglossia', 'Dialect levelling', 'Jargon'], 'Several languages are used in one utterance.'),
         ('Which statement about code-switching is most accurate?', 'It is a skilled, purposeful use of linguistic resources', ['It shows a speaker does not know either language well', 'It only happens among children', 'It is always unconscious'], 'Code-switching is often strategic.')],
  why=[('Explain why speakers code-switch.', 'To signal identity or solidarity, to fit context and audience, to express ideas better in one language, or to include or exclude listeners.'),
       ('Explain how language can be connected to power.', 'Languages and varieties used by institutions, education and the elite carry linguistic capital, so speakers of other languages may be disadvantaged.'),
       ('Explain why writers from multilingual backgrounds may mix languages in their texts.', 'Mixing reflects lived experience, asserts identity and resists the idea that one language must dominate.')],
  contrast=[('code-switching', 'borrowing', 'Code-switching alternates between languages in discourse; borrowing adopts single words from one language into another as part of its vocabulary (e.g. "café").')],
  misc=[('Multilingual people code-switch because they cannot find the words in one language.', 'Code-switching is usually purposeful: it signals identity, relationships and context.')],
  evaluate=[('English\'s global dominance threatens linguistic diversity.', ['minority languages are lost as English spreads', 'English carries economic capital'], ['English is also localised into new varieties', 'multilingualism is growing'], 'English does pressure smaller languages, but its local varieties show that dominance and diversity coexist.')],
  extended=[('Analyse how two texts you have studied use more than one language or variety, and to what effect.', 'Indicative content: identification of code-switching; purposes; effects on audience; context of power.', 8, 'long')])
pq('ch09-st2', ('C2', 'C3', 'C4'), (1, 5), LANGK | {'trans'}, 'lang', ['Explain why the writer uses more than one language or variety in this text.',
                                                                      'How does language mixing in this text relate to identity or power?',
                                                                      'Analyse the effect of the writer\'s language choices on the intended audience.',
                                                                      'Evaluate what the text suggests about the relationship between language and belonging.'])
pq('ch09-st2', 'C3', (2, 4), {'speech', 'ad', 'social'}, 'dev', DEV_Q)

H('ch09-st3',
  terms=[('gendered language', 'language that reflects or reinforces assumptions about gender, such as "chairman" or "man-made"'),
         ('stereotype', 'an oversimplified, fixed image of a group'),
         ('male gaze', 'the representation of women in visual texts from a heterosexual male viewpoint, as objects to be looked at (Laura Mulvey)'),
         ('gender-neutral language', 'language that avoids specifying gender, such as "firefighter" or singular "they"'),
         ('marked term', 'a word that signals deviation from an assumed norm, such as "female doctor"')],
  facts=[('"Built for the man who carries everyone" in a car advert shows:', 'A gendered representation of the provider role', ['Gender-neutral language', 'The male gaze in film', 'Code-switching'], 'The protector role is assigned to a man.'),
         ('Which term is gender-neutral?', 'Firefighter', ['Fireman', 'Chairman', 'Manpower'], '"Firefighter" does not specify gender.')],
  why=[('Explain how everyday texts can reinforce gender stereotypes.', 'Repeated patterns – who is shown as active, who serves, which words describe each gender – normalise assumptions until they seem natural.'),
       ('Explain why "marked" terms such as "female engineer" matter.', 'They imply that the unmarked form ("engineer") is male by default, reinforcing the idea that women in the role are unusual.'),
       ('Explain why analysing absence is important in gender representation.', 'Who is missing (e.g. an absent mother in a family advert) can reveal assumptions as clearly as who is shown.')],
  contrast=[('sex', 'gender', 'Sex usually refers to biological characteristics; gender refers to socially constructed roles, behaviours and identities, which texts represent and shape.')],
  apply=[('A job advertisement asks for "a strong chairman to lead his team". Rewrite it in gender-neutral language and explain one effect of the change.', 'Example: "a strong chair to lead their team"; the change avoids implying the role is for men and widens the pool of people who see themselves as candidates.', 3),
         ('A toy catalogue shows boys with building sets under "Build!" and girls with dolls under "Care!". Analyse what this layout suggests about gender roles.', 'It assigns active, creative construction to boys and nurturing, domestic roles to girls, presenting socially constructed roles as natural from childhood.', 4),
         ('A newspaper describes a female minister\'s outfit before her policy and a male minister\'s policy only. Explain what this reveals about gender representation.', 'It reflects a double standard that evaluates women on appearance and men on achievement, trivialising women in public life.', 3),
         ('Explain how the phrase "female surgeon" can reinforce assumptions about gender.', 'It is a marked term implying that the unmarked "surgeon" is male by default, so women in the role appear exceptional.', 2)],
  misc=[('Gendered language no longer matters because everyone knows "man" includes women.', 'Research and experience suggest generic masculine terms lead people to picture men, so language choices still shape perception.')],
  evaluate=[('Advertising today challenges gender stereotypes more than it reinforces them.', ['many brands promote diversity', 'regulators have banned harmful stereotypes in some countries'], ['many adverts still use traditional roles', '"femvertising" can commodify empowerment'], 'Advertising has shifted but often repackages stereotypes; the change is partial and commercially motivated.')],
  extended=[('Write an opinion column (about 300 words) for a student magazine on whether gender-neutral language should be required in school documents.', 'Indicative content: stance; examples; counter-argument; conventions of an opinion column; register suited to students.', 10, 'long')])
pq('ch09-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'gender', ['How does the text represent gender?',
                                                          'Analyse how language or images in the text construct gender roles.',
                                                          'Explain what assumptions about gender this text makes.',
                                                          'Evaluate whether the text challenges or reinforces gender stereotypes.'])


# =============================================================================================
# ch10 Time and space: social media and digital communication
# =============================================================================================
H('ch10-st1',
  terms=[('online persona', 'the identity a user constructs and performs on social media through posts, images and language'),
         ('meme', 'a unit of culture – often an image with text – that is copied and adapted as it spreads online'),
         ('influencer', 'a social media user with a large following who shapes opinions and often promotes products'),
         ('parasocial relationship', 'a one-sided relationship in which followers feel they know a media figure who does not know them'),
         ('virality', 'the rapid spread of content online through sharing')],
  facts=[('A fitness post moving from a personal story to "Link in bio for my plan" shows:', 'An online persona used for commercial purposes', ['Objective reporting', 'A news standfirst', 'Code-switching'], 'The persona promotes a product.'),
         ('A meme with the template "ME IN SEPTEMBER / ME THE NIGHT BEFORE" relies on:', 'A recognisable format that viewers adapt and share', ['Copyright protection', 'Long-form argument', 'Statistical evidence'], 'Templates make memes easy to decode and remix.')],
  why=[('Explain why an online persona is a constructed text.', 'Users select, edit and frame what they post – images, captions, hashtags – to present a chosen identity to an audience.'),
       ('Explain why memes can build community.', 'Shared templates and in-group references signal belonging to people who understand them, creating solidarity through humour.'),
       ('Explain how likes and shares function as persuasive features.', 'They act as social proof, signalling popularity and approval, which encourages others to trust or engage with content.')],
  contrast=[('a persona', 'a person', 'A persona is the curated identity presented in texts; the person is the real individual, whose life is more complex than the persona.')],
  misc=[('Social media posts are spontaneous and unplanned, so they cannot be analysed like other texts.', 'Many posts are carefully crafted, and even spontaneous ones use conventions and choices that can be analysed.')],
  evaluate=[('Social media allows people to express their true identities.', ['marginalised groups find voice and community', 'users can experiment with identity'], ['personas are curated for approval', 'algorithms reward performance'], 'It enables expression but encourages performance; the "true" self online is always partly constructed.')],
  extended=[('Write two short social media posts about the same event – one by an influencer promoting a brand and one by an ordinary student – and explain how each constructs a persona.', 'Indicative content: platform conventions; contrasting personas; commentary on hashtags, register, images.', 8, 'long')])
pq('ch10-st1', ('C2', 'C3', 'C4'), (1, 5), {'social', 'meme', 'blog'}, 'persona', ['How does the writer construct an online persona in this text?',
                                                                                 'Analyse how the text presents the writer\'s identity to an online audience.',
                                                                                 'Explain what kind of identity the poster is performing, and how.',
                                                                                 'Evaluate the relationship between authenticity and performance in this post.'])
pq('ch10-st1', 'C3', (1, 4), {'social', 'meme'}, 'dev', DEV_Q)

H('ch10-st2',
  terms=[('neologism', 'a newly coined word or expression, such as "doomscrolling"'),
         ('emoji', 'a small digital image used to express emotion or ideas in electronic communication'),
         ('netspeak', 'the informal language of online communication, including abbreviations, acronyms and emoji'),
         ('language change', 'the ongoing change in vocabulary, grammar, spelling and usage over time'),
         ('paralanguage', 'features that accompany language to convey meaning, such as tone of voice – online, emoji and punctuation play this role')],
  facts=[('"Doomscrolling" is an example of:', 'A neologism', ['An archaism', 'A euphemism', 'A dialect form'], 'It is a recent coinage (doom + scrolling).'),
         ('Using "!!" and an emoji to show enthusiasm online is an example of:', 'Digital paralanguage', ['Standardisation', 'Code-switching', 'Prescriptivism'], 'Punctuation and emoji replace tone of voice.')],
  why=[('Explain why digital communication speeds up language change.', 'Huge numbers of users interact rapidly across the world, so new words and forms spread and become normal far faster than through print.'),
       ('Explain why emoji are not simply "lazy" language.', 'They perform functions of tone, gesture and facial expression missing from text, helping to prevent misunderstanding.'),
       ('Explain why prescriptivists and descriptivists respond differently to online language.', 'Prescriptivists judge it against rules and see decline; descriptivists observe it as natural, creative adaptation to a new medium.')],
  contrast=[('prescriptivism', 'descriptivism', 'Prescriptivism prescribes how language should be used, often seeing change as decline; descriptivism describes how language is actually used without judging it.')],
  misc=[('Texting is destroying young people\'s ability to write properly.', 'Research suggests many young people switch registers skilfully; netspeak is an additional register, not a replacement for formal writing.')],
  evaluate=[('Digital communication is making English simpler.', ['abbreviations and short messages dominate', 'punctuation is reduced'], ['new conventions (emoji, ellipsis) add nuance', 'users manage many registers'], 'It is changing English rather than simplifying it, adding new resources for meaning.')],
  extended=[('Write an article for a school magazine (about 300 words) arguing whether digital language is a decline or a development in English.', 'Indicative content: stance; examples of neologisms, emoji, abbreviations; prescriptive/descriptive views; appropriate register.', 10, 'long')])
pq('ch10-st2', ('C2', 'C3', 'C4'), (1, 5), {'social', 'meme', 'blog'}, 'lang', ['Identify features of digital language in this text and explain their effect.',
                                                                               'How does the text reflect conventions of online communication?',
                                                                               'Analyse how the writer adapts language to a digital medium.',
                                                                               'Evaluate what this text suggests about how digital communication is changing English.'])

H('ch10-st3',
  terms=[('misinformation', 'false or misleading information shared without intent to deceive'),
         ('disinformation', 'false information deliberately created and spread to deceive'),
         ('echo chamber', 'an environment in which a person encounters only beliefs that reinforce their own'),
         ('filter bubble', 'the personalised information environment created by algorithms that select content for each user'),
         ('confirmation bias', 'the tendency to favour information that confirms existing beliefs'),
         ('lateral reading', 'checking a source\'s credibility by consulting other sources rather than reading it alone')],
  facts=[('A post says "SHARE BEFORE THEY DELETE THIS!!!" and cites "my cousin\'s friend". These are typical features of:', 'Misinformation', ['A peer-reviewed study', 'An editorial', 'A press release'], 'Urgency and unverifiable sources are warning signs.'),
         ('The difference between misinformation and disinformation is:', 'Intent – disinformation is deliberately deceptive', ['Length', 'The platform used', 'Whether it contains images'], 'Disinformation is spread knowingly.')],
  why=[('Explain why false information often spreads faster than corrections.', 'It is often emotional and surprising, so it attracts engagement, and algorithms reward engagement; corrections are less sensational.'),
       ('Explain how algorithms contribute to echo chambers.', 'They show users more of what they already engage with, narrowing the range of views encountered and reinforcing existing beliefs.'),
       ('Explain why "Do your own research" can be a persuasive misinformation slogan.', 'It flatters readers as independent thinkers while encouraging distrust of experts and selective searching that confirms bias.')],
  contrast=[('an echo chamber', 'a filter bubble', 'An echo chamber is a social environment where people choose to hear only agreeing voices; a filter bubble is created by algorithms that personalise content, often without users realising.'),
            ('misinformation', 'disinformation', 'Misinformation is false information shared without intent to deceive; disinformation is false information created or spread deliberately to deceive.')],
  misc=[('Only uneducated people believe misinformation.', 'Everyone is vulnerable to confirmation bias; misinformation exploits emotion and trust in social networks rather than ignorance alone.')],
  evaluate=[('Social media companies should be responsible for removing misinformation.', ['they profit from engagement', 'they have the tools to act'], ['risks of censorship and errors', 'defining truth is contested'], 'Platforms bear significant responsibility, but transparency and media literacy are needed alongside removal.')],
  extended=[('Write a guide for younger students (about 300 words) on how to recognise misinformation on social media.', 'Indicative content: clear advice (check source, lateral reading, reverse image search, emotional manipulation); appropriate register for younger readers; examples.', 10, 'long')])
pq('ch10-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'misinfo', ['Identify features of this text that might mislead readers, and explain how they work.',
                                                           'How does the text attempt to make an unreliable claim seem credible?',
                                                           'Explain what a media-literate reader would notice in this text.',
                                                           'Evaluate how the text and its platform could contribute to misinformation.'])
pq('ch10-st3', 'C3', (2, 4), {'news'}, 'struct', STRUCT_Q)


# =============================================================================================
# ch11 Paper 1: approaching an unseen non-literary text
# =============================================================================================
H('ch11-st1',
  terms=[('unseen text', 'a text the student has not studied before, analysed under exam conditions in Paper 1'),
         ('guiding question', 'a question printed below each Paper 1 text that suggests a focus for the analysis; students may choose not to use it'),
         ('guided textual analysis', 'the Paper 1 task: an analysis of an unseen non-literary text, supported by a guiding question'),
         ('text type', 'the category of a text with recognisable conventions, such as an infographic, opinion column or advertisement')],
  facts=[('How long do SL students have for Paper 1?', '1 hour 15 minutes', ['2 hours 15 minutes', '1 hour 45 minutes', '45 minutes'], 'SL students analyse one of two passages in 1 hour 15 minutes.'),
         ('How many texts does an HL student analyse in Paper 1?', 'Two – both unseen non-literary passages', ['One, chosen from two', 'Three', 'One literary and one non-literary'], 'HL students write on both passages in 2 hours 15 minutes.'),
         ('How many marks is each Paper 1 analysis worth?', '20 (criteria A–D, 5 marks each)', ['30', '40', '10'], 'Each analysis is marked out of 20; HL total 40.'),
         ('What weighting does Paper 1 carry at both SL and HL?', '35%', ['25%', '20%', '50%'], 'Paper 1 is 35% at both levels.')],
  why=[('Explain why identifying the text type is a useful first step with an unseen passage.', 'Knowing the text type tells the student which conventions to expect and helps infer audience and purpose, which frame the analysis.'),
       ('Explain why students do not have to follow the guiding question.', 'It is a support, not a requirement; a student may develop their own focus as long as the analysis addresses how the text creates meaning.'),
       ('Explain why audience and purpose should be inferred from evidence in an unseen text.', 'No contextual information may be given, so claims about audience and purpose are only convincing when supported by specific textual features.')],
  contrast=[('Paper 1 at SL', 'Paper 1 at HL', 'SL students choose one of two unseen non-literary passages and write one analysis in 1 h 15 (20 marks); HL students analyse both passages in 2 h 15 (40 marks). Both carry 35%.')],
  misc=[('Paper 1 texts can be literary extracts such as poems.', 'Paper 1 in Language and Literature uses non-literary texts only; literary works are assessed in Paper 2, the IO and the HL essay.'),
        ('In Paper 1 you must answer the guiding question exactly as phrased.', 'The guiding question is optional support; a well-focused analysis of your own is also acceptable.')],
  evaluate=[('The guiding question helps weaker students more than strong ones.', ['it gives a clear focus', 'it points to a central feature'], ['strong students also benefit from a focused line of argument', 'over-reliance can narrow analysis'], 'It helps all students; stronger ones use it as a springboard rather than a limit.')],
  extended=[('Explain how you would spend the first 15 minutes of Paper 1 with an unseen text, and justify each step.', 'Indicative content: read for gist; identify type, audience, purpose, context; annotate features linked to guiding question; formulate thesis; plan paragraphs; justification.', 6, 'long')])
pq_kind_mcq('ch11-st1', NONLIT)
pq('ch11-st1', ('C2', 'C3'), (1, 4), NONLIT, ('aud', 'purp'), ['Identify the text type, audience and purpose of this unseen text, giving evidence for each.',
                                                               'Before writing a Paper 1 analysis, record the audience and purpose of this text with supporting evidence.',
                                                               'What can you infer about the intended audience and purpose of this text?'], crit=CRIT_A)
pq('ch11-st1', 'C3', (2, 4), NONLIT, 'kconv', ['Which conventions of its text type does this unseen text use, and why?'], crit=CRIT_A)

H('ch11-st2',
  terms=[('thesis', 'a clear, arguable statement that answers the question and guides the whole analysis'),
         ('line of argument', 'the logical development of ideas through an analysis, each paragraph building on the thesis'),
         ('topic sentence', 'the opening sentence of a paragraph, stating its contribution to the argument'),
         ('focus', 'the extent to which the analysis stays relevant to the question or chosen angle (criterion C)')],
  facts=[('Which is the strongest Paper 1 thesis?', '"The advert shrinks a global crisis to the scale of one commuter\'s routine, turning guilt into a purchase."', ['"The advert uses many techniques."', '"This text is about water bottles."', '"The writer uses a statistic, a tricolon and an image."'], 'It is specific, arguable and answers how the text persuades.'),
         ('A thesis that merely lists three devices is weak because:', 'It does not make an argument about meaning or effect', ['It is too short', 'It mentions devices', 'It is written in the third person'], 'A thesis should argue, not list.')],
  why=[('Explain why a thesis should be arguable rather than descriptive.', 'An arguable thesis gives the analysis direction and allows evaluation; a description gives nothing to prove.'),
       ('Explain why each paragraph should advance the argument rather than repeat it.', 'Developing the argument shows coherence and depth (criterion C), while repetition suggests a list of separate points.'),
       ('Explain why a thesis should address both "how" and "why".', 'Paper 1 rewards analysis of how features create meaning and evaluation of why the writer uses them for the audience and purpose.')],
  contrast=[('a thesis', 'a topic', 'A topic is what the text is about (plastic waste); a thesis is an arguable claim about how the text presents that topic and to what effect.')],
  misc=[('The best way to organise a Paper 1 analysis is to go through the text line by line.', 'Line-by-line commentary often becomes descriptive; organising by argument (aspects or effects) better shows focus and analysis, though a well-handled sequential approach can work.')],
  apply=[('Improve this thesis: "The speech uses rhetorical devices to persuade the audience."', 'Example: "The speaker turns a family anecdote into an accusation, using antithesis and blunt imperatives to shame leaders who mistake applause for action."', 3),
         ('Write a topic sentence for a paragraph on the visual features of an advertisement, linked to the thesis "The advert sells belonging rather than a product."', 'Example: "The image of two generations facing each other across a kitchen table visualises the belonging the brand promises, before a word has been read."', 2)],
  evaluate=[('A strong thesis is more important than detailed analysis in Paper 1.', ['it shapes focus and organisation', 'examiners look for a line of argument'], ['marks for analysis (B) depend on detail', 'a thesis without evidence is unsupported'], 'Both are essential: the thesis organises and detailed analysis proves.')],
  extended=[('Write the introduction (thesis and outline of argument) for a Paper 1 analysis of a non-literary text you have studied in class.', 'Indicative content: identifies text type, audience, purpose briefly; arguable thesis; outline of two or three aspects. Markband: focus and clarity.', 6, 'long')])
pq('ch11-st2', ('C3', 'C4'), (2, 5), NONLIT, 'gqa', ['Guiding question: {gq}\nWrite a thesis statement that answers the guiding question and outline three points that would develop it.',
                                                    'Guiding question: {gq}\nPlan a line of argument for a Paper 1 analysis of this text.',
                                                    'Guiding question: {gq}\nWrite a thesis and a topic sentence for each of your body paragraphs.'], crit=MARKBAND)

H('ch11-st3',
  terms=[('annotation', 'notes made on a text while reading, identifying features, effects and links to the question'),
         ('planning', 'organising points and evidence into a structured outline before writing'),
         ('time management', 'dividing the exam time between reading, planning, writing and checking'),
         ('first reading', 'reading the whole text for gist, tone and purpose before detailed annotation')],
  facts=[('In a 1 hour 15 minute SL Paper 1, a sensible time for reading, annotating and planning is about:', '15–20 minutes', ['1 hour', '2 minutes', '45 minutes'], 'Enough planning to create a clear argument while leaving time to write.'),
         ('Which annotation is most useful?', '"\'Fill it. Carry it. Keep it.\' – imperative tricolon: ritual, simplicity → purchase seems easy"', ['"Tricolon"', '"Interesting"', '"Good line"'], 'Useful annotation links feature, quotation and effect.')],
  why=[('Explain why annotation should link features to effects rather than only label them.', 'Annotations that note effects become analytical points ready for writing; labels alone lead to feature-spotting.'),
       ('Explain why it is useful to read the text twice before writing.', 'A first reading gives overall meaning and tone; a second reading reveals detail and patterns that support a thesis.'),
       ('Explain why HL students must plan time carefully in Paper 1.', 'They must write two complete analyses in 2 hours 15 minutes, so spending too long on one leaves the second underdeveloped.')],
  contrast=[('annotating', 'summarising', 'Annotating identifies how specific features create meaning; summarising restates what the text says.')],
  misc=[('Planning wastes time in a timed exam.', 'A short plan improves focus and organisation (criterion C) and usually saves time during writing.')],
  apply=[('You have 2 hours 15 minutes for HL Paper 1. Propose a time plan for both texts.', 'For example: about 67 minutes per text – roughly 15 minutes reading and planning, 47 minutes writing, 5 minutes checking each; justification.', 3)],
  evaluate=[('Detailed annotation is more important than a written plan.', ['annotation gathers the evidence', 'it reveals patterns'], ['a plan organises the argument', 'without a plan, annotation can lead to a list'], 'Both are needed: annotation collects material, and a plan turns it into an argument.')],
  extended=[('Annotate a short non-literary text of your choice (described in words) and produce a plan for a Paper 1 response.', 'Indicative content: annotations linked to effects; thesis; paragraph plan; time allocation.', 6, 'long')])
pq('ch11-st3', ('C3', 'C4'), (2, 5), NONLIT, 'dev', ['Write two annotations on the quotation "{quote}" that you could develop in a Paper 1 response.',
                                                    'As part of your timed annotation, explain how "{quote}" could support an answer to the guiding question: "{gq}"',
                                                    'Annotate "{quote}": name the feature, its effect and its link to the text\'s purpose.'])
pq('ch11-st3', 'C3', (2, 4), NONLIT, 'struct', ['In planning a Paper 1 answer, how would you use {feature} as evidence?',
                                                'Note in your plan how {feature} contributes to the text\'s purpose.'])

# =============================================================================================
# ch12 Paper 1: writing the guided analysis
# =============================================================================================
H('ch12-st1',
  terms=[('criterion C', 'Paper 1 criterion "Focus and organisation" (5 marks): coherence, focus and development of the analysis'),
         ('coherence', 'the logical connection of ideas so that the analysis reads as a unified argument'),
         ('transition', 'a word or phrase that links paragraphs and signals the relationship between ideas'),
         ('conclusion', 'the final section that synthesises the argument and evaluates the text\'s overall effect, without merely repeating')],
  facts=[('Which criterion assesses focus and organisation in Paper 1?', 'Criterion C', ['Criterion A', 'Criterion B', 'Criterion D'], 'C is Focus and organisation.'),
         ('A conclusion that only repeats the introduction is weak because:', 'It does not synthesise or evaluate the argument', ['It is too short', 'It is in the present tense', 'It mentions the thesis'], 'Conclusions should draw the argument together and evaluate.')],
  why=[('Explain why transitions matter in a Paper 1 analysis.', 'They show how each point relates to the previous one and to the thesis, making the analysis coherent rather than a list.'),
       ('Explain why organising by aspect can be better than by device.', 'Organising by aspect (e.g. how the text creates urgency) groups devices by effect, creating an argument rather than a catalogue.'),
       ('Explain how a conclusion can add value to an analysis.', 'It can synthesise points, evaluate the text\'s overall effectiveness and consider the bigger picture, such as context or ethics.')],
  contrast=[('a sequential structure', 'a thematic structure', 'A sequential structure follows the text from beginning to end; a thematic structure organises paragraphs around aspects of the argument. Thematic structures usually show focus more clearly.')],
  misc=[('Criterion C rewards length: the more paragraphs, the better.', 'Criterion C rewards coherent, focused development; a shorter, well-organised analysis can score higher than a long, repetitive one.')],
  apply=[('Write a transition sentence linking a paragraph on an advert\'s image to a paragraph on its slogan.', 'Example: "If the image creates the feeling of belonging, the slogan names it, anchoring the picture\'s warmth to the brand."', 2)],
  evaluate=[('Organisation matters more to the reader than analysis.', ['a disorganised analysis obscures insight', 'clarity guides the examiner'], ['organisation is only one of four criteria', 'insight is rewarded under A and B'], 'Organisation makes analysis visible; it is a means to communicate insight, not a substitute.')],
  extended=[('Write a full plan and conclusion for a Paper 1 analysis of a text you have studied, showing how each paragraph builds the argument.', 'Indicative content: thesis; paragraph topics with transitions; synthesising conclusion with evaluation.', 6, 'long')])
pq_para('ch12-st1', NONLIT, c=('C3', 'C4'), d=(2, 5), frames=[
    'Guiding question: {gq}\nPlan a three-paragraph Paper 1 analysis with a thesis, a topic sentence for each paragraph and a transition between each.',
    'Guiding question: {gq}\nWrite the conclusion of a Paper 1 analysis that synthesises your argument and evaluates the text\'s overall effect.',
    'Guiding question: {gq}\nOutline a well-organised response, explaining how each section develops the line of argument (criterion C).'])

H('ch12-st2',
  terms=[('criterion B', 'Paper 1 criterion "Analysis and evaluation" (5 marks): how well the student analyses and evaluates the ways textual features and authorial choices shape meaning'),
         ('authorial choice', 'a deliberate decision by the writer about language, structure, style or form'),
         ('evaluation', 'judging how effectively a writer\'s choices achieve their purpose, or their implications'),
         ('feature-spotting', 'naming devices without analysing their effect')],
  facts=[('Which response best shows evaluation?', '"The statistic is persuasive for commuters, yet the footnote\'s tiny sample undermines the claim for a careful reader."', ['"The statistic is a statistic."', '"There is a statistic in line 2."', '"The writer uses numbers."'], 'It judges effectiveness and its limits.'),
         ('What does criterion B reward most?', 'Analysis of how choices shape meaning, and evaluation of their effect', ['Correct spelling', 'Knowing the author\'s biography', 'Length of the answer'], 'B is analysis and evaluation.')],
  why=[('Explain why evaluation goes beyond analysis.', 'Analysis explains how a feature works; evaluation judges how well it works, for whom, and with what wider implications.'),
       ('Explain why focusing on fewer features in more depth earns more credit.', 'Depth allows close analysis of language, connotation and effect, which criterion B rewards over a superficial list.'),
       ('Explain why it is useful to consider the limitations of a text\'s persuasion.', 'Recognising where a text may fail or manipulate shows critical evaluation and independence of thought.')],
  contrast=[('analysis', 'evaluation', 'Analysis explains how features create meaning and effect; evaluation judges the success, limitations or implications of those choices.')],
  misc=[('Evaluation means saying whether you liked the text.', 'Evaluation judges the effectiveness and implications of the writer\'s choices for an audience and purpose, not personal taste.')],
  evaluate=[('Students should always criticise a non-literary text in Paper 1 to show evaluation.', ['criticism shows independence', 'many texts manipulate'], ['evaluation can affirm effectiveness', 'forced criticism is unconvincing'], 'Evaluation should be balanced and evidence-based; it may praise, criticise or both.')],
  extended=[('Write one analytical paragraph on a non-literary text you have studied that both analyses and evaluates a single authorial choice.', 'Indicative content: choice identified with quotation; analysis of effect; evaluation of effectiveness and limitations.', 6, 'long')])
pq('ch12-st2', ('C3', 'C4'), (2, 5), NONLIT, 'dev', ['Analyse and evaluate the writer\'s use of "{quote}".',
                                                    'How effective is the {device} "{quote}" for the intended audience? Analyse and evaluate.',
                                                    'Write a criterion B-focused paragraph on "{quote}", analysing its effect and evaluating its success.'])
pq('ch12-st2', 'C4', (3, 5), NONLIT, 'read', ['Evaluate the text\'s effectiveness for its intended audience, considering how a different reader might respond.',
                                             'Analyse the text\'s main persuasive strategy and evaluate its limitations.'], typ='long', crit=MARKBAND)

H('ch12-st3',
  terms=[('criterion D', 'Paper 1 criterion "Language" (5 marks): clarity, variety and accuracy of language and appropriateness of register and style'),
         ('academic register', 'formal, precise language suited to analytical writing'),
         ('hedging', 'using cautious language such as "suggests" or "may imply" to present interpretations'),
         ('precise terminology', 'accurate use of subject terms (e.g. antithesis, anchorage) to describe features')],
  facts=[('Which sentence uses the most appropriate academic register?', '"The juxtaposition of abundance and absence suggests a community hollowed out by tourism."', ['"The writer is really annoyed about tourists."', '"This bit is kind of sad."', '"Tourism = bad, says writer."'], 'It is formal, precise and analytical.'),
         ('Which verb is the best choice for introducing an interpretation?', 'suggests', ['proves', 'says', 'shows 100%'], 'Hedged verbs present interpretations appropriately.')],
  why=[('Explain why precise vocabulary improves analysis.', 'Precise verbs and terms (e.g. "undermines", "anchors") express exactly how a feature works, which also strengthens criterion B.'),
       ('Explain why hedging is appropriate in literary and textual analysis.', 'Interpretations are arguments, not facts; hedging shows awareness of alternative readings while still making a claim.'),
       ('Explain why variety of sentence structure matters in Paper 1.', 'Varied sentences keep writing clear and engaging and allow complex relationships between ideas to be expressed.')],
  contrast=[('formal register', 'informal register', 'Formal register uses complete sentences, precise vocabulary and impersonal constructions; informal register uses contractions, slang and conversational tone – unsuitable for analysis.')],
  misc=[('Using long, complicated words always earns marks for language.', 'Criterion D rewards clarity, precision and appropriateness; inflated vocabulary that obscures meaning can lower the mark.')],
  apply=[('Rewrite in academic register: "The writer uses loads of emotional stuff to make you feel bad for the dog."', 'Example: "Emotive details such as the dog being \'tied to a motorway barrier in January\' provoke pity and indignation, encouraging donation."', 2),
         ('Replace the weak verb in: "The image shows that the bottle is important."', 'Example: "The image foregrounds the bottle, isolating it against the grey crowd." (foregrounds/isolates/emphasises)', 2),
         ('Rewrite with appropriate hedging: "The poem proves the mother hates London."', 'Example: "The image of a language \'the neighbours think is weather\' may suggest the mother\'s isolation in London."', 2)],
  evaluate=[('Criterion D is the least important of the Paper 1 criteria.', ['it has the same marks as the others', 'content seems more important'], ['language carries the analysis', 'poor expression obscures insight'], 'All criteria are equally weighted; clear language is the vehicle for every other criterion.')],
  extended=[('Take a paragraph of your own previous Paper 1 writing and redraft it to improve precision, register and variety. Explain three changes.', 'Indicative content: before/after comparison; specific changes (verbs, terminology, sentence structure); explanation of effect on clarity.', 6, 'long')])
pq('ch12-st3', 'C3', (2, 4), NONLIT, 'dev', ['Write one precise, academic sentence analysing "{quote}", using an exact analytical verb.',
                                            'Using precise terminology, write two sentences on the effect of "{quote}".'])

H('ch12-st4',
  terms=[('markband', 'a range of marks with descriptors used to assess a response against a criterion'),
         ('exemplar', 'a sample response, often marked, used to show standards'),
         ('best-fit approach', 'IB marking principle: the examiner chooses the markband that best describes the response overall'),
         ('self-assessment', 'evaluating one\'s own work against the assessment criteria to identify improvements')],
  facts=[('In IB marking, the "best-fit" approach means:', 'The examiner awards the band that best describes the work overall', ['Every descriptor must be met exactly', 'Marks are deducted for each error', 'Only the conclusion is marked'], 'Best fit balances strengths and weaknesses.'),
         ('A response that identifies devices but rarely explains effects would most likely score in criterion B at:', 'The lower-middle bands (around 2 out of 5)', ['5 out of 5', '0 out of 5 always', '4 out of 5'], 'Feature-spotting limits B.')],
  why=[('Explain why studying marked exemplars helps students improve.', 'Exemplars show what each band looks like in practice, making abstract descriptors concrete and showing the gap between current and target performance.'),
       ('Explain why self-assessment should focus on one criterion at a time.', 'Concentrating on one criterion makes feedback specific and actionable, rather than a general impression.'),
       ('Explain why a response can score highly on one criterion and lower on another.', 'The criteria assess different skills – understanding, analysis, organisation and language – so a response may have insight but weak structure.')],
  contrast=[('summative assessment', 'formative assessment', 'Summative assessment measures achievement at the end (an exam mark); formative assessment, such as self-assessment, gives feedback to improve learning.')],
  misc=[('If a response has a few errors it cannot get top marks for language.', 'The best-fit approach allows occasional errors in an excellent response; top bands require control, not perfection.')],
  apply=[('A student paragraph reads: "The advert uses a statistic. It also uses a tricolon. There is a picture of a bottle." Assign a likely criterion B mark out of 5 and give two targets.', 'Likely 1–2/5: devices identified but no analysis of effect. Targets: explain each feature\'s effect on the audience; link features to purpose and thesis.', 3),
         ('A student\'s analysis is insightful but jumps between points without links. Which criterion is weakest, and what should the student do?', 'Criterion C (focus and organisation); use a clear thesis, topic sentences and transitions so points build an argument.', 2),
         ('A student\'s Paper 1 response analyses effects precisely but uses informal phrases such as "kind of" and "loads". Which criterion is affected and how could it improve?', 'Criterion D (language); replace informal phrases with precise academic vocabulary and hedged verbs.', 2)],
  evaluate=[('Self-assessment is less reliable than teacher assessment and therefore less useful.', ['students may misjudge their work', 'teachers know the standard'], ['self-assessment builds independence', 'it develops understanding of criteria'], 'It is less reliable as a mark but highly useful as a learning tool, especially alongside teacher feedback.')],
  extended=[('Write a short exemplar paragraph that would reach the top band for criterion B on a text you have studied, then annotate it to show why it meets the descriptors.', 'Indicative content: perceptive analysis of specific choices; evaluation; annotations linked to descriptors.', 6, 'long')])
pq('ch12-st4', ('C3', 'C4'), (2, 5), NONLIT, 'gqa', ['Guiding question: {gq}\nA student\'s thesis is: "The text uses many techniques to persuade." Assess it against criterion C and rewrite it to reach the top band.',
                                                    'Guiding question: {gq}\nList what a top-band response (criteria A and B) would need to include for this text.'], crit=P1_BANDS)


# =============================================================================================
# ch13 Global issues and the learner portfolio
# =============================================================================================
FIELDS = ['culture, identity and community', 'beliefs, values and education', 'politics, power and justice',
          'art, creativity and the imagination', 'science, technology and the environment']
H('ch13-st1',
  terms=[('field of inquiry', 'one of five broad areas suggested for locating a global issue for the Individual Oral'),
         ('global issue', 'an issue with significance on a wide or transnational scale, felt in everyday local contexts'),
         ('transnational', 'extending across national boundaries')],
  facts=[('Which is NOT one of the five fields of inquiry for the Individual Oral?', 'Sport, leisure and health', ['Culture, identity and community', 'Beliefs, values and education', 'Politics, power and justice'], 'The five are culture, identity and community; beliefs, values and education; politics, power and justice; art, creativity and the imagination; science, technology and the environment.'),
         ('Under which field of inquiry would climate migration most naturally fall?', 'Science, technology and the environment', ['Art, creativity and the imagination', 'Beliefs, values and education', 'None of the fields'], 'Environmental change is central, though links to politics and justice can be made.'),
         ('Under which field of inquiry would censorship of artists most naturally fall?', 'Art, creativity and the imagination', ['Science, technology and the environment', 'Beliefs, values and education', 'None of the fields'], 'It concerns artistic freedom, with links to politics, power and justice.')],
  why=[('Explain why fields of inquiry are a starting point rather than the global issue itself.', 'A field is a broad area; the IO needs a specific global issue (e.g. "the commodification of women\'s bodies in media") that can be traced in both texts.'),
       ('Explain why a global issue must be both local and transnational.', 'It must be felt in specific lives and places (as texts show) while also mattering across many countries, giving it wide significance.'),
       ('Explain why the same issue can belong to several fields of inquiry.', 'Issues are interconnected – for example accent prejudice involves identity, education and power – so students can frame them from different angles.')],
  contrast=[('a field of inquiry', 'a global issue', 'A field of inquiry is a broad area (politics, power and justice); a global issue is a specific, arguable concern within it (the silencing of protest by state media).')],
  misc=[('"Love" is a good global issue for the Individual Oral.', '"Love" is a theme, not an issue; a global issue must be a problem or debate of transnational significance, e.g. "the pressure of family expectations on individual choice in marriage".')],
  apply=[('Turn the broad topic "technology" into a focused global issue suitable for the IO.', 'Example: "The way social media platforms monetise young people\'s attention and affect their wellbeing."', 2),
         ('Turn the broad topic "gender" into a focused global issue suitable for the IO.', 'Example: "The representation of women\'s domestic labour as natural and unpaid."', 2),
         ('Turn the broad topic "war" into a focused global issue suitable for the IO.', 'Example: "The use of heroic propaganda to conceal the human cost of war."', 2)],
  evaluate=[('The five fields of inquiry are too broad to be useful.', ['almost any issue fits', 'students still need to narrow down'], ['breadth allows choice', 'they prompt thinking about issue rather than theme'], 'Their breadth is intended; their value lies in prompting students towards issues, which they must then narrow.')],
  extended=[('For one field of inquiry, propose a global issue and explain how it appears in one literary work and one non-literary text you have studied.', 'Indicative content: specific issue; evidence in both texts; justification of global significance.', 6, 'long')])
pq('ch13-st1', ('C2', 'C3'), (1, 4), None, 'field', ['Which field of inquiry would be the most appropriate starting point for an IO using this text? Justify your choice.',
                                                    'Suggest a field of inquiry and a focused global issue for which this text could be used.'], crit=CRIT_OPEN)
pq('ch13-st1', 'C4', (3, 5), None, ('field', 'issue'), ['Discuss how this text could be used to explore a global issue within two different fields of inquiry.'], typ='long',
   crit='The most direct field and issue are given; a second field must be named and justified with reference to the text (e.g. an environmental text may also fit politics, power and justice). ' + MARKBAND)

H('ch13-st2',
  terms=[('local manifestation', 'the specific way a global issue appears in a particular place, community or text'),
         ('global significance', 'the importance of an issue across many societies and contexts'),
         ('issue statement', 'a single sentence that names the global issue precisely and suggests how both texts engage with it')],
  facts=[('Which is the best-phrased global issue for an IO?', 'The way consumer culture commodifies environmental concern', ['Nature', 'The environment is important', 'Plastic'], 'It is specific, arguable and has global significance.'),
         ('In the IO, the global issue must be explored through:', 'An extract from one literary work and one from a non-literary body of work', ['Two literary works only', 'Two non-literary texts only', 'A single text'], 'The IO pairs one literary and one non-literary extract.')],
  why=[('Explain why the global issue should be narrow enough to be discussed in ten minutes.', 'A focused issue allows detailed analysis of how both extracts present it; a broad one leads to generalisation.'),
       ('Explain why the issue must be visible in both extracts.', 'The IO assesses how both texts present the issue; if it is only in one, the connection is weak and criterion A/B suffer.'),
       ('Explain how a non-literary body of work can present a global issue differently from a literary work.', 'Non-literary texts often address the issue directly and persuasively, while literary works explore it through character, narrative and ambiguity.')],
  contrast=[('a theme', 'a global issue', 'A theme is a recurring idea in a work (loss, ambition); a global issue is a real-world problem of wide significance (exploitative labour in global supply chains) that a text engages with.')],
  misc=[('Any theme of a text counts as a global issue.', 'A global issue must have real-world significance across societies; themes such as "friendship" need reframing into an issue.')],
  evaluate=[('Literary works present global issues more powerfully than non-literary texts.', ['they create empathy through character', 'complexity resists easy answers'], ['non-literary texts reach and mobilise wide audiences', 'they confront issues directly'], 'Each has distinctive power: literature deepens understanding, non-literary texts often drive action.')],
  extended=[('Write an issue statement for an IO and explain how an extract from a literary work and a text from a non-literary body of work would each present it.', 'Indicative content: precise statement; extract choices; authorial choices; connection.', 6, 'long')])
pq('ch13-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'issue', ISSUE_Q + ['Write a precise issue statement for an Individual Oral using this text, and justify it.'], crit=CRIT_OPEN)

H('ch13-st3',
  terms=[('extract', 'a passage of no more than 40 lines selected from a text for the Individual Oral'),
         ('representative extract', 'an extract that shows the global issue clearly and reflects the wider work\'s methods'),
         ('outline', 'the one-page plan (no more than ten bullet points) a student may bring into the IO')],
  facts=[('What is the maximum length of each extract for the Individual Oral?', '40 lines', ['20 lines', '100 lines', 'One page of prose'], 'Each extract should be no more than 40 lines.'),
         ('How many bullet points may the IO outline contain?', 'No more than ten', ['Unlimited', 'Exactly three', 'No more than twenty'], 'The outline is limited to ten bullet points.')],
  why=[('Explain why the chosen extract should be rich in authorial choices.', 'Criterion B rewards analysis of authorial choices; an extract dense in significant features gives material to analyse.'),
       ('Explain why the extract should connect to the work as a whole.', 'The IO requires discussion of the extract and the whole work or body of work, so a pivotal extract allows that connection.'),
       ('Explain why visual texts can be good non-literary extracts for the IO.', 'They contain many analysable choices (composition, colour, text) and present issues directly, contrasting with the literary extract\'s methods.')],
  contrast=[('a pivotal extract', 'a typical extract', 'A pivotal extract marks a turning point or key moment in the work; a typical extract shows the work\'s usual methods. Both can work if they present the issue clearly.')],
  misc=[('The best IO extract is the most famous passage of the work.', 'The best extract is the one that presents the chosen global issue most richly; fame does not guarantee relevance.')],
  apply=[('A student\'s global issue is "the silencing of women\'s voices in public life". Suggest what kind of extract from a novel and what kind of non-literary text would suit it.', 'For example: a scene where a female character is interrupted or ignored in a male-dominated setting; a set of newspaper front pages or a speech by a female politician receiving hostile media framing.', 3),
         ('Explain two criteria you would use to choose between two possible extracts for an IO.', 'Density of analysable authorial choices; clarity of the global issue; connection to the whole work; length within 40 lines.', 2)],
  evaluate=[('Choosing the extract is the most important decision in preparing the IO.', ['the extract determines the material for analysis', 'a weak extract limits all criteria'], ['the issue and structure also matter', 'delivery affects criterion C and D'], 'It is foundational, though a strong extract still needs a clear issue and structure.')],
  extended=[('Present your choice of two IO extracts (described briefly) and justify them in relation to a global issue.', 'Indicative content: issue; extract descriptions; justification by authorial choices and connection to wider works.', 6, 'long')])
pq('ch13-st3', ('C3', 'C4'), (2, 5), None, 'issue', ['If you used this text as an IO extract, what global issue would it present, and which two features would you analyse?',
                                                   'Explain why this text would or would not be a strong extract for an IO on the issue it raises.'], crit=CRIT_OPEN)
pq('ch13-st3', 'C3', (2, 4), None, 'dev', ['As an IO extract, how could "{quote}" be used to show the global issue the text raises?'])


# =============================================================================================
# ch14 Individual Oral
# =============================================================================================
H('ch14-st1',
  terms=[('Individual Oral (IO)', 'a 15-minute assessment: a 10-minute prepared response followed by 5 minutes of teacher questions, examining how a global issue is presented in a literary and a non-literary extract'),
         ('prompt', 'the IO task: "Examine the ways in which the global issue of your choice is presented through the content and form of one of the works and one of the texts that you have studied."'),
         ('internal assessment', 'assessment marked by the teacher and moderated by the IB'),
         ('connection to the whole work', 'discussion of how the extract relates to the work or body of work as a whole')],
  facts=[('How long is the Individual Oral in total?', '15 minutes (10 minutes response + 5 minutes questions)', ['10 minutes', '20 minutes', '30 minutes'], 'The IO lasts 15 minutes.'),
         ('How much is the IO worth at HL?', '20% (40 marks)', ['30% (40 marks)', '25% (30 marks)', '35% (20 marks)'], 'HL IO 20%; SL IO 30%.'),
         ('How much is the IO worth at SL?', '30%', ['20%', '35%', '25%'], 'At SL the IO carries 30%.')],
  why=[('Explain why the IO should be roughly balanced between the two texts.', 'The task requires examining both texts; imbalance weakens criteria A and B and the comparison.'),
       ('Explain why the introduction of the IO should state the global issue clearly.', 'A clear issue gives focus (criterion C) and tells the teacher what the analysis will show.'),
       ('Explain why connecting the extract to the whole work matters.', 'The prompt requires discussion of the work as a whole; showing how the extract fits demonstrates knowledge (criterion A).')],
  contrast=[('the 10-minute response', 'the 5-minute discussion', 'The 10-minute response is the student\'s prepared, uninterrupted analysis; the 5-minute discussion consists of teacher questions that let the student clarify and extend ideas.')],
  misc=[('The IO is a memorised speech.', 'Students may use only a ten-point outline; the IO should be a prepared but not scripted analysis, and responses to questions are spontaneous.')],
  apply=[('Propose a timed structure for the 10-minute IO response.', 'For example: introduction with issue and texts (1 min); literary extract (about 3.5 min); non-literary extract (about 3.5 min); connections and whole works (1.5 min); conclusion (0.5 min).', 3)],
  evaluate=[('Discussing the texts separately is better than integrating them throughout the IO.', ['it is clearer and easier to manage', 'each text gets full attention'], ['integration shows connection and insight', 'the issue binds them'], 'Either can succeed; integration can show more insight, but a clear separate structure with explicit connections is often safer.')],
  extended=[('Write the outline (ten bullet points maximum) for an IO on a global issue of your choice, using one literary work and one non-literary text you have studied.', 'Indicative content: issue; texts; key features to analyse in each; connections; timing. Must respect ten-point limit.', 6, 'long')])
pq('ch14-st1', ('C3', 'C4'), (2, 5), None, 'issue', ['Using this text as your non-literary extract, write the introduction to an Individual Oral, stating the global issue and how you will examine it.'], crit=CRIT_OPEN)
pq('ch14-st1', ('C3', 'C4'), (2, 5), None, 'gqa', ['Plan the section of your IO on this text: list the points you would make in about three minutes.',
                                                 'Outline how you would analyse this text in the body of an Individual Oral, in about three minutes of speaking.'], crit=CRIT_OPEN)

H('ch14-st2',
  terms=[('IO criterion B', 'Analysis and evaluation (10 marks): how well the student analyses and evaluates the ways the issue is presented through authorial choices in both texts'),
         ('content and form', 'what a text says and how it says it; the IO prompt asks about both'),
         ('authorial choice', 'a deliberate decision by the writer or creator, such as diction, structure, image or point of view')],
  facts=[('How many marks is criterion B worth in the IO?', '10', ['5', '20', '8'], 'Each IO criterion is worth 10 marks (40 total).'),
         ('The IO prompt asks students to examine the issue through:', 'Content and form', ['Biography and history', 'Plot and character only', 'Themes only'], 'Form (authorial choices) must be analysed.')],
  why=[('Explain why analysis of form is essential in the IO.', 'The prompt asks how the issue is presented "through content and form"; analysing authorial choices is required for criterion B.'),
       ('Explain why comparing the methods of the two texts strengthens the IO.', 'Contrasting how a literary and a non-literary text present the issue shows insight into how form shapes meaning.'),
       ('Explain why quoting precisely matters in an oral.', 'Precise reference shows close knowledge and allows detailed analysis of specific choices.')],
  contrast=[('content', 'form', 'Content is what a text presents (events, ideas); form is how it is presented (structure, language, visual design). The IO must analyse both.')],
  misc=[('In the IO, discussing what happens in the texts is enough.', 'Description of content earns little under criterion B; students must analyse how authorial choices present the issue.')],
  evaluate=[('The non-literary text is easier to analyse in the IO than the literary work.', ['its persuasive features are more obvious', 'it is shorter'], ['visual and multimodal analysis requires specific skills', 'simple-looking texts can be subtle'], 'Neither is inherently easier; each requires appropriate analytical tools.')],
  extended=[('Write the section of an IO script (about 300 words) analysing how an extract from a literary work you have studied presents a global issue.', 'Indicative content: specific authorial choices with quotation; effects; link to issue and whole work.', 8, 'long')])
pq('ch14-st2', ('C3', 'C4'), (2, 5), None, 'dev', ['In an Individual Oral on the issue "{issue}", how would you analyse "{quote}"?',
                                                  'For your IO, analyse how "{quote}" presents the global issue through form as well as content.',
                                                  'Explain how the {device} "{quote}" could support your IO analysis (criterion B).'])

H('ch14-st3',
  terms=[('IO criterion A', 'Knowledge, understanding and interpretation (10 marks): knowledge of the extracts and works and interpretation of their implications in relation to the issue'),
         ('whole work', 'the full literary work or body of work from which the IO extract is taken'),
         ('implication', 'a meaning or consequence suggested by a text rather than stated')],
  facts=[('Which criterion assesses knowledge of the extracts and the works as a whole in the IO?', 'Criterion A', ['Criterion B', 'Criterion C', 'Criterion D'], 'A: Knowledge, understanding and interpretation.'),
         ('A student who only discusses the extracts without referring to the rest of the works is likely to lose marks mainly in:', 'Criterion A', ['Criterion D', 'Criterion C only', 'No criterion'], 'A requires knowledge of the works as a whole.')],
  why=[('Explain why interpretation is rewarded in criterion A.', 'Criterion A rewards understanding of implications – what the texts suggest about the issue – not just recall of content.'),
       ('Explain why references to the wider work should be brief and specific.', 'Brief, specific references show knowledge without taking time from analysis of the extracts.'),
       ('Explain how the global issue links the two texts in criterion A.', 'The issue provides the lens through which the student interprets both texts, showing understanding of how each presents it.')],
  contrast=[('knowledge', 'interpretation', 'Knowledge is accurate understanding of what the texts contain; interpretation is the student\'s argued reading of what they mean or imply.')],
  misc=[('Criterion A is about memorising plot details.', 'It rewards understanding and interpretation of the texts in relation to the issue, supported by well-chosen references.')],
  evaluate=[('A deep interpretation of the extracts matters more than knowledge of the whole works.', ['the extracts are the focus', 'depth shows insight'], ['the task requires the works as a whole', 'context gives meaning to extracts'], 'Both are needed; interpretation of extracts gains depth from knowledge of the whole.')],
  extended=[('Explain how you would show knowledge of the whole work in an IO focused on a short extract.', 'Indicative content: pivotal moments; brief specific references; connecting extract to development of the issue.', 6, 'long')])
pq('ch14-st3', ('C3', 'C4'), (2, 5), None, 'concept', ['For an Individual Oral, explain what this text implies about the global issue it raises, using the concept of {cname}.',
                                                     'Interpret the implications of this text for the issue it raises, as you would in an IO.'], crit=CRIT_OPEN)
pq('ch14-st3', 'C3', (2, 4), None, 'issue', ISSUE_Q, crit=CRIT_OPEN)

H('ch14-st4',
  terms=[('IO criterion C', 'Focus and organisation (10 marks): how well the oral maintains focus on the issue and is coherently structured'),
         ('IO criterion D', 'Language (10 marks): clarity, accuracy and appropriateness of language and register'),
         ('signposting', 'phrases that tell the listener where the oral is going, such as "Turning now to the advertisement..."')],
  facts=[('How long is the teacher-led discussion at the end of the IO?', '5 minutes', ['10 minutes', '2 minutes', '15 minutes'], 'After the 10-minute response there are 5 minutes of questions.'),
         ('Which is most likely to help criterion C in an oral?', 'Clear signposting between sections', ['Speaking as fast as possible', 'Reading a full script', 'Avoiding the global issue'], 'Signposting supports organisation.')],
  why=[('Explain why signposting is especially important in an oral.', 'Listeners cannot reread; signposting tells them how ideas connect, supporting criterion C.'),
       ('Explain how students can use the teacher\'s questions to improve their IO.', 'Questions allow students to clarify, extend or correct points and show further knowledge and analysis.'),
       ('Explain why register matters in the IO.', 'Criterion D rewards appropriate, precise academic language even in speech; too casual a register weakens the oral.')],
  contrast=[('a scripted delivery', 'a prepared delivery', 'A scripted delivery reads a memorised text and sounds unnatural; a prepared delivery uses an outline and practised points while speaking naturally – the IO expects the latter.')],
  misc=[('If you run out of things to say before 10 minutes, the IO is a fail.', 'Shorter responses are not automatically failed, though they may lose marks for underdeveloped analysis; the teacher will move to questions.')],
  apply=[('Write three signposting phrases you could use to move between sections of an IO.', 'Examples: "Having examined how the novel presents the issue through narrative voice, I will now turn to the advertisement\'s visual strategies."; "This connects to the work as a whole..."; "In contrast to the poem\'s ambiguity, the campaign..."', 2),
         ('Your teacher asks: "How does this extract relate to the ending of the novel?" Explain how you would answer effectively.', 'Acknowledge the question; refer briefly and specifically to the ending; link it to the issue and the extract\'s authorial choices; keep the answer concise.', 3)],
  evaluate=[('The five-minute discussion is less important than the ten-minute response.', ['the response contains most of the analysis', 'it is prepared'], ['the discussion can lift marks across criteria', 'it shows genuine understanding'], 'The response carries most weight, but the discussion can confirm and extend understanding.')],
  extended=[('Write a self-assessment of a practice IO against criteria C and D, identifying two strengths and two targets.', 'Indicative content: specific evidence from the practice; accurate use of criteria; actionable targets.', 6, 'long')])
pq('ch14-st4', 'C3', (2, 4), None, 'issue', ['Write the signposted transition you would use in an IO to move from a literary extract to this text, naming the global issue.',
                                            'Write the opening 30 seconds of an IO that uses this text, stating the global issue clearly.'], crit=CRIT_OPEN)
pq('ch14-st4', 'C4', (3, 5), None, 'read', ['In the IO discussion your teacher asks how another reader might respond differently to this text. Prepare a full answer.'], typ='long', crit=MARKBAND)
