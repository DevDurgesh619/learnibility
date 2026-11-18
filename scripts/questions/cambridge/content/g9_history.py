"""Cambridge IGCSE History 0470, year 1 (grade 9): Option B core content, the 20th century.

Paper 1 structured questions are (a) describe [4], (b) explain [6], (c) 'How far' / 'How important' [10],
marked by the board's levels; Paper 2 is a source-based question on one core topic (message,
purpose, comparison, utility, 'convincing evidence').

Each topic is a knowledge pack (key terms, dated events, recall MCQs, (a)/(b)/(c) prompts with
indicative content, claims to check, Paper 1 stimuli and Paper 2 sources) turned into items by the
builders below. Source texts are either well-attested words from the period (quoted from standard
English translations, abridged where marked) or are labelled 'adapted' / 'illustrative' and
attributed to unnamed writers; no invented words are put into the mouth of a real person.
cambridge-g10-history (the depth studies) imports these builders.
"""
import re as _re

from ._lib import topic, mcq, person, city, CTX

PROFILE = {'mark_scale': {'short': (2, 2), 'long': (2.5, 1.5), 'case': (2.33, 1.5)}, 'wordy': True}
CHAPTERS = {}
LET = 'abcdefgh'


def cap(s):
    return s[:1].upper() + s[1:]


def low(s):
    return s[:1].lower() + s[1:]


_COMMON = set('it its the a an this these they he she his her there one some many most written as to figures photographs statistics images'.split())


def low2(s):
    """Lower-case the first letter only when the first word is an ordinary word (keeps names such as Stalin)."""
    w = s.split(' ', 1)[0].lower()
    return low(s) if w in _COMMON else s


def T(name, *extra):
    return topic(name, name.lower(), *extra)


def _dot(s):
    s = s.strip()
    return s if s[-1:] in '.?!”' else s + '.'


def _mins(m):
    return round(max(1.0, m * 1.5) * 2) / 2


# ============================================================== mark schemes (0470 levels)

A_KEY = 'One mark for each relevant point; a further mark for supporting detail, up to 4 marks.'
B_KEY = ('Level 1 (1): general answer. Level 2 (2-3): identifies and/or describes reasons. '
         'Level 3 (4-5): explains one reason. Level 4 (6): explains two or more reasons.')
C_KEY = ('Level 1 (1): general answer. Level 2 (2-3): identifies and/or describes. Level 3 (4-6): explains one side. '
         'Level 4 (7-9): explains both sides. Level 5 (10): explains both sides and reaches a supported judgement on "how far" / "how important".')
MSG_KEY = ('Level 1 (1): describes surface features of the source. Level 2 (2-3): valid interpretation (sub-message) supported by details. '
           'Level 3 (4-5): main message supported by details of the source. Level 4 (6): main message plus the author\'s point of view, set in context.')
WHY_KEY = ('Level 1 (1): undeveloped answer. Level 2 (2-3): explains context OR message only. Level 3 (4-5): explains the purpose / intended impact on the audience. '
           'Level 4 (6-7): explains the purpose in the specific context of the date, supported by the source and own knowledge.')
USE_KEY = ('Level 1 (1): undeveloped or generic comment. Level 2 (2-3): useful or not useful based on face-value content. '
           'Level 3 (4-5): uses content checked against own knowledge. Level 4 (6-7): evaluates the provenance (author, audience, purpose, date) to judge usefulness.')
REL_KEY = ('Level 1 (1): generic comment (e.g. "it is biased"). Level 2 (2-3): reliability judged on content or type only. '
           'Level 3 (4-5): explains reliability using the author, date and purpose. Level 4 (6): reaches a balanced judgement using provenance and cross-reference with own knowledge.')
SUP_KEY = ('Level 1 (1): undeveloped yes/no. Level 2 (2-3): uses details of the source to support OR challenge. '
           'Level 3 (4-5): uses details to support AND challenge, or explains the source in context. Level 4 (6): judgement that also considers the provenance of the source.')
CMP_KEY = ('Level 1 (1): undeveloped comparison. Level 2 (2-3): compares content, agreement OR disagreement, with details. '
           'Level 3 (4-5): compares agreement AND disagreement with details. Level 4 (6-7): compares the overall messages / points of view, supported, and explains why they differ (provenance).')
CON_KEY = ('Level 1 (1-2): general answer or describes the sources. Level 2 (3-5): uses sources to support OR challenge the statement. '
           'Level 3 (6-8): uses sources to support AND challenge. Level 4 (9-11): also evaluates the sources (provenance, cross-reference). '
           'Level 5 (12): as Level 4 with a balanced, supported judgement on "how far".')


def a_key(points):
    return f'{A_KEY} Indicative content: ' + ' '.join(_dot(p) for p in points) + ' [4]'


def b_key(reasons):
    return f'{B_KEY} Indicative content: ' + ' '.join(_dot(x) for x in reasons) + ' [6]'


def c_key(pro, con, judge):
    return (f'{C_KEY} Agree / supporting: ' + ' '.join(_dot(x) for x in pro) + ' Disagree / other factors: ' +
            ' '.join(_dot(x) for x in con) + ' Possible judgement: ' + _dot(judge) + ' [10]')


def c_ans(pro, con, judge):
    return 'For: ' + ' '.join(_dot(x) for x in pro) + ' Against: ' + ' '.join(_dot(x) for x in con) + ' Judgement: ' + _dot(judge)


# ============================================================== generic builders

def _year_ds(y):
    return [str(y + d) for d in (-11, -6, -3, -1, 2, 4, 7, 13)]


def add_terms(t, terms):
    """terms: [(term, definition)] -> C1 items both ways (auto-paired by core)."""
    if len(terms) < 4:
        return
    t.fixed('C1', (1, 2), [(f'Name the term that matches this description: “{d}”.', cap(term), f'{cap(term)}: {d}. [1]',
                            [cap(x) for x, _ in terms if x != term]) for term, d in terms])
    ents = []
    for term, d in terms:
        ds = [cap(y) + '.' for x, y in terms if x != term]
        t.__dict__.setdefault('_termds', []).append((ds, cap(d) + '.'))
        ents.append((f'What is meant by “{term}”?', cap(d) + '.', f'{cap(term)}: {d}. [1]', ds))
    t.fixed('C1', (2, 3), ents)


def finalize(chapters):
    """Widen definition-MCQ distractors with definitions from the other topics of the same chapter,
    so that option sets differ between items (the validator compares stems together with options);
    add a one-mark source-inference MCQ to every topic with sources."""
    for n, topics in chapters.items():
        for t in topics:  # data-response templates first, so that the bank's rotation reaches them
            t.templates.sort(key=lambda tp: 0 if tp.type == 'numerical' else 1)
        allsrc = [s for t in topics for s in (getattr(t, 'pack', None) or {}).get('src', [])]
        for t in topics:
            mine = (getattr(t, 'pack', None) or {}).get('src', [])
            if not mine or len(allsrc) < 5:
                continue

            def smcq(r, D, mine=mine, allsrc=allsrc):
                s = r.choice(mine)
                pool = [x['infer'] for x in allsrc if x is not s and x['infer'] != s['infer']]
                opts, a = mcq(r, s['infer'], r.sample(pool, 3))
                L = r.choice('ABCD')
                return {'stem': _src_intro(r, s, L) + f' Which statement best describes the message of Source {L}?', 'options': opts, 'answer': a,
                        'key': f'Only this statement matches the content of Source {L}. [1]', 'marks': 1, 'minutes': 1.5}
            smcq.__name__ = 'source_mcq'
            t.add('C3', (1, 2), 'mcq')(smcq)
        cl = [(c, ok, why) for t in topics for c, ok, why in (getattr(t, 'pack', None) or {}).get('claims', [])]
        fl = [c for c, ok, _ in cl if not ok]
        for t in topics:
            tr = [(c, why) for c, ok, why in (getattr(t, 'pack', None) or {}).get('claims', []) if ok]
            if not tr or len(fl) < 3:
                continue

            def cmcq(r, D, tr=tr, fl=fl):
                c, why = r.choice(tr)
                opts, a = mcq(r, c, r.sample(fl, 3))
                return {'stem': r.choice(['Which of these statements is accurate?', 'Which one of the following statements is correct?']), 'options': opts, 'answer': a,
                        'key': f'{_dot(why)} The other statements are inaccurate. [1]', 'marks': 1, 'minutes': 1}
            cmcq.__name__ = 'claim_mcq'
            t.add('C2', (1, 2, 3), 'mcq')(cmcq)
        pool = [(id(t), a) for t in topics for _, a in getattr(t, '_termds', [])]
        for t in topics:
            for ds, a in getattr(t, '_termds', []):
                ds.extend(x for i, x in pool if i != id(t) and x != a and x not in ds)


def add_dates(t, dates):
    """dates: [(clause, year[, month])] -> C1 year MCQs and C2 chronology items."""
    if not dates:
        return
    t.fixed('C1', (1, 2), [(f'In which year did this happen: {d[0]}?', str(d[1]), f'{cap(d[0])}: {d[1]}. [1]', _year_ds(d[1])) for d in dates])
    if len(dates) < 4:
        return

    def chrono(r, D):
        n = min(len(dates), 4 if D <= 2 else 5)
        ev = r.sample(dates, n)
        keys = [(d[1], d[2] if len(d) > 2 else 0) for d in ev]
        for i in range(n):
            for j in range(i + 1, n):
                if keys[i][0] == keys[j][0] and (D <= 2 or keys[i][1] == 0 or keys[j][1] == 0 or keys[i][1] == keys[j][1]):
                    return None
        lab = 'ABCDE'[:n]
        order = sorted(range(n), key=lambda i: keys[i])
        lead = r.choice(['Put these events in chronological order, starting with the earliest.',
                         'Arrange these events in the order in which they happened, earliest first.',
                         'Sequence these events from earliest to latest.'])
        stem = lead + ' ' + ' '.join(f'{lab[i]}: {cap(ev[i][0])}.' for i in range(n))
        mk = 2
        if D >= 3:
            stem += ' Then explain how the earliest event helped to lead to a later one in your sequence.'
            mk = 4
        ans = ', '.join(lab[i] for i in order) + ' (' + '; '.join(f'{lab[i]} {ev[i][1]}' for i in order) + ')'
        key = f'Correct order {ans}: 2 marks if all correct, 1 mark if one adjacent pair is reversed.'
        if D >= 3:
            key += ' Up to 2 further marks for a valid, explained link between the earliest event and a later one.'
        return {'stem': stem, 'answer': ans + ('. Link: an explained causal connection from own knowledge.' if D >= 3 else ''),
                'key': key + f' [{mk}]', 'type': 'short', 'marks': mk, 'minutes': _mins(mk)}
    t.add('C2', (1, 2, 3), 'short')(chrono)

    def first(r, D):
        ev = r.sample(dates, 4)
        keys = [(d[1], d[2] if len(d) > 2 else 0) for d in ev]
        if len({k[0] for k in keys}) < 4 and (D <= 1 or len(set(keys)) < 4 or any(k[1] == 0 for k in keys)):
            return None
        last = r.random() < 0.4
        o = sorted(range(4), key=lambda i: keys[i])
        i = o[-1] if last else o[0]
        opts, a = mcq(r, cap(ev[i][0]), [cap(ev[j][0]) for j in range(4) if j != i])
        return {'stem': f'Which of these events happened {"last" if last else "first"}?', 'options': opts, 'answer': a,
                'key': f'{cap(ev[i][0])} ({ev[i][1]}); ' + '; '.join(f'{low2(ev[j][0])} ({ev[j][1]})' for j in o if j != i) + '. [1]', 'marks': 1, 'minutes': 1}
    t.add('C2', (1, 2, 3), 'mcq')(first)


def add_mcqs(t, entries, C='C1', D=(1, 2, 3)):
    """entries: (stem, answer, [3+ distractors], key-with-[1]); stand-alone (not auto-paired)."""
    for stem, ans, ds, key in entries:
        def fn(r, D_, stem=stem, ans=ans, ds=ds, key=key):
            opts, a = mcq(r, ans, list(ds))
            return {'stem': stem, 'options': opts, 'answer': a, 'key': key, 'marks': 1, 'minutes': 1}
        fn.__name__ = 'mcq'
        t.add(C, D, 'mcq')(fn)


def add_claims(t, claims):
    """claims: [(claim, is_correct, explanation)] -> C2 spot-the-error items."""
    ents = []
    for i, (c, ok, why) in enumerate(claims):
        lead = ['A student writes:', 'In a revision class, a student says:', 'A revision website states:', 'A classmate claims:'][i % 4]
        ents.append((f'{lead} “{c}” Is this accurate? Explain your answer using your own knowledge.', ('Accurate. ' if ok else 'Not accurate. ') + why,
                     '1 mark for a correct judgement; 1 mark for accurate supporting knowledge [2]'))
    t.fixed('C2', (1, 2, 3), ents, type='explain')


_SW = set(('which their about there would could after before between explain describe answer important reasons reason other these those where while during '
            'nazis nazism german germany germans soviet union russia russian british britain american states united world country countries people government '
            'first second years since under against through allied allies forces troops'.split()))


def _kw(s):
    return {w for w in _re.findall(r"[a-z]+", s.lower()) if len(w) >= 5 and w not in _SW}


def _stim(r, P, q=None):
    """A Paper 1 style stimulus sentence; when q is given, only one that shares a key word with the question."""
    st = [x for x in (P.get('stim') or []) if x]
    if q is not None:
        k = _kw(q)
        st = [x for x in st if _kw(x) & k]
    return r.choice(st) if st else ''


def add_describe(t, P):
    """P['a']: [(question, plural noun phrase, [points])] -> (a)-style [4] items (C2) and 'Identify two' [2] (C1)."""
    ents = P.get('a', [])
    for q, np, pts in ents:
        def fa(r, D, q=q, pts=pts):
            s = _stim(r, P, q) if r.random() < 0.75 else ''
            return {'stem': (s + ' ' + q).strip(), 'answer': ' '.join(_dot(p) for p in pts), 'key': a_key(pts),
                    'type': 'short', 'marks': 4, 'minutes': 5}
        fa.__name__ = 'describe'
        t.add('C2', (2, 3, 4), 'short')(fa)

        def fi(r, D, np=np, pts=pts):
            k = 2 if D <= 2 else 3
            if len(pts) < k + 1:
                k = 2
            w = {2: 'two', 3: 'three'}[k]
            return {'stem': f'Identify {w} {np}.', 'answer': ' '.join(_dot(p) for p in pts[:k]),
                    'key': f'1 mark for each, any {w} from: ' + ' '.join(_dot(p) for p in pts) + f' [{k}]', 'type': 'short', 'marks': k, 'minutes': k}
        fi.__name__ = 'identify'
        t.add('C1', (1, 2, 3), 'short')(fi)


def add_explain(t, P):
    """P['b']: [(why-question, [explained reasons])] -> (b)-style [6] items (C2)."""
    for q, rs in P.get('b', []):
        def fb(r, D, q=q, rs=rs):
            if D <= 2 and CTX.get('want_marks') == 1:
                return {'stem': f'{q} Give one reason.', 'answer': _dot(rs[0]),
                        'key': '1 mark for a valid reason, for example: ' + ' '.join(_dot(x) for x in rs) + ' [1]', 'type': 'explain', 'marks': 1, 'minutes': 1}
            if D <= 2:
                return {'stem': f'{q} Give two reasons.', 'answer': ' '.join(_dot(x) for x in rs[:2]),
                        'key': '1 mark for each valid reason, any two from: ' + ' '.join(_dot(x) for x in rs) + ' [2]', 'type': 'explain', 'marks': 2, 'minutes': 2.5}
            s = _stim(r, P, q) if r.random() < 0.7 else ''
            tail = r.choice(['', ' Explain your answer.']) if not q.startswith('Explain') else ''
            return {'stem': (s + ' ' + q + tail).strip(), 'answer': ' '.join(_dot(x) for x in rs), 'key': b_key(rs),
                    'type': 'explain', 'marks': 6, 'minutes': 8}
        fb.__name__ = 'explain'
        t.add('C2', (2, 3, 4), 'explain')(fb)


def _c_stem(r, e, P, hints=True):
    q = e['q']
    if q.startswith('‘') or q.startswith('“'):
        stem = q + ' ' + r.choice(['How far do you agree with this statement? Explain your answer.',
                                   'How far do you agree? Explain your answer.'])
    else:
        stem = q + ' Explain your answer.'
    if r.random() < 0.6:
        s = _stim(r, P, q)
        stem = (s + ' ' + stem).strip()
    if hints and e.get('hints') and r.random() < 0.5:
        hs = r.sample(list(e['hints']), min(len(e['hints']), r.choice([2, 3])))
        stem += ' In your answer you may wish to consider: ' + '; '.join(hs) + '.'
    return stem


def add_essays(t, P):
    """P['c']: [dict(q, pro, con, judge[, hints])] -> (c)-style [10] essays (C4, long)."""
    for e in P.get('c', []):
        def fc(r, D, e=e):
            if D <= 2:
                q = e['q'].strip('‘’“”').rstrip('.')
                stem = (f'Consider this view: “{q}.” Give one reason to agree and one reason to disagree.' if not q.startswith('How')
                        else f'{q} Give one point for and one point against.')
                return {'stem': stem, 'answer': c_ans(e['pro'][:1], e['con'][:1], e['judge']),
                        'key': '2 marks for an explained point for; 2 marks for an explained point against (1 mark if only identified) [4]',
                        'type': 'long', 'marks': 4, 'minutes': 6}
            return {'stem': _c_stem(r, e, P), 'answer': c_ans(e['pro'], e['con'], e['judge']), 'key': c_key(e['pro'], e['con'], e['judge']),
                    'type': 'long', 'marks': 10, 'minutes': 15}
        fc.__name__ = 'essay'
        t.add('C4', (2, 3, 4, 5), 'long')(fc)


def add_paper1(t, P):
    """Full Paper 1 structured question (a)(b)(c) [20] and part-sets, chosen to fit the wanted marks."""
    A, B, Cs = P.get('a', []), P.get('b', []), P.get('c', [])
    if not (A and B and Cs):
        return

    def parts(r):
        qa, _, pa = r.choice(A)
        ka = _kw(qa + ' ' + ' '.join(pa))
        sb = [len(ka & _kw(x[0] + ' ' + ' '.join(x[1]))) for x in B]
        qb, rb = r.choice([x for x, v in zip(B, sb) if v == max(sb)] if max(sb) > 0 and r.random() < 0.85 else B)
        kb = ka | _kw(qb + ' ' + ' '.join(rb))
        sc = [len(kb & _kw(e['q'] + ' ' + ' '.join(e['pro'] + e['con']))) for e in Cs]
        ec = r.choice([x for x, v in zip(Cs, sc) if v == max(sc)] if max(sc) > 0 and r.random() < 0.85 else Cs)
        pa_ = (qa, ' '.join(_dot(p) for p in pa), a_key(pa), 4)
        pb_ = (qb, ' '.join(_dot(x) for x in rb), b_key(rb), 6)
        pc_ = (_c_stem(r, ec, {'stim': ['']}, hints=False), c_ans(ec['pro'], ec['con'], ec['judge']), c_key(ec['pro'], ec['con'], ec['judge']), 10)
        return pa_, pb_, pc_

    def assemble(r, chosen, typ):
        s = _stim(r, P, ' '.join(c[0] for c in chosen))
        if len(chosen) == 1:
            q, a, k, m = chosen[0]
            return {'stem': (s + ' ' + q).strip(), 'answer': a, 'key': k, 'marks': m, 'minutes': _mins(m), 'type': typ}
        stem = (s + ' ' + ' '.join(f'({LET[i]}) {c[0]} [{c[3]}]' for i, c in enumerate(chosen))).strip()
        return {'stem': stem, 'answer': ' '.join(f'({LET[i]}) {c[1]}' for i, c in enumerate(chosen)),
                'key': ' '.join(f'({LET[i]}) {c[2]}' for i, c in enumerate(chosen)),
                'marks': sum(c[3] for c in chosen), 'minutes': _mins(sum(c[3] for c in chosen)), 'type': typ}

    def p1_full(r, D):
        pa, pb, pc = parts(r)
        opts = [[pa, pb, pc], [pb, pc], [pa, pc]]
        want = CTX.get('want_marks')
        if want and want <= 12 and r.random() < 0.6:
            ch = [pa, pc] if r.random() < 0.5 else [pb, pc]
        elif D >= 4 or not want:
            ch = r.choice([opts[0], opts[0], opts[1]])
        else:
            ch = r.choice(opts)
        return assemble(r, ch, 'long')
    p1_full.__name__ = 'paper1'
    t.add('C4', (3, 4, 5), 'long')(p1_full)

    def p1_ab(r, D):
        pa, pb, _ = parts(r)
        want = CTX.get('want_marks') or 0
        if want == 4:
            ch = [pa]
        elif want >= 10:
            ch = [pa, pb]
        else:
            ch = [pa, pb] if (D >= 3 and want >= 4) or r.random() < 0.4 else [pa]
        return assemble(r, ch, 'case' if len(ch) > 1 else 'short')
    p1_ab.__name__ = 'paper1ab'
    t.add('C3', (2, 3, 4, 5), 'case')(p1_ab)


# ---------------------------------------------------------------- Paper 2 sources

def _is_cartoon(s):
    return 'cartoon' in s['prov'] or 'poster' in s['prov']


def _src_intro(r, s, L, multi=False):
    if multi:
        return (f'Source {L}: {s["prov"]}. “{s["text"]}”' if not s.get('visual') else f'Source {L}: {s["prov"]}. {s["text"]}')
    return r.choice([
        f'Study Source {L}. Source {L}: {s["prov"]}. “{s["text"]}”',
        f'Source {L} is {s["prov"]}. “{s["text"]}” Study the source.',
        f'Read Source {L} carefully. “{s["text"]}” ({cap(s["prov"])}.)',
    ]) if not s.get('visual') else r.choice([
        f'Study Source {L}, {s["prov"]}. {s["text"]}',
        f'Source {L} is {s["prov"]}. {s["text"]} Study the source.',
    ])


def _src_parts(s, L, P):
    enq, claim = P.get('enq', 'this topic'), P.get('claim')
    vis = _is_cartoon(s)
    who = 'the cartoonist' if 'cartoon' in s['prov'] else ('the artist' if 'poster' in s['prov'] else 'the author')
    stance = s.get('stance')
    sup = ('Supports: ' if stance else 'Challenges: ') + s.get('why', s['infer'])
    out = [
        lambda r: (f'What is the message of Source {L}? Explain your answer using details of the source.' if vis else
                   f'What impression does Source {L} give of {s["about"]}? Explain your answer using details of the source.',
                   s['infer'] + f' Purpose / point of view of {who}: {low2(s["purpose"])}', MSG_KEY + ' [6]'),
        lambda r: (f'Why was Source {L} {"published" if s.get("published", True) else "produced"} at this time? Explain your answer using details of the source and your knowledge.',
                   s['purpose'] + (' Context: ' + s['context'] if s.get('context') else ''), WHY_KEY + ' [7]'),
        lambda r: (f'How useful is Source {L} as evidence about {enq}? Explain your answer using details of the source and your knowledge.',
                   f'Useful: {s["infer"]} Provenance: {s["plus"]}. Limitations: {s["minus"]}. It does not show: {_dot(s["missing"])}',
                   USE_KEY + ' [7]'),
        lambda r: (f'How reliable is Source {L} as an account of {s["about"]}? Explain your answer.',
                   f'Reliable because {low2(s["plus"])}. Less reliable because {low2(s["minus"])}. Judgement: reliable as evidence of this point of view on {s["about"]}, but it needs cross-checking with other evidence.',
                   REL_KEY + ' [6]'),
        lambda r: (f'Use your own knowledge to explain one thing about {enq} that Source {L} does not tell us.', s['missing'],
                   '1 mark for a relevant point from own knowledge; up to 2 further marks for development and explaining why it matters [3]'),
    ]
    if s.get('kind') == 'secondary':
        out.pop(1)
    if claim and stance is not None:
        out.insert(2, lambda r: (f'Does Source {L} support the view that {claim}? Explain your answer using details of the source and your knowledge.',
                                 sup + f' However, {low2(s["minus"])}.', SUP_KEY + ' [6]'))
    return out


def _compose_src(r, intro, parts, want, k):
    built = [p(r) for p in parts]
    marks = [int(_re.findall(r'\[(\d+)\]', b[2])[-1]) for b in built]
    best = None
    for _ in range(40):
        n = r.choice(k)
        idx = sorted(r.sample(range(len(built)), min(n, len(built))))
        tot = sum(marks[i] for i in idx)
        if tot > 20:
            continue
        sc = abs(tot - want) if want else 0
        if best is None or sc < best[0]:
            best = (sc, idx, tot)
        if sc == 0:
            break
    if not best:
        return None
    _, idx, tot = best
    if len(idx) == 1:
        q, a, kk = built[idx[0]]
        return {'stem': intro + ' ' + q, 'answer': a, 'key': kk, 'marks': tot, 'minutes': _mins(tot), 'type': 'case'}
    return {'stem': intro + ' ' + ' '.join(f'({LET[j]}) {built[i][0]} [{marks[i]}]' for j, i in enumerate(idx)),
            'answer': ' '.join(f'({LET[j]}) {built[i][1]}' for j, i in enumerate(idx)),
            'key': ' '.join(f'({LET[j]}) {built[i][2]}' for j, i in enumerate(idx)),
            'marks': tot, 'minutes': _mins(tot), 'type': 'case'}


def add_sources(t, P):
    srcs = P.get('src', [])
    for s in srcs:
        def f3(r, D, s=s):
            L = r.choice('ABCD')
            k = (1,) if D <= 2 else ((1, 2) if D == 3 else (2,))
            return _compose_src(r, _src_intro(r, s, L), _src_parts(s, L, P), CTX.get('want_marks'), k)
        f3.__name__ = 'source'
        t.add('C3', (2, 3, 4, 5), 'case')(f3)

        def f4(r, D, s=s):
            L = r.choice('ABCDE')
            return _compose_src(r, _src_intro(r, s, L), _src_parts(s, L, P), CTX.get('want_marks'), (2, 3))
        f4.__name__ = 'source4'
        t.add('C4', (3, 4, 5), 'case')(f4)

        def f2(r, D, s=s):
            L = r.choice('ABCD')
            det = _re.split(r'(?<=[.!?…])\s', s['text'])[0].rstrip('.')
            det = (f'“{det}”' if not s.get('visual') else det[:1].lower() + det[1:]) if len(det) < 160 else 'a relevant quotation or feature of the source'
            if (CTX.get('want_marks') or 0) >= 4:
                q = r.choice([f'What can you learn from Source {L} about {s["about"]}? Support your answer with details from the source.',
                              f'What does Source {L} tell you about {s["about"]}? Use details of the source to support your answer.'])
                return {'stem': _src_intro(r, s, L) + ' ' + q, 'answer': s['infer'] + f' Supporting details: for example, {det}; each detail should be linked to an inference.',
                        'key': '1 mark for each valid inference and 1 mark for each supporting detail from the source, up to [4]', 'type': 'short', 'marks': 4, 'minutes': 5}
            q = r.choice([f'What can you infer from Source {L} about {s["about"]}? Support your answer with a detail from the source.',
                          f'Give one thing Source {L} suggests about {s["about"]} and a detail from the source that shows it.'])
            return {'stem': _src_intro(r, s, L) + ' ' + q, 'answer': s['infer'] + f' Supporting detail: for example, {det}.',
                    'key': '1 mark for a valid inference; 1 mark for a supporting detail from the source [2]', 'type': 'short', 'marks': 2, 'minutes': 2.5}
        f2.__name__ = 'source2'
        t.add('C3', (1, 2, 3), 'short')(f2)
    if len(srcs) >= 2:
        def cmp2(r, D):
            a, b = r.sample(srcs, 2)
            la, lb = r.choice([('A', 'B'), ('B', 'C'), ('C', 'D')])
            ia, ib = _src_intro(r, a, la, True), _src_intro(r, b, lb, True)
            q = r.choice([f'How far do Sources {la} and {lb} agree about {P.get("enq", "this topic")}? Explain your answer using details of the sources.',
                          f'How similar are Sources {la} and {lb}? Explain your answer using details of the sources.'])
            same = a.get('stance') == b.get('stance')
            if a.get('stance') is None or b.get('stance') is None:
                ans = (f'Source {la}: {a["infer"]} Source {lb}: {b["infer"]} Agreements and differences should be identified in the details of what each source says about {P.get("enq", "this topic")}. '
                       f'Their different origins help explain this: {la} is {a["prov"]}; {lb} is {b["prov"]}.')
                return {'stem': r.choice(['Study Sources %s and %s.' % (la, lb), 'Compare the two sources below.']) + f' {ia} {ib} {q}', 'answer': ans, 'key': CMP_KEY + ' [7]', 'marks': 7, 'minutes': 10, 'type': 'case'}
            ans = (f'Source {la}: {a["infer"]} Source {lb}: {b["infer"]} ' +
                   ('Agreement: both ' + ('support' if a.get('stance') else 'challenge') + f' the view that {P.get("claim", "the statement")}. ' if same and P.get('claim') else
                    'Disagreement: they take different views' + (f' on whether {P["claim"]}. ' if P.get('claim') else '. ')) +
                   f'Their different origins help explain this: {la} is {a["prov"]}; {lb} is {b["prov"]}.')
            return {'stem': r.choice(['Study Sources %s and %s.' % (la, lb), 'Compare the two sources below.']) + f' {ia} {ib} {q}', 'answer': ans, 'key': CMP_KEY + ' [7]', 'marks': 7, 'minutes': 10, 'type': 'case'}
        cmp2.__name__ = 'compare'
        t.add('C3', (3, 4, 5), 'case')(cmp2)
        if P.get('claim'):
            def conv(r, D):
                st = [x for x in srcs if x.get('stance') is not None]
                n = min(len(st), 2 if D <= 3 else 3)
                if n < 2:
                    return None
                ss = r.sample(st, n)
                labs = 'ABC'[:n]
                intro = r.choice(['Study the sources.', 'Read the sources carefully.', 'Study Sources ' + ', '.join(labs) + '.']) + ' ' + ' '.join(_src_intro(r, s, L, True) for s, L in zip(ss, labs))
                names = ', '.join(labs[:-1]) + ' and ' + labs[-1]
                q = f'How far do Sources {names} provide convincing evidence that {P["claim"]}? Use the sources to explain your answer.'
                sup = [L for s, L in zip(ss, labs) if s.get('stance')]
                ch = [L for s, L in zip(ss, labs) if s.get('stance') is False]
                ans = ' '.join(f'Source {L} ' + ('supports' if s.get('stance') else 'challenges') + f': {s.get("why", s["infer"])} Reliability: {s["minus"]}.'
                               for s, L in zip(ss, labs))
                ans += f' Overall: {len(sup)} source(s) support ({", ".join(sup) or "none"}) and {len(ch)} challenge ({", ".join(ch) or "none"}); a judgement must weigh how convincing each is given its provenance.'
                return {'stem': f'{intro} {q}', 'answer': ans, 'key': CON_KEY + ' [12]', 'marks': 12, 'minutes': 18, 'type': 'case'}
            conv.__name__ = 'convincing'
            t.add('C4', (3, 4, 5), 'case')(conv)


def _markify(t, start):
    """Give fixed items the marks stated in their key ([n]) so marks and key agree."""
    for tpl in t.templates[start:]:
        if tpl.name != 'fixed':
            continue

        def fn(r, D, f=tpl.fn):
            q = f(r, D)
            if q and 'marks' not in q:
                m = _re.findall(r'\[(\d+)\]', q['key'])
                if m:
                    q['marks'] = int(m[-1])
                    q['minutes'] = _mins(q['marks'])
            return q
        tpl.fn = fn


def build(t, P):
    start = len(t.templates)
    add_terms(t, P.get('terms', []))
    add_dates(t, P.get('dates', []))
    add_mcqs(t, P.get('mcq', []))
    add_describe(t, P)
    add_explain(t, P)
    add_claims(t, P.get('claims', []))
    add_essays(t, P)
    add_paper1(t, P)
    add_sources(t, P)
    _markify(t, start)
    t.pack = P
    return t


def S(prov, text, about, infer, purpose, plus, minus, missing, stance=None, why=None, kind='primary', visual=False, context=None, published=True):
    visual = visual or '(description' in prov or '(summary' in prov or 'summary of' in prov
    d = dict(prov=prov, text=text, about=about, infer=infer, purpose=purpose, plus=plus, minus=minus, missing=missing,
             stance=stance, kind=kind, visual=visual, published=published)
    if why:
        d['why'] = why
    if context:
        d['context'] = context
    return d


# ============================================================== CHAPTER 2: Background, the First World War and the world in 1918

