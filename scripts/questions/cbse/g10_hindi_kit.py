"""Hindi engine for cbse-g10-hindi (क्षितिज-2, कृतिका-2) and cbse-g12-hindi (आरोह-2, वितान-2).

A subject module describes each chapter as a dict (see g10_hindi_a.py) and calls `build`. Subtopic specs:
    LIT(...)      पाठ-आधारित subtopic: facts, true/false statements, A-R tuples, written (wr), think, long
    GRAM(engine)  व्याकरण subtopic (engines in g10_hindi_gram.ENGINES)
    WRITE(forms)  रचना / अभिव्यक्ति subtopic (forms in WRITERS below, topics given in the spec)
    APATHIT()     अपठित subtopic (uses the subject's passage themes)
Chapter-level data: vocab [(शब्द, अर्थ)], extracts [(st, text, [(q, a, [wrong]) | (q, a)])], writing prompts.

Copyright rule: every passage, extract and verse here is original writing (or a paraphrase in our own words of a
well-known moment); text questions use only well-known facts of each chapter (author, characters, events, theme).
Reuses the validated class 8 helpers in g8_hindi_lib.py (imported, not edited).
"""
from __future__ import annotations

import random
import re

from qbank import F, Builder, mcq, onorm
from g8_hindi_lib import har, shuffled, opts_line, ROMAN, Cycler, person, ge, GIRLS, BOYS, CITIES, SCHOOLS, table_set

LETTERS = ['क', 'ख', 'ग', 'घ']
_CYC: dict = {}


def cyc(key: str) -> Cycler:
    return _CYC.setdefault(key, Cycler(key))


def need(c):
    if not c:
        raise ValueError('not enough data')


def LIT(**kw):
    return dict(kind='lit', **kw)


def GRAM(engine, **kw):
    return dict(kind='gram', engine=engine, **kw)


def WRITE(*forms, **kw):
    return dict(kind='write', forms=forms, **kw)


def APATHIT(**kw):
    return dict(kind='apathit', **kw)


# ---------------------------------------------------------------- basic item generators

def g_fact(rows):
    """rows: (q, a, [wrong...], key?)"""
    def g(r):
        row = r.choice(rows)
        q, a, w = row[:3]
        key = row[3] if len(row) > 3 else f'सही उत्तर: {a}।'
        w = r.sample(list(w), 3) if len(w) > 3 else list(w)
        return mcq(q, a, w, key, r)
    return g


TRUE_LEADS = ['"{t}" के संदर्भ में कौन-सा कथन सही है?', '"{t}" के आधार पर सही कथन चुनिए।',
              '"{t}" के विषय में निम्नलिखित में से कौन-सा कथन उचित है?']
FALSE_LEADS = ['"{t}" के संदर्भ में कौन-सा कथन सही नहीं है?', '"{t}" के आधार पर असत्य कथन चुनिए।',
               '"{t}" के विषय में निम्नलिखित में से कौन-सा कथन उचित नहीं है?']


def g_true(ref, true, false):
    def g(r):
        need(len(false) >= 3)
        t = r.choice(true)
        return mcq(r.choice(TRUE_LEADS).format(t=ref), t, r.sample(false, 3), f'सही कथन: "{t}" शेष कथन पाठ के विपरीत हैं।', r)
    return g


def g_false(ref, true, false):
    def g(r):
        need(len(true) >= 3)
        f = r.choice(false)
        return mcq(r.choice(FALSE_LEADS).format(t=ref), f, r.sample(true, 3), f'"{f}"—यह कथन पाठ के अनुसार सही नहीं है; शेष तीनों सही हैं।', r)
    return g


def g_ar(tuples):
    """A-R items from (A, A_false, R, R_false, why[, unrelated true R]) tuples."""
    def g(r):
        t = r.choice(tuples)
        A, Af, R, Rf, why = t[:5]
        codes = ['a']
        if Rf:
            codes.append('c')
        if Af:
            codes.append('d')
        if len(t) > 5 and t[5]:
            codes.append('b')
        code = r.choice(codes)
        if code == 'a':
            return har(A, R, 'a', f'दोनों कथन सही हैं और कारण, अभिकथन की सही व्याख्या करता है: {why}')
        if code == 'c':
            return har(A, Rf, 'c', f'अभिकथन सही है, पर कारण गलत है; वास्तव में—{R}')
        if code == 'd':
            return har(Af, R, 'd', f'अभिकथन गलत है (सही कथन: {A}); कारण सही है।')
        return har(A, t[5], 'b', f'दोनों कथन सही हैं, पर कारण अभिकथन की व्याख्या नहीं करता। अभिकथन का आधार: {why}')
    return g


def g_wr(pairs, words='25-30', marks=2, think=False):
    def g(r):
        q, a = r.choice(pairs)
        lead = 'तर्कसंगत उत्तर स्वीकार्य। मूल्य-बिंदु: ' if think else 'मूल्य-बिंदु: '
        return {'stem': f'{q} (लगभग {words} शब्दों में)', 'answer': a,
                'key': f'{lead}{a} ({marks} अंक: विषय-वस्तु {marks - 1}, भाषा 1)', 'marks': marks}
    return g


