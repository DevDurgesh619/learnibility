"""Shared kit for the CBSE Hindi subjects cbse-g9-hindi (NCERT Ganga) and cbse-g11-hindi (आरोह-1 + वितान-1).

Copyright rule: no textbook passage of a copyrighted text is reproduced. Prose "extracts" are original passages
written in our own words on a well-known moment or idea of the chapter; poetry extracts quote only public-domain
poets (Raidas, Tulsidas, Kabir, Meera, Subhadra Kumari Chauhan, Nirala). Every literature stem names the text.

A subject module describes each chapter as a dict and calls `build_families`:
    title, author, vidha (कहानी/कविता/निबंध/...), vocab [(word, meaning, [wrong meanings])],
    extracts [(st, text, [(q, a, [wrong]) | (q, a)])], sts {k: spec}
Subtopic specs:
    LIT(facts, true, false, ar, explain, think, long, infer, situ)  literature
    FAMS(fn)                                                       ready-made families fn(ch, grade) -> [Family]
"""
from __future__ import annotations

import random
import re

from qbank import F, mcq, onorm
from g8_hindi_lib import (Cycler, person, ge, GIRLS, BOYS, CITIES, SCHOOLS, shuffled, opts_line, ROMAN, gfix, HAR_OPTIONS)

LETTERS = ['क', 'ख', 'ग', 'घ']
_CYC: dict = {}


def cp(key, r, seq):
    """Cycle through a table without repeats until every row has been used."""
    return _CYC.setdefault(key, Cycler('hk:' + key)).pick(r, list(seq))


def need(c):
    if not c:
        raise ValueError('not enough data')


def LIT(**kw):
    return dict(kind='lit', **kw)


def FAMS(fn, **kw):
    return dict(kind='fams', fn=fn, **kw)


# ---------------------------------------------------------------- naming the text

def tref(ch):
    return f'{ch["vidha"]} "{ch["title"]}"'


def named(ch, q):
    """Make sure a literature stem names the text."""
    if ch['title'] in q:
        return q
    return f'{tref(ch)} के आधार पर बताइए—{q}'


# ---------------------------------------------------------------- item shapes

def har(a, rsn, code, why):
    i = 'abcd'.index(code)
    return {'stem': f'अभिकथन (A): {a}\nकारण (R): {rsn}\nसही विकल्प चुनिए।',
            'options': HAR_OPTIONS[:], 'answer': HAR_OPTIONS[i], 'key': f'({code}) {why}'}


def pick3(r, wrong):
    w = list(wrong)
    need(len(w) >= 3)
    return r.sample(w, 3) if len(w) > 3 else w


def g_fact(ch, rows, key):
    def g(r):
        q, a, wrong = cp(key, r, rows)[:3]
        why = f'सही उत्तर: {a}।'
        return mcq(named(ch, q), a, pick3(r, wrong), why, r)
    return g


def g_vocab(ch, words, key):
    def g(r):
        w, m, wrong = cp(key, r, words)
        stem = r.choice([f'{tref(ch)} में प्रयुक्त शब्द "{w}" का अर्थ है—', f'{tref(ch)} के संदर्भ में "{w}" शब्द का सही अर्थ चुनिए।'])
        return mcq(stem, m, pick3(r, wrong), f'"{w}" का अर्थ है—{m}।', r)
    return g


LEAD_T = ['{T} के संदर्भ में कौन-सा कथन सही है?', '{T} के बारे में निम्नलिखित में से सत्य कथन चुनिए।', '{T} के आधार पर सही कथन पहचानिए।']
LEAD_F = ['{T} के संदर्भ में कौन-सा कथन सही नहीं है?', '{T} के बारे में निम्नलिखित में से असत्य कथन चुनिए।', '{T} के आधार पर गलत कथन पहचानिए।']


def g_true(ch, true, false, ref=None):
    T = ref or tref(ch)

    def g(r):
        need(len(false) >= 3)
        t = r.choice(true)
        return mcq(r.choice(LEAD_T).format(T=T), t, r.sample(false, 3), f'सही कथन: "{t}" शेष कथन पाठ के विपरीत हैं।', r)
    return g


def g_false(ch, true, false, ref=None):
    T = ref or tref(ch)

    def g(r):
        need(len(true) >= 3)
        f = r.choice(false)
        return mcq(r.choice(LEAD_F).format(T=T), f, r.sample(true, 3), f'"{f}"—यह कथन पाठ के अनुसार सही नहीं है; शेष तीनों सही हैं।', r)
    return g