c2a = T('Empires and alliances before 1914 and the outbreak of war', 'alliances before 1914', 'outbreak of war')
build(c2a, {
    'enq': 'the causes of the First World War', 'claim': 'the alliance system was the main cause of the First World War',
    'stim': ['By 1914 the Great Powers of Europe were divided into two armed alliances.',
             'On 28 June 1914 Archduke Franz Ferdinand, heir to the throne of Austria-Hungary, was shot dead in Sarajevo.',
             'Within six weeks of the assassination at Sarajevo, most of the Great Powers of Europe were at war.'],
    'terms': [
        ('Triple Alliance', 'the alliance of Germany, Austria-Hungary and Italy formed in 1882'),
        ('Triple Entente', 'the understanding between Britain, France and Russia, complete by 1907'),
        ('militarism', 'the belief that a country should build up strong armed forces and be ready to use them'),
        ('imperialism', 'the policy of building up an empire by gaining colonies and control over other lands'),
        ('nationalism', 'a strong feeling of loyalty to one\'s nation, sometimes including the wish for a people to have its own state'),
        ('Schlieffen Plan', 'Germany\'s plan to avoid a long two-front war by defeating France quickly through Belgium before turning on Russia'),
        ('mobilisation', 'getting a country\'s armed forces ready for war by calling up soldiers and moving them into position'),
    ],
    'dates': [('the Triple Alliance was formed', 1882), ('Britain and France signed the Entente Cordiale', 1904),
              ('Britain launched HMS Dreadnought', 1906), ('Britain and Russia signed an entente', 1907),
              ('Austria-Hungary annexed Bosnia-Herzegovina', 1908), ('the Agadir crisis took place in Morocco', 1911),
              ('Archduke Franz Ferdinand was assassinated in Sarajevo', 1914)],
    'mcq': [
        ('Who was assassinated in Sarajevo on 28 June 1914?', 'Archduke Franz Ferdinand', ['Kaiser Wilhelm II', 'Tsar Nicholas II', 'Emperor Franz Joseph'],
         'Franz Ferdinand, heir to the Austro-Hungarian throne, was shot by Gavrilo Princip. [1]'),
        ('What was the immediate reason why Britain declared war on Germany on 4 August 1914?', 'Germany invaded Belgium, whose neutrality Britain had guaranteed in 1839',
         ['Germany attacked the British fleet at Scapa Flow', 'Germany declared war on Britain first', 'Britain was a member of the Triple Alliance'],
         'The Treaty of London (1839) guaranteed Belgian neutrality; the Schlieffen Plan sent German troops through Belgium. [1]'),
        ('What was the “blank cheque” of July 1914?', 'Germany\'s promise to support Austria-Hungary in any action against Serbia',
         ['A loan from Britain to France for rearmament', 'Russia\'s promise to defend Serbia', 'An American offer to pay for peace talks'],
         'Given on 5-6 July 1914, it encouraged Austria-Hungary to take a hard line against Serbia. [1]'),
        ('Which member of the Triple Alliance stayed out of the war in 1914 and joined the Allies in 1915?', 'Italy', ['Bulgaria', 'Austria-Hungary', 'The Ottoman Empire'],
         'Italy claimed the alliance was defensive and joined the Allies after the Treaty of London (1915). [1]'),
    ],
    'a': [
        ('Describe the alliance system in Europe by 1914.', 'features of the alliance system in Europe by 1914',
         ['The Triple Alliance (1882) linked Germany, Austria-Hungary and Italy', 'The Triple Entente linked Britain, France and Russia by 1907',
          'France and Russia had a military alliance from 1894', 'Alliances meant a dispute between two powers could draw in the others', 'Britain\'s ententes were understandings rather than binding military alliances']),
        ('What happened in Sarajevo on 28 June 1914?', 'facts about the assassination in Sarajevo on 28 June 1914',
         ['Archduke Franz Ferdinand and his wife Sophie visited Sarajevo, the capital of Bosnia', 'A bomb thrown at their car earlier that day failed to kill them',
          'Gavrilo Princip, a Bosnian Serb linked to the Black Hand group, shot them both', 'Austria-Hungary blamed Serbia and sent it an ultimatum on 23 July']),
        ('Describe the naval race between Britain and Germany before 1914.', 'features of the Anglo-German naval race',
         ['Germany\'s Navy Laws from 1898 began a large expansion of its fleet', 'Britain launched HMS Dreadnought in 1906, a faster, more heavily armed battleship',
          'Germany began building its own dreadnoughts, so both raced to build more', 'British public pressure led to the slogan “We want eight and we won\'t wait” in 1909', 'Britain kept the lead, with more dreadnoughts than Germany by 1914']),
    ],
    'b': [
        ('Why did the assassination of Franz Ferdinand lead to a general European war?',
         ['Austria-Hungary blamed Serbia, sent a harsh ultimatum and declared war on 28 July 1914', 'Russia, as protector of the Slavs, mobilised to support Serbia',
          'Germany had promised to back Austria-Hungary (the “blank cheque”) and declared war on Russia on 1 August and France on 3 August',
          'The Schlieffen Plan sent German troops through neutral Belgium, which brought Britain into the war on 4 August']),
        ('Why were relations between Britain and Germany tense before 1914?',
         ['The naval race threatened Britain\'s naval supremacy, on which its empire and trade depended', 'Kaiser Wilhelm II\'s “world policy” (Weltpolitik) sought colonies and influence that challenged Britain',
          'German actions in the Moroccan crises of 1905 and 1911 pushed Britain closer to France', 'Economic rivalry grew as German industry overtook Britain\'s in steel production']),
        ('Why was the Balkans an area of tension before 1914?',
         ['The decline of the Ottoman Empire left a power vacuum that Austria-Hungary and Russia both wanted to fill', 'Serbian nationalism aimed to unite South Slavs, including those ruled by Austria-Hungary',
          'Austria-Hungary\'s annexation of Bosnia in 1908 angered Serbia and Russia', 'The Balkan Wars of 1912-13 doubled Serbia\'s size and alarmed Austria-Hungary']),
    ],
    'claims': [
        ('Britain went to war in 1914 because it was a member of the Triple Alliance.', False, 'Britain was part of the Triple Entente; the immediate reason was Germany\'s invasion of neutral Belgium.'),
        ('Italy fought alongside Germany throughout the First World War.', False, 'Italy stayed neutral in 1914 and joined the Allies in 1915.'),
        ('The Schlieffen Plan was designed to avoid fighting a long war on two fronts.', True, 'It aimed to knock France out in about six weeks before Russia had fully mobilised.'),
    ],
    'c': [
        dict(q='‘The alliance system was the main cause of the First World War.’',
             pro=['Alliances turned a quarrel between Austria-Hungary and Serbia into a war between the Great Powers within a week', 'The blank cheque and the Franco-Russian alliance meant each power felt obliged to act'],
             con=['Italy ignored the Triple Alliance and Britain\'s entente was not binding, so alliances did not force everyone to fight', 'The naval race and militarism created fear and rigid war plans such as the Schlieffen Plan',
                  'Balkan nationalism and the assassination provided the spark', 'Imperial rivalry in Morocco and elsewhere had already raised tension'],
             judge='Alliances explain why the war spread, but militarism, rigid war plans and Balkan nationalism explain why a crisis became war; the alliances were important but not sufficient on their own',
             hints=['the alliances', 'the naval race', 'the Schlieffen Plan', 'events in the Balkans']),
        dict(q='How far was Germany responsible for the outbreak of war in 1914?',
             pro=['The blank cheque encouraged Austria-Hungary to attack Serbia', 'Germany declared war on Russia and France and invaded Belgium, which brought Britain in', 'Weltpolitik and the naval race raised international tension'],
             con=['Austria-Hungary chose to issue the ultimatum and declare war on Serbia', 'Russia\'s general mobilisation made war more likely', 'Serbian nationalists carried out the assassination; all the powers had arms races and war plans'],
             judge='Germany carried a large share of responsibility through the blank cheque and the Schlieffen Plan, but responsibility was shared, especially with Austria-Hungary and Russia'),
    ],
    'src': [
        S('a British cartoon published in Punch magazine in October 1912', 'The cartoon shows the leaders of the Great Powers sitting on the lid of a large pot labelled “Balkan Troubles”, which is boiling over, as they try to keep the lid down.',
          'the situation in the Balkans before 1914', 'The cartoonist suggests the Balkans was a dangerous problem that the Great Powers were struggling to contain, and that it could “boil over” into a wider war.',
          'To warn British readers that tension in the Balkans (during the First Balkan War) threatened the peace of Europe.',
          'it was published at the time, during the Balkan Wars, and reflects how informed opinion in Britain saw the danger', 'it is one magazine\'s view; it simplifies a complex situation and was produced to comment, not to explain the causes in detail',
          'The role of the alliance system, the naval race or the Schlieffen Plan in turning a Balkan crisis into a general war.', stance=False,
          why='it suggests the danger came from Balkan nationalism and rivalries rather than from the alliances themselves', visual=True,
          context='The First Balkan War began in October 1912, when the Balkan League attacked the Ottoman Empire.'),
        S('an extract from a history book written in 2014 (illustrative extract by an unnamed historian)', 'No government in 1914 deliberately planned a general European war. But the alliances, and the railway timetables of mobilisation tied to them, meant that a local quarrel in the Balkans became a continental war within six weeks.',
          'how the war spread in 1914', 'The historian argues that the alliances and mobilisation plans turned a local crisis into a general war.',
          'To give a researched interpretation of why war broke out, written for the centenary of 1914.',
          'it is written with hindsight by someone who can use evidence from all the countries involved', 'it is one interpretation and the extract is short; other historians place more blame on Germany',
          'The role of German policy such as the blank cheque, or the naval race.', stance=True, why='it argues the alliances and the mobilisation plans linked to them caused the local war to spread', kind='secondary', published=True,
          context='The 2014 centenary produced many new books debating responsibility for the war.'),
    ],
})

c2b = T('The end of the war: armistice, collapse of empires and new states', 'armistice', 'collapse of empires', 'new states')
build(c2b, {
    'enq': 'why Germany ended the war in November 1918', 'claim': 'Germany was forced to end the war mainly by problems at home',
    'stim': ['On 11 November 1918 an armistice ended the fighting on the Western Front.', 'By the end of 1918 the German, Austro-Hungarian and Russian empires had collapsed, and the Ottoman Empire had been defeated.',
             'In autumn 1918 Germany\'s allies collapsed one after another.'],
    'terms': [
        ('armistice', 'an agreement to stop fighting while peace terms are worked out'),
        ('abdication', 'when a monarch gives up the throne'),
        ('self-determination', 'the right of a people to decide how and by whom they are governed'),
        ('successor states', 'the new countries formed from the lands of the collapsed empires, such as Czechoslovakia and Yugoslavia'),
        ('blockade', 'cutting off a country\'s supplies by preventing ships from reaching its ports'),
        ('republic', 'a state with an elected or appointed head of state rather than a monarch'),
    ],
    'dates': [('the USA declared war on Germany', 1917, 4), ('Tsar Nicholas II abdicated', 1917, 3), ('the Bolsheviks seized power in Russia', 1917, 11),
              ('Russia signed the Treaty of Brest-Litovsk with Germany', 1918, 3), ('the Allies launched the Hundred Days Offensive at Amiens', 1918, 8),
              ('the armistice on the Western Front came into effect', 1918, 11)],
    'mcq': [
        ('Where was the armistice of November 1918 signed?', 'In a railway carriage in the forest of Compiègne, France', ['In the Hall of Mirrors at Versailles', 'At Brest-Litovsk', 'In the Reichstag building in Berlin'],
         'Signed in Marshal Foch\'s railway carriage at Compiègne in the early hours of 11 November 1918. [1]'),
        ('Who became leader of Germany\'s new republican government in November 1918?', 'Friedrich Ebert', ['Gustav Stresemann', 'Paul von Hindenburg', 'Wolfgang Kapp'],
         'Ebert, leader of the SPD, took over when the Kaiser abdicated on 9 November 1918. [1]'),
        ('Which of these new states was created from lands of the Austro-Hungarian Empire?', 'Czechoslovakia', ['Belgium', 'Denmark', 'Portugal'],
         'Czechoslovakia declared independence on 28 October 1918. [1]'),
        ('Which event in early November 1918 began the revolution in Germany?', 'A mutiny of sailors at Kiel', ['The Spartacist Rising', 'The Kapp Putsch', 'The Munich Putsch'],
         'The Kiel mutiny spread to other cities; the Spartacist Rising was in January 1919. [1]'),
    ],
    'a': [
        ('Describe the situation in Germany in November 1918.', 'features of the situation in Germany in November 1918',
         ['Sailors mutinied at Kiel and revolution spread, with workers\' and soldiers\' councils set up in many cities', 'The British naval blockade had caused severe food shortages',
          'Kaiser Wilhelm II abdicated on 9 November and fled to the Netherlands', 'A republic was proclaimed and Friedrich Ebert led a new government', 'The new government agreed to the armistice on 11 November']),
        ('What were the terms of the armistice of 11 November 1918?', 'terms of the armistice of November 1918',
         ['German forces had to leave occupied France, Belgium and Alsace-Lorraine', 'Allied troops would occupy the left bank of the Rhine',
          'Germany handed over large quantities of weapons, including artillery, machine guns and aircraft', 'Germany surrendered its submarines and its surface fleet was interned', 'The Treaty of Brest-Litovsk was cancelled and the Allied blockade continued']),
        ('Describe how the great empires of Europe were affected by the end of the war.', 'empires that collapsed or were broken up as a result of the war',
         ['The Russian Empire collapsed in 1917 when the Tsar abdicated and the Bolsheviks took power', 'The German Empire ended when the Kaiser abdicated in November 1918',
          'Austria-Hungary broke apart in October-November 1918 into Austria, Hungary, Czechoslovakia and other states', 'The Ottoman Empire was defeated and signed the armistice of Mudros in October 1918']),
    ],
    'b': [
        ('Why did Germany ask for an armistice in 1918?',
         ['The Ludendorff (Spring) Offensive failed and exhausted the German army', 'The Allied Hundred Days Offensive from August 1918 pushed the Germans back',
          'Fresh American troops were arriving in large numbers', 'The British blockade caused hunger and unrest at home, ending in mutiny and revolution', 'Germany\'s allies Bulgaria, the Ottoman Empire and Austria-Hungary all made peace in autumn 1918']),
        ('Why were several new states created in Europe in 1918-19?',
         ['The Austro-Hungarian, Russian and Ottoman empires collapsed, leaving their peoples without a government', 'Nationalist movements among Poles, Czechs, Slovaks and South Slavs declared independence',
          'Wilson\'s principle of self-determination encouraged the Allies to recognise national states', 'The Allies wanted a belt of states in eastern Europe to contain Germany and Bolshevik Russia']),
        ('Why did many Germans find it hard to accept defeat in November 1918?',
         ['No fighting had taken place on German soil and German troops were still in France and Belgium when the war ended', 'Propaganda had told Germans they were winning, especially after Brest-Litovsk in March 1918',
          'The armistice was signed by civilian politicians, not the army leaders', 'This led to the “stab-in-the-back” myth that Germany had been betrayed at home']),
    ],
    'claims': [
        ('Germany surrendered in 1918 because Allied armies had invaded and occupied most of Germany.', False, 'There was no fighting on German soil; German troops were still in France and Belgium, which helped the “stab-in-the-back” myth to grow.'),
        ('The Kaiser abdicated two days before the armistice came into effect.', True, 'He abdicated on 9 November 1918; the armistice took effect at 11 a.m. on 11 November.'),
        ('Russia fought alongside the Allies until the end of the war in November 1918.', False, 'The Bolshevik government made peace with Germany at Brest-Litovsk in March 1918.'),
    ],
    'c': [
        dict(q='‘The arrival of American troops was the main reason why Germany asked for an armistice in 1918.’',
             pro=['By mid-1918 around 10,000 US troops were arriving in France each day, giving the Allies a growing advantage', 'The prospect of millions more Americans made German victory impossible'],
             con=['The failure of the Ludendorff Offensive cost Germany its best troops', 'The Allied offensive from Amiens in August 1918 was led mainly by British Empire and French forces', 'The blockade caused hunger, strikes and mutiny', 'The collapse of Germany\'s allies left it isolated'],
             judge='US troops mattered mostly by removing hope of victory; military defeat after the failed spring offensive and collapse at home were more immediate causes'),
        dict(q='How important was the collapse of empires in shaping the problems facing the peacemakers in 1919?',
             pro=['Whole regions of central and eastern Europe needed new borders and governments', 'Mixed populations meant self-determination could not satisfy everyone, leaving minorities in new states', 'Bolshevik Russia was absent and feared'],
             con=['The victors\' own aims (security, revenge, reparations) also caused problems', 'Public opinion in Britain and France demanded harsh terms for Germany', 'Wilson\'s ideals clashed with the secret wartime treaties'],
             judge='The collapse of empires created the hardest territorial problems, but the clash between the Big Three\'s aims was the key problem for the German settlement'),
    ],
    'src': [
        S('an extract from the diary of a Berlin housewife, November 1918 (illustrative, based on typical accounts)', 'There is no butter, no meat and hardly any potatoes. Sailors from Kiel have come with red flags and the Kaiser has gone. People say the war is lost, yet our soldiers are still standing in France.',
          'conditions in Germany at the end of the war', 'It suggests Germany was hungry, in revolution and that people were confused because the army had not been beaten on German soil.',
          'To record daily life privately during the revolution, so it was not written to persuade others.',
          'it is written at the time by an ordinary civilian who experienced the shortages', 'it is one person\'s view of one city; she could not know the military situation at the front',
          'The military situation: the failure of the spring offensive and the Allied advance from August 1918.', stance=True, why='it stresses hunger and revolution at home', published=False,
          context='The British blockade and the Kiel mutiny (early November 1918) caused unrest across Germany.'),
        S('a British newspaper report, 12 November 1918 (illustrative)', 'The German armies, beaten in the field since August and driven back across Belgium, have been compelled to accept terms which leave them unable to fight again.',
          'why Germany accepted the armistice', 'It claims Germany was defeated militarily and had no choice but to accept the armistice.',
          'To celebrate the Allied victory and reassure British readers that the war had been won on the battlefield.',
          'it was written immediately after the armistice and its account of the Allied advance matches the events of the Hundred Days', 'it is a victorious country\'s newspaper and ignores the hunger and revolution inside Germany',
          'The effect of the blockade, the Kiel mutiny and the Kaiser\'s abdication.', stance=False, why='it argues Germany was beaten militarily rather than at home',
          context='The armistice had been signed the day before, on 11 November 1918.'),
    ],
})

c2c = T("Wilson's Fourteen Points and the idea of self-determination", 'fourteen points', 'self-determination')
build(c2c, {
    'enq': 'Wilson\'s plans for the peace', 'claim': 'Wilson\'s Fourteen Points offered a fair basis for peace',
    'stim': ['In January 1918 President Woodrow Wilson set out the USA\'s war aims in the Fourteen Points.', 'Wilson hoped the peace would be based on justice and self-determination rather than revenge.'],
    'terms': [
        ('Fourteen Points', 'President Wilson\'s programme for a just peace, set out to the US Congress on 8 January 1918'),
        ('self-determination', 'the idea that national groups should be able to rule themselves'),
        ('collective security', 'the idea that nations act together to protect any member that is attacked'),
        ('open diplomacy', 'agreements between countries made in public rather than through secret treaties'),
        ('freedom of the seas', 'the right of all ships to sail in international waters in peace and war'),
        ('disarmament', 'reducing the number of weapons and the size of armed forces'),
    ],
    'dates': [('the USA entered the First World War', 1917), ('Wilson presented the Fourteen Points to Congress', 1918),
              ('the Paris Peace Conference opened', 1919), ('the US Senate finally rejected the Treaty of Versailles', 1920)],
    'mcq': [
        ('Which of the Fourteen Points did Britain object to most strongly?', 'Freedom of the seas', ['Restoration of Belgium', 'An independent Poland', 'A League of Nations'],
         'Britain relied on naval power and blockade, so it rejected Point 2. [1]'),
        ('Which of these was NOT one of the Fourteen Points?', 'Germany should accept the blame for starting the war', ['An independent Poland with access to the sea', 'A general association of nations', 'Reduction of armaments'],
         'War guilt (Article 231) came from the Treaty of Versailles, not the Fourteen Points. [1]'),
        ('What did Point 14 of the Fourteen Points propose?', 'A general association of nations', ['The return of Alsace-Lorraine to France', 'Freedom of the seas', 'An end to secret treaties'],
         'Point 14 led to the League of Nations. [1]'),
        ('Which Point called for an independent Polish state with access to the sea?', 'Point 13', ['Point 1', 'Point 8', 'Point 14'], 'Point 13; this led to the Polish Corridor. [1]'),
    ],
    'a': [
        ('Describe the main ideas of Wilson\'s Fourteen Points.', 'ideas contained in the Fourteen Points',
         ['No more secret treaties (open diplomacy)', 'Freedom of the seas for all nations', 'Free trade and the removal of economic barriers', 'Reduction of armaments by all countries',
          'Self-determination for the peoples of eastern Europe, including an independent Poland', 'A general association of nations to keep the peace']),
        ('What did Wilson mean by self-determination?', 'features of Wilson\'s idea of self-determination',
         ['National groups should be able to choose their own government', 'Borders should follow lines of nationality where possible', 'Peoples of Austria-Hungary should have the chance of autonomous development', 'Plebiscites (votes) could decide disputed areas']),
        ('Describe the Fourteen Points that dealt with territory in Europe.', 'territorial changes proposed in the Fourteen Points',
         ['Belgium to be evacuated and restored', 'Alsace-Lorraine to be returned to France', 'Italy\'s frontiers to follow clear lines of nationality', 'An independent Poland with secure access to the sea', 'Serbia to be given access to the sea']),
    ],
    'b': [
        ('Why did Wilson put forward the Fourteen Points?',
         ['He believed the war had been caused by secret alliances and arms races, so wanted open diplomacy and disarmament', 'He wanted a just peace so that Germany would not seek revenge',
          'He wanted to spread democracy and self-determination', 'He hoped a League of Nations would prevent future wars', 'As an American he favoured free trade and freedom of the seas']),
        ('Why did Clemenceau and Lloyd George have doubts about the Fourteen Points?',
         ['France had suffered huge losses and Clemenceau wanted security and compensation, not a lenient peace', 'Lloyd George could not accept freedom of the seas because Britain depended on its navy',
          'Self-determination threatened the British and French empires', 'Both leaders faced voters who wanted Germany punished']),
        ('Why was self-determination difficult to apply in eastern Europe?',
         ['Different national groups were mixed together, so any border left minorities', 'New states needed defensible borders and resources, which sometimes meant including other peoples',
          'The Allies would not apply it to Germans, for example in Austria and the Sudetenland', 'Wartime promises to Italy and others conflicted with it']),
    ],
    'claims': [
        ('The Fourteen Points said that Germany should lose all its overseas colonies and pay reparations.', False, 'The Fourteen Points called for an impartial adjustment of colonial claims and did not mention reparations in that form; those came from the Treaty of Versailles.'),
        ('Wilson\'s Fourteen Points included a proposal for a League of Nations.', True, 'Point 14 called for a general association of nations.'),
        ('In 1919 self-determination was applied to German-speaking people as well as to other nationalities.', False, 'Union of Germany and Austria was forbidden and about three million Germans were placed in Czechoslovakia.'),
    ],
    'c': [
        dict(q='‘Wilson\'s Fourteen Points were too idealistic to be put into practice.’',
             pro=['Self-determination could not be applied fairly where peoples were mixed', 'Britain rejected freedom of the seas and France wanted security, not a lenient peace', 'Wilson could not even persuade the US Senate to accept the treaty and League'],
             con=['Several points were achieved: an independent Poland, the return of Alsace-Lorraine, restored Belgium and new national states', 'The League of Nations was created in 1920', 'Some points were practical war aims shared by the Allies'],
             judge='Parts of the Fourteen Points were achieved, especially in territorial changes, but the hopes of disarmament, free trade and a lasting peace based on justice proved unrealistic'),
        dict(q='How far was the principle of self-determination applied in the peace settlement of 1919-20?',
             pro=['Poland, Czechoslovakia, Yugoslavia and the Baltic states were created or recognised', 'Plebiscites were held in areas such as Schleswig and Upper Silesia'],
             con=['Germans were denied union with Austria and placed in Czechoslovakia and Poland', 'New states contained large minorities', 'Former German and Ottoman colonies became mandates of Britain and France rather than independent'],
             judge='Self-determination was applied widely in eastern Europe but selectively, and not to Germans or colonial peoples'),
    ],
    'src': [
        S('Point 14 of President Wilson\'s Fourteen Points, from his address to the US Congress, 8 January 1918', 'A general association of nations must be formed under specific covenants for the purpose of affording mutual guarantees of political independence and territorial integrity to great and small states alike.',
          'Wilson\'s plans for keeping peace', 'Wilson wanted an organisation of nations that would protect the independence and borders of every state, large or small.',
          'To set out American war aims publicly and offer a just basis for peace that might also encourage Germany to make peace.',
          'it is Wilson\'s own public statement of his aims', 'it states an ideal, not how it would work; Wilson did not control what other countries would accept',
          'How the British and French leaders reacted, or whether the US Congress would support such a League.', stance=True, why='it promises equal protection for all states, which suggests a fair peace',
          context='The USA had entered the war in April 1917 and Russia had just left it after the Bolshevik revolution.'),
        S('Point 10 of President Wilson\'s Fourteen Points, January 1918', 'The peoples of Austria-Hungary, whose place among the nations we wish to see safeguarded and assured, should be accorded the freest opportunity to autonomous development.',
          'Wilson\'s idea of self-determination', 'Wilson wanted the nationalities of Austria-Hungary to be allowed to govern themselves.',
          'To support the national groups of Austria-Hungary and weaken the enemy alliance.',
          'it is Wilson\'s own wording, so it shows exactly what he proposed', 'it does not say how mixed populations would be divided',
          'That Austria-Hungary would collapse completely by November 1918 and new states would be created.', stance=True, why='it offers peoples the chance to rule themselves'),
        S('an editorial in a French newspaper, early 1919 (illustrative)', 'Mr Wilson speaks of justice, but he has not seen the ruined towns of our northern departments. France needs guarantees, not fine words, and Germany must pay for what it has destroyed.',
          'French attitudes to Wilson\'s ideas', 'French opinion felt Wilson\'s ideas were too soft on Germany and that France needed security and compensation.',
          'To pressure the French delegation at the peace conference to demand security and reparations.',
          'it reflects widespread French feeling at the time of the conference', 'it is written to persuade and represents one country\'s point of view',
          'That Clemenceau also had to compromise with Wilson and Lloyd George.', stance=False, why='it argues Wilson\'s ideas ignored France\'s suffering, so would not be fair to France'),
    ],
})

CHAPTERS[2] = [c2a, c2b, c2c]


# ============================================================== CHAPTER 3: Were the peace treaties of 1919-23 fair?

c3a = T('Motives and aims of the Big Three at Versailles', 'big three', 'aims of the big three')
build(c3a, {
    'enq': 'the aims of the peacemakers in 1919', 'claim': 'the Big Three had very different aims for the peace with Germany',
    'stim': ['In January 1919 the leaders of the victorious powers met in Paris to draw up the peace settlement.', 'The peace conference was dominated by the “Big Three”: Clemenceau, Lloyd George and Wilson.',
             'Germany was not invited to take part in the negotiations at the Paris Peace Conference.'],
    'terms': [
        ('Big Three', 'the leaders who dominated the Paris Peace Conference: Clemenceau (France), Lloyd George (Britain) and Wilson (USA)'),
        ('reparations', 'compensation for war damage paid by a defeated country to the victors'),
        ('diktat', 'a dictated peace: the German name for a treaty imposed without negotiation'),
        ('buffer zone', 'an area between two rival states intended to make attack more difficult'),
        ('Fontainebleau Memorandum', 'Lloyd George\'s paper of March 1919 warning that a harsh peace would make Germany seek revenge'),
        ('Council of Four', 'the meetings of Wilson, Lloyd George, Clemenceau and Orlando where the main decisions were made'),
    ],
    'dates': [('Lloyd George won the “khaki election” in Britain', 1918, 12), ('the Paris Peace Conference opened', 1919, 1),
              ('Lloyd George wrote the Fontainebleau Memorandum', 1919, 3), ('the Italian delegation walked out of the conference over Fiume', 1919, 4),
              ('Germany signed the Treaty of Versailles in the Hall of Mirrors', 1919, 6)],
    'mcq': [
        ('Which leader at the peace conference was known as “the Tiger”?', 'Georges Clemenceau', ['David Lloyd George', 'Woodrow Wilson', 'Vittorio Orlando'], 'Clemenceau, Prime Minister of France. [1]'),
        ('Which of these was Clemenceau\'s main aim at the peace conference?', 'To make France secure by weakening Germany permanently', ['To create a League of Nations open to Germany', 'To protect freedom of the seas', 'To restore Germany as a trading partner'],
         'France had been invaded in 1870 and 1914; security was Clemenceau\'s priority. [1]'),
        ('Why did Lloyd George want Germany to recover after the war?', 'Germany had been one of Britain\'s biggest trading partners', ['Britain wanted to join the German army', 'Britain owed Germany large debts', 'Germany had promised Britain its colonies'],
         'A prosperous Germany would buy British goods and be less likely to turn communist. [1]'),
        ('Which leader left the peace conference for a time in April 1919 because his country did not get the port of Fiume?', 'Vittorio Orlando', ['Georges Clemenceau', 'Woodrow Wilson', 'David Lloyd George'], 'Orlando, Prime Minister of Italy. [1]'),
    ],
    'a': [
        ('What were Clemenceau\'s aims at the Paris Peace Conference?', 'aims of Clemenceau at the peace conference',
         ['He wanted France to be secure from future German attack', 'He wanted Germany\'s army and industry weakened', 'He wanted the Rhineland separated from Germany or controlled as a buffer', 'He wanted Alsace-Lorraine returned to France', 'He wanted large reparations to rebuild the devastated north-east of France']),
        ('What were Lloyd George\'s aims at the Paris Peace Conference?', 'aims of Lloyd George at the peace conference',
         ['He had promised British voters in December 1918 that Germany would pay', 'He wanted to end the threat of the German navy to Britain', 'He wanted to protect and extend the British Empire, for example by taking German colonies',
          'He wanted Germany to recover so it could trade with Britain', 'He feared a harsh peace would cause German revenge or a communist revolution']),
        ('What were Wilson\'s aims at the Paris Peace Conference?', 'aims of Wilson at the peace conference',
         ['He wanted a peace based on the Fourteen Points', 'He wanted self-determination for the peoples of eastern Europe', 'He wanted a League of Nations to keep the peace', 'He wanted Germany punished but not so harshly that it would seek revenge', 'He wanted disarmament, free trade and freedom of the seas']),
    ],
    'b': [
        ('Why did Clemenceau want a harsh treaty?',
         ['France had lost about 1.4 million soldiers, more than Britain or the USA', 'The north-east of France, including mines and factories, had been devastated', 'France had been invaded by Germany in 1870 and 1914 and wanted security', 'French public opinion demanded revenge and compensation']),
        ('Why did Lloyd George find it difficult to achieve his aims?',
         ['He had promised British voters he would “make Germany pay”, so he could not seem soft', 'He privately wanted a moderate peace so Germany could trade and not seek revenge', 'Clemenceau demanded far harsher terms', 'Wilson\'s ideas such as freedom of the seas conflicted with British interests']),
        ('Why did Wilson want a fair treaty with Germany?',
         ['The USA had suffered far less than France and did not want revenge', 'He believed a harsh treaty would make Germany seek revenge and cause another war', 'He wanted the peace to be based on justice and the Fourteen Points', 'He wanted a strong, democratic Germany as part of a League of Nations']),
    ],
    'claims': [
        ('Germany\'s representatives were invited to negotiate the terms of the Treaty of Versailles.', False, 'Germany was excluded from the negotiations and given the terms in May 1919 to accept or reject.'),
        ('Lloyd George faced pressure from British voters to treat Germany harshly.', True, 'He won the December 1918 election in a mood of “make Germany pay”.'),
        ('Wilson wanted Germany to be split up into small states.', False, 'Wilson wanted a just peace, self-determination and a League, not the destruction of Germany.'),
    ],
    'c': [
        dict(q='‘Clemenceau\'s aims were the most reasonable of the Big Three.’',
             pro=['France had suffered the greatest losses and devastation among the Big Three', 'France bordered Germany and had been invaded twice in fifty years, so security was a real need'],
             con=['Wilson\'s aims looked further ahead to a lasting peace', 'Lloyd George understood that a crippled Germany would harm European trade and stability', 'A very harsh peace risked German revenge'],
             judge='Clemenceau\'s aims were understandable given France\'s losses and position, but Lloyd George\'s and Wilson\'s concern for lasting stability made their aims more realistic in the long term'),
        dict(q='How far did the Big Three agree about how Germany should be treated?',
             pro=['All agreed Germany should be punished in some way, disarmed and lose some territory', 'All agreed Alsace-Lorraine should go back to France and that Belgium should be restored'],
             con=['Clemenceau wanted Germany crippled; Wilson wanted a just peace', 'Lloyd George wanted Germany to recover as a trading partner', 'They clashed over the Rhineland, the Saar, reparations and freedom of the seas'],
             judge='They agreed on the general principle of punishment but disagreed sharply about its extent, which is why the treaty was a compromise'),
    ],
    'src': [
        S('Lloyd George\'s Fontainebleau Memorandum, a paper written for the other peacemakers in March 1919 (abridged)', 'You may strip Germany of her colonies, reduce her armaments to a mere police force and her navy to that of a fifth-rate power; all the same in the end if she feels that she has been unjustly treated in the peace of 1919 she will find means of exacting retribution from her conquerors.',
          'Lloyd George\'s view of the peace', 'Lloyd George warns that a treaty Germany sees as unjust will lead to German revenge, however weak Germany is made.',
          'To persuade Clemenceau and Wilson to moderate the terms, especially on territory and reparations.',
          'it is a private paper by Lloyd George himself, so it shows his real view rather than his election promises', 'it was written to influence the other leaders, so he may have exaggerated the danger',
          'That Lloyd George had publicly promised British voters to make Germany pay.', stance=True, why='it shows Lloyd George wanted a more moderate peace than Clemenceau', published=False,
          context='By March 1919 the Big Three were deadlocked over the Rhineland and reparations.'),
        S('a description of Clemenceau by J. M. Keynes, a British Treasury adviser at the peace conference, in his book The Economic Consequences of the Peace (1919)', 'He had one illusion — France; and one disillusion — mankind.',
          'Clemenceau\'s aims', 'Keynes suggests Clemenceau cared only about France\'s interests and had no faith in ideals such as the League.',
          'Keynes resigned in protest at the treaty and wrote the book to attack it as too harsh.',
          'Keynes saw Clemenceau at work in Paris', 'Keynes opposed the treaty and was critical of Clemenceau, so his description is one-sided',
          'That Clemenceau had to compromise on the Rhineland and the Saar.', stance=True, why='it shows Clemenceau\'s narrow focus on France differed from Wilson\'s ideals', kind='primary'),
        S('a speech by a French deputy in the French parliament, 1919 (illustrative)', 'Our allies across the sea have lost little and gained much. It is France, whose soil was the battlefield, that must be guaranteed against a nation of sixty million that will one day want revenge.',
          'French attitudes to the peace', 'It shows French fears of a larger German population and a belief that Britain and the USA did not share France\'s suffering.',
          'To persuade the French parliament that France needed stronger guarantees than the treaty gave.',
          'it reflects views widely held in France in 1919', 'it is a political speech designed to win support, so it exaggerates',
          'That Britain and the USA offered France a treaty of guarantee, which collapsed when the US Senate rejected Versailles.', stance=True, why='it shows French aims of security differed from those of Britain and the USA'),
    ],
})

