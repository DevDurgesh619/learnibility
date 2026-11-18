"""Shared builders for the IB MYP Language and Literature (English) packs: ib-g8-english (MYP 3),
ib-g9-english (MYP 4) and ib-g10-english (MYP 5).

Kit(R) wraps one pack's Registry and passage library:
  K.P(...)              register an ORIGINAL study passage with its annotation (answers for every frame)
  K.pq(...)             passage-based question frames (stem = passage + frame; answer from the annotation)
  K.qa(...)             passage-specific comprehension / inference questions stored on the passage
  K.vocab(...)          language-in-context MCQs ("As used in the text, X most nearly means")
  K.dev_mcq / tone_mcq / kind_mcq   recognition MCQs on a passage
  K.para(...)           analytical paragraph / essay on the passage guiding question (criteria A-D)
  K.write(...)          directed writing in response to a passage (summary, reply, rewrite for a new audience)
  K.compare(...)        comparative analysis of two paired extracts (eAssessment Task 1 style)
  K.prompts(...)        creative writing from visual prompts described in words (eAssessment Task 2 style)
  K.mock_templates()    style-tagged templates for the MYP 5 eAssessment-style mock (t1a, t1b, t1c, t2a, t2b, t2c)
add_shared(K) registers the shared passage library (non-literary texts and some literary extracts, all original
and pitched at readers aged 13-16; the only quotations are brief public-domain lines, attributed).
"""
from __future__ import annotations

from _common import F, Registry, T, mcq, name  # noqa: F401

# ---------------------------------------------------------------------------------------------------------------
# MYP Language and literature assessment criteria (each 0-8 at full task scale)
# ---------------------------------------------------------------------------------------------------------------
CRIT_ALL = ('MYP criteria (each 0-8, scaled to this item). A Analysing: explains content, context, language, structure, '
            'technique and style and their effects; justifies opinions with examples and explanation, using terminology. '
            'B Organising: a clear, logical structure suited to the task; ideas linked with purpose; referencing conventions. '
            'C Producing text: insight, imagination and personal engagement; deliberate stylistic choices; relevant detail and '
            'examples. D Using language: varied, accurate vocabulary, sentence structures and forms of expression; appropriate '
            'register and style; accurate grammar, spelling and punctuation. 7-8 perceptive/excellent; 5-6 substantial; '
            '3-4 adequate; 1-2 limited.')
CRIT_AN = ('Mark mainly against criterion A (Analysing) and B (Organising). 7-8 equivalent: perceptive analysis of how specific '
           'choices create effects, well-chosen embedded evidence, sustained, logical structure; 5-6: substantial analysis with '
           'relevant evidence; 3-4: adequate, partly descriptive; 1-2: limited, mostly feature-spotting or retelling.')
CRIT_CR = ('Mark mainly against criterion C (Producing text) and D (Using language), with B (Organising). 7-8 equivalent: '
           'imaginative, insightful response with deliberate stylistic choices for effect, a controlled structure and varied, '
           'precise, accurate language; 5-6: substantial engagement and mostly effective choices; 3-4: adequate but uneven; '
           '1-2: limited, with frequent errors that obscure meaning.')
CRIT_B = ('Award marks for: an accurate identification of the feature or technique, a precise quotation or reference, and '
          'an explanation of its effect on the reader linked to the writer\'s purpose (criterion A). Naming a feature '
          'without explaining its effect: half marks at most.')
CRIT_A = ('Award marks for an accurate, specific point supported by a reference to the text (criterion A). A general '
          'assertion without evidence earns at most 1 mark.')
CRIT_OPEN = 'Credit any well-justified alternative supported by the text; the answer given is the most direct reading.'
CRIT_W = ('Indicative content above. Mark against criteria B, C and D: purpose and audience addressed (C), conventions of '
          'the form and logical organisation (B), register, vocabulary and accuracy (D).')
STYLE = {'eval_marks': 8, 'essay_marks': 12, 'markband': CRIT_ALL}

KIND = {
    'ad': 'advertisement', 'leaflet': 'leaflet', 'speech': 'speech', 'news': 'news report', 'oped': 'opinion column',
    'blog': 'blog post', 'letter': 'letter', 'infographic': 'infographic', 'review': 'review', 'interview': 'interview',
    'feature': 'feature article', 'website': 'web page', 'social': 'social media post', 'poster': 'campaign poster',
    'propaganda': 'propaganda poster', 'cartoon': 'cartoon', 'satire': 'satirical article', 'travel': 'travel writing extract',
    'myth': 'myth', 'legend': 'legend', 'prose': 'novel extract', 'story': 'short story extract', 'poem': 'poem',
    'drama': 'playscript extract', 'memoir': 'memoir extract', 'autobio': 'autobiography extract', 'bio': 'biography extract',
    'diary': 'diary entry', 'comic': 'graphic novel page', 'script': 'film script extract',
}
KIND_CONV = {
    'ad': 'a slogan or headline, an image, a brand name or logo, persuasive copy and a call to action',
    'leaflet': 'a clear heading, subheadings, short sections or bullet points, images, contact details and a call to action',
    'speech': 'direct address to a live audience, a hook, devices for the ear (repetition, rhetorical questions, the rule of three) and a memorable ending',
    'news': 'a headline, a lead paragraph answering who, what, where and when, the inverted pyramid and quotations from witnesses or experts',
    'oped': 'a by-line, a first-person argument on a topical issue, evidence and anecdote, a counterargument and a clear stance',
    'blog': 'an informal personal voice, a title and date, short paragraphs and an invitation for readers to comment',
    'letter': 'an address or salutation, a clear purpose in the opening, paragraphs that develop the case and a sign-off',
    'infographic': 'a headline, information shown visually (icons, charts, numbers), very little text and a source',
    'review': 'a rating or verdict, a brief summary that avoids spoilers, evaluation of strengths and weaknesses and a recommendation',
    'interview': 'an introduction to the interviewee, a question-and-answer format and direct quotation of the speaker\'s words',
    'feature': 'an eye-catching headline, a descriptive opening that sets a scene, human-interest detail, quotations and a reflective ending',
    'website': 'menus, banners, headings, hyperlinks and buttons, and short blocks of text for scrolling readers',
    'social': 'brevity, informal language, hashtags, emoji and a handle, written to be shared',
    'poster': 'a bold slogan, a striking central image, a call to action and the organisation\'s logo',
    'propaganda': 'a bold slogan, symbolic images, emotional appeals to duty, pride or fear and an instruction to the public',
    'cartoon': 'a single image or a few panels, caricature, captions or speech bubbles and exaggeration to make a point',
    'satire': 'an ironic voice, exaggeration and mock-seriousness used to criticise a target',
    'travel': 'a first-person traveller, vivid sensory description of place, encounters with local people and reflection',
    'myth': 'gods or supernatural beings, a hero, a quest or test, and an explanation of how something in nature or society began',
    'legend': 'a hero rooted in a real place or time, extraordinary deeds, and a story passed down orally',
    'prose': 'a narrator, characters, setting and plot, developed through description, dialogue and inner thoughts',
    'story': 'a small cast, a single situation, a turning point and often a twist or open ending',
    'poem': 'lines and stanzas, imagery, sound patterns (rhythm, rhyme, alliteration) and a speaker',
    'drama': 'character names before speeches, dialogue, stage directions in italics or brackets, and acts and scenes',
    'memoir': 'a first-person adult narrator looking back on real events, with reflection on what they meant',
    'autobio': 'a first-person account of the writer\'s own life, in roughly chronological order, with reflection',
    'bio': 'a third-person account of a real person\'s life, using facts, dates, sources and quotations',
    'diary': 'a date, a first-person private voice, the present moment and honest feelings',
    'comic': 'panels, gutters, captions, speech bubbles, sound effects and the interplay of word and image',
    'script': 'scene headings (INT./EXT.), action lines, character names and dialogue, and camera directions',
}
KIND_WRONG = {
    'ad': ['news report', 'diary entry', 'short story extract'], 'leaflet': ['poem', 'diary entry', 'news report'],
    'speech': ['infographic', 'news report', 'diary entry'], 'news': ['advertisement', 'diary entry', 'poem'],
    'oped': ['news report', 'advertisement', 'infographic'], 'blog': ['news report', 'speech', 'infographic'],
    'letter': ['advertisement', 'infographic', 'poem'], 'infographic': ['speech', 'blog post', 'letter'],
    'review': ['news report', 'speech', 'poem'], 'interview': ['poem', 'advertisement', 'diary entry'],
    'feature': ['advertisement', 'poem', 'leaflet'], 'website': ['speech', 'poem', 'letter'],
    'social': ['news report', 'speech', 'leaflet'], 'poster': ['short story extract', 'letter', 'diary entry'],
    'propaganda': ['news report', 'blog post', 'letter'], 'cartoon': ['speech', 'news report', 'letter'],
    'satire': ['news report', 'leaflet', 'poem'], 'travel': ['news report', 'advertisement', 'speech'],
    'myth': ['news report', 'advertisement', 'biography extract'], 'legend': ['news report', 'advertisement', 'diary entry'],
    'prose': ['speech', 'advertisement', 'news report'], 'story': ['advertisement', 'news report', 'speech'],
    'poem': ['news report', 'advertisement', 'letter'], 'drama': ['news report', 'blog post', 'advertisement'],
    'memoir': ['advertisement', 'news report', 'speech'], 'autobio': ['news report', 'advertisement', 'myth'],
    'bio': ['autobiography extract', 'advertisement', 'poem'], 'diary': ['news report', 'speech', 'advertisement'],
    'comic': ['speech', 'letter', 'news report'], 'script': ['news report', 'advertisement', 'letter'],
}
NONLIT = {'ad', 'leaflet', 'speech', 'news', 'oped', 'blog', 'letter', 'infographic', 'review', 'interview', 'feature',
          'website', 'social', 'poster', 'propaganda', 'cartoon', 'satire'}
LIT = {'myth', 'legend', 'prose', 'story', 'poem', 'drama', 'comic', 'script'}
LIFE = {'memoir', 'autobio', 'bio', 'diary', 'travel'}
PROSE = {'prose', 'story', 'myth', 'legend'}
NARR = PROSE | {'memoir', 'autobio', 'diary', 'travel'}
VISUAL = {'ad', 'poster', 'propaganda', 'infographic', 'cartoon', 'comic', 'website', 'leaflet'}
PERSUADE = {'ad', 'leaflet', 'speech', 'oped', 'letter', 'poster', 'propaganda', 'blog'}
MEDIA = {'news', 'feature', 'interview', 'oped', 'review', 'website', 'social'}

MARKS_BY_D = {1: 2, 2: 2, 3: 3, 4: 4, 5: 6}
LONG_BY_D = {1: 4, 2: 4, 3: 6, 4: 8, 5: 10}

# ---------------------------------------------------------------------------------------------------------------
# Common question frames
# ---------------------------------------------------------------------------------------------------------------
AUD_Q = ['Identify the intended audience of this {label}. Support your answer with one reference to the text.',
         'Who is the target audience of the text? Refer to two details that suggest this audience.',
         'Explain how the writer shows who the text is aimed at.']
PURP_Q = ['State the main purpose of the text and explain how one feature helps to achieve it.',
          'What is the writer trying to achieve in this {label}? Support your answer with evidence.',
          'Outline the purpose of the text and one way in which the writer pursues it.']
DEV_Q = ['Explain the effect of the {device} "{quote}" on the reader.',
         'Analyse how the phrase "{quote}" helps the writer achieve their purpose.',
         'Identify the technique used in "{quote}" and explain its effect.',
         'Comment on the writer\'s choice of language in "{quote}".']
STRUCT_Q = ['Analyse the effect of {feature} in the text.',
            'Explain how {feature} contributes to the meaning of the text.',
            'How does {feature} shape the reader\'s experience of the text?']
VIS_Q = ['Analyse how the visual elements of the text contribute to its message.',
         'Explain how layout, colour or the image are used in this text and their effect.',
         'Discuss how the words and the image work together in this text.']
TONE_Q = ['Describe the tone of the text and explain how the writer creates it.',
          'How would you describe the writer\'s tone? Refer to two language choices that create it.',
          'Explain how word choice establishes the tone of this {label}.']
MOOD_Q = ['Explain how the writer creates atmosphere in this extract.',
          'Analyse how sensory description is used to build the mood of the extract.',
          'How does the setting contribute to the mood of this extract? Refer closely to the text.']
CHAR_Q = ['What impression does the reader get of the main character? Support your answer with evidence.',
          'Explain what the character\'s actions and words reveal about them.',
          'Analyse how the writer presents the main character in this extract.']
THEME_Q = ['Identify a theme of this extract and explain how it is developed.',
           'What message or theme does the writer explore here? Support your answer with evidence.',
           'Explain how one detail in the extract connects to a wider theme.']
POV_Q = ['Identify the point of view from which this extract is told and explain its effect.',
         'Explain how the narrative perspective shapes what the reader knows and feels.',
         'Why might the writer have chosen this narrative voice? Refer to the text.']
SUM_Q = ['In no more than 50 words, summarise the main ideas of the text in your own words.',
         'Summarise the writer\'s key points in three bullet points, using your own words.',
         'Write a one-sentence summary of the text and then explain what the writer wants the reader to think or do.']
KCONV_Q = ['Identify the text type of this extract and explain how two of its conventions are used.',
           'Which features of the extract show that it is a particular text type? Give examples.',
           'Outline the conventions of the text type used here, with examples from the extract.']


def cap(s):
    return s[0].upper() + s[1:] if s else s


