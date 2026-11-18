"""Cambridge International AS Level Law 9084 (grade 11): English legal system + criminal law.

Paper 1 (English Legal System: short compulsory questions + essays) and Paper 2 (Criminal Law:
problem scenario + essay) style items. Each topic is built from a content spec by `Law.T()`:
definitions, fixed MCQs, leading cases (name, facts, principle), assertion-reason pairs,
explain items, comparisons, problem-scenario frames with invented parties and evaluation
essays. The `Law` class is reused by the grade 12 module (contract and tort).
"""
import re
from ._lib import topic, mcq, compose, CTX, PEOPLE, CITIES

PROFILE = {'mark_scale': {'long': (3, 2.5), 'case': (2, 2)}, 'wordy': True}

AR_OPTS = ['Both A and R are true, and R is the correct explanation of A.',
           'Both A and R are true, but R is not the correct explanation of A.',
           'A is true but R is false.',
           'A is false but R is true.']
AR_WHY = {'A': 'Both statements are correct and R explains why A is true.',
          'B': 'Both statements are correct, but R does not explain A.',
          'C': 'A is correct; R is incorrect.',
          'D': 'A is incorrect; R is a correct statement.'}


def cap(s):
    s = s.strip()
    if not s:
        return s
    s = s[0].upper() + s[1:]
    return s if s[-1] in '.?!' else s + '.'


PROPER = {'Parliament', 'Hansard', 'House', 'Supreme', 'Court', 'Crown', 'King', 'Queen', 'English', 'European', 'Lord', 'Acts',
          'Act', 'Practice', 'Law', 'Royal', 'Privy', 'Rylands', 'Heydon', 'I', 'UK', 'Ministers', 'Juries'}


def lc(s):
    w = s.split(' ', 1)[0]
    return s if (w in PROPER or w.isupper()) else s[0].lower() + s[1:]


def nearest(want, allowed, default):
    if want and want >= min(allowed) - 1:
        return min(allowed, key=lambda m: (abs(m - want), m))
    return default


class _Fill(dict):
    def __missing__(self, k):
        return '{' + k + '}'


_ART = re.compile(r"(?<![(\w'])(a) (?=(?![Oo]ne\b|[Ee]u)[aeioAEIO][a-z])")


def art(s):
    """Fix 'a' before a vowel sound produced by slot filling (a antique -> an antique)."""
    return _ART.sub(lambda m: m.group(1) + 'n ', s)


def realise(r, fr):
    """Turn a scenario frame (dict with {A}/{B}/{C}/{E}/{city} and slot placeholders) into text."""
    if callable(fr):
        fr = fr(r)
    A, B, C, E = r.sample(PEOPLE, 4)
    v = {'A': A, 'B': B, 'C': C, 'E': E, 'city': r.choice(CITIES)}
    for k, opts in fr.get('slots', {}).items():
        x = r.choice(opts)
        x = tuple(y.format_map(_Fill(v)) for y in x) if isinstance(x, tuple) else x.format_map(_Fill(v))
        if isinstance(x, tuple):
            v[k] = x[0]
            for i, y in enumerate(x[1:], 1):
                v[f'{k}_{i}'] = y
        else:
            v[k] = x
    out = {}
    for k, x in fr.items():
        if k == 'slots':
            continue
        if isinstance(x, str):
            out[k] = art(x.format_map(_Fill(v)))
        elif isinstance(x, (list, tuple)):
            out[k] = [art(y.format_map(_Fill(v))) for y in x]
        else:
            out[k] = x
    out['_v'] = v
    return out


def split_marks(m):
    """AO split for a problem answer: knowledge, application, conclusion."""
    if m <= 2:
        return m, 0, 0
    c = 1
    k = max(1, round(m * 0.4))
    return k, m - k - c, c


def key_problem(m, s):
    k, a, c = split_marks(m)
    law, app = s['law'], s['apply']
    if m <= 2:
        return f"1 mark: identifies {s['issue']}. 1 mark: states the rule correctly, e.g. {law[0]}. [{m}]"
    out = (f"AO1 Knowledge [{k}]: identifies {s['issue']}; accurate statement of the law, e.g. {'; '.join(law)}. "
           f"AO2 Application [{a}]: applies the rules to the facts, e.g. {'; '.join(app)}. "
           f"Conclusion [{c}]: {s['concl']}")
    if m >= 6:
        out += ' Top band needs case authority used accurately and every relevant issue applied, not just described.'
    return out + f' [{m}]'


def ans_problem(s):
    return f"Law: {'; '.join(s['law'])}. Application: {'; '.join(s['apply'])}. Conclusion: {cap(s['concl'])}"


def key_essay(m, fo, ag, cases, crit=''):
    k = max(2, round(m * 0.4))
    e = m - k
    return (f"AO1 Knowledge and understanding [{k}]: accurate explanation of the law with supporting authority, e.g. {'; '.join(cases)}. "
            f"AO3 Analysis and evaluation [{e}]: arguments supporting the view, e.g. {'; '.join(fo)}; arguments against / problems, e.g. {'; '.join(ag)}. "
            f"Levels: L1 basic, descriptive points; L2 some accurate law with limited comment; L3 accurate law and some developed evaluation; "
            f"L4 wide-ranging, accurate law with sustained, balanced evaluation and a reasoned conclusion{(' (' + crit + ')') if crit else ''}. [{m}]")


def ans_essay(fo, ag, concl):
    return f"For: {'; '.join(fo)}. Against: {'; '.join(ag)}. Conclusion: {cap(concl)}"


ESSAY_WRAP = [
    '{q}',
    'With reference to decided cases and statutory provisions where relevant, {ql}',
    '{q} Your answer should consider arguments on both sides and reach a conclusion.',
    '{q} Support your answer with relevant authority.',
    'Using your knowledge of the law, {ql}',
]


class Law:
    def __init__(self):
        self.CHAPTERS = {}
        self.DEFS = {}
        self.CASES = {}
        self.ALLCASES = []
        self.TOPICS = []

    # ------------------------------------------------------------------ topic builder
    def T(self, ch, name, defs=(), mcqs=(), cases=(), ars=(), exps=(), cmps=(), scen=(), ev=(), area=None):
        t = topic(name, name)
        t.ch = ch
        t.area = area or name[0].lower() + name[1:]
        t.defs, t.cases, t.scen, t.ev, t.cmps = list(defs), list(cases), list(scen), list(ev), list(cmps)
        t.entries = {}
        self.DEFS.setdefault(ch, []).extend(defs)
        self.CASES.setdefault(ch, []).extend(cases)
        self.ALLCASES.extend(cases)
        self.CHAPTERS.setdefault(ch, []).append(t)
        self.TOPICS.append(t)
        L = self

        # ---- C1: definitions -------------------------------------------------------
        for i, (term, d) in enumerate(defs):
            for j, stem in enumerate((f"Define the term '{term}'.", f"State what is meant by '{term}'.")):
                key = f'1 mark: basic/partial definition; 2 marks: full and accurate definition, i.e. {d[0].lower() + d[1:]} [2]'
                if j == 0:
                    t.entries.setdefault('C1', []).append(((stem, d, key), (1, 2)))

                def fn(r, D, stem=stem, d=d, key=key):
                    return {'stem': stem, 'answer': d, 'key': key, 'type': 'short', 'marks': 2}
                fn.__name__ = 'def_short'
                t.add('C1', (1, 2, 3), 'short')(fn)

        if defs:
            @t.add('C1', (1, 2), 'mcq')
            def def_mcq(r, D):
                term, d = r.choice(t.defs)
                others = [x for x in L.DEFS[ch] if x[0] != term and x[1] != d]
                if len(others) < 3:
                    return None
                ds = [x[1] for x in r.sample(others, 3)]
                opts, ans = mcq(r, d, ds)
                stem = r.choice([f"Which of the following best defines '{term}'?", f"Which statement correctly explains the meaning of '{term}'?"])
                return {'stem': stem, 'options': opts, 'answer': ans, 'key': f'{term}: {d}', 'marks': 1}

            @t.add('C1', (1, 2, 3), 'mcq')
            def def_rev(r, D):
                term, d = r.choice(t.defs)
                others = [x for x in L.DEFS[ch] if x[0] != term]
                if len(others) < 3:
                    return None
                ds = [x[0] for x in r.sample(others, 3)]
                opts, ans = mcq(r, term, ds)
                return {'stem': f'Which legal term is described here: "{d}"', 'options': opts, 'answer': ans,
                        'key': f'This is the definition of {term}.', 'marks': 1}

        # ---- C1: fixed MCQs ----------------------------------------------------------
        for (stem, a, dis, why) in mcqs:
            def fn(r, D, stem=stem, a=a, dis=dis, why=why):
                opts, ans = mcq(r, a, list(dis))
                return {'stem': stem, 'options': opts, 'answer': ans, 'key': f'{a}. {why}', 'marks': 1}
            fn.__name__ = 'mcq_fixed'
            t.add('C1', (1, 2, 3), 'mcq')(fn)

        # ---- C1: case-law MCQs ---------------------------------------------------------
        if cases:
            @t.add('C1', (1, 2, 3), 'mcq')
            def case_mcq(r, D):
                c = r.choice(t.cases)
                pool = [x for x in L.CASES[ch] if x[0] != c[0]]
                if len(pool) < 3:
                    pool += [x for x in L.ALLCASES if x[0] != c[0] and x not in pool]
                if len(pool) < 3:
                    return None
                v = r.randrange(3)
                if v == 0:
                    ds = [x[0] for x in r.sample(pool, 3)]
                    opts, ans = mcq(r, c[0], ds)
                    stem = f'Which case is authority for the principle that {lc(c[2]).rstrip(".")}?'
                elif v == 1:
                    ds = [x[0] for x in r.sample(pool, 3)]
                    opts, ans = mcq(r, c[0], ds)
                    stem = r.choice([f'Which case concerned these facts: {lc(c[1]).rstrip(".")}?', f'Identify the case in which {lc(c[1]).rstrip(".")}.'])
                else:
                    ds = [cap(x[2]) for x in r.sample(pool, 3)]
                    opts, ans = mcq(r, cap(c[2]), ds)
                    stem = f'What principle was established or applied in {c[0]}?'
                return {'stem': stem, 'options': opts, 'answer': ans,
                        'key': f'{c[0]}: {c[1]}; held/principle: {c[2]}', 'marks': 1}

        # ---- C2: assertion-reason ----------------------------------------------------------
        for (A, R, code) in ars:
            def fn(r, D, A=A, R=R, code=code):
                ans = AR_OPTS['ABCD'.index(code)]
                return {'stem': f'Assertion (A): {A} Reason (R): {R} Choose the correct option.', 'options': list(AR_OPTS),
                        'answer': ans, 'key': f'{ans} {AR_WHY[code]}', 'marks': 1}
            fn.__name__ = 'ar'
            t.add('C2', (1, 2, 3), 'mcq')(fn)

        # ---- C2: fixed explain items ------------------------------------------------------
        for e in exps:
            t.entries.setdefault('C2', []).append((e, (2, 3)))

            def fn(r, D, e=e):
                m = int(e[2].rsplit('[', 1)[1].rstrip('].')) if '[' in e[2] else 2
                return {'stem': e[0], 'answer': e[1], 'key': e[2], 'type': 'explain', 'marks': m}
            fn.__name__ = 'exp_fixed'
            t.add('C2', (1, 2, 3, 4), 'explain')(fn)

        # ---- C2: significance of a case -------------------------------------------------------
        if cases:
            @t.add('C2', (1, 2, 3, 4), 'explain')
            def case_explain(r, D):
                c = r.choice(t.cases)
                if D <= 2:
                    stem = r.choice([f'Briefly explain the legal principle established in {c[0]}.',
                                     f'State the facts and the decision in {c[0]}.'])
                    return {'stem': stem, 'answer': f'Facts: {c[1]}. Principle: {cap(c[2])}',
                            'key': f'1 mark: relevant facts ({c[1]}). 1 mark: the principle/decision ({c[2]}). [2]', 'type': 'explain', 'marks': 2}
                stem = r.choice([f'Explain the significance of the decision in {c[0]} for the law on {t.area}.',
                                 f'Using {c[0]} as an example, explain how the courts approach {t.area}.',
                                 f'Describe the facts of {c[0]} and explain why the case is important.'])
                m = 3 if D == 3 else 4
                key = (f'1 mark: facts ({c[1]}). 1 mark: decision/principle ({c[2]}). 1 mark: explains its significance for {t.area}'
                       + (', e.g. how it has been applied, developed or criticised in later cases' if m == 4 else '') + (' [1 further mark].' if m == 4 else '.') + f' [{m}]')
                return {'stem': stem, 'answer': f'Facts: {c[1]}. Principle: {cap(c[2])} This shows how the law on {t.area} is applied.',
                        'key': key, 'type': 'explain', 'marks': m}

        # ---- C2: comparisons --------------------------------------------------------------------
        if cmps:
            @t.add('C2', (1, 2, 3, 4), 'explain')
            def compare(r, D):
                x, y, diffs = r.choice(t.cmps)
                if D <= 2 or len(diffs) < 2:
                    stem = r.choice([f'State one difference between {x} and {y}.', f'Identify one way in which {x} differs from {y}.'])
                    return {'stem': stem, 'answer': cap(diffs[0]), 'key': f'1 mark: identifies a valid difference; 1 mark: both sides made clear, e.g. {"; ".join(diffs)}. [2]',
                            'type': 'explain', 'marks': 2}
                stem = r.choice([f'Explain two differences between {x} and {y}.', f'Distinguish between {x} and {y}, explaining two differences.'])
                return {'stem': stem, 'answer': cap(diffs[0]) + ' ' + cap(diffs[1]),
                        'key': f'2 × (1 mark identifies difference, 1 mark explains both sides). Valid differences include: {"; ".join(diffs)}. [4]', 'type': 'explain', 'marks': 4}

        # ---- C3 / C4: problem scenarios ----------------------------------------------------------
        if scen:
            @t.add('C3', (1, 2, 3, 4, 5), 'case')
            def problem(r, D):
                s = realise(r, r.choice(t.scen))
                want = CTX.get('want_marks')
                if D == 1 or (D == 2 and want == 1):
                    if s.get('owrong') and r.random() < 0.5:
                        opts, ans = mcq(r, cap(s['concl']), [cap(x) for x in s['owrong']])
                        stem = s['facts'] + ' ' + r.choice(['Which is the most likely legal outcome?', 'Which statement best describes the likely legal position?'])
                    else:
                        opts, ans = mcq(r, cap(s['issue']), [cap(x) for x in s['wrong']])
                        stem = s['facts'] + ' ' + s.get('iq', 'Which legal rule or issue is most directly raised by these facts?')
                    return {'stem': stem, 'options': opts, 'answer': ans,
                            'key': f"{ans} The facts raise {s['issue']}: {s['law'][0]}", 'marks': 1}
                if D == 2:
                    v = r.randrange(2)
                    q = ['Identify the main legal issue raised and state the relevant legal rule.',
                         'State, with a brief reason, the most likely legal outcome.'][v]
                    ans = (f"{cap(s['issue'])} {cap(s['law'][0])}" if v == 0 else f"{cap(s['concl'])} Reason: {s['law'][0]}")
                    key = (key_problem(2, s) if v == 0 else f"1 mark: correct outcome ({s['concl']}). 1 mark: reason based on the rule, e.g. {s['law'][0]}. [2]")
                    return {'stem': s['facts'] + ' ' + q, 'answer': ans, 'key': key, 'type': 'case', 'marks': 2}
                if D == 3:
                    m = nearest(want, (3, 4, 5, 6), 4)
                    tail = r.choice(['', ' Refer to at least one decided case.', ' Explain the relevant legal rules before applying them.'])
                else:
                    m = nearest(want, (6, 8, 10, 12), 8 if D == 4 else 10)
                    tail = r.choice([' Your answer should explain the relevant law, refer to decided cases and reach a reasoned conclusion.',
                                     ' Apply the relevant legal rules and case law to the facts, considering any alternative arguments.',
                                     ' Explain and apply the relevant law, using decided cases to support your advice.'])
                    if D == 5:
                        tail += ' Comment on any uncertainty in the law.'
                return {'stem': s['facts'] + ' ' + s['ask'] + tail, 'answer': ans_problem(s), 'key': key_problem(m, s), 'type': 'case', 'marks': m}

            @t.add('C4', (2, 3, 4, 5), 'case')
            def problem_parts(r, D):
                s = realise(r, r.choice(t.scen))
                parts = [
                    lambda r: ('Identify the main legal issue raised by these facts.', cap(s['issue']),
                               f"1 mark: identifies {s['issue']}; 1 mark: links it to the relevant facts. [2]"),
                    lambda r: (r.choice(['Explain the relevant legal rules, referring to decided cases.', 'Outline the law that applies, with supporting authority.']),
                               '; '.join(s['law']) + '.', f"Up to 4 marks for accurate law with authority: {'; '.join(s['law'])}. [4]"),
                    lambda r: (s['ask'], ans_problem(s), key_problem(6, s)),
                ]
                if t.ev:
                    q, fo, ag, cs, concl = t.ev[r.randrange(len(t.ev))]
                    m = 8 if D <= 3 else 10
                    parts.append(lambda r, q=q, fo=fo, ag=ag, cs=cs, concl=concl, m=m: (q, ans_essay(fo, ag, concl), key_essay(m, fo, ag, cs)))
                return compose(r, s['facts'], parts, k=(2, 3), type_='case')

            @t.add('C4', (3, 4, 5), 'case')
            def problem_full(r, D):
                s = realise(r, r.choice(t.scen))
                m = nearest(CTX.get('want_marks'), (8, 10, 12, 15, 20), {3: 10, 4: 12, 5: 15}[min(5, max(3, D))])
                tail = r.choice([' Explain the relevant law, apply it to the facts and evaluate the strength of any arguments available.',
                                 ' In your answer, refer to decided cases and assess how a court is likely to decide.',
                                 ' Consider all the relevant issues and reach a justified conclusion.'])
                return {'stem': s['facts'] + ' ' + s['ask'] + tail, 'answer': ans_problem(s), 'key': key_problem(m, s), 'type': 'case', 'marks': m}

        # ---- C4: essays ---------------------------------------------------------------------------
        if ev:
            @t.add('C4', (2, 3, 4, 5), 'long')
            def essay(r, D):
                q, fo, ag, cs, concl = r.choice(t.ev)
                m = nearest(CTX.get('want_marks'), (8, 10, 12, 15, 20), {2: 8, 3: 12, 4: 15, 5: 20}[min(5, max(2, D))])
                w = r.choice(ESSAY_WRAP)
                stem = w.format(q=q, ql=q[0].lower() + q[1:])
                return {'stem': stem, 'answer': ans_essay(fo, ag, concl), 'key': key_essay(m, fo, ag, cs), 'type': 'long', 'marks': m}

            if not scen:
                @t.add('C3', (1, 2, 3, 4, 5), 'explain')
                def essay_short(r, D):
                    q, fo, ag, cs, concl = r.choice(t.ev)
                    if D <= 2:
                        v = r.randrange(2)
                        pts = fo if v == 0 else ag
                        stem = (f'In the context of {t.area}, identify and briefly explain one argument ' + ('in favour of' if v == 0 else 'against') + ' the current law or system.')
                        return {'stem': stem, 'answer': cap(pts[0]), 'key': f'1 mark: valid point, e.g. {"; ".join(pts)}. 1 mark: brief explanation. [2]', 'type': 'explain', 'marks': 2}
                    m = 4 if D == 3 else 6
                    stem = f'Explain {"two" if m == 4 else "three"} points that could be used in answering the question: "{q}"'
                    return {'stem': stem, 'answer': '; '.join((fo + ag)[:3]) + '.', 'key': f'Per point: 1 mark identification, 1 mark development with authority. Points include: {"; ".join(fo + ag)}. [{m}]',
                            'type': 'explain', 'marks': m}
        return t


L = Law()
CHAPTERS = L.CHAPTERS
T = L.T

# =====================================================================================
# 1 Sources of law: parliamentary and delegated legislation
# =====================================================================================

T(1, 'Parliamentary law-making: Green and White Papers, the legislative process and Royal Assent', area='the legislative process',
  defs=[('Green Paper', 'A consultation document issued by the government setting out proposals for a possible new law so that interested parties can comment before firm decisions are made.'),
        ('White Paper', 'A document setting out the government\'s firm proposals for a new law, usually published after consultation and before a Bill is introduced.'),
        ('Royal Assent', 'The formal agreement of the monarch to a Bill that has passed through Parliament, after which the Bill becomes an Act of Parliament; by convention it is never refused.'),
        ('Private Members\' Bill', 'A public Bill introduced by an individual backbench MP or peer rather than by the government, often after success in the annual ballot.'),
        ('Private Bill', 'A Bill that affects only a particular person, organisation or place, such as a local authority or company, rather than the general public.')],
  mcqs=[('At which stage of a Bill\'s passage through the House of Commons is the main debate on its general principles held?', 'Second reading', ['First reading', 'Committee stage', 'Report stage'],
         'The second reading is the main debate on the principles of the Bill, followed by a vote; the first reading is a formality.'),
        ('Which stage involves a detailed, clause-by-clause examination of a Bill, usually by a Public Bill Committee?', 'Committee stage', ['Second reading', 'Third reading', 'First reading'],
         'At committee stage each clause is examined and amendments may be made.'),
        ('Under the Parliament Acts 1911 and 1949, for how long can the House of Lords normally delay a public Bill that is not a money Bill?', 'About one year', ['One month', 'Five years', 'Indefinitely'],
         'Non-money Bills can be delayed for about a year (passed by the Commons in two successive sessions); money Bills for one month.'),
        ('Which of these Acts was passed using the Parliament Acts, without the consent of the House of Lords?', 'Hunting Act 2004', ['Human Rights Act 1998', 'Constitutional Reform Act 2005', 'Consumer Rights Act 2015'],
         'The Hunting Act 2004 was passed under the Parliament Acts; its validity was upheld in R (Jackson) v Attorney-General (2005).'),
        ('What normally happens at the first reading of a Bill?', 'The title of the Bill is read out and it is ordered to be printed, with no debate', ['MPs debate the main principles and vote', 'Amendments are considered line by line', 'The monarch signs the Bill']
         , 'The first reading is a formality that introduces the Bill.')],
  cases=[('R (Jackson) v Attorney-General (2005)', 'supporters of fox hunting challenged the Hunting Act 2004, arguing that the Parliament Act 1949 (used to pass it) was itself invalid', 'the Parliament Act 1949 was valid, so Acts passed under the Parliament Acts without the Lords\' consent are valid Acts of Parliament')],
  ars=[('The House of Lords cannot usually prevent a public Bill passed by the House of Commons from eventually becoming law.', 'The Parliament Acts 1911 and 1949 limit the power of the House of Lords to delaying most public Bills for about one year.', 'A'),
       ('The monarch regularly refuses Royal Assent to Bills that the government opposes.', 'By convention, Royal Assent is given to every Bill that has properly passed through Parliament.', 'D'),
       ('A Green Paper sets out the firm proposals that will appear in a Bill.', 'Green Papers are consultation documents.', 'D')],
  exps=[('Explain the purpose of the committee stage in the passage of a Bill.', 'A committee of MPs examines each clause in detail and can propose amendments, so errors and weaknesses are corrected before the Bill returns to the full House.', '1 mark: detailed clause-by-clause scrutiny; 1 mark: amendments can be made / improves quality of the law. [2]'),
        ('Explain how consultation through a Green Paper may improve the quality of legislation.', 'Interested parties, experts and the public can comment on the proposals before they are finalised, so problems are identified early and the final law is more workable and more widely accepted.', '1 mark: allows interested parties/experts to comment; 1 mark: problems identified before law is fixed; 1 mark: better quality / greater acceptance. [3]'),
        ('Describe what happens at the report stage and third reading of a Bill.', 'At report stage the amended Bill is reported back to the whole House, which considers and votes on the amendments; at third reading there is a final vote on the Bill as a whole, with only limited debate.', '1 mark: report stage – amendments reported to whole House; 1 mark: amendments debated/voted on; 1 mark: third reading – final vote, limited debate. [3]'),
        ('Explain why Royal Assent is regarded as a formality.', 'By constitutional convention the monarch always gives Royal Assent to a Bill that has passed through Parliament; it has not been refused since 1707.', '1 mark: convention that it is always given; 1 mark: last refused in 1707 (Queen Anne) / monarch acts on advice of ministers. [2]')],
  cmps=[('a Green Paper', 'a White Paper', ['a Green Paper is a consultation document while a White Paper sets out firm proposals', 'a Green Paper invites comments on possible options while a White Paper states the policy the government intends to legislate on', 'a Green Paper comes earlier in the process, a White Paper usually follows consultation']),
        ('a Public Bill', 'a Private Bill', ['a Public Bill affects the whole country while a Private Bill affects only particular individuals, organisations or places', 'Public Bills are usually introduced by the government, Private Bills are promoted by the organisation concerned', 'Public Bills deal with matters of public policy, Private Bills give particular bodies powers, e.g. to build a railway']),
        ('a Government Bill', 'a Private Members\' Bill', ['a Government Bill is introduced by a minister while a Private Members\' Bill is introduced by a backbench MP', 'Government Bills have priority for parliamentary time while Private Members\' Bills have very limited time', 'Government Bills usually succeed because of the government majority while most Private Members\' Bills fail'])],
  scen=[dict(facts='The government of a country with a Westminster-style Parliament wants to introduce a new law on {area}. The minister, {A}, is unsure whether to consult before drafting the Bill and how long the process will take.',
             slots={'area': ['the use of electric scooters on public roads', 'online safety for children', 'carrying knives in public places', 'single-use plastic packaging', 'the regulation of artificial intelligence']},
             issue='the legislative process for a Government Bill, including consultation by Green and White Papers', wrong=['the making of delegated legislation by statutory instrument', 'the creation of law by judicial precedent', 'the making of by-laws by a local authority'],
             iq='Which process is most relevant to the minister\'s plan?',
             ask='Describe to {A} the stages through which the Bill must pass before it becomes law.',
             law=['a Green Paper may be published for consultation, followed by a White Paper of firm proposals', 'first reading is formal; second reading is the main debate and vote on principles', 'committee stage examines each clause and may amend; report stage considers amendments; third reading is a final vote', 'the Bill then goes through the same stages in the House of Lords; the Parliament Acts 1911 and 1949 limit the Lords to delay', 'Royal Assent turns the Bill into an Act'],
             apply=['{A} should consult on {area} because the issue is technical and affects many groups', 'with a government majority the Bill is likely to pass the Commons', 'if the Lords object they can delay but not normally block the Bill', 'the Act may also need commencement orders before it takes effect'],
             concl='the Bill on {area} can become law once it has passed all stages in both Houses and received Royal Assent, which may take many months',
             owrong=['the minister can make the law immediately by issuing a White Paper', 'the Bill becomes law as soon as it passes its second reading in the House of Commons', 'the House of Lords can permanently veto the Bill']),
        dict(facts='{A}, a backbench MP, came {pos} in the annual ballot for Private Members\' Bills and wants to introduce a Bill on {area}. The government has not said whether it supports the Bill.',
             slots={'pos': ['first', 'second', 'third', 'fourth'], 'area': ['banning the sale of energy drinks to children', 'compulsory first-aid training in schools', 'protecting the names of rape victims in social media posts', 'requiring defibrillators in all sports centres']},
             issue='the procedure for and limits of Private Members\' Bills', wrong=['the Parliament Acts procedure', 'the negative resolution procedure for statutory instruments', 'the Law Commission\'s consolidation of statutes'],
             ask='Explain to {A} how the Bill becomes law and assess its chances of success.',
             law=['backbench MPs may introduce Private Members\' Bills; the ballot gives priority to about 20 MPs', 'the Bill must pass the same stages as other public Bills and receive Royal Assent', 'parliamentary time is very limited (mainly sitting Fridays), so opponents can talk out a Bill', 'successful examples include the Abortion Act 1967 and the Murder (Abolition of Death Penalty) Act 1965'],
             apply=['coming {pos} in the ballot gives {A} a reasonable amount of debating time', 'without government support the Bill is likely to run out of time or be talked out', 'cross-party support on {area} would improve its chances'],
             concl='the Bill can become law only if it passes all the usual stages; its chances depend heavily on government support and parliamentary time',
             owrong=['the Bill automatically becomes law because {A} won a place in the ballot', 'the Bill only needs approval by the House of Lords', 'Private Members\' Bills cannot deal with matters of public policy']),
        dict(facts='A Bill on {area} has been passed by the House of Commons, but the House of Lords voted it down {n} months ago. The Bill is not a money Bill. {A}, a government minister, asks whether it can still become law.',
             slots={'area': ['banning trail hunting with dogs', 'reforming the voting age', 'creating a new offence of spiking drinks', 'restricting protest outside abortion clinics'], 'n': ['two', 'four', 'six']},
             issue='the Parliament Acts 1911 and 1949', wrong=['the Practice Statement 1966', 'the doctrine of implied repeal', 'the ultra vires rule'],
             ask='Advise {A} whether the Bill can become law without the agreement of the House of Lords.',
             law=['under the Parliament Acts 1911 and 1949 the Lords can delay a non-money Bill for about one year', 'the Bill must be passed by the Commons in two successive sessions, then it can receive Royal Assent without the Lords\' consent', 'R (Jackson) v Attorney-General (2005) confirmed that Acts passed in this way are valid', 'by the Salisbury convention the Lords do not usually oppose manifesto Bills at second reading'],
             apply=['the Bill on {area} is not a money Bill, so the one-year delay applies', 'the Commons should pass it again in the next session', 'after that it can be presented for Royal Assent without the Lords'],
             concl='the Bill can become law without the Lords\' consent by using the Parliament Acts procedure, after a delay of about one year',
             owrong=['the Bill can never become law because the House of Lords has rejected it', 'the Bill becomes law automatically after one month', 'the Supreme Court must approve the Bill instead of the House of Lords'])],
  ev=[('Evaluate the effectiveness of the legislative process in Parliament as a way of making law.', ['laws are made by elected representatives and so are democratic', 'Bills receive detailed scrutiny at several stages in both Houses', 'consultation through Green Papers allows experts and the public to contribute', 'Parliament can reform whole areas of law at once, unlike judges'],
       ['the process is slow and time-consuming', 'a government with a large majority can dominate the Commons (elective dictatorship) and whip MPs', 'the House of Lords is unelected yet can delay legislation', 'Acts can be complex and badly drafted, requiring interpretation by the courts', 'little time is given to Private Members\' Bills'],
       ['Parliament Acts 1911 and 1949', 'R (Jackson) v Attorney-General (2005)', 'Green and White Papers', 'Private Members\' Bills such as the Abortion Act 1967'], 'the process is democratic and thorough but its effectiveness is limited by government domination and lack of time'),
      ('"The House of Lords plays a valuable role in the law-making process." Discuss.', ['the Lords revises and improves Bills, using expertise of members', 'it can ask the Commons to think again on controversial measures', 'it is less dominated by party politics, with many crossbench members'],
       ['its members are unelected, so it lacks democratic legitimacy', 'its powers are limited by the Parliament Acts, so it can only delay', 'the Salisbury convention means it rarely opposes manifesto commitments'],
       ['Parliament Acts 1911 and 1949', 'R (Jackson) v Attorney-General (2005)', 'Salisbury convention', 'House of Lords Act 1999'], 'the Lords is a valuable revising chamber but its lack of democratic legitimacy rightly limits its powers')])