c3b = T('Why the victors did not get everything they wanted', 'victors did not get everything', 'compromise')
build(c3b, {
    'enq': 'how far the peacemakers achieved their aims', 'claim': 'the Treaty of Versailles was a compromise that satisfied none of the Big Three',
    'stim': ['The Treaty of Versailles was a compromise between the very different aims of the Big Three.', 'None of the peacemakers went home from Paris with everything they wanted.'],
    'terms': [
        ('compromise', 'an agreement in which each side gives up part of what it wanted'),
        ('mandate', 'a former colony of a defeated power governed by a victor on behalf of the League of Nations'),
        ('demilitarised zone', 'an area where no troops or military fortifications are allowed'),
        ('plebiscite', 'a vote by the people of an area to decide a single question, such as which country to belong to'),
        ('Treaty of London (1915)', 'the secret agreement by which the Allies promised Italy territory if it joined the war'),
        ('isolationism', 'the policy of keeping out of the affairs and disputes of other countries'),
    ],
    'dates': [('the Treaty of Versailles came into force', 1920), ('the US Senate first voted against the Treaty of Versailles', 1919, 11),
              ('the Reparations Commission fixed the total at £6,600 million', 1921), ('the Saar plebiscite returned the region to Germany', 1935), ('Allied troops finally left the Rhineland', 1930)],
    'mcq': [
        ('Clemenceau wanted the Rhineland to be separated from Germany. What did the treaty actually decide?', 'It stayed German but was demilitarised and occupied by Allied troops for 15 years', ['It became part of France', 'It became an independent state', 'It was given to Belgium'],
         'A compromise between French demands and British and American objections. [1]'),
        ('What happened to the Saar coalfields under the Treaty of Versailles?', 'France could take the coal for 15 years while the League governed the Saar', ['They were given to Poland', 'They became permanently French', 'They were shared with Britain'],
         'A plebiscite in 1935 returned the Saar to Germany. [1]'),
        ('Why was Wilson disappointed by the outcome of the peace settlement?', 'The US Senate refused to approve the treaty and the USA did not join the League', ['Germany was allowed a large army', 'Italy gained all the land it wanted', 'France received no reparations'],
         'The Senate voted against the treaty in November 1919 and March 1920. [1]'),
        ('Which of Lloyd George\'s aims was achieved by the Treaty of Versailles?', 'The German navy was reduced to six battleships and no submarines', ['Germany stayed a strong trading partner with all its colonies', 'Freedom of the seas was guaranteed', 'Reparations were kept low'],
         'The naval threat to Britain was removed; the German fleet was scuttled at Scapa Flow in June 1919. [1]'),
    ],
    'a': [
        ('Describe what Clemenceau achieved at the Paris Peace Conference.', 'aims that Clemenceau achieved',
         ['Alsace-Lorraine was returned to France', 'The Rhineland was demilitarised and occupied by Allied troops for 15 years', 'France gained control of the Saar coal for 15 years', 'Germany\'s army was limited to 100,000 men', 'Germany accepted war guilt and had to pay reparations']),
        ('Describe the ways in which Wilson did not get what he wanted.', 'ways in which Wilson was disappointed by the peace settlement',
         ['Self-determination was not applied to Germans in Austria and the Sudetenland', 'Disarmament applied only to the defeated powers', 'Freedom of the seas was rejected by Britain', 'The treaty was harsher than his Fourteen Points', 'The US Senate rejected the treaty and the USA never joined the League']),
        ('Describe what Lloyd George achieved at the Paris Peace Conference.', 'gains Britain made from the peace settlement',
         ['The German navy was reduced to six battleships and no submarines', 'Britain gained German colonies as League mandates, such as Tanganyika', 'Britain received a share of reparations', 'He helped block the separation of the Rhineland from Germany', 'He helped keep Danzig as a Free City rather than giving it to Poland']),
    ],
    'b': [
        ('Why was Clemenceau criticised in France after the treaty was signed?',
         ['Many French people believed the treaty was too soft on Germany', 'France did not gain the Rhine as its frontier or a separate Rhineland state', 'The Saar was only controlled for 15 years', 'The Anglo-American guarantee of French security collapsed when the US Senate rejected the treaty']),
        ('Why did the US Senate refuse to approve the Treaty of Versailles?',
         ['Many senators wanted the USA to return to isolationism', 'They feared Article 10 of the League Covenant would drag the USA into foreign wars', 'Republicans opposed Wilson, a Democrat, and he refused to compromise', 'Some Americans thought the treaty was unfair to Germany']),
        ('Why did Lloyd George believe the treaty was too harsh?',
         ['He thought reparations would damage Germany\'s economy and its trade with Britain', 'He feared Germany would seek revenge, as his Fontainebleau Memorandum warned', 'He was worried about Germans being placed under Polish rule', 'He feared harsh terms could push Germany towards communism']),
    ],
    'claims': [
        ('Clemenceau got everything he wanted from the Treaty of Versailles.', False, 'He did not get the Rhineland separated from Germany or the Saar permanently, and the promised Anglo-American guarantee collapsed.'),
        ('The USA never joined the League of Nations.', True, 'The US Senate rejected the treaty in 1919 and 1920 and the USA stayed out.'),
        ('Lloyd George was entirely satisfied with the Treaty of Versailles.', False, 'He gained the naval terms and colonies but thought parts of the treaty, especially in the east and on reparations, were too harsh.'),
    ],
    'c': [
        dict(q='‘The Treaty of Versailles satisfied none of the Big Three.’',
             pro=['Clemenceau did not get the Rhineland separated and was voted out of office in 1920', 'Wilson saw the US Senate reject the treaty and the League', 'Lloyd George thought the treaty was too harsh and would cause future trouble'],
             con=['Clemenceau gained Alsace-Lorraine, a demilitarised Rhineland and a weakened German army', 'Lloyd George removed the German naval threat and gained colonies', 'Wilson saw the League created and new states based on self-determination'],
             judge='Each leader gained important aims, but none was fully satisfied; the treaty was a compromise that each could defend only in part'),
        dict(q='How far did Wilson achieve his aims at the Paris Peace Conference?',
             pro=['The League of Nations was written into the treaty', 'New states such as Poland and Czechoslovakia reflected self-determination'],
             con=['The treaty was much harsher on Germany than he wanted', 'Disarmament and freedom of the seas were not achieved', 'The US Senate rejected the treaty, so the USA did not join the League'],
             judge='Wilson achieved his central aim of the League and some self-determination, but his failure at home undermined much of what he gained'),
    ],
    'src': [
        S('a cartoon by Leonard Raven-Hill published in the British magazine Punch, 10 December 1919, titled “The Gap in the Bridge”', 'A bridge labelled with the names of the Allied countries forms the “League of Nations”, but the keystone in the middle is missing. Uncle Sam, representing the USA, leans against the missing stone, smoking a pipe. The caption says the bridge was designed by the President of the USA.',
          'the weakness caused by the US refusal to join the League', 'The cartoonist suggests the League cannot work without the USA, and that it is ironic that the country whose President designed it would not join.',
          'To comment on the US Senate\'s vote against the treaty in November 1919 and its consequences for the League.',
          'it was published just after the Senate vote and shows how British opinion saw the League\'s prospects', 'it is a comment, not evidence of how the League actually worked later',
          'Why the Senate rejected the treaty, for example fear of being dragged into wars by Article 10.', stance=True, why='it shows Wilson failed to get US support for his League', visual=True,
          context='The US Senate rejected the Treaty of Versailles on 19 November 1919.'),
        S('an article in a French newspaper, June 1919 (illustrative)', 'The Rhine was the only true guarantee for France, and it has been given away for a promise. Fifteen years of occupation will pass quickly, and then France will stand alone.',
          'French views of the treaty', 'It shows French disappointment that Clemenceau did not secure the Rhine frontier and that occupation was only temporary.',
          'To criticise Clemenceau\'s compromises and warn that France would be insecure in future.',
          'it reflects real French complaints about the Rhineland compromise', 'it is written to criticise the government and ignores what France did gain',
          'That France gained Alsace-Lorraine, the Saar coal and a weakened German army.', stance=True, why='it shows Clemenceau was not satisfied by the Rhineland terms'),
        S('a speech by a British Conservative MP in the House of Commons, July 1919 (illustrative)', 'The German fleet lies at the bottom of Scapa Flow, her colonies are ours to administer and she must pay. This treaty gives Britain all that it fought for.',
          'British reactions to the treaty', 'It suggests many in Britain felt the treaty met British aims on the navy, colonies and reparations.',
          'To defend the treaty in Parliament and praise the government\'s success.',
          'it shows views held by many British supporters of the government', 'it is a political speech that ignores Lloyd George\'s own doubts',
          'That Lloyd George privately feared the treaty was too harsh.', stance=False, why='it suggests the treaty did satisfy British aims'),
    ],
})

BREAD = [('1918', 0.63), ('January 1923', 250), ('July 1923', 3465), ('September 1923', 1512000), ('November 1923', 201000000000)]


def _big(x):
    if x >= 1e9:
        return f'{x / 1e9:g} billion'
    if x >= 1e6:
        return f'{x / 1e6:g} million'
    return f'{x:,}' if isinstance(x, int) else f'{x:g}'


c3c = T('Terms of the Treaty of Versailles and its impact on Germany to 1923', 'terms of the treaty of versailles', 'impact on germany')
build(c3c, {
    'enq': 'German reactions to the Treaty of Versailles', 'claim': 'the Treaty of Versailles was too harsh on Germany',
    'stim': ['The Treaty of Versailles was signed on 28 June 1919 in the Hall of Mirrors.', 'Germany lost about 13 per cent of its European territory under the Treaty of Versailles.',
             'Many Germans called the Treaty of Versailles a “diktat”.'],
    'terms': [
        ('Article 231', 'the “war guilt” clause, by which Germany accepted responsibility for the loss and damage caused by the war'),
        ('Polish Corridor', 'the strip of land given to Poland to give it access to the sea, which separated East Prussia from the rest of Germany'),
        ('Anschluss', 'union between Germany and Austria, forbidden by the treaty'),
        ('Rhineland', 'the German land along the River Rhine, which was demilitarised and occupied by Allied troops'),
        ('hyperinflation', 'extremely rapid rise in prices, as in Germany in 1923, when money became almost worthless'),
        ('passive resistance', 'refusing to cooperate without using violence, as German workers did in the Ruhr in 1923'),
        ('November Criminals', 'the name nationalists gave to the politicians who agreed to the armistice and the treaty'),
    ],
    'dates': [('Germany signed the Treaty of Versailles', 1919, 6), ('the Kapp Putsch took place in Berlin', 1920, 3), ('reparations were fixed at £6,600 million', 1921, 4),
              ('the foreign minister Walther Rathenau was assassinated', 1922, 6), ('French and Belgian troops occupied the Ruhr', 1923, 1), ('Hitler attempted the Munich Putsch', 1923, 11)],
    'mcq': [
        ('What size of army was Germany allowed by the Treaty of Versailles?', '100,000 men', ['10,000 men', '500,000 men', '1 million men'], 'Conscription was also banned. [1]'),
        ('Which territory was returned to France by the Treaty of Versailles?', 'Alsace-Lorraine', ['The Saar', 'Eupen and Malmedy', 'North Schleswig'], 'Taken by Germany in 1871. [1]'),
        ('Which region became a Free City under the League of Nations?', 'Danzig', ['Memel', 'Posen', 'Upper Silesia'], 'Danzig was mainly German but Poland was given use of its port. [1]'),
        ('Which of these was NOT forbidden to Germany by the Treaty of Versailles?', 'A navy of six battleships', ['An air force', 'Submarines', 'Tanks'], 'Germany was allowed six battleships but no submarines, tanks or air force. [1]'),
        ('Why did French and Belgian troops occupy the Ruhr in January 1923?', 'Germany had fallen behind with reparations payments', ['Germany had remilitarised the Rhineland', 'Hitler had attempted a putsch in Munich', 'The League of Nations ordered it'],
         'They aimed to take coal and goods instead. [1]'),
    ],
    'a': [
        ('What were the military terms of the Treaty of Versailles?', 'military terms of the Treaty of Versailles',
         ['The army was limited to 100,000 men', 'Conscription was banned', 'Germany was not allowed tanks, an air force or submarines', 'The navy was limited to six battleships', 'The Rhineland was demilitarised']),
        ('Describe the territorial terms of the Treaty of Versailles.', 'territorial losses imposed on Germany by the Treaty of Versailles',
         ['Alsace-Lorraine was returned to France', 'West Prussia and Posen went to Poland, creating the Polish Corridor', 'Danzig became a Free City under the League', 'The Saar was run by the League for 15 years', 'Eupen and Malmedy went to Belgium and North Schleswig to Denmark after a plebiscite', 'Germany\'s colonies became League mandates']),
        ('Describe the effects of the occupation of the Ruhr in 1923.', 'effects of the occupation of the Ruhr in 1923',
         ['German workers went on strike in passive resistance', 'French troops took over mines and factories and some workers were killed', 'Industrial production in Germany fell sharply', 'The government printed money to pay striking workers', 'This made inflation spiral into hyperinflation']),
    ],
    'b': [
        ('Why did the Germans hate the Treaty of Versailles?',
         ['It was a diktat: Germany had no part in the negotiations', 'The war guilt clause was seen as humiliating because many Germans believed they had fought a defensive war', 'Reparations were seen as an impossible burden',
          'The loss of land put Germans under foreign rule, for example in the Polish Corridor', 'Military restrictions left Germany unable to defend itself while its neighbours stayed armed']),
        ('Why did Germany experience hyperinflation in 1923?',
         ['The war had been paid for by borrowing and printing money', 'Reparations payments drained Germany\'s reserves', 'The Ruhr occupation cut production while the government kept paying striking workers', 'The government printed vast amounts of money, so it lost its value']),
        ('Why did the Treaty of Versailles weaken the Weimar Republic?',
         ['The politicians who signed it were blamed as “November Criminals”', 'It encouraged the stab-in-the-back myth', 'It led to extremist risings such as the Kapp Putsch in 1920', 'Reparations contributed to the economic crisis of 1923']),
    ],
    'claims': [
        ('The Treaty of Versailles left Germany with no army at all.', False, 'Germany was allowed an army of 100,000 men, but no conscription, tanks or air force.'),
        ('The reparations total of £6,600 million was fixed in 1921, not in the treaty itself.', True, 'The Reparations Commission announced the figure in April 1921.'),
        ('The hyperinflation of 1923 was caused only by the Treaty of Versailles.', False, 'War debts, printing money and the Ruhr occupation were also important; the treaty was one factor.'),
    ],
    'c': [
        dict(q='‘Reparations were the most important reason why the Germans hated the Treaty of Versailles.’',
             pro=['£6,600 million was seen as a crushing burden that would last for generations', 'Reparations led directly to the Ruhr occupation and hyperinflation in 1923'],
             con=['War guilt (Article 231) was seen as a lie and a national humiliation', 'Being forced to accept a diktat without negotiation caused deep resentment', 'Loss of territory and people, such as the Polish Corridor, angered nationalists', 'Disarmament left Germany feeling defenceless'],
             judge='Reparations caused the most practical hardship, but war guilt and the diktat explain the depth of resentment, because reparations were justified by the war guilt clause'),
        dict(q='How far was the Treaty of Versailles responsible for Germany\'s problems in 1923?',
             pro=['Reparations led to the Ruhr occupation', 'The treaty\'s unpopularity damaged the Weimar Republic and fuelled extremism such as the Munich Putsch'],
             con=['Germany had already been in debt from the war, financed by borrowing', 'The government chose to print money to pay striking workers', 'Political violence from left and right began before the treaty, for example the Spartacist Rising in January 1919'],
             judge='The treaty was an important cause through reparations and the Ruhr, but the war and the government\'s own decisions made the crisis much worse'),
    ],
    'src': [
        S('Article 231 of the Treaty of Versailles, 1919', 'The Allied and Associated Governments affirm and Germany accepts the responsibility of Germany and her allies for causing all the loss and damage to which the Allied and Associated Governments and their nationals have been subjected as a consequence of the war imposed upon them by the aggression of Germany and her allies.',
          'the war guilt clause', 'Germany had to accept responsibility for all the loss and damage of the war, which justified reparations.',
          'To provide a legal basis for the Allies to claim reparations from Germany.',
          'it is the official text of the treaty', 'it tells us what Germany was made to accept, not whether it was true or how Germans reacted',
          'How Germans reacted, for example calling the treaty a diktat, or the reparations figure fixed in 1921.', stance=True, why='it forced Germany to accept all the blame, which Germans saw as unjust', published=False,
          context='Germany had been given the terms in May 1919 and threatened with renewed war if it refused to sign.'),
        S('the German newspaper Deutsche Zeitung, 28 June 1919, the day the treaty was signed (translated, abridged)', 'Vengeance! German nation! Today in the Hall of Mirrors the disgraceful treaty is being signed. Never forget it! The German people will, with unceasing labour, press forward to reconquer the place among the nations to which it is entitled. Then will come vengeance for the shame of 1919.',
          'German reactions to the treaty', 'It shows intense anger and humiliation in Germany and a promise of revenge.',
          'To express nationalist outrage and urge Germans never to accept the treaty.',
          'it was published on the day of signing and shows genuine nationalist feeling', 'it is a nationalist newspaper written to stir emotions, so it does not represent all Germans',
          'That the Weimar government accepted the treaty because it had no choice.', stance=True, why='it presents the treaty as shameful and unjust'),
        S('a cartoon by Will Dyson published in the British newspaper the Daily Herald, 13 May 1919', 'The Big Four leaders are leaving the peace conference. Clemenceau, labelled “The Tiger”, says “Curious! I seem to hear a child weeping!” Behind a pillar a naked child weeps over a copy of the peace treaty. The child is labelled “1940 Class”.',
          'British views of the treaty', 'The cartoonist suggests the treaty is so harsh that it will cause another war, in which the children of 1919 will fight as soldiers around 1940.',
          'To warn readers that the peace terms, just presented to Germany, were too harsh and would lead to future war.',
          'it was published at the time by a British cartoonist, so it shows that some in the victorious countries thought the treaty too harsh', 'the Daily Herald was a left-wing paper that opposed the treaty, so it is one point of view',
          'That most British newspapers supported harsh terms in 1919.', stance=True, why='it suggests the treaty was so harsh it would cause another war', visual=True,
          context='The terms had been given to the German delegation on 7 May 1919.'),
    ],
})


@c3c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3c_bread(r, D):
    i, j = sorted(r.sample(range(len(BREAD)), 2))
    if D <= 2:
        j = i + 1
    (a, pa), (b, pb) = BREAD[i], BREAD[j]
    fac = pb / pa
    tbl = 'Price of a loaf of bread in Berlin (marks): ' + '; '.join(f'{d}: {_big(p)}' for d, p in BREAD) + '.'
    fs = (f'{fac / 1e9:,.0f} billion' if fac >= 1e9 else f'{fac / 1e6:,.1f} million' if fac >= 1e6 else f'{fac:,.0f}' if fac >= 10 else f'{fac:.1f}')
    stem = f'Study the table. {tbl} By how many times did the price of bread increase between {a} and {b}?'
    key = f'{_big(pb)} ÷ {_big(pa)} ≈ {fs} times. 1 mark method, 1 mark answer [2]'
    m = 2
    if D >= 3:
        stem += ' Then explain two reasons why prices rose so quickly in 1923.'
        key = f'Calculation: {_big(pb)} ÷ {_big(pa)} ≈ {fs} times (1 mark method, 1 mark answer). Reasons (up to 2 marks each): the Ruhr occupation cut production; the government printed money to pay striking workers; reparations and war debts; loss of confidence in the mark [6]'
        m = 6
    return {'stem': stem, 'answer': f'About {fs} times.' + (' Reasons: the French and Belgian occupation of the Ruhr cut German production; the government printed money to pay the striking Ruhr workers and its debts, so more money chased fewer goods and the mark lost its value.' if D >= 3 else ''),
            'key': key, 'marks': m, 'minutes': _mins(m), 'type': 'numerical'}


c3d = T('The other treaties: Saint-Germain, Trianon, Neuilly, Sèvres and Lausanne', 'other treaties', 'saint-germain', 'trianon', 'neuilly', 'sèvres', 'lausanne')
build(c3d, {
    'enq': 'the treatment of Germany\'s allies', 'claim': 'the other peace treaties were as harsh as the Treaty of Versailles',
    'stim': ['Separate treaties were made with Germany\'s allies: Austria, Hungary, Bulgaria and Turkey.', 'The treaties with Germany\'s allies redrew the map of central and eastern Europe and the Middle East.'],
    'terms': [
        ('Treaty of Saint-Germain', 'the 1919 treaty with Austria, which forbade union with Germany and limited its army to 30,000'),
        ('Treaty of Trianon', 'the 1920 treaty with Hungary, by which it lost about two-thirds of its territory'),
        ('Treaty of Neuilly', 'the 1919 treaty with Bulgaria, which lost its Aegean coastline to Greece'),
        ('Treaty of Sèvres', 'the 1920 treaty with the Ottoman Empire, rejected by Turkish nationalists'),
        ('Treaty of Lausanne', 'the 1923 treaty that replaced Sèvres and recognised modern Turkey'),
        ('mandate', 'a territory governed by a member of the League on its behalf, such as Iraq, Palestine and Syria'),
    ],
    'dates': [('the Treaty of Saint-Germain was signed with Austria', 1919, 9), ('the Treaty of Neuilly was signed with Bulgaria', 1919, 11),
              ('the Treaty of Trianon was signed with Hungary', 1920, 6), ('the Treaty of Sèvres was signed with the Ottoman Empire', 1920, 8), ('the Treaty of Lausanne was signed with Turkey', 1923, 7)],
    'mcq': [
        ('Which treaty dealt with Hungary?', 'Trianon', ['Neuilly', 'Saint-Germain', 'Sèvres'], 'Treaty of Trianon, June 1920. [1]'),
        ('Which country gained Transylvania from Hungary under the Treaty of Trianon?', 'Romania', ['Italy', 'Greece', 'Bulgaria'], '[1]'),
        ('What did the Treaty of Saint-Germain forbid Austria to do?', 'Unite with Germany', ['Join the League of Nations at any time', 'Keep any army at all', 'Trade with Italy'], 'Anschluss was forbidden; the army was limited to 30,000. [1]'),
        ('Why was the Treaty of Sèvres replaced by the Treaty of Lausanne?', 'Turkish nationalists led by Mustafa Kemal rejected it and fought back successfully', ['The League of Nations declared it illegal', 'The USA refused to sign it', 'The Ottoman Sultan won a war against Britain'],
         'Kemal\'s forces defeated Greece and forced a new treaty in 1923. [1]'),
    ],
    'a': [
        ('Describe the terms of the Treaty of Saint-Germain (1919).', 'terms of the Treaty of Saint-Germain',
         ['Austria\'s army was limited to 30,000', 'Union with Germany was forbidden', 'Bohemia and Moravia went to Czechoslovakia', 'South Tyrol and Trieste went to Italy', 'Bosnia, Croatia and Slovenia went to the new Kingdom of Serbs, Croats and Slovenes (Yugoslavia)', 'Galicia went to Poland']),
        ('Describe the terms of the Treaty of Trianon (1920).', 'terms of the Treaty of Trianon',
         ['Hungary lost about two-thirds of its territory', 'About three million Hungarians were left living in other countries', 'Transylvania went to Romania', 'Slovakia and Ruthenia went to Czechoslovakia', 'Croatia went to Yugoslavia', 'Hungary\'s army was limited to 35,000']),
        ('Describe how the treatment of Turkey changed between the treaties of Sèvres and Lausanne.', 'differences between the treaties of Sèvres and Lausanne',
         ['Sèvres gave Smyrna and Eastern Thrace to Greece, but Lausanne returned them to Turkey', 'Sèvres put the Straits under international control; at Lausanne they stayed Turkish but demilitarised', 'Lausanne removed the military restrictions and reparations of Sèvres', 'Both confirmed the loss of the Arab lands, which became British and French mandates']),
    ],
    'b': [
        ('Why did Hungary resent the Treaty of Trianon?',
         ['It lost about two-thirds of its land, including Transylvania and Slovakia', 'Around three million Hungarians were left under foreign rule, against self-determination', 'It lost most of its industry, raw materials and access to the sea', 'Its army was limited to 35,000']),
        ('Why was the Treaty of Sèvres never put into effect?',
         ['Turkish nationalists led by Mustafa Kemal refused to accept the loss of Turkish land', 'Kemal\'s forces defeated the Greek army, which had occupied Smyrna', 'Britain and France were unwilling to fight a new war to enforce it', 'The Sultan\'s government that signed it lost authority to Kemal\'s nationalists']),
        ('Why did the other treaties cause problems for the new states of eastern Europe?',
         ['The new states, such as Czechoslovakia and Yugoslavia, contained many national minorities', 'Austria and Hungary became small and economically weak after losing industry and markets', 'Disputes over borders, such as Hungary\'s claims to lost land, created lasting tension', 'Small states were vulnerable to larger neighbours such as Germany and the USSR']),
    ],
    'claims': [
        ('The Treaty of Lausanne was harsher on Turkey than the Treaty of Sèvres.', False, 'Lausanne returned land to Turkey, removed reparations and military limits; it was a success for Turkish nationalism.'),
        ('Austria was forbidden to unite with Germany by the Treaty of Saint-Germain.', True, 'Anschluss was forbidden, even though most Austrians were German-speaking.'),
        ('Bulgaria gained land under the Treaty of Neuilly because it had supported the Allies.', False, 'Bulgaria fought for the Central Powers; it lost Western Thrace (its Aegean coastline) to Greece and land to Yugoslavia.'),
    ],
    'c': [
        dict(q='‘Hungary was treated more harshly than any other defeated power.’',
             pro=['Hungary lost about two-thirds of its land, a higher share than any other power', 'Millions of Hungarians were placed under foreign rule'],
             con=['Germany paid far larger reparations and accepted war guilt', 'Austria was reduced to a small state and forbidden to unite with Germany', 'The Ottoman Empire lost all its Arab lands'],
             judge='In territorial terms Hungary suffered most, but Germany faced the heaviest combination of reparations, war guilt and disarmament'),
        dict(q='How far did the treaties with Germany\'s allies follow the principle of self-determination?',
             pro=['Czechoslovakia, Yugoslavia and an enlarged Romania gave national groups their own states', 'Poland was restored, partly from former Austrian land'],
             con=['Germans in Austria and the Sudetenland were denied self-determination', 'Millions of Hungarians were left in other states', 'Arab lands became mandates of Britain and France, not independent states'],
             judge='The treaties applied self-determination to the Allies\' friends but not to the defeated peoples or to colonial territories'),
    ],
    'src': [
        S('a Hungarian poster of the early 1920s (description of a typical design)', 'The poster shows a map of the old Kingdom of Hungary with the lost lands shaded in black. The title says “No, no, never!”',
          'Hungarian reactions to the Treaty of Trianon', 'It shows Hungarians refused to accept the loss of territory and wanted it returned.',
          'To build public support for revising the Treaty of Trianon.',
          'it shows genuine popular feeling in Hungary after the treaty', 'it is propaganda designed to stir anger and gives only the Hungarian view',
          'The views of Romanians, Slovaks and others who gained their own states.', stance=True, why='it presents the losses as unjust', visual=True,
          context='The treaty, signed in June 1920, took about two-thirds of Hungary\'s territory.'),
        S('an extract from a modern history textbook (illustrative)', 'The Treaty of Lausanne was a triumph for Turkish nationalism. Turkey regained Eastern Thrace and Smyrna, paid no reparations and faced no limits on its armed forces.',
          'the Treaty of Lausanne', 'It shows Turkey was treated far more leniently at Lausanne than the other defeated powers.',
          'To explain the outcome of the Lausanne negotiations to students.',
          'it is written with hindsight and its facts can be checked', 'it is a summary and does not explain why the Allies agreed to these terms',
          'That Kemal\'s military victories forced the Allies to negotiate.', stance=False, why='it shows Turkey was not treated harshly at Lausanne', kind='secondary', published=True),
    ],
})

c3e = T('Could the treaties be justified at the time?', 'treaties be justified', 'justified at the time')
build(c3e, {
    'enq': 'whether the Treaty of Versailles was fair', 'claim': 'the Treaty of Versailles could be justified at the time',
    'stim': ['Historians still disagree about whether the Treaty of Versailles was fair to Germany.', 'In 1919 J. M. Keynes, a British economist, attacked the Treaty of Versailles as unjust.',
             'Defenders of the treaty pointed to how Germany had treated Russia in 1918.'],
    'terms': [
        ('Treaty of Brest-Litovsk', 'the March 1918 treaty in which Germany took vast lands, people and resources from Russia'),
        ('Carthaginian peace', 'a brutally harsh peace meant to crush a defeated enemy; Keynes used the phrase about Versailles'),
        ('hindsight', 'understanding an event after it has happened, knowing what came next'),
        ('revisionism', 'the wish to change (revise) a treaty, as Germany wanted to change Versailles'),
        ('war guilt', 'the blame for causing the war, which Germany had to accept under Article 231'),
    ],
    'dates': [('Germany imposed the Treaty of Brest-Litovsk on Russia', 1918), ('Keynes published The Economic Consequences of the Peace', 1919),
              ('the Dawes Plan reorganised reparations payments', 1924), ('the Young Plan reduced the reparations total', 1929), ('reparations payments were ended at the Lausanne Conference', 1932)],
    'mcq': [
        ('Which argument was used at the time to defend the Treaty of Versailles?', 'Germany had imposed an even harsher treaty on Russia at Brest-Litovsk', ['Germany had asked for harsher terms', 'Germany had won the war', 'The treaty gave Germany new colonies'],
         'Brest-Litovsk took about a third of Russia\'s population and much of its industry. [1]'),
        ('Which British economist called the Treaty of Versailles a “Carthaginian peace”?', 'J. M. Keynes', ['David Lloyd George', 'Neville Chamberlain', 'Winston Churchill'], 'In The Economic Consequences of the Peace (1919). [1]'),
        ('Which of these is an argument that the treaty was NOT too harsh?', 'Germany kept most of its territory and remained Europe\'s largest industrial economy', ['Germany had no say in the terms', 'Germans were placed under Polish rule', 'Germany had to accept war guilt'],
         'Germany was not occupied or broken up and recovered economically by the late 1920s. [1]'),
    ],
    'a': [
        ('Describe the arguments used at the time to justify the Treaty of Versailles.', 'arguments used at the time to justify the treaty',
         ['Germany had imposed the harsh Treaty of Brest-Litovsk on Russia in 1918', 'Northern France and Belgium had been devastated and needed rebuilding', 'Victorious governments faced public demands to punish Germany',
          'Germany kept most of its land and its industrial strength', 'Disarmament aimed to prevent future German aggression']),
        ('Describe the criticisms made of the Treaty of Versailles in 1919.', 'criticisms made of the treaty in 1919',
         ['It was a diktat imposed without negotiation', 'War guilt was unfair because other countries shared responsibility', 'Keynes argued reparations would ruin Germany and harm Europe\'s economy',
          'Self-determination was denied to Germans', 'Some, like the cartoonist Will Dyson, warned it would lead to another war']),
    ],
    'b': [
        ('Why did some people in 1919 believe the treaty was too lenient on Germany?',
         ['France wanted the Rhineland separated from Germany and did not get it', 'Germany kept its industrial heartland in the Ruhr and remained potentially the strongest power in Europe', 'Germany\'s population was larger than France\'s', 'They thought Germany would recover and seek revenge, so it needed to be weakened further']),
        ('Why did Keynes argue that the treaty was unwise?',
         ['He thought the reparations were more than Germany could pay', 'A ruined Germany would harm the trade and recovery of the whole of Europe', 'Economic hardship would cause unrest and political extremism', 'He believed the peace was motivated by revenge rather than reconstruction']),
        ('Why is it difficult to decide whether the treaty was fair?',
         ['Judgements depend on whose point of view is taken: France, Britain, the USA or Germany', 'Historians have hindsight that the peacemakers lacked, such as knowledge of Hitler', 'Germany\'s own war aims and Brest-Litovsk suggest it would have imposed a harsh peace', 'Reparations were reduced later, so their real burden is disputed']),
    ],
    'claims': [
        ('Germany paid the full £6,600 million of reparations in the 1920s.', False, 'Payments were reduced by the Dawes (1924) and Young (1929) Plans and ended in 1932; only a fraction was paid.'),
        ('Some people in Britain at the time thought the Treaty of Versailles was too harsh.', True, 'For example Keynes and the cartoonist Will Dyson; even Lloyd George had doubts.'),
        ('Brest-Litovsk shows that Germany was treated more harshly than it had treated others.', False, 'Brest-Litovsk took about a third of Russia\'s population and much of its industry, which defenders of Versailles used to argue the opposite.'),
    ],
    'c': [
        dict(q='‘The Treaty of Versailles was fair given the situation in 1919.’',
             pro=['France and Belgium had suffered great destruction and needed compensation', 'Germany had imposed the far harsher Treaty of Brest-Litovsk on Russia', 'The peacemakers faced strong public pressure to punish Germany', 'Germany was left intact and economically strong'],
             con=['Germany was not allowed to negotiate', 'War guilt ignored the shared responsibility of other powers', 'Self-determination was denied to Germans', 'Reparations caused economic hardship and resentment'],
             judge='By the standards of 1919, after a devastating war, the treaty can be seen as a harsh but understandable compromise; its weakness was that it was hated by Germans but not harsh enough to stop German recovery'),
        dict(q='How far was the Treaty of Versailles a “Carthaginian peace”?',
             pro=['Germany lost land, colonies, its air force and most of its navy', 'War guilt and reparations were seen as humiliating and crippling'],
             con=['Germany was not occupied or divided and kept most of its population and industry', 'Reparations were reduced and only partly paid', 'Germany recovered quickly in the late 1920s'],
             judge='The treaty was harsh in tone and in some terms, but it fell far short of destroying Germany, so “Carthaginian” overstates it'),
    ],
    'src': [
        S('J. M. Keynes, The Economic Consequences of the Peace, published in December 1919 (abridged)', 'The policy of reducing Germany to servitude for a generation, of degrading the lives of millions of human beings, and of depriving a whole nation of happiness should be abhorrent and detestable.',
          'the reparations terms of the treaty', 'Keynes argues that the treaty, especially reparations, was a cruel policy that would ruin the lives of millions of Germans.',
          'To persuade the public in Britain and the USA that the treaty should be revised.',
          'Keynes was an expert economist who attended the conference as a Treasury adviser', 'he had resigned in protest and wrote to attack the treaty, so it is one-sided',
          'That reparations were later reduced by the Dawes and Young Plans.', stance=False, why='it argues the treaty was unjust and too harsh', kind='primary'),
        S('an editorial in a British newspaper, June 1919 (illustrative)', 'Germany complains of harsh terms. Let her remember Brest-Litovsk, and the towns of northern France that her armies left in ruins. She has been treated with more justice than she showed to others.',
          'British attitudes to the treaty', 'It argues the treaty was justified because Germany had been harsher to Russia and had caused great destruction.',
          'To defend the treaty against German complaints and reassure British readers.',
          'it reflects common British opinion at the time', 'it is written from a victor\'s viewpoint and ignores German grievances',
          'That some British people, including Keynes, thought the treaty unwise.', stance=True, why='it defends the treaty as fair'),
        S('an extract from a modern history textbook (illustrative)', 'The treaty was too harsh to be accepted by Germans, yet too lenient to stop Germany recovering its strength. It satisfied nobody and created resentment without guaranteeing security.',
          'the treaty in the longer term', 'It argues the treaty was a poor compromise: it caused resentment without weakening Germany enough.',
          'To give students a balanced interpretation with the benefit of hindsight.',
          'it is written with hindsight and can draw on later evidence', 'hindsight was not available to the peacemakers; the extract is a brief summary',
          'The pressure the peacemakers faced from public opinion in 1919.', stance=False, why='it suggests the treaty was a failure, though it accepts the difficulty of the task', kind='secondary', published=True),
    ],
})

CHAPTERS[3] = [c3a, c3b, c3c, c3d, c3e]


# ============================================================== CHAPTER 4: To what extent was the League of Nations a success?

c4a = T('Aims, organisation and membership of the League', 'aims organisation membership', 'league')
build(c4a, {
    'enq': 'the League of Nations when it was set up', 'claim': 'the League of Nations was weak from the start',
    'stim': ['The League of Nations was set up in January 1920 with its headquarters in Geneva.', 'The Covenant of the League of Nations was written into all the peace treaties of 1919-20.',
             'Forty-two countries were members of the League of Nations when it began.'],
    'terms': [
        ('Covenant', 'the set of rules of the League of Nations, which all members agreed to follow'),
        ('Assembly', 'the League\'s “parliament”, in which every member had one vote; it met once a year'),
        ('Council', 'the small League body, with permanent members such as Britain and France, that met several times a year and dealt with crises'),
        ('Permanent Court of International Justice', 'the League\'s court at The Hague that gave rulings on legal disputes between countries'),
        ('International Labour Organisation', 'the League agency that worked to improve working conditions around the world'),
        ('economic sanctions', 'measures such as banning trade with an aggressor to put pressure on it'),
        ('moral condemnation', 'the League\'s first step against an aggressor: publicly declaring its actions wrong'),
    ],
    'dates': [('the League of Nations officially came into existence', 1920), ('Germany joined the League', 1926), ('Japan and Germany both left the League', 1933),
              ('the USSR joined the League', 1934), ('Italy left the League', 1937), ('the USSR was expelled from the League after invading Finland', 1939)],
    'mcq': [
        ('Where were the headquarters of the League of Nations?', 'Geneva', ['Paris', 'London', 'New York'], 'In neutral Switzerland. [1]'),
        ('Which of these countries was a permanent member of the League Council when it was set up?', 'Japan', ['USA', 'Germany', 'USSR'], 'The original permanent members were Britain, France, Italy and Japan. [1]'),
        ('How did the Assembly and Council usually have to make decisions?', 'Unanimously', ['By a simple majority', 'By the vote of the Secretary-General', 'By the Permanent Court'], 'Unanimity made action slow and difficult. [1]'),
        ('Which of these was NOT a power the League could use against an aggressor?', 'Sending its own permanent army', ['Moral condemnation', 'Economic sanctions', 'Asking members to provide troops'], 'The League had no army of its own. [1]'),
    ],
    'a': [
        ('What were the aims of the League of Nations?', 'aims of the League of Nations',
         ['To discourage aggression and keep the peace through collective security', 'To encourage countries to cooperate, especially in business and trade', 'To encourage disarmament', 'To improve living and working conditions of people around the world']),
        ('Describe the organisation of the League of Nations.', 'parts of the League of Nations',
         ['The Assembly met once a year and every member had one vote', 'The Council met several times a year and in emergencies; it had permanent members such as Britain and France', 'The Secretariat was a civil service that kept records and organised the League\'s work',
          'The Permanent Court of International Justice at The Hague settled legal disputes', 'Commissions and agencies dealt with refugees, health, slavery, mandates and working conditions (the ILO)']),
        ('Describe the membership of the League of Nations in the 1920s and 1930s.', 'features of League membership',
         ['The USA never joined', 'Germany was excluded at first and joined in 1926', 'Bolshevik Russia was excluded; the USSR joined only in 1934', 'Japan and Germany left in 1933 and Italy in 1937', 'Britain and France were the most powerful members throughout']),
    ],
    'b': [
        ('Why did the USA not join the League of Nations?',
         ['The Senate rejected the Treaty of Versailles, which included the League Covenant', 'Many Americans wanted isolationism after heavy losses in a European war', 'They feared Article 10 might force the USA to send troops to defend other countries',
          'Some thought membership would harm American trade, for example through sanctions', 'Party politics: Republicans opposed the Democrat Wilson']),
        ('Why was the absence of the USA a weakness for the League?',
         ['The USA was the world\'s richest and most powerful country', 'Economic sanctions would not work if aggressors could still trade with the USA', 'Britain and France were left to lead the League, but were weakened by the war', 'The League appeared to be a club for the victors of the war']),
        ('Why was the League\'s organisation a weakness?',
         ['Decisions had to be unanimous, so one member could block action', 'The Council and Assembly met infrequently, so the League was slow to react', 'It had no army and relied on members to supply troops', 'Its procedures were complicated and decisions could be delayed by enquiries']),
    ],
    'claims': [
        ('The League of Nations had its own army to stop aggressors.', False, 'It had no army; it relied on members such as Britain and France to provide troops, which they were reluctant to do.'),
        ('Germany was a member of the League from 1926 to 1933.', True, 'Germany joined after Locarno in 1926 and Hitler took it out in 1933.'),
        ('The USA was a permanent member of the League Council.', False, 'The USA never joined the League; the original permanent members were Britain, France, Italy and Japan.'),
    ],
    'c': [
        dict(q='‘The absence of the USA was the main weakness of the League of Nations.’',
             pro=['Without the USA, sanctions were weak because aggressors could trade with America', 'The League lacked the world\'s most powerful economy and potential military power'],
             con=['Unanimity and slow procedures made decisions difficult', 'The League had no army', 'Britain and France put their own interests first, as at Corfu and Abyssinia', 'The Depression made countries less willing to act'],
             judge='The USA\'s absence weakened sanctions, but the League failed mainly because its leading members, Britain and France, would not act firmly'),
        dict(q='How far was the League of Nations doomed to failure from the start?',
             pro=['The USA never joined, and Germany and the USSR were excluded at first', 'It had no army and needed unanimous decisions', 'It was linked to the hated peace treaties'],
             con=['It had successes in the 1920s, such as the Aaland Islands and Bulgaria', 'Its agencies helped refugees and fought disease', 'Its failures came mainly in the 1930s, after the Depression'],
             judge='The League had serious weaknesses from the start, but it was the Depression and the aggression of major powers in the 1930s that exposed them'),
    ],
    'src': [
        S('Article 16 of the Covenant of the League of Nations, 1919 (abridged)', 'Should any Member of the League resort to war in disregard of its covenants, it shall ipso facto be deemed to have committed an act of war against all other Members of the League, which hereby undertake immediately to subject it to the severance of all trade or financial relations.',
          'how the League was meant to deal with aggression', 'Members agreed that an attack on one member was an attack on all, and that they would cut all trade with an aggressor.',
          'To set out the principle of collective security and the use of economic sanctions.',
          'it is the official text agreed by the members', 'it shows what was promised, not whether members would actually carry it out',
          'That the USA, a major trading nation, would not be a member, so sanctions would be hard to enforce.', stance=False, why='it suggests the League had strong powers on paper', published=False),
        S('a cartoon by Leonard Raven-Hill in Punch, 10 December 1919, “The Gap in the Bridge”', 'A bridge representing the League of Nations has a missing keystone, while Uncle Sam (the USA) leans on it smoking a pipe.',
          'the League\'s prospects in 1919', 'The cartoonist suggests the League would be incomplete and weak without the USA.',
          'To comment on the US Senate\'s rejection of the treaty in November 1919.',
          'it shows contemporary British opinion', 'it is a comment, not a factual account',
          'Other weaknesses, such as unanimity and the lack of an army.', stance=True, why='it suggests the League was weak from the start without the USA', visual=True,
          context='The US Senate voted against the Treaty of Versailles in November 1919.'),
        S('a speech by a delegate from a small member state to the League Assembly, 1921 (illustrative)', 'Small nations like ours have, for the first time, a place where our voice counts as much as that of the Great Powers. That alone is worth defending.',
          'how smaller countries saw the League', 'It shows small countries valued the equality the Assembly gave them.',
          'To defend the League and encourage support for it among members.',
          'it shows the view of a member state in the League\'s early years', 'it is a speech made to praise the League, so it is optimistic',
          'That decisions needed unanimity, and the Council was dominated by the Great Powers.', stance=False, why='it suggests members had confidence in the League'),
    ],
})