def g_ar(ch, tuples):
    """tuples: (A, A_false, R, R_false, why[, R_true_unrelated])."""
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
            v = har(A, R, 'a', f'दोनों कथन सही हैं और R, A की सही व्याख्या करता है: {why}')
        elif code == 'c':
            v = har(A, Rf, 'c', f'A सही है, पर R गलत है। वास्तव में—{R}')
        elif code == 'd':
            v = har(Af, R, 'd', f'A गलत है; सही बात यह है—{A} R सही है।')
        else:
            v = har(A, t[5], 'b', f'दोनों कथन सही हैं, पर R, A की व्याख्या नहीं करता। A का कारण: {why}')
        v['stem'] = f'{tref(ch)} के आधार पर निम्नलिखित कथनों पर विचार कीजिए।\n' + v['stem']
        return v
    return g


def g_explain(ch, pairs, words='25-30', marks=2, key='', think=False):
    def g(r):
        q, a = cp(key or ('ex' + str(id(pairs))), r, pairs)
        k = ('किसी भी तर्कसंगत उत्तर को अंक दें। अपेक्षित बिंदु: ' if think else 'मूल्य-बिंदु: ') + a
        k += f' (विषय-वस्तु {marks - 1}, भाषा-अभिव्यक्ति 1)।'
        return {'stem': f'{named(ch, q)} (लगभग {words} शब्दों में)', 'answer': a, 'key': k, 'marks': marks}
    return g


def g_long(ch, pairs, words='60-70', marks=5, key=''):
    def g(r):
        q, pts = cp(key or ('lg' + str(id(pairs))), r, pairs)
        return {'stem': f'{named(ch, q)} (लगभग {words} शब्दों में)', 'answer': pts,
                'key': f'मूल्य-बिंदु: {pts} अंक-विभाजन: विषय-वस्तु {marks - 2}, पाठ से उदाहरण/प्रसंग 1, भाषा-शुद्धता 1।',
                'marks': marks, 'minutes': marks + 3, 'gap': 'G5'}
    return g


_PART = {}
for _m in ('चला', 'लगा', 'बैठा', 'खड़ा', 'पड़ा'):
    _PART[_m] = _PART[_m[:-1] + 'ी'] = (_m, _m[:-1] + 'ी')


def gauto(text, girl):
    """Agree a verb-final phrase with the actor's gender: resolves करता/करती pairs, then turns unpaired
    habitual forms (-ता/-ती before है/और/end of sentence) and a participle before रहता/जाता the right way."""
    text = gfix(text, girl)
    src, dst = ('ता', 'ती') if girl else ('ती', 'ता')
    toks = text.split(' ')
    for i, t in enumerate(toks):
        core = t.rstrip('।,;')
        nxt = toks[i + 1].rstrip('।,;') if i + 1 < len(toks) else ''
        if len(core) > 2 and core.endswith(src) and (nxt in ('है', 'और', '') or t != core):
            toks[i] = core[:-len(src)] + dst + t[len(core):]
    for i, t in enumerate(toks):
        if i and t.rstrip('।,;')[:-2] in ('रह', 'जा') and toks[i - 1] in _PART:
            toks[i - 1] = _PART[toks[i - 1]][1 if girl else 0]
    return ' '.join(toks)


def g_situ(ch, stem, good, bad, why):
    """C3: whose action matches the chapter's idea. good/bad are verb-final phrases with gendered pairs (करता/करती)."""
    def g(r):
        gd = cp('situ' + stem[:20], r, good)
        names = r.sample(GIRLS + BOYS, 4)
        acts = [gd] + r.sample(bad, 3)
        opts = [f'{n} {gauto(a, n in GIRLS)}' for n, a in zip(names, acts)]
        return mcq(named(ch, stem), opts[0], opts[1:], f'{opts[0]}—{why}', r)
    return g


def _ex_intro(ch, poem):
    if poem:
        return f'{tref(ch)} के निम्नलिखित काव्यांश को पढ़कर प्रश्नों के उत्तर दीजिए।'
    return f'{tref(ch)} के प्रसंग पर आधारित निम्नलिखित अंश (अपने शब्दों में) पढ़कर प्रश्नों के उत्तर दीजिए।'