T(1, 'Parliamentary sovereignty and the influences on Parliament', area='parliamentary sovereignty',
  defs=[('parliamentary sovereignty', 'The principle that Parliament is the supreme law-making body: it can make or unmake any law, no Parliament can bind its successors and no court can override or set aside an Act of Parliament.'),
        ('pressure group', 'An organised group of people who share a common interest or cause and try to influence government and Parliament to change, or not change, the law.'),
        ('Law Commission', 'An independent body set up by the Law Commissions Act 1965 to keep the law under review and recommend reform, codification, consolidation and repeal of obsolete laws.'),
        ('declaration of incompatibility', 'A statement by a higher court under section 4 of the Human Rights Act 1998 that an Act of Parliament is incompatible with a Convention right; it does not affect the validity of the Act.'),
        ('implied repeal', 'The rule that where a later Act conflicts with an earlier Act, the later Act prevails and the earlier one is repealed to the extent of the conflict, even if it does not say so.')],
  mcqs=[('Which writer set out the traditional three-part theory of parliamentary sovereignty?', 'A V Dicey', ['Lord Denning', 'Jeremy Bentham', 'Lord Bingham'], 'Dicey (1885): Parliament can make or unmake any law; it cannot bind its successors; no body can override an Act.'),
        ('If a higher court finds that an Act of Parliament is incompatible with a Convention right, what may it do under the Human Rights Act 1998?', 'Issue a declaration of incompatibility', ['Declare the Act void', 'Amend the wording of the Act', 'Order Parliament to repeal the Act'], 'Section 4 HRA allows a declaration of incompatibility; Parliament remains free to decide whether to change the law.'),
        ('Which body was set up in 1965 to keep the law under review and recommend reform?', 'The Law Commission', ['The Criminal Cases Review Commission', 'The Judicial Appointments Commission', 'The Law Society'], 'The Law Commissions Act 1965 created the Law Commission.'),
        ('Which of the following is most likely to be an insider pressure group?', 'The British Medical Association', ['A group of protesters who occupy a motorway', 'A newly formed online campaign with no contacts in government', 'A group that refuses to talk to ministers'], 'Insider groups are consulted regularly by government and have established links with it.'),
        ('Which Act followed a campaign by the Snowdrop pressure group after the Dunblane school shooting?', 'Firearms (Amendment) Act 1997', ['Human Rights Act 1998', 'Theft Act 1968', 'Children Act 1989'], 'The Snowdrop campaign led to the ban on most handguns in the Firearms (Amendment) Act 1997.')],
  cases=[('Pickin v British Railways Board (1974)', 'a landowner claimed that a private Act affecting his land had been obtained by misleading Parliament', 'courts cannot investigate whether an Act was properly passed; once it is on the Parliament roll it must be applied (the enrolled Act rule)'),
         ('Cheney v Conn (1968)', 'a taxpayer argued that tax raised under a Finance Act was unlawful because it helped fund nuclear weapons contrary to the Geneva Conventions', 'an Act of Parliament takes priority over international treaties and cannot be challenged in the courts as contrary to international law'),
         ('Ellen Street Estates v Minister of Health (1934)', 'it was argued that a 1919 Act on compensation could not be impliedly amended by a later 1925 Act', 'Parliament cannot bind its successors; a later Act impliedly repeals an inconsistent earlier Act'),
         ('R v Secretary of State for Transport, ex p Factortame (No 2) (1991)', 'Spanish fishing companies challenged the Merchant Shipping Act 1988, which restricted the registration of fishing boats', 'while the UK was in the EU, the courts could disapply an Act of Parliament that conflicted with directly effective EU law'),
         ('Bellinger v Bellinger (2003)', 'a transgender woman sought recognition of her marriage, which was void under the Matrimonial Causes Act 1973', 'where an Act cannot be read compatibly with Convention rights, the courts may only issue a declaration of incompatibility and leave reform to Parliament')],
  ars=[('A court in England cannot declare an Act of Parliament invalid.', 'Parliamentary sovereignty means no court can override or set aside an Act of Parliament.', 'A'),
       ('A declaration of incompatibility under the Human Rights Act 1998 makes the Act void.', 'Parliament is not obliged to change the law after a declaration of incompatibility.', 'D'),
       ('Pressure groups can influence the content of legislation.', 'Pressure groups can make laws themselves.', 'C')],
  exps=[('Explain what is meant by the rule that Parliament cannot bind its successors.', 'Each Parliament is sovereign, so a later Parliament can repeal or amend any Act passed by an earlier one; an Act cannot be entrenched against future change.', '1 mark: later Parliament can repeal/amend any earlier Act; 1 mark: no Act can be entrenched, e.g. implied repeal (Ellen Street Estates). [2]'),
        ('Explain two ways in which pressure groups try to influence Parliament.', 'Lobbying MPs and ministers directly and responding to consultations; and public campaigns using the media, petitions and demonstrations to put pressure on politicians.', '2 × (1 mark method, 1 mark explanation): lobbying; consultation responses; media campaigns; petitions; demonstrations/direct action. [4]'),
        ('Explain how membership of the European Union affected parliamentary sovereignty.', 'Under the European Communities Act 1972 EU law took priority over conflicting UK law, so courts could disapply an Act (Factortame); this ended when the UK left the EU under the European Union (Withdrawal) Act 2018.', '1 mark: EU law had supremacy; 1 mark: Factortame – Act disapplied; 1 mark: sovereignty restored on leaving the EU (2020). [3]'),
        ('Explain two reasons why many Law Commission reports have not been implemented.', 'Lack of parliamentary time, as government Bills take priority; and lack of political will or interest, especially for technical reforms that do not win votes (e.g. the reform of non-fatal offences).', '2 × (1 mark reason, 1 mark development): parliamentary time; political will; cost; controversy. [4]')],
  cmps=[('an insider pressure group', 'an outsider pressure group', ['insider groups are consulted by government while outsider groups are not', 'insider groups use lobbying and consultation, outsider groups rely on publicity and direct action', 'insider groups are usually seen as having expertise, outsider groups may be seen as radical']),
        ('the Law Commission', 'a pressure group', ['the Law Commission is an independent official body while a pressure group is a private organisation', 'the Law Commission researches and drafts proposals across the law, a pressure group promotes a single interest or cause', 'Law Commission proposals are based on expert research and consultation, pressure groups may present a one-sided view'])],
  scen=[dict(facts='{A} was injured when {harm}. {A} set up a campaign group in {city} to change the law and wants to put pressure on Parliament.',
             slots={'harm': ['a dog of a banned breed attacked {A} in a park', 'a driver using a mobile phone crashed into {A}\'s car', 'an uninsured e-scooter rider hit {A} on a pavement', 'a drink was spiked at a nightclub']},
             issue='the influence of pressure groups on Parliament', wrong=['the role of the Law Commission', 'the doctrine of judicial precedent', 'the controls on delegated legislation'],
             iq='Which influence on Parliament is most relevant to {A}\'s plan?',
             ask='Explain how {A}\'s group could try to influence Parliament and assess how successful it is likely to be.',
             law=['pressure groups influence Parliament through lobbying, petitions (100 000 signatures for a debate), media campaigns and demonstrations', 'insider groups are consulted by government; outsider groups rely on publicity', 'successful campaigns include the Snowdrop campaign leading to the Firearms (Amendment) Act 1997', 'pressure groups cannot make law themselves; only Parliament can'],
             apply=['the group could use the media and an e-petition to publicise cases like {A}\'s', 'it could lobby local MPs and find an MP to introduce a Private Members\' Bill', 'as a new outsider group it has limited access to ministers'],
             concl='the group may influence Parliament, especially if public opinion is strong, but only Parliament can change the law',
             owrong=['the group can change the law itself by collecting enough signatures', 'the courts must change the law if a pressure group asks them to', 'pressure groups are banned from contacting MPs']),
        dict(facts='{A} claims that a section of the {act}, an Act of Parliament, is invalid because {reason}. {A} asks the High Court to declare the section void.',
             slots={'act': ['Transport Act 2019', 'Finance Act 2021', 'Housing Act 2018', 'Fisheries Act 2020'],
                    'reason': [('MPs were misled about its effect during the debate', 'Pickin v British Railways Board (1974)'), ('it conflicts with an international treaty the country has signed', 'Cheney v Conn (1968)'), ('it contradicts an earlier Act which said it could never be changed', 'Ellen Street Estates v Minister of Health (1934)')]},
             issue='parliamentary sovereignty and the inability of courts to challenge an Act of Parliament', wrong=['the ultra vires rule for delegated legislation', 'the mischief rule of statutory interpretation', 'the Practice Statement 1966'],
             ask='Advise {A} whether the court can declare the section void.',
             law=['parliamentary sovereignty: no court can override or set aside an Act of Parliament (Dicey)', 'in {reason_1} the courts refused to question the validity of an Act', 'Parliament cannot bind its successors and a later Act impliedly repeals an inconsistent earlier one', 'under the Human Rights Act 1998 the court may only make a declaration of incompatibility'],
             apply=['{A}\'s argument that {reason} does not allow the court to strike down the {act}', 'the court must apply the Act as it stands'],
             concl='the court cannot declare the section void; {A} would have to persuade Parliament to change the law',
             owrong=['the court must declare the section void', 'the court can suspend the Act until Parliament votes again', 'the Act is invalid unless approved by the Supreme Court'])],
  ev=[('"Parliament is still sovereign." Discuss the extent to which this statement is accurate.', ['courts cannot set aside Acts (Pickin, Cheney v Conn)', 'the UK left the EU, ending the supremacy of EU law', 'declarations of incompatibility under the HRA do not affect an Act\'s validity'],
       ['while in the EU, Factortame allowed courts to disapply Acts', 'political reality means Parliament usually responds to declarations of incompatibility', 'devolution and obiter remarks in Jackson suggest some practical limits'],
       ['Pickin v British Railways Board (1974)', 'Factortame (No 2) (1991)', 'R (Jackson) v Attorney-General (2005)', 'Bellinger v Bellinger (2003)', 'Human Rights Act 1998 ss3-4'], 'legally Parliament remains sovereign, though political and practical limits exist'),
      ('Evaluate the influence of pressure groups and the Law Commission on Parliament.', ['pressure groups raise awareness and represent minority interests', 'the Law Commission provides expert, researched proposals (e.g. Fraud Act 2006)', 'both can prompt Parliament to act on neglected issues'],
       ['pressure groups may be undemocratic and represent narrow interests; wealthy groups have more influence', 'many Law Commission reports are never implemented, e.g. reform of non-fatal offences', 'Parliament is not obliged to follow either'],
       ['Snowdrop campaign and the Firearms (Amendment) Act 1997', 'Law Commissions Act 1965', 'Fraud Act 2006', 'Law Commission report on offences against the person (2015)'], 'both have real influence but Parliament retains the final decision and implementation is uneven')])

T(1, 'Delegated legislation: statutory instruments, by-laws and Orders in Council', area='delegated legislation',
  defs=[('delegated legislation', 'Law made by a person or body other than Parliament, using authority given to it by Parliament in an enabling Act.'),
        ('enabling Act', 'An Act of Parliament (also called a parent Act) that gives a government minister or other body power to make delegated legislation within stated limits.'),
        ('statutory instrument', 'A form of delegated legislation made by a government minister or department under powers in an enabling Act.'),
        ('by-law', 'A form of delegated legislation made by a local authority or public corporation, dealing with local or specialist matters and usually needing approval by a minister.'),
        ('Order in Council', 'Delegated legislation made by the King and the Privy Council, used for example in emergencies, to bring Acts into force or to transfer responsibilities between government departments.')],
  mcqs=[('Which type of delegated legislation is made by government ministers and their departments?', 'Statutory instruments', ['By-laws', 'Orders in Council', 'Private Bills'], 'Ministers make statutory instruments under powers in enabling Acts.'),
        ('Which body makes by-laws?', 'Local authorities and public corporations', ['The Privy Council', 'Government ministers only', 'The Supreme Court'], 'By-laws are made by local authorities (e.g. city councils) and public corporations such as railway operators.'),
        ('Which Act allows Orders in Council to be made in a national emergency when Parliament cannot act quickly?', 'Civil Contingencies Act 2004', ['Human Rights Act 1998', 'Constitutional Reform Act 2005', 'Legislative and Regulatory Reform Act 2006'], 'The Civil Contingencies Act 2004 permits emergency regulations by Order in Council.'),
        ('Approximately how many statutory instruments are made in the UK each year?', 'About 3 000', ['About 30', 'About 300 000', 'About 50'], 'Around 3 000 SIs are made each year, far more than the number of Acts.'),
        ('The annual rates of the national minimum wage are set by statutory instrument. Under which enabling Act are they made?', 'National Minimum Wage Act 1998', ['Employment Rights Act 1996', 'Equality Act 2010', 'Consumer Rights Act 2015'], 'The National Minimum Wage Act 1998 empowers the minister to set the rates by regulations.')],
  ars=[('Delegated legislation can be made quickly to deal with emergencies.', 'Delegated legislation does not have to go through the full parliamentary process for a Bill.', 'A'),
       ('By-laws are made by government ministers.', 'By-laws deal with matters of local concern.', 'D'),
       ('Delegated legislation allows rules to be made by people with technical expertise.', 'Parliament may not have the specialist knowledge needed for detailed technical rules.', 'A')],
  exps=[('Explain two reasons why Parliament delegates law-making power.', 'Parliament lacks time to pass all the detailed rules needed; and ministers, departments and local councils have the technical expertise and local knowledge required.', '2 × (1 mark reason, 1 mark explanation): lack of parliamentary time; expertise; local knowledge; speed/flexibility in emergencies; easy to amend. [4]'),
        ('Explain why delegated legislation is sometimes criticised as undemocratic.', 'It is made by unelected civil servants or ministers rather than elected MPs debating it, and much of it receives little or no scrutiny by Parliament.', '1 mark: made by unelected people/not debated; 1 mark: limited parliamentary scrutiny. [2]'),
        ('Explain what is meant by sub-delegation and why it is a problem.', 'Sub-delegation occurs when the power to make law is passed further down, e.g. from a minister to civil servants; it moves law-making even further from elected representatives.', '1 mark: definition – power passed on to others; 1 mark: further from democratic control. [2]'),
        ('Explain the role of an enabling Act in the creation of delegated legislation.', 'The enabling Act gives the power to make delegated legislation, states who may make it and sets the limits and procedures; anything outside those limits is ultra vires.', '1 mark: gives the power; 1 mark: sets limits/procedure; 1 mark: link to ultra vires. [3]')],
  cmps=[('a statutory instrument', 'a by-law', ['an SI is made by a government minister while a by-law is made by a local authority or public corporation', 'an SI usually applies nationally while a by-law applies to a local area', 'by-laws usually need confirmation by a minister']),
        ('an Order in Council', 'a statutory instrument made by a minister', ['an Order in Council is made by the King and Privy Council, an SI by a minister', 'Orders in Council are often used in emergencies or to transfer powers, SIs for detailed regulations within a department\'s area'])],
  scen=[dict(facts='The {act} gives the Secretary of State power to make regulations about {topic}. {A}, a civil servant, has been asked to {task}.',
             slots={'act': ['Road Traffic Act (fictional) 2020', 'Food Safety Act (fictional) 2019', 'Health and Safety Act (fictional) 2021'],
                    'topic': ['technical safety standards', 'licensing fees', 'the details of inspection procedures'],
                    'task': ['update the rules every year as technology changes', 'set new fee levels quickly', 'add detailed technical requirements']},
             issue='the use of a statutory instrument as delegated legislation', wrong=['a by-law made by a local authority', 'a Private Members\' Bill', 'an Order in Council made in an emergency'],
             iq='Which form of law-making is most appropriate?',
             ask='Explain which form of delegated legislation should be used and why it is suitable.',
             law=['the enabling Act gives ministers power to make statutory instruments', 'SIs are used for detailed and technical rules and can be amended quickly', 'SIs are subject to the affirmative or negative resolution procedure and scrutiny by the Joint Committee on Statutory Instruments'],
             apply=['the rules on {topic} are technical and need frequent change, so an SI is appropriate', 'the minister\'s department has the necessary expertise', 'the SI must stay within the limits of the {act}'],
             concl='a statutory instrument made by the Secretary of State is the appropriate method',
             owrong=['a new Act of Parliament is required every time the rules change', 'the local council should make a by-law', 'the Supreme Court should set the rules']),
        dict(facts='{city} City Council is concerned about {problem} in its town centre and parks. Councillor {A} wants to introduce a rule to {rule}.',
             slots={'problem': ['anti-social drinking', 'dangerous skateboarding', 'dog fouling', 'noise from street music late at night'],
                    'rule': ['ban this in specified areas', 'make it an offence punishable by a fine', 'restrict it to certain hours']},
             issue='the making of by-laws by a local authority', wrong=['the making of statutory instruments by a minister', 'Orders in Council', 'the Parliament Acts procedure'],
             iq='Which form of law-making is most appropriate for the council?',
             ask='Explain how the council could make this rule and the advantages of doing so.',
             law=['local authorities can make by-laws for their area under powers in enabling Acts (e.g. Local Government Act 1972)', 'by-laws usually need confirmation by the relevant minister', 'by-laws can be challenged in the courts if unreasonable (Strickland v Hayes BC)'],
             apply=['{problem} is a local issue, so local knowledge makes the council suitable', 'the by-law should be limited to the problem areas to avoid being unreasonable'],
             concl='the council can make a by-law about {problem}, subject to ministerial confirmation and judicial review',
             owrong=['the council must ask Parliament to pass an Act', 'the council can make any rule it wishes without limits', 'only the Privy Council can make the rule']),
        dict(facts='A national emergency caused by {event} has hit the country. Parliament is not sitting and urgent rules are needed to {need}. {A}, a government lawyer, is asked how this can be done.',
             slots={'event': ['severe flooding', 'a pandemic', 'a nationwide power failure', 'a major earthquake'],
                    'need': ['control movement into affected areas', 'requisition buildings for emergency shelter', 'ration fuel supplies']},
             issue='Orders in Council in an emergency under the Civil Contingencies Act 2004', wrong=['a Private Members\' Bill', 'a by-law', 'a Green Paper'],
             ask='Advise {A} on the most suitable form of law-making and any safeguards.',
             law=['Orders in Council are made by the King and Privy Council', 'the Civil Contingencies Act 2004 allows emergency regulations when there is not time to pass an Act', 'emergency regulations must be laid before Parliament and lapse after 30 days unless approved'],
             apply=['the emergency caused by {event} creates an urgent need that the slow Bill procedure cannot meet', 'safeguards ensure Parliament can still scrutinise the regulations'],
             concl='an Order in Council under the Civil Contingencies Act 2004 is the appropriate method, subject to later parliamentary approval',
             owrong=['nothing can be done until Parliament sits again', 'the police can make the rules themselves', 'the courts must create the rules through precedent'])],
  ev=[('"Delegated legislation is a necessary part of law-making." Discuss.', ['saves parliamentary time', 'uses expertise and local knowledge', 'can be made quickly in emergencies and easily amended', 'allows consultation with experts'],
       ['undemocratic: made by unelected people', 'sub-delegation', 'large volume with little publicity, so people may not know the law', 'parliamentary scrutiny is limited, especially for the negative resolution procedure'],
       ['Civil Contingencies Act 2004', 'National Minimum Wage Act 1998', 'Aylesbury Mushrooms (1972)', 'Strickland v Hayes BC (1896)'], 'it is necessary in a modern state, provided effective controls are in place'),
      ('Evaluate the advantages and disadvantages of the different types of delegated legislation.', ['SIs allow technical detail and quick amendment', 'by-laws use local knowledge and are made by elected councillors', 'Orders in Council deal with emergencies'],
       ['SIs are made by unelected civil servants', 'by-laws may be unreasonable and are little known', 'Orders in Council give the executive wide power with little scrutiny'],
       ['Civil Contingencies Act 2004', 'Strickland v Hayes BC (1896)', 'R (Public Law Project) v Lord Chancellor (2016)'], 'each type serves a useful purpose but all depend on controls to prevent misuse')])

T(1, 'Controls on delegated legislation: parliamentary and judicial (ultra vires)', area='the control of delegated legislation',
  defs=[('ultra vires', 'Latin for "beyond the powers": delegated legislation that goes beyond the powers given by the enabling Act, or is made without following the required procedure, can be declared void.'),
        ('procedural ultra vires', 'Where the correct procedure set out in the enabling Act, such as consultation, has not been followed when making delegated legislation.'),
        ('substantive ultra vires', 'Where the content of delegated legislation goes beyond what Parliament authorised in the enabling Act.'),
        ('affirmative resolution procedure', 'A procedure under which a statutory instrument must be approved by a vote of one or both Houses of Parliament before it becomes law.'),
        ('negative resolution procedure', 'A procedure under which a statutory instrument becomes law unless either House passes a motion to annul it, usually within 40 days.'),
        ('judicial review', 'The process by which the High Court (Administrative Court) reviews the lawfulness of decisions and delegated legislation made by public bodies.')],
  mcqs=[('Which committee reviews all statutory instruments and can draw the attention of Parliament to any that need special consideration?', 'The Joint Committee on Statutory Instruments', ['The Public Accounts Committee', 'The Judicial Appointments Commission', 'The Law Commission'], 'The Joint Committee on SIs (Scrutiny Committee) reviews technical aspects but cannot amend SIs.'),
        ('Which court hears applications for judicial review of delegated legislation?', 'The Administrative Court of the King\'s Bench Division of the High Court', ['The magistrates\' court', 'The Crown Court', 'The county court'], 'Judicial review is heard in the Administrative Court (KBD).'),
        ('Under the negative resolution procedure, a statutory instrument:', 'becomes law unless it is annulled by a vote within a fixed period (usually 40 days)', ['must be approved by a vote before it becomes law', 'is debated and amended line by line', 'needs Royal Assent before it is valid'], 'Most SIs use the negative procedure, which gives weak scrutiny.'),
        ('A by-law is struck down because it is so unreasonable that no reasonable authority could have made it. Which case gives the test of unreasonableness?', 'Associated Provincial Picture Houses v Wednesbury Corporation (1948)', ['Pepper v Hart (1993)', 'Donoghue v Stevenson (1932)', 'Smith v Hughes (1960)'], 'Wednesbury unreasonableness: so unreasonable that no reasonable authority could have come to it.')],
  cases=[('Agricultural, Horticultural and Forestry Industry Training Board v Aylesbury Mushrooms Ltd (1972)', 'the minister failed to consult the Mushroom Growers\' Association before making an order, as the enabling Act required', 'failure to follow a required consultation procedure makes delegated legislation procedurally ultra vires and invalid against those not consulted'),
         ('R v Home Secretary, ex p Fire Brigades Union (1995)', 'the Home Secretary introduced a tariff scheme of criminal injuries compensation instead of bringing the statutory scheme into force', 'a minister who uses delegated or prerogative powers in a way that frustrates the will of Parliament acts unlawfully (substantive ultra vires)'),
         ('Strickland v Hayes Borough Council (1896)', 'a by-law prohibited singing or reciting obscene songs in any public or private place', 'a by-law that is unreasonably wide can be declared void'),
         ('Associated Provincial Picture Houses v Wednesbury Corporation (1948)', 'a council allowed a cinema to open on Sundays only if no children under 15 were admitted', 'delegated decisions are unlawful only if so unreasonable that no reasonable authority could have made them'),
         ('R (Public Law Project) v Lord Chancellor (2016)', 'regulations introduced a residence test for civil legal aid', 'delegated legislation that goes beyond the purpose and scope of the enabling Act is substantively ultra vires'),
         ('R v Secretary of State for Education, ex p National Union of Teachers (2000)', 'teachers were given only four days to respond to consultation on new pay rules', 'consultation that is inadequate in time or substance makes delegated legislation procedurally ultra vires')],
  ars=[('Delegated legislation can be challenged in the courts, whereas an Act of Parliament cannot.', 'Delegated legislation is valid only if it is within the powers granted by the enabling Act.', 'A'),
       ('The Joint Committee on Statutory Instruments can amend a statutory instrument.', 'The Joint Committee on Statutory Instruments reviews all SIs.', 'D'),
       ('Most statutory instruments receive little parliamentary scrutiny.', 'Most statutory instruments are made under the negative resolution procedure.', 'A')],
  exps=[('Explain the difference between procedural and substantive ultra vires.', 'Procedural ultra vires is failure to follow the procedure required by the enabling Act, e.g. consultation (Aylesbury Mushrooms); substantive ultra vires is where the content goes beyond the powers given (Fire Brigades Union).', '1 mark each correct explanation; 1 mark each case example. [4]'),
        ('Explain two parliamentary controls over delegated legislation.', 'The affirmative resolution procedure requires a vote of approval; the negative resolution procedure allows annulment within 40 days; the Joint Committee on Statutory Instruments scrutinises all SIs; the enabling Act itself sets limits.', '2 × (1 mark control, 1 mark explanation). [4]'),
        ('Explain why judicial control of delegated legislation is limited.', 'The courts can act only if someone brings a challenge, which is costly and must be brought quickly; they can only check legality, not the merits; and if the enabling Act gives very wide powers there is little to be ultra vires.', '1 mark per valid limitation, up to 3. [3]'),
        ('Explain why the courts consider whether a by-law is unreasonable.', 'Parliament is presumed not to have authorised unreasonable rules, so a by-law that is so unreasonable that no reasonable authority could make it (Wednesbury) or is too wide (Strickland v Hayes) will be declared void.', '1 mark: presumption Parliament did not intend unreasonable rules; 1 mark: Wednesbury/Strickland. [2]')],
  cmps=[('the affirmative resolution procedure', 'the negative resolution procedure', ['affirmative requires a positive vote of approval, negative becomes law unless annulled', 'affirmative gives more scrutiny and is used for important SIs, negative is used for most SIs', 'under negative resolution an SI can take effect without any debate']),
        ('parliamentary control', 'judicial control', ['parliamentary control happens when SIs are made, judicial control only after a legal challenge', 'Parliament can consider the merits, the courts only legality (ultra vires)', 'judicial control depends on an individual bringing a case'])],
  scen=[dict(facts='The {act} requires the minister to consult "organisations representing {group}" before making regulations. Minister {A} made regulations about {topic} without consulting the {org}, which represents {group}.',
             slots={'act': ['Farming Standards Act (fictional) 2018', 'Fisheries Management Act (fictional) 2017', 'Taxi Licensing Act (fictional) 2016'],
                    'group': ['farmers', 'small fishing businesses', 'taxi drivers'], 'topic': ['training levies', 'licence fees', 'safety inspections'],
                    'org': ['National Growers\' Union', 'Small Operators Association', 'Independent Workers\' Federation']},
             issue='procedural ultra vires', wrong=['substantive ultra vires', 'Wednesbury unreasonableness only', 'implied repeal'],
             ask='Advise the {org} whether the regulations can be challenged.',
             law=['delegated legislation must follow the procedure in the enabling Act', 'failure to consult as required is procedural ultra vires (Aylesbury Mushrooms 1972)', 'consultation must be genuine and allow adequate time (ex p NUT 2000)', 'the challenge is by judicial review in the Administrative Court'],
             apply=['the {act} required consultation with bodies representing {group}', 'the {org} was not consulted, so the procedure was not followed', 'as in Aylesbury Mushrooms the regulations may be invalid at least against the {org}'],
             concl='the regulations are likely to be held procedurally ultra vires and invalid in relation to the {org}',
             owrong=['the regulations are valid because the minister has unlimited power', 'the challenge must be made to the House of Lords', 'the regulations are valid because they were approved by the Joint Committee']),
        dict(facts='The {act} allows the minister to make rules "about the safety of passengers on buses". Minister {A} made a statutory instrument that {rule}.',
             slots={'act': ['Public Transport Act (fictional) 2015', 'Bus Services Act (fictional) 2019'],
                    'rule': ['bans eating on all trains and ferries as well as buses', 'imposes a new tax on bus companies', 'requires bus passengers to show identity cards to the police']},
             issue='substantive ultra vires', wrong=['procedural ultra vires', 'the negative resolution procedure', 'the mischief rule'],
             ask='Advise whether the statutory instrument can be challenged in the courts.',
             law=['delegated legislation is void if it goes beyond the powers given by the enabling Act (substantive ultra vires)', 'R v Home Secretary ex p Fire Brigades Union (1995); R (Public Law Project) v Lord Chancellor (2016)', 'courts presume that Parliament did not intend to authorise taxation or interference with rights without clear words'],
             apply=['the power is limited to the safety of bus passengers', 'a rule that {rule} goes beyond that purpose', 'the court would declare the SI void to the extent it exceeds the power'],
             concl='the statutory instrument is likely to be declared substantively ultra vires and void',
             owrong=['the SI is valid because it was made by a minister', 'the SI can only be challenged by an Act of Parliament', 'the SI is valid because the negative resolution procedure was used']),
        dict(facts='{city} Council made a by-law making it an offence for {rule}. {A} was fined under the by-law for {act}.',
             slots={'rule': [('any group of more than two people to meet in any place in the city at any time', 'groups'), ('anyone to play music audible from outside any building, including private homes, at any time', 'music'), ('any person to whistle in any public or private place', 'whistling')],
                    'act': ['chatting with two friends in a private garden', 'doing so inside a private house', 'doing so on private property late at night']},
             issue='judicial control of an unreasonable by-law', wrong=['procedural ultra vires', 'the negative resolution procedure', 'parliamentary sovereignty'],
             ask='Advise {A} whether the by-law can be challenged.',
             law=['a by-law can be challenged by judicial review or as a defence if it is ultra vires', 'a by-law that is unreasonably wide is void (Strickland v Hayes BC 1896)', 'the test is whether it is so unreasonable that no reasonable authority could have made it (Wednesbury 1948)'],
             apply=['the by-law on {rule_1} applies everywhere and at all times, including private property', 'like the by-law in Strickland it is far wider than needed', 'it is likely to be Wednesbury unreasonable'],
             concl='{A} has a strong argument that the by-law is unreasonable and void, so the fine should be quashed',
             owrong=['{A} has no remedy because by-laws cannot be challenged', '{A} must ask Parliament to repeal the by-law', 'the by-law is valid because the council was elected'])],
  ev=[('Evaluate the effectiveness of the controls over delegated legislation.', ['the affirmative resolution procedure gives real scrutiny for important SIs', 'judicial review can strike down ultra vires legislation (Aylesbury Mushrooms, Fire Brigades Union)', 'consultation with experts improves quality'],
       ['most SIs use the negative procedure and are never debated', 'the Joint Committee cannot amend SIs and its reports are often ignored', 'judicial review depends on a challenge being brought, is costly and only covers legality', 'wide enabling Acts leave little room for ultra vires'],
       ['Aylesbury Mushrooms (1972)', 'ex p Fire Brigades Union (1995)', 'Strickland v Hayes BC (1896)', 'Wednesbury (1948)', 'R (Public Law Project) v Lord Chancellor (2016)'], 'the controls exist but are of limited effectiveness given the volume of delegated legislation')])

# ---- invented statutes for interpretation problems ---------------------------------
STATUTES = [
    dict(act='Public Parks (Safety) Act', sec='it is an offence to bring a vehicle into a public park', word='vehicle',
         mis='the danger and disturbance caused to park users by motor traffic',
         facts=[('rode a child\'s push scooter along a park path', 'guilty, since a scooter is literally a vehicle', 'not guilty, since convicting a child for a toy scooter would be absurd, so a narrower meaning of "vehicle" would be chosen', 'not guilty', 'a toy scooter does not create the danger the Act was aimed at'),
                ('drove an ambulance into the park to reach an injured jogger', 'guilty, since an ambulance is a vehicle', 'not guilty, since it would be absurd and repugnant to convict emergency services for saving life', 'not guilty', 'the Act was not aimed at emergency vehicles helping park users'),
                ('rode a petrol motorbike across the park as a short cut', 'guilty, since a motorbike is a vehicle', 'guilty, since applying the literal meaning causes no absurdity', 'guilty', 'a motorbike is exactly the kind of danger the Act was passed to prevent'),
                ('used an electric wheelchair on the park paths', 'guilty, since an electric wheelchair may literally be a vehicle', 'not guilty, since excluding disabled people from parks would be an absurd result', 'not guilty', 'a wheelchair user is a park user whom the Act was meant to protect')]),
    dict(act='Railway Stations (Conduct) Act', sec='it is an offence to sleep on a railway platform', word='sleep',
         mis='people using platforms as overnight accommodation and obstructing passengers',
         facts=[('dozed off for five minutes on a platform bench while waiting for a delayed train', 'guilty, since the passenger was literally asleep on the platform', 'not guilty, since convicting a waiting passenger who nodded off would be absurd', 'not guilty', 'a passenger briefly dozing is not the mischief of people camping on platforms'),
                ('lay in a sleeping bag on the platform all night intending to sleep but was still awake when arrested', 'not guilty, since the person was not literally asleep', 'guilty, since an acquittal would be absurd, so "sleep" could be read as "settle down to sleep"', 'guilty', 'settling down for the night is exactly the mischief the Act targets')]),
    dict(act='Road Safety (Distraction) Act', sec='it is an offence to use a hand-held mobile telephone while driving', word='mobile telephone',
         mis='accidents caused by drivers being distracted by hand-held devices',
         facts=[('watched a film on a hand-held tablet computer while driving', 'not guilty, since a tablet computer is not literally a mobile telephone', 'not guilty, since the literal meaning is not absurd enough to justify changing the words', 'guilty', 'a hand-held tablet causes the same dangerous distraction the Act was passed to prevent'),
                ('made a call on a hand-held mobile phone while driving on a motorway', 'guilty, since this falls within the plain words', 'guilty, since there is no absurdity', 'guilty', 'this is precisely the mischief')]),
    dict(act='Alcohol (Young Persons) Act', sec='it is an offence to sell alcohol to a person under 18 in a shop', word='in a shop',
         mis='young people obtaining alcohol from retailers',
         facts=[('sold beer to a 16-year-old through a website that delivered to the buyer\'s home', 'not guilty, since the sale did not take place in a shop', 'not guilty, since there is no ambiguity to resolve', 'guilty', 'online sales give under-18s the same access to alcohol that the Act aimed to stop'),
                ('sold vodka over the counter to a 15-year-old in a corner shop', 'guilty, under the plain words', 'guilty, since the literal meaning causes no absurdity', 'guilty', 'this is the very mischief')]),
    dict(act='School Safety Act', sec='it is an offence for any person to have a knife in a school building', word='any person',
         mis='pupils and intruders carrying knives that could be used as weapons',
         facts=[('used a kitchen knife to prepare lunches in the school kitchen as a school cook', 'guilty, since the cook literally had a knife in a school building', 'not guilty, since convicting a cook for preparing food would be absurd', 'not guilty', 'the Act aimed to stop knives being carried as weapons, not used as kitchen tools'),
                ('brought a flick knife to school hidden in a sports bag', 'guilty, under the plain words', 'guilty, since there is no absurdity', 'guilty', 'this is exactly the mischief')]),
]


def si_frame(focus):
    def fr(r):
        st = r.choice(STATUTES)
        f, lit, gold, misout, why = r.choice(st['facts'])
        yr = r.choice(['2014', '2017', '2020', '2023'])
        facts = f'Section 1 of the (fictional) {st["act"]} {yr} provides that "{st["sec"]}". {{A}} {f}.'
        rules = ['literal rule: words are given their plain, ordinary meaning even if the result is absurd (Whiteley v Chappell, LNER v Berriman)',
                 'golden rule: the literal meaning may be modified to avoid an absurd result (R v Allen, narrow approach) or a repugnant one (Re Sigsworth, wide approach)',
                 'mischief rule: the court asks what problem the Act was passed to remedy (Heydon\'s Case; Smith v Hughes)']
        app = [f'literal rule: {{A}} would be {lit}', f'golden rule: {{A}} would be {gold}', f'mischief rule: the mischief was {st["mis"]}; {{A}} would be {misout} because {why}']
        if focus == 'purp':
            rules = [rules[0], 'purposive approach: the court looks for the purpose of Parliament and interprets the words to achieve it (Jones v Tower Boot; R (Quintavalle) v Secretary of State for Health)',
                     'the court may use extrinsic aids such as Hansard (Pepper v Hart) and explanatory notes to identify the purpose']
            app = [f'literal rule: {{A}} would be {lit}', f'purposive approach: the purpose was to prevent {st["mis"]}; {{A}} would be {misout} because {why}']
        opp = 'not guilty' if misout == 'guilty' else 'guilty'
        ask = {'lgm': ['Explain how the literal, golden and mischief rules could be applied to decide whether {A} is guilty.',
                       'Apply the literal rule, the golden rule and the mischief rule to advise whether {A} has committed the offence.'],
               'purp': ['Advise whether {A} is guilty, applying the purposive approach and comparing it with the literal rule.',
                        'Explain how a court using the purposive approach would interpret the section, and advise {A}.'],
               'apply': ['Apply the rules of statutory interpretation to advise whether {A} has committed the offence.',
                         'Using the rules and aids of statutory interpretation, advise whether {A} is guilty under section 1.',
                         'Advise {A}, explaining how different approaches to interpretation could lead to different outcomes.']}[focus]
        return dict(facts=facts, ask=r.choice(ask),
                    issue=f'the meaning of "{st["word"]}" in section 1, to be resolved using the rules of statutory interpretation',
                    wrong=['whether the Act was validly passed by Parliament', 'whether the Act is ultra vires delegated legislation', 'whether the court can declare the Act incompatible with human rights'],
                    iq='Which question will the court have to decide?',
                    law=rules, apply=app,
                    concl=f'the outcome depends on the approach taken; a modern court looking at the purpose of the Act would probably find {{A}} {misout}',
                    owrong=[f'{{A}} must be {opp} whichever approach the court takes', 'the court must refuse to decide because the section is unclear', 'the court must ask Parliament to explain the meaning before deciding'])
    return fr



