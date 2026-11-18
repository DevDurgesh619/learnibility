"""Cambridge International A Level English Language 9093 (grade 12): Papers 3 and 4.

Paper 3 Language Analysis: Q1 language change (a historical text with n-gram / corpus data) and Q2 child language
acquisition (a transcript). Paper 4 Language Topics: Q1 English in the world and Q2 language and the self
(discursive essays responding to a stimulus text and drawing on ideas and research).

All historical-style texts, transcripts, data tables, letters and utterances are original (constructed for this
bank). Named research (Kachru, Skinner, Chomsky, Piaget, Bruner, Vygotsky, Lakoff, Tannen, Giles, Brown and Levinson,
Aitchison, Labov, Trudgill, Milroy, Phillipson ...) is summarised, not quoted. Numerical items (MLU, frequency per
million words, percentage change, rates and shares) are computed in the templates. Long items carry A Level style
level descriptors (AO3 analysis, AO4 linguistic concepts and issues, AO5 evaluation) and indicative content.
Helpers come from g11_english.
"""
import re

from ._lib import topic, mcq, compose, person, city, CTX  # noqa: F401
from .g11_english import Q, cap, clean, marks, upto, pts_key, bands, an, NUMW, sq, _wrap

PROFILE = {'mark_scale': {'long': (2.5, 3)}, 'wordy': True}
CHAPTERS = {}

AO2 = {'p3': 'AO3 analysis of the data and AO4 understanding of linguistic concepts and issues',
       'p4': 'AO4 understanding of linguistic concepts and issues and AO5 evaluation of ideas and research'}
LEVELS2 = {
    'p3': ['detailed, insightful analysis of a wide range of features in the data, with precise, apt examples; sophisticated understanding of relevant concepts, theories and research, applied critically to the data',
           'clear, well-developed analysis of a range of features with appropriate examples; secure understanding of relevant concepts and theories, applied to the data',
           'some analysis of features with examples; some understanding of concepts and theories, not always linked to the data',
           'limited analysis, often descriptive; some relevant terminology; theories mentioned rather than applied',
           'little relevant analysis; mainly paraphrase; very limited terminology'],
    'p4': ['a perceptive, well-structured discussion that evaluates a range of ideas, theories and research critically; precise, relevant examples, including from the stimulus; a sustained, reasoned argument',
           'a clear, structured discussion with some evaluation of ideas and research; relevant examples; a developed argument',
           'some discussion of relevant ideas with examples; evaluation is limited or uneven',
           'a mainly descriptive response with few examples; little evaluation',
           'limited relevant content; ideas asserted rather than discussed'],
}


def lv2(m, kind, ind):
    b = bands(m)
    lv = LEVELS2[kind]
    if len(b) == 5:
        names, descs = ['Level 5', 'Level 4', 'Level 3', 'Level 2', 'Level 1'], lv
    else:
        names, descs = ['Top level', 'Middle level', 'Lower level'], [lv[0], lv[2], lv[4]]
    parts = '; '.join(f'{n} ({r}): {d}' for n, r, d in zip(names, b, descs))
    return f'Level-marked out of {m} ({AO2[kind]}). {parts}. Indicative content: {ind}'


def cls_templates(t, sets, c2_ctx=None, c2=True):
    """sets: (pool, items [(text, label, why)], frame). C1 classify MCQ; C2 explain."""
    @t.add('C1', (1, 2, 3))
    def cls_c1(r, D):
        pool, items, frame = r.choice(sets)
        s, lab, why = r.choice(items)
        opts, ans = mcq(r, cap(lab), [cap(x) for x in pool if x != lab])
        return {'stem': frame.format(q=Q(s)), 'options': opts, 'answer': ans, 'key': f'{cap(lab)}: {why}.'}

    if c2:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def cls_c2(r, D):
            pool, items, frame = r.choice(sets)
            s, lab, why = r.choice(items)
            m = marks('C2', D)
            lead = r.choice(c2_ctx) if c2_ctx else 'Consider this example'
            return {'stem': f'{lead}: {Q(s)} Identify what it illustrates and explain your answer.', 'answer': f'{cap(lab)}: {why}.',
                    'key': f'{upto(m)}: 1 mark – identifies {lab}; 1 mark – explains with reference to the example ({why}); 1 mark – links to a relevant concept, theory or context.', 'marks': m}


def fixed_c2(t, entries):
    """entries: (question, answer, [points]) -> C2 explain items with point keys sized to the marks."""
    ents = list(entries)

    @t.add('C2', (1, 2, 3, 4), 'explain')
    def fx_c2(r, D):
        q, a, pts = r.choice(ents)
        m = marks('C2', D)
        return {'stem': q, 'answer': a, 'key': pts_key(m, pts), 'marks': m}


def essay(r, D, stem, ind, kind='p4'):
    m = marks('C4', D, long=True)
    return {'stem': stem, 'answer': f'Indicative content: {ind}', 'key': lv2(m, kind, ind), 'type': 'long', 'marks': m}


STIM_CLA = ['A parenting website claims: ‘Children learn to talk by copying their parents, so talk to your baby as much as possible.’',
            'A newspaper headline reads: ‘Toddlers are tiny grammar geniuses, scientists say.’',
            'A nursery manager writes: ‘Children here learn most from playing and chatting with each other, not from adults.’',
            'A grandparent comments: ‘We never used baby talk with our children, and they all speak perfectly well.’',
            'A blogger writes: ‘My daughter said “I runned” today. Clearly she isn’t just copying me!’',
            'A podcast host argues: ‘Screen time is ruining toddlers’ language development.’']
ESSAY_LEAD = ['Refer to the statement above and to your wider study.', 'Use the statement as a starting point for your answer.', 'Draw on ideas and research from your study of child language acquisition.']


def stim_essay(r, D, title, ind, kind='p4'):
    st = r.choice(STIM_CLA)
    tail = r.choice(ESSAY_LEAD)
    return essay(r, D, f'{st} {title} {tail}', ind, kind)


def low1(t):
    return t[:1].lower() + t[1:] if t[:1].isupper() and not t.startswith(('I ', '‘')) else t


def pct(a, b):
    return (b - a) / a * 100


def f1(x):
    return f'{x:.1f}'


# =========================================================== 1 Language change

class HText:
    """An original historical-style text with annotated features of its period."""

    def __init__(self, label, date, period, text, feats, modern):
        self.label, self.date, self.period = label, date, period
        self.text = clean(sq(text))
        self.feats = [(sq(q), f, e) for q, f, e in feats]
        self.modern = modern
        for q, _, _ in self.feats:
            assert q in self.text, q

    def show(self):
        return f'Read {self.label} ({self.date}): {Q(self.text)}'


HTEXTS = [
    HText('a letter from a London merchant to his brother', '1665', 'Early Modern English', """
Deare Brother, I received yours of the 3d instant, and am glad to heare that thou and thy Family are in good Health. The Sicknesse
encreaseth here dayly, so that I doe purpose to remove my Wife and Children into the Countrey. Trade is very dead, and no Ship hath
come into the River this fortnight. I pray thee send me word whether the Wooll be sold, and at what price. Thy loving Brother, Thomas""",
          [('Deare Brother', 'non-standard (pre-dictionary) spelling', 'final -e (‘Deare’, ‘heare’) reflects variable spelling before standardisation'),
           ('thou and thy Family', 'archaic second-person pronoun', '‘thou/thy’ is used between close family, marking intimacy (the T/V distinction)'),
           ('The Sicknesse encreaseth here dayly', '-eth third-person verb inflection', '‘encreaseth’ shows the older -eth ending, later replaced by -s'),
           ('I doe purpose', 'auxiliary do in a positive statement', 'unstressed periphrastic ‘do’ in a statement, common in EME, now used only for emphasis'),
           ('no Ship hath come', 'archaic verb form', '‘hath’ is the older third-person form of ‘have’'),
           ('my Wife and Children into the Countrey', 'capitalisation of common nouns', 'common nouns are capitalised, a printing and writing convention that declined in the late 18th century'),
           ('I pray thee send me word', 'politeness formula', '‘I pray thee’ is an archaic request formula, now replaced by ‘please’'),
           ('yours of the 3d instant', 'archaic lexis', '‘instant’ means ‘of this month’, a business convention now largely obsolete')],
          'Dear Brother, I received your letter of the 3rd of this month and am glad to hear that you and your family are well. The plague is increasing here daily, so I intend to move my wife and children to the country …'),
    HText('an advertisement from a newspaper', '1752', 'Early Modern English', """
To be SOLD, at the Golden Lion in Cheapſide, a large Parcel of the fineſt Tea, Coffee and Chocolate, lately imported, at reaſonable
Rates. Likewiſe a choice Collection of Muſick for the Harpſichord. N.B. Ladies and Gentlemen may be ſupplied at their own Houſes.
Thoſe who pleaſe to favour him with their Commands may depend upon being ſerved with the utmoſt Care and Diſpatch.""",
          [('Cheapſide', 'long s (ſ)', 'the long s was used in non-final positions in print until about 1800'),
           ('Muſick', 'non-standard (pre-dictionary) spelling', '‘Musick’ keeps the -ck ending that Johnson retained but which later lost the k'),
           ('a large Parcel of the fineſt Tea, Coffee and Chocolate', 'capitalisation of common nouns', 'nouns such as ‘Parcel’, ‘Tea’ are capitalised'),
           ('lately imported', 'archaic lexis', '‘lately’ for ‘recently’ is now rare in this sense'),
           ('Thoſe who pleaſe to favour him with their Commands', 'politeness formula', 'deferential, elaborate phrasing typical of 18th-century commerce'),
           ('N.B.', 'Latin abbreviation', '‘nota bene’ reflects the prestige of Latin in written English'),
           ('To be SOLD', 'graphological emphasis', 'capitals in print draw attention, as in modern adverts')],
          'For sale at the Golden Lion, Cheapside: the finest tea, coffee and chocolate, recently imported, at reasonable prices. Also a selection of harpsichord music. Home delivery available …'),
    HText('an entry from a traveller’s journal', '1790', 'Early Modern English', """
We set out betimes, the Road being exceeding bad by reason of the late Rains. The Coachman, a surly Fellow, would not be perswaded
to drive faster than a Walk, whereat my Companion was much vexed. About Noon we reached an Inn, where we dined very indifferently
upon a Fowl that had seen better Days. ’Tis a pity the Country is so ill provided with good Roads, for the Prospect is uncommon fine.""",
          [('We set out betimes', 'archaic lexis', '‘betimes’ (early) has fallen out of use'),
           ('exceeding bad', 'adjective used as an adverb intensifier', '‘exceeding’ without -ly as an intensifier, now non-standard'),
           ('would not be perswaded', 'non-standard (pre-dictionary) spelling', '‘perswaded’ is an older spelling of ‘persuaded’'),
           ('whereat my Companion was much vexed', 'archaic lexis', '‘whereat’ (at which) and ‘vexed’ (annoyed) are now formal or archaic'),
           ('’Tis a pity', 'archaic contraction', '‘’Tis’ (it is) is a contraction now found only in poetry or archaism'),
           ('uncommon fine', 'adjective used as an adverb intensifier', '‘uncommon’ for ‘uncommonly’'),
           ('dined very indifferently', 'semantic change', '‘indifferently’ here means ‘poorly’, a sense now less common'),
           ('the Road being exceeding bad', 'capitalisation of common nouns', '‘Road’, ‘Rains’, ‘Coachman’ are capitalised, though the practice was declining by 1790')],
          'We set out early, because the road was extremely bad after the recent rain. The coachman, a grumpy man, could not be persuaded to go faster than walking pace, which annoyed my companion …'),
    HText('instructions from a household management book', '1845', 'Late Modern English', """
The mistress of a household should rise early, for it is impossible that her servants should be punctual if she is not. The
breakfast-table must be laid by eight o'clock. Let the kitchen be inspected daily, and let no waste be suffered. Whilst the lady
need not herself perform menial tasks, she ought to understand them, that she may judge whether they are well done.""",
          [('should rise early', 'modal verb of obligation', 'deontic modals (should, must, ought to) give advice with moral authority'),
           ('Let the kitchen be inspected daily', 'let + passive imperative', 'an indirect, impersonal command structure now rare'),
           ('let no waste be suffered', 'semantic change', '‘suffered’ means ‘allowed’, a sense now archaic'),
           ('Whilst the lady', 'conjunction now declining', '‘whilst’ is declining in frequency in favour of ‘while’'),
           ('that she may judge', 'subjunctive / archaic purpose clause', '‘that she may’ for ‘so that she can’ is now formal'),
           ('breakfast-table', 'hyphenated compound', 'compounds often begin hyphenated and later close up or open (‘breakfast table’)'),
           ('her servants', 'social context', 'reference to servants reflects the class structure of Victorian households')],
          'Householders should get up early: staff will not be punctual otherwise. Breakfast must be laid by eight. Check the kitchen every day and do not allow waste …'),
]
HFEAT_POOL = ['non-standard (pre-dictionary) spelling', 'archaic second-person pronoun', '-eth third-person verb inflection', 'auxiliary do in a positive statement',
              'capitalisation of common nouns', 'long s (ſ)', 'archaic lexis', 'politeness formula', 'archaic contraction', 'semantic change', 'adjective used as an adverb intensifier',
              'archaic verb form', 'hyphenated compound', 'modal verb of obligation', 'conjunction now declining']
HFEATS = [(h, q, f, e) for h in HTEXTS for q, f, e in h.feats]
EVENTS = [
    ('the Norman Conquest', '1066', 'brought thousands of French words into English, especially in law, government, food and fashion (court, justice, beef, fashion)'),
    ('Viking settlement and the Danelaw', 'the 9th–11th centuries', 'introduced Old Norse words (sky, egg, knife, they, them) and may have hastened the loss of inflections'),
    ('William Caxton’s printing press in Westminster', '1476', 'spread a more uniform, south-east Midlands written standard and fixed many spellings'),
    ('the Great Vowel Shift', 'about 1400–1700', 'changed the pronunciation of long vowels, leaving many spellings out of step with speech'),
    ('the publication of the King James Bible', '1611', 'gave wide currency to fixed phrases and a formal, archaic style'),
    ('Samuel Johnson’s A Dictionary of the English Language', '1755', 'gave English an authoritative reference for spelling and meaning'),
    ('Robert Lowth’s A Short Introduction to English Grammar', '1762', 'promoted prescriptive rules such as avoiding double negatives'),
    ('Noah Webster’s An American Dictionary of the English Language', '1828', 'established American spellings such as ‘color’ and ‘center’'),
    ('the expansion of the British Empire', 'the 18th–19th centuries', 'brought borrowings from many languages, e.g. bungalow and pyjamas from Hindi/Urdu'),
    ('the invention of the World Wide Web', '1989–91', 'led to rapid neologism and new informal written registers'),
]
PERIOD_OF = [('Old English', 'about 450–1100'), ('Middle English', 'about 1100–1500'), ('Early Modern English', 'about 1500–1800'), ('Late Modern English', 'about 1800 to the present')]

# ---------------------------------------------------------------- 1.1 historical development
N11 = 'Historical development of English: Old, Middle, Early Modern and Late Modern English'
t11 = topic(N11, N11)
t11.fixed('C1', (1, 2), [
    ('Which period of English is roughly dated 1500–1800?', 'Early Modern English', 'OE c.450–1100; ME c.1100–1500; EME c.1500–1800; LME c.1800–present.', ['Old English', 'Middle English', 'Late Modern English']),
    ('Which event brought a large number of French words into English?', 'The Norman Conquest of 1066', 'Norman French became the language of the ruling class.', ['The invention of printing', 'The Viking invasions', 'The publication of the King James Bible']),
    ('Old English was a highly inflected language. What does this mean?', 'Word endings changed to show grammatical relationships such as case', 'Loss of inflections made word order more important.',
     ['It had no grammar', 'It used many loanwords', 'It was only spoken, never written']),
    ('Which letter, used in Old English, represents the sound ‘th’?', 'þ (thorn)', 'Thorn (þ) and eth (ð) represented th sounds.', ['ſ (long s)', 'æ (ash)', 'ȝ (yogh)']),
])


@t11.add('C1', (1, 2, 3))
def t11_event(r, D):
    ev, date, eff = r.choice(EVENTS)
    others = [e for e in EVENTS if e[0] != ev]
    if r.random() < 0.5:
        opts, ans = mcq(r, date, list({x[1] for x in others}))
        return {'stem': f'When did {ev} take place?', 'options': opts, 'answer': ans, 'key': f'{cap(ev)} ({date}) {eff}.'}
    opts, ans = mcq(r, cap(ev), [cap(x[0]) for x in others])
    return {'stem': f'Which development {eff}?', 'options': opts, 'answer': ans, 'key': f'{cap(ev)}, {date}.'}


@t11.add('C1', (1, 2, 3))
def t11_hfeat(r, D):
    h, q, f, e = r.choice(HFEATS)
    opts, ans = mcq(r, cap(f), [cap(x) for x in HFEAT_POOL if x != f])
    return {'stem': f'In {h.label} ({h.date}), the writer writes {Q(q)}. Which feature of earlier English does this show?', 'options': opts, 'answer': ans, 'key': f'{cap(f)}: {e}.'}


@t11.add('C2', (1, 2, 3, 4), 'explain')
def t11_why(r, D):
    ev, date, eff = r.choice(EVENTS)
    m = marks('C2', D)
    return {'stem': f'Explain the significance of {ev} ({date}) in the history of English.', 'answer': f'It {eff}.',
            'key': pts_key(m, [f'identifies the effect: {eff}', 'gives an example word or feature', 'links to the period or to later developments (e.g. standardisation, lexical expansion)'])
            , 'marks': m}