def g_extract_one(ch, extracts, mcq_only):
    def g(r):
        e = r.choice(extracts)
        text, qs = e[1], e[2]
        pool = [q for q in qs if (len(q) > 2 and bool(q[2])) == mcq_only]
        need(pool)
        q = r.choice(pool)
        head = _ex_intro(ch, ch.get('poem')) + f'\n{text}\nप्रश्न: '
        if mcq_only:
            return mcq(head + q[0], q[1], pick3(r, q[2]), f'अंश के आधार पर: {q[1]}।', r)
        return {'stem': head + q[0], 'answer': q[1], 'key': f'मूल्य-बिंदु: {q[1]} (2 अंक: विषय-वस्तु 1, अभिव्यक्ति 1)', 'marks': 2}
    return g


def extract_set(ch, extracts, n, mcq_only=True):
    """n questions on one extract; MCQs only (for पाठ-आधारित बहुविकल्पी) or mixed."""
    def g(r):
        e = r.choice(extracts)
        text, qs = e[1], e[2]
        pool = [q for q in qs if (len(q) > 2 and q[2])] if mcq_only else list(qs)
        need(len(pool) >= n)
        idx = sorted(r.sample(range(len(pool)), n))
        lines, ans = [_ex_intro(ch, ch.get('poem')), text], []
        marks = 0
        for i, k in enumerate(idx):
            q = pool[k]
            if len(q) > 2 and q[2]:
                opts, L = shuffled(r, q[1], q[2])
                lines.append(f'({ROMAN[i]}) {q[0]}\n{opts_line(opts)}')
                ans.append(f'({ROMAN[i]}) ({L}) {q[1]}')
                marks += 1
            else:
                lines.append(f'({ROMAN[i]}) {q[0]}')
                ans.append(f'({ROMAN[i]}) {q[1]}')
                marks += 2
        return {'stem': '\n'.join(lines), 'answer': '; '.join(ans),
                'key': ('प्रत्येक बहुविकल्पी 1 अंक' + ('' if mcq_only else ', प्रत्येक लिखित उत्तर 2 अंक') + f' (कुल {marks} अंक)। ') + '; '.join(ans) + '।',
                'marks': marks, 'minutes': marks + 2, 'gap': 'G3'}
    return g


def mcq_set(ch, rows, k):
    """k MCQs from fact rows as one item (पाठ-आधारित बहुविकल्पी प्रश्न), 1 mark each."""
    def g(r):
        need(len(rows) >= k)
        pick = r.sample(rows, k)
        lines, ans = [f'{tref(ch)} के आधार पर निम्नलिखित प्रश्नों के सही विकल्प चुनिए।'], []
        for i, (q, a, wrong) in enumerate(pick):
            opts, L = shuffled(r, a, wrong)
            lines.append(f'({ROMAN[i]}) {q}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[i]}) ({L}) {a}')
        return {'stem': '\n'.join(lines), 'answer': '; '.join(ans),
                'key': f'प्रत्येक सही विकल्प के लिए 1 अंक (कुल {k} अंक)। ' + '; '.join(ans) + '।', 'marks': k}
    return g


def short_set(ch, pairs, k, each, words='25-30'):
    def g(r):
        need(len(pairs) >= k)
        pick = r.sample(pairs, k)
        lines = [f'{tref(ch)} के आधार पर निम्नलिखित प्रश्नों के उत्तर लगभग {words} शब्दों में लिखिए।']
        ans = []
        for i, (q, a) in enumerate(pick):
            lines.append(f'({ROMAN[i]}) {q}')
            ans.append(f'({ROMAN[i]}) {a}')
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans),
                'key': f'प्रत्येक भाग {each} अंक (कुल {k * each} अंक): विषय-वस्तु {each - 1}, भाषा 1। ' + ' '.join(ans), 'marks': k * each}
    return g


def long_set(ch_pairs, k, each, words, head):
    """k long answers drawn from several chapters: ch_pairs = [(ch, (q, pts))]."""
    def g(r):
        need(len(ch_pairs) >= k)
        pick = r.sample(ch_pairs, k)
        if len({id(c) for c, _ in pick}) < k:
            raise ValueError('same chapter twice')
        lines, ans = [head], []
        for i, (c, (q, a)) in enumerate(pick):
            lines.append(f'({ROMAN[i]}) {named(c, q)}')
            ans.append(f'({ROMAN[i]}) {a}')
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans),
                'key': f'प्रत्येक भाग {each} अंक (कुल {k * each}): विषय-वस्तु {each - 1}, भाषा 1। ' + ' '.join(ans), 'marks': k * each}
    return g