EJG_LISTS = [('dogs, cats, rabbits or other animals', 'other domestic pets of the same kind',
              [('a pet ferret', 'covered', 'a ferret is a small domestic pet like those listed'), ('a crocodile', 'not covered', 'a crocodile is a wild, dangerous animal, not a domestic pet like those listed'),
               ('a pet hamster', 'covered', 'a hamster is a small domestic pet like those listed')]),
             ('lions, tigers, leopards or other animals', 'other big cats or similar dangerous wild animals',
              [('a pet hamster', 'not covered', 'a hamster is not a dangerous wild animal like those listed'), ('a jaguar', 'covered', 'a jaguar is a big cat like those listed'),
               ('a pet rabbit', 'not covered', 'a rabbit is not of the same kind as the big cats listed')])]


def ejg_frame(r):
    lst, cls, things = r.choice(EJG_LISTS)
    thing, res, why = r.choice(things)
    yr = r.choice(['2016', '2019', '2022'])
    guilty = 'commits the offence' if res == 'covered' else 'does not commit the offence'
    return dict(facts=f'The (fictional) Animal Welfare Act {yr} makes it an offence to keep "{lst}" in a flat without a licence. {{A}} keeps {thing} in a flat in {{city}} without a licence.',
                issue='the ejusdem generis rule of language', wrong=['expressio unius est exclusio alterius', 'the golden rule (wide approach)', 'the presumption against retrospective effect'],
                ask='Explain how the court is likely to interpret "other animals" and whether {A} commits the offence.',
                law=['ejusdem generis: general words after a list of specific words are limited to things of the same kind', 'Powell v Kempton Park Racecourse (1899): "house, office, room or other place" limited to indoor places', 'at least two specific words are needed to form a class (Allen v Emmerson 1944)'],
                apply=[f'the listed words create a class, so "other animals" is likely to mean {cls}', f'{why}', f'so {thing} is probably {res} by the Act'],
                concl=f'applying ejusdem generis, {{A}} probably {guilty}',
                owrong=[f'{{A}} {"does not commit" if res == "covered" else "commits"} the offence because "other animals" must be given its widest literal meaning' if res != 'covered' else f'{{A}} does not commit the offence because only the listed animals are covered', 'the court cannot decide because the Act is ambiguous', 'the Act is void for uncertainty'])


# =====================================================================================
# 2 Statutory interpretation
# =====================================================================================

SI_CASES_LIT = [('Whiteley v Chappell (1868)', 'the defendant pretended to be a dead person in order to vote, and the offence was to impersonate "any person entitled to vote"', 'under the literal rule words are given their plain, ordinary meaning even if the result is absurd: a dead person is not "entitled to vote"'),
                ('Fisher v Bell (1960)', 'a shopkeeper displayed a flick knife in his shop window with a price ticket and was charged with "offering for sale" an offensive weapon', 'the literal (technical legal) meaning of "offer for sale" was applied: goods in a shop window are an invitation to treat, not an offer'),
                ('London and North Eastern Railway v Berriman (1946)', 'a railway worker was killed while oiling points, and compensation was payable only for those "relaying or repairing" the track', 'the literal rule was applied strictly: oiling was maintenance, not relaying or repairing, so the widow received nothing'),
                ('R v Allen (1872)', 'the defendant was charged with bigamy, defined as "whosoever being married shall marry any other person"', 'under the golden rule (narrow approach) "marry" was read as "go through a ceremony of marriage" to avoid an absurd result'),
                ('Adler v George (1964)', 'the defendant obstructed a soldier inside a prohibited place but argued the offence covered only conduct "in the vicinity of" it', 'under the golden rule (narrow approach) "in the vicinity of" was read to include "in" to avoid absurdity'),
                ('Re Sigsworth (1935)', 'a son murdered his mother and, as her next of kin, would have inherited her estate under the Administration of Estates Act 1925', 'under the golden rule (wide approach) the court will not apply words literally where this would be repugnant, so a murderer cannot inherit from his victim'),
                ('Smith v Hughes (1960)', 'prostitutes attracted the attention of men in the street by tapping on windows and calling from balconies, and the offence was to solicit "in a street"', 'under the mischief rule the court considered the problem the Act aimed to remedy (people being solicited in the street), so soliciting from balconies was covered'),
                ('Royal College of Nursing v DHSS (1981)', 'nurses carried out part of a medically induced abortion, but the Abortion Act 1967 required termination "by a registered medical practitioner"', 'applying the mischief rule, the House of Lords held the Act aimed to end unsafe back-street abortions, so procedures carried out by nurses under a doctor\'s supervision were lawful'),
                ('Elliott v Grey (1960)', 'an uninsured car was parked on a road with its wheels off the ground and battery removed, and the offence was to "use" an uninsured car on a road', 'under the mischief rule the car was "used" because it was a hazard that the insurance requirement was intended to cover'),
                ('Corkery v Carpenter (1951)', 'a man was drunk in charge of a bicycle, and the Licensing Act 1872 made it an offence to be drunk in charge of a "carriage"', 'under the mischief rule a bicycle was held to be a "carriage" because the Act aimed to prevent drunken people in charge of any form of transport'),
                ('Heydon\'s Case (1584)', 'the court set out how to interpret a statute that was passed to remedy a defect in the common law', 'the mischief rule: consider the common law before the Act, the mischief or defect, the remedy Parliament chose and the reason for it')]

T(2, 'The literal, golden and mischief rules', area='statutory interpretation',
  defs=[('literal rule', 'A rule of statutory interpretation under which words in an Act are given their plain, ordinary, dictionary meaning, even if the result is absurd.'),
        ('golden rule', 'A rule of statutory interpretation that allows the court to depart from the literal meaning of words to avoid an absurd or repugnant result, using a narrow or a wide approach.'),
        ('mischief rule', 'A rule of statutory interpretation, from Heydon\'s Case (1584), under which the court looks for the problem (mischief) the Act was passed to remedy and interprets the words to suppress it.'),
        ('statutory interpretation', 'The process by which judges decide the meaning of words in an Act of Parliament when applying it to the facts of a case.')],
  mcqs=[('Which rule of interpretation was applied in Whiteley v Chappell (1868)?', 'The literal rule', ['The golden rule', 'The mischief rule', 'The purposive approach'], 'A dead person was not "entitled to vote", so the defendant was not guilty – an absurd result from the literal rule.'),
        ('In which case did the court use the golden rule to prevent a murderer from inheriting from his victim?', 'Re Sigsworth (1935)', ['R v Allen (1872)', 'Smith v Hughes (1960)', 'Fisher v Bell (1960)'], 'Re Sigsworth is an example of the wide approach to the golden rule.'),
        ('From which case does the mischief rule come?', 'Heydon\'s Case (1584)', ['Pepper v Hart (1993)', 'Re Sigsworth (1935)', 'Magor and St Mellons RDC v Newport Corporation (1950)'], 'Heydon\'s Case set out the four questions of the mischief rule.'),
        ('Which statement describes the narrow approach to the golden rule?', 'Where a word has more than one meaning, the court chooses the one that avoids an absurd result', ['The court ignores the words and gives effect to Parliament\'s general purpose', 'The court always applies the dictionary meaning', 'The court looks at Hansard to find what the minister meant'], 'R v Allen and Adler v George illustrate the narrow approach.')],
  cases=SI_CASES_LIT, scen=[si_frame('lgm')] * 3,
  ars=[('The literal rule respects parliamentary sovereignty.', 'Under the literal rule judges apply the words that Parliament actually chose rather than their own view of what it meant.', 'A'),
       ('The golden rule can be used whenever a judge dislikes the literal meaning.', 'The golden rule allows a departure from the literal meaning to avoid an absurd or repugnant result.', 'D'),
       ('In Smith v Hughes (1960) the defendants were convicted although they were not physically in the street.', 'The mischief rule allows the court to consider what problem the Act was passed to remedy.', 'A')],
  exps=[('Explain one advantage and one disadvantage of the literal rule.', 'Advantage: it respects parliamentary sovereignty and makes the law certain because judges apply Parliament\'s words. Disadvantage: it can lead to absurd or unjust results, as in Whiteley v Chappell or LNER v Berriman.', '1 mark advantage + 1 mark development; 1 mark disadvantage + 1 mark example. [4]'),
        ('Explain the difference between the narrow and wide approaches to the golden rule.', 'The narrow approach chooses between possible meanings of a word to avoid absurdity (R v Allen); the wide approach is used where there is only one meaning but applying it would be repugnant, so the court modifies it (Re Sigsworth).', '1 mark narrow + example; 1 mark wide + example. [2]'),
        ('Describe the four questions set out in Heydon\'s Case.', 'What was the common law before the Act? What was the mischief or defect the common law did not provide for? What remedy did Parliament resolve to provide? What was the true reason for the remedy?', '1 mark per question. [4]'),
        ('Explain why the mischief rule is said to promote justice.', 'It allows judges to look at why the Act was passed and to give effect to Parliament\'s intention to remedy a problem, so the law is applied sensibly and loopholes are closed, as in Smith v Hughes.', '1 mark: looks at purpose/Parliament\'s intention; 1 mark: avoids loopholes/unjust results with example. [2]')],
  cmps=[('the literal rule', 'the mischief rule', ['the literal rule focuses on the words while the mischief rule focuses on the problem the Act was meant to cure', 'the literal rule may produce absurd results while the mischief rule avoids loopholes', 'the mischief rule gives judges more discretion, the literal rule less']),
        ('the golden rule', 'the literal rule', ['the golden rule allows departure from the literal meaning to avoid absurdity while the literal rule does not', 'the golden rule is a modification of the literal rule used only when absurdity results'])],
  ev=[('Evaluate the extent to which the literal, golden and mischief rules allow judges to achieve justice.', ['the golden rule avoids absurd results (Re Sigsworth)', 'the mischief rule closes loopholes and promotes Parliament\'s intention (Smith v Hughes, Royal College of Nursing v DHSS)', 'the literal rule respects democracy and gives certainty'],
       ['the literal rule can cause injustice (LNER v Berriman, Whiteley v Chappell)', 'the golden rule is limited and there is no clear test of absurdity', 'the mischief rule gives judges wide discretion and may allow them to make law', 'there is no hierarchy, so judges can choose the rule that gives the result they prefer'],
       ['Whiteley v Chappell (1868)', 'LNER v Berriman (1946)', 'Re Sigsworth (1935)', 'Smith v Hughes (1960)', 'Royal College of Nursing v DHSS (1981)'], 'the golden and mischief rules allow more just outcomes but at the cost of certainty and democratic legitimacy'),
      ('"The literal rule is the best rule of statutory interpretation." Discuss.', ['it respects parliamentary sovereignty', 'it promotes certainty and predictability', 'it encourages precise drafting'],
       ['words can have several meanings', 'it can produce absurd or unjust results', 'it assumes perfect drafting', 'the Law Commission (1969) criticised it'],
       ['Fisher v Bell (1960)', 'Whiteley v Chappell (1868)', 'LNER v Berriman (1946)', 'R v Allen (1872)'], 'the literal rule is a sensible starting point but should not be applied where it defeats Parliament\'s purpose')])

T(2, 'The purposive approach', area='the purposive approach',
  defs=[('purposive approach', 'An approach to statutory interpretation in which the court looks for the purpose or intention of Parliament in passing the Act and interprets the words to give effect to it.'),
        ('Hansard', 'The official report of debates in Parliament, which may be consulted under Pepper v Hart (1993) where a statute is ambiguous.'),
        ('section 3 of the Human Rights Act 1998', 'The duty on courts to read and give effect to legislation in a way which is compatible with Convention rights, so far as it is possible to do so.')],
  mcqs=[('Which judge was criticised for "a naked usurpation of the legislative function" when suggesting that judges should fill in the gaps in legislation?', 'Lord Denning', ['Lord Simonds', 'Lord Diplock', 'Lord Reid'], 'In Magor and St Mellons RDC v Newport Corporation (1950) Lord Simonds criticised Lord Denning\'s gap-filling approach.'),
        ('In R (Quintavalle) v Secretary of State for Health (2003), the House of Lords used the purposive approach to decide that:', 'embryos created by cell nuclear replacement were covered by the Human Fertilisation and Embryology Act 1990', ['a bicycle was a carriage', 'a dead person was not entitled to vote', 'goods in a shop window are an invitation to treat'], 'Parliament\'s purpose was to regulate the creation of embryos, so cloned embryos were included.'),
        ('Which approach to interpretation is used most widely in the European Court of Justice and many civil law systems?', 'The purposive approach', ['The literal rule', 'The golden rule (narrow approach)', 'The ejusdem generis rule'], 'European courts use a broad purposive approach, which influenced English courts.'),
        ('Under section 3 of the Human Rights Act 1998, courts must:', 'read legislation compatibly with Convention rights so far as it is possible to do so', ['strike down Acts that breach Convention rights', 'apply only the literal meaning of Acts', 'refer all human rights cases to the European Court of Human Rights'], 'Section 3 requires compatible interpretation where possible, e.g. Ghaidan v Godin-Mendoza (2004).')],
  cases=[('Jones v Tower Boot Co Ltd (1997)', 'a young worker suffered serious racial harassment from colleagues and the employer argued the acts were not done "in the course of employment"', 'using the purposive approach, "in the course of employment" in the Race Relations Act 1976 was given a broad meaning so that the Act\'s purpose of protecting employees was achieved'),
         ('R (Quintavalle) v Secretary of State for Health (2003)', 'a pro-life group argued that embryos created by cell nuclear replacement (cloning) were not covered by the Human Fertilisation and Embryology Act 1990', 'the House of Lords used the purposive approach: Parliament intended to regulate the creation of all live human embryos'),
         ('Magor and St Mellons RDC v Newport Corporation (1950)', 'Lord Denning in the Court of Appeal suggested judges should "fill in the gaps" to find the intention of Parliament', 'the House of Lords rejected gap-filling as a "naked usurpation of the legislative function" (Lord Simonds)'),
         ('Ghaidan v Godin-Mendoza (2004)', 'a same-sex partner sought to succeed to a tenancy under a provision for a person living with the tenant "as his or her wife or husband"', 'under section 3 Human Rights Act 1998, the words were read to include same-sex partners to make the Act compatible with Convention rights'),
         ('Coltman v Bibby Tankers (1987)', 'a ship sank and the question was whether it was "equipment" under the Employers\' Liability (Defective Equipment) Act 1969', 'applying the purpose of the Act to protect employees, a ship was held to be "equipment"')],
  scen=[si_frame('purp')] * 3,
  ars=[('Judges using the purposive approach may give words a meaning that differs from their literal meaning.', 'The purposive approach seeks to give effect to the intention of Parliament.', 'A'),
       ('The purposive approach was developed only in the 21st century.', 'European influence encouraged the use of the purposive approach in English courts.', 'D')],
  exps=[('Explain how the purposive approach differs from the mischief rule.', 'The mischief rule looks only at the defect in the previous law that the Act was meant to cure; the purposive approach looks more broadly at the overall purpose of Parliament, and may go further from the words, influenced by European law.', '1 mark mischief rule – defect in the old law; 1 mark purposive – wider purpose/intention; 1 mark example or European influence. [3]'),
        ('Explain two advantages of the purposive approach.', 'It gives effect to what Parliament intended, so results are sensible and just; and it allows the law to cover new developments Parliament did not foresee, such as cloning in Quintavalle.', '2 × (1 mark advantage, 1 mark development/example). [4]'),
        ('Explain why the purposive approach is criticised.', 'It gives judges too much power to decide what Parliament intended, which may be uncertain, so judges may effectively make law even though they are unelected; it also makes the law less predictable.', '1 mark: judicial law-making/undemocratic; 1 mark: difficulty of finding Parliament\'s intention/uncertainty. [2]')],
  cmps=[('the purposive approach', 'the literal rule', ['the purposive approach looks at Parliament\'s purpose while the literal rule looks only at the words', 'the purposive approach gives judges more discretion', 'the purposive approach can extend an Act to new situations, the literal rule may leave gaps'])],
  ev=[('"The purposive approach allows judges to make law." Discuss.', ['judges decide what Parliament intended, which may involve choice', 'gap-filling was criticised in Magor and St Mellons', 'section 3 HRA allows words to be read in (Ghaidan v Godin-Mendoza)'],
       ['judges are giving effect to Parliament\'s intention, not their own', 'it avoids absurd results and keeps the law up to date (Quintavalle)', 'Parliament can always reverse a decision it disagrees with'],
       ['Magor and St Mellons RDC v Newport Corporation (1950)', 'Jones v Tower Boot (1997)', 'R (Quintavalle) v Secretary of State for Health (2003)', 'Ghaidan v Godin-Mendoza (2004)', 'Pepper v Hart (1993)'], 'the purposive approach involves limited judicial creativity, but within the purpose Parliament set'),
      ('Evaluate the purposive approach as a method of statutory interpretation.', ['flexible and just', 'keeps statutes up to date with technology', 'consistent with European and international approaches'],
       ['uncertain: Parliament\'s purpose may be unclear', 'undemocratic judicial law-making', 'requires use of extrinsic aids that are time-consuming'],
       ['Jones v Tower Boot (1997)', 'Quintavalle (2003)', 'Coltman v Bibby Tankers (1987)', 'Magor and St Mellons (1950)'], 'it is the dominant modern approach and generally produces sensible results, provided judges respect the words used')])

T(2, 'Intrinsic and extrinsic aids and rules of language', area='aids to interpretation',
  defs=[('intrinsic aid', 'An aid to interpretation found within the Act itself, such as the long title, short title, preamble, headings, interpretation section or schedules.'),
        ('extrinsic aid', 'An aid to interpretation found outside the Act, such as dictionaries, Hansard, Law Commission reports, explanatory notes, earlier Acts and international treaties.'),
        ('ejusdem generis', 'A rule of language under which general words that follow a list of specific words are limited to things of the same kind as the specific words.'),
        ('noscitur a sociis', 'A rule of language under which a word is understood in the context of the other words around it.'),
        ('expressio unius est exclusio alterius', 'A rule of language under which the express mention of one thing implies the exclusion of others not mentioned.'),
        ('presumption', 'A starting point the courts assume Parliament intended unless the Act clearly says otherwise, for example that mens rea is required for a crime or that an Act does not apply retrospectively.')],
  mcqs=[('Which case allowed judges to consult Hansard in limited circumstances?', 'Pepper v Hart (1993)', ['Davis v Johnson (1979)', 'Re Sigsworth (1935)', 'Fisher v Bell (1960)'], 'Pepper v Hart: Hansard may be used where the Act is ambiguous, the statement is by a minister or promoter and it is clear.'),
        ('A statute refers to "dogs, cats and other animals". Under the ejusdem generis rule, "other animals" is most likely to include:', 'other domestic pets', ['lions in a zoo', 'all living creatures', 'farm machinery'], 'General words are limited to the same kind (genus) as the specific words – here domestic animals.'),
        ('Which of the following is an intrinsic aid to interpretation?', 'The interpretation section of the Act', ['A Law Commission report', 'Hansard', 'A dictionary'], 'Intrinsic aids are found within the Act itself.'),
        ('In Powell v Kempton Park Racecourse (1899), "house, office, room or other place" was held not to include:', 'an outdoor enclosure', ['a betting office', 'a room in a hotel', 'an indoor betting hall'], 'Applying ejusdem generis, the specific words were all indoor places, so "other place" meant other indoor places.'),
        ('In Tempest v Kilner (1846), which rule of language meant that "goods, wares and merchandise" did not include stocks and shares?', 'Expressio unius est exclusio alterius', ['Ejusdem generis', 'Noscitur a sociis', 'The golden rule'], 'Express mention of goods, wares and merchandise excluded other types of property.')],
  cases=[('Pepper v Hart (1993)', 'teachers at a private school disputed how a tax on their reduced school fees should be calculated, and a minister had explained the meaning in Parliament', 'Hansard may be consulted where the legislation is ambiguous, the statement was made by a minister or promoter of the Bill and the statement is clear'),
         ('Powell v Kempton Park Racecourse (1899)', 'betting took place in an outdoor enclosure and the Act referred to "house, office, room or other place"', 'under the ejusdem generis rule, general words following specific words are limited to the same kind, so "other place" meant indoor places'),
         ('Allen v Emmerson (1944)', 'the phrase "theatres and other places of amusement" was considered in relation to a funfair', 'ejusdem generis needs at least two specific words to create a class; with only one, the general words were given their wide meaning'),
         ('Inland Revenue Commissioners v Frere (1965)', 'an Act referred to "interest, annuities or other annual interest"', 'under noscitur a sociis, "interest" was read in context to mean only annual interest'),
         ('Muir v Keay (1875)', 'a café opened at night was said not to be a "house for public refreshment, resort and entertainment" requiring a licence', 'under noscitur a sociis, "entertainment" was read with refreshment, so it meant refreshment rooms such as cafés, not musical entertainment'),
         ('Tempest v Kilner (1846)', 'the Statute of Frauds 1677 required contracts for "goods, wares and merchandise" over a value to be in writing, and the contract was for stocks and shares', 'under expressio unius est exclusio alterius, the express list excluded stocks and shares'),
         ('Davis v Johnson (1979)', 'the Court of Appeal had looked at Hansard to interpret the Domestic Violence and Matrimonial Proceedings Act 1976', 'the House of Lords reaffirmed the rule (later relaxed in Pepper v Hart) that judges should not consult Hansard')],
  ars=[('Judges can now always refer to Hansard when interpreting an Act.', 'Pepper v Hart (1993) relaxed the rule against using Hansard.', 'D'),
       ('Explanatory notes are an extrinsic aid.', 'Explanatory notes are published separately from the Act and are not part of it.', 'A'),
       ('Ejusdem generis cannot apply to a list with only one specific word.', 'In Allen v Emmerson (1944) "theatres and other places of amusement" was held to include a funfair.', 'B')],
  exps=[('Explain the three conditions set out in Pepper v Hart (1993) for consulting Hansard.', 'The legislation must be ambiguous or obscure or lead to an absurdity; the statement relied on must be by a minister or other promoter of the Bill; and the statement must be clear.', '1 mark per condition. [3]'),
        ('Explain two problems with using Hansard as an aid to interpretation.', 'It is time-consuming and expensive to search, increasing the cost of cases; and statements in debate may be made in the heat of argument and may not reflect what Parliament as a whole intended.', '2 × (1 mark problem, 1 mark explanation). [4]'),
        ('Explain the difference between ejusdem generis and noscitur a sociis.', 'Ejusdem generis limits general words that follow a list of specific words to the same kind (Powell v Kempton Park); noscitur a sociis means a word is read in the context of the words around it (Muir v Keay).', '1 mark each rule explained; 1 mark each example. [4]'),
        ('Explain two presumptions that courts apply when interpreting statutes.', 'That mens rea is required for a criminal offence (Sweet v Parsley); and that an Act does not apply retrospectively; also that Parliament does not intend to change the common law or bind the Crown unless it says so.', '2 × (1 mark presumption, 1 mark explanation). [4]')],
  cmps=[('intrinsic aids', 'extrinsic aids', ['intrinsic aids are found within the Act while extrinsic aids are outside it', 'examples of intrinsic aids are the long title and interpretation section; extrinsic aids include Hansard and dictionaries', 'intrinsic aids are always available, while some extrinsic aids (Hansard) can only be used in limited circumstances'])],
  scen=[ejg_frame,
        dict(facts='{A} is charged under a section of the (fictional) Public Safety Act {yr}, which makes it an offence to "{word}". The meaning of the section is unclear, and during the debate on the Bill the minister made a clear statement about its intended meaning.',
             slots={'yr': ['2015', '2018', '2021'], 'word': ['carry a blade in a public place', 'use a vehicle on a footpath', 'fly a drone near a building']},
             issue='the use of Hansard as an extrinsic aid under Pepper v Hart (1993)', wrong=['the use of the long title as an intrinsic aid', 'the noscitur a sociis rule', 'the mischief rule from Heydon\'s Case'],
             ask='Explain whether the court may look at what the minister said and what other aids it may use.',
             law=['Pepper v Hart (1993): Hansard may be used if the Act is ambiguous, the statement was by a minister or promoter and it is clear', 'other extrinsic aids include explanatory notes, dictionaries and Law Commission reports', 'intrinsic aids include the long title, preamble, headings and interpretation section'],
             apply=['the section is unclear, so the first condition is met', 'the statement was made by the minister and is clear', 'the court may therefore consult Hansard, together with the explanatory notes'],
             concl='all three Pepper v Hart conditions appear to be met, so the court may use Hansard to interpret the section')],
  ev=[('Evaluate the usefulness of extrinsic aids in statutory interpretation.', ['help judges find Parliament\'s intention (Pepper v Hart)', 'Law Commission reports explain the mischief', 'dictionaries help find ordinary meanings'],
       ['Hansard is time-consuming and costly to research', 'ministerial statements may not represent Parliament\'s intention', 'dictionaries give several meanings', 'use of aids may undermine the separation of powers'],
       ['Pepper v Hart (1993)', 'Davis v Johnson (1979)', 'Royal College of Nursing v DHSS (1981)'], 'extrinsic aids are useful but must be used with care and within limits')])


T(2, 'Applying the rules of interpretation to a scenario', area='the application of the rules of interpretation',
  defs=[('ambiguity', 'A situation in which a word or phrase in a statute is capable of having more than one meaning, so that the court must decide which meaning Parliament intended.'),
        ('drafting error', 'A mistake made by the parliamentary draftsman in the wording of an Act, which may lead to a meaning Parliament clearly did not intend.')],
  mcqs=[('A statute makes it an offence to "sell" a product, and the court applies the technical contract-law meaning of "sell". Which rule is it applying?', 'The literal rule', ['The mischief rule', 'The golden rule (wide approach)', 'The purposive approach'], 'Fisher v Bell (1960): the technical legal meaning of "offer for sale" was applied.'),
        ('A court reads an Act so as to avoid a result that would allow a criminal to profit from a serious crime, even though the words are clear. Which approach is it using?', 'The golden rule (wide approach)', ['The literal rule', 'The ejusdem generis rule', 'The narrow approach to the golden rule'], 'Re Sigsworth (1935) and R v Registrar General, ex p Smith (1991) illustrate the wide approach.'),
        ('When applying the rules to a problem question, what should a student normally do first?', 'Identify the word or phrase in the statute whose meaning is in dispute', ['Decide which party they prefer', 'Look for a Practice Statement', 'Decide whether the Act is valid'], 'Identify the problem word, then apply each rule in turn with authority.'),
        ('In Cheeseman v DPP (1990), police officers watching a public toilet were held not to be "passengers". Which aid helped the court reach this literal meaning?', 'A dictionary', ['Hansard', 'A Law Commission report', 'The Practice Statement 1966'], 'The court used a dictionary definition of "passenger" (a person passing by).')],
  cases=[('R v Registrar General, ex p Smith (1991)', 'a man detained in a secure hospital after killing a cell-mate applied for his birth certificate, which the Adoption Act 1976 gave him an absolute right to obtain', 'under the golden rule (wide approach) the court refused to apply the literal words because of the risk he would harm his birth mother'),
         ('Inco Europe Ltd v First Choice Distribution (2000)', 'a section of the Arbitration Act 1996 contained an obvious drafting error that would have changed the law on appeals by mistake', 'the court may correct an obvious drafting error and read in words if it is clear what Parliament intended'),
         ('Cheeseman v DPP (1990)', 'police officers hid in a public toilet to catch the defendant, who was charged with an offence done "to the annoyance of passengers"', 'using the literal rule and a dictionary, police officers who were not passing through were not "passengers"')],
  ars=[('Different rules of statutory interpretation can lead to different outcomes on the same facts.', 'There is no fixed order in which judges must apply the rules of interpretation.', 'A'),
       ('Judges must always use the mischief rule before the literal rule.', 'Judges are free to choose which rule of interpretation to apply.', 'D')],
  exps=[('Explain how a student should structure an answer applying statutory interpretation to a problem.', 'Identify the word in dispute; explain each rule (literal, golden, mischief/purposive) with a case; apply each rule to the facts to show the likely outcome; reach a conclusion on the most likely approach.', '1 mark identify word; 1 mark explain rules with cases; 1 mark apply each rule; 1 mark conclusion. [4]'),
        ('Explain why the outcome of a case may depend on which rule of interpretation the judge chooses.', 'The rules can give different meanings to the same words: the literal rule may convict (or acquit) on the plain words, while the mischief rule may produce the opposite result by looking at the problem the Act was aimed at; because there is no hierarchy, the judge\'s choice can decide the case.', '1 mark: rules give different meanings; 1 mark: example; 1 mark: no hierarchy / judicial choice. [3]')],
  scen=[si_frame('apply')] * 4,
  ev=[('"The rules of statutory interpretation are unpredictable because judges are free to choose which one to apply." Discuss.', ['no hierarchy of rules, so outcomes depend on the judge', 'cases such as LNER v Berriman and Smith v Hughes produce opposite approaches', 'makes legal advice difficult'],
       ['the modern purposive approach is now dominant, giving more consistency', 'aids such as Hansard and explanatory notes help', 'the literal rule remains the starting point, giving some predictability'],
       ['LNER v Berriman (1946)', 'Smith v Hughes (1960)', 'Pepper v Hart (1993)', 'R (Quintavalle) v Secretary of State for Health (2003)'], 'there is some unpredictability, but the modern purposive approach and aids reduce it')])

# =====================================================================================
# 3 Judicial precedent
# =====================================================================================

T(3, 'Stare decisis, ratio decidendi and obiter dicta', area='judicial precedent',
  defs=[('stare decisis', 'Latin for "stand by what has been decided": the principle that courts follow the legal rules decided in earlier cases where the material facts are similar.'),
        ('ratio decidendi', 'The legal principle or reason for the decision in a case, which forms the binding part of a precedent for lower (and sometimes the same) courts.'),
        ('obiter dicta', '"Things said by the way": remarks by a judge that are not part of the ratio decidendi; they are persuasive but not binding.'),
        ('binding precedent', 'A previous decision that a court must follow, because it was made by a higher court (or in some cases the same court) and the material facts are sufficiently similar.'),
        ('persuasive precedent', 'A previous decision or statement that a court is not bound to follow but may choose to follow, such as obiter dicta, Privy Council decisions or dissenting judgments.'),
        ('original precedent', 'A decision on a point of law that has never been decided before, so the judge must decide it by reasoning from analogy or principle.')],
  mcqs=[('Which part of a judgment is binding on lower courts?', 'The ratio decidendi', ['The obiter dicta', 'The dissenting judgment', 'The summary of the facts'], 'Only the ratio decidendi is binding.'),
        ('Which of these is a source of persuasive precedent?', 'Decisions of the Judicial Committee of the Privy Council', ['The ratio of a Supreme Court decision', 'An Act of Parliament', 'The ratio of a Court of Appeal decision for a High Court judge'], 'Privy Council decisions are persuasive, e.g. A-G for Jersey v Holley (2005).'),
        ('Obiter dicta in R v Howe (1987) that duress should not be a defence to attempted murder were later followed in which case?', 'R v Gotts (1992)', ['R v Hasan (2005)', 'R v Graham (1982)', 'R v Woollin (1998)'], 'The Court of Appeal in Gotts followed the persuasive obiter in Howe.'),
        ('In Hedley Byrne v Heller (1964), the House of Lords adopted reasoning from which earlier source?', 'Lord Denning\'s dissenting judgment in Candler v Crane Christmas (1951)', ['The ratio of Donoghue v Stevenson (1932)', 'A Law Commission report', 'A decision of the European Court of Human Rights'], 'A dissenting judgment is persuasive and was later adopted.')],
  cases=[('Donoghue v Stevenson (1932)', 'a woman became ill after drinking ginger beer containing the decomposed remains of a snail, bought for her by a friend', 'a manufacturer owes a duty of care to the ultimate consumer of its products (the neighbour principle), which became a binding original precedent'),
         ('R v Howe (1987)', 'the defendants took part in murders under threats of death and argued duress', 'duress is no defence to murder; the obiter statement that it is also no defence to attempted murder was persuasive'),
         ('R v Gotts (1992)', 'a 16-year-old stabbed his mother on his father\'s orders under threat of being shot', 'following the persuasive obiter in R v Howe, duress is no defence to attempted murder'),
         ('Central London Property Trust v High Trees House (1947)', 'a landlord agreed to halve the rent on a block of flats during the Second World War', 'Lord Denning\'s obiter dicta on promissory estoppel became an influential persuasive precedent'),
         ('A-G for Jersey v Holley (2005)', 'the Privy Council considered the test for provocation in a case from Jersey', 'a Privy Council decision is persuasive, but was followed by the Court of Appeal in R v James and Karimi (2006) in preference to a House of Lords decision')],
  ars=[('Obiter dicta do not have to be followed by later courts.', 'Obiter dicta are not part of the reason for the decision.', 'A'),
       ('The ratio decidendi is always clearly labelled in a judgment.', 'Where there are several judgments, the ratio may be difficult to identify.', 'D'),
       ('A dissenting judgment can never influence the law.', 'Dissenting judgments are a type of persuasive precedent.', 'D')],
  exps=[('Explain the difference between ratio decidendi and obiter dicta.', 'The ratio is the legal principle on which the decision is based and is binding; obiter dicta are other comments, e.g. on hypothetical facts, which are only persuasive.', '1 mark ratio; 1 mark obiter; 1 mark binding v persuasive. [3]'),
        ('Explain two sources of persuasive precedent.', 'Obiter dicta (e.g. R v Howe followed in R v Gotts); decisions of lower courts or the Privy Council (A-G for Jersey v Holley); dissenting judgments (Candler v Crane Christmas); decisions of courts in other common law countries.', '2 × (1 mark source, 1 mark example/explanation). [4]'),
        ('Explain why it can be difficult to identify the ratio decidendi of a case.', 'Judges do not label the ratio; judgments can be long; in appeal courts each judge may give different reasons, so there may be no single ratio.', '1 mark per reason, up to 2. [2]')],
  cmps=[('binding precedent', 'persuasive precedent', ['binding precedent must be followed, persuasive precedent may be followed', 'binding precedent comes from the ratio of higher courts; persuasive comes from obiter, the Privy Council, lower courts or dissents']),
        ('ratio decidendi', 'obiter dicta', ['the ratio is the reason for the decision and is binding, obiter dicta are statements by the way and are persuasive', 'the ratio is based on the material facts, obiter dicta may concern hypothetical situations'])],
  scen=[dict(facts='In {case}, the {court} held that {held}. The judge added that "{obiter}". {A} is now bringing a similar case in the {lower}.',
             slots={'case': ['Arden v Bexley (fictional, 2019)', 'Patel v Northgate Ltd (fictional, 2021)', 'Okafor v Riverside Council (fictional, 2018)'],
                    'court': ['Court of Appeal', 'Supreme Court'], 'lower': ['High Court', 'county court'],
                    'held': ['a gym owed a duty of care to members injured by faulty equipment', 'a landlord was liable for damp caused by a broken gutter'],
                    'obiter': ['the same principle would probably apply to a free public sports facility', 'the position might be different if the tenant had caused the damage']},
             issue='the distinction between the binding ratio decidendi and persuasive obiter dicta', wrong=['the Practice Statement 1966', 'the mischief rule', 'the ultra vires rule'],
             ask='Explain which parts of the earlier judgment the {lower} must follow in {A}\'s case.',
             law=['the ratio decidendi of a higher court binds lower courts through stare decisis', 'obiter dicta are persuasive only (R v Howe and R v Gotts)', 'the material facts must be sufficiently similar for the ratio to apply'],
             apply=['the {court} is above the {lower} in the hierarchy', 'the holding that {held} is the ratio and binds the {lower} if the material facts are similar', 'the remark that "{obiter}" is obiter and need not be followed'],
             concl='the {lower} is bound by the ratio if the facts are similar but may choose whether to follow the obiter comment')],
  ev=[('Evaluate the importance of the distinction between ratio decidendi and obiter dicta in the doctrine of precedent.', ['only the ratio binds, so the law develops in a controlled way', 'obiter allows judges to signal future developments (High Trees, R v Howe)', 'persuasive precedent gives flexibility'],
       ['the ratio is often hard to identify', 'multiple judgments make the ratio unclear', 'lower courts may treat obiter as almost binding'],
       ['Donoghue v Stevenson (1932)', 'R v Howe (1987)', 'R v Gotts (1992)', 'Central London Property Trust v High Trees House (1947)'], 'the distinction is central to precedent but its practical application can be uncertain')])