@t11.add('C2', (1, 2, 3, 4), 'explain')
def t11_feat_explain(r, D):
    h, q, f, e = r.choice(HFEATS)
    m = marks('C2', D)
    return {'stem': f'In {h.label} ({h.date}), the writer writes {Q(q)}. Identify one feature that differs from present-day English and explain the change.', 'answer': f'{cap(f)}: {e}.',
            'key': pts_key(m, [f'identifies the feature ({f})', f'explains it: {e}', 'gives the present-day equivalent or a reason for the change']), 'marks': m}


@t11.add('C3', (2, 3, 4, 5), 'explain')
def t11_analyse(r, D):
    h = r.choice(HTEXTS)
    n = 2 + (D >= 3) + (D >= 5)
    m = marks('C3', D)
    return {'stem': f'{h.show()} Identify {NUMW[n]} features of {h.period} in this text and explain how each differs from present-day English.',
            'answer': ' '.join(f'{Q(q)} – {f}: {e}.' for q, f, e in h.feats[:n]), 'key': pts_key(m, [f'{Q(q)} ({f}): {e}' for q, f, e in h.feats]), 'marks': m}


@t11.add('C3', (2, 3, 4, 5), 'multi_step')
def t11_compose(r, D):
    h = r.choice(HTEXTS)
    a, b, c = r.sample(h.feats, 3)
    parts = [
        lambda r: (f'Give the present-day English equivalent of {Q(a[0])}.', f'See: {h.modern}', '1 mark accurate modernisation [1]'),
        lambda r: (f'Identify the feature in {Q(b[0])}.', cap(b[1]), f'1 mark: {b[1]} [1]'),
        lambda r: (f'Explain why {Q(c[0])} would be unusual today.', cap(c[2]), '1 mark feature; 1 mark explanation [2]'),
        lambda r: ('Using evidence from the text, explain which period of English it belongs to.', f'{h.period}: e.g. {Q(a[0])}, {Q(b[0])}.', '1 mark period; 2 marks evidence [3]'),
    ]
    return compose(r, h.show(), parts, k=(2, 3, 4), type_='multi_step')


@t11.add('C4', (2, 3, 4, 5), 'long')
def t11_long(r, D):
    h = r.choice(HTEXTS)
    ind = '; '.join(f'{Q(q)} ({f}): {e}' for q, f, e in h.feats) + f'; context: {h.date}, before/after standardisation; modern version: {h.modern}'
    task = r.choice(['Analyse ways in which this text exemplifies the characteristics of English of its period. Refer to specific details from the text.',
                     'Analyse how this text differs from present-day English in lexis, grammar, orthography and discourse, and explain the reasons for the differences.'])
    return essay(r, D, f'{h.show()} {task}', ind, kind='p3')


# ---------------------------------------------------------------- 1.2 lexical change
N12 = 'Lexical change: borrowing, coinage, compounding, blending, semantic shift'
t12 = topic(N12, N12)
PROC = ['borrowing', 'blending', 'clipping', 'acronym', 'initialism', 'conversion', 'compounding', 'affixation', 'eponym', 'back-formation', 'coinage']
SEM = ['broadening', 'narrowing', 'amelioration', 'pejoration']
WORDS = [
    ('brunch', 'blending', 'breakfast + lunch'), ('smog', 'blending', 'smoke + fog'), ('podcast', 'blending', 'iPod + broadcast'), ('motel', 'blending', 'motor + hotel'),
    ('emoticon', 'blending', 'emotion + icon'), ('bus', 'clipping', 'shortened from omnibus'), ('flu', 'clipping', 'shortened from influenza'), ('lab', 'clipping', 'shortened from laboratory'),
    ('exam', 'clipping', 'shortened from examination'), ('laser', 'acronym', 'light amplification by stimulated emission of radiation, pronounced as a word'),
    ('scuba', 'acronym', 'self-contained underwater breathing apparatus, pronounced as a word'), ('NATO', 'acronym', 'North Atlantic Treaty Organization, pronounced as a word'),
    ('BBC', 'initialism', 'each letter is pronounced separately'), ('URL', 'initialism', 'uniform resource locator, letters pronounced separately'),
    ('to text', 'conversion', 'the noun ‘text’ used as a verb'), ('to friend', 'conversion', 'the noun ‘friend’ used as a verb on social media'), ('a must', 'conversion', 'the modal ‘must’ used as a noun'),
    ('to google', 'conversion', 'a brand name used as a verb'), ('laptop', 'compounding', 'lap + top'), ('skyscraper', 'compounding', 'sky + scraper'), ('smartphone', 'compounding', 'smart + phone'),
    ('unfriend', 'affixation', 'prefix un- added to friend'), ('microplastic', 'affixation', 'prefix micro- added to plastic'), ('retweet', 'affixation', 'prefix re- added to tweet'),
    ('sandwich', 'eponym', 'named after the Earl of Sandwich'), ('cardigan', 'eponym', 'named after the Earl of Cardigan'), ('boycott', 'eponym', 'named after Captain Charles Boycott'),
    ('to edit', 'back-formation', 'formed by removing -or from editor'), ('to babysit', 'back-formation', 'formed from babysitter'), ('to burgle', 'back-formation', 'formed from burglar'),
    ('pyjamas', 'borrowing', 'from Hindi/Urdu'), ('tsunami', 'borrowing', 'from Japanese'), ('algebra', 'borrowing', 'from Arabic'), ('ballet', 'borrowing', 'from French'),
    ('kindergarten', 'borrowing', 'from German'), ('safari', 'borrowing', 'from Swahili'), ('robot', 'borrowing', 'from Czech'), ('yoghurt', 'borrowing', 'from Turkish'),
    ('blurb', 'coinage', 'invented by the humorist Gelett Burgess in the early 20th century'), ('googol', 'coinage', 'invented for the number 10 to the power 100'),
]
SWORDS = [
    ('holiday', 'broadening', 'once ‘holy day’, a religious festival; now any day off'), ('dog', 'broadening', 'once a particular breed; now any dog'),
    ('business', 'broadening', 'once ‘busyness’, the state of being busy; now commerce in general'), ('meat', 'narrowing', 'once any food; now animal flesh'),
    ('deer', 'narrowing', 'once any animal; now a particular animal'), ('girl', 'narrowing', 'once a young person of either sex; now a female child'),
    ('hound', 'narrowing', 'once any dog; now a hunting dog'), ('nice', 'amelioration', 'once ‘foolish’ or ‘ignorant’; now ‘pleasant’'),
    ('pretty', 'amelioration', 'once ‘cunning’ or ‘crafty’; now ‘attractive’'), ('sick', 'amelioration', 'in youth slang ‘excellent’, a positive shift from ‘ill’'),
    ('silly', 'pejoration', 'once ‘blessed’ or ‘innocent’; now ‘foolish’'), ('villain', 'pejoration', 'once a farm labourer; now a criminal'),
    ('awful', 'pejoration', 'once ‘inspiring awe’; now ‘very bad’'), ('naughty', 'pejoration', 'once ‘having nothing’ (poor); later ‘wicked’, now ‘badly behaved’'),
]
CAUSES = ['technological change', 'contact with other languages', 'social and cultural change', 'the influence of the media and the internet', 'the need for euphemism']
t12.fixed('C1', (1, 2), [
    ('What is semantic broadening?', 'A word’s meaning becoming more general over time', 'E.g. holiday: holy day → any day off.', ['A word’s meaning becoming more specific', 'A word becoming more positive', 'A word being shortened']),
    ('What is amelioration?', 'A word acquiring a more positive meaning over time', 'E.g. nice: foolish → pleasant.', ['A word acquiring a more negative meaning', 'A word disappearing', 'Two words combining']),
    ('What is the difference between an acronym and an initialism?', 'An acronym is pronounced as a word; an initialism is pronounced letter by letter', 'NATO (acronym) v. BBC (initialism).',
     ['There is no difference', 'An initialism is always longer', 'Acronyms are always borrowed words']),
    ('What is a neologism?', 'A newly coined word or expression', 'Neologisms are new words entering the language.', ['An obsolete word', 'A word borrowed from Latin', 'A spelling mistake']),
])


@t12.add('C1', (1, 2, 3))
def t12_proc(r, D):
    w, p, why = r.choice(WORDS)
    ex = {'acronym': ['initialism'], 'initialism': ['acronym'], 'conversion': ['eponym'], 'eponym': ['conversion']}.get(p, [])
    opts, ans = mcq(r, cap(p), [cap(x) for x in PROC if x != p and x not in ex])
    return {'stem': f'Which word-formation process produced {Q(w)}?', 'options': opts, 'answer': ans, 'key': f'{cap(p)}: {why}.'}


@t12.add('C1', (1, 2, 3))
def t12_sem(r, D):
    w, p, why = r.choice(SWORDS)
    opts, ans = mcq(r, cap(p), [cap(x) for x in SEM if x != p] + ['Clipping'])
    return {'stem': f'The word {Q(w)} has changed in meaning: {why.split(";")[0]}. Which type of semantic change is this?', 'options': opts, 'answer': ans, 'key': f'{cap(p)}: {why}.'}


@t12.add('C2', (1, 2, 3, 4), 'explain')
def t12_explain(r, D):
    m = marks('C2', D)
    if r.random() < 0.5:
        w, p, why = r.choice(WORDS)
        return {'stem': f'Explain how the word {Q(w)} was formed and suggest one reason why such words enter the language.', 'answer': f'{cap(p)}: {why}.',
                'key': pts_key(m, [f'identifies the process ({p})', f'explains the formation ({why})', f'a plausible cause, e.g. {r.choice(CAUSES)}']), 'marks': m}
    w, p, why = r.choice(SWORDS)
    return {'stem': f'Explain the semantic change shown by {Q(w)}.', 'answer': f'{cap(p)}: {why}.',
            'key': pts_key(m, [f'names the change ({p})', f'describes the earlier and current meanings ({why})', 'suggests a reason (e.g. social attitudes, metaphor, euphemism, overuse)']), 'marks': m}


@t12.add('C3', (1, 2, 3, 4, 5), 'explain')
def t12_classify(r, D):
    n = 3 + (D >= 3) + (D >= 5)
    picks = r.sample(WORDS, n - 1) + [r.choice(SWORDS)]
    r.shuffle(picks)
    m = marks('C3', D)
    who = person(r)
    return {'stem': f'{who} has collected these words while investigating lexical change: ' + ', '.join(Q(w) for w, _, _ in picks) +
            '. For each word, identify the process of lexical or semantic change and explain how it applies.',
            'answer': ' '.join(f'{Q(w)}: {p} ({why}).' for w, p, why in picks), 'key': pts_key(m, [f'{Q(w)} – {p}: {why}' for w, p, why in picks]), 'marks': m}


NEW_WORDS = ['doomscrolling', 'staycation', 'to ghost', 'influencer', 'hangry', 'vlog', 'to livestream', 'cancel culture']
NW_INFO = {'doomscrolling': 'compounding (doom + scrolling)', 'staycation': 'blending (stay + vacation)', 'to ghost': 'conversion and semantic shift (noun → verb, ‘to cut off contact’)',
           'influencer': 'affixation and semantic broadening (influence + -er, now a social-media role)', 'hangry': 'blending (hungry + angry)', 'vlog': 'blending/clipping (video + blog)',
           'to livestream': 'compounding and conversion (live + stream, used as a verb)', 'cancel culture': 'compounding with semantic shift of ‘cancel’'}


@t12.add('C4', (2, 3, 4, 5), 'multi_step')
def t12_new(r, D):
    ws = r.sample(NEW_WORDS, 3)
    m = marks('C4', D)
    return {'stem': f'The following words have entered English in the 21st century: ' + ', '.join(Q(w) for w in ws) + '. Analyse how each was formed and evaluate what these words suggest about the causes of lexical change today.',
            'answer': ' '.join(f'{Q(w)}: {NW_INFO[w]}.' for w in ws) + ' They reflect technology, social media and changing social practices.',
            'key': pts_key(m, [f'{Q(w)}: {NW_INFO[w]}' for w in ws] + ['causes: technology and the internet', 'causes: social and cultural change', 'evaluation, e.g. speed of spread through social media; some words may not last']), 'marks': m}


@t12.add('C4', (2, 3, 4, 5), 'long')
def t12_long(r, D):
    title = r.choice(['‘The main driver of lexical change today is technology.’ Discuss this view, referring to a range of examples and ideas about language change.',
                      'Discuss the ways in which English has expanded its vocabulary over time, evaluating the importance of borrowing compared with other processes.',
                      'Discuss the view that semantic change reflects changes in society, with reference to examples and research.'])
    ind = 'processes: borrowing (pyjamas, tsunami), compounding, blending (brunch, podcast), clipping, acronyms, conversion (to google), affixation, eponyms; semantic change (broadening, narrowing, amelioration, pejoration); causes: technology, contact, social change, media; evaluation of relative importance; recent examples.'
    return essay(r, D, title, ind)


# ---------------------------------------------------------------- 1.3 orthographic and grammatical change; standardisation
N13 = 'Orthographic and grammatical change; standardisation and Johnson\'s dictionary'
t13 = topic(N13, N13)
t13.fixed('C1', (1, 2), [
    ('When was Samuel Johnson’s A Dictionary of the English Language published?', '1755', 'Johnson’s dictionary (1755) became the standard authority for spelling for over a century.', ['1476', '1611', '1828']),
    ('Who introduced the printing press to England?', 'William Caxton', 'Caxton set up his press in Westminster in 1476.', ['Samuel Johnson', 'Robert Lowth', 'Noah Webster']),
    ('What is meant by ‘standardisation’?', 'The process by which one variety becomes accepted as the norm for spelling, grammar and usage', 'Standardisation involves selection, codification, elaboration and acceptance.',
     ['The invention of new words', 'The loss of all regional dialects', 'Translating texts into English']),
    ('Which 18th-century grammarian is known for prescriptive rules such as condemning double negatives?', 'Robert Lowth', 'Lowth’s Short Introduction to English Grammar (1762) was influential and prescriptive.', ['Geoffrey Chaucer', 'Jean Aitchison', 'David Crystal']),
    ('By about which date had the long s (ſ) largely disappeared from printed English?', 'About 1800', 'Printers abandoned the long s around the turn of the 19th century.', ['About 1500', 'About 1650', 'About 1950']),
])
CHANGES = [
    ('thou hast', 'you have', 'grammatical', 'loss of the second-person singular pronoun and its verb ending'), ('he maketh', 'he makes', 'grammatical', 'replacement of -eth by -s for the third person'),
    ('I doe beleeve', 'I believe', 'grammatical', 'loss of unstressed periphrastic do in statements, and spelling standardisation'), ('the house is building', 'the house is being built', 'grammatical', 'rise of the progressive passive in the 19th century'),
    ('publick', 'public', 'orthographic', 'loss of the final -k after Johnson’s era'), ('shew', 'show', 'orthographic', 'standardisation of an older spelling'),
    ('compleat', 'complete', 'orthographic', 'a variant spelling replaced by the standard form'), ('ſtreet', 'street', 'orthographic', 'loss of the long s around 1800'),
    ('to-day', 'today', 'orthographic', 'a hyphenated compound closing up'), ('Whom did you see?', 'Who did you see?', 'grammatical', 'decline of ‘whom’ in informal usage'),
    ('Shall I open the window?', 'Should I open the window? / Do you want me to open the window?', 'grammatical', 'decline of ‘shall’, especially outside British English'),
    ('If I were you', 'If I was you', 'grammatical', 'decline of the subjunctive ‘were’ in informal speech'),
]


@t13.add('C1', (1, 2, 3))
def t13_kind(r, D):
    old, new, kind, why = r.choice(CHANGES)
    opts, ans = mcq(r, cap(kind) + ' change', ['Lexical change (borrowing)', 'Semantic change', 'Phonological change only'])
    return {'stem': f'Earlier English {Q(old)} has become {Q(new)}. What kind of change is this?', 'options': opts, 'answer': ans, 'key': f'{cap(kind)} change: {why}.'}


fixed_c2(t13, [
    ('Explain why Johnson’s Dictionary was important in the standardisation of English.', 'It codified spelling and meanings, providing an authority used by printers, schools and writers.',
     ['codified spelling and meaning (about 40,000 entries)', 'used illustrative quotations from literature as authority', 'adopted by printers, schools and publishers', 'reduced variation in spelling (though not all spellings were rational)']),
    ('Explain how the printing press contributed to standardisation.', 'Printing spread a single written variety widely and encouraged consistent spellings.',
     ['mass production of identical texts', 'spread of the London/south-east Midlands variety', 'printers’ house styles fixed spellings', 'some spellings fixed before the Great Vowel Shift ended, so spelling and sound diverged']),
    ('Explain why English spelling is often said to be irregular.', 'Spelling was fixed by printing and dictionaries while pronunciation continued to change, and borrowings kept foreign spellings.',
     ['spellings fixed before or during the Great Vowel Shift', 'borrowings keep their original spellings', 'etymological respellings (e.g. debt with b)', 'printers’ practices']),
    ('Explain what is meant by ‘codification’ in standardisation.', 'Recording a variety’s rules in authoritative dictionaries and grammars.',
     ['definition: setting down norms in reference works', 'example: Johnson’s Dictionary (1755)', 'example: Lowth’s Grammar (1762)', 'effect: creates a prescriptive standard']),
    ('Explain why prescriptive 18th-century grammarians objected to double negatives.', 'They applied logic and Latin grammar, arguing that two negatives cancel out.',
     ['influence of Latin as a model', 'appeal to mathematical logic', 'association of double negatives with non-standard speech and lower social status', 'yet double negatives had been normal in Chaucer’s English']),
])