# ---------------------------------------------------------------- families for a literature subtopic

def lit_families(ch, st, k, grade, first):
    out = []
    facts = st.get('facts', [])
    sid = f'{ch["title"]}:{k}'
    if facts:
        a, b = facts[0::2], facts[1::2] or facts
        out.append(F('C1', 'D1', 'mcq', g_fact(ch, a, sid + 'fa')))
        out.append(F('C1', 'D2', 'mcq', g_fact(ch, b, sid + 'fb')))
    if first and ch.get('vocab'):
        out.append(F('C1', 'D1', 'mcq', g_vocab(ch, ch['vocab'], sid + 'v')))
    if st.get('true') and st.get('false'):
        out.append(F('C2', 'D2', 'mcq', g_true(ch, st['true'], st['false'], st.get('ref'))))
        out.append(F('C2', 'D3', 'mcq', g_false(ch, st['true'], st['false'], st.get('ref'))))
    if st.get('ar'):
        out.append(F('C2', 'D3', 'mcq', g_ar(ch, st['ar']), kinds=('ar',)))
    ex = st.get('explain', [])
    if ex:
        out.append(F('C2', 'D2', 'explain', g_explain(ch, ex[0::2], '25-30', 2, sid + 'e1')))
        out.append(F('C3', 'D3', 'explain', g_explain(ch, ex[1::2] or ex, '30-40', 2, sid + 'e2')))
    inf = st.get('infer', [])
    if inf:
        out.append(F('C3', 'D2', 'mcq', g_fact(ch, inf[0::2], sid + 'i1')))
        out.append(F('C3', 'D3', 'mcq', g_fact(ch, inf[1::2] or inf, sid + 'i2')))
    if st.get('situ'):
        out.append(F('C3', 'D2', 'mcq', g_situ(ch, *st['situ'])))
    exs = [e for e in ch.get('extracts', []) if e[0] == k]
    if exs:
        out.append(F('C3', 'D2', 'mcq', g_extract_one(ch, exs, True)))
        if any(len(q) == 2 or not q[2] for e in exs for q in e[2]):
            out.append(F('C3', 'D3', 'short', g_extract_one(ch, exs, False)))
        out.append(F('C3', 'D4', 'case', extract_set(ch, exs, 4, False)))
    if st.get('think'):
        out.append(F('C4', 'D3', 'explain', g_explain(ch, st['think'], '30-40', 3, sid + 't', think=True), gap='G5'))
    if st.get('long'):
        out.append(F('C4', 'D4', 'long', g_long(ch, st['long'], '60-70' if grade < 11 else '80-100', 5, sid + 'l')))
    return out


def build_families(chapters, sid, grade, extra=None):
    """chapters: {n: ch}. Returns {subtopic id: [Family]}."""
    fams = {}
    for n, ch in chapters.items():
        cid = f'{sid}-ch{n:02d}'
        first = next((k for k, s in ch['sts'].items() if s['kind'] == 'lit'), None)
        for k, st in ch['sts'].items():
            stid = f'{cid}-st{k}'
            if st['kind'] == 'lit':
                fams[stid] = lit_families(ch, st, k, grade, k == first)
            elif st['kind'] == 'fams':
                fams[stid] = st['fn'](ch, grade)
            else:
                raise SystemExit(st['kind'])
            fams[stid] += st.get('extra', [])
    return fams


# ---------------------------------------------------------------- अपठित गद्यांश / काव्यांश (original texts)

def _pick_idx(r, theme, n_pick, must=()):
    """Ordered sentence indices for a passage: always sentence 0, every sentence in `must`, then random others,
    each pulled in together with the sentences it leans on (theme['deps'] = {i: [j, ...]})."""
    deps = theme.get('deps', {})

    def close(i, acc):
        if i not in acc:
            acc.add(i)
            for j in deps.get(i, ()):
                close(j, acc)
    idx = set()
    for i in (0, *must):
        close(i, idx)
    rest = [i for i in range(1, len(theme['sents'])) if i not in idx]
    r.shuffle(rest)
    for i in rest:
        if len(idx) >= n_pick:
            break
        close(i, idx)
    return sorted(idx)