T(3, 'The court hierarchy and binding precedent; the Practice Statement 1966', area='the court hierarchy and precedent',
  defs=[('Practice Statement 1966', 'A statement by the Lord Chancellor on behalf of the House of Lords that it would treat its own former decisions as normally binding but would depart from them "when it appears right to do so"; it now applies to the Supreme Court.'),
        ('per incuriam', 'A decision made "through lack of care", i.e. in ignorance of a relevant statute or binding precedent; the Court of Appeal need not follow its own per incuriam decisions.'),
        ('court hierarchy', 'The ranking of the courts, which decides which courts\' decisions bind which other courts in the doctrine of precedent.')],
  mcqs=[('Which was the first major use of the Practice Statement 1966?', 'British Railways Board v Herrington (1972)', ['Conway v Rimmer (1968)', 'Young v Bristol Aeroplane Co (1944)', 'R v Gotts (1992)'], 'Herrington overruled Addie v Dumbreck (1929) on the duty owed to child trespassers; Conway v Rimmer (1968) was an earlier, minor use.'),
        ('Which case sets out the exceptions to the rule that the Court of Appeal (Civil Division) is bound by its own decisions?', 'Young v Bristol Aeroplane Co (1944)', ['Davis v Johnson (1979)', 'R v Shivpuri (1986)', 'Pepper v Hart (1993)'], 'Young: conflicting CA decisions; conflict with a later HL/SC decision; per incuriam.'),
        ('Since October 2009, which court has been at the top of the court hierarchy for most cases in the English legal system?', 'The Supreme Court', ['The House of Lords', 'The Court of Appeal', 'The Privy Council'], 'The Constitutional Reform Act 2005 created the Supreme Court, which replaced the Appellate Committee of the House of Lords.'),
        ('Why does the Court of Appeal (Criminal Division) have more freedom to depart from its own decisions than the Civil Division?', 'Because a person\'s liberty is at stake', ['Because it has more judges', 'Because it is above the Supreme Court', 'Because criminal law is made only by Parliament'], 'R v Taylor (1950) and R v Spencer (1985): greater flexibility where liberty is involved.'),
        ('In R v Shivpuri (1986), the House of Lords used the Practice Statement to overrule which decision made only a year earlier?', 'Anderton v Ryan (1985)', ['Addie v Dumbreck (1929)', 'DPP v Majewski (1977)', 'Donoghue v Stevenson (1932)'], 'Shivpuri overruled Anderton v Ryan on attempting the impossible.')],
  cases=[('British Railways Board v Herrington (1972)', 'a six-year-old child was badly burned on an electrified railway line after getting through a broken fence', 'the House of Lords used the Practice Statement to overrule Addie v Dumbreck (1929) and held that occupiers owe a duty of common humanity to child trespassers'),
         ('R v Shivpuri (1986)', 'the defendant believed he was dealing in drugs but the substance was harmless vegetable matter', 'the House of Lords used the Practice Statement to overrule Anderton v Ryan (1985): a person can be guilty of attempting the impossible'),
         ('Young v Bristol Aeroplane Co Ltd (1944)', 'the Court of Appeal considered whether it was bound by its own previous decisions', 'the Court of Appeal is bound by its own decisions except where they conflict, conflict with a later House of Lords decision or were made per incuriam'),
         ('Davis v Johnson (1979)', 'Lord Denning in the Court of Appeal refused to follow the Court of Appeal\'s own earlier decisions on domestic violence injunctions', 'the House of Lords confirmed that the Court of Appeal is bound by its own previous decisions, subject only to the Young exceptions'),
         ('R v G and R (2003)', 'two boys aged 11 and 12 set fire to newspapers behind a shop, causing about £1 million of damage', 'the House of Lords used the Practice Statement to overrule MPC v Caldwell (1982): recklessness in criminal damage is subjective'),
         ('Conway v Rimmer (1968)', 'a probationary police officer wanted to see documents that the Home Office claimed were privileged', 'this was the first use of the Practice Statement, on a technical point of the law of evidence'),
         ('R v R (1991)', 'a husband was charged with raping his wife, relying on the old rule that a husband could not rape his wife', 'the House of Lords held that the marital rape exemption was no longer part of the law')],
  ars=[('The Supreme Court can depart from its own previous decisions.', 'The Practice Statement 1966 allows the highest court to depart from its own decisions when it appears right to do so.', 'A'),
       ('The High Court is bound by decisions of the Court of Appeal.', 'Courts lower in the hierarchy are bound by the ratio of courts above them.', 'A'),
       ('The Court of Appeal can always overrule decisions of the Supreme Court.', 'The Court of Appeal is bound by decisions of the Supreme Court.', 'D')],
  exps=[('Explain the three exceptions in Young v Bristol Aeroplane Co (1944).', 'The Court of Appeal may depart from its own decision where there are two conflicting decisions of its own (it must choose one); where its decision conflicts with a later House of Lords/Supreme Court decision; and where the decision was made per incuriam.', '1 mark per exception. [3]'),
        ('Explain why the House of Lords issued the Practice Statement in 1966.', 'Too rigid adherence to precedent could lead to injustice in particular cases and restrict the proper development of the law, so the House of Lords wanted the flexibility to depart from its own decisions.', '1 mark: rigidity/injustice; 1 mark: allow development of the law. [2]'),
        ('Explain why the House of Lords used the Practice Statement only rarely.', 'It recognised the need for certainty in areas such as contract, property and criminal law, where people rely on the law; changing the law has retrospective effect, and Parliament may be better placed to make major changes.', '1 mark: certainty/reliance; 1 mark: retrospective effect or role of Parliament. [2]'),
        ('Describe the position of the High Court in the doctrine of precedent.', 'The High Court is bound by the Supreme Court and the Court of Appeal; Divisional Courts are bound by their own decisions; it binds the county courts and magistrates\' courts.', '1 mark: bound by higher courts; 1 mark: Divisional Courts bound by own decisions/binds inferior courts. [2]')],
  cmps=[('the Court of Appeal (Civil Division)', 'the Court of Appeal (Criminal Division)', ['the Criminal Division has more freedom to depart from its own decisions because liberty is at stake', 'the Civil Division is bound by its own decisions subject only to the Young exceptions']),
        ('overruling under the Practice Statement', 'the Young v Bristol Aeroplane exceptions', ['the Practice Statement applies to the Supreme Court, Young applies to the Court of Appeal', 'the Practice Statement is a general power to depart "when it appears right", Young sets out limited, specific exceptions'])],
  scen=[dict(facts='{A} is a party to a case in the {court}. The legal point was decided in {prev}, a decision of the {pcourt}, which {A}\'s lawyer argues was wrongly decided.',
             slots={'court': [('High Court', 'is bound by the Court of Appeal and Supreme Court and cannot overrule them'), ('Court of Appeal (Civil Division)', 'is bound by its own decisions subject to the exceptions in Young v Bristol Aeroplane, and by the Supreme Court'), ('Supreme Court', 'can depart from its own previous decisions under the Practice Statement 1966 when it appears right to do so')],
                    'prev': ['Mills v Harbour Ltd (fictional, 2001)', 'Rana v Coastline plc (fictional, 1998)', 'Bell v Westfield Council (fictional, 2010)'],
                    'pcourt': ['Supreme Court', 'Court of Appeal']},
             issue='the binding effect of precedent in the court hierarchy', wrong=['the purposive approach', 'the rule in Heydon\'s Case', 'the doctrine of parliamentary sovereignty'],
             ask='Advise {A} whether the {court} must follow {prev}.',
             law=['stare decisis: lower courts are bound by the ratio of higher courts', 'the {court} {court_1}', 'Practice Statement 1966 used in Herrington (1972) and R v G (2003); Young v Bristol Aeroplane exceptions (1944)', 'the court may also be able to distinguish the earlier case on its material facts'],
             apply=['the earlier decision was made by the {pcourt}', 'the {court} {court_1}', 'if the material facts differ, the {court} could distinguish {prev}'],
             concl='whether {prev} must be followed depends on where the {pcourt} sits in relation to the {court}; distinguishing may be possible if the material facts differ'),
        dict(facts='The Court of Appeal (Civil Division) is hearing an appeal by {A}. There are two earlier Court of Appeal decisions on the same point which {conflict}.',
             slots={'conflict': [('conflict with each other', 'the court can choose which of its two conflicting decisions to follow'), ('were both made without reference to a relevant statute', 'the decisions were made per incuriam and need not be followed'), ('conflict with a later Supreme Court decision', 'the court must follow the Supreme Court decision')]},
             issue='the exceptions in Young v Bristol Aeroplane Co (1944)', wrong=['the Practice Statement 1966', 'the golden rule', 'the ultra vires rule'],
             ask='Advise whether the Court of Appeal is bound by its earlier decisions in {A}\'s case.',
             law=['the Court of Appeal is normally bound by its own previous decisions (Davis v Johnson 1979)', 'Young v Bristol Aeroplane (1944): exceptions for conflicting decisions, conflict with a later House of Lords/Supreme Court decision and per incuriam decisions', 'the Practice Statement does not apply to the Court of Appeal'],
             apply=['the earlier decisions {conflict}', 'so {conflict_1}'],
             concl='{conflict_1}, so the Court of Appeal is not bound to follow the earlier decision against {A}')],
  ev=[('Evaluate the extent to which the Practice Statement 1966 has made the law more flexible.', ['allowed the law to develop with social change (Herrington, R v R)', 'corrected errors quickly (Shivpuri overruling Anderton v Ryan)', 'R v G (2003) restored subjective recklessness'],
       ['used rarely because of the need for certainty', 'the Court of Appeal cannot use it', 'changes depend on cases reaching the Supreme Court'],
       ['British Railways Board v Herrington (1972)', 'R v Shivpuri (1986)', 'R v G and R (2003)', 'Davis v Johnson (1979)'], 'the Practice Statement has added useful flexibility but is used cautiously')])

T(3, 'Avoiding precedent: distinguishing, overruling and reversing', area='avoiding precedent',
  defs=[('distinguishing', 'A method of avoiding a precedent by showing that the material facts of the present case are sufficiently different from those of the earlier case, so the earlier ratio does not apply.'),
        ('overruling', 'Where a higher court (or the Supreme Court under the Practice Statement) decides that the legal rule in an earlier case was wrong and sets it aside for the future.'),
        ('reversing', 'Where a higher court, on appeal in the same case, changes the decision of the lower court.'),
        ('disapproving', 'Where a court expresses the opinion that an earlier decision was wrong but does not overrule it because it is not necessary to decide the point.')],
  mcqs=[('Which pair of cases is the classic example of distinguishing?', 'Balfour v Balfour (1919) and Merritt v Merritt (1970)', ['Herrington (1972) and Addie v Dumbreck (1929)', 'R v Howe (1987) and R v Gotts (1992)', 'Pepper v Hart (1993) and Davis v Johnson (1979)'], 'In Merritt the spouses had separated when they made the agreement, so Balfour was distinguished.'),
        ('A higher court changes the decision of the lower court in the same case on appeal. This is called:', 'reversing', ['overruling', 'distinguishing', 'disapproving'], 'Reversing concerns the same case; overruling concerns a different, earlier case.'),
        ('Which statement about overruling is correct?', 'It has retrospective effect, so it applies to events before the new decision', ['It only applies to future events', 'It can only be done by Parliament', 'It concerns the same case on appeal'], 'Overruling declares what the law has always been, as in R v R (1991) and SW v UK (1995).'),
        ('Which court overruled Addie v Dumbreck (1929)?', 'The House of Lords in British Railways Board v Herrington (1972)', ['The Court of Appeal in Young v Bristol Aeroplane', 'Parliament in the Occupiers\' Liability Act 1957', 'The High Court in Merritt v Merritt'], 'Herrington used the Practice Statement.')],
  cases=[('Balfour v Balfour (1919)', 'a husband working abroad promised to pay his wife £30 a month while they were living together happily but temporarily apart', 'agreements between spouses living together are presumed not to be intended to create legal relations'),
         ('Merritt v Merritt (1970)', 'a husband who had left his wife signed an agreement to transfer the house to her if she paid off the mortgage', 'Balfour v Balfour was distinguished because the couple had separated, so there was intention to create legal relations'),
         ('Addie v Dumbreck (1929)', 'a child trespasser was killed by machinery at a colliery', 'an occupier owed no duty to trespassers except not to injure them deliberately or recklessly; this was later overruled in Herrington'),
         ('Sweet v Parsley (1970)', 'a teacher who sublet a farmhouse was convicted when tenants smoked cannabis there without her knowledge', 'the House of Lords reversed the conviction, holding that mens rea is presumed to be required'),
         ('R v Brown (1993)', 'a group of men consensually took part in sado-masochistic acts causing wounds', 'consent is no defence to actual bodily harm or worse except in recognised exceptions; the case was distinguished in R v Wilson (1996)'),
         ('R v Wilson (1996)', 'a husband branded his initials on his wife\'s buttocks with a hot knife at her request', 'R v Brown was distinguished: consensual activity between spouses akin to tattooing was not criminal')],
  ars=[('Distinguishing allows a lower court to avoid an unjust precedent from a higher court.', 'Distinguishing depends on finding a material difference in the facts.', 'A'),
       ('Overruling and reversing mean the same thing.', 'Reversing happens in the same case on appeal.', 'D'),
       ('Overruling can cause injustice to people who relied on the old law.', 'Overruling operates retrospectively.', 'A')],
  exps=[('Explain the difference between overruling and reversing.', 'Overruling is where a court in a later case decides that the legal rule in an earlier, different case was wrong (Herrington overruling Addie v Dumbreck); reversing is where a higher court changes the decision of a lower court in the same case on appeal.', '1 mark overruling; 1 mark reversing; 1 mark example. [3]'),
        ('Explain how distinguishing gives flexibility to the doctrine of precedent.', 'Any court can distinguish, so judges can avoid an earlier precedent that would produce an unjust result where the material facts differ, e.g. Merritt v Merritt distinguished Balfour v Balfour.', '1 mark: any court can use it; 1 mark: material facts differ; 1 mark: example. [3]'),
        ('Explain why distinguishing is sometimes criticised.', 'Judges may draw very fine or artificial distinctions to avoid a precedent, which makes the law complex and uncertain and difficult to predict.', '1 mark: artificial/fine distinctions; 1 mark: uncertainty/complexity. [2]')],
  cmps=[('distinguishing', 'overruling', ['distinguishing leaves the earlier precedent intact while overruling sets it aside', 'any court can distinguish but only a higher court (or the Supreme Court under the Practice Statement) can overrule', 'distinguishing depends on different material facts, overruling on the earlier law being wrong'])],
  scen=[dict(facts='In {prev}, a higher court held that {rule}. {A} now brings a similar case in a lower court, but in {A}\'s case {rule_1}.',
             slots={'prev': ['Green v Hollis (fictional, 2005)', 'Moss v Trent Ltd (fictional, 2012)'],
                    'rule': [('a promise between friends to share petrol costs was not legally binding', 'the parties in {A}\'s case had signed a written agreement and were running a business together'),
                             ('a shop was not liable for a customer\'s fall on a dry floor', 'the floor in {A}\'s case had been wet for two hours without a warning sign')]},
             issue='distinguishing a precedent', wrong=['overruling under the Practice Statement', 'reversing on appeal', 'implied repeal'],
             ask='Explain how the lower court could avoid following {prev} and whether it is likely to do so.',
             law=['a lower court is bound by the ratio of a higher court where the material facts are similar', 'it may distinguish the precedent if the material facts are significantly different (Balfour v Balfour and Merritt v Merritt)', 'a lower court cannot overrule a higher court'],
             apply=['in {prev} the court held that {rule}', 'in {A}\'s case {rule_1}', 'this is a material difference, so the lower court can distinguish {prev}'],
             concl='the lower court is likely to distinguish {prev} because the material facts differ, so it is not bound to follow it'),
        dict(facts='{A} was convicted in the Crown Court. The Court of Appeal dismissed {A}\'s appeal, applying an old Supreme Court precedent. The Supreme Court has now given permission to appeal and is asked to {ask2}.',
             slots={'ask2': ['change the decision in {A}\'s case and set aside the old precedent', 'quash the conviction because the old precedent was wrongly decided']},
             issue='reversing and overruling', wrong=['distinguishing', 'disapproving obiter dicta', 'per incuriam in the Crown Court'],
             ask='Explain how the Supreme Court could change the law and the outcome of {A}\'s case.',
             law=['reversing: a higher court changes the decision of a lower court in the same case on appeal (Sweet v Parsley)', 'overruling: the Supreme Court can overrule its own earlier decision using the Practice Statement 1966 (Herrington; R v G)', 'overruling operates retrospectively'],
             apply=['by allowing {A}\'s appeal the Supreme Court would reverse the Court of Appeal\'s decision', 'if it decides the old precedent was wrong it would overrule it', 'the Court of Appeal had to apply the old precedent because it was bound by it'],
             concl='the Supreme Court can both reverse the decision in {A}\'s case and overrule the old precedent under the Practice Statement')],
  ev=[('"Distinguishing gives judges too much freedom to avoid precedents they dislike." Discuss.', ['fine distinctions allow judges to reach their preferred outcome', 'leads to uncertainty and complexity', 'R v Brown and R v Wilson are hard to reconcile'],
       ['distinguishing is necessary to avoid injustice', 'judges must find a genuine material difference', 'it allows the law to develop gradually'],
       ['Balfour v Balfour (1919)', 'Merritt v Merritt (1970)', 'R v Brown (1993)', 'R v Wilson (1996)'], 'distinguishing is a valuable tool for flexibility but its misuse can reduce certainty')])

T(3, 'Advantages and disadvantages of the doctrine of precedent', area='the doctrine of precedent',
  defs=[('certainty', 'The advantage of precedent that lawyers and the public can predict how the law will be applied because courts follow earlier decisions.'),
        ('retrospective effect', 'The effect of a new judicial decision that applies to events occurring before the decision was made, as in R v R (1991).')],
  mcqs=[('Which is an advantage of the doctrine of precedent?', 'It provides certainty so people can predict the outcome of cases', ['It allows any judge to ignore earlier decisions', 'It means law is only made by Parliament', 'It removes the need for appeals'], 'Certainty and consistency are the main advantages.'),
        ('Which is a disadvantage of the doctrine of precedent?', 'It can be rigid, so a bad decision may be followed for many years', ['It makes the law completely unpredictable', 'It prevents lawyers from giving advice', 'It requires Parliament to approve every judgment'], 'Rigidity: e.g. Addie v Dumbreck stood from 1929 to 1972.'),
        ('In SW v UK (1995), the European Court of Human Rights considered whether which decision had unfair retrospective effect?', 'R v R (1991)', ['Donoghue v Stevenson (1932)', 'R v Shivpuri (1986)', 'Merritt v Merritt (1970)'], 'The ECtHR held there was no breach of Article 7 as the change was a foreseeable development.')],
  cases=[('SW v United Kingdom (1995)', 'a husband convicted after R v R abolished the marital rape exemption argued that the law had been changed retrospectively', 'the European Court of Human Rights held there was no breach of Article 7 because the development of the law was reasonably foreseeable')],
  ars=[('The doctrine of precedent helps to save time in the courts.', 'Where a point of law has already been decided, cases need not be re-argued from first principles.', 'A'),
       ('The doctrine of precedent prevents the law from ever changing.', 'The Practice Statement and distinguishing allow some flexibility.', 'D')],
  exps=[('Explain two advantages of the doctrine of precedent.', 'Certainty: people can predict outcomes and plan; consistency/fairness: like cases are treated alike; time-saving; flexibility through distinguishing and the Practice Statement; practical rules based on real cases.', '2 × (1 mark advantage, 1 mark explanation). [4]'),
        ('Explain two disadvantages of the doctrine of precedent.', 'Rigidity: lower courts must follow bad decisions; complexity and volume of reported cases; slow growth because change depends on cases being appealed; retrospective effect (R v R); judge-made law is undemocratic.', '2 × (1 mark disadvantage, 1 mark explanation). [4]'),
        ('Explain why the retrospective effect of judicial decisions may be unfair.', 'A new decision applies to events that happened before it was made, so a person may be liable or guilty under a rule that did not exist when they acted, as argued in SW v UK.', '1 mark: applies to past events; 1 mark: unfairness/example. [2]')],
  ev=[('Evaluate the advantages and disadvantages of the doctrine of judicial precedent.', ['certainty and predictability', 'consistency and fairness', 'flexibility through distinguishing and the Practice Statement', 'detailed practical rules from real cases'],
       ['rigidity: bad decisions may stand for years (Addie v Dumbreck)', 'complexity and volume of case law', 'slow development, depending on appeals', 'retrospective effect (R v R; SW v UK)', 'judicial law-making is undemocratic'],
       ['British Railways Board v Herrington (1972)', 'Balfour v Balfour and Merritt v Merritt', 'R v R (1991)', 'SW v UK (1995)', 'Young v Bristol Aeroplane (1944)'], 'precedent achieves a reasonable balance between certainty and flexibility, although it can be slow and rigid'),
      ('"The doctrine of precedent achieves a good balance between certainty and flexibility." Discuss.', ['certainty from stare decisis and the hierarchy', 'flexibility from distinguishing, the Practice Statement and Young exceptions'],
       ['Practice Statement used rarely', 'Court of Appeal tightly bound (Davis v Johnson)', 'distinguishing can produce artificial distinctions'],
       ['Practice Statement 1966', 'Young v Bristol Aeroplane (1944)', 'Davis v Johnson (1979)', 'Merritt v Merritt (1970)'], 'the balance generally favours certainty, with flexibility available but used sparingly'),
      ('"Judges should not make law." Discuss in the context of judicial precedent.', ['judges are unelected, so law-making should be left to Parliament', 'retrospective effect of judge-made law is unfair', 'judges lack the resources for wide consultation'],
       ['judges must develop the law when Parliament has not acted (R v R; Donoghue v Stevenson)', 'judge-made law can respond quickly to individual cases', 'Parliament can always reverse judicial decisions'],
       ['Donoghue v Stevenson (1932)', 'R v R (1991)', 'Magor and St Mellons (1950)', 'British Railways Board v Herrington (1972)'], 'judges inevitably make some law, but should do so cautiously and leave major policy changes to Parliament')])

# =====================================================================================
# 4 The courts and alternative dispute resolution
# =====================================================================================

T(4, 'Civil and criminal courts: jurisdiction and the appeal system', area='the courts and appeals',
  defs=[('jurisdiction', 'The power of a court to hear and decide a particular type of case, determined by the type and value or seriousness of the case.'),
        ('appeal by way of case stated', 'An appeal on a point of law from the magistrates\' court (or Crown Court) to the Divisional Court of the King\'s Bench Division, based on a written statement of the facts and the law applied.'),
        ('small claims track', 'The track used in the county court for straightforward civil claims of up to £10 000, with simplified procedure and limited recovery of legal costs.'),
        ('Criminal Cases Review Commission', 'An independent body set up under the Criminal Appeal Act 1995 to investigate possible miscarriages of justice and refer cases back to the appeal courts.'),
        ('leave to appeal', 'Permission to appeal, which must normally be obtained from the trial court or the appeal court before an appeal can be heard.')],
  mcqs=[('Which court hears the trial of indictable offences such as murder?', 'The Crown Court', ['The magistrates\' court', 'The county court', 'The Divisional Court'], 'Indictable offences are tried by a judge and jury in the Crown Court.'),
        ('A claimant wants to sue for £6 000 for a faulty car. To which track is the claim most likely to be allocated?', 'The small claims track in the county court', ['The fast track in the High Court', 'The multi-track in the Court of Appeal', 'The Crown Court'], 'Most claims up to £10 000 go to the small claims track.'),
        ('On what ground will the Court of Appeal (Criminal Division) allow an appeal against conviction?', 'The conviction is unsafe', ['The defendant has changed solicitor', 'The sentence was too lenient', 'The jury took too long'], 'Criminal Appeal Act 1995 s2: the only ground is that the conviction is unsafe.'),
        ('Which Act created an exception to the double jeopardy rule for cases where there is new and compelling evidence?', 'Criminal Justice Act 2003', ['Criminal Appeal Act 1968', 'Bail Act 1976', 'Courts Act 1971'], 'Part 10 of the CJA 2003; used in R v Dobson (2011).'),
        ('Which court hears appeals on points of law of general public importance from the Court of Appeal?', 'The Supreme Court', ['The High Court', 'The Crown Court', 'The Privy Council'], 'The Supreme Court is the final appeal court, with permission.'),
        ('Which civil track normally deals with claims of between £10 000 and £25 000 that can be tried in one day?', 'The fast track', ['The small claims track', 'The multi-track', 'The Divisional Court track'], 'Fast track: £10 000–£25 000, trial of up to one day.')],
  cases=[('R v Dobson (2011)', 'the defendant had been acquitted of the murder of Stephen Lawrence in 1996, but new DNA evidence was found', 'under the Criminal Justice Act 2003 an acquittal can be quashed and a retrial ordered where there is new and compelling evidence'),
         ('Attorney-General\'s Reference (No 4 of 1989)', 'a sentence passed by the Crown Court was referred by the Attorney-General as unduly lenient', 'the Court of Appeal may increase a sentence that is unduly lenient on a reference by the Attorney-General under the Criminal Justice Act 1988')],
  ars=[('The prosecution can appeal against an acquittal by a jury in all cases.', 'The Criminal Justice Act 2003 allows a retrial for serious offences where there is new and compelling evidence.', 'D'),
       ('Appeals from the magistrates\' court on a point of law go to the Divisional Court of the King\'s Bench Division.', 'Appeals by way of case stated deal with points of law.', 'A'),
       ('The county court hears most civil cases.', 'The county court has jurisdiction over contract, tort, consumer and housing claims of lower value.', 'A')],
  exps=[('Describe the routes of appeal for a defendant convicted in the magistrates\' court.', 'An appeal against conviction or sentence to the Crown Court (rehearing by a judge and two magistrates); or an appeal by way of case stated on a point of law to the Divisional Court of the King\'s Bench Division, with a possible further appeal to the Supreme Court.', '1 mark: Crown Court route; 1 mark: case stated to Divisional Court; 1 mark: further appeal to Supreme Court on point of law of public importance. [3]'),
        ('Describe the routes of appeal for a defendant convicted in the Crown Court.', 'Appeal against conviction or sentence to the Court of Appeal (Criminal Division) with leave; the ground is that the conviction is unsafe; further appeal to the Supreme Court if a point of law of general public importance is certified and permission granted.', '1 mark: CA Criminal Division, leave needed; 1 mark: unsafe ground; 1 mark: Supreme Court route. [3]'),
        ('Explain two ways in which the prosecution can appeal in criminal cases.', 'By case stated from the magistrates\' court on a point of law; Attorney-General\'s reference on a point of law after an acquittal (which does not affect the acquittal); reference of an unduly lenient sentence; retrial for new and compelling evidence (CJA 2003).', '2 × (1 mark route, 1 mark explanation). [4]'),
        ('Explain the role of the Criminal Cases Review Commission.', 'It investigates alleged miscarriages of justice after normal appeals have failed and can refer a case back to the Court of Appeal if there is a real possibility the conviction would not be upheld.', '1 mark: investigates miscarriages; 1 mark: refers to Court of Appeal where real possibility. [2]')],
  cmps=[('the county court', 'the High Court', ['the county court hears lower-value and less complex civil claims, the High Court higher-value or complex claims', 'the High Court has three divisions (King\'s Bench, Chancery, Family) and also hears appeals in Divisional Courts']),
        ('the magistrates\' court', 'the Crown Court', ['the magistrates\' court tries summary and some either-way offences, the Crown Court indictable and some either-way offences', 'magistrates decide verdict and sentence, while in the Crown Court a jury decides the verdict and a judge sentences', 'the Crown Court has greater sentencing powers'])],
  scen=[dict(facts='{A} was convicted of {off} after a trial in the {court}. {A} believes that {complaint}.',
             slots={'off': [('theft', 'either-way'), ('assault occasioning actual bodily harm', 'either-way'), ('burglary', 'either-way')],
                    'court': [('magistrates\' court', 'appeal to the Crown Court against conviction or sentence, or by way of case stated on a point of law to the Divisional Court of the King\'s Bench Division'), ('Crown Court', 'appeal with leave to the Court of Appeal (Criminal Division) on the ground that the conviction is unsafe, and possibly to the Supreme Court on a point of law of general public importance')],
                    'complaint': ['the trial judge or magistrates misunderstood the law', 'important evidence was wrongly admitted', 'the sentence was too harsh']},
             issue='the criminal appeal system', wrong=['the civil track allocation system', 'judicial review of delegated legislation', 'the Practice Statement 1966'],
             ask='Advise {A} on the appeal routes available.',
             law=['from the magistrates\' court: appeal to the Crown Court, or case stated to the Divisional Court on a point of law', 'from the Crown Court: appeal with leave to the Court of Appeal (Criminal Division); conviction quashed if unsafe (Criminal Appeal Act 1995)', 'further appeal to the Supreme Court requires a certified point of law of general public importance', 'the Criminal Cases Review Commission can refer cases after appeals fail'],
             apply=['{A} was tried in the {court}, so the route is: {court_1}', 'the complaint that {complaint} could support an appeal'],
             concl='{A} can {court_1}'),
        dict(facts='{A} wants to sue a {who} in {city} for £{amt} because {why}.',
             slots={'who': ['builder', 'garage', 'online retailer', 'landlord'],
                    'amt': [('3 500', 'the small claims track in the county court'), ('8 000', 'the small claims track in the county court'), ('18 000', 'the fast track in the county court'), ('250 000', 'the multi-track, possibly in the High Court')],
                    'why': ['the work done was defective', 'goods supplied were faulty', 'a deposit has not been returned']},
             issue='the civil court system and track allocation', wrong=['the criminal appeal system', 'mode of trial for either-way offences', 'arbitration under the Arbitration Act 1996'],
             ask='Advise {A} which court and track are likely to hear the claim, and describe the possible routes of appeal.',
             law=['civil claims start in the county court or High Court depending on value and complexity', 'small claims track up to £10 000; fast track £10 000–£25 000; higher-value or complex claims go to the multi-track (with an intermediate track for some claims up to £100 000)', 'appeals usually go to the next level of judge, then to the Court of Appeal (Civil Division), with permission'],
             apply=['the claim for £{amt} is likely to be allocated to {amt_1}', 'appeal would require permission'],
             concl='the claim is likely to be heard on {amt_1}')],
  ev=[('Evaluate the effectiveness of the criminal appeal system in correcting miscarriages of justice.', ['two routes from the magistrates\' court', 'Court of Appeal can quash unsafe convictions', 'CCRC investigates miscarriages and has referred many cases', 'double jeopardy reform allows guilty people to be retried (R v Dobson)'],
       ['leave is required and many appeals fail', 'the Court of Appeal is reluctant to interfere with jury verdicts', 'the CCRC has limited resources and long delays', 'the "real possibility" test is restrictive'],
       ['Criminal Appeal Act 1995', 'Criminal Justice Act 2003', 'R v Dobson (2011)'], 'the system corrects many errors but delays and restrictive tests mean some miscarriages remain')])