@t13.add('C2', (2, 3, 4), 'explain')
def t13_change(r, D):
    old, new, kind, why = r.choice(CHANGES)
    m = marks('C2', D)
    return {'stem': f'Explain the {kind} change from {Q(old)} to {Q(new)}.', 'answer': cap(why) + '.',
            'key': pts_key(m, [f'describes the change ({why})', 'identifies the approximate period', 'suggests a cause (standardisation, simplification, analogy, social attitudes)']), 'marks': m}


@t13.add('C3', (2, 3, 4, 5), 'short')
def t13_modernise(r, D):
    h = r.choice(HTEXTS)
    m = marks('C3', D)
    n = 2 + (D >= 4)
    return {'stem': f'{h.show()} Rewrite the first two sentences in present-day standard English, and explain {NUMW[n]} of the orthographic or grammatical changes you made.',
            'answer': f'Model: {h.modern} Changes: ' + '; '.join(f'{f} ({Q(q)})' for q, f, _ in h.feats[:n]) + '.',
            'key': pts_key(m, ['accurate modernisation'] + [f'{Q(q)}: {f} – {e}' for q, f, e in h.feats]), 'marks': m}


@t13.add('C3', (1, 2, 3, 4), 'explain')
def t13_set(r, D):
    picks = r.sample(CHANGES, 2 + (D >= 3))
    m = marks('C3', D)
    return {'stem': 'For each pair below, state whether the change is orthographic or grammatical and explain it: ' + ' '.join(f'({i + 1}) {Q(a)} → {Q(b)}' for i, (a, b, _, _) in enumerate(picks)),
            'answer': ' '.join(f'({i + 1}) {k}: {w}.' for i, (_, _, k, w) in enumerate(picks)), 'key': pts_key(m, [f'({i + 1}) {k} – {w}' for i, (_, _, k, w) in enumerate(picks)]), 'marks': m}


@t13.add('C4', (2, 3, 4, 5), 'long')
def t13_long(r, D):
    title = r.choice(['‘Standardisation has made English a more precise language.’ Discuss.', 'Discuss the role of printing, dictionaries and grammars in the standardisation of English.',
                      'To what extent did eighteenth-century attempts to fix English succeed? Refer to examples of orthographic and grammatical change.'])
    ind = 'Caxton 1476 and printing; Johnson 1755 (codification, but his Preface accepted that language cannot be fixed); Lowth 1762 and prescriptive grammar; Webster 1828; examples: long s, capitalised nouns, -eth → -s, thou → you, do-support, progressive passive; continuing change (whom, shall, subjunctive); evaluation of precision v. prestige.'
    return essay(r, D, title, ind)


# ---------------------------------------------------------------- 1.4 n-gram graphs and corpus data
N14 = 'Using n-gram graphs and corpus data to analyse change'
t14 = topic(N14, N14)
NG = [  # (older form, newer form, years, reason)
    ('e-mail', 'email', (1995, 2000, 2005, 2010, 2015), 'hyphenated compounds tend to close up as they become familiar'),
    ('on-line', 'online', (1990, 1995, 2000, 2005, 2010), 'the compound closed up as the internet became everyday'),
    ('to-day', 'today', (1880, 1900, 1920, 1940, 1960), 'the hyphen was dropped as the compound became fully lexicalised'),
    ('shew', 'show', (1700, 1740, 1780, 1820, 1860), 'spelling was standardised through dictionaries and printing'),
    ('musick', 'music', (1700, 1730, 1760, 1790, 1820), 'the -ck spelling was abandoned as printers standardised spelling'),
    ('connexion', 'connection', (1800, 1850, 1900, 1950, 2000), 'the Latin-influenced spelling gave way to the more regular form'),
    ('web site', 'website', (1995, 2000, 2005, 2010, 2015), 'the open compound closed up with frequent use'),
    ('whilst', 'while', (1800, 1850, 1900, 1950, 2000), 'the -st form has declined, especially in American English, though it survives in British usage'),
]


def ng_data(r, item):
    old, new, yrs, why = item
    a0 = r.randint(30, 90) * 1.0
    b0 = r.randint(2, 12) * 1.0
    olds, news = [], []
    fo, fn = r.uniform(0.45, 0.7), r.uniform(1.6, 2.6)
    for i in range(5):
        olds.append(round(a0 * fo ** i, 1))
        news.append(round(b0 * fn ** i, 1))
    if not any(o > n for o, n in zip(olds, news)) or not any(n > o for o, n in zip(olds, news)):
        return None
    return olds, news


def ng_table(item, olds, news):
    old, new, yrs, _ = item
    rows = '; '.join(f'{y}: {Q(old)} {o}, {Q(new)} {n}' for y, o, n in zip(yrs, olds, news))
    return f'A student’s simplified n-gram data show the frequency per million words of {Q(old)} and {Q(new)} in a corpus of published texts. {rows}.'


t14.fixed('C1', (1, 2), [
    ('What does an n-gram viewer graph usually show?', 'The relative frequency of a word or phrase in a large corpus over time', 'Frequency is normally given per million words (or as a percentage) by year.',
     ['How a word is pronounced', 'The meaning of a word in each year', 'The number of speakers of English']),
    ('Why are corpus frequencies usually given ‘per million words’?', 'So that frequencies can be compared fairly across corpora or years of different sizes', 'Normalising removes the effect of corpus size.',
     ['Because a million is the size of every corpus', 'To make the numbers larger', 'Because rare words are ignored']),
    ('Which is a limitation of n-gram data drawn from published books?', 'It under-represents informal and spoken language', 'Published books favour formal written usage and educated writers.', ['It includes every word ever spoken', 'It cannot show change over time', 'It shows only spoken data']),
    ('In corpus linguistics, what is a collocate?', 'A word that frequently occurs near another word', 'E.g. ‘strong’ collocates with ‘coffee’.', ['A word with the same meaning', 'A word that is spelled the same', 'A word borrowed from another language']),
])


@t14.add('C1', (1, 2, 3))
def t14_read(r, D):
    item = r.choice(NG)
    d = ng_data(r, item)
    if not d:
        return None
    olds, news = d
    yrs = item[2]
    i = next(k for k in range(5) if news[k] > olds[k])
    opts, ans = mcq(r, f'Between {yrs[i - 1]} and {yrs[i]}', [f'Between {yrs[j - 1]} and {yrs[j]}' for j in range(1, 5) if j != i] + [f'Before {yrs[0]}', f'After {yrs[4]}'])
    return {'stem': ng_table(item, olds, news) + f' Between which two dates did {Q(item[1])} first become more frequent than {Q(item[0])}?', 'options': opts, 'answer': ans,
            'key': f'In {yrs[i - 1]} {Q(item[0])} ({olds[i - 1]}) was ahead; by {yrs[i]} {Q(item[1])} ({news[i]}) had overtaken it ({olds[i]}).'}


@t14.add('C2', (1, 2, 3, 4), 'explain')
def t14_limit(r, D):
    m = marks('C2', D)
    item = r.choice(NG)
    q = r.choice([f'A student concludes from n-gram data that nobody uses {Q(item[0])} any more. Explain two reasons why this conclusion may be unreliable.',
                  f'Explain two limitations of using an n-gram viewer to investigate the change from {Q(item[0])} to {Q(item[1])}.'])
    return {'stem': q, 'answer': 'The corpus is mainly published writing, so informal, spoken and online usage is under-represented; OCR errors, genre bias and house styles can distort frequencies.',
            'key': pts_key(m, ['corpus is mostly published books, not speech or informal writing', 'OCR (scanning) errors, e.g. long s read as f', 'publishers’ house styles may impose spellings', 'genre or regional imbalance in the corpus', 'frequency shows use, not attitudes or meaning']), 'marks': m}


@t14.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_pm(r, D):
    size = r.choice([150, 200, 250, 360, 450, 520, 800])
    rate = round(r.uniform(0.5, 40.0), 1)
    count = round(rate * size)
    w = r.choice(['selfie', 'whilst', 'amongst', 'awesome', 'gonna', 'innit', 'hashtag', 'thou'])
    pm = count / size
    m = marks('C3', D)
    stem = f'In a {size}-million-word corpus, the word {Q(w)} occurs {count:,} times. Calculate its frequency per million words.'
    ans = f'{count:,} ÷ {size} = {pm:.2f} per million words.'
    if D >= 3:
        size2 = r.choice([x for x in (100, 120, 300, 400, 600) if x != size])
        count2 = round(r.uniform(0.5, 40.0) * size2)
        pm2 = count2 / size2
        stem += f' In a second, {size2}-million-word corpus from a later period, it occurs {count2:,} times. Calculate the percentage change in frequency per million between the two corpora, and comment on what the data suggest.'
        ans += f' Later: {count2:,} ÷ {size2} = {pm2:.2f}. Change = ({pm2:.2f} − {pm:.2f}) ÷ {pm:.2f} × 100 = {pct(pm, pm2):+.1f}%.'
    return {'stem': stem, 'answer': ans, 'key': f'{upto(m)}: method (count ÷ corpus size in millions) and correct values; ' + ('percentage change correctly calculated; a valid comment (e.g. rising/falling use, possible register differences between corpora).' if D >= 3 else 'answer to 2 decimal places.'),
            'marks': m}


@t14.add('C3', (2, 3, 4, 5), 'multi_step')
def t14_compose(r, D):
    item = r.choice(NG)
    d = ng_data(r, item)
    if not d:
        return None
    olds, news = d
    old, new, yrs, why = item
    i, j = 0, 4
    ch = pct(news[i], news[j])
    co = pct(olds[i], olds[j])
    ratio = news[4] / olds[4]
    parts = [
        lambda r: (f'Describe the trend in the frequency of {Q(old)}.', f'It falls steadily from {olds[0]} to {olds[4]} per million.', '1 mark direction; 1 mark data [2]'),
        lambda r: (f'Calculate the percentage change in the frequency of {Q(new)} between {yrs[i]} and {yrs[j]}.', f'({news[j]} − {news[i]}) ÷ {news[i]} × 100 = {ch:+.1f}%',
                   '1 mark method; 1 mark answer [2]'),
        lambda r: (f'Calculate the percentage change in the frequency of {Q(old)} between {yrs[i]} and {yrs[j]}.', f'({olds[j]} − {olds[i]}) ÷ {olds[i]} × 100 = {co:+.1f}%',
                   '1 mark method; 1 mark answer [2]'),
        lambda r: (f'How many times more frequent is {Q(new)} than {Q(old)} in {yrs[4]}? Give your answer to 1 decimal place.', f'{news[4]} ÷ {olds[4]} = {ratio:.1f} times', '1 mark method; 1 mark answer [2]'),
        lambda r: ('Suggest a reason for the change shown.', cap(why) + '.', '1 mark reason; 1 mark development [2]'),
    ]
    return compose(r, ng_table(item, olds, news), parts, k=(2, 3, 4), type_='multi_step')


@t14.add('C4', (2, 3, 4, 5), 'long')
def t14_long(r, D):
    h = r.choice(HTEXTS)
    item = r.choice(NG[3:6] if h.date < '1800' else NG[:3] + NG[6:])
    d = ng_data(r, item)
    if not d:
        return None
    olds, news = d
    ind = '; '.join(f'{Q(q)} ({f}): {e}' for q, f, e in h.feats[:5]) + f'; n-gram data: {Q(item[0])} falls from {olds[0]} to {olds[4]} while {Q(item[1])} rises from {news[0]} to {news[4]} per million ({item[3]}); links between text features and the data; limitations of corpus evidence.'
    return essay(r, D, f'{h.show()} {ng_table(item, olds, news)} Analyse ways in which the text and the data show changes in English over time. Refer to specific details from both.', ind, kind='p3')


# ---------------------------------------------------------------- 1.5 attitudes to change
N15 = 'Attitudes to language change: prescriptivism and descriptivism (Aitchison)'
t15 = topic(N15, N15)
ATT = [
    ('Young people today cannot write a proper sentence; text messaging is destroying English.', 'prescriptive', 'it judges change as decline and assumes a fixed correct standard'),
    ('Language changes because the needs of its speakers change; no variety is inherently better than another.', 'descriptive', 'it observes and explains change without judging it'),
    ('It is simply wrong to split an infinitive.', 'prescriptive', 'it states a rule as absolute, regardless of actual usage'),
    ('Corpus data show that ‘less’ is now widely used with plural nouns in informal speech.', 'descriptive', 'it reports usage from evidence'),
    ('We should protect English from the flood of American words.', 'prescriptive', 'it treats change as a threat to be resisted'),
    ('Dictionaries should record how people actually use words, including slang.', 'descriptive', 'it supports recording usage rather than regulating it'),
    ('Using ‘literally’ to mean ‘figuratively’ is lazy and incorrect.', 'prescriptive', 'it condemns a semantic change as laziness'),
    ('The spread of ‘like’ as a discourse marker performs useful functions such as quoting and hedging.', 'descriptive', 'it analyses the functions of a new usage'),
    ('Standards are slipping: in my day, everyone knew the difference between ‘fewer’ and ‘less’.', 'prescriptive', 'it looks back to a supposed golden age'),
    ('Every generation complains about the language of the next; such complaints are part of a long tradition.', 'descriptive', 'it takes a historical, non-judgemental view'),
]
AITCH = [
    ('People drop their consonants because they can’t be bothered to speak properly.', 'damp spoon syndrome', 'it blames change on laziness, like leaving a damp spoon in the sugar bowl'),
    ('English was at its finest in the age of Shakespeare and has been decaying ever since.', 'crumbling castle', 'it imagines a past perfect state now crumbling'),
    ('These American phrases are spreading through our schools like a virus.', 'infectious disease', 'it presents new usages as an infection caught from others'),
    ('Teenagers are too lazy to pronounce the t in ‘water’.', 'damp spoon syndrome', 'it attributes a phonological change to laziness'),
    ('Our beautiful language is being eroded, stone by stone.', 'crumbling castle', 'it uses the image of a once-perfect structure decaying'),
    ('Text-speak is an epidemic that children catch from their phones.', 'infectious disease', 'it describes change as a contagious illness'),
]
t15.fixed('C1', (1, 2), [
    ('What is a prescriptive approach to language?', 'One that sets rules for how language should be used and judges usage as correct or incorrect', 'Prescriptivism lays down norms; descriptivism records usage.',
     ['One that records how language is actually used', 'One that studies only spoken language', 'One that studies only historical texts']),
    ('Which linguist identified the ‘damp spoon’, ‘crumbling castle’ and ‘infectious disease’ metaphors of language decline?', 'Jean Aitchison', 'Aitchison described these metaphors in her 1996 Reith Lectures.',
     ['Noam Chomsky', 'Samuel Johnson', 'William Labov']),
    ('What is Aitchison’s own view of language change?', 'Change is natural and inevitable, neither progress nor decay', 'Aitchison argues that change is driven by speakers’ needs, not laziness.',
     ['Change is always a sign of decay', 'Change can be stopped by education', 'Change happens only in writing']),
    ('Which of these is a descriptivist activity?', 'Recording how a word is actually used in a large corpus', 'Descriptivists gather evidence of usage.', ['Banning a word from a school essay', 'Writing a rule that forbids split infinitives', 'Correcting a newspaper’s grammar']),
])


@t15.add('C1', (1, 2, 3))
def t15_att(r, D):
    if r.random() < 0.5:
        s, lab, why = r.choice(AITCH)
        opts, ans = mcq(r, cap(lab), ['Damp spoon syndrome', 'Crumbling castle', 'Infectious disease', 'Descriptivism'])
        return {'stem': f'Which of Aitchison’s metaphors for attitudes to language change best fits this comment? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(lab)}: {why}.'}
    s, lab, why = r.choice(ATT)
    opts, ans = mcq(r, cap(lab), ['Prescriptive', 'Descriptive', 'Neither: it is about pronunciation only', 'Neither: it is a factual definition'])
    return {'stem': f'Is this comment prescriptive or descriptive? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(lab)}: {why}.'}


@t15.add('C2', (1, 2, 3, 4), 'explain')
def t15_explain(r, D):
    s, lab, why = r.choice(ATT + AITCH)
    m = marks('C2', D)
    who = r.choice(['a letter to a newspaper', 'a radio phone-in', 'a linguistics textbook', 'an online comment thread', 'a teacher’s blog', 'a dictionary editor’s blog'])
    return {'stem': f'This comment appeared in {who}: {Q(s)} Explain the attitude to language change it shows.', 'answer': f'{cap(lab)}: {why}.',
            'key': pts_key(m, [f'identifies the attitude ({lab})', f'explains with reference to the wording ({why})', 'links to a relevant idea (e.g. Aitchison, prescriptivism v. descriptivism, Swift, Johnson, Crystal)']), 'marks': m}