def g_long(pairs, words, marks):
    def g(r):
        q, a = r.choice(pairs)
        return {'stem': f'{q} (लगभग {words} शब्दों में)', 'answer': a,
                'key': f'मूल्य-बिंदु: {a} ({marks} अंक: विषय-वस्तु {marks - 1}, भाषा और प्रस्तुति 1)', 'marks': marks, 'minutes': marks + 3,
                'gap': 'G5'}
    return g


def wr_set(pairs, k, each, words, head=None):
    """k written questions as one item (पाठ्यपुस्तक खंड), `each` marks per part."""
    def g(r):
        need(len(pairs) >= k)
        pick = r.sample(pairs, k)
        h = head or f'निम्नलिखित प्रश्नों के उत्तर लगभग {words} शब्दों में लिखिए।'
        lines = [h] + [f'({ROMAN[i]}) {q}' for i, (q, _) in enumerate(pick)]
        ans = ' '.join(f'({ROMAN[i]}) {a}' for i, (_, a) in enumerate(pick))
        return {'stem': '\n'.join(lines), 'answer': ans,
                'key': f'प्रत्येक भाग {each} अंक (विषय-वस्तु {each - 1}, भाषा 1); कुल {k * each} अंक। {ans}', 'marks': k * each,
                'minutes': k * (each + 1)}
    return g


def mcq_block(rows, k, head):
    """k MCQs from rows (q, a, [wrong], key?) as one item."""
    def g(r):
        need(len(rows) >= k)
        pick = r.sample(rows, k)
        lines, ans = [head], []
        for i, row in enumerate(pick):
            q, a, w = row[:3]
            opts, L = shuffled(r, a, w)
            lines.append(f'({ROMAN[i]}) {q}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[i]}) ({L}) {a}')
        return {'stem': '\n'.join(lines), 'answer': '; '.join(ans),
                'key': f'प्रत्येक सही विकल्प 1 अंक (कुल {k} अंक)। ' + '; '.join(ans) + '।', 'marks': k, 'minutes': k + 1}
    return g


def jumble(s: str, r: random.Random):
    w = s.rstrip('।?!').split()
    if not 6 <= len(w) <= 18:
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


def g_jumble(statements):
    def g(r):
        s = r.choice(statements)
        j = jumble(s, r)
        need(j)
        return {'stem': f'निम्नलिखित वाक्यांशों को सही क्रम में लगाकर पाठ से संबंधित सार्थक वाक्य बनाइए:\n{j}', 'answer': s,
                'key': f'"{s}" (1 अंक; समान अर्थ वाला कोई अन्य शुद्ध क्रम भी स्वीकार्य)', 'marks': 1}
    return g


def g_vocab_mcq(words, title):
    def g(r):
        w = r.choice(words)
        others = [x for x in words if x is not w]
        need(len(others) >= 3)
        ds = [x[1] for x in r.sample(others, 3)]
        stem = r.choice([f'"{title}" पाठ में प्रयुक्त शब्द "{w[0]}" का अर्थ है—', f'"{w[0]}" शब्द का सही अर्थ चुनिए।',
                         f'पाठ के संदर्भ में "{w[0]}" का अर्थ क्या है?'])
        return mcq(stem, w[1], ds, f'"{w[0]}" का अर्थ है—{w[1]}।', r)
    return g


def g_vocab_use(words):
    def g(r):
        w = r.choice(words)
        return {'stem': f'"{w[0]}" शब्द का अर्थ लिखकर उसका अपने वाक्य में प्रयोग कीजिए।', 'answer': f'अर्थ: {w[1]}। (उचित वाक्य-प्रयोग)',
                'key': f'अर्थ "{w[1]}" के लिए 1 अंक; अर्थ स्पष्ट करने वाले शुद्ध वाक्य के लिए 1 अंक।', 'marks': 2}
    return g


# ---------------------------------------------------------------- extracts (original passages on the chapter's theme)

def _ex_head(ch, label, real=False, many=False):
    q = 'पूछे गए प्रश्नों के उत्तर दीजिए' if many else 'प्रश्न का उत्तर दीजिए'
    if real:
        return f'निम्नलिखित {label} "{ch["title"]}" से लिया गया है। इसे पढ़कर {q}।'
    return f'निम्नलिखित {label} "{ch["title"]}" के भाव पर आधारित (मौलिक) है। इसे पढ़कर {q}।'


def g_extract_one(ch, extracts, mcq_only):
    def g(r):
        ex = r.choice(extracts)
        text, qs = ex[1:3]
        pool = [q for q in qs if (len(q) > 2 and bool(q[2])) == mcq_only]
        need(pool)
        q = r.choice(pool)
        label = 'काव्यांश' if '\n' in text else 'गद्यांश'
        stem = f'{_ex_head(ch, label, len(ex) > 3)}\n{text}\nप्रश्न: {q[0]}'
        if mcq_only:
            return mcq(stem, q[1], list(q[2])[:3], f'{label} के आधार पर उत्तर: {q[1]}।', r)
        return {'stem': stem, 'answer': q[1], 'key': f'{q[1]} (2 अंक: विषय-वस्तु 1, भाषा 1)', 'marks': 2}
    return g