T(4, 'Criminal process: bail, classification of offences and sentencing aims', area='the criminal process',
  defs=[('bail', 'The release of a suspect or defendant from custody while awaiting the next stage of the case, sometimes subject to conditions.'),
        ('summary offence', 'The least serious type of criminal offence, triable only in the magistrates\' court, such as common assault and most driving offences.'),
        ('triable either way offence', 'An offence of middle seriousness, such as theft or assault occasioning actual bodily harm, which may be tried in either the magistrates\' court or the Crown Court.'),
        ('indictable offence', 'The most serious type of criminal offence, such as murder, manslaughter, rape and robbery, which can be tried only in the Crown Court.'),
        ('deterrence', 'A sentencing aim of discouraging the offender (individual deterrence) or others (general deterrence) from committing crimes in future.'),
        ('rehabilitation', 'A sentencing aim of reforming the offender so that they do not reoffend, for example through community orders with treatment or education requirements.')],
  mcqs=[('Which Act creates a general presumption in favour of bail?', 'Bail Act 1976', ['Criminal Justice Act 2003', 'Police and Criminal Evidence Act 1984', 'Sentencing Act 2020'], 'Section 4 of the Bail Act 1976.'),
        ('Which of the following is an indictable-only offence?', 'Robbery', ['Theft', 'Common assault', 'Speeding'], 'Robbery is indictable only; theft is triable either way; common assault and speeding are summary.'),
        ('Which Act lists the purposes of sentencing adult offenders?', 'Sentencing Act 2020', ['Bail Act 1976', 'Juries Act 1974', 'Courts Act 1971'], 'Section 57 Sentencing Act 2020 (formerly s142 CJA 2003).'),
        ('Which sentencing aim focuses on compensating the victim or the community?', 'Reparation', ['Retribution', 'Deterrence', 'Protection of the public'], 'Reparation: making amends, e.g. compensation orders and unpaid work.'),
        ('Which of these is a ground for refusing bail under the Bail Act 1976?', 'There are substantial grounds for believing the defendant would fail to surrender to custody', ['The defendant is unemployed', 'The defendant has pleaded not guilty', 'The offence is triable either way'], 'Grounds include failing to surrender, committing offences on bail and interfering with witnesses.')],
  ars=[('Theft can be tried in the Crown Court.', 'Theft is a triable either way offence.', 'A'),
       ('A defendant charged with murder can never be granted bail.', 'Bail for murder can be granted only by a Crown Court judge.', 'D'),
       ('Courts may impose conditions when granting bail.', 'Conditions such as curfew, residence and reporting to a police station reduce the risk of absconding or reoffending.', 'A')],
  exps=[('Explain two factors a court considers when deciding whether to grant bail.', 'The nature and seriousness of the offence; the defendant\'s character, previous convictions and community ties; their record of surrendering to bail in the past; and the strength of the evidence.', '2 × (1 mark factor, 1 mark explanation). [4]'),
        ('Explain the difference between retribution and deterrence as aims of sentencing.', 'Retribution (punishment) looks back and punishes the offender because they deserve it, in proportion to the crime; deterrence looks forward and aims to prevent future crime by the offender or by others.', '1 mark retribution; 1 mark deterrence; 1 mark backward v forward looking. [3]'),
        ('Explain why some offenders are given community orders rather than custodial sentences.', 'Community orders can address the causes of offending through requirements such as unpaid work, drug treatment or education, supporting rehabilitation and reparation while avoiding the negative effects and cost of prison.', '1 mark: rehabilitation/reparation; 1 mark: avoids prison costs/negative effects. [2]'),
        ('Explain the purpose of the either-way plea before venue and mode of trial procedure.', 'The defendant indicates a plea; if not guilty, magistrates decide whether the case is suitable for summary trial, and the defendant can still elect Crown Court trial by jury.', '1 mark: plea before venue; 1 mark: magistrates decide suitability; 1 mark: right to elect jury trial. [3]')],
  cmps=[('a summary offence', 'an indictable offence', ['summary offences are tried only in the magistrates\' court, indictable offences only in the Crown Court', 'summary offences are minor, e.g. common assault; indictable offences are the most serious, e.g. murder', 'indictable offences carry much higher maximum sentences']),
        ('individual deterrence', 'general deterrence', ['individual deterrence aims to stop the offender reoffending, general deterrence aims to discourage other people', 'general deterrence may justify an exemplary sentence'])],
  scen=[dict(facts='{A}, aged {age}, has been charged with {off}. {A} {hist}.',
             slots={'age': ['19', '24', '35', '52'],
                    'off': [('robbery of a petrol station', 'indictable-only', 'the Crown Court'), ('theft from a shop', 'triable either way', 'the magistrates\' court or the Crown Court'), ('common assault', 'summary', 'the magistrates\' court')],
                    'hist': ['has two previous convictions for failing to attend court', 'has a job and lives with family', 'has no fixed address and has threatened a witness']},
             issue='bail and the classification of offences', wrong=['the doctrine of precedent', 'the small claims track', 'the Practice Statement 1966'],
             ask='Advise whether {A} is likely to be granted bail and in which court the case will be tried.',
             law=['Bail Act 1976 s4: presumption in favour of bail', 'bail may be refused if there are substantial grounds to believe the defendant would fail to surrender, commit offences or interfere with witnesses', 'conditions such as curfew, residence or a surety can be imposed', 'offences are classified as summary, triable either way and indictable'],
             apply=['{A} {hist}, which is relevant to the risk factors', '{off} is {off_1}, so it will be tried in {off_2}'],
             concl='the presumption of bail applies to {A}, subject to the risks shown; the case will be tried in {off_2}'),
        dict(facts='{A} has pleaded guilty to {off}. {A} {hist}. The judge is considering the appropriate sentence.',
             slots={'off': ['burglary of a home', 'assault occasioning actual bodily harm in a nightclub', 'dangerous driving'],
                    'hist': ['is 20, has no previous convictions and is addicted to drugs', 'has several previous convictions for similar offences', 'has offered to pay compensation to the victim']},
             issue='the aims of sentencing under the Sentencing Act 2020', wrong=['the grounds for refusing bail', 'the jurisdiction of the county court', 'the exceptions in Young v Bristol Aeroplane'],
             ask='Explain which aims of sentencing the judge should consider for {A}.',
             law=['Sentencing Act 2020 s57: punishment, reduction of crime (including deterrence), reform and rehabilitation, protection of the public and reparation', 'aggravating factors (e.g. previous convictions) and mitigating factors (e.g. guilty plea, remorse) are considered', 'a guilty plea earns a reduction of up to one third'],
             apply=['{A} {hist}', 'this points towards rehabilitation, reparation or protection/deterrence as appropriate', 'the early guilty plea reduces the sentence'],
             concl='the sentence should balance punishment with the aim most relevant to {A}\'s circumstances, reduced for the guilty plea')],
  ev=[('Evaluate whether the aims of sentencing can all be achieved at the same time.', ['a community order can combine punishment, rehabilitation and reparation', 'custody can protect the public and punish'],
       ['the aims conflict: deterrence may require harsh sentences while rehabilitation favours community measures', 'prison has high reoffending rates, undermining reform', 'evidence that deterrence works is weak'],
       ['Sentencing Act 2020 s57', 'Bail Act 1976'], 'the aims often conflict, so judges must prioritise according to the offence and offender')])

T(4, 'Tribunals and alternative dispute resolution: negotiation, mediation, conciliation and arbitration', area='tribunals and ADR',
  defs=[('alternative dispute resolution', 'Methods of resolving disputes without going to court, such as negotiation, mediation, conciliation and arbitration.'),
        ('mediation', 'A form of ADR in which a neutral mediator helps the parties to reach their own agreement but does not suggest solutions or impose a decision.'),
        ('conciliation', 'A form of ADR in which a neutral conciliator plays an active role, suggesting possible solutions to help the parties reach agreement, e.g. ACAS in employment disputes.'),
        ('arbitration', 'A form of ADR in which the parties agree to have their dispute decided by an independent arbitrator, whose decision (award) is legally binding.'),
        ('negotiation', 'A form of ADR in which the parties, or their lawyers, discuss the dispute directly and try to reach a settlement without a third party.'),
        ('tribunal', 'A specialist body outside the ordinary court system that decides disputes in particular areas, such as employment, immigration or social security.')],
  mcqs=[('Which Act reformed the tribunal system into a First-tier Tribunal and an Upper Tribunal?', 'Tribunals, Courts and Enforcement Act 2007', ['Arbitration Act 1996', 'Courts and Legal Services Act 1990', 'Constitutional Reform Act 2005'], 'The TCEA 2007 created the two-tier structure.'),
        ('Which form of ADR produces a legally binding decision made by an independent third party?', 'Arbitration', ['Mediation', 'Negotiation', 'Conciliation'], 'Arbitration awards are binding and enforceable under the Arbitration Act 1996.'),
        ('Which body provides conciliation in employment disputes?', 'ACAS', ['The Law Commission', 'The Bar Council', 'The Criminal Cases Review Commission'], 'ACAS (Advisory, Conciliation and Arbitration Service).'),
        ('In which case did the Court of Appeal penalise a successful party in costs for unreasonably refusing to consider ADR?', 'Dunnett v Railtrack (2002)', ['R v Dobson (2011)', 'Carlill v Carbolic Smoke Ball Co (1893)', 'Pepper v Hart (1993)'], 'Railtrack won but was denied its costs for refusing ADR.'),
        ('Who normally sits in an employment tribunal hearing an unfair dismissal claim?', 'An employment judge, sometimes with two lay members', ['A jury of twelve', 'Three Supreme Court Justices', 'A single magistrate'], 'Employment tribunals use an employment judge, sometimes with lay members from employer and employee backgrounds.')],
  cases=[('Dunnett v Railtrack plc (2002)', 'Railtrack won an appeal but had refused the Court of Appeal\'s suggestion to try ADR', 'a party who unreasonably refuses ADR may be penalised in costs even if it wins'),
         ('Halsey v Milton Keynes General NHS Trust (2004)', 'a hospital trust refused the claimant\'s offer of mediation in a clinical negligence claim', 'courts should encourage ADR, and unreasonable refusal can be penalised in costs, but at that time courts could not compel parties to mediate'),
         ('Churchill v Merthyr Tydfil County Borough Council (2023)', 'a homeowner sued a council over Japanese knotweed without first using the council\'s complaints procedure', 'courts may lawfully order parties to engage in ADR, provided this does not impair the right to a fair trial and is proportionate')],
  ars=[('An arbitrator\'s award is legally binding on the parties.', 'Arbitration is governed by the Arbitration Act 1996.', 'B'),
       ('A mediator imposes a solution on the parties.', 'Mediation is a form of ADR using a neutral third party.', 'D'),
       ('Courts can now order parties to engage in ADR.', 'In Churchill v Merthyr Tydfil CBC (2023) the Court of Appeal held that ordering ADR can be lawful.', 'A')],
  exps=[('Explain two advantages of mediation compared with going to court.', 'It is cheaper and quicker; it is private and informal; the parties keep control of the outcome; and it can preserve relationships, e.g. between neighbours or business partners.', '2 × (1 mark advantage, 1 mark explanation). [4]'),
        ('Explain two disadvantages of arbitration.', 'Arbitrators can be expensive, especially in commercial cases; there are very limited rights of appeal; an unrepresented party may be at a disadvantage; and decisions do not create precedents.', '2 × (1 mark disadvantage, 1 mark explanation). [4]'),
        ('Explain the difference between mediation and conciliation.', 'In mediation the neutral third party facilitates discussion but does not suggest solutions; in conciliation the third party plays a more active role and suggests possible solutions.', '1 mark mediation; 1 mark conciliation; 1 mark contrast of role. [3]'),
        ('Explain two advantages of tribunals over courts.', 'They are cheaper (often no fees, no need for lawyers), quicker, less formal and decided by panels with specialist expertise.', '2 × (1 mark advantage, 1 mark explanation). [4]')],
  cmps=[('mediation', 'arbitration', ['a mediator helps the parties reach their own agreement, an arbitrator makes a binding decision', 'mediation is voluntary and non-binding until agreed, an arbitration award is enforceable', 'arbitration is more formal and closer to a court hearing']),
        ('tribunals', 'courts', ['tribunals are specialist and less formal, courts deal with a wide range of cases formally', 'tribunals have panels with lay experts, courts have judges (and sometimes juries)', 'tribunals are usually cheaper and quicker'])],
  scen=[dict(facts='{A} and {B} are {rel} in {city} who are in dispute about {dispute}. They want to {want}.',
             slots={'rel': [('neighbours', 'mediation'), ('business partners', 'mediation or conciliation'), ('a supplier and a manufacturer under a contract containing an arbitration clause', 'arbitration')],
                    'dispute': ['a boundary fence and overhanging trees', 'money owed under a contract', 'the quality of goods supplied'],
                    'want': ['avoid the cost of court proceedings', 'keep the dispute private', 'resolve the dispute quickly']},
             issue='the choice of an appropriate method of alternative dispute resolution', wrong=['an appeal by way of case stated', 'the small claims track only', 'judicial review'],
             ask='Advise {A} and {B} on the most suitable method of resolving their dispute.',
             law=['negotiation: the parties settle directly', 'mediation: a neutral mediator facilitates agreement; conciliation: the conciliator suggests solutions', 'arbitration: a binding award under the Arbitration Act 1996, often required by a contract clause', 'courts encourage ADR and may penalise unreasonable refusal in costs (Dunnett v Railtrack; Halsey) or order ADR (Churchill 2023)'],
             apply=['as {rel}, the most suitable method is likely to be {rel_1}', 'this meets their wish to {want}', 'if ADR fails they can still go to court'],
             concl='{rel_1} is likely to be the most suitable method for {A} and {B}'),
        dict(facts='{A} was dismissed by {B} Ltd after {yrs} years of employment and believes the dismissal was unfair.',
             slots={'yrs': ['three', 'five', 'eight']},
             issue='the role of tribunals and conciliation in employment disputes', wrong=['trial in the Crown Court', 'arbitration under a commercial contract', 'the small claims track'],
             ask='Advise {A} on how the claim could be resolved.',
             law=['claims for unfair dismissal are heard by employment tribunals', 'early conciliation through ACAS is normally required before a claim is made', 'tribunals are specialist, less formal and cheaper than courts; appeals go to the Employment Appeal Tribunal'],
             apply=['{A} should first contact ACAS for early conciliation', 'if that fails, {A} can bring a claim in the employment tribunal'],
             concl='{A} should use ACAS early conciliation and, if needed, bring a claim before an employment tribunal')],
  ev=[('Evaluate the advantages and disadvantages of using alternative dispute resolution rather than the courts.', ['cheaper and quicker', 'private and informal', 'parties keep control; relationships preserved', 'specialist arbitrators'],
       ['imbalance of power between parties', 'no precedent and limited appeal', 'arbitration can be expensive', 'mediated agreements may not be enforceable'],
       ['Arbitration Act 1996', 'Dunnett v Railtrack (2002)', 'Halsey v Milton Keynes (2004)', 'Churchill v Merthyr Tydfil CBC (2023)'], 'ADR is often preferable for private disputes but courts remain necessary for complex cases and precedent'),
      ('Evaluate the effectiveness of tribunals in resolving disputes.', ['cheap, quick and informal', 'specialist expertise', 'two-tier system under the TCEA 2007 improves consistency'],
       ['lack of legal aid makes representation unequal', 'delays have grown', 'fees and complexity in some tribunals'],
       ['Tribunals, Courts and Enforcement Act 2007'], 'tribunals are generally effective but are limited by lack of funding and representation')])

# =====================================================================================
# 5 Legal personnel
# =====================================================================================

T(5, 'The legal profession: solicitors and barristers, training and roles', area='the legal profession',
  defs=[('solicitor', 'A qualified lawyer who gives legal advice to clients, drafts documents, handles transactions and litigation, and may act as an advocate; regulated by the Solicitors Regulation Authority.'),
        ('barrister', 'A qualified lawyer who specialises in advocacy and giving expert opinions, usually self-employed in chambers and regulated by the Bar Standards Board.'),
        ('cab-rank rule', 'The professional rule that a self-employed barrister must accept a case within their area of expertise if they are available and a proper fee is offered, regardless of who the client is.'),
        ('King\'s Counsel', 'A senior barrister or solicitor-advocate appointed for excellence in advocacy in the higher courts, sometimes described as "taking silk".'),
        ('pupillage', 'The practical training period, normally one year, that a trainee barrister spends working under the supervision of an experienced barrister (pupil supervisor).'),
        ('Solicitors Qualifying Examination', 'The centralised assessment (SQE1 and SQE2) that, together with a degree or equivalent and two years\' qualifying work experience, leads to qualification as a solicitor.')],
  mcqs=[('Which body regulates solicitors?', 'The Solicitors Regulation Authority', ['The Law Society', 'The Bar Standards Board', 'The Judicial Appointments Commission'], 'The SRA regulates; the Law Society represents solicitors.'),
        ('Which of these must a trainee barrister join?', 'One of the four Inns of Court', ['The Law Society', 'A firm of solicitors', 'The Crown Prosecution Service'], 'Lincoln\'s Inn, Gray\'s Inn, Inner Temple and Middle Temple.'),
        ('In which case did the House of Lords remove the immunity of advocates from negligence claims?', 'Arthur J S Hall & Co v Simons (2000)', ['Rondel v Worsley (1969)', 'Donoghue v Stevenson (1932)', 'Pepper v Hart (1993)'], 'Hall v Simons overruled the immunity recognised in Rondel v Worsley.'),
        ('Which Act allowed alternative business structures in which lawyers and non-lawyers can jointly own legal businesses?', 'Legal Services Act 2007', ['Courts and Legal Services Act 1990', 'Access to Justice Act 1999', 'Constitutional Reform Act 2005'], 'The LSA 2007 created the Legal Services Board and ABSs.'),
        ('Which Act first allowed solicitors to obtain rights of audience in the higher courts?', 'Courts and Legal Services Act 1990', ['Legal Services Act 2007', 'Juries Act 1974', 'Bail Act 1976'], 'The CLSA 1990, extended by the Access to Justice Act 1999.')],
  cases=[('Arthur J S Hall & Co v Simons (2000)', 'clients sued their solicitors for negligence in handling litigation, and the solicitors claimed advocates\' immunity', 'advocates (barristers and solicitors) no longer have immunity from being sued for negligence in the conduct of cases'),
         ('Rondel v Worsley (1969)', 'a client sued his barrister for negligence in the conduct of his criminal defence', 'barristers were immune from negligence claims for work in court; this was later overruled in Hall v Simons (2000)')],
  ars=[('A barrister must normally accept a case if available and offered a proper fee.', 'The cab-rank rule ensures that unpopular clients can obtain representation.', 'A'),
       ('Members of the public can never instruct a barrister directly.', 'Most barristers are instructed by solicitors.', 'D')],
  exps=[('Describe the training required to qualify as a solicitor.', 'A degree (in any subject) or equivalent; passing SQE1 (legal knowledge) and SQE2 (practical skills); two years of qualifying work experience; and satisfying the SRA\'s character and suitability requirements.', '1 mark degree; 1 mark SQE1 and SQE2; 1 mark qualifying work experience; 1 mark character and suitability. [4]'),
        ('Describe the training required to qualify as a barrister.', 'An academic stage (law degree or non-law degree plus conversion course), a vocational Bar course, membership of an Inn of Court and call to the Bar, then pupillage of about a year before seeking tenancy in chambers.', '1 mark academic; 1 mark Bar course and Inn; 1 mark pupillage; 1 mark tenancy/call. [4]'),
        ('Explain two differences between the work of solicitors and barristers.', 'Solicitors deal directly with clients and handle a wide range of legal work such as conveyancing, wills and litigation, mostly in firms; barristers specialise in advocacy and opinions, usually self-employed in chambers and instructed by solicitors.', '2 × (1 mark difference, 1 mark explanation). [4]'),
        ('Explain why the Legal Services Act 2007 was introduced.', 'Following the Clementi review, it aimed to increase competition and consumer protection by creating the Legal Services Board, the Legal Ombudsman and alternative business structures.', '1 mark: competition/consumer protection; 1 mark: LSB, Ombudsman or ABSs. [2]')],
  cmps=[('solicitors', 'barristers', ['solicitors usually work in firms, barristers are usually self-employed in chambers', 'solicitors deal directly with clients, barristers are usually instructed by solicitors', 'solicitors are regulated by the SRA, barristers by the Bar Standards Board', 'barristers are subject to the cab-rank rule'])],
  ev=[('Evaluate the extent to which the legal profession is accessible to people from all backgrounds.', ['the SQE allows qualification through apprenticeships and work experience', 'scholarships from Inns of Court', 'increasing numbers of women and ethnic minority solicitors'],
       ['high cost of training and unpaid work experience', 'shortage of pupillages', 'senior ranks (partners, KCs) remain dominated by privately educated white men'],
       ['Legal Services Act 2007', 'Solicitors Qualifying Examination', 'Arthur J S Hall & Co v Simons (2000)'], 'access is improving but significant barriers remain at entry and in senior positions'),
      ('"There is no longer any need for separate professions of solicitors and barristers." Discuss.', ['overlapping roles: solicitor-advocates, direct access to barristers', 'fusion could reduce costs to clients', 'duplication of work'],
       ['barristers provide specialist advocacy', 'cab-rank rule protects access to justice', 'small firms can access specialist barristers without employing them'],
       ['Courts and Legal Services Act 1990', 'Access to Justice Act 1999', 'Legal Services Act 2007'], 'the professions are converging, but there are still benefits in a specialist independent Bar')])

T(5, 'The judiciary: types of judge, appointment, independence and the separation of powers', area='the judiciary',
  defs=[('judicial independence', 'The principle that judges should be free to decide cases impartially according to the law, without pressure from the government, Parliament, the parties or the media.'),
        ('separation of powers', 'The theory (associated with Montesquieu) that the legislative, executive and judicial functions of the state should be held by separate bodies to prevent abuse of power.'),
        ('security of tenure', 'Protection for senior judges, who hold office during good behaviour and can be removed only by the monarch following an address by both Houses of Parliament.'),
        ('Judicial Appointments Commission', 'The independent body created by the Constitutional Reform Act 2005 to select candidates for judicial office in England and Wales solely on merit.'),
        ('superior judges', 'Judges in the High Court and above: High Court judges, Lords and Lady Justices of Appeal, and Justices of the Supreme Court.')],
  mcqs=[('Which Act created the Judicial Appointments Commission and the Supreme Court?', 'Constitutional Reform Act 2005', ['Courts Act 1971', 'Tribunals, Courts and Enforcement Act 2007', 'Human Rights Act 1998'], 'The CRA 2005 reformed the role of the Lord Chancellor and created the JAC and Supreme Court.'),
        ('Which of these is an inferior judge?', 'A circuit judge', ['A Justice of the Supreme Court', 'A Lord Justice of Appeal', 'A High Court judge'], 'Inferior judges include circuit judges, recorders and district judges.'),
        ('Who is the head of the judiciary in England and Wales?', 'The Lady or Lord Chief Justice', ['The Lord Chancellor', 'The Prime Minister', 'The Attorney-General'], 'Since the CRA 2005 the Lord Chief Justice is head of the judiciary.'),
        ('Which case shows that a judge must not sit where there is an appearance of bias?', 'R v Bow Street Magistrates, ex p Pinochet Ugarte (No 2) (1999)', ['Sirros v Moore (1975)', 'Pepper v Hart (1993)', 'Davis v Johnson (1979)'], 'Lord Hoffmann\'s links with Amnesty International led to the decision being set aside.'),
        ('What is the compulsory retirement age for judges following the Public Service Pensions and Judicial Offices Act 2022?', '75', ['60', '65', '80'], 'The 2022 Act raised the retirement age from 70 to 75.')],
  cases=[('R v Bow Street Metropolitan Stipendiary Magistrate, ex p Pinochet Ugarte (No 2) (1999)', 'Lord Hoffmann sat in the House of Lords case on extraditing General Pinochet without disclosing his links to Amnesty International, which was a party', 'a judge must not sit where there is a real possibility or appearance of bias; the decision was set aside and reheard'),
         ('Sirros v Moore (1975)', 'a judge wrongly ordered the detention of a man, who then sued the judge', 'judges have immunity from being sued for acts done in their judicial capacity in good faith, which protects independence')],
  ars=[('Senior judges cannot be dismissed by the government.', 'Superior judges can be removed only by the monarch on an address by both Houses of Parliament.', 'A'),
       ('The Lord Chancellor still sits as a judge in the Supreme Court.', 'The Constitutional Reform Act 2005 removed the Lord Chancellor\'s judicial role.', 'D'),
       ('Judges\' salaries are paid from the Consolidated Fund.', 'Paying salaries without an annual parliamentary vote helps protect judicial independence.', 'A')],
  exps=[('Explain three ways in which judicial independence is protected.', 'Security of tenure for superior judges; salaries paid from the Consolidated Fund; judicial immunity from suit (Sirros v Moore); appointment by the independent JAC; the duty on ministers in s3 CRA 2005 to uphold independence.', '1 mark per method explained, up to 3. [3]'),
        ('Describe the process for appointing High Court judges.', 'Vacancies are advertised by the Judicial Appointments Commission; candidates need relevant legal qualifications and experience (7 years post-qualification); they complete application forms, qualifying tests and interviews/role plays; the JAC selects on merit and good character and recommends to the Lord Chancellor.', '1 mark advertisement/JAC; 1 mark eligibility; 1 mark selection process; 1 mark merit and recommendation. [4]'),
        ('Explain the role of judges in the separation of powers.', 'Judges form the judiciary, which should be separate from the legislature and executive; they interpret and apply the law, and through judicial review check that the executive acts within its powers.', '1 mark: judiciary as separate branch; 1 mark: check on executive through judicial review. [2]')],
  cmps=[('superior judges', 'inferior judges', ['superior judges sit in the High Court and above, inferior judges in the Crown Court, county court and magistrates\' court', 'superior judges can only be removed by an address of both Houses, inferior judges can be dismissed by the Lord Chancellor with the agreement of the Lord Chief Justice for incapacity or misbehaviour'])],
  scen=[dict(facts='Judge {A} is due to hear a case involving {party}. It emerges that {link}.',
             slots={'party': ['a large pharmaceutical company', 'an environmental charity', 'a political campaign group'],
                    'link': ['the judge owns shares in one of the parties', 'the judge is an unpaid director of a charity linked to one of the parties', 'the judge\'s spouse works for one of the parties']},
             issue='judicial impartiality and independence', wrong=['the cab-rank rule', 'the Practice Statement 1966', 'the eligibility rules for jury service'],
             ask='Advise whether Judge {A} should hear the case.',
             law=['judges must be impartial and independent', 'a judge must not sit if there is a real possibility or appearance of bias (Pinochet (No 2) 1999)', 'judges take an oath to act without fear or favour'],
             apply=['because {link}, a fair-minded observer could think there is a real possibility of bias', 'as in Pinochet, the decision could be set aside if the judge sits'],
             concl='Judge {A} should declare the interest and not hear the case')],
  ev=[('Evaluate the extent to which judges in England and Wales are independent.', ['security of tenure and salary protection', 'appointment by the independent JAC', 'judicial immunity (Sirros v Moore)', 'Lord Chancellor\'s role reduced by CRA 2005'],
       ['the Lord Chancellor still has some role in appointments', 'judges may be influenced by their backgrounds', 'media and political criticism (e.g. "Enemies of the People" headlines in 2016)'],
       ['Constitutional Reform Act 2005', 'Pinochet (No 2) (1999)', 'Sirros v Moore (1975)'], 'the judiciary is largely independent, especially since 2005, although some concerns remain'),
      ('Evaluate whether the judicial appointments process produces a judiciary that reflects society.', ['the JAC selects on merit with transparent procedures', 'diversity has improved, with more women and ethnic minority judges'],
       ['senior judges remain mostly white, male and privately educated', 'eligibility requirements favour barristers', 'part-time and career breaks are harder to combine with judicial careers'],
       ['Constitutional Reform Act 2005', 'Tribunals, Courts and Enforcement Act 2007'], 'the process is fairer than before, but the senior judiciary is still not representative')])

T(5, 'Lay magistrates: selection, role and evaluation', area='lay magistrates',
  defs=[('lay magistrate', 'An unpaid volunteer, also called a Justice of the Peace, with no formal legal qualifications, who sits in the magistrates\' court to hear criminal and some civil and family cases.'),
        ('legal adviser', 'A qualified lawyer in the magistrates\' court who advises magistrates on law and procedure but must not take part in deciding guilt or sentence.'),
        ('local advisory committee', 'A committee that recruits, interviews and recommends candidates for appointment as lay magistrates in its area.')],
  mcqs=[('How many lay magistrates normally sit together to hear a case?', 'Two or three', ['One', 'Twelve', 'Five'], 'A bench of two or three magistrates, advised by a legal adviser.'),
        ('Which of these is one of the six key qualities required of lay magistrates?', 'Sound judgement', ['A law degree', 'Five years\' experience as a police officer', 'Fluency in Latin'], 'The key qualities are good character, understanding and communication, social awareness, maturity and sound temperament, sound judgement, and commitment and reliability.'),
        ('What is the minimum number of half-day sittings a magistrate is expected to attend each year?', '26', ['5', '100', '200'], 'Magistrates must sit at least 13 days (26 half days) a year.'),
        ('Which statement about lay magistrates is correct?', 'They are unpaid volunteers, though they may claim expenses', ['They are paid a full-time salary', 'They must be qualified lawyers', 'They decide cases only in the Crown Court'], 'Lay magistrates are unpaid but may receive expenses and loss of earnings allowances.')],
  ars=[('Magistrates rely on a legal adviser for advice on the law.', 'Lay magistrates do not have formal legal qualifications.', 'A'),
       ('Lay magistrates hear all criminal cases.', 'Most criminal cases begin in the magistrates\' court.', 'D'),
       ('Using lay magistrates is cheaper than using professional judges.', 'Lay magistrates are unpaid.', 'A')],
  exps=[('Describe the selection and appointment of lay magistrates.', 'Vacancies are advertised; candidates apply to the local advisory committee; there are two interviews (testing the key qualities and judicial aptitude through case studies); the committee recommends suitable candidates; they are appointed by the Lady or Lord Chief Justice.', '1 mark advertising/application; 1 mark two interviews; 1 mark recommendation by advisory committee; 1 mark appointment by LCJ. [4]'),
        ('Explain three roles of lay magistrates in criminal cases.', 'Trying summary offences and either-way offences tried summarily; deciding bail and issuing warrants; sentencing within their limited powers; early administrative hearings and sending indictable cases to the Crown Court; sitting in the Crown Court on appeals.', '1 mark per role, up to 3. [3]'),
        ('Explain two advantages of using lay magistrates.', 'They are cheap because they are unpaid; they bring local knowledge and involve the community in justice; they come from a wider cross-section of society than professional judges; and few of their decisions are overturned.', '2 × (1 mark advantage, 1 mark explanation). [4]'),
        ('Explain two disadvantages of using lay magistrates.', 'Inconsistent sentencing between benches; they may be prosecution-minded or case-hardened; they are not fully representative (often older and middle-class); they may rely too heavily on the legal adviser.', '2 × (1 mark disadvantage, 1 mark explanation). [4]')],
  cmps=[('lay magistrates', 'district judges (magistrates\' courts)', ['lay magistrates are unpaid volunteers, district judges are paid professional lawyers', 'lay magistrates sit as a bench of two or three, district judges sit alone', 'district judges often hear the more complex or lengthy cases'])],
  scen=[dict(facts='{A}, aged {age}, is a {job} in {city} who wants to become a lay magistrate. {A} {extra}.',
             slots={'age': ['19', '34', '58', '73'], 'job': ['nurse', 'shop manager', 'teacher', 'self-employed plumber'],
                    'extra': ['has a conviction for a minor driving offence', 'works shifts and is worried about the time commitment', 'has no legal qualifications']},
             issue='the qualifications and selection of lay magistrates', wrong=['the eligibility rules for jury service', 'the training of barristers', 'the appointment of High Court judges'],
             ask='Advise {A} on the selection process and whether {A} is likely to be eligible.',
             law=['magistrates may be appointed from age 18 and retire at 75', 'no legal qualifications are needed, but candidates must show the six key qualities', 'serious convictions, bankruptcy and some occupations (e.g. police officers) may disqualify', 'they must sit at least 26 half-days a year; employers must allow reasonable time off'],
             apply=['{A} is {age}, within the age limits', '{A} {extra}, which must be considered', 'the advisory committee will interview {A}'],
             concl='{A} is likely to be eligible to apply, subject to showing the key qualities and passing the interviews')],
  ev=[('Evaluate the use of lay magistrates in the criminal justice system.', ['cheap', 'local knowledge', 'lay involvement and wide cross-section', 'few successful appeals'],
       ['inconsistent sentencing', 'prosecution bias and case-hardening', 'not fully representative', 'reliance on legal adviser', 'slower than district judges'],
       ['Courts Act 2003', 'six key qualities'], 'lay magistrates provide a cheap and democratic system that works well for most minor cases, despite concerns about consistency and representation')])