def _wq(w):
    return w[0], w[1], (w[2] if len(w) > 2 else ())


def passage(theme, n_mcq=4, written=(2,), label='गद्यांश', n_pick=5):
    """Original passage from a theme's self-contained sentences (kept in order): n_mcq MCQs, a title MCQ and
    written questions with the given marks."""
    sents = theme['sents']

    def gen(r):
        need(len(sents) > n_pick and len(theme['written']) >= len(written))
        wqs = [_wq(w) for w in r.sample(theme['written'], len(written))]
        idx = _pick_idx(r, theme, n_pick, [i for w in wqs for i in w[2]])
        need(sum(1 for i in idx if sents[i][1]) >= n_mcq)
        text = ' '.join(sents[i][0] for i in idx)
        qi = sorted(r.sample([i for i in idx if sents[i][1]], n_mcq))
        lines = [f'निम्नलिखित {label} को ध्यानपूर्वक पढ़कर पूछे गए प्रश्नों के उत्तर दीजिए।', text]
        ans = []
        j = 0
        for i in qi:
            _, q, a, wrong = sents[i]
            opts, L = shuffled(r, a, wrong)
            lines.append(f'({ROMAN[j]}) {q}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[j]}) ({L}) {a}')
            j += 1
        t_ok = r.choice(theme['titles'])
        opts, L = shuffled(r, t_ok, theme['bad_titles'])
        lines.append(f'({ROMAN[j]}) {label} के लिए सबसे उपयुक्त शीर्षक कौन-सा है?\n{opts_line(opts)}')
        ans.append(f'({ROMAN[j]}) ({L}) {t_ok}')
        j += 1
        for m, (q, a, _) in zip(written, wqs):
            lines.append(f'({ROMAN[j]}) {q} ({m} अंक)')
            ans.append(f'({ROMAN[j]}) {a}')
            j += 1
        total = n_mcq + 1 + sum(written)
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans), 'marks': total, 'minutes': total + 3, 'gap': 'G3',
                'key': f'बहुविकल्पी प्रश्न 1-1 अंक; लिखित प्रश्न {"/".join(map(str, written))} अंक (विषय-वस्तु और अभिव्यक्ति)। कुल {total} अंक। ' + ' '.join(ans)}
    return gen


def passage_one(theme, n_pick=4):
    """Short passage with one MCQ (bank and practice forms)."""
    sents = theme['sents']

    def gen(r):
        idx = _pick_idx(r, theme, n_pick)
        text = ' '.join(sents[i][0] for i in idx)
        i = r.choice([x for x in idx[1:] if sents[x][1]] or [idx[0]])
        _, q, a, wrong = sents[i]
        need(q)
        return mcq(f'गद्यांश पढ़कर प्रश्न का उत्तर दीजिए।\n{text}\nप्रश्न: {q}', a, pick3(r, wrong),
                   f'गद्यांश के वाक्य "{sents[i][0]}" से उत्तर: {a}।', r)
    return gen


def passage_written(theme, n_pick=5):
    """Passage with one inference question (C4)."""
    sents = theme['sents']

    def gen(r):
        q, a, must = _wq(r.choice(theme['written']))
        idx = _pick_idx(r, theme, n_pick, must)
        text = ' '.join(sents[i][0] for i in idx)
        return {'stem': f'गद्यांश पढ़कर प्रश्न का उत्तर लगभग 30-40 शब्दों में दीजिए।\n{text}\nप्रश्न: {q}', 'answer': a,
                'key': f'मूल्य-बिंदु: {a} (2 अंक: विषय-वस्तु 1, अभिव्यक्ति 1)', 'marks': 2, 'gap': 'G3'}
    return gen


