"""Cambridge International AS & A Level History 9489, AS Level (grade 11): the three AS options
(European: France 1774-1814, the Industrial Revolution in Britain, Liberalism and nationalism in
Italy and Germany; American: origins of the Civil War, Civil War and Reconstruction, the Gilded Age
and Progressive Era; International: empire and world powers 1870-1919, the League of Nations and
international relations in the 1920s and 1930s).

Paper 1 (Historical Sources) is a two-part source question on a set topic: (a) compare and contrast
two sources [15]; (b) 'How far do the sources support the view that ...?' (four sources, [25] in the
examination; the platform caps an item at 20 marks, so it is set on two to four sources and marked
out of 20 with the levels scaled). Paper 2 (Outline Study) questions are two-part: (a) 'Explain why
...' [10] and (b) 'To what extent / How far ...' [20], marked by levels.

Each topic is a knowledge pack (key terms, dated events, recall MCQs, 'Explain why' causes with a
judgement, essay prompts with arguments for and against, claims to check, and Paper 1 sources)
turned into items by the builders below. Sources are either well-attested words from the period
(quoted or summarised, marked as such) or labelled '(illustrative)' and attributed to unnamed
writers; no invented words are put into the mouth of a real person.
cambridge-g12-history imports these builders.
"""
import re as _re

from ._lib import mcq, CTX, person
from .g9_history import (S, T, cap, low, low2, _dot, _mins, _kw, add_terms, add_mcqs, add_claims, finalize, _markify, _year_ds)

PROFILE = {'mark_scale': {'short': (3, 2), 'long': (4, 1.5), 'case': (4, 1.5)}, 'wordy': True}
CHAPTERS = {}
LET = 'abcdefgh'

# ============================================================== mark schemes (9489 levels)

WHY_KEY = ('Level 4 (9-10): explains a range of causes and reaches a supported judgement about their relative importance or how they are linked. '
           'Level 3 (6-8): explains two or more causes; any judgement is undeveloped. Level 2 (3-5): describes or identifies causes, or explains only one. '
           'Level 1 (1-2): general, unsupported points.')
ESS_KEY = ('Level 5 (18-20): sustained analysis of both sides of the question, supported by precise evidence, with a well-substantiated judgement. '
           'Level 4 (15-17): developed analysis of both sides; a judgement is reached but is not fully supported. '
           'Level 3 (10-14): analysis of one side, or of both with limited development or accuracy. Level 2 (6-9): mainly descriptive, with implicit links to the question. '
           'Level 1 (1-5): general assertions with little accurate knowledge.')
CMP_KEY = ('Level 4 (12-15): compares and contrasts the sources, explaining similarities AND differences, and evaluates them using provenance and context to explain why they differ. '
           'Level 3 (8-11): explains similarities AND differences in content, supported by details from both sources. '
           'Level 2 (4-7): explains a similarity OR a difference. Level 1 (1-3): describes or paraphrases the content of the sources without valid comparison.')
SUP_KEY = ('Level 5 (17-20): evaluates the sources (provenance, purpose, context, cross-reference) to show how far they support AND challenge the view, reaching a supported judgement. '
           'Level 4 (13-16): uses the sources to support AND challenge the view and evaluates some of them. '
           'Level 3 (9-12): uses the sources at face value to support AND challenge. Level 2 (5-8): uses the sources to support OR challenge. '
           'Level 1 (1-4): writes about the topic without valid use of the sources. (The examination version uses four sources and 25 marks; levels are scaled.)')
REL_KEY = ('1 mark for a valid point about the content; up to 2 marks for using the provenance (author, date, purpose, audience) to judge reliability; '
           'up to 2 marks for cross-referencing with own knowledge; 1 mark for a supported overall judgement')
PURP_KEY = ('1 mark for identifying the purpose; up to 2 marks for explaining it with details of the source; up to 2 marks for setting it in the context of the date')


def why_key(rs, judge, k=None):
    return f'{k or WHY_KEY} Indicative content: ' + ' '.join(_dot(x) for x in rs) + ' Possible judgement: ' + _dot(judge) + ' [10]'


def why_ans(rs, judge):
    return ' '.join(_dot(x) for x in rs) + ' Judgement: ' + _dot(judge)


def ess_key(pro, con, judge, k=None):
    return (f'{k or ESS_KEY} Agree / supporting: ' + ' '.join(_dot(x) for x in pro) + ' Disagree / other factors: ' +
            ' '.join(_dot(x) for x in con) + ' Possible judgement: ' + _dot(judge) + ' [20]')


def ess_ans(pro, con, judge):
    return 'For: ' + ' '.join(_dot(x) for x in pro) + ' Against: ' + ' '.join(_dot(x) for x in con) + ' Judgement: ' + _dot(judge)


# names too general to tie a stimulus sentence to a question
_STIM_NAMES = {'napoleon', 'mussolini', 'stalin', 'hitler', 'league', 'reagan', 'carter', 'nixon', 'britain', 'president', 'germany', 'france'}


def _stim(r, P, q=None):
    st = [x for x in (P.get('stim') or []) if x]
    if q is not None:
        k = _kw(q) - _STIM_NAMES
        sc = [(len(_kw(x) & k), x) for x in st]
        best = max([n for n, _ in sc] + [0])
        st = [x for n, x in sc if n and n == best]
    return r.choice(st) if st else ''


def _essq(e, r=None):
    q = e['q']
    if q.startswith('‘') or q.startswith('“'):
        tail = ['How far do you agree?', 'How far do you agree with this view?', 'Discuss.'] if r else ['How far do you agree?']
        return q + ' ' + (r.choice(tail) if r else tail[0])
    return q


# ============================================================== dates (as g9_history.add_dates, but keys show the month when one is given)

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def _when(d):
    if len(d) < 3 or not d[2]:
        return str(d[1])
    m = int(d[2])
    day = int(round((d[2] - m) * 100))
    return (f'{day} ' if day else '') + f'{MONTHS[m - 1]} {d[1]}'


def add_dates(t, dates):
    """dates: [(clause, year[, month or month.day])] -> C1 year MCQs and C2 chronology items."""
    if not dates:
        return
    t.fixed('C1', (1, 2), [(f'In which year did this happen: {d[0]}?', str(d[1]), f'{cap(d[0])}: {_when(d)}. [1]', _year_ds(d[1])) for d in dates])
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
            stem += ' Then explain how one event in your sequence helped to cause a later one.'
            mk = 4
        ans = ', '.join(lab[i] for i in order) + ' (' + '; '.join(f'{lab[i]} {_when(ev[i])}' for i in order) + ')'
        key = f'Correct order {ans}: 2 marks if all correct, 1 mark if one adjacent pair is reversed.'
        if D >= 3:
            key += ' Up to 2 further marks for a valid, explained causal link between two of the events.'
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
                'key': f'{cap(ev[i][0])} ({_when(ev[i])}); ' + '; '.join(f'{low2(ev[j][0])} ({_when(ev[j])})' for j in o if j != i) + '. [1]', 'marks': 1, 'minutes': 1}
    t.add('C2', (1, 2, 3), 'mcq')(first)


# ============================================================== Paper 2 (a): 'Explain why' [10]

N_W = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}


