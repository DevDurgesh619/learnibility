"""Cambridge International AS Level Global Perspectives & Research 9239 (AS, grade 11), taught as
'political science': critical thinking applied to political and governance issues.

Chapters follow the CUP coursebook: global issues; causes, consequences and courses of action;
perspectives; argument analysis; evidence and sources; evaluating arguments; research skills; the
essay (Component 2); the team project (Component 3). Items mirror Component 1 (written exam: source
passages, short structured questions and an extended 'compare the arguments' answer) plus
assertion-reason and data items. Real institutions, treaties and theorists are used for knowledge;
numeric data (turnout, vote and seat shares, survey results) use fictional countries so that
figures are never mistaken for real statistics.
"""
import re

from core import MARKS
from ._lib import topic, mcq, compose, person, two_people, city, fmt

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

COUNTRIES = ['Zentara', 'Kestria', 'Lunaria', 'Marvona', 'Nordavia', 'Pelora', 'Sundara', 'Valdoria', 'Calvania', 'Dravonia',
             'Esteria', 'Fendaria', 'Gorvania', 'Halvoria', 'Istrana', 'Jovania', 'Korvia', 'Loristan', 'Merania', 'Ostrelia']
PARTIES = ['Progress Party', 'National Union', 'Green Alliance', 'Labour Front', 'Liberal Democrats', 'People’s Movement',
           'Civic Platform', 'Unity List', 'Reform Party', 'Social Democrats']


# ============================================================== generic helpers

def cap(s):
    return s[:1].upper() + s[1:]


def low(s):
    return s[:1].lower() + s[1:] if not s[:2].isupper() else s


def T(name, *extra):
    return topic(name, name.lower(), *extra)


def dm(C, D):
    return MARKS.get((C, D), (2, 2))[0]


def lm(D):
    """Marks for an extended (long) answer at difficulty D, matching the mock scaling."""
    return max(1, round(dm('C4', max(2, D)) * 1.5))


def pct(x, dp=1):
    return fmt(round(x, dp), dp) + '%'