def kavya(poems, n_mcq=4, written=(2,)):
    """Original poem: n_mcq MCQs, a title MCQ, written questions."""
    def gen(r):
        k = r.choice(poems)
        need(len(k['qs']) >= n_mcq and len(k['written']) >= len(written))
        qs = r.sample(k['qs'], n_mcq)
        lines = ['निम्नलिखित काव्यांश को ध्यानपूर्वक पढ़कर पूछे गए प्रश्नों के उत्तर दीजिए।', k['text']]
        ans = []
        j = 0
        for q, a, wrong in qs:
            opts, L = shuffled(r, a, wrong)
            lines.append(f'({ROMAN[j]}) {q}\n{opts_line(opts)}')
            ans.append(f'({ROMAN[j]}) ({L}) {a}')
            j += 1
        t, bad = k['title']
        opts, L = shuffled(r, t, bad)
        lines.append(f'({ROMAN[j]}) काव्यांश का उपयुक्त शीर्षक है—\n{opts_line(opts)}')
        ans.append(f'({ROMAN[j]}) ({L}) {t}')
        j += 1
        for m, (q, a) in zip(written, r.sample(k['written'], len(written))):
            lines.append(f'({ROMAN[j]}) {q} ({m} अंक)')
            ans.append(f'({ROMAN[j]}) {a}')
            j += 1
        total = n_mcq + 1 + sum(written)
        return {'stem': '\n'.join(lines), 'answer': ' '.join(ans), 'marks': total, 'minutes': total + 3, 'gap': 'G3',
                'key': f'बहुविकल्पी प्रश्न 1-1 अंक; लिखित प्रश्न {"/".join(map(str, written))} अंक। कुल {total} अंक। ' + ' '.join(ans)}
    return gen


def kavya_one(poems):
    def gen(r):
        k = r.choice(poems)
        q, a, wrong = r.choice(k['qs'])
        return mcq(f'काव्यांश पढ़कर प्रश्न का उत्तर दीजिए।\n{k["text"]}\nप्रश्न: {q}', a, pick3(r, wrong), f'काव्यांश के आधार पर: {a}।', r)
    return gen


def kavya_written(poems):
    def gen(r):
        k = r.choice(poems)
        q, a = r.choice(k['written'])
        return {'stem': f'काव्यांश पढ़कर प्रश्न का उत्तर लगभग 30-40 शब्दों में दीजिए।\n{k["text"]}\nप्रश्न: {q}', 'answer': a,
                'key': f'मूल्य-बिंदु: {a} (2 अंक)', 'marks': 2, 'gap': 'G3'}
    return gen


# ---------------------------------------------------------------- written-answer generators (रचना)

CLASS_WORD = {9: 'कक्षा 9', 11: 'कक्षा 11'}


def who(r, grade):
    nm, girl = person(r)
    return nm, girl, f'{CLASS_WORD[grade]} {ge(girl, "के छात्र", "की छात्रा")} {nm}'


FORMAL_FMT = ('प्रारूप: प्रेषक का पता (परीक्षा भवन), दिनांक, सेवा में—पद और पता, विषय, संबोधन (महोदय/महोदया), '
              'मुख्य भाग (परिचय, समस्या/निवेदन, अनुरोध), धन्यवाद-सहित समापन (भवदीय/भवदीया, प्रार्थी), नाम।')
INFORMAL_FMT = 'प्रारूप: प्रेषक का पता, दिनांक, संबोधन (पूज्य/प्रिय), अभिवादन, कुशल-क्षेम, मुख्य बात, समापन, संबंध-सूचक शब्द और नाम।'


def letter_key(m):
    if m >= 7:
        return f'अंक-विभाजन ({m}): प्रारूप 2 (पता, दिनांक, संबोधन, समापन), विषय-वस्तु 3, भाषा-शुद्धता और प्रस्तुति 2। शब्द-सीमा लगभग 100-120 शब्द।'
    if m == 6:
        return 'अंक-विभाजन (6): प्रारूप 2, विषय-वस्तु 3, भाषा-शुद्धता 1। शब्द-सीमा लगभग 100-120 शब्द।'
    return 'अंक-विभाजन (5): प्रारूप 1 (पता, दिनांक, विषय, संबोधन, समापन), विषय-वस्तु 3, भाषा-शुद्धता 1। शब्द-सीमा लगभग 120 शब्द।'


def formal_letter(topics, grade, marks=7, ns='fl'):
    """topics: (to_whom, about, points)."""
    def gen(r):
        nm, girl, me = who(r, grade)
        city = r.choice(CITIES)
        sch = r.choice(SCHOOLS)
        to, subj, pts = cp(ns, r, topics)
        stem = (f'आप {city} के {sch} में {me} हैं। {to} को {subj} लगभग 100-120 शब्दों में एक औपचारिक पत्र लिखिए।')
        return {'stem': stem, 'answer': f'औपचारिक पत्र। {FORMAL_FMT} मुख्य बिंदु: {pts}', 'key': letter_key(marks),
                'marks': marks, 'minutes': 10}
    return gen


