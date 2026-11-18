"""Grammar engines for the QB-CBSE English subjects (cbse-g8-english, cbse-g9-english).

Every engine builds sentences from structured parts and computes the answer, so keys are always
consistent: verb forms come from the VERBS table, agreement from explicit number flags.
"""
from __future__ import annotations

import random
import re

from qbank import F, ar, mcq, onorm, GIRLS, BOYS
from eng_kit_g8_g9_g12 import (person, PRON_F, PRON_M, roman, inline_opts, need, g_ar_from, g_fact, inject_error, jumble, slots, fill)

# ---------------------------------------------------------------- verbs

IRREG = {
    'be': ('was', 'been'), 'begin': ('began', 'begun'), 'break': ('broke', 'broken'), 'bring': ('brought', 'brought'),
    'build': ('built', 'built'), 'burst': ('burst', 'burst'), 'buy': ('bought', 'bought'), 'catch': ('caught', 'caught'),
    'choose': ('chose', 'chosen'), 'come': ('came', 'come'), 'cut': ('cut', 'cut'), 'do': ('did', 'done'), 'draw': ('drew', 'drawn'),
    'drink': ('drank', 'drunk'), 'drive': ('drove', 'driven'), 'eat': ('ate', 'eaten'), 'fall': ('fell', 'fallen'), 'feel': ('felt', 'felt'),
    'find': ('found', 'found'), 'fly': ('flew', 'flown'), 'forget': ('forgot', 'forgotten'), 'get': ('got', 'got'), 'give': ('gave', 'given'),
    'go': ('went', 'gone'), 'grow': ('grew', 'grown'), 'have': ('had', 'had'), 'hear': ('heard', 'heard'), 'hide': ('hid', 'hidden'),
    'hold': ('held', 'held'), 'keep': ('kept', 'kept'), 'know': ('knew', 'known'), 'lead': ('led', 'led'), 'leave': ('left', 'left'),
    'lose': ('lost', 'lost'), 'make': ('made', 'made'), 'meet': ('met', 'met'), 'pay': ('paid', 'paid'), 'put': ('put', 'put'),
    'read': ('read', 'read'), 'ride': ('rode', 'ridden'), 'ring': ('rang', 'rung'), 'rise': ('rose', 'risen'), 'run': ('ran', 'run'),
    'say': ('said', 'said'), 'see': ('saw', 'seen'), 'sell': ('sold', 'sold'), 'send': ('sent', 'sent'), 'sing': ('sang', 'sung'),
    'sit': ('sat', 'sat'), 'sleep': ('slept', 'slept'), 'speak': ('spoke', 'spoken'), 'spend': ('spent', 'spent'), 'stand': ('stood', 'stood'),
    'steal': ('stole', 'stolen'), 'sow': ('sowed', 'sown'), 'swim': ('swam', 'swum'), 'take': ('took', 'taken'), 'teach': ('taught', 'taught'),
    'tell': ('told', 'told'), 'think': ('thought', 'thought'), 'throw': ('threw', 'thrown'), 'understand': ('understood', 'understood'),
    'wake': ('woke', 'woken'), 'wear': ('wore', 'worn'), 'win': ('won', 'won'), 'write': ('wrote', 'written'), 'shake': ('shook', 'shaken'),
    'weave': ('wove', 'woven'), 'blow': ('blew', 'blown'), 'show': ('showed', 'shown'), 'light': ('lit', 'lit'), 'dig': ('dug', 'dug'),
    'feed': ('fed', 'fed'), 'shine': ('shone', 'shone'), 'strike': ('struck', 'struck'), 'tear': ('tore', 'torn'), 'bear': ('bore', 'borne'),
}
ING = {'lie': 'lying', 'die': 'dying', 'tie': 'tying', 'run': 'running', 'sit': 'sitting', 'swim': 'swimming', 'stop': 'stopping',
       'plan': 'planning', 'get': 'getting', 'put': 'putting', 'cut': 'cutting', 'begin': 'beginning', 'win': 'winning', 'dig': 'digging',
       'shop': 'shopping', 'chat': 'chatting', 'drop': 'dropping', 'clap': 'clapping', 'jog': 'jogging', 'nod': 'nodding', 'grab': 'grabbing',
       'snatch': 'snatching', 'travel': 'travelling', 'hop': 'hopping', 'rob': 'robbing', 'trap': 'trapping', 'admit': 'admitting',
       'permit': 'permitting', 'regret': 'regretting', 'forget': 'forgetting', 'hit': 'hitting', 'set': 'setting', 'slip': 'slipping'}
PAST = {'stop': 'stopped', 'plan': 'planned', 'drop': 'dropped', 'clap': 'clapped', 'chat': 'chatted', 'nod': 'nodded', 'grab': 'grabbed',
        'travel': 'travelled', 'hop': 'hopped', 'rob': 'robbed', 'trap': 'trapped', 'admit': 'admitted', 'permit': 'permitted', 'slip': 'slipped',
        'regret': 'regretted', 'shop': 'shopped', 'jog': 'jogged', 'study': 'studied', 'carry': 'carried', 'try': 'tried', 'cry': 'cried',
        'hurry': 'hurried', 'worry': 'worried', 'reply': 'replied', 'copy': 'copied', 'marry': 'married', 'bury': 'buried', 'dry': 'dried',
        'apply': 'applied', 'occur': 'occurred', 'refer': 'referred', 'prefer': 'preferred'}


def past(v):
    if v in IRREG:
        return IRREG[v][0]
    if v in PAST:
        return PAST[v]
    if v.endswith('e'):
        return v + 'd'
    if v.endswith('y') and v[-2] not in 'aeiou':
        return v[:-1] + 'ied'
    return v + 'ed'


def pp(v):
    if v in IRREG:
        return IRREG[v][1]
    return past(v)


def ing(v):
    if v in ING:
        return ING[v]
    if v == 'be':
        return 'being'
    if v.endswith('ie'):
        return v[:-2] + 'ying'
    if v.endswith('e') and not v.endswith('ee') and v not in ('be',):
        return v[:-1] + 'ing'
    return v + 'ing'


def s3(v):
    if v == 'be':
        return 'is'
    if v == 'have':
        return 'has'
    if v == 'do':
        return 'does'
    if v == 'go':
        return 'goes'
    if re.search(r'(s|sh|ch|x|z|o)$', v):
        return v + 'es'
    if v.endswith('y') and v[-2] not in 'aeiou':
        return v[:-1] + 'ies'
    return v + 's'


def pres(v, pl):
    if v == 'be':
        return 'are' if pl else 'is'
    return v if pl else s3(v)


def be_past(pl):
    return 'were' if pl else 'was'


def be_pres(pl):
    return 'are' if pl else 'is'


def have(pl):
    return 'have' if pl else 'has'


def cap(s):
    return s[0].upper() + s[1:] if s else s


def sent(*parts):
    return cap(' '.join(p for p in parts if p).replace(' ,', ',')) + '.'


def names(r, k=2):
    out = []
    while len(out) < k:
        n, p = person(r)
        if n not in [o[0] for o in out]:
            out.append((n, p))
    return out


def subst(t, r):
    """Fill {A}, {B} with names and {he}/{his}/{him}/{He}/{His} with A's pronouns, {bhe}... with B's."""
    (a, pa), (b, pb) = names(r)
    d = {'A': a, 'B': b}
    for k, v in pa.items():
        d[k] = v
    for k, v in pb.items():
        d['b' + k] = v
    return t.format(**d), d


def mcq_unique(stem, correct, wrong, key, r):
    seen, ws = {onorm(correct)}, []
    for w in wrong:
        if onorm(w) not in seen:
            ws.append(w)
            seen.add(onorm(w))
    need(len(ws) >= 3)
    return mcq(stem, correct, ws[:3], key, r)


# ---------------------------------------------------------------- engine: simple past and past continuous

PC_PAIRS = [
    ('{A}', 0, 'tell', 'a funny story in the court', 'the courtiers', 1, 'burst', 'into laughter'),
    ('the farmers', 1, 'sow', 'paddy in the fields', 'the first rain', 0, 'fall', ''),
    ('{A}', 0, 'cross', 'the busy street', 'a car', 0, 'stop', 'suddenly'),
    ('the children', 1, 'play', 'in the courtyard', 'the school bell', 0, 'ring', ''),
    ('{A}', 0, 'read', 'in the library', 'the lights', 1, 'go', 'out'),
    ('{A} and {B}', 1, 'wait', 'for the bus', 'a cold wind', 0, 'start', 'to blow'),
    ('the king', 0, 'listen', 'to the court poet', 'a messenger', 0, 'rush', 'into the hall'),
    ('the minister', 0, 'explain', 'his plan to the king', 'a guard', 0, 'interrupt', 'him'),
    ('{A}', 0, 'cook', 'dinner', 'the telephone', 0, 'ring', ''),
    ('the guards', 1, 'sleep', 'at the gate', 'the thief', 0, 'slip', 'into the palace'),
    ('{A}', 0, 'paint', 'a picture of the river', '{B}', 0, 'arrive', 'with a basket of mangoes'),
    ('the students', 1, 'write', 'their test', 'the fire alarm', 0, 'go', 'off'),
    ('{A}', 0, 'water', 'the plants', 'a bird', 0, 'fly', 'past the window'),
    ('the queen', 0, 'walk', 'in the palace garden', 'she', 0, 'hear', 'a strange sound'),
    ('{A}', 0, 'practise', 'the flute', 'the power', 0, 'fail', ''),
    ('the villagers', 1, 'celebrate', 'the harvest festival', 'a storm', 0, 'break', ''),
    ('the boatmen', 1, 'row', 'across the lake', 'the wind', 0, 'change', 'direction'),
    ('the merchant', 0, 'count', 'his coins', 'a monkey', 0, 'snatch', 'his cap'),
    ('{A}', 0, 'ride', 'to school', 'a dog', 0, 'run', 'across the road'),
    ('we', 1, 'have', 'lunch', 'the guests', 1, 'arrive', ''),
    ('{A}', 0, 'sing', 'at the annual function', 'the microphone', 0, 'stop', 'working'),
    ('the jester', 0, 'perform', 'his tricks', 'the king', 0, 'laugh', 'loudly'),
    ('the soldiers', 1, 'march', 'past the fort', 'the drums', 1, 'begin', 'to beat'),
    ('{A}', 0, 'climb', 'the steps of the temple', '{B}', 0, 'call', 'out to {him}'),
    ('the courtiers', 1, 'whisper', 'among themselves', 'the king', 0, 'enter', 'the hall'),
    ('{A}', 0, 'fly', 'a kite on the terrace', 'the string', 0, 'snap', ''),
    ('the shopkeeper', 0, 'close', 'his shop', 'a customer', 0, 'come', 'running'),
    ('my grandmother', 0, 'tell', 'us a folk tale', 'the lamp', 0, 'flicker', ''),
]
PC_TOPICS = ['a funny incident in your school assembly', 'the day the lights went out during a family dinner', 'a surprise at a village fair',
             'an unexpected visitor during a rainy evening', 'a misunderstanding between two friends and how it was solved',
             'a trick played on April Fools\' Day', 'a day at a crowded railway station']


def _pc(r):
    t = r.choice(PC_PAIRS)
    s1, pl1, v1, r1, s2, pl2, v2, r2 = t
    s1, d = subst(s1, r)
    r2 = r2.format(**d)
    s2 = s2.format(**d)
    return s1, pl1, v1, r1, s2, pl2, v2, r2