T(5, 'Juries: selection, role and evaluation', area='juries',
  defs=[('jury', 'A group of twelve randomly selected members of the public who decide the verdict (guilty or not guilty) on the facts in a Crown Court trial.'),
        ('majority verdict', 'A verdict reached by at least 10 out of 12 jurors (or 10 of 11, or 9 of 10), allowed only after the jury has deliberated for at least two hours.'),
        ('jury vetting', 'Checking potential jurors\' backgrounds, either routine police checks for criminal records or, exceptionally, wider checks in national security cases.'),
        ('jury equity', 'The power of a jury to acquit a defendant according to its own sense of fairness, even where the law suggests the defendant is guilty, as in R v Ponting (1985).')],
  mcqs=[('Which Act sets out the qualifications for jury service?', 'Juries Act 1974', ['Courts Act 1971', 'Criminal Justice Act 1988', 'Bail Act 1976'], 'The Juries Act 1974, as amended (e.g. by the Criminal Justice Act 2003).'),
        ('What are the age limits for jury service?', '18 to 75', ['16 to 65', '21 to 70', '18 to 60'], 'Jurors must be aged 18-75 and registered to vote.'),
        ('Which case established that judges cannot direct a jury to convict and that jurors cannot be punished for their verdict?', 'Bushell\'s Case (1670)', ['R v Young (1995)', 'R v Mirza (2004)', 'R v Twomey (2009)'], 'Bushell\'s Case established the independence of the jury.'),
        ('In which case did jurors use a ouija board to try to contact the murder victim?', 'R v Young (Stephen) (1995)', ['R v Ponting (1985)', 'Attorney-General v Fraill (2011)', 'R v Karakaya (2005)'], 'The conviction was quashed because the incident happened in a hotel, outside the jury room.'),
        ('Which was the first criminal trial in England to be held without a jury under s44 Criminal Justice Act 2003 because of jury tampering?', 'R v Twomey (2009)', ['R v Pryce (2013)', 'R v Mirza (2004)', 'R v Abdroikov (2007)'], 'The Heathrow robbery trial proceeded before a judge alone.')],
  cases=[('Bushell\'s Case (1670)', 'jurors who refused to convict Quakers of unlawful assembly were imprisoned by the judge', 'jurors cannot be punished for their verdict, establishing the independence of the jury'),
         ('R v Ponting (1985)', 'a civil servant leaked documents about the sinking of the Belgrano and the judge said there was no defence', 'the jury acquitted anyway, illustrating jury equity'),
         ('R v Young (Stephen) (1995)', 'some jurors in a murder trial used a ouija board in their hotel to try to contact the victim', 'the conviction was quashed and a retrial ordered because the misconduct took place outside the jury room'),
         ('R v Mirza (2004)', 'after conviction a juror wrote that other jurors had been racially biased against the defendant', 'courts cannot investigate what was said in the jury room because of jury secrecy'),
         ('Attorney-General v Fraill (2011)', 'a juror contacted the defendant on Facebook during a drugs trial', 'the juror was jailed for contempt of court, showing the problem of jurors using the internet'),
         ('R v Twomey (2009)', 'previous trials of men accused of a robbery at Heathrow had collapsed because of attempted jury tampering', 'a trial may be held without a jury where there is a real and present danger of jury tampering (s44 CJA 2003)')],
  ars=[('Jury deliberations are secret.', 'It is an offence for jurors to disclose what was said in the jury room.', 'A'),
       ('Juries give reasons for their verdicts.', 'Juries return a general verdict of guilty or not guilty.', 'D'),
       ('Jurors are chosen at random from the electoral register.', 'Random selection is intended to produce a representative and impartial jury.', 'A')],
  exps=[('Explain who is disqualified from jury service.', 'People on bail; those sentenced to life imprisonment, imprisonment for public protection or five years or more (disqualified for life); those who have served a prison sentence or community order in the last ten years; and mentally disordered persons lacking capacity.', '1 mark per correct category, up to 3. [3]'),
        ('Describe how jurors are selected for a Crown Court trial.', 'Names are chosen at random from the electoral register by the Jury Central Summoning Bureau; those summoned may be excused or have service deferred; at court a panel is chosen by ballot and 12 are sworn in, subject to challenges for cause and the prosecution\'s right to stand by.', '1 mark random from electoral register; 1 mark summons/excusal/deferral; 1 mark ballot at court; 1 mark challenges. [4]'),
        ('Explain two advantages of jury trial.', 'Public confidence and participation in justice; jury equity allows acquittal against unjust laws (Ponting); decisions by 12 people of varied backgrounds reduce individual bias; secrecy allows free discussion.', '2 × (1 mark advantage, 1 mark explanation). [4]'),
        ('Explain two disadvantages of jury trial.', 'Jurors may not understand complex evidence such as in fraud cases; bias or prejudice (Mirza); use of the internet (Fraill, Karakaya); perverse verdicts; jury tampering (Twomey); cost and time.', '2 × (1 mark disadvantage, 1 mark explanation/case). [4]')],
  cmps=[('juries', 'lay magistrates', ['juries decide only the verdict, magistrates decide verdict and sentence', 'jurors are chosen at random and serve once, magistrates apply, are selected and serve for years', 'juries sit in the Crown Court, magistrates in the magistrates\' court'])],
  scen=[dict(facts='{A}, aged {age}, has received a summons for jury service at {city} Crown Court. {A} {extra}.',
             slots={'age': ['17', '22', '45', '76'],
                    'extra': [('was released from a three-year prison sentence six years ago', 'disqualified, as someone who has served a prison sentence in the last ten years'), ('is currently on bail for a theft charge', 'disqualified while on bail'), ('has a holiday booked for the week of the trial', 'not disqualified but may ask to defer service'), ('is a police officer', 'eligible, though the trial judge must consider any risk of bias (R v Abdroikov 2007)')]},
             issue='eligibility for and selection of jurors', wrong=['the selection of lay magistrates', 'the appointment of judges', 'the cab-rank rule'],
             ask='Advise {A} whether {A} can or must serve on the jury.',
             law=['Juries Act 1974: aged 18-75, on the electoral register and resident in the UK for at least five years since age 13', 'disqualified: those on bail, those with certain sentences (five years or more for life; any custody or community order in the last ten years) and mentally disordered persons', 'excusal and deferral are discretionary; police officers and lawyers are eligible since the CJA 2003'],
             apply=['{A} is {age}; jurors must be 18-75', '{A} {extra}, so {A} is {extra_1}'],
             concl='if within the age range, {A} is {extra_1}; anyone outside 18-75 cannot serve')],
  ev=[('Evaluate the advantages and disadvantages of using juries in criminal trials.', ['public confidence and participation', 'jury equity (Ponting)', 'random selection reduces bias', 'secrecy allows free discussion'],
       ['jurors may not understand complex evidence', 'racial or other bias (Mirza)', 'internet research and social media (Fraill)', 'jury tampering (Twomey)', 'perverse verdicts and no reasons given'],
       ['Juries Act 1974', 'R v Ponting (1985)', 'R v Mirza (2004)', 'Attorney-General v Fraill (2011)', 'R v Twomey (2009)', 'R v Young (1995)'], 'juries are an important democratic safeguard, though reforms such as better guidance on the internet are needed'),
      ('"Jury trial should be abolished for complex fraud cases." Discuss.', ['jurors may not understand complex financial evidence', 'trials are long and costly', 'collapse of long fraud trials'],
       ['research suggests jurors understand more than assumed', 'loss of democratic involvement', 'judge-alone trials may be less trusted'],
       ['Criminal Justice Act 2003 s43 (never brought into force and later repealed)', 'Roskill Committee 1986', 'R v Twomey (2009)'], 'abolition is arguable for the most complex cases, but better case management may be preferable')])

# =====================================================================================
# 6 Criminal law: general elements of criminal liability
# =====================================================================================

T(6, 'Actus reus: voluntary acts, omissions and duties to act', area='actus reus and omissions',
  defs=[('actus reus', 'The physical element of a crime: a voluntary act, omission or state of affairs, together with any required circumstances and consequences.'),
        ('omission', 'A failure to act, which can form the actus reus of a crime only where the defendant was under a legal duty to act.'),
        ('voluntary act', 'An act done by the conscious choice of the defendant; involuntary acts, such as reflex actions, cannot form the actus reus (Hill v Baxter).'),
        ('state of affairs offence', 'An offence where the actus reus is being in a particular situation rather than doing an act, e.g. being found drunk on a highway (R v Larsonneur; Winzar v Chief Constable of Kent).')],
  mcqs=[('In which case was a railway gatekeeper liable for failing to close a gate, causing a death, because of his contractual duty?', 'R v Pittwood (1902)', ['R v Miller (1983)', 'R v Dytham (1979)', 'R v Instan (1893)'], 'Contractual duty: Pittwood.'),
        ('Which case established a duty to act where the defendant has accidentally created a dangerous situation?', 'R v Miller (1983)', ['R v Gibbins and Proctor (1918)', 'R v Stone and Dobinson (1977)', 'R v Pittwood (1902)'], 'Miller fell asleep with a cigarette, woke to find the mattress on fire and did nothing.'),
        ('In R v Dytham (1979), a police officer was guilty because he failed to:', 'intervene when a man was being kicked to death nearby', ['close a railway crossing', 'feed his child', 'put out a fire he had started'], 'Duty arising from public office: misconduct in a public office.'),
        ('Which statement about omissions in English law is correct?', 'There is generally no duty to act, so a bystander who fails to rescue a stranger commits no offence', ['Everyone has a legal duty to rescue anyone in danger', 'Omissions can never be the actus reus of a crime', 'An omission is a crime only if it is intentional'], 'English law has no general duty to act; liability needs a recognised duty.')],
  cases=[('R v Pittwood (1902)', 'a railway crossing keeper went to lunch leaving the gate open, and a man crossing was hit by a train and killed', 'a duty to act can arise from a contract of employment, and the duty can be owed to the public as well as the employer'),
         ('R v Gibbins and Proctor (1918)', 'a father and his partner starved his seven-year-old daughter to death', 'parents owe a duty to their children because of their relationship, and someone who has assumed responsibility can also be liable'),
         ('R v Stone and Dobinson (1977)', 'the defendants took in Stone\'s anorexic sister, failed to care for her properly or get help, and she died', 'a duty arises where a person voluntarily assumes responsibility for someone who cannot care for themselves'),
         ('R v Miller (1983)', 'a squatter fell asleep with a lit cigarette, woke to find his mattress smouldering and moved to another room without raising the alarm', 'a person who creates a dangerous situation, even accidentally, is under a duty to take reasonable steps to limit the harm'),
         ('R v Dytham (1979)', 'an on-duty police officer watched a man being beaten to death outside a nightclub and drove away', 'a duty to act can arise from holding a public office'),
         ('R v Instan (1893)', 'a niece lived with and was supported by her elderly aunt, then failed to feed her or call for help when she became ill', 'a duty can arise from a relationship combined with voluntary assumption of care'),
         ('Hill v Baxter (1958)', 'a driver claimed he had become unconscious and could not remember the journey before a collision', 'the actus reus must be voluntary; examples of involuntary acts include a driver attacked by a swarm of bees'),
         ('Airedale NHS Trust v Bland (1993)', 'doctors asked whether they could withdraw feeding from a patient in a persistent vegetative state after the Hillsborough disaster', 'withdrawing treatment that is no longer in the patient\'s best interests is an omission, not an act, and is lawful because the duty ends')],
  ars=[('A stranger who watches a child drown in a shallow pond commits no criminal offence.', 'English law imposes no general duty to act.', 'A'),
       ('The actus reus of a crime must be voluntary.', 'In R v Pittwood (1902) a gatekeeper was liable for an omission.', 'B'),
       ('A doctor who withdraws treatment from a patient in a persistent vegetative state is guilty of murder.', 'In Airedale NHS Trust v Bland (1993) withdrawal of treatment was treated as an omission.', 'D')],
  exps=[('Explain why the actus reus of a crime must be voluntary.', 'Criminal liability is based on choice: it would be unjust to punish someone for movements they could not control, such as reflexes or acts during a seizure (Hill v Baxter).', '1 mark: idea of control/choice; 1 mark: example or case. [2]'),
        ('Explain three situations in which a duty to act arises.', 'Contract (R v Pittwood); special relationship (R v Gibbins and Proctor); voluntary assumption of care (R v Stone and Dobinson); creating a dangerous situation (R v Miller); public office (R v Dytham); statute (e.g. failing to provide a specimen of breath).', '1 mark per situation with case, up to 3. [3]'),
        ('Explain the significance of R v Miller (1983).', 'It established that a person who accidentally creates a dangerous situation and becomes aware of it is under a duty to take reasonable steps to deal with it; failure to do so can be the actus reus of a crime such as arson.', '1 mark facts; 1 mark principle; 1 mark significance (duty from creating danger). [3]')],
  cmps=[('an act', 'an omission', ['an act is a positive movement, an omission is a failure to act', 'any voluntary act can be an actus reus but an omission only where there is a legal duty to act'])],
  scen=[dict(facts='{A} {situation}. {B} {failure}, and {B2}.',
             slots={'situation': [('agreed, for payment, to work as a lifeguard at a hotel pool in {city}', 'contract', 'R v Pittwood (1902)'),
                                  ('took {E}, an elderly neighbour who could not look after herself, into the family home and promised to care for her', 'voluntary assumption of care', 'R v Stone and Dobinson (1977)'),
                                  ('dropped a lit match into a bin at work by accident and saw it start to smoulder', 'creation of a dangerous situation', 'R v Miller (1983)'),
                                  ('is the parent of {E}, aged four', 'special relationship', 'R v Gibbins and Proctor (1918)')],
                    'failure': ['did nothing to help when the danger arose', 'walked away without calling for help'],
                    'B2': ['{E} was seriously harmed as a result', 'serious harm resulted']},
             issue='liability for an omission where a duty to act exists', wrong=['transferred malice', 'oblique intention', 'the coincidence of actus reus and mens rea'],
             ask='Discuss whether {A} could be criminally liable for failing to act.',
             law=['there is no general duty to act in English law', 'a duty arises from contract (Pittwood), relationship (Gibbins and Proctor), voluntary assumption of care (Stone and Dobinson), creating danger (Miller) or public office (Dytham)', 'the omission must cause the harm and be accompanied by the required mens rea'],
             apply=['{A} {situation}, so a duty arises from {situation_1} ({situation_2})', 'failing to act was a breach of that duty', 'causation and mens rea must then be proved for the particular offence'],
             concl='{A} owed a duty to act based on {situation_1}, so the failure to act can form the actus reus'),
        dict(facts='{A} was driving along a road in {city} when {event}. {A}\'s car swerved and hit {B}, who was injured.',
             slots={'event': [('a swarm of bees flew in through the window and stung {A} repeatedly', 'involuntary'), ('{A} had a sudden epileptic seizure without any previous warning', 'involuntary'), ('{A} looked down to read a text message', 'voluntary')]},
             issue='whether the actus reus was voluntary', wrong=['a duty to act arising from contract', 'transferred malice', 'strict liability'],
             ask='Discuss whether {A}\'s conduct satisfies the actus reus requirement of an offence.',
             law=['the actus reus must be voluntary (Hill v Baxter 1958)', 'involuntary movements caused by an external force are not acts of the defendant', 'a voluntary but careless act is still an act'],
             apply=['here {event}', 'this movement was {event_1}'],
             concl='if the movement was involuntary {A} has no actus reus; if voluntary, {A} may be liable; here it was {event_1}')],
  ev=[('Evaluate the law on liability for omissions.', ['respects individual autonomy', 'duties are recognised in clear situations', 'avoids imposing heavy burdens on bystanders'],
       ['moral obligation to help strangers is ignored', 'the categories are uncertain (Stone and Dobinson)', 'distinction between acts and omissions can be artificial (Bland)', 'other countries (e.g. France) impose a duty to rescue'],
       ['R v Pittwood (1902)', 'R v Gibbins and Proctor (1918)', 'R v Stone and Dobinson (1977)', 'R v Miller (1983)', 'Airedale NHS Trust v Bland (1993)'], 'the law strikes a defensible balance, though the categories of duty are not always clear')])

T(6, 'Causation: factual and legal causation and intervening acts', area='causation',
  defs=[('factual causation', 'The "but for" test: the defendant\'s conduct is a factual cause of the result if the result would not have happened but for that conduct (R v White).'),
        ('legal causation', 'The requirement that the defendant\'s conduct is an operating and substantial (more than minimal) cause of the result, and that the chain of causation is not broken.'),
        ('novus actus interveniens', 'A new and intervening act, such as an unforeseeable act of a third party or of the victim, that breaks the chain of causation.'),
        ('thin skull rule', 'The rule that the defendant must take the victim as they find them, so the defendant is liable even if the victim suffers more serious harm because of a pre-existing condition or belief (R v Blaue).')],
  mcqs=[('In R v White (1910), why was the defendant not guilty of murder?', 'His mother died of a heart attack that would have happened anyway, so he was not the factual cause', ['He had no intention to kill', 'The poison was an omission', 'His mother consented'], 'He was guilty only of attempted murder.'),
        ('Which case held that negligent medical treatment will break the chain of causation only if it is "so independent" and "so potent" that the original wound is insignificant?', 'R v Cheshire (1991)', ['R v Jordan (1956)', 'R v Blaue (1975)', 'R v Pagett (1983)'], 'Cheshire narrowed Jordan, where treatment was "palpably wrong".'),
        ('In R v Roberts (1971), the victim jumped from a moving car. Why was the defendant liable?', 'Her reaction was reasonably foreseeable, so it did not break the chain', ['She had a thin skull', 'He had an intention to kill', 'She had consented to the risk'], 'Only a "daft" reaction breaks the chain (R v Williams 1992).'),
        ('Which case established that a victim\'s free, deliberate and informed decision to self-inject a drug breaks the chain of causation?', 'R v Kennedy (No 2) (2007)', ['R v Smith (1959)', 'R v Malcherek (1981)', 'R v Blaue (1975)'], 'The supplier was not liable for manslaughter.')],
  cases=[('R v White (1910)', 'the defendant put cyanide in his mother\'s drink but she died of an unrelated heart attack before the poison took effect', 'the defendant is not the factual cause of death if the result would have happened anyway (the "but for" test)'),
         ('R v Pagett (1983)', 'the defendant used his pregnant girlfriend as a human shield when shooting at police, and police shot and killed her', 'the reasonable reaction of a third party acting in self-defence does not break the chain of causation'),
         ('R v Smith (1959)', 'a soldier stabbed in a barracks fight was dropped twice on the way to the medical station and given poor treatment', 'if the original wound is still an operating and substantial cause of death, the defendant remains liable'),
         ('R v Jordan (1956)', 'a stab wound had almost healed when the hospital gave the victim a drug to which he was known to be allergic', 'palpably wrong medical treatment that is the sole cause of death can break the chain of causation'),
         ('R v Cheshire (1991)', 'a shooting victim died after a negligent tracheotomy, by which time the gunshot wounds were no longer life-threatening', 'negligent treatment breaks the chain only if it is so independent of the defendant\'s acts and so potent that his contribution is insignificant'),
         ('R v Blaue (1975)', 'a stabbing victim who was a Jehovah\'s Witness refused a blood transfusion and died', 'the defendant must take the victim as he finds her, including her religious beliefs (thin skull rule)'),
         ('R v Roberts (1971)', 'a woman jumped from a moving car to escape the driver\'s sexual advances and was injured', 'the victim\'s reaction does not break the chain if it was reasonably foreseeable; only a "daft" reaction does'),
         ('R v Kennedy (No 2) (2007)', 'the defendant prepared a syringe of heroin which the victim injected himself, and the victim died', 'the free, deliberate and informed act of a fully informed adult breaks the chain of causation'),
         ('R v Malcherek (1981)', 'victims of the defendants\' attacks were put on life-support machines, which doctors switched off when brain death was diagnosed', 'switching off a life-support machine after brain death does not break the chain of causation')],
  ars=[('A defendant is liable even if the victim dies because of an unusual medical condition.', 'The thin skull rule means the defendant must take the victim as they find them.', 'A'),
       ('Negligent medical treatment always breaks the chain of causation.', 'In R v Cheshire (1991) the defendant was liable despite negligent treatment.', 'D'),
       ('Factual causation alone is enough for liability.', 'The "but for" test identifies the factual cause of a result.', 'D')],
  exps=[('Explain the difference between factual and legal causation.', 'Factual causation uses the "but for" test (R v White); legal causation requires the defendant\'s act to be an operating and substantial cause (R v Smith) with no break in the chain.', '1 mark factual + case; 1 mark legal + case. [2]'),
        ('Explain when the act of a third party may break the chain of causation.', 'Where it is a free, deliberate and informed act that is not reasonably foreseeable; a reasonable act in self-defence or to escape does not break the chain (R v Pagett); negligent medical treatment rarely does (R v Cheshire) unless palpably wrong and the sole cause (R v Jordan).', '1 mark unforeseeable/free act; 1 mark Pagett; 1 mark medical treatment rule. [3]'),
        ('Explain the thin skull rule, using a case.', 'The defendant must take the victim as they find them, including physical conditions or beliefs, so the defendant is liable for the full consequences even if they are more serious than expected; in R v Blaue the victim\'s refusal of a blood transfusion did not break the chain.', '1 mark rule; 1 mark case. [2]')],
  cmps=[('R v Jordan (1956)', 'R v Cheshire (1991)', ['in Jordan the treatment was palpably wrong and the wound had almost healed, so the chain was broken; in Cheshire the treatment was negligent but did not break the chain', 'Cheshire set a stricter test: treatment must be so independent and potent that the original act is insignificant'])],
  scen=[dict(facts='{A} stabbed {B} during an argument in {city}. {B} was taken to hospital, where {med}. {B} died.',
             slots={'med': [('a junior doctor negligently failed to notice that {B} had developed a chest infection', 'negligent treatment that is unlikely to break the chain (R v Cheshire; R v Smith)', 'liable for the death'),
                            ('{B} refused a blood transfusion because of religious beliefs', 'the thin skull rule (R v Blaue)', 'liable for the death'),
                            ('after the wound had healed, {B} was given a large dose of a drug to which {B} was known to be allergic', 'palpably wrong treatment that may break the chain (R v Jordan)', 'possibly not liable for the death, only for the stabbing'),
                            ('{B} was declared brain-dead and the life-support machine was switched off', 'switching off life support does not break the chain (R v Malcherek)', 'liable for the death')]},
             issue='factual and legal causation and intervening acts', wrong=['the coincidence of actus reus and mens rea', 'liability for omissions', 'strict liability'],
             ask='Discuss whether {A} caused {B}\'s death.',
             law=['factual causation: but for the defendant\'s act the result would not have occurred (R v White)', 'legal causation: the act must be an operating and substantial cause (R v Smith)', 'medical treatment breaks the chain only if so independent and potent (R v Cheshire), e.g. palpably wrong (R v Jordan)', 'the thin skull rule applies (R v Blaue)'],
             apply=['but for the stabbing {B} would not have been in hospital, so factual causation is satisfied', 'here {med}, which raises {med_1}', 'so {A} is {med_2}'],
             concl='{A} is {med_2}',
             owrong=['{A} cannot be liable because doctors are always responsible once a victim is in hospital', '{A} is not the factual cause because others were involved', '{A} is liable only if {A} intended death']),
        dict(facts='{A} {threat} {B} in a car park in {city}. To escape, {B} {react} and was seriously injured.',
             slots={'threat': ['threatened to attack', 'chased with a knife', 'shouted violent threats at'],
                    'react': [('ran across a busy road and was hit by a car', 'a foreseeable reaction (R v Roberts)', 'liable'), ('jumped from a first-floor balcony', 'a foreseeable reaction unless "daft" (R v Williams)', 'probably liable'), ('stopped to take selfies and then deliberately lay down in the road', 'a "daft" and unforeseeable reaction that may break the chain (R v Williams)', 'probably not liable')]},
             issue='whether the victim\'s own act breaks the chain of causation', wrong=['the thin skull rule only', 'strict liability', 'a duty to act arising from contract'],
             ask='Discuss whether {A} is the legal cause of {B}\'s injuries.',
             law=['factual causation: "but for" test', 'the victim\'s reaction does not break the chain if it is reasonably foreseeable (R v Roberts)', 'only a "daft" reaction, out of proportion to the threat, breaks the chain (R v Williams 1992)', 'the free, deliberate and informed act of the victim may break the chain (R v Kennedy (No 2))'],
             apply=['but for {A}\'s conduct, {B} would not have been injured', '{B} {react}, which is {react_1}'],
             concl='{A} is {react_2} for the injuries')],
  ev=[('Evaluate the rules on intervening acts in causation.', ['protect defendants from liability for unforeseeable events', 'Cheshire ensures attackers do not escape liability because of hospital errors', 'thin skull rule protects vulnerable victims'],
       ['difficult distinctions (Jordan v Cheshire)', 'thin skull rule can seem harsh (Blaue)', 'the "daft" test is vague', 'policy rather than principle often decides cases'],
       ['R v Pagett (1983)', 'R v Jordan (1956)', 'R v Cheshire (1991)', 'R v Blaue (1975)', 'R v Roberts (1971)', 'R v Kennedy (No 2) (2007)'], 'the rules are broadly fair but rely heavily on policy and can be uncertain')])

T(6, 'Mens rea: direct and oblique intention, recklessness and negligence', area='mens rea',
  defs=[('mens rea', 'The mental element of a crime, such as intention or recklessness, that the prosecution must prove the defendant had at the time of the actus reus.'),
        ('direct intention', 'Where the defendant\'s aim or purpose is to bring about the consequence (R v Mohan: "a decision to bring about... no matter whether the accused desired that consequence").'),
        ('oblique intention', 'Where the consequence is not the defendant\'s aim, but it is a virtual certainty as a result of the defendant\'s actions and the defendant appreciates this (R v Woollin).'),
        ('subjective recklessness', 'Where the defendant is aware of a risk and goes on to take it when it is unreasonable to do so (R v Cunningham; R v G).'),
        ('negligence', 'Falling below the standard of care expected of a reasonable person; an objective standard used for some offences such as gross negligence manslaughter.')],
  mcqs=[('Which case sets out the current test for oblique intention?', 'R v Woollin (1998)', ['R v Mohan (1975)', 'R v Cunningham (1957)', 'R v G (2003)'], 'Woollin: virtual certainty of death or serious injury and appreciation by D.'),
        ('Which case overruled the objective test of recklessness from MPC v Caldwell (1982)?', 'R v G and R (2003)', ['R v Cunningham (1957)', 'R v Nedrick (1986)', 'R v Matthews and Alleyne (2003)'], 'R v G restored subjective recklessness.'),
        ('In R v Matthews and Alleyne (2003), the Court of Appeal held that foresight of virtual certainty is:', 'evidence from which the jury may find intention, not intention itself', ['the same thing as intention', 'irrelevant to intention', 'a form of recklessness'], 'Following Woollin, the jury is "entitled to find" intention.'),
        ('Which word in Woollin replaced "infer" from Nedrick in the direction to the jury?', '"find"', ['"presume"', '"assume"', '"deem"'], 'Lord Steyn substituted "find" for "infer".')],
  cases=[('R v Mohan (1975)', 'the defendant drove at a police officer who was trying to stop him', 'direct intention is "a decision to bring about, in so far as it lies within the accused\'s power, the commission of the offence"'),
         ('R v Nedrick (1986)', 'the defendant poured paraffin through a letterbox and set it alight, killing a child', 'the jury may infer intention if death or serious injury was a virtual certainty and the defendant appreciated this'),
         ('R v Woollin (1998)', 'the defendant threw his three-month-old son onto a hard surface in a fit of temper, and the baby died', 'the jury is entitled to find intention if death or serious bodily harm was a virtual certainty and the defendant appreciated that this was the case'),
         ('R v Matthews and Alleyne (2003)', 'the defendants threw a non-swimmer from a bridge into a river, and he drowned', 'foresight of virtual certainty is evidence of intention, not a rule of law equating it with intention'),
         ('R v Cunningham (1957)', 'the defendant tore a gas meter from a wall to steal the money inside, and gas seeped next door, harming the occupant', 'recklessness is subjective: the defendant must have foreseen the risk and taken it'),
         ('R v G and R (2003)', 'two boys aged 11 and 12 set fire to newspapers behind a shop, not realising the fire would spread', 'a person is reckless only if aware of a risk which it is unreasonable to take; MPC v Caldwell was overruled'),
         ('R v Hancock and Shankland (1986)', 'striking miners pushed concrete blocks from a bridge onto a motorway, killing a taxi driver', 'the greater the probability of a consequence, the more likely it is that it was foreseen and intended')],
  ars=[('A defendant who did not desire a consequence may still be found to have intended it.', 'Under R v Woollin the jury may find intention where the consequence was a virtual certainty and the defendant appreciated this.', 'A'),
       ('Recklessness in English criminal law is assessed objectively.', 'R v G (2003) held that recklessness requires awareness of a risk.', 'D'),
       ('Motive is the same as intention.', 'A good motive is no defence if the defendant intended the result.', 'D')],
  exps=[('Explain the difference between direct and oblique intention.', 'Direct intention is where the result is the defendant\'s aim or purpose (Mohan); oblique intention is where the result is not the aim but is a virtual certainty and the defendant appreciates this (Woollin).', '1 mark direct + case; 1 mark oblique + case; 1 mark contrast. [3]'),
        ('Explain the significance of R v G and R (2003) for the law on recklessness.', 'The House of Lords overruled MPC v Caldwell, which had used an objective test, and held that recklessness is subjective: the defendant must be aware of the risk, which is fairer to children and others who cannot appreciate risks.', '1 mark overruled Caldwell; 1 mark subjective test; 1 mark fairness point. [3]'),
        ('Explain the difference between recklessness and negligence.', 'Recklessness is subjective: the defendant foresees a risk and unjustifiably takes it; negligence is objective: the defendant falls below the standard of the reasonable person, whether or not they foresaw the risk.', '1 mark recklessness; 1 mark negligence; 1 mark subjective v objective. [3]')],
  cmps=[('direct intention', 'subjective recklessness', ['direct intention means the result is the defendant\'s aim, recklessness means the defendant foresaw a risk of it and took that risk', 'intention is required for murder, recklessness is enough for offences such as s20 and criminal damage'])],
  scen=[dict(facts='{A} wanted to {aim}. To do this, {A} {act}. {B}, who {where}, was killed.',
             slots={'aim': ['claim insurance money on a building', 'frighten a business rival', 'destroy evidence of a fraud'],
                    'act': [('set fire to the building at night', 'a virtual certainty', 'is likely to'), ('planted a small bomb timed to explode while the building was occupied', 'a virtual certainty', 'is likely to'), ('threw a brick through a window of an empty-looking office', 'not a virtual certainty', 'is unlikely to')],
                    'where': ['was asleep inside', 'was working late inside']},
             issue='oblique intention under R v Woollin', wrong=['direct intention under R v Mohan', 'subjective recklessness under R v G', 'transferred malice'],
             ask='Discuss whether {A} had the mens rea for murder.',
             law=['murder requires intention to kill or cause grievous bodily harm', 'direct intention: the result is the aim (R v Mohan)', 'oblique intention: the jury may find intention if death or serious injury was a virtual certainty and the defendant appreciated this (R v Woollin; R v Nedrick)', 'foresight is evidence of intention (R v Matthews and Alleyne)'],
             apply=['{A}\'s aim was to {aim}, not to kill, so there is no direct intention', 'death or serious injury was {act_1} as a result of the act', 'the jury {act_2} find oblique intention if {A} appreciated this'],
             concl='the jury {act_2} find that {A} had oblique intention for murder; otherwise manslaughter may be considered'),
        dict(facts='{A}, aged {age}, {act} in {city}. {res}.',
             slots={'age': ['12', '15', '19', '30'],
                    'act': ['lit a small fire in a skip behind a shop', 'threw stones at a passing train', 'set off fireworks next to a wooden fence'],
                    'res': ['The fire spread and caused serious damage', 'A window was smashed and a passenger was cut', 'A shed was burned down']},
             issue='subjective recklessness under R v G', wrong=['oblique intention', 'negligence only', 'strict liability'],
             ask='Discuss whether {A} was reckless.',
             law=['recklessness is subjective: the defendant must be aware of a risk which, in the circumstances known to him, it is unreasonable to take (R v G 2003)', 'R v Cunningham (1957) also requires foresight of the risk', 'MPC v Caldwell objective test no longer applies'],
             apply=['the question is whether {A} actually foresaw the risk', 'as {A} is {age}, evidence of whether {A} appreciated the danger is important', 'if {A} did not foresee any risk, {A} was not reckless'],
             concl='{A} is reckless only if {A} actually foresaw the risk of the harm and unreasonably took it')],
  ev=[('Evaluate the law on oblique intention.', ['Woollin gives a clear test of virtual certainty', 'limits murder to the most culpable', 'jury flexibility'],
       ['"entitled to find" leaves uncertainty whether foresight is intention or evidence', 'juries may reach different verdicts on similar facts', 'the Law Commission has recommended codification'],
       ['R v Nedrick (1986)', 'R v Woollin (1998)', 'R v Matthews and Alleyne (2003)', 'R v Hancock and Shankland (1986)'], 'the law is clearer since Woollin but uncertainty remains about the status of foresight'),
      ('"The subjective approach to recklessness is fairer than an objective approach." Discuss.', ['punishes only those who choose to take risks', 'fair to children and those with limited capacity (R v G)', 'consistent with the principle of personal fault'],
       ['allows thoughtless defendants to escape liability', 'harder to prove', 'some offences use negligence, showing objective fault has a role'],
       ['R v Cunningham (1957)', 'MPC v Caldwell (1982)', 'R v G and R (2003)'], 'the subjective approach is fairer in principle, though it can let careless defendants escape')])