def extract_set(r, ch, extracts, n, only_mcq=False):
    ex = r.choice(extracts)
    text, qs = ex[1:3]
    pool = [q for q in qs if len(q) > 2 and q[2]] if only_mcq else list(qs)
    need(len(pool) >= n)
    picks = sorted(r.sample(range(len(pool)), n))
    label = 'काव्यांश' if '\n' in text else 'गद्यांश'
    lines = [_ex_head(ch, label, len(ex) > 3, True), text]
    ans = []
    for i, k in enumerate(picks):
        q = pool[k]
        if len(q) > 2 and q[2]:
            opts, L = shuffled(r, q[1], q[2])
            lines.append(f'({ROMAN[i]}) {q[0]}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[i]}) ({L}) {q[1]}')
        else:
            lines.append(f'({ROMAN[i]}) {q[0]}')
            ans.append(f'({ROMAN[i]}) {q[1]}')
    a = ' '.join(ans)
    return {'stem': '\n'.join(lines), 'answer': a, 'key': a + f' (प्रत्येक 1 अंक, कुल {n} अंक)', 'marks': n, 'minutes': n + 2, 'gap': 'G7'}


# ---------------------------------------------------------------- writing (रचना)

def slots(r, grade):
    nm, girl = person(r)
    return dict(name=nm, girl=girl, city=r.choice(CITIES), school=r.choice(SCHOOLS), grade=grade,
                chhatra=ge(girl, 'छात्र', 'छात्रा'), vala=ge(girl, 'वाले', 'वाली'))


def fillh(t, s):
    t = re.sub(r'(\S+)/(\S+)', lambda m: m.group(2) if s['girl'] else m.group(1), t) if '/' in t and '{' in t else t
    return t.format(**s)


WRITERS = {}


def writer(name):
    def deco(fn):
        WRITERS[name] = fn
        return fn
    return deco


@writer('anuch')
def w_anuch(topics, grade, marks=6, words='120'):
    """topics: (title, [hints])."""
    c = cyc('anuch')

    def g(r):
        title, hints = c.pick(r, topics)
        h = [hints[i] for i in sorted(r.sample(range(len(hints)), 3))] if len(hints) > 3 else list(hints)
        stem = f'"{title}" विषय पर दिए गए संकेत-बिंदुओं के आधार पर लगभग {words} शब्दों में एक अनुच्छेद लिखिए।\nसंकेत-बिंदु: ' + ' • '.join(h)
        return {'stem': stem, 'answer': f'अनुच्छेद में ये बिंदु क्रम से आएँ: {"; ".join(h)}। आरंभ विषय-प्रवेश से और अंत निष्कर्ष से हो।',
                'key': f'अंक-विभाजन ({marks}): भूमिका और निष्कर्ष 1, संकेत-बिंदुओं का विस्तार {marks - 3}, भाषा-शुद्धता 1, प्रस्तुति और शब्द-सीमा 1।',
                'marks': marks, 'minutes': 10, 'gap': 'G5'}
    return g


@writer('patra')
def w_patra(topics, grade, marks=5, words='100'):
    """topics: (to_whom, subject phrase ending in 'हेतु/के संबंध में', points)."""
    c = cyc('patra')

    def g(r):
        s = slots(r, grade)
        to, subj, pts = c.pick(r, topics)
        stem = (f'आप {s["city"]} के {s["school"]} में कक्षा {grade} {ge(s["girl"], "के छात्र", "की छात्रा")} {s["name"]} हैं। '
                f'{to} को {subj} लगभग {words} शब्दों में एक पत्र लिखिए।')
        return {'stem': stem, 'answer': ('औपचारिक पत्र—प्रेषक का पता, दिनांक, सेवा में (पद और पता), विषय, संबोधन, मुख्य भाग, समापन (भवदीय/भवदीया), '
                                         f'नाम। मुख्य बिंदु: {pts}'),
                'key': f'अंक-विभाजन ({marks}): आरंभ और अंत की औपचारिकताएँ 1, विषय-वस्तु {marks - 2}, भाषा-शुद्धता और प्रस्तुति 1।',
                'marks': marks, 'minutes': 9, 'gap': 'G5'}
    return g


