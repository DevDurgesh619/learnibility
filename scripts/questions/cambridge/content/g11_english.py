"""Cambridge International AS Level English Language 9093 (grade 11): Papers 1 and 2.

Paper 1 Reading: text types and conventions, audience and purpose, spoken and multimodal texts, comparing
two texts (Q1(b)), directed response (Q1(a)) and writer's style / text analysis (Q2) through the language
frameworks (lexis and semantics, grammar and syntax, discourse and structure, phonology and prosody,
pragmatics, graphology). Paper 2 Writing: shorter writing tasks and the reflective commentary (Section A),
extended imaginative, descriptive, discursive and argumentative writing (Section B).

All source texts (16 extracts in eight topic pairs: speeches, articles, reviews, blogs, leaflets, web pages,
transcripts of spontaneous speech, comment threads), student responses, sentences and titles are original.
Short items quote only a phrase so different items on one extract stay distinct; whole extracts are quoted
only by analysis, comparison and directed-response tasks. Extended tasks carry level descriptors in the
style of the 9093 mark schemes (AO1 reading, AO2 writing, AO3 analysis) and indicative content.
"""
import re

from ._lib import topic, mcq, compose, person, city, CTX  # noqa: F401
from core import MARKS

PROFILE = {'mark_scale': {'long': (2.5, 3)}, 'wordy': True}
CHAPTERS = {}


# =========================================================== helpers

def Q(s):
    if '‘' in s and '“' not in s:
        return f'“{s}”'
    return f'‘{s}’'


def cap(s):
    return s[:1].upper() + s[1:] if s else s


def low(s):
    return s[:1].lower() + s[1:] if s and not s[:2].isupper() else s


def clean(s):
    return re.sub(r'\s+', ' ', s).strip()


def marks(C, D, long=False):
    """Marks for this item; follows a requested total (mock section / parallel form) when one is set."""
    base = MARKS.get((C, D), (2, 2))[0]
    want = CTX.get('want_marks')
    if long:
        sc = min(20, max(1, round(base * 2.5)))
        if want and want != base and want >= 5:
            return min(20, want)
        return sc
    if want and want != base:
        return max(1, min(20, want))
    return base


def an(w):
    return 'an' if w[:1].lower() in 'aeiou' else 'a'


def upto(m):
    return f'Award up to {m} mark' + ('' if m == 1 else 's')


def bands(n, k=5):
    """Mark ranges, top level first, for n marks split into k levels (k=3 when n is small)."""
    k = 5 if n >= 10 else 3 if n >= 3 else 1
    cuts = [round(n * i / k) for i in range(k + 1)]
    out = []
    for i in range(k, 0, -1):
        lo, hi = cuts[i - 1] + 1, cuts[i]
        if lo > hi:
            lo = hi
        out.append(str(hi) if lo == hi else f'{lo}–{hi}')
    return out


def lv_key(m, kind, indicative):
    """Level-marked key in the style of the 9093 mark schemes."""
    lv = LEVELS[kind]
    b = bands(m)
    if len(b) == 5:
        names = ['Level 5', 'Level 4', 'Level 3', 'Level 2', 'Level 1']
        descs = lv
    elif len(b) == 3:
        names = ['Top level', 'Middle level', 'Lower level']
        descs = [lv[0], lv[2], lv[4]]
    else:
        names, descs = ['Credit'], [lv[0]]
    parts = '; '.join(f'{n} ({r}): {d}' for n, r, d in zip(names, b, descs))
    return f'Level-marked out of {m} ({AO[kind]}). {parts}. Indicative content: {indicative}'


def pts_key(m, points, extra=''):
    pts = list(points)
    if m > len(pts) + 1:
        per = -(-m // max(1, len(pts)))
        s = f'{upto(m)}: up to {per} marks for each of the following, according to how fully it is developed and supported: ' + '; '.join(pts)
        return s + '; credit any other valid, supported point.' + (f' {extra}' if extra else '')
    s = f'{upto(m)}, 1 per valid point: ' + '; '.join(pts)
    if len(pts) < m + 1:
        s += '; or any other valid, supported point'
    return s + '.' + (f' {extra}' if extra else '')


NUMW = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}

AO = {
    'analysis': 'AO1 understanding and AO3 analysis of how meaning is shaped',
    'compare': 'AO1 understanding and AO3 comparative analysis of form, structure and language',
    'directed': 'AO2 writing for a specified audience, form and purpose, using the source text',
    'writing': 'AO2 writing: content, structure, style and accuracy',
    'commentary': 'AO3 analysis of own linguistic choices, with comparison where required',
}
LEVELS = {
    'analysis': ['insightful, sustained analysis of how a wide range of language features and structural choices shape meaning; precise, well-integrated quotation; perceptive about audience, purpose and context; fluent use of terminology',
                 'clear, developed analysis of a range of features with relevant quotation; effects explained in relation to audience and purpose; accurate terminology',
                 'some analysis of features with appropriate quotation; effects explained in general terms; some relevant terminology',
                 'identifies some features with limited comment on effect; some quotation; occasional terminology',
                 'mainly paraphrase or feature-spotting; little relevant comment on language'],
    'compare': ['perceptive, balanced comparison of form, structure and language throughout; precise quotation from both texts; insightful links to audience, purpose and context',
                'clear comparison of a range of features in both texts with relevant quotation; effects explained',
                'some comparison with appropriate examples; may treat the texts separately at times',
                'limited comparison; mostly separate discussion of each text; few examples',
                'little or no comparison; mainly paraphrase'],
    'directed': ['form, register and voice fully appropriate and sustained; ideas from the source selected and adapted with skill, not lifted; precise, varied and accurate language',
                 'form and register appropriate; relevant ideas clearly adapted; language clear and mostly accurate',
                 'form recognisable; some relevant ideas, sometimes lifted; register mostly appropriate; some errors',
                 'form and register insecure; ideas thin or copied; errors sometimes impede clarity',
                 'little sense of form, audience or source; frequent errors'],
    'writing': ['highly effective, sophisticated writing for the purpose and audience; ambitious, precise vocabulary and a wide range of controlled structures; cohesive, deliberately shaped organisation; consistently accurate',
                'effective writing with a clear sense of purpose and audience; a good range of vocabulary and structures; well organised; mostly accurate',
                'generally clear writing appropriate to the task; some range of vocabulary and structures; organisation mostly secure; some errors',
                'some sense of purpose; limited vocabulary and sentence variety; organisation uneven; errors sometimes affect meaning',
                'little sense of purpose or audience; simple, repetitive expression; frequent errors'],
    'commentary': ['perceptive, precise analysis of specific choices of form, structure and language, each linked to audience and purpose with apt quotation from own writing; insightful comparison with the stimulus where required',
                   'clear analysis of a range of choices with relevant quotation and effects; comparison developed where required',
                   'some analysis of choices with some quotation; effects stated rather than explored; comparison partial',
                   'identifies a few choices; mostly narrates the writing process; little quotation',
                   'little analysis; general or irrelevant comment'],
}

FWNAME = {'lexis': 'lexis and semantics', 'grammar': 'grammar and syntax', 'discourse': 'discourse and structure',
          'phonology': 'phonology and prosody', 'pragmatics': 'pragmatics', 'graphology': 'graphology and visual design'}

# feature -> definition (used for C1 identify items and keys)
FDEF = {
    # lexis
    'metaphor': 'a direct comparison that presents one thing as another', 'simile': 'a comparison using ‘like’ or ‘as’',
    'personification': 'giving human qualities to something non-human', 'hyperbole': 'deliberate exaggeration for effect',
    'idiom': 'a fixed expression whose meaning is not literal', 'semantic field': 'a group of words linked by a shared area of meaning',
    'emotive language': 'words chosen to provoke an emotional response', 'colloquial lexis': 'informal, conversational vocabulary',
    'precise numerical detail': 'figures and quantities used as evidence', 'hedging': 'language that softens or qualifies a claim',
    'pun': 'a play on words exploiting more than one meaning', 'understatement': 'presenting something as less significant than it is',
    'cliché': 'an over-used, predictable expression', 'positive evaluative lexis': 'approving adjectives and adverbs that judge a subject',
    # grammar
    'imperative': 'a sentence (or clause) that gives a command or instruction', 'rhetorical question': 'a question asked for effect rather than to obtain an answer',
    'exclamative': 'a sentence expressing strong feeling, usually ending in an exclamation mark', 'minor sentence': 'a sentence without a main verb',
    'passive voice': 'a construction in which the object of the action becomes the subject and the agent may be omitted',
    'modal verb': 'an auxiliary such as must, should, could or may expressing obligation or possibility',
    'antithesis': 'contrasting ideas placed in balanced, parallel structures', 'tricolon': 'a pattern of three parallel words, phrases or clauses',
    'ellipsis': 'the omission of words that can be understood from context', 'parenthesis': 'extra information inserted into a sentence between dashes, brackets or commas',
    'compressed noun phrases': 'information packed into short noun phrases without full sentences', 'declarative': 'a sentence that makes a statement',
    'direct address': 'addressing the reader or listener as ‘you’',
    # discourse
    'anecdote': 'a short personal story used to support a point', 'direct quotation': 'reporting the exact words of a named source',
    'concession': 'acknowledging an opposing point before answering it', 'discourse marker': 'a word or phrase that organises talk or text (well, so, of course)',
    'call to action': 'an explicit instruction or request to do something', 'testimonial': 'a quoted endorsement from a customer or user',
    'bathos': 'an anticlimactic drop from the serious to the trivial', 'cyclical structure': 'an ending that returns to the opening idea',
    'temporal sequencing': 'organising a text through time markers', 'reformulation': 'restating what another speaker has said in different words',
    'echoing': 'repeating another speaker’s words', 'filler': 'a non-lexical sound such as erm or er that fills a pause',
    'overlap': 'two speakers talking at the same time', 'back-channelling': 'brief responses (mm, right) showing a listener is following',
    'false start': 'beginning an utterance, abandoning it and starting again', 'tag question': 'a short question added to a statement (isn’t it?)',
    'vague language': 'deliberately imprecise expressions (or something, sort of)', 'phatic talk': 'talk that builds social contact rather than conveying information',
    'headline': 'a short, prominent title summarising and selling a story', 'lead paragraph': 'an opening paragraph that summarises who, what, where and when',
    'repetition': 'repeating a word or phrase for emphasis',
    # phonology
    'alliteration': 'repetition of initial consonant sounds in nearby words', 'sibilance': 'repetition of ‘s’ and ‘sh’ sounds',
    'onomatopoeia': 'a word whose sound imitates its meaning', 'prosodic stress': 'extra emphasis placed on a word in speech',
    'plosive sounds': 'repeated /p/, /b/, /t/, /d/, /k/, /g/ sounds', 'assonance': 'repetition of vowel sounds in nearby words',
    'rhythm': 'the pattern of stressed and unstressed syllables',
    'rising intonation': 'the pitch of the voice going up, often signalling a question or unfinished point',
    'falling intonation': 'the pitch of the voice going down, often signalling completion or certainty',
    # pragmatics
    'irony': 'saying one thing while implying another', 'implicature': 'meaning that is implied rather than stated',
    'inclusive pronoun': '‘we’ or ‘us’ used to unite speaker and audience', 'self-deprecation': 'humour at the speaker’s own expense',
    # graphology
    'image': 'a photograph or illustration that works with the written text', 'bullet points': 'a list set out with symbols for quick scanning',
    'capitalisation for emphasis': 'capital letters used to signal stress or loudness in writing', 'emoji': 'small pictorial symbols that signal tone or emotion',
    'social media handle': 'an @-name used to address or identify a user', 'interactive button': 'a clickable element prompting the reader to act',
}
FPOOL = {
    'lexis': ['metaphor', 'simile', 'personification', 'hyperbole', 'idiom', 'semantic field', 'emotive language', 'colloquial lexis', 'precise numerical detail', 'hedging', 'pun', 'understatement', 'cliché', 'positive evaluative lexis'],
    'grammar': ['imperative', 'rhetorical question', 'exclamative', 'minor sentence', 'passive voice', 'modal verb', 'antithesis', 'tricolon', 'ellipsis', 'parenthesis', 'compressed noun phrases', 'declarative', 'direct address'],
    'discourse': ['anecdote', 'direct quotation', 'concession', 'discourse marker', 'call to action', 'testimonial', 'bathos', 'temporal sequencing', 'reformulation', 'echoing', 'filler', 'overlap', 'back-channelling', 'false start', 'tag question', 'vague language', 'phatic talk', 'headline', 'lead paragraph', 'repetition'],
    'phonology': ['alliteration', 'sibilance', 'onomatopoeia', 'prosodic stress', 'plosive sounds', 'assonance', 'rhythm', 'rising intonation', 'falling intonation'],
    'pragmatics': ['irony', 'implicature', 'inclusive pronoun', 'self-deprecation', 'phatic talk', 'hedging', 'direct address'],
    'graphology': ['image', 'bullet points', 'capitalisation for emphasis', 'emoji', 'social media handle', 'interactive button', 'headline'],
}


class Feat:
    def __init__(self, ex, quote, feature, fw, effect, also=()):
        self.ex, self.quote, self.feature, self.fw, self.effect, self.also = ex, quote, feature, fw, effect, tuple(also)


class Ex:
    """An original extract with its audience, purpose, conventions, annotated features and content points."""
    ALL = []

    def __init__(self, xid, pair, side, kind, label, text, audience, purpose, context, register, spoken=False, multimodal=False):
        self.id, self.pair, self.side, self.kind, self.label = xid, pair, side, kind, label
        text = text.replace("'", '’')
        self.text = clean(text) if not spoken else '\n'.join(ln.strip() for ln in text.strip().split('\n') if ln.strip())
        self.audience, self.purpose, self.context, self.register = audience, purpose, context, register
        self.spoken, self.multimodal = spoken, multimodal
        self.feats, self.convs, self.points, self.false = [], [], [], []
        Ex.ALL.append(self)

    def _chk(self, q):
        assert q.replace("'", '’') in self.text + ' ' + self.label, (self.id, q)

    def f(self, quote, feature, fw, effect, also=()):
        self._chk(quote)
        assert feature in FDEF, feature
        assert fw in FPOOL, fw
        self.feats.append(Feat(self, quote.replace("'", '’'), feature, fw, effect, also))
        return self

    def c(self, quote, conv):
        self._chk(quote)
        self.convs.append((quote.replace("'", '’'), conv))
        return self

    def p(self, *pts):
        self.points.extend(pts)
        return self

    def x(self, *false):
        self.false.extend(false)
        return self

    def body(self):
        if self.spoken:
            return ' '.join(self.text.split('\n'))
        return self.text

    def show(self):
        key = ' (Transcription key: (.) micropause; (1) pause in seconds; // overlapping speech; CAPITALS = stressed word; [ ] non-verbal feature.)' if self.spoken else ''
        return f'Read {self.label}.{key} {Q(self.body())}'

    def opening(self, n=22):
        w = self.body().split(' ')
        return ' '.join(w[:n]) + (' …' if len(w) > n else '')


SPOKEN_KEY = '(.) micropause; (1) pause in seconds; // overlapping speech; CAPITALS = stressed word; [ ] non-verbal feature'


# =========================================================== the extracts (eight topic pairs)

PAIRS = {}

# ---- 1 rooftop gardens
A1 = Ex('roof_speech', 'roof', 'A', 'speech', 'Text A, a speech by a city councillor at a residents’ meeting launching a rooftop-garden scheme', """
Friends, neighbours, fellow gardeners – thank you for coming out on such a wet evening. Look up when you leave tonight. Every flat
roof you see is a field waiting to be planted. Last summer, the pilot garden on the bus depot grew four hundred kilos of vegetables,
cooled the building below by three degrees and gave thirty families somewhere to meet. Imagine that on every block. Some say it is
too expensive. I say we cannot afford not to. So I am asking you tonight: lend us your hands, your weekends and your stubbornness,
and together we will turn this grey city green.""",
    'local residents attending a public meeting', 'to persuade residents to volunteer for the rooftop-garden scheme',
    'a spoken address at a council meeting, prepared in advance', 'semi-formal, warm and rousing')
A1.f('Friends, neighbours, fellow gardeners', 'tricolon', 'grammar', 'the three-part address widens from personal to shared identity, flattering the audience as ‘gardeners’ before they have agreed to anything', also=('direct address',))
A1.f('Look up when you leave tonight.', 'imperative', 'grammar', 'the command makes the audience imagine a physical action, making the vision immediate and personal', also=('direct address',))
A1.f('Every flat roof you see is a field waiting to be planted.', 'metaphor', 'lexis', 'unused concrete is reframed as fertile farmland; ‘waiting’ suggests the roofs are almost asking to be used')
A1.f('grew four hundred kilos of vegetables', 'precise numerical detail', 'lexis', 'concrete figures from the pilot scheme give the speaker credibility and make the benefits measurable')
A1.f('Some say it is too expensive. I say we cannot afford not to.', 'antithesis', 'grammar', 'the parallel ‘Some say … I say’ structure raises the objection only to overturn it, turning cost into a reason to act', also=('concession',))
A1.f('lend us your hands, your weekends and your stubbornness', 'tricolon', 'grammar', 'the list builds from the expected to the humorous ‘stubbornness’, flattering the audience’s determination and ending on a light note')
A1.f('turn this grey city green', 'alliteration', 'phonology', 'the repeated /g/ sound and the colour contrast make the closing slogan memorable and hopeful', also=('assonance',))
A1.f('together we will', 'inclusive pronoun', 'pragmatics', '‘we’ unites councillor and residents as partners, reducing the sense of a politician giving orders')
A1.c('thank you for coming out on such a wet evening', 'a greeting and acknowledgement of the audience, typical of a spoken address')
A1.c('So I am asking you tonight', 'an explicit call to action that signals the speech is reaching its climax')
A1.c('Imagine that on every block.', 'a direct appeal to the listeners’ imagination, a common rhetorical move in speeches')
A1.p('the pilot garden on the bus depot grew 400 kg of vegetables', 'it cooled the building below by three degrees', 'it gave thirty families a place to meet',
     'every flat roof is potential growing space', 'some people object to the cost', 'volunteers are needed, including at weekends')
A1.x('the pilot garden was on the roof of the town hall', 'the scheme will be paid for by a supermarket', 'volunteers will be paid an hourly rate', 'the pilot garden cooled the building by ten degrees')

B1 = Ex('roof_blog', 'roof', 'B', 'blog post', 'Text B, a blog post by a resident, ‘My Year on the Roof’', """
I'll be honest: when the council asked for rooftop volunteers, I signed up mainly to get out of my flat. Twelve months later I have
calloused hands, a slightly ridiculous number of chilli plants and – who knew? – actual friends. It isn't all sunshine. The lift to
the depot roof breaks constantly, the water tank leaked twice in August, and our tomatoes were demolished by pigeons. But on
Saturday mornings, with the traffic grinding below and Mrs Okafor handing round her ginger tea, it feels like the only quiet place
in the city. If you're on the fence, come up and see. Bring gloves.""",
    'other residents and general readers of a personal blog', 'to share a personal experience honestly and encourage others to join',
    'an online personal blog written a year after the scheme began', 'informal, conversational and self-deprecating')
B1.f("I'll be honest:", 'discourse marker', 'discourse', 'the conversational opener promises frankness and builds trust before the writer admits an unheroic motive')
B1.f('a slightly ridiculous number of chilli plants', 'self-deprecation', 'pragmatics', 'gentle humour at the writer’s own expense creates a likeable, unpretentious persona', also=('understatement',))
B1.f('– who knew? –', 'parenthesis', 'grammar', 'the dashed aside mimics speech and conveys pleasant surprise that the garden produced friendships', also=('rhetorical question',))
B1.f("It isn't all sunshine.", 'idiom', 'lexis', 'the familiar idiom signals a turn towards problems, making the writer seem balanced and credible', also=('metaphor',))
B1.f('our tomatoes were demolished by pigeons', 'bathos', 'discourse', 'the list of setbacks ends on a comic anticlimax, keeping the tone light even while admitting problems', also=('passive voice', 'hyperbole'))
B1.f('with the traffic grinding below', 'onomatopoeia', 'phonology', 'the harsh verb ‘grinding’ evokes the noise of the city, contrasting with the peace of the roof')
B1.f('Bring gloves.', 'minor sentence', 'grammar', 'the clipped final command is practical and witty, ending on an invitation rather than a lecture', also=('imperative', 'call to action'))
B1.f("If you're on the fence, come up and see.", 'call to action', 'discourse', 'an informal invitation that addresses doubtful readers directly and lowers the barrier to joining', also=('idiom', 'direct address', 'imperative'))
B1.c('My Year on the Roof', 'a personal, first-person title typical of a blog post')
B1.c("If you're on the fence, come up and see.", 'direct, informal address to the reader, as bloggers write to a community of followers')
B1.c("I'll be honest:", 'a chatty, first-person voice that makes the post feel like a conversation')
B1.p('the writer joined mainly to get out of the flat', 'after a year the writer has made real friends', 'the lift to the roof often breaks',
     'the water tank leaked twice', 'pigeons destroyed the tomatoes', 'Saturday mornings on the roof are peaceful', 'readers are invited to visit')
B1.x('the writer was a professional gardener before joining', 'the council paid for a new lift', 'the garden won a city prize', 'the writer has stopped volunteering')
PAIRS['roof'] = ('a rooftop-garden scheme', A1, B1,
                 ['Text A presents the scheme as a public cause through rousing rhetoric, while Text B offers a personal, humorous account that admits practical problems',
                  'Text A uses statistics from the pilot scheme as evidence; Text B relies on anecdote and personal detail',
                  'Text A addresses a live audience with inclusive ‘we’; Text B writes to individual readers in a chatty first person'],
                 ['Both texts are written for a formal audience of council officials', 'Text B uses more statistics than Text A',
                  'Text A admits that the lift and water tank keep failing', 'Both texts are entirely negative about the scheme'])

# ---- 2 heatwave and water
A2 = Ex('water_news', 'water', 'A', 'news article', 'Text A, a news article from a national newspaper', """
Reservoirs at Record Low as Heatwave Grips Capital. Water levels in the capital's three main reservoirs have fallen to 31 per cent of
capacity, the lowest figure since records began in 1978, officials confirmed yesterday. From Monday, the use of hosepipes and
sprinklers will be banned, and car washes must recycle at least half of the water they use. “We are not yet in a crisis,” said
Dr Leila Haddad, director of the regional water authority, “but every household can make a difference.” Forecasters expect
temperatures to remain above 38°C for at least another week. Critics argue that the authority has failed to repair leaking pipes,
which lose an estimated fifth of all treated water.""",
    'the general adult readership of a national newspaper', 'to inform readers about the water shortage and the new restrictions',
    'a printed and online national news report during a heatwave', 'formal, impersonal and factual')
A2.f('Reservoirs at Record Low', 'alliteration', 'phonology', 'the repeated /r/ makes the headline punchy and memorable', also=('headline',))
A2.f('Heatwave Grips Capital', 'personification', 'lexis', 'the dynamic verb ‘grips’ presents the heat as a physical force holding the city, adding drama to a factual report', also=('headline', 'metaphor'))
A2.f('the lowest figure since records began in 1978', 'precise numerical detail', 'lexis', 'the historical comparison quantifies the seriousness and gives the report authority')
A2.f('will be banned', 'passive voice', 'grammar', 'the agent is omitted, giving the ban an impersonal, official authority and keeping focus on the restriction', also=('modal verb',))
A2.f('car washes must recycle', 'modal verb', 'grammar', 'the deontic modal ‘must’ expresses a legal obligation, signalling that the rule is compulsory')
A2.f('“We are not yet in a crisis,” said', 'direct quotation', 'discourse', 'quoting a named expert adds credibility and balance, and the reassuring tone contrasts with the alarming figures')
A2.f('Critics argue', 'concession', 'discourse', 'the reporting clause introduces an opposing view, giving balance and ending on an unresolved controversy')
A2.f('an estimated fifth', 'hedging', 'lexis', '‘estimated’ qualifies the figure, showing journalistic caution about an unverified statistic')
A2.c('Reservoirs at Record Low as Heatwave Grips Capital.', 'a headline in compressed present tense, summarising the story')
A2.c('officials confirmed yesterday', 'a lead paragraph answering what, where and when, typical of the inverted-pyramid structure')
A2.c('said Dr Leila Haddad, director of the regional water authority', 'attributed quotation with the source’s name and role')
A2.p('reservoirs are at 31% of capacity', 'this is the lowest level since 1978', 'hosepipes and sprinklers are banned from Monday',
     'car washes must recycle at least half their water', 'temperatures will stay above 38°C for another week', 'leaking pipes lose about a fifth of treated water')
A2.x('the reservoirs are at 13% of capacity', 'drinking water will be rationed to two hours a day', 'car washes have been closed completely', 'the heatwave is expected to end tomorrow')

B2 = Ex('water_phonein', 'water', 'B', 'transcript of a radio phone-in', 'Text B, a transcript of a radio phone-in in which the presenter (P) talks to a caller (C)', """
P: and on line two we've got Samuel (.) morning Samuel
C: morning (.) erm yeah I just wanted to say (.) I'm sick of being told to take shorter showers when //
P: // right
C: when the pipes on my street have been leaking for (1) three MONTHS
P: three months (.) wow
C: yeah you can literally see it (.) bubbling up by the bus stop (.) and nobody's come
P: so you'd say the authority's (.) passing the buck a bit
C: exactly (.) exactly that (.) fix your own leaks first you know
P: fair point (.) we have asked them on to the show (.) let's see if they turn up [laughs]""",
    'radio listeners and the caller himself', 'to air a listener’s complaint and entertain the audience with lively talk',
    'a live, unscripted local radio phone-in during the water restrictions', 'informal and conversational', spoken=True)
B2.f('morning Samuel', 'phatic talk', 'discourse', 'the greeting builds friendly rapport and welcomes the caller on air rather than conveying information', also=('phatic talk',))
B2.f('erm yeah I just wanted to say', 'filler', 'discourse', 'the filler and hedged opener show unplanned speech and the caller’s slight nervousness on air', also=('hedging', 'discourse marker'))
B2.f('// right', 'overlap', 'discourse', 'the presenter’s overlapping ‘right’ is supportive back-channelling, encouraging the caller to continue', also=('back-channelling',))
B2.f('three MONTHS', 'prosodic stress', 'phonology', 'the stressed word conveys the caller’s anger and makes the length of the delay the focus')
B2.f('three months (.) wow', 'echoing', 'discourse', 'the presenter repeats the caller’s words to validate the complaint and emphasise it for listeners', also=('repetition', 'back-channelling'))
B2.f('passing the buck a bit', 'reformulation', 'discourse', 'the presenter sums up the complaint in an idiom, framing it for listeners; ‘a bit’ softens the accusation', also=('idiom', 'hedging'))
B2.f('exactly (.) exactly that', 'repetition', 'discourse', 'the repeated agreement shows the caller accepting the presenter’s summary', also=('echoing',))
B2.f('[laughs]', 'implicature', 'pragmatics', 'the laugh implies doubt that the authority will appear, aligning the presenter with the caller without openly criticising', also=('irony',))
B2.c('and on line two we\'ve got Samuel', 'the presenter manages turn-taking and introduces callers, a convention of phone-in talk')
B2.c('fair point (.) we have asked them on to the show', 'the presenter closes the topic and links it to the programme')
B2.p('the caller is told to take shorter showers', 'pipes on his street have leaked for three months', 'water can be seen bubbling up by a bus stop',
     'nobody has come to repair the leak', 'the caller thinks the authority should fix its own leaks first', 'the station has invited the authority onto the show')
B2.x('the caller has been fined for using a hosepipe', 'the leak was repaired the next day', 'the caller works for the water authority', 'the authority has already agreed to appear')
PAIRS['water'] = ('a water shortage during a heatwave', A2, B2,
                  ['Text A is planned, formal written news with attributed quotation; Text B is unplanned spoken interaction with fillers, pauses and overlaps',
                   'Text A presents the authority’s view and the critics’ view in a balanced way; Text B focuses on one listener’s anger',
                   'Text A uses impersonal passive constructions; Text B uses personal, colloquial lexis such as ‘sick of’'],
                  ['Both texts are carefully scripted in advance', 'Text B quotes the director of the water authority',
                   'Text A uses fillers and overlapping speech', 'Text B gives the exact reservoir levels'])