class Kit:
    """Passage library and question builders bound to one pack's Registry."""

    def __init__(self, R):
        self.R = R
        self.PASS: list[dict] = []
        self.PAIRS: list[dict] = []
        self.PROMPTS: list[dict] = list(PROMPTS)

    # -- registration helpers ---------------------------------------------------------------------------------
    def _reg(self, keys, t):
        keys = [keys] if isinstance(keys, str) else keys
        for k in keys:
            self.R.t.setdefault(k, []).append(t)

    def P(self, **kw):
        kw.setdefault('dev', [])
        kw.setdefault('struct', [])
        self.PASS.append(kw)
        return kw

    def by_id(self, pid):
        for p in self.PASS:
            if p['id'] == pid:
                return p
        raise KeyError(pid)

    def pair(self, a, b, q, ans, **kw):
        self.PAIRS.append(dict(a=a, b=b, q=q, ans=ans, **kw))

    def pool(self, kinds=None, note=None, ids=None):
        out = []
        for p in self.PASS:
            if ids is not None and p['id'] not in ids:
                continue
            if ids is None and kinds is not None and p['kind'] not in kinds:
                continue
            if note:
                notes = note if isinstance(note, tuple) else (note,)
                if not all(p.get(n) for n in notes):
                    continue
            out.append(p)
        return out

    # -- passage presentation -----------------------------------------------------------------------------------
    @staticmethod
    def label(p):
        return KIND[p['kind']]

    def intro(self, p, neutral=False, tag=None):
        head = 'Read the following text.' if neutral else f'Read the following {p["title"]}.'
        if tag:
            head = f'{tag}: {p["title"]}.'
        return f'{head}\n\n{p["text"]}'

    def _get(self, p, note, rng):
        if note in ('dev', 'struct'):
            if not p.get(note):
                return None
            e = rng.choice(p[note])
            if note == 'dev':
                return dict(device=e[0], quote=e[1]), f'{cap(e[0])}: "{e[1]}" – {e[2]}.'
            return dict(feature=e[0]), f'{cap(e[0])}: {e[1]}.'
        if note == 'kconv':
            ex = []
            if p.get('dev'):
                d0 = rng.choice(p['dev'])
                ex.append(f'"{d0[1]}" ({d0[0]})')
            if p.get('struct'):
                ex.append(p['struct'][0][0])
            exs = ' and '.join(ex) if ex else 'its layout'
            return dict(), (f'It is a {self.label(p)}. Conventions: {KIND_CONV[p["kind"]]}. In this text, for example: {exs}, '
                            f'each chosen to suit the purpose and audience.')
        if note == 'tone':
            if not p.get('tone'):
                return None
            return dict(), f'The tone is {p["tone"]}: {p.get("tonex", "")}'.strip()
        if isinstance(note, tuple):
            parts = [p.get(n) for n in note]
            if not all(parts):
                return None
            return dict(), ' '.join(cap(x).rstrip('.') + '.' for x in parts)
        v = p.get(note)
        if not v:
            return None
        if note == 'theme' and p.get('gqa'):
            return dict(), f'Theme: {v}. How it is developed: {p["gqa"]}'
        if note in ('purp', 'aud') and p.get('dev'):
            d0 = rng.choice(p['dev'])
            v = f'{v.rstrip(".")}. Supporting evidence: "{d0[1]}" ({d0[0]}) – {d0[2]}.'
        return dict(), v

    def _fmt(self, q, p, fd):
        d = dict(fd)
        d.setdefault('gq', p.get('gq', ''))
        d.setdefault('label', self.label(p))
        d.setdefault('theme', p.get('theme', 'its theme').split(':')[0].rstrip('.'))
        return q.format(**d)

    # -- builders ----------------------------------------------------------------------------------------------
    def pq(self, keys, c, d, kinds, note, qs, typ='short', crit=None, marks=None, neutral=False, ids=None, name_='pq'):
        """Passage frames: stem = passage + one of qs; answer from the passage annotation for `note`."""
        kinds = set(kinds) if kinds else None

        def fn(rng, slot):
            pool = self.pool(kinds, None if note == 'kconv' else note, ids)
            if note == 'kconv':
                pool = [p for p in pool if p['kind'] in KIND_CONV]
            if not pool:
                return None
            p = rng.choice(pool)
            g = self._get(p, note, rng)
            if g is None:
                return None
            fd, ans = g
            q = self._fmt(rng.choice(qs), p, fd)
            m = marks if marks else (LONG_BY_D[slot.d] if typ == 'long' else MARKS_BY_D[slot.d])
            return dict(stem=f'{self.intro(p, neutral)}\n\n{q}', answer=ans, type=typ, marks=m,
                        markingKey=f'{ans} {crit or CRIT_B}')
        nm = name_ + '_' + (note if isinstance(note, str) else '_'.join(note))
        self._reg(keys, T(c, d, fn, typ, None, nm))

    def qa(self, keys, c, d, kinds=None, ids=None, crit=None, field='qa'):
        """Passage-specific questions stored as p[field] = [(question, answer), ...]."""
        kinds = set(kinds) if kinds else None

        def fn(rng, slot):
            pool = self.pool(kinds, field, ids)
            if not pool:
                return None
            p = rng.choice(pool)
            q, a = rng.choice(p[field])[:2]
            return dict(stem=f'{self.intro(p)}\n\n{q}', answer=a, type='short', marks=MARKS_BY_D[slot.d],
                        markingKey=f'{a} {crit or CRIT_A}')
        self._reg(keys, T(c, d, fn, 'short', None, 'qa_' + field))

    def vocab(self, keys, d=(1, 3), kinds=None, ids=None, c='C1'):
        kinds = set(kinds) if kinds else None

        def fn(rng, slot):
            pool = self.pool(kinds, 'vocab', ids)
            if not pool:
                return None
            p = rng.choice(pool)
            w, mean, wrong = rng.choice(p['vocab'])[:3]
            q = rng.choice([f'As it is used in the text, the word "{w}" most nearly means:',
                            f'In the context of this text, what does "{w}" mean?',
                            f'Which meaning of "{w}" fits the way it is used in the text?'])
            return mcq(rng, f'{self.intro(p)}\n\n{q}', mean, wrong, f'In context, "{w}" means {mean.lower()}.')
        self._reg(keys, T(c, d, fn, 'mcq', None, 'vocab'))

    def vocab_explain(self, keys, c='C2', d=(2, 4), kinds=None, ids=None):
        kinds = set(kinds) if kinds else None

        def fn(rng, slot):
            pool = [p for p in self.pool(kinds, 'vocab', ids) if any(len(v) > 3 for v in p['vocab'])]
            if not pool:
                return None
            p = rng.choice(pool)
            w, mean, _, why = rng.choice([v for v in p['vocab'] if len(v) > 3])
            q = rng.choice([f'Explain what the word "{w}" means in this text and why the writer chose it.',
                            f'What does "{w}" suggest here? Explain the connotations of the word in context.'])
            a = f'"{w}" means {mean.lower()} here; {why}'
            return dict(stem=f'{self.intro(p)}\n\n{q}', answer=a, type='short', marks=MARKS_BY_D[slot.d],
                        markingKey=f'{a} 1 mark for the meaning in context; further marks for connotation and effect.')
        self._reg(keys, T(c, d, fn, 'short', None, 'vocab_explain'))

    def dev_mcq(self, keys, kinds=None, d=(1, 3), ids=None):
        kinds = set(kinds) if kinds else None

        def fn(rng, slot):
            pool = self.pool(kinds, 'dev', ids)
            if not pool:
                return None
            p = rng.choice(pool)
            e = rng.choice(p['dev'])
            q = rng.choice([f'The words "{e[1]}" are an example of which technique?',
                            f'Which technique is used in "{e[1]}"?',
                            f'Identify the device in the quotation "{e[1]}".'])
            return mcq(rng, f'{self.intro(p)}\n\n{q}', e[0], e[3], f'"{e[1]}" is an example of {e[0]}: {e[2]}.')
        self._reg(keys, T('C1', d, fn, 'mcq', None, 'dev_mcq'))

    def tone_mcq(self, keys, kinds=None, d=(1, 3), ids=None):
        kinds = set(kinds) if kinds else None

        def fn(rng, slot):
            pool = self.pool(kinds, ('tone', 'tw'), ids)
            if not pool:
                return None
            p = rng.choice(pool)
            q = rng.choice(['Which word best describes the overall tone of the text?',
                            'The tone of this text is best described as:',
                            'Which of the following best captures the writer\'s tone?'])
            return mcq(rng, f'{self.intro(p)}\n\n{q}', p['tone'], p['tw'], f'The tone is {p["tone"]}: {p.get("tonex", "")}'.strip())
        self._reg(keys, T('C1', d, fn, 'mcq', None, 'tone_mcq'))

    def kind_mcq(self, keys, kinds=None, d=(1, 2), ids=None):
        kinds = set(kinds) if kinds else None

        def fn(rng, slot):
            pool = [p for p in self.pool(kinds, None, ids) if p['kind'] in KIND_WRONG]
            if not pool:
                return None
            p = rng.choice(pool)
            q = rng.choice(['Which text type is this?', 'This text is best classified as a:',
                            'Identify the text type of the extract above.'])
            return mcq(rng, f'{self.intro(p, neutral=True)}\n\n{q}', self.label(p), KIND_WRONG[p['kind']],
                       f'It is a {self.label(p)}: it uses conventions such as {KIND_CONV[p["kind"]]}.')
        self._reg(keys, T('C1', d, fn, 'mcq', None, 'kind_mcq'))

    def para(self, keys, kinds=None, c='C4', d=(3, 5), frames=None, crit=None, ids=None, marks=None):
        """Analytical paragraph / short essay on the passage's guiding question."""
        kinds = set(kinds) if kinds else None
        frames = frames or [
            '{gq}\nWrite one analytical paragraph (point, evidence, explanation) that answers this question, using at least two quotations.',
            'Answer the following question in a well-organised response of about 250 words: {gq}',
        ]

        def fn(rng, slot):
            pool = self.pool(kinds, ('gq', 'gqa'), ids)
            if not pool:
                return None
            p = rng.choice(pool)
            m = marks or (6 if slot.d <= 3 else 8 if slot.d == 4 else 12)
            q = self._fmt(rng.choice(frames), p, {})
            return dict(stem=f'{self.intro(p)}\n\n{q}', answer=p['gqa'], type='long', marks=m,
                        markingKey=f'Indicative content: {p["gqa"]} {crit or CRIT_AN}')
        self._reg(keys, T(c, d, fn, 'long', None, 'para'))

    def write(self, keys, c='C4', d=(3, 5), kinds=None, ids=None, field='write', crit=None):
        """Directed writing in response to a passage: p[field] = [(task, indicative content), ...]."""
        kinds = set(kinds) if kinds else None

        def fn(rng, slot):
            pool = self.pool(kinds, field, ids)
            if not pool:
                return None
            p = rng.choice(pool)
            task, ind = rng.choice(p[field])[:2]
            m = 6 if slot.d <= 3 else 8 if slot.d == 4 else 12
            return dict(stem=f'{self.intro(p)}\n\n{task}', answer=ind, type='long', marks=m,
                        markingKey=f'{ind} {crit or CRIT_W}')
        self._reg(keys, T(c, d, fn, 'long', None, 'write_' + field))

    def _pairs(self, only=None, need_sim=False):
        """Pairs, optionally restricted to those whose Text A or Text B id is in `only`."""
        prs = [x for x in self.PAIRS if not need_sim or x.get('sim')]
        if only is not None:
            prs = [x for x in prs if x['a'] in only or x['b'] in only]
        return prs

    def compare(self, keys, c='C4', d=(3, 5), frames=None, marks=None, crit=None, only=None):
        frames = frames or ['{q}', 'Compare and contrast the two texts. {q}',
                            '{q} In your answer, refer closely to both texts and use comparative connectives.']

        def fn(rng, slot):
            prs = self._pairs(only)
            if not prs:
                return None
            pr = rng.choice(prs)
            a, b = self.by_id(pr['a']), self.by_id(pr['b'])
            q = rng.choice(frames).format(q=pr['q'])
            m = marks or (8 if slot.d <= 4 else 12)
            stem = f'{self.intro(a, tag="Text A")}\n\n{self.intro(b, tag="Text B")}\n\n{q}'
            return dict(stem=stem, answer=pr['ans'], type='long', marks=m,
                        markingKey=f'Indicative content: {pr["ans"]} {crit or CRIT_AN} Comparison must be sustained across both texts (criterion B).')
        self._reg(keys, T(c, d, fn, 'long', None, 'compare'))

    def compare_short(self, keys, c='C3', d=(2, 4), only=None):
        """One-similarity / one-difference questions on a pair (pair notes 'sim' and 'diff' optional)."""
        def fn(rng, slot):
            prs = self._pairs(only, need_sim=True)
            if not prs:
                return None
            pr = rng.choice(prs)
            a, b = self.by_id(pr['a']), self.by_id(pr['b'])
            q, ans = rng.choice([('Identify ONE similarity and ONE difference between the two texts, supporting each with a reference to both texts.', f'Similarity: {pr["sim"]} Difference: {pr["diff"]}'),
                                 ('Using a comparative connective, write two sentences that compare how the two texts approach their shared subject.', f'For example: "Similarly, {pr["sim"]}" and "However, {pr["diff"]}"')])
            stem = f'{self.intro(a, tag="Text A")}\n\n{self.intro(b, tag="Text B")}\n\n{q}'
            return dict(stem=stem, answer=ans, type='short', marks=MARKS_BY_D[slot.d] + 1,
                        markingKey=f'{ans} One mark for each valid, supported point; credit other valid comparisons.')
        self._reg(keys, T(c, d, fn, 'short', None, 'compare_short'))

    def prompts(self, keys, mode, c='C4', d=(3, 5)):
        """Creative writing from visual prompts. mode: interpret | plan | write | open (opening paragraph) | one."""
        def fn(rng, slot):
            return self._prompt_item(rng, slot, mode)
        typ = 'long' if mode in ('write', 'open', 'one') else 'case'
        self._reg(keys, T(c, d, fn, typ, None, 'prompt_' + mode))

    def _three(self, rng):
        ps = rng.sample(self.PROMPTS, 3)
        txt = '\n'.join(f'Image {i}: {p["img"]}' for i, p in enumerate(ps, 1))
        return ps, txt

    def _prompt_item(self, rng, slot, mode, marks=None, minutes=None):
        if mode in ('interpret', 'plan', 'write'):
            ps, txt = self._three(rng)
            head = f'Look at the three images described below.\n\n{txt}\n\n'
        else:
            ps = [rng.choice(self.PROMPTS)]
            head = f'Look at the image described below.\n\n{ps[0]["img"]}\n\n'
        if mode == 'interpret':
            q = rng.choice(['Choose ONE image. Describe the mood it creates and suggest two different story ideas it could inspire, explaining whose perspective you would tell each from.',
                            'Choose ONE image. Explain what the image suggests about place, character and feeling, and outline one story it could start.'])
            ans = ' | '.join(f'Image {i}: mood – {p["mood"]}; ideas – {p["ideas"]}' for i, p in enumerate(ps, 1))
            m = marks or 5
            key = f'Indicative content (any image): {ans} Marks: mood identified and justified from details (2); two plausible ideas (2); perspective explained (1).'
            return dict(stem=head + q, answer=ans, type='case', marks=m, markingKey=key, **({'minutes': minutes} if minutes else {}))
        if mode == 'plan':
            q = rng.choice(['Choose ONE image and plan a creative piece of 400-600 words. State your form and audience, your narrator, a three-part structure and two language techniques you will use, with a reason for each.',
                            'Choose ONE image. Plan a piece of creative writing: give a title, the form (story, diary, letter or speech), the opening hook, the turning point, the ending and the register you will use.'])
            p = ps[0]
            ans = (f'Model plan for Image 1 – form: {p["form"]}; narrator: {p["voice"]} narrator; structure: {p["plan"]}; techniques: '
                   f'{p["tech"]}. Plans for the other images must show the same elements.')
            m = marks or 5
            key = f'{ans} Marks: form and audience (1); narrator and perspective (1); coherent structure with a turning point (2); purposeful techniques (1).'
            return dict(stem=head + q, answer=ans, type='case', marks=m, markingKey=key, **({'minutes': minutes} if minutes else {}))
        if mode == 'write':
            q = rng.choice(['Write a creative piece of 400-600 words inspired by ONE of the images. You may write a story, a diary entry, a letter or a speech.',
                            'Choose ONE image and use it as the starting point for a piece of imaginative writing (400-600 words). Give your piece a title.',
                            'Write a narrative or descriptive piece (400-600 words) inspired by ONE image. Your piece should show a clear perspective and a deliberate structure.'])
            p = ps[0]
            ans = (f'Indicative content (Image 1 example): {p["ideas"]}; {p["voice"]} narrator; structure: {p["plan"]}; techniques such as {p["tech"]}. '
                   'Any image and form may be chosen; the piece should go beyond literal description of the image.')
            m = marks or (12 if slot.d <= 4 else 16)
            return dict(stem=head + q, answer=ans, type='long', marks=m, markingKey=f'{ans} {CRIT_CR}', **({'minutes': minutes} if minutes else {}))
        p = ps[0]
        if mode == 'open':
            q = rng.choice(['Write the opening paragraph (about 150 words) of a story inspired by this image. Hook the reader and establish the mood.',
                            'Write a descriptive paragraph (about 150 words) that recreates this scene using at least three senses.'])
            ans = f'Indicative content: establishes a {p["mood"]} mood; possible idea – {p["ideas"]}; techniques such as {p["tech"]}; a hook that raises a question.'
            return dict(stem=head + q, answer=ans, type='long', marks=6 if slot.d <= 3 else 8, markingKey=f'{ans} {CRIT_CR}')
        q = rng.choice([f'Write a {p["form"]} of about 300 words inspired by this image.',
                        f'Using this image as a stimulus, write about 300 words told by {p["voice"]} narrator.'])
        ans = f'Indicative content: {p["ideas"]}; structure – {p["plan"]}; techniques such as {p["tech"]}; a {p["mood"]} mood.'
        return dict(stem=head + q, answer=ans, type='long', marks=8 if slot.d <= 4 else 12, markingKey=f'{ans} {CRIT_CR}')

    # -- MYP 5 eAssessment-style mock ------------------------------------------------------------------------------
    def mock_templates(self, lit_kinds=None, nonlit_kinds=None):
        lit_kinds = set(lit_kinds or (LIT | LIFE))
        nonlit_kinds = set(nonlit_kinds or NONLIT)

        def t1(rng, slot, kinds, tag, style):
            if slot.style != style:
                return None
            pool = self.pool(kinds, ('gq', 'gqa'))
            p = rng.choice(pool)
            stem = (f'Task 1 – Analysis. {self.intro(p, tag=tag)}\n\n{p["gq"]}\n'
                    'Refer closely to the text, using short quotations, and explain the effects of the writer\'s choices.')
            return dict(stem=stem, answer=p['gqa'], type='explain', marks=5, minutes=10,
                        markingKey=f'Indicative content: {p["gqa"]} Criterion A (scaled to 5): 5 perceptive analysis of several choices with precise evidence; 3-4 substantial; 2 adequate; 1 limited.')

        def t1a(rng, slot):
            return t1(rng, slot, lit_kinds, 'Text A', 't1a')

        def t1b(rng, slot):
            return t1(rng, slot, nonlit_kinds, 'Text B', 't1b')

        def t1c(rng, slot):
            if slot.style != 't1c':
                return None
            pr = rng.choice(self.PAIRS)
            a, b = self.by_id(pr['a']), self.by_id(pr['b'])
            stem = (f'Task 1 – Comparative analysis. {self.intro(a, tag="Text A")}\n\n{self.intro(b, tag="Text B")}\n\n'
                    f'{pr["q"]} Write a comparative response that analyses both texts, using evidence and comparative connectives.')
            return dict(stem=stem, answer=pr['ans'], type='long', marks=20, minutes=35,
                        markingKey=f'Indicative content: {pr["ans"]} {CRIT_ALL} (A 8, B 4, D 8 scaled to 20.)')

        def t2(mode, style, marks, minutes):
            def fn(rng, slot):
                if slot.style != style:
                    return None
                it = self._prompt_item(rng, slot, mode, marks=marks, minutes=minutes)
                it['stem'] = 'Task 2 – Creative writing. ' + it['stem']
                return it
            return fn

        return [T(('C3', 'C4'), (3, 5), t1a, 'explain', 't1a', 'task1a'),
                T(('C3', 'C4'), (3, 5), t1b, 'explain', 't1b', 'task1b'),
                T('C4', (3, 5), t1c, 'long', 't1c', 'task1c'),
                T(('C3', 'C4'), (2, 4), t2('interpret', 't2a', 5, 8), 'case', 't2a', 'task2a'),
                T(('C3', 'C4'), (2, 4), t2('plan', 't2b', 5, 10), 'case', 't2b', 'task2b'),
                T('C4', (3, 5), t2('write', 't2c', 20, 50), 'long', 't2c', 'task2c')]