@writer('email')
def w_email(topics, grade, marks=5, words='80'):
    """topics: (to_whom with e-mail role, subject phrase, points)."""
    c = cyc('email')

    def g(r):
        s = slots(r, grade)
        to, subj, pts = c.pick(r, topics)
        stem = f'आप {s["city"]} {ge(s["girl"], "निवासी", "निवासी")} {s["name"]} हैं। {to} को {subj} लगभग {words} शब्दों में एक ई-मेल लिखिए।'
        return {'stem': stem, 'answer': f'ई-मेल—प्रति (To), विषय (Subject) पंक्ति, संबोधन, संक्षिप्त मुख्य भाग, समापन और नाम। मुख्य बिंदु: {pts}',
                'key': f'अंक-विभाजन ({marks}): ई-मेल का प्रारूप (प्रति, विषय, संबोधन, समापन) 1, विषय-वस्तु {marks - 2}, भाषा 1।',
                'marks': marks, 'minutes': 8, 'gap': 'G5'}
    return g


@writer('svavritt')
def w_svavritt(posts, grade, marks=5, words='80'):
    """posts: (post, organisation, requirement)."""
    c = cyc('svavritt')

    def g(r):
        s = slots(r, grade)
        post, org, req = c.pick(r, posts)
        stem = (f'{org} में "{post}" पद के लिए आवेदन करना है ({req})। इसके लिए {s["name"]} की ओर से लगभग {words} शब्दों में अपना स्ववृत्त '
                '(बायोडाटा) तैयार कीजिए।')
        return {'stem': stem, 'answer': ('स्ववृत्त—नाम, पिता/माता का नाम, जन्मतिथि, पता, संपर्क, ई-मेल; शैक्षिक योग्यताएँ (तालिका रूप में); '
                                         f'अन्य योग्यताएँ/अनुभव; रुचियाँ; भाषा-ज्ञान; उपलब्धियाँ; घोषणा, दिनांक और हस्ताक्षर। पद "{post}" के अनुरूप योग्यताएँ।'),
                'key': f'अंक-विभाजन ({marks}): प्रारूप 1, व्यक्तिगत विवरण 1, योग्यताएँ और अनुभव {marks - 3}, प्रस्तुति 1।', 'marks': marks, 'minutes': 8, 'gap': 'G5'}
    return g


@writer('vigyapan')
def w_vigyapan(items, grade, marks=4, words='40'):
    """items: (what to advertise, hints)."""
    c = cyc('vigyapan')

    def g(r):
        what, hints = c.pick(r, items)
        stem = f'{what} के लिए लगभग {words} शब्दों में एक आकर्षक विज्ञापन तैयार कीजिए।'
        return {'stem': stem, 'answer': f'विज्ञापन—आकर्षक शीर्षक/नारा, मुख्य विशेषताएँ ({hints}), छूट/सुविधा, संपर्क-सूत्र, प्रस्तुति (चौखट, बड़े अक्षर)।',
                'key': f'अंक-विभाजन ({marks}): विषय-वस्तु 2, प्रस्तुति और आकर्षक भाषा 1, संपर्क-विवरण/नारा 1।', 'marks': marks, 'minutes': 6, 'gap': 'G5'}
    return g


@writer('sandesh')
def w_sandesh(items, grade, marks=4, words='40'):
    """items: (occasion/purpose sentence with {name}, hints)."""
    c = cyc('sandesh')

    def g(r):
        s = slots(r, grade)
        what, hints = c.pick(r, items)
        stem = f'{fillh(what, s)} इसके लिए लगभग {words} शब्दों में एक संदेश लिखिए।'
        return {'stem': stem, 'answer': f'संदेश—शीर्षक "संदेश", दिनांक और समय, संबोधन, मुख्य संदेश ({hints}), भेजने वाले का नाम।',
                'key': f'अंक-विभाजन ({marks}): प्रारूप 1, विषय-वस्तु 2, भाषा 1।', 'marks': marks, 'minutes': 6, 'gap': 'G5'}
    return g


@writer('rachna')
def w_rachna(topics, grade, marks=6, words='120'):
    """अप्रत्याशित विषयों पर रचनात्मक लेखन (class 12). topics: list of titles."""
    c = cyc('rachna')

    def g(r):
        t = c.pick(r, topics)
        return {'stem': f'"{t}" विषय पर लगभग {words} शब्दों में एक रचनात्मक लेख लिखिए।',
                'answer': 'आकर्षक आरंभ, विषय के विविध पक्षों पर मौलिक विचार, अनुभव या उदाहरण, सुसंगत क्रम और प्रभावी निष्कर्ष।',
                'key': f'अंक-विभाजन ({marks}): आरंभ और प्रस्तुति 1, विषय-वस्तु और मौलिकता {marks - 3}, भाषा-शुद्धता 1, निष्कर्ष 1।', 'marks': marks,
                'minutes': 10, 'gap': 'G5'}
    return g