LETTERS = [
    ('Sir, I was appalled to hear a newsreader say ‘less people’ last night. If the national broadcaster cannot uphold standards, who will? Our language is crumbling before our eyes, and nobody seems to care.',
     ['prescriptive complaint about ‘less’ with count nouns', 'appeal to authority (the broadcaster as guardian of standards)', 'crumbling castle metaphor (‘crumbling before our eyes’)', 'rhetorical question', 'emotive lexis (‘appalled’)']),
    ('Dear Editor, my grandson says everything is ‘literally’ amazing. Literally! These young people are infecting each other with sloppy speech picked up from the internet.',
     ['prescriptive objection to semantic change of ‘literally’', 'infectious disease metaphor (‘infecting’)', 'blames the internet and youth', 'exclamatory repetition', 'generalisation from one example']),
    ('I am tired of hearing people say ‘gonna’ and ‘wanna’. It is pure laziness: they simply cannot be bothered to pronounce the words properly.',
     ['prescriptive view of phonological reduction', 'damp spoon syndrome (laziness)', 'ignores that assimilation/elision are natural in fluent speech', 'confuses informal speech with incorrect speech']),
    ('Teachers should stop marking down students who end sentences with prepositions. That ‘rule’ was invented by Latin-loving grammarians and has never matched how English speakers actually talk.',
     ['descriptive stance', 'historical awareness (18th-century Latin-based rules)', 'appeal to actual usage', 'challenges prescriptive authority']),
]


@t15.add('C3', (2, 3, 4, 5), 'explain')
def t15_letter(r, D):
    txt, pts = r.choice(LETTERS)
    m = marks('C3', D)
    return {'stem': f'Read this extract from a letter to a newspaper: {Q(txt)} Analyse the attitudes to language change expressed, and the language used to express them, with reference to relevant ideas.',
            'answer': '; '.join(cap(x) for x in pts) + '.', 'key': pts_key(m, pts + ['reference to a relevant theorist or idea (e.g. Aitchison)']), 'marks': m}


@t15.add('C3', (1, 2, 3, 4), 'explain')
def t15_sort(r, D):
    picks = r.sample(ATT, 3 + (D >= 3))
    m = marks('C3', D)
    return {'stem': 'Classify each comment as prescriptive or descriptive and give a reason: ' + ' '.join(f'({i + 1}) {Q(s)}' for i, (s, _, _) in enumerate(picks)),
            'answer': ' '.join(f'({i + 1}) {lab}: {why}.' for i, (_, lab, why) in enumerate(picks)), 'key': pts_key(m, [f'({i + 1}) {lab} – {why}' for i, (_, lab, why) in enumerate(picks)]), 'marks': m}


@t15.add('C4', (2, 3, 4, 5), 'long')
def t15_long(r, D):
    txt, pts = r.choice(LETTERS)
    title = r.choice(['Discuss attitudes to language change, referring to this extract and to ideas and research you have studied.',
                      '‘Language change is a sign of decline.’ Using the extract as a starting point, discuss this view.',
                      'Evaluate prescriptive and descriptive approaches to language change, with reference to the extract.'])
    ind = '; '.join(pts) + '; Aitchison’s metaphors (damp spoon, crumbling castle, infectious disease); Swift (1712), Johnson (1755, Preface), Lowth (1762); descriptivist responses (Crystal, Aitchison); change as natural and functional; the social role of standards.'
    return essay(r, D, f'Read this extract from a letter to a newspaper: {Q(txt)} {title}', ind)


CHAPTERS[1] = [t11, t12, t13, t14, t15]


# =========================================================== 2 Child language acquisition

STAGES = [('pre-verbal (cooing and babbling)', '0–12 months'), ('holophrastic (one-word)', '12–18 months'), ('two-word', '18–24 months'), ('telegraphic', '24–36 months'), ('post-telegraphic', '36 months +')]
UTTS = [
    ('[cooing] ooo (.) aah', 'pre-verbal (cooing and babbling)', 'vowel-like comfort sounds before babbling (about 6–8 weeks onwards)'),
    ('ba ba ba ba', 'pre-verbal (cooing and babbling)', 'reduplicated (canonical) babbling of consonant–vowel syllables (about 6–8 months)'),
    ('ba da gu', 'pre-verbal (cooing and babbling)', 'variegated babbling: different syllables combined'),
    ('juice ↗', 'holophrastic (one-word)', 'a single word with rising intonation functioning as a request (‘Can I have juice?’)'),
    ('up', 'holophrastic (one-word)', 'a one-word utterance carrying a whole meaning (‘pick me up’)'),
    ('daddy car', 'two-word', 'two content words in a possessor–possessed or agent–object relation'),
    ('more milk', 'two-word', 'a pivot word (‘more’) with an open-class word'),
    ('no bed', 'two-word', 'negation placed before the word (Bellugi stage 1)'),
    ('me want biscuit', 'telegraphic', 'content words in order, function words (do, a) omitted, object pronoun for subject'),
    ('doggy run fast', 'telegraphic', 'subject–verb–adverbial with no inflections or auxiliaries'),
    ('where mummy going', 'telegraphic', 'wh-question without auxiliary (‘is’)'),
    ('I goed to the park and I sawed a duck', 'post-telegraphic', 'clause coordination and full sentence structure, with virtuous errors (goed, sawed)'),
    ('can I have the red one because mine is broken', 'post-telegraphic', 'auxiliary inversion in a question and subordination with ‘because’'),
    ('the mans are fixing the road', 'post-telegraphic', 'progressive aspect and auxiliary, with an overgeneralised plural'),
]
# utterance tokens with morpheme boundaries (+) for MLU (Brown's rules: inflections count; compounds, diminutives and irregular pasts count as one)
MLU_UTT = ['daddy go+ing', 'dog+s run', 'more juice', 'mummy shoe', 'teddy fall+ed down', 'me want biscuit', 'baby cry+ing', 'where ball', 'big truck', 'kitty eat+ing fish',
           'no bath', 'that mine', 'car+s go fast', 'I jump+ed', 'doggy bark+s', 'want milk', 'look bird+s', 'all gone', 'grandma come+s', 'me do it', 'red one', 'he kick+ed ball',
           'two cat+s', 'went park', 'birthday cake']
BROWN = [(1.0, 2.0, 'Stage I'), (2.0, 2.5, 'Stage II'), (2.5, 3.0, 'Stage III'), (3.0, 3.75, 'Stage IV'), (3.75, 4.5, 'Stage V')]


def morphs(u):
    return sum(1 + w.count('+') for w in u.split(' '))


def plain(u):
    return u.replace('+', '')


# ---------------------------------------------------------------- 2.1 stages
N21 = 'Stages of spoken language development: pre-verbal to post-telegraphic'
t21 = topic(N21, N21)
t21.fixed('C1', (1, 2), [
    ('At about what age do most children produce their first recognisable words?', 'About 12 months', 'The holophrastic stage begins around 12 months.', ['About 3 months', 'About 30 months', 'About 4 years']),
    ('What is a holophrase?', 'A single word that expresses a whole idea or sentence', 'E.g. ‘juice’ meaning ‘I want juice’.', ['A two-word utterance', 'A babbled syllable', 'A question with an auxiliary verb']),
    ('What is MLU?', 'Mean length of utterance, usually measured in morphemes', 'MLU = total morphemes ÷ number of utterances (Brown, 1973).', ['Maximum length of utterance', 'Morphemes learnt per year', 'A test of vocabulary size']),
    ('Which feature characterises telegraphic speech?', 'Content words in order with function words and inflections omitted', 'E.g. ‘me want biscuit’.', ['Single words only', 'Babbling', 'Fully formed complex sentences']),
    ('What is the typical order of the pre-verbal stage?', 'Crying, cooing, babbling', 'Babies cry from birth, coo from about 6–8 weeks and babble from about 6 months.', ['Babbling, crying, cooing', 'Cooing, crying, babbling', 'Babbling, cooing, crying']),
])


@t21.add('C1', (1, 2, 3))
def t21_stage(r, D):
    u, st, why = r.choice(UTTS)
    opts, ans = mcq(r, cap(st), [cap(s) for s, _ in STAGES if s != st])
    who = person(r)
    return {'stem': f'{who}, a young child, says: {Q(u)} Which stage of development does this utterance most clearly show?', 'options': opts, 'answer': ans, 'key': f'{cap(st)}: {why}.'}


@t21.add('C2', (1, 2, 3, 4), 'explain')
def t21_explain(r, D):
    u, st, why = r.choice(UTTS)
    m = marks('C2', D)
    return {'stem': f'A child says {Q(u)}. Explain which stage of development this suggests, referring to features of the utterance.', 'answer': f'{cap(st)}: {why}.',
            'key': pts_key(m, [f'identifies the stage ({st})', f'refers to a specific feature ({why})', 'gives a typical age range or contrasts with the next stage']), 'marks': m}


@t21.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_mlu(r, D):
    n = 4 + D
    us = r.sample(MLU_UTT, n)
    tot = sum(morphs(u) for u in us)
    mlu = tot / n
    if any(abs(mlu - b) < 0.005 for lo, hi, _ in BROWN for b in (lo, hi)):
        return None
    stage = next((s for lo, hi, s in BROWN if lo <= mlu < hi), None)
    who = person(r)
    m = marks('C3', D)
    stem = (f'These are {n} utterances recorded from {who}, aged about two: ' + ' | '.join(Q(plain(u)) for u in us) +
            '. Using Brown’s rules (count each word and each inflection such as plural -s, -ing and regular -ed as a morpheme; compounds, diminutives and irregular past forms count as one), calculate the mean length of utterance (MLU) in morphemes to 2 decimal places.')
    ans = f'Morphemes: ' + ', '.join(f'{plain(u)} = {morphs(u)}' for u in us) + f'. Total {tot} ÷ {n} = {mlu:.2f}.'
    if D >= 3 and stage:
        stem += ' Then state which of Brown’s stages this MLU suggests.'
        ans += f' This falls in Brown’s {stage}.'
    return {'stem': stem, 'answer': ans, 'key': f'{upto(m)}: correct morpheme counts (e.g. ' + '; '.join(f'{u.replace("+", " + ")} = {morphs(u)}' for u in us[:3]) + f'); total {tot}; MLU {mlu:.2f}' +
            (f'; {stage}' if D >= 3 and stage else '') + '.', 'marks': m}


@t21.add('C3', (2, 3, 4, 5), 'multi_step')
def t21_compose(r, D):
    a, b, c = r.sample(UTTS, 3)
    parts = [
        lambda r: (f'Identify the stage shown by {Q(a[0])}.', cap(a[1]), f'1 mark: {a[1]} [1]'),
        lambda r: (f'Explain one feature of {Q(b[0])} that is typical of its stage.', f'{cap(b[1])}: {b[2]}.', '1 mark feature; 1 mark explanation [2]'),
        lambda r: (f'Give the typical age range for the stage shown by {Q(c[0])}.', dict(STAGES)[c[1]], '1 mark [1]'),
        lambda r: (f'Explain how {Q(c[0])} differs from the stage before it.', f'{cap(c[2])}.', '1 mark difference; 2 marks development with reference to the utterance [3]'),
    ]
    return compose(r, f'Three utterances were recorded from children of different ages: (i) {Q(a[0])} (ii) {Q(b[0])} (iii) {Q(c[0])}.', parts, k=(2, 3, 4), type_='multi_step')


@t21.add('C4', (2, 3, 4, 5), 'long')
def t21_long(r, D):
    title = r.choice(['Discuss the extent to which children’s spoken language develops through clearly defined stages. Refer to examples and research.',
                      '‘Ages and stages give a misleadingly neat picture of child language development.’ Discuss.'])
    ind = 'pre-verbal (crying, cooing, babbling: reduplicated and variegated); holophrastic (12–18 months); two-word (18–24); telegraphic (24–36); post-telegraphic (36+); MLU and Brown’s stages; individual variation; stages overlap; comprehension precedes production; evaluation of stage models.'
    return stim_essay(r, D, title, ind)


# ---------------------------------------------------------------- 2.2 theories
N22 = 'Theories of acquisition: behaviourist (Skinner), nativist (Chomsky), cognitive (Piaget)'
t22 = topic(N22, N22)
THEORIES = ['behaviourist', 'nativist', 'cognitive', 'interactionist']
TH_ITEMS = [
    ('Children learn language by imitating adults and being rewarded for correct forms.', 'behaviourist', 'imitation and operant conditioning (Skinner, 1957)'),
    ('Every child is born with a language acquisition device.', 'nativist', 'Chomsky’s LAD and innate universal grammar'),
    ('Children cannot use language to express concepts they have not yet understood.', 'cognitive', 'Piaget: language follows cognitive development (e.g. object permanence)'),
    ('Caregivers support children by framing routines such as reading picture books together.', 'interactionist', 'Bruner’s LASS and scaffolding'),
    ('The input children hear is too messy and incomplete to explain the grammar they acquire.', 'nativist', 'the poverty of the stimulus argument'),
    ('A child praised for saying ‘milk’ is more likely to say it again.', 'behaviourist', 'positive reinforcement'),
    ('Children only use words like ‘bigger’ once they understand the concept of comparison.', 'cognitive', 'cognition precedes language'),
    ('A child can do with help today what they will do alone tomorrow.', 'interactionist', 'Vygotsky’s zone of proximal development'),
    ('Children across cultures pass through similar stages at similar ages.', 'nativist', 'evidence for an innate, universal capacity'),
    ('Children produce ‘I goed’, a form they have never heard adults use.', 'nativist', 'virtuous errors suggest rule formation, not imitation'),
]
EVID = [
    ('Berko’s ‘wug’ test (1958): children produced ‘wugs’ for a nonsense creature they had never seen', 'supports nativist / rule-based accounts', 'children apply plural rules productively rather than imitating'),
    ('Braine’s ‘other one spoon’ example: a child could not reproduce ‘the other spoon’ despite repeated correction', 'challenges behaviourism', 'correction and imitation did not change the child’s output'),
    ('the case of Genie, who was isolated until 13 and never fully acquired grammar', 'supports the critical period hypothesis (Lenneberg)', 'suggests a biological window for acquisition, though her abuse complicates the evidence'),
    ('children’s virtuous errors such as ‘mouses’ and ‘runned’', 'challenges behaviourism', 'adults do not model these forms, so they cannot be imitated'),
    ('children whose parents use more expansions and recasts often develop vocabulary faster', 'supports interactionist accounts', 'interaction quality appears to matter'),
    ('children using words such as ‘gone’ once they understand object permanence', 'supports cognitive theory (Piaget)', 'language appears linked to cognitive milestones'),
    ('children learning accents, vocabulary and politeness routines from their families', 'supports behaviourism in part', 'imitation clearly plays a role in some aspects of language'),
]
t22.fixed('C1', (1, 2), [
    ('Which theorist is associated with the language acquisition device (LAD)?', 'Noam Chomsky', 'Chomsky proposed an innate LAD and universal grammar.', ['B. F. Skinner', 'Jean Piaget', 'Jerome Bruner']),
    ('Which theory explains language acquisition through imitation and reinforcement?', 'Behaviourism', 'Skinner’s Verbal Behavior (1957).', ['Nativism', 'Cognitive theory', 'Interactionism']),
    ('What does the ‘poverty of the stimulus’ argument claim?', 'The language children hear is not rich enough to explain the grammar they acquire', 'This supports an innate capacity.', ['Poor children learn language more slowly', 'Children need no input at all', 'Stimulus–response learning explains everything']),
    ('According to Piaget, what is the relationship between language and thought?', 'Cognitive development comes first and language follows', 'Children talk about concepts once they understand them.', ['Language creates all thought', 'They are unrelated', 'Language is fully innate']),
    ('What is the critical period hypothesis?', 'There is a limited window in childhood during which language is acquired most easily', 'Associated with Lenneberg (1967).', ['Children must start school by age five', 'Language is learnt only after puberty', 'Every child learns at the same speed']),
])


@t22.add('C1', (1, 2, 3))
def t22_th(r, D):
    s, th, why = r.choice(TH_ITEMS)
    opts, ans = mcq(r, cap(th), [cap(x) for x in THEORIES if x != th])
    return {'stem': f'Which theory of language acquisition does this statement best reflect? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(th)}: {why}.'}


@t22.add('C2', (1, 2, 3, 4), 'explain')
def t22_evid(r, D):
    ev, verdict, why = r.choice(EVID)
    m = marks('C2', D)
    return {'stem': f'Explain how {ev} can be used as evidence in the debate about how children acquire language.', 'answer': f'It {verdict}: {why}.',
            'key': pts_key(m, ['describes the evidence accurately', f'links it to a theory ({verdict})', f'explains why ({why})', 'notes a limitation of the evidence']), 'marks': m}


@t22.add('C2', (2, 3, 4), 'explain')
def t22_contrast(r, D):
    a, b = r.sample(['behaviourist', 'nativist', 'cognitive'], 2)
    m = marks('C2', D)
    desc = {'behaviourist': 'imitation and reinforcement (Skinner)', 'nativist': 'an innate capacity, the LAD and universal grammar (Chomsky)', 'cognitive': 'language following cognitive development (Piaget)'}
    return {'stem': f'Explain one key difference between the {a} and {b} explanations of child language acquisition.', 'answer': f'The {a} view stresses {desc[a]}; the {b} view stresses {desc[b]}.',
            'key': pts_key(m, [f'accurate summary of the {a} view', f'accurate summary of the {b} view', 'a clear point of difference, ideally with an example']), 'marks': m}


@t22.add('C3', (2, 3, 4, 5), 'explain')
def t22_apply(r, D):
    T = r.choice(TRANSCRIPTS)
    m = marks('C3', D)
    return {'stem': f'{T.show()} Explain how features of this transcript could be used to support or challenge two theories of language acquisition.',
            'answer': ' '.join(f'{Q(q)} ({f}): {th}.' for q, f, _, th in T.feats[:3]),
            'key': pts_key(m, [f'{Q(q)} ({f}) – {th}' for q, f, _, th in T.feats] + ['balanced evaluation of the theories']), 'marks': m}