c4b = T('Successes and failures of the League in the 1920s', 'successes and failures', '1920s')
build(c4b, {
    'enq': 'the League\'s work in the 1920s', 'claim': 'the League of Nations was successful in the 1920s',
    'stim': ['In the 1920s the League of Nations dealt with a number of border disputes.', 'The League of Nations had both successes and failures in the 1920s.',
             'The League\'s commissions and agencies carried out humanitarian work in the 1920s.'],
    'terms': [
        ('Aaland Islands', 'islands claimed by both Sweden and Finland; in 1921 the League gave them to Finland and Sweden accepted'),
        ('Vilna', 'the Lithuanian capital seized by Polish troops in 1920; the League failed to make Poland leave'),
        ('Corfu incident', 'the 1923 crisis in which Mussolini bombarded and occupied the Greek island of Corfu'),
        ('Conference of Ambassadors', 'a body of Allied ambassadors that dealt with peace-treaty issues and overruled the League over Corfu'),
        ('Nansen passport', 'an identity document issued through the League to help refugees travel and settle'),
        ('Locarno Treaties', 'agreements of 1925 guaranteeing Germany\'s western borders, made outside the League'),
        ('Kellogg-Briand Pact', 'the 1928 agreement in which over 60 countries promised not to use war to settle disputes'),
    ],
    'dates': [('Polish troops seized Vilna', 1920), ('the League settled the Aaland Islands dispute', 1921), ('Mussolini occupied Corfu', 1923),
              ('the League resolved the Greek-Bulgarian dispute', 1925), ('the Kellogg-Briand Pact was signed', 1928)],
    'mcq': [
        ('Which dispute did the League settle in favour of Finland in 1921?', 'The Aaland Islands', ['Vilna', 'Corfu', 'Upper Silesia'], '[1]'),
        ('How did the Corfu crisis of 1923 end?', 'Greece was made to apologise and pay compensation to Italy', ['Italy was expelled from the League', 'Italy kept Corfu', 'Greece received compensation from Italy'],
         'The Conference of Ambassadors overruled the League; Mussolini then left Corfu. [1]'),
        ('Why is the Greek-Bulgarian dispute of 1925 seen as a League success?', 'Greece withdrew its troops and paid compensation after the League condemned it', ['Bulgaria joined the League as a result', 'The League sent its army to Bulgaria', 'Greece was given part of Bulgaria'],
         'The League acted quickly and both sides accepted the ruling. [1]'),
        ('Who led the League\'s work to return prisoners of war and help refugees?', 'Fridtjof Nansen', ['Albert Thomas', 'Aristide Briand', 'Lord Lytton'], 'Around 400,000 prisoners of war were returned home. [1]'),
    ],
    'a': [
        ('What happened in the Corfu crisis of 1923?', 'events of the Corfu crisis',
         ['The Italian General Tellini and his staff were murdered while mapping the Greek-Albanian border', 'Mussolini demanded compensation and the execution of the murderers', 'Italy bombarded and occupied the Greek island of Corfu',
          'Greece appealed to the League, which condemned Italy', 'The Conference of Ambassadors made Greece apologise and pay 50 million lire, and Italy then left Corfu']),
        ('Describe the League\'s humanitarian work in the 1920s.', 'achievements of the League\'s agencies in the 1920s',
         ['About 400,000 prisoners of war were returned home', 'The Refugee Committee helped refugees, for example with Nansen passports', 'The Health Committee worked against diseases such as leprosy and malaria',
          'The Slavery Commission helped free 200,000 slaves in Sierra Leone', 'The ILO campaigned for better working conditions', 'Loans helped Austria and Hungary to recover']),
        ('What happened in the dispute between Greece and Bulgaria in 1925?', 'events of the Greek-Bulgarian dispute of 1925',
         ['Greek soldiers were killed in an incident on the border with Bulgaria', 'Greece invaded Bulgaria', 'Bulgaria appealed to the League', 'The League ordered Greece to withdraw and pay compensation', 'Greece obeyed, though it complained that larger powers were treated differently']),
    ],
    'b': [
        ('Why was the League able to settle the Aaland Islands dispute?',
         ['Sweden and Finland were both small powers that respected the League', 'Both sides agreed to accept the League\'s decision', 'The League\'s solution protected the Swedish-speaking islanders by demilitarising the islands and guaranteeing their culture', 'No Great Power interest was threatened']),
        ('Why was the League unable to deal effectively with the Corfu crisis?',
         ['Italy was a Great Power and a permanent member of the Council', 'Britain and France were unwilling to confront Mussolini', 'The Conference of Ambassadors overruled the League', 'It showed that a powerful aggressor could get its way by force']),
        ('Why did the League fail to make Poland leave Vilna?',
         ['France saw Poland as an ally against Germany and did not want to act', 'Britain would not act alone so far from home', 'The League had no army of its own', 'Poland was prepared to use force and present the League with a fait accompli']),
    ],
    'claims': [
        ('The Corfu crisis showed that the League could control the Great Powers.', False, 'Italy got its way and Greece was made to pay compensation, showing that a Great Power could defy the League.'),
        ('Some of the League\'s most successful work was done by its agencies rather than in border disputes.', True, 'For example returning about 400,000 prisoners of war and work against disease and slavery.'),
        ('The Locarno Treaties were negotiated by the League of Nations.', False, 'They were made between the powers outside the League, which suggests countries did not fully trust it.'),
    ],
    'c': [
        dict(q='‘The League of Nations was successful in the 1920s.’',
             pro=['It settled disputes over the Aaland Islands (1921), Upper Silesia (1921) and between Greece and Bulgaria (1925)', 'Its agencies returned prisoners of war, helped refugees and fought disease and slavery', 'Germany joined in 1926, strengthening it'],
             con=['It failed over Vilna (1920) and Corfu (1923), when larger powers used force', 'Major agreements such as Locarno and Kellogg-Briand were made outside it', 'It made little progress on disarmament'],
             judge='The League was successful when dealing with small powers and humanitarian problems, but it failed when a larger power was involved'),
        dict(q='How important was the work of the League\'s agencies compared with its work on disputes?',
             pro=['Agencies helped millions: refugees, prisoners of war, freed slaves and disease control', 'Their work continued after 1945 in UN bodies such as the ILO and the WHO'],
             con=['The League\'s main aim was to prevent war, so disputes were the real test', 'Successes in disputes, such as Bulgaria 1925, built confidence in collective security', 'Agency work could not prevent the aggression of the 1930s'],
             judge='The agencies achieved the most lasting successes, but the League\'s reputation depended on keeping the peace, so disputes were more important to its overall success'),
    ],
    'src': [
        S('a cartoon of the kind published in British newspapers in 1923 (illustrative description)', 'The cartoon shows a large figure representing Mussolini standing over a small figure representing Greece. Figures representing the League of Nations look on, uncertain what to do.',
          'the League\'s handling of the Corfu crisis', 'It suggests the League was powerless when a strong country like Italy bullied a weak one.',
          'To criticise the League and the Great Powers for allowing Mussolini to get his way.',
          'it was produced at the time of the crisis and reflects British opinion', 'it is a description of a cartoon whose purpose was to comment, so it simplifies events',
          'That the Conference of Ambassadors, not the League, made the final decision.', stance=False, why='it shows the League failing in a major crisis', visual=True,
          context='Mussolini occupied Corfu in August 1923 after the murder of General Tellini.'),
        S('a report by a League official on the work of the Refugee Commission, 1926 (illustrative)', 'Over the last six years the Commission has brought home some four hundred thousand prisoners of war and helped many thousands of refugees to find homes and work.',
          'the League\'s humanitarian work', 'It suggests the League achieved a great deal of practical work for refugees and prisoners of war.',
          'To show members the achievements of the Commission and justify its funding.',
          'the figures match what historians record about the League\'s work', 'an official report may emphasise success to justify its work',
          'The League\'s failures in disputes such as Vilna and Corfu.', stance=True, why='it shows real successes in humanitarian work'),
        S('an editorial in a Greek newspaper after the Bulgarian crisis, 1925 (illustrative)', 'Greece has accepted the decision of the League, though we cannot help noting that a greater power was treated very differently at Corfu two years ago.',
          'how fairly the League treated different countries', 'It accepts the League\'s decision but complains that the League was stricter with smaller powers.',
          'To accept the ruling while protesting that the League applied double standards.',
          'it reflects Greek opinion, from the country directly involved in both crises', 'Greece had been the loser in both cases, so Greek writers may be bitter',
          'That Greece did withdraw and pay compensation, which shows the League could work.', stance=True, why='it shows the League\'s decision was accepted, though it was a success only against a small power'),
    ],
})

c4c = T("Weaknesses in the League's organisation and the role of collective security", 'weaknesses in the league', 'collective security')
build(c4c, {
    'enq': 'the weaknesses of the League of Nations', 'claim': 'collective security could not work in practice',
    'stim': ['The League of Nations depended on the idea of collective security.', 'Critics argued that the League of Nations was a “toothless tiger”.',
             'The League\'s structure made it slow to take decisions.'],
    'terms': [
        ('collective security', 'the idea that all members act together to protect any member that is attacked, so that aggression is deterred'),
        ('unanimity', 'the rule that decisions needed the agreement of every member present'),
        ('veto', 'the power of one member to block a decision'),
        ('aggressor', 'a country that attacks another without justification'),
        ('disarmament', 'reducing armed forces and weapons, one of the League\'s aims'),
        ('World Disarmament Conference', 'the League conference of 1932-34 that failed to agree on reducing arms'),
    ],
    'dates': [('the Geneva Protocol, which would have strengthened collective security, was rejected by Britain', 1925), ('the World Disarmament Conference opened', 1932),
              ('Germany walked out of the World Disarmament Conference and left the League', 1933), ('the League imposed limited sanctions on Italy', 1935)],
    'mcq': [
        ('What did collective security mean?', 'Members acting together to stop any aggressor', ['Each country building up its own defences', 'Britain and France guaranteeing only their own borders', 'Countries signing secret alliances'], '[1]'),
        ('Why were economic sanctions often ineffective?', 'Non-members such as the USA could keep trading with the aggressor', ['They were never allowed by the Covenant', 'They applied only to small countries', 'The League had to ask Germany\'s permission'], '[1]'),
        ('Which of these made the League slow to act?', 'The Council met only a few times a year and needed unanimous agreement', ['It had too many permanent members from Asia', 'Its court was in Moscow', 'It had too large an army to move quickly'], '[1]'),
    ],
    'a': [
        ('Describe the weaknesses in the League\'s organisation.', 'weaknesses in the League\'s organisation',
         ['Decisions in the Council and Assembly had to be unanimous', 'The Council met only a few times a year, so it reacted slowly', 'The League had no army of its own', 'Sanctions depended on members being willing to apply them', 'Important countries were missing, such as the USA']),
        ('Describe the steps the League could take against an aggressor.', 'steps the League could take against an aggressor',
         ['It could investigate and hold an enquiry, for example the Lytton Commission', 'It could condemn the aggressor (moral condemnation)', 'It could impose economic sanctions such as banning trade', 'It could, in theory, ask members to provide troops for military action']),
    ],
    'b': [
        ('Why did collective security fail to work in the 1930s?',
         ['Britain and France put their own interests first and would not risk war', 'The USA was not a member, so sanctions could be avoided', 'The League had no army and members would not provide troops', 'The aggressors were Great Powers such as Japan and Italy, and simply left the League']),
        ('Why did the League fail to achieve disarmament?',
         ['Members did not trust each other enough to reduce their forces', 'France feared Germany and would not disarm while Germany demanded equal treatment', 'Hitler withdrew Germany from the World Disarmament Conference in 1933', 'The Depression and the rise of dictators increased insecurity']),
        ('Why did Britain and France fail to make the League stronger?',
         ['They were exhausted and in debt after the First World War', 'Britain cared more about its empire and trade than about Europe', 'France was more concerned about security against Germany and made its own alliances', 'Both disagreed about how to deal with Germany']),
    ],
    'claims': [
        ('Sanctions were the League\'s most effective weapon in the 1930s.', False, 'Sanctions against Italy in 1935 excluded oil and were not supported by the USA, so they failed.'),
        ('One member could block a decision of the League Council.', True, 'Decisions needed unanimity, so any member could stop action.'),
        ('The League succeeded in reducing the armed forces of all its members.', False, 'Only the defeated powers were disarmed by the treaties; the World Disarmament Conference of 1932-34 failed.'),
    ],
    'c': [
        dict(q='‘The League failed because of the weaknesses in its organisation.’',
             pro=['Unanimity and infrequent meetings made it slow and indecisive', 'It had no army to enforce decisions', 'Sanctions were weak without the USA'],
             con=['Britain and France\'s self-interest and unwillingness to act was decisive, as over Abyssinia', 'The Depression made countries more aggressive and less willing to cooperate', 'Determined aggressors like Japan and Italy simply left the League'],
             judge='Organisational weaknesses made failure more likely, but the League failed mainly because its leading members lacked the will to use the powers it had'),
        dict(q='How far was collective security a realistic idea?',
             pro=['It worked against small powers in the 1920s', 'All members accepted it in the Covenant'],
             con=['It required countries to risk war for distant states in which they had no interest', 'It needed all the Great Powers to be members, which never happened', 'In the 1930s Great Powers were the aggressors'],
             judge='Collective security was realistic only if the Great Powers were committed to it, which they were not'),
    ],
    'src': [
        S('an extract from a speech by a British Conservative MP, 1935 (illustrative)', 'We are asked to go to war for the sake of countries few of our people could find on a map. Collective security means that Britain does the fighting and the others give their approval.',
          'British attitudes to collective security', 'It shows that some British politicians were unwilling to risk war to enforce collective security.',
          'To argue against using British forces to enforce League decisions.',
          'it reflects views that were common in Britain in the 1930s', 'it is a political speech by one person and is designed to persuade',
          'That Britain had promised in the Covenant to act together with other members.', stance=True, why='it shows members were unwilling to fight to enforce collective security'),
        S('an extract from a modern history textbook (illustrative)', 'The League was not a world government. It could only be as strong as its members wanted it to be, and in the 1930s its most powerful members wanted to avoid war at almost any price.',
          'the League\'s weaknesses', 'It argues the League\'s weakness was the reluctance of its members, not just its structure.',
          'To explain to students why the League failed.',
          'it is written with hindsight and draws on research', 'it is a brief summary that does not discuss the League\'s successes',
          'Successes such as the Aaland Islands or the work of the agencies.', stance=True, why='it argues collective security depended on members who would not act', kind='secondary', published=True),
    ],
})

c4d = T('How the Depression made the work of the League more difficult', 'depression', 'work of the league more difficult')
build(c4d, {
    'enq': 'the effects of the Depression on international relations', 'claim': 'the Depression was the main reason the League failed in the 1930s',
    'stim': ['In October 1929 the Wall Street Crash in the USA began a worldwide economic depression.', 'The Great Depression caused mass unemployment in many countries in the early 1930s.'],
    'terms': [
        ('Wall Street Crash', 'the collapse of share prices on the New York stock exchange in October 1929'),
        ('Great Depression', 'the worldwide economic slump of the early 1930s, with falling trade and mass unemployment'),
        ('tariff', 'a tax on imported goods, used to protect a country\'s own industries'),
        ('protectionism', 'protecting home industries by restricting imports, for example with tariffs'),
        ('militarism', 'the belief that a country should use military strength to achieve its aims; it grew in Japan in the 1930s'),
    ],
    'dates': [('the Wall Street Crash took place', 1929), ('the USA passed the Hawley-Smoot tariff', 1930), ('Japan invaded Manchuria', 1931), ('Hitler became Chancellor of Germany', 1933), ('Italy invaded Abyssinia', 1935)],
    'mcq': [
        ('How did the Depression affect Japan?', 'Its silk exports to the USA collapsed, strengthening the militarists who wanted to expand', ['It became the world\'s largest exporter of oil', 'It joined the USA in a free-trade area', 'It was occupied by the League'], '[1]'),
        ('Why were Britain and France less willing to act against aggressors during the Depression?', 'They were struggling with unemployment and could not afford sanctions or war', ['They had already disarmed completely', 'They had left the League', 'They had become allies of Japan'], '[1]'),
        ('How did the Depression help Hitler?', 'Mass unemployment in Germany increased support for extremist parties', ['It made Germany richer than Britain', 'It ended reparations in 1929', 'It caused the League to give Germany colonies'], '[1]'),
    ],
    'a': [
        ('Describe the effects of the Depression on international trade.', 'effects of the Depression on international trade',
         ['World trade fell sharply after 1929', 'American loans to Europe were recalled', 'Countries raised tariffs to protect their own industries, such as the US Hawley-Smoot tariff of 1930', 'Prices of goods such as silk and wheat collapsed', 'Unemployment rose in many countries']),
        ('Describe how the Depression affected the policies of Japan, Germany and Italy.', 'ways the Depression encouraged aggressive policies',
         ['In Japan the army gained influence and looked to conquer land and resources such as Manchuria', 'In Germany unemployment of about six million helped Hitler win power', 'Mussolini sought an empire, such as Abyssinia, to distract Italians from economic problems', 'Dictators promised to solve economic problems by expansion']),
    ],
    'b': [
        ('Why did the Depression make the work of the League more difficult?',
         ['Countries put their own economic problems first rather than cooperating', 'Britain and France were unwilling to use sanctions that would harm their own trade', 'It helped extreme nationalist governments come to power, as in Germany', 'Countries such as Japan and Italy turned to conquest to gain resources and markets']),
        ('Why did the Depression lead to the rise of militarism in Japan?',
         ['The collapse of the silk trade with the USA ruined many Japanese farmers', 'Japan lacked raw materials and wanted secure supplies and markets', 'The army argued that conquering Manchuria would solve Japan\'s economic problems', 'Civilian governments were blamed for the crisis and lost authority']),
    ],
    'claims': [
        ('The Depression made countries more willing to cooperate through the League.', False, 'Countries turned to protectionism and nationalism, putting their own interests first.'),
        ('The Depression helped Hitler to come to power in Germany.', True, 'Unemployment of about six million in 1932 increased support for the Nazis.'),
        ('The Depression only affected the USA.', False, 'It spread worldwide as American loans were recalled and world trade collapsed.'),
    ],
    'c': [
        dict(q='‘The Depression was the main reason why the League failed in the 1930s.’',
             pro=['It encouraged aggression by Japan and Italy and helped Hitler to power', 'It made Britain and France unwilling to impose sanctions or spend on rearmament'],
             con=['The League had organisational weaknesses from the start: no army, unanimity and no USA', 'Britain and France\'s self-interest, as shown by the Hoare-Laval Pact', 'Determined aggressors simply left the League'],
             judge='The Depression created the conditions for the League\'s failure, but its existing weaknesses and the lack of will among its leading members were what allowed aggression to succeed'),
    ],
    'src': [
        S('figures from the economic historian C. P. Kindleberger, The World in Depression (1973), based on League of Nations data', 'Total monthly imports of 75 countries (millions of US gold dollars): January 1929: 2,998; January 1930: 2,739; January 1931: 1,839; January 1932: 1,206; January 1933: 992.',
          'the effect of the Depression on world trade', 'It shows world trade fell by about two-thirds between January 1929 and January 1933.',
          'To show the scale of the economic collapse after the Wall Street Crash.',
          'statistics based on League data allow comparison over time', 'the figures are totals and do not show how different countries were affected',
          'How the collapse affected politics, for example the rise of militarism in Japan.', stance=True, why='it shows how severe the economic crisis was, which made cooperation harder', kind='secondary', published=True),
        S('an article in a Japanese newspaper, 1931 (illustrative)', 'Our farmers are ruined since America stopped buying our silk. Manchuria, with its coal, iron and land, is Japan\'s lifeline. The government must act.',
          'Japanese attitudes during the Depression', 'It shows economic hardship led many Japanese to support expansion into Manchuria.',
          'To build public support for military action in Manchuria.',
          'it reflects views that were common in Japan in 1931', 'it is written to persuade and does not mention the army\'s own ambitions',
          'That the Kwantung Army staged the Mukden Incident itself in September 1931.', stance=True, why='it links the Depression directly to Japan\'s aggression'),
    ],
})

c4e = T('The League in the 1930s: Manchuria and Abyssinia', 'manchuria', 'abyssinia')
build(c4e, {
    'enq': 'the League\'s handling of Manchuria and Abyssinia', 'claim': 'Britain and France were to blame for the League\'s failure in Abyssinia',
    'stim': ['In September 1931 the Japanese army in Manchuria claimed that Chinese soldiers had sabotaged the South Manchurian Railway.', 'In October 1935 Italian forces invaded Abyssinia.',
             'The crises in Manchuria and Abyssinia exposed the weaknesses of the League of Nations.'],
    'terms': [
        ('Mukden Incident', 'the explosion on the South Manchurian Railway in September 1931, staged by Japanese officers and used as an excuse to invade Manchuria'),
        ('Manchukuo', 'the puppet state set up by Japan in Manchuria in 1932, with the former Chinese emperor Puyi as ruler'),
        ('Lytton Commission', 'the League enquiry into Manchuria, whose 1932 report condemned Japan\'s actions'),
        ('Hoare-Laval Pact', 'the secret British-French plan of December 1935 to give Italy much of Abyssinia'),
        ('Wal-Wal incident', 'the clash between Italian and Abyssinian troops at an oasis in December 1934 that Mussolini used as an excuse for war'),
        ('Stresa Front', 'the 1935 agreement between Britain, France and Italy to oppose German breaches of the Treaty of Versailles'),
    ],
    'dates': [('the Mukden Incident took place', 1931, 9), ('Japan set up the puppet state of Manchukuo', 1932, 3), ('Japan left the League after the Lytton Report was accepted', 1933, 3),
              ('the Wal-Wal incident took place', 1934, 12), ('Italy invaded Abyssinia', 1935, 10), ('the Hoare-Laval plan was leaked to the press', 1935, 12), ('Italian forces captured Addis Ababa', 1936, 5)],
    'mcq': [
        ('What did the Lytton Report conclude about Manchuria?', 'Japan had acted unlawfully and Manchuria should be returned to China', ['Japan had been provoked and should keep Manchuria', 'China should pay compensation to Japan', 'Manchuria should become a League mandate run by Britain'],
         'The Assembly accepted the report in February 1933; Japan left the League. [1]'),
        ('Which important product was NOT included in the League\'s sanctions on Italy in 1935?', 'Oil', ['Weapons', 'Rubber', 'Tin'], 'An oil ban was delayed for fear of how Mussolini and the USA would react. [1]'),
        ('Why did Britain not close the Suez Canal to Italian ships?', 'It feared war with Italy', ['The canal belonged to Italy', 'The League ordered it to stay open for Japan', 'It had already closed it in 1934'], 'Closing the canal would have cut Italy\'s supply route to Abyssinia. [1]'),
        ('Who was the Emperor of Abyssinia who appealed to the League in 1936?', 'Haile Selassie', ['Puyi', 'Mustafa Kemal', 'King Zog'], 'He addressed the Assembly in Geneva in June 1936. [1]'),
    ],
    'a': [
        ('What happened in Manchuria in 1931-33?', 'events of the Manchurian crisis',
         ['Japanese officers staged an explosion on the railway near Mukden in September 1931', 'The Japanese army occupied Manchuria', 'China appealed to the League, which sent the Lytton Commission', 'Japan set up the puppet state of Manchukuo in 1932', 'When the League accepted the Lytton Report, Japan left the League in 1933']),
        ('Describe how the League responded to the Italian invasion of Abyssinia.', 'actions taken by the League over Abyssinia',
         ['The League condemned Italy as the aggressor', 'It imposed economic sanctions in October-November 1935', 'Sanctions did not include oil, coal or steel', 'Britain and France secretly agreed the Hoare-Laval Pact', 'Sanctions were abandoned in July 1936 after Italy had conquered Abyssinia']),
        ('What was the Hoare-Laval Pact?', 'features of the Hoare-Laval Pact',
         ['It was a secret plan made in December 1935 by the British and French foreign ministers', 'It would have given Italy about two-thirds of Abyssinia', 'It was leaked to the press', 'There was public outrage in Britain and Hoare resigned', 'It showed Britain and France were undermining the League']),
    ],
    'b': [
        ('Why did the League fail to stop Japanese aggression in Manchuria?',
         ['Manchuria was far from Europe and Britain and France had no wish to fight there', 'Japan was a permanent member of the Council and a Great Power', 'The Lytton Commission took a year to report, while Japan completed its conquest', 'Without the USA, sanctions would not work; Japan simply left the League']),
        ('Why was the Abyssinian crisis so damaging for the League?',
         ['Abyssinia was a League member and Italy\'s aggression was clear', 'Sanctions were half-hearted and excluded oil', 'Britain and France were seen to betray the League with the Hoare-Laval Pact', 'It showed collective security had failed, encouraging Hitler, who remilitarised the Rhineland in March 1936']),
        ('Why were Britain and France unwilling to take strong action against Italy?',
         ['They wanted Mussolini as an ally against Hitler (the Stresa Front)', 'They feared war with Italy in the Mediterranean', 'Their economies were weakened by the Depression', 'The USA would not support an oil embargo']),
    ],
    'claims': [
        ('After the Lytton Report, Japan withdrew its troops from Manchuria.', False, 'Japan rejected the report and left the League in 1933, keeping Manchuria.'),
        ('The League\'s sanctions against Italy failed partly because they did not include oil.', True, 'Oil was vital for Italy\'s army; an oil embargo was never applied.'),
        ('The Hoare-Laval Pact was approved by the League Assembly.', False, 'It was a secret British-French plan; when it was leaked, public outrage forced Hoare to resign.'),
    ],
    'c': [
        dict(q='‘The Abyssinian crisis was more damaging to the League than the Manchurian crisis.’',
             pro=['Abyssinia was in Europe\'s sphere of interest, close to British and French routes, so the League could have acted', 'Britain and France openly undermined the League with the Hoare-Laval Pact', 'It destroyed faith in sanctions and encouraged Hitler'],
             con=['Manchuria was the first major test, and failure showed a Great Power could defy the League', 'Japan\'s departure in 1933 weakened the League', 'Manchuria set the pattern of delay and inaction'],
             judge='Manchuria exposed the League\'s weakness, but Abyssinia was more damaging because the League had the means to act and its leading members chose not to'),
        dict(q='How far were Britain and France to blame for the League\'s failure in Abyssinia?',
             pro=['They delayed and excluded oil from sanctions', 'Britain kept the Suez Canal open', 'The Hoare-Laval Pact betrayed the League and Abyssinia'],
             con=['Mussolini was the aggressor and was determined to conquer Abyssinia', 'The USA was not a member and would not support an oil embargo', 'The League\'s structure made quick action difficult'],
             judge='Mussolini caused the crisis, but Britain and France were mainly to blame for the League\'s failure because they had the power to stop Italy and chose not to'),
    ],
    'src': [
        S('a cartoon published in the British magazine Punch, August 1935, titled “The Awful Warning”', 'Britain and France are shown addressing Mussolini, who is armed and ready for war. The caption reads: “We don\'t want you to fight, but, by jingo, if you do, we shall probably issue a joint memorandum suggesting a mild disapproval of you.”',
          'British and French attitudes to Mussolini before the invasion', 'The cartoonist suggests Britain and France were too weak and unwilling to take real action against Mussolini.',
          'To mock the weakness of British and French policy as Italy prepared to invade Abyssinia.',
          'it was published in Britain at the time and criticises the British government, so it is not government propaganda', 'it is satirical and exaggerates for effect',
          'That the League did impose limited sanctions in October 1935.', stance=True, why='it suggests Britain and France had no intention of acting firmly', visual=True,
          context='By summer 1935 Italian troops were gathering in Eritrea and Italian Somaliland.'),
        S('an extract from a modern history textbook (illustrative)', 'The Lytton Commission was a careful and fair enquiry, but by the time it reported, Japan was in full control of Manchuria. The League\'s procedures were simply too slow for a determined aggressor.',
          'the League\'s response to Manchuria', 'It argues the League\'s slow procedures, rather than the bad faith of its members, explain the failure in Manchuria.',
          'To explain the League\'s failure to students.',
          'it is written with hindsight and recognises the quality of the enquiry', 'it focuses on Manchuria, not Abyssinia',
          'The role of Britain and France\'s reluctance to act so far from Europe.', stance=False, why='it blames the League\'s slow procedures rather than Britain and France', kind='secondary', published=True),
        S('a report in a British newspaper, December 1935 (illustrative)', 'The news that our Foreign Secretary has agreed to hand two-thirds of Abyssinia to Italy has been met with fury. The country voted for the League; it did not vote for this.',
          'British public reaction to the Hoare-Laval Pact', 'It shows British public anger that the government had betrayed the League over Abyssinia.',
          'To express and stir up public opposition to the Hoare-Laval Pact.',
          'its account of public anger matches the fact that Hoare was forced to resign', 'it is written to condemn the government and gives one side',
          'That the French government also supported the plan, and Mussolini\'s determination to conquer.', stance=True, why='it shows the British government undermining the League'),
    ],
})

CHAPTERS[4] = [c4a, c4b, c4c, c4d, c4e]


# ============================================================== CHAPTER 5: Why had international peace collapsed by 1939?

c5a = T('Long-term consequences of the peace treaties and failures of the League', 'long-term consequences', 'failures of the league')
build(c5a, {
    'enq': 'the long-term causes of the Second World War', 'claim': 'the Treaty of Versailles was the main long-term cause of the Second World War',
    'stim': ['In 1919 many Germans swore that they would overturn the Treaty of Versailles.', 'By the mid-1930s the League of Nations had lost much of its authority.',
             'Hitler\'s foreign policy drew on German resentment of the peace settlement of 1919.'],
    'terms': [
        ('revisionism', 'the aim of changing (revising) the peace treaties, a central aim of German foreign policy between the wars'),
        ('Lebensraum', '“living space”, Hitler\'s aim of gaining land in eastern Europe for the German people'),
        ('Grossdeutschland', 'a “Greater Germany” uniting all German-speaking people in one state'),
        ('rearmament', 'building up armed forces again, which Germany did openly from 1935'),
        ('isolationism', 'the US policy of avoiding involvement in European affairs between the wars'),
    ],
    'dates': [('the Treaty of Versailles was signed', 1919), ('Japan invaded Manchuria', 1931), ('Hitler became Chancellor of Germany', 1933),
              ('Italy invaded Abyssinia', 1935), ('Germany remilitarised the Rhineland', 1936)],
    'mcq': [
        ('Which term of the Treaty of Versailles did Hitler break first when he announced conscription in 1935?', 'The military restrictions', ['The war guilt clause', 'The loss of colonies', 'The Saar arrangements'], 'Conscription and an air force were announced openly in March 1935. [1]'),
        ('Why did the failure over Abyssinia encourage Hitler?', 'It showed Britain and France would not use force to uphold the League', ['It gave Germany Abyssinian oil', 'It made Italy Germany\'s enemy', 'It strengthened the League\'s army'], 'Hitler remilitarised the Rhineland in March 1936 while attention was on Abyssinia. [1]'),
        ('Which of these was a grievance of many Germans about the peace settlement?', 'Millions of Germans lived outside Germany, for example in the Sudetenland', ['Germany had been given too many colonies', 'Germany had been allowed to unite with Austria', 'Germany was forced to join the League in 1919'], '[1]'),
    ],
    'a': [
        ('Describe the German grievances about the Treaty of Versailles that Hitler exploited.', 'German grievances about the Treaty of Versailles',
         ['War guilt was seen as a lie and a humiliation', 'Reparations were blamed for economic hardship', 'Military restrictions left Germany weaker than its neighbours', 'Germans were placed under foreign rule, for example in the Polish Corridor and the Sudetenland', 'Union with Austria was forbidden']),
        ('Describe how the failures of the League in the 1930s affected international relations.', 'consequences of the League\'s failures in the 1930s',
         ['Japan kept Manchuria and left the League in 1933', 'Italy conquered Abyssinia and left the League in 1937', 'Collective security was discredited', 'Dictators believed they could use force without being stopped', 'Countries such as Britain and France turned to appeasement and rearmament instead']),
    ],
    'b': [
        ('Why did the Treaty of Versailles help to cause the Second World War?',
         ['It created resentment that Hitler exploited to win support', 'It left Germany weakened but not destroyed, so it could recover and seek revenge', 'It left German minorities in Czechoslovakia and Poland, which gave Hitler excuses for expansion', 'It was not enforced: Britain came to feel it was too harsh and allowed Hitler to break it']),
        ('Why did the failure of the League make war more likely?',
         ['Aggressors learned that the League would not stop them', 'Collective security was replaced by every country looking after itself', 'Britain and France turned to appeasement', 'Italy and Japan moved closer to Germany, forming the Axis']),
    ],
    'claims': [
        ('The Treaty of Versailles made the Second World War inevitable.', False, 'The treaty caused resentment, but Germany\'s grievances were being peacefully revised in the 1920s; the Depression, Hitler and appeasement were also needed.'),
        ('Hitler used German resentment of the Treaty of Versailles to win support.', True, 'Overturning the treaty was a central Nazi promise.'),
        ('The League stopped Hitler from remilitarising the Rhineland.', False, 'The League and Britain and France took no action in March 1936.'),
    ],
    'c': [
        dict(q='‘The Treaty of Versailles was the main reason for the outbreak of war in 1939.’',
             pro=['Resentment of the treaty helped Hitler win power and support for his foreign policy', 'German minorities in Czechoslovakia and Poland gave Hitler his targets'],
             con=['The failure of the League allowed aggression to go unpunished', 'The Depression helped Hitler to power and made Britain and France reluctant to act', 'Hitler\'s own aims, such as Lebensraum, went far beyond overturning the treaty', 'Appeasement and the Nazi-Soviet Pact made war possible in 1939'],
             judge='The treaty created grievances, but war came in 1939 because Hitler set out to go beyond them and other powers failed to stop him in time'),
        dict(q='How important was the failure of the League of Nations in causing the Second World War?',
             pro=['Manchuria and Abyssinia showed collective security had failed', 'Hitler learned that aggression would not be punished'],
             con=['Hitler\'s aims would probably have led to war anyway', 'Appeasement by Britain and France was a separate policy choice', 'The Nazi-Soviet Pact removed the threat of a two-front war'],
             judge='The League\'s failure was important because it removed the main obstacle to aggression, but it did not itself cause war; Hitler\'s policies did'),
    ],
    'src': [
        S('an extract from a modern history textbook (illustrative)', 'Versailles was not the cause of the war in 1939, but it provided Hitler with the excuses and the popular support he needed. Without the treaty, his message would have found far fewer listeners.',
          'the role of the Treaty of Versailles', 'It argues the treaty was an indirect cause of war because it gave Hitler support and excuses.',
          'To explain the long-term causes of the war to students.',
          'it is written with hindsight and reaches a balanced view', 'it is a short extract and does not discuss other factors in detail',
          'The role of the Depression and appeasement.', stance=True, why='it gives the treaty a central role in Hitler\'s rise and policies', kind='secondary', published=True),
        S('an extract from another modern history book (illustrative)', 'Many of the grievances of 1919 had been reduced by 1929: reparations were cut, Germany was in the League and Allied troops were leaving the Rhineland. It was the Depression, not the treaty, that turned grievance into catastrophe.',
          'how far Versailles caused the war', 'It argues the Depression was more important than the treaty, because German grievances were being peacefully solved before 1929.',
          'To challenge the view that Versailles led directly to war.',
          'the facts about the 1920s can be checked and are accurate', 'it is one historian\'s interpretation and plays down German resentment',
          'That Hitler\'s aims of Lebensraum went far beyond revising the treaty.', stance=False, why='it argues the Depression rather than the treaty caused the collapse of peace', kind='secondary', published=True),
    ],
})