# ---- 3 night market
A3 = Ex('market_review', 'market', 'A', 'review', 'Text A, a review from a city magazine’s food column', """
Arrive hungry and leave your diet at home. The new night market on Harbour Road is loud, cramped and gloriously chaotic, and I
loved almost every minute. The star is a tiny stall run by two sisters who fold dumplings so fast their hands blur; their
pork-and-chive parcels (six for a very reasonable price) are worth the twenty-minute queue alone. The grilled corn was a
disappointment – charred outside, oddly cold within – and seating is a battle you will probably lose. Still, for sheer energy
there is nothing like it in the city. Four stars.""",
    'readers of a city lifestyle magazine looking for places to eat', 'to evaluate the market and entertain readers',
    'a regular food column in a printed and online city magazine', 'informal, witty and evaluative')
A3.f('Arrive hungry and leave your diet at home.', 'imperative', 'grammar', 'the playful commands address the reader directly and set a humorous, indulgent tone', also=('direct address',))
A3.f('loud, cramped and gloriously chaotic', 'tricolon', 'grammar', 'two negative adjectives are turned positive by ‘gloriously’, showing the reviewer finds the chaos part of the charm', also=('positive evaluative lexis',))
A3.f('fold dumplings so fast their hands blur', 'hyperbole', 'lexis', 'the exaggeration creates a vivid image of skill and speed, making the stall seem like a spectacle')
A3.f('charred outside, oddly cold within', 'antithesis', 'grammar', 'the balanced contrast gives a precise, concise criticism, showing the review is discriminating rather than gushing')
A3.f('seating is a battle you will probably lose', 'metaphor', 'lexis', 'the comic war metaphor warns readers about crowding while keeping the tone light', also=('direct address', 'hedging'))
A3.f('Four stars.', 'minor sentence', 'grammar', 'the verbless verdict follows review conventions and delivers a clear final judgement')
A3.f('I loved almost every minute', 'hedging', 'lexis', '‘almost’ qualifies the praise, preparing for the criticisms and making the reviewer seem fair')
A3.c('Four stars.', 'a star rating giving an overall verdict')
A3.c('(six for a very reasonable price)', 'comment on value for money, which readers of reviews expect')
A3.c('The grilled corn was a disappointment', 'balanced criticism alongside praise')
A3.p('the market is on Harbour Road', 'it is loud, crowded and lively', 'the best stall is run by two sisters making dumplings', 'the pork-and-chive dumplings are good value',
     'there is a twenty-minute queue for dumplings', 'the grilled corn was disappointing', 'seating is hard to find', 'the reviewer gave four stars')
A3.x('the reviewer gave the market five stars', 'the dumpling stall is run by a father and son', 'the market has plenty of seating', 'the grilled corn was the highlight')

B3 = Ex('market_leaflet', 'market', 'B', 'promotional leaflet', 'Text B, a promotional leaflet for the same night market', """
HARBOUR ROAD NIGHT MARKET [image: strings of lanterns above crowded stalls] Taste the world in one street! Over 60 stalls •
Open Thursday–Sunday, 6 pm till late • Live music every Friday. From sizzling satay to sweet mango sticky rice, there's something for
every appetite. Bring the whole family – kids eat free before 7 pm on Sundays! Find us: two minutes from Harbour Road station.
Follow us @harbournights for this week's specials.""",
    'potential visitors, including families', 'to persuade people to visit the market', 'a printed leaflet distributed around the city', 'enthusiastic, informal and promotional', multimodal=True)
B3.f('Taste the world in one street!', 'exclamative', 'grammar', 'the exclamatory slogan, with its hyperbolic promise, creates excitement and suggests variety', also=('imperative', 'hyperbole'))
B3.f('[image: strings of lanterns above crowded stalls]', 'image', 'graphology', 'the lanterns create a festive, welcoming atmosphere and the crowds suggest popularity')
B3.f('Over 60 stalls •', 'bullet points', 'graphology', 'the bulleted facts let readers scan opening times and attractions quickly', also=('compressed noun phrases',))
B3.f('sizzling satay', 'sibilance', 'phonology', 'the repeated /s/ sounds imitate food cooking and appeal to the senses', also=('alliteration', 'onomatopoeia'))
B3.f("there's something for every appetite", 'hyperbole', 'lexis', 'the sweeping claim widens the appeal to every reader')
B3.f('kids eat free before 7 pm on Sundays!', 'exclamative', 'grammar', 'the exclamation highlights a family incentive and targets parents directly', also=('call to action',))
B3.f('Follow us @harbournights', 'social media handle', 'graphology', 'the handle links print to social media, inviting an ongoing relationship with readers', also=('call to action', 'imperative'))
B3.c('HARBOUR ROAD NIGHT MARKET', 'a bold heading naming the product')
B3.c('Open Thursday–Sunday, 6 pm till late', 'practical information in compressed form')
B3.c('Find us: two minutes from Harbour Road station.', 'directions and contact details')
B3.p('there are over 60 stalls', 'it opens Thursday to Sunday from 6 pm', 'there is live music on Fridays', 'food ranges from satay to mango sticky rice',
     'children eat free before 7 pm on Sundays', 'it is two minutes from Harbour Road station')
B3.x('the market opens every day of the week', 'there is live music every night', 'children eat free all weekend', 'the market is next to the airport')
PAIRS['market'] = ('a night market', A3, B3,
                   ['Text A evaluates the market, including criticisms; Text B presents only positives to sell it',
                    'Text A is continuous prose with an individual reviewer’s voice; Text B relies on layout, an image, bullet points and slogans',
                    'Text A ends with a star rating; Text B ends with a social-media call to action'],
                   ['Both texts criticise the grilled corn', 'Text B gives the market a star rating',
                    'Text A uses bullet points to list opening times', 'Both texts are written by the same reviewer'])

# ---- 4 mountain trek
A4 = Ex('trek_memoir', 'trek', 'A', 'travel memoir', 'Text A, an extract from a travel memoir about trekking to a mountain monastery', """
By the third day my legs had stopped complaining and simply given up. The path zigzagged above the cloud line, and every time I
thought I had reached the top, another ridge rose ahead of me like a cruel joke. Our guide, Pema, walked as if the mountain were
flat, humming to himself and pausing only to point out a vulture circling below us. Below us. I remember that more than anything:
looking down at a bird in flight. When the monastery finally appeared, its prayer flags snapping in the wind, I did not feel
triumph. I felt very small, and strangely grateful.""",
    'general readers of travel literature', 'to recount and reflect on a personal journey, and to entertain', 'a published book of travel writing, written after the event', 'literary, reflective and personal')
A4.f('my legs had stopped complaining and simply given up', 'personification', 'lexis', 'the legs become reluctant companions, conveying exhaustion with wry humour')
A4.f('like a cruel joke', 'simile', 'lexis', 'the false summits seem to mock the narrator, conveying frustration and the mountain’s indifference')
A4.f('walked as if the mountain were flat', 'hyperbole', 'lexis', 'the exaggeration contrasts the guide’s ease with the narrator’s struggle, emphasising his expertise')
A4.f('Below us.', 'minor sentence', 'grammar', 'the repeated fragment isolates the extraordinary detail and slows the reader to share the narrator’s awe', also=('repetition', 'ellipsis'))
A4.f('its prayer flags snapping in the wind', 'onomatopoeia', 'phonology', 'the sharp sound of ‘snapping’ brings the scene to life and suggests the wind’s force at altitude', also=('sibilance',))
A4.f('I did not feel triumph. I felt very small, and strangely grateful.', 'antithesis', 'grammar', 'the expected emotion is denied and replaced with humility, giving a reflective, unexpected ending')
A4.f('By the third day', 'temporal sequencing', 'discourse', 'the time marker places the reader mid-journey and structures the account chronologically')
A4.c('I remember that more than anything', 'retrospective first-person reflection, typical of memoir')
A4.c('Our guide, Pema,', 'named real people from the journey')
A4.c('I did not feel triumph.', 'an ending that reflects on the meaning of the experience rather than just narrating it')
A4.p('by day three the narrator was exhausted', 'the path climbed above the clouds', 'false summits kept appearing', 'the guide Pema walked easily and hummed',
     'they saw a vulture flying below them', 'at the monastery the narrator felt small and grateful')
A4.x('the narrator reached the monastery on the first day', 'Pema was exhausted by the climb', 'the narrator felt triumphant at the top', 'they saw eagles nesting near the path')

B4 = Ex('trek_web', 'trek', 'B', 'web page', 'Text B, a page from a trekking company’s website', """
[Banner photograph: a line of hikers on a ridge at sunrise] MONASTERY TRAIL – 5 DAYS | Moderate | From $640. Walk in the footsteps
of pilgrims on one of the region's most spectacular routes. ✔ Expert local guides ✔ Comfortable teahouse lodges ✔ All meals included.
Day 3 is our favourite: you'll climb above the clouds and watch eagles soar beneath your feet. “The best week of my life!” – Ana,
Brazil [BOOK NOW button]""",
    'potential customers planning a trekking holiday', 'to persuade readers to book the trek', 'a commercial website page viewed on screen', 'enthusiastic, promotional and concise', multimodal=True)
B4.f('[Banner photograph: a line of hikers on a ridge at sunrise]', 'image', 'graphology', 'the sunrise photograph suggests adventure, achievement and beauty before the reader reads a word')
B4.f('✔ Expert local guides ✔ Comfortable teahouse lodges ✔ All meals included', 'bullet points', 'graphology', 'the tick list reassures readers about safety and comfort at a glance', also=('compressed noun phrases', 'tricolon'))
B4.f('Walk in the footsteps of pilgrims', 'imperative', 'grammar', 'the command invites the reader into the experience and gives the trek spiritual, historic significance', also=('metaphor', 'direct address'))
B4.f("you'll climb above the clouds and watch eagles soar beneath your feet", 'direct address', 'grammar', 'second-person future tense lets readers imagine themselves on the trek, presenting it as certain and magical', also=('hyperbole',))
B4.f('“The best week of my life!” – Ana, Brazil', 'testimonial', 'discourse', 'a customer’s exclamation provides social proof; naming her country suggests international appeal', also=('exclamative', 'hyperbole', 'direct quotation'))
B4.f('[BOOK NOW button]', 'interactive button', 'graphology', 'the capitalised button is a direct call to action that turns interest into a sale', also=('call to action', 'capitalisation for emphasis'))
B4.f('MONASTERY TRAIL – 5 DAYS | Moderate | From $640', 'compressed noun phrases', 'grammar', 'key facts are packed into a scannable line with no full sentences', also=('headline',))
B4.c('[BOOK NOW button]', 'an interactive call to action')
B4.c('“The best week of my life!” – Ana, Brazil', 'a customer testimonial')
B4.c('From $640', 'price information presented as ‘from’, suggesting affordability')
B4.p('the trek lasts five days', 'it is rated moderate', 'prices start at $640', 'local guides lead the trek', 'walkers stay in teahouse lodges', 'all meals are included',
     'on day three walkers climb above the clouds')
B4.x('the trek is rated very difficult', 'meals cost extra', 'walkers camp in tents', 'the trek lasts ten days')
PAIRS['trek'] = ('trekking to a mountain monastery', A4, B4,
                 ['Text A presents exhaustion and humility honestly; Text B idealises the trek as easy and magical',
                  'Text A is reflective first-person memoir; Text B is second-person commercial persuasion with images and a button',
                  'Text A’s bird below the walkers is a vulture, an ominous image; Text B’s eagles soaring beneath your feet are glamorous'],
                 ['Both texts include a booking button', 'Text B admits the walk is exhausting',
                  'Text A uses bullet points and ticks', 'Both texts are written in the second person throughout'])

# ---- 5 phones in school
A5 = Ex('phones_podcast', 'phones', 'A', 'podcast transcript', 'Text A, a transcript from a student podcast in which two presenters, Kenji (K) and Zara (Z), discuss a new ban on phones in school', """
K: so (.) the ban (.) week one (.) how are we feeling
Z: honestly (.) I thought I'd hate it but (.) lunch is actually (.) louder now (.) like people TALK
K: [laughs] people talk (.) shocking
Z: no but seriously //
K: // I know I know
Z: there was this one boy who was (.) he was just playing cards with the year sevens (.) which (.) never would have happened before
K: mm (.) I do miss checking the bus times though (.) that's a genuine (.) problem isn't it
Z: true (.) true (.) they could put a screen up in the canteen or something""",
    'other students who listen to the school podcast', 'to discuss and entertain, sharing reactions to the ban', 'a recorded, largely unscripted student podcast', 'informal, playful and conversational', spoken=True)
A5.f('so (.) the ban (.) week one', 'ellipsis', 'grammar', 'the verbless noun phrases sketch the topic quickly, typical of spontaneous speech, as listeners can infer the meaning', also=('compressed noun phrases', 'minor sentence', 'discourse marker'))
A5.f('honestly', 'discourse marker', 'discourse', 'signals a sincere, personal opinion and marks the start of Zara’s turn', also=('hedging',))
A5.f('like people TALK', 'prosodic stress', 'phonology', 'the stress on ‘TALK’ highlights the surprising change and adds humour')
A5.f('[laughs] people talk (.) shocking', 'irony', 'pragmatics', 'Kenji’s mock amazement gently teases the idea that talking is remarkable, building rapport through humour', also=('echoing',))
A5.f('// I know I know', 'overlap', 'discourse', 'the overlapping reassurance shows cooperative, friendly talk rather than an attempt to take the floor', also=('repetition', 'back-channelling'))
A5.f('who was (.) he was just', 'false start', 'discourse', 'the self-repair shows the speaker planning in real time', also=('repetition',))
A5.f("that's a genuine (.) problem isn't it", 'tag question', 'discourse', 'the tag invites agreement, softening a criticism of the ban and passing the turn to Zara')
A5.f('or something', 'vague language', 'discourse', 'the vague tag keeps the suggestion tentative and conversational', also=('hedging',))
A5.c('so (.) the ban (.) week one (.) how are we feeling', 'a presenter’s opening question that sets the topic, as in podcast talk')
A5.c('mm', 'back-channel responses typical of conversational turn-taking')
A5.p('the ban is in its first week', 'lunchtimes are louder because people talk', 'a boy played cards with younger students', 'students miss checking bus times', 'a screen could show bus times in the canteen')
A5.x('both presenters want the ban removed', 'the ban has been in place for a year', 'teachers have banned card games', 'the canteen already has a bus-times screen')

B5 = Ex('phones_editorial', 'phones', 'B', 'editorial', 'Text B, an editorial in a national newspaper, ‘Pocket the Phones’', """
The evidence is now difficult to ignore. In schools that have removed smartphones from the school day, teachers report calmer
corridors, fewer incidents of online bullying and, in several studies, modest gains in test scores. Of course, a ban is not a
cure-all; determined pupils will always find a way, and parents understandably want to be able to reach their children. But these
are problems of management, not of principle. Children deserve a few hours each day in which their attention belongs to them rather
than to an algorithm. Schools should pocket the phones – and keep them pocketed.""",
    'adult newspaper readers, including parents and policymakers', 'to argue that schools should ban phones', 'an unsigned editorial expressing the newspaper’s view', 'formal, assured and persuasive')
B5.f('The evidence is now difficult to ignore.', 'declarative', 'grammar', 'the confident opening statement presents the argument as settled fact, positioning the reader to agree')
B5.f('calmer corridors', 'alliteration', 'phonology', 'the /k/ alliteration makes the benefit memorable and suggests order')
B5.f('modest gains in test scores', 'hedging', 'lexis', '‘modest’ concedes the gains are small, making the argument seem honest and measured', also=('understatement',))
B5.f('Of course, a ban is not a cure-all', 'concession', 'discourse', 'the editorial anticipates objections before rebutting them, strengthening its credibility', also=('discourse marker', 'idiom'))
B5.f('problems of management, not of principle', 'antithesis', 'grammar', 'the balanced contrast dismisses objections as practical details rather than reasons against the ban')
B5.f('their attention belongs to them rather than to an algorithm', 'personification', 'lexis', 'the algorithm is presented as a rival owner of children’s minds, making phones seem predatory', also=('antithesis',))
B5.f('Schools should pocket the phones', 'modal verb', 'grammar', 'the deontic ‘should’ expresses the newspaper’s firm recommendation', also=('pun',))
B5.f('and keep them pocketed', 'pun', 'lexis', 'the wordplay echoes the title, giving a neat, memorable closing slogan', also=('repetition', 'cyclical structure'))
B5.c('Pocket the Phones', 'a short, punchy imperative title that states the paper’s position')
B5.c('Of course, a ban is not a cure-all', 'concession and rebuttal, typical of an argumentative editorial')
B5.c('Schools should pocket the phones', 'a firm recommendation in the conclusion')
B5.p('teachers report calmer corridors', 'there is less online bullying', 'some studies show small gains in test scores', 'determined pupils may still use phones',
     'parents want to contact their children', 'the editorial calls these practical problems, not reasons against a ban')
B5.x('studies show test scores doubled', 'the editorial opposes a ban', 'parents unanimously support the ban', 'bullying increased after phones were removed')
PAIRS['phones'] = ('a ban on phones in school', A5, B5,
                   ['Text A is spontaneous, cooperative talk with fillers, overlaps and tag questions; Text B is a planned, formal written argument',
                    'Text A presents students’ mixed personal reactions; Text B argues one position using evidence and concession',
                    'Text A’s humour is playful and conversational; Text B’s wordplay is crafted into a closing slogan'],
                   ['Both texts are written by students', 'Text B uses tag questions and back-channelling',
                    'Text A cites studies of test scores', 'Both texts argue strongly against the ban'])

# ---- 6 running for charity
A6 = Ex('run_appeal', 'run', 'A', 'charity appeal email', 'Text A, a fundraising email from a children’s hospital charity', """
Dear Supporter, Six-year-old Mateo spent his last birthday in a hospital bed, wired to a machine that breathed for him. Today he is
learning to ride a bike. The difference? A specialist ventilator, bought with money raised by runners like you. This year we need
forty more ventilators. Each one costs less than a family car, yet each one gives a child back their future. Will you run for Mateo
on 12 March? Sign up today, and we will send you a free training plan and your charity vest. With heartfelt thanks, The Fundraising
Team""",
    'past donors and potential charity runners', 'to persuade readers to sign up for a fundraising run', 'an email sent to a charity’s mailing list', 'warm, emotive and direct')
A6.f('Six-year-old Mateo spent his last birthday in a hospital bed', 'anecdote', 'discourse', 'opening with one named child personalises the cause and creates immediate sympathy', also=('emotive language',))
A6.f('a machine that breathed for him', 'personification', 'lexis', 'the machine performing a basic human act emphasises how fragile the child was', also=('emotive language',))
A6.f('The difference?', 'rhetorical question', 'grammar', 'the short question creates a pause and sets up the ventilator as the answer', also=('minor sentence', 'ellipsis'))
A6.f('runners like you', 'direct address', 'grammar', 'the reader is flattered as already part of the heroic group of runners', also=('direct address',))
A6.f('costs less than a family car', 'precise numerical detail', 'lexis', 'the comparison makes an expensive item feel affordable and relatable', also=('hyperbole',))
A6.f('gives a child back their future', 'emotive language', 'lexis', 'the abstract noun ‘future’ raises the stakes from equipment to a whole life')
A6.f('Will you run for Mateo on 12 March?', 'call to action', 'discourse', 'the direct question asks for commitment and ties the reader to the named child', also=('rhetorical question', 'direct address'))
A6.c('Dear Supporter,', 'a formal salutation typical of a letter or email')
A6.c('With heartfelt thanks, The Fundraising Team', 'a warm sign-off from the organisation')
A6.c('Sign up today, and we will send you a free training plan', 'an incentive linked to a call to action')
A6.p('Mateo spent his birthday on a ventilator', 'he is now learning to ride a bike', 'a ventilator bought by runners helped him', 'the charity needs forty more ventilators',
     'each ventilator costs less than a family car', 'the run is on 12 March', 'runners get a free training plan and vest')
A6.x('the charity needs four more ventilators', 'Mateo is a professional runner', 'the run is on 12 May', 'runners must pay for their vests')

B6 = Ex('run_blog', 'run', 'B', 'blog post', 'Text B, a post from a personal running blog, ‘Kilometre 30’', """
Nobody warns you about kilometre 30. The crowds have thinned, the energy gels taste like warm glue and your brain starts negotiating:
just walk for a bit, nobody will know. I knew. At kilometre 31 a woman in a pink tutu overtook me, and something in me snapped – not
my hamstring, thankfully, just my pride. I finished in 4 hours 12, which won't trouble the record books, but I raised enough for half
a ventilator. Next year, the whole thing. Tutu optional.""",
    'readers of a personal blog, many of them runners', 'to entertain and reflect on running a charity marathon', 'a personal blog written after the race', 'informal, humorous and self-deprecating')
B6.f('Nobody warns you about kilometre 30.', 'declarative', 'grammar', 'the confident, mysterious generalisation hooks the reader and implies insider knowledge', also=('direct address',))
B6.f('taste like warm glue', 'simile', 'lexis', 'the unpleasant comparison is comic and conveys physical misery')
B6.f('your brain starts negotiating', 'personification', 'lexis', 'the brain becomes a separate, tempting voice, dramatising the mental battle', also=('direct address', 'metaphor'))
B6.f('I knew.', 'minor sentence', 'grammar', 'the two-word sentence cuts through the temptation, showing the narrator’s conscience', also=('declarative',))
B6.f('not my hamstring, thankfully, just my pride', 'self-deprecation', 'pragmatics', 'the comic correction turns a moment of determination into a joke against himself', also=('pun', 'parenthesis'))
B6.f("won't trouble the record books", 'understatement', 'lexis', 'the modest phrase plays down the achievement, creating a likeable persona', also=('idiom', 'self-deprecation'))
B6.f('Tutu optional.', 'minor sentence', 'grammar', 'the clipped, humorous final line callbacks the tutu, closing with a joke', also=('ellipsis', 'compressed noun phrases'))
B6.c('Kilometre 30', 'an intriguing, personal title for a blog post')
B6.c('Next year, the whole thing.', 'a forward-looking ending addressed to followers')
B6.p('kilometre 30 is the hardest point', 'crowds thin and energy gels taste bad', 'the writer was tempted to walk', 'a woman in a tutu overtook him and spurred him on',
     'he finished in 4 hours 12 minutes', 'he raised enough for half a ventilator', 'he plans to run again next year')
B6.x('the writer won the race', 'the writer injured his hamstring', 'he raised enough for two ventilators', 'he walked most of the final ten kilometres')
PAIRS['run'] = ('running a marathon for charity', A6, B6,
                ['Text A uses one child’s story and emotive lexis to make readers act; Text B uses humour and self-deprecation to entertain',
                 'Text A follows email conventions (salutation, sign-off, call to action); Text B is a first-person blog narrative',
                 'Text A addresses the reader as ‘you’ to recruit runners; Text B uses ‘you’ to share an experience runners recognise'],
                ['Both texts are written by Mateo', 'Text B ends with a formal sign-off from an organisation',
                 'Text A is mainly humorous and self-deprecating', 'Text B asks readers to sign up for 12 March'])

# ---- 7 e-scooters
A7 = Ex('scooter_leaflet', 'scooter', 'A', 'information leaflet', 'Text A, an information leaflet from a city transport department, ‘Riding an E-scooter Safely’', """
Riding an E-scooter Safely. E-scooters are now available to hire across the city centre. To keep yourself and others safe: • You
must be 18 or over and hold a driving licence. • Ride on roads and cycle lanes only – never on pavements. • Wear a helmet. It could
save your life. • Only one rider per scooter. Fines of up to $300 may be issued to riders who break these rules. For more
information, visit our website or scan the QR code below.""",
    'members of the public who might hire e-scooters', 'to inform and instruct riders about safety rules', 'an official leaflet available at hire points and online', 'formal, clear and instructional', multimodal=True)
A7.f('You must be 18 or over', 'modal verb', 'grammar', 'deontic ‘must’ states a legal requirement firmly and unambiguously', also=('direct address',))
A7.f('• Ride on roads and cycle lanes only', 'bullet points', 'graphology', 'bulleted rules are easy to scan and remember', also=('imperative',))
A7.f('– never on pavements', 'parenthesis', 'grammar', 'the dash isolates the prohibition and gives it emphasis', also=('ellipsis',))
A7.f('Wear a helmet.', 'imperative', 'grammar', 'the short, direct command gives a clear instruction with no room for doubt', also=('direct address',))
A7.f('It could save your life.', 'modal verb', 'grammar', 'epistemic ‘could’ presents a possible consequence, adding emotional weight to the instruction', also=('direct address', 'emotive language'))
A7.f('Fines of up to $300 may be issued', 'passive voice', 'grammar', 'the agentless passive gives the warning impersonal, official authority', also=('modal verb', 'precise numerical detail'))
A7.f('scan the QR code below', 'imperative', 'grammar', 'the instruction links the printed leaflet to digital information', also=('call to action',))
A7.c('Riding an E-scooter Safely.', 'a clear, informative title')
A7.c('• Only one rider per scooter.', 'rules presented as a bulleted list')
A7.c('For more information, visit our website', 'signposting to further information')
A7.p('e-scooters can be hired across the city centre', 'riders must be 18 or over with a driving licence', 'scooters must be ridden on roads and cycle lanes, not pavements',
     'helmets should be worn', 'only one rider is allowed per scooter', 'fines of up to $300 can be issued')
A7.x('riders must be 16 or over', 'scooters may be ridden on pavements at night', 'two riders may share a scooter', 'fines of up to $3,000 can be issued')

B7 = Ex('scooter_voxpop', 'scooter', 'B', 'transcript of street interviews', 'Text B, a transcript of street interviews (vox pops) for a local news website; I is the interviewer, R1 and R2 are members of the public', """
I: what do you think of the new scooters
R1: love them (.) honestly (.) I get to work in ten minutes instead of (.) what (.) forty on the bus
I: and safety
R1: well (.) I mean I'm careful (.) I don't know about everyone else
R2: they're a menace (.) a MENACE (.) one nearly took my dog out yesterday (.) on the pavement
I: on the pavement
R2: on the pavement (.) and he just (.) laughed (.) went whizzing off""",
    'readers and viewers of a local news website', 'to present a range of public opinions on the scooters', 'unscripted street interviews recorded and transcribed', 'informal and spontaneous', spoken=True)
B7.f('love them', 'ellipsis', 'grammar', 'the subject ‘I’ is omitted, typical of quick, enthusiastic spoken replies', also=('minor sentence',))
B7.f('instead of (.) what (.) forty', 'vague language', 'discourse', 'the self-directed ‘what’ and pause show the speaker estimating in real time', also=('filler', 'hedging'))
B7.f('well (.) I mean', 'discourse marker', 'discourse', 'the markers signal hesitation as the speaker moves to a less comfortable topic', also=('hedging', 'filler'))
B7.f('a menace (.) a MENACE', 'prosodic stress', 'phonology', 'the repetition with heavier stress intensifies R2’s anger', also=('repetition',))
B7.f('took my dog out', 'idiom', 'lexis', 'the colloquial phrase exaggerates the near-miss vividly', also=('colloquial lexis', 'hyperbole'))
B7.f('I: on the pavement', 'echoing', 'discourse', 'the interviewer repeats R2’s words to prompt more detail without asking a full question', also=('repetition',))
B7.f('went whizzing off', 'onomatopoeia', 'phonology', 'the imitative ‘whizzing’ conveys the speed and carelessness of the rider', also=('colloquial lexis',))
B7.c('what do you think of the new scooters', 'an open question to start each interview')
B7.c('I: and safety', 'brief interviewer prompts that steer the topic')
B7.p('R1 loves the scooters', 'R1’s commute is ten minutes instead of forty by bus', 'R1 says he is careful but doubts others are', 'R2 thinks the scooters are a menace',
     'a scooter nearly hit R2’s dog on the pavement', 'the rider laughed and sped off')
