"""Cambridge International A Level Global Perspectives & Research 9239 (A Level, grade 12), taught as
'political science': Component 4, the Research Report (up to 5,000 words plus research log).

Chapters: choosing a research question and planning (topic choice, question, proposal, ethics);
research methods and sources (literature review, primary methods, evaluating methods and data,
analysing and synthesising evidence); writing the report and reflecting (structure, sustained
argument, referencing and academic style, research log). Items are written in the style of the
C1 written paper (source/data-based structured questions, extended answers with level keys) applied
to research on political and governance issues. Shared issue packs and helpers come from the AS module.
"""
from ._lib import compose, person, city, fmt
from .g11_political_science import (cap, low, T, lm, levels, Q, MC, add_terms, add_mcqs, add_ar, add_claims, essay_q,  # noqa: F401
                                    table, pct, ISSUES, issue, COUNTRIES, PARTIES, SRC_HIGH, SRC_MID, SRC_LOW, SURN, PUBS,
                                    JOURNALS, ref_book, IDEOLOGIES)

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}


def keyterm(q):
    for t, how in [('responsibility', 'distinguish legal duty from moral obligation and say whose responsibility is meant'),
                   ('benefits', 'state benefits for whom, measured how and over what time period'),
                   ('best', 'set criteria such as effectiveness, cost and legitimacy'),
                   ('effective', 'state measurable criteria, e.g. change in the number of cases or in public trust'),
                   ('legal', 'specify which body of law (national or international) is meant')]:
        if t in q.lower():
            return f'“{t}”: {how}.'
    return '“should”: set out the criteria (effectiveness, rights, cost, legitimacy) by which the answer will be judged.'


def rq(r, i):
    a = r.choice(i['actions'])
    return r.choice([i['q'], f'To what extent is it the responsibility of the {a[1]} to address {i["name"]}?',
                     f'How far do the benefits outweigh the drawbacks of the proposal that the {a[1]} should {a[0]}?',
                     f'To what extent is {i["name"]} best addressed through national rather than international action?'])


# ============================================================== CHAPTER 1: Choosing a question and planning

d1a = T('Choosing a topic: personal interest, academic context and feasibility', 'choosing a topic personal interest academic context feasibility')
add_terms(d1a, [
    ('feasibility', 'whether a research project can be completed with the time, sources, skills and word count available'),
    ('academic context', 'the existing body of research, theory and debate in which a topic sits'),
    ('scope', 'the boundaries of a research project: the places, groups, time period and aspects it covers'),
    ('originality', 'the extent to which a project offers a new angle, case or combination of perspectives'),
    ('research report', 'the A Level Component 4 piece of independent research of up to 5,000 words, accompanied by a research log'),
])
add_mcqs(d1a, 'C1', (1, 2, 3), [
    ('What is the maximum length of the A Level Global Perspectives & Research report?', '5,000 words', ['2,000 words', '3,500 words', '8,000 words'], 'The research report is up to 5,000 words.'),
    ('Which document must accompany the Component 4 research report?', 'A research log', ['A video presentation', 'A team reflection', 'A press release'], 'Candidates submit the report with a research log.'),
])
FEAS = [  # (feature, helps?)
    ('there are many peer-reviewed studies and official reports on the issue', True),
    ('the student can interview local councillors who have agreed to take part', True),
    ('the only relevant data are held in a classified government archive', False),
    ('the topic is so new that almost nothing has been written about it', False),
    ('the student would need to travel to several countries to collect data', False),
    ('there is a clear academic debate with contrasting perspectives', True),
]


@d1a.add('C1', (1, 2, 3), 'mcq')
def d1a_feas(r, D):
    i = issue(r)
    good = [f for f, h in FEAS if h]
    bad = [f for f, h in FEAS if not h]
    if r.random() < 0.5:
        return MC(r, f'{person(r)} is considering a research report on {i["name"]}. Which finding makes the topic most feasible?', cap(r.choice(good)),
                  [cap(x) for x in bad], 'Feasibility depends on access to sufficient credible sources and data within the time available.')
    return MC(r, f'{person(r)} is considering a research report on {i["name"]}. Which finding most reduces the feasibility of the topic?', cap(r.choice(bad)),
              [cap(x) for x in good], 'Lack of access to data, or the need for unrealistic fieldwork, makes a topic unfeasible.')


@d1a.add('C2', (1, 2, 3, 4), 'explain')
def d1a_interest(r, D):
    i = issue(r)
    f = r.choice([('personal interest', 'it sustains motivation over many months of independent work, and prior knowledge helps the student ask better questions',
                   'it may lead to bias if the student already holds strong views'),
                  ('academic context', 'an existing debate provides theories, studies and contrasting perspectives to analyse',
                   'a crowded field may make it hard to find an original angle'),
                  ('feasibility', 'the student can actually obtain enough credible evidence within the time and word limit',
                   'focusing only on feasibility may produce a safe but unoriginal question')])
    return Q(f'Explain why {f[0]} matters when choosing a topic such as {i["name"]} for the research report, and identify one risk.',
             f'{cap(f[1])}. Risk: {f[2]}.', '1 mark why it matters; 1 mark developed; 1 mark risk [3]', 3, 'explain')


@d1a.add('C3', (2, 3, 4, 5), 'numerical')
def d1a_score(r, D):
    iss = r.sample(ISSUES, 3)
    w = r.choice([[1, 2, 3], [2, 2, 3], [1, 3, 2], [2, 1, 3]])
    crit = ['personal interest', 'academic debate', 'feasibility']
    sc = [[r.randint(2, 5) for _ in crit] for _ in iss]
    tot = [sum(a * b for a, b in zip(s, w)) for s in sc]
    if len(set(tot)) < 3:
        return None
    best = max(range(3), key=lambda j: tot[j])
    p = person(r)
    tab = table(['Topic'] + [f'{c} (weight {x})' for c, x in zip(crit, w)], [[iss[j]['name']] + sc[j] for j in range(3)])
    stem = f'{p} scores three possible research topics from 1 to 5 against weighted criteria. {tab} Calculate the weighted score for each topic and identify the topic {p} should choose.'
    ans = '; '.join(f'{iss[j]["name"]}: ' + ' + '.join(f'{s}×{x}' for s, x in zip(sc[j], w)) + f' = {tot[j]}' for j in range(3)) + f'. Choose: {iss[best]["name"]}.'
    key = '1 mark method; 1 mark all totals; 1 mark choice'
    m = 3
    if D >= 4:
        stem += ' Explain why the weights chosen are themselves a judgement that should be justified in the research log.'
        ans += ' The weights reflect what the student values (e.g. feasibility over interest); different weights could change the choice, so the reasoning should be recorded and justified.'
        key += '; 1 mark weights are value judgements; 1 mark could change outcome / record in log'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@d1a.add('C3', (2, 3, 4, 5), 'case')
