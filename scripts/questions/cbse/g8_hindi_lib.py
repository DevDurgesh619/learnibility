"""Shared helpers for the CBSE class 8 Hindi (Malhar) question bank.

Everything here is original text written for the bank (no textbook passages are reproduced).
"""
from __future__ import annotations

import random
import re

from qbank import F, mcq, onorm


def gfix(text: str, girl: bool) -> str:
    """Resolve gendered pairs such as "करता/करती" for the person speaking or acting."""
    return re.sub(r'(\S+)/(\S+)', lambda m: m.group(2) if girl else m.group(1), text)

# ---------------------------------------------------------------- names and places (Devanagari)

GIRLS = ['अनन्या', 'इशिता', 'मीरा', 'दीया', 'काव्या', 'सान्वी', 'रिया', 'अदिति', 'पूजा', 'स्नेहा', 'तन्वी',
         'नंदिनी', 'ज़ोया', 'फ़ातिमा', 'हरलीन', 'लक्ष्मी', 'प्रिया', 'श्रेया', 'आयशा', 'गौरी', 'मेहक', 'तारा']
BOYS = ['आरव', 'कबीर', 'रोहन', 'विहान', 'अर्जुन', 'निखिल', 'कुणाल', 'आदित्य', 'ईशान', 'राहुल', 'सिद्धार्थ',
        'इमरान', 'हरप्रीत', 'कार्तिक', 'मनीष', 'देव', 'यश', 'फ़रहान', 'आर्यन', 'वरुण', 'साहिल', 'ओम']
CITIES = ['दिल्ली', 'मुंबई', 'पुणे', 'जयपुर', 'लखनऊ', 'कोच्चि', 'भोपाल', 'चंडीगढ़', 'इंदौर', 'पटना', 'नागपुर',
          'सूरत', 'गुवाहाटी', 'मैसूरु', 'देहरादून', 'वाराणसी', 'कोयंबटूर', 'राँची', 'शिमला', 'आगरा']
SCHOOLS = ['केंद्रीय विद्यालय', 'सरस्वती विद्या मंदिर', 'आदर्श पब्लिक स्कूल', 'राजकीय उच्चतर माध्यमिक विद्यालय',
           'जवाहर नवोदय विद्यालय', 'ज्ञानदीप विद्यालय', 'नवभारत पब्लिक स्कूल', 'प्रगति विद्यालय']
LETTERS = ['क', 'ख', 'ग', 'घ']


_USED: dict = {}
_ORDER: dict = {}