@t22.add('C4', (2, 3, 4, 5), 'long')
def t22_long(r, D):
    title = r.choice(['Evaluate the view that children acquire language mainly through imitation.', '‘Children are born to talk.’ To what extent do you agree?',
                      'Compare and evaluate nativist and cognitive explanations of how children acquire language.'])
    ind = 'Skinner (1957): imitation, operant conditioning, reinforcement; counter-evidence: virtuous errors, Braine’s ‘other one spoon’; Chomsky: LAD, universal grammar, poverty of the stimulus, Berko’s wug test; Piaget: cognition first, object permanence; critical period (Lenneberg, Genie); interactionist alternatives (Bruner, Vygotsky); evaluation and synthesis.'
    return stim_essay(r, D, title, ind)


# ---------------------------------------------------------------- 2.3 interactionist theory and CDS
N23 = 'Interactionist theory and child-directed speech (Bruner, Vygotsky)'
t23 = topic(N23, N23)
CDS_POOL = ['expansion', 'recast', 'repetition', 'simplified lexis', 'exaggerated intonation', 'use of the child’s name instead of a pronoun', 'questions to prompt a response', 'praise (positive reinforcement)']
CDS = [
    ('CHILD: doggy run / MOTHER: yes, the doggy is running', 'expansion', 'the adult expands the telegraphic utterance into a full grammatical sentence'),
    ('CHILD: I goed there / FATHER: oh, you went there, did you?', 'recast', 'the adult rephrases the error correctly without explicitly correcting it'),
    ('MOTHER: ball (.) ball (.) where’s the ball (.) there’s the ball', 'repetition', 'repeating the key word helps the child segment and remember it'),
    ('FATHER: look at the moo-cow', 'simplified lexis', 'a simple, child-friendly word is used'),
    ('MOTHER: [high pitch] ooh WHAT’S that ↗', 'exaggerated intonation', 'high pitch and exaggerated rise attract attention'),
    ('MOTHER: Mummy’s going to get your coat now', 'use of the child’s name instead of a pronoun', 'third-person names avoid the complexity of pronouns'),
    ('FATHER: what’s this (.) is it a cat or a dog', 'questions to prompt a response', 'questions give the child a turn and scaffold an answer'),
    ('MOTHER: clever girl (.) yes that’s a cup', 'praise (positive reinforcement)', 'praise rewards the child’s attempt'),
    ('CHILD: me falled / GRANDMA: you fell over? oh dear', 'recast', 'the adult provides the correct irregular past tense in a natural response'),
    ('CHILD: car / FATHER: a big red car', 'expansion', 'the adult extends the holophrase into a noun phrase'),
]
t23.fixed('C1', (1, 2), [
    ('What is LASS?', 'Bruner’s language acquisition support system: the support caregivers give through interaction and routines', 'LASS complements Chomsky’s LAD.', ['A test of vocabulary', 'A stage of babbling', 'A type of overextension']),
    ('What is Vygotsky’s zone of proximal development?', 'The gap between what a child can do alone and what they can do with help from a more knowledgeable other', 'Scaffolding works within the ZPD.',
     ['The age at which talking begins', 'The part of the brain used for language', 'The time a child spends babbling']),
    ('What is scaffolding?', 'Temporary support from an adult that is gradually withdrawn as the child becomes more capable', 'Associated with Bruner (Wood, Bruner and Ross, 1976).', ['Correcting every error', 'Leaving the child to learn alone', 'A type of phonological error']),
    ('Which feature is typical of child-directed speech?', 'Higher pitch and exaggerated intonation', 'CDS also uses repetition, simple lexis and short utterances.', ['Long, complex sentences', 'Technical vocabulary', 'Fast speech without pauses']),
])
cls_templates(t23, [(CDS_POOL, CDS, 'Which feature of child-directed speech is shown? {q}')], c2_ctx=['In this exchange between a caregiver and a two-year-old', 'This was recorded at a family mealtime', 'This exchange took place during a bath-time routine'])


@t23.add('C3', (2, 3, 4, 5), 'explain')
def t23_analyse(r, D):
    picks = r.sample(CDS, 2 + (D >= 3))
    m = marks('C3', D)
    return {'stem': 'Analyse the features of child-directed speech in these exchanges and explain how each might support the child’s development, with reference to interactionist theory: ' +
            ' '.join(f'({i + 1}) {Q(s)}' for i, (s, _, _) in enumerate(picks)),
            'answer': ' '.join(f'({i + 1}) {lab}: {why}.' for i, (_, lab, why) in enumerate(picks)),
            'key': pts_key(m, [f'({i + 1}) {lab} – {why}' for i, (_, lab, why) in enumerate(picks)] + ['link to Bruner (LASS, scaffolding) or Vygotsky (ZPD, MKO)']), 'marks': m}


@t23.add('C4', (2, 3, 4, 5), 'long')
def t23_long(r, D):
    title = r.choice(['‘Interaction with caregivers is essential for language acquisition.’ Discuss.', 'Evaluate the contribution of child-directed speech to children’s language development.',
                      'To what extent do interactionist theories provide a more complete account of acquisition than nativist theories?'])
    ind = 'Bruner: LASS, routines, scaffolding; Vygotsky: ZPD, MKO; CDS features (pitch, repetition, expansions, recasts, questions); evidence: cultures with little CDS still acquire language (e.g. Schieffelin’s Kaluli study); cases of deprivation; balance with nativist accounts; evaluation.'
    return stim_essay(r, D, title, ind)


# ---------------------------------------------------------------- 2.4 analysing transcripts
N24 = 'Analysing transcripts of child language: overextension, virtuous errors'
t24 = topic(N24, N24)


class Tr:
    def __init__(self, label, age, text, feats):
        self.label, self.age = label, age
        self.text = clean(sq(text))
        self.feats = [(sq(q), f, e, th) for q, f, e, th in feats]
        for q, *_ in self.feats:
            assert q in self.text, q

    def show(self):
        return f'Read this transcript of {self.label}; the child is {self.age}. (Key: (.) micropause; CAPITALS = stress; [ ] non-verbal; C = child.) {Q(self.text)}'


TRANSCRIPTS = [
    Tr('Ravi and his mother looking at a picture book', '2 years 3 months', """
MOTHER: what's that Ravi C: doggy MOTHER: no (.) that's a horse (.) a HORSE C: horse (.) big doggy horse MOTHER: yes it's a big horse (.) what's the
horse doing C: horse eat MOTHER: that's right (.) the horse is eating grass C: me eat grass [laughs] MOTHER: no (.) you don't eat grass silly""",
       [('C: doggy', 'categorical overextension', 'the child extends ‘doggy’ to another four-legged animal', 'supports cognitive views: the child is forming categories'),
        ('big doggy horse', 'telegraphic utterance', 'content words without function words', 'typical of the telegraphic stage'),
        ('horse eat', 'omission of inflection', 'the -ing ending and auxiliary are missing', 'shows grammar still developing'),
        ('the horse is eating grass', 'expansion (CDS)', 'the mother expands ‘horse eat’ into a full sentence', 'supports interactionist accounts'),
        ('me eat grass', 'object pronoun for subject', '‘me’ used for ‘I’', 'common pronoun error before case is mastered'),
        ('a HORSE', 'prosodic stress (CDS)', 'the mother stresses the correct word', 'scaffolding through emphasis'),
        ("what's the horse doing", 'question to prompt a response', 'the mother gives the child a turn', 'Bruner’s scaffolding')]),
    Tr('Mei talking to her father after nursery', '3 years 6 months', """
FATHER: what did you do today C: we goed to the garden and I digged a hole FATHER: you dug a hole (.) wow C: yeah and there was two mouses (.) no (.) two
mices FATHER: two mice C: two mice (.) they runned away FATHER: they ran away did they C: yeah (.) Miss Ana said they was scared of me""",
       [('we goed', 'virtuous error (overgeneralised -ed)', 'regular past-tense rule applied to an irregular verb', 'suggests rule formation (nativist)'),
        ('I digged a hole', 'virtuous error (overgeneralised -ed)', 'the -ed rule applied to ‘dig’', 'challenges imitation-based accounts'),
        ('you dug a hole', 'recast (CDS)', 'the father models the correct form without correcting explicitly', 'interactionist support'),
        ('two mouses (.) no (.) two mices', 'self-repair with overgeneralised plural', 'the child applies the plural rule, then attempts a double-marked form', 'shows active hypothesis-testing'),
        ('two mice (.) they runned away', 'uptake then a new virtuous error', 'the child imitates ‘mice’ but overgeneralises ‘runned’', 'imitation explains some forms but not others'),
        ('they was scared', 'subject–verb agreement error', '‘was’ with a plural subject', 'may reflect developing grammar or local dialect input')]),
    Tr('Lucas and his grandmother at bath time', '1 year 10 months', """
GRANDMA: where's your duck Lucas C: duck (.) gone GRANDMA: gone (.) where's it gone C: der GRANDMA: there it is (.) clever boy C: more bubble
GRANDMA: more bubbles (.) okay (.) here we go C: [splashes] wet GRANDMA: yes you're all wet""",
       [('duck (.) gone', 'two-word utterance', 'object + state, showing object permanence', 'supports Piaget: ‘gone’ appears with object permanence'),
        ('C: der', 'phonological substitution', '/d/ replaces /ð/ in ‘there’', 'typical substitution of an easier sound'),
        ('more bubble', 'pivot grammar / two-word', 'pivot word ‘more’ with an open word, plural -s omitted', 'Braine’s pivot schema'),
        ('clever boy', 'praise (CDS)', 'the grandmother rewards the child’s answer', 'supports behaviourist reinforcement'),
        ('more bubbles (.) okay', 'expansion (CDS)', 'the grandmother adds the plural', 'interactionist scaffolding'),
        ('C: [splashes] wet', 'holophrase', 'one word describing the situation', 'holophrastic stage persisting alongside two-word utterances')]),
    Tr('Amara and her older brother playing with toy cars', '2 years 8 months', """
BROTHER: whose car is this C: mine car BROTHER: it's MY car (.) you've got the blue one C: no (.) me want red (.) no blue BROTHER: okay have
the red one C: red one go fast (.) brrm BROTHER: why's it go fast C: cos it big wheels""",
       [('mine car', 'pronoun error', '‘mine’ used as a determiner for ‘my’', 'shows developing pronoun system'),
        ('no (.) me want red (.) no blue', 'negation with ‘no’ at the front', 'Bellugi’s first stage of negation', 'stage-like development of negation'),
        ('red one go fast', 'telegraphic utterance', 'missing third-person -s and auxiliary', 'typical telegraphic stage'),
        ('brrm', 'onomatopoeia / sound play', 'imitation of engine noise', 'play and imitation'),
        ("why's it go fast", 'older sibling’s non-standard input', 'the brother’s question lacks do-support', 'input from siblings differs from adult CDS'),
        ('cos it big wheels', 'copula and possessive verb omission', '‘has’ is missing in a causal clause', 'emerging subordination with ‘cos’')]),
    Tr('Kwame and his mother at the supermarket', '2 years', """
MOTHER: look (.) apples C: ball MOTHER: no it's an apple (.) you eat it C: apple (.) eat MOTHER: yes (.) we'll eat it at home C: tato MOTHER: potato (.)
clever C: [points] moon MOTHER: that's a lamp darling (.) a round lamp""",
       [('C: ball', 'analogical overextension', 'the round apple is called ‘ball’ because of its shape', 'cognitive: categories based on perceptual features'),
        ('apple (.) eat', 'two-word utterance', 'object + action', 'two-word stage'),
        ('C: tato', 'deletion of unstressed syllable', 'the unstressed first syllable of potato is dropped', 'phonological simplification'),
        ('C: [points] moon', 'analogical overextension', '‘moon’ extended to a round lamp', 'shape-based overextension'),
        ("no it's an apple (.) you eat it", 'correction with explanation (CDS)', 'the mother corrects and explains function', 'interactionist teaching'),
        ('potato (.) clever', 'modelling and praise', 'the correct form is modelled and the attempt praised', 'behaviourist reinforcement')]),
]
FEATS24 = [(T, q, f, e, th) for T in TRANSCRIPTS for q, f, e, th in T.feats]
ERR = [
    ('A child calls every man ‘daddy’.', 'categorical overextension', 'a word is applied to a wider category than adults use'),
    ('A child calls the moon a ‘ball’.', 'analogical overextension', 'the extension is based on shape'),
    ('A child uses ‘cat’ only for the family pet, not other cats.', 'underextension', 'a word is applied too narrowly'),
    ('A child says ‘I swimmed’.', 'virtuous error', 'the regular -ed rule is applied to an irregular verb'),
    ('A child says ‘nana’ for banana.', 'deletion of unstressed syllable', 'the unstressed first syllable is dropped'),
    ('A child says ‘tat’ for cat.', 'phonological substitution', '/t/ replaces /k/ (fronting)'),
    ('A child says ‘poon’ for spoon.', 'consonant cluster reduction', 'the cluster /sp/ is reduced to /p/'),
    ('A child says ‘gog’ for dog.', 'assimilation', 'one consonant becomes like another in the word'),
    ('A child says ‘wawa’ for water.', 'reduplication', 'a syllable is repeated'),
    ('A child says ‘sheeps’.', 'virtuous error', 'the regular plural rule is overgeneralised'),
]
ERR_POOL = ['categorical overextension', 'analogical overextension', 'underextension', 'virtuous error', 'deletion of unstressed syllable', 'phonological substitution', 'consonant cluster reduction', 'assimilation', 'reduplication']
t24.fixed('C1', (1, 2), [
    ('What is a virtuous error?', 'An error that shows the child is applying a grammatical rule, such as ‘runned’', 'It is ‘virtuous’ because it reveals rule learning.', ['A polite request', 'Copying an adult mistake', 'A pronunciation error caused by missing teeth']),
    ('What is overextension?', 'Using a word for a wider range of things than adults do', 'E.g. ‘doggy’ for all animals.', ['Using a word too narrowly', 'Repeating a syllable', 'Speaking very loudly']),
    ('Which of these is an example of underextension?', 'Using ‘shoe’ only for the child’s own shoes', 'Underextension = too narrow.', ['Calling all men ‘daddy’', 'Saying ‘goed’', 'Saying ‘wawa’ for water']),
])
cls_templates(t24, [(ERR_POOL, ERR, 'Which feature of child language is shown? {q}')], c2_ctx=['A parent records this in a diary', 'A researcher notes this observation', 'This was observed at a nursery'])


def fgroup(f):
    if any(k in f for k in ('telegraphic', 'two-word', 'holophrase', 'pivot')):
        return 'stage'
    if 'overextension' in f:
        return 'ext'
    if any(k in f for k in ('CDS', 'praise', 'question to prompt', 'recast', 'expansion', 'modelling')):
        return 'cds'
    if any(k in f for k in ('virtuous', 'overgeneralised')):
        return 'virt'
    if any(k in f for k in ('pronoun', 'omission', 'agreement')):
        return 'gram'
    return f


@t24.add('C1', (1, 2, 3))
def t24_tr(r, D):
    T, q, f, e, th = r.choice(FEATS24)
    pool = sorted({x[2] for x in FEATS24 if x[2] != f and fgroup(x[2]) != fgroup(f)})
    opts, ans = mcq(r, cap(f), [cap(x) for x in pool])
    return {'stem': f'In a transcript of {T.label} (child aged {T.age}), the line {Q(q)} occurs. Which feature does it show?', 'options': opts, 'answer': ans, 'key': f'{cap(f)}: {e}.'}


@t24.add('C2', (1, 2, 3, 4), 'explain')
def t24_explain(r, D):
    T, q, f, e, th = r.choice(FEATS24)
    m = marks('C2', D)
    return {'stem': f'In a transcript of {T.label} (the child is {T.age}), the line {Q(q)} occurs. Explain what this shows about the child’s language development or the interaction.',
            'answer': f'{cap(f)}: {e}; {th}.', 'key': pts_key(m, [f'identifies the feature ({f})', f'explains it ({e})', f'links to theory or stage ({th})']), 'marks': m}


@t24.add('C3', (2, 3, 4, 5), 'explain')
def t24_analyse(r, D):
    T = r.choice(TRANSCRIPTS)
    n = 2 + (D >= 3) + (D >= 5)
    m = marks('C3', D)
    focus = r.choice(['the child’s language', 'the interaction between the speakers'])
    return {'stem': f'{T.show()} Analyse {NUMW[n]} features of {focus} in this transcript, explaining what each suggests about the child’s development.',
            'answer': ' '.join(f'{Q(q)} – {f}: {e}.' for q, f, e, _ in T.feats[:n]), 'key': pts_key(m, [f'{Q(q)} ({f}): {e}; {th}' for q, f, e, th in T.feats]), 'marks': m}


@t24.add('C3', (2, 3, 4, 5), 'multi_step')
def t24_compose(r, D):
    T = r.choice(TRANSCRIPTS)
    a, b, c = r.sample(T.feats, 3)
    parts = [
        lambda r: (f'Identify the feature shown in {Q(a[0])}.', cap(a[1]), f'1 mark: {a[1]} [1]'),
        lambda r: (f'Explain what {Q(b[0])} suggests about the child’s development.', f'{cap(b[2])}; {b[3]}.', '1 mark feature; 1 mark explanation [2]'),
        lambda r: (f'Explain how {Q(c[0])} could be used as evidence for a theory of acquisition.', f'{cap(c[3])}.', '1 mark theory; 2 marks explanation [3]'),
        lambda r: ('Identify one feature of the adult’s speech typical of child-directed speech.', 'E.g. expansion, recast, questions, praise, stress.', '1 mark feature; 1 mark example [2]'),
    ]
    return compose(r, T.show(), parts, k=(2, 3), type_='multi_step')