def d1a_case(r, D):
    i = issue(r)
    p = person(r)
    hi = r.choice(SRC_HIGH)
    intro = (f'{p} lives in {city(r)} and has followed debates about {i["name"]} for two years. A first search finds {hi[0]} and several news reports, '
             f'but little local data. {p} wants to research “{i["name"]}” for the research report.')
    parts = [
        lambda r: ('Explain one advantage of choosing a topic of personal interest.', 'Motivation is sustained over a long project and existing knowledge helps frame good questions.', '1 mark advantage; 1 mark developed [2]'),
        lambda r: ('Explain why the topic needs to be narrowed.', f'“{cap(i["name"])}” is too broad for 5,000 words; narrowing to a country, group, time period or policy allows depth and a clear debate.', '1 mark too broad; 1 mark how narrowing helps [2]'),
        lambda r: ('Suggest one way to narrow the topic.', f'Focus on one course of action, e.g. whether the {i["actions"][0][1]} should {i["actions"][0][0]}, in a specified region.', '1 mark [1]'),
        lambda r: ('Assess the feasibility of the topic.', f'Feasible in terms of secondary sources ({hi[0]}) but limited local data; primary research or a narrower comparative focus may be needed.', '1 mark strength; 1 mark limitation; 1 mark judgement [3]'),
        lambda r: ('Identify two perspectives the report could compare.', f'{cap(i["persp"][0][0])}; {i["persp"][1][0]}.', '1 mark each [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d1a.add('C4', (2, 3, 4, 5), 'long')
def d1a_essay(r, D):
    i = issue(r)
    return essay_q(r, D, 'feasibility should be the most important factor when choosing a research report topic',
                   ['A topic without accessible evidence cannot be researched properly.', 'Time and word limits are fixed.'],
                   ['Without interest, motivation fades over a long project.', 'A topic needs a genuine academic debate and alternative perspectives.'],
                   f'Feasibility is a necessary condition, but the best topics, e.g. on {i["name"]}, combine interest, debate and access to evidence.')


d1b = T('Formulating a focused research question that permits debate and alternative perspectives', 'formulating a focused research question that permits debate and alternative perspectives')
add_terms(d1b, [
    ('research question', 'the single, focused question the research report sets out to answer'),
    ('alternative perspectives', 'different, reasoned positions on the question, which the report must identify and evaluate'),
    ('key term', 'a word in the question, such as “effective” or “responsibility”, whose meaning must be defined and made measurable'),
    ('operationalise', 'to define a concept so that it can be measured or assessed with evidence'),
], D1=(1, 2), D2=(1, 2, 3))
WEAK12 = {
    'descriptive': ('It invites description rather than evaluation of a debate', lambda i: f'What are the main features of {i["name"]}?'),
    'closed': ('It has a single factual answer, so no alternative perspectives are possible', lambda i: f'In which year was the first international agreement on {i["name"]} signed?'),
    'broad': ('It is far too broad to answer in depth in 5,000 words', lambda i: f'How can the world solve all political problems?'),
    'biased': ('It is worded to assume the answer', lambda i: f'Why is it obviously right that {i["arg"]["conc"]}?'),
    'vague': ('It leaves its key terms undefined, so it cannot be answered with evidence', lambda i: f'Is {i["name"]} good or bad?'),
}


@d1b.add('C1', (1, 2, 3), 'mcq')
def d1b_best(r, D):
    i = issue(r)
    ks = r.sample(list(WEAK12), 3)
    return MC(r, f'Which research question on {i["name"]} best permits debate and alternative perspectives?', rq(r, i), [WEAK12[k][1](i) for k in ks],
              'A focused, contestable question with a global dimension permits alternative perspectives to be evaluated.')


@d1b.add('C2', (1, 2, 3), 'mcq')
def d1b_weak(r, D):
    i = issue(r)
    k = r.choice(list(WEAK12))
    return MC(r, f'A proposed research question is: “{WEAK12[k][1](i)}” What is its main weakness?', WEAK12[k][0], [v[0] for kk, v in WEAK12.items() if kk != k], WEAK12[k][0] + '.')


KEYTERMS = [('effective', 'state measurable criteria, e.g. change in turnout or in the number of cases'), ('responsibility', 'distinguish legal duty from moral obligation'),
            ('benefits', 'specify for whom and over what time period'), ('best addressed', 'set criteria such as effectiveness, cost and legitimacy')]


@d1b.add('C2', (1, 2, 3, 4), 'explain')
def d1b_terms(r, D):
    i = issue(r)
    a = r.choice(i['actions'])
    t, how = r.choice(KEYTERMS)
    qq = {'effective': f'How effective would it be for the {a[1]} to {a[0]}?', 'responsibility': f'To what extent is it the responsibility of the {a[1]} to address {i["name"]}?',
          'benefits': f'How far do the benefits outweigh the drawbacks of the proposal that the {a[1]} should {a[0]}?',
          'best addressed': f'To what extent is {i["name"]} best addressed through national rather than international action?'}[t]
    return Q(f'A student’s research question is “{qq}” Explain why the term “{t}” must be defined in the report, and suggest how.',
             f'“{cap(t)}” can be understood in different ways, so perspectives may talk past each other and the judgement cannot be tested; the student should {how}.',
             '1 mark ambiguity; 1 mark consequence for judgement; 1 mark sensible definition/criteria [3]', 3, 'explain')


@d1b.add('C3', (2, 3, 4, 5), 'explain')
def d1b_rewrite(r, D):
    i = issue(r)
    k = r.choice(list(WEAK12))
    m = 3 if D <= 3 else 4
    return Q(f'Rewrite this research question so that it is focused and permits alternative perspectives: “{WEAK12[k][1](i)}” Explain how your version improves on it.',
             f'e.g. “{rq(r, i)}” — the original {low(WEAK12[k][0])[3:]}; the new question is contestable, focused and can be answered using evidence from different perspectives (e.g. {i["persp"][0][0]} and {i["persp"][1][0]}).',
             '1 mark focused question; 1 mark contestable; 1 mark explains improvement' + ('; 1 mark names perspectives that could be compared' if m == 4 else '') + f' [{m}]', m, 'explain')


@d1b.add('C3', (2, 3, 4, 5), 'case')
def d1b_case(r, D):
    i = issue(r)
    q = rq(r, i)
    h1, h2 = r.sample(i['persp'], 2)
    intro = f'{person(r)}’s proposed research question is: “{q}”'
    parts = [
        lambda r: ('Identify two alternative perspectives the question permits.', f'{cap(h1[0])}: {h1[1]}; {h2[0]}: {h2[1]}.', '1 mark each [2]'),
        lambda r: ('Identify a key term that needs defining and suggest a definition.', keyterm(q), '1 mark term; 1 mark workable definition [2]'),
        lambda r: ('Explain why the question has a global dimension.', cap(i['global']) + '.', '1 mark global link; 1 mark developed [2]'),
        lambda r: ('Suggest how the scope could be narrowed further.', 'Limit to one region or set of countries and a time period, e.g. since 2015.', '1 mark [1]'),
        lambda r: ('Explain one type of primary research that could help answer the question.', 'e.g. a survey or interviews with stakeholders (students, officials, NGO workers) to explore perspectives locally.', '1 mark method; 1 mark relevance [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d1b.add('C4', (2, 3, 4, 5), 'long')
def d1b_essay(r, D):
    i = issue(r)
    return essay_q(r, D, '“to what extent” questions are always the best form of research question for the research report',
                   ['They invite judgement and the weighing of perspectives.', 'They allow a qualified conclusion.'],
                   ['Other forms (“Should…?”, “How far…?”) can be equally contestable.', 'A “to what extent” question can still be vague or too broad.'],
                   f'The form matters less than focus, contestability and defined terms; e.g. “{i["q"]}” works without that wording.')


d1c = T('The research proposal and planning: aims, timeline and supervision', 'research proposal planning aims timeline supervision')
add_terms(d1c, [
    ('research proposal', 'a plan setting out the question, aims, context, methods, sources, timeline and ethical considerations'),
    ('aim', 'a broad statement of what the research intends to achieve'),
    ('objective', 'a specific, measurable step towards achieving an aim'),
    ('timeline', 'a schedule of research tasks and deadlines'),
    ('supervisor', 'the teacher who gives general guidance on the research but does not write or correct the report'),
    ('milestone', 'a significant point in a project, such as completing the literature review'),
])
PROP = ['Research question', 'Aims and objectives', 'Context and rationale', 'Methods and sources', 'Timeline', 'Ethical considerations']
PROP_S = {
    'Research question': lambda i: f'“{i["q"]}”',
    'Aims and objectives': lambda i: f'To compare the perspectives of {i["persp"][0][0]} and {i["persp"][1][0]}, and to evaluate evidence on whether the {i["actions"][0][1]} should {i["actions"][0][0]}.',
    'Context and rationale': lambda i: f'The issue matters because {i["global"]}.',
    'Methods and sources': lambda i: 'A literature review of peer-reviewed studies and international reports, plus an online survey of 120 students.',
    'Timeline': lambda i: 'Weeks 1–4 literature review; weeks 5–7 survey; weeks 8–12 analysis and drafting.',
    'Ethical considerations': lambda i: 'Participants will give informed consent, remain anonymous and may withdraw at any time.',
}


@d1c.add('C1', (1, 2, 3), 'mcq')
def d1c_sec(r, D):
    i = issue(r)
    k = r.choice(PROP)
    return MC(r, f'A research proposal on {i["name"]} contains this text: {PROP_S[k](i)} Which section of the proposal is it?', k, r.sample([x for x in PROP if x != k], 3), f'{k}.')


add_mcqs(d1c, 'C1', (1, 2, 3), [
    ('What is the appropriate role of a supervisor in the research report?', 'To give general guidance and feedback without writing or correcting the report', ['To rewrite weak sections of the report', 'To choose the research question for the student', 'To collect primary data for the student'], 'The report must be the student’s own work; supervisors guide.'),
    ('Which of these is an objective rather than an aim?', 'To survey 100 students about their voting intentions by the end of March', ['To understand youth political participation', 'To explore perspectives on democracy', 'To contribute to the debate about voting rights'], 'Objectives are specific, measurable and time-bound.'),
])


@d1c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d1c_backplan(r, D):
    i = issue(r)
    due = r.choice([20, 22, 24, 26])
    tasks = [('literature review', r.randint(3, 6)), ('primary research', r.randint(2, 4)), ('analysis', r.randint(2, 3)), ('drafting', r.randint(3, 5)), ('editing and referencing', r.randint(1, 2))]
    tot = sum(d for _, d in tasks)
    if tot >= due:
        return None
    start = due - tot
    lst = ', '.join(f'{t} {d} week' + ('s' if d != 1 else '') for t, d in tasks)
    if D <= 2:
        return MC(r, f'The research report on {i["name"]} is due at the end of week {due}. Tasks, done one after another: {lst}. What is the latest week by the end of which the student must start?',
                  f'Week {start}', [f'Week {start + 1}', f'Week {max(0, start - 2)}', f'Week {tot}'], f'Total {tot} weeks; {due} − {tot} = {start}.')
    stem = (f'A student’s report on {i["name"]} must be submitted at the end of week {due}. Tasks, done in sequence: {lst}. The supervisor advises leaving 2 weeks’ contingency. '
            'Calculate the total time needed and the latest week by the end of which the student must start, including the contingency.')
    s2 = due - tot - 2
    if s2 < 0:
        return None
    ans = f'Total = {tot} weeks; with contingency {tot + 2} weeks; latest start = end of week {due} − {tot + 2} = week {s2}.'
    key = '1 mark total; 1 mark contingency added; 1 mark latest start'
    m = 3
    if D >= 4:
        stem += ' Explain why the contingency is important for primary research.'
        ans += ' Primary research is often delayed (low response rates, ethical approval, cancelled interviews), so slack protects the deadline.'
        key += '; 1 mark reason delays are likely; 1 mark effect on deadline'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@d1c.add('C2', (1, 2, 3, 4), 'explain')
def d1c_explain(r, D):
    i = issue(r)
    k = r.choice(['Timeline', 'Ethical considerations', 'Methods and sources', 'Aims and objectives'])
    why = {'Timeline': 'it breaks a long project into deadlines so that research, drafting and editing are all completed on time',
           'Ethical considerations': 'it shows potential harm to participants has been considered before any primary research is carried out',
           'Methods and sources': 'it shows how the question will be answered and whether the evidence needed is accessible',
           'Aims and objectives': 'it keeps the research focused on answering the question and gives measurable steps'}[k]
    return Q(f'Explain why a research proposal on {i["name"]} should include a section headed “{k}”.', cap(why) + '.',
             '1 mark purpose; 1 mark developed/applied [2]', 2, 'explain')


@d1c.add('C3', (2, 3, 4, 5), 'case')
def d1c_case(r, D):
    i = issue(r)
    p = person(r)
    missing = r.sample(['Timeline', 'Ethical considerations', 'Methods and sources'], 1)[0]
    present = [k for k in PROP if k != missing]
    intro = f'{p}’s draft research proposal on “{i["q"]}” contains these sections: ' + ', '.join(present) + '. '
    parts = [
        lambda r: ('Identify the missing section.', missing + '.', '1 mark [1]'),
        lambda r: ('Explain why the missing section is needed.', {'Timeline': 'Without deadlines the project may overrun; milestones allow progress to be checked with the supervisor.',
                                                                   'Ethical considerations': 'Primary research may affect participants; consent, anonymity and the right to withdraw must be planned.',
                                                                   'Methods and sources': 'The reader cannot judge whether the question can be answered without knowing what evidence will be used and how.'}[missing], '1 mark purpose; 1 mark consequence of omission [2]'),
        lambda r: ('Write one SMART objective for the research.', f'e.g. “By week 6, to review ten peer-reviewed studies on {i["name"]} from at least three regions.”', '1 mark specific/measurable; 1 mark time-bound [2]'),
        lambda r: ('Explain how the supervisor can help without compromising the independence of the research.', 'By giving general feedback on the plan and progress, asking questions and setting deadlines, but not writing, rewriting or correcting the report.', '1 mark appropriate help; 1 mark limit [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d1c.add('C4', (2, 3, 4, 5), 'long')
def d1c_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'a detailed research proposal is the key to a successful research report on {i["name"]}',
                   ['It clarifies the question, methods and sources before work begins.', 'A timeline and milestones prevent last-minute work.'],
                   ['Research often changes direction as evidence is found, so plans must be flexible.', 'Success depends on the quality of analysis and evaluation, which a plan cannot guarantee.'],
                   'A proposal is necessary but not sufficient; it should be revised as the research log records changes.')


d1d = T('Ethical considerations in independent research', 'ethical considerations in independent research', 'ethics')
ETH = {
    'Informed consent': 'participants agree to take part after being told the purpose of the research and what it involves',
    'Anonymity': 'participants’ names and identifying details are not included in the report',
    'Confidentiality': 'information given by participants is stored securely and not shared beyond the research',
    'Right to withdraw': 'participants can leave the research at any time and have their data removed',
    'Protection from harm': 'participants should not suffer physical or psychological harm, such as distress or embarrassment',
    'Avoiding deception': 'participants should not be misled about the purpose of the research',
}
d1d.fixed('C1', (1, 2), [(f'Which ethical principle requires that {d}?', k, f'{k}: {d}. [1]', [x for x in ETH if x != k]) for k, d in ETH.items()])
ETH_CASES = [
    ('Before a survey on {n}, {p} explains its purpose and asks each student to sign a form agreeing to take part.', 'Informed consent'),
    ('In a report on {n}, {p} refers to interviewees as “Councillor A” and “Councillor B”.', 'Anonymity'),
    ('{p} tells interviewees about {n} that they may stop the interview at any time and have their answers deleted.', 'Right to withdraw'),
    ('{p} keeps interview recordings about {n} on a password-protected drive and deletes them after the report is submitted.', 'Confidentiality'),
    ('{p} decides not to ask refugees in {c} to describe traumatic experiences when researching {n}.', 'Protection from harm'),
    ('{p} tells participants honestly that a survey in {c} is about attitudes to {n}, rather than calling it a “general opinion survey”.', 'Avoiding deception'),
]


@d1d.add('C1', (1, 2, 3), 'mcq')
def d1d_case_mcq(r, D):
    s, k = r.choice(ETH_CASES)
    i = issue(r)
    txt = s.replace('{n}', i['name']).replace('{p}', person(r)).replace('{c}', city(r))
    return MC(r, f'Which ethical principle is shown? “{txt}”', k, r.sample([x for x in ETH if x != k], 3), f'{k}: {ETH[k]}.')


@d1d.add('C2', (1, 2, 3, 4), 'explain')
def d1d_explain(r, D):
    i = issue(r)
    k = r.choice(list(ETH))
    return Q(f'A student plans interviews with people affected by {i["name"]}. Explain why {low(k)} is important and how the student could ensure it.',
             f'{k} means that {ETH[k]}; this protects participants and the credibility of the research. The student could explain it at the start, record it on a consent form and follow it when storing and reporting data.',
             '1 mark meaning; 1 mark why important; 1 mark practical step [3]', 3, 'explain')


add_claims(d1d, [
    ('If participants are anonymous, informed consent is not needed.', False, 'Consent and anonymity are separate principles; participants must still agree to take part knowing the purpose.'),
    ('Research with participants under 18 usually needs consent from a parent or guardian as well.', True, 'Young people are considered vulnerable; schools and ethics guidelines normally require parental consent.'),
    ('Using publicly available statistics raises no ethical issues at all.', False, 'Fewer issues arise, but the researcher must still represent the data honestly and cite sources.'),
    ('Ethical research protects both participants and the credibility of the findings.', True, 'Unethical methods can harm people and undermine trust in the results.'),
], D=(1, 2, 3, 4))


@d1d.add('C3', (2, 3, 4, 5), 'case')
def d1d_case(r, D):
    i = issue(r)
    p = person(r)
    intro = (f'{p} plans to research {i["name"]} by interviewing 15-year-old students at a school in {city(r)} and posting quotations with their first names on a public blog. '
             'The students will be told the interviews are “about school life”.')
    parts = [
        lambda r: ('Identify two ethical problems with the plan.', 'Deception (true purpose hidden); lack of anonymity (first names published); possible lack of parental consent for under-18s.', '1 mark each, max 2 [2]'),
        lambda r: ('Explain why consent from a parent or guardian may be needed.', 'Participants are under 18 and considered vulnerable, so school and ethical guidelines usually require parental consent in addition to their own.', '1 mark under-18/vulnerable; 1 mark guidelines [2]'),
        lambda r: ('Suggest how the plan could be changed to meet ethical standards.', 'Explain the true purpose, obtain written consent (and parental consent), anonymise quotations, store data securely and offer the right to withdraw.', '1 mark each change, max 3 [3]'),
        lambda r: ('Explain how unethical methods could reduce the value of the findings.', 'Deceived or identifiable participants may not answer honestly, and the report’s credibility would be undermined.', '1 mark honesty of answers; 1 mark credibility [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d1d.add('C4', (2, 3, 4, 5), 'long')
def d1d_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'ethical rules make it too difficult for students to research sensitive political issues such as {i["name"]}',
                   ['Consent and anonymity requirements limit who can be interviewed.', 'Some groups (refugees, officials) may be inaccessible or vulnerable.'],
                   ['Secondary sources and anonymised surveys still allow rigorous research.', 'Ethical rules protect participants and make findings more trustworthy.'],
                   'Ethics shape the methods rather than preventing research; good design can meet both aims.')


CHAPTERS[1] = [d1a, d1b, d1c, d1d]


# ============================================================== CHAPTER 2: Research methods and sources

def studies(r, i, n=3):
    """Fictional studies with authors, years, places and findings for synthesis items."""
    names = r.sample(SURN, n)
    ys = sorted(r.sample(range(2012, 2026), n))
    regs = r.sample(['Latin America', 'South-East Asia', 'West Africa', 'Western Europe', 'South Asia', 'the Middle East', 'East Africa', 'North America'], n)
    a = i['arg']
    finds = [f'evidence supporting the view that {a["ic"]}', f'evidence supporting the opposing view that {a["counter"]}', f'mixed results, depending on how strongly governments enforced the policy']
    r.shuffle(finds)
    return [(names[k], ys[k], regs[k], finds[k % 3]) for k in range(n)]


d2a = T('Literature review: identifying and engaging with academic sources', 'literature review academic sources')
add_terms(d2a, [
    ('literature review', 'a critical survey of existing research on a question, identifying debates, findings and gaps'),
    ('peer review', 'evaluation of a study by independent experts before publication'),
    ('research gap', 'an aspect of a question that existing research has not yet answered'),
    ('synthesis', 'combining findings from several sources to show patterns, agreements and disagreements'),
    ('grey literature', 'research published outside academic journals, such as reports by governments, NGOs and think tanks'),
    ('citation tracking', 'finding further sources by following the references in a useful article, or later works that cite it'),
])


@d2a.add('C1', (1, 2, 3), 'mcq')
def d2a_type(r, D):
    i = issue(r)
    j = r.choice(JOURNALS)
    kinds = [(f'an article on {i["name"]} in the peer-reviewed {j}', 'Academic, peer-reviewed source'),
             (f'a policy report on {i["name"]} published by an NGO', 'Grey literature'),
             (f'an opinion column on {i["name"]} in a daily newspaper', 'Journalistic opinion'),
             (f'raw responses from a survey the student carried out on {i["name"]}', 'Primary data')]
    s, k = r.choice(kinds)
    return MC(r, f'How should a researcher classify {s}?', k, [x for _, x in kinds if x != k], f'{k}.')


@d2a.add('C2', (1, 2, 3), 'mcq')
def d2a_synth(r, D):
    i = issue(r)
    st = studies(r, i, 2)
    (a, ya, ra, fa), (b, yb, rb, fb) = st
    ans = f'{a} ({ya}) and {b} ({yb}) reach different conclusions, possibly because they studied different regions ({ra} and {rb}).'
    ds = [f'{a} ({ya}) studied {ra}. {b} ({yb}) studied {rb}.', f'{b} ({yb}) is more recent, so {a} ({ya}) can be ignored.', f'Both studies prove that {i["arg"]["conc"]}.']
    return MC(r, f'{a} ({ya}), studying {ra}, found {fa}; {b} ({yb}), studying {rb}, found {fb}. Which sentence best synthesises these studies in a literature review on {i["name"]}?', ans, ds,
              'Synthesis compares and explains the relationship between findings rather than listing or dismissing them.')


@d2a.add('C2', (1, 2, 3, 4), 'explain')
def d2a_purpose(r, D):
    i = issue(r)
    return Q(r.choice([f'Explain two purposes of a literature review in a research report on {i["name"]}.', 'Explain why a literature review should do more than summarise sources one by one.']),
             'It places the question in its academic context and identifies the main debates and perspectives; it reveals gaps that the report can address; synthesis shows how findings relate, rather than listing them.',
             '1 mark each purpose, 1 mark each developed [4]', 4, 'explain')


@d2a.add('C3', (2, 3, 4, 5), 'case')
def d2a_case(r, D):
    i = issue(r)
    st = studies(r, i, 3)
    intro = f'A student researching “{rq(r, i)}” has read three studies. ' + ' '.join(f'{n} ({y}) studied {g} and found {f}.' for n, y, g, f in st)
    old = min(st, key=lambda x: x[1])
    parts = [
        lambda r: ('Identify one point of disagreement between the studies.', f'{st[0][0]} found {st[0][3]}, whereas {st[1][0]} found {st[1][3]}.', '1 mark identifies; 1 mark supported with authors [2]'),
        lambda r: ('Suggest one reason why the studies reached different conclusions.', 'Different regions and political contexts, different time periods, or different methods and definitions.', '1 mark reason; 1 mark linked to the studies [2]'),
        lambda r: ('Identify a possible research gap.', 'e.g. none of the studies examines the student’s own region, or recent years, or the perspective of the people most affected.', '1 mark [1]'),
        lambda r: (f'Explain one limitation of relying on {old[0]} ({old[1]}).', f'It is the oldest study ({old[1]}); circumstances, laws or technology may have changed since, so its findings may be out of date.', '1 mark currency; 1 mark applied [2]'),
        lambda r: ('Write a sentence that synthesises two of the studies.', f'e.g. “While {st[0][0]} ({st[0][1]}) found {st[0][3]}, {st[1][0]} ({st[1][1]}) found {st[1][3]}, suggesting that context shapes the outcome.”', '1 mark compares; 1 mark explains relationship [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d2a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d2a_count(r, D):
    i = issue(r)
    tot = r.choice([24, 30, 32, 36, 40])
    pr = r.randint(int(tot * 0.2), int(tot * 0.5))
    gl = r.randint(4, int(tot * 0.3))
    nw = tot - pr - gl
    old = r.randint(3, max(4, pr // 2))
    p = 100 * pr / tot
    stem = f'A student’s reading list on {i["name"]} has {tot} sources: {pr} peer-reviewed articles, {gl} reports by governments and NGOs, and {nw} news or opinion pieces.'
    if D <= 2:
        return MC(r, stem + ' What percentage of the sources are peer-reviewed?', pct(p), [pct(100 * gl / tot), pct(100 * nw / tot), pct(100 * pr / (tot - pr))], f'{pr}/{tot} × 100 = {pct(p)}.')
    stem += f' {old} of the peer-reviewed articles were published more than ten years ago. Calculate the percentage of sources that are peer-reviewed, and the percentage of the peer-reviewed articles that are more than ten years old. Comment on the balance of the reading list.'
    q = 100 * old / pr
    ans = f'{pr}/{tot} × 100 = {pct(p)} peer-reviewed; {old}/{pr} × 100 = {pct(q)} of these are over ten years old. ' + \
          ('Under half the list is academic, so the student should add more peer-reviewed research' if p < 50 else 'About half the list is academic') + \
          ', and recent studies are needed to keep the review current; news pieces are useful for perspectives but weaker as evidence.'
    m = 4
    return Q(stem, ans, f'1 mark peer-reviewed %; 1 mark old %; 1 mark comment on academic balance; 1 mark comment on currency [{m}]', m, 'numerical')


@d2a.add('C4', (2, 3, 4, 5), 'long')
def d2a_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'grey literature from NGOs and governments is as valuable as academic research for a report on {i["name"]}',
                   ['NGO and government reports are often more current and contain field data.', 'They reveal the perspectives of key stakeholders.'],
                   ['They are not peer reviewed and may reflect vested interests.', 'Academic research uses transparent methods and engages with theory.'],
                   'Grey literature is valuable for perspectives and recent data, but must be evaluated and corroborated against academic research.')


d2b = T('Primary research methods: surveys, interviews and experiments', 'primary research methods surveys interviews experiments')
add_terms(d2b, [
    ('primary research', 'collecting new data directly, for example through surveys, interviews or experiments'),
    ('closed question', 'a survey question with fixed answer options, which produces quantitative data'),
    ('open question', 'a question that lets respondents answer in their own words, producing qualitative data'),
    ('Likert scale', 'a rating scale, such as 1 (strongly disagree) to 5 (strongly agree), used to measure attitudes'),
    ('semi-structured interview', 'an interview with prepared questions but freedom to follow up interesting answers'),
    ('stratified sampling', 'dividing a population into groups and sampling from each in proportion to its size'),
    ('opportunity sampling', 'selecting whoever is available and willing at the time'),
])
QFAULTS = {
    'Leading question': lambda i: f'Don’t you agree that {i["arg"]["conc"]}?',
    'Double-barrelled question': lambda i: f'Do you think {i["name"]} is serious and that the {i["actions"][0][1]} should {i["actions"][0][0]}?',
    'Ambiguous question': lambda i: f'Do you often think about {i["name"]}?',
    'Loaded wording': lambda i: f'Should our weak and useless leaders finally do something about {i["name"]}?',
}
QFIX = {'Leading question': 'it suggests the expected answer', 'Double-barrelled question': 'it asks two things at once, so one answer cannot be interpreted',
        'Ambiguous question': '“often” means different things to different respondents', 'Loaded wording': 'emotive words push respondents towards one answer'}


@d2b.add('C1', (1, 2, 3), 'mcq')
def d2b_fault(r, D):
    i = issue(r)
    k = r.choice(list(QFAULTS))
    return MC(r, f'A draft survey question reads: “{QFAULTS[k](i)}” What is the main problem with it?', k, [x for x in QFAULTS if x != k] + ['Closed question'] if k != 'Ambiguous question' else [x for x in QFAULTS if x != k],
              f'{k}: {QFIX[k]}.')


@d2b.add('C1', (1, 2, 3), 'mcq')
def d2b_method(r, D):
    i = issue(r)
    tasks = [(f'to measure how many of 300 students support the proposal that the {i["actions"][0][1]} should {i["actions"][0][0]}', 'A questionnaire with closed questions'),
             (f'to explore in depth why a local councillor holds her views on {i["name"]}', 'A semi-structured interview'),
             (f'to test whether reading a fact-check changes how much people trust a false claim about {i["name"]}', 'An experiment with a control group'),
             (f'to understand how a group of young activists discuss {i["name"]} together', 'A focus group')]
    t, k = r.choice(tasks)
    return MC(r, f'A student wants {t}. Which method is most suitable?', k, [x for _, x in tasks if x != k], f'{k}.')


@d2b.add('C2', (1, 2, 3, 4), 'explain')
def d2b_rewrite(r, D):
    i = issue(r)
    k = r.choice(list(QFAULTS))
    return Q(f'Explain what is wrong with this survey question and rewrite it: “{QFAULTS[k](i)}”',
             f'{k}: {QFIX[k]}. Improved, e.g.: “To what extent do you agree or disagree that {i["arg"]["conc"]}? (Strongly agree / Agree / Neither / Disagree / Strongly disagree)”.',
             '1 mark identifies fault; 1 mark explains effect on data; 1 mark neutral, single, clear rewrite [3]', 3, 'explain')


@d2b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d2b_strat(r, D):
    i = issue(r)
    years = ['Year 10', 'Year 11', 'Year 12', 'Year 13']
    pops = [r.choice([120, 150, 160, 180, 200, 240]) for _ in years]
    N = sum(pops)
    n = r.choice([40, 50, 60, 80])
    ex = [p * n / N for p in pops]
    if any(abs(x - round(x)) > 1e-9 for x in ex):
        return None
    tab = table(['Year group'] + years, [['Students'] + pops])
    if D <= 2:
        j = r.randrange(4)
        return MC(r, f'A student surveys {n} students at a school about {i["name"]}, using a stratified sample by year group. {tab} How many {years[j]} students should be included?',
                  str(round(ex[j])), [str(round(n / 4)) if round(n / 4) != round(ex[j]) else str(round(ex[j]) + 2), str(pops[j] // 10), str(round(ex[j]) + 5)],
                  f'{pops[j]}/{N} × {n} = {fmt(round(ex[j]))}.')
    stem = f'A student plans a stratified sample of {n} students, by year group, for a survey on {i["name"]}. {tab} Calculate the number to sample from each year group.'
    ans = '; '.join(f'{y}: {p}/{N} × {n} = {fmt(round(x))}' for y, p, x in zip(years, pops, ex)) + '.'
    key = '1 mark method (proportion × sample size); 1 mark all values; 1 mark totals check to ' + str(n)
    m = 3
    if D >= 4:
        stem += ' Explain one advantage of stratified sampling over opportunity sampling here.'
        ans += ' Each year group is represented in proportion, so results are less biased than surveying whoever is available (e.g. only friends or one class).'
        key += '; 1 mark representativeness; 1 mark contrast with opportunity sampling bias'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@d2b.add('C3', (2, 3, 4, 5), 'case')
def d2b_case(r, D):
    i = issue(r)
    p = person(r)
    k = r.choice(list(QFAULTS))
    intro = (f'{p} is researching “{rq(r, i)}”. The plan is to hand out a questionnaire to friends in the school canteen, including the question “{QFAULTS[k](i)}”, '
             'and to interview one local politician.')
    parts = [
        lambda r: ('Identify the sampling method and one weakness.', 'Opportunity sampling: friends in the canteen are unlikely to represent all students.', '1 mark method; 1 mark weakness [2]'),
        lambda r: ('Explain the problem with the survey question.', f'{k}: {QFIX[k]}.', '1 mark fault; 1 mark effect on data [2]'),
        lambda r: ('Suggest one advantage of the interview.', 'It provides in-depth, qualitative insight into an expert/stakeholder perspective that a questionnaire cannot.', '1 mark [1]'),
        lambda r: ('Explain one limitation of interviewing only one politician.', 'One person represents only one perspective and may have a vested interest; findings cannot be generalised.', '1 mark one perspective/bias; 1 mark generalisation [2]'),
        lambda r: ('Suggest how the primary research could be improved.', 'Use a stratified or random sample; pilot neutral closed and Likert questions; interview people with contrasting perspectives.', '1 mark each improvement, max 3 [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d2b.add('C4', (2, 3, 4, 5), 'long')
def d2b_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'interviews are more useful than questionnaires for researching perspectives on {i["name"]}',
                   ['Interviews reveal reasons and values behind a perspective.', 'Follow-up questions clarify meaning.'],
                   ['Questionnaires reach larger, more representative samples.', 'Closed questions produce data that can be compared and analysed statistically.'],
                   'The best choice depends on the question; many reports combine both (triangulation).')


d2c = T('Evaluating methods, sources and data: credibility, reliability and limitations', 'evaluating methods sources data credibility reliability limitations')
add_terms(d2c, [
    ('reliability', 'the consistency of a method: whether it would give similar results if repeated'),
    ('validity', 'whether a method actually measures what it claims to measure'),
    ('generalisability', 'how far findings from a sample can be applied to a wider population'),
    ('sampling bias', 'distortion caused when the sample does not represent the population'),
    ('social desirability bias', 'the tendency of respondents to give answers that make them look good'),
    ('triangulation', 'using more than one method or source to check findings'),
    ('response rate', 'the percentage of people asked to take part who actually respond'),
], D1=(1, 2), D2=(1, 2, 3))
BIAS = [
    ('Students were asked in front of their teacher whether they had ever shared false news about {n}.', 'Social desirability bias'),
    ('An online poll about {n} was answered only by people who chose to visit a campaign website.', 'Self-selection (sampling) bias'),
    ('The interviewer nodded approvingly whenever a participant criticised the government’s policy on {n}.', 'Interviewer bias'),
    ('Only 12% of the people sent a questionnaire about {n} returned it.', 'Non-response bias'),
]


@d2c.add('C1', (1, 2, 3), 'mcq')
def d2c_bias(r, D):
    s, k = r.choice(BIAS)
    i = issue(r)
    return MC(r, f'Which problem is most likely to affect this research? “{s.replace("{n}", i["name"])}”', k, [x for _, x in BIAS if x != k], f'{k}.')


add_ar(d2c, [
    ('A method can be reliable without being valid.', 'A survey can give consistent results while measuring the wrong thing.', 'AR', 'Both true; R explains A.'),
    ('Triangulation strengthens research findings.', 'If different methods give the same result, the finding is less likely to be an artefact of one method.', 'AR', 'Both true; R explains A.'),
    ('A large sample always guarantees generalisable results.', 'Biased sampling methods can produce unrepresentative samples of any size.', 'R', 'A false; R true.'),
])


@d2c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d2c_moe(r, D):
    i = issue(r)
    n = r.choice([100, 400, 625, 900, 1600, 2500])
    moe = 100 / n ** 0.5
    sup = r.randint(48, 58)
    stem = (f'A survey of {n:,} randomly selected adults finds {sup}% support for the proposal that the {i["actions"][0][1]} should {i["actions"][0][0]}. '
            f'The approximate 95% margin of error is given by 1/√n × 100 percentage points.')
    if D <= 2:
        return MC(r, stem + ' What is the margin of error?', f'±{fmt(round(moe, 1))} percentage points', [f'±{fmt(round(100 / n, 2))} percentage points', f'±{fmt(round(moe * 2, 1))} percentage points', f'±{fmt(round(n ** 0.5, 1))} percentage points'],
                  f'1/√{n:,} × 100 = {fmt(round(moe, 1))}.')
    lo, hi = sup - moe, sup + moe
    stem += ' Calculate the margin of error and the likely range of true support. Can the researcher conclude that a majority supports the proposal?'
    maj = lo > 50
    ans = f'1/√{n:,} × 100 = ±{fmt(round(moe, 1))} points; range {fmt(round(lo, 1))}% to {fmt(round(hi, 1))}%. ' + \
          ('The whole range is above 50%, so a majority is likely.' if maj else 'The range includes 50% or less, so a majority cannot be concluded.')
    key = '1 mark margin; 1 mark range; 1 mark correct conclusion'
    m = 3
    if D >= 4:
        stem += ' Explain why the margin of error does not account for all sources of error.'
        ans += ' It covers random sampling error only, not bias from question wording, non-response or a non-random sample.'
        key += '; 1 mark only random error; 1 mark example of systematic bias'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@d2c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d2c_rr(r, D):
    i = issue(r)
    sent = r.choice([200, 250, 300, 400, 500])
    back = r.randint(int(sent * 0.15), int(sent * 0.6))
    rr = 100 * back / sent
    if D <= 2:
        return MC(r, f'A student emails a questionnaire about {i["name"]} to {sent} people and receives {back} replies. What is the response rate?', pct(rr),
                  [pct(100 * (sent - back) / sent), pct(100 * back / (sent + back)), f'{back}%'], f'{back}/{sent} × 100 = {pct(rr)}.')
    return Q(f'A student emails a questionnaire about {i["name"]} to {sent} people and receives {back} replies. Calculate the response rate and explain how non-response could affect the validity of the findings.',
             f'{back}/{sent} × 100 = {pct(rr)}. People who reply may differ from those who do not (e.g. more interested or with stronger views), so results may not represent the whole group.',
             '1 mark response rate; 1 mark non-respondents may differ; 1 mark effect on validity/generalisation [3]', 3, 'numerical')


@d2c.add('C2', (1, 2, 3, 4), 'explain')
def d2c_explain(r, D):
    i = issue(r)
    s = r.choice(SRC_HIGH + SRC_MID + SRC_LOW)
    return Q(f'A student uses {s[0]} as evidence in a report on {i["name"]}. Evaluate its credibility.', f'Strength: {s[1]}. Weakness: {s[2]}. It should be corroborated by independent evidence.',
             '1 mark strength; 1 mark weakness; 1 mark corroboration or judgement [3]', 3, 'explain')


@d2c.add('C3', (2, 3, 4, 5), 'case')
def d2c_case(r, D):
    i = issue(r)
    n = r.choice([40, 60, 80])
    intro = (f'A student researching {i["name"]} surveyed {n} classmates (opportunity sample) using Likert-scale questions, and interviewed one official from {i["persp"][0][0]}. '
             f'The student concludes that “people in our country support the view that {i["arg"]["conc"]}”.')
    parts = [
        lambda r: ('Explain one threat to the validity of the survey.', 'Classmates may answer to please the researcher (social desirability) or interpret questions differently.', '1 mark threat; 1 mark explained [2]'),
        lambda r: ('Explain why the conclusion cannot be generalised.', f'{n} classmates from one school are not representative of the national population (age, location, background).', '1 mark small/unrepresentative; 1 mark linked to “people in our country” [2]'),
        lambda r: ('Explain one limitation of the interview evidence.', f'One official represents one stakeholder with a possible vested interest ({i["persp"][0][2]}).', '1 mark one perspective; 1 mark vested interest [2]'),
        lambda r: ('Suggest how triangulation could strengthen the findings.', 'Compare the survey with national polls and peer-reviewed studies, and interview stakeholders with different perspectives.', '1 mark method; 1 mark how it checks findings [2]'),
        lambda r: ('Rewrite the conclusion so that it reflects the limitations of the data.', f'e.g. “Among the {n} classmates surveyed, most supported the view; this cannot be generalised to the national population.”', '1 mark qualified scope; 1 mark acknowledges limitation [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d2c.add('C4', (2, 3, 4, 5), 'long')
def d2c_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'student primary research adds little of value to a report on {i["name"]} compared with published research',
                   ['Student samples are small and unrepresentative.', 'Published research uses larger samples and peer-reviewed methods.'],
                   ['Primary research can explore a local context or perspective that published research ignores.', 'Triangulating local data with published studies can reveal differences.'],
                   'Primary research is most valuable when clearly limited in its claims and used alongside published evidence.')


d2d = T('Analysing data and synthesising evidence from different perspectives', 'analysing data synthesising evidence from different perspectives')
add_terms(d2d, [
    ('quantitative data', 'numerical data that can be counted or measured'),
    ('qualitative data', 'descriptive data, such as words from interviews, that explain meanings and reasons'),
    ('cross-tabulation', 'a table that shows how answers vary between groups of respondents'),
    ('mode', 'the most frequent value or answer in a data set'),
    ('thematic analysis', 'identifying recurring themes in qualitative data'),
], D1=(1, 2), D2=(1, 2, 3))


@d2d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d2d_cross(r, D):
    i = issue(r)
    g = r.choice([('Under 25', '25 and over'), ('Urban', 'Rural'), ('Students', 'Workers')])
    na, nb = r.choice([80, 100, 120, 150]), r.choice([60, 90, 140, 200])
    ya = r.randint(int(na * 0.3), int(na * 0.8)); yb = r.randint(int(nb * 0.3), int(nb * 0.8))
    pa, pb = 100 * ya / na, 100 * yb / nb
    if abs(pa - pb) < 3:
        return None
    tot = 100 * (ya + yb) / (na + nb)
    tab = table(['Group', 'Support', 'Total asked'], [[g[0], ya, na], [g[1], yb, nb]])
    stem = f'Survey results on whether the {i["actions"][0][1]} should {i["actions"][0][0]}: {tab}'
    if D <= 2:
        return MC(r, stem + f' What percentage of the {g[0]} group supports the proposal?', pct(pa), [pct(100 * ya / (na + nb)), pct(100 * ya / nb), pct(tot)], f'{ya}/{na} × 100 = {pct(pa)}.')
    stem += ' Calculate the percentage support in each group and overall. Explain why comparing the raw numbers who support the proposal would be misleading.'
    ans = (f'{g[0]}: {ya}/{na} = {pct(pa)}; {g[1]}: {yb}/{nb} = {pct(pb)}; overall {ya + yb}/{na + nb} = {pct(tot)}. '
           f'Groups are different sizes, so raw counts ({ya} vs {yb}) do not show relative support; percentages do.')
    key = '1 mark each group %; 1 mark overall %; 1 mark explains different group sizes'
    m = 4
    if D >= 4:
        stem += ' Suggest what qualitative evidence could explain the difference between the groups.'
        ans += ' Interviews or open responses could reveal the reasons (interests, values, experience) behind each group’s view.'
        key += '; 1 mark qualitative evidence explaining reasons'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@d2d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d2d_likert(r, D):
    i = issue(r)
    c = [r.randint(2, 20) for _ in range(5)]
    n = sum(c)
    mean = sum((k + 1) * x for k, x in enumerate(c)) / n
    mode = max(range(5), key=lambda k: (c[k], -k)) + 1
    if c.count(max(c)) > 1:
        return None
    labels = ['1 Strongly disagree', '2 Disagree', '3 Neutral', '4 Agree', '5 Strongly agree']
    tab = '; '.join(f'{l}: {x}' for l, x in zip(labels, c))
    stem = f'Respondents rated the statement “{cap(i["arg"]["conc"])}” on a 1–5 scale. Responses: {tab}.'
    if D <= 2:
        return MC(r, stem + ' What is the modal response?', labels[mode - 1], [l for k, l in enumerate(labels) if k != mode - 1], f'Most frequent = {labels[mode - 1]} ({c[mode - 1]}).')
    agree = 100 * (c[3] + c[4]) / n
    stem += ' Calculate the mean score and the percentage who agree or strongly agree. Explain one limitation of reporting only the mean.'
    ans = (f'Mean = ({" + ".join(f"{k + 1}×{x}" for k, x in enumerate(c))})/{n} = {fmt(round(mean, 2))}; agree/strongly agree = {c[3] + c[4]}/{n} = {pct(agree)}. '
           'The mean hides how opinions are spread (polarised vs neutral), and treats the scale as if gaps between points were equal.')
    return Q(stem, ans, '1 mark mean method; 1 mark mean; 1 mark agree %; 1 mark limitation [4]', 4, 'numerical')


@d2d.add('C2', (1, 2, 3, 4), 'explain')
def d2d_synth(r, D):
    i = issue(r)
    h1, h2 = r.sample(i['persp'], 2)
    return Q(f'A report on {i["name"]} includes evidence from {h1[0]} ({h1[1]}) and from {h2[0]} ({h2[1]}). Explain how the student could synthesise these perspectives rather than simply describe them.',
             f'Identify where they agree and disagree, explain why (e.g. {h1[2]}; {h2[2]}), weigh the quality of the evidence each uses, and combine insights into a judgement on the question.',
             '1 mark agreement/disagreement; 1 mark explains differences; 1 mark weighs evidence; 1 mark combined judgement [4]', 4, 'explain')


@d2d.add('C1', (1, 2, 3), 'mcq')
def d2d_type(r, D):
    i = issue(r)
    items = [(f'the percentage of respondents who agree that the {i["actions"][0][1]} should {i["actions"][0][0]}', 'Quantitative data'),
             (f'interview quotations explaining why people feel strongly about {i["name"]}', 'Qualitative data'),
             (f'a table showing support for the proposal broken down by age group', 'Cross-tabulation'),
             (f'recurring ideas identified across ten interview transcripts on {i["name"]}', 'Thematic analysis')]
    s, k = r.choice(items)
    return MC(r, f'In a research report, which term best describes {s}?', k, [x for _, x in items if x != k], f'{k}.')


@d2d.add('C4', (3, 4, 5), 'case')
def d2d_case4(r, D):
    i = issue(r)
    n1, n2 = r.choice([200, 300, 400]), r.choice([8, 10, 12])
    s1 = r.randint(52, 70)
    intro = (f'A student researching “{rq(r, i)}” has three kinds of evidence: a survey of {n1} adults ({s1}% support the proposal that the {i["actions"][0][1]} should {i["actions"][0][0]}); '
             f'{n2} interviews, mostly expressing the concern that {i["actions"][0][3]}; and a peer-reviewed study finding that {i["arg"]["ic"]}.')
    parts = [
        lambda r: ('Explain why the survey and interviews appear to disagree.', 'The survey measures overall support; interviewees, a smaller and possibly unrepresentative group, explain concerns. Support and concern can coexist.', '1 mark different measures; 1 mark sample difference [2]'),
        lambda r: ('Explain how qualitative evidence adds to the quantitative evidence.', 'It explains reasons and values behind the numbers, revealing concerns that a percentage hides.', '1 mark reasons; 1 mark example [2]'),
        lambda r: ('Evaluate which evidence should carry most weight in the conclusion.', 'The peer-reviewed study for effects (method checked, larger scale); the survey for public opinion; interviews for reasons. Weight depends on what part of the question is being answered.',
                   '1 mark evaluates each; 1 mark matches evidence to sub-question; 1 mark judgement [3]'),
        lambda r: ('Write a sentence that synthesises the three kinds of evidence.', f'e.g. “Although {s1}% of adults surveyed supported the proposal, interviewees worried that {i["actions"][0][3]}; the study suggests that {i["arg"]["ic"]}, so support may be justified if this concern is addressed.”',
                   '1 mark uses all three; 1 mark shows relationship; 1 mark leads to judgement [3]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


@d2d.add('C4', (2, 3, 4, 5), 'long')
def d2d_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'quantitative data are more persuasive than qualitative data in a report on {i["name"]}',
                   ['Numbers summarise large samples and can be compared.', 'Statistics appear objective to readers.'],
                   ['Qualitative data explain the reasons behind perspectives.', 'Numbers can mislead through sampling or presentation.'],
                   'Persuasiveness depends on quality and fit to the question; synthesis of both is strongest.')


CHAPTERS[2] = [d2a, d2b, d2c, d2d]


# ============================================================== CHAPTER 3: Writing the report and reflecting

RSEC = ['Introduction', 'Literature review and context', 'Methodology', 'Analysis and evaluation of perspectives', 'Conclusion and reflection']

d3a = T('Structuring a 5,000-word research report: introduction, analysis, evaluation and conclusion', 'structuring a 5,000-word research report introduction analysis evaluation conclusion')
add_terms(d3a, [
    ('methodology section', 'the part of a report that explains and justifies how evidence was gathered and analysed'),
    ('abstract', 'a short summary of a report’s question, methods, findings and conclusion'),
    ('analysis', 'examining evidence and arguments in detail to show how they bear on the question'),
    ('evaluation', 'judging the strength of arguments, evidence and methods'),
    ('signposting', 'phrases that guide the reader through the structure of the argument'),
])


@d3a.add('C1', (1, 2, 3), 'mcq')
def d3a_sec(r, D):
    i = issue(r)
    k = r.randrange(5)
    purpose = [f'Sets out the question “{i["q"]}”, its importance and how the report will answer it',
               f'Reviews existing research and debates on {i["name"]}',
               'Explains and justifies how the evidence was collected and analysed',
               f'Weighs the perspectives of {i["persp"][0][0]} and {i["persp"][1][0]} using evidence',
               'Answers the question with a supported judgement and reflects on the research process'][k]
    return MC(r, f'Which section of a research report would do this? “{purpose}.”', RSEC[k], [s for j, s in enumerate(RSEC) if j != k], f'{RSEC[k]}.')


@d3a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d3a_words(r, D):
    i = issue(r)
    shares = r.choice([[10, 20, 10, 50, 10], [8, 22, 10, 48, 12], [10, 18, 12, 50, 10], [10, 25, 10, 45, 10]])
    total = r.choice([4800, 5000])
    words = [total * s / 100 for s in shares]
    if any(abs(w - round(w)) > 1e-9 for w in words):
        return None
    tab = ', '.join(f'{s} {p}%' for s, p in zip(RSEC, shares))
    if D <= 2:
        j = r.choice([0, 1, 3])
        return MC(r, f'A {total:,}-word report on {i["name"]} is planned as: {tab}. How many words are planned for the {RSEC[j].lower()}?', f'{round(words[j]):,} words',
                  [f'{round(words[j] / 2):,} words', f'{round(total * (shares[j] + 10) / 100):,} words', f'{shares[j] * 10:,} words' if shares[j] * 10 != round(words[j]) else f'{round(words[j]) + 250:,} words'],
                  f'{shares[j]}% × {total:,} = {round(words[j]):,}.')
    drafted = [round(w + r.choice([-150, -50, 0, 100, 250, 400])) for w in words]
    dt = sum(drafted)
    stem = (f'A report on {i["name"]} was planned as {tab} of {total:,} words. The draft sections contain ' + ', '.join(f'{s} {d:,}' for s, d in zip(RSEC, drafted)) +
            ' words. Calculate the draft total and how many words must be cut, if any, to meet the 5,000-word limit. Identify the section furthest over its plan.')
    big = max(range(5), key=lambda j: drafted[j] - words[j])
    cut = max(0, dt - 5000)
    ov = drafted[big] - round(words[big])
    ans = f'Draft total = {dt:,} words; ' + (f'cut {cut:,} words.' if cut else 'within the limit.') + (f' Furthest over plan: {RSEC[big]} (+{ov:,}).' if ov > 0 else ' No section is over its planned length.')
    key = '1 mark total; 1 mark words to cut; 1 mark section identified'
    m = 3
    if D >= 4:
        stem += ' Explain why the analysis and evaluation section should normally be the largest.'
        ans += ' Most marks reward analysis, evaluation of perspectives and evidence, and a supported judgement, so space should go there rather than to description.'
        key += '; 1 mark marks for analysis/evaluation; 1 mark avoid description'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@d3a.add('C2', (1, 2, 3, 4), 'explain')
def d3a_method(r, D):
    i = issue(r)
    return Q(f'Explain why a research report on “{i["q"]}” needs a methodology section.',
             'It explains how evidence was found and analysed (search strategy, primary methods, sampling) and justifies these choices, so the reader can judge the reliability and limitations of the findings.',
             '1 mark describes content; 1 mark justification of choices; 1 mark allows reader to judge reliability [3]', 3, 'explain')


@d3a.add('C3', (2, 3, 4, 5), 'case')
def d3a_case(r, D):
    i = issue(r)
    intro = f'A student’s draft report on “{i["q"]}” spends 2,500 words describing the history of {i["name"]}, 1,500 words summarising sources one by one, and 800 words on a conclusion.'
    parts = [
        lambda r: ('Identify two problems with the structure.', 'Too much description; no clear methodology; sources summarised rather than compared; little analysis/evaluation.', '1 mark each [2]'),
        lambda r: ('Suggest a better structure for the report.', 'Introduction → literature review/context → methodology → analysis and evaluation of perspectives (largest section) → conclusion and reflection.', '1 mark logical order; 1 mark analysis/evaluation largest [2]'),
        lambda r: ('Explain how the student could turn the summary of sources into analysis.', 'Group sources by perspective or theme, compare their reasoning and evidence, and evaluate their credibility in relation to the question.', '1 mark compare; 1 mark evaluate [2]'),
        lambda r: ('Explain what the introduction should contain.', 'The question, why it matters (global significance), key terms defined, the perspectives to be compared and an outline of the approach.', '1 mark each element, max 3 [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d3a.add('C4', (2, 3, 4, 5), 'long')
def d3a_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'following a standard report structure limits the quality of independent research on issues such as {i["name"]}',
                   ['A fixed template can encourage box-ticking rather than original thinking.', 'Some questions suit a thematic rather than sectional structure.'],
                   ['A clear structure helps readers follow a long, complex argument.', 'Conventions such as a methodology section make the research transparent and checkable.'],
                   'Structure supports quality when adapted to the question; the argument, not the template, should drive organisation.')


d3b = T('Constructing a sustained argument and reaching a supported judgement', 'constructing a sustained argument and reaching a supported judgement')
add_terms(d3b, [
    ('sustained argument', 'a line of reasoning that is developed consistently through the whole report towards an answer to the question'),
    ('supported judgement', 'a conclusion that follows logically from the evidence and analysis presented'),
    ('counter-argument', 'a reasoned position against the report’s line of argument, which must be considered and answered'),
    ('qualification', 'a limitation stated in a judgement, such as the conditions under which it holds'),
], D1=(1, 2), D2=(1, 2, 3))
JFAULT = {
    'It introduces new evidence in the conclusion': lambda i: f'In conclusion, a new study I found last week shows that {i["arg"]["ic"]}, so {i["arg"]["conc"]}.',
    'It does not answer the question': lambda i: f'In conclusion, {i["name"]} is a complex issue with many perspectives.',
    'It overstates certainty': lambda i: f'In conclusion, this report has proved conclusively that {i["arg"]["conc"]}; no reasonable person could disagree.',
    'It contradicts the analysis in the report': lambda i: f'Although every section of this report found strong evidence against it, in conclusion {i["arg"]["conc"]}.',
}


def judgement(i):
    a = i['arg']
    return (f'On balance, this report concludes that {a["conc"]}, because {a["r1"]} and the evidence suggests that {a["ic"]}; however, this holds only if {a["assume"]}, '
            f'and the concern that {a["counter"]} remains significant.')


@d3b.add('C1', (1, 2, 3), 'mcq')
def d3b_best(r, D):
    i = issue(r)
    return MC(r, f'Which is the best final judgement for a report on “{i["q"]}”?', judgement(i), [f(i) for f in r.sample(list(JFAULT.values()), 3)],
              'A clear, qualified judgement following from the analysis.')


@d3b.add('C2', (1, 2, 3), 'mcq')
def d3b_fault(r, D):
    i = issue(r)
    k = r.choice(list(JFAULT))
    return MC(r, f'A report’s conclusion reads: “{JFAULT[k](i)}” What is the main weakness?', k, [x for x in JFAULT if x != k], f'{k}.')


@d3b.add('C2', (2, 3, 4), 'explain')
def d3b_counter(r, D):
    i = issue(r)
    a = i['arg']
    return Q(f'A report argues that {a["conc"]}. Explain how dealing with the counter-argument that {a["counter"]} can strengthen the report’s argument.',
             f'It shows the alternative perspective has been considered; answering it (e.g. {a["rebut"]}) removes an objection, and acknowledging what cannot be answered leads to a more credible, qualified judgement.',
             '1 mark shows balance; 1 mark answering removes objection; 1 mark qualification increases credibility [3]', 3, 'explain')


@d3b.add('C3', (2, 3, 4, 5), 'case')
def d3b_case(r, D):
    i = issue(r)
    a = i['arg']
    h1, h2 = r.sample(i['persp'], 2)
    intro = (f'A student’s report on “{i["q"]}” presents the perspective of {h1[0]} ({h1[1]}) in Section 2 and of {h2[0]} ({h2[1]}) in Section 3, '
             'then concludes in one sentence that “both sides have good points”.')
    parts = [
        lambda r: ('Explain why this is not a sustained argument.', 'The perspectives are described separately; there is no line of reasoning developed across the sections and no judgement.', '1 mark separate description; 1 mark no developing line/judgement [2]'),
        lambda r: ('Suggest how the student could compare the perspectives directly.', 'Organise by criteria (effectiveness, rights, cost), weighing each perspective’s reasoning and evidence under each.', '1 mark criteria; 1 mark weighing [2]'),
        lambda r: ('Write a supported final judgement.', judgement(i), '1 mark clear answer; 1 mark supported reason; 1 mark qualification [3]'),
        lambda r: ('Explain how the student should use evidence quality to decide between the perspectives.', f'Prefer the perspective supported by more credible, representative evidence (e.g. {a["ev"]}), while noting vested interests ({h1[2]}; {h2[2]}).', '1 mark credibility; 1 mark vested interest [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d3b.add('C4', (2, 3, 4, 5), 'long')
def d3b_essay(r, D):
    i = issue(r)
    a = i['arg']
    return essay_q(r, D, a['conc'], [cap(a['r1']) + '.', cap(a['r2']) + '.', cap(a['ev']) + '.'], [cap(a['counter']) + '.', f'The argument assumes that {a["assume"]}.'],
                   f'A sustained answer weighs the evidence and reaches a qualified judgement (response to objection: {a["rebut"]}).',
                   [f'the perspective of {i["persp"][0][0]}', f'the perspective of {i["persp"][1][0]}', 'the quality of the evidence'])


d3c = T('Referencing, academic style and the bibliography', 'referencing academic style bibliography')
add_terms(d3c, [
    ('bibliography', 'a list of all sources consulted, including some not cited in the text'),
    ('reference list', 'a list of all the sources cited in the text, in alphabetical order of author'),
    ('hedging', 'cautious language, such as “suggests” or “may”, that avoids overstating claims'),
    ('academic register', 'a formal, precise and objective style of writing'),
    ('secondary citation', 'citing a source you have not read through another author who quotes it, e.g. (Smith, 2010, cited in Jones, 2020)'),
], D1=(1, 2), D2=(1, 2, 3))


def ref_article(r, i):
    s1, s2 = r.sample(SURN, 2)
    a1, a2 = r.sample('ABCDEFGHJKLMNPRST', 2)
    y = r.randint(2012, 2025)
    j = r.choice(JOURNALS)
    v, n = r.randint(8, 40), r.randint(1, 4)
    p1 = r.randint(10, 300); p2 = p1 + r.randint(12, 30)
    t = f'{cap(i["name"])}: {r.choice(["a comparative analysis", "evidence and debates", "a cross-national study"])}'
    good = f'{s1}, {a1}. and {s2}, {a2}. ({y}) ‘{t}’, {j}, {v}({n}), pp. {p1}–{p2}.'
    bad = [f'{a1}. {s1} and {a2}. {s2} ({y}) ‘{t}’, {j}, {v}({n}), pp. {p1}–{p2}.', f'‘{t}’, {j} ({y}), {s1} and {s2}.', f'{s1}, {a1}. and {s2}, {a2}. ‘{t}’, {j}.']
    return dict(s1=s1, s2=s2, y=y, good=good, bad=bad, t=t, j=j, a1=a1, a2=a2, v=v, n=n, p1=p1, p2=p2)


@d3c.add('C1', (1, 2, 3), 'mcq')
def d3c_art(r, D):
    i = issue(r)
    a = ref_article(r, i)
    return MC(r, f'Which is the correct Harvard reference for a journal article by {a["a1"]}. {a["s1"]} and {a["a2"]}. {a["s2"]} ({a["y"]}), “{a["t"]}”, in {a["j"]}, volume {a["v"]}, issue {a["n"]}, pages {a["p1"]}–{a["p2"]}?',
              a['good'], a['bad'], 'Harvard article: Surname, Initial. and Surname, Initial. (Year) ‘Title’, Journal, volume(issue), pp. pages.')


@d3c.add('C1', (1, 2, 3), 'mcq')
def d3c_cite(r, D):
    i = issue(r)
    a = ref_article(r, i)
    kind = r.choice(['two', 'three', 'secondary'])
    if kind == 'two':
        return MC(r, f'Which is the correct Harvard in-text citation for a {a["y"]} article by {a["s1"]} and {a["s2"]}?', f'({a["s1"]} and {a["s2"]}, {a["y"]})',
                  [f'({a["a1"]}. {a["s1"]}, {a["y"]})', f'({a["s1"]}, {a["s2"]})', f'({a["y"]}, {a["s1"]} and {a["s2"]})'], 'Two authors: (Surname and Surname, year).')
    if kind == 'three':
        s3 = r.choice([x for x in SURN if x not in (a['s1'], a['s2'])])
        return MC(r, f'In many Harvard styles, how is a {a["y"]} source by {a["s1"]}, {a["s2"]} and {s3} cited in the text?', f'({a["s1"]} et al., {a["y"]})',
                  [f'({a["s1"]}, {a["s2"]}, {s3})', f'({s3} et al., {a["y"]})', f'(et al. {a["s1"]}, {a["y"]})'], 'Three or more authors: first author et al. (some styles list all three on first use).')
    return MC(r, f'A student read a quotation from {a["s1"]} ({a["y"] - 6}) inside a {a["y"]} book by {a["s2"]}, without reading {a["s1"]}’s original. Which citation is correct?',
              f'({a["s1"]}, {a["y"] - 6}, cited in {a["s2"]}, {a["y"]})', [f'({a["s1"]}, {a["y"] - 6})', f'({a["s2"]}, {a["y"] - 6})', f'({a["s1"]} and {a["s2"]}, {a["y"]})'],
              'Secondary citation: (Original, year, cited in Source read, year).')


STYLE = [
    ('This evidence suggests that the policy may have increased turnout among some groups.', ['This totally proves the policy was brilliant.', 'I reckon the policy worked loads.', 'Everyone knows the policy obviously worked.']),
    ('The data indicate a modest decline in public trust between 2015 and 2022.', ['Trust in government has completely collapsed.', 'People just don’t trust politicians any more, right?', 'Trust went down a bit, I think.']),
    ('Interview evidence indicates that some officials regard the reform as difficult to implement.', ['Officials basically hate the reform.', 'The reform is a total disaster, as anyone can see.', 'Loads of officials I spoke to were not keen.']),
    ('It could be argued that the evidence from a single country is insufficient to support a general conclusion.', ['One country proves nothing, obviously.', 'This evidence is useless.', 'I don’t really buy the evidence from that one country.']),
    ('Critics argue that the measure restricts freedom of expression.', ['Haters say the measure is rubbish.', 'Some people moan that the measure is bad.', 'Obviously the measure is an attack on freedom.']),
]


@d3c.add('C2', (1, 2, 3), 'mcq')
def d3c_style(r, D):
    i = issue(r)
    g, bad = r.choice(STYLE)
    return MC(r, f'In a research report on {i["name"]}, which sentence is written in the most appropriate academic style?', g, bad,
              'Formal register, hedged claim, no colloquial or absolute language.')


@d3c.add('C2', (2, 3, 4), 'explain')
def d3c_hedge(r, D):
    i = issue(r)
    a = i['arg']
    return Q(f'A student writes: “This proves that {a["ic"]}.” Explain why this should be rewritten using hedging language, and rewrite it.',
             f'One piece of evidence rarely proves a claim on a complex political issue; hedging reflects the strength of the evidence. Rewrite: “This suggests that {a["ic"]}.”',
             '1 mark evidence does not prove; 1 mark hedging matches strength of evidence; 1 mark acceptable rewrite [3]', 3, 'explain')


@d3c.add('C3', (1, 2, 3, 4, 5), 'short')
def d3c_order(r, D):
    i = issue(r)
    n = 4 if D <= 3 else 5
    names = r.sample(SURN, n)
    ys = [r.randint(2010, 2025) for _ in names]
    order = sorted(zip(names, ys))
    m = 2 if D <= 3 else 3
    return Q(f'The reference list of a report on {i["name"]} must include works by: ' + '; '.join(f'{s} ({y})' for s, y in zip(names, ys)) + '. Put them in the correct order for a Harvard reference list.',
             ', '.join(f'{s} ({y})' for s, y in order) + '.', 'Alphabetical by first author’s surname. ' + ('2 marks fully correct; 1 mark one pair out of order' if m == 2 else '3 marks fully correct; 2 marks one pair out of order; 1 mark first two correct') + f' [{m}]', m, 'short')


@d3c.add('C3', (2, 3, 4, 5), 'case')
def d3c_case(r, D):
    i = issue(r)
    b = ref_book(r, i)
    a = ref_article(r, i)
    yr = r.randint(2023, 2026)
    intro = (f'A student’s report on {i["name"]} uses a book by {b["ini"]}. {b["s"]} ({b["y"]}, {b["place"]}: {b["pub"]}), titled “{b["t"]}”, and a journal article by {a["s1"]} and {a["s2"]} ({a["y"]}). '
             f'It also uses a webpage from the UN website accessed on 3 March {yr}.')
    parts = [
        lambda r: ('Write the Harvard reference for the book.', b['good'], '1 mark author/year; 1 mark title; 1 mark place: publisher [3]'),
        lambda r: ('Write the in-text citation for the journal article.', f'({a["s1"]} and {a["s2"]}, {a["y"]})', '1 mark [1]'),
        lambda r: ('State two details that must be recorded for the webpage reference.', 'URL and date accessed (also author/organisation, year, title).', '1 mark each [2]'),
        lambda r: ('Explain the difference between a reference list and a bibliography.', 'A reference list contains only sources cited in the text; a bibliography may include all sources consulted.', '1 mark each [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d3c.add('C4', (2, 3, 4, 5), 'long')
def d3c_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'in a research report on {i["name"]}, academic style matters as much as content',
                   ['Precise, hedged language shows the strength of evidence accurately.', 'Consistent referencing makes the research checkable and credible.'],
                   ['A well-styled report with weak analysis remains weak.', 'Assessment rewards analysis, evaluation and judgement most.'],
                   'Style serves content: it cannot replace strong analysis, but poor style can undermine it.')


d3d = T('Keeping the research log and reflecting on the research process', 'research log reflecting on the research process')
add_terms(d3d, [
    ('research log', 'a record kept throughout the project of decisions, sources, meetings, problems and changes of direction'),
    ('reflexivity', 'awareness of how the researcher’s own perspective and choices may have shaped the research'),
    ('critical incident', 'a moment in the research that led to a significant decision or change'),
    ('reflection', 'evaluating the research process and one’s own learning in order to improve future work'),
], D1=(1, 2), D2=(1, 2, 3))
LOG = [
    ('Week {w}: Search on {n} returned too many results; narrowed by adding a country and date filter.', 'A change in search strategy'),
    ('Week {w}: Meeting with supervisor — advised narrowing the question on {n}; agreed new deadline for literature review.', 'A supervision meeting'),
    ('Week {w}: Only 18 of 150 survey replies about {n}; decided to add interviews to triangulate.', 'A change of method in response to a problem'),
    ('Week {w}: Realised my own support for one side of the debate on {n} may be shaping which sources I select.', 'Reflexivity about personal bias'),
]


@d3d.add('C1', (1, 2, 3), 'mcq')
def d3d_log(r, D):
    s, k = r.choice(LOG)
    i = issue(r)
    txt = s.replace('{w}', str(r.randint(2, 18))).replace('{n}', i['name'])
    return MC(r, f'What does this research log entry mainly record? “{txt}”', k, [x for _, x in LOG if x != k], f'{k}.')


@d3d.add('C2', (1, 2, 3, 4), 'explain')
def d3d_why(r, D):
    i = issue(r)
    return Q(r.choice([f'Explain two reasons why a student researching {i["name"]} should keep a detailed research log.', 'Explain why a research log is useful when writing the reflection at the end of the report.']),
             'It records decisions and reasons as they happen, so changes of direction can be explained and justified; it provides evidence for honest reflection on methods, problems and learning; it shows the work is the student’s own.',
             '1 mark each reason, 1 mark each developed [4]', 4, 'explain')


@d3d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def d3d_time(r, D):
    i = issue(r)
    ph = ['planning', 'literature review', 'primary research', 'analysis', 'writing']
    plan = [r.choice([6, 8, 10]), r.choice([20, 24, 30]), r.choice([12, 15, 18]), r.choice([10, 12, 15]), r.choice([20, 25, 30])]
    act = [p + r.choice([-4, -2, 0, 3, 6, 10]) for p in plan]
    tp, ta = sum(plan), sum(act)
    j = max(range(5), key=lambda k: (act[k] - plan[k]) / plan[k])
    over = 100 * (act[j] - plan[j]) / plan[j]
    tab = table(['Phase'] + ph, [['Planned hours'] + plan, ['Actual hours (from log)'] + act])
    if D <= 2:
        return MC(r, f'A research log on {i["name"]} records: {tab} How many hours did the project take in total?', f'{ta} hours', [f'{tp} hours', f'{ta - tp} hours' if ta != tp else f'{ta + 10} hours', f'{max(act)} hours'],
                  ' + '.join(map(str, act)) + f' = {ta}.')
    stem = f'A research log on {i["name"]} records: {tab} Calculate the total planned and actual hours, and the percentage by which the phase that overran most (in percentage terms) exceeded its plan.'
    ans = f'Planned {tp} h; actual {ta} h. Largest overrun: {ph[j]}, ({act[j]} − {plan[j]})/{plan[j]} × 100 = {pct(over)}.'
    key = '1 mark totals; 1 mark identifies phase; 1 mark percentage'
    m = 3
    if D >= 4:
        stem += ' Suggest how the student could use this in the reflection.'
        ans += f' Reflect on why {ph[j]} took longer (e.g. underestimating difficulty or responses), what was learned, and how future planning would change.'
        key += '; 1 mark explains cause; 1 mark lesson for future'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@d3d.add('C3', (2, 3, 4, 5), 'case')
def d3d_case(r, D):
    i = issue(r)
    intro = (f'Extract from a student’s research reflection on {i["name"]}: “I started with a broad question but narrowed it after my supervisor meeting. My survey response rate was very low, '
             'so I added interviews. I now realise I mainly read sources that agreed with my own view.”')
    parts = [
        lambda r: ('Identify one change of direction recorded in the reflection.', 'Narrowing the question; adding interviews after a low response rate.', '1 mark [1]'),
        lambda r: ('Explain why the final sentence shows reflexivity.', 'The student recognises that personal views shaped source selection, which may have biased the findings.', '1 mark recognises own bias; 1 mark effect on research [2]'),
        lambda r: ('Suggest what the student should do differently in future research.', 'Deliberately search for sources representing opposing perspectives; pilot the survey and plan for low responses.', '1 mark each relevant action, max 2 [2]'),
        lambda r: ('Explain how the research log supports this reflection.', 'Dated entries provide evidence of when and why decisions were made, making the reflection specific and honest rather than reconstructed from memory.', '1 mark evidence of decisions; 1 mark accuracy/specificity [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@d3d.add('C4', (2, 3, 4, 5), 'long')
def d3d_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'in a research report on {i["name"]}, reflecting on the research process is as important as the findings',
                   ['Reflection develops independent research skills that transfer to university and work.', 'It shows awareness of limitations and bias.'],
                   ['The findings answer the research question, which is the purpose of the report.', 'Reflection without strong findings has limited value to readers.'],
                   'Both matter: reflection makes the limits and strengths of the findings clear.')


CHAPTERS[3] = [d3a, d3b, d3c, d3d]