class Cycler:
    """Pick table rows without repeating until every row has been used once (keeps forms varied).
    Cyclers with the same namespace share their record, so two families drawing on the same rows
    (e.g. the same writing topics) do not repeat each other's rows either."""

    def __init__(self, ns: str = 'w'):
        self.used = _USED.setdefault(ns, set())
        self.order = _ORDER.setdefault(ns, [])

    def pick(self, r, seq):
        seq = list(seq)
        keys = [repr(x) for x in seq]
        free = [i for i, k in enumerate(keys) if k not in self.used]
        if not free:
            recent = set(k for k in self.order[-max(1, len(seq) // 2):] if k in keys)
            for k in keys:
                if k not in recent:
                    self.used.discard(k)
            free = [i for i, k in enumerate(keys) if k not in self.used]
        i = r.choice(free)
        self.used.add(keys[i])
        self.order.append(keys[i])
        return seq[i]


def person(r: random.Random):
    """(name, is_girl)."""
    if r.random() < 0.5:
        return r.choice(GIRLS), True
    return r.choice(BOYS), False


def ge(girl: bool, m: str, f: str) -> str:
    return f if girl else m


# ---------------------------------------------------------------- item shapes

HAR_OPTIONS = [
    'अभिकथन (A) और कारण (R) दोनों सही हैं तथा कारण (R), अभिकथन (A) की सही व्याख्या करता है।',
    'अभिकथन (A) और कारण (R) दोनों सही हैं, परंतु कारण (R), अभिकथन (A) की सही व्याख्या नहीं करता।',
    'अभिकथन (A) सही है, परंतु कारण (R) गलत है।',
    'अभिकथन (A) गलत है, परंतु कारण (R) सही है।',
]


def har(a: str, rsn: str, code: str, why: str) -> dict:
    i = 'abcd'.index(code)
    return {'stem': f'अभिकथन (A): {a}\nकारण (R): {rsn}\nसही विकल्प चुनिए।',
            'options': HAR_OPTIONS[:], 'answer': HAR_OPTIONS[i], 'key': f'({code}) {why}'}


def AR(C, D, rows, **kw):
    """Assertion-Reason family over rows of (A, R, code, why)."""
    def gen(r):
        a, rsn, code, why = r.choice(rows)
        return har(a, rsn, code, why)
    kw.setdefault('kinds', ('ar',))
    return F(C, D, 'mcq', gen, **kw)


def M(C, D, rows, **kw):
    """MCQ family over rows of (stem, correct, [wrong...], key). Three wrong options are sampled when more are given."""
    def gen(r):
        stem, ans, wrong, key = r.choice(rows)
        w = list(wrong)
        w = r.sample(w, 3) if len(w) > 3 else w
        return mcq(stem, ans, w, key, r)
    return F(C, D, 'mcq', gen, **kw)


def W(C, D, typ, rows, **kw):
    """Written-answer family over rows of (stem, answer, key)."""
    def gen(r):
        stem, ans, key = r.choice(rows)
        return {'stem': stem, 'answer': ans, 'key': key}
    return F(C, D, typ, gen, **kw)


def G(C, D, typ, fn, **kw):
    return F(C, D, typ, fn, **kw)


def opts_line(opts):
    return '  '.join(f'({LETTERS[i]}) {o}' for i, o in enumerate(opts))


def shuffled(r, ans, wrong):
    w = list(wrong)
    w = r.sample(w, 3) if len(w) > 3 else w
    opts = [ans] + w
    if len({onorm(o) for o in opts}) != 4:
        raise ValueError('options not distinct')
    r.shuffle(opts)
    return opts, LETTERS[opts.index(ans)]


ROMAN = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']


def mcq_set(rows, k, head='निम्नलिखित प्रश्नों के सही विकल्प चुनिए।'):
    """k MCQs from rows as one item (पाठ-आधारित बहुविकल्पी प्रश्न), 1 mark each."""

    def gen(r):
        pick = r.sample(rows, k)
        lines, ans = [head], []
        for i, (stem, a, wrong, key) in enumerate(pick):
            opts, L = shuffled(r, a, wrong)
            lines.append(f'({ROMAN[i]}) {stem}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[i]}) ({L}) {a}')
        return {'stem': '\n'.join(lines), 'answer': '; '.join(ans),
                'key': f'प्रत्येक सही विकल्प के लिए 1 अंक (कुल {k} अंक)। ' + '; '.join(ans) + '।'}
    return gen


def short_set(rows, k, each, head='निम्नलिखित प्रश्नों के उत्तर लगभग 25-30 शब्दों में लिखिए।'):
    """k written questions from rows (stem, answer, key) as one item, `each` marks per part."""
    def gen(r):
        pick = r.sample(rows, k)
        lines, ans, keys = [head], [], []
        for i, (stem, a, key) in enumerate(pick):
            lines.append(f'({ROMAN[i]}) {stem}')
            ans.append(f'({ROMAN[i]}) {a}')
            keys.append(f'({ROMAN[i]}) {key}')
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans),
                'key': f'प्रत्येक भाग {each} अंक (कुल {k * each} अंक): विषय-वस्तु {each - 1 if each > 1 else each}, भाषा 1। ' + ' '.join(keys)}
    return gen


def table_set(make_part, k, head, each=1):
    """k parts, each from make_part(r) -> (question, answer), as one grammar item (निर्देशानुसार)."""
    def gen(r):
        seen, parts = set(), []
        guard = 0
        while len(parts) < k and guard < 60:
            guard += 1
            q, a = make_part(r)
            if q in seen or any(a in pq or pa in q or pa == a for pq, pa in parts):
                continue
            seen.add(q)
            parts.append((q, a))
        if len(parts) < k:
            raise ValueError('not enough parts')
        stem = head + '\n' + '\n'.join(f'({ROMAN[i]}) {q}' for i, (q, _) in enumerate(parts))
        ans = '; '.join(f'({ROMAN[i]}) {a}' for i, (_, a) in enumerate(parts))
        return {'stem': stem, 'answer': ans, 'key': f'प्रत्येक भाग {each} अंक (कुल {k * each} अंक)। {ans}।'}
    return gen


# ---------------------------------------------------------------- अपठित गद्यांश / काव्यांश

def passage_gen(theme: dict, n_pick: int = 5, label='गद्यांश'):
    """Original passage built from a theme's self-contained sentences (kept in order), with
    four MCQs from the chosen sentences, one title MCQ and one 2-mark written question (7 marks)."""
    sents = theme['sents']

    def gen(r):
        idx = [0] + sorted(r.sample(range(1, len(sents)), n_pick - 1))
        text = ' '.join(sents[i][0] for i in idx)
        qi = r.sample(idx, 4)
        qi.sort()
        lines = [f'निम्नलिखित {label} को ध्यानपूर्वक पढ़कर पूछे गए प्रश्नों के उत्तर दीजिए।', text]
        ans = []
        for j, i in enumerate(qi):
            _, q, a, wrong = sents[i]
            opts, L = shuffled(r, a, wrong)
            lines.append(f'({ROMAN[j]}) {q}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[j]}) ({L}) {a}')
        t_ok = r.choice(theme['titles'])
        opts, L = shuffled(r, t_ok, theme['bad_titles'])
        lines.append(f'(v) {label} के लिए सबसे उपयुक्त शीर्षक कौन-सा है?\n{opts_line(opts)}')
        ans.append(f'(v) ({L}) {t_ok}')
        q6, a6 = r.choice(theme['written'])
        lines.append(f'(vi) {q6}')
        ans.append(f'(vi) {a6}')
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans),
                'key': '(i)–(v) प्रत्येक 1 अंक; (vi) 2 अंक (विषय-वस्तु 1, अभिव्यक्ति 1)। कुल 7 अंक। ' + ' '.join(ans)}
    return gen