B7.x('both speakers want the scooters banned', 'R2’s dog was injured', 'R1 takes the bus to work', 'the rider apologised to R2')
PAIRS['scooter'] = ('e-scooters in the city', A7, B7,
                    ['Text A is an official, planned text of rules and modal verbs; Text B is spontaneous speech with fillers, ellipsis and overlapping opinions',
                     'Text A presents scooters neutrally as a regulated service; Text B shows that people disagree strongly about them',
                     'Text A uses impersonal passives to warn of fines; Text B uses personal anecdote and colloquial idiom'],
                    ['Both texts are unscripted', 'Text A includes a member of the public’s anecdote about a dog',
                     'Text B lists the rules in bullet points', 'Both texts agree that scooters are a menace'])

# ---- 8 cinema closing
A8 = Ex('cinema_feature', 'cinema', 'A', 'feature article', 'Text A, a feature article in a regional newspaper about the closure of the Rialto cinema', """
For ninety-two years the Rialto has been the place where this town fell in love – with film stars, with stories, and quite often with
each other. On Sunday its velvet curtains will close for the last time. Inside, the carpet is threadbare and the seats creak like old
ships, but the projectionist, Mr Farouk, still climbs the narrow stairs each evening as he has done since 1979. “People say streaming
killed us,” he shrugs. “Maybe. But you cannot laugh with three hundred strangers on your sofa.” The building will become a car park.""",
    'readers of a regional newspaper, many with memories of the cinema', 'to inform readers of the closure and evoke nostalgia', 'a feature article published in the week of the closure', 'reflective, affectionate and quietly critical')
A8.f('the place where this town fell in love', 'metaphor', 'lexis', 'the town is personified as a lover, presenting the cinema as the heart of the community', also=('personification',))
A8.f('with film stars, with stories, and quite often with each other', 'tricolon', 'grammar', 'the list builds to a warm, humorous climax that reminds readers of real courtships', also=('repetition',))
A8.f('its velvet curtains will close for the last time', 'metaphor', 'lexis', 'the closing curtains symbolise the end of an era, giving the closure theatrical finality', also=('emotive language',))
A8.f('the seats creak like old ships', 'simile', 'lexis', 'the comparison suggests age and romance, making decline seem dignified', also=('onomatopoeia',))
A8.f('“People say streaming killed us,”', 'direct quotation', 'discourse', 'the projectionist’s own words give a personal, authentic voice to the story', also=('metaphor',))
A8.f('you cannot laugh with three hundred strangers on your sofa', 'antithesis', 'grammar', 'the absurd image contrasts private streaming with shared cinema, making the loss clear', also=('hyperbole', 'direct address'))
A8.f('The building will become a car park.', 'bathos', 'discourse', 'the flat final sentence deflates the nostalgia and implies criticism without stating it', also=('declarative', 'implicature'))
A8.c('For ninety-two years', 'an opening that establishes the history and human interest of the story')
A8.c('the projectionist, Mr Farouk,', 'a named interviewee giving a human angle')
A8.c('The building will become a car park.', 'a pointed final sentence typical of a feature’s closing ‘kicker’')
A8.p('the Rialto has operated for ninety-two years', 'it closes on Sunday', 'the carpet is worn and the seats creak', 'Mr Farouk has been projectionist since 1979',
     'he thinks streaming contributed to the closure', 'the building will become a car park')
A8.x('the Rialto is being converted into flats', 'Mr Farouk started work in 1992', 'the cinema has just been renovated', 'the cinema will reopen next year')

B8 = Ex('cinema_thread', 'cinema', 'B', 'online comment thread', 'Text B, a thread of comments posted under a local news website’s report on the Rialto closure', """
@filmfan_88: Saw my first ever film there in 1996 😭 end of an era. | @nadia.k: Honestly? It was freezing and the sound was terrible.
Nostalgia is fine but nobody actually WENT. | @filmfan_88: @nadia.k harsh but… fair 😂 | @localhistory: The Rialto opened in 1932
with a silent film and a live orchestra. Photos in our archive (link below). | @samuel_w: car park. a CAR PARK. unbelievable.""",
    'other readers of the local news website', 'to share personal reactions, memories and information', 'public comments posted online under a news report', 'informal and varied, from nostalgic to blunt', multimodal=True)
B8.f('😭', 'emoji', 'graphology', 'the crying emoji conveys grief playfully, standing in for facial expression')
B8.f('end of an era', 'cliché', 'lexis', 'the familiar phrase sums up the loss quickly, typical of informal online comment', also=('idiom',))
B8.f('Honestly? It was freezing', 'rhetorical question', 'grammar', 'the one-word question announces a frank, contrary view', also=('discourse marker', 'minor sentence'))
B8.f('nobody actually WENT', 'capitalisation for emphasis', 'graphology', 'capital letters mimic spoken stress and make the criticism forceful', also=('prosodic stress',))
B8.f('@nadia.k harsh but… fair 😂', 'social media handle', 'graphology', 'the handle addresses one commenter directly, creating a conversation within the thread', also=('emoji',))
B8.f('car park. a CAR PARK. unbelievable.', 'repetition', 'discourse', 'repetition, capitals and lower-case fragments convey disbelief and anger', also=('minor sentence', 'capitalisation for emphasis'))
B8.f('Photos in our archive (link below).', 'compressed noun phrases', 'grammar', 'the verbless phrasing and link are typical of informative online posts', also=('minor sentence', 'ellipsis'))
B8.c('@filmfan_88:', 'usernames that identify each contributor')
B8.c('(link below)', 'hyperlinks to further material')
B8.p('one commenter saw their first film there in 1996', 'one says the cinema was cold with poor sound', 'one says few people actually went',
     'the Rialto opened in 1932 with a silent film and live orchestra', 'one commenter is angry about the car park')
B8.x('every commenter wants the Rialto saved', 'the Rialto opened in 1996', 'nadia.k worked at the cinema', 'the local history group is organising a protest')
PAIRS['cinema'] = ('the closure of an old cinema', A8, B8,
                   ['Text A is a single, crafted journalistic voice; Text B is many short, informal voices responding to each other',
                    'Text A is consistently nostalgic until its final line; Text B includes a blunt counter-view that nobody went',
                    'Text A creates emotion through imagery and quotation; Text B uses emoji, capitals and fragments'],
                   ['Both texts are written by Mr Farouk', 'Text A uses emoji to convey grief',
                    'Text B is a single continuous article', 'Both texts claim the cinema was always full'])

EXTRACTS = Ex.ALL
FEATS = [f for e in EXTRACTS for f in e.feats]
SPOKEN = [e for e in EXTRACTS if e.spoken]
MULTI = [e for e in EXTRACTS if e.multimodal]

TNAME = {'roof_speech': 'speech', 'roof_blog': 'blog post', 'water_news': 'news report', 'water_phonein': 'transcript of spontaneous speech',
         'market_review': 'review', 'market_leaflet': 'advertising leaflet', 'trek_memoir': 'travel memoir', 'trek_web': 'web page',
         'phones_podcast': 'transcript of spontaneous speech', 'phones_editorial': 'editorial', 'run_appeal': 'charity appeal', 'run_blog': 'blog post',
         'scooter_leaflet': 'information leaflet', 'scooter_voxpop': 'transcript of spontaneous speech', 'cinema_feature': 'feature article', 'cinema_thread': 'online comment thread'}
TGROUP = {'news report': 1, 'feature article': 1, 'editorial': 1, 'blog post': 2, 'travel memoir': 2, 'online comment thread': 2,
          'advertising leaflet': 3, 'web page': 3, 'information leaflet': 3, 'charity appeal': 3, 'transcript of spontaneous speech': 4, 'speech': 5, 'review': 6}
PURPOSE = {'roof_speech': ('to persuade', ()), 'roof_blog': ('to entertain and reflect', ('to persuade',)), 'water_news': ('to inform', ()),
           'water_phonein': ('to entertain and air opinions', ('to inform',)), 'market_review': ('to evaluate', ('to entertain and reflect', 'to inform')),
           'market_leaflet': ('to persuade', ('to inform',)), 'trek_memoir': ('to entertain and reflect', ()), 'trek_web': ('to persuade', ('to inform',)),
           'phones_podcast': ('to entertain and air opinions', ()), 'phones_editorial': ('to persuade', ()), 'run_appeal': ('to persuade', ()),
           'run_blog': ('to entertain and reflect', ()), 'scooter_leaflet': ('to instruct', ('to inform',)), 'scooter_voxpop': ('to entertain and air opinions', ('to inform',)),
           'cinema_feature': ('to inform', ('to entertain and reflect',)), 'cinema_thread': ('to entertain and air opinions', ('to inform', 'to entertain and reflect'))}
PURPOSES = ['to persuade', 'to inform', 'to instruct', 'to evaluate', 'to entertain and reflect', 'to entertain and air opinions']

KCONV = {
    'speech': ['direct address to a listening audience', 'spoken signposting to guide listeners through the points', 'a rousing call to action at the end'],
    'blog post': ['a personal first-person voice addressing a community of readers', 'informal register with conversational asides', 'an invitation to readers to comment, follow or join in'],
    'news report': ['a headline and a lead paragraph summarising the key facts', 'quotations attributed to named sources', 'an inverted-pyramid structure, with the most important facts first'],
    'review': ['an evaluative verdict, often a star rating', 'balanced praise and criticism of specific features', 'comment on value for money'],
    'transcript of spontaneous speech': ['fillers, pauses and overlaps recorded with a transcription key', 'turns labelled by speaker initials', 'non-fluency features such as false starts and repairs'],
    'information leaflet': ['clear headings and bullet points for quick scanning', 'imperatives and modal verbs giving rules or instructions', 'signposting to further information or contact details'],
    'travel memoir': ['retrospective first-person narration of a real journey', 'reflection on the personal significance of the experience', 'descriptive detail of real places and people met'],
    'editorial': ['an unsigned opinion representing the publication', 'concession and rebuttal of opposing views', 'a firm recommendation in the conclusion'],
    'web page': ['hyperlinks and interactive buttons', 'banner images and short, scannable sections', 'testimonials from previous customers'],
    'charity appeal': ['a case study of one person the charity has helped', 'a direct request for money or action', 'an explanation of what the reader’s support will pay for'],
    'feature article': ['a human-interest angle with interviews', 'more descriptive, personal writing than a hard news report', 'a memorable closing line (a ‘kicker’)'],
    'online comment thread': ['usernames and replies addressed with @', 'short, informal posts in many voices', 'emoji and non-standard punctuation for tone'],
    'advertising leaflet': ['a slogan and an eye-catching image', 'brief persuasive copy with practical details', 'an incentive or offer to prompt action'],
}
for e in EXTRACTS:
    e.tname = TNAME[e.id]
    e.pp, e.pp_also = PURPOSE[e.id]


def short_label(e):
    return re.sub(r'^Text [AB], ', '', e.label)


def feats_of(fws=None, spoken=None, multi=None, exs=None):
    out = []
    for f in FEATS:
        if fws and f.fw not in fws:
            continue
        if spoken is not None and f.ex.spoken != spoken:
            continue
        if multi is not None and f.ex.multimodal != multi:
            continue
        if exs and f.ex not in exs:
            continue
        out.append(f)
    return out


def feat_mcq(r, f, pool=None, frame=None):
    pool = pool or FPOOL[f.fw]
    ds = [cap(d) for d in pool if d != f.feature and d not in f.also]
    opts, ans = mcq(r, cap(f.feature), ds)
    frame = frame or r.choice(['Which language feature is used in {q} ({src})?', 'In {src}, the writer writes {q}. Identify the feature used.',
                               'Read {q} from {src}. Which term best describes this feature?'])
    return {'stem': frame.format(q=Q(f.quote), src=short_label(f.ex)), 'options': opts, 'answer': ans,
            'key': f'{cap(f.feature)}: {FDEF[f.feature]}. Here {Q(f.quote)}: {f.effect}.'}


def effect_key(m, f, focus=''):
    pts = [f'names or describes the feature accurately ({f.feature}, {FWNAME[f.fw]})', f'explains the effect: {f.effect}',
           f'links the effect to the audience ({f.ex.audience}) or purpose ({f.ex.purpose})', 'develops the point with a second connotation or a link to the wider text']
    return f'{upto(m)}: ' + '; '.join(f'1 mark – {p}' for p in pts[:max(1, m)]) + '.' + (f' {focus}' if focus else '')


# =========================================================== 1 Reading: text types and analysis

# ---------------------------------------------------------------- 1.1 text types and conventions
N11 = 'Text types and conventions: speeches, articles, reviews, blogs, transcripts'
t11 = topic(N11, N11)
t11.fixed('C1', (1, 2), [
    ('In AS English Language, what does the term ‘genre’ (text type) refer to?', 'A category of text recognised by shared conventions of form, purpose and language',
     'Genre = a text type (speech, review, blog …) identified by its conventions.', ['The topic a text is about', 'The length of a text', 'The writer’s personal opinion']),
    ('What is meant by the ‘mode’ of a text?', 'Whether it is spoken, written or multimodal (or a blend of these)', 'Mode = the channel of communication; many modern texts blend modes.',
     ['The most frequent word in it', 'Its level of formality', 'The date it was produced']),
    ('Which text type most typically uses an inverted-pyramid structure?', 'A news report', 'News reports place the most important facts first, then supporting detail.',
     ['A travel memoir', 'A podcast transcript', 'A personal blog post']),
    ('Which feature most clearly distinguishes a transcript of spontaneous speech from a scripted speech?', 'Non-fluency features such as fillers, false starts and overlaps',
     'Spontaneous speech is unplanned, so it shows non-fluency features.', ['Use of the first person', 'A clear topic', 'Use of questions']),
    ('A text gives a star rating and weighs good and bad points of a product. What text type is it most likely to be?', 'A review',
     'Reviews evaluate and give a verdict.', ['An editorial', 'An information leaflet', 'A memoir']),
])


@t11.add('C1', (1, 2, 3))
def t11_conv(r, D):
    kind = r.choice(list(KCONV))
    good = r.choice(KCONV[kind])
    others = [c for k, cs in KCONV.items() if k != kind and TGROUP.get(k) != TGROUP.get(kind) for c in cs]
    opts, ans = mcq(r, cap(good), [cap(c) for c in r.sample(others, 6)])
    return {'stem': r.choice([f'Which convention is MOST typical of {an(kind)} {kind}?', f'A student is identifying the conventions of {an(kind)} {kind}. Which of these should they expect to find?']),
            'options': opts, 'answer': ans, 'key': f'{cap(good)} is a convention of {an(kind)} {kind}; the other options belong to other text types.'}


@t11.add('C1', (1, 2, 3))
def t11_type(r, D):
    e = r.choice(EXTRACTS)
    ds = [k for k in TGROUP if TGROUP[k] != TGROUP[e.tname]]
    opts, ans = mcq(r, cap(e.tname), [cap(d) for d in ds])
    n = 18 + 6 * D
    return {'stem': f'Read the opening of an extract: {Q(e.opening(n))} What type of text is it most likely to be?', 'options': opts, 'answer': ans,
            'key': f'{cap(e.tname)}: ' + '; '.join(c for _, c in e.convs[:2]) + '.'}


@t11.add('C2', (1, 2, 3, 4), 'explain')
def t11_conv_explain(r, D):
    e = r.choice(EXTRACTS)
    q, c = r.choice(e.convs)
    m = marks('C2', D)
    return {'stem': r.choice([f'In {e.label}, the writer includes {Q(q)}. Explain how this is a convention of {an(e.tname)} {e.tname} and why it suits the text’s purpose.',
                              f'Explain why {Q(q)} is typical of {an(e.tname)} {e.tname} such as {short_label(e)}.']),
            'answer': f'It is {c}. It suits {an(e.tname)} {e.tname} whose purpose is {e.purpose}, for {e.audience}.',
            'key': f'{upto(m)}: 1 mark – identifies the convention ({c}); 1 mark – links it to the purpose ({e.purpose}); 1 mark – explains its effect on the audience ({e.audience}).',
            'marks': m}


@t11.add('C2', (2, 3, 4), 'explain')
def t11_why_conv(r, D):
    kind = r.choice(list(KCONV))
    c = r.choice(KCONV[kind])
    m = marks('C2', D)
    who = person(r)
    return {'stem': f'{who} is writing {an(kind)} {kind}. Explain why {an(kind)} {kind} usually includes {c}.',
            'answer': f'Because it helps {an(kind)} {kind} meet its audience’s expectations and its purpose: {c} is part of how readers recognise and use the text type.',
            'key': f'{upto(m)}: 1 mark – what the convention does for the reader or listener; 1 mark – link to the typical purpose of {an(kind)} {kind}; 1 mark – a developed example or consequence of omitting it.',
            'marks': m}


@t11.add('C3', (2, 3, 4, 5), 'explain')
def t11_find(r, D):
    e = r.choice(EXTRACTS)
    n = 2 if D <= 3 else 3
    m = marks('C3', D)
    return {'stem': f'{e.show()} Identify {NUMW[n]} conventions of {an(e.tname)} {e.tname} in this extract. For each, quote the text and explain how it helps the writer achieve the purpose of the text.',
            'answer': ' '.join(f'{Q(q)} – {c}.' for q, c in e.convs[:n]),
            'key': pts_key(m, [f'{Q(q)}: {c}' for q, c in e.convs] + [f'explanation linked to purpose ({e.purpose})']), 'marks': m}


@t11.add('C3', (2, 3, 4, 5), 'multi_step')
def t11_compose(r, D):
    e = r.choice(EXTRACTS)
    c1, c2 = r.sample(e.convs, 2) if len(e.convs) >= 2 else (e.convs[0], e.convs[0])
    f = r.choice(e.feats)
    parts = [
        lambda r: ('State what type of text this is.', cap(e.tname), f'1 mark: {e.tname} [1]'),
        lambda r: ('Identify the intended audience.', cap(e.audience), f'1 mark: {e.audience} [1]'),
        lambda r: (f'Explain how {Q(c1[0])} is a convention of this text type.', cap(c1[1]), f'1 mark identifies the convention; 1 mark explains its function [2]'),
        lambda r: (f'Explain the effect of {Q(f.quote)}.', cap(f.effect), f'1 mark names the feature ({f.feature}); 1 mark effect; 1 mark link to purpose [3]'),
        lambda r: (f'Describe the register of the text and explain why it suits its context.', f'{cap(e.register)}; it suits {e.context}.', f'1 mark register; 1 mark link to context [2]'),
    ]
    return compose(r, e.show(), parts, k=(2, 3, 4), type_='multi_step')