@writer('feature')
def w_feature(topics, grade, marks=4, words='80'):
    """पत्रकारीय लेखन: topics are (form, title) where form is फ़ीचर/आलेख/रिपोर्ट."""
    c = cyc('feature')
    shape = {'फ़ीचर': 'रोचक शीर्षक, कथात्मक या दृश्यात्मक आरंभ, तथ्यों के साथ भावनात्मक जुड़ाव, उद्धरण/अनुभव, सधा हुआ अंत',
             'आलेख': 'शीर्षक, विषय-प्रवेश, तथ्यों और आँकड़ों सहित विश्लेषण, विभिन्न पक्ष, लेखक का निष्कर्ष',
             'रिपोर्ट': 'शीर्षक, स्थान और तिथि, क्या-कब-कहाँ-कौन-क्यों-कैसे, मुख्य घटनाएँ उलटा पिरामिड शैली में, तटस्थ भाषा'}

    def g(r):
        form, t = c.pick(r, topics)
        return {'stem': f'"{t}" विषय पर लगभग {words} शब्दों में एक {form} लिखिए।', 'answer': f'{form} के तत्त्व: {shape[form]}।',
                'key': f'अंक-विभाजन ({marks}): प्रारूप/शीर्षक 1, विषय-वस्तु {marks - 2}, भाषा 1।', 'marks': marks, 'minutes': 7, 'gap': 'G5'}
    return g


@writer('sansmaran')
def w_sansmaran(topics, grade, marks=5, words='120'):
    """अभिव्यक्ति: topics are (form, subject) where form is संस्मरण/रेखाचित्र."""
    c = cyc('sansmaran')
    shape = {'संस्मरण': 'लेखक की स्मृति में बसे व्यक्ति/घटना का आत्मीय, कालक्रमिक वर्णन; "मैं" शैली; प्रसंगों और अनुभूतियों के साथ; अंत में उस स्मृति का प्रभाव',
             'रेखाचित्र': 'व्यक्ति या दृश्य का शब्द-चित्र: रूप-रंग, वेशभूषा, आदतें, बोलचाल, स्वभाव की रेखाएँ उभारना; संक्षिप्त प्रसंग; संवेदनशील दृष्टि'}

    def g(r):
        form, t = c.pick(r, topics)
        return {'stem': f'"{t}" विषय पर लगभग {words} शब्दों में एक {form} लिखिए।', 'answer': f'{form} के तत्त्व: {shape[form]}।',
                'key': f'अंक-विभाजन ({marks}): विधा के अनुरूप शिल्प 1, विषय-वस्तु और संवेदना {marks - 2}, भाषा 1।', 'marks': marks, 'minutes': 8, 'gap': 'G5'}
    return g


@writer('natya')
def w_natya(situations, grade, marks=5, words='120'):
    """नाट्य रूपांतरण / रेडियो नाटक: situations are (form, situation)."""
    c = cyc('natya')
    shape = {'नाट्य रूपांतरण': 'दृश्य-विभाजन, स्थान-समय का संकेत, पात्रों के नाम सहित संवाद, कोष्ठक में मंच-निर्देश (हाव-भाव, प्रकाश), द्वंद्व और चरम क्षण',
             'रेडियो नाटक': 'ध्वनि-प्रभाव और संगीत के संकेत, केवल संवादों से दृश्य की कल्पना, सीमित पात्र, पात्रों के नाम बार-बार संवाद में, स्पष्ट उच्चारण योग्य छोटे वाक्य'}

    def g(r):
        form, sit = c.pick(r, situations)
        return {'stem': f'निम्नलिखित स्थिति को लगभग {words} शब्दों के एक {form} अंश में प्रस्तुत कीजिए—{sit}',
                'answer': f'{form} के तत्त्व: {shape[form]}।',
                'key': f'अंक-विभाजन ({marks}): {form} का प्रारूप 1, संवाद और प्रसंग {marks - 2}, भाषा 1।', 'marks': marks, 'minutes': 8, 'gap': 'G5'}
    return g


def write_families(spec, ch, grade):
    """Families for a WRITE subtopic: format facts, A-R, explain, a few drafting tasks and the writing tasks."""
    out = []
    facts = spec.get('facts', [])
    if facts:
        out += [F('C1', 'D1', 'mcq', g_fact(facts)), F('C1', 'D2', 'mcq', g_fact(facts[::-1]))]
    if spec.get('true') and spec.get('false'):
        out += [F('C2', 'D2', 'mcq', g_true(spec.get('ref', ch['title']), spec['true'], spec['false'])),
                F('C2', 'D3', 'mcq', g_false(spec.get('ref', ch['title']), spec['true'], spec['false']))]
    if spec.get('ar'):
        out.append(F('C2', 'D3', 'mcq', g_ar(spec['ar']), kinds=('ar',)))
    if spec.get('wr'):
        out.append(F('C2', 'D2', 'explain', g_wr(spec['wr'], spec.get('words', '25-30'))))
    if spec.get('theory'):
        tw = spec.get('twords', '60')
        out += [F('C2', 'D3', 'explain', g_wr(spec['theory'], tw, 4), marks=4), F('C3', 'D3', 'explain', g_wr(spec['theory'][::-1], tw, 4), marks=4)]
    for extra in spec.get('extra', []):
        out.append(extra)
    for form, topics, kw in spec.get('tasks', []):
        gen = WRITERS[form](topics, grade, **kw)
        out += [F('C4', 'D4', 'long', gen), F('C4', 'D5', 'long', gen), F('C3', 'D4', 'long', gen)]
    return out