def passage_short(theme: dict, n_pick: int = 4):
    """Short passage with one MCQ (1 mark) — for bank and practice forms."""
    sents = theme['sents']

    def gen(r):
        idx = [0] + sorted(r.sample(range(1, len(sents)), n_pick - 1))
        text = ' '.join(sents[i][0] for i in idx)
        i = r.choice(idx[1:])
        _, q, a, wrong = sents[i]
        w = list(wrong)
        return mcq(f'गद्यांश पढ़कर प्रश्न का उत्तर दीजिए।\n{text}\nप्रश्न: {q}', a, w[:3],
                   f'गद्यांश के वाक्य "{sents[i][0]}" से उत्तर: {a}।', r)
    return gen


# ---------------------------------------------------------------- रचना (writing)

FORMAL_FMT = ('प्रारूप: सेवा में, पद और पता, दिनांक, विषय, संबोधन (महोदय/महोदया), मुख्य भाग, '
              'धन्यवाद-सहित समापन (भवदीय/आपका आज्ञाकारी शिष्य), नाम और कक्षा।')
INFORMAL_FMT = 'प्रारूप: प्रेषक का पता, दिनांक, संबोधन (पूज्य/प्रिय), अभिवादन, कुशल-क्षेम, मुख्य बात, समापन, संबंध-सूचक शब्द और नाम।'
LETTER_KEY = 'अंक-विभाजन (7): प्रारूप 2 (पता, दिनांक, संबोधन, समापन), विषय-वस्तु 3, भाषा-शुद्धता और प्रस्तुति 2। शब्द-सीमा लगभग 100 शब्द।'


def formal_letter(topics):
    """topics: list of (to_whom, subject, points)."""
    cyc = Cycler()

    def gen(r):
        nm, girl = person(r)
        city = r.choice(CITIES)
        sch = r.choice(SCHOOLS)
        to, subj, pts = cyc.pick(r, topics)
        stem = (f'आप {city} के {sch} में कक्षा 8 {ge(girl, "के छात्र", "की छात्रा")} {nm} हैं। '
                f'{to} को {subj} लगभग 100 शब्दों में पत्र लिखिए।')
        return {'stem': stem, 'answer': f'औपचारिक पत्र। {FORMAL_FMT} मुख्य बिंदु: {pts}',
                'key': LETTER_KEY}
    return gen


def informal_letter(topics):
    """topics: list of (relation, subject, points)."""
    cyc = Cycler()

    def gen(r):
        nm, girl = person(r)
        city = r.choice(CITIES)
        rel, subj, pts = cyc.pick(r, topics)
        stem = f'आप {city} में रहने {ge(girl, "वाले", "वाली")} {nm} हैं। अपने {rel} को {subj} लगभग 100 शब्दों में पत्र लिखिए।'
        return {'stem': stem, 'answer': f'अनौपचारिक पत्र। {INFORMAL_FMT} मुख्य बिंदु: {pts}',
                'key': LETTER_KEY}
    return gen