@t24.add('C4', (2, 3, 4, 5), 'long')
def t24_long(r, D):
    T = r.choice(TRANSCRIPTS)
    task = r.choice(['Analyse ways in which the speakers use language in this transcript. In your answer you should refer to specific details from the transcript as well as to ideas from your wider study of language acquisition.',
                     'Analyse what this transcript reveals about the child’s stage of development and the role of interaction, referring to relevant theories.'])
    ind = '; '.join(f'{Q(q)} ({f}): {e}; {th}' for q, f, e, th in T.feats) + f'; age {T.age} and expected stage; theories (Skinner, Chomsky, Piaget, Bruner, Vygotsky).'
    return essay(r, D, f'{T.show()} {task}', ind, kind='p3')


CHAPTERS[2] = [t21, t22, t23, t24]


# =========================================================== 3 English in the world

# ---------------------------------------------------------------- 3.1 Kachru
N31 = 'Global English: Kachru\'s concentric circles'
t31 = topic(N31, N31)
CIRCLE = {'inner circle': ['the United Kingdom', 'the United States', 'Australia', 'New Zealand', 'Ireland', 'Canada (English-speaking)'],
          'outer circle': ['India', 'Nigeria', 'Singapore', 'Kenya', 'the Philippines', 'Pakistan', 'Malaysia', 'Ghana'],
          'expanding circle': ['China', 'Japan', 'Brazil', 'Russia', 'Germany', 'Egypt', 'South Korea', 'Mexico']}
CDESC = {'inner circle': 'English is the primary, first language of most people (norm-providing)',
         'outer circle': 'English has an official or institutional role as a second language, often a legacy of colonialism (norm-developing)',
         'expanding circle': 'English is learnt as a foreign language, mainly for international communication (norm-dependent)'}
NORM = {'inner circle': 'norm-providing', 'outer circle': 'norm-developing', 'expanding circle': 'norm-dependent'}
t31.fixed('C1', (1, 2), [
    ('In which year did Braj Kachru publish his model of the three concentric circles of English?', '1985', 'Kachru’s model appeared in 1985.', ['1755', '1957', '2010']),
    ('Why are outer-circle countries described as ‘norm-developing’?', 'They are developing their own standards of English alongside inherited ones', 'E.g. Indian English and Singapore English norms.', ['They have no English speakers', 'They copy British norms exactly', 'They speak only pidgins']),
    ('Which is a common criticism of Kachru’s model?', 'It is based on geography and history rather than speakers’ actual proficiency and use', 'Critics note blurred boundaries and growth of English in the expanding circle.',
     ['It includes too few languages other than English', 'It is about child language', 'It ignores the United States']),
    ('Which linguist proposed an alternative model based on proficiency, with ‘international English’ at the centre?', 'Marko Modiano', 'Modiano (1999) placed proficient international users at the centre.', ['Noam Chomsky', 'William Labov', 'Deborah Tannen']),
])


@t31.add('C1', (1, 2, 3))
def t31_country(r, D):
    c = r.choice(list(CIRCLE))
    country = r.choice(CIRCLE[c])
    if r.random() < 0.5:
        opts, ans = mcq(r, cap(c), ['Inner circle', 'Outer circle', 'Expanding circle', 'Pidgin circle'])
        return {'stem': f'In Kachru’s model, which circle does {country} belong to?', 'options': opts, 'answer': ans, 'key': f'{cap(c)}: {CDESC[c]}.'}
    opts, ans = mcq(r, cap(NORM[c]), ['Norm-providing', 'Norm-developing', 'Norm-dependent', 'Norm-rejecting'])
    return {'stem': f'In Kachru’s terms, how would the English used in {country} be described?', 'options': opts, 'answer': ans, 'key': f'{country} is in the {c}: {CDESC[c]}.'}


@t31.add('C2', (1, 2, 3, 4), 'explain')
def t31_explain(r, D):
    c = r.choice(list(CIRCLE))
    country = r.choice(CIRCLE[c])
    m = marks('C2', D)
    return {'stem': f'Explain why {country} is placed in Kachru’s {c}, and what this suggests about the status of English there.', 'answer': cap(CDESC[c]) + '.',
            'key': pts_key(m, [f'correct description of the {c}', f'reason linked to {country} (history, official status or foreign-language learning)', f'the norm relationship ({NORM[c]})']), 'marks': m}


fixed_c2(t31, [
    ('Explain two criticisms of Kachru’s concentric circles model.', 'It is based on nation states rather than speakers, and boundaries are blurred (e.g. South Africa, Singapore).',
     ['nation-based rather than speaker-based', 'blurred boundaries (South Africa, Singapore, where many speak English as a first language)', 'implies inner-circle superiority', 'static: does not show movement between circles', 'ignores proficiency differences within countries']),
    ('Explain why the expanding circle may now contain more English users than the inner circle.', 'English is widely learnt as a foreign language in populous countries such as China and Brazil.',
     ['large populations learning English (China, Brazil)', 'English in education, business and the internet', 'estimates suggest non-native users outnumber native speakers']),
    ('Explain what is meant by ‘norm-providing’ in Kachru’s model.', 'Inner-circle varieties have traditionally provided the standards of grammar and pronunciation for learners.',
     ['definition', 'example (British or American standards in teaching)', 'consequence or challenge to the idea']),
])


@t31.add('C3', (1, 2, 3, 4, 5), 'explain')
def t31_sort(r, D):
    n = 3 + (D >= 3) + (D >= 5)
    pairs = []
    while len(pairs) < n:
        c = r.choice(list(CIRCLE))
        ctry = r.choice(CIRCLE[c])
        if ctry not in [p[1] for p in pairs]:
            pairs.append((c, ctry))
    m = marks('C3', D)
    return {'stem': 'Place each country in Kachru’s model and justify your answer: ' + ', '.join(p[1] for p in pairs) + '.' + (' Then identify one country that is difficult to place and explain why.' if D >= 4 else ''),
            'answer': ' '.join(f'{p[1]}: {p[0]} ({NORM[p[0]]}).' for p in pairs) + (' E.g. South Africa or Singapore, where many people speak English as a first language although it is historically an outer-circle country.' if D >= 4 else ''),
            'key': pts_key(m, [f'{p[1]} – {p[0]}' for p in pairs] + ['justifications refer to history, official status or foreign-language use'] + (['a valid problem case (e.g. South Africa, Singapore, Canada’s Quebec)'] if D >= 4 else [])), 'marks': m}


@t31.add('C4', (2, 3, 4, 5), 'long')
def t31_long(r, D):
    stim = r.choice(['A news report notes that more people now use English as a second or foreign language than as a first language.',
                     'A blogger from Singapore writes: ‘English is my first language, but your model calls me an outer-circle speaker.’',
                     'A language school advertises ‘Learn proper English from native speakers only.’'])
    title = r.choice(['Discuss how useful Kachru’s concentric circles model is for understanding English in the world today.', 'Evaluate the view that the idea of the ‘native speaker’ is no longer helpful for describing global English.'])
    ind = 'Kachru (1985): inner (norm-providing), outer (norm-developing), expanding (norm-dependent); strengths: simple, historical, highlights world Englishes; criticisms: nation-based, blurred boundaries, inner-circle bias, static; alternatives: Modiano (1999), McArthur’s circle of World English; ELF and non-native majority; evaluation.'
    return essay(r, D, f'{stim} {title}', ind)


# ---------------------------------------------------------------- 3.2 world Englishes, pidgins and creoles
N32 = 'World Englishes, pidgins and creoles'
t32 = topic(N32, N32)
VARS = ['Singapore English (Singlish)', 'Indian English', 'Nigerian English', 'Jamaican Creole', 'Tok Pisin']
VFEATS = [
    ('Can or not?', 'Singapore English (Singlish)', 'the ‘can or not’ tag question, a calque of Chinese structures'),
    ('This one very expensive lah.', 'Singapore English (Singlish)', 'copula deletion and the discourse particle ‘lah’'),
    ('I eat already.', 'Singapore English (Singlish)', '‘already’ used as a perfective marker (‘I have eaten’)'),
    ('Please do the needful.', 'Indian English', 'a fixed formal phrase meaning ‘please do what is necessary’'),
    ('The meeting has been preponed.', 'Indian English', '‘prepone’ (bring forward), formed by analogy with ‘postpone’'),
    ('I am knowing the answer.', 'Indian English', 'progressive aspect with a stative verb'),
    ('I will flash you when I arrive.', 'Nigerian English', '‘flash’ = give a missed call'),
    ('We were stuck in a go-slow for two hours.', 'Nigerian English', '‘go-slow’ = traffic jam'),
    ('Mi a go a market.', 'Jamaican Creole', '‘mi’ as subject pronoun and ‘a’ as a progressive marker'),
    ('Di pikni dem a play.', 'Jamaican Creole', 'plural marker ‘dem’ after the noun'),
    ('Mi go long haus sik.', 'Tok Pisin', '‘haus sik’ = hospital (house + sick)'),
    ('Tupela meri i kam.', 'Tok Pisin', 'the suffix -pela and the predicate marker ‘i’'),
]
PC = [
    ('A simplified contact language with no native speakers, used for trade between groups', 'pidgin', 'pidgins arise from contact and are nobody’s first language'),
    ('A contact language that has become the first language of a community', 'creole', 'a pidgin becomes a creole when children acquire it natively (nativisation)'),
    ('The variety in a creole continuum closest to the standard language', 'acrolect', 'the acrolect is the prestige, standard-like end'),
    ('The variety in a creole continuum furthest from the standard', 'basilect', 'the basilect is the most creole-like end'),
    ('Intermediate varieties in a creole continuum', 'mesolect', 'mesolects sit between the basilect and acrolect'),
    ('The process by which a creole moves towards the standard language', 'decreolisation', 'speakers shift towards the acrolect, often because of its prestige'),
    ('The language that supplies most of a pidgin’s vocabulary', 'lexifier (superstrate)', 'e.g. English for Tok Pisin'),
    ('The process by which a pidgin gains native speakers and grammatical complexity', 'creolisation', 'children expand the pidgin into a full language'),
]
PC_POOL = ['pidgin', 'creole', 'acrolect', 'basilect', 'mesolect', 'decreolisation', 'lexifier (superstrate)', 'creolisation']
t32.fixed('C1', (1, 2), [
    ('What is the main difference between a pidgin and a creole?', 'A creole has native speakers; a pidgin does not', 'Creoles develop when a pidgin is acquired as a first language.', ['A pidgin is older', 'A creole has no grammar', 'There is no difference']),
    ('Tok Pisin is an official language of which country?', 'Papua New Guinea', 'Tok Pisin is an English-lexified creole of Papua New Guinea.', ['Nigeria', 'Jamaica', 'Singapore']),
    ('What does the term ‘World Englishes’ emphasise?', 'That there are many legitimate varieties of English around the world', 'Associated with Kachru: Englishes in the plural.', ['That only British English is correct', 'That English is declining', 'That English has one global standard']),
])
cls_templates(t32, [(VARS, VFEATS, 'Which variety is this utterance most likely to come from? {q}')],
              c2_ctx=['This utterance was recorded in a study of world Englishes', 'A student found this example in a corpus of international English'])
cls_templates(t32, [(PC_POOL, PC, 'Which term matches this definition? {q}')], c2=False)


@t32.add('C3', (2, 3, 4, 5), 'explain')
def t32_analyse(r, D):
    picks = r.sample(VFEATS, 2 + (D >= 3) + (D >= 5))
    m = marks('C3', D)
    return {'stem': 'Analyse the linguistic features of these utterances and explain what they show about the development of new Englishes: ' + ' '.join(f'({i + 1}) {Q(s)} ({v})' for i, (s, v, _) in enumerate(picks)),
            'answer': ' '.join(f'({i + 1}) {w}.' for i, (_, _, w) in enumerate(picks)),
            'key': pts_key(m, [f'({i + 1}) {w}' for i, (_, _, w) in enumerate(picks)] + ['influence of substrate languages or local culture', 'new varieties are rule-governed, not ‘broken’ English']), 'marks': m}


@t32.add('C4', (2, 3, 4, 5), 'long')
def t32_long(r, D):
    s, v, w = r.choice(VFEATS)
    stim = f'A visitor to a country where {v} is spoken writes online: ‘I heard someone say {Q(s)} – they clearly can’t speak English properly.’'
    title = r.choice(['Discuss attitudes towards new varieties of English, with reference to the comment above and your wider study.', 'Discuss the development and status of pidgins, creoles and new Englishes.'])
    ind = f'{Q(s)}: {w}; features of Singlish, Indian, Nigerian English; pidgin → creole (nativisation), creole continuum (basilect, mesolect, acrolect), decreolisation; substrate influence; prestige and stigma (e.g. Speak Good English Movement in Singapore); covert prestige and identity; evaluation of the ‘broken English’ view.'
    return essay(r, D, f'{stim} {title}', ind)


# ---------------------------------------------------------------- 3.3 ELF, globalisation and the internet
N33 = 'English as a lingua franca, globalisation and the internet'
t33 = topic(N33, N33)
ELF = [
    ('She work in a bank in Frankfurt.', 'dropping third-person -s', 'a common ELF feature that rarely causes misunderstanding'),
    ('We need more informations about the shipment.', 'uncountable noun used as countable', '‘informations’ is common in ELF and transparent in meaning'),
    ('You are coming tomorrow, isn’t it?', 'invariant tag question', 'one tag used for all statements'),
    ('This is the man which I met.', 'interchangeable who/which', 'relative pronouns used without the human/non-human distinction'),
    ('We should discuss about the contract.', 'redundant preposition', '‘discuss about’ adds a preposition for explicitness'),
    ('Let’s make a discussion on Monday.', 'overuse of common verbs', '‘make’ used with a wide range of nouns'),
]
ELF_POOL = ['dropping third-person -s', 'uncountable noun used as countable', 'invariant tag question', 'interchangeable who/which', 'redundant preposition', 'overuse of common verbs']
t33.fixed('C1', (1, 2), [
    ('What is English as a lingua franca (ELF)?', 'English used as a common language between speakers who have different first languages', 'Most ELF interactions involve no native speakers.', ['English spoken only in the UK', 'A creole spoken in the Caribbean', 'The English of young children']),
    ('Who proposed the Lingua Franca Core for pronunciation?', 'Jennifer Jenkins', 'Jenkins (2000) identified features essential for intelligibility.', ['Robert Lowth', 'Jean Piaget', 'Penelope Brown']),
    ('Which corpus records spoken ELF interactions in Europe?', 'VOICE (Vienna-Oxford International Corpus of English)', 'Compiled under Barbara Seidlhofer.', ['The British National Corpus only', 'Johnson’s Dictionary', 'The Oxford English Dictionary']),
    ('In ELF research, what matters most?', 'Mutual intelligibility and communicative effectiveness', 'ELF research shifts focus from native-speaker correctness to intelligibility.', ['Imitating a British accent', 'Avoiding all errors', 'Using idioms']),
])
cls_templates(t33, [(ELF_POOL, ELF, 'Which ELF feature does this sentence show? {q}')], c2_ctx=['This was said in a business meeting between speakers from Brazil and Korea', 'This was written in an email between engineers in Germany and Indonesia'])
fixed_c2(t33, [
    ('Explain how the internet has contributed to the global spread of English.', 'English dominates much online content and platforms, and online communication spreads new forms quickly.',
     ['English as a dominant language of websites, software and platforms', 'global social media spreads neologisms quickly', 'online learning resources', 'growth of other languages online is reducing English’s share']),
    ('Explain why ELF speakers may find native speakers harder to understand than other ELF speakers.', 'Native speakers often use idioms, fast connected speech and cultural references unfamiliar to ELF users.',
     ['idioms and culture-specific references', 'fast speech with elision and weak forms', 'less accommodation to the listener', 'ELF users adapt and negotiate meaning']),
    ('Explain one way globalisation affects English and one way it affects other languages.', 'English spreads as a global lingua franca; other languages may lose domains of use.',
     ['English spreads in business, science, aviation and media', 'new varieties and hybrid forms develop', 'other languages lose domains (domain loss)', 'borrowing of English words into other languages']),
])


@t33.add('C3', (2, 3, 4, 5), 'explain')
def t33_exchange(r, D):
    a, b = person(r), person(r)
    picks = r.sample(ELF, 2 + (D >= 4))
    m = marks('C3', D)
    lines = ' '.join(f'{[a, b][i % 2]}: {Q(s)}' for i, (s, _, _) in enumerate(picks))
    ctx = r.choice(['an online meeting between engineers in two different countries', 'a conversation between exchange students at a university', 'a phone call between a supplier and a buyer'])
    return {'stem': f'This exchange took place during {ctx}; neither speaker has English as a first language: {lines} Analyse the ELF features and evaluate whether they would affect communication.',
            'answer': ' '.join(f'{Q(s)}: {lab} – {why}.' for s, lab, why in picks) + ' Meaning remains clear, so communication is likely to succeed.',
            'key': pts_key(m, [f'{Q(s)} – {lab}: {why}' for s, lab, why in picks] + ['evaluation: intelligibility rather than native-speaker correctness', 'reference to ELF research (Jenkins, Seidlhofer)']), 'marks': m}