# ---------------------------------------------------------------- literature families

def lit_families(ch, spec, grade, extracts, statements, cfg):
    ref = spec.get('ref', ch['title'])
    out = []
    facts = spec.get('facts', [])
    if facts:
        out += [F('C1', 'D1', 'mcq', g_fact(facts)), F('C1', 'D2', 'mcq', g_fact(facts))]
    true, false = spec.get('true', []), spec.get('false', [])
    if true and false:
        out += [F('C2', 'D2', 'mcq', g_true(ref, true, false)), F('C2', 'D3', 'mcq', g_false(ref, true, false))]
    if spec.get('ar'):
        out.append(F('C2', 'D3', 'mcq', g_ar(spec['ar']), kinds=('ar',)))
    wr = spec.get('wr', [])
    if wr:
        out.append(F('C2', 'D2', 'explain', g_wr(wr, cfg['w2'], 2)))
        if len(wr) >= 3:
            out.append(F('C2', 'D3', 'explain', wr_set(wr, 2, 2, cfg['w2'])))
    if spec.get('think'):
        out.append(F('C4', 'D3', 'explain', g_wr(spec['think'], cfg['w3'], 3, think=True), gap='G5'))
    if spec.get('long'):
        out.append(F('C4', 'D4', 'long', g_long(spec['long'], cfg['wl'], cfg['ml'])))
    if extracts:
        if any(len(q) > 2 and q[2] for e in extracts for q in e[2]):
            out.append(F('C3', 'D2', 'mcq', g_extract_one(ch, extracts, True)))
        if any(not (len(q) > 2 and q[2]) for e in extracts for q in e[2]):
            out.append(F('C3', 'D3', 'explain', g_extract_one(ch, extracts, False)))
        out.append(F('C3', 'D4', 'case', (lambda ex: lambda r: extract_set(r, ch, ex, 4))(extracts)))
    if statements:
        out.append(F('C3', 'D1', 'short', g_jumble(statements), gap='G3'))
    if ch.get('vocab'):
        out.append(F('C3', 'D1', 'mcq', g_vocab_mcq(ch['vocab'], ch['title'])))
        out.append(F('C3', 'D2', 'explain', g_vocab_use(ch['vocab'])))
    for extra in spec.get('extra', []):
        out.append(extra)
    return out


def build(sid, chapters, grade, cfg, passages=None, mock_extra=None):
    """Return (families by subtopic, mock-only families by subtopic)."""
    from g10_hindi_gram import gram_families
    fams = {}
    for n, ch in chapters.items():
        cid = f'{sid}-ch{n:02d}'
        for k, spec in ch['sts'].items():
            st = f'{cid}-st{k}'
            kind = spec['kind']
            if kind == 'lit':
                exs = [e for e in ch.get('extracts', []) if e[0] == k]
                stmts = spec.get('true', [])
                fl = lit_families(ch, spec, grade, exs, stmts, cfg)
                for p in ch.get('writing', []):
                    if p[0] == k:
                        gen = WRITERS[p[1]](p[2], grade, **p[3]) if len(p) > 3 else WRITERS[p[1]](p[2], grade)
                        fl.append(F('C4', 'D5' if len(fl) % 2 else 'D4', 'long', gen))
                fams[st] = fl
            elif kind == 'gram':
                fams[st] = gram_families(spec, ch, grade)
            elif kind == 'write':
                fams[st] = write_families(spec, ch, grade)
            elif kind == 'apathit':
                fams[st] = apathit_families(spec, passages or {}, grade)
            else:
                raise SystemExit(kind)
    mock = mock_extra(chapters, fams) if mock_extra else {}
    return fams, mock


# ---------------------------------------------------------------- अपठित