T(6, 'Coincidence of actus reus and mens rea; transferred malice', area='coincidence and transferred malice',
  defs=[('coincidence of actus reus and mens rea', 'The principle that the actus reus and mens rea of an offence must be present at the same time, although the courts allow for continuing acts and series of acts.'),
        ('continuing act', 'An actus reus that continues over a period of time, so that mens rea formed at any point during it is sufficient (Fagan v MPC).'),
        ('transferred malice', 'The principle that a defendant\'s mens rea against one victim can be transferred to another victim of the same type of offence (R v Latimer).'),
        ('series of acts (same transaction)', 'The principle that where there is a series of linked acts, the actus reus and mens rea need only coincide at some point during the transaction (Thabo Meli v R).')],
  mcqs=[('In Fagan v MPC (1969), why was the defendant guilty of assaulting a police officer?', 'Driving onto the officer\'s foot and refusing to move was a continuing act during which he formed mens rea', ['He intended to drive onto the foot from the start', 'Battery is a strict liability offence', 'He owed a duty as a driver'], 'The actus reus continued while the car remained on the foot.'),
        ('Which case shows that malice cannot be transferred between different types of offence?', 'R v Pembliton (1874)', ['R v Latimer (1886)', 'R v Mitchell (1983)', 'Thabo Meli v R (1954)'], 'Mens rea for assault (throwing a stone at people) could not be transferred to criminal damage of a window.'),
        ('In Thabo Meli v R (1954), the defendants were guilty of murder because:', 'the beating and the disposal of the body were one series of acts', ['they intended to kill when they threw the body over the cliff', 'they were reckless', 'the victim had a thin skull'], 'The court treated the plan as one transaction.'),
        ('In R v Latimer (1886), the defendant aimed a blow with his belt at a man but it struck and wounded a woman. He was:', 'guilty, because his malice was transferred to the woman', ['not guilty, because he did not intend to hit the woman', 'guilty only of attempted assault on the man', 'not guilty, because the injury was an accident'], 'Transferred malice: same type of offence.')],
  cases=[('Fagan v Metropolitan Police Commissioner (1969)', 'the defendant accidentally drove onto a police officer\'s foot and then refused to move the car', 'where the actus reus is a continuing act, mens rea formed during it is sufficient'),
         ('Thabo Meli v R (1954)', 'the defendants beat a man, thought he was dead and threw his body over a cliff, where he died of exposure', 'where there is a series of acts forming one transaction, it is enough that mens rea existed at some point during it'),
         ('R v Church (1966)', 'the defendant knocked a woman unconscious, panicked and, thinking she was dead, threw her into a river where she drowned', 'the series-of-acts approach applies even without a pre-planned scheme'),
         ('R v Le Brun (1991)', 'the defendant hit his wife and, while dragging her body away to avoid detection, dropped her and she died from hitting her head', 'where the later act is part of the same sequence, such as trying to cover up the first act, the actus reus and mens rea coincide'),
         ('R v Latimer (1886)', 'the defendant swung his belt at a man, but it bounced off and struck a woman in the face', 'mens rea for one victim can be transferred to an unintended victim of the same type of offence'),
         ('R v Pembliton (1874)', 'the defendant threw a stone at people he was fighting, but missed and broke a window', 'malice cannot be transferred from one type of offence (against the person) to a different type (criminal damage)'),
         ('Attorney-General\'s Reference (No 3 of 1994) (1997)', 'the defendant stabbed a pregnant woman; the baby was born prematurely and died months later', 'the House of Lords refused a "double transfer" of malice from mother to foetus to child for murder, but manslaughter was possible'),
         ('R v Gnango (2011)', 'two men had a gunfight in a car park and a passer-by was killed by a bullet fired by the defendant\'s opponent', 'transferred malice can operate with joint liability: the defendant could be guilty of the murder of the passer-by')],
  ars=[('Mens rea can be transferred from an intended victim to an actual victim of the same offence.', 'R v Latimer (1886) established the doctrine of transferred malice.', 'A'),
       ('The actus reus and mens rea must always exist at exactly the same moment.', 'Fagan v MPC (1969) treated the actus reus as a continuing act.', 'D'),
       ('Malice can always be transferred between different types of offence.', 'In R v Pembliton (1874) the defendant was not guilty of damaging the window.', 'D')],
  exps=[('Explain how the courts have avoided strict application of the coincidence rule.', 'By treating the actus reus as a continuing act during which mens rea arises (Fagan v MPC); and by treating a series of linked acts as one transaction (Thabo Meli v R; R v Church; R v Le Brun).', '1 mark continuing act + case; 1 mark series of acts + case; 1 mark explanation of why. [3]'),
        ('Explain the limits of the doctrine of transferred malice.', 'Malice transfers only within the same type of offence (R v Pembliton), and the House of Lords refused a double transfer from mother to foetus to child for murder (Attorney-General\'s Reference (No 3 of 1994)).', '1 mark same type of offence + Pembliton; 1 mark double transfer + A-G Ref. [2]')],
  cmps=[('a continuing act', 'a series of acts', ['a continuing act is one act lasting over time (Fagan), a series of acts is several linked acts treated as one transaction (Thabo Meli)', 'in both, mens rea need only exist at some point during the actus reus'])],
  scen=[dict(facts='{A} {aim} at {B} in a {place} in {city}, but {miss}.',
             slots={'aim': ['threw a glass bottle', 'swung a heavy bag', 'threw a punch'],
                    'place': ['bar', 'bus station', 'football ground'],
                    'miss': [('missed and hit {C}, who was cut on the face', 'transferred to {C}, because the offence is the same type (offence against the person)', 'can be liable for the injury to {C}'),
                             ('missed and smashed a shop window', 'not transferred to the window, because criminal damage is a different type of offence (R v Pembliton)', 'is not liable for criminal damage unless reckless as to the property')]},
             issue='transferred malice', wrong=['a continuing act', 'oblique intention', 'liability for an omission'],
             ask='Discuss {A}\'s liability, applying the doctrine of transferred malice.',
             law=['transferred malice: mens rea against one victim transfers to the actual victim of the same type of offence (R v Latimer)', 'it does not transfer between different types of offence (R v Pembliton)', 'no "double transfer" (Attorney-General\'s Reference (No 3 of 1994))'],
             apply=['{A} had mens rea towards {B}', 'the mens rea is {miss_1}'],
             concl='{A} {miss_2}'),
        dict(facts='{A} hit {B} on the head with a {weapon} during a fight in {city}. Believing {B} was dead, {A} {dispose}. In fact {B} was alive and died as a result of {cause}.',
             slots={'weapon': ['metal bar', 'brick', 'bottle'],
                    'dispose': [('dragged {B} into a river to hide the body', 'drowning'), ('buried {B} in a shallow grave', 'suffocation'), ('left {B} in a freezing field', 'exposure')],
                    'cause': ['{dispose_1}']},
             issue='the coincidence of actus reus and mens rea (series of acts)', wrong=['transferred malice', 'strict liability', 'diminished responsibility'],
             ask='Discuss whether the actus reus and mens rea of murder coincide.',
             law=['actus reus and mens rea must coincide', 'a series of acts can be one transaction (Thabo Meli v R)', 'this applies without a preconceived plan (R v Church) and where the later act is an attempt to cover up (R v Le Brun)'],
             apply=['when {A} {dispose} there was no mens rea, but the earlier blow was done with mens rea', 'the acts form one transaction, so they coincide'],
             concl='the actus reus and mens rea coincide across the series of acts, so {A} can be liable for murder (or manslaughter if only intent for lesser harm)')],
  ev=[('Evaluate how the courts have applied the requirement of coincidence of actus reus and mens rea.', ['continuing act and series of acts avoid unjust acquittals', 'consistent with common sense (Thabo Meli, Le Brun)'],
       ['the extensions may be seen as manipulating the rule', 'uncertainty about how long a "transaction" lasts', 'Fagan stretches the meaning of an act'],
       ['Fagan v MPC (1969)', 'Thabo Meli v R (1954)', 'R v Church (1966)', 'R v Le Brun (1991)'], 'the courts have adapted the rule sensibly to achieve justice, at some cost to certainty')])

T(6, 'Strict liability offences', area='strict liability',
  defs=[('strict liability offence', 'An offence where the prosecution does not need to prove mens rea in respect of at least one element of the actus reus.'),
        ('absolute liability', 'An offence where no mens rea is required at all and the actus reus need not even be voluntary, such as R v Larsonneur (1933).'),
        ('regulatory offence', 'A minor offence, often of strict liability, concerned with matters of social concern such as food safety, pollution or sale of alcohol, rather than "truly criminal" behaviour.'),
        ('due diligence defence', 'A statutory defence in some strict liability offences, available where the defendant took all reasonable precautions and exercised all due diligence to avoid committing the offence.')],
  mcqs=[('Which case set out the criteria (Lord Scarman) for deciding whether an offence is of strict liability?', 'Gammon (Hong Kong) Ltd v Attorney-General of Hong Kong (1985)', ['Sweet v Parsley (1970)', 'R v Woollin (1998)', 'Callow v Tillstone (1900)'], 'Gammon: presumption of mens rea; displaced only clearly or by necessary implication, e.g. matters of social concern.'),
        ('In Smedleys v Breed (1974), the defendants were liable even though:', 'they had taken all reasonable care and only one tin in over three million contained a caterpillar', ['they intended to sell contaminated food', 'the caterpillar was harmful', 'the customer consented'], 'Strict liability: no defence of due care under the Food and Drugs Act 1955.'),
        ('Which case held that a pharmacist was guilty of supplying drugs on a forged prescription even though he did not know it was forged?', 'Pharmaceutical Society of Great Britain v Storkwain (1986)', ['B v DPP (2000)', 'Sweet v Parsley (1970)', 'R v Prince (1875)'], 'Storkwain: the Medicines Act 1968 offence was of strict liability.'),
        ('In B v DPP (2000), the House of Lords held that:', 'the presumption of mens rea applied to the age element of the offence, so an honest belief that the girl was over 14 was a defence', ['all sexual offences are strict liability', 'mistakes as to age are never a defence', 'mens rea is never required for statutory offences'], 'The presumption of mens rea was not displaced.')],
  cases=[('Sweet v Parsley (1970)', 'a teacher who sublet a farmhouse was convicted when tenants smoked cannabis there without her knowledge', 'there is a presumption that mens rea is required for statutory offences, especially "truly criminal" offences'),
         ('Gammon (Hong Kong) Ltd v Attorney-General of Hong Kong (1985)', 'builders were charged after part of a building collapsed in breach of building regulations', 'the presumption of mens rea can be displaced where the offence concerns social concern such as public safety and strict liability will promote observance of the law'),
         ('Pharmaceutical Society of Great Britain v Storkwain Ltd (1986)', 'a pharmacist supplied drugs on a forged doctor\'s prescription without knowing it was forged', 'the offence was of strict liability, so lack of knowledge was no defence'),
         ('Callow v Tillstone (1900)', 'a butcher sold unfit meat after a vet had certified it as fit', 'selling unfit meat was a strict liability offence, so the butcher was liable despite taking care'),
         ('Smedleys Ltd v Breed (1974)', 'a caterpillar was found in one tin of peas out of more than three million produced', 'the offence was of strict liability, so taking all reasonable care was no defence'),
         ('Alphacell Ltd v Woodward (1972)', 'polluted water overflowed from a company\'s tanks into a river without the company being negligent', 'causing polluted matter to enter a river is a strict liability offence'),
         ('Harrow London Borough Council v Shah (1999)', 'a newsagent\'s employee sold a lottery ticket to a 13-year-old boy believing he was over 16', 'the offence of selling a lottery ticket to someone under 16 was of strict liability'),
         ('Cundy v Le Cocq (1884)', 'a publican served alcohol to a customer who was drunk, though he showed no signs of it', 'selling alcohol to a drunken person was a strict liability offence'),
         ('B v DPP (2000)', 'a 15-year-old boy asked a 13-year-old girl for oral sex, believing she was older than 14', 'the presumption of mens rea applies to the age element unless excluded clearly or by necessary implication')],
  ars=[('Strict liability offences are usually regulatory offences.', 'Courts are more willing to impose strict liability for offences concerned with public safety and social concern.', 'A'),
       ('In strict liability offences the prosecution does not need to prove the actus reus.', 'Strict liability removes the need to prove mens rea for at least one element.', 'D'),
       ('Courts presume that mens rea is required for statutory offences.', 'Sweet v Parsley (1970) confirmed this presumption.', 'A')],
  exps=[('Explain two arguments in favour of strict liability.', 'It protects the public by encouraging high standards in areas of social concern such as food, pollution and alcohol; it is easier to enforce and saves court time because mens rea need not be proved; penalties are usually small.', '2 × (1 mark argument, 1 mark explanation). [4]'),
        ('Explain two arguments against strict liability.', 'It is unjust to convict people who took all reasonable care (Smedleys, Callow v Tillstone); there is no evidence it improves standards; a conviction can cause stigma and harm business reputation; it may breach the presumption of innocence.', '2 × (1 mark argument, 1 mark explanation/case). [4]'),
        ('Explain how the courts decide whether a statutory offence is of strict liability.', 'They start with the presumption of mens rea (Sweet v Parsley); they consider the Gammon criteria: whether the offence is truly criminal or regulatory, whether it concerns social concern or public safety, the wording of the Act, and whether strict liability would promote the purpose of the law.', '1 mark presumption; 1 mark wording; 1 mark social concern/regulatory; 1 mark promote observance. [4]')],
  cmps=[('a strict liability offence', 'an offence requiring mens rea', ['strict liability does not need proof of mens rea for at least one element; other offences require intention, recklessness or knowledge', 'strict liability offences are usually regulatory with lower penalties, mens rea offences are often truly criminal'])],
  scen=[dict(facts='{A} runs a {biz} in {city}. {event}. {A} {care}. {A} is charged with an offence under the (fictional) {act}, which does not mention any mental element.',
             slots={'biz': [('food factory', 'Food Safety Act 2015', 'A piece of metal was found in a tin of soup'), ('corner shop', 'Licensing Act 2016', 'An assistant sold beer to a 16-year-old who looked about 20'), ('chemical plant', 'River Protection Act 2017', 'A sealed tank cracked and polluted a nearby river')],
                    'event': ['{biz_2}'], 'act': ['{biz_1}'],
                    'care': ['had trained staff carefully and carried out regular checks', 'had no idea anything had gone wrong']},
             issue='whether the offence is of strict liability', wrong=['oblique intention', 'transferred malice', 'subjective recklessness'],
             ask='Discuss whether {A} is likely to be liable even though {A} was not at fault.',
             law=['presumption of mens rea for statutory offences (Sweet v Parsley 1970; B v DPP 2000)', 'Gammon (1985): presumption displaced for regulatory offences of social concern where strict liability promotes observance', 'examples: Smedleys v Breed (food), Alphacell v Woodward (pollution), Harrow LBC v Shah (sales to minors)', 'some statutes provide a due diligence defence'],
             apply=['the {act} is silent on mens rea, so the presumption applies at first', 'the offence concerns public safety and is regulatory, so the presumption is likely to be displaced', 'that {A} {care} would not help unless there is a due diligence defence'],
             concl='the offence is likely to be strict liability, so {A} is probably liable despite not being at fault')],
  ev=[('Evaluate the arguments for and against strict liability offences.', ['protects public in areas of social concern', 'easier to enforce, saving time', 'encourages higher standards', 'usually minor penalties'],
       ['convicts the blameless (Callow v Tillstone, Smedleys)', 'no evidence that it raises standards', 'stigma of conviction', 'inconsistent with the presumption of innocence', 'courts inconsistent in deciding which offences are strict'],
       ['Sweet v Parsley (1970)', 'Gammon (1985)', 'Smedleys v Breed (1974)', 'Pharmaceutical Society v Storkwain (1986)', 'B v DPP (2000)'], 'strict liability can be justified for minor regulatory offences, preferably with a due diligence defence')])

# =====================================================================================
# 7 Criminal law: offences and defences
# =====================================================================================

T(7, 'Non-fatal offences against the person: assault, battery, ABH, GBH and wounding', area='non-fatal offences against the person',
  defs=[('assault', 'Intentionally or recklessly causing the victim to apprehend the infliction of immediate unlawful force (a common law offence charged under s39 Criminal Justice Act 1988).'),
        ('battery', 'Intentionally or recklessly applying unlawful force to another person, which can be as little as an unwanted touch (Collins v Wilcock).'),
        ('actual bodily harm', 'Any hurt or injury calculated to interfere with the health or comfort of the victim, which need not be permanent but must be more than transient or trifling (R v Miller; R v Chan-Fook).'),
        ('grievous bodily harm', '"Really serious harm" (DPP v Smith), which can include serious psychiatric injury (R v Burstow), judged in the light of the victim\'s age and health (R v Bollom).'),
        ('wound', 'A break in the continuity of the whole skin, both the outer and inner layers (JCC v Eisenhower).')],
  mcqs=[('What is the maximum sentence for assault occasioning actual bodily harm under s47 Offences Against the Person Act 1861?', '5 years\' imprisonment', ['6 months\' imprisonment', 'Life imprisonment', '2 years\' imprisonment'], 's47 and s20 both carry 5 years; s18 carries life.'),
        ('Which case decided that the mens rea for s47 is only the mens rea for the assault or battery?', 'R v Savage; DPP v Parmenter (1991)', ['R v Mowatt (1968)', 'R v Belfon (1976)', 'R v Burstow (1997)'], 'No need to intend or foresee ABH (also R v Roberts 1971).'),
        ('In JCC v Eisenhower (1984), why was there no wound?', 'The internal bleeding from an air-gun pellet did not break both layers of the skin', ['The victim consented', 'The defendant did not intend to injure', 'The injury healed quickly'], 'A wound requires a break in the whole skin.'),
        ('Which case held that silent telephone calls can amount to an assault?', 'R v Ireland (1997)', ['Tuberville v Savage (1669)', 'Collins v Wilcock (1984)', 'R v Chan-Fook (1994)'], 'Silence can cause apprehension of immediate force.'),
        ('What does "maliciously" mean in s20 OAPA 1861, according to R v Mowatt (1968)?', 'The defendant intended or foresaw that some harm might result', ['The defendant intended to cause really serious harm', 'The defendant acted with spite', 'The defendant was negligent'], 'Foresight of some harm, not serious harm, is enough.'),
        ('Which offence requires an intention to cause grievous bodily harm?', 'Section 18 OAPA 1861', ['Section 20 OAPA 1861', 'Section 47 OAPA 1861', 'Common assault'], 's18: wounding or causing GBH with intent.')],
  cases=[('Logdon v DPP (1976)', 'the defendant showed the victim a replica gun in a drawer and said he would hold her hostage', 'an assault is committed if the victim apprehends immediate force, even if the defendant could not actually use it'),
         ('Tuberville v Savage (1669)', 'the defendant put his hand on his sword and said "If it were not assize time, I would not take such language from you"', 'words can negate an assault where they show that no immediate force will be used'),
         ('R v Ireland (1997)', 'the defendant made repeated silent telephone calls to three women, causing psychiatric harm', 'silence can be an assault, and psychiatric injury can be actual bodily harm'),
         ('Collins v Wilcock (1984)', 'a police officer took hold of a woman\'s arm to stop her walking away, without arresting her', 'any touching beyond everyday physical contact can be a battery'),
         ('DPP v K (1990)', 'a schoolboy hid acid in a hand dryer, which sprayed onto another pupil', 'a battery can be committed by indirect force'),
         ('R v Miller (1954)', 'a husband was charged with assaulting his wife, causing her actual bodily harm', 'actual bodily harm includes any hurt or injury calculated to interfere with the health or comfort of the victim'),
         ('R v Chan-Fook (1994)', 'the defendant locked a suspected thief in a room, causing him to panic', 'ABH can include psychiatric injury but not mere emotions such as fear or panic'),
         ('DPP v Smith (2006)', 'the defendant cut off his ex-girlfriend\'s ponytail without her consent', 'cutting off a substantial amount of hair can be actual bodily harm'),
         ('R v Roberts (1971)', 'a woman jumped from a moving car after the driver made advances and tried to remove her coat', 'for s47, the defendant need only have the mens rea for the assault or battery, not for the harm'),
         ('JCC (a minor) v Eisenhower (1984)', 'the victim was hit near the eye by an air-gun pellet, causing internal bleeding but no break in the skin', 'a wound requires a break in both layers of the skin; internal bleeding is not a wound'),
         ('R v Bollom (2003)', 'a 17-month-old child suffered bruising and abrasions over her body', 'the seriousness of injuries for GBH is assessed taking into account the victim\'s age and health'),
         ('R v Burstow (1997)', 'the defendant stalked a woman for months, causing severe depression', 'serious psychiatric injury can amount to grievous bodily harm and can be "inflicted" without physical force'),
         ('R v Mowatt (1968)', 'during a struggle the defendant punched and seriously injured a police officer', 'for s20 the defendant must intend or foresee that some harm might result, not necessarily serious harm'),
         ('R v Belfon (1976)', 'the defendant slashed the victim with a razor, causing serious wounds', 's18 requires a specific intention to cause grievous bodily harm; foresight or recklessness is not enough')],
  ars=[('An assault can be committed without any physical contact.', 'Assault is causing the victim to apprehend immediate unlawful force.', 'A'),
       ('For s47 ABH, the defendant must intend or foresee the actual bodily harm.', 'R v Savage (1991) held that the mens rea of the assault or battery is enough.', 'D'),
       ('A small cut that breaks both layers of the skin can be a wound.', 'A wound requires a break in the continuity of the whole skin (JCC v Eisenhower).', 'A')],
  exps=[('Explain the actus reus and mens rea of battery.', 'Actus reus: the application of unlawful force, which can be minimal (Collins v Wilcock) or indirect (DPP v K, Haystead). Mens rea: intention or subjective recklessness as to applying unlawful force (R v Venna).', '1 mark AR; 1 mark example; 1 mark MR. [3]'),
        ('Explain the difference between s20 and s18 Offences Against the Person Act 1861.', 's20 requires malicious wounding or inflicting GBH with intention or recklessness as to some harm (Mowatt); s18 requires wounding or causing GBH with specific intent to cause GBH (or to resist arrest), and carries life imprisonment rather than 5 years.', '1 mark s20 MR; 1 mark s18 specific intent; 1 mark sentence difference. [3]'),
        ('Explain how the courts decide whether an injury is ABH or GBH.', 'ABH is any hurt or injury that is more than transient or trifling (Miller, Chan-Fook), e.g. bruises, minor fractures; GBH is really serious harm (DPP v Smith, Saunders), e.g. broken limbs, serious psychiatric injury (Burstow), assessed in light of the victim (Bollom); the CPS Charging Standard gives guidance.', '1 mark ABH definition; 1 mark GBH definition; 1 mark examples/Bollom. [3]')],
  cmps=[('assault', 'battery', ['assault causes apprehension of force, battery involves actual application of force', 'assault can occur without touching, battery requires contact (direct or indirect)']),
        ('a wound', 'grievous bodily harm', ['a wound is any break in both layers of the skin, even minor; GBH is really serious harm', 'GBH can be internal or psychiatric without any wound'])],
  scen=[dict(facts='{A} and {B} argued outside a {place} in {city}. {A} {act}. {B} suffered {inj}.',
             slots={'place': ['nightclub', 'football stadium', 'restaurant', 'bus stop'],
                    'act': [('pushed {B} hard in the chest, intending only to move {B} out of the way', 'intention or recklessness as to battery only'), ('punched {B} in the face, aware that some injury might result', 'foresight of some harm'), ('stabbed {B} in the stomach, saying "I want to put you in hospital"', 'an intention to cause really serious harm')],
                    'inj': [('bruising and a cut lip', 's47 ABH (any hurt or injury more than transient or trifling, R v Miller)'), ('a broken jaw', 'GBH (really serious harm, DPP v Smith)'), ('a deep wound that needed stitches', 'a wound (break in both layers of the skin, JCC v Eisenhower)')]},
             issue='non-fatal offences against the person under the Offences Against the Person Act 1861', wrong=['unlawful act manslaughter', 'strict liability offences', 'criminal damage'],
             iq='Which area of law is most relevant to {A}\'s liability?',
             ask='Discuss {A}\'s criminal liability for the injuries to {B}.',
             law=['battery: application of unlawful force (Collins v Wilcock); s47 ABH: assault or battery causing ABH, with mens rea only for the assault or battery (Savage; Roberts)', 's20: maliciously wounding or inflicting GBH, with intention or foresight of some harm (Mowatt)', 's18: wounding or causing GBH with intent to cause GBH (Belfon)', 'GBH is really serious harm (DPP v Smith; Bollom); a wound breaks both layers of skin (Eisenhower)'],
             apply=['{A} {act}, which shows {act_1}', '{B} suffered {inj}, which is {inj_1}', 'the most serious offence is chosen by matching the injury with {A}\'s mens rea'],
             concl='{A} is liable for the offence that matches {inj_1} with {act_1}; if serious harm was intended, s18 applies'),
        dict(facts='{A} {act} {B} in {city}. {B} {res}.',
             slots={'act': [('waved a fake gun at', 'assault (apprehension of immediate force, Logdon v DPP)'), ('made a series of silent late-night phone calls to', 'assault by silence (R v Ireland)'), ('threw a cup of hot coffee over', 'battery by indirect force (DPP v K)')],
                    'res': [('was terrified but not physically hurt', 'no ABH, as fear or panic alone is not ABH (Chan-Fook)'), ('developed a diagnosed anxiety disorder', 'ABH, as recognised psychiatric injury (Chan-Fook; Ireland)'), ('suffered severe clinical depression', 'possibly GBH, as serious psychiatric injury (Burstow)')]},
             issue='assault, battery and psychiatric injury as bodily harm', wrong=['transferred malice', 'gross negligence manslaughter', 'oblique intention'],
             ask='Discuss which non-fatal offence, if any, {A} has committed.',
             law=['assault: causing apprehension of immediate unlawful force; words or silence can suffice (R v Ireland; R v Constanza)', 'battery: unlawful force, direct or indirect (DPP v K)', 'ABH can include recognised psychiatric injury but not mere fear (Chan-Fook); serious psychiatric injury can be GBH (Burstow)'],
             apply=['{A}\'s conduct is {act_1}', '{B}\'s harm: {res_1}'],
             concl='{A} has committed {act_1}; any further liability depends on whether {B}\'s condition is ABH or GBH: {res_1}')],
  ev=[('"The Offences Against the Person Act 1861 is in urgent need of reform." Discuss.', ['old-fashioned language ("maliciously", "grievous")', 'inconsistent mens rea: s47 needs no foresight of harm yet has the same maximum as s20', 'difference between "inflict" and "cause" is confusing', 'psychiatric injury had to be added by the courts (Burstow, Ireland)'],
       ['the courts have adapted the Act successfully', 'the CPS Charging Standard provides guidance', 'judges and lawyers understand the terms'],
       ['R v Savage; DPP v Parmenter (1991)', 'R v Mowatt (1968)', 'R v Burstow (1997)', 'R v Ireland (1997)', 'Law Commission draft Bill 1998 and report 2015'], 'reform along the lines of the Law Commission proposals is overdue')])

T(7, 'Murder and voluntary manslaughter: loss of control and diminished responsibility', area='murder and voluntary manslaughter',
  defs=[('murder', 'The unlawful killing of a reasonable creature in being under the King\'s peace with malice aforethought, express or implied (Coke); the mens rea is intention to kill or to cause grievous bodily harm.'),
        ('malice aforethought', 'The mens rea of murder: an intention to kill (express malice) or an intention to cause grievous bodily harm (implied malice, R v Vickers).'),
        ('loss of control', 'A partial defence to murder under ss54-56 Coroners and Justice Act 2009, reducing murder to voluntary manslaughter where D lost self-control because of a qualifying trigger and a normal person might have reacted similarly.'),
        ('diminished responsibility', 'A partial defence to murder under s2 Homicide Act 1957 (as amended by s52 Coroners and Justice Act 2009) based on an abnormality of mental functioning arising from a recognised medical condition.'),
        ('voluntary manslaughter', 'A killing with the mens rea for murder that is reduced to manslaughter because a partial defence, such as loss of control or diminished responsibility, applies.')],
  mcqs=[('What is the sentence for a person convicted of murder?', 'A mandatory life sentence', ['A maximum of 14 years', 'A discretionary sentence chosen by the jury', 'A fine and community order'], 'Murder carries a mandatory life sentence; this is why partial defences matter.'),
        ('Which of these is excluded as a qualifying trigger for loss of control under s55 Coroners and Justice Act 2009?', 'Sexual infidelity on its own', ['Fear of serious violence', 'Things said or done of an extremely grave character', 'A combination of fear of violence and grave provocation'], 'Sexual infidelity must be disregarded as a trigger, though it may be context (R v Clinton 2012).'),
        ('On whom is the burden of proving diminished responsibility?', 'The defendant, on the balance of probabilities', ['The prosecution, beyond reasonable doubt', 'The judge', 'The defendant, beyond reasonable doubt'], 'Section 2(2) Homicide Act 1957.'),
        ('Under s54 Coroners and Justice Act 2009, must the loss of control be sudden?', 'No, s54(2) states the loss of control need not be sudden', ['Yes, it must be sudden and temporary', 'Yes, but only for women', 'No, and no loss of control is needed at all'], 'This reform helps victims of long-term abuse; but a considered desire for revenge is excluded.'),
        ('Which case held that "substantially" impaired in diminished responsibility means important or weighty, not merely more than trivial?', 'R v Golds (2016)', ['R v Byrne (1960)', 'R v Dietschmann (2003)', 'R v Jewell (2014)'], 'Golds (Supreme Court).'),
        ('Which case held that a defendant\'s intoxication does not prevent diminished responsibility if the abnormality substantially impaired him anyway?', 'R v Dietschmann (2003)', ['R v Clinton (2012)', 'R v Dawes (2013)', 'R v Vickers (1957)'], 'Dietschmann: jury considers whether the abnormality, despite drink, substantially impaired him.')],
  cases=[('R v Vickers (1957)', 'a burglar hit an elderly woman several times when she disturbed him, and she died', 'an intention to cause grievous bodily harm is sufficient mens rea for murder (implied malice)'),
         ('R v Clinton (2012)', 'the defendant killed his wife after she told him about her affairs and taunted him', 'sexual infidelity cannot alone be a qualifying trigger, but it can be considered as context alongside other triggers'),
         ('R v Jewell (2014)', 'the defendant shot a colleague after collecting a bag with a gun and other weapons, claiming he feared for his life', 'loss of control means a loss of the ability to act in accordance with considered judgement; planning suggests no loss of control'),
         ('R v Dawes (2013)', 'the defendant claimed he lost control after finding his wife with another man, but there was evidence he started the violence', 'a defendant cannot rely on a trigger that he deliberately incited as an excuse to use violence'),
         ('R v Byrne (1960)', 'a sexual psychopath strangled and mutilated a young woman', 'abnormality of mind is a state so different from that of ordinary people that a reasonable man would term it abnormal (decided under the old wording)'),
         ('R v Golds (2016)', 'a man suffering from a mental disorder killed his partner, and the meaning of "substantially impaired" was disputed', '"substantially" impaired should be given its ordinary meaning of important or weighty, not merely more than trivial'),
         ('R v Dietschmann (2003)', 'the defendant, who was drunk and suffering a grief reaction, killed a man he thought had insulted his dead aunt', 'intoxication does not prevent diminished responsibility; the jury asks whether the abnormality substantially impaired him despite the drink'),
         ('R v Ahluwalia (1992)', 'after years of abuse a wife set fire to her sleeping husband', 'under the old law a delay could negate provocation; diminished responsibility was later accepted at a retrial, showing the need for reform')],
  ars=[('A successful plea of loss of control results in a conviction for voluntary manslaughter.', 'Loss of control is a partial defence to murder.', 'A'),
       ('For diminished responsibility, any mental condition is enough.', 'The abnormality must arise from a recognised medical condition.', 'D'),
       ('Loss of control is not available where the defendant acted in a considered desire for revenge.', 'Section 54(4) Coroners and Justice Act 2009 excludes acts in a considered desire for revenge.', 'A')],
  exps=[('Explain the three requirements of the loss of control defence.', 'The defendant lost self-control (need not be sudden, s54(2)); the loss of control had a qualifying trigger: fear of serious violence or things said/done of an extremely grave character causing a justifiable sense of being seriously wronged (s55); and a person of D\'s sex and age with a normal degree of tolerance and self-restraint in D\'s circumstances might have reacted in the same or a similar way (s54(1)(c)).', '1 mark per requirement. [3]'),
        ('Explain the requirements of diminished responsibility under s2 Homicide Act 1957 as amended.', 'An abnormality of mental functioning arising from a recognised medical condition, which substantially impaired D\'s ability to understand his conduct, form a rational judgement or exercise self-control, and which provides an explanation for the killing (a significant contributory factor).', '1 mark abnormality/recognised condition; 1 mark substantial impairment of one ability; 1 mark explanation for the killing. [3]'),
        ('Explain why partial defences to murder exist.', 'Murder carries a mandatory life sentence, so the judge cannot reflect reduced blameworthiness in sentencing; partial defences reduce the conviction to manslaughter, allowing a sentence that fits the defendant\'s culpability.', '1 mark: mandatory life sentence; 1 mark: allows discretion/fair labelling. [2]')],
  cmps=[('loss of control', 'diminished responsibility', ['loss of control is based on a reaction to a qualifying trigger, diminished responsibility on a recognised medical condition', 'the prosecution must disprove loss of control once raised, while the defendant must prove diminished responsibility on the balance of probabilities', 'loss of control has an objective normal-person test, diminished responsibility does not'])],
  scen=[dict(facts='{A} {back}. One evening {B} {trigger}. {A} {reaction} and killed {B}.',
             slots={'back': ['had been bullied and threatened by {B}, a flatmate, for months', 'lived with {B}, who had been violent towards {A} for years', 'had recently argued with {B} about money'],
                    'trigger': [('pulled out a knife and threatened to kill {A}', 'fear of serious violence under s55(3)'), ('told {A} that {B} had been having an affair', 'sexual infidelity, which must be disregarded on its own (s55(6)(c); R v Clinton)'), ('taunted {A} about the recent death of {A}\'s child', 'possibly things said of an extremely grave character causing a justifiable sense of being seriously wronged (s55(4))')],
                    'reaction': [('immediately grabbed a heavy pan in a rage and hit {B} on the head', 'an apparent loss of self-control'), ('went to the garage, waited an hour, then returned with a hammer', 'a considered desire for revenge that excludes the defence (s54(4); R v Jewell)')]},
             issue='the partial defence of loss of control', wrong=['diminished responsibility', 'self-defence as a complete defence', 'insanity'],
             iq='Which partial defence is {A} most likely to raise?',
             ask='Discuss whether {A} can rely on the defence of loss of control.',
             law=['murder requires an unlawful killing with intention to kill or cause GBH (R v Vickers)', 'Coroners and Justice Act 2009 s54: D lost self-control (need not be sudden), with a qualifying trigger, and a normal person might have reacted similarly', 's55 triggers: fear of serious violence; things said or done of an extremely grave character causing a justifiable sense of being seriously wronged; sexual infidelity disregarded (R v Clinton)', 'excluded: considered desire for revenge; incited triggers (R v Dawes)'],
             apply=['{A} has the actus reus and probably the mens rea for murder', '{B}\'s conduct ({trigger}) is relevant as {trigger_1}', '{A} {reaction}, which suggests {reaction_1}', 'the jury must consider whether a person of {A}\'s sex and age with normal tolerance and self-restraint might have reacted in the same way'],
             concl='if the trigger qualifies and there was a genuine loss of control, {A} will be guilty of voluntary manslaughter rather than murder; here the reaction suggests {reaction_1}'),
        dict(facts='{A} has been diagnosed with {cond}. During {episode}, {A} attacked and killed {B}. {A} {drink}.',
             slots={'cond': ['severe depression', 'paranoid schizophrenia', 'post-traumatic stress disorder'],
                    'episode': ['a period of severe symptoms', 'an argument in a car park in {city}'],
                    'drink': ['had also drunk a large amount of alcohol that day', 'had not taken any alcohol or drugs', 'had stopped taking prescribed medication']},
             issue='the partial defence of diminished responsibility', wrong=['loss of control', 'insanity under the M\'Naghten Rules', 'involuntary intoxication'],
             iq='Which partial defence is {A} most likely to raise?',
             ask='Discuss whether {A} can rely on the defence of diminished responsibility.',
             law=['s2 Homicide Act 1957 (as amended by s52 CJA 2009): abnormality of mental functioning from a recognised medical condition', 'it must substantially impair D\'s ability to understand his conduct, form a rational judgement or exercise self-control (R v Golds: important or weighty)', 'it must provide an explanation for the killing', 'D must prove it on the balance of probabilities; intoxication does not prevent the defence (R v Dietschmann)'],
             apply=['{cond} is a recognised medical condition', 'medical evidence must show it substantially impaired {A}\'s abilities', '{A} {drink}; under Dietschmann the jury asks whether the condition itself substantially impaired {A}'],
             concl='{A} has a good argument for diminished responsibility, which would reduce murder to voluntary manslaughter if proved on the balance of probabilities')],
  ev=[('Evaluate the extent to which the Coroners and Justice Act 2009 has improved the law on loss of control.', ['loss of control need not be sudden, helping abused victims', 'fear of serious violence trigger', 'revenge excluded', 'sexual infidelity excluded'],
       ['R v Clinton allows infidelity as context, undermining the exclusion', '"extremely grave" and "justifiable sense" are vague', 'still requires loss of control, which may not fit slow-burn cases', 'the normal person test may be hard to apply'],
       ['Coroners and Justice Act 2009 ss54-56', 'R v Clinton (2012)', 'R v Jewell (2014)', 'R v Dawes (2013)', 'R v Ahluwalia (1992)'], 'the Act improved the old provocation defence but problems of interpretation remain'),
      ('Evaluate the law on diminished responsibility.', ['the 2009 reform uses modern medical terms', 'recognised medical condition gives clearer basis', 'Golds clarified "substantially"', 'allows sentencing flexibility'],
       ['burden of proof on the defendant may be unfair', 'heavy reliance on psychiatric experts', 'difficulty with intoxication (Dietschmann)', 'developmental immaturity in young defendants is not covered'],
       ['Homicide Act 1957 s2', 'Coroners and Justice Act 2009 s52', 'R v Byrne (1960)', 'R v Golds (2016)', 'R v Dietschmann (2003)'], 'the reformed defence is clearer and more medically based, though some criticisms remain')])