@t33.add('C4', (2, 3, 4, 5), 'long')
def t33_long(r, D):
    title = r.choice(['‘English belongs to everyone who uses it.’ Discuss this view with reference to English as a lingua franca.', 'Discuss the impact of globalisation and the internet on English and its users.',
                      'Evaluate the view that learners should aim for intelligibility rather than native-speaker norms.'])
    ind = 'ELF: definition, Jenkins’ Lingua Franca Core, Seidlhofer and VOICE; typical ELF features (third-person -s, informations, isn’t it); ownership of English (Widdowson); internet: English online, netspeak (Crystal), spread of neologisms, growth of other languages online; globalisation in business, science and media; evaluation of standards v. intelligibility.'
    return essay(r, D, title, ind)


# ---------------------------------------------------------------- 3.4 language death and linguistic imperialism
N34 = 'Language death, linguistic imperialism and attitudes to global English'
t34 = topic(N34, N34)
t34.fixed('C1', (1, 2), [
    ('Who wrote Linguistic Imperialism (1992)?', 'Robert Phillipson', 'Phillipson argued that the spread of English serves the interests of powerful nations.', ['Braj Kachru', 'David Crystal', 'Noam Chomsky']),
    ('Which writer stopped writing novels in English and turned to Gikuyu, explaining his reasons in Decolonising the Mind (1986)?', 'Ngũgĩ wa Thiong’o', 'Ngũgĩ argued that language carries culture and identity.', ['Chinua Achebe', 'Samuel Johnson', 'Jennifer Jenkins']),
    ('What is ‘language shift’?', 'A community gradually moving from using one language to another', 'Shift often precedes language death.', ['A change in pronunciation', 'A type of code-switching', 'The spread of a new word']),
    ('What is the most important factor in keeping a language alive?', 'Intergenerational transmission: children acquiring it at home', 'Languages die when children no longer learn them.', ['Having a dictionary', 'Being used on television', 'Having many loanwords']),
    ('Which is an example of language revitalisation?', 'Māori kōhanga reo (‘language nests’) for young children', 'Immersion pre-schools in New Zealand from 1982.', ['Banning a language in schools', 'Adopting English as the only official language', 'Creating a pidgin']),
])
DEATH_STAGES = [('Potentially endangered', 'children still learn it but a dominant language is spreading'), ('Endangered', 'few children are learning it'),
                ('Seriously endangered', 'the youngest fluent speakers are young adults or older'), ('Moribund', 'only a few elderly speakers remain'), ('Extinct', 'no speakers remain')]


@t34.add('C1', (1, 2, 3))
def t34_stage(r, D):
    lab, desc = r.choice(DEATH_STAGES)
    opts, ans = mcq(r, lab, [x for x, _ in DEATH_STAGES if x != lab])
    return {'stem': f'A language is described as follows: {desc}. Which term best describes its status?', 'options': opts, 'answer': ans, 'key': f'{lab}: {desc}.'}


fixed_c2(t34, [
    ('Explain what Phillipson means by ‘linguistic imperialism’.', 'The dominance of English is maintained by structural and cultural inequalities that favour English and its speakers.',
     ['English promoted through education, aid and institutions', 'benefits flow to English-speaking nations', 'other languages marginalised', 'critics argue that people choose English for opportunity (agency)']),
    ('Explain why some writers from former colonies choose to write in English while others reject it.', 'Some, like Achebe, adapt English to carry local experience and reach a wide audience; others, like Ngũgĩ, see it as a colonial imposition.',
     ['Achebe: English reshaped for African experience', 'wider readership and economic reasons', 'Ngũgĩ: language carries culture; English as colonial', 'identity and decolonisation']),
    ('Explain two causes of language death.', 'Language shift to a dominant language and the loss of intergenerational transmission.',
     ['economic pressure to use a dominant language', 'education in a dominant language', 'urbanisation and migration', 'loss of intergenerational transmission', 'historical suppression']),
    ('Explain why linguists are concerned about language death.', 'Each language encodes unique knowledge, culture and ways of seeing the world.',
     ['loss of cultural knowledge and identity', 'loss of data for linguistics', 'loss of ecological or local knowledge', 'human rights of speakers']),
])


@t34.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t34_data(r, D):
    lang = r.choice(['a small island language', 'an indigenous language of a river valley', 'a mountain community’s language', 'a coastal fishing community’s language'])
    ages = ['60+', '40–59', '20–39', 'under 20']
    p = [r.randint(80, 95)]
    for _ in range(3):
        p.append(max(2, p[-1] - r.randint(12, 30)))
    m = marks('C3', D)
    drop = p[0] - p[3]
    rel = (p[3] - p[0]) / p[0] * 100
    stem = (f'A survey of {lang} in {city(r)} recorded the percentage of each age group who speak it fluently: ' + '; '.join(f'{a}: {x}%' for a, x in zip(ages, p)) +
            f'. (a) Calculate the difference in percentage points between the oldest and youngest groups. (b) Calculate the percentage decrease in fluency rate from the oldest to the youngest group.')
    ans = f'(a) {p[0]} − {p[3]} = {drop} percentage points. (b) ({p[3]} − {p[0]}) ÷ {p[0]} × 100 = {rel:.1f}%, a decrease of {-rel:.1f}%.'
    if D >= 3:
        stem += ' (c) Explain what the data suggest about the future of the language.'
        ans += ' (c) Intergenerational transmission is breaking down; without intervention the language is heading towards endangerment or death.'
    return {'stem': stem, 'answer': ans, 'key': f'{upto(m)}: (a) {drop} percentage points; (b) {-rel:.1f}% decrease with method' + ('; (c) interpretation linked to intergenerational transmission and stages of endangerment.' if D >= 3 else '.'), 'marks': m}


@t34.add('C3', (2, 3, 4, 5), 'explain')
def t34_stim(r, D):
    stims = [('English is a neutral tool: it belongs to nobody, so it threatens nobody.', ['challenges Phillipson’s view that English is not neutral', 'ELF ownership argument (Widdowson)', 'evidence of language shift where English dominates', 'English as a key to opportunity']),
             ('If my grandchildren speak only English, they will have lost something no school can give back.', ['intergenerational transmission', 'language and identity (Ngũgĩ)', 'emotive appeal and family context', 'revitalisation programmes']),
             ('Learning English is a choice families make freely for a better future.', ['agency v. imperialism debate', 'economic motives', 'structural pressures limiting choice (Phillipson)', 'bilingualism as an alternative to shift'])]
    s, pts = r.choice(stims)
    m = marks('C3', D)
    return {'stem': f'A speaker at a conference on global English says: {Q(s)} Analyse the attitude expressed and relate it to ideas about linguistic imperialism and language death.', 'answer': '; '.join(cap(x) for x in pts) + '.',
            'key': pts_key(m, pts), 'marks': m}


@t34.add('C4', (2, 3, 4, 5), 'long')
def t34_long(r, D):
    title = r.choice(['‘The global spread of English is a threat to the world’s linguistic diversity.’ Discuss.', 'Evaluate the view that English is a tool of linguistic imperialism.',
                      'Discuss the causes of language death and the effectiveness of attempts to revitalise endangered languages.'])
    ind = 'Phillipson (1992) linguistic imperialism; counter-views: agency, English as an economic resource; Ngũgĩ v. Achebe; Crystal (2000) on language death; Krauss (1992) estimate that a large proportion of languages are endangered; causes: shift, domain loss, lack of transmission; revitalisation: Māori kōhanga reo, Welsh, Hebrew; bilingualism; evaluation.'
    return essay(r, D, title, ind)


CHAPTERS[3] = [t31, t32, t33, t34]


# =========================================================== 4 Language and the self

# ---------------------------------------------------------------- 4.1 idiolect, sociolect and dialect
N41 = 'Language and identity: idiolect, sociolect and dialect'
t41 = topic(N41, N41)
ID_TERMS = ['idiolect', 'sociolect', 'dialect', 'accent', 'covert prestige', 'overt prestige', 'code-switching', 'social network']
ID_ITEMS = [
    ('A teacher always ends explanations with ‘right then, off you go’, a phrase her students imitate.', 'idiolect', 'an individual’s distinctive language habits'),
    ('Surfers share terms such as ‘gnarly’ and ‘barrel’ that outsiders rarely use.', 'sociolect', 'language shared by a social group'),
    ('Speakers in one region say ‘bairn’ for child and ‘ken’ for know.', 'dialect', 'regional variation in vocabulary and grammar'),
    ('Two people use the same words and grammar but pronounce ‘bath’ differently.', 'accent', 'variation in pronunciation only'),
    ('Some men in Norwich reported using more non-standard forms than they actually used.', 'covert prestige', 'non-standard forms carry hidden prestige linked to toughness and local identity (Trudgill)'),
    ('A job candidate adopts Received Pronunciation in an interview.', 'overt prestige', 'the standard is publicly valued for status'),
    ('A student uses Hindi with her grandmother and English with friends, sometimes in the same sentence.', 'code-switching', 'moving between languages or varieties according to context or for effect'),
    ('People with dense, close-knit local ties keep their vernacular features most strongly.', 'social network', 'Milroy’s Belfast study linked network density to vernacular use'),
]
STUDIES = [
    ('Labov’s New York department-store study (1966)', 'staff in higher-status stores pronounced post-vocalic /r/ (‘fourth floor’) more often, showing social stratification of a variable'),
    ('Trudgill’s Norwich study (1974)', 'lower-class speakers and men used more -in’ forms; men over-reported non-standard use, revealing covert prestige'),
    ('Milroy’s Belfast study (1980)', 'speakers in dense, multiplex social networks kept vernacular forms most strongly'),
    ('Eckert’s ‘jocks and burnouts’ study (1989)', 'adolescents’ use of linguistic variables marked their social-group identity within a school'),
    ('Labov’s Martha’s Vineyard study (1963)', 'islanders who identified with the island exaggerated a local vowel to mark identity against tourists'),
]
t41.fixed('C1', (1, 2), [
    ('What is an idiolect?', 'An individual’s unique way of using language', 'Shaped by region, age, occupation, interests and experiences.', ['The language of a whole country', 'A type of pidgin', 'A regional accent only']),
    ('What is the difference between accent and dialect?', 'Accent is pronunciation only; dialect includes vocabulary and grammar', 'A dialect may be spoken with different accents.', ['They mean the same', 'Dialect is pronunciation only', 'Accent includes grammar']),
    ('What is covert prestige?', 'Hidden status gained by using non-standard forms that signal group membership', 'Trudgill’s Norwich study (1974).', ['Status gained from using the standard', 'A secret language', 'The prestige of written English']),
    ('Which researcher studied social networks in Belfast?', 'Lesley Milroy', 'Milroy (1980): dense networks maintain vernacular.', ['William Labov', 'Robin Lakoff', 'Howard Giles']),
])
cls_templates(t41, [(ID_TERMS, ID_ITEMS, 'Which concept does this example best illustrate? {q}')], c2_ctx=['A student investigating language and identity records this', 'A sociolinguistics textbook gives this example'])


@t41.add('C1', (1, 2, 3))
def t41_study(r, D):
    st, find = r.choice(STUDIES)
    opts, ans = mcq(r, cap(find), [cap(f) for s, f in STUDIES if s != st])
    return {'stem': f'Which finding is associated with {st}?', 'options': opts, 'answer': ans, 'key': f'{st}: {find}.'}


@t41.add('C2', (2, 3, 4), 'explain')
def t41_study_explain(r, D):
    st, find = r.choice(STUDIES)
    m = marks('C2', D)
    return {'stem': f'Explain what {st} suggests about the relationship between language and identity.', 'answer': cap(find) + '.',
            'key': pts_key(m, ['accurate summary of the method or context', f'key finding: {find}', 'implication for language and identity']), 'marks': m}


@t41.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t41_data(r, D):
    groups = r.sample(['working-class men', 'working-class women', 'middle-class men', 'middle-class women'], 4)
    var = r.choice([('-in’ for -ing (e.g. walkin’)', 'non-standard'), ('glottal stop for /t/ (e.g. wa’er)', 'non-standard'), ('dropped /h/ (e.g. ’ouse)', 'non-standard')])
    data = {}
    for g in groups:
        n = r.choice([40, 50, 60, 80, 120])
        base = {'working-class men': 0.75, 'working-class women': 0.5, 'middle-class men': 0.35, 'middle-class women': 0.15}[g]
        k = max(1, min(n - 1, round(n * (base + r.uniform(-0.1, 0.1)))))
        data[g] = (k, n)
    m = marks('C3', D)
    pcts = {g: k / n * 100 for g, (k, n) in data.items()}
    hi = max(pcts, key=pcts.get)
    lo = min(pcts, key=pcts.get)
    stem = (f'A student in {city(r)} recorded the use of {var[0]} in interviews. Number of non-standard tokens / total tokens: ' + '; '.join(f'{g}: {k}/{n}' for g, (k, n) in data.items()) +
            '. Calculate the percentage of non-standard forms for each group (to 1 decimal place)' + (' and analyse what the results suggest, with reference to research.' if D >= 3 else '.'))
    ans = ' '.join(f'{g}: {k} ÷ {n} × 100 = {pcts[g]:.1f}%.' for g, (k, n) in data.items())
    if D >= 3:
        ans += f' Highest: {hi}; lowest: {lo}. This pattern resembles Trudgill’s findings (class and gender stratification; covert prestige for men).'
    return {'stem': stem, 'answer': ans, 'key': f'{upto(m)}: correct percentages (' + '; '.join(f'{g} {pcts[g]:.1f}%' for g in data) + ')' +
            ('; interpretation of class/gender patterns; reference to Trudgill or Labov; awareness of small sample sizes.' if D >= 3 else '.'), 'marks': m}


@t41.add('C4', (2, 3, 4, 5), 'long')
def t41_long(r, D):
    stim = r.choice(['A student writes in a school magazine: ‘When I moved to the city, I lost my accent in six months. I sound like everyone else now, but my grandmother says I sound like a stranger.’',
                     'A radio presenter says: ‘Regional accents are making a comeback on national television, and that can only be a good thing.’',
                     'An employer says: ‘We do not judge people by their accents, but clients expect a certain way of speaking.’'])
    title = r.choice(['Discuss the ways in which language reflects and shapes personal and group identity. Refer to the text above and to your wider study.', 'Evaluate the view that the way we speak reveals who we are.'])
    ind = 'idiolect, sociolect, dialect and accent; Labov (1963, 1966); Trudgill (1974) covert prestige; Milroy (1980) social networks; Eckert (1989); accommodation (Giles) and identity; code-switching; attitudes to accents and discrimination; evaluation of how far identity is chosen or imposed.'
    return essay(r, D, f'{stim} {title}', ind)


# ---------------------------------------------------------------- 4.2 language and gender
N42 = 'Language and gender: deficit, dominance, difference theories (Lakoff, Tannen)'
t42 = topic(N42, N42)
G_THEORIES = ['deficit', 'dominance', 'difference', 'diversity']
G_ITEMS = [
    ('Women’s language is weaker because it uses more hedges and tag questions.', 'deficit', 'Lakoff (1975) presented women’s language as lacking authority'),
    ('Men interrupt women more often because they hold more social power.', 'dominance', 'Zimmerman and West (1975) linked interruptions to male dominance'),
    ('Men and women grow up in different subcultures and so talk in different styles.', 'difference', 'Tannen (1990): report talk v. rapport talk'),
    ('Variation within each gender is greater than variation between them; context matters more.', 'diversity', 'Cameron (2007) challenges the Mars/Venus myth'),
    ('Men tend to give advice when women want sympathy.', 'difference', 'Tannen’s advice v. understanding contrast'),
    ('Language was made by men and encodes male norms (e.g. ‘chairman’).', 'dominance', 'Spender (1980) Man Made Language'),
    ('Women use ‘empty’ adjectives such as ‘divine’ and ‘lovely’.', 'deficit', 'one of Lakoff’s proposed features of women’s language'),
    ('Speakers with less power in court used ‘powerless’ language whatever their gender.', 'diversity', 'O’Barr and Atkins (1980): power, not gender, explained the features'),
]
LAKOFF = ['hedges', 'tag questions', 'empty adjectives', 'super-polite forms', 'intensifiers', 'hypercorrect grammar']
LK = [('I sort of think we should leave.', 'hedges'), ('It’s a lovely day, isn’t it?', 'tag questions'), ('What a divine dress!', 'empty adjectives'),
      ('Would you mind terribly if I asked you to close the window?', 'super-polite forms'), ('I was so happy.', 'intensifiers'), ('Whom did you wish to speak to?', 'hypercorrect grammar'),
      ('It’s kind of expensive, I suppose.', 'hedges'), ('That was a really, really good film.', 'intensifiers')]
TANNEN = [('status', 'support'), ('independence', 'intimacy'), ('advice', 'understanding'), ('information', 'feelings'), ('orders', 'proposals'), ('conflict', 'compromise')]
t42.fixed('C1', (1, 2), [
    ('Who wrote Language and Woman’s Place (1975)?', 'Robin Lakoff', 'Lakoff proposed a list of features of ‘women’s language’.', ['Deborah Tannen', 'Deborah Cameron', 'Jennifer Coates']),
    ('Which approach is associated with Deborah Tannen’s You Just Don’t Understand (1990)?', 'Difference', 'Tannen describes men’s and women’s styles as different, not deficient.', ['Deficit', 'Dominance', 'Behaviourism']),
    ('Zimmerman and West (1975) found that in mixed-sex conversations most interruptions were made by …', 'men', 'They reported 46 of 48 interruptions by men in mixed-sex pairs.', ['women', 'children', 'equally by both']),
    ('Which researcher argued in The Myth of Mars and Venus (2007) that gender differences in language are exaggerated?', 'Deborah Cameron', 'Cameron stresses variation and context.', ['Robin Lakoff', 'B. F. Skinner', 'Robert Phillipson']),
])
cls_templates(t42, [(G_THEORIES, G_ITEMS, 'Which approach to language and gender does this statement reflect? {q}'), (LAKOFF, [(s, f, f'one of Lakoff’s proposed features') for s, f in LK], 'Which of Lakoff’s proposed features is shown? {q}')],
              c2_ctx=['A student studying language and gender finds this example', 'This statement appears in a debate about gender and talk'])