c5b = T("Hitler's foreign policy aims and actions, 1933-38", "hitler's foreign policy", 'aims and actions')
build(c5b, {
    'enq': 'Hitler\'s foreign policy', 'claim': 'Hitler had a clear plan for war from the start',
    'stim': ['When Hitler came to power in 1933, he promised to overturn the Treaty of Versailles.', 'Between 1933 and 1938 Hitler broke several terms of the Treaty of Versailles.',
             'In March 1938 German troops marched into Austria.'],
    'terms': [
        ('Anschluss', 'the union of Germany and Austria, carried out by Hitler in March 1938'),
        ('Lebensraum', 'living space for Germans in eastern Europe, especially in Poland and the USSR'),
        ('Rome-Berlin Axis', 'the 1936 agreement between Mussolini and Hitler to work together'),
        ('Anti-Comintern Pact', 'the 1936 agreement between Germany and Japan against communism, joined by Italy in 1937'),
        ('Anglo-German Naval Agreement', 'the 1935 agreement allowing Germany a navy up to 35 per cent of the size of the British fleet'),
        ('Condor Legion', 'the German air force unit that fought for Franco in the Spanish Civil War and bombed Guernica in 1937'),
        ('Sudetenland', 'the border region of Czechoslovakia with about three million German-speaking people'),
    ],
    'dates': [('Germany left the League of Nations and the Disarmament Conference', 1933, 10), ('Nazis murdered the Austrian Chancellor Dollfuss in a failed putsch', 1934, 7),
              ('the Saar voted to return to Germany', 1935, 1), ('Hitler announced conscription and the Luftwaffe', 1935, 3), ('German troops remilitarised the Rhineland', 1936, 3),
              ('the Anschluss took place', 1938, 3), ('the Munich Agreement was signed', 1938, 9)],
    'mcq': [
        ('What percentage of voters in the Saar plebiscite of January 1935 chose to return to Germany?', 'About 90 per cent', ['About 30 per cent', 'About 50 per cent', 'About 60 per cent'], 'Hitler used it as a propaganda success. [1]'),
        ('Why was the Anglo-German Naval Agreement of 1935 significant?', 'Britain accepted that Germany could break the Treaty of Versailles', ['It banned the German navy', 'It made Britain and Germany allies', 'It gave Germany Britain\'s colonies'], 'It also undermined the Stresa Front. [1]'),
        ('What happened when German troops entered the Rhineland in March 1936?', 'Britain and France protested but took no action', ['The French army forced them to retreat', 'The League imposed oil sanctions on Germany', 'Belgium declared war on Germany'], '[1]'),
        ('Why did Mussolini oppose a Nazi takeover of Austria in 1934?', 'He wanted Austria as a buffer between Italy and Germany', ['He had already annexed Austria', 'He was an ally of the USSR', 'He wanted Austria in the League'], 'He moved troops to the Brenner Pass after Dollfuss was murdered. [1]'),
    ],
    'a': [
        ('What were Hitler\'s foreign policy aims?', 'aims of Hitler\'s foreign policy',
         ['To overturn the Treaty of Versailles', 'To rearm Germany', 'To unite all German-speaking people in a Greater Germany', 'To gain Lebensraum (living space) in eastern Europe', 'To destroy communism and the USSR']),
        ('Describe the remilitarisation of the Rhineland in 1936.', 'features of the remilitarisation of the Rhineland',
         ['German troops marched into the Rhineland on 7 March 1936', 'This broke the Treaty of Versailles and the Locarno Treaties', 'Hitler gave orders to retreat if the French resisted', 'The world was distracted by the Abyssinian crisis', 'Britain and France protested but did not act; many British people thought Germany was "walking into its own back garden"']),
        ('Describe how Hitler achieved the Anschluss in 1938.', 'stages in the Anschluss of 1938',
         ['Hitler pressured the Austrian Chancellor Schuschnigg to give Nazis posts in government', 'Schuschnigg called a plebiscite on Austrian independence', 'Hitler forced him to cancel it and resign', 'German troops entered Austria on 12 March 1938', 'A plebiscite controlled by the Nazis recorded over 99 per cent in favour of union']),
    ],
    'b': [
        ('Why was Hitler able to rearm Germany without being stopped?',
         ['Many in Britain felt Germany had been unfairly disarmed by Versailles', 'Germany\'s neighbours had not disarmed, so Hitler claimed he only wanted equality', 'The League\'s disarmament conference had failed', 'Britain made the Anglo-German Naval Agreement, accepting German rearmament', 'Britain and France were preoccupied with the Depression']),
        ('Why did Britain and France not stop the remilitarisation of the Rhineland?',
         ['France was in the middle of an election campaign and would not act without Britain', 'Many in Britain thought Germany was only moving into its own territory', 'Both were distracted by the Abyssinian crisis', 'They overestimated German strength and feared war']),
        ('Why was the Anschluss important?',
         ['It broke the Treaty of Versailles and the Treaty of Saint-Germain without any response from Britain and France', 'It added Austria\'s population, soldiers and resources to Germany', 'It surrounded western Czechoslovakia on three sides', 'It increased Hitler\'s confidence that he would not be opposed']),
    ],
    'claims': [
        ('Hitler\'s first attempt to take over Austria in 1934 succeeded.', False, 'The 1934 Nazi putsch failed; Mussolini moved troops to the Austrian border and Hitler backed down.'),
        ('The remilitarisation of the Rhineland broke both the Treaty of Versailles and the Locarno Treaties.', True, 'Both had confirmed the Rhineland as a demilitarised zone.'),
        ('The Rome-Berlin Axis was formed before Hitler became Chancellor.', False, 'It was formed in 1936, after Mussolini moved closer to Hitler over Abyssinia.'),
    ],
    'c': [
        dict(q='‘Hitler had a clear plan for war from the start.’',
             pro=['Mein Kampf set out aims of overturning Versailles and gaining Lebensraum in the east', 'The Hossbach Memorandum of 1937 recorded Hitler discussing expansion by force', 'He rearmed rapidly from 1933'],
             con=['Hitler often took advantage of opportunities, as with the Rhineland during the Abyssinian crisis', 'He was cautious and gambled, ready to retreat in the Rhineland', 'The Anschluss was hurried when Schuschnigg called a plebiscite', 'Others\' weakness (appeasement) shaped his timing'],
             judge='Hitler had clear long-term aims, but he was an opportunist about the timing and methods; the outcome also depended on how others responded'),
        dict(q='How important was the remilitarisation of the Rhineland as a turning point in Hitler\'s foreign policy?',
             pro=['It was his first use of troops to break Versailles and Locarno', 'Its success showed Britain and France would not act and increased his confidence', 'Fortifications in the west made it harder for France to help its eastern allies'],
             con=['Rearmament from 1933-35 had already broken the treaty', 'The Anschluss and Munich added more territory and resources', 'The Nazi-Soviet Pact was the decisive step towards war'],
             judge='The Rhineland was a crucial gamble that changed the balance of power, but the Anschluss and Munich did more to make further expansion possible'),
    ],
    'src': [
        S('a speech by Hitler to the Reichstag, 7 March 1936 (summary of the main points)', 'Hitler told the Reichstag that the Franco-Soviet treaty had broken the spirit of Locarno, that Germany was restoring its full sovereignty over the Rhineland, and offered a 25-year non-aggression pact to France and Belgium.',
          'Hitler\'s justification for remilitarising the Rhineland', 'Hitler presented the move as a defensive response to the Franco-Soviet pact and combined it with peace offers.',
          'To justify the move to Germans and to reassure Britain and France so that they would not respond with force.',
          'it shows how Hitler presented his actions on the day', 'Hitler\'s peace offers were propaganda and he privately ordered retreat if France resisted',
          'That German generals feared French action and that Hitler called the 48 hours after the march the most nerve-racking of his life.', stance=False, why='Hitler presented himself as reacting to events rather than following a plan for war',
          context='The march into the Rhineland took place while the League was dealing with Abyssinia.'),
        S('an extract from the Hossbach Memorandum, a record of a meeting between Hitler and his military leaders, November 1937 (summary)', 'Colonel Hossbach recorded that Hitler said Germany\'s problem of living space could only be solved by force, and that Austria and Czechoslovakia should be taken first, at the latest by 1943-45.',
          'Hitler\'s plans in 1937', 'It suggests Hitler was planning expansion by force in a clear sequence.',
          'To record the discussion for those present.',
          'it records a secret meeting at which Hitler spoke freely to his commanders', 'the record was written days later from notes, and some historians argue it reflects Hitler\'s thinking rather than a fixed plan',
          'That Hitler\'s actual timing, as with the Anschluss in 1938, often depended on events.', stance=True, why='it suggests a planned programme of expansion by force', published=False),
    ],
})

c5c = T('Was the policy of appeasement justified?', 'appeasement', 'munich')
build(c5c, {
    'enq': 'the policy of appeasement', 'claim': 'the policy of appeasement was justified',
    'stim': ['In September 1938 Chamberlain flew to Germany three times to meet Hitler.', 'At Munich in September 1938 Britain and France agreed that Germany could take the Sudetenland.',
             'Neville Chamberlain became British Prime Minister in May 1937.'],
    'terms': [
        ('appeasement', 'the policy of giving in to some of a dictator\'s demands in the hope of avoiding war'),
        ('Munich Agreement', 'the agreement of 29-30 September 1938 by which Britain, France and Italy allowed Germany to take the Sudetenland'),
        ('Sudeten Germans', 'the German-speaking minority in the border regions of Czechoslovakia'),
        ('Peace Ballot', 'the 1934-35 survey in which millions of Britons expressed support for the League and disarmament'),
        ('Guilty Men', 'a book published in 1940 that blamed the appeasers for Britain\'s unpreparedness for war'),
    ],
    'dates': [('Chamberlain became Prime Minister', 1937, 5), ('the Munich Agreement was signed', 1938, 9), ('German troops occupied the rest of Czechoslovakia', 1939, 3), ('Britain guaranteed Poland\'s independence', 1939, 3), ('Britain declared war on Germany', 1939, 9)],
    'mcq': [
        ('Which country was NOT invited to the Munich Conference, although its territory was being discussed?', 'Czechoslovakia', ['Italy', 'France', 'Germany'], 'The USSR was not invited either. [1]'),
        ('What did Chamberlain say on his return from Munich on 30 September 1938?', '“I believe it is peace for our time.”', ['“We shall fight on the beaches.”', '“An iron curtain has descended across the Continent.”', '“We have sustained a total and unmitigated defeat.”'],
         'Churchill\'s criticism of Munich in the Commons was “We have sustained a total and unmitigated defeat.” [1]'),
        ('Which event in March 1939 showed that appeasement had failed?', 'German troops occupied the rest of Czechoslovakia', ['Germany remilitarised the Rhineland', 'Germany and Austria united', 'Germany left the League of Nations'], 'Hitler had now taken non-German land, so his claim to be uniting Germans was exposed. [1]'),
        ('Which of these is an argument that appeasement was justified?', 'It gave Britain time to rearm, especially the RAF', ['It encouraged Hitler to make further demands', 'It abandoned Czechoslovakia\'s strong defences', 'It made Stalin distrust Britain and France'], '[1]'),
    ],
    'a': [
        ('Describe the events of the Sudeten crisis in September 1938.', 'events of the Sudeten crisis of 1938',
         ['Hitler demanded the Sudetenland, claiming Sudeten Germans were mistreated', 'Chamberlain met Hitler at Berchtesgaden on 15 September and agreed to parts of the Sudetenland being handed over', 'At Bad Godesberg on 22 September Hitler demanded all of it by 1 October', 'Europe prepared for war and Britain dug trenches and issued gas masks', 'At Munich on 29-30 September Britain, France and Italy agreed Germany could take the Sudetenland']),
        ('What were the terms of the Munich Agreement?', 'terms of the Munich Agreement',
         ['Germany would occupy the Sudetenland in stages from 1 October 1938', 'An international commission would decide other disputed areas', 'Czechoslovakia was not consulted', 'Britain and France promised to guarantee what was left of Czechoslovakia', 'Hitler and Chamberlain also signed a separate declaration that Britain and Germany would never go to war again']),
    ],
    'b': [
        ('Why did Chamberlain follow a policy of appeasement?',
         ['He and many Britons remembered the horrors of the First World War and wanted to avoid another', 'Britain\'s armed forces were not ready for war in 1938', 'Many thought the Treaty of Versailles had been too harsh and Hitler\'s demands were reasonable', 'Britain could not rely on allies: the USA was isolationist and France was divided', 'Some saw Hitler as a barrier against communism']),
        ('Why was the Munich Agreement criticised?',
         ['Czechoslovakia lost its fortified border and its Skoda arms works without being consulted', 'It encouraged Hitler to believe Britain and France would never fight', 'The USSR was excluded and came to distrust Britain and France', 'It did not stop Hitler, who took the rest of Czechoslovakia in March 1939']),
        ('Why did Britain abandon appeasement in 1939?',
         ['Hitler\'s occupation of Prague in March 1939 showed he wanted more than German-speaking land', 'British public opinion turned against Hitler', 'Britain\'s rearmament had progressed, especially fighters and radar', 'Britain gave a guarantee to Poland in March 1939']),
    ],
    'claims': [
        ('The USSR was invited to the Munich Conference.', False, 'The USSR was not invited, which increased Stalin\'s distrust of Britain and France.'),
        ('Appeasement was popular with many British people in 1938.', True, 'Chamberlain was welcomed as a hero on his return from Munich.'),
        ('Britain was fully prepared for war in September 1938.', False, 'Rearmament had begun but the RAF lacked modern fighters and radar was incomplete; this was a key argument for buying time.'),
    ],
    'c': [
        dict(q='‘Chamberlain was right to follow a policy of appeasement.’',
             pro=['Britain was not ready for war in 1938 and used the year to build fighters and radar', 'Public opinion and the Dominions did not support war over the Sudetenland', 'Many believed German grievances over Versailles were genuine', 'It showed that Britain had tried everything, uniting the country when war came in 1939'],
             con=['It encouraged Hitler to make further demands', 'Czechoslovakia\'s army and defences were abandoned', 'Germany also used the time to rearm', 'It made Stalin distrust the West, leading to the Nazi-Soviet Pact'],
             judge='Appeasement was understandable given Britain\'s position and public opinion, but it misjudged Hitler and made war more likely on worse terms'),
        dict(q='How far was appeasement responsible for the outbreak of war in 1939?',
             pro=['It allowed Hitler to grow stronger with each success', 'It convinced Hitler that Britain and France would not fight for Poland', 'It pushed Stalin towards the Nazi-Soviet Pact'],
             con=['Hitler\'s aims of Lebensraum made war likely anyway', 'The Nazi-Soviet Pact removed the danger of a two-front war', 'The failure of the League and the Depression had already weakened the peace'],
             judge='Appeasement did not cause the war, but it made it more likely by encouraging Hitler and failing to build an alliance with the USSR'),
    ],
    'src': [
        S('a radio broadcast by Neville Chamberlain to the British people, 27 September 1938 (extract)', 'How horrible, fantastic, incredible it is that we should be digging trenches and trying on gas-masks here because of a quarrel in a far away country between people of whom we know nothing.',
          'Chamberlain\'s attitude to the Sudeten crisis', 'Chamberlain suggests that Britain should not go to war over Czechoslovakia, a distant dispute that did not concern Britain directly.',
          'To prepare the British people for a peaceful settlement and justify his efforts to avoid war.',
          'it is Chamberlain\'s own words at the height of the crisis', 'it was broadcast to influence public opinion, so it may not reveal all his reasoning, such as concerns about rearmament',
          'That Britain\'s military chiefs had warned the country was not ready for war.', stance=True, why='it shows Chamberlain\'s genuine wish to avoid an unnecessary war, which the public shared'),
        S('a speech by Winston Churchill in the House of Commons, 5 October 1938 (extract)', 'We have sustained a total and unmitigated defeat.',
          'reactions to the Munich Agreement', 'Churchill condemns the Munich Agreement as a complete defeat for Britain and France.',
          'To attack Chamberlain\'s policy and warn Parliament of the dangers of further appeasement.',
          'Churchill was an MP with access to information about German rearmament', 'he was a long-standing critic of appeasement and of the government, so his view is one-sided',
          'That most MPs and much of the public supported the agreement at the time.', stance=False, why='it argues Munich was a disaster'),
        S('a letter to a British newspaper from a First World War veteran, October 1938 (illustrative)', 'I lost two brothers on the Somme. Anyone who has seen what I have seen will thank Mr Chamberlain with all his heart.',
          'British public reaction to Munich', 'It shows that many people who remembered the First World War supported appeasement.',
          'To express support for Chamberlain and the Munich Agreement.',
          'it reflects the strong feeling of relief in Britain in 1938', 'it is one person\'s emotional view and does not consider the effect on Czechoslovakia',
          'That Hitler occupied the rest of Czechoslovakia in March 1939.', stance=True, why='it shows the policy had strong public support rooted in the memory of war'),
    ],
})

c5d = T('The Nazi-Soviet Pact and the outbreak of war in September 1939', 'nazi-soviet pact', 'outbreak of war in september 1939')
build(c5d, {
    'enq': 'the Nazi-Soviet Pact', 'claim': 'the Nazi-Soviet Pact was the most important cause of war in September 1939',
    'stim': ['On 23 August 1939 Nazi Germany and the Soviet Union signed a non-aggression pact.', 'On 1 September 1939 German forces invaded Poland.',
             'In March 1939 Britain and France guaranteed to defend Poland.'],
    'terms': [
        ('Nazi-Soviet Pact', 'the non-aggression pact signed by Germany and the USSR on 23 August 1939'),
        ('secret protocol', 'the hidden part of the Nazi-Soviet Pact dividing Poland and eastern Europe into German and Soviet spheres'),
        ('Polish Corridor', 'the strip of Polish land separating East Prussia from the rest of Germany'),
        ('Danzig', 'the mainly German Free City under League control that Hitler demanded in 1939'),
        ('Pact of Steel', 'the military alliance signed by Germany and Italy in May 1939'),
        ('ultimatum', 'a final demand with a threat of action if it is not met'),
    ],
    'dates': [('Britain and France guaranteed Poland', 1939, 3), ('Germany and Italy signed the Pact of Steel', 1939, 5), ('the Nazi-Soviet Pact was signed', 1939, 8),
              ('Germany invaded Poland', 1939, 9.01), ('the Soviet Union invaded eastern Poland', 1939, 9.17)],
    'mcq': [
        ('Who signed the Nazi-Soviet Pact on behalf of the two governments?', 'Ribbentrop and Molotov', ['Hitler and Stalin', 'Chamberlain and Daladier', 'Göring and Trotsky'], 'The foreign ministers signed in Moscow. [1]'),
        ('Why did Stalin sign the Nazi-Soviet Pact?', 'To gain time to prepare for war and land in eastern Europe', ['Because he admired Nazi ideas', 'Because Britain had asked him to', 'To win back Alsace-Lorraine'], '[1]'),
        ('On what date did Britain and France declare war on Germany?', '3 September 1939', ['1 September 1939', '23 August 1939', '17 September 1939'], 'Two days after the invasion of Poland, when their ultimatum expired. [1]'),
        ('What did the secret protocol of the Nazi-Soviet Pact provide?', 'The division of Poland and eastern Europe between Germany and the USSR', ['A joint invasion of Britain', 'The return of German colonies', 'Soviet membership of the Axis'], '[1]'),
    ],
    'a': [
        ('What were the terms of the Nazi-Soviet Pact?', 'terms of the Nazi-Soviet Pact',
         ['Germany and the USSR promised not to attack each other for ten years', 'They agreed not to help any enemy of the other', 'A secret protocol divided Poland between them', 'The USSR would have a sphere of influence over the Baltic states and Bessarabia', 'A separate trade agreement gave Germany Soviet raw materials']),
        ('Describe the events that led from the Nazi-Soviet Pact to war in September 1939.', 'events leading from the Nazi-Soviet Pact to war',
         ['The pact was signed in Moscow on 23 August 1939', 'Britain confirmed its guarantee with an Anglo-Polish alliance on 25 August', 'Germany invaded Poland on 1 September', 'Britain and France sent an ultimatum demanding withdrawal', 'They declared war on 3 September and the USSR invaded eastern Poland on 17 September']),
    ],
    'b': [
        ('Why did Stalin sign the Nazi-Soviet Pact?',
         ['He distrusted Britain and France after they excluded him from Munich', 'The Anglo-French mission to Moscow in August 1939 was slow and low-ranking, suggesting they were not serious', 'He needed time to build up the Red Army, weakened by the purges', 'The pact gave him land in Poland and the Baltic states as a buffer zone']),
        ('Why did the Nazi-Soviet Pact make war more likely?',
         ['Hitler no longer feared a war on two fronts', 'Poland could not be helped by the USSR', 'Hitler believed Britain and France would back down again', 'It cleared the way for the invasion of Poland eight days later']),
        ('Why did Britain and France go to war over Poland in 1939 when they had not fought for Czechoslovakia?',
         ['The occupation of Prague in March 1939 had shown Hitler could not be trusted', 'They had given Poland a public guarantee', 'Rearmament had made Britain more ready to fight', 'Public opinion had turned against appeasement']),
    ],
    'claims': [
        ('The Nazi-Soviet Pact made Germany and the USSR allies who shared the same ideology.', False, 'It was a non-aggression pact of convenience between enemies; Hitler attacked the USSR in 1941.'),
        ('The USSR invaded eastern Poland in September 1939.', True, 'Soviet troops entered Poland on 17 September 1939, as agreed in the secret protocol.'),
        ('Britain declared war on Germany on the same day that Germany invaded Poland.', False, 'Germany invaded on 1 September; Britain and France declared war on 3 September.'),
    ],
    'c': [
        dict(q='‘The Nazi-Soviet Pact was the most important reason for the outbreak of war in 1939.’',
             pro=['It removed the danger of a two-front war, allowing Hitler to invade Poland', 'It divided Poland between Germany and the USSR, making the invasion safe'],
             con=['Hitler\'s aim of Lebensraum meant war in the east was always likely', 'Appeasement had convinced Hitler that Britain and France would not fight', 'The failures of the League and the Treaty of Versailles created the conditions for war'],
             judge='The pact was the immediate trigger that made war in September 1939 possible, but the deeper causes lay in Hitler\'s aims and the earlier failure to stop him'),
        dict(q='How far were Britain and France to blame for the Nazi-Soviet Pact?',
             pro=['They excluded Stalin from Munich', 'Their mission to Moscow in 1939 was slow and lacked authority', 'They would not agree to Soviet troops entering Poland'],
             con=['Poland refused to allow Soviet troops on its soil', 'Stalin could gain more from Hitler, including land', 'Stalin\'s own priority was buying time to rearm'],
             judge='Britain and France contributed through their distrust of the USSR, but Stalin made a calculated choice based on what Hitler could offer'),
    ],
    'src': [
        S('a cartoon by David Low titled “Rendezvous”, published in the British newspaper the Evening Standard, 20 September 1939', 'Hitler and Stalin meet over the body of a dead soldier representing Poland. They bow politely to each other. Hitler says: “The scum of the earth, I believe?” Stalin replies: “The bloody assassin of the workers, I presume?”',
          'the Nazi-Soviet Pact', 'The cartoonist suggests the pact was a cynical deal between two enemies who still hated each other, made at the expense of Poland.',
          'To mock the pact and show readers it was based on hypocrisy, just after both had invaded Poland.',
          'Low was a well-informed cartoonist and the cartoon was published at the time', 'it is a satirical comment by a British critic of both dictators',
          'That Stalin had tried, and failed, to reach an agreement with Britain and France in 1939.', stance=True, why='it shows the pact led directly to the destruction of Poland', visual=True,
          context='Germany invaded Poland on 1 September and the USSR on 17 September 1939.'),
        S('a statement in a Soviet history textbook published in the 1980s (summary)', 'The textbook stated that the USSR signed the pact only because Britain and France had refused to form a genuine alliance against Hitler and wanted to turn German aggression eastwards.',
          'Soviet views of the pact', 'It argues the USSR signed the pact defensively because the West had refused to cooperate.',
          'To defend Soviet policy and blame the Western powers.',
          'it shows how the Soviet government explained the pact', 'it is Soviet propaganda and did not mention the secret protocol, whose existence the USSR denied until 1989',
          'The secret protocol dividing Poland and the Baltic states.', stance=False, why='it presents the pact as a defensive reaction to Western appeasement rather than a cause of war', kind='secondary'),
    ],
})

CHAPTERS[5] = [c5a, c5b, c5c, c5d]


# ============================================================== CHAPTER 6: Who was to blame for the Cold War?

c6a = T('Why the USA-USSR alliance broke down in 1945: Yalta and Potsdam', 'yalta and potsdam', 'alliance broke down in 1945')
build(c6a, {
    'enq': 'relations between the Allies in 1945', 'claim': 'the Grand Alliance had already broken down by the end of 1945',
    'stim': ['In February 1945 Roosevelt, Churchill and Stalin met at Yalta in the Crimea.', 'By the time of the Potsdam Conference in July 1945, relations between the Allies had changed.',
             'The USA and the USSR had been allies against Hitler, but by 1946 they were rivals.'],
    'terms': [
        ('Grand Alliance', 'the wartime alliance of Britain, the USA and the USSR against Nazi Germany'),
        ('capitalism', 'an economic system based on private ownership of businesses and free markets'),
        ('communism', 'a system in which the state owns and runs the economy on behalf of the people, under one-party rule'),
        ('Declaration on Liberated Europe', 'the Yalta promise that the peoples of liberated countries could choose their governments in free elections'),
        ('sphere of influence', 'an area where one power has a dominating influence over other countries'),
        ('atomic diplomacy', 'using possession of the atomic bomb to put pressure on another country'),
    ],
    'dates': [('the Yalta Conference took place', 1945, 2), ('President Roosevelt died and Truman took over', 1945, 4), ('Germany surrendered', 1945, 5),
              ('the Potsdam Conference began', 1945, 7), ('an atomic bomb was dropped on Hiroshima', 1945, 8)],
    'mcq': [
        ('Who represented the USA at the Potsdam Conference?', 'Harry Truman', ['Franklin D. Roosevelt', 'Dwight Eisenhower', 'George Marshall'], 'Roosevelt died in April 1945. [1]'),
        ('Which British leader replaced Churchill during the Potsdam Conference?', 'Clement Attlee', ['Anthony Eden', 'Neville Chamberlain', 'Harold Macmillan'], 'Labour won the July 1945 general election. [1]'),
        ('What did Stalin agree to at Yalta?', 'To join the war against Japan three months after Germany\'s defeat', ['To withdraw the Red Army from Germany', 'To give the USA atomic secrets', 'To allow the USA to run Poland'], '[1]'),
        ('What news did Truman give Stalin at Potsdam?', 'That the USA had a powerful new weapon', ['That Roosevelt had resigned', 'That Japan had surrendered', 'That Britain would leave Germany'], 'Truman told Stalin on 24 July 1945; Stalin already knew of it through spies. [1]'),
    ],
    'a': [
        ('What was agreed at the Yalta Conference?', 'agreements made at the Yalta Conference',
         ['Germany would be divided into four zones of occupation, and Berlin too', 'Free elections would be held in the liberated countries of eastern Europe', 'Poland would be in the Soviet sphere of influence, with its border moved west', 'The USSR would join the war against Japan after Germany\'s defeat', 'The United Nations would be set up', 'Nazi war criminals would be tried']),
        ('Describe the disagreements at the Potsdam Conference.', 'disagreements between the Allies at Potsdam',
         ['They disagreed over the new Polish-German border on the Oder-Neisse line', 'They argued over reparations: Stalin wanted large payments, Truman did not want Germany crippled', 'Truman objected to the communist-dominated government in Poland', 'Truman was suspicious of Stalin and less willing to compromise than Roosevelt', 'The atomic bomb increased mistrust']),
    ],
    'b': [
        ('Why did relations between the USA and the USSR worsen in 1945?',
         ['Ideological differences between capitalism and communism resurfaced once Germany was defeated', 'Truman was more suspicious of Stalin than Roosevelt had been', 'The Red Army occupied eastern Europe and Stalin set up friendly governments, as in Poland', 'The US atomic bomb alarmed Stalin and increased mistrust', 'They disagreed about the future of Germany and reparations']),
        ('Why was there agreement at Yalta but disagreement at Potsdam?',
         ['At Yalta they still needed each other to defeat Germany and Japan', 'By Potsdam Germany had surrendered and the common enemy had gone', 'Roosevelt had died and Truman was more hostile to Stalin', 'Stalin had begun to impose communist rule in Poland', 'The USA had the atomic bomb and felt less need to compromise']),
    ],
    'claims': [
        ('At Yalta, Stalin promised free elections in the countries of eastern Europe.', True, 'The Declaration on Liberated Europe promised free elections; disagreement came over how this was carried out.'),
        ('Roosevelt and Churchill both attended the Potsdam Conference throughout.', False, 'Roosevelt had died in April 1945; Truman attended, and Attlee replaced Churchill partway through.'),
        ('The atomic bomb improved trust between the USA and the USSR.', False, 'It increased Stalin\'s suspicion and started an arms race; the USSR tested its own bomb in 1949.'),
    ],
    'c': [
        dict(q='‘The change of American leader from Roosevelt to Truman was the main reason the wartime alliance broke down.’',
             pro=['Truman was more anti-communist and took a tougher line at Potsdam', 'He used the atomic bomb as a source of pressure'],
             con=['Ideological differences between capitalism and communism existed long before 1945', 'Stalin\'s actions in Poland and eastern Europe broke the spirit of Yalta', 'The defeat of Germany removed the common enemy', 'The atomic bomb itself created fear and suspicion'],
             judge='Truman\'s attitude sped up the breakdown, but the deeper causes were ideological differences and Soviet control of eastern Europe, which would have caused tension under any leader'),
        dict(q='How far was the atomic bomb responsible for the breakdown of the wartime alliance?',
             pro=['Truman kept the bomb secret until Potsdam and used it to strengthen the US position', 'Stalin saw it as a threat and started a crash programme to build his own'],
             con=['Disagreements over Poland and Germany began before the bomb was used', 'Ideological hostility existed since 1917', 'Soviet actions in eastern Europe alarmed the West'],
             judge='The bomb increased mistrust and began the arms race, but it added to existing causes rather than being the main one'),
    ],
    'src': [
        S('a photograph of the “Big Three” at Yalta, February 1945 (description)', 'Churchill, Roosevelt and Stalin sit side by side in front of the Livadia Palace, wrapped in coats, with their advisers standing behind them. They appear relaxed and cooperative.',
          'relations between the Allies at Yalta', 'It gives the impression of three leaders working together as allies.',
          'To show the world, and the Allied public, that the Grand Alliance was united as the war neared its end.',
          'a photograph is a direct record of the meeting', 'it was an official photograph posed for publicity, so it shows only the image the leaders wanted to present',
          'The disagreements over Poland, reparations and the future of Germany.', stance=False, why='it suggests the alliance was still working in February 1945', visual=True,
          context='The Allies needed each other to finish the war against Germany and Japan.'),
        S('a remark by Stalin recorded by the Yugoslav communist Milovan Djilas in his book Conversations with Stalin (1962)', 'This war is not as in the past; whoever occupies a territory also imposes on it his own social system. Everyone imposes his own system as far as his army can reach.',
          'Stalin\'s intentions in eastern Europe', 'It suggests Stalin intended to impose communism wherever the Red Army was in control.',
          'Djilas published the book after he had broken with communism, to expose Stalin\'s methods.',
          'Djilas met Stalin in person in 1944-45', 'it was written many years later by a critic of Stalin, from memory',
          'Stalin\'s security fears after two invasions from the west.', stance=True, why='it shows Stalin\'s aims conflicted with the Yalta promise of free elections', kind='primary'),
    ],
})