def paragraph(topics, words='80-100'):
    """topics: list of (title, [hint points])."""
    cyc = Cycler()

    def gen(r):
        title, hints = cyc.pick(r, topics)
        h = [hints[i] for i in sorted(r.sample(range(len(hints)), 3))] if len(hints) > 3 else hints
        stem = f'"{title}" विषय पर दिए गए संकेत-बिंदुओं के आधार पर लगभग {words} शब्दों में अनुच्छेद लिखिए।\nसंकेत-बिंदु: ' + ' • '.join(h)
        return {'stem': stem, 'answer': f'अनुच्छेद में ये बिंदु क्रम से आएँ: {"; ".join(h)}। आरंभ विषय के परिचय से और अंत निष्कर्ष/संदेश से हो।',
                'key': 'अंक-विभाजन (7): आरंभ और अंत 1, संकेत-बिंदुओं का क्रमबद्ध विस्तार 4, भाषा-शुद्धता 2।'}
    return gen


def dialogue(situations):
    """situations: list of (setting with {a} {b}, points)."""
    cyc = Cycler()

    def gen(r):
        (a, ga), (b, gb) = person(r), person(r)
        if a == b:
            raise ValueError('same names')
        setting, pts = cyc.pick(r, situations)
        setting = gfix(setting, ga)
        if ga and gb:
            setting = setting.replace('कर रहे हैं', 'कर रही हैं')
        stem = f'{setting.format(a=a, b=b)} इस विषय पर दोनों के बीच लगभग 60-80 शब्दों में संवाद लिखिए।'
        return {'stem': stem, 'answer': f'संवाद में बारी-बारी से दोनों के कथन, उचित विराम-चिह्न और स्वाभाविक भाषा। मुख्य बातें: {pts}',
                'key': 'अंक-विभाजन (6): प्रारूप (पात्रों के नाम, क्रम) 1, विषय-वस्तु 3, भाषा और विराम-चिह्न 2।'}
    return gen


def notice(events):
    """events: list of (event, details)."""
    cyc = Cycler()

    def gen(r):
        sch = r.choice(SCHOOLS)
        city = r.choice(CITIES)
        ev, det = cyc.pick(r, events)
        role = r.choice(['सांस्कृतिक सचिव', 'छात्र-परिषद के अध्यक्ष', 'हिंदी साहित्य परिषद के सचिव', 'पर्यावरण क्लब के प्रभारी'])
        stem = f'{city} के {sch} के {role} की ओर से "{ev}" के लिए लगभग 50 शब्दों में एक सूचना लिखिए।'
        return {'stem': stem, 'answer': f'सूचना: विद्यालय का नाम, "सूचना" शीर्षक, दिनांक, विषय, विवरण ({det}), सूचना देने वाले का नाम/पद।',
                'key': 'अंक-विभाजन (5): प्रारूप (शीर्षक, दिनांक, नाम-पद) 2, विषय-वस्तु 2, भाषा 1।'}
    return gen


# ---------------------------------------------------------------- generic text-based generators

def situation(stem_tpl, good, bad, why):
    """MCQ: which person's action matches the chapter's idea. good/bad: action phrases (verb-final, ending in 'है/हैं')."""
    cyc = Cycler()

    def gen(r):
        g = cyc.pick(r, good)
        names = r.sample(GIRLS + BOYS, 4)
        acts = [g] + r.sample(bad, 3)
        opts = [f'{n} {gfix(a, n in GIRLS)}' for n, a in zip(names, acts)]
        return mcq(stem_tpl, opts[0], opts[1:], f'{opts[0]}—{why}', r)
    return gen


def claims(chapter, rows, words=40):
    """C4 evaluation: rows of (claim, answer points)."""
    cyc = Cycler()

    def gen(r):
        c, a = cyc.pick(r, rows)
        return {'stem': f'"{c}"—"{chapter}" के आधार पर इस कथन पर अपने विचार लगभग {words} शब्दों में लिखिए।',
                'answer': a, 'key': 'अंक-विभाजन: स्पष्ट मत (सहमति/असहमति) 1, पाठ से जुड़ा तर्क या उदाहरण 1, अपने जीवन/समाज से जुड़ाव 1 (भाषा-शुद्धता अपेक्षित)।'}
    return gen