def add_why(t, P, lead_full='Explain why', wkey=None):
    """P['why']: [(clause, [causes], judgement)]: 'Explain why <clause>.'"""
    wk = wkey or WHY_KEY
    W = P.get('why', [])
    for clause, rs, judge in W:
        def fi(r, D, clause=clause, rs=rs):
            k = 2 if D <= 2 else 3
            k = min(k, len(rs) - 1)
            lead = r.choice(['Identify', 'State', 'Give'])
            return {'stem': f'{lead} {N_W[k]} reasons why {clause}.', 'answer': ' '.join(_dot(x) for x in rs[:k]),
                    'key': f'1 mark for each, any {N_W[k]} from: ' + ' '.join(_dot(x) for x in rs) + f' [{k}]', 'type': 'short', 'marks': k, 'minutes': _mins(k)}
        fi.__name__ = 'identify'
        t.add('C1', (1, 2, 3), 'short')(fi)

        def fa(r, D, clause=clause, rs=rs, judge=judge):
            want = CTX.get('want_marks') or 10
            if D <= 2 and want <= 4:
                m = 2 if want <= 2 else 4
                return {'stem': f'Explain {"one reason" if m == 2 else "two reasons"} why {clause}.', 'answer': ' '.join(_dot(x) for x in rs[:m // 2]),
                        'key': f'For each reason: 1 mark for identifying it and 1 mark for explaining it with supporting detail, from: ' + ' '.join(_dot(x) for x in rs) + f' [{m}]',
                        'type': 'explain', 'marks': m, 'minutes': _mins(m)}
            s = _stim(r, P, clause) if r.random() < 0.6 else ''
            return {'stem': (s + ' ' + f'{lead_full} {clause}.').strip(), 'answer': why_ans(rs, judge), 'key': why_key(rs, judge, wk),
                    'type': 'explain', 'marks': 10, 'minutes': 15}
        fa.__name__ = 'explain_why'
        t.add('C2', (2, 3, 4), 'explain')(fa)

        def frank(r, D, clause=clause, rs=rs, judge=judge):
            if len(rs) < 3:
                return None
            k = 3 if D <= 3 else min(4, len(rs))
            pick = r.sample(rs, k)
            lab = 'ABCD'[:k]
            want = CTX.get('want_marks') or 6
            m = 10 if (want >= 8 or D >= 5) else 6
            lead = r.choice([f'Historians have offered several reasons why {clause}.', f'A revision guide lists these reasons why {clause}.',
                             f'Consider the following explanations of why {clause}.'])
            stem = lead + ' ' + ' '.join(f'{lab[i]}: {cap(pick[i])}.' for i in range(k)) + \
                r.choice([' Explain which of these was the most important reason.', ' Which was the most significant? Explain your answer with reference to the other reasons.',
                          ' Explain how these reasons were linked and decide which mattered most.'])
            key = (f'{wk} Here: up to 4 marks for explaining the chosen reason, up to 4 for explaining the others in relation to it, up to 2 for a supported judgement of relative importance [10]'
                   if m == 10 else '1 mark for a choice; up to 3 marks for explaining it with precise detail; up to 2 marks for comparing it with the other reasons [6]')
            return {'stem': stem, 'answer': 'Any reasoned choice. ' + ' '.join(f'{lab[i]}: {_dot(pick[i])}' for i in range(k)) + ' Possible judgement: ' + _dot(judge),
                    'key': key, 'type': 'explain', 'marks': m, 'minutes': _mins(m)}
        frank.__name__ = 'rank'
        t.add('C3', (2, 3, 4, 5), 'explain')(frank)


# ============================================================== Paper 2 (b): essays [20]

def add_as_essays(t, P, ekey=None):
    """P['ess']: [dict(q, pro, con, judge[, hints])]."""
    for e in P.get('ess', []):
        def fc(r, D, e=e):
            if D <= 2:
                q = e['q'].strip('‘’“”').rstrip('.?')
                stem = (f'Consider this view: “{q}.” Explain one argument that supports it and one that challenges it.' if e['q'][0] in '‘“'
                        else f'{q}? Explain one argument on each side of the question.')
                return {'stem': stem, 'answer': ess_ans(e['pro'][:1], e['con'][:1], e['judge']),
                        'key': '2 marks for an explained argument in support; 2 marks for an explained argument against (1 mark each if only identified) [4]',
                        'type': 'long', 'marks': 4, 'minutes': 6}
            stem = _essq(e, r)
            if r.random() < 0.4:
                s = _stim(r, P, e['q'])
                stem = (s + ' ' + stem).strip()
            if e.get('hints') and r.random() < 0.5:
                hs = r.sample(list(e['hints']), min(len(e['hints']), r.choice([2, 3])))
                stem += ' In your answer you may wish to consider: ' + '; '.join(hs) + '.'
            return {'stem': stem, 'answer': ess_ans(e['pro'], e['con'], e['judge']), 'key': ess_key(e['pro'], e['con'], e['judge'], ekey),
                    'type': 'long', 'marks': 20, 'minutes': 30}
        fc.__name__ = 'essay'
        t.add('C4', (2, 3, 4, 5), 'long')(fc)

        def fplan(r, D, e=e):
            n = 2 if D <= 3 else 3
            n = min(n, len(e['pro']), len(e['con']))
            m = 2 + 2 * n
            who = person(r)
            stem = (f'{who} is planning an answer to the question: “{_essq(e)}” Write a one-sentence line of argument for the answer and outline '
                    f'{N_W[n]} points {who} could use to support the view and {N_W[n]} to challenge it.')
            return {'stem': stem, 'answer': 'Line of argument: ' + _dot(e['judge']) + ' Support: ' + ' '.join(_dot(x) for x in e['pro'][:n]) + ' Challenge: ' + ' '.join(_dot(x) for x in e['con'][:n]),
                    'key': f'2 marks for a line of argument that answers the question directly and is sustainable; 1 mark for each relevant supporting point and 1 for each challenging point [{m}]',
                    'type': 'short', 'marks': m, 'minutes': _mins(m)}
        fplan.__name__ = 'plan'
        t.add('C3', (2, 3, 4, 5), 'short')(fplan)

        def fjudge(r, D, e=e):
            who = person(r)
            crit = r.choice((e['con'][1:] + e['pro'][1:]) or e['con'])
            return {'stem': f'{who} ends an essay on “{_essq(e)}” with this conclusion: “{cap(e["judge"])}.” Explain one piece of evidence that supports this conclusion and one point a critic could make against it.',
                    'answer': f'Evidence the conclusion rests on (either strand of the judgement), for example: {_dot(e["pro"][0])} / {_dot(e["con"][0])} '
                              f'Possible criticism: the conclusion may underplay the point that {low2(_dot(crit))}',
                    'key': '1 mark for relevant supporting evidence and 1 mark for explaining how it supports the judgement; 1 mark for a valid counter-point and 1 mark for developing it [4]',
                    'type': 'explain', 'marks': 4, 'minutes': 5}
        fjudge.__name__ = 'judge'
        t.add('C2', (2, 3, 4), 'explain')(fjudge)


# ============================================================== Paper 1: sources

def _intro(r, s, L, multi=False):
    q = s['text'] if s.get('visual') else f'“{s["text"]}”'
    if multi:
        return f'Source {L}: {s["prov"]}. {q}'
    return r.choice([f'Study Source {L}. Source {L}: {s["prov"]}. {q}', f'Source {L} is {s["prov"]}. {q} Study the source.',
                     f'Read Source {L}. {q} ({cap(s["prov"])}.)'])


def add_as_sources(t, P):
    srcs = P.get('src', [])
    enq, claim = P.get('enq', 'this topic'), P.get('claim')
    for s in srcs:
        def f2(r, D, s=s):
            L = r.choice('ABCD')
            det = _re.split(r'(?<=[.!?…])\s', s['text'])[0].rstrip('.')
            det = (f'“{det}”' if not s.get('visual') else low(det)) if len(det) < 160 else 'a relevant quotation or feature of the source'
            if (CTX.get('want_marks') or 0) >= 4 and D >= 2:
                q = r.choice([f'What can you learn from Source {L} about {s["about"]}? Support your answer with details from the source.',
                              f'What does Source {L} reveal about {s["about"]}? Use details of the source to support your answer.'])
                return {'stem': _intro(r, s, L) + ' ' + q, 'answer': s['infer'] + f' Supporting details: for example, {det}; each detail should be linked to an inference.',
                        'key': '1 mark for each valid inference and 1 mark for each supporting detail from the source [4]', 'type': 'short', 'marks': 4, 'minutes': 5}
            q = r.choice([f'What can you infer from Source {L} about {s["about"]}? Support your answer with a detail from the source.',
                          f'Give one thing Source {L} suggests about {s["about"]} and a detail from the source that shows it.'])
            return {'stem': _intro(r, s, L) + ' ' + q, 'answer': s['infer'] + f' Supporting detail: for example, {det}.',
                    'key': '1 mark for a valid inference; 1 mark for a supporting detail from the source [2]', 'type': 'short', 'marks': 2, 'minutes': 2.5}
        f2.__name__ = 'source2'
        t.add('C3', (1, 2, 3), 'short')(f2)

        def frel(r, D, s=s):
            L = r.choice('ABCD')
            which = r.random() < 0.5 or s.get('kind') == 'secondary'
            if which:
                q = r.choice([f'How reliable is Source {L} as evidence about {s["about"]}? Use the provenance of the source and your own knowledge.',
                              f'Assess the reliability of Source {L} as evidence about {s["about"]}.'])
                ans = f'Reliable because {low2(s["plus"])}. Less reliable because {low2(s["minus"])}. Cross-reference: {_dot(s["missing"])} Judgement: reliable as evidence of this point of view, but it needs to be tested against other evidence.'
                return {'stem': _intro(r, s, L) + ' ' + q, 'answer': ans, 'key': REL_KEY + ' [6]', 'type': 'case', 'marks': 6, 'minutes': 8}
            q = r.choice([f'Why do you think Source {L} was {"published" if s.get("published", True) else "written"}? Use details of the source and your knowledge of the context.',
                          f'Explain the purpose of Source {L}. Use the source and your own knowledge.'])
            ans = s['purpose'] + (' Context: ' + s['context'] if s.get('context') else '') + f' Detail: {s["infer"]}'
            return {'stem': _intro(r, s, L) + ' ' + q, 'answer': ans, 'key': PURP_KEY + ' [5]', 'type': 'case', 'marks': 5, 'minutes': 7}
        frel.__name__ = 'reliability'
        t.add('C3', (2, 3, 4), 'case')(frel)

        if claim and s.get('stance') is not None:
            def fsup(r, D, s=s):
                L = r.choice('ABCD')
                sup = ('Supports: ' if s['stance'] else 'Challenges: ') + s.get('why', s['infer'])
                return {'stem': _intro(r, s, L) + f' Does Source {L} support the view that {claim}? Explain your answer using the source and your own knowledge.',
                        'answer': sup + f' However, {low2(s["minus"])}.',
                        'key': '1 mark for a valid judgement; up to 2 marks for details of the source used to support it; up to 2 marks for evaluating the source (provenance or own knowledge) [5]',
                        'type': 'case', 'marks': 5, 'minutes': 7}
            fsup.__name__ = 'support1'
            t.add('C3', (2, 3, 4, 5), 'case')(fsup)

    if len(srcs) >= 2:
        def cmp15(r, D):
            a, b = r.sample(srcs, 2)
            la, lb = r.choice([('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'C'), ('B', 'D')])
            q = r.choice([f'Compare and contrast Sources {la} and {lb} as evidence about {enq}.', f'Compare and contrast the views of Sources {la} and {lb} on {enq}.',
                          f'To what extent do Sources {la} and {lb} agree about {enq}?'])
            if (CTX.get('want_marks') or 15) <= 8 and D <= 3:
                return {'stem': f'Study Sources {la} and {lb}. {_intro(r, a, la, True)} {_intro(r, b, lb, True)} Identify one similarity and one difference between Sources {la} and {lb} on {enq}.',
                        'answer': f'Source {la}: {a["infer"]} Source {lb}: {b["infer"]} A similarity and a difference must each be supported by details from both sources.',
                        'key': '1 mark for a similarity and 1 for supporting it from both sources; 1 mark for a difference and 1 for supporting it from both sources [4]', 'type': 'case', 'marks': 4, 'minutes': 6}
            if a.get('stance') is not None and b.get('stance') is not None and claim:
                rel = ('Both ' + ('support' if a['stance'] else 'challenge') + f' the view that {claim}' if a['stance'] == b['stance']
                       else f'They disagree about whether {claim}')
            else:
                rel = f'They should be compared on what each says about {enq}'
            ans = (f'Source {la}: {a["infer"]} Source {lb}: {b["infer"]} {rel}; similarities and differences should be supported with details. '
                   f'Provenance: {la} is {a["prov"]} ({low2(a["minus"])}); {lb} is {b["prov"]} ({low2(b["minus"])}). Differences in authorship, date and purpose explain the contrast.')
            return {'stem': f'Study Sources {la} and {lb}. {_intro(r, a, la, True)} {_intro(r, b, lb, True)} {q}', 'answer': ans, 'key': CMP_KEY + ' [15]',
                    'type': 'case', 'marks': 15, 'minutes': 22}
        cmp15.__name__ = 'compare'
        t.add('C3', (3, 4, 5), 'case')(cmp15)
        t.add('C4', (3, 4, 5), 'case')(cmp15)

    st = [s for s in srcs if s.get('stance') is not None]
    if claim and len(st) >= 2:
        def howfar(r, D):
            n = min(len(st), 4 if D >= 4 else 3, max(2, len(st)))
            ss = r.sample(st, n)
            labs = 'ABCD'[:n]
            intro = r.choice(['Study all the sources.', 'Read the sources carefully.', f'Study Sources {labs[0]} to {labs[-1]}.' if n > 2 else 'Study Sources A and B.']) + ' ' + ' '.join(_intro(r, s, L, True) for s, L in zip(ss, labs))
            names = ', '.join(labs[:-1]) + ' and ' + labs[-1] if n > 2 else f'{labs[0]} and {labs[1]}'
            q = r.choice([f'How far do Sources {names} support the view that {claim}?', f'“{cap(claim)}.” How far do Sources {names} support this view?'])
            sup = [L for s, L in zip(ss, labs) if s['stance']]
            ch = [L for s, L in zip(ss, labs) if not s['stance']]
            ans = ' '.join(f'Source {L} ' + ('supports' if s['stance'] else 'challenges') + f': {_dot(s.get("why", s["infer"]))} Evaluation: {s["minus"]}.' for s, L in zip(ss, labs))
            ans += (f' Grouping: support {", ".join(sup) or "none"}; challenge {", ".join(ch) or "none"}. A judgement must weigh how convincing each group is, '
                    'using provenance and own knowledge, rather than counting sources.')
            return {'stem': f'{intro} {q}', 'answer': ans, 'key': SUP_KEY + ' [20]', 'type': 'case', 'marks': 20, 'minutes': 30}
        howfar.__name__ = 'howfar'
        t.add('C4', (3, 4, 5), 'case')(howfar)


def build_as(t, P):
    start = len(t.templates)
    add_terms(t, P.get('terms', []))
    add_dates(t, P.get('dates', []))
    add_mcqs(t, P.get('mcq', []))
    add_why(t, P)
    add_claims(t, P.get('claims', []))
    add_as_essays(t, P)
    add_as_sources(t, P)
    _markify(t, start)
    t.pack = P
    return t


# ============================================================== CHAPTER 1: European option, France 1774-1814

f1a = T('Causes of the French Revolution of 1789: the ancien régime, finance and the Enlightenment', 'causes of the french revolution', 'ancien régime', 'enlightenment')
build_as(f1a, {
    'enq': 'the causes of the French Revolution', 'claim': 'the French Revolution was caused mainly by the financial crisis of the monarchy',
    'stim': ['By 1788 interest payments on the French royal debt took about half of government spending.', 'In August 1788 Louis XVI agreed to summon the Estates-General for May 1789.',
             'The harvest of 1788 was poor and bread prices in Paris reached their highest level of the century in the summer of 1789.'],
    'terms': [
        ('ancien régime', 'the social and political system of France before 1789, based on absolute monarchy and the privileges of the First and Second Estates'),
        ('Estates-General', 'the assembly of representatives of the clergy, nobility and Third Estate, which had not met since 1614'),
        ('taille', 'the main direct tax of the ancien régime, from which the nobility and clergy were largely exempt'),
        ('philosophes', 'writers of the French Enlightenment, such as Voltaire, Montesquieu and Rousseau, who applied reason to criticise existing institutions'),
        ('cahiers de doléances', 'lists of grievances drawn up by each estate and community in 1789 for the Estates-General'),
        ('Assembly of Notables', 'a gathering of leading nobles and clergy called by Calonne in 1787, which refused to approve his reforms of taxation'),
        ('Tennis Court Oath', 'the pledge of the deputies of the National Assembly on 20 June 1789 not to separate until France had a constitution'),
    ],
    'dates': [('Louis XVI became king', 1774, 5), ('France formally allied with the American colonists against Britain', 1778, 2), ('Necker published the Compte rendu', 1781, 2),
              ('the Assembly of Notables met', 1787, 2), ('the Estates-General opened at Versailles', 1789, 5.05), ('the Bastille was stormed', 1789, 7.14)],
    'mcq': [
        ('Which minister presented the king\'s finances as healthy in the Compte rendu au roi of 1781?', 'Necker', ['Calonne', 'Turgot', 'Brienne'], 'Necker\'s published account hid the cost of the American war. [1]'),
        ('Which war added most to the French royal debt in the years before 1789?', 'The War of American Independence', ['The Seven Years\' War', 'The War of the Austrian Succession', 'The Napoleonic Wars'], 'France\'s intervention, 1778-83, was financed mainly by loans. [1]'),
        ('Why did the deputies of the Third Estate object to voting by order in 1789?', 'The two privileged orders could always outvote them, two votes to one', ['They wanted the king to decide every question', 'They had fewer deputies than the clergy', 'They wanted voting to take place in secret'], 'Doubling the Third Estate meant little unless votes were counted by head. [1]'),
        ('Which Enlightenment writer argued for the separation of powers in The Spirit of the Laws?', 'Montesquieu', ['Rousseau', 'Voltaire', 'Diderot'], 'Published in 1748. [1]'),
    ],
    'why': [
        ('the French monarchy faced bankruptcy by 1787', ['The cost of wars, especially the American war of 1778-83, was paid for by borrowing', 'Interest on the debt took a growing share of revenue',
                                                           'The privileged orders were largely exempt from direct taxes, so the tax base was narrow', 'Tax collection through tax farmers was inefficient and corrupt',
                                                           'The parlements blocked attempts at reform'],
         'the underlying problem was the privileged tax system, which made it impossible to pay for the wars without crisis'),
        ('Louis XVI agreed to call the Estates-General in 1788', ['The Assembly of Notables refused to approve Calonne\'s land tax in 1787', 'The Parlement of Paris declared that only the Estates-General could consent to new taxes',
                                                                  'The aristocratic revolt of 1788 and riots such as the Day of the Tiles in Grenoble showed resistance to royal authority', 'The treasury suspended payments in August 1788, so the crown had no other way to raise money'],
         'the crown ran out of credit and the privileged orders refused reform, so the king had no alternative'),
        ('the Third Estate declared itself the National Assembly in June 1789', ['The dispute over voting by order or by head deadlocked the Estates-General', 'Pamphlets such as Sieyès\'s What is the Third Estate? encouraged deputies to claim to represent the nation',
                                                                                 'Some clergy joined the Third Estate, strengthening its claim', 'The king\'s failure to give a clear lead allowed the deputies to take the initiative'],
         'the voting deadlock was the immediate trigger, but Enlightenment ideas of popular sovereignty gave the deputies the confidence to act'),
    ],
    'claims': [
        ('The nobility and clergy paid little or no taille under the ancien régime.', True, 'The privileged orders were largely exempt from the taille, which fell mainly on the peasantry.'),
        ('The Estates-General met every few years throughout the eighteenth century.', False, 'It had not met since 1614 until it was summoned for 1789.'),
        ('Rousseau\'s idea of the general will influenced radical revolutionaries.', True, 'His Social Contract (1762) was widely cited by radicals such as Robespierre.'),
    ],
    'ess': [
        dict(q='‘The French Revolution was caused mainly by the financial crisis of the monarchy.’',
             pro=['Bankruptcy forced the crown to call the Estates-General, the event that opened the revolution', 'Calonne\'s and Brienne\'s failed reforms showed the crisis could not be solved within the old system',
                  'The cost of the American war made the debt unmanageable'],
             con=['Enlightenment ideas undermined belief in absolute monarchy and privilege', 'Resentment of privilege by the bourgeoisie and peasantry created social tension', 'Poor harvests and high bread prices in 1788-89 brought ordinary people into action',
                  'Louis XVI\'s weak and indecisive leadership turned a crisis into a revolution'],
             judge='the financial crisis was the trigger that made change unavoidable, but it became a revolution because of long-term resentment of privilege and new ideas about sovereignty',
             hints=['the royal debt', 'the Enlightenment', 'social grievances', 'the role of Louis XVI']),
        dict(q='How far was Louis XVI responsible for the outbreak of revolution in 1789?',
             pro=['He failed to support reforming ministers such as Turgot and Calonne', 'He hesitated over the voting dispute and then appeared to threaten the Assembly with troops', 'His dismissal of Necker in July 1789 provoked the Paris rising'],
             con=['He inherited a debt and a tax system created by earlier kings', 'The privileged orders and parlements blocked reform', 'Economic crisis and harvest failure were beyond his control'],
             judge='Louis did not cause the crisis, but his indecision at key moments turned a financial crisis into a political revolution'),
        dict(q='To what extent did the Enlightenment cause the French Revolution?',
             pro=['It spread criticism of absolutism, privilege and the Church', 'Ideas of popular sovereignty and natural rights shaped the demands of 1789', 'The American Revolution showed Enlightenment ideas in action'],
             con=['Most philosophes favoured reform, not revolution', 'Financial bankruptcy forced the calling of the Estates-General', 'Peasants and urban workers acted mainly because of hunger and feudal dues'],
             judge='the Enlightenment shaped how the crisis was understood and what the revolutionaries demanded, but it did not by itself cause the collapse of royal authority'),
    ],
    'src': [
        S('a pamphlet by the Abbé Sieyès, What is the Third Estate?, January 1789 (abridged)', 'What is the Third Estate? Everything. What has it been until now in the political order? Nothing. What does it ask? To become something.',
          'the political aims of the Third Estate', 'Sieyès argues that the Third Estate is the real nation but has been excluded from political power.',
          'To persuade readers that the Third Estate should have real power in the Estates-General.', 'it is a famous and influential pamphlet of the time', 'it is a piece of political propaganda written to win support',
          'It does not explain the role of the royal bankruptcy in calling the Estates-General.', stance=False, why='it presents the revolution as a demand for political rights rather than a response to bankruptcy',
          context='The Estates-General was due to meet in May 1789 and the method of voting was undecided.'),
        S('a report to the king by his finance minister, 1787 (illustrative)', 'The debt grows each year; the loans of the last war must be paid; the revenues are pledged in advance. Without a tax that falls on all landowners, without exception, the state cannot continue.',
          'the royal finances in 1787', 'It suggests the crown was close to bankruptcy and that taxing the privileged was the only solution.',
          'To persuade the king to support a general land tax.', 'it comes from inside the government and shows how ministers saw the crisis', 'a minister had reasons to exaggerate the crisis to win support for his plan',
          'It does not show how the privileged orders responded to the proposals.', stance=True, why='it shows bankruptcy as the central problem facing the monarchy'),
        S('a cahier de doléances of a rural parish, spring 1789 (illustrative)', 'We pay the taille, the tithe and the dues of the lord, while those who own the most pay least. We ask that all subjects bear taxes equally and that the lord\'s rights over our harvest be abolished.',
          'the grievances of the peasantry', 'It shows peasants resented unequal taxation and feudal dues.',
          'To set out the grievances of the parish for the Estates-General.', 'cahiers were written at the time by the communities themselves', 'they were often drafted by local lawyers and may not reflect every villager\'s view',
          'It does not mention the influence of Enlightenment writers.', stance=False, why='it shows that social grievances about privilege, not only state finance, drove demands for change'),
    ],
})

f1b = T('Why the revolution became more radical, 1789-95: war, the sans-culottes and the Terror', 'more radical', 'sans-culottes', 'terror')
build_as(f1b, {
    'enq': 'the radicalisation of the revolution', 'claim': 'war was the main reason for the radicalisation of the revolution',
    'stim': ['France declared war on Austria in April 1792.', 'On 10 August 1792 crowds of sans-culottes and National Guards stormed the Tuileries palace.',
             'Between September 1793 and July 1794 about 17,000 people were officially executed in France.'],
    'terms': [
        ('sans-culottes', 'radical Parisian artisans, shopkeepers and workers who wore trousers rather than the knee-breeches of the wealthy'),
        ('Jacobins', 'members of the radical political club that dominated the Convention in 1793-94 under Robespierre'),
        ('Girondins', 'a group of deputies who led France into war in 1792 and were purged from the Convention in June 1793'),
        ('Committee of Public Safety', 'the twelve-member committee that ran the revolutionary government during the Terror'),
        ('levée en masse', 'the decree of August 1793 that conscripted the whole nation for the war effort'),
        ('Law of Suspects', 'the law of September 1793 allowing the arrest of anyone suspected of opposing the revolution'),
        ('Thermidor', 'the coup of July 1794 that overthrew and executed Robespierre'),
    ],
    'dates': [('the royal family attempted to flee and was stopped at Varennes', 1791, 6), ('France declared war on Austria', 1792, 4), ('the monarchy was overthrown in Paris', 1792, 8),
              ('Louis XVI was executed', 1793, 1), ('the Law of Suspects was passed', 1793, 9), ('Robespierre was overthrown in the coup of Thermidor', 1794, 7)],
    'mcq': [
        ('What did the Brunswick Manifesto of July 1792 threaten?', 'The destruction of Paris if the royal family was harmed', ['The invasion of Britain', 'The end of the Civil Constitution of the Clergy', 'The return of the Estates-General'], 'Issued by the Prussian commander; it provoked the attack on the Tuileries. [1]'),
        ('Which revolt in western France began in March 1793 against conscription?', 'The rising in the Vendée', ['The Réveillon riots', 'The Great Fear', 'The Day of the Tiles'], '[1]'),
        ('What did the Civil Constitution of the Clergy (1790) require?', 'That priests be elected and swear an oath to the constitution', ['That priests be appointed by the pope alone', 'That the Church pay the taille', 'That all monasteries be expanded'], 'About half of the clergy refused the oath. [1]'),
        ('Which measure of 1793 fixed maximum prices for grain and other goods?', 'The Law of the Maximum', ['The Le Chapelier Law', 'The Concordat', 'The Law of 22 Prairial'], 'The General Maximum was passed in September 1793. [1]'),
    ],
    'why': [
        ('the monarchy was overthrown in August 1792', ['The flight to Varennes in 1791 destroyed trust in Louis XVI', 'The king vetoed decrees against refractory priests and émigrés', 'War with Austria and Prussia made the king look like a traitor',
                                                        'The Brunswick Manifesto threatened Paris and provoked the sans-culottes', 'Radical clubs and sections organised the attack on the Tuileries'],
         'war turned distrust of the king into fear of treason, which made the sans-culottes act'),
        ('the Terror was introduced in 1793', ['France faced foreign invasion and military defeat', 'Civil war in the Vendée and federalist revolts threatened the Republic', 'Food shortages and inflation of the assignat fuelled sans-culotte pressure',
                                                'The Jacobins needed sans-culotte support against the Girondins', 'Revolutionary leaders believed terror was needed to defend virtue and the Republic'],
         'the Terror began as an emergency response to war and civil war, but it was driven forward by sans-culotte pressure and Jacobin ideology'),
        ('Robespierre fell from power in July 1794', ['Military victory at Fleurus in June 1794 removed the case for emergency rule', 'The Law of 22 Prairial and the Great Terror made deputies fear for their own lives',
                                                       'Robespierre had alienated both the Hébertists and Dantonists by executing their leaders', 'His speech of 8 Thermidor threatened unnamed enemies in the Convention'],
         'once the military emergency was over, fear among the deputies themselves made it possible to unite against him'),
    ],
    'claims': [
        ('Louis XVI was executed before France went to war with Austria.', False, 'War began in April 1792; Louis was executed in January 1793.'),
        ('The Committee of Public Safety was set up in April 1793.', True, 'Robespierre joined it in July 1793.'),
        ('The Terror ended immediately when France declared war in 1792.', False, 'The Terror was introduced in 1793 because of the war and ended after Thermidor in 1794.'),
    ],
    'ess': [
        dict(q='‘War was the main reason why the revolution became more radical between 1792 and 1794.’',
             pro=['War made the king appear a traitor and led to the overthrow of the monarchy', 'Defeats and invasion in 1793 justified emergency measures such as the Committee of Public Safety', 'Conscription provoked the Vendée revolt, which led to brutal repression'],
             con=['The king\'s own actions, such as the flight to Varennes, undermined constitutional monarchy before war began', 'Economic crisis and sans-culotte pressure forced measures like the Maximum', 'Jacobin ideology and the politics of faction drove the Great Terror after the military crisis had eased'],
             judge='war was the main catalyst because it linked opposition to treason, but radicalisation also depended on the failure of the king and on sans-culotte pressure'),
        dict(q='To what extent did the sans-culottes control the course of the revolution in 1792-94?',
             pro=['They stormed the Tuileries in August 1792', 'Their rising of 2 June 1793 forced the purge of the Girondins', 'Their pressure in September 1793 brought the Maximum and put Terror on the agenda'],
             con=['The Jacobin leadership used them and then curbed them, executing the Hébertists in March 1794', 'The Committee of Public Safety centralised power from late 1793', 'They had little influence on war strategy or the coup of Thermidor'],
             judge='the sans-culottes drove key turning points in 1792-93, but from late 1793 the revolutionary government controlled and then suppressed them'),
        dict(q='How far was the Terror a response to the circumstances of 1793?',
             pro=['Foreign invasion, civil war and federalist revolts threatened the Republic', 'Emergency measures such as the levée en masse and the Law of Suspects followed military crisis'],
             con=['The Terror intensified after the military situation improved, with the Law of 22 Prairial in June 1794', 'Ideas of virtue and the general will justified purging enemies', 'Factional rivalry led to the execution of Hébertists and Dantonists'],
             judge='the Terror began as a response to circumstances, but its peak in 1794 owed more to ideology and factional politics'),
    ],
    'src': [
        S('a speech by Robespierre to the National Convention, February 1794 (translated, abridged)', 'If the spring of popular government in time of peace is virtue, the spring of popular government in revolution is at once virtue and terror: virtue, without which terror is fatal; terror, without which virtue is powerless.',
          'the justification of the Terror', 'Robespierre argues that terror is necessary in a revolution to protect virtue and the Republic.',
          'To justify the Terror to the Convention and defend the revolutionary government.', 'it shows directly how the leading member of the Committee of Public Safety justified the Terror', 'it is a political speech intended to justify policy, not to describe its effects',
          'It does not mention the war, which was already turning in France\'s favour.', stance=False, why='it justifies the Terror by ideology (virtue) rather than by the war',
          context='The Republic had survived the crises of 1793 but the Committee was about to move against rival factions.'),
        S('a letter from a deputy on mission in the Vendée, 1793 (illustrative)', 'The rebels are everywhere; the frontiers are threatened and traitors in our own towns give help to the enemy. Only the severest measures will save the Republic.',
          'conditions in 1793', 'It suggests that rebellion and the threat of invasion led revolutionaries to demand harsh measures.',
          'To report on the rebellion and justify harsh action to the government in Paris.', 'it was written at the time by someone who saw the civil war', 'a representative on mission had reasons to exaggerate the danger to justify his own actions',
          'It does not show the scale of the repression in the Vendée.', stance=True, why='it links the demand for terror directly to war and rebellion'),
        S('a petition from a Paris section to the Convention, September 1793 (illustrative)', 'The people are hungry while hoarders grow rich. We demand a maximum on the price of bread and that suspects be arrested. Make terror the order of the day!',
          'the demands of the sans-culottes', 'It shows the sans-culottes demanding price controls and terror against enemies.',
          'To pressure the Convention into adopting economic controls and repression.', 'petitions from the sections reflect the demands of the Parisian crowd at the time', 'it represents the most militant sections and may not speak for all Parisians',
          'It does not show how far the Jacobins shared or merely used these demands.', stance=False, why='it suggests popular pressure over food and hoarding, not just the war, drove the Terror'),
    ],
})

f1c = T('The Directory and the rise of Napoleon Bonaparte, 1795-99', 'directory', 'rise of napoleon')
build_as(f1c, {
    'enq': 'the rise of Napoleon Bonaparte', 'claim': 'Napoleon came to power mainly because of the weakness of the Directory',
    'stim': ['The Constitution of the Year III (1795) created a two-chamber legislature and an executive of five Directors.', 'In 1796-97 Bonaparte won a series of victories in northern Italy.',
             'On 18-19 Brumaire (9-10 November 1799) Bonaparte took part in a coup against the Directory.'],
    'terms': [
        ('Directory', 'the five-man executive that governed France from 1795 to 1799'),
        ('Brumaire', 'the coup of November 1799 that overthrew the Directory and brought Napoleon to power as First Consul'),
        ('Vendémiaire', 'the royalist rising in Paris in October 1795, put down by troops under Bonaparte'),
        ('coup of Fructidor', 'the purge of September 1797 in which the Directory used the army to annul royalist election victories'),
        ('Consulate', 'the government of France from 1799 to 1804, headed by three consuls with Bonaparte as First Consul'),
        ('Conspiracy of Equals', 'the plot led by Babeuf in 1796 to overthrow the Directory and create a more equal society'),
    ],
    'dates': [('the Directory was established', 1795, 11), ('Bonaparte put down the royalist rising of Vendémiaire', 1795, 10), ('Bonaparte signed the Treaty of Campo Formio with Austria', 1797, 10),
              ('the French fleet was destroyed at the Battle of the Nile', 1798, 8), ('Bonaparte seized power in the coup of Brumaire', 1799, 11)],
    'mcq': [
        ('Which Director was the main organiser of the coup of Brumaire?', 'Sieyès', ['Barras', 'Carnot', 'Talleyrand'], 'Sieyès wanted a stronger executive and used Bonaparte as the "sword". [1]'),
        ('Where did Bonaparte win his reputation in 1796-97?', 'Northern Italy', ['Egypt', 'The Netherlands', 'Spain'], 'Victories such as Lodi, Arcole and Rivoli. [1]'),
        ('How did the Directory respond to royalist gains in the elections of 1797?', 'It used troops to annul the results in the coup of Fructidor', ['It invited the Bourbons to return', 'It resigned in favour of the royalists', 'It abolished elections permanently'], '[1]'),
        ('Who presided over the Council of Five Hundred during the coup of Brumaire?', 'Lucien Bonaparte', ['Joseph Fouché', 'Joachim Murat', 'Paul Barras'], 'He called in troops when deputies threatened his brother. [1]'),
    ],
    'why': [
        ('the Directory was unpopular by 1799', ['It repeatedly overturned election results, as in the coups of Fructidor (1797) and Floréal (1798)', 'Inflation and the collapse of the assignat damaged the economy',
                                                'Corruption among Directors such as Barras discredited the regime', 'Renewed war and defeats in 1799 revived fears of invasion', 'Conscription under the Jourdan Law of 1798 was resented'],
         'its reliance on the army to override elections destroyed its legitimacy, so military defeat in 1799 left it with few defenders'),
        ('Bonaparte was able to seize power in 1799', ['His victories in Italy made him a popular hero', 'He controlled propaganda, such as army bulletins and newspapers, to build his image', 'Sieyès and other politicians wanted a general to back a coup',
                                                       'The army was loyal to him rather than to the Directory', 'The Directory was discredited by corruption and defeat'],
         'Bonaparte\'s military reputation was essential, but he succeeded because leading politicians wanted to replace the Directory and needed a general'),
    ],
    'claims': [
        ('The Egyptian campaign of 1798-99 was a complete military success for Bonaparte.', False, 'Nelson destroyed the French fleet at the Nile, and the army was stranded; Bonaparte returned to France without it in 1799.'),
        ('The Directory relied increasingly on the army to stay in power.', True, 'It used troops at Vendémiaire, Fructidor and against the left in 1798.'),
        ('The coup of Brumaire went entirely according to plan.', False, 'Deputies of the Five Hundred jostled Bonaparte, and troops had to clear the chamber.'),
    ],
    'ess': [
        dict(q='‘Bonaparte came to power in 1799 mainly because of the weakness of the Directory.’',
             pro=['The Directory had no stable majority and overturned elections, so it lacked legitimacy', 'Corruption and economic problems made it unpopular', 'Defeats in 1799 created a sense of crisis'],
             con=['Bonaparte\'s military reputation from Italy and his propaganda made him uniquely popular', 'Sieyès and other politicians planned the coup and chose Bonaparte', 'The army\'s loyalty to Bonaparte made the coup possible when the deputies resisted'],
             judge='the Directory\'s weakness created the opportunity, but Bonaparte\'s reputation and army support explain why he, rather than Sieyès, emerged as master of France'),
        dict(q='How successful was the Directory in governing France, 1795-99?',
             pro=['It survived threats from royalists and the left for four years', 'It ended the Terror and restored some order', 'Military victories in Italy brought wealth and territory'],
             con=['It relied on coups such as Fructidor to stay in power', 'It never solved the financial crisis or inflation', 'It was overthrown in 1799 with little resistance'],
             judge='it achieved survival and some stability after the Terror, but its dependence on the army made it a failure as a constitutional government'),
    ],
    'src': [
        S('the proclamation of the Consuls to the French people, December 1799 (translated)', 'Citizens, the Revolution is established upon the principles which began it: it is ended.',
          'the aims of the new Consulate', 'The Consuls claim that the principles of 1789 are secure and that the period of revolutionary upheaval is over.',
          'To reassure the French that the new government would bring stability while keeping the gains of the revolution.', 'it is an official statement of the new regime', 'it is propaganda presenting a coup as the completion of the revolution',
          'It does not mention that power had been seized by force.', stance=True, why='it shows Bonaparte presenting himself as the answer to the instability of the Directory years'),
        S('a memoir by a member of the Council of Five Hundred, written c.1815 (illustrative)', 'The grenadiers entered with fixed bayonets and the deputies fled through the windows. It was not the weakness of the Republic that defeated us, but the soldiers who obeyed one man.',
          'the coup of Brumaire', 'It suggests that the coup succeeded because of armed force and the army\'s loyalty to Bonaparte.',
          'To explain and perhaps justify the deputies\' failure to resist the coup.', 'the author was present at the event', 'it was written years later, after Napoleon\'s fall, by an opponent with reasons to blame him',
          'It does not show the support for the coup among politicians such as Sieyès.', stance=False, why='it stresses Bonaparte\'s military power rather than the weakness of the Directory'),
    ],
})

f1d = T("Napoleon's domestic policies and the extent of change, 1799-1814", "napoleon's domestic policies", 'extent of change', 'code napoléon', 'concordat')
build_as(f1d, {
    'enq': 'Napoleon\'s domestic policies', 'claim': 'Napoleon preserved the main gains of the revolution',
    'stim': ['In 1804 Napoleon crowned himself Emperor in Notre-Dame, in the presence of the pope.', 'The Civil Code of 1804 applied one system of law to the whole of France.',
             'The Concordat of 1801 restored relations between the French state and the papacy.'],
    'terms': [
        ('Concordat', 'the agreement of 1801 between Napoleon and Pope Pius VII that recognised Catholicism as the religion of the majority of the French'),
        ('Civil Code', 'the single code of French law introduced in 1804, later known as the Code Napoléon'),
        ('prefect', 'an official appointed by Napoleon to run each department of France'),
        ('lycée', 'a state secondary school set up under Napoleon to train officials and officers'),
        ('plebiscite', 'a vote of the whole electorate on a single question, used by Napoleon to approve constitutional changes'),
        ('Legion of Honour', 'the order created in 1802 to reward service to the state, both civil and military'),
        ('notables', 'the wealthy landowners and officials on whose support Napoleon\'s regime relied'),
    ],
    'dates': [('the Bank of France was founded', 1800, 1), ('the Concordat was signed', 1801, 7), ('Napoleon was made Consul for life', 1802, 8),
              ('the Civil Code was introduced', 1804, 3), ('Napoleon was crowned Emperor', 1804, 12), ('Napoleon abdicated for the first time', 1814, 4)],
    'mcq': [
        ('Which institution did Napoleon create in 1800 to stabilise the currency and government finance?', 'The Bank of France', ['The Committee of Public Safety', 'The Imperial University', 'The Continental System'], '[1]'),
        ('What was the main method Napoleon used to approve changes to the constitution?', 'Plebiscites', ['Elections to the Estates-General', 'Votes of the Paris sections', 'Decisions of the Parlement of Paris'], 'For example, those of 1800, 1802 and 1804. [1]'),
        ('Which revolutionary principle did the Civil Code keep?', 'Equality before the law', ['Equal rights for women in marriage', 'Universal male suffrage', 'The abolition of private property'], 'It confirmed the end of feudal privilege. [1]'),
        ('Who was Napoleon\'s minister of police?', 'Joseph Fouché', ['Talleyrand', 'Sieyès', 'Carnot'], '[1]'),
    ],
    'why': [
        ('Napoleon signed the Concordat with the pope in 1801', ['He wanted to end the religious divisions created by the Civil Constitution of the Clergy', 'Reconciling Catholics weakened royalist resistance, as in the west',
                                                                    'He could use the Church to support the regime, for example through the imperial catechism', 'The pope accepted the loss of Church lands, reassuring their purchasers'],
         'the Concordat was above all a political move to win Catholic support and isolate royalists'),
        ('Napoleon\'s regime had wide support among the notables', ['He guaranteed the land settlement of the revolution', 'The Civil Code protected property and the authority of fathers', 'Order and efficient administration followed years of instability',
                                                                       'Careers in administration, the army and the Legion of Honour rewarded loyalty', 'Victories brought prestige and wealth'],
         'Napoleon kept the support of the notables mainly because he protected property and offered order and careers'),
    ],
    'claims': [
        ('The Civil Code gave women equal rights with men in marriage.', False, 'It made wives legally subordinate to their husbands.'),
        ('Napoleon restored the property and privileges of the nobility as they had been before 1789.', False, 'He created a new imperial nobility but did not restore feudal privileges or return the lands sold in the revolution.'),
        ('Prefects in the departments were appointed by the central government.', True, 'This centralised administration under Napoleon.'),
    ],
    'ess': [
        dict(q='‘Napoleon preserved the main gains of the revolution.’',
             pro=['The Civil Code kept equality before the law and the end of feudalism', 'The land settlement and the sale of Church lands were guaranteed', 'Careers were open to talent in the army and administration'],
             con=['Political liberty disappeared: press censorship, police and a powerless legislature', 'The Concordat restored the Church\'s position and a new imperial nobility was created', 'Women\'s rights and workers\' rights were reduced'],
             judge='Napoleon preserved the social gains of 1789 that benefited the propertied classes, but he destroyed political liberty'),
        dict(q='To what extent was Napoleon\'s rule in France a dictatorship?',
             pro=['He controlled the press, reducing Paris newspapers from about seventy in 1800 to four by 1811', 'Fouché\'s police and censorship suppressed opposition', 'The legislative bodies had little real power'],
             con=['Plebiscites gave the regime popular approval', 'Government relied on the support of the notables', 'Law was codified and administration was efficient, not arbitrary'],
             judge='it was a dictatorship in that political power was concentrated in Napoleon, but it rested on consent from the notables and on legal order'),
        dict(q='How far did Napoleon\'s domestic policies bring stability to France?',
             pro=['The Concordat ended the religious conflict', 'The Bank of France and a sound currency restored finance', 'Prefects and the Civil Code gave efficient, uniform government'],
             con=['Stability depended on constant war, conscription and plunder', 'Opposition was suppressed rather than reconciled', 'The regime collapsed after military defeat in 1814'],
             judge='his policies gave France lasting institutions, but the stability of his own regime depended on military success'),
    ],
    'src': [
        S('Article 1 of the Concordat, 1801 (translated)', 'The Catholic, apostolic and Roman religion shall be freely exercised in France. Its worship shall be public, in conformity with the police regulations which the government shall deem necessary for public tranquillity.',
          'the religious settlement', 'It shows that Catholicism was restored but placed under the control of the state.',
          'To set out the terms on which the Church would operate in France.', 'it is the official text of the agreement', 'it shows intentions, not how the settlement worked in practice',
          'It does not mention the Organic Articles that Napoleon added to tighten state control.', stance=False, why='it restores the Church, which challenges the idea that Napoleon kept the anticlerical gains of the revolution'),
        S('a report by a prefect to the minister of the interior, 1806 (illustrative)', 'The department is calm. The purchasers of national lands are reassured by the Code, the priests preach obedience, and conscription is accepted, if not loved.',
          'conditions in the provinces', 'It suggests that Napoleon\'s policies brought order and reassured property owners.',
          'To report to the government on the state of the department.', 'prefects knew local conditions well', 'a prefect had reasons to present a favourable picture to his superiors',
          'It does not show the views of those who opposed the regime.', stance=True, why='it shows the land settlement of the revolution protected by the Code'),
        S('a historian writing in 1990 (illustrative)', 'Napoleon was heir to the revolution in his administration and law, but its gravedigger in politics: equality survived, liberty did not.',
          'Napoleon\'s legacy', 'The historian argues that Napoleon preserved equality before the law but destroyed political liberty.',
          'To offer a balanced interpretation of Napoleon\'s domestic rule.', 'it is a considered judgement made with hindsight', 'it is an interpretation and needs to be tested against evidence',
          'It does not give the evidence for its view.', stance=True, why='it accepts that the legal and administrative gains of the revolution were preserved', kind='secondary'),
    ],
})

CHAPTERS[1] = [f1a, f1b, f1c, f1d]


# ============================================================== CHAPTER 2: European option, the Industrial Revolution in Britain, 1750-1850

i2a = T('Causes of the Industrial Revolution: population, agriculture, capital and technology', 'causes of the industrial revolution', 'population, agriculture, capital')
build_as(i2a, {
    'enq': 'the causes of the Industrial Revolution', 'claim': 'technological invention was the main cause of the Industrial Revolution',
    'stim': ['The population of England and Wales roughly doubled between the first census of 1801 and 1851.', 'Over 4,000 parliamentary enclosure acts were passed in the century after 1750.',
             'In 1771 Richard Arkwright opened a water-powered cotton-spinning mill at Cromford in Derbyshire.'],
    'terms': [
        ('enclosure', 'the fencing of open fields and common land into compact, privately farmed holdings, often by act of Parliament'),
        ('four-course rotation', 'the system of growing wheat, turnips, barley and clover in turn so that no field had to lie fallow'),
        ('domestic system', 'the organisation of production in workers\' homes, with merchants supplying raw materials and collecting finished goods'),
        ('factory system', 'the concentration of workers and powered machinery in one building under supervision'),
        ('country banks', 'small local banks that multiplied after 1750 and provided credit to local businesses'),
        ('selective breeding', 'breeding only from the best animals to improve size and yield, associated with Robert Bakewell'),
    ],
    'dates': [('John Kay invented the flying shuttle', 1733), ('the Bridgewater Canal opened', 1761), ('Arkwright patented the water frame', 1769),
              ('Crompton developed the spinning mule', 1779), ('Boulton and Watt formed their partnership', 1775), ('the first national census was taken', 1801)],
    'mcq': [
        ('Who first smelted iron successfully using coke at Coalbrookdale?', 'Abraham Darby', ['Henry Cort', 'James Watt', 'John Wilkinson'], 'In 1709. [1]'),
        ('What was the main advantage of James Watt\'s separate condenser?', 'It greatly reduced the fuel used by steam engines', ['It allowed engines to run on water power', 'It made engines lighter for use on ships', 'It ended the need for coal in iron-making'], 'Patented in 1769. [1]'),
        ('Which of these was a source of capital for early industrial enterprise?', 'Profits from trade, including the Atlantic trade', ['Loans from the World Bank', 'Grants from the Board of Health', 'Income tax paid by workers'], 'Most firms were financed by family, partners and reinvested profits. [1]'),
        ('Why was Britain\'s supply of coal important to industrialisation?', 'It provided a cheap fuel for steam engines and iron-making', ['It was exported to pay for the Napoleonic Wars', 'It replaced cotton as the main export', 'It allowed farms to stop using horses'], '[1]'),
    ],
    'why': [
        ('Britain\'s population grew rapidly after 1750', ['Earlier marriage increased the birth rate', 'Better food supply from improved agriculture reduced deaths from famine', 'Inoculation and later vaccination against smallpox reduced deaths', 'Industrial jobs encouraged earlier marriage and larger families'],
         'a rising birth rate linked to earlier marriage was the main driver, supported by a more reliable food supply'),
        ('Britain was the first country to industrialise', ['It had large deposits of coal and iron ore close together', 'Agricultural improvement fed a growing population and released labour', 'Overseas trade and empire supplied raw cotton and markets',
                                                             'Political stability and protection of property encouraged investment', 'Inventors and entrepreneurs responded to high wages and cheap coal by developing labour-saving machines'],
         'no single factor explains it: Britain\'s advantage was the combination of cheap coal, high wages, markets and stable institutions'),
    ],
    'claims': [
        ('Most of the capital for early textile mills came from large London banks.', False, 'It came mainly from family, partners and reinvested profits; banks mostly provided short-term credit.'),
        ('Enclosure helped farmers adopt new methods such as crop rotation.', True, 'Compact holdings made it easier to experiment and to improve land.'),
        ('Britain\'s first national census was taken in 1851.', False, 'The first census was taken in 1801.'),
    ],
    'ess': [
        dict(q='‘Technological invention was the main cause of the Industrial Revolution.’',
             pro=['Machines such as the water frame and mule transformed cotton production', 'Watt\'s steam engine made power available away from rivers', 'Coke smelting and puddling allowed mass production of iron'],
             con=['Population growth provided labour and a home market', 'Agricultural improvement fed the towns', 'Capital from trade and stable government financed industry', 'Inventions were a response to demand, high wages and cheap coal'],
             judge='invention was the visible driver of change, but it depended on the demand, capital and resources that made new machines profitable'),
        dict(q='To what extent was agricultural change a necessary precondition for industrialisation?',
             pro=['Higher output fed a growing urban population', 'Rising farm incomes created demand for manufactured goods', 'Enclosure and improvement released some labour for industry'],
             con=['Much of the industrial labour force came from natural population growth', 'Capital came mainly from trade and industry itself', 'Coal, technology and overseas markets were more direct causes'],
             judge='agricultural change was an important support but not a precondition on its own; it worked together with population growth and trade'),
    ],
    'src': [
        S('Adam Smith, The Wealth of Nations, 1776 (opening of Book I, abridged)', 'The greatest improvement in the productive powers of labour ... seem to have been the effects of the division of labour.',
          'the sources of economic growth', 'Smith argues that the division of labour is the main cause of increased productivity.',
          'To explain how nations grow rich and to argue for free trade.', 'Smith was a leading economist writing at the start of the period', 'he was writing before the factory system and steam power were widespread',
          'It does not mention steam power or the new machines.', stance=False, why='it stresses organisation of work rather than invention'),
        S('a report on a cotton mill by a visitor, 1790s (illustrative)', 'One machine, turned by water, now does the work that two hundred women spinning at home once did. The master tells me his profits are laid out each year in more machines.',
          'early factory production', 'It suggests that machinery hugely increased output and that profits were reinvested.',
          'To describe the new mills to readers who had not seen them.', 'it is an eyewitness description from the time', 'the visitor relies on the mill owner\'s own claims',
          'It does not show how the mill was first financed or where its workers came from.', stance=True, why='it shows machinery transforming production'),
    ],
})

i2b = T('Economic effects: textiles, iron, steam power and the transport revolution', 'economic effects', 'textiles, iron, steam power', 'transport revolution')
build_as(i2b, {
    'enq': 'the economic effects of the Industrial Revolution', 'claim': 'the railways were the most important economic development of the period',
    'stim': ['The Liverpool and Manchester Railway opened in 1830.', 'Cotton goods made up roughly half of Britain\'s exports by value by the 1830s.',
             'By 1850 there were over 6,000 miles of railway in Britain.'],
    'terms': [
        ('puddling', 'Henry Cort\'s process of 1784 for making wrought iron by stirring molten pig iron in a reverberatory furnace'),
        ('turnpike trust', 'a body that maintained a stretch of road and charged tolls for its use'),
        ('railway mania', 'the speculative boom of the mid-1840s in which hundreds of new railway lines were authorised'),
        ('rotary motion', 'the turning motion produced by Watt\'s engines after 1781, which allowed steam to drive factory machinery'),
        ('power loom', 'a weaving machine driven by water or steam, first designed by Edmund Cartwright in 1785'),
        ('handloom weaver', 'a weaver working at home on a hand-operated loom, whose earnings collapsed as power looms spread'),
    ],
    'dates': [('Henry Cort patented the puddling process', 1784), ('Cartwright designed the power loom', 1785), ('the Stockton and Darlington Railway opened', 1825),
              ('the Liverpool and Manchester Railway opened', 1830), ('Watt\'s engine was adapted to produce rotary motion', 1781)],
    'mcq': [
        ('Which railway was the first to carry passengers between two major cities using only steam locomotives?', 'The Liverpool and Manchester Railway', ['The Stockton and Darlington Railway', 'The Great Western Railway', 'The London and Birmingham Railway'], 'Opened in 1830. [1]'),
        ('Why was the Bridgewater Canal important?', 'It halved the price of coal in Manchester', ['It linked London with Bristol', 'It was the first canal to use steam barges', 'It carried cotton directly from America'], '[1]'),
        ('Which industry led early industrial growth in Britain?', 'Cotton textiles', ['Shipbuilding', 'Chemicals', 'Motor vehicles'], '[1]'),
    ],
    'why': [
        ('the cotton industry grew so rapidly after 1780', ['Spinning machines such as the water frame and mule raised output enormously', 'Raw cotton supply grew, especially from the American South after the cotton gin', 'Cheap cotton cloth had huge home and overseas markets',
                                                              'Steam power allowed mills to be built in towns near coal'],
         'mechanisation was decisive, but growth depended on cheap raw cotton and expanding markets'),
        ('railways had such a large economic impact by 1850', ['They cut the cost and time of moving goods and people', 'Building them created huge demand for iron, coal and labour', 'They opened national markets for goods such as fresh food',
                                                                 'They attracted large-scale investment through joint-stock companies'],
         'their greatest impact was in creating demand for heavy industry and in linking national markets'),
    ],
    'claims': [
        ('Steam power had replaced water power in most textile mills by 1800.', False, 'Water power remained important until the 1830s; steam spread gradually.'),
        ('Railway building increased demand for coal and iron.', True, 'Rails, locomotives and bridges used vast amounts of iron, and engines burned coal.'),
        ('Canals were faster than railways for carrying passengers.', False, 'Canals were slow; railways were much faster and soon dominated passenger traffic.'),
    ],
    'ess': [
        dict(q='‘The railways were the most important economic development in Britain between 1750 and 1850.’',
             pro=['They transformed transport costs and speeds', 'They created demand for coal, iron and engineering', 'They linked national markets and stimulated investment'],
             con=['Railways came late; most growth before 1830 came from cotton, iron and canals', 'Cotton was the leading sector and largest export', 'Steam power underpinned both factories and railways'],
             judge='railways were transformative after 1830, but for most of the period the cotton industry and steam power were more important'),
        dict(q='How far did the Industrial Revolution change the British economy by 1850?',
             pro=['Factory production dominated cotton', 'Output of coal and iron rose many times over', 'A national railway network existed'],
             con=['Agriculture was still the largest single employer', 'Many industries such as building and clothing used traditional methods', 'Workshop and domestic production remained common'],
             judge='key sectors were transformed, but in 1850 much of the economy still worked in traditional ways'),
    ],
    'src': [
        S('a speech by a Manchester merchant, 1830s (illustrative)', 'Goods that took a week by canal now reach Liverpool in a day. Our trade has never been so brisk, and every foundry in the district is busy making rails and engines.',
          'the impact of railways', 'It suggests railways sped up trade and created demand for iron and engineering.',
          'To celebrate the benefits of the railway for local trade.', 'the merchant has direct experience of trade in Manchester', 'he is an enthusiast who may exaggerate the benefits',
          'It does not mention those who lost from railways, such as canal companies.', stance=True, why='it presents railways as transforming trade and industry'),
        S('a historian writing in 1985 (illustrative)', 'The railways were the child of industrialisation, not its parent. By 1830 the cotton industry was already Britain\'s greatest export and steam had been at work for half a century.',
          'the role of railways', 'The historian argues that industrialisation was well advanced before the railways.',
          'To challenge the view that the railways caused the Industrial Revolution.', 'it is a considered judgement with hindsight', 'it is one historian\'s interpretation',
          'It does not discuss the effects of railways after 1830.', stance=False, why='it argues cotton and steam mattered earlier and more', kind='secondary'),
    ],
})

i2c = T('Social effects: urbanisation, working and living conditions and class', 'social effects', 'urbanisation', 'working and living conditions')
build_as(i2c, {
    'enq': 'living and working conditions during industrialisation', 'claim': 'industrialisation made life worse for most working people before 1850',
    'stim': ['Manchester grew from about 75,000 people in 1801 to over 300,000 in 1851.', 'Cholera struck British towns in 1831-32 and again in 1848-49.',
             'In 1842 Edwin Chadwick published his report on the sanitary condition of the labouring population.'],
    'terms': [
        ('back-to-back housing', 'cheap terraced houses built sharing a back wall, with no through ventilation'),
        ('urbanisation', 'the growth of towns and the movement of people from the countryside into them'),
        ('standard of living debate', 'the historians\' argument between optimists and pessimists about whether workers\' lives improved during industrialisation'),
        ('truck system', 'paying workers in tokens or goods from the employer\'s shop instead of money'),
        ('Luddites', 'workers who smashed machinery in 1811-16, mainly in the Midlands and North'),
        ('working class', 'the class of wage earners whose shared experience of industrial work produced a sense of common identity'),
    ],
    'dates': [('the Luddite machine-breaking began', 1811), ('the Peterloo Massacre took place', 1819), ('the first cholera epidemic reached Britain', 1831),
              ('the Tolpuddle Martyrs were transported', 1834), ('Engels published The Condition of the Working Class in England', 1845)],
    'mcq': [
        ('Which disease, spread by contaminated water, caused major epidemics in 1831-32 and 1848-49?', 'Cholera', ['Smallpox', 'Influenza', 'Malaria'], '[1]'),
        ('What happened at St Peter\'s Fields, Manchester, in August 1819?', 'Yeomanry charged a peaceful reform meeting, killing about fifteen people', ['The first trade union was founded', 'Luddites destroyed a cotton mill', 'The People\'s Charter was published'], 'The Peterloo Massacre. [1]'),
        ('Who argued that the factory system created a revolutionary working class in 1845?', 'Friedrich Engels', ['Adam Smith', 'Edwin Chadwick', 'Robert Peel'], '[1]'),
    ],
    'why': [
        ('living conditions in industrial towns were so poor in the 1830s and 1840s', ['Towns grew too fast for housing and services to keep up', 'Builders put up cheap back-to-backs and cellar dwellings', 'There was little clean water or sewerage, so diseases such as cholera and typhus spread',
                                                                                       'Local government was weak and laissez-faire ideas discouraged spending', 'Low wages left families in overcrowded rooms'],
         'rapid growth was the root cause, but weak local government and laissez-faire attitudes explain why problems were left unsolved'),
        ('a sense of working-class identity developed by the 1830s', ['Shared experience of factory discipline and long hours', 'Concentration of workers in towns made organisation easier', 'Exclusion from the vote by the 1832 Reform Act',
                                                                      'Movements such as trade unions and the radical press spread ideas', 'Events such as Peterloo created common grievances'],
         'shared conditions created the potential, but political exclusion after 1832 turned it into a sense of class'),
    ],
    'claims': [
        ('Chadwick\'s report linked poor sanitation with disease and early death.', True, 'He showed that labourers in towns such as Liverpool died much younger than the middle class.'),
        ('Real wages fell steadily and sharply for all workers between 1780 and 1850.', False, 'Historians disagree; many estimates show little improvement before about 1820 and some rise afterwards, varying by group.'),
        ('Handloom weavers\' earnings collapsed as the power loom spread.', True, 'By the 1830s many handloom weavers were in severe poverty.'),
    ],
    'ess': [
        dict(q='‘Industrialisation made life worse for most working people before 1850.’',
             pro=['Overcrowded, insanitary towns raised death rates', 'Factory work brought long hours, strict discipline and child labour', 'Groups such as handloom weavers suffered falling earnings'],
             con=['Many estimates show real wages rising after about 1820', 'Cheaper cotton clothing and goods became available', 'Factory work offered more regular employment than farm labour', 'Experience varied greatly by region, trade and decade'],
             judge='for many urban workers conditions worsened before 1840, but the picture was mixed and improvements in wages began before 1850'),
        dict(q='To what extent did industrialisation create a working-class consciousness in Britain by 1850?',
             pro=['Chartism mobilised millions behind working-class political demands', 'Trade unions and the radical press grew', 'Peterloo and the 1832 franchise created shared grievances'],
             con=['Workers were divided by skill, trade, region and religion', 'Many skilled workers sought respectability rather than class conflict', 'Chartism declined after 1848'],
             judge='a working-class political identity clearly emerged, especially through Chartism, but it was neither uniform nor revolutionary'),
    ],
    'src': [
        S('Edwin Chadwick, Report on the Sanitary Condition of the Labouring Population, 1842 (summary)', 'Chadwick\'s report showed that the average age at death of labourers, mechanics and servants in Liverpool was about 15 years, compared with 35 for gentry and professional people.',
          'living conditions in towns', 'It shows that poor sanitation in towns caused very high death rates among working people.',
          'To persuade Parliament that public health reform was needed.', 'it uses statistical evidence collected from across the country', 'Chadwick was campaigning for reform and chose evidence to support his case; average age at death is pulled down by infant deaths',
          'It does not show whether wages were rising or falling.', stance=True, why='it shows appalling conditions and early death in industrial towns'),
        S('evidence of a mill worker to a parliamentary committee, 1832 (illustrative)', 'I began at the mill at eight years old. We worked from six in the morning till eight at night, and the overlooker strapped us if we fell asleep.',
          'child labour in factories', 'It suggests children worked very long hours under harsh discipline.',
          'To give evidence to the committee investigating factory conditions.', 'it is a first-hand account from a worker', 'the Sadler Committee heard mainly witnesses chosen by reformers, so it may present the worst cases',
          'It does not show conditions in better-run mills.', stance=True, why='it shows harsh conditions in factory work'),
        S('a historian writing in 1975 (illustrative)', 'Taken as a whole, the evidence suggests that the real wages of working families rose after the 1820s, slowly at first, and that cheaper food and clothing benefited many.',
          'the standard of living', 'The historian takes an optimistic view that real wages rose after the 1820s.',
          'To contribute to the standard of living debate.', 'it is based on long-run wage and price data', 'wage series do not measure housing, health or working conditions',
          'It does not discuss the quality of life in towns.', stance=False, why='it argues that real wages, and so living standards for many, improved', kind='secondary'),
    ],
})

i2d = T('Political responses: Chartism, the Reform Act of 1832 and factory and public health reform', 'chartism', 'reform act of 1832', 'public health reform')
build_as(i2d, {
    'enq': 'political responses to industrialisation', 'claim': 'Chartism failed mainly because of the divisions within the movement',
    'stim': ['The People\'s Charter was published in 1838.', 'The 1832 Reform Act gave the vote to £10 householders in the boroughs.',
             'In April 1848 a Chartist meeting on Kennington Common presented the third national petition.'],
    'terms': [
        ('People\'s Charter', 'the document of 1838 setting out six points for democratic reform of Parliament'),
        ('rotten borough', 'a parliamentary seat with very few voters, often controlled by a patron'),
        ('moral force', 'the Chartist strategy, linked to William Lovett, of winning reform by petitions, education and peaceful persuasion'),
        ('physical force', 'the Chartist strategy, linked to Feargus O\'Connor, of threatening or using pressure and even violence'),
        ('laissez-faire', 'the belief that government should interfere as little as possible in economic and social life'),
        ('factory inspectors', 'officials appointed under the 1833 Factory Act to enforce the law'),
    ],
    'dates': [('the Great Reform Act was passed', 1832), ('the Factory Act banned children under nine from textile mills', 1833), ('the People\'s Charter was published', 1838),
              ('the Mines Act banned women and girls from working underground', 1842), ('the first Public Health Act was passed', 1848), ('the Ten Hours Act was passed', 1847)],
    'mcq': [
        ('Which of these was one of the six points of the People\'s Charter?', 'A secret ballot', ['Votes for women', 'An elected House of Lords', 'Free education for all'], 'Others: votes for all men over 21, no property qualification, payment of MPs, equal constituencies, annual parliaments. [1]'),
        ('Which Chartist leader edited the Northern Star?', 'Feargus O\'Connor', ['William Lovett', 'Richard Oastler', 'Lord Grey'], '[1]'),
        ('Who led the government that passed the 1832 Reform Act?', 'Earl Grey', ['the Duke of Wellington', 'Robert Peel', 'Lord Melbourne'], '[1]'),
        ('What did the 1848 Public Health Act create?', 'A General Board of Health', ['A national health service', 'Compulsory vaccination', 'A Ministry of Labour'], 'Local boards could be set up, and imposed where the death rate was above 23 per 1,000. [1]'),
    ],
    'why': [
        ('the Reform Act was passed in 1832', ['Pressure from the middle classes for representation of the new industrial towns', 'Riots in Bristol, Nottingham and Derby in 1831 created fear of revolution', 'The Whigs under Grey believed limited reform would preserve the constitution',
                                              'The king agreed to create new peers if needed, so the Lords gave way', 'Rotten boroughs and the lack of seats for towns like Manchester were widely criticised'],
         'the Whigs passed reform to prevent revolution by attaching the middle classes to the system'),
        ('Chartism failed to achieve its aims by 1848', ['Parliament rejected all three petitions', 'The movement was divided between moral and physical force', 'Support rose and fell with economic conditions',
                                                         'The authorities used troops, police and arrests effectively', 'The middle classes supported the Anti-Corn Law League instead'],
         'Parliament\'s refusal and the strength of the state were decisive, but divisions and dependence on economic distress weakened the movement'),
    ],
    'claims': [
        ('The 1832 Reform Act gave the vote to most working men.', False, 'It enfranchised mainly the middle class; only about one adult man in five in England and Wales could vote afterwards.'),
        ('The 1833 Factory Act appointed inspectors to enforce it.', True, 'Four inspectors were appointed.'),
        ('All six points of the Charter had been achieved by 1850.', False, 'None had been achieved by 1850; most were achieved later, but annual parliaments never were.'),
    ],
    'ess': [
        dict(q='‘Chartism failed mainly because of the divisions within the movement.’',
             pro=['Moral and physical force leaders such as Lovett and O\'Connor quarrelled', 'Regional and local differences weakened national organisation', 'The Newport Rising of 1839 alienated moderate opinion'],
             con=['Parliament had no intention of conceding democracy', 'Government repression and the army were effective', 'Economic recovery after 1842 and 1848 reduced support', 'Middle-class reformers were absorbed by the Anti-Corn Law League'],
             judge='divisions weakened Chartism, but the decisive reason was the refusal of a Parliament elected on a narrow franchise to concede, backed by the power of the state'),
        dict(q='How far did governments respond effectively to the social problems caused by industrialisation by 1850?',
             pro=['Factory Acts of 1833, 1844 and 1847 limited hours for children and women', 'The Mines Act of 1842 banned women and young children underground', 'The 1848 Public Health Act began state action on sanitation'],
             con=['Most laws were limited and weakly enforced', 'Local boards of health were voluntary unless death rates were very high', 'The 1834 Poor Law treated poverty harshly'],
             judge='governments began to accept a role in social reform, but by 1850 the response was limited and piecemeal'),
    ],
    'src': [
        S('the People\'s Charter, 1838 (summary of its six points)', 'The Charter demanded a vote for every man over twenty-one, the secret ballot, no property qualification for MPs, payment of MPs, equal constituencies and annual parliaments.',
          'Chartist aims', 'It shows the Chartists demanded democratic political reform.',
          'To set out a programme that could unite working-class reformers.', 'it is the founding document of the movement', 'it shows aims, not how much support or unity the movement had',
          'It does not show how Chartists planned to achieve these aims.', stance=None),
        S('a speech at a Chartist meeting in the north of England, 1839 (illustrative)', 'We have petitioned and been laughed at. If the Parliament will not hear the voice of the people, the people must arm themselves to be heard.',
          'Chartist methods', 'It shows that some Chartists were willing to threaten force.',
          'To rouse support for physical force if the petition failed.', 'it shows the language used at meetings at the time', 'one speaker at one meeting does not represent the whole movement',
          'It does not show the views of moral force Chartists.', stance=True, why='it shows the division over methods within Chartism'),
        S('a letter from a magistrate to the Home Office, 1842 (illustrative)', 'The troops arrived in good time and the meeting dispersed quietly. Since the mills reopened, the Charter is less talked of in the town.',
          'the decline of Chartist activity', 'It suggests troops and economic recovery reduced Chartist activity.',
          'To report to the government on the restoration of order.', 'magistrates had direct knowledge of local disturbances', 'a magistrate had reasons to stress his own success in keeping order',
          'It does not show the size of Chartist support.', stance=False, why='it points to repression and economic recovery rather than divisions'),
    ],
})

CHAPTERS[2] = [i2a, i2b, i2c, i2d]


# ============================================================== CHAPTER 3: European option, liberalism and nationalism in Italy and Germany, 1815-71

n3a = T('The impact of the 1848 revolutions in the Italian and German states', '1848 revolutions', 'italian and german states')
build_as(n3a, {
    'enq': 'the revolutions of 1848-49 in Italy and Germany', 'claim': 'the revolutions of 1848-49 failed mainly because of divisions among the revolutionaries',
    'stim': ['In March 1848 revolutions broke out in Vienna, Berlin and Milan.', 'The Frankfurt Parliament first met in May 1848.',
             'In April 1849 Frederick William IV of Prussia refused the imperial crown offered by the Frankfurt Parliament.'],
    'terms': [
        ('Frankfurt Parliament', 'the all-German national assembly elected in 1848 to draw up a constitution for a united Germany'),
        ('Grossdeutschland', 'the "greater Germany" solution, a united Germany including the German lands of Austria'),
        ('Kleindeutschland', 'the "smaller Germany" solution, a united Germany under Prussia that excluded Austria'),
        ('Statuto', 'the constitution granted by Charles Albert of Piedmont in 1848, which survived the failure of the revolutions'),
        ('Roman Republic', 'the republic proclaimed in Rome in February 1849 and defended by Mazzini and Garibaldi until French troops crushed it'),
        ('Zollverein', 'the Prussian-led customs union of German states set up in 1834, which excluded Austria'),
    ],
    'dates': [('the Zollverein came into effect', 1834), ('the Five Days of Milan forced the Austrians out of the city', 1848, 3), ('Piedmont was defeated by Austria at Custoza', 1848, 7),
              ('Piedmont was defeated at Novara and Charles Albert abdicated', 1849, 3), ('Prussia accepted the Punctation of Olmütz', 1850, 11)],
    'mcq': [
        ('Who commanded the Austrian forces that defeated Piedmont in 1848-49?', 'Radetzky', ['Metternich', 'Windischgrätz', 'Schwarzenberg'], '[1]'),
        ('Why did Pope Pius IX lose the support of Italian nationalists in April 1848?', 'He refused to support war against Catholic Austria', ['He declared war on France', 'He abolished the Papal States', 'He supported Mazzini\'s republic'], 'His Allocution of 29 April 1848. [1]'),
        ('Who defended the Roman Republic against the French in 1849?', 'Garibaldi', ['Cavour', 'Victor Emmanuel II', 'Charles Albert'], 'With Mazzini as one of the triumvirs. [1]'),
        ('Which state forced Prussia to abandon its plan for a union of German states at Olmütz in 1850?', 'Austria', ['France', 'Russia', 'Denmark'], '[1]'),
    ],
    'why': [
        ('the revolutions in the German states failed by 1849', ['The Frankfurt Parliament had no army of its own and relied on the princes', 'Liberals were divided over Grossdeutschland and Kleindeutschland', 'Middle-class liberals feared the radicalism of workers and peasants',
                                                                  'Frederick William IV refused the crown', 'Austria and Prussia recovered control of their armies and capitals by late 1848'],
         'the revolutionaries never controlled armed force, so when the rulers recovered their nerve the revolutions collapsed'),
        ('the revolutions in Italy failed by 1849', ['Austrian military strength under Radetzky defeated Piedmont at Custoza and Novara', 'Italian states and leaders were divided in aims, between monarchists and republicans', 'The pope withdrew support in April 1848',
                                                     'France intervened to crush the Roman Republic', 'The peasantry gave little support'],
         'Austrian military power was decisive, but divisions among Italians meant they could not resist it'),
    ],
    'claims': [
        ('The Frankfurt Parliament was elected by a broad male franchise.', True, 'Elections were held on a wide male suffrage, though most deputies were educated middle-class men.'),
        ('Piedmont lost its constitution after its defeat in 1849.', False, 'Victor Emmanuel II kept the Statuto, which made Piedmont a focus for liberals.'),
        ('Frederick William IV accepted the crown of a united Germany in 1849.', False, 'He refused it, reportedly calling it a crown "from the gutter".'),
    ],
    'ess': [
        dict(q='‘The revolutions of 1848-49 in Italy and Germany failed mainly because of divisions among the revolutionaries.’',
             pro=['Liberals and radicals disagreed over aims and methods', 'Germans divided over Grossdeutschland and Kleindeutschland', 'Italians divided between monarchists and republicans and between states'],
             con=['The armies of Austria and Prussia remained loyal to their rulers', 'Foreign intervention, especially France in Rome, crushed revolutions', 'The rulers recovered once the shock of March 1848 passed'],
             judge='divisions weakened the revolutions, but they failed because the old regimes kept control of military force'),
        dict(q='How far did the 1848 revolutions change the prospects for unification in Italy and Germany?',
             pro=['Piedmont kept the Statuto and became the leader of Italian liberals', 'The failure of idealism discredited Mazzini\'s methods and encouraged realism', 'The Frankfurt Parliament raised the Kleindeutsch solution under Prussia'],
             con=['Austria restored its dominance in both Italy and Germany by 1850', 'Olmütz showed Prussia could not yet challenge Austria', 'Unification later depended on diplomacy and war, not on 1848'],
             judge='1848 failed in the short term, but it pointed both movements towards leadership by Piedmont and Prussia'),
    ],
    'src': [
        S('a speech by a moderate deputy in the Frankfurt Parliament, 1848 (illustrative)', 'We want unity, but we want it with order. If we follow the agitators of the streets we shall have neither unity nor freedom, only anarchy.',
          'divisions among German liberals', 'It shows moderate liberals feared radicals more than they opposed the princes.',
          'To persuade the Parliament to reject radical methods.', 'it shows the views of a member of the assembly at the time', 'one deputy\'s speech does not represent all members',
          'It does not show the role of the Prussian and Austrian armies.', stance=True, why='it shows liberals divided from radicals'),
        S('a report by an Austrian officer in Lombardy, 1848 (illustrative)', 'The Piedmontese fight bravely, but they are few and badly led. Our army is united and the rebels quarrel among themselves; victory is certain.',
          'the war in northern Italy', 'It suggests the Austrian army was stronger and that the Italians were divided.',
          'To report confidently to superiors on the campaign.', 'an officer had direct knowledge of the fighting', 'he had reasons to present the Austrian army favourably',
          'It does not mention the pope\'s withdrawal of support.', stance=True, why='it stresses Italian quarrels as well as Austrian strength'),
    ],
})

n3b = T('Italian unification: the roles of Cavour, Garibaldi and foreign powers', 'italian unification', 'cavour', 'garibaldi')
build_as(n3b, {
    'enq': 'Italian unification', 'claim': 'Cavour was the main architect of Italian unification',
    'stim': ['In July 1858 Cavour and Napoleon III met secretly at Plombières.', 'In May 1860 Garibaldi landed in Sicily with about a thousand volunteers.',
             'The Kingdom of Italy was proclaimed in March 1861.'],
    'terms': [
        ('Risorgimento', 'the "resurgence", the nineteenth-century movement for Italian unification and national revival'),
        ('Plombières agreement', 'the secret deal of 1858 in which Napoleon III promised to help Piedmont fight Austria in return for Nice and Savoy'),
        ('the Thousand', 'Garibaldi\'s volunteer army (the Redshirts) that conquered Sicily and Naples in 1860'),
        ('Young Italy', 'the nationalist movement founded by Mazzini in 1831 to create a united, republican Italy'),
        ('National Society', 'the Italian National Society founded in 1857, which supported unification under Piedmont'),
        ('plebiscite', 'a popular vote on a single question, used in 1860 to approve the annexation of central and southern Italy'),
    ],
    'dates': [('Cavour became prime minister of Piedmont', 1852), ('Piedmont joined the Crimean War', 1855), ('the Battles of Magenta and Solferino were fought', 1859),
              ('Garibaldi landed at Marsala in Sicily', 1860, 5), ('the Kingdom of Italy was proclaimed', 1861, 3), ('Italian troops entered Rome', 1870, 9)],
    'mcq': [
        ('What did Piedmont have to give to France in 1860?', 'Nice and Savoy', ['Lombardy and Venetia', 'Parma and Modena', 'Sardinia and Corsica'], 'The price of French help agreed at Plombières. [1]'),
        ('Why did Napoleon III make peace with Austria at Villafranca in July 1859?', 'He feared Prussian intervention and was shocked by the losses at Solferino', ['Piedmont had been defeated', 'Garibaldi had captured Rome', 'Britain had declared war on France'], '[1]'),
        ('Where did Garibaldi hand over his conquests to Victor Emmanuel II in October 1860?', 'Teano', ['Turin', 'Marsala', 'Milan'], '[1]'),
        ('How did Italy gain Venetia in 1866?', 'As a result of Prussia\'s defeat of Austria', ['By a victory at the Battle of Custoza', 'By purchase from France', 'By a rising led by Mazzini'], 'Italy had been defeated at Custoza and Lissa. [1]'),
    ],
    'why': [
        ('Cavour sought French help against Austria', ['Piedmont alone had been defeated by Austria in 1848-49', 'Napoleon III sympathised with Italian nationalism and wanted to weaken Austria', 'Participation in the Crimean War had won Cavour a hearing at the Paris peace congress',
                                                       'Cavour believed Italy would be made by diplomacy and war, not by popular revolution'],
         'Cavour recognised that only a great power could defeat Austria, so French help was essential'),
        ('Garibaldi\'s expedition of 1860 succeeded', ['Sicilian peasants had risen against Bourbon rule', 'The Neapolitan army was poorly led and demoralised', 'The British navy did not prevent his crossings',
                                                       'Garibaldi\'s leadership and reputation attracted volunteers', 'Cavour allowed the expedition to sail'],
         'Garibaldi\'s leadership was crucial, but the weakness of the Bourbon state made his success possible'),
        ('Cavour sent Piedmontese troops into the Papal States in 1860', ['He feared Garibaldi would march on Rome and provoke French intervention', 'He wanted Piedmont, not the radicals, to control the south', 'Annexing the Marches and Umbria linked north and south', 'It allowed Victor Emmanuel to take the leadership of unification'],
         'Cavour acted mainly to take control of unification away from Garibaldi and the radicals'),
    ],
    'claims': [
        ('Cavour planned from the start to unite the whole of Italy including the south.', False, 'Most historians think he aimed at a northern kingdom under Piedmont and acted in the south mainly to control Garibaldi.'),
        ('Garibaldi handed over southern Italy to Victor Emmanuel II in 1860.', True, 'He met the king at Teano in October 1860.'),
        ('Rome became part of Italy in 1861.', False, 'Rome was protected by French troops and was taken only in 1870, after the French withdrew.'),
    ],
    'ess': [
        dict(q='‘Cavour was the main architect of Italian unification.’',
             pro=['He modernised Piedmont and made it the leader of Italian liberalism', 'He won French support at Plombières and so defeated Austria in 1859', 'He annexed the central duchies and the Papal States to control the process'],
             con=['Garibaldi conquered the south, which Cavour had not planned to take', 'Foreign powers, especially France and Prussia, made unification possible', 'Mazzini\'s ideas had spread the idea of a united Italy'],
             judge='Cavour shaped the form unification took under Piedmont, but he was not its only architect: the south was won by Garibaldi and Venetia and Rome by events abroad'),
        dict(q='To what extent was Italian unification achieved by foreign powers rather than by Italians?',
             pro=['French armies defeated Austria in 1859', 'Prussia\'s victory gave Italy Venetia in 1866', 'French withdrawal in 1870 allowed the capture of Rome'],
             con=['Cavour\'s diplomacy secured French help', 'Garibaldi and the Thousand conquered the south', 'Plebiscites showed support in central and southern Italy'],
             judge='Italians provided the leadership and won the south, but at each stage of the war against Austria and for Rome foreign powers were decisive'),
    ],
    'src': [
        S('a letter from Cavour to a fellow minister, 1860 (illustrative)', 'Garibaldi has done the greatest service that one man could do for Italy, but he must not be allowed to go to Rome. If he does, France will act and all will be lost.',
          'Cavour\'s attitude to Garibaldi', 'It suggests Cavour admired Garibaldi but feared his march on Rome would provoke France.',
          'To explain Cavour\'s plans to a colleague privately.', 'it is a private letter, so it may reveal real intentions', 'Cavour often wrote differently to different people to suit his aims',
          'It does not show what Garibaldi himself intended.', stance=True, why='it shows Cavour controlling events'),
        S('a proclamation by Garibaldi, 1860 (illustrative)', 'Italians! The Sicilians are fighting against the enemies of Italy and for Italy. It is the duty of every Italian to help them with words, money and arms.',
          'Garibaldi\'s aims in 1860', 'It shows Garibaldi presenting the Sicilian revolt as a national Italian cause.',
          'To win volunteers and support for the expedition.', 'it shows the appeal Garibaldi made at the time', 'it is propaganda designed to attract recruits',
          'It does not show Cavour\'s role in allowing the expedition.', stance=False, why='it shows Garibaldi and popular nationalism driving events in the south'),
    ],
})

n3c = T('German unification: Prussia, Bismarck and the wars of 1864-71', 'german unification', 'bismarck', 'wars of 1864-71')
build_as(n3c, {
    'enq': 'German unification', 'claim': 'Bismarck planned German unification from the start',
    'stim': ['Bismarck became Minister-President of Prussia in September 1862.', 'On 3 July 1866 Prussia defeated Austria at Königgrätz (Sadowa).',
             'The German Empire was proclaimed in the Hall of Mirrors at Versailles on 18 January 1871.'],
    'terms': [
        ('Realpolitik', 'politics based on practical considerations of power rather than ideals'),
        ('North German Confederation', 'the union of German states north of the River Main under Prussian leadership, set up in 1867'),
        ('Ems Telegram', 'the report of July 1870 that Bismarck edited to make it seem that the king had insulted the French ambassador'),
        ('Schleswig-Holstein', 'the two duchies disputed with Denmark, over which Prussia and Austria fought Denmark in 1864'),
        ('Treaty of Prague', 'the peace of 1866 that ended the Austro-Prussian War and excluded Austria from German affairs'),
        ('needle gun', 'the breech-loading rifle used by the Prussian army, which could be fired faster than Austrian muzzle-loaders'),
    ],
    'dates': [('Bismarck became Minister-President of Prussia', 1862, 9), ('Prussia and Austria fought Denmark', 1864), ('the Gastein Convention was signed', 1865, 8),
              ('Prussia defeated Austria at Königgrätz', 1866, 7), ('the North German Confederation was formed', 1867), ('Napoleon III surrendered at Sedan', 1870, 9), ('the German Empire was proclaimed at Versailles', 1871, 1)],
    'mcq': [
        ('Which ministers reformed the Prussian army in the 1860s?', 'Roon and Moltke', ['Metternich and Schwarzenberg', 'Cavour and Rattazzi', 'Stein and Hardenberg'], 'Roon as war minister, Moltke as chief of the general staff. [1]'),
        ('Which provinces did France lose to Germany in 1871?', 'Alsace and most of Lorraine', ['Nice and Savoy', 'Schleswig and Holstein', 'Bavaria and Baden'], 'By the Treaty of Frankfurt. [1]'),
        ('What sparked the crisis between France and Prussia in 1870?', 'The Hohenzollern candidature for the Spanish throne', ['The Schleswig-Holstein question', 'The annexation of Hanover', 'The sale of Luxembourg to Belgium'], '[1]'),
        ('Why did Bismarck offer Austria lenient terms in 1866?', 'To avoid lasting hostility and keep Austria as a possible future ally', ['Because Austria had won the war', 'Because France demanded it', 'Because he wanted Austria in the North German Confederation'], '[1]'),
    ],
    'why': [
        ('Prussia defeated Austria in 1866', ['The reformed Prussian army was larger, better trained and used the needle gun', 'Moltke used railways to concentrate forces quickly', 'Bismarck isolated Austria diplomatically: Italy was an ally and France and Russia stayed neutral',
                                               'Austria was weakened by debt and had to fight Italy too'],
         'Prussian military superiority was decisive, made possible by Bismarck\'s isolation of Austria'),
        ('the southern German states joined the German Empire in 1871', ['France was seen as the aggressor after the Ems Telegram', 'Secret military alliances of 1866 bound them to Prussia', 'The Zollverein had tied their economies to the north',
                                                                           'Victory over France created a surge of national feeling', 'Bismarck offered concessions such as Bavaria keeping some rights'],
         'war with France created the national feeling and the circumstances that made it impossible for the south to stay out'),
    ],
    'claims': [
        ('Bismarck said that the great questions of the day would be decided by "iron and blood".', True, 'In a speech to the budget committee of the Prussian Landtag in September 1862.'),
        ('Austria joined the North German Confederation in 1867.', False, 'Austria was excluded from German affairs by the Treaty of Prague in 1866.'),
        ('The German Empire was proclaimed in Berlin.', False, 'It was proclaimed in the Hall of Mirrors at Versailles.'),
    ],
    'ess': [
        dict(q='‘Bismarck planned German unification from the start.’',
             pro=['His "iron and blood" speech showed he expected unification by force', 'Each war prepared the way for the next', 'He manipulated the Ems Telegram to provoke war with France'],
             con=['His first aim was Prussian dominance in north Germany, not national unity', 'He responded to opportunities such as the Schleswig-Holstein crisis and the Spanish succession', 'Economic and military developments outside his control mattered'],
             judge='Bismarck aimed consistently at Prussian power, but he was an opportunist who exploited events rather than following a plan for unification'),
        dict(q='How far was Prussian economic strength the main reason for German unification?',
             pro=['The Zollverein tied the German states to Prussia economically', 'Industrial growth, coal and railways supported a modern army', 'Prussian wealth paid for army reform'],
             con=['Bismarck\'s diplomacy isolated each enemy', 'Military reform and Moltke\'s leadership won the wars', 'French and Austrian mistakes helped Prussia'],
             judge='economic strength gave Prussia the means, but unification was achieved through Bismarck\'s diplomacy and military victory'),
    ],
    'src': [
        S('Bismarck, speech to the budget committee of the Prussian Landtag, September 1862 (translated, abridged)', 'The great questions of the day will not be decided by speeches and majority decisions - that was the great mistake of 1848 and 1849 - but by iron and blood.',
          'Bismarck\'s methods', 'Bismarck argues that power and force, not parliamentary debate, will decide Germany\'s future.',
          'To persuade the deputies to approve money for army reform.', 'it is Bismarck\'s own words at the start of his ministry', 'it was a speech to win a budget dispute, not a statement of a detailed plan',
          'It does not say that he aimed at unification under Prussia.', stance=True, why='it suggests he expected to use force to settle the German question'),
        S('Bismarck, Reflections and Reminiscences, published 1898 (summary)', 'In his memoirs Bismarck presented the wars of 1864, 1866 and 1870 as steps in a deliberate policy that he had pursued from the start to unite Germany under Prussia.',
          'Bismarck\'s aims', 'It presents unification as the result of a long-term plan by Bismarck.',
          'To present his career in the best light after his dismissal.', 'it is Bismarck\'s own account', 'written decades later, after his dismissal, to defend his reputation',
          'It does not reflect his uncertainty in the 1860s.', stance=True, why='it claims he followed a plan from the start'),
        S('a historian writing in 1990 (illustrative)', 'Bismarck was a gambler who played the cards he was dealt. He sought Prussian mastery in the north; Germany came to him as much as he came to Germany.',
          'Bismarck\'s role', 'The historian argues that Bismarck was an opportunist aiming at Prussian power rather than national unity.',
          'To challenge the view that Bismarck had a master plan.', 'it is a considered interpretation with hindsight', 'it is an interpretation that needs to be tested against evidence',
          'It does not give details of particular decisions.', stance=False, why='it presents Bismarck as an opportunist without a plan', kind='secondary'),
    ],
})

n3d = T('How far unification was driven by nationalism or by Realpolitik', 'nationalism or by realpolitik', 'realpolitik')
build_as(n3d, {
    'enq': 'the forces behind unification', 'claim': 'unification in Italy and Germany was driven more by Realpolitik than by nationalism',
    'stim': ['Mazzini founded Young Italy in 1831.', 'Membership of the German National Association reached about 25,000 in the early 1860s.',
             'In 1861 Massimo d\'Azeglio is reported to have said: "We have made Italy; now we must make Italians."'],
    'terms': [
        ('nationalism', 'the belief that people who share a language, culture and history should form one independent state'),
        ('liberalism', 'support for constitutional government, individual rights and free trade'),
        ('cultural nationalism', 'a sense of nationhood expressed through language, literature, music and history rather than politics'),
        ('Nationalverein', 'the German National Association founded in 1859 to promote unity under Prussia'),
        ('Indemnity Bill', 'the law of 1866 by which the Prussian liberals approved Bismarck\'s unconstitutional spending, splitting the liberals'),
        ('Mazzinianism', 'Mazzini\'s ideas of a united, democratic Italy created by a popular rising'),
    ],
    'dates': [('Young Italy was founded', 1831), ('the German National Association was founded', 1859), ('the Prussian Landtag passed the Indemnity Bill', 1866), ('the plebiscites approved annexation of the central Italian duchies', 1860, 3)],
    'mcq': [
        ('Which writer was most associated with a democratic, republican Italian nationalism?', 'Mazzini', ['Cavour', 'Metternich', 'Pius IX'], '[1]'),
        ('What did the Indemnity Bill of 1866 show about Prussian liberals?', 'Many were willing to accept Bismarck\'s methods once Prussia had won', ['They had gained control of the army', 'They opposed the war with Austria', 'They wanted Austria to lead Germany'], '[1]'),
        ('Which group in Italy was largely untouched by nationalism before 1860?', 'The peasantry, especially in the south', ['Students in Turin', 'Exiles in London', 'Members of the National Society'], '[1]'),
    ],
    'why': [
        ('nationalism had limited popular support in Italy before 1860', ['Most Italians were illiterate peasants who spoke regional dialects', 'Loyalty to region and to the Church was stronger than to Italy', 'Nationalism was mainly a cause of the educated middle class',
                                                                           'The failures of 1848-49 discredited popular risings'],
         'nationalism was confined to an educated minority, so unification depended on states and armies'),
        ('Prussian liberals came to support Bismarck after 1866', ['Victory over Austria achieved the national aims liberals had failed to reach in 1848', 'Bismarck offered the Indemnity Bill as a reconciliation', 'Many liberals valued unity above constitutional principles', 'The North German Confederation had a parliament elected by universal male suffrage'],
         'success in 1866 persuaded many liberals that national unity mattered more than parliamentary control'),
    ],
    'claims': [
        ('Most Italians spoke standard Italian in 1861.', False, 'Only a small minority, perhaps under 10 per cent, spoke standard Italian; most spoke regional dialects.'),
        ('The German Empire of 1871 was created by agreement of the German princes after a war.', True, 'It was a federation of states under the Prussian king as emperor.'),
        ('Mazzini supported unification under the Piedmontese monarchy from the start.', False, 'He wanted a democratic republic, though he sometimes cooperated with the monarchy.'),
    ],
    'ess': [
        dict(q='‘Unification in both Italy and Germany was driven more by Realpolitik than by nationalism.’',
             pro=['Cavour and Bismarck used diplomacy and war to expand Piedmont and Prussia', 'Foreign alliances and wars were decisive', 'Popular nationalism in 1848 failed'],
             con=['Garibaldi\'s campaign and plebiscites showed nationalist support', 'Nationalist feeling made the southern German states join in 1870', 'Nationalist societies prepared opinion for unification'],
             judge='Realpolitik delivered unification, but leaders could exploit nationalism because it had become a powerful idea among the educated classes'),
        dict(q='To what extent were the outcomes of unification in Italy and Germany similar?',
             pro=['Both were achieved under a dominant northern state and monarchy', 'Both depended on war and foreign diplomacy', 'Both created states led by conservatives and the propertied'],
             con=['Germany was a federation; Italy a centralised state', 'Germany was achieved by Prussian military power; Italy owed more to foreign help and Garibaldi', 'Italy faced deep north-south divisions and opposition from the Church'],
             judge='the processes were similar in reliance on a leading state and war, but the resulting states differed greatly in strength and structure'),
    ],
    'src': [
        S('a pamphlet by an Italian nationalist exile, 1850s (illustrative)', 'Italy will not be made by kings or diplomats but by the people. A nation is born when its people rise as one.',
          'nationalist ideas', 'It argues that unification must come from popular nationalism, not from states.',
          'To keep the Mazzinian ideal alive after 1849.', 'it shows the ideas of nationalist exiles at the time', 'it states hopes rather than describing what happened',
          'It does not show how much support such ideas had among Italians.', stance=False, why='it stresses popular nationalism'),
        S('a letter from a Prussian conservative, 1866 (illustrative)', 'We did not fight for the dreams of professors at Frankfurt. We fought for Prussia, and Germany will follow because Prussia is strong.',
          'the motives of Prussian leaders', 'It suggests Prussian leaders were driven by Prussian power, not German nationalism.',
          'To explain Prussian aims to a fellow conservative.', 'it reflects the views of the conservative elite at the time', 'one writer\'s views may not represent government policy',
          'It does not show the views of German liberals.', stance=True, why='it presents unification as the product of Prussian power politics'),
    ],
})

CHAPTERS[3] = [n3a, n3b, n3c, n3d]


# ============================================================== CHAPTER 4: American option, the origins of the Civil War, 1820-61

a4a = T('Slavery, sectionalism and the Missouri Compromise', 'slavery, sectionalism', 'missouri compromise')
build_as(a4a, {
    'enq': 'sectional tension in the 1820s and 1830s', 'claim': 'slavery was the main cause of sectional tension between North and South before 1840',
    'stim': ['In 1819 Missouri applied to join the Union as a slave state.', 'In 1831 William Lloyd Garrison began publishing The Liberator.',
             'In 1832 South Carolina declared the federal tariffs of 1828 and 1832 null and void within the state.'],
    'terms': [
        ('sectionalism', 'loyalty to the interests of one region (North, South or West) above those of the nation'),
        ('Missouri Compromise', 'the agreement of 1820 admitting Missouri as a slave state and Maine as a free state and banning slavery in the rest of the Louisiana Purchase north of 36°30′'),
        ('nullification', 'the claim that a state could declare a federal law void within its borders'),
        ('abolitionism', 'the movement to end slavery immediately, associated with Garrison and Frederick Douglass'),
        ('gag rule', 'the rules of 1836-44 by which the House of Representatives refused to discuss anti-slavery petitions'),
        ('Tallmadge amendment', 'the proposal of 1819 to ban the further introduction of slaves into Missouri, which sparked the crisis'),
    ],
    'dates': [('the Missouri Compromise was agreed', 1820), ('Nat Turner\'s rebellion took place in Virginia', 1831), ('South Carolina passed its Ordinance of Nullification', 1832, 11),
              ('the House of Representatives adopted the gag rule', 1836), ('the Tariff of Abominations was passed', 1828)],
    'mcq': [
        ('Which line divided free from slave territory in the Louisiana Purchase under the Missouri Compromise?', '36°30′ north', ['49° north', 'The Mason-Dixon line', 'The Mississippi River'], '[1]'),
        ('Which state was admitted as a free state alongside Missouri in 1820?', 'Maine', ['California', 'Ohio', 'Kansas'], 'It kept the balance of free and slave states in the Senate. [1]'),
        ('Who, as vice-president, set out the theory of nullification?', 'John C. Calhoun', ['Henry Clay', 'Andrew Jackson', 'Daniel Webster'], 'In the South Carolina Exposition and Protest (1828). [1]'),
        ('What did southern states do after Nat Turner\'s rebellion?', 'Tightened slave codes, for example limiting education of enslaved people', ['Abolished slavery gradually', 'Gave the vote to free Black men', 'Ended the internal slave trade'], '[1]'),
    ],
    'why': [
        ('the admission of Missouri caused a crisis in 1819-20', ['It threatened to upset the balance of free and slave states in the Senate', 'The Tallmadge amendment raised the question of Congress\'s power over slavery in new states',
                                                                   'Northern votes in the House were growing faster than southern', 'It was the first time the expansion of slavery into the West became a national issue'],
         'the crisis was about political power in the Senate as much as morality, which is why it was settled by balancing the states'),
        ('the nullification crisis of 1832-33 alarmed southerners and nationalists alike', ['South Carolina challenged federal authority over the tariff', 'Jackson threatened to use force through the Force Bill', 'Southerners feared a federal government able to override states might one day attack slavery', 'It raised the question of whether states could leave the Union'],
         'the tariff was the issue, but the crisis mattered because it raised the constitutional question that would later be used to defend slavery'),
    ],
    'claims': [
        ('The Missouri Compromise banned slavery in all western territories.', False, 'It banned slavery only in the remaining Louisiana Purchase lands north of 36°30′, except Missouri.'),
        ('The gag rule prevented the House from debating anti-slavery petitions.', True, 'It lasted from 1836 until 1844.'),
        ('Nullification was mainly a dispute over the tariff.', True, 'South Carolina objected to the tariffs of 1828 and 1832, though fear of federal power over slavery lay behind it.'),
    ],
    'ess': [
        dict(q='‘Slavery was the main cause of sectional tension in the United States between 1820 and 1840.’',
             pro=['The Missouri crisis was about the expansion of slavery', 'Abolitionism after 1831 alarmed the South', 'The gag rule showed slavery could not be discussed calmly'],
             con=['The tariff and the nullification crisis set the South against northern economic interests', 'Disputes over federal power and states\' rights were constitutional', 'In the 1830s party loyalties to Whigs and Democrats cut across sections'],
             judge='slavery lay behind most disputes, but before 1840 the two-party system and compromise kept sectional tension under control'),
        dict(q='How successful was the Missouri Compromise in reducing sectional conflict?',
             pro=['It kept the balance in the Senate', 'It settled the status of slavery in the Louisiana Purchase for over thirty years', 'No major crisis over territory followed until the 1840s'],
             con=['It drew a geographical line that encouraged sectional thinking', 'It did not settle the question of slavery in future territories', 'Jefferson called it a "fire bell in the night", warning of future conflict'],
             judge='it was successful in the short and medium term, but it postponed rather than solved the problem of slavery in the West'),
    ],
    'src': [
        S('a letter from Thomas Jefferson, April 1820', 'This momentous question, like a fire bell in the night, awakened and filled me with terror. I considered it at once as the knell of the Union.',
          'reactions to the Missouri crisis', 'Jefferson suggests the Missouri crisis threatened the survival of the Union.',
          'To express his alarm at the sectional division over Missouri privately.', 'Jefferson was a former president with long political experience', 'he was a southern slaveholder writing in retirement, and his fears may be exaggerated',
          'It does not describe the terms of the compromise.', stance=True, why='it shows that a dispute over slavery had become a threat to the Union'),
        S('a speech by a South Carolina politician, 1832 (illustrative)', 'This tariff robs the planter to enrich the northern manufacturer. If Congress may tax us at will, there is no right of ours it may not one day trample.',
          'the nullification crisis', 'It shows southern anger at the tariff and fear of federal power.',
          'To win support for nullification in South Carolina.', 'it reflects the arguments used at the time', 'it is a partisan speech intended to rouse support',
          'It does not mention slavery directly.', stance=False, why='it presents the tariff and states\' rights, not slavery, as the issue'),
    ],
})

a4b = T('Westward expansion, the Mexican War and the Compromise of 1850', 'westward expansion', 'mexican war', 'compromise of 1850')
build_as(a4b, {
    'enq': 'the impact of westward expansion', 'claim': 'the Compromise of 1850 settled the issue of slavery in the territories',
    'stim': ['The United States annexed Texas in 1845.', 'In 1846 David Wilmot proposed that slavery should be banned in any territory gained from Mexico.',
             'The discovery of gold in California in 1848 brought a rush of settlers.'],
    'terms': [
        ('Manifest Destiny', 'the belief that the United States was destined to expand across the North American continent'),
        ('Wilmot Proviso', 'the proposal of 1846 to ban slavery in any territory acquired from Mexico; it passed the House but not the Senate'),
        ('popular sovereignty', 'the idea that the settlers of a territory should decide for themselves whether to allow slavery'),
        ('Fugitive Slave Act', 'the law of 1850 requiring citizens to help recapture people who had escaped from slavery and denying them a jury trial'),
        ('Treaty of Guadalupe Hidalgo', 'the treaty of 1848 by which Mexico ceded California and the south-west to the United States'),
        ('Free Soil Party', 'the party formed in 1848 to oppose the spread of slavery into the western territories'),
    ],
    'dates': [('Texas was annexed', 1845), ('war with Mexico began', 1846), ('the Treaty of Guadalupe Hidalgo was signed', 1848),
              ('the Compromise of 1850 was passed', 1850), ('Uncle Tom\'s Cabin was published as a book', 1852)],
    'mcq': [
        ('Who proposed the series of measures that became the Compromise of 1850?', 'Henry Clay', ['Abraham Lincoln', 'John Brown', 'Jefferson Davis'], 'Stephen Douglas then steered them through Congress as separate bills. [1]'),
        ('Under the Compromise of 1850, how was California admitted?', 'As a free state', ['As a slave state', 'As a territory with popular sovereignty', 'As part of Texas'], '[1]'),
        ('Which measure of the Compromise of 1850 most angered northerners?', 'The Fugitive Slave Act', ['The admission of California', 'The end of the slave trade in Washington DC', 'The settlement of the Texas boundary'], '[1]'),
        ('Which novel by Harriet Beecher Stowe strengthened northern opposition to slavery?', 'Uncle Tom\'s Cabin', ['The Liberator', 'The Impending Crisis of the South', 'Leaves of Grass'], '[1]'),
    ],
    'why': [
        ('the Mexican War increased sectional tension', ['It raised the question of slavery in the new territories', 'The Wilmot Proviso divided Congress on sectional lines', 'Many northerners saw it as a war to extend slavery', 'Gold in California made a decision urgent'],
         'by adding vast new territory, the war forced the question of slavery\'s expansion back into national politics'),
        ('the Compromise of 1850 was agreed', ['California\'s application for statehood forced a decision', 'Clay, Webster and Douglas worked for compromise', 'The death of President Taylor removed an obstacle and Fillmore supported it',
                                               'Douglas passed the measures as separate bills with different majorities', 'Most Americans still wanted to save the Union'],
         'it was passed through political skill rather than genuine agreement, as each measure had a different majority'),
    ],
    'claims': [
        ('The Compromise of 1850 admitted California as a slave state.', False, 'California was admitted as a free state.'),
        ('The Wilmot Proviso became law in 1846.', False, 'It passed the House but was defeated in the Senate.'),
        ('The Fugitive Slave Act denied people accused of escaping from slavery a jury trial.', True, 'Cases were heard by commissioners, who were paid more for returning a person to slavery.'),
    ],
    'ess': [
        dict(q='‘The Compromise of 1850 settled the issue of slavery in the territories.’',
             pro=['It admitted California as free and left Utah and New Mexico to popular sovereignty', 'It calmed the crisis of 1849-50 and secession talk died down', 'Both main parties accepted it as a final settlement in 1852'],
             con=['The Fugitive Slave Act increased northern hostility to slavery', 'Popular sovereignty was vague and was soon extended to Kansas-Nebraska', 'It was an armistice rather than a compromise: no majority supported the whole package'],
             judge='it ended the immediate crisis but settled nothing, because the principle of popular sovereignty reopened the question in 1854'),
        dict(q='To what extent did westward expansion cause the growth of sectional conflict between 1845 and 1850?',
             pro=['The Mexican War added territory whose status divided the sections', 'The Wilmot Proviso split Congress on sectional lines', 'California\'s statehood threatened the balance in the Senate'],
             con=['Slavery itself, and moral opposition to it, was the deeper cause', 'Abolitionism and fugitive slave cases raised tension independently', 'Political leaders reached compromise in 1850, showing expansion need not cause conflict'],
             judge='expansion was the main trigger of conflict in these years because it turned slavery into a question about the future of the West'),
    ],
    'src': [
        S('a speech by a northern Free Soil congressman, 1848 (illustrative)', 'We do not ask to touch slavery where it is. We ask only that the free soil won from Mexico shall stay free for free labour.',
          'northern attitudes to the new territories', 'It shows northerners opposed the spread of slavery into the West while accepting it in the South.',
          'To win support for the Free Soil position.', 'it reflects Free Soil arguments of the time', 'it is a political speech for a new party seeking votes',
          'It does not show southern views.', stance=False, why='it shows that northerners would not accept slavery in the new territories, which the Compromise did not resolve'),
        S('a newspaper in a southern state, 1850 (illustrative)', 'The Union is saved. The South has her Fugitive Slave Law and the North has California. Let agitation now cease.',
          'reactions to the Compromise of 1850', 'It suggests some southerners saw the Compromise as a final settlement.',
          'To encourage acceptance of the Compromise among its readers.', 'it shows opinion at the time of the Compromise', 'a single newspaper may reflect the views of its editor and party',
          'It does not show the northern reaction to the Fugitive Slave Act.', stance=True, why='it presents the Compromise as ending agitation'),
    ],
})

a4c = T('Kansas-Nebraska, Dred Scott and the rise of the Republican Party', 'kansas-nebraska', 'dred scott', 'republican party')
build_as(a4c, {
    'enq': 'the growth of sectional conflict in the 1850s', 'claim': 'the Kansas-Nebraska Act was the most important cause of the rise of the Republican Party',
    'stim': ['The Kansas-Nebraska Act of 1854 allowed settlers in those territories to decide on slavery by popular sovereignty.', 'In March 1857 the Supreme Court gave its decision in Dred Scott v. Sandford.',
             'In 1856 the Republican candidate, John C. Frémont, won eleven northern states.'],
    'terms': [
        ('Bleeding Kansas', 'the violence between pro-slavery and free-state settlers in Kansas in 1854-58'),
        ('Know-Nothings', 'the anti-immigrant, anti-Catholic American Party that grew rapidly in 1854-55'),
        ('Slave Power', 'the northern belief that a conspiracy of slaveholders controlled the federal government'),
        ('Lecompton Constitution', 'the pro-slavery constitution for Kansas of 1857, backed by President Buchanan but rejected by Congress'),
        ('Freeport Doctrine', 'Douglas\'s argument in 1858 that settlers could keep slavery out of a territory by refusing to pass laws to protect it'),
        ('free labour ideology', 'the Republican belief that free men working for wages could rise to own property, which slavery threatened'),
    ],
    'dates': [('the Kansas-Nebraska Act was passed', 1854), ('Senator Charles Sumner was beaten in the Senate chamber', 1856, 5), ('the Supreme Court decided the Dred Scott case', 1857, 3),
              ('Lincoln and Douglas held a series of debates in Illinois', 1858), ('John Brown raided Harpers Ferry', 1859, 10)],
    'mcq': [
        ('Who introduced the Kansas-Nebraska Act?', 'Stephen Douglas', ['Abraham Lincoln', 'Henry Clay', 'James Buchanan'], '[1]'),
        ('What did the Supreme Court rule in the Dred Scott case?', 'That Black Americans were not citizens and Congress could not ban slavery in the territories', ['That slavery was unconstitutional', 'That popular sovereignty must decide every case', 'That Kansas must be a free state'], 'The opinion was written by Chief Justice Taney. [1]'),
        ('Which earlier settlement did the Kansas-Nebraska Act in effect repeal?', 'The Missouri Compromise', ['The Compromise of 1850', 'The Treaty of Guadalupe Hidalgo', 'The Wilmot Proviso'], '[1]'),
    ],
    'why': [
        ('the Republican Party grew rapidly between 1854 and 1856', ['The Kansas-Nebraska Act outraged northerners by opening land closed to slavery', 'Bleeding Kansas and the beating of Sumner seemed to prove the aggression of the Slave Power',
                                                                     'The Whig Party collapsed, leaving voters without a home', 'The free labour ideology appealed to northern farmers and workers', 'The Know-Nothings declined, and many joined the Republicans'],
         'Kansas-Nebraska provided the issue, but the collapse of the Whigs gave the Republicans the opportunity'),
        ('the Dred Scott decision increased sectional tension', ['It declared the Missouri Compromise unconstitutional', 'It implied slavery could not be banned in any territory, undermining both the Republicans and popular sovereignty',
                                                                   'Northerners saw it as proof of a Slave Power conspiracy', 'It encouraged southern demands for federal protection of slavery in the territories'],
         'it raised tension by making compromise impossible: the Republican programme was declared unconstitutional'),
    ],
    'claims': [
        ('The Kansas-Nebraska Act banned slavery in Kansas.', False, 'It left the decision to the settlers through popular sovereignty.'),
        ('The Republican Party was founded in 1854.', True, 'It formed in response to the Kansas-Nebraska Act.'),
        ('The Dred Scott decision declared that Congress could ban slavery in the territories.', False, 'It ruled that Congress had no power to ban slavery there.'),
    ],
    'ess': [
        dict(q='‘The Kansas-Nebraska Act was the most important cause of the rise of the Republican Party.’',
             pro=['It reopened the issue of slavery in territory closed to it since 1820', 'It led directly to the founding of the party in 1854', 'Bleeding Kansas kept the issue alive'],
             con=['The collapse of the Whig Party left voters looking for a new party', 'Nativism and the decline of the Know-Nothings brought in voters', 'Dred Scott and the Lecompton constitution deepened fears of the Slave Power', 'The free labour ideology had wide appeal'],
             judge='Kansas-Nebraska was the trigger and the most important single cause, but the party became a major force because the Whigs collapsed and later events confirmed fears of the Slave Power'),
        dict(q='To what extent was the breakdown of the second party system responsible for the sectional crisis of the 1850s?',
             pro=['The collapse of the Whigs ended a national party that had bridged the sections', 'Sectional parties made compromise harder', 'The Democratic Party split in 1860'],
             con=['Slavery was the issue that caused the parties to break down', 'Events such as Kansas, Dred Scott and Harpers Ferry polarised opinion', 'Leaders such as Douglas and Buchanan made mistakes'],
             judge='the collapse of national parties made the crisis much harder to manage, but slavery was the issue that broke them'),
    ],
    'src': [
        S('Abraham Lincoln, "House Divided" speech, June 1858 (abridged)', 'A house divided against itself cannot stand. I believe this government cannot endure, permanently half slave and half free.',
          'Republican views of slavery', 'Lincoln argues that the Union cannot survive permanently half slave and half free.',
          'To accept the Republican nomination for the Senate and attack Douglas\'s popular sovereignty.', 'it is Lincoln\'s own words at the time', 'it was a campaign speech intended to win votes and define his difference from Douglas',
          'It does not show how Lincoln planned to deal with slavery in the states.', stance=True, why='it shows Republicans believed slavery\'s expansion threatened the Union, the issue raised by Kansas-Nebraska'),
        S('a letter from a former Whig in Ohio, 1855 (illustrative)', 'The Whig party is dead. I cannot vote Democrat after Nebraska, and the Know-Nothings care only for the Pope. The new Republican party is the only home left to us.',
          'why voters joined the Republicans', 'It suggests voters joined the Republicans because the Whigs had collapsed and they opposed the Kansas-Nebraska Act.',
          'To explain his political choice privately.', 'it is a private, contemporary view', 'one voter\'s view may not be typical',
          'It does not show the views of southerners.', stance=False, why='it stresses the collapse of the Whigs as well as Nebraska'),
    ],
})

a4d = T("Lincoln's election, secession and the outbreak of war in 1861", "lincoln's election", 'secession', 'outbreak of war in 1861')
build_as(a4d, {
    'enq': 'secession and the outbreak of war', 'claim': 'the southern states seceded mainly to protect slavery',
    'stim': ['In November 1860 Lincoln won the presidency without carrying a single state in the Deep South.', 'South Carolina seceded from the Union on 20 December 1860.',
             'Confederate guns opened fire on Fort Sumter on 12 April 1861.'],
    'terms': [
        ('secession', 'the withdrawal of a state from the Union'),
        ('Confederate States of America', 'the government formed by the seceded states in February 1861, with Jefferson Davis as president'),
        ('Crittenden Compromise', 'the proposal of December 1860 to extend the 36°30′ line to the Pacific, rejected by Republicans'),
        ('upper South', 'the slave states such as Virginia, North Carolina, Tennessee and Arkansas that seceded only after Fort Sumter'),
        ('border states', 'the slave states of Delaware, Maryland, Kentucky and Missouri that stayed in the Union'),
        ('fire-eaters', 'radical southern secessionists such as Edmund Ruffin and William Yancey'),
    ],
    'dates': [('Lincoln was elected president', 1860, 11), ('South Carolina seceded', 1860, 12), ('the Confederate States of America was formed', 1861, 2),
              ('Lincoln was inaugurated', 1861, 3), ('Confederate forces fired on Fort Sumter', 1861, 4)],
    'mcq': [
        ('Roughly what share of the popular vote did Lincoln win in 1860?', 'About 40 per cent', ['About 60 per cent', 'About 25 per cent', 'About 52 per cent'], 'He won a majority of electoral votes from the free states. [1]'),
        ('Which candidate did southern Democrats nominate in 1860?', 'John C. Breckinridge', ['Stephen Douglas', 'John Bell', 'Jefferson Davis'], 'The Democratic Party split in 1860. [1]'),
        ('How many states had seceded before Lincoln\'s inauguration?', 'Seven', ['Four', 'Eleven', 'Fifteen'], 'The Deep South states; four more seceded after Fort Sumter. [1]'),
        ('Why was Fort Sumter significant in April 1861?', 'Lincoln sent supplies, and the Confederate attack on it began the war', ['It was the Confederate capital', 'It was where Lincoln was inaugurated', 'It was the site of the first Union victory'], '[1]'),
    ],
    'why': [
        ('the Deep South seceded after Lincoln\'s election', ['Southerners feared a Republican president would threaten slavery in the long term', 'Lincoln had won without any southern votes, showing the South had lost power in the Union',
                                                              'Fire-eaters had prepared opinion for secession', 'John Brown\'s raid had increased fears of slave rebellion', 'They believed in the right of states to leave the Union'],
         'secession was a response to the loss of southern power, which secessionists believed made slavery unsafe in the Union'),
        ('attempts at compromise failed in 1860-61', ['Lincoln and the Republicans refused to allow slavery to expand into the territories', 'Secessionists did not want compromise', 'Buchanan was weak and did little', 'Neither side trusted the other after the events of the 1850s'],
         'compromise failed because the one issue that mattered, the expansion of slavery, was the one neither side would give way on'),
    ],
    'claims': [
        ('Lincoln promised in 1860 to abolish slavery in the southern states.', False, 'He opposed the expansion of slavery but said he had no intention of interfering with it where it existed.'),
        ('Virginia seceded after the attack on Fort Sumter.', True, 'Virginia seceded in April 1861 after Lincoln called for 75,000 volunteers.'),
        ('All the slave states joined the Confederacy.', False, 'Delaware, Maryland, Kentucky and Missouri stayed in the Union.'),
    ],
    'ess': [
        dict(q='‘The southern states seceded mainly to protect slavery.’',
             pro=['The declarations of causes of states such as South Carolina and Mississippi stressed slavery', 'Fear of Republican hostility to slavery followed Lincoln\'s election', 'Alexander Stephens called slavery the cornerstone of the Confederacy'],
             con=['Southerners argued for states\' rights and constitutional liberty', 'Loss of political power in the Union alarmed southern leaders', 'The upper South seceded mainly in response to Lincoln\'s call for troops'],
             judge='states\' rights arguments were real, but the right the seceding states most wanted to defend was the right to hold slaves'),
        dict(q='How far was Lincoln responsible for the outbreak of war in 1861?',
             pro=['He refused to accept the Crittenden Compromise', 'He decided to resupply Fort Sumter', 'His call for 75,000 volunteers drove the upper South to secede'],
             con=['The Deep South seceded before he took office', 'The Confederacy fired the first shots', 'He tried to avoid provocation, sending only food to Sumter'],
             judge='Lincoln was determined to preserve the Union, but responsibility for the outbreak lies mainly with the secessionists who left before he took office and fired first'),
    ],
    'src': [
        S('South Carolina\'s Declaration of the Immediate Causes of Secession, December 1860 (abridged)', 'An increasing hostility on the part of the non-slaveholding States to the institution of slavery has led to a disregard of their obligations.',
          'the reasons for secession', 'It shows South Carolina justified secession by northern hostility to slavery.',
          'To justify secession to the people of the state and the world.', 'it is the official statement of the first state to secede', 'it was written to justify a decision already made',
          'It does not show the views of non-slaveholding southern whites.', stance=True, why='it names hostility to slavery as the reason for secession'),
        S('Alexander Stephens, vice-president of the Confederacy, "Cornerstone" speech, March 1861 (abridged)', 'Our new government is founded upon the great truth that the negro is not equal to the white man; that slavery, subordination to the superior race, is his natural and normal condition.',
          'the purpose of the Confederacy', 'Stephens openly states that the Confederacy was founded to defend slavery and racial inequality.',
          'To explain the new Confederate constitution to a southern audience.', 'it is the words of a Confederate leader at the time', 'it was an improvised speech and Stephens later claimed it was misreported',
          'It does not show why the upper South seceded later.', stance=True, why='it shows slavery as the cornerstone of the new nation'),
        S('a speech by a southern Unionist, 1861 (illustrative)', 'We are told the North means to march armies against us. I will stand by Virginia; I did not want to leave the Union, but I will not fight my neighbours.',
          'why the upper South seceded', 'It suggests some southerners seceded out of loyalty to their state when war came, not to protect slavery.',
          'To explain why a Unionist would follow his state.', 'it shows the dilemma of upper South Unionists', 'it is one person\'s view and illustrative',
          'It does not reflect the views of the Deep South.', stance=False, why='it suggests loyalty to the state and opposition to coercion'),
    ],
})

CHAPTERS[4] = [a4a, a4b, a4c, a4d]


# ============================================================== CHAPTER 5: American option, Civil War and Reconstruction, 1861-77

c5a = T('Why the Union won the Civil War', 'union won the civil war', 'why the union won')
build_as(c5a, {
    'enq': 'why the Union won the Civil War', 'claim': 'the Union won mainly because of its greater economic resources',
    'stim': ['In 1861 the Union states had about 22 million people; the Confederacy about 9 million, of whom about 3.5 million were enslaved.', 'In July 1863 the Union won at Gettysburg and captured Vicksburg.',
             'Lee surrendered to Grant at Appomattox Court House on 9 April 1865.'],
    'terms': [
        ('Anaconda Plan', 'General Winfield Scott\'s strategy of blockading the South and controlling the Mississippi to strangle the Confederacy'),
        ('total war', 'warfare directed at the enemy\'s economy and civilian morale as well as its armies, as in Sherman\'s march'),
        ('King Cotton diplomacy', 'the Confederate belief that Britain and France would intervene to secure cotton supplies'),
        ('blockade runners', 'fast ships that tried to evade the Union naval blockade of southern ports'),
        ('war of attrition', 'a war won by wearing down the enemy\'s resources and manpower'),
        ('Copperheads', 'northern Democrats who opposed the war and wanted a negotiated peace'),
    ],
    'dates': [('the First Battle of Bull Run was fought', 1861, 7), ('the Battle of Antietam was fought', 1862, 9), ('the Battle of Gettysburg was fought', 1863, 7.01),
              ('Grant became general-in-chief of the Union armies', 1864, 3), ('Sherman captured Atlanta', 1864, 9), ('Lee surrendered at Appomattox', 1865, 4)],
    'mcq': [
        ('Which Union victory in July 1863 gave the Union control of the Mississippi River?', 'Vicksburg', ['Gettysburg', 'Antietam', 'Chancellorsville'], 'It surrendered on 4 July 1863, splitting the Confederacy. [1]'),
        ('Why did Britain not intervene on the side of the Confederacy?', 'It had other sources of cotton and opposed slavery, especially after the Emancipation Proclamation', ['It was at war with France', 'It had abolished its navy', 'The Confederacy refused to sell it cotton'], '[1]'),
        ('Which Union general led the march from Atlanta to the sea in 1864?', 'William T. Sherman', ['George McClellan', 'Ulysses S. Grant', 'George Meade'], '[1]'),
        ('About how many Black soldiers served in the Union army?', 'About 180,000', ['About 18,000', 'About 1.8 million', 'None'], 'Around 10 per cent of the Union army by 1865. [1]'),
    ],
    'why': [
        ('the Union won the Civil War', ['Greater population, industry and railways allowed it to sustain a long war', 'The naval blockade strangled the southern economy', 'Grant and Sherman fought a war of attrition and destroyed southern resources',
                                         'Lincoln\'s leadership kept the North committed to the war', 'The Confederacy failed to win foreign recognition'],
         'superior resources were decisive once the Union had leaders, such as Lincoln and Grant, willing to use them in a war of attrition'),
        ('the Confederacy was unable to win foreign recognition', ['Britain had built up stocks of cotton and found other suppliers', 'Union victory at Antietam in 1862 ended the moment when Britain considered mediation',
                                                                    'The Emancipation Proclamation made the war a war against slavery, which British opinion opposed', 'Britain feared war with the United States and depended on northern grain'],
         'the Confederacy never won a victory decisive enough to persuade Britain that intervention was safe'),
    ],
    'claims': [
        ('The Confederacy had more railway mileage than the Union.', False, 'The Union had more than twice as much.'),
        ('Lee invaded the North twice, at Antietam and at Gettysburg.', True, 'Both invasions ended in retreat.'),
        ('The Union blockade was completely effective from 1861.', False, 'It was porous at first but became steadily more effective.'),
    ],
    'ess': [
        dict(q='‘The Union won the Civil War mainly because of its greater economic resources.’',
             pro=['The Union had far more industry, railways and money', 'Its larger population allowed it to replace losses', 'The blockade and economic strength wore down the South'],
             con=['Union leadership, especially Lincoln and Grant, was vital', 'Confederate weaknesses, such as states\' rights disputes and inflation, undermined its war effort', 'Key victories such as Gettysburg, Vicksburg and Atlanta were not inevitable', 'Emancipation and Black soldiers strengthened the Union'],
             judge='resources gave the Union a decisive advantage in a long war, but it took effective leadership and military victories to convert them into victory'),
        dict(q='How far was poor Confederate leadership responsible for the defeat of the South?',
             pro=['Davis quarrelled with state governors and generals', 'Lee\'s offensive strategy wasted scarce manpower at Gettysburg', 'The Confederacy failed to manage its finances, causing huge inflation'],
             con=['The South was outnumbered and out-produced', 'Lee was a skilled commander who won many battles against the odds', 'Union leaders such as Lincoln and Grant were the main reason for defeat'],
             judge='Confederate leadership had weaknesses, but the South lost mainly because it could not match Union resources once the North found effective leaders'),
    ],
    'src': [
        S('a letter from a Confederate officer, 1864 (illustrative)', 'We are beaten not by their courage but by their numbers. For every man we lose they bring two, and our men are barefoot while theirs have new boots and full wagons.',
          'the reasons for Confederate defeat', 'It suggests the Confederacy was overwhelmed by northern numbers and resources.',
          'To explain the army\'s difficulties to his family.', 'he had direct experience of the war', 'Confederates had reasons to blame numbers rather than their own failings (the later "Lost Cause" argument)',
          'It does not show the role of Union generals or Confederate political problems.', stance=True, why='it stresses northern numbers and supplies'),
        S('a speech by a Union general, 1865 (illustrative)', 'It was not numbers alone. We won when we learned to fight as one army, under one plan, and to strike at the South\'s railways, crops and will to resist.',
          'the reasons for Union victory', 'It suggests Union strategy and leadership, not just resources, won the war.',
          'To celebrate the army\'s achievement after victory.', 'he had direct knowledge of Union strategy', 'he had reasons to emphasise the skill of the generals',
          'It does not discuss the blockade or foreign policy.', stance=False, why='it stresses strategy and leadership rather than resources'),
    ],
})

c5b = T('The Emancipation Proclamation and the end of slavery', 'emancipation proclamation', 'end of slavery')
build_as(c5b, {
    'enq': 'the end of slavery', 'claim': 'Lincoln issued the Emancipation Proclamation mainly as a military measure',
    'stim': ['Lincoln issued the preliminary Emancipation Proclamation on 22 September 1862, five days after Antietam.', 'The final Emancipation Proclamation took effect on 1 January 1863.',
             'The Thirteenth Amendment, abolishing slavery throughout the United States, was ratified in December 1865.'],
    'terms': [
        ('contrabands', 'enslaved people who escaped to Union lines, treated as captured enemy property from 1861'),
        ('Confiscation Acts', 'laws of 1861 and 1862 allowing Union forces to seize property, including enslaved people, used to support the rebellion'),
        ('Thirteenth Amendment', 'the amendment to the Constitution that abolished slavery throughout the United States, ratified in 1865'),
        ('United States Colored Troops', 'the units of Black soldiers raised by the Union army from 1863'),
        ('Radical Republicans', 'the members of the Republican Party who pressed for immediate emancipation and equal rights'),
        ('gradual compensated emancipation', 'Lincoln\'s early proposal that states free enslaved people over time with payment to owners'),
    ],
    'dates': [('the First Confiscation Act was passed', 1861, 8), ('the preliminary Emancipation Proclamation was issued', 1862, 9), ('the Emancipation Proclamation took effect', 1863, 1),
              ('Black soldiers of the 54th Massachusetts attacked Fort Wagner', 1863, 7), ('the Thirteenth Amendment was ratified', 1865, 12)],
    'mcq': [
        ('Which enslaved people did the Emancipation Proclamation declare free?', 'Those in areas in rebellion against the United States', ['All enslaved people in the United States', 'Only those in the border states', 'Only those who had served in the army'], 'It excluded the border states and Union-held areas. [1]'),
        ('Why did Lincoln wait for a Union victory before announcing emancipation?', 'So that it would not look like a desperate measure', ['Because Congress had banned it', 'Because the border states demanded it', 'Because Britain had asked him to'], 'Antietam provided the victory. [1]'),
        ('Which African American leader urged Lincoln to make the war a war against slavery and to enlist Black soldiers?', 'Frederick Douglass', ['Booker T. Washington', 'W. E. B. Du Bois', 'Hiram Revels'], '[1]'),
    ],
    'why': [
        ('Lincoln issued the Emancipation Proclamation', ['It weakened the Confederacy by attacking its labour force', 'It allowed the recruitment of Black soldiers', 'It made foreign intervention on the side of the South less likely',
                                                           'Enslaved people escaping to Union lines had already undermined slavery', 'Lincoln had come to see emancipation as a moral and political necessity'],
         'it was presented as a military measure, which made it constitutional, but it reflected a political and moral shift'),
        ('slavery collapsed in the South during the war', ['Enslaved people fled to Union lines in large numbers', 'Union armies freed people as they advanced', 'The Confiscation Acts and the Proclamation gave legal backing',
                                                           'Black soldiers fought for freedom', 'The Thirteenth Amendment made abolition permanent'],
         'slavery was destroyed by the actions of enslaved people and Union armies, then made permanent by law'),
    ],
    'claims': [
        ('The Emancipation Proclamation freed enslaved people in Kentucky and Maryland.', False, 'It did not apply to the border states that stayed in the Union.'),
        ('The Proclamation allowed Black men to enlist in the Union army and navy.', True, 'About 180,000 served in the army.'),
        ('Lincoln always aimed to abolish slavery from the start of the war.', False, 'At first his aim was to preserve the Union; his policy on slavery developed during the war.'),
    ],
    'ess': [
        dict(q='‘Lincoln issued the Emancipation Proclamation mainly as a military measure.’',
             pro=['It was justified as a war measure under his powers as commander-in-chief', 'It applied only to areas in rebellion, where it would damage the enemy', 'It opened the way to recruiting Black soldiers'],
             con=['Lincoln had long opposed slavery morally', 'Pressure from Radicals, abolitionists and Black leaders shaped the decision', 'It aimed to prevent British and French recognition of the Confederacy', 'Enslaved people\'s own flight forced the issue'],
             judge='it was framed as a military measure for constitutional reasons, but it reflected moral conviction and political pressure as much as military need'),
        dict(q='To what extent did enslaved people free themselves during the Civil War?',
             pro=['Hundreds of thousands fled to Union lines', 'Escapes forced Union commanders and Congress to act', 'Black soldiers fought for the Union'],
             con=['Union armies were needed to make freedom real', 'The Proclamation and Thirteenth Amendment provided legal freedom', 'Many enslaved people far from Union lines remained enslaved until 1865'],
             judge='enslaved people played a central role in destroying slavery, but their freedom depended on Union victory and federal law'),
    ],
    'src': [
        S('Abraham Lincoln, letter to Horace Greeley, August 1862 (abridged)', 'My paramount object in this struggle is to save the Union, and is not either to save or to destroy slavery. If I could save the Union without freeing any slave I would do it.',
          'Lincoln\'s war aims', 'Lincoln states that saving the Union, not ending slavery, was his main aim.',
          'To prepare public opinion for emancipation by presenting it as a means of saving the Union.', 'it is Lincoln\'s own public statement', 'he had already drafted the Proclamation and wrote to shape opinion, so it may conceal his intentions',
          'It does not mention his personal hatred of slavery, which he stated in the same letter.', stance=True, why='it presents emancipation as a means to win the war and save the Union'),
        S('a speech by Frederick Douglass, 1863 (summary)', 'Douglass welcomed the Proclamation as the start of a war for freedom, but criticised its limits and urged that Black men be allowed to fight so that they could claim citizenship.',
          'African American views of emancipation', 'It shows that Black leaders saw emancipation as a moral cause and a route to citizenship.',
          'To encourage Black enlistment and push for wider rights.', 'Douglass was the leading African American spokesman of the time', 'he was campaigning and had political aims',
          'It does not show Lincoln\'s reasons.', stance=False, why='it presents emancipation as a moral cause, not only a military measure'),
    ],
})

c5c = T('Presidential and Radical Reconstruction', 'presidential and radical reconstruction', 'radical reconstruction')
build_as(c5c, {
    'enq': 'Reconstruction', 'claim': 'Radical Reconstruction transformed the position of African Americans in the South',
    'stim': ['In 1865-66 southern legislatures passed Black Codes limiting the rights of freed people.', 'The Reconstruction Acts of 1867 divided the former Confederacy into five military districts.',
             'In 1870 Hiram Revels of Mississippi became the first African American to sit in the US Senate.'],
    'terms': [
        ('Black Codes', 'laws passed by southern states in 1865-66 to restrict the rights and labour of freed people'),
        ('Freedmen\'s Bureau', 'the federal agency set up in 1865 to help freed people with food, schools, labour contracts and legal disputes'),
        ('Fourteenth Amendment', 'the amendment of 1868 that defined citizenship and guaranteed equal protection of the laws'),
        ('Fifteenth Amendment', 'the amendment of 1870 forbidding states to deny the vote on grounds of race'),
        ('carpetbaggers', 'the hostile name for northerners who moved south during Reconstruction'),
        ('scalawags', 'the hostile name for white southerners who supported the Republicans'),
        ('Ten Percent Plan', 'Lincoln\'s plan of 1863 to readmit a state when 10 per cent of its 1860 voters took an oath of loyalty'),
    ],
    'dates': [('Lincoln announced the Ten Percent Plan', 1863, 12), ('Congress passed the Civil Rights Act over Johnson\'s veto', 1866, 4), ('the first Reconstruction Act was passed', 1867, 3),
              ('Andrew Johnson was impeached', 1868, 2), ('the Fifteenth Amendment was ratified', 1870, 2)],
    'mcq': [
        ('Why was President Andrew Johnson impeached in 1868?', 'He dismissed the Secretary of War in defiance of the Tenure of Office Act', ['He vetoed the Thirteenth Amendment', 'He refused to end the war', 'He was found guilty of corruption'], 'He was acquitted by one vote in the Senate. [1]'),
        ('What did the Reconstruction Acts of 1867 require before southern states could be readmitted?', 'New constitutions with Black male suffrage and ratification of the Fourteenth Amendment', ['Payment of war reparations', 'Abolition of state governments', 'Election of Union generals as governors'], '[1]'),
        ('Which group led Congressional opposition to Johnson\'s policies?', 'The Radical Republicans, such as Thaddeus Stevens and Charles Sumner', ['The Copperheads', 'The Know-Nothings', 'The Redeemers'], '[1]'),
    ],
    'why': [
        ('Congress took control of Reconstruction from President Johnson in 1866-67', ['Johnson\'s lenient terms allowed former Confederates back into power', 'Southern states passed Black Codes', 'Violence such as the Memphis and New Orleans riots of 1866 shocked the North',
                                                                                         'Johnson vetoed the Freedmen\'s Bureau and Civil Rights bills', 'Republicans won large majorities in the 1866 elections'],
         'the South\'s defiance under Johnson\'s plan persuaded northern voters that stronger federal action was needed'),
        ('Radical Reconstruction achieved only limited change for African Americans', ['Most freed people did not get land and became sharecroppers', 'White violence, including the Ku Klux Klan, intimidated Black voters', 'Federal enforcement was limited and declined after 1872', 'Northern commitment to racial equality was shallow'],
         'without land or lasting federal protection, the political gains of Radical Reconstruction were vulnerable'),
    ],
    'claims': [
        ('The Fourteenth Amendment guaranteed equal protection of the laws.', True, 'It was ratified in 1868.'),
        ('Freed people were given forty acres of land each by Congress.', False, 'Sherman\'s Field Order 15 promised land in some coastal areas, but Johnson reversed it and Congress never redistributed land.'),
        ('African Americans held public office in the South during Reconstruction.', True, 'Hundreds served in state legislatures, and some in Congress.'),
    ],
    'ess': [
        dict(q='‘Radical Reconstruction transformed the position of African Americans in the South.’',
             pro=['The Fourteenth and Fifteenth Amendments gave citizenship and the vote', 'Hundreds of African Americans held office', 'Schools, churches and families were built or reunited with Freedmen\'s Bureau support'],
             con=['Most remained landless sharecroppers', 'Violence by the Klan and others limited freedom', 'The gains were reversed after 1877'],
             judge='Radical Reconstruction brought revolutionary legal and political change, but without economic independence it did not transform daily life for most freed people'),
        dict(q='How far was Andrew Johnson responsible for the failure of Presidential Reconstruction?',
             pro=['He pardoned many former Confederates', 'He tolerated the Black Codes', 'He vetoed civil rights legislation and alienated moderate Republicans'],
             con=['White southerners resisted any change to racial hierarchy', 'Lincoln\'s lenient plan had set the pattern', 'Congress was divided on how far to go'],
             judge='Johnson\'s policies and stubbornness made the failure worse, but southern white resistance was the underlying cause'),
    ],
    'src': [
        S('extract from a Black Code of a southern state, 1865 (summary)', 'Freed people were required to sign annual labour contracts; those without them could be arrested for vagrancy and hired out to employers.',
          'the Black Codes', 'It shows that southern states tried to control the labour and movement of freed people.',
          'To keep freed people working on plantations under white control.', 'it is a law passed at the time', 'it shows what the law said, not how strictly it was enforced',
          'It does not show the reaction of the North.', stance=None),
        S('a letter from a Freedmen\'s Bureau agent in Georgia, 1868 (illustrative)', 'The freedmen have voted and some now sit in the legislature, but on the plantations little has changed. Without land they must work on whatever terms the planter offers, and the night riders punish any who resist.',
          'the impact of Radical Reconstruction', 'It suggests political change had happened but economic dependence and violence remained.',
          'To report on conditions to his superiors.', 'Bureau agents saw conditions at first hand', 'agents had reasons to stress problems to secure more support',
          'It does not show change in cities or in education.', stance=False, why='it shows the limits of change in daily life'),
        S('a speech by a Black member of a southern state legislature, 1868 (illustrative)', 'Three years ago we were slaves; today we make laws. We have built schools in every county and we shall not go back.',
          'the achievements of Reconstruction', 'It suggests Radical Reconstruction brought dramatic political and educational change.',
          'To celebrate achievements and encourage supporters.', 'it shows the views of a Black politician at the time', 'it is a political speech intended to inspire',
          'It does not mention violence or economic hardship.', stance=True, why='it shows political and educational transformation'),
    ],
})

c5d = T('Why Reconstruction ended in 1877 and its legacy', 'reconstruction ended in 1877', 'legacy')
build_as(c5d, {
    'enq': 'the end of Reconstruction', 'claim': 'Reconstruction ended mainly because the North lost interest',
    'stim': ['In 1876 the presidential election between Hayes and Tilden was disputed.', 'In April 1877 the last federal troops protecting Republican governments in South Carolina and Louisiana were withdrawn.',
             'The Panic of 1873 began a long economic depression in the United States.'],
    'terms': [
        ('Redeemers', 'southern Democrats who regained control of state governments from the Republicans in the 1870s'),
        ('Compromise of 1877', 'the informal agreement by which Hayes became president and federal troops were withdrawn from the South'),
        ('Mississippi Plan', 'the use of violence and intimidation by Democrats in 1875 to prevent Black people voting'),
        ('Enforcement Acts', 'laws of 1870-71, including the Ku Klux Klan Act, to protect Black voters'),
        ('sharecropping', 'farming land owned by another in return for a share of the crop, which often trapped families in debt'),
        ('Jim Crow', 'the system of racial segregation laws in the South from the late nineteenth century'),
    ],
    'dates': [('the Ku Klux Klan Act was passed', 1871), ('the Panic of 1873 began', 1873), ('Democrats used the Mississippi Plan to win state elections', 1875),
              ('the disputed Hayes-Tilden election was held', 1876, 11), ('federal troops were withdrawn from the last southern state capitals', 1877, 4)],
    'mcq': [
        ('Which Supreme Court case of 1873 narrowed the protection given by the Fourteenth Amendment?', 'The Slaughterhouse Cases', ['Dred Scott v. Sandford', 'Plessy v. Ferguson', 'Brown v. Board of Education'], '[1]'),
        ('Who became president as a result of the Compromise of 1877?', 'Rutherford B. Hayes', ['Samuel Tilden', 'Ulysses S. Grant', 'Andrew Johnson'], '[1]'),
        ('What happened at Colfax, Louisiana, in 1873?', 'A white militia massacred dozens of Black men', ['Federal troops arrested the Klan leadership', 'The first Black governor was elected', 'The Freedmen\'s Bureau was founded'], '[1]'),
    ],
    'why': [
        ('Reconstruction ended in 1877', ['Northern voters were preoccupied with the depression after 1873', 'Corruption scandals under Grant discredited Republican governments', 'White southern violence and intimidation restored Democratic control',
                                          'Supreme Court decisions weakened federal protection', 'The disputed 1876 election led to the withdrawal of troops'],
         'the North\'s declining willingness to use federal power allowed white southern violence to succeed'),
        ('African Americans lost many of the rights gained during Reconstruction after 1877', ['Southern states introduced poll taxes and literacy tests', 'Segregation laws spread', 'Violence and lynching went unpunished', 'The Supreme Court allowed segregation in Plessy v. Ferguson (1896)'],
         'once federal protection was withdrawn, southern states could remove rights by law and force'),
    ],
    'claims': [
        ('The Compromise of 1877 was a formal treaty approved by Congress.', False, 'It was an informal political bargain.'),
        ('The Fourteenth and Fifteenth Amendments remained part of the Constitution after 1877.', True, 'They were later the basis of the civil rights movement.'),
        ('The Panic of 1873 made Reconstruction more popular in the North.', False, 'It turned attention to the economy and helped Democrats win the House in 1874.'),
    ],
    'ess': [
        dict(q='‘Reconstruction ended mainly because the North lost interest.’',
             pro=['The depression after 1873 turned attention to economic issues', 'Democrats won the House in 1874', 'Republicans were weary of the cost of enforcing southern governments'],
             con=['White southern violence and intimidation overthrew Republican governments', 'Supreme Court decisions limited federal power', 'Divisions and corruption weakened southern Republican governments'],
             judge='southern violence destroyed Reconstruction state by state, but it could succeed only because the North was no longer willing to intervene'),
        dict(q='To what extent was Reconstruction a failure?',
             pro=['Black political rights were largely lost by 1900', 'Freed people did not gain land', 'Segregation and violence followed'],
             con=['Slavery was abolished permanently', 'The Fourteenth and Fifteenth Amendments became the basis of later civil rights', 'Black churches, schools and communities endured'],
             judge='Reconstruction failed in its immediate aim of securing equal rights, but it left constitutional foundations that were later used to win them'),
    ],
    'src': [
        S('a northern newspaper editorial, 1875 (illustrative)', 'The country is tired of these annual autumn outbreaks in the South. The people want the troops home and the government to attend to the depression.',
          'northern attitudes to Reconstruction', 'It suggests northern opinion was weary of intervention in the South.',
          'To argue for an end to federal intervention.', 'it shows the mood of part of northern opinion', 'a single newspaper reflects its editor\'s politics',
          'It does not show the violence suffered by Black southerners.', stance=True, why='it shows the North losing interest'),
        S('testimony of a Black voter to a congressional committee, 1876 (illustrative)', 'They came to my house at night with guns and said that if I voted Republican I would be found in the river. Many of us did not vote.',
          'the elections of the 1870s', 'It shows intimidation was used to stop Black people voting.',
          'To give evidence of violence to Congress.', 'it is a first-hand account', 'committees sometimes chose witnesses to support a party case',
          'It does not show northern opinion.', stance=False, why='it shows southern violence, not just northern indifference, ended Reconstruction'),
    ],
})

CHAPTERS[5] = [c5a, c5b, c5c, c5d]


# ============================================================== CHAPTER 6: American option, the Gilded Age and Progressive Era, 1870s-1920

g6a = T('Industrialisation, big business and the robber barons', 'industrialisation, big business', 'robber barons')
build_as(g6a, {
    'enq': 'the growth of big business', 'claim': 'the leaders of big business were "robber barons" who harmed the American economy',
    'stim': ['The first transcontinental railroad was completed in 1869.', 'By the 1880s Standard Oil controlled about 90 per cent of oil refining in the United States.',
             'In 1901 J. P. Morgan created US Steel, the first company valued at over a billion dollars.'],
    'terms': [
        ('robber barons', 'the critical name for industrialists and financiers, such as Rockefeller and Vanderbilt, accused of ruthless methods'),
        ('trust', 'a combination in which shareholders of several companies handed control to one board of trustees, as with Standard Oil in 1882'),
        ('vertical integration', 'controlling every stage of production, from raw materials to distribution, as Carnegie did in steel'),
        ('horizontal integration', 'buying up or combining rival firms in the same stage of an industry, as Rockefeller did in oil refining'),
        ('laissez-faire', 'the belief that government should not regulate business'),
        ('Gospel of Wealth', 'Carnegie\'s argument of 1889 that the rich had a duty to use their fortunes for the public good'),
    ],
    'dates': [('the first transcontinental railroad was completed', 1869), ('Standard Oil was founded', 1870), ('the Standard Oil Trust was formed', 1882),
              ('the Interstate Commerce Act was passed', 1887), ('the Sherman Antitrust Act was passed', 1890), ('US Steel was formed', 1901)],
    'mcq': [
        ('Which industrialist built his fortune in steel through vertical integration?', 'Andrew Carnegie', ['John D. Rockefeller', 'Cornelius Vanderbilt', 'J. P. Morgan'], '[1]'),
        ('What did the Sherman Antitrust Act of 1890 make illegal?', 'Combinations in restraint of trade', ['All trade unions', 'Railroad rebates to farmers', 'Imports of foreign steel'], 'It was weakly enforced at first. [1]'),
        ('Which body did the Interstate Commerce Act of 1887 create?', 'The Interstate Commerce Commission', ['The Federal Reserve', 'The Federal Trade Commission', 'The Department of Labor'], 'To regulate railroad rates. [1]'),
    ],
    'why': [
        ('the American economy grew so rapidly after 1870', ['Abundant natural resources such as coal, iron and oil', 'Railroads created a national market', 'Immigration provided cheap labour and consumers',
                                                             'New technology such as the Bessemer process and electricity', 'Government support through tariffs, land grants and laissez-faire policies'],
         'resources and a national market were fundamental, but government policy and entrepreneurs turned them into rapid growth'),
        ('big business combinations such as trusts developed', ['Fierce competition and price wars cut profits', 'Large firms gained economies of scale', 'Railroad rebates favoured big shippers', 'Laws were weak and courts favoured business'],
         'businessmen formed trusts to escape ruinous competition, and weak regulation allowed them to do so'),
    ],
    'claims': [
        ('Rockefeller used rebates from railroads to undercut competitors.', True, 'Secret rebates gave Standard Oil a cost advantage.'),
        ('The Sherman Antitrust Act quickly broke up most trusts in the 1890s.', False, 'It was weakly enforced and was even used against trade unions.'),
        ('The transcontinental railroad was completed in 1869.', True, 'The lines met at Promontory Summit, Utah.'),
    ],
    'ess': [
        dict(q='‘The leaders of big business in the Gilded Age were robber barons who harmed the American economy.’',
             pro=['They used ruthless methods such as rebates, price-cutting and bribery', 'Monopolies kept prices high and crushed small firms', 'Workers suffered low wages and dangerous conditions'],
             con=['They built efficient industries that lowered prices, such as kerosene and steel', 'They created jobs and made the US the leading industrial power', 'Philanthropists such as Carnegie gave away fortunes'],
             judge='their methods were often ruthless, but they were also "industrial statesmen" whose organisation drove growth; the harm fell more on competitors and workers than on the economy as a whole'),
        dict(q='How far was government policy responsible for the rapid industrial growth of the USA after 1870?',
             pro=['High tariffs protected industry', 'Land grants helped build railroads', 'Laissez-faire allowed business to grow without regulation'],
             con=['Natural resources and a large home market were more fundamental', 'Immigration provided labour', 'Entrepreneurs and new technology drove change'],
             judge='government policy helped, but growth depended mainly on resources, markets, labour and enterprise'),
    ],
    'src': [
        S('Andrew Carnegie, The Gospel of Wealth, 1889 (summary)', 'Carnegie argued that competition was hard on individuals but best for the race, and that the rich should use their surplus wealth during their lifetimes for the good of the community.',
          'the views of industrialists', 'It shows Carnegie defending competition and wealth while arguing for philanthropy.',
          'To justify great fortunes and encourage philanthropy.', 'it shows the views of a leading industrialist', 'Carnegie was defending himself and his class',
          'It does not show the views of workers.', stance=False, why='it presents big business as beneficial'),
        S('a cartoon in a popular magazine, 1880s (description)', 'The cartoon shows a giant oil tank with tentacles wrapped around the Capitol, a state house and small businesses.',
          'public attitudes to Standard Oil', 'It shows Standard Oil as a monopoly that controlled government and crushed small firms.',
          'To criticise the power of Standard Oil and the trusts.', 'it shows how critics saw the trusts at the time', 'it is satire designed to make a point, not a balanced view',
          'It does not show the lower prices that Standard Oil brought.', stance=True, why='it presents Standard Oil as harmful'),
    ],
})

g6b = T('Immigration, urbanisation and the condition of workers', 'immigration, urbanisation', 'condition of workers')
build_as(g6b, {
    'enq': 'the lives of immigrants and workers', 'claim': 'trade unions were largely ineffective in improving the conditions of workers before 1914',
    'stim': ['About 25 million immigrants arrived in the United States between 1870 and 1920.', 'Ellis Island in New York harbour opened as an immigration station in 1892.',
             'In 1911 a fire at the Triangle Shirtwaist Factory in New York killed 146 workers.'],
    'terms': [
        ('new immigrants', 'immigrants from southern and eastern Europe, such as Italians, Poles and Jews, who arrived in large numbers after about 1880'),
        ('tenement', 'a crowded, poorly built apartment building in which many immigrant families lived'),
        ('nativism', 'hostility to immigrants and the favouring of native-born Americans'),
        ('Knights of Labor', 'a national union open to most workers, which grew rapidly in the 1880s and then declined'),
        ('American Federation of Labor', 'the federation of craft unions for skilled workers founded in 1886 and led by Samuel Gompers'),
        ('political machine', 'a party organisation, such as Tammany Hall, that controlled city politics by exchanging favours for votes'),
    ],
    'dates': [('the Great Railroad Strike took place', 1877), ('the Chinese Exclusion Act was passed', 1882), ('the Haymarket affair took place in Chicago', 1886, 5),
              ('the Homestead strike took place', 1892, 7), ('the Pullman strike was broken by federal troops', 1894, 7), ('the Triangle Shirtwaist fire took place', 1911, 3)],
    'mcq': [
        ('Which law of 1882 banned the immigration of Chinese labourers?', 'The Chinese Exclusion Act', ['The Sherman Act', 'The Dawes Act', 'The Immigration Act of 1924'], '[1]'),
        ('Who wrote How the Other Half Lives (1890), with photographs of New York tenements?', 'Jacob Riis', ['Upton Sinclair', 'Ida Tarbell', 'Lincoln Steffens'], '[1]'),
        ('Why did the Haymarket affair damage the labour movement?', 'A bomb killed police officers and unions were linked with anarchism in the public mind', ['It led to the eight-hour day', 'It caused the AFL to dissolve', 'It brought immigration to an end'], '[1]'),
    ],
    'why': [
        ('so many immigrants came to the USA between 1870 and 1920', ['Jobs in expanding industries pulled migrants to the USA', 'Poverty, rural overpopulation and persecution, such as of Jews in Russia, pushed people out of Europe',
                                                                       'Cheap steamship travel made the journey easier', 'Letters and remittances from earlier migrants encouraged others to follow'],
         'the pull of industrial jobs was the main reason, made easier by cheap transport'),
        ('trade unions found it hard to improve workers\' conditions before 1914', ['Employers used lockouts, blacklists and strike-breakers', 'Courts issued injunctions and federal troops broke strikes such as Pullman', 'Workers were divided by skill, ethnicity and race',
                                                                                    'Plentiful immigrant labour made workers easy to replace', 'Unions were associated with violence and radicalism after Haymarket'],
         'the combined power of employers and the state was the main obstacle, made worse by divisions among workers'),
    ],
    'claims': [
        ('The AFL organised mainly skilled workers in craft unions.', True, 'Gompers focused on wages, hours and conditions for skilled workers.'),
        ('Federal troops supported the strikers in the Pullman strike of 1894.', False, 'Federal troops were sent to break the strike.'),
        ('Most new immigrants after 1880 came from Britain and Germany.', False, 'Most came from southern and eastern Europe.'),
    ],
    'ess': [
        dict(q='‘Trade unions were largely ineffective in improving the conditions of American workers before 1914.’',
             pro=['Major strikes at Homestead and Pullman were defeated', 'Union membership was low, only a small minority of workers', 'The Knights of Labor collapsed after 1886'],
             con=['The AFL won better wages and hours for skilled workers', 'Union pressure contributed to state laws on safety and hours', 'Unions survived and grew after 1900'],
             judge='unions achieved gains for some skilled workers, but most industrial workers saw little benefit before 1914'),
        dict(q='To what extent did immigrants benefit from coming to the USA between 1870 and 1914?',
             pro=['Wages were higher than in Europe', 'Many escaped persecution', 'Some achieved upward mobility for their children'],
             con=['They faced poor housing in tenements and dangerous work', 'Nativism and discrimination', 'Many returned home disappointed'],
             judge='most immigrants gained economically compared with what they left, but at a high cost in living and working conditions'),
    ],
    'src': [
        S('a letter from an Italian immigrant in New York to his family, 1905 (illustrative)', 'I earn in a week what I earned in a month at home, but we are eight in two rooms and the work at the docks is hard and dangerous.',
          'immigrant life', 'It suggests immigrants gained higher wages but faced overcrowding and dangerous work.',
          'To tell his family about his life in America.', 'it is a private, first-hand account', 'one immigrant\'s experience may not be typical',
          'It does not mention trade unions.', stance=None),
        S('a statement by a steel company manager after the Homestead strike, 1892 (illustrative)', 'The men have learned that they cannot dictate to this company. The works are open and the new hands are at their places.',
          'the Homestead strike', 'It suggests the company broke the union and replaced the strikers.',
          'To present the company\'s victory publicly.', 'it reflects the company\'s view at the time', 'it is one-sided and ignores the violence of the strike',
          'It does not show the workers\' grievances.', stance=True, why='it shows a union defeated by a powerful employer'),
        S('a speech by an AFL organiser, 1900s (illustrative)', 'Where we are organised, the eight-hour day and the union wage are won. Where we are not, the bosses take what they please.',
          'the achievements of unions', 'It suggests unions won better hours and wages where they were strong.',
          'To recruit members.', 'it shows the AFL\'s claims at the time', 'it is a recruiting speech and exaggerates success',
          'It does not show the many unorganised workers.', stance=False, why='it claims unions improved conditions'),
    ],
})

g6c = T('Populism and the agrarian protest movement', 'populism', 'agrarian protest')
build_as(g6c, {
    'enq': 'agrarian protest', 'claim': 'the Populist movement was a failure',
    'stim': ['The Grange (Patrons of Husbandry) was founded in 1867.', 'In 1892 the People\'s Party adopted the Omaha Platform.',
             'In 1896 the Democrats nominated William Jennings Bryan on a free silver platform.'],
    'terms': [
        ('Grange', 'the farmers\' organisation founded in 1867 that set up co-operatives and campaigned for railroad regulation'),
        ('Farmers\' Alliances', 'the farmers\' organisations of the 1880s in the South and Midwest that led to the People\'s Party'),
        ('free silver', 'the demand for unlimited coinage of silver to increase the money supply and raise farm prices'),
        ('Omaha Platform', 'the People\'s Party programme of 1892, including free silver, a graduated income tax and government ownership of railroads'),
        ('crop-lien system', 'the system by which southern farmers pledged their future crop to merchants for credit, trapping them in debt'),
        ('gold standard', 'the system in which the currency is backed by and convertible into gold'),
    ],
    'dates': [('the Grange was founded', 1867), ('the Supreme Court decided Munn v. Illinois, allowing states to regulate grain elevators', 1877), ('the People\'s Party adopted the Omaha Platform', 1892),
              ('Bryan gave his "Cross of Gold" speech', 1896, 7), ('McKinley defeated Bryan in the presidential election', 1896, 11)],
    'mcq': [
        ('Which presidential candidate of the People\'s Party won over a million votes in 1892?', 'James B. Weaver', ['William Jennings Bryan', 'Grover Cleveland', 'Eugene Debs'], 'He won 22 electoral votes. [1]'),
        ('Why did many farmers support free silver?', 'They expected inflation to raise crop prices and ease the burden of debt', ['They wanted lower crop prices', 'They owned silver mines', 'They wanted to return to the gold standard'], '[1]'),
        ('Who won the presidential election of 1896?', 'William McKinley', ['William Jennings Bryan', 'Theodore Roosevelt', 'Grover Cleveland'], '[1]'),
    ],
    'why': [
        ('farmers protested in the late nineteenth century', ['Falling crop prices', 'High railroad rates and grain elevator charges', 'Heavy debts and deflation, which made debts harder to repay',
                                                                'High tariffs raised the cost of manufactured goods', 'A sense that eastern bankers and corporations controlled politics'],
         'falling prices in a deflationary economy were the root cause, and farmers blamed railroads and banks'),
        ('the People\'s Party declined after 1896', ['Fusion with the Democrats behind Bryan cost it its separate identity', 'McKinley\'s victory defeated free silver', 'Farm prices rose after 1897 and new gold discoveries increased the money supply',
                                                     'Racial divisions weakened alliances between Black and white farmers in the South'],
         'fusion in 1896 was decisive, and returning prosperity removed the grievances that had fed the movement'),
    ],
    'claims': [
        ('The Omaha Platform called for a graduated income tax.', True, 'It also called for direct election of senators.'),
        ('Bryan won the 1896 election.', False, 'McKinley won; Bryan lost again in 1900 and 1908.'),
        ('Farmers wanted deflation to continue.', False, 'Deflation increased the real burden of their debts; they wanted inflation.'),
    ],
    'ess': [
        dict(q='‘The Populist movement was a failure.’',
             pro=['The People\'s Party never won the presidency and collapsed after 1896', 'Free silver was defeated', 'Racial divisions undermined southern Populism'],
             con=['Many Populist ideas were later adopted, such as the income tax and direct election of senators', 'It forced economic grievances on to the national agenda', 'It influenced the Democratic Party and the Progressive movement'],
             judge='Populism failed as a party, but many of its demands were achieved by the Progressives, so its influence outlasted its defeat'),
        dict(q='How far were railroads to blame for the problems of farmers in the late nineteenth century?',
             pro=['High freight rates and discrimination against small shippers', 'Control of grain elevators', 'Railroad influence over state politics'],
             con=['Falling world crop prices due to overproduction', 'Deflation and tight money', 'Tariffs and debt'],
             judge='railroads were the most visible target, but the deeper cause was falling prices in a deflationary world market'),
    ],
    'src': [
        S('William Jennings Bryan, speech to the Democratic National Convention, July 1896 (abridged)', 'You shall not press down upon the brow of labor this crown of thorns, you shall not crucify mankind upon a cross of gold.',
          'the free silver campaign', 'Bryan argues that the gold standard was oppressing working people and farmers.',
          'To win the nomination and support for free silver.', 'it is one of the most famous speeches of the period', 'it is political rhetoric intended to rouse a convention',
          'It does not explain the economics of silver.', stance=None),
        S('a farmer\'s letter to a Kansas newspaper, 1891 (illustrative)', 'Corn at ten cents a bushel, and the railroad takes half in freight. The banker holds my mortgage. We have voted for the old parties for twenty years and got nothing.',
          'farmers\' grievances', 'It shows farmers blamed low prices, railroad rates and debt, and had lost faith in the main parties.',
          'To express anger and encourage support for the new party.', 'it shows grievances at the time', 'one farmer may not be typical',
          'It does not show whether the Populists succeeded.', stance=None),
        S('a historian writing in 1990 (illustrative)', 'The People\'s Party lost its elections, but within twenty years the income tax, the direct election of senators and railroad regulation were law.',
          'the legacy of Populism', 'The historian argues that Populist ideas succeeded later even though the party failed.',
          'To reassess the significance of Populism.', 'it is a considered judgement with hindsight', 'other factors also explain the later reforms',
          'It does not discuss the collapse of the party.', stance=False, why='it argues that Populism achieved many of its aims later', kind='secondary'),
    ],
})

g6d = T('The Progressive movement and reform under Roosevelt, Taft and Wilson', 'progressive movement', 'roosevelt, taft and wilson')
build_as(g6d, {
    'enq': 'Progressive reform', 'claim': 'Theodore Roosevelt was the most successful Progressive president',
    'stim': ['In 1906 Upton Sinclair\'s novel The Jungle exposed conditions in the Chicago meat-packing industry.', 'In 1912 the Progressive (Bull Moose) Party nominated Theodore Roosevelt.',
             'The Sixteenth Amendment, allowing a federal income tax, was ratified in 1913.'],
    'terms': [
        ('muckrakers', 'journalists such as Ida Tarbell and Lincoln Steffens who exposed corruption and social problems'),
        ('Square Deal', 'Theodore Roosevelt\'s programme of fairness for business, labour and consumers'),
        ('trust-busting', 'using antitrust law to break up monopolies'),
        ('New Freedom', 'Woodrow Wilson\'s programme of 1912 to restore competition by attacking the tariff, banks and trusts'),
        ('New Nationalism', 'Roosevelt\'s programme of 1912 for strong federal regulation of big business and social reform'),
        ('Federal Reserve System', 'the central banking system created in 1913 to regulate the money supply'),
    ],
    'dates': [('the Supreme Court upheld the break-up of the Northern Securities Company', 1904), ('the Meat Inspection Act and Pure Food and Drug Act were passed', 1906), ('Taft signed the Payne-Aldrich Tariff', 1909),
              ('Wilson won the presidential election', 1912, 11), ('the Federal Reserve Act was passed', 1913, 12), ('the Clayton Antitrust Act was passed', 1914), ('the Nineteenth Amendment gave women the vote', 1920)],
    'mcq': [
        ('Which journalist exposed the methods of Standard Oil in 1904?', 'Ida Tarbell', ['Upton Sinclair', 'Jacob Riis', 'Jane Addams'], '[1]'),
        ('How did Roosevelt intervene in the anthracite coal strike of 1902?', 'He threatened to take over the mines and secured arbitration', ['He sent troops to break the strike', 'He refused to act', 'He nationalised the coal industry permanently'], '[1]'),
        ('Which amendment of 1913 provided for the direct election of senators?', 'The Seventeenth', ['The Sixteenth', 'The Eighteenth', 'The Nineteenth'], '[1]'),
        ('Which president brought more antitrust suits, about 90?', 'Taft', ['Theodore Roosevelt', 'Wilson', 'McKinley'], 'Roosevelt brought about 44. [1]'),
    ],
    'why': [
        ('the Progressive movement developed after 1900', ['Muckrakers exposed corruption and social problems', 'The middle class feared both big business and radical labour', 'Rapid urbanisation created problems that cities could not solve',
                                                           'Populist demands had prepared the ground', 'Religious and moral concerns, such as the Social Gospel'],
         'the growth of a reform-minded urban middle class, alarmed by the effects of industrialisation, was the driving force'),
        ('Roosevelt and Taft fell out by 1912', ['Taft signed the Payne-Aldrich Tariff, which Progressives saw as a betrayal', 'Taft sacked Gifford Pinchot in the Ballinger-Pinchot affair over conservation', 'Taft\'s antitrust suit against US Steel attacked a merger Roosevelt had approved', 'Roosevelt had moved further left with the New Nationalism'],
         'policy differences mattered, but the split was also about Roosevelt\'s ambition to return to power'),
    ],
    'claims': [
        ('The Pure Food and Drug Act was passed under Theodore Roosevelt.', True, 'It was passed in 1906, the year The Jungle was published.'),
        ('Wilson created the Federal Reserve System.', True, 'The Federal Reserve Act was passed in 1913.'),
        ('Progressives were mainly concerned with abolishing private property.', False, 'They wanted to regulate capitalism and reform government, not abolish it.'),
    ],
    'ess': [
        dict(q='‘Theodore Roosevelt was the most successful Progressive president.’',
             pro=['He revived the Sherman Act against Northern Securities', 'He passed the Meat Inspection, Pure Food and Drug and Hepburn Acts', 'He protected millions of acres through conservation and made the presidency a force for reform'],
             con=['Taft brought more antitrust suits and supported the income tax amendment', 'Wilson passed the Federal Reserve, Clayton Act, FTC and Underwood Tariff', 'Roosevelt often compromised with big business'],
             judge='Roosevelt made Progressivism a national movement, but Wilson\'s legislation achieved more lasting structural reform'),
        dict(q='To what extent did the Progressive movement achieve its aims by 1920?',
             pro=['Amendments for income tax, direct election of senators, prohibition and women\'s suffrage', 'Regulation of food, drugs, railroads and trusts', 'Many state reforms such as the initiative and referendum'],
             con=['Big business remained powerful', 'African Americans were largely ignored and segregation grew, even in federal offices under Wilson', 'Many reforms were weakly enforced'],
             judge='Progressives achieved major political and regulatory reforms, but they did not transform the power of big business or address racial injustice'),
    ],
    'src': [
        S('Upton Sinclair, The Jungle, 1906 (summary)', 'The novel described workers falling into vats and diseased meat being sold to the public in the Chicago stockyards.',
          'conditions in the meat-packing industry', 'It exposed unsafe and unhygienic conditions in meat-packing.',
          'To expose the exploitation of workers and win support for socialism.', 'Sinclair investigated the stockyards himself', 'it is a novel, written to persuade, and he exaggerated for effect',
          'It does not show the federal response.', stance=True, why='its publication led Roosevelt to support the Meat Inspection Act'),
        S('a speech by a supporter of Wilson, 1914 (illustrative)', 'In two years this administration has lowered the tariff, given the nation a sound banking system and put real teeth into the laws against monopoly. No president has done more.',
          'Wilson\'s reforms', 'It suggests Wilson\'s reforms were greater than those of earlier presidents.',
          'To win support for the Democrats in the 1914 elections.', 'it lists real measures passed under Wilson', 'it is a partisan election speech',
          'It does not mention Wilson\'s support for segregation in federal offices.', stance=False, why='it claims Wilson achieved more than Roosevelt'),
    ],
})

CHAPTERS[6] = [g6a, g6b, g6c, g6d]


# ============================================================== CHAPTER 7: International option, empire and the emergence of world powers, 1870-1919

e7a = T('Motives for the new imperialism', 'motives for the new imperialism', 'new imperialism')
build_as(e7a, {
    'enq': 'the motives for imperial expansion', 'claim': 'economic motives were the main reason for the new imperialism',
    'stim': ['Between 1870 and 1914 European powers took control of most of Africa and much of South-East Asia and the Pacific.', 'In 1902 the British economist J. A. Hobson published Imperialism: A Study.',
             'In 1875 Disraeli\'s government bought a large share in the Suez Canal Company.'],
    'terms': [
        ('new imperialism', 'the rapid expansion of European, American and Japanese colonial empires between about 1870 and 1914'),
        ('Social Darwinism', 'the misapplication of ideas of natural selection to claim that some races and nations were fitter to rule than others'),
        ('civilising mission', 'the claim that colonial rule brought Christianity, education and "civilisation" to colonised peoples'),
        ('informal empire', 'influence over a territory through trade, investment or treaties without formal annexation'),
        ('surplus capital', 'Hobson\'s idea that capitalists invested abroad because they could not find profitable outlets at home'),
        ('protectorate', 'a territory controlled by a foreign power while keeping its own ruler'),
    ],
    'dates': [('the Suez Canal opened', 1869), ('Britain occupied Egypt', 1882), ('Hobson published Imperialism: A Study', 1902), ('Lenin wrote Imperialism, the Highest Stage of Capitalism', 1916),
              ('Kipling published "The White Man\'s Burden"', 1899)],
    'mcq': [
        ('Who argued that imperialism was the highest stage of capitalism?', 'Lenin', ['Hobson', 'Kipling', 'Bismarck'], 'Written in 1916. [1]'),
        ('Why was the Suez Canal strategically important to Britain?', 'It shortened the route to India', ['It gave access to the Black Sea', 'It linked the Atlantic and Pacific', 'It was the main route for American cotton'], '[1]'),
        ('Which of these is an example of a strategic motive for imperialism?', 'Taking territory to protect the route to India', ['Selling cotton goods in Africa', 'Spreading Christianity', 'Finding land for settlers'], '[1]'),
    ],
    'why': [
        ('European powers expanded their empires after 1870', ['The search for raw materials and markets after the depression of the 1870s', 'Strategic rivalry and the need for coaling stations and routes', 'National prestige, especially after German and Italian unification',
                                                                'Ideas of racial superiority and a civilising mission', 'Technology such as steamships, quinine and machine guns made conquest easier'],
         'economic and strategic motives combined with national rivalry, while new technology made expansion possible'),
        ('Britain occupied Egypt in 1882', ['To protect the Suez Canal and the route to India', 'To protect European bondholders after Egypt\'s bankruptcy', 'The Urabi revolt threatened European control', 'Fear that France might act first'],
         'protection of the canal and route to India was the main reason, but financial interests made intervention more likely'),
    ],
    'claims': [
        ('Hobson argued that imperialism benefited the whole British nation.', False, 'He argued it benefited a small group of investors and financiers at the nation\'s expense.'),
        ('Quinine helped Europeans survive malaria in tropical Africa.', True, 'It reduced deaths among Europeans and made inland expansion possible.'),
        ('Most British overseas investment before 1914 went to tropical African colonies.', False, 'Most went to the USA, Latin America and the settler dominions.'),
    ],
    'ess': [
        dict(q='‘Economic motives were the main reason for the new imperialism.’',
             pro=['Industrial powers wanted raw materials such as rubber and palm oil', 'Businesses sought new markets and investment opportunities', 'Hobson and Lenin argued finance capital drove expansion'],
             con=['Most investment went to non-colonial areas', 'Strategic rivalry, such as protecting routes to India, drove many annexations', 'Nationalism and prestige mattered, especially for Germany and Italy', 'Men on the spot and missionaries often acted without government approval'],
             judge='economic interests were important, but much expansion was strategic and political, driven by rivalry between the powers'),
        dict(q='To what extent was the new imperialism driven by ideas rather than by interests?',
             pro=['Social Darwinism and racial theories justified expansion', 'The civilising mission and missionary activity', 'Popular nationalism and the press created support'],
             con=['Strategic interests drove annexations such as Egypt', 'Economic interests such as rubber and minerals', 'Rivalry between governments'],
             judge='ideas provided justification and popular support, but the decisions to annex were mainly driven by strategic and economic interests'),
    ],
    'src': [
        S('J. A. Hobson, Imperialism: A Study, 1902 (summary)', 'Hobson argued that imperialism was driven by a small group of financiers seeking profitable outlets for surplus capital, while the nation as a whole paid the costs.',
          'the causes of imperialism', 'It argues imperialism served the economic interests of financiers.',
          'To criticise imperialism, especially after the Boer War.', 'Hobson was a respected economist writing at the time', 'he was a critic of imperialism and the Boer War, and selected evidence to support his case',
          'It does not explain strategic motives.', stance=True, why='it argues economic interests drove imperialism', kind='secondary'),
        S('a speech by a French politician to the Chamber of Deputies, 1885 (illustrative)', 'A great nation cannot stand aside while others divide the world. Our fleets need ports and coaling stations, and our flag must be seen beside those of our rivals.',
          'French motives for expansion', 'It suggests strategic needs and national prestige drove French imperialism.',
          'To win support in parliament for colonial expansion.', 'it shows arguments used at the time', 'it is a political speech intended to persuade',
          'It does not mention economic profit.', stance=False, why='it stresses prestige and strategy'),
    ],
})

e7b = T('The Scramble for Africa and imperial rivalry', 'scramble for africa', 'imperial rivalry')
build_as(e7b, {
    'enq': 'the Scramble for Africa', 'claim': 'the Berlin Conference was the main cause of the Scramble for Africa',
    'stim': ['In 1870 about 10 per cent of Africa was under European control; by 1914 about 90 per cent was.', 'The Berlin West Africa Conference met from November 1884 to February 1885.',
             'In 1898 British and French forces faced each other at Fashoda on the upper Nile.'],
    'terms': [
        ('Berlin Conference', 'the conference of 1884-85 that set rules for European claims to African territory'),
        ('effective occupation', 'the principle that a power must actually control a territory to claim it'),
        ('Congo Free State', 'the territory ruled personally by Leopold II of Belgium from 1885 until 1908'),
        ('Fashoda crisis', 'the confrontation of 1898 between Britain and France on the upper Nile, which ended with French withdrawal'),
        ('Battle of Adwa', 'the Ethiopian victory over Italy in 1896 that preserved Ethiopian independence'),
        ('chartered company', 'a company given a government charter to rule and trade in a territory, such as the British South Africa Company'),
    ],
    'dates': [('the Berlin Conference opened', 1884, 11), ('Ethiopia defeated Italy at Adwa', 1896), ('the Fashoda crisis took place', 1898),
              ('the South African War (Boer War) began', 1899), ('the First Moroccan Crisis began with the Kaiser\'s visit to Tangier', 1905), ('the Agadir crisis took place', 1911)],
    'mcq': [
        ('Which two African states remained independent in 1914?', 'Ethiopia and Liberia', ['Egypt and Morocco', 'Sudan and Ghana', 'Congo and Kenya'], '[1]'),
        ('Who called the Berlin Conference of 1884-85?', 'Bismarck', ['Leopold II', 'Gladstone', 'Napoleon III'], '[1]'),
        ('What was the outcome of the Fashoda crisis?', 'France withdrew, and Britain kept control of the Nile valley', ['Britain and France went to war', 'France gained Sudan', 'Germany took control of Egypt'], '[1]'),
        ('Which ruler controlled the Congo Free State as his personal possession?', 'Leopold II of Belgium', ['Wilhelm II of Germany', 'Victor Emmanuel III', 'Menelik II'], 'Belgium took it over in 1908 after international outrage. [1]'),
    ],
    'why': [
        ('the Scramble for Africa happened so quickly after 1880', ['Rivalry between European powers made each fear being left out', 'Leopold II\'s and France\'s claims in the Congo triggered a race', 'Britain\'s occupation of Egypt in 1882 alarmed France',
                                                                     'The Berlin Conference set rules that encouraged rapid claims', 'Technology such as quinine, steamships and the Maxim gun made conquest possible'],
         'rivalry between the powers turned slow expansion into a race, once technology made conquest cheap'),
        ('the Moroccan crises increased tension between the great powers', ['Germany tried to test and break the Anglo-French Entente', 'Instead Britain supported France, strengthening the Entente', 'Germany was diplomatically isolated at Algeciras in 1906', 'The crises fed naval and military rivalry'],
         'Germany\'s attempts to divide Britain and France backfired, drawing the Entente powers closer together'),
    ],
    'claims': [
        ('The Berlin Conference divided Africa into colonies on a map.', False, 'It set rules for claims, such as effective occupation, but did not partition the continent.'),
        ('Ethiopia defeated an Italian army at Adwa in 1896.', True, 'This preserved Ethiopian independence.'),
        ('The Fashoda crisis led to war between Britain and France.', False, 'France withdrew, and the two powers later signed the Entente Cordiale in 1904.'),
    ],
    'ess': [
        dict(q='‘The Berlin Conference was the main cause of the Scramble for Africa.’',
             pro=['It set the rule of effective occupation, which encouraged rapid conquest', 'It legitimised claims such as Leopold\'s Congo', 'The pace of annexation increased after 1885'],
             con=['The Scramble had already begun with the occupation of Egypt and the Congo rivalry', 'Economic, strategic and nationalist motives drove expansion', 'Men on the spot such as Rhodes acted independently', 'Technological advantages made conquest possible'],
             judge='the Conference shaped how the Scramble happened, but it was a response to a race that rivalry and opportunity had already begun'),
        dict(q='How far did imperial rivalry in Africa increase tension between the great powers before 1914?',
             pro=['Fashoda brought Britain and France close to war', 'The Moroccan crises increased Anglo-German hostility', 'German resentment at its small empire fed Weltpolitik'],
             con=['Most African disputes were settled peacefully by negotiation', 'Fashoda was followed by the Entente Cordiale', 'Tension in Europe arose more from the Balkans and naval rivalry'],
             judge='African rivalries caused crises, but they were usually settled; their main effect was to shape alliances rather than cause war'),
    ],
    'src': [
        S('the General Act of the Berlin Conference, 1885 (summary)', 'The Act required any power taking possession of territory on the African coast to notify the other signatories and to establish authority sufficient to protect existing rights.',
          'the rules of the Scramble', 'It shows the powers agreed rules for making claims to African territory.',
          'To prevent conflict between European powers over Africa.', 'it is the official agreement', 'it shows intentions of the European powers only; no Africans were represented',
          'It does not show how the rules were applied.', stance=True, why='it set the rules that encouraged rapid occupation'),
        S('a letter from a British colonial official in West Africa, 1883 (illustrative)', 'The French are pushing up every river. If we do not take this coast now, we shall find their flag here next year and our traders shut out.',
          'the motives of officials before the Berlin Conference', 'It suggests rivalry with France was already driving British expansion before 1884.',
          'To persuade London to annex territory.', 'it shows the views of men on the spot', 'officials often exaggerated threats to win support',
          'It does not show the views of the British government.', stance=False, why='it shows rivalry driving expansion before the Conference'),
    ],
})

e7c = T('The emergence of the USA as a world power: the Spanish-American War and after', 'usa as a world power', 'spanish-american war')
build_as(e7c, {
    'enq': 'the emergence of the USA as a world power', 'claim': 'the Spanish-American War marked a turning point in US foreign policy',
    'stim': ['In February 1898 the USS Maine exploded in Havana harbour.', 'By the Treaty of Paris (1898) Spain ceded the Philippines, Puerto Rico and Guam to the United States.',
             'The Panama Canal opened in 1914.'],
    'terms': [
        ('yellow journalism', 'sensational newspaper reporting, as in Hearst\'s and Pulitzer\'s papers, which stirred support for war in 1898'),
        ('Open Door policy', 'the US demand of 1899-1900 that all powers have equal trading rights in China'),
        ('Roosevelt Corollary', 'Theodore Roosevelt\'s claim in 1904 that the USA could intervene in Latin American countries to keep order'),
        ('Platt Amendment', 'the condition of 1901 that allowed the USA to intervene in Cuba and to lease Guantánamo Bay'),
        ('big stick diplomacy', 'Roosevelt\'s policy of backing diplomacy with the threat of military force'),
        ('dollar diplomacy', 'Taft\'s policy of using investment and loans to extend US influence abroad'),
    ],
    'dates': [('Mahan published The Influence of Sea Power upon History', 1890), ('the USS Maine exploded in Havana harbour', 1898, 2), ('Dewey destroyed the Spanish fleet at Manila Bay', 1898, 5),
              ('the USA annexed Hawaii', 1898, 7), ('the Roosevelt Corollary was announced', 1904), ('the USA entered the First World War', 1917, 4)],
    'mcq': [
        ('Whose writings argued that sea power was the key to national greatness?', 'Alfred Thayer Mahan', ['Frederick Jackson Turner', 'William Randolph Hearst', 'John Hay'], '[1]'),
        ('Which territory did the USA fight a long war to control after 1899?', 'The Philippines', ['Cuba', 'Puerto Rico', 'Hawaii'], 'The Philippine-American War, 1899-1902. [1]'),
        ('Who announced the Open Door policy?', 'Secretary of State John Hay', ['Theodore Roosevelt', 'William McKinley', 'Woodrow Wilson'], '[1]'),
    ],
    'why': [
        ('the USA went to war with Spain in 1898', ['Sympathy for Cuban rebels against Spanish rule', 'The explosion of the Maine, blamed on Spain', 'Yellow journalism stirred public opinion', 'American economic interests in Cuba', 'Strategic and expansionist ideas such as those of Mahan'],
         'public opinion inflamed by the Maine and the press forced McKinley\'s hand, but strategic and economic interests made war attractive to expansionists'),
        ('the USA built the Panama Canal', ['To move the navy quickly between the Atlantic and Pacific', 'To boost trade between the coasts and with Asia', 'The Spanish-American War had shown the need for it', 'Roosevelt supported Panamanian independence from Colombia in 1903 to gain the canal zone'],
         'strategic naval needs were the main reason, reinforced by commercial benefit'),
    ],
    'claims': [
        ('The USA annexed Cuba after the Spanish-American War.', False, 'Cuba became nominally independent, but the Platt Amendment gave the USA the right to intervene.'),
        ('The Spanish-American War lasted only a few months.', True, 'It began in April 1898 and fighting ended in August.'),
        ('The US Senate approved the Treaty of Versailles in 1919.', False, 'The Senate rejected it in November 1919 and March 1920.'),
    ],
    'ess': [
        dict(q='‘The Spanish-American War marked a turning point in US foreign policy.’',
             pro=['The USA acquired an overseas empire for the first time', 'It became a Pacific power with the Philippines and Hawaii', 'It led to more active policies such as the Open Door, the Roosevelt Corollary and the Panama Canal'],
             con=['The USA had already expanded across the continent and bought Alaska in 1867', 'The Monroe Doctrine had long claimed influence in Latin America', 'The USA remained reluctant to join alliances and rejected the League in 1919-20'],
             judge='it was a turning point in that the USA became an overseas imperial power, but there was continuity in expansionism and in avoiding European alliances'),
        dict(q='How far had the USA become a world power by 1919?',
             pro=['Largest industrial economy', 'Overseas empire and the Panama Canal', 'Its intervention helped decide the First World War, and Wilson shaped the peace'],
             con=['Its army was small before 1917', 'The Senate rejected the League of Nations', 'Its influence outside the Americas and Pacific was limited'],
             judge='by 1919 the USA had the economic power and had shown the military potential of a world power, but it was unwilling to accept the commitments of one'),
    ],
    'src': [
        S('Senator Albert Beveridge, speech to the US Senate, January 1900 (abridged)', 'The Philippines are ours forever. And just beyond the Philippines are China\'s illimitable markets. We will not retreat from either.',
          'motives for annexing the Philippines', 'It shows that access to Asian markets was a motive for American expansion.',
          'To win support for keeping the Philippines.', 'it shows the arguments of expansionists at the time', 'it is a political speech by an enthusiast',
          'It does not show the views of anti-imperialists.', stance=True, why='it shows a new, imperial direction in US policy'),
        S('a statement by an anti-imperialist group, 1899 (summary)', 'Anti-imperialists argued that ruling the Philippines without the consent of its people betrayed the principles of the Declaration of Independence.',
          'opposition to US imperialism', 'It shows strong opposition within the USA to overseas empire.',
          'To campaign against annexation.', 'it shows that many Americans opposed empire', 'it is a campaigning statement',
          'It does not show government policy.', stance=False, why='it shows that many Americans rejected the new imperial direction'),
    ],
})

e7d = T('The rise of Japan as a world power: the Meiji period and the Russo-Japanese War', 'rise of japan', 'meiji', 'russo-japanese war')
build_as(e7d, {
    'enq': 'the rise of Japan', 'claim': 'Japan\'s rise as a world power was due mainly to Meiji modernisation',
    'stim': ['In 1853 Commodore Perry\'s US warships arrived in Edo Bay demanding that Japan open to trade.', 'The Meiji Restoration of 1868 returned power to the emperor.',
             'In May 1905 the Japanese navy destroyed the Russian Baltic Fleet at Tsushima.'],
    'terms': [
        ('Meiji Restoration', 'the political revolution of 1868 that ended the Tokugawa shogunate and restored imperial rule'),
        ('unequal treaties', 'the treaties imposed on Japan from 1854 that gave Western powers trading privileges and extraterritoriality'),
        ('Charter Oath', 'the emperor\'s statement of 1868 promising, among other things, to seek knowledge throughout the world'),
        ('Iwakura Mission', 'the Japanese diplomatic and study mission to the USA and Europe in 1871-73'),
        ('zaibatsu', 'large family-controlled industrial and financial combines such as Mitsui and Mitsubishi'),
        ('Treaty of Portsmouth', 'the treaty of 1905 that ended the Russo-Japanese War'),
    ],
    'dates': [('Perry\'s squadron arrived in Japan', 1853), ('the Meiji Restoration took place', 1868), ('Japan introduced conscription', 1873),
              ('the Meiji Constitution was introduced', 1889), ('the Treaty of Shimonoseki ended the war with China', 1895), ('the Anglo-Japanese Alliance was signed', 1902), ('Japan annexed Korea', 1910)],
    'mcq': [
        ('Which territory did Japan gain from China by the Treaty of Shimonoseki (1895)?', 'Taiwan (Formosa)', ['Korea', 'Manchuria', 'Sakhalin'], 'It was forced to give back the Liaodong Peninsula by the Triple Intervention. [1]'),
        ('Why was the Anglo-Japanese Alliance of 1902 important to Japan?', 'It meant no other power was likely to join Russia against Japan', ['It gave Japan control of India', 'It ended the unequal treaties at once', 'It made Britain pay for the Japanese navy'], '[1]'),
        ('Which country mediated the Treaty of Portsmouth in 1905?', 'The United States', ['Britain', 'France', 'Germany'], 'President Theodore Roosevelt. [1]'),
    ],
    'why': [
        ('Japan was able to modernise rapidly after 1868', ['The Meiji leaders were determined to avoid colonisation by the West', 'They borrowed Western technology, institutions and experts', 'Feudal domains were abolished and a centralised state created',
                                                            'Universal education and conscription built a national army', 'Government investment created industries later sold to the zaibatsu'],
         'a determined leadership, driven by fear of Western domination, used the power of a centralised state to borrow selectively from the West'),
        ('Japan defeated Russia in 1904-05', ['Japan had a modern navy and well-trained army', 'Russia\'s forces were far from home, linked only by the unfinished Trans-Siberian Railway', 'The Anglo-Japanese Alliance prevented other powers helping Russia',
                                                'Russia was weakened by revolution in 1905', 'Japanese victories at Port Arthur, Mukden and Tsushima'],
         'Japanese preparation and naval power were decisive, helped by Russia\'s distance and internal crisis'),
    ],
    'claims': [
        ('Japan was the first Asian power in modern times to defeat a European great power in a major war.', True, 'Its victory over Russia in 1905 shocked the world.'),
        ('The Meiji Constitution of 1889 made the elected Diet the supreme power in Japan.', False, 'Sovereignty lay with the emperor; the Diet had limited powers.'),
        ('Japan gained all its war aims at the Treaty of Portsmouth.', False, 'It gained Port Arthur, southern Sakhalin and recognition in Korea, but no indemnity, which caused riots in Tokyo.'),
    ],
    'ess': [
        dict(q='‘Japan\'s rise as a world power by 1914 was due mainly to Meiji modernisation.’',
             pro=['Industrialisation and a modern army and navy', 'Centralised government and conscription', 'Education and national unity under the emperor'],
             con=['The Anglo-Japanese Alliance gave diplomatic security', 'Weakness of China and Russia', 'Rivalry between Western powers allowed Japan to expand'],
             judge='modernisation gave Japan the means, but international circumstances, especially the alliance with Britain and the weakness of its neighbours, made its rise possible'),
        dict(q='To what extent did the Russo-Japanese War make Japan a world power?',
             pro=['Japan defeated a European great power', 'It gained control of Korea and South Manchurian interests', 'It won international recognition and ended remaining unequal treaties by 1911'],
             con=['The war nearly bankrupted Japan and it gained no indemnity', 'Japan had already defeated China in 1895', 'Western powers still did not treat Japan as an equal, as shown in 1919 over the racial equality clause'],
             judge='the war confirmed Japan as a great power in East Asia, but it was not yet accepted as an equal by the West'),
    ],
    'src': [
        S('the Charter Oath, 1868 (translated, abridged)', 'Evil customs of the past shall be broken off and everything based upon the just laws of nature. Knowledge shall be sought throughout the world so as to strengthen the foundations of imperial rule.',
          'the aims of the Meiji government', 'It shows the new government intended to learn from the world to strengthen Japan.',
          'To set out the principles of the new government.', 'it is the official statement of the new regime', 'it is a statement of intent, not evidence of what was achieved',
          'It does not show the role of the military or foreign alliances.', stance=True, why='it shows modernisation was a deliberate policy'),
        S('a British newspaper, 1902 (illustrative)', 'The alliance with Japan secures our position in the Far East. Should Russia fight Japan, she will fight alone.',
          'the Anglo-Japanese Alliance', 'It suggests the alliance gave Japan security against a coalition.',
          'To explain the alliance to British readers.', 'it shows British thinking at the time', 'it reflects British interests, not Japanese',
          'It does not show Japan\'s military strength.', stance=False, why='it stresses diplomacy rather than modernisation'),
    ],
})

CHAPTERS[7] = [e7a, e7b, e7c, e7d]


# ============================================================== CHAPTER 8: International option, the League of Nations and international relations in the 1920s

l8a = T('The peace settlement of 1919-20: aims and reactions', 'peace settlement of 1919-20', 'aims and reactions')
build_as(l8a, {
    'enq': 'the peace settlement of 1919-20', 'claim': 'the Treaty of Versailles was too harsh on Germany',
    'stim': ['The Treaty of Versailles was signed on 28 June 1919.', 'In 1921 the Reparations Commission set Germany\'s reparations at 132 billion gold marks (£6,600 million).',
             'In 1919 J. M. Keynes published The Economic Consequences of the Peace.'],
    'terms': [
        ('war guilt clause', 'Article 231 of the Treaty of Versailles, which made Germany accept responsibility for the loss and damage caused by the war'),
        ('reparations', 'payments for war damage demanded from the defeated powers'),
        ('self-determination', 'the principle that peoples should choose their own government, central to Wilson\'s Fourteen Points'),
        ('diktat', 'the German name for the treaty, meaning a dictated peace that Germany had no part in negotiating'),
        ('mandate', 'a former German or Ottoman territory governed by a victorious power on behalf of the League'),
        ('Fourteen Points', 'Wilson\'s programme for peace announced in January 1918'),
    ],
    'dates': [('Wilson announced the Fourteen Points', 1918, 1), ('the Treaty of Versailles was signed', 1919, 6), ('the Treaty of Saint-Germain with Austria was signed', 1919, 9),
              ('the Treaty of Trianon with Hungary was signed', 1920, 6), ('the Treaty of Sèvres with Turkey was signed', 1920, 8), ('the Treaty of Lausanne replaced Sèvres', 1923, 7)],
    'mcq': [
        ('What size was the German army limited to by the Treaty of Versailles?', '100,000 men', ['250,000 men', '50,000 men', '500,000 men'], 'Conscription was also banned. [1]'),
        ('Which treaty dealt with Hungary?', 'Trianon', ['Neuilly', 'Saint-Germain', 'Sèvres'], 'Hungary lost about two-thirds of its territory. [1]'),
        ('What was Clemenceau\'s main aim at the peace conference?', 'Security for France against future German attack', ['A lenient peace to revive trade', 'Self-determination for all peoples', 'The return of the Kaiser'], '[1]'),
        ('Why was the Treaty of Sèvres replaced by the Treaty of Lausanne?', 'Turkish nationalists under Mustafa Kemal refused to accept it and defeated Greece', ['Britain declared war on Italy', 'The USA joined the League', 'Germany demanded it'], '[1]'),
    ],
    'why': [
        ('the peacemakers found it difficult to agree in 1919', ['Clemenceau wanted security and a harsh peace', 'Wilson wanted a just peace based on the Fourteen Points', 'Lloyd George wanted Germany punished but able to trade and recover',
                                                                 'Secret wartime treaties conflicted with self-determination', 'Public opinion in Britain and France demanded harsh terms'],
         'the peacemakers had conflicting aims shaped by different national interests, so the treaty was a compromise'),
        ('Germans resented the Treaty of Versailles', ['Germany was not allowed to negotiate', 'The war guilt clause was seen as a humiliation', 'Reparations were seen as unfair and ruinous', 'Territorial losses placed Germans under foreign rule', 'Many Germans did not believe their army had been defeated'],
         'resentment centred on the dictated nature and war guilt clause, which seemed to deny Germany the self-determination offered to others'),
    ],
    'claims': [
        ('The USA ratified the Treaty of Versailles in 1919.', False, 'The Senate rejected it.'),
        ('Germany lost all its overseas colonies under the treaty.', True, 'They became mandates under the League.'),
        ('The reparations figure was fixed in the Treaty of Versailles itself.', False, 'It was set in 1921 by the Reparations Commission.'),
    ],
    'ess': [
        dict(q='‘The Treaty of Versailles was too harsh on Germany.’',
             pro=['Germany lost about 13 per cent of its European territory and all colonies', 'Reparations and the war guilt clause caused deep resentment', 'Germany was not allowed to negotiate'],
             con=['Germany remained united and potentially the strongest power in Europe', 'Germany had imposed harsher terms on Russia at Brest-Litovsk', 'Reparations were within Germany\'s capacity, and much was never paid'],
             judge='the treaty was harsh enough to cause lasting resentment but not harsh enough to prevent German recovery, which was its main weakness'),
        dict(q='How far did the peace settlement of 1919-20 achieve the aims of the peacemakers?',
             pro=['France gained Alsace-Lorraine and a demilitarised Rhineland', 'The League of Nations was created', 'Britain gained colonies and the German fleet was removed'],
             con=['Clemenceau did not get the Rhine frontier or an Anglo-American guarantee', 'Wilson\'s League was rejected by the US Senate', 'Self-determination was applied inconsistently'],
             judge='each peacemaker gained some aims, but the settlement satisfied none of them fully and left Germany resentful'),
    ],
    'src': [
        S('a German newspaper, Deutsche Zeitung, 28 June 1919 (translated, abridged)', 'Vengeance! German nation! Today in the Hall of Mirrors the disgraceful treaty is being signed. Do not forget it.',
          'German reactions to the treaty', 'It shows German anger and a desire for revenge.',
          'To express and encourage German outrage.', 'it shows public reaction in Germany on the day of signing', 'it is a nationalist newspaper and expresses an extreme view',
          'It does not explain the terms of the treaty.', stance=True, why='it shows Germans regarded the treaty as unbearably harsh'),
        S('J. M. Keynes, The Economic Consequences of the Peace, 1919 (summary)', 'Keynes argued that reparations were far beyond Germany\'s capacity to pay and would ruin the economy of Europe.',
          'the economic terms', 'Keynes argues reparations were excessive and economically damaging.',
          'To criticise the treaty and influence opinion.', 'Keynes was a Treasury adviser at the conference', 'he had resigned in protest and wanted to change policy',
          'It does not consider French security needs.', stance=True, why='it argues reparations were too harsh', kind='secondary'),
        S('a historian writing in 1990 (illustrative)', 'Germany was defeated but not destroyed. It kept its industry and its unity; the treaty was too severe to conciliate and too lenient to restrain.',
          'the severity of the treaty', 'The historian argues that the treaty was not too harsh in itself but failed to weaken Germany permanently.',
          'To reassess the treaty.', 'it is based on later research', 'it is one interpretation',
          'It does not discuss German public opinion.', stance=False, why='it argues the treaty left Germany strong', kind='secondary'),
    ],
})

l8b = T('Origins, aims and structure of the League of Nations', 'origins, aims and structure', 'league of nations')
build_as(l8b, {
    'enq': 'the League of Nations', 'claim': 'the League of Nations was weakened from the start by the absence of the USA',
    'stim': ['The Covenant of the League of Nations formed the first part of the Treaty of Versailles.', 'The League\'s headquarters were in Geneva.',
             'The League\'s Assembly first met in November 1920.'],
    'terms': [
        ('Covenant', 'the founding document of the League, setting out its aims and rules'),
        ('collective security', 'the idea that members would act together against an aggressor'),
        ('Assembly', 'the League body in which every member state had one vote, meeting once a year'),
        ('Council', 'the smaller League body that met several times a year to deal with crises, with permanent and non-permanent members'),
        ('sanctions', 'measures, usually economic, taken against a state that broke the Covenant'),
        ('Permanent Court of International Justice', 'the League court in The Hague that settled legal disputes between states'),
    ],
    'dates': [('the League of Nations came into existence', 1920, 1), ('the Permanent Court of International Justice was set up', 1922), ('Germany joined the League', 1926, 9), ('the USSR joined the League', 1934, 9)],
    'mcq': [
        ('Which were the permanent members of the League Council when it first met?', 'Britain, France, Italy and Japan', ['Britain, France, the USA and Germany', 'Britain, the USA, the USSR and China', 'France, Germany, Italy and Spain'], 'The USA had been expected to be a fifth. [1]'),
        ('Which article of the Covenant dealt with sanctions against an aggressor?', 'Article 16', ['Article 10', 'Article 231', 'Article 1'], 'Article 10 pledged members to respect each other\'s territory. [1]'),
        ('Which League agency worked to improve working conditions?', 'The International Labour Organization', ['The Mandates Commission', 'The Health Organisation', 'The Conference of Ambassadors'], '[1]'),
        ('Why did decisions in the League Council often take a long time?', 'Decisions had to be unanimous', ['The Council met only once every five years', 'Only the USA could call meetings', 'The Secretariat could veto decisions'], '[1]'),
    ],
    'why': [
        ('the USA did not join the League', ['The Senate rejected the Treaty of Versailles', 'Republicans feared Article 10 would drag the USA into foreign wars', 'Isolationist opinion wanted to avoid European entanglements',
                                             'Wilson refused to accept reservations and his illness weakened his campaign', 'Many Americans of German and Irish descent disliked the treaty'],
         'fear that Article 10 would commit the USA to war, combined with Wilson\'s refusal to compromise, led to rejection'),
        ('the League\'s structure made it difficult to act quickly', ['The Council and Assembly required unanimity', 'The League had no army of its own', 'Sanctions depended on members\' willingness', 'Major powers such as the USA, Germany and the USSR were absent at first'],
         'the requirement for unanimity and the lack of armed force meant action depended on the great powers\' willingness'),
    ],
    'claims': [
        ('The League of Nations had its own army.', False, 'It relied on members to provide forces.'),
        ('Germany was a member of the League from 1920.', False, 'Germany joined in 1926 and left in 1933.'),
        ('The League\'s headquarters were in Geneva.', True, 'Switzerland was neutral.'),
    ],
    'ess': [
        dict(q='‘The League of Nations was weakened from the start by the absence of the USA.’',
             pro=['The USA was the world\'s greatest economic power, so sanctions were less effective', 'Britain and France were left to lead and lacked the resources and will', 'The League looked like a club of the victors'],
             con=['The structure of unanimity and lack of an army were greater weaknesses', 'The absence of Germany and the USSR also weakened it', 'Britain and France put national interests first', 'The League had successes in the 1920s without the USA'],
             judge='the absence of the USA was a serious weakness, but the League\'s structure and the attitudes of Britain and France were more fundamental'),
        dict(q='How far was the League of Nations designed to fail?',
             pro=['Unanimity rule made decisions slow', 'No army to enforce decisions', 'Membership excluded key powers'],
             con=['Its agencies achieved real success in health, refugees and labour', 'It settled several disputes in the 1920s', 'Its failures came mainly from the actions of the great powers in the 1930s'],
             judge='the League had serious design flaws but was not designed to fail; it worked when the great powers supported it'),
    ],
    'src': [
        S('Article 10 of the Covenant of the League of Nations, 1919', 'The Members of the League undertake to respect and preserve as against external aggression the territorial integrity and existing political independence of all Members of the League.',
          'the commitments of League members', 'It shows members promised to defend each other against aggression.',
          'To set out the principle of collective security.', 'it is the official text', 'it shows aims, not whether members would act',
          'It does not explain how members would enforce it.', stance=None),
        S('a speech by a US Republican senator, 1919 (illustrative)', 'Article 10 would bind us to send American boys to fight in every quarrel in Europe and Asia. I will never vote to surrender American independence to a council of foreigners.',
          'US opposition to the League', 'It shows fear that the League would drag the USA into foreign wars.',
          'To persuade the Senate to reject the treaty.', 'it shows the arguments of opponents', 'it is a partisan speech that exaggerates',
          'It does not show the views of Wilson\'s supporters.', stance=True, why='it explains why the USA stayed out'),
    ],
})

l8c = T("The League's work in the 1920s: disputes and humanitarian agencies", "league's work in the 1920s", 'humanitarian agencies')
build_as(l8c, {
    'enq': 'the work of the League in the 1920s', 'claim': 'the League was successful in the 1920s',
    'stim': ['In 1921 the League settled the dispute between Finland and Sweden over the Åland Islands.', 'In 1923 Mussolini occupied the Greek island of Corfu.',
             'In 1922 the League introduced the "Nansen passport" for stateless refugees.'],
    'terms': [
        ('Nansen passport', 'the identity document for stateless refugees introduced by the League in 1922'),
        ('Conference of Ambassadors', 'the body of Allied ambassadors set up to enforce the peace treaties, which sometimes overrode the League'),
        ('Health Organisation', 'the League agency that worked against epidemic diseases such as typhus, leprosy and malaria'),
        ('Mandates Commission', 'the League body that supervised the government of mandated territories'),
        ('Slavery Commission', 'the League body that worked to end slavery and forced labour'),
        ('plebiscite', 'a vote by the inhabitants of a disputed area on which state they wish to belong to'),
    ],
    'dates': [('the Åland Islands dispute was settled', 1921), ('the League divided Upper Silesia between Germany and Poland', 1921), ('Italy occupied Corfu', 1923, 8),
              ('the League stopped the Greek invasion of Bulgaria', 1925, 10), ('Poland seized Vilna from Lithuania', 1920, 10)],
    'mcq': [
        ('Why is the Corfu incident of 1923 seen as a failure for the League?', 'The Conference of Ambassadors made Greece pay compensation to Italy', ['Italy left the League', 'Greece annexed Corfu', 'The League declared war on Italy'], 'Mussolini withdrew only after Greece paid. [1]'),
        ('How did the League settle the Greek-Bulgarian dispute of 1925?', 'It ordered Greece to withdraw and pay compensation, and Greece obeyed', ['It sent an army to Bulgaria', 'It gave the disputed land to Greece', 'It expelled Bulgaria'], '[1]'),
        ('Who led the League\'s work in returning prisoners of war and helping refugees?', 'Fridtjof Nansen', ['Aristide Briand', 'Gustav Stresemann', 'Lord Robert Cecil'], '[1]'),
    ],
    'why': [
        ('the League was able to settle some disputes in the 1920s', ['The states involved were small powers', 'The great powers supported the League\'s decisions', 'The threat of sanctions could work against small states', 'The international mood of the mid-1920s favoured cooperation'],
         'the League succeeded when the great powers supported it against small states'),
        ('the League failed to resolve the Corfu and Vilna disputes', ['Italy was a great power and a permanent member of the Council', 'Britain and France put their own interests first', 'The Conference of Ambassadors overrode the League', 'France supported Poland as an ally against Germany'],
         'the League failed when a great power or its allies were involved, because Britain and France would not act against them'),
    ],
    'claims': [
        ('The League\'s Health Organisation helped fight epidemics such as typhus.', True, 'It worked in eastern Europe and with Soviet Russia.'),
        ('Lithuania regained Vilna after the League\'s intervention.', False, 'Poland kept Vilna.'),
        ('The League\'s work for refugees helped hundreds of thousands of people.', True, 'Nansen\'s work helped return about 400,000 prisoners of war and resettle refugees.'),
    ],
    'ess': [
        dict(q='‘The League of Nations was successful in the 1920s.’',
             pro=['It settled disputes such as the Åland Islands and Greece-Bulgaria', 'Its humanitarian agencies helped refugees, fought disease and freed slaves', 'Loans helped Austria and Hungary recover'],
             con=['It failed over Vilna and Corfu when great powers were involved', 'Major agreements such as Locarno were made outside the League', 'Disarmament made little progress'],
             judge='the League was successful in humanitarian work and in disputes between small powers, but it could not restrain great powers even in the 1920s'),
        dict(q='How far did the humanitarian work of the League make up for its failures in settling disputes?',
             pro=['It helped about 400,000 prisoners of war return home', 'The Health Organisation and Refugee Commission saved many lives', 'The ILO and Slavery Commission improved conditions'],
             con=['Its main purpose was to keep the peace', 'Failures such as Corfu showed great powers could defy it', 'Humanitarian success did not prevent later aggression'],
             judge='its humanitarian work was a genuine and lasting achievement, but it could not compensate for weakness in its central task of collective security'),
    ],
    'src': [
        S('a League of Nations report on refugee work, 1920s (illustrative)', 'Through the efforts of the High Commissioner, prisoners of war from twenty-six countries have been returned to their homes, and tens of thousands of refugees have been given identity papers.',
          'the League\'s humanitarian work', 'It shows the League\'s success in helping prisoners of war and refugees.',
          'To publicise the League\'s achievements.', 'it is an official report with figures', 'it was written to present the League positively',
          'It does not mention failures in disputes.', stance=True, why='it shows the League\'s humanitarian success'),
        S('a cartoon in a British magazine, 1923 (description)', 'The cartoon shows a small dove labelled "League of Nations" hiding behind a chair while a burly figure labelled "Italy" stamps on a map of Corfu.',
          'the Corfu incident', 'It suggests the League was too weak to stand up to Mussolini.',
          'To criticise the League\'s weakness.', 'it shows contemporary opinion', 'it is satire and simplifies events',
          'It does not show the League\'s successes.', stance=False, why='it shows the League failing against a great power'),
    ],
})

l8d = T('Locarno, Kellogg-Briand, the Washington Conference and disarmament', 'locarno', 'kellogg-briand', 'washington conference', 'disarmament')
build_as(l8d, {
    'enq': 'international relations in the later 1920s', 'claim': 'the Locarno Treaties brought real security to Europe',
    'stim': ['The Locarno Treaties were initialled in October 1925 and signed in London in December 1925.', 'In 1928 the Kellogg-Briand Pact renounced war as an instrument of national policy.',
             'The Washington Naval Conference of 1921-22 limited battleship tonnage of the leading naval powers.'],
    'terms': [
        ('Locarno spirit', 'the mood of international cooperation and optimism that followed the Locarno Treaties'),
        ('Kellogg-Briand Pact', 'the agreement of 1928 renouncing war as an instrument of national policy, eventually signed by over sixty states'),
        ('Five-Power Treaty', 'the naval agreement of 1922 that fixed a 5:5:3 ratio of capital ships for the USA, Britain and Japan'),
        ('Rhineland Pact', 'the main Locarno treaty, guaranteeing the Franco-German and Belgian-German borders'),
        ('Dawes Plan', 'the plan of 1924 that rescheduled German reparations and provided US loans'),
        ('Young Plan', 'the plan of 1929 that reduced Germany\'s total reparations and extended payments to 1988'),
    ],
    'dates': [('the Washington Naval Conference opened', 1921, 11), ('the Treaty of Rapallo was signed between Germany and Soviet Russia', 1922, 4), ('the Dawes Plan was agreed', 1924),
              ('the Locarno Treaties were signed', 1925, 12), ('the Kellogg-Briand Pact was signed', 1928, 8), ('the World Disarmament Conference opened', 1932, 2)],
    'mcq': [
        ('Which borders did the Locarno Treaties guarantee?', 'Germany\'s western borders with France and Belgium', ['Germany\'s eastern borders with Poland', 'The borders of Austria', 'All borders in Europe'], 'Germany\'s eastern borders were covered only by arbitration treaties. [1]'),
        ('Which two statesmen were awarded the Nobel Peace Prize for 1926 for their work for Franco-German reconciliation at Locarno?', 'Stresemann and Briand', ['Hitler and Mussolini', 'Wilson and Lloyd George', 'Kellogg and Hoover'], '[1]'),
        ('What was the main weakness of the Kellogg-Briand Pact?', 'It had no means of enforcement', ['Only three countries signed it', 'It allowed wars of conquest', 'It required all states to disarm completely'], '[1]'),
    ],
    'why': [
        ('international relations improved in the mid-1920s', ['The Dawes Plan eased the reparations crisis after the Ruhr occupation', 'Stresemann pursued fulfilment and cooperation', 'Briand and Austen Chamberlain wanted reconciliation',
                                                              'Economic recovery and US loans brought prosperity', 'Germany joined the League in 1926'],
         'economic recovery made cooperation possible, and leaders such as Stresemann and Briand took advantage of it'),
        ('disarmament made little progress in the 1920s', ['France feared Germany and would not disarm without security guarantees', 'The Geneva Protocol of 1924 was rejected by Britain', 'Powers disagreed over what counted as armaments', 'The USA and USSR were outside the League'],
         'disarmament failed because France would not reduce its forces without security guarantees that Britain would not give'),
    ],
    'claims': [
        ('The Locarno Treaties guaranteed Germany\'s eastern borders.', False, 'They guaranteed only its western borders.'),
        ('The Washington Conference limited the size of the navies of the USA, Britain and Japan.', True, 'The Five-Power Treaty set ratios for capital ships.'),
        ('The Kellogg-Briand Pact was organised by the League of Nations.', False, 'It was negotiated outside the League by the USA and France.'),
    ],
    'ess': [
        dict(q='‘The Locarno Treaties brought real security to Europe.’',
             pro=['Germany accepted its western borders voluntarily', 'They led to German entry to the League in 1926', 'They created a spirit of cooperation'],
             con=['They left Germany\'s eastern borders open to revision', 'They depended on Stresemann and economic prosperity', 'They were made outside the League, weakening it', 'The spirit of Locarno collapsed with the Depression'],
             judge='Locarno improved relations, but it rested on prosperity and goodwill and left the eastern question unresolved, so security was more apparent than real'),
        dict(q='How far did the international agreements of the 1920s reduce the risk of war?',
             pro=['The Washington Conference prevented a naval race in the Pacific', 'Locarno and Germany\'s entry to the League eased Franco-German tension', 'The Dawes and Young Plans eased reparations disputes'],
             con=['Kellogg-Briand had no means of enforcement', 'Disarmament failed', 'Agreements depended on US loans and collapsed in the Depression'],
             judge='they reduced tension while prosperity lasted, but had no means of enforcement and did not survive the Depression'),
    ],
    'src': [
        S('Article 1 of the Kellogg-Briand Pact, 1928', 'The High Contracting Parties solemnly declare in the names of their respective peoples that they condemn recourse to war for the solution of international controversies, and renounce it as an instrument of national policy.',
          'the Kellogg-Briand Pact', 'It shows states promised not to use war to settle disputes.',
          'To renounce war as a means of policy.', 'it is the official text', 'it contains no enforcement mechanism',
          'It does not say what would happen if a state broke the pact.', stance=None),
        S('a speech by a French deputy, 1926 (illustrative)', 'Germany has signed at Locarno. She accepts the Rhine frontier freely. For the first time since the war, France can sleep at night.',
          'French reactions to Locarno', 'It suggests Locarno gave France a sense of security.',
          'To welcome Locarno and support Briand\'s policy.', 'it shows French opinion at the time', 'it is a political speech by a supporter of the policy',
          'It does not mention Germany\'s eastern borders.', stance=True, why='it shows Locarno increasing French security'),
        S('a historian writing in 1990 (illustrative)', 'Locarno was a mirage. Stresemann accepted the western frontier only to free his hands in the east, and France gained a guarantee that Britain had no means to honour.',
          'the significance of Locarno', 'The historian argues that Locarno gave only an illusion of security.',
          'To reassess Locarno with hindsight.', 'it draws on later evidence of Stresemann\'s aims', 'it is one interpretation and may be influenced by knowledge of later events',
          'It does not discuss the improvement in relations after 1925.', stance=False, why='it argues Locarno brought only an illusion of security', kind='secondary'),
    ],
})

CHAPTERS[8] = [l8a, l8b, l8c, l8d]


# ============================================================== CHAPTER 9: International option, the League of Nations and international relations in the 1930s

d9a = T('The impact of the Great Depression on international relations', 'great depression', 'impact of the great depression')
build_as(d9a, {
    'enq': 'the impact of the Depression on international relations', 'claim': 'the Great Depression was the main reason for the breakdown of international order in the 1930s',
    'stim': ['The Wall Street Crash began in October 1929.', 'In 1930 the USA passed the Smoot-Hawley Tariff.',
             'By early 1932 about six million Germans were registered as unemployed.'],
    'terms': [
        ('protectionism', 'protecting home industries from foreign competition by tariffs and quotas'),
        ('autarky', 'economic self-sufficiency, a goal of Nazi Germany'),
        ('Smoot-Hawley Tariff', 'the US tariff of 1930 that raised duties on imports and provoked retaliation'),
        ('Hoover Moratorium', 'the one-year suspension of war debt and reparations payments proposed by President Hoover in 1931'),
        ('imperial preference', 'the system of lower tariffs within the British Empire agreed at Ottawa in 1932'),
        ('Lausanne Conference', 'the conference of 1932 that effectively ended German reparations'),
    ],
    'dates': [('the Wall Street Crash began', 1929, 10), ('the Smoot-Hawley Tariff was passed', 1930, 6), ('the Hoover Moratorium was announced', 1931, 6),
              ('the Lausanne Conference effectively ended reparations', 1932, 7), ('Hitler became Chancellor of Germany', 1933, 1)],
    'mcq': [
        ('Why did the Depression hit Germany particularly hard?', 'Its recovery depended on short-term US loans that were recalled', ['It had no industry', 'It was still paying for the Napoleonic Wars', 'It had just joined the League'], '[1]'),
        ('Which Japanese export was badly hit by the collapse of US demand after 1929?', 'Silk', ['Oil', 'Wheat', 'Cars'], 'Rural Japan suffered severely, increasing support for expansion. [1]'),
        ('How did many countries respond to the Depression?', 'By raising tariffs to protect their own industries', ['By lowering tariffs to zero', 'By joining a single European currency', 'By giving more money to the League'], '[1]'),
    ],
    'why': [
        ('the Depression damaged international cooperation', ['Countries turned to protectionism and economic nationalism', 'Governments focused on domestic problems', 'Unemployment helped extremist parties such as the Nazis gain power',
                                                              'Japan and Italy looked to expansion to solve economic problems', 'Britain and France were less willing to enforce sanctions that hurt their trade'],
         'the Depression made states put national interests first, weakening cooperation and helping aggressive regimes gain support'),
        ('the Depression helped Hitler come to power', ['Mass unemployment caused despair', 'The Weimar governments seemed unable to cope', 'Nazi propaganda offered work and national revival', 'Fear of communism drove the middle classes and elites to the Nazis'],
         'the Depression turned the Nazis from a fringe party into the largest party by creating desperation and fear of communism'),
    ],
    'claims': [
        ('The Smoot-Hawley Tariff reduced US import duties.', False, 'It raised them, provoking retaliation and a collapse in world trade.'),
        ('The Lausanne Conference of 1932 effectively ended reparations.', True, 'Germany made no further payments.'),
        ('The Depression made Britain and France more willing to spend money on enforcing collective security.', False, 'It made them less willing.'),
    ],
    'ess': [
        dict(q='‘The Great Depression was the main reason for the breakdown of international order in the 1930s.’',
             pro=['It helped bring Hitler to power', 'It pushed Japan towards expansion in Manchuria', 'It made Britain and France reluctant to act or rearm'],
             con=['The aims of the dictators, especially Hitler\'s ideology, drove aggression', 'Weaknesses of the League existed before the Depression', 'British and French appeasement was a policy choice'],
             judge='the Depression created the conditions for aggression and weakened the will to resist it, but the decisions of the dictators turned crisis into war'),
        dict(q='How far did the Depression change Japanese foreign policy?',
             pro=['Collapse of silk exports caused rural poverty', 'The army gained support for expansion to secure resources', 'Manchuria was seen as an economic lifeline'],
             con=['Japan had ambitions in China before 1929', 'The army in Manchuria acted independently', 'Nationalism and militarism had long roots'],
             judge='the Depression greatly strengthened the case for expansion, but it accelerated ambitions that already existed'),
    ],
    'src': [
        S('a speech by a Japanese army officer, 1931 (illustrative)', 'Our villages starve while the silk markets of America are closed to us. Manchuria\'s coal and soil are our lifeline; we must secure them.',
          'Japanese motives for expansion', 'It suggests economic crisis drove Japanese expansion into Manchuria.',
          'To win support for action in Manchuria.', 'it shows the arguments used by the military at the time', 'it is propaganda for a policy of expansion',
          'It does not show the role of nationalism or the army\'s independence.', stance=True, why='it links Japanese aggression to the Depression'),
        S('a historian writing in 2000 (illustrative)', 'The slump did not create the ambitions of Hitler or the Japanese army. It removed the restraints that had held them in check.',
          'the Depression and international relations', 'The historian argues that the Depression removed restraints rather than creating ambitions.',
          'To offer a balanced interpretation.', 'it is a considered interpretation', 'it is one view among many',
          'It does not give detailed evidence.', stance=False, why='it argues the Depression was not the root cause', kind='secondary'),
    ],
})

d9b = T('The Manchurian Crisis and the Abyssinian Crisis: why the League failed', 'manchurian crisis', 'abyssinian crisis', 'why the league failed')
build_as(d9b, {
    'enq': 'the League\'s failures in the 1930s', 'claim': 'the League failed in the 1930s mainly because Britain and France put their own interests first',
    'stim': ['On 18 September 1931 an explosion on the South Manchurian Railway near Mukden gave the Japanese army an excuse to occupy Manchuria.', 'In October 1935 Italian forces invaded Abyssinia.',
             'In December 1935 the Hoare-Laval Pact proposed giving Italy much of Abyssinia.'],
    'terms': [
        ('Mukden incident', 'the explosion on the South Manchurian Railway in September 1931, staged by Japanese officers'),
        ('Manchukuo', 'the puppet state set up by Japan in Manchuria in 1932 under the former Chinese emperor Puyi'),
        ('Lytton Report', 'the League report of 1932 that condemned Japan\'s actions in Manchuria'),
        ('Hoare-Laval Pact', 'the secret British-French plan of December 1935 to give Italy much of Abyssinia'),
        ('Walwal incident', 'the clash on the Abyssinian border in December 1934 used by Mussolini as an excuse for war'),
        ('oil sanctions', 'the embargo on oil exports to Italy that the League never imposed'),
    ],
    'dates': [('the Mukden incident took place', 1931, 9), ('the Lytton Report was published', 1932, 10), ('Japan left the League', 1933, 3),
              ('Italy invaded Abyssinia', 1935, 10), ('Italian troops entered Addis Ababa', 1936, 5), ('Italy left the League', 1937, 12)],
    'mcq': [
        ('What did Japan do after the League accepted the Lytton Report?', 'It left the League', ['It withdrew from Manchuria', 'It paid compensation to China', 'It invaded Abyssinia'], '[1]'),
        ('Why did the League\'s sanctions against Italy fail to stop the invasion of Abyssinia?', 'They did not include oil, coal or steel, and the Suez Canal stayed open', ['Italy had no army', 'Abyssinia surrendered at once', 'The USA joined the sanctions'], '[1]'),
        ('Who appealed to the League in person for help in June 1936?', 'Haile Selassie', ['Puyi', 'Chiang Kai-shek', 'Ramsay MacDonald'], '[1]'),
    ],
    'why': [
        ('the League failed to stop Japan in Manchuria', ['Japan was a great power and a permanent member of the Council', 'Britain and France had no forces to spare in the Far East', 'The USA and USSR were not members', 'The Lytton Report took a year to produce', 'Economic sanctions would have hurt members during the Depression'],
         'no power was willing or able to take action against Japan in the Far East, so the League could only condemn'),
        ('the League failed to stop Italy in Abyssinia', ['Britain and France wanted Mussolini as an ally against Hitler', 'Sanctions excluded oil and the Suez Canal stayed open', 'The Hoare-Laval Pact destroyed the League\'s credibility', 'Hitler\'s remilitarisation of the Rhineland diverted attention'],
         'Britain and France put the hope of an alliance with Mussolini against Hitler above collective security'),
    ],
    'claims': [
        ('The League imposed oil sanctions on Italy in 1935.', False, 'Oil was excluded from sanctions.'),
        ('The Lytton Report condemned Japan.', True, 'It recommended Manchuria be returned to Chinese sovereignty with autonomy.'),
        ('Abyssinia was a member of the League of Nations.', True, 'It had joined in 1923.'),
    ],
    'ess': [
        dict(q='‘The League failed in the 1930s mainly because Britain and France put their own interests first.’',
             pro=['They would not risk war with Japan in the Far East', 'They wanted Mussolini as an ally and did the Hoare-Laval deal', 'They feared the economic cost of sanctions during the Depression'],
             con=['The League\'s structure, unanimity and lack of an army, made action hard', 'The absence of the USA made sanctions ineffective', 'The aggressors were determined and simply left the League'],
             judge='the League\'s structural weaknesses mattered, but in each crisis it failed because Britain and France chose not to use the powers it had'),
        dict(q='How far was the Abyssinian crisis more damaging to the League than the Manchurian crisis?',
             pro=['Abyssinia was in Europe\'s sphere and closer to Britain and France, so failure was more obvious', 'The Hoare-Laval Pact showed members undermining their own League', 'It drove Mussolini towards Hitler'],
             con=['Manchuria set the precedent that aggression would go unpunished', 'Japan\'s departure showed great powers could defy the League', 'Both crises revealed the same weaknesses'],
             judge='Manchuria showed the League\'s weakness, but Abyssinia destroyed its credibility because sanctions were imposed and then undermined by its leading members'),
    ],
    'src': [
        S('Haile Selassie, speech to the League Assembly, June 1936 (translated, abridged)', 'It is collective security: it is the very existence of the League of Nations. It is the confidence that each State is to place in international treaties. God and history will remember your judgment.',
          'the Abyssinian crisis', 'It suggests the League\'s failure to protect Abyssinia threatened collective security itself.',
          'To appeal for help and shame members into acting.', 'it is the emperor\'s own words at the time', 'he was pleading for his country and wanted to persuade',
          'It does not explain why Britain and France did not act.', stance=None),
        S('a memorandum by a British Foreign Office official, 1935 (illustrative)', 'We cannot risk driving Mussolini into the arms of Hitler. Whatever the League may say, Italy\'s friendship on the Brenner is worth more to us than Abyssinia.',
          'British policy over Abyssinia', 'It suggests Britain put its strategic interest in Italy above the League.',
          'To advise ministers on policy.', 'it shows thinking inside government', 'one official\'s view may not be government policy',
          'It does not show the public mood.', stance=True, why='it shows British interests overriding collective security'),
        S('a historian writing in 1990 (illustrative)', 'The League could only be as strong as its members wished it to be, and its structure gave the reluctant every excuse for inaction.',
          'the League\'s failure', 'The historian argues that the League\'s weakness lay in its members and its structure.',
          'To explain the failure of collective security.', 'it is a considered interpretation', 'it gives no detailed evidence',
          'It does not discuss specific decisions.', stance=False, why='it stresses structural weakness as well as members\' choices', kind='secondary'),
    ],
})

d9c = T("Hitler's foreign policy and the policy of appeasement", "hitler's foreign policy", 'appeasement')
build_as(d9c, {
    'enq': 'appeasement', 'claim': 'appeasement was a sensible policy for Britain in the 1930s',
    'stim': ['In March 1936 German troops marched into the demilitarised Rhineland.', 'In March 1938 Germany annexed Austria (the Anschluss).',
             'At Munich on 29-30 September 1938 Britain, France, Germany and Italy agreed that Germany should take the Sudetenland.'],
    'terms': [
        ('appeasement', 'the policy of avoiding war by meeting reasonable grievances through negotiation and concessions'),
        ('Anschluss', 'the union of Germany and Austria in March 1938, forbidden by the Treaty of Versailles'),
        ('Sudetenland', 'the border regions of Czechoslovakia with a large German-speaking population'),
        ('Stresa Front', 'the agreement of April 1935 between Britain, France and Italy to oppose German breaches of the treaties'),
        ('Lebensraum', 'living space, Hitler\'s aim of conquering land in the east for German settlement'),
        ('Anglo-German Naval Agreement', 'the agreement of 1935 allowing Germany a navy of 35 per cent of the British surface fleet'),
    ],
    'dates': [('Germany left the Disarmament Conference and the League', 1933, 10), ('the Saar voted to return to Germany', 1935, 1), ('the Anglo-German Naval Agreement was signed', 1935, 6),
              ('German troops remilitarised the Rhineland', 1936, 3), ('the Anschluss took place', 1938, 3), ('the Munich Agreement was signed', 1938, 9), ('German troops occupied Prague', 1939, 3)],
    'mcq': [
        ('Which agreement in 1935 undermined the Stresa Front?', 'The Anglo-German Naval Agreement', ['The Munich Agreement', 'The Nazi-Soviet Pact', 'The Pact of Steel'], '[1]'),
        ('Why did Britain not act against the remilitarisation of the Rhineland?', 'Many thought Germany was only moving into its own territory', ['Britain had no army', 'France asked Britain to support Germany', 'The League had approved it'], '[1]'),
        ('What did Chamberlain claim after returning from Munich?', '"Peace for our time"', ['"Blood, toil, tears and sweat"', '"Iron and blood"', '"The lamps are going out all over Europe"'], '[1]'),
        ('When did Britain guarantee Poland\'s independence?', 'March 1939', ['September 1938', 'March 1936', 'August 1939'], 'After the German occupation of Prague. [1]'),
    ],
    'why': [
        ('Britain followed a policy of appeasement', ['Fear of another war like 1914-18 and of bombing', 'Britain was not ready militarily and needed time to rearm', 'Many felt the Treaty of Versailles was unfair to Germany',
                                                      'The Dominions and the USA would not support war', 'Communism was seen as a greater threat', 'Economic problems after the Depression'],
         'appeasement reflected public fear of war and Britain\'s military weakness, as well as a genuine belief that German grievances were reasonable'),
        ('the occupation of Prague in March 1939 ended appeasement', ['It was the first time Hitler took non-German territory', 'It showed Hitler could not be trusted after Munich', 'British public opinion turned against further concessions', 'Britain\'s rearmament had progressed'],
         'Prague proved that Hitler\'s aims went beyond revising Versailles, which destroyed the case for appeasement'),
    ],
    'claims': [
        ('Czechoslovakia was invited to the Munich Conference.', False, 'It was not represented at the conference.'),
        ('The Saar plebiscite of 1935 was held under League supervision.', True, 'About 90 per cent voted to return to Germany.'),
        ('Britain went to war when Germany remilitarised the Rhineland.', False, 'Britain and France did nothing beyond protesting.'),
    ],
    'ess': [
        dict(q='‘Appeasement was a sensible policy for Britain in the 1930s.’',
             pro=['Britain was not ready for war and used the time to rearm, especially in the air', 'Public opinion and the Dominions opposed war in 1938', 'Some German grievances over Versailles seemed reasonable'],
             con=['It encouraged Hitler to make further demands', 'It sacrificed Czechoslovakia and its strong defences', 'It alienated the USSR and led to the Nazi-Soviet Pact'],
             judge='appeasement was understandable given Britain\'s weakness and public mood, but continuing it after Hitler\'s aims became clear in 1938 was a serious misjudgement'),
        dict(q='To what extent was Hitler\'s foreign policy planned?',
             pro=['Mein Kampf set out aims of overturning Versailles and gaining Lebensraum', 'The Hossbach Memorandum of 1937 shows plans for expansion', 'Rearmament from 1933 prepared for war'],
             con=['Hitler exploited opportunities such as the Anschluss crisis', 'Timing often depended on others\' actions', 'He did not expect war with Britain in 1939'],
             judge='Hitler had long-term aims but was an opportunist in their timing and method'),
    ],
    'src': [
        S('Neville Chamberlain, radio broadcast, 27 September 1938 (abridged)', 'How horrible, fantastic, incredible it is that we should be digging trenches and trying on gas masks here because of a quarrel in a far-away country between people of whom we know nothing.',
          'British attitudes to Czechoslovakia', 'Chamberlain suggests that Britain should not go to war over a distant dispute.',
          'To prepare the British public for a settlement over Czechoslovakia.', 'it is the prime minister\'s own words at the height of the crisis', 'it was a broadcast designed to shape public opinion',
          'It does not discuss British rearmament.', stance=True, why='it reflects the public fear of war that made appeasement seem sensible'),
        S('Winston Churchill, speech in the House of Commons, 5 October 1938 (abridged)', 'We have sustained a total and unmitigated defeat. And do not suppose that this is the end. This is only the beginning of the reckoning.',
          'reactions to Munich', 'It suggests Munich was a defeat that would encourage Hitler.',
          'To attack the government\'s policy.', 'it shows the view of critics at the time', 'Churchill was a long-standing opponent of the policy and out of office, so he had reasons to attack it',
          'It does not consider Britain\'s military weakness.', stance=False, why='it argues appeasement was a disaster'),
    ],
})

d9d = T('The outbreak of war in 1939: responsibility and interpretations', 'outbreak of war in 1939', 'responsibility and interpretations')
build_as(d9d, {
    'enq': 'the outbreak of war in 1939', 'claim': 'Hitler was responsible for the outbreak of war in 1939',
    'stim': ['On 23 August 1939 Germany and the USSR signed a non-aggression pact.', 'German forces invaded Poland on 1 September 1939.',
             'Britain and France declared war on Germany on 3 September 1939.'],
    'terms': [
        ('Nazi-Soviet Pact', 'the non-aggression pact of August 1939 between Germany and the USSR, with a secret protocol dividing eastern Europe'),
        ('Polish Corridor', 'the strip of land giving Poland access to the sea, which separated East Prussia from the rest of Germany'),
        ('Danzig', 'the German-speaking free city under League supervision that Hitler demanded in 1939'),
        ('Hossbach Memorandum', 'the record of a meeting in November 1937 at which Hitler outlined plans for expansion'),
        ('Guilty Men', 'the book of 1940 that blamed British politicians for appeasement'),
        ('Pact of Steel', 'the military alliance between Germany and Italy signed in May 1939'),
    ],
    'dates': [('Britain guaranteed Poland', 1939, 3), ('Germany and Italy signed the Pact of Steel', 1939, 5), ('the Nazi-Soviet Pact was signed', 1939, 8),
              ('Germany invaded Poland', 1939, 9.01), ('Britain and France declared war on Germany', 1939, 9.03)],
    'mcq': [
        ('Which historian argued in 1961 that Hitler was an opportunist who did not plan a general war?', 'A. J. P. Taylor', ['Fritz Fischer', 'E. H. Carr', 'Ian Kershaw'], 'In The Origins of the Second World War. [1]'),
        ('Why did Stalin sign the Nazi-Soviet Pact?', 'He distrusted Britain and France and wanted time and territory', ['He had been defeated by Germany', 'He wanted to join the Axis permanently', 'The League ordered him to'], '[1]'),
        ('What did the secret protocol of the Nazi-Soviet Pact provide?', 'The division of Poland and eastern Europe into spheres of influence', ['A joint attack on Britain', 'Soviet membership of the League', 'The return of Alsace-Lorraine'], '[1]'),
    ],
    'why': [
        ('Britain declared war on Germany in September 1939', ['Germany invaded Poland, which Britain had guaranteed', 'Prague had shown Hitler could not be trusted', 'Public opinion now supported resistance', 'Rearmament had made Britain more prepared'],
         'Britain declared war because Hitler\'s invasion of Poland proved that only force would stop him'),
        ('Hitler was prepared to risk war over Poland in 1939', ['The Nazi-Soviet Pact removed the danger of a two-front war', 'He believed Britain and France would back down again', 'He wanted Lebensraum in the east', 'German rearmament gave him a temporary advantage'],
         'the Nazi-Soviet Pact convinced Hitler that he could attack Poland without a war on two fronts'),
    ],
    'claims': [
        ('A. J. P. Taylor argued that Hitler followed a detailed blueprint for war.', False, 'Taylor argued Hitler was an opportunist who exploited the mistakes of others.'),
        ('The Nazi-Soviet Pact contained a secret protocol dividing Poland.', True, 'It divided eastern Europe into spheres of influence.'),
        ('Britain and France declared war on 1 September 1939.', False, 'They declared war on 3 September, after Germany ignored their ultimatum.'),
    ],
    'ess': [
        dict(q='‘Hitler was responsible for the outbreak of war in 1939.’',
             pro=['His aims of Lebensraum and overturning Versailles required war', 'He broke the Munich Agreement by taking Prague', 'He invaded Poland knowing Britain had guaranteed it'],
             con=['Appeasement encouraged him to think Britain would not fight', 'The Nazi-Soviet Pact made the invasion possible', 'The Treaty of Versailles and the failure of the League created the conditions', 'Taylor argued he blundered into a war he did not want in 1939'],
             judge='others made war more likely, but Hitler\'s aims and his decision to invade Poland make him primarily responsible'),
        dict(q='How far was the Nazi-Soviet Pact the main cause of the outbreak of war in 1939?',
             pro=['It removed the threat of a two-front war for Hitler', 'It made the invasion of Poland possible', 'It ended Anglo-French hopes of an alliance with the USSR'],
             con=['Hitler\'s aims were the underlying cause', 'Appeasement had encouraged him', 'Britain\'s guarantee to Poland made a German attack a cause of general war'],
             judge='the Pact was the immediate trigger that made Hitler confident to attack, but it was a means to his aims rather than the main cause'),
    ],
    'src': [
        S('A. J. P. Taylor, The Origins of the Second World War, 1961 (summary of the argument)', 'Taylor argued that Hitler was a traditional German statesman who exploited opportunities created by others, and that the war of 1939 resulted from diplomatic blunders on all sides.',
          'responsibility for the war', 'Taylor argues that responsibility was shared and that Hitler was an opportunist.',
          'To challenge the view that the war was the result of a Nazi plan.', 'Taylor was a leading historian who used diplomatic documents', 'his interpretation was controversial and was criticised for ignoring Nazi ideology',
          'It does not give weight to Hitler\'s racial aims.', stance=False, why='it argues responsibility was shared', kind='secondary'),
        S('the Hossbach Memorandum, November 1937 (summary)', 'The record of the meeting states that Hitler told his commanders that Germany\'s problem of living space could be solved only by force, and that action against Austria and Czechoslovakia might come as early as 1938.',
          'Hitler\'s aims', 'It suggests Hitler planned expansion by force.',
          'To record a meeting between Hitler and his commanders.', 'it is a record made at the time by Hitler\'s adjutant', 'it was written from memory days later and its status as a "plan" is disputed',
          'It does not mention Poland or war with Britain in 1939.', stance=True, why='it shows Hitler intended expansion by force'),
        S('a historian writing in 2000 (illustrative)', 'The road to war ran through Hitler\'s ideology. Others made mistakes, but only one man wanted to conquer the east and was willing to risk war to do it.',
          'responsibility for the war', 'The historian argues that Hitler\'s ideology was the main cause of war.',
          'To restate the case for Hitler\'s responsibility.', 'it reflects later research on Nazi aims', 'it is one interpretation',
          'It does not discuss appeasement.', stance=True, why='it places responsibility on Hitler', kind='secondary'),
    ],
})

CHAPTERS[9] = [d9a, d9b, d9c, d9d]
finalize(CHAPTERS)