def mock_sections(t1_chapters, t2_chapters):
    """MYP 5 eAssessment-style mock: Task 1 analysis (30) and Task 2 creative writing (scaled to 30)."""
    return [
        dict(section='Task 1 – Analysis: Text A (literary extract)', count=1, c=['C3'], d=[3], type='explain', marks=5, style='t1a', chapters=t1_chapters),
        dict(section='Task 1 – Analysis: Text B (non-literary text)', count=1, c=['C3'], d=[3], type='explain', marks=5, style='t1b', chapters=t1_chapters),
        dict(section='Task 1 – Comparative analysis of Texts A and B (criteria A, B, D)', count=1, c=['C4'], d=[4], type='long', marks=20, style='t1c', chapters=t1_chapters),
        dict(section='Task 2 – Creative writing: interpreting three visual prompts', count=1, c=['C3'], d=[3], type='case', marks=5, style='t2a', chapters=t2_chapters),
        dict(section='Task 2 – Creative writing: planning the response', count=1, c=['C3'], d=[3], type='case', marks=5, style='t2b', chapters=t2_chapters),
        dict(section='Task 2 – Creative writing: 400-600 word piece (criteria B, C, D)', count=1, c=['C4'], d=[4], type='long', marks=20, style='t2c', chapters=t2_chapters),
    ]


# ---------------------------------------------------------------------------------------------------------------
# Visual prompts (images described in words) for creative writing
# ---------------------------------------------------------------------------------------------------------------
def VP(img, mood, ideas, form, voice, plan, tech):
    return dict(img=img, mood=mood, ideas=ideas, form=form, voice=voice, plan=plan, tech=tech)


PROMPTS = [
    VP('[A photograph: an empty playground swing still moving in thick fog; a single red glove lies on the wet tarmac.]',
       'eerie and melancholy', 'someone has just left in a hurry – a lost child, a goodbye, or a memory returning to an adult who played there',
       'short story', 'a first-person', 'calm opening in the fog – discovery of the glove – revelation of who left it', 'pathetic fallacy, a recurring colour motif (red against grey), short sentences for tension'),
    VP('[A photograph: a crowded night market in Bangkok seen from above; one stall glows brighter than the rest, and a boy stands still in the moving crowd.]',
       'busy, vibrant but slightly lonely', 'a boy separated from his family, a stallholder\'s last night before the market closes, or a newcomer to the city',
       'story', 'a third-person limited', 'sensory overload – a moment of stillness and loss – reunion or decision', 'sensory lists, contrast between motion and stillness, a shift in pace'),
    VP('[A painting: a lighthouse on a black rock in a storm; its beam cuts across the waves towards a small boat.]',
       'dramatic and hopeful', 'a keeper guiding a boat home, a rescue told from the boat, or a lighthouse that is about to be switched off forever',
       'diary entry', 'a first-person', 'the storm builds – the boat is seen – the outcome at dawn', 'personification of the sea, light and dark imagery, a cyclical ending'),
    VP('[A photograph: an elderly woman and a teenage girl sit on a train platform in Mumbai, sharing earphones; the departures board shows "DELAYED".]',
       'warm, quiet and bittersweet', 'a grandmother and granddaughter on their last journey together, a delayed train that changes a decision, or music that bridges generations',
       'story', 'a first-person teenage', 'waiting and irritation – shared song and memory – departure', 'dialogue to reveal character, a symbol (the shared earphones), a flashback'),
    VP('[A photograph: a cracked smartphone screen lit up in the dark, showing 47 unread messages.]',
       'tense and anxious', 'a rumour spreading online, a message that cannot be taken back, or an emergency at home',
       'story', 'a second-person', 'the screen lights up – the messages are read – a choice about how to respond', 'second-person address, fragmented sentences, a countdown structure'),
    VP('[A painting: a wide golden wheatfield with a single tree; a red kite is caught in its branches.]',
       'peaceful with a hint of longing', 'a child\'s lost kite, a farmer\'s memory of his brother, or a promise made under the tree years ago',
       'memoir-style narrative', 'a first-person adult looking back', 'present day – memory of the kite – return to the present changed', 'colour imagery, retrospective narration, a symbolic object'),
    VP('[A photograph: a flooded street in a coastal town; a dog sits on the roof of a floating car, looking at the camera.]',
       'tense but strangely calm', 'a rescue told by a volunteer, the dog\'s owner searching for it, or the day the river came',
       'news-inspired narrative or a letter', 'a first-person rescuer', 'the water rises – the search – the rescue and its cost', 'present tense for immediacy, sensory detail of water, a powerful final image'),
    VP('[A photograph: a girl in a football kit stands alone in a stadium tunnel, looking towards the bright pitch.]',
       'nervous and expectant', 'a first match after an injury, a trial for a national team, or proving a doubter wrong',
       'speech or story', 'a first-person', 'doubt in the tunnel – flashback to training – stepping into the light', 'internal monologue, light and dark contrast, a ticking clock'),
    VP('[A photograph: an abandoned greenhouse in Iceland, its glass broken, with tomatoes still growing wild inside.]',
       'mysterious and hopeful', 'life continuing after people leave, a family returning to their old farm, or a secret garden',
       'descriptive piece', 'a first-person explorer', 'approach – inside the greenhouse – what the discovery means', 'juxtaposition of decay and growth, sensory description, a reflective close'),
    VP('[A drawing: a staircase that spirals up into the clouds; at the bottom, a pair of school shoes has been left neatly side by side.]',
       'dreamlike and uncertain', 'an escape from pressure, a fantasy quest, or a dream about growing up',
       'fantasy story', 'a third-person', 'ordinary morning – the staircase appears – the climb and what is at the top', 'magical realism, symbolism, a circular structure'),
    VP('[A photograph: the hands of a street musician in Buenos Aires playing an old accordion; coins and a handwritten sign that says "For Mamá" lie in the case.]',
       'tender and determined', 'a musician raising money for his mother, a passer-by whose day is changed, or the history of the accordion',
       'story', 'a third-person passer-by', 'ordinary rush hour – the music stops someone – a small act of kindness', 'sound imagery, a shift in perspective, understatement'),
    VP('[A photograph: a moving van parked outside a block of flats at dawn; a child presses a hand against the van\'s back window.]',
       'sad and reflective', 'leaving home, a friend left behind, or the first morning in a new country',
       'diary entry or letter', 'a first-person child', 'the last morning – the journey – the first sight of somewhere new', 'present tense, lists of things left behind, a hopeful final line'),
    VP('[A photograph: a hospital corridor at 3 a.m.; a vending machine glows and a teenage boy sits beneath it with a paper cup.]',
       'quiet, anxious and lonely', 'waiting for news of a parent, meeting a stranger in the night, or a night that changes a family',
       'story', 'a first-person teenage', 'waiting – a conversation with a stranger – the doctor appears', 'slow pacing, dialogue, sensory detail of sound and light'),
    VP('[A painting: a desert at night under a sky full of stars; a camel caravan\'s lanterns form a line of tiny lights.]',
       'vast, peaceful and awe-inspiring', 'a journey to a new life, a young guide\'s first crossing, or an ancient story retold',
       'myth-inspired narrative', 'a third-person storyteller', 'departure – a test in the desert – arrival at dawn', 'imagery of light and darkness, repetition, the oral-storytelling voice'),
    VP('[A photograph: a robot vacuum cleaner stuck against a door in a dark flat; the door is open just a crack, letting in light.]',
       'humorous and slightly unsettling', 'the world from a machine\'s point of view, a family who has disappeared, or a robot that wants to escape',
       'science fiction story', 'a first-person machine', 'routine – something unusual – the door opens', 'an unusual narrator, humour, dramatic irony'),
    VP('[A photograph: two hands, one old and one young, holding the same chess piece above a board in a park in Moscow.]',
       'tense but affectionate', 'a final game between a grandfather and grandson, a rivalry between strangers, or passing on a skill',
       'story', 'a third-person', 'the game begins – memories surface – the final move', 'symbolism of the game, dialogue, a pause before the climax'),
    VP('[A photograph: a schoolbag left on a bench at a bus stop in heavy rain; the bus\'s red tail-lights disappear around the corner.]',
       'frustrated and lonely', 'a missed bus that changes a day, a forgotten bag that holds a secret, or a moment of rebellion',
       'story', 'a first-person', 'the missed bus – opening the bag – an unexpected consequence', 'pathetic fallacy, a twist, short paragraphs'),
    VP('[A photograph: a mountain village in Nepal after an earthquake; a girl carries a school whiteboard on her back up a dusty path.]',
       'determined and hopeful', 'rebuilding a school, a teacher\'s journey, or a community that refuses to give up',
       'speech or story', 'a first-person', 'the damage – the decision to rebuild – the first lesson', 'contrast between destruction and hope, the rule of three, a call to action'),
    VP('[A drawing: a city where all the buildings are made of books; a boy reads on a balcony while pages flutter down like snow.]',
       'whimsical and wondrous', 'a world where stories are homes, a city in danger of being forgotten, or the last library',
       'fantasy story', 'a third-person', 'introduction of the world – a threat – the boy\'s choice', 'extended metaphor, vivid imagery, world-building detail'),
    VP('[A photograph: a fishing boat returning to a harbour in Ghana at sunset; children run along the beach towards it.]',
       'joyful and warm', 'a father\'s return, a first catch, or a village celebration',
       'descriptive piece', 'a first-person child', 'waiting on the beach – the boat appears – the welcome', 'colour imagery, sound, a rising tempo'),
    VP('[A photograph: a single lit window in a tall dark tower block at midnight; a silhouette is holding a sign against the glass that says "HELLO?".]',
       'mysterious and lonely', 'a call for help, a game between neighbours, or loneliness in a big city',
       'story', 'a first-person neighbour', 'noticing the sign – replying – meeting the person', 'suspense, an epistolary element (signs as messages), a gentle twist'),
    VP('[A photograph: snow falling on a market in Kraków; a stallholder pours hot chocolate for a girl who is counting coins.]',
       'cosy but poignant', 'a small kindness, a girl saving for a present, or a stallholder\'s memory of his own childhood',
       'story', 'a third-person', 'the cold – the coins don\'t add up – the kindness', 'sensory contrast of cold and warmth, dialogue, understatement'),
    VP('[A photograph: a cracked mirror propped against a wall in an empty room; it reflects a doorway, but the doorway is not in the room.]',
       'uncanny and unsettling', 'a ghost story, a parallel world, or a memory of a house that no longer exists',
       'Gothic short story', 'a first-person', 'arrival in the empty house – the impossible reflection – what steps through', 'foreshadowing, the uncanny, a cliffhanger ending'),
    VP('[A photograph: a crowd of students marching with hand-painted placards that read "THERE IS NO PLANET B"; one younger girl is on her father\'s shoulders.]',
       'energetic and defiant', 'a first protest, a speech at the march, or a family divided by an issue',
       'speech', 'a first-person speaker', 'hook – evidence and personal story – a call to action', 'rhetorical questions, anaphora, direct address'),
]