def informal_letter(topics, grade, marks=7, ns='il'):
    def gen(r):
        nm, girl = person(r)
        city = r.choice(CITIES)
        rel, subj, pts = cp(ns, r, topics)
        stem = f'आप {city} में रहने {ge(girl, "वाले", "वाली")} {nm} हैं। अपने {rel} को {subj} लगभग 100 शब्दों में पत्र लिखिए।'
        return {'stem': stem, 'answer': f'अनौपचारिक पत्र। {INFORMAL_FMT} मुख्य बिंदु: {pts}', 'key': letter_key(marks),
                'marks': marks, 'minutes': 10}
    return gen


def paragraph(topics, words='100-120', marks=7, ns='pa'):
    """topics: (title, [hint points])."""
    def gen(r):
        title, hints = cp(ns, r, topics)
        h = [hints[i] for i in sorted(r.sample(range(len(hints)), 3))] if len(hints) > 3 else hints
        stem = f'"{title}" विषय पर दिए गए संकेत-बिंदुओं के आधार पर लगभग {words} शब्दों में अनुच्छेद लिखिए।\nसंकेत-बिंदु: ' + ' • '.join(h)
        k = (f'अंक-विभाजन ({marks}): आरंभ और अंत 1, संकेत-बिंदुओं का क्रमबद्ध विस्तार {marks - 3}, भाषा-शुद्धता 2।' if marks >= 6
             else f'अंक-विभाजन ({marks}): विषय-वस्तु {marks - 2}, संगठन 1, भाषा 1।')
        return {'stem': stem, 'answer': f'अनुच्छेद में ये बिंदु क्रम से आएँ: {"; ".join(h)}। आरंभ विषय के परिचय से और अंत निष्कर्ष/संदेश से हो।',
                'key': k, 'marks': marks, 'minutes': 10}
    return gen


def dialogue(situations, marks=6, ns='dl'):
    """situations: (setting with {a} {b} and gendered pairs, points)."""
    def gen(r):
        (a, ga), (b, gb) = person(r), person(r)
        need(a != b)
        setting, pts = cp(ns, r, situations)
        setting = gfix(setting, ga)
        if ga and gb:
            setting = setting.replace('कर रहे हैं', 'कर रही हैं')
        stem = f'{setting.format(a=a, b=b)} इस विषय पर दोनों के बीच लगभग 60-80 शब्दों में संवाद लिखिए।'
        return {'stem': stem, 'answer': f'संवाद में बारी-बारी से दोनों के कथन, उचित विराम-चिह्न और स्वाभाविक भाषा। मुख्य बातें: {pts}',
                'key': f'अंक-विभाजन ({marks}): प्रारूप (पात्रों के नाम, क्रम) 1, विषय-वस्तु {marks - 3}, भाषा और विराम-चिह्न 2।', 'marks': marks, 'minutes': 8}
    return gen


ROLES = ['सांस्कृतिक सचिव', 'छात्र-परिषद के अध्यक्ष', 'छात्र-परिषद के सचिव', 'कार्यक्रम-संयोजक', 'प्रधानाचार्य']


def notice(events, marks=5, ns='nt'):
    """events: (event, details)."""
    def gen(r):
        sch = r.choice(SCHOOLS)
        city = r.choice(CITIES)
        ev, det = cp(ns, r, events)
        role = r.choice(ROLES)
        stem = f'{city} के {sch} के {role} की ओर से "{ev}" के लिए लगभग 50 शब्दों में एक सूचना लिखिए।'
        return {'stem': stem, 'answer': f'सूचना: संस्था का नाम, "सूचना" शीर्षक, दिनांक, विषय, विवरण ({det}), सूचना देने वाले का नाम/पद।',
                'key': f'अंक-विभाजन ({marks}): प्रारूप (शीर्षक, दिनांक, नाम-पद) 2, विषय-वस्तु {marks - 3}, भाषा 1।', 'marks': marks, 'minutes': 6}
    return gen