c6b = T('How the USSR gained control of Eastern Europe by 1948', 'control of eastern europe by 1948', 'salami tactics')
build(c6b, {
    'enq': 'the Soviet takeover of eastern Europe', 'claim': 'Stalin\'s actions in eastern Europe were mainly defensive',
    'stim': ['By 1948 communist governments controlled most of eastern Europe.', 'In March 1946 Winston Churchill warned that an “iron curtain” had descended across Europe.',
             'Stalin claimed that the USSR needed friendly governments on its western border.'],
    'terms': [
        ('salami tactics', 'the method of removing opponents gradually, slice by slice, used by communists to take power in eastern Europe'),
        ('satellite state', 'a country that is formally independent but controlled by a more powerful one'),
        ('Iron Curtain', 'Churchill\'s phrase for the division of Europe between the Soviet-controlled east and the democratic west'),
        ('Cominform', 'the Communist Information Bureau, set up in 1947 to coordinate communist parties under Soviet direction'),
        ('Comecon', 'the Council for Mutual Economic Assistance, set up in 1949 to coordinate the economies of the communist states'),
        ('buffer zone', 'a belt of friendly states protecting the USSR from attack from the west'),
    ],
    'dates': [('Churchill made his “Iron Curtain” speech at Fulton, Missouri', 1946, 3), ('communists won rigged elections in Poland', 1947, 1),
              ('the Cominform was set up', 1947, 9), ('communists seized power in Czechoslovakia', 1948, 2), ('Yugoslavia was expelled from the Cominform', 1948, 6), ('Comecon was set up', 1949, 1)],
    'mcq': [
        ('Which communist leader broke away from Stalin\'s control in 1948?', 'Tito of Yugoslavia', ['Rákosi of Hungary', 'Gottwald of Czechoslovakia', 'Ulbricht of East Germany'], 'Yugoslavia had liberated itself largely without the Red Army. [1]'),
        ('Which was the last country in eastern Europe to fall under communist control in 1948?', 'Czechoslovakia', ['Poland', 'Romania', 'Bulgaria'], 'The communist coup took place in February 1948. [1]'),
        ('Who described the communist method of gaining power as “salami tactics”?', 'Mátyás Rákosi', ['Winston Churchill', 'Harry Truman', 'Josip Tito'], 'Rákosi led the Hungarian communists. [1]'),
        ('Where did Churchill make his “Iron Curtain” speech?', 'Fulton, Missouri, USA', ['London', 'Potsdam', 'Moscow'], 'On 5 March 1946, with Truman present. [1]'),
    ],
    'a': [
        ('Describe how communists gained control of one eastern European country by 1948.', 'methods communists used to gain power in eastern Europe',
         ['Communists joined coalition governments after the war', 'They took control of key ministries such as the interior ministry and the police', 'Opponents were arrested, exiled or frightened into silence', 'Elections were rigged, as in Poland in January 1947', 'Rival parties were forced to merge with the communists, leaving one-party rule']),
        ('Describe the communist takeover of Czechoslovakia in 1948.', 'events of the communist takeover of Czechoslovakia in 1948',
         ['Communists were the largest party after the 1946 elections and Gottwald was Prime Minister', 'In February 1948 non-communist ministers resigned in protest at communist control of the police', 'Communists organised armed workers\' militias and demonstrations', 'President Beneš appointed a communist-dominated government', 'Foreign Minister Jan Masaryk was found dead in March 1948']),
    ],
    'b': [
        ('Why did Stalin want control of eastern Europe?',
         ['The USSR had been invaded through eastern Europe in 1914 and 1941 and wanted a buffer zone', 'About 20 million Soviet people had died in the war and Stalin wanted security', 'He wanted to spread communism', 'He wanted resources and reparations to rebuild the USSR', 'He distrusted the Western powers and their atomic bomb']),
        ('Why did the West see Soviet actions in eastern Europe as a threat?',
         ['Stalin broke the Yalta promise of free elections', 'Communist rule was imposed by force and opponents were persecuted', 'Soviet control seemed to show communist expansion was under way, as Churchill\'s Iron Curtain speech warned', 'Communist parties were strong in western Europe, for example in France and Italy, and in Greece there was a civil war']),
    ],
    'claims': [
        ('All of eastern Europe was under Soviet control by 1948, including Yugoslavia.', False, 'Tito\'s Yugoslavia broke with Stalin and was expelled from the Cominform in 1948.'),
        ('Communists in eastern Europe often first took power as part of coalition governments.', True, 'They then used salami tactics to remove their partners one by one.'),
        ('The Iron Curtain speech was given by President Truman.', False, 'It was given by Winston Churchill in Fulton, Missouri, in March 1946, with Truman in the audience.'),
    ],
    'c': [
        dict(q='‘Stalin\'s actions in eastern Europe after 1945 were mainly defensive.’',
             pro=['The USSR had been invaded through Poland twice in 30 years', 'The scale of Soviet losses made security Stalin\'s priority', 'He had been given a sphere of influence in Poland at Yalta'],
             con=['He imposed communist dictatorships by force, breaking the Yalta promise of free elections', 'Cominform spread Soviet control over communist parties across Europe', 'He took resources and reparations from occupied countries'],
             judge='Stalin\'s motives combined security and the spread of communism; the methods he used made the West see them as aggressive whatever his intentions'),
    ],
    'src': [
        S('a speech by Winston Churchill at Fulton, Missouri, 5 March 1946 (extract)', 'From Stettin in the Baltic to Trieste in the Adriatic, an iron curtain has descended across the Continent.',
          'Western views of Soviet actions in eastern Europe', 'Churchill warns that Europe has been divided and that eastern Europe is now cut off under Soviet control.',
          'To warn the American public of Soviet expansion and encourage a close British-American alliance against it.',
          'Churchill was a respected wartime leader with knowledge of events', 'he was out of office and strongly anti-communist, speaking to persuade the USA to act',
          'Stalin\'s reasons, such as security after invasion.', stance=False, why='it presents Soviet actions as aggressive expansion', context='Truman was present at the speech in Fulton.'),
        S('Stalin\'s response to Churchill\'s Fulton speech, published in the Soviet newspaper Pravda, March 1946 (summary)', 'Stalin said that the USSR had lost far more people than Britain and the USA together in the war, and that it was natural for it to want governments friendly to the USSR in the countries through which Germany had attacked. He compared Churchill to Hitler as a warmonger.',
          'Soviet views of eastern Europe', 'Stalin argues that Soviet control of eastern Europe was a natural defensive response to the war.',
          'To defend Soviet policy and attack Churchill as a warmonger.',
          'it gives Stalin\'s own justification', 'it is propaganda in a state-controlled newspaper and ignores how communists were seizing power',
          'The use of salami tactics and rigged elections, as in Poland in 1947.', stance=True, why='it presents Soviet control as defensive'),
    ],
})

c6c = T('The US reaction: Truman Doctrine and Marshall Plan', 'truman doctrine', 'marshall plan')
build(c6c, {
    'enq': 'the Truman Doctrine and Marshall Plan', 'claim': 'the Marshall Plan was mainly intended to stop the spread of communism',
    'stim': ['In March 1947 President Truman asked Congress for $400 million to help Greece and Turkey.', 'In June 1947 the US Secretary of State George Marshall proposed a European recovery programme.',
             'In 1947 the USA adopted a policy of containment.'],
    'terms': [
        ('containment', 'the US policy of preventing the spread of communism to new countries'),
        ('Truman Doctrine', 'Truman\'s statement of March 1947 that the USA would support free peoples resisting outside pressure or armed minorities'),
        ('Marshall Plan', 'the European Recovery Programme, in which the USA gave about $13 billion of aid to western Europe from 1948'),
        ('Long Telegram', 'the 1946 message from the US diplomat George Kennan arguing that Soviet expansion must be contained'),
        ('dollar imperialism', 'the Soviet description of the Marshall Plan as a way for the USA to control Europe with money'),
        ('Cominform', 'the organisation set up by Stalin in 1947 to coordinate communist parties, partly in response to the Marshall Plan'),
    ],
    'dates': [('Kennan sent the Long Telegram', 1946, 2), ('Britain told the USA it could no longer afford to support Greece', 1947, 2), ('Truman announced the Truman Doctrine', 1947, 3),
              ('Marshall announced his plan in a speech at Harvard University', 1947, 6), ('Congress passed the Marshall Plan', 1948, 4)],
    'mcq': [
        ('Which two countries were the first to receive aid under the Truman Doctrine?', 'Greece and Turkey', ['Poland and Hungary', 'France and Italy', 'Britain and Germany'], '$400 million was approved in 1947. [1]'),
        ('Why did Stalin refuse Marshall Aid for eastern Europe?', 'He believed it was a way for the USA to gain influence over Europe', ['The USA did not offer it to any communist state', 'Eastern Europe did not need help', 'Marshall Aid was only for Asian countries'], 'Molotov walked out of the Paris talks in July 1947. [1]'),
        ('About how much aid did the USA give under the Marshall Plan?', 'About $13 billion', ['About $400 million', 'About $1 billion', 'About $100 billion'], 'From 1948 to 1952. [1]'),
        ('Which eastern European country first showed interest in Marshall Aid before Stalin stopped it?', 'Czechoslovakia', ['Albania', 'Bulgaria', 'East Germany'], '[1]'),
    ],
    'a': [
        ('What was the Truman Doctrine?', 'features of the Truman Doctrine',
         ['It was announced by Truman to Congress in March 1947', 'It said the USA would support free peoples resisting armed minorities or outside pressure', 'It was prompted by Britain\'s withdrawal of support for the Greek government against communist rebels', '$400 million of aid went to Greece and Turkey', 'It marked the start of containment and the end of US isolation from Europe']),
        ('Describe the Marshall Plan.', 'features of the Marshall Plan',
         ['It was proposed by George Marshall in June 1947', 'It offered economic aid to help Europe recover from the war', 'About $13 billion was given between 1948 and 1952', '16 countries took part initially, with Britain, France and West Germany receiving the largest shares', 'Stalin refused aid for the USSR and its satellites']),
    ],
    'b': [
        ('Why did the USA introduce the Marshall Plan?',
         ['Europe\'s economy was devastated and people faced hunger and unemployment', 'Poverty could make communism attractive, as in Italy and France where communist parties were strong', 'A prosperous Europe would buy American goods and help the US economy', 'It would strengthen the policy of containment begun with the Truman Doctrine']),
        ('Why did Stalin see the Truman Doctrine and Marshall Plan as a threat?',
         ['He saw them as an attempt to build an anti-Soviet bloc in Europe', 'Marshall Aid could draw eastern European countries away from Soviet control', 'He called it “dollar imperialism”, a way to make Europe dependent on the USA', 'It led him to set up Cominform (1947) and later Comecon (1949) to tighten control']),
    ],
    'claims': [
        ('The Marshall Plan was offered only to countries in western Europe.', False, 'Aid was offered to all of Europe, including the USSR, but Stalin refused it and stopped his satellites accepting.'),
        ('The Truman Doctrine was a response to events in Greece and Turkey.', True, 'Britain could no longer afford to support the Greek government against communist rebels.'),
        ('The Marshall Plan was mainly military aid.', False, 'It was economic aid for recovery: food, machinery, fuel and loans.'),
    ],
    'c': [
        dict(q='‘The Marshall Plan was intended mainly to stop the spread of communism.’',
             pro=['It followed the Truman Doctrine and was part of containment', 'Poverty made communism attractive in countries such as France and Italy', 'It helped bind western Europe to the USA'],
             con=['It was a genuine humanitarian response to hunger and devastation', 'It served US economic interests by creating markets for American goods', 'It was offered to all of Europe, including the USSR'],
             judge='Humanitarian and economic motives were real, but the plan\'s timing and purpose show that containing communism was its main strategic aim'),
        dict(q='How far did the Truman Doctrine and Marshall Plan make the Cold War worse?',
             pro=['They divided Europe into two economic and political blocs', 'Stalin responded with Cominform and Comecon', 'They led to the currency reform in Germany that triggered the Berlin Blockade'],
             con=['Soviet actions in eastern Europe had already created tension', 'They were a response to communist pressure in Greece and Turkey', 'They brought stability and recovery to western Europe'],
             judge='They hardened the division of Europe, but they were a response to tension that already existed rather than its cause'),
    ],
    'src': [
        S('President Truman\'s speech to the US Congress, 12 March 1947 (extract)', 'I believe that it must be the policy of the United States to support free peoples who are resisting attempted subjugation by armed minorities or by outside pressures.',
          'the Truman Doctrine', 'Truman says the USA will support countries resisting communist takeover, whether by rebels or from outside.',
          'To persuade Congress to approve $400 million of aid to Greece and Turkey and to commit the USA to containment.',
          'it is Truman\'s own public statement of his policy', 'it was intended to persuade Congress, so it presents the issue as a simple choice between freedom and oppression',
          'That the immediate cause was Britain\'s withdrawal from Greece.', stance=True, why='it shows US policy was aimed at stopping communism'),
        S('a speech by George Marshall at Harvard University, 5 June 1947 (extract)', 'Our policy is directed not against any country or doctrine but against hunger, poverty, desperation and chaos.',
          'the aims of the Marshall Plan', 'Marshall claims the aid is humanitarian and not directed against communism or the USSR.',
          'To win support for aid in the USA and in Europe, and to make the offer acceptable to all European countries.',
          'it is the official announcement of the plan by its author', 'Marshall needed to present the plan positively; it does not reveal the strategic aims discussed in private',
          'That the plan followed the Truman Doctrine and was seen by Stalin as “dollar imperialism”.', stance=False, why='Marshall presents the plan as humanitarian, not anti-communist'),
        S('a Soviet cartoon of the kind published in the magazine Krokodil, c. 1949 (illustrative description)', 'An American figure is shown handing out dollars to European leaders who are tied to him with strings, like puppets.',
          'Soviet views of the Marshall Plan', 'The cartoonist suggests Marshall Aid was a way for the USA to control European countries.',
          'To persuade Soviet readers that American aid was a form of imperialism.',
          'it shows the official Soviet view', 'it is propaganda from a state-controlled magazine',
          'That western European economies recovered rapidly with the aid.', stance=True, why='it suggests the plan was a political weapon in the Cold War', visual=True),
    ],
})

c6d = T('The Berlin Blockade and airlift and their consequences', 'berlin blockade', 'airlift')
build(c6d, {
    'enq': 'the Berlin Blockade', 'claim': 'the Berlin Blockade was a victory for the West',
    'stim': ['In June 1948 Stalin cut all road, rail and canal links between the western zones of Germany and West Berlin.', 'For almost a year West Berlin was supplied entirely by air.',
             'Berlin lay deep inside the Soviet zone of Germany.'],
    'terms': [
        ('Berlin Blockade', 'the Soviet closing of land and water routes to West Berlin from June 1948 to May 1949'),
        ('Berlin Airlift', 'the operation in which American and British aircraft flew supplies into West Berlin during the blockade'),
        ('Bizonia', 'the combined British and American zones of Germany from January 1947'),
        ('Deutschmark', 'the new currency introduced in the western zones of Germany in June 1948'),
        ('NATO', 'the North Atlantic Treaty Organization, the Western military alliance formed in April 1949'),
        ('FRG', 'the Federal Republic of Germany (West Germany), set up in May 1949'),
        ('GDR', 'the German Democratic Republic (East Germany), set up in October 1949'),
    ],
    'dates': [('the British and American zones were joined as Bizonia', 1947, 1), ('the Deutschmark was introduced in the western zones', 1948, 6.2),
              ('Stalin began the Berlin Blockade', 1948, 6.24), ('NATO was formed', 1949, 4), ('the blockade was lifted', 1949, 5.12), ('the Federal Republic of Germany was set up', 1949, 5.23), ('the German Democratic Republic was set up', 1949, 10)],
    'mcq': [
        ('What was the immediate trigger for the Berlin Blockade?', 'The introduction of a new currency in the western zones', ['The formation of NATO', 'The building of the Berlin Wall', 'The death of Stalin'], 'The Deutschmark was introduced in June 1948. [1]'),
        ('How long did the Berlin Blockade last?', 'About 11 months', ['About 11 days', 'About 3 years', 'About 6 weeks'], 'From 24 June 1948 to 12 May 1949. [1]'),
        ('Why did Stalin not shoot down the airlift planes?', 'It would have been an act of war against the USA and Britain', ['He did not have any aircraft', 'The UN had banned it', 'The planes were flying over France'], '[1]'),
        ('Which organisation was formed in April 1949 partly as a result of the blockade?', 'NATO', ['The Warsaw Pact', 'Comecon', 'The United Nations'], '[1]'),
    ],
    'a': [
        ('Describe the Berlin Airlift.', 'features of the Berlin Airlift',
         ['American and British planes flew food, fuel and supplies into West Berlin', 'It began in June 1948 and continued until September 1949', 'At its peak a plane landed every few minutes', 'Over two million tonnes of supplies were delivered', 'Stalin lifted the blockade in May 1949 after it failed']),
        ('What were the consequences of the Berlin Blockade?', 'consequences of the Berlin Blockade',
         ['Germany was divided into two states, the FRG and the GDR, in 1949', 'NATO was formed in April 1949, committing the USA to the defence of western Europe', 'Berlin became a symbol of the Cold War', 'The USSR later formed the Warsaw Pact (1955)', 'Relations between the superpowers were worse than ever']),
    ],
    'b': [
        ('Why did Stalin blockade West Berlin in 1948?',
         ['He feared a strong, united West Germany allied to the USA', 'The new currency in the western zones threatened the economy of the Soviet zone', 'West Berlin was a showcase of Western prosperity inside the Soviet zone', 'He hoped to force the West to leave Berlin or abandon its plans for West Germany']),
        ('Why did the Berlin Blockade fail?',
         ['The airlift kept West Berlin supplied', 'Stalin would not risk war by shooting down planes', 'West Berliners refused to accept Soviet offers of food in the east', 'The West showed it would not give up Berlin, and the blockade became a propaganda defeat for Stalin']),
    ],
    'claims': [
        ('The Berlin Blockade ended when the West agreed to leave Berlin.', False, 'Stalin lifted the blockade in May 1949; the Western powers stayed in West Berlin.'),
        ('The Berlin Blockade led directly to the formation of NATO.', True, 'NATO was formed in April 1949, while the blockade was still going on.'),
        ('Soviet planes shot down many airlift aircraft.', False, 'Stalin did not shoot them down because that would have meant war; accidents did cause deaths.'),
    ],
    'c': [
        dict(q='‘The Berlin Blockade was a victory for the West.’',
             pro=['The airlift kept West Berlin free and the blockade was lifted', 'It was a propaganda triumph showing Western determination', 'NATO was formed and West Germany was created as an ally'],
             con=['Germany was divided, which the USSR could accept as the price of security', 'The airlift was very expensive', 'It began a more dangerous era of military alliances and confrontation'],
             judge='It was a clear victory for the West over Berlin itself, but it also hardened the division of Germany and Europe'),
        dict(q='How far was the Berlin Blockade caused by the actions of the Western powers?',
             pro=['The West merged its zones and introduced a new currency without Soviet agreement', 'Marshall Aid was building up West Germany against Soviet wishes'],
             con=['Stalin chose to blockade a city of two million people', 'Stalin wanted to force the West out of Berlin', 'Disagreements over reparations and Germany had existed since Potsdam'],
             judge='The West\'s policies in Germany provoked Stalin, but the blockade was his decision and aimed to force the West out'),
    ],
    'src': [
        S('a photograph taken in West Berlin in 1948 (description)', 'A crowd of Berliners stands on a pile of rubble near Tempelhof airport, watching an American transport plane flying low overhead as it comes in to land.',
          'the Berlin Airlift', 'It suggests Berliners welcomed the airlift and depended on it.',
          'To record and publicise the success of the airlift.',
          'it is a photograph taken at the time in West Berlin', 'photographs like this were widely used as Western propaganda, and it shows only one moment',
          'The scale of the airlift, or that Soviet offers of food in the east were mostly refused.', stance=True, why='it shows the airlift succeeding with Berliners\' support', visual=True,
          context='The airlift began in late June 1948.'),
        S('a Soviet statement on the blockade, 1948 (summary)', 'The Soviet authorities claimed that the routes had been closed for “technical difficulties” and that the Western powers had broken the Potsdam agreements by introducing a separate currency.',
          'the Soviet justification for the blockade', 'It presents the blockade as a reaction to Western breaches of agreements rather than an aggressive act.',
          'To justify the blockade to Germans and to the world.',
          'it shows the Soviet position', 'it is propaganda: the “technical difficulties” were an obvious excuse',
          'That Stalin\'s aim was to force the West out of Berlin.', stance=False, why='it presents the Western powers as responsible for the crisis'),
    ],
})

c6e = T('Who was more to blame for the Cold War? Traditional and revisionist views', 'traditional and revisionist', 'who was more to blame')
build(c6e, {
    'enq': 'responsibility for the Cold War', 'claim': 'the USSR was more to blame than the USA for the Cold War',
    'stim': ['Historians have disagreed about who was to blame for the Cold War.', 'Traditional, revisionist and post-revisionist historians interpret the start of the Cold War differently.'],
    'terms': [
        ('traditional (orthodox) view', 'the interpretation, common in the West in the 1950s, that Soviet expansion was mainly to blame for the Cold War'),
        ('revisionist view', 'the interpretation, popular from the 1960s, that US economic and political expansion was mainly to blame'),
        ('post-revisionist view', 'the interpretation that both sides shared responsibility through mutual suspicion and misunderstanding'),
        ('interpretation', 'a historian\'s explanation or judgement about the past, based on evidence'),
        ('Cold War', 'a state of hostility between the superpowers without direct fighting between them'),
    ],
    'dates': [('Churchill made the Iron Curtain speech', 1946), ('the Truman Doctrine was announced', 1947), ('the Berlin Blockade began', 1948), ('the USSR tested its first atomic bomb', 1949), ('the USSR collapsed and its archives began to open', 1991)],
    'mcq': [
        ('Which view of the Cold War argues that Stalin\'s expansion in eastern Europe was the main cause?', 'The traditional (orthodox) view', ['The revisionist view', 'The post-revisionist view', 'The Soviet view'], '[1]'),
        ('Why did revisionist interpretations become popular in the USA in the 1960s?', 'The Vietnam War made many Americans question US foreign policy', ['Soviet archives became available', 'The USSR had collapsed', 'Stalin was still alive'], '[1]'),
        ('Which development after 1991 influenced historians\' views of the Cold War?', 'The opening of Soviet archives', ['The discovery of the atomic bomb', 'The Truman Doctrine', 'The end of the Korean War'], '[1]'),
    ],
    'a': [
        ('Describe the traditional view of the origins of the Cold War.', 'features of the traditional view of the origins of the Cold War',
         ['It blames the USSR for the Cold War', 'Stalin broke the Yalta promise of free elections', 'Communism was seen as aggressive and expansionist', 'The USA was seen as responding defensively with containment', 'It was popular in the West in the late 1940s and 1950s']),
        ('Describe the revisionist view of the origins of the Cold War.', 'features of the revisionist view of the origins of the Cold War',
         ['It blames the USA for the Cold War', 'The USA wanted to spread capitalism and open markets for its goods', 'The atomic bomb was used to intimidate the USSR', 'Soviet actions were seen as defensive after the losses of the war', 'It became popular in the 1960s during the Vietnam War']),
    ],
    'b': [
        ('Why have historians disagreed about who was to blame for the Cold War?',
         ['They wrote at different times and were influenced by events such as the Vietnam War', 'Evidence changed: Soviet archives only opened after 1991', 'They come from different countries and political viewpoints', 'They focus on different events, such as Yalta, the atomic bomb or Marshall Aid']),
        ('Why can the USA be blamed for the Cold War?',
         ['The atomic bomb and atomic diplomacy alarmed Stalin', 'The Truman Doctrine divided the world into two camps', 'The Marshall Plan was seen as dollar imperialism', 'Western actions in Germany, such as the new currency, provoked the Berlin Blockade']),
        ('Why can the USSR be blamed for the Cold War?',
         ['Stalin broke the Yalta promise of free elections in eastern Europe', 'Communists used salami tactics to seize power', 'The Berlin Blockade threatened two million people', 'Stalin supported communist movements outside his sphere, as in Czechoslovakia']),
    ],
    'claims': [
        ('Revisionist historians blamed the USSR for the Cold War.', False, 'Revisionists blamed the USA; the traditional view blamed the USSR.'),
        ('Post-revisionist historians argue that both sides contributed to the Cold War.', True, 'They stress mutual suspicion and misunderstanding.'),
        ('Historians\' interpretations of the Cold War have not changed since 1950.', False, 'They have changed with new evidence, such as Soviet archives after 1991, and with events such as Vietnam.'),
    ],
    'c': [
        dict(q='‘The USSR was more to blame than the USA for the start of the Cold War.’',
             pro=['Stalin broke the Yalta promise of free elections', 'Communist takeovers used force and fraud', 'The Berlin Blockade was an aggressive act'],
             con=['US atomic diplomacy alarmed Stalin', 'The Truman Doctrine and Marshall Plan divided Europe', 'Soviet actions can be seen as defensive after enormous wartime losses', 'Mutual suspicion and ideology meant both sides misread each other'],
             judge='Both sides were responsible, but Stalin\'s imposition of communist rule in eastern Europe was the action that turned rivalry into Cold War'),
    ],
    'src': [
        S('an extract from a book by an American historian writing in the 1950s (illustrative of the traditional view)', 'The Cold War was the result of Soviet expansion. Stalin broke every promise made at Yalta and the United States had no choice but to resist.',
          'the origins of the Cold War', 'It blames the USSR entirely and presents the USA as acting defensively.',
          'To explain the Cold War to an American readership at the height of the conflict.',
          'it reflects evidence available in the West at the time', 'it was written in the 1950s, when anti-communism was strong in the USA, and without access to Soviet records',
          'The effect on Stalin of the atomic bomb and the Marshall Plan.', stance=True, why='it puts the blame on the USSR', kind='secondary', published=True),
        S('an extract from a book by an American historian writing in the late 1960s (illustrative of the revisionist view)', 'American leaders wanted an open world for American trade and investment. They saw Soviet security needs in eastern Europe as aggression and used their atomic monopoly to try to force Stalin to give way.',
          'the origins of the Cold War', 'It blames the USA for pursuing its economic interests and pressuring the USSR.',
          'To challenge the traditional view, at a time when the Vietnam War had made many Americans critical of US policy.',
          'it considers the Soviet point of view', 'it may be influenced by opposition to the Vietnam War',
          'Soviet use of force and rigged elections in eastern Europe.', stance=False, why='it puts the blame on the USA', kind='secondary', published=True),
        S('an extract from a book by a historian writing in the 1990s (illustrative of the post-revisionist view)', 'Neither side wanted a Cold War, but each saw the other\'s defensive steps as aggression. The new Soviet archives show Stalin was cautious but deeply suspicious; American leaders were equally convinced that only firmness would work.',
          'the origins of the Cold War', 'It argues both sides contributed through mutual suspicion and misunderstanding.',
          'To offer a balanced interpretation using newly available evidence.',
          'it uses Soviet archives opened after 1991', 'it is still one interpretation and some historians using the same archives blame Stalin more',
          'Specific events such as the Berlin Blockade.', stance=False, why='it argues blame was shared rather than mainly Soviet', kind='secondary', published=True),
    ],
})

CHAPTERS[6] = [c6a, c6b, c6c, c6d, c6e]


# ============================================================== CHAPTER 7: How effectively did the USA contain the spread of communism?

c7a = T('The Korean War, 1950-53', 'korean war')
build(c7a, {
    'enq': 'the Korean War', 'claim': 'the Korean War was a success for containment',
    'stim': ['On 25 June 1950 North Korean forces crossed the 38th parallel into South Korea.', 'The Korean War was the first major conflict of the Cold War.',
             'In 1949 China had become communist under Mao Zedong.'],
    'terms': [
        ('38th parallel', 'the line of latitude dividing North and South Korea after 1945'),
        ('domino theory', 'the belief that if one country fell to communism, its neighbours would follow'),
        ('NSC-68', 'the 1950 US report that recommended a large military build-up to contain communism'),
        ('Inchon landings', 'the UN amphibious attack behind North Korean lines in September 1950'),
        ('armistice', 'the 1953 ceasefire agreement signed at Panmunjom that ended the fighting in Korea'),
        ('limited war', 'a war fought for restricted aims without using all available weapons, such as nuclear bombs'),
    ],
    'dates': [('China became a communist state', 1949, 10), ('North Korea invaded South Korea', 1950, 6), ('UN forces landed at Inchon', 1950, 9), ('Chinese forces entered the war', 1950, 10.25),
              ('Truman dismissed General MacArthur', 1951, 4), ('the Korean armistice was signed', 1953, 7)],
    'mcq': [
        ('Why was the USSR unable to veto UN action in Korea in June 1950?', 'It was boycotting the Security Council over the UN\'s refusal to seat communist China', ['It had left the UN in 1949', 'It supported UN action', 'It did not have a veto'], '[1]'),
        ('Who commanded the UN forces in Korea until April 1951?', 'General Douglas MacArthur', ['General Dwight Eisenhower', 'General George Patton', 'General Matthew Ridgway'], 'He was dismissed by Truman after publicly calling for war on China. [1]'),
        ('Where was the border between North and South Korea after the 1953 armistice?', 'Close to the 38th parallel', ['At the Yalu River', 'At the Pusan perimeter', 'At the 17th parallel'], 'The 17th parallel divided Vietnam. [1]'),
        ('Which leader ruled North Korea at the time of the invasion?', 'Kim Il Sung', ['Syngman Rhee', 'Mao Zedong', 'Ho Chi Minh'], 'Syngman Rhee led South Korea. [1]'),
    ],
    'a': [
        ('Describe the main events of the Korean War from 1950 to 1953.', 'stages of the Korean War',
         ['North Korea invaded in June 1950 and pushed UN and South Korean forces back to Pusan', 'UN forces landed at Inchon in September 1950 and drove the North Koreans back', 'UN forces crossed the 38th parallel and advanced towards the Yalu River', 'China entered the war in October-November 1950 and pushed UN forces back south', 'The war became a stalemate near the 38th parallel until the armistice of July 1953']),
        ('Describe the role of the United Nations in the Korean War.', 'ways the United Nations was involved in the Korean War',
         ['The Security Council condemned the invasion and called on members to help South Korea', 'The USSR could not veto this because it was boycotting the Council', 'Sixteen countries sent troops, though most were American', 'The UN force was commanded by the American General MacArthur']),
    ],
    'b': [
        ('Why did the USA become involved in the Korean War?',
         ['Truman believed in containment and the domino theory', 'China had become communist in 1949 and the USA feared communism spreading across Asia', 'The USSR had tested an atomic bomb in 1949 and NSC-68 called for a stronger response', 'Truman faced criticism at home for “losing” China and needed to appear strong', 'A communist South Korea would threaten Japan']),
        ('Why did Truman dismiss MacArthur in 1951?',
         ['MacArthur wanted to attack China, possibly with atomic weapons', 'He publicly criticised Truman\'s policy of limited war', 'Truman feared escalation into a world war with China and the USSR', 'MacArthur had underestimated the risk of Chinese intervention, leading to the retreat of late 1950']),
    ],
    'claims': [
        ('The USA fought in Korea without UN approval.', False, 'The UN Security Council authorised action; the USSR was boycotting the Council at the time.'),
        ('At the end of the Korean War the border was close to where it had been in 1950.', True, 'The armistice line was near the 38th parallel.'),
        ('MacArthur was dismissed for refusing to attack China.', False, 'He was dismissed because he wanted to widen the war against China and publicly challenged Truman.'),
    ],
    'c': [
        dict(q='‘The Korean War was a success for the USA\'s policy of containment.’',
             pro=['South Korea remained non-communist', 'The UN, led by the USA, showed aggression would be resisted', 'The USA rearmed and strengthened alliances such as SEATO (1954)'],
             con=['The attempt to “roll back” communism in North Korea failed after China intervened', 'Millions died and Korea was devastated', 'Communist China emerged stronger and Korea stayed divided'],
             judge='The war succeeded in its original aim of containing communism in North Korea, but failed when the USA tried to go further'),
        dict(q='How far was the USA responsible for the Korean War becoming a wider conflict?',
             pro=['UN forces crossed the 38th parallel and advanced to China\'s border at the Yalu', 'MacArthur ignored Chinese warnings'],
             con=['North Korea began the war with Soviet approval', 'China chose to send hundreds of thousands of troops', 'Truman kept the war limited by refusing to use atomic bombs or attack China'],
             judge='The decision to advance to the Yalu brought China in, but the USA also took steps to keep the war from spreading further'),
    ],
    'src': [
        S('a statement by President Truman, 27 June 1950 (summary)', 'Truman announced that he had ordered US air and sea forces to support South Korea, saying that the attack showed communism had moved beyond subversion to the use of armed invasion and war.',
          'US reasons for intervening in Korea', 'Truman presents the invasion as communist aggression that had to be resisted.',
          'To explain and justify US intervention to the American public and the world.',
          'it is the President\'s own explanation at the time', 'it presents a simple picture of aggression and does not mention US political pressures at home',
          'That the UN had approved action because the USSR was boycotting the Security Council.', stance=True, why='it shows the USA intervened to contain communism'),
        S('an extract from a modern history textbook (illustrative)', 'The armistice of 1953 left Korea divided almost exactly where it had been in 1950. Over three million people may have died to restore the border.',
          'the outcome of the Korean War', 'It suggests the war achieved little at enormous human cost.',
          'To inform students about the results of the war.',
          'it is written with hindsight and its account of the border is accurate', 'it focuses on the costs and does not discuss what the USA saw as the success of containment',
          'That South Korea remained independent and later prospered.', stance=False, why='it emphasises the costs and limited results', kind='secondary', published=True),
    ],
})

c7b = T('The Cuban Missile Crisis, 1962', 'cuban missile crisis')
build(c7b, {
    'enq': 'the Cuban Missile Crisis', 'claim': 'Kennedy won the Cuban Missile Crisis',
    'stim': ['In October 1962 an American U-2 spy plane photographed Soviet missile sites under construction in Cuba.', 'For thirteen days in October 1962 the world seemed close to nuclear war.',
             'In January 1959 Fidel Castro took power in Cuba.'],
    'terms': [
        ('Bay of Pigs', 'the failed invasion of Cuba by CIA-trained Cuban exiles in April 1961'),
        ('quarantine', 'Kennedy\'s word for the naval blockade of Cuba, chosen because a blockade is an act of war'),
        ('ExComm', 'the Executive Committee of the National Security Council that advised Kennedy during the crisis'),
        ('U-2', 'the American high-altitude spy plane that photographed the missile sites'),
        ('brinkmanship', 'pushing a crisis to the edge of war to make the other side back down'),
        ('hotline', 'the direct communication link between Washington and Moscow set up in 1963'),
        ('Jupiter missiles', 'American nuclear missiles based in Turkey that the USSR wanted removed'),
    ],
    'dates': [('Fidel Castro took power in Cuba', 1959), ('the Bay of Pigs invasion failed', 1961), ('U-2 photographs revealed missile sites in Cuba', 1962), ('the hotline between Washington and Moscow was set up', 1963),
              ('Khrushchev was removed from power in the USSR', 1964)],
    'mcq': [
        ('What did Kennedy announce on 22 October 1962?', 'A naval quarantine (blockade) of Cuba', ['An air strike on Cuba', 'An invasion of Cuba', 'The removal of US missiles from Turkey'], 'He also demanded the removal of the missiles. [1]'),
        ('What did Khrushchev demand in his second letter of 27 October 1962?', 'The removal of US missiles from Turkey', ['The removal of US troops from Berlin', 'Membership of NATO', 'The return of Alaska'], 'Kennedy replied publicly to the first letter. [1]'),
        ('What happened on 27 October 1962 that increased tension?', 'An American U-2 plane was shot down over Cuba', ['A Soviet ship sank a US destroyer', 'The USA invaded Cuba', 'Castro was assassinated'], 'Major Rudolf Anderson was killed. [1]'),
        ('Which of these was an outcome of the Cuban Missile Crisis?', 'A telephone hotline between Washington and Moscow', ['The Berlin Wall was pulled down', 'Castro was overthrown', 'Cuba joined NATO'], 'Set up in 1963 to prevent misunderstandings. [1]'),
    ],
    'a': [
        ('Describe the events of the Cuban Missile Crisis from 14 to 28 October 1962.', 'events of the Cuban Missile Crisis in October 1962',
         ['A U-2 plane photographed missile sites in Cuba on 14 October', 'Kennedy and ExComm discussed options including an air strike and invasion', 'On 22 October Kennedy announced a naval quarantine of Cuba', 'Soviet ships carrying missiles turned back on 24 October', 'Khrushchev sent two letters on 26 and 27 October and a U-2 was shot down', 'On 28 October Khrushchev agreed to remove the missiles']),
        ('Describe the consequences of the Cuban Missile Crisis.', 'consequences of the Cuban Missile Crisis',
         ['The Soviet missiles were removed from Cuba', 'The USA secretly removed its Jupiter missiles from Turkey', 'A hotline was set up between Washington and Moscow in 1963', 'The Partial Test Ban Treaty was signed in 1963', 'Castro remained in power and Cuba stayed communist', 'Khrushchev\'s reputation was damaged and he was removed in 1964']),
    ],
    'b': [
        ('Why did Khrushchev place nuclear missiles on Cuba?',
         ['To protect Cuba, a communist ally, from another US invasion after the Bay of Pigs', 'To close the missile gap: the USA had far more long-range missiles', 'To respond to US Jupiter missiles in Turkey', 'To test Kennedy, whom he thought weak after the Bay of Pigs and the Vienna summit', 'To gain a bargaining position, possibly over Berlin']),
        ('Why did Kennedy choose a quarantine rather than an air strike?',
         ['An air strike might not destroy all the missiles', 'Attacking Cuba could kill Soviet personnel and lead to nuclear war', 'A quarantine gave Khrushchev time to back down', 'It showed firmness while leaving room for negotiation']),
        ('Why was the Cuban Missile Crisis resolved without war?',
         ['Both leaders realised the danger of nuclear war', 'Kennedy chose a quarantine rather than an attack', 'Khrushchev accepted a deal: no US invasion of Cuba and, secretly, removal of the Jupiter missiles', 'Back-channel talks, such as Robert Kennedy\'s meeting with the Soviet ambassador, allowed compromise']),
    ],
    'claims': [
        ('The removal of the American missiles from Turkey was announced publicly as part of the deal in 1962.', False, 'It was kept secret; the Jupiters were removed quietly in 1963, which made Kennedy look like the winner.'),
        ('The Cuban Missile Crisis led to the setting up of a hotline between Washington and Moscow.', True, 'It was set up in 1963 so the leaders could communicate directly.'),
        ('The Bay of Pigs invasion succeeded in overthrowing Castro.', False, 'It failed within days in April 1961 and pushed Castro closer to the USSR.'),
    ],
    'c': [
        dict(q='‘Kennedy won the Cuban Missile Crisis.’',
             pro=['The Soviet missiles were removed from Cuba', 'Kennedy appeared firm and his reputation rose', 'Khrushchev was humiliated and removed from power in 1964'],
             con=['Khrushchev gained a promise that the USA would not invade Cuba, so Castro survived', 'The US Jupiter missiles were removed from Turkey', 'Both sides gained from the hotline and the Test Ban Treaty'],
             judge='Kennedy appeared to win because the deal on Turkey was secret, but Khrushchev gained important concessions; in reality both sides gained by avoiding war'),
        dict(q='How far was the Cuban Missile Crisis a success for containment?',
             pro=['Soviet missiles were removed from the western hemisphere', 'The USA showed it would stand firm against Soviet expansion'],
             con=['Cuba remained a communist state close to the USA', 'The USA had to promise not to invade Cuba', 'Containment had already failed in Cuba in 1959-61 with Castro\'s turn to the USSR'],
             judge='The crisis contained the nuclear threat, but it confirmed rather than reversed communism in Cuba'),
    ],
    'src': [
        S('President Kennedy\'s television broadcast to the American people, 22 October 1962 (extract)', 'It shall be the policy of this Nation to regard any nuclear missile launched from Cuba against any nation in the Western Hemisphere as an attack by the Soviet Union on the United States, requiring a full retaliatory response upon the Soviet Union.',
          'Kennedy\'s response to the missiles', 'Kennedy warns that any missile launched from Cuba would be treated as a Soviet attack and answered with full retaliation.',
          'To inform Americans of the crisis, warn the USSR of the consequences and show US determination.',
          'it is Kennedy\'s own public statement at the time', 'it was intended to put pressure on Khrushchev and reassure Americans, so it does not reveal private discussions about compromise',
          'That Kennedy was secretly prepared to remove the missiles from Turkey.', stance=True, why='it shows Kennedy taking a firm stand that forced Khrushchev to back down'),
        S('a cartoon by Leslie Illingworth published in the British newspaper the Daily Mail, 29 October 1962', 'Khrushchev and Kennedy are arm-wrestling, each sitting on a nuclear bomb, with their fingers on the detonator buttons. Khrushchev says: “OK Mr President, let\'s talk.”',
          'the end of the Cuban Missile Crisis', 'The cartoonist suggests both leaders were equally responsible for bringing the world close to destruction, and that they had to negotiate.',
          'To comment on the outcome of the crisis, the day after Khrushchev agreed to remove the missiles.',
          'it was published at the time by a British cartoonist, so it is not American or Soviet propaganda', 'it is satirical and simplifies events',
          'The details of the deal, such as the secret removal of the Jupiter missiles.', stance=False, why='it presents the two leaders as equals rather than suggesting Kennedy won', visual=True,
          context='Khrushchev agreed on 28 October 1962 to remove the missiles.'),
    ],
})