T(7, 'Involuntary manslaughter: unlawful act and gross negligence manslaughter', area='involuntary manslaughter',
  defs=[('involuntary manslaughter', 'An unlawful killing where the defendant did not have the mens rea for murder, including unlawful act manslaughter and gross negligence manslaughter.'),
        ('unlawful act manslaughter', 'Manslaughter where the defendant kills by an unlawful (criminal) act which is objectively dangerous, also called constructive manslaughter.'),
        ('gross negligence manslaughter', 'Manslaughter where the defendant owed the victim a duty of care, breached it, the breach caused death, there was an obvious and serious risk of death and the negligence was so bad as to be criminal (R v Adomako).'),
        ('dangerous act', 'An act that all sober and reasonable people would recognise must subject the victim to the risk of some harm, though not necessarily serious harm (R v Church).')],
  mcqs=[('Which case sets out the test for gross negligence manslaughter?', 'R v Adomako (1994)', ['R v Church (1966)', 'DPP v Newbury and Jones (1976)', 'R v Lamb (1967)'], 'Adomako: duty, breach, causing death, gross negligence; risk of death (Misra and Srivastava).'),
        ('In R v Lamb (1967), why was there no unlawful act manslaughter?', 'There was no unlawful act because the victim did not fear any force, so there was no assault', ['The act was not dangerous', 'The defendant owed no duty of care', 'The death was caused by a third party'], 'Lamb: a joke with a revolver, no assault and no mens rea for one.'),
        ('In DPP v Newbury and Jones (1976), which point was decided?', 'The defendant need not foresee that the act might cause harm; the test of dangerousness is objective', ['An omission can be the unlawful act', 'Gross negligence requires a risk of death', 'The victim must be aware of the danger'], 'Boys pushed a paving stone off a bridge onto a train.'),
        ('In R v Rose (2017), why was the optometrist not guilty of gross negligence manslaughter?', 'The risk of death must be obvious and serious from information available at the time of the breach', ['She owed no duty of care to the patient', 'Her negligence did not cause the death', 'Optometrists cannot commit manslaughter'], 'Rose: reasonably foreseeable risk based on what was known at the time.'),
        ('Which case held that an omission cannot be the unlawful act for unlawful act manslaughter?', 'R v Lowe (1973)', ['R v Watson (1989)', 'R v Goodfellow (1986)', 'R v Kennedy (No 2) (2007)'], 'Failing to call a doctor for a child was gross negligence, not an unlawful act.')],
  cases=[('R v Church (1966)', 'after a fight the defendant threw the unconscious victim into a river, believing her dead, and she drowned', 'an act is dangerous if all sober and reasonable people would recognise the risk of some harm'),
         ('R v Lamb (1967)', 'the defendant pointed a revolver at his friend as a joke, not understanding how the chamber rotated, and shot him dead', 'there must be an unlawful act; with no fear of force there was no assault and so no unlawful act'),
         ('DPP v Newbury and Jones (1976)', 'two teenage boys pushed a paving stone off a railway bridge onto a train, killing the guard', 'the defendant need not foresee any harm; dangerousness is judged objectively'),
         ('R v Watson (1989)', 'burglars broke into the house of a frail 87-year-old man, who died of a heart attack 90 minutes later', 'the act becomes dangerous once the reasonable person present would realise the victim\'s frailty'),
         ('R v Dawson (1985)', 'robbers threatened a petrol station attendant with a replica gun and he died of a heart attack due to an unknown heart condition', 'the reasonable person has the same knowledge as the defendant; the victim\'s hidden condition made the act not dangerous'),
         ('R v Goodfellow (1986)', 'the defendant set fire to his council house to be rehoused, and his wife, child and another woman died', 'the unlawful act need not be aimed at the victim; criminal damage endangering life was dangerous'),
         ('R v Adomako (1994)', 'an anaesthetist failed to notice for six minutes that a tube supplying oxygen to a patient had become disconnected, and the patient died', 'gross negligence manslaughter requires a duty of care, breach, death caused by the breach and negligence so bad that it should be criminal'),
         ('R v Misra and Srivastava (2004)', 'two doctors failed to diagnose and treat a severe infection in a patient after surgery, and he died', 'for gross negligence manslaughter there must be an obvious and serious risk of death, not merely of injury'),
         ('R v Wacker (2003)', 'a lorry driver smuggling 60 illegal immigrants closed the air vent and 58 died', 'a duty of care can exist even if the parties were engaged in a joint illegal enterprise'),
         ('R v Rose (2017)', 'an optometrist failed to examine a boy\'s optic nerve properly and missed a fatal condition', 'the serious and obvious risk of death must be foreseeable from the information available at the time of the breach')],
  ars=[('A defendant can be guilty of unlawful act manslaughter without foreseeing any harm.', 'Dangerousness is judged by the sober and reasonable person (R v Church; DPP v Newbury and Jones).', 'A'),
       ('Gross negligence manslaughter requires a risk of serious injury.', 'R v Misra and Srivastava (2004) requires an obvious and serious risk of death.', 'D'),
       ('A civil wrong can be the unlawful act for unlawful act manslaughter.', 'R v Franklin (1883) held that the unlawful act must be a crime.', 'D')],
  exps=[('Explain the elements of unlawful act manslaughter.', 'An unlawful act that is a crime (Franklin, Lamb), not an omission (Lowe); the act must be dangerous on the objective test (Church, Newbury and Jones); and it must cause death (Kennedy); D must have the mens rea for the unlawful act.', '1 mark unlawful (criminal) act; 1 mark dangerous; 1 mark causes death; 1 mark MR of unlawful act. [4]'),
        ('Explain the test for gross negligence manslaughter set out in R v Adomako.', 'D owed the victim a duty of care; D breached the duty; the breach caused death; there was an obvious and serious risk of death (Misra); and the negligence was so bad that the jury considers it criminal.', '1 mark duty; 1 mark breach; 1 mark causation; 1 mark gross (jury question)/risk of death. [4]'),
        ('Explain why gross negligence manslaughter has been criticised as circular.', 'The jury is asked whether the negligence was so bad as to be criminal, so in effect it decides that conduct is criminal because it is criminal; this leaves the definition vague and outcomes inconsistent.', '1 mark: circular test explained; 1 mark: consequence – uncertainty/inconsistency. [2]')],
  cmps=[('unlawful act manslaughter', 'gross negligence manslaughter', ['unlawful act manslaughter requires a criminal act, gross negligence manslaughter a breach of a duty of care which can be an omission', 'unlawful act manslaughter needs only a risk of some harm, gross negligence a serious and obvious risk of death'])],
  scen=[dict(facts='{A} {act} {B} outside a shop in {city}. {B}, who {cond}, {res} and died.',
             slots={'act': [('punched', 'battery'), ('threatened with an imitation gun', 'assault'), ('threw a brick through the window of a house occupied by', 'criminal damage')],
                    'cond': [('had a heart condition that nobody could have seen', 'unknown to {A} (R v Dawson)'), ('was 90 years old and obviously frail', 'obvious to any reasonable person present (R v Watson)'), ('was a healthy 25-year-old', 'irrelevant to dangerousness')],
                    'res': ['suffered a heart attack', 'fell and hit their head on the pavement']},
             issue='unlawful act manslaughter', wrong=['gross negligence manslaughter', 'loss of control', 'murder with oblique intention'],
             iq='Which offence is {A} most likely to be charged with?',
             ask='Discuss whether {A} is guilty of unlawful act manslaughter.',
             law=['there must be an unlawful act that is a crime (R v Lamb; R v Franklin)', 'the act must be dangerous: sober and reasonable people would recognise the risk of some harm (R v Church; DPP v Newbury and Jones)', 'the reasonable person knows what D knew or would have seen (R v Dawson; R v Watson)', 'the act must cause the death, and D need not foresee harm'],
             apply=['{A}\'s act was a {act_1}, a criminal act', '{B}\'s condition was {cond_1}', 'the jury must decide whether a sober and reasonable person would recognise a risk of some harm from the act', 'causation: {B}\'s death followed the act; the thin skull rule applies'],
             concl='{A} is likely to be guilty of unlawful act manslaughter if the act was dangerous in the Church sense; the victim\'s condition being {cond_1} affects this'),
        dict(facts='{A} is {role}. {A} {breach}. As a result, {B} died.',
             slots={'role': [('a lifeguard at a pool in {city}', 'contract of employment'), ('an electrician who installed wiring in {B}\'s home', 'contractual duty to a customer'), ('a nurse caring for {B} on a hospital ward', 'doctor/nurse-patient relationship (Adomako)')],
                    'breach': [('ignored repeated alarms and warnings for over an hour', 'gross'), ('made a single minor error that an experienced colleague might also have made', 'probably not gross')]},
             issue='gross negligence manslaughter', wrong=['unlawful act manslaughter', 'murder', 'diminished responsibility'],
             iq='Which offence is {A} most likely to be charged with?',
             ask='Discuss whether {A} is guilty of gross negligence manslaughter.',
             law=['R v Adomako (1994): duty of care, breach, causing death, and negligence so gross it should be criminal', 'there must be an obvious and serious risk of death (Misra and Srivastava), foreseeable at the time of breach (R v Rose)', 'a duty can exist even in an illegal enterprise (R v Wacker)'],
             apply=['{A} owed {B} a duty as {role} ({role_1})', '{A} {breach}, which is a breach', 'the negligence is {breach_1}, so the jury will decide whether it was so bad as to be criminal'],
             concl='{A} owed and breached a duty; liability depends on the jury finding the negligence gross: here it is {breach_1}')],
  ev=[('Evaluate the law on involuntary manslaughter.', ['covers a wide range of culpable killings', 'Adomako test applies across professions', 'objective dangerousness protects victims'],
       ['unlawful act manslaughter can convict for minor acts causing unforeseen death (e.g. one-punch cases)', 'Adomako test is circular', 'the wide range of conduct under one label is unfair', 'Law Commission (2006) proposed reform'],
       ['R v Church (1966)', 'DPP v Newbury and Jones (1976)', 'R v Adomako (1994)', 'R v Misra and Srivastava (2004)', 'R v Rose (2017)'], 'the law is broad and flexible but uncertain and potentially harsh; reform is desirable')])

T(7, 'General defences: self-defence, duress and necessity', area='general defences',
  defs=[('self-defence', 'A complete defence where D uses force that is necessary, and reasonable in the circumstances as D believed them to be, to protect himself or others or property (s76 Criminal Justice and Immigration Act 2008).'),
        ('duress by threats', 'A defence where D commits a crime because of a threat of death or serious injury to himself or someone for whom he is responsible, and a sober person of reasonable firmness would have acted in the same way (R v Graham; R v Hasan).'),
        ('duress of circumstances', 'A defence where D commits an offence to avoid death or serious injury threatened by the circumstances rather than by a person (R v Willer; R v Martin 1989).'),
        ('necessity', 'A defence where D commits an offence to avoid a greater evil; recognised only in very limited circumstances (Re A (Conjoined Twins)) and not a defence to murder (R v Dudley and Stephens).')],
  mcqs=[('Which case established that duress is not a defence to murder?', 'R v Howe (1987)', ['R v Graham (1982)', 'R v Hasan (2005)', 'R v Willer (1986)'], 'Howe: no duress for murder; Gotts extended it to attempted murder.'),
        ('In householder cases, under s76(5A) Criminal Justice and Immigration Act 2008, force is not reasonable if it is:', 'grossly disproportionate', ['at all disproportionate', 'used inside the house', 'used against an intruder'], 'Added by the Crime and Courts Act 2013.'),
        ('In R v Hasan (2005), the House of Lords held that duress is not available where the defendant:', 'voluntarily associated with criminals and foresaw or ought to have foreseen the risk of being subjected to compulsion by threats of violence', ['was threatened with death', 'committed robbery', 'was under 18'], 'Voluntary association with criminals excludes duress.'),
        ('Which case established that a defendant who uses force under an honest mistake about the facts is judged on the facts as he believed them to be?', 'R v Gladstone Williams (1984)', ['R v Clegg (1995)', 'R v Martin (Anthony) (2001)', 'R v Bird (1985)'], 'The mistake need only be honest, not reasonable (unless caused by voluntary intoxication).'),
        ('In R v Dudley and Stephens (1884), the court held that:', 'necessity is not a defence to murder', ['necessity is always a defence', 'duress of circumstances applies to murder', 'killing to survive is self-defence'], 'Shipwrecked sailors who killed and ate the cabin boy were guilty of murder.')],
  cases=[('R v Gladstone Williams (1984)', 'the defendant saw a man struggling with a youth and punched him, believing a mugging was taking place, when in fact the man was arresting the youth', 'the defendant is judged on the facts as he honestly believed them to be, even if the belief is unreasonable'),
         ('R v Martin (Anthony) (2001)', 'a farmer shot two burglars in his isolated farmhouse, killing one', 'the reasonableness of force is judged objectively; a psychiatric condition is not relevant to whether force was reasonable'),
         ('R v Clegg (1995)', 'a soldier fired at a car that had driven through a checkpoint, killing a passenger after the car had passed', 'where excessive force is used, self-defence fails completely and there is no partial defence reducing murder to manslaughter'),
         ('R v Bird (1985)', 'a girl hit a man in the face with a glass when he slapped her and pushed her against a wall', 'there is no duty to retreat, though willingness to retreat is evidence of reasonableness'),
         ('R v Graham (1982)', 'the defendant helped his violent partner kill his wife, claiming he was afraid of him', 'duress requires that D reasonably believed there was a threat of death or serious injury and a sober person of reasonable firmness would have responded in the same way'),
         ('R v Hasan (2005)', 'a man working for a drug dealer was forced to commit a burglary under threats', 'duress is not available where D voluntarily associated with criminals and foresaw or ought to have foreseen the risk of being subjected to threats of violence'),
         ('R v Howe (1987)', 'the defendants took part in killings after threats from a violent man', 'duress is not a defence to murder, whether as principal or secondary party'),
         ('R v Willer (1986)', 'the defendant drove on the pavement to escape a gang of youths threatening violence', 'duress of circumstances can be a defence where D acts to avoid a threat of death or serious injury'),
         ('R v Martin (Colin) (1989)', 'the defendant drove while disqualified because his wife threatened suicide unless he drove their son to work', 'duress of circumstances applies where D reasonably believes his actions are necessary to avoid death or serious injury'),
         ('R v Dudley and Stephens (1884)', 'shipwrecked sailors killed and ate the cabin boy to survive', 'necessity is not a defence to murder'),
         ('Re A (Conjoined Twins) (2000)', 'doctors sought permission to separate conjoined twins, knowing one twin would die but both would die without the operation', 'necessity justified the operation in these exceptional circumstances')],
  ars=[('Self-defence is a complete defence.', 'If successful, self-defence results in an acquittal.', 'A'),
       ('A defendant who uses force must always try to retreat first.', 'In R v Bird (1985) the court held there is no duty to retreat.', 'D'),
       ('Duress can be a defence to attempted murder.', 'R v Gotts (1992) held that duress is not available for attempted murder.', 'D')],
  exps=[('Explain the requirements of self-defence.', 'The force must be necessary, judged on the facts as D honestly believed them (Gladstone Williams; s76(3)-(4)); and the amount of force must be reasonable in those circumstances, judged objectively (s76(6); Martin), or not grossly disproportionate in householder cases (s76(5A)).', '1 mark necessity; 1 mark honest belief; 1 mark reasonable force objective; 1 mark householder rule. [4]'),
        ('Explain the two-part test for duress from R v Graham (1982).', 'Subjective: was D compelled to act because he reasonably believed there was a threat of death or serious injury? Objective: would a sober person of reasonable firmness, sharing D\'s characteristics, have responded in the same way?', '1 mark subjective test; 1 mark objective test; 1 mark relevant characteristics. [3]'),
        ('Explain why duress is not a defence to murder.', 'The House of Lords in R v Howe held that the law should not allow a person to take an innocent life to save their own; ordinary people are expected to be heroic in such cases, and allowing the defence could help terrorists and gangs.', '1 mark: sanctity of innocent life; 1 mark: policy/risk of abuse. [2]')],
  cmps=[('duress by threats', 'duress of circumstances', ['duress by threats arises from a person\'s threat to make D commit a specific crime, duress of circumstances from a dangerous situation', 'both require a threat of death or serious injury and the Graham test']),
        ('self-defence', 'duress', ['self-defence involves using force against the attacker, duress involves committing a crime against an innocent person', 'self-defence is available for murder, duress is not'])],
  scen=[dict(facts='{A} was walking home in {city} when {B} {threat}. {A} {resp}.',
             slots={'threat': ['approached shouting and holding a broken bottle', 'grabbed {A}\'s bag and raised a fist', 'appeared to reach into a pocket for a weapon, though {B} was actually holding a phone'],
                    'resp': [('pushed {B} away, causing {B} to fall and break an arm', 'probably reasonable force'), ('punched {B} once to escape', 'probably reasonable force'), ('knocked {B} down and then kicked {B} repeatedly while {B} lay on the ground', 'excessive force once the threat had ended (R v Clegg)')]},
             issue='self-defence', wrong=['duress by threats', 'necessity', 'loss of control'],
             iq='Which defence is {A} most likely to raise?',
             ask='Discuss whether {A} can rely on self-defence.',
             law=['common law and s76 Criminal Justice and Immigration Act 2008: force must be necessary and reasonable', 'necessity judged on the facts as D honestly believed them (R v Gladstone Williams), even if mistaken', 'the amount of force is judged objectively in those circumstances, allowing for the heat of the moment (s76(7))', 'no duty to retreat (R v Bird); excessive force means the defence fails completely (R v Clegg)'],
             apply=['{A} honestly believed an attack was imminent, so force was necessary on the facts as {A} believed them', '{A} {resp}, which is {resp_1}'],
             concl='if the force was reasonable, {A} has a complete defence; here the response looks like {resp_1}'),
        dict(facts='{B}, a member of a gang that {A} had {assoc}, told {A}: "{threat}" {A} then {crime}.',
             slots={'assoc': [('joined voluntarily to sell drugs', 'voluntary association, which excludes duress (R v Hasan)'), ('never had any contact with before', 'no voluntary association')],
                    'threat': [('Rob that shop tonight or I will kill your brother.', 'a threat of death to a family member'), ('Steal that car or I will tell everyone your secrets.', 'a threat to reveal secrets, which is not a threat of death or serious injury')],
                    'crime': ['robbed a shop in {city} that night', 'stole a car from a car park the next day']},
             issue='duress by threats', wrong=['self-defence', 'necessity', 'involuntary intoxication'],
             iq='Which defence is {A} most likely to raise?',
             ask='Discuss whether {A} can rely on the defence of duress.',
             law=['threat of death or serious injury to D or someone for whom D is responsible (R v Graham; R v Hasan)', 'two-part test: reasonable belief in the threat; a sober person of reasonable firmness would have acted the same way', 'no reasonable opportunity for evasive action, e.g. going to the police', 'not available if D voluntarily associated with criminals (R v Hasan) or for murder/attempted murder (Howe; Gotts)'],
             apply=['the threat was {threat_1}', '{A} had {assoc}: {assoc_1}', 'the delay before the crime may have given {A} a chance to go to the police'],
             concl='duress is available only if the threat was of death or serious injury and there was no voluntary association; here the threat was {threat_1} and there was {assoc_1}')],
  ev=[('Evaluate the law on self-defence.', ['subjective belief protects those who make honest mistakes', 'objective reasonableness prevents excessive violence', 'householder rule supports people defending their homes'],
       ['all-or-nothing: excessive force leads to murder conviction (Clegg)', 'householder "grossly disproportionate" test is controversial', 'difficulty of judging force in the heat of the moment'],
       ['R v Gladstone Williams (1984)', 'R v Martin (Anthony) (2001)', 'R v Clegg (1995)', 's76 CJIA 2008', 'Crime and Courts Act 2013'], 'the law is broadly fair but the lack of a partial defence for excessive force is a weakness'),
      ('"Duress should be available as a defence to murder." Discuss.', ['a person under extreme threat lacks real choice', 'the law expects heroism', 'Law Commission recommended it as a full or partial defence'],
       ['sanctity of innocent life (Howe)', 'risk that criminals and terrorists would exploit it', 'sentencing can reflect pressure in other offences'],
       ['R v Howe (1987)', 'R v Gotts (1992)', 'R v Hasan (2005)', 'Law Commission report (2006)'], 'there is a strong case for at least a partial defence of duress to murder')])

T(7, 'Capacity defences: insanity, automatism and intoxication', area='capacity defences',
  defs=[('insanity', 'A defence under the M\'Naghten Rules (1843) where, at the time of the act, D was labouring under a defect of reason from a disease of the mind so as not to know the nature and quality of the act or that it was wrong.'),
        ('disease of the mind', 'A legal concept covering any internal cause of a malfunctioning of the mind, whether physical or mental, such as arteriosclerosis (R v Kemp), epilepsy (R v Sullivan) or hyperglycaemia (R v Hennessy).'),
        ('non-insane automatism', 'A complete defence where D\'s act was involuntary because of a total loss of control caused by an external factor, such as a blow to the head or an insulin injection (R v Quick).'),
        ('specific intent offence', 'An offence such as murder, s18 or theft for which voluntary intoxication can be a defence if it means D did not form the required intent (DPP v Majewski).'),
        ('basic intent offence', 'An offence such as manslaughter, s47, s20 or assault for which voluntary intoxication is no defence, because becoming intoxicated is itself reckless (DPP v Majewski).')],
  mcqs=[('What verdict is returned when the defence of insanity succeeds?', 'Not guilty by reason of insanity (the special verdict)', ['Guilty of manslaughter', 'Not guilty, with no further orders possible', 'Guilty but insane'], 'Under the Criminal Procedure (Insanity and Unfitness to Plead) Act 1991 the judge can make a hospital order, supervision order or absolute discharge.'),
        ('In R v Hennessy (1989), a diabetic who had not taken insulin (hyperglycaemia) was treated as:', 'insane, because the cause was internal', ['an automaton, because the cause was external', 'involuntarily intoxicated', 'having no defence at all, because diabetes is not a disease'], 'Compare R v Quick (hypoglycaemia caused by insulin = external).'),
        ('Which case established the rule that voluntary intoxication is no defence to a basic intent offence?', 'DPP v Majewski (1977)', ['R v Kingston (1994)', 'R v Hardie (1984)', 'Attorney-General for Northern Ireland v Gallagher (1963)'], 'Majewski: getting drunk is a reckless course of conduct.'),
        ('In R v Kingston (1994), the defendant\'s drink was spiked and he then committed an indecent assault. Why was he guilty?', 'He still formed the intent; a drunken intent is still an intent', ['Involuntary intoxication is never a defence', 'The offence was strict liability', 'He was voluntarily intoxicated'], 'Involuntary intoxication helps only if D did not form the mens rea.'),
        ('In R v Windle (1952), what did the court say "wrong" means in the M\'Naghten Rules?', 'Legally wrong', ['Morally wrong only', 'Against religious teaching', 'Socially unacceptable'], 'If D knew the act was against the law, the defence fails.')],
  cases=[('M\'Naghten\'s Case (1843)', 'the defendant, suffering from paranoid delusions, shot and killed the Prime Minister\'s secretary, thinking he was the Prime Minister', 'the M\'Naghten Rules: D must prove a defect of reason from a disease of the mind so that he did not know the nature and quality of his act or that it was wrong'),
         ('R v Kemp (1957)', 'a man suffering from arteriosclerosis attacked his wife with a hammer during a blackout', 'a disease of the mind can be a physical condition affecting the mind; the condition of the brain is irrelevant'),
         ('R v Sullivan (1984)', 'during an epileptic fit the defendant kicked a man in the head', 'epilepsy is a disease of the mind, so the defence is insanity, not automatism'),
         ('R v Hennessy (1989)', 'a diabetic who had not taken his insulin drove a stolen car while hyperglycaemic', 'high blood sugar caused by the disease itself is an internal cause, so the defence is insanity'),
         ('R v Burgess (1991)', 'the defendant attacked his girlfriend with a bottle and a video recorder while sleepwalking', 'sleepwalking caused by an internal factor is a disease of the mind, leading to the insanity defence'),
         ('R v Quick (1973)', 'a diabetic nurse attacked a patient while hypoglycaemic after taking insulin and not eating', 'a malfunction caused by an external factor such as insulin can support non-insane automatism'),
         ('Attorney-General\'s Reference (No 2 of 1992) (1993)', 'a lorry driver crashed into a car on the hard shoulder after "driving without awareness"', 'automatism requires a total destruction of voluntary control; reduced or partial control is not enough'),
         ('R v Bailey (1983)', 'a diabetic attacked his ex-partner\'s new boyfriend after taking insulin but not eating enough', 'self-induced automatism is a defence to a basic intent offence if D was not reckless in becoming an automaton'),
         ('DPP v Majewski (1977)', 'the defendant, having taken drugs and alcohol, attacked people in a pub and police officers', 'voluntary intoxication is no defence to a basic intent offence'),
         ('Attorney-General for Northern Ireland v Gallagher (1963)', 'the defendant decided to kill his wife, bought a knife and whisky, and drank the whisky for "Dutch courage" before killing her', 'where D forms the intent before becoming intoxicated, intoxication is no defence'),
         ('R v Kingston (1994)', 'the defendant\'s coffee was secretly drugged and he then indecently assaulted a boy', 'involuntary intoxication is no defence if D still formed the mens rea; a drunken intent is still an intent'),
         ('R v Hardie (1984)', 'the defendant took Valium belonging to his ex-partner to calm down and then started a fire in a wardrobe', 'taking a sedative drug that is normally expected to calm is not reckless, so the intoxication can be treated as involuntary'),
         ('R v Lipman (1970)', 'after taking LSD the defendant killed his girlfriend believing he was fighting snakes at the centre of the earth', 'voluntary intoxication is no defence to manslaughter, a basic intent offence')],
  ars=[('A defendant who knew his act was against the law cannot rely on insanity.', 'In R v Windle (1952) "wrong" in the M\'Naghten Rules was held to mean legally wrong.', 'A'),
       ('A diabetic who becomes hypoglycaemic after taking insulin may rely on non-insane automatism.', 'In R v Quick (1973) the cause of the malfunction was external.', 'A'),
       ('Voluntary intoxication is a defence to all offences.', 'Under DPP v Majewski, voluntary intoxication can only be a defence to specific intent offences.', 'D')],
  exps=[('Explain the difference between insanity and non-insane automatism.', 'Both involve a malfunction of the mind, but insanity arises from an internal cause (a disease of the mind, e.g. Sullivan, Hennessy) and leads to the special verdict, while non-insane automatism arises from an external cause (Quick) and leads to a complete acquittal.', '1 mark internal v external cause; 1 mark example of each; 1 mark consequences of each verdict. [3]'),
        ('Explain the rules on voluntary intoxication.', 'For specific intent offences, intoxication is a defence if D did not form the intent (Sheehan and Moore), but not if D formed the intent before drinking (Gallagher); for basic intent offences it is no defence because becoming intoxicated is reckless (Majewski; Lipman).', '1 mark specific intent rule; 1 mark Gallagher/drunken intent; 1 mark basic intent rule with case. [3]'),
        ('Explain why the insanity defence is criticised.', 'The legal definition of disease of the mind differs from medical definitions, so diabetics, epileptics and sleepwalkers are labelled insane; the label is stigmatising; the internal/external distinction produces arbitrary results (Hennessy v Quick).', '1 mark per criticism, up to 3. [3]')],
  cmps=[('specific intent offences', 'basic intent offences', ['for specific intent offences voluntary intoxication can negate mens rea, for basic intent offences it cannot', 'examples: murder, s18, theft (specific); manslaughter, s20, s47, assault (basic)']),
        ('R v Quick (1973)', 'R v Hennessy (1989)', ['in Quick hypoglycaemia was caused by insulin (external) giving automatism, in Hennessy hyperglycaemia was caused by diabetes (internal) giving insanity', 'Quick could be acquitted outright, Hennessy faced the special verdict'])],
  scen=[dict(facts='{A}, who has diabetes, {cause} and became confused. In this state {A} hit {B}, a colleague, causing a broken nose.',
             slots={'cause': [('injected insulin and skipped lunch', 'external (insulin), so non-insane automatism (R v Quick)', 'a complete acquittal, unless self-induced recklessly (R v Bailey)'), ('forgot to take insulin for two days', 'internal (the diabetes itself), so insanity (R v Hennessy)', 'the special verdict of not guilty by reason of insanity')]},
             issue='the distinction between insanity and non-insane automatism', wrong=['voluntary intoxication', 'diminished responsibility', 'duress of circumstances'],
             iq='Which defence issue is raised by these facts?',
             ask='Discuss which defence {A} may rely on and its effect.',
             law=['insanity: defect of reason from a disease of the mind (internal cause) so that D did not know the nature and quality of the act or that it was wrong (M\'Naghten; Sullivan; Hennessy)', 'non-insane automatism: total loss of control caused by an external factor (Hill v Baxter; Quick; A-G\'s Ref No 2 of 1992)', 'self-induced automatism is no defence to basic intent offences if D was reckless (R v Bailey)'],
             apply=['{A} {cause}', 'the cause was {cause_1}'],
             concl='{A} is likely to rely on {cause_1}, leading to {cause_2}'),
        dict(facts='{A} drank {drink} at a party in {city}. {A} then {act}.',
             slots={'drink': [('a large amount of vodka', 'voluntary'), ('several cans of strong beer and some wine', 'voluntary')],
                    'act': [('stabbed {B} in the chest, and {B} died; {A} says that because of the alcohol {A} did not intend to kill or seriously injure {B}', 'murder, a specific intent offence', 'if {A} did not form the intent, murder fails but manslaughter (basic intent) remains (Majewski; Lipman)'),
                            ('punched {B}, causing a black eye', 's47 ABH, a basic intent offence', 'voluntary intoxication is no defence (Majewski)')]},
             issue='intoxication as a defence', wrong=['insanity', 'loss of control', 'necessity'],
             iq='Which defence issue is raised by these facts?',
             ask='Discuss whether {A}\'s intoxication provides a defence.',
             law=['voluntary intoxication: a defence to specific intent offences only if D did not form the intent (Sheehan and Moore); no defence to basic intent offences (Majewski)', 'Dutch courage is no defence (Gallagher)', 'involuntary intoxication: a defence only if D lacked mens rea; a drunken intent is still an intent (Kingston)'],
             apply=['the intoxication was {drink_1}', 'the offence is {act_1}', '{act_2}'],
             concl='the effect of the voluntary intoxication depends on whether the offence is of specific or basic intent: {act_2}'),
        dict(facts='At a party in {city}, someone secretly added {sub} to {A}\'s soft drink. {A} then {act}.',
             slots={'sub': ['a strong sedative', 'a large measure of vodka', 'a recreational drug'],
                    'act': [('punched {B}, a stranger, causing a cut eye; {A} remembers wanting to hit {B} but says that sober {A} would never have done it', 'intended the act, so the intoxication is no defence (R v Kingston)'),
                            ('lashed out wildly while barely conscious and hit {B}, with no awareness of what was happening', 'may have lacked mens rea entirely, so involuntary intoxication can be a defence')]},
             issue='involuntary intoxication', wrong=['voluntary intoxication under DPP v Majewski', 'insanity', 'duress of circumstances'],
             iq='Which defence issue is raised by these facts?',
             ask='Discuss whether {A} has a defence based on intoxication.',
             law=['intoxication is involuntary where D did not know they were taking an intoxicant (spiked drinks) or took a sedative in the normal way (R v Hardie)', 'involuntary intoxication is a defence to any offence if D did not form the mens rea', 'a drunken intent is still an intent (R v Kingston)'],
             apply=['the drink was spiked, so the intoxication was involuntary', '{A} {act_1}'],
             concl='{A} {act_1}')],
  ev=[('Evaluate the law on insanity.', ['protects society while recognising lack of fault', 'flexible disposals since the 1991 Act', 'clear historic rules'],
       ['legal definition out of line with medicine', 'diabetics and epileptics labelled insane', 'internal/external distinction arbitrary (Quick v Hennessy)', 'stigma; few defendants use it', 'Law Commission proposed a new "recognised medical condition" defence (2013)'],
       ['M\'Naghten (1843)', 'R v Kemp (1957)', 'R v Sullivan (1984)', 'R v Hennessy (1989)', 'R v Burgess (1991)', 'R v Quick (1973)'], 'the law is outdated and in need of reform'),
      ('Evaluate the rules on intoxication as a defence.', ['Majewski protects the public from drunken violence', 'policy that self-induced intoxication should not excuse', 'specific intent offences have fallback basic intent offences'],
       ['Majewski is illogical: recklessness in drinking is not the same as recklessness at the time of the offence', 'specific/basic intent distinction is unclear', 'Kingston seems harsh'],
       ['DPP v Majewski (1977)', 'R v Lipman (1970)', 'A-G for Northern Ireland v Gallagher (1963)', 'R v Kingston (1994)', 'R v Hardie (1984)'], 'the rules are driven by policy rather than principle but protect the public')])