def task(rows, marks, words, keytxt, ns):
    """Generic writing task: rows of (stem template with {name}/{city}/{school}, answer points)."""
    def gen(r):
        t, pts = cp(ns, r, rows)
        nm, girl = person(r)
        s = t.format(name=nm, city=r.choice(CITIES), school=r.choice(SCHOOLS), ge=ge(girl, 'के', 'की'))
        return {'stem': f'{s} (लगभग {words} शब्दों में)', 'answer': pts, 'key': f'मूल्य-बिंदु: {pts} {keytxt}', 'marks': marks,
                'minutes': marks + 4, 'gap': 'G5'}
    return gen


# ---------------------------------------------------------------- generic fact-table families (writing forms, media, skills)

def table_fams(ch, tab, ns, kinds_long=None):
    """tab: dict(facts=[(q,a,[w])], true, false, ar, explain, apply=[(q,a,[w])], think, tasks=[gen,...]).
    Non-literature subtopic (stems need not name a text)."""
    nm = lambda q: q  # noqa: E731
    out = []
    facts = tab['facts']
    out.append(F('C1', 'D1', 'mcq', _fact(facts[0::2], ns + 'fa')))
    out.append(F('C1', 'D2', 'mcq', _fact(facts[1::2], ns + 'fb')))
    if tab.get('true'):
        out.append(F('C2', 'D2', 'mcq', _tf(tab['true'], tab['false'], tab['ref'], True)))
        out.append(F('C2', 'D3', 'mcq', _tf(tab['true'], tab['false'], tab['ref'], False)))
    if tab.get('ar'):
        out.append(F('C2', 'D3', 'mcq', _ar(tab['ar']), kinds=('ar',)))
    ex = tab.get('explain', [])
    if ex:
        out.append(F('C2', 'D2', 'explain', _ex(ex[0::2], ns + 'e1', '25-30', 2)))
        out.append(F('C3', 'D3', 'explain', _ex(ex[1::2] or ex, ns + 'e2', '30-40', 2)))
    ap = tab.get('apply', [])
    if ap:
        out.append(F('C3', 'D2', 'mcq', _fact(ap[0::2], ns + 'a1')))
        out.append(F('C3', 'D3', 'mcq', _fact(ap[1::2] or ap, ns + 'a2')))
    for g in tab.get('apply_gens', []):
        out.append(F(g[0], g[1], g[2], g[3], **(g[4] if len(g) > 4 else {})))
    if tab.get('think'):
        out.append(F('C4', 'D3', 'explain', _ex(tab['think'], ns + 't', '30-40', 3, think=True), gap='G5'))
    for t in tab.get('tasks', []):
        out.append(t)
    return out


def _fact(rows, key):
    def g(r):
        q, a, wrong = cp(key, r, rows)[:3]
        return mcq(q, a, pick3(r, wrong), f'सही उत्तर: {a}।', r)
    return g


def _tf(true, false, ref, want_true):
    def g(r):
        if want_true:
            t = r.choice(true)
            return mcq(r.choice(LEAD_T).format(T=ref), t, r.sample(false, 3), f'सही कथन: "{t}"', r)
        f = r.choice(false)
        return mcq(r.choice(LEAD_F).format(T=ref), f, r.sample(true, 3), f'"{f}"—यह कथन सही नहीं है; शेष तीनों सही हैं।', r)
    return g


def _ar(tuples):
    def g(r):
        t = r.choice(tuples)
        A, Af, R, Rf, why = t[:5]
        codes = ['a'] + (['c'] if Rf else []) + (['d'] if Af else []) + (['b'] if len(t) > 5 and t[5] else [])
        code = r.choice(codes)
        if code == 'a':
            return har(A, R, 'a', f'दोनों सही हैं और R, A की व्याख्या करता है: {why}')
        if code == 'c':
            return har(A, Rf, 'c', f'A सही है, पर R गलत है। वास्तव में—{R}')
        if code == 'd':
            return har(Af, R, 'd', f'A गलत है; सही बात—{A} R सही है।')
        return har(A, t[5], 'b', f'दोनों सही हैं, पर R, A की व्याख्या नहीं करता। A का कारण: {why}')
    return g


def _ex(pairs, key, words, marks, think=False):
    def g(r):
        q, a = cp(key, r, pairs)
        k = ('किसी भी तर्कसंगत उत्तर को अंक दें। अपेक्षित बिंदु: ' if think else 'मूल्य-बिंदु: ') + a + f' ({marks} अंक)।'
        return {'stem': f'{q} (लगभग {words} शब्दों में)', 'answer': a, 'key': k, 'marks': marks}
    return g