def levels(m, l1, l2, l3):
    """Level-of-response key for an extended answer worth m marks."""
    if m <= 3:
        return f'Level 1 (1 mark): {l1} Level 2 ({2 if m == 2 else "2–" + str(m)} marks): {l2} {l3} [{m}]'
    a = max(1, m // 3)
    b = max(a + 1, (2 * m) // 3)
    rng = lambda x, y: str(x) if x == y else f'{x}–{y}'
    return (f'Level 1 ({rng(1, a)} marks): {l1} Level 2 ({rng(a + 1, b)} marks): {l2} '
            f'Level 3 ({rng(b + 1, m)} marks): {l3} [{m}]')


def Q(stem, ans, key, marks=None, typ=None, opts=None):
    q = {'stem': stem, 'answer': ans, 'key': key}
    if marks:
        q['marks'] = marks
    if typ:
        q['type'] = typ
    if opts:
        q['options'] = opts
    return q


def MC(r, stem, ans, ds, key):
    opts, a = mcq(r, ans, list(ds))
    if not re.search(r'\[\d+\]\s*$', key):
        key = key + ' [1]'
    return {'stem': stem, 'options': opts, 'answer': a, 'key': key, 'marks': 1}


def add_terms(t, terms, D1=(1, 2), D2=(2, 3)):
    """terms: [(term, definition)] -> definition->term and term->definition MCQs."""
    if len(terms) < 4:
        return
    t.fixed('C1', D1, [(f'Which term matches this definition: “{d}”?', cap(term), f'{cap(term)}: {d}. [1]',
                        [cap(x) for x, _ in terms if x != term]) for term, d in terms])
    t.fixed('C1', D2, [(f'What is meant by “{term}” in Global Perspectives?', cap(d) + '.', f'{cap(term)}: {d}. [1]',
                        [cap(y) + '.' for x, y in terms if x != term]) for term, d in terms])


def add_mcqs(t, C, D, entries):
    """entries: (stem, answer, [3+ distractors], key) as stand-alone MCQ templates."""
    for stem, ans, ds, key in entries:
        def fn(r, D_, stem=stem, ans=ans, ds=ds, key=key):
            return MC(r, stem, ans, ds, key)
        fn.__name__ = 'mcq'
        t.add(C, D, 'mcq')(fn)


AR_OPTS = ['Both A and R are true, and R is the correct explanation of A.', 'Both A and R are true, but R is not the correct explanation of A.',
           'A is true, but R is false.', 'A is false, but R is true.']
AR_CODE = {'AR': 0, 'AnR': 1, 'A': 2, 'R': 3}


def add_ar(t, entries, D=(2, 3)):
    """Assertion-reason MCQs: (assertion, reason, code AR/AnR/A/R, why)."""
    for A, R, code, why in entries:
        def fn(r, D_, A=A, R=R, code=code, why=why):
            return {'stem': f'Assertion (A): {A} Reason (R): {R} Choose the correct option.', 'options': list(AR_OPTS),
                    'answer': AR_OPTS[AR_CODE[code]], 'key': f'{why} [1]', 'marks': 1}
        fn.__name__ = 'ar'
        t.add('C2', D, 'mcq')(fn)


def add_explain(t, entries, D=(2, 3, 4)):
    """Fixed explain items (stem, answer, key ending [n]); marks follow the key."""
    for stem, ans, key in entries:
        m = re.findall(r'\[(\d+)\]', key)

        def fn(r, D_, stem=stem, ans=ans, key=key, m=m):
            return Q(stem, ans, key, int(m[-1]) if m else None)
        fn.__name__ = 'fixed'
        t.add('C2', D, 'explain')(fn)
    t.entries = getattr(t, 'entries', {})
    t.entries.setdefault('C2', []).extend(((e, D) for e in entries))


CLAIM_LEADS = ['A student writes:', 'In a seminar, a student says:', 'A revision blog states:', 'A classmate claims:', 'A newspaper column asserts:']


def add_claims(t, claims, D=(1, 2, 3)):
    """claims: [(claim, is_correct, why)] -> 'is this correct?' items, each with several lead-ins."""
    def fn(r, D_):
        c, ok, why = r.choice(claims)
        lead = r.choice(CLAIM_LEADS)
        return Q(f'{lead} “{c}” Is this correct? Explain your answer.', ('Correct. ' if ok else 'Not correct. ') + why,
                 '1 mark correct judgement; 1 mark accurate supporting explanation [2]', 2, 'explain')
    fn.__name__ = 'claims'
    t.add('C2', D, 'explain')(fn)


ESSAY_LEADS = [
    lambda c, p: f'“{cap(c)}.” To what extent do you agree with this statement?',
    lambda c, p: f'To what extent do you agree that {c}? Consider different perspectives in your answer.',
    lambda c, p: f'Evaluate the view that {c}.',
    lambda c, p: f'{p} argues that {c}. How far do you agree? Support your answer with reasoning and evidence.',
    lambda c, p: f'“{cap(c)}.” Discuss this claim, considering arguments for and against before reaching a supported conclusion.',
    lambda c, p: f'Assess the claim that {c}.',
]


def essay_q(r, D, claim, pro, con, judge, hints=(), scene=''):
    m = lm(D)
    p = person(r)
    if D <= 2:
        stem = f'Explain whether you agree that {claim}. Give one reason for and one reason against.'
    else:
        stem = r.choice(ESSAY_LEADS)(claim, p)
        if hints and r.random() < 0.7:
            hs = r.sample(list(hints), min(len(hints), r.choice([2, 3])))
            stem += ' You may wish to consider: ' + '; '.join(hs) + '.'
    if scene:
        stem = scene + ' ' + stem
    ans = 'For: ' + ' '.join(pro) + ' Against: ' + ' '.join(con) + ' Judgement: ' + judge
    key = levels(m, 'simple, one-sided assertions with little support.',
                 'explains arguments on one side well, or both sides in less depth, using some evidence or examples.',
                 'balanced analysis of different perspectives, evidence evaluated for quality, and a reasoned, supported judgement on “to what extent”.')
    return Q(stem, ans, key, m, 'long')


def add_essay(t, claim, pro, con, judge, hints=(), D=(2, 3, 4, 5)):
    def fn(r, D_):
        return essay_q(r, D_, claim, pro, con, judge, hints)
    fn.__name__ = 'essay'
    t.add('C4', D, 'long')(fn)


def add_case(t, intros, parts, C3=(2, 3, 4, 5), C4=(3, 4, 5)):
    """Scenario with fixed parts [(q, a, key-with-[n])]; intros may be callables r -> str."""
    plist = [(lambda r, p=p: p) for p in parts]

    def mk(k):
        def fn(r, D):
            it = r.choice(intros)
            return compose(r, it(r) if callable(it) else it, plist, k=k, type_='case')
        fn.__name__ = 'case'
        return fn
    if C3:
        t.add('C3', C3, 'case')(mk((2, 3)))
    if C4:
        t.add('C4', C4, 'case')(mk((3, 4)))


def table(headers, rows):
    out = ' | '.join(headers) + '. '
    out += ' '.join(' | '.join(str(x) for x in row) + '.' for row in rows)
    return out


def art(w):
    return ('an ' if w[:1].lower() in 'aeiou' else 'a ') + w


# ============================================================== shared issue packs
# Each issue: debatable question, local / national / global dimensions, causes (text, type),
# consequences (text, scale, term), courses of action (action, actor, advantage, limitation),
# perspectives (holder, view, reason), a model argument and a real-world example.

ISSUES = [
    dict(key='turnout', name='low voter turnout among young people', area='Political and governance issues',
         q='Should voting be made compulsory to increase democratic participation?',
         local='a city council election in which fewer than one in four 18–24-year-olds vote',
         national='governments elected on a minority of the eligible electorate, weakening their claim to a mandate',
         globl='a decline in youth turnout reported across many established democracies, which international bodies such as International IDEA monitor and compare',
         causes=[('Many young people move home often, so they are not registered at their current address', 'political'),
                 ('Young people feel that political parties ignore issues that matter to them', 'social'),
                 ('Voting procedures, such as having to vote in person on a working day, are inconvenient', 'political'),
                 ('Low trust in politicians after high-profile scandals', 'social')],
         cons=[('Politicians focus policies on older voters who turn out in higher numbers', 'national', 'long'),
               ('Elected governments can claim less legitimacy', 'national', 'long'),
               ('Young people become less likely to vote later in life, as voting is habit-forming', 'national', 'long'),
               ('Local councils make decisions about youth services with little youth input', 'local', 'short')],
         actions=[('make voting compulsory, with a small fine for non-voters', 'national government',
                   'turnout in Australia, where voting has been compulsory since 1924, is regularly above 90%', 'it may force uninformed or unwilling people to vote, and it limits individual freedom'),
                  ('introduce automatic voter registration', 'electoral commission',
                   'it removes a practical barrier for people who move home often', 'it does not address lack of interest or trust'),
                  ('run citizenship education programmes in schools', 'education ministry',
                   'it builds knowledge and the habit of participation early', 'results take years to appear and depend on teaching quality')],
         persp=[('a youth campaign group', 'supports automatic registration and voting at 16', 'it wants young people’s interests represented'),
                ('a libertarian think tank', 'opposes compulsory voting', 'it believes not voting is a legitimate choice and the state should not coerce citizens'),
                ('a governing party with mostly older voters', 'is reluctant to change voting rules', 'higher youth turnout might help its rivals')],
         arg=dict(conc='voting should be made compulsory', r1='a democracy works best when governments are chosen by the whole electorate',
                  r2='compulsory voting forces parties to address the needs of groups that currently stay at home',
                  ev='In Australia, where voting is compulsory, turnout is usually above 90%', ic='compulsory voting would make elected governments more representative',
                  assume='governments chosen by more of the electorate will be more representative of the electorate’s interests',
                  counter='compulsory voting removes the freedom not to vote', rebut='voters may still spoil their ballot or choose “none of the above”'),
         fact='Australia has had compulsory voting since 1924 and Belgium since 1893.'),
    dict(key='disinfo', name='the spread of online disinformation during elections', area='Digital world',
         q='Should social media companies be legally responsible for false political content on their platforms?',
         local='false rumours about polling station closures shared in a community messaging group',
         national='voters in a national election exposed to misleading political advertisements',
         globl='foreign governments and networks using social media platforms that operate across borders to influence elections in other countries',
         causes=[('Platform algorithms promote content that attracts strong emotional reactions', 'technological'),
                 ('Many users share posts without checking their source', 'social'),
                 ('Political advertising online is cheap and can be targeted at small groups', 'economic'),
                 ('Laws on election advertising were written before social media existed', 'political')],
         cons=[('Voters make choices based on false information', 'national', 'short'),
               ('Trust in election results and in the media falls', 'national', 'long'),
               ('Polarisation increases as people see only content that confirms their views', 'global', 'long'),
               ('Candidates and election officials face online harassment', 'local', 'short')],
         actions=[('require platforms to label and remove false political content', 'national government',
                   'it reduces the reach of the most harmful falsehoods quickly', 'governments or companies may use it to silence legitimate criticism'),
                  ('fund independent fact-checking organisations', 'governments and civil society groups',
                   'fact-checkers can correct claims without the state deciding what is true', 'corrections often reach fewer people than the original false claim'),
                  ('teach media literacy in schools', 'education ministry',
                   'it helps citizens judge sources for themselves in the long term', 'it does little for adults who have already left school')],
         persp=[('a social media company', 'prefers voluntary codes of conduct to new laws', 'regulation would raise its costs and legal risks'),
                ('a press freedom organisation', 'warns against laws that let governments define “fake news”', 'such laws have been used to jail journalists'),
                ('an electoral commission', 'wants transparency rules for online political adverts', 'it is responsible for fair elections')],
         arg=dict(conc='social media companies should be legally responsible for false political content', r1='false political content can change how people vote',
                  r2='platforms profit from the engagement that false content attracts',
                  ev='the 2018 Cambridge Analytica scandal showed that data from millions of Facebook users had been harvested for political targeting',
                  ic='platforms have both the power and the incentive to shape elections',
                  assume='companies are able to tell reliably which political claims are false',
                  counter='this would turn private companies into censors of political speech', rebut='the law could be limited to clearly false factual claims, such as the wrong polling date'),
         fact='The EU Digital Services Act (2022) requires very large platforms to assess and reduce risks to elections.'),
    dict(key='climmig', name='migration caused by climate change', area='Migration and work',
         q='Should people displaced by climate change be given legal refugee status?',
         local='families in a coastal village moving inland after repeated flooding',
         national='rapid growth of informal settlements in a capital city as rural people leave drought-hit land',
         globl='the 1951 Refugee Convention not covering people displaced by environmental change, so no international body is clearly responsible for them',
         causes=[('Rising sea levels threaten low-lying islands and deltas', 'environmental'),
                 ('Repeated droughts destroy the livelihoods of farmers', 'environmental'),
                 ('Poorer countries lack funds to build flood defences', 'economic'),
                 ('Weak international agreements on reducing emissions', 'political')],
         cons=[('Pressure on housing and services in the cities that receive migrants', 'local', 'short'),
               ('Loss of culture and identity for communities that must relocate', 'local', 'long'),
               ('Tension between countries over who should accept climate migrants', 'global', 'long'),
               ('Remittances sent home by migrants support families who stay behind', 'national', 'long')],
         actions=[('extend refugee protection to people displaced by climate change', 'United Nations member states',
                   'it would give displaced people clear legal rights', 'many states fear it would commit them to accepting very large numbers of people'),
                  ('fund adaptation such as sea walls and drought-resistant crops through climate finance', 'richer countries',
                   'it helps people stay in their homes', 'funding promised by richer countries has often been delayed or smaller than pledged'),
                  ('create planned relocation schemes within countries', 'national government',
                   'moves can be organised safely before disaster strikes', 'communities may resist leaving ancestral land')],
         persp=[('the government of a low-lying Pacific island state', 'demands that high-emitting countries accept responsibility', 'its territory may become uninhabitable'),
                ('a populist party in a high-income country', 'opposes new obligations to accept migrants', 'it campaigns on reducing immigration'),
                ('UNHCR', 'recognises climate change as a driver of displacement but uses the existing definition of a refugee', 'it must work within the mandate states have given it')],
         arg=dict(conc='people displaced by climate change should be given legal refugee status', r1='they are forced to leave their homes through no fault of their own',
                  r2='the countries that caused most emissions have a duty to help those harmed', ev='the UN Human Rights Committee ruled in the Teitiota case (2020) that states may not return people to places where climate change threatens their right to life',
                  ic='climate migrants deserve the same protection as other forcibly displaced people',
                  assume='being forced to leave home is the key feature that should define who is a refugee',
                  counter='widening the definition could weaken protection for people fleeing persecution', rebut='a separate protocol could protect climate migrants without changing the 1951 Convention'),
         fact='In Teitiota v New Zealand (2020) the UN Human Rights Committee accepted that climate change could in future trigger states’ duty not to return people.'),
    dict(key='corrupt', name='corruption in public procurement', area='Political and governance issues',
         q='How effective are anti-corruption agencies at reducing corruption in government contracts?',
         local='a city road contract awarded to a company owned by a councillor’s relative',
         national='public money lost on overpriced hospital and school building contracts',
         globl='bribes paid by multinational companies to win contracts abroad and money hidden in offshore financial centres',
         causes=[('Officials have wide discretion and little oversight when awarding contracts', 'political'),
                 ('Public sector pay is low compared with the value of the contracts officials control', 'economic'),
                 ('Contract information is not published, so citizens cannot check it', 'political'),
                 ('Companies see bribes as a normal cost of doing business', 'economic')],
         cons=[('Public services such as hospitals are of lower quality or cost more', 'national', 'long'),
               ('Citizens lose trust in government institutions', 'national', 'long'),
               ('Foreign investors avoid countries seen as corrupt', 'global', 'long'),
               ('Honest local firms lose business to connected competitors', 'local', 'short')],
         actions=[('publish all public contracts online (open contracting)', 'national government',
                   'citizens, journalists and rival firms can spot suspicious deals', 'publication alone does not punish anyone'),
                  ('create an independent anti-corruption agency with powers to prosecute', 'parliament',
                   'it can investigate powerful officials without political interference', 'agencies can be captured or starved of funds by the politicians they investigate'),
                  ('enforce laws against foreign bribery, such as the UK Bribery Act 2010', 'governments of companies’ home countries',
                   'it tackles the supply side of bribery', 'enforcement against powerful multinationals is slow and costly')],
         persp=[('Transparency International', 'campaigns for open contracting and stronger enforcement', 'it is an NGO whose mission is to fight corruption'),
                ('a business association', 'supports simpler procurement rules', 'complex rules raise costs for its members'),
                ('a government minister accused of corruption', 'claims the investigation is politically motivated', 'he wants to protect his reputation and position')],
         arg=dict(conc='every government should publish all public contracts online', r1='corruption thrives when deals are hidden from public view',
                  r2='publication allows journalists and citizens to act as watchdogs', ev='after Ukraine introduced its ProZorro e-procurement system in 2016, many observers reported savings on public purchases',
                  ic='open contracting makes corruption harder to hide',
                  assume='people will actually use published contract information to scrutinise deals',
                  counter='publishing contracts could reveal commercially sensitive information', rebut='sensitive details can be redacted while prices and winners are published'),
         fact='The UN Convention against Corruption (2003) is the only legally binding universal anti-corruption treaty.'),
    dict(key='unsc', name='reform of the UN Security Council', area='Political and governance issues',
         q='Should the permanent members of the UN Security Council lose their veto power?',
         local='a community group in a war-affected town waiting for UN peacekeepers who are not sent',
         national='a large democracy such as India or Brazil with no permanent seat on the Council',
         globl='five permanent members (China, France, Russia, the UK and the USA) able to block action on conflicts that affect the whole world',
         causes=[('The Council’s structure reflects the balance of power in 1945', 'political'),
                 ('Any change to the UN Charter can be vetoed by the permanent members', 'political'),
                 ('Regional rivals disagree about which countries should get new seats', 'political'),
                 ('The global population and economy have shifted towards Asia, Africa and Latin America', 'economic')],
         cons=[('The Council fails to act on some humanitarian crises because of a veto', 'global', 'short'),
               ('Countries in Africa feel under-represented, reducing the UN’s legitimacy', 'global', 'long'),
               ('States act outside the UN, through regional alliances', 'global', 'long'),
               ('Civilians in conflicts may not receive protection', 'local', 'short')],
         actions=[('abolish or restrict the veto for cases of mass atrocities', 'UN member states',
                   'it would stop one country blocking action to prevent genocide', 'the permanent members would have to agree, and they can veto Charter amendments'),
                  ('add new permanent members such as the G4 (Brazil, Germany, India, Japan) and African states', 'UN member states',
                   'it would make the Council more representative of today’s world', 'regional rivals oppose specific candidates, so agreement is hard to reach'),
                  ('require permanent members to explain each veto to the General Assembly', 'UN General Assembly',
                   'it raises the political cost of using the veto', 'it cannot overturn a veto')],
         persp=[('the African Union (the Ezulwini Consensus)', 'demands two permanent seats with veto power for Africa', 'Africa has no permanent seat although many Council items concern African conflicts'),
                ('a permanent member', 'defends the veto', 'it protects its national interests and allies'),
                ('a human rights NGO', 'calls for veto restraint in cases of mass atrocity', 'it focuses on protecting civilians')],
         arg=dict(conc='the veto power of the permanent members should be restricted', r1='a single country can block action supported by most of the world',
                  r2='the permanent members were chosen in 1945 and do not reflect today’s world', ev='Russia has vetoed draft resolutions on the war in Syria many times since 2011',
                  ic='the veto prevents the Council from fulfilling its responsibility for international peace',
                  assume='without the veto the Council would act more effectively on crises',
                  counter='the veto keeps the great powers inside the UN system', rebut='a restriction only in cases of mass atrocities would leave most of their influence intact'),
         fact='Under Article 108 of the UN Charter, amendments need ratification by two-thirds of members including all five permanent members.'),
    dict(key='vote16', name='lowering the voting age to 16', area='Political and governance issues',
         q='Should the voting age be lowered to 16?',
         local='16-year-olds in a town affected by a decision to close the local youth centre who cannot vote on it',
         national='a parliament debating whether 16- and 17-year-olds should vote in general elections',
         globl='different voting ages around the world, with Austria, Brazil and Argentina allowing voting at 16',
         causes=[('Young people are affected by long-term decisions on climate and debt', 'social'),
                 ('Youth campaign groups have become better organised', 'political'),
                 ('16-year-olds can already work and pay tax in many countries', 'economic'),
                 ('Political parties hope to gain young voters’ support', 'political')],
         cons=[('A larger electorate that includes people still at school', 'national', 'short'),
               ('Parties pay more attention to education and climate policy', 'national', 'long'),
               ('First-time voters may form a lifelong voting habit while still living at home', 'national', 'long'),
               ('Schools need to provide more political education', 'local', 'short')],
         actions=[('lower the voting age to 16 for all elections', 'parliament',
                   'it gives a voice to people affected by long-term decisions', 'critics argue many 16-year-olds are not yet ready to vote'),
                  ('lower the voting age to 16 for local elections first', 'local government',
                   'its effects can be tested before national change', 'young people may see it as a token gesture'),
                  ('keep the age at 18 but improve citizenship education', 'education ministry',
                   'it prepares young people before they vote', 'it does not give under-18s a voice now')],
         persp=[('a student union', 'supports voting at 16', 'its members are directly affected'),
                ('a conservative columnist', 'opposes lowering the age', 'she believes adulthood and full rights should start at 18'),
                ('a political scientist who has studied Austria', 'reports that 16- and 17-year-olds there turned out at rates similar to young adults', 'she bases her view on election data')],
         arg=dict(conc='the voting age should be lowered to 16', r1='16-year-olds will live longest with the results of today’s decisions',
                  r2='people who vote in their first election are more likely to keep voting', ev='after Austria lowered the voting age to 16 in 2007, studies found that 16- and 17-year-olds turned out at rates similar to slightly older first-time voters',
                  ic='votes at 16 could build a habit of lifelong participation',
                  assume='16-year-olds are mature enough to make informed voting decisions',
                  counter='16-year-olds are easily influenced by parents and teachers', rebut='research finds young voters’ choices are no less consistent with their own views than older voters’'),
         fact='Austria became the first EU country to lower the voting age to 16 for national elections, in 2007.'),
    dict(key='quotas', name='the under-representation of women in parliaments', area='Political and governance issues',
         q='Are gender quotas the best way to increase the number of women in parliament?',
         local='a municipal council in which only two of twenty councillors are women',
         national='a parliament in which fewer than one in five members are women',
         globl='a world average of roughly a quarter of parliamentary seats held by women, which the Inter-Parliamentary Union tracks, and the UN Sustainable Development Goal 5 on gender equality',
         causes=[('Parties choose men for safe seats more often than women', 'political'),
                 ('Women carry more unpaid caring work, leaving less time for politics', 'social'),
                 ('Women politicians face more online abuse', 'social'),
                 ('Cultural stereotypes that leadership is a male role', 'social')],
         cons=[('Policies on issues such as childcare and violence against women receive less attention', 'national', 'long'),
               ('Fewer female role models for girls considering politics', 'local', 'long'),
               ('Parliaments are seen as less legitimate by half the population', 'national', 'long'),
               ('A country scores poorly in international gender equality rankings', 'global', 'short')],
         actions=[('introduce legal candidate quotas requiring parties to field a minimum share of women', 'parliament',
                   'Rwanda, which has reserved seats for women, has had a female majority in its lower house since 2008', 'critics argue quotas may be seen as undermining selection on merit'),
                  ('introduce voluntary party quotas or all-women shortlists', 'political parties',
                   'parties can act quickly without new laws', 'parties may only apply them to seats they cannot win'),
                  ('provide childcare and flexible sitting hours in parliament', 'parliament',
                   'it removes practical barriers for candidates with caring responsibilities', 'it does not address bias in candidate selection')],
         persp=[('UN Women', 'supports temporary special measures such as quotas', 'it works for gender equality under SDG 5'),
                ('a party official', 'prefers selection “on merit”', 'he believes quotas restrict local members’ choice'),
                ('a female MP elected through a quota', 'argues quotas opened doors that had been closed', 'she has personal experience of the selection process')],
         arg=dict(conc='countries should introduce legal gender quotas for parliament', r1='voluntary efforts have increased women’s representation only slowly',
                  r2='parliaments that reflect the population make better-informed laws', ev='Rwanda’s constitution reserves 30% of seats for women, and women have held a majority of its lower house since 2008',
                  ic='legal requirements are needed to change who is selected',
                  assume='having more women in parliament will change the decisions that parliament makes',
                  counter='quotas mean candidates are chosen because of gender rather than ability', rebut='quotas widen the pool of candidates and parties still choose among them'),
         fact='Rwanda’s 2003 constitution reserves at least 30% of decision-making posts for women.'),
    dict(key='surveil', name='state use of facial recognition surveillance', area='Digital world',
         q='Should governments be allowed to use live facial recognition in public places?',
         local='a city installing facial recognition cameras in a busy shopping street',
         national='a national police database of facial images built without a specific law authorising it',
         globl='surveillance technology sold by companies in one country to governments in many others, some of which use it against protesters',
         causes=[('The cost of cameras and computing power has fallen sharply', 'technological'),
                 ('Governments face pressure to prevent crime and terrorism', 'political'),
                 ('Data protection laws do not cover new technologies clearly', 'political'),
                 ('Technology companies market surveillance systems aggressively', 'economic')],
         cons=[('People may avoid protests for fear of being identified', 'national', 'long'),
               ('Misidentification, which studies have found is more common for some ethnic groups', 'local', 'short'),
               ('Some crimes are solved faster', 'local', 'short'),
               ('Authoritarian governments gain more control over citizens', 'global', 'long')],
         actions=[('ban live facial recognition in public places', 'parliament',
                   'it protects privacy and freedom of assembly', 'police lose a tool that can help find suspects'),
                  ('allow it only with a court warrant and independent audits', 'parliament',
                   'it balances security with legal safeguards', 'oversight bodies may lack technical expertise'),
                  ('restrict exports of surveillance technology to countries with poor human rights records', 'exporting governments',
                   'it reduces misuse abroad', 'buyers may turn to suppliers in countries without restrictions')],
         persp=[('a police chief', 'supports facial recognition', 'she believes it helps catch dangerous offenders'),
                ('a civil liberties group', 'calls for a ban', 'it defends privacy and freedom of assembly'),
                ('a technology company that sells cameras', 'argues the technology is accurate and safe', 'it profits from sales')],
         arg=dict(conc='governments should ban live facial recognition in public places', r1='it records everyone, not only suspects',
                  r2='mistaken identifications fall more often on some ethnic groups', ev='a 2019 study by the US National Institute of Standards and Technology found higher false-match rates for some demographic groups in many algorithms',
                  ic='the technology threatens the rights of innocent people',
                  assume='the harm to innocent people outweighs the benefits for public safety',
                  counter='the technology helps police find missing people and dangerous suspects', rebut='these aims can be met with targeted searches authorised by a judge'),
         fact='The EU AI Act (2024) restricts real-time remote biometric identification by police in public spaces to narrow exceptions.'),
    dict(key='press', name='threats to press freedom', area='Political and governance issues',
         q='How far should governments be able to restrict the media in the name of national security?',
         local='a local reporter threatened after exposing a council official’s links to a building firm',
         national='a law that allows a government to shut down news websites accused of “spreading falsehoods”',
         globl='journalists jailed or killed in many countries, recorded each year by Reporters Without Borders and the Committee to Protect Journalists',
         causes=[('Governments want to control criticism before elections', 'political'),
                 ('Media owners have business links with ruling parties', 'economic'),
                 ('Advertising revenue for independent newspapers has collapsed', 'economic'),
                 ('Broad security laws give officials wide powers', 'political')],
         cons=[('Corruption and abuses go unreported', 'national', 'long'),
               ('Self-censorship among journalists', 'national', 'long'),
               ('Citizens rely on social media rumours rather than verified news', 'local', 'short'),
               ('International criticism and possible sanctions', 'global', 'short')],
         actions=[('protect journalists’ sources and repeal broad “false news” laws', 'parliament',
                   'it allows investigative journalism to hold power to account', 'governments say some restrictions are needed during emergencies'),
                  ('fund public-interest journalism through independent trusts', 'government and philanthropists',
                   'it supports reporting that the market will not pay for', 'funders may try to influence content'),
                  ('raise press freedom in trade and aid agreements', 'foreign governments',
                   'external pressure can protect individual journalists', 'it may be seen as interference in domestic affairs')],
         persp=[('a government spokesperson', 'argues restrictions protect national security', 'the government wants to limit critical coverage'),
                ('Reporters Without Borders', 'condemns the restrictions', 'it is an NGO that defends press freedom'),
                ('a citizen who relies on state television', 'trusts official news', 'she has little access to alternative sources')],
         arg=dict(conc='governments should repeal broad “false news” laws', r1='such laws are vague and let officials decide what is true',
                  r2='a free press is needed to expose corruption', ev='press freedom organisations have documented journalists jailed under “false news” laws in several countries',
                  ic='these laws are more often used to silence critics than to protect the public',
                  assume='governments cannot be trusted to judge fairly what counts as false news',
                  counter='false reports can cause panic during a crisis', rebut='existing laws on defamation and incitement already deal with genuinely harmful falsehoods'),
         fact='Article 19 of the Universal Declaration of Human Rights (1948) protects freedom of opinion and expression.'),
    dict(key='water', name='disputes over shared rivers', area='Water, food and agriculture',
         q='Should countries upstream on a shared river need the agreement of downstream countries before building dams?',
         local='farmers downstream noticing lower river levels during the dry season',
         national='a government building a large hydroelectric dam to supply electricity to millions of homes',
         globl='more than 260 river basins shared by two or more countries, with weak international law on how to share the water',
         causes=[('Population growth increases demand for water and food', 'social'),
                 ('Upstream countries want hydroelectric power for development', 'economic'),
                 ('Old treaties gave most of the water to downstream countries', 'political'),
                 ('Climate change makes rainfall less reliable', 'environmental')],
         cons=[('Diplomatic tension and threats between neighbouring states', 'global', 'short'),
               ('Electricity for millions of people in the upstream country', 'national', 'long'),
               ('Reduced water for irrigation downstream', 'local', 'long'),
               ('Loss of river ecosystems and fisheries', 'local', 'long')],
         actions=[('negotiate a basin-wide water-sharing treaty', 'riverside governments',
                   'it gives every country a say and reduces conflict', 'negotiations can take decades'),
                  ('ask a neutral mediator such as the African Union or the World Bank to help', 'riverside governments',
                   'a neutral party can build trust', 'states may reject recommendations'),
                  ('share real-time data on dam filling and river flows', 'dam operator',
                   'downstream countries can plan ahead', 'it does not settle how much water each country receives')],
         persp=[('the government of Ethiopia', 'argues the Grand Ethiopian Renaissance Dam is vital for development', 'millions of its people lack electricity'),
                ('the government of Egypt', 'fears reduced Nile flows', 'it depends on the Nile for most of its fresh water'),
                ('an environmental NGO', 'warns about damage to river ecosystems', 'its mission is to protect biodiversity')],
         arg=dict(conc='upstream countries should agree dam operations with downstream neighbours', r1='downstream countries depend on the river for drinking water and farming',
                  r2='agreed rules reduce the risk of conflict', ev='the Indus Waters Treaty between India and Pakistan (1960) has survived several wars',
                  ic='shared rules can make water a source of cooperation rather than conflict',
                  assume='countries will keep to an agreement once it is signed',
                  counter='upstream countries have the right to use resources on their own territory', rebut='international water law also requires them not to cause significant harm to others'),
         fact='Ethiopia began filling the Grand Ethiopian Renaissance Dam on the Blue Nile in 2020.'),
    dict(key='plastic', name='the export of plastic waste to poorer countries', area='Sustainable living',
         q='Should richer countries be banned from exporting plastic waste?',
         local='open burning of imported plastic near a recycling yard, causing breathing problems for nearby residents',
         national='a government deciding whether to ban imports of foreign plastic waste',
         globl='plastic waste shipped from high-income countries to South-East Asia after China restricted imports in 2018',
         causes=[('Recycling at home is more expensive than shipping waste abroad', 'economic'),
                 ('Mixed plastics are hard to recycle', 'technological'),
                 ('Weak enforcement of waste rules in receiving countries', 'political'),
                 ('Consumers in rich countries use large amounts of single-use plastic', 'social')],
         cons=[('Air and water pollution near recycling sites', 'local', 'short'),
               ('Health problems for informal waste workers', 'local', 'long'),
               ('Plastic leaking into rivers and oceans', 'global', 'long'),
               ('Income and jobs in the recycling trade', 'national', 'short')],
         actions=[('tighten international rules on plastic waste trade', 'parties to the Basel Convention',
                   'the 2019 Basel amendments require consent before contaminated plastic waste is shipped', 'illegal shipments can still be disguised'),
                  ('ban exports and build domestic recycling capacity', 'exporting governments',
                   'countries take responsibility for their own waste', 'it is costly and takes time'),
                  ('make producers pay for collection and recycling (extended producer responsibility)', 'national government',
                   'it gives firms an incentive to design recyclable packaging', 'costs may be passed on to consumers')],
         persp=[('an environmental NGO in Malaysia', 'calls for a total ban on imports', 'it sees local communities harmed'),
                ('a waste trading company', 'argues the trade supplies raw materials', 'it earns profits from shipping waste'),
                ('the government of an exporting country', 'claims its waste is recycled responsibly', 'it wants to meet recycling targets cheaply')],
         arg=dict(conc='richer countries should be banned from exporting plastic waste', r1='much exported plastic is not recycled but burned or dumped',
                  r2='countries that consume the plastic should bear the cost of dealing with it', ev='after China’s 2018 import restrictions, Malaysia returned hundreds of containers of illegally imported plastic waste to their countries of origin',
                  ic='exporting waste shifts the harm onto poorer communities',
                  assume='exporting countries could manage the waste better at home',
                  counter='trade in sorted, clean plastic provides useful raw materials', rebut='a ban could be limited to mixed and contaminated plastic'),
         fact='Amendments to the Basel Convention on plastic waste took effect in 2021.'),
    dict(key='sanctions', name='the use of economic sanctions', area='Conflict and peace',
         q='Are economic sanctions an effective way to change a government’s behaviour?',
         local='a pharmacy unable to import medicines because banks will not process payments',
         national='an economy in recession after its oil exports are restricted',
         globl='sanctions imposed by the UN Security Council, the EU or the USA affecting trade and finance around the world',
         causes=[('States want a response to aggression that stops short of war', 'political'),
                 ('A government violates international law or human rights', 'political'),
                 ('Global banking makes financial sanctions easier to enforce', 'economic'),
                 ('Domestic public opinion demands that the government “does something”', 'political')],
         cons=[('Shortages and price rises for ordinary citizens', 'national', 'short'),
               ('Elites may avoid sanctions while the poor suffer', 'national', 'long'),
               ('Trade diverted to countries that do not apply the sanctions', 'global', 'long'),
               ('Pressure on the targeted government to negotiate', 'global', 'short')],
         actions=[('use targeted (“smart”) sanctions on named individuals and firms', 'UN Security Council or regional bodies',
                   'they aim at decision-makers rather than the whole population', 'assets can be moved to relatives or hidden'),
                  ('combine sanctions with diplomacy and clear conditions for lifting them', 'sanctioning governments',
                   'the target knows what it must do', 'the target may not trust promises to lift sanctions'),
                  ('allow humanitarian exemptions for food and medicine', 'UN Security Council',
                   'they reduce harm to civilians', 'banks may still refuse payments to avoid risk')],
         persp=[('the government imposing sanctions', 'argues they punish aggression', 'it wants to show strength without military action'),
                ('a humanitarian NGO', 'warns about harm to civilians', 'it delivers aid to the affected population'),
                ('the targeted government', 'calls the sanctions illegal interference', 'it wants to blame external enemies for economic problems')],
         arg=dict(conc='economic sanctions are rarely an effective way to change a government’s behaviour', r1='targeted governments can blame foreigners for economic hardship',
                  r2='ordinary citizens suffer more than the leaders responsible', ev='decades of US sanctions on Cuba since the 1960s have not changed its system of government',
                  ic='sanctions often strengthen rather than weaken the targeted regime',
                  assume='the purpose of sanctions is to change the target’s behaviour rather than to signal disapproval',
                  counter='sanctions helped end apartheid in South Africa', rebut='in that case sanctions worked alongside strong internal resistance'),
         fact='UN sanctions under Article 41 of the UN Charter are measures “not involving the use of armed force”.'),
]
ISSUE = {i['key']: i for i in ISSUES}
for _i in ISSUES:
    _i['global'] = _i.pop('globl')


def issue(r, avoid=()):
    return r.choice([i for i in ISSUES if i['key'] not in avoid])


LEVEL_WORD = {'local': 'local', 'national': 'national', 'global': 'global'}
CAUSE_TYPES = ['political', 'economic', 'social', 'technological', 'environmental']
NEWS = ['a news website', 'a radio report', 'a local newspaper', 'a television news bulletin', 'a community newsletter', 'a podcast episode']


def news_intro(r, i):
    c = city(r)
    return r.choice([
        f'Read this extract from {r.choice(NEWS)} in {c}: “Residents are concerned about {i["local"]}.”',
        f'A student in {c} reads a report about {i["local"]}.',
        f'{person(r)}, a student in {c}, is investigating {i["name"]} after noticing {i["local"]}.',
        f'A report from {c} describes {i["local"]}. The issue is part of a wider debate about {i["name"]}.',
    ])


# ============================================================== CHAPTER 1: Global issues and topics

c1a = T('What makes an issue global: local, national and global dimensions', 'local national global dimensions', 'global issue')
add_terms(c1a, [
    ('global issue', 'an issue that affects people in many parts of the world and cannot be solved by one country acting alone'),
    ('local dimension', 'the way an issue affects or is experienced by a particular community or place'),
    ('national dimension', 'the way an issue affects a whole country and is dealt with by its government and laws'),
    ('global dimension', 'the way an issue crosses borders, affecting many countries and requiring international cooperation'),
    ('globalisation', 'the growing interconnection of economies, cultures and societies through trade, travel, migration and communication'),
    ('interdependence', 'the situation in which countries rely on each other, so events in one place affect others'),
    ('sovereignty', 'the authority of a state to govern itself without outside interference'),
    ('intergovernmental organisation', 'a body whose members are states, such as the United Nations or the African Union'),
])
add_mcqs(c1a, 'C1', (1, 2, 3), [
    ('Which organisation’s membership is made up of 193 sovereign states?', 'The United Nations General Assembly', ['Amnesty International', 'The European Commission', 'The International Committee of the Red Cross'],
     'The UN has 193 member states, all represented in the General Assembly.'),
    ('Which of the following is a non-governmental organisation (NGO)?', 'Amnesty International', ['The World Trade Organization', 'The African Union', 'The UN Security Council'],
     'Amnesty International is an independent NGO; the others are intergovernmental bodies.'),
    ('Which feature most clearly makes an issue global rather than national?', 'Its causes or effects cross national borders, so no single government can solve it alone',
     ['It is reported on national television', 'It affects a large number of people in one country', 'It is debated in a national parliament'],
     'Global = transnational causes/effects needing cooperation.'),
])
add_ar(c1a, [
    ('The spread of election disinformation is a global issue.', 'Social media platforms operate across national borders.', 'AR', 'Both true; cross-border platforms are why the issue is global.'),
    ('Climate migration is only a national issue.', 'Most people displaced by climate change move within their own country.', 'R',
     'A is false: it also has global dimensions (cross-border migration, no international legal status). R is broadly true: most displacement is internal.'),
    ('Sovereignty can make global issues harder to solve.', 'States can refuse to accept international agreements.', 'AR', 'Both true and R explains A.'),
    ('Local actions are irrelevant to global issues.', 'Global issues need international cooperation.', 'R', 'A is false: local action can contribute and reveals local dimensions. R is true but does not make local action irrelevant.'),
])
add_claims(c1a, [
    ('An issue is global only if it affects every country equally.', False, 'Global issues cross borders and affect many countries, but the impact is often very unequal, e.g. climate migration hits low-lying states hardest.'),
    ('Most global issues have local, national and global dimensions at the same time.', True, 'For example, low youth turnout is seen in a city election (local), affects a government’s mandate (national) and is a trend across many democracies (global).'),
    ('Globalisation has made countries more interdependent.', True, 'Trade, finance, migration and communication link countries, so events in one place affect others.'),
    ('If a national government passes a law on an issue, the issue is no longer global.', False, 'A national law addresses the national dimension; cross-border causes and effects remain and need cooperation.'),
])


def _dim_mcq(r, D):
    i = issue(r)
    lv = r.choice(['local', 'national', 'global'])
    others = [x for x in ('local', 'national', 'global') if x != lv]
    c = i['causes'][r.randrange(len(i['causes']))][0]
    stem = r.choice([f'A student is researching {i["name"]}. Which of the following is a {lv} dimension of this issue?',
                     f'Which of the following best describes the {lv} dimension of {i["name"]}?',
                     f'In an investigation of {i["name"]}, which example illustrates the {lv} dimension?'])
    return MC(r, stem, cap(i[lv]), [cap(i[o]) for o in others] + [cap(low(c))],
              f'{cap(lv)} dimension: {i[lv]}. The others are the {others[0]} and {others[1]} dimensions, and a cause of the issue.')


c1a.add('C1', (1, 2, 3), 'mcq')(_dim_mcq)


@c1a.add('C2', (1, 2, 3, 4), 'explain')
def c1a_why_global(r, D):
    i = issue(r)
    m = 2 if D <= 2 else 3
    stem = r.choice([f'Explain why {i["name"]} can be described as a global issue.',
                     f'{person(r)} says that {i["name"]} is “just a problem for individual countries”. Explain why this view is too narrow.',
                     f'Explain how {i["name"]} has both national and global dimensions.'])
    ans = f'National: {cap(i["national"])}. Global: {cap(i["global"])}. Because causes and effects cross borders, no single government can solve it alone.'
    key = '1 mark identifies a cross-border cause or effect; 1 mark develops with an example' + ('; 1 mark explains why international cooperation is needed' if m == 3 else '') + f' [{m}]'
    return Q(stem, ans, key, m, 'explain')


def c1a_parts(i):
    return [
        lambda r: ('Identify the local dimension of the issue described.', cap(i['local']) + '.', '1 mark for the local example [1]'),
        lambda r: (f'Suggest one national dimension of {i["name"]}.', cap(i['national']) + '.', '1 mark national example; 1 mark explains link to government or laws [2]'),
        lambda r: ('Explain why this issue also has a global dimension.', cap(i['global']) + '.', '1 mark cross-border cause/effect; 1 mark developed with example [2]'),
        lambda r: ('Suggest why action at a local level alone may not solve the issue.', f'The causes are partly national and global ({low(i["causes"][0][0])}), so local action cannot change them; national laws and international cooperation are also needed.',
                   '1 mark cause outside local control; 1 mark need for wider action [2]'),
        lambda r: (f'Explain one way in which a course of action by the {i["actions"][0][1]} could affect the local community.', f'If the {i["actions"][0][1]} decided to {i["actions"][0][0]}, the community would feel the effect: {i["actions"][0][2]}; however {i["actions"][0][3]}.',
                   '1 mark identifies effect; 1 mark explains link from national/global action to local [2]'),
    ]


@c1a.add('C3', (2, 3, 4, 5), 'case')
def c1a_case(r, D):
    i = issue(r)
    return compose(r, news_intro(r, i), c1a_parts(i), k=(2, 3), type_='case')


@c1a.add('C4', (3, 4, 5), 'case')
def c1a_case4(r, D):
    i = issue(r)
    return compose(r, news_intro(r, i), c1a_parts(i), k=(3, 4), type_='case')


@c1a.add('C4', (2, 3, 4, 5), 'long')
def c1a_essay(r, D):
    i = issue(r)
    a = i['actions']
    return essay_q(r, D, f'{i["name"]} can only be solved through international cooperation',
                   [f'{cap(i["global"])}.', f'Possible international action: {a[0][0]} ({a[0][1]}).'],
                   [f'Much of the problem is national or local: {i["national"]}.', f'National or local action such as to {a[-1][0]} can make a difference: {a[-1][2]}.'],
                   'International cooperation is necessary for the cross-border dimensions, but most effective responses combine it with national and local action.',
                   ['local, national and global dimensions', 'sovereignty', 'the role of international organisations', 'evidence of what has worked'])


c1b = T('Exploring the AS topic areas: e.g. political and governance issues, environment, technology and society', 'topic areas political governance environment technology society')
FAR_AREAS = ['Sport and recreation', 'Arts in society', 'Medical ethics', 'Transport and infrastructure', 'Language and communication', 'Humans and other species']
add_terms(c1b, [
    ('governance', 'the processes and institutions through which decisions are made and power is exercised in a society'),
    ('democracy', 'a system of government in which citizens choose their rulers through free and fair elections'),
    ('human rights', 'basic rights and freedoms that belong to every person, set out in documents such as the Universal Declaration of Human Rights (1948)'),
    ('rule of law', 'the principle that everyone, including the government, is subject to and accountable under the law'),
    ('legitimacy', 'the acceptance by citizens that those in power have the right to rule'),
    ('civil society', 'organised groups outside government and business, such as NGOs, unions and community groups'),
])


@c1b.add('C1', (1, 2, 3), 'mcq')
def c1b_area(r, D):
    i = issue(r)
    stem = r.choice([f'A news report discusses {i["name"]}. Which topic area is it most closely linked to?',
                     f'{person(r)} wants to research {i["name"]}. Under which topic area would this issue most naturally fall?'])
    return MC(r, stem, i['area'], r.sample(FAR_AREAS, 3), f'{cap(i["name"])} belongs most clearly to “{i["area"]}”.')


@c1b.add('C1', (1, 2, 3), 'mcq')
def c1b_type(r, D):
    i = issue(r)
    c, ty = r.choice(i['causes'])
    return MC(r, f'In a study of {i["name"]}, which kind of factor is this: “{c}”?', cap(ty) + ' factor',
              [cap(x) + ' factor' for x in CAUSE_TYPES if x != ty], f'This is mainly a {ty} factor. [1]')


@c1b.add('C2', (1, 2, 3, 4), 'explain')
def c1b_links(r, D):
    i = issue(r)
    (c1, t1), (c2, t2) = r.sample(i['causes'], 2)
    if t1 == t2:
        return None
    stem = f'Using {i["name"]} as an example, explain how one global issue can involve more than one topic area.'
    ans = f'It is linked to {i["area"]}, but it also has a {t1} side (“{low(c1)}”) and a {t2} side (“{low(c2)}”)' + ('; governments must decide how to respond, so it is also a political and governance issue.' if i['area'] != 'Political and governance issues' else ', so it reaches beyond formal politics into other topic areas such as society and the economy.')
    return Q(stem, ans, '1 mark identifies one topic area; 1 mark a second area with an example from the issue; 1 mark explains the link [3]', 3, 'explain')


@c1b.add('C3', (2, 3, 4, 5), 'case')
def c1b_case(r, D):
    i = issue(r)
    tys = sorted({t for _, t in i['causes']})
    ty = r.choice(tys)
    cs = [c for c, t in i['causes'] if t == ty]
    parts = [
        lambda r: ('Identify the topic area this issue most clearly belongs to.', i['area'] + '.', '1 mark [1]'),
        lambda r: (f'Identify one {ty} factor that contributes to the issue.', cs[0] + '.', '1 mark [1]'),
        lambda r: ('Name two groups whose perspectives on the issue a student could research.', f'{cap(i["persp"][0][0])}; {i["persp"][1][0]}.', '1 mark each [2]'),
        lambda r: ('Explain why governments are involved in responding to this issue.', f'Governments make laws and policies, for example a {i["actions"][0][1]} could {i["actions"][0][0]}; {i["actions"][0][2]}.',
                   '1 mark identifies government action; 1 mark explains its purpose [2]'),
        lambda r: ('Suggest one piece of evidence a student could look for to judge how serious the issue is.', f'For example, data on how many people experience {i["local"]}, or on {low(i["cons"][0][0])}.',
                   '1 mark relevant evidence; 1 mark explains what it would show [2]'),
    ]
    return compose(r, news_intro(r, i), parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c1b.add('C4', (2, 3, 4, 5), 'long')
def c1b_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'{i["name"]} is better understood as a political issue than as an issue of {low(i["area"]) if i["area"] != "Political and governance issues" else "technology or society"}',
                   ['Governments and international bodies decide the rules and the response.', f'For example, {i["actions"][0][1]} could {i["actions"][0][0]}.'],
                   [f'Its causes include {low(i["causes"][1][0])}, which is not mainly political.', 'Non-state actors such as businesses, NGOs and individuals also shape it.'],
                   'The issue is best understood across topic areas; politics shapes the response but other factors drive the causes.')


c1c = T('Framing a global issue as a question', 'framing a global issue as a question', 'question')
add_terms(c1c, [
    ('debatable question', 'a question to which reasonable people can give different answers supported by evidence'),
    ('closed question', 'a question with a single factual or yes/no answer that leaves no room for debate'),
    ('leading question', 'a question worded so that it suggests or assumes a particular answer'),
    ('scope', 'the range of places, groups and time covered by an enquiry'),
    ('enquiry question', 'a focused question that guides research into an issue'),
])
WEAK = {
    'closed': 'It is a closed, factual question with no room for debate',
    'broad': 'It is too broad to research in depth',
    'leading': 'It is a leading question that assumes the answer',
    'local': 'It has no global dimension and no room for different perspectives',
}


def weak_q(r, i, kind):
    c = city(r)
    if kind == 'closed':
        return r.choice([f'In which year did the debate about {i["name"]} begin?', f'How many countries are affected by {i["name"]}?', f'What is meant by {i["name"]}?'])
    if kind == 'broad':
        return r.choice([f'What is wrong with the world’s approach to {low(i["area"])}?', 'How can global politics be improved?', f'What are all the problems facing {low(i["area"])} today?'])
    if kind == 'leading':
        return r.choice([f'Why is it obvious that {i["arg"]["conc"]}?', f'Why do only selfish people oppose the view that {i["arg"]["conc"]}?'])
    return r.choice([f'Should the council in {c} change the opening hours of its town hall?', f'Which café in {c} should host the next student debate?'])


@c1c.add('C1', (1, 2, 3), 'mcq')
def c1c_best(r, D):
    i = issue(r)
    ks = r.sample(list(WEAK), 3)
    stem = r.choice([f'Which question would be most effective for a Global Perspectives enquiry into {i["name"]}?',
                     f'{person(r)} is choosing an enquiry question about {i["name"]}. Which question is best?'])
    return MC(r, stem, i['q'], [weak_q(r, i, k) for k in ks], 'The best question is focused, open, debatable and has a global dimension.')


@c1c.add('C2', (1, 2, 3), 'mcq')
def c1c_weak(r, D):
    i = issue(r)
    k = r.choice(list(WEAK))
    q = weak_q(r, i, k)
    return MC(r, f'A student proposes this enquiry question: “{q}” What is its main weakness?', WEAK[k], [v for kk, v in WEAK.items() if kk != k],
              f'{WEAK[k]}.')


@c1c.add('C2', (2, 3, 4), 'explain')
def c1c_explain(r, D):
    i = issue(r)
    k = r.choice(list(WEAK))
    q = weak_q(r, i, k)
    why = {'closed': 'it can be answered with a single fact, so there are no competing perspectives or arguments to evaluate',
           'broad': 'it covers far too many issues and places to research in depth within an essay',
           'leading': 'its wording assumes the answer, so it discourages consideration of other perspectives',
           'local': 'it concerns one place only and is not a global issue, so different national and global perspectives cannot be compared'}[k]
    return Q(f'Explain why “{q}” is not an effective question for a Global Perspectives enquiry.', f'{WEAK[k]}: {why}.',
             '1 mark identifies the weakness; 1 mark explains why it limits the enquiry [2]', 2, 'explain')


@c1c.add('C3', (2, 3, 4, 5), 'explain')
def c1c_rewrite(r, D):
    i = issue(r)
    k = r.choice(['closed', 'broad', 'leading'])
    q = weak_q(r, i, k)
    m = 3 if D <= 3 else 4
    stem = f'{person(r)} writes this question for an enquiry: “{q}” Rewrite it as an effective, debatable question about {i["name"]} and explain why your version is better.'
    ans = f'For example: “{i["q"]}” This is focused on one issue, open to different answers and perspectives, and has a clear global dimension; the original {low(WEAK[k])[3:]}.'
    key = '1 mark focused, open question; 1 mark debatable/allows perspectives; 1 mark explains the improvement' + ('; 1 mark identifies the original weakness' if m == 4 else '') + f' [{m}]'
    return Q(stem, ans, key, m, 'explain')


@c1c.add('C4', (3, 4, 5), 'case')
def c1c_choose(r, D):
    i = issue(r)
    ks = r.sample(list(WEAK), 2)
    qs = [i['q'], weak_q(r, i, ks[0]), weak_q(r, i, ks[1])]
    order = r.sample(range(3), 3)
    lab = 'XYZ'
    best = lab[order.index(0)]
    intro = f'Three students suggest questions about {i["name"]}: ' + ' '.join(f'Question {lab[j]}: “{qs[order[j]]}”' for j in range(3))
    parts = [
        lambda r: ('Identify the question that is most suitable for a Global Perspectives essay.', f'Question {best}.', '1 mark [1]'),
        lambda r: (f'Explain the weakness of the other two questions.', f'One is weak because {low(WEAK[ks[0]])}; the other because {low(WEAK[ks[1]])}.', '2 marks for each weakness explained [4]'),
        lambda r: (f'Explain two features that make Question {best} effective.', 'It is open and debatable, so different perspectives can be compared; it is focused on one issue with a global dimension, so it can be researched in depth.',
                   '1 mark each feature, 1 mark each explained [4]'),
        lambda r: (f'Suggest two different perspectives that could be compared when answering Question {best}.', f'{cap(i["persp"][0][0])}, which {i["persp"][0][1]}; {i["persp"][1][0]}, which {i["persp"][1][1]}.',
                   '1 mark each perspective [2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


CHAPTERS[1] = [c1a, c1b, c1c]


# ============================================================== CHAPTER 2: Causes, consequences, courses of action

CLASSES = ['A cause of the issue', 'A consequence of the issue', 'A proposed course of action', 'A perspective on the issue']


def statement(r, i, kind):
    if kind == 0:
        return r.choice(i['causes'])[0]
    if kind == 1:
        return r.choice(i['cons'])[0]
    if kind == 2:
        a = r.choice(i['actions'])
        return f'The {a[1]} should {a[0]}'
    h = r.choice(i['persp'])
    return f'{cap(h[0])} {h[1]} because {h[2]}'


c2a = T('Identifying causes of a global issue', 'identifying causes', 'causes')
add_terms(c2a, [
    ('cause', 'a factor that makes an issue happen or makes it worse'),
    ('underlying cause', 'a long-term condition that makes an issue likely to develop'),
    ('trigger', 'a short-term event that sets off an issue whose underlying causes already exist'),
    ('correlation', 'a relationship in which two things change together, which does not by itself prove that one causes the other'),
    ('contributory factor', 'one of several causes that together produce an issue'),
])


@c2a.add('C1', (1, 2, 3), 'mcq')
def c2a_classify(r, D):
    i = issue(r)
    k = r.randrange(4)
    s = statement(r, i, k)
    lead = r.choice([f'A student researching {i["name"]} makes this note:', f'In a report on {i["name"]} you read:', f'One of {person(r)}’s research notes on {i["name"]} says:'])
    return MC(r, f'{lead} “{s}.” How should this statement be classified?', CLASSES[k], [c for c in CLASSES if c != CLASSES[k]],
              f'{CLASSES[k]}: causes explain why the issue happens, consequences are its effects, courses of action are proposed responses, perspectives are views held by a person or group.')


@c2a.add('C1', (1, 2, 3), 'mcq')
def c2a_which_cause(r, D):
    i = issue(r)
    c = r.choice(i['causes'])[0]
    a = r.choice(i['actions'])
    ds = [r.choice(i['cons'])[0], f'The {a[1]} should {a[0]}', f'{cap(i["persp"][0][0])} {i["persp"][0][1]}']
    return MC(r, f'Which of the following is a cause of {i["name"]}?', c, ds, f'{c} explains why the issue occurs; the others are a consequence, a course of action and a perspective.')


@c2a.add('C2', (1, 2, 3, 4), 'explain')
def c2a_two(r, D):
    i = issue(r)
    (a, ta), (b, tb) = r.sample(i['causes'], 2)
    stem = r.choice([f'Identify two causes of {i["name"]} and state what type of factor each one is.',
                     f'Give two different causes of {i["name"]}. For each, say whether it is a political, economic, social, technological or environmental factor.'])
    return Q(stem, f'{a} ({ta}); {b} ({tb}).', '1 mark each cause; 1 mark each correct type [4]', 4, 'explain')


@c2a.add('C2', (2, 3, 4), 'explain')
def c2a_multi(r, D):
    i = issue(r)
    cs = r.sample(i['causes'], 2)
    stem = r.choice([f'Explain why it is difficult to identify a single cause of {i["name"]}.',
                     f'{person(r)} claims that {low(cs[0][0])} is “the cause” of {i["name"]}. Explain why this claim is too simple.'])
    ans = (f'The issue has several interacting causes, for example {low(cs[0][0])} and {low(cs[1][0])}; they operate at different levels (local, national, global) '
           'and reinforce each other, and a correlation between one factor and the issue does not prove it is the main cause.')
    return Q(stem, ans, '1 mark several causes identified; 1 mark explains interaction / different levels; 1 mark correlation ≠ causation or need for evidence [3]', 3, 'explain')


@c2a.add('C3', (2, 3, 4, 5), 'case')
def c2a_source(r, D):
    i = issue(r)
    cs = r.sample(i['causes'], len(i['causes']))
    shown, extra = cs[:3], cs[3]
    src = f'{cap(i["name"])} has many roots. {shown[0][0]}. In addition, {low(shown[1][0])}. Some experts also point out that {low(shown[2][0])}. As a result, {low(i["cons"][0][0])}.'
    intro = r.choice([f'Read the source, an extract from a report by a research centre in {city(r)}. “{src}”',
                      f'{person(r)} finds this paragraph in an online article: “{src}”'])
    parts = [
        lambda r: ('Identify two causes of the issue given in the source.', f'Any two of: {shown[0][0]}; {low(shown[1][0])}; {low(shown[2][0])}.', '1 mark each [2]'),
        lambda r: (f'Identify one consequence mentioned in the source.', i['cons'][0][0] + '.', '1 mark [1]'),
        lambda r: (f'State whether “{low(shown[0][0])}” is mainly a political, economic, social, technological or environmental cause.', cap(shown[0][1]) + '.', '1 mark [1]'),
        lambda r: ('Suggest one further cause of the issue that is not mentioned in the source.', extra[0] + '.', '1 mark relevant cause; 1 mark brief explanation [2]'),
        lambda r: ('Explain which cause in the source a government could most easily address.', f'The {i["actions"][0][1]} could act on causes it controls, e.g. by deciding to {i["actions"][0][0]}; causes linked to attitudes or global markets are harder to change.',
                   '1 mark choice; 1 mark explains why within government control; 1 mark comparison with a harder cause [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c2a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2a_survey(r, D):
    i = issue(r)
    cs = r.sample(i['causes'], 3)
    n = r.choice([200, 250, 400, 500, 800])
    shares = r.sample([38, 31, 24, 19, 16, 12], 3)
    counts = [round(n * s / 100) for s in shares]
    other = n - sum(counts)
    if other <= 0:
        return None
    c = r.choice(COUNTRIES)
    tab = '; '.join(f'“{cs[j][0]}”: {counts[j]}' for j in range(3)) + f'; other reasons: {other}'
    top = max(range(3), key=lambda j: counts[j])
    p = 100 * counts[top] / n
    stem = (f'A survey asked {n} people in {c} to choose the main cause of {i["name"]}. Results: {tab}. '
            f'Calculate the percentage of respondents who chose the most popular cause.')
    m = 2
    key = f'Most popular = {counts[top]}; {counts[top]}/{n} × 100 = {pct(p)}. 1 mark method, 1 mark answer'
    ans = f'{pct(p)} chose “{cs[top][0]}”.'
    if D >= 3:
        stem += ' Explain why this result does not prove that this is the main cause of the issue.'
        ans += ' The survey measures opinion, not causation; respondents may lack expertise, and the sample may not be representative.'
        key += '; 1 mark opinion ≠ evidence of cause; 1 mark sample/representativeness or expertise point'
        m = 4
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c2a.add('C4', (2, 3, 4, 5), 'long')
def c2a_essay(r, D):
    i = issue(r)
    c, ty = r.choice(i['causes'])
    others = [x for x, _ in i['causes'] if x != c]
    return essay_q(r, D, f'{low(c)} is the most important cause of {i["name"]}',
                   [f'This {ty} factor directly shapes the issue.', f'It links to the consequence: {low(i["cons"][0][0])}.'],
                   [f'Other causes also matter: {low(others[0])}; {low(others[1])}.', 'Causes interact, so ranking them depends on the country and the evidence available.'],
                   'A supported judgement weighs the evidence for each cause and recognises that they interact.',
                   ['underlying and immediate causes', 'local, national and global factors', 'the quality of evidence'])


c2b = T('Identifying consequences and their scale and severity', 'consequences scale severity')
add_terms(c2b, [
    ('consequence', 'an effect or result of an issue or of a course of action'),
    ('scale', 'how widely a consequence is felt: the number of people or the size of the area affected'),
    ('severity', 'how serious a consequence is for those affected, for example how harmful, lasting or irreversible it is'),
    ('unintended consequence', 'an outcome of an action that was not planned or expected by those who took it'),
    ('stakeholder', 'a person, group or organisation affected by, or able to influence, an issue'),
    ('long-term consequence', 'an effect that develops or lasts over many years'),
])
add_ar(c2b, [
    ('A consequence can be large in scale but low in severity.', 'Scale measures how many are affected, while severity measures how seriously they are affected.', 'AR', 'Both true; R explains A.'),
    ('Unintended consequences only follow bad policies.', 'Even well-designed policies can change behaviour in unexpected ways.', 'R', 'A is false; R is true.'),
    ('Some consequences of an issue can be positive.', 'Every global issue harms all stakeholders equally.', 'A', 'A true (e.g. remittances from migrants); R false.'),
])


@c2b.add('C1', (1, 2, 3), 'mcq')
def c2b_which(r, D):
    i = issue(r)
    c = r.choice(i['cons'])[0]
    a = r.choice(i['actions'])
    ds = [r.choice(i['causes'])[0], f'The {a[1]} should {a[0]}', f'{cap(i["persp"][1][0])} {i["persp"][1][1]}']
    stem = r.choice([f'Which of the following is a consequence of {i["name"]}?', f'Which statement describes an effect of {i["name"]}?'])
    return MC(r, stem, c, ds, f'{c} is an effect of the issue; the others are a cause, a course of action and a perspective.')


@c2b.add('C1', (1, 2, 3), 'mcq')
def c2b_scale(r, D):
    i = issue(r)
    c, sc, term = r.choice(i['cons'])
    ans = f'{cap(sc)}, {"short-term" if term == "short" else "long-term"}'
    ds = [f'{cap(s)}, {t}' for s in ('local', 'national', 'global') for t in ('short-term', 'long-term') if f'{cap(s)}, {t}' != ans]
    return MC(r, f'In a study of {i["name"]}, how is this consequence best described? “{c}.”', ans, ds, f'{c}: mainly {sc} in scale and {"short" if term == "short" else "long"}-term.')


@c2b.add('C2', (1, 2, 3, 4), 'explain')
def c2b_scale_sev(r, D):
    i = issue(r)
    (c1, s1, _), (c2, s2, _) = r.sample(i['cons'], 2)
    stem = f'Using two consequences of {i["name"]}, explain the difference between the scale and the severity of a consequence.'
    ans = (f'Scale is how widely an effect is felt; severity is how serious it is for those affected. “{c1}” is {s1} in scale; '
           f'“{c2}” is {s2} in scale, but either could be more severe depending on how harmful and lasting it is for the people affected.')
    return Q(stem, ans, '1 mark scale defined; 1 mark severity defined; 1 mark each consequence used correctly [4]', 4, 'explain')


@c2b.add('C2', (2, 3, 4), 'explain')
def c2b_unintended(r, D):
    i = issue(r)
    a = r.choice(i['actions'])
    return Q(f'Suppose the {a[1]} decides to {a[0]}. Explain one limitation or possible unintended consequence of this action.',
             f'For example: {a[3]}. Such effects are not the aim of the action but could reduce its benefit or create new problems.',
             '1 mark plausible unintended outcome; 1 mark explains why it is unintended/its effect [2]', 2, 'explain')


@c2b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2b_table(r, D):
    i = issue(r)
    cs = r.sample(COUNTRIES, 3)
    pops = [r.choice([2, 4, 5, 8, 12, 20, 25, 40, 60]) for _ in cs]
    aff = [round(p * r.choice([3, 5, 6, 8, 10, 12, 15, 20]) * 10) for p in pops]   # thousands affected
    rate = [a / (p * 1000) * 100 for a, p in zip(aff, pops)]
    if len({round(x, 1) for x in rate}) < 3 or len(set(aff)) < 3:
        return None
    big = max(range(3), key=lambda j: aff[j])
    sev = max(range(3), key=lambda j: rate[j])
    tab = table(['Country', 'Population (millions)', 'People affected (thousands)'], [[cs[j], pops[j], f'{aff[j]:,}'] for j in range(3)])
    stem = f'The table shows how many people are affected by {i["name"]} in three countries. {tab} '
    calc = '; '.join(f'{cs[j]}: {aff[j]:,} ÷ {pops[j] * 1000:,} × 100 = {pct(rate[j])}' for j in range(3))
    if D <= 2:
        j = r.randrange(3)
        stem += f'Calculate the percentage of the population of {cs[j]} that is affected.'
        return Q(stem, pct(rate[j]), f'{aff[j]:,} thousand ÷ {pops[j]:,} million = {aff[j]:,} ÷ {pops[j] * 1000:,}; × 100 = {pct(rate[j])}. 1 mark method, 1 mark answer [2]', 2, 'numerical')
    stem += 'Calculate the percentage of each population affected. Identify the country where the issue is largest in scale and the country where it is most severe in proportion to population.'
    m = 4
    ans = f'{calc}. Largest scale: {cs[big]} ({aff[big]:,} thousand). Highest proportion: {cs[sev]} ({pct(rate[sev])}).'
    key = '1 mark method; 1 mark all three percentages; 1 mark largest absolute number; 1 mark highest proportion'
    if D >= 4:
        stem += ' Suggest one other factor that should be considered when judging severity.'
        ans += ' Other factors: how long the effect lasts, whether it is reversible, and how vulnerable the people affected are.'
        key += '; 1 mark valid factor (duration, reversibility, vulnerability)'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c2b.add('C3', (2, 3, 4, 5), 'case')
def c2b_case(r, D):
    i = issue(r)
    cs = i['cons']
    parts = [
        lambda r: ('Identify one short-term and one long-term consequence of the issue.',
                   f'Short-term: {next((c for c, s, t in cs if t == "short"), cs[0][0])}. Long-term: {next((c for c, s, t in cs if t == "long"), cs[1][0])}.', '1 mark each [2]'),
        lambda r: ('Identify one stakeholder affected by the issue and describe how they are affected.', f'{cap(i["persp"][0][0])}: {i["persp"][0][2]}.', '1 mark stakeholder; 1 mark effect [2]'),
        lambda r: ('Explain which consequence is likely to be the most severe.', f'For example, “{cs[1][0]}”, because it is long-lasting and difficult to reverse; others may affect more people but less seriously.',
                   '1 mark choice; 1 mark severity criterion (duration/irreversibility/vulnerability); 1 mark comparison [3]'),
        lambda r: ('Suggest one positive consequence that some stakeholders might experience.', f'Some groups may benefit, e.g. {low(i["persp"][2][0])} if {i["persp"][2][2]}; or new jobs or pressure for reform.',
                   '1 mark plausible positive consequence; 1 mark who benefits [2]'),
    ]
    return compose(r, news_intro(r, i), parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c2b.add('C4', (2, 3, 4, 5), 'long')
def c2b_essay(r, D):
    i = issue(r)
    c, sc, term = r.choice([x for x in i['cons'] if x[1] != 'global'] or i['cons'])
    return essay_q(r, D, f'the {sc} consequences of {i["name"]} are more serious than its global consequences',
                   [f'{c}: this is felt directly by people’s lives.', 'Local and national effects are immediate and visible.'],
                   [f'Global consequences such as {low(next((x[0] for x in i["cons"] if x[1] == "global"), i["global"]))} affect many more people.', 'Global effects can be long-term and harder to reverse.'],
                   'Seriousness depends on the criteria used (scale, severity, duration, reversibility); a supported judgement weighs these.')


c2c = T('Proposing and justifying courses of action to address an issue', 'courses of action', 'proposing justifying')
add_terms(c2c, [
    ('course of action', 'a proposed response to an issue, saying who should do what'),
    ('feasibility', 'how practical a course of action is, given cost, time, resources and political support'),
    ('effectiveness', 'how far a course of action would actually reduce the issue'),
    ('acceptability', 'how far stakeholders are willing to support a course of action'),
    ('cost-benefit analysis', 'comparing the expected costs of an action with its expected benefits'),
])


@c2c.add('C1', (1, 2, 3), 'mcq')
def c2c_limit(r, D):
    i = issue(r)
    a = r.choice(i['actions'])
    others = [x for x in i['actions'] if x is not a]
    stem = r.choice([f'A proposal to address {i["name"]} is to {a[0]}. Which statement is a limitation of this course of action?',
                     f'Which is the strongest criticism of the proposal that the {a[1]} should {a[0]}?'])
    return MC(r, stem, cap(a[3]), [cap(a[2])] + [cap(x[2]) for x in others], f'Limitation: {a[3]}. The other options are advantages.')


add_mcqs(c2c, 'C1', (1, 2, 3), [
    ('Which criterion asks whether stakeholders will support a course of action?', 'Acceptability', ['Feasibility', 'Severity', 'Scale'], 'Acceptability = stakeholder support.'),
    ('Which criterion asks whether a course of action can be carried out with the money, time and power available?', 'Feasibility', ['Acceptability', 'Legitimacy', 'Severity'], 'Feasibility = practicality.'),
])


@c2c.add('C2', (1, 2, 3, 4), 'explain')
def c2c_adv(r, D):
    i = issue(r)
    a = r.choice(i['actions'])
    stem = r.choice([f'Explain one advantage and one limitation of the proposal that the {a[1]} should {a[0]}.',
                     f'{person(r)} suggests that, to address {i["name"]}, the {a[1]} should {a[0]}. Explain one strength and one weakness of this course of action.'])
    return Q(stem, f'Advantage: {a[2]}. Limitation: {a[3]}.', '1 mark advantage, 1 mark developed; 1 mark limitation, 1 mark developed [4]', 4, 'explain')


@c2c.add('C2', (2, 3, 4), 'explain')
def c2c_who(r, D):
    i = issue(r)
    a = r.choice(i['actions'])
    return Q(f'Explain why the {a[1]} is an appropriate actor to {a[0]}.',
             f'The {a[1]} has the authority, resources or reach to carry it out; {a[2]}.', '1 mark identifies power/authority; 1 mark links to the action [2]', 2, 'explain')


CRITS = ['effectiveness', 'cost', 'acceptability', 'speed of impact']


@c2c.add('C3', (2, 3, 4, 5), 'numerical')
def c2c_matrix(r, D):
    i = issue(r)
    acts = i['actions']
    w = r.choice([[3, 2, 2, 1], [2, 1, 2, 1], [3, 1, 1, 2], [2, 2, 1, 1], [4, 2, 1, 1]])
    sc = [[r.randint(1, 5) for _ in CRITS] for _ in acts]
    tot = [sum(a * b for a, b in zip(s, w)) for s in sc]
    if len(set(tot)) < 3:
        return None
    best = max(range(3), key=lambda j: tot[j])
    lab = 'PQR'
    tab = table(['Action'] + [f'{c} (weight {x})' for c, x in zip(CRITS, w)], [[f'{lab[j]}: {acts[j][0]}'] + sc[j] for j in range(3)])
    stem = (f'A team scored three courses of action to address {i["name"]} from 1 (poor) to 5 (excellent) on each criterion '
            f'(for cost, 5 = cheapest). {tab} Calculate the weighted total for each action and identify which the team should recommend.')
    calc = '; '.join(f'{lab[j]}: ' + ' + '.join(f'{s}×{x}' for s, x in zip(sc[j], w)) + f' = {tot[j]}' for j in range(3))
    ans = f'{calc}. Recommend {lab[best]} ({acts[best][0]}).'
    key = '1 mark method (score × weight, summed); 1 mark all totals correct; 1 mark correct recommendation'
    m = 3
    if D >= 4:
        w2 = [1] * 4
        tot2 = [sum(s) for s in sc]
        b2 = max(range(3), key=lambda j: tot2[j])
        same = tot2.count(tot2[b2]) == 1 and b2 == best
        stem += ' Then calculate the unweighted totals and explain what the comparison shows about the decision.'
        ans += (f' Unweighted: ' + ', '.join(f'{lab[j]} {tot2[j]}' for j in range(3)) + '. ' +
                ('The same action comes first, so the recommendation is robust to the weights.' if same else 'The ranking changes, so the decision depends on the weights, which are value judgements that must be justified.'))
        key += '; 1 mark unweighted totals; 1 mark explains whether the decision depends on the weights'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c2c.add('C3', (2, 3, 4, 5), 'case')
def c2c_case(r, D):
    i = issue(r)
    a, b = r.sample(i['actions'], 2)
    parts = [
        lambda r: ('Identify who would carry out each course of action.', f'Action 1: the {a[1]}. Action 2: the {b[1]}.', '1 mark each [2]'),
        lambda r: ('Explain one advantage of Action 1.', cap(a[2]) + '.', '1 mark advantage; 1 mark developed [2]'),
        lambda r: ('Explain one limitation of Action 2.', cap(b[3]) + '.', '1 mark limitation; 1 mark developed [2]'),
        lambda r: ('Suggest one criterion, other than cost, that should be used to compare the two actions, and explain why it matters.', 'Effectiveness/acceptability/feasibility/speed: e.g. acceptability matters because an action that stakeholders oppose may be blocked or ignored.',
                   '1 mark criterion; 1 mark explanation [2]'),
        lambda r: ('Recommend one of the two actions, justifying your choice.', f'Either, if justified: e.g. Action 1 because {a[2]}, although {a[3]}; this outweighs Action 2 because {b[3]}.',
                   '1 mark choice; 1 mark reason; 1 mark acknowledges a drawback/compares [3]'),
    ]
    intro = f'Two courses of action are proposed to address {i["name"]}. Action 1: the {a[1]} should {a[0]}. Action 2: the {b[1]} should {b[0]}.'
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c2c.add('C4', (2, 3, 4, 5), 'long')
def c2c_essay(r, D):
    i = issue(r)
    a = r.choice(i['actions'])
    others = [x for x in i['actions'] if x is not a]
    return essay_q(r, D, f'the best way to address {i["name"]} is for the {a[1]} to {a[0]}',
                   [cap(a[2]) + '.', f'It acts on a cause of the issue: {low(i["causes"][0][0])}.'],
                   [cap(a[3]) + '.', f'An alternative is to {others[0][0]}: {others[0][2]}.'],
                   'A supported judgement compares actions on effectiveness, feasibility and acceptability, and may recommend a combination.',
                   ['effectiveness', 'feasibility', 'acceptability to stakeholders', 'unintended consequences'])


CHAPTERS[2] = [c2a, c2b, c2c]


# ============================================================== CHAPTER 3: Perspectives

THINKERS = [
    ('Thomas Hobbes', 'Leviathan (1651)', 'without a strong sovereign, life in the state of nature would be “solitary, poor, nasty, brutish, and short”'),
    ('John Locke', 'Two Treatises of Government (1689)', 'people have natural rights to life, liberty and property, and government rests on the consent of the governed'),
    ('Jean-Jacques Rousseau', 'The Social Contract (1762)', 'legitimate government expresses the “general will” of the people'),
    ('Montesquieu', 'The Spirit of the Laws (1748)', 'liberty is best protected by separating legislative, executive and judicial powers'),
    ('Edmund Burke', 'Reflections on the Revolution in France (1790)', 'society should change gradually, respecting tradition and inherited institutions'),
    ('Mary Wollstonecraft', 'A Vindication of the Rights of Woman (1792)', 'women are rational beings who deserve the same education and rights as men'),
    ('John Stuart Mill', 'On Liberty (1859)', 'the only justification for restricting a person’s freedom is to prevent harm to others (the harm principle)'),
    ('Karl Marx', 'The Communist Manifesto (1848, with Engels)', 'history is driven by class struggle, and capitalism exploits the working class'),
    ('John Rawls', 'A Theory of Justice (1971)', 'just principles are those people would choose behind a “veil of ignorance” about their own position in society'),
    ('Robert Nozick', 'Anarchy, State, and Utopia (1974)', 'only a minimal state that protects rights and enforces contracts can be justified'),
    ('Niccolò Machiavelli', 'The Prince (1532)', 'a ruler must sometimes act ruthlessly to keep power and maintain the state'),
    ('Hans Morgenthau', 'Politics Among Nations (1948)', 'states act in pursuit of power and the national interest (political realism)'),
]
IDEOLOGIES = {
    'liberal': ('individual freedom, rights and limited, accountable government', 'protects or restricts individual rights and freedoms'),
    'conservative': ('tradition, order, stability and gradual change', 'preserves stability and established institutions or risks sudden disruption'),
    'socialist': ('equality, collective welfare and fair distribution of resources', 'reduces inequality and protects workers and the poor'),
    'environmentalist': ('sustainability and protection of the natural world for future generations', 'reduces harm to ecosystems and future generations'),
    'feminist': ('equality between women and men and challenging patriarchal structures', 'advances or ignores gender equality'),
    'nationalist': ('the interests, identity and sovereignty of the nation', 'serves the national interest and protects sovereignty'),
}
INFLUENCES = ['culture and religion', 'nationality', 'age and generation', 'economic interests', 'personal experience', 'political ideology', 'education', 'occupation']


c3a = T('What is a perspective? Viewpoints, worldviews and the influences on them', 'perspective viewpoints worldviews influences')
add_terms(c3a, [
    ('perspective', 'a coherent world view that responds to an issue and is made up of argument, evidence and assumptions, shaped by a particular standpoint'),
    ('viewpoint', 'a single opinion or position taken on an issue'),
    ('worldview', 'a broad set of beliefs and values through which a person interprets the world'),
    ('ideology', 'a connected set of political ideas about how society should be organised'),
    ('bias', 'a tendency to favour one view or group, which may distort judgement'),
    ('values', 'principles or standards that a person regards as important, such as freedom or equality'),
])


@c3a.add('C1', (1, 2, 3), 'mcq')
def c3a_thinker(r, D):
    n, w, idea = r.choice(THINKERS)
    others = [x for x in THINKERS if x[0] != n]
    if r.random() < 0.5:
        return MC(r, f'Which political thinker argued that {idea}?', n, [x[0] for x in r.sample(others, 6)], f'{n}, {w}.')
    if r.random() < 0.5:
        return MC(r, f'Which work was written by {n}?', w, [x[1] for x in r.sample(others, 6)], f'{n} wrote {w}.')
    return MC(r, f'Which idea is most closely associated with {n}?', cap(idea), [cap(x[2]) for x in r.sample(others, 6)], f'{n} ({w}): {idea}.')


@c3a.add('C1', (1, 2, 3), 'mcq')
def c3a_ideo(r, D):
    k = r.choice(list(IDEOLOGIES))
    return MC(r, r.choice([f'Which set of values is most central to a {k} perspective?', f'A {k} perspective on a political issue is most likely to emphasise']),
              cap(IDEOLOGIES[k][0]), [cap(v[0]) for kk, v in IDEOLOGIES.items() if kk != k], f'{cap(k)}: {IDEOLOGIES[k][0]}.')


@c3a.add('C2', (1, 2, 3), 'mcq')
def c3a_why(r, D):
    i = issue(r)
    h = r.choice(i['persp'])
    others = [p[2] for j in ISSUES if j is not i for p in j['persp']]
    return MC(r, f'On the issue of {i["name"]}, {h[0]} {h[1]}. Which is the most likely reason for this perspective?', cap(h[2]), [cap(x) for x in r.sample(others, 3)],
              f'{cap(h[0])}: {h[2]}.')


@c3a.add('C2', (1, 2, 3, 4), 'explain')
def c3a_infl(r, D):
    i = issue(r)
    h = r.choice(i['persp'])
    stem = r.choice([f'On {i["name"]}, {h[0]} {h[1]}. Explain what is likely to influence this perspective.',
                     f'Explain why {h[0]} might take a different perspective on {i["name"]} from other stakeholders.'])
    return Q(stem, f'Its perspective is shaped by its position and interests: {h[2]}. Other stakeholders, e.g. {i["persp"][(i["persp"].index(h) + 1) % 3][0]}, have different interests or values, so they reach a different view.',
             '1 mark identifies the influence (interest, values, experience, role); 1 mark explains link to the view; 1 mark contrast with another stakeholder [3]', 3, 'explain')


@c3a.add('C2', (2, 3, 4), 'explain')
def c3a_ideo_resp(r, D):
    i = issue(r)
    a = r.choice(i['actions'])
    k = r.choice(list(IDEOLOGIES))
    v, test = IDEOLOGIES[k]
    return Q(f'The {a[1]} proposes to {a[0]}. Explain how someone with a {k} perspective might judge this proposal.',
             f'A {k} perspective values {v}, so they would judge the proposal by whether it {test}. Depending on that, they could support it or oppose it; e.g. the limitation “{a[3]}” may matter more or less to them.',
             '1 mark identifies core values of the perspective; 1 mark applies them to the proposal; 1 mark reaches a reasoned likely response [3]', 3, 'explain')


@c3a.add('C2', (1, 2, 3, 4), 'explain')
def c3a_inf_gen(r, D):
    inf = r.choice(INFLUENCES)
    i = issue(r)
    return Q(f'Explain how {inf} could influence a person’s perspective on {i["name"]}.',
             f'{cap(inf)} shapes what a person values and what they know or stand to gain or lose, so it affects which arguments and evidence on {i["name"]} they find convincing; e.g. {i["persp"][0][0]} {i["persp"][0][1]} because {i["persp"][0][2]}.',
             '1 mark explains how the influence shapes values/interests; 1 mark applies to the issue [2]', 2, 'explain')


add_claims(c3a, [
    ('A perspective is the same as an opinion.', False, 'An opinion is a single view; a perspective is a wider standpoint made up of arguments, evidence, assumptions and values.'),
    ('People from the same country always share the same perspective on global issues.', False, 'Perspectives within a country differ because of age, ideology, interests and experience.'),
    ('Recognising your own perspective helps you to avoid bias in research.', True, 'Being aware of your own assumptions makes it easier to consider other perspectives fairly.'),
    ('Political realists believe states mainly pursue their national interest.', True, 'Realists such as Hans Morgenthau see international politics as a struggle for power between self-interested states.'),
    ('John Locke argued for an all-powerful ruler to avoid chaos.', False, 'This was Thomas Hobbes; Locke argued that government rests on consent and must protect natural rights.'),
], D=(1, 2, 3, 4))


@c3a.add('C3', (2, 3, 4, 5), 'case')
def c3a_case(r, D):
    i = issue(r)
    h1, h2 = r.sample(i['persp'], 2)
    intro = f'On the issue of {i["name"]}, {h1[0]} {h1[1]}, while {h2[0]} {h2[1]}.'
    k = r.choice(list(IDEOLOGIES))
    parts = [
        lambda r: ('Identify the two perspectives described.', f'{cap(h1[0])}: {h1[1]}. {cap(h2[0])}: {h2[1]}.', '1 mark each [2]'),
        lambda r: (f'Explain one reason why {h1[0]} holds its perspective.', cap(h1[2]) + '.', '1 mark reason; 1 mark developed [2]'),
        lambda r: (f'Explain one factor that might influence the perspective of {h2[0]}.', cap(h2[2]) + '; it may also be shaped by its values, role or interests.', '1 mark factor; 1 mark linked to view [2]'),
        lambda r: (f'Suggest how a {k} perspective might differ from both.', f'A {k} perspective values {IDEOLOGIES[k][0]}, so it would ask whether the response {IDEOLOGIES[k][1]}.', '1 mark values; 1 mark applied [2]'),
        lambda r: ('Explain why it is important to consider more than one perspective on this issue.', 'Each stakeholder sees only part of the issue and may have a vested interest; comparing perspectives reveals assumptions and leads to a more balanced, credible judgement.',
                   '1 mark balance/avoid bias; 1 mark reveals assumptions or interests; 1 mark better-supported judgement [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c3a.add('C4', (2, 3, 4, 5), 'long')
def c3a_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'people’s perspectives on {i["name"]} are shaped more by self-interest than by values',
                   [f'{cap(i["persp"][0][0])} {i["persp"][0][1]} because {i["persp"][0][2]}.', 'Organisations with vested interests often adopt views that protect them.'],
                   [f'Some actors are driven by principle, e.g. {i["persp"][1][0]}: {i["persp"][1][2]}.', 'Ideologies such as liberalism or socialism shape views even when they cost the holder.'],
                   'Interests and values usually combine; a supported judgement uses examples of each and considers how far they can be separated.')


c3b = T('Identifying perspectives in sources: who holds them and why', 'identifying perspectives in sources', 'who holds them')
add_terms(c3b, [
    ('stakeholder', 'a person or group with an interest in an issue, who may be affected by it or able to influence it'),
    ('vested interest', 'a personal stake in an outcome, often financial, that may influence a person’s view'),
    ('purpose of a source', 'the reason a source was produced, for example to inform, persuade or sell'),
    ('provenance', 'the origin of a source: who produced it, when, where and for whom'),
    ('target audience', 'the group of people a source is intended to reach'),
])


def persp_source(r, i, h):
    c = city(r)
    return r.choice([
        f'A spokesperson for {h[0]} told a press conference in {c} that the organisation {h[1]}, explaining that {h[2]}.',
        f'In a statement published on its website, {h[0]} says it {h[1]}. The statement adds that {h[2]}.',
        f'An article written for {h[0]} argues that it {h[1]} on the question of {i["name"]}, noting that {h[2]}.',
        f'Speaking at a conference in {c} on {i["name"]}, a representative of {h[0]} said that it {h[1]}.',
    ])


@c3b.add('C1', (1, 2, 3), 'mcq')
def c3b_who(r, D):
    i = issue(r)
    h = r.choice(i['persp'])
    others = [p[0] for p in i['persp'] if p is not h] + [p[0] for j in ISSUES if j is not i for p in j['persp']][:0]
    extra = [p[0] for j in r.sample([j for j in ISSUES if j is not i], 2) for p in j['persp'][:1]]
    return MC(r, f'On {i["name"]}, which stakeholder is most likely to hold this view: it {h[1]}?', cap(h[0]), [cap(x) for x in others + extra],
              f'{cap(h[0])} {h[1]} because {h[2]}.')


PSCALE = {
    'personal': lambda i, c: f'“As a student in {c}, I have seen how {i["local"]} affects my friends and family.”',
    'national': lambda i, c: f'“Our government must put our own citizens first when deciding how to respond to {i["name"]}.”',
    'global': lambda i, c: f'“{cap(i["name"])} affects people everywhere, and only coordinated international action will work.”',
}


@c3b.add('C1', (1, 2, 3), 'mcq')
def c3b_scale(r, D):
    i = issue(r)
    k = r.choice(list(PSCALE))
    s = PSCALE[k](i, city(r))
    return MC(r, f'What kind of perspective does this statement express? {s}', f'A {k} perspective', [f'A {x} perspective' for x in PSCALE if x != k] + ['A neutral, factual perspective'],
              f'{cap(k)} perspective: the statement focuses on {"one person’s own experience" if k == "personal" else "the interests of one nation" if k == "national" else "the world as a whole"}.')


@c3b.add('C2', (1, 2, 3, 4), 'explain')
def c3b_vested(r, D):
    i = issue(r)
    h = r.choice(i['persp'])
    src = persp_source(r, i, h)
    return Q(f'{src} Explain why it is important to know who produced this statement when judging its perspective.',
             f'The perspective reflects the producer’s position: {h[2]}. Knowing this reveals possible vested interest or bias, so the reader can judge how far the view is balanced and look for other perspectives.',
             '1 mark identifies who/position; 1 mark explains interest or purpose; 1 mark effect on how we judge the view [3]', 3, 'explain')


@c3b.add('C3', (2, 3, 4, 5), 'case')
def c3b_source(r, D):
    i = issue(r)
    h = r.choice(i['persp'])
    o = [p for p in i['persp'] if p is not h][0]
    src = persp_source(r, i, h)
    parts = [
        lambda r: ('Identify the perspective expressed in the source.', f'{cap(h[0])} {h[1]}.', '1 mark [1]'),
        lambda r: ('Identify who holds this perspective.', cap(h[0]) + '.', '1 mark [1]'),
        lambda r: ('Explain why the producer of the source might hold this perspective.', cap(h[2]) + '.', '1 mark reason; 1 mark link to position/interests [2]'),
        lambda r: ('Suggest the purpose of the source.', 'To persuade the audience (public, government or members) to support its view and influence policy.', '1 mark purpose; 1 mark linked to audience [2]'),
        lambda r: ('Identify a stakeholder likely to hold a different perspective, and explain why.', f'{cap(o[0])}, which {o[1]}, because {o[2]}.', '1 mark stakeholder; 1 mark explanation [2]'),
        lambda r: ('Explain one reason why the source may not give a complete picture of the issue.', f'It presents one stakeholder’s view; {h[2]}, so it may leave out evidence or perspectives, such as those of {o[0]}.',
                   '1 mark one-sided/vested interest; 1 mark what may be missing [2]'),
    ]
    return compose(r, f'Read the source. “{src}”', parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c3b.add('C4', (3, 4, 5), 'case')
def c3b_two(r, D):
    i = issue(r)
    h1, h2 = r.sample(i['persp'], 2)
    intro = f'Source A: {persp_source(r, i, h1)} Source B: {persp_source(r, i, h2)}'
    parts = [
        lambda r: ('Identify the perspective in each source.', f'A: {h1[0]} {h1[1]}. B: {h2[0]} {h2[1]}.', '1 mark each [2]'),
        lambda r: ('Explain why the two producers hold different perspectives.', f'A: {h1[2]}. B: {h2[2]}. Their roles, interests and values differ.', '1 mark each reason; 1 mark comparison [3]'),
        lambda r: ('Explain which source is more likely to be influenced by a vested interest.', 'The one whose producer gains or loses directly (money, power, reputation) from the outcome; judgement must be explained using provenance.',
                   '1 mark choice; 1 mark identifies interest; 1 mark explains effect on reliability [3]'),
        lambda r: ('Suggest what further information you would need to decide which perspective is better supported.', 'Independent evidence (data, peer-reviewed research), the date and full context of each statement, and corroboration from neutral sources.',
                   '1 mark per relevant suggestion with reason, max 2 [2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


c3c = T('Comparing perspectives on the same global issue', 'comparing perspectives on the same global issue')
add_terms(c3c, [
    ('national perspective', 'a view of an issue shaped mainly by the interests, culture or policies of one country'),
    ('global perspective', 'a view that considers how an issue affects people across the world and the shared interests involved'),
    ('consensus', 'general agreement among different groups'),
    ('common ground', 'points on which different perspectives agree'),
    ('synthesis', 'combining insights from different perspectives into a new, more complete understanding'),
])


@c3c.add('C2', (1, 2, 3, 4), 'explain')
def c3c_simdiff(r, D):
    i = issue(r)
    h1, h2 = r.sample(i['persp'], 2)
    return Q(f'On {i["name"]}, {h1[0]} {h1[1]}, while {h2[0]} {h2[1]}. Identify one difference and one possible similarity between these perspectives.',
             f'Difference: they reach opposite or different conclusions, because {h1[2]} whereas {h2[2]}. Possible similarity: both accept that {i["name"]} is a real issue that needs a response.',
             '1 mark difference; 1 mark explained; 1 mark plausible similarity [3]', 3, 'explain')


@c3c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3c_poll(r, D):
    i = issue(r)
    a = r.choice(i['actions'])
    groups = r.choice([['18–24', '25–44', '45–64', '65+'], ['Urban', 'Rural', 'Small towns', 'Suburbs'], ['Students', 'Employed', 'Unemployed', 'Retired']])
    vals = r.sample(range(28, 79), 4)
    c = r.choice(COUNTRIES)
    tab = table(['Group'] + groups, [['% supporting'] + [f'{v}%' for v in vals]])
    hi = max(range(4), key=lambda j: vals[j]); lo = min(range(4), key=lambda j: vals[j])
    diff = vals[hi] - vals[lo]
    stem = f'An opinion poll in {c} asked whether the {a[1]} should {a[0]}. {tab} '
    if D <= 2:
        stem += 'Calculate the difference in support between the most and least supportive groups.'
        return Q(stem, f'{diff} percentage points ({groups[hi]} {vals[hi]}% − {groups[lo]} {vals[lo]}%).', f'{vals[hi]} − {vals[lo]} = {diff} percentage points; 1 mark identifies groups, 1 mark answer [2]', 2, 'numerical')
    stem += 'Calculate the difference in support between the most and least supportive groups, and suggest why their perspectives might differ.'
    ans = f'{diff} percentage points ({groups[hi]} {vals[hi]}% vs {groups[lo]} {vals[lo]}%). The groups may be affected differently by the proposal or hold different values and interests.'
    key = '1 mark groups identified; 1 mark difference in percentage points; 1 mark plausible reason linked to interests/experience'
    m = 3
    if D >= 4:
        stem += ' Explain one limitation of using this poll to compare perspectives.'
        ans += ' Limitation: we do not know the sample size or how respondents were chosen, and a yes/no poll does not show the reasons behind a perspective.'
        key += '; 1 mark limitation (sample, wording, no reasons)'
        m = 4
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c3c.add('C3', (2, 3, 4, 5), 'case')
def c3c_case(r, D):
    i = issue(r)
    h1, h2 = r.sample(i['persp'], 2)
    intro = f'Perspective 1: {cap(h1[0])} {h1[1]}. Perspective 2: {cap(h2[0])} {h2[1]}. Both concern {i["name"]}.'
    parts = [
        lambda r: ('Identify the main difference between the two perspectives.', f'1: {h1[1]}; 2: {h2[1]}.', '1 mark [1]'),
        lambda r: ('Explain why each group holds its perspective.', f'1: {h1[2]}. 2: {h2[2]}.', '1 mark each [2]'),
        lambda r: ('Suggest one point of common ground between them.', f'Both recognise that {i["name"]} matters and could accept a measure such as: {i["actions"][-1][0]}.', '1 mark plausible common ground; 1 mark explained [2]'),
        lambda r: ('Explain what kind of evidence would help you decide which perspective is more convincing.', 'Independent data on the consequences and on the effects of proposed actions, e.g. comparative studies across countries, rather than statements by the groups themselves.',
                   '1 mark type of evidence; 1 mark why it helps (independent, relevant) [2]'),
        lambda r: ('Is one perspective more likely to be a national perspective and the other a global one? Explain.', 'It depends on whether each focuses on one country’s interests or on effects worldwide; answers must refer to the wording and holder of each perspective.',
                   '1 mark judgement; 1 mark supported from the perspectives [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c3c.add('C2', (1, 2, 3), 'mcq')
def c3c_mcq(r, D):
    i = issue(r)
    h1, h2 = r.sample(i['persp'], 2)
    ans = 'They reach different views because they have different interests, roles or values'
    return MC(r, f'On {i["name"]}, {h1[0]} {h1[1]}, while {h2[0]} {h2[1]}. Which statement best explains the difference?', ans,
              ['One of them must be using false evidence', 'They disagree only because they live in different countries', 'Perspectives on global issues are random and cannot be explained'],
              'Different stakeholders have different interests, roles and values.')


@c3c.add('C4', (2, 3, 4, 5), 'long')
def c3c_essay(r, D):
    i = issue(r)
    h1, h2 = r.sample(i['persp'], 2)
    return essay_q(r, D, f'on {i["name"]}, the perspective of {h1[0]} is more convincing than the perspective of {h2[0]}',
                   [f'{cap(h1[0])} {h1[1]}: {h1[2]}.', 'Its view may be supported by evidence about the consequences of the issue.'],
                   [f'{cap(h2[0])} {h2[1]}: {h2[2]}.', 'Each perspective may be influenced by vested interest; independent evidence is needed.'],
                   'A supported judgement compares the reasoning, evidence and possible bias of each perspective rather than simply agreeing with one.',
                   ['the reasoning used', 'the quality of evidence', 'vested interests', 'national and global perspectives'])


CHAPTERS[3] = [c3a, c3b, c3c]


# ============================================================== CHAPTER 4: Argument analysis

ROLE = ['Main conclusion', 'Intermediate conclusion', 'Reason', 'Evidence', 'Counter-assertion', 'Response to a counter-assertion']


def arg_parts(i):
    a = i['arg']
    return [('Evidence', cap(a['ev']) + '.'), ('Reason', cap(a['r1']) + '.'), ('Reason', 'Moreover, ' + a['r2'] + '.'),
            ('Intermediate conclusion', 'So ' + a['ic'] + '.'), ('Counter-assertion', 'Some people claim that ' + a['counter'] + '.'),
            ('Response to a counter-assertion', 'However, ' + a['rebut'] + '.'), ('Main conclusion', 'Therefore, ' + a['conc'] + '.')]


def arg_text(r, i, D, numbered=False):
    ps = arg_parts(i)
    if D >= 3 and r.random() < 0.5:
        # conclusion first, then support
        a = i['arg']
        ps = [('Main conclusion', cap(a['conc']) + '.'), ('Reason', cap(a['r1']) + '.'), ('Evidence', 'For example: ' + cap(a['ev']) + '.'),
              ('Reason', 'Furthermore, ' + a['r2'] + '.'), ('Intermediate conclusion', 'This shows that ' + a['ic'] + '.'),
              ('Counter-assertion', 'It is sometimes argued that ' + a['counter'] + '.'), ('Response to a counter-assertion', 'But ' + a['rebut'] + '.')]
    if numbered:
        return ' '.join(f'({k + 1}) {s}' for k, (_, s) in enumerate(ps)), ps
    return ' '.join(s for _, s in ps), ps


def arg_intro(r, i, txt):
    return r.choice([f'Read the argument about {i["name"]}. “{txt}”', f'{person(r)} wrote this argument for a school debate: “{txt}”',
                     f'This argument appeared in an opinion column in {city(r)}: “{txt}”'])


c4a = T('Components of an argument: claims, reasons, evidence and conclusions', 'components of an argument claims reasons evidence conclusions')
add_terms(c4a, [
    ('argument', 'a set of reasons and evidence given to persuade the reader to accept a conclusion'),
    ('claim', 'a statement that something is the case, which may or may not be supported'),
    ('reason', 'a statement given to support a conclusion'),
    ('evidence', 'facts, data, examples or expert testimony used to support a reason'),
    ('main conclusion', 'the claim the whole argument is trying to persuade the reader to accept'),
    ('intermediate conclusion', 'a conclusion drawn from some reasons that then acts as a reason for the main conclusion'),
    ('counter-assertion', 'a claim that opposes the argument, which the author usually then responds to'),
], D1=(1, 2), D2=(1, 2, 3))


@c4a.add('C1', (1, 2, 3), 'mcq')
def c4a_conc(r, D):
    i = issue(r)
    txt, ps = arg_text(r, i, D)
    a = i['arg']
    return MC(r, f'{arg_intro(r, i, txt)} Which of the following is the main conclusion of the argument?', cap(a['conc']),
              [cap(a['ic']), cap(a['r1']), cap(a['counter'])], f'Main conclusion: {a["conc"]} (signalled by “therefore” or stated first and supported by everything else).')


@c4a.add('C2', (1, 2, 3), 'mcq')
def c4a_role(r, D):
    i = issue(r)
    ps = arg_parts(i)
    role, s = r.choice([p for p in ps if p[0] != 'Main conclusion'])
    txt = ' '.join(x for _, x in ps)
    return MC(r, f'{arg_intro(r, i, txt)} What is the function of “{s}” in this argument?', role, [x for x in ROLE if x != role],
              f'“{s}” is the {low(role)}.')


@c4a.add('C2', (1, 2, 3, 4), 'explain')
def c4a_ev_vs_reason(r, D):
    i = issue(r)
    a = i['arg']
    return Q(f'In an argument that {a["conc"]}, the author writes: “{cap(a["r1"])}” and “{cap(a["ev"])}”. Explain the difference between the role of these two statements.',
             f'The first is a reason: a general claim that supports the conclusion. The second is evidence: a specific fact or example used to support a reason and make it more convincing.',
             '1 mark reason identified and explained; 1 mark evidence identified and explained [2]', 2, 'explain')


@c4a.add('C3', (2, 3, 4, 5), 'case')
def c4a_case(r, D):
    i = issue(r)
    txt, ps = arg_text(r, i, D, numbered=True)
    a = i['arg']
    num = {role: k + 1 for k, (role, _) in reversed(list(enumerate(ps)))}
    parts = [
        lambda r: ('Identify the main conclusion.', cap(a['conc']) + f' (sentence {num["Main conclusion"]}).', '1 mark [1]'),
        lambda r: ('Identify the intermediate conclusion.', cap(a['ic']) + f' (sentence {num["Intermediate conclusion"]}).', '1 mark [1]'),
        lambda r: ('Identify the evidence used.', cap(a['ev']) + f' (sentence {num["Evidence"]}).', '1 mark [1]'),
        lambda r: ('Identify the counter-assertion and explain how the author responds to it.', f'Counter-assertion: {a["counter"]}. Response: {a["rebut"]}.', '1 mark counter; 1 mark response [2]'),
        lambda r: ('Identify two reasons given to support the intermediate conclusion.', f'{cap(a["r1"])}; {a["r2"]}.', '1 mark each [2]'),
        lambda r: ('Explain how the evidence supports the argument.', f'It gives a real example/data ({a["ev"]}) that makes the reason more credible and links to the conclusion that {a["conc"]}.',
                   '1 mark identifies what evidence shows; 1 mark links it to reason/conclusion [2]'),
    ]
    return compose(r, arg_intro(r, i, txt), parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c4a.add('C4', (3, 4, 5), 'case')
def c4a_case4(r, D):
    i = issue(r)
    txt, ps = arg_text(r, i, D, numbered=True)
    a = i['arg']
    parts = [
        lambda r: ('Identify the main conclusion and the intermediate conclusion.', f'MC: {a["conc"]}. IC: {a["ic"]}.', '1 mark each [2]'),
        lambda r: ('Describe the structure of the argument.', 'Two reasons (with evidence) support the intermediate conclusion, which supports the main conclusion; a counter-assertion is raised and answered.', '1 mark reasons → IC; 1 mark IC → MC; 1 mark counter/response [3]'),
        lambda r: ('Evaluate how well the evidence supports the main conclusion.', f'It is relevant and specific ({a["ev"]}), but it is one example/country and may not apply elsewhere; it supports the reason more than the full conclusion.',
                   '1 mark strength; 1 mark weakness (generalisation/sufficiency); 1 mark judgement [3]'),
        lambda r: ('Suggest a further piece of evidence that would strengthen the argument.', 'Comparative data from several countries, or a peer-reviewed study showing the effect claimed.', '1 mark relevant evidence; 1 mark why it strengthens [2]'),
    ]
    return compose(r, arg_intro(r, i, txt), parts, k=(3, 4), type_='case')


INDICATORS = {'conclusion': ['therefore', 'so', 'consequently', 'thus', 'it follows that', 'hence'],
              'reason': ['because', 'since', 'as', 'for the reason that', 'given that'],
              'counter-assertion': ['some people argue that', 'it is sometimes claimed that', 'opponents say that', 'admittedly'],
              'evidence/example': ['for example', 'for instance', 'research shows', 'according to']}


@c4a.add('C1', (1, 2, 3), 'mcq')
def c4a_ind(r, D):
    k = r.choice(list(INDICATORS))
    w = r.choice(INDICATORS[k])
    ds = [r.choice(v) for kk, v in INDICATORS.items() if kk != k]
    return MC(r, r.choice([f'Which word or phrase most often signals a {k}?', f'An author wants to introduce a {k}. Which expression would usually be used?']), w, ds, f'“{w}” typically signals a {k}.')


@c4a.add('C4', (2, 3, 4, 5), 'long')
def c4a_essay(r, D):
    i = issue(r)
    a = i['arg']
    return essay_q(r, D, f'{a["conc"]}', [cap(a['r1']) + '.', cap(a['ev']) + '.', cap(a['r2']) + '.'], [cap(a['counter']) + '.', f'The argument assumes that {a["assume"]}.'],
                   f'Judgement weighs the reasons and evidence against the counter-argument (response offered: {a["rebut"]}).', ['reasons and evidence', 'assumptions', 'counter-arguments'])


c4b = T('Identifying assumptions and implicit reasoning', 'assumptions implicit reasoning')
add_terms(c4b, [
    ('assumption', 'an unstated reason that the argument depends on: if it is false, the conclusion does not follow'),
    ('implicit reasoning', 'reasoning that is suggested but not stated directly in an argument'),
    ('explicit', 'stated directly in the text'),
    ('negation test', 'checking a possible assumption by asking whether the argument collapses if the statement is false'),
])

MINI = [  # (reason with {c}/{c2}, conclusion, assumption, distractor stated or irrelevant)
    ('{c} has more police officers per person than {c2}', '{c} is safer than {c2}', 'more police officers per person lead to lower crime', 'police officers in {c} are paid more than in {c2}'),
    ('turnout in {c} rose after online voting was introduced', 'online voting increased turnout in {c}', 'nothing else that could explain the rise changed at the same time', 'online voting is cheaper than postal voting'),
    ('the President of {c} won 55% of the vote', 'the President’s policies are supported by most citizens of {c}', 'people who voted for the President support all of the President’s policies', '55% is more than half'),
    ('{c} spends twice as much on its army as {c2}', '{c} would win any war against {c2}', 'military spending determines military success', '{c} has a larger population than {c2}'),
    ('the new anti-corruption agency in {c} has charged 40 officials this year', 'corruption in {c} is falling', 'the number of officials charged reflects how much corruption is taking place', 'the agency was set up by parliament'),
    ('many protesters in {c} are students', 'the protests in {c} do not represent the views of ordinary citizens', 'students are not ordinary citizens whose views count', 'the protests began in the capital city'),
    ('{c} has a written constitution', 'citizens’ rights are well protected in {c}', 'a written constitution is enforced in practice', 'the constitution of {c} was written in the twentieth century'),
    ('the government of {c} has published all its contracts online', 'there is no corruption in public contracts in {c}', 'publication alone prevents corrupt deals from taking place', 'publishing contracts is popular with voters'),
    ('women hold 50% of seats in the parliament of {c}', 'women in {c} have achieved equality', 'representation in parliament means equality in all areas of life', 'the parliament of {c} has 200 members'),
    ('{c} has signed the Paris Agreement', '{c} will cut its emissions', 'signing an agreement means a country will carry out its commitments', 'the Paris Agreement was signed in 2015'),
    ('most newspapers in {c} support the government', 'the government of {c} is doing a good job', 'newspaper support reflects the quality of government rather than ownership or pressure', 'newspaper sales in {c} are falling'),
    ('{c} holds elections every four years', '{c} is a democracy', 'regular elections are free and fair', 'elections in {c} are held on a Sunday'),
    ('{c} introduced compulsory voting and turnout reached 92%', 'compulsory voting makes voters better informed', 'people who are required to vote will learn more about politics', 'turnout is the percentage of registered voters who vote'),
    ('a survey found 70% of people in {c} trust the army', 'the army should run the government of {c}', 'an institution that is trusted should also govern', 'the survey was carried out by telephone'),
]


def mini(r):
    m = r.choice(MINI)
    c, c2 = r.sample(COUNTRIES, 2)
    f = lambda s: s.replace('{c}', c).replace('{c2}', c2)
    return [f(x) for x in m]


@c4b.add('C1', (1, 2, 3), 'mcq')
def c4b_mini(r, D):
    reason, conc, ass, dis = mini(r)
    other = mini(r)
    if other[2] == ass:
        return None
    return MC(r, f'“{cap(reason)}, so {conc}.” Which of the following is an assumption on which this argument depends?', cap(ass),
              [cap(reason), cap(dis), cap(other[2])], f'Unstated but necessary: {ass}. Negation test: if this is false, the conclusion does not follow.')


@c4b.add('C2', (1, 2, 3), 'mcq')
def c4b_arg(r, D):
    i = issue(r)
    txt, _ = arg_text(r, i, D)
    a = i['arg']
    o = issue(r, avoid=[i['key']])
    return MC(r, f'{arg_intro(r, i, txt)} Which of the following is an assumption the argument relies on?', cap(a['assume']),
              [cap(a['r1']), cap(a['ic']), cap(o['arg']['assume'])], f'Assumption: {a["assume"]}. The reason and IC are stated, so they are not assumptions; the fourth option is irrelevant.')


@c4b.add('C2', (1, 2, 3, 4), 'explain')
def c4b_explain(r, D):
    reason, conc, ass, _ = mini(r)
    stem = r.choice([f'“{cap(reason)}, so {conc}.” Identify one assumption in this argument and explain why the argument depends on it.',
                     f'{person(r)} argues: “{cap(reason)}. Therefore {conc}.” Explain one unstated assumption that the argument makes.'])
    return Q(stem, f'Assumption: {ass}. If this is not true, the reason no longer supports the conclusion, so the argument fails.',
             '1 mark assumption identified; 1 mark explains dependence (negation test) [2]', 2, 'explain')


@c4b.add('C3', (2, 3, 4, 5), 'explain')
def c4b_weak(r, D):
    reason, conc, ass, _ = mini(r)
    m = 3 if D <= 3 else 4
    stem = f'Read this argument: “{cap(reason)}. It follows that {conc}.” Identify the assumption, explain why it may be false, and explain the effect on the argument.'
    ans = f'Assumption: {ass}. It may be false because other factors could explain the reason given, or the link is not automatic. If it is false, the conclusion that {conc} is not supported.'
    key = '1 mark assumption; 1 mark why it may be false (with example/alternative); 1 mark effect on conclusion' + ('; 1 mark suggests evidence that would test it' if m == 4 else '') + f' [{m}]'
    return Q(stem, ans, key, m, 'explain')


@c4b.add('C3', (2, 3, 4, 5), 'case')
def c4b_case(r, D):
    i = issue(r)
    txt, _ = arg_text(r, i, D)
    a = i['arg']
    parts = [
        lambda r: ('Identify one assumption in the argument.', cap(a['assume']) + '.', '1 mark [1]'),
        lambda r: ('Explain why the argument depends on this assumption.', f'If it were false, the reasons would not lead to the conclusion that {a["conc"]}.', '1 mark negation; 1 mark link to conclusion [2]'),
        lambda r: ('Explain how the counter-assertion challenges an assumption of the argument.', f'The counter-assertion ({a["counter"]}) suggests that the benefits claimed may come at a cost, questioning whether {a["assume"]} is enough to justify the conclusion.',
                   '1 mark link counter to assumption; 1 mark effect on argument [2]'),
        lambda r: ('Suggest what evidence would show whether the assumption is reasonable.', 'Comparative or before-and-after data from several countries that tests the link assumed.', '1 mark relevant evidence; 1 mark explains what it would show [2]'),
    ]
    return compose(r, arg_intro(r, i, txt), parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c4b.add('C4', (2, 3, 4, 5), 'long')
def c4b_essay(r, D):
    i = issue(r)
    a = i['arg']
    return essay_q(r, D, f'the argument that {a["conc"]} depends on a questionable assumption',
                   [f'It assumes that {a["assume"]}.', 'If that assumption fails, the reasons do not lead to the conclusion.'],
                   [f'Evidence such as “{a["ev"]}” gives some support to the assumption.', 'Most arguments on complex issues rely on reasonable assumptions.'],
                   'A supported judgement tests the assumption against evidence and decides how far the argument survives.')


c4c = T('Structure of reasoning: chains of reasoning, counter-arguments and rebuttals', 'structure of reasoning chains counter-arguments rebuttals')
add_terms(c4c, [
    ('chain of reasoning', 'a sequence in which one reason leads to an intermediate conclusion, which leads on to further conclusions'),
    ('counter-argument', 'an argument for a different or opposite conclusion'),
    ('rebuttal', 'a response that shows why a counter-argument is weak or does not defeat the main argument'),
    ('joint reasons', 'reasons that support a conclusion only when taken together'),
    ('independent reasons', 'reasons that each support the conclusion on their own'),
])


@c4c.add('C2', (1, 2, 3, 4), 'short')
def c4c_order(r, D):
    i = issue(r)
    a = i['arg']
    items = [('reason', cap(a['r1'])), ('IC', cap(a['ic'])), ('MC', cap(a['conc']))]
    if D >= 3:
        items.insert(1, ('reason 2', cap(a['r2'])))
    lab = 'PQRS'[:len(items)]
    order = r.sample(range(len(items)), len(items))
    shown = ' '.join(f'{lab[j]}: {items[order[j]][1]}.' for j in range(len(items)))
    seq = sorted(range(len(items)), key=lambda j: order[j])
    ans = ' → '.join(lab[j] for j in seq)
    m = 2 if D < 3 else 3
    return Q(f'Arrange these statements into a chain of reasoning, ending with the main conclusion. {shown}', ans,
             f'Order: {ans} (reason(s) → intermediate conclusion → main conclusion). 2 marks fully correct; 1 mark if the conclusion is correctly last' + (', 1 mark reasons before IC' if m == 3 else '') + f' [{m}]', m, 'short')


@c4c.add('C1', (1, 2, 3), 'mcq')
def c4c_rebut(r, D):
    i = issue(r)
    a = i['arg']
    o = issue(r, avoid=[i['key']])
    stem = f'An author argues that {a["conc"]}. The author then writes: “Some people claim that {a["counter"]}.” Which sentence would be the best rebuttal?'
    return MC(r, stem, cap(a['rebut']) + '.', [cap(a['counter']) + ' in every case.', cap(o['arg']['rebut']) + '.', f'This is an issue that people disagree about.'],
              f'Rebuttal: {a["rebut"]}; it responds directly to the counter-assertion.')


@c4c.add('C2', (2, 3, 4), 'explain')
def c4c_why_counter(r, D):
    i = issue(r)
    a = i['arg']
    return Q(f'An argument concludes that {a["conc"]}. Explain why including the counter-assertion “{a["counter"]}” and the response “{a["rebut"]}” can make the argument stronger.',
             'It shows the author has considered other perspectives; answering the strongest objection removes a reason to reject the conclusion and makes the argument more balanced and persuasive.',
             '1 mark shows other perspectives considered; 1 mark response removes/weakens objection; 1 mark increases credibility/persuasiveness [3]', 3, 'explain')


@c4c.add('C2', (1, 2, 3), 'mcq')
def c4c_joint(r, D):
    c = r.choice(COUNTRIES)
    pairs = [
        ('joint', f'Party X won more seats than any other party in {c}. Party X has the support of a majority in parliament. So Party X can form a government alone.',
         'The reasons support the conclusion only together'),
        ('independent', f'Compulsory voting raises turnout. Separately, it makes parties campaign among all groups. Either reason alone supports introducing it in {c}.',
         'Each reason supports the conclusion on its own'),
    ]
    kind, txt, ans = r.choice(pairs)
    return MC(r, f'Read: “{txt}” How do the reasons support the conclusion?', ans,
              ['The reasons support the conclusion only together' if kind == 'independent' else 'Each reason supports the conclusion on its own',
               'The reasons contradict the conclusion', 'There are no reasons, only a conclusion'], f'{kind.capitalize()} reasons.')


@c4c.add('C3', (2, 3, 4, 5), 'case')
def c4c_case(r, D):
    i = issue(r)
    txt, _ = arg_text(r, i, D)
    a = i['arg']
    o = i['persp'][1]
    parts = [
        lambda r: ('Describe the chain of reasoning that leads to the intermediate conclusion.', f'{cap(a["r1"])}, and {a["r2"]}; together these lead to the IC that {a["ic"]}.', '1 mark reasons; 1 mark link to IC [2]'),
        lambda r: ('Identify the counter-assertion and the response to it.', f'Counter: {a["counter"]}. Response: {a["rebut"]}.', '1 mark each [2]'),
        lambda r: ('Evaluate how effective the response to the counter-assertion is.', f'It partly answers the objection ({a["rebut"]}) but may not fully remove it; evidence is needed to show the response works in practice.',
                   '1 mark strength; 1 mark limitation; 1 mark judgement [3]'),
        lambda r: (f'Write a counter-argument that {o[0]} might make.', f'{cap(o[0])} {o[1]}, arguing that {o[2]}, so the conclusion should be rejected or limited.', '1 mark relevant counter-claim; 1 mark supporting reason [2]'),
    ]
    return compose(r, arg_intro(r, i, txt), parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c4c.add('C4', (2, 3, 4, 5), 'long')
def c4c_essay(r, D):
    i = issue(r)
    a = i['arg']
    return essay_q(r, D, f'the counter-argument that {a["counter"]} defeats the case that {a["conc"]}',
                   [cap(a['counter']) + '.', 'If the objection is strong, the reasons may not be enough.'],
                   [cap(a['rebut']) + '.', f'The chain of reasoning ({a["r1"]}; {a["ic"]}) still stands.'],
                   'A supported judgement decides whether the rebuttal answers the counter-argument and what evidence would settle it.')


CHAPTERS[4] = [c4a, c4b, c4c]


# ============================================================== CHAPTER 5: Evidence and sources

SRC_HIGH = [
    ('a peer-reviewed article in an academic political science journal', 'other experts checked its methods before publication', 'it may be several years old or focus on a narrow case'),
    ('a report by an intergovernmental organisation such as the UN Development Programme', 'it draws on data from many countries and has a reputation to protect', 'it may avoid openly criticising member governments'),
    ('a report by an independent election-monitoring mission', 'its observers were present at polling stations and are trained to assess elections', 'observers can visit only a sample of polling stations'),
    ('a study by a university research centre with no funding from interested parties', 'its authors have expertise and no obvious vested interest', 'it may use a small or local sample'),
]
SRC_MID = [
    ('a speech by a government minister', 'the minister has access to official information', 'the minister may present the government’s record favourably'),
    ('a campaign report produced by an NGO', 'the NGO has field experience of the issue', 'its purpose is partly to persuade and raise funds, so it may select evidence'),
    ('an article in an established international newspaper', 'it has editorial checks and a reputation for accuracy', 'it may reflect the paper’s editorial line'),
    ('a briefing paper from a think tank funded by an industry association', 'its researchers may have expertise', 'its funding may create a vested interest'),
]
SRC_LOW = [
    ('an anonymous post on a social media platform', 'it may give an immediate eyewitness view', 'the author cannot be identified, so expertise and reputation cannot be checked'),
    ('a press release from a company that would profit from the policy', 'the company knows its own products', 'it has a clear vested interest'),
    ('a personal blog by a student with no stated sources', 'it may reflect a genuine personal experience', 'it has no expertise or sources to check'),
    ('a leaflet produced by a political party during an election campaign', 'it states the party’s position clearly', 'its purpose is to win votes, so it is likely to be one-sided'),
]
RAVEN = {
    'Reputation': ['{s} has won international awards for accurate reporting on {n}.', '{s} was fined last year for publishing false claims about {n}.'],
    'Ability to see': ['{p} was present in {c} when the events linked to {n} took place.', '{p} is commenting on events in {c} that were only reported to them second-hand.'],
    'Vested interest': ['The author of the report on {n} would gain financially if its recommendation were adopted.', '{p} is paid by an organisation that campaigns on one side of the debate about {n}.'],
    'Expertise': ['{p} is a professor who has researched {n} for twenty years.', '{p} has no training or experience in the subject of {n}.'],
    'Neutrality': ['{p} has no connection to either side of the debate on {n}.', '{p} is a member of the party that proposed the policy on {n}.'],
}


def raven_stmt(r):
    k = r.choice(list(RAVEN))
    i = issue(r)
    s = r.choice(RAVEN[k]).replace('{s}', r.choice(['The newspaper', 'The broadcaster', 'The website'])).replace('{p}', person(r)).replace('{c}', city(r)).replace('{n}', i['name'])
    return k, s, i


c5a = T('Credibility of sources: expertise, reputation, vested interest and bias', 'credibility of sources expertise reputation vested interest bias')
add_terms(c5a, [
    ('credibility', 'how far a source or claim can be believed, judged by criteria such as expertise, reputation and vested interest'),
    ('expertise', 'specialist knowledge or training relevant to the claim being made'),
    ('reputation', 'the standing a source has gained from its past record of accuracy or inaccuracy'),
    ('vested interest', 'something a source stands to gain or lose that may lead it to present information in a particular way'),
    ('corroboration', 'support for a claim from another, independent source'),
    ('ability to see', 'whether a source was in a position to observe or know about the events it describes'),
    ('neutrality', 'having no reason to favour one side of an issue'),
], D1=(1, 2), D2=(1, 2, 3))


@c5a.add('C1', (1, 2, 3), 'mcq')
def c5a_raven(r, D):
    k, s, i = raven_stmt(r)
    return MC(r, f'Which credibility criterion does this information mainly relate to? “{s}”', k, [x for x in RAVEN if x != k],
              f'{k}: the statement concerns {low(k)}.')


@c5a.add('C1', (1, 2, 3), 'mcq')
def c5a_best(r, D):
    i = issue(r)
    h = r.choice(SRC_HIGH)
    ls = r.sample(SRC_LOW, 3)
    return MC(r, f'A student is researching {i["name"]}. Which source is likely to be the most credible?', cap(h[0]), [cap(x[0]) for x in ls],
              f'{cap(h[0])}: {h[1]}. The others lack expertise or have a clear vested interest or bias.')


@c5a.add('C2', (1, 2, 3, 4), 'explain')
def c5a_explain(r, D):
    i = issue(r)
    s = r.choice(SRC_HIGH + SRC_MID + SRC_LOW)
    stem = r.choice([f'A student finds {s[0]} about {i["name"]}. Explain one strength and one weakness of this source’s credibility.',
                     f'Assess the credibility of {s[0]} as a source of information on {i["name"]}.'])
    return Q(stem, f'Strength: {s[1]}. Weakness: {s[2]}.', '1 mark strength, 1 mark explained using a credibility criterion; 1 mark weakness, 1 mark explained [4]', 4, 'explain')


@c5a.add('C2', (1, 2, 3, 4), 'explain')
def c5a_vested(r, D):
    i = issue(r)
    h = r.choice(i['persp'])
    return Q(f'{persp_source(r, i, h)} Explain how a vested interest might affect the credibility of this source.',
             f'The source {h[1]}; {h[2]}, so it may select evidence that supports its position and leave out evidence against it. Its claims need corroboration from a neutral source.',
             '1 mark identifies the interest; 1 mark explains likely effect on claims; 1 mark need for corroboration [3]', 3, 'explain')


add_ar(c5a, [
    ('A source with a vested interest is always wrong.', 'Vested interest gives a reason to present information selectively.', 'R', 'A false: such a source may still be accurate; it needs corroboration. R true.'),
    ('An eyewitness account can be credible on what happened at a protest.', 'The eyewitness had the ability to see the events.', 'AR', 'Both true; ability to see explains credibility.'),
    ('Corroboration increases the credibility of a claim.', 'Independent sources agreeing make it less likely the claim is invented or mistaken.', 'AR', 'Both true; R explains A.'),
])


@c5a.add('C3', (2, 3, 4, 5), 'case')
def c5a_case(r, D):
    i = issue(r)
    s = r.choice(SRC_MID + SRC_LOW + SRC_HIGH)
    claim = r.choice(i['cons'])[0]
    yr = r.choice([2019, 2021, 2022, 2023, 2024, 2025])
    intro = f'A student researching {i["name"]} finds {s[0]}, published in {yr}. It states: “{claim}.”'
    parts = [
        lambda r: ('Identify one feature of the source that increases its credibility.', cap(s[1]) + '.', '1 mark feature; 1 mark linked to criterion [2]'),
        lambda r: ('Identify one feature of the source that reduces its credibility.', cap(s[2]) + '.', '1 mark feature; 1 mark linked to criterion [2]'),
        lambda r: ('Suggest how the student could check the claim.', 'Look for corroboration in an independent source, e.g. official statistics or a peer-reviewed study, and check the date and original data.', '1 mark corroboration; 1 mark specific type of source [2]'),
        lambda r: ('Explain how the date of publication affects the usefulness of the source.', f'Published in {yr}: recent enough to be relevant only if the situation has not changed since; the student should check for newer data.', '1 mark currency; 1 mark applied [2]'),
        lambda r: ('Make a judgement about how far the claim can be trusted.', 'Judgement weighing the strength and weakness above and the need for corroboration.', '1 mark judgement; 1 mark supported by two criteria [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c5a.add('C4', (3, 4, 5), 'case')
def c5a_compare(r, D):
    i = issue(r)
    a = r.choice(SRC_HIGH)
    b = r.choice(SRC_MID + SRC_LOW)
    intro = f'On {i["name"]}, Source A is {a[0]}; Source B is {b[0]}. The two sources reach different conclusions.'
    parts = [
        lambda r: ('Explain one strength of Source A’s credibility.', cap(a[1]) + '.', '1 mark strength; 1 mark criterion [2]'),
        lambda r: ('Explain one weakness of Source B’s credibility.', cap(b[2]) + '.', '1 mark weakness; 1 mark criterion [2]'),
        lambda r: ('Explain one limitation of Source A.', cap(a[2]) + '.', '1 mark limitation; 1 mark developed [2]'),
        lambda r: ('Which source is more credible? Justify your answer.', f'Usually Source A, because {a[1]}, whereas {b[2]}; but A’s limitation ({a[2]}) means its findings should still be corroborated.',
                   '1 mark judgement; 2 marks comparison using criteria; 1 mark acknowledges limitation [4]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


@c5a.add('C4', (2, 3, 4, 5), 'long')
def c5a_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'official government sources are the most credible sources of information about {i["name"]}',
                   ['Governments collect large-scale data through statistics offices.', 'Ministers have access to official information.'],
                   [f'Governments have vested interests, e.g. {i["persp"][0][0]} {i["persp"][0][1]}.', 'Independent academic studies and international bodies may be more neutral.'],
                   'Credibility depends on the type of claim and the government’s independence; corroboration across sources is the best test.')


EV_TYPES = ['Statistic', 'Expert opinion', 'Anecdote', 'Prediction', 'Value judgement', 'Verifiable fact']


def ev_stmt(r, k, i):
    p, c, co = person(r), city(r), r.choice(COUNTRIES)
    if k == 'Statistic':
        return f'A survey of {r.choice([800, 1200, 1500, 2000, 2500]):,} adults in {co} found that {r.randint(31, 79)}% think the {i["actions"][0][1]} should {i["actions"][0][0]}.'
    if k == 'Expert opinion':
        return f'Professor {p}, who has researched {i["name"]} for many years, believes that {i["arg"]["ic"]}.'
    if k == 'Anecdote':
        return f'“I talked to my neighbours about {i["name"]} and they all agreed with me, so I am sure everyone feels the same,” said {p}, who lives in {c}.'
    if k == 'Prediction':
        return f'A campaign group in {c} predicts that, if nothing is done by {r.choice([2035, 2040, 2050])}, this effect will become far more serious: “{i["cons"][1][0]}”.'
    if k == 'Value judgement':
        return f'Whatever the evidence says, the way the world has handled {i["name"]} is simply unjust.'
    return i['fact']


c5b = T('Quality of evidence: facts, statistics, expert opinion and anecdote', 'quality of evidence facts statistics expert opinion anecdote')
add_terms(c5b, [
    ('anecdote', 'a personal story or individual experience used as evidence'),
    ('statistic', 'numerical data, often collected from a survey or official records'),
    ('expert opinion', 'the judgement of a person with specialist knowledge'),
    ('value judgement', 'a statement about what is good, bad, right or wrong, which cannot be proved true or false'),
    ('verifiable fact', 'a statement that can be checked and shown to be true or false'),
    ('representative sample', 'a sample whose characteristics reflect those of the whole population'),
], D1=(1, 2), D2=(1, 2, 3))


@c5b.add('C1', (1, 2, 3), 'mcq')
def c5b_type(r, D):
    i = issue(r)
    k = r.choice(EV_TYPES)
    s = ev_stmt(r, k, i)
    return MC(r, f'What type of evidence is this? “{s}”', k, r.sample([x for x in EV_TYPES if x != k], 3), f'{k}.')


@c5b.add('C2', (1, 2, 3, 4), 'explain')
def c5b_weak(r, D):
    i = issue(r)
    k = r.choice(['Anecdote', 'Statistic', 'Expert opinion', 'Prediction'])
    s = ev_stmt(r, k, i)
    why = {'Anecdote': ('it is vivid and shows the human impact', 'it is one person’s experience and cannot be generalised'),
           'Statistic': ('it is based on a large sample, so it is more representative than one example', 'we do not know how the sample was chosen or how the question was worded'),
           'Expert opinion': ('the expert has relevant knowledge', 'it is still an opinion; experts can disagree and no data is given'),
           'Prediction': ('it warns about possible future consequences', 'it cannot be verified yet and comes from a campaign group with a purpose')}[k]
    return Q(f'Read this evidence about {i["name"]}: “{s}” Explain one strength and one weakness of this evidence.', f'{k}. Strength: {why[0]}. Weakness: {why[1]}.',
             '1 mark strength, 1 mark developed; 1 mark weakness, 1 mark developed [4]', 4, 'explain')


@c5b.add('C2', (1, 2, 3), 'mcq')
def c5b_strongest(r, D):
    i = issue(r)
    s = ev_stmt(r, 'Statistic', i)
    ds = [ev_stmt(r, k, i) for k in ('Anecdote', 'Value judgement', 'Prediction')]
    return MC(r, f'Which piece of evidence would give the strongest support to a claim about public opinion on {i["name"]}?', s, ds,
              'A large survey is more representative than an anecdote; a value judgement and a prediction are not evidence of current opinion.')


@c5b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5b_sample(r, D):
    i = issue(r)
    co = r.choice(COUNTRIES)
    pop = r.choice([4, 6, 9, 12, 15, 30])  # millions of adults
    n = r.choice([120, 150, 250, 300, 400, 600])
    yes = r.randint(int(n * 0.55), int(n * 0.8))
    p = 100 * yes / n
    how = r.choice(['an online poll on a campaign group’s website', 'interviews outside a university in the capital', 'a phone-in on a radio show'])
    stem = (f'A campaign group in {co} claims that “most citizens” support the proposal that the {i["actions"][0][1]} should {i["actions"][0][0]}. '
            f'Its evidence: {yes} of {n} people who took part in {how} agreed. {co} has about {pop} million adults. '
            'Calculate the percentage who agreed and the sample as a percentage of the adult population.')
    sp = n / (pop * 1e6) * 100
    ans = f'{yes}/{n} × 100 = {pct(p)}; sample = {n}/{pop:,} million × 100 = {sp:.4f}% of adults (about {sp:.2g}%).'
    key = '1 mark agreement %; 1 mark sample as % of population'
    m = 2
    if D >= 3:
        stem += ' Evaluate whether the evidence supports the claim.'
        ans += f' The result shows majority support among respondents, but the sample is tiny and self-selected/unrepresentative ({how}), so it does not show what “most citizens” think.'
        key += '; 1 mark sample not representative (method); 1 mark size/self-selection; 1 mark judgement'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c5b.add('C3', (2, 3, 4, 5), 'case')
def c5b_case(r, D):
    i = issue(r)
    ks = r.sample(['Statistic', 'Expert opinion', 'Anecdote', 'Value judgement', 'Prediction'], 3)
    sts = [ev_stmt(r, k, i) for k in ks]
    intro = f'A briefing on {i["name"]} uses three pieces of evidence. E1: “{sts[0]}” E2: “{sts[1]}” E3: “{sts[2]}”'
    parts = [
        lambda r: ('Identify the type of evidence in E1, E2 and E3.', f'E1 {ks[0]}; E2 {ks[1]}; E3 {ks[2]}.', '1 mark each [3]'),
        lambda r: ('Which piece of evidence is weakest? Explain your answer.', 'Usually the anecdote or value judgement: it is not representative or cannot be verified.', '1 mark choice; 1 mark reason [2]'),
        lambda r: ('Explain why a value judgement cannot be used on its own to prove a claim.', 'It expresses what someone thinks is right or wrong; it cannot be checked as true or false, so it needs reasons and evidence.', '1 mark not verifiable; 1 mark needs support [2]'),
        lambda r: ('Suggest one further piece of evidence that would strengthen the briefing.', 'A large representative survey, official statistics over time, or a peer-reviewed comparative study.', '1 mark evidence; 1 mark why it is stronger [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c5b.add('C4', (2, 3, 4, 5), 'long')
def c5b_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'statistics are always more reliable than personal testimony as evidence about {i["name"]}',
                   ['Large, representative samples can be generalised.', 'Statistics can be checked and compared over time.'],
                   ['Statistics can be biased by sampling, question wording or presentation.', 'Testimony shows experience and causes that numbers miss, e.g. eyewitnesses with ability to see.'],
                   'Reliability depends on how the evidence was produced; the strongest case uses statistics and testimony that corroborate each other.')


add_claims(c5b, [
    ('An expert opinion is a fact.', False, 'It is a judgement by someone with relevant knowledge; it may be well informed but can still be wrong or disputed.'),
    ('A larger sample is always representative.', False, 'Size helps, but a large self-selected sample can still be biased; how the sample is chosen matters.'),
    ('An anecdote can illustrate a point but cannot prove a general claim.', True, 'One case may be untypical, so it cannot be generalised to a whole population.'),
    ('A prediction cannot be verified at the time it is made.', True, 'It is about the future, so it can only be judged on the reasoning and evidence behind it.'),
], D=(1, 2, 3, 4))


c5c = T('Evaluating the use of statistics and data in arguments', 'statistics and data in arguments')
add_terms(c5c, [
    ('percentage point', 'the simple difference between two percentages, e.g. from 40% to 50% is a rise of 10 percentage points'),
    ('turnout', 'the percentage of registered voters who cast a vote in an election'),
    ('median', 'the middle value when data are arranged in order, less affected by extreme values than the mean'),
    ('per capita', 'per person, calculated by dividing a total by the population'),
    ('correlation', 'a statistical relationship between two variables, which does not prove causation'),
    ('truncated axis', 'a graph axis that does not start at zero, which can exaggerate differences'),
], D1=(1, 2), D2=(1, 2, 3))


@c5c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5c_pp(r, D):
    co = r.choice(COUNTRIES)
    a = r.randint(38, 62)
    b = a + r.choice([4, 5, 6, 8, 10, 12])
    pp = b - a
    rel = 100 * pp / a
    who = r.choice(['18–24-year-olds', 'first-time voters', 'voters in rural areas', 'women aged under 30'])
    stem = f'Turnout among {who} in {co} rose from {a}% at one election to {b}% at the next. A minister says turnout “rose by {pp}%”.'
    if D <= 2:
        opts_q = stem + ' What was the percentage increase in turnout?'
        return MC(r, opts_q, pct(rel), [f'{pp}%', pct(100 * pp / b), pct(100 * b / a)], f'Percentage change = ({b} − {a}) / {a} × 100 = {pct(rel)}; the rise was {pp} percentage points.')
    stem += ' Calculate the change in percentage points and the percentage increase, and explain whether the minister’s statement is accurate.'
    return Q(stem, f'{pp} percentage points; ({b} − {a})/{a} × 100 = {pct(rel)}. The minister confuses percentage points with per cent: the relative increase was {pct(rel)}.',
             '1 mark percentage points; 1 mark percentage change; 1 mark explains the confusion [3]', 3, 'numerical')


@c5c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5c_mandate(r, D):
    co = r.choice(COUNTRIES)
    party = r.choice(PARTIES)
    t = r.randint(48, 72)
    v = r.randint(34, 49)
    e = v * t / 100
    seats = r.randint(51, 60)
    stem = f'In an election in {co}, turnout was {t}%. The {party} won {v}% of the votes cast and {seats}% of the seats. The party leader claims “the people have given us a clear mandate”.'
    if D <= 2:
        return MC(r, stem + ' What percentage of the registered electorate voted for the party?', pct(e), [f'{v}%', pct(t * (100 - v) / 100), f'{seats}%'],
                  f'{v}% × {t}% = {pct(e)} of the electorate.')
    m = 4 if D >= 4 else 3
    stem += ' Calculate the percentage of the registered electorate that voted for the party and use your answer to evaluate the leader’s claim.'
    ans = (f'{v} × {t}/100 = {pct(e)} of the electorate. The party has a majority of seats ({seats}%) but only {v}% of votes and about {round(e)}% of all registered voters, '
           'so the claim of a “clear mandate” is weak; however, it won more votes than any other party under the rules of the system.')
    key = '1 mark method; 1 mark answer; 1 mark challenges claim using the figure' + ('; 1 mark balanced point (legal majority/rules of system)' if m == 4 else '') + f' [{m}]'
    return Q(stem, ans, key, m, 'numerical')


@c5c.add('C3', (2, 3, 4, 5), 'numerical')
def c5c_seats(r, D):
    co = r.choice(COUNTRIES)
    ps = r.sample(PARTIES, 3)
    total = r.choice([100, 120, 150, 200])
    votes = r.choice([[44, 36, 20], [41, 38, 21], [39, 33, 28], [47, 30, 23], [42, 35, 23]])
    s1 = r.randint(int(total * 0.55), int(total * 0.65))
    s3 = r.randint(1, int(total * 0.06))
    s2 = total - s1 - s3
    seats = [s1, s2, s3]
    sp = [100 * s / total for s in seats]
    diff = [sp[j] - votes[j] for j in range(3)]
    tab = table(['Party', '% of votes', f'Seats (of {total})'], [[ps[j], votes[j], seats[j]] for j in range(3)])
    stem = f'Results of a first-past-the-post election in {co}: {tab} Calculate each party’s percentage of seats and identify which party is most under-represented.'
    under = min(range(3), key=lambda j: diff[j])
    ans = '; '.join(f'{ps[j]}: {seats[j]}/{total} = {pct(sp[j])} of seats ({"+" if diff[j] >= 0 else "−"}{fmt(abs(round(diff[j], 1)), 1)} points vs votes)' for j in range(3)) + f'. Most under-represented: {ps[under]}.'
    key = '1 mark method; 1 mark all seat percentages; 1 mark correct party identified'
    m = 3
    if D >= 4:
        stem += ' Explain why first-past-the-post can produce this result, and what a supporter of the system might say in its defence.'
        ans += ' FPTP awards each constituency to the candidate with most votes, so a party with spread-out support wins few seats; supporters say it usually produces stable single-party government and a clear link between MP and constituency.'
        key += '; 1 mark explanation of FPTP effect; 1 mark defence (stability/constituency link)'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


def dhondt(votes, seats):
    won = [0] * len(votes)
    for _ in range(seats):
        q = [v / (w + 1) for v, w in zip(votes, won)]
        j = max(range(len(votes)), key=lambda k: q[k])
        won[j] += 1
    return won


@c5c.add('C3', (3, 4, 5), 'numerical')
def c5c_dhondt(r, D):
    co = r.choice(COUNTRIES)
    ps = r.sample(PARTIES, 4)
    votes = sorted(r.sample(range(8, 60), 4), reverse=True)
    votes = [v * 1000 for v in votes]
    seats = r.choice([5, 6, 7])
    # avoid ties at the last seat
    qs = sorted([v / d for v in votes for d in range(1, seats + 2)], reverse=True)
    if abs(qs[seats - 1] - qs[seats]) < 1:
        return None
    won = dhondt(votes, seats)
    tab = table(['Party', 'Votes'], [[ps[j], f'{votes[j]:,}'] for j in range(4)])
    stem = f'A region of {co} elects {seats} members using the D’Hondt method of proportional representation (divide each party’s votes by 1, 2, 3, … and give seats to the highest quotients). {tab} Calculate how many seats each party wins.'
    ans = '; '.join(f'{ps[j]} {won[j]}' for j in range(4)) + '.'
    key = f'Highest {seats} quotients: ' + ', '.join(f'{fmt(round(q))}' for q in qs[:seats]) + '. 1 mark method (dividing by 1, 2, 3…); 1 mark quotients correct; 1 mark allocation'
    m = 3
    if D >= 4:
        tv = sum(votes)
        stem += ' Compare each party’s share of seats with its share of votes.'
        ans += ' ' + '; '.join(f'{ps[j]}: {pct(100 * votes[j] / tv)} of votes, {pct(100 * won[j] / seats)} of seats' for j in range(4)) + '. D’Hondt slightly favours larger parties.'
        key += '; 1 mark vote and seat shares; 1 mark comment that larger parties gain slightly'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c5c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5c_median(r, D):
    co = r.choice(COUNTRIES)
    n = 7 if D <= 3 else 9
    xs = sorted(r.sample(range(2, 40), n - 1)) + [r.choice([250, 300, 400, 480])]
    xs.sort()
    mean = sum(xs) / n
    med = xs[n // 2]
    lst = ', '.join(str(x) for x in r.sample(xs, n))
    stem = f'Donations (in thousands of dollars) received by {n} candidates in a local election in {co} were: {lst}.'
    if D <= 2:
        return MC(r, stem + ' What is the median donation?', f'${med} thousand', [f'${fmt(round(mean, 1))} thousand', f'${xs[0]} thousand', f'${xs[n // 2 - 1]} thousand'],
                  f'Ordered: {", ".join(map(str, xs))}; median = {med}.')
    stem += ' Calculate the mean and the median. A newspaper reports that “the average candidate received over ${} thousand”. Explain why this is misleading.'.format(int(mean))
    return Q(stem, f'Mean = {sum(xs)}/{n} = {fmt(round(mean, 1))}; median = {med}. The mean is pulled up by one very large donation ({xs[-1]}); the median better represents a typical candidate.',
             f'1 mark mean; 1 mark median; 1 mark outlier identified; 1 mark explains why median is more representative [4]', 4, 'numerical')


@c5c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5c_percap(r, D):
    a, b = r.sample(COUNTRIES, 2)
    what = r.choice(['complaints of electoral fraud', 'registered NGOs', 'reported attacks on journalists', 'freedom-of-information requests'])
    pa, pb = r.choice([5, 8, 10, 12, 16]), r.choice([40, 50, 60, 80, 120])
    ka = r.randint(20, 90); kb = r.randint(ka + 20, ka + 200)
    ra, rb = ka / pa, kb / pb
    if abs(ra - rb) < 0.3:
        return None
    hi = a if ra > rb else b
    stem = f'Last year {a} (population {pa} million) recorded {ka} {what}, and {b} (population {pb} million) recorded {kb}. A report claims the problem is worse in {b}.'
    if D <= 2:
        return MC(r, stem + f' How many {what} were recorded per million people in {a}?', fmt(round(ra, 2)), [fmt(round(pa / ka, 2)), str(ka), fmt(round(ka * pa))],
                  f'{ka} ÷ {pa} = {fmt(round(ra, 2))} per million.')
    stem += ' Calculate the rate per million people in each country and evaluate the claim.'
    ans = f'{a}: {ka}/{pa} = {fmt(round(ra, 2))} per million; {b}: {kb}/{pb} = {fmt(round(rb, 2))} per million. Relative to population, the rate is higher in {hi}, ' + \
          ('so the claim is not supported.' if hi == a else 'so the claim is supported by the rates as well as the totals.') + ' Recorded numbers also depend on how willing people are to report.'
    m = 4 if D >= 4 else 3
    key = '1 mark each rate; 1 mark judgement based on rates' + ('; 1 mark recorded figures may reflect reporting, not reality' if m == 4 else '') + f' [{m}]'
    return Q(stem, ans, key, m, 'numerical')


@c5c.add('C3', (2, 3, 4, 5), 'numerical')
def c5c_axis(r, D):
    co = r.choice(COUNTRIES)
    a = r.randint(52, 60); b = a + r.choice([2, 3, 4])
    s = a - r.choice([1, 2])
    real = 100 * (b - a) / a
    app = (b - s) / (a - s)
    party1, party2 = r.sample(PARTIES, 2)
    stem = (f'A campaign leaflet in {co} shows a bar chart of approval ratings: {party1} {b}%, {party2} {a}%. The vertical axis starts at {s}%. '
            f'Calculate how many times taller the {party1} bar appears than the {party2} bar, and the actual percentage difference between the ratings. Explain how the graph could mislead.')
    return Q(stem, f'Bar heights: {b - s} vs {a - s}, so the {party1} bar looks {fmt(round(app, 2))} times taller; actual difference {b - a} points, i.e. {pct(real)} higher. The truncated axis exaggerates a small difference.',
             '1 mark apparent ratio; 1 mark actual difference; 1 mark explains truncated axis exaggerates [3]', 3, 'numerical')


add_mcqs(c5c, 'C2', (1, 2, 3), [
    ('Countries with more internet users tend to have higher election turnout. What can be concluded?', 'There is a correlation, but internet use may not cause higher turnout',
     ['Internet use causes higher turnout', 'Higher turnout causes internet use', 'There is no relationship between the two'], 'Correlation ≠ causation; e.g. income or education could affect both.'),
    ('A poll of 1,000 people reports 52% support with a margin of error of ±3 percentage points. What does this mean?', 'True support is likely to be between 49% and 55%',
     ['Exactly 52% of the population supports the policy', 'Support is certainly above 50%', 'Support is between 51% and 53%'], '52 ± 3 = 49–55%; a majority is not certain.'),
    ('Why might an average (mean) income figure give a misleading picture of a typical citizen?', 'A few very high incomes raise the mean above what most people earn',
     ['The mean is always lower than the median', 'Averages cannot be calculated for incomes', 'The mean ignores high incomes'], 'Skewed distributions: median more representative.'),
    ('A government reports that crime fell by 20% after it changed how crimes are recorded. What is the main problem with this claim?', 'The change in recording means the figures before and after are not comparable',
     ['A 20% fall is too small to matter', 'Crime figures are always invented', 'The government did not use a graph'], 'Changes in definitions/measurement break comparability.'),
])


@c5c.add('C4', (3, 4, 5), 'case')
def c5c_case4(r, D):
    co = r.choice(COUNTRIES)
    years = [2010, 2014, 2018, 2022]
    t = [r.randint(55, 70)]
    for _ in range(3):
        t.append(t[-1] + r.choice([-6, -4, -3, 2, 3]))
    yt = [r.randint(30, 45)]
    for _ in range(3):
        yt.append(yt[-1] + r.choice([-5, -3, 2, 4, 6]))
    tab = table(['Year'] + [str(y) for y in years], [['Overall turnout (%)'] + t, ['Turnout aged 18–24 (%)'] + yt])
    gap = [a - b for a, b in zip(t, yt)]
    party = r.choice(PARTIES)
    intro = f'Election data for {co}: {tab} The {party} argues: “Young people are becoming more and more disengaged from politics, so voting must be made compulsory.”'
    parts = [
        lambda r: ('Calculate the gap between overall and youth turnout in each year.', ', '.join(f'{y}: {g} points' for y, g in zip(years, gap)) + '.', '1 mark method; 1 mark all correct [2]'),
        lambda r: ('Calculate the change in youth turnout between 2010 and 2022 in percentage points.', f'{yt[3]} − {yt[0]} = {yt[3] - yt[0]:+d} points.', '1 mark [1]'),
        lambda r: ('Explain whether the data support the claim that young people are “becoming more and more disengaged”.',
                   f'Youth turnout went {", ".join(str(x) for x in yt)}%: ' + ('it fell overall, giving some support,' if yt[3] < yt[0] else 'it did not fall consistently,') + ' but turnout measures only voting, not other forms of engagement such as protest or campaigning.',
                   '1 mark uses trend accurately; 1 mark judgement; 1 mark limitation (turnout ≠ engagement) [3]'),
        lambda r: ('Explain why the data alone cannot show that compulsory voting is the right response.', 'The data describe turnout but not its causes or the effects of compulsory voting; evidence from countries that introduced it, and other options such as automatic registration, must be considered.',
                   '1 mark data show what, not why; 1 mark need evidence about the policy; 1 mark alternative actions [3]'),
        lambda r: ('Suggest one further piece of data that would help evaluate the argument.', 'Turnout in comparable countries with compulsory voting, or survey data on why young people do not vote.', '1 mark data; 1 mark why useful [2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


@c5c.add('C4', (2, 3, 4, 5), 'long')
def c5c_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'statistics used in debates about {i["name"]} tell us more about the people presenting them than about the issue',
                   ['Statistics are selected and presented to support a perspective (e.g. truncated axes, percentages vs percentage points).', 'Vested interests affect which data are collected and published.'],
                   ['Well-collected statistics from neutral sources (statistics offices, peer-reviewed studies) are strong evidence.', 'Misuse can be detected by checking method, sample and presentation.'],
                   'Statistics can be strong evidence, but only when their source, method and presentation are evaluated.')


CHAPTERS[5] = [c5a, c5b, c5c]


# ============================================================== CHAPTER 6: Evaluating arguments

c6a = T('Logic and coherence of reasoning; relevance and sufficiency', 'logic coherence reasoning relevance sufficiency')
add_terms(c6a, [
    ('relevance', 'whether a reason or piece of evidence actually bears on the conclusion'),
    ('sufficiency', 'whether the reasons and evidence given are enough to justify the conclusion'),
    ('consistency', 'the absence of contradictions between the claims in an argument'),
    ('coherence', 'the quality of an argument whose parts fit together logically to support the conclusion'),
    ('inference', 'a conclusion drawn from evidence or reasoning'),
    ('generalisation', 'a broad claim made on the basis of particular cases'),
], D1=(1, 2), D2=(1, 2, 3))


@c6a.add('C1', (1, 2, 3), 'mcq')
def c6a_irrel(r, D):
    i = issue(r)
    o = issue(r, avoid=[i['key']])
    a = i['arg']
    return MC(r, f'An author argues that {a["conc"]}. Which statement is NOT relevant to this conclusion?', o['fact'],
              [cap(a['r1']) + '.', cap(a['r2']) + '.', cap(a['ev']) + '.'], f'{o["fact"]} concerns a different issue ({o["name"]}), so it does not bear on the conclusion.')


@c6a.add('C2', (1, 2, 3), 'mcq')
def c6a_infer(r, D):
    co = r.choice(COUNTRIES)
    y1 = r.choice([2014, 2015, 2016, 2017, 2018])
    y2 = y1 + r.choice([4, 5])
    a = r.randint(62, 78); b = a - r.randint(4, 12)
    ans = f'Turnout fell by {a - b} percentage points between {y1} and {y2}'
    return MC(r, f'In {co}, turnout at the general election was {a}% in {y1} and {b}% in {y2}. Which conclusion can be reliably drawn?', ans,
              [f'Fewer people voted in {y2} than in {y1}', f'Voters were less interested in politics in {y2}', 'Turnout will fall again at the next election', f'Turnout fell by {pct(100 * (a - b) / b)} between {y1} and {y2}'],
              f'Only the change in percentage points follows; the number of voters depends on the size of the electorate, and interest or future trends are not shown. ({a} − {b} = {a - b} points.)')


@c6a.add('C2', (1, 2, 3, 4), 'explain')
def c6a_suff(r, D):
    reason, conc, ass, _ = mini(r)
    return Q(f'“{cap(reason)}. Therefore {conc}.” Explain whether the reason given is sufficient to support the conclusion.',
             f'Not sufficient: the reason is relevant, but the conclusion also needs it to be true that {ass}; more evidence is needed to rule out other explanations.',
             '1 mark judgement (insufficient); 1 mark identifies the gap/what else is needed; 1 mark explains why [3]', 3, 'explain')


@c6a.add('C2', (2, 3, 4), 'explain')
def c6a_consist(r, D):
    i = issue(r)
    co = r.choice(COUNTRIES)
    a = i['actions'][0]
    txt = (f'“The {a[1]} in {co} has no power to change anything about {i["name"]}. Its decisions are the main reason the problem has become so serious. '
           f'Therefore it should {a[0]}.”')
    return Q(f'Read this argument: {txt} Identify the inconsistency in the argument and explain its effect.',
             'It claims the authority has no power to change anything, yet says its decisions caused the problem and that it should act; these claims contradict each other, so the argument is incoherent and less persuasive.',
             '1 mark identifies the two conflicting claims; 1 mark explains why they conflict; 1 mark effect on the argument [3]', 3, 'explain')


@c6a.add('C3', (2, 3, 4, 5), 'case')
def c6a_case(r, D):
    i = issue(r)
    o = issue(r, avoid=[i['key']])
    a = i['arg']
    n = r.choice([3, 4, 5])
    txt = (f'{cap(a["r1"])}. {o["fact"]} A survey of {n * 10} people in {city(r)} found most agreed. Therefore, {a["conc"]}.')
    parts = [
        lambda r: ('Identify one statement that is irrelevant to the conclusion.', o['fact'], '1 mark [1]'),
        lambda r: ('Explain why the survey evidence is insufficient to support the conclusion.', f'Only {n * 10} people in one city were asked; they may not be representative, and agreement does not show that the policy would work.', '1 mark small/local sample; 1 mark opinion ≠ effectiveness [2]'),
        lambda r: ('Identify an assumption needed for the conclusion to follow.', cap(a['assume']) + '.', '1 mark [1]'),
        lambda r: ('Suggest how the argument could be made more coherent.', f'Remove the irrelevant statement, add evidence such as “{a["ev"]}”, link reasons explicitly to an intermediate conclusion and respond to the counter-argument that {a["counter"]}.',
                   '1 mark each relevant improvement, max 3 [3]'),
    ]
    return compose(r, f'Read the argument: “{txt}”', parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c6a.add('C4', (2, 3, 4, 5), 'long')
def c6a_essay(r, D):
    i = issue(r)
    a = i['arg']
    return essay_q(r, D, f'the reasons given for the view that {a["conc"]} are sufficient to justify it',
                   [cap(a['r1']) + '.', cap(a['r2']) + '.', cap(a['ev']) + '.'],
                   [f'It relies on the assumption that {a["assume"]}.', f'It does not fully answer the objection that {a["counter"]}.'],
                   'A supported judgement tests relevance, sufficiency and assumptions, and says what extra evidence would be needed.')


FLAWS = {
    'Hasty generalisation': 'drawing a general conclusion from too few or untypical cases',
    'Post hoc (false cause)': 'assuming that because one event followed another, the first caused the second',
    'Slippery slope': 'claiming that one step will inevitably lead to a chain of extreme consequences without evidence',
    'Ad hominem': 'attacking the person making an argument rather than the argument itself',
    'Straw man': 'misrepresenting an opponent’s argument as a weaker or more extreme version so it is easier to attack',
    'Appeal to popularity': 'claiming something is true or right because many people believe it',
    'False dichotomy': 'presenting only two options when others exist',
    'Appeal to inappropriate authority': 'relying on the opinion of someone who has no expertise on the subject',
    'Circular reasoning': 'using the conclusion as one of the reasons for it',
    'Tu quoque': 'dismissing a criticism because the critic is also guilty of the same thing',
}


def flaw_text(r, k, i):
    p, c, co, co2 = person(r), city(r), r.choice(COUNTRIES), r.choice(COUNTRIES)
    a = r.choice(i['actions'])
    conc = i['arg']['conc']
    if k == 'Hasty generalisation':
        n = r.choice([6, 8, 10, 12, 15])
        return f'{p} asked {n} people at a {r.choice(["rally", "café", "university debate", "football match"])} in {c} and {n - r.randint(1, 3)} of them said the {a[1]} should {a[0]}. This proves that most people in the country support it.'
    if k == 'Post hoc (false cause)':
        return f'In {r.choice([2015, 2017, 2019, 2021])}, {co} decided to {a[0]}. Two years later, {r.choice(["trust in government rose", "the economy grew faster", "the number of protests fell"])}. Clearly the policy caused this.'
    if k == 'Slippery slope':
        return f'If we agree to {a[0]} now, it will be only the first step: ever more extreme measures will follow, and before long {r.choice(["we will have lost control of our own country", "ordinary people will have no freedom left", "the whole political system will collapse"])}.'
    if k == 'Ad hominem':
        return f'We should ignore {p}’s argument that {conc}: {p} {r.choice(["failed politics at university", "has never held a proper job", "dresses badly on television"])}.'
    if k == 'Straw man':
        return f'People who say that {conc} really want {r.choice(["to tear down every existing institution overnight", "the government to control everything we do", "to abolish all national borders immediately"])}. That is absurd, so their view should be rejected.'
    if k == 'Appeal to popularity':
        return f'Millions of people have shared posts saying that {conc}, so it must be the right policy.'
    if k == 'False dichotomy':
        return f'Either the {a[1]} must {a[0]}, or we accept that {i["name"]} will never be solved. There is no other choice.'
    if k == 'Appeal to inappropriate authority':
        return f'A famous {r.choice(["footballer", "film star", "pop singer", "chef"])} said in an interview that {conc}, so it must be true.'
    if k == 'Circular reasoning':
        return f'{cap(conc)}, because this is clearly what should happen, and what should happen is that {conc}.'
    return f'The government of {co2} has criticised {co} over {i["name"]}. But {co2} has the same problem itself, so the criticism is worthless.'


c6b = T('Common flaws in reasoning: generalisation, false cause, slippery slope and ad hominem', 'flaws in reasoning generalisation false cause slippery slope ad hominem')
c6b.fixed('C1', (1, 2), [(f'Which flaw in reasoning involves {d}?', k, f'{k}: {d}. [1]', [x for x in FLAWS if x != k]) for k, d in FLAWS.items()])
c6b.fixed('C1', (2, 3), [(f'What is meant by the flaw “{k}”?', cap(d) + '.', f'{k}: {d}. [1]', [cap(y) + '.' for x, y in FLAWS.items() if x != k]) for k, d in FLAWS.items()])


@c6b.add('C2', (1, 2, 3), 'mcq')
def c6b_name(r, D):
    i = issue(r)
    k = r.choice(list(FLAWS))
    t = flaw_text(r, k, i)
    stem = r.choice([f'Which flaw is shown in this argument? “{t}”', f'“{t}” Which flaw in reasoning does this contain?', f'A speaker says: “{t}” Identify the flaw.'])
    return MC(r, stem, k, r.sample([x for x in FLAWS if x != k], 3), f'{k}: {FLAWS[k]}.')


@c6b.add('C2', (2, 3, 4), 'explain')
def c6b_explain(r, D):
    i = issue(r)
    k = r.choice(list(FLAWS))
    t = flaw_text(r, k, i)
    return Q(f'“{t}” Name the flaw in this reasoning and explain why it weakens the argument.', f'{k}: the argument relies on {FLAWS[k]}, so the conclusion does not follow from the reasons given.',
             '1 mark names flaw; 1 mark explains how it applies here; 1 mark effect on conclusion [3]', 3, 'explain')


@c6b.add('C3', (2, 3, 4, 5), 'case')
def c6b_case(r, D):
    i = issue(r)
    k1, k2 = r.sample(list(FLAWS), 2)
    t1, t2 = flaw_text(r, k1, i), flaw_text(r, k2, i)
    intro = f'Read these two extracts from a debate about {i["name"]}. Extract 1: “{t1}” Extract 2: “{t2}”'
    parts = [
        lambda r: ('Name the flaw in Extract 1.', k1 + '.', '1 mark [1]'),
        lambda r: ('Name the flaw in Extract 2.', k2 + '.', '1 mark [1]'),
        lambda r: ('Explain why the reasoning in Extract 1 is flawed.', f'It relies on {FLAWS[k1]}.', '1 mark identifies feature; 1 mark explains why conclusion does not follow [2]'),
        lambda r: ('Explain why the reasoning in Extract 2 is flawed.', f'It relies on {FLAWS[k2]}.', '1 mark identifies feature; 1 mark explains why conclusion does not follow [2]'),
        lambda r: ('Suggest how one of the extracts could be rewritten to avoid the flaw.', f'e.g. Extract 1: replace the flawed move with relevant evidence, such as “{i["arg"]["ev"]}”, and a reason linked to the conclusion.', '1 mark identifies change; 1 mark improved reasoning [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c6b.add('C4', (3, 4, 5), 'case')
def c6b_case4(r, D):
    i = issue(r)
    a = i['arg']
    k1, k2 = r.sample(list(FLAWS), 2)
    txt = f'{cap(a["r1"])}. {flaw_text(r, k1, i)} {flaw_text(r, k2, i)} Therefore, {a["conc"]}.'
    parts = [
        lambda r: ('Identify two flaws in the argument.', f'{k1}; {k2}.', '1 mark each [2]'),
        lambda r: ('Explain how each flaw weakens the argument.', f'{k1}: {FLAWS[k1]}. {k2}: {FLAWS[k2]}. Neither gives a valid reason for the conclusion.', '2 marks each flaw explained [4]'),
        lambda r: ('Identify the strongest part of the argument and explain why.', f'“{cap(a["r1"])}” — it is a relevant reason that does not rely on a flaw.', '1 mark identification; 1 mark explanation [2]'),
        lambda r: ('Evaluate how far the argument supports its conclusion.', 'Only weakly: once the flawed parts are removed, one reason remains, without evidence; the conclusion may still be true but this argument does not establish it.',
                   '1 mark judgement; 1 mark remaining support; 1 mark distinguishes weak argument from false conclusion [3]'),
    ]
    return compose(r, f'Read this argument about {i["name"]}: “{txt}”', parts, k=(3, 4), type_='case')


@c6b.add('C4', (2, 3, 4, 5), 'long')
def c6b_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'flaws in reasoning are more common in political debate about {i["name"]} than in academic writing about it',
                   ['Politicians and campaigners aim to persuade quickly, using ad hominem, slippery slope or appeals to popularity.', 'Social media rewards emotional, simplified arguments.'],
                   ['Academic writing is peer reviewed, which removes many flaws.', 'Academics can still generalise from small samples or confuse correlation with causation.'],
                   'Flaws appear in both, but the purpose and checks of each type of writing affect how common they are.')


c6c = T('Comparing and judging the relative strength of two arguments', 'comparing and judging the relative strength of two arguments')
add_terms(c6c, [
    ('strength of an argument', 'how well its reasons and evidence support its conclusion'),
    ('weighing evidence', 'judging the relative importance and quality of different pieces of evidence'),
    ('balanced judgement', 'a conclusion that takes account of the strengths and weaknesses on both sides'),
    ('persuasive language', 'emotive or rhetorical wording intended to win agreement rather than to give reasons'),
])
EV_Q = [  # (text template, score)
    ('a peer-reviewed study comparing {k} countries over ten years', 3),
    ('official statistics from the national statistics office covering the whole country', 3),
    ('a report by an independent international organisation', 2),
    ('an interview with one family in {c}', 0),
    ('a press release from a company that would profit from the outcome', 0),
    ('an online poll on a campaign website', 0),
    ('a survey of 40 students at one school in {c}', 1),
]


def build_arg(r, side, i, strong):
    c = city(r)
    k = r.choice([12, 18, 25, 30])
    good = [e for e in EV_Q if e[1] >= 2]
    bad = [e for e in EV_Q if e[1] <= 1]
    e = r.choice(good if strong else bad)
    ev = e[0].replace('{k}', str(k)).replace('{c}', c)
    a = i['arg']
    if side == 'for':
        txt = f'{cap(a["r1"])}. This is supported by {ev}. ' + (f'Some argue that {a["counter"]}, but {a["rebut"]}. ' if strong else '') + f'So {a["conc"]}.'
        if not strong:
            txt = f'{flaw_text(r, r.choice(["Appeal to popularity", "Slippery slope", "Ad hominem"]), i)} ' + txt
    else:
        txt = f'{cap(a["counter"])}. This is supported by {ev}. ' + (f'Supporters point out that {a["r1"]}, but this does not outweigh the costs. ' if strong else '') + f'So it is wrong to say that {a["conc"]}.'
        if not strong:
            txt = f'{flaw_text(r, r.choice(["Appeal to popularity", "Straw man", "Ad hominem"]), i)} ' + txt
    return txt, ev


@c6c.add('C2', (1, 2, 3), 'mcq')
def c6c_mcq(r, D):
    i = issue(r)
    s = r.random() < 0.5
    ta, _ = build_arg(r, 'for', i, s)
    tb, _ = build_arg(r, 'against', i, not s)
    ans = 'Argument A' if s else 'Argument B'
    return MC(r, f'Argument A: “{ta}” Argument B: “{tb}” Which argument is stronger?', ans, ['Argument A' if not s else 'Argument B', 'Both are equally strong', 'Neither has any reasoning'],
              f'{ans} uses better-quality evidence, considers the other side and avoids flaws.')


@c6c.add('C2', (2, 3, 4), 'explain')
def c6c_why(r, D):
    i = issue(r)
    s = r.random() < 0.5
    ta, ea = build_arg(r, 'for', i, s)
    tb, eb = build_arg(r, 'against', i, not s)
    w, wev, wl, wlev = ('A', ea, 'B', eb) if s else ('B', eb, 'A', ea)
    return Q(f'Argument A: “{ta}” Argument B: “{tb}” Explain which argument is stronger.',
             f'Argument {w} is stronger: it is supported by {wev}, which is more reliable than {wlev}, and it responds to a counter-argument. Argument {wl} contains a flaw and weaker evidence.',
             '1 mark judgement; 1 mark compares quality of evidence; 1 mark refers to counter-argument or flaw [3]', 3, 'explain')


@c6c.add('C3', (2, 3, 4, 5), 'case')
def c6c_case(r, D):
    i = issue(r)
    s = r.random() < 0.5
    ta, ea = build_arg(r, 'for', i, s)
    tb, eb = build_arg(r, 'against', i, not s)
    w = 'A' if s else 'B'
    l = 'B' if s else 'A'
    parts = [
        lambda r: ('Identify the conclusion of each argument.', f'A: {i["arg"]["conc"]}. B: it is wrong to say that {i["arg"]["conc"]}.', '1 mark each [2]'),
        lambda r: ('Compare the evidence used in the two arguments.', f'A uses {ea}; B uses {eb}. Argument {w}’s evidence is larger-scale, more independent or more systematic.', '1 mark identifies each; 1 mark comparison of quality [2]'),
        lambda r: (f'Identify a flaw in Argument {l}.', f'Argument {l} begins with a flawed claim (e.g. appeal to popularity, slippery slope, straw man or ad hominem) that gives no real reason.', '1 mark flaw named; 1 mark explained [2]'),
        lambda r: ('Which argument is stronger? Justify your answer.', f'Argument {w}: better evidence, responds to the opposing view and avoids flaws; but it still relies on assumptions (e.g. {i["arg"]["assume"]}).',
                   '1 mark judgement; 2 marks justification comparing both; 1 mark limitation acknowledged [4]'),
    ]
    return compose(r, f'Argument A: “{ta}” Argument B: “{tb}”', parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c6c.add('C4', (2, 3, 4, 5), 'long')
def c6c_long(r, D):
    i = issue(r)
    s = r.random() < 0.5
    ta, ea = build_arg(r, 'for', i, s)
    tb, eb = build_arg(r, 'against', i, not s)
    m = lm(D)
    w = 'A' if s else 'B'
    stem = (f'Argument A: “{ta}” Argument B: “{tb}” Compare and evaluate the two arguments. Which is more convincing? '
            'In your answer consider reasoning, evidence, use of language and the perspectives each represents.')
    ans = (f'Argument {w} is more convincing: its evidence ({ea if s else eb}) is more reliable and representative, it responds to the opposing view, and it avoids flawed appeals. '
           f'The other relies on {eb if s else ea} and a flawed opening claim. However, both rest on assumptions, e.g. that {i["arg"]["assume"]}, and more evidence would be needed for a firm judgement.')
    key = levels(m, 'describes the arguments with little comparison.', 'compares the arguments using at least two criteria (evidence, reasoning, language, perspective) with some judgement.',
                 'sustained comparison across several criteria, evaluating evidence quality and flaws, leading to a clear, well-supported judgement.')
    return Q(stem, ans, key, m, 'long')


CHAPTERS[6] = [c6a, c6b, c6c]


# ============================================================== CHAPTER 7: Research skills

KW = {  # issue key -> (phrase, second term, synonym of second term, term to exclude)
    'turnout': ('"compulsory voting"', 'turnout', 'participation', 'Australia'),
    'disinfo': ('"social media"', 'disinformation', '"fake news"', 'advertising'),
    'climmig': ('"climate migration"', 'refugee', '"displaced persons"', 'tourism'),
    'corrupt': ('"public procurement"', 'corruption', 'bribery', 'sport'),
    'unsc': ('"Security Council"', 'veto', 'reform', 'football'),
    'vote16': ('"voting age"', 'youth', '"young people"', 'driving'),
    'quotas': ('"gender quotas"', 'parliament', 'legislature', 'business'),
    'surveil': ('"facial recognition"', 'police', 'surveillance', 'smartphone'),
    'press': ('"press freedom"', 'journalists', 'media', 'celebrity'),
    'water': ('"transboundary rivers"', 'dams', 'hydropower', 'fishing'),
    'plastic': ('"plastic waste"', 'export', 'trade', 'packaging'),
    'sanctions': ('"economic sanctions"', 'effectiveness', 'impact', 'sport'),
}


def good_q(r, i):
    a = r.choice(i['actions'])
    return r.choice([i['q'], f'How far do the benefits outweigh the drawbacks of the proposal that the {a[1]} should {a[0]}?',
                     f'To what extent is it the responsibility of the {a[1]} to address {i["name"]}?'])


RQ_WEAK = {
    'descriptive': ('It is descriptive, inviting an account rather than an argument', lambda i, r: f'Describe the history of {i["name"]}.'),
    'broad': ('It is too broad to answer in 2,000 words', lambda i, r: f'What are all the causes and effects of every global {low(i["area"])} issue?'),
    'closed': ('It is closed, with a single factual answer', lambda i, r: f'Which international body publishes data on {i["name"]}?'),
    'one-sided': ('It focuses on one perspective, so different perspectives cannot be compared', lambda i, r: f'Why does {i["persp"][0][0]} take the view that it {i["persp"][0][1]}?'),
    'unresearchable': ('It cannot be researched because no evidence could exist', lambda i, r: f'What will {i["name"]} be like in the year 2300?'),
}

c7a = T('Devising a research question for the essay', 'devising a research question for the essay')
add_terms(c7a, [
    ('research question', 'the focused, debatable question that an essay or report sets out to answer'),
    ('focus', 'the narrowing of a topic to a specific issue, place, group or time that can be researched in depth'),
    ('feasibility', 'whether a question can be researched with the time, sources and word count available'),
    ('contestable', 'open to reasonable disagreement, so that different perspectives can be compared'),
])


@c7a.add('C1', (1, 2, 3), 'mcq')
def c7a_best(r, D):
    i = issue(r)
    ks = r.sample(list(RQ_WEAK), 3)
    g = good_q(r, i)
    return MC(r, f'Which would be the most suitable question for a Global Perspectives essay on {i["name"]}?', g, [RQ_WEAK[k][1](i, r) for k in ks],
              'Best: focused, contestable, global, allows comparison of perspectives and can be researched.')


@c7a.add('C2', (1, 2, 3), 'mcq')
def c7a_weak(r, D):
    i = issue(r)
    k = r.choice(list(RQ_WEAK))
    return MC(r, f'A student’s proposed essay question is: “{RQ_WEAK[k][1](i, r)}” What is the main problem with it?', RQ_WEAK[k][0], [v[0] for kk, v in RQ_WEAK.items() if kk != k],
              f'{RQ_WEAK[k][0]}.')


@c7a.add('C2', (2, 3, 4), 'explain')
def c7a_why_good(r, D):
    i = issue(r)
    g = good_q(r, i)
    return Q(f'Explain why “{g}” is a suitable question for a Global Perspectives essay.',
             f'It is contestable, so different perspectives (e.g. {i["persp"][0][0]} and {i["persp"][1][0]}) can be compared; it is focused enough for the word limit; and it has a global dimension ({i["global"]}).',
             '1 mark contestable/perspectives; 1 mark focus/feasibility; 1 mark global dimension [3]', 3, 'explain')


@c7a.add('C3', (2, 3, 4, 5), 'explain')
def c7a_improve(r, D):
    i = issue(r)
    k = r.choice(list(RQ_WEAK))
    m = 3 if D <= 3 else 4
    return Q(f'{person(r)} proposes this essay question: “{RQ_WEAK[k][1](i, r)}” Identify its weakness and write an improved question, explaining why it is better.',
             f'Weakness: {low(RQ_WEAK[k][0])}. Improved: “{good_q(r, i)}” — focused, contestable and global, so perspectives can be compared within the word limit.',
             '1 mark weakness; 1 mark improved question; 1 mark explains improvement' + ('; 1 mark refers to perspectives/feasibility' if m == 4 else '') + f' [{m}]', m, 'explain')


@c7a.add('C3', (2, 3, 4, 5), 'case')
def c7a_narrow(r, D):
    i = issue(r)
    intro = f'{person(r)} is interested in {low(i["area"])} and wants to write an essay. The starting point is the broad topic “{i["area"]}”.'
    parts = [
        lambda r: ('Suggest a narrower issue within this topic area.', cap(i['name']) + '.', '1 mark [1]'),
        lambda r: ('Write a focused research question on that issue.', good_q(r, i), '1 mark focused; 1 mark contestable [2]'),
        lambda r: ('Identify two perspectives the essay could compare.', f'{cap(i["persp"][0][0])}: {i["persp"][0][1]}; {i["persp"][1][0]}: {i["persp"][1][1]}.', '1 mark each [2]'),
        lambda r: ('Explain one practical reason why the question is feasible.', 'There are accessible sources (reports by international bodies, academic articles, news), and the scope fits the word limit.', '1 mark source availability; 1 mark scope [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c7a.add('C4', (3, 4, 5), 'case')
def c7a_eval(r, D):
    i = issue(r)
    ks = r.sample(list(RQ_WEAK), 2)
    qs = [good_q(r, i), RQ_WEAK[ks[0]][1](i, r), RQ_WEAK[ks[1]][1](i, r)]
    order = r.sample(range(3), 3)
    best = 'ABC'[order.index(0)]
    intro = 'A teacher is reviewing three essay questions. ' + ' '.join(f'Question {"ABC"[j]}: “{qs[order[j]]}”' for j in range(3))
    parts = [
        lambda r: ('Identify the strongest question.', f'Question {best}.', '1 mark [1]'),
        lambda r: ('Explain the weakness of each of the other questions.', f'{RQ_WEAK[ks[0]][0]}; {low(RQ_WEAK[ks[1]][0])}.', '2 marks each [4]'),
        lambda r: (f'Explain how Question {best} allows the student to compare perspectives.', f'It is contestable, so e.g. {i["persp"][0][0]} and {i["persp"][1][0]} would answer differently, and their reasoning and evidence can be compared.', '1 mark contestable; 1 mark named perspectives; 1 mark comparison [3]'),
        lambda r: (f'Suggest one way Question {best} could be made more focused.', 'Limit it to a region, a time period or specific countries, e.g. “in South-East Asia since 2015”.', '1 mark suggestion; 1 mark why it helps [2]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


@c7a.add('C4', (2, 3, 4, 5), 'long')
def c7a_essay(r, D):
    i = issue(r)
    return essay_q(r, D, 'the choice of research question is the most important factor in the success of a Global Perspectives essay',
                   ['A focused, contestable question makes comparison of perspectives possible.', 'A poor question (descriptive, too broad) limits the marks available for analysis and evaluation.'],
                   ['The quality of sources and evidence matters as much.', 'Clear structure, evaluation and referencing also determine success.'],
                   f'The question sets the limits of what is possible, but success depends on research and evaluation too; e.g. “{i["q"]}” still needs credible sources.')


c7b = T('Searching for and selecting sources: databases, keywords and reading strategies', 'searching selecting sources databases keywords reading strategies')
add_terms(c7b, [
    ('Boolean operator', 'a word such as AND, OR or NOT used to combine or exclude search terms'),
    ('keyword', 'an important word or phrase used to search for sources on a topic'),
    ('academic database', 'an online collection of scholarly articles and books, such as JSTOR or Google Scholar'),
    ('skimming', 'reading quickly to get the general idea of a text'),
    ('scanning', 'searching a text quickly for specific information, such as a name or figure'),
    ('lateral reading', 'checking a source by opening other tabs to see what independent sources say about it'),
], D1=(1, 2), D2=(1, 2, 3))
add_mcqs(c7b, 'C1', (1, 2, 3), [
    ('Which Boolean operator narrows a search so that results must contain both terms?', 'AND', ['OR', 'NOT', 'ALL'], 'AND requires both terms.'),
    ('Which Boolean operator broadens a search to include either of two terms?', 'OR', ['AND', 'NOT', 'ONLY'], 'OR includes either term.'),
    ('What does putting a phrase in quotation marks usually do in a search engine?', 'Searches for the exact phrase in that order', ['Excludes the phrase', 'Searches for any one of the words', 'Translates the phrase'], 'Quotation marks = exact phrase.'),
    ('What does the CRAAP test check?', 'Currency, relevance, authority, accuracy and purpose of a source', ['Cost, reach, audience, author and publisher', 'Credibility, reliability, accuracy, age and price', 'Citation, references, abstract, appendix and pages'], 'CRAAP = Currency, Relevance, Authority, Accuracy, Purpose.'),
    ('Which domain is most likely to belong to a government body?', '.gov', ['.com', '.biz', '.net'], '.gov is reserved for government bodies (in many countries a variant such as .gov.uk).'),
])


@c7b.add('C1', (1, 2, 3), 'mcq')
def c7b_string(r, D):
    i = issue(r)
    a, b, syn, ex = KW[i['key']]
    kind = r.choice(['both', 'either', 'exclude'])
    if kind == 'both':
        ans = f'{a} AND {b}'
        ds = [f'{a} OR {b}', f'{a} NOT {b}', f'{b} NOT {a}']
        need = f'contain both {a} and {b}'
    elif kind == 'either':
        ans = f'{a} AND ({b} OR {syn})'
        ds = [f'{a} AND {b} AND {syn}', f'{a} NOT ({b} OR {syn})', f'{a} OR {b} OR {syn}']
        need = f'contain {a} together with either {b} or {syn}'
    else:
        ans = f'{a} AND {b} NOT {ex}'
        ds = [f'{a} AND {b} AND {ex}', f'{a} OR {b} OR {ex}', f'{a} NOT {b} AND {ex}']
        need = f'contain {a} and {b} but not {ex}'
    return MC(r, f'A student researching {i["name"]} wants results that {need}. Which search string should be used?', ans, ds, f'{ans}.')


@c7b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c7b_venn(r, D):
    i = issue(r)
    a, b, syn, ex = KW[i['key']]
    na = r.choice([4200, 5600, 8100, 12400, 15800])
    nb = r.choice([2300, 3100, 6700, 9300])
    both = r.choice([600, 850, 1200, 1500, 1900])
    if both >= min(na, nb):
        return None
    either = na + nb - both
    stem = f'In an academic database, searching {a} gives {na:,} results and {b} gives {nb:,}; {a} AND {b} gives {both:,}.'
    if D <= 2:
        return MC(r, stem + f' How many results would {a} OR {b} give?', f'{either:,}', [f'{na + nb:,}', f'{both:,}', f'{na - both:,}'],
                  f'OR = {na:,} + {nb:,} − {both:,} = {either:,} (the overlap is counted once).')
    only = na - both
    stem += f' Calculate the number of results for {a} OR {b}, and for {a} NOT {b}. Explain which search would be most useful for an essay on “{i["q"]}”.'
    return Q(stem, f'OR: {na:,} + {nb:,} − {both:,} = {either:,}. NOT: {na:,} − {both:,} = {only:,}. AND ({both:,}) is most useful: it is focused on both aspects and manageable, though still needs filtering by date and source type.',
             '1 mark OR with overlap subtracted; 1 mark NOT; 1 mark justified choice; 1 mark further narrowing (filters, date, peer review) [4]', 4, 'numerical')


@c7b.add('C2', (1, 2, 3, 4), 'explain')
def c7b_strategy(r, D):
    i = issue(r)
    s = r.choice([('skimming', 'to decide quickly whether a long report on the issue is relevant'), ('scanning', 'to find a specific statistic in a long report'),
                  ('lateral reading', 'to check whether an unfamiliar website is credible'), ('reading the abstract first', 'to judge whether an academic article is relevant before reading it all')])
    return Q(f'A student researching {i["name"]} needs {s[1]}. Explain why {s[0]} is a suitable strategy.',
             f'{cap(s[0])} saves time and focuses effort: it lets the student {s[1][3:]} without reading every word, so more sources can be considered.',
             '1 mark describes the strategy; 1 mark explains why it suits the purpose [2]', 2, 'explain')


@c7b.add('C3', (2, 3, 4, 5), 'case')
def c7b_case(r, D):
    i = issue(r)
    a, b, syn, ex = KW[i['key']]
    hi, lo = r.choice(SRC_HIGH), r.choice(SRC_LOW)
    intro = f'{person(r)} is researching the question “{i["q"]}”. A general web search returns millions of results, including {hi[0]} and {lo[0]}.'
    parts = [
        lambda r: ('Suggest a better search string, using Boolean operators.', f'{a} AND ({b} OR {syn}) NOT {ex}', '1 mark AND/OR combination; 1 mark relevant terms [2]'),
        lambda r: ('Suggest one way to limit the results further.', 'Filter by date (e.g. last ten years), use an academic database or limit to .gov/.org/.edu domains.', '1 mark [1]'),
        lambda r: ('Explain which of the two sources should be selected.', f'{cap(hi[0])}: {hi[1]}; whereas {lo[0]}: {lo[2]}.', '1 mark choice; 1 mark reason based on credibility [2]'),
        lambda r: ('Explain why the student should also look for sources with a different perspective.', 'The essay must compare perspectives; using only sources that agree would produce a one-sided, biased answer.', '1 mark need to compare; 1 mark risk of bias [2]'),
        lambda r: ('Describe a reading strategy for dealing with a long report.', 'Skim the contents/summary first, then scan for key terms and data relevant to the question, making notes with page numbers.', '1 mark strategy; 1 mark applied [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c7b.add('C4', (2, 3, 4, 5), 'long')
def c7b_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'academic databases are more useful than general search engines for researching {i["name"]}',
                   ['Databases contain peer-reviewed articles with checked methods.', 'Filters by subject and date give focused, credible results.'],
                   ['Academic work may be slow to cover recent events.', 'Search engines find reports by NGOs, international organisations and news needed for current perspectives.'],
                   'The best research combines both, evaluating each source’s credibility.')


SURN = ['Okafor', 'Lindqvist', 'Ramírez', 'Tanaka', 'Haddad', 'Mensah', 'Kowalski', 'Nguyen', 'Silva', 'Banerjee', 'Novak', 'Adeyemi', 'Petrov', 'Moreau', 'Chen', 'Duarte']
PUBS = [('Harbour Academic Press', 'London'), ('Meridian University Press', 'Toronto'), ('Northgate Books', 'Singapore'), ('Lakeside Publishing', 'Cape Town')]
JOURNALS = ['Journal of Comparative Governance', 'Review of Global Governance Studies', 'International Politics Quarterly', 'Democracy and Society Review']
SUBT = ['a comparative study', 'evidence from ten democracies', 'policy and practice', 'perspectives from the Global South', 'challenges and responses']


def ref_book(r, i):
    s = r.choice(SURN)
    ini = r.choice('ABCDEFGHJKLMNPRST')
    y = r.randint(2012, 2025)
    t = f'{cap(i["name"])}: {r.choice(SUBT)}'
    pub, place = r.choice(PUBS)
    good = f'{s}, {ini}. ({y}) {t}. {place}: {pub}.'
    bad = [f'{ini}. {s} ({y}) {t}. {place}: {pub}.', f'{t}. {s}, {ini}. ({y}). {place}: {pub}.', f'{s}, {ini}. {t}. {place}: {pub}.', f'{s} ({y}) {t}.']
    return dict(s=s, ini=ini, y=y, t=t, pub=pub, place=place, good=good, bad=bad, cite=f'({s}, {y})')


c7c = T('Note-making, referencing and avoiding plagiarism', 'note-making referencing plagiarism')
add_terms(c7c, [
    ('plagiarism', 'presenting someone else’s words or ideas as your own without acknowledgement'),
    ('paraphrase', 'expressing someone else’s idea in your own words, still with a citation'),
    ('in-text citation', 'a short reference in the text, such as (Author, year), linking to the full reference list'),
    ('reference list', 'the full details of every source cited, in alphabetical order of author at the end of the work'),
    ('Harvard referencing', 'an author–date system of citation, with a reference list ordered alphabetically by author'),
    ('direct quotation', 'the exact words of a source, placed in quotation marks and cited'),
])


@c7c.add('C1', (1, 2, 3), 'mcq')
def c7c_ref(r, D):
    i = issue(r)
    b = ref_book(r, i)
    return MC(r, f'A student used a book by {b["ini"]}. {b["s"]}, titled “{b["t"]}”, published in {b["y"]} by {b["pub"]} in {b["place"]}. Which is the correct Harvard reference?', b['good'], b['bad'],
              f'Harvard: Surname, Initial. (Year) Title. Place: Publisher. → {b["good"]}')


@c7c.add('C1', (1, 2, 3), 'mcq')
def c7c_cite(r, D):
    i = issue(r)
    b = ref_book(r, i)
    pg = r.randint(12, 240)
    return MC(r, f'A student quotes page {pg} of a {b["y"]} book by {b["ini"]}. {b["s"]}. Which in-text citation follows the Harvard style?', f'({b["s"]}, {b["y"]}, p. {pg})',
              [f'({b["ini"]}. {b["s"]}, p. {pg})', f'({b["t"]}, {b["y"]})', f'[{b["s"]} {pg}]'], 'Harvard in-text: (Surname, year, p. page) for a quotation.')


@c7c.add('C2', (1, 2, 3), 'mcq')
def c7c_plag(r, D):
    i = issue(r)
    s = r.choice(SURN)
    cases = [
        ('Copying a paragraph from a report and changing a few words, without a citation', True),
        (f'Quoting a sentence from {s} in quotation marks with an in-text citation', False),
        (f'Summarising an argument from {s} in your own words with a citation', False),
        ('Using a statistic from a website without saying where it came from', True),
        ('Including a common-knowledge fact, such as the date the UN was founded, without a citation', False),
        ('Submitting a teammate’s notes as your own reflective paper', True),
    ]
    yes = [c for c, p in cases if p]
    no = [c for c, p in cases if not p]
    if r.random() < 0.5:
        return MC(r, f'While researching {i["name"]}, which action by a student would be plagiarism?', r.choice(yes), no, 'Plagiarism = using others’ words/ideas without acknowledgement.')
    return MC(r, f'While researching {i["name"]}, which action by a student is NOT plagiarism?', r.choice(no), yes, 'Cited quotations and paraphrases, and common knowledge, are not plagiarism.')


@c7c.add('C2', (2, 3, 4), 'explain')
def c7c_why(r, D):
    i = issue(r)
    return Q(r.choice([f'Explain two reasons why accurate referencing matters in an essay on {i["name"]}.', 'Explain why referencing is important in a Global Perspectives essay.']),
             'It acknowledges others’ work and avoids plagiarism; it lets the reader check the evidence and judge the credibility of sources; it shows the range of research.',
             '1 mark each reason, 1 mark each developed [4]', 4, 'explain')


@c7c.add('C3', (2, 3, 4, 5), 'case')
def c7c_case(r, D):
    i = issue(r)
    b = ref_book(r, i)
    pg = r.randint(12, 240)
    quote = f'{cap(i["arg"]["ic"])}.'
    intro = f'{person(r)} is writing an essay on “{i["q"]}”. The student reads page {pg} of {b["t"]} by {b["ini"]}. {b["s"]}, published by {b["pub"]}, {b["place"]}, in {b["y"]}. The author writes: “{quote}”'
    parts = [
        lambda r: ('Write a Harvard reference for the book.', b['good'], '1 mark author format; 1 mark year/title order; 1 mark place: publisher [3]'),
        lambda r: ('Write an in-text citation for a direct quotation from page ' + str(pg) + '.', f'({b["s"]}, {b["y"]}, p. {pg})', '1 mark [1]'),
        lambda r: ('Paraphrase the quotation in your own words.', 'Any accurate rewording keeping the meaning, followed by a citation ' + b['cite'] + '.', '1 mark accurate meaning in own words; 1 mark citation [2]'),
        lambda r: ('Explain one method of note-making that would help the student avoid accidental plagiarism.', 'Record full source details and page numbers with every note; put copied words in quotation marks and write summaries in their own words, e.g. using Cornell notes.',
                   '1 mark method; 1 mark how it avoids plagiarism [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c7c.add('C3', (1, 2, 3, 4, 5), 'short')
def c7c_order(r, D):
    i = issue(r)
    n = 3 if D <= 2 else 4
    names = r.sample(SURN, n)
    ys = [r.randint(2010, 2025) for _ in names]
    lst = '; '.join(f'{s} ({y})' for s, y in zip(names, ys))
    order = sorted(names)
    m = 2 if D <= 3 else 3
    return Q(f'A reference list for an essay on {i["name"]} contains sources by: {lst}. In what order should they appear in a Harvard reference list?',
             ', '.join(order) + '.', f'Alphabetical by author surname: {", ".join(order)}. ' + ('2 marks fully correct, 1 mark one pair wrong' if m == 2 else '3 marks fully correct, 2 one pair wrong, 1 first item correct') + f' [{m}]', m, 'short')


@c7c.add('C4', (2, 3, 4, 5), 'long')
def c7c_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'when researching an issue such as {i["name"]}, avoiding plagiarism is mainly the responsibility of the student rather than the school',
                   ['Students choose how to take notes and must cite sources accurately.', 'Plagiarism is a matter of academic honesty and personal integrity.'],
                   ['Schools must teach referencing and note-making explicitly.', 'Easy access to AI tools and online text means schools need clear rules and checking systems.'],
                   'Responsibility is shared, but the student is ultimately accountable for the work submitted.')


CHAPTERS[7] = [c7a, c7b, c7c]


# ============================================================== CHAPTER 8: The essay (Component 2)

SECTIONS = ['Introduction', 'Perspective 1 and its evidence', 'Perspective 2 and its evidence', 'Comparison and evaluation', 'Conclusion']

c8a = T('Structuring an argumentative essay that compares perspectives', 'structuring an argumentative essay that compares perspectives')
add_terms(c8a, [
    ('introduction', 'the opening section, which sets out the question, its context and global significance, and the perspectives to be compared'),
    ('thematic structure', 'organising an essay by themes or criteria, comparing perspectives within each section'),
    ('signposting', 'phrases that tell the reader where the argument is going, such as “In contrast…” or “This suggests…”'),
    ('topic sentence', 'the first sentence of a paragraph, stating its main point'),
    ('word limit', 'the maximum length allowed; for the AS essay, 1,750–2,000 words'),
])
add_mcqs(c8a, 'C1', (1, 2, 3), [
    ('What is the recommended length of the Cambridge AS Global Perspectives essay (Component 2)?', '1,750–2,000 words', ['500–800 words', '3,000–3,500 words', '5,000 words'], 'The essay is 1,750–2,000 words.'),
    ('Which feature is essential in a Global Perspectives essay?', 'Comparison and evaluation of different perspectives on the question', ['A summary of one source', 'A description of the history of the topic', 'Personal opinions without evidence'], 'Comparing and evaluating perspectives is central.'),
    ('Where should the essay first state the perspectives that will be compared?', 'In the introduction', ['Only in the conclusion', 'In the reference list', 'In a footnote'], 'The introduction sets out the question and perspectives.'),
])


@c8a.add('C2', (1, 2, 3), 'mcq')
def c8a_purpose(r, D):
    i = issue(r)
    k = r.randrange(len(SECTIONS))
    purpose = ['States the question, explains its global importance and outlines the perspectives',
               f'Explains the first perspective (e.g. {i["persp"][0][0]}) with its reasoning and evidence',
               f'Explains a contrasting perspective (e.g. {i["persp"][1][0]}) with its reasoning and evidence',
               'Weighs the perspectives against each other, evaluating reasoning and sources',
               'Reaches a supported judgement on the question and notes limitations'][k]
    others = [s for j, s in enumerate(SECTIONS) if j != k]
    return MC(r, f'In an essay on “{i["q"]}”, which section would do the following? “{purpose}.”', SECTIONS[k], others, f'{SECTIONS[k]}.')


@c8a.add('C2', (2, 3, 4), 'explain')
def c8a_thematic(r, D):
    i = issue(r)
    return Q(f'Explain why a thematic structure may be better than a “block” structure (one perspective, then the other) for an essay on “{i["q"]}”.',
             'A thematic structure compares perspectives point by point within each theme (e.g. effectiveness, rights, cost), so evaluation runs through the essay; a block structure risks two separate descriptions with comparison left to the end.',
             '1 mark describes thematic; 1 mark describes block weakness; 1 mark explains benefit for comparison/evaluation [3]', 3, 'explain')


@c8a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c8a_words(r, D):
    i = issue(r)
    total = r.choice([1750, 1800, 1850, 1900, 2000])
    shares = r.choice([[10, 25, 25, 30, 10], [10, 20, 20, 35, 15], [12, 22, 22, 32, 12], [8, 26, 26, 30, 10]])
    words = [total * s / 100 for s in shares]
    tab = ', '.join(f'{s} {p}%' for s, p in zip(SECTIONS, shares))
    if D <= 2:
        j = r.choice([0, 3, 4])
        return Q(f'{person(r)} plans a {total:,}-word essay on “{i["q"]}”: {tab}. How many words should the {SECTIONS[j].lower()} be?',
                 f'{fmt(round(words[j]))} words', f'{shares[j]}% × {total:,} = {fmt(round(words[j]))} words. 1 mark method, 1 mark answer [2]', 2, 'numerical')
    drafted = [round(w + r.choice([-60, -30, 0, 40, 80, 120])) for w in words]
    dt = sum(drafted)
    over = dt - 2000
    stem = (f'{person(r)} plans an essay on “{i["q"]}” with this allocation: {tab}, for {total:,} words. The first draft sections contain '
            + ', '.join(f'{s} {d}' for s, d in zip(SECTIONS, drafted)) + ' words. Calculate the planned length of each section and the total length of the draft. State whether the draft is within the 1,750–2,000 word range.')
    ans = 'Planned: ' + ', '.join(f'{s} {fmt(round(w))}' for s, w in zip(SECTIONS, words)) + f'. Draft total = {dt:,} words: ' + \
          (f'{over} words over the limit.' if over > 0 else ('within the range.' if dt >= 1750 else f'{1750 - dt} words short of the minimum.'))
    key = '1 mark planned lengths; 1 mark draft total; 1 mark correct judgement'
    m = 3
    if D >= 4:
        big = max(range(5), key=lambda j: drafted[j] - words[j])
        stem += ' Suggest which section should be revised first, and why.'
        ans += f' Revise the {SECTIONS[big].lower()} first: it exceeds its plan by the most ({drafted[big] - round(words[big])} words); keep the comparison/evaluation section strong as it carries most marks.'
        key += '; 1 mark identifies section most over plan; 1 mark justification linked to purpose/marks'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c8a.add('C3', (2, 3, 4, 5), 'case')
def c8a_plan(r, D):
    i = issue(r)
    h1, h2 = r.sample(i['persp'], 2)
    intro = f'{person(r)} is planning an essay on the question “{i["q"]}”.'
    parts = [
        lambda r: ('Suggest two perspectives the essay could compare.', f'{cap(h1[0])} ({h1[1]}); {h2[0]} ({h2[1]}).', '1 mark each [2]'),
        lambda r: ('Write a suitable opening sentence for the introduction.', f'e.g. “{cap(i["name"])} is a global issue because {i["global"]}; this essay compares the perspectives of {h1[0]} and {h2[0]}.”', '1 mark global context; 1 mark sets out perspectives [2]'),
        lambda r: ('Suggest two themes that could organise the main body.', 'e.g. effectiveness of proposed actions; rights and freedoms; costs; evidence from different countries.', '1 mark each [2]'),
        lambda r: ('Explain where the essay should evaluate sources.', 'Throughout the body, when each source is used (e.g. commenting on author, expertise and vested interest), not only at the end.', '1 mark integrated evaluation; 1 mark reason [2]'),
        lambda r: ('Explain what the conclusion must contain.', 'A clear, supported answer to the question that follows from the comparison, with limitations and possible further research.', '1 mark judgement; 1 mark linked to comparison; 1 mark limitations [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c8a.add('C4', (2, 3, 4, 5), 'long')
def c8a_essay(r, D):
    i = issue(r)
    return essay_q(r, D, 'the structure of an essay matters more than the quality of its evidence',
                   ['A clear structure makes comparison and evaluation visible to the reader.', 'Signposting and topic sentences show the line of argument.'],
                   ['Without credible evidence, a well-structured essay is still unconvincing.', 'Evaluation of sources is assessed directly.'],
                   f'Both are needed; e.g. an essay on “{i["q"]}” needs structure to compare perspectives and evidence to support the judgement.')


c8b = T('Using evidence to support analysis and evaluation', 'using evidence to support analysis and evaluation')
add_terms(c8b, [
    ('PEEL paragraph', 'a paragraph structure: Point, Evidence, Explanation, Link back to the question'),
    ('analysis', 'breaking an issue or argument into parts and explaining how they relate'),
    ('evaluation', 'judging the strengths and weaknesses of arguments, evidence and sources'),
    ('synthesis', 'bringing together evidence from different sources to form a new, combined understanding'),
], D1=(1, 2), D2=(1, 2, 3))
PEEL = ['Point', 'Evidence', 'Explanation', 'Link']


def peel(i):
    a = i['arg']
    return {'Point': cap(a['r1']) + '.', 'Evidence': 'For example: ' + cap(a['ev']) + '.', 'Explanation': 'This suggests that ' + a['ic'] + '.',
            'Link': f'This supports the view that {a["conc"]}, although {a["counter"]}.'}


@c8b.add('C1', (1, 2, 3), 'mcq')
def c8b_missing(r, D):
    i = issue(r)
    p = peel(i)
    miss = r.choice(PEEL)
    txt = ' '.join(p[k] for k in PEEL if k != miss)
    return MC(r, f'A paragraph from an essay on “{i["q"]}” reads: “{txt}” Which element of a PEEL paragraph is missing?', miss, [k for k in PEEL if k != miss],
              f'Missing: {miss}.')


@c8b.add('C2', (1, 2, 3, 4), 'explain')
def c8b_improve(r, D):
    i = issue(r)
    a = i['arg']
    return Q(f'A student writes: “{cap(a["ev"])}. This proves that {a["conc"]}.” Explain how the student could use this evidence more effectively.',
             f'Explain how the evidence supports a reason ({a["r1"]}), comment on its credibility and whether it can be generalised, and acknowledge the counter-argument that {a["counter"]}; “proves” overstates what one example shows.',
             '1 mark link evidence to reason; 1 mark evaluate source/generalisability; 1 mark avoid overstatement/consider counter-evidence [3]', 3, 'explain')


@c8b.add('C2', (1, 2, 3), 'mcq')
def c8b_eval(r, D):
    i = issue(r)
    s = r.choice(SRC_HIGH)
    ans = f'According to {s[0]}, which is credible because {s[1]}, …'
    ds = [f'Everyone knows that {i["arg"]["ic"]}.', f'I think that {i["arg"]["conc"]}.', f'A website says that {i["arg"]["ic"]}.']
    return MC(r, f'Which sentence shows the best use of evidence in an essay on {i["name"]}?', ans, ds, 'It names the source and evaluates its credibility.')


@c8b.add('C3', (2, 3, 4, 5), 'case')
def c8b_case(r, D):
    i = issue(r)
    p = peel(i)
    miss = r.choice(['Evidence', 'Explanation', 'Link'])
    txt = ' '.join(p[k] for k in PEEL if k != miss)
    s = r.choice(SRC_MID)
    parts = [
        lambda r: ('Identify the element of a PEEL paragraph that is missing.', miss + '.', '1 mark [1]'),
        lambda r: ('Write a sentence that would supply the missing element.', p[miss], '1 mark relevant; 1 mark fits the paragraph [2]'),
        lambda r: (f'The student wants to add evidence from {s[0]}. Explain how the student should comment on this source in the paragraph.', f'Name the source and evaluate it: {s[1]}, but {s[2]}; so its claim should be corroborated.', '1 mark strength; 1 mark weakness [2]'),
        lambda r: ('Explain how the paragraph could show synthesis of evidence.', 'Combine this evidence with a source from a different perspective, showing where they agree and differ, to build a more complete point.', '1 mark combine sources; 1 mark explains agreement/difference [2]'),
    ]
    return compose(r, f'Read this paragraph from an essay on “{i["q"]}”: “{txt}”', parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c8b.add('C4', (2, 3, 4, 5), 'long')
def c8b_essay(r, D):
    i = issue(r)
    return essay_q(r, D, f'in an essay on {i["name"]}, evaluating sources is more important than finding more evidence',
                   ['Evaluation shows which evidence can be trusted and why.', 'A few well-evaluated sources support stronger judgements than many unexamined ones.'],
                   ['Without enough evidence, perspectives cannot be compared fairly.', 'Corroboration needs several sources.'],
                   'Both matter; the best essays select a range of credible sources and evaluate them as they are used.')


c8c = T('Reaching a supported conclusion and acknowledging limitations', 'supported conclusion acknowledging limitations')
add_terms(c8c, [
    ('supported conclusion', 'a final judgement that answers the question and follows from the arguments and evidence discussed'),
    ('limitation', 'a weakness or restriction in the research, such as limited sources or a narrow focus'),
    ('further research', 'questions or evidence that could be investigated to test or extend the conclusion'),
    ('qualified judgement', 'a conclusion that states the conditions under which it holds, rather than claiming certainty'),
])
CONC_FAULTS = {
    'summary': ('It only summarises the essay without answering the question', lambda i: f'This essay has looked at {i["persp"][0][0]} and {i["persp"][1][0]} and their views on {i["name"]}.'),
    'new': ('It introduces a new argument not discussed in the essay', lambda i: f'In conclusion, the most important point, not mentioned earlier, is that {low(i["causes"][2][0])}.'),
    'fence': ('It refuses to reach a judgement', lambda i: f'In conclusion, there are good points on both sides about {i["name"]}, so it is impossible to say.'),
    'certain': ('It overstates certainty and ignores limitations', lambda i: f'In conclusion, it has been proved beyond doubt that {i["arg"]["conc"]}, and nobody could disagree.'),
}


def good_conc(i):
    a = i['arg']
    return f'Overall, the evidence suggests that {a["conc"]}, mainly because {a["r1"]}; however, this depends on the assumption that {a["assume"]}, and the research relied mostly on sources from a few countries.'


@c8c.add('C1', (1, 2, 3), 'mcq')
def c8c_best(r, D):
    i = issue(r)
    return MC(r, f'Which is the best conclusion for an essay on “{i["q"]}”?', good_conc(i), [CONC_FAULTS[k][1](i) for k in r.sample(list(CONC_FAULTS), 3)],
              'Best: a clear, qualified judgement that follows from the essay and acknowledges limitations.')


@c8c.add('C2', (1, 2, 3), 'mcq')
def c8c_fault(r, D):
    i = issue(r)
    k = r.choice(list(CONC_FAULTS))
    return MC(r, f'A student’s conclusion reads: “{CONC_FAULTS[k][1](i)}” What is the main weakness?', CONC_FAULTS[k][0], [v[0] for kk, v in CONC_FAULTS.items() if kk != k], CONC_FAULTS[k][0] + '.')


@c8c.add('C2', (2, 3, 4), 'explain')
def c8c_limit(r, D):
    i = issue(r)
    lim = r.choice([('most sources came from high-income countries', 'perspectives from the countries most affected may be missing'),
                    ('the word limit allowed only two perspectives', 'other important stakeholders were not considered'),
                    ('much of the evidence was from campaign groups', 'vested interests may have shaped the evidence'),
                    ('recent data were not available', 'the situation may have changed since the sources were written')])
    return Q(f'An essay on {i["name"]} found that {lim[0]}. Explain why the student should acknowledge this limitation in the conclusion.',
             f'Because {lim[1]}, the judgement is less certain; acknowledging it shows critical awareness, makes the conclusion more credible and suggests further research.',
             '1 mark effect of limitation on the judgement; 1 mark acknowledging shows reflection/credibility; 1 mark further research [3]', 3, 'explain')


@c8c.add('C3', (2, 3, 4, 5), 'case')
def c8c_case(r, D):
    i = issue(r)
    k = r.choice(list(CONC_FAULTS))
    txt = CONC_FAULTS[k][1](i)
    parts = [
        lambda r: ('Identify the main weakness of this conclusion.', CONC_FAULTS[k][0] + '.', '1 mark [1]'),
        lambda r: ('Rewrite the conclusion so that it reaches a supported judgement.', good_conc(i), '1 mark clear judgement; 1 mark supported by a reason from the essay; 1 mark qualified/limitation [3]'),
        lambda r: ('Suggest one limitation the student could acknowledge.', 'e.g. sources mainly from one region, limited recent data, only two perspectives compared, or reliance on sources with vested interests.', '1 mark [1]'),
        lambda r: ('Suggest one question for further research.', f'e.g. How have attempts to {i["actions"][1][0]} worked in practice in different countries?', '1 mark relevant question; 1 mark linked to limitation [2]'),
    ]
    return compose(r, f'A student’s essay on “{i["q"]}” ends: “{txt}”', parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c8c.add('C4', (2, 3, 4, 5), 'long')
def c8c_essay(r, D):
    i = issue(r)
    return essay_q(r, D, 'a good conclusion to a Global Perspectives essay should always take a clear side',
                   ['The question asks for a judgement, so the conclusion must answer it.', 'Sitting on the fence avoids the evaluation the essay has built up.'],
                   ['A qualified judgement (it depends on…) can be the most accurate answer.', 'Limitations may mean certainty is not justified.'],
                   f'A conclusion should give a clear but qualified answer; e.g. on “{i["q"]}”, stating the conditions under which each view holds.')


CHAPTERS[8] = [c8a, c8b, c8c]


# ============================================================== CHAPTER 9: The team project (Component 3)

LOCAL = [
    dict(p='low turnout in student council elections at a school', g='declining youth participation in elections in many democracies',
         sols=[('introduce online voting for student elections', 'it is quick and convenient', 'some students may lack access or worry about privacy'),
               ('hold candidate debates during lessons', 'students learn about candidates’ ideas', 'it takes time from teaching'),
               ('run a peer campaign explaining how the council has changed school life', 'it shows that voting makes a difference', 'its effect may be short-lived')]),
    dict(p='misleading health and election rumours shared in a neighbourhood messaging group', g='the global spread of online disinformation',
         sols=[('run media literacy workshops at the community centre', 'residents learn to check sources themselves', 'only motivated people may attend'),
               ('appoint volunteer “fact-check champions” in the group', 'corrections appear quickly where rumours spread', 'volunteers may be accused of bias'),
               ('share a simple checklist for verifying posts', 'it is cheap and easy to spread', 'people may ignore it')]),
    dict(p='young people having no say in decisions made by the town council', g='under-representation of young people in governance worldwide',
         sols=[('set up a youth advisory council', 'young people are consulted regularly', 'the council may ignore its advice'),
               ('hold a youth consultation online before major decisions', 'many people can take part', 'responses may not be representative'),
               ('reserve a seat for a youth representative at council meetings', 'young people are present when decisions are made', 'one person cannot represent all young people')]),
    dict(p='plastic waste from the school canteen', g='the global trade in and pollution from plastic waste',
         sols=[('replace single-use packaging with reusable containers', 'it cuts waste at source', 'it has an initial cost'),
               ('set up a recycling scheme with a local firm', 'waste is reused', 'mixed plastics may not be recyclable'),
               ('run a student awareness campaign', 'it changes habits', 'effects can fade')]),
    dict(p='newly arrived migrant families in the town struggling to access services', g='international migration, including migration linked to conflict and climate change',
         sols=[('create a multilingual guide to local services', 'it removes a language barrier', 'it must be kept up to date'),
               ('organise a student buddy scheme for new families', 'it builds personal support and community links', 'it depends on volunteers'),
               ('ask the council to provide interpreters at its offices', 'it helps with complex official matters', 'it is costly for the council')]),
    dict(p='lack of trust in the honesty of local officials', g='corruption and the demand for transparent government worldwide',
         sols=[('campaign for the council to publish its spending online', 'residents can check how money is spent', 'few residents may read the data'),
               ('hold a public question-time with councillors twice a year', 'officials answer residents directly', 'it may become a platform for speeches'),
               ('start a student journalism project on local decisions', 'it scrutinises decisions and builds skills', 'students may lack access to information')]),
]

c9a = T('Working collaboratively: roles, planning and team research', 'working collaboratively roles planning team research')
add_terms(c9a, [
    ('collaboration', 'working together towards a shared goal, combining different skills and contributions'),
    ('Gantt chart', 'a chart showing project tasks against time, including who does what and when'),
    ('SMART target', 'a goal that is Specific, Measurable, Achievable, Relevant and Time-bound'),
    ('delegation', 'giving responsibility for a task to a team member'),
    ('team research', 'research divided between team members, each investigating a different perspective or aspect of the problem'),
])
TUCK = [('Forming', 'members are polite and unsure of their roles'), ('Storming', 'disagreements arise over ideas and roles'),
        ('Norming', 'the team agrees ways of working and roles'), ('Performing', 'the team works effectively towards the goal'),
        ('Adjourning', 'the project ends and the team reflects and disbands')]
BELBIN = [('Plant', 'creative and generates new ideas'), ('Monitor Evaluator', 'judges ideas carefully and objectively'),
          ('Co-ordinator', 'clarifies goals and delegates tasks'), ('Shaper', 'drives the team forward under pressure'),
          ('Implementer', 'turns ideas into practical plans'), ('Completer Finisher', 'checks details and meets deadlines'),
          ('Teamworker', 'supports others and reduces conflict'), ('Resource Investigator', 'finds contacts and resources outside the team'),
          ('Specialist', 'brings in-depth knowledge of a particular subject')]


@c9a.add('C1', (1, 2, 3), 'mcq')
def c9a_tuck(r, D):
    k, d = r.choice(TUCK)
    l = local(r)
    return MC(r, f'A team working on {l["p"]} finds that {d}. Which stage of Tuckman’s model of team development is this?', k, [x for x, _ in TUCK if x != k], f'{k}: {d}.')


def local(r):
    return r.choice(LOCAL)


@c9a.add('C1', (1, 2, 3), 'mcq')
def c9a_belbin(r, D):
    k, d = r.choice(BELBIN)
    p = person(r)
    return MC(r, f'In a team project, {p} {d}. Which Belbin team role does {p} show?', k, r.sample([x for x, _ in BELBIN if x != k], 3), f'{k}: {d}.')


@c9a.add('C2', (1, 2, 3, 4), 'explain')
def c9a_split(r, D):
    l = local(r)
    return Q(f'A team is investigating {l["p"]}. Explain why each member should research a different perspective on the problem.',
             f'It ensures a range of perspectives (e.g. students, local officials, organisations working on {l["g"]}) is covered without duplication, and each member then brings distinct evidence to the team’s discussion of solutions.',
             '1 mark coverage of perspectives; 1 mark avoids duplication/efficiency; 1 mark improves the solution [3]', 3, 'explain')


@c9a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c9a_gantt(r, D):
    l = local(r)
    a, b, c, d = r.randint(2, 4), r.randint(3, 6), r.randint(2, 5), r.randint(1, 3)
    stem = (f'A team planning a project on {l["p"]} lists these tasks: A agree the problem and roles ({a} days); B individual research on perspectives ({b} days, after A); '
            f'C survey of students ({c} days, after A, can run at the same time as B); D agree the solution ({d} days, after both B and C).')
    tot = a + max(b, c) + d
    crit = 'A → B → D' if b > c else ('A → C → D' if c > b else 'A → B/C → D')
    if D <= 2:
        return MC(r, stem + ' What is the shortest time in which all tasks can be completed?', f'{tot} days', [f'{a + b + c + d} days', f'{a + min(b, c) + d} days', f'{a + b + d + 1} days' if a + b + d + 1 not in (tot, a + b + c + d) else f'{tot + 2} days'],
                  f'{a} + max({b}, {c}) + {d} = {tot} days.')
    m = 3 if D <= 3 else 4
    stem += ' Calculate the shortest completion time and identify the sequence of tasks that determines it.'
    ans = f'{a} + max({b}, {c}) + {d} = {tot} days; critical sequence {crit}.'
    key = '1 mark recognises B and C run in parallel; 1 mark total; 1 mark critical sequence'
    if m == 4:
        stem += ' Explain how a delay to the shorter of tasks B and C would affect the project.'
        sl = abs(b - c)
        ans += f' The shorter task has {sl} day(s) of slack, so a delay of up to {sl} day(s) would not change the finish date.'
        key += '; 1 mark slack explained'
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c9a.add('C3', (2, 3, 4, 5), 'case')
def c9a_case(r, D):
    l = local(r)
    p1, p2, p3 = r.sample(PEOPLE_T, 3)
    intro = f'{p1}, {p2} and {p3} form a team to address {l["p"]}. After two meetings, {p1} has done most of the work and {p3} has missed both meetings.'
    parts = [
        lambda r: ('Identify the stage of team development the team has reached.', 'Storming (conflict over roles/contribution) or still Forming.', '1 mark with reason [1]'),
        lambda r: ('Suggest two ways the team could improve its collaboration.', 'Agree roles and a Gantt chart with deadlines; hold short regular check-ins and record decisions; share documents online.', '1 mark each [2]'),
        lambda r: (f'Explain how {p1} could respond to {p3}’s absence constructively.', 'Contact them to find out why, agree a specific task and deadline, and adjust the plan if needed, rather than doing their work.', '1 mark communication; 1 mark agreed task/accountability [2]'),
        lambda r: ('Write a SMART target for the team’s research.', f'e.g. “By Friday each member will find and evaluate two credible sources on a different perspective on {l["p"]}.”', '1 mark specific/measurable; 1 mark time-bound [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c9a.add('C4', (2, 3, 4, 5), 'long')
def c9a_essay(r, D):
    l = local(r)
    return essay_q(r, D, 'the success of a team project depends more on good planning than on the abilities of individual members',
                   ['A clear plan with roles and deadlines prevents duplication and missed tasks.', 'Planning lets the team combine research on different perspectives.'],
                   ['Skilled, motivated members can overcome a weak plan.', 'Communication and trust matter as much as planning.'],
                   f'Planning provides the framework, but success also needs commitment and communication; e.g. a team addressing {l["p"]} needs both.')


PEOPLE_T = ['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Ethan', 'Priya', 'Omar', 'Hana', 'Jonas', 'Kwame', 'Elena']


c9b = T('Developing and justifying a solution to a local problem with a global dimension', 'solution to a local problem with a global dimension')
add_terms(c9b, [
    ('local problem', 'an issue experienced in the student’s own community, such as a school or town'),
    ('solution', 'a practical course of action that the team proposes to reduce or solve the problem'),
    ('justification', 'reasons and evidence showing why the proposed solution is the best option'),
    ('feasibility study', 'an assessment of whether a proposed solution can be carried out with the resources available'),
])


@c9b.add('C1', (1, 2, 3), 'mcq')
def c9b_global(r, D):
    l = local(r)
    others = [x['g'] for x in LOCAL if x is not l]
    return MC(r, f'A team addresses {l["p"]}. Which global issue is this local problem most clearly connected to?', cap(l['g']), [cap(x) for x in r.sample(others, 3)], f'Link: {l["g"]}.')


@c9b.add('C2', (1, 2, 3, 4), 'explain')
def c9b_adv(r, D):
    l = local(r)
    s = r.choice(l['sols'])
    return Q(f'A team proposes to {s[0]} to address {l["p"]}. Explain one strength and one weakness of this solution.', f'Strength: {s[1]}. Weakness: {s[2]}.',
             '1 mark strength, 1 mark developed; 1 mark weakness, 1 mark developed [4]', 4, 'explain')


@c9b.add('C3', (2, 3, 4, 5), 'numerical')
def c9b_cost(r, D):
    l = local(r)
    sols = l['sols']
    cost = [r.choice([150, 200, 300, 450, 600, 800]) for _ in sols]
    reach = [r.choice([60, 80, 120, 150, 200, 300, 400]) for _ in sols]
    cpp = [c / n for c, n in zip(cost, reach)]
    if len({round(x, 2) for x in cpp}) < 3:
        return None
    best = min(range(3), key=lambda j: cpp[j])
    tab = table(['Solution', 'Cost ($)', 'People reached'], [[s[0], c, n] for s, c, n in zip(sols, cost, reach)])
    stem = f'A team compares three solutions to {l["p"]}. {tab} Calculate the cost per person reached for each solution and identify the most cost-effective.'
    ans = '; '.join(f'{s[0]}: ${fmt(round(c / n, 2))}' for s, c, n in zip(sols, cost, reach)) + f'. Most cost-effective: {sols[best][0]}.'
    key = '1 mark method (cost ÷ people); 1 mark all values; 1 mark identification'
    m = 3
    if D >= 4:
        stem += ' Explain why the most cost-effective solution may not be the best one to recommend.'
        ans += f' Cost per person ignores how much each person is helped and how lasting the effect is; e.g. its weakness: {sols[best][2]}.'
        key += '; 1 mark effectiveness/depth of impact; 1 mark applies a weakness of the solution'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c9b.add('C3', (2, 3, 4, 5), 'case')
def c9b_case(r, D):
    l = local(r)
    s1, s2 = r.sample(l['sols'], 2)
    intro = f'A team in {city(r)} has researched {l["p"]}, which links to {l["g"]}. They are choosing between two solutions: to {s1[0]}, or to {s2[0]}.'
    parts = [
        lambda r: ('Explain the global dimension of the problem.', f'It is a local example of {l["g"]}, so research from other countries can inform the solution.', '1 mark link; 1 mark explained [2]'),
        lambda r: ('Explain one advantage of the first solution.', cap(s1[1]) + '.', '1 mark advantage; 1 mark developed [2]'),
        lambda r: ('Explain one disadvantage of the second solution.', cap(s2[2]) + '.', '1 mark disadvantage; 1 mark developed [2]'),
        lambda r: ('Suggest how the team could test which solution works better.', 'Run a small pilot of each and measure change, e.g. a before-and-after survey or count.', '1 mark pilot/trial; 1 mark measurable outcome [2]'),
        lambda r: ('Recommend one solution and justify it.', f'e.g. to {s1[0]}: {s1[1]}, and its drawback ({s1[2]}) can be reduced; the other’s drawback ({s2[2]}) is harder to overcome.', '1 mark choice; 1 mark reason; 1 mark comparison [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c9b.add('C4', (2, 3, 4, 5), 'long')
def c9b_essay(r, D):
    l = local(r)
    s = r.choice(l['sols'])
    return essay_q(r, D, f'the best way to address {l["p"]} is to {s[0]}',
                   [cap(s[1]) + '.', f'It responds to a local example of {l["g"]}.'],
                   [cap(s[2]) + '.', 'Other solutions may reach more people or last longer.'],
                   'A justified recommendation compares solutions on effectiveness, cost, feasibility and acceptability, using research evidence.')


c9c = T('Delivering an individual presentation', 'delivering an individual presentation', 'presentation')
add_terms(c9c, [
    ('presentation', 'a spoken explanation of research and a proposed solution, supported by visual aids'),
    ('visual aid', 'a slide, image, chart or object used to support a spoken presentation'),
    ('audience awareness', 'adapting content, language and delivery to the people listening'),
    ('cue card', 'a small card with key points used as a prompt while speaking'),
])
add_mcqs(c9c, 'C1', (1, 2, 3), [
    ('Which is the best use of slides in a presentation?', 'Short key points and clear charts that support what the speaker says', ['Full paragraphs to read aloud', 'As many images as possible on each slide', 'Complex tables with small text'], 'Slides support, not replace, the speaker.'),
    ('What should the end of an individual presentation include?', 'A clear summary of the proposed solution and the reasons for it', ['A new research topic', 'An apology for any mistakes', 'A list of team members’ hobbies'], 'Conclude with a justified solution.'),
])


@c9c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c9c_rate(r, D):
    p = person(r)
    wpm = r.choice([120, 130, 140, 150])
    mins = r.choice([6, 7, 8, 10])
    words = r.choice([900, 1100, 1250, 1400, 1600])
    need = wpm * mins
    t = words / wpm
    if D <= 2:
        return MC(r, f'{p} speaks at about {wpm} words per minute. About how many words should a {mins}-minute presentation script contain?', f'{need:,} words',
                  [f'{wpm + mins:,} words', f'{round(wpm * mins / 2):,} words', f'{wpm * (mins + 2):,} words'], f'{wpm} × {mins} = {need:,}.')
    stem = f'{p} speaks at about {wpm} words per minute and has a script of {words:,} words for a presentation that must last no more than {mins} minutes. Calculate how long the script would take and how many words must be cut, if any.'
    cut = max(0, words - need)
    ans = f'{words:,} ÷ {wpm} = {fmt(round(t, 1))} minutes; maximum = {need:,} words, so ' + (f'cut {cut:,} words.' if cut else 'no cut is needed.')
    key = '1 mark time; 1 mark maximum words; 1 mark words to cut'
    m = 3
    if D >= 4:
        stem += ' Suggest how to decide which content to cut.'
        ans += ' Keep the problem, key evidence and the justified solution; cut background detail and repeated points; slides can carry data.'
        key += '; 1 mark keeps essential content; 1 mark removes less important content'
        m = 5
    return Q(stem, ans, key + f' [{m}]', m, 'numerical')


@c9c.add('C2', (1, 2, 3, 4), 'explain')
def c9c_explain(r, D):
    l = local(r)
    f = r.choice([('cite sources on the slides', 'it shows the evidence is credible and avoids plagiarism'),
                  ('use a chart of survey results', 'it shows the scale of the problem quickly and clearly'),
                  ('practise with a timer', 'it keeps the presentation within the time limit and improves fluency'),
                  ('explain the global dimension', 'it shows how the local problem connects to wider issues and research'),
                  ('make eye contact rather than reading a script', 'it keeps the audience engaged and sounds more confident')])
    return Q(f'Explain why a student presenting a solution to {l["p"]} should {f[0]}.', cap(f[1]) + '.', '1 mark reason; 1 mark developed [2]', 2, 'explain')


@c9c.add('C3', (2, 3, 4, 5), 'case')
def c9c_case(r, D):
    l = local(r)
    s = r.choice(l['sols'])
    intro = f'{person(r)} is preparing an individual presentation on the team’s proposal to {s[0]} to address {l["p"]}. The first draft has twelve slides full of text and no sources.'
    parts = [
        lambda r: ('Suggest two improvements to the slides.', 'Fewer slides with key points; add a chart or image; cite sources on each slide.', '1 mark each [2]'),
        lambda r: ('Outline a suitable structure for the presentation.', 'Problem and its global dimension → research findings and perspectives → solution and justification → conclusion.', '1 mark logical order; 1 mark includes justification [2]'),
        lambda r: ('Explain how the student could show the solution is justified.', f'Use research evidence: e.g. {s[1]}; acknowledge the weakness ({s[2]}) and explain how it could be reduced.', '1 mark evidence; 1 mark limitation addressed [2]'),
        lambda r: ('Suggest one way to make the delivery more engaging.', 'Use cue cards rather than reading, vary tone, ask a rhetorical question, or show a short, relevant image.', '1 mark [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c9c.add('C4', (2, 3, 4, 5), 'long')
def c9c_essay(r, D):
    l = local(r)
    return essay_q(r, D, f'a presentation is a better way than a written report to communicate a proposed solution to {l["p"]}',
                   ['It can engage an audience directly, using visuals and voice.', 'The speaker can adapt to the audience.'],
                   ['A written report can include more evidence and detailed referencing.', 'Readers can return to it and check sources.'],
                   'Each suits different purposes; the presentation must still show credible evidence and justification.')


c9d = T('Writing a reflective paper on collaboration and learning', 'reflective paper collaboration learning', 'reflection')
add_terms(c9d, [
    ('reflection', 'thinking critically about an experience to learn from it and improve future work'),
    ('Gibbs’ reflective cycle', 'a model of reflection: description, feelings, evaluation, analysis, conclusion and action plan'),
    ('action plan', 'what the writer will do differently next time as a result of reflection'),
    ('evaluation (in reflection)', 'judging what went well and what went less well'),
], D1=(1, 2), D2=(1, 2, 3))
GIBBS = ['Description', 'Feelings', 'Evaluation', 'Analysis', 'Conclusion', 'Action plan']
GIBBS_S = {
    'Description': 'Our team met four times to research {p}; I researched the perspective of local officials.',
    'Feelings': 'I felt frustrated when our second meeting ended without a decision about {p}.',
    'Evaluation': 'Our survey on {p} went well, but our first deadline was missed.',
    'Analysis': 'We missed the deadline on {p} because roles were unclear, which I now see as typical of the “storming” stage.',
    'Conclusion': 'I learned that agreeing roles early matters as much as the research itself.',
    'Action plan': 'In my next group project I will suggest a Gantt chart with named roles in the first meeting.',
}


@c9d.add('C1', (1, 2, 3), 'mcq')
def c9d_gibbs(r, D):
    l = local(r)
    k = r.choice(GIBBS)
    s = GIBBS_S[k].replace('{p}', l['p'])
    return MC(r, f'Which stage of Gibbs’ reflective cycle does this sentence from a reflective paper illustrate? “{s}”', k, r.sample([x for x in GIBBS if x != k], 3), f'{k}.')


@c9d.add('C2', (1, 2, 3, 4), 'explain')
def c9d_desc(r, D):
    l = local(r)
    return Q(f'A student’s reflective paper on a project about {l["p"]} says: “We met, did our research, made a presentation and finished on time.” Explain why this is description rather than reflection, and how it could be improved.',
             'It only reports what happened; reflection evaluates what went well or badly, analyses why, and states what the writer learned and will do differently (e.g. how roles were shared and what that taught them).',
             '1 mark identifies description only; 1 mark what reflection adds (evaluation/analysis); 1 mark suggests improvement [3]', 3, 'explain')


@c9d.add('C3', (2, 3, 4, 5), 'case')
def c9d_case(r, D):
    l = local(r)
    intro = f'A student is writing a reflective paper after a team project on {l["p"]}. The team’s solution was well received, but there was conflict over roles in the first two weeks.'
    parts = [
        lambda r: ('Identify two aspects of the project the student should reflect on.', 'Collaboration (roles, conflict, communication) and own learning (research skills, understanding of perspectives).', '1 mark each [2]'),
        lambda r: ('Write one sentence of analysis about the conflict.', 'e.g. “The conflict arose because we had not agreed roles, so two of us researched the same perspective.”', '1 mark cause identified; 1 mark explained [2]'),
        lambda r: ('Write an action plan point for a future project.', 'e.g. “Next time I will propose clear roles and a timeline at the first meeting.”', '1 mark specific; 1 mark linked to the experience [2]'),
        lambda r: ('Explain how the student’s view of the problem changed through hearing other team members’ research.', f'Learning other perspectives (e.g. on {l["g"]}) showed the problem is more complex and that solutions must suit different stakeholders.', '1 mark change; 1 mark linked to perspectives [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c9d.add('C4', (2, 3, 4, 5), 'long')
def c9d_essay(r, D):
    l = local(r)
    return essay_q(r, D, f'after a team project on {l["p"]}, reflecting on how the team worked together is more valuable than reflecting on the solution it produced',
                   ['Collaboration skills transfer to future projects and work.', 'Understanding team problems helps avoid them next time.'],
                   ['Reflecting on the solution shows learning about the issue and perspectives.', 'Evaluating evidence used for the solution builds research skills.'],
                   'Both are valuable; the best reflection links how the team worked to the quality of the solution.')


CHAPTERS[9] = [c9a, c9b, c9c, c9d]