@t42.add('C1', (1, 2, 3))
def t42_tannen(r, D):
    a, b = r.choice(TANNEN)
    others = [y for x, y in TANNEN if y != b]
    opts, ans = mcq(r, cap(b), [cap(o) for o in others])
    return {'stem': f'In Tannen’s difference model, men’s ‘{a}’ is contrasted with women’s …', 'options': opts, 'answer': ans, 'key': f'Tannen (1990): {a} v. {b}.'}


@t42.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t42_data(r, D):
    words_m = r.choice([1800, 2400, 3000, 3600])
    words_f = r.choice([1600, 2000, 2500, 3200])
    feat = r.choice(['tag questions', 'hedges', 'interruptions', 'minimal responses (mm, yeah)'])
    km = r.randint(6, 40)
    kf = r.randint(6, 40)
    rm, rf = km / words_m * 1000, kf / words_f * 1000
    if abs(rm - rf) < 0.3:
        return None
    m = marks('C3', D)
    stem = (f'A student recorded a group discussion in {city(r)}. The male speakers produced {words_m:,} words and {km} {feat}; the female speakers produced {words_f:,} words and {kf} {feat}. '
            f'Calculate the rate of {feat} per 1,000 words for each group (to 1 decimal place).')
    ans = f'Male: {km} ÷ {words_m:,} × 1,000 = {rm:.1f}. Female: {kf} ÷ {words_f:,} × 1,000 = {rf:.1f}. ' + ('Male speakers' if rm > rf else 'Female speakers') + ' used them more often.'
    if D >= 3:
        stem += ' Then evaluate what the results show about gender and talk, referring to research.'
        ans += ' Interpretation must be cautious: one small sample, functions vary (e.g. Holmes: facilitative v. epistemic tags), and context, role and power may matter more than gender (Cameron, O’Barr and Atkins).'
    return {'stem': stem, 'answer': ans, 'key': f'{upto(m)}: normalising by word count; male {rm:.1f}, female {rf:.1f} per 1,000 words' +
            ('; evaluation referring to Lakoff/Holmes/Cameron and the limits of the data.' if D >= 3 else '.'), 'marks': m}


@t42.add('C3', (2, 3, 4, 5), 'explain')
def t42_tr(r, D):
    a, b = r.sample(['JONAS', 'ELENA', 'KWAME', 'AISHA'], 2)
    m = marks('C3', D)
    tr = (f'{a}: so the plan is we leave at six // {b}: // I was sort of thinking (.) maybe seven would be better (.) wouldn’t it {a}: no (.) six (.) traffic’s terrible later '
          f'{b}: mm (.) okay (.) I suppose that makes sense {a}: right (.) and you book the tickets {b}: could you possibly send me the link')
    return {'stem': f'Read this transcript of two colleagues planning a trip: {Q(tr)} Analyse how the speakers’ language could be interpreted using theories of language and gender and power.',
            'answer': f'{a}: interruption-free assertions, bald imperatives, topic control; {b}: hedges (sort of, maybe), tag question (wouldn’t it), minimal responses, super-polite request (could you possibly).',
            'key': pts_key(m, ['hedges and tag question (Lakoff)', 'minimal responses and accommodation', f'{a}’s bald directives and topic control (dominance or status)', 'super-polite request (negative politeness)', 'caution: role/power may explain features (O’Barr and Atkins, Cameron)']), 'marks': m}


@t42.add('C4', (2, 3, 4, 5), 'long')
def t42_long(r, D):
    stim = r.choice(['A magazine article claims: ‘Women talk more than men – everyone knows that.’', 'A business coach advises women: ‘Drop the hedges and tag questions if you want to be taken seriously.’',
                     'A blogger writes: ‘Men and women are from different planets when it comes to conversation.’'])
    title = r.choice(['Discuss the view expressed above, referring to ideas and research about language and gender.', 'Evaluate deficit, dominance and difference approaches to language and gender.'])
    ind = 'Lakoff (1975) deficit; Zimmerman and West (1975), Spender (1980) dominance; Tannen (1990), Coates difference; Cameron (2007), O’Barr and Atkins (1980) diversity/power; Holmes on tag questions; evidence on who talks more; context, role and power; evaluation of methods and of stereotypes.'
    return essay(r, D, f'{stim} {title}', ind)


# ---------------------------------------------------------------- 4.3 language and power
N43 = 'Language and power: accommodation theory and politeness (Giles, Brown and Levinson)'
t43 = topic(N43, N43)
POL = ['bald on record', 'positive politeness', 'negative politeness', 'off record']
POL_ITEMS = [
    ('Close the door.', 'bald on record', 'a direct command with no redress'), ('Hey mate, you’re brilliant at this – could you give me a hand?', 'positive politeness', 'appeals to friendship and approval (positive face)'),
    ('I’m so sorry to bother you, but would it be possible to borrow your notes?', 'negative politeness', 'apology and indirectness respect the hearer’s freedom (negative face)'),
    ('It’s a bit cold in here, isn’t it?', 'off record', 'an indirect hint that the window should be closed'), ('Pass the salt.', 'bald on record', 'efficient, direct request'),
    ('We’re all in this together, so let’s get it finished.', 'positive politeness', 'inclusive ‘we’ and solidarity'), ('I don’t suppose you could possibly stay late tonight?', 'negative politeness', 'hedging and pessimism minimise imposition'),
    ('Someone hasn’t washed their cup again.', 'off record', 'an indirect criticism without naming anyone'),
]
CAT = ['upward convergence', 'downward convergence', 'divergence', 'maintenance']
CAT_ITEMS = [
    ('A student adopts a more formal accent and vocabulary when speaking to an interviewer.', 'upward convergence', 'moving towards a more prestigious style'),
    ('A manager uses slang and a local accent to sound friendly to new apprentices.', 'downward convergence', 'moving towards a less prestigious style to build rapport'),
    ('A visitor who feels insulted exaggerates her regional accent.', 'divergence', 'emphasising difference to show distance or identity'),
    ('A speaker keeps his usual accent and style regardless of who he is speaking to.', 'maintenance', 'neither converging nor diverging'),
    ('A teenager shifts to a more standard style when phoning a bank.', 'upward convergence', 'accommodating towards a higher-status interlocutor'),
    ('A politician drops formal vocabulary in a factory visit.', 'downward convergence', 'accommodating to the audience to appear ‘ordinary’'),
]
FAIR = [('power in discourse', 'how powerful participants control talk within an interaction (e.g. interviewer controls topics and turns)'),
        ('power behind discourse', 'how social institutions and conventions determine who may speak and how'), ('synthetic personalisation', 'mass-media texts addressing readers as individuals to simulate friendliness')]
t43.fixed('C1', (1, 2), [
    ('Who developed communication accommodation theory?', 'Howard Giles', 'Giles’ accommodation theory (from the 1970s) explains convergence and divergence.', ['Penelope Brown', 'Robin Lakoff', 'Noam Chomsky']),
    ('In Brown and Levinson’s politeness theory, what is ‘negative face’?', 'The desire to be unimpeded and free from imposition', 'Positive face = desire to be liked and approved.', ['The desire to be liked', 'A frown', 'The use of swear words']),
    ('What is a face-threatening act?', 'An act that threatens the hearer’s or speaker’s positive or negative face', 'E.g. requests, criticisms, refusals.', ['A rude facial expression', 'A compliment', 'An interruption only']),
    ('Who distinguished between ‘power in discourse’ and ‘power behind discourse’?', 'Norman Fairclough', 'Fairclough, Language and Power (1989).', ['Howard Giles', 'Deborah Tannen', 'Braj Kachru']),
])
cls_templates(t43, [(POL, POL_ITEMS, 'Which politeness strategy (Brown and Levinson) is used? {q}'), (CAT, CAT_ITEMS, 'Which accommodation strategy (Giles) is shown? {q}')],
              c2_ctx=['This was observed in a workplace', 'A student analysing talk at a family dinner notes this'])


@t43.add('C1', (1, 2, 3))
def t43_fair(r, D):
    t_, d = r.choice(FAIR)
    opts, ans = mcq(r, cap(t_), [cap(x) for x, _ in FAIR if x != t_] + ['Covert prestige'])
    return {'stem': f'Which of Fairclough’s concepts matches this description: {d}?', 'options': opts, 'answer': ans, 'key': f'{cap(t_)}: {d}.'}


TR43 = [
    ('a job interview', 'INTERVIEWER: so (.) tell me why you want this role CANDIDATE: well (.) I’ve always been passionate about design and I // INTERVIEWER: // sorry (.) can I stop you there (.) what experience do you actually have CANDIDATE: erm (.) I did a placement last summer (.) at a studio in Lisbon INTERVIEWER: right (.) next question',
     ['interviewer controls topics and turns (power in discourse, Fairclough)', 'interruption (‘sorry (.) can I stop you there’) as a face-threatening act softened by an apology', 'candidate’s hedges and fillers show lower status', '‘right (.) next question’ closes the topic: institutional power', 'candidate’s upward convergence to formal register']),
    ('a doctor’s consultation', 'DOCTOR: and how long have you had the pain PATIENT: about a week (.) I didn’t want to bother you DOCTOR: you’re not bothering me at all (.) let’s have a look PATIENT: thank you (.) sorry DOCTOR: no need to apologise (.) can you lie down for me',
     ['doctor asks questions and directs actions (power in discourse)', 'patient’s negative politeness (‘didn’t want to bother you’, ‘sorry’)', 'doctor’s positive politeness and reassurance', 'inclusive ‘let’s’ softens a directive', '‘can you lie down for me’ – an indirect directive (mitigated FTA)']),
    ('a classroom', 'TEACHER: right (.) phones away please (.) Omar (.) that includes you OMAR: I’m just checking the time miss TEACHER: there’s a clock (.) look up OMAR: [laughs] fair enough TEACHER: thank you',
     ['teacher’s bald-on-record directives (‘phones away’)', 'naming as a face-threatening act', 'Omar’s excuse and humour to save face', 'teacher’s ‘thank you’ restores politeness', 'institutional power behind discourse (school roles)']),
]


@t43.add('C3', (2, 3, 4, 5), 'explain')
def t43_tr(r, D):
    ctx, tr, pts = r.choice(TR43)
    m = marks('C3', D)
    return {'stem': f'Read this transcript from {ctx}: {Q(tr)} Analyse how power and politeness are shown in the interaction, referring to relevant theories.', 'answer': '; '.join(cap(p) for p in pts) + '.',
            'key': pts_key(m, pts), 'marks': m}


@t43.add('C4', (2, 3, 4, 5), 'long')
def t43_long(r, D):
    ctx, tr, pts = r.choice(TR43)
    title = r.choice(['Discuss how speakers use language to exercise and resist power, referring to the transcript and to your wider study.', 'Evaluate how useful accommodation theory and politeness theory are for explaining interactions such as this one.'])
    ind = '; '.join(pts) + '; Giles (CAT: convergence, divergence); Brown and Levinson (face, FTAs, strategies); Fairclough (power in/behind discourse); Grice’s maxims; evaluation: cultural variation in politeness, context.'
    return essay(r, D, f'Read this transcript from {ctx}: {Q(tr)} {title}', ind)


# ---------------------------------------------------------------- 4.4 discursive essay on language topics
N44 = 'Writing a discursive essay on language topics using evidence and theory'
t44 = topic(N44, N44)
ESSAYS = [
    ('‘The way people speak should not affect how they are judged.’', 'accent prejudice, overt/covert prestige, Labov, Trudgill, Giles (matched-guise studies), workplace discrimination, identity'),
    ('‘Men and women speak differently.’', 'Lakoff, Zimmerman and West, Tannen, Coates, Cameron, O’Barr and Atkins, context and power'),
    ('‘Politeness is more about power than kindness.’', 'Brown and Levinson, face, FTAs, Fairclough, institutional talk, cultural variation'),
    ('‘Our idiolect is shaped more by the groups we belong to than by where we come from.’', 'idiolect, sociolect, dialect, Milroy, Eckert, code-switching, online communities'),
    ('‘In a globalised world, everyone needs the same English.’', 'Kachru, ELF, Jenkins, world Englishes, standard English, identity'),
    ('‘Speakers always adapt their language to the person they are talking to.’', 'Giles CAT, convergence/divergence, audience design (Bell), maintenance, power'),
]
WEAK_THESIS = [
    ('In this essay I will talk about {t}.', 'announces the topic but takes no position and gives no direction'),
    ('Everyone already knows the answer, so the statement is obviously true.', 'asserts a view as common sense without evidence'),
    ('{names}.', 'lists names without ideas or argument'),
    ('Language is very interesting and important in our lives.', 'vague generalisation with no relevance to the question'),
]


def weak_for(r, q, ideas):
    w, why = r.choice(WEAK_THESIS)
    t_ = q.strip('‘’.').lower()
    names = ', '.join(x for x in ideas.split(', ')[:4])
    return w.format(t=t_ if len(t_) < 60 else 'this topic', names=cap(names)), why
t44.fixed('C1', (1, 2), [
    ('In a Paper 4 essay, what does AO5 reward?', 'Evaluation of ideas, theories and research to develop a reasoned argument', 'AO5 = evaluate issues and ideas; AO4 = knowledge of concepts.', ['Accurate spelling only', 'Creative storytelling', 'Copying the stimulus text']),
    ('How should the stimulus text be used in a Paper 4 essay?', 'As a starting point and source of examples, alongside wider study', 'Refer to it but go beyond it.', ['Ignored completely', 'Copied in full', 'Summarised without comment']),
    ('Which is the best way to use research in a discursive language essay?', 'Summarise the key idea, apply it to an example and evaluate it', 'Apply and evaluate, rather than just naming theorists.', ['List as many names as possible', 'Quote long passages from memory', 'Avoid research altogether']),
])


@t44.add('C1', (1, 2, 3))
def t44_best(r, D):
    q, ideas = r.choice(ESSAYS)
    good = f'This essay will argue that the statement is partly true, but that context, power and identity complicate the picture, drawing on {ideas.split(", ")[0]} and {ideas.split(", ")[1]}.'
    ds = []
    while len(ds) < 3:
        w, _ = weak_for(r, q, ideas)
        if w not in ds:
            ds.append(w)
    opts, ans = mcq(r, good, ds)
    return {'stem': f'Which is the most effective opening thesis for an essay on {q}?', 'options': opts, 'answer': ans, 'key': 'It takes a qualified position and signals the ideas that will be evaluated.'}


@t44.add('C2', (1, 2, 3, 4), 'explain')
def t44_weak(r, D):
    q, ideas = r.choice(ESSAYS)
    s, why = weak_for(r, q, ideas)
    m = marks('C2', D)
    return {'stem': f'A student begins an essay on {q} with: {Q(s)} Explain why this is weak and suggest a better opening.', 'answer': f'It {why}. A better opening takes a qualified position and signals the ideas to be evaluated.',
            'key': pts_key(m, [f'identifies the weakness ({why})', 'explains what a strong thesis does', f'a valid improved opening drawing on relevant ideas ({ideas.split(", ")[0]})']), 'marks': m}


@t44.add('C3', (1, 2, 3, 4, 5), 'multi_step')
def t44_plan(r, D):
    q, ideas = r.choice(ESSAYS)
    ids = ideas.split(', ')
    parts = [
        lambda r: ('Write a thesis statement.', 'A qualified position that answers the question.', '1 mark position; 1 mark qualification [2]'),
        lambda r: (f'Write a paragraph that applies and evaluates {ids[0]}.', f'Summary of {ids[0]}, application to an example, evaluation.', '1 mark summary; 1 mark example; 2 marks evaluation [4]'),
        lambda r: (f'Explain how {ids[1]} could be used as a counter-argument.', f'{cap(ids[1])} offers an alternative view that qualifies the thesis.', '1 mark idea; 2 marks link to argument [3]'),
        lambda r: ('Write a concluding sentence.', 'A conclusion that reaches a reasoned judgement.', '1 mark judgement; 1 mark link to question [2]'),
    ]
    return compose(r, f'You are planning a discursive essay on {q}', parts, k=(2, 3), type_='multi_step')


@t44.add('C4', (2, 3, 4, 5), 'long')
def t44_long(r, D):
    q, ideas = r.choice(ESSAYS)
    frame = r.choice(['Write a discursive essay in which you evaluate this view, referring to ideas and research from your study of language and the self.',
                      'Discuss this statement, drawing on relevant theories, studies and examples of everyday language use.',
                      'To what extent do you agree? Support your argument with reference to research and to examples you have studied.'])
    return essay(r, D, f'{q} {frame}',
                 f'a clear, qualified thesis; {ideas}; examples from data and everyday talk; evaluation of methods and of competing theories; counter-arguments; reasoned conclusion.')


CHAPTERS[4] = [t41, t42, t43, t44]

for _ts in CHAPTERS.values():
    for _t in _ts:
        for _tp in _t.templates:
            if not getattr(_tp, '_tidy', False):
                _tp.fn = _wrap(_tp.fn)
                _tp._tidy = True