@t11.add('C4', (2, 3, 4, 5), 'long')
def t11_long(r, D):
    e = r.choice(EXTRACTS)
    m = marks('C4', D, long=True)
    task = r.choice([f'Analyse how the writer uses the conventions of {an(e.tname)} {e.tname}, together with language and structure, to achieve the purpose of the text.',
                     f'Discuss how far this extract is a typical {e.tname}. Analyse its form, structure and language in your answer.',
                     f'Analyse the ways in which form, structure and language are used to engage {e.audience}.'])
    ind = '; '.join(c for _, c in e.convs) + '; ' + '; '.join(f'{Q(f.quote)} ({f.feature}): {f.effect}' for f in e.feats[:4]) + f'; register: {e.register}.'
    return {'stem': f'{e.show()} {task}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'analysis', ind), 'type': 'long', 'marks': m}


NEW_KIND = [('a speech', 'spoken signposting, direct address and a call to action'), ('a news report', 'headline, lead paragraph, third person, attributed quotation'),
            ('an information leaflet', 'headings, bullet points, imperatives and contact details'), ('a review', 'evaluative verdict, balanced criticism and a rating'),
            ('a personal blog post', 'first-person voice, informal register and an invitation to respond'), ('a web page', 'banner image, short sections, hyperlinks and a button')]


@t11.add('C4', (2, 3, 4, 5), 'multi_step')
def t11_reform(r, D):
    e = r.choice(EXTRACTS)
    k, conv = r.choice([x for x in NEW_KIND if e.tname not in x[0]])
    m = marks('C4', D)
    return {'stem': f'{e.show()} Explain how the form, structure and language of this {e.tname} would need to change if the same content were presented as {k}. Refer closely to the extract.',
            'answer': f'It would need {conv}; the register ({e.register}) and structure would change to suit the new form; specific phrases such as {Q(e.feats[0].quote)} would be adapted.',
            'key': pts_key(m, [f'conventions of {k}: {conv}', f'change of register from {e.register}', 'change of structure or layout', 'reference to a specific phrase that would change and why',
                               'awareness of how audience or purpose would shift']), 'marks': m}


# ---------------------------------------------------------------- 1.2 audience, purpose and context
N12 = 'Audience, purpose and context of a text'
t12 = topic(N12, N12)
t12.fixed('C1', (1, 2), [
    ('What is meant by the ‘context of production’ of a text?', 'The circumstances in which the text was created, such as who wrote it, when, where and why',
     'Context of production = writer, time, place, publication and motive.', ['The place where a reader happens to read it', 'The number of words it contains', 'The font and layout chosen']),
    ('What is meant by the ‘context of reception’?', 'The circumstances in which an audience reads, hears or views the text',
     'Reception = how, where and by whom the text is received.', ['The writer’s biography', 'The grammar of the first sentence', 'The publisher’s address']),
    ('A text is written for parents but will also be read by teachers. What are the teachers?', 'A secondary audience', 'Primary audience = the main target; secondary = others who will also read it.',
     ['The primary audience', 'The writer', 'The context of production']),
    ('Which term describes the relationship between writer and audience, shown through levels of formality?', 'Tenor', 'In register analysis, field = subject, tenor = relationship, mode = channel.',
     ['Field', 'Mode', 'Genre']),
    ('Which word best describes a text whose main purpose is to tell readers how to do something safely?', 'Instructive', 'Instructive texts direct actions, often with imperatives.',
     ['Reflective', 'Entertaining', 'Descriptive']),
])


@t12.add('C1', (1, 2, 3))
def t12_purpose(r, D):
    e = r.choice(EXTRACTS)
    ds = [p for p in PURPOSES if p != e.pp and p not in e.pp_also]
    opts, ans = mcq(r, cap(e.pp), [cap(d) for d in ds])
    return {'stem': f'{e.show()} What is the primary purpose of this text?', 'options': opts, 'answer': ans,
            'key': f'{cap(e.pp)}: the text aims {e.purpose}.'}


AUDS = ['young children', 'academic specialists', 'government ministers', 'tourists who do not speak the local language', 'retired professional athletes', 'investors in a technology company']


@t12.add('C1', (1, 2, 3))
def t12_aud(r, D):
    e = r.choice(EXTRACTS)
    opts, ans = mcq(r, cap(e.audience), [cap(a) for a in AUDS])
    return {'stem': f'Read the opening of {e.label}: {Q(e.opening(30))} Who is the most likely intended audience?', 'options': opts, 'answer': ans,
            'key': f'{cap(e.audience)}: shown by the register ({e.register}) and the context ({e.context}).'}


@t12.add('C2', (1, 2, 3, 4), 'explain')
def t12_aware(r, D):
    f = r.choice(FEATS)
    e = f.ex
    m = marks('C2', D)
    return {'stem': r.choice([f'In {e.label}, the writer writes {Q(f.quote)}. Explain how this shows awareness of the intended audience ({e.audience}).',
                              f'Explain how {Q(f.quote)} helps {short_label(e)} achieve its purpose ({e.purpose}).']),
            'answer': f'{cap(f.feature)}: {f.effect}.', 'key': effect_key(m, f), 'marks': m}


@t12.add('C2', (2, 3, 4), 'explain')
def t12_context(r, D):
    e = r.choice(EXTRACTS)
    f = r.choice(e.feats)
    m = marks('C2', D)
    return {'stem': f'{short_label(e).capitalize()} is {e.context}. Explain how this context shapes the language of the text, referring to {Q(f.quote)}.',
            'answer': f'The context ({e.context}) leads to a {e.register} register; {Q(f.quote)} is an example: {f.effect}.',
            'key': f'{upto(m)}: 1 mark – identifies a relevant aspect of context (mode, publication, time, relationship); 1 mark – links it to register ({e.register}); 1 mark – explains the quoted example ({f.feature}).',
            'marks': m}


@t12.add('C3', (2, 3, 4, 5), 'multi_step')
def t12_apc(r, D):
    e = r.choice(EXTRACTS)
    fs = r.sample(e.feats, 2)
    who = person(r)
    parts = [
        lambda r: ('Identify the primary audience and give one piece of evidence.', f'{cap(e.audience)}; evidence such as {Q(fs[0].quote)}.', '1 mark audience; 1 mark evidence [2]'),
        lambda r: ('State the main purpose of the text.', cap(e.purpose), f'1 mark: {e.purpose} [1]'),
        lambda r: ('Explain how the context of production affects the text.', f'{cap(e.context)}: this explains its {e.register} register.', '1 mark context; 1 mark effect on language [2]'),
        lambda r: (f'Explain how {Q(fs[1].quote)} is suited to the audience.', cap(fs[1].effect), f'1 mark feature ({fs[1].feature}); 2 marks explanation linked to audience [3]'),
        lambda r: ('Describe the tenor (relationship with the audience) the writer creates.', f'{cap(e.register)}.', '1 mark description; 1 mark supporting reference [2]'),
    ]
    return compose(r, f'{who} is analysing a text. {e.show()}', parts, k=(2, 3, 4), type_='multi_step')


NEW_AUD = [('primary-school children', 'simpler lexis, shorter sentences, a friendly tone and perhaps images'),
           ('elderly residents with little internet access', 'clear print layout, no slang or online references, a respectful tone'),
           ('government officials deciding on funding', 'formal register, evidence and figures, a clear recommendation'),
           ('international visitors', 'no local references or idioms, plain international English, practical details'),
           ('teenagers on social media', 'a short, punchy format, informal lexis, images and hashtags')]


@t12.add('C4', (2, 3, 4, 5), 'multi_step')
def t12_retarget(r, D):
    e = r.choice(EXTRACTS)
    aud, how = r.choice(NEW_AUD)
    m = marks('C4', D)
    return {'stem': f'{e.show()} The text was written for {e.audience}. Explain, with close reference to the text, what changes would be needed to adapt it for {aud}, and why.',
            'answer': f'Changes: {how}; specific phrases such as {Q(e.feats[0].quote)} and {Q(e.feats[-1].quote)} would need adapting because the new audience has different needs and expectations.',
            'key': pts_key(m, [f'awareness of the new audience’s needs ({how})', 'change to register or tenor', 'change to lexis, with an example from the text', 'change to structure, layout or length',
                               'change to purpose or emphasis', 'explanation of why each change suits the new audience']), 'marks': m}


@t12.add('C4', (2, 3, 4, 5), 'long')
def t12_long(r, D):
    e = r.choice(EXTRACTS)
    m = marks('C4', D, long=True)
    task = r.choice(['Analyse how the writer adapts language and structure to suit the audience and purpose of this text.',
                     'How does the context of this text shape its form, structure and language? Analyse closely.',
                     'Analyse how the writer establishes a relationship with the audience in this text.'])
    ind = f'audience: {e.audience}; purpose: {e.purpose}; context: {e.context}; register: {e.register}; ' + '; '.join(f'{Q(f.quote)} ({f.feature}): {f.effect}' for f in e.feats[:5]) + '.'
    return {'stem': f'{e.show()} {task}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'analysis', ind), 'type': 'long', 'marks': m}


# ---------------------------------------------------------------- 1.3 spoken and multimodal texts
N13 = 'Analysing spoken and multimodal texts: transcripts and visual features'
t13 = topic(N13, N13)
t13.fixed('C1', (1, 2), [
    ('In a transcript, what does the symbol (.) usually indicate?', 'A micropause of less than about half a second', 'Transcription key: (.) = micropause; (2) = a two-second pause.',
     ['An overlap', 'A stressed word', 'The end of a sentence']),
    ('In a transcript, what does // usually indicate?', 'The point where speakers begin to overlap', 'Overlapping speech is marked with // at the start of the overlap.', ['A long pause', 'Laughter', 'Rising intonation']),
    ('Why are transcripts of spontaneous speech usually written without standard punctuation?', 'Because speech is organised in utterances, pauses and intonation, not written sentences',
     'Punctuation would impose written sentence boundaries; pauses are marked instead.', ['Because speakers never finish their sentences', 'To save space', 'Because punctuation is too formal']),
    ('What are paralinguistic features?', 'Non-verbal aspects of communication such as laughter, gesture and facial expression',
     'Paralinguistic features accompany speech: laughter, gesture, tone of voice.', ['Words borrowed from other languages', 'Grammatical errors', 'Pauses within words']),
    ('What is a multimodal text?', 'A text that combines more than one mode, such as writing, images, sound or interactive elements',
     'E.g. a web page with images, text and buttons.', ['A text with many paragraphs', 'A text in several languages', 'A text read aloud only']),
    ('What is an adjacency pair?', 'Two related turns in which the first prompts the second, such as question and answer', 'Adjacency pairs: greeting–greeting, question–answer, offer–acceptance.',
     ['Two words that rhyme', 'Two speakers talking at once', 'A pair of synonyms']),
])

SPOOL = ['filler', 'overlap', 'back-channelling', 'false start', 'tag question', 'vague language', 'phatic talk', 'echoing', 'reformulation', 'prosodic stress', 'ellipsis', 'discourse marker', 'repetition']
SP_SNIP = [
    ('A: are you coming tonight B: yeah (.) yeah I think so', 'repetition', 'the repeated ‘yeah’ gives B time to commit while sounding agreeable'),
    ('A: so I went to the bank and // they said B: // oh no', 'overlap', 'B’s overlapping sympathy is supportive rather than an interruption'),
    ('A: it was (.) it was sort of (.) amazing', 'false start', 'A restarts the utterance while searching for the right word'),
    ('A: you’ve finished the report haven’t you', 'tag question', 'the tag seeks confirmation and puts gentle pressure on the listener'),
    ('A: we could get pizza or something', 'vague language', 'the vague tag keeps the suggestion open and polite'),
    ('A: lovely weather again B: isn’t it just', 'phatic talk', 'the exchange maintains friendly contact rather than giving information'),
    ('A: I erm (.) I wasn’t sure what to say', 'filler', 'the filler marks hesitation and planning time'),
    ('A: the train was late B: mm A: so I ran B: right', 'back-channelling', 'B’s minimal responses show attention and encourage A to continue'),
    ('A: the price went up AGAIN', 'prosodic stress', 'the stress conveys frustration that the rise is repeated'),
    ('A: coming to the match B: might be', 'ellipsis', 'subjects and auxiliaries are omitted because the context makes them clear'),
    ('A: so you’re saying we start earlier B: yes exactly', 'reformulation', 'A rephrases B’s point to check understanding'),
    ('A: well (.) anyway (.) where were we', 'discourse marker', 'the markers close a digression and return to the main topic'),
    ('A: the bus broke down B: broke down', 'echoing', 'B repeats A’s words to express surprise and prompt more detail'),
    ('A: you know what I mean B: totally', 'discourse marker', 'the marker checks shared understanding and invites agreement'),
]
SP_CTX = ['two friends planning a weekend', 'colleagues talking in an office kitchen', 'a customer and a shop assistant', 'two students revising for an exam', 'neighbours chatting over a fence',
          'a parent and a teenager in a car']


@t13.add('C1', (1, 2, 3))
def t13_spot(r, D):
    if r.random() < 0.5:
        f = r.choice(feats_of(spoken=True))
        return feat_mcq(r, f, pool=SPOOL if f.feature in SPOOL else None, frame='In {src} a speaker says {q}. Which feature of spoken language does this show?')
    line, feat, why = r.choice(SP_SNIP)
    opts, ans = mcq(r, cap(feat), [cap(x) for x in SPOOL if x != feat])
    return {'stem': f'In a conversation between {r.choice(SP_CTX)}: {Q(line)} Which spoken-language feature is shown?', 'options': opts, 'answer': ans,
            'key': f'{cap(feat)}: {FDEF[feat]}; {why}.'}


@t13.add('C1', (1, 2, 3))
def t13_visual(r, D):
    f = r.choice(feats_of(fws=['graphology']))
    return feat_mcq(r, f, frame='{src} includes {q}. Which visual or graphological feature is this?')


@t13.add('C2', (1, 2, 3, 4), 'explain')
def t13_explain(r, D):
    m = marks('C2', D)
    if r.random() < 0.5:
        line, feat, why = r.choice(SP_SNIP)
        ctx = r.choice(SP_CTX)
        return {'stem': f'In a conversation between {ctx}, this exchange occurs: {Q(line)} Identify the spoken-language feature and explain its function in the interaction.',
                'answer': f'{cap(feat)}: {why}.', 'key': f'{upto(m)}: 1 mark – identifies {feat}; 1 mark – explains its function ({why}); 1 mark – links to the relationship between speakers or the context.', 'marks': m}
    f = r.choice(feats_of(spoken=True) + feats_of(fws=['graphology']))
    return {'stem': f'Explain the function of {Q(f.quote)} in {f.ex.label}.', 'answer': f'{cap(f.feature)}: {f.effect}.', 'key': effect_key(m, f), 'marks': m}


@t13.add('C3', (2, 3, 4, 5), 'explain')
def t13_analyse(r, D):
    e = r.choice(SPOKEN + MULTI)
    n = 2 if D <= 3 else 3
    m = marks('C3', D)
    fs = e.feats
    what = 'features of spontaneous speech' if e.spoken else 'visual and verbal features'
    extra = ' Comment on what they reveal about the relationship between the speakers.' if e.spoken else ' Explain how the visual and written elements work together.'
    return {'stem': f'{e.show()} Analyse {NUMW[n]} {what} in this text.{extra}', 'answer': ' '.join(f'{Q(f.quote)} – {f.feature}: {f.effect}.' for f in fs[:n]),
            'key': pts_key(m, [f'{Q(f.quote)} ({f.feature}): {f.effect}' for f in fs]), 'marks': m}


@t13.add('C3', (1, 2, 3, 4), 'multi_step')
def t13_compose(r, D):
    e = r.choice(SPOKEN)
    fs = r.sample(e.feats, 3)
    parts = [
        lambda r: (f'Identify the feature shown by {Q(fs[0].quote)}.', cap(fs[0].feature), f'1 mark: {fs[0].feature} [1]'),
        lambda r: (f'Explain the function of {Q(fs[1].quote)} in the conversation.', cap(fs[1].effect), f'1 mark feature; 1 mark function [2]'),
        lambda r: ('Who controls the conversation? Give evidence.', 'The interviewer/presenter largely manages turns and topics; evidence from questions and prompts.' if e.id != 'phones_podcast' else
                   'Control is shared, but Kenji opens and steers topics; Zara holds the longest turns.', '1 mark judgement; 1 mark evidence [2]'),
        lambda r: (f'Explain how {Q(fs[2].quote)} shows that the speech is unplanned or interactive.', cap(fs[2].effect), '1 mark feature; 2 marks explanation [3]'),
    ]
    return compose(r, e.show(), parts, k=(2, 3), type_='multi_step')


@t13.add('C4', (2, 3, 4, 5), 'long')
def t13_long(r, D):
    e = r.choice(SPOKEN + MULTI)
    m = marks('C4', D, long=True)
    if e.spoken:
        task = r.choice(['Analyse the features of spontaneous speech in this transcript and explain what they reveal about the speakers’ roles and relationships.',
                         'Analyse how the speakers use language to express opinions and manage the interaction.'])
    else:
        task = r.choice(['Analyse how this text combines visual and verbal features to achieve its purpose.', 'Analyse how layout, images and language work together to engage the audience.'])
    ind = '; '.join(f'{Q(f.quote)} ({f.feature}): {f.effect}' for f in e.feats) + f'; context: {e.context}.'
    return {'stem': f'{e.show()} {task}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'analysis', ind), 'type': 'long', 'marks': m}


# ---------------------------------------------------------------- 1.4 comparing two texts
N14 = 'Comparing two texts: similarities and differences in form and language'
t14 = topic(N14, N14)
t14.fixed('C1', (1, 2), [
    ('In a comparative analysis, what is the most effective way to organise the answer?', 'Integrate the texts, comparing them point by point throughout',
     'Integrated comparison is rewarded more highly than writing about each text separately.', ['Write about Text A, then Text B, with no links', 'Summarise both texts', 'Discuss only the text you prefer']),
    ('Which connective signals a contrast between two texts?', 'whereas', '‘Whereas’, ‘however’, ‘in contrast’ signal difference; ‘similarly’ signals similarity.', ['similarly', 'likewise', 'in the same way']),
    ('In a comparison, what does ‘form’ refer to?', 'The type and shape of each text, such as transcript, leaflet or article, and its conventions',
     'Form = text type and its conventions; language = lexis, grammar and so on.', ['Only the length of each text', 'The topic of the texts', 'The writer’s handwriting']),
])


def pair_texts(r):
    key = r.choice(list(PAIRS))
    return PAIRS[key]


def both(A, B):
    return f'{A.show()} {B.show()}'


@t14.add('C1', (1, 2, 3))
def t14_true(r, D):
    topic_, A, B, true, false = pair_texts(r)
    opts, ans = mcq(r, r.choice(true), false)
    return {'stem': f'Text A is {short_label(A)}; Text B is {short_label(B)}. Both are about {topic_}. {Q(A.opening(25))} / {Q(B.opening(25))} Which statement about the two texts is accurate?',
            'options': opts, 'answer': ans, 'key': f'{ans}. The other statements are contradicted by the texts.'}


def pair_feats(A, B, same_fw=True):
    pairs = [(fa, fb) for fa in A.feats for fb in B.feats if (fa.fw == fb.fw or not same_fw)]
    return pairs


@t14.add('C2', (1, 2, 3, 4), 'explain')
def t14_quotes(r, D):
    topic_, A, B, true, false = pair_texts(r)
    fa, fb = r.choice(pair_feats(A, B))
    m = marks('C2', D)
    return {'stem': f'Text A ({short_label(A)}) includes {Q(fa.quote)}. Text B ({short_label(B)}) includes {Q(fb.quote)}. Compare how these quotations reflect the different forms and purposes of the two texts.',
            'answer': f'Text A: {fa.feature} – {fa.effect}. Text B: {fb.feature} – {fb.effect}. The difference reflects {A.purpose} versus {B.purpose}.',
            'key': f'{upto(m)}: 1 mark – feature/effect in Text A ({fa.feature}); 1 mark – feature/effect in Text B ({fb.feature}); 1 mark – a comparative point linked to form or purpose (e.g. {true[0]}).', 'marks': m}


@t14.add('C2', (2, 3, 4), 'explain')
def t14_form(r, D):
    topic_, A, B, true, false = pair_texts(r)
    m = marks('C2', D)
    asp = r.choice(['form', 'register', 'purpose', 'relationship with the audience'])
    return {'stem': f'Text A is {short_label(A)} and Text B is {short_label(B)}, both on {topic_}. Explain one difference in {asp} between the two texts.',
            'answer': r.choice(true), 'key': f'{upto(m)}: 1 mark – identifies a valid difference in {asp}; 1 mark – supporting reference to each text; 1 mark – explains the reason for the difference (form/purpose/context). E.g. {true[0]}.', 'marks': m}


@t14.add('C3', (2, 3, 4, 5), 'multi_step')
def t14_compose(r, D):
    topic_, A, B, true, false = pair_texts(r)
    fa, fb = r.choice(pair_feats(A, B))
    parts = [
        lambda r: ('Identify one similarity in the purpose of the two texts.', f'Both concern {topic_}; A aims {A.purpose}, B aims {B.purpose}.', '1 mark similarity; 1 mark reference [2]'),
        lambda r: ('Compare the register of the two texts.', f'A is {A.register}; B is {B.register}.', '1 mark each text; 1 mark comparative comment [3]'),
        lambda r: (f'Compare the effect of {Q(fa.quote)} (Text A) with {Q(fb.quote)} (Text B).', f'A: {fa.effect}. B: {fb.effect}.', '1 mark each effect; 1 mark comparison [3]'),
        lambda r: ('Explain one difference in form and its effect.', true[1] if len(true) > 1 else true[0], '1 mark difference; 1 mark effect [2]'),
    ]
    return compose(r, both(A, B), parts, k=(2, 3), type_='multi_step')


@t14.add('C4', (2, 3, 4, 5), 'long')
def t14_long(r, D):
    topic_, A, B, true, false = pair_texts(r)
    m = marks('C4', D, long=True)
    task = r.choice(['Compare the form, structure and language of Text A and Text B.', f'Compare how Text A and Text B present {topic_}. Analyse form, structure and language.',
                     'Compare the ways in which the two texts engage their audiences.'])
    ind = '; '.join(true) + '; Text A: ' + '; '.join(f'{Q(f.quote)} ({f.feature})' for f in A.feats[:3]) + '; Text B: ' + '; '.join(f'{Q(f.quote)} ({f.feature})' for f in B.feats[:3]) + '.'
    return {'stem': f'{both(A, B)} {task}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'compare', ind), 'type': 'long', 'marks': m}


CHAPTERS[1] = [t11, t12, t13, t14]


@t14.add('C4', (2, 3, 4, 5), 'multi_step')
def t14_quote_set(r, D):
    topic_, A, B, true, false = pair_texts(r)
    fa = r.sample(A.feats, 2)
    fb = r.sample(B.feats, 2)
    m = marks('C4', D)
    focus = r.choice(['tone', 'the relationship with the audience', 'how each writer conveys attitude', 'the effect of the different forms'])
    return {'stem': f'Text A is {short_label(A)}; Text B is {short_label(B)}, both on {topic_}. From Text A: (i) {Q(fa[0].quote)} (ii) {Q(fa[1].quote)}. From Text B: (iii) {Q(fb[0].quote)} (iv) {Q(fb[1].quote)}. '
                    f'Using these quotations, compare the two texts, focusing on {focus}.',
            'answer': ' '.join(f'{Q(f.quote)}: {f.feature} – {f.effect}.' for f in fa + fb) + f' Overall: {true[0]}.',
            'key': pts_key(m, [f'{Q(f.quote)} – {f.feature}: {f.effect}' for f in fa + fb] + [f'a comparative judgement, e.g. {true[0]}'], 'At least one mark must come from an explicit comparison.'), 'marks': m}


# =========================================================== 2 Directed response (Paper 1 Question 1(a))

TARGETS = [
    ('a letter to a local newspaper', 'the newspaper’s readers', 'letter'), ('a short assembly speech', 'secondary-school students', 'speech'),
    ('an information leaflet', 'members of the public', 'leaflet'), ('a blog post', 'young adults who follow a community blog', 'blog'),
    ('a news report for a community website', 'local residents', 'report'), ('a diary entry', 'yourself alone', 'diary'),
    ('a script for a 60-second radio advertisement', 'local radio listeners', 'radio'), ('an email', 'a close friend who lives abroad', 'email'),
    ('a formal report', 'a city council committee', 'formal report'), ('a magazine article', 'teenage readers', 'article'),
]
TREG = {'letter': 'formal and courteous', 'speech': 'direct, spoken and rousing', 'leaflet': 'clear, concise and instructive', 'blog': 'personal and conversational',
        'report': 'objective and impersonal', 'diary': 'private, informal and reflective', 'radio': 'lively, spoken and punchy', 'email': 'friendly and informal',
        'formal report': 'formal, objective and impersonal', 'article': 'engaging and semi-formal', 'review': 'lively and evaluative'}
TCONV = {
    'letter': ['an appropriate salutation and sign-off', 'a clear statement of purpose in the opening paragraph', 'a formal, courteous register'],
    'speech': ['direct address and inclusive pronouns for a listening audience', 'spoken signposting such as ‘first’ and ‘finally’', 'a memorable ending with a call to action'],
    'leaflet': ['headings and subheadings', 'bullet points for key information', 'imperatives and contact details'],
    'blog': ['a first-person, conversational voice', 'a personal angle and anecdote', 'an invitation for readers to respond'],
    'report': ['a headline and a lead sentence answering who, what, where and when', 'third-person, impersonal narration', 'quotations attributed to named people'],
    'diary': ['first-person, past-tense reflection on the day', 'private thoughts and feelings', 'an informal, intimate register'],
    'radio': ['sound effects and voice directions', 'repetition of the key message and contact details', 'short, punchy spoken sentences'],
    'email': ['a friendly greeting and sign-off', 'informal, colloquial lexis', 'shared references between writer and reader'],
    'formal report': ['a title, numbered sections and subheadings', 'an objective, impersonal register', 'recommendations based on findings'],
    'article': ['a catchy headline and standfirst', 'engaging direct address to the reader', 'paragraphs developing an angle with examples'],
}
ROLES = {
    'roof_speech': ['a resident who attended the meeting', 'the councillor who gave the speech'], 'roof_blog': ['Mrs Okafor, one of the volunteers', 'the blogger'],
    'water_news': ['Dr Leila Haddad of the water authority', 'a resident affected by the restrictions'], 'water_phonein': ['Samuel, the caller', 'the radio presenter'],
    'market_review': ['one of the two sisters who run the dumpling stall', 'the food reviewer'], 'market_leaflet': ['the market organiser', 'a family who visited the market'],
    'trek_memoir': ['Pema, the guide', 'the narrator'], 'trek_web': ['the trekking company’s marketing manager', 'a customer who has just booked the trek'],
    'phones_podcast': ['Zara, one of the presenters', 'the head teacher of the school'], 'phones_editorial': ['a parent who disagrees with the editorial', 'the editor of the newspaper'],
    'run_appeal': ['Mateo’s parent', 'a volunteer at the charity'], 'run_blog': ['the blogger', 'the woman in the pink tutu'],
    'scooter_leaflet': ['a city transport officer', 'a student who rides an e-scooter'], 'scooter_voxpop': ['R2, the dog owner', 'R1, the commuter'],
    'cinema_feature': ['Mr Farouk, the projectionist', 'a long-time customer of the Rialto'], 'cinema_thread': ['@nadia.k', 'the local history group'],
}
WRANGE = {1: '100–120', 2: '120–150', 3: '120–150', 4: '120–150', 5: '120–150'}


def target_for(r, e):
    opts = [t for t in TARGETS if not (t[2] in ('blog',) and e.tname == 'blog post') and not (t[2] == 'speech' and e.tname == 'speech')
            and not (t[2] == 'leaflet' and 'leaflet' in e.tname) and not (t[2] == 'report' and e.tname == 'news report')]
    return r.choice(opts)


def directed(r, D, e, emphasis=''):
    form, aud, k = target_for(r, e)
    role = r.choice(ROLES[e.id])
    m = marks('C4', D, long=True)
    w = WRANGE[D]
    stem = (f'{e.show()} You are {role}. Using material from the text, write {form} written for {aud} ({w} words). '
            f'Base your answer closely on the text, adapting its content for your new audience and purpose.{emphasis}')
    ind = (f'Form: {"; ".join(TCONV[k])}. Content selected from the source: ' + '; '.join(e.points[:5]) +
           f'. Voice: convincingly that of {role}. Register shifted from the source’s {e.register} register to suit {aud}.')
    return {'stem': stem, 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'directed', ind), 'type': 'long', 'marks': m}


# ---------------------------------------------------------------- 2.1 transforming a text
N21 = 'Transforming a source text for a new audience, purpose and form'
t21 = topic(N21, N21)
t21.fixed('C1', (1, 2), [
    ('In a directed response, what does the examiner mainly reward?', 'Writing that suits the new form, audience and purpose while using the source material',
     'Directed response tests the transformation of source material for a new task.', ['Copying as much of the source as possible', 'Analysis of the source’s language', 'Personal opinions unrelated to the source']),
    ('What is the main risk of writing well beyond the word range in a directed response?', 'Material beyond the limit may not be credited and selection skills are not shown',
     'The word range tests selection and concision.', ['The examiner will add marks for effort', 'Nothing – longer is always better', 'The answer becomes an essay']),
    ('A source text is a formal report; the task is a diary entry. Which change is most essential?', 'Shifting to a first-person, personal and reflective voice',
     'A diary is private, first person and reflective.', ['Adding numbered sections', 'Including a headline', 'Using more statistics']),
    ('In a directed response, ‘transformation’ means …', 'reshaping the source’s content into a different form for a different audience and purpose',
     'Ideas stay; form, register and emphasis change.', ['translating the source into another language', 'correcting the errors in the source', 'summarising the source in note form']),
])


@t21.add('C1', (1, 2, 3))
def t21_conv(r, D):
    form, aud, k = r.choice(TARGETS)
    good = r.choice(TCONV[k])
    others = [c for kk, cs in TCONV.items() if kk != k and not ({kk, k} <= {'report', 'formal report'}) and not ({kk, k} <= {'diary', 'email', 'blog'}) for c in cs]
    opts, ans = mcq(r, cap(good), [cap(c) for c in r.sample(others, 6)])
    return {'stem': f'A directed-response task asks you to write {form} written for {aud}. Which feature should your response include?', 'options': opts, 'answer': ans,
            'key': f'{cap(good)} is a convention of {form}.'}


@t21.add('C2', (1, 2, 3, 4), 'explain')
def t21_changes(r, D):
    e = r.choice(EXTRACTS)
    form, aud, k = target_for(r, e)
    m = marks('C2', D)
    return {'stem': f'A student is transforming {e.label} into {form} written for {aud}. Explain two changes they will need to make to form and register.',
            'answer': f'Form: adopt {TCONV[k][0]} and {TCONV[k][1]}. Register: move from the source’s {e.register} register to a {TREG[k]} register suited to {aud}.',
            'key': f'{upto(m)}: 1 mark – a relevant change of form ({TCONV[k][0]}); 1 mark – a relevant change of register or tenor; 1 mark – explanation linked to the new audience ({aud}).', 'marks': m}


@t21.add('C3', (2, 3, 4, 5), 'short')
def t21_opening(r, D):
    e = r.choice(EXTRACTS)
    form, aud, k = target_for(r, e)
    m = marks('C3', D)
    n = {2: 40, 3: 50, 4: 60, 5: 80}.get(D, 40)
    return {'stem': f'{e.show()} Write the opening (about {n} words) of {form} written for {aud}, based on this text. Then explain one choice you made to suit the new form.',
            'answer': f'An opening that uses {TCONV[k][0]} and adapts a point from the source such as ‘{e.points[0]}’, in a register suited to {aud}; explanation of one choice.',
            'key': pts_key(m, [f'opening clearly in the new form ({TCONV[k][0]})', 'register suited to the new audience', 'content adapted (not lifted) from the source', 'accurate, controlled expression',
                               'a valid explanation of one choice']), 'marks': m}


@t21.add('C3', (2, 3, 4, 5), 'multi_step')
def t21_plan(r, D):
    e = r.choice(EXTRACTS)
    form, aud, k = target_for(r, e)
    parts = [
        lambda r: (f'State two conventions of {form}.', f'{cap(TCONV[k][0])}; {TCONV[k][1]}.', '1 mark each [2]'),
        lambda r: ('Identify two pieces of content from the text you would include.', '; '.join(cap(p) for p in e.points[:2]), '1 mark each relevant point [2]'),
        lambda r: (f'Describe the register you would adopt for {aud} and explain why.', f'{cap(TREG[k])}, because the new audience is {aud} and the form is {form}.', '1 mark register; 1 mark reason [2]'),
        lambda r: (f'Write an opening sentence for {form}.', f'A sentence using {TCONV[k][0]}.', '1 mark form; 1 mark register [2]'),
        lambda r: ('Identify one feature of the source you would NOT keep, and explain why.', f'E.g. {Q(e.feats[0].quote)}, which suits {an(e.tname)} {e.tname} but not {form}.', '1 mark feature; 1 mark reason [2]'),
    ]
    return compose(r, f'{e.show()} You are planning {form} written for {aud} based on this text.', parts, k=(2, 3, 4), type_='multi_step')


@t21.add('C4', (2, 3, 4, 5), 'long')
def t21_task(r, D):
    return directed(r, D, r.choice(EXTRACTS))


# ---------------------------------------------------------------- 2.2 selecting and adapting content
N22 = 'Selecting and adapting content from the source text'
t22 = topic(N22, N22)
t22.fixed('C1', (1, 2), [
    ('What is ‘lifting’ in a directed response?', 'Copying phrases or sentences directly from the source without adapting them',
     'Lifting shows little transformation and is not rewarded.', ['Using a quotation in an analysis', 'Lifting the tone of a text', 'Removing irrelevant content']),
    ('When selecting material for a directed response, which details should be prioritised?', 'Those most relevant to the new audience and purpose',
     'Selection is driven by the task, not by the order of the source.', ['The first details in the source', 'The most unusual words in the source', 'Every statistic, whatever the task']),
    ('Which is an example of adapting rather than lifting?', 'Turning a statistic into a comparison a child would understand',
     'Adaptation reshapes content for the new reader.', ['Copying a whole paragraph', 'Underlining key words in the source', 'Quoting the headline exactly']),
])


@t22.add('C1', (1, 2, 3))
def t22_accurate(r, D):
    e = r.choice(EXTRACTS)
    opts, ans = mcq(r, cap(r.choice(e.points)), [cap(x) for x in e.false])
    return {'stem': f'{e.show()} A student is selecting content from this text for a directed response. Which of these points is accurate?', 'options': opts, 'answer': ans,
            'key': f'{ans} is stated in the text; the other options misrepresent it.'}


@t22.add('C2', (1, 2, 3, 4), 'explain')
def t22_lift(r, D):
    f = r.choice(FEATS)
    e = f.ex
    form, aud, k = target_for(r, e)
    m = marks('C2', D)
    return {'stem': f'A student writing {form} written for {aud}, based on {e.label}, copies {Q(f.quote)} word for word. Explain why this is weak and how the content could be adapted.',
            'answer': f'It is lifting: the phrase belongs to the source’s form ({e.tname}) and {e.register} register; it should be rephrased in the voice and register of {form} written for {aud}.',
            'key': f'{upto(m)}: 1 mark – identifies lifting/lack of transformation; 1 mark – explains the mismatch of form or register; 1 mark – a valid adapted version or method.', 'marks': m}


@t22.add('C2', (2, 3, 4), 'explain')
def t22_relevance(r, D):
    e = r.choice(EXTRACTS)
    form, aud, k = target_for(r, e)
    p1, p2 = r.sample(e.points, 2)
    m = marks('C2', D)
    return {'stem': f'For {form} written for {aud}, based on {short_label(e)}, a student must choose between including ‘{p1}’ and ‘{p2}’. Explain which is more useful and why.',
            'answer': f'Either, if justified: the better choice is the one that serves the purpose of {form} and interests {aud}.',
            'key': f'{upto(m)}: 1 mark – a clear choice; 1 mark – justification linked to audience ({aud}); 1 mark – justification linked to the purpose or form.', 'marks': m}


@t22.add('C3', (1, 2, 3, 4, 5), 'explain')
def t22_select(r, D):
    e = r.choice(EXTRACTS)
    form, aud, k = target_for(r, e)
    n = 2 + (D >= 3) + (D >= 5)
    m = marks('C3', D)
    return {'stem': f'{e.show()} Select {NUMW[n]} points from this text that would be most useful for {form} written for {aud}. Then explain how you would adapt one of them.',
            'answer': '; '.join(cap(p) for p in e.points[:n]) + '. Adaptation: rephrase in a register suited to the new audience.',
            'key': pts_key(m, [cap(p) for p in e.points] + ['a valid explanation of adapting one point']), 'marks': m}


@t22.add('C3', (2, 3, 4, 5), 'short')
def t22_summary(r, D):
    e = r.choice(EXTRACTS)
    w = {2: 40, 3: 50, 4: 60, 5: 70}.get(D, 50)
    m = marks('C3', D)
    return {'stem': f'{e.show()} In no more than {w} words, and using your own words as far as possible, summarise the main points of this text for a reader who has not seen it.',
            'answer': ' '.join(cap(p) + '.' for p in e.points), 'key': pts_key(m, [cap(p) for p in e.points], 'Deduct for lifting long phrases or for exceeding the word limit significantly.'), 'marks': m}


@t22.add('C4', (2, 3, 4, 5), 'long')
def t22_task(r, D):
    e = r.choice(EXTRACTS)
    return directed(r, D, e, emphasis=' Select only the material that is relevant to your audience, and reshape it rather than copying it.')


# ---------------------------------------------------------------- 2.3 register, tone and voice
N23 = 'Controlling register, tone and voice in a directed response'
t23 = topic(N23, N23)
TONES = ['formal and impersonal', 'informal and chatty', 'sarcastic', 'nostalgic', 'urgent and alarmed', 'reassuring', 'technical', 'enthusiastic', 'apologetic', 'authoritative']
TONE_SNIP = [
    ('Residents are advised that the bridge will be closed until further notice.', 'formal and impersonal'), ('So yeah, turns out I’m rubbish at camping. Who knew?', 'informal and chatty'),
    ('Oh wonderful, another meeting that could have been an email.', 'sarcastic'), ('We used to walk to that bakery every Saturday, when the street still smelled of bread.', 'nostalgic'),
    ('Leave the building now – the fire is spreading towards the stairwell!', 'urgent and alarmed'), ('There is no need to worry: your data is safe and nothing has been lost.', 'reassuring'),
    ('The compressor operates at 3.5 bar with a duty cycle of sixty per cent.', 'technical'), ('This is hands down the best festival line-up we have ever had!', 'enthusiastic'),
    ('We are very sorry for the delay and for any inconvenience this has caused.', 'apologetic'), ('All visitors must sign in at reception. No exceptions will be made.', 'authoritative'),
    ('Can you believe it? Free pizza for every volunteer this Friday!', 'enthusiastic'), ('Applicants should submit two references with the completed form.', 'formal and impersonal'),
    ('Please accept our apologies – your order was sent to the wrong address.', 'apologetic'), ('Back then, the harbour was full of wooden boats and nobody locked their doors.', 'nostalgic'),
]
REG_ERR = [
    ('a formal letter to a city council', 'Hey guys, the scooters are a total nightmare and you need to sort it.', 'the greeting and slang (‘hey guys’, ‘total nightmare’, ‘sort it’) are far too informal for officials',
     'I am writing to express concern about the safety risks posed by e-scooters, and to ask the council to review its regulations.'),
    ('a speech to younger students', 'It is incumbent upon all pupils to ensure adherence to the revised electronic-device protocol.', 'the Latinate, bureaucratic lexis is too formal and distant for young listeners',
     'From Monday, phones stay in your bag all day. Here’s why that might be a good thing.'),
    ('a diary entry', 'The participant experienced considerable fatigue at kilometre thirty.', 'the third-person, clinical register is wrong for a private, personal diary',
     'Kilometre thirty nearly finished me. My legs felt like concrete.'),
    ('a review for a teenage magazine', 'The establishment provides adequate nutritional options at a reasonable cost.', 'the impersonal register lacks the lively, evaluative voice teenage readers expect',
     'Cheap, cheerful and seriously tasty – this place is a winner.'),
    ('an information leaflet for tourists', 'You’ll probably wanna, like, not ride on the pavement, yeah?', 'hesitant, slangy phrasing undermines the clear instructions a leaflet needs',
     'Do not ride on pavements. Use roads and cycle lanes only.'),
    ('a news report', 'I reckon the reservoirs are basically empty and it’s scary.', 'personal opinion and colloquial lexis are inappropriate in objective news',
     'Reservoir levels have fallen to 31 per cent, the lowest since records began.'),
    ('a charity appeal email', 'Donations are requested. Ventilators are expensive.', 'the flat, impersonal tone fails to engage readers emotionally or address them directly',
     'Your gift could help a child like Mateo breathe on their own again.'),
    ('a blog post for young travellers', 'The aforementioned trek necessitates a moderate level of physical preparedness.', 'stiff, formal lexis clashes with the friendly, personal voice of a blog',
     'Fair warning: this trek is no stroll – get some hill walks in first.'),
    ('a formal report to a school board', 'Basically loads of kids hate the ban but some think it’s ok I guess.', 'vague, colloquial expression and hedging make the findings imprecise',
     'A majority of students surveyed oppose the ban, although a significant minority support it.'),
    ('an email to a close friend', 'Dear Sir or Madam, I am writing to inform you that I completed the marathon.', 'the formal salutation and phrasing are wrong for a friend',
     'Guess what – I actually finished the marathon! Legs are still in shock.'),
    ('a radio advertisement', 'The market is open on certain days and has various stalls selling items.', 'the vague, dull phrasing lacks the energy and specific detail of a radio advert',
     'Sizzling satay, live music, sixty stalls – Harbour Road Night Market, Thursday to Sunday!'),
    ('a feature article for older readers', 'The Rialto is, like, totally finished lol.', 'internet slang and ‘lol’ are unsuited to the reflective tone and older audience',
     'After ninety-two years, the Rialto’s lights will finally go out.'),
]


@t23.add('C1', (1, 2, 3))
def t23_tone(r, D):
    s, tone = r.choice(TONE_SNIP)
    opts, ans = mcq(r, cap(tone), [cap(x) for x in TONES if x != tone])
    return {'stem': f'Which word or phrase best describes the tone of this sentence? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(tone)}: shown by the lexis and sentence type.'}


@t23.add('C1', (1, 2, 3))
def t23_regfit(r, D):
    ctx, bad, why, good = r.choice(REG_ERR)
    others = [x[3] for x in REG_ERR if x[0] != ctx]
    opts, ans = mcq(r, good, [bad] + r.sample(others, 3), k=3)
    return {'stem': f'Which sentence is most appropriate for {ctx}?', 'options': opts, 'answer': ans,
            'key': f'{Q(good)} suits {ctx}; {Q(bad)} is inappropriate because {why}.'}


@t23.add('C2', (1, 2, 3, 4), 'explain')
def t23_err(r, D):
    ctx, bad, why, good = r.choice(REG_ERR)
    m = marks('C2', D)
    who = person(r)
    return {'stem': f'{who} writes this sentence in {ctx}: {Q(bad)} Explain why the register is inappropriate.', 'answer': cap(why) + '.',
            'key': f'{upto(m)}: 1 mark – identifies the register problem; 1 mark – refers to specific words; 1 mark – explains the mismatch with audience or form ({ctx}).', 'marks': m}


@t23.add('C3', (1, 2, 3, 4, 5), 'short')
def t23_rewrite(r, D):
    m = marks('C3', D)
    if r.random() < 0.5:
        ctx, bad, why, good = r.choice(REG_ERR)
        return {'stem': f'Rewrite this sentence so that its register suits {ctx}, and explain one change you made: {Q(bad)}', 'answer': f'Model: {good} The original was weak because {why}.',
                'key': pts_key(m, ['register now suits the context', 'meaning preserved', 'specific lexical changes', 'accurate expression', 'valid explanation of a change']), 'marks': m}
    f = r.choice(FEATS)
    aud, how = r.choice(NEW_AUD)
    return {'stem': f'In {f.ex.label}, the writer writes {Q(f.quote)}. Rewrite this for {aud}, and explain how your version changes the tone.',
            'answer': f'A version adapted for {aud} ({how}), with an explanation of the shift from the original’s {f.ex.register} tone.',
            'key': pts_key(m, [f'register suited to {aud}', 'meaning broadly kept', 'tone shift explained', 'accurate expression']), 'marks': m}


@t23.add('C4', (2, 3, 4, 5), 'long')
def t23_task(r, D):
    e = r.choice(EXTRACTS)
    return directed(r, D, e, emphasis=' Pay particular attention to creating a convincing voice and an appropriate register and tone throughout.')


CHAPTERS[2] = [t21, t22, t23]


# =========================================================== 3 Writer's style and analysis (Paper 1 Q1(b) and Q2)

def fw_templates(t, fws, label, snips=None, noun=''):
    noun = noun or ' and '.join(FWNAME[x] for x in fws)
    """C1 identify / C2 explain / C3 analyse / C4 long templates over extract features in the given frameworks."""
    fl = feats_of(fws=fws)

    @t.add('C1', (1, 2, 3))
    def fw_c1(r, D):
        return feat_mcq(r, r.choice(fl), frame=r.choice([f'Which {label} feature is used in {{q}} ({{src}})?', f'Read {{q}} from {{src}}. Which {label} term best describes it?']))

    @t.add('C2', (1, 2, 3, 4), 'explain')
    def fw_c2(r, D):
        f = r.choice(fl)
        m = marks('C2', D)
        stem = r.choice([f'Explain the effect of {Q(f.quote)} in {f.ex.label}. Refer to {noun} in your answer.',
                         f'In {short_label(f.ex)}, the writer uses {f.feature} in {Q(f.quote)}. Explain how this contributes to the text’s purpose.',
                         f'Comment on the {label} choices in {Q(f.quote)} ({short_label(f.ex)}) and their effect on the audience.'])
        return {'stem': stem, 'answer': f'{cap(f.feature)}: {f.effect}.', 'key': effect_key(m, f), 'marks': m}

    @t.add('C3', (2, 3, 4, 5), 'explain')
    def fw_c3(r, D):
        e = r.choice([x for x in EXTRACTS if any(f.fw in fws for f in x.feats)])
        mine = [f for f in e.feats if f.fw in fws]
        n = min(len(mine), 2 if D <= 3 else 3)
        m = marks('C3', D)
        return {'stem': f'{e.show()} Analyse how the writer uses {noun} in this text. Refer to {NUMW[n]} example{'s' if n > 1 else ''} and explain {'their effects' if n > 1 else 'its effect'}.',
                'answer': ' '.join(f'{Q(f.quote)} – {f.feature}: {f.effect}.' for f in mine[:n]),
                'key': pts_key(m, [f'{Q(f.quote)} ({f.feature}): {f.effect}' for f in mine], 'Up to 1 mark for each accurate identification and up to 2 for each developed explanation of effect.'), 'marks': m}

    @t.add('C4', (2, 3, 4, 5), 'long')
    def fw_c4(r, D):
        cand = [x for x in EXTRACTS if sum(f.fw in fws for f in x.feats) >= 2]
        if not cand:
            return None
        e = r.choice(cand)
        m = marks('C4', D, long=True)
        mine = [f for f in e.feats if f.fw in fws]
        task = r.choice([f'Analyse the ways in which {noun} and other language choices shape the meaning of this text.',
                         f'With close reference to {noun}, analyse how the writer creates a distinctive voice and engages the audience.'])
        ind = '; '.join(f'{Q(f.quote)} ({f.feature}): {f.effect}' for f in mine) + '; other relevant features: ' + '; '.join(f'{Q(f.quote)} ({f.feature})' for f in e.feats if f not in mine) + '.'
        return {'stem': f'{e.show()} {task}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'analysis', ind), 'type': 'long', 'marks': m}

    if snips:
        sets = snips

        @t.add('C1', (1, 2, 3))
        def sn_c1(r, D):
            pool, items, frame = r.choice(sets)
            s, lab, why = r.choice(items)
            opts, ans = mcq(r, cap(lab), [cap(x) for x in pool if x != lab])
            return {'stem': frame.format(q=Q(s)), 'options': opts, 'answer': ans, 'key': f'{cap(lab)}: {why}.'}

        @t.add('C2', (1, 2, 3, 4), 'explain')
        def sn_c2(r, D):
            pool, items, frame = r.choice(sets)
            s, lab, why = r.choice(items)
            m = marks('C2', D)
            ctx = r.choice(['a newspaper article', 'a short story', 'a political speech', 'a travel blog', 'a magazine feature', 'an advertisement'])
            return {'stem': f'This sentence comes from {ctx}: {Q(s)} Identify the {label} feature and explain its effect.', 'answer': f'{cap(lab)}: {why}.',
                    'key': f'{upto(m)}: 1 mark – identifies {lab}; 1 mark – explains the effect ({why}); 1 mark – links the effect to the likely purpose of {ctx}.', 'marks': m}


# ---------------------------------------------------------------- 3.1 lexis
N31 = 'Lexis and semantic fields; connotation and figurative language'
t31 = topic(N31, N31)
t31.fixed('C1', (1, 2), [
    ('What is a semantic field?', 'A group of words related by a shared area of meaning', 'E.g. attack, defence, battle = a semantic field of war.', ['A list of synonyms in a dictionary', 'The sound pattern of a line', 'The order of words in a sentence']),
    ('What does ‘connotation’ mean?', 'The associations and feelings a word carries beyond its literal meaning', 'Denotation = literal meaning; connotation = associations.',
     ['The dictionary definition of a word', 'The origin of a word', 'The number of syllables in a word']),
    ('Which word has the most negative connotation?', 'scrawny', '‘Slim’ and ‘slender’ are positive; ‘thin’ is neutral; ‘scrawny’ is negative.', ['slender', 'slim', 'thin']),
    ('What is the difference between a simile and a metaphor?', 'A simile compares using ‘like’ or ‘as’; a metaphor states that one thing is another', 'Both are figurative comparisons.',
     ['A simile is always longer', 'A metaphor uses ‘like’', 'There is no difference']),
    ('What is ‘lexis’?', 'The vocabulary of a language or text', 'Lexis = words and their choices; semantics = meaning.', ['The grammar of a sentence', 'The sound system of a language', 'The layout of a page']),
])
LEX_SETS = [
    (['war', 'religion', 'nature', 'medicine', 'machinery', 'theatre'], [
        ('The striker attacked again, launching a fresh assault on the battered defence.', 'war', '‘attacked’, ‘assault’ and ‘battered defence’ present football as combat'),
        ('The market is a pilgrimage for food lovers, a temple to the humble dumpling.', 'religion', '‘pilgrimage’ and ‘temple’ elevate food to something sacred'),
        ('The city’s lungs are clogged and its arteries choked with traffic.', 'medicine', '‘lungs’, ‘clogged’ and ‘arteries’ present the city as a sick body'),
        ('The new manager oiled the team’s gears until every part ran smoothly.', 'machinery', '‘oiled’, ‘gears’ and ‘ran smoothly’ present the team as an efficient machine'),
        ('As the curtain fell on her career, she took one last bow before her loyal audience.', 'theatre', '‘curtain fell’, ‘bow’ and ‘audience’ present a career as a performance'),
        ('Ideas blossomed in the classroom, rooted in curiosity and watered by patience.', 'nature', '‘blossomed’, ‘rooted’ and ‘watered’ present learning as growth'),
        ('The election campaign became a siege, each party digging in behind its trenches.', 'war', '‘siege’, ‘digging in’ and ‘trenches’ present politics as warfare'),
        ('The surgeon of the budget cut deep, removing the infected parts of the plan.', 'medicine', '‘surgeon’, ‘cut’ and ‘infected’ present budget cuts as an operation'),
    ], 'Which semantic field dominates this sentence? {q}'),
    (['positive connotation', 'negative connotation', 'neutral', 'mixed (both positive and negative)'], [
        ('The minister’s statement was a calculated evasion.', 'negative connotation', '‘calculated evasion’ implies deliberate dishonesty'),
        ('Their cosy flat overlooks the harbour.', 'positive connotation', '‘cosy’ suggests warmth and comfort rather than small size'),
        ('The building has three floors.', 'neutral', 'the sentence is factual with no evaluative lexis'),
        ('The protesters swarmed into the square.', 'negative connotation', '‘swarmed’ likens people to insects, suggesting threat'),
        ('Her thrifty habits saved the family business.', 'positive connotation', '‘thrifty’ presents carefulness with money as a virtue'),
        ('The cramped flat overlooks the harbour.', 'negative connotation', '‘cramped’ presents the small space as uncomfortable'),
        ('The meeting will begin at 9 a.m.', 'neutral', 'a factual statement without evaluation'),
        ('Crowds of well-wishers gathered outside the hospital.', 'positive connotation', '‘well-wishers’ presents the crowd as supportive'),
    ], 'Which best describes the connotations of the language in this sentence? {q}'),
]
fw_templates(t31, ['lexis'], 'lexical and semantic', snips=LEX_SETS)


# ---------------------------------------------------------------- 3.2 grammar and syntax
N32 = 'Grammar and syntax: sentence types, modality, tense and voice'
t32 = topic(N32, N32)
t32.fixed('C1', (1, 2), [
    ('Which modal verb expresses the strongest obligation?', 'must', 'Deontic modality: must > should > could/might.', ['might', 'could', 'may']),
    ('What is epistemic modality?', 'Modality that expresses how certain or possible something is', 'E.g. ‘It might rain’; deontic modality expresses obligation or permission.',
     ['Modality that gives commands', 'The use of the past tense', 'The omission of the subject']),
    ('In ‘The window was broken’, what is the effect of the agentless passive?', 'It hides or downplays who broke the window', 'Agentless passives remove responsibility or focus on the action.',
     ['It makes the sentence a question', 'It shows the action is in the future', 'It names the person responsible']),
    ('What is a complex sentence?', 'A sentence with a main clause and at least one subordinate clause', 'E.g. ‘Although it rained, we played.’', ['A sentence with two main clauses joined by ‘and’', 'A sentence with no verb', 'Any long sentence']),
    ('Which sentence function does ‘Close the door.’ have?', 'Imperative', 'Imperatives give commands.', ['Declarative', 'Interrogative', 'Exclamative']),
])
GRAM_SETS = [
    (['declarative', 'interrogative', 'imperative', 'exclamative'], [
        ('Sign the petition before Friday.', 'imperative', 'the sentence commands the reader to act'), ('How much longer can we ignore the evidence?', 'interrogative', 'it is a question, here rhetorical'),
        ('The museum reopens next week.', 'declarative', 'it makes a statement'), ('What a disaster that turned out to be!', 'exclamative', 'it expresses strong feeling with ‘what a …!’'),
        ('Book early to avoid disappointment.', 'imperative', 'a command addressed to the reader'), ('Why should young people care about pensions?', 'interrogative', 'a question opening an argument'),
        ('How beautiful the valley looks at dawn!', 'exclamative', 'an exclamation of admiration'), ('Most visitors arrive by train.', 'declarative', 'a statement of fact'),
    ], 'What is the function of this sentence? {q}'),
    (['simple', 'compound', 'complex', 'minor'], [
        ('The door opened.', 'simple', 'one main clause'), ('The rain stopped and the crowd returned.', 'compound', 'two main clauses joined by a coordinating conjunction'),
        ('When the rain stopped, the crowd returned.', 'complex', 'a subordinate clause (‘When the rain stopped’) plus a main clause'), ('Silence.', 'minor', 'no main verb'),
        ('Although the tickets were expensive, every seat was sold.', 'complex', 'a subordinate concessive clause plus a main clause'), ('She ran, but the bus left.', 'compound', 'two main clauses joined by ‘but’'),
        ('Not again.', 'minor', 'a verbless fragment'), ('The old projectionist climbed the stairs.', 'simple', 'one main clause with an expanded noun phrase'),
    ], 'What type of sentence structure is this? {q}'),
    (['deontic modality', 'epistemic modality', 'no modality', 'dynamic modality (ability)'], [
        ('Visitors must wear a helmet.', 'deontic modality', '‘must’ expresses obligation'), ('The storm could reach the coast by midnight.', 'epistemic modality', '‘could’ expresses possibility'),
        ('Schools should ban phones.', 'deontic modality', '‘should’ expresses a recommendation or duty'), ('The results may surprise you.', 'epistemic modality', '‘may’ expresses possibility'),
        ('The bridge closes at noon.', 'no modality', 'the verb is unmodalised, presenting a fact'), ('You must not feed the animals.', 'deontic modality', '‘must not’ expresses prohibition'),
        ('It might be the last time we see the Rialto open.', 'epistemic modality', '‘might’ expresses uncertainty'), ('The festival attracts thousands of visitors.', 'no modality', 'an unmodalised statement'),
    ], 'Which type of modality, if any, does this sentence show? {q}'),
    (['active voice', 'passive voice with agent', 'agentless passive', 'imperative mood'], [
        ('Mistakes were made.', 'agentless passive', 'the agent is omitted, avoiding blame'), ('The council approved the plan.', 'active voice', 'the agent (council) is the subject'),
        ('The plan was approved by the council.', 'passive voice with agent', 'the agent appears in a ‘by’ phrase'), ('Fines will be issued.', 'agentless passive', 'no agent is named, creating impersonal authority'),
        ('Pigeons demolished our tomatoes.', 'active voice', 'the agent is the subject'), ('Our tomatoes were demolished by pigeons.', 'passive voice with agent', 'the agent is delayed to the end for comic effect'),
        ('The reservoir was drained last spring.', 'agentless passive', 'the agent is unnamed'), ('Volunteers built the garden.', 'active voice', 'the agent leads the sentence'),
    ], 'Which best describes the voice of this sentence? {q}'),
]
fw_templates(t32, ['grammar'], 'grammatical and syntactic', snips=GRAM_SETS)


@t32.add('C3', (1, 2, 3, 4), 'short')
def t32_transform(r, D):
    pool, items, frame = GRAM_SETS[3]
    acts = [('The council approved the plan.', 'The plan was approved (by the council).'), ('Pigeons demolished our tomatoes.', 'Our tomatoes were demolished by pigeons.'),
            ('Volunteers built the garden.', 'The garden was built (by volunteers).'), ('The company raised its prices.', 'Prices were raised (by the company).'),
            ('The authority closed the reservoir.', 'The reservoir was closed (by the authority).'), ('Someone broke the window.', 'The window was broken.')]
    s, p = r.choice(acts)
    m = marks('C3', D)
    use = r.choice(['a news report that wants to sound impersonal', 'a statement by an organisation that wishes to avoid blame', 'a scientific report'])
    return {'stem': f'Rewrite {Q(s)} in the passive voice, and explain why a writer of {use} might prefer the passive form.',
            'answer': f'{p} The passive shifts focus to the action or the thing affected and allows the agent to be omitted, which suits {use}.',
            'key': pts_key(m, ['correct passive form', 'agent optional or omitted correctly', 'explains change of focus', f'links to the purpose of {use}']), 'marks': m}


# ---------------------------------------------------------------- 3.3 discourse, cohesion and perspective
N33 = 'Discourse structure, cohesion and narrative perspective'
t33 = topic(N33, N33)
t33.fixed('C1', (1, 2), [
    ('What is anaphoric reference?', 'A word that refers back to something mentioned earlier', 'E.g. ‘Mr Farouk climbs the stairs. He …’ – ‘he’ refers back.', ['A word that refers forward', 'A repeated sound', 'A question to the reader']),
    ('What is cataphoric reference?', 'A word that refers forward to something mentioned later', 'E.g. ‘It was huge: the wave …’ – ‘it’ points forward.', ['A word that refers back', 'A sentence without a verb', 'A list of three']),
    ('What is free indirect discourse?', 'Third-person narration that takes on the thoughts and voice of a character', 'It blends narrator and character voice without quotation marks.',
     ['Speech in quotation marks', 'A first-person diary', 'Stage directions']),
    ('Which is an example of lexical cohesion?', 'Using related words such as ‘reservoir’, ‘water’ and ‘pipes’ across a text', 'Lexical cohesion links a text through repeated or related words.',
     ['Using a full stop', 'Starting a new paragraph', 'Writing in the passive voice']),
])
DIS_SETS = [
    (['anaphoric reference', 'cataphoric reference', 'substitution', 'ellipsis', 'lexical cohesion', 'conjunction'], [
        ('The guide stopped. He pointed at the ridge.', 'anaphoric reference', '‘He’ refers back to ‘the guide’'),
        ('It rose out of the mist, enormous and silent: the monastery.', 'cataphoric reference', '‘It’ points forward to ‘the monastery’, creating suspense'),
        ('I wanted a ticket but there weren’t any left.', 'substitution', '‘any’ substitutes for ‘tickets’'),
        ('Some volunteers came on Saturday; others on Sunday.', 'ellipsis', 'the verb ‘came’ is omitted from the second clause'),
        ('The heat was relentless. Temperatures soared; the reservoirs shrank.', 'lexical cohesion', '‘heat’, ‘temperatures’ and ‘reservoirs’ create a chain of related words'),
        ('The plan is cheap. However, it may not work.', 'conjunction', '‘However’ links the sentences by signalling contrast'),
        ('This is what worries me: nobody has checked the pipes.', 'cataphoric reference', '‘This’ points forward to the explanation'),
        ('Mr Farouk loves the Rialto. It has been his life.', 'anaphoric reference', '‘It’ refers back to ‘the Rialto’'),
    ], 'Which cohesive device is shown here? {q}'),
    (['first-person narration', 'second-person narration', 'third-person limited narration', 'third-person omniscient narration', 'free indirect discourse'], [
        ('I remember the smell of the cinema more than any film.', 'first-person narration', 'the narrator is a participant using ‘I’'),
        ('You step off the bus and the heat hits you like a wall.', 'second-person narration', '‘you’ places the reader inside the experience'),
        ('Pema watched the tourists struggle, wondering whether any of them would make it.', 'third-person limited narration', 'the narration stays close to one character’s thoughts'),
        ('Every villager slept soundly, unaware that the river, miles upstream, had already begun to rise.', 'third-person omniscient narration', 'the narrator knows more than any character'),
        ('She looked at the queue. Twenty minutes? For dumplings? Well, why not.', 'free indirect discourse', 'the character’s thoughts appear in the narrative voice without quotation marks'),
        ('We had walked for six hours before anyone spoke.', 'first-person narration', 'a first-person plural participant narrator'),
        ('He knew the cinema would close; what he did not know was that his daughter had bought it.', 'third-person omniscient narration', 'the narrator reveals information hidden from the character'),
        ('Kenji glanced at the clock. Ten more minutes. Surely she would call.', 'free indirect discourse', 'Kenji’s thoughts merge with the narration'),
    ], 'Which narrative perspective is used here? {q}'),
]
fw_templates(t33, ['discourse'], 'discourse and structural', snips=DIS_SETS)


@t33.add('C3', (2, 3, 4, 5), 'explain')
def t33_structure(r, D):
    e = r.choice([x for x in EXTRACTS if not x.spoken])
    m = marks('C3', D)
    first = e.body().split('. ')[0]
    last = e.body().rstrip('.').split('. ')[-1]
    return {'stem': f'{e.show()} Analyse how the text is structured. Comment on the opening ({Q(first)}), the development and the ending ({Q(last)}).',
            'answer': f'The opening establishes the {e.tname} and engages {e.audience}; the middle develops content (' + '; '.join(e.points[:2]) + '); the ending is shaped to the purpose: ' + e.purpose + '.',
            'key': pts_key(m, ['effect of the opening', 'how the middle develops or sequences ideas', 'effect of the ending', 'cohesive links or shifts in focus', 'link of structure to purpose']), 'marks': m}


# ---------------------------------------------------------------- 3.4 phonology and prosody
N34 = 'Phonology and prosodic features in spoken and literary texts'
t34 = topic(N34, N34)
t34.fixed('C1', (1, 2), [
    ('What are prosodic features?', 'Features of speech such as stress, intonation, pitch, pace and volume', 'Prosody = the ‘music’ of speech beyond the words.', ['Spelling patterns', 'The use of metaphors', 'Paragraph structure']),
    ('Which sounds are plosives?', '/p/, /b/, /t/, /d/, /k/, /g/', 'Plosives are made by stopping and releasing air.', ['/s/ and /ʃ/', '/m/ and /n/', '/a/ and /o/']),
    ('Rising intonation at the end of an utterance most often signals …', 'a question or an invitation for the listener to respond', 'Falling intonation usually signals completion.',
     ['the end of the conversation', 'anger', 'a quotation']),
    ('What is sibilance?', 'Repetition of /s/ and /ʃ/ sounds', 'Sibilance can suggest softness, secrecy or hissing.', ['Repetition of vowel sounds', 'A silent letter', 'A long pause']),
])
PHON_SETS = [
    (['alliteration', 'sibilance', 'assonance', 'plosive sounds', 'onomatopoeia', 'rhythm'], [
        ('Big, bold and bursting with flavour.', 'plosive sounds', 'the hard /b/ sounds give energy and force'), ('the soft sea sighing on the shingle', 'sibilance', 'the /s/ and /ʃ/ sounds mimic the hushing waves'),
        ('the low moan of the slow road home', 'assonance', 'the long /əʊ/ vowels slow the line and create a mournful tone'), ('the kettle hissed and the toast popped', 'onomatopoeia', '‘hissed’ and ‘popped’ imitate the sounds'),
        ('Clean, clear, cold water for every child', 'alliteration', 'the repeated /k/ sound makes the slogan memorable'), ('We will rise, we will rebuild, we will return', 'rhythm', 'the regular, repeated pattern creates a marching beat'),
        ('Fresh fish, fried fast', 'alliteration', 'the /f/ sounds make the advert catchy'), ('the thud and clatter of the closing gates', 'onomatopoeia', '‘thud’ and ‘clatter’ imitate the noise'),
    ], 'Which sound feature is most prominent here? {q}'),
    (['rising intonation', 'falling intonation', 'prosodic stress', 'increased volume', 'slower pace', 'raised pitch'], [
        ('A: you’re coming tomorrow ↗', 'rising intonation', 'the rise turns a statement into a question'), ('A: that’s the end of it ↘', 'falling intonation', 'the fall signals finality'),
        ('A: I said the RED one', 'prosodic stress', 'the stress corrects a misunderstanding'), ('A: GET OUT OF THE ROAD', 'increased volume', 'capitals show shouting, here urgency'),
        ('A: and <slowly> nobody (.) said (.) a word', 'slower pace', 'slowing down builds tension and emphasis'), ('A: [high pitch] oh he’s so cute', 'raised pitch', 'high pitch signals excitement or child-directed talk'),
        ('A: is that your final answer ↗', 'rising intonation', 'the rise invites a response'), ('A: I did NOT take it', 'prosodic stress', 'stress on ‘NOT’ insists on denial'),
    ], 'Which prosodic feature is shown in this transcript line (↗ = rising, ↘ = falling, CAPITALS = stress or loudness)? {q}'),
]
L1 = Ex('poem', None, None, 'poem', 'a poem, ‘Harbour, Dawn’', """
The slow boats slide on silver water, / the gulls cry, cut and cry again; / a rope slaps, sharp, against a mast, / and from the market,
low and long, / the first bell rolls along the quay.""", 'readers of poetry', 'to evoke the atmosphere of a harbour at dawn', 'a short lyric poem', 'literary and lyrical')
L1.f('The slow boats slide on silver water', 'sibilance', 'phonology', 'the soft /s/ sounds create a hushed, gliding movement that matches the calm water', also=('alliteration',))
L1.f('cry, cut and cry again', 'plosive sounds', 'phonology', 'the hard /k/ sounds are harsh and abrupt, imitating the gulls’ sharp calls', also=('alliteration', 'repetition'))
L1.f('a rope slaps, sharp, against a mast', 'onomatopoeia', 'phonology', '‘slaps’ imitates the sudden sound, and the commas break the rhythm like the jolt of the rope', also=('sibilance',))
L1.f('low and long, / the first bell rolls', 'assonance', 'phonology', 'the long /əʊ/ vowels slow the line, echoing the deep, lingering bell', also=('alliteration',))
L2 = Ex('storm', None, None, 'descriptive prose', 'an extract from a descriptive piece, ‘The Storm’', """
Then the storm broke. Thunder boomed and bellowed over the bay, rain battered the tin roofs like thrown gravel, and the wind whistled,
whined and wailed through every crack in the shutters. And then, just as suddenly, silence: the soft sigh of the sea settling back
to sleep.""", 'general readers', 'to describe a storm vividly', 'a descriptive composition', 'literary and dramatic')
L2.f('Thunder boomed and bellowed over the bay', 'plosive sounds', 'phonology', 'the repeated /b/ sounds are loud and forceful, recreating the thunder', also=('alliteration', 'onomatopoeia'))
L2.f('whistled, whined and wailed', 'alliteration', 'phonology', 'the /w/ sounds and onomatopoeic verbs mimic the rising, moaning wind', also=('onomatopoeia', 'tricolon'))
L2.f('the soft sigh of the sea settling back to sleep', 'sibilance', 'phonology', 'the hushed /s/ sounds contrast with the earlier plosives, creating calm after the storm', also=('alliteration', 'personification'))
L2.f('Then the storm broke.', 'rhythm', 'phonology', 'the short, heavily stressed sentence gives an abrupt beat that marks the moment the storm begins', also=('declarative',))
L3 = Ex('rally', None, None, 'transcript of a campaign speech', 'a transcript of part of a campaign speech (↗ = rising intonation; ↘ = falling intonation)', """
we will build (.) we will BUILD (.) homes that people can afford ↘ (2) and if they tell you it can't be done ↗ (.) ask them (.) who
DID it last time ↘ [applause]""", 'supporters at a rally', 'to persuade and rouse supporters', 'a live political speech', 'rousing and combative')
L3.f('we will build (.) we will BUILD', 'prosodic stress', 'phonology', 'the repetition with stress on the second ‘BUILD’ intensifies the promise and invites applause', also=('repetition',))
L3.f('homes that people can afford ↘', 'falling intonation', 'phonology', 'the fall signals certainty and closes the promise firmly')
L3.f("it can't be done ↗", 'rising intonation', 'phonology', 'the rise leaves the opponents’ claim hanging, as if questioning it, before the retort')
L3.f('who DID it last time', 'prosodic stress', 'phonology', 'stress on ‘DID’ pointedly contrasts the speaker’s record with opponents’ doubts', also=('rhetorical question',))
for _x in (L1, L2, L3):
    Ex.ALL.remove(_x)
    _x.tname, _x.pp, _x.pp_also = _x.kind, _x.purpose, ()
SOUNDTEXTS = [L1, L2, L3]
FEATS_PHON = [f for x in SOUNDTEXTS for f in x.feats]
fw_templates(t34, ['phonology'], 'phonological and prosodic', snips=PHON_SETS)


@t34.add('C1', (1, 2, 3))
def t34_lit_c1(r, D):
    return feat_mcq(r, r.choice(FEATS_PHON), frame='In {src}, which sound feature is most prominent in {q}?')


@t34.add('C2', (1, 2, 3, 4), 'explain')
def t34_lit_c2(r, D):
    f = r.choice(FEATS_PHON)
    m = marks('C2', D)
    return {'stem': f'Explain how sound is used for effect in {Q(f.quote)} from {f.ex.label}.', 'answer': f'{cap(f.feature)}: {f.effect}.', 'key': effect_key(m, f), 'marks': m}


@t34.add('C4', (2, 3, 4, 5), 'long')
def t34_long(r, D):
    x = r.choice(SOUNDTEXTS)
    m = marks('C4', D, long=True)
    task = r.choice(['Analyse how phonological and prosodic features contribute to the meaning and effect of this text.',
                     'Analyse how the writer or speaker uses sound to create atmosphere or emphasis, referring also to other language features.'])
    ind = '; '.join(f'{Q(f.quote)} ({f.feature}): {f.effect}' for f in x.feats) + f'; purpose: {x.purpose}.'
    return {'stem': f'Read {x.label}: {Q(x.text)} {task}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'analysis', ind), 'type': 'long', 'marks': m}


@t34.add('C3', (2, 3, 4, 5), 'explain')
def t34_sound(r, D):
    pool, items, frame = PHON_SETS[0]
    picks = r.sample(items, 2 if D <= 3 else 3)
    m = marks('C3', D)
    ctx = r.choice(['a poem about the sea', 'a radio advertisement', 'a political slogan', 'the opening of a short story'])
    return {'stem': f'These phrases come from {ctx}: ' + ' '.join(f'({i + 1}) {Q(s)}' for i, (s, _, _) in enumerate(picks)) + ' Identify the sound feature in each and analyse its effect.',
            'answer': ' '.join(f'({i + 1}) {cap(l)}: {w}.' for i, (_, l, w) in enumerate(picks)),
            'key': pts_key(m, [f'({i + 1}) {l}: {w}' for i, (_, l, w) in enumerate(picks)], '1 mark for each feature and 1 for each explained effect.'), 'marks': m}


# ---------------------------------------------------------------- 3.5 writing a style analysis
N35 = 'Writing a style analysis using the language frameworks'
t35 = topic(N35, N35)
t35.fixed('C1', (1, 2), [
    ('In a style analysis, what is ‘feature-spotting’?', 'Naming techniques without explaining their effects in context', 'Feature-spotting gains little credit; effects must be analysed.',
     ['Finding the most important features', 'Quoting precisely', 'Using several frameworks']),
    ('Which is the strongest way to use evidence in a style analysis?', 'Embed short, precise quotations and analyse particular words', 'Brief embedded quotations allow close analysis.',
     ['Copy out whole paragraphs', 'Paraphrase without quoting', 'Quote only the first line']),
    ('Which framework is concerned with how texts are organised and how parts link together?', 'Discourse', 'Discourse = structure and cohesion across a text.', ['Phonology', 'Lexis', 'Graphology']),
    ('What should the opening of a style analysis usually do?', 'Establish the text’s genre, audience, purpose and context in an overview', 'An overview frames the analysis that follows.',
     ['Retell the story of the text', 'List every feature found', 'Give a personal opinion of the topic']),
])
COMMENTS = [
    ('The writer’s use of the agentless passive ‘will be banned’ gives the restriction impersonal authority.', 'grammar and syntax'),
    ('The semantic field of warfare (‘battle’, ‘lose’) makes finding a seat sound comically dangerous.', 'lexis and semantics'),
    ('The text moves from a personal anecdote to a direct appeal, guiding the reader from sympathy to action.', 'discourse and structure'),
    ('The sibilance in ‘sizzling satay’ imitates the sound of cooking.', 'phonology and prosody'),
    ('The banner photograph and the BOOK NOW button work together to turn desire into a sale.', 'graphology and visual design'),
    ('The presenter’s laugh implies scepticism without openly criticising the authority.', 'pragmatics'),
    ('The deontic modal ‘must’ makes the rule non-negotiable.', 'grammar and syntax'),
    ('Positive evaluative adjectives such as ‘gloriously’ reveal the reviewer’s affection.', 'lexis and semantics'),
    ('The ending returns to the title’s wordplay, giving the editorial a cyclical shape.', 'discourse and structure'),
    ('Stress on ‘MONTHS’ conveys the caller’s exasperation.', 'phonology and prosody'),
    ('The tick list allows readers to scan the benefits at a glance.', 'graphology and visual design'),
    ('By saying ‘you’re on the fence’, the blogger implies that doubt is natural and easily overcome.', 'pragmatics'),
]
WEAK = [
    ('The writer uses a metaphor, which makes the reader want to read on.', 'a generic effect that could apply to any text; the metaphor is not quoted or analysed',
     'The metaphor ‘a field waiting to be planted’ reframes bare concrete as fertile land, so the audience begins to see the roofs as potential rather than waste.'),
    ('There is a rhetorical question and some emotive language and a statistic.', 'feature-spotting: a list of techniques with no quotation or effect',
     'The rhetorical question ‘The difference?’ creates a pause that sets up the ventilator as the answer, turning the reader’s sympathy into a sense that money can solve the problem.'),
    ('The text is about a cinema that is closing and the man is sad.', 'paraphrase of content with no analysis of language',
     'The simile ‘the seats creak like old ships’ presents the cinema’s decline as dignified and romantic, encouraging nostalgia.'),
    ('The writer uses lots of words to describe the market.', 'vague and inaccurate terminology; no specific words are examined',
     'The tricolon ‘loud, cramped and gloriously chaotic’ turns negative adjectives into praise through the adverb ‘gloriously’.'),
    ('The speaker says erm, which shows he is stupid.', 'an unjustified judgement; fillers are normal in spontaneous speech',
     'The filler ‘erm’ shows the caller planning in real time and perhaps nervousness at speaking on air.'),
    ('The leaflet uses short sentences to make it short.', 'a circular explanation that says nothing about effect on the audience',
     'The short imperative ‘Wear a helmet.’ gives an unambiguous instruction, which suits the leaflet’s purpose of keeping riders safe.'),
]


@t35.add('C1', (1, 2, 3))
def t35_fw(r, D):
    c, fw = r.choice(COMMENTS)
    opts, ans = mcq(r, cap(fw), [cap(x) for x in FWNAME.values() if x != fw])
    return {'stem': f'A student writes: {Q(c)} Which language framework is the student mainly using?', 'options': opts, 'answer': ans, 'key': f'{cap(fw)}.'}


@t35.add('C2', (1, 2, 3, 4), 'explain')
def t35_weak(r, D):
    s, why, better = r.choice(WEAK)
    m = marks('C2', D)
    who = person(r)
    return {'stem': f'{who} writes this sentence in a style analysis: {Q(s)} Explain why it would gain little credit and suggest how it could be improved.',
            'answer': f'{cap(why)}. Improved: {better}', 'key': f'{upto(m)}: 1 mark – identifies the weakness ({why}); 1 mark – explains what analysis requires (precise quotation, effect in context); 1 mark – a valid improved version.', 'marks': m}


@t35.add('C3', (1, 2, 3, 4, 5), 'explain')
def t35_para(r, D):
    f = r.choice(FEATS)
    m = marks('C3', D)
    return {'stem': f'Write an analytical paragraph on {Q(f.quote)} from {f.ex.label}. Identify the feature, embed the quotation and analyse its effect in relation to the audience ({f.ex.audience}) and purpose.',
            'answer': f'Model: The writer’s use of {f.feature} in {Q(f.quote)} … {f.effect}, which suits a text written {f.ex.purpose}.',
            'key': pts_key(m, [f'accurate identification ({f.feature})', 'embedded quotation', f'analysis of effect: {f.effect}', 'link to audience or purpose', 'precise terminology and fluent expression']), 'marks': m}


@t35.add('C4', (2, 3, 4, 5), 'long')
def t35_long(r, D):
    e = r.choice(EXTRACTS)
    m = marks('C4', D, long=True)
    ctx = f'This text is {short_label(e)}, {e.context}.'
    task = r.choice(['Analyse the ways in which language and style are used in this text.', 'Analyse how the writer uses language, form and structure to achieve the purpose of this text.',
                     'Using the language frameworks, write a style analysis of this text.'])
    ind = f'overview of genre, audience ({e.audience}), purpose and context; ' + '; '.join(f'{Q(f.quote)} – {f.feature} ({FWNAME[f.fw]}): {f.effect}' for f in e.feats) + '.'
    return {'stem': f'{ctx} {e.show()} {task}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'analysis', ind), 'type': 'long', 'marks': m}


CHAPTERS[3] = [t31, t32, t33, t34, t35]


# =========================================================== 4 Writing: shorter writing tasks (Paper 2 Section A)

SW_TOPICS = ['a plan to make the town centre car-free', 'a proposal to start the school day an hour later', 'volunteering abroad during a gap year', 'a new community library',
             'learning a musical instrument as a teenager', 'the closure of a local swimming pool', 'a scheme to plant trees along every street', 'free public transport for students',
             'a ban on single-use plastics at a music festival', 'a youth-led recycling project', 'a new skate park', 'the rise of online learning', 'a weekly car-free Sunday',
             'turning an empty shop into a youth centre']
SW_AUDS = ['students at your school', 'local residents', 'parents of secondary-school students', 'members of a youth club', 'older people in your community']
SW_RECIP = ['the editor of a local newspaper', 'the head of your school', 'your local mayor', 'the manager of a local company']
SW_PUBS = ['a national newspaper’s weekend supplement', 'a teenage lifestyle magazine', 'your school magazine', 'a community website']
SW_REVIEW = ['a restaurant that has just opened near your home', 'a film you have recently seen', 'a museum you have visited', 'a mobile app you use every day', 'a concert you attended',
             'a book you have recently read', 'a theme park you visited', 'a video game you have played']
SW_FORMS = {
    'leaflet': lambda r, t: (f'a leaflet for {r.choice(SW_AUDS)} giving information and advice about {t}', 'leaflet'),
    'speech': lambda r, t: (f'the text of a speech to {r.choice(SW_AUDS)} persuading them to support {t}', 'speech'),
    'letter': lambda r, t: (f'a letter to {r.choice(SW_RECIP)} giving your views on {t}', 'letter'),
    'article': lambda r, t: (f'an article for {r.choice(SW_PUBS)} exploring {t}', 'article'),
    'blog': lambda r, t: (f'a blog post for {r.choice(SW_AUDS)} describing your own experience of {t}', 'blog'),
    'review': lambda r, t: (f'a review of {r.choice(SW_REVIEW)} for {r.choice(SW_PUBS)}', 'review'),
}
TCONV['review'] = ['an evaluative verdict or rating', 'balanced praise and criticism of specific features', 'comment on value for money and a recommendation']
SW_W = {1: '250–300', 2: '300–350', 3: '300–400', 4: '300–400', 5: '300–400'}


def sw_task(r, forms=None):
    k = r.choice(forms or list(SW_FORMS))
    desc, ck = SW_FORMS[k](r, r.choice(SW_TOPICS))
    return desc, ck


def sw_long(r, D, extra='', forms=None):
    desc, ck = sw_task(r, forms)
    m = marks('C4', D, long=True)
    ind = f'conventions of the form: {"; ".join(TCONV[ck])}; a clear sense of audience and purpose; deliberate choices of voice, structure and language; accuracy.'
    return {'stem': f'Write {desc} ({SW_W[D]} words).{extra}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'writing', ind), 'type': 'long', 'marks': m}


# ---------------------------------------------------------------- 4.1 writing short texts for an audience
N41 = 'Writing short texts for a specified audience: leaflets, reviews, speeches, letters'
t41 = topic(N41, N41)
t41.fixed('C1', (1, 2), [
    ('A formal letter that begins ‘Dear Sir or Madam’ should normally end with …', 'Yours faithfully', '‘Yours faithfully’ when the recipient is not named; ‘Yours sincerely’ when they are.', ['Yours sincerely', 'Cheers', 'Best wishes, xx']),
    ('Which feature is most important in a leaflet that gives advice?', 'Clear headings and concise, scannable sections', 'Leaflets are skimmed; layout aids navigation.', ['Long, complex paragraphs', 'A star rating', 'A transcription key']),
    ('Which of these is most typical of a speech rather than an article?', 'Direct address and signposting for a listening audience', 'Listeners cannot reread, so speeches signpost and address the audience.',
     ['A headline and standfirst', 'Footnotes', 'Bullet points']),
    ('In a review, what is the function of balanced criticism?', 'It makes the reviewer’s verdict more credible', 'Readers trust a reviewer who weighs strengths and weaknesses.', ['It makes the review longer', 'It avoids giving a verdict', 'It replaces the rating']),
])


@t41.add('C1', (1, 2, 3))
def t41_conv(r, D):
    desc, ck = sw_task(r)
    good = r.choice(TCONV[ck])
    others = [c for kk, cs in TCONV.items() if kk != ck and not ({kk, ck} <= {'report', 'formal report'}) and not ({kk, ck} <= {'diary', 'email', 'blog'}) and not ({kk, ck} <= {'article', 'blog'}) for c in cs]
    opts, ans = mcq(r, cap(good), [cap(c) for c in r.sample(others, 6)])
    return {'stem': f'You are asked to write {desc}. Which feature would be most appropriate to include?', 'options': opts, 'answer': ans, 'key': f'{cap(good)} is a convention of this form.'}


@t41.add('C2', (1, 2, 3, 4), 'explain')
def t41_why(r, D):
    desc, ck = sw_task(r)
    c = r.choice(TCONV[ck])
    m = marks('C2', D)
    return {'stem': f'A student is writing {desc}. Explain why {c} would help the text succeed.',
            'answer': f'{cap(c)} meets the audience’s expectations of the form and supports its purpose.',
            'key': f'{upto(m)}: 1 mark – what the feature does; 1 mark – link to the audience; 1 mark – link to the purpose or form, with an example.', 'marks': m}


@t41.add('C3', (1, 2, 3, 4, 5), 'multi_step')
def t41_plan(r, D):
    desc, ck = sw_task(r)
    parts = [
        lambda r: ('Identify the audience and purpose of the task.', 'Audience and purpose as stated in the task.', '1 mark audience; 1 mark purpose [2]'),
        lambda r: ('List three conventions of the form you will use.', '; '.join(cap(c) for c in TCONV[ck]), '1 mark each [3]'),
        lambda r: ('Describe the register and tone you will adopt, with a reason.', 'A register suited to the audience, e.g. semi-formal and engaging.', '1 mark register; 1 mark reason [2]'),
        lambda r: ('Write the first two sentences of your text.', 'An opening in the correct form that engages the audience.', '1 mark form; 1 mark engagement; 1 mark accuracy [3]'),
        lambda r: ('Outline the structure of your text in three stages.', 'A logical three-part structure (opening, development, ending) suited to the form.', '1 mark each stage [3]'),
    ]
    return compose(r, f'You are asked to write {desc}.', parts, k=(2, 3), type_='multi_step')


@t41.add('C4', (2, 3, 4, 5), 'long')
def t41_task(r, D):
    return sw_long(r, D)


# ---------------------------------------------------------------- 4.2 openings, voice and stylistic choices
N42 = 'Crafting openings, voice and stylistic choices in short texts'
t42 = topic(N42, N42)
OPEN_POOL = ['rhetorical question', 'anecdote', 'startling statistic', 'direct address', 'in medias res', 'vivid description', 'provocative statement', 'dialogue']
OPENINGS = [
    ('How many of us could survive a week without a phone?', 'rhetorical question'), ('Last spring my grandmother handed me a seed packet and a trowel, and my summer changed.', 'anecdote'),
    ('Every minute, a lorry-load of plastic enters the ocean.', 'startling statistic'), ('You have walked past it a hundred times without noticing.', 'direct address'),
    ('The engine coughed, the boat lurched, and suddenly we were drifting.', 'in medias res'), ('Grey water slaps against the harbour wall under a sky the colour of pewter.', 'vivid description'),
    ('Homework is a waste of everyone’s time.', 'provocative statement'), ('“You’re not seriously wearing that,” said my brother.', 'dialogue'),
    ('Ninety per cent of the town’s shops have closed in a decade.', 'startling statistic'), ('Why do we still sit in rows to learn?', 'rhetorical question'),
    ('Imagine opening your front door to silence – no cars, no horns, just birdsong.', 'direct address'), ('Libraries are not dying; they are being killed.', 'provocative statement'),
]
OPEN_PHRASE = {'rhetorical question': 'a rhetorical question', 'anecdote': 'an anecdote', 'startling statistic': 'a startling statistic', 'direct address': 'direct address to the reader',
               'in medias res': 'an opening in medias res (in the middle of the action)', 'vivid description': 'a vivid description', 'provocative statement': 'a provocative statement', 'dialogue': 'a line of dialogue'}
WEAK_OPEN = [
    ('In this speech I am going to talk about the skate park.', 'it announces the topic flatly instead of engaging the audience', 'Picture this: a Saturday morning, a hundred teenagers, and nowhere for them to go.'),
    ('Hello. My name is Ana and today is Monday.', 'it gives irrelevant information and no hook', 'Ana here – and I have a question that will change your Monday.'),
    ('Since the dawn of time, people have liked music.', 'a cliché and sweeping generalisation with no specific focus', 'At fourteen, I could not read music; at fifteen, I played my first concert.'),
    ('This review is about a restaurant.', 'it is vague and gives no sense of the reviewer’s voice or verdict', 'Go for the noodles, stay for the view – but avoid the dessert menu.'),
    ('Dear Sir, I want to say some things.', 'it is vague and states no purpose', 'Dear Sir, I am writing to urge the council to reconsider the closure of Riverside Pool.'),
    ('Pollution is bad and we should stop it.', 'it is simplistic and unsupported, with no hook or specific detail', 'Our river was once clear enough to swim in; last summer it was clear enough to see the shopping trolleys.'),
]


@t42.add('C1', (1, 2, 3))
def t42_open(r, D):
    s, lab = r.choice(OPENINGS)
    opts, ans = mcq(r, cap(lab), [cap(x) for x in OPEN_POOL if x != lab])
    return {'stem': f'Which technique is used in this opening? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(lab)}.'}


@t42.add('C2', (1, 2, 3, 4), 'explain')
def t42_weak(r, D):
    s, why, better = r.choice(WEAK_OPEN)
    m = marks('C2', D)
    return {'stem': f'A student begins a piece of writing: {Q(s)} Explain why this opening is ineffective and suggest an improvement.', 'answer': f'{cap(why)}. Improved: {better}',
            'key': f'{upto(m)}: 1 mark – identifies the weakness; 1 mark – explains its effect on the reader; 1 mark – a valid, more engaging alternative.', 'marks': m}


@t42.add('C2', (2, 3, 4), 'explain')
def t42_effect(r, D):
    s, lab = r.choice(OPENINGS)
    desc, ck = sw_task(r)
    m = marks('C2', D)
    form = r.choice(['a persuasive speech', 'a magazine article', 'a personal blog post', 'a short story', 'a discursive essay', 'a letter to a newspaper'])
    return {'stem': f'Explain the likely effect of {Q(s)} as the opening of {form}, and evaluate how well this technique suits that form.',
            'answer': f'It uses {lab} to hook the reader; its suitability depends on the conventions and audience of {form}.',
            'key': f'{upto(m)}: 1 mark – identifies the technique ({lab}); 1 mark – explains its likely effect; 1 mark – evaluates its suitability for this form and audience.', 'marks': m}


@t42.add('C3', (1, 2, 3, 4, 5), 'short')
def t42_two(r, D):
    desc, ck = sw_task(r)
    a, b = r.sample(OPEN_POOL, 2)
    m = marks('C3', D)
    return {'stem': f'Write two contrasting openings (one or two sentences each) for {desc}: one using {OPEN_PHRASE[a]} and one using {OPEN_PHRASE[b]}. Then explain which is more effective for the audience.',
            'answer': f'Two openings, using {a} and {b} accurately, and a justified evaluation.',
            'key': pts_key(m, [f'opening using {a}', f'opening using {b}', 'both suited to the form', 'evaluation linked to audience', 'accuracy']), 'marks': m}


@t42.add('C4', (2, 3, 4, 5), 'long')
def t42_task(r, D):
    a = r.choice(OPEN_POOL)
    return sw_long(r, D, extra=f' Begin with {OPEN_PHRASE[a]}, and create a distinctive voice throughout.')



# ---------------------------------------------------------------- 4.3 editing
N43 = 'Editing for precision, concision and accuracy'
t43 = topic(N43, N43)
ISSUES = ['tautology', 'comma splice', 'subject–verb agreement', 'dangling modifier', 'apostrophe error', 'ambiguous pronoun reference', 'wordiness', 'wrong word (malapropism)', 'inconsistent tense', 'cliché']
EDITS = [
    ('The festival will be free of charge and cost nothing.', 'tautology', '‘free of charge’ and ‘cost nothing’ say the same thing', 'The festival will be free.'),
    ('The library closed last year, it was very popular.', 'comma splice', 'two main clauses are joined only by a comma', 'The library closed last year, although it was very popular.'),
    ('The number of volunteers have increased.', 'subject–verb agreement', 'the subject ‘number’ is singular', 'The number of volunteers has increased.'),
    ('Walking to school, the rain soaked my bag.', 'dangling modifier', 'the rain was not walking to school', 'Walking to school, I got my bag soaked by the rain.'),
    ('The council has made it’s decision.', 'apostrophe error', '‘it’s’ means ‘it is’; the possessive is ‘its’', 'The council has made its decision.'),
    ('When Zara met Ines, she was nervous.', 'ambiguous pronoun reference', 'it is unclear who ‘she’ refers to', 'Zara was nervous when she met Ines.'),
    ('Due to the fact that it was raining, the match was postponed until a later date.', 'wordiness', '‘due to the fact that’ and ‘until a later date’ are padding', 'Because of rain, the match was postponed.'),
    ('The new rules will effect everyone who rides a scooter.', 'wrong word (malapropism)', '‘effect’ (noun) is confused with ‘affect’ (verb)', 'The new rules will affect everyone who rides a scooter.'),
    ('We walked to the monastery and then we climb the stairs.', 'inconsistent tense', 'the tense shifts from past to present', 'We walked to the monastery and then climbed the stairs.'),
    ('At the end of the day, every cloud has a silver lining.', 'cliché', 'two worn-out phrases replace precise meaning', 'Even the setbacks taught us something useful.'),
    ('In my opinion I personally think the plan is good.', 'tautology', '‘in my opinion’ and ‘I personally think’ repeat the same idea', 'I think the plan is good.'),
    ('The scooters are popular, many people use them daily.', 'comma splice', 'a comma joins two independent clauses', 'The scooters are popular; many people use them daily.'),
    ('Each of the stalls sell street food.', 'subject–verb agreement', '‘each’ takes a singular verb', 'Each of the stalls sells street food.'),
    ('Having eaten the dumplings, the queue seemed worthwhile.', 'dangling modifier', 'the queue did not eat the dumplings', 'Having eaten the dumplings, I felt the queue had been worthwhile.'),
    ('The students books were left in the hall.', 'apostrophe error', 'the plural possessive needs an apostrophe after the s', 'The students’ books were left in the hall.'),
    ('It is absolutely essential that we must act now in the present moment.', 'wordiness', 'redundant intensifiers and phrases', 'We must act now.'),
]
PARAS = [
    ('Due to the fact that the pool is closing, many people they are upset, it was the only pool in town. The council have said there decision is final. In my opinion I think this is a disgrace and at the end of the day something must be done.',
     'Because the town’s only pool is closing, many people are upset. The council has said its decision is final. I think this is a disgrace, and something must be done.',
     ['wordiness (‘due to the fact that’)', 'double subject (‘people they’)', 'comma splice', '‘council have’ → ‘has’ (consistency)', '‘there’ → ‘its/their’', 'tautology (‘In my opinion I think’)', 'cliché (‘at the end of the day’)']),
    ('Walking through the market, the smell of spices were everywhere. Each of the stalls sell something different, there is food from twenty countries. Its a brilliant place and it effects everyone who visits it in a positive way.',
     'As I walked through the market, the smell of spices was everywhere. Each stall sells something different: there is food from twenty countries. It is a brilliant place that affects every visitor positively.',
     ['dangling modifier', '‘smell … were’ → ‘was’', '‘Each … sell’ → ‘sells’', 'comma splice', '‘Its’ → ‘It’s/It is’', '‘effects’ → ‘affects’', 'wordiness']),
    ('The trek was hard, we walk for seven hours every day. When Pema met the tourists, he was tired. The views were absolutely totally amazing and the mountains was huge.',
     'The trek was hard: we walked for seven hours every day. The tourists were tired when Pema met them. The views were spectacular and the mountains were huge.',
     ['comma splice', 'tense shift (‘walk’)', 'ambiguous ‘he’', 'redundant intensifiers', '‘mountains was’ → ‘were’', 'imprecise ‘amazing’']),
    ('The ban on phones will be implemented and put into practice from Monday onwards. Students who brings phones will have them confiscated, this is fair. The head teacher said it will improve focus, she was confident.',
     'The phone ban begins on Monday. Students who bring phones will have them confiscated, which is fair. The head teacher said confidently that it will improve focus.',
     ['tautology (‘implemented and put into practice’)', 'wordiness (‘from Monday onwards’)', '‘Students who brings’ → ‘bring’', 'comma splice', 'second comma splice']),
]


@t43.add('C1', (1, 2, 3))
def t43_issue(r, D):
    s, iss, why, fix = r.choice(EDITS)
    opts, ans = mcq(r, cap(iss), [cap(x) for x in ISSUES if x != iss])
    return {'stem': f'Which error or weakness is found in this sentence? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(iss)}: {why}. Correction: {fix}'}


@t43.add('C2', (1, 2, 3, 4), 'explain')
def t43_explain(r, D):
    s, iss, why, fix = r.choice(EDITS)
    m = marks('C2', D)
    return {'stem': f'Explain what is wrong with this sentence and correct it: {Q(s)}', 'answer': f'{cap(iss)}: {why}. Corrected: {fix}',
            'key': f'{upto(m)}: 1 mark – identifies the problem ({iss}); 1 mark – explains it; 1 mark – an accurate correction.', 'marks': m}


@t43.add('C3', (1, 2, 3, 4, 5), 'short')
def t43_edit(r, D):
    para, fixed, errs = r.choice(PARAS)
    m = marks('C3', D)
    n = min(len(errs), 2 + D)
    return {'stem': f'Edit this paragraph for accuracy and concision, correcting at least {NUMW.get(n, n)} errors or weaknesses: {Q(para)}', 'answer': f'Model: {fixed}',
            'key': pts_key(m, errs, 'Deduct for introducing new errors.'), 'marks': m}


@t43.add('C4', (2, 3, 4, 5), 'multi_step')
def t43_justify(r, D):
    para, fixed, errs = r.choice(PARAS)
    m = marks('C4', D)
    who = person(r)
    return {'stem': f'{who} has drafted this paragraph for a letter to a local newspaper: {Q(para)} Produce an improved version and write a short commentary justifying your three most important changes in terms of precision, concision and accuracy.',
            'answer': f'Model: {fixed} Justifications: ' + '; '.join(errs[:3]) + '.', 'key': pts_key(m, errs + ['justifications linked to clarity for the reader', 'register suitable for a newspaper letter']), 'marks': m}


CHAPTERS[4] = [t41, t42, t43]


# =========================================================== 5 Reflective commentary (Paper 2 Question 1(b))

def sq(t):
    """Straight single quotes -> curly: opening after a space/bracket/start, closing or apostrophe otherwise."""
    return re.sub(r"(^|[\s(])'", lambda m_: m_.group(1) + '‘', t).replace("'", '’')


class Piece:
    """A student's short piece written in response to a stimulus text, with its choices and comparisons."""

    def __init__(self, stim, task, form, aud, text, choices, comps):
        self.stim, self.task, self.form, self.aud = stim, task, form, aud
        self.text = clean(sq(text))
        self.choices = [(sq(q), c, e) for q, c, e in choices]
        self.comps = [(sq(a), sq(b), d) for a, b, d in comps]
        for q, _, _ in self.choices:
            assert q in self.text, q
        for a, b, _ in self.comps:
            assert a in self.text, a
            assert b.replace("'", '’') in stim.text, b

    def show(self):
        return f'A student was asked to write {self.task}. This is the student’s response: {Q(self.text)}'


PIECES = [
    Piece(A3, 'a review of a local café for a student website', 'review', 'students', """
Café Lumo, Kiln Street. Verdict: worth the walk. Tucked behind the bus station, Lumo is tiny – six tables, one overworked espresso machine
and a playlist stuck firmly in the 1990s. But the cardamom buns? Life-changing. Soft, sticky and still warm at four o'clock. Service is
slow when it's busy, so don't come in a hurry. Students get ten per cent off with a card. Three and a half stars.""",
          [('Verdict: worth the walk.', 'front-loaded verdict in a minor sentence', 'give busy student readers my judgement immediately'),
           ('one overworked espresso machine', 'personification', 'add humour and make the café feel characterful rather than shabby'),
           ('But the cardamom buns? Life-changing.', 'rhetorical question followed by a hyperbolic minor sentence', 'create a lively, teenage voice and highlight the best item'),
           ('Soft, sticky and still warm', 'tricolon with sibilance', 'appeal to the senses so readers can almost taste the buns'),
           ("so don't come in a hurry", 'direct address with an imperative', 'give practical advice in a friendly tone'),
           ('Students get ten per cent off with a card.', 'content selected for the audience', 'include the detail that matters most to student readers')],
          [('Three and a half stars.', 'Four stars.', 'both end with a star rating, a convention of reviews'),
           ('Verdict: worth the walk.', 'Arrive hungry and leave your diet at home.', 'the stimulus opens with playful imperatives, whereas my review opens with a verdict for quick reading'),
           ('Life-changing.', 'fold dumplings so fast their hands blur', 'both use hyperbole to praise the food')]),
    Piece(A1, 'a speech to students persuading them to join a school gardening club', 'speech', 'students', """
Hands up if you have ever eaten a tomato you grew yourself. Not many of you. Not yet. Behind the science block there is a patch of ground
nobody uses – weeds, broken pots, a lonely bench. By June, it could be feeding the canteen. We need twenty volunteers, one lunchtime a
week. No experience required, just a willingness to get muddy. So come to Room 12 on Thursday. Let's grow something.""",
          [('Hands up if you have ever eaten a tomato you grew yourself.', 'interactive imperative opening', 'involve a live audience physically from the first line'),
           ('Not many of you. Not yet.', 'minor sentences', 'pause for effect and hint, through ‘yet’, that this could change'),
           ('weeds, broken pots, a lonely bench', 'list with personification', 'make the neglected space seem sad so that listeners want to rescue it'),
           ('No experience required', 'reassurance', 'remove a likely objection and make joining feel easy'),
           ("Let's grow something.", 'inclusive imperative with a double meaning', 'end on a short, memorable call to action; ‘grow’ suggests personal growth too')],
          [('Hands up if you have ever eaten a tomato you grew yourself.', 'Look up when you leave tonight.', 'both open with an imperative that asks listeners to do something physical'),
           ('We need twenty volunteers', 'grew four hundred kilos of vegetables', 'the stimulus uses figures as evidence of success; I use a figure as a target'),
           ("Let's grow something.", 'turn this grey city green', 'both end with a short slogan, but mine is plainer and more conversational for a student audience')]),
    Piece(A6, 'a short fundraising leaflet for a school sponsored walk', 'leaflet', 'parents and students', """
WALK 10K, CHANGE A LIFE. [image: students in yellow T-shirts crossing a bridge] On 4 May, our whole school is walking for the city's food
bank. Last year 300 walkers raised enough for 2,000 family meals. This year we want to double it. • Get sponsored by family and friends •
Collect your T-shirt from reception • Bring water and a smile. Every step counts.""",
          [('WALK 10K, CHANGE A LIFE.', 'capitalised imperative headline with parallel structure', 'grab attention and link a small effort to a big result'),
           ('[image: students in yellow T-shirts crossing a bridge]', 'image', 'show a sense of community and make the event look fun'),
           ('Last year 300 walkers raised enough for 2,000 family meals.', 'statistics', 'prove that the event makes a real difference'),
           ('• Get sponsored by family and friends', 'bulleted imperatives', 'make the steps easy to follow at a glance'),
           ('Every step counts.', 'idiom with a literal pun', 'end on a memorable phrase that suits a walk')],
          [('WALK 10K, CHANGE A LIFE.', 'Six-year-old Mateo spent his last birthday in a hospital bed', 'the stimulus opens with one child’s story, whereas my leaflet opens with a slogan, because readers skim leaflets'),
           ('Last year 300 walkers raised enough for 2,000 family meals.', 'Each one costs less than a family car', 'both translate money into something concrete, but I use statistics rather than a comparison'),
           ('• Get sponsored by family and friends', 'Sign up today, and we will send you a free training plan', 'both end with practical calls to action; mine uses bullet points instead of continuous prose')]),
    Piece(A2, 'a blog post by a teenager about living with water restrictions', 'blog', 'teenage readers', """
Day nine of the hosepipe ban and my mum has started timing my showers. Four minutes. FOUR. I'm not saying it's a human-rights issue, but
it's close. Joking aside, it's weird seeing the park go brown. The fountain in the square has been switched off and the ducks look
personally offended. I get it – the reservoirs are at 31 per cent. But maybe fix the leaky pipes first?""",
          [('Day nine of the hosepipe ban', 'time marker as an opening', 'give a diary-like immediacy and a personal angle'),
           ('Four minutes. FOUR.', 'minor sentences with capitals', 'mimic exasperated speech and create comedy'),
           ("I'm not saying it's a human-rights issue, but it's close.", 'ironic hyperbole', 'mock my own overreaction so readers laugh with me'),
           ('the ducks look personally offended', 'personification', 'make the effects of the drought vivid and funny'),
           ('But maybe fix the leaky pipes first?', 'rhetorical question', 'end with a pointed criticism in a casual tone')],
          [('my mum has started timing my showers', 'will be banned', 'the stimulus uses an impersonal passive; I use a personal, everyday detail'),
           ('the reservoirs are at 31 per cent', 'have fallen to 31 per cent of capacity', 'I keep the key statistic from the stimulus but drop its formal phrasing'),
           ('But maybe fix the leaky pipes first?', 'Critics argue that the authority has failed to repair leaking pipes', 'both end on the leaks, but the stimulus reports critics neutrally while I make the criticism my own')]),
    Piece(A7, 'a script for a 30-second radio advertisement promoting safe e-scooter riding', 'radio', 'radio listeners', """
[sound of traffic] VOICE 1 (worried): Is that a scooter on the pavement? VOICE 2 (calm): Not any more. In this city, scooters stay on roads
and cycle lanes. Helmet on. One rider. Eighteen plus. VOICE 1: And if you don't? VOICE 2: Up to three hundred dollars. Ride smart. Ride
safe. [ping]""",
          [('[sound of traffic]', 'sound effect', 'set the scene instantly for listeners who cannot see anything'),
           ('Is that a scooter on the pavement?', 'question-and-answer dialogue', 'dramatise the problem through two voices'),
           ('Helmet on. One rider. Eighteen plus.', 'compressed minor sentences', 'make the rules quick and easy to remember by ear'),
           ('Ride smart. Ride safe.', 'parallel imperatives with alliteration', 'give a catchy slogan to end the advert')],
          [('Helmet on. One rider. Eighteen plus.', '• Only one rider per scooter.', 'the stimulus uses visual bullet points; I turn the rules into short spoken fragments for radio'),
           ('Up to three hundred dollars.', 'Fines of up to $300 may be issued', 'the stimulus uses an impersonal passive; my script states the fine bluntly as an answer'),
           ('Ride smart. Ride safe.', 'Wear a helmet.', 'both use imperatives, but mine are paired for rhythm')]),
    Piece(A4, 'a travel blog entry written at the end of a day’s trekking', 'blog', 'followers of a travel blog', """
Altitude: 3,900 metres. Mood: somewhere between joy and nausea. Today we climbed for seven hours and I genuinely thought my lungs had
resigned. Then the clouds split and there it was – the whole valley laid out like a map someone had painted in gold. Our guide just
smiled and said, 'Every day, the same. Every day, new.' I'm going to think about that for a while.""",
          [('Altitude: 3,900 metres. Mood: somewhere between joy and nausea.', 'header-style noun phrases', 'parody a log entry and set a humorous tone at once'),
           ('my lungs had resigned', 'personification', 'convey exhaustion with humour'),
           ('like a map someone had painted in gold', 'simile', 'capture the beauty of the view'),
           ("'Every day, the same. Every day, new.'", 'direct speech with a paradox', 'let the guide’s wisdom carry the reflective ending'),
           ("I'm going to think about that for a while.", 'reflective ending', 'leave readers with a thoughtful, unresolved note')],
          [('my lungs had resigned', 'my legs had stopped complaining and simply given up', 'both personify the body to convey exhaustion humorously'),
           ('like a map someone had painted in gold', 'like a cruel joke', 'the stimulus simile expresses frustration; mine expresses wonder'),
           ("I'm going to think about that for a while.", 'I felt very small, and strangely grateful.', 'both end reflectively, but mine is more casual for a blog')]),
    Piece(B5, 'a letter to a newspaper editor arguing against a school phone ban', 'letter', 'newspaper readers', """
Dear Editor, Your editorial 'Pocket the Phones' (12 May) makes a confident case, but it overlooks the students it claims to protect. For
many young carers, a phone is not a distraction; it is a lifeline. Banning phones outright punishes the responsible majority for the habits
of a few. Surely teaching students to manage technology is better than pretending it does not exist? Yours faithfully, Ines Duarte""",
          [('Dear Editor,', 'formal salutation', 'follow the conventions of a letter to a newspaper'),
           ("Your editorial 'Pocket the Phones' (12 May)", 'reference to the original text', 'make clear what I am responding to'),
           ('a phone is not a distraction; it is a lifeline', 'antithesis with metaphor', 'reframe the phone as essential for some students'),
           ('punishes the responsible majority for the habits of a few', 'antithesis', 'present the ban as unfair'),
           ('Surely teaching students to manage technology is better than pretending it does not exist?', 'rhetorical question', 'leave readers with a challenge they find hard to reject')],
          [('a phone is not a distraction; it is a lifeline', 'problems of management, not of principle', 'both use antithesis to reframe the argument'),
           ('Surely teaching students to manage technology', 'Schools should pocket the phones', 'the stimulus ends with a firm modal recommendation; I end with a rhetorical question'),
           ('makes a confident case, but it overlooks', 'Of course, a ban is not a cure-all', 'both use concession, but I concede the editorial’s confidence before attacking it')]),
    Piece(A8, 'a short tribute to a closing local shop for a community newsletter', 'article', 'local residents', """
After forty-one years, Mendes Hardware will sell its last box of nails on Saturday. For generations of DIY disasters, Mr Mendes was the
calm voice at the counter: 'Ah, you need a washer, not a new tap.' He knew every customer's name and most of their mistakes. The shelves
are emptying now, but the advice he gave away free will last longer than any of it. Thank you, Mr Mendes.""",
          [('After forty-one years', 'time-span opening', 'establish the shop’s place in local history'),
           ('its last box of nails', 'concrete detail', 'make the closure feel real and specific'),
           ("'Ah, you need a washer, not a new tap.'", 'direct speech', 'give Mr Mendes a warm, recognisable voice'),
           ("every customer's name and most of their mistakes", 'humorous anticlimax', 'add affectionate humour'),
           ('Thank you, Mr Mendes.', 'direct address in a minor sentence', 'end with a personal, community-wide thank-you')],
          [('After forty-one years', 'For ninety-two years', 'both open with the length of service to show the place’s importance'),
           ("'Ah, you need a washer, not a new tap.'", '“People say streaming killed us,”', 'both quote the shopkeeper, but my quotation shows his helpfulness rather than his view of the closure'),
           ('Thank you, Mr Mendes.', 'The building will become a car park.', 'the stimulus ends bleakly with bathos; I end warmly with gratitude')]),
]
COMM_WEAK = [
    ('I wrote this review because the question told me to write a review.', 'narrates the writing process'),
    ('I think my speech is really good and the audience will love it.', 'evaluates quality instead of analysing'),
    ('I used lots of techniques like metaphors and lists to make it better.', 'feature-spotting without effect'),
    ('First I planned it, then I wrote it, then I checked it.', 'narrates the writing process'),
    ('My leaflet is better than the stimulus text because it is more interesting.', 'evaluates quality instead of analysing'),
    ('I chose words that were good for the text.', 'no quotation from own writing'),
    ('I used a rhetorical question.', 'feature-spotting without effect'),
    ('The language in my piece is effective.', 'no quotation from own writing'),
    ('I added a simile because similes are a good technique.', 'no reference to audience or purpose'),
    ('My piece uses informal language.', 'no reference to audience or purpose'),
]
FLAW_VERB = {'narrates the writing process': 'narrates the writing process instead of analysing choices', 'evaluates quality instead of analysing': 'judges the quality of the writing instead of analysing it',
             'feature-spotting without effect': 'names techniques without explaining their effects', 'no quotation from own writing': 'gives no quotation from the student’s own writing',
             'no reference to audience or purpose': 'does not link the choice to the audience or purpose'}
COMM_FLAWS = ['narrates the writing process', 'evaluates quality instead of analysing', 'feature-spotting without effect', 'no quotation from own writing', 'no reference to audience or purpose']


def good_sentence(p, ch):
    q, c, e = ch
    return f'I used {c} in {Q(q)} to {e}, which suits {p.aud}.'


# ---------------------------------------------------------------- 5.1 explaining own choices
N51 = 'Explaining own linguistic choices and their intended effects'
t51 = topic(N51, N51)
t51.fixed('C1', (1, 2), [
    ('What is the main focus of a reflective commentary?', 'Analysing the linguistic and structural choices made in your own writing and their intended effects',
     'The commentary analyses choices of form, structure and language, linked to audience and purpose.', ['Retelling the content of your writing', 'Describing how long you spent writing', 'Giving your opinion of the topic']),
    ('Which assessment objective does the reflective commentary mainly target?', 'AO3: analysing how meaning is shaped by linguistic choices', 'The commentary is an analytical task on your own text.',
     ['AO2 only: writing creatively', 'Spelling accuracy only', 'Knowledge of literary history']),
    ('In a commentary, why should you quote from your own writing?', 'To provide precise evidence for the choices you analyse', 'As in any analysis, quotation supports claims.', ['To make the commentary longer', 'To show you can copy accurately', 'Quotation is not allowed']),
])


@t51.add('C1', (1, 2, 3))
def t51_best(r, D):
    p = r.choice(PIECES)
    good = good_sentence(p, r.choice(p.choices))
    opts, ans = mcq(r, good, [w for w, _ in r.sample(COMM_WEAK, 5)])
    return {'stem': f'A student wrote {p.task}. Which sentence would gain most credit in the student’s reflective commentary?', 'options': opts, 'answer': ans,
            'key': f'{Q(good)} names a specific choice, quotes it and explains its effect on the audience; the others narrate, evaluate or feature-spot.'}


@t51.add('C2', (1, 2, 3, 4), 'explain')
def t51_effect(r, D):
    p = r.choice(PIECES)
    q, c, e = r.choice(p.choices)
    m = marks('C2', D)
    return {'stem': f'A student wrote {p.task}, including the words {Q(q)}{"" if q[-1:] in ".?!" else "."} Explain the intended effect of this choice, as the student might in a reflective commentary.',
            'answer': f'{cap(c)}: intended to {e}.', 'key': f'{upto(m)}: 1 mark – identifies the choice ({c}); 1 mark – explains the intended effect ({e}); 1 mark – links it to the audience ({p.aud}) or purpose.', 'marks': m}


@t51.add('C3', (1, 2, 3, 4, 5), 'explain')
def t51_para(r, D):
    p = r.choice(PIECES)
    n = 2 if D <= 3 else 3
    m = marks('C3', D)
    chs = p.choices[:]
    r.shuffle(chs)
    return {'stem': f'{p.show()} Imagine you are this student. Write a paragraph of reflective commentary analysing {NUMW[n]} of the choices you made, quoting from your writing.',
            'answer': ' '.join(good_sentence(p, ch) for ch in chs[:n]),
            'key': pts_key(m, [f'{Q(q)}: {c} – intended to {e}' for q, c, e in p.choices] + ['analytical terminology', 'links to audience and purpose']), 'marks': m}


@t51.add('C4', (2, 3, 4, 5), 'long')
def t51_long(r, D):
    p = r.choice(PIECES)
    m = marks('C4', D, long=True)
    task = r.choice(['Write a reflective commentary on this response, analysing the choices of form, structure and language and their intended effects.',
                     'Writing as the student, produce a reflective commentary explaining how your linguistic choices suit your audience and purpose.'])
    ind = '; '.join(f'{Q(q)} ({c}): to {e}' for q, c, e in p.choices) + f'; form conventions of {an(p.form)} {p.form}; audience: {p.aud}.'
    return {'stem': f'{p.show()} {task}', 'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'commentary', ind), 'type': 'long', 'marks': m}


@t51.add('C3', (2, 3, 4, 5), 'explain')
def t51_quotes(r, D):
    p = r.choice(PIECES)
    chs = r.sample(p.choices, 2 if D <= 3 else 3)
    m = marks('C3', D)
    qs = ' '.join(f'({i + 1}) {Q(q)}' for i, (q, _, _) in enumerate(chs))
    return {'stem': f'A student wrote {p.task}. The response includes: {qs} Writing as the student, analyse each choice and its intended effect on {p.aud}.',
            'answer': ' '.join(good_sentence(p, ch) for ch in chs),
            'key': pts_key(m, [f'({i + 1}) {c}: to {e}' for i, (_, c, e) in enumerate(chs)], '1 mark for each accurately named choice and 1 for each explained effect.'), 'marks': m}


# ---------------------------------------------------------------- 5.2 comparing own writing with a stimulus text
N52 = 'Comparing own writing with a stimulus text'
t52 = topic(N52, N52)
t52.fixed('C1', (1, 2), [
    ('In a commentary that compares your writing with the stimulus text, what should you mainly compare?', 'Choices of form, structure and language and the reasons for them',
     'Comparison explains how and why your text differs from or resembles the stimulus.', ['Which text is longer', 'Which text you prefer', 'The handwriting of the two texts']),
    ('Which connective best introduces a difference between your text and the stimulus?', 'whereas', 'Use comparative connectives: whereas, in contrast, similarly, likewise.', ['therefore', 'firstly', 'in conclusion']),
    ('Why might your text deliberately differ in register from the stimulus?', 'Because your text has a different audience, form or purpose', 'Differences should be explained by the new task.', ['To avoid using any words from it', 'Because the stimulus is always wrong', 'To make it shorter']),
])
WEAK_COMP = ['Both texts are really good.', 'My text is better than the stimulus text.', 'The stimulus text is longer than mine.', 'I copied some words from the stimulus.',
             'The stimulus text was boring so I made mine fun.', 'Both texts have words in them.']


@t52.add('C1', (1, 2, 3))
def t52_best(r, D):
    p = r.choice(PIECES)
    a, b, d = r.choice(p.comps)
    good = cap(d) + '.'
    opts, ans = mcq(r, good, r.sample(WEAK_COMP, 4))
    return {'stem': f'A student wrote {p.task}, using {p.stim.label} as the stimulus. Which is the most effective comparative point for the commentary?', 'options': opts, 'answer': ans,
            'key': f'{good} It compares specific choices and explains the difference.'}


@t52.add('C2', (1, 2, 3, 4), 'explain')
def t52_diff(r, D):
    p = r.choice(PIECES)
    a, b, d = r.choice(p.comps)
    m = marks('C2', D)
    return {'stem': f'A student wrote {p.task}, based on {p.stim.label}. The stimulus includes {Q(b)}; the student wrote {Q(a)}. Explain the similarity or difference between these choices and the reason for it.',
            'answer': cap(d) + '.', 'key': f'{upto(m)}: 1 mark – identifies the similarity or difference; 1 mark – refers to both quotations; 1 mark – explains it in terms of form, audience or purpose.', 'marks': m}


@t52.add('C3', (2, 3, 4, 5), 'explain')
def t52_compare(r, D):
    p = r.choice(PIECES)
    n = 2 if D <= 3 else 3
    m = marks('C3', D)
    return {'stem': f'{p.stim.show()} {p.show()} Compare {NUMW[n]} of the student’s choices with choices in the stimulus text, explaining the reasons for the similarities and differences.',
            'answer': ' '.join(cap(d) + '.' for _, _, d in p.comps[:n]),
            'key': pts_key(m, [f'{Q(a)} v. {Q(b)}: {d}' for a, b, d in p.comps] + ['comparative connectives used', 'reasons linked to audience, form or purpose']), 'marks': m}


@t52.add('C3', (1, 2, 3, 4, 5), 'explain')
def t52_quotes(r, D):
    p = r.choice(PIECES)
    cs = r.sample(p.comps, 2)
    m = marks('C3', D)
    qs = ' '.join(f'({i + 1}) stimulus {Q(b)} – student {Q(a)}' for i, (a, b, _) in enumerate(cs))
    return {'stem': f'A student wrote {p.task}, using {p.stim.label} as the stimulus. Compare these pairs of choices and explain the reasons for the similarities or differences: {qs}',
            'answer': ' '.join(f'({i + 1}) {cap(d)}.' for i, (_, _, d) in enumerate(cs)),
            'key': pts_key(m, [f'({i + 1}) {d}' for i, (_, _, d) in enumerate(cs)] + ['reasons linked to the new audience, form or purpose']), 'marks': m}


@t52.add('C4', (2, 3, 4, 5), 'multi_step')
def t52_eval(r, D):
    p = r.choice(PIECES)
    m = marks('C4', D)
    qs = ' '.join(f'({i + 1}) stimulus {Q(b)} – student {Q(a)}' for i, (a, b, _) in enumerate(p.comps))
    who = person(r)
    return {'stem': f'{who} wrote {p.task}, adapting {p.stim.label}. Compare the pairs of choices below and evaluate how successfully the student has adapted the stimulus for {p.aud}: {qs}',
            'answer': ' '.join(f'({i + 1}) {cap(d)}.' for i, (_, _, d) in enumerate(p.comps)) + ' Evaluation: the adaptations suit the new form and audience.',
            'key': pts_key(m, [f'({i + 1}) {d}' for i, (_, _, d) in enumerate(p.comps)] + ['an evaluative judgement on the success of the adaptation', 'reference to audience and form']), 'marks': m}


@t52.add('C4', (2, 3, 4, 5), 'long')
def t52_long(r, D):
    p = r.choice(PIECES)
    m = marks('C4', D, long=True)
    ind = '; '.join(f'{Q(a)} v. {Q(b)}: {d}' for a, b, d in p.comps) + '; ' + '; '.join(f'{Q(q)} ({c})' for q, c, _ in p.choices[:3]) + '.'
    return {'stem': f'{p.stim.show()} {p.show()} Write a reflective commentary on the student’s response, analysing its form, structure and language and comparing it with the stimulus text.',
            'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'commentary', ind), 'type': 'long', 'marks': m}


# ---------------------------------------------------------------- 5.3 structuring a commentary
N53 = 'Structuring a reflective commentary with evidence from own writing'
t53 = topic(N53, N53)
t53.fixed('C1', (1, 2), [
    ('What is the best way to open a reflective commentary?', 'A brief overview of the task’s audience, purpose and form and your overall approach', 'An overview frames the analysis.',
     ['A summary of the plot of your writing', 'A list of all the techniques you used', 'An apology for any mistakes']),
    ('How should paragraphs in a commentary usually be organised?', 'Around specific choices or frameworks, each with quotation and effect', 'E.g. one paragraph on structure, one on lexis, one on grammar.',
     ['In the order in which you wrote the piece, sentence by sentence', 'With no paragraphs at all', 'By the length of each quotation']),
    ('Which tense is most often used to analyse choices in a commentary?', 'The present and past tense to describe choices and their intended effects (e.g. ‘I chose … to …’)', 'Commentaries discuss decisions made and their effects.',
     ['The future tense only', 'Only the conditional', 'Tense does not matter at all']),
])


@t53.add('C1', (1, 2, 3))
def t53_flaw(r, D):
    s, fl = r.choice(COMM_WEAK)
    opts, ans = mcq(r, cap(fl), [cap(x) for x in COMM_FLAWS if x != fl])
    return {'stem': f'A student writes in a reflective commentary: {Q(s)} What is the main weakness of this sentence?', 'options': opts, 'answer': ans, 'key': f'{cap(fl)}.'}


@t53.add('C2', (1, 2, 3, 4), 'explain')
def t53_fix(r, D):
    s, fl = r.choice(COMM_WEAK)
    p = r.choice(PIECES)
    m = marks('C2', D)
    return {'stem': f'In a commentary on {p.task}, a student writes: {Q(s)} Explain why this is weak, and rewrite it using evidence from the student’s text: {Q(p.text)}',
            'answer': f'Weakness: it {FLAW_VERB[fl]}. Improved: {good_sentence(p, r.choice(p.choices))}',
            'key': f'{upto(m)}: 1 mark – identifies the weakness ({fl}); 1 mark – a rewrite that quotes a specific choice; 1 mark – the rewrite explains an effect on the audience.', 'marks': m}


@t53.add('C3', (1, 2, 3, 4, 5), 'multi_step')
def t53_plan(r, D):
    p = r.choice(PIECES)
    chs = p.choices
    parts = [
        lambda r: ('Write an overview sentence for the commentary.', f'An overview naming the form ({p.form}), audience ({p.aud}) and overall approach.', '1 mark form/audience; 1 mark approach [2]'),
        lambda r: ('Choose one choice of structure and explain it with a quotation.', good_sentence(p, chs[0]), '1 mark quotation; 2 marks effect [3]'),
        lambda r: ('Choose one lexical choice and explain it with a quotation.', good_sentence(p, chs[-1]), '1 mark quotation; 2 marks effect [3]'),
        lambda r: ('Write a concluding sentence linking your choices to your purpose.', 'A conclusion that links the choices to the purpose of the text.', '1 mark link; 1 mark clarity [2]'),
    ]
    return compose(r, f'{p.show()} You are planning the student’s reflective commentary.', parts, k=(2, 3, 4), type_='multi_step')


@t53.add('C4', (2, 3, 4, 5), 'long')
def t53_long(r, D):
    p = r.choice(PIECES)
    m = marks('C4', D, long=True)
    ind = 'overview of audience, purpose and form; paragraphs organised by framework or choice; ' + '; '.join(f'{Q(q)} ({c}): to {e}' for q, c, e in p.choices) + '; comparison with the stimulus where relevant; conclusion.'
    return {'stem': f'{p.show()} Write a well-structured reflective commentary on this response. Organise it by choices or frameworks, support each point with quotation and explain each effect.',
            'answer': f'Indicative content: {ind}', 'key': lv_key(m, 'commentary', ind), 'type': 'long', 'marks': m}


CHAPTERS[5] = [t51, t52, t53]


# =========================================================== 6 Extended writing (Paper 2 Section B)

EW_W = {2: '500–600', 3: '600–900', 4: '600–900', 5: '600–900'}


def ew_long(r, D, stem, kind_ind):
    m = marks('C4', D, long=True)
    return {'stem': f'{stem} ({EW_W.get(D, "600–900")} words)', 'answer': f'Indicative content: {kind_ind}', 'key': lv_key(m, 'writing', kind_ind), 'type': 'long', 'marks': m}


# ---------------------------------------------------------------- 6.1 imaginative and descriptive writing
N61 = 'Imaginative and descriptive writing: narrative techniques and atmosphere'
t61 = topic(N61, N61)
NT_POOL = ['in medias res', 'flashback', 'foreshadowing', 'pathetic fallacy', 'cyclical structure', 'unreliable narrator', 'free indirect discourse', 'cliffhanger', 'sensory imagery', 'dialogue']
NT_DEF = {'in medias res': 'beginning in the middle of the action', 'flashback': 'a shift back in time to earlier events', 'foreshadowing': 'a hint of what will happen later',
          'pathetic fallacy': 'weather or setting reflecting mood', 'cyclical structure': 'ending where the story began', 'unreliable narrator': 'a narrator whose account cannot be fully trusted',
          'free indirect discourse': 'third-person narration coloured by a character’s thoughts', 'cliffhanger': 'ending a section at a moment of suspense',
          'sensory imagery': 'description appealing to the senses', 'dialogue': 'the words characters speak'}
NT_SNIP = [
    ('The lifeboat was already half full of water when Amara realised she could not see her brother.', 'in medias res', 'the reader is plunged into a crisis without explanation, creating urgency'),
    ('Twenty years earlier, on the same platform, my father had promised he would come back.', 'flashback', 'the shift in time explains the present and adds emotional depth'),
    ('Nobody noticed the hairline crack spreading slowly across the dam wall.', 'foreshadowing', 'the detail hints at disaster and creates dramatic irony'),
    ('Thunder rolled over the hills as the brothers stopped speaking to each other.', 'pathetic fallacy', 'the storm mirrors the brothers’ conflict'),
    ('And so, once again, I stood at the gate where it had all begun.', 'cyclical structure', 'returning to the opening place gives a sense of closure and change'),
    ('I never lie, of course. Well, hardly ever. And never about anything important.', 'unreliable narrator', 'the self-contradiction makes the reader distrust the narrator'),
    ('Lucas looked at the exam paper. Question one. Easy. Question two. Easy. Question three – what on earth was that?', 'free indirect discourse', 'Lucas’s panicked thoughts merge with the narration'),
    ('She turned the key, the door swung open – and someone was already inside.', 'cliffhanger', 'the section ends on a shock, compelling the reader to continue'),
    ('The air tasted of salt and diesel, and the deck was slick and cold beneath my bare feet.', 'sensory imagery', 'taste and touch make the setting immediate'),
    ('“You’re late,” she said. “I know,” he replied. “I always am.”', 'dialogue', 'clipped exchanges reveal tension and character economically'),
    ('The sky turned the colour of a bruise as the funeral procession wound through the village.', 'pathetic fallacy', 'the bruised sky reflects grief'),
    ('Later, I would wish I had listened to the old fisherman’s warning.', 'foreshadowing', 'the retrospective comment signals that something will go wrong'),
]
IMAG_TITLES = [
    'Write a story called ‘The Last Train Home’.', 'Write a story that begins: ‘The lights went out at exactly midnight.’', 'Write a descriptive piece called ‘The Market at Dawn’.',
    'Write a story in which a character discovers something they were never meant to find.', 'Write a descriptive piece about a city during a power cut.', 'Write a story called ‘The Visitor’.',
    'Describe a place that has changed beyond recognition.', 'Write a story about a journey that does not go to plan.', 'Write a descriptive piece called ‘After the Flood’.',
    'Write a story that ends: ‘…and that was the last time anyone saw the lighthouse lit.’', 'Write a descriptive piece about a crowded bus station at night.', 'Write a story called ‘The Promise’.',
    'Describe an abandoned building as nature reclaims it.', 'Write a story told by a character who is hiding a secret.', 'Write a descriptive piece called ‘The Heatwave’.',
    'Write a story about two strangers stranded together.', 'Describe the moments before and after a storm.', 'Write a story called ‘The Map’.',
]
IMAG_IND = 'an engaging, coherent narrative or description; deliberate structure (e.g. in medias res, flashback, cyclical ending); convincing characterisation or a strong sense of place; atmosphere built through sensory imagery and figurative language; varied sentence structures for pace; precise, ambitious vocabulary; accuracy.'
t61.fixed('C1', (1, 2), [
    ('What is the main difference between descriptive and narrative writing?', 'Description focuses on evoking a place, moment or person; narrative develops a sequence of events',
     'Descriptive pieces should not turn into stories with plot.', ['Description is always in the present tense', 'Narratives never describe', 'There is no difference']),
    ('Which technique most directly creates atmosphere through setting?', 'Pathetic fallacy', 'Weather and setting reflect mood.', ['Flashback', 'Dialogue tags', 'Footnotes']),
    ('What does ‘show, don’t tell’ mean?', 'Conveying feelings and character through action, detail and dialogue rather than stating them', 'E.g. ‘Her hands shook’ rather than ‘She was nervous’.',
     ['Using pictures instead of words', 'Avoiding all description', 'Writing only dialogue']),
])


@t61.add('C1', (1, 2, 3))
def t61_tech(r, D):
    s, lab, why = r.choice(NT_SNIP)
    opts, ans = mcq(r, cap(lab), [cap(x) for x in NT_POOL if x != lab])
    return {'stem': f'Which narrative technique is used in this sentence? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(lab)} ({NT_DEF[lab]}): {why}.'}


@t61.add('C2', (1, 2, 3, 4), 'explain')
def t61_effect(r, D):
    s, lab, why = r.choice(NT_SNIP)
    m = marks('C2', D)
    where = r.choice(['the opening of a short story', 'the middle of a story', 'the end of a chapter', 'a descriptive composition'])
    return {'stem': f'This sentence appears in {where}: {Q(s)} Identify the technique and explain how it engages the reader.', 'answer': f'{cap(lab)}: {why}.',
            'key': f'{upto(m)}: 1 mark – identifies {lab}; 1 mark – explains the effect ({why}); 1 mark – comments on its suitability for {where}.', 'marks': m}


@t61.add('C3', (1, 2, 3, 4, 5), 'short')
def t61_para(r, D):
    title = r.choice(IMAG_TITLES)
    a, b = r.sample(NT_POOL, 2)
    m = marks('C3', D)
    n = {1: 60, 2: 80, 3: 100, 4: 120, 5: 150}[D]
    return {'stem': f'For the task {Q(title)}, write a paragraph (about {n} words) that uses {a} and {b}. Then label where each technique appears.',
            'answer': f'A paragraph using {a} ({NT_DEF[a]}) and {b} ({NT_DEF[b]}) accurately, with both labelled.',
            'key': pts_key(m, [f'effective use of {a}', f'effective use of {b}', 'relevant to the task', 'controlled sentence structures and vocabulary', 'accurate labelling']), 'marks': m}


@t61.add('C4', (2, 3, 4, 5), 'long')
def t61_task(r, D):
    return ew_long(r, D, r.choice(IMAG_TITLES), IMAG_IND)


# ---------------------------------------------------------------- 6.2 discursive writing
N62 = 'Discursive writing: exploring a topic from multiple viewpoints'
t62 = topic(N62, N62)
DISC = [
    ('whether social media brings people together or drives them apart', 'it connects distant friends and communities', 'it encourages comparison and division'),
    ('the advantages and disadvantages of living in a large city', 'jobs, culture and transport', 'cost, pollution and loneliness'),
    ('whether tourism helps or harms local communities', 'income and jobs for residents', 'rising prices, crowding and loss of culture'),
    ('whether school uniforms should be compulsory', 'equality and a sense of identity', 'cost and restriction of self-expression'),
    ('the role of artificial intelligence in education', 'personalised learning and instant feedback', 'over-reliance and loss of independent thinking'),
    ('whether competitive sport should be compulsory in schools', 'fitness and teamwork', 'pressure and exclusion of less sporty students'),
    ('whether zoos still have a place in the modern world', 'conservation and education', 'animal welfare and captivity'),
    ('whether it is better to work for yourself or for a company', 'freedom and creativity', 'insecurity and lack of support'),
    ('the effects of online shopping on high streets', 'convenience and choice for consumers', 'closed shops and empty town centres'),
    ('whether young people should be able to vote at sixteen', 'engagement with decisions that affect their future', 'concerns about maturity and influence'),
    ('whether space exploration is worth the cost', 'scientific discovery and inspiration', 'urgent problems on Earth that need funding'),
    ('whether traditional crafts should be protected', 'cultural heritage and identity', 'cost and declining demand'),
]
t62.fixed('C1', (1, 2), [
    ('How does discursive writing differ from argumentative writing?', 'Discursive writing explores several viewpoints in a balanced way; argumentative writing persuades towards one view',
     'A discursive piece may reach a judgement, but it weighs perspectives fairly.', ['Discursive writing must be fictional', 'Argumentative writing must be balanced', 'They are identical']),
    ('Which connective best signals the move to an opposing viewpoint in a discursive essay?', 'On the other hand', 'Contrastive connectives signal a shift in perspective.', ['Furthermore', 'For example', 'In addition']),
    ('What is the usual tone of discursive writing?', 'Measured and objective', 'Discursive writing avoids one-sided, emotive persuasion.', ['Aggressive and one-sided', 'Comic and informal throughout', 'Purely narrative']),
])
DISC_WEAK = [
    ('Everyone knows zoos are cruel, so they should all be shut down immediately.', 'it is one-sided, assumes agreement and ignores the conservation argument'),
    ('Some people like cities and some people do not.', 'it is vague and undeveloped, with no reasons or evidence'),
    ('Tourism is good. Tourism brings money. Tourism is great for everyone.', 'it is repetitive, one-sided and unsupported'),
    ('Uniforms are pointless and only stupid schools have them.', 'it is emotive and insulting, which undermines a balanced discussion'),
    ('AI in schools has advantages and disadvantages, which I will now list.', 'it announces rather than explores and promises a list rather than a discussion'),
    ('In conclusion, there are good and bad points.', 'the conclusion gives no evaluation or judgement'),
]


@t62.add('C1', (1, 2, 3))
def t62_view(r, D):
    t_, pro, con = r.choice(DISC)
    other = [x for x in DISC if x[0] != t_]
    opts, ans = mcq(r, cap(con), [cap(x[2]) for x in r.sample(other, 3)])
    return {'stem': f'In a discursive essay on {t_}, a writer develops this point: {Q(pro)}. Which point would best represent an opposing viewpoint on the same topic?', 'options': opts, 'answer': ans,
            'key': f'{cap(con)} is the counter-view on this topic; the other options belong to different debates.'}


@t62.add('C2', (1, 2, 3, 4), 'explain')
def t62_weak(r, D):
    s, why = r.choice(DISC_WEAK)
    m = marks('C2', D)
    return {'stem': f'Explain why this sentence would be weak in a discursive essay, and suggest an improvement: {Q(s)}', 'answer': cap(why) + '.',
            'key': f'{upto(m)}: 1 mark – identifies the weakness; 1 mark – explains why it undermines balance or development; 1 mark – a valid improved version.', 'marks': m}


@t62.add('C3', (1, 2, 3, 4, 5), 'multi_step')
def t62_plan(r, D):
    t_, pro, con = r.choice(DISC)
    parts = [
        lambda r: ('Write a thesis statement for the introduction.', f'An opening that frames the debate on {t_} without taking sides too early.', '1 mark relevance; 1 mark balance [2]'),
        lambda r: (f'Develop the viewpoint that {pro} with an example.', f'A point on {pro}, with an example.', '1 mark point; 1 mark example; 1 mark development [3]'),
        lambda r: (f'Develop the opposing viewpoint that {con} with an example.', f'A point on {con}, with an example.', '1 mark point; 1 mark example; 1 mark development [3]'),
        lambda r: ('Write a concluding sentence that reaches a reasoned judgement.', 'A conclusion that weighs both sides and reaches a qualified view.', '1 mark judgement; 1 mark justification [2]'),
    ]
    return compose(r, f'You are planning a discursive essay on {t_}.', parts, k=(2, 3, 4), type_='multi_step')


@t62.add('C4', (2, 3, 4, 5), 'long')
def t62_task(r, D):
    t_, pro, con = r.choice(DISC)
    frame = r.choice([f'Write a discursive essay exploring {t_}.', f'Write an article for a quality magazine discussing {t_}.', f'Write a discursive piece considering different views on {t_}.'])
    ind = f'balanced exploration of at least two perspectives (e.g. {pro}; {con}); evidence and examples; measured tone; cohesive paragraphs with contrastive connectives; a reasoned, qualified conclusion; accuracy.'
    return ew_long(r, D, frame, ind)


# ---------------------------------------------------------------- 6.3 argumentative writing
N63 = 'Argumentative writing: persuasive structure and rhetoric'
t63 = topic(N63, N63)
RH_POOL = ['ethos (appeal to credibility)', 'pathos (appeal to emotion)', 'logos (appeal to logic)', 'hypophora', 'anaphora', 'antithesis', 'concession and rebuttal', 'tricolon']
RH_SNIP = [
    ('As a nurse for twenty years, I have seen what poor air does to children’s lungs.', 'ethos (appeal to credibility)', 'the speaker’s experience gives authority'),
    ('Imagine a child gasping for breath because we could not be bothered to change.', 'pathos (appeal to emotion)', 'a distressing image provokes guilt and sympathy'),
    ('If each household saves ten litres a day, the city saves four million litres.', 'logos (appeal to logic)', 'a clear calculation persuades through reason'),
    ('Why should we care? Because the next drought will not wait for us to be ready.', 'hypophora', 'the writer asks and immediately answers a question, controlling the argument'),
    ('We will not give up. We will not give in. We will not go quietly.', 'anaphora', 'repeating the opening words builds determination'),
    ('It is not a cost; it is an investment.', 'antithesis', 'the contrast reframes the issue'),
    ('Critics say the scheme is too expensive. Yet the cost of doing nothing is far greater.', 'concession and rebuttal', 'the objection is acknowledged and then overturned'),
    ('Cleaner air, quieter streets, healthier children.', 'tricolon', 'three benefits build rhythmically'),
    ('Every leading scientist on the panel agreed with this conclusion.', 'ethos (appeal to credibility)', 'appeals to expert authority'),
    ('Some argue that homework builds discipline. However, the research on younger students suggests otherwise.', 'concession and rebuttal', 'the counter-argument is answered with evidence'),
]
ARG = [
    '‘Homework should be abolished.’', '‘Private cars should be banned from city centres.’', '‘Celebrities have a duty to be role models.’', '‘Exams are the fairest way to assess students.’',
    '‘Every young person should learn to cook.’', '‘Fast fashion should be taxed heavily.’', '‘Libraries are more important than ever.’', '‘Professional athletes are paid too much.’',
    '‘Children should not be allowed smartphones until they are fourteen.’', '‘Tourists should pay to enter historic city centres.’', '‘Remote working is better for everyone.’',
    '‘Governments should fund the arts before sport.’',
]
t63.fixed('C1', (1, 2), [
    ('In an argumentative essay, why is it useful to include a counter-argument?', 'Rebutting it strengthens your own case and shows awareness of other views', 'Concession and rebuttal make an argument more convincing.',
     ['It shows you are unsure', 'It makes the essay balanced and neutral', 'It is not useful']),
    ('Which rhetorical appeal uses facts, statistics and reasoning?', 'Logos', 'Aristotle: ethos (credibility), pathos (emotion), logos (logic).', ['Ethos', 'Pathos', 'Kairos']),
    ('What is the effect of a clear thesis statement at the start of an argument?', 'It tells the reader exactly what position will be defended', 'A clear stance guides the reader.', ['It hides the writer’s view', 'It summarises both sides equally', 'It replaces the conclusion']),
])


@t63.add('C1', (1, 2, 3))
def t63_rh(r, D):
    s, lab, why = r.choice(RH_SNIP)
    opts, ans = mcq(r, cap(lab), [cap(x) for x in RH_POOL if x != lab])
    return {'stem': f'Which rhetorical technique is used here? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(lab)}: {why}.'}


@t63.add('C2', (1, 2, 3, 4), 'explain')
def t63_effect(r, D):
    s, lab, why = r.choice(RH_SNIP)
    m = marks('C2', D)
    who = person(r)
    return {'stem': f'{who} uses this sentence in an argumentative speech: {Q(s)} Explain how it persuades the audience.', 'answer': f'{cap(lab)}: {why}.',
            'key': f'{upto(m)}: 1 mark – identifies the technique; 1 mark – explains how it persuades; 1 mark – comments on its likely effect on the audience.', 'marks': m}


@t63.add('C3', (1, 2, 3, 4, 5), 'short')
def t63_rebut(r, D):
    title = r.choice(ARG)
    stance = r.choice(['agree', 'disagree'])
    m = marks('C3', D)
    n = {1: 60, 2: 80, 3: 100, 4: 120, 5: 150}[D]
    return {'stem': f'You are writing an argumentative essay in which you {stance} with the statement {title} Write a paragraph (about {n} words) that raises a likely counter-argument and rebuts it.',
            'answer': 'A paragraph that fairly states a counter-argument, then rebuts it with evidence or reasoning, using a contrastive connective.',
            'key': pts_key(m, ['counter-argument stated fairly', 'rebuttal with reasoning or evidence', 'contrastive connective', 'persuasive language', 'accuracy']), 'marks': m}


@t63.add('C4', (2, 3, 4, 5), 'long')
def t63_task(r, D):
    title = r.choice(ARG)
    frame = r.choice([f'{title} Write an argumentative essay giving your views.', f'{title} Write the text of a speech for a debating competition arguing for or against this statement.',
                      f'{title} Write a letter to a national newspaper arguing your point of view.'])
    ind = 'a clear, sustained stance; logically sequenced, developed arguments; evidence and examples; rhetorical devices (ethos, pathos, logos, antithesis, tricolon); counter-arguments rebutted; a forceful conclusion; register suited to the form; accuracy.'
    return ew_long(r, D, frame, ind)


# ---------------------------------------------------------------- 6.4 planning and time
N64 = 'Planning and structuring extended writing within the time limit'
t64 = topic(N64, N64)
t64.fixed('C1', (1, 2), [
    ('Paper 2 lasts 2 hours, with two sections of equal marks. About how long should you spend on the Section B extended piece?', 'About one hour, including planning and checking',
     'Equal marks suggest roughly equal time.', ['About 15 minutes', 'About 1 hour 45 minutes', 'As long as it takes, even if Section A is unfinished']),
    ('What is the recommended length for Section B extended writing?', '600–900 words', 'Section B asks for 600–900 words.', ['100–150 words', '120–150 words', 'At least 2,000 words']),
    ('What is the main purpose of a plan for an extended piece?', 'To organise ideas into a deliberate, coherent structure before writing', 'Planning supports structure and cohesion.', ['To write the first draft', 'To count the words', 'To list difficult vocabulary']),
    ('What should you do in the last few minutes of the exam?', 'Proofread for errors in spelling, punctuation and grammar', 'Checking improves accuracy.', ['Start a new piece', 'Rewrite the whole piece', 'Add a long new paragraph']),
])
PLAN_WEAK = [
    ('Intro – stuff about phones. Middle – more stuff. End – conclusion.', 'too vague: no specific ideas, evidence or progression'),
    ('1. Phones are bad. 2. Phones are bad for sleep. 3. Phones are bad for eyes. 4. Phones are bad.', 'repetitive and one-dimensional, with no development or counter-argument'),
    ('A long list of twenty facts about zoos with no order.', 'no structure: ideas are not grouped or sequenced'),
    ('A plan that covers only the opening scene of a story.', 'incomplete: it does not plan the development or ending'),
    ('A two-page plan written in full sentences.', 'too long for timed conditions; it uses time needed for writing'),
]


@t64.add('C1', (1, 2, 3))
def t64_order(r, D):
    t_, pro, con = r.choice(DISC)
    good = f'Introduction → {pro} → {con} → evaluation → conclusion'
    bad = [f'Conclusion → {pro} → introduction → {con}', f'{pro} → {pro} again → conclusion', f'Introduction → conclusion → {con} → {pro}']
    opts, ans = mcq(r, good, bad)
    return {'stem': f'Which plan gives the most logical structure for a discursive essay on {t_}?', 'options': opts, 'answer': ans,
            'key': 'A clear introduction, each viewpoint developed in turn, evaluation and a reasoned conclusion.'}


@t64.add('C2', (1, 2, 3, 4), 'explain')
def t64_weak(r, D):
    s, why = r.choice(PLAN_WEAK)
    title = r.choice(ARG + [f'Write a discursive essay on {x[0]}.' for x in DISC])
    m = marks('C2', D)
    return {'stem': f'A student’s plan for {Q(title)} is: {Q(s)} Explain why this plan is weak and how it could be improved.', 'answer': cap(why) + '.',
            'key': f'{upto(m)}: 1 mark – identifies the weakness; 1 mark – explains its consequence for the final piece; 1 mark – a specific improvement.', 'marks': m}


@t64.add('C3', (1, 2, 3, 4, 5), 'short')
def t64_plan(r, D):
    kind = r.choice(['imag', 'disc', 'arg'])
    m = marks('C3', D)
    if kind == 'imag':
        title = r.choice(IMAG_TITLES)
        need = ['an opening hook or technique', 'development/complication', 'climax or turning point', 'ending (e.g. cyclical or reflective)', 'notes on atmosphere and techniques']
    elif kind == 'disc':
        x = r.choice(DISC)
        title = f'Write a discursive essay exploring {x[0]}.'
        need = ['introduction framing the debate', f'viewpoint 1: {x[1]}', f'viewpoint 2: {x[2]}', 'evaluation', 'reasoned conclusion']
    else:
        title = r.choice(ARG) + ' Argue for or against.'
        need = ['thesis statement', 'argument 1 with evidence', 'argument 2 with evidence', 'counter-argument and rebuttal', 'forceful conclusion']
    return {'stem': f'In timed conditions you have five minutes to plan a response to {Q(title)} Write a concise plan.', 'answer': 'A plan with: ' + '; '.join(need) + '.',
            'key': pts_key(m, need), 'marks': m}


@t64.add('C4', (2, 3, 4, 5), 'multi_step')
def t64_c4(r, D):
    title = r.choice(ARG + IMAG_TITLES)
    m = marks('C4', D)
    return {'stem': f'For the task {Q(title)}, produce a paragraph-by-paragraph plan and then write the opening paragraph. Explain how your plan helps you use the hour available effectively.',
            'answer': 'A structured plan, a strong opening paragraph and a brief explanation of time allocation (e.g. 5–10 minutes planning, 40–45 writing, 5 checking).',
            'key': pts_key(m, ['logical, complete plan', 'opening paragraph that hooks the reader', 'opening consistent with the plan', 'realistic time allocation', 'accuracy of expression', 'awareness of word range (600–900)']), 'marks': m}


@t64.add('C4', (2, 3, 4, 5), 'long')
def t64_long(r, D):
    t_ = r.choice(IMAG_TITLES + ARG)
    lead = f'{t_} Write an argumentative essay giving your views.' if t_ in ARG else t_
    return ew_long(r, D, f'{lead} Plan carefully before you write, and leave time to check your work.', IMAG_IND if t_ not in ARG else
                   'a clear stance; logically sequenced, developed arguments with evidence; counter-arguments addressed; rhetoric used purposefully; cohesive structure; accuracy.')


CHAPTERS[6] = [t61, t62, t63, t64]


# =========================================================== key tidy-up
_LAD = re.compile(r'^(Award up to (\d+) marks?): ((?:1 mark – [^;]+(?:; |\.?$))+)(.*)$', re.S)


def _tidy(q):
    if not q or not isinstance(q.get('key'), str):
        return q
    m_ = _LAD.match(q['key'])
    if m_:
        n = int(m_.group(2))
        pts = [x.strip(' .') for x in re.split(r'; (?=1 mark – )', m_.group(3))]
        if len(pts) > n:
            body = '; '.join(x.replace('1 mark – ', '', 1) for x in pts)
            q['key'] = f'{m_.group(1)}, 1 for each of the following up to the maximum: {body}.' + (' ' + m_.group(4).strip() if m_.group(4).strip() else '')
    return q


def _wrap(fn):
    def g(r, D):
        return _tidy(fn(r, D))
    g.__name__ = fn.__name__
    return g


for _ts in CHAPTERS.values():
    for _t in _ts:
        for _tp in _t.templates:
            if not getattr(_tp, '_tidy', False):
                _tp.fn = _wrap(_tp.fn)
                _tp._tidy = True