def pc_engine(ch, st, grade):
    def choose(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2 = _pc(r)
        frame = f'While {s1} ______ {r1}, {s2} {past(v2)} {r2}'.strip() + '.'
        c = f'{be_past(pl1)} {ing(v1)}'
        wrong = [f'{be_past(not pl1)} {ing(v1)}', f'{be_pres(pl1)} {ing(v1)}', f'will be {ing(v1)}']
        return mcq_unique(f'Choose the correct option to complete the sentence:\n"{frame}"', c, wrong,
                          f'The longer background action is in the past continuous ({be_past(pl1)} + -ing; "{s1}" takes "{be_past(pl1)}").', r)

    def choose2(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2 = _pc(r)
        frame = f'{cap(s1)} {be_past(pl1)} {ing(v1)} {r1} when {s2} ______ {r2}'.replace('  ', ' ').strip() + '.'
        c = past(v2)
        wrong = [pres(v2, pl2), f'{have(pl2)} {pp(v2)}', f'will {v2}']
        return mcq_unique(f'Choose the correct option:\n"{frame}"', c, wrong,
                          f'The short action that interrupts is in the simple past: "{c}".', r)

    def transform(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2 = _pc(r)
        q = f'While {s1} ({v1}) {r1}, {s2} ({v2}) {r2}'.strip() + '.'
        a = f'While {s1} {be_past(pl1)} {ing(v1)} {r1}, {s2} {past(v2)} {r2}'.strip() + '.'
        return {'stem': f'Put the verbs in brackets into the correct past tense form:\n"{q}"', 'answer': a,
                'key': f'"{a}" – past continuous for the background action, simple past for the interrupting action. 1 mark.', 'marks': 1}

    def transform2(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2 = _pc(r)
        a1 = f'{cap(s1)} {be_past(pl1)} {ing(v1)} {r1}.'.replace(' .', '.')
        a2 = f'{cap(s2)} {past(v2)} {r2}'.strip() + '.'
        ans = f'{cap(s1)} {be_past(pl1)} {ing(v1)} {r1} when {s2} {past(v2)} {r2}'.strip() + '.'
        alt = f'While {s1} {be_past(pl1)} {ing(v1)} {r1}, {s2} {past(v2)} {r2}'.strip() + '.'
        return {'stem': f'Combine the two sentences into one, using "when" or "while":\n{a1} {a2}', 'answer': ans,
                'key': f'"{ans}" or "{alt}" (2 marks: 1 for the connector, 1 for keeping the tenses correct.)', 'marks': 2}

    def error(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2 = _pc(r)
        kind = r.choice(['num', 'pp', 'ing'])
        if kind == 'num':
            w = f'While {s1} {be_past(not pl1)} {ing(v1)} {r1}, {s2} {past(v2)} {r2}'.strip() + '.'
            fix = f'"{be_past(not pl1)}" → "{be_past(pl1)}": the subject "{s1}" is {"plural" if pl1 else "singular"}.'
        elif kind == 'pp' and pp(v2) != past(v2):
            w = f'While {s1} {be_past(pl1)} {ing(v1)} {r1}, {s2} {pp(v2)} {r2}'.strip() + '.'
            fix = f'"{pp(v2)}" → "{past(v2)}": the simple past is needed; "{pp(v2)}" is the past participle and needs a helping verb.'
        else:
            w = f'While {s1} {be_past(pl1)} {v1} {r1}, {s2} {past(v2)} {r2}'.strip() + '.'
            fix = f'"{be_past(pl1)} {v1}" → "{be_past(pl1)} {ing(v1)}": the past continuous needs the -ing form.'
        return {'stem': f'Identify the error in this sentence and explain the correction:\n"{w}"', 'answer': fix,
                'key': f'{fix} (1 mark for the error, 1 for the correction with reason.)', 'marks': 2}

    rules = [
        ('The past continuous tense is formed with …', 'was/were + the -ing form of the verb', 'had + past participle', 'has/have + past participle', 'will be + past participle',
         'e.g. "was reading", "were playing".'),
        ('Which tense describes an action that was in progress at a time in the past?', 'Past continuous', 'Simple present', 'Present perfect', 'Future perfect',
         'It shows an ongoing past action.'),
        ('In "While I was reading, the lights went out", which action interrupted the other?', 'the lights went out', 'I was reading', 'Both happened at different times',
         'Neither', 'The short simple-past action interrupts the longer one.'),
        ('Which word often introduces the longer background action in the past continuous?', 'while', 'yesterday', 'already', 'since', '"While" + past continuous.'),
        ('Which tense is mainly used to narrate the main events of a story?', 'Simple past', 'Simple present', 'Future continuous', 'Present perfect continuous',
         'Narratives move forward in the simple past.'),
        ('Choose the correct past continuous form of "they sing".', 'they were singing', 'they was singing', 'they are singing', 'they sang', 'Plural subject: "were".'),
        ('Which sentence is in the simple past?', 'The king laughed at the joke.', 'The king was laughing at the joke.', 'The king has laughed at the joke.',
         'The king laughs at the joke.', 'Simple past = V2 (laughed).'),
    ]
    ars = [('In "While the farmers were sowing paddy, it began to rain", "were sowing" is in the past continuous.', '"were sowing" is in the simple past.',
            'The past continuous is formed with was/were and the -ing form of the verb.', 'The past continuous is formed with had and the past participle.',
            '"were + sowing" fits the was/were + -ing pattern.'),
           ('"The jester was performing when the king laughed" uses the simple past for the interrupting action.', 'The interrupting action is in the past continuous.',
            'A short action that breaks into a longer one is usually in the simple past.', 'A short action is always shown in the future tense.',
            '"laughed" is short and interrupts.'),
           ('"The children was playing" is incorrect.', '"The children was playing" is correct.', '"Children" is plural and takes "were".',
            '"Children" is singular and takes "was".', 'Plural subject → were.')]

    def write(r):
        t = r.choice(ch.get('topics', []) + PC_TOPICS)
        n, _ = person(r)
        return {'stem': f'{n} wants to narrate {t if t[0].islower() else "the topic: " + t} in a short paragraph (80–100 words). Write the paragraph. Use at least two verbs in the past '
                        'continuous and three in the simple past, and underline them.',
                'answer': 'A connected narrative paragraph with the required tense forms underlined.',
                'key': 'Content and sequence 2; correct past continuous (2 verbs) 1; correct simple past (3 verbs) 1; expression 1.', 'marks': 5}
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=transform2, error=error, write=write)


# ---------------------------------------------------------------- engine: reported speech

# (kind, direct, indirect) — indirect uses {x:wrong|right}; right may use S.he/S.his/S.him or L.he/L.his/L.him.
REP = [
    ('st', 'I am waiting for the king\'s reply.', '{p:I|S.he} {t:am|was} waiting for the king\'s reply'),
    ('st', 'I have solved the puzzle.', '{p:I|S.he} {t:have|had} solved the puzzle'),
    ('st', 'I will help you with the project.', '{p:I|S.he} {t:will|would} help {p:you|L.him} with the project'),
    ('st', 'You are the best runner in the team.', '{p:you|L.he} {t:are|was} the best runner in the team'),
    ('st', 'I can repair the old radio.', '{p:I|S.he} {t:can|could} repair the old radio'),
    ('st', 'My brother lives in Pune.', '{p:my|S.his} brother {t:lives|lived} in Pune'),
    ('st', 'I saw the camel near the well.', '{p:I|S.he} {t:saw|had seen} the camel near the well'),
    ('st', 'I am going to the market now.', '{p:I|S.he} {t:am going|was going} to the market {w:now|then}'),
    ('st', 'The bus will leave tomorrow.', 'the bus {t:will|would} leave {w:tomorrow|the next day}'),
    ('st', 'I met your teacher yesterday.', '{p:I|S.he} {t:met|had met} {p:your|L.his} teacher {w:yesterday|the previous day}'),
    ('st', 'I do not know the answer.', '{p:I|S.he} {t:do not|did not} know the answer'),
    ('st', 'You must finish this work today.', '{p:you|L.he} {t:must|had to} finish {w:this|that} work {w:today|that day}'),
    ('st', 'I may be late for practice.', '{p:I|S.he} {t:may|might} be late for practice'),
    ('st', 'We are planting saplings in the park.', '{p:we|they} {t:are|were} planting saplings in the park'),
    ('st', 'I found these coins in the garden.', '{p:I|S.he} {t:found|had found} {w:these|those} coins in the garden'),
    ('st', 'The camel is lame in one leg.', 'the camel {t:is|was} lame in one leg'),
    ('st', 'I have never seen such a clever trick.', '{p:I|S.he} {t:has|had} never seen such a clever trick'),
    ('st', 'I am proud of you.', '{p:I|S.he} {t:am|was} proud of {p:you|L.him}'),
    ('yn', 'Are you coming to the fair?', '{c:that if|if} {p:you|L.he} {t:are|was} coming to the fair'),
    ('yn', 'Have you seen my notebook?', '{c:that if|if} {p:you|L.he} {t:have|had} seen {p:my|S.his} notebook'),
    ('yn', 'Can you read this letter for me?', '{c:that if|if} {p:you|L.he} {t:can|could} read {w:this|that} letter for {p:me|S.him}'),
    ('yn', 'Did you lose a camel?', '{c:that if|if} {p:you|L.he} {t:lost|had lost} a camel'),
    ('yn', 'Will you join the drama club?', '{c:that if|if} {p:you|L.he} {t:will|would} join the drama club'),
    ('yn', 'Is the library open today?', '{c:that if|if} the library {t:is|was} open {w:today|that day}'),
    ('yn', 'Do you like folk tales?', '{c:that if|if} {p:you|L.he} {t:like|liked} folk tales'),
    ('wh', 'Where are you going?', '{c:that where|where} {p:you|L.he} {t:are|was} going'),
    ('wh', 'Why did you leave early?', '{c:that why|why} {p:you|L.he} {t:left|had left} early'),
    ('wh', 'What is your name?', '{c:that what|what} {p:your|L.his} name {t:is|was}'),
    ('wh', 'How did you find the way?', '{c:that how|how} {p:you|L.he} {t:found|had found} the way'),
    ('wh', 'When will the results come out?', '{c:that when|when} the results {t:will|would} come out'),
    ('wh', 'Who has taken my pen?', '{c:that who|who} {t:has|had} taken {p:my|S.his} pen'),
    ('wh', 'Which road leads to Ujjain?', '{c:that which|which} road {t:leads|led} to Ujjain'),
    ('wh', 'How many saplings have you planted?', '{c:that how many|how many} saplings {p:you|L.he} {t:have|had} planted'),
]
REP_CMD = [
    ('cmd', 'Close the door.', 'close the door'),
    ('cmd', 'Wait here.', 'wait {w:here|there}'),
    ('cmd', 'Bring me a glass of water.', 'bring {p:me|S.him} a glass of water'),
    ('cmd', 'Finish your homework first.', 'finish {p:your|L.his} homework first'),
    ('neg', 'Do not make a noise.', 'make a noise'),
    ('neg', 'Don\'t touch the wires.', 'touch the wires'),
    ('neg', 'Do not waste water.', 'waste water'),
    ('req', 'Please help me carry this bag.', 'help {p:me|S.him} carry {w:this|that} bag'),
    ('req', 'Please lend me your dictionary.', 'lend {p:me|S.him} {p:your|L.his} dictionary'),
    ('req', 'Kindly read this letter to me.', 'read {w:this|that} letter to {p:me|S.him}'),
    ('req', 'Please speak a little slowly.', 'speak a little slowly'),
]
SPEAKERS = [('the teacher', PRON_F), ('the coach', PRON_M), ('Grandpa', PRON_M), ('Grandma', PRON_F), ('the doctor', PRON_F),
            ('the king', PRON_M), ('the postman', PRON_M), ('the principal', PRON_F)]


def _who(r, roles=True):
    if roles and r.random() < 0.35:
        n, p = r.choice(SPEAKERS)
        return n, p
    return person(r)


def _resolve(t, S, L, mode):
    """mode: 'right' (correct), or a set of token types to leave wrong ({'t'}, {'p'}, {'c'})."""
    def rep(m):
        typ, wrong, right = m.group(1), m.group(2), m.group(3)
        val = wrong if (mode != 'right' and typ in mode) else right
        if val.startswith('S.'):
            return S[val[2:]]
        if val.startswith('L.'):
            return L[val[2:]]
        return val
    return re.sub(r'\{(\w):([^|}]*)\|([^}]*)\}', rep, t)


def rep_item(r, kinds=('st', 'yn', 'wh')):
    pool = [e for e in REP if e[0] in kinds] + [e for e in REP_CMD if e[0] in kinds]
    e = r.choice(pool)
    (sn, sp) = _who(r)
    (ln, lp) = person(r)
    while ln == sn:
        ln, lp = person(r)
    kind, direct, ind = e
    D = f'{cap(sn)} said to {ln}, "{direct}"'

    def make(mode):
        body = _resolve(ind, sp, lp, mode)
        if kind == 'st':
            return f'{cap(sn)} told {ln} that {body}.'
        if kind == 'yn':
            return f'{cap(sn)} asked {ln} {body}.'
        if kind == 'wh':
            return f'{cap(sn)} asked {ln} {body}.'
        if kind == 'cmd':
            return f'{cap(sn)} {"ordered" if sn in ("the king", "the coach") else "told"} {ln} to {body}.'
        if kind == 'neg':
            return f'{cap(sn)} told {ln} not to {body}.'
        return f'{cap(sn)} requested {ln} to {body}.'
    right = make('right')
    wrongs = []
    if '{p:' in ind:
        wrongs.append(make({'p'}))
        if '{t:' in ind:
            wrongs.append(make({'t', 'p'}))
    elif '{t:' in ind:
        wrongs.append(make({'t'}))
    if '{c:' in ind:
        wrongs.append(make({'c'}))
    if '{w:' in ind:
        wrongs.append(make({'w'}))
    if kind == 'st':
        wrongs.append(right.replace(f'told {ln} that', f'told to {ln} that'))
        wrongs.append(make({'t', 'p'}))
    elif kind in ('cmd', 'req'):
        wrongs.append(f'{cap(sn)} told {ln} that {_resolve(ind, sp, lp, "right")}.')
        wrongs.append(f'{cap(sn)} requested to {ln} that {ln} {_resolve(ind, sp, lp, "right")}.')
    elif kind == 'neg':
        wrongs.append(f'{cap(sn)} told {ln} to not {_resolve(ind, sp, lp, "right")}.')
        wrongs.append(f'{cap(sn)} told {ln} do not {_resolve(ind, sp, lp, "right")}.')
    else:
        wrongs.append(make({'t', 'p'}))
        wrongs.append(right[:-1] + '?')
    return D, right, wrongs, kind


REP_WHY = {'st': 'reporting verb "told" + listener + that; pronouns and tense change (present → past, past → past perfect, will → would, can → could).',
           'yn': 'yes/no question → asked + if/whether; question becomes a statement (no inversion, no question mark); tense and pronouns change.',
           'wh': 'wh-question → asked + the question word; statement word order; tense and pronouns change.',
           'cmd': 'command → told/ordered + listener + to-infinitive.', 'neg': 'negative command → told + listener + not to + verb.',
           'req': 'request → requested + listener + to-infinitive; "please" is dropped.'}


def rep_engine(ch, st, grade, kinds=('st', 'yn', 'wh')):
    def choose(r):
        D, right, wrongs, kind = rep_item(r, kinds)
        return mcq_unique(f'Choose the correct indirect (reported) form of:\n{D}', right, wrongs, f'Rule: {REP_WHY[kind]}', r)

    def choose2(r):
        D, right, wrongs, kind = rep_item(r, kinds)
        verb = {'st': 'told', 'yn': 'asked', 'wh': 'asked', 'cmd': 'told', 'neg': 'told', 'req': 'requested'}[kind]
        if kind == 'cmd' and ' ordered ' in right:
            verb = 'ordered'
        opts = {'told': ['asked', 'requested', 'said'], 'asked': ['told', 'said', 'ordered'], 'requested': ['ordered', 'said', 'asked that'],
                'ordered': ['said', 'spoke', 'talked']}[verb]
        if kind in ('cmd', 'neg'):
            opts = ['said', 'spoke', 'talked']
        blanked = right.replace(f' {verb} ', ' ______ ', 1)
        need(blanked != right)
        return mcq_unique(f'Choose the reporting verb that best completes the indirect speech of:\n{D}\n→ {blanked}', verb, opts,
                          f'"{verb}" suits a {dict(st="statement", yn="yes/no question", wh="wh-question", cmd="command", neg="negative command", req="request")[kind]}.', r)

    def transform(r):
        D, right, wrongs, kind = rep_item(r, kinds)
        return {'stem': f'Change into indirect speech:\n{D}', 'answer': right, 'key': f'"{right}" ({REP_WHY[kind]}) 1 mark.', 'marks': 1}

    def transform2(r):
        D, right, wrongs, kind = rep_item(r, kinds)
        return {'stem': f'Change the following into direct speech:\n{right}', 'answer': D,
                'key': f'"{D}" (Accept "{D.split(",")[0]}, …" with the original words in quotation marks.) 1 mark.', 'marks': 1}

    def error(r):
        D, right, wrongs, kind = rep_item(r, kinds)
        w = wrongs[0]
        return {'stem': f'A student reported this sentence:\n{D}\nas: "{w}"\nIdentify the mistake and write the correct indirect form.',
                'answer': right, 'key': f'Correct: "{right}". {REP_WHY[kind]} (1 mark error, 1 mark correction.)', 'marks': 2}

    def dialogue(r):
        sn, sp = _who(r, roles=False)
        ln, lp = person(r)
        while ln == sn:
            ln, lp = person(r)
        pool = [e for e in REP + REP_CMD if e[0] in kinds]
        es = r.sample(pool, 3)
        lines, outs = [], []
        for i, (kind, direct, ind) in enumerate(es):
            spk, lis, sP, lP = (sn, ln, sp, lp) if i % 2 == 0 else (ln, sn, lp, sp)
            lines.append(f'{spk}: "{direct}"')
            body = _resolve(ind, sP, lP, 'right')
            v = {'st': f'told {lis} that {body}', 'yn': f'asked {lis} {body}', 'wh': f'asked {lis} {body}', 'cmd': f'told {lis} to {body}',
                 'neg': f'told {lis} not to {body}', 'req': f'requested {lis} to {body}'}[kind]
            outs.append(f'{spk} {v}.')
        return {'stem': 'Report the following conversation in indirect speech, using suitable reporting verbs:\n' + '\n'.join(lines),
                'answer': ' '.join(outs), 'key': ' '.join(outs) + ' (1 mark for each line; accept "said that" for statements and suitable linkers such as "replied".)',
                'marks': 3, 'minutes': 4}

    rules = [
        ('When the reporting verb is in the past tense, "will" in direct speech usually becomes …', 'would', 'shall', 'will', 'had', 'will → would.'),
        ('In indirect speech, "yesterday" usually changes to …', 'the previous day', 'today', 'tomorrow', 'now', 'Time words move back.'),
        ('A yes/no question is reported with …', 'if or whether', 'that', 'to', 'because', 'asked + if/whether.'),
        ('In indirect speech, the simple present usually changes to the …', 'simple past', 'present perfect', 'future', 'present continuous', 'is → was, lives → lived.'),
        ('Which reporting verb suits a polite request?', 'requested', 'ordered', 'shouted', 'replied', '"Please …" → requested … to.'),
        ('"Here" in direct speech usually becomes … in indirect speech.', 'there', 'where', 'here', 'then', 'Place words change.'),
        ('In a reported wh-question, the word order is …', 'that of a statement (subject before verb)', 'that of a question (verb before subject)', 'reversed completely', 'unchanged with a question mark', 'No inversion.'),
        ('The simple past in direct speech usually changes to the … in indirect speech.', 'past perfect', 'simple present', 'future perfect', 'present continuous', 'saw → had seen.'),
        ('"This" in direct speech usually becomes … in indirect speech.', 'that', 'these', 'which', 'it', 'this → that.'),
    ]
    ars = [('In indirect speech, "I am tired," said Ravi becomes "Ravi said that he was tired."', 'The pronoun "I" stays as "I" in indirect speech.',
            'Pronouns and tenses change when the reporting verb is in the past.', 'Tenses never change in indirect speech.', 'Past reporting verb → backshift.'),
           ('A reported question does not end with a question mark.', 'A reported question must end with a question mark.',
            'In indirect speech, a question becomes a statement.', 'In indirect speech, a question stays a question.', 'It is now a statement.'),
           ('"Please open the window" is reported with "requested".', '"Please open the window" is reported with "ordered".',
            'Requests are reported with verbs such as requested or asked + to-infinitive.', 'Requests are reported with "that" + a question.', 'Polite request.')]

    def write(r):
        t = r.choice(ch.get('topics', []) + ['a festival', 'a school trip', 'a new hobby', 'a lost-and-found incident', 'a visit to a museum'])
        n, _ = person(r)
        n2, _ = person(r)
        return {'stem': f'{n} and {n2} had a conversation about {t}. Write a short paragraph (80–100 words) reporting their conversation. Use indirect speech for at least four '
                        'sentences, including one question and one request, and underline the reporting verbs.',
                'answer': 'A paragraph with correctly reported statements, a question and a request.',
                'key': 'Correct reporting verbs 1; tense/pronoun changes 2; content and coherence 1; expression 1.', 'marks': 5}
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=transform2, error=error,
                write=write, para=dialogue)


# ---------------------------------------------------------------- engine: modals of deduction (must, might, can't)

DED = [
    ('The lights are off and the door is locked.', 'The Nolans [M] be out.', 'must'),
    ('Tim has been working since dawn without a break.', 'He [M] be very tired.', 'must'),
    ('The footprints are tiny, about the size of a child\'s shoe.', 'The thief [M] be a tall man with big feet.', "can't"),
    ('I am not sure where the key is.', 'It [M] be in the drawer, but I haven\'t checked.', 'might'),
    ('The cake is still warm.', 'Someone [M] have baked it a short while ago.', 'must'),
    ('{A} was in Delhi at noon.', '{He} [M] be the person seen in Mumbai at noon.', "can't"),
    ('The phone is ringing, but I don\'t know who it is.', 'It [M] be Grandma calling.', 'might'),
    ('The dog is wagging its tail and jumping.', 'It [M] be happy to see us.', 'must'),
    ('The shop sign says "Closed on Sundays", and today is Sunday.', 'The shop [M] be open now.', "can't"),
    ('There are dark clouds, but the forecast is unclear.', 'It [M] rain later this evening.', 'might'),
    ('{A} has the encyclopedia open at the fifth word on the page.', '{He} [M] be checking the clue.', 'must'),
    ('The window was broken from the inside.', 'The burglar [M] have entered through the window from outside.', "can't"),
    ('{A} speaks fluent Tamil and often talks about Madurai.', '{He} [M] have lived in Tamil Nadu, or {he} may simply love the language.', 'might'),
    ('The note is written in green ink, and only the Chief uses green ink.', 'The Chief [M] have written the note.', 'must'),
    ('Nobody has entered the room since the morning, and the vase was fine then.', 'An outsider [M] have broken the vase.', "can't"),
    ('{A} hasn\'t replied to my message yet.', '{He} [M] be busy, or {he} may not have seen it.', 'might'),
    ('The milk smells sour.', 'It [M] have gone bad.', 'must'),
    ('{A} has just eaten a big lunch.', '{He} [M] be hungry already.', "can't"),
    ('The detective found a train ticket in the coat pocket, but it has no date on it.', 'The owner [M] have travelled recently.', 'might'),
    ('All the plants in the garden are wet, and the ground is muddy.', 'It [M] have rained last night.', 'must'),
    ('The safe was opened without being forced, and only two people knew the code.', 'One of the two [M] have opened it.', 'must'),
    ('The parcel is very light.', 'It [M] contain the heavy dictionary you ordered.', "can't"),
    ('There is a chance of traffic on the highway today.', 'We [M] reach the station a little late.', 'might'),
    ('{A} won every chess match at school this year.', '{He} [M] be a very good player.', 'must'),
]
DED_REWRITE = [
    ('I\'m sure {A} is at the station.', '{A} must be at the station.'),
    ('It is impossible that the thief is still inside the house.', 'The thief can\'t be still inside the house.'),
    ('Perhaps the letter is in the drawer.', 'The letter might be in the drawer.'),
    ('I\'m certain the parcel has arrived.', 'The parcel must have arrived.'),
    ('It\'s possible that {A} knows the answer.', '{A} might know the answer.'),
    ('I\'m sure that isn\'t the right road.', 'That can\'t be the right road.'),
    ('Maybe the clue is hidden in the book.', 'The clue might be hidden in the book.'),
    ('I\'m sure {A} forgot the meeting.', '{A} must have forgotten the meeting.'),
    ('It is impossible that {A} wrote this note.', '{A} can\'t have written this note.'),
    ('Perhaps it will snow in Shimla tonight.', 'It might snow in Shimla tonight.'),
    ('I\'m sure the museum is closed today.', 'The museum must be closed today.'),
    ('It\'s possible that the train is late.', 'The train might be late.'),
]
DED_CLUE = ['a muddy bicycle, a missing umbrella and an open window', 'an empty biscuit tin, crumbs on the sofa and a guilty-looking puppy',
            'a half-written letter, a cold cup of tea and a ringing phone', 'wet footprints, a dripping raincoat and a bunch of fresh flowers',
            'a torn map, a compass and a train ticket to Shimla', 'a page torn from an encyclopedia, a pencil and a coded note']
DED_WHY = {'must': '"must" shows the speaker is almost certain from the evidence.', "can't": '"can\'t" shows the speaker is sure something is impossible.',
           'might': '"might" shows it is only possible; the evidence is not strong.'}


def ded_engine(ch, st, grade):
    def _e(r):
        ev, concl, m = r.choice(DED)
        t, d = subst(ev + ' || ' + concl, r)
        ev, concl = t.split(' || ')
        return ev, concl, m

    def choose(r):
        ev, concl, m = _e(r)
        return mcq(f'Read the clue and choose the modal that best completes the deduction.\nClue: {ev}\nDeduction: {concl.replace("[M]", "______")}',
                   m, [x for x in ['must', "can't", 'might', "mustn't"] if x != m][:3], DED_WHY[m], r)

    def choose2(r):
        ev, concl, m = _e(r)
        opts = {'must': 'almost certain that it is true', "can't": 'sure that it is impossible', 'might': 'thinks it is possible but is not sure'}
        return mcq(f'Clue: {ev}\n"{concl.replace("[M]", m)}"\nWhat does the modal "{m}" show about the speaker?', opts[m],
                   [v for k, v in opts.items() if k != m] + ['is giving permission'], DED_WHY[m], r)

    def transform(r):
        a, b = r.choice(DED_REWRITE)
        t, d = subst(a + ' || ' + b, r)
        a, b = t.split(' || ')
        return {'stem': f'Rewrite the sentence using a modal of deduction (must, might/may/could, can\'t): "{a}"', 'answer': b,
                'key': f'"{b}" (accept may/could for might). 1 mark.', 'marks': 1}

    def transform2(r):
        ev, concl, m = _e(r)
        return {'stem': f'Complete the deduction with a suitable modal and give a reason for your choice.\nClue: {ev}\nDeduction: {concl.replace("[M]", "______")}',
                'answer': f'{m} – {DED_WHY[m]}', 'key': f'"{m}" (accept may/could for might). Reason: {DED_WHY[m]} 2 marks.', 'marks': 2}

    def error(r):
        ev, concl, m = _e(r)
        wrong = {'must': "can't", "can't": "mustn't", 'might': 'must'}[m]
        return {'stem': f'Clue: {ev}\nA student wrote: "{concl.replace("[M]", wrong)}"\nIs the modal correct? Correct it and explain.',
                'answer': f'No – it should be "{m}".', 'key': f'"{wrong}" → "{m}". {DED_WHY[m]}' + (' "mustn\'t" expresses prohibition, not deduction.' if wrong == "mustn't" else '') + ' 2 marks.', 'marks': 2}

    def write(r):
        c = r.choice(DED_CLUE)
        n, _ = person(r)
        return {'stem': f'Detective {n} enters a room and finds {c}. Write four or five sentences (60–80 words) in which {n} makes deductions about '
                        'what happened. Use must, might/could and can\'t at least once each, and give the clue behind each deduction.',
                'answer': 'Deductions linked to clues using must, might/could and can\'t correctly.',
                'key': 'Correct use of must (certainty), might/could (possibility), can\'t (impossibility): 3; each linked to a clue: 1; expression: 1.', 'marks': 5}
    rules = [
        ('Which modal shows that the speaker is almost certain something is true?', 'must', 'might', "can't", 'should', 'must = strong deduction.'),
        ('Which modal shows that something is impossible?', "can't", 'must', 'might', 'may', "can't = negative certainty."),
        ('Which modal shows only possibility?', 'might', 'must', "can't", "mustn't", 'might/may/could.'),
        ('The opposite of "He must be at home" (as a deduction) is …', "He can't be at home.", "He mustn't be at home.", 'He must not to be at home.', 'He might be at home.', "can't, not mustn't."),
        ('Which sentence is a deduction about the past?', 'She must have left early.', 'She must leave early.', 'She can leave early.', 'She should leave early.', 'modal + have + past participle.'),
        ('"Mustn\'t" is used to express …', 'prohibition', 'impossibility', 'possibility', 'certainty about the past', '"You mustn\'t smoke here."'),
    ]
    ars = [("In 'It can't be Tim – he is in London', the speaker is sure that it is not Tim.", "In 'It can't be Tim', the speaker thinks it might be Tim.",
            "'Can't' is used for a deduction that something is impossible.", "'Can't' is used to express strong certainty that something is true.", 'Negative deduction.'),
           ("'She must have forgotten' is a deduction about the past.", "'She must have forgotten' is an order.", "Modal + have + past participle refers to the past.",
            'Modal + have + past participle refers to the future.', 'must have + V3.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=transform2, error=error, write=write)


# ---------------------------------------------------------------- engine: present perfect vs simple past

PP_ANY = [('plant', 'a cherry seed'), ('water', 'the sapling'), ('visit', 'Mussoorie'), ('finish', 'the science project'), ('write', 'a letter to {his} cousin'),
          ('read', 'the new novel'), ('climb', 'the hill behind the school'), ('lose', 'the house key'), ('eat', 'all the cherries'), ('paint', 'the garden gate'),
          ('build', 'a fence around the plant'), ('meet', 'the forest officer'), ('clean', 'the courtyard'), ('take', 'a photograph of the blossoms'),
          ('see', 'a leopard near the stream'), ('pick', 'the ripe tomatoes')]
PP_COUNT = [('plant', 'ten saplings'), ('write', 'three letters'), ('read', 'five books'), ('take', 'twenty photographs'), ('visit', 'four hill stations'),
            ('pick', 'forty cherries'), ('collect', 'two hundred seeds'), ('make', 'six clay pots'), ('win', 'three medals')]
PP_STATE = [('live', 'in Dehradun'), ('know', 'the gardener'), ('have', 'this bicycle'), ('be', 'in the Eco Club'), ('work', 'at the plant nursery'),
            ('want', 'a garden of {his} own')]
PAST_CUES = ['yesterday', 'last week', 'last monsoon', 'two days ago', 'in 2023', 'an hour ago', 'last Sunday', 'last summer', 'three years ago']
SINCE_CUES = ['since 2019', 'since last winter', 'since {his} childhood', 'since the summer of 2021', 'since last spring']


def _pp_subj(r):
    if r.random() < 0.3:
        s = r.choice([('we', 1), ('my grandparents', 1), ('the children', 1), ('our neighbours', 1)])
        return s[0], s[1], {'his': 'their' if s[0] != 'we' else 'our', 'he': 'they', 'him': 'them'}
    n, p = person(r)
    return n, 0, p


def pp_engine(ch, st, grade):
    def item(r):
        s, pl, p = _pp_subj(r)
        kind = r.choice(['past', 'past', 'count', 'state'])
        if kind == 'past':
            v, o = r.choice(PP_ANY)
            cue = r.choice(PAST_CUES)
            right, tense = past(v), 'simple past'
            wrong = [f'{have(pl)} {pp(v)}', f'{be_pres(pl)} {ing(v)}', f'will {v}']
        elif kind == 'count':
            v, o = r.choice(PP_COUNT)
            cue = 'so far'
            right, tense = f'{have(pl)} {pp(v)}', 'present perfect'
            wrong = [past(v) if past(v) != pp(v) else f'{be_past(pl)} {ing(v)}', f'{be_pres(pl)} {ing(v)}', f'will {v}']
        else:
            v, o = r.choice(PP_STATE)
            cue = r.choice(SINCE_CUES)
            right, tense = f'{have(pl)} {pp(v)}', 'present perfect'
            wrong = [past(v) if v != 'be' else be_past(pl), f'{be_pres(pl)} {ing(v)}' if v != 'be' else f'{be_pres(pl)} being', f'will {v}']
        o = o.format(his=p['his'])
        cue = cue.format(his=p['his'])
        return s, pl, v, o, cue, right, tense, wrong, kind

    WHY = {'simple past': 'a finished past time ("{cue}") needs the simple past.',
           'present perfect': '"{cue}" links the past to the present, so the present perfect (has/have + past participle) is used.'}

    def choose(r):
        s, pl, v, o, cue, right, tense, wrong, kind = item(r)
        return mcq_unique(f'Choose the correct option:\n"{cap(s)} ______ {o} {cue}."', right, wrong, WHY[tense].format(cue=cue), r)

    def choose2(r):
        s, pl, v, o, cue, right, tense, wrong, kind = item(r)
        return mcq_unique(f'Which tense should fill the blank? "{cap(s)} ______ ({v}) {o} {cue}."', tense,
                          [t for t in ['simple past', 'present perfect', 'present continuous', 'simple future'] if t != tense], WHY[tense].format(cue=cue), r)

    def transform(r):
        s, pl, v, o, cue, right, tense, wrong, kind = item(r)
        return {'stem': f'Fill in the blank with the correct form of the verb in brackets: "{cap(s)} ______ ({v}) {o} {cue}."',
                'answer': right, 'key': f'"{right}" – {WHY[tense].format(cue=cue)} 1 mark.', 'marks': 1}

    def transform2(r):
        a = item(r)
        b = item(r)
        while b[8] == a[8] or b[0] == a[0]:
            b = item(r)
        q = ' '.join(f'({roman(i)}) {cap(x[0])} ______ ({x[2]}) {x[3]} {x[4]}.' for i, x in enumerate([a, b]))
        ans = f'(i) {a[5]} (ii) {b[5]}'
        return {'stem': f'Fill in the blanks with the simple past or the present perfect of the verbs in brackets:\n{q}', 'answer': ans,
                'key': f'{ans}. (i) {WHY[a[6]].format(cue=a[4])} (ii) {WHY[b[6]].format(cue=b[4])} 1 mark each.', 'marks': 2}

    def error(r):
        s, pl, v, o, cue, right, tense, wrong, kind = item(r)
        w = wrong[0]
        return {'stem': f'Correct the error in this sentence and give the reason: "{cap(s)} {w} {o} {cue}."',
                'answer': f'{w} → {right}', 'key': f'"{w}" → "{right}": {WHY[tense].format(cue=cue)} 2 marks.', 'marks': 2}

    def write(r):
        n, _ = person(r)
        t = r.choice(ch.get('topics', []) + ['a plant you have grown', 'changes in your neighbourhood over the years', 'a hobby you have kept up'])
        return {'stem': f'{n} is writing a diary entry (80–100 words) about {t}. Write it, using the present perfect at least three times (with '
                        'expressions like so far, since, already, never) and the simple past at least three times (with yesterday, last year, ago). Underline the verbs.',
                'answer': 'A diary entry using both tenses correctly with suitable time expressions.',
                'key': 'Diary format 1; correct present perfect with time expressions 1.5; correct simple past with time expressions 1.5; expression 1.', 'marks': 5}
    rules = [
        ('The present perfect tense is formed with …', 'has/have + past participle', 'had + past participle', 'was/were + -ing', 'did + base form', 'e.g. has planted.'),
        ('Which time expression goes with the simple past?', 'two days ago', 'so far', 'since 2019', 'already', 'A finished past time.'),
        ('Which time expression goes with the present perfect?', 'so far', 'yesterday', 'last week', 'in 2020', 'Up to now.'),
        ('Which sentence is correct?', 'Rakesh has planted the seed already.', 'Rakesh has planted the seed yesterday.', 'Rakesh planted the seed so far.', 'Rakesh has plant the seed.', 'already + present perfect.'),
        ('"Since" is followed by …', 'a point of time (since 2019)', 'a period of time (since three years)', 'a past participle', 'a future time', 'since + point of time.'),
        ('Which tense connects a past action with the present?', 'Present perfect', 'Simple past', 'Past perfect', 'Simple future', 'It shows present relevance.'),
    ]
    ars = [('"I have seen the film yesterday" is incorrect.', '"I have seen the film yesterday" is correct.',
            'The present perfect is not used with a finished past time such as "yesterday".', 'The present perfect must be used with "yesterday".', 'yesterday → simple past.'),
           ('"She has lived here since 2019" is correct.', '"She lived here since 2019" is correct.',
            '"Since" with a point of time shows an action continuing up to now, which needs the present perfect.', '"Since" always goes with the simple future.', 'since + present perfect.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=transform2, error=error, write=write)


# ---------------------------------------------------------------- engine: passive voice

# (tense, subject, subj_plural, agent (None = drop), verb, object, obj_plural, rest)
PAS = [
    ('pres', 'the technician', 0, 'the technician', 'check', 'the air purifier', 0, 'every morning'),
    ('pres', 'the crew', 0, 'the crew', 'test', 'the oxygen supply', 0, 'twice a day'),
    ('pres', 'people', 1, None, 'grow', 'rice', 0, 'in the Kaveri delta'),
    ('pres', 'the machine', 0, 'the machine', 'recycle', 'the waste water', 0, ''),
    ('pres', 'solar panels', 1, 'solar panels', 'produce', 'the station\'s electricity', 0, ''),
    ('pres', 'the scientists', 1, 'the scientists', 'record', 'the readings', 1, 'every hour'),
    ('past', 'Sven', 0, 'Sven', 'bring', 'a canary', 0, 'on board'),
    ('past', 'the alarm', 0, 'the alarm', 'wake', 'the captain', 0, 'at midnight'),
    ('past', 'the engineers', 1, 'the engineers', 'repair', 'the faulty pump', 0, 'in an hour'),
    ('past', 'someone', 0, None, 'open', 'the oxygen cylinder', 0, 'just in time'),
    ('past', 'the commander', 0, 'the commander', 'write', 'the report', 0, ''),
    ('past', 'the students', 1, 'the students', 'build', 'a model rocket', 0, ''),
    ('past', 'C. V. Raman', 0, 'C. V. Raman', 'discover', 'the Raman effect', 0, 'in 1928'),
    ('past', 'they', 1, None, 'launch', 'the satellite', 0, 'from Sriharikota'),
    ('perf', 'the team', 0, 'the team', 'complete', 'the experiment', 0, ''),
    ('perf', 'the doctor', 0, 'the doctor', 'examine', 'the astronauts', 1, ''),
    ('perf', 'the students', 1, 'the students', 'collect', 'the samples', 1, ''),
    ('perf', 'somebody', 0, None, 'switch', 'off the lights', 1, ''),
    ('fut', 'the crew', 0, 'the crew', 'send', 'the data', 0, 'to Earth tomorrow'),
    ('fut', 'the principal', 0, 'the principal', 'announce', 'the results', 1, 'on Monday'),
    ('fut', 'experts', 1, 'experts', 'study', 'the samples', 1, ''),
    ('modal', 'you', 1, None, 'store', 'the chemicals', 1, 'carefully'),
    ('modal', 'the pilot', 0, 'the pilot', 'follow', 'the safety rules', 1, ''),
    ('cont', 'the workers', 1, 'the workers', 'paint', 'the laboratory', 0, ''),
    ('cont', 'the astronaut', 0, 'the astronaut', 'feed', 'the canary', 0, ''),
]
OBJ_FORM = {'they': 'them', 'we': 'us', 'he': 'him', 'she': 'her', 'I': 'me', 'you': 'you'}


def _act(t):
    tense, S, spl, ag, v, O, opl, rest = t
    if tense == 'pres':
        vp = pres(v, spl)
    elif tense == 'past':
        vp = past(v)
    elif tense == 'perf':
        vp = f'{have(spl)} {pp(v)}'
    elif tense == 'fut':
        vp = f'will {v}'
    elif tense == 'modal':
        vp = f'must {v}'
    else:
        vp = f'{be_pres(spl)} {ing(v)}'
    return sent(S, vp, O, rest)


def _pas(t, err=None):
    tense, S, spl, ag, v, O, opl, rest = t
    part = pp(v)
    if err == 'part':
        if past(v) != pp(v):
            part = past(v)
        elif v in ('open', 'complete', 'clean', 'switch', 'test', 'record', 'study', 'store'):
            part = ing(v) + ' been'
        else:
            part = v
    pl = opl if err != 'num' else not opl
    if tense == 'pres':
        aux = be_pres(pl)
    elif tense == 'past':
        aux = be_past(pl)
    elif tense == 'perf':
        aux = f'{have(pl)} been'
    elif tense == 'fut':
        aux = 'will be'
    elif tense == 'modal':
        aux = 'must be'
    else:
        aux = f'{be_pres(pl)} being'
    if err == 'tense':
        aux = {'pres': be_past(pl), 'past': be_pres(pl), 'perf': be_past(pl), 'fut': be_pres(pl), 'modal': 'must', 'cont': be_pres(pl)}[tense]
    if v == 'switch' and O.startswith('off '):
        O, extra = O[4:], 'off '
        part = part + ' off'
    by = f'by {OBJ_FORM.get(ag, ag)}' if ag else ''
    return sent(O, aux, part, by, rest)


def pas_engine(ch, st, grade):
    def choose(r):
        t = r.choice(PAS)
        right = _pas(t)
        wrong = [_pas(t, 'num'), _pas(t, 'part'), _pas(t, 'tense'), _act(t)]
        return mcq_unique(f'Choose the correct passive form of:\n"{_act(t)}"', right, wrong,
                          'Object becomes subject; correct form of "be" for the tense and number + past participle; agent with "by" if needed.', r)

    def choose2(r):
        t = r.choice(PAS)
        right = _pas(t)
        a = _act(t)
        voice = r.choice(['active', 'passive'])
        s = a if voice == 'active' else right
        return mcq(f'Is this sentence in the active or the passive voice?\n"{s}"', voice.capitalize() + ' voice',
                   ['Passive voice' if voice == 'active' else 'Active voice', 'Neither: it is in reported speech', 'Both active and passive'],
                   f'{"The doer is the subject" if voice == "active" else "The receiver of the action is the subject; be + past participle"}.', r)

    def transform(r):
        t = r.choice(PAS)
        return {'stem': f'Change into the passive voice: "{_act(t)}"', 'answer': _pas(t),
                'key': f'"{_pas(t)}" (be-form for the tense + past participle{"; the agent can be dropped" if not t[3] else ""}). 1 mark.', 'marks': 1}

    def transform2(r):
        t = r.choice([x for x in PAS if x[3]])
        return {'stem': f'Change into the active voice: "{_pas(t)}"', 'answer': _act(t), 'key': f'"{_act(t)}" 1 mark.', 'marks': 1}

    def error(r):
        t = r.choice(PAS)
        kind = r.choice(['num', 'part']) if pp(t[4]) != past(t[4]) else 'num'
        w = _pas(t, kind)
        need(w != _pas(t))
        why = 'the verb "be" must agree with the new subject' if kind == 'num' else 'the passive needs the past participle (V3), not the simple past'
        return {'stem': f'A student changed "{_act(t)}" into "{w}". Identify the error and correct it.', 'answer': _pas(t),
                'key': f'Correct: "{_pas(t)}" – {why}. 2 marks.', 'marks': 2}

    PROC = ['how the air is kept fresh in a space station', 'how tea is processed from leaf to cup', 'how a clay pot is made', 'how waste paper is recycled',
            'how drinking water is purified in a city', 'how a school science exhibition was organised', 'how seeds are prepared for sowing']

    def write(r):
        p = r.choice(PROC)
        return {'stem': f'Write a short paragraph (60–80 words) describing {p}. Use the passive voice in at least five sentences and sequence words '
                        '(first, then, next, finally).', 'answer': 'A process description mainly in the passive voice.',
                'key': 'Correct passive forms (5) 2.5; logical sequence with linkers 1.5; expression 1.', 'marks': 5}
    rules = [
        ('The passive voice is formed with …', 'a form of "be" + past participle', 'has/have + base form', 'a form of "do" + base form', 'will + -ing form', 'be + V3.'),
        ('Why is the passive voice common in scientific writing?', 'It focuses on the process or result rather than on who did it', 'It is always shorter',
         'It makes writing more personal', 'It avoids verbs', 'Focus on the action.'),
        ('The passive of "The crew repaired the pump" is …', 'The pump was repaired by the crew.', 'The pump is repaired by the crew.', 'The pump was repair by the crew.',
         'The crew was repaired by the pump.', 'Past tense → was + V3.'),
        ('In the passive voice, the doer of the action is introduced with …', 'by', 'with', 'from', 'to', '"by the crew".'),
        ('Which sentence is in the passive voice?', 'The canary was fed by Sven.', 'Sven fed the canary.', 'Sven was feeding the canary.', 'The canary sang.', 'be + V3.'),
        ('The passive of the present perfect "They have cleaned the lab" is …', 'The lab has been cleaned.', 'The lab is cleaned.', 'The lab had cleaned.', 'The lab has cleaned.', 'has been + V3.'),
    ]
    ars = [('"The data will be sent tomorrow" is in the passive voice.', '"The data will be sent tomorrow" is in the active voice.',
            'It uses "will be" followed by the past participle "sent".', 'It uses "will" followed by the base form "send".', 'will be + V3 = future passive.'),
           ('In "Rice is grown in the Kaveri delta", the agent is left out.', '"Rice is grown in the Kaveri delta" names the agent.',
            'The agent is dropped when it is obvious or unimportant, such as "people".', 'The agent must always be stated in the passive.', 'Agent = people (obvious).')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=transform2, error=error, write=write)


# ---------------------------------------------------------------- engine: relative clauses

REL = [
    ('Bibha Chowdhuri was a physicist.', 'She studied cosmic rays.', 'who', 'Bibha Chowdhuri was a physicist {r} studied cosmic rays.'),
    ('This is the laboratory.', 'Its walls are covered with charts.', 'whose', 'This is the laboratory {r} walls are covered with charts.'),
    ('The telescope stood in the corner.', 'It was very old.', 'which', 'The telescope, {r} stood in the corner, was very old.'),
    ('{A} is the student.', '{His} model won the first prize.', 'whose', '{A} is the student {r} model won the first prize.'),
    ('I met a scientist.', 'She works at the Bose Institute.', 'who', 'I met a scientist {r} works at the Bose Institute.'),
    ('The book is on the table.', 'It explains particle physics simply.', 'which', 'The book {r} explains particle physics simply is on the table.'),
    ('We visited a village.', 'Its people make beautiful pots.', 'whose', 'We visited a village {r} people make beautiful pots.'),
    ('The girl is my cousin.', 'She topped the science olympiad.', 'who', 'The girl {r} topped the science olympiad is my cousin.'),
    ('Mumbai is a busy city.', 'It never sleeps.', 'which', 'Mumbai is a busy city {r} never sleeps.'),
    ('The professor guided many students.', 'Their research changed the field.', 'whose', 'The professor guided many students {r} research changed the field.'),
    ('{A} has a microscope.', 'It can magnify objects a hundred times.', 'which', '{A} has a microscope {r} can magnify objects a hundred times.'),
    ('The woman is a famous astronomer.', 'She gave the lecture.', 'who', 'The woman {r} gave the lecture is a famous astronomer.'),
    ('The experiment failed twice.', 'It finally succeeded.', 'which', 'The experiment, {r} failed twice, finally succeeded.'),
    ('The team included a young researcher.', 'Her ideas were bold.', 'whose', 'The team included a young researcher {r} ideas were bold.'),
    ('The cosmic rays come from outer space.', 'They strike the Earth constantly.', 'which', 'The cosmic rays {r} strike the Earth constantly come from outer space.'),
    ('Kalpana Chawla was an astronaut.', 'She was born in Karnal.', 'who', 'Kalpana Chawla was an astronaut {r} was born in Karnal.'),
    ('The star is named Bibha.', 'It is in the constellation Sextans.', 'which', 'The star {r} is in the constellation Sextans is named Bibha.'),
    ('The scientist won an award.', 'Her discovery helped farmers.', 'whose', 'The scientist {r} discovery helped farmers won an award.'),
    ('The students asked many questions.', 'They attended the workshop.', 'who', 'The students {r} attended the workshop asked many questions.'),
    ('The camera was expensive.', 'It recorded the experiment.', 'which', 'The camera {r} recorded the experiment was expensive.'),
]
REL_WHY = {'who': '"who" refers to a person and is the subject of the clause.', 'which': '"which" refers to a thing or an animal.',
           'whose': '"whose" shows possession (her/his/its/their …).'}


def rel_engine(ch, st, grade):
    def _e(r):
        a, b, rel, c = r.choice(REL)
        t, d = subst(a + ' || ' + b + ' || ' + c.replace('{r}', '[R]'), r)
        a, b, c = t.split(' || ')
        return a, b, rel, c.replace('[R]', '{r}')

    def choose(r):
        a, b, rel, c = _e(r)
        return mcq(f'Fill in the blank with the correct relative pronoun:\n"{c.replace("{r}", "______")}"', rel,
                   [x for x in ['who', 'which', 'whose', 'whom'] if x != rel][:3], REL_WHY[rel], r)

    def choose2(r):
        a, b, rel, c = _e(r)
        right = c.replace('{r}', rel)
        wrongs = [c.replace('{r}', x) for x in ['who', 'which', 'whose'] if x != rel] + [c.replace('{r}', 'whom')]
        return mcq(f'Which sentence correctly combines: "{a}" + "{b}"?', right, wrongs[:3], REL_WHY[rel], r)

    def transform(r):
        a, b, rel, c = _e(r)
        return {'stem': f'Combine the two sentences using a suitable relative pronoun (who, which, whose, that): {a} {b}', 'answer': c.replace('{r}', rel),
                'key': f'"{c.replace("{r}", rel)}" – {REL_WHY[rel]} (Accept "that" for who/which in defining clauses.) 1 mark.', 'marks': 1}

    def transform2(r):
        a, b, rel, c = _e(r)
        x = c.replace('{r}', rel)
        return {'stem': f'Underline the relative clause in this sentence and say what it describes: "{x}"', 'answer': f'Relative clause introduced by "{rel}"',
                'key': f'The clause beginning "{rel} …" gives more information about the noun just before it. {REL_WHY[rel]} 1 mark.', 'marks': 1}

    def error(r):
        a, b, rel, c = _e(r)
        wrong = {'who': 'which', 'which': 'who', 'whose': 'who'}[rel]
        return {'stem': f'Find and correct the error: "{c.replace("{r}", wrong)}"', 'answer': f'{wrong} → {rel}',
                'key': f'"{wrong}" → "{rel}": {REL_WHY[rel]} 2 marks.', 'marks': 2}

    def write(r):
        t = r.choice(['a woman scientist you admire', 'a teacher who inspired you', 'an Indian scientist who changed people\'s lives', 'a scientific instrument you would like to invent'])
        return {'stem': f'Write a short biographical paragraph (80–100 words) on {t}. Use at least three relative clauses with who, which and whose, and underline them.',
                'answer': 'A biographical paragraph with three correct relative clauses.',
                'key': 'Correct relative clauses (who, which, whose) 3; content and organisation 1; expression 1.', 'marks': 5}
    rules = [
        ('Which relative pronoun is used for people?', 'who', 'which', 'where', 'what', 'who → people.'),
        ('Which relative pronoun shows possession?', 'whose', 'who', 'which', 'whom', 'whose → possession.'),
        ('Which relative pronoun is used for things and animals?', 'which', 'who', 'whose only', 'whom', 'which → things.'),
        ('A non-defining relative clause is separated from the rest of the sentence by …', 'commas', 'a full stop', 'a colon', 'nothing', 'It adds extra information.'),
        ('In "The girl who won the quiz is my sister", the relative clause is …', 'who won the quiz', 'The girl', 'is my sister', 'my sister', 'It describes "the girl".'),
        ('"That" cannot be used in …', 'a non-defining relative clause', 'a defining relative clause', 'a clause about things', 'a clause about people', 'Not after a comma.'),
    ]
    ars = [('"Bibha Chowdhuri, who studied cosmic rays, was a pioneer" contains a non-defining relative clause.', 'It contains a defining relative clause.',
            'The clause between commas adds extra information about a person already identified.', 'The clause between commas identifies which person is meant.', 'Commas → non-defining.'),
           ('"whose" is correct in "the scientist whose discovery helped farmers".', '"who" is correct in "the scientist who discovery helped farmers".',
            '"Whose" shows possession: the discovery belongs to the scientist.', '"Whose" is used only for things.', 'Possession.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=transform2, error=error, write=write)


# ---------------------------------------------------------------- engine: sequence of tenses (g9)

SEQ = [
    ('Krishtakka said that she ______ to read the novel herself.', 'wanted', ['wants', 'will want', 'is wanting'], 'Past reporting verb → past tense in the clause.'),
    ('{A} knew that {he} ______ the bus if {he} did not hurry.', 'would miss', ['will miss', 'misses', 'has missed'], 'Past main verb → would.'),
    ('The teacher told us that the sun ______ in the east.', 'rises', ['rose', 'had risen', 'was rising'], 'A universal truth stays in the present tense.'),
    ('Grandmother said that she ______ the alphabet by the festival.', 'would learn', ['will learn', 'learns', 'is learning'], 'will → would after a past reporting verb.'),
    ('{A} thought that {his} friend ______ already left.', 'had', ['has', 'have', 'is'], 'An earlier past action → past perfect.'),
    ('Our science teacher explained that water ______ at 100 °C at sea level.', 'boils', ['boiled', 'had boiled', 'would boil'], 'Scientific fact → present tense.'),
    ('{A} said that {he} ______ (can) finish the project by Friday.', 'could', ['can', 'is able', 'will can'], 'can → could.'),
    ('The children noticed that their grandmother ______ crying.', 'was', ['is', 'has been', 'will be'], 'Past main verb → past continuous.'),
    ('{A} realised that {he} ______ {his} keys at home.', 'had left', ['has left', 'leaves', 'will leave'], 'The leaving happened earlier → past perfect.'),
    ('The guide told the tourists that honesty ______ the best policy.', 'is', ['was', 'had been', 'were'], 'A proverb or universal truth stays in the present.'),
    ('She worked hard so that she ______ (can) read the magazine on her own.', 'could', ['can', 'will', 'shall'], 'Past main clause → could in the purpose clause.'),
    ('{A} asked whether the library ______ open on Sundays.', 'was', ['is being', 'will be', 'has been being'], 'Past reporting verb → past tense.'),
    ('We hoped that the rain ______ before the match.', 'would stop', ['will stop', 'stops', 'has stopped'], 'Past main verb → would.'),
    ('The narrator remembered how her grandmother ______ for the next episode every week.', 'waited', ['waits', 'will wait', 'has waited'], 'Past context → past tense.'),
    ('{A} wondered why {his} brother ______ so late.', 'was', ['is', 'will be', 'has been'], 'Past main verb → past.'),
    ('Galileo proved that the Earth ______ round the Sun.', 'moves', ['moved', 'had moved', 'was moving'], 'A universal truth remains in the present.'),
]


def seq_engine(ch, st, grade):
    base = rep_engine(ch, st, grade, kinds=('st',))

    def choose(r):
        t, a, ws, why = r.choice(SEQ)
        t, d = subst(t, r)
        return mcq(f'Choose the correct option to complete the sentence:\n"{t}"', a, ws, why, r)

    def transform(r):
        t, a, ws, why = r.choice(SEQ)
        t, d = subst(t, r)
        return {'stem': f'Fill in the blank with the correct verb form, keeping the sequence of tenses: "{t}"', 'answer': a,
                'key': f'"{a}" – {why} 1 mark.', 'marks': 1}

    def error(r):
        t, a, ws, why = r.choice(SEQ)
        t, d = subst(t, r)
        w = ws[0]
        return {'stem': f'Find the error in the sequence of tenses and correct it: "{t.replace("______ (can)", "______").replace("______", w)}"', 'answer': f'{w} → {a}',
                'key': f'"{w}" → "{a}": {why} 2 marks.', 'marks': 2}
    rules = [
        ('According to the sequence of tenses, a past tense in the main clause is usually followed by …', 'a past tense in the subordinate clause', 'a present tense in the subordinate clause',
         'a future tense in the subordinate clause', 'no verb', 'Past → past.'),
        ('Which is an exception to the sequence of tenses?', 'A universal truth', 'A past habit', 'A completed action', 'A reported question', 'Universal truths stay present.'),
        ('Which sentence follows the sequence of tenses?', 'She said that she was tired.', 'She said that she is tired.', 'She said that she will be tired.', 'She says that she was tired yesterday will.', 'Past → past.'),
        ('Which sentence correctly states a universal truth in reported speech?', 'The teacher said that the Earth revolves round the Sun.', 'The teacher said that the Earth revolved round the Sun tomorrow.',
         'The teacher said that the Earth will revolve round the Sun.', 'The teacher said that the Earth had been revolving round the Sun yesterday.', 'Present for truths.'),
        ('If the main verb is in the present or future tense, the subordinate clause …', 'can be in any tense the sense needs', 'must be in the past', 'must be in the past perfect', 'must be in the future', 'Only past main verbs restrict.'),
    ]
    ars = [('"He said that honesty is the best policy" is correct.', '"He said that honesty is the best policy" is incorrect.',
            'A universal truth or proverb stays in the present even after a past reporting verb.', 'Every reported clause must change to the past.', 'Exception.'),
           ('"She knew that she would succeed" follows the sequence of tenses.', '"She knew that she will succeed" follows the sequence of tenses.',
            'A past main verb is followed by a past form such as "would".', 'A past main verb is followed by "will".', 'will → would.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=base['choose'], transform=transform, transform2=base['transform'], error=error, write=base['write'])


# ---------------------------------------------------------------- engine: modals for functions (g9)

MOD_FN = [
    ('Sentila can shape a pot without a wheel.', 'ability'), ('You may leave the class after the test.', 'permission'), ('Students must wear their ID cards.', 'obligation'),
    ('You should rest after a long journey.', 'advice'), ('It may rain in the evening.', 'possibility'), ('{A} could swim when {he} was five.', 'past ability'),
    ('Can I borrow your pencil?', 'permission'), ('We have to submit the form by Monday.', 'obligation'), ('You ought to thank your mother.', 'advice'),
    ('The potter might sell all his pots at the fair.', 'possibility'), ('May I come in, ma\'am?', 'permission'), ('You must not touch the hot kiln.', 'prohibition'),
    ('{A} can speak three languages.', 'ability'), ('You should drink more water in summer.', 'advice'), ('The train might be late today.', 'possibility'),
    ('Visitors must not feed the animals.', 'prohibition'), ('Could you pass me the clay, please?', 'request'), ('Will you help me with the coil?', 'request'),
]
MOD_FILL = [
    ('Arenla ______ make pots of many sizes. (ability)', 'can', ['must', 'should', 'may']),
    ('You ______ wear a helmet while riding. (obligation)', 'must', ['can', 'might', 'may']),
    ('______ I use your phone for a minute? (permission)', 'May', ['Must', 'Should', 'Ought']),
    ('You ______ see a doctor about that cough. (advice)', 'should', ['can', 'may', 'need']),
    ('Carry an umbrella; it ______ rain later. (possibility)', 'might', ['must', 'should', 'can\'t']),
    ('When {A} was young, {he} ______ climb trees easily. (past ability)', 'could', ['must', 'should', 'may']),
    ('Passengers ______ not cross the railway tracks. (prohibition)', 'must', ['can', 'might', 'would']),
    ('You ______ finish your homework before playing. (advice)', 'should', ['can', 'may', 'might']),
    ('______ you please lend me your notes? (polite request)', 'Could', ['Must', 'Should', 'Ought']),
    ('The clay ______ crack if it dries too quickly. (possibility)', 'may', ['must', 'should', 'shall']),
    ('Everyone ______ follow the school rules. (obligation)', 'must', ['might', 'could', 'may']),
    ('{A} ______ play the sitar beautifully. (ability)', 'can', ['must', 'should', 'need']),
]
MOD_REWRITE = [
    ('It is necessary for you to wear a helmet.', 'You must wear a helmet.'), ('It is a good idea for you to sleep early.', 'You should sleep early.'),
    ('Perhaps the potter is at the market.', 'The potter may/might be at the market.'), ('You are allowed to use the library after school.', 'You may/can use the library after school.'),
    ('{A} is able to make a pot in an hour.', '{A} can make a pot in an hour.'), ('You are not allowed to touch the exhibits.', 'You must not touch the exhibits.'),
    ('Is it all right if I open the window?', 'May/Can I open the window?'), ('{A} was able to read at the age of four.', '{A} could read at the age of four.'),
    ('It is advisable to save some money every month.', 'You should save some money every month.'), ('It is possible that the shop is closed.', 'The shop may/might be closed.'),
]


def modfn_engine(ch, st, grade):
    fns = sorted({f for _, f in MOD_FN})

    def choose(r):
        t, a, ws = r.choice(MOD_FILL)
        t, d = subst(t, r)
        return mcq(f'Choose the modal that fits the meaning shown in brackets:\n"{t}"', a, ws, f'"{a}" expresses the function in brackets.', r)

    def choose2(r):
        t, f = r.choice(MOD_FN)
        t, d = subst(t, r)
        clash = {'permission': {'request'}, 'request': {'permission'}, 'prohibition': {'obligation'}, 'obligation': {'prohibition'}}
        pool = [x for x in fns if x != f and not (x in f or f in x) and x not in clash.get(f, set())]
        return mcq(f'What function does the modal express in: "{t}"?', f, r.sample(pool, 3), f'It expresses {f}.', r)

    def transform(r):
        a, b = r.choice(MOD_REWRITE)
        t, d = subst(a + ' || ' + b, r)
        a, b = t.split(' || ')
        return {'stem': f'Rewrite the sentence using a suitable modal: "{a}"', 'answer': b, 'key': f'"{b}" 1 mark.', 'marks': 1}

    def transform2(r):
        t, a, ws = r.choice(MOD_FILL)
        t, d = subst(t, r)
        return {'stem': f'Fill in the blank with a suitable modal: "{t}"', 'answer': a, 'key': f'"{a}" (accept equivalents with the same function). 1 mark.', 'marks': 1}

    def error(r):
        t, a, ws = r.choice(MOD_FILL)
        t, d = subst(t, r)
        w = ws[0]
        return {'stem': f'The modal in this sentence does not express the meaning in brackets. Correct it and explain: "{t.replace("______", w)}"',
                'answer': f'{w} → {a}', 'key': f'"{w}" → "{a}": "{a}" expresses the function shown. 2 marks.', 'marks': 2}

    def write(r):
        t = r.choice(['rules for visitors to a pottery workshop', 'advice to a friend who wants to learn a craft', 'safety rules in a science laboratory', 'what you can and cannot do in a heritage museum'])
        return {'stem': f'Write a short paragraph (80–100 words) giving {t}. Use modals for ability, obligation, permission, possibility and advice, and underline them.',
                'answer': 'A paragraph using at least five modals with the stated functions.', 'key': 'Five modals used correctly for their functions 3; content 1; expression 1.', 'marks': 5}
    rules = [
        ('Which modal expresses advice?', 'should', 'can', 'may', 'will', 'should → advice.'), ('Which modal is used to ask permission politely?', 'May', 'Must', 'Should', 'Will', 'May I …?'),
        ('Which modal expresses past ability?', 'could', 'can', 'must', 'shall', 'could = past of can.'), ('"Must not" expresses …', 'prohibition', 'permission', 'ability', 'possibility', 'not allowed.'),
        ('Which modal expresses strong obligation?', 'must', 'might', 'could', 'may', 'must → obligation.'), ('Which sentence expresses possibility?', 'It might rain today.', 'You must rain today.', 'Can you rain?', 'You should rain.', 'might → possibility.'),
    ]
    ars = [('"You should wear a helmet" gives advice.', '"You should wear a helmet" gives permission.', '"Should" is used to give advice or suggest the right thing to do.', '"Should" is used only for past ability.', 'Advice.'),
           ('"May I come in?" is a request for permission.', '"May I come in?" expresses ability.', '"May" is used to ask for or give permission politely.', '"May" expresses strong obligation.', 'Permission.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=transform2, error=error, write=write)


# ---------------------------------------------------------------- engine: subject-verb concord (g9)

def _concord(r):
    """Return (sentence with ___, correct, plural?, rule)."""
    k = r.choice(['coll', 'neither', 'either', 'each', 'along', 'oneof', 'number', 'anumber', 'uncount', 'every_and', 'lot', 'manya', 'distance', 'subject_pl'])
    n, p = person(r)
    if k == 'coll':
        s = r.choice(['The team', 'The committee', 'The jury', 'The panel', 'Our class team'])
        c = r.choice(['______ ready for the final match.', '______ meeting in the hall today.', '______ happy with the decision.'])
        return f'{s} {c}', 'is', 0, 'A collective noun acting as one unit takes a singular verb.'
    if k in ('neither', 'either'):
        a = r.choice([('the coach', 0), ('the captain', 0), ('the players', 1), ('the athletes', 1), (n, 0), ('her teammates', 1)])
        b = r.choice([x for x in [('the coach', 0), ('the players', 1), ('the athletes', 1), ('the referee', 0), ('the volunteers', 1), ('the manager', 0)] if x[0] != a[0]])
        w1, w2 = ('Neither', 'nor') if k == 'neither' else ('Either', 'or')
        return f'{w1} {a[0]} {w2} {b[0]} ______ at the stadium.', 'are' if b[1] else 'is', b[1], f'With {w1.lower()} … {w2}, the verb agrees with the nearer subject ("{b[0]}").'
    if k == 'each':
        s = r.choice(['Each of the athletes', 'Each of the boys', 'Each of these medals', 'Each player', 'Every student'])
        return f'{s} ______ proud of the team.', 'is', 0, '"Each"/"every" takes a singular verb.'
    if k == 'along':
        w = r.choice(['along with', 'as well as', 'together with'])
        return f'{n}, {w} {p["his"]} teammates, ______ practising for the Paralympics.', 'is', 0, f'Words joined by "{w}" do not change the number of the first subject ("{n}").'
    if k == 'oneof':
        s = r.choice(['para-athletes', 'shot-put champions', 'medallists', 'coaches'])
        return f'One of the {s} ______ from our city.', 'is', 0, '"One of the + plural noun" takes a singular verb (the subject is "one").'
    if k == 'number':
        return f'The number of spectators ______ growing every year.', 'is', 0, '"The number of" is singular.'
    if k == 'anumber':
        return f'A number of volunteers ______ helping at the venue.', 'are', 1, '"A number of" means "many" and takes a plural verb.'
    if k == 'uncount':
        s = r.choice(['The news', 'The information', 'The sports equipment', 'His advice', 'Mathematics'])
        return f'{s} ______ very useful for the athletes.', 'is', 0, f'"{s.split()[-1]}" is uncountable/singular in meaning and takes a singular verb.'
    if k == 'every_and':
        return 'Every boy and girl ______ invited to the sports meet.', 'is', 0, '"Every … and …" takes a singular verb.'
    if k == 'lot':
        return 'A lot of people ______ waiting outside the stadium.', 'are', 1, '"A lot of" + plural noun takes a plural verb.'
    if k == 'manya':
        return 'Many a runner ______ dreamt of a gold medal.', 'has', 0, '"Many a" + singular noun takes a singular verb.'
    if k == 'distance':
        return f'Ten kilometres ______ a long distance for a wheelchair race.', 'is', 0, 'A distance thought of as one amount takes a singular verb.'
    s, h, rest = r.choice([('The ramps at the station', 'ramps', 'well maintained'), ('The new wheelchairs in the sports room', 'wheelchairs', 'light and strong'),
                           ('The para-athletes from Haryana', 'para-athletes', 'training for the national games'), ('The medals in the cabinet', 'medals', 'polished every week')])
    return f'{s} ______ {rest}.', 'are', 1, f'The head noun ("{h}") is plural.'


def concord_engine(ch, st, grade):
    def opts(c):
        if c == 'is':
            return ['is', 'are', 'were', 'being']
        if c == 'are':
            return ['are', 'is', 'was', 'being']
        return ['has', 'have', 'having', 'is having']

    def choose(r):
        s, c, pl, why = _concord(r)
        o = opts(c)
        return mcq(f'Choose the correct verb: "{s}"', c, [x for x in o if x != c], why, r)

    def transform(r):
        s, c, pl, why = _concord(r)
        base = 'have' if c in ('has', 'have') else 'be'
        return {'stem': f'Fill in the blank with the correct present-tense form of "{base}": "{s}"', 'answer': c, 'key': f'"{c}" – {why} 1 mark.', 'marks': 1}

    def error(r):
        s, c, pl, why = _concord(r)
        w = {'is': 'are', 'are': 'is', 'has': 'have'}[c]
        return {'stem': f'Identify and correct the error in subject-verb agreement: "{s.replace("______", w)}"', 'answer': f'{w} → {c}',
                'key': f'"{w}" → "{c}": {why} 2 marks.', 'marks': 2}

    def transform2(r):
        a = _concord(r)
        b = _concord(r)
        need(a[0] != b[0])
        ans = f'(i) {a[1]} (ii) {b[1]}'
        return {'stem': f'Fill in the blanks with is/are/has/have:\n(i) {a[0]}\n(ii) {b[0]}', 'answer': ans, 'key': f'{ans}. (i) {a[3]} (ii) {b[3]} 1 mark each.', 'marks': 2}

    def write(r):
        return {'stem': r.choice(['Write a short report (80–100 words) for the school magazine on a para-sports event. Use at least four of these subjects correctly with present-tense verbs: '
                                  'the team, each of the players, neither the coach nor the players, one of the athletes, a number of volunteers.',
                                  'Write a paragraph (80–100 words) on making your school accessible to everyone. Use at least four of: the committee, either the ramps or the lift, '
                                  'every student and teacher, the number of, the information.']),
                'answer': 'A report/paragraph with correct subject-verb agreement.', 'key': 'Four correct agreements 2; content 2; expression 1.', 'marks': 5}
    rules = [
        ('With "neither … nor", the verb agrees with …', 'the subject nearer to the verb', 'the first subject always', 'the longer subject', 'neither subject', 'Proximity rule.'),
        ('"Each of the players ___ a medal." Choose the verb.', 'has', 'have', 'are having', 'were having', 'Each → singular.'),
        ('Which is correct?', 'The news is good.', 'The news are good.', 'The news were good.', 'The news be good.', 'News is uncountable.'),
        ('"A number of" is followed by …', 'a plural noun and a plural verb', 'a singular noun and a singular verb', 'an uncountable noun', 'no verb', 'A number of = many.'),
        ('A collective noun such as "team", seen as one unit, usually takes …', 'a singular verb', 'a plural verb', 'no verb', 'only a past verb', 'Unit → singular.'),
        ('"One of my friends ___ a para-athlete." Choose the verb.', 'is', 'are', 'were', 'be', 'The subject is "one".'),
    ]
    ars = [('"Neither the coach nor the players are ready" is correct.', '"Neither the coach nor the players is ready" is correct.',
            'With neither … nor, the verb agrees with the nearer subject.', 'With neither … nor, the verb always agrees with the first subject.', 'players → are.'),
           ('"The number of para-athletes is increasing" is correct.', '"The number of para-athletes are increasing" is correct.',
            'The head of the subject is "number", which is singular.', 'The head of the subject is "para-athletes".', 'number → is.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose, transform=transform, transform2=transform2, error=error, write=write)


# ---------------------------------------------------------------- engine: conditionals type 1 (g9)

COND = [
    ('you', 1, 'practise', 'daily', 'you', 1, 'improve', 'quickly'), ('{A}', 0, 'study', 'hard', '{he}', 0, 'pass', 'the exam'),
    ('it', 0, 'rain', 'tomorrow', 'the match', 0, 'be', 'cancelled'), ('we', 1, 'leave', 'now', 'we', 1, 'catch', 'the train'),
    ('Shruti', 0, 'tell', 'her parents the truth', 'they', 1, 'understand', ''), ('you', 1, 'heat', 'ice', 'it', 0, 'melt', ''),
    ('the band', 0, 'win', 'the competition', 'it', 0, 'perform', 'on television'), ('{A}', 0, 'miss', 'the rehearsal', 'the director', 0, 'be', 'upset'),
    ('they', 1, 'save', 'water', 'the garden', 0, 'survive', 'the summer'), ('you', 1, 'call', 'me', 'I', 1, 'come', 'at once'),
    ('{A}', 0, 'join', 'the music club', '{he}', 0, 'learn', 'the tabla'), ('the twins', 1, 'sing', 'together', 'the audience', 0, 'love', 'it'),
    ('we', 1, 'plant', 'more trees', 'the air', 0, 'become', 'cleaner'), ('you', 1, 'not hurry', '', 'you', 1, 'miss', 'the bus'),
]


def _cond(r):
    t = r.choice(COND)
    s1, pl1, v1, r1, s2, pl2, v2, r2 = t
    s1, d = subst(s1, r)
    s2 = s2.format(**d)
    neg = v1.startswith('not ')
    v1b = v1[4:] if neg else v1
    pres1 = (('do not ' if pl1 else 'does not ') + v1b) if neg else pres(v1b, pl1 if s1 != 'I' else 1)
    if v2 == 'be' and r2 in ('cancelled', 'upset'):
        res = f'will be {r2}'
        r2 = ''
    else:
        res = f'will {v2}'
    return s1, pl1, v1b, r1, s2, pl2, v2, r2, pres1, res, neg


def cond_engine(ch, st, grade):
    def choose(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2, p1, res, neg = _cond(r)
        need(not neg)
        frame = f'If {s1} ______ {r1}, {s2} {res} {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        wrong = [f'will {v1}', past(v1) if past(v1) != p1 else f'had {pp(v1)}', pres(v1, not pl1) if pres(v1, not pl1) != p1 else ing(v1)]
        return mcq_unique(f'Choose the correct option (first conditional):\n"{cap(frame)}"', p1, wrong, 'In a first conditional, the if-clause takes the simple present; the main clause takes will + base form.', r)

    def choose2(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2, p1, res, neg = _cond(r)
        frame = f'If {s1} {p1} {r1}, {s2} ______ {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        base = res.split(' ', 1)[1]
        wrong = [f'would {base}', f'will {past(base.split()[0])}' + (' ' + base.split(' ', 1)[1] if ' ' in base else ''), f'had {base}' if base.split()[0] != 'be' else 'had been']
        return mcq_unique(f'Choose the correct option:\n"{cap(frame)}"', res, wrong, 'Main clause of a first conditional: will + base form.', r)

    def transform(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2, p1, res, neg = _cond(r)
        q = f'If {s1} ({"not " if neg else ""}{v1}) {r1}, {s2} ({v2}) {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        a = f'If {s1} {p1} {r1}, {s2} {res} {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        return {'stem': f'Complete the first conditional sentence with the correct forms of the verbs in brackets: "{cap(q)}"', 'answer': cap(a),
                'key': f'"{cap(a)}" – if + simple present, will + base form. 1 mark.', 'marks': 1}

    def transform2(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2, p1, res, neg = _cond(r)
        need(neg)
        a = f'Unless {s1} {pres(v1, pl1)} {r1}, {s2} {res} {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        q = f'If {s1} {p1} {r1}, {s2} {res} {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        return {'stem': f'Rewrite using "unless": "{cap(q)}"', 'answer': cap(a), 'key': f'"{cap(a)}" – unless = if … not. 1 mark.', 'marks': 1}

    def transform3(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2, p1, res, neg = _cond(r)
        need(not neg)
        a = f'If {s1} {p1} {r1}, {s2} {res} {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        imp = f'{cap(v1)} {r1}'.strip() + '.' if s1 == 'you' else None
        need(imp)
        return {'stem': f'Combine into one first-conditional sentence: "{imp} {cap(s2)} {res} {r2}".'.replace(' ".', '".').replace('  ', ' '),
                'answer': cap(a), 'key': f'"{cap(a)}" 1 mark.', 'marks': 1}

    def error(r):
        s1, pl1, v1, r1, s2, pl2, v2, r2, p1, res, neg = _cond(r)
        need(not neg)
        w = f'If {s1} will {v1} {r1}, {s2} {res} {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        a = f'If {s1} {p1} {r1}, {s2} {res} {r2}'.replace('  ', ' ').strip().replace(' ,', ',') + '.'
        return {'stem': f'Find and correct the error: "{cap(w)}"', 'answer': cap(a), 'key': f'"will {v1}" → "{p1}": the if-clause of a first conditional takes the simple present, not "will". 2 marks.', 'marks': 2}

    def tr(r):
        return (transform2 if r.random() < 0.3 else transform3 if r.random() < 0.4 else transform)(r)

    def write(r):
        return {'stem': r.choice(['Write a short message (80–100 words) to a friend who is nervous about a music competition. Use at least four first-conditional sentences (if/unless) to encourage them.',
                                  'Write a paragraph (80–100 words) on how small daily habits can change your future. Use at least four first-conditional sentences and underline them.']),
                'answer': 'A message/paragraph with four correct first conditionals.', 'key': 'Four correct first conditionals 2; content 2; expression 1.', 'marks': 5}
    rules = [
        ('A first conditional sentence talks about …', 'a real or likely situation in the future', 'an impossible past situation', 'a habit in the past', 'a universal truth only', 'Real future possibility.'),
        ('In a first conditional, the if-clause uses the …', 'simple present', 'simple future', 'past perfect', 'present perfect continuous', 'if + present.'),
        ('In a first conditional, the main clause usually uses …', 'will + base form', 'would + have + past participle', 'had + past participle', 'was/were + -ing', 'will + V1.'),
        ('"Unless" means …', 'if … not', 'because', 'although', 'so that', 'unless = if not.'),
        ('Which sentence is a correct first conditional?', 'If it rains, we will stay indoors.', 'If it will rain, we stay indoors.', 'If it rained, we will stay indoors.', 'If it rains, we stayed indoors.', 'if + present, will + base.'),
    ]
    ars = [('"If you practise daily, you will improve" is a first conditional.', '"If you practise daily, you will improve" is a third conditional.',
            'It uses the simple present in the if-clause and will + base form in the main clause.', 'It uses the past perfect in the if-clause.', 'Pattern of type 1.'),
           ('"If it will rain, the match will be cancelled" is incorrect.', '"If it will rain, the match will be cancelled" is correct.',
            '"Will" is not normally used in the if-clause of a first conditional.', '"Will" must be used in both clauses.', 'if + present.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=tr, error=error, write=write)


# ---------------------------------------------------------------- engine: determiners (g9)

ART = [('hour', 'an'), ('honest postman', 'an'), ('university', 'a'), ('umbrella', 'an'), ('one-rupee coin', 'a'), ('MLA', 'an'), ('useful tip', 'a'),
       ('envelope', 'an'), ('ordinary postcard', 'an'), ('hospital', 'a'), ('owl', 'an'), ('NGO', 'an'), ('union', 'a'), ('year', 'a'), ('eagle', 'an'),
       ('honour', 'an'), ('European tourist', 'a'), ('X-ray', 'an'), ('uniform', 'a'), ('inland letter', 'an'), ('village', 'a'), ('heir', 'an'),
       ('unique stamp', 'a'), ('old letter box', 'an'), ('SMS', 'an'), ('humble man', 'a'), ('urgent telegram', 'an'), ('user', 'a')]
COUNT = ['letters', 'parcels', 'money orders', 'postcards', 'inland letters', 'registered letters']
UNCOUNT = ['mail', 'luggage', 'money', 'cash']


def det_item(r):
    k = r.choice(['art', 'art', 'many', 'much', 'this', 'any', 'each'])
    if k == 'art':
        ws = r.sample(ART, 4)
        right = f'{ws[0][1]} {ws[0][0]}'
        wrong = [f'{"a" if a == "an" else "an"} {w}' for w, a in ws[1:]]
        return ('Which phrase uses the article correctly?', right, wrong,
                f'"{right}": "{ws[0][1]}" goes by the first sound of "{ws[0][0]}" ({"vowel" if ws[0][1] == "an" else "consonant"} sound).'), None
    if k == 'many':
        n = r.choice(COUNT)
        return (f'How ______ {n} did Khetaram deliver today?', 'many', ['much', 'little', 'a little'], f'"{n}" is countable → "many".'), 'many'
    if k == 'much':
        n = r.choice(UNCOUNT)
        return (f'How ______ {n} did the postman carry?', 'much', ['many', 'few', 'a few'], f'"{n}" is uncountable → "much".'), 'much'
    if k == 'this':
        n = r.choice(COUNT[:6])
        return (f'______ {n} on my desk must be posted today.', 'These', ['This', 'That', 'Each'], f'Plural "{n}", near the speaker → "These".'), None
    if k == 'any':
        n = r.choice(['stamps', 'envelopes', 'postcards', 'inland letters'])
        return (f'Sorry, there aren\'t ______ {n} left at the counter.', 'any', ['some', 'much', 'a'], 'Negative sentence → "any".'), None
    n = r.choice(['letter', 'parcel', 'envelope', 'money order'])
    return (f'______ {n} must carry the correct PIN code.', 'Every', ['All', 'Many', 'Few'], f'"Every" (or "Each") + singular noun ("{n}") with a singular verb.'), 'Every'


def det_engine(ch, st, grade):
    def choose(r):
        (q, a, ws, why), _ = det_item(r)
        return mcq(f'Choose the correct determiner/option:\n"{q}"' if '______' in q else q, a, ws, why, r)

    def transform(r):
        (q, a, ws, why), b = det_item(r)
        need(b)
        return {'stem': f'Fill in the blank with a suitable determiner: "{q}"', 'answer': a, 'key': f'"{a}" – {why} 1 mark.', 'marks': 1}

    def transform2(r):
        ws = r.sample(ART, 3)
        q = '; '.join(f'({roman(i)}) ___ {w}' for i, (w, _) in enumerate(ws))
        ans = '; '.join(f'({roman(i)}) {a} {w}' for i, (w, a) in enumerate(ws))
        return {'stem': f'Write "a" or "an" before each noun phrase: {q}', 'answer': ans, 'key': f'{ans}. Choose by the first sound, not the first letter. 1 mark (½ each, rounded).', 'marks': 1}

    def error(r):
        (q, a, ws, why), b = det_item(r)
        need(b)
        w = ws[0]
        s = q.replace('______', w)
        return {'stem': f'Identify and correct the error in the use of determiners: "{s[0].upper() + s[1:]}"', 'answer': f'{w} → {a}', 'key': f'"{w}" → "{a}": {why} 2 marks.', 'marks': 2}

    def write(r):
        return {'stem': r.choice(['Write a paragraph (80–100 words) describing a day in the life of a village postman. Use at least six different determiners (a/an/the, this/these, some/any, much/many, each/every) and underline them.',
                                  'Write a short notice-board article (80–100 words) on why handwritten letters still matter. Use at least six determiners correctly and underline them.']),
                'answer': 'A paragraph with six correct determiners.', 'key': 'Six correct determiners 3; content 1; expression 1.', 'marks': 5}
    rules = [
        ('Which article is used before "hour"?', 'an', 'a', 'the only', 'no article ever', 'The "h" is silent; vowel sound.'),
        ('"Much" is used with …', 'uncountable nouns', 'plural countable nouns', 'proper nouns', 'singular countable nouns only', 'much money, much time.'),
        ('Which is correct?', 'a university', 'an university', 'a hour', 'a honest man', 'University begins with a "yoo" (consonant) sound.'),
        ('"These" is used with …', 'plural nouns near the speaker', 'singular nouns far away', 'uncountable nouns', 'verbs', 'these + plural.'),
        ('"Any" is normally used in …', 'negative sentences and questions', 'only positive statements', 'only with singular nouns', 'only after "the"', 'any → negatives/questions.'),
        ('Articles, quantifiers and demonstratives are all kinds of …', 'determiners', 'pronouns', 'conjunctions', 'prepositions', 'They come before nouns.'),
    ]
    ars = [('"An honest postman" is correct.', '"A honest postman" is correct.', 'The article depends on the first sound; "honest" begins with a vowel sound.', 'The article depends only on the first letter.', 'Silent h.'),
           ('"How many letters?" is correct.', '"How much letters?" is correct.', '"Letters" is a countable noun.', '"Letters" is an uncountable noun.', 'many + countable.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose, transform=transform, transform2=transform2, error=error, write=write)


# ---------------------------------------------------------------- engine: noun clauses and relative clauses (g9)

NCL = [
    ('I know that {A} will follow {his} dream.', 'that {A} will follow {his} dream', 'noun clause', 'object of "know"'),
    ('What you believe shapes your future.', 'What you believe', 'noun clause', 'subject of the verb "shapes"'),
    ('The coach asked whether we were ready.', 'whether we were ready', 'noun clause', 'object of "asked"'),
    ('The girl who sings in the choir is my friend.', 'who sings in the choir', 'relative clause', 'describes "the girl"'),
    ('This is the dream that kept {A} going.', 'that kept {A} going', 'relative clause', 'describes "the dream"'),
    ('We wondered how the athlete trained so hard.', 'how the athlete trained so hard', 'noun clause', 'object of "wondered"'),
    ('The book which you lent me was inspiring.', 'which you lent me', 'relative clause', 'describes "the book"'),
    ('That hard work pays off is well known.', 'That hard work pays off', 'noun clause', 'subject of "is"'),
    ('{A} met a musician whose songs are famous.', 'whose songs are famous', 'relative clause', 'describes "a musician"'),
    ('My wish is that I become a pilot.', 'that I become a pilot', 'noun clause', 'complement of "is"'),
    ('Nobody knows where the treasure is hidden.', 'where the treasure is hidden', 'noun clause', 'object of "knows"'),
    ('The village where my grandparents live is near Udaipur.', 'where my grandparents live', 'relative clause', 'describes "the village"'),
    ('The teacher was pleased with what we had written.', 'what we had written', 'noun clause', 'object of the preposition "with"'),
    ('Students who set goals usually do well.', 'who set goals', 'relative clause', 'describes "students"'),
    ('{A} said that {he} would never give up.', 'that {he} would never give up', 'noun clause', 'object of "said"'),
    ('The day when we won the trophy was unforgettable.', 'when we won the trophy', 'relative clause', 'describes "the day"'),
]
NCL_JOIN = [
    ('{A} will succeed. I am sure of it.', 'that', 'I am sure that {A} will succeed.'), ('Where does {he} live? Do you know?', 'where', 'Do you know where {A} lives?'),
    ('Will the bus come on time? I wonder.', 'whether/if', 'I wonder whether the bus will come on time.'), ('You said something. It inspired me.', 'what', 'What you said inspired me.'),
    ('Dreams need effort. Everyone agrees.', 'that', 'Everyone agrees that dreams need effort.'), ('How did she win? Tell me.', 'how', 'Tell me how she won.'),
    ('Why was the match delayed? Nobody knows.', 'why', 'Nobody knows why the match was delayed.'), ('Is the shop open? Ask the guard.', 'whether/if', 'Ask the guard whether the shop is open.'),
]


def nrel_engine(ch, st, grade):
    def _n(r):
        s, c, typ, fn = r.choice(NCL)
        t, d = subst(s + ' || ' + c, r)
        s, c = t.split(' || ')
        return s, c, typ, fn

    def choose(r):
        s, c, typ, fn = _n(r)
        return mcq(f'In "{s}", the underlined part "{c}" is a …', typ, [x for x in ['noun clause', 'relative clause', 'adverb clause', 'phrase'] if x != typ], f'It is a {typ}: it {fn}.', r)

    def choose2(r):
        s, c, typ, fn = _n(r)
        need(typ == 'noun clause')
        fns = ['subject of the verb', 'object of the verb', 'complement', 'object of a preposition']
        main = 'subject of the verb' if fn.startswith('subject') else 'object of a preposition' if 'preposition' in fn else 'complement' if fn.startswith('complement') else 'object of the verb'
        return mcq(f'What is the function of the noun clause "{c}" in "{s}"?', main, [x for x in fns if x != main], f'It is the {fn}.', r)

    def transform(r):
        a, j, b = r.choice(NCL_JOIN)
        t, d = subst(a + ' || ' + b, r)
        a, b = t.split(' || ')
        return {'stem': f'Combine into one sentence using a noun clause (use "{j}"): {a}', 'answer': b, 'key': f'"{b}" 1 mark.', 'marks': 1}

    rel = rel_engine(ch, st, grade)

    def transform2(r):
        s, c, typ, fn = _n(r)
        return {'stem': f'Identify the subordinate clause in "{s}", name its type and state its function.', 'answer': f'"{c}" – {typ}; {fn}',
                'key': f'Clause: "{c}" (½); type: {typ} (½); function: {fn} (1). 2 marks.', 'marks': 2}

    def write(r):
        return {'stem': 'Write a paragraph (80–100 words) about a dream you want to follow. Use at least two noun clauses (that/what/whether) and two relative clauses (who/which/whose), and underline them.',
                'answer': 'A paragraph with two noun clauses and two relative clauses.', 'key': 'Noun clauses 2; relative clauses 2; expression 1.', 'marks': 5}
    rules = [
        ('A noun clause does the work of a …', 'noun', 'verb', 'adverb', 'preposition', 'It can be subject or object.'),
        ('A relative clause usually describes …', 'a noun that comes before it', 'the verb', 'the whole sentence\'s time', 'nothing', 'It works like an adjective.'),
        ('In "I know that you are honest", "that you are honest" is …', 'a noun clause', 'a relative clause', 'an adverb clause', 'a phrase', 'Object of "know".'),
        ('Which word commonly introduces a noun clause?', 'that', 'because', 'although', 'unless', '"that", "what", "whether".'),
        ('Which word commonly introduces a relative clause about a person?', 'who', 'whether', 'unless', 'because', 'who/whom/whose.'),
    ]
    ars = [('In "What you said inspired me", the noun clause is the subject.', 'In "What you said inspired me", the noun clause is the object.',
            'The clause "What you said" does the action of the verb "inspired".', 'The clause "What you said" receives the action of "inspired".', 'Subject position.'),
           ('"who sings in the choir" in "The girl who sings in the choir is my friend" is a relative clause.', 'It is a noun clause.',
            'It describes the noun "girl", like an adjective.', 'It is the object of the verb "is".', 'Adjective function.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose2, transform=transform, transform2=transform2, error=rel['error'], write=write)


# ---------------------------------------------------------------- engine: editing / omission / rearrangement (g9)

EDIT_BANK = [
    'Every dream begins with a small step taken with courage.', 'She decided to learn painting after she saw a mural in her town.',
    'The young athlete was practising in the rain when the coach arrived.', 'My grandfather has always encouraged me to follow my heart.',
    'The boy wanted to become a pilot, but his family could not afford the fees.', 'Hard work and patience are the keys to success.',
    'The girl who won the scholarship comes from a small village in Odisha.', 'Many people give up their dreams because they fear failure.',
    'He was the first student in his school to win a national award.', 'A good mentor helps a learner to see what is possible.',
    'They hoped to open a small library for the children of their area.', 'The coach was watching every move the players made.',
    'Our teacher told us that dreams need both effort and planning.', 'She is the most determined person I have ever met.',
    'An old musician taught the children to play the flute.', 'The students were preparing for the science fair all week.',
]
OMIT = [(r'\b(?:wanted|decided|hoped|tried|planned|learnt|learned|began|wished|chose|refused|agreed|promised|helps|encouraged) (to) ', 'to'),
        (r'\b(was|were|is|are) (?=\w+ing\b)', None), (r'\b(the) (?=(?:most|first|best|keys)\b)', 'the')]


def omission(s, r):
    cands = []
    for pat, w in OMIT:
        for m in re.finditer(pat, s):
            cands.append((m.start(1), m.end(1), m.group(1)))
    if not cands:
        return None
    a, b, w = r.choice(cands)
    before = s[:a].rstrip().split()[-1] if s[:a].strip() else '(start)'
    after = s[b:].lstrip().split()[0]
    return (s[:a] + s[b:].lstrip()).replace('  ', ' '), w, before, after


def edit_engine(ch, st, grade):
    bank = EDIT_BANK + list(st.get('sentences', []))

    def choose(r):
        s = r.choice(bank)
        x = inject_error(s, r)
        need(x)
        wrong, w, c = x
        alts = {'is': ['are', 'were', 'be'], 'are': ['is', 'was', 'be'], 'was': ['were', 'are', 'be'], 'were': ['was', 'is', 'be'], 'has': ['have', 'having', 'be'],
                'have': ['has', 'having', 'is'], 'does': ['do', 'doing', 'be'], 'do': ['does', 'doing', 'be']}
        need(c in alts)
        ds = alts[c]
        ds = [d for d in ds if d != c][:3]
        if w not in ds:
            ds = [w] + ds[:2]
        return mcq_unique(f'The sentence has one error. Choose the correct replacement for the wrong word:\n"{wrong}"', c, ds, f'"{w}" → "{c}". Correct: "{s}"', r)

    def transform(r):
        s = r.choice(bank)
        x = inject_error(s, r)
        need(x)
        wrong, w, c = x
        return {'stem': f'Identify the error and write the correction (editing):\n"{wrong}"', 'answer': f'{w} → {c}', 'key': f'"{w}" → "{c}". Correct: "{s}" 1 mark.', 'marks': 1}

    def transform2(r):
        s = r.choice(bank)
        x = omission(s, r)
        need(x)
        o, w, b, a = x
        return {'stem': f'One word is missing in this sentence. Write the missing word along with the words before and after it (omission):\n"{o}"',
                'answer': f'{b} {w} {a}', 'key': f'Missing word "{w}" between "{b}" and "{a}". Correct: "{s}" 1 mark.', 'marks': 1}

    def rearr(r):
        s = r.choice(bank)
        j = jumble(s, r)
        need(j)
        return {'stem': f'Rearrange the words and phrases to form a meaningful sentence:\n{j}', 'answer': s, 'key': f'"{s}" 1 mark.', 'marks': 1}

    def error(r):
        s = r.choice(bank)
        x = inject_error(s, r)
        need(x)
        wrong, w, c = x
        return {'stem': f'Explain why the following sentence is incorrect and rewrite it correctly:\n"{wrong}"', 'answer': s,
                'key': f'"{w}" should be "{c}" ({"agreement/tense" if c in ("is", "are", "was", "were", "has", "have", "do", "does") else "article before a vowel/consonant sound" if c.lower() in ("a", "an") else "verb form: simple past needed, not the past participle"}). Correct: "{s}" 2 marks.', 'marks': 2}

    def para(r):
        ss = r.sample(bank, 4)
        out, keys = [], []
        for i, s in enumerate(ss):
            x = inject_error(s, r)
            need(x)
            out.append(x[0])
            keys.append(f'({roman(i)}) {x[1]} → {x[2]}')
        return {'stem': 'The following paragraph has one error in each sentence. Write the incorrect word and the correction for each:\n' + ' '.join(out),
                'answer': '; '.join(keys), 'key': '; '.join(keys) + ' (1 mark each.)', 'marks': 4, 'minutes': 5}

    def write(r):
        return para(r)
    rules = [
        ('In an editing task, each line usually has …', 'one error to be identified and corrected', 'no errors', 'three missing words', 'a spelling error only', 'One error per line.'),
        ('In an omission task, the answer is written as …', 'the word before, the missing word and the word after', 'only the full corrected paragraph', 'the number of the line only', 'the wrong word only', 'Show position.'),
        ('Which of these is most likely the error in "She have finished her work"?', 'have → has', 'She → Her', 'finished → finish', 'work → works', 'Subject-verb agreement.'),
        ('Which is correct?', 'an old letter', 'a old letter', 'an letter', 'a apple', '"an" before a vowel sound.'),
        ('Before rearranging jumbled words, it helps to find the …', 'subject and the main verb', 'longest word', 'last word', 'punctuation only', 'Build the core first.'),
    ]
    ars = [('"He has went home" contains an error.', '"He has went home" is correct.', 'After "has", the past participle "gone" is needed.', 'After "has", the simple past is always used.', 'has + V3.'),
           ('"She decided learn painting" has a missing word.', '"She decided learn painting" is complete.', '"Decided" is followed by a to-infinitive.', '"Decided" is followed by an -ing form only.', 'decided to.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose, transform=transform, transform2=lambda r: (transform2 if r.random() < 0.5 else rearr)(r),
                error=error, write=write, para=para)


# ---------------------------------------------------------------- engine: sentence transformation (g9)

TRANS = [
    ('{A} is too tired to run.', 'Use "so … that".', '{A} is so tired that {he} cannot run.'),
    ('As soon as {A} heard the news, {he} smiled.', 'Begin with "No sooner".', 'No sooner had {A} heard the news than {he} smiled.'),
    ('Only a determined person can succeed.', 'Begin with "None but".', 'None but a determined person can succeed.'),
    ('Everyone admires {A}\'s courage.', 'Make it negative without changing the meaning.', 'There is no one who does not admire {A}\'s courage.'),
    ('{A} is the best singer in the class.', 'Use the comparative degree.', '{A} is better than any other singer in the class.'),
    ('Being tired, {A} went to bed early.', 'Make it a complex sentence using "because".', 'Because {A} was tired, {he} went to bed early.'),
    ('In spite of the rain, {A} went to practice.', 'Begin with "Although".', 'Although it was raining, {A} went to practice.'),
    ('{A} must work hard to win the race.', 'Use "If … not".', 'If {A} does not work hard, {he} will not win the race.'),
    ('I always remember my first stage performance.', 'Make it negative.', 'I never forget my first stage performance.'),
    ('{A} is as tall as {B}.', 'Make it negative using the comparative.', '{A} is not taller than {B}.'),
    ('The task was very difficult, but {A} completed it.', 'Make it complex using "Although".', 'Although the task was very difficult, {A} completed it.'),
    ('{A} said, "I believe in myself."', 'Change into indirect speech.', '{A} said that {he} believed in {himself}.'),
    ('Believe in yourself, and you will succeed.', 'Use "If".', 'If you believe in yourself, you will succeed.'),
    ('Unless you try, you cannot win.', 'Use "If … not".', 'If you do not try, you cannot win.'),
    ('{A} was so weak that {he} could not walk.', 'Use "too … to".', '{A} was too weak to walk.'),
    ('Very few cities in India are as clean as Indore.', 'Use the superlative degree.', 'Indore is one of the cleanest cities in India.'),
    ('No other river in India is as long as the Ganga.', 'Use the superlative degree.', 'The Ganga is the longest river in India.'),
    ('{A} confessed {his} mistake.', 'Make it a complex sentence using "that".', '{A} confessed that {he} had made a mistake.'),
    ('The coach praised the players. They had won the match.', 'Combine into a simple sentence.', 'The coach praised the players for winning the match.'),
    ('{A} completed the race. {He} collapsed.', 'Combine using "as soon as".', 'As soon as {A} completed the race, {he} collapsed.'),
    ('It is never too late to learn.', 'Make it affirmative.', 'It is always the right time to learn.'),
    ('{A} did not reach on time. {He} missed the bus.', 'Combine using "because".', '{A} did not reach on time because {he} missed the bus.'),
]
TRANS_WRONG = {
    0: ['{A} is so tired that {he} can run.', '{A} is very tired to run.', '{A} is too tired that {he} cannot run.'],
    1: ['No sooner {A} heard the news than {he} smiled.', 'No sooner had {A} heard the news when {he} smiled.', 'No sooner did {A} heard the news than {he} smiled.'],
    4: ['{A} is better than all singer in the class.', '{A} is best than any other singer in the class.', '{A} is better than any singer in the class.'],
    6: ['Although it was raining, but {A} went to practice.', 'Although of the rain, {A} went to practice.', 'Although raining, {A} did not go to practice.'],
    14: ['{A} was too weak that {he} could not walk.', '{A} was too weak to not walk.', '{A} was so weak to walk.'],
    16: ['The Ganga is longer river in India.', 'The Ganga is the longer than all rivers.', 'The Ganga is the most long river in India.'],
}


def trans_engine(ch, st, grade):
    def _t(r, only=None):
        i = r.choice(only) if only else r.randrange(len(TRANS))
        a, ins, b = TRANS[i]
        t, d = subst(a + ' || ' + b, r)
        a, b = t.split(' || ')
        return i, a, ins, b, d

    def choose(r):
        i, a, ins, b, d = _t(r, list(TRANS_WRONG))
        ws = [w.format(**d) for w in TRANS_WRONG[i]]
        return mcq(f'Choose the correct transformation of "{a}" ({ins})', b, ws, f'"{b}"', r)

    def transform(r):
        i, a, ins, b, d = _t(r)
        return {'stem': f'Rewrite as directed: "{a}" ({ins})', 'answer': b, 'key': f'"{b}" (accept equivalent correct forms). 1 mark.', 'marks': 1}

    def transform2(r):
        i, a, ins, b, d = _t(r)
        return {'stem': f'Rewrite the sentence as directed and say whether the meaning has changed: "{a}" ({ins})', 'answer': f'{b} – meaning unchanged',
                'key': f'"{b}" 1 mark; meaning unchanged 1 mark.', 'marks': 2}

    def error(r):
        i, a, ins, b, d = _t(r, list(TRANS_WRONG))
        w = TRANS_WRONG[i][0].format(**d)
        return {'stem': f'A student was asked to transform "{a}" ({ins}) and wrote: "{w}". What is wrong? Write the correct form.', 'answer': b,
                'key': f'Correct: "{b}". The student\'s version changes the meaning or breaks the pattern. 2 marks.', 'marks': 2}

    def write(r):
        picks = r.sample(range(len(TRANS)), 3)
        lines, ans = [], []
        for k, i in enumerate(picks):
            a, ins, b = TRANS[i]
            t, d = subst(a + ' || ' + b, r)
            a, b = t.split(' || ')
            lines.append(f'({roman(k)}) {a} ({ins})')
            ans.append(f'({roman(k)}) {b}')
        return {'stem': 'Rewrite as directed:\n' + '\n'.join(lines), 'answer': ' '.join(ans), 'key': ' '.join(ans) + ' (1 mark each.)', 'marks': 3, 'minutes': 4}
    rules = [
        ('"Too … to" can be rewritten using …', 'so … that … not', 'as … as', 'no sooner … than', 'not only … but also', 'too tired to run = so tired that cannot run.'),
        ('"No sooner" is followed by …', 'had + subject + past participle … than', 'did + subject … when', 'subject + verb … then', 'will + subject … than', 'No sooner had … than.'),
        ('A complex sentence has …', 'one main clause and at least one subordinate clause', 'two main clauses only', 'no verb', 'only a phrase', 'Subordinate clause.'),
        ('Which word introduces a clause of contrast?', 'although', 'because', 'unless', 'so that', 'although = contrast.'),
        ('"Only he can do it" in negative form is …', 'None but he can do it.', 'Only he cannot do it.', 'He cannot do it only.', 'Nobody can do it.', 'Only → None but.'),
    ]
    ars = [('"She is too weak to walk" means the same as "She is so weak that she cannot walk".', '"She is too weak to walk" means she can walk.',
            '"Too … to" has a negative meaning.', '"Too … to" has a positive meaning.', 'too = excessively, so cannot.'),
           ('"Although" and "but" should not be used together in one sentence.', '"Although" and "but" should always be used together.',
            'Both words show contrast, so using both is repetitive.', '"Although" shows cause, not contrast.', 'Double connector.')]
    return dict(rules=rules, ar=ars, choose=choose, choose2=choose, transform=transform, transform2=transform2, error=error, write=write, para=write)


ENGINES = {'past_cont': pc_engine, 'reported': rep_engine, 'reported_ext': lambda ch, st, g: rep_engine(ch, st, g, kinds=('st', 'yn', 'wh', 'cmd', 'neg', 'req')),
           'deduction': ded_engine, 'pres_perf': pp_engine, 'passive': pas_engine, 'relative': rel_engine, 'seq_tenses': seq_engine,
           'modals': modfn_engine, 'concord': concord_engine, 'cond1': cond_engine, 'determiners': det_engine, 'noun_rel': nrel_engine,
           'editing': edit_engine, 'transform': trans_engine}


def _gsig(stem):
    """Signatures (content words, names dropped) of the parts of a grammar item: each gapped clause, else the quoted
    part, else the whole stem. Used to keep near-identical frames out of one set."""
    parts = re.findall(r'[^\n"]*______[^\n"]*', stem) or re.findall(r'"([^"]{8,})"', stem) or [stem]
    out = []
    for q in parts:
        w = frozenset(x.lower() for x in re.findall(r"[A-Za-z'-]+", q) if len(x) > 3 and not x[0].isupper())
        if w:
            out.append(w)
    return out


def _inner(s):
    """Relabel an item's own (i), (ii) … parts as (a), (b) … so they do not clash with the set's numbering."""
    return re.sub(r'\((i|ii|iii|iv|v)\)', lambda m: '(' + 'abcde'[['i', 'ii', 'iii', 'iv', 'v'].index(m.group(1))] + ')', s)


def gram_set(E, n, r, mix=('transform', 'transform2', 'choose')):
    lines, ans = [], []
    seen = set()
    sigs = []
    tries = 0
    while len(lines) < n and tries < 60:
        tries += 1
        g = E[r.choice(mix)]
        try:
            v = g(r)
        except (ValueError, IndexError):
            continue
        if v['stem'] in seen:
            continue
        sig = _gsig(v['stem'])
        if any(len(a & b) / len(a | b) > 0.6 for a in sig for b in sigs):
            continue
        if any(len(a & b) / len(a | b) > 0.6 for i_, a in enumerate(sig) for b in sig[i_ + 1:]):
            continue
        seen.add(v['stem'])
        sigs.extend(sig)
        i = len(lines)
        if not v.get('options'):
            v = dict(v, stem=_inner(v['stem']), answer=_inner(v['answer']))
        if v.get('options'):
            lines.append(f'({roman(i)}) {v["stem"]}  {inline_opts(v["options"])}')
            ans.append(f'({roman(i)}) ({"abcd"[v["options"].index(v["answer"])]}) {v["answer"]}')
        else:
            lines.append(f'({roman(i)}) {v["stem"]}')
            ans.append(f'({roman(i)}) {v["answer"]}')
    need(len(lines) == n)
    a = ' '.join(ans)
    return {'stem': 'Attempt the following grammar items as directed.\n' + '\n'.join(lines), 'answer': a, 'key': a + ' (1 mark each.)', 'marks': n, 'minutes': n + 1}


def gram_families(st, ch, grade):
    E = ENGINES[st['engine']](ch, st, grade)
    w0 = E['write']

    def write(r):
        v = w0(r)
        s = slots(r, grade)
        if not v['stem'].startswith('Write'):
            return v
        return dict(v, stem=f'You are {s["name"]} of Class {s["class"]}, {s["school"]}. ' + v['stem'])
    E['write'] = write
    out = [F('C1', 'D1', 'mcq', g_fact(E['rules'])), F('C1', 'D2', 'mcq', g_fact(E['rules'])),
           F('C2', 'D2', 'mcq', E['choose']), F('C2', 'D3', 'explain', E['error']), F('C2', 'D3', 'mcq', g_ar_from(E['ar']), kinds=('ar',)),
           F('C3', 'D1', 'mcq', E['choose2']), F('C3', 'D2', 'short', E['transform']), F('C3', 'D3', 'short', E['transform2']),
           F('C3', 'D4', 'case', lambda r: gram_set(E, 4, r)), F('C4', 'D4', 'long', E['write'])]
    if E.get('para'):
        out.append(F('C4', 'D3', 'explain', E['para'], gap='G5'))
    else:
        out.append(F('C4', 'D3', 'explain', lambda r: gram_set(E, 3, r, ('transform', 'transform2')), gap='G5'))
    return out


def mock_grammar(st, ch, grade, n=5, kind='grammar5'):
    E = ENGINES[st['engine']](ch, st, grade)
    return [F('C3', 'D2', 'case', lambda r: gram_set(E, n, r), kinds=(kind,))]