US_VN = [(1964, 23300), (1965, 184300), (1966, 385300), (1967, 485600), (1968, 536100), (1969, 475200), (1970, 334600), (1971, 156800), (1972, 24200)]

c7c = T('US involvement in Vietnam: escalation and tactics', 'vietnam', 'escalation and tactics')
build(c7c, {
    'enq': 'US involvement in Vietnam', 'claim': 'US tactics in Vietnam were bound to fail',
    'stim': ['In 1954 the Geneva Agreements divided Vietnam at the 17th parallel.', 'In August 1964 Congress passed the Gulf of Tonkin Resolution.',
             'By the end of 1968 there were over half a million American troops in Vietnam.'],
    'terms': [
        ('Viet Cong', 'the communist guerrilla fighters in South Vietnam, supported by North Vietnam'),
        ('Ho Chi Minh Trail', 'the network of jungle paths through Laos and Cambodia used to supply the Viet Cong'),
        ('Gulf of Tonkin Resolution', 'the 1964 vote by Congress giving President Johnson power to take military action in Vietnam'),
        ('Operation Rolling Thunder', 'the US bombing campaign against North Vietnam from 1965 to 1968'),
        ('search and destroy', 'US missions to find and kill Viet Cong fighters in villages and the countryside'),
        ('Agent Orange', 'a chemical sprayed by US forces to destroy jungle cover and crops'),
        ('guerrilla warfare', 'fighting in small groups using surprise attacks, ambushes and booby traps rather than open battle'),
    ],
    'dates': [('the French were defeated at Dien Bien Phu', 1954, 5), ('the Geneva Agreements divided Vietnam', 1954, 7), ('the Gulf of Tonkin incident led to a resolution in Congress', 1964),
              ('Operation Rolling Thunder began', 1965, 3), ('the Tet Offensive began', 1968, 1), ('US troops massacred villagers at My Lai', 1968, 3)],
    'mcq': [
        ('At which line of latitude was Vietnam divided in 1954?', 'The 17th parallel', ['The 38th parallel', 'The 49th parallel', 'The Equator'], 'Elections to reunite the country, due in 1956, were never held. [1]'),
        ('Which US President sent the first combat troops to Vietnam in 1965?', 'Lyndon B. Johnson', ['John F. Kennedy', 'Richard Nixon', 'Dwight Eisenhower'], 'Marines landed at Da Nang in March 1965. [1]'),
        ('What was the main purpose of Agent Orange?', 'To destroy jungle cover and crops used by the Viet Cong', ['To set villages on fire', 'To purify drinking water', 'To mark landing zones for helicopters'], 'It also caused long-term health problems. [1]'),
        ('Which of these was a Viet Cong tactic?', 'Using underground tunnel networks to hide and launch surprise attacks', ['Large tank battles in open country', 'Strategic bombing of US cities', 'Naval blockades of US ports'], 'For example the Cu Chi tunnels. [1]'),
    ],
    'a': [
        ('Describe the tactics used by the Viet Cong.', 'tactics used by the Viet Cong',
         ['They used guerrilla warfare, attacking in small groups and then disappearing', 'They used booby traps and mines', 'They hid in tunnel networks such as those at Cu Chi', 'They mixed with villagers, making them hard to identify', 'They were supplied along the Ho Chi Minh Trail']),
        ('Describe the tactics used by US forces in Vietnam.', 'tactics used by US forces in Vietnam',
         ['Bombing of North Vietnam in Operation Rolling Thunder', 'Search and destroy missions against villages', 'Chemical weapons such as Agent Orange and napalm', 'Helicopters to move troops quickly', 'Strategic hamlets to separate villagers from the Viet Cong']),
        ('Describe how US involvement in Vietnam increased between 1954 and 1965.', 'stages in the escalation of US involvement in Vietnam',
         ['The USA supported Ngo Dinh Diem\'s government in South Vietnam after 1954', 'Eisenhower sent money and military advisers', 'Kennedy increased the number of advisers to about 16,000 by 1963', 'After the Gulf of Tonkin incident in 1964 Congress gave Johnson power to act', 'In 1965 Johnson began Operation Rolling Thunder and sent combat troops']),
    ],
    'b': [
        ('Why did the USA become involved in Vietnam?',
         ['US leaders believed in the domino theory and feared communism would spread across South-East Asia', 'The policy of containment committed the USA to resisting communism', 'After the French defeat in 1954 the USA saw itself as the defender of South Vietnam', 'The Gulf of Tonkin incident in 1964 gave Johnson a reason to escalate']),
        ('Why did US tactics fail to defeat the Viet Cong?',
         ['The Viet Cong used guerrilla tactics and knew the land', 'Search and destroy and chemical weapons killed civilians and turned villagers against the USA', 'Bombing could not stop supplies along the Ho Chi Minh Trail', 'US soldiers were young conscripts on one-year tours with low morale', 'The Viet Cong had strong support from North Vietnam, China and the USSR']),
    ],
    'claims': [
        ('The first US combat troops were sent to Vietnam by President Kennedy.', False, 'Kennedy sent advisers; Johnson sent the first combat troops in March 1965.'),
        ('The Ho Chi Minh Trail passed through Laos and Cambodia.', True, 'This made it hard for the USA to attack without widening the war.'),
        ('Search and destroy missions won the support of South Vietnamese villagers.', False, 'They often killed civilians and destroyed homes, turning villagers against the USA.'),
    ],
    'c': [
        dict(q='‘The tactics of the Viet Cong were the main reason why the USA failed in Vietnam.’',
             pro=['Guerrilla warfare and tunnels neutralised American firepower', 'The Ho Chi Minh Trail kept them supplied', 'They won support from many villagers'],
             con=['US tactics such as search and destroy alienated the population', 'The South Vietnamese government was corrupt and unpopular', 'Opposition grew in the USA, especially after Tet in 1968', 'North Vietnam received aid from China and the USSR'],
             judge='Viet Cong tactics were crucial, but they succeeded because US methods and an unpopular South Vietnamese government made it impossible to win support'),
    ],
    'src': [
        S('President Eisenhower at a press conference, 7 April 1954 (extract)', 'You have a row of dominoes set up, you knock over the first one, and what will happen to the last one is the certainty that it will go over very quickly.',
          'US reasons for becoming involved in South-East Asia', 'Eisenhower argues that if one country in South-East Asia fell to communism, others would quickly follow.',
          'To explain why the USA should care about events in Indochina, as the French faced defeat at Dien Bien Phu.',
          'it is the President\'s own words at the time', 'it is a simple image used to persuade, not a detailed analysis',
          'That Vietnamese communists were also nationalists fighting for independence from France.', stance=None),
        S('a report by an American war correspondent, 1967 (illustrative)', 'We can hold any ground we choose, but the moment we leave a village the Viet Cong return. Every burnt hut makes a new recruit for them.',
          'US tactics in Vietnam', 'It suggests US tactics could not achieve lasting control and turned villagers against the USA.',
          'To inform the American public about the reality of the war.',
          'the writer reports from Vietnam', 'journalists by 1967 were increasingly critical of the war and may focus on failures',
          'The scale of US bombing of North Vietnam.', stance=True, why='it shows US tactics creating more enemies'),
        S('a television report by the American newsreader Walter Cronkite after visiting Vietnam during the Tet Offensive, 27 February 1968 (extract)', 'To say that we are mired in stalemate seems the only realistic, yet unsatisfactory, conclusion.',
          'American views of the war in 1968', 'Cronkite tells viewers that the war cannot be won and has become a stalemate.',
          'To give Americans his honest judgement on the war after Tet.',
          'Cronkite was a trusted and usually neutral reporter who had visited Vietnam', 'it is one person\'s judgement, and militarily Tet was a defeat for the Viet Cong',
          'That the Viet Cong suffered very heavy losses in the Tet Offensive.', stance=True, why='it suggests the US approach could not win the war'),
    ],
})


@c7c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c7c_troops(r, D):
    i, j = sorted(r.sample(range(len(US_VN)), 2))
    (ya, a), (yb, b) = US_VN[i], US_VN[j]
    tbl = 'US military personnel in Vietnam at the end of each year: ' + '; '.join(f'{y}: {n:,}' for y, n in US_VN) + '.'
    ch = b - a
    pc = 100 * ch / a
    word = 'increase' if ch > 0 else 'decrease'
    stem = f'Study the figures. {tbl} Calculate the percentage {word} in US personnel between {ya} and {yb}.'
    res = f'{word} of {abs(pc):.0f}%'
    key = f'({b:,} − {a:,}) ÷ {a:,} × 100 = {pc:.0f}%, i.e. a {res}. 1 mark method, 1 mark answer [2]'
    m = 2
    if D >= 3:
        peak = max(US_VN, key=lambda x: x[1])
        stem += ' Identify the year with the most US personnel, and explain why the number fell after that.'
        key = (f'Percentage: ({b:,} − {a:,}) ÷ {a:,} × 100 = {pc:.0f}%, a {res} (2 marks). Peak year {peak[0]} (1 mark). Explanation (up to 2 marks): Nixon\'s policy of Vietnamisation from 1969 '
               'withdrew US troops and handed fighting to the South Vietnamese army, because of opposition at home after Tet and the cost of the war [5]')
        m = 5
    return {'stem': stem, 'answer': f'A {res}' + (f'; peak in 1968; numbers fell because of Vietnamisation under Nixon.' if D >= 3 else ''), 'key': key, 'marks': m, 'minutes': _mins(m), 'type': 'numerical'}


c7d = T('Why the USA withdrew from Vietnam and how far containment succeeded', 'withdrew from vietnam', 'containment succeeded')
build(c7d, {
    'enq': 'why the USA withdrew from Vietnam', 'claim': 'opposition in the USA was the main reason for the US withdrawal from Vietnam',
    'stim': ['In January 1973 the Paris Peace Accords ended direct US involvement in the Vietnam War.', 'In 1969 President Nixon announced a policy of Vietnamisation.',
             'In April 1975 North Vietnamese forces captured Saigon.'],
    'terms': [
        ('Vietnamisation', 'Nixon\'s policy of withdrawing US troops and handing the fighting to the South Vietnamese army'),
        ('Tet Offensive', 'the surprise Viet Cong and North Vietnamese attack on cities across South Vietnam in January 1968'),
        ('anti-war movement', 'the protests in the USA, especially among students, against the Vietnam War'),
        ('Paris Peace Accords', 'the January 1973 agreement for a ceasefire and the withdrawal of US forces from Vietnam'),
        ('draft', 'the US system of conscripting young men into the armed forces'),
        ('credibility gap', 'the difference between what the US government said about the war and what Americans saw happening'),
    ],
    'dates': [('the Tet Offensive began', 1968, 1), ('Nixon announced Vietnamisation', 1969, 6), ('four students were shot dead at Kent State University', 1970, 5),
              ('the Paris Peace Accords were signed', 1973, 1), ('Saigon fell to North Vietnamese forces', 1975, 4)],
    'mcq': [
        ('Why was the Tet Offensive a turning point, even though the Viet Cong suffered heavy losses?', 'It convinced many Americans that the war could not be won', ['It ended the war immediately', 'It was a victory for US bombing', 'It brought China into the war'], '[1]'),
        ('What happened at Kent State University in May 1970?', 'National Guardsmen shot dead four students protesting against the war', ['The first draft cards were burnt', 'Nixon announced the end of the war', 'Veterans opened a war memorial'], 'The protest was against the invasion of Cambodia. [1]'),
        ('About how many US servicemen died in the Vietnam War?', 'About 58,000', ['About 5,800', 'About 580,000', 'About 1.5 million'], '[1]'),
        ('What happened to Vietnam in 1975-76?', 'It was reunited as a communist state', ['It joined NATO', 'It remained divided at the 17th parallel', 'It became a US territory'], 'Saigon fell in April 1975 and was renamed Ho Chi Minh City. [1]'),
    ],
    'a': [
        ('Describe the opposition to the Vietnam War in the USA.', 'forms of opposition to the Vietnam War in the USA',
         ['Large protest marches took place in Washington and other cities', 'Students protested on university campuses, for example at Kent State in 1970', 'Young men burnt their draft cards or avoided the draft', 'Television and newspapers showed the brutality of the war, such as the My Lai massacre', 'Some veterans joined the protests']),
        ('Describe Nixon\'s policy of Vietnamisation.', 'features of Vietnamisation',
         ['US troops were gradually withdrawn from 1969', 'The South Vietnamese army was trained and equipped to take over the fighting', 'The USA continued heavy bombing, including of Cambodia and Laos', 'US troop numbers fell from over 500,000 to about 24,000 by the end of 1972', 'It ended with the Paris Peace Accords in 1973']),
    ],
    'b': [
        ('Why did the USA withdraw from Vietnam?',
         ['The Tet Offensive of 1968 convinced many Americans the war could not be won', 'Opposition at home grew, with mass protests and media criticism', 'The war was enormously expensive and damaged Johnson\'s domestic programmes', 'About 58,000 Americans were killed and morale among troops was low', 'Nixon was elected promising to end the war and achieve “peace with honour”']),
        ('Why did the media play an important part in turning Americans against the war?',
         ['Vietnam was the first war shown nightly on television', 'Images of atrocities such as My Lai shocked the public', 'Reports of Tet contradicted government claims that the war was being won', 'Respected reporters such as Walter Cronkite called the war a stalemate']),
    ],
    'claims': [
        ('The USA withdrew from Vietnam because it was defeated in the Tet Offensive.', False, 'Militarily Tet was a defeat for the Viet Cong; its importance was its effect on American opinion.'),
        ('Vietnam was reunited under communist rule after the fall of Saigon in 1975.', True, 'North Vietnamese forces captured Saigon in April 1975.'),
        ('Containment failed everywhere in Asia.', False, 'South Korea remained non-communist; but Vietnam, Laos and Cambodia all became communist in 1975.'),
    ],
    'c': [
        dict(q='‘Opposition in the USA was the main reason for the US withdrawal from Vietnam.’',
             pro=['Mass protests and media coverage made the war politically impossible to continue', 'Nixon promised to end the war to win the 1968 election'],
             con=['The USA could not defeat the Viet Cong\'s guerrilla tactics', 'The South Vietnamese government was weak and unpopular', 'The financial cost of the war was enormous', 'Tet showed the war could not be won militarily at acceptable cost'],
             judge='Military failure made the war unwinnable, but it was opposition at home that forced US leaders to accept withdrawal'),
        dict(q='How far was containment a success in Asia between 1950 and 1975?',
             pro=['South Korea was saved from communism', 'Taiwan, Japan, Thailand and the Philippines remained non-communist', 'SEATO and US bases restricted communist expansion'],
             con=['China became communist in 1949', 'Vietnam, Laos and Cambodia all became communist in 1975', 'The Vietnam War damaged US prestige and cost huge sums and lives'],
             judge='Containment had mixed results: it succeeded in Korea and much of the region, but its failure in Vietnam was a major defeat'),
    ],
    'src': [
        S('a photograph taken for the Associated Press near Trang Bang, South Vietnam, June 1972 (description)', 'Children run screaming along a road after a napalm attack. In the centre is a nine-year-old girl, Phan Thi Kim Phuc, whose clothes have been burnt off. Soldiers walk behind them.',
          'the effects of the war on civilians', 'It shows the terrible suffering of Vietnamese civilians caused by the war.',
          'To record the effects of the napalm attack; when published around the world it increased opposition to the war.',
          'it is a real photograph taken at the moment of the event', 'it shows a single incident; the napalm was dropped by the South Vietnamese air force, which the photograph does not show',
          'The scale of the war or the reasons why the USA was involved.', stance=True, why='images like this strengthened opposition to the war in the USA', visual=True,
          context='By 1972 most US ground troops had already been withdrawn.'),
        S('a speech by a supporter of President Nixon, 1970 (illustrative)', 'The noisy protesters on our campuses do not speak for America. The silent majority wants an honourable peace, not a surrender.',
          'American public opinion on the war', 'It suggests that most Americans did not support the anti-war protesters.',
          'To defend Nixon\'s policy and attack the anti-war movement.',
          'it reflects the view that many Americans held', 'it is a political speech intended to win support',
          'That Nixon was withdrawing troops because of the pressure of public opinion.', stance=False, why='it suggests opposition did not represent most Americans'),
    ],
})

CHAPTERS[7] = [c7a, c7b, c7c, c7d]


# ============================================================== CHAPTER 8: How secure was the USSR's control over Eastern Europe, 1948-c.1989?

c8a = T('Soviet control of Eastern Europe and the Warsaw Pact', 'soviet control', 'warsaw pact')
build(c8a, {
    'enq': 'Soviet control of eastern Europe', 'claim': 'Soviet control of eastern Europe was secure in the 1950s',
    'stim': ['By 1949 the USSR controlled eastern Europe through Cominform, Comecon and the Red Army.', 'In May 1955 the USSR and its satellites signed the Warsaw Pact.',
             'Stalin died in March 1953.'],
    'terms': [
        ('Warsaw Pact', 'the military alliance of the USSR and its eastern European satellites, formed in May 1955'),
        ('Comecon', 'the organisation set up in 1949 to coordinate the economies of the communist states'),
        ('de-Stalinisation', 'Khrushchev\'s policy of criticising Stalin and reducing some of the terror of his rule'),
        ('Secret Speech', 'Khrushchev\'s speech of February 1956 denouncing Stalin\'s crimes'),
        ('peaceful coexistence', 'Khrushchev\'s idea that communism and capitalism could compete without war'),
        ('satellite state', 'a country formally independent but controlled by the USSR'),
    ],
    'dates': [('Comecon was set up', 1949, 1), ('Stalin died', 1953, 3), ('workers rose in revolt in East Germany', 1953, 6), ('West Germany joined NATO', 1955, 5.09), ('the Warsaw Pact was signed', 1955, 5.14),
              ('Khrushchev made his Secret Speech', 1956, 2)],
    'mcq': [
        ('Which event led directly to the formation of the Warsaw Pact in 1955?', 'West Germany joining NATO', ['The Hungarian Uprising', 'The building of the Berlin Wall', 'The Marshall Plan'], '[1]'),
        ('What happened in East Germany in June 1953?', 'A workers\' uprising was crushed by Soviet tanks', ['The Berlin Wall was built', 'East Germany left the Warsaw Pact', 'Free elections were held'], '[1]'),
        ('What did Khrushchev do in his Secret Speech of February 1956?', 'He denounced Stalin\'s crimes and cult of personality', ['He announced the building of the Berlin Wall', 'He declared war on the USA', 'He ended the Warsaw Pact'], 'It encouraged hopes of reform in eastern Europe. [1]'),
        ('Which of these was NOT a method the USSR used to control eastern Europe?', 'Allowing free multiparty elections', ['Soviet troops stationed in satellite states', 'Secret police networks', 'Comecon economic planning'], '[1]'),
    ],
    'a': [
        ('Describe the methods the USSR used to control eastern Europe.', 'methods the USSR used to control eastern Europe',
         ['Communist parties loyal to Moscow ruled as one-party states', 'Secret police such as the Stasi in East Germany watched and arrested opponents', 'Soviet troops were stationed in satellite states', 'Cominform and later the Warsaw Pact tied the states together politically and militarily', 'Comecon coordinated economies to serve Soviet needs', 'Censorship and propaganda controlled information']),
        ('Describe the effects of Soviet control on the people of eastern Europe.', 'effects of Soviet control on the people of eastern Europe',
         ['Political opponents were imprisoned or executed', 'There was little freedom of speech, religion or travel', 'Living standards were lower than in the West, with shortages of consumer goods', 'Resources were taken to benefit the USSR', 'Contact with the West was restricted']),
    ],
    'b': [
        ('Why did Khrushchev\'s Secret Speech cause problems for Soviet control?',
         ['It admitted Stalin had committed crimes, undermining the leaders he had installed', 'It raised hopes that the USSR would allow more freedom', 'It encouraged reformers in Poland and Hungary in 1956', 'Communist leaders such as Rákosi lost authority']),
        ('Why did the USSR set up the Warsaw Pact?',
         ['West Germany joined NATO in May 1955, which alarmed the USSR', 'It gave the USSR a legal reason to keep troops in the satellites', 'It tied the satellite armies to Soviet command', 'It was a propaganda response to NATO']),
    ],
    'claims': [
        ('The Warsaw Pact was formed before NATO.', False, 'NATO was formed in 1949; the Warsaw Pact in 1955, after West Germany joined NATO.'),
        ('Soviet troops crushed a workers\' uprising in East Germany in 1953.', True, 'The uprising of 17 June 1953 was put down by Soviet tanks.'),
        ('De-Stalinisation meant that the USSR gave up control of eastern Europe.', False, 'It meant criticism of Stalin\'s methods, not an end to Soviet control, as Hungary found in 1956.'),
    ],
    'c': [
        dict(q='‘Military force was the main way the USSR controlled eastern Europe.’',
             pro=['Soviet troops crushed uprisings in East Germany (1953) and Hungary (1956)', 'The Warsaw Pact justified stationing troops in satellite states'],
             con=['Loyal communist parties governed day to day', 'Secret police and censorship kept people in line', 'Comecon tied economies to the USSR', 'Propaganda and education promoted communism'],
             judge='Force was the ultimate guarantee of control, but day-to-day control relied on communist parties, secret police and economic ties'),
    ],
    'src': [
        S('a photograph taken in East Berlin, 17 June 1953 (description)', 'Young men are throwing stones at Soviet tanks in a street in East Berlin.',
          'the 1953 uprising in East Germany', 'It shows that some East Germans were prepared to resist Soviet control openly and that the USSR used tanks to restore order.',
          'To record the uprising; such photographs were published widely in the West.',
          'it is a photograph taken at the time', 'it shows only one moment, and Western newspapers selected images that showed Soviet repression',
          'How widespread the uprising was or how it was ended.', stance=False, why='it shows Soviet control faced open resistance in 1953', visual=True),
        S('a statement by the East German government, June 1953 (summary)', 'The government claimed that the disturbances were the work of Western agents and provocateurs, and that the workers had been misled.',
          'the East German government\'s view of the uprising', 'It blames the uprising on Western agents rather than on genuine discontent.',
          'To justify the use of force and hide the scale of opposition to the regime.',
          'it shows the official explanation', 'it is propaganda by a government trying to hide its unpopularity',
          'That the uprising began with protests against increased work quotas.', stance=True, why='it presents the regime as in control and the uprising as foreign-inspired'),
    ],
})

c8b = T('The Hungarian Uprising, 1956', 'hungarian uprising')
build(c8b, {
    'enq': 'the Hungarian Uprising', 'claim': 'the Hungarian Uprising failed because the West did not help',
    'stim': ['On 23 October 1956 students in Budapest demonstrated against Soviet control.', 'In November 1956 Soviet tanks entered Budapest to crush the Hungarian Uprising.',
             'In July 1956 the hated Hungarian leader Rákosi was removed from power.'],
    'terms': [
        ('Imre Nagy', 'the reformist Hungarian Prime Minister during the 1956 uprising, executed in 1958'),
        ('Mátyás Rákosi', 'the Stalinist leader of Hungary until July 1956'),
        ('János Kádár', 'the Hungarian communist installed as leader by the USSR in November 1956'),
        ('neutrality', 'not taking sides in a conflict; Nagy announced that Hungary would be neutral'),
        ('AVH', 'the Hungarian secret police, hated for its brutality'),
    ],
    'dates': [('Khrushchev made his Secret Speech', 1956, 2), ('Rákosi was removed from power', 1956, 7), ('demonstrations began in Budapest', 1956, 10.23), ('Nagy announced Hungary would leave the Warsaw Pact', 1956, 11.01),
              ('Soviet forces attacked Budapest', 1956, 11.04), ('Imre Nagy was executed', 1958)],
    'mcq': [
        ('Which announcement by Nagy most alarmed the USSR?', 'That Hungary would leave the Warsaw Pact', ['That he would build a new railway', 'That Hungary would join Comecon', 'That he would visit Moscow'], 'Announced on 1 November 1956. [1]'),
        ('Why was the West unable to help Hungary in 1956?', 'Britain and France were involved in the Suez crisis and the USA feared nuclear war', ['Hungary was a NATO member', 'The UN had banned all aid', 'Hungary had asked the West not to help'], '[1]'),
        ('About how many Hungarians fled the country after the uprising?', 'About 200,000', ['About 2,000', 'About 2 million', 'About 20,000'], '[1]'),
        ('Who replaced Nagy as leader of Hungary in November 1956?', 'János Kádár', ['Mátyás Rákosi', 'Alexander Dubček', 'Wladyslaw Gomułka'], '[1]'),
    ],
    'a': [
        ('Describe the events of the Hungarian Uprising in October-November 1956.', 'events of the Hungarian Uprising',
         ['Students and workers demonstrated in Budapest on 23 October and pulled down a statue of Stalin', 'Fighting broke out with the AVH and Soviet troops', 'Imre Nagy became Prime Minister and Soviet troops withdrew from Budapest', 'Nagy announced free elections and that Hungary would leave the Warsaw Pact', 'On 4 November Soviet tanks attacked Budapest and crushed the rising', 'Thousands were killed and about 200,000 fled abroad']),
        ('What reforms did Nagy announce in 1956?', 'reforms announced by Nagy in 1956',
         ['Free elections with more than one party', 'Freedom of speech and an end to censorship', 'Release of political prisoners such as Cardinal Mindszenty', 'Withdrawal of Soviet troops', 'Hungary to leave the Warsaw Pact and become neutral']),
    ],
    'b': [
        ('Why did the Hungarians rise against Soviet control in 1956?',
         ['They hated the brutal Rákosi regime and the AVH secret police', 'Living standards were low and Soviet economic demands took Hungarian resources', 'Khrushchev\'s Secret Speech raised hopes of change', 'Events in Poland in 1956 suggested reform was possible', 'Hungarians resented Soviet control of their culture and religion']),
        ('Why did the USSR crush the Hungarian Uprising?',
         ['Nagy planned to leave the Warsaw Pact, which threatened the whole Soviet bloc', 'Multiparty elections would end communist rule', 'Other satellites might follow Hungary\'s example', 'Khrushchev needed to show strength to hard-liners in Moscow', 'The West was distracted by the Suez crisis']),
    ],
    'claims': [
        ('The USA sent troops to help the Hungarian rebels in 1956.', False, 'The USA gave no military help: it feared nuclear war and Britain and France were involved at Suez.'),
        ('Nagy announced that Hungary would leave the Warsaw Pact.', True, 'He announced it on 1 November 1956; Soviet forces attacked three days later.'),
        ('After the uprising Nagy remained Prime Minister of Hungary.', False, 'He was replaced by Kádár, arrested and executed in 1958.'),
    ],
    'c': [
        dict(q='‘The Hungarian Uprising failed because the West did not help.’',
             pro=['Radio Free Europe broadcasts encouraged Hungarians to expect help that never came', 'Without Western support the rebels could not resist Soviet tanks'],
             con=['The USSR was determined to keep Hungary in the Warsaw Pact', 'The Soviet army was overwhelmingly strong', 'Western help risked nuclear war, so it was never realistic', 'Nagy\'s move to leave the Warsaw Pact made a Soviet attack certain'],
             judge='Western help could not have changed the result without risking nuclear war; the uprising failed because the USSR was determined and able to crush it'),
        dict(q='How far did the Hungarian Uprising show that Soviet control of eastern Europe was secure?',
             pro=['The USSR crushed the rising in days and installed a loyal leader', 'The West did not intervene, showing it accepted the Soviet sphere'],
             con=['The uprising showed deep hatred of Soviet rule', 'Control depended on force rather than consent', 'Kádár later had to allow some economic reforms to keep people content'],
             judge='The rising showed that Soviet control was militarily secure but politically fragile, depending on the threat of force'),
    ],
    'src': [
        S('the final radio broadcast by Imre Nagy, 4 November 1956 (extract)', 'Today at daybreak Soviet troops attacked our capital with the obvious intention of overthrowing the legal democratic Hungarian government. Our troops are in combat. The government is at its post. I notify the people of our country and the entire world of this fact.',
          'the Soviet attack on Budapest', 'Nagy tells Hungarians and the world that Soviet forces are attacking the legal Hungarian government.',
          'To inform the world and appeal, by implication, for international support.',
          'it was broadcast as events happened by the Prime Minister himself', 'Nagy wanted to win sympathy, so he presents the Soviet action in the worst light',
          'That Nagy had announced Hungary would leave the Warsaw Pact.', stance=True, why='it shows Hungary hoped the world would respond'),
        S('a statement by the Soviet government, 1956 (summary)', 'The Soviet government stated that its troops had been asked to help the Hungarian people defeat counter-revolutionary forces supported by Western imperialists.',
          'the Soviet justification for the invasion', 'It presents the invasion as help given to Hungary against Western-backed counter-revolution.',
          'To justify the invasion to Soviet citizens and the world.',
          'it shows the official Soviet view', 'it is propaganda; the request for help came from Kádár\'s new government after the attack began',
          'The reforms Nagy had promised, such as free elections.', stance=False, why='it says the rising failed because the Hungarian people themselves rejected the rebels'),
    ],
})

c8c = T('The Berlin Wall, 1961', 'berlin wall')
build(c8c, {
    'enq': 'the building of the Berlin Wall', 'claim': 'the Berlin Wall was a sign of Soviet weakness',
    'stim': ['On 13 August 1961 East German troops began to seal off West Berlin with barbed wire.', 'Between 1949 and 1961 millions of East Germans left for the West, many of them through Berlin.',
             'In June 1963 President Kennedy visited West Berlin.'],
    'terms': [
        ('refugee', 'a person who flees their country, as many East Germans did through Berlin'),
        ('brain drain', 'the loss of skilled and educated people, such as doctors and engineers, to another country'),
        ('Checkpoint Charlie', 'the best-known crossing point between East and West Berlin, scene of a tank stand-off in October 1961'),
        ('Stasi', 'the East German secret police'),
        ('death strip', 'the area between the inner and outer walls, guarded by soldiers with orders to shoot'),
    ],
    'dates': [('the German Democratic Republic was set up', 1949), ('Kennedy and Khrushchev met at the Vienna summit', 1961, 6), ('the Berlin Wall was begun', 1961, 8),
              ('US and Soviet tanks faced each other at Checkpoint Charlie', 1961, 10), ('Kennedy visited West Berlin', 1963), ('the Berlin Wall was opened', 1989)],
    'mcq': [
        ('Why did the East German government build the Berlin Wall?', 'To stop East Germans escaping to the West', ['To keep West German troops out of East Germany', 'To mark the end of the Second World War', 'Because the UN ordered it'], '[1]'),
        ('Approximately how many people had left East Germany for the West between 1949 and 1961?', 'About 2.7 million', ['About 27,000', 'About 270,000', 'About 27 million'], 'Many were young and skilled. [1]'),
        ('What did Kennedy say in West Berlin in June 1963?', '“Ich bin ein Berliner”', ['“Mr Gorbachev, tear down this wall”', '“Peace for our time”', '“We shall fight on the beaches”'], 'Reagan said “tear down this wall” in 1987. [1]'),
        ('How did the USA respond to the building of the Wall in August 1961?', 'It protested but took no military action to remove it', ['It bombed the Wall', 'It closed West Berlin', 'It invaded East Germany'], 'Kennedy said “a wall is a hell of a lot better than a war”, according to his aides. [1]'),
    ],
    'a': [
        ('Describe the building of the Berlin Wall in 1961.', 'features of the building of the Berlin Wall',
         ['On the night of 12-13 August 1961 East German troops sealed the border with barbed wire', 'Crossing points were closed and families were separated', 'The barbed wire was soon replaced by a concrete wall', 'Guard towers, searchlights and a death strip were added', 'Guards were ordered to shoot people trying to escape']),
        ('Describe the consequences of the Berlin Wall.', 'consequences of the Berlin Wall',
         ['The flood of refugees from East Germany was stopped', 'Families and friends were separated for decades', 'More than a hundred people were killed trying to cross, such as Peter Fechter in 1962', 'It became a symbol of the Cold War and of the lack of freedom in the East', 'It reduced the immediate crisis over Berlin and the risk of war']),
    ],
    'b': [
        ('Why was the Berlin Wall built in 1961?',
         ['About 2.7 million East Germans had left for the West, many through Berlin', 'Many of those leaving were young, skilled workers such as doctors and engineers', 'The loss of workers damaged the East German economy', 'West Berlin\'s prosperity was an embarrassment to communism', 'Khrushchev had failed to force the West out of Berlin at the Vienna summit']),
        ('Why did the West not try to stop the building of the Berlin Wall?',
         ['The Wall was built on East German territory', 'Using force risked war with the USSR', 'The Wall meant Khrushchev had given up trying to force the West out of West Berlin', 'Kennedy concluded that a wall was better than a war']),
    ],
    'claims': [
        ('The Berlin Wall was built to stop West Germans entering East Germany.', False, 'It was built to stop East Germans escaping to the West.'),
        ('The first barrier in August 1961 was mainly barbed wire.', True, 'It was replaced with a concrete wall in the following days and weeks.'),
        ('The building of the Berlin Wall led to a war between the superpowers.', False, 'There was a tense stand-off at Checkpoint Charlie in October 1961, but no war.'),
    ],
    'c': [
        dict(q='‘The Berlin Wall was a sign of Soviet weakness rather than strength.’',
             pro=['It showed communism had to imprison its own people to stop them leaving', 'It was a propaganda gift to the West, as shown by Kennedy\'s visit in 1963'],
             con=['It solved the refugee problem and stabilised East Germany', 'The West accepted it without action', 'It strengthened Soviet control of East Germany for nearly 30 years'],
             judge='The Wall was a practical success for the USSR in controlling East Germany, but a moral and propaganda defeat that exposed the weakness of communism\'s appeal'),
    ],
    'src': [
        S('President Kennedy\'s speech in West Berlin, 26 June 1963 (summary with extracts)', 'Kennedy told a huge crowd that “all free men, wherever they may live, are citizens of Berlin, and, therefore, as a free man, I take pride in the words ‘Ich bin ein Berliner’.” He said the Wall showed the failures of the communist system.',
          'Western views of the Berlin Wall', 'Kennedy presents the Wall as evidence that communism had failed and that West Berlin stood for freedom.',
          'To reassure West Berliners of US support and to win a propaganda victory over the USSR.',
          'it is Kennedy\'s own speech in Berlin', 'it was a propaganda speech designed to inspire, not to analyse',
          'That the USA had taken no action to stop the Wall being built.', stance=True, why='it presents the Wall as a sign that communism had failed'),
        S('an East German poster of the 1960s (description of a typical design)', 'The poster shows the border defences protecting East Germany and describes the Wall as an “anti-fascist protective rampart”.',
          'the East German justification for the Wall', 'It presents the Wall as protecting East Germany from Western aggression and fascism.',
          'To persuade East Germans that the Wall was defensive and necessary.',
          'it shows the official East German view', 'it is propaganda that hides the real purpose of stopping people from leaving',
          'That around 2.7 million people had left East Germany before 1961.', stance=False, why='it presents the Wall as a sign of strength and security', visual=True),
    ],
})