APATHIT_FACTS = [
    ('अपठित गद्यांश का सबसे उपयुक्त शीर्षक कैसा होना चाहिए?', 'संक्षिप्त और केंद्रीय भाव को प्रकट करने वाला', ['बहुत लंबा और विस्तृत', 'गद्यांश के अंतिम शब्द जैसा', 'किसी पात्र का नाम ही'],
     'शीर्षक छोटा, सटीक और मूल भाव का सूचक होता है।'),
    ('गद्यांश का केंद्रीय भाव प्रायः कहाँ मिलता है?', 'आरंभिक या निष्कर्ष-वाक्यों में', ['केवल विराम-चिह्नों में', 'पृष्ठ-संख्या में', 'कठिन शब्दों की सूची में'],
     'मुख्य विचार प्रायः आरंभ या अंत में स्पष्ट होता है।'),
    ('प्रश्नों के उत्तर देने से पहले गद्यांश को कैसे पढ़ना चाहिए?', 'ध्यानपूर्वक, कम-से-कम दो बार', ['केवल शीर्षक देखकर', 'केवल अंतिम पंक्ति पढ़कर', 'बिना पढ़े'],
     'पहली बार में भाव, दूसरी बार में विवरण समझ आता है।'),
    ('काव्यांश में "प्रतीक" से क्या अभिप्राय है?', 'किसी वस्तु द्वारा किसी अन्य भाव या विचार का संकेत', ['कविता की पंक्ति-संख्या', 'कवि का नाम', 'तुकांत शब्द'],
     'प्रतीक किसी गहरे अर्थ की ओर संकेत करता है।'),
    ('अपठित अंश में किसी शब्द का अर्थ न आने पर क्या करना चाहिए?', 'प्रसंग (संदर्भ) से अर्थ का अनुमान लगाना', ['प्रश्न छोड़ देना', 'कोई भी अर्थ लिख देना', 'पूरा अंश दोबारा लिखना'],
     'आसपास के वाक्य अर्थ का संकेत देते हैं।'),
    ('"निष्कर्ष" निकालने का अर्थ है—', 'पढ़े हुए अंश से सार रूप में परिणाम तक पहुँचना', ['अंश को ज्यों-का-त्यों उतारना', 'नए पात्र जोड़ना', 'शीर्षक बदलना'],
     'निष्कर्ष = अंश का सार-परिणाम।'),
]
APATHIT_AR = [('अपठित अंश के उत्तर अपने शब्दों में लिखने चाहिए।', 'अपठित अंश के उत्तर में पूरा अंश उतार देना चाहिए।',
               'इससे यह पता चलता है कि विद्यार्थी ने अंश का भाव समझा है।', 'इससे उत्तर अधिक लंबा और सुंदर दिखता है।', 'अपने शब्दों में लिखना समझ का प्रमाण है।'),
              ('शीर्षक अंश के केंद्रीय भाव पर आधारित होना चाहिए।', 'शीर्षक किसी भी शब्द से बनाया जा सकता है।',
               'शीर्षक पूरे अंश का सार संक्षेप में प्रस्तुत करता है।', 'शीर्षक केवल पहले शब्द से बनता है।', 'शीर्षक = सार।')]
APATHIT_WR = [('अपठित गद्यांश के प्रश्नों के उत्तर देते समय किन बातों का ध्यान रखना चाहिए?', 'अंश को ध्यान से दो बार पढ़ना, प्रश्न समझना, उत्तर अंश पर आधारित और अपने शब्दों में संक्षेप में लिखना।'),
              ('अपठित काव्यांश और अपठित गद्यांश को समझने में क्या अंतर है?', 'काव्यांश में भाव, प्रतीक और बिंब पर ध्यान देना होता है; गद्यांश में तथ्य और विचार-क्रम पर।')]


def apathit_families(spec, passages, grade):
    from g8_hindi_lib import passage_gen, passage_short
    themes = spec.get('themes') or []
    poems = spec.get('poems') or []
    out = [F('C1', 'D1', 'mcq', g_fact(APATHIT_FACTS)), F('C1', 'D2', 'mcq', g_fact(APATHIT_FACTS[::-1])),
           F('C2', 'D3', 'mcq', g_ar(APATHIT_AR), kinds=('ar',)), F('C2', 'D2', 'explain', g_wr(APATHIT_WR))]
    for t in themes:
        out += [F('C3', 'D2', 'mcq', passage_short(t), gap='G7'), F('C3', 'D3', 'case', passage_gen(t), marks=7, minutes=10, gap='G7')]
    for p in poems:
        out += [F('C3', 'D2', 'mcq', kavya_one(p), gap='G7'), F('C3', 'D4', 'case', kavya_gen([p], 4), gap='G7')]
    if themes:
        out.append(F('C4', 'D3', 'explain', lambda r: theme_written(r, themes), gap='G5'))
        out.append(F('C4', 'D4', 'case', (lambda ts: lambda r: passage_gen(r.choice(ts))(r))(themes), marks=7, minutes=10, gap='G7'))
    return out


def theme_written(r, themes):
    t = r.choice(themes)
    q, a = r.choice(t['written'])
    text = ' '.join(s[0] for s in t['sents'][:5])
    return {'stem': f'गद्यांश पढ़कर प्रश्न का उत्तर लगभग 30-40 शब्दों में दीजिए।\n{text}\nप्रश्न: {q}', 'answer': a,
            'key': f'मूल्य-बिंदु: {a} (3 अंक: विषय-वस्तु 2, भाषा 1)', 'marks': 3}


def kavya_one(p):
    def g(r):
        q, a, w = r.choice(p['qs'])
        return mcq(f'काव्यांश पढ़कर प्रश्न का उत्तर दीजिए।\n{p["text"]}\nप्रश्न: {q}', a, list(w)[:3], f'काव्यांश के अनुसार: {a}।', r)
    return g


