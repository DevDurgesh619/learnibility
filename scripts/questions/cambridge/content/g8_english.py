"""Cambridge Lower Secondary English 0861, Stage 9 (grade 8).

Reading fiction and non-fiction, poetry, drama, life writing, media and language accuracy. Checkpoint
pattern: Paper 1 non-fiction, Paper 2 fiction (each a reading section plus a writing task).

Every passage, poem, playscript, sentence and title here is an original text written for this bank.
Items are built by combining a text (or a short quotation from it) with a question frame:
C1 retrieval / terminology MCQs, C2 explain the effect of a word or technique, C3 apply (identify and
analyse, rewrite, summarise), C4 extended writing (level-marked) and multi-part reading items.
The shared machinery (Text, feature templates, writing-task keys) is reused by g10_english.py.
"""
import re

from ._lib import topic, mcq, compose, person, city, two_people, CTX  # noqa: F401
from core import MARKS

PROFILE = {'mark_scale': {'long': (2.5, 3)}, 'wordy': True}
CHAPTERS = {}


# =========================================================== shared helpers

_OPEN_Q = re.compile(r"(^|[\s(—–-])'")
_CLOSE_Q = re.compile(r"'(?=[\s,.!?;:)—–-]|$)")


def dq(s):
    """Turn straight single dialogue quotes into curly double quotes (apostrophes inside words are kept)."""
    if "'" not in s:
        return s
    s = _OPEN_Q.sub(lambda m: m.group(1) + '“', s)
    s = _CLOSE_Q.sub('”', s)
    return s.replace("'", '’')


def Q(s):
    return f'‘{dq(s)}’'


def clean(s):
    return re.sub(r'\s+', ' ', s).strip()


def cap(s):
    return s[:1].upper() + s[1:]


def mk(C, D, typ=None, profile=None):
    """Marks the generator will give a (C, D) cell of this type (used to size keys)."""
    profile = profile or PROFILE
    m = MARKS.get((C, D), (2, 2))[0]
    sc = profile.get('mark_scale', {}).get(typ) if typ else None
    # A mock section or a strict practice form asks for a specific total: size the key to it.
    want = CTX.get('want_marks')
    if want and want != m and not typ:
        return want
    return max(1, round(m * sc[0])) if sc else m


def upto(m):
    return f'Award up to {m} mark' + ('' if m == 1 else 's') + ' from'


def keypts(s):
    """A points-based key sized to the marks the generator is about to give this item."""
    s = re.sub(r'(?:^|(?<=; ))1 mark(?: each)?: ', '', s)
    s = re.sub(r'(?:a )?further marks? for ', 'credit for ', s)
    return f"{upto(CTX.get('want_marks') or 2)}: {s}"


def bands(n):
    """Lower, middle and top mark bands for n marks, as text."""
    a, b = n // 3, (2 * n) // 3

    def rg(x, y):
        return str(y) if x >= y else f'{x}–{y}'
    return rg(1, max(1, a)), rg(a + 1, max(a + 1, b)), rg(b + 1, n)


STYLE = ('precise, often ambitious vocabulary chosen for effect; a wide range of sentence structures used deliberately; register consistently suited to audience and purpose; spelling, punctuation and grammar almost always accurate',
         'generally appropriate vocabulary with some ambition; some variety of sentence structure; register mostly suitable; occasional errors that do not obscure meaning',
         'simple or repetitive vocabulary; limited sentence variety; register may slip; frequent errors in spelling, punctuation or grammar that sometimes obscure meaning')

CONTENT = {
    'narrative': ('an engaging, well-developed story with a clear, controlled structure; convincing characters and setting; tension or interest sustained; an effective ending',
                  'a clear story with some development of character and setting; structure mostly secure but pace may be uneven',
                  'a simple sequence of events with little development; structure unclear or ending abrupt'),
    'opening': ('setting, character and tension all established quickly and subtly; a strong hook; detail selected to raise questions the reader wants answered',
                'setting and character introduced with some effective detail; some attempt to create interest or tension',
                'a basic introduction that tells rather than shows; little sense of setting or tension'),
    'descriptive': ('a vivid, coherent picture built through carefully selected sensory detail and imagery; strong atmosphere; deliberate shifts of focus give structure',
                    'a clear description with some effective detail and imagery; some atmosphere; may drift into narrative',
                    'a list-like description with limited detail and little atmosphere; may turn into a story'),
    'argument': ('a clear, sustained point of view; well-developed reasons supported by evidence; counter-arguments anticipated and rebutted; logical, cohesive paragraphs and a strong conclusion',
                 'a clear view with some supporting reasons and evidence; some development; paragraphs mostly logical',
                 'a simple view with few or undeveloped reasons; limited organisation'),
    'discursive': ('both sides explored fairly and in depth with evidence; points weighed against each other; a reasoned judgement reached in the conclusion; cohesive paragraphing',
                   'both sides covered with some development; structure clear though weighing of points is limited',
                   'mainly one side or a list of points; little development or evaluation'),
    'speech': ('a clear purpose and point of view; strong, consistent sense of audience; rhetorical devices used purposefully; well-signposted structure with an effective opening and ending',
               'clear purpose with some awareness of audience; some rhetorical devices; structure mostly clear',
               'purpose unclear; little sense of a listening audience; few devices; loosely organised'),
    'explanation': ('a clear, accurate and logically sequenced explanation; technical vocabulary used correctly; cohesive devices link causes and effects; helpful organisation (paragraphs, subheadings)',
                    'a mostly clear explanation in a sensible order; some technical vocabulary; some linking of cause and effect',
                    'an unclear or incomplete explanation; little technical vocabulary; steps not linked'),
    'report': ('all key facts (who, what, where, when, why, how) in an effective lead; inverted-pyramid structure; quotations used well; objective tone and a headline suited to the audience',
               'most key facts covered; recognisable report structure; some quotation; tone mostly objective',
               'facts incomplete or disordered; little sense of report form; tone personal or inconsistent'),
    'article': ('an engaging headline and opening; content well chosen for the stated audience; clear angle with developed points, examples and quotations; effective ending',
                'suitable content for the audience with some development; recognisable article features',
                'limited content; little sense of audience or article form'),
    'recount': ('a vivid, selective account with a clear chronology; reflection on the significance of the experience woven in; a distinctive personal voice',
                'a clear account with some detail and some reflection; personal voice present',
                'a list of events with little detail or reflection'),
    'script': ('correct playscript layout throughout; dialogue reveals character and motivation and builds tension; stage directions purposeful; a clear shape to the scene',
               'mostly correct layout; dialogue gives some sense of character; some stage directions; scene has a beginning and end',
               'layout often incorrect; dialogue flat or confusing; few stage directions'),
    'letter': ('form and register fully appropriate (greeting, purpose stated early, sign-off); points developed and well ordered; tone consistently suited to the reader',
               'recognisable letter form; points clear with some development; tone mostly suitable',
               'form inconsistent; points brief or unclear; tone unsuited to the reader'),
    'summary': ('all or nearly all relevant points identified; expressed concisely in own words; well organised and within the word limit',
                'most relevant points; mostly own words; some repetition or unnecessary detail',
                'few relevant points; much copying or irrelevant detail; may exceed the limit'),
}

READING = ('perceptive, well-developed analysis of how the writer uses language and structure to create effects; precise, well-chosen references; sustained focus on the question',
           'clear explanation of some effects with relevant references; some analysis of particular words and phrases',
           'some relevant points, mostly retelling the text; few references; little comment on language')

WORDS = {1: '120–150', 2: '150–200', 3: '250–350', 4: '350–450', 5: '450–600'}


def levels_key(m, genre, indicative, style=STYLE, split=0.6):
    a = max(1, round(m * split))
    b = m - a
    c = CONTENT[genre] if isinstance(genre, str) else genre
    lo, mi, hi = bands(a)
    out = (f'Level-marked out of {m}: Content and structure {a} marks, Style and accuracy {b} marks. '
           f'Content and structure – top band ({hi}): {c[0]}; middle band ({mi}): {c[1]}; lower band ({lo}): {c[2]}. ')
    if b:
        slo, smi, shi = bands(b)
        out += f'Style and accuracy – top band ({shi}): {style[0]}; middle band ({smi}): {style[1]}; lower band ({slo}): {style[2]}. '
    return out + f'Indicative content: {indicative}'


def reading_key(m, indicative):
    lo, mi, hi = bands(m)
    return (f'Level-marked out of {m} (reading). Top band ({hi}): {READING[0]}; middle band ({mi}): {READING[1]}; lower band ({lo}): {READING[2]}. '
            f'Indicative content: {indicative}')


def wtask(D, stem, genre, indicative, model, C='C4', profile=None, words=True):
    m = mk(C, D, 'long', profile)
    w = f' Write about {WORDS.get(D, "250–350")} words.' if words else ''
    return {'stem': clean(stem) + w, 'answer': model, 'key': levels_key(m, genre, indicative), 'type': 'long'}


def points_key(m, points, extra=''):
    """Point-marked key: up to m marks from the listed points."""
    return f'Award 1 mark per valid point, up to {m}: ' + '; '.join(points) + '.' + (f' {extra}' if extra else '')


# ---------------------------------------------------------------- technique definitions

DEF = {
    'simile': 'a comparison using ‘like’ or ‘as’',
    'metaphor': 'a comparison that says one thing is another',
    'personification': 'giving human qualities or actions to something non-human',
    'alliteration': 'repetition of the same consonant sound at the start of nearby words',
    'sibilance': 'repetition of soft ‘s’ or ‘sh’ sounds',
    'assonance': 'repetition of vowel sounds in nearby words',
    'onomatopoeia': 'a word that imitates the sound it describes',
    'repetition': 'repeating a word, phrase or structure for emphasis',
    'short sentence': 'a deliberately brief sentence that stands out',
    'rhetorical question': 'a question asked for effect, not to get an answer',
    'hyperbole': 'deliberate exaggeration',
    'pathetic fallacy': 'weather or setting that reflects a mood or feeling',
    'contrast': 'placing opposite ideas or images side by side',
    'irony': 'saying one thing while meaning, or revealing, the opposite',
    'listing': 'a series of items piled up one after another',
    'rule of three': 'a group of three words, phrases or ideas for emphasis',
    'emotive language': 'words chosen to stir the reader’s feelings',
    'direct address': 'speaking directly to the reader as ‘you’',
    'statistic': 'a number or figure used as evidence',
    'imperative': 'a command verb that tells the reader to act',
    'anecdote': 'a short personal story used to support a point',
    'inclusive pronoun': '‘we’, ‘us’ or ‘our’ used to put the writer and reader on the same side',
    'expert opinion': 'the view of an authority used as evidence',
    'counter-argument': 'an opposing view raised so that it can be answered',
    'enjambment': 'a sentence running on from one line of poetry to the next without punctuation',
    'caesura': 'a pause or break in the middle of a line of poetry',
    'rhyming couplet': 'two consecutive lines that rhyme',
    'internal rhyme': 'rhyme within a single line',
    'foreshadowing': 'a hint of what will happen later',
    'flashback': 'a scene that moves back in time to earlier events',
    'cliffhanger': 'ending a section at a moment of suspense',
    'semantic field': 'a group of words linked by a common topic',
    'colloquial language': 'informal, everyday speech',
    'pun': 'a play on words with more than one meaning',
    'oxymoron': 'two contradictory words placed together',
    'sensory imagery': 'description that appeals to the senses',
    'dialogue': 'the words characters speak to each other',
    'ellipsis': 'three dots showing a pause, hesitation or missing words',
}

IMAGERY = ['simile', 'metaphor', 'personification', 'pathetic fallacy', 'hyperbole', 'oxymoron', 'onomatopoeia']
SOUND = ['alliteration', 'sibilance', 'assonance', 'onomatopoeia', 'internal rhyme', 'rhyming couplet', 'repetition']
NARR = ['simile', 'metaphor', 'personification', 'repetition', 'short sentence', 'pathetic fallacy', 'contrast', 'irony', 'listing', 'hyperbole']
PERSUADE = ['rhetorical question', 'emotive language', 'rule of three', 'direct address', 'statistic', 'imperative', 'anecdote', 'inclusive pronoun', 'expert opinion', 'hyperbole', 'counter-argument', 'metaphor']


class Feat:
    __slots__ = ('text', 'quote', 'device', 'focus', 'effect', 'also')

    def __init__(self, text, quote, device, focus, effect, also=()):
        self.text, self.quote, self.device, self.focus, self.effect, self.also = text, quote, device, focus, effect, tuple(also)


class Text:
    """An original passage with annotated retrieval, inference and technique items."""
    ALL = {}

    def __init__(self, pid, kind, label, text, poem=False, title=''):
        self.id, self.kind, self.label, self.poem, self.title = pid, kind, label, poem, title
        if poem:
            self.lines = [ln.strip() for ln in text.strip().split('\n') if ln.strip()]
            self.text = dq(' / '.join(self.lines))
        else:
            self.text = dq(clean(text))
        self.feats, self.rets, self.infs, self.foci = [], [], [], []
        Text.ALL[pid] = self

    def _chk(self, quote):
        assert dq(quote) in self.text, (self.id, quote)

    def f(self, quote, device, focus, effect, also=()):
        self._chk(quote)
        assert focus in quote, (self.id, focus)
        assert device in DEF, device
        self.feats.append(Feat(self, quote, device, focus, effect, also))
        return self

    def r(self, quote, question, answer, ds):
        self._chk(quote)
        self.rets.append((quote, question, answer, ds))
        return self

    def i(self, quote, question, answer, key):
        self._chk(quote)
        self.infs.append((quote, question, answer, key))
        return self

    def x(self, task, indicative):
        self.foci.append((task, indicative))
        return self

    def where(self):
        return self.label

    def body(self):
        return self.text


# ---------------------------------------------------------------- generic templates over texts

def ret_items(texts):
    out = []
    for T in texts:
        for quote, question, answer, ds in T.rets:
            out.append((f'Read this from {T.label}: {Q(quote)} {question}', answer,
                        f'Retrieval: the answer is stated in the quotation ({Q(quote)}).', ds))
    return out


def inf_items(texts):
    out = []
    for T in texts:
        for quote, question, answer, key in T.infs:
            out.append((f'In {T.label} the writer writes: {Q(quote)} {question}', answer, key))
    return out


C1F = ['Which technique is used in this line from {src}? {q}',
       'Read {q} ({src}). Which language feature does the writer use here?']
C2F = ['Explain the effect of the words {f} in this line from {src}: {q}',
       'In {src} the writer uses the {dev} {f}: {q} Explain what it suggests to the reader.',
       '{q} ({src}). What does the phrase {f} suggest, and how might it make the reader feel?']
C2F_WHOLE = ['Explain the effect of this line from {src}: {q}',
             'In {src} the writer uses {dev} in the line {q} Explain what it suggests to the reader.',
             '{q} ({src}). What does this line suggest, and how might it make the reader feel?']
C3F = ['Identify the technique used in {q} ({src}) and analyse its effect on the reader.',
       'Read {q} from {src}. Name the language feature, quote the key words and explain how they shape the reader’s response.']


def c2_key(m, focus, effect):
    pts = [f'1 for an accurate meaning or connotation of {Q(focus)}', '1 for the effect on the reader, mood or idea created',
           '1 for a developed point that explores a second connotation or links to the wider text']
    return f'{upto(m)}: ' + '; '.join(pts[:max(1, m)]) + f'. Model point: {effect} Credit any valid interpretation supported by the words.'


def feature_templates(t, feats, pool, c1=True, c2=True, c3=True, c3_pairs=True):
    """Register C1 identify / C2 explain / C3 analyse templates over a list of Feat."""
    feats = list(feats)
    if not feats:
        return

    if c1:
        @t.add('C1', (1, 2, 3))
        def feat_c1(r, D):
            f = r.choice(feats)
            ds = [d for d in pool if d != f.device and d not in f.also]
            opts, ans = mcq(r, cap(f.device), [cap(d) for d in ds])
            stem = r.choice(C1F).format(q=Q(f.quote), src=f.text.label)
            return {'stem': stem, 'options': opts, 'answer': ans,
                    'key': f'{cap(f.device)}: {DEF[f.device]}. Here {Q(f.focus)} – {f.effect}'}

    if c2:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def feat_c2(r, D):
            f = r.choice(feats)
            whole = f.focus.strip(' .,') == f.quote.strip(' .,')
            frames = C2F_WHOLE if whole else C2F
            stem = r.choice(frames).format(q=Q(f.quote), src=f.text.label, f=Q(f.focus), dev=f.device)
            return {'stem': stem, 'answer': f.effect, 'key': c2_key(mk('C2', D), f.focus, f.effect)}

    if c3:
        @t.add('C3', (2, 3, 4, 5), 'explain')
        def feat_c3(r, D):
            m = mk('C3', D)
            same = [g for g in feats if g.text is not None]
            if D >= 4 and c3_pairs:
                f = r.choice(same)
                others = [g for g in feats if g.text is f.text and g is not f]
                if others:
                    g = r.choice(others)
                    stem = (f'Analyse how the writer uses language in these two quotations from {f.text.label}: '
                            f'(i) {Q(f.quote)} (ii) {Q(g.quote)} Identify a technique in each and explain its effect.')
                    ans = f'(i) {cap(f.device)}: {f.effect} (ii) {cap(g.device)}: {g.effect}'
                    key = (f'{upto(m)}: for each quotation, 1 for the technique ({f.device}; {g.device}) and 1 for an explanation of its effect; '
                           'remaining mark(s) for a developed point linking both to the mood or purpose of the text.')
                    return {'stem': stem, 'answer': ans, 'key': key}
            f = r.choice(feats)
            stem = r.choice(C3F).format(q=Q(f.quote), src=f.text.label)
            ans = f'{cap(f.device)} ({Q(f.focus)}): {f.effect}'
            key = (f'{upto(m)}: 1 for naming the technique ({f.device}); 1 for selecting the key words {Q(f.focus)}; '
                   f'remaining mark(s) for analysis of the effect, e.g. {f.effect}')
            return {'stem': stem, 'answer': ans, 'key': key}


def text_parts(T, extended=True):
    """Parts for compose() from one text: retrieval [1], inference [2], technique [3], extended [6]."""
    parts = []
    if T.rets:
        def p_ret(r):
            quote, question, answer, _ = r.choice(T.rets)
            return (question, answer, f'1 mark: {answer} [1]')
        parts.append(p_ret)
    if T.infs:
        def p_inf(r):
            quote, question, answer, key = r.choice(T.infs)
            return (f'Look at {Q(quote)}. {question}', answer, f'{key} [2]')
        parts.append(p_inf)
    if T.feats:
        def p_feat(r):
            f = r.choice(T.feats)
            return (f'The writer writes {Q(f.quote)}. Identify the technique and explain its effect.', f'{cap(f.device)}: {f.effect}',
                    f'1 mark technique ({f.device}); 2 marks explanation of effect, e.g. {f.effect} [3]')
        parts.append(p_feat)
    if extended and T.foci:
        def p_ext(r):
            task, ind = r.choice(T.foci)
            return (task, ind, f'Level-marked: top band (5–6) perceptive analysis with precise references; middle (3–4) clear explanation of some effects; lower (1–2) mainly retelling. [6]')
        parts.append(p_ext)
    return parts


def build_parts(r, intro, built, type_='multi_step'):
    """Format already-built parts (text, answer, key-with-[n]) as one structured question."""
    from ._lib import _part_marks, LETTERS
    tot = sum(_part_marks(k) for _, _, k in built)
    if len(built) == 1:
        t_, a, k = built[0]
        q = {'stem': intro.strip() + ' ' + t_, 'answer': a, 'key': k}
    else:
        q = {'stem': intro.strip() + ' ' + ' '.join(f'({LETTERS[j]}) {t_}' for j, (t_, _, _) in enumerate(built)),
             'answer': ' '.join(f'({LETTERS[j]}) {a}' for j, (_, a, _) in enumerate(built)),
             'key': ' '.join(f'({LETTERS[j]}) {k}' for j, (_, _, k) in enumerate(built))}
    q['marks'] = max(1, min(20, tot))
    q['minutes'] = round(max(1.0, q['marks'] * 1.25) * 2) / 2
    q['type'] = type_
    return q


def text_compose(r, T, extended=True):
    intro = f'Read {T.label}. {Q(T.text)}'
    if extended and T.foci:
        from ._lib import _part_marks
        short = text_parts(T, extended=False)
        n = r.choice([1, 2, 2, 3]) if len(short) >= 2 else len(short)
        idx = sorted(r.sample(range(len(short)), min(n, len(short))))
        built = [short[i](r) for i in idx]
        # the extended part takes whatever the requested total leaves (at least 4, at most 12)
        want = CTX.get('want_marks') or 0
        rest = want - sum(_part_marks(k) for _, _, k in built)
        while rest < 4 and built and want:
            built.pop()
            rest = want - sum(_part_marks(k) for _, _, k in built)
        em = rest if want and 4 <= rest <= 12 else 6
        task, ind = r.choice(T.foci)
        lo, mi, hi = bands(em)
        built.append((task, ind, f'Level-marked: top band ({hi}) perceptive analysis with precise references; middle ({mi}) clear explanation of some effects; '
                                 f'lower ({lo}) mainly retelling. [{em}]'))
        return build_parts(r, intro, built)
    return compose(r, intro, text_parts(T, extended), k=(2, 3, 4), type_='multi_step')


def compose_templates(t, texts, C=('C3', 'C4'), D3=(3, 4, 5), D4=(2, 3, 4, 5)):
    texts = [T for T in texts]

    if 'C3' in C:
        @t.add('C3', D3, 'multi_step')
        def text_c3(r, D):
            return text_compose(r, r.choice(texts), extended=False)

    if 'C4' in C and any(T.foci for T in texts):
        @t.add('C4', D4, 'multi_step')
        def text_c4(r, D):
            return text_compose(r, r.choice([T for T in texts if T.foci]), extended=True)


def extended_templates(t, texts, C='C4', D=(2, 3, 4, 5)):
    """Single extended reading response on a whole text (one per focus)."""
    texts = [T for T in texts if T.foci]

    @t.add(C, D, 'long')
    def text_ext(r, D_):
        T = r.choice(texts)
        task, ind = r.choice(T.foci)
        m = mk(C, D_, 'long')
        return {'stem': f'Read {T.label}. {Q(T.text)} {task} Support your answer with close reference to the text.',
                'answer': ind, 'key': reading_key(m, ind), 'type': 'long'}


def classify_templates(t, items, pool, frames, C2frames=None, C3frames=None, key_fmt='{label}: {why}'):
    """items: (text, label, why). C1 MCQ classify; optional C2 explain; optional C3 apply frames.

    C3frames: list of (frame, answer_fn(item) -> str, key_fn(item, m) -> str)."""
    items = list(items)

    @t.add('C1', (1, 2, 3))
    def cls_c1(r, D):
        text, label, why = r.choice(items)[:3]
        ds = [p for p in pool if p != label]
        opts, ans = mcq(r, label, ds)
        return {'stem': r.choice(frames).format(q=Q(text)), 'options': opts, 'answer': ans, 'key': key_fmt.format(label=cap(label), why=why)}

    if C2frames:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def cls_c2(r, D):
            text, label, why = r.choice(items)[:3]
            m = mk('C2', D)
            return {'stem': r.choice(C2frames).format(q=Q(text), label=label), 'answer': f'{cap(label)}: {why}',
                    'key': f'{upto(m)}: 1 for identifying {label}; further mark(s) for explaining the effect or clue: {why}'}

    if C3frames:
        @t.add('C3', (2, 3, 4, 5), 'explain')
        def cls_c3(r, D):
            it = r.choice(items)
            frame, afn, kfn = r.choice(C3frames)
            res = afn(it)
            if res is None:
                return None
            return {'stem': frame.format(q=Q(it[0]), label=it[1]), 'answer': res, 'key': kfn(it, mk('C3', D))}


def rewrite_templates(t, items, frames, C='C3', D=(1, 2, 3, 4), typ='explain'):
    """items: (instruction, original, model, key-note). C3 rewrite/edit tasks."""
    items = list(items)

    @t.add(C, D, typ)
    def rw(r, D_):
        ins, orig, model, note = r.choice(items)
        m = mk(C, D_)
        return {'stem': r.choice(frames).format(ins=ins, q=Q(orig)), 'answer': model,
                'key': f'{upto(m)}: {note} Accept any version that meets the instruction and keeps the meaning; deduct for new errors.'}


def writing_templates(t, tasks, genre, C='C4', D=(2, 3, 4, 5), profile=None):
    """tasks: list of (stem, indicative, model). One long writing item per task (+ word-count by D)."""
    tasks = list(tasks)

    @t.add(C, D, 'long')
    def wr(r, D_):
        stem, ind, model = r.choice(tasks)
        return wtask(D_, stem, genre, ind, model, C=C, profile=profile)


# =========================================================== Unit 1 Narrative fiction: openings, viewpoint, character

FERRY = Text('ferry', 'fiction', 'the opening of a story, ‘The Last Ferry’', """
The last ferry of the season left without Mira. She reached the jetty in time to see its lights shrink across the black
water, and for a long moment she simply stood there, her suitcase leaning against her leg like a tired dog. The ticket
office was shuttered. A single gull picked at a crust beside the bins, unbothered. Behind her, the town climbed the hill
in crooked steps, every window dark except one, high up near the church, where a lamp burned yellow and steady. Mira
checked her phone again. No signal, just as there had been none since the bus crossed the bridge. Her aunt had promised
to meet her. Her aunt had promised a great many things. She picked up the suitcase, turned towards the single light, and
began to climb.""")
FERRY.r('She reached the jetty in time to see its lights shrink across the black water', 'Where is Mira when the story begins?',
        'At the jetty, just after the ferry has left', ['On the ferry, crossing the water', 'At her aunt’s house', 'At the church on the hill', 'At the bus station by the bridge'])
FERRY.r('The ticket office was shuttered.', 'What does ‘shuttered’ tell you about the ticket office?', 'It was closed up',
        ['It was crowded with passengers', 'It had been damaged by a storm', 'It was brightly lit', 'It was selling the last tickets'])
FERRY.r('Mira checked her phone again. No signal, just as there had been none since the bus crossed the bridge.', 'Why can Mira not phone for help?',
        'There is no phone signal', ['Her battery has run out', 'She has lost her phone', 'Her aunt has no phone', 'The ticket office has her phone'])
FERRY.r('every window dark except one, high up near the church, where a lamp burned yellow and steady', 'Which part of the town is lit?',
        'One window high up near the church', ['Every window in the town', 'The ticket office', 'The jetty', 'The bins beside the gull'])
FERRY.i('Her aunt had promised to meet her. Her aunt had promised a great many things.', 'What does this suggest about Mira’s feelings towards her aunt?',
        'It suggests Mira does not fully trust her aunt. The repetition of ‘promised’ and the phrase ‘a great many things’ imply the aunt often breaks her word, so Mira is disappointed but not surprised.',
        '1 mark: inference (distrust, disappointment, aunt is unreliable); 1 mark: supported by the repetition of ‘promised’ or ‘a great many things’; a further mark for noting the weary, unsurprised tone')
FERRY.i('for a long moment she simply stood there', 'What does this suggest about how Mira reacts to missing the ferry?',
        'She is stunned and does not know what to do; ‘simply stood’ and ‘a long moment’ show she is frozen by shock or disappointment.',
        '1 mark: shock/uncertainty/defeat; 1 mark: reference to ‘simply stood’ or ‘long moment’')
FERRY.i('A single gull picked at a crust beside the bins, unbothered.', 'Why might the writer include the detail of the gull?',
        'The gull is calm and ‘unbothered’, which contrasts with Mira’s difficult situation and emphasises how alone she is: nobody else in the scene cares.',
        '1 mark: contrast with Mira’s distress or emphasis on emptiness; 1 mark: explanation using ‘single’ or ‘unbothered’')
FERRY.i('She picked up the suitcase, turned towards the single light, and began to climb.', 'What does this final sentence suggest about Mira’s character?',
        'She is determined and practical: instead of giving up she makes a decision and acts. Climbing towards the light suggests hope and courage.',
        '1 mark: determined/resourceful/brave; 1 mark: evidence from the sequence of actions or the light as hope')
FERRY.f('her suitcase leaning against her leg like a tired dog', 'simile', 'like a tired dog',
        'the suitcase seems like a weary companion; it reflects Mira’s own exhaustion and loneliness, since her luggage is her only company.', also=('personification',))
FERRY.f('Her aunt had promised to meet her. Her aunt had promised a great many things.', 'repetition', 'Her aunt had promised',
        'repeating the phrase stresses how often the aunt has made promises, creating a bitter, sceptical tone and hinting she cannot be relied on.')
FERRY.f('The ticket office was shuttered.', 'short sentence', 'The ticket office was shuttered.',
        'the abrupt sentence closes off one more option, emphasising Mira’s isolation and the finality of being stranded.')
FERRY.f('the town climbed the hill in crooked steps', 'personification', 'climbed',
        'the town seems to be making an effort, like a person, suggesting a steep, uneven, old place and hinting at the hard climb Mira faces.')
FERRY.f('every window dark except one, high up near the church, where a lamp burned yellow and steady', 'contrast', 'dark except one',
        'the single lit window stands out against the darkness like a beacon, drawing Mira (and the reader) towards it and suggesting hope or mystery.')
FERRY.x('How does the writer create a sense of isolation in this opening?', 'Missing the last ferry; shuttered office; no signal; ‘single’ gull and light; dark windows; the unreliable aunt; the climb alone. Effects of short sentences, repetition and contrast.')
FERRY.x('What impressions of Mira does the writer create, and how?', 'Lonely and let down (simile of the tired dog, repetition of ‘promised’), but determined (final sequence of verbs ‘picked up… turned… began to climb’).')

GREENHOUSE = Text('greenhouse', 'fiction', 'the opening of a story, ‘Nobody Believes Me’', """
I want to make it clear from the start that I did not break the greenhouse. Everyone in our street thinks I did,
including my mother, who has known me for thirteen years and should frankly know better. Yes, I was in the garden. Yes,
I had the cricket bat. And yes, the ball did happen to be lying among the broken glass when Mr Okoro came running out in
his slippers. But anyone who has studied physics, which I have, for nearly a whole term, knows that a ball cannot travel
that far on its own. Someone else was involved. Possibly a fox. I explained all this to Mr Okoro, calmly and reasonably,
while he made a noise like a kettle coming to the boil.""")
GREENHOUSE.r('I did not break the greenhouse', 'What does the narrator insist they did not break?', 'The greenhouse',
             ['A window in the house', 'The cricket bat', 'Mr Okoro’s slippers', 'The garden fence'])
GREENHOUSE.r('Yes, I had the cricket bat.', 'What was the narrator holding?', 'A cricket bat', ['A football', 'A tennis racket', 'A garden hose', 'Nothing at all'])
GREENHOUSE.r('when Mr Okoro came running out in his slippers', 'Who came running out?', 'Mr Okoro, in his slippers', ['The narrator’s mother', 'A fox', 'A police officer', 'The narrator’s physics teacher'])
GREENHOUSE.r('which I have, for nearly a whole term', 'How long has the narrator studied physics?', 'Nearly a whole term',
             ['Thirteen years', 'Several years', 'One week', 'Since primary school'])
GREENHOUSE.i('Yes, I was in the garden. Yes, I had the cricket bat. And yes, the ball did happen to be lying among the broken glass',
             'How does this make the reader doubt the narrator?',
             'The narrator admits every piece of evidence against them; the repeated ‘Yes’ builds a list of facts that all point to their guilt, and ‘did happen to be’ sounds evasive.',
             '1 mark: the evidence points to guilt / narrator is unreliable; 1 mark: reference to the repeated ‘Yes’ or the evasive ‘did happen to be’')
GREENHOUSE.i('which I have, for nearly a whole term', 'What does this reveal about the narrator?',
             'The narrator is over-confident and exaggerates their expertise; ‘nearly a whole term’ is a tiny amount of study, which makes their claim comic.',
             '1 mark: over-confident/boastful/naive; 1 mark: explains the humour of ‘nearly a whole term’')
GREENHOUSE.i('while he made a noise like a kettle coming to the boil', 'What does this suggest about Mr Okoro’s mood?',
             'He is furious and his anger is building up, about to explode; the narrator’s comparison is dismissive and comic.',
             '1 mark: anger rising; 1 mark: explanation of the kettle image')
GREENHOUSE.f('Yes, I was in the garden. Yes, I had the cricket bat.', 'repetition', 'Yes',
             'the repeated ‘Yes’ sounds like a reluctant confession, piling up evidence and making the reader suspect the narrator is guilty.')
GREENHOUSE.f('while he made a noise like a kettle coming to the boil', 'simile', 'like a kettle coming to the boil',
             'Mr Okoro’s anger is shown as a rising whistle about to explode; the domestic image is comic and shows the narrator does not take him seriously.')
GREENHOUSE.f('Someone else was involved. Possibly a fox.', 'short sentence', 'Possibly a fox.',
             'the brief, absurd suggestion lands like a punchline; it exposes how desperate and ridiculous the narrator’s excuse is.')
GREENHOUSE.f('I explained all this to Mr Okoro, calmly and reasonably,', 'irony', 'calmly and reasonably',
             'the narrator presents themself as rational, but the reader sees the explanation is nonsense, so the claim is ironic and comic.')
GREENHOUSE.x('How does the writer make the narrator seem unreliable and humorous?', 'Admits all the evidence; repetition of ‘Yes’; exaggerated expertise; absurd fox excuse; ironic ‘calmly and reasonably’; mocking simile about Mr Okoro.')

STALL = Text('stall', 'fiction', 'an extract from a story, ‘The Radio Mender’', """
Dada Farouk's stall was the smallest in the market, but people queued for it anyway. He sat on an upturned crate,
sleeves rolled to the elbow, mending radios with fingers as quick and careful as a bird building a nest. He never
hurried and never apologised for not hurrying. 'A thing done fast is a thing done twice,' he told a customer who tapped
his watch. When a boy came up clutching a cracked phone and a fistful of coins, Dada Farouk looked at the coins, then at
the boy's worn shoes, and pushed the money back across the counter. 'Pay me when you are rich,' he said, already
unscrewing the case. The boy opened his mouth to argue. Dada Farouk raised one grey eyebrow, and the boy closed it again.""")
STALL.r('people queued for it anyway', 'How do people react to Dada Farouk’s stall?', 'They queue for it even though it is small',
        ['They avoid it because it is small', 'They complain about his prices', 'They only visit when other stalls are shut', 'They steal radios from it'])
STALL.r("When a boy came up clutching a cracked phone and a fistful of coins", 'What does the boy bring to the stall?', 'A cracked phone and a handful of coins',
        ['A broken radio and a watch', 'A pair of worn shoes', 'A crate and a screwdriver', 'Nothing except a question'])
STALL.r("'Pay me when you are rich,' he said", 'What does Dada Farouk tell the boy?', 'To pay him when he is rich',
        ['To come back tomorrow', 'To pay double', 'To find another stall', 'To fix the phone himself'])
STALL.i("He never hurried and never apologised for not hurrying.", 'What does this suggest about Dada Farouk?',
        'He is calm, confident and sure of his own methods; he will not be pressured by impatient customers.',
        '1 mark: calm/confident/stubborn; 1 mark: explained with ‘never apologised’')
STALL.i("looked at the coins, then at the boy's worn shoes, and pushed the money back across the counter", 'What do Dada Farouk’s actions show about him?',
        'He is observant and kind: he notices the boy is poor (worn shoes) and generously refuses payment without making a fuss.',
        '1 mark: generous/kind/observant; 1 mark: reference to looking at the shoes or pushing the money back')
STALL.i("Dada Farouk raised one grey eyebrow, and the boy closed it again.", 'What does this moment reveal about the relationship between Dada Farouk and the boy?',
        'Dada Farouk has quiet authority; a single small gesture is enough to stop the boy arguing, so the boy respects him.',
        '1 mark: authority/respect; 1 mark: the smallness of the gesture (‘one’ eyebrow) shows how much power he has')
STALL.f('mending radios with fingers as quick and careful as a bird building a nest', 'simile', 'as quick and careful as a bird building a nest',
        'his hands are skilful, delicate and patient; the natural image suggests his work is instinctive and gentle.')
STALL.f("'A thing done fast is a thing done twice,'", 'repetition', 'a thing done',
        'the balanced, repeated structure sounds like a proverb, showing his wisdom and his belief in doing work properly.')
STALL.f("Dada Farouk's stall was the smallest in the market, but people queued for it anyway.", 'contrast', 'the smallest in the market, but people queued',
        'the contrast between the tiny stall and the queue shows that his reputation and skill matter more than appearances.')
STALL.x('How does the writer present Dada Farouk as a character?', 'Skilled (bird simile), patient and confident (never hurried), wise (proverb), generous and observant (worn shoes, pushes coins back), respected (queue, eyebrow). Methods: description, dialogue, action, reactions of others.')

CAPTAIN = Text('captain', 'fiction', 'an extract from a story, ‘The New Captain’', """
Coach Adeyemi blew the whistle so hard that a pigeon left the roof. 'Captain,' she said, and pointed at Lena. A murmur
ran round the changing room. Lena was not the fastest player, nor the loudest; that was Rosa, who was now examining her
boots with great concentration. Lena stood up slowly. 'Me?' 'You,' said the coach. 'You're the only one who passes the
ball when you could shoot.' Rosa snorted. Lena felt her face burn, but she crossed the room, sat down beside Rosa and said
quietly, 'I'll need you up front on Saturday. Nobody scores like you.' Rosa looked up. For a second she said nothing.
Then, very slightly, she nodded.""")
CAPTAIN.r("'Captain,' she said, and pointed at Lena.", 'Who is chosen as captain?', 'Lena', ['Rosa', 'Coach Adeyemi', 'The fastest player', 'Nobody'])
CAPTAIN.r("'You're the only one who passes the ball when you could shoot.'", 'Why does the coach choose Lena?', 'She passes the ball when she could shoot',
          ['She is the fastest player', 'She is the loudest player', 'She scores the most goals', 'She asked to be captain'])
CAPTAIN.i('Rosa, who was now examining her boots with great concentration', 'What does this suggest about Rosa’s feelings?',
          'Rosa is embarrassed or jealous because she expected to be captain; she pretends to be busy to hide her disappointment.',
          '1 mark: disappointment/jealousy/embarrassment; 1 mark: explains the pretence in ‘with great concentration’')
CAPTAIN.i("Lena felt her face burn, but she crossed the room, sat down beside Rosa", 'What does this show about Lena?',
          'Although she is embarrassed, she is brave and thoughtful: she goes straight to Rosa to include her, showing leadership.',
          '1 mark: brave/considerate/a natural leader; 1 mark: contrast between ‘face burn’ and her decisive action')
CAPTAIN.i('Then, very slightly, she nodded.', 'What does Rosa’s nod suggest?',
          'Rosa accepts Lena as captain, though reluctantly; ‘very slightly’ shows her pride is still hurt but she has been won over.',
          '1 mark: acceptance; 1 mark: reluctance shown by ‘very slightly’')
CAPTAIN.f('Coach Adeyemi blew the whistle so hard that a pigeon left the roof.', 'hyperbole', 'so hard that a pigeon left the roof',
          'the exaggeration is comic and shows the coach is forceful and commanding from the very first line.')
CAPTAIN.f("Rosa snorted.", 'short sentence', 'Rosa snorted.',
          'the blunt sentence captures Rosa’s scorn in a single sound, creating a moment of tension in the room.')
CAPTAIN.x('How does the writer show the tension between Lena and Rosa, and how it is resolved?', 'Rosa’s pretended interest in her boots; the snort; Lena’s burning face; Lena’s quiet praise ‘Nobody scores like you’; the pause and slight nod.')


# ---------------------------------------------------------------- 1.1 explicit and implicit meaning
t11 = topic('Explicit and implicit meaning in a story opening', 'explicit and implicit meaning', 'reading fiction', 'story opening')
U1_TEXTS = [FERRY, GREENHOUSE, STALL, CAPTAIN]
t11.fixed('C1', (1, 2), ret_items(U1_TEXTS))
t11.fixed('C1', (1, 2), [
    ('What is meant by implicit information in a story?', 'Information the reader must infer from clues rather than being told directly',
     'Implicit = suggested or implied; explicit = stated directly in the text.',
     ['Information stated directly in the text', 'Information found only in the title', 'Information that is untrue']),
    ('Which question asks for explicit information?', 'What time does the train leave?', 'Explicit questions can be answered by finding a stated fact; the others need inference.',
     ['Why might the narrator feel uneasy?', 'What does the setting suggest about the character’s mood?', 'How does the writer hint that something will go wrong?']),
    ('What do you do when you infer something from a text?', 'work out a meaning from the clues the writer gives', 'Inference = reading between the lines using evidence.',
     ['copy the exact words from the text', 'guess without using evidence', 'summarise the whole story']),
])
t11.fixed('C2', (2, 3), inf_items(U1_TEXTS))


@t11.add('C3', (2, 3, 4, 5), 'explain')
def t11_evidence(r, D):
    T = r.choice(U1_TEXTS)
    quote, question, answer, key = r.choice(T.infs)
    m = mk('C3', D)
    lead = r.choice(['Answer in your own words and support your answer with a short quotation.', 'Make an inference and support it with close reference to the words of the text.',
                     'Use point, evidence and explanation in your answer.'])
    return {'stem': f'Read this sentence from {T.label}: {Q(quote)} {question} {lead}',
            'answer': answer, 'key': f'{upto(m)}: point (inference) + evidence (short quotation) + explanation of how the words create that impression. {key}.'}


compose_templates(t11, U1_TEXTS)
extended_templates(t11, U1_TEXTS)

# ---------------------------------------------------------------- 1.2 viewpoint
VIEW = ['first-person narrator', 'second-person narration', 'third-person limited narrator', 'third-person omniscient narrator', 'first-person plural narrator']
VIEW_SNIP = [
    ('I pressed my ear to the door. Whatever they were arguing about, it was about me.', 'first-person narrator', 'the narrator uses ‘I’ and ‘me’, so we only know what this character hears and suspects.',
     'Kofi pressed his ear to the door. Whatever they were arguing about, he was sure it was about him.'),
    ('Kofi pressed his ear to the door. He could not make out the words, but he knew the argument was about him.', 'third-person limited narrator', 'the narrator uses ‘he’ but stays with Kofi’s thoughts only.',
     'I pressed my ear to the door. I could not make out the words, but I knew the argument was about me.'),
    ('In the kitchen, Mrs Mensah was worrying about money; upstairs, her son was listening at the door, convinced she was angry with him; neither knew that the letter on the table would solve everything.',
     'third-person omniscient narrator', 'the narrator knows the thoughts of more than one character and even what will happen next.', None),
    ('You step off the train and the heat hits you like an open oven.', 'second-person narration', 'the reader is placed inside the story as ‘you’, making the experience immediate.',
     'I stepped off the train and the heat hit me like an open oven.'),
    ('We had lived on Harbour Street for nine summers, and we thought we knew every crack in its pavements.', 'first-person plural narrator', 'the narrator speaks for a group as ‘we’, giving a shared, community voice.',
     'They had lived on Harbour Street for nine summers, and they thought they knew every crack in its pavements.'),
    ('Nobody saw Amira slip out of the hall. She told herself she only needed some air.', 'third-person limited narrator', 'the narrator uses ‘she’ and gives only Amira’s thoughts, which may be self-deceiving (‘told herself’).',
     'Nobody saw me slip out of the hall. I told myself I only needed some air.'),
    ('The villagers believed the well was cursed. The well, of course, knew nothing about it; it simply held its water in the dark, as it had for three hundred years.',
     'third-person omniscient narrator', 'an all-knowing narrator comments on the villagers’ beliefs from above and knows the well’s whole history.', None),
    ('I am not a nosy person. I just happen to notice things, such as the fact that Mr Dube’s curtains have been closed for four days, which I have written in my notebook.',
     'first-person narrator', 'the ‘I’ narrator claims not to be nosy while revealing a notebook of observations, so they are unreliable.',
     'She was not, she insisted, a nosy person. She just happened to notice things, such as the fact that Mr Dube’s curtains had been closed for four days, which she had written in her notebook.'),
    ('You open the letter. You read the first line twice. Your hands, you notice, are shaking.', 'second-person narration', '‘you’ makes the reader experience the moment directly and builds tension.',
     'I opened the letter. I read the first line twice. My hands, I noticed, were shaking.'),
    ('Tomás, who had been told the story a hundred times, could still not quite believe it.', 'third-person limited narrator', 'the narrator uses his name and ‘he’-perspective, staying close to Tomás’s reactions.',
     'I had been told the story a hundred times, and I could still not quite believe it.'),
    ('My brother always starts our fights. Today, for example, he started it by sitting in my chair, so I had no choice but to pour juice on his homework.',
     'first-person narrator', 'the ‘I’ narrator blames the brother while describing their own unfair reaction, so they are unreliable.',
     'Leo was sure his brother always started their fights. Today, for example, his brother had sat in his chair, so Leo felt he had no choice but to pour juice on his homework.'),
    ('We waited at the school gate every afternoon that winter, and every afternoon the old man walked past without looking at us.', 'first-person plural narrator',
     '‘we’ and ‘us’ give a group perspective, suggesting a shared childhood memory.', None),
]
UNRELIABLE = [
    ('I was perfectly calm during the exam. I only checked the clock forty times, and my hands were sweating because the room was warm.',
     'The narrator claims to be calm, but checking the clock ‘forty times’ and sweating hands show anxiety; the excuse about the warm room is not convincing.'),
    ('My brother always starts our fights. Today, for example, he started it by sitting in my chair, so I had no choice but to pour juice on his homework.',
     'The narrator blames the brother for a minor action while describing an extreme reaction of their own; ‘I had no choice’ is clearly untrue.'),
    ('I am not a nosy person. I just happen to notice things, such as the fact that Mr Dube’s curtains have been closed for four days, which I have written in my notebook.',
     'The narrator denies being nosy but records neighbours’ curtains in a notebook, so their self-description cannot be trusted.'),
    ('Everyone at the party adored my singing. Several people even left early so they could tell their friends about it.',
     'The narrator misreads people leaving early as praise; the reader can see the guests were probably escaping, which makes the narrator comically unreliable.'),
    ('I did not eat the last mango. I simply moved it somewhere safer, which happened to be my stomach.',
     'The narrator denies eating the mango and then admits it in a joke, revealing that their account is self-serving.'),
]
t12 = topic('Narrative viewpoint', 'narrative viewpoint', 'first person third person', 'unreliable narrators')
t12.fixed('C1', (1, 2), [
    ('A story told by a character using ‘I’ is written in which narrative perspective?', 'first person', 'First person: the narrator is a character in the story and uses ‘I’/‘me’.',
     ['second person', 'third person', 'omniscient person']),
    ('What is an omniscient narrator?', 'A narrator who knows the thoughts and feelings of all the characters', 'Omniscient = all-knowing; often third person.',
     ['A narrator who only knows one character’s thoughts', 'A narrator who is the main character', 'A narrator who speaks to the reader as ‘you’']),
    ('What is true of an unreliable narrator’s account?', 'cannot be fully trusted by the reader', 'Unreliable narrators may be biased, mistaken, lying or naive; the reader spots gaps between what is said and what happened.',
     ['is always written in the third person', 'is told entirely in dialogue', 'contains no description']),
    ('Which pronouns usually signal a third-person narrative?', 'he, she, they', 'Third person: the narrator refers to characters as he/she/they.',
     ['I, me, my', 'you, your', 'we, us, our']),
    ('What is the main limitation of a first-person narrator?', 'The reader only learns what that character knows or chooses to tell', 'A first-person view is restricted to one character’s knowledge and opinions.',
     ['The reader learns every character’s thoughts', 'The story cannot include dialogue', 'The story must be told in the present tense']),
])
classify_templates(t12, VIEW_SNIP, VIEW,
                   ['Which narrative viewpoint is used in this extract? {q}', 'Read the extract: {q} Identify the narrative viewpoint.'],
                   C2frames=['Read: {q} This extract uses a {label}. Explain one effect of this choice of viewpoint on the reader.',
                             'Explain how the choice of a {label} shapes what the reader learns in this extract: {q}'],
                   C3frames=[('Rewrite this extract using a different narrative viewpoint, then explain one thing that changes for the reader: {q}',
                              lambda it: (f'Model rewrite: {Q(it[3])} The change of viewpoint alters how close the reader is to the character’s thoughts.' if it[3] else None),
                              lambda it, m: f'{upto(m)}: 1 for consistent change of pronouns and verb forms; 1 for keeping the meaning; remaining mark(s) for explaining the effect (closeness, knowledge, reliability). Original: {it[1]}.')])
t12.fixed('C2', (2, 3, 4), [(f'Read this narrator’s account: {Q(a)} Explain why the reader might not trust this narrator.', b,
                             '1 mark: identifies the gap between what the narrator claims and what the evidence shows; 1 mark: quotes the revealing detail; a further mark for explaining the effect (humour, sympathy or suspicion).')
                            for a, b in UNRELIABLE])


@t12.add('C3', (3, 4, 5), 'explain')
def t12_unrel(r, D):
    a, b = r.choice(UNRELIABLE)
    m = mk('C3', D)
    return {'stem': f'Analyse how the writer signals that the narrator is unreliable in this extract: {Q(a)} Refer to particular words in your answer.',
            'answer': b, 'key': f'{upto(m)}: 1 for recognising unreliability; 1 per relevant word or phrase analysed; 1 for the effect on the reader (dramatic irony, humour).'}


VIEW_TASKS = [
    ('Write the greenhouse incident from ‘Nobody Believes Me’ again, this time in the first person from the point of view of Mr Okoro, the neighbour.',
     'Mr Okoro’s first-person voice: his calm evening, the crash, running out in slippers, the ridiculous fox excuse; his anger and perhaps a grudging amusement; the reader now sees the narrator from outside.',
     'Plan: (1) Mr Okoro relaxing with tea; (2) the crash of glass; (3) the scene in the garden – bat, ball, the child’s excuses; (4) his reaction and reflection. Sample opening: ‘I had just poured my tea when the sky fell in on my tomatoes.’'),
    ('Write a short story told by an unreliable first-person narrator who insists they are not jealous of their best friend’s success.',
     'Narrator’s claims of not being jealous contradicted by actions and details; reader sees the truth through clues; possible moment of self-realisation.',
     'Plan: friend wins a prize; narrator claims to be delighted but ‘accidentally’ mis-spells friend’s name on the card, leaves the celebration early etc.; ending where the mask slips.'),
    ('Write an account of a busy market morning using a third-person omniscient narrator who reveals the thoughts of at least three different characters.',
     'Moves between characters (a stallholder, a shopper, a child); reveals secret thoughts the others do not know; narrator may comment on events or hint at the future.',
     'Plan: wide opening view of the market; stallholder worried about rent; shopper hiding a secret; child who has lost a coin; narrator links them in a final moment.'),
    ('Write the first day at a new school twice, in two short sections: first from the viewpoint of the nervous new student (first person), then from a teacher watching them (third person).',
     'Two clearly different viewpoints; contrast in what each knows and feels; consistent pronouns; the second section reveals details the first narrator missed.',
     'Plan: Section 1 – ‘I’ narrator, racing thoughts, misreads a smile as mockery; Section 2 – teacher notices the student’s shaking hands and plans to help.'),
    ('Write a short story in the second person (‘you’) about waiting for exam results.',
     'Sustained second-person viewpoint placing the reader in the experience; tension through present tense and sensory detail; a clear ending.',
     'Plan: you wake early; you check your phone again; the walk to school; the envelope; the decision to open it. Sample: ‘You have been awake since four. You have counted the cracks in the ceiling twice.’'),
    ('Write a story about a lost dog finding its way home, narrated by the dog.',
     'First-person animal narrator with a limited, distinctive view of human behaviour; humour or pathos from what the dog misunderstands; clear journey structure.',
     'Plan: the chase that leads the dog away; strange streets; a kind stranger misunderstood; the familiar smell of home; reunion.'),
]
writing_templates(t12, VIEW_TASKS, 'narrative')

# ---------------------------------------------------------------- 1.3 characterisation
CHAR_METHODS = ['what the character says (dialogue)', 'what the character does (action)', 'description of appearance', 'how other characters react to them', 'the character’s thoughts and feelings']
CHAR_SNIP = [
    ("'A thing done fast is a thing done twice,' he told a customer who tapped his watch.", 'what the character says (dialogue)', 'his proverb shows he is wise and refuses to be rushed.', 'Dada Farouk', 'wise and patient'),
    ("looked at the coins, then at the boy's worn shoes, and pushed the money back across the counter", 'what the character does (action)', 'his actions show he is observant and generous.', 'Dada Farouk', 'kind and generous'),
    ('Dada Farouk\'s stall was the smallest in the market, but people queued for it anyway.', 'how other characters react to them', 'the queue shows how much people trust his skill.', 'Dada Farouk', 'respected'),
    ('Rosa, who was now examining her boots with great concentration', 'what the character does (action)', 'Rosa pretends to be busy, which reveals her hurt pride.', 'Rosa', 'jealous and proud'),
    ("'I'll need you up front on Saturday. Nobody scores like you.'", 'what the character says (dialogue)', 'Lena’s words are generous and tactful, showing leadership.', 'Lena', 'tactful and generous'),
    ('Her coat was three sizes too big and fastened with a safety pin, but she wore it like a queen.', 'description of appearance', 'the shabby coat contrasts with her proud bearing, suggesting dignity despite poverty.', 'the girl', 'proud and dignified'),
    ('Mr Varga had a face like a closed door and a voice to match.', 'description of appearance', 'the simile suggests he is unwelcoming, stern and hard to reach.', 'Mr Varga', 'cold and unapproachable'),
    ('Whenever Aunt Bisi entered a room, conversations stopped and children remembered urgent business elsewhere.', 'how other characters react to them', 'others fear or respect her, so she is formidable.', 'Aunt Bisi', 'formidable'),
    ('Jonas told himself he was not afraid of the dark. He just preferred to sleep with the light on, the door open and the radio playing.', 'the character’s thoughts and feelings', 'his self-justification reveals his fear and gives humour.', 'Jonas', 'secretly afraid'),
    ('She counted the money twice, then a third time, then hid it inside the hollow leg of her bed.', 'what the character does (action)', 'repeated counting and hiding suggest she is cautious, anxious or secretive.', 'she', 'cautious and secretive'),
    ("'Oh, don't mind me,' sighed Mrs Patel, lifting the heaviest box herself. 'I'm only seventy-three.'", 'what the character says (dialogue)', 'her sarcastic remark shows she is stubborn and wants others to feel guilty.', 'Mrs Patel', 'stubborn and sharp-tongued'),
    ('Ravi wondered, not for the first time, whether anyone would notice if he simply stopped talking altogether.', 'the character’s thoughts and feelings', 'his private thought reveals loneliness and a feeling of being ignored.', 'Ravi', 'lonely'),
]
t13 = topic('Characterisation through dialogue, action and description', 'characterisation', 'dialogue action description', 'character')
t13.fixed('C1', (1, 2), [
    ('What does ‘show, don’t tell’ mean a writer should do?', 'reveal character through actions, speech and detail rather than stating traits directly',
     'Showing lets the reader infer: ‘She slammed the door’ instead of ‘She was angry’.', ['tell the reader exactly what each character is like', 'avoid using any dialogue', 'describe only the setting']),
    ('Which sentence SHOWS that a character is nervous rather than telling us?', 'Her fingers kept twisting the strap of her bag.',
     'The physical action lets the reader infer nervousness; the others state the feeling directly.', ['She was very nervous.', 'She felt nervous about the test.', 'Everyone could tell she was nervous.']),
    ('What is a character’s motivation?', 'The reason behind what a character wants or does', 'Motivation = what drives a character’s choices.', ['The place where the story is set', 'The order of events in the plot', 'The narrator’s tone of voice']),
])
classify_templates(t13, CHAR_SNIP, CHAR_METHODS,
                   ['Which method of characterisation does the writer mainly use here? {q}', 'Read: {q} How is the character mainly presented?'],
                   C2frames=['Read: {q} What does this suggest about the character? Explain how the writer shows this through {label}.'],
                   C3frames=[('Read: {q} Using point, evidence and explanation, analyse what this reveals about the character.',
                              lambda it: f'The character seems {it[4]}: {it[2]}',
                              lambda it, m: f'{upto(m)}: 1 for a valid trait ({it[4]} or similar); 1 for apt evidence; remaining mark(s) for explaining how the words create the impression ({it[1]}).')])
t13.fixed('C2', (2, 3), [
    (f'Rewrite this ‘telling’ sentence so that it shows the trait instead: {Q(a)} Then explain why your version is more effective.', b,
     '1 mark: a convincing showing sentence (action, speech or detail); 1 mark: explanation that the reader infers the trait, making it more vivid.')
    for a, b in [('Sam was very lazy.', 'Model: ‘Sam reached for the remote with his foot rather than sit up.’ The action lets the reader work out the laziness and adds humour.'),
                 ('The old woman was kind.', 'Model: ‘The old woman pressed a warm bread roll into each child’s hand as they passed her gate.’ The gesture proves her kindness.'),
                 ('Daniel was angry.', 'Model: ‘Daniel’s pen snapped in his fist.’ The physical detail is dramatic and lets the reader feel the anger.'),
                 ('Priya was confident.', 'Model: ‘Priya walked to the front, set her notes aside and smiled at the crowd.’ Her actions show assurance without stating it.'),
                 ('The headteacher was strict.', 'Model: ‘When the headteacher walked in, thirty chairs scraped back at once.’ The others’ reaction shows his authority.')]])
CHAR_TASKS = [
    ('Write a scene in which two friends argue about a secret, revealing their characters through dialogue and action rather than direct description.',
     'Distinct voices for each friend; actions and gestures that show emotion; subtext; a turning point; correct dialogue punctuation.',
     'Plan: setting (bus stop after school); Friend A hints she knows; Friend B deflects with jokes; tension rises; B finally admits the truth; final gesture shows the friendship may survive.'),
    ('Describe a market trader at the start of a working day so that the reader can infer their personality without being told it directly.',
     'Appearance, actions and speech that suggest traits; reactions of customers; small revealing details; show not tell.',
     'Plan: arrival before dawn; how they arrange the stall; how they treat a poor customer and a rich one; a final telling detail.'),
    ('Write a story opening that introduces a character who is hiding something. Use at least three methods of characterisation.',
     'Speech, action, appearance, thoughts and others’ reactions combined; hints about the secret; tension created through what is not said.',
     'Plan: character arrives at a family meal; avoids a question; hides a letter in a pocket; sibling notices; ending on a hint.'),
    ('Write about a grandparent or older neighbour through a single incident that reveals what kind of person they are.',
     'One focused incident; vivid details of appearance and habit; dialogue that sounds real; reader infers the traits.',
     'Plan: the neighbour rescues a kite from a tree; their sharp words but gentle actions; the narrator’s changing view of them.'),
    ('Write a scene in which a new student arrives in a classroom. Show how three different classmates react, so that each reaction reveals their character.',
     'Three contrasting reactions (welcoming, suspicious, indifferent) shown through action and dialogue; viewpoint handled consistently.',
     'Plan: the door opens; one classmate moves her bag to make space; one whispers a comment; one keeps drawing; the new student’s response.'),
]
writing_templates(t13, CHAR_TASKS, 'narrative')
feature_templates(t13, STALL.feats + CAPTAIN.feats, NARR, c1=False)
compose_templates(t13, [STALL, CAPTAIN], C=('C4',))

# ---------------------------------------------------------------- 1.4 writing a story opening
OPEN_TYPES = ['starting in the middle of the action (in medias res)', 'opening with dialogue', 'opening with a description of the setting',
              'opening with a mysterious statement', 'opening with a question to the reader', 'opening with a character description']
OPENINGS = [
    ('The rope snapped just as Daniel reached the halfway point.', OPEN_TYPES[0], 'the reader is thrown straight into danger and wants to know if Daniel survives.'),
    ("'If you open that box,' said Gran, 'you'll have to live with what's inside.'", OPEN_TYPES[1], 'the warning creates mystery about the box and reveals Gran’s character instantly.'),
    ('Fog lay on the valley like spilt milk, and the church bell rang through it without seeming to come from anywhere.', OPEN_TYPES[2], 'the eerie, muffled setting creates atmosphere and unease.'),
    ('On the morning I turned fourteen, I found a letter addressed to me in my own handwriting.', OPEN_TYPES[3], 'the impossible detail raises an immediate question the reader wants answered.'),
    ('Have you ever kept a secret so long that you forgot it was not true?', OPEN_TYPES[4], 'the question involves the reader personally and hints at a story about lies.'),
    ('Mrs Petrova was the kind of neighbour who knew your business before you did.', OPEN_TYPES[5], 'the witty description creates a vivid character and suggests conflict to come.'),
    ('Three things happened on the day the river froze, and only one of them was the river.', OPEN_TYPES[3], 'the riddle-like statement promises two more surprising events.'),
    ('The desert at noon was white and silent, a sheet of glare stretching to the edge of the world.', OPEN_TYPES[2], 'the harsh, empty setting suggests isolation and danger.'),
    ('The ice cracked under Hana’s left boot, then under her right.', OPEN_TYPES[0], 'beginning at the moment of danger creates instant tension.'),
    ("'Nobody leaves this room until I find out who did it,' said Mr Lim.", OPEN_TYPES[1], 'the dramatic line establishes conflict, a mystery and a commanding character.'),
    ('Uncle Tariq wore the same brown suit to every wedding, funeral and birthday for thirty years.', OPEN_TYPES[5], 'the comic detail sketches a stubborn, memorable character.'),
    ('What would you do if your shadow stopped following you?', OPEN_TYPES[4], 'the strange question hooks the reader with a fantasy idea and invites them to imagine.'),
]
WEAK_OPENINGS = [
    ('One day I woke up. I got dressed and had breakfast. Then I went to school and something strange happened.',
     'Model: ‘The strange thing began before breakfast, when the bathroom mirror showed my reflection still asleep.’ Starts at the interesting moment, cuts dull routine, and creates mystery.'),
    ('It was a dark and stormy night. It was very dark and very stormy.',
     'Model: ‘Rain hammered the tin roof so hard that Ama did not hear the knock until the third time.’ Replaces cliché and repetition with specific detail and adds tension.'),
    ('My name is Sam and I am thirteen and this is a story about a haunted house.',
     'Model: ‘Everyone on Kestrel Road crossed the street rather than walk past number nine, and until last Tuesday I had laughed at them.’ Shows rather than tells; hints at the haunting.'),
    ('The forest was nice. There were trees and birds. It was quiet.',
     'Model: ‘In the forest even the birds seemed to whisper, and the pines leaned together as if sharing a secret.’ Uses precise imagery and creates atmosphere instead of vague words like ‘nice’.'),
    ('Once upon a time there was a girl who lived in a village. She was good and kind.',
     'Model: ‘Every morning Lina left a bowl of rice outside the door of the house nobody else would visit.’ Shows kindness through action and raises a question about the house.'),
    ('The holiday ended and we went home. It was sad.',
     'Model: ‘By the time the car pulled away, the sea was only a silver line in the mirror, and no one had said a word for an hour.’ Shows sadness through detail and silence.'),
    ('Suddenly there was a loud noise and everyone was scared.',
     'Model: ‘The crash came from the attic, a sound like a wardrobe falling down a staircase, and the dog crawled under the table.’ Specific sound and reactions replace vague words.'),
    ('It was the first day of school. I was nervous. I walked in.',
     'Model: ‘I had practised the walk from the gate to the classroom door eleven times in my head, but none of the practice had included the rain.’ Builds character and tension through detail.'),
]
TITLES_OPEN = ['The Locked Gate', 'The Night the Lights Went Out', 'The Stranger on the Platform', 'Under the Ice', 'The Letter',
               'The Last Day of Summer', 'The Empty Classroom', 'Lost in the Market', 'Footprints in the Sand', 'The Storm Shelter', 'The Visitor', 'The Wrong Bus']
OPEN_REQ = [('establishes setting, character and a sense of tension', 'Setting, character and tension established; a hook; show not tell.'),
            ('begins in the middle of the action', 'In medias res; reader oriented quickly; tension maintained.'),
            ('uses a first-person narrator and ends on a moment of suspense', 'Consistent first person; voice; suspense in the final line.'),
            ('opens with a line of dialogue and introduces two contrasting characters', 'Dialogue opening punctuated correctly; contrast of characters through speech and action.'),
            ('uses the weather or setting to suggest the main character’s mood', 'Pathetic fallacy; atmosphere linked to feeling; controlled description.')]
t14 = topic('Writing a story opening', 'writing a story opening', 'setting character tension', 'story opening')
t14.fixed('C1', (1, 2), [
    ('What is the main purpose of a story’s opening?', 'To hook the reader and establish setting, character or situation', 'An opening must make the reader want to read on while orienting them.',
     ['To explain how the story ends', 'To list every character', 'To summarise the whole plot']),
    ('What does ‘in medias res’ mean?', 'Starting in the middle of the action', 'Latin for ‘into the middle of things’: the story begins at an exciting point.',
     ['Starting with the ending', 'Starting with a dream', 'Starting with the title']),
    ('Which is a common weakness in story openings?', 'Describing a dull daily routine before anything happens', 'Openings that begin with waking up and breakfast delay the interest.',
     ['Raising a question the reader wants answered', 'Introducing a character through action', 'Using a precise detail of setting']),
])
classify_templates(t14, OPENINGS, OPEN_TYPES,
                   ['Which kind of opening is this? {q}', 'A story begins: {q} Which technique does the writer use to open the story?'],
                   C2frames=['A story begins: {q} Explain why this opening might make a reader want to continue.',
                             'This story opening is an example of {label}: {q} Explain the effect of opening in this way.'])
rewrite_templates(t14, [('Rewrite this weak story opening to make it more engaging.', a, b, 'Award for: starting at an interesting moment; specific, vivid detail; a hook or question; accurate expression.') for a, b in WEAK_OPENINGS],
                  ['{ins} Explain one change you made. {q}', 'Here is a student’s opening: {q} {ins}', 'Improve this opening so that it shows rather than tells: {q}'])
writing_templates(t14, [(f'Write the opening of a story called ‘{ti}’ that {req}.', ind, f'Model approach for ‘{ti}’: begin with a precise image or action, introduce the main character through what they do, plant one unanswered question, and end the section at a moment of tension. {ind}')
                        for ti in TITLES_OPEN for req, ind in OPEN_REQ], 'opening')
CHAPTERS[1] = [t11, t12, t13, t14]


# =========================================================== Unit 2 Non-fiction: information and explanation

def add_summary(T, focus, points, model):
    if not hasattr(T, 'sums'):
        T.sums = []
    T.sums.append((focus, points, model))
    return T


MONSOON = Text('monsoon', 'explanation', 'an explanation text, ‘How a Monsoon Forms’', """
Every summer, the land in South Asia heats up much faster than the surrounding ocean. As the hot air above the land
rises, it creates an area of low pressure. Cooler, moist air from over the Indian Ocean is then drawn inland to replace
it. This sea air carries enormous quantities of water vapour. When it meets mountains such as the Western Ghats or the
Himalayas, it is forced upwards, cools and condenses into thick clouds. As a result, heavy rain falls, sometimes for
weeks at a time. In winter the process reverses: the land cools more quickly than the sea, so dry winds blow from the
land towards the ocean. Farmers depend on the summer monsoon, because in much of the region it brings most of the year's
rain in just a few months.""")
MONSOON.r('the land in South Asia heats up much faster than the surrounding ocean', 'What happens to the land in summer?', 'It heats up faster than the ocean',
          ['It cools faster than the ocean', 'It stays the same temperature as the ocean', 'It is covered by the ocean', 'It freezes'])
MONSOON.r('As the hot air above the land rises, it creates an area of low pressure.', 'What does the rising hot air create?', 'An area of low pressure',
          ['An area of high pressure', 'A mountain range', 'A dry winter wind', 'A cloud of dust'])
MONSOON.r('When it meets mountains such as the Western Ghats or the Himalayas, it is forced upwards, cools and condenses into thick clouds.',
          'What happens to the moist air when it meets mountains?', 'It is forced upwards, cools and forms clouds', ['It sinks and warms up', 'It blows back out to sea', 'It turns into snow at once', 'It stops moving'])
MONSOON.r('In winter the process reverses: the land cools more quickly than the sea, so dry winds blow from the land towards the ocean.',
          'Which way do the winds blow in winter?', 'From the land towards the ocean', ['From the ocean towards the land', 'Up the mountains', 'In circles over the land', 'They stop completely'])
MONSOON.i('As a result, heavy rain falls, sometimes for weeks at a time.', 'Why does the writer use the phrase ‘As a result’ here?',
          'It is a causal connective that links the rain to the process just explained, showing the reader that the rain is the effect of the air rising and cooling.',
          '1 mark: identifies it as a cause-and-effect link; 1 mark: explains what it connects')
MONSOON.i('Farmers depend on the summer monsoon, because in much of the region it brings most of the year\'s rain in just a few months.',
          'What does this sentence suggest about the importance of the monsoon?',
          'Life and food production depend on it: if the monsoon fails or is late, crops could fail, because most of the year’s rain arrives in this short period.',
          '1 mark: importance to farming/food; 1 mark: inference about the consequences of a failed monsoon')
add_summary(MONSOON, 'the stages by which summer monsoon rain is formed',
            ['land heats faster than the sea', 'hot air rises, creating low pressure', 'moist sea air is drawn inland', 'air is forced up by mountains', 'it cools and condenses into clouds', 'heavy rain falls'],
            'In summer the land warms faster than the sea, so rising air leaves low pressure that draws moist ocean air inland. Mountains force this air upwards, where it cools and condenses into clouds that release heavy rain.')

BEES = Text('bees', 'information', 'an information text, ‘The Waggle Dance’', """
Honeybees cannot draw maps, but they can dance them. When a forager bee discovers a good patch of flowers, she returns
to the hive and performs a 'waggle dance' on the honeycomb. She runs forward in a straight line, shaking her body from
side to side, then loops back round and repeats the movement. The direction of the straight run shows the direction of
the food in relation to the sun. The length of the waggle tells the other bees how far away it is: the longer the
waggle, the further the flight. Other workers follow the dancer closely, sensing her movements in the dark hive, and then
fly off to find the flowers for themselves. The dance was first decoded by the Austrian scientist Karl von Frisch, who
later shared a Nobel Prize for his work.""")
BEES.r('performs a \'waggle dance\' on the honeycomb', 'Where does the bee perform the dance?', 'On the honeycomb inside the hive', ['On a flower', 'In the air outside the hive', 'On the scientist’s hand', 'On the ground'])
BEES.r('The direction of the straight run shows the direction of the food in relation to the sun.', 'What does the direction of the straight run show?',
       'The direction of the food compared with the sun', ['How far away the food is', 'How much food there is', 'Which bee found the food', 'What time of day it is'])
BEES.r('the longer the waggle, the further the flight', 'What does a longer waggle tell the other bees?', 'That the food is further away',
       ['That the food is closer', 'That there is more food', 'That the food is dangerous', 'That the dancer is tired'])
BEES.r('The dance was first decoded by the Austrian scientist Karl von Frisch', 'Who first decoded the dance?', 'Karl von Frisch, an Austrian scientist',
       ['A beekeeper in the hive', 'An unnamed Nobel committee', 'A forager bee', 'A group of farmers'])
BEES.i('Honeybees cannot draw maps, but they can dance them.', 'Why is this an effective opening sentence for an information text?',
       'It hooks the reader with a surprising, playful idea (dancing a map) while summarising the main topic of the text in one line.',
       '1 mark: engages/surprises the reader; 1 mark: introduces the topic clearly')
BEES.i('Other workers follow the dancer closely, sensing her movements in the dark hive', 'Why do the other bees need to follow the dancer closely?',
       'Because the hive is dark, they cannot see the dance, so they have to sense her movements by staying close to her.',
       '1 mark: hive is dark; 1 mark: they sense/feel the movements')
add_summary(BEES, 'how the waggle dance communicates the location of food',
            ['the bee runs in a straight line while waggling', 'the direction of the run shows the direction of the food relative to the sun', 'the length of the waggle shows the distance', 'other bees follow closely and sense the movements', 'they then fly to the flowers themselves'],
            'A returning forager waggles along a straight line: its direction gives the food’s direction relative to the sun and its length gives the distance. Nearby bees sense the movements and fly out to the flowers.')

STILL = Text('still', 'explanation', 'an explanation text, ‘How a Solar Still Works’', """
A solar still is a simple device that uses the sun's heat to turn salty or dirty water into clean drinking water. First,
a shallow basin is filled with the untreated water and covered with a sloping sheet of clear plastic or glass. Sunlight
passes through the cover and warms the water, causing some of it to evaporate. The water vapour leaves salt, mud and most
germs behind. When the vapour touches the cooler underside of the cover, it condenses into droplets. Because the cover
slopes, these droplets run down into a collecting channel and then into a container. A small still might produce only a
few litres a day, but it needs no fuel, no electricity and very little maintenance, which makes it valuable in remote,
sunny places.""")
STILL.r('a shallow basin is filled with the untreated water and covered with a sloping sheet of clear plastic or glass', 'What is the basin covered with?',
        'A sloping sheet of clear plastic or glass', ['A wet cloth', 'A metal lid', 'A layer of sand', 'A black plastic bag'])
STILL.r('The water vapour leaves salt, mud and most germs behind.', 'What does the water vapour leave behind?', 'Salt, mud and most germs',
        ['Clean drinking water', 'The plastic cover', 'Sunlight and heat', 'Only the salt'])
STILL.r('A small still might produce only a few litres a day', 'How much water might a small still produce?', 'A few litres a day', ['Hundreds of litres a day', 'A few drops a week', 'A litre an hour', 'Enough for a whole village'])
STILL.r('it needs no fuel, no electricity and very little maintenance', 'Which of these does a solar still need?', 'Very little maintenance',
        ['Fuel', 'Electricity', 'A large team of engineers', 'A connection to a water pipe'])
STILL.i('Because the cover slopes, these droplets run down into a collecting channel', 'Why is the slope of the cover important?',
        'The slope makes the droplets run in one direction into the channel, so the clean water is collected instead of dripping back into the dirty water.',
        '1 mark: droplets run down/are guided; 1 mark: collected rather than falling back')
STILL.i('which makes it valuable in remote, sunny places', 'Why is a solar still especially valuable in remote, sunny places?',
        'These places have plenty of sunlight but may lack fuel, electricity and repair services, which the still does not need.',
        '1 mark: sunlight available; 1 mark: lack of fuel/electricity/maintenance in remote areas')
add_summary(STILL, 'how a solar still produces clean water',
            ['untreated water is put in a covered basin', 'sunlight warms the water so it evaporates', 'impurities are left behind', 'vapour condenses on the cooler cover', 'droplets run down the slope into a container'],
            'Untreated water in a covered basin is warmed by sunlight and evaporates, leaving salt and dirt behind. The vapour condenses on the cool sloping cover and the droplets run down into a container.')

MANGROVE = Text('mangrove', 'information', 'an information leaflet, ‘Mangroves: The Coast’s Living Wall’', """
Mangroves are trees that grow where the land meets the sea. Unlike most plants, they can survive in salty water, and
their tangled roots arch out of the mud like the legs of a giant spider. These roots do far more than hold the trees up.
They slow down waves and trap sediment, protecting coastlines from erosion and storm surges. They also shelter young
fish, crabs and shrimps, which is why mangroves are often called the nurseries of the sea. Mangrove forests store large
amounts of carbon in their soil, helping to slow climate change. Sadly, large areas of mangrove have been lost in recent
decades, much of it cleared for shrimp farms and coastal building. Visitors can help by staying on boardwalks, taking
litter home and supporting local replanting projects.""")
MANGROVE.r('Mangroves are trees that grow where the land meets the sea.', 'Where do mangroves grow?', 'Where the land meets the sea', ['High in the mountains', 'In deserts far from water', 'Only in freshwater lakes', 'In city parks'])
MANGROVE.r('which is why mangroves are often called the nurseries of the sea', 'Why are mangroves called the nurseries of the sea?', 'They shelter young fish, crabs and shrimps',
           ['They grow very quickly', 'They are planted by children', 'They provide wood for cradles', 'They produce sea water'])
MANGROVE.r('much of it cleared for shrimp farms and coastal building', 'What has caused much of the loss of mangroves?', 'Clearing for shrimp farms and coastal building',
           ['Disease spread by crabs', 'Too much rainfall', 'Visitors walking on boardwalks', 'Replanting projects'])
MANGROVE.r('Visitors can help by staying on boardwalks, taking litter home and supporting local replanting projects.', 'Which is one way the leaflet says visitors can help?', 'Taking their litter home',
           ['Picking mangrove seeds', 'Feeding the fish', 'Building shrimp farms', 'Walking on the roots'])
MANGROVE.i('These roots do far more than hold the trees up.', 'What is the purpose of this sentence in the leaflet?',
           'It is a topic sentence that signals a shift from describing the roots to explaining their wider benefits, making the reader expect a list of uses.',
           '1 mark: signals/introduces new information; 1 mark: leads into the benefits that follow')
MANGROVE.i('Sadly, large areas of mangrove have been lost in recent decades', 'What does the word ‘Sadly’ show about the writer’s attitude?',
           'The writer is not completely neutral: ‘Sadly’ expresses regret and encourages the reader to care about protecting mangroves.',
           '1 mark: regret/concern; 1 mark: effect on reader (to persuade them to help)')
MANGROVE.f('their tangled roots arch out of the mud like the legs of a giant spider', 'simile', 'like the legs of a giant spider',
           'the vivid comparison helps the reader picture the arching, many-legged roots, making the information memorable.')
MANGROVE.f('mangroves are often called the nurseries of the sea', 'metaphor', 'the nurseries of the sea',
           'comparing mangroves to a nursery suggests a safe, protective place where young creatures are cared for.')
add_summary(MANGROVE, 'the benefits of mangroves',
            ['they protect coasts by slowing waves', 'they trap sediment and reduce erosion and storm-surge damage', 'they shelter young fish, crabs and shrimps', 'they store carbon, helping slow climate change'],
            'Mangrove roots slow waves and trap sediment, protecting coasts from erosion and storm surges. They shelter young sea creatures and store carbon in their soil, helping to slow climate change.')

EARS = Text('ears', 'explanation', 'an explanation text, ‘Why Do Your Ears Pop?’', """
Have you ever noticed your ears 'pop' as a plane comes in to land? The cause is a difference in air pressure. Behind
each eardrum is a small air-filled space called the middle ear. It is connected to the back of the throat by a narrow
passage known as the Eustachian tube. Normally, the air pressure on both sides of the eardrum is the same. However, when
a plane descends, the air pressure in the cabin rises quickly. The higher pressure outside pushes the eardrum inwards,
which can feel uncomfortable or even painful. Swallowing or yawning opens the Eustachian tube briefly, allowing air to
flow into the middle ear until the pressures are equal again. The 'pop' you hear is the eardrum springing back into
place.""")
EARS.r('It is connected to the back of the throat by a narrow passage known as the Eustachian tube.', 'What connects the middle ear to the throat?', 'The Eustachian tube',
       ['The eardrum', 'The cabin', 'The outer ear', 'The nose'])
EARS.r('when a plane descends, the air pressure in the cabin rises quickly', 'What happens to cabin air pressure as a plane descends?', 'It rises quickly',
       ['It falls quickly', 'It stays the same', 'It disappears', 'It becomes equal to the middle ear at once'])
EARS.r('Swallowing or yawning opens the Eustachian tube briefly', 'According to the text, what can open the Eustachian tube?', 'Swallowing or yawning',
       ['Covering your ears', 'Holding your breath', 'Standing up', 'Closing your eyes'])
EARS.r("The 'pop' you hear is the eardrum springing back into place.", 'What causes the ‘pop’ sound?', 'The eardrum springing back into place',
       ['Air leaving the plane', 'The engines slowing down', 'The Eustachian tube closing', 'The cabin door opening'])
EARS.i("Have you ever noticed your ears 'pop' as a plane comes in to land?", 'Why does the writer begin with a question?',
       'A question addressed to ‘you’ links the topic to the reader’s own experience, making them curious to find out the explanation.',
       '1 mark: engages the reader/personal experience; 1 mark: creates curiosity about the cause')
EARS.i('However, when a plane descends, the air pressure in the cabin rises quickly.', 'What is the function of ‘However’ in this sentence?',
       'It signals a contrast between the normal situation (equal pressure) and what happens when a plane descends, moving the explanation on to the cause of the problem.',
       '1 mark: contrast connective; 1 mark: links normal state to the change')
add_summary(EARS, 'why ears pop when a plane lands',
            ['the middle ear is an air-filled space behind the eardrum', 'cabin pressure rises as the plane descends', 'higher outside pressure pushes the eardrum in', 'swallowing or yawning opens the Eustachian tube', 'air enters until pressures are equal and the eardrum springs back'],
            'As a plane descends, cabin pressure rises and pushes the eardrum inwards. Swallowing or yawning opens the Eustachian tube so air enters the middle ear; when the pressures equalise the eardrum springs back with a pop.')

MONSOON.x('How does the writer make the process of the monsoon clear for the reader?', 'Sequenced explanation from cause to effect; causal connectives (As a result, so, because); technical vocabulary (low pressure, condenses); present tense; contrast of summer and winter; final sentence on importance to farmers.')
BEES.x('How does the writer make the information about the waggle dance interesting as well as clear?', 'Playful opening (dance them a map); step-by-step description; explanation of direction and distance with a memorable pattern (the longer… the further); detail of the dark hive; authority from the scientist and Nobel Prize.')
STILL.x('How does the writer explain how a solar still works and why it is useful?', 'Definition first; sequencing (First, When, Because); cause and effect of evaporation and condensation; technical words; balanced ending weighing small output against no fuel or electricity.')
MANGROVE.x('How does the leaflet inform readers and also encourage them to protect mangroves?', 'Definition; vivid simile of spider legs; list of benefits; metaphor nurseries of the sea; carbon fact; ‘Sadly’ signals concern; practical advice to visitors ends with a call to action.')
EARS.x('How does the writer explain why ears pop in a way that suits a general reader?', 'Opening question linking to experience; technical terms explained (middle ear, Eustachian tube); clear cause-effect chain with ‘However’; practical tip (swallowing or yawning); final sentence explains the pop.')
U2_TEXTS = [MONSOON, BEES, STILL, MANGROVE, EARS]

# ---------------------------------------------------------------- 2.1 features and purpose
INFO_FEATS = ['causal connective', 'technical vocabulary', 'present tense for general truths', 'sequencing connective', 'question to engage the reader', 'definition of a term', 'factual detail or number']
INFO_SNIP = [
    ('As a result, heavy rain falls, sometimes for weeks at a time.', 'causal connective', '‘As a result’ links the rain to its cause.'),
    ('Because the cover slopes, these droplets run down into a collecting channel', 'causal connective', '‘Because’ explains why the droplets move.'),
    ('It is connected to the back of the throat by a narrow passage known as the Eustachian tube.', 'technical vocabulary', '‘Eustachian tube’ is the precise scientific name.'),
    ('When it meets mountains such as the Western Ghats or the Himalayas, it is forced upwards, cools and condenses into thick clouds.', 'technical vocabulary', '‘condenses’ is the precise scientific term for vapour turning into liquid.'),
    ('Honeybees cannot draw maps, but they can dance them.', 'present tense for general truths', 'the present tense presents something that is always true of bees.'),
    ('Mangroves are trees that grow where the land meets the sea.', 'definition of a term', 'the sentence explains what the word ‘mangroves’ means.'),
    ('A solar still is a simple device that uses the sun\'s heat to turn salty or dirty water into clean drinking water.', 'definition of a term', 'it defines the key term at the start.'),
    ('First, a shallow basin is filled with the untreated water', 'sequencing connective', '‘First’ shows the order of the steps.'),
    ('Have you ever noticed your ears \'pop\' as a plane comes in to land?', 'question to engage the reader', 'it links the topic to the reader’s own experience.'),
    ('A small still might produce only a few litres a day', 'factual detail or number', 'a precise quantity informs the reader realistically.'),
    ('The dance was first decoded by the Austrian scientist Karl von Frisch, who later shared a Nobel Prize for his work.', 'factual detail or number', 'a named source and award add authority.'),
    ('Then the dough is left in a warm place, where the yeast begins to feed on the sugar.', 'sequencing connective', '‘Then’ moves the reader to the next step.'),
    ('Consequently, the ice on the lake melts from the edges inwards.', 'causal connective', '‘Consequently’ shows the melting is an effect of what came before.'),
    ('Photosynthesis is the process by which green plants make food using light energy.', 'definition of a term', 'the term is defined before it is explained.'),
]
t21 = topic('Features and purpose of information and explanation texts', 'features and purpose', 'information and explanation texts')
t21.fixed('C1', (1, 2), [
    ('What is the main purpose of an explanation text?', 'To explain how or why something happens', 'Explanation texts describe processes and causes (how/why).',
     ['To persuade the reader to buy something', 'To entertain with a made-up story', 'To describe the writer’s feelings']),
    ('Which tense is usually used in an information text about how something works?', 'The present tense', 'General truths and processes are written in the present (‘The heart pumps…’).',
     ['The future tense', 'The past perfect tense', 'A mixture of tenses chosen at random']),
    ('Which connective is most typical of an explanation text?', 'therefore', 'Explanations link causes and effects (therefore, because, as a result).',
     ['once upon a time', 'suddenly', 'in my opinion']),
    ('Why do information texts often use subheadings?', 'To organise the information so readers can find what they need', 'Subheadings divide content into topics and help skimming and scanning.',
     ['To make the text longer', 'To tell a story in order', 'To hide the main point']),
    ('Which of these is the most typical feature of an information text?', 'An impersonal, formal tone', 'Information texts are usually impersonal and factual.',
     ['A first-person narrator telling a story', 'Rhyming lines', 'Stage directions']),
    ('What is the purpose of a diagram with labels in an explanation?', 'To show visually the parts or stages that the words describe', 'Diagrams support the written explanation.',
     ['To replace the title', 'To give the writer’s opinion', 'To add humour']),
])
classify_templates(t21, INFO_SNIP, INFO_FEATS,
                   ['Which feature of an information or explanation text is shown here? {q}', 'Read this sentence from a non-fiction text: {q} Which feature does it mainly illustrate?'],
                   C2frames=['This sentence uses a {label}: {q} Explain how this feature helps the reader.',
                             'Explain why a writer of an explanation text would use a {label}, as in: {q}'],
                   C3frames=[('Identify one feature of explanation writing in this sentence and explain its purpose: {q}',
                              lambda it: f'{cap(it[1])}: {it[2]}', lambda it, m: f'{upto(m)}: 1 for the feature ({it[1]}); 1 for the example; remaining mark(s) for its purpose for the reader.')])
t21.fixed('C2', (2, 3), inf_items([MONSOON, MANGROVE, EARS]))
compose_templates(t21, U2_TEXTS, C=('C4',))


@t21.add('C3', (3, 4, 5), 'explain')
def t21_features(r, D):
    T = r.choice(U2_TEXTS)
    m = mk('C3', D)
    n = 2 if D <= 3 else 3
    return {'stem': f'Read {T.label}. {Q(T.text)} Identify {n} features that show this is {"an explanation" if T.kind == "explanation" else "an information"} text, giving an example of each and explaining its purpose.',
            'answer': ('Possible features: present tense for general truths; technical vocabulary; ' + ('causal and sequencing connectives (e.g. ‘As a result’, ‘First’, ‘Because’); ' if T.kind == 'explanation' else 'factual details and definitions; ')
                       + 'impersonal third-person style; a clear opening that introduces the topic.'),
            'key': f'{upto(m)}: for each feature, 1 for the feature with an example from the text; credit purpose (clarity, sequence, accuracy, authority).'}

# ---------------------------------------------------------------- 2.2 skimming and scanning
t22 = topic('Skimming, scanning and selecting key information', 'skimming scanning', 'selecting key information')
t22.fixed('C1', (1, 2), ret_items(U2_TEXTS))
t22.fixed('C1', (1, 2), [
    ('What is skimming?', 'Reading quickly to get the general idea or gist of a text', 'Skim for gist; scan for specific details.',
     ['Searching for one particular fact, name or number', 'Reading every word slowly and carefully', 'Copying out the key sentences']),
    ('What is scanning?', 'Searching a text quickly for a specific piece of information', 'Scanning: eyes move quickly looking for a key word, date or number.',
     ['Reading for the overall gist', 'Summarising the main points', 'Re-reading a paragraph to analyse its language']),
    ('Which reading strategy would be best for finding a date in a long article?', 'Scanning', 'Scanning is used for specific details such as dates and names.',
     ['Skimming', 'Close reading of every sentence', 'Reading aloud']),
])
t22.fixed('C2', (2, 3), [
    ('Explain the difference between skimming and scanning, and give one situation in which you would use each.',
     'Skimming is reading quickly for the gist (e.g. deciding whether an article is useful); scanning is searching for a particular detail (e.g. finding a train time in a timetable).',
     '1 mark: skimming defined; 1 mark: scanning defined; a further mark for apt situations.'),
    ('Explain how subheadings and topic sentences help a reader to skim a text.', 'They summarise what each section is about, so the reader can grasp the main ideas quickly without reading every word.',
     '1 mark: summarise sections; 1 mark: speed/finding the gist.'),
    ('A student is asked to find three reasons why mangroves are important. Explain how they should select information from the leaflet.',
     'Scan for key words such as ‘protect’, ‘shelter’ and ‘store’; select only the relevant points; ignore descriptive detail such as the spider simile.',
     '1 mark: scanning for key words; 1 mark: rejecting irrelevant detail.'),
    ('Why should you use the key words in a question to guide your scanning?', 'The key words tell you what information to look for, so you can find the relevant part of the text quickly and avoid irrelevant details.',
     '1 mark: identifies what to look for; 1 mark: efficiency/relevance.'),
])
SELECT = [
    (MONSOON, 'This sea air carries enormous quantities of water vapour. When it meets mountains such as the Western Ghats or the Himalayas, it is forced upwards, cools and condenses into thick clouds. As a result, heavy rain falls, sometimes for weeks at a time.', 'Give two reasons why heavy rain falls when moist air meets mountains.', 'The air is forced upwards; it cools and condenses into clouds.', ['air forced upwards', 'air cools', 'vapour condenses into clouds']),
    (MONSOON, 'Cooler, moist air from over the Indian Ocean is then drawn inland to replace it. This sea air carries enormous quantities of water vapour. In winter the process reverses: the land cools more quickly than the sea, so dry winds blow from the land towards the ocean.', 'State two differences between the summer and winter monsoon winds.', 'Summer winds are moist and blow from the sea to the land; winter winds are dry and blow from the land to the sea.', ['direction of wind', 'moist versus dry', 'land heats in summer / cools in winter']),
    (BEES, 'The direction of the straight run shows the direction of the food in relation to the sun. The length of the waggle tells the other bees how far away it is: the longer the waggle, the further the flight.', 'Identify the two pieces of information the waggle dance gives to other bees.', 'The direction of the food relative to the sun and how far away the food is.', ['direction (relative to sun)', 'distance (length of waggle)']),
    (STILL, 'The water vapour leaves salt, mud and most germs behind. A small still might produce only a few litres a day, but it needs no fuel, no electricity and very little maintenance, which makes it valuable in remote, sunny places.', 'List three things that the water vapour leaves behind or the still does not need.', 'Leaves behind salt, mud and most germs; does not need fuel, electricity or much maintenance.', ['salt', 'mud', 'germs', 'fuel', 'electricity', 'maintenance']),
    (STILL, 'A small still might produce only a few litres a day, but it needs no fuel, no electricity and very little maintenance, which makes it valuable in remote, sunny places.', 'Give two advantages and one disadvantage of a solar still.', 'Advantages: no fuel or electricity, little maintenance. Disadvantage: produces only a few litres a day.', ['no fuel/electricity', 'little maintenance', 'small output']),
    (MANGROVE, 'They slow down waves and trap sediment, protecting coastlines from erosion and storm surges. They also shelter young fish, crabs and shrimps, which is why mangroves are often called the nurseries of the sea. Mangrove forests store large amounts of carbon in their soil, helping to slow climate change.', 'List three ways in which mangroves benefit people or wildlife.', 'They protect coasts from erosion and storm surges; they shelter young fish, crabs and shrimps; they store carbon and help slow climate change.', ['coastal protection', 'shelter for young sea creatures', 'carbon storage']),
    (MANGROVE, 'Sadly, large areas of mangrove have been lost in recent decades, much of it cleared for shrimp farms and coastal building. Visitors can help by staying on boardwalks, taking litter home and supporting local replanting projects.', 'Identify two causes of mangrove loss and two ways visitors can help.', 'Causes: shrimp farms and coastal building. Help: stay on boardwalks, take litter home or support replanting.', ['shrimp farms', 'coastal building', 'boardwalks', 'litter', 'replanting']),
    (EARS, 'Swallowing or yawning opens the Eustachian tube briefly, allowing air to flow into the middle ear until the pressures are equal again. The \'pop\' you hear is the eardrum springing back into place.', 'Give two ways of making your ears pop, and explain why they work.', 'Swallowing or yawning: both open the Eustachian tube so air flows into the middle ear and the pressures equalise.', ['swallowing', 'yawning', 'opens tube / equalises pressure']),
]


PARAS = [
    ('Camels in the Desert', """Camels are superbly adapted to desert life. Their wide, padded feet spread their weight so they do not sink into soft sand. Long eyelashes and nostrils that can close keep out blowing dust. Contrary to popular belief, their humps store fat, not water; the fat can be broken down for energy when food is scarce. A thirsty camel can drink over 100 litres of water in a few minutes.""",
     'List three ways in which camels are adapted to the desert.', 'Wide padded feet stop them sinking in sand; long eyelashes and closable nostrils keep out dust; humps store fat for energy; they can drink large amounts quickly.',
     ['padded feet spread weight', 'eyelashes/nostrils keep out dust', 'humps store fat for energy', 'drink a lot quickly'],
     'Camels survive in deserts because their feet, eyelashes and nostrils suit sand and dust, their humps store fat for energy, and they can rehydrate very quickly.'),
    ('Why Leaves Change Colour', """In autumn, the leaves of many trees turn from green to red, orange and yellow. The green colour comes from chlorophyll, which plants use to capture sunlight. As days shorten and temperatures fall, trees stop making chlorophyll. The green fades, revealing yellow and orange pigments that were there all along. Some trees also produce new red pigments. Eventually the leaves fall, helping the tree save water through winter.""",
     'Identify two reasons why leaves change colour in autumn.', 'Trees stop making green chlorophyll as days shorten and it gets colder, so hidden yellow and orange pigments show; some trees make new red pigments.',
     ['shorter days/colder weather', 'chlorophyll production stops', 'hidden yellow/orange pigments revealed', 'some make red pigments'],
     'In autumn, shorter, colder days stop trees producing green chlorophyll, revealing hidden yellow and orange pigments and sometimes new red ones, before the leaves fall.'),
    ('The Great Green Wall', """The Great Green Wall is an African-led project to restore land across the Sahel, the dry region on the southern edge of the Sahara. The original idea was a belt of trees stretching thousands of kilometres from Senegal to Djibouti. Today the project also supports farmers to protect existing trees, save rainwater and grow drought-resistant crops. Its aims are to fight desertification, create jobs and improve food security.""",
     'State three aims of the Great Green Wall project.', 'To fight desertification, to create jobs and to improve food security.', ['fight desertification', 'create jobs', 'improve food security', 'restore land'],
     'The Great Green Wall restores land across the Sahel by planting and protecting trees and helping farmers, aiming to stop desertification, create jobs and secure food.'),
    ('Clever Octopuses', """Octopuses are among the most intelligent invertebrates. They can solve puzzles, open jars to reach food and even escape from aquarium tanks. An octopus has about 500 million nerve cells, and around two-thirds of them are in its arms rather than its brain, so each arm can explore and react partly on its own. Octopuses can also change the colour and texture of their skin in a fraction of a second to hide from predators.""",
     'Give three pieces of evidence that octopuses are intelligent or unusual.', 'They solve puzzles and open jars; they escape from tanks; most of their nerve cells are in their arms; they change colour and texture to hide.',
     ['solve puzzles/open jars', 'escape tanks', 'nerve cells in arms', 'change colour/texture'],
     'Octopuses are highly intelligent invertebrates that solve problems and escape tanks, have most of their nerve cells in their arms and can instantly camouflage themselves.'),
    ('Why Cities Are Warmer', """Cities are often several degrees warmer than the countryside around them, an effect known as the urban heat island. Dark roads and roofs absorb sunlight during the day and release the heat slowly at night. Cars, air conditioners and factories add extra heat. There are also fewer trees and plants to provide shade and cool the air. Planting trees and painting roofs white are two ways to reduce the effect.""",
     'Identify three causes of the urban heat island effect.', 'Dark surfaces absorb and slowly release heat; vehicles, air conditioners and factories produce heat; there are fewer trees to shade and cool the air.',
     ['dark surfaces absorb heat', 'heat released at night', 'heat from cars/machines', 'fewer trees/plants'],
     'Cities are warmer than the countryside because dark surfaces store heat, machines add heat and there is little vegetation; trees and white roofs can reduce this.'),
    ('Sleep and Teenagers', """Teenagers need between eight and ten hours of sleep a night, yet many get far less. During puberty, the body clock shifts, so teenagers naturally feel sleepy later in the evening. Early school starts and late-night screen use make the problem worse, because the blue light from phones delays the release of melatonin, the hormone that makes us sleepy. Lack of sleep can affect memory, mood and concentration.""",
     'Give two reasons why many teenagers do not get enough sleep.', 'Their body clock shifts so they feel sleepy later; early school starts; screen light delays melatonin.',
     ['body clock shifts later', 'early school starts', 'screens delay melatonin'],
     'Many teenagers sleep less than the eight to ten hours they need because their body clocks shift later, school starts early and screens delay melatonin, harming memory and mood.'),
    ('The First Bicycles', """The earliest bicycle, built in Germany in 1817, had no pedals at all: riders pushed it along with their feet. Pedals attached to the front wheel appeared in the 1860s, and soon makers built enormous front wheels to travel further with each turn. These ‘penny-farthings’ were fast but dangerous. The ‘safety bicycle’ of the 1880s, with equal-sized wheels and a chain drive, is the design most bicycles still follow today.""",
     'List the three stages in the development of the bicycle described in the paragraph.', 'A pedal-less machine pushed with the feet (1817); bikes with pedals on the front wheel, leading to the penny-farthing (1860s–70s); the chain-driven safety bicycle with equal wheels (1880s).',
     ['no pedals, pushed by feet', 'pedals on front wheel / penny-farthing', 'chain-driven safety bicycle'],
     'Bicycles developed from a pedal-less machine of 1817, through front-pedal designs and the dangerous penny-farthing, to the chain-driven safety bicycle of the 1880s.'),
    ('Coral Reefs', """Coral reefs cover less than one per cent of the ocean floor, yet they support around a quarter of all marine species. Reefs are built by tiny animals called polyps, which live in partnership with algae. The algae provide food and colour; in return, the coral provides shelter. When the water becomes too warm, the coral expels the algae and turns white, a process called bleaching. Bleached coral can recover, but it may die if the heat lasts.""",
     'Explain two things that happen during coral bleaching.', 'When water gets too warm the coral expels its algae and turns white; it may recover or die if the heat continues.',
     ['water too warm', 'algae expelled', 'coral turns white', 'may recover or die'],
     'Coral reefs, built by polyps living with algae, support a quarter of sea species; when water overheats, coral expels the algae and bleaches, and may die.'),
]


@t22.add('C3', (2, 3, 4, 5), 'short')
def t22_select(r, D):
    T, ex, task, ans, pts = r.choice(SELECT)
    m = mk('C3', D)
    return {'stem': f'Read this part of {T.label}: {Q(ex)} {task} Use your own words where possible.', 'answer': ans, 'key': points_key(m, pts, 'Do not credit copied irrelevant detail.')}


@t22.add('C3', (2, 3, 4, 5), 'short')
def t22_para(r, D):
    title, text, task, ans, pts, _ = r.choice(PARAS)
    m = mk('C3', D)
    return {'stem': f'Read this paragraph from an information text, ‘{title}’: {Q(clean(text))} {task}', 'answer': ans, 'key': points_key(m, pts)}


@t22.add('C4', (2, 3, 4, 5), 'multi_step')
def t22_c4(r, D):
    title, text, task, ans, pts, _ = r.choice(PARAS)
    T = r.choice(U2_TEXTS)
    quote, question, a2, _ = r.choice(T.rets)
    parts = [
        lambda r: (f'Skim the paragraph ‘{title}’ and state its main topic in a few words.', title, '1 mark: main topic identified [1]'),
        lambda r: (task, ans, points_key(3, pts) + ' [3]'),
        lambda r: (f'Scan {T.label} to find the answer: {question}', a2, f'1 mark: {a2} [1]'),
        lambda r: ('Explain which reading strategy (skimming or scanning) you used for each of the previous parts, and why.', 'Skimming for the gist/main topic; scanning for specific details such as reasons or facts.', '1 mark each strategy matched with a reason [2]'),
        lambda r: ('Select the one detail from the paragraph you think would most surprise a reader, and explain your choice.', 'Any accurate detail with a reason (e.g. a striking figure).', '1 mark detail; 1 mark reason [2]'),
    ]
    return compose(r, f'Read the paragraph. {Q(clean(text))}', parts, k=(2, 3, 4), type_='multi_step')


@t22.add('C2', (2, 3, 4), 'short')
def t22_locate(r, D):
    T = r.choice(U2_TEXTS)
    quote, question, answer, _ = r.choice(T.rets)
    return {'stem': f'Scan {T.label} to answer this question: {question} Then quote the words that gave you the answer. {Q(T.text)}', 'answer': f'{answer}. Quotation: {Q(quote)}',
            'key': keypts('1 mark: correct answer; 1 mark: accurate supporting quotation.')}


compose_templates(t22, U2_TEXTS, C=('C4',))

# ---------------------------------------------------------------- 2.3 summarising
OWN_WORDS = [
    ('The higher pressure outside pushes the eardrum inwards, which can feel uncomfortable or even painful.', 'The extra pressure in the cabin presses the eardrum in, which may hurt.'),
    ('These roots do far more than hold the trees up.', 'The roots have many other uses besides supporting the trees.'),
    ('it needs no fuel, no electricity and very little maintenance', 'it runs without power and hardly ever needs repairs.'),
    ('Other workers follow the dancer closely, sensing her movements in the dark hive', 'The other bees stay close and feel how she moves, because they cannot see in the hive.'),
    ('Cooler, moist air from over the Indian Ocean is then drawn inland to replace it.', 'Damp, cooler sea air is pulled over the land to take its place.'),
    ('Mangrove forests store large amounts of carbon in their soil, helping to slow climate change.', 'The ground under mangroves holds a lot of carbon, which reduces global warming.'),
    ('much of it cleared for shrimp farms and coastal building', 'many mangroves were cut down to make way for prawn farming and construction on the coast.'),
]
t23 = topic('Summarising main points in own words', 'summarising main points', 'own words', 'summary')
t23.fixed('C1', (1, 2), [
    ('Which of these should you leave out of a summary?', 'Examples, descriptive detail and repetition', 'A summary keeps only the main points.', ['The main points', 'Key information that answers the question', 'The writer’s central idea']),
    ('What does ‘in your own words’ mean in a summary task?', 'Rephrasing the ideas without copying long phrases from the text', 'You may keep technical terms but must reword the rest.',
     ['Adding your own opinions to the text', 'Copying the text exactly', 'Writing in the first person']),
    ('What is a topic sentence?', 'A sentence, often at the start of a paragraph, that states its main idea', 'Topic sentences help you identify main points for a summary.',
     ['The last sentence of a story', 'A sentence that contains a quotation', 'A sentence with no verb']),
])
t23.fixed('C2', (1, 2, 3), [(f'Rewrite this sentence in your own words: {Q(a)}', b, '1 mark: meaning kept accurately; 1 mark: substantially reworded (technical terms may be kept).') for a, b in OWN_WORDS])


@t23.add('C1', (1, 2, 3))
def t23_best(r, D):
    T = r.choice(U2_TEXTS)
    focus, pts, model = r.choice(T.sums)
    wrong = [f'It explains only that {pts[-1]}.', 'It describes the writer’s personal experience of the topic.', 'It argues that readers should change their behaviour.',
             'It lists the examples and the descriptive details from the text.']
    opts, ans = mcq(r, model, wrong)
    return {'stem': f'Which is the best summary of {focus}, according to {T.label}?', 'options': opts, 'answer': ans,
            'key': f'The best summary covers the main stages/points ({"; ".join(pts)}) concisely.'}


@t23.add('C3', (2, 3, 4, 5), 'short')
def t23_summary(r, D):
    T = r.choice(U2_TEXTS)
    focus, pts, model = r.choice(T.sums)
    w = {1: 30, 2: 40, 3: 50, 4: 60, 5: 60}[D]
    m = mk('C3', D)
    return {'stem': f'Read {T.label}. {Q(T.text)} In no more than {w} words, summarise {focus}. Use your own words as far as possible.',
            'answer': model, 'key': points_key(m, pts, 'Credit concise own-words expression; no credit for copied lists or examples.')}


@t23.add('C4', (2, 3, 4, 5), 'long')
def t23_summary_long(r, D):
    T1, T2 = r.sample(U2_TEXTS, 2)
    f1, p1, m1 = r.choice(T1.sums)
    m = mk('C4', D, 'long')
    return {'stem': f'Read {T1.label}. {Q(T1.text)} Write a summary of {f1} for a younger student who has never studied this topic. Write one paragraph of about 80–100 words in your own words, using clear connectives to show the order or the causes.',
            'answer': f'Model summary: {m1}', 'key': levels_key(m, 'summary', '; '.join(p1) + '. Language should suit a younger reader (simple sentences, technical words explained).')}


compose_templates(t23, U2_TEXTS, C=('C4',))


@t23.add('C3', (2, 3, 4, 5), 'short')
def t23_para(r, D):
    title, text, _, _, _, model = r.choice(PARAS)
    m = mk('C3', D)
    w = 25 if D <= 2 else 35
    frame = r.choice([f'Summarise the main point of this paragraph in one sentence of no more than {w} words.',
                      f'Write a summary of this paragraph in your own words (maximum {w} words).'])
    return {'stem': f'Read this paragraph, ‘{title}’: {Q(clean(text))} {frame}', 'answer': f'Model: {model}',
            'key': f'{upto(m)}: main idea captured; key supporting points included; own words; within the word limit; no examples or minor detail.'}


SUM_FORMS = [('a short paragraph for a school science display', 'clear, factual, formal'),
             ('a script for a 30-second podcast segment for students', 'spoken, direct, with an engaging first line'),
             ('a set of revision notes with a heading and bullet points, then a one-sentence overview', 'concise notes; the overview must be a full sentence')]


@t23.add('C4', (2, 3, 4, 5), 'long')
def t23_two(r, D):
    (t1, x1, _, _, p1, mo1), (t2, x2, _, _, p2, mo2) = r.sample(PARAS, 2)
    form, reg = r.choice(SUM_FORMS)
    m = mk('C4', D, 'long')
    return {'stem': f'Read the two paragraphs. A: ‘{t1}’ {Q(clean(x1))} B: ‘{t2}’ {Q(clean(x2))} Summarise the key information from both paragraphs as {form}. Use your own words; about 100–120 words.',
            'answer': f'A: {mo1} B: {mo2}', 'key': levels_key(m, 'summary', f'A – {"; ".join(p1)}. B – {"; ".join(p2)}. Register: {reg}.')}

# ---------------------------------------------------------------- 2.4 writing an explanation
GAPS = [
    ('The sun heats the water in the lake. ____, some of it evaporates.', 'As a result', ['However', 'For example', 'Meanwhile'], 'cause and effect'),
    ('Seeds need water to germinate. ____ they need warmth and oxygen.', 'In addition,', ['Therefore,', 'Finally,', 'Nevertheless,'], 'adding information'),
    ('Most metals are good conductors. ____, plastic does not conduct electricity.', 'In contrast', ['As a result', 'Because of this', 'First'], 'contrast'),
    ('____ the mixture is heated, the water boils away and salt crystals remain.', 'When', ['Although', 'Unless', 'Despite'], 'time and condition'),
    ('First, the beans are picked and dried. ____, they are roasted at a high temperature.', 'Next', ['However', 'In contrast', 'For instance'], 'sequence'),
    ('Volcanoes erupt ____ pressure builds up in the magma chamber.', 'because', ['although', 'unless', 'whereas'], 'cause'),
    ('The ice cap reflects sunlight. ____, when it melts, more heat is absorbed by the dark ocean.', 'Consequently', ['For example', 'Meanwhile', 'Similarly'], 'cause and effect'),
    ('Many animals hibernate in winter. Bears, ____, may sleep for several months.', 'for example', ['therefore', 'however', 'as a result'], 'giving an example'),
    ('The battery stores chemical energy. ____ a circuit is complete, this energy is transferred to the bulb.', 'Once', ['Although', 'Whereas', 'Unless'], 'time'),
    ('Paper is pulped and cleaned. ____, it is pressed into thin sheets and dried.', 'Finally', ['However', 'Despite this', 'For example'], 'sequence (last step)'),
]
MUDDLED = [
    ('Rewrite this explanation so that it is clear, in the right order and uses connectives.', 'The bread rises. You mix flour, water and yeast. The yeast makes gas. You bake it. You leave it somewhere warm.',
     'First, flour, water and yeast are mixed to make dough. The dough is then left somewhere warm, where the yeast feeds and produces carbon dioxide gas. As a result, the dough rises. Finally, it is baked.',
     'Award for: correct sequence; time and causal connectives; impersonal style; technical term (carbon dioxide).'),
    ('Improve this explanation by using technical vocabulary and a formal, impersonal style.', 'When water gets really hot it turns into steam and goes up, then it hits something cold and turns back into water again.',
     'When water is heated to its boiling point, it evaporates and becomes water vapour. When the vapour meets a cold surface, it condenses back into liquid water.',
     'Award for: evaporates/condenses/boiling point/vapour; passive or impersonal style; clear cause and effect.'),
    ('Rewrite this explanation in the correct order and join the ideas with cohesive devices.', 'Lava comes out. Pressure builds up. Magma rises under the ground. The volcano erupts.',
     'Deep underground, magma rises towards the surface. As it gathers, pressure builds up in the magma chamber. Eventually the pressure becomes too great and the volcano erupts, so lava flows out.',
     'Award for: sequence; causal links (as, so, eventually); technical words kept accurately.'),
    ('Make this explanation more precise and cohesive.', 'Plants need stuff to make food. They use light. They take in things from the air and the ground.',
     'Plants make their own food by photosynthesis. Using light energy, they combine carbon dioxide from the air with water absorbed by their roots to produce glucose and oxygen.',
     'Award for: technical vocabulary (photosynthesis, carbon dioxide, glucose); precise nouns replacing ‘stuff’/‘things’; cohesive structure.'),
    ('Rewrite this so that it explains rather than simply lists.', 'Earthquakes. Plates move. Pressure. Shaking. Damage to buildings.',
     'Earthquakes happen because the plates of the Earth’s crust move. When plates stick, pressure builds; when it is suddenly released, the ground shakes, which can damage buildings.',
     'Award for: full sentences; causal connectives; logical chain of cause and effect.'),
]
PROCESSES = [
    ('how a rainbow forms', 'sunlight entering raindrops; refraction (bending) and dispersion into colours; reflection inside the drop; light leaving at different angles; the sun must be behind the observer.'),
    ('how bread rises', 'yeast is a living micro-organism; it feeds on sugars in warm conditions; it produces carbon dioxide gas; gas is trapped in the stretchy dough (gluten); baking sets the structure.'),
    ('how paper is recycled', 'collection and sorting; pulping with water; removing ink and contaminants; pressing and drying into new sheets; benefits such as saving trees and energy.'),
    ('how a bicycle’s gears make cycling easier on hills', 'pedals turn the front chainwheel; the chain drives a rear cog; a larger rear cog means the wheel turns less per pedal stroke; less force needed but more pedalling.'),
    ('how a fridge keeps food cold', 'a refrigerant liquid evaporates inside the fridge and absorbs heat; a compressor pumps it outside; it condenses and releases heat at the back.'),
    ('why the moon appears to change shape', 'the moon reflects sunlight; half is always lit; as it orbits the Earth we see different amounts of the lit half; phases from new moon to full moon over about a month.'),
    ('how a cut on your skin heals', 'blood clots to seal the wound; a scab forms; white blood cells fight infection; new skin cells grow underneath; the scab falls off.'),
    ('how sound travels from a drum to your ear', 'the drum skin vibrates; vibrations pass through air particles as a wave; they reach the eardrum and make it vibrate; the brain interprets the signal as sound.'),
]
t24 = topic('Writing a clear explanation', 'writing a clear explanation', 'technical vocabulary', 'cohesive devices')
t24.fixed('C1', (1, 2), [
    ('What is a cohesive device?', 'A word or phrase that links ideas across sentences and paragraphs', 'E.g. connectives (therefore), pronouns referring back (this process), and repetition of key nouns.',
     ['A full stop at the end of a sentence', 'A heading in bold type', 'A word that describes a noun']),
    ('Which phrase links back to an idea already explained?', 'This process', '‘This process’ refers back, binding the explanation together.', ['Once upon a time', 'In my view', 'Suddenly']),
    ('Which sentence is written in an impersonal style suitable for an explanation?', 'The mixture is heated until it boils.', 'Impersonal/passive style focuses on the process, not the person.',
     ['I heated my mixture until it boiled, which was fun.', 'You should totally heat it till it boils.', 'We loved watching it boil!']),
])


@t24.add('C1', (1, 2, 3))
def t24_gap(r, D):
    s, a, ds, fn = r.choice(GAPS)
    opts, ans = mcq(r, a, ds)
    return {'stem': f'Choose the connective that best completes this explanation: {Q(s)}', 'options': opts, 'answer': ans, 'key': f'‘{a}’ signals {fn}.'}


@t24.add('C2', (2, 3, 4), 'explain')
def t24_gap_explain(r, D):
    s, a, ds, fn = r.choice(GAPS)
    wrong = r.choice(ds)
    return {'stem': f'A student completed this sentence with ‘{wrong}’: {Q(s)} Explain why ‘{a}’ would be a better choice.',
            'answer': f'‘{a}’ shows {fn}, which is the relationship between the ideas; ‘{wrong}’ signals a different relationship and confuses the logic.',
            'key': keypts(f'1 mark: identifies the relationship ({fn}); 1 mark: explains why ‘{wrong}’ is wrong; a further mark for a clear comment on the reader’s understanding.')}


rewrite_templates(t24, MUDDLED, ['{ins} {q}', 'Here is a student’s draft explanation: {q} {ins}'])
writing_templates(t24, [(f'Write an explanation of {p} for a science magazine aimed at readers of your age. Use technical vocabulary, cohesive devices and a clear sequence.',
                         ind, f'Model structure: title as a question; opening definition; paragraphs following the process step by step with causal and time connectives; a closing sentence on why it matters. Key content: {ind}')
                        for p, ind in PROCESSES] +
                       [(f'Write an explanation of {p} for a younger student. Include a short introduction, steps in order and a concluding sentence.',
                         ind, f'Model structure: simple question title; short definition; three or four steps with ‘first’, ‘then’, ‘as a result’; technical words explained in brackets. Key content: {ind}')
                        for p, ind in PROCESSES], 'explanation')
CHAPTERS[2] = [t21, t22, t23, t24]


# =========================================================== Unit 3 Poetry: imagery, sound and form

HARBOUR = Text('harbour', 'poem', 'the poem ‘Harbour at Dawn’', """
The harbour wakes with a yawn of grey;
the fishing boats nod and creak and sway.
Gulls stitch the sky with silver thread
above the nets like cobwebs spread.
The water lies as still as stone
and holds each mast as if its own,
till a radio crackles, coughs and hums,
and the first bright engine roars. Day comes.
""", poem=True)
HARBOUR.f('The harbour wakes with a yawn of grey', 'personification', 'wakes with a yawn',
          'the harbour is presented like a sleepy person getting up, creating a gentle, drowsy, early-morning mood.')
HARBOUR.f('Gulls stitch the sky with silver thread', 'metaphor', 'stitch the sky with silver thread',
          'the gulls’ flight paths become threads sewn across the sky, suggesting delicate, criss-crossing movement and light catching their wings.', also=('alliteration', 'sibilance'))
HARBOUR.f('above the nets like cobwebs spread', 'simile', 'like cobwebs',
          'the nets look fine, grey and delicate, and the image of cobwebs hints that they have been left still overnight.')
HARBOUR.f('The water lies as still as stone', 'simile', 'as still as stone',
          'the comparison emphasises complete calm and heaviness, as if the water is solid; the ‘s’ sounds add hush.', also=('alliteration', 'sibilance'))
HARBOUR.f('till a radio crackles, coughs and hums', 'onomatopoeia', 'crackles, coughs and hums',
          'the sound words bring the first human noise into the silence, showing the quiet morning beginning to break.', also=('personification', 'listing'))
HARBOUR.f('and the first bright engine roars. Day comes.', 'short sentence', 'Day comes.',
          'the abrupt two-word sentence after the roar marks the moment night ends, giving a firm, final sense of arrival.')
HARBOUR.f('the fishing boats nod and creak and sway', 'personification', 'nod',
          'the boats seem half-asleep, nodding like drowsy people, which continues the image of the harbour waking.')
HARBOUR.x('How does the poet present the harbour waking up?', 'Personification of harbour and boats as sleepy; quiet images (cobwebs, still as stone); sound builds from creaks to radio to engine roar; regular rhyming couplets give a gentle rhythm until the caesura and final short sentence.')

KITCHEN = Text('kitchen', 'poem', 'the poem ‘Grandmother’s Kitchen’', """
In my grandmother's kitchen
the kettle is always
about to sing.
Spices sleep in their jars,
cumin, turmeric, clove,
small brown secrets
she never wrote down.
Her hands are maps
of every meal she has made,
and when she laughs
the whole room
leans in to listen.
""", poem=True)
KITCHEN.f('the kettle is always / about to sing', 'personification', 'about to sing',
          'the kettle seems cheerful and alive, suggesting a warm, welcoming kitchen that is always ready for visitors.')
KITCHEN.f('Spices sleep in their jars', 'personification', 'sleep',
          'the spices seem peaceful and resting, waiting to be ‘woken’ by cooking; the sibilance adds softness.', also=('sibilance', 'alliteration'))
KITCHEN.f('small brown secrets / she never wrote down', 'metaphor', 'small brown secrets',
          'calling the spices secrets suggests her recipes are private knowledge passed on by memory, valuable and mysterious.')
KITCHEN.f('Her hands are maps / of every meal she has made', 'metaphor', 'Her hands are maps',
          'her lined, worn hands record a lifetime of cooking, suggesting experience, history and the love she has given through food.', also=('alliteration',))
KITCHEN.f('the whole room / leans in to listen', 'personification', 'leans in to listen',
          'the room itself seems drawn to her laughter, showing how she is the warm centre of the family.', also=('alliteration',))
KITCHEN.f('cumin, turmeric, clove,', 'listing', 'cumin, turmeric, clove',
          'naming the spices gives specific sensory detail and cultural identity, and the list sounds like a chant or recipe.')
KITCHEN.x('How does the poet present the grandmother and her kitchen?', 'Personification makes the kitchen alive and welcoming; metaphors of secrets and maps show experience and memory; free verse and enjambment create a conversational, affectionate tone; ending focuses on her warmth.')

BOOTS = Text('boots', 'poem', 'the poem ‘My Father’s Boots’', """
By the back door my father's boots
stand guard, still caked with field;
they lean on one another
like two old soldiers home from war.
He has not worn them since the spring.
Each morning I walk past them, slow,
and every morning they say nothing,
and every morning I say nothing back.
""", poem=True)
BOOTS.f("By the back door my father's boots / stand guard", 'personification', 'stand guard',
        'the boots seem loyal and watchful, as if still on duty for the absent father, which makes his absence more painful.')
BOOTS.f('they lean on one another / like two old soldiers home from war', 'simile', 'like two old soldiers home from war',
        'the boots seem tired, battered and supporting each other, suggesting hard work, endurance and perhaps loss.')
BOOTS.f('He has not worn them since the spring.', 'short sentence', 'He has not worn them since the spring.',
        'the plain, end-stopped line stands alone and hints at illness, absence or death without explaining, creating a sad mystery.')
BOOTS.f('and every morning they say nothing, / and every morning I say nothing back.', 'repetition', 'every morning',
        'the repeated phrase shows a daily, unchanging ritual of grief and silence; the speaker cannot talk about the loss.')
BOOTS.x('How does the poet use the boots to explore the speaker’s feelings about their father?', 'Boots as a symbol of the absent father; personification (stand guard, say nothing); soldier simile; the short, blunt line about spring; repetition showing ongoing grief; restrained tone.')

CITYRAIN = Text('cityrain', 'poem', 'the poem ‘City Rain’', """
Rain arrives in the city
without knocking.
It drums on bus shelters,
slicks the streets to mirrors,
turns every gutter
into a gossiping river.
Umbrellas bloom like black flowers.
A taxi hisses past.
And for a moment
the whole loud city
holds its breath
and listens.
""", poem=True)
CITYRAIN.f('Rain arrives in the city / without knocking.', 'personification', 'without knocking',
           'the rain is like a rude, unexpected visitor, suggesting it comes suddenly and takes over the city.')
CITYRAIN.f('It drums on bus shelters,', 'onomatopoeia', 'drums',
           'the word imitates the loud, rhythmic beat of rain on metal and plastic, bringing the noise of the city into the poem.')
CITYRAIN.f('slicks the streets to mirrors,', 'metaphor', 'slicks the streets to mirrors',
           'wet streets become shiny reflective surfaces, suggesting light and colour reflected everywhere; ‘slicks’ suggests speed and smoothness.', also=('sibilance', 'alliteration'))
CITYRAIN.f('turns every gutter / into a gossiping river.', 'personification', 'gossiping river',
           'the running water seems to chatter like people sharing news, capturing its constant, busy sound.', also=('metaphor',))
CITYRAIN.f('Umbrellas bloom like black flowers.', 'simile', 'like black flowers',
           'umbrellas opening suddenly are compared to flowers opening, an unexpected, beautiful image in a grey city.', also=('alliteration',))
CITYRAIN.f('A taxi hisses past.', 'onomatopoeia', 'hisses',
           'the hissing sound of tyres on wet roads is captured exactly, and the short line mirrors the quick passing.', also=('short sentence', 'sibilance'))
CITYRAIN.f('the whole loud city / holds its breath / and listens.', 'personification', 'holds its breath',
           'the city becomes a person pausing in wonder, creating a calm, reflective ending after the noise.')
CITYRAIN.x('How does the poet present the effect of rain on the city?', 'Personification (without knocking, gossiping, holds its breath); onomatopoeia (drums, hisses); metaphors and similes of mirrors and flowers; free verse with short lines and enjambment; shift from noise to stillness.')

DROUGHT = Text('drought', 'poem', 'the poem ‘Drought’', """
The sky is hard and white as bone,
the river is a path of stone;
the cattle stand with lowered heads
in fields of dry and dusty beds.
We watch the west for days on end
for any cloud the wind might send,
and when at last the thunder rolls,
we run outside with cups and bowls.
""", poem=True)
DROUGHT.f('The sky is hard and white as bone,', 'simile', 'white as bone',
          'the harsh, pale sky is linked to bones, suggesting dryness, death and a landscape stripped bare.')
DROUGHT.f('the river is a path of stone;', 'metaphor', 'a path of stone',
          'the river has dried up completely; the shocking image shows how severe the drought is.')
DROUGHT.f('in fields of dry and dusty beds.', 'alliteration', 'dry and dusty',
          'the hard ‘d’ sounds stress the dryness and make the line sound heavy and tired.')
DROUGHT.f('We watch the west for days on end', 'alliteration', 'watch the west',
          'the repeated ‘w’ sound slows the line, suggesting long, anxious waiting and hope.')
DROUGHT.f('and when at last the thunder rolls, / we run outside with cups and bowls.', 'rhyming couplet', 'rolls',
          'the final rhyming couplet brings a satisfying, joyful release as the rain arrives, matching the relief in the content.')
DROUGHT.x('How does the poet show the effects of drought and the relief when it ends?', 'Similes and metaphors of bone and stone; sad image of cattle; alliteration of dry/dusty; regular rhyme and steady metre suggest the long wait; final couplet shifts to joy and action.')

TREE = Text('tree', 'poem', 'the poem ‘The Tree Outside My Window’', """
In January it is a skeleton,
all elbows and knuckles,
scratching at the glass.
By April it has changed its mind:
a green rumour spreads
from twig to twig.
July, and it is a crowded room
of leaves and gossip,
of birds that never sleep.
And I, who have not moved all year,
watch it become
three different trees.
""", poem=True)
TREE.f('In January it is a skeleton,', 'metaphor', 'a skeleton',
       'the bare winter tree is bony and lifeless, a slightly frightening image of death.')
TREE.f('all elbows and knuckles, / scratching at the glass.', 'personification', 'scratching at the glass',
       'the tree seems to reach out and claw at the window, creating an eerie, restless winter mood.', also=('metaphor',))
TREE.f('By April it has changed its mind:', 'personification', 'changed its mind',
       'the tree seems to decide to live again, giving a playful sense of spring as a choice.')
TREE.f('a green rumour spreads / from twig to twig.', 'metaphor', 'a green rumour',
       'new buds appear gradually like gossip passing from person to person, a fresh image of spring spreading.', also=('alliteration',))
TREE.f('July, and it is a crowded room / of leaves and gossip,', 'metaphor', 'a crowded room',
       'the full summer tree is busy and noisy like a party, full of life and sound.')
TREE.f('And I, who have not moved all year,', 'contrast', 'who have not moved all year',
       'the still speaker contrasts with the changing tree, suggesting the speaker feels stuck or reflective.')
TREE.x('How does the poet use the structure and imagery of the poem to show change?', 'Three seasonal stanzas (January, April, July) give a chronological structure; metaphors move from death (skeleton) to rumour to crowded room; final stanza turns to the motionless speaker – a shift that invites reflection.')

POEMS = [HARBOUR, KITCHEN, BOOTS, CITYRAIN, DROUGHT, TREE]

# ---------------------------------------------------------------- 3.1 imagery
t31 = topic('Imagery in poetry', 'imagery in poetry', 'simile metaphor personification')
t31.fixed('C1', (1, 2), [
    ('What is the difference between a simile and a metaphor?', 'A simile compares using ‘like’ or ‘as’; a metaphor says one thing is another', 'Simile: as still as stone. Metaphor: the river is a path of stone.',
     ['A simile rhymes; a metaphor does not', 'A metaphor uses ‘like’; a simile does not', 'There is no difference']),
    ('Which line contains personification?', 'The wind whispered secrets to the trees.', 'The wind is given a human action (whispering).',
     ['The wind was as cold as ice.', 'The wind is a knife.', 'The wind blew from the north.']),
    ('What is imagery?', 'Language that creates pictures or sensations in the reader’s mind', 'Imagery appeals to the senses and includes similes, metaphors and personification.',
     ['The pattern of rhymes in a poem', 'The number of stanzas in a poem', 'The title of a poem']),
    ('‘The classroom was a zoo.’ Which technique is this an example of?', 'a metaphor', 'It says the classroom IS a zoo, without ‘like’ or ‘as’.', ['a simile', 'onomatopoeia', 'alliteration']),
    ('What is an extended metaphor?', 'A comparison that is developed over several lines or a whole poem', 'E.g. a tree presented as a person throughout a poem.',
     ['A metaphor that is very long and has many adjectives', 'A simile with two ‘likes’', 'A rhyme that continues for a stanza']),
])
IMG_FEATS = [f for T in POEMS for f in T.feats if f.device in IMAGERY]
feature_templates(t31, IMG_FEATS, IMAGERY)
IMG_WRITE = [('the sea during a storm', 'simile'), ('a crowded railway station', 'metaphor'), ('the moon on a winter night', 'personification'), ('a city at midnight', 'metaphor'),
             ('a cat waiting by a mouse hole', 'simile'), ('the first day of the monsoon', 'personification'), ('an old bicycle', 'personification'), ('a desert at noon', 'simile'),
             ('fireworks over a river', 'metaphor'), ('a library late in the evening', 'personification')]


@t31.add('C3', (1, 2, 3, 4), 'short')
def t31_write(r, D):
    subj, dev = r.choice(IMG_WRITE)
    m = mk('C3', D)
    ex = {'simile': 'e.g. ‘The waves hurled themselves at the cliffs like furious wrestlers.’', 'metaphor': 'e.g. ‘The station was a beehive of hurrying people.’',
          'personification': 'e.g. ‘The moon peered nervously through the bare branches.’'}[dev]
    return {'stem': f'Write one original line of poetry that uses {dev} to describe {subj}. Then explain the effect you intended.',
            'answer': f'Any original {dev} about {subj}, {ex} with an explanation of the mood or picture created.',
            'key': f'{upto(m)}: 1 for an accurate {dev}; 1 for originality/aptness (not a cliché); remaining mark(s) for explaining the intended effect.'}


extended_templates(t31, POEMS)
compose_templates(t31, POEMS, C=('C4',))

# ---------------------------------------------------------------- 3.2 sound and rhythm
SOUND_LINES = [
    ('The slow black slug slid silently across the step.', 'sibilance', 'the repeated ‘s’ sounds imitate the slug’s quiet, slippery movement.', ()),
    ('Deep in the cold of the old stone hold', 'assonance', 'the repeated long ‘o’ sound creates a hollow, echoing, gloomy effect.', ('internal rhyme',)),
    ('Crack! went the branch, and the wild wind howled.', 'onomatopoeia', '‘Crack!’ and ‘howled’ imitate the violent noises of the storm.', ('alliteration',)),
    ('Big boots banged on the bare boards of the bridge.', 'alliteration', 'the heavy repeated ‘b’ sounds imitate thudding footsteps.', ('onomatopoeia',)),
    ('Light the fire high and bright tonight', 'internal rhyme', 'rhymes inside the line (light/bright/tonight) make it chant-like and energetic.', ('assonance',)),
    ('The moon was pale, the night was cold; / the tale was long, the teller old.', 'rhyming couplet', 'the two rhyming lines (cold/old) give a neat, storytelling closure.', ('assonance', 'repetition', 'internal rhyme')),
    ('Fizz, pop and sizzle went the pan on the stove.', 'onomatopoeia', 'the sound words make the cooking noisy and lively.', ('sibilance',)),
    ('Through misty mornings the mournful mill-wheel moans', 'alliteration', 'the soft repeated ‘m’ sounds create a low, sad hum.', ('assonance', 'onomatopoeia')),
    ('Hush now, the shadows are shifting and sighing', 'sibilance', 'soft ‘sh’ and ‘s’ sounds create a whispering, secretive mood.', ('alliteration',)),
    ('Again and again and again the waves return', 'repetition', 'the repeated word mirrors the endless rhythm of the sea.', ()),
    ('The rain came down, the rain came down, the rain came down all day.', 'repetition', 'repeating the phrase makes the rain seem relentless and dull.', ()),
    ('Sweet, deep sleep will keep you till the dawn', 'assonance', 'the long ‘ee’ sounds are soothing and drawn-out, like a lullaby.', ('internal rhyme',)),
]
t32 = topic('Sound and rhythm in poetry', 'sound and rhythm', 'alliteration assonance rhyme metre')
t32.fixed('C1', (1, 2), [
    ('What is metre in poetry?', 'The regular pattern of stressed and unstressed syllables in a line', 'E.g. iambic metre: da-DUM da-DUM.', ['The number of stanzas', 'The rhyme at the end of each line', 'The length of the title']),
    ('What is the rhyme scheme of a stanza whose lines end ‘grey / sway / thread / spread’?', 'AABB', 'grey/sway rhyme (A), thread/spread rhyme (B): rhyming couplets.', ['ABAB', 'ABCD', 'ABBA']),
    ('Which word is an example of onomatopoeia?', 'sizzle', 'Sizzle imitates the sound it names.', ['silent', 'sunlight', 'slowly']),
    ('What is assonance?', 'Repetition of vowel sounds in nearby words', 'E.g. ‘the cold of the old stone hold’.', ['Repetition of consonant sounds at the start of words', 'A word that imitates a sound', 'Rhyme at the end of lines']),
    ('Why might a poet use a steady, regular rhythm?', 'To create a sense of order, calm or a repeated movement such as walking', 'Regular metre can mimic movement or suggest control; broken rhythm suggests disruption.',
     ['To make the poem impossible to read aloud', 'To avoid using any rhyme', 'Because poems must always have regular rhythm']),
    ('The line ‘The sky is hard and white as bone’ has a da-DUM da-DUM rhythm. What is this rhythm called?', 'iambic metre', 'Iambs = unstressed + stressed syllables (the SKY is HARD...).', ['free verse', 'blank page', 'a refrain']),
])
SOUND_FEATS = [f for T in POEMS for f in T.feats if f.device in SOUND] + [Feat(type('S', (), {'label': 'a poem'})(), q, d, q if len(q) < 40 else q.split(' / ')[0], e, a) for q, d, e, a in SOUND_LINES]
feature_templates(t32, SOUND_FEATS, SOUND)
SCHEMES = [(HARBOUR, 'AABB (rhyming couplets)', 'grey/sway, thread/spread, stone/own, hums/comes'), (DROUGHT, 'AABB (rhyming couplets)', 'bone/stone, heads/beds, end/send, rolls/bowls'),
           (CITYRAIN, 'no regular rhyme scheme (free verse)', 'line endings such as city/knocking/shelters do not rhyme'), (KITCHEN, 'no regular rhyme scheme (free verse)', 'kitchen/always/sing do not rhyme')]


@t32.add('C3', (2, 3, 4, 5), 'explain')
def t32_scheme(r, D):
    T, sch, ev = r.choice(SCHEMES)
    m = mk('C3', D)
    return {'stem': f'Read {T.label}: {Q(T.text)} Identify the rhyme scheme and explain how the poem’s sound and rhythm suit its subject.',
            'answer': f'{sch}: {ev}. ' + ('The regular rhyme and steady metre create a calm, ordered or song-like effect matching the subject.' if 'AABB' in sch else 'The lack of rhyme and the uneven line lengths give a natural, conversational movement that suits the subject.'),
            'key': f'{upto(m)}: 1 for the correct rhyme scheme with evidence; remaining marks for linking rhythm/sound to mood or meaning (e.g. onomatopoeia, alliteration, line length).'}


SOUND_TASKS = [
    ('Write a poem of two or three stanzas about a thunderstorm, using onomatopoeia, alliteration and at least one rhyming couplet.', 'onomatopoeia for thunder and rain; alliteration; a rhyming couplet; sound building to a climax and fading.'),
    ('Write a poem about a busy kitchen at dinner time that uses sound devices to bring the scene to life.', 'onomatopoeia (sizzle, clatter); sibilance; rhythm that speeds up and slows down; sensory detail.'),
    ('Write a lullaby-style poem for a younger child about the night sky, using assonance and a regular rhythm.', 'long soothing vowel sounds; regular metre; gentle rhyme; repetition or refrain.'),
    ('Write a poem about a train journey whose rhythm imitates the movement of the train.', 'regular, repeated metre or repetition mimicking wheels; onomatopoeia; changing pace at stations.'),
    ('Write a short poem about the sea in which the sound of the words matches the movement of the waves.', 'sibilance or long vowels for waves; repetition; enjambment or line length mirroring motion.'),
]
writing_templates(t32, [(s, ind, f'Model features: {ind} Example line: ‘The sizzle and spit of the pan on the flame.’') for s, ind in SOUND_TASKS],
                  ('a poem that uses sound devices skilfully and purposefully; sound and rhythm clearly support the subject and mood; well-shaped stanzas',
                   'some effective sound devices; some sense of rhythm; recognisable poetic form', 'few sound devices or used mechanically; little sense of form or rhythm'))

# ---------------------------------------------------------------- 3.3 form and structure
FORM_TERMS = ['enjambment', 'caesura', 'end-stopped line', 'free verse', 'stanza', 'refrain', 'rhyming couplet']
FORM_SNIP = [
    ('the kettle is always / about to sing.', 'enjambment', 'the sentence runs over the line break, making the reader wait for ‘sing’, like waiting for the kettle.'),
    ('and the first bright engine roars. Day comes.', 'caesura', 'the full stop mid-line creates a pause that marks the sudden arrival of day.'),
    ('He has not worn them since the spring.', 'end-stopped line', 'the line ends with a full stop, so the sad fact stands alone and the reader pauses on it.'),
    ('the whole loud city / holds its breath / and listens.', 'enjambment', 'the lines run on, slowing the ending so the reader also pauses and ‘listens’.'),
    ('turns every gutter / into a gossiping river.', 'enjambment', 'the run-on line mimics the water flowing on into the gutter.'),
    ('Here I stand. I wait. The tide comes in.', 'caesura', 'several full stops in one line create halting pauses that suggest hesitation or tension.'),
    ('Rain arrives in the city / without knocking.', 'enjambment', 'the line break holds back ‘without knocking’, giving it surprise, like the rain itself.'),
    ('Sing me home, sing me home, / over the hills, sing me home.', 'refrain', 'the repeated phrase works like a chorus, giving a song-like, longing quality.'),
    ('The sky is hard and white as bone,', 'end-stopped line', 'the line ends with punctuation, giving a firm, steady rhythm that matches the harsh, still heat.'),
    ('and when at last the thunder rolls, / we run outside with cups and bowls.', 'rhyming couplet', 'the rhyme gives a satisfying, celebratory finish.'),
]
STANZA_TERMS = [('couplet', 'two lines'), ('tercet', 'three lines'), ('quatrain', 'four lines'), ('sestet', 'six lines'), ('octave', 'eight lines')]
t33 = topic('Poetic forms and structure', 'poetic forms and structure', 'stanzas enjambment free verse')
t33.fixed('C1', (1, 2), [
    ('What is free verse?', 'Poetry without a regular rhyme scheme or metre', 'Free verse follows natural speech rhythms; line breaks still matter.', ['Poetry that is free to read online', 'Poetry with exactly fourteen lines', 'Poetry that must rhyme in couplets']),
    ('What is a stanza?', 'A group of lines forming a section of a poem', 'Stanzas are like paragraphs in poetry.', ['A single word that rhymes', 'The title of a poem', 'The last line of a poem']),
    ('What is a volta?', 'A turn or shift in thought or mood in a poem', 'Often signalled by ‘But’, ‘Yet’ or a new stanza, e.g. the final stanza of ‘The Tree Outside My Window’.', ['A type of rhyme', 'A line of eight syllables', 'A repeated chorus']),
    ('What is a sonnet?', 'A fourteen-line poem with a set rhyme scheme', 'Traditional sonnets have 14 lines, often in iambic pentameter.', ['A poem of three lines about nature', 'Any poem that tells a story', 'A poem with no punctuation']),
    ('What is a haiku?', 'A three-line poem, traditionally of 5, 7 and 5 syllables', 'A Japanese form often focused on nature and a single moment.', ['A fourteen-line love poem', 'A long narrative poem', 'A poem in rhyming couplets']),
    ('What is a ballad usually?', 'a poem that tells a story, often in quatrains with a regular rhythm', 'Ballads are narrative, song-like poems.', ['a poem with no rhythm', 'a single-line poem', 'a description of one object']),
])
classify_templates(t33, FORM_SNIP, FORM_TERMS,
                   ['Which structural feature is shown in these lines? {q}', 'Read the lines (a slash shows a line break): {q} Which feature of form is used?'],
                   C2frames=['These lines use {label}: {q} Explain the effect of this structural choice.', 'Explain how the use of {label} affects the way a reader reads these lines: {q}'],
                   C3frames=[('Identify the structural feature in these lines and analyse why the poet might have used it: {q}', lambda it: f'{cap(it[1])}: {it[2]}',
                              lambda it, m: f'{upto(m)}: 1 for {it[1]}; remaining marks for an analysis that links the structure to meaning or mood.')])


@t33.add('C1', (1, 2, 3))
def t33_stanza(r, D):
    name, lines = r.choice(STANZA_TERMS)
    opts, ans = mcq(r, name, [n for n, _ in STANZA_TERMS if n != name])
    return {'stem': f'What is the name for a stanza of {lines}?', 'options': opts, 'answer': ans, 'key': f'A {name} has {lines}.'}


STRUCT_Q = [
    (TREE, 'Explain how the poet organises the poem, and why the final stanza is different.', 'Three stanzas follow the seasons in chronological order (January, April, July), each with a new metaphor. The final stanza turns (a volta) to the still speaker, contrasting their lack of change with the tree.'),
    (CITYRAIN, 'Explain how the use of short lines and line breaks contributes to the poem’s effect.', 'Short lines and enjambment create pauses and surprise (‘without knocking’), mimic quick sounds (‘A taxi hisses past.’) and slow the ending so the reader pauses with the city.'),
    (BOOTS, 'Explain how the structure of the poem reflects the speaker’s feelings.', 'One stanza of quiet observation; the central end-stopped line about spring stands out; the final repeated lines create a cycle of silence, reflecting stuck, unspoken grief.'),
    (HARBOUR, 'Explain how the form of the poem suits its subject.', 'Regular rhyming couplets and steady metre give a calm, rocking rhythm like boats on the water; the caesura in the final line breaks the pattern as day arrives.'),
    (DROUGHT, 'Explain how the poet structures the poem to move from suffering to relief.', 'Lines 1–4 describe the drought; lines 5–6 the waiting; the final couplet turns with ‘when at last’ to sudden joyful action.'),
    (KITCHEN, 'Explain why the poet might have chosen free verse for this poem.', 'Free verse sounds like natural, affectionate speech, suiting personal memory; enjambment creates gentle anticipation (‘always / about to sing’).'),
]


@t33.add('C3', (3, 4, 5), 'explain')
def t33_struct(r, D):
    T, q, a = r.choice(STRUCT_Q)
    m = mk('C3', D)
    return {'stem': f'Read {T.label}: {Q(T.text)} {q}', 'answer': a, 'key': f'{upto(m)}: 1 per valid structural point (stanza, line length, enjambment, caesura, rhyme, volta) linked to effect, with reference.'}


FORM_TASKS = [
    ('Write a poem of three stanzas about a place you know well at three different times of day, using enjambment at least twice.', 'three stanzas with a clear time sequence; enjambment for effect; a final turn or reflection.'),
    ('Write a free-verse poem about an object that reminds you of someone, ending with a stanza that shifts in mood.', 'free verse; object as symbol; a volta in the final stanza.'),
    ('Write a sequence of three haiku about the changing seasons in your country.', 'three haiku in 5-7-5 syllables; one moment per haiku; seasonal imagery.'),
    ('Write a short ballad of three or four quatrains that tells the story of a journey.', 'narrative in quatrains; regular rhythm; ABCB or ABAB rhyme; story with a clear ending.'),
    ('Write a poem in rhyming couplets about a market, then add one line that breaks the pattern for effect.', 'consistent couplets; a deliberate break in form at a key moment.'),
]
writing_templates(t33, [(s, ind, f'Model features: {ind}') for s, ind in FORM_TASKS],
                  ('form handled deliberately and accurately; structural choices (stanzas, line breaks, rhyme) clearly linked to meaning', 'recognisable form with some deliberate choices', 'form loosely followed; little sense of structure'))

# ---------------------------------------------------------------- 3.4 comparing poems
PAIRS = [
    (KITCHEN, BOOTS, 'family members and memory',
     'Both use a household object or place to represent a family member (kitchen, boots) and both use personification. ‘Grandmother’s Kitchen’ is warm and celebratory; ‘My Father’s Boots’ is restrained and sad, suggesting loss. Both use free verse, but the repetition in ‘My Father’s Boots’ creates a cycle of silence while the enjambment in ‘Grandmother’s Kitchen’ creates warmth.'),
    (CITYRAIN, DROUGHT, 'weather and its effects on people',
     'Both personify or vividly picture the weather. ‘City Rain’ shows rain as an everyday, noisy visitor in free verse; ‘Drought’ shows the desperate absence of rain in regular couplets, ending with joy when it finally arrives. Onomatopoeia dominates ‘City Rain’; harsh images (bone, stone) dominate ‘Drought’.'),
    (HARBOUR, TREE, 'change and the passing of time',
     '‘Harbour at Dawn’ shows change over one morning using personification and building sound; ‘The Tree Outside My Window’ shows change over a year through seasonal stanzas and metaphor. The harbour poem ends with the arrival of day; the tree poem ends by turning to the speaker.'),
    (HARBOUR, CITYRAIN, 'places coming to life',
     'Both personify a place (the harbour wakes; the city holds its breath) and use onomatopoeia (crackles, drums, hisses). ‘Harbour at Dawn’ moves from silence to noise in rhyming couplets; ‘City Rain’ moves from noise to silence in free verse.'),
]
CMP_ASPECTS = ['the use of personification', 'the use of sound', 'the structure and form of the poems', 'the mood or tone created', 'the way each poem ends']
t34 = topic('Comparing two poems on a similar theme', 'comparing two poems', 'similar theme')
t34.fixed('C1', (1, 2), [
    ('Which connective is most useful for showing a similarity when comparing poems?', 'Similarly', 'Similarity: similarly, likewise, both. Difference: whereas, however, in contrast.', ['Whereas', 'In contrast', 'However']),
    ('Which connective signals a difference between two poems?', 'whereas', '‘whereas’ introduces a contrast in the same sentence.', ['likewise', 'similarly', 'also']),
    ('In a comparison essay, what is the best way to organise paragraphs?', 'Discuss both poems in each paragraph, focused on one point of comparison', 'Integrated comparison is stronger than writing about one poem then the other.',
     ['Write only about the poem you prefer', 'Summarise each poem without comparing', 'List all the techniques in both poems without explaining']),
    ('What must two poems do to share a theme?', 'explore a similar central idea, such as loss, nature or change', 'Theme = central idea or message.', ['have the same number of lines', 'are by the same poet', 'use the same rhyme scheme']),
])
t34.fixed('C2', (2, 3, 4), [(f'Read {A.label}: {Q(A.text)} and {B.label}: {Q(B.text)} Both poems are about {th}. Identify one similarity and one difference between them.', a,
                             '1 mark: valid similarity; 1 mark: valid difference; a further mark for supporting reference to both poems.') for A, B, th, a in PAIRS])


@t34.add('C3', (2, 3, 4, 5), 'explain')
def t34_aspect(r, D):
    A, B, th, a = r.choice(PAIRS)
    asp = r.choice(CMP_ASPECTS)
    m = mk('C3', D)
    fa = [f for f in A.feats][:3]
    fb = [f for f in B.feats][:3]
    return {'stem': f'Compare {asp} in {A.label} and {B.label}. Poem 1: {Q(A.text)} Poem 2: {Q(B.text)} Use a comparative connective and a short quotation from each poem.',
            'answer': f'{a} Possible references: {", ".join(Q(f.focus) for f in fa[:2])} / {", ".join(Q(f.focus) for f in fb[:2])}.',
            'key': f'{upto(m)}: point about poem 1 with evidence; comparative point about poem 2 with evidence; explanation of the effect of each; comparative connective used.'}


@t34.add('C2', (2, 3, 4), 'explain')
def t34_lines(r, D):
    A, B, th, a = r.choice(PAIRS)
    f, g = r.choice(A.feats), r.choice(B.feats)
    m = mk('C2', D)
    same = f.device == g.device
    return {'stem': f'Line from {A.label}: {Q(f.quote)} Line from {B.label}: {Q(g.quote)} Explain one similarity or difference in the way these two lines create an effect.',
            'answer': (f'Both use {f.device}: ' if same else f'The first uses {f.device}, whereas the second uses {g.device}: ') + f'{f.effect} By contrast/similarly, {g.effect}',
            'key': f'{upto(m)}: 1 for identifying the technique in each line; 1 for a comparative point about effect; credit any valid comparison.'}


@t34.add('C3', (2, 3, 4, 5), 'explain')
def t34_lines3(r, D):
    A, B, th, a = r.choice(PAIRS)
    f, g = r.choice(A.feats), r.choice(B.feats)
    m = mk('C3', D)
    return {'stem': f'Both poems explore {th}. Compare how the poets use language in these lines. Poem 1 ({A.label}): {Q(f.quote)} Poem 2 ({B.label}): {Q(g.quote)} Write a comparative paragraph using point, evidence and explanation for each.',
            'answer': f'Poem 1 uses {f.device} ({Q(f.focus)}): {f.effect} Poem 2 uses {g.device} ({Q(g.focus)}): {g.effect} A comparative link (e.g. ‘whereas’, ‘similarly’) should connect the two to the theme of {th}.',
            'key': f'{upto(m)}: technique and effect for poem 1; technique and effect for poem 2; comparative connective and a judgement linking both to the theme.'}


@t34.add('C4', (2, 3, 4, 5), 'long')
def t34_essay(r, D):
    A, B, th, a = r.choice(PAIRS)
    lead = r.choice([f'Compare how the poets present {th} in these two poems.', f'Compare the ways in which the two poets explore {th}.',
                     f'‘Both poems use everyday details to explore {th}.’ How far do you agree? Compare the two poems in your answer.'])
    m = mk('C4', D, 'long')
    return {'stem': f'Poem 1, {A.label}: {Q(A.text)} Poem 2, {B.label}: {Q(B.text)} {lead} Write about language, structure and the effect on the reader.',
            'answer': a, 'key': reading_key(m, a + ' Strong answers integrate comparison in each paragraph and use comparative connectives.')}


CHAPTERS[3] = [t31, t32, t33, t34]


# =========================================================== Unit 4 Persuasive and argument writing

BOTTLES = Text('bottles', 'persuasive', 'a persuasive article from a school magazine, ‘Ditch the Plastic Bottle’', """
Every day, our school throws away more than four hundred plastic bottles. Four hundred! Imagine them piled in the
playground: a glittering mountain of waste that will outlive every one of us. Is that really the legacy we want to leave?
Some people say that recycling solves the problem, but only a small fraction of all the plastic ever made has been
recycled. The rest is buried, burned or washed into the sea, where it chokes turtles and breaks down into tiny fragments
that end up in the fish we eat. The solution is simple, cheap and fair: install free water fountains and give every
student a refillable bottle. Other schools in our city have already done it. We can do it too, and we must start now.""")
BOTTLES.f('Every day, our school throws away more than four hundred plastic bottles.', 'statistic', 'more than four hundred',
          'a precise, large number makes the problem seem real and shocking, and gives the argument authority.')
BOTTLES.f('Imagine them piled in the playground', 'imperative', 'Imagine',
          'the command pulls the reader into picturing the waste, making the problem visual and personal.', also=('direct address',))
BOTTLES.f('a glittering mountain of waste that will outlive every one of us', 'metaphor', 'a glittering mountain of waste',
          'the image exaggerates the scale of the waste; ‘glittering’ ironically makes rubbish look attractive while ‘outlive’ stresses how long it lasts.', also=('hyperbole',))
BOTTLES.f('Is that really the legacy we want to leave?', 'rhetorical question', 'Is that really the legacy',
          'the question makes the reader feel responsible for the future and expects the answer ‘no’, pushing them to agree.', also=('inclusive pronoun',))
BOTTLES.f('Some people say that recycling solves the problem, but only a small fraction of all the plastic ever made has been recycled.', 'counter-argument', 'Some people say',
          'raising and then rebutting an opposing view makes the writer seem fair and well-informed while dismissing the objection.', also=('statistic',))
BOTTLES.f('where it chokes turtles and breaks down into tiny fragments that end up in the fish we eat', 'emotive language', 'chokes turtles',
          'the distressing image of suffering animals and contaminated food stirs pity and fear, making readers want to act.')
BOTTLES.f('The solution is simple, cheap and fair', 'rule of three', 'simple, cheap and fair',
          'three positive adjectives make the solution sound complete and hard to argue with; the rhythm is memorable.', also=('listing',))
BOTTLES.f('We can do it too, and we must start now.', 'inclusive pronoun', 'We can do it too',
          '‘we’ unites writer and readers as a team, ending on a confident call to action.', also=('imperative',))
BOTTLES.x('How does the writer try to persuade students to support refillable bottles?', 'Statistic and repetition (four hundred!); imperative ‘Imagine’; metaphor of a glittering mountain; rhetorical question; counter-argument rebutted; emotive turtles; rule of three; inclusive ‘we’ and urgent ending.')

APPEAL = Text('appeal', 'persuasive', 'a charity appeal, ‘Give a Child a Book’', """
Close your eyes and picture a classroom with no books. No stories, no atlases, no dictionaries. In parts of the world,
this is not imaginary; it is every school day. Amal is ten. She walks five kilometres to school each morning and shares
one tattered reader with six classmates. She dreams of being a doctor. For just five dollars a month, you can put a
library in her classroom. Five dollars: less than the price of a cinema ticket. Your gift will buy books, train teachers
and light up young minds. Don't wait for someone else to act. Give today, and give a child a future.""")
APPEAL.f('Close your eyes and picture a classroom with no books.', 'imperative', 'Close your eyes and picture',
         'commanding the reader to imagine makes them experience the lack of books personally.', also=('direct address',))
APPEAL.f('No stories, no atlases, no dictionaries.', 'rule of three', 'No stories, no atlases, no dictionaries',
         'the repeated ‘no’ in a list of three emphasises how much is missing and builds a sense of loss.', also=('listing', 'repetition'))
APPEAL.f('Amal is ten. She walks five kilometres to school each morning and shares one tattered reader with six classmates.', 'anecdote', 'Amal is ten',
         'a named child turns statistics into a real person, making the reader feel sympathy and connection.', also=('emotive language', 'short sentence'))
APPEAL.f('shares one tattered reader with six classmates', 'emotive language', 'one tattered reader',
         '‘tattered’ suggests worn-out, inadequate resources, stirring pity.', also=('statistic', 'anecdote'))
APPEAL.f('For just five dollars a month, you can put a library in her classroom.', 'direct address', 'you can put a library',
         'speaking to ‘you’ makes the reader feel personally powerful and responsible; ‘just’ minimises the cost.', also=('hyperbole', 'statistic'))
APPEAL.f('Your gift will buy books, train teachers and light up young minds.', 'rule of three', 'buy books, train teachers and light up young minds',
         'three benefits build to an inspiring climax, showing the gift’s wide impact.', also=('metaphor', 'listing', 'direct address'))
APPEAL.f("Don't wait for someone else to act.", 'imperative', "Don't wait",
         'the command creates urgency and makes the reader feel guilty if they do nothing.', also=('direct address',))
APPEAL.x('How does the writer use language to persuade readers to donate?', 'Imperatives; rule of three; anecdote of Amal; emotive ‘tattered’; direct address and minimising cost (‘just five dollars’, cinema ticket); metaphor ‘light up young minds’; urgent ending.')

SKATE = Text('skate', 'biased', 'a newspaper opinion column, ‘Skate Park Plan Is a Disaster Waiting to Happen’', """
The council's plan to build a skate park beside Jubilee Gardens is, quite simply, madness. The gardens are one of the
last peaceful places in our town, loved by families, pensioners and wildlife alike. Now the council wants to fill them
with concrete ramps and teenagers shouting at all hours. The park will cost $250,000. Local residents were consulted in
a survey last spring, but only 300 people replied. Everyone I have spoken to is against it. Supporters claim the park
will keep young people off the streets, but in my experience bored teenagers will cause trouble wherever they are. The
council should listen to the people who actually pay for it, before it is too late.""")
SKATE.f("The council's plan to build a skate park beside Jubilee Gardens is, quite simply, madness.", 'emotive language', 'madness',
        'the extreme, loaded word dismisses the plan without evidence and pushes the reader to share the writer’s anger.', also=('hyperbole',))
SKATE.f('loved by families, pensioners and wildlife alike', 'rule of three', 'families, pensioners and wildlife',
        'listing sympathetic groups suggests that everyone innocent will suffer from the plan.', also=('listing', 'emotive language'))
SKATE.f('Everyone I have spoken to is against it.', 'anecdote', 'Everyone I have spoken to',
        'a personal, unrepresentative sample is presented as if it were proof, which is misleading.', also=('hyperbole',))
SKATE.f('Supporters claim the park will keep young people off the streets, but in my experience bored teenagers will cause trouble wherever they are.', 'counter-argument', 'Supporters claim',
        'the opposing view is mentioned only to be dismissed with an opinion and a stereotype rather than evidence.', also=('anecdote',))
SKATE.x('How does the writer try to turn readers against the skate park, and how far is the article biased?', 'Loaded words (madness, disaster); stereotypes of teenagers; one-sided selection; a fact undermined by ‘only’; unrepresentative ‘everyone I have spoken to’; dismissive counter-argument; final appeal to taxpayers.')

U4_PERS = [BOTTLES, APPEAL, SKATE]

# ---------------------------------------------------------------- 4.1 persuasive techniques
PERS_WRITE = [('persuade your school to start a recycling club', 'rhetorical question'), ('persuade parents to let teenagers walk to school', 'statistic'),
              ('persuade the council to build more cycle lanes', 'rule of three'), ('persuade readers to adopt a rescue dog', 'emotive language'),
              ('persuade students to join the school choir', 'direct address'), ('persuade your town to plant more trees', 'imperative'),
              ('persuade people to switch off lights they are not using', 'inclusive pronoun'), ('persuade classmates to read more books', 'anecdote'),
              ('persuade a company to sponsor the school sports day', 'expert opinion'), ('persuade families to eat more vegetables', 'counter-argument')]
t41 = topic('Persuasive techniques', 'persuasive techniques', 'rhetorical questions emotive language rule of three')
t41.fixed('C1', (1, 2), [
    ('What is a rhetorical question?', 'A question asked for effect, without expecting an answer', 'E.g. ‘Is that really the legacy we want to leave?’', ['A question that must be answered in writing', 'A question asked by an expert', 'A question at the end of an exam']),
    ('Which sentence uses the rule of three?', 'Our parks should be clean, safe and welcoming.', 'Three linked adjectives give rhythm and emphasis.',
     ['Our parks should be clean.', 'Our parks are dirty and unsafe.', 'Do you like our parks?']),
    ('What is emotive language?', 'Words chosen to provoke a strong emotional reaction', 'E.g. ‘chokes turtles’, ‘tattered’.', ['Language used only in poetry', 'Technical scientific vocabulary', 'Language with no adjectives']),
    ('Which of these is an example of direct address?', 'You can make a difference today.', 'Direct address speaks to the reader as ‘you’.', ['They made a difference yesterday.', 'Differences are important.', 'I once made a difference.']),
    ('Why do persuasive writers use inclusive pronouns such as ‘we’ and ‘our’?', 'To make the reader feel part of a shared group or cause', '‘We’ suggests the writer and reader are on the same side.',
     ['To make the text more formal and distant', 'To show the writer is an expert', 'To avoid giving an opinion']),
])
PERS_FEATS = [f for T in U4_PERS for f in T.feats]
feature_templates(t41, PERS_FEATS, PERSUADE)


@t41.add('C3', (1, 2, 3, 4), 'short')
def t41_write(r, D):
    aim, dev = r.choice(PERS_WRITE)
    m = mk('C3', D)
    return {'stem': f'Write two sentences that {aim}. One of them must use {"an" if dev[0] in "aeiou" else "a"} {dev}. Underline or name the technique and explain why it would persuade the reader.',
            'answer': f'Any two persuasive sentences in which one is a clear {dev} ({DEF[dev]}), with a valid explanation of its persuasive effect.',
            'key': f'{upto(m)}: 1 for an accurate {dev}; 1 for persuasive purpose clearly served; remaining mark(s) for explaining the effect on the reader.'}


extended_templates(t41, U4_PERS)
compose_templates(t41, U4_PERS, C=('C4',))
PERS_TASKS = [
    ('Write an article for your school magazine persuading students to walk or cycle to school.', 'article'),
    ('Write a leaflet persuading visitors to protect a local beach or river.', 'article'),
    ('Write a letter to your headteacher persuading them to create a school garden.', 'letter'),
    ('Write a charity appeal persuading readers to donate to an animal rescue centre.', 'article'),
    ('Write an advertisement for a new after-school club, persuading students to join.', 'article'),
    ('Write a blog post persuading teenagers to spend one day a week without screens.', 'article'),
    ('Write a letter to your local council persuading them to improve the bus service for young people.', 'letter'),
    ('Write a magazine article persuading families to holiday in their own country rather than abroad.', 'article'),
]
_ptasks = [(s_, 'clear persuasive purpose; a range of techniques (rhetorical question, rule of three, emotive language, statistics, direct address, counter-argument); structured paragraphs; strong call to action.',
            'Model structure: hook (question or striking fact); problem; two or three reasons with evidence and emotive detail; counter-argument rebutted; call to action.') for s_, g in PERS_TASKS]
writing_templates(t41, [x for x, (_, g) in zip(_ptasks, PERS_TASKS) if g == 'article'], 'argument')
writing_templates(t41, [x for x, (_, g) in zip(_ptasks, PERS_TASKS) if g == 'letter'], 'letter')

# ---------------------------------------------------------------- 4.2 bias, fact and opinion
FACTS = ['The park will cost $250,000.', 'The survey received 300 replies.', 'The school has 820 students.', 'The new bridge is 1.2 kilometres long.',
         'The library opens at 9 a.m. on weekdays.', 'Water boils at 100 °C at sea level.', 'The match ended 2–1.', 'The museum was built in 1902.',
         'Last year the town recycled 40 tonnes of glass.', 'The film lasts two hours and ten minutes.', 'The bus route was changed in March.', 'Mount Kilimanjaro is in Tanzania.']
OPINIONS = ['The plan is, quite simply, madness.', 'Skateboarding is a pointless hobby.', 'The new bridge is an eyesore.', 'Homework is the worst part of school life.',
            'The museum is the most interesting building in the city.', 'Everyone will love the new menu.', 'The match was a disgrace to the sport.', 'The film is far too long and boring.',
            'Teenagers today are lazier than ever.', 'The council never listens to anyone.', 'Summer is the best season for a holiday.', 'The old bus route was much better.']
LOADED = [
    ('The council wants to fill the gardens with concrete ramps and teenagers shouting at all hours.', 'teenagers shouting at all hours', 'The council plans to build skateboard ramps in part of the gardens, which some residents fear could be noisy.'),
    ('Protesters swarmed the town hall, screeching their demands.', 'swarmed … screeching', 'Protesters gathered outside the town hall and called for changes.'),
    ('The greedy developers are bulldozing our precious woodland.', 'greedy … bulldozing … precious', 'The developers are clearing part of the woodland to build houses.'),
    ('Thousands of fans flooded the streets in a wild frenzy of celebration.', 'flooded … wild frenzy', 'Thousands of fans gathered in the streets to celebrate.'),
    ('The minister finally admitted that the scheme had collapsed.', 'finally admitted … collapsed', 'The minister said the scheme had not met its targets.'),
    ('A gang of youths loitered outside the shop.', 'gang … loitered', 'A group of young people waited outside the shop.'),
    ('The heroic headteacher bravely saved the school from closure.', 'heroic … bravely saved', 'The headteacher led a campaign that kept the school open.'),
    ('The so-called experts have once again got it wrong.', 'so-called … once again', 'Some experts’ predictions turned out to be inaccurate.'),
]
t42 = topic('Evaluating bias, fact and opinion in media texts', 'evaluating bias fact and opinion', 'media texts', 'bias')
t42.fixed('C1', (1, 2), [
    ('What is a fact?', 'A statement that can be checked and proved true or false', 'Facts can be verified; opinions express beliefs or judgements.', ['A statement of what someone believes', 'A statement that uses emotive language', 'A statement that everyone agrees with']),
    ('What does it mean if a text is biased?', 'It presents a one-sided view, favouring one side unfairly', 'Bias: selective facts, loaded words, ignoring the other side.', ['It contains only facts', 'It gives both sides equal space', 'It is written in the third person']),
    ('Which word in this sentence most clearly signals an opinion: ‘The disappointing new library opened on Monday’?', 'disappointing', 'An evaluative adjective expresses judgement; the rest is checkable.', ['library', 'opened', 'Monday']),
    ('Why might a writer place the word ‘only’ before a fact, as in ‘only 300 people replied’?', 'To make the number seem small and weaken the opposing case', 'A fact can be framed with loaded words to support a bias.',
     ['To make the number seem very large', 'To show the number is an estimate', 'Because ‘only’ is required before numbers']),
])


@t42.add('C1', (1, 2, 3))
def t42_fact(r, D):
    if r.random() < 0.5:
        a = r.choice(FACTS)
        opts, ans = mcq(r, a, r.sample(OPINIONS, 4))
        return {'stem': 'Which of these statements is a fact rather than an opinion?', 'options': opts, 'answer': ans, 'key': f'{Q(a)} can be checked and proved; the others are judgements.'}
    a = r.choice(OPINIONS)
    opts, ans = mcq(r, a, r.sample(FACTS, 4))
    return {'stem': 'Which of these statements is an opinion rather than a fact?', 'options': opts, 'answer': ans, 'key': f'{Q(a)} expresses a judgement that cannot be proved; the others are checkable.'}


@t42.add('C2', (1, 2, 3, 4), 'explain')
def t42_loaded(r, D):
    s, w, n = r.choice(LOADED)
    m = mk('C2', D)
    return {'stem': f'Read this sentence from a news article: {Q(s)} Explain how the writer’s choice of words shows bias.',
            'answer': f'The loaded words {Q(w)} create a negative or exaggerated impression rather than simply reporting what happened, so the reader is pushed towards the writer’s view.',
            'key': f'{upto(m)}: 1 for identifying loaded words ({w}); 1 for their connotations; a further mark for the intended effect on the reader.'}


rewrite_templates(t42, [('Rewrite this sentence in neutral, unbiased language.', s, f'Model: {Q(n)}', 'Award for removing loaded words and keeping the facts.') for s, w, n in LOADED],
                  ['{ins} {q}', 'A journalist wants to sound impartial. {ins} Explain one change you made. {q}'])


RESORT = Text('resort', 'biased', 'a travel feature, ‘Paradise Found at Azure Bay’', """
Forget every holiday you have ever had. Azure Bay is, without doubt, the most beautiful resort on the planet. Its
150 luxury rooms overlook a private beach of powder-white sand, and the hotel's three restaurants serve food that will
make you weep with joy. Families adore the kids' club; couples adore the sunset spa. Yes, the nearest town is a
two-hour drive away, but why would you ever want to leave? Rooms start at $400 a night, a small price for perfection.
Every guest I met said it was the best week of their lives. Book now, before the rest of the world discovers it.""")
RESORT.f('Azure Bay is, without doubt, the most beautiful resort on the planet.', 'hyperbole', 'the most beautiful resort on the planet',
         'the extreme superlative is an opinion presented as certain fact (‘without doubt’), leaving no room for comparison.')
RESORT.f("serve food that will make you weep with joy", 'hyperbole', 'weep with joy', 'the exaggeration sells an emotional experience rather than giving information about the food.', also=('emotive language', 'direct address'))
RESORT.f('Yes, the nearest town is a two-hour drive away, but why would you ever want to leave?', 'rhetorical question', 'why would you ever want to leave',
         'a real disadvantage is admitted and instantly brushed aside with a question, so the reader does not dwell on it.', also=('counter-argument', 'direct address'))
RESORT.f('Every guest I met said it was the best week of their lives.', 'anecdote', 'Every guest I met', 'unrepresentative personal evidence is presented as universal praise.', also=('hyperbole',))
RESORT.f('Book now, before the rest of the world discovers it.', 'imperative', 'Book now', 'the command creates urgency and fear of missing out.', also=('direct address',))
U4_BIAS = [SKATE, RESORT]
t42.fixed('C2', (2, 3), [(f'Explain why this statement is an opinion, and rewrite it as a fact: {Q(o)}', f'It is a judgement that cannot be proved ({o.split()[-1].strip(".")} is evaluative). A factual version would give checkable information, e.g. {Q(f)}',
                          '1 mark: identifies the judgement word(s); 1 mark: a checkable factual rewrite.') for o, f in zip(OPINIONS, FACTS)])
feature_templates(t42, RESORT.feats + SKATE.feats, PERSUADE, c1=False, c3=False)
BIAS_EVENTS = ['a new shopping centre opening on the edge of town', 'a school deciding to scrap its uniform', 'a music festival held in a city park', 'a factory closing and moving abroad',
               'a city introducing a charge for cars entering the centre', 'a football club building a new stadium near homes']


@t42.add('C4', (2, 3, 4, 5), 'long')
def t42_two(r, D):
    ev = r.choice(BIAS_EVENTS)
    m = mk('C4', D, 'long')
    return {'stem': f'Write two short news reports about {ev}: one biased in favour and one biased against. Then write a short paragraph explaining the techniques you used to create bias in each. Write about {WORDS.get(D, "250–350")} words in total.',
            'answer': f'Model approach: same core facts in both; report 1 uses positive loaded words, favourable quotations and selected facts; report 2 uses negative loaded words, critical quotations and omits benefits; commentary names the techniques (loaded language, selection, ordering, quotation choice, headline).',
            'key': levels_key(m, ('both reports share the facts but are clearly and skilfully biased in opposite directions; commentary precisely explains selection, loaded language, ordering and headlines',
                                  'two recognisably different reports with some loaded language; commentary identifies some techniques', 'reports barely differ or ignore facts; little explanation'),
                              'selection and omission of facts; connotations of word choice; which quotations are included; headline framing; order of information.'), 'type': 'long'}


@t42.add('C3', (2, 3, 4, 5), 'explain')
def t42_sort(r, D):
    m = mk('C3', D)
    T = r.choice(U4_BIAS)
    stem = r.choice([f'Read {T.label}: {Q(T.text)} Identify two facts and two opinions in the text, and explain how the writer uses facts to support their bias.',
                     f'Read {T.label}: {Q(T.text)} How fair is this text? Identify evidence of bias and explain what information is missing.'])
    ans = ('Facts: the park will cost $250,000; 300 people replied to the survey. Opinions: the plan is madness; the gardens are one of the last peaceful places; bored teenagers will cause trouble. The writer frames facts with loaded words (‘only 300’) and omits the views of young people and the benefits of the park.'
           if T is SKATE else 'Facts: 150 rooms; three restaurants; the nearest town is two hours away; rooms start at $400 a night. Opinions: the most beautiful resort on the planet; food that will make you weep with joy; a small price for perfection. The writer brushes aside the remote location and the high price, quotes only delighted guests and gives no independent reviews.')
    return {'stem': stem,
            'answer': ans,
            'key': f'{upto(m)}: 1 per correct fact/opinion; credit explanation of framing (‘only’), stereotyping, unrepresentative evidence, missing viewpoints.'}


@t42.add('C4', (2, 3, 4, 5), 'long')
def t42_reply(r, D):
    if r.random() < 0.4:
        stem, genre, ind = r.choice([
            ('Write an honest, balanced review of Azure Bay for a travel website, using the facts in the feature but giving readers a fair picture.', 'article',
             'Uses the facts (rooms, restaurants, price, remote location); weighs positives and negatives; neutral or measured tone; advice for different kinds of traveller.'),
            ('Write a letter to the travel magazine complaining that the feature on Azure Bay was an advertisement disguised as journalism.', 'letter',
             'Formal complaint; identifies hyperbole, unrepresentative quotations and the dismissed drawbacks; requests balanced reporting.')])
        m = mk('C4', D, 'long')
        return {'stem': f'Read {RESORT.label}: {Q(RESORT.text)} {stem} Write about {WORDS.get(D, "250–350")} words.', 'answer': f'Model approach: {ind}', 'key': levels_key(m, genre, ind), 'type': 'long'}
    stem, genre, ind = r.choice([
        ('Write a letter to the editor responding to the article. Argue that the skate park would benefit the town and point out the bias in the original column.', 'letter',
         'Formal letter; identifies bias (loaded words, stereotypes, ‘everyone I have spoken to’); argues benefits (safe space, exercise, community); rebuts the cost point.'),
        ('Rewrite the column as a balanced news report about the skate park plan, using only facts and quoting people on both sides.', 'report',
         'Neutral headline; lead with who/what/where/when; cost and survey facts; quotes from a resident and a young skater; no loaded words.'),
        ('Write an opinion column for the same newspaper arguing in favour of the skate park, using persuasive techniques but avoiding unfair bias.', 'article',
         'Clear view with evidence; persuasive devices; acknowledges residents’ concerns about noise; suggests solutions; fair tone.'),
    ])
    m = mk('C4', D, 'long')
    return {'stem': f'Read {SKATE.label}: {Q(SKATE.text)} {stem} Write about {WORDS.get(D, "250–350")} words.', 'answer': f'Model approach: {ind}', 'key': levels_key(m, genre, ind), 'type': 'long'}


# ---------------------------------------------------------------- 4.3 balanced argument
PHONES = Text('phones', 'argument', 'a balanced article, ‘Should Phones Be Banned in Schools?’', """
Few topics divide students and teachers as sharply as mobile phones. Supporters of a ban argue that phones distract
students in lessons and that social media can make bullying worse. Some schools that have introduced bans report calmer
corridors and better concentration. On the other hand, many parents want their children to carry a phone for safety on
the journey to and from school. Phones can also be useful learning tools, giving instant access to dictionaries,
calculators and research. A compromise may be the best solution: phones could be kept in lockers during lessons but
allowed at break or used under a teacher's guidance. Ultimately, the aim should be to teach students to use technology
responsibly rather than simply to remove it.""")
PHONES.r('Supporters of a ban argue that phones distract students in lessons and that social media can make bullying worse.', 'Give one argument used by supporters of a ban.',
         'Phones distract students in lessons', ['Phones help with research', 'Parents want phones for safety', 'Phones are cheap to buy'])
PHONES.r('many parents want their children to carry a phone for safety on the journey to and from school', 'Why do many parents want their children to carry a phone?',
         'For safety on the journey to and from school', ['To play games at break', 'To photograph their lessons', 'To call teachers at night'])
PHONES.i('On the other hand, many parents want their children to carry a phone', 'What is the function of ‘On the other hand’ in the article?',
         'It signals a turn from the arguments for a ban to the arguments against, showing the reader that the other side is now being considered.',
         '1 mark: contrast/signals the counter-view; 1 mark: links the two halves of the argument')
PHONES.i('A compromise may be the best solution', 'Why does the writer suggest a compromise near the end?',
         'After weighing both sides, the writer offers a solution that takes account of each, which shows balance and leads to a reasoned conclusion.',
         '1 mark: reaches a judgement after weighing both sides; 1 mark: shows fairness/balance')
PHONES.i('Ultimately, the aim should be to teach students to use technology responsibly rather than simply to remove it.', 'What is the writer’s final view?',
         'The writer believes education about responsible use is better than a total ban; ‘Ultimately’ signals this considered conclusion.',
         '1 mark: final view stated; 1 mark: reference to ‘Ultimately’ or ‘rather than simply to remove it’')
ARG_GAPS = [
    ('Some people believe uniforms create equality. ____, others argue they limit self-expression.', 'However', ['Furthermore', 'Therefore', 'For example'], 'introduces the opposing view'),
    ('____, it is clear that both sides make valid points, but the benefits outweigh the costs.', 'In conclusion', ['For instance', 'Firstly', 'Meanwhile'], 'signals the final judgement'),
    ('Exercise improves health. ____, it can boost concentration in lessons.', 'Furthermore', ['However', 'In contrast', 'Nevertheless'], 'adds a further point on the same side'),
    ('____ longer holidays sound appealing, they could cause students to forget what they have learned.', 'Although', ['Because', 'Therefore', 'Since'], 'concedes a point before countering it'),
    ('Critics say the scheme is too expensive. ____, the long-term savings would cover the cost.', 'Nevertheless', ['Similarly', 'Firstly', 'For example'], 'rebuts a counter-argument'),
    ('Many cities have introduced car-free days. Bogotá, ____, closes roads to cars every Sunday.', 'for example', ['however', 'in conclusion', 'nevertheless'], 'introduces evidence'),
    ('____, it is true that online learning offers flexibility.', 'Admittedly', ['Consequently', 'Finally', 'Similarly'], 'concedes a point to the other side'),
    ('Junk food is cheap and widely advertised. ____, many young people eat too much of it.', 'Consequently', ['Admittedly', 'On the other hand', 'For instance'], 'shows a result'),
]
CLAIMS = [
    ('School uniforms should be abolished because they stop students expressing themselves.', 'Opponents might argue that uniforms reduce peer pressure about expensive clothes. However, students can still express themselves through their ideas, work and activities, and uniforms save families money.'),
    ('Homework should be banned because students need time to relax.', 'Some argue that homework is essential for practice. While practice matters, short, focused tasks in school could achieve the same benefit without exhausting students.'),
    ('Zoos should be closed because animals belong in the wild.', 'Supporters of zoos point out that they protect endangered species through breeding programmes. Nevertheless, these programmes could be run in sanctuaries that give animals far more space.'),
    ('Everyone should become vegetarian to protect the planet.', 'Critics say that meat is an important source of protein and part of many cultures. Admittedly this is true, yet reducing meat rather than banning it would still cut emissions while respecting traditions.'),
    ('Video games are a waste of time.', 'Some claim games improve problem-solving and teamwork. This may be true for some games, but the hours spent could also be used for exercise or reading, so limits are sensible.'),
    ('Cars should be banned from city centres.', 'Opponents argue that businesses rely on customers arriving by car. However, cities that have pedestrianised their centres often see more shoppers, not fewer, because the streets become pleasant places to visit.'),
    ('Students should be allowed to choose all their own subjects at age twelve.', 'Some say this gives students freedom and motivation. On the other hand, twelve-year-olds may drop subjects they will need later, so a broad core with some choice may be wiser.'),
]
ARG_TOPICS = ['Should the school day start later?', 'Should students wear school uniform?', 'Should zoos exist?', 'Is social media good for teenagers?', 'Should homework be banned?',
              'Should cars be banned from city centres?', 'Should every student learn a musical instrument?', 'Should children be paid for doing household chores?',
              'Should exams be replaced by coursework?', 'Is it better to live in the city or the countryside?']
t43 = topic('Structuring a balanced argument', 'structuring a balanced argument', 'counter-argument')
t43.fixed('C1', (1, 2), ret_items([PHONES]) + [
    ('What is a counter-argument?', 'A point that opposes the writer’s own view', 'Raising and answering counter-arguments strengthens an argument.', ['A point that repeats the main argument', 'The title of an essay', 'A summary of the conclusion']),
    ('What should the conclusion of a balanced argument do?', 'Weigh up both sides and give a reasoned judgement', 'A balanced piece reaches a considered view after examining both sides.',
     ['Introduce three new arguments', 'Repeat the introduction word for word', 'Only list the points against']),
    ('What is a rebuttal?', 'A response that shows why a counter-argument is weak or wrong', 'Rebuttal: ‘However, this ignores…’.', ['An agreement with the other side', 'A rhetorical question', 'A list of statistics']),
])


@t43.add('C1', (1, 2, 3))
def t43_gap(r, D):
    s, a, ds, fn = r.choice(ARG_GAPS)
    opts, ans = mcq(r, a, ds)
    return {'stem': f'Choose the best discourse marker to complete this sentence from an argument: {Q(s)}', 'options': opts, 'answer': ans, 'key': f'‘{a}’ {fn}.'}


t43.fixed('C2', (2, 3), inf_items([PHONES]) + [
    ('Explain why a balanced argument should include a counter-argument even when the writer has a clear view.', 'It shows the writer has considered other perspectives, makes the argument fairer and more convincing, and allows the writer to rebut objections.', '1 mark: fairness/credibility; 1 mark: chance to rebut.'),
    ('Explain why each paragraph of an argument should begin with a clear topic sentence.', 'The topic sentence tells the reader the point of the paragraph, helping them follow the line of argument.', '1 mark: signals the point; 1 mark: clarity of structure.'),
    ('Explain the difference between ‘Furthermore’ and ‘However’ in an argument.', '‘Furthermore’ adds a point on the same side; ‘However’ introduces a contrasting point or counter-argument.', '1 mark: function of ‘Furthermore’ (adds); 1 mark: function of ‘However’ (contrasts).'),
])


BAL_MARKERS = [
    ('On the other hand,', 'signals a move to the opposing view, so the reader knows the article is now presenting the other side'),
    ('Admittedly,', 'concedes a point to the other side before the writer answers it, which makes the writer seem fair'),
    ('Nevertheless,', 'shows that, despite the point just made, the writer still holds their view'),
    ('Critics of this idea point out that', 'introduces a counter-argument and attributes it to others, keeping the tone balanced'),
    ('Weighing up both sides,', 'signals the start of the conclusion, where the writer judges which arguments are stronger'),
    ('A further argument in favour is that', 'adds another point to the same side, building that side of the case'),
]


@t43.add('C2', (1, 2, 3), 'explain')
def t43_marker(r, D):
    mkr, fn = r.choice(BAL_MARKERS)
    m = mk('C2', D)
    return {'stem': f'In a balanced argument, a paragraph begins {Q(mkr)} Explain how this phrase guides the reader through the argument.', 'answer': cap(fn) + '.',
            'key': f'{upto(m)}: identifies the function of the phrase ({fn}); explains how it helps the reader follow the structure of the argument.'}


@t43.add('C3', (2, 3, 4, 5), 'explain')
def t43_counter(r, D):
    c, model = r.choice(CLAIMS)
    m = mk('C3', D)
    return {'stem': f'A student writes: {Q(c)} Write two or three sentences that present a counter-argument to this claim and then rebut it.',
            'answer': f'Model: {model}', 'key': f'{upto(m)}: 1 for a fair counter-argument; 1 for a rebuttal with a reason; remaining mark(s) for appropriate discourse markers (however, admittedly, nevertheless) and clear expression.'}


@t43.add('C3', (2, 3, 4), 'short')
def t43_plan(r, D):
    q = r.choice(ARG_TOPICS)
    m = mk('C3', D)
    return {'stem': f'Write a five-paragraph plan for a balanced argument answering the question {Q(q)} Give a one-line summary of each paragraph.',
            'answer': 'Model plan: 1 Introduction – the issue and why it matters; 2 Arguments for, with evidence; 3 Arguments against, with evidence; 4 Weighing the strongest points / possible compromise; 5 Conclusion – reasoned judgement.',
            'key': f'{upto(m)}: introduction; points for; points against; evaluation; conclusion with judgement; logical order.'}


writing_templates(t43, [(f'Write a balanced argument answering the question {Q(q)} Present both sides fairly, use evidence and reach a reasoned conclusion.',
                         'introduction setting out the issue; paragraphs for and against with evidence; counter-arguments and rebuttals; discourse markers; reasoned conclusion.',
                         f'Model plan for {Q(q)}: introduction; strongest arguments for; strongest arguments against; weighing/compromise; conclusion giving a clear, justified view.') for q in ARG_TOPICS], 'discursive')
compose_templates(t43, [PHONES], C=('C4',))

# ---------------------------------------------------------------- 4.4 formal speech and debate
SPEECH = Text('speech', 'speech', 'a student’s speech to the school council, ‘Give Us a Quiet Room’', """
Good morning, members of the council, teachers and fellow students. I am here to ask for one simple thing: a quiet
room. Think about the last time you tried to revise at break. Where did you go? The library is full, the corridors are
noisy, and the canteen sounds like a football stadium. My first point is about wellbeing. A recent survey of our Year 9
found that seven out of ten students feel stressed during exam season. My second point is about fairness. Not every
student has a calm place to study at home. Some of you may say there is no spare room. But the old music store has been
empty since September. Friends, we are not asking for luxury. We are asking for a space to think. Thank you.""")
SPEECH.f('Good morning, members of the council, teachers and fellow students.', 'direct address', 'members of the council, teachers and fellow students',
         'greeting each group shows respect and awareness of a mixed, formal audience, and establishes a polite, confident tone.')
SPEECH.f('Where did you go?', 'rhetorical question', 'Where did you go?', 'the question makes listeners recall their own frustration, so they relate to the problem.', also=('direct address',))
SPEECH.f('the canteen sounds like a football stadium', 'hyperbole', 'like a football stadium', 'the exaggerated comparison makes the noise vivid and adds humour, keeping listeners engaged.', also=('metaphor',))
SPEECH.f('A recent survey of our Year 9 found that seven out of ten students feel stressed during exam season.', 'statistic', 'seven out of ten',
         'the figure provides evidence and makes the problem seem widespread rather than personal.', also=('expert opinion',))
SPEECH.f('Some of you may say there is no spare room. But the old music store has been empty since September.', 'counter-argument', 'Some of you may say',
         'anticipating the objection and answering it with a practical fact makes the speaker seem prepared and reasonable.')
SPEECH.f('we are not asking for luxury. We are asking for a space to think.', 'repetition', 'We are asking',
         'the repeated structure creates a memorable contrast and a strong, rhythmic ending.', also=('inclusive pronoun', 'contrast'))
SPEECH.r('I am here to ask for one simple thing: a quiet room.', 'What is the speaker asking for?', 'A quiet room', ['A bigger canteen', 'More library books', 'A new music store', 'Shorter exams'])
SPEECH.r('But the old music store has been empty since September.', 'Which space does the speaker suggest could be used?', 'The old music store', ['The library', 'The canteen', 'The corridors', 'A classroom'])
SPEECH.x('How does the speaker try to persuade the school council?', 'Polite formal greeting; clear purpose; rhetorical questions; humour/hyperbole; signposting (My first point… My second point…); statistic; counter-argument answered; inclusive ‘we’; repetition in the ending.')
MOTIONS = ['This house believes that homework does more harm than good.', 'This house would ban single-use plastics in schools.', 'This house believes that every student should learn to cook.',
           'This house would make sport compulsory every day.', 'This house believes that city life is better than country life.', 'This house would lower the voting age to sixteen.',
           'This house believes that space exploration is worth the cost.', 'This house would replace exams with coursework.', 'This house believes that zoos should be closed.',
           'This house would give every student a tablet instead of textbooks.']
SPOKEN = [
    ('In this essay I will discuss three reasons why recycling is important.', 'Good afternoon, everyone. Today I want to give you three reasons why recycling matters to every single one of us.'),
    ('It can be concluded that the evidence supports a later start time.', 'So what does all this tell us? Quite simply: a later start would help us learn.'),
    ('Some people disagree with this view.', 'Now, some of you may be thinking, ‘That will never work.’ Let me show you why it can.'),
    ('There are many advantages to learning a language.', 'Imagine stepping off a plane and understanding every word around you. That is what learning a language gives you.'),
    ('Finally, the costs are not as high as people think.', 'And my final point – perhaps the most important – is cost. It is far lower than you might fear.'),
    ('Sport is beneficial for health and concentration.', 'Who here feels sharper after a game at break? Exactly. Sport wakes up our bodies and our brains.'),
]
t44 = topic('Formal speech and debate', 'formal speech and debate', 'presenting a point of view')
t44.fixed('C1', (1, 2), [
    ('In a formal debate, what is the side that supports the motion called?', 'proposition', 'Proposition supports the motion; opposition argues against it.', ['opposition', 'chair', 'audience']),
    ('What is signposting in a speech?', 'Phrases that tell listeners where the speech is going, such as ‘My first point is…’', 'Listeners cannot re-read, so signposts help them follow.', ['Pointing at the audience', 'Using slides', 'Ending with a question']),
    ('Why is repetition often more common in speeches than in written essays?', 'Listeners need key ideas reinforced because they cannot re-read', 'Repetition aids memory and rhythm in spoken texts.',
     ['Speeches must be longer than essays', 'Repetition is grammatically required in speech', 'Audiences prefer to hear the same word every sentence']),
    ('What is the role of the chair in a debate?', 'To manage the debate, introduce speakers and keep time', 'The chair is neutral and keeps order.', ['To argue for the motion', 'To vote first', 'To write the motion']),
    ('Which is the best way to open a formal speech?', 'Greet the audience and state your purpose clearly', 'An appropriate greeting and clear purpose orient listeners.', ['Start with a joke unrelated to the topic', 'Read your notes silently', 'Begin with your conclusion only']),
])
feature_templates(t44, SPEECH.feats, PERSUADE + ['repetition'], c1=True)
rewrite_templates(t44, [('Rewrite this written sentence so that it would work well in a speech to students.', a, f'Model: {Q(b)}', 'Award for features of spoken persuasion: direct address, rhetorical question, signposting, rhythm; appropriate register.') for a, b in SPOKEN],
                  ['{ins} {q}', '{q} {ins} Explain what makes your version suit a listening audience.'])
writing_templates(t44, [(f'Write a speech for the {side} in a school debate on the motion {Q(mo)}', 'formal greeting; clear stance; signposted points with evidence; rhetorical devices; rebuttal of the other side; memorable conclusion.',
                         f'Model structure: greeting and stance ({side}); point 1 with evidence; point 2 with an anecdote; rebuttal of the strongest opposing point; call to the audience to vote.')
                        for mo in MOTIONS for side in ('proposition', 'opposition')], 'speech')
compose_templates(t44, [SPEECH], C=('C3', 'C4'))
CHAPTERS[4] = [t41, t42, t43, t44]


# =========================================================== Unit 5 Drama: playscripts and performance

CLOCK = Text('clock', 'script', 'an extract from a play, ‘The Clock’', """
A cluttered attic. Evening. Rain against the window. JAMIE (14) kneels beside an open trunk. Enter TARA (16), holding a
torch. TARA: What are you doing up here? JAMIE: (without turning) Nothing. TARA: That's Grandad's trunk. Mum said—
JAMIE: I know what Mum said. (He lifts out a small brass clock. Its glass is cracked.) TARA: (quietly) You broke it.
JAMIE: It was already like this! I just... wanted to see it. (Pause. TARA sits on the floor beside him. She takes the
clock gently.) TARA: He used to wind it every Sunday. Said it was the only thing in the house that never lied.
(Thunder. The torch flickers and goes out. Darkness.) JAMIE: Tara?""")
CLOCK.r('A cluttered attic. Evening. Rain against the window.', 'Where is the scene set?', 'In a cluttered attic in the evening', ['In a kitchen at breakfast', 'In a school hall', 'In a garden in the rain', 'In Grandad’s shop'])
CLOCK.r('He lifts out a small brass clock. Its glass is cracked.', 'What does Jamie take out of the trunk?', 'A small brass clock with cracked glass', ['A torch', 'A letter from Grandad', 'A photograph', 'A key'])
CLOCK.r('He used to wind it every Sunday.', 'How often did Grandad wind the clock?', 'Every Sunday', ['Every morning', 'Once a year', 'Never', 'Every evening'])
CLOCK.i("TARA: That's Grandad's trunk. Mum said— JAMIE: I know what Mum said.", 'What does the interruption suggest about Jamie’s feelings?',
        'Jamie is defensive and irritated; he does not want to be reminded of the rule, which suggests guilt or strong emotion connected to Grandad.',
        '1 mark: defensive/irritated/guilty; 1 mark: reference to the dash showing the interruption')
CLOCK.i("JAMIE: It was already like this! I just... wanted to see it.", 'What does the ellipsis suggest about Jamie at this point?',
        'The pause shows hesitation and vulnerability: he is struggling to admit that he misses his grandfather.',
        '1 mark: hesitation/emotion; 1 mark: links to missing Grandad')
CLOCK.i('Said it was the only thing in the house that never lied.', 'What might the clock symbolise for the characters?',
        'It represents Grandad and his values of honesty and routine; the cracked glass may suggest the family is broken by his loss.',
        '1 mark: link to Grandad/memory; 1 mark: developed symbolic reading (honesty, broken family, time passing)')
CLOCK.i('(Thunder. The torch flickers and goes out. Darkness.) JAMIE: Tara?', 'Why is this an effective way to end the extract?',
        'The sudden darkness and Jamie’s frightened one-word question create a cliffhanger, leaving the audience in suspense.',
        '1 mark: suspense/cliffhanger; 1 mark: reference to darkness or the short question')
CLOCK.x('How does the playwright create tension and emotion in this extract?', 'Pathetic fallacy (rain, thunder); interruptions and dashes; stage directions (without turning, quietly, gently); the symbolic broken clock; pause; blackout cliffhanger.')

INTERVIEW = Text('interview', 'script', 'an extract from a play, ‘The Interview’', """
A small office. A desk, two chairs. MS RAO, the manager, is typing. NADIA (17) stands in the doorway, clutching a
folder. MS RAO: (not looking up) Sit. (NADIA sits on the edge of the chair. She drops the folder; papers scatter. She
scrambles to collect them.) NADIA: Sorry. Sorry, I— MS RAO: Why do you want to work here? NADIA: (taking a deep
breath) Because my mother worked here. For twenty years. Until you let her go. (MS RAO stops typing. A long silence.)
MS RAO: (slowly) Does she know you've come? NADIA: No. (MS RAO closes the laptop.)""")
INTERVIEW.r('MS RAO, the manager, is typing.', 'What is Ms Rao doing at the start of the scene?', 'Typing', ['Reading a folder', 'Talking on the phone', 'Standing in the doorway', 'Collecting papers'])
INTERVIEW.r('Because my mother worked here. For twenty years.', 'How long did Nadia’s mother work there?', 'Twenty years', ['Two years', 'Seventeen years', 'Since September', 'One summer'])
INTERVIEW.i('MS RAO: (not looking up) Sit.', 'What does this stage direction and line suggest about Ms Rao at first?',
            'She is powerful, busy and dismissive: she does not look at Nadia and gives a one-word command.',
            '1 mark: dismissive/powerful; 1 mark: reference to ‘not looking up’ or the one-word command')
INTERVIEW.i('She drops the folder; papers scatter. She scrambles to collect them.', 'What does this action show about Nadia’s state of mind?',
            'She is extremely nervous; the clumsy action shows she is under pressure and not in control.',
            '1 mark: nervous; 1 mark: links the action to her feelings')
INTERVIEW.i('(MS RAO stops typing. A long silence.)', 'Why is the silence dramatically effective?',
            'It marks a shift in power: Nadia’s revelation shocks Ms Rao, and the silence lets the tension build for the audience.',
            '1 mark: tension/shock; 1 mark: shift in power or audience anticipation')
INTERVIEW.i('(MS RAO closes the laptop.)', 'What does closing the laptop suggest?',
            'She is now giving Nadia her full attention; the interview has become personal and serious.',
            '1 mark: full attention/change in attitude; 1 mark: interview now personal')
INTERVIEW.x('How does the playwright show the change in the relationship between Ms Rao and Nadia?', 'Ms Rao dominant at first (not looking up, ‘Sit’); Nadia nervous (dropped folder, repeated ‘Sorry’); revelation in short sentences; silence; Ms Rao’s slow question and closing laptop show power shifting.')

STAGEFRIGHT = Text('stagefright', 'script', 'an extract from a comedy, ‘Stage Fright’', """
A school stage, the night of the play. Behind the curtain. OMAR, dressed as a tree, paces. OMAR: (to the audience)
Twelve lines. I have twelve lines and I can remember precisely none of them. (Enter MRS CHEN, the director, with a
clipboard.) MRS CHEN: Omar! Places, please. Two minutes. OMAR: Mrs Chen, I think I've got a fever. MRS CHEN: (feeling
his forehead) You've got stage fright. Everybody has it. Even trees. (She exits. OMAR takes a deep breath and turns to
face the curtain. It begins to rise.) OMAR: (whispering) Here goes.""")
STAGEFRIGHT.r('OMAR, dressed as a tree, paces.', 'What is Omar dressed as?', 'A tree', ['A director', 'A doctor', 'A curtain', 'A teacher'])
STAGEFRIGHT.r('Twelve lines. I have twelve lines', 'How many lines does Omar have?', 'Twelve', ['Two', 'None', 'Twenty', 'One'])
STAGEFRIGHT.i('OMAR: (to the audience) Twelve lines. I have twelve lines and I can remember precisely none of them.', 'What is the effect of Omar speaking directly to the audience?',
              'This aside lets the audience share his secret panic, creating comedy and sympathy.', '1 mark: identifies aside/direct address; 1 mark: effect (comedy, sympathy, closeness)')
STAGEFRIGHT.i("You've got stage fright. Everybody has it. Even trees.", 'How does Mrs Chen’s reply create humour?',
              'Her short, matter-of-fact sentences and the joke ‘Even trees’ mock Omar’s costume gently while reassuring him.', '1 mark: humour of ‘Even trees’; 1 mark: brisk, reassuring tone')
STAGEFRIGHT.x('How does the playwright create comedy in this extract?', 'Visual comedy of the tree costume; aside to the audience; exaggeration (precisely none); brisk dialogue; joke ‘Even trees’; curtain rising for a comic cliffhanger.')
SCRIPTS = [CLOCK, INTERVIEW, STAGEFRIGHT]

# ---------------------------------------------------------------- 5.1 conventions
SCRIPT_TERMS = ['stage direction', 'aside', 'monologue', 'soliloquy', 'prop', 'cue', 'blackout', 'scene', 'exit']
t51 = topic('Conventions of playscripts', 'conventions of playscripts', 'stage directions dialogue scene structure')
t51.fixed('C1', (1, 2), ret_items(SCRIPTS) + [
    ('What is a stage direction?', 'An instruction in a script, usually in brackets or italics, telling actors what to do or how to speak', 'E.g. (quietly), (She exits).', ['A line spoken by the narrator', 'The title of the play', 'A list of the actors']),
    ('In a playscript, how is the speaker of each line usually shown?', 'The character’s name at the start of the line, often in capitals', 'Scripts use NAME: line, with no speech marks.', ['Inside speech marks', 'In a footnote', 'In the title']),
    ('What is an aside?', 'A short remark spoken to the audience that other characters do not hear', 'E.g. OMAR: (to the audience) Twelve lines…', ['A long speech by one character alone on stage', 'A change of scenery', 'A stage direction about lighting']),
    ('What is a soliloquy?', 'A speech in which a character alone on stage speaks their thoughts aloud', 'Soliloquies reveal inner feelings to the audience.', ['A conversation between two characters', 'A song at the end of a play', 'The first scene of a play']),
    ('What is a prop?', 'An object used by actors on stage', 'E.g. the clock, the torch, the folder.', ['A character’s motivation', 'A type of stage direction', 'The scenery painted at the back']),
    ('Which of these is NOT used in a playscript?', 'Speech marks around dialogue', 'Scripts set out speech after the character’s name without speech marks.', ['Character names before lines', 'Stage directions in brackets', 'A description of the setting at the start']),
    ('What is a blackout?', 'All the stage lights going off suddenly', 'Often used to end a scene dramatically.', ['A character forgetting their lines', 'The audience leaving', 'A dark costume']),
])
PROSE = [
    ('‘Where have you been?’ asked Mum, folding her arms. Leo shrugged and dropped his bag. ‘Out,’ he muttered.',
     'MUM: (folding her arms) Where have you been? (LEO shrugs and drops his bag.) LEO: (muttering) Out.'),
    ('Grandpa slowly lowered his newspaper and peered over his glasses. ‘You did what?’ he said. Mei could not look at him.',
     'GRANDPA: (slowly lowering his newspaper and peering over his glasses) You did what? (MEI looks away.)'),
    ('The door burst open and Sipho ran in, soaking wet. ‘It’s gone!’ he shouted. ‘The bridge – it’s gone!’',
     '(The door bursts open. SIPHO runs in, soaking wet.) SIPHO: (shouting) It’s gone! The bridge – it’s gone!'),
    ('Ines tapped her pen on the desk. ‘Tell me the truth,’ she said quietly, ‘or don’t tell me anything.’',
     'INES: (tapping her pen on the desk; quietly) Tell me the truth, or don’t tell me anything.'),
    ('The shop bell rang. Mr Haddad looked up and smiled. ‘Back again?’ he asked. Freya grinned and held up an empty jar.',
     '(The shop bell rings. MR HADDAD looks up and smiles.) MR HADDAD: Back again? (FREYA grins and holds up an empty jar.)'),
    ('Kenji paced up and down the platform, checking his watch. ‘She’s never late,’ he said to no one in particular.',
     '(KENJI paces the platform, checking his watch.) KENJI: (to himself) She’s never late.'),
]
PROSE = [(re.sub(r'(^|\s)‘', r'\1“', re.sub(r'([,.!?–])’', r'\1”', a)), b) for a, b in PROSE]
t51.fixed('C2', (2, 3), [i for i in inf_items(SCRIPTS) if 'stage direction' in i[0] or 'interruption' in i[0] or 'ellipsis' in i[0] or 'silence' in i[0] or 'laptop' in i[0] or 'aside' in i[0] or 'directly' in i[0]] +
          [('Explain why playwrights include stage directions such as (quietly) or (without turning).', 'They tell actors how to deliver lines and move, revealing feelings that the words alone may not show.', '1 mark: guide performance; 1 mark: reveal emotion/subtext.'),
           ('Explain why playscripts do not use speech marks.', 'Almost everything in a script is speech, and each speaker is shown by their name, so speech marks are unnecessary.', '1 mark: names show the speaker; 1 mark: script is mainly dialogue.')])
rewrite_templates(t51, [('Rewrite this prose extract as a playscript, using character names and stage directions.', a, f'Model: {b}', 'Award for: names in capitals; no speech marks; stage directions in brackets in the present tense; meaning kept.') for a, b in PROSE],
                  ['{ins} {q}', 'Turn this story extract into a short playscript: {q} Set it out correctly.'])


@t51.add('C3', (3, 4, 5), 'explain')
def t51_conv(r, D):
    T = r.choice(SCRIPTS)
    m = mk('C3', D)
    return {'stem': f'Read {T.label}: {Q(T.text)} Identify three conventions of a playscript used in this extract and explain how each helps a director or actor.',
            'answer': 'E.g. setting description at the start (helps design the stage); character names before lines (shows who speaks); stage directions in brackets (how to move or speak, e.g. pauses, props, lighting); entrances and exits; sound or lighting cues.',
            'key': f'{upto(m)}: 1 per convention correctly identified with an example; further marks for explaining its use in performance.'}


compose_templates(t51, SCRIPTS, C=('C4',))

# ---------------------------------------------------------------- 5.2 motivation and tension
t52 = topic('Character motivation and dramatic tension', 'character motivation', 'dramatic tension in a scene')
t52.fixed('C1', (1, 2), [
    ('What is dramatic tension?', 'A feeling of suspense or conflict that makes the audience eager to know what happens', 'Created by conflict, secrets, silences, interruptions and timing.', ['The length of a play', 'The number of characters on stage', 'The cost of the tickets']),
    ('What is subtext?', 'The unspoken thoughts and feelings beneath what characters actually say', 'E.g. Jamie says ‘Nothing’ but means much more.', ['The list of characters', 'The writing under the title', 'A second act']),
    ('What is dramatic irony?', 'When the audience knows something that a character does not', 'It creates tension as the audience waits for the character to discover the truth.', ['When a character tells a joke', 'When the play ends happily', 'When two characters argue']),
    ('Which technique most often increases tension in a scene?', 'A long pause or silence after a revelation', 'Silences make the audience wait and anticipate.', ['A detailed list of props', 'A cheerful song', 'A change of costume']),
    ('In ‘The Interview’, what is Nadia’s main motivation for coming?', 'To confront the manager about her mother losing her job', 'Her line ‘Until you let her go’ reveals her motive.', ['To get a job as a manager', 'To return a lost folder', 'To meet her mother there']),
])
t52.fixed('C2', (2, 3, 4), inf_items(SCRIPTS))
feature_templates(t52, [Feat(T, q, d, f, e) for T, q, d, f, e in [
    (CLOCK, "TARA: That's Grandad's trunk. Mum said— JAMIE: I know what Mum said.", 'dialogue', 'Mum said—', 'the interruption shows conflict between the siblings and Jamie’s defensiveness, raising tension.'),
    (CLOCK, "JAMIE: It was already like this! I just... wanted to see it.", 'ellipsis', 'I just... wanted', 'the hesitation reveals Jamie’s vulnerable feelings about his grandfather.'),
    (INTERVIEW, 'NADIA: Sorry. Sorry, I—', 'repetition', 'Sorry. Sorry', 'the repeated apology shows panic and lack of power at the start of the scene.'),
    (INTERVIEW, 'NADIA: (taking a deep breath) Because my mother worked here. For twenty years. Until you let her go.', 'short sentence', 'Until you let her go.', 'the short, blunt fragments build to an accusation that shifts power to Nadia.'),
    (CLOCK, '(Thunder. The torch flickers and goes out. Darkness.)', 'pathetic fallacy', 'Thunder', 'the storm and darkness reflect the characters’ grief and fear and create suspense.'),
    (STAGEFRIGHT, "MRS CHEN: (feeling his forehead) You've got stage fright. Everybody has it. Even trees.", 'short sentence', 'Even trees.', 'the comic short sentence releases tension with a joke.'),
]], ['dialogue', 'ellipsis', 'repetition', 'short sentence', 'pathetic fallacy', 'irony', 'contrast'], c1=True)


@t52.add('C3', (2, 3, 4, 5), 'explain')
def t52_direct(r, D):
    T = r.choice(SCRIPTS)
    quote, question, answer, key = r.choice(T.infs)
    m = mk('C3', D)
    return {'stem': f'You are directing {T.label}. Read this moment: {Q(quote)} Explain how you would want the actors to perform it to show the characters’ motivation and build tension. Refer to voice, movement and timing.',
            'answer': f'Interpretation: {answer} Performance ideas: tone of voice and volume, pauses before or after the line, eye contact or avoiding it, gestures with props, positioning on stage.',
            'key': f'{upto(m)}: 1 for a valid reading of motivation/tension; further marks for specific, justified performance choices (voice, movement, timing) linked to the text.'}


extended_templates(t52, SCRIPTS)
CONT = [(CLOCK, 'Continue the scene from the moment the torch goes out, revealing what Jamie really feels about Grandad and building to a new moment of tension.',
         'darkness used for confession; Tara’s response; a sound or discovery that raises tension; stage directions for lighting and movement.'),
        (INTERVIEW, 'Continue the scene after Ms Rao closes the laptop, showing how the balance of power between the two characters changes.',
         'Ms Rao’s explanation or guilt; Nadia’s anger or doubt; pauses and interruptions; a final twist (a job offer, a secret about the mother).'),
        (STAGEFRIGHT, 'Write the next scene, set on stage during the play, in which Omar forgets his lines and has to improvise.',
         'comic tension; asides to the audience; reactions of other actors and Mrs Chen; a funny or triumphant resolution.')]


@t52.add('C4', (2, 3, 4, 5), 'long')
def t52_cont(r, D):
    T, task, ind = r.choice(CONT)
    m = mk('C4', D, 'long')
    return {'stem': f'Read {T.label}: {Q(T.text)} {task} Use playscript conventions. Write about {WORDS.get(D, "250–350")} words.',
            'answer': f'Model approach: {ind}', 'key': levels_key(m, 'script', ind + ' Characters’ motivations remain consistent with the extract.'), 'type': 'long'}


@t52.add('C4', (2, 3, 4, 5), 'long')
def t52_tension(r, D):
    sc, th = r.choice(SCENES)
    dev = r.choice(['a long silence', 'an interruption', 'a secret the audience knows but one character does not (dramatic irony)', 'a sound effect or blackout'])
    m = mk('C4', D, 'long')
    return {'stem': f'Write a scene about {sc} in which the characters want different things. Use {dev} to build dramatic tension at the key moment. Write about {WORDS.get(D, "250–350")} words.',
            'answer': f'Model approach: establish each character’s motivation early; escalate the conflict ({th}); place {dev} at the turning point; end with a resolution or a cliffhanger.',
            'key': levels_key(m, 'script', f'clear, contrasting motivations; {dev} used at the turning point; rising tension; correct layout.'), 'type': 'long'}

# ---------------------------------------------------------------- 5.3 writing and performing a scene
SCENES = [
    ('two friends who discover they have both applied for the same scholarship', 'conflict between loyalty and ambition'),
    ('a family waiting at an airport for a relative they have not seen for ten years', 'anticipation, nerves and a reunion'),
    ('a student who must tell their parent that they have failed an important test', 'fear, honesty and a parent’s reaction'),
    ('two strangers stuck in a lift during a power cut', 'tension, humour and gradual trust'),
    ('a shopkeeper who catches a child stealing bread', 'moral dilemma and compassion'),
    ('siblings clearing out their late grandmother’s house who find a hidden letter', 'grief, secrets and memory'),
    ('a team captain who must tell a friend they have been dropped from the team', 'loyalty and difficult news'),
    ('a new neighbour who knocks on the door late at night asking for help', 'mystery and trust'),
]
t53 = topic('Writing and performing a short scene', 'writing and performing a short scene', 'performing')
t53.fixed('C1', (1, 2), [
    ('When performing a script, what does ‘projection’ mean?', 'Speaking loudly and clearly enough for the whole audience to hear', 'Projection is about voice carrying, not shouting.', ['Showing slides on a screen', 'Planning the plot', 'Learning lines silently']),
    ('Why do actors rehearse ‘blocking’?', 'To plan where and how they move on stage', 'Blocking = positions and movements.', ['To stop the audience entering', 'To write the stage directions', 'To choose costumes']),
    ('In a short scene, what usually drives the action?', 'A conflict or problem between characters', 'Scenes need a clear conflict or want to create drama.', ['A long description of the setting', 'A list of props', 'The title']),
])
t53.fixed('C2', (2, 3), [
    ('Explain how an actor could use a pause to create tension.', 'A pause before or after an important line makes the audience wait and wonder, increasing suspense and drawing attention to what is said next.', '1 mark: audience anticipation; 1 mark: emphasis on a key line.'),
    ('Explain why a scene should usually start close to the moment of conflict.', 'Starting near the conflict hooks the audience quickly and avoids slow explanation; short scenes have little time.', '1 mark: hooks/engages; 1 mark: economy of time.'),
    ('Explain how facial expression and gesture can show subtext.', 'They reveal feelings that contradict or add to the words, e.g. a smile while clenching fists shows hidden anger.', '1 mark: shows unspoken feelings; 1 mark: example.'),
    ('Explain why stage directions in a script should be brief and in the present tense.', 'They are instructions for performance happening now; brief directions are easy for actors to follow and leave room for interpretation.', '1 mark: present tense = live action; 1 mark: clarity/room for actors.'),
])
PERFORM_1 = [
    ('(He stares at the floor and does not answer.)', 'his silence and lowered gaze suggest guilt or shame, so the audience senses he is hiding something'),
    ('(She laughs, a little too loudly.)', 'the forced laugh hints that she is nervous or pretending to be relaxed'),
    ('(A long pause. The clock ticks.)', 'the silence and the ticking stretch the moment, building tension before the next line'),
    ('(He slowly folds the letter and puts it in his pocket.)', 'the slow, careful action suggests the letter matters and that he is keeping its contents secret'),
    ('(She turns her back on him as she speaks.)', 'turning away shows rejection or hurt without the character having to say so'),
    ('(He grips the back of the chair until his knuckles whiten.)', 'the tight grip shows he is struggling to control anger or fear'),
    ('(She keeps glancing at the door.)', 'the repeated glances suggest she is anxious, expecting someone or wanting to escape'),
    ('(He smiles, but his eyes stay cold.)', 'the contrast between the smile and the cold eyes reveals that his friendliness is false'),
    ('(She hesitates, then pushes the money back across the table.)', 'the hesitation shows she is tempted, but returning the money shows her honesty wins'),
    ('(The lights dim until only his face is lit.)', 'isolating his face in light focuses attention on him and suggests he is alone with his thoughts'),
]
PERFORM_FRAMES = ['A script contains this stage direction: {sd} Explain what it suggests to the audience about the character.',
                  'In a short scene, an actor follows the stage direction {sd} What does this action show the audience?']


@t53.add('C2', (1, 2), 'explain')
def t53_dir1(r, D):
    sd, eff = r.choice(PERFORM_1)
    m = mk('C2', D)
    return {'stem': r.choice(PERFORM_FRAMES).format(sd=sd), 'answer': cap(eff) + '.',
            'key': f'{upto(m)}: a valid inference about the character’s feelings or situation linked to the action, e.g. {eff}.'}


rewrite_templates(t53, [('Write the next six lines of this scene as a playscript, adding at least two stage directions.', f'Opening line: {a}', f'Model continuation: the second character responds; a stage direction shows a reaction (e.g. (She turns away.)); the conflict escalates; a pause; a final line that leaves the scene open. Theme: {b}.',
                          'Award for: correct layout; dialogue develops conflict; purposeful stage directions; consistent characters.')
                         for a, b in [("AISHA: I saw your name on the list. Were you going to tell me?", 'loyalty and ambition'), ("FATHER: (holding up the letter) Explain this.", 'fear and honesty'),
                                      ("GRANDSON: (holding up an envelope) This was under the floorboards.", 'secrets and memory'), ("CAPTAIN: Sit down. There's something I need to tell you.", 'loyalty and difficult news'),
                                      ("NEIGHBOUR: (at the door, out of breath) Please. I didn't know who else to ask.", 'mystery and trust'), ("MOTHER: (staring at the clock) Ten years. Will we even recognise her?", 'anticipation and reunion'),
                                      ("STRANGER 1: (pressing the button again) It's not moving.", 'tension and trust'), ("SHOPKEEPER: Put it back. Or tell me why you need it.", 'compassion')]],
                  ['{ins} {q}'], C='C3', D=(2, 3, 4, 5))
writing_templates(t53, [(f'Write a short scene for the stage about {sc}. Include a description of the setting, stage directions and a moment of tension.',
                         f'Conflict: {th}; correct layout; stage directions for voice, movement and props; a clear turning point; an ending that resolves or leaves a question.',
                         f'Model structure: setting line; opening line close to the conflict; rising tension through interruptions or silence; a turning point revealing motivation ({th}); a final image or line.')
                        for sc, th in SCENES], 'script')


@t53.add('C4', (2, 3, 4, 5), 'long')
def t53_perf(r, D):
    T = r.choice(SCRIPTS)
    m = mk('C4', D, 'long')
    return {'stem': f'Read {T.label}: {Q(T.text)} Write director’s notes for a performance of this extract: explain how the setting, lighting, sound and the actors’ voices and movements should be used to bring out the characters and the tension. Write about {WORDS.get(D, "250–350")} words.',
            'answer': 'Model notes: staging and lighting matched to the mood; key moments identified (interruptions, pauses, revelations, blackout); specific vocal and physical choices for each character, each justified by the text.',
            'key': levels_key(m, ('detailed, practical and imaginative performance ideas, each precisely justified by reference to the script', 'some sensible performance ideas with some reference to the script', 'few or vague ideas, little reference to the text'),
                              'setting and atmosphere; lighting/sound cues; delivery of key lines; movement and proxemics; use of props; timing of pauses.'), 'type': 'long'}


CHAPTERS[5] = [t51, t52, t53]


# =========================================================== Unit 6 Autobiography, biography and recount

RIVER = Text('river', 'memoir', 'a memoir extract, ‘The River’', """
I learned to swim in the brown river behind my uncle's house the summer I was nine. There was no teacher, no float, no
shallow end; there was only my cousin Bilal, who was eleven and therefore an expert. 'Just kick,' he said, and let go of
my hands. I sank like a stone. Under the water everything turned green and silent, and I remember thinking, quite
calmly, that this was a strange place to end up. Then Bilal's hand closed around my collar and hauled me into the air. I
coughed half the river onto the bank. 'Again,' he said. Looking back now, I am amazed that either of us was allowed near
that water. But by the end of August I could swim to the far bank and back, and I have never since felt quite so proud.""")
RIVER.r('the summer I was nine', 'How old was the writer when they learned to swim?', 'Nine', ['Eleven', 'Seven', 'Thirteen', 'Fifteen'])
RIVER.r('there was only my cousin Bilal, who was eleven', 'Who taught the writer to swim?', 'Their cousin Bilal', ['Their uncle', 'A swimming teacher', 'Their mother', 'A lifeguard'])
RIVER.r('by the end of August I could swim to the far bank and back', 'What could the writer do by the end of August?', 'Swim to the far bank and back', ['Dive from the bridge', 'Teach Bilal to swim', 'Swim only with a float', 'Nothing – they gave up'])
RIVER.i('who was eleven and therefore an expert', 'How does the writer create humour here?', 'The adult writer gently mocks the child’s belief that being two years older made Bilal an expert; ‘therefore’ makes the logic sound comically serious.',
        '1 mark: irony/gentle mockery; 1 mark: explains ‘therefore’ or the age gap')
RIVER.i('Looking back now, I am amazed that either of us was allowed near that water.', 'What does this sentence show about the difference between the child and the adult writer?',
        'The adult can see the danger the child did not; it adds reflection, showing how the writer’s understanding has changed over time.', '1 mark: adult hindsight/reflection; 1 mark: awareness of danger now vs then')
RIVER.i('I have never since felt quite so proud', 'Why is this an effective ending?', 'It shows the significance of the experience, linking the childhood event to a lasting feeling and giving the memoir a reflective conclusion.',
        '1 mark: significance/reflection; 1 mark: links past to present')
RIVER.f('I sank like a stone.', 'simile', 'like a stone', 'the short, blunt comparison captures how suddenly and helplessly the child went under, with some humour.', also=('short sentence',))
RIVER.f('Under the water everything turned green and silent', 'sensory imagery', 'green and silent', 'the sight and sound details recreate the strange, dreamlike calm of being underwater.')
RIVER.f('I coughed half the river onto the bank.', 'hyperbole', 'half the river', 'the exaggeration is comic and shows how much water the child swallowed.')
RIVER.f("'Again,' he said.", 'short sentence', "Again", 'Bilal’s one-word reply is comically unsympathetic and shows his determination as a teacher.', also=('dialogue',))
RIVER.x('How does the writer present the experience of learning to swim?', 'Humorous, affectionate tone; Bilal as a comic, determined teacher; vivid sensory moment underwater; hyperbole; adult reflection (Looking back now); pride at the end.')

SATO = Text('sato', 'biography', 'an extract from a biography of the (fictional) engineer Hana Sato', """
Hana Sato was born in 1961 in a fishing village on the coast of Japan, the youngest of five children. Her father
repaired boat engines, and by the age of eight Hana could strip down an outboard motor faster than most of his
customers. At school she was quiet, often in trouble for taking apart the classroom clock. In 1983 she became one of only
two women to graduate in mechanical engineering from her university that year. Her breakthrough came in 1998, when she
designed a low-cost water pump that could be repaired with a bicycle spanner. Instead of selling it to large companies,
she published the design for free. Today the pump is used in more than forty countries. 'An invention nobody can fix,' she
once said, 'is only half an invention.'""")
SATO.r('Hana Sato was born in 1961 in a fishing village on the coast of Japan', 'Where was Hana Sato born?', 'In a fishing village on the coast of Japan', ['In Tokyo', 'In a mountain town', 'On a boat', 'Abroad'])
SATO.r('Her breakthrough came in 1998', 'When did Hana Sato have her breakthrough?', '1998', ['1961', '1983', '2008', '1969'])
SATO.r('Today the pump is used in more than forty countries.', 'In how many countries is the pump used?', 'More than forty', ['Five', 'Two', 'Eight', 'Over four hundred'])
SATO.i('often in trouble for taking apart the classroom clock', 'Why might the biographer include this detail?', 'It is an anecdote that shows her early curiosity about machines, foreshadowing her career as an engineer, and adds human interest.',
       '1 mark: shows curiosity/early talent; 1 mark: links to later career or engages reader')
SATO.i('Instead of selling it to large companies, she published the design for free.', 'What does this suggest about Hana Sato’s values?', 'She cared more about helping people than about money; she wanted the pump to be available to everyone.',
       '1 mark: generous/idealistic; 1 mark: reference to choosing free publication over profit')
SATO.i("'An invention nobody can fix,' she once said, 'is only half an invention.'", 'Why does the biographer end with this quotation?', 'Her own words sum up her philosophy and leave the reader with a memorable impression of her personality and beliefs.',
       '1 mark: sums up beliefs; 1 mark: memorable ending/her own voice')
SATO.x('How does the biographer present Hana Sato as an admirable person?', 'Chronological structure; early anecdotes of talent; achievement against the odds (one of two women); practical genius (bicycle spanner); generosity (free design); impact (forty countries); her own words.')

TORONTO = Text('toronto', 'autobiography', 'an autobiography extract, ‘Arrival’', """
The first thing I noticed about Toronto was the cold. It was not the friendly cold of a fridge door opened on a hot day
in Lahore; it was a cold with teeth. My father had bought us coats from a market before we left, thin padded things that
the wind went straight through. At my new school, the teacher said my name wrongly, and I was too shy to correct her, so
for two whole years I answered to a name that was not quite mine. I did not speak in class for a month. Then one
afternoon a girl called Grace asked if she could borrow my eraser, and when I answered, she said, 'Oh! You talk!' and
laughed, and suddenly so did I. We are still friends. She still has my eraser.""")
TORONTO.r('The first thing I noticed about Toronto was the cold.', 'What did the writer notice first about Toronto?', 'The cold', ['The size of the school', 'The friendly people', 'The traffic', 'The food'])
TORONTO.r('for two whole years I answered to a name that was not quite mine', 'For how long did the writer answer to the wrong name?', 'Two years', ['A month', 'One afternoon', 'One term', 'Five years'])
TORONTO.r('a girl called Grace asked if she could borrow my eraser', 'What did Grace ask to borrow?', 'An eraser', ['A coat', 'A pen', 'A book', 'Some money'])
TORONTO.i('I was too shy to correct her, so for two whole years I answered to a name that was not quite mine', 'What does this suggest about how the writer felt at the new school?',
          'They felt shy and lost part of their identity; the wrong name symbolises how they did not feel fully themselves in the new country.', '1 mark: shy/displaced; 1 mark: symbolic loss of identity')
TORONTO.i('We are still friends. She still has my eraser.', 'How does the writer end the extract, and why is it effective?', 'With two short, humorous sentences in the present tense, linking past and present and showing the lasting friendship with warmth.',
          '1 mark: humour/warmth; 1 mark: link between past and present')
TORONTO.f('it was a cold with teeth', 'metaphor', 'a cold with teeth', 'the cold seems to bite like an animal, showing how harsh and hostile the new place felt.', also=('personification',))
TORONTO.f('It was not the friendly cold of a fridge door opened on a hot day in Lahore', 'contrast', 'the friendly cold of a fridge door', 'comparing the pleasant cold of home with the harsh new cold shows the writer’s homesickness.')
TORONTO.f('I did not speak in class for a month.', 'short sentence', 'I did not speak in class for a month.', 'the plain sentence emphasises the writer’s isolation and silence.')
TORONTO.x('How does the writer present their experience of arriving in a new country?', 'Metaphor of cold with teeth; contrast with home; detail of thin coats; lost name; silence; turning point with Grace; humour and warmth in the ending.')
LIFE = [RIVER, SATO, TORONTO]

# ---------------------------------------------------------------- 6.1 features
LIFE_TYPES = ['autobiography', 'biography', 'memoir', 'diary', 'recount']
LIFE_SNIP = [
    ('I was born in Accra in 1990, the year the river flooded our street.', 'autobiography', 'first person, the writer’s own life from birth.'),
    ('She was born in Accra in 1990 and grew up to become the country’s youngest judge.', 'biography', 'third person account of another person’s life.'),
    ('Dear Diary, Today was the worst day of term. Tomorrow will be better, I hope.', 'diary', 'dated, private, informal entry written as things happen.'),
    ('That summer at my grandmother’s farm taught me more about patience than any school ever did.', 'memoir', 'focuses on one period and reflects on its meaning.'),
    ('On Tuesday our class visited the science museum. First we saw the planetarium; then we tried the robotics workshop.', 'recount', 'retells events in time order, usually soon after they happened.'),
    ('Throughout his career, the architect insisted on visiting every building site personally, according to colleagues.', 'biography', 'third person and uses others’ accounts as sources.'),
    ('Monday 3 March. Rained again. Mum says we might move house.', 'diary', 'date heading, note-like, immediate.'),
    ('Looking back, I realise that the year we spent in that tiny flat shaped who I am.', 'memoir', 'reflective, hindsight, a significant period.'),
    ('In this book I tell the story of my life, from my childhood in Hanoi to my years as a pilot.', 'autobiography', 'first person account of the whole of the writer’s life.'),
    ('Yesterday our team travelled to the regional final. We arrived at nine, warmed up and played our first match at ten.', 'recount', 'chronological retelling of an event.'),
]
t61 = topic('Features of autobiography, biography and memoir', 'features of autobiography biography and memoir')
t61.fixed('C1', (1, 2), ret_items(LIFE) + [
    ('What is the main difference between an autobiography and a biography?', 'An autobiography is written by the subject about themself; a biography is written by someone else', 'Auto = self.',
     ['A biography is always fiction', 'An autobiography is always in the third person', 'There is no difference']),
    ('Which feature is most typical of a memoir?', 'Reflection on the meaning of particular experiences', 'Memoirs focus on selected memories and what they meant.', ['A complete list of dates from birth to death', 'Stage directions', 'A rhyme scheme']),
    ('Which of these would a biographer most likely use as a source?', 'Letters, interviews and records about the person', 'Biographers research evidence about their subject.', ['Their own childhood memories', 'Invented dialogue only', 'A dictionary']),
    ('How is life writing usually organised?', 'chronologically, though it may use flashbacks', 'Time order is common, sometimes with shifts for effect.', ['alphabetically', 'by rhyme', 'randomly']),
])
classify_templates(t61, LIFE_SNIP, LIFE_TYPES, ['Which type of life writing is this most likely to be from? {q}', 'Read the extract: {q} What kind of text is it from?'],
                   C2frames=['This extract is from a {label}: {q} Explain two features that show this.'],
                   C3frames=[('Identify the type of life writing in this extract, explain the features that show it, and rewrite the sentence as a different type (e.g. biography into autobiography): {q}',
                              lambda it: f'{cap(it[1])}: {it[2]} The rewrite should change person and/or tense and tone appropriately.',
                              lambda it, m: f'{upto(m)}: 1 for the type ({it[1]}); 1 for supporting features; remaining mark(s) for an accurate rewrite in a different form.')])
t61.fixed('C2', (2, 3), [i for i in inf_items(LIFE) if 'biographer' in i[1] or 'Looking back' in i[0] or 'ending' in i[1].lower() or 'end' in i[1]])


@t61.add('C3', (2, 3, 4, 5), 'explain')
def t61_compare(r, D):
    A, B = r.sample(LIFE, 2)
    m = mk('C3', D)
    tag = {'memoir': 'memoir (first person, one period, reflective)', 'biography': 'biography (third person, researched facts, chronological, quotation from the subject)', 'autobiography': 'autobiography (first person, the writer’s own experiences, reflection)'}
    return {'stem': f'Text A is {A.label}: {Q(A.text)} Text B is {B.label}: {Q(B.text)} Explain two differences between the ways the two texts are written, linked to their type of life writing.',
            'answer': f'Text A is a {tag[A.kind]}; Text B is a {tag[B.kind]}. Differences may include person (first/third), use of reflection versus facts and dates, tone and use of quotation.',
            'key': f'{upto(m)}: 1 per valid difference with evidence from both texts; further marks for linking features to the purpose of each type.'}


compose_templates(t61, LIFE, C=('C4',))

# ---------------------------------------------------------------- 6.2 presenting people and events
t62 = topic('How writers present people and events in life writing', 'analysing how writers present people and events', 'life writing')
t62.fixed('C2', (2, 3, 4), inf_items(LIFE))
feature_templates(t62, [f for T in LIFE for f in T.feats], NARR + ['sensory imagery'])
extended_templates(t62, LIFE)
LIFE_CMP = ['the challenges the writer or subject faces and how they respond', 'the way the writers make people and events vivid for the reader', 'the use of humour, anecdote and personal detail']


@t62.add('C4', (2, 3, 4, 5), 'long')
def t62_cmp(r, D):
    A, B = r.sample(LIFE, 2)
    asp = r.choice(LIFE_CMP)
    m = mk('C4', D, 'long')
    ind = f'Text A: {A.foci[0][1]} Text B: {B.foci[0][1]} Comparison of how each presents {asp}, with reference to person, tone, structure and language.'
    qa = ' … '.join(Q(x[0]) for x in r.sample(A.infs, 2))
    qb = ' … '.join(Q(x[0]) for x in r.sample(B.infs, 2))
    return {'stem': f'Here are extracts from two pieces of life writing. Text A ({A.label}): {qa} Text B ({B.label}): {qb} Compare how the two writers present {asp}. Refer closely to language and structure in both texts.',
            'answer': ind, 'key': reading_key(m, ind)}
compose_templates(t62, LIFE, C=('C3',))

# ---------------------------------------------------------------- 6.3 writing a memoir with reflection
MEMOIR_PROMPTS = ['a time you were afraid but did something anyway', 'a person who changed the way you see the world', 'a place you have left behind', 'the first time you were trusted with responsibility',
                  'a meal that you will never forget', 'a mistake that taught you something important', 'a journey that changed you', 'a moment you felt you truly belonged somewhere',
                  'an object that holds a special memory for you', 'a day when everything went wrong']
REFLECT = [
    ('We moved house when I was ten. I went to a new school.', 'We moved house when I was ten, and although I hated the new school at first, I can see now that it taught me how to make friends from nothing.'),
    ('My grandfather gave me his old watch.', 'My grandfather gave me his old watch, and only later did I understand that he was really giving me his time – the hours he would no longer have.'),
    ('I forgot my lines in the school play.', 'I forgot my lines in the school play; at the time it felt like the end of the world, but it was the first time I learned that people forgive mistakes faster than we do.'),
    ('We got lost on the mountain and found the path at sunset.', 'We got lost on the mountain and found the path at sunset, and I think that was when I first realised my father did not know everything – and that this was all right.'),
    ('I broke my arm falling off my bike.', 'I broke my arm falling off my bike, and those six weeks of one-handed life taught me more about patience than any lesson ever had.'),
    ('My best friend moved to another country.', 'My best friend moved to another country, and looking back, that goodbye was the moment I discovered that distance changes friendship but does not end it.'),
]
t63 = topic('Writing a personal recount or memoir with reflection', 'writing a personal recount or memoir', 'reflection')
t63.fixed('C1', (1, 2), [
    ('What is reflection in a memoir?', 'Thinking about the meaning or significance of an experience', 'E.g. ‘Looking back, I realise…’.', ['Describing the weather', 'Listing what happened in order', 'Using dialogue']),
    ('Which phrase signals reflection?', 'Only later did I understand', 'It shows hindsight and changed understanding.', ['Then we went home', 'It was a sunny day', 'Suddenly, there was a noise']),
    ('Why might a memoir writer use the present tense in the final paragraph?', 'To link the past experience to who they are now', 'Shifting to the present shows the lasting effect.', ['Because memoirs must end in the future tense', 'To hide the ending', 'To make it a diary']),
])
t63.fixed('C2', (2, 3), [
    ('Explain why a memoir focuses on a few key moments rather than everything that happened.', 'Selecting significant moments keeps the reader interested and allows the writer to explore their meaning in depth.', '1 mark: selection/interest; 1 mark: depth of reflection.'),
    ('Explain how dialogue can bring a memoir to life.', 'Remembered speech recreates people’s voices and personalities and makes the scene immediate, as with Bilal’s ‘Just kick’.', '1 mark: character/voice; 1 mark: immediacy, with example.'),
    ('Explain the difference between a recount and a memoir.', 'A recount retells events in order; a memoir also explores feelings and the significance of the events, often with adult hindsight.', '1 mark: what a recount does; 1 mark: what a memoir adds (feelings, significance, hindsight).'),
])
@t63.add('C2', (1, 2, 3), 'explain')
def t63_reflect(r, D):
    plain, refl = r.choice(REFLECT)
    m = mk('C2', D)
    frame = r.choice(['A memoir writer changes {a} to {b} Explain what the added reflection does for the reader.',
                      'Compare these two versions of a sentence from a memoir. First draft: {a} Final draft: {b} Explain why the final draft is more effective.',
                      'In a recount, the writer revises {a} into {b} How does this change help the reader understand the experience?'])
    return {'stem': frame.format(a=Q(plain), b=Q(refl)),
            'answer': 'It turns a bare event into a meaningful memory: the older writer looks back and explains what the experience taught them, so the reader understands its significance.',
            'key': f'{upto(m)}: shows hindsight or a change in understanding; explains the significance or lesson of the event; links past and present self.'}


rewrite_templates(t63, [('Add reflection to this sentence from a recount so that it shows what the experience meant to the writer.', a, f'Model: {Q(b)}', 'Award for: reflective phrase (looking back, I realise, only later); a clear insight; accurate expression.') for a, b in REFLECT],
                  ['{ins} {q}', '{q} {ins}'], D=(1, 2, 3, 4))
@t63.add('C3', (2, 3, 4, 5), 'short')
def t63_open(r, D):
    p_ = r.choice(MEMOIR_PROMPTS)
    m = mk('C3', D)
    return {'stem': f'Write the opening paragraph of a memoir about {p_}. Include at least two sensory details and end with one sentence of reflection that looks back from the present.',
            'answer': 'Model: begins at a vivid moment in the past tense, with sight/sound/smell details, and ends with a reflective present-tense sentence (e.g. ‘Even now, I can see…’ or ‘I did not know then that…’).',
            'key': f'{upto(m)}: vivid opening moment; two or more sensory details; reflective final sentence showing hindsight; accurate tense control.'}


writing_templates(t63, [(f'Write a memoir about {p}. Include vivid detail of the experience and reflection on what it meant to you.',
                         'focused, selected moments; sensory detail; remembered dialogue; reflective comments showing hindsight; ending that links past to present.',
                         f'Model structure: opening at a vivid moment; context; the key incident with sensory detail and dialogue; turning point; reflection (‘Looking back…’) on what {p} taught you.') for p in MEMOIR_PROMPTS], 'recount')
CHAPTERS[6] = [t61, t62, t63]


# =========================================================== Unit 7 Fiction from different times and cultures

THORN = Text('thorn', 'older', 'an extract written in a nineteenth-century style, ‘The House at Thornleigh’', """
It was upon a raw evening in the latter part of November that I first beheld the house at Thornleigh. The coach, which
had laboured since noon along roads more fit for ducks than horses, set me down at the gate and departed with indecent
haste, as though the driver had no wish to linger. I confess that my spirits sank. Before me rose a long, low dwelling of
grey stone, its windows shuttered, its chimneys smokeless, and about it a garden so overgrown that the very paths had
been swallowed up. I had been promised a cheerful household and a warm welcome; I perceived neither. Yet I had come too
far to turn back, and, gathering my cloak about me, I advanced towards the door.""")
THORN.r('It was upon a raw evening in the latter part of November', 'When does the narrator arrive?', 'On a cold evening late in November', ['On a summer morning', 'At noon in early November', 'On a December night', 'At dawn in spring'])
THORN.r('set me down at the gate and departed with indecent haste', 'What does the coach do after setting the narrator down?', 'Leaves very quickly', ['Waits for the narrator', 'Drives up to the house', 'Breaks down at the gate', 'Turns back to collect luggage'])
THORN.r('its windows shuttered, its chimneys smokeless', 'Which detail shows that no fires are lit in the house?', 'Its chimneys are smokeless', ['Its windows are shuttered', 'The garden is overgrown', 'The stone is grey', 'The paths are hidden'])
THORN.i('departed with indecent haste, as though the driver had no wish to linger', 'What does the driver’s behaviour suggest about the house?',
        'The driver’s rush to leave hints that the house has a bad reputation or is frightening, which foreshadows trouble.', '1 mark: house is feared/unwelcoming; 1 mark: reference to ‘indecent haste’ or ‘no wish to linger’')
THORN.i('I had been promised a cheerful household and a warm welcome; I perceived neither.', 'How does this sentence create a sense of disappointment?',
        'The semicolon sets the hopeful expectation against the blunt reality in two words, ‘perceived neither’, emphasising the narrator’s let-down.', '1 mark: contrast of expectation and reality; 1 mark: reference to structure/‘perceived neither’')
THORN.i('Yet I had come too far to turn back, and, gathering my cloak about me, I advanced towards the door.', 'What does this suggest about the narrator?',
        'The narrator is determined and brave despite fear; ‘Yet’ shows them overcoming doubt, and ‘advanced’ sounds purposeful.', '1 mark: determined/brave; 1 mark: reference to ‘Yet’ or ‘advanced’')
THORN.f('along roads more fit for ducks than horses', 'hyperbole', 'more fit for ducks than horses', 'the comic exaggeration shows the roads were flooded and muddy, stressing a long, miserable journey.')
THORN.f('a garden so overgrown that the very paths had been swallowed up', 'personification', 'swallowed up', 'the garden seems to devour the paths, making the place feel wild, neglected and threatening.', also=('metaphor',))
THORN.f('its windows shuttered, its chimneys smokeless', 'listing', 'its windows shuttered, its chimneys smokeless', 'the list of closed, lifeless features builds an impression of a cold, unwelcoming house.', also=('repetition',))
THORN.x('How does the writer create a mysterious and unwelcoming atmosphere in this extract?', 'Raw November evening; driver’s indecent haste; shuttered windows and smokeless chimneys; personified garden swallowing paths; contrast of promised welcome with reality; long formal sentences and the narrator’s sinking spirits.')

LETTER = Text('letter', 'older', 'a letter written in a nineteenth-century style, from Charlotte to her sister', """
My dearest Eliza, You will forgive, I hope, the shortness of this letter, for I write in great haste and by a failing
candle. Mamma is much recovered, though the physician forbids her to venture out of doors until the weather mends. Our
neighbour Mr Fenwick called upon us twice this week, and on the second occasion brought a basket of hothouse grapes,
which Mamma declared to be very civil of him, and which I declared to be very sour. I am resolved to say no more of Mr
Fenwick. Pray write soon and tell me all your news, for there is none here worth the telling. Your ever affectionate
sister, Charlotte.""")
LETTER.r('Mamma is much recovered', 'How is Mamma’s health?', 'She is much better', ['She is worse', 'She has gone out', 'She is travelling', 'She has written to Eliza'])
LETTER.r('Our neighbour Mr Fenwick called upon us twice this week', 'How many times did Mr Fenwick visit this week?', 'Twice', ['Once', 'Three times', 'Every day', 'Not at all'])
LETTER.r('brought a basket of hothouse grapes', 'What did Mr Fenwick bring?', 'A basket of grapes', ['A letter', 'A candle', 'Medicine for Mamma', 'Some books'])
LETTER.i('which Mamma declared to be very civil of him, and which I declared to be very sour', 'What does this contrast suggest about Charlotte’s feelings towards Mr Fenwick?',
         'Charlotte is irritated by or pretends to dislike Mr Fenwick, while Mamma approves of him; ‘sour’ may describe her attitude more than the grapes.', '1 mark: dislike/irritation (or hidden interest); 1 mark: contrast with Mamma’s ‘civil’')
LETTER.i('I am resolved to say no more of Mr Fenwick.', 'Why might a reader find this sentence amusing or revealing?',
         'She has just written a great deal about him, so her resolution suggests he occupies her thoughts more than she admits.', '1 mark: irony; 1 mark: hidden interest')
LETTER.x('What impressions of Charlotte and her life does the letter create?', 'Affectionate to her sister; witty and sharp (sour grapes); dutiful about Mamma; bored at home (no news worth telling); hidden feelings about Mr Fenwick; formal nineteenth-century conventions of address and sign-off.')

MILL = Text('mill', 'older', 'an extract written in a nineteenth-century style, ‘The Mill’', """
The mill stood at the bottom of the valley, where the river ran swiftest, and its great wheel turned day and night with
a groaning that could be heard a mile off. The children of the village were forbidden to go near it, which naturally
ensured that they went near it at every opportunity. Old Josiah Crane, who had been miller there for forty years, was
reputed to be a hard man, though none could say he had ever done them any particular harm; he was merely silent, and in
a village where everybody's business was common property, silence was itself a kind of crime.""")
MILL.r('Old Josiah Crane, who had been miller there for forty years', 'How long had Josiah Crane been the miller?', 'Forty years', ['Four years', 'Fourteen years', 'A mile', 'Since he was a child'])
MILL.r('The children of the village were forbidden to go near it', 'What were the village children forbidden to do?', 'Go near the mill', ['Swim in the river', 'Speak to the miller', 'Leave the village', 'Play at night'])
MILL.i('which naturally ensured that they went near it at every opportunity', 'How does the writer create humour here?', 'The ironic ‘naturally ensured’ points out that forbidding children to do something makes them want to do it more.',
       '1 mark: irony identified; 1 mark: explanation of the joke about children')
MILL.i('in a village where everybody\'s business was common property, silence was itself a kind of crime', 'What does this suggest about the villagers?',
       'They are nosy gossips who distrust privacy; Josiah is judged simply for keeping to himself, not for any wrongdoing.', '1 mark: gossiping/nosy; 1 mark: unfair judgement of Josiah')
MILL.f('its great wheel turned day and night with a groaning that could be heard a mile off', 'personification', 'groaning', 'the wheel seems to groan like a suffering person, giving the mill a heavy, ominous presence.', also=('hyperbole', 'onomatopoeia'))
MILL.f('which naturally ensured that they went near it at every opportunity', 'irony', 'naturally ensured', 'the narrator’s dry comment mocks the predictable disobedience of children.')
MILL.x('How does the writer present Josiah Crane and the village?', 'Ominous mill (groaning wheel); ironic narrator; Josiah reputed hard but harmless; villagers nosy (common property); long, balanced sentences with semicolons typical of older prose.')
OLDER = [THORN, LETTER, MILL]

# ---------------------------------------------------------------- 7.1 older fiction
ARCHAIC = [
    ('beheld', 'saw', 'I first beheld the house at Thornleigh', ['held tightly', 'left behind', 'built']),
    ('laboured', 'struggled with great effort', 'The coach, which had laboured since noon', ['rested', 'raced easily', 'been repaired']),
    ('indecent haste', 'rude, unseemly speed', 'departed with indecent haste', ['great caution', 'a heavy load', 'loud singing']),
    ('I confess', 'I admit', 'I confess that my spirits sank', ['I deny', 'I pretend', 'I forget']),
    ('dwelling', 'house or home', 'a long, low dwelling of grey stone', ['well', 'barn', 'wall']),
    ('perceived', 'noticed or saw', 'I perceived neither', ['expected', 'refused', 'promised']),
    ('advanced', 'moved forward', 'I advanced towards the door', ['ran away', 'waited', 'knocked loudly']),
    ('physician', 'doctor', 'the physician forbids her to venture out', ['priest', 'neighbour', 'servant']),
    ('venture', 'dare to go', 'forbids her to venture out of doors', ['refuse', 'sleep', 'write']),
    ('civil', 'polite', 'very civil of him', ['rude', 'expensive', 'unusual']),
    ('resolved', 'determined', 'I am resolved to say no more', ['unable', 'forbidden', 'eager']),
    ('Pray', 'Please', 'Pray write soon', ['Never', 'Perhaps', 'Quickly']),
    ('reputed', 'said by others', 'was reputed to be a hard man', ['proved', 'known for certain', 'paid']),
    ('common property', 'known to everyone', "everybody's business was common property", ['owned by the council', 'kept secret', 'very valuable']),
    ('the latter part', 'the later part', 'in the latter part of November', ['the first part', 'the coldest part', 'the middle']),
    ('mends', 'improves', 'until the weather mends', ['breaks', 'worsens', 'changes colour']),
]
MODERNISE = [
    ('It was upon a raw evening in the latter part of November that I first beheld the house at Thornleigh.', 'I first saw the house at Thornleigh on a cold, damp evening late in November.'),
    ('I confess that my spirits sank.', 'I admit I felt my heart sink.'),
    ('I had been promised a cheerful household and a warm welcome; I perceived neither.', 'I had been told I would find a happy home and a warm welcome, but I saw neither.'),
    ('You will forgive, I hope, the shortness of this letter, for I write in great haste and by a failing candle.', 'Sorry this letter is short – I am writing quickly and my candle is going out.'),
    ('the physician forbids her to venture out of doors until the weather mends', 'the doctor will not let her go outside until the weather gets better'),
    ('Pray write soon and tell me all your news, for there is none here worth the telling.', 'Please write soon with all your news, because nothing interesting is happening here.'),
    ('Old Josiah Crane, who had been miller there for forty years, was reputed to be a hard man', 'People said that old Josiah Crane, who had run the mill for forty years, was a harsh man'),
    ('though none could say he had ever done them any particular harm', 'although nobody could name anything bad he had actually done to them'),
]
SYNTAX = [
    ('Before me rose a long, low dwelling of grey stone', 'inverted word order (verb before subject)', 'placing ‘rose’ before ‘a long, low dwelling’ delays the house, building suspense and a formal, dramatic tone.'),
    ('You will forgive, I hope, the shortness of this letter', 'an interrupting clause', '‘I hope’ is inserted politely in the middle of the sentence, typical of formal older letters.'),
    ('The coach, which had laboured since noon along roads more fit for ducks than horses, set me down at the gate', 'a long sentence with an embedded relative clause', 'the clause about the journey delays the main verb, mimicking the slow, tiring journey.'),
    ('I had been promised a cheerful household and a warm welcome; I perceived neither.', 'a semicolon balancing two clauses', 'the two halves are balanced, setting expectation against reality.'),
    ('he was merely silent, and in a village where everybody\'s business was common property, silence was itself a kind of crime', 'a long, multi-clause sentence', 'the building clauses lead to a witty final judgement, typical of nineteenth-century narrators.'),
]
t71 = topic('Reading older and pre-twentieth-century fiction', 'reading older and pre-twentieth-century fiction', 'archaic vocabulary and syntax')
t71.fixed('C1', (1, 2), ret_items(OLDER) + [
    ('Which feature is typical of nineteenth-century prose?', 'Long sentences with several clauses and formal vocabulary', 'Older prose often uses complex syntax, semicolons and formal or archaic words.',
     ['Text-message abbreviations', 'Very short, one-word paragraphs throughout', 'Modern slang']),
    ('What is archaic vocabulary?', 'Words that are old-fashioned and rarely used today', 'E.g. ‘beheld’, ‘pray’ (please), ‘physician’.', ['Technical scientific words', 'Words borrowed from other languages', 'Words that rhyme']),
    ('Why do older texts often seem formal to modern readers?', 'Conventions of politeness and writing style were different', 'Social conventions shaped formal address and style.', ['They were all written by lawyers', 'They were written for very young children', 'They have no punctuation']),
])


@t71.add('C1', (1, 2, 3))
def t71_word(r, D):
    w, mean, ctx, ds = r.choice(ARCHAIC)
    opts, ans = mcq(r, mean, ds)
    return {'stem': f'In the phrase {Q(ctx)}, what does {Q(w)} mean?', 'options': opts, 'answer': ans, 'key': f'{Q(w)} means {Q(mean)} here; use the context to work out older vocabulary.'}


@t71.add('C2', (1, 2, 3), 'short')
def t71_ctx(r, D):
    w, mean, ctx, ds = r.choice(ARCHAIC)
    return {'stem': f'Use the context to explain what {Q(w)} means in {Q(ctx)}, and suggest a modern word or phrase that could replace it.', 'answer': f'{cap(mean)}. A modern replacement: {mean}.',
            'key': keypts('1 mark: accurate meaning; 1 mark: suitable modern equivalent that fits the sentence.')}


rewrite_templates(t71, [('Rewrite this sentence in modern English, keeping the meaning.', a, f'Model: {Q(b)}', 'Award for accurate meaning; archaic words replaced; natural modern syntax.') for a, b in MODERNISE],
                  ['{ins} {q}', 'Translate this older-style sentence into everyday modern English: {q}'], D=(1, 2, 3, 4))
classify_templates(t71, [(a, b, c) for a, b, c in SYNTAX], [b for _, b, _ in SYNTAX],
                   ['Which feature of older syntax is shown in {q}?'],
                   C2frames=['This sentence uses {label}: {q} Explain its effect.'],
                   C3frames=[('Analyse how the structure of this older-style sentence creates an effect: {q}', lambda it: f'{cap(it[1])}: {it[2]}', lambda it, m: f'{upto(m)}: 1 for identifying the structure; remaining marks for explaining its effect with reference to the words.')])
t71.fixed('C2', (2, 3), inf_items(OLDER))
extended_templates(t71, OLDER)
compose_templates(t71, OLDER, C=('C4',))
OLD_TASKS = [
    ('Write a letter in a nineteenth-century style from Eliza replying to her sister Charlotte, using formal address, older vocabulary and longer sentences.', 'formal greeting and sign-off; archaic vocabulary (pray, resolved, civil); balanced, multi-clause sentences; witty response to the news about Mr Fenwick.'),
    ('Continue the story of the narrator arriving at Thornleigh, writing in a style that imitates nineteenth-century prose.', 'first-person formal narrator; long sentences with semicolons; older vocabulary; atmosphere of mystery as the door opens.'),
    ('Rewrite the extract from ‘The Mill’ as a modern story opening set in the present day, keeping the irony but using contemporary language.', 'modern vocabulary and syntax; same ironic narrator; Josiah updated (e.g. a silent neighbour); comparison of how the style has changed.'),
    ('Write a diary entry, in a nineteenth-century style, by one of the village children who has crept into the mill.', 'dated entry; formal, older diction; suspense; impressions of Josiah Crane.'),
]
writing_templates(t71, [(a, b, f'Model approach: {b}') for a, b in OLD_TASKS], ('convincing imitation or transformation of older style; content developed with clear purpose', 'some features of older style; content mostly clear', 'little sense of older style; limited content'))

# ---------------------------------------------------------------- 7.2 setting and cultural context
LANTERN = Text('lantern', 'fiction', 'an extract from a story set in Vietnam, ‘The Lantern Festival’', """
On the night of the full moon, the old town of Hoi An switched off its electric lights. Linh had seen it every year of
her life, but it still made her catch her breath. One by one, the silk lanterns glowed into life along the riverbank, red
and gold and green, until the water itself seemed to burn. Her grandmother pressed a paper lantern into her hands, a
candle flickering inside. 'Make a wish for someone else,' she said. 'Wishes for yourself sink.' Linh thought of her
father, working on a ship somewhere beyond the edge of the map, and set the lantern on the water. It wobbled, steadied,
and drifted out to join the thousands of others, a slow river of light carrying everyone's hopes towards the sea.""")
LANTERN.r('On the night of the full moon, the old town of Hoi An switched off its electric lights.', 'What happens in Hoi An on the night of the full moon?', 'The town switches off its electric lights', ['A storm hits the town', 'Ships leave the harbour', 'Everyone stays indoors', 'The river floods'])
LANTERN.r("'Make a wish for someone else,' she said. 'Wishes for yourself sink.'", 'What does Linh’s grandmother tell her to do?', 'Make a wish for someone else', ['Make a wish for herself', 'Keep the lantern', 'Blow out the candle', 'Go home'])
LANTERN.r('Linh thought of her father, working on a ship', 'Where is Linh’s father?', 'Working on a ship far away', ['At home in Hoi An', 'Beside her on the riverbank', 'In the old town market', 'At school'])
LANTERN.i("'Make a wish for someone else,' she said. 'Wishes for yourself sink.'", 'What does this tradition suggest about the values of the community?', 'It suggests selflessness and caring for others are valued; the belief is passed down from the older generation.',
          '1 mark: selflessness/community; 1 mark: tradition passed on by grandmother')
LANTERN.i('working on a ship somewhere beyond the edge of the map', 'What does this phrase suggest about how Linh feels about her father?', 'He seems impossibly far away; she misses him and perhaps worries about him.', '1 mark: distance/longing; 1 mark: reference to ‘beyond the edge of the map’')
LANTERN.f('until the water itself seemed to burn', 'hyperbole', 'the water itself seemed to burn', 'the reflected lights are so bright and many that the river appears on fire, a magical, overwhelming image.', also=('metaphor',))
LANTERN.f('a slow river of light carrying everyone\'s hopes towards the sea', 'metaphor', 'a slow river of light', 'the lanterns form a second river, suggesting the shared hopes of the whole community moving together.')
LANTERN.f('It wobbled, steadied, and drifted out', 'listing', 'wobbled, steadied, and drifted', 'the sequence of verbs slows the moment and mirrors Linh’s anxious hope for her father.')
LANTERN.x('How does the writer use the setting and cultural tradition to show Linh’s feelings?', 'Lantern festival as a communal tradition; magical light imagery; grandmother’s belief; father’s distance; the lantern’s journey mirrors Linh’s hope.')

HARMATTAN = Text('harmattan', 'fiction', 'an extract from a story set in northern Ghana, ‘Harmattan’', """
When the harmattan came, it came quietly. One morning Kwame woke and the sun had turned into a pale coin behind a
curtain of dust. The wind from the Sahara had arrived in the night, as it did every December, carrying the desert with
it. By noon there was a fine red powder on everything: on the windowsills, on his mother's sewing machine, on the leaves
of the mango tree, even on his tongue. His lips cracked. The nights grew cold enough for blankets. Yet the old men under
the neem tree welcomed it. 'The harmattan dries the grain,' his grandfather said, 'and it reminds the young that the
world is bigger than their village.'""")
HARMATTAN.r('as it did every December, carrying the desert with it', 'When does the harmattan arrive?', 'Every December', ['Every June', 'Only once in a lifetime', 'At the start of the rainy season', 'Every afternoon'])
HARMATTAN.r('The wind from the Sahara had arrived in the night', 'Where does the harmattan wind come from?', 'The Sahara', ['The sea', 'The mountains', 'The mango tree', 'The city'])
HARMATTAN.r("'The harmattan dries the grain,' his grandfather said", 'According to the grandfather, what is one benefit of the harmattan?', 'It dries the grain', ['It brings rain', 'It cools the days', 'It cleans the windows', 'It waters the mango tree'])
HARMATTAN.i('Yet the old men under the neem tree welcomed it.', 'Why might the old men welcome the harmattan?', 'They understand its benefits for farming and see it as part of the natural cycle, unlike the young who notice only the discomfort.',
            '1 mark: benefits/wisdom; 1 mark: contrast with discomfort described earlier')
HARMATTAN.i("'and it reminds the young that the world is bigger than their village.'", 'What does the grandfather mean?', 'The dust from far away shows that the village is connected to a vast world; it encourages humility and curiosity.',
            '1 mark: connection to wider world; 1 mark: lesson for the young')
HARMATTAN.f('the sun had turned into a pale coin behind a curtain of dust', 'metaphor', 'a pale coin', 'the sun is dimmed and flat like a coin, showing how thick the dust is and creating an eerie atmosphere.')
HARMATTAN.f('When the harmattan came, it came quietly.', 'personification', 'it came quietly', 'the wind arrives like a silent visitor, making it seem powerful and mysterious.', also=('repetition',))
HARMATTAN.f('on the windowsills, on his mother\'s sewing machine, on the leaves of the mango tree, even on his tongue', 'listing', 'even on his tongue', 'the list builds to the most personal place, showing the dust gets everywhere.', also=('repetition',))
HARMATTAN.x('How does the writer present the harmattan and its importance to the community?', 'Quiet, personified arrival; metaphors of coin and curtain; list of dust everywhere; physical discomfort; old men’s welcome; grandfather’s wisdom about the wider world.')
CULTURE = [LANTERN, HARMATTAN]
t72 = topic('How setting and cultural context shape a story', 'setting and cultural context', 'shape a story')
t72.fixed('C1', (1, 2), ret_items(CULTURE) + [
    ('What is meant by the cultural context of a story?', 'The customs, beliefs and way of life of the people and place in which it is set', 'Context shapes characters’ values, choices and conflicts.', ['The number of chapters', 'The author’s handwriting', 'The price of the book']),
    ('How can setting affect a story’s plot?', 'It can create problems or opportunities that drive what characters do', 'E.g. a festival, a storm or a remote place shapes events.', ['It never affects the plot', 'It only matters in poetry', 'It decides the title only']),
])
t72.fixed('C2', (2, 3), inf_items(CULTURE))
feature_templates(t72, [f for T in CULTURE for f in T.feats], NARR, c1=True)
extended_templates(t72, CULTURE)
compose_templates(t72, CULTURE, C=('C3',))
FESTIVALS = ['a harvest festival', 'the first rain after a long dry season', 'a wedding in a large family', 'the night before a new year celebration', 'a market day in a mountain village',
             'a religious festival you know well', 'a fishing community preparing for a storm', 'a city during a national holiday']
writing_templates(t72, [(f'Write a story set during {f}. Use details of the setting and the customs of the community to shape the characters’ choices and the events.',
                         'setting and customs integral to the plot; sensory detail; characters whose values reflect the culture; a clear conflict and resolution.',
                         f'Model approach: open with a sensory picture of {f}; introduce a character with a problem linked to the tradition; build to a moment where the custom matters; resolve with insight.') for f in FESTIVALS], 'narrative')

# ---------------------------------------------------------------- 7.3 narrative structure
STRUCT = ['foreshadowing', 'flashback', 'cliffhanger', 'circular structure', 'in medias res', 'linear chronological narrative']
STRUCT_SNIP = [
    ('Nobody noticed the small crack in the dam that morning. By the end of the week, everyone would wish they had.', 'foreshadowing', 'it hints at a coming disaster, creating suspense.'),
    ("'It's perfectly safe,' said Uncle Ravi, patting the old rope bridge. It creaked.", 'foreshadowing', 'the creak contradicts his words and warns of danger.'),
    ('She turned the key, the door swung open, and the face that looked back at her was her own.', 'cliffhanger', 'the chapter ends on a shocking, unexplained moment.'),
    ('The footsteps stopped right outside the tent.', 'cliffhanger', 'the section breaks off at the most tense point.'),
    ('As the plane lifted off, Mateo closed his eyes and was back in his grandfather\'s workshop, the smell of sawdust thick in the air.', 'flashback', 'the story moves back in time to an earlier memory.'),
    ('The photograph took her back to the summer the river flooded, when she was six and the whole street slept in the school hall.', 'flashback', 'a trigger object leads into an earlier event.'),
    ('The story ends where it began: at the bus stop, in the rain, with Ana waiting – but this time she is smiling.', 'circular structure', 'the ending returns to the opening setting, showing how the character has changed.'),
    ('The car was already sliding towards the edge when Dad shouted.', 'in medias res', 'the story starts at a dramatic moment without explanation.'),
    ('On Monday Kai found the map. On Tuesday he showed it to his sister. On Wednesday they set off.', 'linear chronological narrative', 'events are told in the order they happen.'),
    ('Little did they know that this would be the last summer they spent together.', 'foreshadowing', 'the narrator hints at a future loss.'),
    ('And then the lights went out.', 'cliffhanger', 'the short final line leaves the reader in suspense.'),
    ('Even now, forty years later, she cannot hear a train whistle without remembering the platform.', 'flashback', 'the present-day narrator is about to recall a past event.'),
]
TRAIN = Text('train', 'fiction', 'an extract from a story, ‘The Platform’', """
Even now, forty years later, Rosa cannot hear a train whistle without her stomach tightening. She is in her garden in
Lisbon, pruning roses, when the sound drifts up from the valley, and suddenly she is eight again, standing on a crowded
platform in the rain, holding her brother's hand so tightly that her fingers ache. 'Don't let go,' her mother had said.
'Whatever happens, don't let go.' The whistle had shrieked. The crowd had surged. And Rosa had let go. She sets the
shears down carefully on the path. Her hands, she notices, are shaking, just as they were then.""")
TRAIN.r('She is in her garden in Lisbon, pruning roses', 'Where is Rosa at the start of the extract?', 'In her garden in Lisbon', ['On a crowded platform', 'On a train', 'In the rain at a station', 'In her mother’s house'])
TRAIN.r('suddenly she is eight again', 'How old is Rosa in the memory?', 'Eight', ['Forty', 'Eighteen', 'Six', 'Twelve'])
TRAIN.i('when the sound drifts up from the valley, and suddenly she is eight again', 'How does the writer move from the present into the past?', 'The sound of the whistle triggers the memory; ‘suddenly’ shows the abrupt shift, and the tense stays present to make the memory vivid.',
        '1 mark: trigger (whistle); 1 mark: ‘suddenly’/abrupt transition')
TRAIN.i('The whistle had shrieked. The crowd had surged. And Rosa had let go.', 'Why does the writer use three short sentences here?', 'They speed up the pace and build to the shocking confession; ‘And Rosa had let go’ lands with great weight.',
        '1 mark: pace/tension; 1 mark: climax on the final sentence')
TRAIN.i('Her hands, she notices, are shaking, just as they were then.', 'Why is this an effective ending?', 'It returns to the present but links back to the past, showing the memory still affects her and leaving the reader wondering what happened to her brother.',
        '1 mark: links past and present; 1 mark: unresolved mystery/emotion')
TRAIN.f("'Don't let go,' her mother had said. 'Whatever happens, don't let go.'", 'repetition', "don't let go", 'the repeated warning stresses the mother’s fear and makes the later ‘Rosa had let go’ more painful.')
TRAIN.f('The whistle had shrieked. The crowd had surged. And Rosa had let go.', 'short sentence', 'And Rosa had let go.', 'the short final sentence is a devastating climax, delivered bluntly.', also=('repetition',))
TRAIN.x('How does the writer use structure to create tension and emotion in this extract?', 'Present-day frame; flashback triggered by sound; present tense inside memory; past perfect for key events; short sentences building to the confession; return to present with shaking hands; unanswered question.')
t73 = topic('Narrative structure: flashback, foreshadowing and cliffhangers', 'narrative structure', 'flashback foreshadowing cliffhangers')
t73.fixed('C1', (1, 2), ret_items([TRAIN]) + [
    ('What is foreshadowing?', 'A hint early in a story about something that will happen later', 'It builds suspense and makes the ending feel prepared.', ['A scene from the past', 'The final sentence of a chapter', 'A description of the weather']),
    ('What is a flashback?', 'A scene that interrupts the present story to show earlier events', 'Often triggered by a sound, smell or object.', ['A dream about the future', 'A sudden ending', 'A list of characters']),
    ('What is a cliffhanger?', 'An ending to a chapter or story at a moment of suspense', 'It makes the reader desperate to know what happens next.', ['A long description of a cliff', 'A happy ending', 'A summary of the plot']),
])
classify_templates(t73, STRUCT_SNIP, STRUCT, ['Which structural technique does this extract show? {q}', 'Read: {q} Which narrative device is the writer using?'],
                   C2frames=['This extract uses {label}: {q} Explain the effect on the reader.', 'Explain why a writer might use {label}, as in: {q}'],
                   C3frames=[('Identify the structural technique and analyse how it affects the reader’s response: {q}', lambda it: f'{cap(it[1])}: {it[2]}',
                              lambda it, m: f'{upto(m)}: 1 for {it[1]}; remaining marks for analysis of effect on suspense, pace or understanding.')])
t73.fixed('C2', (2, 3), inf_items([TRAIN]))
STORY_SITU = ['a school trip to a cave', 'a family moving to a new city', 'a football final', 'a camping trip in the mountains', 'an old shop about to close', 'a boat trip on a lake']


@t73.add('C3', (2, 3, 4, 5), 'short')
def t73_write(r, D):
    sit = r.choice(STORY_SITU)
    dev = r.choice(['foreshadowing', 'a cliffhanger', 'a flashback'])
    m = mk('C3', D)
    ex = {'foreshadowing': 'e.g. ‘The guide checked his torch twice before we went in, and I noticed he did not smile.’', 'a cliffhanger': 'e.g. ‘Behind us, very softly, the entrance began to close.’',
          'a flashback': 'e.g. ‘The smell of the cave took me back to the night of the storm, when Dad had carried me through the dark.’'}[dev]
    return {'stem': f'A story is about {sit}. Write two or three sentences that use {dev}, then explain how your sentences affect the reader.',
            'answer': f'Any sentences using {dev} appropriately, {ex} with an explanation of the effect (suspense, curiosity, deeper understanding of character).',
            'key': f'{upto(m)}: 1 for accurate use of {dev}; 1 for fitting the situation; remaining mark(s) for explaining the effect.'}


extended_templates(t73, [TRAIN])
writing_templates(t73, [(f'Write a story about {s} that uses {d}.', f'{d} used purposefully; clear time shifts signalled by tense or transitions; tension sustained.',
                         f'Model approach: decide where {d} fits (opening, middle or end); signal time shifts clearly; make sure the device changes how the reader understands events.')
                        for s in STORY_SITU for d in ('a flashback', 'foreshadowing and a cliffhanger ending', 'a circular structure')], 'narrative')

# ---------------------------------------------------------------- 7.4 writing a complete short story
STAGES = ['exposition (opening)', 'rising action', 'climax', 'falling action', 'resolution']
PLOTS = [
    ['Maya finds a stray kitten during a storm.', 'Her landlord forbids pets, so she hides it in her room.', 'The landlord hears mewing and bangs on the door.', 'Maya explains; the landlord’s face softens.', 'The kitten becomes the building’s shared pet.'],
    ['Arjun is chosen to read a poem at assembly.', 'He practises but grows more nervous each day.', 'On stage, his mind goes blank in front of the whole school.', 'A friend in the front row mouths the first line.', 'Arjun finishes the poem and is cheered.'],
    ['A fishing village hears that a storm is coming.', 'The fishermen argue about whether to go out one last time.', 'One boat is caught at sea as the waves rise.', 'The villagers light fires on the beach to guide it home.', 'The boat returns and the village is united.'],
    ['Lina inherits her grandmother’s old camera.', 'She develops the last film and finds photos of a place she does not know.', 'She travels to the place and meets an old man who recognises the photos.', 'He tells her the story of her grandmother’s youth.', 'Lina takes a new photo in the same spot.'],
]
t74 = topic('Writing a complete short story', 'writing a complete short story', 'controlled structure')
t74.fixed('C1', (1, 2), [
    ('Which is the correct order of a traditional story structure?', 'Exposition, rising action, climax, falling action, resolution', 'The ‘story mountain’ builds to a climax then resolves.',
     ['Climax, exposition, resolution, rising action', 'Resolution, climax, exposition, falling action', 'Rising action, resolution, climax, exposition']),
    ('What is the climax of a story?', 'The moment of greatest tension or the turning point', 'Everything builds to it; afterwards tension falls.', ['The first paragraph', 'The list of characters', 'The title']),
    ('Why should a short story usually have only a few characters?', 'There is not enough space to develop many characters well', 'Focus allows depth.', ['Short stories are not allowed many characters', 'Readers dislike characters', 'It makes the story longer']),
    ('What makes an effective ending to a short story?', 'One that resolves or deliberately leaves open the central conflict in a satisfying way', 'Endings should feel earned, not rushed (‘and then I woke up’ is weak).',
     ['Ending with ‘and it was all a dream’', 'Stopping suddenly in the middle of the action with no purpose', 'Introducing a new character in the last line']),
])


@t74.add('C1', (1, 2, 3))
def t74_stage(r, D):
    plot = r.choice(PLOTS)
    i = r.randrange(5)
    opts, ans = mcq(r, STAGES[i], [s for s in STAGES if s != STAGES[i]])
    return {'stem': f'In a story plan, this event appears: {Q(plot[i])} Which stage of the story structure is it most likely to be?', 'options': opts, 'answer': ans,
            'key': f'Plan: {" → ".join(plot)}. This event is the {STAGES[i]}.'}


@t74.add('C3', (2, 3, 4), 'short')
def t74_order(r, D):
    plot = r.choice(PLOTS)
    idx = list(range(5))
    while idx == sorted(idx):
        r.shuffle(idx)
    letters = 'ABCDE'
    jumbled = ' '.join(f'{letters[j]}: {plot[k]}' for j, k in enumerate(idx))
    order = ''.join(letters[idx.index(k)] for k in range(5))
    m = mk('C3', D)
    return {'stem': f'These events from a story plan are in the wrong order. {jumbled} Put them in the order of a story mountain and label each stage.',
            'answer': f'{order}: ' + '; '.join(f'{STAGES[k]} – {plot[k]}' for k in range(5)),
            'key': f'{upto(m)}: correct order {order}; labels exposition, rising action, climax, falling action, resolution.'}


t74.fixed('C2', (2, 3), [
    ('Explain why a writer of a short story should plan the ending before starting to write.', 'Knowing the ending lets the writer build towards it with foreshadowing and control the pace, so the ending feels earned rather than rushed.', '1 mark: control/foreshadowing; 1 mark: avoids a rushed or random ending.'),
    ('Explain why ‘and then I woke up and it was all a dream’ is usually a weak ending.', 'It cancels the events and the reader’s investment, avoiding a genuine resolution of the conflict.', '1 mark: cancels events/cheats reader; 1 mark: no real resolution.'),
    ('Explain how varying pace can improve a short story.', 'Slowing down at key moments (detail, short sentences) builds tension, while summarising less important events keeps the story moving.', '1 mark: slow key moments; 1 mark: summarise minor events.'),
    ('Explain why a short story usually focuses on one main conflict.', 'Limited length means one conflict can be developed fully, giving a clear shape and a satisfying resolution.', '1 mark: limited length; 1 mark: depth and clarity.'),
])


@t74.add('C2', (2, 3, 4), 'explain')
def t74_explain(r, D):
    plot = r.choice(PLOTS)
    return {'stem': f'A story plan reads: {" ".join(plot)} Explain why the third event works as the climax, and suggest how the writer could build tension before it.',
            'answer': f'{Q(plot[2])} is the moment of greatest tension and the turning point; tension could be built through short sentences, a ticking clock, foreshadowing or delaying the outcome.',
            'key': keypts('1 mark: identifies why it is the turning point/greatest tension; 1 mark: a valid technique for building tension; further mark for explanation.')}


STORY_TITLES = ['The Bridge', 'The Promise', 'A Door That Should Not Have Opened', 'The Last Match', 'The Message in the Bottle', 'Second Chances', 'The Long Way Home', 'The Storm',
                'The Secret Room', 'Night Shift', 'The Gift', 'Ice']
writing_templates(t74, [(f'Write a complete short story with the title {Q(ti)}. Plan a clear structure with a turning point and a satisfying ending.',
                         'clear exposition; rising tension; a well-placed climax; controlled resolution; limited characters well developed; varied pace.',
                         f'Model plan for {Q(ti)}: exposition (character, setting, want); rising action (obstacle, complications); climax (turning point); falling action; resolution that links back to the title.')
                        for ti in STORY_TITLES] +
                       [(f'Write a short story that begins with the sentence {Q(s)}', 'opening sentence integrated; clear story arc; tension; satisfying ending.', 'Model approach: use the sentence as an in medias res hook; reveal context through action; build to a climax; resolve or end with a deliberate twist.')
                        for s in ['Nobody had opened the gate for twenty years.', 'The phone rang at exactly midnight.', 'I should never have said yes.', 'The map was wrong.', 'It was the quietest the city had ever been.']], 'narrative')
CHAPTERS[7] = [t71, t72, t73, t74]


# =========================================================== Unit 8 Media, reports and journalism

FISHING = Text('fishing', 'news', 'a news report, ‘Fishing Crew Rescued After 40 Hours Adrift’', """
Five fishermen were rescued yesterday after spending more than 40 hours adrift in the Arabian Sea when their boat's
engine failed. The crew of the Noor, which set out from Muscat on Monday morning, lost radio contact shortly after
midday as strong winds pushed the vessel away from the coast. A coastguard helicopter spotted the boat at dawn on
Wednesday, about 80 kilometres offshore. All five men were taken to hospital suffering from dehydration but are said to
be in a stable condition. 'We had almost given up hope,' said the captain, Salim Al-Harthy, 47. 'When we heard the
helicopter, we cried like children.' The coastguard has urged fishermen to carry emergency beacons, which send a
satellite signal if a boat gets into difficulty.""")
FISHING.r('Five fishermen were rescued yesterday', 'How many fishermen were rescued?', 'Five', ['Four', 'Forty', 'Eight', 'Two'])
FISHING.r('A coastguard helicopter spotted the boat at dawn on Wednesday, about 80 kilometres offshore.', 'How far offshore was the boat found?', 'About 80 kilometres', ['About 40 kilometres', 'About 8 kilometres', 'About 800 kilometres', 'Close to the harbour'])
FISHING.r('All five men were taken to hospital suffering from dehydration', 'What were the men suffering from?', 'Dehydration', ['Broken bones', 'Sunburn only', 'Food poisoning', 'Hypothermia'])
FISHING.r('The coastguard has urged fishermen to carry emergency beacons', 'What does the coastguard advise fishermen to carry?', 'Emergency beacons', ['Extra fuel', 'Spare engines', 'More food', 'Life jackets only'])
FISHING.i('Five fishermen were rescued yesterday after spending more than 40 hours adrift in the Arabian Sea when their boat\'s engine failed.', 'Why is this an effective opening sentence for a news report?',
          'It gives the key facts at once (who, what, when, where, why) so readers grasp the story immediately; this is the ‘lead’ of an inverted pyramid.', '1 mark: key facts / 5 Ws; 1 mark: inverted pyramid/lead')
FISHING.i("'When we heard the helicopter, we cried like children.'", 'Why does the reporter include this quotation?', 'It adds human interest and emotion, showing how desperate the men were, and the eyewitness voice makes the report vivid and credible.',
          '1 mark: human interest/emotion; 1 mark: credibility/eyewitness')
FISHING.i('The coastguard has urged fishermen to carry emergency beacons', 'Why does the report end with this information?', 'Less important background and advice go at the end of an inverted-pyramid report; it also gives a practical message to readers.',
          '1 mark: least important at end; 1 mark: practical message/wider relevance')

ROOFTOP = Text('rooftop', 'feature', 'a feature article, ‘The Gardens in the Sky’', """
Seven floors above the traffic of downtown Singapore, Mei Lim is picking chillies. Around her, in raised beds made from
recycled crates, grow tomatoes, aubergines, lemongrass and a tangle of beans that has climbed halfway up the lift shaft.
'People think you need a field to grow food,' she laughs, wiping soil from her hands. 'You just need a roof and a bit of
stubbornness.' Mei is one of a growing number of city dwellers turning unused rooftops into farms. Supporters say the
gardens cool buildings, cut food miles and give neighbours a reason to talk to each other. Critics point out that they
will never feed a whole city. But up here, with bees drifting between the flowers and the city humming below, it is hard
not to feel that something important is taking root.""")
ROOFTOP.r('Seven floors above the traffic of downtown Singapore', 'Where is Mei Lim’s garden?', 'On a roof seven floors above downtown Singapore', ['In a field outside the city', 'In a school playground', 'Inside a lift shaft', 'On a farm in the countryside'])
ROOFTOP.r('in raised beds made from recycled crates', 'What are the raised beds made from?', 'Recycled crates', ['Old tyres', 'Concrete blocks', 'Plastic bottles', 'Glass windows'])
ROOFTOP.r('Critics point out that they will never feed a whole city.', 'What criticism of rooftop gardens is mentioned?', 'They will never feed a whole city', ['They are too noisy', 'They attract pests', 'They damage buildings', 'They are illegal'])
ROOFTOP.i('Seven floors above the traffic of downtown Singapore, Mei Lim is picking chillies.', 'Why does the writer open with this scene rather than with facts?',
          'A vivid present-tense scene with a real person draws the reader in, typical of a feature article, before the wider topic is explained.', '1 mark: engages/human interest; 1 mark: feature article style (scene-setting, present tense)')
ROOFTOP.i('Supporters say the gardens cool buildings, cut food miles and give neighbours a reason to talk to each other. Critics point out that they will never feed a whole city.', 'How does the writer show balance here?',
          'Benefits from supporters are followed by a criticism, so both views are presented before the writer’s own closing judgement.', '1 mark: both sides; 1 mark: reference to ‘Supporters say’/‘Critics point out’')
ROOFTOP.f('it is hard not to feel that something important is taking root', 'pun', 'taking root', 'the gardening phrase also means an idea is becoming established, giving a witty, optimistic ending.', also=('metaphor',))
ROOFTOP.f("'You just need a roof and a bit of stubbornness.'", 'colloquial language', 'a bit of stubbornness', 'the casual, humorous quotation gives Mei a likeable voice and makes the article personal.')
ROOFTOP.f('with bees drifting between the flowers and the city humming below', 'contrast', 'the city humming below', 'the peaceful garden is set against the busy city, emphasising the calm the gardens bring.', also=('personification', 'onomatopoeia'))

FILTER = Text('filter', 'news', 'a news report, ‘Student’s Microplastic Filter Wins Top Prize’', """
A 15-year-old from Nairobi has won first prize at an international young scientists' competition for a low-cost filter
that traps microplastics in washing-machine water. Wanjiru Kamau's device, built from recycled bottles and layers of
cotton mesh, captured up to 80 per cent of plastic fibres in tests at her school laboratory. Tiny fibres shed from
synthetic clothes are among the most common forms of plastic pollution in rivers and oceans. 'I kept seeing the river
near my home getting dirtier,' Wanjiru said. 'I wanted to stop the problem before it reached the water.' The judges
praised the invention as 'simple, cheap and genuinely useful'. Wanjiru will receive $5,000 towards her studies and plans
to share the design online so that other schools can build their own.""")
FILTER.r('A 15-year-old from Nairobi', 'Where is Wanjiru from?', 'Nairobi', ['Lagos', 'Accra', 'Kampala', 'Cape Town'])
FILTER.r('captured up to 80 per cent of plastic fibres', 'What proportion of plastic fibres did the filter capture in tests?', 'Up to 80 per cent', ['Up to 15 per cent', 'Exactly half', 'All of them', 'Up to 50 per cent'])
FILTER.r('Wanjiru will receive $5,000 towards her studies', 'What prize money will Wanjiru receive?', '$5,000', ['$500', '$15,000', '$80', '$50,000'])
FILTER.i("'I kept seeing the river near my home getting dirtier,' Wanjiru said.", 'Why does the reporter include Wanjiru’s own words?', 'Her quotation explains her motivation in a personal voice, making readers admire her and connect with the story.',
         '1 mark: motivation/personal voice; 1 mark: effect on reader (admiration, human interest)')
FILTER.i('Tiny fibres shed from synthetic clothes are among the most common forms of plastic pollution in rivers and oceans.', 'What is the purpose of this sentence in the report?', 'It gives background so the reader understands why the invention matters.',
         '1 mark: background/context; 1 mark: importance of invention')
MEDIA = [FISHING, ROOFTOP, FILTER]

# ---------------------------------------------------------------- 8.1 reports and features
NEWS_TERMS = ['headline', 'lead (opening paragraph)', 'byline', 'caption', 'inverted pyramid', 'quotation', 'subheading']
NEWS_DEF = [
    ('The line in large type at the top of a newspaper story that sums it up', 'headline'), ('The opening paragraph that gives the key facts of the story', 'lead (opening paragraph)'),
    ('The line that gives the writer’s name', 'byline'), ('The short text that explains a photograph', 'caption'),
    ('The structure that puts the most important information first and the least important last', 'inverted pyramid'),
    ('A witness’s or expert’s exact words', 'quotation'), ('A short heading that breaks up a long article', 'subheading'),
]
t81 = topic('Newspaper reports and feature articles', 'newspaper reports and feature articles', 'language and layout')
t81.fixed('C1', (1, 2), ret_items(MEDIA) + [
    ('What is the main difference between a news report and a feature article?', 'A news report gives the facts of a recent event; a feature explores a topic in more depth, often with a personal angle', 'Features are longer, more descriptive and may include opinion.',
     ['A feature article is always shorter', 'A news report always includes the writer’s opinion', 'There is no difference']),
    ('In which person and tense are news reports usually written?', 'the third person and the past tense', 'E.g. ‘Five fishermen were rescued yesterday’.', ['the first person and the future tense', 'the second person', 'rhyming verse']),
    ('Which questions should the lead of a news report answer?', 'Who, what, where, when and why', 'The ‘5 Ws’ (and sometimes how).', ['Only who and when', 'What the reader thinks', 'How long the article is']),
])


@t81.add('C1', (1, 2, 3))
def t81_term(r, D):
    d, term = r.choice(NEWS_DEF)
    opts, ans = mcq(r, term, [x for x in NEWS_TERMS if x != term])
    return {'stem': f'What is the name for this feature of a newspaper? {d}.', 'options': opts, 'answer': ans, 'key': f'{cap(term)}: {d.lower()}.'}


t81.fixed('C2', (2, 3), inf_items(MEDIA))


@t81.add('C3', (2, 3, 4, 5), 'explain')
def t81_compare(r, D):
    m = mk('C3', D)
    A = r.choice([FISHING, FILTER])
    return {'stem': f'Text A is {A.label}: {Q(A.text)} Text B is {ROOFTOP.label}: {Q(ROOFTOP.text)} Explain how Text A shows the features of a news report and Text B the features of a feature article.',
            'answer': 'Text A: lead with 5 Ws; past tense; third person; facts and figures; quotations; inverted pyramid with background last. Text B: present-tense scene-setting opening; personal angle (Mei); descriptive detail; quotations for personality; both sides discussed; reflective, witty ending (pun).',
            'key': f'{upto(m)}: 1 per valid feature with evidence, from both texts; credit comparison of purpose (inform quickly vs explore and engage).'}


compose_templates(t81, MEDIA, C=('C4',))
NEWS_SNIP = [
    ('Five fishermen were rescued yesterday after spending more than 40 hours adrift in the Arabian Sea when their boat\'s engine failed.', 'lead (opening paragraph)', 'it packs who, what, when, where and why into one sentence.'),
    ("'We had almost given up hope,' said the captain, Salim Al-Harthy, 47.", 'quotation', 'an eyewitness’s exact words with name and age add credibility.'),
    ('The coastguard has urged fishermen to carry emergency beacons, which send a satellite signal if a boat gets into difficulty.', 'inverted pyramid', 'background advice comes last because it is least essential.'),
    ('Seven floors above the traffic of downtown Singapore, Mei Lim is picking chillies.', 'lead (opening paragraph)', 'a feature lead sets a scene in the present tense to draw readers in.'),
    ("The judges praised the invention as 'simple, cheap and genuinely useful'.", 'quotation', 'quoting the judges gives authority to the praise.'),
    ('Tiny fibres shed from synthetic clothes are among the most common forms of plastic pollution in rivers and oceans.', 'inverted pyramid', 'context is placed after the main facts.'),
    ('STUDENT’S MICROPLASTIC FILTER WINS TOP PRIZE', 'headline', 'a short, bold summary of the story in present tense.'),
    ('Photo: Wanjiru Kamau with her filter in the school laboratory.', 'caption', 'it explains what the photograph shows.'),
    ('By Grace Mensah, Science Correspondent', 'byline', 'it names the journalist and their role.'),
]
classify_templates(t81, NEWS_SNIP, NEWS_TERMS, ['Which feature of a newspaper article is this? {q}'],
                   C3frames=[('Identify the feature of a newspaper text shown here, explain its purpose, and write your own example of the same feature for a story about a school sports day: {q}',
                              lambda it: f'{cap(it[1])}: {it[2]} Own example: any accurate {it[1]} about a sports day.',
                              lambda it, m: f'{upto(m)}: 1 for {it[1]}; 1 for purpose; remaining mark(s) for an accurate original example.')])

# ---------------------------------------------------------------- 8.2 language and structure to influence
HEADLINES = [
    ('ROOF-TOP OF THE CROPS', 'pun', 'a play on ‘top of the crops/pops’ makes the headline witty and memorable.'),
    ('Heatwave Horror as Hospitals Fill', 'alliteration', 'the repeated ‘h’ makes it punchy and dramatic.'),
    ('SAVED!', 'short sentence', 'the single exclamatory word gives instant relief and excitement.'),
    ('Is This the End for Our High Street?', 'rhetorical question', 'it involves the reader and suggests a worrying answer.'),
    ('Tiny Hands, Giant Hearts: Pupils Raise $10,000', 'contrast', 'opposites (tiny/giant) highlight the achievement.'),
    ('Fury Over Bus Fare Hike', 'emotive language', '‘Fury’ suggests strong public anger and grabs attention.'),
    ('Teen Inventor Cleans Up', 'pun', '‘cleans up’ means both cleaning water and winning prizes.'),
    ('Record-Breaking Rain Brings City to Standstill', 'hyperbole', '‘standstill’ exaggerates disruption for drama.'),
    ('Seven Seconds That Saved a Life', 'alliteration', 'the ‘s’ sounds create a dramatic rhythm and focus on the short time.'),
    ('Who Will Pay for the Flood Damage?', 'rhetorical question', 'it raises an issue the article will explore and implies blame.'),
]
t82 = topic('How writers use language and structure to influence readers', 'analysing how writers use language and structure to influence readers', 'influence readers')
t82.fixed('C1', (1, 2), [
    ('Why do newspapers often use puns in headlines?', 'To make the headline witty and memorable and attract readers', 'Puns entertain and catch the eye.', ['To make the facts clearer', 'Because puns are required by law', 'To hide the topic']),
    ('A writer places a sad eyewitness quotation at the very end of an article. What is the most likely purpose?', 'To leave the reader with a strong emotional impression', 'Endings linger; structure shapes response.', ['To give the key facts first', 'To add a statistic', 'To fill space']),
    ('Which structural choice most influences what readers think is important?', 'The order in which information is presented', 'Writers put what they want emphasised first or last.', ['The font size of page numbers', 'The length of the byline', 'The paper colour']),
])
classify_templates(t82, HEADLINES, ['pun', 'alliteration', 'short sentence', 'rhetorical question', 'contrast', 'emotive language', 'hyperbole'],
                   ['Which technique is used in this newspaper headline? {q}', 'A newspaper uses the headline {q} Which technique does it use?'],
                   C2frames=['The headline {q} uses {label}. Explain how it is designed to influence readers.'],
                   C3frames=[('Analyse how this headline tries to attract and influence readers: {q} Then write an alternative headline for the same story using a different technique.',
                              lambda it: f'{cap(it[1])}: {it[2]} Alternative: any accurate headline using a different technique (e.g. a question, alliteration or a pun).',
                              lambda it, m: f'{upto(m)}: 1 for {it[1]}; 1 for effect; remaining mark(s) for an effective alternative using a named technique.')])
feature_templates(t82, ROOFTOP.feats + BOTTLES.feats[:3] + SKATE.feats[:2], PERSUADE + ['pun', 'colloquial language', 'contrast'], c1=False)
STRUCT_MEDIA = [
    (FISHING, 'Explain how the reporter has ordered the information, and why.', 'Inverted pyramid: key facts in the lead; then details of the incident; then the rescue and condition; then an emotional quotation; finally background advice. This lets readers get the essentials quickly and ends with relevance.'),
    (ROOFTOP, 'Explain how the writer structures the article to engage and influence readers.', 'Opens with a vivid scene and a person; moves to wider trend; balances supporters and critics; returns to the rooftop scene for a positive, punning ending that leaves readers sympathetic.'),
    (FILTER, 'Explain how the order of information makes readers admire Wanjiru.', 'Achievement first; details of the invention and impressive figure (80%); background on why it matters; her personal motive in her own words; judges’ praise; generous plan to share the design last.'),
]


@t82.add('C3', (3, 4, 5), 'explain')
def t82_struct(r, D):
    T, q, a = r.choice(STRUCT_MEDIA)
    m = mk('C3', D)
    return {'stem': f'Read {T.label}: {Q(T.text)} {q}', 'answer': a, 'key': f'{upto(m)}: 1 per valid structural point (opening, order, placement of quotation, ending) linked to its effect on readers.'}


@t82.add('C4', (2, 3, 4, 5), 'long')
def t82_ext(r, D):
    T = r.choice([ROOFTOP, FILTER, FISHING, SKATE, BOTTLES])
    m = mk('C4', D, 'long')
    task = r.choice(['How does the writer use language and structure to influence the reader’s view of the people and events?', 'How does the writer try to shape the reader’s response? Consider word choice, quotation and the order of information.'])
    ind = 'Word choice and connotations; use and placement of quotations; facts and figures; opening and ending; balance or bias; overall effect on readers’ attitudes.'
    return {'stem': f'Read {T.label}: {Q(T.text)} {task}', 'answer': ind, 'key': reading_key(m, ind)}

# ---------------------------------------------------------------- 8.3 writing a news report
FACTSETS = [
    ('local students', 'Notes: Saturday; Riverside School robotics team (4 students, aged 13–14); won national schools robotics final in Kuala Lumpur; robot sorts recycling; beat 32 teams; captain Aisha Rahman: “We failed three times before it worked”; prize: trip to world championships in Tokyo.'),
    ('residents of the town', 'Notes: Tuesday night; storm; 120 mm rain in 6 hours; River Kalu burst banks; 40 homes flooded in Lower Town; no injuries; school used as shelter; council leader: “Our volunteers worked all night”; clean-up starts Thursday; flood barrier plan delayed since 2019.'),
    ('readers of a national newspaper', 'Notes: yesterday morning; elephant calf stuck in mud at waterhole, Amboseli; rangers and villagers worked 5 hours; used ropes and a tractor; calf reunited with herd; ranger Daniel Mutua: “The mother waited the whole time”; drought making waterholes muddy.'),
    ('young readers of a children’s news website', 'Notes: last week; 11-year-old Tomás Ruiz found fossil on beach near Lima; fossil is part of an ancient whale jawbone, around 10 million years old (museum estimate); now displayed at city museum; Tomás: “I thought it was a rock”; museum invites children to fossil-hunting day.'),
    ('parents and students at a school', 'Notes: Friday; school canteen trial; plastic cutlery replaced by metal; 2,000 plastic items saved per week; some students complain about queues; head of catering: “We are adding a second washing station”; full decision in June.'),
    ('residents of a city', 'Notes: Sunday; first car-free day in city centre; 10 a.m.–4 p.m.; streets used for cycling, music, food stalls; around 15,000 visitors; air pollution down 30% on the day (city monitoring); some shop owners report fewer sales; mayor plans monthly car-free days.'),
    ('readers of a local newspaper', 'Notes: Monday; fire at a bakery on Market Street, 5 a.m.; baker Mr Osei escaped unharmed; neighbours raised $8,000 online in two days to rebuild; fire caused by an electrical fault; reopening planned in two months; Mr Osei: “I have never felt so loved by this street.”'),
    ('students in a school magazine', 'Notes: last month; Year 9 student Leila Haddad, 14, cycled 300 km in 5 days for a children’s hospital; raised $3,200; trained for 6 months; accompanied by her uncle; Leila: “Day three, in the rain, was the hardest”; planning a sponsored swim next.'),
]
t83 = topic('Writing a news report or article for a specified audience', 'writing a news report or article', 'specified audience')
t83.fixed('C1', (1, 2), [
    ('Which is the best opening sentence for a news report?', 'Forty homes were flooded in Lower Town on Tuesday night after the River Kalu burst its banks.', 'It gives who/what/where/when/why concisely.',
     ['I want to tell you about a really bad storm.', 'Have you ever seen a flood? It is scary.', 'Once upon a time there was a river.']),
    ('Why do reporters include quotations from witnesses?', 'To add credibility and human interest', 'Quotes give real voices and evidence.', ['To give their own opinion', 'To make the report rhyme', 'To avoid giving facts']),
    ('How should a report for young children differ from one for adults?', 'Simpler vocabulary, shorter sentences and explanations of difficult ideas', 'Audience shapes language and detail.', ['It should contain no facts', 'It should be longer', 'It should use more technical terms']),
])
t83.fixed('C2', (2, 3), [
    ('Explain why a news reporter should avoid using ‘I’ and personal opinions.', 'Reports aim to be objective and trustworthy; personal opinions would make the report biased.', '1 mark: objectivity; 1 mark: trust/bias.'),
    ('Explain why the least important information goes at the end of a news report.', 'Readers may stop early, and editors can cut from the end without losing key facts (inverted pyramid).', '1 mark: readers skim; 1 mark: editing/inverted pyramid.'),
    ('Explain how a headline should be adapted for a children’s news website.', 'It should be clear, simple and engaging (perhaps playful), avoiding frightening or complex language.', '1 mark: simplicity/clarity; 1 mark: tone suited to children.'),
])


@t83.add('C3', (2, 3, 4, 5), 'short')
def t83_lead(r, D):
    aud, notes = r.choice(FACTSETS)
    m = mk('C3', D)
    return {'stem': f'Use these notes to write a headline and an opening paragraph (lead) for a news report aimed at {aud}. {notes}',
            'answer': 'Model: a short, striking headline; a lead of one or two sentences answering who, what, where, when and why, in the past tense and third person, with language suited to the audience.',
            'key': f'{upto(m)}: 1 for an effective headline; 1–2 for covering the 5 Ws accurately; 1 for register suited to {aud}.'}


@t83.add('C2', (1, 2, 3), 'short')
def t83_quote(r, D):
    aud, notes = r.choice(FACTSETS)
    q = re.findall(r'“([^”]+)”', notes)
    return {'stem': f'A reporter is writing for {aud} from these notes: {notes} Which piece of information would you put in the final paragraph, and why?',
            'answer': 'The least important or background information (e.g. future plans or wider context) goes last, following the inverted pyramid; ' + (f'the quotation “{q[0]}” could go near the end for human interest.' if q else ''),
            'key': keypts('1 mark: sensible choice of background/future information; 1 mark: reason linked to the inverted pyramid.')}


@t83.add('C4', (2, 3, 4, 5), 'long')
def t83_report(r, D):
    aud, notes = r.choice(FACTSETS)
    form = r.choice(['a news report', 'a news report with a short eyewitness section', 'an online news article with a headline and a subheading'])
    m = mk('C4', D, 'long')
    return {'stem': f'Write {form} for {aud} using these notes. You may add realistic details. {notes} Write about {WORDS.get(D, "250–350")} words.',
            'answer': 'Model structure: headline; lead with 5 Ws; details in order of importance; quotation(s) integrated with reporting verbs; background and next steps last; objective tone adapted to the audience.',
            'key': levels_key(m, 'report', f'all key facts from the notes; correct order; quotation punctuated; register suited to {aud}.')}

# ---------------------------------------------------------------- 8.4 group discussion and presentations
TRANSCRIPTS = [
    ('Um, so, my presentation is about, um, recycling. Recycling is good. It is good because, um, it is good for the planet. That is it.',
     'Weaknesses: fillers (um), no clear structure, repetition of ‘good’, no evidence, abrupt ending. Strengths: topic is stated.', 'Plan a hook, three points with evidence and a conclusion; replace fillers with pauses; vary vocabulary.'),
    ('Good morning. Imagine a city with no cars. Today I will give you three reasons why our town should try a car-free Sunday: cleaner air, safer streets and stronger communities. First, cleaner air…',
     'Strengths: greeting, hook, clear signposted structure, rule of three. Possible weakness: needs evidence for each point.', 'Add a statistic or example for each reason and finish with a call to action.'),
    ('As you can see on this slide, which has all my notes on it, the… [reads the slide aloud for two minutes without looking up]',
     'Weaknesses: reading from slides, no eye contact, overloaded slide. Strength: visual aid used.', 'Use slides with key words or images only; speak to the audience; practise so notes are prompts.'),
    ('Thank you, Mateo. I agree with your point about safety, but I wonder whether the cost might be a problem. Ines, what do you think?',
     'Strengths: acknowledges the previous speaker, builds on the idea, raises a counter-point politely, invites others to speak.', 'A model of good discussion; could add evidence about the cost.'),
    ('No, that is wrong. My idea is better. We should just do my plan.',
     'Weaknesses: dismissive, gives no reasons, does not listen or build on others’ ideas.', 'Acknowledge others’ points, give reasons, and suggest compromise (‘I see your point, but…’).'),
    ('I’m going to talk really fast because there’s loads to get through, so, yeah, basically sharks are amazing and also they’re not dangerous and also they’re dying out and—',
     'Weaknesses: rushed pace, informal register (loads, yeah, basically), points crammed together without development or evidence. Strength: enthusiasm.', 'Slow down; choose two or three points; use signposts and evidence; adopt a more formal register.'),
    ('Can I just come in there? Sofia, you said the trip is too expensive. Could we ask local businesses to sponsor it? That might solve the problem.',
     'Strengths: polite interruption, summarises another speaker’s point accurately, offers a constructive solution as a question.', 'A good model of collaborative discussion; could check whether others agree.'),
    ('[Speaks very quietly, looking at the floor] My talk is about volcanoes. Volcanoes erupt when pressure builds up under the ground.',
     'Weaknesses: poor projection and no eye contact, so the audience may lose interest. Strength: accurate, clear content.', 'Project the voice, look up at the audience, open with a hook such as a striking image or fact.'),
    ('So to sum up: the quiet room would cost almost nothing, it would help students who feel stressed, and the empty music store is ready now. Please vote yes. Thank you.',
     'Strengths: clear summary, rule of three, call to action, polite close.', 'A strong ending; could briefly remind the audience of the strongest piece of evidence.'),
]
ROLES = [('chair', 'keeps the discussion on track, invites people to speak and manages time'), ('note-taker', 'records the main points and decisions'),
         ('summariser', 'sums up the points made so far'), ('challenger', 'questions ideas and asks for evidence'), ('encourager', 'invites quieter members to contribute')]
t84 = topic('Group discussion and evaluating spoken presentations', 'group discussion', 'evaluating spoken presentations')
t84.fixed('C1', (1, 2), [
    ('Which phrase is best for building on someone else’s idea in a discussion?', '‘Building on what Priya said…’', 'It acknowledges and develops a previous contribution.', ['‘That is wrong.’', '‘Anyway, my idea…’', '‘Whatever.’']),
    ('What is a filler in spoken English?', 'A sound or word like ‘um’ or ‘like’ used while thinking', 'Too many fillers weaken a presentation.', ['A visual aid', 'A key point', 'A rhetorical question']),
    ('Why is eye contact important in a presentation?', 'It engages the audience and makes the speaker seem confident', 'Looking at the audience builds connection.', ['It makes the talk shorter', 'It is needed to read slides', 'It is not important']),
    ('What does ‘active listening’ involve?', 'Paying close attention, responding to and asking questions about what others say', 'Active listeners build on and question ideas.', ['Waiting silently for your turn without listening', 'Talking over others', 'Writing your own speech']),
])


@t84.add('C1', (1, 2, 3))
def t84_role(r, D):
    role, what = r.choice(ROLES)
    opts, ans = mcq(r, role, [x for x, _ in ROLES if x != role])
    return {'stem': f'In a group discussion, which role {what}?', 'options': opts, 'answer': ans, 'key': f'The {role} {what}.'}


@t84.add('C2', (2, 3, 4), 'explain')
def t84_eval(r, D):
    tr, ev, adv = r.choice(TRANSCRIPTS)
    m = mk('C2', D)
    return {'stem': f'Read this transcript from a student’s spoken contribution: {Q(tr)} Evaluate one strength or weakness of this contribution and explain its effect on listeners.',
            'answer': ev, 'key': f'{upto(m)}: 1 for an accurate strength/weakness; 1 for its effect on listeners; a further mark for supporting reference.'}


@t84.add('C3', (2, 3, 4, 5), 'explain')
def t84_feedback(r, D):
    tr, ev, adv = r.choice(TRANSCRIPTS)
    m = mk('C3', D)
    return {'stem': f'Read this transcript: {Q(tr)} Write feedback for the speaker giving one strength, one weakness and two specific improvements, with reasons.',
            'answer': f'{ev} Improvements: {adv}', 'key': f'{upto(m)}: valid strength; valid weakness; two specific, practical improvements; reasons linked to the audience.'}


TALKS = ['why your school should have a longer lunch break', 'a hobby you think everyone should try', 'a person from history you admire', 'how to reduce waste at home',
         'why learning a second language matters', 'the best place you have ever visited', 'why reading for pleasure is important', 'a technology that has changed the way we live']
writing_templates(t84, [(f'Write the script of a two-minute presentation to your class about {tk}, then write a short reflection on how you would make it engaging when you speak.',
                         'script with greeting, hook, signposted points, evidence, conclusion; reflection on voice, pace, pauses, eye contact, visual aids.',
                         f'Model: hook (question or striking fact); three signposted points about {tk}; conclusion with call to action; reflection on delivery (pauses, eye contact, key-word slides).') for tk in TALKS], 'speech')
CHAPTERS[8] = [t81, t82, t83, t84]


# =========================================================== Unit 9 Language, grammar and writing accuracy

# ---------------------------------------------------------------- 9.1 complex sentences
SUBORD = [
    ('Although the rain had stopped, the streets were still flooded.', 'Although the rain had stopped', ['the streets were still flooded', 'the streets', 'were still flooded']),
    ('The boy who found the wallet handed it to the police.', 'who found the wallet', ['The boy', 'handed it to the police', 'to the police']),
    ('We stayed indoors because the wind was too strong.', 'because the wind was too strong', ['We stayed indoors', 'the wind', 'was too strong']),
    ('When the bell rang, everyone rushed to the door.', 'When the bell rang', ['everyone rushed to the door', 'to the door', 'everyone rushed']),
    ('The museum, which opened in 1902, is closing for repairs.', 'which opened in 1902', ['The museum', 'is closing for repairs', 'for repairs']),
    ('If you finish early, you may read quietly.', 'If you finish early', ['you may read quietly', 'read quietly', 'you may']),
    ('She kept running until she reached the river.', 'until she reached the river', ['She kept running', 'the river', 'kept running']),
    ('Unless we leave now, we will miss the last bus.', 'Unless we leave now', ['we will miss the last bus', 'the last bus', 'we will miss']),
    ('The scientist explained that the ice was melting faster than expected.', 'that the ice was melting faster than expected', ['The scientist explained', 'faster than expected', 'the ice']),
    ('Since it was her birthday, Grace was allowed to choose the film.', 'Since it was her birthday', ['Grace was allowed to choose the film', 'to choose the film', 'Grace was allowed']),
]
SENT_TYPES = [
    ('The fox ran.', 'simple sentence', 'one main clause.'), ('The fox ran and the hens scattered.', 'compound sentence', 'two main clauses joined by ‘and’.'),
    ('As the fox ran, the hens scattered.', 'complex sentence', 'a main clause plus a subordinate clause (‘As the fox ran’).'), ('Silence.', 'minor sentence', 'no main verb; used for effect.'),
    ('The bus was late, so we walked.', 'compound sentence', 'two main clauses joined by ‘so’.'), ('Because the bus was late, we walked.', 'complex sentence', 'subordinate clause + main clause.'),
    ('Rain fell all night.', 'simple sentence', 'one main clause.'), ('What a day!', 'minor sentence', 'no main verb; exclamatory fragment.'),
    ('The girl, who had never seen snow, stared in wonder.', 'complex sentence', 'main clause with an embedded relative clause.'), ('I knocked, but nobody answered.', 'compound sentence', 'two main clauses joined by ‘but’.'),
    ('Nobody moved.', 'simple sentence', 'one main clause.'), ('Not again.', 'minor sentence', 'fragment without a main verb.'),
]
COMBINE = [
    ('The train was delayed.', 'We missed the start of the concert.', 'Because the train was delayed, we missed the start of the concert.'),
    ('Amara opened the box.', 'She gasped.', 'As soon as Amara opened the box, she gasped.'),
    ('The old man sat on the bench.', 'He fed the pigeons every morning.', 'The old man, who fed the pigeons every morning, sat on the bench.'),
    ('It was raining.', 'The match went ahead.', 'Although it was raining, the match went ahead.'),
    ('You water the plant.', 'It will die.', 'Unless you water the plant, it will die.'),
    ('The storm passed.', 'The villagers came out to inspect the damage.', 'After the storm passed, the villagers came out to inspect the damage.'),
    ('The library is very old.', 'It was built in 1850.', 'The library, which was built in 1850, is very old.'),
    ('Kenji practised every day.', 'He won the competition.', 'Since Kenji practised every day, he won the competition.'),
    ('The lights went out.', 'Everyone screamed.', 'When the lights went out, everyone screamed.'),
    ('She was exhausted.', 'She kept climbing.', 'Even though she was exhausted, she kept climbing.'),
]
OPEN_STYLES = [('a subordinate clause', 'e.g. ‘Although…’, ‘When…’, ‘Because…’'), ('an -ing verb (present participle)', 'e.g. ‘Shivering…’, ‘Glancing back…’'),
               ('an adverb', 'e.g. ‘Slowly,…’, ‘Reluctantly,…’'), ('a prepositional phrase', 'e.g. ‘Beneath the bridge,…’, ‘In the morning,…’')]
PLAIN = [
    ('The cat crept across the garden in the dark.', {'a subordinate clause': 'As darkness fell, the cat crept across the garden.', 'an -ing verb (present participle)': 'Creeping across the dark garden, the cat stayed low.',
                                                       'an adverb': 'Silently, the cat crept across the dark garden.', 'a prepositional phrase': 'In the dark, the cat crept across the garden.'}),
    ('Lena opened the letter with shaking hands.', {'a subordinate clause': 'Although her hands were shaking, Lena opened the letter.', 'an -ing verb (present participle)': 'Trembling, Lena opened the letter.',
                                                    'an adverb': 'Nervously, Lena opened the letter with shaking hands.', 'a prepositional phrase': 'With shaking hands, Lena opened the letter.'}),
    ('The boat drifted towards the rocks.', {'a subordinate clause': 'Because the engine had failed, the boat drifted towards the rocks.', 'an -ing verb (present participle)': 'Rocking wildly, the boat drifted towards the rocks.',
                                             'an adverb': 'Slowly, the boat drifted towards the rocks.', 'a prepositional phrase': 'Through the fog, the boat drifted towards the rocks.'}),
    ('The crowd cheered when the runner crossed the line.', {'a subordinate clause': 'When the runner crossed the line, the crowd cheered.', 'an -ing verb (present participle)': 'Leaping to their feet, the crowd cheered as the runner crossed the line.',
                                                              'an adverb': 'Joyfully, the crowd cheered as the runner crossed the line.', 'a prepositional phrase': 'At the finish line, the crowd cheered for the runner.'}),
    ('I waited outside the head teacher’s office.', {'a subordinate clause': 'While my heart thumped, I waited outside the head teacher’s office.', 'an -ing verb (present participle)': 'Fidgeting, I waited outside the head teacher’s office.',
                                                     'an adverb': 'Anxiously, I waited outside the head teacher’s office.', 'a prepositional phrase': 'On a hard wooden chair, I waited outside the head teacher’s office.'}),
    ('The market filled with noise at dawn.', {'a subordinate clause': 'As the sun rose, the market filled with noise.', 'an -ing verb (present participle)': 'Waking with the dawn, the market filled with noise.',
                                               'an adverb': 'Suddenly, the market filled with noise.', 'a prepositional phrase': 'At dawn, the market filled with noise.'}),
]
SENT_EFFECT = [
    ('The wind howled through the broken shutters, the floorboards creaked beneath her feet and somewhere below a door slammed again and again. Then silence.',
     'The long, listing complex sentence builds tension with accumulated sounds; the minor sentence ‘Then silence.’ stops it abruptly, creating shock and suspense.'),
    ('He ran. He did not look back. He did not stop.', 'The repeated short simple sentences create a fast, breathless pace and show his panic and determination.'),
    ('Although she had trained for months, had studied every rival and had slept well, Ama felt her legs tremble as she stepped onto the track.',
     'The fronted subordinate clause lists her preparation first, so the main clause about trembling legs comes as a contrast, showing nerves despite readiness.'),
    ('The house was empty. Dust lay thick on every surface, and the clocks had all stopped at the same minute.',
     'The short opening sentence states the fact bluntly; the longer compound sentence adds eerie detail, building atmosphere.'),
    ('Slowly, carefully, without making a sound, Tariq lifted the latch.', 'The fronted adverbs and phrase delay the main action, mirroring Tariq’s slow, careful movement and building suspense.'),
]
DESC_TOPICS = ['a railway station at night', 'a storm approaching a beach', 'a classroom just before an exam', 'a forest after snowfall', 'a busy kitchen during a festival', 'a city street at dawn']
t91 = topic('Complex sentences and varied sentence openings', 'complex sentences', 'subordinate clauses', 'varied sentence openings')
t91.fixed('C1', (1, 2), [
    ('What is a subordinate clause?', 'A clause that adds information but cannot stand alone as a sentence', 'E.g. ‘because it was raining’; it depends on a main clause.', ['A clause that makes sense on its own', 'A single word that describes a noun', 'A sentence with no verb']),
    ('Which word is a subordinating conjunction?', 'although', 'Subordinating conjunctions: although, because, when, if, unless, since, while.', ['and', 'but', 'or']),
    ('What is a relative clause?', 'A subordinate clause beginning with a word such as who, which or that', 'E.g. ‘The boy who found the wallet…’.', ['A clause about family members', 'A main clause after a comma', 'A list of adjectives']),
    ('When a sentence begins with a subordinate clause, what punctuation usually follows the clause?', 'A comma', 'E.g. ‘When the bell rang, everyone rushed out.’', ['A semicolon', 'A colon', 'No punctuation']),
])


@t91.add('C1', (1, 2, 3))
def t91_sub(r, D):
    s, sub, ds = r.choice(SUBORD)
    opts, ans = mcq(r, sub, ds)
    return {'stem': f'Which part of this sentence is the subordinate clause? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{Q(sub)} depends on the main clause and cannot stand alone.'}


classify_templates(t91, SENT_TYPES, ['simple sentence', 'compound sentence', 'complex sentence', 'minor sentence'], ['What type of sentence is this? {q}', 'Identify the sentence type: {q}'])
t91.fixed('C2', (2, 3, 4), [(f'Explain how the writer uses sentence structure for effect in this extract: {Q(a)}', b, '1 mark: identifies sentence type(s)/structure; 1 mark: effect on pace, tension or emphasis; a further mark for developed explanation with reference.') for a, b in SENT_EFFECT])


@t91.add('C3', (1, 2, 3, 4), 'short')
def t91_combine(r, D):
    a, b, model = r.choice(COMBINE)
    m = mk('C3', D)
    frame = r.choice(['Combine these two simple sentences into one complex sentence using a subordinating conjunction or a relative clause:', 'Join these sentences into a single complex sentence, punctuating it correctly:'])
    return {'stem': f'{frame} {Q(a)} {Q(b)}', 'answer': f'Model: {Q(model)}', 'key': f'{upto(m)}: subordinate clause correctly formed; logical link kept; comma placed correctly if the subordinate clause comes first.'}


@t91.add('C3', (1, 2, 3, 4, 5), 'short')
def t91_opener(r, D):
    s, opts = r.choice(PLAIN)
    style, eg = r.choice(OPEN_STYLES)
    m = mk('C3', D)
    return {'stem': f'Rewrite this sentence so that it begins with {style} ({eg}): {Q(s)}', 'answer': f'Model: {Q(opts[style])}',
            'key': f'{upto(m)}: begins with {style}; meaning kept; correctly punctuated (comma after the opening element).'}


writing_templates(t91, [(f'Write a descriptive paragraph about {d}. Use at least one simple, one compound, one complex and one minor sentence, and begin sentences in at least three different ways. Label the sentence types in brackets.',
                         'range of sentence types used deliberately; varied openings; punctuation of clauses accurate; description coherent.',
                         f'Model features for {d}: short simple sentence for impact; complex sentence with fronted subordinate clause; -ing opener; minor sentence at a key moment.') for d in DESC_TOPICS],
                  ('a wide, deliberate range of sentence structures and openings used for effect; all clauses correctly punctuated; coherent description', 'some variety of structures and openings; mostly accurate punctuation', 'mainly simple or repetitive structures; punctuation errors'))

# ---------------------------------------------------------------- 9.2 punctuation
PUNCT = [
    ('I have three favourite foods____ mangoes, rice and fried plantain.', 'colon', 'a colon introduces a list after a complete clause.'),
    ('The road was closed____ we had to find another way.', 'semicolon', 'a semicolon joins two closely related main clauses.'),
    ('There was only one thing left to do____ run.', 'colon', 'a colon introduces an explanation or dramatic reveal.'),
    ('My brother____ who is always late____ arrived on time for once.', 'commas', 'a pair of commas marks off extra information (a relative clause).'),
    ('The concert____ held in the park every summer____ attracts thousands of visitors.', 'commas', 'commas mark off the non-essential phrase.'),
    ('She opened the door____ and there, on the step, was the missing dog.', 'dash', 'a dash creates a pause for a dramatic reveal.'),
    ('The museum (____open Tuesday to Sunday____) is free to enter.', 'brackets', 'brackets enclose extra information that could be removed.'),
    ('I invited Ana, from Lisbon____ Kwame, from Accra____ and Mei, from Singapore.', 'semicolons', 'semicolons separate items in a list that already contain commas.'),
    ('It was not the cold that bothered him____ it was the silence.', 'semicolon', 'two balanced main clauses are joined by a semicolon.'),
    ('The recipe needs only one secret ingredient____ patience.', 'colon', 'a colon introduces a single item that explains the clause.'),
]
P_MARKS = ['colon', 'semicolon', 'commas', 'dash', 'brackets', 'semicolons', 'full stop']
P_EXPLAIN = [
    ('The results were clear: the new filter worked.', 'colon', 'introduces an explanation or result of the first clause.'),
    ('Some students walked; others took the bus.', 'semicolon', 'links two related main clauses and balances the contrast.'),
    ('We waited and waited – then the doors opened.', 'dash', 'creates a dramatic pause before the key moment.'),
    ('The capital city (which I had never visited) was larger than I expected.', 'brackets', 'add extra, non-essential information as an aside.'),
    ('You will need three things: a torch, a map and warm clothes.', 'colon', 'introduces the list that explains what ‘three things’ are, so the reader is prepared for the items that follow.'),
    ('The team – exhausted, muddy and triumphant – lifted the cup.', 'dash', 'a pair of dashes marks off a dramatic interruption.'),
    ('He had one ambition; she had none.', 'semicolon', 'joins two short contrasting main clauses.'),
    ('My aunt, a doctor in Nairobi, visits every summer.', 'commas', 'a pair of commas marks off a phrase giving extra information (apposition).'),
]
UNPUNCT = [
    ('when the bus finally arrived it was packed so we decided to walk', 'When the bus finally arrived, it was packed, so we decided to walk.'),
    ('my grandmother who is eighty still swims every morning', 'My grandmother, who is eighty, still swims every morning.'),
    ('there was only one way out the window', 'There was only one way out: the window.'),
    ('the sky darkened the birds fell silent', 'The sky darkened; the birds fell silent.'),
    ('i have visited three cities paris france cairo egypt and lima peru', 'I have visited three cities: Paris, France; Cairo, Egypt; and Lima, Peru.'),
    ('wheres my bag shouted leo i left it right here', '‘Where’s my bag?’ shouted Leo. ‘I left it right here.’'),
    ('the twins jake and ella are starting secondary school', 'The twins, Jake and Ella, are starting secondary school.'),
    ('its the dogs bowl not the cats', 'It’s the dog’s bowl, not the cat’s.'),
]
t92 = topic('Punctuation for effect and clarity', 'punctuation for effect and clarity', 'semicolons colons dashes brackets')
t92.fixed('C1', (1, 2), [
    ('Which punctuation mark can join two closely related main clauses without a conjunction?', 'A semicolon', 'E.g. ‘The road was closed; we turned back.’', ['A comma', 'A colon used before any clause', 'An apostrophe']),
    ('Which sentence uses a colon correctly?', 'She had one goal: to win.', 'A colon follows a complete clause and introduces an explanation.', ['She had: one goal to win.', 'She: had one goal to win.', 'She had one: goal to win.']),
    ('What is a comma splice?', 'Two main clauses wrongly joined with only a comma', 'E.g. ‘It was late, we went home.’ Fix with a full stop, semicolon or conjunction.', ['A list separated by commas', 'A comma before a quotation', 'A comma after a subordinate clause']),
    ('What are brackets used to do?', 'enclose extra information that the sentence would make sense without', 'E.g. ‘The museum (open daily) is free.’', ['show possession', 'end a question', 'introduce speech']),
])


@t92.add('C1', (1, 2, 3))
def t92_gap(r, D):
    s, mark, why = r.choice(PUNCT)
    opts, ans = mcq(r, mark, [m_ for m_ in P_MARKS if m_ != mark and not (mark.startswith('semicolon') and m_.startswith('semicolon'))])
    return {'stem': f'Which punctuation should go in the gap(s)? {Q(s)}', 'options': opts, 'answer': ans, 'key': f'{cap(mark)}: {why}'}


@t92.add('C2', (1, 2, 3, 4), 'explain')
def t92_explain(r, D):
    s, mark, why = r.choice(P_EXPLAIN)
    m = mk('C2', D)
    return {'stem': f'Explain why the writer has used a {mark if mark not in ("brackets", "commas") else "pair of " + mark} in this sentence: {Q(s)}', 'answer': f'The {mark} {why}',
            'key': f'{upto(m)}: 1 for the function of the {mark}; further mark(s) for the effect on clarity or emphasis.'}


@t92.add('C3', (1, 2, 3, 4), 'short')
def t92_punct(r, D):
    raw, fixed = r.choice(UNPUNCT)
    m = mk('C3', D)
    return {'stem': f'Rewrite this sentence with correct punctuation and capital letters: {Q(raw)}', 'answer': f'Model: {Q(fixed)}', 'key': f'{upto(m)}: capital letters; correct clause punctuation; apostrophes and speech marks where needed. Accept equivalent correct versions (e.g. a full stop instead of a semicolon).'}


PUNCT_TASKS = ['the moment a long-awaited parcel arrives', 'a crowded beach on a public holiday', 'a visit to a grandparent’s village', 'the minutes before a race', 'an unexpected snow day', 'a power cut during a family dinner']
writing_templates(t92, [(f'Write a paragraph about {p} that uses a semicolon, a colon, a dash and a pair of brackets correctly and for effect. Then explain why you used each one.',
                         'each mark used correctly and purposefully; explanation of each function; paragraph coherent.', f'Model: e.g. ‘The parcel had one word on it: FRAGILE.’ / ‘We waited; nobody spoke.’ / ‘Then – at last – the knock came.’ / ‘My aunt (who never sends anything) had sent it.’')
                        for p in PUNCT_TASKS],
                  ('all four marks used accurately and for clear effect; precise explanations; fluent paragraph', 'most marks used accurately; some explanation', 'marks used incorrectly or not at all; little explanation'))

# ---------------------------------------------------------------- 9.3 vocabulary and register
REGISTER = [
    ('Hey, can u send me the homework? Thx!', 'Could you please send me the homework? Thank you.'),
    ('The food at the event was well nice.', 'The food at the event was excellent.'),
    ('Loads of people turned up to the meeting.', 'A large number of people attended the meeting.'),
    ('We need to sort out the problem asap.', 'We need to resolve the problem as soon as possible.'),
    ('The new rules are rubbish and nobody likes them.', 'The new rules have been widely criticised.'),
    ('I reckon the council should do something about the potholes.', 'I believe the council should take action to repair the potholes.'),
    ('Kids get really stressed out before exams.', 'Many young people experience considerable stress before examinations.'),
    ('The trip got cancelled ’cos of the weather.', 'The trip was cancelled because of the weather.'),
]
FORMAL_W = [('assist', ['help out', 'give a hand', 'chip in']), ('purchase', ['buy', 'grab', 'pick up']), ('inform', ['tell', 'let know', 'fill in']), ('require', ['need', 'want', 'gotta have']),
            ('commence', ['start', 'kick off', 'get going']), ('sufficient', ['enough', 'plenty', 'loads']), ('approximately', ['about', 'roughly', 'more or less']), ('inquire', ['ask', 'check', 'find out']),
            ('attempt', ['try', 'have a go', 'give it a shot']), ('reside', ['live', 'stay', 'hang out'])]
PRECISE = [
    ('The dog went across the road.', 'went', ['darted', 'limped', 'trotted', 'slunk'], 'precise verbs show how the dog moved and suggest mood (fear, injury, confidence).'),
    ('She said she was sorry.', 'said', ['whispered', 'sobbed', 'muttered', 'admitted'], 'a precise speech verb shows how she spoke and her feelings.'),
    ('It was a nice day.', 'nice', ['glorious', 'crisp', 'balmy', 'golden'], 'a specific adjective creates a clear picture instead of a vague judgement.'),
    ('The old house was big.', 'big', ['vast', 'rambling', 'towering', 'sprawling'], 'a precise adjective suggests the shape and atmosphere of the house.'),
    ('He looked at the letter.', 'looked', ['glared', 'peered', 'glanced', 'stared'], 'the choice of verb reveals emotion and intensity.'),
    ('The crowd made a noise.', 'made a noise', ['roared', 'murmured', 'gasped', 'erupted'], 'a single vivid verb is more concise and shows the type of sound.'),
]
AUDIENCES = [('a formal email to a hotel manager', 'a text message to a friend'), ('a speech to parents at a prize-giving', 'a chat with classmates'), ('a letter of application for a volunteer post', 'a note to your sibling'),
             ('a report for the school governors', 'a post for the school social-media page')]
MESSAGES = ['you cannot attend an event you had agreed to go to', 'you want to complain about a delayed delivery', 'you are thanking someone for help with a project', 'you are asking for more time to finish a task']
t93 = topic('Choosing vocabulary and register for audience and purpose', 'choosing vocabulary and register', 'audience and purpose')
t93.fixed('C1', (1, 2), [
    ('What is register?', 'The level of formality of language chosen to suit audience and purpose', 'Formal vs informal register.', ['The volume of a speaker’s voice', 'A list of students in a class', 'The rhyme scheme of a poem']),
    ('Which feature is typical of formal writing?', 'Full forms such as ‘do not’ instead of ‘don’t’', 'Formal writing avoids contractions and slang.', ['Slang and abbreviations', 'Emojis', 'Very short exclamations']),
    ('What are connotations?', 'The ideas and feelings a word suggests beyond its literal meaning', 'E.g. ‘home’ suggests warmth and safety; ‘house’ is more neutral.', ['A word’s dictionary definition only', 'Words that sound the same', 'Words borrowed from another language']),
])


@t93.add('C1', (1, 2, 3))
def t93_formal(r, D):
    f, ds = r.choice(FORMAL_W)
    opts, ans = mcq(r, f, ds)
    return {'stem': 'Which word or phrase is most suitable for a formal letter?', 'options': opts, 'answer': ans, 'key': f'{Q(f)} is formal; the others are informal or colloquial.'}


@t93.add('C2', (1, 2, 3, 4), 'explain')
def t93_precise(r, D):
    s, w, opts, why = r.choice(PRECISE)
    a, b = r.sample(opts, 2)
    m = mk('C2', D)
    wd = 'words' if ' ' in w else 'word'
    if m == 1:
        return {'stem': f'In the sentence {Q(s)}, the {wd} {Q(w)} could be replaced by {Q(a)}. Explain how this choice changes the effect.',
                'answer': f'{Q(a)} gives a more specific picture than {Q(w)}; {why}', 'key': keypts(f'1 mark: a valid comment on the connotation or precision of {Q(a)}.')}
    return {'stem': f'In the sentence {Q(s)}, the {wd} {Q(w)} could be replaced by {Q(a)} or {Q(b)}. Explain how each choice changes the meaning or effect.',
            'answer': f'{Q(a)} and {Q(b)} each give a more specific picture than {Q(w)}; {why}', 'key': f'{upto(m)}: 1 for the connotation of {Q(a)}; 1 for {Q(b)}; further mark for comparing effects.'}


rewrite_templates(t93, [('Rewrite this sentence in a formal register.', a, f'Model: {Q(b)}', 'Award for removing slang/contractions/abbreviations, precise vocabulary and correct grammar.') for a, b in REGISTER],
                  ['{ins} {q}', 'This sentence will appear in a letter to a local councillor. {ins} {q}'])


@t93.add('C4', (2, 3, 4, 5), 'long')
def t93_two(r, D):
    formal, informal = r.choice(AUDIENCES)
    msg = r.choice(MESSAGES)
    m = mk('C4', D, 'long')
    return {'stem': f'Write two versions of a message in which {msg}: first {formal}, then {informal}. Then explain three differences in vocabulary and register between your versions. Write about {WORDS.get(D, "250–350")} words in total.',
            'answer': 'Model approach: formal version with appropriate greeting, full forms, polite modal verbs (could, would), precise vocabulary and sign-off; informal version with contractions, colloquial words and a friendly tone; commentary naming the differences.',
            'key': levels_key(m, ('both versions precisely suited to audience and purpose; commentary explains register choices perceptively', 'two recognisably different registers; some explanation', 'little difference in register; minimal explanation'),
                              'greetings and sign-offs; contractions; vocabulary choice; sentence length; politeness strategies.'), 'type': 'long'}


# ---------------------------------------------------------------- 9.4 spelling
MISSPELT = [('necessary', ['neccessary', 'necesary', 'neccesary']), ('separate', ['seperate', 'separat', 'seperete']), ('definitely', ['definately', 'definitly', 'defanitely']),
            ('accommodation', ['accomodation', 'acommodation', 'accommadation']), ('embarrass', ['embarass', 'embaras', 'enbarrass']), ('rhythm', ['rythm', 'rhythem', 'rythym']),
            ('conscience', ['concience', 'conscence', 'consciense']), ('environment', ['enviroment', 'enviorment', 'environmant']), ('beginning', ['begining', 'beggining', 'beginnig']),
            ('occurred', ['occured', 'ocurred', 'occurrd']), ('government', ['goverment', 'governmant', 'govermint']), ('immediately', ['immediatly', 'imediately', 'immediatley']),
            ('possession', ['posession', 'possesion', 'posesion']), ('achieve', ['acheive', 'achive', 'acheeve']), ('disappear', ['dissappear', 'disapear', 'dissapear']),
            ('recommend', ['reccomend', 'recomend', 'reccommend'])]
PREFIXES = [('un-', 'not', 'unhappy'), ('dis-', 'not / opposite of', 'disagree'), ('mis-', 'wrongly', 'misunderstand'), ('re-', 'again', 'rebuild'), ('pre-', 'before', 'preview'),
            ('sub-', 'under', 'submarine'), ('inter-', 'between', 'international'), ('trans-', 'across', 'transport'), ('anti-', 'against', 'antisocial'), ('bi-', 'two', 'bicycle')]
SUFFIX_RULES = [
    ('hope', '-ing', 'hoping', 'drop the final -e before a suffix beginning with a vowel'), ('care', '-ful', 'careful', 'keep the final -e before a suffix beginning with a consonant'),
    ('happy', '-ness', 'happiness', 'change -y to -i when a consonant comes before the -y'), ('begin', '-ing', 'beginning', 'double the final consonant after a short stressed vowel'),
    ('run', '-er', 'runner', 'double the final consonant after a single short vowel'), ('beauty', '-ful', 'beautiful', 'change -y to -i before the suffix'),
    ('enjoy', '-ment', 'enjoyment', 'keep the -y when a vowel comes before it'), ('admire', '-ation', 'admiration', 'drop the final -e before a vowel suffix'),
    ('refer', '-ed', 'referred', 'double the final r because the stress is on the last syllable'), ('travel', '-ing', 'travelling', 'in British spelling, double the final l after a single vowel'),
    ('argue', '-ment', 'argument', 'an exception: the e is dropped even though -ment begins with a consonant'), ('notice', '-able', 'noticeable', 'keep the e after c to keep the soft ‘s’ sound'),
]
FAMILIES = [('sign', ['signature', 'signal', 'design'], 'the silent g is sounded in signature and signal'), ('muscle', ['muscular'], 'the c is sounded in muscular'),
            ('bomb', ['bombard'], 'the b is sounded in bombard'), ('nation', ['national', 'nationality'], 'the root keeps its spelling though the vowel sound changes'),
            ('define', ['definite', 'definition'], 'remembering ‘define’ helps spell ‘definite’ with an i'), ('separate', ['separation'], 'remember ‘a rat’ in sep-a-rat-e'),
            ('compete', ['competition', 'competitive'], 'the root explains the i in competition'), ('medicine', ['medical', 'medicinal'], 'medical reminds you of the c in medicine')]
t94 = topic('Spelling strategies: prefixes, suffixes and word families', 'spelling strategies', 'prefixes suffixes word families')
t94.fixed('C1', (1, 2), [
    ('What is a prefix?', 'A group of letters added to the start of a word to change its meaning', 'E.g. un- + happy = unhappy.', ['Letters added to the end of a word', 'A word that sounds like another', 'A silent letter']),
    ('What is a word family?', 'A group of words that share the same root', 'E.g. sign, signal, signature.', ['Words that rhyme', 'Words with the same number of letters', 'Words with the same prefix only']),
    ('Which strategy helps you remember the spelling of ‘necessary’?', 'A mnemonic, such as ‘one collar, two sleeves’ (one c, two s)', 'Mnemonics link a tricky spelling to a memorable phrase.', ['Writing it as it sounds', 'Never using the word', 'Adding a double c']),
])


@t94.add('C1', (1, 2, 3))
def t94_spell(r, D):
    w, ws = r.choice(MISSPELT)
    opts, ans = mcq(r, w, ws)
    return {'stem': 'Which is the correct spelling?', 'options': opts, 'answer': ans, 'key': f'Correct: {w}.'}


@t94.add('C1', (1, 2, 3))
def t94_prefix(r, D):
    p, mean, ex = r.choice(PREFIXES)
    opts, ans = mcq(r, mean, [m_ for _, m_, _ in PREFIXES if m_ != mean])
    return {'stem': f'What does the prefix {Q(p)} mean, as in {Q(ex)}?', 'options': opts, 'answer': ans, 'key': f'{p} means {Q(mean)} ({ex}).'}


@t94.add('C2', (1, 2, 3, 4), 'explain')
def t94_rule(r, D):
    base, suf, res, rule = r.choice(SUFFIX_RULES)
    return {'stem': f'Add the suffix {Q(suf)} to {Q(base)} and explain the spelling rule you used.', 'answer': f'{res}: {rule}.', 'key': keypts(f'1 mark: correct spelling ({res}); 1 mark: rule explained ({rule}).')}


@t94.add('C3', (1, 2, 3, 4), 'short')
def t94_family(r, D):
    root, fam, tip = r.choice(FAMILIES)
    m = mk('C3', D)
    return {'stem': f'Write three words in the same word family as {Q(root)} and explain how knowing the family helps you spell a tricky word in it.',
            'answer': f'E.g. {", ".join(fam)}; {tip}.', 'key': f'{upto(m)}: 1 per correctly spelt family word (up to 3); 1 for explaining how the family helps spelling.'}


@t94.add('C3', (2, 3, 4, 5), 'short')
def t94_correct(r, D):
    picks = r.sample(MISSPELT, 4)
    wrong = [r.choice(ws) for _, ws in picks]
    sent = f'It was {wrong[0]} to arrive early, but we {r.choice(["could not", "did not"])} expect the {wrong[1]} to be so small. The guide said we would {wrong[2]} enjoy it, and nothing {wrong[3]} to change our minds.'
    m = mk('C3', D)
    return {'stem': f'Find and correct the spelling errors in this passage, and explain a strategy for remembering one of the words: {Q(sent)}',
            'answer': 'Corrections: ' + '; '.join(f'{w} → {c}' for w, (c, _) in zip(wrong, picks)), 'key': f'{upto(m)}: 1 per correction; 1 for a valid strategy (mnemonic, root word, syllables, rule).'}


@t94.add('C4', (2, 3, 4, 5), 'multi_step')
def t94_c4(r, D):
    a, b = r.sample(SUFFIX_RULES, 2)
    p = r.choice(PREFIXES)
    w, ws = r.choice(MISSPELT)
    root, fam, tip = r.choice(FAMILIES)
    parts = [
        lambda r: (f'Add {Q(a[1])} to {Q(a[0])} and {Q(b[1])} to {Q(b[0])}.', f'{a[2]}; {b[2]}', '1 mark each [2]'),
        lambda r: (f'Explain the spelling rule for {Q(a[2])}.', a[3], '1 mark rule [1]'),
        lambda r: (f'Use the prefix {Q(p[0])} to make two new words and give the meaning of each.', f'E.g. {p[2]} and another word with {p[0]}; meaning includes {Q(p[1])}.', '1 mark per word with meaning [2]'),
        lambda r: (f'A student writes {Q(r.choice(ws))}. Correct it and suggest a strategy to remember it.', f'{w}; any valid mnemonic or breaking the word into syllables.', '1 mark correction; 1 mark strategy [2]'),
        lambda r: (f'Write two words in the word family of {Q(root)} and explain how the family helps spelling.', f'{", ".join(fam[:2])}; {tip}.', '1 mark words; 1 mark explanation [2]'),
    ]
    return compose(r, 'Answer these spelling questions.', parts, k=(3, 4, 5), type_='multi_step')


# ---------------------------------------------------------------- 9.5 planning, proofreading and editing
PROOF = [
    ('Their was a loud noise outside, everyone ran to the window. We seen a lorry which had crashed into the lamppost.',
     'There was a loud noise outside, and everyone ran to the window. We saw a lorry that had crashed into the lamppost.', ['Their → There', 'comma splice fixed', 'seen → saw']),
    ('The team was very exited about the match. They had trained hard all week and they was ready.',
     'The team was very excited about the match. They had trained hard all week and they were ready.', ['exited → excited', 'they was → they were']),
    ('Me and my friend went to the libary to research are project on volcanoes.',
     'My friend and I went to the library to research our project on volcanoes.', ['Me and my friend → My friend and I', 'libary → library', 'are → our']),
    ('Its important to recycle because it reduces waste, saves energy, and helps the enviroment.',
     'It’s important to recycle because it reduces waste, saves energy and helps the environment.', ['Its → It’s', 'enviroment → environment', 'optional: no comma before ‘and’ in British style']),
    ('When I arrived at the station. The train had already left so I had to wait a hour.',
     'When I arrived at the station, the train had already left, so I had to wait an hour.', ['sentence fragment fixed', 'a hour → an hour', 'comma before so']),
    ('Each of the students have brought there own lunch.', 'Each of the students has brought their own lunch.', ['have → has (each is singular)', 'there → their']),
    ('I could of finished the race if I hadnt tripped over.', 'I could have finished the race if I hadn’t tripped over.', ['could of → could have', 'hadnt → hadn’t']),
    ('The book who I borrowed was more better than the film.', 'The book that I borrowed was better than the film.', ['who → that/which', 'more better → better']),
]
PLAN_TASKS = ['a story about a lost key', 'an article about saving water at school', 'a speech for a debate on school uniform', 'a description of a market at dusk', 'a letter of complaint about a broken product', 'a balanced argument about homework']
t95 = topic('Planning, proofreading and editing extended writing', 'planning proofreading and editing', 'extended writing')
t95.fixed('C1', (1, 2), [
    ('What is the main purpose of proofreading?', 'To find and correct errors in spelling, punctuation and grammar', 'Proofreading is a final accuracy check.', ['To plan the main ideas', 'To make the writing longer', 'To choose a title']),
    ('What is the difference between editing and proofreading?', 'Editing improves content, structure and style; proofreading corrects surface errors', 'Edit first (big changes), proofread last (small errors).', ['There is no difference', 'Proofreading changes the whole structure', 'Editing only checks spelling']),
    ('Which is a useful proofreading strategy?', 'Reading your work aloud slowly or reading it backwards sentence by sentence', 'Slowing down helps you see what you actually wrote.', ['Reading only the first line', 'Checking only the longest words', 'Skipping the final paragraph']),
    ('Why should you plan before extended writing?', 'To organise ideas into a clear structure before you start', 'A plan helps paragraphing and coherence.', ['To avoid using paragraphs', 'Because the plan is marked more than the writing', 'To make the writing shorter']),
    ('When should a new paragraph begin?', 'When there is a change of time, place, topic or speaker', 'TiPToP: time, place, topic, person.', ['After every sentence', 'Only at the end', 'Whenever a long word appears']),
])


@t95.add('C2', (1, 2, 3, 4), 'short')
def t95_find(r, D):
    bad, good, errs = r.choice(PROOF)
    m = mk('C2', D)
    return {'stem': f'Identify the errors in this sentence and explain how to correct {"one of them" if D <= 2 else "them"}: {Q(bad)}', 'answer': '; '.join(errs) + f'. Corrected: {Q(good)}',
            'key': f'{upto(m)}: 1 per error identified with a correct fix and reason.'}


@t95.add('C3', (1, 2, 3, 4, 5), 'short')
def t95_fix(r, D):
    a, b = r.sample(PROOF, 2)
    text = a[0] + ' ' + b[0] if D >= 3 else a[0]
    fixed = a[1] + (' ' + b[1] if D >= 3 else '')
    errs = a[2] + (b[2] if D >= 3 else [])
    m = mk('C3', D)
    return {'stem': f'Proofread and rewrite this draft, correcting all errors in spelling, punctuation and grammar: {Q(text)}', 'answer': f'Model: {Q(fixed)}', 'key': f'{upto(m)}: ' + '; '.join(errs) + '. Deduct for new errors.'}


@t95.add('C3', (2, 3, 4), 'short')
def t95_plan(r, D):
    task = r.choice(PLAN_TASKS)
    m = mk('C3', D)
    return {'stem': f'Write a paragraph-by-paragraph plan for {task}. Include the purpose of each paragraph and one key detail or piece of evidence for each.',
            'answer': 'Model: four to six paragraphs in a logical order (introduction/hook; development points; turning point or counter-argument; conclusion), each with a purpose and detail suited to the form.',
            'key': f'{upto(m)}: logical sequence; suitable opening and ending; each paragraph has a clear purpose; details relevant to the form and audience.'}


@t95.add('C4', (2, 3, 4, 5), 'long')
def t95_edit(r, D):
    task = r.choice(PLAN_TASKS)
    m = mk('C4', D, 'long')
    return {'stem': f'Plan and write {task}. Then proofread your work and list three corrections or improvements you made, explaining why each makes your writing better. Write about {WORDS.get(D, "250–350")} words.',
            'answer': 'Model approach: brief plan; full piece with clear paragraphs; a list of three specific edits (e.g. replacing a vague word, fixing a comma splice, reordering a paragraph) with reasons.',
            'key': levels_key(m, ('well-planned, coherent piece suited to form and audience; three precise edits with insightful reasons', 'clear piece with some planning evident; edits identified with some explanation', 'little evidence of planning; edits vague or missing'),
                              'planning; paragraphing (TiPToP); accuracy; reflective editing comments.'), 'type': 'long'}


CHAPTERS[9] = [t91, t92, t93, t94, t95]


def settle_fixed_marks(chapters):
    """Fixed C2 items whose key spells out marks ('1 mark: …; 1 mark: …') get a key sized to the
    marks the slot actually carries (pairs keep their own spelled-out keys and marks)."""
    for topics in chapters.values():
        for t in topics:
            for tp in t.templates:
                if tp.name != 'fixed' or tp.C != 'C2' or getattr(tp, '_settled', False):
                    continue

                def wrap(fn):
                    def g(r, D):
                        q = fn(r, D)
                        k = q.get('key', '') if q else ''
                        if q and 'marks' not in q and re.match(r'1 mark', k) and '[' not in k:
                            q = dict(q, key=keypts(k))
                        return q
                    return g
                tp.fn = wrap(tp.fn)
                tp._settled = True


settle_fixed_marks(CHAPTERS)