c8d = T('The Prague Spring, 1968 and the Brezhnev Doctrine', 'prague spring', 'brezhnev doctrine')
build(c8d, {
    'enq': 'the Prague Spring', 'claim': 'the Soviet invasion of Czechoslovakia in 1968 was a success for the USSR',
    'stim': ['In January 1968 Alexander Dubček became leader of the Czechoslovak Communist Party.', 'On the night of 20-21 August 1968 Warsaw Pact forces invaded Czechoslovakia.',
             'Dubček promised “socialism with a human face”.'],
    'terms': [
        ('Prague Spring', 'the period of reform in Czechoslovakia under Dubček from January to August 1968'),
        ('socialism with a human face', 'Dubček\'s aim of a communist system with more freedom and less repression'),
        ('Action Programme', 'Dubček\'s plan of reforms announced in April 1968'),
        ('Brezhnev Doctrine', 'the Soviet claim that the Warsaw Pact had the right to intervene in any socialist country where socialism was threatened'),
        ('censorship', 'government control over what can be published or broadcast'),
    ],
    'dates': [('the Hungarian Uprising was crushed', 1956), ('Dubček became leader of the Czechoslovak Communist Party', 1968, 1), ('the Action Programme was announced', 1968, 4),
              ('Warsaw Pact forces invaded Czechoslovakia', 1968, 8), ('the student Jan Palach set himself on fire in protest', 1969, 1), ('Dubček was replaced by Husák', 1969, 4)],
    'mcq': [
        ('How did Dubček\'s reforms differ from Nagy\'s in 1956?', 'Dubček promised Czechoslovakia would stay in the Warsaw Pact', ['Dubček wanted to join NATO', 'Dubček abolished the Communist Party', 'Dubček declared war on the USSR'], '[1]'),
        ('Which Warsaw Pact member refused to take part in the invasion of Czechoslovakia?', 'Romania', ['Poland', 'Hungary', 'Bulgaria'], 'Ceauşescu condemned the invasion. [1]'),
        ('How did most Czechoslovaks respond to the invasion?', 'With non-violent protest, such as removing street signs and talking to soldiers', ['By fighting a long guerrilla war', 'By welcoming the troops', 'By invading Poland'], '[1]'),
        ('Who replaced Dubček as leader of Czechoslovakia in April 1969?', 'Gustáv Husák', ['János Kádár', 'Lech Wałęsa', 'Václav Havel'], '[1]'),
    ],
    'a': [
        ('What reforms were introduced during the Prague Spring?', 'reforms of the Prague Spring',
         ['Censorship was relaxed and the press could criticise the government', 'People were allowed more freedom to travel abroad', 'Some private enterprise and more trade with the West', 'Greater power for trade unions and less central planning', 'Discussion of other political groups, though the Communist Party kept the leading role']),
        ('Describe the Warsaw Pact invasion of Czechoslovakia in August 1968.', 'features of the invasion of Czechoslovakia in 1968',
         ['Hundreds of thousands of Soviet and other Warsaw Pact troops invaded on 20-21 August', 'Dubček and other leaders were arrested and taken to Moscow', 'Czechoslovaks resisted mainly by non-violent protest', 'Dozens of civilians were killed', 'Dubček was later replaced by Husák and the reforms were reversed']),
    ],
    'b': [
        ('Why did the USSR invade Czechoslovakia in 1968?',
         ['Brezhnev feared the reforms would lead to the end of communist control', 'Freedom of the press allowed criticism of the USSR', 'Leaders of East Germany and Poland feared reform would spread to their countries', 'Czechoslovakia bordered West Germany and was strategically important', 'Contacts with Tito\'s Yugoslavia and Romania suggested Czechoslovakia might move away from Moscow']),
        ('Why did the West not intervene to help Czechoslovakia?',
         ['The USA was involved in the Vietnam War', 'Intervention risked nuclear war', 'Czechoslovakia was accepted as part of the Soviet sphere', 'The West was also improving relations with the USSR (détente)']),
    ],
    'claims': [
        ('Dubček planned to take Czechoslovakia out of the Warsaw Pact.', False, 'Unlike Nagy, Dubček promised to stay in the Warsaw Pact.'),
        ('The Brezhnev Doctrine was announced after the invasion of Czechoslovakia.', True, 'Brezhnev set it out in November 1968 to justify the invasion.'),
        ('The Czechoslovak army fought a long war against the invading forces.', False, 'Resistance was mainly non-violent; the army was ordered not to resist.'),
    ],
    'c': [
        dict(q='‘The Soviet invasion of Czechoslovakia in 1968 was a success for the USSR.’',
             pro=['Communist control was restored and the reforms were ended', 'The Brezhnev Doctrine warned other satellites not to try reform', 'The West did not intervene'],
             con=['The invasion damaged the USSR\'s reputation around the world, including among communists in the West', 'It showed control relied on force, not consent', 'Romania and Yugoslavia criticised it, exposing divisions'],
             judge='In the short term it was a success, but it showed that Soviet control depended on force, a weakness exposed in the 1980s'),
        dict(q='How similar were the Soviet responses to Hungary (1956) and Czechoslovakia (1968)?',
             pro=['In both cases the USSR used tanks to crush reform', 'In both cases the leader was removed and a loyal communist installed', 'In both cases the West did not intervene'],
             con=['Hungary\'s rising was violent and thousands died; resistance in Czechoslovakia was mainly non-violent', 'Czechoslovakia was invaded by several Warsaw Pact countries, not just the USSR', 'Nagy was executed; Dubček was demoted but survived'],
             judge='The aim and result were very similar, but the scale of violence and the use of the Warsaw Pact were different'),
    ],
    'src': [
        S('a speech by Leonid Brezhnev to the Polish Communist Party Congress, November 1968 (translated extract)', 'When forces that are hostile to socialism try to turn the development of some socialist country towards capitalism, it becomes not only a problem of the country concerned, but a common problem and concern of all socialist countries.',
          'the Brezhnev Doctrine', 'Brezhnev claims all socialist countries have the right to intervene if socialism is threatened in any one of them.',
          'To justify the invasion of Czechoslovakia and warn other satellites against reform.',
          'it is Brezhnev\'s own statement of Soviet policy', 'it presents an invasion as a defence of socialism, which is propaganda',
          'That many Czechoslovaks supported Dubček\'s reforms and protested against the invasion.', stance=True, why='it shows the USSR had established a clear doctrine to keep control'),
        S('a photograph taken in Bratislava, Czechoslovakia, August 1968 (description)', 'A man stands in front of a Soviet tank with his shirt open, as if daring the soldiers to shoot. Crowds of people surround the tank.',
          'Czechoslovak reactions to the invasion', 'It shows Czechoslovaks defied the invasion with courage and non-violent protest.',
          'To record the protests; such images were widely published in the West.',
          'it is a photograph taken at the time', 'it shows one moment and was chosen by Western newspapers to show resistance',
          'That the reforms were reversed and Dubček was removed in 1969.', stance=False, why='it shows Soviet control was resented and the invasion damaged the USSR\'s image', visual=True),
    ],
})

c8e = T('Solidarity in Poland and Gorbachev: the collapse of Soviet control by 1989', 'solidarity', 'gorbachev', 'collapse of soviet control')
build(c8e, {
    'enq': 'the collapse of Soviet control in eastern Europe', 'claim': 'Gorbachev was the main reason for the collapse of Soviet control in eastern Europe',
    'stim': ['In August 1980 workers at the Lenin Shipyard in Gdańsk went on strike.', 'In March 1985 Mikhail Gorbachev became leader of the Soviet Union.',
             'On 9 November 1989 the Berlin Wall was opened.'],
    'terms': [
        ('Solidarity', 'the independent trade union led by Lech Wałęsa, founded in Poland in 1980'),
        ('martial law', 'military rule imposed by a government in an emergency, as in Poland in December 1981'),
        ('glasnost', 'Gorbachev\'s policy of openness, allowing more freedom of speech and information'),
        ('perestroika', 'Gorbachev\'s policy of restructuring the Soviet economy'),
        ('Sinatra Doctrine', 'the 1989 policy that eastern European states could go their “own way” without Soviet intervention'),
        ('Velvet Revolution', 'the peaceful end of communist rule in Czechoslovakia in November-December 1989'),
    ],
    'dates': [('Karol Wojtyła, a Pole, was elected Pope John Paul II', 1978), ('Solidarity was founded after the Gdańsk strikes', 1980), ('martial law was declared in Poland', 1981),
              ('Gorbachev became Soviet leader', 1985), ('the Berlin Wall was opened', 1989), ('the Warsaw Pact was dissolved', 1991, 7), ('the USSR collapsed', 1991, 12)],
    'mcq': [
        ('Who was the leader of Solidarity?', 'Lech Wałęsa', ['Wojciech Jaruzelski', 'Václav Havel', 'Alexander Dubček'], '[1]'),
        ('Why did General Jaruzelski declare martial law in December 1981?', 'To crush Solidarity and avoid a possible Soviet invasion', ['To welcome the Pope', 'To prepare for war with Germany', 'To hold free elections'], '[1]'),
        ('What did glasnost mean?', 'Openness and greater freedom of speech', ['Restructuring of the economy', 'Military rule', 'Withdrawal from Afghanistan'], 'Perestroika was economic restructuring. [1]'),
        ('Which country opened its border with Austria in 1989, allowing East Germans to escape to the West?', 'Hungary', ['Poland', 'Romania', 'Bulgaria'], '[1]'),
        ('In which country was the communist leader executed in December 1989?', 'Romania', ['Hungary', 'Poland', 'East Germany'], 'Nicolae Ceauşescu was executed on 25 December 1989. [1]'),
    ],
    'a': [
        ('Describe the rise of Solidarity in Poland in 1980-81.', 'features of the rise of Solidarity in 1980-81',
         ['Rising food prices led to strikes, including at the Lenin Shipyard in Gdańsk in August 1980', 'Strikers led by Lech Wałęsa issued 21 demands, including free trade unions and the right to strike', 'The government accepted the Gdańsk Agreement in August 1980', 'Solidarity grew to about ten million members', 'In December 1981 General Jaruzelski declared martial law and banned Solidarity']),
        ('Describe the collapse of communist rule in eastern Europe in 1989.', 'events in the collapse of communist rule in 1989',
         ['In Poland, Solidarity won semi-free elections in June 1989 and a non-communist Prime Minister took office', 'Hungary opened its border with Austria and East Germans escaped to the West', 'Mass protests in East Germany led to the opening of the Berlin Wall on 9 November', 'The Velvet Revolution ended communist rule in Czechoslovakia', 'In Romania Ceauşescu was overthrown and executed in December']),
        ('Describe Gorbachev\'s policies.', 'policies introduced by Gorbachev',
         ['Glasnost: openness and more freedom of speech', 'Perestroika: restructuring the economy to make it more efficient', 'Reducing military spending and making arms agreements with the USA', 'Withdrawing Soviet troops from Afghanistan, completed in 1989', 'Telling eastern European leaders the USSR would not use force to keep them in power']),
    ],
    'b': [
        ('Why was Solidarity a threat to Soviet control?',
         ['It was an independent organisation outside Communist Party control, which was not allowed under communism', 'It had about ten million members, a large share of Poland\'s workers', 'It had the support of the Catholic Church and the Polish Pope', 'Other satellites might copy it']),
        ('Why did Soviet control of eastern Europe collapse in 1989?',
         ['Gorbachev made it clear that the USSR would not use force to keep communist governments in power', 'The economies of the USSR and its satellites were failing and could not match the West', 'Solidarity in Poland showed communism could be challenged and replaced peacefully', 'Glasnost allowed people to criticise their governments openly', 'Events in one country encouraged the next, as when Hungary opened its border']),
    ],
    'claims': [
        ('Solidarity was destroyed for good by martial law in 1981.', False, 'It was banned but survived underground and won the elections of 1989.'),
        ('Gorbachev withdrew Soviet troops from Afghanistan.', True, 'The withdrawal was completed in February 1989.'),
        ('Soviet tanks were used to crush protests in East Germany in 1989.', False, 'Gorbachev refused to use force; the Berlin Wall was opened on 9 November 1989.'),
    ],
    'c': [
        dict(q='‘Gorbachev was the main reason for the collapse of Soviet control in eastern Europe.’',
             pro=['He refused to use force, abandoning the Brezhnev Doctrine', 'Glasnost encouraged open criticism', 'His reforms raised hopes of change in the satellites'],
             con=['Economic failure made the communist system unsustainable', 'Solidarity in Poland showed communism could be challenged', 'People power in the satellites forced change', 'Western pressure and the arms race added to Soviet economic problems'],
             judge='Gorbachev did not intend to end Soviet control, but his refusal to use force allowed long-standing discontent and economic failure to bring it down'),
        dict(q='How important was Solidarity in the collapse of communism in eastern Europe?',
             pro=['It was the first independent mass movement in the Soviet bloc', 'It survived martial law and won the 1989 elections, showing others the way'],
             con=['Without Gorbachev\'s refusal to intervene, Solidarity might have been crushed again', 'Economic decline undermined all the communist regimes', 'Events in Hungary and East Germany had their own causes'],
             judge='Solidarity was very important as an example, but it succeeded in 1989 because Gorbachev would not intervene'),
    ],
    'src': [
        S('a list of the main demands of the Gdańsk strikers, August 1980 (summary of selected demands)', 'The strikers demanded free trade unions independent of the Communist Party, the right to strike, freedom of speech and the press, the release of political prisoners and the broadcasting of Sunday Mass on the radio.',
          'the aims of the Gdańsk strikers', 'It shows the strikers wanted political freedoms, not just better pay and conditions.',
          'To set out their demands to the Polish government in negotiations.',
          'it shows exactly what the strikers asked for', 'it does not show how many Poles supported these demands or how the government responded',
          'That the government accepted the Gdańsk Agreement but later declared martial law.', stance=False, why='it shows pressure for change came from Polish workers themselves rather than from Gorbachev, who was not yet in power', published=False),
        S('an extract from a modern history textbook (illustrative)', 'Gorbachev did not set out to end Soviet control of eastern Europe. But once it was clear that Soviet tanks would not come, the communist regimes, which had depended on that threat for forty years, fell within months.',
          'the end of Soviet control', 'It argues Gorbachev\'s refusal to use force was decisive, even though he did not intend the collapse.',
          'To explain to students why communism collapsed so quickly in 1989.',
          'it is written with hindsight and can draw on later evidence', 'it is a brief summary and plays down economic and popular causes',
          'The role of Solidarity and of economic failure.', stance=True, why='it makes Gorbachev\'s decision the key factor', kind='secondary', published=True),
    ],
})

CHAPTERS[8] = [c8a, c8b, c8c, c8d, c8e]


# ============================================================== CHAPTER 1: Historical skills (built from the content packs above)

def packs(chapters):
    """[(chapter_no, pack)] for every topic in the given chapters."""
    return [(n, t.pack) for n in sorted(chapters) for t in chapters[n] if getattr(t, 'pack', None)]


GENERIC_JUDGE = ['There were many reasons and all of them were equally important.', 'I agree completely because it was the most important thing.',
                 'Some historians agree and some historians disagree, so it is impossible to decide.', 'This is a difficult question and there are arguments on both sides.']

COMMAND = [
    ('describe', 'give a detailed account of the main features of an event or situation, with accurate supporting detail'),
    ('identify', 'name or state a point briefly, without needing to explain it'),
    ('explain why', 'give reasons and show how each one helped to bring about the event or outcome'),
    ('how far', 'weigh the evidence for and against a statement and reach a supported judgement'),
    ('how important', 'judge the significance of one factor by comparing it with other factors'),
    ('supporting detail', 'specific, accurate evidence such as a name, date, number or event that develops a point'),
    ('relevance', 'how directly a piece of information helps to answer the question set'),
]
CAUSATION = [
    ('long-term cause', 'a cause that built up over many years and created the conditions for an event'),
    ('short-term cause', 'a cause that happened shortly before an event and made it more likely to happen then'),
    ('trigger', 'the immediate event that sets off a larger event, such as the assassination at Sarajevo in 1914'),
    ('consequence', 'a result or effect of an event'),
    ('factor', 'one of several reasons or influences that together explain an event'),
    ('turning point', 'a moment when the direction of events changes significantly'),
]
SOURCE_TERMS = [
    ('provenance', 'the origin of a source: who produced it, when, where and for whom'),
    ('purpose', 'the reason a source was produced, such as to inform, persuade or record'),
    ('message', 'the main point or argument a source is trying to get across'),
    ('utility', 'how useful a source is for answering a particular question'),
    ('reliability', 'how far a source can be trusted to give an accurate account'),
    ('cross-referencing', 'checking a source against other sources and own knowledge'),
    ('propaganda', 'material produced to persuade people to hold particular views, often one-sided'),
    ('inference', 'a conclusion worked out from a source that it does not state directly'),
]
JUDGE_TERMS = [
    ('judgement', 'a conclusion that answers the question directly and explains why one side or factor outweighs the other'),
    ('counter-argument', 'a point that challenges or argues against the statement in the question'),
    ('criteria', 'the standards used to reach a judgement, such as how many people were affected or how long the effects lasted'),
    ('balanced argument', 'an answer that explains points on both sides of the question before reaching a judgement'),
    ('substantiated', 'supported by accurate and relevant evidence'),
    ('interpretation', 'a historian\'s view or judgement about the past'),
]
CAUSE_SETS = [
    ('the outbreak of the First World War in 1914', ['the alliance system', 'the Anglo-German naval race', 'imperial rivalry in Africa'], ['the assassination of Franz Ferdinand at Sarajevo', 'Austria-Hungary\'s ultimatum to Serbia', 'the German invasion of Belgium'], 'the assassination of Franz Ferdinand at Sarajevo'),
    ('the outbreak of the Second World War in 1939', ['resentment of the Treaty of Versailles', 'the failure of the League of Nations', 'the Great Depression'], ['the Nazi-Soviet Pact', 'Hitler\'s demands over Danzig', 'the British guarantee to Poland'], 'the German invasion of Poland on 1 September 1939'),
    ('the Soviet invasion of Hungary in 1956', ['hatred of the Rákosi regime and the secret police', 'low living standards under Soviet economic control', 'resentment of Soviet domination since 1945'], ['Khrushchev\'s Secret Speech raising hopes of reform', 'the student demonstrations of 23 October', 'Nagy\'s promise of free elections'], 'Nagy\'s announcement that Hungary would leave the Warsaw Pact'),
    ('the Cuban Missile Crisis of 1962', ['US hostility to Castro\'s revolution', 'the nuclear arms race and the missile gap', 'US Jupiter missiles in Turkey'], ['the failure of the Bay of Pigs invasion', 'Khrushchev\'s belief that Kennedy was weak after Vienna', 'Soviet missiles being shipped to Cuba'], 'the U-2 photographs of missile sites in October 1962'),
    ('the Berlin Blockade of 1948', ['disagreement over Germany since Potsdam', 'ideological rivalry between the USA and the USSR', 'Marshall Aid building up western Germany'], ['the merger of the western zones', 'plans for a West German state', 'the introduction of the Deutschmark'], 'the introduction of the Deutschmark in June 1948'),
    ('the US withdrawal from Vietnam', ['the failure of US tactics against guerrilla warfare', 'the weakness of the South Vietnamese government', 'the rising cost of the war'], ['the Tet Offensive', 'Cronkite\'s broadcast calling the war a stalemate', 'the shootings at Kent State'], 'Nixon\'s election in 1968 on a promise to end the war'),
]


def _other(r, items, n, exclude):
    pool = [x for c, x in items if c != exclude]
    return r.sample(pool, n)


def skills_topics(P_ALL, name_a, name_b, name_c, name_d, kw=None):
    """Four skills topics (describe / causation / sources / judgement) using the content packs P_ALL."""
    kw = kw or {}
    A = [(c, x) for c, P in P_ALL for x in P.get('a', [])]
    B = [(c, x) for c, P in P_ALL for x in P.get('b', [])]
    E = [(c, x, P) for c, P in P_ALL for x in P.get('c', [])]
    SR = [(c, s, P) for c, P in P_ALL for s in P.get('src', [])]
    pts = [(c, p) for c, (q, np, ps) in A for p in ps]
    rsn = [(c, x) for c, (q, rs) in B for x in rs]

    # ---------------- (a) technique
    ta = T(name_a, *kw.get('a', ()))
    build(ta, {'terms': COMMAND})

    @ta.add('C1', (1, 2, 3), 'mcq')
    def a_relevant(r, D):
        c, (q, np, ps) = r.choice(A)
        ok = r.choice(ps)
        ds = [p for _, p in r.sample([x for x in pts if x[0] != c], 3)]
        opts, a = mcq(r, ok, ds)
        return {'stem': f'A student is answering the question: “{q}” Which of these statements is relevant and would gain credit?', 'options': opts, 'answer': a,
                'key': 'Only this statement answers the question set; the others are accurate but about different topics, so they gain no credit. [1]', 'marks': 1, 'minutes': 1}

    @ta.add('C2', (1, 2, 3, 4), 'explain')
    def a_mark(r, D):
        c, (q, np, ps) = r.choice(A)
        k = r.choice([1, 2, 2, 3]) if D >= 2 else 1
        k = min(k, len(ps) - 1)
        used = r.sample(ps, k)
        filler = r.choice(['It was very important and affected a lot of people.', 'This was a big event in history.', 'There were lots of things that happened.'])
        irr = _other(r, pts, 1, c)[0] if r.random() < 0.5 else None
        ans_txt = ' '.join(_dot(p) for p in used) + ' ' + filler + (' ' + _dot(irr) if irr else '')
        rest = [p for p in ps if p not in used][:2]
        why = f'{k} relevant point{"s" if k > 1 else ""} with no further development; the general sentence' + (' and the point about a different topic gain' if irr else ' gains') + ' no credit'
        return {'stem': f'Here is a student\'s answer to the question “{q}” [4]: “{ans_txt}” Using the mark scheme (one mark per relevant point, a further mark for supporting detail), how many marks would you award? Explain your decision and suggest how the answer could be improved.',
                'answer': f'{k} mark{"s" if k > 1 else ""}: {why}. To improve, add further precise points such as: ' + ' '.join(_dot(p) for p in rest),
                'key': f'1 mark for the correct mark ({k}/4); 1 mark for explaining why the other sentences gain no credit; 1 mark for a valid improvement with accurate detail [3]', 'type': 'explain', 'marks': 3, 'minutes': 4}

    @ta.add('C3', (2, 3, 4), 'short')
    def a_write(r, D):
        c, (q, np, ps) = r.choice(A)
        lead = r.choice(['Practise your (a) technique.', 'Paper 1 (a)-style question.', 'Write a precise answer using accurate supporting detail.'])
        return {'stem': f'{lead} {q}', 'answer': ' '.join(_dot(p) for p in ps), 'key': a_key(ps), 'type': 'short', 'marks': 4, 'minutes': 5}

    @ta.add('C4', (2, 3, 4, 5), 'multi_step')
    def a_select(r, D):
        c, (q, np, ps) = r.choice(A)
        good = r.sample(ps, min(3, len(ps)))
        bad = _other(r, pts, 3 if D >= 3 else 2, c)
        allx = good + bad
        r.shuffle(allx)
        lab = 'PQRSTU'[:len(allx)]
        notes = ' '.join(f'{l}: {_dot(x)}' for l, x in zip(lab, allx))
        gl = [l for l, x in zip(lab, allx) if x in good]
        m = 6
        return {'stem': f'A student has made these notes to answer the question “{q}” {notes} (a) Identify which notes are relevant to the question. (b) Explain why the other notes would gain no credit. (c) Use the relevant notes to write a four-mark answer, adding supporting detail.',
                'answer': f'(a) {", ".join(gl)}. (b) The others are accurate but about different topics, so they do not answer the question. (c) ' + ' '.join(_dot(p) for p in ps),
                'key': f'(a) {", ".join(gl)} [1] (b) explanation of relevance [1] (c) {a_key(ps)}', 'type': 'multi_step', 'marks': m, 'minutes': 8}

    # ---------------- causation
    tb = T(name_b, *kw.get('b', ()))
    build(tb, {'terms': CAUSATION})

    @tb.add('C1', (1, 2, 3), 'mcq')
    def b_valid(r, D):
        c, (q, rs) = r.choice(B)
        ok = r.choice(rs)
        ds = [x for _, x in r.sample([y for y in rsn if y[0] != c], 3)]
        opts, a = mcq(r, ok, ds)
        return {'stem': f'Which of these is a valid reason in answer to the question: “{q}”', 'options': opts, 'answer': a,
                'key': 'Only this reason is relevant to the question; the others explain different events. [1]', 'marks': 1, 'minutes': 1}

    @tb.add('C2', (1, 2, 3, 4), 'explain')
    def b_level(r, D):
        c, (q, rs) = r.choice(B)
        lv = r.choice([1, 3, 4]) if D >= 2 else r.choice([1, 3])
        if lv == 1:
            txt = r.choice(['There were lots of reasons for this and they all mattered.', 'It happened because of the situation at the time and people\'s decisions.'])
            res = 'Level 1 (1 mark): a general answer with no specific reasons or knowledge'
        elif lv == 3:
            txt = _dot(r.choice(rs))
            res = 'Level 3 (4-5 marks): it explains one reason with accurate detail'
        else:
            txt = ' '.join(_dot(x) for x in r.sample(rs, 2))
            res = 'Level 4 (6 marks): it explains two reasons, each linked to the question'
        return {'stem': f'A student answered the question “{q}” [6] with: “{txt}” Using the levels (L1 general answer; L2 identifies or describes reasons; L3 explains one reason; L4 explains two reasons), which level does this answer reach? Explain your decision.',
                'answer': res + '.', 'key': '1 mark for the correct level; 1 mark for a justification referring to the level descriptors [2]', 'type': 'explain', 'marks': 2, 'minutes': 2.5}

    @tb.add('C3', (2, 3, 4, 5), 'case')
    def b_classify(r, D):
        ev, lng, sht, trig = r.choice(CAUSE_SETS)
        items = r.sample(lng, 2) + r.sample(sht, 2)
        r.shuffle(items)
        lab = 'WXYZ'
        stem = f'Here are four causes of {ev}: ' + ' '.join(f'{l}: {cap(x)}.' for l, x in zip(lab, items)) + ' (a) Classify each cause as long-term or short-term. [2]'
        ans = '(a) Long-term: ' + ', '.join(l for l, x in zip(lab, items) if x in lng) + '; short-term: ' + ', '.join(l for l, x in zip(lab, items) if x in sht) + '.'
        key = '(a) 2 marks all four correct; 1 mark for two or three correct [2]'
        m = 2
        if D >= 3:
            stem += f' (b) Explain how one long-term cause made {ev} more likely. [3]'
            ans += ' (b) An explained link from a long-term cause, showing how it created the conditions for the event.'
            key += ' (b) 1 mark for identifying the cause; up to 2 marks for explaining the link [3]'
            m = 5
        if D >= 4:
            stem += f' (c) What was the trigger of {ev}? [1]'
            ans += f' (c) {cap(trig)}.'
            key += f' (c) {cap(trig)} [1]'
            m = 6
        return {'stem': stem, 'answer': ans, 'key': key, 'type': 'case', 'marks': m, 'minutes': _mins(m)}

    @tb.add('C4', (2, 3, 4, 5), 'long')
    def b_rank(r, D):
        c, (q, rs) = r.choice(B)
        n = 2 if D <= 2 else 3
        rr = r.sample(rs, min(n, len(rs)))
        lab = 'PQR'[:len(rr)]
        stem = (f'Consider the question “{q}” Here are some reasons: ' + ' '.join(f'{l}: {_dot(x)}' for l, x in zip(lab, rr)) +
                ' Explain how each reason contributed, show how at least two of them were linked, and decide which was the most important. Justify your choice.')
        return {'stem': stem, 'answer': 'Explains each reason in turn; links, for example, how one reason made another more serious; reaches a judgement on the most important reason with criteria (e.g. which made the outcome certain, or which came first and caused the others).',
                'key': 'Level 1 (1-2): describes reasons. Level 2 (3-5): explains reasons separately. Level 3 (6-8): explains and links reasons. Level 4 (9-10): explains and links reasons and reaches a supported judgement on relative importance [10]',
                'type': 'long', 'marks': 10, 'minutes': 15}

    # ---------------- sources
    tc = T(name_c, *kw.get('c', ()))
    build(tc, {'terms': SOURCE_TERMS})

    @tc.add('C1', (1, 2, 3), 'mcq')
    def c_type(r, D):
        c, s, P = r.choice(SR)
        k = s.get('kind', 'primary')
        opts, a = mcq(r, f'{cap(k)} source', ['Primary source', 'Secondary source', 'Neither: it is only an opinion', 'It cannot be classified without knowing if it is true'])
        return {'stem': f'Source A is {s["prov"]}. What type of source is it?', 'options': opts, 'answer': a,
                'key': f'{cap(k)}: decided by when and by whom it was produced, not by whether it is accurate. [1]', 'marks': 1, 'minutes': 1}

    @tc.add('C2', (2, 3, 4), 'explain')
    def c_msg_purpose(r, D):
        c, s, P = r.choice(SR)
        return {'stem': f'{_src_intro(r, s, "A")} Explain the difference between the message of Source A and its purpose, using details of the source.',
                'answer': f'Message: {s["infer"]} Purpose: {s["purpose"]}',
                'key': '1 mark for a valid message supported by a detail; 1 mark for a valid purpose linked to the author, audience or date; up to 2 marks for explaining the difference (what it says vs why it was produced) [4]',
                'type': 'explain', 'marks': 4, 'minutes': 5}

    @tc.add('C3', (2, 3, 4, 5), 'case')
    def c_src(r, D):
        c, s, P = r.choice(SR)
        L = r.choice('ABCD')
        k = (1,) if D <= 2 else ((1, 2) if D == 3 else (2,))
        return _compose_src(r, 'Source skills practice. ' + _src_intro(r, s, L), _src_parts(s, L, P), CTX.get('want_marks'), k)

    @tc.add('C4', (3, 4, 5), 'case')
    def c_two(r, D):
        grp = {}
        for c, s, P in SR:
            if P.get('claim') and s.get('stance') is not None:
                grp.setdefault(id(P), (P, []))[1].append(s)
        P, ss = r.choice([v for v in grp.values() if len(v[1]) >= 2])
        a, b = r.sample(ss, 2)
        intro = 'Source skills practice: cross-referencing. ' + _src_intro(r, a, 'A', True) + ' ' + _src_intro(r, b, 'B', True)
        q = f'(a) What can you infer from each source about {P["enq"]}? [4] (b) How far do Sources A and B agree? [7] (c) Which source is more useful to a historian studying {P["enq"]}? Explain your answer using the provenance of both sources. [7]'
        ans = (f'(a) A: {a["infer"]} B: {b["infer"]} (b) ' + ('They broadly agree' if a['stance'] == b['stance'] else 'They disagree') +
               f' about whether {P["claim"]}. (c) A: {a["plus"]}; but {a["minus"]}. B: {b["plus"]}; but {b["minus"]}. Judgement depends on the enquiry; each is useful for different purposes.')
        key = '(a) 2 marks for each valid inference supported from the source [4] (b) ' + CMP_KEY + ' [7] (c) ' + USE_KEY + ' [7]'
        return {'stem': f'{intro} {q}', 'answer': ans, 'key': key, 'type': 'case', 'marks': 18, 'minutes': 27}

    # ---------------- judgement
    td = T(name_d, *kw.get('d', ()))
    build(td, {'terms': JUDGE_TERMS})

    @td.add('C1', (1, 2, 3), 'mcq')
    def d_best(r, D):
        c, e, P = r.choice(E)
        opts, a = mcq(r, _dot(e['judge']), GENERIC_JUDGE)
        q = e['q']
        return {'stem': f'Which of these is the best concluding judgement for the question: {q}', 'options': opts, 'answer': a,
                'key': 'The best judgement answers the question directly and gives a reason why one side outweighs the other; the others are vague or unsupported. [1]', 'marks': 1, 'minutes': 1}

    @td.add('C2', (1, 2, 3, 4), 'explain')
    def d_level(r, D):
        c, e, P = r.choice(E)
        lv = r.choice([3, 4, 5]) if D >= 2 else 3
        txt = ' '.join(_dot(x) for x in e['pro'][:2])
        res = 'Level 3 (4-6 marks): it explains one side of the argument only'
        if lv >= 4:
            txt += ' On the other hand, there are arguments against this. ' + ' '.join(_dot(x) for x in e['con'][:2])
            res = 'Level 4 (7-9 marks): it explains both sides but does not reach a judgement'
        if lv == 5:
            txt += ' In conclusion: ' + _dot(e['judge'])
            res = 'Level 5 (10 marks): it explains both sides and reaches a supported judgement'
        return {'stem': f'Read this student\'s answer to the question {e["q"]} “{txt}” Using the levels (L3 explains one side; L4 explains both sides; L5 explains both sides with a supported judgement), which level does it reach? Explain your decision.',
                'answer': res + '.', 'key': '1 mark for the correct level; 1 mark for a justification referring to the descriptors [2]', 'type': 'explain', 'marks': 2, 'minutes': 2.5}

    @td.add('C3', (2, 3, 4, 5), 'short')
    def d_counter(r, D):
        c, e, P = r.choice(E)
        n = 2 if D <= 3 else 3
        n = min(n, len(e['con']))
        return {'stem': f'A student is planning an answer to: {e["q"]} They have written these points in support: ' + ' '.join(_dot(x) for x in e['pro'][:2]) + f' Give {["", "one", "two", "three"][n]} explained counter-argument{"s" if n > 1 else ""} that the student could use.',
                'answer': ' '.join(_dot(x) for x in e['con'][:n]), 'key': f'2 marks for each explained counter-argument (1 if only identified), up to [{2 * n}]', 'type': 'short', 'marks': 2 * n, 'minutes': _mins(2 * n)}

    @td.add('C4', (2, 3, 4, 5), 'long')
    def d_essay(r, D):
        c, e, P = r.choice(E)
        lead = r.choice(['Plan and write a full answer.', 'Write an extended answer.', 'Paper 1 (c)-style question.'])
        return {'stem': lead + ' ' + _c_stem(r, e, P), 'answer': c_ans(e['pro'], e['con'], e['judge']), 'key': c_key(e['pro'], e['con'], e['judge']), 'type': 'long', 'marks': 10, 'minutes': 15}

    return [ta, tb, tc, td]


CHAPTERS[1] = skills_topics(packs(CHAPTERS),
                            'Knowledge and description: writing a precise (a) answer', 'Causation and consequence: explaining why events happened',
                            'Analysing sources: content, provenance, purpose and cross-referencing', "Reaching a judgement: 'How far' and 'Who was to blame' questions")
finalize(CHAPTERS)