def kavya_gen(poems, k=4, written=1, title=True):
    """Original poem with k MCQs, a title MCQ and `written` 2-mark questions."""
    def g(r):
        p = r.choice(poems)
        need(len(p['qs']) >= k)
        qs = r.sample(p['qs'], k)
        lines = ['निम्नलिखित काव्यांश को ध्यानपूर्वक पढ़कर पूछे गए प्रश्नों के उत्तर दीजिए।', p['text']]
        ans = []
        for j, (q, a, wrong) in enumerate(qs):
            opts, L = shuffled(r, a, wrong)
            lines.append(f'({ROMAN[j]}) {q}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[j]}) ({L}) {a}')
        j = k
        if title:
            t, bad = p['title']
            opts, L = shuffled(r, t, bad)
            lines.append(f'({ROMAN[j]}) काव्यांश का उपयुक्त शीर्षक है—\n{opts_line(opts)}')
            ans.append(f'({ROMAN[j]}) ({L}) {t}')
            j += 1
        ws = r.sample(p['written'], min(written, len(p['written'])))
        for q, a in ws:
            lines.append(f'({ROMAN[j]}) {q}')
            ans.append(f'({ROMAN[j]}) {a}')
            j += 1
        mk = k + (1 if title else 0) + 2 * len(ws)
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans),
                'key': f'बहुविकल्पी प्रत्येक 1 अंक; लिखित प्रत्येक 2 अंक। कुल {mk} अंक। ' + ' '.join(ans), 'marks': mk, 'minutes': mk + 3, 'gap': 'G7'}
    return g


def gadyansh(themes, n_mcq=5, n_wr=1, wr_marks=2):
    """Original passage from a theme: n_mcq MCQs (from sentences, title counts as one) and n_wr written questions."""
    def g(r):
        t = r.choice(themes)
        sents = t['sents']
        n_s = min(len(sents), n_mcq + 2)
        idx = [0] + sorted(r.sample(range(1, len(sents)), n_s - 1))
        text = ' '.join(sents[i][0] for i in idx)
        qi = sorted(r.sample(idx, n_mcq - 1))
        lines = ['निम्नलिखित गद्यांश को ध्यानपूर्वक पढ़कर पूछे गए प्रश्नों के उत्तर दीजिए।', text]
        ans = []
        for j, i in enumerate(qi):
            _, q, a, wrong = sents[i]
            opts, L = shuffled(r, a, wrong)
            lines.append(f'({ROMAN[j]}) {q}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[j]}) ({L}) {a}')
        j = n_mcq - 1
        t_ok = r.choice(t['titles'])
        opts, L = shuffled(r, t_ok, t['bad_titles'])
        lines.append(f'({ROMAN[j]}) गद्यांश के लिए सबसे उपयुक्त शीर्षक कौन-सा है?\n{opts_line(opts)}')
        ans.append(f'({ROMAN[j]}) ({L}) {t_ok}')
        j += 1
        ws = r.sample(t['written'], min(n_wr, len(t['written'])))
        for q, a in ws:
            lines.append(f'({ROMAN[j]}) {q}')
            ans.append(f'({ROMAN[j]}) {a}')
            j += 1
        mk = n_mcq + wr_marks * len(ws)
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans),
                'key': f'बहुविकल्पी प्रत्येक 1 अंक; लिखित प्रत्येक {wr_marks} अंक (विषय-वस्तु {wr_marks - 1}, भाषा 1)। कुल {mk} अंक। ' + ' '.join(ans),
                'marks': mk, 'minutes': mk + 4, 'gap': 'G7'}
    return g


# ---------------------------------------------------------------- builder with mock-only families

class HindiBuilder(Builder):
    def __init__(self, *a, mock_families=None, **kw):
        super().__init__(*a, **kw)
        self.mock_families = mock_families or {}

    def _mocks(self, chapters):
        for st, fl in self.mock_families.items():
            for f in fl:
                f.st = st
            self.families.setdefault(st, []).extend(fl)
        return super()._mocks(chapters)


def first_lit(ch, cid):
    for k, st in ch['sts'].items():
        if st['kind'] == 'lit':
            return f'{cid}-st{k}'
    return f'{cid}-st{min(ch["sts"])}'


def all_mcq_rows(ch):
    rows = []
    for st in ch['sts'].values():
        if st['kind'] == 'lit':
            rows += [x for x in st.get('facts', []) if len(x[2]) >= 3]
    return rows


def all_wr(ch, with_think=True):
    out = []
    for st in ch['sts'].values():
        if st['kind'] == 'lit':
            out += st.get('wr', []) + (st.get('think', []) if with_think else [])
    return out


def all_long(ch):
    out = []
    for st in ch['sts'].values():
        if st['kind'] == 'lit':
            out += st.get('long', [])
    return out


def run(sid, generated_by, chapters, grade, cfg, pattern, passages, mock_extra, accuracy=None):
    fams, mock = build(sid, chapters, grade, cfg, passages, mock_extra)
    b = HindiBuilder(sid, generated_by, fams, pattern, mock_families=mock, mock_minutes_per_mark=2.25)
    files = b.build()
    b.write(files, accuracy)
    print(f'{sid}: wrote {sum(len(v) for v in files.values())} questions')
    return files
