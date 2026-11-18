"""Cambridge International AS Level Sociology 9699 (AS content, grade 11).

Paper 1 Socialisation, identity and methods of research; Paper 2 The family. Items follow the
9699 style: short definitions and 'describe two' items, 'explain' items, source/data-response
questions on research methods (percentages, rates, samples) and 'evaluate' essays marked in levels.

Each topic is built from a knowledge pack (key terms, sociologists, explanations, misconceptions,
assertion-reason pairs, scenarios with perspective views, research contexts, data tables, a source
and essay prompts) by the generic builders below. Research-method evaluation draws on METHODS.
Contexts are generic (person(), city()); studies in sources are presented as hypothetical.
"""
import re

from ._lib import topic, mcq, person, city, two_people

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.5, 1.5)}, 'wordy': True}
CHAPTERS = {}
_MK = re.compile(r'\[(\d+)\]')
LET = 'abcdefgh'
NUM = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}


def cap(s):
    return s[:1].upper() + s[1:]


def low(s):
    w = s.split(' ', 1)[0]
    if s[:2].isupper() or w.endswith(('’s', "'s")) or (w[:1].isupper() and w.rstrip(',') in _PROPER):
        return s
    return s[:1].lower() + s[1:]


_PROPER = {'Durkheim', 'Weber', 'Marx', 'Parsons', 'Giddens', 'Beck', 'Castells', 'Ohmae', 'Rostow', 'Huntington', 'Said', 'Habermas', 'Lyon', 'Davie', 'Bruce'}


def dot(s):
    s = s.strip()
    return s if s.endswith(('.', '?', '!', '”')) else s + '.'


def T(name, *extra):
    """Topic whose first keyword is the exact subtopic name."""
    return topic(name, name, *extra)


WOMEN = ['Amara', 'Sofia', 'Zara', 'Aisha', 'Leila', 'Priya', 'Chloe', 'Mei', 'Hana', 'Ines', 'Elena', 'Freya', 'Nadia', 'Ana', 'Lina', 'Grace', 'Isla']
MEN = ['Lucas', 'Kenji', 'Mateo', 'Noah', 'Ethan', 'Omar', 'Daniel', 'Tariq', 'Jonas', 'Kwame', 'Yusuf', 'Ravi', 'Diego', 'Samuel', 'Felix', 'Sipho', 'Arjun', 'Mohammed', 'Tomás']


def ctxd(r):
    a, b = two_people(r)
    c1, c2 = r.sample(['Nairobi', 'Lima', 'Singapore', 'Dubai', 'Cape Town', 'Lisbon', 'Kuala Lumpur', 'Bogotá', 'Cairo', 'Hanoi',
                       'Lagos', 'Doha', 'Jakarta', 'Manila', 'Karachi', 'Muscat', 'Santiago', 'Accra', 'Colombo', 'Auckland',
                       'Toronto', 'Madrid', 'Istanbul', 'Bangkok', 'Mumbai', 'Kathmandu', 'Dhaka', 'Riyadh', 'Mexico City', 'Seoul'], 2)
    return {'person': a, 'person2': b, 'city': c1, 'city2': c2, 'woman': r.choice(WOMEN), 'man': r.choice(MEN)}


def fill(s, d):
    for k, v in d.items():
        s = s.replace('{' + k + '}', str(v))
    return s


def marks_of(key):
    m = _MK.findall(key)
    return int(m[-1]) if m else 1


def assemble(intro, parts, typ):
    """parts: [(text, answer, key-with-[n])] in order -> structured item."""
    if not parts:
        return None
    if len(parts) == 1:
        t, a, k = parts[0]
        stem, ans, key = (intro.strip() + ' ' + t).strip(), a, k
    else:
        stem = intro.strip() + ' ' + ' '.join(f'({LET[i]}) {t}' for i, (t, _, _) in enumerate(parts))
        ans = ' '.join(f'({LET[i]}) {a}' for i, (_, a, _) in enumerate(parts))
        key = ' '.join(f'({LET[i]}) {k}' for i, (_, _, k) in enumerate(parts))
    m = max(1, min(20, sum(marks_of(k) for _, _, k in parts)))
    return {'stem': stem, 'answer': ans, 'key': key, 'marks': m, 'minutes': min(40, round(max(1.0, m * 1.25) * 2) / 2), 'type': typ}


def pick_parts(r, core, opt, n):
    """core: parts that must appear (in order, first); opt: optional parts; choose n in total, keep order of opt."""
    n = max(len(core), min(n, len(core) + len(opt)))
    idx = sorted(r.sample(range(len(opt)), n - len(core)))
    return [opt[i] for i in idx] + core


def _reg(t, C, D, typ, fn, name):
    fn.__name__ = name
    t.add(C, D, typ)(fn)
    return fn


# ============================================================== perspectives and sociologists

PERSP = {
    'Functionalism': {'cons'}, 'New Right': {'cons', 'right'}, 'Neoliberalism': {'right'}, 'Marxism': {'marx'}, 'Neo-Marxism': {'marx'},
    'Liberal feminism': {'fem'}, 'Marxist feminism': {'fem', 'marx'}, 'Radical feminism': {'fem'}, 'Difference feminism': {'fem'},
    'Interactionism': {'int'}, 'Social action theory': {'int'}, 'Postmodernism': {'pm'}, 'Late modernity': {'pm'},
    'Pluralism': {'plur'}, 'Modernisation theory': {'cons', 'mod'}, 'Dependency theory': {'marx', 'dep'}, 'World-systems theory': {'marx', 'dep'},
    'Weberian theory': {'weber'}, 'Positivism': {'pos'}, 'Interpretivism': {'int', 'interp'}, 'Personal life perspective': {'pm', 'int'},
    'Post-development theory': {'pm', 'postdev'}, 'Hyperglobalism': {'hyper'}, 'Transformationalism': {'trans'}, 'Globalisation scepticism': {'scep'},
    'Cultural effects theory': {'marx'}, 'Black feminism': {'fem'},
    'Religious market theory': {'rct'}, 'Postcolonial feminism': {'fem', 'postdev'},
}
BASIC = ['Functionalism', 'Marxism', 'Interactionism', 'Radical feminism', 'Liberal feminism', 'Postmodernism', 'New Right', 'Pluralism', 'Weberian theory']
THINKERS = []     # (name, claim, persp, detail, crit) across all packs, filled by build()


ADJ = {'Functionalism': 'functionalist', 'New Right': 'New Right', 'Neoliberalism': 'neoliberal', 'Marxism': 'Marxist', 'Neo-Marxism': 'neo-Marxist',
       'Liberal feminism': 'liberal feminist', 'Marxist feminism': 'Marxist feminist', 'Radical feminism': 'radical feminist', 'Difference feminism': 'difference feminist',
       'Black feminism': 'black feminist', 'Interactionism': 'interactionist', 'Social action theory': 'social action', 'Postmodernism': 'postmodernist',
       'Late modernity': 'late modern', 'Pluralism': 'pluralist', 'Modernisation theory': 'modernisation', 'Dependency theory': 'dependency',
       'World-systems theory': 'world-systems', 'Weberian theory': 'Weberian', 'Positivism': 'positivist', 'Interpretivism': 'interpretivist',
       'Personal life perspective': 'personal life', 'Post-development theory': 'post-development', 'Hyperglobalism': 'hyperglobalist',
       'Transformationalism': 'transformationalist', 'Globalisation scepticism': 'sceptical', 'Cultural effects theory': 'cultural effects', 'Feminism': 'feminist',
       'Religious market theory': 'religious market', 'Postcolonial feminism': 'postcolonial feminist'}


def adj(p):
    return ADJ.get(p, p.lower())


def a_soc(p):
    w = adj(p)
    return ('an ' if w[0].lower() in 'aeiou' else 'a ') + w + ' sociologist'


DEV = ['Modernisation theory', 'Dependency theory', 'World-systems theory', 'Neoliberalism', 'Post-development theory', 'Hyperglobalism',
       'Globalisation scepticism', 'Transformationalism', 'Functionalism', 'Marxism', 'Postmodernism']


def persp_ds(ans):
    tags = PERSP.get(ans, {ans})
    pool = DEV if ans in DEV[:8] else BASIC
    return [p for p in pool if p != ans and not (PERSP.get(p, {p}) & tags)]


def name_ds(name, persp):
    tags = PERSP.get(persp, {persp})
    bad = {n for n, _, p, _, _ in THINKERS if PERSP.get(p, {p}) & tags}
    out = []
    for n, _, p, _, _ in THINKERS:
        if n != name and n not in bad and n not in out:
            out.append(n)
    return out


# ============================================================== research methods knowledge

METHODS = {
    'questionnaire': dict(
        name='self-completion questionnaires', theory='positivist', kind='quantitative',
        s=['they can reach a large, geographically spread sample quickly and cheaply, so findings can be generalised',
           'closed, pre-coded questions produce quantitative data that is easy to compare and turn into statistics',
           'they are standardised, so the study can be repeated by another researcher to check reliability',
           'there is no interviewer present, so interviewer bias is avoided and anonymity is easier to guarantee'],
        l=['response rates are often low, so the sample may become unrepresentative',
           'closed questions impose the researcher’s categories and cannot explore the meanings behind answers, which lowers validity',
           'respondents may misunderstand questions, or give socially desirable answers, and there is no chance to clarify',
           'they measure what people say they do, not what they actually do'],
        f={'sensitive': ('s', 'anonymity may encourage respondents to admit sensitive or embarrassing behaviour they would not reveal face to face'),
           'large': ('s', 'large samples allow patterns and trends across social groups to be measured'),
           'young': ('l', 'younger respondents may misread questions or lack the concentration to complete them carefully, and may answer as they think adults expect'),
           'meaning': ('l', 'pre-set answers cannot capture the subjective meanings people attach to their experiences'),
           'hidden': ('l', 'hard-to-reach or deviant groups are unlikely to be on a sampling frame or to return a questionnaire'),
           'behaviour': ('l', 'people may report ideal behaviour (for example an equal division of housework) rather than what really happens')}),
    'structured interview': dict(
        name='structured interviews', theory='positivist', kind='quantitative',
        s=['every respondent is asked the same questions in the same order, so results are standardised and reliable',
           'response rates are usually higher than for postal questionnaires because the interviewer is present',
           'the interviewer can explain unclear questions, so fewer answers are spoiled',
           'answers can be quantified and compared between social groups'],
        l=['the interviewer’s presence may produce interviewer bias or socially desirable answers',
           'the fixed schedule cannot follow up interesting answers, so data lacks depth',
           'they are more costly and time-consuming than questionnaires because interviewers must be trained and paid',
           'the interview is an artificial social encounter, so answers may not reflect real behaviour'],
        f={'sensitive': ('l', 'respondents may be reluctant to reveal sensitive information face to face to a stranger following a fixed script'),
           'young': ('s', 'the interviewer can read questions aloud, so younger or less literate respondents can take part'),
           'large': ('s', 'trained interviewers can survey a large, representative sample in a standard way')}),
    'unstructured interview': dict(
        name='unstructured interviews', theory='interpretivist', kind='qualitative',
        s=['rapport between interviewer and interviewee builds trust, so people may reveal more, producing valid data',
           'the interviewer can follow up answers and explore meanings in the interviewee’s own words',
           'the interviewee can raise issues the researcher had not thought of, so the research is not limited by pre-set categories',
           'they produce rich, detailed qualitative data that gives verstehen (an empathetic understanding)'],
        l=['each interview is unique, so it is hard to repeat and the data is less reliable',
           'samples are small, so findings are difficult to generalise',
           'they are time-consuming and the data is hard to analyse and compare',
           'the interviewer may lead the interviewee or interpret answers selectively (interviewer bias)'],
        f={'sensitive': ('s', 'a sympathetic, non-judgemental interviewer can help people talk about painful or private experiences'),
           'meaning': ('s', 'they allow people to explain the meanings they give to their experiences in their own words'),
           'hidden': ('s', 'once trust is gained, members of marginalised groups may be willing to talk openly'),
           'large': ('l', 'they cannot measure patterns across a large population because only a few people can be interviewed'),
           'young': ('l', 'the power imbalance between adult researcher and child may make children say what they think adults want to hear')}),
    'semi-structured interview': dict(
        name='semi-structured interviews', theory='interpretivist', kind='qualitative and quantitative',
        s=['a core set of questions allows some comparison between interviewees while follow-up questions add depth',
           'the interviewer can probe and clarify answers, which improves validity',
           'they are more flexible than structured interviews but easier to analyse than unstructured ones'],
        l=['follow-up questions differ between interviews, so reliability is lower than with a fixed schedule',
           'samples are usually fairly small, so representativeness is limited',
           'interviewer bias may still affect answers'],
        f={'sensitive': ('s', 'the interviewer can adapt questions sensitively while still covering the key issues'),
           'meaning': ('s', 'open follow-up questions let interviewees explain their reasoning')}),
    'participant observation': dict(
        name='participant observation', theory='interpretivist', kind='qualitative',
        s=['the researcher sees what people actually do in their natural setting, not just what they say, so validity is high',
           'by joining the group the researcher can gain verstehen and see the world through members’ eyes',
           'it is flexible and can uncover issues the researcher had not anticipated',
           'it is often the only way to study small or closed groups in depth'],
        l=['the observer’s presence may change the group’s behaviour (the Hawthorne effect), especially if overt',
           'the researcher may become too involved and lose objectivity (“going native”)',
           'studies are small-scale and impossible to repeat exactly, so findings are unreliable and hard to generalise',
           'it is time-consuming, costly and may put the researcher at risk'],
        f={'hidden': ('s', 'it can give access to groups that would never complete a questionnaire, such as deviant subcultures'),
           'meaning': ('s', 'it reveals the meanings and labels that shape interaction as it happens'),
           'behaviour': ('s', 'it records real behaviour, avoiding the gap between what people say and what they do'),
           'large': ('l', 'it cannot measure the extent of a pattern across a whole society'),
           'private': ('l', 'it is very difficult to observe private behaviour inside homes'),
           'past': ('l', 'it can only study what is happening now, not past events')}),
    'covert participant observation': dict(
        name='covert participant observation', theory='interpretivist', kind='qualitative',
        s=['because the group does not know it is being studied, members act naturally and the Hawthorne effect is avoided',
           'it can give access to closed or deviant groups who would refuse an overt researcher',
           'it produces rich, first-hand qualitative data with high validity'],
        l=['it involves deception and lack of informed consent, which breaks ethical guidelines',
           'the researcher may be drawn into illegal or harmful activity and is at risk if discovered',
           'note-taking is difficult, so data depends on memory and may be inaccurate',
           'the study cannot be repeated, so reliability is low'],
        f={'hidden': ('s', 'it may be the only way to study a group that hides its activities from outsiders'),
           'sensitive': ('l', 'secretly recording sensitive behaviour without consent raises serious ethical problems of deception and harm'),
           'young': ('l', 'studying children covertly is ethically unacceptable because they cannot consent and are vulnerable')}),
    'non-participant observation': dict(
        name='non-participant observation', theory='both positivist and interpretivist (depending on how structured it is)', kind='quantitative or qualitative',
        s=['the researcher stays detached, so is less likely to “go native” and can record more objectively',
           'a structured observation schedule allows behaviour to be counted and compared, improving reliability',
           'it records behaviour as it happens rather than relying on people’s accounts'],
        l=['the presence of an observer may change behaviour (the Hawthorne effect)',
           'the researcher sees what happens but may not understand the meanings behind it',
           'observation schedules impose the researcher’s categories on behaviour'],
        f={'young': ('s', 'children can be observed in classrooms or playgrounds without having to answer questions'),
           'private': ('l', 'private behaviour in the home is rarely open to observation')}),
    'laboratory experiment': dict(
        name='laboratory experiments', theory='positivist', kind='quantitative',
        s=['the researcher controls variables, so cause and effect relationships can be identified',
           'the procedure is standardised, so the experiment can be repeated to check reliability',
           'results are quantitative and easy to compare'],
        l=['the artificial setting means people may not behave as they would in real life, so validity is low',
           'it is impossible to control all the variables that affect human behaviour',
           'participants who know they are being studied may change their behaviour (the Hawthorne effect or demand characteristics)',
           'many social issues cannot be studied in a laboratory for ethical or practical reasons'],
        f={'past': ('l', 'past events cannot be recreated in a laboratory'),
           'large': ('l', 'only small samples can be studied, so results are difficult to generalise'),
           'sensitive': ('l', 'it would be unethical to recreate harmful situations, such as violence, in a laboratory')}),
    'field experiment': dict(
        name='field experiments', theory='positivist', kind='quantitative',
        s=['they take place in a natural setting, so behaviour is more realistic than in a laboratory',
           'participants usually do not know they are part of an experiment, so they act naturally',
           'one variable can be altered (for example the name on a job application) to test its effect'],
        l=['the researcher has much less control over variables than in a laboratory',
           'participants have not given informed consent, which raises ethical issues',
           'they are hard to repeat exactly because conditions in the real world change'],
        f={'young': ('s', 'variables in a school, such as teacher expectations, can be altered in a normal classroom'),
           'sensitive': ('l', 'deceiving people about sensitive matters may cause harm or distress')}),
    'official statistics': dict(
        name='official statistics', theory='positivist', kind='quantitative',
        s=['they are usually free and readily available, saving time and money',
           'they cover very large numbers of people, often a whole population, so they are representative',
           'they are collected regularly, so trends over time and comparisons between groups can be made',
           'positivists see them as objective “social facts” that can be used to test hypotheses'],
        l=['they are collected for government purposes, so categories may not fit the sociologist’s needs',
           'definitions and methods of collection may change over time, making comparisons difficult',
           'interpretivists argue they are social constructions shaped by the decisions of officials and the public',
           'they show patterns but not the meanings or reasons behind them'],
        f={'change': ('s', 'regular collection over many years allows long-term trends to be identified'),
           'large': ('s', 'they give national data on whole populations that no single researcher could collect'),
           'hidden': ('l', 'much of the behaviour (for example unreported crime or abuse) never appears in them – the “dark figure”'),
           'sensitive': ('l', 'sensitive behaviour is often under-reported, so official figures underestimate the true extent'),
           'meaning': ('l', 'they cannot tell us how people feel or why they act as they do')}),
    'personal documents': dict(
        name='personal documents (diaries, letters, blogs and social media posts)', theory='interpretivist', kind='qualitative',
        s=['they give an insight into people’s feelings and meanings in their own words, so validity can be high',
           'they may be the only source of evidence about the past',
           'they are often cheap to obtain and produced without the researcher influencing them'],
        l=['they may not be authentic or credible; the writer may exaggerate or present themselves favourably',
           'they are usually unrepresentative because only some people keep or publish them',
           'their meaning must be interpreted by the researcher, which may introduce bias'],
        f={'past': ('s', 'they allow sociologists to study families and communities in the past that cannot be observed now'),
           'meaning': ('s', 'they show how people themselves understood their experiences'),
           'large': ('l', 'they cannot show how common a pattern is across a society')}),
    'longitudinal study': dict(
        name='longitudinal studies (following the same sample over time)', theory='positivist', kind='mainly quantitative',
        s=['they show how people’s lives change over time and allow cause and effect to be explored',
           'comparing the same people at different points avoids the problem of comparing different samples',
           'they can combine quantitative and qualitative data'],
        l=['sample attrition (people dropping out) can make the sample unrepresentative over time',
           'they are very expensive and results take many years to appear',
           'being studied repeatedly may change participants’ behaviour'],
        f={'change': ('s', 'they are ideal for tracking change in the same individuals or families over many years'),
           'young': ('s', 'they can follow children through their education into adulthood')}),
    'case study': dict(
        name='case studies', theory='interpretivist', kind='mainly qualitative',
        s=['they give a detailed, in-depth picture of one group, institution or community',
           'they can be used to generate hypotheses that are tested later on larger samples',
           'they may use several methods, increasing validity'],
        l=['one case may be untypical, so findings cannot be generalised',
           'the detailed data is difficult to compare with other cases',
           'the researcher’s interpretation may be biased'],
        f={'hidden': ('s', 'a single case can give rare insight into an unusual or closed group'),
           'large': ('l', 'a single case cannot show how widespread a pattern is')}),
    'content analysis': dict(
        name='content analysis', theory='positivist (quantitative content analysis) or interpretivist (qualitative content analysis)', kind='quantitative or qualitative',
        s=['it is cheap and the sources (newspapers, television, websites) are easy to obtain',
           'quantitative content analysis using a coding sheet can be repeated by another researcher, so it is reliable',
           'it allows representations to be compared over time or between different media'],
        l=['coding categories reflect the researcher’s own interpretation, so different coders may disagree',
           'it shows what content contains but not how audiences interpret it',
           'counting images or words may miss their deeper meaning and context'],
        f={'change': ('s', 'media content from different decades can be compared to measure change'),
           'meaning': ('l', 'counting does not reveal the meanings audiences take from the content')}),
}
METHOD_LIST = list(METHODS)
SINGULAR = {'participant observation', 'covert participant observation', 'non-participant observation', 'content analysis'}


def are(m):
    return 'is' if m in SINGULAR else 'are'


OBS = {'participant observation', 'covert participant observation', 'non-participant observation', 'laboratory experiment', 'field experiment', 'case study'}


def suitable(m, fl):
    fl = set(fl)
    need = {'content analysis': {'media'}, 'official statistics': {'large', 'change'}, 'personal documents': {'meaning', 'past'},
            'longitudinal study': {'change', 'young'}, 'unstructured interview': {'meaning', 'sensitive', 'hidden', 'private', 'young'},
            'semi-structured interview': {'meaning', 'sensitive', 'hidden', 'private', 'young', 'behaviour'}}.get(m)
    if m in OBS:
        if 'past' in fl:
            return False
        need = {'behaviour', 'meaning', 'hidden', 'young'}
    return not need or bool(need & fl)


def mnote(m, flags, side):
    return [txt for f, (sd, txt) in METHODS[m].get('f', {}).items() if f in flags and sd == side]


def mpoints(r, m, flags, side, n):
    spec = mnote(m, flags, side)
    gen = [x for x in METHODS[m][side] if x not in spec]
    r.shuffle(gen)
    out = spec[:1] + gen
    return out[:n]


# ============================================================== builders

def add_terms(t, terms):
    """terms: (term, definition, example). C1 MCQs both ways; C2 example and distinction items."""
    if len(terms) < 4:
        return
    t.fixed('C1', (1, 2, 3), [(f'Which term describes {low(d).rstrip(".")}?', cap(tm), f'{cap(tm)}: {d}. [1]',
                               [cap(x[0]) for x in terms if x[0] != tm]) for tm, d, ex in terms])
    t.fixed('C1', (1, 2, 3), [(f'What is meant by the term “{tm}”?', cap(d).rstrip('.') + '.', f'{cap(tm)}: {d}. [1]',
                               [cap(x[1]).rstrip('.') + '.' for x in terms if x[0] != tm]) for tm, d, ex in terms])

    def define(r, D):
        tm, d, ex = r.choice(terms)
        lead = r.choice(['Define the term', 'What is meant by the term', 'Explain what sociologists mean by'])
        q = '?' if lead.startswith('What') else '.'
        if D <= 1:
            return {'stem': f'{lead} “{tm}”{q}', 'answer': cap(d) + '.', 'key': f'1 mark for a clear definition: {d}. [1]', 'marks': 1, 'type': 'short'}
        return {'stem': f'{lead} “{tm}”? Give one example.' if q == '?' else f'{lead} “{tm}”, and give one example.', 'answer': f'{cap(d)}. Example: {ex}.',
                'key': f'1 mark for a clear definition ({d}); 1 mark for a relevant example such as {ex}. [2]', 'marks': 2, 'type': 'short'}
    _reg(t, 'C2', (1, 2), 'short', define, 'define')

    def distinguish(r, D):
        i = r.randrange(len(terms))
        j = r.choice([k for k in range(max(0, i - 2), min(len(terms), i + 3)) if k != i])
        (a, da, ea), (b, db, eb) = terms[i], terms[j]
        if D >= 3:
            lead = r.choice(['Distinguish between', 'Explain the difference between'])
            return {'stem': f'{lead} “{a}” and “{b}”, using an example of each.',
                    'answer': f'{cap(a)}: {da} (e.g. {ea}). {cap(b)}: {db} (e.g. {eb}).',
                    'key': f'1 mark each accurate definition; 1 mark each relevant example. [4]', 'marks': 4, 'type': 'explain'}
        lead = r.choice(['Distinguish between', 'What is the difference between'])
        return {'stem': f'{lead} “{a}” and “{b}”?' if lead.startswith('What') else f'{lead} “{a}” and “{b}”.',
                'answer': f'{cap(a)}: {da}. {cap(b)}: {db}.', 'key': '1 mark for each accurate definition, showing the contrast. [2]', 'marks': 2, 'type': 'explain'}
    _reg(t, 'C2', (2, 3, 4), 'explain', distinguish, 'distinguish')


def add_thinkers(t, thinkers):
    """thinkers: (name, claim (that-clause), perspective, detail, criticism)."""
    for x in thinkers:
        THINKERS.append(tuple(x))

    def who(r, D):
        name, claim, p, det, crit = r.choice(thinkers)
        ds = name_ds(name, p)
        if len(ds) < 3:
            return None
        opts, a = mcq(r, name, ds)
        return {'stem': f'Which sociologist argued that {claim}?', 'options': opts, 'answer': a, 'key': f'{name} ({p}): {det} [1]', 'marks': 1}
    _reg(t, 'C1', (1, 2, 3), 'mcq', who, 'who')

    def which_p(r, D):
        name, claim, p, det, crit = r.choice(thinkers)
        ds = persp_ds(p)
        if len(ds) < 3:
            return None
        opts, a = mcq(r, p, ds)
        stem = r.choice([f'{name} argued that {claim}. Which sociological perspective does this view belong to?',
                         f'Which perspective is most closely associated with {name}’s view that {claim}?'])
        return {'stem': stem, 'options': opts, 'answer': a, 'key': f'{p}: {det} [1]', 'marks': 1}
    _reg(t, 'C1', (1, 2, 3), 'mcq', which_p, 'which_p')

    def outline(r, D):
        name, claim, p, det, crit = r.choice(thinkers)
        if D <= 2:
            return {'stem': r.choice([f'Outline what {name} meant by arguing that {claim}.', f'Briefly explain {name}’s view that {claim}.']),
                    'answer': cap(det), 'key': f'1 mark for identifying the idea; 1 mark for developing it: {det} [2]', 'marks': 2, 'type': 'explain'}
        return {'stem': r.choice([f'{name} argued that {claim}. Explain this view and one criticism of it.',
                                  f'Explain {name}’s argument that {claim}, and give one criticism of this argument.']),
                'answer': f'{cap(det)} Criticism: {crit}', 'key': f'Up to 2 marks for explaining the view ({p}); up to 2 marks for an explained criticism. [4]', 'marks': 4, 'type': 'explain'}
    _reg(t, 'C2', (2, 3, 4), 'explain', outline, 'outline')


def add_explain(t, entries, D=(2, 3, 4)):
    """Fixed explain items (stem, answer, key-with-[n])."""
    t.fixed('C2', D, list(entries), type='explain')


def add_why(t, whys):
    """whys: (singular noun, plural noun, rest, [points]) -> 'State one / Explain two / Explain three ...'."""
    def fn(r, D):
        sing, plu, rest, pts = r.choice(whys)
        n = 1 if D <= 1 else (2 if D == 2 else 3)
        n = min(n, len(pts))
        ch = r.sample(pts, n)
        if n == 1:
            return {'stem': f'State one {sing} {rest}.', 'answer': cap(ch[0]) + '.', 'key': f'1 mark for a valid point, e.g. {ch[0]}. [1]', 'marks': 1, 'type': 'short'}
        lead = r.choice(['Explain', 'Describe and explain']) if n == 2 else 'Explain'
        m = 2 * n
        return {'stem': f'{lead} {NUM[n]} {plu} {rest}.', 'answer': ' '.join(f'{i + 1}. {cap(p)}.' for i, p in enumerate(ch)),
                'key': f'For each of {NUM[n]} points: 1 mark for identifying it and 1 mark for developing/explaining it. Other valid points: {"; ".join(p for p in pts if p not in ch)}. [{m}]',
                'marks': m, 'type': 'explain'}
    _reg(t, 'C2', (1, 2, 3, 4), 'explain', fn, 'why')


CLAIM_LEADS = ['A student writes:', 'In a class discussion, a student says:', 'A revision guide states:', 'A classmate claims:']


def add_claims(t, claims):
    ents = []
    for i, (c, ok, why) in enumerate(claims):
        ents.append((f'{CLAIM_LEADS[i % 4]} “{c}” Is this correct? Explain your answer.', ('Correct. ' if ok else 'Not correct. ') + why,
                     '1 mark for the correct judgement; 1 mark for an accurate sociological explanation. [2]'))
    t.fixed('C2', (1, 2, 3), ents, type='explain')


AR_OPTS = ['Both A and R are true, and R is the correct explanation of A',
           'Both A and R are true, but R is not the correct explanation of A',
           'A is true but R is false', 'A is false but R is true']


def add_ar(t, pairs, falses):
    if len(pairs) < 2 or not falses:
        return

    def fn(r, D):
        case = r.randrange(4)
        i = r.randrange(len(pairs))
        if case == 0:
            a, rr = pairs[i]
        elif case == 1:
            j = r.choice([x for x in range(len(pairs)) if x != i])
            a, rr = pairs[i][0], pairs[j][1]
        elif case == 2:
            a, rr = pairs[i][0], r.choice(falses)
        else:
            a, rr = r.choice(falses), pairs[i][1]
        stem = f'Assertion (A): {a} Reason (R): {rr} Which option is correct?'
        key = {0: 'A is true and R explains it. [1]', 1: 'A and R are both true statements, but R does not explain A. [1]',
               2: f'A is true; R is false: “{rr}” is incorrect. [1]', 3: f'A is false: “{a}” is incorrect; R is a true statement. [1]'}[case]
        return {'stem': stem, 'options': list(AR_OPTS), 'answer': AR_OPTS[case], 'key': key, 'marks': 1}
    _reg(t, 'C2', (2, 3), 'mcq', fn, 'ar')


def add_apply(t, scen, views, research=False):
    """scen: scenario sentences with {person}/{city}; views: {perspective: interpretation}. C3 application.
    research=True: the scenario describes a piece of research, so perspectives evaluate it."""
    ps = list(views)
    v1, v2 = ('view this research', 'evaluate this research') if research else ('explain this', 'interpret this situation')
    if not scen or not ps:
        return

    def fn(r, D):
        d = ctxd(r)
        s = fill(r.choice(scen), d)
        if D >= 4 and len(ps) >= 2:
            p1, p2 = r.sample(ps, 2)
            lead = r.choice([f'Compare how {adj(p1)} and {adj(p2)} sociologists might {v2}.',
                             f'Explain how {adj(p1)} and {adj(p2)} sociologists might differ in the way they {v2}.'])
            return {'stem': f'{s} {lead}', 'answer': f'{p1}: {views[p1]} {p2}: {views[p2]}',
                    'key': f'Up to 3 marks for each perspective: 1 mark for its key idea, 1 mark for applying it to the situation, 1 mark for a relevant concept or sociologist. 1 further mark for a clear point of contrast is included within the 6. [6]', 'marks': 6, 'type': 'explain'}
        p = r.choice(ps)
        if D <= 2:
            return {'stem': f'{s} Suggest how {a_soc(p)} might {v1}.', 'answer': f'{p}: {views[p]}',
                    'key': '1 mark for the key idea of the perspective; 1 mark for applying it to the situation. [2]', 'marks': 2, 'type': 'explain'}
        return {'stem': f'{s} Explain how {a_soc(p)} might {v2}.', 'answer': f'{p}: {views[p]}',
                'key': '1 mark for identifying the key idea of the perspective; up to 2 marks for applying it to the details of the situation; 1 mark for a relevant concept or sociologist. [4]', 'marks': 4, 'type': 'explain'}
    _reg(t, 'C3', (2, 3, 4, 5), 'explain', fn, 'apply')


METH_LEADS = ['{person} is planning a study of {ctx}.', 'A sociologist in {city} wants to research {ctx}.',
              'A research team is investigating {ctx}.', '{person}, a sociology student, is designing a project on {ctx}.']

LV_EVAL = {
    6: 'Level 1 (1-2): one or two simple points about the method. Level 2 (3-4): explains strengths OR limitations applied to the context. Level 3 (5-6): explains strengths AND limitations applied to the context with a supported judgement. [6]',
    8: 'Level 1 (1-2): simple, list-like points. Level 2 (3-4): some explained strengths or limitations, weakly applied. Level 3 (5-6): explained strengths and limitations applied to the context, using concepts (validity, reliability, representativeness, ethics). Level 4 (7-8): well-developed, balanced evaluation applied to the context, with theoretical links (positivism/interpretivism) and a reasoned conclusion. [8]',
    10: 'Level 1 (1-3): simple, list-like points. Level 2 (4-6): explained strengths or limitations with some application. Level 3 (7-8): explained strengths and limitations applied to the context using concepts (validity, reliability, representativeness, practical and ethical issues). Level 4 (9-10): balanced, well-applied evaluation with theoretical links, comparison with an alternative method and a reasoned conclusion. [10]',
}


def add_methods(t, contexts, methods=None):
    """contexts: (description, set of flags). C3 strengths/limitations; C4 evaluate the use of a method."""
    ml = list(methods or [m for m in METHOD_LIST if m != 'content analysis'])
    if not contexts:
        return

    def strengths(r, D):
        c, fl = r.choice(contexts)[:2]
        c = fill(c, ctxd(r))
        ok = [x for x in ml if suitable(x, fl) and x != 'laboratory experiment']
        if not ok:
            return None
        m = r.choice(ok)
        M = METHODS[m]
        intro = fill(r.choice(METH_LEADS), dict(ctxd(r), ctx=c))
        if D <= 2:
            side = r.choice(['s', 'l'])
            w = 'strength' if side == 's' else 'limitation'
            p = mpoints(r, m, fl, side, 1)
            return {'stem': f'{intro} Explain one {w} of using {M["name"]} for this research.', 'answer': cap(p[0]) + '.',
                    'key': f'1 mark for identifying a relevant {w}; 1 mark for explaining it in the context of {c}. [2]', 'marks': 2, 'type': 'explain'}
        if D == 3:
            side = r.choice(['s', 'l'])
            w = 'strengths' if side == 's' else 'limitations'
            p = mpoints(r, m, fl, side, 2)
            return {'stem': f'{intro} Explain two {w} of using {M["name"]} for this research.', 'answer': f'1. {cap(p[0])}. 2. {cap(p[1])}.',
                    'key': f'For each {w[:-1]}: 1 mark identified, 1 mark explained and applied to {c}. [4]', 'marks': 4, 'type': 'explain'}
        s = mpoints(r, m, fl, 's', 1)
        lm = mpoints(r, m, fl, 'l', 2)
        return {'stem': f'{intro} Explain one strength and two limitations of using {M["name"]} for this research.',
                'answer': f'Strength: {s[0]}. Limitations: 1. {lm[0]}. 2. {lm[1]}.',
                'key': f'For each of three points: 1 mark identified, 1 mark explained and applied to {c}. [6]', 'marks': 6, 'type': 'explain'}
    _reg(t, 'C3', (2, 3, 4), 'explain', strengths, 'm_strength')

    def evaluate(r, D):
        c, fl = r.choice(contexts)[:2]
        c = fill(c, ctxd(r))
        ok = [x for x in ml if suitable(x, fl)]
        if not ok:
            return None
        m = r.choice(ok)
        M = METHODS[m]
        s = mpoints(r, m, fl, 's', 2)
        lm = mpoints(r, m, fl, 'l', 2)
        theory = f'Theory: {M["name"]} {are(m)} favoured {"" if " " in M["theory"] else "mainly "}by {M["theory"]} sociologists and {"produces" if are(m) == "is" else "produce"} {M["kind"]} data.'
        alt = r.choice([x for x in ml if METHODS[x]['theory'] != M['theory'] and x != m] or [x for x in METHOD_LIST if x != m])
        ans = (f'Strengths: {s[0]}; {s[1]}. Limitations: {lm[0]}; {lm[1]}. {theory} '
               f'Judgement: useful for some aims in studying {c} but best combined with another method such as {METHODS[alt]["name"]} (triangulation).')
        if D <= 2:
            return {'stem': fill(r.choice(METH_LEADS), dict(ctxd(r), ctx=c)) + f' Explain one strength and one limitation of using {M["name"]} for this study.',
                    'answer': f'Strength: {s[0]}. Limitation: {lm[0]}.', 'key': f'For each: 1 mark identified; 1 mark explained in the context of {c}. [4]', 'marks': 4, 'type': 'explain'}
        mk = 6 if D == 3 else (8 if D == 4 else 10)
        stem = r.choice([f'Evaluate the usefulness of {M["name"]} for studying {c}.',
                         f'Evaluate the strengths and limitations of using {M["name"]} to research {c}.',
                         f'Assess how useful {M["name"]} {are(m)} for studying {c}.',
                         fill(r.choice(METH_LEADS), dict(ctxd(r), ctx=c)) + f' Evaluate the use of {M["name"]} for this research.'])
        return {'stem': stem, 'answer': ans, 'key': LV_EVAL[mk], 'marks': mk, 'type': 'long'}
    _reg(t, 'C4', (2, 3, 4, 5), 'long', evaluate, 'm_eval')


# ----------------------------------------------------------------- data response

def _pc(x, dp=1):
    s = f'{x:.{dp}f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


DATA_LEADS = ['A survey of {n} {pop} in {city} produced the data below.',
              '{person}, a sociology student, found the following figures in a report on {what} in {city}. The report was based on {n} {pop}.',
              'The table shows results from research into {what}, using {mname} with {n} {pop} in {city}.',
              'Study the data, which come from a study of {what} ({n} {pop}, {city}).']


def _data(r, spec):
    rows = list(spec['rows'])
    cols = list(spec['cols'])
    for _ in range(60):
        vals = []
        for i, _ in enumerate(rows):
            lo, hi = spec['base'][i]
            a = r.randint(lo, hi)
            dlo, dhi = spec['delta'][i]
            b = a + r.randint(dlo, dhi)
            if spec.get('unit', '%') == '%':
                b = max(1, min(99, b))
            vals.append((a, b))
        if not spec.get('share') or (sum(v[0] for v in vals) <= 98 and sum(v[1] for v in vals) <= 98):
            break
    if spec.get('complement') and len(vals) == 2:
        vals[1] = (100 - vals[0][0], 100 - vals[0][1])
    if spec.get('dist'):
        for _ in range(30):
            last = (100 - sum(v[0] for v in vals[:-1]), 100 - sum(v[1] for v in vals[:-1]))
            if 2 <= last[0] <= 95 and 2 <= last[1] <= 95:
                break
            vals = [(max(1, a - r.randint(0, 6)), max(1, b - r.randint(0, 6))) for a, b in vals]
        vals[-1] = (100 - sum(v[0] for v in vals[:-1]), 100 - sum(v[1] for v in vals[:-1]))
        if min(vals[-1]) < 1:
            vals[-1] = (max(1, vals[-1][0]), max(1, vals[-1][1]))
    n = r.choice(spec.get('n', [200, 240, 300, 400, 450, 500, 600, 800, 1000, 1200]))
    d = dict(ctxd(r), n=n, pop=spec['pop'], what=spec['what'], mname=METHODS[spec['method']]['name'])
    intro = fill(r.choice(spec.get('leads') or DATA_LEADS), d)
    unit = spec.get('unit', '%')
    tab = f'Table: {spec["label"]} | {cols[0]} | {cols[1]}. ' + ' '.join(f'{g} | {a}{unit} | {b}{unit}.' for g, (a, b) in zip(rows, vals))
    return rows, cols, vals, n, intro + ' ' + tab, d


def uu(x, U, signed=False):
    v = f'{x:+d}' if signed else str(x)
    return f'{v} {U[:-1] if abs(x) == 1 and U.endswith("s") else U}'


def _data_parts(r, spec, rows, cols, vals, n):
    unit = spec.get('unit', '%')
    U = spec.get('uname', 'percentage points')
    cmpc = spec.get('cmp')
    i = r.randrange(len(rows))
    g, (a, b) = rows[i], vals[i]
    hi_i = max(range(len(rows)), key=lambda k: vals[k][1])
    ties = [k for k in range(len(rows)) if vals[k][1] == vals[hi_i][1]]
    parts = {}
    if len(ties) == 1:
        parts['ident'] = (f'Using the data, identify the group with the highest figure for {cols[1]}.', f'{rows[hi_i]} ({vals[hi_i][1]}{unit}).',
                          f'{rows[hi_i]}, {vals[hi_i][1]}{unit}. [1]')
    ch = b - a
    if cmpc:
        parts['pp'] = (f'Calculate the difference, in {U}, between {cols[0]} and {cols[1]} for {g}.', f'{b} − {a} = {uu(ch, U, True)} ({cols[1]} compared with {cols[0]}).',
                       f'1 mark for using {a} and {b}; 1 mark for {uu(abs(ch), U)} with direction. [2]')
    else:
        parts['pp'] = (f'Calculate the change, in {U}, for {g} between {cols[0]} and {cols[1]}.', f'{b} − {a} = {uu(ch, U, True)}.',
                       f'1 mark for using {a} and {b}; 1 mark for {uu(ch, U, True)} (sign or “rise/fall” needed). [2]')
    if a and not cmpc:
        rel = 100 * (b - a) / a
        parts['rel'] = (f'Calculate the percentage change in the figure for {g} between {cols[0]} and {cols[1]}. Show your working.',
                        f'({b} − {a}) ÷ {a} × 100 = {_pc(rel)}%.', f'1 mark for ({b} − {a}) ÷ {a} × 100; 1 mark for {_pc(rel)}% (accept 2-3 s.f.). [2]')
    if len(rows) >= 2:
        j = r.choice([k for k in range(len(rows)) if k != i])
        g1, g2 = rows[i], rows[j]
        gap1, gap2 = vals[i][0] - vals[j][0], vals[i][1] - vals[j][1]
        trend = 'narrowed' if abs(gap2) < abs(gap1) else ('widened' if abs(gap2) > abs(gap1) else 'stayed the same')
        if cmpc:
            parts['gap'] = (f'Calculate the difference between {g1} and {g2} for {cols[0]} and for {cols[1]}, and state for which of these the difference is larger.',
                            f'{cols[0]}: {uu(abs(gap1), U)}; {cols[1]}: {uu(abs(gap2), U)}; ' + ('the difference is the same for both.' if abs(gap1) == abs(gap2) else f'the difference is larger for {cols[0] if abs(gap1) > abs(gap2) else cols[1]}.'),
                            f'1 mark each difference ({abs(gap1)} and {abs(gap2)}); 1 mark for the correct comparison. [3]')
        else:
            parts['gap'] = (f'Calculate the gap between {g1} and {g2} in {cols[0]} and in {cols[1]}, and state whether it narrowed or widened.',
                            f'{cols[0]}: {uu(abs(gap1), U)}; {cols[1]}: {uu(abs(gap2), U)}; the gap {trend}.',
                            f'1 mark each gap ({abs(gap1)} and {abs(gap2)}); 1 mark for “{trend}”. [3]')
        k = r.choice([100, 120, 150, 200, 250, 300])
        if k < n and unit == '%' and not (spec.get('nocount') or spec.get('dist') or spec.get('share')):
            est = round(k * vals[j][1] / 100)
            who = f'{k} of the respondents were {g2}' if not cmpc else f'{k} of the {g2} respondents were in the group “{cols[1]}”'
            parts['count'] = (f'Suppose {who}. Using the {cols[1]} figure, calculate how many of them gave this response.',
                              f'{vals[j][1]}% of {k} = {vals[j][1]} ÷ 100 × {k} = {est} (to the nearest whole person).',
                              f'1 mark method ({vals[j][1]} ÷ 100 × {k}); 1 mark answer {est}. [2]')
    ups = [rows[k] for k in range(len(rows)) if vals[k][1] > vals[k][0]]
    downs = [rows[k] for k in range(len(rows)) if vals[k][1] < vals[k][0]]
    desc = []
    if cmpc:
        if ups:
            desc.append(f'the figure is higher for {cols[1]} than for {cols[0]} among ' + ', '.join(ups))
        if downs:
            desc.append(f'the figure is lower for {cols[1]} than for {cols[0]} among ' + ', '.join(downs))
    else:
        if ups:
            desc.append('the figure rose for ' + ', '.join(ups))
        if downs:
            desc.append('the figure fell for ' + ', '.join(downs))
    if len(ties) == 1:
        desc.append(f'{rows[hi_i]} had the highest figure for {cols[1]}')
    parts['desc'] = ('Describe two patterns shown in the data.', cap('; '.join(desc)) + '.',
                     '1 mark for each accurate pattern supported by figures from the table. [2]')
    e = r.choice(spec['expl'])
    parts['expl'] = (r.choice(['Suggest one sociological explanation for the patterns shown in the data.', 'Using sociological ideas, suggest one reason for the patterns in the data.']),
                     cap(e) + '.', f'1 mark for a relevant explanation; 1 mark for linking it to the data. Other valid explanations: {"; ".join(x for x in spec["expl"] if x != e)}. [2]')
    lm = r.choice(METHODS[spec['method']]['l'] + mnote(spec['method'], spec.get('flags', set()), 'l'))
    parts['valid'] = (r.choice([f'Explain one reason why these data may not give a valid picture of {spec["what"]}.',
                                f'Explain one limitation of using {METHODS[spec["method"]]["name"]} to collect data like these.']),
                      cap(lm) + '.', '1 mark for identifying a relevant limitation (validity, representativeness, reliability); 1 mark for explaining it in context. [2]')
    return parts


def add_data(t, specs):
    """specs: dict(what, pop, rows, cols, base, delta, label, expl, method, claim, counter[, flags, n, unit])."""
    if not specs:
        return

    def mcqcalc(r, D):
        spec = r.choice(specs)
        rows, cols, vals, n, intro, d = _data(r, spec)
        i = r.randrange(len(rows))
        a, b = vals[i]
        if a == b:
            return None
        c = b - a
        U = spec.get('uname', 'percentage points')
        rel = 100 * c / a
        ans = uu(c, U, True)
        others = [vals[k][1] - vals[k][0] for k in range(len(rows)) if k != i]
        ds = [uu(-c, U, True), f'{_pc(rel)} {U}', uu(c + (5 if c > 0 else -5), U, True)] + [uu(o, U, True) for o in others]
        ds = [x for x in ds if x != ans]
        opts, aa = mcq(r, ans, ds)
        q = (f'What is the difference, in {U}, between {cols[0]} and {cols[1]} for {rows[i]} ({cols[1]} minus {cols[0]})?' if spec.get('cmp')
             else f'By how many {U} did the figure for {rows[i]} change between {cols[0]} and {cols[1]}?')
        return {'stem': f'{intro} {q}', 'options': opts, 'answer': aa, 'key': f'{b} − {a} = {uu(c, U, True)}. [1]', 'marks': 1}
    _reg(t, 'C3', (1, 2), 'mcq', mcqcalc, 'data_mcq')

    def dr(r, D):
        spec = r.choice(specs)
        rows, cols, vals, n, intro, d = _data(r, spec)
        P = _data_parts(r, spec, rows, cols, vals, n)
        calc = [P[k] for k in ('ident', 'pp', 'rel', 'gap', 'count') if k in P]
        words = [P['desc'], P['expl'], P['valid']]
        if D <= 2:
            parts = r.sample(calc, 2) if r.random() < 0.6 else [r.choice(calc), P['desc']]
        elif D == 3:
            parts = r.sample(calc, 2) + [r.choice(words)]
        else:
            parts = r.sample(calc, 2) + r.sample(words, 2)
        order = list(P.values())
        parts.sort(key=lambda p: order.index(p))
        return assemble(intro, parts, 'numerical' if D <= 2 else 'case')
    _reg(t, 'C3', (2, 3, 4, 5), 'case', dr, 'data')

    def ev(r, D):
        spec = r.choice(specs)
        rows, cols, vals, n, intro, d = _data(r, spec)
        P = _data_parts(r, spec, rows, cols, vals, n)
        calc = [P[k] for k in ('pp', 'rel', 'gap', 'count') if k in P]
        ups = sum(1 for a, b in vals if b > a)
        mk = 4 if D <= 3 else 6
        evp = (f'Using the data and your own sociological knowledge, evaluate the view that {spec["claim"]}.',
               f'Evidence from the data: {P["desc"][1]} {cap(r.choice(spec["expl"]))}. Qualifications: {spec["counter"]} The data also come from {METHODS[spec["method"]]["name"]} of {n} {spec["pop"]} in one place, so they may not be representative or valid. Judgement: the data give partial support only.',
               ('Level 1 (1-2): simple use of data or own knowledge. Level 2 (3-4): uses the data and own knowledge to argue for and against, with a judgement. [4]' if mk == 4 else
                'Level 1 (1-2): simple use of data or knowledge. Level 2 (3-4): uses data AND sociological knowledge on one side, or both sides thinly. Level 3 (5-6): balanced evaluation using the data, sociological arguments and comment on the validity of the data, with a reasoned conclusion. [6]'))
        pre = [r.choice(calc)] + ([P['valid']] if D >= 4 else [])
        return assemble(intro, pre + [evp], 'case')
    _reg(t, 'C4', (2, 3, 4, 5), 'case', ev, 'data_eval')


# ----------------------------------------------------------------- source

SRC_LEADS = ['Read Source A. “{text}”', 'Source A: “{text}” Use Source A and your own knowledge to answer the questions.',
             'Study the following extract (Source A) from a report on research carried out in {city}. “{text}”',
             '{person} found this account of a study (Source A) while revising. “{text}”']


def add_source(t, srcs):
    """srcs: dict(text, method, about, finds [2], persp, pview, claim, pro, con[, flags])."""
    if not srcs:
        return

    def parts(r, s):
        M = METHODS[s['method']]
        fl = s.get('flags', set())
        st = mpoints(r, s['method'], fl, 's', 1)[0]
        lm = mpoints(r, s['method'], fl, 'l', 1)[0]
        return {
            'meth': ('Identify the main research method used in the study described in Source A.', cap(M['name']) + '.', f'{cap(M["name"])}. [1]'),
            'finds': ('Using Source A, identify two findings of the study.', f'1. {cap(s["finds"][0])}. 2. {cap(s["finds"][1])}.', '1 mark for each finding taken from the source. [2]'),
            'str': (f'Using Source A, explain one strength of the method used for studying {s["about"]}.', cap(st) + '.', '1 mark for a relevant strength; 1 mark for applying it to the study in the source. [2]'),
            'lim': (f'Explain one limitation of the method used in Source A for studying {s["about"]}.', cap(lm) + '.', '1 mark for a relevant limitation; 1 mark for applying it to the study in the source. [2]'),
            'persp': (f'Explain how {a_soc(s["persp"])} might interpret the findings in Source A.', cap(s['pview']), '1 mark for the key idea of the perspective; up to 2 marks for applying it to the findings in the source. [3]'),
            'eval': (f'Using Source A and your own knowledge, evaluate the view that {s["claim"]}.',
                     f'For: {s["pro"]} Against: {s["con"]} Also consider how far a single study using {M["name"]} can support a general claim. Judgement: a reasoned conclusion.',
                     'Level 1 (1-2): simple points from the source or own knowledge. Level 2 (3-4): explained points for and against using the source and own knowledge. Level 3 (5-6): balanced, well-supported evaluation with comment on the evidence and a reasoned conclusion. [6]'),
        }

    def src3(r, D):
        s = r.choice(srcs)
        intro = fill(r.choice(SRC_LEADS), dict(ctxd(r), text=fill(s['text'], ctxd(r))))
        P = parts(r, s)
        opt = [P[k] for k in ('meth', 'finds', 'str', 'lim', 'persp')]
        n = 2 if D <= 2 else (3 if D == 3 else 4)
        return assemble(intro, pick_parts(r, [], opt, n), 'case')
    _reg(t, 'C3', (2, 3, 4, 5), 'case', src3, 'source')

    def src4(r, D):
        s = r.choice(srcs)
        intro = fill(r.choice(SRC_LEADS), dict(ctxd(r), text=fill(s['text'], ctxd(r))))
        P = parts(r, s)
        opt = [P[k] for k in ('meth', 'finds', 'str', 'lim', 'persp')]
        n = 2 if D <= 3 else 3
        return assemble(intro, pick_parts(r, [P['eval']], opt, n), 'case')
    _reg(t, 'C4', (3, 4, 5), 'case', src4, 'source_eval')


# ----------------------------------------------------------------- essays

B_FORMS = ['Evaluate the view that {p}.', '“{P}.” Evaluate this view.', 'Assess the claim that {p}.',
           'To what extent do sociological arguments and evidence support the view that {p}?']
A_KEY = 'Level 1 (1-3): one or two simple points, limited sociological knowledge. Level 2 (4-6): explained points using some concepts, studies or theories. Level 3 (7-8): two well-explained, developed points with accurate concepts, studies or theories, clearly applied to the question. Creditworthy: {pts} [8]'
B_KEY = 'Level 1 (1-3): a few simple points. Level 2 (4-6): some explained arguments, mainly on one side; limited evaluation. Level 3 (7-9): a range of explained arguments and evidence for and against, with some evaluation. Level 4 (10-12): a balanced, well-supported analysis using theories, studies and concepts, sustained evaluation and a reasoned conclusion. For: {fr} Against: {ag} [12]'


def add_essay(t, prompts):
    """prompts: (part (a) task, (a) points, (b) claim, for, against)."""
    def fn(r, D):
        a_task, a_pts, claim, fr, ag = r.choice(prompts)
        b = r.choice(B_FORMS).replace('{p}', claim).replace('{P}', cap(claim))
        ka, kb = A_KEY.format(pts=a_pts), B_KEY.format(fr=fr, ag=ag)
        concl = 'Conclusion: a reasoned judgement on how far the view holds.'
        if D >= 5 or (D == 4 and r.random() < 0.3):
            stem, ans, key, m = f'(a) {a_task} (b) {b}', f'(a) {a_pts} (b) For: {fr} Against: {ag} {concl}', f'(a) {ka} (b) {kb}', 20
        elif D == 4:
            stem, ans, key, m = b, f'For: {fr} Against: {ag} {concl}', kb, 12
        else:
            stem, ans, key, m = a_task, a_pts, ka, 8
        return {'stem': stem, 'answer': ans, 'key': key, 'type': 'long', 'marks': m, 'minutes': min(40, 2 * m)}
    _reg(t, 'C4', (2, 3, 4, 5), 'long', fn, 'essay')


def add_mcq(t, entries, D=(1, 2, 3)):
    """Fixed MCQs (stem, answer, key, distractors)."""
    t.fixed('C1', D, [(s, a, k, ds) for s, a, k, ds in entries])


def _markify(t, start):
    for tpl in t.templates[start:]:
        if tpl.name != 'fixed':
            continue

        def fn(r, D, f=tpl.fn):
            q = f(r, D)
            if q and 'marks' not in q:
                q['marks'] = 1 if q.get('options') else marks_of(q['key'])
            return q
        tpl.fn = fn


def build(t, P, views=None):
    start = len(t.templates)
    add_terms(t, P.get('terms', []))
    add_thinkers(t, P.get('thinkers', []))
    if P.get('mcq'):
        add_mcq(t, P['mcq'])
    if P.get('explain'):
        add_explain(t, P['explain'])
    if P.get('why'):
        add_why(t, P['why'])
    if P.get('claims'):
        add_claims(t, P['claims'])
    if P.get('ar'):
        add_ar(t, *P['ar'])
    add_apply(t, P.get('scen', []), P.get('views') or views or {}, P.get('research', False))
    add_methods(t, P.get('ctx', []), P.get('methods'))
    add_data(t, P.get('data', []))
    add_source(t, P.get('source', []))
    if P.get('essays'):
        add_essay(t, P['essays'])
    _markify(t, start)
    return t


# ============================================================== CHAPTER 1: Sociological perspectives

V1 = {
    'Functionalism': 'society is a system of interdependent institutions that meet needs (functional prerequisites); shared norms and values (value consensus) learnt through socialisation create social order and integration, so the situation can be seen as contributing to stability (Durkheim, Parsons).',
    'Marxism': 'society is based on conflict between the bourgeoisie, who own the means of production, and the proletariat; institutions spread ruling-class ideology and false class consciousness, so the situation reflects and reproduces class inequality and exploitation (Marx, Althusser).',
    'Radical feminism': 'society is patriarchal: men dominate women in every sphere, including the family and personal relationships, so the situation is an example of male power and the oppression of women (Firestone, Millett).',
    'Interactionism': 'society is built up from small-scale interactions in which people create shared meanings, negotiate roles and apply labels; the situation should be understood through the meanings the people involved give to it (Mead, Blumer, Becker).',
    'Postmodernism': 'society is fragmented and diverse; there are no fixed structures or single truths, so individuals choose identities and lifestyles from many options and the situation reflects choice, consumption and media-saturated culture (Lyotard, Baudrillard).',
}

c1a = T('Functionalism: society as a system, value consensus and social order')
build(c1a, {
    'terms': [
        ('value consensus', 'broad agreement among members of a society about its main values and goals', 'widespread agreement that education and hard work should be rewarded'),
        ('social order', 'the stable, predictable patterns of behaviour that allow society to function smoothly', 'people queuing and obeying traffic laws without being forced to'),
        ('organic analogy', 'the comparison of society to a living body whose parts (institutions) each perform a function for the whole', 'the family compared to an organ that keeps the body healthy'),
        ('functional prerequisites', 'the basic needs that every society must meet in order to survive', 'Parsons’s four needs: adaptation, goal attainment, integration and latency'),
        ('anomie', 'a state of normlessness in which shared rules break down and people are unsure how to behave', 'rising suicide during rapid economic change, as described by Durkheim'),
        ('social solidarity', 'the sense of belonging and shared commitment that binds members of a society together', 'a nation coming together in collective mourning after a disaster'),
        ('manifest function', 'the intended and recognised consequence of an institution or practice', 'a school teaching pupils to read and write'),
        ('latent function', 'an unintended and often unrecognised consequence of an institution or practice', 'schools providing childcare that allows parents to work'),
    ],
    'thinkers': [
        ('Durkheim', 'society is a reality “sui generis” made up of social facts that constrain individuals', 'Functionalism',
         'Durkheim saw social facts (norms, values, institutions) as external to individuals and constraining them; shared values and collective conscience create social solidarity.',
         'Interactionists argue this underplays human agency: people actively create and change norms rather than simply being shaped by them.'),
        ('Parsons', 'every social system must meet four functional prerequisites: adaptation, goal attainment, integration and latency (pattern maintenance)', 'Functionalism',
         'Parsons’s AGIL model links each need to a sub-system (economy, polity, religion/law, family/education); value consensus integrates the system.',
         'It is criticised for assuming consensus and stability, so it struggles to explain conflict and rapid social change.'),
        ('Merton', 'institutions can have latent functions and dysfunctions as well as manifest functions', 'Functionalism',
         'Merton argued that not everything is functional for everyone: some practices have unintended consequences or harm parts of society (dysfunctions).',
         'Marxists reply that “dysfunctions” such as inequality are not accidents but built into capitalism.'),
        ('Durkheim', 'rapid social change can produce anomie, a state of normlessness', 'Functionalism',
         'When change is too fast for shared norms to adapt (for example in economic crises), regulation weakens and people lose a sense of limits, leading to deviance and suicide.',
         'Critics argue anomie is hard to measure and that the official suicide statistics Durkheim relied on are socially constructed.'),
    ],
    'explain': [
        ('Explain how socialisation contributes to social order, according to functionalists.', 'Functionalists argue that through primary and secondary socialisation individuals internalise shared norms and values, so most people conform willingly; this value consensus makes behaviour predictable and creates social order without constant force.', '1 mark: internalisation of norms/values; 1 mark: agencies (family, education); 1 mark: link to predictability/social order without coercion. [3]'),
        ('Explain what is meant by the claim that institutions are “interdependent”, using an example.', 'Institutions depend on each other to function: for example, the economy needs schools to produce a skilled workforce, and schools depend on families to send socialised children. A change in one institution affects others.', '1 mark: meaning of interdependence; 1 mark: developed example; 1 mark: change in one part affects others. [3]'),
        ('Explain two criticisms of functionalism.', 'It assumes value consensus and ignores conflict and inequality (Marxist and feminist criticism); it sees people as passive “puppets” of the system and ignores agency (interactionist criticism); it is teleological, explaining an institution by its effects.', '2 marks for each criticism identified and explained. [4]'),
        ('Explain the difference between the functionalist and Marxist views of social order.', 'Functionalists see order as based on value consensus that benefits everyone; Marxists see order as imposed by the ruling class through ideology and coercion, serving capitalist interests.', '1 mark functionalist view; 1 mark Marxist view; 1 mark explicit contrast (consensus vs. conflict/ideology). [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why functionalism is described as a structural or “macro” theory', ['it explains behaviour in terms of the structure of society as a whole rather than individual choices', 'it focuses on how institutions fit together and meet society’s needs', 'it sees individuals as shaped by social facts external to them', 'it explains society from the “top down”, starting from the system']),
        ('function', 'functions', 'that shared values perform for society according to functionalists', ['they provide goals that guide behaviour', 'they make behaviour predictable and enable cooperation', 'they create social solidarity and a sense of belonging', 'they reduce the need for coercion, as most people conform willingly']),
    ],
    'claims': [
        ('Functionalists believe that every part of society causes conflict.', False, 'Functionalists stress consensus and integration; each part is seen as contributing to stability, although Merton accepted that some parts may be dysfunctional.'),
        ('Durkheim argued that a certain amount of crime can be functional for society.', True, 'He argued crime reaffirms the boundaries of acceptable behaviour and can allow necessary social change.'),
        ('Parsons saw the family as having no function in modern society.', False, 'Parsons argued the family keeps two “irreducible” functions: primary socialisation and the stabilisation of adult personalities.'),
        ('Functionalism is a consensus, structural theory.', True, 'It explains behaviour by the structure of society and assumes agreement over core values.'),
    ],
    'ar': ([('Functionalists see deviance as a threat to social order.', 'they believe social order depends on shared norms and values.'),
            ('Functionalists use the organic analogy to describe society.', 'they see institutions as parts that function together like organs in a body.'),
            ('Durkheim argued that rapid social change can increase deviance.', 'anomie weakens the norms that regulate behaviour.')],
           ['functionalists argue that all social order is imposed by force.', 'Parsons rejected the idea that societies have needs.']),
    'scen': ['In {city}, a national holiday brings families and communities together in shared ceremonies and celebrations.',
             'After a factory closes in a small town near {city}, crime and suicide rates rise and people say they no longer know “what the rules are”.',
             'A school in {city} holds a weekly assembly where pupils sing the national anthem and celebrate pupils who have worked hard.'],
    'ctx': [('how far young people in {city} share the same values as their parents', {'large', 'meaning'}),
            ('the effects of rapid economic change on community life', {'change', 'meaning'}),
            ('participation in religious and national ceremonies', {'behaviour', 'large'})],
    'data': [dict(what='agreement with shared social values', pop='adults', rows=['Aged 18-34', 'Aged 35-54', 'Aged 55+'], cols=('2005', '2025'),
                  base=[(55, 70), (62, 75), (70, 85)], delta=[(-15, -3), (-10, 0), (-6, 2)], label='percentage agreeing that “most people share the same basic values”',
                  expl=['postmodernists would argue that society has become more fragmented and diverse, so fewer people feel values are shared',
                        'globalisation and migration expose people to a wider range of cultures and values',
                        'older people were socialised when communities and religion were stronger, so they perceive more consensus'],
                  method='questionnaire', claim='modern societies are still based on value consensus',
                  counter='Even if majorities agree, falling figures for younger people suggest growing diversity; Marxists would add that apparent agreement may reflect ruling-class ideology rather than genuine consensus.')],
    'source': [dict(text='A researcher spent a year in a fishing community near {city}. She observed that neighbours helped each other during storms, shared catches with widows and punished people who broke community rules by refusing to trade with them. Almost everyone she spoke to said that “we all believe the same things here”.',
                    method='participant observation', about='value consensus in a community', finds=['neighbours cooperated and shared resources', 'rule-breakers were punished with informal sanctions such as refusing to trade with them'],
                    persp='Functionalism', pview='The community shows value consensus and mechanical solidarity: shared norms are enforced by informal sanctions, which maintains social order, as Durkheim argued.',
                    claim='social order is based mainly on shared values', pro='The source shows cooperation and informal sanctions upholding shared norms; functionalists such as Parsons argue socialisation creates consensus.',
                    con='Marxists argue order is imposed by the powerful through ideology; feminists ask whose values dominate; one small community may be untypical of large, diverse modern societies.', flags={'meaning'})],
    'essays': [('Explain two ways in which functionalists argue that social order is maintained.', 'Socialisation into shared norms and values creates value consensus (Parsons); institutions such as religion and education integrate individuals (Durkheim); social control and sanctions deal with deviance; interdependent institutions meet functional prerequisites.',
                'functionalism provides an adequate explanation of social order in modern societies',
                'Value consensus explains why most people conform without force; socialisation is supported by evidence of shared norms; institutions do perform functions (e.g. education and the economy); Merton’s ideas of latent function and dysfunction make it more flexible.',
                'Marxists see order as imposed through ideology and coercion; feminists see it as patriarchal; interactionists say order is negotiated in interaction; postmodernists argue modern societies are too fragmented for consensus; functionalism struggles to explain conflict and change.')],
}, V1)

c1b = T('Marxism and conflict theory: class, power and ideology')
build(c1b, {
    'terms': [
        ('bourgeoisie', 'the capitalist ruling class who own the means of production', 'owners of factories, banks and large companies'),
        ('proletariat', 'the working class who must sell their labour power to the bourgeoisie in order to survive', 'factory and service workers paid wages'),
        ('means of production', 'the resources used to produce goods and wealth, such as land, factories, machinery and capital', 'a car factory and its machinery'),
        ('ideology', 'a set of ideas and beliefs that justifies the interests of a powerful group', 'the belief that anyone can become rich through hard work'),
        ('false class consciousness', 'a state in which the working class accepts ruling-class ideas and fails to recognise its own exploitation', 'workers believing that inequality is natural and fair'),
        ('hegemony', 'the ideological leadership of the ruling class, which wins the consent of the subordinate class', 'popular media presenting capitalism as the only realistic system'),
        ('surplus value', 'the difference between the value workers produce and the wages they are paid, taken by the capitalist as profit', 'a worker producing goods worth $200 a day but paid $60'),
        ('alienation', 'the loss of control over, and separation from, the products and process of one’s own labour', 'a worker repeating one small task on an assembly line'),
    ],
    'thinkers': [
        ('Marx', 'the history of all hitherto existing society is the history of class struggle', 'Marxism',
         'Marx argued that the economic base (relations of production) shapes the superstructure; the bourgeoisie exploit the proletariat, and class conflict drives historical change.',
         'Critics argue class structure has become more complex (a large middle class) and that predicted revolutions in advanced capitalist societies have not happened.'),
        ('Althusser', 'ideological state apparatuses such as education, the media and religion reproduce capitalist ideology', 'Neo-Marxism',
         'Althusser distinguished repressive state apparatuses (police, army) from ideological state apparatuses that maintain control by shaping beliefs.',
         'Critics argue this is deterministic: it gives people little capacity to resist ideology.'),
        ('Gramsci', 'the ruling class maintains power mainly through hegemony, winning consent rather than using force', 'Neo-Marxism',
         'Gramsci argued that the working class can develop counter-hegemonic ideas through “organic intellectuals”, so ideology can be resisted.',
         'Some argue it is hard to measure hegemony and that consent may simply reflect genuinely shared values.'),
        ('Weber', 'class, status and party are separate sources of power and inequality', 'Weberian theory',
         'Weber argued inequality is not only economic: social status (prestige) and party (political power) can vary independently of class.',
         'Marxists argue Weber underestimates how far economic ownership underlies other forms of power.'),
    ],
    'explain': [
        ('Explain how, according to Marxists, the superstructure helps to maintain capitalism.', 'Institutions in the superstructure (education, religion, media, family, law) spread ruling-class ideology, creating false class consciousness so the working class accepts inequality as natural or fair; this legitimates the economic base and prevents revolution.', '1 mark: base-superstructure idea; 1 mark: ideology/false consciousness; 1 mark: legitimation of capitalism/prevents challenge. [3]'),
        ('Explain the difference between traditional Marxism and neo-Marxism.', 'Traditional Marxism stresses economic determinism and class conflict; neo-Marxists (Gramsci, Frankfurt School) give more weight to culture and ideas, arguing that ideology and hegemony can be resisted and that people have some agency.', '1 mark traditional view; 1 mark neo-Marxist view; 1 mark for contrast (determinism vs agency/culture). [3]'),
        ('Explain how Marxists use the idea of exploitation to explain inequality.', 'Workers produce more value than they receive in wages; the surplus value is taken by capitalists as profit. This creates growing wealth for the bourgeoisie and relative poverty for the proletariat, so inequality is built into capitalism.', '1 mark: surplus value; 1 mark: profit to bourgeoisie; 1 mark: inequality built into system. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of the Marxist view of society', ['it is economically deterministic and underestimates culture and agency', 'the class structure has fragmented, with a large middle class', 'it neglects other inequalities such as gender and ethnicity', 'communist revolutions did not occur in the most advanced capitalist societies as predicted']),
        ('way', 'ways', 'in which, according to Marxists, the ruling class maintains its power', ['through ideology spread by institutions such as education and the media', 'through control of the state, law and police (repressive state apparatus)', 'through economic ownership, controlling jobs and wages', 'by dividing the working class, for example by ethnicity or gender']),
    ],
    'claims': [
        ('Marxists believe that society is based on value consensus.', False, 'Marxism is a conflict theory: apparent agreement reflects ruling-class ideology, not genuine consensus.'),
        ('For Marx, the economic base shapes the rest of society.', True, 'The relations of production (base) shape institutions and ideas in the superstructure.'),
        ('Gramsci argued that the ruling class rules only by force.', False, 'Gramsci emphasised hegemony – rule mainly by consent through ideas – with coercion in the background.'),
        ('Weber agreed with Marx that class is the only source of inequality.', False, 'Weber argued that status and party are also sources of power and inequality.'),
    ],
    'ar': ([('Marxists argue that the working class often accepts inequality.', 'ideology creates false class consciousness.'),
            ('Marx predicted increasing conflict between classes.', 'he believed the proletariat would become aware of its exploitation and form a class for itself.'),
            ('Neo-Marxists give more attention to culture than traditional Marxists.', 'they argue ideology and hegemony are central to maintaining capitalism.')],
           ['Marx argued that the bourgeoisie sell their labour to the proletariat.', 'Althusser argued that ideology plays no part in maintaining capitalism.']),
    'scen': ['A large company in {city} announces record profits while cutting the wages of its warehouse workers.',
             'A popular television programme in {city} follows a poor family who become wealthy by winning a talent competition.',
             'Workers at a clothing factory near {city} go on strike after a fire reveals unsafe working conditions.'],
    'ctx': [('workers’ attitudes towards their employers in a large factory', {'meaning', 'behaviour'}),
            ('how far people accept inequality as fair', {'large', 'meaning'}),
            ('changes in income inequality over the last thirty years', {'change', 'large'})],
    'data': [dict(what='perceptions of class and fairness', pop='workers', rows=['Manual workers', 'Routine non-manual workers', 'Professionals and managers'], cols=('2000', '2025'),
                  base=[(40, 55), (45, 60), (60, 75)], delta=[(-12, 0), (-10, 2), (-5, 4)], label='percentage agreeing that “in this country, people get rewarded for their effort and skill”',
                  expl=['Marxists would argue that ideology (meritocracy) is more accepted by those who benefit most from capitalism',
                        'growing inequality and insecure work may be weakening false class consciousness among manual workers',
                        'Weberians would point to differences in market situation between occupational groups'],
                  method='questionnaire', claim='most people accept ruling-class ideology',
                  counter='Large and possibly growing minorities reject the idea that rewards are fair, suggesting class consciousness and resistance; figures may reflect real differences in experience rather than ideology.')],
    'source': [dict(text='A study of 30 warehouse workers near {city} used unstructured interviews. Many described their work as “boring and pointless” and said they had no say in how it was organised. Yet most said that the company owners “deserved” their wealth because they had “taken the risks”.',
                    method='unstructured interview', about='workers’ experience of work', finds=['workers felt their work was boring and that they had no control over it', 'most workers believed the owners deserved their wealth'],
                    persp='Marxism', pview='The workers experience alienation (no control over their labour) but also show false class consciousness, accepting the ideology that owners deserve their wealth.',
                    claim='the working class is unaware of its exploitation', pro='The workers in the source justify owners’ wealth, supporting the idea of false class consciousness and hegemony (Gramsci).',
                    con='They also recognise alienation and lack of control; strikes, trade unions and protest show awareness; the sample of 30 workers is small and may not be representative.', flags={'meaning'})],
    'essays': [('Explain two ways in which Marxists argue that ideology maintains capitalism.', 'Education teaches acceptance of hierarchy and the myth of meritocracy (Althusser’s ISAs); the media spreads ruling-class ideas (hegemony, Gramsci); religion offers compensation and justifies inequality; consumer culture distracts from exploitation.',
                'Marxism remains a useful theory for understanding modern societies',
                'Inequality of wealth and income persists and has widened; global capitalism and transnational corporations concentrate power; neo-Marxist ideas of hegemony explain consent; precarious work supports ideas of exploitation.',
                'Class structure is more complex and fluid; Weber shows status and party matter; feminists and others stress gender and ethnic inequality; postmodernists see identity as based on consumption, not class; communist societies have largely failed.')],
}, V1)

c1c = T('Feminist perspectives: liberal, Marxist and radical feminism')
build(c1c, {
    'terms': [
        ('patriarchy', 'a social system in which men hold power and dominate women', 'male control of political leadership and household decisions'),
        ('liberal feminism', 'the feminist view that gender inequality can be reduced through reforms such as equal opportunities laws and changes in socialisation', 'campaigns for equal pay legislation'),
        ('radical feminism', 'the feminist view that patriarchy is the main and most universal form of inequality and must be overthrown', 'arguing that the family and sexual relationships are sites of male power'),
        ('Marxist feminism', 'the feminist view that women’s oppression is linked to capitalism, which benefits from women’s unpaid domestic labour', 'housewives reproducing the labour force at no cost to employers'),
        ('gender', 'the socially constructed roles, behaviours and identities associated with being male or female', 'expectations that girls should be caring and boys competitive'),
        ('intersectionality', 'the idea that gender combines with other inequalities such as class, ethnicity and disability to shape experience', 'black working-class women facing racism and sexism at the same time'),
        ('dual burden', 'the situation in which women do paid work and also most of the unpaid domestic work', 'a woman working full-time who also does most of the cooking and childcare'),
    ],
    'thinkers': [
        ('Oakley', 'the housewife role is socially constructed and oppressive rather than natural', 'Liberal feminism',
         'Oakley’s interviews with London housewives found most were dissatisfied with housework, which was monotonous and isolating; she argued gender roles are learnt through socialisation (manipulation and canalisation).',
         'Radical feminists argue reform of socialisation is not enough because patriarchy is structural.'),
        ('Benston', 'women’s unpaid domestic labour benefits capitalism by reproducing the workforce for free', 'Marxist feminism',
         'Benston argued that the nuclear family provides capitalism with a free labour force: women rear the next generation of workers and maintain the current ones at no cost to employers.',
         'Radical feminists argue that patriarchy existed before capitalism, so capitalism cannot be the main cause.'),
        ('Firestone', 'women’s oppression is rooted in their biological role in reproduction, which men have used to control them', 'Radical feminism',
         'Firestone argued that the sexual division of labour originates in childbearing and that women would only be free when technology removed the biological basis of their dependence.',
         'Critics argue it is biologically deterministic and ignores differences between women.'),
        ('Walby', 'patriarchy operates through six structures, including paid work, the household, the state, violence, sexuality and culture', 'Radical feminism',
         'Walby argued there has been a shift from private patriarchy (in the home) to public patriarchy (in work, the state and media).',
         'Postmodern and black feminists argue the concept of patriarchy is too general to capture different women’s experiences.'),
        ('hooks', 'feminism has often reflected the experiences of white, middle-class women and ignored race and class', 'Black feminism',
         'bell hooks argued that black women face interlocking oppressions of racism, sexism and class, so there is no single “women’s experience”.',
         'Some argue that stressing differences between women weakens collective feminist action.'),
    ],
    'explain': [
        ('Explain two differences between liberal and radical feminism.', 'Liberal feminists see inequality as caused by socialisation and discrimination and seek gradual reform through laws and policies; radical feminists see patriarchy as the root of all inequality, embedded in the family and sexuality, and seek revolutionary change, sometimes separatism.', '2 marks for each explained difference (cause of inequality; solution/strategy). [4]'),
        ('Explain why Marxist feminists argue that the family benefits capitalism.', 'Women’s unpaid domestic labour reproduces labour power at no cost; women act as a reserve army of labour; the family absorbs men’s frustration (Ansley’s “takers of shit”) and socialises children into obedience.', '1 mark each valid point, up to 3, with development. [3]'),
        ('Explain what is meant by the claim that gender is socially constructed.', 'Gender roles and identities are learnt through socialisation rather than fixed by biology; they vary between cultures and over time, so behaviours seen as “masculine” or “feminine” are products of society.', '1 mark: learnt not biological; 1 mark: socialisation agencies/process; 1 mark: cross-cultural or historical variation. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of radical feminism', ['it treats all women as sharing the same oppression, ignoring class and ethnicity', 'it underestimates progress towards equality in law, work and education', 'some versions rely on biological arguments', 'separatism is unrealistic for most women']),
        ('way', 'ways', 'in which feminists argue patriarchy is maintained', ['through gender socialisation in families and schools', 'through the unequal domestic division of labour and the dual burden', 'through male violence and the threat of violence', 'through media representations that sexualise and stereotype women', 'through lower pay and the glass ceiling at work']),
    ],
    'claims': [
        ('All feminists agree that capitalism is the main cause of women’s oppression.', False, 'Only Marxist feminists emphasise capitalism; radical feminists see patriarchy as the main cause and liberal feminists point to socialisation and discrimination.'),
        ('Liberal feminists believe equal opportunities laws can help reduce gender inequality.', True, 'They favour gradual reform through law and changes in attitudes and socialisation.'),
        ('Radical feminists see the family as a key site of patriarchal power.', True, 'They argue the family is where men exploit women’s domestic and emotional labour and where domestic violence occurs.'),
        ('Intersectional feminists argue all women experience oppression in the same way.', False, 'They argue gender combines with class, ethnicity, sexuality and disability to produce different experiences.'),
    ],
    'ar': ([('Radical feminists argue that “the personal is political”.', 'they believe that patriarchal power operates in private relationships as well as public life.'),
            ('Liberal feminists favour gradual change.', 'they believe that changing laws and attitudes can achieve equality within existing society.'),
            ('Marxist feminists link women’s oppression to capitalism.', 'women’s unpaid labour reproduces the labour force at no cost to employers.')],
           ['radical feminists argue that patriarchy has disappeared in modern societies.', 'liberal feminists argue that the family must be abolished.']),
    'scen': ['In a dual-earner household in {city}, both partners work full-time but {man}’s wife still does most of the cooking, cleaning and childcare.',
             'A survey in {city} finds that women hold only one in five senior management posts in large companies, although they make up half of the workforce.',
             'Parents in {city} buy dolls and kitchen sets for their daughters and construction toys for their sons.'],
    'views': {'Liberal feminism': 'gender inequality results from socialisation and discrimination; the situation can be improved by reform such as equal opportunities policies, changing attitudes and more equal socialisation, and progress is already happening (Oakley, Somerville).',
              'Marxist feminism': 'women’s position benefits capitalism: their unpaid domestic labour reproduces the workforce and they act as a cheap, flexible reserve army of labour, so the situation reflects both capitalism and patriarchy (Benston, Ansley).',
              'Radical feminism': 'the situation is an example of patriarchy, the system of male domination found in all societies; men benefit from women’s labour and subordination, and only radical change will end it (Firestone, Walby).',
              'Functionalism': 'different roles for men and women may be seen as functional: Parsons argued instrumental (male) and expressive (female) roles complement each other and help the family meet society’s needs.'},
    'ctx': [('women’s experiences of the dual burden', {'meaning', 'private', 'behaviour'}),
            ('gender stereotypes in children’s play', {'young', 'behaviour'}),
            ('the gender pay gap across different occupations', {'large', 'change'})],
    'data': [dict(what='gender and senior employment', pop='large companies', rows=['Women', 'Men'], cols=('2010', '2025'),
                  base=[(12, 20), (80, 88)], delta=[(3, 12), (-12, -3)], label='percentage of senior management posts held', n=[120, 150, 200, 250, 300],
                  expl=['liberal feminists would point to equal opportunities laws and changing attitudes',
                        'radical feminists would argue that a glass ceiling and male networks still keep most senior posts for men',
                        'Marxist feminists would argue women are used as a flexible reserve army of labour in lower-paid roles'],
                  method='official statistics', claim='gender inequality in employment is disappearing',
                  counter='Women still hold a minority of senior posts; pay gaps, part-time work and the dual burden continue, as radical and Marxist feminists argue.')],
    'source': [dict(text='A researcher interviewed 40 women in {city} who worked full-time. Most said that they still did the majority of housework and childcare, and many described feeling “exhausted”. Several said their partners “helped” but did not take responsibility for planning family life.',
                    method='semi-structured interview', about='women’s domestic responsibilities', finds=['most of the women did the majority of housework and childcare', 'partners “helped” but did not take responsibility for planning (the mental load)'],
                    persp='Radical feminism', pview='The findings show patriarchy in the private sphere: men benefit from women’s unpaid labour and emotional work, creating a dual burden.',
                    claim='women remain unequal to men in modern families', pro='The source shows women still do most domestic work despite paid employment, supporting feminist ideas of the dual burden and triple shift.',
                    con='Liberal feminists point to gradual change and more shared roles in younger couples; Young and Willmott claim families are more symmetrical; the sample of 40 working women in one city may not represent all families.', flags={'meaning', 'private'})],
    'essays': [('Explain two differences between Marxist feminist and radical feminist views of society.', 'Cause: capitalism and patriarchy together vs patriarchy as the primary, universal system; Solution: overthrow capitalism vs overthrow patriarchy/separatism; View of men: workers also exploited vs men as the main beneficiaries.',
                'radical feminism gives the best explanation of gender inequality',
                'Patriarchy appears in all societies (universality); evidence of domestic violence and the dual burden; Walby shows patriarchy has moved into public spheres; “the personal is political” highlights hidden inequalities.',
                'Liberal feminists show progress through reform; Marxist feminists link inequality to capitalism; black and intersectional feminists say it ignores differences between women; postmodernists reject a single explanation; some versions are biologically deterministic.')],
}, V1)

c1d = T('Interactionism and social action theory: meanings, labelling and the self')
build(c1d, {
    'terms': [
        ('social action theory', 'an approach that explains society through the meanings and motives behind individuals’ actions', 'Weber explaining behaviour by the reasons actors give for it'),
        ('verstehen', 'empathetic understanding of the meanings people give to their actions', 'a researcher trying to see the world through a gang member’s eyes'),
        ('labelling', 'the process of attaching a definition or name to a person, which may shape how others treat them', 'a teacher calling a pupil a “troublemaker”'),
        ('self-fulfilling prophecy', 'a prediction that comes true because people act on it', 'a pupil labelled as weak losing confidence and doing badly'),
        ('looking-glass self', 'Cooley’s idea that our self-image develops from how we think others see us', 'a teenager deciding they are clever because teachers praise them'),
        ('master status', 'a status that dominates all others in shaping how a person is seen by others', 'being seen first and foremost as an “ex-prisoner”'),
        ('definition of the situation', 'the meaning people give to a situation, which shapes how they act in it', 'treating a rumour of a bank collapse as true and withdrawing savings'),
    ],
    'thinkers': [
        ('Mead', 'the self develops through interaction as children learn to take the role of the other', 'Interactionism',
         'Mead distinguished the “I” (spontaneous self) from the “me” (socialised self); through play and games children learn to see themselves as others see them (the generalised other).',
         'Structural sociologists argue it neglects how wider structures such as class shape interaction.'),
        ('Becker', 'deviance is not a quality of the act but the result of others successfully applying a label', 'Interactionism',
         'Becker argued that “deviant behaviour is behaviour that people so label”; the powerful (“moral entrepreneurs”) create rules and labels.',
         'Critics argue it ignores the causes of initial deviance and the harm done to victims.'),
        ('Goffman', 'social life can be understood as a performance in which individuals manage the impressions they give to others', 'Interactionism',
         'Goffman’s dramaturgical approach describes front-stage and back-stage behaviour and impression management.',
         'Critics argue it describes interaction cleverly but does not explain why some people have more power to define situations.'),
        ('Weber', 'sociology must understand the meanings behind social action as well as its causes', 'Social action theory',
         'Weber identified types of action (instrumentally rational, value-rational, traditional, affectual) and stressed verstehen.',
         'Positivists argue that subjective meanings cannot be measured objectively.'),
        ('Cooley', 'the self is a “looking-glass self”, formed by imagining how others see us', 'Interactionism',
         'Cooley argued people imagine how they appear to others, imagine others’ judgements and develop feelings about themselves accordingly.',
         'It may overstate how far people accept others’ views; people can resist negative labels.'),
    ],
    'explain': [
        ('Explain how labelling can lead to a self-fulfilling prophecy.', 'A person is given a label (e.g. “troublemaker”); others treat them in line with the label; the person internalises it as part of their self-concept and acts in ways that confirm it, so the prediction comes true.', '1 mark: label applied; 1 mark: others’ treatment; 1 mark: internalisation and behaviour confirming label. [3]'),
        ('Explain why interactionism is described as a “micro” approach.', 'It studies small-scale, face-to-face interaction and the meanings individuals create, rather than the structure of society as a whole; society is seen as built “from the bottom up”.', '1 mark: small-scale interaction; 1 mark: meanings/agency; 1 mark: contrast with structural/macro theories. [3]'),
        ('Explain two criticisms of interactionism.', 'It neglects wider social structures and power such as class and patriarchy; it is hard to generalise from its small-scale studies; it can be too deterministic about labels, ignoring resistance; it does not explain where labels originate.', '2 marks each explained criticism. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why interactionists prefer qualitative research methods', ['they want to understand meanings, which requires verstehen', 'qualitative methods allow people to describe experiences in their own words', 'they see social reality as constructed in interaction, which numbers cannot capture', 'methods such as participant observation reveal how labels are applied in real situations']),
    ],
    'claims': [
        ('Interactionists believe behaviour is determined by social structure.', False, 'They stress agency: people actively interpret and negotiate meanings, though they may be constrained.'),
        ('Becker argued that no act is deviant in itself.', True, 'An act becomes deviant when others label it as such.'),
        ('A self-fulfilling prophecy always happens when a label is applied.', False, 'People may reject or resist labels (e.g. Fuller’s study of black girls who worked hard to prove teachers wrong).'),
        ('Goffman used the idea of a theatre to describe social interaction.', True, 'His dramaturgical approach uses front stage, back stage and impression management.'),
    ],
    'ar': ([('Interactionists use methods such as participant observation.', 'they want to understand the meanings people give to their actions.'),
            ('Labels can change a person’s self-concept.', 'people develop their sense of self partly through how others see them.'),
            ('Weber stressed verstehen.', 'he argued that understanding motives is essential to explaining social action.')],
           ['interactionists see society as a system that determines individual behaviour.', 'Mead argued the self is present at birth and does not change.']),
    'scen': ['At a new school in {city}, {person} is seated at the back of the class and called “lazy” by a teacher in the first week; by the end of term {person} has stopped handing in homework.',
             'A young man in {city} who has been released from prison finds that employers reject him as soon as they learn about his conviction.',
             'Staff at a restaurant in {city} are polite and cheerful to customers but joke and complain about them in the kitchen.'],
    'ctx': [('how teachers’ labels affect pupils’ self-image', {'young', 'meaning', 'behaviour'}),
            ('how people who have been to prison manage their identity', {'hidden', 'meaning', 'sensitive'}),
            ('everyday impression management in the workplace', {'behaviour', 'meaning'})],
    'data': [dict(what='labelling in schools', pop='pupils', rows=['Pupils labelled “able” by teachers', 'Pupils labelled “less able” by teachers'], cols=('Start of year', 'End of year'),
                  base=[(65, 78), (40, 55)], delta=[(0, 8), (-12, -2)], label='percentage of pupils who described themselves as “good at school work”',
                  expl=['pupils internalise teachers’ labels, as the looking-glass self suggests', 'teachers may give more attention and encouragement to pupils they label as able, creating a self-fulfilling prophecy',
                        'pupils labelled less able may form anti-school subcultures to protect their self-esteem'],
                  method='questionnaire', claim='teachers’ labels shape pupils’ self-concept', flags={'young'},
                  counter='Pupils’ self-image may also reflect real differences in attainment, family background or peer groups; some pupils resist labels; self-report questionnaires with children may lack validity.')],
    'source': [dict(text='A researcher observed lessons in a secondary school in {city} for six months. She noticed that teachers asked more questions of pupils in top sets and praised them more often. In bottom sets, teachers spent more time on discipline, and pupils described themselves as “the thick ones”.',
                    method='non-participant observation', about='teacher labelling in classrooms', finds=['teachers asked more questions of top-set pupils and praised them more', 'bottom-set pupils described themselves as “the thick ones”'],
                    persp='Interactionism', pview='The source shows labelling in interaction: teachers’ different treatment communicates labels that pupils internalise, which can create a self-fulfilling prophecy.',
                    claim='labelling is the main reason for differences in pupils’ achievement', pro='The source shows teachers treating sets differently and pupils internalising labels; studies such as Rosenthal and Jacobson support the self-fulfilling prophecy.',
                    con='Structural factors such as material deprivation and cultural capital also matter; pupils may resist labels; observation may have changed teachers’ behaviour (Hawthorne effect).', flags={'young', 'behaviour'})],
    'essays': [('Explain two ways in which interactionists explain the development of the self.', 'Mead’s “I” and “me” and taking the role of the other; Cooley’s looking-glass self; labelling and the self-fulfilling prophecy; Goffman’s impression management and master status.',
                'interactionism gives a more useful understanding of society than structural theories',
                'It shows people are active and create meanings; explains how labels and self-fulfilling prophecies work; produces valid, detailed studies (Becker, Goffman); avoids the determinism of functionalism and Marxism.',
                'It ignores structure and power (class, patriarchy); cannot explain large-scale patterns; findings are hard to generalise; structuration (Giddens) suggests both structure and action are needed.')],
}, V1)

c1e = T('Postmodernism and the idea of a fragmented society')
build(c1e, {
    'terms': [
        ('postmodernity', 'a stage of society characterised by diversity, fragmentation, choice and rapid change, following modernity', 'societies in which people choose from many lifestyles and identities'),
        ('metanarrative', 'a “big story” or grand theory that claims to explain everything about society', 'Marxism’s claim to explain all history as class struggle'),
        ('fragmentation', 'the breaking up of society into many different groups, cultures and lifestyles with no single shared culture', 'many subcultures and online communities replacing a single national culture'),
        ('hyperreality', 'a condition in which media images and simulations seem more real than reality itself', 'people experiencing a war mainly through television and social media images'),
        ('pick and mix identity', 'an identity constructed by choosing from a range of cultural options rather than inherited from class or tradition', 'a young person combining fashion, music and religion from several cultures'),
        ('consumer culture', 'a culture in which identity is expressed mainly through the goods and lifestyles people buy', 'identifying oneself through brands and leisure choices'),
    ],
    'thinkers': [
        ('Lyotard', 'postmodern society is marked by incredulity towards metanarratives', 'Postmodernism',
         'Lyotard argued people no longer believe in grand theories (religion, science, Marxism) that claim to offer the truth; knowledge is fragmented into many “language games”.',
         'Critics point out that the claim that there are no metanarratives is itself a kind of metanarrative.'),
        ('Baudrillard', 'in postmodern society media signs and simulations create a hyperreality', 'Postmodernism',
         'Baudrillard argued that images no longer represent reality; simulacra (copies without originals) become more “real” to people than the world they refer to.',
         'Critics argue that real inequalities in income, health and power still shape people’s lives regardless of media images.'),
        ('Giddens', 'we live in late modernity, in which tradition declines and individuals must reflexively construct their own identities', 'Late modernity',
         'Giddens rejects the idea of a completely new postmodern era: late modernity is an intensification of modern features such as reflexivity and globalisation.',
         'Postmodernists argue the changes are so great that a new type of society has emerged.'),
        ('Bauman', 'modern society has become “liquid”, with fluid and unstable relationships and identities', 'Postmodernism',
         'Bauman argued that in liquid modernity people’s commitments, jobs and relationships are temporary, which brings freedom but also insecurity.',
         'Critics argue many people still have stable jobs, families and communities.'),
    ],
    'explain': [
        ('Explain why postmodernists reject metanarratives such as Marxism and functionalism.', 'They argue society is too diverse and fragmented for one theory to explain; there is no single truth, only competing perspectives; grand theories claim objectivity they cannot have.', '1 mark: fragmentation/diversity; 1 mark: no single truth/relativism; 1 mark: developed example. [3]'),
        ('Explain two criticisms of postmodernism.', 'It exaggerates choice: class, gender and ethnicity still constrain identities (Philo and Miller); its own claim that there are no truths is a metanarrative; it offers no basis for improving society; there is little empirical evidence for some claims.', '2 marks each explained criticism. [4]'),
    ],
    'why': [
        ('feature', 'features', 'of postmodern society', ['fragmentation and cultural diversity', 'identities based on consumption and choice', 'media saturation and hyperreality', 'globalisation and rapid change', 'loss of faith in metanarratives']),
    ],
    'claims': [
        ('Postmodernists argue that social class is the main source of identity today.', False, 'They argue identity is chosen and based on consumption and lifestyle rather than fixed by class.'),
        ('Giddens describes contemporary society as “late modernity” rather than postmodernity.', True, 'He sees current changes as an intensification of modernity, not a complete break.'),
        ('Baudrillard argued that media images represent reality accurately.', False, 'He argued signs and simulations create a hyperreality that replaces reality.'),
    ],
    'ar': ([('Postmodernists reject structural theories.', 'they argue society is too fragmented for a single theory to explain.'),
            ('Postmodernists see identity as fluid.', 'people can choose from a wide range of lifestyles and cultural options.')],
           ['postmodernists argue that society is becoming more uniform.', 'Lyotard argued that metanarratives are becoming more popular.']),
    'scen': ['{person}, a teenager in {city}, mixes K-pop music, streetwear from the USA, traditional family festivals and an online gaming identity.',
             'A survey in {city} finds that fewer young people describe themselves as “working class” or “middle class”, and more describe themselves through hobbies, brands and online communities.'],
    'views': {'Postmodernism': 'identity is now chosen and fluid; consumption, media and globalisation allow pick-and-mix identities, so fixed categories such as class matter less (Lyotard, Baudrillard).',
              'Marxism': 'apparent choice is shaped by capitalism and advertising; consumer identities are a form of ideology that distracts from continuing class inequality.',
              'Late modernity': 'individuals in late modernity must reflexively construct their identities as tradition declines, but structures such as class still influence their choices (Giddens).'},
    'ctx': [('how young people construct identities online', {'meaning', 'behaviour'}),
            ('the importance of social class to people’s sense of identity', {'large', 'change', 'meaning'})],
    'data': [dict(what='sources of identity', pop='young people aged 16-24', rows=['Social class', 'Nationality', 'Hobbies and lifestyle'], cols=('2000', '2025'),
                  base=[(30, 45), (45, 60), (20, 35)], delta=[(-15, -3), (-12, 0), (5, 18)], label='percentage saying this is “very important” to their identity',
                  expl=['postmodernists argue that identities are increasingly based on consumption and lifestyle choice', 'globalisation and the media expose young people to many cultural options',
                        'decline of traditional industries has weakened working-class communities and identities'],
                  method='questionnaire', claim='traditional sources of identity such as class are no longer important',
                  counter='Many young people still see class and nationality as important; class still shapes life chances even if people do not identify with it; one age group may be untypical.')],
    'essays': [('Explain two features of postmodern society, according to postmodernists.', 'Fragmentation and diversity; rejection of metanarratives (Lyotard); media saturation and hyperreality (Baudrillard); identities based on consumption and choice; liquid relationships (Bauman).',
                'society has become so fragmented that structural theories are no longer useful',
                'Diversity of families, cultures and identities; decline of class identity; globalisation and media; Lyotard’s incredulity towards metanarratives.',
                'Class, gender and ethnic inequalities still shape life chances; Giddens argues this is late modernity; postmodernism’s own claims form a metanarrative; neo-Marxists see consumer culture as ideology.')],
})

CHAPTERS[1] = [c1a, c1b, c1c, c1d, c1e]


# ============================================================== CHAPTER 2: Socialisation and identity

V2 = {
    'Functionalism': 'socialisation passes on the shared norms and values of society, creating value consensus and preparing individuals for adult roles; agencies such as the family and school integrate the individual into society (Parsons, Durkheim).',
    'Marxism': 'socialisation transmits ruling-class ideology, teaching people to accept hierarchy and inequality as normal; agencies such as education and the media reproduce capitalist values and false class consciousness (Althusser).',
    'Liberal feminism': 'gender socialisation teaches boys and girls different, unequal roles; changing socialisation (non-sexist toys, books and teaching) can reduce gender inequality (Oakley).',
    'Interactionism': 'socialisation is an active, two-way process: individuals interpret and negotiate the norms and roles they are taught, and the self develops through interaction with significant others (Mead, Cooley).',
    'Postmodernism': 'people now choose from a wide range of global cultural influences, especially through the media, so socialisation is more fragmented and identities are more fluid.',
}

c2a = T('Culture, norms, values, roles and status')
build(c2a, {
    'terms': [
        ('culture', 'the shared way of life of a group, including its norms, values, beliefs, language and material objects, passed from one generation to the next', 'the food, festivals, language and customs of a community'),
        ('norms', 'specific, informal rules or expectations about how people should behave in particular situations', 'queuing in a shop or shaking hands when meeting someone'),
        ('values', 'general beliefs about what is good, right and worth striving for in a society', 'respect for elders or the importance of individual achievement'),
        ('role', 'the set of expected behaviours attached to a particular position in society', 'the role of a teacher, which involves teaching and caring for pupils'),
        ('ascribed status', 'a social position given at birth or fixed by characteristics a person cannot change', 'royal status or caste position inherited from parents'),
        ('achieved status', 'a social position gained through a person’s own effort, abilities or choices', 'becoming a doctor after years of study'),
        ('subculture', 'a group within a society whose norms and values differ in some ways from those of the mainstream culture', 'a youth music subculture with its own style and slang'),
        ('cultural diversity', 'the existence of different cultures and ways of life within and between societies', 'several languages, religions and cuisines within one city'),
    ],
    'thinkers': [
        ('Linton', 'every society distinguishes between ascribed and achieved statuses', 'Functionalism',
         'Linton argued that statuses are positions in society with attached roles; ascribed statuses are fixed at birth and achieved statuses are earned.',
         'Critics argue many “achieved” statuses still depend heavily on ascribed characteristics such as class and ethnicity.'),
        ('Parsons', 'modern industrial societies are based on universalistic values and achieved status rather than particularistic values and ascribed status', 'Functionalism',
         'Parsons argued that in modern societies people are judged by the same standards and positions are allocated on merit, unlike in traditional societies.',
         'Marxists argue that inequality of opportunity means ascribed characteristics such as class still largely determine status.'),
        ('Merton', 'people may experience role conflict when the expectations of different roles clash', 'Functionalism',
         'Merton developed the idea of the role set: each status has several roles attached, and their demands can conflict.',
         'Interactionists argue roles are not fixed scripts but are negotiated and interpreted by individuals.'),
    ],
    'explain': [
        ('Explain the difference between norms and values, using an example of each.', 'Values are general beliefs about what is desirable (e.g. respect for privacy); norms are specific rules of behaviour that put values into practice (e.g. knocking before entering a room).', '1 mark each definition; 1 mark each example; must show the link that norms express values. [4]'),
        ('Explain why norms vary between cultures, using an example.', 'Norms are socially constructed and learnt, not biologically fixed; different societies have different histories, religions and environments, so they develop different rules (e.g. greeting norms differ: bowing in Japan, handshakes in many Western countries).', '1 mark socially constructed/learnt; 1 mark reason for variation; 1 mark example. [3]'),
        ('Explain what is meant by role conflict, using an example.', 'Role conflict occurs when the expectations of two or more of a person’s roles clash, e.g. a working parent who must attend an important meeting at the same time as their child’s school event.', '1 mark definition; 1 mark developed example. [2]'),
    ],
    'why': [
        ('reason', 'reasons', 'why culture is said to be learnt rather than inherited', ['cultural norms vary greatly between societies, which would not happen if they were biological', 'children raised in a different culture adopt its norms and language', 'norms change over time within the same society', 'feral children who lack socialisation do not acquire culture']),
        ('way', 'ways', 'in which a person’s status may affect their life chances', ['high status may bring higher income and better access to education and health care', 'ascribed status such as caste or gender may limit opportunities', 'status affects how others treat a person and the respect they receive', 'status can give power and influence over others']),
    ],
    'claims': [
        ('Values are more specific than norms.', False, 'Values are general beliefs; norms are the specific rules that put values into practice.'),
        ('A person’s gender is an example of an ascribed status in many societies.', True, 'It is assigned at birth and in many societies shapes the positions open to a person.'),
        ('Culture is the same in every society.', False, 'Culture varies greatly between and within societies (cultural diversity), showing it is socially constructed.'),
        ('Norms can change over time.', True, 'For example, norms about cohabitation and divorce have changed greatly in many societies since the 1960s.'),
    ],
    'ar': ([('Norms vary between societies.', 'norms are socially constructed rather than biologically determined.'),
            ('Modern societies place more emphasis on achieved status.', 'positions in modern societies are increasingly allocated through education and qualifications.'),
            ('Subcultures can exist within a mainstream culture.', 'groups may share some mainstream values while having distinctive norms of their own.')],
           ['ascribed status is gained through personal effort.', 'values are the specific rules that govern behaviour in particular situations.']),
    'scen': ['{person}, who has recently moved to {city}, is unsure whether to bow, shake hands or kiss on the cheek when meeting colleagues.',
             'In {city}, a young woman who is a full-time nurse, a mother and a carer for her elderly father says she “cannot be in three places at once”.',
             'A group of young skateboarders in {city} have their own slang, clothing style and rules about who belongs.'],
    'ctx': [('the norms and values of a youth subculture in {city}', {'hidden', 'meaning', 'behaviour'}),
            ('role conflict experienced by working parents', {'meaning', 'sensitive'}),
            ('changing attitudes towards achieved and ascribed status', {'large', 'change'})],
    'data': [dict(what='attitudes to status and success', pop='adults', rows=['People aged 18-34', 'People aged 35-59', 'People aged 60+'], cols=('2000', '2025'),
                  base=[(55, 70), (50, 65), (40, 55)], delta=[(2, 12), (0, 8), (-3, 6)], label='percentage agreeing that “success depends mainly on hard work rather than family background”',
                  expl=['modern societies emphasise achieved status and meritocracy, as Parsons argued', 'younger people have grown up with wider access to education and may believe positions are earned',
                        'older people may remember more rigid social hierarchies based on ascribed status'],
                  method='questionnaire', claim='achieved status has replaced ascribed status in modern societies',
                  counter='Beliefs are not the same as reality: social mobility studies show family background still strongly affects life chances; ascribed characteristics such as gender, ethnicity and caste still matter.')],
    'essays': [('Explain two ways in which culture influences human behaviour.', 'Norms guide behaviour in specific situations and are enforced by sanctions; values shape goals and choices; roles give expectations attached to statuses; language and beliefs shape how people see the world.',
                'human behaviour is shaped more by culture than by individual choice',
                'Norms, values and roles are learnt and enforced through sanctions; cultural variation shows behaviour is learnt; functionalists stress value consensus; feral children show culture is needed to become human.',
                'Interactionists argue people interpret and negotiate norms; postmodernists stress choice; individuals can resist or reject norms (deviance, subcultures); some behaviour may have biological influences.')],
}, V2)

c2b = T('Primary and secondary socialisation and agencies of socialisation')
build(c2b, {
    'terms': [
        ('socialisation', 'the lifelong process by which people learn the culture (norms, values and roles) of their society', 'a child learning table manners and language'),
        ('primary socialisation', 'the early socialisation of children, mainly by the family, in which basic norms, values and language are learnt', 'parents teaching a toddler to say “please” and “thank you”'),
        ('secondary socialisation', 'socialisation that continues beyond the family, through agencies such as schools, peer groups, the media, religion and the workplace', 'a new employee learning the unwritten rules of the workplace'),
        ('agency of socialisation', 'a group or institution that teaches people the norms and values of society', 'the family, school, peer group, media or religion'),
        ('hidden curriculum', 'the norms, values and attitudes that schools teach informally through their organisation and routines, rather than through formal lessons', 'learning punctuality and respect for authority'),
        ('peer group', 'a group of people of similar age and status who influence each other’s behaviour', 'teenage friends who share fashion and music tastes'),
        ('role model', 'a person whose behaviour is copied by others, especially children', 'a child copying an older sibling or a sports star'),
        ('re-socialisation', 'the process of learning new norms and values to replace earlier ones, often in a new setting', 'a new prisoner or army recruit learning the rules of the institution'),
    ],
    'thinkers': [
        ('Parsons', 'the family is a “personality factory” whose main function is the primary socialisation of children', 'Functionalism',
         'Parsons argued that children internalise society’s norms and values in the family, so that they become part of their personality.',
         'Interactionists argue children are not passive: they actively interpret what they are taught.'),
        ('Bowles and Gintis', 'the hidden curriculum of schools prepares pupils to accept the hierarchy and discipline of capitalist workplaces', 'Marxism',
         'Bowles and Gintis’s correspondence principle holds that school mirrors work: pupils learn obedience, punctuality and to be motivated by external rewards (grades, like wages).',
         'Critics such as Willis show pupils can resist the hidden curriculum rather than accept it.'),
        ('Oakley', 'gender socialisation takes place through manipulation and canalisation', 'Liberal feminism',
         'Oakley argued that parents manipulate children’s self-concept by encouraging gender-appropriate behaviour and canalise them towards gender-typed toys and activities.',
         'Critics argue that children today experience much more varied gender socialisation and choose their own identities.'),
        ('Mead', 'children learn to take the role of the other, first through play and then through games', 'Interactionism',
         'Mead argued that through imitation, play and games children learn the perspectives of significant others and eventually the “generalised other”, the norms of society.',
         'Structural theorists argue it underplays how socialisation is shaped by power and inequality.'),
    ],
    'explain': [
        ('Explain two ways in which the peer group acts as an agency of socialisation.', 'Peers use informal sanctions (approval, teasing, exclusion) to enforce group norms; they provide role models for style, language and attitudes; they can encourage conformity or deviance through peer pressure.', '2 marks for each way explained (identification + development). [4]'),
        ('Explain how the media may influence the socialisation of young people.', 'The media provides role models and representations of gender, ethnicity and success; repeated messages may shape norms and values; social media creates pressure to conform to ideals of appearance and lifestyle; however audiences interpret messages actively.', '1 mark each valid explained point up to 3. [3]'),
        ('Explain the difference between primary and secondary socialisation, using an example of each.', 'Primary socialisation occurs in early childhood mainly in the family and teaches basic norms and language (e.g. toilet training); secondary socialisation occurs later through school, peers, media and work (e.g. learning to raise a hand to speak in class).', '1 mark each definition; 1 mark each example. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why the family is often seen as the most important agency of socialisation', ['primary socialisation shapes basic norms, values and language at the most formative age', 'children spend most of their early years with their family', 'emotional bonds make children likely to copy parents as role models', 'parents use rewards and punishments to shape behaviour']),
        ('way', 'ways', 'in which schools socialise pupils', ['through the formal curriculum, which teaches knowledge and skills valued by society', 'through the hidden curriculum of rules, routines and hierarchy', 'through rewards and sanctions such as merits and detentions', 'through teachers acting as role models', 'by teaching shared national history and values']),
    ],
    'claims': [
        ('Socialisation stops when a person becomes an adult.', False, 'Socialisation is lifelong: adults continue to learn new roles through work, parenthood, the media and re-socialisation.'),
        ('Secondary socialisation includes learning norms at work.', True, 'The workplace is an agency of secondary socialisation where people learn new roles and occupational norms.'),
        ('Marxists see the hidden curriculum as preparing pupils for exploitation at work.', True, 'Bowles and Gintis argue it produces an obedient, disciplined workforce that accepts hierarchy.'),
        ('Interactionists see children as passive receivers of socialisation.', False, 'Interactionists see socialisation as active: children interpret and negotiate what they learn.'),
    ],
    'ar': ([('The hidden curriculum teaches pupils to accept authority.', 'school routines such as obeying teachers and following timetables mirror the discipline of work.'),
            ('Primary socialisation is usually carried out by the family.', 'young children spend most of their time with family members.'),
            ('Peer groups can encourage deviance as well as conformity.', 'peers enforce their own norms through approval and rejection.')],
           ['secondary socialisation always takes place before primary socialisation.', 'the media has no influence on the norms of young people.']),
    'scen': ['{person}, aged 14, starts dressing and speaking like a group of older students at school in {city} and stops spending time with family at weekends.',
             'A new recruit to the army in {city} has to wear a uniform, follow strict routines and obey orders without question.',
             'Parents in {city} give their son toy cars and praise him for being “tough”, while they buy their daughter dolls and praise her for being “kind”.'],
    'ctx': [('how parents socialise young children into gender roles', {'young', 'private', 'behaviour'}),
            ('the influence of social media on teenagers’ values', {'young', 'meaning', 'large'}),
            ('the hidden curriculum in a secondary school', {'young', 'behaviour'})],
    'data': [dict(what='influences on young people', pop='young people aged 13-17', rows=['Parents', 'Friends', 'Social media'], cols=('2010', '2025'),
                  base=[(45, 60), (20, 30), (5, 15)], delta=[(-15, -3), (-4, 6), (8, 20)], label='percentage naming this as the “biggest influence on my opinions”', share=True,
                  expl=['the growth of social media has made it a powerful agency of secondary socialisation', 'peer groups now operate online as well as in person',
                        'postmodernists argue young people draw on many global influences rather than only the family'], flags={'young'},
                  method='questionnaire', claim='the family is no longer the most important agency of socialisation',
                  counter='Parents are still the most named influence for many; primary socialisation in early childhood shapes how young people interpret later influences; self-reports by teenagers may underestimate family influence.')],
    'source': [dict(text='A researcher observed 25 families with young children in {city}, visiting each home twice a week for a month. She noted that parents usually praised girls for being helpful and boys for being brave. Several parents said they “treated their children the same”, but their behaviour often differed.',
                    method='non-participant observation', about='gender socialisation in families', finds=['parents praised girls for being helpful and boys for being brave', 'parents claimed to treat children the same but their behaviour often differed'],
                    persp='Liberal feminism', pview='The findings show gender socialisation through manipulation (praise for gender-appropriate behaviour), as Oakley argued; changing parents’ practices could reduce inequality.',
                    claim='the family is the most important agency of gender socialisation', pro='The source shows parents shaping gendered behaviour from an early age; primary socialisation is highly influential (Oakley, Parsons).',
                    con='Schools, peers and the media also teach gender norms; children actively negotiate identities; the observer’s presence may have changed parents’ behaviour and 25 families in one city are not representative.', flags={'young', 'private', 'behaviour'})],
    'essays': [('Explain two ways in which secondary agencies of socialisation shape identity.', 'Education: formal and hidden curriculum, labelling, gender subject choice; peer groups: informal sanctions and subcultural identities; media: role models and representations; religion: moral values and community identity; workplace: occupational norms.',
                'the family remains the most important agency of socialisation in modern societies',
                'Primary socialisation shapes basic norms, language and personality (Parsons); strong emotional bonds; family influences later choices of school and friends.',
                'Media and peer groups have growing influence; education spends many hours shaping pupils; postmodernists see fragmented, chosen identities; family diversity means family socialisation varies; Marxists stress the role of education and media in spreading ideology.')],
}, V2)

c2c = T('The nature versus nurture debate: feral children and cultural diversity')
build(c2c, {
    'terms': [
        ('nature', 'the view that human behaviour is mainly determined by biological or genetic factors', 'claims that aggression is caused by male hormones'),
        ('nurture', 'the view that human behaviour is mainly shaped by socialisation and the social environment', 'children learning language and customs from those around them'),
        ('feral children', 'children who have grown up with little or no human contact and so have not been socialised', 'children found living with animals or locked away from society'),
        ('instinct', 'a fixed, inborn pattern of behaviour that does not have to be learnt', 'a baby’s sucking reflex'),
        ('cultural relativism', 'the idea that behaviour should be understood in relation to the culture in which it occurs, not judged by the standards of another culture', 'understanding different marriage customs in their own cultural context'),
        ('biological determinism', 'the belief that biology fixes human behaviour and social differences', 'claims that women are naturally better suited to childcare'),
        ('cross-cultural comparison', 'comparing behaviour and norms in different societies to see whether they are universal or culturally specific', 'comparing gender roles among different peoples'),
    ],
    'thinkers': [
        ('Mead (Margaret)', 'gender roles vary greatly between societies, showing that they are culturally rather than biologically determined', 'Interactionism',
         'Margaret Mead’s anthropological studies in New Guinea reported very different patterns of male and female temperament among the Arapesh, Mundugumor and Tchambuli.',
         'Later researchers questioned the accuracy of her fieldwork and interpretations.'),
        ('Curtiss', 'the case of Genie showed that a child deprived of human contact during early childhood could not fully acquire language', 'Interactionism',
         'Genie, discovered aged 13 after years of isolation, learnt some words but never mastered grammar, suggesting a critical period for socialisation.',
         'Single cases may be untypical: Genie may have had developmental problems from birth, and she suffered severe abuse.'),
        ('Murdock', 'some social institutions, such as the nuclear family, are universal because they meet basic needs', 'Functionalism',
         'Murdock studied over 200 societies and argued the nuclear family was found in all of them, performing sexual, reproductive, economic and educational functions.',
         'Cross-cultural evidence of diverse family types (e.g. the Nayar) challenges the claim of universality.'),
    ],
    'explain': [
        ('Explain how studies of feral children support the nurture side of the debate.', 'Feral children such as Genie or children raised with animals lack language, human norms and social skills; this shows such behaviour is learnt through socialisation rather than biologically inherited, and that there may be a critical period for learning.', '1 mark: what feral children lack; 1 mark: shows behaviour is learnt; 1 mark: critical period/limitation. [3]'),
        ('Explain two limitations of using feral children as evidence in the nature versus nurture debate.', 'Cases are rare and often poorly documented, so they are unreliable; the children may have had learning disabilities from birth (which may be why they were abandoned); abuse and trauma may explain their behaviour; it is unethical to study deprivation deliberately.', '2 marks for each explained limitation. [4]'),
        ('Explain how cross-cultural evidence is used to support the view that behaviour is culturally determined.', 'If behaviour such as gender roles, eating habits or marriage customs varies greatly between societies, it cannot be fixed by biology, which is the same in all humans; so behaviour must be learnt through culture.', '1 mark: variation between societies; 1 mark: biology is constant; 1 mark: conclusion and example. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why most sociologists emphasise nurture rather than nature', ['norms and values vary between cultures and over time', 'feral children show that human behaviour must be learnt', 'gender roles differ across societies', 'socialisation and sanctions shape behaviour throughout life']),
    ],
    'claims': [
        ('Feral children prove that biology has no influence on human behaviour.', False, 'They show socialisation is essential, but they do not rule out biological influences; most sociologists see nature and nurture interacting.'),
        ('Cultural diversity in gender roles suggests these roles are learnt.', True, 'If roles were biologically fixed they would be the same everywhere; variation suggests they are culturally shaped.'),
        ('Murdock claimed the nuclear family is universal.', True, 'He argued it was found in all 250 societies he studied, though later evidence challenged this.'),
    ],
    'ar': ([('Feral children usually lack language skills.', 'language must be learnt through interaction with others.'),
            ('Sociologists use cross-cultural comparison.', 'it shows whether behaviour is universal or varies between cultures.')],
           ['all societies have identical norms about marriage.', 'Genie learnt to speak fluently within a few months of being found.']),
    'scen': ['A newspaper in {city} reports the discovery of a seven-year-old child who had been kept alone in a room and had never learnt to speak.',
             'Two siblings separated at birth are raised in different countries; one becomes a confident public speaker and the other is shy and reserved.',
             'In one society women do most farming while men care for children; in another society near {city} the roles are reversed.'],
    'views': {'Functionalism': 'behaviour is shaped by socialisation into shared norms and values; without primary socialisation a person cannot take on social roles, showing the importance of nurture.',
              'Interactionism': 'the self develops through interaction with others; lack of interaction means the self, language and the ability to take the role of the other cannot develop (Mead).',
              'Liberal feminism': 'differences in male and female behaviour are mainly learnt through gender socialisation, not biology, so they can be changed (Oakley).'},
    'ctx': [('gender roles in two contrasting cultures', {'meaning', 'behaviour'}),
            ('how children who have experienced extreme neglect develop language', {'young', 'sensitive', 'hidden'})],
    'data': [dict(what='gender and childcare in different countries', pop='households', rows=['Country A', 'Country B', 'Country C'], cols=('Fathers', 'Mothers'),
                  base=[(10, 20), (25, 35), (35, 45)], delta=[(30, 50), (10, 25), (0, 12)], label='average daily minutes spent on childcare', unit=' min', uname='minutes', cmp=True,
                  leads=['Researchers compared time-use diaries from {n} households in three countries.', 'The table shows time-use data from {n} households in three countries, collected by {person}’s research team.'],
                  expl=['variation between countries suggests that childcare roles are shaped by culture and policy rather than biology', 'countries with paid parental leave for fathers may have more equal patterns',
                        'cultural norms about masculinity differ between societies'],
                  method='personal documents', claim='gender roles in childcare are determined by biology',
                  counter='Mothers do more childcare in every country, which some see as biological; but the large differences between countries point to cultural and policy influences.')],
    'essays': [('Explain two ways in which sociologists use evidence to support the nurture side of the nature versus nurture debate.', 'Feral children (Genie, Isabelle) show lack of socialisation prevents normal development; cross-cultural studies (Margaret Mead, gender roles) show variation; historical change in norms; twin studies showing environmental influence.',
                'human behaviour is the result of nurture rather than nature',
                'Feral children lack language and social skills; cross-cultural variation in gender and family roles; norms change over time; sociologists show socialisation and sanctions shape behaviour.',
                'Some behaviour has biological roots (reflexes, possibly some sex differences); evidence from feral children is limited and unethical to test; many argue nature and nurture interact; socio-biologists argue behaviour has evolutionary origins.')],
})

CHAPTERS[2] = [c2a, c2b, c2c]


# ============================================================== CHAPTER 3: Social control, conformity and resistance

V3 = {
    'Functionalism': 'social control maintains value consensus and social order; sanctions reinforce shared norms, and limited deviance can even be functional by clarifying boundaries (Durkheim, Parsons).',
    'Marxism': 'social control serves the ruling class: agencies such as the police, law and education protect capitalist interests and spread ideology, so conformity is produced by coercion and false class consciousness (Althusser).',
    'Interactionism': 'social control works through labelling and interaction: agents of control decide who is deviant, and labels can push people into deviant careers (Becker, Lemert).',
    'Radical feminism': 'women are controlled by patriarchy through informal controls such as the fear of violence, gossip and the double standard, as well as through male-dominated formal institutions (Heidensohn).',
}

c3a = T('Formal and informal social control and sanctions')
build(c3a, {
    'terms': [
        ('social control', 'the methods used to persuade or force individuals to conform to the norms and values of society', 'laws, school rules and family expectations'),
        ('formal social control', 'control based on written rules and laws, enforced by official agencies such as the police, courts and prisons', 'a fine for speeding'),
        ('informal social control', 'control based on the approval or disapproval of others, such as family, friends and the community', 'parents grounding a teenager or friends teasing someone'),
        ('positive sanction', 'a reward for conforming to norms', 'praise, a prize or a promotion'),
        ('negative sanction', 'a punishment for breaking norms', 'a detention, a fine or being ignored by friends'),
        ('agent of social control', 'a person or institution that enforces norms', 'police officers, teachers or parents'),
        ('surveillance', 'the monitoring of people’s behaviour, often using technology, to control it', 'CCTV cameras in a shopping centre'),
    ],
    'thinkers': [
        ('Foucault', 'modern societies control people mainly through surveillance and self-discipline rather than physical punishment', 'Postmodernism',
         'Foucault used the image of Bentham’s panopticon: people who believe they may be watched discipline themselves, so power works through surveillance.',
         'Critics argue Foucault exaggerates control and underplays resistance; surveillance can also protect people.'),
        ('Durkheim', 'punishment expresses society’s collective outrage and reinforces shared values', 'Functionalism',
         'Durkheim argued that punishing offenders reaffirms the collective conscience and strengthens social solidarity.',
         'Marxists argue punishment mainly protects the interests of the powerful.'),
        ('Heidensohn', 'women are controlled more than men in the home, in public and at work', 'Radical feminism',
         'Heidensohn argued that domestic responsibilities, fear of male violence and concern for reputation keep women under tighter informal control, which helps explain lower female crime rates.',
         'Critics argue control of women has weakened as they have gained more independence.'),
    ],
    'explain': [
        ('Explain the difference between formal and informal social control, using an example of each.', 'Formal control is official, based on written rules and enforced by agencies such as the police and courts (e.g. a prison sentence); informal control is unofficial, based on others’ reactions (e.g. a parent’s disapproval or peers’ teasing).', '1 mark each definition; 1 mark each example. [4]'),
        ('Explain why informal social control may be more effective than formal control.', 'People care about the approval of family and friends, whom they see daily; informal control works through internalised norms and shame, so people conform even when no official is watching; formal control relies on detection and punishment.', '1 mark: importance of significant others; 1 mark: internalisation/constant presence; 1 mark: comparison with formal. [3]'),
        ('Explain how new technology has changed social control.', 'CCTV, online tracking, facial recognition and social media allow constant surveillance; people self-regulate because they may be watched (Foucault); employers and governments can monitor behaviour; but technology can also be used to resist control.', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which schools exercise social control over pupils', ['through rules and sanctions such as detentions and exclusions', 'through rewards such as merits and prizes', 'through the hidden curriculum of routines and hierarchy', 'through surveillance in classrooms and corridors', 'through labelling of pupils']),
        ('sanction', 'sanctions', 'that a peer group might use to control its members', ['teasing or ridicule', 'exclusion from the group', 'approval and popularity for conforming', 'gossip that damages reputation']),
    ],
    'claims': [
        ('Positive sanctions are punishments.', False, 'Positive sanctions are rewards for conforming; negative sanctions are punishments.'),
        ('The police and courts are agents of formal social control.', True, 'They enforce written laws through official procedures.'),
        ('Social control only operates through the law.', False, 'Much control is informal, through family, peers, religion and the media.'),
    ],
    'ar': ([('Informal social control is often effective.', 'people value the approval of family and friends.'),
            ('CCTV can change people’s behaviour.', 'people who believe they are being watched tend to discipline themselves.')],
           ['informal social control is carried out by the courts.', 'negative sanctions are rewards for good behaviour.']),
    'scen': ['A shopping centre in {city} installs facial-recognition cameras and reports a fall in shoplifting.',
             'In a small village near {city}, a young woman says she would never stay out late because “everyone would talk about it”.',
             'A school in {city} introduces a system of merit points that pupils can exchange for rewards, alongside detentions for lateness.'],
    'ctx': [('the effects of CCTV on behaviour in public places', {'behaviour', 'large'}),
            ('informal social control of young women in a small community', {'meaning', 'sensitive'}),
            ('the use of rewards and punishments in schools', {'young', 'behaviour'})],
    'data': [dict(what='sanctions in schools', pop='secondary schools', rows=['Detentions', 'Merit awards', 'Exclusions'], cols=('2015', '2025'), n=[40, 60, 80, 100, 120],
                  base=[(55, 70), (40, 55), (5, 10)], delta=[(-15, -2), (5, 20), (-3, 2)], label='percentage of schools using this sanction “frequently”',
                  expl=['schools increasingly use positive sanctions because they believe rewards encourage conformity', 'Foucault might argue that control has become softer but more pervasive',
                        'policy changes may discourage exclusions'], flags={'large'},
                  method='questionnaire', claim='schools now rely more on positive than negative sanctions',
                  counter='Detentions are still widely used; schools may report the sanctions they think are approved; frequency of use does not show which sanctions are effective.')],
    'essays': [('Explain two ways in which agencies of informal social control encourage conformity.', 'Family: rewards, punishments and emotional ties; peer group: approval, teasing and exclusion; religion: moral codes and fear of sin; media: shaming and representations of acceptable behaviour; workplace: promotion or dismissal.',
                'informal social control is more important than formal social control in maintaining order',
                'Most people conform because of internalised norms and the approval of others; family and peers have daily influence; Heidensohn shows the power of informal control over women.',
                'Formal control deals with serious deviance that informal control fails to prevent; laws reinforce norms; surveillance and policing deter crime (Foucault); in large, anonymous cities informal controls are weaker.')],
}, V3)

c3b = T('Conformity, deviance and resistance to social control')
build(c3b, {
    'terms': [
        ('conformity', 'behaving in line with the norms and expectations of a group or society', 'wearing school uniform as required'),
        ('deviance', 'behaviour that breaks the norms of a group or society and is disapproved of', 'swearing at a religious ceremony'),
        ('crime', 'behaviour that breaks the criminal law and can be punished by the state', 'theft or assault'),
        ('resistance', 'actions that challenge or reject the norms, rules or power of dominant groups', 'a youth subculture that mocks mainstream values'),
        ('relativity of deviance', 'the idea that what counts as deviant varies between cultures, over time and between situations', 'drinking alcohol being acceptable in some societies but illegal in others'),
        ('deviant career', 'the process by which a person labelled deviant comes to adopt a deviant identity and lifestyle', 'a young offender who joins a gang after being rejected by others'),
        ('primary deviance', 'rule-breaking that has not been labelled and has little effect on a person’s self-identity', 'a pupil who occasionally copies homework without being caught'),
        ('secondary deviance', 'deviance that results from being labelled, as the person comes to see themselves as deviant', 'a teenager labelled a “thief” who begins to steal more'),
    ],
    'thinkers': [
        ('Lemert', 'societal reaction to primary deviance can lead to secondary deviance', 'Interactionism',
         'Lemert argued that most people commit some primary deviance; it is when others label them that a deviant self-concept and further deviance (secondary deviance) develop.',
         'Critics argue it ignores the reasons people commit deviance in the first place.'),
        ('Merton', 'deviance results from a strain between society’s cultural goals and the legitimate means of achieving them', 'Functionalism',
         'Merton’s strain theory identifies five adaptations: conformity, innovation, ritualism, retreatism and rebellion.',
         'Critics argue it assumes everyone shares the same goals and ignores group deviance.'),
        ('Hall and Jefferson', 'youth subcultures are a symbolic form of resistance to ruling-class hegemony', 'Neo-Marxism',
         'The Birmingham CCCS argued working-class youth styles (such as skinheads) resisted capitalism through style, but this resistance was “magical”, not changing their real situation.',
         'Critics argue the CCCS read too much political meaning into style; many young people join subcultures for fun.'),
        ('Becker', 'deviance is created when moral entrepreneurs make rules and apply them to particular people', 'Interactionism',
         'Becker argued powerful groups campaign for new rules and labels, so deviance reflects who has the power to define behaviour.',
         'Critics argue some acts, such as murder, are almost universally regarded as deviant.'),
    ],
    'explain': [
        ('Explain, using examples, why deviance is said to be relative.', 'What counts as deviant depends on culture (e.g. alcohol use), historical period (e.g. same-sex relationships decriminalised in many countries) and situation (e.g. killing in war vs. murder); so deviance is socially constructed, not fixed.', '1 mark: definition of relativity; 1 mark each of two examples from different dimensions (culture/time/situation). [3]'),
        ('Explain the difference between deviance and crime.', 'Deviance is any behaviour that breaks social norms and attracts disapproval; crime is behaviour that breaks the law. Not all deviance is criminal (e.g. rudeness) and not all crime is seen as deviant (e.g. minor speeding).', '1 mark each definition; 1 mark example showing they overlap but differ. [3]'),
        ('Explain two reasons why people conform to social norms.', 'Socialisation means people internalise norms and believe in them; fear of sanctions (formal and informal); desire for approval and belonging; rational calculation of costs and benefits; hegemony leads people to accept dominant ideas.', '2 marks each reason explained. [4]'),
    ],
    'why': [
        ('form', 'forms', 'of resistance to social control', ['youth subcultures that reject mainstream values through style', 'protest movements and strikes', 'everyday resistance such as rule-bending at work or school', 'online activism and campaigns', 'counter-cultures that reject society’s values']),
    ],
    'claims': [
        ('Deviance always involves breaking the law.', False, 'Deviance means breaking social norms; much deviance is not illegal (e.g. rudeness), and laws change over time.'),
        ('What is seen as deviant can change over time.', True, 'For example, attitudes to cohabitation, tattoos and same-sex relationships have changed in many societies.'),
        ('Merton’s “innovators” accept society’s goals but use illegitimate means to achieve them.', True, 'Innovation involves pursuing success through deviant or criminal means.'),
        ('Labelling theorists argue that labels have no effect on behaviour.', False, 'They argue labels can create a self-fulfilling prophecy and secondary deviance.'),
    ],
    'ar': ([('Deviance is relative.', 'norms vary between cultures, over time and between situations.'),
            ('Labelling can lead to secondary deviance.', 'a labelled person may adopt a deviant self-concept and be excluded from conventional roles.'),
            ('Some youth subcultures are seen as forms of resistance.', 'their style may express rejection of dominant values.')],
           ['all societies agree on what counts as deviant.', 'Merton argued that deviance is caused by too much social integration.']),
    'scen': ['A group of young people in {city} paint political murals on buildings without permission, saying they are “giving a voice to the community”.',
             '{person}, a 15-year-old in {city}, is caught shoplifting once; after a police caution, neighbours call {person} a “thief” and {person} begins to spend time with an older group who steal regularly.',
             'Office workers in {city} secretly take longer breaks than allowed and share jokes about their manager.'],
    'ctx': [('the meanings young people give to membership of a street gang', {'hidden', 'sensitive', 'meaning'}),
            ('how teenagers who have been cautioned by the police see themselves', {'young', 'sensitive', 'meaning'}),
            ('everyday resistance among workers in a call centre', {'behaviour', 'meaning'})],
    'data': [dict(what='attitudes to deviant behaviour', pop='adults', rows=['People aged 18-29', 'People aged 30-59', 'People aged 60+'], cols=('2000', '2025'),
                  base=[(20, 35), (35, 50), (50, 65)], delta=[(-15, -3), (-12, -2), (-8, 2)], label='percentage who see having a visible tattoo as “unacceptable” at work',
                  expl=['deviance is relative and changes over time as norms change', 'younger generations have been socialised into more tolerant norms',
                        'media and celebrity culture have normalised tattoos'],
                  method='questionnaire', claim='norms about deviance change over time',
                  counter='Older people still disapprove more, suggesting some continuity; workplace norms may differ from wider attitudes; questionnaires record stated attitudes, not actual behaviour by employers.')],
    'essays': [('Explain two reasons why some people resist social control.', 'Strain between goals and means (Merton’s rebellion and innovation); labelling and secondary deviance; subcultural resistance to hegemony (CCCS); political protest against injustice; rejection of norms seen as illegitimate.',
                'deviance is best understood as resistance to social control',
                'Neo-Marxists (Hall and Jefferson) see subcultures as resistance; protest movements challenge laws; feminists see women’s deviance as resisting patriarchal control; labelling theory shows rule-making reflects power.',
                'Much deviance is opportunistic or caused by strain, not resistance; functionalists see deviance as a result of poor socialisation or anomie; interactionists stress labels rather than resistance; many deviant acts harm others and are not political.')],
}, V3)

c3c = T('Theories of conformity: consensus, coercion and hegemony')
build(c3c, {
    'terms': [
        ('consensus', 'agreement among members of society about shared norms and values, so people conform willingly', 'most people obeying traffic laws because they believe they keep people safe'),
        ('coercion', 'the use or threat of force to make people conform', 'riot police breaking up a protest'),
        ('hegemony', 'the dominance of ruling-class ideas, which leads subordinate groups to consent to their own subordination', 'workers accepting that low wages are “just how things are”'),
        ('internalisation', 'the process by which people take norms and values into their own personality so that they conform without external pressure', 'feeling guilty after telling a lie'),
        ('repressive state apparatus', 'Althusser’s term for state institutions that control through force, such as the police, courts and army', 'the army being used to end a strike'),
        ('ideological state apparatus', 'Althusser’s term for institutions that control through ideas, such as education, religion and the media', 'school teaching that success is due to individual effort'),
        ('rational choice', 'the view that people conform or deviate after weighing up the likely costs and benefits', 'not shoplifting because the risk of being caught is high'),
    ],
    'thinkers': [
        ('Parsons', 'conformity results from the internalisation of shared values during socialisation', 'Functionalism',
         'Parsons argued that through socialisation norms become part of the personality, so most people want to do what society requires.',
         'Wrong criticised this as an “over-socialised conception of man” that ignores conflict and choice.'),
        ('Althusser', 'the state maintains capitalism through both repressive and ideological state apparatuses', 'Neo-Marxism',
         'Althusser argued that the RSA uses force when needed, while ISAs (education, media, religion, family) secure conformity by shaping beliefs.',
         'His approach is criticised as deterministic, leaving little room for resistance.'),
        ('Gramsci', 'the ruling class maintains power through hegemony, combining consent with coercion', 'Neo-Marxism',
         'Gramsci argued that ruling-class ideas become “common sense”, but hegemony is never complete, so the working class can develop counter-hegemony.',
         'Critics argue it is difficult to distinguish hegemony from genuine consensus.'),
        ('Hirschi', 'people conform because of strong social bonds to society', 'New Right',
         'Hirschi’s control theory identifies four bonds: attachment, commitment, involvement and belief; when bonds weaken, deviance becomes more likely.',
         'Critics argue it ignores structural causes of deviance such as poverty and inequality.'),
    ],
    'explain': [
        ('Explain the difference between consensus and coercion explanations of conformity.', 'Consensus theorists (functionalists) argue people conform because they share and have internalised the same values; coercion theorists (Marxists) argue conformity is forced on people by the powerful through the threat or use of force.', '1 mark each explanation with a perspective; 1 mark explicit contrast. [3]'),
        ('Explain what Gramsci meant by hegemony.', 'Hegemony is ideological and cultural leadership by the ruling class: its ideas come to seem like common sense, so subordinate classes consent to their own domination; coercion is used only when consent breaks down; hegemony is never complete.', '1 mark: ruling-class ideas as common sense; 1 mark: consent rather than force; 1 mark: incomplete/counter-hegemony. [3]'),
        ('Explain one strength and one weakness of the consensus explanation of conformity.', 'Strength: explains why most people conform most of the time without force, through socialisation. Weakness: it ignores conflict, inequality and power, and cannot explain resistance; Wrong called it “over-socialised”.', '2 marks for an explained strength; 2 marks for an explained weakness. [4]'),
    ],
    'why': [
        ('way', 'ways', 'in which, according to Marxists, the state uses coercion to maintain conformity', ['the police can arrest protesters and strikers', 'the courts and prisons punish those who break laws protecting property', 'the army can be used in times of crisis', 'surveillance discourages opposition']),
    ],
    'claims': [
        ('Gramsci believed the ruling class rules mainly through force.', False, 'He argued it rules mainly through hegemony (consent), using coercion only when needed.'),
        ('Functionalists explain conformity mainly in terms of value consensus.', True, 'They argue people conform because they have internalised shared norms and values.'),
        ('Althusser saw schools as ideological state apparatuses.', True, 'He argued education spreads ideology that reproduces capitalism.'),
        ('Hegemony means the same as coercion.', False, 'Hegemony refers to rule by consent through ideas; coercion is rule by force.'),
    ],
    'ar': ([('Gramsci argued hegemony is never complete.', 'workers have a dual consciousness shaped by both ruling-class ideas and their own experience of exploitation.'),
            ('Marxists see conformity as partly the result of coercion.', 'the state can use the police, courts and army to protect capitalist interests.'),
            ('Functionalists see most conformity as voluntary.', 'socialisation leads people to internalise shared values.')],
           ['Althusser argued that the media is a repressive state apparatus.', 'functionalists argue conformity is mainly produced by force.']),
    'scen': ['During a strike at a mine near {city}, police in riot gear arrest picket leaders, while newspapers describe the strikers as “selfish”.',
             'Most people in {city} pay their taxes on time, even though few are ever investigated by the tax authorities.',
             'A popular film shown in {city} celebrates a poor young man who becomes a billionaire through hard work and talent.'],
    'views': {'Functionalism': 'conformity results from value consensus: people have internalised shared norms through socialisation and conform willingly, with sanctions used only for the few who deviate (Parsons).',
              'Marxism': 'conformity results from coercion and ideology: the state’s repressive apparatus uses force when needed, and institutions spread ideas that legitimate capitalism (Althusser).',
              'Neo-Marxism': 'conformity results from hegemony: ruling-class ideas become “common sense” and win consent, though this is never complete and can be challenged (Gramsci).',
              'New Right': 'conformity depends on strong social bonds and effective sanctions; when attachment, commitment and belief weaken, deviance increases (Hirschi).'},
    'ctx': [('why most people obey the law', {'large', 'meaning'}),
            ('how the media presents strikes and protests', {'media', 'change'}),
            ('how far workers accept their employers’ values', {'meaning', 'behaviour'})],
    'data': [dict(what='reasons for obeying the law', pop='adults', rows=['“Because it is the right thing to do”', '“Because I might get caught”', '“Because others would disapprove”'], cols=('Under 30', '30 and over'),
                  base=[(40, 55), (20, 35), (10, 20)], delta=[(0, 15), (-12, 0), (-5, 3)], label='percentage giving this as their main reason for obeying the law', share=True, cmp=True, nocount=True,
                  expl=['the high share citing “the right thing to do” supports functionalist ideas of internalised values', 'those citing fear of being caught suggest coercion and deterrence also matter',
                        'neo-Marxists would argue that apparent agreement may reflect hegemony rather than genuine consensus'],
                  method='structured interview', claim='conformity is based mainly on consensus rather than coercion',
                  counter='A substantial share cite fear of punishment, supporting coercion explanations; people may give socially desirable answers in interviews; hegemony theory suggests “consent” itself is shaped by ideology.')],
    'essays': [('Explain two ways in which Marxists explain conformity.', 'Coercion through the repressive state apparatus (police, courts, army); ideology spread by ideological state apparatuses (education, media, religion – Althusser); hegemony and consent (Gramsci); economic dependence on wages.',
                'conformity in modern societies is based more on hegemony than on consensus',
                'Neo-Marxists show ruling-class ideas appear as common sense; media and education spread ideology; inequality persists without revolt; consent can be manufactured.',
                'Functionalists see genuine value consensus; many people conform from rational choice or social bonds (Hirschi); interactionists stress negotiated order; hegemony is hard to prove and may be confused with shared values.')],
}, V3)

CHAPTERS[3] = [c3a, c3b, c3c]


# ============================================================== CHAPTER 4: Social identity

V4 = {
    'Functionalism': 'identities based on shared roles help integrate individuals into society; socialisation prepares people for roles linked to gender, age and occupation, which contributes to social stability.',
    'Marxism': 'identities are shaped by class position under capitalism; other identities (such as consumer or national identity) may distract people from class inequality and exploitation.',
    'Radical feminism': 'identities are shaped by patriarchy: gender identities are socially constructed in ways that keep women subordinate to men.',
    'Interactionism': 'identity is created and negotiated in interaction; people respond to labels and manage the impressions they give, so identities are active and changeable (Goffman, Mead).',
    'Postmodernism': 'identities are fluid, fragmented and chosen; globalisation, the media and consumption allow people to construct hybrid, pick-and-mix identities rather than having them fixed by class, gender or ethnicity.',
}

c4a = T('Gender identity and the social construction of masculinities and femininities')
build(c4a, {
    'terms': [
        ('sex', 'the biological differences between males and females, such as chromosomes and reproductive organs', 'differences in hormones and anatomy'),
        ('gender', 'the socially constructed differences in behaviour, roles and identities expected of men and women', 'expectations that men should not show emotion'),
        ('hegemonic masculinity', 'the dominant, most valued form of masculinity in a society, associated with toughness, heterosexuality and power', 'a culture celebrating physically strong, competitive men'),
        ('emphasised femininity', 'a form of femininity organised around accommodating the interests and desires of men', 'pressure on women to be attractive and supportive'),
        ('crisis of masculinity', 'the idea that men are uncertain about their identity because traditional male roles such as breadwinner have declined', 'unemployed former industrial workers losing their sense of purpose'),
        ('gender role socialisation', 'the process of learning the behaviour and attitudes expected of one’s gender', 'boys being told “big boys don’t cry”'),
        ('new man', 'a form of masculinity in which men are caring, emotionally expressive and share domestic tasks', 'a father who takes parental leave'),
    ],
    'thinkers': [
        ('Connell', 'there is a hierarchy of masculinities in which hegemonic masculinity dominates subordinate and marginalised forms', 'Radical feminism',
         'Connell argued that hegemonic masculinity is culturally dominant, while gay and other forms are subordinated; most men are “complicit”, benefiting from patriarchy without fully embodying the ideal.',
         'Critics argue the concept is vague and hard to measure.'),
        ('Mac an Ghaill', 'changes in the economy have produced a crisis of masculinity among working-class young men', 'Interactionism',
         'Mac an Ghaill’s study found working-class boys who expected manual jobs that no longer existed responded with “macho” behaviour.',
         'Critics argue the crisis is exaggerated and that masculinities have always been changing.'),
        ('McRobbie', 'magazines for teenage girls promoted a narrow femininity based on romance, beauty and domesticity', 'Liberal feminism',
         'McRobbie’s analysis of Jackie magazine showed it reinforced traditional femininity; later she noted more confident, independent images of young women.',
         'Audiences interpret media actively and may reject such messages.'),
        ('Butler', 'gender is performative, created through repeated acts rather than fixed by biology', 'Postmodernism',
         'Butler argued that people “do” gender through repeated performances of masculine or feminine behaviour, so gender can be subverted and changed.',
         'Critics argue it underplays the material inequalities between men and women.'),
    ],
    'explain': [
        ('Explain the difference between sex and gender.', 'Sex refers to biological differences (chromosomes, hormones, anatomy); gender refers to socially constructed roles, behaviour and identities that are learnt and vary between cultures and over time.', '1 mark sex; 1 mark gender; 1 mark showing gender is learnt/variable. [3]'),
        ('Explain two ways in which gender identities have changed in many societies.', 'More women in paid work and higher education, with more independent femininities; men taking more domestic and childcare roles (“new man”); greater acceptance of diverse and non-binary identities; decline of traditional male breadwinner role (crisis of masculinity).', '2 marks for each explained change. [4]'),
        ('Explain how the media may contribute to the social construction of femininity.', 'Media representations stress beauty, slimness and romance (McRobbie); advertising links femininity to consumption; women are sexualised (the male gaze); social media creates pressure to perform idealised femininity; however there are now more diverse, empowered images.', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why some sociologists argue there is a “crisis of masculinity”', ['decline of manual industries removed traditional working-class male jobs', 'women’s greater economic independence has weakened the male breadwinner role', 'girls outperform boys in education in many countries', 'traditional masculine norms discourage men from seeking emotional support']),
    ],
    'claims': [
        ('Gender identities are fixed by biology.', False, 'Sociologists argue gender is socially constructed: it varies between cultures and changes over time.'),
        ('Connell argued that there are many forms of masculinity.', True, 'Connell described a hierarchy of hegemonic, complicit, subordinated and marginalised masculinities.'),
        ('Butler argued that gender is something people “do” through performance.', True, 'She argued gender is created through repeated acts, so it can be changed.'),
    ],
    'ar': ([('Gender roles vary between cultures.', 'gender is socially constructed rather than biologically determined.'),
            ('Some sociologists identify a crisis of masculinity.', 'the decline of traditional male jobs has undermined the breadwinner identity.')],
           ['sex refers to the socially constructed roles of men and women.', 'Connell argued that all men share a single form of masculinity.']),
    'scen': ['{man}, a father in {city}, takes six months of parental leave while his partner returns to work, and some of his friends joke that he is “not a real man”.',
             'A social media influencer in {city} posts daily videos about make-up, dieting and “being the perfect girlfriend”.',
             'After the closure of the steelworks near {city}, many young men say they feel “useless” and spend time in gangs.'],
    'ctx': [('how young men in {city} understand masculinity', {'meaning', 'sensitive'}),
            ('representations of femininity on social media', {'media', 'meaning', 'change'}),
            ('changes in gender roles over the last forty years', {'change', 'large'})],
    'data': [dict(what='attitudes to gender roles', pop='adults', rows=['Men', 'Women'], cols=('2000', '2025'),
                  base=[(35, 50), (25, 40)], delta=[(-20, -8), (-20, -10)], label='percentage agreeing that “a man’s job is to earn money; a woman’s job is to look after the home”',
                  expl=['the social construction of gender has changed as more women enter paid work', 'liberal feminists would point to equal opportunities and changing socialisation',
                        'media representations of gender have become more diverse'],
                  method='questionnaire', claim='traditional gender identities have declined',
                  counter='A significant minority still hold traditional views; attitudes may change faster than behaviour (women still do more domestic work); social desirability may lead people to under-report traditional views.')],
    'source': [dict(text='A researcher carried out group interviews with 48 boys aged 15-16 in two schools in {city}. Many said that being “hard” and “not caring about school” was important to be respected by friends. A few boys, however, said that they wanted to go to university and were teased as “geeks”.',
                    method='semi-structured interview', about='masculine identities among teenage boys', finds=['many boys valued being “hard” and not caring about school', 'boys who wanted to go to university were teased as “geeks”'],
                    persp='Interactionism', pview='The boys construct masculine identities through interaction and peer labels; “geek” labels act as informal sanctions enforcing a dominant (hegemonic) masculinity.',
                    claim='masculinity is socially constructed', pro='The source shows boys learning and enforcing norms of masculinity through peer interaction; Connell and Mac an Ghaill show masculinities vary and change.',
                    con='Some argue biological differences (e.g. hormones) influence behaviour; group interviews may encourage boys to exaggerate “hard” identities in front of peers; two schools may be untypical.', flags={'young', 'meaning'})],
    'essays': [('Explain two ways in which gender identity is socially constructed.', 'Primary socialisation (manipulation and canalisation – Oakley); education and the hidden curriculum; peer group policing of masculinity and femininity; media representations (McRobbie); performance of gender (Butler).',
                'traditional gender identities are disappearing in modern societies',
                'More women in paid work and higher education; “new man” and more involved fathers; diverse and fluid gender identities; postmodernists (Butler) see gender as performative and changeable.',
                'Women still do most domestic work; hegemonic masculinity persists (Connell); media continues stereotyping; gender pay gap and glass ceiling; change varies by class, ethnicity and country.')],
}, V4)

c4b = T('Ethnic identity, hybridity and globalisation')
build(c4b, {
    'terms': [
        ('ethnicity', 'a shared cultural identity based on factors such as language, religion, history, traditions and sense of common origin', 'a community sharing a language and religious festivals'),
        ('ethnic identity', 'a person’s sense of belonging to an ethnic group and the meaning they give to it', 'a young person identifying strongly as Tamil'),
        ('hybrid identity', 'an identity formed by combining elements from two or more cultures', 'a British-Asian young person mixing Bollywood and hip-hop'),
        ('diaspora', 'a population dispersed from its original homeland that keeps links to it', 'Indian communities living in East Africa and the Gulf'),
        ('cultural defence', 'the strengthening of ethnic identity and tradition as a response to hostility or racism from the wider society', 'a minority group emphasising its religion after experiencing discrimination'),
        ('racialisation', 'the process by which groups are defined and treated in terms of “race”', 'media portraying a migrant group as a threat'),
        ('globalisation', 'the growing interconnectedness of societies across the world through trade, migration, media and communication', 'people following the same online trends in many countries'),
    ],
    'thinkers': [
        ('Hall', 'identities in the modern world are increasingly hybrid and constantly changing', 'Postmodernism',
         'Stuart Hall argued ethnic identities are not fixed essences but are produced through history, culture and representation, and that globalisation creates new hybrid identities.',
         'Critics argue many people still have strong, traditional ethnic identities.'),
        ('Modood', 'ethnic minority identities in Britain involve both continuity with tradition and adaptation to the wider society', 'Interactionism',
         'Modood’s surveys found that many second-generation minorities kept aspects of religion and culture while also identifying as British.',
         'Survey methods may not capture how identities shift in different contexts.'),
        ('Back', 'young people in multi-ethnic neighbourhoods create new “neighbourhood nationalisms” that mix cultures', 'Postmodernism',
         'Back’s ethnography of two London estates found young people combining black, white and Asian cultural styles into new identities.',
         'His study was small-scale and may not be typical of other areas.'),
        ('Johal', 'British-Asian young people have dual identities and can “code-switch” between cultures', 'Interactionism',
         'Johal found that young British-Asians adopted “white masks” at school or work and Asian identity at home, using hybrid identities strategically.',
         'Critics argue such switching may cause tension and not all young people experience identity this way.'),
    ],
    'explain': [
        ('Explain what is meant by a hybrid identity, using an example.', 'A hybrid identity combines elements of two or more cultures to create something new, often among the children of migrants; for example, a young person in a diaspora community mixing their parents’ language and religion with global youth culture.', '1 mark definition; 1 mark link to migration/globalisation; 1 mark example. [3]'),
        ('Explain two ways in which globalisation may influence ethnic identity.', 'Migration creates diasporas and hybrid identities; global media spreads cultural products that mix with local cultures (glocalisation); global communication keeps diasporas linked to homelands; it may also provoke cultural defence and stronger traditional identities.', '2 marks for each explained way. [4]'),
        ('Explain why some minority ethnic groups may strengthen their ethnic identity.', 'Cultural defence against racism and exclusion; maintaining links to homeland and family; religion and community organisations providing support; pride and resistance to negative stereotypes.', '1 mark each explained reason up to 3. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which ethnic identity can be expressed', ['through language and dialect', 'through religion and religious festivals', 'through food and dress', 'through music and media', 'through family and marriage customs']),
    ],
    'claims': [
        ('Ethnicity is the same as nationality.', False, 'Ethnicity is a shared cultural identity; people of many ethnicities can share the same nationality.'),
        ('Hybrid identities combine elements of different cultures.', True, 'They are common among the children of migrants and in global cities.'),
        ('Globalisation always weakens ethnic identities.', False, 'It can also strengthen them, for example through cultural defence or diaspora links via the internet.'),
    ],
    'ar': ([('Hybrid identities are common in global cities.', 'migration and global media bring different cultures into close contact.'),
            ('Some minorities strengthen their ethnic identity.', 'cultural defence can be a response to racism and exclusion.')],
           ['ethnic identities are fixed at birth and never change.', 'Stuart Hall argued that globalisation has ended cultural mixing.']),
    'scen': ['{person}, whose parents migrated to {city} from another continent, speaks one language at home and another with friends, and mixes music from both cultures.',
             'After a rise in racist attacks in {city}, young people from a minority community begin attending their place of worship more often and wearing traditional dress.',
             'A food festival in {city} serves “fusion” dishes that combine recipes from several migrant communities.'],
    'ctx': [('how second-generation migrants in {city} see their identity', {'meaning', 'sensitive'}),
            ('the experiences of minority ethnic young people in schools', {'young', 'meaning', 'sensitive'}),
            ('changes in the ethnic composition of a large city', {'large', 'change'})],
    'data': [dict(what='identity among second-generation migrants', pop='young adults', rows=['Mainly the country they live in', 'Mainly their parents’ country of origin', 'Both equally'], cols=('2005', '2025'),
                  base=[(30, 40), (30, 40), (20, 30)], delta=[(0, 8), (-15, -5), (5, 15)], label='percentage describing their identity as', dist=True,
                  expl=['postmodernists and Hall would see the rise in “both equally” as evidence of hybrid identities', 'globalisation and social media allow young people to keep links with their parents’ culture while belonging locally',
                        'longer settlement means more young people identify with the country they live in'],
                  method='questionnaire', claim='young people from migrant families increasingly have hybrid identities',
                  counter='Many still identify mainly with one culture; identity may change depending on context (Johal), which fixed survey categories cannot capture; experiences differ between ethnic groups.')],
    'essays': [('Explain two reasons why ethnic identities may be changing.', 'Globalisation and migration creating diasporas; hybridity among second and third generations (Hall, Back); global media; intermarriage; decline of traditional religious practice; cultural defence in response to racism.',
                'ethnic identities are becoming more hybrid in a globalised world',
                'Hall and Back show mixing of cultures; global media and migration; code-switching (Johal); second generations combine cultures; glocalisation.',
                'Many minorities keep strong traditional identities (Modood); cultural defence strengthens boundaries; racism maintains ethnic divisions; hybridity may apply mainly to young people in cities.')],
}, V4)

c4c = T('Age identity: childhood, youth and old age as social constructs')
build(c4c, {
    'terms': [
        ('social construction of age', 'the idea that the meanings and expectations attached to age groups are created by society rather than fixed by biology', 'the age at which people are seen as adults varying between societies'),
        ('childhood', 'a stage of life seen in many modern societies as separate from adulthood and requiring protection', 'laws banning child labour and making schooling compulsory'),
        ('youth', 'the life stage between childhood and adulthood, often associated with independence, peer groups and youth culture', 'teenagers developing distinctive fashion and music tastes'),
        ('ageism', 'prejudice or discrimination against people because of their age', 'employers refusing to hire workers over 55'),
        ('rite of passage', 'a ceremony that marks the transition from one life stage to another', 'a coming-of-age ceremony or a graduation'),
        ('dependency', 'the condition of relying on others for support, often associated with childhood and old age', 'retired people relying on pensions or family care'),
        ('third age', 'the period after retirement when many older people remain healthy and active', 'retired people travelling or studying'),
    ],
    'thinkers': [
        ('Ariès', 'childhood as a separate stage of life did not exist in medieval Europe', 'Interactionism',
         'Ariès used paintings and documents to argue that medieval children were treated as “mini-adults” once they could survive without constant care; modern childhood emerged from the 13th century onwards.',
         'Pollock argued that medieval societies did have a concept of childhood, just a different one.'),
        ('Postman', 'childhood is disappearing because television and new media give children access to adult information', 'Interactionism',
         'Postman argued that print culture created a barrier between adults and children through literacy; television removes this “information hierarchy”.',
         'Critics argue childhood is protected more than ever through laws and schooling.'),
        ('Pilcher', 'modern childhood is defined by separateness from adulthood', 'Functionalism',
         'Pilcher argued that modern childhood is a distinct life stage, with laws, dress, products and services designed specifically for children.',
         'The degree of separateness varies by class, ethnicity and country.'),
        ('Featherstone and Hepworth', 'later life is increasingly shaped by consumer culture and individual choice', 'Postmodernism',
         'They argued that older people now use consumption to construct active, youthful identities, blurring traditional age boundaries.',
         'Poorer pensioners may not have the resources to make such choices.'),
    ],
    'explain': [
        ('Explain why childhood is said to be socially constructed.', 'The meaning and length of childhood vary between cultures and historical periods (e.g. children working in some societies; Ariès on medieval Europe); laws on school leaving, marriage and work define childhood differently in different societies.', '1 mark: meaning; 1 mark cross-cultural example; 1 mark historical example. [3]'),
        ('Explain two ways in which old age is socially constructed.', 'Retirement age and pensions are set by the state; the status of the elderly differs between cultures (respected elders vs. burden); media stereotypes; consumer culture and the “third age”.', '2 marks for each explained way. [4]'),
        ('Explain what is meant by youth culture, using an example.', 'Youth culture is the distinctive styles, values and activities of young people, often expressed through music, fashion, language and media, for example online gaming communities or street dance styles.', '1 mark definition; 1 mark developed example. [2]'),
    ],
    'why': [
        ('reason', 'reasons', 'why the position of children has changed in modern societies', ['laws banning child labour made children economically dependent', 'compulsory schooling separated children from adults', 'lower infant mortality led parents to invest more emotionally in fewer children', 'smaller families became more child-centred', 'children’s rights legislation']),
        ('example', 'examples', 'of ageism in modern societies', ['employers discriminating against older job applicants', 'media stereotypes of older people as frail or out of touch', 'young people being stereotyped as troublemakers', 'lack of political voice for children']),
    ],
    'claims': [
        ('Childhood is experienced in the same way in every society.', False, 'Childhood varies between cultures, historical periods and social classes.'),
        ('Ariès argued that the modern idea of childhood developed over several centuries.', True, 'He argued medieval children were treated as small adults and modern childhood emerged gradually.'),
        ('Old age is defined only by biology.', False, 'Retirement age, pensions and cultural status show that old age is also socially constructed.'),
    ],
    'ar': ([('Childhood varies between societies.', 'childhood is socially constructed.'),
            ('Postman argued that childhood is disappearing.', 'television and new media give children access to adult information.')],
           ['Ariès argued that medieval children were kept separate from adult life.', 'retirement age is the same in every country.']),
    'scen': ['In one village near {city}, children of eight help in the fields and look after younger siblings; in the city itself, children of the same age are not allowed to walk to school alone.',
             'An advertising campaign in {city} shows people in their seventies running marathons, travelling and using dating apps.',
             'A 12-year-old in {city} has a smartphone, follows adult celebrities online and wears clothes similar to those of her older sister.'],
    'ctx': [('how children in {city} experience childhood today', {'young', 'meaning', 'behaviour'}),
            ('experiences of ageism among older workers', {'meaning', 'sensitive'}),
            ('changes in the way childhood has been represented in the past', {'past', 'change', 'meaning'})],
    'data': [dict(what='perceptions of when adulthood begins', pop='adults', rows=['People aged 18-29', 'People aged 30-59', 'People aged 60+'], cols=('1995', '2025'),
                  base=[(35, 50), (45, 60), (55, 70)], delta=[(-15, -5), (-12, -2), (-8, 2)], label='percentage agreeing that “a person is an adult by the age of 21”',
                  expl=['longer education and later home-leaving have extended youth', 'the transition to adulthood is now gradual and individualised rather than marked by clear rites of passage',
                        'economic insecurity delays independence such as owning a home'],
                  method='questionnaire', claim='the boundaries between age stages are becoming blurred',
                  counter='Legal ages for voting, marriage and work still mark clear boundaries; views vary between age groups; experiences differ by class and country.')],
    'essays': [('Explain two ways in which childhood has changed in modern societies.', 'Laws on child labour and compulsory schooling; children’s rights; child-centred families; separateness (Pilcher); media and consumption (Postman’s disappearing childhood).',
                'childhood is becoming shorter in modern societies',
                'Postman: media remove the information barrier; children consume adult fashion and products; earlier sexualisation; access to the internet.',
                'Children are more protected and supervised than ever; longer schooling extends dependency; laws define childhood clearly; the march of progress view (Aries) sees improvement; experiences differ by class and country.')],
}, V4)

c4d = T('Social class identity and changes in class identity')
build(c4d, {
    'terms': [
        ('social class', 'a group of people who share a similar economic position, such as occupation, income and wealth', 'manual workers or professionals'),
        ('class identity', 'a person’s sense of belonging to a particular social class', 'someone proudly describing themselves as working class'),
        ('class consciousness', 'awareness of one’s class position and of shared interests with others in the same class', 'workers uniting in a trade union'),
        ('social mobility', 'movement of individuals or groups between social classes', 'the child of a factory worker becoming a lawyer'),
        ('embourgeoisement', 'the idea that affluent manual workers adopt middle-class lifestyles and values', 'well-paid factory workers buying their own homes'),
        ('cultural capital', 'the knowledge, tastes and skills, often middle-class, that give advantages in education and society', 'familiarity with museums, books and classical music'),
        ('underclass', 'a group said to be below the working class, dependent on welfare and excluded from mainstream society', 'long-term unemployed people in deprived areas'),
    ],
    'thinkers': [
        ('Bourdieu', 'class is reproduced through economic, cultural and social capital', 'Neo-Marxism',
         'Bourdieu argued that middle-class families pass on cultural capital (tastes, knowledge, language) that gives their children advantages, so class identity is reflected in “habitus”.',
         'Critics argue cultural capital is hard to measure and working-class cultures are undervalued rather than lacking.'),
        ('Pakulski and Waters', 'class is “dead” as a source of identity in postmodern societies', 'Postmodernism',
         'They argued that identities are now based on consumption and status rather than production, so class identity has declined.',
         'Evidence shows class still strongly shapes life chances such as health, education and income.'),
        ('Savage', 'traditional class categories should be replaced by a model of seven classes based on economic, social and cultural capital', 'Weberian theory',
         'The Great British Class Survey (Savage et al.) identified groups such as the “elite” and the “precariat”, showing class is still important but more complex.',
         'The online survey had a self-selecting sample, so it over-represented the middle class.'),
        ('Goldthorpe and Lockwood', 'affluent manual workers had not become middle class but had adopted an instrumental, privatised lifestyle', 'Weberian theory',
         'Their Luton study rejected embourgeoisement: affluent workers kept working-class attitudes to work and politics but focused on home and family.',
         'The study was limited to one town in the 1960s.'),
    ],
    'explain': [
        ('Explain two reasons why class identity may have weakened in many societies.', 'Decline of manual industry and traditional working-class communities; rise of consumer culture and lifestyle-based identity (Pakulski and Waters); increased social mobility and growth of the middle class; other identities (gender, ethnicity, sexuality) have become more important.', '2 marks for each explained reason. [4]'),
        ('Explain what Bourdieu meant by cultural capital.', 'Cultural capital is the knowledge, attitudes, language and tastes valued by the education system and passed on by (mainly middle-class) families; it gives children advantages and helps reproduce class inequality.', '1 mark definition; 1 mark how it is passed on; 1 mark link to advantage/reproduction. [3]'),
        ('Explain the difference between class position and class identity.', 'Class position is a person’s objective economic situation (occupation, income, wealth); class identity is their subjective sense of belonging to a class. A person may be objectively working class but not identify as such.', '1 mark each concept; 1 mark contrast/example. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which social class continues to affect people’s life chances', ['educational achievement varies by class', 'life expectancy and health differ between classes', 'wealth and income inequality', 'access to elite occupations depends on class background', 'housing and neighbourhood']),
    ],
    'claims': [
        ('Postmodernists argue that class is the main source of identity today.', False, 'They argue identity is based on consumption and choice; Pakulski and Waters claimed class is “dead”.'),
        ('Social class still affects life chances such as health and education.', True, 'Evidence shows clear class differences in attainment, life expectancy and income.'),
        ('Goldthorpe and Lockwood found that affluent workers had become middle class.', False, 'They rejected embourgeoisement, finding affluent workers kept working-class attitudes.'),
    ],
    'ar': ([('Class identity has weakened for many people.', 'the decline of manual industries has broken up traditional working-class communities.'),
            ('Bourdieu argued that class is reproduced through culture.', 'middle-class families pass on cultural capital valued by schools.')],
           ['Marx argued that class conflict would disappear under capitalism.', 'Savage found that class no longer affects people’s life chances.']),
    'scen': ['In a former mining town near {city}, older residents say they are “proud to be working class”, but their grandchildren describe themselves through music, fashion and online communities.',
             '{person}, the first person in the family to attend university in {city}, says that they feel “out of place” among wealthier students who talk about holidays abroad and classical concerts.',
             'A survey in {city} finds that many people in routine office jobs on low pay describe themselves as “middle class”.'],
    'ctx': [('how first-generation university students experience class', {'meaning', 'sensitive'}),
            ('changes in class identity in a former industrial town', {'change', 'meaning', 'past'}),
            ('the relationship between social class and life chances', {'large', 'change'})],
    'data': [dict(what='class identity', pop='adults', rows=['Working class', 'Middle class', 'No class / don’t know'], cols=('1990', '2025'),
                  base=[(50, 60), (30, 38), (5, 10)], delta=[(-15, -5), (0, 8), (3, 10)], label='percentage describing themselves as', dist=True,
                  expl=['the decline of manual work has reduced traditional working-class identity', 'postmodernists argue identities are now based on consumption and lifestyle',
                        'occupational change has expanded the middle class'],
                  method='questionnaire', claim='social class is no longer important to people’s identity',
                  counter='A large share still describe themselves in class terms; class still shapes life chances (Savage); subjective identity is not the same as objective class position.')],
    'essays': [('Explain two ways in which social class identity has changed.', 'Decline of traditional working-class identity with deindustrialisation; growth of the middle class and white-collar work; consumption-based identities (Pakulski and Waters); new classes such as the precariat (Savage); fragmentation of class identity.',
                'social class is no longer an important source of identity',
                'Postmodernists (Pakulski and Waters) argue identity is based on consumption; decline of class-based communities and trade unions; other identities such as gender, ethnicity and sexuality matter more.',
                'Class still shapes life chances and cultural tastes (Bourdieu, Savage); many people still identify with a class; Marxists argue class position matters regardless of identity; the precariat shows new class divisions.')],
}, V4)

CHAPTERS[4] = [c4a, c4b, c4c, c4d]


# ============================================================== CHAPTER 5: Research approaches, theory and methods

V5 = {
    'Positivism': 'sociology should study society scientifically, using quantitative, reliable methods such as questionnaires and official statistics to discover social facts, correlations and causes; the researcher should remain objective and detached (Comte, Durkheim).',
    'Interpretivism': 'social reality is constructed through the meanings people give to their actions, so researchers must use qualitative methods such as unstructured interviews and participant observation to achieve verstehen and valid data (Weber).',
    'Feminism': 'research has often ignored women’s experiences; feminist researchers prefer non-hierarchical, qualitative methods that give women a voice and take account of power relationships in research (Oakley).',
}


def classify(t, cases, labels, q, C='C1', D=(1, 2, 3), name='classify'):
    """cases: (description with {person}/{city}/{n}, label, reason). MCQ: which label applies?"""
    def fn(r, D_):
        desc, lab, why = r.choice(cases)
        d = dict(ctxd(r), n=r.choice([20, 30, 40, 50, 60, 80, 100, 120, 150, 200, 250, 300, 400, 500]))
        stem = fill(desc, d) + ' ' + q
        opts, a = mcq(r, lab, [x for x in labels if x != lab])
        return {'stem': stem, 'options': opts, 'answer': a, 'key': f'{lab}: {why} [1]', 'marks': 1}
    _reg(t, C, D, 'mcq', fn, name)


c5a = T('Positivism and interpretivism')
build(c5a, {
    'research': True,
    'terms': [
        ('positivism', 'the view that sociology should use the methods of the natural sciences to discover objective, measurable social facts and laws', 'Durkheim using suicide statistics to find correlations'),
        ('interpretivism', 'the view that sociologists must understand the subjective meanings people give to their actions, using qualitative methods', 'a researcher joining a gang to understand members’ motives'),
        ('social facts', 'Durkheim’s term for social phenomena that exist outside individuals and constrain their behaviour', 'suicide rates, laws and religious norms'),
        ('verstehen', 'empathetic understanding of social action from the actor’s point of view', 'seeing the world through the eyes of a homeless person'),
        ('quantitative data', 'data in numerical form that can be counted and analysed statistically', 'the percentage of respondents who agree with a statement'),
        ('qualitative data', 'data in the form of words, images or detailed descriptions that convey meanings and experiences', 'a transcript of an in-depth interview'),
        ('objectivity', 'studying society without letting personal values or bias influence the research', 'using a standardised questionnaire to avoid influencing answers'),
        ('value freedom', 'the idea that researchers should keep their own values out of the research process', 'reporting findings even when they contradict the researcher’s beliefs'),
    ],
    'thinkers': [
        ('Comte', 'sociology should be a “positive science” that discovers the laws governing society', 'Positivism',
         'Comte, who coined the term sociology, believed scientific methods could find laws of social development and be used to improve society.',
         'Interpretivists argue humans have consciousness and act on meanings, so they cannot be studied like objects in nature.'),
        ('Durkheim', 'suicide rates are social facts that can be explained by levels of social integration and regulation', 'Positivism',
         'Durkheim used official statistics comparatively to show suicide rates varied with integration and regulation (egoistic, altruistic, anomic, fatalistic suicide).',
         'Atkinson and Douglas argue suicide statistics are socially constructed by coroners’ judgements.'),
        ('Weber', 'sociologists must interpret the meanings behind social action through verstehen', 'Interpretivism',
         'Weber argued social action must be understood at the level of meaning as well as cause, but he also valued objective, causal explanation.',
         'Positivists argue meanings cannot be observed or measured reliably.'),
        ('Douglas', 'official suicide statistics cannot be taken at face value because they depend on how deaths are interpreted', 'Interpretivism',
         'Douglas argued researchers should study the meanings of suicide through qualitative sources such as diaries and suicide notes.',
         'Critics argue this replaces coroners’ interpretations with the sociologist’s own.'),
    ],
    'explain': [
        ('Explain why positivists prefer quantitative methods.', 'They aim to study society scientifically and objectively; quantitative methods are standardised and reliable, allow large representative samples, and produce statistics that reveal correlations and causes (social facts).', '1 mark each developed reason up to 3. [3]'),
        ('Explain two differences between positivist and interpretivist approaches to research.', 'View of society: external social facts vs. socially constructed meanings; methods: quantitative vs. qualitative; aims: causes and laws vs. understanding (verstehen); key concerns: reliability and representativeness vs. validity; researcher role: detached vs. involved.', '2 marks each explained difference. [4]'),
        ('Explain why interpretivists value validity more than reliability.', 'They believe the aim of research is to understand meanings, so data must give a true picture of people’s experiences (validity); standardised methods may be reliable but impose the researcher’s categories and miss meanings.', '1 mark meaning of validity; 1 mark interpretivist aim; 1 mark limitation of reliable but invalid methods. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of the positivist approach to sociology', ['people act on meanings and cannot be studied like objects in nature', 'quantitative data lacks validity and depth', 'official statistics are social constructions', 'researchers cannot be fully value-free', 'closed questions impose the researcher’s categories']),
        ('criticism', 'criticisms', 'of the interpretivist approach to sociology', ['small samples are unrepresentative', 'qualitative studies are hard to repeat, so are unreliable', 'the researcher’s interpretation may be biased', 'it neglects wider social structures']),
    ],
    'claims': [
        ('Positivists believe sociology should be scientific.', True, 'They believe society can be studied objectively using the methods of the natural sciences.'),
        ('Interpretivists prefer large-scale questionnaires because they produce valid data.', False, 'Interpretivists prefer qualitative methods such as unstructured interviews because they give valid, meaningful data.'),
        ('Durkheim’s study of suicide is an example of interpretivist research.', False, 'It is a classic positivist study using official statistics to find social causes.'),
        ('Weber combined interest in meanings with causal explanation.', True, 'He argued for verstehen but also wanted to explain social action causally.'),
    ],
    'ar': ([('Positivists prefer quantitative methods.', 'they want reliable data that can reveal correlations and causes.'),
            ('Interpretivists prefer qualitative methods.', 'they aim to understand the meanings people give to their actions.'),
            ('Interpretivists criticise the use of official statistics.', 'they see statistics as social constructions produced by the decisions of officials.')],
           ['positivists argue that sociology should not aim to be scientific.', 'interpretivists value reliability above validity.']),
    'scen': ['{person}, a researcher in {city}, sends a questionnaire with 30 closed questions to 2,000 households to find out whether income affects voting.',
             'A sociologist lives with a group of street children in {city} for nine months to understand how they see their own lives.',
             'A study uses official statistics from 40 countries to compare suicide rates with levels of unemployment.'],
    'ctx': [('why some young people leave school early', {'meaning', 'large', 'young'}),
            ('the experiences of homeless people in {city}', {'hidden', 'meaning', 'sensitive'}),
            ('the relationship between unemployment and crime rates', {'large', 'change'})],
    'data': [dict(what='methods used in published sociological research', pop='journal articles', rows=['Mainly quantitative methods', 'Mainly qualitative methods', 'Mixed methods'], cols=('2000', '2025'), n=[200, 300, 400, 500, 600],
                  base=[(45, 55), (30, 40), (8, 15)], delta=[(-12, -2), (-5, 5), (5, 15)], label='percentage of articles using', dist=True, nocount=True,
                  leads=['A researcher analysed {n} journal articles published in sociology journals and recorded the main methods used.', '{person} reviewed {n} sociology journal articles to see which research methods they used.'],
                  expl=['many sociologists now combine positivist and interpretivist approaches (methodological pluralism)', 'mixed methods allow triangulation, improving validity and reliability',
                        'funding bodies may prefer studies that produce both statistics and in-depth understanding'],
                  method='content analysis', claim='the debate between positivism and interpretivism is less important today',
                  counter='Most studies still rely mainly on one approach; theoretical preferences still shape choice of method; a sample of journals may not represent all research.')],
    'essays': [('Explain two reasons why positivists prefer quantitative research methods.', 'Aim of scientific study of social facts; reliability through standardisation; representativeness and generalisation; testing hypotheses and finding correlations/causes; objectivity and detachment.',
                'sociology can and should be a science',
                'Positivists (Comte, Durkheim) show patterns and correlations can be measured; quantitative methods are reliable and representative; scientific findings can inform policy.',
                'Interpretivists argue humans act on meanings and need verstehen; official statistics are socially constructed; realists argue even natural sciences study unobservable structures; values affect research choices; postmodernists reject the idea of objective truth.')],
}, V5)
classify(c5a, [
    ('{person} uses official statistics from 30 countries to test whether divorce rates are linked to women’s employment.', 'Positivism', 'quantitative data used to find correlations between social facts.'),
    ('{person} spends a year living with a religious group in {city} to understand how members see the world.', 'Interpretivism', 'participant observation used to gain verstehen.'),
    ('A researcher sends a pre-coded questionnaire to {n} randomly selected households in {city} to measure the division of housework.', 'Positivism', 'standardised, quantitative, reliable method on a large sample.'),
    ('{person} conducts long, unstructured interviews with 12 nurses in {city} about the emotional demands of their work.', 'Interpretivism', 'qualitative method focused on meanings and experiences.'),
    ('A sociologist analyses diaries written by migrants arriving in {city} to understand their feelings about their new lives.', 'Interpretivism', 'personal documents used to understand subjective meanings.'),
    ('A research team uses a structured interview schedule with {n} respondents in {city} to compare voting by social class.', 'Positivism', 'standardised method producing quantitative, comparable data.'),
], ['Positivism', 'Interpretivism', 'Functionalism', 'Postmodernism'], 'Which methodological approach does this research best reflect?')

c5b = T('Validity, reliability, representativeness and generalisability')
build(c5b, {
    'research': True,
    'terms': [
        ('validity', 'the extent to which research gives a true and accurate picture of what it claims to measure', 'an in-depth interview revealing a person’s real feelings'),
        ('reliability', 'the extent to which research produces the same results when repeated by another researcher using the same method', 'a standardised questionnaire giving similar results when repeated'),
        ('representativeness', 'the extent to which a sample has the same characteristics as the wider population it is drawn from', 'a sample with the same proportions of age groups as the population'),
        ('generalisability', 'the extent to which findings from a sample can be applied to the wider population', 'concluding that a pattern found in a national survey applies to the whole country'),
        ('research population', 'the whole group that a researcher is interested in studying', 'all secondary school teachers in a country'),
        ('sampling frame', 'a list of all members of the research population from which a sample can be drawn', 'a school register or electoral roll'),
        ('Hawthorne effect', 'the tendency of people to change their behaviour because they know they are being studied', 'workers working harder because researchers are watching'),
        ('interviewer bias', 'the influence of the interviewer’s characteristics or behaviour on the answers given', 'respondents giving answers they think the interviewer wants'),
    ],
    'thinkers': [
        ('Mayo', 'workers changed their behaviour simply because they knew they were being studied', 'Positivism',
         'Mayo’s Hawthorne studies found productivity rose whatever lighting changes were made, because workers responded to the attention of researchers – the Hawthorne effect.',
         'Later re-analysis suggested other factors such as fear of job loss may also have affected productivity.'),
        ('Becker', 'researchers inevitably take sides, so the question is “whose side are we on?”', 'Interactionism',
         'Becker argued value freedom is impossible: sociologists should openly side with the “underdog” whose voice is rarely heard.',
         'Gouldner argued Becker himself still took a limited, liberal side and ignored structural power.'),
        ('Oakley', 'interviews should be non-hierarchical so that respondents are treated as equals', 'Liberal feminism',
         'Oakley argued that a sympathetic, two-way interview with women produces more valid data than a detached, “masculine” interview.',
         'Critics argue that this involvement may bias the data and reduce reliability.'),
    ],
    'explain': [
        ('Explain the difference between validity and reliability, using an example of a method that is strong in each.', 'Validity: research gives a true picture (e.g. unstructured interviews or participant observation reveal meanings); reliability: research can be repeated with the same results (e.g. standardised questionnaires).', '1 mark each definition; 1 mark each appropriate method example. [4]'),
        ('Explain why a sample may not be representative.', 'The sampling frame may be incomplete; non-random selection such as opportunity sampling; low response rates mean only some types of people reply; the sample may be too small; certain groups are hard to reach.', '1 mark each developed reason up to 3. [3]'),
        ('Explain why research using small samples may be difficult to generalise.', 'A small sample is unlikely to reflect the range of characteristics in the population, so a few unusual cases can distort findings; results may apply only to that group.', '1 mark: small sample unlikely to be representative; 1 mark: unusual cases distort; 1 mark: limits generalisation. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which researchers can improve the validity of their data', ['build rapport so respondents give honest answers', 'use open questions so respondents use their own words', 'triangulate with other methods', 'observe behaviour in natural settings', 'avoid leading questions']),
        ('way', 'ways', 'in which researchers can improve the reliability of their research', ['use standardised questions and procedures', 'use pre-coded answers', 'carry out a pilot study', 'record the method clearly so others can repeat it', 'train interviewers to behave consistently']),
    ],
    'claims': [
        ('A reliable method always produces valid data.', False, 'A method can give consistent results that are still inaccurate, e.g. a questionnaire where people give socially desirable answers.'),
        ('Covert participant observation is usually high in validity but low in reliability.', True, 'It shows natural behaviour but cannot be repeated exactly.'),
        ('The larger the sample, the more representative it must be.', False, 'Size helps, but a large biased sample (e.g. self-selecting) can still be unrepresentative.'),
        ('A sampling frame is a list of the research population.', True, 'It is used to select a sample, e.g. an electoral roll or school register.'),
    ],
    'ar': ([('Standardised questionnaires are usually reliable.', 'every respondent answers the same questions in the same way, so the study can be repeated.'),
            ('Participant observation is often said to have high validity.', 'it allows the researcher to see behaviour in its natural setting.'),
            ('Low response rates can reduce representativeness.', 'those who reply may differ from those who do not.')],
           ['validity means that a study can be repeated with the same results.', 'a self-selecting sample is always representative.']),
    'scen': ['{person} studies 15 pupils from one school in {city} and claims that the findings apply to all pupils in the country.',
             'A survey on household income in {city} uses an online questionnaire; 42% of those invited reply, mostly older and better-off residents.',
             'Two researchers use the same structured interview schedule in {city} and obtain very similar results.'],
    'views': {'Positivism': 'research should be reliable and representative so that findings can be generalised and tested; standardised, large-scale methods such as questionnaires achieve this.',
              'Interpretivism': 'validity matters most: the aim is to understand meanings and experiences in depth, even if samples are small and studies are hard to repeat.'},
    'ctx': [('domestic violence in {city}', {'sensitive', 'hidden', 'private'}),
            ('pupils’ attitudes to school', {'young', 'meaning', 'large'}),
            ('voting behaviour in a national election', {'large', 'change'})],
    'data': [dict(what='response rates in survey research', pop='people invited to take part', rows=['Postal questionnaire', 'Online questionnaire', 'Face-to-face structured interview'], cols=('2005', '2025'),
                  base=[(25, 35), (25, 35), (60, 70)], delta=[(-15, -5), (-12, 0), (-15, -5)], label='response rate', nocount=True,
                  leads=['A research company recorded the response rates for {n} surveys it carried out in {city}.', 'The table shows response rates for different survey methods, reported by a research agency in {city} that ran {n} surveys.'], n=[40, 60, 80, 100, 120],
                  expl=['people are increasingly busy and suspicious of surveys, so fewer respond', 'face-to-face interviews have higher response rates because the interviewer is present',
                        'the volume of online surveys and spam has made people less willing to respond'],
                  method='official statistics', claim='low response rates are a serious threat to the representativeness of survey research',
                  counter='Interviews still achieve higher response rates; weighting and follow-up reminders can reduce bias; what matters is whether non-respondents differ from respondents.')],
    'essays': [('Explain two ways in which researchers try to ensure their samples are representative.', 'Using a complete, up-to-date sampling frame; random or stratified random sampling; quota sampling to match population proportions; adequate sample size; follow-up to improve response rates; pilot studies.',
                'validity is more important than reliability in sociological research',
                'Interpretivists argue the aim is to understand meanings (verstehen); reliable but invalid data is useless; qualitative methods give rich, valid data; feminist research gives voice to the powerless.',
                'Positivists argue reliability allows findings to be checked and generalised; small, valid studies cannot inform policy; triangulation aims for both; validity is hard to establish without checking.')],
}, V5)
classify(c5b, [
    ('A researcher repeats a study using the same questionnaire with a similar sample in {city} and obtains almost identical results.', 'Reliability', 'the study produced consistent results when repeated.'),
    ('{person}’s sample of {n} people contains the same proportions of men, women and age groups as the population of {city}.', 'Representativeness', 'the sample reflects the characteristics of the population.'),
    ('After months of trust-building, interviewees in {city} reveal experiences they had never told anyone before.', 'Validity', 'the data gives a true picture of people’s experiences.'),
    ('A national survey of {n} randomly selected households allows the researchers to make claims about the whole country.', 'Generalisability', 'the findings can be applied to the wider population.'),
], ['Reliability', 'Validity', 'Representativeness', 'Generalisability'], 'Which research concept is illustrated here?')

c5c = T('Practical, ethical and theoretical factors in choosing a method')
build(c5c, {
    'research': True,
    'terms': [
        ('practical factors', 'issues such as time, money, access and the skills of the researcher that affect the choice of method', 'a limited budget preventing a national survey'),
        ('ethical factors', 'moral issues about the way research affects the people involved, such as consent, harm and confidentiality', 'gaining parents’ permission before interviewing children'),
        ('theoretical factors', 'the influence of the researcher’s methodological perspective, such as positivism or interpretivism, on the choice of method', 'an interpretivist choosing participant observation'),
        ('informed consent', 'agreement to take part in research after being told about its aims and what participation involves', 'a signed consent form explaining the study'),
        ('confidentiality', 'keeping the identities and information of research participants private', 'using pseudonyms in a published report'),
        ('gatekeeper', 'a person who controls access to a group or setting that a researcher wants to study', 'a head teacher allowing a researcher into a school'),
        ('research aims', 'the purposes of a study, which shape the type of data and methods needed', 'aiming to measure trends or to understand experiences'),
        ('debriefing', 'telling participants the true purpose of a study after it has finished, especially if deception was used', 'explaining to participants that a field experiment was being carried out'),
    ],
    'thinkers': [
        ('Humphreys', 'covert observation can give access to hidden behaviour that people would never report', 'Interactionism',
         'Humphreys’s “Tearoom Trade” study of men in public toilets used covert observation and later traced participants to interview them in disguise.',
         'It is widely criticised as unethical because it used deception and risked exposing participants.'),
        ('Venkatesh', 'gaining trust over a long period allows researchers to understand gang life from the inside', 'Interactionism',
         'Venkatesh spent years with a Chicago drug gang, gaining access through a gang leader who acted as gatekeeper.',
         'His closeness to the gang raised ethical questions about knowledge of crimes and his objectivity.'),
        ('Oakley', 'researching women’s lives requires methods that build trust and treat participants as equals', 'Liberal feminism',
         'Oakley showed theoretical (feminist) values can shape the choice of method, favouring sympathetic, non-hierarchical interviews.',
         'Critics argue that friendship with interviewees can bias data.'),
    ],
    'explain': [
        ('Explain two practical factors that may influence a sociologist’s choice of research method.', 'Time: participant observation may take months or years; cost: national surveys or trained interviewers are expensive; access: some groups (e.g. elites or gangs) are hard to reach; researcher characteristics: age, gender or ethnicity may affect access; funding bodies may want quantitative data.', '2 marks for each explained factor. [4]'),
        ('Explain two ethical issues a researcher should consider when studying children.', 'Informed consent: children may not fully understand, so parents’ or guardians’ consent is needed; vulnerability and harm: questions must not cause distress; confidentiality, except where a child is at risk; power imbalance between adult and child.', '2 marks for each explained issue. [4]'),
        ('Explain how a researcher’s theoretical approach may influence the choice of method.', 'Positivists favour quantitative, reliable methods to find causes; interpretivists favour qualitative methods for verstehen and validity; feminists may favour methods giving women a voice. Theory shapes aims and what counts as good data.', '1 mark each perspective-method link up to 2; 1 mark for linking theory to research aims. [3]'),
    ],
    'why': [
        ('ethical issue', 'ethical issues', 'that can arise in covert participant observation', ['lack of informed consent', 'deception of participants', 'possible involvement in illegal or harmful acts', 'risk of exposing participants’ identities', 'harm to the researcher']),
        ('reason', 'reasons', 'why access can be a problem in sociological research', ['powerful groups can refuse to be studied', 'deviant groups may be suspicious of outsiders', 'gatekeepers may block access', 'the researcher’s age, gender or ethnicity may prevent them fitting in']),
    ],
    'claims': [
        ('Ethical issues only matter in covert research.', False, 'All research must consider consent, harm, confidentiality and the vulnerability of participants.'),
        ('Funding bodies can influence the methods sociologists use.', True, 'Funders may require particular types of data, such as statistics, or limit time and cost.'),
        ('Interpretivists choose methods mainly on practical grounds.', False, 'Their choice is mainly theoretical: they prefer qualitative methods for validity and verstehen.'),
    ],
    'ar': ([('Covert research raises ethical problems.', 'participants have not given informed consent.'),
            ('Researchers often use pseudonyms.', 'confidentiality protects participants from harm.'),
            ('Some groups are difficult to research.', 'gatekeepers may refuse access.')],
           ['informed consent means participants are not told the aims of the research.', 'practical factors never affect the choice of research method.']),
    'scen': ['{person}, a student with a small budget and only three months, wants to study the experiences of refugees in {city}.',
             'A sociologist in {city} wants to study a secretive religious group that refuses to talk to outsiders.',
             'A government department in {city} offers funding for research into youth unemployment but wants “hard statistics” for its report.'],
    'views': V5,
    'ctx': [('people who have experienced homelessness in {city}', {'hidden', 'sensitive', 'meaning'}),
            ('young carers who look after a disabled parent', {'young', 'sensitive', 'private'}),
            ('the attitudes of senior managers in large companies', {'meaning', 'hidden'})],
    'essays': [('Explain two ethical issues that may arise in sociological research.', 'Informed consent; deception (covert methods); confidentiality and anonymity; harm to participants (psychological, legal, social); vulnerable groups such as children; harm to researchers; legal obligations to report crime.',
                'practical factors are the most important influence on a sociologist’s choice of method',
                'Time, money and access limit what is possible; funding bodies shape research; the researcher’s skills and personal characteristics matter; some methods are impossible for certain groups.',
                'Theoretical factors (positivism vs. interpretivism) shape aims and preferred data; ethical factors can rule out methods (covert research with children); the topic and research question matter; most choices balance practical, ethical and theoretical factors (PET).')],
})
classify(c5c, [
    ('{person} cannot afford to employ interviewers, so uses an online questionnaire.', 'Practical factor', 'cost/money shaped the choice.'),
    ('A researcher decides not to study a gang covertly because members could not give informed consent.', 'Ethical factor', 'concern for consent and deception.'),
    ('{woman} chooses participant observation because she wants to understand the group’s meanings through verstehen.', 'Theoretical factor', 'an interpretivist methodological preference.'),
    ('The head teacher of a school in {city} refuses to let a researcher observe lessons.', 'Practical factor', 'access was blocked by a gatekeeper.'),
    ('A study of children in {city} is changed so that parents can withdraw their children at any time.', 'Ethical factor', 'protecting vulnerable participants and the right to withdraw.'),
    ('A positivist researcher chooses a large, standardised survey to test a hypothesis about income and health.', 'Theoretical factor', 'positivist preference for reliable, quantitative data.'),
], ['Practical factor', 'Ethical factor', 'Theoretical factor', 'Political factor'], 'Which type of factor most directly influenced the research decision?')

c5d = T('Sampling techniques: random, stratified, quota, snowball and opportunity')
build(c5d, {
    'research': True,
    'terms': [
        ('random sampling', 'a sampling method in which every member of the research population has an equal chance of being selected', 'drawing names from a complete school register using a random number generator'),
        ('systematic sampling', 'selecting every nth person from a sampling frame', 'choosing every 10th name on an electoral roll'),
        ('stratified random sampling', 'dividing the population into groups (strata) by characteristics such as age or gender, then randomly sampling from each in proportion to its size', 'randomly choosing 60% girls and 40% boys to match a school’s population'),
        ('quota sampling', 'selecting people who fit pre-set categories in proportion to the population until each quota is filled, without random selection', 'an interviewer stopping people in the street until 50 women aged 18-30 have been interviewed'),
        ('snowball sampling', 'finding participants through contacts given by people already in the sample', 'asking one drug user to introduce the researcher to others'),
        ('opportunity sampling', 'selecting whoever is available and willing at the time of the research', 'interviewing people who happen to be in a shopping centre'),
        ('purposive sampling', 'deliberately choosing participants because they have characteristics relevant to the research', 'selecting only head teachers to study school leadership'),
    ],
    'thinkers': [
        ('Savage', 'self-selecting online samples can produce biased pictures of the class structure', 'Weberian theory',
         'The Great British Class Survey attracted mainly educated, middle-class volunteers, so researchers had to add a separate nationally representative survey.',
         'Defenders argue very large online samples can still reveal useful patterns.'),
        ('Polsky', 'hidden and deviant groups can only be reached through trusted contacts', 'Interactionism',
         'Polsky’s research on hustlers relied on contacts and introductions, a form of snowball sampling, to reach people who would avoid official surveys.',
         'Snowball samples are unrepresentative because members share social networks.'),
    ],
    'explain': [
        ('Explain the difference between stratified random sampling and quota sampling.', 'Both divide the population into categories in proportion to their size; in stratified random sampling people within each stratum are chosen randomly from a sampling frame, whereas in quota sampling the researcher chooses anyone who fits the category until the quota is filled, so selection is not random.', '1 mark each method; 1 mark random vs. non-random selection. [3]'),
        ('Explain why snowball sampling is often used to study deviant groups.', 'There is no sampling frame for hidden groups such as drug users; members may distrust outsiders; introductions from trusted members give access and encourage participation.', '1 mark each developed point up to 3. [3]'),
        ('Explain one strength and one limitation of opportunity sampling.', 'Strength: quick, cheap and easy. Limitation: those available (e.g. shoppers on a weekday morning) are unlikely to represent the population, so findings cannot be generalised.', '2 marks each explained point. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why researchers may not be able to use random sampling', ['there may be no complete sampling frame', 'the group may be hidden or deviant', 'random samples can be costly and time-consuming', 'those selected may refuse to take part']),
    ],
    'claims': [
        ('Quota sampling involves random selection within each category.', False, 'Quota sampling is non-random: interviewers choose anyone who fits the category until the quota is filled.'),
        ('Snowball sampling is useful when there is no sampling frame.', True, 'Contacts introduce the researcher to others in hidden populations.'),
        ('Stratified random sampling can make a sample more representative than simple random sampling.', True, 'It ensures key groups appear in the correct proportions.'),
        ('Opportunity samples are usually highly representative.', False, 'They include only those available and willing at a particular time and place.'),
    ],
    'ar': ([('Snowball samples are often unrepresentative.', 'members tend to introduce people from their own social networks.'),
            ('Stratified samples reflect key characteristics of the population.', 'people are selected from each group in proportion to its size.'),
            ('Random sampling requires a sampling frame.', 'every member of the population must be listed to have an equal chance of selection.')],
           ['opportunity sampling gives every member of the population an equal chance of selection.', 'quota sampling always uses a complete list of the population.']),
    'scen': ['A researcher in {city} wants to interview undocumented migrant workers, who are afraid of being reported to the authorities.',
             '{person} interviews the first 50 people who walk past the library in {city} on a Tuesday morning.',
             'A national survey in {city} selects every 20th address from a list of all homes registered for local taxes.'],
    'views': {'Positivism': 'sampling should be random and representative so that findings can be generalised to the whole population and tested statistically.',
              'Interpretivism': 'representativeness matters less than depth; small purposive or snowball samples are acceptable when the aim is to understand meanings in hard-to-reach groups.'},
    'ctx': [('drug use among young people in {city}', {'hidden', 'sensitive', 'young'}),
            ('attitudes of university students to part-time work', {'large', 'meaning'}),
            ('the experiences of sex workers', {'hidden', 'sensitive'})],
    'essays': [('Explain two reasons why sociologists may use non-random sampling methods.', 'No sampling frame for hidden or deviant groups (snowball); cost and time (opportunity, quota); purposive aims in qualitative research; difficulty of access; interpretivist aims do not require representativeness.',
                'random sampling is always the best way to obtain a representative sample',
                'Each member has an equal chance of selection, reducing researcher bias; allows statistical generalisation; stratified random sampling improves representativeness further.',
                'Small random samples can be unrepresentative by chance; no sampling frame for hidden groups; non-response undermines randomness; quota sampling is cheaper and often accurate; interpretivists may not seek representativeness.')],
}, V5)
classify(c5d, [
    ('A researcher gives every student in a school in {city} a number and uses a random number generator to choose {n} of them.', 'Random sampling', 'every member had an equal chance of selection.'),
    ('{person} interviews one homeless person in {city}, who then introduces {person} to friends living on the streets.', 'Snowball sampling', 'participants were found through contacts.'),
    ('An interviewer in {city} is told to find 40 men and 60 women aged over 60 and stops passers-by until the numbers are reached.', 'Quota sampling', 'categories filled by non-random selection.'),
    ('A list of {n}0 employees is divided by grade, and a random sample is taken from each grade in proportion to its size.', 'Stratified random sampling', 'random selection within strata in proportion to size.'),
    ('{person} hands questionnaires to anyone willing to complete one in a café in {city}.', 'Opportunity sampling', 'whoever was available and willing was selected.'),
    ('A researcher chooses every 25th name from an alphabetical list of {n}0 voters in {city}.', 'Systematic sampling', 'every nth name was chosen from a sampling frame.'),
], ['Random sampling', 'Snowball sampling', 'Quota sampling', 'Stratified random sampling', 'Opportunity sampling', 'Systematic sampling'], 'Which sampling technique is being used?')


@c5d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5d_strat(r, D):
    groups = r.choice([(['boys', 'girls'], 'pupils at a school in {city}'), (['manual workers', 'office workers', 'managers'], 'employees at a factory in {city}'),
                       (['aged 18-34', 'aged 35-59', 'aged 60 and over'], 'adults in a town near {city}'), (['first-year', 'second-year', 'third-year'], 'students at a college in {city}')])
    names, pop = groups
    k = len(names)
    for _ in range(50):
        n = r.choice([40, 50, 60, 80, 100, 120, 150, 200])
        mult = r.choice([5, 8, 10, 12, 15, 20])
        if k == 2:
            p = r.choice([0.3, 0.35, 0.4, 0.45, 0.55, 0.6, 0.65, 0.7])
            shares = [p, 1 - p]
        else:
            a = r.choice([0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
            b = r.choice([0.2, 0.25, 0.3, 0.35, 0.4])
            if a + b >= 0.9:
                continue
            shares = [a, b, round(1 - a - b, 2)]
        Ntot = n * mult
        Ns = [round(Ntot * s_) for s_ in shares]
        Ns[-1] = Ntot - sum(Ns[:-1])
        ss = [n * N_ // Ntot for N_ in Ns]
        if all(n * N_ % Ntot == 0 for N_ in Ns) and all(x > 0 for x in ss):
            break
    else:
        return None
    d = ctxd(r)
    popt = fill(pop, d)
    desc = ', '.join(f'{N_} {nm}' for N_, nm in zip(Ns, names))
    intro = f'{d["person"]} wants a stratified random sample of {n} from {Ntot} {popt}. The population is made up of {desc}.'
    j = r.randrange(k)
    if D <= 1:
        ans = str(ss[j])
        ds = [str(x) for x in {round(n / k), ss[j] + 5, max(1, ss[j] - 5), Ns[j] // 10, ss[(j + 1) % k]} if x != ss[j]]
        opts, a = mcq(r, ans, ds)
        return {'stem': f'{intro} How many {names[j]} should be in the sample?', 'options': opts, 'answer': a,
                'key': f'{Ns[j]} ÷ {Ntot} × {n} = {ss[j]}. [1]', 'marks': 1}
    parts = [(f'Calculate how many {names[j]} should be included in the sample.', f'{Ns[j]} ÷ {Ntot} × {n} = {ss[j]}.', f'1 mark for {Ns[j]}/{Ntot} × {n}; 1 mark for {ss[j]}. [2]'),
             ('Calculate the number from each group needed in the sample.', '; '.join(f'{nm}: {N_} ÷ {Ntot} × {n} = {x}' for nm, N_, x in zip(names, Ns, ss)) + '.', f'1 mark for the method; 1 mark for all {k} correct values summing to {n}. [2]'),
             (f'State the sampling fraction used.', f'{n} ÷ {Ntot} = 1/{mult} (one in {mult}).', f'1/{mult}. [1]'),
             ('Explain why stratified random sampling is more likely than simple random sampling to produce a representative sample here.', 'It guarantees each group appears in the same proportion as in the population, whereas a simple random sample could by chance over- or under-represent a group.', '1 mark: proportions guaranteed; 1 mark: contrast with chance variation in simple random sampling. [2]'),
             ('Explain one practical problem the researcher might face in using this sampling method.', 'An up-to-date sampling frame showing each person’s group is needed; selected people may refuse, so the achieved sample may no longer match the strata; it takes more time than opportunity sampling.', '1 mark identifying the problem; 1 mark explaining it. [2]')]
    if D == 2:
        sel = [parts[0], parts[2]] if r.random() < 0.5 else [parts[1]]
    elif D == 3:
        sel = r.choice([[parts[1], parts[3]], [parts[0], parts[2], parts[3]], [parts[0], parts[4]]])
    else:
        sel = [parts[1], parts[2], parts[3], parts[4]] if D >= 5 else [parts[1], parts[3], parts[4]]
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


@c5d.add('C3', (1, 2, 3, 4), 'numerical')
def c5d_syst(r, D):
    for _ in range(30):
        n = r.choice([50, 80, 100, 120, 150, 200, 250, 400])
        k = r.choice([4, 5, 8, 10, 12, 15, 20, 25])
        N = n * k
        if N <= 6000:
            break
    frame = r.choice(['the electoral roll for a district of {city}', 'a list of all households in a village near {city}', 'the register of students at a university in {city}', 'a list of members of a trade union in {city}'])
    d = ctxd(r)
    intro = f'{d["person"]} wants a systematic sample of {n} people from {fill(frame, d)}, which contains {N} names.'
    if D <= 1:
        ds = [str(x) for x in (n, k * 2, max(2, k // 2), N // 100 if N // 100 != k else k + 3, k + 1)]
        opts, a = mcq(r, str(k), [x for x in ds if x != str(k)])
        return {'stem': f'{intro} What sampling interval should be used (select every nth name)?', 'options': opts, 'answer': a, 'key': f'{N} ÷ {n} = {k}: every {k}th name. [1]', 'marks': 1}
    start = r.randint(1, k)
    parts = [('Calculate the sampling interval.', f'{N} ÷ {n} = {k}; every {k}th name.', f'1 mark {N} ÷ {n}; 1 mark {k}. [2]'),
             (f'If the first name selected is number {start}, state the numbers of the next three names selected.', f'{start + k}, {start + 2 * k}, {start + 3 * k}.', f'All three correct ({start + k}, {start + 2 * k}, {start + 3 * k}). [1]'),
             ('Explain one way in which this sample might be unrepresentative.', 'The sampling frame may be incomplete or out of date (e.g. people not registered or who have moved); if the list has a repeating pattern the interval may pick out one type of person; selected people may refuse.', '1 mark identifying; 1 mark explaining. [2]')]
    sel = parts[:2] if D == 2 else parts
    return assemble(intro, sel, 'numerical')

CHAPTERS[5] = [c5a, c5b, c5c, c5d]


# ============================================================== CHAPTER 6: Quantitative research methods

c6a = T('Questionnaires and structured interviews')
build(c6a, {
    'research': True,
    'terms': [
        ('questionnaire', 'a list of written questions completed by respondents themselves, by post, online or by hand', 'an online survey about students’ use of social media'),
        ('structured interview', 'an interview in which the interviewer reads out the same pre-set questions in the same order to every respondent', 'a market research interviewer reading questions from a schedule'),
        ('closed question', 'a question that offers a fixed choice of answers', '“Do you own your home? Yes / No”'),
        ('open question', 'a question that allows respondents to answer in their own words', '“How do you feel about your job?”'),
        ('pre-coded question', 'a question whose possible answers have already been given numbers or categories for analysis', 'a five-point agree–disagree scale'),
        ('response rate', 'the percentage of people selected for a survey who actually take part', '300 replies from 1,000 questionnaires sent = 30%'),
        ('pilot study', 'a small-scale trial of a research method to identify problems before the main study', 'testing a questionnaire on ten people to find confusing questions'),
        ('operationalisation', 'turning an abstract concept into something that can be measured', 'measuring “religiosity” by frequency of attendance and prayer'),
    ],
    'thinkers': [
        ('Young and Willmott', 'families were becoming more symmetrical, based on structured interview evidence', 'Functionalism',
         'Young and Willmott used structured interviews with a large sample of families in London to argue that conjugal roles were becoming more equal.',
         'Oakley criticised their question design: men who did one household task a week counted as “helping”, which exaggerated equality.'),
        ('Oakley', 'questions about who “helps” with housework can give a misleading picture of equality', 'Liberal feminism',
         'Oakley argued that operationalising equality through vague questions in structured surveys produces invalid data.',
         'Others argue time-use diaries can be more accurate than either survey or interview data.'),
    ],
    'explain': [
        ('Explain two advantages of using closed questions in a questionnaire.', 'They are quick to answer, which improves response rates; answers are pre-coded so data is easy to quantify and compare; they are standardised, improving reliability; less risk of researcher interpretation bias.', '2 marks for each explained advantage. [4]'),
        ('Explain why it is important to carry out a pilot study before sending out a questionnaire.', 'It shows whether questions are clear and understood in the same way; reveals missing answer categories; tests the length and response rate; allows the researcher to improve the questionnaire before costly mistakes are made.', '1 mark each developed reason up to 3. [3]'),
        ('Explain why respondents may not give truthful answers in structured interviews.', 'Social desirability: they give answers that make them look good; interviewer bias: the interviewer’s age, gender or ethnicity may influence them; they may want to please the interviewer; they may not remember accurately.', '1 mark each developed reason up to 3. [3]'),
    ],
    'why': [
        ('way', 'ways', 'of improving the response rate to a postal or online questionnaire', ['keep the questionnaire short and clear', 'send reminders', 'offer an incentive such as a prize draw', 'guarantee anonymity', 'include a covering letter explaining the purpose']),
    ],
    'claims': [
        ('Open questions produce data that is easier to quantify than closed questions.', False, 'Closed, pre-coded questions are easier to quantify; open answers must be categorised first.'),
        ('Structured interviews usually achieve higher response rates than postal questionnaires.', True, 'The interviewer’s presence encourages people to take part.'),
        ('Questionnaires measure what people do rather than what they say they do.', False, 'They record what people say, which may differ from actual behaviour.'),
    ],
    'ar': ([('Postal questionnaires often have low response rates.', 'there is no interviewer present to encourage participation.'),
            ('Structured interviews are favoured by positivists.', 'they produce standardised, quantitative data that is reliable.'),
            ('Pilot studies can improve questionnaires.', 'they reveal confusing or missing questions before the main study.')],
           ['closed questions allow respondents to answer in their own words.', 'response rates are always 100% in structured interviews.']),
    'scen': ['{person} sends a 40-question postal questionnaire to 2,000 households in {city}; only 260 are returned, mostly from retired people.',
             'An interviewer in {city} reads a fixed list of questions about housework to husbands while their wives are in the room.'],
    'views': {'Positivism': 'questionnaires and structured interviews produce standardised, quantitative, reliable data from large samples, allowing hypotheses to be tested and findings generalised.',
              'Interpretivism': 'pre-set questions impose the researcher’s meanings and cannot uncover respondents’ own interpretations, so the data lacks validity.'},
    'ctx': [('attitudes to marriage among young adults in {city}', {'large', 'meaning'}),
            ('experiences of bullying in secondary schools', {'young', 'sensitive'}),
            ('the division of housework in dual-earner families', {'behaviour', 'private', 'large'})],
    'methods': ['questionnaire', 'structured interview', 'semi-structured interview', 'unstructured interview'],
    'essays': [('Explain two reasons why positivists favour questionnaires.', 'Standardised so reliable; large, representative samples allow generalisation; quantitative data allows correlations and hypothesis testing; researcher detached so objective; cheap and quick.',
                'questionnaires are the most useful method for sociological research',
                'Large samples, reliable and representative; cheap and fast; anonymity for sensitive topics; quantitative data for comparison and trends (positivists).',
                'Low response rates; closed questions lack validity and impose meanings; social desirability; cannot study hidden groups or behaviour; interpretivists prefer qualitative methods for verstehen.')],
}, V5)


@c6a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6a_rate(r, D):
    sent = r.choice([400, 500, 600, 800, 1000, 1200, 1500, 2000, 2500])
    rate = r.choice([18, 22, 25, 28, 30, 35, 40, 45, 55, 60, 65, 72])
    ret = sent * rate // 100
    if ret * 100 != sent * rate:
        return None
    d = ctxd(r)
    topic_ = r.choice(['attitudes to cohabitation', 'use of social media', 'experiences of work', 'religious belief', 'views on immigration', 'household finances'])
    intro = f'{d["person"]} sent a questionnaire about {topic_} to {sent} randomly selected adults in {d["city"]}. {ret} completed questionnaires were returned.'
    if D <= 1:
        ds = [f'{x}%' for x in (100 - rate, rate // 2 if rate // 2 != rate else rate + 3, min(99, rate * 2), round(sent / ret))] 
        opts, a = mcq(r, f'{rate}%', [x for x in ds if x != f'{rate}%'])
        return {'stem': f'{intro} What was the response rate?', 'options': opts, 'answer': a, 'key': f'{ret} ÷ {sent} × 100 = {rate}%. [1]', 'marks': 1}
    agree = r.choice([20, 25, 30, 40, 45, 50, 60, 64, 70, 75, 80])
    na = ret * agree // 100
    parts = [('Calculate the response rate.', f'{ret} ÷ {sent} × 100 = {rate}%.', f'1 mark method; 1 mark {rate}%. [2]'),
             (f'{agree}% of those who replied agreed with the main statement in the questionnaire. Calculate how many respondents this was.', f'{agree} ÷ 100 × {ret} = {na}' + ('' if ret * agree % 100 == 0 else ' (to the nearest whole person)') + '.',
              f'1 mark method; 1 mark {round(ret * agree / 100)}. [2]'),
             (f'Explain why a response rate of {rate}% may affect the representativeness of the findings.', ('With fewer than half replying, ' if rate < 50 else 'Even with a fairly good rate, ') + 'those who replied may differ systematically from those who did not (e.g. older, more educated or more interested in the topic), so the achieved sample may not represent the population.',
              '1 mark: respondents may differ from non-respondents; 1 mark: consequence for representativeness/generalisation. [2]'),
             ('Suggest two ways the researcher could have increased the response rate.', 'Send reminders; offer an incentive; keep the questionnaire short; guarantee anonymity; include a clear covering letter; use interviewers instead.', '1 mark each valid way. [2]'),
             ('Explain one reason why a structured interview might have produced more valid answers on this topic than a questionnaire, and one reason why it might not.', 'More valid: the interviewer can clarify questions so fewer are misunderstood. Less valid: interviewer bias or social desirability may lead respondents to give answers that please the interviewer.', '2 marks for each explained reason. [4]')]
    if D == 2:
        sel = [parts[0], parts[1]] if r.random() < 0.5 else [parts[0], parts[3]]
    elif D == 3:
        sel = [parts[0], parts[1], parts[2]] if r.random() < 0.5 else [parts[0], parts[2], parts[3]]
    else:
        sel = [parts[0], parts[1], parts[2], parts[4]]
    if ret * agree % 100:
        sel = [p for p in sel if p is not parts[1]] or [parts[0], parts[2]]
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


c6b = T('Experiments: laboratory and field experiments in sociology')
build(c6b, {
    'research': True,
    'terms': [
        ('laboratory experiment', 'an experiment carried out in a controlled, artificial setting where the researcher manipulates variables', 'measuring children’s aggression after they watch a violent video in a laboratory'),
        ('field experiment', 'an experiment carried out in a real-life social setting, often without participants knowing', 'sending identical job applications with different names to employers'),
        ('independent variable', 'the factor the researcher changes to see its effect', 'the ethnic-sounding name on a CV'),
        ('dependent variable', 'the factor measured to see whether it is affected by the independent variable', 'the number of job interview offers'),
        ('control group', 'a group in an experiment that is not exposed to the independent variable, used for comparison', 'children who watch a non-violent video'),
        ('experimental group', 'the group in an experiment that is exposed to the independent variable', 'children who watch a violent video'),
        ('comparative method', 'a “thought experiment” comparing groups or societies to identify the causes of differences', 'Durkheim comparing suicide rates across religious groups'),
    ],
    'thinkers': [
        ('Rosenthal and Jacobson', 'teachers’ expectations can raise pupils’ achievement through a self-fulfilling prophecy', 'Interactionism',
         'In a field experiment in a Californian school, teachers were told some randomly chosen pupils were “spurters”; many of these pupils made greater IQ gains.',
         'The study involved deceiving teachers and has proved hard to replicate.'),
        ('Bandura', 'children imitate aggressive behaviour they have seen modelled', 'Positivism',
         'Bandura’s laboratory experiments with a Bobo doll found children who watched an adult behave aggressively were more likely to copy it.',
         'The artificial setting lacks validity: hitting a toy designed to be hit is not real violence.'),
        ('Rosenhan', 'psychiatric labels shape how staff interpret people’s behaviour', 'Interactionism',
         'In Rosenhan’s field experiment, sane “pseudo-patients” admitted to psychiatric hospitals had their normal behaviour interpreted as symptoms.',
         'It deceived hospital staff, raising ethical concerns.'),
    ],
    'explain': [
        ('Explain why sociologists rarely use laboratory experiments.', 'Artificial settings mean behaviour lacks validity; it is impossible to control all variables affecting human behaviour; many issues cannot be studied for ethical reasons; small samples limit generalisation; the Hawthorne effect.', '1 mark each developed reason up to 3. [3]'),
        ('Explain one advantage and one disadvantage of field experiments compared with laboratory experiments.', 'Advantage: natural setting so behaviour is more realistic and valid. Disadvantage: less control over variables, so cause and effect are harder to establish; also ethical problems of consent.', '2 marks for each explained point. [4]'),
        ('Explain why a control group is used in an experiment.', 'It provides a baseline for comparison: by comparing the experimental group (exposed to the independent variable) with a similar control group (not exposed), the researcher can see whether the variable caused any difference.', '1 mark: comparison/baseline; 1 mark: isolates effect of the independent variable. [2]'),
    ],
    'why': [
        ('ethical problem', 'ethical problems', 'that can arise in field experiments', ['participants have not given informed consent', 'deception is used', 'participants may be harmed or embarrassed', 'participants cannot withdraw from a study they do not know about']),
    ],
    'claims': [
        ('Field experiments take place in artificial settings.', False, 'Field experiments take place in real-life settings; laboratory experiments are artificial.'),
        ('Experiments are favoured by positivists.', True, 'They allow variables to be controlled to identify cause and effect.'),
        ('Rosenthal and Jacobson’s study was a laboratory experiment.', False, 'It was a field experiment carried out in a real school.'),
    ],
    'ar': ([('Laboratory experiments are often criticised for lacking validity.', 'people may behave differently in an artificial setting.'),
            ('Field experiments can study real behaviour.', 'participants are often unaware that they are being studied.')],
           ['laboratory experiments give the researcher less control than field experiments.', 'the dependent variable is the one the researcher deliberately changes.']),
    'scen': ['{person}, a researcher in {city}, sends pairs of identical job applications to employers, one with a local-sounding name and one with a migrant-sounding name.',
             'A researcher shows one group of children in {city} a violent cartoon and another group a non-violent cartoon, and then counts aggressive acts in a playroom.'],
    'views': {'Positivism': 'experiments allow variables to be controlled so that cause and effect can be identified objectively and the study can be repeated.',
              'Interpretivism': 'people act on meanings and know when they are being studied, so experiments create artificial behaviour and cannot reveal the meanings behind actions.'},
    'ctx': [('discrimination by employers against migrant job applicants', {'behaviour', 'sensitive'}),
            ('the effect of teachers’ expectations on pupils’ progress', {'young', 'behaviour'})],
    'methods': ['laboratory experiment', 'field experiment', 'questionnaire', 'participant observation', 'non-participant observation', 'unstructured interview'],
    'essays': [('Explain two reasons why field experiments may be more useful to sociologists than laboratory experiments.', 'Natural setting improves validity; participants unaware so no Hawthorne effect; can study real social processes such as discrimination; can study larger groups.',
                'experiments are of limited use in sociological research',
                'Artificial settings; impossible to control all variables; ethical problems of deception and harm; Hawthorne effect; small samples; interpretivists argue they ignore meanings.',
                'Field experiments such as Rosenthal and Jacobson or CV studies reveal real discrimination; they can show cause and effect; controlled comparison is valuable; positivists value their reliability.')],
}, V5)


@c6b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6b_field(r, D):
    pairs = r.choice([40, 50, 60, 80, 100, 120, 150, 200])
    p1 = r.choice([20, 25, 30, 35, 40, 45, 50])
    p2 = p1 - r.choice([5, 10, 12, 15, 18, 20])
    a1, a2 = pairs * p1 // 100, pairs * p2 // 100
    if a1 * 100 != pairs * p1 or a2 * 100 != pairs * p2 or p2 <= 0:
        return None
    d = ctxd(r)
    intro = (f'In a field experiment in {d["city"]}, researchers sent {pairs} pairs of identical job applications to employers. In each pair one used a locally common name and the other a name associated with a minority ethnic group. '
             f'{a1} of the “local-name” applications received an invitation to interview, compared with {a2} of the “minority-name” applications.')
    if D <= 1:
        ans = f'{p1 - p2} percentage points'
        ds = [f'{a1 - a2} percentage points' if a1 - a2 != p1 - p2 else f'{p1 - p2 + 5} percentage points', f'{p1} percentage points', f'{p2} percentage points', f'{round(100 * (p1 - p2) / p1)} percentage points']
        opts, a = mcq(r, ans, [x for x in ds if x != ans])
        return {'stem': f'{intro} What is the difference between the two success rates?', 'options': opts, 'answer': a,
                'key': f'{a1}/{pairs} = {p1}%; {a2}/{pairs} = {p2}%; difference {p1 - p2} percentage points. [1]', 'marks': 1}
    parts = [('Calculate the percentage of applications in each group that received an interview invitation.', f'Local name: {a1} ÷ {pairs} × 100 = {p1}%; minority name: {a2} ÷ {pairs} × 100 = {p2}%.', '1 mark each correct percentage. [2]'),
             ('Identify the independent and dependent variables in this experiment.', 'Independent variable: the name (ethnic background) on the application. Dependent variable: whether an interview invitation was received.', '1 mark each. [2]'),
             ('Explain why the applications in each pair were otherwise identical.', 'To control other variables (qualifications, experience), so any difference in invitations can be attributed to the name, i.e. to discrimination.', '1 mark: controls other variables; 1 mark: isolates effect of the name. [2]'),
             ('Explain one ethical problem with this research.', 'Employers did not give informed consent and were deceived; their time was wasted; if identified they could suffer reputational harm.', '1 mark identifying; 1 mark explaining. [2]'),
             ('Evaluate how far this experiment shows that employers discriminate against minority ethnic applicants.', f'It shows a clear gap ({p1 - p2} percentage points) when other variables were controlled, which suggests discrimination; but names may signal other things (e.g. class or religion), the sample of employers may not be representative, and it measures only the first stage of recruitment.',
              'Level 1 (1-2): simple comment. Level 2 (3-4): explains strengths and limitations of the evidence with a judgement. [4]')]
    if D == 2:
        sel = [parts[0], parts[1]]
    elif D == 3:
        sel = r.choice([[parts[0], parts[2]], [parts[0], parts[1], parts[3]]])
    else:
        sel = [parts[0], parts[1], parts[4]] if D == 4 else [parts[0], parts[2], parts[3], parts[4]]
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


c6c = T('Official statistics and other secondary quantitative data')
build(c6c, {
    'research': True,
    'terms': [
        ('official statistics', 'numerical data collected by governments and their agencies', 'census data, crime figures and birth rates'),
        ('secondary data', 'data that already exists, collected by someone other than the researcher', 'government statistics, newspapers and previous studies'),
        ('primary data', 'data collected first-hand by the researcher for the current study', 'answers from a researcher’s own questionnaire'),
        ('census', 'a survey of the whole population of a country, usually carried out every ten years', 'a national population count recording age, household size and occupation'),
        ('hard statistics', 'statistics that are relatively objective and difficult to manipulate, such as births and deaths', 'registered deaths'),
        ('soft statistics', 'statistics that are open to interpretation and manipulation, often depending on decisions by officials', 'recorded crime or truancy figures'),
        ('dark figure of crime', 'crime that is not reported to or recorded by the police and so does not appear in official statistics', 'unreported domestic violence'),
    ],
    'thinkers': [
        ('Durkheim', 'official suicide statistics can be used comparatively to find the social causes of suicide', 'Positivism',
         'Durkheim compared suicide rates between countries and religious groups, finding rates varied with social integration and regulation.',
         'Interactionists such as Atkinson argue that coroners’ decisions shape the statistics.'),
        ('Atkinson', 'suicide statistics reflect the common-sense theories used by coroners to classify deaths', 'Interpretivism',
         'Atkinson argued coroners look for cues such as a note, mode of death or a history of depression, so statistics are social constructions.',
         'Taken to its extreme, this view would make all statistics unusable.'),
        ('Cicourel', 'official statistics on juvenile delinquency are the product of police and probation officers’ stereotypes', 'Interactionism',
         'Cicourel found that officers’ typifications of the “typical delinquent” led to more working-class youths being arrested and charged.',
         'His study was based on two Californian cities and may not be typical.'),
    ],
    'explain': [
        ('Explain the difference between hard and soft statistics, using an example of each.', 'Hard statistics are relatively objective and hard to manipulate (e.g. births or deaths); soft statistics depend on interpretation and decisions by officials and can be manipulated (e.g. crime or unemployment figures).', '1 mark each definition; 1 mark each example. [4]'),
        ('Explain why interpretivists argue that official statistics are social constructions.', 'They are the result of decisions made by people, such as whether victims report crimes, whether police record them, and how officials classify cases; definitions are set by governments and change; so they reflect social processes, not objective facts.', '1 mark each developed point up to 3. [3]'),
        ('Explain two advantages of using official statistics in sociological research.', 'Free and readily available; large-scale, often covering the whole population; collected regularly so trends can be seen; allow comparisons between groups and areas; positivists see them as reliable social facts.', '2 marks for each explained advantage. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why official crime statistics may underestimate the true amount of crime', ['victims may not report crimes because they think the police will do nothing', 'some crimes have no obvious victim', 'victims may fear retaliation or feel embarrassed', 'the police may decide not to record reported crimes', 'some crimes such as fraud are hidden']),
    ],
    'claims': [
        ('Official statistics always give an accurate picture of society.', False, 'Many (especially soft) statistics are shaped by reporting, recording and definitions, so they may be inaccurate.'),
        ('Census data allows comparisons over time.', True, 'It is collected regularly, though changes in questions can affect comparisons.'),
        ('Positivists see official statistics as a useful source of social facts.', True, 'They are large-scale and quantitative, allowing correlations and trends to be identified.'),
    ],
    'ar': ([('Official crime statistics are described as soft statistics.', 'they depend on the reporting decisions of victims and the recording decisions of the police.'),
            ('Official statistics allow trends to be studied.', 'many are collected in the same way every year.')],
           ['births and deaths are examples of soft statistics.', 'official statistics are collected by sociologists for their own research.']),
    'scen': ['A researcher compares recorded crime in {city}, which fell by 12% in one year, with a victim survey for the same year that shows little change.',
             '{person} uses official unemployment statistics to measure change in {city} over ten years, although the government changed the definition of “unemployed” during the period.'],
    'views': {'Positivism': 'official statistics are useful social facts: large-scale, reliable and cheap, they allow trends and correlations to be identified and hypotheses tested (Durkheim).',
              'Interpretivism': 'official statistics are social constructions produced by the decisions of officials and the public, so they tell us more about those decisions than about the reality they claim to measure (Atkinson, Cicourel).',
              'Marxism': 'official statistics are produced by the state and may serve ruling-class interests, for example by concealing inequality or focusing on working-class crime rather than corporate crime.'},
    'ctx': [('changes in the divorce rate over fifty years', {'change', 'large'}),
            ('the extent of domestic violence', {'sensitive', 'hidden', 'private'}),
            ('regional differences in educational achievement', {'large', 'change'})],
    'methods': ['official statistics', 'questionnaire', 'structured interview', 'unstructured interview', 'longitudinal study'],
    'essays': [('Explain two reasons why positivists use official statistics.', 'Cheap, available and large-scale; collected regularly so trends can be studied; comparisons between groups and societies; treated as objective social facts; allow hypotheses to be tested (Durkheim).',
                'official statistics are of limited use to sociologists',
                'They are socially constructed (Atkinson, Cicourel); definitions change; the dark figure; they show patterns not meanings; may be politically manipulated.',
                'Hard statistics such as births and deaths are reliable; large-scale data no researcher could collect; essential for trends and comparisons; even “constructed” statistics reveal how institutions operate.')],
}, V5)


@c6c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6c_rates(r, D):
    kind = r.choice([('births', 'crude birth rate', 'births per 1,000 population'), ('deaths', 'crude death rate', 'deaths per 1,000 population'),
                     ('marriages', 'crude marriage rate', 'marriages per 1,000 population'), ('divorces', 'crude divorce rate', 'divorces per 1,000 population')])
    ev, rname, unit = kind
    lo, hi = {'births': (8, 30), 'deaths': (5, 14), 'marriages': (3, 9), 'divorces': (1, 4)}[ev]
    for _ in range(40):
        pop = r.choice([120000, 150000, 200000, 250000, 400000, 500000, 800000, 1200000, 1500000, 2000000])
        rate1 = round(r.uniform(lo, hi), 1)
        rate2 = round(rate1 * r.choice([0.7, 0.8, 0.85, 0.9, 1.1, 1.15, 1.25]), 1)
        n1, n2 = round(rate1 * pop / 1000), round(rate2 * pop / 1000)
        if n1 != n2:
            break
    rr1, rr2 = n1 / pop * 1000, n2 / pop * 1000
    d = ctxd(r)
    y1, y2 = r.choice([(2005, 2025), (2010, 2024), (2000, 2020), (1995, 2025)])
    intro = f'Official statistics for a region around {d["city"]} show a population of {pop:,} in both {y1} and {y2}. There were {n1:,} {ev} in {y1} and {n2:,} in {y2}.'
    if D <= 1:
        ans = f'{rr1:.1f}'
        ds = [f'{rr1 * 10:.1f}', f'{rr1 / 10:.2f}', f'{rr2:.1f}', f'{n1 / pop * 100:.2f}']
        opts, a = mcq(r, ans, [x for x in ds if x != ans])
        return {'stem': f'{intro} What was the {rname} ({unit}) in {y1}?', 'options': opts, 'answer': a, 'key': f'{n1:,} ÷ {pop:,} × 1,000 = {rr1:.1f}. [1]', 'marks': 1}
    pc = 100 * (rr2 - rr1) / rr1
    parts = [(f'Calculate the {rname} ({unit}) for {y1} and for {y2}.', f'{y1}: {n1:,} ÷ {pop:,} × 1,000 = {rr1:.1f}; {y2}: {n2:,} ÷ {pop:,} × 1,000 = {rr2:.1f}.', '1 mark method; 1 mark both rates correct to 1 d.p. [2]'),
             (f'Calculate the percentage change in the {rname} between {y1} and {y2}.', f'({rr2:.1f} − {rr1:.1f}) ÷ {rr1:.1f} × 100 = {_pc(100 * (round(rr2, 1) - round(rr1, 1)) / round(rr1, 1))}%.', '1 mark method; 1 mark answer (accept small rounding differences). [2]'),
             (f'Explain why sociologists use rates per 1,000 rather than the total number of {ev}.', f'Rates take account of population size, so places or years with different populations can be compared fairly; raw totals rise or fall simply because the population changes.', '1 mark: controls for population size; 1 mark: allows valid comparison. [2]'),
             (f'Explain one reason why official statistics on {ev} may be more reliable than official statistics on crime.', f'Registration of {ev} is a legal requirement and the event is clearly defined (a “hard” statistic), whereas crime statistics depend on victims reporting and police recording (“soft” statistics).', '1 mark: hard vs soft; 1 mark: explanation of registration/definition. [2]'),
             (f'Suggest two sociological reasons for the change in the {rname}.', {'births': ('Pro-natalist policies; migration of young adults into the region; improved economic confidence.', 'Women’s greater participation in education and paid work; the cost of children; availability of contraception; changing attitudes to family size.'),
                                                                                    'deaths': ('An ageing population with more older people; epidemics or worsening health care.', 'Improvements in health care, diet, sanitation and living standards.'),
                                                                                    'marriages': ('Changing attitudes or financial incentives encouraging marriage; a larger number of young adults.', 'Secularisation and the growing acceptance of cohabitation; later marriage.'),
                                                                                    'divorces': ('Changes in divorce law, declining stigma, secularisation, rising expectations of marriage and women’s financial independence.', 'Fewer people marrying in the first place; more couples cohabiting instead; later, more considered marriages.')}[ev][0 if rr2 > rr1 else 1],
              '1 mark each valid reason linked to the direction of change. [2]')]
    if D == 2:
        sel = [parts[0], parts[2]]
    elif D == 3:
        sel = [parts[0], parts[1], parts[2]] if r.random() < 0.5 else [parts[0], parts[3], parts[4]]
    else:
        sel = [parts[0], parts[1], parts[3], parts[4]]
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


c6d = T('Analysing and interpreting quantitative data in sociological research')
build(c6d, {
    'research': True,
    'terms': [
        ('mean', 'the average found by adding all the values and dividing by the number of values', 'the mean of 2, 4 and 9 is 5'),
        ('median', 'the middle value when data is arranged in order', 'the median of 3, 5, 6, 8, 20 is 6'),
        ('mode', 'the value that occurs most often in a set of data', 'in 2, 3, 3, 7 the mode is 3'),
        ('correlation', 'a statistical relationship between two variables, where one changes as the other changes', 'areas with higher unemployment tending to have higher crime rates'),
        ('causation', 'a relationship in which a change in one variable directly produces a change in another', 'a new law directly reducing a particular crime'),
        ('trend', 'the general direction of change in data over time', 'a steady rise in cohabitation over thirty years'),
        ('percentage point', 'the unit for the arithmetic difference between two percentages', 'a rise from 30% to 35% is 5 percentage points'),
    ],
    'thinkers': [
        ('Durkheim', 'statistical patterns in suicide rates reveal the influence of social facts on individual behaviour', 'Positivism',
         'Durkheim identified correlations (e.g. Protestants had higher suicide rates than Catholics) and argued these reflected differences in integration.',
         'Correlation does not prove causation; differences may reflect how deaths were recorded.'),
    ],
    'explain': [
        ('Explain the difference between correlation and causation, using a sociological example.', 'Correlation means two variables change together (e.g. areas with poorer housing have lower exam results); causation means one directly produces the other; a correlation may be due to a third factor (e.g. poverty affecting both).', '1 mark correlation; 1 mark causation; 1 mark example showing a third variable or limitation. [3]'),
        ('Explain why the median may be a better measure of average than the mean for income data.', 'Income data usually contains a few very high values that pull the mean upwards; the median (middle value) is not affected by extreme values, so it better represents a typical person.', '1 mark: extreme values distort the mean; 1 mark: median unaffected/typical. [2]'),
        ('Explain the difference between a percentage change and a change in percentage points.', 'A percentage-point change is the arithmetic difference between two percentages (30% to 36% = 6 points); a percentage change is the change relative to the starting value (6 ÷ 30 × 100 = 20%).', '1 mark each with correct illustration. [2]'),
    ],
    'why': [
        ('reason', 'reasons', 'why sociologists should be cautious when interpreting statistical data', ['correlation does not prove causation', 'the sample may not be representative', 'definitions and categories may have changed over time', 'statistics may be socially constructed', 'small differences may be due to chance']),
    ],
    'claims': [
        ('If two variables are correlated, one must cause the other.', False, 'Correlation may be coincidental or caused by a third variable.'),
        ('The mode is the most frequently occurring value.', True, 'It is useful for categorical data such as the most common family type.'),
        ('A rise from 20% to 30% is a 10% increase.', False, 'It is a 10 percentage-point rise but a 50% increase relative to the starting value.'),
    ],
    'ar': ([('A positive correlation does not prove causation.', 'a third variable may affect both variables.'),
            ('The median is not distorted by extreme values.', 'it is based on the middle value in an ordered set of data.')],
           ['the mean is always the best measure of average for income.', 'a negative correlation means there is no relationship between the variables.']),
    'scen': ['A study in {city} finds that pupils who eat breakfast get better exam results and concludes that breakfast clubs will close the achievement gap.',
             'A report on living standards in {city} uses the mean household income, which is much higher than the median household income, to describe a “typical” family.'],
    'views': {'Positivism': 'statistical analysis reveals objective patterns and correlations that can be used to test hypotheses and identify causes, as Durkheim did.',
              'Interpretivism': 'statistics only show surface patterns; they need to be interpreted alongside qualitative evidence of meanings, and the categories used are themselves social constructions.'},
    'ctx': [('the link between poverty and educational achievement', {'large', 'change'}),
            ('trends in cohabitation and marriage', {'large', 'change'})],
    'methods': ['official statistics', 'questionnaire', 'structured interview', 'longitudinal study'],
    'essays': [('Explain two problems sociologists face when interpreting quantitative data.', 'Correlation is not causation; unrepresentative samples; changes in definitions; statistics as social constructions; choice of average can mislead; missing data and the dark figure.',
                'quantitative data gives an objective picture of society',
                'Standardised, reliable and large-scale; allows comparison and trends; positivists see statistics as social facts; patterns can be checked by others.',
                'Interpretivists see statistics as social constructions; operationalisation choices shape results; correlation is not causation; data lacks meaning and context; interpretation involves values.')],
}, V5)


@c6d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6d_avg(r, D):
    what = r.choice([('hours of housework done per week by', 'men in a sample of dual-earner couples', 'h'), ('hours spent online per day by', 'students in a sample', 'h'),
                     ('number of household tasks regularly done by', 'fathers in a sample of families', ''), ('years of full-time education completed by', 'adults in a village survey', '')])
    lab, grp, u = what
    for _ in range(40):
        n = r.choice([7, 9, 11])
        vals = sorted(r.randint(1, 15) for _ in range(n - 1)) + [r.randint(18, 30)]
        vals.sort()
        cnt = {v: vals.count(v) for v in vals}
        mx = max(cnt.values())
        modes = [v for v in cnt if cnt[v] == mx]
        if mx >= 2 and len(modes) == 1 and sum(vals) % n == 0:
            break
    else:
        return None
    mean = sum(vals) // n
    med = vals[n // 2]
    mode = modes[0]
    rng = vals[-1] - vals[0]
    show = vals[:]
    r.shuffle(show)
    d = ctxd(r)
    intro = f'{d["person"]} recorded the {lab} {n} {grp} in {d["city"]}: ' + ', '.join(map(str, show)) + '.'
    if D <= 1:
        which = r.choice(['mean', 'median', 'mode'])
        ans = {'mean': mean, 'median': med, 'mode': mode}[which]
        ds = [str(x) for x in {mean, med, mode, rng, vals[-1]} if x != ans]
        if len(ds) < 3:
            ds.append(str(ans + 1))
        opts, a = mcq(r, str(ans), ds)
        how = {'mean': f'{sum(vals)} ÷ {n} = {mean}', 'median': f'ordered: {", ".join(map(str, vals))}; middle value = {med}', 'mode': f'{mode} occurs most often'}[which]
        return {'stem': f'{intro} What is the {which}?', 'options': opts, 'answer': a, 'key': f'{how}. [1]', 'marks': 1}
    parts = [('Calculate the mean.', f'{sum(vals)} ÷ {n} = {mean}.', f'1 mark total {sum(vals)}; 1 mark {mean}. [2]'),
             ('Find the median.', f'Ordered: {", ".join(map(str, vals))}; median = {med}.', f'1 mark ordering; 1 mark {med}. [2]'),
             ('State the mode and the range.', f'Mode = {mode}; range = {vals[-1]} − {vals[0]} = {rng}.', '1 mark each. [2]'),
             ('Explain which average best represents the typical value in this data set.', f'The median ({med}) or mode, because the extreme value of {vals[-1]} pulls the mean ({mean}) upwards.' if mean > med else f'The mean ({mean}) and median ({med}) are similar, so either is reasonable, though the median is less affected by the extreme value {vals[-1]}.',
              '1 mark choice; 1 mark reason referring to the extreme value. [2]'),
             ('Explain one reason why the findings from this sample should not be generalised.', f'The sample of {n} is very small and was not necessarily randomly selected, so it may not represent the wider population.', '1 mark: small/unrepresentative sample; 1 mark: consequence for generalisation. [2]')]
    if D == 2:
        sel = r.choice([[parts[0], parts[1]], [parts[1], parts[2]]])
    elif D == 3:
        sel = [parts[0], parts[1], parts[3]]
    else:
        sel = [parts[0], parts[1], parts[2], parts[3]] if D == 4 else parts
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')

CHAPTERS[6] = [c6a, c6b, c6c, c6d]


# ============================================================== CHAPTER 7: Qualitative research methods and mixed methods

c7a = T('Unstructured and semi-structured interviews')
build(c7a, {
    'research': True,
    'terms': [
        ('unstructured interview', 'an informal, guided conversation with no fixed list of questions, allowing the interviewee to talk freely', 'a long conversation with a refugee about their journey'),
        ('semi-structured interview', 'an interview with a set of core questions but freedom for the interviewer to probe and ask follow-up questions', 'asking every teacher the same five questions and then following up interesting answers'),
        ('rapport', 'a relationship of trust and understanding between the researcher and the people being studied', 'an interviewer who listens sympathetically and puts the interviewee at ease'),
        ('probing', 'asking follow-up questions to encourage an interviewee to explain or develop an answer', '“Can you tell me more about why you felt that way?”'),
        ('group interview', 'an interview with several people at once, in which they can discuss topics with one another', 'interviewing a group of five friends together'),
        ('transcript', 'a written record of everything said in an interview', 'a typed record of a recorded interview'),
        ('social desirability', 'the tendency of respondents to give answers that present themselves in a good light', 'exaggerating the amount of housework one does'),
    ],
    'thinkers': [
        ('Oakley', 'interviewing women should be a non-hierarchical, two-way relationship', 'Liberal feminism',
         'In her study of first-time mothers, Oakley answered interviewees’ questions and built friendships, arguing this produced more valid data.',
         'Critics argue the interviewer’s involvement may lead interviewees to say what they think the interviewer wants.'),
        ('Dobash and Dobash', 'domestic violence is best understood through in-depth interviews with women who have experienced it', 'Radical feminism',
         'Dobash and Dobash used unstructured interviews, police and court records to show violence occurred when husbands felt their authority was challenged.',
         'Their sample came from refuges and police records, so may not represent all victims.'),
        ('Labov', 'the interview setting can shape how people speak and what they reveal', 'Interactionism',
         'Labov found black American children seemed inarticulate in formal interviews but spoke fluently in relaxed settings with a familiar interviewer, showing interviewer effects.',
         'The findings relate to language use and may not apply to all interview topics.'),
    ],
    'explain': [
        ('Explain why unstructured interviews are useful for studying sensitive topics.', 'Rapport and trust encourage interviewees to talk about painful or private experiences; the interviewer can respond sensitively and follow up; interviewees can describe experiences in their own words, so data is valid.', '1 mark each developed point up to 3. [3]'),
        ('Explain two advantages of semi-structured interviews over structured interviews.', 'The interviewer can probe and ask follow-up questions, giving more depth and validity; interviewees can raise unexpected issues; core questions still allow some comparison.', '2 marks for each explained advantage. [4]'),
        ('Explain two disadvantages of group interviews.', 'Dominant individuals may influence others (peer pressure); people may not reveal private views in front of others; it is difficult to record and transcribe; confidentiality cannot be guaranteed.', '2 marks for each explained disadvantage. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why interpretivists favour unstructured interviews', ['they produce rich, qualitative data about meanings', 'rapport increases validity', 'the interviewee sets the agenda, avoiding imposition of the researcher’s categories', 'they allow verstehen']),
    ],
    'claims': [
        ('Unstructured interviews are easy to repeat, so they are highly reliable.', False, 'Each unstructured interview is unique, so they are difficult to replicate and less reliable.'),
        ('Rapport can improve the validity of interview data.', True, 'Trust encourages interviewees to give honest and detailed answers.'),
        ('Interviewer bias cannot occur in unstructured interviews.', False, 'The interviewer’s characteristics and reactions may influence answers, perhaps even more than in structured interviews.'),
    ],
    'ar': ([('Unstructured interviews are favoured by interpretivists.', 'they allow interviewees to explain the meanings of their experiences in their own words.'),
            ('Unstructured interviews are usually carried out with small samples.', 'they are time-consuming and costly to conduct and analyse.')],
           ['unstructured interviews use a fixed list of closed questions.', 'interpretivists value reliability above validity.']),
    'scen': ['{person} spends three hours talking to a woman in {city} who has left a violent partner, letting her tell her story in her own way.',
             'A researcher in {city} interviews groups of five teenage boys about their views on masculinity and notices that one boy dominates each discussion.'],
    'views': V5,
    'ctx': [('women’s experiences of domestic violence', {'sensitive', 'private', 'meaning'}),
            ('how teenagers experience peer pressure', {'young', 'meaning', 'sensitive'}),
            ('the experiences of migrant domestic workers in {city}', {'hidden', 'meaning', 'sensitive'})],
    'methods': ['unstructured interview', 'semi-structured interview', 'structured interview', 'questionnaire', 'participant observation'],
    'source': [dict(text='A sociologist interviewed 20 fathers in {city} who had taken more than six months of parental leave. Each interview lasted around two hours and followed the father’s own account. Many said they had felt “out of place” at parent groups, and several said friends had questioned their masculinity.',
                    method='unstructured interview', about='fathers’ experiences of parental leave', finds=['many fathers felt out of place at parent groups', 'several said friends had questioned their masculinity'],
                    persp='Interactionism', pview='The fathers’ experiences show how identities are negotiated in interaction: others’ reactions and labels challenge their sense of masculinity and shape how they see themselves.',
                    claim='unstructured interviews are the best method for studying family life', pro='The source shows rich, detailed data on feelings and meanings, gained through long interviews following the fathers’ own accounts.',
                    con='Twenty fathers in one city cannot be generalised; interviews record what people say rather than what they do; time-use diaries or questionnaires show wider patterns; interviewer effects may shape answers.', flags={'meaning', 'sensitive'})],
    'essays': [('Explain two strengths of unstructured interviews for sociological research.', 'Rapport and trust; rich, valid qualitative data; interviewee’s own words and meanings; flexibility to explore unexpected issues; useful for sensitive topics (Dobash and Dobash).',
                'unstructured interviews produce more valid data than structured interviews',
                'Rapport encourages honesty; probing reveals meanings; interviewees use their own words; interpretivists value verstehen; feminists (Oakley) favour non-hierarchical interviews.',
                'Interviewer bias and social desirability; data shaped by the interaction (Labov); small samples; lack of reliability; structured interviews can reduce bias through standardisation; validity also depends on honesty.')],
}, V5)

c7b = T('Participant and non-participant observation, overt and covert')
build(c7b, {
    'research': True,
    'terms': [
        ('participant observation', 'a method in which the researcher joins in the life of the group being studied while observing it', 'a researcher working in a factory to study workers'),
        ('non-participant observation', 'a method in which the researcher observes a group without taking part in its activities', 'a researcher sitting at the back of a classroom'),
        ('overt observation', 'observation in which the group knows that the researcher is studying them', 'a researcher openly introduced to a youth club'),
        ('covert observation', 'observation in which the group does not know that it is being studied', 'a researcher posing as a member of a religious group'),
        ('going native', 'becoming so involved with the group being studied that the researcher loses objectivity', 'a researcher adopting the group’s values and defending its actions'),
        ('field notes', 'the written record a researcher makes of observations during or after fieldwork', 'notes written each night after leaving the setting'),
        ('gatekeeper', 'a person who controls access to a group or setting', 'a gang leader who introduces the researcher to members'),
    ],
    'thinkers': [
        ('Whyte', 'participant observation with a trusted key informant can reveal the structure of a community from the inside', 'Interactionism',
         'Whyte’s “Street Corner Society” studied an Italian-American gang in Boston; his key informant “Doc” gave access and explained the group’s norms.',
         'Whyte admitted that he changed the group’s behaviour and became too involved at times.'),
        ('Patrick', 'covert participation can give access to violent gangs that would refuse to be studied openly', 'Interactionism',
         'James Patrick joined a Glasgow gang covertly; he left when he could no longer avoid taking part in violence.',
         'It raised serious ethical and safety issues and he delayed publication for fear of reprisals.'),
        ('Goffman', 'total institutions strip people of their previous identities', 'Interactionism',
         'Goffman’s participant observation as an assistant in a psychiatric hospital (Asylums) showed how patients adapted to institutional life.',
         'It was a single institution in the USA, so findings may not be generalisable.'),
        ('Willis', 'a group of working-class “lads” formed an anti-school counter-culture that prepared them for manual work', 'Neo-Marxism',
         'Willis used participant observation and interviews with 12 boys to study the “lads”’ culture of having a laff and rejecting school.',
         'The small sample of 12 boys in one school cannot be generalised, and Willis may have romanticised them.'),
    ],
    'explain': [
        ('Explain the difference between overt and covert observation.', 'In overt observation the group knows they are being studied and has given consent; in covert observation the researcher’s identity and purpose are hidden, so behaviour is more natural but there is deception.', '1 mark each definition; 1 mark contrast (consent/Hawthorne effect). [3]'),
        ('Explain two problems a researcher might face in getting into, staying in and getting out of a group.', 'Getting in: gaining access and trust, especially through gatekeepers; staying in: risk of going native or being discovered, recording data; getting out: leaving may be difficult or dangerous and relationships end.', '2 marks for each explained problem. [4]'),
        ('Explain why participant observation is said to have high validity.', 'The researcher sees behaviour in its natural setting rather than relying on accounts; can gain verstehen by experiencing the group’s life; can uncover issues not anticipated; especially if covert, avoids the Hawthorne effect.', '1 mark each developed reason up to 3. [3]'),
    ],
    'why': [
        ('ethical problem', 'ethical problems', 'of covert participant observation', ['lack of informed consent', 'deception of participants', 'risk of being involved in crime', 'harm to participants if they are identified', 'danger to the researcher']),
    ],
    'claims': [
        ('Covert observation avoids the Hawthorne effect.', True, 'The group does not know it is being studied, so behaves naturally.'),
        ('Participant observation is usually carried out with large, representative samples.', False, 'It normally involves small groups and cannot easily be generalised.'),
        ('Overt observation raises no ethical issues.', False, 'Issues remain, such as confidentiality and possible harm.'),
    ],
    'ar': ([('Covert observation raises ethical problems.', 'the group has not given informed consent.'),
            ('Participant observation can produce valid data.', 'the researcher observes behaviour in its natural setting.'),
            ('Overt observation may lead to the Hawthorne effect.', 'the group knows it is being studied and may change its behaviour.')],
           ['covert observation requires the informed consent of all participants.', 'participant observation produces highly reliable data because it is easy to repeat.']),
    'scen': ['{person}, a sociology lecturer in {city}, takes a job in a fast-food restaurant without telling colleagues, to study how workers cope with boring work.',
             'A researcher in {city} openly spends six months with a youth gang, after being introduced by one of its leaders.'],
    'views': V5,
    'ctx': [('a religious sect in {city}', {'hidden', 'meaning', 'behaviour'}),
            ('the culture of a police station', {'hidden', 'behaviour', 'meaning'}),
            ('interaction in primary school classrooms', {'young', 'behaviour'})],
    'methods': ['participant observation', 'covert participant observation', 'non-participant observation', 'unstructured interview', 'questionnaire'],
    'source': [dict(text='A researcher worked for eight months as a part-time cleaner in a large hotel in {city} without telling her colleagues she was a sociologist. She found that cleaners helped each other to meet impossible targets and used humour to cope with rude guests. She wrote her notes each evening from memory.',
                    method='covert participant observation', about='workplace culture among hotel cleaners', finds=['cleaners helped each other to meet targets', 'cleaners used humour to cope with rude guests'],
                    persp='Marxism', pview='The cleaners experience exploitation and alienation through impossible targets; their mutual help and humour can be seen as forms of resistance and class solidarity.',
                    claim='covert participant observation is the best way to study workplace culture', pro='The source shows natural behaviour observed over a long period; colleagues did not know they were being studied, avoiding the Hawthorne effect.',
                    con='There was no informed consent; notes written from memory may be inaccurate; one hotel may be untypical; overt observation or interviews avoid deception.', flags={'behaviour', 'hidden'})],
    'essays': [('Explain two reasons why sociologists might choose covert rather than overt participant observation.', 'Access to closed or deviant groups (Patrick); avoids the Hawthorne effect so behaviour is natural; higher validity; groups might refuse an overt researcher.',
                'participant observation is the most valid method for studying social groups',
                'Natural setting; verstehen; sees what people do not just what they say; flexibility; covert version avoids Hawthorne effect (Whyte, Patrick, Goffman).',
                'Going native and researcher bias; Hawthorne effect in overt studies; ethical problems of covert research; small, unrepresentative samples; data depends on the researcher’s interpretation; positivists criticise lack of reliability.')],
}, V5)

c7c = T('Documents, case studies and longitudinal studies')
build(c7c, {
    'research': True,
    'terms': [
        ('personal documents', 'documents written by individuals for their own purposes, such as diaries, letters and social media posts', 'a migrant’s letters home'),
        ('public documents', 'documents produced by organisations such as governments, schools and businesses', 'school inspection reports or parliamentary records'),
        ('historical documents', 'documents from the past that can be used to study earlier societies', 'parish records of births and marriages'),
        ('case study', 'a detailed study of a single example, such as one person, group, institution or event', 'an in-depth study of one school'),
        ('longitudinal study', 'a study of the same group of people over a long period, collecting data at intervals', 'following a group of children from birth to adulthood'),
        ('sample attrition', 'the loss of members of a sample over time in a longitudinal study', 'participants moving away or refusing to continue'),
        ('authenticity', 'whether a document is genuine and what it claims to be', 'checking that a diary was really written by the person named'),
        ('credibility', 'whether a document is believable and free from distortion', 'considering whether a writer exaggerated events'),
    ],
    'thinkers': [
        ('Scott', 'documents should be assessed for authenticity, credibility, representativeness and meaning', 'Interpretivism',
         'Scott’s four criteria help researchers judge whether documents are genuine, believable, typical and correctly understood.',
         'Applying the criteria still depends on the researcher’s interpretation.'),
        ('Thomas and Znaniecki', 'letters written by migrants can reveal how migration changes family and community life', 'Interactionism',
         'Their study “The Polish Peasant in Europe and America” used hundreds of letters between Polish migrants and families back home.',
         'Letters were written for particular readers and may not be representative of all migrants.'),
        ('Laslett', 'historical records show that the nuclear family was common in pre-industrial England', 'Functionalism',
         'Laslett used parish records to show average household size was small (about 4.75) before industrialisation.',
         'Records may be incomplete and say little about relationships within households.'),
    ],
    'explain': [
        ('Explain two problems of using personal documents in sociological research.', 'Authenticity: they may be fake or altered; credibility: writers may exaggerate or present themselves favourably; representativeness: only some people keep or publish documents; meaning: interpretation may be difficult.', '2 marks for each explained problem. [4]'),
        ('Explain one strength and one limitation of longitudinal studies.', 'Strength: they track changes in the same people over time and can help identify causes. Limitation: sample attrition makes the sample unrepresentative over time; they are expensive and slow.', '2 marks for each explained point. [4]'),
        ('Explain why case studies are difficult to generalise from.', 'A single case may be untypical; it reflects particular local circumstances; with no comparison it is hard to know whether findings apply elsewhere.', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why sociologists use historical documents', ['to study societies and events in the past that cannot be observed', 'to compare past and present patterns', 'they are often cheap and easily available', 'they can show how people at the time understood events']),
    ],
    'claims': [
        ('Longitudinal studies follow the same group of people over time.', True, 'This allows researchers to track changes in individuals’ lives.'),
        ('Personal documents are always credible.', False, 'Writers may exaggerate, lie or present a one-sided picture.'),
        ('A case study of one school can be generalised to all schools.', False, 'One case may be untypical; findings need comparison with other cases.'),
    ],
    'ar': ([('Longitudinal studies may become unrepresentative.', 'sample attrition means some types of people drop out more than others.'),
            ('Historical documents are useful to sociologists.', 'they provide evidence about societies that can no longer be observed directly.')],
           ['case studies are designed to produce statistically representative findings.', 'personal documents are produced by government departments.']),
    'scen': ['A research team in {city} has followed 5,000 children born in the same week since 2000, interviewing them every few years.',
             '{person} studies hundreds of social media posts written by young climate activists in {city} to understand why they joined the movement.'],
    'views': V5,
    'ctx': [('how children’s family circumstances affect their later lives', {'change', 'young', 'large'}),
            ('family life in the nineteenth century', {'past', 'meaning'}),
            ('the experiences of a single community after a factory closure', {'change', 'meaning'})],
    'methods': ['personal documents', 'longitudinal study', 'case study', 'questionnaire', 'unstructured interview', 'official statistics'],
    'essays': [('Explain two strengths of using personal documents in sociological research.', 'Insight into meanings and feelings in people’s own words; evidence about the past; produced without researcher influence; cheap and accessible; can supplement other methods.',
                'longitudinal studies are the most useful way to study social change',
                'Track the same individuals over time; show causes and sequences; combine quantitative and qualitative data; avoid comparing different samples.',
                'Attrition; very costly and slow; Hawthorne effect from repeated study; other methods (official statistics, documents) show long-term change more cheaply; findings may be outdated when published.')],
}, V5)


@c7c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c7c_attr(r, D):
    start = r.choice([2000, 2400, 3000, 4000, 5000, 6000, 8000, 10000])
    w = [100]
    for _ in range(3):
        w.append(w[-1] - r.choice([5, 8, 10, 12, 15]))
    nums = [start * x // 100 for x in w]
    if any(start * x % 100 for x in w):
        return None
    yrs = r.choice([(0, 5, 10, 15), (2005, 2010, 2015, 2020), (1, 7, 14, 21)])
    lab = (lambda y: f'age {y}') if yrs[0] in (0, 1) else (lambda y: str(y))
    d = ctxd(r)
    intro = f'A longitudinal study in {d["city"]} began with {start:,} participants. The numbers still taking part were: ' + ', '.join(f'{lab(y)}: {n_:,}' for y, n_ in zip(yrs, nums)) + '.'
    lost = start - nums[-1]
    pct = 100 * lost / start
    if D <= 1:
        ans = f'{_pc(pct)}%'
        ds = [f'{_pc(100 - pct)}%', f'{_pc(100 * (nums[2] - nums[3]) / nums[2])}%', f'{lost // 10}%', f'{_pc(pct / 3)}%']
        opts, a = mcq(r, ans, [x for x in ds if x != ans])
        return {'stem': f'{intro} What percentage of the original sample had been lost by the final wave?', 'options': opts, 'answer': a, 'key': f'({start:,} − {nums[-1]:,}) ÷ {start:,} × 100 = {_pc(pct)}%. [1]', 'marks': 1}
    parts = [('Calculate the percentage of the original sample lost by the final wave.', f'({start:,} − {nums[-1]:,}) ÷ {start:,} × 100 = {_pc(pct)}%.', '1 mark method; 1 mark answer. [2]'),
             ('Identify the period in which the largest number of participants dropped out.', (lambda i: f'Between {lab(yrs[i])} and {lab(yrs[i + 1])} ({nums[i] - nums[i + 1]:,} participants).')(max(range(3), key=lambda i: nums[i] - nums[i + 1])),
              '1 mark correct period with figure. [1]') if len({nums[i] - nums[i + 1] for i in range(3)}) == 3 else None,
             ('Explain why sample attrition may reduce the representativeness of the study.', 'Those who drop out may differ from those who stay (e.g. poorer families who move more often, or people with problems), so the remaining sample becomes biased and findings may not apply to the original population.', '1 mark: drop-outs not random; 1 mark: bias/representativeness consequence. [2]'),
             ('Suggest two ways the researchers could reduce sample attrition.', 'Keep in regular contact and update addresses; offer incentives; make participation easy (online options, short questionnaires); build trust and explain the value of the study.', '1 mark each. [2]'),
             ('Explain one advantage of a longitudinal study over a single survey at one point in time.', 'It shows how the same individuals change over time, so the order of events and possible causes can be identified, which a one-off snapshot cannot do.', '1 mark: same individuals over time; 1 mark: causes/sequence. [2]')]
    parts = [p for p in parts if p]
    if D == 2:
        sel = parts[:2]
    elif D == 3:
        sel = [parts[0]] + r.sample(parts[1:], 2)
    else:
        sel = parts[:4] if D == 4 else parts
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


c7d = T('Triangulation and mixed-methods research')
build(c7d, {
    'research': True,
    'terms': [
        ('triangulation', 'using two or more methods or sources to check the accuracy of findings', 'comparing interview data with observation of the same group'),
        ('methodological pluralism', 'using a variety of methods in one study so that each provides different kinds of data', 'combining a national survey with in-depth case studies'),
        ('mixed methods', 'research that combines quantitative and qualitative methods', 'a questionnaire followed by unstructured interviews with some respondents'),
        ('data triangulation', 'using data from different sources, times or places to check findings', 'comparing police records with victim surveys'),
        ('investigator triangulation', 'using more than one researcher to collect or analyse data to reduce individual bias', 'two observers coding the same classroom interaction'),
        ('realism', 'a view of science and research that combines a concern with underlying structures and with people’s meanings', 'studying both class structures and how people experience class'),
    ],
    'thinkers': [
        ('Denzin', 'triangulation of data, investigators, theories and methods improves the quality of research', 'Interactionism',
         'Denzin identified four types of triangulation, arguing that combining them reduces the bias of any single approach.',
         'Critics argue methods based on different assumptions about reality cannot simply be combined.'),
        ('Hey', 'girls’ friendships can be studied through a combination of observation and their own notes', 'Liberal feminism',
         'Valerie Hey combined observation in schools with analysis of notes passed between girls to study their friendships.',
         'The notes were obtained without full consent of all writers, raising ethical issues.'),
    ],
    'explain': [
        ('Explain what is meant by triangulation and why sociologists use it.', 'Triangulation means using more than one method or source to check findings; it increases validity and reliability because weaknesses of one method are offset by strengths of another; it gives a fuller picture.', '1 mark definition; 1 mark validity/cross-checking; 1 mark fuller picture. [3]'),
        ('Explain two problems of using mixed methods in sociological research.', 'More time and cost; requires skills in different methods; methods may produce conflicting results that are hard to reconcile; methods rest on different theoretical assumptions (positivist vs interpretivist).', '2 marks for each explained problem. [4]'),
    ],
    'why': [
        ('way', 'ways', 'in which mixed methods can improve sociological research', ['quantitative data shows patterns while qualitative data explains them', 'triangulation checks validity', 'qualitative pilot work can improve questionnaire design', 'it combines reliability and validity']),
    ],
    'claims': [
        ('Triangulation means using three different methods.', False, 'It means using more than one method or source to check findings; it need not be three.'),
        ('Mixed methods can combine the strengths of positivist and interpretivist approaches.', True, 'Quantitative data gives patterns and reliability; qualitative data gives meanings and validity.'),
    ],
    'ar': ([('Triangulation can increase the validity of research.', 'findings from one method can be checked against another.'),
            ('Mixed methods research is often more expensive.', 'it requires more time and a wider range of research skills.')],
           ['triangulation always produces identical results from each method.', 'positivists reject all forms of quantitative data.']),
    'scen': ['A research team in {city} sends a questionnaire on housework to 1,000 couples and then carries out unstructured interviews with 30 of them.',
             '{woman} finds that interview data about how often teachers praise pupils does not match what she observed in their lessons.'],
    'views': V5,
    'ctx': [('the domestic division of labour', {'behaviour', 'private', 'large', 'meaning'}),
            ('reasons for truancy from school', {'young', 'meaning', 'large'})],
    'essays': [('Explain two reasons why sociologists use triangulation.', 'To check validity; to combine reliability with validity; to give a fuller picture; to reduce researcher bias; qualitative work can generate hypotheses for quantitative testing.',
                'using mixed methods always produces better sociological research than using a single method',
                'Combines patterns with meanings; triangulation checks findings; methodological pluralism is common in modern research; realists support combining approaches.',
                'Methods rest on incompatible theoretical assumptions; conflicting results; extra cost and time; a single well-chosen method may suit the research question better.')],
}, V5)

CHAPTERS[7] = [c7a, c7b, c7c, c7d]


# ============================================================== CHAPTER 8: Family and social change

V8 = {
    'Functionalism': 'the family performs vital functions for society and its members, such as primary socialisation and the stabilisation of adult personalities; changes in family structure reflect the needs of the economy, as the isolated nuclear family fits industrial society (Parsons, Murdock).',
    'Marxism': 'the family serves capitalism: it passes on private property, socialises children into accepting hierarchy, and acts as a unit of consumption; family life reflects class inequality (Engels, Zaretsky).',
    'Radical feminism': 'the family is a patriarchal institution in which men benefit from women’s unpaid domestic and emotional labour and domestic violence maintains male control (Delphy and Leonard).',
    'New Right': 'the traditional nuclear family with married parents and a male breadwinner is the best environment for raising children; the growth of lone-parent families and cohabitation threatens social order and creates welfare dependency (Murray).',
    'Postmodernism': 'family life is now diverse and fluid; individuals choose from many family types and relationships, so there is no longer a single “normal” family (Stacey, Giddens).',
}

c8a = T('Defining the family and household: nuclear, extended, lone-parent and reconstituted')
build(c8a, {
    'terms': [
        ('family', 'a group of people related by blood, marriage, civil partnership or adoption, often (but not always) living together', 'parents and their children'),
        ('household', 'one person living alone, or a group of people who live at the same address and share living facilities', 'four students sharing a flat'),
        ('nuclear family', 'a family of two generations: parents (or a parent) and their dependent children', 'a married couple living with their two children'),
        ('extended family', 'a family that includes relatives beyond the nuclear family, such as grandparents, aunts or cousins', 'grandparents, parents and children living together'),
        ('lone-parent family', 'a family made up of one parent and their dependent children', 'a divorced mother raising two children alone'),
        ('reconstituted family', 'a family in which one or both partners have children from a previous relationship', 'a couple living with the wife’s children from her first marriage'),
        ('beanpole family', 'a multi-generational family that is long and thin, with few relatives in each generation', 'four generations alive but each with one or two children'),
        ('household of choice', 'a household formed by people who choose to live together, often based on friendship rather than kinship', 'friends who share a home and support each other'),
    ],
    'thinkers': [
        ('Murdock', 'the nuclear family is universal because it performs four essential functions', 'Functionalism',
         'Murdock’s study of 250 societies identified sexual, reproductive, economic and educational functions of the family.',
         'Examples such as the Nayar of southern India and kibbutzim in Israel challenge the claim of universality.'),
        ('Gough', 'among the Nayar, the nuclear family was not the basic unit of family life', 'Interactionism',
         'Gough described how Nayar women had several visiting husbands and children were raised in the mother’s matrilineal household.',
         'Some argue the Nayar case is a historical exception.'),
        ('Rapoport and Rapoport', 'family diversity takes five main forms: organisational, cultural, class, life-stage and cohort', 'Postmodernism',
         'The Rapoports argued diversity is now the norm and families vary in structure, cultural background, class and stage of life.',
         'New Right thinkers argue diversity reflects family breakdown rather than positive choice.'),
    ],
    'explain': [
        ('Explain the difference between a family and a household, using an example.', 'A family is based on kinship (blood, marriage or adoption) and members need not live together; a household is based on shared residence and may not involve kinship, e.g. students sharing a flat are a household but not a family.', '1 mark each definition; 1 mark example. [3]'),
        ('Explain why it is difficult to define “the family”.', 'There is great diversity of family types; families vary between cultures (e.g. the Nayar); definitions based on the nuclear family exclude many people; same-sex, chosen and transnational families challenge traditional definitions.', '1 mark each developed point up to 3. [3]'),
        ('Explain two differences between nuclear and extended families.', 'Size: two generations vs. three or more or wider kin; functions: extended families share care and economic support; residence: extended may live together or nearby; nuclear more geographically mobile.', '2 marks for each explained difference. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why the number of one-person households has increased in many societies', ['people are marrying later or not at all', 'rising divorce and separation', 'an ageing population with more widowed older people', 'greater affluence allows people to live alone', 'individualisation and choice']),
    ],
    'claims': [
        ('A household is always made up of family members.', False, 'A household is defined by shared residence and can include unrelated people.'),
        ('Murdock claimed the nuclear family is found in every society.', True, 'He argued it is universal because it meets four basic needs.'),
        ('Reconstituted families are formed after separation, divorce or the death of a partner.', True, 'They involve a couple where at least one partner has children from a previous relationship.'),
    ],
    'ar': ([('The Nayar challenge Murdock’s view of the family.', 'children were raised without a nuclear family based on a resident father.'),
            ('One-person households have increased.', 'people are living longer and marrying later.'),
            ('Reconstituted families have become more common.', 'divorce and remarriage rates have risen in many societies.')],
           ['a household must contain at least two generations.', 'Murdock argued the family has no economic function.']),
    'scen': ['{person}, who lives in {city}, shares a flat with three friends; they cook together, share bills and spend holidays together.',
             'In {city}, a widowed grandmother moves in with her son, his wife and their two children.',
             '{woman} lives with her new partner, her two children from her first marriage and his daughter, who stays every other weekend.'],
    'views': {'Functionalism': 'the nuclear family is universal and performs essential functions such as reproduction and socialisation (Murdock); other arrangements are seen as variations on, or less functional than, this model.',
              'New Right': 'the “proper” family is a married heterosexual couple with children; other households represent family breakdown that harms children and society.',
              'Personal life perspective': 'what counts as family should be defined by people themselves: friends, step-relatives and others who give support and meaning can be “family” (Smart, Weeks’s chosen families).',
              'Postmodernism': 'there is no single family type; households are diverse and fluid, formed by choice and changing over the life course (Stacey).'},
    'ctx': [('family structures in {city}', {'large', 'change'}),
            ('how children experience life in reconstituted families', {'young', 'private', 'meaning'}),
            ('the meaning of “family” to young adults living with friends', {'meaning'})],
    'data': [dict(what='household types', pop='households', rows=['Couple with dependent children', 'One-person households', 'Lone parent with dependent children'], cols=('1995', '2025'), nocount=True,
                  base=[(32, 38), (22, 28), (6, 9)], delta=[(-10, -4), (3, 8), (1, 4)], label='percentage of all households',
                  leads=['Census data for {city} show the following household types ({n} households in the sample analysed).', 'The table shows household types in {city}, based on a sample of {n} census records.'],
                  expl=['later marriage, divorce and an ageing population have increased one-person households', 'postmodernists see growing family diversity as the result of individual choice',
                        'the New Right would interpret the rise in lone-parent households as evidence of family breakdown'],
                  method='official statistics', claim='the nuclear family is in decline',
                  counter='Couples with children are still a large group and most people live in a nuclear family at some stage of life (Chester’s neo-conventional family); figures are snapshots and miss the life course.')],
    'essays': [('Explain two reasons why it is difficult to define the family.', 'Diversity of family forms (nuclear, extended, lone-parent, reconstituted, same-sex); cross-cultural variation (the Nayar, kibbutz); differences between family and household; changing legal definitions; families of choice.',
                'the nuclear family is still the dominant family form',
                'Most people live in a nuclear family at some point (Chester); most children are raised by two parents; functionalists see it as best suited to modern society; neo-conventional families with dual earners are common.',
                'Growth of lone-parent, reconstituted, same-sex and one-person households; Rapoports’ five types of diversity; postmodernists (Stacey) see diversity as the norm; cultural and class variation.')],
}, V8)

c8b = T('Functionalist, Marxist and feminist views of the family')
build(c8b, {
    'terms': [
        ('primary socialisation', 'the learning of basic norms, values and language in early childhood, mainly in the family', 'parents teaching children right from wrong'),
        ('stabilisation of adult personalities', 'Parsons’s idea that the family provides emotional support that relieves the stress of adult life', 'a parent relaxing with family after a difficult day at work'),
        ('instrumental role', 'Parsons’s term for the breadwinning role, which he assigned to men', 'a father working full-time to provide for the family'),
        ('expressive role', 'Parsons’s term for the caring, nurturing role, which he assigned to women', 'a mother providing emotional support and childcare'),
        ('unit of consumption', 'the Marxist idea that families buy the goods produced by capitalism, generating profit', 'families buying new technology because of advertising'),
        ('reserve army of labour', 'workers, often women, who can be drawn into paid work when needed and dismissed when not', 'women recruited during wartime and sent home afterwards'),
        ('triple shift', 'the situation in which women do paid work, domestic work and emotional work', 'a mother who works full-time, cooks and supports family members emotionally'),
        ('dark side of the family', 'the harmful aspects of family life, such as abuse, violence and oppression', 'domestic violence and child abuse'),
    ],
    'thinkers': [
        ('Parsons', 'the family retains two basic and irreducible functions: primary socialisation and the stabilisation of adult personalities', 'Functionalism',
         'Parsons argued the isolated nuclear family fits industrial society and has lost other functions to specialist institutions.',
         'Feminists criticise his view of instrumental and expressive roles as justifying gender inequality.'),
        ('Engels', 'the monogamous nuclear family developed to ensure that men could pass on private property to their legitimate heirs', 'Marxism',
         'Engels linked the family’s origin to private property and the control of women’s sexuality by men.',
         'Historical evidence for his account is limited, and the family exists in non-capitalist societies.'),
        ('Zaretsky', 'the family provides an illusion of a private haven from the harsh world of capitalism', 'Marxism',
         'Zaretsky argued the family meets needs that capitalism neglects, which helps capitalism survive, and acts as a unit of consumption.',
         'Functionalists argue the family genuinely benefits its members.'),
        ('Delphy and Leonard', 'the family is a patriarchal and hierarchical institution in which men exploit women’s labour', 'Radical feminism',
         'Delphy and Leonard argued that the family is an economic system in which husbands benefit from wives’ unpaid work.',
         'Critics argue it ignores changes such as women’s employment and more equal relationships.'),
        ('Ansley', 'wives act as “takers of shit”, absorbing the frustration of husbands exploited at work', 'Marxist feminism',
         'Ansley argued the family soaks up men’s anger that might otherwise be directed against capitalism.',
         'It portrays women as passive victims and ignores domestic violence by women or changing roles.'),
    ],
    'explain': [
        ('Explain two functions of the family identified by functionalists.', 'Primary socialisation (Parsons); stabilisation of adult personalities; sexual, reproductive, economic and educational functions (Murdock); emotional support.', '2 marks for each explained function. [4]'),
        ('Explain how Marxists argue that the family benefits capitalism.', 'It passes on private property (Engels); socialises children to accept hierarchy; acts as a unit of consumption generating profit; provides a “haven” that makes exploitation bearable (Zaretsky).', '1 mark each developed point up to 3. [3]'),
        ('Explain one criticism of the functionalist view of the family made by feminists.', 'Functionalists see the family as harmonious and roles as natural; feminists argue it is patriarchal, women do unpaid labour and suffer domestic violence (dark side), and the expressive role confines women.', '1 mark functionalist view; 2 marks explained feminist criticism. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of the functionalist view of the family', ['it ignores the dark side of family life, such as abuse and violence', 'it assumes gender roles are natural, which feminists reject', 'it is based on the white, middle-class American family of the 1950s', 'it ignores family diversity', 'it sees the family as harmonious and ignores conflict']),
    ],
    'claims': [
        ('Parsons argued that the family has lost all its functions.', False, 'He argued it lost some functions but kept two irreducible ones: primary socialisation and the stabilisation of adult personalities.'),
        ('Engels linked the monogamous family to private property.', True, 'He argued monogamy ensured property passed to legitimate heirs.'),
        ('Radical feminists see the family as harmonious and equal.', False, 'They see it as a key site of patriarchal oppression and exploitation.'),
        ('Marxists see the family as a unit of consumption.', True, 'Families buy goods produced by capitalism, generating profit, encouraged by advertising.'),
    ],
    'ar': ([('Marxist feminists argue that the family benefits capitalism.', 'women’s unpaid domestic labour reproduces the workforce at no cost to employers.'),
            ('Parsons saw the nuclear family as suited to industrial society.', 'it is geographically mobile and has handed specialised functions to other institutions.'),
            ('Radical feminists highlight the dark side of the family.', 'domestic violence and abuse are mainly carried out by men against women and children.')],
           ['Engels argued that the family began with the abolition of private property.', 'Parsons assigned the expressive role to men.']),
    'scen': ['In a family in {city}, the father works long hours while the mother looks after the children and the home; she says she has “no time for herself”.',
             'Advertisements in {city} encourage parents to buy the latest gadgets so that their children will “fit in” at school.',
             '{man} comes home exhausted from a stressful factory job and relaxes while his wife prepares dinner and listens to his complaints.'],
    'views': {'Functionalism': V8['Functionalism'], 'Marxism': V8['Marxism'], 'Radical feminism': V8['Radical feminism'],
              'Marxist feminism': 'the family serves both capitalism and patriarchy: women’s unpaid labour reproduces the workforce and absorbs men’s frustration (Benston, Ansley).',
              'Liberal feminism': 'family roles are becoming more equal through changes in law, attitudes and women’s employment, though inequality remains (Somerville).'},
    'ctx': [('how families share emotional support', {'meaning', 'private'}),
            ('the impact of advertising on family spending', {'media', 'behaviour', 'large'}),
            ('the experiences of women doing the triple shift', {'meaning', 'private', 'sensitive'})],
    'source': [dict(text='In a study in {city}, 300 couples completed time-use diaries for one week. Women in full-time work spent an average of 16 hours a week on housework and 10 hours on childcare; men in full-time work spent 8 hours and 6 hours. Women also reported more stress about “keeping the family happy”.',
                    method='personal documents', about='the division of labour in families', finds=['women in full-time work spent more time on housework and childcare than men', 'women reported more stress about keeping the family happy (emotional work)'],
                    persp='Radical feminism', pview='The data show patriarchy in the home: women carry a triple shift of paid work, domestic labour and emotional work, which benefits men (Delphy and Leonard).',
                    claim='the family mainly benefits men', pro='The source shows women doing more domestic and emotional labour even when in full-time work; radical feminists argue men benefit from this exploitation.',
                    con='Functionalists argue the family benefits all members and society; liberal feminists note gradual change; diaries depend on accurate recording; 300 couples in one city may be unrepresentative.', flags={'private', 'behaviour'})],
    'essays': [('Explain two ways in which Marxists see the family as benefiting capitalism.', 'Inheritance of private property (Engels); ideological functions – socialising children into hierarchy; unit of consumption; haven from exploitation (Zaretsky); reproduction of labour power.',
                'the family benefits all its members and society as a whole',
                'Functionalists: primary socialisation, stabilisation of adult personalities (Parsons), Murdock’s four functions; emotional support; New Right sees it as essential to social order.',
                'Marxists: it serves capitalism; feminists: it exploits women and hides violence; the dark side (Leach, Laing); benefits differ by gender, age and class; postmodernists stress diversity.')],
})

c8c = T('Industrialisation and changes in family structure')
build(c8c, {
    'terms': [
        ('industrialisation', 'the process by which an economy changes from being based mainly on agriculture to being based on factories and manufacturing', 'the growth of textile factories in nineteenth-century cities'),
        ('urbanisation', 'the growth in the proportion of a population living in towns and cities', 'rural families moving to cities to find factory work'),
        ('isolated nuclear family', 'Parsons’s term for a nuclear family that is geographically and socially separate from wider kin', 'a family moving across the country for a job'),
        ('geographical mobility', 'the movement of people from one area to another, often for work', 'a family relocating to a new city for a promotion'),
        ('social mobility', 'movement of people up or down the class structure', 'a factory worker’s child becoming a doctor'),
        ('structural differentiation', 'the process by which specialist institutions develop to take over functions once performed by the family', 'schools taking over education and hospitals taking over health care'),
        ('modified extended family', 'a family in which relatives live apart but keep in contact and give help through visits, phone calls and online communication', 'grandparents who help with childcare by video call and visits'),
    ],
    'thinkers': [
        ('Parsons', 'industrialisation led to the isolated nuclear family because it fits the needs of an industrial economy', 'Functionalism',
         'Parsons argued a geographically and socially mobile workforce is needed, so smaller nuclear families replaced extended ones.',
         'Historical research (Laslett, Anderson) challenges the idea that pre-industrial families were mainly extended.'),
        ('Laslett', 'the nuclear family was already common in pre-industrial England', 'Functionalism',
         'Laslett’s analysis of parish records showed average household size of about 4.75, suggesting nuclear families pre-dated industrialisation.',
         'Records may not show how kin outside the household supported each other.'),
        ('Anderson', 'extended families became more common in early industrial towns as a mutual support network', 'Interactionism',
         'Anderson’s study of the 1851 census for Preston found many households included extended kin who helped each other with housing and jobs.',
         'This was one town at one time and may not be typical.'),
        ('Young and Willmott', 'the family developed through stages towards a symmetrical nuclear family', 'Functionalism',
         'Young and Willmott identified pre-industrial, early industrial, symmetrical and (predicted) asymmetrical stages, arguing the family adapted to economic change.',
         'Feminists such as Oakley argue they exaggerated equality in the symmetrical family.'),
    ],
    'explain': [
        ('Explain why Parsons argued that industrialisation led to the isolated nuclear family.', 'Industry needed a geographically mobile workforce, which was easier for small nuclear families; achieved status in work conflicted with ascribed status in extended families; specialist institutions took over functions, so the family specialised in socialisation and personality stabilisation.', '1 mark each developed point up to 3. [3]'),
        ('Explain one piece of evidence that challenges Parsons’s view of family change.', 'Laslett found most pre-industrial households were nuclear (average 4.75 people); Anderson found extended households increased in early industrial Preston; modified extended families remain important today.', '1 mark evidence; 2 marks explaining how it challenges Parsons. [3]'),
        ('Explain what is meant by the modified extended family.', 'A family in which kin live apart, often at a distance, but maintain regular contact and support through visits, phone and internet, and practical and financial help.', '1 mark living apart; 1 mark contact/support. [2]'),
    ],
    'why': [
        ('function', 'functions', 'that the family has lost to other institutions according to functionalists', ['education to schools', 'health care to hospitals and doctors', 'economic production to factories and businesses', 'welfare to the state']),
    ],
    'claims': [
        ('Laslett found that most pre-industrial households were extended.', False, 'He found most were nuclear, with an average size of about 4.75.'),
        ('Parsons argued industrial societies need a geographically mobile workforce.', True, 'He saw the nuclear family as best fitted to this need.'),
        ('Anderson’s study of Preston found extended families helped each other in early industrial towns.', True, 'Kin shared housing and helped each other find work.'),
    ],
    'ar': ([('Parsons saw the nuclear family as suited to industrial society.', 'industrial economies require geographically mobile workers.'),
            ('Laslett challenged the “march of progress” view of family change.', 'his evidence showed nuclear households were common before industrialisation.')],
           ['industrialisation increased the size of families in all societies.', 'Anderson used diaries rather than census data.']),
    'scen': ['In {city}, rapid growth of factories has led many young couples to leave their villages and live far from their parents.',
             '{woman} lives 300 km from her parents in {city} but speaks to them daily by video call and they help pay for her children’s school fees.'],
    'ctx': [('family relationships among migrants from rural areas to {city}', {'meaning', 'change'}),
            ('family structure in the nineteenth century', {'past', 'change'})],
    'data': [dict(what='household size', pop='households', rows=['Households with 1-2 people', 'Households with 3-4 people', 'Households with 5 or more people'], cols=('1970', '2025'), dist=True,
                  base=[(25, 32), (35, 42), (28, 35)], delta=[(15, 25), (-2, 5), (-20, -12)], label='percentage of all households',
                  expl=['industrialisation and urbanisation reduced household size as nuclear families became more common', 'falling birth rates mean fewer children per family',
                        'more people living alone or as couples because of ageing and later marriage'],
                  method='official statistics', claim='industrialisation has led to smaller, nuclear families',
                  counter='Household size does not show contact with wider kin; modified extended families remain important; Laslett shows nuclear households pre-dated industrialisation.')],
    'essays': [('Explain two reasons why family structures change as societies industrialise.', 'Need for geographical mobility (Parsons); structural differentiation; urbanisation; falling birth rates; changing gender roles and women’s employment; the welfare state.',
                'industrialisation led to the isolated nuclear family',
                'Parsons: fit between nuclear family and industry; mobility; achieved status; structural differentiation; Young and Willmott’s symmetrical family.',
                'Laslett: nuclear families common before industrialisation; Anderson: extended families in early industrial towns; Willmott: modified extended families; diversity today; changes vary by culture.')],
}, V8)


@c8c.add('C3', (1, 2, 3, 4), 'numerical')
def c8c_mean(r, D):
    sizes = [1, 2, 3, 4, 5, 6]
    for _ in range(40):
        f = [r.randint(2, 12) for _ in sizes]
        n = sum(f)
        tot = sum(s_ * c for s_, c in zip(sizes, f))
        if n in (20, 25, 30, 40, 50) and (tot * 100) % n == 0:
            break
    else:
        return None
    mean = tot / n
    d = ctxd(r)
    intro = f'{d["person"]} studied {n} households from parish records of a village near {d["city"]} in the 1790s. Number of people in household (number of households): ' + ', '.join(f'{s_} ({c})' for s_, c in zip(sizes, f)) + '.'
    if D <= 1:
        ans = _pc(mean, 2)
        ds = [_pc(tot / len(sizes), 2), _pc(mean + 1, 2), _pc(n / len(sizes), 2), str(sizes[f.index(max(f))]) if str(sizes[f.index(max(f))]) != ans else _pc(mean - 0.5, 2)]
        opts, a = mcq(r, ans, [x for x in ds if x != ans])
        return {'stem': f'{intro} What is the mean household size?', 'options': opts, 'answer': a, 'key': f'Total people {tot} ÷ {n} households = {ans}. [1]', 'marks': 1}
    parts = [('Calculate the mean household size.', f'Total people = {" + ".join(f"{s_}×{c}" for s_, c in zip(sizes, f))} = {tot}; {tot} ÷ {n} = {_pc(mean, 2)}.', f'1 mark total of {tot}; 1 mark {_pc(mean, 2)}. [2]'),
             ('Calculate the percentage of households with five or more people.', f'({f[4]} + {f[5]}) ÷ {n} × 100 = {_pc(100 * (f[4] + f[5]) / n)}%.', '1 mark method; 1 mark answer. [2]'),
             ('Explain how evidence like this was used by Laslett to challenge Parsons’s view of family change.', 'Small average household sizes in pre-industrial records suggest nuclear households were common before industrialisation, contradicting the idea that industrialisation replaced extended families with nuclear ones.', '1 mark: small households/nuclear before industrialisation; 1 mark: challenge to Parsons. [2]'),
             ('Explain one limitation of using parish records to study family life.', 'They show who lived in a household but not relationships, roles or contact with kin living nearby; records may be incomplete or inaccurate; one village may be untypical.', '1 mark identifying; 1 mark explaining. [2]')]
    sel = parts[:2] if D == 2 else (parts[:3] if D == 3 else parts)
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


c8d = T('Family diversity and the postmodern view of the family')
build(c8d, {
    'terms': [
        ('family diversity', 'the existence of a wide variety of family types and household arrangements in a society', 'nuclear, lone-parent, same-sex and reconstituted families living in the same street'),
        ('cereal packet family', 'the stereotypical image of the nuclear family (married parents, two children, male breadwinner) often presented in advertising', 'advertisements showing a smiling mother serving breakfast to a husband and two children'),
        ('neo-conventional family', 'Chester’s term for a dual-earner nuclear family in which both spouses go out to work', 'a married couple both in full-time jobs raising children'),
        ('individualisation', 'the process by which people become freer from traditional norms and make their own choices about relationships', 'choosing whether to marry, cohabit or live alone'),
        ('pure relationship', 'Giddens’s term for a relationship entered into for its own sake and lasting only as long as it satisfies both partners', 'a couple who stay together only while both are happy'),
        ('divorce-extended family', 'Stacey’s term for a family whose members are connected by divorce rather than marriage', 'former in-laws who remain close after divorce'),
        ('personal life perspective', 'an approach that studies the relationships people themselves see as important, including non-kin and pets', 'a person who regards a close friend as “family”'),
    ],
    'thinkers': [
        ('Rapoport and Rapoport', 'family diversity has five dimensions: organisational, cultural, class, life-stage and cohort', 'Postmodernism',
         'The Rapoports argued diversity is a central feature of family life and should be accepted.',
         'Chester argued the extent of diversity is exaggerated.'),
        ('Chester', 'the neo-conventional family remains the norm, and most people live in a nuclear family at some point', 'Functionalism',
         'Chester argued the main change has been from a male-breadwinner family to a dual-earner one; diversity often reflects life-cycle stages.',
         'Critics argue increasing numbers never live in a nuclear family and diversity is real.'),
        ('Stacey', 'postmodern families are diverse and women have been the main agents of change in creating new family forms', 'Postmodernism',
         'Stacey’s research in Silicon Valley found women creating new family types, such as the divorce-extended family.',
         'Her study was small and based in one region of the USA.'),
        ('Giddens', 'relationships have been transformed into “pure relationships” based on choice and emotional satisfaction', 'Late modernity',
         'Giddens argued contraception and women’s independence created plastic sexuality and more equal, democratic relationships.',
         'Critics argue he exaggerates choice and ignores continuing inequality and constraint.'),
        ('Murray', 'the growth of lone-parent families and welfare dependency undermines the traditional family', 'New Right',
         'Murray argued that generous welfare benefits create a “perverse incentive” for lone parenthood and an underclass.',
         'Critics argue benefits are not generous enough to encourage lone parenthood and that poverty, not family structure, is the problem.'),
    ],
    'explain': [
        ('Explain two types of family diversity identified by the Rapoports.', 'Organisational (differences in structure and roles, e.g. dual-earner or reconstituted); cultural (ethnic and religious differences); class (differences in resources and parenting); life-stage (families change over the life cycle); cohort (effects of the historical period).', '2 marks for each explained type. [4]'),
        ('Explain the New Right view of family diversity.', 'The New Right sees the traditional married nuclear family as the best for children and society; diversity such as lone parenthood is seen as family breakdown linked to welfare dependency, crime and poor socialisation (Murray).', '1 mark each developed point up to 3. [3]'),
        ('Explain what postmodernists mean when they say there is no longer a typical family.', 'Families are diverse, fluid and chosen; people move through many family types; individualisation means relationships are negotiated; no single model is dominant or “normal” (Stacey).', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'for increasing family diversity', ['rising divorce and remarriage', 'growing acceptance of cohabitation and same-sex relationships', 'secularisation', 'women’s economic independence', 'migration bringing different cultural family patterns']),
    ],
    'claims': [
        ('The New Right welcomes family diversity as a sign of freedom.', False, 'The New Right sees diversity as family breakdown and favours the traditional married nuclear family.'),
        ('Chester argued that the neo-conventional family is still the norm.', True, 'He saw the dual-earner nuclear family as the dominant form.'),
        ('Giddens argued that relationships have become based more on choice.', True, 'His idea of the pure relationship emphasises satisfaction and choice.'),
    ],
    'ar': ([('Postmodernists argue there is no typical family.', 'individuals choose and negotiate their own family arrangements.'),
            ('The New Right is critical of lone-parent families.', 'it argues children need both a male and a female role model.')],
           ['Chester argued that the nuclear family has disappeared.', 'the Rapoports argued that family diversity is declining.']),
    'scen': ['In one street in {city} there are a same-sex couple raising adopted children, a lone father, a three-generation family and a couple who live apart by choice.',
             '{woman} says that her closest “family” are two friends she met at university and her dog.'],
    'ctx': [('the experiences of children in lone-parent families', {'young', 'private', 'meaning'}),
            ('how people define who counts as “family”', {'meaning'}),
            ('changes in family types over thirty years', {'change', 'large'})],
    'data': [dict(what='how children live', pop='dependent children', rows=['With married parents', 'With cohabiting parents', 'With a lone parent'], cols=('1995', '2025'), dist=True,
                  base=[(70, 78), (8, 12), (14, 20)], delta=[(-15, -8), (5, 10), (1, 5)], label='percentage of dependent children living',
                  leads=['Official data for {city} show where dependent children live, based on a sample of {n} children.', 'The table shows the family types in which {n} dependent children in {city} were living.'],
                  expl=['secularisation and changing attitudes have made cohabitation acceptable', 'rising divorce and separation increase lone-parent families',
                        'postmodernists see this as increasing family diversity and choice'],
                  method='official statistics', claim='family diversity is increasing',
                  counter='Most children still live with two parents, often married; Chester argues diversity is exaggerated; cohabiting couples often marry later.')],
    'essays': [('Explain two reasons for increasing family diversity.', 'Divorce and remarriage (reconstituted families); cohabitation and secularisation; same-sex partnerships and changing law; migration and cultural diversity; individualisation and choice (Giddens, Beck).',
                'family diversity is a positive development for society',
                'Postmodernists and the Rapoports see diversity as reflecting choice and freedom; feminists welcome escape from patriarchal families; Giddens’s democratic, pure relationships; acceptance of same-sex families.',
                'New Right (Murray) links diversity to welfare dependency and poor socialisation; children may suffer from family breakdown; Chester argues diversity is exaggerated; diversity may reflect poverty rather than choice.')],
}, V8)

CHAPTERS[8] = [c8a, c8b, c8c, c8d]


# ============================================================== CHAPTER 9: Family roles and relationships

c9a = T('Conjugal roles and the domestic division of labour')
build(c9a, {
    'terms': [
        ('conjugal roles', 'the roles played by husbands and wives (or partners) within a marriage or relationship', 'who earns, cooks, cleans and cares for children'),
        ('segregated conjugal roles', 'roles in which partners have separate, clearly different tasks and leisure', 'a male breadwinner and a female housewife with separate friends'),
        ('joint conjugal roles', 'roles in which partners share tasks, decision-making and leisure', 'a couple who share cooking and childcare and socialise together'),
        ('domestic division of labour', 'the way housework, childcare and other domestic tasks are divided between members of a household', 'the woman doing most of the cooking while the man does repairs'),
        ('symmetrical family', 'Young and Willmott’s term for a family in which partners’ roles are similar, though not identical', 'both partners working and sharing housework'),
        ('dual burden', 'the situation in which women are responsible for both paid work and most domestic work', 'a full-time teacher who also does most of the housework'),
        ('emotion work', 'the work of managing the feelings of family members and maintaining relationships', 'remembering birthdays and comforting upset children'),
        ('commercialisation of housework', 'the replacement of domestic tasks by goods and services bought on the market', 'buying ready meals and paying for cleaners'),
    ],
    'thinkers': [
        ('Bott', 'conjugal roles can be classified as segregated or joint', 'Interactionism',
         'Bott’s study of London couples related segregated roles to close-knit social networks and joint roles to loose-knit networks.',
         'The categories are broad and hard to measure precisely.'),
        ('Young and Willmott', 'the family is becoming more symmetrical as roles become more similar', 'Functionalism',
         'They argued women working, geographical mobility, new technology and higher living standards led to more joint roles.',
         'Oakley argued their evidence was weak: helping once a week counted as sharing.'),
        ('Oakley', 'there is little evidence of symmetry: housework and childcare remain mainly women’s responsibility', 'Liberal feminism',
         'Oakley’s interviews with housewives found only 15% of husbands had high participation in housework and 25% in childcare.',
         'Her sample of 40 London housewives was small, and roles have changed since the 1970s.'),
        ('Duncombe and Marsden', 'women perform a triple shift of paid work, domestic work and emotion work', 'Radical feminism',
         'Duncombe and Marsden found women did most of the emotional work of maintaining family relationships.',
         'Some argue men also do emotional work that is less visible.'),
        ('Gershuny', 'women who work full-time do less housework, leading to “lagged adaptation”', 'Liberal feminism',
         'Gershuny’s time-use data showed men gradually doing more domestic work as women’s employment increased, reflecting changing values.',
         'Change is slow and women still do more overall.'),
    ],
    'explain': [
        ('Explain the difference between joint and segregated conjugal roles, using an example of each.', 'Segregated roles: separate tasks and leisure, e.g. man as breadwinner and woman as housewife; joint roles: shared tasks and leisure, e.g. both partners cooking and caring for children and socialising together.', '1 mark each definition; 1 mark each example. [4]'),
        ('Explain two reasons why the domestic division of labour may have become more equal.', 'More women in paid work (Gershuny’s lagged adaptation); changing attitudes and gender norms; commercialisation of housework; men spending more time at home; legislation such as shared parental leave.', '2 marks for each explained reason. [4]'),
        ('Explain why measuring the domestic division of labour is difficult.', 'People may exaggerate their contribution (social desirability); “helping” may be counted as sharing (Oakley’s criticism of Young and Willmott); tasks differ in time and unpleasantness; emotion work is hard to measure; diaries and questionnaires give different results.', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why women still do more housework than men in many families', ['gender socialisation teaches that domestic work is women’s responsibility', 'men usually earn more, so women are expected to reduce paid work', 'patriarchal ideology and male power in the home', 'workplace cultures expect men to work long hours', 'women do more emotion work']),
    ],
    'claims': [
        ('Young and Willmott found that conjugal roles were becoming more joint.', True, 'They described the symmetrical family, in which roles are more similar.'),
        ('Oakley agreed that most families were fully symmetrical.', False, 'She argued there was little evidence of symmetry and Young and Willmott exaggerated men’s contribution.'),
        ('Time-use diaries can give a more accurate picture of housework than interviews.', True, 'They record activities as they happen, reducing memory errors and exaggeration, though they rely on honest recording.'),
    ],
    'ar': ([('Feminists criticise the idea of the symmetrical family.', 'women still do most of the housework, childcare and emotion work.'),
            ('Housework has become more commercialised.', 'many families now buy goods and services such as ready meals and cleaning.'),
            ('Gershuny identified “lagged adaptation”.', 'men’s domestic contribution increases slowly after women enter paid work.')],
           ['Bott argued that conjugal roles were always joint.', 'Oakley found that most husbands did as much housework as their wives.']),
    'scen': ['{woman} and her husband both work full-time in {city}; she does the cooking, cleaning and organises the children’s activities, while he does “jobs around the house” at weekends.',
             'A couple in {city} split all housework equally using a shared app, and both work part-time to share childcare.'],
    'views': {'Functionalism': 'roles have become more joint and symmetrical as the family adapts to women’s employment; complementary roles help the family function (Young and Willmott, Parsons).',
              'Liberal feminism': 'there has been gradual progress towards equality, as men do more domestic work (Gershuny’s lagged adaptation), but further change in attitudes and policies is needed.',
              'Radical feminism': 'little has changed: women still do most domestic and emotional work, a triple shift that benefits men under patriarchy (Duncombe and Marsden, Delphy and Leonard).'},
    'ctx': [('the division of housework in dual-earner couples in {city}', {'behaviour', 'private', 'large'}),
            ('who does the emotion work in families', {'meaning', 'private'})],
    'methods': ['questionnaire', 'structured interview', 'unstructured interview', 'semi-structured interview', 'personal documents', 'non-participant observation'],
    'data': [dict(what='the domestic division of labour', pop='dual-earner couples', rows=['Cooking', 'Cleaning', 'Childcare'], cols=('Men', 'Women'), cmp=True, unit=' h', uname='hours', nocount=True,
                  base=[(3, 6), (2, 4), (4, 8)], delta=[(3, 7), (3, 6), (3, 8)], label='average hours per week spent on each task',
                  leads=['Time-use diaries kept by {n} dual-earner couples in {city} produced the following data.', 'A study of {n} dual-earner couples in {city} recorded the average weekly hours spent on domestic tasks.'],
                  expl=['gender socialisation leads women to take responsibility for domestic tasks', 'radical feminists argue men benefit from women’s unpaid labour',
                        'men in dual-earner couples are doing more than in the past (lagged adaptation) but still less than women'],
                  method='personal documents', claim='conjugal roles have become symmetrical',
                  counter='Women still do more of every task in the table; diaries may be completed inaccurately; tasks such as emotion work are not shown.')],
    'source': [dict(text='A study in {city} used questionnaires with 600 couples. 72% of men said they “shared housework equally” with their partner, but only 41% of women in the same couples agreed. Couples where the woman earned more than the man were most likely to report sharing.',
                    method='questionnaire', about='conjugal roles', finds=['72% of men but only 41% of women said housework was shared equally', 'couples where the woman earned more were most likely to report sharing'],
                    persp='Liberal feminism', pview='The findings suggest gradual change (especially where women earn more) but also that men overestimate their contribution; inequality remains and more change in attitudes is needed.',
                    claim='the domestic division of labour is now equal in most couples', pro='Many respondents report sharing, and Young and Willmott and Gershuny suggest roles are becoming more joint, especially where women have economic power.',
                    con='The gap between men’s and women’s answers suggests social desirability and lack of validity; feminist studies (Oakley, Duncombe and Marsden) show women still do more, including emotion work.', flags={'behaviour', 'private'})],
    'essays': [('Explain two reasons why conjugal roles may have become more joint.', 'Women’s employment and income (resources theory); changing gender norms; commercialisation of housework; new technology; geographical mobility and privatised families (Young and Willmott); legal changes such as parental leave.',
                'conjugal roles in modern families are now equal',
                'Young and Willmott’s symmetrical family; Gershuny’s lagged adaptation; more dual-earner couples; men more involved in childcare; commercialisation of housework.',
                'Oakley and other feminists show women still do more; the dual burden and triple shift; emotion work (Duncombe and Marsden); decision-making power still lies with men; measurement problems.')],
}, V8)

c9b = T('Power, decision-making and domestic violence in relationships')
build(c9b, {
    'terms': [
        ('domestic violence', 'physical, emotional, sexual or financial abuse between partners or family members', 'a partner repeatedly hitting or controlling the other'),
        ('coercive control', 'a pattern of controlling behaviour, such as isolation, threats and monitoring, used to dominate a partner', 'a partner checking the other’s phone and restricting their money'),
        ('pooling', 'a way of managing money in which both partners have access to income and take joint responsibility for spending', 'a joint bank account'),
        ('allowance system', 'a way of managing money in which one partner (usually the man) gives the other an allowance for household spending', 'a husband giving his wife a weekly amount for food'),
        ('resource theory', 'the view that the partner with greater resources, such as income, has more power in decision-making', 'the higher earner deciding major purchases'),
        ('dark figure of domestic violence', 'domestic violence that is not reported to or recorded by the authorities', 'abuse hidden because victims fear reprisals'),
    ],
    'thinkers': [
        ('Pahl and Vogler', 'there has been a move towards pooling money, but men still usually make the major financial decisions', 'Liberal feminism',
         'Pahl and Vogler identified allowance and pooling systems; even where money was pooled, men had more control over big decisions.',
         'Couples’ own accounts may not reflect how decisions are really made.'),
        ('Edgell', 'very important decisions in professional families were usually taken by husbands', 'Radical feminism',
         'Edgell classified decisions as very important (e.g. moving house), important and less important; men dominated the first.',
         'His study was of middle-class couples in the 1970s.'),
        ('Dobash and Dobash', 'domestic violence is linked to men’s attempts to assert authority over their wives', 'Radical feminism',
         'They found violent incidents were often set off by what husbands saw as challenges to their authority, such as questioning about money.',
         'Their sample of women in refuges may not represent all domestic violence.'),
        ('Wilkinson', 'domestic violence is linked to stress caused by social inequality', 'Marxism',
         'Wilkinson argued that low income, poor housing and lack of status create stress that reduces the quality of relationships and increases violence.',
         'It cannot explain why most low-income men are not violent or why violence occurs in all classes.'),
    ],
    'explain': [
        ('Explain why official statistics may underestimate domestic violence.', 'Victims may not report it because of fear, shame or financial dependence; they may not see it as a crime; police may not record it; it happens in private; coercive control is hard to prove.', '1 mark each developed reason up to 3. [3]'),
        ('Explain the radical feminist explanation of domestic violence.', 'Domestic violence is a result of patriarchy: men use violence and the threat of violence to control women; it is widespread and reflects men’s power in the family and society (Dobash and Dobash).', '1 mark patriarchy; 1 mark control/power; 1 mark evidence or study. [3]'),
        ('Explain two ways in which power may be unequal in relationships.', 'Control of money (allowance system; Pahl and Vogler); major decisions made by men (Edgell); domestic violence and coercive control; unequal leisure time; career decisions prioritising men’s jobs.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why victims of domestic violence may not report it', ['fear of further violence', 'financial dependence on the abuser', 'shame or embarrassment', 'concern for children', 'belief that the police will not help']),
    ],
    'claims': [
        ('Domestic violence only occurs in working-class families.', False, 'It occurs across all social classes, though stress linked to inequality may increase the risk.'),
        ('Pahl and Vogler found that pooling of money has increased.', True, 'But men still tended to control major financial decisions.'),
        ('Radical feminists see domestic violence as a result of individual psychological problems.', False, 'They see it as a product of patriarchal power across society.'),
    ],
    'ar': ([('Much domestic violence is not recorded in official statistics.', 'victims often do not report it and police may not record it.'),
            ('Resource theory links power to income.', 'the partner who earns more often has more say in major decisions.')],
           ['Edgell found wives made most very important decisions.', 'domestic violence is always physical.']),
    'scen': ['{man} earns twice as much as his wife in {city} and insists on deciding where the family goes on holiday and which school the children attend.',
             'A woman in {city} says her partner checks her phone, controls all the money and stops her seeing her friends, although he has never hit her.'],
    'views': {'Radical feminism': 'violence and control are expressions of patriarchy: men use money, decision-making and violence to maintain power over women (Dobash and Dobash, Edgell).',
              'Marxism': 'inequality and stress caused by low income and insecure work damage relationships and increase violence (Wilkinson); power in families mirrors economic power.',
              'Liberal feminism': 'power is becoming more equal as women gain income and legal protection, though inequality remains in decision-making and money management (Pahl and Vogler).'},
    'ctx': [('domestic violence in {city}', {'sensitive', 'hidden', 'private'}),
            ('how couples make financial decisions', {'private', 'meaning', 'behaviour'})],
    'methods': ['questionnaire', 'structured interview', 'unstructured interview', 'semi-structured interview', 'official statistics', 'covert participant observation'],
    'data': [dict(what='financial decision-making in couples', pop='couples', rows=['Mainly the man', 'Mainly the woman', 'Jointly'], cols=('2000', '2025'), dist=True,
                  base=[(35, 45), (15, 20), (35, 45)], delta=[(-15, -5), (-2, 4), (5, 15)], label='percentage of couples saying major financial decisions are made',
                  expl=['women’s rising income gives them more say (resource theory)', 'more couples pool money (Pahl and Vogler)',
                        'changing gender norms favour joint decision-making'],
                  method='structured interview', claim='decision-making power in couples has become equal',
                  counter='Men still make more decisions alone than women; joint decisions may hide unequal influence; answers in interviews may be socially desirable.')],
    'essays': [('Explain two reasons why domestic violence is difficult to measure.', 'Under-reporting by victims (fear, shame, dependence); police recording practices; hidden coercive control; changing definitions; victim surveys depend on disclosure; the dark figure.',
                'domestic violence is best explained by patriarchy',
                'Radical feminists: most serious violence is by men against women (Dobash and Dobash); linked to male authority and control; occurs across classes and cultures.',
                'Wilkinson links violence to inequality and stress; women can also be perpetrators; violence in same-sex relationships; individual and psychological factors; not all men are violent.')],
})

c9c = T('The social construction of childhood and changing parent-child relationships')
build(c9c, {
    'terms': [
        ('child-centred family', 'a family in which children’s needs and interests are a central focus of family life and spending', 'parents organising weekends around children’s activities'),
        ('toxic childhood', 'Palmer’s term for the damage done to children by rapid technological and cultural change', 'children spending long hours on screens and eating junk food'),
        ('march of progress view', 'the view that children’s position has steadily improved and they are now better cared for and protected', 'falling infant mortality and laws protecting children'),
        ('conflict view of childhood', 'the view that inequalities between children and adults, and among children, persist', 'adult control over children’s time, space and bodies'),
        ('age patriarchy', 'Gittins’s term for adult domination over children', 'parents controlling what children wear and where they go'),
        ('infant mortality rate', 'the number of babies who die before their first birthday per 1,000 live births', '4 infant deaths per 1,000 live births'),
        ('helicopter parenting', 'a style of parenting in which parents closely supervise and control children’s activities', 'parents not allowing children to play outside alone'),
    ],
    'thinkers': [
        ('Ariès', 'the idea of childhood as a separate stage developed gradually from the Middle Ages', 'Interactionism',
         'Ariès used paintings and documents to argue medieval children were treated as mini-adults from about age seven.',
         'Pollock argued medieval society had a different, not absent, concept of childhood.'),
        ('Palmer', 'children are being damaged by a “toxic childhood” of technology, junk food and pressure', 'New Right',
         'Palmer argued rapid technological and cultural change harms children’s physical, emotional and intellectual development.',
         'Critics argue this is a moral panic and ignores improvements in children’s lives.'),
        ('Gittins', 'children are subject to age patriarchy', 'Radical feminism',
         'Gittins argued adults dominate children, controlling their time, space and bodies; abuse is an extreme form of this.',
         'March of progress theorists point to children’s rights and greater protection.'),
        ('Postman', 'childhood is disappearing because television ends the information hierarchy between adults and children', 'Interactionism',
         'Postman argued literacy once separated adults and children; television gives children access to adult knowledge.',
         'Critics argue the internet and longer schooling have extended childhood in some ways.'),
    ],
    'explain': [
        ('Explain the march of progress view of childhood.', 'Children’s position has improved over time: lower infant mortality, better health and education, laws against child labour and abuse, and families are more child-centred (Ariès, Shorter).', '1 mark each developed point up to 3. [3]'),
        ('Explain two ways in which adults control children.', 'Control over time (bedtimes, routines); control over space (where they can go); control over bodies (dress, touch); economic dependency; restrictions on access to resources (Hockey and James).', '2 marks for each explained way. [4]'),
        ('Explain two reasons why families have become more child-centred.', 'Lower infant mortality and smaller families encourage emotional investment; laws and welfare define children as needing protection; children’s rights; rising living standards; parents’ concern about risk.', '2 marks for each explained reason. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why the position of children has changed in many societies', ['laws restricting child labour', 'compulsory schooling', 'falling infant mortality', 'smaller families', 'children’s rights and welfare policies']),
    ],
    'claims': [
        ('The conflict view argues that childhood has improved for all children.', False, 'Conflict theorists argue inequalities between adults and children, and among children by class, gender and ethnicity, remain.'),
        ('Palmer argued that modern childhood is “toxic”.', True, 'She argued technology and consumer culture damage children’s development.'),
        ('Falling infant mortality may have encouraged parents to invest more in each child.', True, 'With fewer deaths and fewer children, parents may form closer emotional bonds.'),
    ],
    'ar': ([('Many families have become more child-centred.', 'parents have fewer children and invest more time and money in each.'),
            ('Gittins argued children experience age patriarchy.', 'adults control children’s time, space and bodies.')],
           ['Ariès argued medieval children were kept separate from adult life.', 'the march of progress view claims children are worse off today than in the past.']),
    'scen': ['Parents in {city} drive their children to school, organise their after-school activities and track their phones.',
             'In a rural area near {city}, many 12-year-olds leave school to work on family farms.'],
    'views': {'Functionalism': 'the march of progress view: children are better cared for, protected and educated than in the past, and families are more child-centred.',
              'Radical feminism': 'children, like women, experience age patriarchy: adults control their lives, and the dark side includes abuse (Gittins).',
              'Marxism': 'children’s experiences depend on class: poorer children have worse health, education and opportunities, while childhood is also commercialised by capitalism.',
              'Postmodernism': 'childhood is fluid and changing; media and technology blur the line between adult and child (Postman).'},
    'ctx': [('children’s use of digital technology', {'young', 'behaviour', 'large'}),
            ('parent-child relationships in {city}', {'young', 'private', 'meaning'})],
    'data': [dict(what='children’s independent mobility', pop='children aged 8-11', rows=['Walk to school alone', 'Play outside without an adult', 'Visit shops alone'], cols=('1990', '2025'),
                  base=[(55, 75), (60, 75), (40, 55)], delta=[(-40, -25), (-35, -20), (-30, -15)], label='percentage of children allowed to',
                  expl=['parents have become more concerned about traffic and “stranger danger” (a culture of risk)', 'the conflict view sees growing adult control over children’s space',
                        'more child-centred, protective parenting'], flags={'young'},
                  method='questionnaire', claim='childhood has become more controlled by adults',
                  counter='Children have more rights and voice in many ways; online freedom has increased even as physical freedom has declined; experiences vary by class and area.')],
    'essays': [('Explain two reasons why the position of children in society has changed.', 'Laws on child labour and schooling; falling infant mortality and smaller families; children’s rights; child-centred consumer culture; welfare state; changing ideas of childhood (Ariès).',
                'the position of children in society has steadily improved',
                'March of progress: lower infant mortality, better health and education, children’s rights, child-centred families.',
                'Conflict view: age patriarchy (Gittins), control of time and space; inequalities among children by class, gender and ethnicity; toxic childhood (Palmer); disappearing childhood (Postman); child poverty persists.')],
})

c9d = T('Ageing, grandparents and the beanpole family')
build(c9d, {
    'terms': [
        ('ageing population', 'a population in which the average age is rising and the proportion of older people is increasing', 'more people aged over 65 than under 16'),
        ('beanpole family', 'a multi-generational family that is long and thin, with several generations but few members in each', 'great-grandparents, grandparents, parents and one child'),
        ('pivot generation', 'middle-aged people who care for both their children and their elderly parents', 'a woman caring for her teenage children and her mother'),
        ('dependency ratio', 'the relationship between the size of the working population and the non-working (dependent) population', 'more retired people for every worker'),
        ('kinship network', 'the relatives with whom a person has contact and exchanges help', 'grandparents providing childcare and receiving care in return'),
        ('intergenerational support', 'help exchanged between generations, such as childcare, money or care', 'grandparents paying school fees'),
    ],
    'thinkers': [
        ('Brannen', 'the beanpole family has become more common as life expectancy rises and birth rates fall', 'Functionalism',
         'Brannen argued vertical (intergenerational) ties have strengthened while horizontal ties (cousins, siblings) have weakened; the “pivot generation” gives support both ways.',
         'Not all families fit the beanpole pattern; diversity remains.'),
        ('Hunt', 'older people’s experiences are increasingly shaped by individual choices rather than fixed stages of life', 'Postmodernism',
         'Hunt argued that life-course stages are blurred and that older people choose varied lifestyles.',
         'Poverty, ill health and ageism limit choice for many older people.'),
    ],
    'explain': [
        ('Explain why the beanpole family has become more common.', 'Rising life expectancy means more generations alive at once; falling birth rates mean fewer siblings and cousins; so families are long and thin with stronger vertical ties.', '1 mark life expectancy; 1 mark birth rates; 1 mark shape/vertical ties. [3]'),
        ('Explain two ways in which grandparents contribute to family life.', 'Childcare enabling parents to work; financial help; emotional support and passing on culture; acting as role models; providing a home in extended households.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('effect', 'effects', 'of an ageing population on family life', ['more beanpole families', 'more care for elderly relatives, often by women', 'grandparents providing childcare', 'more one-person households of older people', 'inheritance and financial support across generations']),
    ],
    'claims': [
        ('The beanpole family has many members in each generation.', False, 'It has several generations but few members in each.'),
        ('An ageing population can increase the caring responsibilities of middle-aged women.', True, 'Women in the pivot generation often care for both children and parents.'),
    ],
    'ar': ([('Beanpole families have become more common.', 'people are living longer and having fewer children.'),
            ('Grandparents often provide childcare.', 'many mothers are in paid employment.')],
           ['an ageing population means birth rates are rising.', 'beanpole families have strong horizontal ties between cousins.']),
    'scen': ['{woman}, aged 52, lives in {city} and looks after her 80-year-old father while also supporting her two teenagers.',
             'In {city}, many grandparents collect their grandchildren from school every day while both parents work.'],
    'views': {'Functionalism': 'families adapt to demographic change: beanpole families and grandparents provide vital support such as childcare and care for the elderly.',
              'Radical feminism': 'the burden of caring for elderly relatives and grandchildren falls mainly on women, extending their unpaid labour (the pivot generation).',
              'Postmodernism': 'later life is increasingly varied and chosen; older people construct diverse identities and relationships.'},
    'ctx': [('the role of grandparents in childcare', {'meaning', 'behaviour', 'large'}),
            ('the experiences of people caring for elderly parents', {'meaning', 'sensitive', 'private'})],
    'data': [dict(what='grandparents and childcare', pop='working parents with children under 12', rows=['Grandparents', 'Paid childcare', 'Partner/other parent'], cols=('2005', '2025'), share=True,
                  base=[(25, 35), (20, 30), (20, 30)], delta=[(3, 10), (-5, 5), (-3, 5)], label='percentage naming this as their main source of childcare',
                  expl=['more mothers are in paid work while childcare costs are high, so grandparents help', 'longer life expectancy means more grandparents are available and healthy',
                        'beanpole families strengthen intergenerational ties'],
                  method='questionnaire', claim='grandparents have become more important to family life',
                  counter='Many families rely on paid childcare or partners; grandparents themselves may still be working; the data do not show the quality of relationships.')],
    'essays': [('Explain two ways in which an ageing population affects family life.', 'Beanpole families; pivot generation caring both ways; grandparents’ childcare; more older one-person households; financial transfers and inheritance.',
                'grandparents play a more important role in family life than in the past',
                'Longer life expectancy; beanpole families (Brannen); childcare for working parents; financial support.',
                'Geographical mobility separates generations; many grandparents work longer; care often flows to grandparents; the role varies by culture and class.')],
}, V8)


@c9d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c9d_dep(r, D):
    for _ in range(40):
        young = r.choice([15, 16, 18, 20, 22, 25, 28, 30])
        old = r.choice([8, 10, 12, 14, 16, 18, 20, 22, 25])
        work = 100 - young - old
        ratio = 100 * (young + old) / work
        if 40 <= work <= 75:
            break
    d = ctxd(r)
    intro = f'In a country studied by {d["person"]}, {young}% of the population are aged under 16, {work}% are aged 16-64 and {old}% are aged 65 and over.'
    if D <= 1:
        ans = _pc(ratio)
        ds = [_pc(100 * old / work), _pc(100 * young / work), _pc(young + old), _pc(100 * work / (young + old))]
        opts, a = mcq(r, ans, [x for x in ds if x != ans])
        return {'stem': f'{intro} What is the dependency ratio (dependants per 100 people of working age)?', 'options': opts, 'answer': a,
                'key': f'({young} + {old}) ÷ {work} × 100 = {ans}. [1]', 'marks': 1}
    parts = [('Calculate the dependency ratio (dependants per 100 people of working age).', f'({young} + {old}) ÷ {work} × 100 = {_pc(ratio)}.', '1 mark method; 1 mark answer to 1 d.p. [2]'),
             ('Calculate the old-age dependency ratio (people aged 65+ per 100 of working age).', f'{old} ÷ {work} × 100 = {_pc(100 * old / work)}.', '1 mark method; 1 mark answer. [2]'),
             ('Explain one way in which an ageing population may affect family life.', 'More beanpole families and a pivot generation caring for both children and elderly parents; more older one-person households; grandparents providing childcare.', '1 mark identifying; 1 mark explaining. [2]'),
             ('Explain why women may be most affected by the increase in older dependants.', 'Women do most unpaid caring for elderly relatives, often alongside paid work and childcare, adding to the dual burden or triple shift.', '1 mark: women as main carers; 1 mark: effect on their workload/employment. [2]')]
    sel = parts[:2] if D == 2 else (parts[:3] if D == 3 else parts)
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')

CHAPTERS[9] = [c9a, c9b, c9c, c9d]


# ============================================================== CHAPTER 10: Marriage, divorce and demographic change

c10a = T('Trends in marriage, cohabitation and singlehood')
build(c10a, {
    'terms': [
        ('cohabitation', 'a couple living together in a sexual relationship without being married or in a civil partnership', 'a couple who have lived together for five years with no plans to marry'),
        ('serial monogamy', 'a pattern of having a series of marriages or long-term relationships, one after another', 'a person who marries, divorces and remarries twice'),
        ('singlehood', 'not living with a partner, whether never married, divorced or widowed', 'a 35-year-old professional living alone by choice'),
        ('secularisation', 'the process by which religion loses its influence over society and individuals', 'fewer couples marrying in a religious ceremony'),
        ('arranged marriage', 'a marriage in which families play a major role in choosing the partner', 'parents introducing their son to a suitable partner from the same community'),
        ('living apart together', 'a couple in a long-term relationship who choose to live in separate homes', 'partners who each keep their own flat'),
        ('remarriage', 'marriage of a person who has previously been married', 'a divorced woman marrying a new partner'),
    ],
    'thinkers': [
        ('Chester', 'cohabitation is often a temporary stage before marriage rather than a permanent alternative', 'Functionalism',
         'Chester argued many couples cohabit first and then marry, especially when they have children, so marriage remains valued.',
         'Others argue cohabitation is increasingly a long-term alternative to marriage.'),
        ('Beck and Beck-Gernsheim', 'individualisation means people make relationship choices for themselves rather than following tradition', 'Late modernity',
         'They argued that in a risk society, relationships are negotiated and less stable, as individuals pursue self-fulfilment.',
         'Critics argue tradition, religion and class still shape choices.'),
        ('Giddens', 'modern relationships are “pure relationships” that last only while both partners are satisfied', 'Late modernity',
         'Giddens linked declining marriage and rising cohabitation to the search for emotional satisfaction and equality.',
         'Many couples still marry for long-term commitment, religion or children.'),
    ],
    'explain': [
        ('Explain two reasons for the increase in cohabitation.', 'Decline in stigma attached to sex outside marriage; secularisation; cost of weddings; trial marriage; individualisation and wish to avoid divorce; more women economically independent.', '2 marks for each explained reason. [4]'),
        ('Explain why the number of people living alone has increased.', 'Later marriage and more people never marrying; rising divorce and separation; an ageing population with more widows and widowers; greater affluence; individualisation and preference for independence.', '1 mark each developed reason up to 3. [3]'),
        ('Explain two reasons why people marry later than in the past.', 'Longer education and career building, especially for women; cohabitation first; cost of weddings and housing; less pressure to marry early; contraception allowing sex before marriage without risk of pregnancy.', '2 marks for each explained reason. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why fewer people are marrying in many societies', ['secularisation reduces religious pressure to marry', 'cohabitation has become socially acceptable', 'women’s economic independence', 'fear of divorce', 'the high cost of weddings', 'individualisation and changing attitudes']),
    ],
    'claims': [
        ('Cohabitation is always a permanent alternative to marriage.', False, 'For many couples it is a stage before marriage; for others it is an alternative.'),
        ('Secularisation may help explain the decline in marriage.', True, 'With less religious influence, there is less pressure to marry and less stigma attached to cohabitation.'),
        ('Remarriages make up a significant share of all marriages in many societies.', True, 'Rising divorce has led to more remarriages and serial monogamy.'),
    ],
    'ar': ([('Cohabitation has increased.', 'there is less stigma attached to sex and childbirth outside marriage.'),
            ('People are marrying later.', 'many spend longer in education and building careers.')],
           ['marriage rates have risen steadily in most Western societies since 1970.', 'secularisation increases religious pressure to marry.']),
    'scen': ['{woman} and her partner have lived together in {city} for eight years and have two children; they say marriage is “just a piece of paper”.',
             'In {city}, the average age at first marriage has risen from 23 to 31 over forty years.'],
    'views': V8,
    'ctx': [('why couples choose to cohabit rather than marry', {'meaning', 'private'}),
            ('changes in marriage rates since 1970', {'change', 'large'})],
    'data': [dict(what='marriage and cohabitation', pop='adults aged 25-34', rows=['Married', 'Cohabiting', 'Single (not living with a partner)'], cols=('1995', '2025'), dist=True,
                  base=[(48, 58), (12, 18), (25, 35)], delta=[(-20, -10), (6, 14), (2, 10)], label='percentage of adults aged 25-34 who are',
                  expl=['secularisation and declining stigma have made cohabitation acceptable', 'individualisation means people choose relationships rather than follow tradition (Beck)',
                        'longer education and careers delay marriage'],
                  method='official statistics', claim='marriage is becoming less important in modern societies',
                  counter='Many cohabiting couples later marry (Chester); most people still marry at some point; remarriage shows continued commitment to the institution.')],
    'essays': [('Explain two reasons for the decline in marriage rates.', 'Secularisation; declining stigma of cohabitation and singlehood; women’s independence; fear of divorce; individualisation (Beck, Giddens); cost.',
                'marriage is no longer an important institution in modern societies',
                'Falling marriage rates; rising cohabitation, singlehood and divorce; individualisation and pure relationships; secularisation.',
                'Most people still marry at some time; remarriage shows commitment; cohabitation often leads to marriage (Chester); same-sex marriage shows its symbolic value; patterns vary by culture and religion.')],
})

c10b = T('Divorce: trends and explanations')
build(c10b, {
    'terms': [
        ('divorce', 'the legal ending of a marriage', 'a court granting a decree ending a marriage'),
        ('divorce rate', 'the number of divorces per 1,000 married people in a year', '10 divorces per 1,000 married couples'),
        ('separation', 'when a married couple stop living together without legally ending the marriage', 'a couple living apart while deciding whether to divorce'),
        ('empty-shell marriage', 'a marriage in which the couple stay legally married but no longer love each other or share their lives', 'a couple who stay together only for the children'),
        ('no-fault divorce', 'divorce granted without either partner having to prove that the other was to blame', 'a divorce on the basis of irretrievable breakdown'),
        ('stigma', 'a mark of disgrace or shame attached to a person or behaviour', 'divorced women being treated as outcasts in the past'),
        ('rising expectations of marriage', 'the idea that people now expect more emotional satisfaction from marriage, so they are more likely to leave an unhappy one', 'divorcing because the relationship is no longer fulfilling'),
    ],
    'thinkers': [
        ('Fletcher', 'higher expectations of marriage are a major reason for the increase in divorce', 'Functionalism',
         'Fletcher argued that the rise in divorce reflects the value placed on marriage: people expect more and will not accept an unhappy one, and most remarry.',
         'Feminists argue it ignores women’s dissatisfaction with patriarchal marriage.'),
        ('Hochschild', 'women’s dissatisfaction with the dual burden contributes to divorce', 'Liberal feminism',
         'Hochschild argued that women experience a conflict between equality at work and inequality at home, leading to marital tension.',
         'Men also initiate many divorces and other factors are involved.'),
        ('Allan and Crow', 'marriage is now based on love rather than economic necessity, so it is easier to end', 'Interactionism',
         'They argued that as the family has ceased to be a unit of production, couples are less economically tied together.',
         'Financial ties such as property and children still make divorce costly.'),
        ('Murray', 'high divorce rates undermine the traditional family and harm children', 'New Right',
         'The New Right sees divorce as part of family breakdown linked to welfare dependency and poor socialisation.',
         'Feminists see divorce as liberating women from oppressive marriages.'),
    ],
    'explain': [
        ('Explain two reasons for the increase in divorce in many societies.', 'Changes in law making divorce easier and cheaper; declining stigma; secularisation; rising expectations of marriage (Fletcher); women’s financial independence; individualisation.', '2 marks for each explained reason. [4]'),
        ('Explain why divorce statistics may not show the full extent of marriage breakdown.', 'They exclude separations and empty-shell marriages; couples may stay together for religious, financial or children’s reasons; cohabiting relationships that end do not count.', '1 mark each developed reason up to 3. [3]'),
        ('Explain the difference between the New Right and feminist views of divorce.', 'The New Right sees divorce as family breakdown harming children and society; feminists see it as a sign of women’s growing independence and escape from patriarchal oppression.', '1 mark each view; 1 mark contrast. [3]'),
    ],
    'why': [
        ('consequence', 'consequences', 'of rising divorce rates for family life', ['more lone-parent families', 'more reconstituted families', 'more one-person households', 'serial monogamy', 'children may experience economic and emotional difficulties']),
    ],
    'claims': [
        ('A rise in divorce means people no longer value marriage.', False, 'Fletcher argued it reflects higher expectations, and most divorced people remarry.'),
        ('Changes in divorce law have contributed to rising divorce rates.', True, 'Laws have made divorce easier, cheaper and possible without proof of fault.'),
        ('Feminists see divorce only as a sign of family breakdown.', False, 'Many feminists see it as women escaping oppressive marriages.'),
    ],
    'ar': ([('Divorce rates rose after legal reforms in many countries.', 'new laws made divorce easier and cheaper to obtain.'),
            ('Women initiate the majority of divorces in many countries.', 'women may be more dissatisfied with the inequalities of marriage.')],
           ['divorce rates fall when stigma attached to divorce declines.', 'the New Right welcomes rising divorce as a sign of freedom.']),
    'scen': ['After a new law in {city} allows couples to divorce without proving fault, the number of divorces doubles in two years.',
             '{woman} divorces her husband after 15 years, saying she was “tired of doing everything at home while working full-time”.'],
    'views': {'Functionalism': 'rising divorce reflects higher expectations of marriage; most people remarry, so marriage is still valued (Fletcher).',
              'New Right': 'rising divorce is evidence of family breakdown, harming children and creating welfare dependency (Murray).',
              'Radical feminism': 'divorce shows women are escaping oppressive patriarchal marriages; women’s dissatisfaction with the dual burden and male power drives divorce.',
              'Postmodernism': 'divorce reflects individual choice and the search for fulfilment; relationships are fluid and family types diverse (Stacey, Giddens).'},
    'ctx': [('children’s experiences of their parents’ divorce', {'young', 'sensitive', 'private', 'meaning'}),
            ('long-term trends in divorce', {'change', 'large'})],
    'essays': [('Explain two reasons why divorce rates have increased.', 'Legal changes; declining stigma; secularisation; rising expectations (Fletcher); women’s independence and dissatisfaction (Hochschild); individualisation.',
                'rising divorce rates are a threat to the family',
                'New Right: family breakdown, harm to children, lone-parent families and welfare dependency; instability of relationships.',
                'Fletcher: higher expectations and remarriage; feminists: escape from oppression; postmodernists: diversity and choice; empty-shell marriages were not better; most children adapt.')],
}, V8)


@c10b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c10b_rate(r, D):
    for _ in range(40):
        married = r.choice([400000, 500000, 600000, 800000, 1000000, 1200000, 2000000, 2500000])
        r1 = r.choice([2, 3, 4, 5, 6])
        r2 = r1 + r.choice([2, 3, 4, 5, 6, -1])
        m2 = married * r.choice([90, 95, 100]) // 100
        d1, d2 = married * r1 // 1000, m2 * r2 // 1000
        if r2 > 0 and d1 * 1000 == married * r1 and d2 * 1000 == m2 * r2:
            break
    else:
        return None
    y1, y2 = r.choice([(1970, 1995), (1965, 1990), (1975, 2000), (1980, 2010)])
    d = ctxd(r)
    intro = f'In a country studied by {d["person"]}, there were {married:,} married people and {d1:,} divorces in {y1}; in {y2} there were {m2:,} married people and {d2:,} divorces.'
    if D <= 1:
        ans = str(r2)
        ds = [str(x) for x in {r1, r2 * 10, round(100 * d2 / m2, 1), r2 + 2, d2 // 1000} if str(x) != ans]
        opts, a = mcq(r, ans, ds)
        return {'stem': f'{intro} What was the divorce rate per 1,000 married people in {y2}?', 'options': opts, 'answer': a, 'key': f'{d2:,} ÷ {m2:,} × 1,000 = {r2}. [1]', 'marks': 1}
    pc = 100 * (r2 - r1) / r1
    parts = [(f'Calculate the divorce rate per 1,000 married people in {y1} and in {y2}.', f'{y1}: {d1:,} ÷ {married:,} × 1,000 = {r1}; {y2}: {d2:,} ÷ {m2:,} × 1,000 = {r2}.', '1 mark method; 1 mark both rates. [2]'),
             ('Calculate the percentage change in the divorce rate between the two years.', f'({r2} − {r1}) ÷ {r1} × 100 = {_pc(pc)}%.', '1 mark method; 1 mark answer. [2]'),
             ('Explain why sociologists use the number of divorces per 1,000 married people rather than the total number of divorces.', 'The number of married people changes over time; a rate allows fair comparison between years and countries.', '1 mark: controls for number married; 1 mark: allows comparison. [2]'),
             ('Suggest two reasons for the change in the divorce rate.', ('Changes in divorce law; declining stigma; secularisation; rising expectations of marriage; women’s financial independence.' if r2 > r1 else 'Fewer people marrying (so those who marry are more committed); later marriage; more cohabitation.'),
              '1 mark each valid reason linked to the direction of change. [2]'),
             ('Explain one reason why divorce statistics may underestimate the extent of relationship breakdown.', 'They exclude separations, empty-shell marriages and the break-up of cohabiting couples.', '1 mark identifying; 1 mark explaining. [2]')]
    if D == 2:
        sel = parts[:2]
    elif D == 3:
        sel = [parts[0], parts[1], r.choice(parts[2:])]
    else:
        sel = [parts[0], parts[1], parts[3], parts[4]]
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


c10c = T('Same-sex families, reconstituted families and lone parenthood')
build(c10c, {
    'terms': [
        ('same-sex family', 'a family headed by a couple of the same sex, with or without children', 'two women raising an adopted child'),
        ('reconstituted family', 'a family in which one or both partners have children from previous relationships', 'a stepfather living with his partner’s children'),
        ('lone-parent family', 'a family headed by one parent with dependent children', 'a widowed father raising three children'),
        ('civil partnership', 'a legally recognised union of two people, in some countries available to same-sex couples', 'a registered partnership giving legal rights similar to marriage'),
        ('welfare dependency', 'the New Right idea that generous state benefits encourage people to rely on the state rather than work or family', 'claims that benefits encourage lone parenthood'),
        ('step-family', 'another term for a reconstituted family, including step-parents and step-siblings', 'children living with a step-mother and her children'),
        ('chosen family', 'Weeks’s term for networks of friends and partners that function as family, especially among gay and lesbian people', 'close friends who celebrate holidays together and support each other'),
    ],
    'thinkers': [
        ('Weeks', 'gay and lesbian people often create “chosen families” of friends and partners', 'Postmodernism',
         'Weeks argued that changing attitudes and the decline of stigma allowed same-sex couples to create stable relationships and chosen families.',
         'Same-sex families still face discrimination and legal inequality in many countries.'),
        ('Murray', 'lone-parent families create an underclass dependent on welfare', 'New Right',
         'Murray argued that boys growing up without fathers lack role models, contributing to crime and dependency.',
         'Critics argue the problems are caused by poverty, not family type.'),
        ('Ferri and Smith', 'step-parenting can be very similar to parenting in first-time families', 'Functionalism',
         'Ferri and Smith found that step-families are diverse and that being a step-parent is not necessarily a problem.',
         'Allan and Crow note particular tensions in step-families, such as divided loyalties.'),
        ('Allan and Crow', 'reconstituted families may face particular tensions such as divided loyalties and contact with non-resident parents', 'Interactionism',
         'They argued that reconstituted families must negotiate new relationships and may experience conflict over money and discipline.',
         'Such tensions may result from poverty or the earlier divorce rather than the family form.'),
    ],
    'explain': [
        ('Explain two reasons for the increase in lone-parent families.', 'Rising divorce and separation; declining stigma attached to births outside marriage; women’s economic independence; welfare support; some women choosing to have children alone.', '2 marks for each explained reason. [4]'),
        ('Explain two problems that reconstituted families may face.', 'Divided loyalties between parents; tension between step-siblings and step-parents; disputes over discipline and money; maintenance payments to non-resident children; contact arrangements.', '2 marks for each explained problem. [4]'),
        ('Explain why same-sex families have become more common in many societies.', 'Legal changes (civil partnerships, same-sex marriage, adoption rights); declining stigma and changing attitudes; secularisation; reproductive technology and surrogacy.', '1 mark each developed reason up to 3. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why most lone-parent families are headed by women', ['courts usually award custody to mothers', 'mothers are more likely to be the main carers before separation', 'women are more likely to choose to raise children alone', 'fathers are more likely to leave or to be non-resident']),
    ],
    'claims': [
        ('Most lone-parent families are headed by fathers.', False, 'Most are headed by mothers, partly because mothers are usually granted custody and are the main carers.'),
        ('The New Right sees lone-parent families as harmful to children.', True, 'It argues children need a male role model and links lone parenthood to welfare dependency.'),
        ('Same-sex couples can now marry in some countries.', True, 'Legal changes in many countries have extended marriage or civil partnership to same-sex couples.'),
    ],
    'ar': ([('Lone-parent families are more likely to be in poverty.', 'many lone parents cannot work full-time because of childcare responsibilities.'),
            ('Same-sex families have become more visible.', 'laws and attitudes towards same-sex relationships have changed in many countries.')],
           ['reconstituted families are formed only after the death of a parent.', 'the New Right supports lone-parent families as an equal alternative.']),
    'scen': ['{person}, a single mother in {city}, works part-time and struggles to pay rent; a newspaper column blames “broken families” for local crime.',
             'Two men in {city} who have been partners for ten years adopt a child after a change in the law.'],
    'views': {'New Right': 'the married, heterosexual two-parent family is the best environment for children; lone-parent and other non-traditional families are departures from this norm, and lone parenthood is linked to a lack of male role models and welfare dependency (Murray).',
              'Liberal feminism': 'lone-parent families often reflect women’s ability to leave unsatisfactory relationships; their problems stem from poverty and lack of childcare, which policy can address.',
              'Postmodernism': 'same-sex, reconstituted and lone-parent families are part of growing diversity and choice; there is no single ideal family (Weeks, Stacey).',
              'Marxism': 'family forms are shaped by economic conditions under capitalism: the problems some lone-parent and reconstituted families face reflect poverty, low wages and the cost of childcare and housing rather than family structure itself.'},
    'ctx': [('the experiences of lone parents in {city}', {'meaning', 'sensitive', 'private'}),
            ('relationships between step-parents and step-children', {'private', 'young', 'meaning'}),
            ('how same-sex couples organise family life', {'meaning', 'private'})],
    'data': [dict(what='poverty among different family types', pop='families with children', rows=['Lone-parent families', 'Couple families with one earner', 'Couple families with two earners'], cols=('2010', '2025'),
                  base=[(40, 50), (25, 35), (6, 12)], delta=[(-8, 3), (-5, 5), (-3, 3)], label='percentage of families in relative poverty',
                  expl=['lone parents often cannot work full-time because of childcare, so incomes are lower', 'Marxists and feminists blame low pay and lack of affordable childcare, not family type',
                        'two-earner families have more income to share'],
                  method='official statistics', claim='lone-parent families are a cause of poverty',
                  counter='The data show a correlation, not causation: poverty may also cause relationship breakdown; policy (childcare, benefits) affects poverty; many lone-parent families are not poor.')],
    'essays': [('Explain two reasons for the growth of reconstituted families.', 'Rising divorce and separation; remarriage and serial monogamy; repartnering after cohabitation; declining stigma; individualisation.',
                'lone-parent families are harmful to children',
                'New Right: lack of male role models, poorer socialisation, welfare dependency (Murray); higher risk of poverty.',
                'Problems linked to poverty, not structure; many children do well; conflict in two-parent families can be more harmful; feminists see lone parenthood as escape from abuse; postmodernists value diversity.')],
})

c10d = T('Demographic change: birth rates, death rates, life expectancy and family size')
build(c10d, {
    'terms': [
        ('birth rate', 'the number of live births per 1,000 of the population per year', '11 births per 1,000 people'),
        ('death rate', 'the number of deaths per 1,000 of the population per year', '9 deaths per 1,000 people'),
        ('total fertility rate', 'the average number of children a woman is expected to have in her lifetime', '1.6 children per woman'),
        ('life expectancy', 'the average number of years a person born in a particular year can be expected to live', 'life expectancy at birth of 81 years'),
        ('infant mortality rate', 'the number of babies who die before their first birthday per 1,000 live births', '4 infant deaths per 1,000 live births'),
        ('natural increase', 'the difference between the number of births and the number of deaths in a population', '12,000 births minus 9,000 deaths = 3,000'),
        ('net migration', 'the difference between the number of people entering and leaving a country', '50,000 immigrants minus 30,000 emigrants'),
        ('ageing population', 'a population in which the proportion of older people is increasing', 'the share aged over 65 rising from 10% to 20%'),
    ],
    'thinkers': [
        ('Harper', 'falling death rates and rising life expectancy are producing beanpole families and changing relationships across generations', 'Functionalism',
         'Harper argued falling infant mortality and fertility mean parents invest more in fewer children and more generations are alive at once.',
         'Experiences of ageing differ greatly by class and gender.'),
        ('Hirsch', 'an ageing population will require new policies on pensions, housing and work', 'Functionalism',
         'Hirsch argued that longer life means people may need to work longer and that housing and care must adapt.',
         'Critics argue fears of an ageing “burden” are exaggerated and older people contribute through care and volunteering.'),
    ],
    'explain': [
        ('Explain two reasons why the birth rate has fallen in many societies.', 'Women’s greater participation in education and paid work; availability of contraception and abortion; falling infant mortality; children are an economic cost rather than an asset; changing attitudes and later marriage.', '2 marks for each explained reason. [4]'),
        ('Explain two reasons why life expectancy has increased.', 'Improved nutrition and living standards; medical advances (vaccination, antibiotics); public health measures (clean water, sanitation); welfare state and health care; fewer dangerous manual jobs.', '2 marks for each explained reason. [4]'),
        ('Explain two effects of a falling birth rate on family life.', 'Smaller families and more child-centredness; more women able to work; beanpole families; fewer siblings and cousins; more childless couples.', '2 marks for each explained effect. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why family size has fallen in many societies', ['children have become an economic cost rather than an asset', 'women are in education and paid work', 'contraception is widely available', 'lower infant mortality means parents need fewer births', 'later marriage']),
    ],
    'claims': [
        ('A falling death rate always means a rising population.', False, 'Population change also depends on births and migration.'),
        ('Falling infant mortality is one reason for smaller families.', True, 'Parents no longer need many births to ensure some children survive.'),
        ('The total fertility rate is the number of births per 1,000 people.', False, 'That is the birth rate; the total fertility rate is the average number of children per woman.'),
    ],
    'ar': ([('Family size has fallen in many societies.', 'children have become an economic cost rather than an economic asset.'),
            ('Life expectancy has risen.', 'improvements in diet, sanitation and medicine have reduced death rates.')],
           ['the birth rate is the number of children per woman.', 'rising infant mortality leads parents to have fewer children.']),
    'scen': ['In {city}, the average number of children per woman has fallen from 4.2 to 1.8 in forty years, while the number of people over 80 has doubled.',
             '{woman} and her partner in {city} decide to have only one child because of the cost of housing and education.'],
    'views': {'Functionalism': 'smaller, child-centred families fit the needs of a modern economy, and beanpole families provide intergenerational support as life expectancy rises (Parsons, Harper).',
              'Liberal feminism': 'falling birth rates reflect women’s greater control over their lives through education, careers and contraception, so women choose smaller families or later motherhood.',
              'Marxism': 'decisions about family size are shaped by capitalism: children are expensive in a consumer economy, while low wages, insecure work and housing costs limit what families can afford.',
              'Postmodernism': 'whether, when and how many children to have is an individual lifestyle choice; life courses are increasingly diverse.'},
    'ctx': [('changes in family size over fifty years', {'change', 'large'}),
            ('why couples decide how many children to have', {'meaning', 'private'})],
    'essays': [('Explain two reasons for the decline in family size.', 'Changes in women’s position; contraception; falling infant mortality; children as an economic cost; compulsory schooling and child labour laws; changing values.',
                'demographic change has transformed family life',
                'Smaller, child-centred families; beanpole families; pivot generation; more older one-person households; more women working.',
                'Families still remain central and often nuclear; other changes (divorce, cohabitation, economy) matter as much; effects vary by class, culture and country.')],
}, V8)


@c10d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c10d_demo(r, D):
    for _ in range(40):
        pop = r.choice([200000, 250000, 400000, 500000, 800000, 1000000, 2000000])
        br = r.choice([8, 9, 10, 11, 12, 14, 16, 18, 22, 25, 30])
        dr = r.choice([5, 6, 7, 8, 9, 10, 11, 12])
        b, d_ = pop * br // 1000, pop * dr // 1000
        if b * 1000 == pop * br and d_ * 1000 == pop * dr:
            break
    nimm, nem = r.choice([(30000, 12000), (15000, 20000), (8000, 3000), (25000, 25000), (12000, 18000)])
    nimm, nem = nimm * pop // 1000000 or 1000, nem * pop // 1000000 or 1000
    d = ctxd(r)
    intro = f'In one year, a region near {d["city"]} with a population of {pop:,} recorded {b:,} births, {d_:,} deaths, {nimm:,} immigrants and {nem:,} emigrants.'
    ni = b - d_
    nm = nimm - nem
    if D <= 1:
        ans = str(br)
        ds = [str(x) for x in {dr, br - dr, br * 10, round(b / 100)} if str(x) != ans]
        opts, a = mcq(r, ans, ds)
        return {'stem': f'{intro} What was the birth rate (births per 1,000 population)?', 'options': opts, 'answer': a, 'key': f'{b:,} ÷ {pop:,} × 1,000 = {br}. [1]', 'marks': 1}
    parts = [('Calculate the birth rate and the death rate per 1,000 population.', f'Birth rate {b:,} ÷ {pop:,} × 1,000 = {br}; death rate {d_:,} ÷ {pop:,} × 1,000 = {dr}.', '1 mark each. [2]'),
             ('Calculate the natural increase and the net migration.', f'Natural increase = {b:,} − {d_:,} = {ni:,}; net migration = {nimm:,} − {nem:,} = {nm:,}.', '1 mark each. [2]'),
             ('Calculate the total population change over the year and the new population.', f'{ni:,} + ({nm:,}) = {ni + nm:,}; new population = {pop + ni + nm:,}.', '1 mark change; 1 mark new population. [2]'),
             ('Explain one effect of a low birth rate on family life.', 'Smaller families with more child-centred parenting; beanpole families; more women able to work; fewer siblings and wider kin.', '1 mark identifying; 1 mark explaining. [2]'),
             ('Explain one reason why the death rate has fallen in many societies.', 'Better nutrition, medicine and public health (clean water, sanitation, vaccination) reduce deaths, especially among infants and older people.', '1 mark identifying; 1 mark explaining. [2]')]
    if D == 2:
        sel = parts[:2]
    elif D == 3:
        sel = parts[:3]
    else:
        sel = parts[:3] + [r.choice(parts[3:])] if D == 4 else parts
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')

CHAPTERS[10] = [c10a, c10b, c10c, c10d]