# ---------------------------------------------------------------------------------------------------------------
# Shared passage library (original texts written for this bank; pitched at ages 13-16)
# ---------------------------------------------------------------------------------------------------------------
def add_shared(K: Kit):
    P = K.P
    P(id='trainers', kind='ad', title='advertisement for running shoes, printed in a teen sports magazine',
      text=("[Image: a girl sprints up concrete steps at dawn; the city below is still asleep.]\n"
            "THEY SAID TOO YOUNG. THEY SAID TOO SMALL. THEY SAID TOO LATE.\n"
            "She said: watch me.\n"
            "STRIDE X – featherlight foam, grip that never quits.\n"
            "Your city. Your rules. Your run.\n"
            "#RunYourWay  |  Available now in 12 colours."),
      aud='Teenagers, especially girls, who play sport or want to: the young athlete in the image, the magazine and the hashtag target them.',
      purp='To persuade young readers to buy STRIDE X by linking the shoes with determination and proving doubters wrong.',
      tone='defiant', tw=['nostalgic', 'gentle', 'humorous'], tonex='the repeated "THEY SAID" and the reply "watch me" create a defiant, rebellious tone.',
      dev=[('anaphora (repetition)', 'THEY SAID TOO YOUNG. THEY SAID TOO SMALL. THEY SAID TOO LATE.', 'the repeated doubts build pressure, so the reader shares the girl\'s frustration and wants to see her prove them wrong', ['onomatopoeia', 'simile', 'statistic']),
           ('tricolon (rule of three)', 'Your city. Your rules. Your run.', 'three short, possessive phrases give the reader a feeling of control and make the slogan memorable', ['oxymoron', 'rhetorical question', 'simile']),
           ('direct address', 'Your city', 'the second-person pronoun makes every reader feel personally spoken to and included', ['personification', 'alliteration', 'hyperbole']),
           ('hyperbole', 'grip that never quits', 'the exaggeration suggests the shoes are completely reliable, like a loyal teammate', ['onomatopoeia', 'rhetorical question', 'simile'])],
      struct=[('the contrast between the capitalised doubts and the short reply', 'the shift from loud criticism to a calm "She said: watch me" makes the athlete seem confident and in control'),
              ('ending with the hashtag and colours', 'it moves from emotion to action, inviting readers to join an online community and buy')],
      visual='The low angle up the steps makes the girl look powerful; the sleeping city shows her dedication, and the dawn light suggests a new beginning.',
      vocab=[('quits', 'gives up', ['leaves a job', 'becomes quiet', 'falls over'], 'it personifies the grip as a determined athlete who never gives up.')],
      gq='How does the advertisement use language and image to persuade young people that the shoes will make them stronger?',
      gqa=('Point: the advert sells confidence, not just shoes. Evidence: the anaphora "THEY SAID TOO YOUNG..." and the reply "watch me". Explanation: the repeated doubts build frustration that the short reply releases, '
           'so the reader links the brand with proving people wrong. The tricolon "Your city. Your rules. Your run." and the low-angle dawn image make the reader feel powerful and independent; the product details are brief because the emotion does the persuading.'),
      write=[('Write a letter to the editor of the magazine (about 200 words) arguing either that this advertisement inspires young people or that it puts pressure on them to buy expensive products.', 'Indicative content: letter conventions (salutation, clear stance, sign-off); refers to specific features (the "THEY SAID" repetition, the image, the hashtag); one counterargument; formal register.')],
      summary='The advert uses a story of a girl who ignores people\'s doubts to sell STRIDE X running shoes; it links the shoes with confidence and freedom and invites readers to buy them and join #RunYourWay.',
      theme='determination: proving doubters wrong')

    P(id='plasticfree', kind='leaflet', title='leaflet from a school eco-club in Singapore',
      text=("GO PLASTIC-FREE THIS JULY!\n"
            "Did you know? Our canteen throws away about 900 plastic cups every week. That's over 30,000 a year – enough to reach the top of Marina Bay Sands if you stacked them!\n"
            "What can YOU do?\n"
            "• Bring a reusable bottle (free refills at the new water fountains).\n"
            "• Say \"no straw, please\".\n"
            "• Join our Thursday lunchtime clean-up.\n"
            "Small changes. Big difference. Sign up at the eco-club table by Friday!"),
      aud='Students at the school: the canteen, the lunchtime clean-up and the informal, energetic tone address them directly.',
      purp='To persuade students to reduce plastic use in July and to join the eco-club\'s activities.',
      tone='enthusiastic', tw=['bitter', 'mournful', 'detached'], tonex='exclamation marks, capital letters and an upbeat call to action make the tone enthusiastic.',
      dev=[('statistic', 'about 900 plastic cups every week', 'a precise local number makes the problem real and shows it is caused by the readers themselves', ['simile', 'onomatopoeia', 'metaphor']),
           ('rhetorical question', 'What can YOU do?', 'it makes the reader stop and think, and leads straight into practical answers', ['statistic', 'simile', 'alliteration']),
           ('imperative', 'Bring a reusable bottle', 'the command gives clear, simple instructions that are easy to follow', ['rhetorical question', 'personification', 'hyperbole']),
           ('antithesis (contrast)', 'Small changes. Big difference.', 'the contrast reassures readers that easy actions can have a large effect', ['onomatopoeia', 'statistic', 'simile'])],
      struct=[('the bullet-pointed list of actions', 'it breaks advice into short, manageable steps that a busy student can scan quickly'),
              ('the vivid comparison with Marina Bay Sands', 'it turns an abstract number into a local landmark the audience can picture, making the problem memorable')],
      vocab=[('reusable', 'able to be used again', ['made of recycled plastic', 'free of charge', 'disposable'], 'it contrasts with single-use plastic and presents a practical solution.')],
      qa=[('According to the leaflet, how many plastic cups does the canteen throw away in a year?', 'Over 30,000.'),
          ('Identify two actions the leaflet asks students to take.', 'Any two of: bring a reusable bottle; say "no straw, please"; join the Thursday clean-up; sign up at the eco-club table.'),
          ('Why do you think the writer compares the stack of cups to Marina Bay Sands?', 'It helps readers picture the size of the problem using a famous local building, making the statistic memorable and shocking.')],
      gq='How does the leaflet persuade students that they can make a difference?',
      gqa='The leaflet first shocks readers with a local statistic (900 cups a week) made vivid by the Marina Bay Sands comparison, then reassures them with simple bullet-pointed imperatives. The antithesis "Small changes. Big difference." resolves the worry, and the deadline ("by Friday") creates urgency to act now.',
      write=[('Rewrite the leaflet\'s message as a 60-second assembly speech to Grade 8 students.', 'Indicative content: a hook (question or statistic), spoken features (direct address, repetition), two or three actions, a clear call to action; register suited to peers.'),
             ('Write an email (about 150 words) to the school principal asking for funding for more water fountains, using information from the leaflet.', 'Indicative content: formal greeting; states the problem using the leaflet\'s figures; explains the benefit; makes a polite, specific request; formal sign-off.')],
      summary='The canteen wastes about 900 plastic cups a week (30,000 a year). Students can help by using refillable bottles, refusing straws and joining a weekly clean-up; they should sign up by Friday.',
      theme='the environment and individual action')

    P(id='phonesfree', kind='speech', title='speech by a student council president to her school assembly in Toronto',
      text=("Good morning, everyone. Raise your hand if you checked your phone before breakfast today. (Pause.) Me too.\n"
            "We are the most connected generation in history – and, according to our own school survey, 62 per cent of us say we feel lonely every week. Connected, but alone.\n"
            "I'm not asking you to throw your phone in the lake. I'm asking for one hour. One lunchtime a week, phones in our bags, eyes on each other.\n"
            "Let's try it. Let's talk. Let's remember what our friends' faces look like when they laugh."),
      aud='Fellow students at a school assembly; the speaker includes herself ("Me too", "we") to address her peers as equals.',
      purp='To persuade students to support a weekly phone-free lunchtime by showing that constant connection can make them feel lonely.',
      tone='warm and persuasive', tw=['angry and accusing', 'cold and formal', 'sarcastic'], tonex='humour, inclusive pronouns and a modest request create a warm tone.',
      dev=[('rhetorical question / audience participation', 'Raise your hand if you checked your phone before breakfast today', 'it involves the audience physically and makes them admit the habit, so the problem feels shared', ['statistic', 'simile', 'onomatopoeia']),
           ('statistic', '62 per cent of us say we feel lonely every week', 'evidence from their own school makes the claim credible (logos) and hard to dismiss', ['simile', 'alliteration', 'hyperbole']),
           ('oxymoron / antithesis', 'Connected, but alone.', 'the paradox sums up the problem memorably in three words', ['onomatopoeia', 'simile', 'rhetorical question']),
           ('anaphora (repetition)', 'Let\'s try it. Let\'s talk. Let\'s remember', 'the repeated inclusive imperative builds momentum and unites the audience in action', ['statistic', 'personification', 'onomatopoeia'])],
      struct=[('the humorous concession "I\'m not asking you to throw your phone in the lake"', 'it anticipates an objection and makes the actual request seem small and reasonable'),
              ('the movement from a personal hook to evidence to a call to action', 'it gains attention, proves the problem and then gives the audience something specific to do')],
      vocab=[('connected', 'linked to others through technology', ['physically tied together', 'related by family', 'in agreement'], 'the speaker exploits its double meaning: linked online but not emotionally close.')],
      qa=[('What exactly is the speaker asking her audience to do?', 'To keep phones in their bags for one lunchtime a week and talk to each other.'),
          ('Why does the speaker say "Me too" after the opening question?', 'To show she has the same habit, so she does not seem to be lecturing; it builds trust and a shared identity with her audience.')],
      gq='How does the speaker persuade her audience to try a phone-free lunchtime?',
      gqa=('The speaker builds trust before persuading: the opening show of hands and "Me too" make the habit shared, not shameful (ethos). The school statistic and the paradox "Connected, but alone" give logical and emotional weight. '
           'The humorous concession shrinks the request to "one hour", and the anaphoric "Let\'s..." ending turns agreement into collective action, closing on the emotive image of friends laughing.'),
      write=[('Write a response to the speech for the school newspaper (about 200 words), giving your opinion on the phone-free lunchtime idea.', 'Indicative content: headline; clear opinion; reference to the speaker\'s points (statistic, "Connected, but alone"); one counterargument (e.g. phones help some students feel included); conclusion.')],
      summary='A student leader argues that, although students are highly connected, many feel lonely; she asks them to try one phone-free lunchtime a week to talk face to face.',
      theme='technology and friendship')

    P(id='turtles', kind='news', title='news report from a coastal newspaper in Kenya',
      text=("RECORD TURTLE HATCHING ON WATAMU BEACH\n"
            "More than 1,200 green turtle hatchlings reached the sea from Watamu Beach on Saturday night, the highest number recorded in a single night since monitoring began in 1998.\n"
            "Volunteers from Local Ocean Conservation guarded 14 nests for eight weeks.\n"
            "\"We were on our knees in the sand at 2 a.m., counting,\" said volunteer Amani Mwangi, 17. \"Every single one made it past the crabs.\"\n"
            "Experts warn that rising sand temperatures could reduce numbers in future years."),
      aud='General readers of a regional newspaper, especially people living on the Kenyan coast who care about local wildlife and tourism.',
      purp='To inform readers about a record turtle hatching and the volunteers\' role, while noting a future threat.',
      tone='informative and quietly celebratory', tw=['sarcastic', 'furious', 'despairing'], tonex='factual reporting is lifted by the volunteer\'s excited quotation.',
      dev=[('superlative', 'the highest number recorded in a single night', 'it signals that the event is newsworthy and historic', ['simile', 'onomatopoeia', 'rhetorical question']),
           ('direct quotation', '"We were on our knees in the sand at 2 a.m., counting,"', 'an eyewitness adds human interest and vivid detail to the facts', ['metaphor', 'hyperbole', 'alliteration']),
           ('precise figures', '1,200 ... 14 nests for eight weeks', 'numbers make the report factual and credible', ['personification', 'simile', 'onomatopoeia'])],
      struct=[('the lead paragraph', 'it answers what, where, when and why it matters in one sentence, so readers get the key facts first'),
              ('the inverted pyramid ending with the expert warning', 'less essential but important context comes last, adding balance to the good news')],
      qa=[('Which organisation did the volunteers belong to?', 'Local Ocean Conservation.'),
          ('How long did volunteers guard the nests?', 'For eight weeks.'),
          ('What threat to future hatchings is mentioned?', 'Rising sand temperatures, which could reduce numbers.')],
      vocab=[('monitoring', 'regular checking and recording', ['warning people', 'teaching', 'guarding with weapons'], 'it shows the scientific, long-term nature of the conservation work.')],
      gq='How does the report combine facts and human interest to engage its readers?',
      gqa='The headline and lead give hard facts (1,200 hatchlings, a record since 1998), following the inverted pyramid. The quotation from 17-year-old Amani adds vivid human interest ("on our knees in the sand at 2 a.m.") and celebrates young volunteers. The final expert warning adds balance and a sense of concern for the future.',
      summary='A record 1,200 turtle hatchlings reached the sea at Watamu after volunteers guarded nests for eight weeks; experts warn rising sand temperatures may threaten future numbers.',
      theme='conservation and young people\'s action', facts_op=('Fact: "Volunteers from Local Ocean Conservation guarded 14 nests for eight weeks." Opinion or prediction: "Experts warn that rising sand temperatures could reduce numbers" (a forecast, not yet proved).'))

    P(id='uniform', kind='oped', title='opinion column by a Year 10 student in a school magazine in Melbourne',
      text=("Why I've Changed My Mind About Uniforms\n"
            "In Year 7 I thought school uniform was a prison sentence in polyester. I wanted to wear my own clothes, my own style, my own identity.\n"
            "Then I met Jonah. Jonah's family couldn't afford the brands everyone else wore. On mufti days he 'forgot' and wore his blazer anyway.\n"
            "A uniform doesn't erase who we are. It erases the price tag.\n"
            "Yes, the jumpers are itchy. Yes, the colour is a crime against fashion. But I'd rather be itchy than watch a friend hide."),
      aud='Fellow students, especially those who dislike uniform; the writer speaks as one of them ("In Year 7 I thought...").',
      purp='To persuade readers that school uniform protects less wealthy students from being judged.',
      tone='humorous but sincere', tw=['angry', 'neutral and scientific', 'despairing'], tonex='jokes about itchy jumpers sit alongside a serious, caring point about a friend.',
      dev=[('metaphor', 'a prison sentence in polyester', 'the exaggerated image humorously captures how restrictive uniform felt, and the alliteration makes it memorable', ['simile', 'onomatopoeia', 'statistic']),
           ('anecdote', 'Then I met Jonah', 'a real story about a friend makes the argument personal and emotional (pathos)', ['statistic', 'rhetorical question', 'oxymoron']),
           ('antithesis', 'A uniform doesn\'t erase who we are. It erases the price tag.', 'the balanced contrast reframes the issue: uniform hides wealth, not personality', ['onomatopoeia', 'simile', 'hyperbole']),
           ('concession', 'Yes, the jumpers are itchy.', 'admitting the weak points makes the writer seem fair and honest, which strengthens the argument', ['simile', 'statistic', 'onomatopoeia'])],
      struct=[('the change-of-mind structure (then and now)', 'showing how the writer\'s view changed invites readers who disagree to change their minds too'),
              ('the single-sentence paragraph "A uniform doesn\'t erase who we are. It erases the price tag."', 'isolating the key claim gives it emphasis as the turning point of the column')],
      vocab=[('erase', 'remove completely', ['draw', 'improve', 'reveal'], 'the repetition of "erases" shows exactly what uniform removes – not identity, but signs of money.'),
             ('mufti days', 'days when students can wear their own clothes', ['sports days', 'exam days', 'holidays'])],
      qa=[('Why did Jonah wear his blazer on mufti days?', 'Because his family could not afford brand-name clothes, so he hid this by "forgetting" and wearing uniform.'),
          ('Why is the word \'forgot\' placed in inverted commas?', 'It suggests Jonah did not really forget – he chose to wear uniform to avoid being judged for his clothes.')],
      gq='How does the writer persuade readers to change their minds about school uniform?',
      gqa=('The writer first agrees with the reader ("a prison sentence in polyester"), building trust through humour. The anecdote about Jonah and the scare quotes around "forgot" create sympathy and reveal hidden inequality. '
           'The antithesis "It doesn\'t erase who we are. It erases the price tag" reframes the debate, and the concessions ("Yes, the jumpers are itchy") make the writer seem fair before the emotional final line.'),
      write=[('Write a reply column (about 250 words) arguing that students should be allowed to wear their own clothes, responding to at least two of this writer\'s points.', 'Indicative content: headline; clear counter-stance; addresses the Jonah argument (e.g. a clothing bank or plain dress code could solve inequality); self-expression and cost of uniforms; persuasive devices; conclusion.')],
      summary='The writer once hated uniform, but a friend who could not afford brands changed her mind: uniform hides wealth differences, so it protects students from being judged.',
      theme='identity and fairness')

    P(id='volcano', kind='blog', title='travel blog post by a 15-year-old visiting Iceland',
      text=("Day 4: I Stood Next to a Volcano (and Lived)\n"
            "Posted by @nadia_explores\n"
            "OK, so technically the eruption at Fagradalsfjall had stopped. But the ground was still breathing. Steam curled out of black rock like the earth was exhaling after a long run.\n"
            "Our guide, Sigga, said the lava field was younger than me. I didn't know rocks could be younger than me!!\n"
            "My boots smelled of sulphur (rotten eggs, basically) for two days. Worth it.\n"
            "Drop a 🌋 in the comments if Iceland is on your list!"),
      aud='Other teenagers who follow travel blogs: the handle, casual phrases ("OK, so"), emoji and the comment invitation target young online readers.',
      purp='To entertain and share a personal travel experience, and to build a community of followers.',
      tone='excited and chatty', tw=['formal and serious', 'bitter', 'fearful'], tonex='informal phrases, double exclamation marks and humour create excitement.',
      dev=[('personification', 'the ground was still breathing', 'the volcano seems alive, making the landscape feel powerful and slightly dangerous', ['statistic', 'onomatopoeia', 'rhetorical question']),
           ('simile', 'like the earth was exhaling after a long run', 'it compares the steam to a tired runner\'s breath, giving a vivid, familiar picture', ['metaphor', 'alliteration', 'statistic']),
           ('humorous aside in brackets', '(rotten eggs, basically)', 'the informal explanation makes the blogger sound friendly and funny', ['simile', 'statistic', 'personification']),
           ('hyperbolic title', 'I Stood Next to a Volcano (and Lived)', 'the exaggerated danger hooks readers while the brackets hint at the joke', ['simile', 'onomatopoeia', 'oxymoron'])],
      struct=[('the diary-style title "Day 4"', 'it shows the post is part of a series, encouraging readers to follow the journey'),
              ('ending with an invitation to comment', 'it turns readers into participants and builds an online community')],
      vocab=[('sulphur', 'a yellow chemical element with a strong smell like rotten eggs', ['a type of volcanic rock', 'a kind of steam', 'a hiking boot'])],
      qa=[('Why was the writer surprised by what the guide said?', 'The guide said the lava field was younger than the writer – she had not realised rocks could be so new.'),
          ('Find two features that show this is a blog post rather than a printed travel guide.', 'Any two: the handle "@nadia_explores"; the date-style title "Day 4"; emoji; the invitation to comment; informal language such as "OK, so".')],
      gq='How does the blogger make her experience vivid and entertaining for her readers?',
      gqa='Personification and simile ("the ground was still breathing", "like the earth was exhaling") make the volcano feel alive. Humour – the bracketed "(and Lived)", "(rotten eggs, basically)" – and exclamation marks create a chatty, friendly voice, while the comment invitation and emoji draw readers into a community.',
      write=[('Rewrite the blog post as a short section (about 150 words) of a formal travel guide for families visiting Fagradalsfjall.', 'Indicative content: third-person or impersonal voice; factual information (location, guided tours, safety around steam and gas, smell of sulphur); no emoji or slang; clear, formal register.')],
      summary='A teenage blogger describes visiting a recently erupted volcano in Iceland: steaming rocks, a lava field younger than her and a strong sulphur smell, which she thought was worth it.',
      theme='travel and wonder at nature')

    P(id='library_letter', kind='letter', title='letter from a student to her local council in Manchester',
      text=("Dear Councillor Patel,\n"
            "I am writing to ask you to reconsider the decision to close Levenshulme Library.\n"
            "For many students in my area, the library is the only quiet place to study. My flat has five people and one table. The library has Wi-Fi, printers and Mrs Okafor, who has helped me with every homework project since I was eight.\n"
            "Closing it would save money this year, but it would cost our community far more in the future.\n"
            "I would be grateful if you could meet our youth group to discuss alternatives.\n"
            "Yours sincerely,\nAmira Hassan (age 14)"),
      aud='A local councillor who has power over the decision; the formal salutation and polite requests suit this official audience.',
      purp='To persuade the councillor to reconsider closing the library and to agree to meet the youth group.',
      tone='polite but firm', tw=['angry and rude', 'light-hearted', 'indifferent'], tonex='formal phrases ("I would be grateful") combine with clear, determined arguments.',
      dev=[('personal anecdote', 'My flat has five people and one table.', 'a concrete detail from her life shows why the library matters without exaggeration', ['simile', 'onomatopoeia', 'rhetorical question']),
           ('antithesis', 'would save money this year, but it would cost our community far more in the future', 'the contrast of saving and costing challenges the council\'s financial reasoning', ['simile', 'alliteration', 'personification']),
           ('formal register', 'I would be grateful if you could meet our youth group', 'polite, formal language shows respect and makes the request hard to refuse', ['slang', 'hyperbole', 'onomatopoeia'])],
      struct=[('stating the purpose in the first sentence', 'the busy reader knows immediately what the letter is about'),
              ('ending with a specific request', 'asking for a meeting gives the councillor a clear, achievable action')],
      qa=[('What three things does the library offer, according to the writer?', 'Wi-Fi, printers and the help of Mrs Okafor (as well as a quiet place to study).'),
          ('Why does the writer include her age in the sign-off?', 'To show she is a young person directly affected, which adds emotional weight and shows young people care about the issue.')],
      vocab=[('reconsider', 'think about again and possibly change', ['refuse', 'celebrate', 'announce'], 'it is a polite word that asks for a change of mind without accusing the council of being wrong.')],
      gq='How does the writer make her letter persuasive while remaining polite?',
      gqa='She states her purpose immediately and keeps a formal register ("I would be grateful"), which shows respect. Concrete personal details (five people, one table; Mrs Okafor) give emotional evidence, and the antithesis of saving now but costing more later challenges the council\'s logic. The specific request for a meeting ends on an achievable action.',
      write=[('Write the councillor\'s reply to Amira (about 200 words), either agreeing to meet or explaining why the library must close.', 'Indicative content: formal letter conventions; responds to her specific points (study space, Wi-Fi, Mrs Okafor); explains the council\'s position or proposes a meeting/alternatives; respectful register.')],
      summary='A 14-year-old asks her councillor not to close the local library, explaining that it provides study space, Wi-Fi, printers and a helpful librarian, and asks for a meeting to discuss alternatives.',
      theme='community and access to education')

    P(id='sleepgraph', kind='infographic', title='infographic from a health website for teenagers',
      text=("[Headline in large white letters on dark blue: ARE YOU RUNNING ON EMPTY?]\n"
            "[Icon of a phone battery at 20%: Teenagers need 8–10 hours of sleep a night.]\n"
            "[Bar chart: 7 in 10 teenagers get less than 8 hours on school nights.]\n"
            "[Three icons in a row: a moon, a closed book, a phone with a cross through it – \"Same bedtime. Wind down. Screens off 1 hour before bed.\"]\n"
            "[Small print: Source: national adolescent health survey, 2023.]"),
      aud='Teenagers (the headline asks "Are you...?" and the advice is about school nights); parents and teachers may also read it.',
      purp='To inform teenagers about how much sleep they need and to encourage healthier sleep habits.',
      tone='concerned but friendly', tw=['furious', 'mocking', 'nostalgic'], tonex='the friendly question and simple tips soften the worrying statistic.',
      dev=[('metaphor', 'RUNNING ON EMPTY', 'it compares a tired teenager to a vehicle with no fuel, making the problem easy to understand', ['simile', 'onomatopoeia', 'oxymoron']),
           ('statistic', '7 in 10 teenagers get less than 8 hours', 'it shows the problem is common, so readers may recognise themselves', ['metaphor', 'alliteration', 'hyperbole']),
           ('imperative', 'Screens off 1 hour before bed.', 'a short command gives clear, practical advice', ['rhetorical question', 'simile', 'personification'])],
      struct=[('the progression from problem (headline, statistic) to solution (three tips)', 'readers are first made to care and then shown what to do'),
              ('the source in small print', 'it adds credibility without distracting from the main message')],
      visual='The low phone-battery icon is a symbol teenagers instantly recognise, linking tiredness to something from their daily lives; the dark blue background suggests night, and three simple icons make the advice quick to remember.',
      qa=[('How many hours of sleep do teenagers need, according to the infographic?', '8–10 hours a night.'),
          ('Why might the designer have used a phone battery icon?', 'Teenagers use phones constantly, so a low battery is a familiar symbol of running out of energy; it also links to the advice about screens.')],
      gq='How does the infographic use visual and verbal features to communicate its message quickly?',
      gqa='The rhetorical-question headline and the "running on empty" metaphor hook teenagers. The low-battery icon visualises tiredness in a familiar way, the bar chart proves the problem is widespread, and three simple icons with imperatives give memorable solutions; the source adds credibility.',
      summary='Teenagers need 8–10 hours\' sleep, but 7 in 10 get less than 8 on school nights; they should keep the same bedtime, wind down and switch off screens an hour before bed.',
      theme='health and teenage life')

    P(id='bookreview', kind='review', title='book review on a teen reading website',
      text=("★★★★☆  The Map of Small Things – reviewed by Kai, 14\n"
            "If you like adventure stories with heart, this is for you. Thirteen-year-old Leila finds a hand-drawn map in her late grandfather's coat and follows it across Istanbul.\n"
            "The best part? The city feels alive – spice markets, ferries, rooftop cats. I could almost smell the simit.\n"
            "The middle drags a little (too many clues, not enough danger), but the ending made me text my own grandad.\n"
            "Read it if: you love puzzles, families and food. Skip it if: you need explosions."),
      aud='Teenage readers deciding what to read next; the reviewer is a 14-year-old using a friendly, peer-to-peer voice.',
      purp='To evaluate the novel and help readers decide whether to read it.',
      tone='enthusiastic but balanced', tw=['bitter', 'neutral and technical', 'sarcastic'], tonex='praise is mixed with honest criticism of the middle section.',
      dev=[('sensory detail / listing', 'spice markets, ferries, rooftop cats', 'the list recreates the city\'s variety and shows why the setting is a strength', ['rhetorical question', 'oxymoron', 'statistic']),
           ('rhetorical question', 'The best part?', 'it creates a conversational pause that draws the reader into the reviewer\'s opinion', ['simile', 'statistic', 'personification']),
           ('personal response', 'the ending made me text my own grandad', 'it proves the emotional power of the book through the reviewer\'s real reaction', ['statistic', 'onomatopoeia', 'metaphor'])],
      struct=[('the star rating at the start', 'it gives an instant verdict before the detail'),
              ('the "Read it if / Skip it if" ending', 'it gives clear, balanced advice for different readers')],
      vocab=[('drags', 'moves too slowly and becomes boring', ['pulls something heavy', 'becomes exciting', 'is cut short'])],
      qa=[('What is the reviewer\'s main criticism of the novel?', 'The middle section is slow – too many clues and not enough danger.'),
          ('Which type of reader does the reviewer say should skip the book?', 'Readers who need explosions (non-stop action).')],
      gq='How does the reviewer give a balanced and engaging evaluation of the novel?',
      gqa='The star rating and "Read it if / Skip it if" structure give a clear, balanced verdict. Sensory listing ("spice markets, ferries, rooftop cats") shows the setting\'s strength, the honest criticism ("The middle drags") builds trust, and the personal reaction (texting his grandad) proves the book\'s emotional impact.',
      write=[('Write a review (about 200 words) of a book or film you have enjoyed, using the same conventions as this review.', 'Indicative content: rating; brief spoiler-free summary; at least one strength with an example; one weakness; personal response; recommendation for specific readers.')],
      summary='Kai gives the novel four stars: a girl follows her late grandfather\'s map across Istanbul; the setting and ending are excellent, though the middle is slow.',
      theme='family and adventure')

    P(id='grandmother_kitchen', kind='poem', title='poem by a student poet, "My Grandmother\'s Hands"',
      text=("Her hands are maps of seventy years,\n"
            "rivers of blue beneath brown paper skin.\n"
            "They knead the dough like they are\n"
            "pressing out the war, the boat, the cold.\n"
            "Flour rises like snow in reverse.\n"
            "When she holds mine, I feel the journey –\n"
            "every border folded into her palms."),
      aud='General readers of poetry, perhaps especially young people with grandparents who migrated; the speaker is a grandchild.',
      purp='To celebrate a grandmother and to suggest how her hard past (war, migration) lives on in her hands.',
      tone='loving and reflective', tw=['angry', 'comic', 'indifferent'], tonex='tender images of touch and baking create warmth while hints of war add depth.',
      dev=[('metaphor', 'Her hands are maps of seventy years', 'the hands become a record of her life, suggesting each line tells part of her story', ['simile', 'onomatopoeia', 'alliteration']),
           ('simile', 'They knead the dough like they are / pressing out the war, the boat, the cold', 'the everyday task of baking becomes a way of working through painful memories of migration', ['metaphor', 'personification', 'hyperbole']),
           ('simile (unusual)', 'Flour rises like snow in reverse', 'the surprising image turns the kitchen into a gentle, magical place and echoes "the cold" of her past', ['onomatopoeia', 'alliteration', 'rhetorical question']),
           ('tricolon', 'the war, the boat, the cold', 'three short nouns summarise a whole history of hardship in very few words', ['simile', 'onomatopoeia', 'personification'])],
      struct=[('the final line "every border folded into her palms"', 'it extends the map metaphor from the opening, giving the poem a circular shape and a powerful closing image'),
              ('enjambment across lines 3–4', 'the sentence runs on, mimicking the continuous kneading motion and delaying the revelation of "the war"')],
      vocab=[('knead', 'press and fold dough with the hands', ['need', 'cut', 'cook in an oven'])],
      char='The grandmother is strong, hard-working and resilient: her hands "knead" her painful memories away, and she shares her history through touch rather than words.',
      theme='family, migration and memory',
      gq='How does the poet use imagery to present the grandmother and her past?',
      gqa='The extended map metaphor ("maps of seventy years", "every border folded into her palms") presents her hands as a record of a journey across borders. The simile of kneading out "the war, the boat, the cold" shows her quietly working through trauma, while "Flour rises like snow in reverse" softens the past into warmth. The speaker\'s touch ("When she holds mine") passes the history on.',
      write=[('Write a poem or short descriptive piece (about 120 words) about the hands of someone important to you, using an extended metaphor.', 'Indicative content: a clear extended metaphor; sensory details; hints of the person\'s history or character; a closing image that links back to the opening.')],
      summary='The speaker describes her grandmother\'s hands as maps of her life; while baking, she seems to press out memories of war and migration, and her touch passes that journey on.')

    P(id='rain_haiku', kind='poem', title='sequence of three haiku, "Monsoon Morning"',
      text=("First fat drops of rain –\n"
            "the dusty street holds its breath,\n"
            "then the whole sky falls.\n\n"
            "Children in puddles\n"
            "splash the grey world into gold –\n"
            "school bags overhead.\n\n"
            "Evening. Frogs begin\n"
            "their loud green orchestra; the\n"
            "drains sing all night long."),
      aud='Readers of poetry who may know the monsoon; the vivid, simple images make it accessible to young readers.',
      purp='To capture the arrival of the monsoon in a series of precise, sensory moments.',
      tone='joyful and celebratory', tw=['gloomy', 'angry', 'sarcastic'], tonex='images of children playing and frogs "singing" celebrate the rain.',
      dev=[('personification', 'the dusty street holds its breath', 'the street seems to wait in suspense, building anticipation before the downpour', ['simile', 'onomatopoeia', 'statistic']),
           ('hyperbole', 'the whole sky falls', 'the exaggeration conveys the sudden, overwhelming force of monsoon rain', ['simile', 'alliteration', 'oxymoron']),
           ('metaphor', 'their loud green orchestra', 'the frogs\' croaking becomes music, making the evening feel lively and harmonious', ['simile', 'onomatopoeia', 'rhetorical question']),
           ('colour imagery', 'splash the grey world into gold', 'the change from grey to gold shows how the children\'s joy transforms the scene', ['onomatopoeia', 'statistic', 'personification'])],
      struct=[('the 5-7-5 syllable pattern of each haiku', 'the strict, short form captures single moments, like snapshots'),
              ('the movement from first drops to morning play to evening', 'the sequence follows the passing of a day, showing the monsoon changing life from start to finish')],
      theme='nature and joy', mood='The mood moves from tense anticipation ("holds its breath") to playful joy and finally a noisy, contented night.',
      gq='How does the poet use the haiku form and imagery to capture the arrival of the monsoon?',
      gqa='Each 5-7-5 haiku freezes one moment, like a photograph, and the sequence moves from morning to night. Personification ("holds its breath") builds suspense; hyperbole ("the whole sky falls") shows sudden power; colour imagery ("grey world into gold") and the metaphor of the frogs\' "loud green orchestra" turn the rain into a celebration.',
      write=[('Write a sequence of three haiku about a season or type of weather in your own country, moving from morning to night.', 'Indicative content: three haiku in 5-7-5 form (allow minor variation); each captures one precise image; a sense of time passing; at least one figurative device.')],
      summary='Three haiku follow a monsoon day: the first drops, children splashing joyfully, and frogs and drains "singing" through the night.')

    P(id='newgirl', kind='prose', title='extract from a novel about starting a new school',
      text=("Mei stood at the classroom door clutching a timetable she had folded so many times it was soft as cloth.\n"
            "Twenty-eight faces turned. Someone laughed – not at her, probably, but her cheeks burned anyway.\n"
            "\"There's a seat here,\" said a girl with silver braces and paint on her fingers. She shoved a pile of comics aside. \"I'm Zara. Do you like drawing? Please say yes. Nobody here likes drawing.\"\n"
            "Mei, who had filled three sketchbooks on the plane from Shanghai, almost smiled.\n"
            "\"Yes,\" she said. It was the first word she had spoken all day."),
      aud='Young teenage readers who may have experienced starting somewhere new.',
      purp='To show a character\'s anxiety on her first day and the beginning of a friendship.',
      tone='tense then hopeful', tw=['comic and silly', 'angry', 'cold and detached'], tonex='Mei\'s nerves give way to warmth through Zara\'s friendly chatter.',
      dev=[('simile', 'soft as cloth', 'the timetable has been folded so often that it shows how nervously Mei has been handling it', ['metaphor', 'onomatopoeia', 'hyperbole']),
           ('short sentence', 'Twenty-eight faces turned.', 'the brief sentence captures the sudden, overwhelming attention Mei feels', ['simile', 'rhetorical question', 'personification']),
           ('dialogue', '"Do you like drawing? Please say yes. Nobody here likes drawing."', 'Zara\'s rapid, hopeful questions reveal that she is lonely too, which creates a bond between the girls', ['simile', 'metaphor', 'hyperbole'])],
      struct=[('ending on "It was the first word she had spoken all day."', 'the final line reveals Mei\'s loneliness and makes the single "Yes" a turning point'),
              ('the shift from Mei\'s fear to Zara\'s speech', 'the change in focus moves the extract from isolation to connection')],
      char='Mei is shy and anxious (clutching her timetable, burning cheeks) but creative and quietly hopeful: she has filled three sketchbooks and "almost smiled" when Zara mentions drawing.',
      pov='Third-person limited narration close to Mei: we feel her nerves ("her cheeks burned anyway") and learn her thoughts ("not at her, probably"), so we share her anxiety.',
      vocab=[('clutching', 'holding tightly', ['dropping', 'reading carefully', 'waving'], 'it suggests nerves and a need for something to hold on to.')],
      qa=[('What evidence suggests that Zara also feels lonely?', 'She says "Nobody here likes drawing" and pleads "Please say yes", showing she wants a friend with the same interest.'),
          ('Why does Mei "almost smile"?', 'Because she loves drawing (she filled three sketchbooks on the plane) and realises she may have found a friend.'),
          ('What does the word "probably" in "not at her, probably" suggest about Mei?', 'It shows her insecurity: she is not sure the laughter is not about her, so she feels self-conscious.')],
      theme='friendship and belonging',
      gq='How does the writer present Mei\'s feelings on her first day at a new school?',
      gqa='Point: Mei is presented as anxious and isolated. Evidence: the timetable folded until "soft as cloth" and her "cheeks burned anyway". Explanation: the simile reveals repeated nervous handling and the physical blush shows embarrassment even when she is not sure she is being mocked ("probably"). The short sentence "Twenty-eight faces turned" emphasises sudden attention. Zara\'s chatter about drawing creates hope, and the final line reveals that "Yes" is her first word all day, a turning point towards belonging.',
      write=[('Continue the story (about 250 words) from Zara\'s point of view, showing what she notices about Mei during their first lesson together.', 'Indicative content: first-person or close third-person from Zara; consistent characterisation (chatty, artistic, lonely); details of Mei\'s drawing or shyness; dialogue; a developing friendship.')],
      summary='A nervous girl, Mei, arrives at a new school from Shanghai; a friendly classmate, Zara, invites her to sit down and asks if she likes drawing, and Mei speaks her first word of the day.')

    P(id='lostdog', kind='story', title='extract from a short story set in Cape Town',
      text=("The poster had been on the lamppost for three weeks: MISSING – BRUNO – REWARD. The rain had washed the dog's face into a grey smudge.\n"
            "Thabo passed it every morning. Every morning he told himself it wasn't his business.\n"
            "Then, on Thursday, behind the fish shop, something whined.\n"
            "It was thin, and it was muddy, and one ear stood up like a question mark.\n"
            "Thabo crouched. The dog looked at him. He looked at the poster. He looked at the reward. He thought about his mother's empty purse.\n"
            "\"Come on, Bruno,\" he whispered. \"Let's get you home.\""),
      aud='Teenage readers of short stories.',
      purp='To entertain and to explore a moral choice between self-interest and kindness.',
      tone='tense and tender', tw=['comic', 'furious', 'boastful'], tonex='suspense about Thabo\'s choice combines with a gentle ending.',
      dev=[('repetition', 'Every morning he told himself it wasn\'t his business.', 'it shows Thabo\'s habit of ignoring the poster, so finding the dog becomes a turning point', ['simile', 'onomatopoeia', 'oxymoron']),
           ('simile', 'one ear stood up like a question mark', 'the image makes the dog endearing and hints at the question facing Thabo', ['metaphor', 'personification', 'alliteration']),
           ('short, parallel sentences', 'The dog looked at him. He looked at the poster. He looked at the reward.', 'the slow, repeated pattern shows Thabo weighing his choice and builds suspense', ['simile', 'hyperbole', 'onomatopoeia'])],
      struct=[('the time shift "Then, on Thursday"', 'it breaks the routine and signals the start of the story\'s main event'),
              ('the ambiguous ending', 'we do not learn whether Thabo takes the reward; his gentle words suggest kindness comes first, leaving the reader to judge his motives')],
      char='Thabo is reluctant at first but kind and thoughtful; his family is poor ("his mother\'s empty purse"), so his gentle choice to take Bruno home shows a mixture of need and compassion.',
      theme='kindness and moral choice',
      vocab=[('smudge', 'a blurred, dirty mark', ['a bright photograph', 'a torn corner', 'a pencil drawing'], 'it shows the poster has been there so long the dog has almost been forgotten.')],
      qa=[('How long had the poster been on the lamppost?', 'Three weeks.'),
          ('What detail suggests that Thabo\'s family needs money?', '"his mother\'s empty purse".'),
          ('Why might the writer have chosen to end with Thabo\'s words to the dog rather than with him collecting the reward?', 'It focuses on his kindness rather than the money, leaves his motives open, and gives a warm, quiet ending.')],
      gq='How does the writer build tension around Thabo\'s decision?',
      gqa='Repetition ("Every morning he told himself...") establishes his avoidance, so the shift "Then, on Thursday" signals change. Short, parallel sentences ("The dog looked at him. He looked at the poster. He looked at the reward.") slow the pace as he weighs his options, and the detail of the "empty purse" raises the stakes. The whispered ending resolves the tension with kindness while leaving his motives ambiguous.',
      write=[('Write the next scene (about 250 words), when Thabo knocks on the door of Bruno\'s owner.', 'Indicative content: consistent characterisation; dialogue revealing the owner; a decision about the reward that shows Thabo\'s values; a satisfying or surprising ending.')],
      summary='Thabo walks past a missing-dog poster every day; when he finds the dog behind a fish shop, he thinks about the reward and his family\'s money worries but gently decides to take the dog home.')

    P(id='storm_drama', kind='drama', title='extract from a playscript for young actors',
      text=("SCENE 2. A school hall. Night. Rain hammers on the roof. The lights flicker.\n"
            "ANA: (whispering) Did you hear that?\n"
            "LUCAS: It's the wind. (He doesn't look up from his phone.)\n"
            "ANA: The wind doesn't knock three times.\n"
            "(A knock. Three times. LUCAS slowly lowers his phone.)\n"
            "LUCAS: (forcing a laugh) OK. That's... a very polite wind.\n"
            "(The lights go out. Blackout.)"),
      aud='Young audiences and actors; the suspense and humour suit a school production.',
      purp='To entertain by building suspense, using dialogue and staging, with a touch of humour.',
      tone='suspenseful with comic relief', tw=['peaceful', 'angry', 'romantic'], tonex='flickering lights and knocks build fear, while Lucas\'s joke relieves it briefly.',
      dev=[('stage directions', '(A knock. Three times. LUCAS slowly lowers his phone.)', 'the knock confirms Ana\'s fear and Lucas\'s slow movement shows his growing fear without words', ['soliloquy', 'aside', 'monologue']),
           ('humour / comic relief', 'That\'s... a very polite wind.', 'Lucas\'s nervous joke releases tension briefly and reveals he is scared', ['dramatic irony', 'monologue', 'foreshadowing']),
           ('pathetic fallacy', 'Rain hammers on the roof. The lights flicker.', 'the stormy setting reflects and increases the characters\' unease', ['hyperbole', 'aside', 'oxymoron'])],
      struct=[('ending the scene with a blackout', 'the sudden darkness creates a cliffhanger, leaving the audience in suspense'),
              ('the contrast between Ana and Lucas', 'Ana\'s alertness and Lucas\'s dismissiveness create conflict and let the audience share the shift in Lucas\'s feelings')],
      char='Lucas acts unbothered (he "doesn\'t look up from his phone") but is secretly afraid: he "slowly lowers his phone" and "forc[es] a laugh". Ana is observant and anxious.',
      staging='Lighting: flickering lights, then a sudden blackout for maximum shock. Sound: a loud rain effect and three sharp knocks from offstage. Blocking: Ana close to the door, Lucas sitting far away on the floor, so the knock makes him turn towards it.',
      theme='fear and the unknown',
      gq='How does the playwright use dialogue and stage directions to build suspense?',
      gqa='The opening stage directions (rain "hammers", lights "flicker") set an unsettling atmosphere. Ana\'s whispered question and her line "The wind doesn\'t knock three times" raise fear, which the stage direction immediately confirms. Lucas\'s forced joke ("a very polite wind") gives comic relief that ironically shows his fear, and the final blackout leaves the audience on a cliffhanger.',
      write=[('Write the next half-page of the playscript (about 200 words) after the blackout, using correct playscript conventions.', 'Indicative content: character names, dialogue, stage directions in brackets for lighting, sound and movement; maintains suspense or offers a twist (e.g. a caretaker or a friend); consistent characterisation.')],
      summary='Two students in a dark school hall during a storm hear three knocks; Lucas, who pretended not to care, makes a nervous joke before the lights go out.')

    P(id='nobel_mum', kind='memoir', title='memoir extract by a writer remembering her first day in a new country',
      text=("I was nine when we arrived in Oslo in January. I had never seen snow, and I had never been so cold that my teeth hurt.\n"
            "My mother bought me a red coat from a charity shop. It was two sizes too big. 'You will grow into it,' she said, and she was right, though not in the way she meant.\n"
            "That coat went everywhere with me – to my first Norwegian lesson, to my first sleepover, to the school where nobody could say my name.\n"
            "I still have it. It fits now. So does the city."),
      aud='Adult and teenage readers interested in migration and growing up; the reflective adult narrator invites thoughtful reading.',
      purp='To recall and reflect on the experience of arriving in a new country as a child and growing to belong.',
      tone='reflective and gently hopeful', tw=['furious', 'comic', 'bitter'], tonex='the adult narrator looks back calmly, with quiet pride in having adapted.',
      dev=[('symbolism', 'a red coat from a charity shop. It was two sizes too big.', 'the oversized coat symbolises the new life that she had to grow into', ['onomatopoeia', 'statistic', 'rhetorical question']),
           ('double meaning', '\'You will grow into it,\' ... though not in the way she meant', 'the narrator reveals that she grew into a new identity, not just a coat', ['simile', 'onomatopoeia', 'alliteration']),
           ('parallel short sentences', 'It fits now. So does the city.', 'the matching endings link the coat and the city, showing she now belongs', ['simile', 'hyperbole', 'personification'])],
      struct=[('the list of places the coat went', 'it compresses years of experience into one sentence, showing gradual adaptation'),
              ('the shift to present tense at the end', 'it moves from memory to the present, showing the lasting result of the experience')],
      context='The writer was a nine-year-old migrant arriving in Norway in winter; the cold, the new language and the name nobody could pronounce show the challenges of migration.',
      theme='identity, migration and belonging',
      gq='How does the writer use the red coat to show her changing sense of belonging?',
      gqa='The coat is a symbol: "two sizes too big" suggests the new country first felt too large and unfamiliar. Her mother\'s words gain a double meaning ("not in the way she meant") as the narrator grows into a new identity. The list of places shows gradual adaptation, and the final parallel sentences "It fits now. So does the city." link coat and country, showing she now belongs.',
      write=[('Write a memoir-style paragraph (about 200 words) about an object that reminds you of a time of change in your life.', 'Indicative content: first-person retrospective voice; a symbolic object described in detail; a specific memory; reflection on what it means now; a closing line that links past and present.')],
      summary='A writer recalls arriving in Oslo aged nine; her mother bought her a coat that was too big, and over time she grew into both the coat and her new life in the city.')

    P(id='hiking_diary', kind='diary', title='diary entry by a 13-year-old on a school expedition in the Scottish Highlands',
      text=("Wednesday 14 May\n"
            "Today was the WORST and maybe the BEST day of my life.\n"
            "We walked 18 km in the rain. My boots filled with water like two buckets. Leo's map blew into a loch. We argued for twenty minutes about which way was north.\n"
            "Then the clouds split open and there it was: the whole valley, gold and green, with a rainbow sitting on it like a crown.\n"
            "Nobody said anything for ages. Even Leo stopped complaining.\n"
            "Tomorrow: 22 km. Help."),
      aud='Primarily the writer herself (a private diary), though readers can enjoy its honesty and humour.',
      purp='To record and reflect on the day\'s experiences and feelings.',
      tone='honest and humorous', tw=['formal', 'sinister', 'indifferent'], tonex='exaggeration and the final "Help." show humour, while the valley moment is sincere.',
      dev=[('oxymoron / contradiction', 'the WORST and maybe the BEST day of my life', 'it hooks the reader and sums up the mixed experience of hardship and reward', ['simile', 'statistic', 'onomatopoeia']),
           ('simile', 'My boots filled with water like two buckets', 'the comic exaggeration shows how miserable and wet the walk was', ['metaphor', 'personification', 'alliteration']),
           ('simile', 'a rainbow sitting on it like a crown', 'the regal image makes the valley seem magical and rewarding after the struggle', ['metaphor', 'onomatopoeia', 'hyperbole']),
           ('minor sentence', 'Help.', 'the one-word ending is a comic understatement of her dread at tomorrow\'s longer walk', ['simile', 'rhetorical question', 'statistic'])],
      struct=[('the turning point "Then the clouds split open"', 'it divides the entry into struggle and reward, mirroring the "worst" and "best" of the opening'),
              ('the date and first-person present reflection', 'they show the diary\'s private, immediate voice')],
      theme='perseverance and the reward of effort',
      qa=[('How far did the group walk on Wednesday?', '18 km.'),
          ('What happened to Leo\'s map?', 'It blew into a loch.'),
          ('Why did "nobody say anything for ages"?', 'They were amazed by the beautiful view of the valley and rainbow after the difficult walk.')],
      gq='How does the writer show that the day was both the worst and the best?',
      gqa='The opening contradiction sets up the two halves. Comic similes ("like two buckets") and the lost map show the misery of the walk, while the turning point ("Then the clouds split open") introduces a magical image of the valley with "a rainbow ... like a crown". The silence that follows shows awe, and "Help." ends with humour.',
      write=[('Rewrite the diary entry as a short report (about 150 words) for the school newsletter about the expedition.', 'Indicative content: headline; third-person or "we" voice; facts (distance, weather, location); a quotation from a student; formal or semi-formal register; no private feelings in diary style.')],
      summary='On a long, wet 18 km walk the group lost their map and argued, but when the clouds cleared they saw a stunning valley with a rainbow; tomorrow they must walk 22 km.')

    P(id='robotdog', kind='ad', title='advertisement for a robot pet, posted on a technology website',
      text=("[Image: a silver robot puppy curled on the lap of a smiling elderly man; sunlight through a window.]\n"
            "MEET PIXEL. HE NEVER NEEDS A WALK. HE NEVER FORGETS YOUR BIRTHDAY.\n"
            "Powered by AI, Pixel learns your routines, reminds you of medicines and plays your favourite songs.\n"
            "\"I talk to him every morning,\" says Harold, 81, from Leeds.\n"
            "Companionship, reinvented. Order today – free delivery."),
      aud='Older people who live alone and their adult children who might buy it for them; the elderly man in the image and the medicine reminders suggest this.',
      purp='To persuade readers that the robot dog can provide companionship and practical help, and to make them order it.',
      tone='warm and reassuring', tw=['sinister', 'mocking', 'angry'], tonex='the sunlit image and gentle testimonial create comfort.',
      dev=[('anaphora (repetition)', 'HE NEVER NEEDS A WALK. HE NEVER FORGETS YOUR BIRTHDAY.', 'the repeated "never" stresses the robot\'s advantages over a real pet or busy relatives', ['simile', 'statistic', 'onomatopoeia']),
           ('testimonial', '"I talk to him every morning," says Harold, 81', 'a real-sounding customer makes the product trustworthy and emotional', ['statistic', 'metaphor', 'alliteration']),
           ('slogan', 'Companionship, reinvented.', 'the short, memorable phrase presents technology as a fresh answer to loneliness', ['rhetorical question', 'simile', 'onomatopoeia'])],
      struct=[('the progression from headline to features to testimonial to call to action', 'it moves from curiosity to information, trust and finally purchase')],
      visual='The puppy curled on the man\'s lap and the sunlight suggest comfort, warmth and affection, hiding the fact that the "pet" is a machine.',
      read='One reader might see a caring solution to loneliness; a more critical reader might find it sad that a machine replaces human visits, and notice the advert implies families "forget birthdays".',
      gq='How does the advertisement present the robot as a comforting companion?',
      gqa='The sunlit image of the puppy on an old man\'s lap borrows the warmth of a real pet. The anaphora "HE NEVER..." lists advantages, the testimonial from Harold, 81, gives emotional proof, and the slogan "Companionship, reinvented" presents technology as the answer to loneliness. A critical reader may notice that it quietly replaces human contact.',
      summary='The advert promotes Pixel, an AI robot puppy that needs no walks, remembers routines and medicines and keeps lonely older people company.',
      theme='technology and loneliness')

    P(id='floodnews', kind='news', title='news report from an online news site in Pakistan',
      text=("TEENAGERS' APP HELPS RESCUERS REACH FLOOD FAMILIES\n"
            "A free app built by three students from Lahore has helped rescue teams locate more than 400 families cut off by floods in Sindh province this week.\n"
            "The app, called Pukaar (\"Call\"), lets users share their location and needs even with a weak signal.\n"
            "\"We built it in a weekend,\" said co-founder Hira Baig, 16. \"We didn't sleep much.\"\n"
            "Rescue coordinator Imran Shah called the app \"a lifeline\", but warned that thousands of people still have no phone access at all."),
      aud='General readers of an online news site, nationally and internationally.',
      purp='To inform readers about a student-built app that helped flood rescues, and its limits.',
      tone='informative and positive', tw=['satirical', 'romantic', 'despairing'], tonex='factual reporting highlights an inspiring achievement while staying balanced.',
      dev=[('quotation from an expert', '"a lifeline"', 'an authority\'s metaphor confirms the app\'s value and makes it vivid', ['simile', 'hyperbole', 'onomatopoeia']),
           ('quotation from a young founder', '"We built it in a weekend ... We didn\'t sleep much."', 'it adds human interest and shows the students\' dedication with modest humour', ['statistic', 'personification', 'rhetorical question']),
           ('precise figure', 'more than 400 families', 'the number shows the scale of the impact and makes the report credible', ['metaphor', 'simile', 'personification'])],
      struct=[('the inverted pyramid', 'the most important facts come first (who, what, where), followed by detail and quotations, and a qualification at the end'),
              ('ending with the warning about phone access', 'it balances the positive story with a reminder of a wider problem')],
      qa=[('What does the app\'s name mean in English?', '"Call".'),
          ('What limitation of the app does the rescue coordinator mention?', 'Thousands of people have no phone access at all, so they cannot use it.')],
      facts_op='Fact: "has helped rescue teams locate more than 400 families". Opinion: Imran Shah\'s description of the app as "a lifeline" (a judgement, attributed to him).',
      gq='How does the report present the students and their app?',
      gqa='The headline and lead present the app as effective, with the figure of 400 families as evidence. The quotation from 16-year-old Hira adds human interest and modesty, and the expert\'s metaphor "a lifeline" gives authority. The final warning keeps the report balanced and objective.',
      summary='Three Lahore students built a free app, Pukaar, in one weekend; it has helped rescuers find over 400 flood-hit families, though many people still lack phone access.',
      theme='young people, technology and disaster relief')

    P(id='museum_site', kind='website', title='home page of a science museum in Mexico City',
      text=("[Banner: a giant animated dinosaur skeleton lifts its head as the page loads.]\n"
            "UNIVERSUM KIDS ZONE  |  Visit  |  Exhibitions  |  Schools  |  Tickets\n"
            "BIG QUESTIONS. HANDS-ON ANSWERS.\n"
            "▶ Touch a meteorite 4.5 billion years old.\n"
            "▶ Build a robot that dances.\n"
            "▶ Stand inside a tornado (don't worry – it's only wind!).\n"
            "[Button: BOOK YOUR SCHOOL TRIP]  [Button: Español / English]"),
      aud='Teachers planning school trips and young visitors; the "Kids Zone", school-trip button and playful tone address both.',
      purp='To inform visitors about exhibitions and persuade schools and families to book a visit.',
      tone='playful and inviting', tw=['solemn', 'threatening', 'bored'], tonex='exciting verbs and a joke in brackets make the museum sound fun.',
      dev=[('antithesis', 'BIG QUESTIONS. HANDS-ON ANSWERS.', 'the balanced slogan promises that serious science will be fun and active', ['onomatopoeia', 'simile', 'rhetorical question']),
           ('imperative verbs', 'Touch ... Build ... Stand', 'commands invite physical action, emphasising interactive learning', ['simile', 'statistic', 'onomatopoeia']),
           ('humorous reassurance', '(don\'t worry – it\'s only wind!)', 'the joke removes fear and adds a friendly voice', ['statistic', 'metaphor', 'alliteration'])],
      struct=[('the navigation menu and buttons', 'they let different users go straight to what they need, typical of web pages'),
              ('the bulleted list with arrow symbols', 'it makes the attractions easy to scan quickly on a screen')],
      visual='The animated dinosaur banner grabs attention immediately and shows that this is a lively, modern museum; the language button shows it welcomes international visitors.',
      gq='How does the web page encourage young people and teachers to visit the museum?',
      gqa='The animated dinosaur banner and the antithetical slogan "BIG QUESTIONS. HANDS-ON ANSWERS." promise exciting, active learning. Imperative verbs list memorable experiences, the bracketed joke adds warmth, and the menu and "BOOK YOUR SCHOOL TRIP" button make booking easy for teachers.',
      summary='The museum\'s web page advertises interactive exhibits – a 4.5-billion-year-old meteorite, robot building and a tornado chamber – and invites schools to book trips.',
      theme='learning through experience')

    P(id='fastfashion_poster', kind='poster', title='campaign poster from a youth environmental group',
      text=("[Image: a mountain of discarded clothes in a desert; a single price tag in the foreground reads \"€4.99\".]\n"
            "WORN ONCE. THROWN AWAY. STILL HERE IN 200 YEARS.\n"
            "The world buys about 80 billion new garments a year.\n"
            "Before you buy, ask: Do I need it? Will I wear it 30 times?\n"
            "#ThinkBeforeYouThread  –  Fashion Forward Youth Network"),
      aud='Young consumers who buy cheap fashion; the hashtag and social campaign style target teenagers and young adults.',
      purp='To persuade young people to buy fewer clothes and think about the environmental cost of fast fashion.',
      tone='serious and challenging', tw=['playful', 'romantic', 'indifferent'], tonex='blunt short sentences and a shocking image create a serious tone.',
      dev=[('tricolon', 'WORN ONCE. THROWN AWAY. STILL HERE IN 200 YEARS.', 'three short statements tell the life story of a garment and end on a shocking time-scale', ['simile', 'onomatopoeia', 'personification']),
           ('statistic', 'about 80 billion new garments a year', 'the enormous number shows the scale of the problem', ['metaphor', 'simile', 'alliteration']),
           ('rhetorical questions', 'Do I need it? Will I wear it 30 times?', 'they give readers a practical test to use before buying', ['statistic', 'hyperbole', 'simile']),
           ('pun', '#ThinkBeforeYouThread', 'the play on "think before you tread" makes the message witty and shareable', ['oxymoron', 'statistic', 'simile'])],
      struct=[('the movement from shocking image to statistic to personal questions', 'it moves from the global problem to the individual reader\'s next decision')],
      visual='The cheap price tag in the foreground contrasts with the mountain of clothes behind, showing that a low price hides an enormous environmental cost; the desert setting suggests waste dumped far from shoppers.',
      gq='How does the poster challenge young people\'s attitudes to buying clothes?',
      gqa='The image juxtaposes a tiny €4.99 price tag with a mountain of waste, revealing hidden costs. The tricolon traces a garment\'s short use and long afterlife, and the statistic shows global scale. Rhetorical questions give a personal test, and the punning hashtag makes the campaign memorable and shareable.',
      summary='The poster shows a mountain of discarded clothes to argue that cheap fashion is worn briefly but lasts centuries as waste; it asks young people to buy only what they will wear often.',
      theme='consumerism and the environment')

    P(id='interview_chef', kind='interview', title='interview from a teen magazine with a young chef in Lima',
      text=("At 16, Valentina Rojas runs a weekend food stall in Lima that sells out in two hours. We asked her how.\n"
            "Q: Where did you learn to cook?\n"
            "A: My abuela's kitchen. She never measured anything. She'd say, 'Cook until it smells like home.'\n"
            "Q: What's the hardest part?\n"
            "A: Waking up at 4 a.m. to buy fish. And being taken seriously. People ask where my parents are.\n"
            "Q: Advice for other teens?\n"
            "A: Start small. Burn things. Try again."),
      aud='Teenage readers of a lifestyle magazine, especially those interested in food or starting their own projects.',
      purp='To inform and inspire readers by presenting a young entrepreneur in her own words.',
      tone='lively and inspiring', tw=['gloomy', 'sarcastic', 'formal and distant'], tonex='Valentina\'s direct, humorous answers give energy and encouragement.',
      dev=[('direct quotation of a family saying', '\'Cook until it smells like home.\'', 'it reveals the warmth and tradition behind her cooking', ['statistic', 'oxymoron', 'onomatopoeia']),
           ('tricolon of imperatives', 'Start small. Burn things. Try again.', 'short commands give memorable, encouraging advice that accepts failure as part of learning', ['simile', 'metaphor', 'statistic']),
           ('hook in the introduction', 'sells out in two hours', 'the impressive fact makes readers curious about her success', ['simile', 'personification', 'onomatopoeia'])],
      struct=[('the question-and-answer format', 'it lets Valentina speak directly, making her seem real and approachable'),
              ('the introduction in the magazine\'s voice', 'it frames the interview and explains why readers should care')],
      qa=[('What two difficulties does Valentina mention?', 'Waking up at 4 a.m. to buy fish, and not being taken seriously because of her age.'),
          ('What does Valentina\'s advice suggest about her attitude to failure?', 'She sees mistakes ("Burn things") as a normal part of learning; persistence matters most.')],
      gq='How does the interview present Valentina as an inspiring role model?',
      gqa='The introduction hooks readers with her success ("sells out in two hours"). The Q&A format lets her speak directly; her grandmother\'s saying reveals warmth and heritage, her honest answer about not being taken seriously shows resilience, and the closing tricolon of imperatives gives memorable, encouraging advice.',
      write=[('Write a set of five interview questions and answers (about 250 words) with a young person in your community who has achieved something unusual.', 'Indicative content: an introduction that hooks the reader; open questions; answers in a distinct voice with quotations; a logical order ending with advice or future plans.')],
      summary='Sixteen-year-old Valentina runs a successful food stall in Lima; she learned to cook from her grandmother, struggles with early mornings and not being taken seriously, and advises others to start small and keep trying.',
      theme='ambition and heritage')

    pr = K.pair
    pr('newgirl', 'phonesfree', 'Compare how the two texts present the importance of real connection between young people.',
       'Both texts value face-to-face connection. Text A dramatises it through one moment: Mei\'s isolation ("Twenty-eight faces turned") ends when Zara offers a seat and a shared interest, and the single word "Yes" marks belonging. '
       'Text B argues for it directly: the paradox "Connected, but alone" and the school statistic show loneliness, and anaphoric "Let\'s..." imperatives call for action. Difference: the novel shows through character and dialogue (implicit), the speech persuades through rhetoric and evidence (explicit); both end on an image of friendship.',
       sim='both suggest that loneliness is overcome by real, face-to-face contact – Zara\'s offer of a seat and the speaker\'s "eyes on each other".',
       diff='Text A shows connection through a story and dialogue, while Text B argues for it with a statistic and direct persuasion.')
    pr('grandmother_kitchen', 'nobel_mum', 'Compare how the two texts use objects to explore memory and migration.',
       'Text A uses the grandmother\'s hands (an extended map metaphor, "every border folded into her palms") to show a history of war and migration carried in the body; Text B uses the red coat as a symbol of a new life the narrator grows into ("It fits now. So does the city."). '
       'Both are told by family members, but the poem looks at someone else\'s past with tenderness, while the memoir reflects on the writer\'s own adaptation. The poem uses compressed imagery and enjambment; the memoir uses anecdote, chronology and a shift to the present tense.',
       sim='both use an object or body part as a symbol of a migrant\'s journey – hands as "maps" and a coat that is "two sizes too big".',
       diff='Text A is a poem looking at a grandmother\'s painful past, while Text B is a memoir reflecting on the writer\'s own growing sense of belonging.')
    pr('volcano', 'hiking_diary', 'Compare how the two writers present an encounter with the natural world.',
       'Both are first-person, informal, humorous accounts of a challenging outdoor experience. Text A (blog) addresses a public audience with emoji, a handle and a comment invitation, and uses personification ("the ground was still breathing") to make the volcano alive. '
       'Text B (private diary) moves from comic misery ("like two buckets") to awe at the valley ("a rainbow ... like a crown"). Difference: the blog performs for followers; the diary records honest private feelings, including a moment of silent wonder.',
       sim='both writers use humour and vivid similes to describe nature – "like the earth was exhaling" and "like a crown".',
       diff='Text A is written for public followers (handle, emoji, comments), while Text B is a private diary that records the writer\'s honest feelings.')
    pr('fastfashion_poster', 'plasticfree', 'Compare how the two texts persuade young people to change their habits to protect the environment.',
       'Both use shocking statistics (80 billion garments; 900 cups a week), short imperatives or questions, and a hashtag or sign-up call to action. Text A is more confrontational: the image of a clothes mountain and the tricolon "WORN ONCE. THROWN AWAY. STILL HERE IN 200 YEARS." create guilt. '
       'Text B is more upbeat and local: exclamation marks, a Marina Bay Sands comparison and the reassuring antithesis "Small changes. Big difference." Text A targets global consumer habits; Text B targets a school community with concrete actions.',
       sim='both use a striking statistic to show the scale of waste and end with a call to action.',
       diff='Text A uses a shocking image and a serious tone to create guilt, while Text B uses an enthusiastic tone and simple, local actions.')
    pr('lostdog', 'robotdog', 'Compare how the two texts present the relationship between people and animals (or animal-like companions).',
       'Text A presents a real, vulnerable dog ("thin ... muddy") whose rescue tests Thabo\'s kindness; the relationship involves responsibility and moral choice. Text B presents a robot dog as a convenient companion that "never needs a walk", selling comfort through a testimonial and a warm image. '
       'Text A uses narrative suspense and symbolism (the "question mark" ear); Text B uses persuasive anaphora and a slogan. A critical comparison: the story values care and effort, while the advert removes effort – raising questions about what companionship means.',
       sim='both present an animal or animal-like companion that brings comfort to a person who needs it.',
       diff='in Text A the dog needs care from Thabo, whereas in Text B the robot is sold as a pet that needs nothing and does the caring.')
    pr('trainers', 'interview_chef', 'Compare how the two texts present young people\'s determination to succeed.',
       'Text A (advert) dramatises determination through anaphora ("THEY SAID TOO YOUNG...") and a defiant reply, using it to sell shoes; Text B (interview) lets a real young chef describe hardships (4 a.m. starts, not being taken seriously) and ends with the tricolon "Start small. Burn things. Try again." '
       'Both show young people proving doubters wrong. Difference: the advert\'s determination is an image constructed for profit; the interview\'s is grounded in specific detail and modest humour, making it more convincing.',
       sim='both show a young person ignoring people who doubt them – "THEY SAID TOO YOUNG" and "People ask where my parents are".',
       diff='Text A uses determination to sell a product, while Text B presents a real person\'s experience in her own words.')
